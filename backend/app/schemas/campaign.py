from datetime import datetime
from pydantic import BaseModel


class CampaignGenerate(BaseModel):
    brand_id: int
    name: str
    duration_days: int


class CampaignItemOut(BaseModel):
    day_index: int
    poster_id: int
    caption_id: int
    scheduled_time: datetime | None = None


class CampaignOut(BaseModel):
    id: int
    name: str
    duration_days: int
    items: list[CampaignItemOut]

    class Config:
        from_attributes = True
