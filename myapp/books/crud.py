from asyncpg import Connection
from typing import Optional
from myapp.books.schemas import BookCreate
from uuid import UUID


# -----------------------
# Create a book
# -----------------------
async def crud_create_book(conn : Connection, book : BookCreate):
    query = """
        INSERT INTO books(title,author,publisher,published_date,page_count,language)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *;
    """

    row = await conn.fetchrow(
            query,
            book.title,
            book.author,
            book.publisher,
            book.published_date,
            book.page_count,
            book.language
        )
    return dict(row) if row else None 
    

# ------------------------------------------
# Get All (Pagination + Filters + Search)
# ------------------------------------------
async def crud_get_books(conn : Connection, limit : int = 10, offset : int = 0, title : Optional[str] = None, author : Optional[str] = None, language : Optional[str] = None):
    conditions = []
    values = []

    # Dynamic filtering that prevents sql injection
    if title:
        conditions.append(f"title ILIKE ${len(values)+1}")
        values.append(f"%{title}%")
    if author:
        conditions.append(f"author ILIKE ${len(values)+1}")
        values.append(f"%{author}%")
    if language:
        conditions.append(f"language ILIKE ${len(values)+1}")
        values.append(f"%{language}%")
    values.append(limit)
    values.append(offset)

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    

    query = f"""
            SELECT * FROM books
            {where_clause}
            ORDER BY id 
            LIMIT ${len(values)-1} OFFSET ${len(values)};
            """
    

    rows = await conn.fetch(query,*values)
    return [dict(row) for row in rows]




# -----------------
# Delete 
# -----------------
async def crud_delete_book(conn : Connection, book_id : UUID):
    query = "DELETE FROM books WHERE id = $1 RETURNING *;"
    row = await conn.fetchrow(query,book_id)
    return dict(row) if row else None