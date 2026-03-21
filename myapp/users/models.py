from asyncpg import Pool


async def create_users_table(pool : Pool):
    pgcrypto_query = 'CREATE EXTENSION IF NOT EXISTS "pgcrypto";'
    table_query = """
            CREATE TABLE IF NOT EXISTS users(
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
        """
    
    async with pool.acquire() as conn:
        await conn.execute(pgcrypto_query)
        await conn.execute(table_query)
        print("Users table created successfully ")