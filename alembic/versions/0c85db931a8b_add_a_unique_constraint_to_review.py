"""Add a unique constraints to review and library

Revision ID: 0c85db931a8b
Revises: 22bc2bf4a18d
Create Date: 2026-05-01 11:46:01.231660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c85db931a8b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('UUSERGAMEREVIEW', 'reviews', ['user_id', 'game_id'])
    op.create_unique_constraint('UGAMEUSERENTRY', 'game_library', ['user_id', 'game_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('UUSERGAMEREVIEW', 'reviews')
    op.drop_constraint('UGAMEUSERENTRY', 'game_library')