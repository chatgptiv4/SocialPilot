# SocialPilot AI

Full-stack SaaS app for AI-driven social media posters, captions, scheduling, and analytics.

## Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment

```bash
cp ../.env.example .env
```

### PostgreSQL

1. Install PostgreSQL locally.
2. Create database:
   ```bash
   createdb socialpilot
   ```
3. Update `DATABASE_URL` in `.env` if needed.

### Alembic Migrations

```bash
alembic upgrade head
```

### Seed Templates

```bash
python scripts/seed_templates.py
```

### Run API

```bash
uvicorn app.main:app --reload
```

### Redis + Celery

Start Redis locally:
```bash
redis-server
```

Start Celery worker:
```bash
celery -A app.tasks.celery_app.celery_app worker --loglevel=info
```

## Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
pytest
```

## API Endpoints

- Auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`
- Brand DNA: `/api/brands`
- Posters: `/api/posters/generate`, `/api/posters/{id}`
- AI: `/api/ai/chat`, `/api/ai/generate-campaign`, `/api/ai/generate-caption`, `/api/ai/optimize`
- Schedule: `/api/schedule`, `/api/schedule/{id}/publish-now`
- Connected Accounts: `/api/social/accounts`, `/api/social/connect/{provider}`
- Analytics: `/api/analytics/overview`, `/api/analytics/posts/{id}`
