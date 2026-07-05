"""initial

Revision ID: 001
Revises:
Create Date: 2026-07-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "game_state",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("boss_name", sa.String(length=128), nullable=False),
        sa.Column("hp", sa.Integer(), nullable=False),
        sa.Column("max_hp", sa.Integer(), nullable=False),
        sa.Column("damage_per_click", sa.Integer(), nullable=False),
        sa.Column("total_damage", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("game_state")
