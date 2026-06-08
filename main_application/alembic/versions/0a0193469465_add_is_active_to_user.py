"""add is_active to user

Revision ID: 0a0193469465
Revises: bdd654f5ef4b
Create Date: 2026-06-07 13:09:31.386673

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0a0193469465"
down_revision: Union[str, Sequence[str], None] = "bdd654f5ef4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_active", sa.Boolean(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("is_active")
