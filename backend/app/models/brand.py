from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    niche = Column(String, nullable=False)
    target_audience = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    brand_colors = Column(JSON, nullable=False)
    fonts = Column(JSON, nullable=False)
    logo_url = Column(String)
    watermark_text = Column(String)
    watermark_opacity = Column(Integer, default=40)
    banned_words = Column(JSON, nullable=False)
    preferred_cta = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="brands")
    assets = relationship("BrandAsset", back_populates="brand")


class BrandAsset(Base):
    __tablename__ = "brand_assets"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    asset_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    brand = relationship("Brand", back_populates="assets")
