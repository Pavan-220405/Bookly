from asyncpg import Pool

async def create_books_table(pool : Pool):
    pgcrypto_query = 'CREATE EXTENSION IF NOT EXISTS "pgcrypto";'
    table_query = """
            CREATE TABLE IF NOT EXISTS books(
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
            """
    
    async with pool.acquire() as conn:
        await conn.execute(pgcrypto_query)
        await conn.execute(table_query)
        print("Books table created successfully")