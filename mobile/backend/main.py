"""SmartCampusAI Mobile Backend — FastAPI ana uygulama."""
from __future__ import annotations

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Proje kokunu PYTHONPATH'e ekle (Streamlit kodlarini import edebilmek icin)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.data_adapter import DataAdapter, DataPaths
from .core.deps import get_current_user, get_data_adapter
from .routers import auth, mood, ogrenci, messaging, ihbar, smarti, veli, ogretmen, rehber, yonetici, quiz_koleksiyon, bildirim, odeme


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
@app.get(settings.API_PREFIX + "/bilgi-yarismasi/{level}")
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


# ── Gunun Bilgisi ──
@app.get(f"{settings.API_PREFIX}/gunun-bilgisi")
async def gunun_bilgisi():
    import sys
    sys.path.insert(0, str(settings.DATA_DIR.parent))
    try:
        from models.gunun_bilgisi_kitap import get_gunun_bilgisi, get_gecmis_bilgiler, KATEGORILER
        from datetime import date
        bugun = get_gunun_bilgisi(date.today()) or {}
        gecmis = get_gecmis_bilgiler()
        return {
            "bugun": bugun,
            "kategoriler": list(KATEGORILER.keys()),
            "gecmis": [
                {"tarih": t.isoformat(), **b}
                for t, b in gecmis[:30]
            ],
        }
    except Exception as e:
        return {"bugun": {}, "kategoriler": [], "gecmis": [], "hata": str(e)}


# ── E-Dergi ──
@app.get(f"{settings.API_PREFIX}/e-dergi")
async def e_dergi():
    from pathlib import Path
    dergi_dir = settings.DATA_DIR.parent / "data" / "dergi_gorseller"
    if not dergi_dir.exists():
        dergi_dir = settings.DATA_DIR.parent / "dergi_gorseller"
    dergiler = []
    if dergi_dir.exists():
        for f in sorted(dergi_dir.glob("*.pdf")):
            sayi = f.stem.replace("SmartCampus_eDergi_Sayi", "").replace("SmartCampus_eDergi_", "")
            dergiler.append({"sayi": sayi, "dosya": f.name, "boyut_mb": round(f.stat().st_size / 1024 / 1024, 1)})
    return {"toplam": len(dergiler), "dergiler": dergiler}


# ── Zeka Oyunlari ──
@app.get(f"{settings.API_PREFIX}/zeka-oyunlari")
async def zeka_oyunlari():
    """Mobilde calisacak zeka oyunlari listesi."""
    oyunlar = [
        {"id": "hafiza", "ikon": "🧠", "ad": "Hafıza Oyunu",
         "aciklama": "Eşleşen kartları bul", "seviye": ["Kolay", "Orta", "Zor"]},
        {"id": "sudoku", "ikon": "🔢", "ad": "Sudoku Mini",
         "aciklama": "4×4 mini sudoku", "seviye": ["4x4"]},
        {"id": "bilmece", "ikon": "❓", "ad": "Bilmeceler",
         "aciklama": "Düşün ve bul", "seviye": ["İlkokul", "Ortaokul"]},
        {"id": "kelime", "ikon": "📝", "ad": "Kelime Bulmaca",
         "aciklama": "Gizli kelimeyi bul", "seviye": ["Kolay", "Zor"]},
        {"id": "stroop", "ikon": "🎨", "ad": "Stroop Testi",
         "aciklama": "Rengi söyle, kelimeyi değil", "seviye": ["Normal"]},
        {"id": "siralama", "ikon": "📊", "ad": "Sayı Sıralama",
         "aciklama": "Sayıları küçükten büyüğe sırala", "seviye": ["Kolay", "Zor"]},
    ]
    return {"oyunlar": oyunlar}


