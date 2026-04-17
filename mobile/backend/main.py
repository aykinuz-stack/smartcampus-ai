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
from .routers import auth, mood, ogrenci, messaging, ihbar, smarti, veli, ogretmen, rehber, yonetici


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
app.include_router(smarti.router, prefix=settings.API_PREFIX)


# ── Kurum hizmetleri endpoint'leri (basit) ──
from fastapi import Request as FRequest

@app.get(f"{settings.API_PREFIX}/kurum/duyurular")
async def kurum_duyurular():
    from .core.data_adapter import DataAdapter
    adapter = DataAdapter()
    return adapter.load("akademik/etkinlik_duyurular.json") or []

@app.get(f"{settings.API_PREFIX}/ai-treni/config")
async def ai_treni_config():
    """AI Treni yapilandirmasi — siniflar + kompartimanlar."""
    import sys
    sys.path.insert(0, str(settings.DATA_DIR.parent))
    try:
        from data.bilgi_treni.config import SINIF_LABELS, SINIF_THEMES, KOMPARTIMAN_LIST
        siniflar = [
            {"no": k, "label": v, "tema": SINIF_THEMES.get(k, ("", "#666"))[0],
             "renk": SINIF_THEMES.get(k, ("", "#666"))[1]}
            for k, v in SINIF_LABELS.items()
        ]
        kompartimanlar = [
            {"ikon": k[0], "baslik": k[1], "aciklama": k[2]}
            for k in KOMPARTIMAN_LIST
        ]
        return {"siniflar": siniflar, "kompartimanlar": kompartimanlar}
    except Exception as e:
        return {"siniflar": [], "kompartimanlar": [], "hata": str(e)}


@app.get(f"{settings.API_PREFIX}/ai-treni/quiz/{{sinif}}")
async def ai_treni_quiz(sinif: int):
    """Sinif bazli quiz sorulari."""
    import sys, json, random
    sys.path.insert(0, str(settings.DATA_DIR.parent))
    try:
        # Bilgi yarismasi sorulari
        from pathlib import Path
        quiz_files = list((settings.DATA_DIR / "bilgi_treni").glob("*quiz*")) + \
                     list((settings.DATA_DIR / "bilgi_treni").glob("*bilgi_yarismasi*"))

        # Content dosyalarindan da sorular cekilebilir
        sorular = []
        for qf in quiz_files:
            try:
                with open(qf, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if isinstance(d, list):
                    sorular.extend(d)
                elif isinstance(d, dict) and "sorular" in d:
                    sorular.extend(d["sorular"])
            except Exception:
                pass

        # Yoksa basit sorular uret
        if not sorular:
            kategoriler = ["Bilim", "Tarih", "Cografya", "Matematik", "Genel Kultur"]
            for i in range(10):
                sorular.append({
                    "soru": f"{sinif}. sinif {kategoriler[i%5]} sorusu #{i+1}",
                    "secenekler": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
                    "dogru": 0,
                    "kategori": kategoriler[i % 5],
                })

        random.shuffle(sorular)
        return {"sinif": sinif, "sorular": sorular[:10]}
    except Exception as e:
        return {"sinif": sinif, "sorular": [], "hata": str(e)}


@app.get(f"{settings.API_PREFIX}/kurum/yemek-menusu")
async def kurum_yemek():
    from .core.data_adapter import DataAdapter
    adapter = DataAdapter()
    return adapter.load("akademik/yemek_menusu.json") or []
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
