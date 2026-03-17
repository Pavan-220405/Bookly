from fastapi import FastAPI
from myapp.books.routes import book_router

version = "v1"
app = FastAPI(
    title="Bookly - Book Review API",
    description="A REST API for book review web service",
    version=version
    )

@app.get('/',tags=["Health Check"])
async def health_check():
    return {"status" : "Bookly API Running Successfully"} 

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])