# ── KDG Premium (CEFR Ingilizce + Almanca) ──
@app.get(settings.API_PREFIX + "/kdg/{dil}")
async def kdg_dersler(dil: str = "ingilizce"):
    """KDG Premium — CEFR seviyeli kelime + gramer."""
    import json
    from pathlib import Path
    lang_dir = {"ingilizce": "english", "almanca": "german"}.get(dil, "english")
    base = settings.DATA_DIR / lang_dir

    # Kelimeler
    words_data = {}
    wp = base / "cefr_words.json"
    if not wp.exists():
        wp = Path(__file__).resolve().parent.parent.parent / "data" / lang_dir / "cefr_words.json"
    if wp.exists():
        with open(wp, "r", encoding="utf-8") as f:
            words_data = json.load(f)

    # Gramer
    grammar_data = {}
    gp = base / "cefr_grammar.json"
    if not gp.exists():
        gp = Path(__file__).resolve().parent.parent.parent / "data" / lang_dir / "cefr_grammar.json"
    if gp.exists():
        with open(gp, "r", encoding="utf-8") as f:
            grammar_data = json.load(f)

    seviyeler = []
    for level in ["A1", "A2", "B1", "B2", "C1"]:
        w = words_data.get(level, {})
        g = grammar_data.get(level, [])
        cats = w.get("categories", {})
        toplam_kelime = sum(len(v) if isinstance(v, list) else 0 for v in cats.values())
        seviyeler.append({
            "seviye": level,
            "aciklama": w.get("description", ""),
            "hedef": w.get("target", 0),
            "kategori_sayisi": len(cats),
            "kelime_sayisi": toplam_kelime,
            "gramer_sayisi": len(g) if isinstance(g, list) else 0,
        })

    return {"dil": dil, "seviyeler": seviyeler, "diller": ["ingilizce", "almanca"]}


@app.get(settings.API_PREFIX + "/kdg/{dil}/{seviye}")
async def kdg_seviye_detay(dil: str, seviye: str):
    """KDG seviye detay — kategoriler + kelimeler + gramer."""
    import json
    from pathlib import Path
    lang_dir = {"ingilizce": "english", "almanca": "german"}.get(dil, "english")

    words_data = {}
    for p in [settings.DATA_DIR / lang_dir / "cefr_words.json",
              Path(__file__).resolve().parent.parent.parent / "data" / lang_dir / "cefr_words.json"]:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f: words_data = json.load(f)
            break

    grammar_data = {}
    for p in [settings.DATA_DIR / lang_dir / "cefr_grammar.json",
              Path(__file__).resolve().parent.parent.parent / "data" / lang_dir / "cefr_grammar.json"]:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f: grammar_data = json.load(f)
            break

    level_words = words_data.get(seviye.upper(), {})
    level_grammar = grammar_data.get(seviye.upper(), [])

    # Kategorileri normalize et
    cats = level_words.get("categories", {})
    kategoriler = []
    for kat_ad, kelimeler in cats.items():
        if isinstance(kelimeler, list):
            kategoriler.append({
                "kategori": kat_ad,
                "kelimeler": [
                    {"word": w.get("e", w.get("de", "")),
                     "tr": w.get("t", ""),
                     "pron": w.get("p", "")}
                    for w in kelimeler if isinstance(w, dict)
                ],
            })

    return {
        "dil": dil,
        "seviye": seviye.upper(),
        "aciklama": level_words.get("description", ""),
        "kategoriler": kategoriler,
        "gramer": level_grammar if isinstance(level_grammar, list) else [],
    }


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
app.include_router(quiz_koleksiyon.router, prefix=settings.API_PREFIX)
app.include_router(bildirim.router, prefix=settings.API_PREFIX)
app.include_router(odeme.router, prefix=settings.API_PREFIX)


# ══════════════════════════════════════════════════════════════
# GÜNLÜK İŞLER — bugünkü devamsız/geç/izinli öğrenciler
# ══════════════════════════════════════════════════════════════

