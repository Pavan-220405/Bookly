from fastapi import FastAPI
from myapp.books.routes import book_router
from myapp.db.engine import init_db
from contextlib import asynccontextmanager


# The events that should run only at the beginning of the server 
@asynccontextmanager
async def life_span(app : FastAPI):
        print("Server is starting...")
        await init_db()
        yield 
        print("Server has been stopped")



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