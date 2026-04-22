"""
UZY-01 Uzay Kesfet - 3D Ultra Premium Egitim Modulu
====================================================
30 konu ile cocuk dostu, interaktif uzay egitim modulu.
"""

from __future__ import annotations
import streamlit as st
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome


# ============================================================
# KATEGORI TANIMLARI
# ============================================================

_KATEGORILER = [
    {"id": "gunes_sistemi",  "baslik": "Gunes Sistemi",          "emoji": "🌌", "renk1": "#FF6B35", "renk2": "#D4540E", "ikon": "☀️",  "aciklama": "Gunes ve 8 gezegen ile tanis!"},
    {"id": "ay_dunya",       "baslik": "Ay ve Dunya Hareketleri", "emoji": "🌍", "renk1": "#4A90D9", "renk2": "#2563EB", "ikon": "🌙",  "aciklama": "Dunya ve Ay nasil hareket eder?"},
    {"id": "dunya_yapisi",   "baslik": "Dunyanin Yapisi",         "emoji": "🌏", "renk1": "#10B981", "renk2": "#059669", "ikon": "🏔️", "aciklama": "Gezegenimizin ic ve dis yapisi"},
    {"id": "uzay_kesfi",     "baslik": "Uzay Kesfi",              "emoji": "🚀", "renk1": "#8B5CF6", "renk2": "#6D28D9", "ikon": "🛸",  "aciklama": "Insanligin uzay macerasi"},
    {"id": "uzay_cisimleri", "baslik": "Uzay Cisimleri",          "emoji": "☄️", "renk1": "#06B6D4", "renk2": "#0891B2", "ikon": "⭐",  "aciklama": "Kozmik cisimler ve yildiz olusimlari"},
]

_KAT_MAP = {k["id"]: k for k in _KATEGORILER}


# ============================================================
# 30 UZAY KONUSU
# ============================================================

