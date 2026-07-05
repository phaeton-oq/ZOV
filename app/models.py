from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class GameState(Base):
    __tablename__ = "game_state"

    player_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    hp: Mapped[int] = mapped_column(Integer, default=50)
    max_hp: Mapped[int] = mapped_column(Integer, default=50)
    damage_per_click: Mapped[int] = mapped_column(Integer, default=1)
    total_damage: Mapped[int] = mapped_column(Integer, default=0)
