"""create users and books tables

Revision ID: eddfd88378bb
Revises: 
Create Date: 2026-03-22 21:51:59.760861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eddfd88378bb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

    op.execute("""
                CREATE TABLE users(
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
                user_name TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                is_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
""")
    

    op.execute("""
                CREATE TABLE books(
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title TEXT UNIQUE NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT NOT NULL,
                published_date DATE,
                page_count INTEGER NOT NULL CHECK (page_count >= 1),
                language TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE books;")
    op.execute("DROP TABLE users;")