_KONULAR = [
    {"id": 1,  "baslik": "Gunes",    "emoji": "☀️",  "kat": "gunes_sistemi", "renk": "#FF9500",
     "aciklama": "Gunes Sistemimizin kalbi! Tum gezegenler onun etrafinda doner.",
     "bilgi": "Gunes o kadar buyuk ki, icine 1.3 milyon tane Dunya sigar!"},
    {"id": 2,  "baslik": "Merkur",   "emoji": "🪨",  "kat": "gunes_sistemi", "renk": "#A0887E",
     "aciklama": "Gunese en yakin ve en kucuk gezegen.",
     "bilgi": "Merkurde bir gun (176 Dunya gunu) bir yilindan (88 gun) daha uzun surer!"},
    {"id": 3,  "baslik": "Venus",    "emoji": "🌟",  "kat": "gunes_sistemi", "renk": "#E8A87C",
     "aciklama": "En parlak gezegen! Kalin atmosferi onu en sicak yapar.",
     "bilgi": "Venus ters yonde doner, orada Gunes batidan dogar!"},
    {"id": 4,  "baslik": "Dunya",    "emoji": "🌍",  "kat": "gunes_sistemi", "renk": "#3B82F6",
     "aciklama": "Mavi Gezegen! Bilinen tek yasanabilir gezegen.",
     "bilgi": "Dunyanin yuzde 71i suyla kaplidir, uzaydan bakinca mavi gorunur!"},
    {"id": 5,  "baslik": "Mars",     "emoji": "🔴",  "kat": "gunes_sistemi", "renk": "#DC2626",
     "aciklama": "Kizil Gezegen! Demir oksit ona kirmizi rengini verir.",
     "bilgi": "Marstaki Olympus Mons, Everestten 3 kat yuksek!"},
    {"id": 6,  "baslik": "Jupiter",  "emoji": "🟠",  "kat": "gunes_sistemi", "renk": "#EA580C",
     "aciklama": "En buyuk gezegen! Buyuk Kirmizi Leke dev bir firtinadir.",
     "bilgi": "Jupiterin Buyuk Kirmizi Lekesi 300 yildir devam eden bir firtinadir!"},
    {"id": 7,  "baslik": "Saturn",   "emoji": "💍",  "kat": "gunes_sistemi", "renk": "#D4A017",
     "aciklama": "Muhtesem halkalariyla unlu! Halkalar buz ve kayadan olusur.",
     "bilgi": "Saturn o kadar hafif ki, dev bir okyanus olsa yuzerdi!"},
    {"id": 8,  "baslik": "Uranus",   "emoji": "🔵",  "kat": "gunes_sistemi", "renk": "#67E8F9",
     "aciklama": "Yan yatik donen buz devi! Ekseni neredeyse yatay.",
     "bilgi": "Uranus -224 derece ile en soguk gezegendir!"},
    {"id": 9,  "baslik": "Neptun",   "emoji": "🌊",  "kat": "gunes_sistemi", "renk": "#1D4ED8",
     "aciklama": "En uzak gezegen! Supersonik ruzgarlariyla bilinir.",
     "bilgi": "Neptundeki ruzgarlar saatte 2.100 km hiza ulasir!"},

    {"id": 10, "baslik": "Ay",                        "emoji": "🌙",  "kat": "ay_dunya", "renk": "#CBD5E1",
     "aciklama": "Dunyanin tek dogal uydusu. En yakin gok cismi.",
     "bilgi": "Ay her yil Dunyadan 3.8 cm uzaklasiyor!"},
    {"id": 11, "baslik": "Ayin Evreleri",              "emoji": "🌘",  "kat": "ay_dunya", "renk": "#94A3B8",
     "aciklama": "Yeniay, Ilk Dordun, Dolunay, Son Dordun.",
     "bilgi": "Ay evreleri tam olarak 29.5 gunde tamamlanir!"},
    {"id": 12, "baslik": "Dunyanin Eksen Donusu",      "emoji": "🔄",  "kat": "ay_dunya", "renk": "#60A5FA",
     "aciklama": "Dunya 24 saatte kendi ekseni etrafinda bir tur atar.",
     "bilgi": "Ekvatorda donus hizi saatte 1.670 km!"},
    {"id": 13, "baslik": "Gunes Etrafinda Dolanma",     "emoji": "🌐",  "kat": "ay_dunya", "renk": "#3B82F6",
     "aciklama": "Dunya Gunesin etrafinda 365 gun 6 saatte doner.",
     "bilgi": "Dunya Gunesin etrafinda saatte 107.000 km hizla ilerler!"},
    {"id": 14, "baslik": "Gece ve Gunduz",              "emoji": "🌓",  "kat": "ay_dunya", "renk": "#7C3AED",
     "aciklama": "Dunyanin donmesiyle Gunese bakan yuz gunduz olur.",
     "bilgi": "Kutuplarda yaz aylarinda Gunes hic batmaz!"},
    {"id": 15, "baslik": "Mevsimlerin Olusumu",         "emoji": "🍂",  "kat": "ay_dunya", "renk": "#F59E0B",
     "aciklama": "Dunyanin ekseninin 23.5 derece egik olmasi mevsimleri yaratir.",
     "bilgi": "Kuzeyde yaz iken guneyde kis yasanir!"},

    {"id": 16, "baslik": "Dunya Katmanlari",           "emoji": "🧅",  "kat": "dunya_yapisi", "renk": "#EF4444",
     "aciklama": "Kabuk, Manto ve Cekirdek olmak uzere uc katman.",
     "bilgi": "Dunyanin ic cekirdegi Gunesin yuzeyi kadar sicaktir, 5.500 derece!"},
    {"id": 17, "baslik": "Atmosfer",                    "emoji": "💨",  "kat": "dunya_yapisi", "renk": "#38BDF8",
     "aciklama": "Dunyayi saran koruyucu gaz tabakasi.",
     "bilgi": "Atmosfer olmasaydi gunduz 120, gece -170 derece olurdu!"},
    {"id": 18, "baslik": "Okyanuslar",                  "emoji": "🌊",  "kat": "dunya_yapisi", "renk": "#0284C7",
     "aciklama": "Dunyanin yuzde 71ini kaplayan dev su kutleleri.",
     "bilgi": "Okyanuslarin en derin noktasi 11.034 metre!"},
    {"id": 19, "baslik": "Kitalar",                     "emoji": "🗺️", "kat": "dunya_yapisi", "renk": "#16A34A",
     "aciklama": "Dunyadaki 7 buyuk kara parcasi.",
     "bilgi": "250 milyon yil once tum kitalar tek bir kitaydi: Pangea!"},
    {"id": 20, "baslik": "Daglar",                      "emoji": "⛰️", "kat": "dunya_yapisi", "renk": "#78716C",
     "aciklama": "Tektonik plakalarin carpismasiyla olusan yapilar.",
     "bilgi": "Everest Dagi her yil yaklasik 4 mm yukselmeye devam ediyor!"},
    {"id": 21, "baslik": "Volkanlar",                   "emoji": "🌋",  "kat": "dunya_yapisi", "renk": "#DC2626",
     "aciklama": "Yeraltindaki magmanin yeryuzune ciktigi yapilar.",
     "bilgi": "Dunyada 1.500den fazla aktif yanardag vardir!"},

    {"id": 22, "baslik": "Uydular (Yapay Uydu)",        "emoji": "📡",  "kat": "uzay_kesfi", "renk": "#A78BFA",
     "aciklama": "Insanlar tarafindan uzaya gonderilen araclar.",
     "bilgi": "Dunya yorungesinde 7.000den fazla aktif yapay uydu vardir!"},
    {"id": 23, "baslik": "Uzay Istasyonu",              "emoji": "🛸",  "kat": "uzay_kesfi", "renk": "#A5B4FC",
     "aciklama": "Uzayda yorungede donen dev laboratuvar.",
     "bilgi": "ISS saatte 27.600 km hizla Dunyanin etrafini 90 dakikada dolanir!"},
    {"id": 24, "baslik": "Roket",                       "emoji": "🚀",  "kat": "uzay_kesfi", "renk": "#C084FC",
     "aciklama": "Uzaya cikmak icin kullanilan guclu araclar.",
     "bilgi": "Bir roketin uzaya cikabilmesi icin saatte en az 28.000 km hiz gerekir!"},
    {"id": 25, "baslik": "Uzay Mekigi",                 "emoji": "🛩️", "kat": "uzay_kesfi", "renk": "#7C3AED",
     "aciklama": "Tekrar kullanilabilen uzay araclari.",
     "bilgi": "Uzay mekigi atmosfere girisde 1.650 dereceye dayanmak zorundadir!"},
    {"id": 26, "baslik": "Astronot",                    "emoji": "👨‍🚀", "kat": "uzay_kesfi", "renk": "#6D28D9",
     "aciklama": "Uzaya giden cesur kasifler!",
     "bilgi": "Uzayda yercekimi olmadigindan astronotlarin boyu 5 cm uzar!"},

    {"id": 27, "baslik": "Asteroit",                    "emoji": "🪨",  "kat": "uzay_cisimleri", "renk": "#F97316",
     "aciklama": "Gunes etrafinda donen kaya ve metal parcalari.",
     "bilgi": "Asteroit kusaginda milyonlarca asteroit bulunur!"},
    {"id": 28, "baslik": "Kuyruklu Yildiz",             "emoji": "☄️",  "kat": "uzay_cisimleri", "renk": "#22D3EE",
     "aciklama": "Gunese yaklastikca isinan buz ve toz toplari.",
     "bilgi": "Kuyruklu yildizlarin kuyrugu milyonlarca km uzunluga ulasabilir!"},
    {"id": 29, "baslik": "Goktasi / Meteorit",          "emoji": "💫",  "kat": "uzay_cisimleri", "renk": "#14B8A6",
     "aciklama": "Uzaydan Dunyaya dusen kaya parcalari.",
     "bilgi": "Her gun Dunyaya yaklasik 100 ton uzay tozu duser!"},
    {"id": 30, "baslik": "Takimyildizlar",              "emoji": "⭐",  "kat": "uzay_cisimleri", "renk": "#FBBF24",
     "aciklama": "Gokyuzundeki yildizlarin olusturdugu hayali sekiller.",
     "bilgi": "Uluslararasi 88 takimyildiz resmi olarak taninmaktadir!"},
]


