from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class ConnectedAccount(Base):
    __tablename__ = "connected_accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="connected_accounts")


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    layout_config = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posters = relationship("Poster", back_populates="template")


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    size = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    template = relationship("Template", back_populates="posters")
    captions = relationship("Caption", back_populates="poster")


class Caption(Base):
    __tablename__ = "captions"

    id = Column(Integer, primary_key=True)
    poster_id = Column(Integer, ForeignKey("posters.id"), nullable=False)
    content = Column(Text, nullable=False)
    hashtags = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    poster = relationship("Poster", back_populates="captions")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="campaigns")
    items = relationship("CampaignItem", back_populates="campaign")


class CampaignItem(Base):
    __tablename__ = "campaign_items"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    day_index = Column(Integer, nullable=False)
    poster_id = Column(Integer, ForeignKey("posters.id"), nullable=False)
    caption_id = Column(Integer, ForeignKey("captions.id"), nullable=False)
    scheduled_time = Column(DateTime(timezone=True))

    campaign = relationship("Campaign", back_populates="items")


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    poster_id = Column(Integer, ForeignKey("posters.id"), nullable=False)
    caption_id = Column(Integer, ForeignKey("captions.id"), nullable=False)
    platforms = Column(JSON, nullable=False)
    scheduled_for = Column(DateTime(timezone=True), nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="scheduled_posts")
    logs = relationship("PostLog", back_populates="scheduled_post")


class PostLog(Base):
    __tablename__ = "post_logs"

    id = Column(Integer, primary_key=True)
    scheduled_post_id = Column(Integer, ForeignKey("scheduled_posts.id"), nullable=False)
    status = Column(String, nullable=False)
    detail = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    scheduled_post = relationship("ScheduledPost", back_populates="logs")


class AnalyticsMetric(Base):
    __tablename__ = "analytics_metrics"

    id = Column(Integer, primary_key=True)
    scheduled_post_id = Column(Integer, ForeignKey("scheduled_posts.id"), nullable=False)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AISuggestion(Base):
    __tablename__ = "ai_suggestions"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    suggestion_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
