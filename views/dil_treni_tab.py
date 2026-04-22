"""
Dil Treni — 10 Dil Vagonu, 400 kelime/cümle per dil
Tren + vagon metaforu, flashcard, arama, kategori filtresi, TTS
Kişisel Dil Gelişimi modülüne alt sekme olarak eklenir.
"""
from __future__ import annotations
import json
import streamlit as st
import streamlit.components.v1 as components

from data.dil_treni.config import LANGUAGES, CATEGORIES, CATEGORY_ORDER

# ── Lazy data loaders ──
_WORD_CACHE: dict[str, list] = {}


def _load_words(lang_code: str) -> list[dict]:
    """Dil koduna göre kelime listesini yükle."""
    if lang_code in _WORD_CACHE:
        return _WORD_CACHE[lang_code]
    try:
        mod = __import__(f"data.dil_treni.words_{lang_code}", fromlist=["WORDS"])
        _WORD_CACHE[lang_code] = mod.WORDS
        return mod.WORDS
    except ImportError:
        _WORD_CACHE[lang_code] = []
        return []


_DT_PREFIX = "dil_treni_"


# ══════════════════════════════════════════════════════════════════════════════
# TRAIN HUB — 10 vagon seçim ekranı
# ══════════════════════════════════════════════════════════════════════════════

