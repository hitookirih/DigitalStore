"""add password to user

Revision ID: bdd654f5ef4b
Revises: 734e678ee13f
Create Date: 2026-06-07 11:32:47.524545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "bdd654f5ef4b"
down_revision: Union[str, Sequence[str], None] = "734e678ee13f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("password", sa.String(), nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("password")

