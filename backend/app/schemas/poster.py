from datetime import datetime
from pydantic import BaseModel


class PosterGenerate(BaseModel):
    brand_id: int
    template_id: int
    title: str
    size: str
    overlay_text: str
    background_url: str | None = None
    logo_url: str | None = None


class PosterOut(BaseModel):
    id: int
    brand_id: int
    template_id: int
    title: str
    size: str
    image_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class CaptionGenerate(BaseModel):
    poster_id: int
    prompt: str


class CaptionOut(BaseModel):
    id: int
    poster_id: int
    content: str
    hashtags: list[str]

    class Config:
        from_attributes = True