@app.get(settings.API_PREFIX + "/gunluk-isler")
async def gunluk_isler(
    user: dict = Depends(get_current_user),
    adapter: DataAdapter = Depends(get_data_adapter),
):
    """Bugünkü yoklama sonuçları — devamsız, geç, izinli öğrenciler."""
    from datetime import date as _date, timedelta

    bugun = _date.today().isoformat()
    attendance = adapter.load(DataPaths.ATTENDANCE) or []
    students = adapter.load(DataPaths.STUDENTS) or []
    all_users = adapter.load("users.json") or []

    stu_map = {s.get("id"): s for s in students}
    role = user.get("role", "").lower()

    # Bugünkü kayıtlar
    bugun_kayitlar = [a for a in attendance if a.get("tarih") == bugun]

    # Kategorize et
    devamsiz = {}
    gec_list = []
    izinli_list = []

    for a in bugun_kayitlar:
        sid = a.get("student_id", "")
        turu = a.get("turu", "")
        stu = stu_map.get(sid, {})
        if not stu:
            continue

        info = {
            "student_id": sid,
            "ad_soyad": f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip(),
            "sinif": str(stu.get("sinif", "")),
            "sube": stu.get("sube", ""),
            "numara": stu.get("numara", ""),
            "ders": a.get("ders", ""),
            "ders_saati": a.get("ders_saati", 0),
        }

        if turu in ("devamsiz", "ozursuz"):
            if sid not in devamsiz:
                devamsiz[sid] = {
                    "student_id": sid,
                    "ad_soyad": info["ad_soyad"],
                    "sinif": info["sinif"],
                    "sube": info["sube"],
                    "numara": info["numara"],
                    "veli_adi": f"{stu.get('veli_adi', '')} {stu.get('veli_soyadi', '')}".strip(),
                    "veli_telefon": stu.get("veli_telefon", ""),
                    "dersler": [],
                }
            devamsiz[sid]["dersler"].append(f"{info['ders']} ({info['ders_saati']}. ders)")
        elif turu == "gec":
            gec_list.append(info)
        elif turu in ("izinli", "raporlu"):
            izinli_list.append(info)

    # Rol bazlı filtreleme
    if role == "veli":
        ogrenci_id = user.get("ogrenci_id", "")
        children = user.get("children_ids", [])
        if ogrenci_id:
            children = list(set(children + [ogrenci_id]))
        devamsiz = {k: v for k, v in devamsiz.items() if k in children}
        gec_list = [g for g in gec_list if g["student_id"] in children]
        izinli_list = [i for i in izinli_list if i["student_id"] in children]
    elif role == "ogrenci":
        own_id = user.get("student_id", user.get("source_id", ""))
        own_stu = stu_map.get(own_id, {})
        own_sinif = str(own_stu.get("sinif", ""))
        own_sube = own_stu.get("sube", "")
        sinif_ids = {s.get("id") for s in students
                     if str(s.get("sinif", "")) == own_sinif
                     and s.get("sube", "") == own_sube}
        devamsiz = {k: v for k, v in devamsiz.items() if k in sinif_ids}
        gec_list = [g for g in gec_list if g["student_id"] in sinif_ids]
        izinli_list = [i for i in izinli_list if i["student_id"] in sinif_ids]

    # ── Öğretmen ek bilgileri ──
    ogretmen_ek = {}
    if role in ("ogretmen", "superadmin", "yonetici", "mudur"):
        from datetime import date as _d2
        bugun_str = _d2.today().strftime("%A").lower()
        gun_map = {"monday": "Pazartesi", "tuesday": "Salı", "wednesday": "Çarşamba",
                   "thursday": "Perşembe", "friday": "Cuma", "saturday": "Cumartesi", "sunday": "Pazar"}
        bugun_gun = gun_map.get(bugun_str, bugun_str)

        # Ders programı (bugün, sadece bu öğretmenin dersleri)
        schedule = adapter.load("akademik/schedule.json") or []
        ogretmen_adi = user.get("ad_soyad", user.get("name", ""))
        bugun_dersler = [s for s in schedule
                         if s.get("gun", "").lower() == bugun_gun.lower()
                         and ogretmen_adi.lower() in (s.get("ogretmen_adi", s.get("ogretmen", "")) or "").lower()]
        def _saat_key(s):
            v = s.get("saat", 0)
            if isinstance(v, int):
                return v
            try:
                return int(str(v).split(":")[0].split("-")[0])
            except (ValueError, IndexError):
                return 0
        bugun_dersler.sort(key=_saat_key)

        # Bekleyen not girişi (son 30 gün sınavlar - notu girilmemiş)
        grades = adapter.load(DataPaths.GRADES) or []
        homework = adapter.load(DataPaths.HOMEWORK) or []

        # Teslim edilen ödevler (bugün)
        submissions = adapter.load(DataPaths.HOMEWORK_SUBMISSIONS) or []
        bugun_teslim = [s for s in submissions if s.get("teslim_tarihi", "")[:10] == bugun]

        # Nöbet (bugün)
        nobet_data = adapter.load("akademik/nobet_gorevler.json") or []
        ogretmen_adi = user.get("ad_soyad", user.get("name", ""))
        bugun_nobet = any(
            n for n in nobet_data
            if bugun_gun.lower() in (n.get("gun", "").lower(), "")
            and ogretmen_adi.lower() in (n.get("ogretmen_adi", n.get("ogretmen", "")) or "").lower()
        )

        # Okunmamış mesajlar
        mesajlar = adapter.load("akademik/veli_mesajlar.json") or []
        user_id = user.get("user_id", "")
        okunmamis = sum(1 for m in mesajlar
                        if m.get("ogretmen_id") == user_id
                        and not m.get("okundu", False)
                        and "veli" in m.get("yon", ""))

        # Doğum günü olan öğrenciler
        bugun_ay_gun = _d2.today().strftime("-%m-%d")
        dogum_gunu = [
            f"{s.get('ad', '')} {s.get('soyad', '')} ({s.get('sinif', '')}/{s.get('sube', '')})"
            for s in students
            if (s.get("dogum_tarihi", "") or "").endswith(bugun_ay_gun)
        ]

        # Ders defteri eksik (son 3 gün)
        ders_defteri = adapter.load("akademik/ders_defteri.json") or []
        son3gun = [(_d2.today() - timedelta(days=i)).isoformat() for i in range(3)]
        dd_girilmis = {(d.get("tarih", "")[:10], d.get("sinif"), d.get("sube"), d.get("ders"))
                       for d in ders_defteri if d.get("tarih", "")[:10] in son3gun}

        ogretmen_ek = {
            "bugun_ders_programi": bugun_dersler[:10],
            "bugun_gun": bugun_gun,
            "teslim_edilen_odev": len(bugun_teslim),
            "nobet_var": bugun_nobet,
            "okunmamis_mesaj": okunmamis,
            "dogum_gunu": dogum_gunu[:5],
            "ders_defteri_eksik": max(0, len(bugun_dersler) - len(dd_girilmis)),
        }

    return {
        "tarih": bugun,
        "yoklama_alinan": len(set(a.get("student_id") for a in bugun_kayitlar)),
        "devamsiz": list(devamsiz.values()),
        "devamsiz_sayisi": len(devamsiz),
        "gec": gec_list,
        "gec_sayisi": len(gec_list),
        "izinli": izinli_list,
        "izinli_sayisi": len(izinli_list),
        **ogretmen_ek,
    }


