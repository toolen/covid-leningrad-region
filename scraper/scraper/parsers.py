import logging
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple, Union

from scraper.constants import (DISTRICT_PROPERTIES, PROPERTY_DISTRICT_DATE,
                               PROPERTY_DISTRICT_LOCALITIES,
                               PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS,
                               PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS,
                               PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES,
                               PROPERTY_TO_TYPE_WRAPPER, RU_HEADER_TO_PROPERTY)
from scraper.types import DistrictType
from scraper.utils import get_date_from_str

logger = logging.getLogger(__name__)


class CovidPageParser(HTMLParser):
    row_index = None
    col_index = -1
    row_span = None
    col_index_to_property: Dict[int, str] = {}
    current_date = None
    result: List[DistrictType] = []
    current_district = None
    current_locality = None
    current_tag = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        self.current_tag = tag

        if tag == "tr":
            self.col_index = -1
            if self.row_index is None:
                self.row_index = 0
            else:
                self.row_index += 1

            if self.row_index != 0:
                if self.current_district and self.current_locality:
                    self.current_district[PROPERTY_DISTRICT_LOCALITIES].append(
                        self.current_locality
                    )
                self.current_locality = {
                    PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS: 0,
                    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS: 0,
                    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES: 0,
                }

        if tag == "td":
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
                        self.result.append(self.current_district)
                    if self.row_index != 0:
                        self.current_district = {
                            PROPERTY_DISTRICT_DATE: self.current_date,
                            PROPERTY_DISTRICT_LOCALITIES: [],
                        }
            else:
                self.col_index += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            if self.current_district and self.current_locality:
                self.current_district[PROPERTY_DISTRICT_LOCALITIES].append(
                    self.current_locality
                )
                self.result.append(self.current_district)

        self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self.current_tag == "td":
            data = data.strip() or "0"
            if self.row_index == 0:
                if data in RU_HEADER_TO_PROPERTY:
                    prop = RU_HEADER_TO_PROPERTY[data]
                    self.col_index_to_property[self.col_index] = prop
                else:
                    self.current_date = get_date_from_str(data)
                    self.col_index_to_property[
                        self.col_index
                    ] = PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS
            else:
                prop = self.col_index_to_property[self.col_index]
                wrapper = PROPERTY_TO_TYPE_WRAPPER[prop]
                value: Union[str, int, float] = wrapper(data)
                if prop in DISTRICT_PROPERTIES:
                    self.current_district[prop] = value
                else:
                    self.current_locality[prop] = value

    def parse(self, data: str) -> List[DistrictType]:
        super().feed(data)
        return self.result

    def error(self, message: str) -> None:
        logger.error(message)