def _build_train_hub_html() -> str:
    """10 dil vagonu ile tren hub HTML'i."""
    # Vagon HTML'leri
    wagons_html = ""
    for i, lang in enumerate(LANGUAGES):
        wagons_html += f"""
        <div class="dt-wagon" onclick="selectLang('{lang['code']}')" title="{lang['name']}">
            <div class="dt-wb">
                <div class="dt-wr"></div>
                <div class="dt-wi">
                    <div class="dt-wflag">{lang['flag']}</div>
                    <div class="dt-wname">{lang['name']}</div>
                </div>
                <div class="dt-ww dt-w1"></div>
                <div class="dt-ww dt-w2"></div>
            </div>
            <div class="dt-wh">
                <div class="dt-whl"></div>
                <div class="dt-whl"></div>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}

.dt-scene {{
    position: relative;
    width: 100%;
    height: 340px;
    overflow: hidden;
    background: linear-gradient(180deg, #05051a, #0B0F19 40%, #131825 70%, #1A2035);
    border-radius: 16px;
    border: 1px solid rgba(212,175,55,0.2);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* ── Stars ── */
.dt-stars {{ position: absolute; width: 100%; height: 45%; }}
.dt-star {{
    position: absolute;
    border-radius: 50%;
    background: #6366F1;
    animation: dt-tw 2s ease-in-out infinite alternate;
}}
@keyframes dt-tw {{
    0% {{ opacity: 0.3; transform: scale(0.8); }}
    100% {{ opacity: 1; transform: scale(1.2); }}
}}

/* ── Moon ── */
.dt-moon {{
    position: absolute;
    top: 12px; right: 40px;
    width: 32px; height: 32px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #6366F1, #6366F1);
    box-shadow: 0 0 35px rgba(212,175,55,0.4);
}}

/* ── Title ── */
.dt-title {{
    position: absolute;
    top: 8px; left: 0; right: 0;
    text-align: center;
    z-index: 10;
}}
.dt-title h1 {{
    font-size: 1.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366F1, #6366F1, #6366F1);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: dt-shimmer 3s linear infinite;
    letter-spacing: 2px;
}}
.dt-title p {{
    color: #94A3B8;
    font-size: 0.72rem;
    margin-top: 2px;
}}
@keyframes dt-shimmer {{
    0% {{ background-position: -200% 0; }}
    100% {{ background-position: 200% 0; }}
}}

/* ── Ground & Rails ── */
.dt-ground {{
    position: absolute;
    bottom: 0; width: 100%; height: 80px;
    background: linear-gradient(180deg, #131825, #0e0e30);
    border-top: 2px solid rgba(212,175,55,0.15);
}}
.dt-ties {{
    position: absolute;
    bottom: 25px; width: 300%; height: 18px;
    background: repeating-linear-gradient(90deg, #2a2a50 0px, #2a2a50 5px, transparent 5px, transparent 35px);
}}
.dt-rail {{
    position: absolute;
    bottom: 38px; width: 300%; height: 3px;
    background: linear-gradient(90deg, #6366F1, #A5B4FC, #6366F1, #A5B4FC);
    background-size: 180px;
    box-shadow: 0 0 6px rgba(212,175,55,0.3);
}}
.dt-rail2 {{ bottom: 24px; }}

/* ── Train container ── */
.dt-train-scroll {{
    position: absolute;
    bottom: 40px;
    left: 0; right: 0;
    overflow-x: auto;
    overflow-y: visible;
    white-space: nowrap;
    padding: 0 20px 10px 20px;
    scrollbar-width: thin;
    scrollbar-color: rgba(212,175,55,0.3) transparent;
    z-index: 5;
}}
.dt-train-scroll::-webkit-scrollbar {{ height: 4px; }}
.dt-train-scroll::-webkit-scrollbar-thumb {{ background: rgba(212,175,55,0.3); border-radius: 4px; }}

.dt-train-group {{
    display: inline-flex;
    align-items: flex-end;
    gap: 6px;
    animation: dt-idle 3s ease-in-out infinite;
    padding-top: 30px;
}}
@keyframes dt-idle {{
    0%,100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-2px); }}
}}
.dt-train-group.dt-dep {{
    animation: dt-depart 2s ease-in forwards !important;
}}
@keyframes dt-depart {{
    0% {{ transform: translateX(0); }}
    30% {{ transform: translateX(10px) translateY(-3px); }}
    100% {{ transform: translateX(120vw); }}
}}

/* ── Locomotive ── */
.dt-loco {{
    display: inline-block;
    position: relative;
    width: 120px; height: 85px;
    vertical-align: bottom;
}}
.dt-loco-body {{
    position: absolute;
    bottom: 16px; left: 14px;
    width: 95px; height: 42px;
    background: linear-gradient(180deg, #232B3E, #131825);
    border: 2px solid #6366F1;
    border-radius: 6px 20px 3px 3px;
    box-shadow: 0 0 10px rgba(212,175,55,0.2);
}}
.dt-loco-cabin {{
    position: absolute;
    bottom: 40px; right: 18px;
    width: 38px; height: 30px;
    background: linear-gradient(180deg, #1A2035, #131825);
    border: 2px solid #6366F1;
    border-radius: 5px 5px 0 0;
}}
.dt-loco-window {{
    position: absolute;
    top: 5px; left: 5px;
    width: 12px; height: 10px;
    background: rgba(212,175,55,0.3);
    border-radius: 2px;
    border: 1px solid #6366F1;
}}
.dt-chimney {{
    position: absolute;
    bottom: 58px; left: 22px;
    width: 12px; height: 18px;
    background: linear-gradient(180deg, #6366F1, #A5B4FC);
    border-radius: 3px 3px 1px 1px;
}}
.dt-headlight {{
    position: absolute;
    bottom: 32px; left: 10px;
    width: 8px; height: 8px;
    background: radial-gradient(circle, #6366F1, #6366F1);
    border-radius: 50%;
    box-shadow: 0 0 15px #6366F1;
}}
.dt-loco-wheel {{
    position: absolute;
    bottom: 5px;
    width: 16px; height: 16px;
    border-radius: 50%;
    border: 2px solid #6366F1;
    background: radial-gradient(circle, #232B3E 40%, #131825);
    animation: dt-ws 0.8s linear infinite paused;
}}
.dt-loco-wheel::after {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 8px; height: 2px;
    background: #6366F1;
    transform: translate(-50%,-50%);
}}
.dt-lw1 {{ left: 18px; }}
.dt-lw2 {{ left: 46px; }}
.dt-lw3 {{ left: 76px; }}
@keyframes dt-ws {{
    0% {{ transform: rotate(0); }}
    100% {{ transform: rotate(360deg); }}
}}
.dt-dep .dt-loco-wheel,
.dt-dep .dt-whl {{
    animation-play-state: running !important;
}}

/* ── Smoke ── */
.dt-smoke-box {{
    position: absolute;
    bottom: 80px; left: 18px;
    width: 24px; height: 40px;
    overflow: visible; z-index: 6;
}}
.dt-smoke {{
    position: absolute; bottom: 0;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212,175,55,0.2), rgba(212,175,55,0.04));
    animation: dt-sr 2.5s ease-out infinite;
}}
@keyframes dt-sr {{
    0% {{ opacity: 0.6; transform: translateY(0) scale(0.3); }}
    50% {{ opacity: 0.3; transform: translateY(-30px) translateX(6px) scale(1); }}
    100% {{ opacity: 0; transform: translateY(-60px) translateX(14px) scale(1.3); }}
}}

/* ── Wagon ── */
.dt-wagon {{
    display: inline-block;
    position: relative;
    width: 90px; height: 72px;
    vertical-align: bottom;
    cursor: pointer;
    transition: transform 0.3s, filter 0.3s;
}}
.dt-wagon:hover {{
    transform: translateY(-8px) scale(1.06);
    filter: brightness(1.25);
}}
.dt-wb {{
    position: absolute;
    bottom: 14px; left: 5px; right: 5px;
    height: 46px;
    background: linear-gradient(180deg, #1A2035, #131825);
    border: 2px solid rgba(212,175,55,0.5);
    border-radius: 4px;
    box-shadow: 0 0 8px rgba(212,175,55,0.15);
    overflow: hidden;
}}
.dt-wr {{
    position: absolute;
    top: -3px; left: -2px; right: -2px;
    height: 4px;
    background: linear-gradient(90deg, #A5B4FC, #6366F1, #A5B4FC);
    border-radius: 2px;
}}
.dt-wi {{
    position: absolute;
    inset: 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}
.dt-wflag {{
    font-size: 1.4rem;
    line-height: 1;
    filter: drop-shadow(0 2px 4px rgba(212,175,55,0.3));
}}
.dt-wname {{
    font-size: 0.5rem;
    color: #6366F1;
    font-weight: 700;
    margin-top: 3px;
    letter-spacing: 0.3px;
}}
.dt-ww {{
    position: absolute;
    bottom: -2px;
    width: 3px; height: 12px;
    background: #A5B4FC;
}}
.dt-w1 {{ left: 12px; }}
.dt-w2 {{ right: 12px; }}
.dt-wh {{
    position: absolute;
    bottom: 3px; left: 6px; right: 6px;
    display: flex;
    justify-content: space-between;
    padding: 0 10px;
}}
.dt-whl {{
    width: 12px; height: 12px;
    border-radius: 50%;
    border: 2px solid #6366F1;
    background: radial-gradient(circle, #232B3E 40%, #131825);
    animation: dt-ws 0.8s linear infinite paused;
}}

/* ── Nav arrows ── */
.dt-nav {{
    position: absolute;
    bottom: 90px;
    width: 36px; height: 36px;
    background: rgba(212,175,55,0.15);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 50%;
    color: #6366F1;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20;
    transition: all 0.3s;
}}
.dt-nav:hover {{
    background: rgba(212,175,55,0.3);
    box-shadow: 0 0 12px rgba(212,175,55,0.3);
}}
.dt-nav-left {{ left: 8px; }}
.dt-nav-right {{ right: 8px; }}

/* ── Info bar ── */
.dt-info {{
    position: absolute;
    bottom: 8px; left: 20px; right: 20px;
    text-align: center;
    color: #64748B;
    font-size: 0.72rem;
    z-index: 10;
}}
</style>
</head>
<body>
<div class="dt-scene">
    <!-- Stars -->
    <div class="dt-stars" id="dtStars"></div>
    <!-- Moon -->
    <div class="dt-moon"></div>
    <!-- Title -->
    <div class="dt-title">
        <h1>🚂 DİL TRENİ</h1>
        <p>10 Dil • 4000 Kelime • Sesli Telaffuz</p>
    </div>
    <!-- Ground -->
    <div class="dt-ground">
        <div class="dt-ties"></div>
        <div class="dt-rail"></div>
        <div class="dt-rail dt-rail2"></div>
    </div>
    <!-- Train -->
    <div class="dt-train-scroll" id="dtScroll">
        <div class="dt-train-group" id="dtTrain">
            <!-- Locomotive -->
            <div class="dt-loco">
                <div class="dt-smoke-box">
                    <div class="dt-smoke" style="width:12px;height:12px;left:4px;animation-delay:0s"></div>
                    <div class="dt-smoke" style="width:16px;height:16px;left:8px;animation-delay:0.8s"></div>
                    <div class="dt-smoke" style="width:10px;height:10px;left:1px;animation-delay:1.6s"></div>
                </div>
                <div class="dt-chimney"></div>
                <div class="dt-loco-body"></div>
                <div class="dt-loco-cabin">
                    <div class="dt-loco-window"></div>
                    <div class="dt-loco-window" style="left:27px"></div>
                </div>
                <div class="dt-headlight"></div>
                <div class="dt-loco-wheel dt-lw1"></div>
                <div class="dt-loco-wheel dt-lw2"></div>
                <div class="dt-loco-wheel dt-lw3"></div>
            </div>
            <!-- Wagons -->
            {wagons_html}
        </div>
    </div>
    <!-- Nav -->
    <div class="dt-nav dt-nav-left" onclick="scrollTrain(-200)">◀</div>
    <div class="dt-nav dt-nav-right" onclick="scrollTrain(200)">▶</div>
    <!-- Info -->
    <div class="dt-info">◆ Bir vagon seçerek dil öğrenmeye başlayın ◆</div>
    <!-- (dialog kaldırıldı — seçim Streamlit butonlarından yapılır) -->
</div>

<script>
// Stars
(function() {{
    const c = document.getElementById('dtStars');
    for (let i = 0; i < 40; i++) {{
        const s = document.createElement('div');
        s.className = 'dt-star';
        const sz = 1 + Math.random() * 2.5;
        s.style.cssText = `width:${{sz}}px;height:${{sz}}px;top:${{Math.random()*100}}%;left:${{Math.random()*100}}%;animation-delay:${{Math.random()*3}}s`;
        c.appendChild(s);
    }}
}})();

function scrollTrain(dx) {{
    document.getElementById('dtScroll').scrollBy({{ left: dx, behavior: 'smooth' }});
}}

function selectLang(code) {{
    // Sadece görsel efekt — seçim aşağıdaki Streamlit butonlarından yapılır
    const el = document.querySelector('.dt-wagon[onclick*="' + code + '"]');
    if (el) {{
        el.style.transform = 'translateY(-10px) scale(1.1)';
        el.style.filter = 'brightness(1.4)';
        setTimeout(() => {{ el.style.transform = ''; el.style.filter = ''; }}, 600);
    }}
}}
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# FLASHCARD + GRID UI — tek dil görünümü
# ══════════════════════════════════════════════════════════════════════════════

def _build_lang_html(lang_code: str) -> str:
    """Bir dil için flashcard + grid HTML'i."""
    lang = next((l for l in LANGUAGES if l["code"] == lang_code), None)
    if not lang:
        return "<p>Dil bulunamadı.</p>"

    words = _load_words(lang_code)
    if not words:
        return f"<p>{lang['name']} kelime verisi henüz yüklenmedi.</p>"

    cats_json = json.dumps(CATEGORIES, ensure_ascii=False)
    cat_order_json = json.dumps(CATEGORY_ORDER)
    words_json = json.dumps(words, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
:root {{
    --gold: #6366F1;
    --gold2: #6366F1;
    --navy: #0B0F19;
    --navy2: #1A2035;
    --text: #E2E8F0;
    --muted: #94A3B8;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
    background: linear-gradient(180deg, #05051a, #0B0F19);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 16px;
}}

/* ── Header ── */
.dt-header {{
    background: linear-gradient(135deg, var(--navy), var(--navy2));
    padding: 20px 24px;
    border-radius: 14px;
    border: 1px solid rgba(212,175,55,0.25);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 16px;
}}
.dt-header-flag {{ font-size: 2.5rem; }}
.dt-header-info h2 {{
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gold), var(--gold2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.dt-header-info p {{ color: var(--muted); font-size: 0.82rem; margin-top: 2px; }}

/* ── Stats ── */
.dt-stats {{
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}}
.dt-stat {{
    flex: 1;
    min-width: 90px;
    background: linear-gradient(135deg, rgba(20,20,60,0.9), rgba(10,10,46,0.95));
    padding: 12px 14px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid rgba(212,175,55,0.15);
}}
.dt-stat-val {{
    font-size: 1.3rem;
    font-weight: 800;
    color: var(--gold);
}}
.dt-stat-lbl {{
    font-size: 0.68rem;
    color: var(--muted);
    margin-top: 2px;
}}

/* ── Progress ── */
.dt-progress-bar {{
    height: 6px;
    background: rgba(212,175,55,0.1);
    border-radius: 3px;
    margin-bottom: 14px;
    overflow: hidden;
}}
.dt-progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--gold), var(--gold2));
    border-radius: 3px;
    transition: width 0.4s;
}}

