"""require user id not null

Revision ID: 6cde8b243f7d
Revises: 9983a1e2e606
Create Date: 2025-02-14 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6cde8b243f7d"
down_revision: Union[str, None] = "9983a1e2e606"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "validation_history", "user_id", existing_type=sa.Integer(), nullable=False
    )
    op.alter_column(
        "chat_history", "user_id", existing_type=sa.Integer(), nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "chat_history", "user_id", existing_type=sa.Integer(), nullable=True
    )
    op.alter_column(
        "validation_history", "user_id", existing_type=sa.Integer(), nullable=True
    )