# ══════════════════════════════════════════════════════════════
# QR KOD HANDLER — Kitap-Yazılım entegrasyonu
# ══════════════════════════════════════════════════════════════

@app.get(settings.API_PREFIX + "/qr-handler")
async def qr_handler(
    sinif: int,
    ders: str,
    unite: str = "",
    konu: str = "",
    user: dict = Depends(get_current_user),
    adapter: DataAdapter = Depends(get_data_adapter),
):
    """Kitaptaki QR kod tarandığında ilgili içeriği döndürür."""
    role = user.get("role", "").lower()
    plans = adapter.load("olcme/annual_plans.json") or []

    # Kazanım eşleştirme
    kazanimlar = [p for p in plans if p.get("grade") == sinif and p.get("subject") == ders]
    if unite:
        kazanimlar = [p for p in kazanimlar if unite.lower() in p.get("unit", "").lower()]
    if konu:
        kazanimlar = [p for p in kazanimlar if konu.lower() in p.get("topic", "").lower()]

    toplam_kazanim = sum(len(k.get("learning_outcomes", [])) for k in kazanimlar[:20])

    # Soru bankasından eşleşen soru sayısı
    sorular = adapter.load("olcme/questions.json") or []
    soru_sayisi = sum(1 for q in sorular
                      if q.get("sinif") == sinif
                      and ders.lower() in (q.get("ders", "") or "").lower())

    # Rol bazlı yönlendirme önerileri
    yonlendirmeler = []
    if role == "ogrenci":
        yonlendirmeler = [
            {"baslik": "Quiz Çöz", "route": "/bilgi-yarismasi-koleksiyon", "ikon": "quiz"},
            {"baslik": "Konu Tekrarı", "route": "/notes", "ikon": "book"},
            {"baslik": "Matematik Köyü", "route": "/matematik-koyu", "ikon": "calculate"},
            {"baslik": "AI Treni", "route": "/ai-treni", "ikon": "train"},
            {"baslik": "Smarti'ye Sor", "route": "/smarti", "ikon": "smart_toy"},
        ]
    elif role == "veli":
        yonlendirmeler = [
            {"baslik": "Çocuk Performansı", "route": "/veli/cocuk-detay", "ikon": "analytics"},
            {"baslik": "Karne Görüntüle", "route": "/veli/cocuk-detay", "ikon": "school"},
            {"baslik": "Öğretmene Mesaj", "route": "/messages", "ikon": "chat"},
        ]
    elif role in ("ogretmen", "yonetici"):
        yonlendirmeler = [
            {"baslik": "Sınav Oluştur", "route": "/ogretmen/sinav-sonuclari", "ikon": "quiz"},
            {"baslik": "Ders Defteri", "route": "/ogretmen/ders-defteri", "ikon": "book"},
            {"baslik": "Yoklama Al", "route": "/ogretmen/yoklama", "ikon": "how_to_reg"},
            {"baslik": "Sınıf Analizi", "route": "/yonetici/erken-uyari", "ikon": "analytics"},
        ]

    # Telafi önerisi
    telafi = None
    if role == "ogrenci":
        student_id = user.get("student_id", user.get("source_id", ""))
        if student_id:
            grades = adapter.load(DataPaths.GRADES) or []
            ders_notlari = [g for g in grades
                            if g.get("student_id") == student_id
                            and ders.lower() in (g.get("ders", "") or "").lower()]
            if ders_notlari:
                avg = sum(float(g.get("puan", 0) or 0) for g in ders_notlari) / len(ders_notlari)
                if avg < 50:
                    telafi = {
                        "seviye": "kritik",
                        "ortalama": round(avg, 1),
                        "oneri": f"Bu konuyu kitaptan tekrar oku ve quiz çöz.",
                    }
                elif avg < 70:
                    telafi = {
                        "seviye": "dikkat",
                        "ortalama": round(avg, 1),
                        "oneri": f"Konuyu pekiştirmek için etkinlikleri yap.",
                    }

    return {
        "sinif": sinif,
        "ders": ders,
        "unite": unite,
        "konu": konu,
        "kazanim_sayisi": toplam_kazanim,
        "soru_sayisi": soru_sayisi,
        "role": role,
        "yonlendirmeler": yonlendirmeler,
        "telafi": telafi,
        "kazanimlar": [
            {"topic": k.get("topic", ""), "outcomes": k.get("learning_outcomes", [])[:3]}
            for k in kazanimlar[:10]
        ],
    }


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
