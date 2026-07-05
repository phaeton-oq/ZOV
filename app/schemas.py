from pydantic import BaseModel, ConfigDict


class GameStateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: str
    hp: int
    max_hp: int
    damage_per_click: int
    total_damage: int


class HitOut(BaseModel):
    damage: int
    killed: bool
    state: GameStateOut
