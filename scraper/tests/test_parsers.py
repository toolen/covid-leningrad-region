import json
import os.path
from datetime import date

from scraper.parsers import CovidPageParser
from tests.conftest import date_parser


def test_covid_page_parser(path_to_files_dir):

    with open(os.path.join(path_to_files_dir, "page.html"), "r") as f:
        parser = CovidPageParser()
        parser.get_system_date = lambda: date.today().replace(
            year=2021, month=10, day=14
        )
        html = f.read()
        result = parser.parse(html)

        assert result is not None
        assert len(result) == 3

        with open(os.path.join(path_to_files_dir, "page.json"), "r") as json_file:
            json_data = json_file.read()
            dict_ = json.loads(json_data, object_hook=date_parser)

            assert result == dict_
