from datetime import datetime
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    brand_id: int
    poster_id: int
    caption_id: int
    platforms: list[str]
    scheduled_for: datetime


class ScheduleOut(BaseModel):
    id: int
    brand_id: int
    poster_id: int
    caption_id: int
    platforms: list[str]
    scheduled_for: datetime
    published: bool

    class Config:
        from_attributes = True
