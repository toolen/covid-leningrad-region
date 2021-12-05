"""This file contains models."""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class Locality(BaseModel):
    """This class contains fields for locality entity."""

    locality: str = ""
    locality_number_of_infections: int = 0
    locality_total_number_of_infections: int = 0
    locality_total_number_of_recoveries: int = 0


class District(BaseModel):
    """This class contains fields for district entity."""

    date: datetime = datetime.now()
    district: str = ""
    district_total_number_of_infections: int = 0
    district_total_number_of_recoveries: int = 0
    district_total_percentage_of_recovered: float = 0.0
    localities: List[Locality] = []
