from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.claude_service import ClaudeService
from app.expert_system.engine import PhysiqExpertEngine

router = APIRouter()


@router.post("/recommend")
async def get_recommendation(
    user_data: dict,
    db: AsyncSession = Depends(get_db),
):
    engine = PhysiqExpertEngine()
    expert_result = engine.run(user_data)

    claude = ClaudeService()
    response = await claude.get_coaching_advice(user_data, expert_result)
    return {"recommendation": response}