/* ── Controls ── */
.dt-controls {{
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}}
.dt-search {{
    flex: 1;
    min-width: 200px;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(212,175,55,0.25);
    background: rgba(20,20,60,0.9);
    color: var(--text);
    font-size: 0.88rem;
    outline: none;
}}
.dt-search:focus {{
    border-color: var(--gold);
    box-shadow: 0 0 10px rgba(212,175,55,0.15);
}}
.dt-mode-btn {{
    padding: 10px 18px;
    border-radius: 10px;
    border: 1px solid rgba(212,175,55,0.3);
    background: linear-gradient(135deg, var(--navy2), var(--navy));
    color: var(--gold);
    font-weight: 700;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.3s;
}}
.dt-mode-btn:hover, .dt-mode-btn.active {{
    background: linear-gradient(135deg, var(--gold), #A5B4FC);
    color: var(--navy);
    box-shadow: 0 0 15px rgba(212,175,55,0.25);
}}

/* ── Categories ── */
.dt-cats {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}}
.dt-cat {{
    padding: 6px 12px;
    border-radius: 16px;
    border: 1px solid rgba(212,175,55,0.2);
    background: rgba(20,20,60,0.8);
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s;
    white-space: nowrap;
}}
.dt-cat:hover {{ border-color: rgba(212,175,55,0.5); color: var(--gold); }}
.dt-cat.active {{
    background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(244,208,63,0.1));
    border-color: var(--gold);
    color: var(--gold);
}}

