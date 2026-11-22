import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.config import settings
from app.api.routes import router as api_router
from app.services.similarity_engine import get_sentence_transformer_model

import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Warm up model in background daemon thread for instant startup
    print(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}...")
    threading.Thread(target=get_sentence_transformer_model, daemon=True).start()
    yield
    print("Shutting down ResumeAI...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Production-grade AI-Powered Resume Analyzer & Job Matcher with semantic similarity and LLM feedback.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes under /api
app.include_router(api_router, prefix=settings.API_PREFIX)

# Static Files & SPA Frontend Serving
STATIC_DIR = Path(__file__).resolve().parent / "static"
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

serve_dir = None
if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
    serve_dir = FRONTEND_DIST
elif STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists():
    serve_dir = STATIC_DIR

if serve_dir:
    app.mount("/assets", StaticFiles(directory=str(serve_dir / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API paths
        if full_path.startswith("api/") or full_path == "api":
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        file_path = serve_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(serve_dir / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.PROJECT_VERSION,
            "status": "online",
            "api_docs": "/docs",
            "message": "FastAPI ResumeAI Engine is running. Build frontend with 'npm run build' to serve static UI."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
