from pydantic import BaseModel


class ChatRequest(BaseModel):
    brand_id: int
    message: str


class ChatResponse(BaseModel):
    reply: str
    intent: str
    action: str | None = None
    action_payload: dict | None = None


class OptimizeRequest(BaseModel):
    brand_id: int
    scheduled_post_id: int


class OptimizeResponse(BaseModel):
    suggestions: list[str]
