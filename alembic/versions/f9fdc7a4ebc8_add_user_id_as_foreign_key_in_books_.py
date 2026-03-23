"""Add user_id as foreign key in books table to show ownership

Revision ID: f9fdc7a4ebc8
Revises: 6a052f3b888b
Create Date: 2026-03-23 23:27:25.321068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9fdc7a4ebc8'
down_revision: Union[str, Sequence[str], None] = '6a052f3b888b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
            ALTER TABLE books
            ADD COLUMN user_id UUID
            REFERENCES users(id);
""")


def downgrade() -> None:
    """Downgrade schema."""
    
    op.execute("""
            ALTER TABLE books
            DROP COLUMN user_id;
""")