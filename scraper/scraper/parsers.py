"""This file contains parsers."""
import logging
from datetime import date
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

from scraper.constants import (
    DISTRICT_PROPERTIES,
    PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS,
    PROPERTY_TO_TYPE_WRAPPER,
    RU_HEADER_TO_PROPERTY,
)
from scraper.exceptions import NoCurrentDateException
from scraper.models import District, Locality
from scraper.types import DistrictType
from scraper.utils import get_date_from_str

logger = logging.getLogger(__name__)


class CovidPageParser(HTMLParser):
    """This class parses an html page with statistics on the incidence of covid."""

    row_index = None
    col_index = -1
    row_span = None
    col_index_to_property: Dict[int, str] = {}
    current_date = None
    result: List[DistrictType] = []
    current_district: Optional[District] = None
    current_locality: Optional[Locality] = None
    current_tag = None
    skip_all = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """
        Handle start tag.

        :param tag:
        :param attrs:
        :return:
        """
        if self.skip_all:
            return

        self.current_tag = tag

        if tag == "tr":
            self.handle_start_of_tr_tag()

        if tag == "td":
            self.handle_start_of_td_tag(attrs)

    def handle_start_of_tr_tag(self) -> None:
        """
        Handle <tr> tag.

        :return:
        """
        self.col_index = -1
        if self.row_index is None:
            self.row_index = 0
        else:
            self.row_index += 1
        if self.row_index != 0:
            if self.current_district and self.current_locality:
                self.current_district.localities.append(self.current_locality)
            self.current_locality = Locality()

    def handle_start_of_td_tag(self, attrs: List[Tuple[str, Optional[str]]]) -> None:
        """
        Handle <td> tag.

        :param attrs:
        :return:
        """
        if self.col_index == -1:
            if self.row_span:
                self.col_index = 2
                self.row_span -= 1
            else:
                self.col_index = 0

                for attr, value in attrs:
                    if attr == "rowspan" and isinstance(value, str):
                        self.row_span = int(value) - 1
                        break

                if self.current_district:
                    self.result.append(self.current_district.dict())
                if self.row_index != 0:
                    self.current_district = District(date=self.current_date)
        else:
            self.col_index += 1

    def handle_endtag(self, tag: str) -> None:
        """
        Handle end tag.

        :param tag:
        :return:
        """
        if tag == "table":
            if self.current_district and self.current_locality:
                self.current_district.localities.append(self.current_locality)
                self.result.append(self.current_district.dict())

        self.current_tag = None

    def handle_data(self, data: str) -> None:
        """
        Handle text within tag.

        :param data:
        :return:
        """
        if self.skip_all:
            return

        if self.current_tag == "h1":
            self.set_current_date_from_title(data)
        if self.current_tag == "td":
            data = data.strip() or "0"
            if data == "Ленинградская область":
                # do not parse summary
                self.skip_all = True
                self.current_locality = None
                self.current_district = None
                return
            if self.row_index == 0:
                if data in RU_HEADER_TO_PROPERTY:
                    prop = RU_HEADER_TO_PROPERTY[data]
                    self.col_index_to_property[self.col_index] = prop
                else:
                    self.set_current_date_from_table(data)
                    self.col_index_to_property[
                        self.col_index
                    ] = PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS
            else:
                prop = self.col_index_to_property[self.col_index]
                wrapper = PROPERTY_TO_TYPE_WRAPPER[prop]
                value = wrapper(data)
                if prop in DISTRICT_PROPERTIES:
                    setattr(self.current_district, prop, value)
                else:
                    setattr(self.current_locality, prop, value)

    def set_current_date_from_title(self, data: str) -> None:
        """
        Parse date from title.

        :param data:
        :return:
        """
        date_as_str = data.strip().split().pop()
        try:
            system_date = self.get_system_date()
            date_from_title = get_date_from_str(date_as_str, "%d.%m.%Y")
            if date_from_title.date() == system_date:
                self.current_date = date_from_title
        except ValueError:
            self.error(
                f"Failed to parse current date from title. Invalid value: {date_as_str}"
            )

    def set_current_date_from_table(self, data: str) -> None:
        """
        Parse date from table.

        :param data:
        :return:
        """
        try:
            system_date = self.get_system_date()
            current_date_from_table = get_date_from_str(data)
            if not self.current_date and current_date_from_table.date() == system_date:
                self.current_date = current_date_from_table
        except ValueError:
            self.error(
                f"Failed to parse current date from table. Invalid value: {data}"
            )
        finally:
            if not self.current_date:
                raise NoCurrentDateException(
                    "Failed to get current date from html page."
                )
            # elif self.current_date.date() != date.today():
            #     raise CurrentDatesNotMatchException(
            #         f"Date from page: {self.current_date.date()} != system date: {date.today()}"
            #     )

    def get_system_date(self) -> date:
        """
        Return current date from system.

        :return:
        """
        return date.today()

    def parse(self, data: str) -> List[DistrictType]:
        """
        Return parsed data.

        :param data:
        :return:
        """
        super().feed(data)
        return self.result

    def error(self, message: str) -> None:
        """
        Handle parser error.

        :param message:
        :return:
        """
        logger.error(message)
