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

# ── Dil Gelisimi (TUM ROLLER) ──
@app.get(f"{settings.API_PREFIX}/dil/dersler")
async def dil_dersler(dil: str = "ingilizce"):
    """Dil dersleri — tum roller erisebilir."""
    import json
    from pathlib import Path
    dil_map = {
        "ingilizce": "fono/fono_lessons.json",
        "almanca": "fono_almanca_104/fono_almanca_104_lessons.json",
        "fransizca": "fono_fransizca/fono_fransizca_lessons.json",
        "italyanca": "fono_italyanca/fono_italyanca_lessons.json",
        "ispanyolca": "fono_ispanyolca/fono_ispanyolca_lessons.json",
    }
    rel = dil_map.get(dil, dil_map["ingilizce"])
    data = None
    for sp in [settings.DATA_DIR / rel,
               Path(__file__).resolve().parent.parent.parent / "data" / rel]:
        if sp.exists():
            try:
                with open(sp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data: break
            except Exception: pass
    if not data: data = {}
    lessons = data.get("lessons", []) if isinstance(data, dict) else []
    ders_listesi = []
    for i, l in enumerate(lessons):
        voc = l.get("vocabulary", l.get("words", []))
        ders_listesi.append({
            "no": l.get("ders", i + 1),
            "title": l.get("title", f"Ders {i+1}"),
            "kelime_sayisi": len(voc),
            "gramer_sayisi": len(l.get("grammar_topics", [])),
            "alistirma_sayisi": len(l.get("exercises", [])),
        })
    diller = []
    for dk, dp in dil_map.items():
        for sp in [settings.DATA_DIR / dp,
                   Path(__file__).resolve().parent.parent.parent / "data" / dp]:
            if sp.exists(): diller.append(dk); break
    return {"dil": dil, "toplam_ders": len(lessons), "diller": diller, "dersler": ders_listesi}


@app.get(f"{settings.API_PREFIX}/dil/ders/{{ders_no}}")
async def dil_ders_detay(ders_no: int, dil: str = "ingilizce"):
    """Tek ders detayi — tum roller."""
    import json
    from pathlib import Path
    dil_map = {
        "ingilizce": "fono/fono_lessons.json",
        "almanca": "fono_almanca_104/fono_almanca_104_lessons.json",
        "fransizca": "fono_fransizca/fono_fransizca_lessons.json",
        "italyanca": "fono_italyanca/fono_italyanca_lessons.json",
        "ispanyolca": "fono_ispanyolca/fono_ispanyolca_lessons.json",
    }
    rel = dil_map.get(dil, dil_map["ingilizce"])
    data = None
    for sp in [settings.DATA_DIR / rel,
               Path(__file__).resolve().parent.parent.parent / "data" / rel]:
        if sp.exists():
            try:
                with open(sp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data: break
            except Exception: pass
    if not data: data = {}
    lessons = data.get("lessons", []) if isinstance(data, dict) else []
    lesson = None
    for l in lessons:
        if l.get("ders") == ders_no or lessons.index(l) == ders_no - 1:
            lesson = l; break
    if not lesson:
        return {"hata": f"Ders {ders_no} bulunamadi"}
    # Kelime alanini normalize et (en/de/fr/it/es -> word + tr)
    dil_key = {"ingilizce": "en", "almanca": "de", "fransizca": "fr",
               "italyanca": "it", "ispanyolca": "es"}.get(dil, "en")
    vocabulary = lesson.get("vocabulary", lesson.get("words", []))
    normalized_vocab = []
    for v in vocabulary:
        word = v.get(dil_key) or v.get("en") or v.get("word") or v.get("kelime", "")
        normalized_vocab.append({
            "word": word,
            "pron": v.get("pron", ""),
            "tr": v.get("tr", v.get("meaning", "")),
        })
    return {
        "no": lesson.get("ders", ders_no),
        "title": lesson.get("title", ""),
        "dil": dil,
        "vocabulary": normalized_vocab,
        "grammar_topics": lesson.get("grammar_topics", []),
        "grammar_examples": lesson.get("grammar_examples", []),
        "reading": lesson.get("reading", ""),
        "exercises": lesson.get("exercises", []),
    }


# ── Dijital Kutuphane ──
@app.get(f"{settings.API_PREFIX}/dijital-kutuphane/icerik")
async def dk_icerik():
    """Dijital kutuphane — mobilde calisacak icerikler."""
    kategoriler = [
        {"id": "youtube", "ikon": "📺", "baslik": "YouTube Kanalları",
         "aciklama": "Eğitim kanalları", "renk": "#DC2626",
         "icerikler": [
             {"ad": "TRT Çocuk", "url": "https://www.youtube.com/trtcocuk", "tur": "video"},
             {"ad": "Niloya", "url": "https://www.youtube.com/@niloyatv", "tur": "video"},
             {"ad": "Kukuli", "url": "https://www.youtube.com/Kukuli", "tur": "video"},
             {"ad": "Düşyeri", "url": "https://www.youtube.com/@Dusyeri", "tur": "video"},
             {"ad": "EBA", "url": "https://www.youtube.com/@EbaGovTr-Eba", "tur": "video"},
             {"ad": "Robotistan", "url": "https://www.youtube.com/c/robotistan", "tur": "video"},
             {"ad": "Super Simple Songs", "url": "https://www.youtube.com/user/SuperSimpleSongs", "tur": "video"},
             {"ad": "Sesame Street", "url": "https://www.youtube.com/sesamestreet", "tur": "video"},
             {"ad": "Eğlenceli Bilim", "url": "https://youtube.com/@eglencelibilim", "tur": "video"},
             {"ad": "Pinkfong", "url": "https://www.youtube.com/Pinkfong", "tur": "video"},
         ]},
        {"id": "e_ogrenme", "ikon": "🎓", "baslik": "E-Öğrenme Platformları",
         "aciklama": "İnteraktif öğrenme", "renk": "#2563EB",
         "icerikler": [
             {"ad": "Khan Academy", "url": "https://tr.khanacademy.org", "tur": "platform"},
             {"ad": "EBA", "url": "https://www.eba.gov.tr", "tur": "platform"},
             {"ad": "Vitamin Eğitim", "url": "https://www.vitaminegitim.com", "tur": "platform"},
             {"ad": "Morpa Kampüs", "url": "https://www.morpakampus.com", "tur": "platform"},
         ]},
        {"id": "interaktif", "ikon": "🔬", "baslik": "İnteraktif Araçlar",
         "aciklama": "Simülasyon ve lab", "renk": "#059669",
         "icerikler": [
             {"ad": "PhET Simülasyonları", "url": "https://phet.colorado.edu/tr/", "tur": "lab"},
             {"ad": "GeoGebra", "url": "https://www.geogebra.org", "tur": "lab"},
             {"ad": "Desmos", "url": "https://www.desmos.com/calculator", "tur": "lab"},
             {"ad": "Scratch", "url": "https://scratch.mit.edu", "tur": "kodlama"},
             {"ad": "Code.org", "url": "https://code.org", "tur": "kodlama"},
         ]},
        {"id": "radyo", "ikon": "📻", "baslik": "Eğitim Radyosu",
         "aciklama": "Sesli yayınlar", "renk": "#7C3AED",
         "icerikler": [
             {"ad": "TRT Radyo Çocuk", "url": "https://www.trtdinle.com/canli/radyo-cocuk", "tur": "radyo"},
             {"ad": "TRT Radyo 1", "url": "https://www.trtdinle.com/canli/radyo1", "tur": "radyo"},
         ]},
        {"id": "muze", "ikon": "🏛️", "baslik": "Sanal Müzeler",
         "aciklama": "Online tur", "renk": "#D97706",
         "icerikler": [
             {"ad": "Google Arts & Culture", "url": "https://artsandculture.google.com", "tur": "muze"},
             {"ad": "Topkapı Sarayı", "url": "https://www.google.com/maps/@41.0115,28.9833,3a,75y", "tur": "muze"},
             {"ad": "Louvre Müzesi", "url": "https://www.louvre.fr/en/online-tours", "tur": "muze"},
             {"ad": "British Museum", "url": "https://www.britishmuseum.org/collection", "tur": "muze"},
             {"ad": "NASA", "url": "https://www.nasa.gov/stem", "tur": "bilim"},
         ]},
        {"id": "sesli_kitap", "ikon": "🎧", "baslik": "Sesli Kitaplar",
         "aciklama": "Dinleyerek öğren", "renk": "#EC4899",
         "icerikler": [
             {"ad": "Masal Dinle (YouTube)", "url": "https://www.youtube.com/results?search_query=masal+dinle+çocuk", "tur": "ses"},
             {"ad": "Sesli Hikayeler", "url": "https://www.youtube.com/results?search_query=sesli+hikaye+çocuk", "tur": "ses"},
         ]},
        {"id": "kelime", "ikon": "📖", "baslik": "Kelime Hazinesi",
         "aciklama": "Kelime öğren", "renk": "#0891B2",
         "icerikler": [
             {"ad": "Türkçe Sözlük (TDK)", "url": "https://sozluk.gov.tr", "tur": "sozluk"},
             {"ad": "Tureng (İng-Tr)", "url": "https://tureng.com", "tur": "sozluk"},
         ]},
    ]
    return {"kategoriler": kategoriler, "toplam_kategori": len(kategoriler)}


# ── Bilgi Yarismasi ──
@app.get(f"{settings.API_PREFIX}/bilgi-yarismasi/{level}")
async def bilgi_yarismasi(level: str = "ilkokul"):
    """Bilgi yarismasi sorulari — ilkokul/ortaokul/lise."""
    import sys, json, random
    sys.path.insert(0, str(settings.DATA_DIR.parent))
    try:
        from views.bilgi_yarismasi_game import _build_questions_json
        sorular = json.loads(_build_questions_json(level))
        random.shuffle(sorular)
        # Normalize: k=kategori, s=soru, o=secenekler, d=dogru, a=aciklama
        normalized = []
        for q in sorular[:15]:
            normalized.append({
                "kategori": q.get("k", ""),
                "soru": q.get("s", ""),
                "secenekler": q.get("o", []),
                "dogru": q.get("d", 0),
                "aciklama": q.get("a", ""),
            })
        return {"level": level, "toplam": len(sorular), "sorular": normalized}
    except Exception as e:
        return {"level": level, "toplam": 0, "sorular": [], "hata": str(e)}


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


# ── Revir (Okul Sagligi) ──
@app.get(f"{settings.API_PREFIX}/saglik/revir-ozet")
async def revir_ozet():
    from .core.data_adapter import DataAdapter
    from datetime import date
    adapter = DataAdapter()
    ziyaretler = adapter.load("saglik/revir_ziyaretleri.json") or []
    today = date.today().isoformat()
    bugun = [z for z in ziyaretler if z.get("tarih","").startswith(today)]
    from collections import Counter
    neden_dag = Counter(z.get("neden","?") for z in ziyaretler)
    return {
        "toplam": len(ziyaretler),
        "bugun": len(bugun),
        "supheli": sum(1 for z in ziyaretler if z.get("supheli_yaralanma")),
        "neden_dagilimi": dict(neden_dag.most_common(10)),
        "son_ziyaretler": [
            {"tarih": z.get("tarih"), "ogrenci": z.get("student_name"),
             "neden": z.get("neden"), "islem": z.get("islem",""),
             "supheli": z.get("supheli_yaralanma", False)}
            for z in sorted(ziyaretler, key=lambda x: x.get("tarih",""), reverse=True)[:20]
        ],
    }


# ── Kutuphane ──
@app.get(f"{settings.API_PREFIX}/kutuphane/ozet")
async def kutuphane_ozet():
    from .core.data_adapter import DataAdapter
    adapter = DataAdapter()
    # Kutuphane verileri tenant bazli olabilir
    odunc = adapter.load("kutuphane/odunc_kayitlari.json") or []
    kitaplar = adapter.load("kutuphane/kitaplar.json") or []
    geciken = [o for o in odunc if o.get("durum") == "gecikti"]
    return {
        "toplam_kitap": len(kitaplar),
        "aktif_odunc": sum(1 for o in odunc if o.get("durum") in ("odunc","gecikti")),
        "geciken": len(geciken),
        "son_odunc": [
            {"kitap": o.get("kitap_adi",""), "ogrenci": o.get("ogrenci_adi",""),
             "tarih": o.get("odunc_tarihi",""), "iade": o.get("iade_tarihi",""),
             "durum": o.get("durum","")}
            for o in sorted(odunc, key=lambda x: x.get("odunc_tarihi",""), reverse=True)[:15]
        ],
    }


# ── Sosyal Etkinlik ──
@app.get(f"{settings.API_PREFIX}/sosyal/ozet")
async def sosyal_ozet():
    from .core.data_adapter import DataAdapter
    adapter = DataAdapter()
    kulupler = adapter.load("sosyal_etkinlik/kulupler.json") or []
    etkinlikler = adapter.load("sosyal_etkinlik/etkinlikler.json") or []
    from datetime import date
    today = date.today().isoformat()
    yaklasan = [e for e in etkinlikler if e.get("tarih_baslangic","") >= today]
    return {
        "toplam_kulup": len(kulupler),
        "toplam_etkinlik": len(etkinlikler),
        "yaklasan": len(yaklasan),
        "kulupler": [
            {"ad": k.get("ad"), "kademe": k.get("kademe",""),
             "gun": k.get("faaliyet_gunu",""), "durum": k.get("durum",""),
             "uye": len(k.get("ogrenciler",[]))}
            for k in kulupler
        ],
        "yaklasan_etkinlikler": [
            {"baslik": e.get("baslik"), "tarih": e.get("tarih_baslangic"),
             "kategori": e.get("kategori",""), "konum": e.get("lokasyon",""),
             "durum": e.get("durum","")}
            for e in sorted(yaklasan, key=lambda x: x.get("tarih_baslangic",""))[:10]
        ],
    }


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