/* ── Grid ── */
.dt-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 10px;
}}
.dt-card {{
    background: linear-gradient(145deg, rgba(20,20,60,0.95), rgba(10,10,46,0.98));
    border: 1px solid rgba(212,175,55,0.15);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
    transition: all 0.3s;
    position: relative;
}}
.dt-card:hover {{
    border-color: rgba(212,175,55,0.4);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}}
.dt-card-word {{
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--gold);
    margin-bottom: 4px;
}}
.dt-card-ph {{
    font-size: 0.78rem;
    color: #94A3B8;
    font-style: italic;
    margin-bottom: 6px;
}}
.dt-card-tr {{
    font-size: 0.88rem;
    color: var(--text);
    margin-bottom: 8px;
}}
.dt-card-cat {{
    font-size: 0.62rem;
    color: var(--muted);
    background: rgba(212,175,55,0.08);
    padding: 2px 8px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 6px;
}}
.dt-play-btn {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 5px 14px;
    border-radius: 14px;
    border: 1px solid rgba(212,175,55,0.3);
    background: rgba(212,175,55,0.1);
    color: var(--gold);
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s;
}}
.dt-play-btn:hover {{
    background: var(--gold);
    color: var(--navy);
}}

/* ── Flashcard ── */
.dt-fc-container {{ display: none; }}
.dt-fc-container.active {{ display: block; }}
.dt-grid-container {{ display: block; }}
.dt-grid-container.hidden {{ display: none; }}