# ============================================================
# CSS — 3 parca halinde enjekte (Streamlit uyumlu)
# ============================================================

def _inject_css_core():
    """Temel layout + hero + grid CSS."""
    st.markdown("""<style>
    .uzay-hero {
        background: linear-gradient(160deg, #020014 0%, #0a0628 20%, #0d1137 45%, #1a0a2e 70%, #0b0020 100%);
        border-radius: 24px; padding: 44px 38px 36px; margin-bottom: 26px;
        position: relative; overflow: hidden;
        border: 1px solid rgba(139,92,246,0.15);
        box-shadow: 0 0 60px rgba(99,102,241,0.15), 0 20px 60px rgba(0,0,0,0.5);
    }
    .uzay-hero-stars {
        position: absolute; inset: 0;
        background-image:
            radial-gradient(1.5px 1.5px at 10% 20%, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 25% 65%, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 40% 10%, rgba(255,255,255,0.9), transparent),
            radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.5), transparent),
            radial-gradient(1.5px 1.5px at 70% 30%, rgba(200,220,255,0.9), transparent),
            radial-gradient(1px 1px at 85% 55%, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 15% 90%, rgba(200,200,255,0.7), transparent),
            radial-gradient(1.5px 1.5px at 60% 45%, rgba(255,240,200,0.8), transparent),
            radial-gradient(1px 1px at 92% 75%, rgba(255,255,255,0.5), transparent),
            radial-gradient(2px 2px at 35% 40%, rgba(255,255,255,0.7), transparent);
        animation: uzStar 4s ease-in-out infinite alternate;
    }
    .uzay-hero-nebula {
        position: absolute; inset: 0;
        background:
            radial-gradient(ellipse 300px 200px at 15% 60%, rgba(139,92,246,0.12), transparent),
            radial-gradient(ellipse 250px 180px at 75% 30%, rgba(59,130,246,0.10), transparent);
    }
    .uzay-hero-ring {
        position: absolute; top: -60px; right: -60px;
        width: 200px; height: 200px;
        border: 1.5px solid rgba(139,92,246,0.12);
        border-radius: 50%;
        animation: uzSpin 30s linear infinite;
    }
    .uzay-hero-content { position: relative; z-index: 5; }
    .uzay-hero-badge {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.25);
        border-radius: 20px; padding: 4px 14px;
        font-size: 0.65rem; font-weight: 700; color: rgba(200,180,255,0.9);
        text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 14px;
    }
    .uzay-hero-badge-dot {
        width: 6px; height: 6px; background: #8B5CF6; border-radius: 50%;
        animation: uzPulse 2s ease-in-out infinite;
        box-shadow: 0 0 6px rgba(139,92,246,0.8);
    }
    .uzay-hero-title {
        font-size: 2.1rem; font-weight: 900; color: #fff;
        text-shadow: 0 0 30px rgba(139,92,246,0.4), 0 2px 4px rgba(0,0,0,0.3);
    }
    .uzay-hero-sub {
        font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-top: 6px;
        letter-spacing: 0.3px; line-height: 1.5;
    }
    .uzay-hero-planets {
        position: absolute; top: 20px; right: 36px;
        font-size: 2.6rem; z-index: 5;
        filter: drop-shadow(0 0 20px rgba(255,200,0,0.3));
        animation: uzFloat 6s ease-in-out infinite;
    }
    .uzay-hero-stats {
        display: flex; gap: 14px; margin-top: 24px; flex-wrap: wrap;
    }
    .uzay-hero-stat {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 12px 22px; text-align: center;
        transition: all .3s ease;
    }
    .uzay-hero-stat:hover {
        background: rgba(255,255,255,0.08);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139,92,246,0.15);
    }
    .uzay-hero-stat-val { font-size: 1.5rem; font-weight: 900; color: #fff; }
    .uzay-hero-stat-lbl {
        font-size: 0.6rem; color: rgba(255,255,255,0.45);
        text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;
    }
    .uzay-kat-header {
        display: flex; align-items: center; gap: 16px;
        padding: 18px 28px; border-radius: 16px; margin-bottom: 20px;
        position: relative; overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.1);
    }
    .uzay-kat-emoji { font-size: 2rem; }
    .uzay-kat-title { font-size: 1.15rem; font-weight: 800; color: #fff; }
    .uzay-kat-desc { font-size: 0.78rem; color: rgba(255,255,255,0.7); margin-top: 2px; }
    .uzay-kat-count {
        margin-left: auto; background: rgba(255,255,255,0.12);
        border-radius: 20px; padding: 4px 14px;
        font-size: 0.7rem; font-weight: 700; color: rgba(255,255,255,0.9);
    }
    .uzay-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 22px; padding: 4px 2px;
    }
    @media (max-width: 900px) { .uzay-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { .uzay-grid { grid-template-columns: 1fr; } }
    </style>""", unsafe_allow_html=True)


