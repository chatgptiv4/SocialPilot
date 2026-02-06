from fastapi import FastAPI
from sqlalchemy import text
import redis
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai, analytics, auth, brands, posters, schedule, social
from app.websockets.chat import router as chat_router
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(brands.router, prefix=settings.api_v1_prefix)
app.include_router(posters.router, prefix=settings.api_v1_prefix)
app.include_router(ai.router, prefix=settings.api_v1_prefix)
app.include_router(schedule.router, prefix=settings.api_v1_prefix)
app.include_router(social.router, prefix=settings.api_v1_prefix)
app.include_router(analytics.router, prefix=settings.api_v1_prefix)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/health")
def health_check():
    db_status = "ok"
    redis_status = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        db_status = f"error: {exc}"
    try:
        client = redis.from_url(settings.redis_url)
        client.ping()
    except Exception as exc:  # noqa: BLE001
        redis_status = f"error: {exc}"
    return {"database": db_status, "redis": redis_status}