.dt-flashcard {{
    max-width: 460px;
    margin: 0 auto 16px;
    min-height: 280px;
    perspective: 1000px;
    cursor: pointer;
}}
.dt-fc-inner {{
    position: relative;
    width: 100%;
    min-height: 280px;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}}
.dt-flashcard.flipped .dt-fc-inner {{
    transform: rotateY(180deg);
}}
.dt-fc-face {{
    position: absolute;
    width: 100%;
    min-height: 280px;
    backface-visibility: hidden;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px;
    text-align: center;
}}
.dt-fc-front {{
    background: linear-gradient(135deg, rgba(26,26,78,0.9), rgba(10,10,46,0.95));
    border: 2px solid var(--gold);
}}
.dt-fc-back {{
    background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(26,26,78,0.95));
    border: 2px solid var(--gold2);
    transform: rotateY(180deg);
}}
.dt-fc-label {{
    font-size: 0.75rem;
    color: var(--muted);
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 12px;
}}
.dt-fc-word {{
    font-size: 2rem;
    font-weight: 900;
    color: var(--gold);
    margin-bottom: 6px;
}}
.dt-fc-answer {{
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--gold);
    margin-bottom: 6px;
}}
.dt-fc-phonetic {{
    font-size: 1rem;
    color: #94A3B8;
    font-style: italic;
    margin-bottom: 10px;
}}
.dt-fc-turkish {{
    font-size: 0.9rem;
    color: var(--text);
    margin-bottom: 12px;
}}
.dt-fc-hint {{
    font-size: 0.75rem;
    color: var(--muted);
}}
.dt-fc-play {{
    padding: 8px 20px;
    border-radius: 16px;
    border: 1px solid var(--gold);
    background: rgba(212,175,55,0.15);
    color: var(--gold);
    font-weight: 700;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.3s;
}}
.dt-fc-play:hover {{
    background: var(--gold);
    color: var(--navy);
}}

