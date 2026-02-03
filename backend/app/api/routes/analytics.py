from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.content import AnalyticsMetric, AISuggestion
from app.schemas.analytics import AnalyticsOverview, AISuggestionOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
def overview(db: Session = Depends(get_db), user=Depends(get_current_user)):
    totals = db.query(
        func.coalesce(func.sum(AnalyticsMetric.impressions), 0),
        func.coalesce(func.sum(AnalyticsMetric.clicks), 0),
        func.coalesce(func.sum(AnalyticsMetric.likes), 0),
        func.coalesce(func.sum(AnalyticsMetric.comments), 0),
    ).first()
    return AnalyticsOverview(
        total_impressions=totals[0],
        total_clicks=totals[1],
        total_likes=totals[2],
        total_comments=totals[3],
    )


@router.get("/posts/{post_id}", response_model=list[AnalyticsOverview])
def post_metrics(post_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    metrics = db.query(AnalyticsMetric).filter(AnalyticsMetric.scheduled_post_id == post_id).all()
    return [
        AnalyticsOverview(
            total_impressions=metric.impressions,
            total_clicks=metric.clicks,
            total_likes=metric.likes,
            total_comments=metric.comments,
        )
        for metric in metrics
    ]


@router.get("/ai-suggestions", response_model=list[AISuggestionOut])
def ai_suggestions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(AISuggestion).all()
