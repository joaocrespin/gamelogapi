"""Create unique constraint for user email

Revision ID: de8843220337
Revises: 0c85db931a8b
Create Date: 2026-05-24 09:42:10.176210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de8843220337'
down_revision: Union[str, Sequence[str], None] = '0c85db931a8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('UQUSEREMAIL', 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('UQUSEREMAIL', 'users')
