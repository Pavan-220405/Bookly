from asyncpg import Connection
from myapp.reviews.schemas import ReviewCRUD


async def crud_write_review(review : ReviewCRUD, conn : Connection):
    query = """
        INSERT INTO reviews (book_id,user_id,review_text,rating)
        VALUES ($1, $2, $3, $4)
        RETURNING *;
    """
    row = await conn.fetchrow(query,review.book_id,review.user_id,review.review_text,review.rating)

    return dict(row) if row else None