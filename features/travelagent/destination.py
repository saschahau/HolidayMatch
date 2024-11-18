from typing import List

from pydantic import BaseModel

class Destination(BaseModel):
    name: str
    description: str
    climate: str
    activities: List[str]
    budget: str
    travel_tips: str
    best_time_to_visit: List[str]
    currency: str
    language: str
    trending: bool
    transportation: List[str]
