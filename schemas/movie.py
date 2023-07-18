from pydantic import BaseModel, Field
from typing import Optional
import datetime


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=20)
    year: int = Field(le=datetime.date.today().year)
    category: str = Field(min_length=5, max_length=20)

    # The following replaces the use of "default" as a parameter in each Field()
    class Config:
        schema_extra = {
            "example": {
                "id": 0,
                "title": "Unknown title",
                "year": 2023,
                "category": "Unknown category",
            }
        }