.dt-fc-actions {{
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 12px;
}}
.dt-fc-btn {{
    padding: 10px 22px;
    border-radius: 18px;
    border: none;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 700;
    transition: all 0.25s;
}}
.dt-fc-btn.repeat {{ background: #e74c3c; color: #fff; }}
.dt-fc-btn.repeat:hover {{ background: #c0392b; }}
.dt-fc-btn.skip {{ background: rgba(255,255,255,0.1); color: var(--text); }}
.dt-fc-btn.skip:hover {{ background: rgba(255,255,255,0.2); }}
.dt-fc-btn.learned {{ background: #2ecc71; color: #fff; }}
.dt-fc-btn.learned:hover {{ background: #27ae60; }}

.dt-fc-counter {{
    text-align: center;
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 8px;
}}

/* ── Empty ── */
.dt-empty {{
    text-align: center;
    padding: 40px;
    color: var(--muted);
    font-size: 0.9rem;
}}
</style>
</head>
<body>

<!-- Header -->
<div class="dt-header">
    <div class="dt-header-flag">{lang['flag']}</div>
    <div class="dt-header-info">
        <h2>◆ {lang['name']}</h2>
        <p id="dtWordCount">0 kelime • Sesli telaffuz ile öğren</p>
    </div>
</div>

<!-- Stats -->
<div class="dt-stats">
    <div class="dt-stat">
        <div class="dt-stat-val" id="dtTotal">0</div>
        <div class="dt-stat-lbl">Toplam</div>
    </div>
    <div class="dt-stat">
        <div class="dt-stat-val" id="dtLearned">0</div>
        <div class="dt-stat-lbl">Öğrenildi</div>
    </div>
    <div class="dt-stat">
        <div class="dt-stat-val" id="dtRemaining">0</div>
        <div class="dt-stat-lbl">Kalan</div>
    </div>
    <div class="dt-stat">
        <div class="dt-stat-val" id="dtCatCount">0</div>
        <div class="dt-stat-lbl">Kategori</div>
    </div>
</div>

<!-- Progress -->
<div class="dt-progress-bar">
    <div class="dt-progress-fill" id="dtProgress" style="width:0%"></div>
</div>

<!-- Controls -->
<div class="dt-controls">
    <input type="text" class="dt-search" id="dtSearch" placeholder="🔍 Kelime ara (Türkçe veya {lang['name']})..." oninput="applyFilters()">
    <button class="dt-mode-btn" id="dtGridBtn" onclick="setMode('grid')">▦ Grid</button>
    <button class="dt-mode-btn" id="dtFcBtn" onclick="setMode('flashcard')">🃏 Flashcard</button>
</div>

<!-- Categories -->
<div class="dt-cats" id="dtCats"></div>

<!-- Grid -->
<div class="dt-grid-container" id="dtGridContainer">
    <div class="dt-grid" id="dtGrid"></div>
    <div class="dt-empty" id="dtEmpty" style="display:none">Sonuç bulunamadı</div>
</div>

<!-- Flashcard -->
<div class="dt-fc-container" id="dtFcContainer">
    <div class="dt-flashcard" id="dtFlashcard" onclick="flipCard()">
        <div class="dt-fc-inner">
            <div class="dt-fc-face dt-fc-front">
                <div class="dt-fc-label">TÜRKÇE</div>
                <div class="dt-fc-word" id="dtFcWord"></div>
                <div class="dt-fc-hint">Kartı çevirmek için tıklayın</div>
            </div>
            <div class="dt-fc-face dt-fc-back">
                <div class="dt-fc-answer" id="dtFcAnswer"></div>
                <div class="dt-fc-phonetic" id="dtFcPh"></div>
                <div class="dt-fc-turkish" id="dtFcTr"></div>
                <button class="dt-fc-play" onclick="event.stopPropagation();playFcAudio()">▶ Dinle</button>
            </div>
        </div>
    </div>
    <div class="dt-fc-actions">
        <button class="dt-fc-btn repeat" onclick="markCard('repeat')">↻ Tekrar</button>
        <button class="dt-fc-btn skip" onclick="markCard('skip')">▶ Atla</button>
        <button class="dt-fc-btn learned" onclick="markCard('learned')">✓ Öğrendim</button>
    </div>
    <div class="dt-fc-counter" id="dtFcCounter"></div>
</div>

<script>
const LANG = '{lang_code}';
const TTS_CODE = '{lang["tts"]}';
const DATA = {words_json};
const CATS = {cats_json};
const CAT_ORDER = {cat_order_json};

let activeCats = new Set();
let mode = 'grid';
let learned = {{}};
let fcFiltered = [];
let fcIndex = 0;

// ── localStorage ──
const STORE_KEY = 'dt_learned_' + LANG;
function loadProgress() {{
    try {{
        const d = localStorage.getItem(STORE_KEY);
        if (d) learned = JSON.parse(d);
    }} catch(e) {{}}
}}
function saveProgress() {{
    try {{ localStorage.setItem(STORE_KEY, JSON.stringify(learned)); }} catch(e) {{}}
}}
function getLKey(w) {{ return w.tr + '|' + w.word; }}

// ── TTS ──
function speak(text) {{
    if (!window.speechSynthesis) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = TTS_CODE;
    u.rate = 0.85;
    speechSynthesis.speak(u);
}}

// ── Filter ──
function getFiltered() {{
    const q = (document.getElementById('dtSearch').value || '').toLowerCase().trim();
    return DATA.filter(w => {{
        if (activeCats.size && !activeCats.has(w.cat)) return false;
        if (q) {{
            const hay = (w.tr + ' ' + w.word + ' ' + (w.ph || '')).toLowerCase();
            if (!hay.includes(q)) return false;
        }}
        return true;
    }});
}}

// ── Grid: bir kez oluştur, CSS ile filtrele ──
let gridBuilt = false;
let allCards = [];

function buildGridOnce() {{
    if (gridBuilt) return;
    const el = document.getElementById('dtGrid');
    let h = '';
    DATA.forEach((w, idx) => {{
        const catInfo = CATS[w.cat] || {{}};
        const safeWord = (w.word || '').replace(/&/g,'&amp;').replace(/"/g,'&quot;');
        h += `<div class="dt-card" data-cat="${{w.cat}}" data-idx="${{idx}}" data-search="${{(w.tr+' '+w.word+' '+(w.ph||'')).toLowerCase()}}">
            <div class="dt-card-cat">${{catInfo.icon || ''}} ${{catInfo.tr || w.cat}}</div>
            <div class="dt-card-word">${{w.word}}</div>
            <div class="dt-card-ph">${{w.ph || ''}}</div>
            <div class="dt-card-tr">${{w.tr}}</div>
            <button class="dt-play-btn" data-word="${{safeWord}}" onclick="event.stopPropagation();speak(this.dataset.word)">▶ Dinle</button>
        </div>`;
    }});
    el.innerHTML = h;
    allCards = Array.from(el.children);
    gridBuilt = true;
}}

function applyFilters() {{
    const q = (document.getElementById('dtSearch').value || '').toLowerCase().trim();
    let visibleCount = 0;

    if (mode === 'grid') {{
        buildGridOnce();
        allCards.forEach(card => {{
            const cat = card.dataset.cat;
            const search = card.dataset.search;
            const catOk = !activeCats.size || activeCats.has(cat);
            const searchOk = !q || search.includes(q);
            const show = catOk && searchOk;
            card.style.display = show ? '' : 'none';
            if (show) visibleCount++;
        }});
        document.getElementById('dtEmpty').style.display = visibleCount ? 'none' : 'block';
    }} else {{
        fcFiltered = getFiltered();
        fcIndex = 0;
        renderFlashcard();
        visibleCount = fcFiltered.length;
    }}
    renderStats(visibleCount);
}}

// ── Categories ──
let catChips = [];
function renderCats() {{
    if (catChips.length) {{
        catChips.forEach(ch => {{
            ch.classList.toggle('active', activeCats.has(ch.dataset.cid), key="dil_treni__m1");
        }});
        return;
    }}
    const el = document.getElementById('dtCats');
    let h = '';
    const usedCats = new Set(DATA.map(w => w.cat));
    CAT_ORDER.forEach(cid => {{
        if (!usedCats.has(cid)) return;
        const c = CATS[cid];
        if (!c) return;
        h += `<div class="dt-cat" data-cid="${{cid}}" onclick="toggleCat('${{cid}}')">${{c.icon}} ${{c.tr}}</div>`;
    }});
    el.innerHTML = h;
    catChips = Array.from(el.children);
}}
function toggleCat(cid) {{
    if (activeCats.has(cid)) activeCats.delete(cid);
    else activeCats.add(cid);
    renderCats();
    applyFilters();
}}

// ── Stats ──
function renderStats(visibleCount) {{
    const total = DATA.length;
    const learnedCount = Object.values(learned).filter(v => v).length;
    const cats = new Set(DATA.map(w => w.cat));
    document.getElementById('dtTotal').textContent = total;
    document.getElementById('dtLearned').textContent = learnedCount;
    document.getElementById('dtRemaining').textContent = total - learnedCount;
    document.getElementById('dtCatCount').textContent = cats.size;
    document.getElementById('dtWordCount').textContent = (visibleCount !== undefined ? visibleCount : total) + ' kelime • Sesli telaffuz ile öğren';
    const pct = total > 0 ? (learnedCount / total * 100) : 0;
    document.getElementById('dtProgress').style.width = pct.toFixed(1) + '%';
}}

// ── Flashcard ──
function renderFlashcard() {{
    const card = document.getElementById('dtFlashcard');
    card.classList.remove('flipped');
    if (!fcFiltered.length) {{
        document.getElementById('dtFcWord').textContent = '—';
        document.getElementById('dtFcAnswer').textContent = '—';
        document.getElementById('dtFcPh').textContent = '';
        document.getElementById('dtFcTr').textContent = '';
        document.getElementById('dtFcCounter').textContent = '';
        return;
    }}
    if (fcIndex >= fcFiltered.length) fcIndex = 0;
    const w = fcFiltered[fcIndex];
    document.getElementById('dtFcWord').textContent = w.tr;
    document.getElementById('dtFcAnswer').textContent = w.word;
    document.getElementById('dtFcPh').textContent = w.ph || '';
    document.getElementById('dtFcTr').textContent = w.tr;
    document.getElementById('dtFcCounter').textContent = (fcIndex + 1) + ' / ' + fcFiltered.length;
}}
function flipCard() {{
    document.getElementById('dtFlashcard').classList.toggle('flipped', key="dil_treni__m2");
}}
function playFcAudio() {{
    if (!fcFiltered.length) return;
    speak(fcFiltered[fcIndex].word);
}}
function markCard(action) {{
    if (!fcFiltered.length) return;
    const w = fcFiltered[fcIndex];
    const lk = getLKey(w);
    if (action === 'learned') {{ learned[lk] = true; saveProgress(); }}
    else if (action === 'repeat') {{ learned[lk] = false; saveProgress(); }}
    fcIndex++;
    if (fcIndex >= fcFiltered.length) fcIndex = 0;
    renderFlashcard();
    renderStats();
}}

// ── Mode ──
function setMode(m) {{
    mode = m;
    document.getElementById('dtGridBtn').classList.toggle('active', m === 'grid', key="dil_treni__m3");
    document.getElementById('dtFcBtn').classList.toggle('active', m === 'flashcard', key="dil_treni__m4");
    document.getElementById('dtGridContainer').classList.toggle('hidden', m !== 'grid', key="dil_treni__m5");
    document.getElementById('dtFcContainer').classList.toggle('active', m === 'flashcard', key="dil_treni__m6");
    applyFilters();
}}

// ── Init ──
loadProgress();
renderCats();
setMode('grid');
applyFilters();
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render_dil_treni():
    """Dil Treni ana render fonksiyonu."""
    # Init state
    if "dt_selected_lang" not in st.session_state:
        st.session_state["dt_selected_lang"] = None

    # Check query params for language selection (from iframe redirect)
    qp = st.query_params.get("dt_lang", "")
    if qp and qp in [l["code"] for l in LANGUAGES]:
        st.session_state["dt_selected_lang"] = qp
        try:
            del st.query_params["dt_lang"]
        except Exception:
            pass
        st.rerun()

    selected = st.session_state["dt_selected_lang"]

    if selected and selected in [l["code"] for l in LANGUAGES]:
        # Üst bar: Geri butonu + dil bilgisi
        lang_info = next((l for l in LANGUAGES if l["code"] == selected), None)
        c1, c2, c3 = st.columns([0.15, 0.15, 0.70])
        with c1:
            if st.button("🚂 Trene Dön", key="dt_back_hub", type="secondary", use_container_width=True):
                st.session_state["dt_selected_lang"] = None
                st.rerun()
        with c2:
            if st.button("◆ Ana Menü", key="dt_back_kdg", type="secondary", use_container_width=True):
                st.session_state["dt_selected_lang"] = None
                from views.kisisel_dil_gelisimi import _VIEW_KEY
                st.session_state[_VIEW_KEY] = "hub"
                st.rerun()
        with c3:
            if lang_info:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#0B0F19,#141440);'
                    f'padding:8px 16px;border-radius:10px;border:1px solid rgba(212,175,55,0.15);'
                    f'display:inline-flex;align-items:center;gap:8px;">'
                    f'<span style="font-size:1.4rem">{lang_info["flag"]}</span>'
                    f'<span style="font-size:1rem;font-weight:800;'
                    f'background:linear-gradient(135deg,#6366F1,#6366F1);'
                    f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
                    f'background-clip:text;">{lang_info["name"]} — 400 Kelime</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        # Render language content
        try:
            html = _build_lang_html(selected)
            components.html(html, height=1200, scrolling=True)
        except Exception as e:
            st.error(f"Dil yüklenirken hata: {e}")
            if st.button("🚂 Trene Geri Dön", key="dt_back_err", type="primary"):
                st.session_state["dt_selected_lang"] = None
                st.rerun()
    else:
        # Train hub — tren animasyonu + fallback butonlar
        components.html(_build_train_hub_html(), height=350, scrolling=False)

        # Dil seçim butonları — tren animasyonu altında
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0B0F19,#141440);'
            'padding:16px 20px;border-radius:14px;border:1px solid rgba(212,175,55,0.2);'
            'margin-top:8px;text-align:center;">'
            '<span style="font-size:0.9rem;font-weight:800;'
            'background:linear-gradient(135deg,#6366F1,#6366F1);'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            'background-clip:text;">◆ Dil Seçin — Vagona Binin ◆</span></div>',
            unsafe_allow_html=True,
        )
        row1 = st.columns(5)
        row2 = st.columns(5)
        for i, lang in enumerate(LANGUAGES):
            col = row1[i] if i < 5 else row2[i - 5]
            with col:
                if st.button(
                    f"{lang['flag']} {lang['name']}",
                    key=f"dt_sel_{lang['code']}",
                    use_container_width=True,
                    type="primary",
                ):
                    st.session_state["dt_selected_lang"] = lang["code"]
                    st.rerun()
