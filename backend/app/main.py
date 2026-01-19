from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import gray_sketch
from app.routers import color_sketch
from app.routers import sticker
from app.routers import cartoon
from app.routers import neon_glow
from app.routers import comic_art
from app.routers import manga
from app.routers import popart
from app.routers import style_transfer
from app.routers import pixel_art

app = FastAPI(
    title="Image Transformation API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(gray_sketch.router)
app.include_router(color_sketch.router)
app.include_router(sticker.router)
app.include_router(cartoon.router)
app.include_router(neon_glow.router)
app.include_router(comic_art.router)
app.include_router(manga.router)
app.include_router(popart.router)
app.include_router(style_transfer.router)
app.include_router(pixel_art.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
