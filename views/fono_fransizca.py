"""
Fono Fransizca - Kendi Kendine Hizli Fransizca Egitim Portali
104 Ders, ders ders ilerleyen, interaktif alistirmali ogrenme modulu
"""
from __future__ import annotations
import json, os, pathlib, random, streamlit as st
import streamlit.components.v1 as _components
from datetime import datetime

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
_DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "fono_fransizca"
_LESSONS_FILE = _DATA_DIR / "fono_fransizca_lessons.json"
_PROGRESS_FILE = _DATA_DIR / "user_progress_fr.json"
_PRATIK_FILE = _DATA_DIR / "gunluk_pratik_fr.json"
_PREFIX = "fono_fr_"

_BOOK_INFO = {
    1: {"title": "Birinci Basamak - Kitap 1", "level": "A1 Baslangic", "range": (1, 26),
        "color": "#4f46e5", "color_light": "#818cf8", "color_bg": "#e0e7ff", "emoji": "\U0001f4d8"},
    2: {"title": "Birinci Basamak - Kitap 2", "level": "A1 Baslangic", "range": (27, 52),
        "color": "#4f46e5", "color_light": "#818cf8", "color_bg": "#e0e7ff", "emoji": "\U0001f4d7"},
    3: {"title": "Ikinci Basamak - Kitap 1", "level": "A2 Temel", "range": (53, 78),
        "color": "#7c3aed", "color_light": "#a78bfa", "color_bg": "#ede9fe", "emoji": "\U0001f4d9"},
    4: {"title": "Ikinci Basamak - Kitap 2", "level": "A2 Temel", "range": (79, 104),
        "color": "#7c3aed", "color_light": "#a78bfa", "color_bg": "#ede9fe", "emoji": "\U0001f4d5"},
}

# ---------------------------------------------------------------------------
# TTS JavaScript core
# ---------------------------------------------------------------------------
_TTS_JS_CORE = """
<script>
function speakFR(text, rate) {
    var synth = window.speechSynthesis;
    synth.cancel();
    var utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'fr-FR';
    utter.rate = rate || 0.85;
    utter.pitch = 1.05;
    var voices = synth.getVoices();
    var pref = ['Amelie','Thomas','Virginie','Aurelie','Nicolas','Julie'];
    var frV = null;
    for (var i = 0; i < voices.length; i++) {
        if (voices[i].lang && voices[i].lang.startsWith('fr')) {
            if (!frV) frV = voices[i];
            for (var j = 0; j < pref.length; j++) {
                if (voices[i].name.indexOf(pref[j]) !== -1) { frV = voices[i]; break; }
            }
        }
    }
    if (frV) utter.voice = frV;
    synth.speak(utter);
}
window.speechSynthesis.onvoiceschanged = function(){};
</script>
"""