def _inject_css_cards():
    """3D flip kart CSS."""
    st.markdown("""<style>
    .uzay-card {
        perspective: 1200px; height: 300px; cursor: pointer;
    }
    .uzay-card-inner {
        position: relative; width: 100%; height: 100%;
        transform-style: preserve-3d;
        transition: transform .8s cubic-bezier(.4,0,.2,1), box-shadow .4s ease;
        border-radius: 20px;
    }
    .uzay-card:hover .uzay-card-inner {
        transform: rotateY(180deg) scale(1.02);
        box-shadow: 0 0 30px var(--cg, rgba(139,92,246,0.4)), 0 20px 50px rgba(0,0,0,0.3);
    }
    .uzay-card-front, .uzay-card-back {
        position: absolute; inset: 0;
        backface-visibility: hidden; -webkit-backface-visibility: hidden;
        border-radius: 20px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; padding: 26px 18px;
        overflow: hidden;
    }
    .uzay-card-front {
        background: linear-gradient(160deg, var(--c1, #8B5CF6), var(--c2, #6D28D9));
        box-shadow: 0 4px 20px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.15);
    }
    .uzay-card-front::before {
        content: ''; position: absolute; top: -50px; right: -40px;
        width: 140px; height: 140px; border-radius: 50%;
        background: radial-gradient(circle, rgba(255,255,255,0.1), transparent 70%);
    }
    .uzay-card-num {
        position: absolute; top: 12px; left: 16px;
        font-size: 0.6rem; font-weight: 800; color: rgba(255,255,255,0.3);
        letter-spacing: 1.5px;
    }
    .uzay-card-cat {
        position: absolute; top: 12px; right: 14px;
        background: rgba(255,255,255,0.15); border-radius: 8px; padding: 2px 8px;
        font-size: 0.55rem; font-weight: 700; color: rgba(255,255,255,0.7);
        letter-spacing: 0.5px; text-transform: uppercase;
    }
    .uzay-card-emoji {
        font-size: 3.8rem; margin-bottom: 12px;
        filter: drop-shadow(0 6px 16px rgba(0,0,0,0.3));
        animation: uzFloat 5s ease-in-out infinite;
        animation-delay: var(--fd, 0s);
    }
    .uzay-card-title {
        font-size: 1.02rem; font-weight: 800; color: #fff; text-align: center;
        text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    .uzay-card-desc {
        font-size: 0.72rem; color: rgba(255,255,255,0.85);
        text-align: center; margin-top: 6px; line-height: 1.45;
    }
    .uzay-card-hint {
        position: absolute; bottom: 10px; right: 14px;
        font-size: 0.58rem; color: rgba(255,255,255,0.25);
        letter-spacing: 0.5px;
    }
    .uzay-card-back {
        transform: rotateY(180deg);
        background: linear-gradient(160deg, #080818 0%, #0f0f28 40%, #0a0a1e 100%);
        border: 1.5px solid var(--c1, #8B5CF6);
        box-shadow: inset 0 0 40px rgba(0,0,0,0.4);
    }
    .uzay-card-back::after {
        content: ''; position: absolute; top: 14px; right: 14px;
        width: 8px; height: 8px; background: var(--c1, #8B5CF6);
        border-radius: 50%; box-shadow: 0 0 10px var(--c1, #8B5CF6);
        animation: uzPulse 2s ease-in-out infinite;
    }
    .uzay-card-back-icon { font-size: 1.8rem; margin-bottom: 8px; }
    .uzay-card-back-label {
        font-size: 0.58rem; text-transform: uppercase; letter-spacing: 2px;
        color: var(--c1, #8B5CF6); font-weight: 800; margin-bottom: 8px;
    }
    .uzay-card-back-div {
        width: 40px; height: 2px; border-radius: 1px;
        background: linear-gradient(90deg, transparent, var(--c1, #8B5CF6), transparent);
        margin-bottom: 10px;
    }
    .uzay-card-back-fact {
        font-size: 0.82rem; color: rgba(255,255,255,0.9);
        text-align: center; line-height: 1.6; font-weight: 500;
    }
    .uzay-card-back-ft {
        position: absolute; bottom: 12px;
        font-size: 0.6rem; color: rgba(255,255,255,0.25);
    }
    </style>""", unsafe_allow_html=True)


