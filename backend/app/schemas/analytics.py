from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_impressions: int
    total_clicks: int
    total_likes: int
    total_comments: int


class AISuggestionOut(BaseModel):
    id: int
    suggestion_type: str
    content: str

    class Config:
        from_attributes = True
