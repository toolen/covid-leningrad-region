from datetime import datetime
from typing import Dict, List, Union

LocalityType = Dict[str, Union[str, int]]
DistrictType = Dict[str, Union[str, int, float, datetime, List[LocalityType]]]
