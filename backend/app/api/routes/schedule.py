import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.content import PostLog, ScheduledPost
from app.schemas.schedule import ScheduleCreate, ScheduleOut

router = APIRouter(prefix="/schedule", tags=["schedule"])
logger = logging.getLogger(__name__)


@router.post("", response_model=ScheduleOut)
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    scheduled = ScheduledPost(user_id=user.id, **payload.model_dump())
    db.add(scheduled)
    db.commit()
    db.refresh(scheduled)
    return scheduled


@router.get("", response_model=list[ScheduleOut])
def list_schedule(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(ScheduledPost).filter(ScheduledPost.user_id == user.id).all()


@router.post("/{schedule_id}/publish-now")
def publish_now(schedule_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    scheduled = db.query(ScheduledPost).filter(ScheduledPost.id == schedule_id, ScheduledPost.user_id == user.id).first()
    if not scheduled:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    scheduled.published = True
    log = PostLog(scheduled_post_id=scheduled.id, status="published", detail="Published manually")
    db.add(log)
    db.commit()
    logger.info("Manual publish for scheduled post %s", schedule_id)
    return {"status": "published"}