def _inject_css_extra():
    """Animasyonlar, tab, stat, tablo CSS."""
    st.markdown("""<style>
    @keyframes uzStar {
        0% { opacity: 0.4; } 100% { opacity: 0.85; }
    }
    @keyframes uzFloat {
        0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); }
    }
    @keyframes uzPulse {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.3); }
    }
    @keyframes uzSpin {
        from { transform: rotate(0deg); } to { transform: rotate(360deg); }
    }
    .uzay-stat-grid { display: flex; gap: 14px; flex-wrap: wrap; margin: 18px 0 10px; }
    .uzay-stat-card {
        flex: 1; min-width: 125px;
        background: linear-gradient(160deg, rgba(15,15,40,0.9), rgba(20,20,50,0.9));
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px; padding: 18px 12px; text-align: center;
        transition: all .3s ease; box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .uzay-stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(99,102,241,0.2);
    }
    .uzay-stat-emoji { font-size: 1.8rem; margin-bottom: 6px; }
    .uzay-stat-val { font-size: 1.6rem; font-weight: 900; }
    .uzay-stat-lbl {
        font-size: 0.6rem; color: rgba(255,255,255,0.45);
        text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;
    }
    .uzay-info-banner {
        background: linear-gradient(135deg, rgba(30,27,75,0.8), rgba(49,46,129,0.8));
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 12px; padding: 14px 20px;
        display: flex; align-items: center; gap: 12px;
        margin: 14px 0; color: rgba(255,255,255,0.75); font-size: 0.82rem;
    }
    .uzay-tbl-wrap {
        background: linear-gradient(160deg, #080818, #0f0f28);
        border-radius: 14px; overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    }
    .uzay-tbl { width: 100%; border-collapse: collapse; }
    .uzay-tbl th {
        padding: 11px 14px; text-align: left;
        font-size: 0.63rem; text-transform: uppercase; letter-spacing: 1.2px;
        color: rgba(255,255,255,0.35); background: rgba(255,255,255,0.03);
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .uzay-tbl td {
        padding: 9px 14px; border-bottom: 1px solid rgba(255,255,255,0.03);
    }
    .uzay-tbl tr:hover td { background: rgba(139,92,246,0.04); }
    .uzay-badge {
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-size: 0.63rem; font-weight: 700; color: #fff;
    }
    [data-testid="stTabs"] > div:first-child > div[role="tablist"] {
        background: linear-gradient(135deg, #020014 0%, #0d1137 60%, #1a0a2e 100%) !important;
        border-radius: 14px !important; padding: 6px 8px !important;
        gap: 4px !important; flex-wrap: wrap !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.2) !important;
    }
    [data-testid="stTabs"] > div:first-child button[role="tab"] {
        color: rgba(255,255,255,0.55) !important; border: none !important;
        border-radius: 10px !important; font-weight: 600 !important;
        font-size: 0.8rem !important; padding: 8px 16px !important;
        transition: all .3s ease !important; background: transparent !important;
    }
    [data-testid="stTabs"] > div:first-child button[role="tab"]:hover {
        background: rgba(139,92,246,0.12) !important;
        color: rgba(255,255,255,0.85) !important;
    }
    [data-testid="stTabs"] > div:first-child button[aria-selected="true"] {
        background: rgba(255,255,255,0.93) !important;
        color: #4A00E0 !important; font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    </style>""", unsafe_allow_html=True)


