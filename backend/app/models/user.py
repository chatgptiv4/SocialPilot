from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    brands = relationship("Brand", back_populates="owner")
    connected_accounts = relationship("ConnectedAccount", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")
    scheduled_posts = relationship("ScheduledPost", back_populates="user")