# ---------------------------------------------------------------------------
# Veri yukleme / kaydetme
# ---------------------------------------------------------------------------
def _load_lessons() -> list[dict]:
    if _LESSONS_FILE.exists():
        with open(_LESSONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("lessons", [])
    return []


def _load_progress() -> dict:
    if _PROGRESS_FILE.exists():
        with open(_PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed_lessons": [], "exercise_scores": {}, "current_lesson": 1}


def _save_progress(prog: dict):
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)


def _get_lesson(lessons: list, ders_no: int) -> dict | None:
    for l in lessons:
        if l.get("ders") == ders_no:
            return l
    return None


def _is_unlocked(ders_no: int, progress: dict) -> bool:
    if ders_no == 1:
        return True
    completed = set(progress.get("completed_lessons", []))
    return (ders_no - 1) in completed


def _get_book_for_lesson(ders_no: int) -> int:
    for bid, info in _BOOK_INFO.items():
        if info["range"][0] <= ders_no <= info["range"][1]:
            return bid
    return 1


# ---------------------------------------------------------------------------
# CSS — Blue/Indigo theme
# ---------------------------------------------------------------------------
def _inject_css():
    if st.session_state.get(f"{_PREFIX}css_done"):
        return
    st.session_state[f"{_PREFIX}css_done"] = True
    st.markdown("""
    <style>
    .fono-header {
        background: linear-gradient(135deg, #312e81 0%, #4f46e5 50%, #3730a3 100%);
        color: white; padding: 28px 32px; border-radius: 16px;
        margin-bottom: 24px; position: relative; overflow: hidden;
        box-shadow: 0 8px 32px rgba(79,70,229,0.3);
    }
    .fono-header::before {
        content: ''; position: absolute; top: -50%; right: -20%;
        width: 300px; height: 300px; border-radius: 50%;
        background: rgba(255,255,255,0.05);
    }
    .fono-header h1 { margin: 0; font-size: 1.8rem; font-weight: 800; }
    .fono-header p { margin: 4px 0 0 0; opacity: 0.85; font-size: 0.95rem; }

    .fono-lesson-card {
        background: white; border-radius: 12px; padding: 14px 18px;
        border: 1px solid #e2e8f0; margin-bottom: 8px;
        border-left: 4px solid #4f46e5; transition: all 0.2s ease;
    }
    .fono-lesson-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .fono-lesson-locked {
        opacity: 0.5; border-left-color: #94a3b8;
    }
    .fono-lesson-done {
        border-left-color: #10b981; background: #f0fdf4;
    }

    .fono-vocab-card {
        background: linear-gradient(135deg, #111827, #1A2035);
        padding: 12px 16px; border-radius: 10px; border: 1px solid #e2e8f0;
        margin-bottom: 8px; transition: all 0.2s;
    }
    .fono-vocab-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .fono-vocab-fr { font-weight: 700; color: #4338ca; font-size: 1.1rem; }
    .fono-vocab-pron { color: #6366f1; font-size: 0.85rem; font-style: italic; }
    .fono-vocab-tr { color: #475569; font-size: 0.95rem; margin-top: 2px; }

    .fono-grammar-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac; border-radius: 12px;
        padding: 16px 20px; margin: 12px 0;
    }
    .fono-reading-box {
        background: #fffbeb; border: 1px solid #fcd34d;
        border-radius: 12px; padding: 16px 20px; margin: 12px 0; line-height: 1.7;
    }
    .fono-exercise-box {
        background: linear-gradient(135deg, #eef2ff, #e0e7ff);
        border: 1px solid #a5b4fc; border-radius: 12px;
        padding: 16px 20px; margin: 12px 0;
    }

    .fono-step-nav {
        display: flex; gap: 6px; margin-bottom: 16px; flex-wrap: wrap;
    }
    .fono-step-btn {
        padding: 8px 16px; border-radius: 8px; font-size: 0.85rem;
        font-weight: 600; cursor: pointer; border: 2px solid #e2e8f0;
        background: white; color: #475569; transition: all 0.2s;
    }
    .fono-step-btn.active {
        background: #4f46e5; color: white; border-color: #4f46e5;
    }

    .fono-progress-bar {
        background: #e2e8f0; border-radius: 8px; height: 10px;
        overflow: hidden; margin: 8px 0;
    }
    .fono-progress-fill {
        height: 100%; border-radius: 8px;
        background: linear-gradient(90deg, #4f46e5, #818cf8);
        transition: width 0.5s ease;
    }
    .fono-stat-card {
        background: white; border-radius: 12px; padding: 16px;
        text-align: center; border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .fono-stat-num { font-size: 1.8rem; font-weight: 800; color: #4f46e5; }
    .fono-stat-label { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; }

    .fono-correct { background: #d1fae5 !important; border-color: #10b981 !important; }
    .fono-wrong { background: #fee2e2 !important; border-color: #ef4444 !important; }

    .fono-flashcard {
        background: linear-gradient(135deg, #4f46e5, #3730a3);
        color: white; border-radius: 16px; padding: 40px;
        text-align: center; margin: 16px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        min-height: 180px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .fono-flashcard .word { font-size: 2rem; font-weight: 800; }
    .fono-flashcard .pron { font-size: 1rem; opacity: 0.8; margin-top: 4px; font-style: italic; }
    .fono-flashcard .meaning { font-size: 1.2rem; margin-top: 12px; opacity: 0.9; }

    .fono-book-header {
        border-radius: 14px; padding: 20px 24px; margin-bottom: 16px;
        color: white; box-shadow: 0 6px 24px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
def _render_header():
    st.markdown("""
    <div class="fono-header">
        <h1>FONO Kendi Kendine Hizli Fransizca</h1>
        <p>104 Ders | 4 Kitap | Adim Adim Fransizca Ogrenme Portali</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Genel ilerleme
# ---------------------------------------------------------------------------
def _render_stats(lessons: list, progress: dict):
    completed = set(progress.get("completed_lessons", []))
    total = len(lessons) if lessons else 104
    done = len(completed)
    pct = int(done / total * 100) if total else 0

    cols = st.columns(4)
    stats = [
        ("Toplam Ders", str(total), "#4f46e5"),
        ("Tamamlanan", str(done), "#059669"),
        ("Kalan", str(total - done), "#f59e0b"),
        ("Ilerleme", f"%{pct}", "#7c3aed"),
    ]
    for col, (label, val, color) in zip(cols, stats):
        col.markdown(f"""
        <div class="fono-stat-card">
            <div class="fono-stat-num" style="color:{color}">{val}</div>
            <div class="fono-stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fono-progress-bar">
        <div class="fono-progress-fill" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Kitap & Ders Listesi
# ---------------------------------------------------------------------------
def _render_book_list(lessons: list, progress: dict):
    completed = set(progress.get("completed_lessons", []))

    for bid, info in _BOOK_INFO.items():
        color = info["color"]
        color_light = info["color_light"]
        rng = info["range"]
        book_lessons = [l for l in lessons if rng[0] <= l["ders"] <= rng[1]]
        book_done = sum(1 for l in book_lessons if l["ders"] in completed)
        book_total = rng[1] - rng[0] + 1
        book_pct = int(book_done / book_total * 100) if book_total else 0

        with st.expander(f"{info['emoji']} Kitap {bid}: {info['title']} ({info['level']}) - %{book_pct}", expanded=(bid == 1)):
            st.markdown(f"""
            <div class="fono-progress-bar">
                <div class="fono-progress-fill" style="width:{book_pct}%; background:linear-gradient(90deg,{color},{color_light})"></div>
            </div>
            <div style="font-size:0.8rem; color:{color}; font-weight:600; margin-bottom:12px">
                {book_done}/{book_total} ders tamamlandi
            </div>
            """, unsafe_allow_html=True)

            # Ders listesi
            for ders_no in range(rng[0], rng[1] + 1):
                lesson = _get_lesson(lessons, ders_no)
                is_done = ders_no in completed
                unlocked = _is_unlocked(ders_no, progress)
                title = lesson.get("title", f"Ders {ders_no}") if lesson else f"Ders {ders_no}"

                if is_done:
                    icon = "\u2705"
                    css_class = "fono-lesson-done"
                elif unlocked:
                    icon = "\U0001f513"
                    css_class = ""
                else:
                    icon = "\U0001f512"
                    css_class = "fono-lesson-locked"

                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f"""
                    <div class="fono-lesson-card {css_class}" style="border-left-color:{color}">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:1.1rem">{icon}</span>
                            <div>
                                <div style="font-weight:700; color:#0B0F19; font-size:0.95rem">Ders {ders_no}: {title}</div>
                                <div style="font-size:0.75rem; color:#94a3b8">
                                    {lesson.get('type_label', '') if lesson else ''}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if unlocked:
                        label = "Tekrar" if is_done else "Basla"
                        if st.button(label, key=f"{_PREFIX}open_{ders_no}", use_container_width=True):
                            st.session_state[f"{_PREFIX}view"] = "lesson"
                            st.session_state[f"{_PREFIX}ders_no"] = ders_no
                            st.session_state[f"{_PREFIX}step"] = 0
                            # Reset exercise states
                            for k in list(st.session_state.keys()):
                                if k.startswith(f"{_PREFIX}ex_"):
                                    del st.session_state[k]
                            st.rerun()


# ---------------------------------------------------------------------------
# Ders Icerik Ekrani
# ---------------------------------------------------------------------------
def _render_lesson(lessons: list, progress: dict):
    ders_no = st.session_state.get(f"{_PREFIX}ders_no", 1)
    step = st.session_state.get(f"{_PREFIX}step", 0)
    lesson = _get_lesson(lessons, ders_no)

    if not lesson:
        st.error(f"Ders {ders_no} icerigi bulunamadi.")
        if st.button("Geri Don", key=f"{_PREFIX}back_err"):
            st.session_state[f"{_PREFIX}view"] = "list"
            st.rerun()
        return

    bid = _get_book_for_lesson(ders_no)
    info = _BOOK_INFO[bid]
    color = info["color"]
    color_light = info["color_light"]

    # Geri butonu
    if st.button("\u2190 Ders Listesine Don", key=f"{_PREFIX}back_to_list"):
        st.session_state[f"{_PREFIX}view"] = "list"
        st.rerun()

    # Ders header
    st.markdown(f"""
    <div class="fono-book-header" style="background:linear-gradient(135deg,{color},{color_light})">
        <h2 style="margin:0; font-size:1.4rem">Ders {ders_no}: {lesson.get('title', '')}</h2>
        <p style="margin:4px 0 0 0; opacity:0.85; font-size:0.85rem">
            {info['emoji']} Kitap {bid} | {info['title']} | {lesson.get('type_label', '')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Adim butonlari
    has_vocab = bool(lesson.get("vocabulary"))
    has_grammar = bool(lesson.get("grammar_topics"))
    has_reading = bool(lesson.get("reading"))
    has_exercises = bool(lesson.get("exercises"))

    steps = []
    if has_vocab:
        steps.append(("Kelimeler", "vocab"))
    if has_grammar:
        steps.append(("Gramer", "grammar"))
    if has_reading:
        steps.append(("Okuma", "reading"))
    if has_exercises:
        steps.append(("Alistirmalar", "exercises"))

    if not steps:
        st.warning("Bu ders icin icerik henuz yuklenmemis.")
        return

    # Clamp step
    if step >= len(steps):
        step = 0

    # Step navigation
    step_cols = st.columns(len(steps))
    for i, (label, _) in enumerate(steps):
        with step_cols[i]:
            btn_type = "primary" if i == step else "secondary"
            if st.button(label, key=f"{_PREFIX}nav_{ders_no}_{i}", use_container_width=True, type=btn_type):
                st.session_state[f"{_PREFIX}step"] = i
                st.rerun()

    st.markdown("---")

    step_type = steps[step][1]

    if step_type == "vocab":
        _render_vocabulary(lesson, ders_no, color, color_light)
    elif step_type == "grammar":
        _render_grammar(lesson, ders_no)
    elif step_type == "reading":
        _render_reading(lesson, ders_no)
    elif step_type == "exercises":
        _render_exercises(lesson, ders_no, progress)

    # Navigasyon ve tamamlama
    st.markdown("---")
    nav_cols = st.columns([1, 2, 1])

    with nav_cols[0]:
        if step > 0:
            if st.button("\u2190 Onceki", key=f"{_PREFIX}prev_step_{ders_no}", use_container_width=True):
                st.session_state[f"{_PREFIX}step"] = step - 1
                st.rerun()

    with nav_cols[1]:
        completed = set(progress.get("completed_lessons", []))
        if ders_no not in completed:
            if st.button("\u2705 Dersi Tamamla", key=f"{_PREFIX}complete_{ders_no}",
                        type="primary", use_container_width=True):
                progress.setdefault("completed_lessons", []).append(ders_no)
                _save_progress(progress)
                st.success(f"Ders {ders_no} tamamlandi!")
                st.balloons()
                st.rerun()
        else:
            st.success("Bu ders tamamlandi!")

    with nav_cols[2]:
        if step < len(steps) - 1:
            if st.button("Sonraki \u2192", key=f"{_PREFIX}next_step_{ders_no}", use_container_width=True):
                st.session_state[f"{_PREFIX}step"] = step + 1
                st.rerun()
        elif ders_no < 104:
            next_ders = ders_no + 1
            if _is_unlocked(next_ders, progress):
                if st.button(f"Ders {next_ders} \u2192", key=f"{_PREFIX}next_lesson_{ders_no}", use_container_width=True):
                    st.session_state[f"{_PREFIX}ders_no"] = next_ders
                    st.session_state[f"{_PREFIX}step"] = 0
                    for k in list(st.session_state.keys()):
                        if k.startswith(f"{_PREFIX}ex_"):
                            del st.session_state[k]
                    st.rerun()


# ---------------------------------------------------------------------------
# KELIMELER — TTS destekli
# ---------------------------------------------------------------------------
def _render_vocabulary(lesson: dict, ders_no: int, color: str, color_light: str):
    vocab = lesson.get("vocabulary", [])
    if not vocab:
        st.info("Bu derste yeni kelime listesi yoktur.")
        return

    st.markdown(f"### Kelimeler ({len(vocab)} kelime)")

    # Gorunum secimi
    view_mode = st.radio("Gorunum:", ["Kartlar", "Flashcard"], key=f"{_PREFIX}vocab_mode_{ders_no}",
                         horizontal=True, label_visibility="collapsed")

    if view_mode == "Kartlar":
        _render_vocabulary_tts_grid(vocab, ders_no, color, color_light)

    elif view_mode == "Flashcard":
        _render_flashcard_tts(vocab, ders_no, color, color_light)


def _render_vocabulary_tts_grid(vocab: list, ders_no: int, color: str, color_light: str):
    """Kelime kartlari TTS destekli HTML grid."""
    cards_html = _TTS_JS_CORE + '<div style="display:flex;flex-wrap:wrap;gap:10px;">'

    for i, w in enumerate(vocab):
        fr = w.get("fr", "")
        pron = w.get("pron", "")
        tr = w.get("tr", "")
        fr_escaped = fr.replace("'", "\\'").replace('"', '\\"')

        cards_html += f"""
        <div style="background:linear-gradient(135deg,#111827,#1A2035);padding:14px 16px;
             border-radius:12px;border:1px solid #e2e8f0;border-left:4px solid {color};
             flex:1;min-width:200px;max-width:32%;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1;">
                    <div style="font-weight:700;color:#4338ca;font-size:1.05rem;margin-bottom:3px">
                        {fr}
                    </div>
                    <div style="color:#6366f1;font-size:0.82rem;font-style:italic;margin-bottom:4px">
                        [{pron}]
                    </div>
                    <div style="color:#475569;font-size:0.92rem">{tr}</div>
                </div>
                <div style="display:flex;flex-direction:column;gap:4px;flex-shrink:0;margin-left:8px;">
                    <button onclick="speakFR('{fr_escaped}', 0.85)"
                        style="background:linear-gradient(135deg,#4f46e5,#3730a3);color:white;
                        border:none;border-radius:50%;width:32px;height:32px;cursor:pointer;
                        font-size:0.9rem;display:flex;align-items:center;justify-content:center;
                        box-shadow:0 2px 8px rgba(79,70,229,0.3);"
                        title="Sesli Oku">&#128266;</button>
                    <button onclick="speakFR('{fr_escaped}', 0.55)"
                        style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:white;
                        border:none;border-radius:50%;width:32px;height:32px;cursor:pointer;
                        font-size:0.75rem;display:flex;align-items:center;justify-content:center;
                        box-shadow:0 2px 8px rgba(124,58,237,0.3);"
                        title="Yavas Oku">&#128034;</button>
                </div>
            </div>
        </div>
        """

    cards_html += '</div>'
    height = ((len(vocab) + 2) // 3) * 110 + 40
    _components.html(cards_html, height=min(height, 2000), scrolling=True)


def _render_flashcard_tts(vocab: list, ders_no: int, color: str, color_light: str):
    """Flashcard gorunumu — TTS destekli."""
    card_idx = st.session_state.get(f"{_PREFIX}fc_{ders_no}", 0)
    if card_idx >= len(vocab):
        card_idx = 0
    show_meaning = st.session_state.get(f"{_PREFIX}fc_show_{ders_no}", False)

    w = vocab[card_idx]
    fr_text = w.get("fr", "")
    fr_escaped = fr_text.replace("'", "\\'").replace('"', '\\"')
    meaning_html = f'<div class="meaning">{w.get("tr", "")}</div>' if show_meaning else '<div class="meaning" style="opacity:0.5">Anlami gormek icin tiklayin</div>'

    flashcard_html = _TTS_JS_CORE + f"""
    <div style="background:linear-gradient(135deg,{color},{color_light});
         color:white;border-radius:16px;padding:40px;text-align:center;
         box-shadow:0 8px 24px rgba(0,0,0,0.15);min-height:180px;
         display:flex;flex-direction:column;align-items:center;justify-content:center;">
        <div style="font-size:2rem;font-weight:800">{fr_text}</div>
        <div style="font-size:1rem;opacity:0.8;margin-top:4px;font-style:italic">[{w.get("pron", "")}]</div>
        {'<div style="font-size:1.2rem;margin-top:12px;opacity:0.9">' + w.get("tr", "") + '</div>' if show_meaning else '<div style="font-size:1.2rem;margin-top:12px;opacity:0.5">Anlami gormek icin tiklayin</div>'}
        <div style="margin-top:8px;opacity:0.6;font-size:0.8rem">
            {card_idx + 1} / {len(vocab)}
        </div>
        <div style="margin-top:14px;display:flex;gap:8px;">
            <button onclick="speakFR('{fr_escaped}', 0.85)"
                style="background:rgba(255,255,255,0.2);color:white;border:1px solid rgba(255,255,255,0.3);
                border-radius:20px;padding:8px 18px;cursor:pointer;font-size:0.9rem;">
                &#128266; Sesli Oku
            </button>
            <button onclick="speakFR('{fr_escaped}', 0.55)"
                style="background:rgba(255,255,255,0.1);color:white;border:1px solid rgba(255,255,255,0.2);
                border-radius:20px;padding:8px 18px;cursor:pointer;font-size:0.9rem;">
                &#128034; Yavas
            </button>
        </div>
    </div>
    """
    _components.html(flashcard_html, height=320, scrolling=False)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        if st.button("\u2190 Onceki", key=f"{_PREFIX}fc_prev_{ders_no}", use_container_width=True):
            st.session_state[f"{_PREFIX}fc_{ders_no}"] = max(0, card_idx - 1)
            st.session_state[f"{_PREFIX}fc_show_{ders_no}"] = False
            st.rerun()
    with fc2:
        label_show = "Gizle" if show_meaning else "Anlami Goster"
        if st.button(label_show, key=f"{_PREFIX}fc_toggle_{ders_no}", use_container_width=True):
            st.session_state[f"{_PREFIX}fc_show_{ders_no}"] = not show_meaning
            st.rerun()
    with fc3:
        if st.button("Sonraki \u2192", key=f"{_PREFIX}fc_next_{ders_no}", use_container_width=True):
            st.session_state[f"{_PREFIX}fc_{ders_no}"] = min(len(vocab) - 1, card_idx + 1)
            st.session_state[f"{_PREFIX}fc_show_{ders_no}"] = False
            st.rerun()


# ---------------------------------------------------------------------------
# GRAMER — TTS destekli
# ---------------------------------------------------------------------------
def _render_grammar(lesson: dict, ders_no: int):
    topics = lesson.get("grammar_topics", [])
    examples = lesson.get("grammar_examples", [])

    st.markdown("### Gramer Konulari")

    if topics:
        for t in topics:
            st.markdown(f"""
            <div class="fono-grammar-box">
                <div style="font-weight:700; color:#166534; font-size:1rem; margin-bottom:4px">{t}</div>
            </div>
            """, unsafe_allow_html=True)

    if examples:
        st.markdown("#### Ornek Cumleler")
        examples_html = _TTS_JS_CORE + '<div style="display:flex;flex-direction:column;gap:8px;">'

        for ex in examples:
            fr = ex.get("fr", "")
            tr = ex.get("tr", "")
            fr_escaped = fr.replace("'", "\\'").replace('"', '\\"')

            examples_html += f"""
            <div style="background:white;border:1px solid #e2e8f0;border-radius:8px;
                 padding:10px 14px;border-left:3px solid #4f46e5;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="flex:1;">
                        <div style="font-weight:600;color:#4338ca">{fr}</div>
                        <div style="color:#64748b;font-size:0.9rem;margin-top:2px">{tr}</div>
                    </div>
                    <div style="display:flex;gap:4px;flex-shrink:0;margin-left:8px;">
                        <button onclick="speakFR('{fr_escaped}', 0.85)"
                            style="background:#4f46e5;color:white;border:none;border-radius:50%;
                            width:30px;height:30px;cursor:pointer;font-size:0.85rem;">&#128266;</button>
                        <button onclick="speakFR('{fr_escaped}', 0.55)"
                            style="background:#7c3aed;color:white;border:none;border-radius:50%;
                            width:30px;height:30px;cursor:pointer;font-size:0.75rem;">&#128034;</button>
                    </div>
                </div>
            </div>
            """

        examples_html += '</div>'
        height = len(examples) * 72 + 40
        _components.html(examples_html, height=min(height, 2000), scrolling=True)


# ---------------------------------------------------------------------------
# OKUMA — TTS destekli
# ---------------------------------------------------------------------------
def _render_reading(lesson: dict, ders_no: int):
    reading = lesson.get("reading", {})
    if not reading:
        st.info("Bu derste okuma parcasi yoktur.")
        return

    title = reading.get("title", "Okuma Parcasi")
    text_fr = reading.get("fr", "")
    text_tr = reading.get("tr", "")

    st.markdown(f"### {title}")

    # Okuma kutusu + TTS butonu
    fr_escaped = text_fr.replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
    reading_html = _TTS_JS_CORE + f"""
    <div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:12px;
         padding:16px 20px;line-height:1.8;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
            <div style="font-weight:700;color:#92400e">{title}</div>
            <div style="display:flex;gap:6px;flex-shrink:0;">
                <button onclick="speakFR('{fr_escaped}', 0.85)"
                    style="background:linear-gradient(135deg,#4f46e5,#3730a3);color:white;
                    border:none;border-radius:20px;padding:6px 14px;cursor:pointer;font-size:0.82rem;
                    box-shadow:0 2px 8px rgba(79,70,229,0.3);">
                    &#128266; Sesli Oku
                </button>
                <button onclick="speakFR('{fr_escaped}', 0.55)"
                    style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:white;
                    border:none;border-radius:20px;padding:6px 14px;cursor:pointer;font-size:0.82rem;
                    box-shadow:0 2px 8px rgba(124,58,237,0.3);">
                    &#128034; Yavas
                </button>
            </div>
        </div>
        <div style="color:#78350f;white-space:pre-line">{text_fr}</div>
    </div>
    """
    line_count = text_fr.count("\n") + 3
    height = max(line_count * 30 + 100, 200)
    _components.html(reading_html, height=min(height, 800), scrolling=True)

    if text_tr:
        with st.expander("Turkce Cevirisini Gor"):
            st.markdown(f"""
            <div style="background:#111827; border:1px solid #e2e8f0; border-radius:10px;
                 padding:14px 18px; line-height:1.7; white-space:pre-line">
                {text_tr}
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ALISTIRMALAR (interaktif)
# ---------------------------------------------------------------------------
def _render_exercises(lesson: dict, ders_no: int, progress: dict):
    exercises = lesson.get("exercises", [])
    if not exercises:
        st.info("Bu derste alistirma yoktur.")
        return

    st.markdown(f"### Alistirmalar ({len(exercises)} alistirma)")

    total_correct = 0
    total_questions = 0

    for ex_idx, exercise in enumerate(exercises):
        ex_type = exercise.get("type", "")
        ex_title = exercise.get("title", f"Alistirma {ex_idx + 1}")
        questions = exercise.get("questions", [])

        st.markdown(f"""
        <div class="fono-exercise-box">
            <div style="font-weight:700; color:#4338ca; font-size:1rem; margin-bottom:4px">
                {ex_title}
            </div>
            <div style="color:#6366f1; font-size:0.85rem">
                {_get_exercise_type_label(ex_type)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        checked_key = f"{_PREFIX}ex_checked_{ders_no}_{ex_idx}"
        is_checked = st.session_state.get(checked_key, False)

        for q_idx, q in enumerate(questions):
            total_questions += 1
            q_key = f"{_PREFIX}ex_{ders_no}_{ex_idx}_{q_idx}"

            if ex_type == "fill_blank":
                correct = _render_fill_blank(q, q_key, is_checked)
            elif ex_type == "translate_to_tr":
                correct = _render_translate(q, q_key, is_checked, "tr")
            elif ex_type == "translate_to_fr":
                correct = _render_translate(q, q_key, is_checked, "fr")
            elif ex_type == "multiple_choice":
                correct = _render_multiple_choice(q, q_key, is_checked)
            elif ex_type == "match":
                correct = _render_match(q, q_key, is_checked)
            elif ex_type == "true_false":
                correct = _render_true_false(q, q_key, is_checked)
            else:
                correct = _render_fill_blank(q, q_key, is_checked)

            if is_checked and correct:
                total_correct += 1

        # Kontrol butonu
        if not is_checked:
            if st.button(f"Cevaplari Kontrol Et", key=f"{_PREFIX}check_{ders_no}_{ex_idx}",
                        type="primary"):
                st.session_state[checked_key] = True
                st.rerun()
        else:
            ex_questions = len(questions)
            ex_correct = sum(1 for qi, q in enumerate(questions)
                           if _check_answer(q, f"{_PREFIX}ex_{ders_no}_{ex_idx}_{qi}", exercise.get("type", "")))
            pct = int(ex_correct / ex_questions * 100) if ex_questions else 0
            score_color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="background:white; border:2px solid {score_color}; border-radius:10px;
                 padding:12px 16px; text-align:center; margin:8px 0;">
                <span style="font-weight:700; color:{score_color}; font-size:1.2rem">
                    {ex_correct}/{ex_questions} Dogru (%{pct})
                </span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Tekrar Dene", key=f"{_PREFIX}retry_{ders_no}_{ex_idx}"):
                st.session_state[checked_key] = False
                for qi in range(len(questions)):
                    k = f"{_PREFIX}ex_{ders_no}_{ex_idx}_{qi}"
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

        st.markdown("---")

    # Save exercise score
    if any(st.session_state.get(f"{_PREFIX}ex_checked_{ders_no}_{i}", False)
           for i in range(len(exercises))):
        progress.setdefault("exercise_scores", {})[str(ders_no)] = {
            "total": total_questions,
            "correct": total_correct,
            "date": datetime.now().isoformat()
        }
        _save_progress(progress)


def _get_exercise_type_label(ex_type: str) -> str:
    labels = {
        "fill_blank": "Bosluk Doldurma",
        "translate_to_tr": "Fransizca -> Turkce Ceviri",
        "translate_to_fr": "Turkce -> Fransizca Ceviri",
        "multiple_choice": "Coktan Secmeli",
        "match": "Eslestirme",
        "true_false": "Dogru / Yanlis",
    }
    return labels.get(ex_type, "Alistirma")


def _render_fill_blank(q: dict, key: str, checked: bool) -> bool:
    sentence = q.get("sentence", "")
    answer = q.get("answer", "")
    display = sentence.replace("___", "______")

    st.markdown(f"**{display}**")
    user_input = st.text_input("Cevabiniz:", key=key, label_visibility="collapsed",
                                placeholder="Cevabinizi yazin...")

    if checked:
        is_correct = _normalize(user_input) == _normalize(answer)
        if is_correct:
            st.success(f"\u2705 Dogru! {answer}")
        else:
            st.error(f"\u274c Yanlis. Dogru cevap: **{answer}**")
        return is_correct
    return False


def _render_translate(q: dict, key: str, checked: bool, target: str) -> bool:
    source = q.get("source", "")
    answer = q.get("answer", "")
    direction = "Turkce'ye cevirin" if target == "tr" else "Fransizca'ya cevirin"

    st.markdown(f"**{source}** \u2192 _{direction}_")
    user_input = st.text_input("Ceviri:", key=key, label_visibility="collapsed",
                                placeholder="Cevirinizi yazin...")

    if checked:
        # Accept multiple valid answers
        valid_answers = [answer]
        if q.get("alt_answers"):
            valid_answers.extend(q["alt_answers"])
        is_correct = any(_normalize(user_input) == _normalize(a) for a in valid_answers)
        if is_correct:
            st.success(f"\u2705 Dogru! {answer}")
        else:
            st.error(f"\u274c Dogru cevap: **{answer}**")
        return is_correct
    return False


def _render_multiple_choice(q: dict, key: str, checked: bool) -> bool:
    question = q.get("question", "")
    options = q.get("options", [])
    correct_idx = q.get("correct", 0)

    st.markdown(f"**{question}**")
    selected = st.radio("Seciniz:", options, key=key, label_visibility="collapsed")

    if checked:
        correct_answer = options[correct_idx] if correct_idx < len(options) else ""
        is_correct = selected == correct_answer
        if is_correct:
            st.success(f"\u2705 Dogru!")
        else:
            st.error(f"\u274c Yanlis. Dogru cevap: **{correct_answer}**")
        return is_correct
    return False


def _render_true_false(q: dict, key: str, checked: bool) -> bool:
    statement = q.get("statement", "")
    answer = q.get("answer", True)

    st.markdown(f"**{statement}**")
    selected = st.radio("Dogru mu Yanlis mi?", ["Dogru", "Yanlis"], key=key,
                        horizontal=True, label_visibility="collapsed")

    if checked:
        user_bool = (selected == "Dogru")
        is_correct = user_bool == answer
        if is_correct:
            st.success(f"\u2705 Dogru!")
        else:
            st.error(f"\u274c Yanlis. Cevap: **{'Dogru' if answer else 'Yanlis'}**")
        return is_correct
    return False


def _render_match(q: dict, key: str, checked: bool) -> bool:
    pairs = q.get("pairs", [])
    if not pairs:
        return False

    st.markdown("**Eslestirin:**")
    # Show left side, user selects right side
    left_items = [p.get("left", "") for p in pairs]
    right_items = [p.get("right", "") for p in pairs]
    shuffled_right = right_items.copy()
    rng = random.Random(hash(key))
    rng.shuffle(shuffled_right)

    all_correct = True
    for i, left in enumerate(left_items):
        sel = st.selectbox(f"{left} \u2192", shuffled_right,
                          key=f"{key}_match_{i}", label_visibility="collapsed")
        if checked:
            correct = right_items[i]
            if sel == correct:
                st.success(f"\u2705 {left} = {correct}")
            else:
                st.error(f"\u274c {left} = **{correct}**")
                all_correct = False

    return all_correct if checked else False


def _check_answer(q: dict, key: str, ex_type: str) -> bool:
    user_val = st.session_state.get(key, "")
    if ex_type == "fill_blank":
        return _normalize(user_val) == _normalize(q.get("answer", ""))
    elif ex_type in ("translate_to_tr", "translate_to_fr"):
        valid = [q.get("answer", "")]
        if q.get("alt_answers"):
            valid.extend(q["alt_answers"])
        return any(_normalize(user_val) == _normalize(a) for a in valid)
    elif ex_type == "multiple_choice":
        options = q.get("options", [])
        correct_idx = q.get("correct", 0)
        correct = options[correct_idx] if correct_idx < len(options) else ""
        return user_val == correct
    elif ex_type == "true_false":
        return (user_val == "Dogru") == q.get("answer", True)
    return False


def _normalize(s: str) -> str:
    return s.strip().lower().rstrip(".!?,;:").strip()


# ---------------------------------------------------------------------------
# Gunluk Pratik Fransizca
# ---------------------------------------------------------------------------
def _load_pratik() -> dict:
    if _PRATIK_FILE.exists():
        with open(_PRATIK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _render_gunluk_pratik():
    data = _load_pratik()
    if not data or not data.get("chapters"):
        st.warning("Gunluk Pratik Fransizca verileri yuklenemedi.")
        return

    chapters = data["chapters"]

    st.markdown("""
    <div style="background:linear-gradient(135deg,#312e81 0%,#4f46e5 50%,#7c3aed 100%);
         padding:24px 28px;border-radius:14px;margin-bottom:20px;color:white;">
        <h2 style="margin:0;font-size:1.5rem;font-weight:800">Gunluk Pratik Fransizca</h2>
        <p style="margin:4px 0 0 0;opacity:0.85;font-size:0.88rem">
            Pratik Fransizca-Turkce El Kitabi — 13 Bolum, 70+ Alt Konu, 500+ Cumle & Sesli Okuma
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Bolum secimi
    ch_options = [f"{ch['id']}. {ch['title']}" for ch in chapters]
    sel_ch_label = st.selectbox("Bolum Secin:", ch_options, key=f"{_PREFIX}pratik_ch")
    sel_ch_idx = ch_options.index(sel_ch_label)
    chapter = chapters[sel_ch_idx]

    # Alt konu secimi
    sections = chapter.get("sections", [])
    if not sections:
        st.info("Bu bolumde henuz icerik yok.")
        return

    sec_options = [f"{s['id']} — {s['title']}" for s in sections]
    sel_sec_label = st.selectbox("Alt Konu:", sec_options, key=f"{_PREFIX}pratik_sec_{chapter['id']}")
    sel_sec_idx = sec_options.index(sel_sec_label)
    section = sections[sel_sec_idx]

    phrases = section.get("phrases", [])
    if not phrases:
        st.info("Bu konuda henuz ifade yok.")
        return

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#eef2ff,#e0e7ff);border:1px solid #a5b4fc;
         border-radius:12px;padding:14px 18px;margin-bottom:16px;">
        <div style="font-weight:700;color:#4338ca;font-size:1.1rem">{section['title']}</div>
        <div style="color:#6366f1;font-size:0.82rem;margin-top:2px">{len(phrases)} ifade</div>
    </div>
    """, unsafe_allow_html=True)

    # Gorunum modu
    view_mode = st.radio("Gorunum:", ["Kartlar", "Liste", "Quiz"],
                         key=f"{_PREFIX}pratik_mode_{chapter['id']}_{section['id']}",
                         horizontal=True, label_visibility="collapsed")

    if view_mode == "Kartlar":
        _render_pratik_cards(phrases, section['id'])
    elif view_mode == "Liste":
        _render_pratik_list(phrases, section['id'])
    elif view_mode == "Quiz":
        _render_pratik_quiz(phrases, section['id'])


def _render_pratik_cards(phrases: list, sec_id: str):
    """Kart gorunumu - TTS destekli."""
    cards_html = _TTS_JS_CORE + '<div style="display:flex;flex-direction:column;gap:10px;">'

    for i, p in enumerate(phrases):
        tr_text = p.get("tr", "")
        fr_text = p.get("fr", "")
        pron = p.get("pron", "")
        fr_escaped = fr_text.replace("'", "\\'").replace('"', '\\"')

        cards_html += f"""
        <div style="background:linear-gradient(135deg,#111827,#1A2035);padding:14px 18px;
             border-radius:12px;border:1px solid #e2e8f0;border-left:4px solid #4f46e5;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1;">
                    <div style="font-weight:700;color:#4338ca;font-size:1.05rem;margin-bottom:3px">
                        {fr_text}
                    </div>
                    <div style="color:#6366f1;font-size:0.82rem;font-style:italic;margin-bottom:4px">
                        /{pron}/
                    </div>
                    <div style="color:#475569;font-size:0.92rem">{tr_text}</div>
                </div>
                <div style="display:flex;gap:4px;flex-shrink:0;margin-left:10px;">
                    <button onclick="speakFR('{fr_escaped}', 0.85)"
                        style="background:linear-gradient(135deg,#4f46e5,#3730a3);color:white;
                        border:none;border-radius:50%;width:38px;height:38px;cursor:pointer;
                        font-size:1.1rem;display:flex;align-items:center;justify-content:center;
                        box-shadow:0 2px 8px rgba(79,70,229,0.3);"
                        title="Sesli Oku">&#128266;</button>
                    <button onclick="speakFR('{fr_escaped}', 0.55)"
                        style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:white;
                        border:none;border-radius:50%;width:38px;height:38px;cursor:pointer;
                        font-size:0.9rem;display:flex;align-items:center;justify-content:center;
                        box-shadow:0 2px 8px rgba(124,58,237,0.3);"
                        title="Yavas Oku">&#128034;</button>
                </div>
            </div>
        </div>
        """

    cards_html += '</div>'
    height = len(phrases) * 95 + 60
    _components.html(cards_html, height=min(height, 2000), scrolling=True)


def _render_pratik_list(phrases: list, sec_id: str):
    """Tablo gorunumu - TTS destekli."""
    list_html = _TTS_JS_CORE + """
    <table style="width:100%;border-collapse:collapse;font-size:0.9rem;">
        <thead>
            <tr style="background:linear-gradient(135deg,#312e81,#4f46e5);color:white;">
                <th style="padding:10px 12px;text-align:left;border-radius:8px 0 0 0;">Turkce</th>
                <th style="padding:10px 12px;text-align:left;">Fran\u00e7ais</th>
                <th style="padding:10px 12px;text-align:left;">Okunus</th>
                <th style="padding:10px 8px;text-align:center;border-radius:0 8px 0 0;width:50px;">&#128266;</th>
            </tr>
        </thead>
        <tbody>
    """

    for i, p in enumerate(phrases):
        tr_text = p.get("tr", "")
        fr_text = p.get("fr", "")
        pron = p.get("pron", "")
        fr_escaped = fr_text.replace("'", "\\'").replace('"', '\\"')
        bg = "#111827" if i % 2 == 0 else "#ffffff"

        list_html += f"""
        <tr style="background:{bg};border-bottom:1px solid #e2e8f0;">
            <td style="padding:8px 12px;color:#475569;font-weight:600">{tr_text}</td>
            <td style="padding:8px 12px;color:#4338ca;font-weight:700">{fr_text}</td>
            <td style="padding:8px 12px;color:#6366f1;font-style:italic;font-size:0.82rem">/{pron}/</td>
            <td style="padding:8px 8px;text-align:center">
                <button onclick="speakFR('{fr_escaped}', 0.85)"
                    style="background:#4f46e5;color:white;border:none;border-radius:50%;
                    width:30px;height:30px;cursor:pointer;font-size:0.85rem;">&#128266;</button>
            </td>
        </tr>
        """

    list_html += "</tbody></table>"
    height = len(phrases) * 42 + 80
    _components.html(list_html, height=min(height, 2000), scrolling=True)


def _render_pratik_quiz(phrases: list, sec_id: str):
    """Mini quiz - Turkce'den Fransizca'ya ceviri."""
    if len(phrases) < 3:
        st.info("Quiz icin en az 3 ifade gerekli.")
        return

    quiz_key = f"{_PREFIX}pratik_quiz_{sec_id}"
    if quiz_key not in st.session_state:
        sample_size = min(5, len(phrases))
        rng = random.Random()
        st.session_state[quiz_key] = rng.sample(range(len(phrases)), sample_size)

    indices = st.session_state[quiz_key]
    checked_key = f"{quiz_key}_checked"
    is_checked = st.session_state.get(checked_key, False)

    st.markdown("### Mini Quiz — Turkce -> Fransizca")

    correct_count = 0
    for qi, idx in enumerate(indices):
        p = phrases[idx]
        st.markdown(f"**{qi+1}.** {p['tr']}")
        user_ans = st.text_input("Fransizca karsiligi:", key=f"{quiz_key}_{qi}",
                                  placeholder="Cevabinizi yazin...", label_visibility="collapsed")
        if is_checked:
            norm_user = user_ans.strip().lower().rstrip(".!?,;:").strip()
            norm_answer = p['fr'].strip().lower().rstrip(".!?,;:").strip()
            if norm_user == norm_answer:
                st.success(f"\u2705 Dogru! {p['fr']}")
                correct_count += 1
            else:
                st.error(f"\u274c Dogru cevap: **{p['fr']}** /{p.get('pron', '')}/")

    if not is_checked:
        if st.button("Cevaplari Kontrol Et", key=f"{quiz_key}_btn", type="primary"):
            st.session_state[checked_key] = True
            st.rerun()
    else:
        pct = int(correct_count / len(indices) * 100)
        sc = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
        st.markdown(f"""
        <div style="background:white;border:2px solid {sc};border-radius:10px;
             padding:12px 16px;text-align:center;margin:8px 0;">
            <span style="font-weight:700;color:{sc};font-size:1.2rem">
                {correct_count}/{len(indices)} Dogru (%{pct})
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Yeni Quiz", key=f"{quiz_key}_retry"):
            del st.session_state[quiz_key]
            st.session_state[checked_key] = False
            for qi in range(len(indices)):
                k = f"{quiz_key}_{qi}"
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()


# ---------------------------------------------------------------------------
# Kelime Bankasi — TTS destekli
# ---------------------------------------------------------------------------
def _render_vocab_bank(lessons: list):
    st.markdown("### Kelime Bankasi")

    book_options = [f"Kitap {bid}: {info['title']}" for bid, info in _BOOK_INFO.items()]
    selected = st.selectbox("Kitap:", book_options, key=f"{_PREFIX}vb_book")
    bid = list(_BOOK_INFO.keys())[book_options.index(selected)]
    rng = _BOOK_INFO[bid]["range"]

    all_words = []
    for l in lessons:
        if rng[0] <= l["ders"] <= rng[1]:
            for w in l.get("vocabulary", []):
                all_words.append((w, l["ders"]))

    search = st.text_input("Kelime Ara:", key=f"{_PREFIX}vb_search", placeholder="Fransizca veya Turkce...")
    if search:
        all_words = [(w, d) for w, d in all_words
                     if search.lower() in w.get("fr", "").lower()
                     or search.lower() in w.get("tr", "").lower()]

    st.markdown(f"**{len(all_words)} kelime**")

    # TTS destekli kelime kartlari
    if all_words:
        bank_html = _TTS_JS_CORE + '<div style="display:flex;flex-wrap:wrap;gap:10px;">'

        for idx, (w, ders) in enumerate(all_words):
            fr = w.get("fr", "")
            pron = w.get("pron", "")
            tr = w.get("tr", "")
            fr_escaped = fr.replace("'", "\\'").replace('"', '\\"')

            bank_html += f"""
            <div style="background:linear-gradient(135deg,#111827,#1A2035);padding:12px 14px;
                 border-radius:10px;border:1px solid #e2e8f0;flex:1;min-width:200px;max-width:32%;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div style="flex:1;">
                        <div style="font-weight:700;color:#4338ca;font-size:1.05rem">{fr}</div>
                        <div style="color:#6366f1;font-size:0.8rem;font-style:italic">[{pron}]</div>
                        <div style="color:#475569;font-size:0.9rem;margin-top:2px">{tr}</div>
                        <div style="font-size:0.7rem;color:#94a3b8;margin-top:4px">Ders {ders}</div>
                    </div>
                    <div style="display:flex;flex-direction:column;gap:3px;flex-shrink:0;margin-left:6px;">
                        <button onclick="speakFR('{fr_escaped}', 0.85)"
                            style="background:#4f46e5;color:white;border:none;border-radius:50%;
                            width:28px;height:28px;cursor:pointer;font-size:0.8rem;">&#128266;</button>
                        <button onclick="speakFR('{fr_escaped}', 0.55)"
                            style="background:#7c3aed;color:white;border:none;border-radius:50%;
                            width:28px;height:28px;cursor:pointer;font-size:0.7rem;">&#128034;</button>
                    </div>
                </div>
            </div>
            """

        bank_html += '</div>'
        height = ((len(all_words) + 2) // 3) * 110 + 40
        _components.html(bank_html, height=min(height, 2000), scrolling=True)


# ---------------------------------------------------------------------------
# Ilerleme Raporu
# ---------------------------------------------------------------------------
def _render_progress_report(lessons: list, progress: dict):
    st.markdown("### Ilerleme Raporu")
    completed = set(progress.get("completed_lessons", []))
    scores = progress.get("exercise_scores", {})

    for bid, info in _BOOK_INFO.items():
        color = info["color"]
        rng = info["range"]
        total = rng[1] - rng[0] + 1
        done = sum(1 for d in range(rng[0], rng[1] + 1) if d in completed)
        pct = int(done / total * 100) if total else 0

        st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:14px 18px; margin-bottom:10px;
             border-left:5px solid {color}; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700">{info['emoji']} Kitap {bid}: {info['title']}</span>
                <span style="font-weight:700; color:{color}">{done}/{total}</span>
            </div>
            <div class="fono-progress-bar" style="margin-top:8px">
                <div class="fono-progress-fill" style="width:{pct}%; background:{color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Alistirma skorlari
    if scores:
        st.markdown("### Alistirma Sonuclari")
        for ders_str in sorted(scores.keys(), key=lambda x: int(x)):
            s = scores[ders_str]
            correct = s.get("correct", 0)
            total = s.get("total", 1)
            pct = int(correct / total * 100) if total else 0
            sc = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:6px 0; border-bottom:1px solid #1A2035">
                <span style="font-weight:600; min-width:80px">Ders {ders_str}</span>
                <div class="fono-progress-bar" style="flex:1">
                    <div class="fono-progress-fill" style="width:{pct}%; background:{sc}"></div>
                </div>
                <span style="font-weight:700; color:{sc}">{correct}/{total} (%{pct})</span>
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ANA RENDER
# ---------------------------------------------------------------------------
def render_fono_fransizca():
    _inject_css()
    _render_header()

    lessons = _load_lessons()
    progress = _load_progress()

    view = st.session_state.get(f"{_PREFIX}view", "list")

    if view == "lesson":
        _render_lesson(lessons, progress)
    else:
        tabs = st.tabs(["Dersler", "Ilerleme", "Kelime Bankasi", "Gunluk Pratik Fransizca"])
        with tabs[0]:
            _render_stats(lessons, progress)
            st.markdown("---")
            _render_book_list(lessons, progress)
        with tabs[1]:
            _render_progress_report(lessons, progress)
        with tabs[2]:
            _render_vocab_bank(lessons)
        with tabs[3]:
            _render_gunluk_pratik()
