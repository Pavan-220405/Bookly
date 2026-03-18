from fastapi import FastAPI
from myapp.books.routes import book_router
from contextlib import asynccontextmanager

from myapp.db.engine import init_db, close_db, get_pool
from myapp.books.models import create_books_table


@asynccontextmanager
async def life_span(app : FastAPI):
    print("Server is starting...")

    # Initialize pool
    await init_db()

    # Create tables
    await create_books_table(get_pool())
    print("Databases initialized !!!")

    yield

    print("Server is shutting down...")
    await close_db()



version = "v1"
app = FastAPI(
    title="Bookly - Book Review API",
    description="A REST API for book review web service",
    version=version,
    lifespan=life_span
    )



@app.get('/',tags=["Health Check"])
async def health_check():
    return {"status" : "Bookly API Running Successfully"} 

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])