"""Add role in the users table

Revision ID: 6a052f3b888b
Revises: eddfd88378bb
Create Date: 2026-03-23 00:17:51.372326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a052f3b888b'
down_revision: Union[str, Sequence[str], None] = 'eddfd88378bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
               ALTER TABLE users
               ADD COLUMN role TEXT DEFAULT 'user';
""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
                ALTER TABLE users
                DROP COLUMN role;
""")
