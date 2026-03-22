# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from myapp.db.engine import init_db, close_db, get_pool
# from myapp.db.redis_engine import init_redis, get_redis, close_redis
# from myapp.books.models import create_books_table
# from myapp.users.models import create_users_table

# from myapp.books.routes import book_router
# from myapp.users.routes import auth_router



# @asynccontextmanager
# async def life_span(app : FastAPI):
#     print("Server is starting...")

#     # Initialize pool
#     await init_db()
#     await init_redis()

#     # Create tables
#     pool = get_pool()
#     # await create_books_table(pool=pool) --> Done by Alembic
#     # await create_users_table(pool=pool) --> Done by Alembic
#     print("Databases and Tables initialized !!!")

#     yield

#     print("Server is shutting down...")
#     await close_db()
#     await close_redis()



# version = "v1"
# app = FastAPI(
#     title="Bookly - Book Review API",
#     description="A REST API for book review web service",
#     version=version,
#     lifespan=life_span
#     )


# @app.get('/',tags=["Health Check"])
# async def health_check():
#     return {"status" : "Bookly API Running Successfully"} 

# app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])
# app.include_router(auth_router,prefix=f"/api/{version}/users",tags=['Users'])