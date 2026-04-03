from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import HTMLResponse

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


# @app.get('/',tags=["Health Check"])
# async def health_check():
#     return {"status" : "Bookly API Running Successfully"} 

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['Books'])
app.include_router(auth_router,prefix=f"/api/{version}/users",tags=['Users'])
app.include_router(review_router,prefix=f"/api/{version}/reviews",tags=['Reviews'])




@app.get("/", response_class=HTMLResponse,tags=["Landing page"])
async def landing_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bookly</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: radial-gradient(circle at top, #1a1a2e, #0f0f1a);
    color: white;
    overflow-x: hidden;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 60px;
}

.logo {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 1px;
}

.nav-links a {
    margin-left: 25px;
    text-decoration: none;
    color: #aaa;
    font-weight: 500;
    transition: 0.3s;
}

.nav-links a:hover {
    color: white;
}

.hero {
    height: 85vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0 20px;
}

.hero h1 {
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(90deg, #7f5af0, #2cb67d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 18px;
    max-width: 650px;
    margin: 20px 0 40px;
    color: #bbb;
}

.cta-buttons {
    display: flex;
    gap: 20px;
}

.primary-btn {
    padding: 14px 32px;
    border-radius: 40px;
    background: linear-gradient(90deg, #7f5af0, #2cb67d);
    border: none;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: 0.3s;
}

.primary-btn:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 10px 30px rgba(127, 90, 240, 0.4);
}

.secondary-btn {
    padding: 14px 32px;
    border-radius: 40px;
    background: transparent;
    border: 1px solid #444;
    color: white;
    cursor: pointer;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    padding: 80px 60px;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-10px);
    border-color: #7f5af0;
}

.card h3 {
    margin-bottom: 10px;
}

.card p {
    color: #aaa;
    font-size: 14px;
}

.footer {
    text-align: center;
    padding: 30px;
    color: #666;
}
</style>
</head>

<body>

<div class="navbar">
    <div class="logo">📚 Bookly</div>
    <div class="nav-links">
        <a href="#">Features</a>
        <a href="#">About</a>
        <a href="#">Login</a>
    </div>
</div>

<div class="hero">
    <h1>Read Smarter. Track Better.</h1>
    <p>Bookly is your intelligent reading companion. Organize your books, discover new ones, and power your reading journey with AI.</p>
    <div class="cta-buttons">
        <button class="primary-btn">Get Started</button>
        <button class="secondary-btn">Explore</button>
    </div>
</div>

<div class="features">
    <div class="card">
        <h3>📖 Smart Tracking</h3>
        <p>Keep track of every book you've read with a seamless experience.</p>
    </div>
    <div class="card">
        <h3>🤖 AI Recommendations</h3>
        <p>Get personalized book suggestions powered by intelligent models.</p>
    </div>
    <div class="card">
        <h3>⚡ Real-time Sync</h3>
        <p>Access your reading list anytime, anywhere across devices.</p>
    </div>
    <div class="card">
        <h3>📊 Insights</h3>
        <p>Analyze your reading habits and improve consistency.</p>
    </div>
</div>

<div class="footer">
    © 2026 Bookly • Built with ❤️
</div>

</body>
</html>
    """