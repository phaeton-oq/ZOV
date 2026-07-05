from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.deps import get_player_id
from app.schemas import GameStateOut, HitOut
from app.services import get_or_create_state, hit_boss

router = APIRouter(prefix="/game", tags=["game"])


@router.get("", response_model=GameStateOut)
async def get_game(
    player_id: str = Depends(get_player_id),
    session: AsyncSession = Depends(get_db),
):
    return await get_or_create_state(session, player_id)


@router.post("/hit", response_model=HitOut)
async def hit(
    player_id: str = Depends(get_player_id),
    session: AsyncSession = Depends(get_db),
):
    state, damage, killed = await hit_boss(session, player_id)
    return HitOut(damage=damage, killed=killed, state=state)
