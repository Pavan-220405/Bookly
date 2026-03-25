from fastapi import FastAPI
from contextlib import asynccontextmanager

from myapp.db.engine import init_db, close_db, get_pool
from myapp.db.redis_engine import init_redis, close_redis

from myapp.books.routes import book_router
from myapp.users.routes import auth_router
from myapp.reviews.routes import review_router



@asynccontextmanager
async def life_span(app : FastAPI):
    print("Server is starting...")

    # Initialize pool
    await init_db()
    await init_redis()

    # Create tables
    pool = get_pool()
    print("Databases and Tables initialized !!!")

    yield

    print("Server is shutting down...")
    await close_db()
    await close_redis()



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
app.include_router(auth_router,prefix=f"/api/{version}/users",tags=['Users'])
app.include_router(review_router,prefix=f"/api/{version}/reviews",tags=['Reviews'])