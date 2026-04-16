"""SmartCampusAI Mobile Backend — FastAPI ana uygulama."""
from __future__ import annotations

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Proje kokunu PYTHONPATH'e ekle (Streamlit kodlarini import edebilmek icin)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .routers import auth, mood, ogrenci, messaging, ihbar, veli, ogretmen, rehber, yonetici


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama ayaga kalkarken + kapanirken."""
    print(f"[BACKEND] {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"[BACKEND] DATA_DIR: {settings.DATA_DIR}")
    print(f"[BACKEND] API Prefix: {settings.API_PREFIX}")
    yield
    print("[BACKEND] Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SmartCampusAI mobil uygulama icin REST API. Streamlit ile AYNI veriyi paylasir.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global error handler
@app.exception_handler(Exception)
async def global_exc(request: Request, exc: Exception):
    """Beklenmeyen hatalari loglayip 500 dondur."""
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Sunucu hatasi", "error": str(exc) if settings.DEBUG else "internal"},
    )


# Router'lari kaydet
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(mood.router, prefix=settings.API_PREFIX)
app.include_router(ogrenci.router, prefix=settings.API_PREFIX)
app.include_router(messaging.router, prefix=settings.API_PREFIX)
app.include_router(ihbar.router, prefix=settings.API_PREFIX)
app.include_router(veli.router, prefix=settings.API_PREFIX)
app.include_router(ogretmen.router, prefix=settings.API_PREFIX)
app.include_router(rehber.router, prefix=settings.API_PREFIX)
app.include_router(yonetici.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": f"/docs",
        "api": settings.API_PREFIX,
    }


@app.get(f"{settings.API_PREFIX}/health")
async def health():
    """Healthcheck — uptime monitorluk icin."""
    return {"status": "healthy", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mobile.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
