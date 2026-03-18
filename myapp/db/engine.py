import asyncpg
from myapp.config import settings
from typing import Optional

# Global pool
pool: Optional[asyncpg.Pool] = None


# -------------------------
# Initialize DB Pool
# -------------------------
async def init_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=1,
            max_size=10
        )


# -------------------------
# Get Pool (SAFE ACCESS)
# -------------------------
def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_db() first.")
    return pool


# -------------------------
# Close DB Pool
# -------------------------
async def close_db():
    global pool
    if pool:
        await pool.close()
        pool = None