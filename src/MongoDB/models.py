import uuid
from typing import Optional
from pydantic import BaseModel, Field

class SegmentData(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    SegmentID: str = Field(...)
    WeatherStation: str = Field(...)
    Date: str = Field(...)
    Speed: str = Field(...)
    Rain: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "SegmentID": "1",
                "WeatherStation": "Bellevue",
                "Date": "11/12/2022",
                "Speed": "60",
                "Rain": "0.5"
            }
        }

class SegmentDataUpdate(BaseModel):
    SegmentID: Optional[str]
    WeatherStation: Optional[str]
    Date: Optional[str]
    Speed: Optional[str]
    Rain: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "SegmentID": "1",
                "WeatherStation": "Bellevue",
                "Date": "11/12/2022",
                "Speed": "60",
                "Rain": "0.5"
            }
        }