from pydantic import BaseModel


class BrandBase(BaseModel):
    name: str
    niche: str
    target_audience: str
    tone: str
    brand_colors: list[str]
    fonts: dict
    watermark_text: str | None = None
    watermark_opacity: int = 40
    banned_words: list[str]
    preferred_cta: str


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BrandBase):
    pass


class BrandOut(BrandBase):
    id: int
    logo_url: str | None = None

    class Config:
        from_attributes = True
