"""Add reviews table

Revision ID: af7ec92f353a
Revises: f9fdc7a4ebc8
Create Date: 2026-03-25 22:58:51.283580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af7ec92f353a'
down_revision: Union[str, Sequence[str], None] = 'f9fdc7a4ebc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    op.execute("""
            CREATE TABLE reviews(
               id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
               book_id UUID NOT NULL REFERENCES books(id) ON DELETE CASCADE,
               user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
               review_text TEXT NOT NULL,
               rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
               created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

               CONSTRAINT unique_user_book_review UNIQUE (user_id, book_id)
               );
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE reviews;")