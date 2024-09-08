"""This file contains constants."""

from typing import Callable, Dict, Final, Tuple, Union

PROPERTY_DISTRICT_DATE: Final = "date"
PROPERTY_DISTRICT: Final = "district"
PROPERTY_DISTRICT_TOTAL_NUMBER_OF_INFECTIONS: Final = (
    "district_total_number_of_infections"
)
PROPERTY_DISTRICT_TOTAL_NUMBER_OF_RECOVERIES: Final = (
    "district_total_number_of_recoveries"
)
PROPERTY_DISTRICT_TOTAL_PERCENTAGE_OF_RECOVERED: Final = (
    "district_total_percentage_of_recovered"
)
PROPERTY_DISTRICT_LOCALITIES: Final = "localities"
PROPERTY_LOCALITY: Final = "locality"
PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS: Final = "locality_number_of_infections"
PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS: Final = (
    "locality_total_number_of_infections"
)
PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES: Final = (
    "locality_total_number_of_recoveries"
)
DISTRICT_PROPERTIES: Tuple[str, str, str, str] = (
    PROPERTY_DISTRICT,
    PROPERTY_DISTRICT_TOTAL_NUMBER_OF_INFECTIONS,
    PROPERTY_DISTRICT_TOTAL_NUMBER_OF_RECOVERIES,
    PROPERTY_DISTRICT_TOTAL_PERCENTAGE_OF_RECOVERED,
)
LOCALITY_PROPERTIES = (
    PROPERTY_LOCALITY,
    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS,
    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES,
)
RU_HEADER_TO_PROPERTY = {
    "Район": PROPERTY_DISTRICT,
    "Число случаев": PROPERTY_DISTRICT_TOTAL_NUMBER_OF_INFECTIONS,
    "Населённый пункт": PROPERTY_LOCALITY,
    "Общее число случаев": PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS,
    "Число выздоровлений": PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES,
    "Число выздоровлений по районам": PROPERTY_DISTRICT_TOTAL_NUMBER_OF_RECOVERIES,
    "% выздоровевших от заболевших": PROPERTY_DISTRICT_TOTAL_PERCENTAGE_OF_RECOVERED,
}
PROPERTY_TO_TYPE_WRAPPER: Dict[
    str, Union[Callable[[str], str], Callable[[str], int], Callable[[str], float]]
] = {
    PROPERTY_DISTRICT: str,
    PROPERTY_DISTRICT_TOTAL_NUMBER_OF_INFECTIONS: int,
    PROPERTY_DISTRICT_TOTAL_NUMBER_OF_RECOVERIES: int,
    PROPERTY_DISTRICT_TOTAL_PERCENTAGE_OF_RECOVERED: lambda x: float(
        x.replace(",", ".")
    ),
    PROPERTY_LOCALITY: str,
    PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS: int,
    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_INFECTIONS: int,
    PROPERTY_LOCALITY_TOTAL_NUMBER_OF_RECOVERIES: int,
}
