import logging
from celery import shared_task
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.content import PostLog, ScheduledPost

logger = logging.getLogger(__name__)


@shared_task
def publish_scheduled_posts():
    db: Session = SessionLocal()
    try:
        posts = db.query(ScheduledPost).filter(ScheduledPost.published.is_(False)).all()
        for post in posts:
            post.published = True
            log = PostLog(scheduled_post_id=post.id, status="published", detail="Auto-published via worker")
            db.add(log)
            logger.info("Auto-published scheduled post %s", post.id)
        db.commit()
    finally:
        db.close()