# ============================================================
# RENDER
# ============================================================

def _render_hero():
    kat_sayisi = len(_KATEGORILER)
    konu_sayisi = len(_KONULAR)
    gezegen = sum(1 for k in _KONULAR if k["kat"] == "gunes_sistemi")
    st.markdown(f"""<div class="uzay-hero">
<div class="uzay-hero-stars"></div>
<div class="uzay-hero-nebula"></div>
<div class="uzay-hero-ring"></div>
<div class="uzay-hero-planets">🪐 ✨ 🌍</div>
<div class="uzay-hero-content">
<div class="uzay-hero-badge"><span class="uzay-hero-badge-dot"></span> 3D Ultra Premium</div>
<div class="uzay-hero-title">🔭 Uzay Kesfet</div>
<div class="uzay-hero-sub">Gezegenler, Ay, Dunya ve uzayin sirlarini kesfet! Kartlarin uzerine gel, bilgi evreni acilsin!</div>
<div class="uzay-hero-stats">
<div class="uzay-hero-stat"><div class="uzay-hero-stat-val">{konu_sayisi}</div><div class="uzay-hero-stat-lbl">Konu</div></div>
<div class="uzay-hero-stat"><div class="uzay-hero-stat-val">{kat_sayisi}</div><div class="uzay-hero-stat-lbl">Kategori</div></div>
<div class="uzay-hero-stat"><div class="uzay-hero-stat-val">{gezegen}</div><div class="uzay-hero-stat-lbl">Gezegen</div></div>
<div class="uzay-hero-stat"><div class="uzay-hero-stat-val">3D</div><div class="uzay-hero-stat-lbl">Kartlar</div></div>
</div></div></div>""", unsafe_allow_html=True)


