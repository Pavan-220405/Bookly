from asyncpg import Pool
import asyncio

async def create_books_table(pool : Pool):
    async with pool.acquire() as conn:
        query = """
            CREATE TABLE IF NOT EXISTS books(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publisher VARCHAR(255) NOT NULL,
                published_date DATE,
                page_count INTEGER NOT NULL CHECK (page_count >= 1),
                language VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        
        await conn.execute(query)
        print("Books Table Created!!")


if __name__ == "__main__":
    from myapp.db.engine import get_pool

    async def main():
        pool = get_pool()
        await create_books_table(pool)

    asyncio.run(main())