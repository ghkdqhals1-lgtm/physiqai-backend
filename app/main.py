from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health, users, workouts, ai_coach
from app.routers import inbody, diet_logs, sleep_logs, weekly_reports

app = FastAPI(
    title="PhysiqAI API",
    version="0.1.0",
    debug=settings.app_debug,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(inbody.router, prefix="/api/v1/inbody", tags=["inbody"])
app.include_router(workouts.router, prefix="/api/v1/workout-logs", tags=["workout-logs"])
app.include_router(diet_logs.router, prefix="/api/v1/diet-logs", tags=["diet-logs"])
app.include_router(sleep_logs.router, prefix="/api/v1/sleep-logs", tags=["sleep-logs"])
app.include_router(weekly_reports.router, prefix="/api/v1/weekly-reports", tags=["weekly-reports"])
app.include_router(ai_coach.router, prefix="/api/v1/coach", tags=["ai-coach"])
