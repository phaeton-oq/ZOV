from sqlalchemy.ext.asyncio import AsyncSession

from app.models import GameState

DEFAULT_HP = 50


async def get_or_create_state(session: AsyncSession, player_id: str) -> GameState:
    state = await session.get(GameState, player_id)
    if state is None:
        state = GameState(
            player_id=player_id,
            hp=DEFAULT_HP,
            max_hp=DEFAULT_HP,
            damage_per_click=1,
            total_damage=0,
        )
        session.add(state)
        await session.commit()
        await session.refresh(state)
    return state


async def hit_boss(session: AsyncSession, player_id: str) -> tuple[GameState, int, bool]:
    state = await get_or_create_state(session, player_id)
    if state.hp <= 0:
        return state, 0, False

    damage = state.damage_per_click
    state.hp -= damage
    state.total_damage += damage
    killed = False

    if state.hp <= 0:
        state.hp = 0
        killed = True
        state.max_hp += 20
        state.hp = state.max_hp
        state.damage_per_click += 1

    await session.commit()
    await session.refresh(state)
    return state, damage, killed