def _kart_html(k: dict, idx: int) -> str:
    delay = (idx % 6) * 0.4
    kat = _KAT_MAP.get(k["kat"], {})
    r = k["renk"]
    return (
        f'<div class="uzay-card" style="--c1:{r};--c2:{r}88;--cg:{r}44;--fd:{delay}s;">'
        f'<div class="uzay-card-inner">'
        f'<div class="uzay-card-front">'
        f'<div class="uzay-card-num">#{k["id"]:02d}</div>'
        f'<div class="uzay-card-cat">{kat.get("baslik","")[:12]}</div>'
        f'<div class="uzay-card-emoji">{k["emoji"]}</div>'
        f'<div class="uzay-card-title">{k["baslik"]}</div>'
        f'<div class="uzay-card-desc">{k["aciklama"]}</div>'
        f'<div class="uzay-card-hint">cevir &rarr;</div>'
        f'</div>'
        f'<div class="uzay-card-back">'
        f'<div class="uzay-card-back-icon">💡</div>'
        f'<div class="uzay-card-back-label">Bunu Biliyor Muydun?</div>'
        f'<div class="uzay-card-back-div"></div>'
        f'<div class="uzay-card-back-fact">{k["bilgi"]}</div>'
        f'<div class="uzay-card-back-ft">{k["emoji"]} {k["baslik"]}</div>'
        f'</div>'
        f'</div></div>'
    )


def _render_kat(kat: dict):
    konular = [k for k in _KONULAR if k["kat"] == kat["id"]]
    if not konular:
        return
    st.markdown(
        f'<div class="uzay-kat-header" style="background:linear-gradient(135deg,{kat["renk1"]},{kat["renk2"]});">'
        f'<div class="uzay-kat-emoji">{kat["emoji"]}</div>'
        f'<div><div class="uzay-kat-title">{kat["baslik"]}</div>'
        f'<div class="uzay-kat-desc">{kat["aciklama"]}</div></div>'
        f'<div class="uzay-kat-count">{len(konular)} konu</div></div>',
        unsafe_allow_html=True
    )
    html = '<div class="uzay-grid">'
    for i, k in enumerate(konular):
        html += _kart_html(k, i)
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    st.markdown(
        f'<div class="uzay-info-banner"><span style="font-size:1.3rem;">{kat["ikon"]}</span>'
        f'<span>Kartlarin uzerine gelerek 3D bilgi kartini cevir!</span></div>',
        unsafe_allow_html=True
    )


