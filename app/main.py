from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import settings
from app.routers import game, health

CLICKER_DIR = Path(__file__).resolve().parent.parent / "clicker"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="ZOV API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(game.router, prefix="/api")


@app.get("/")
async def index():
    return FileResponse(CLICKER_DIR / "index.html", media_type="text/html")


@app.get("/script.js")
async def script():
    return FileResponse(CLICKER_DIR / "script.js", media_type="application/javascript")


@app.get("/style.css")
async def style():
    return FileResponse(CLICKER_DIR / "style.css", media_type="text/css")