def _render_tum():
    st.markdown(
        '<div class="uzay-kat-header" style="background:linear-gradient(135deg,#4A00E0,#8E2DE2);">'
        '<div class="uzay-kat-emoji">🌌</div>'
        '<div><div class="uzay-kat-title">Tum Konular</div>'
        '<div class="uzay-kat-desc">30 uzay konusu tek bakista</div></div>'
        '<div class="uzay-kat-count">30 konu</div></div>',
        unsafe_allow_html=True
    )
    html = '<div class="uzay-grid">'
    for i, k in enumerate(_KONULAR):
        html += _kart_html(k, i)
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_stats():
    cards = ""
    for kat in _KATEGORILER:
        n = sum(1 for k in _KONULAR if k["kat"] == kat["id"])
        cards += (
            f'<div class="uzay-stat-card">'
            f'<div class="uzay-stat-emoji">{kat["emoji"]}</div>'
            f'<div class="uzay-stat-val" style="color:{kat["renk1"]};">{n}</div>'
            f'<div class="uzay-stat-lbl">{kat["baslik"]}</div></div>'
        )
    st.markdown(f'<div class="uzay-stat-grid">{cards}</div>', unsafe_allow_html=True)


def _render_tablo():
    rows = ""
    for k in _KONULAR:
        kat = _KAT_MAP.get(k["kat"], {})
        rows += (
            f'<tr><td style="color:rgba(255,255,255,0.35);font-weight:800;font-size:.75rem;">#{k["id"]:02d}</td>'
            f'<td style="font-size:1.3rem;text-align:center;">{k["emoji"]}</td>'
            f'<td style="color:#fff;font-weight:600;">{k["baslik"]}</td>'
            f'<td><span class="uzay-badge" style="background:{kat.get("renk1","#666")};">{kat.get("baslik","")}</span></td></tr>'
        )
    st.markdown(
        f'<div class="uzay-tbl-wrap"><table class="uzay-tbl">'
        f'<thead><tr><th>No</th><th></th><th>Konu</th><th>Kategori</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True
    )


def _render_smarti():
    def ctx() -> str:
        return f"Uzay Kesfet: {len(_KONULAR)} konu, {len(_KATEGORILER)} kategori."
    render_smarti_chat("uzay_kesfet", ctx)


# ============================================================
# ANA GIRIS
# ============================================================

def render_uzay_kesfet():
    try:
        _inject_css_core()
        _inject_css_cards()
        _inject_css_extra()

        render_smarti_welcome("uzay_kesfet")
        _render_hero()

        tab_labels = [f"{k['emoji']} {k['baslik']}" for k in _KATEGORILER]
        tab_labels += ["🌌 Tum Konular", "📊 Ozet", "🤖 Smarti"]
        tabs = st.tabs(tab_labels)

        for i, kat in enumerate(_KATEGORILER):
            with tabs[i]:
                _render_kat(kat)

        with tabs[len(_KATEGORILER)]:
            _render_tum()

        with tabs[len(_KATEGORILER) + 1]:
            st.markdown(
                '<div class="uzay-kat-header" style="background:linear-gradient(135deg,#4A00E0,#8E2DE2);">'
                '<div class="uzay-kat-emoji">📊</div>'
                '<div><div class="uzay-kat-title">Konu Ozeti</div>'
                '<div class="uzay-kat-desc">Kategorilere gore dagilim</div></div></div>',
                unsafe_allow_html=True
            )
            _render_stats()
            _render_tablo()

        with tabs[len(_KATEGORILER) + 2]:
            _render_smarti()

    except Exception as e:
        import traceback
        st.error(f"Uzay Kesfet Hata: {e}")
        st.code(traceback.format_exc(), language="python")
