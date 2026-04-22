# -*- coding: utf-8 -*-
"""Grade 2 Interactive Activity Book — EBA-style HTML pages.

Generates HTML activity book pages with:
- SVG cartoon characters with speech bubbles
- Interactive vocabulary cards with TTS
- Speaking-Expression sections
- Listening & pronunciation sections
- Drag-and-drop / click activities
- Colorful, child-friendly design

Each week produces 2 double-page spreads (4 pages).
"""
from __future__ import annotations


# ── SVG Character Library ────────────────────────────────────────────────────

# Simple cartoon children as inline SVG (uniform-wearing students)
_SVG_CHILDREN = {
    "girl1": '''<svg viewBox="0 0 100 160" width="{w}" height="{h}">
        <circle cx="50" cy="30" r="22" fill="#FFDAB9"/>
        <circle cx="42" cy="26" r="3" fill="#333"/>
        <circle cx="58" cy="26" r="3" fill="#333"/>
        <path d="M44 36 Q50 42 56 36" stroke="#333" fill="none" stroke-width="2"/>
        <path d="M28 15 Q50 -5 72 15 Q75 30 70 35 L65 20 Q50 8 35 20 L30 35 Q25 30 28 15Z" fill="#8B4513"/>
        <rect x="35" y="52" width="30" height="40" rx="5" fill="#1e40af"/>
        <rect x="35" y="52" width="30" height="12" fill="white"/>
        <line x1="50" y1="52" x2="50" y2="64" stroke="#1e40af" stroke-width="1"/>
        <rect x="38" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="52" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="22" y="55" width="13" height="6" rx="3" fill="#FFDAB9"/>
        <rect x="65" y="55" width="13" height="6" rx="3" fill="#FFDAB9"/>
        <rect x="36" y="122" width="12" height="6" rx="3" fill="#333"/>
        <rect x="52" y="122" width="12" height="6" rx="3" fill="#333"/>
    </svg>''',
    "boy1": '''<svg viewBox="0 0 100 160" width="{w}" height="{h}">
        <circle cx="50" cy="30" r="22" fill="#FDDCB5"/>
        <circle cx="42" cy="26" r="3" fill="#333"/>
        <circle cx="58" cy="26" r="3" fill="#333"/>
        <path d="M44 36 Q50 42 56 36" stroke="#333" fill="none" stroke-width="2"/>
        <path d="M30 18 Q50 0 70 18 L68 12 Q50 -2 32 12Z" fill="#4A3728"/>
        <rect x="35" y="52" width="30" height="40" rx="5" fill="#1e40af"/>
        <rect x="35" y="52" width="30" height="12" fill="white"/>
        <line x1="50" y1="52" x2="50" y2="64" stroke="#1e40af" stroke-width="1"/>
        <rect x="38" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="52" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="22" y="55" width="13" height="6" rx="3" fill="#FDDCB5"/>
        <rect x="65" y="55" width="13" height="6" rx="3" fill="#FDDCB5"/>
        <rect x="36" y="122" width="12" height="6" rx="3" fill="#333"/>
        <rect x="52" y="122" width="12" height="6" rx="3" fill="#333"/>
    </svg>''',
    "girl2": '''<svg viewBox="0 0 100 160" width="{w}" height="{h}">
        <circle cx="50" cy="30" r="22" fill="#E8C39E"/>
        <circle cx="42" cy="26" r="3" fill="#333"/>
        <circle cx="58" cy="26" r="3" fill="#333"/>
        <path d="M44 36 Q50 40 56 36" stroke="#333" fill="none" stroke-width="2"/>
        <path d="M26 20 Q50 -8 74 20 Q72 35 68 30 Q60 10 40 10 Q32 35 28 30 Q24 35 26 20Z" fill="#1a1a1a"/>
        <rect x="35" y="52" width="30" height="40" rx="5" fill="#1e40af"/>
        <rect x="35" y="52" width="30" height="12" fill="white"/>
        <line x1="50" y1="52" x2="50" y2="64" stroke="#1e40af" stroke-width="1"/>
        <rect x="38" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="52" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="22" y="55" width="13" height="6" rx="3" fill="#E8C39E"/>
        <rect x="65" y="55" width="13" height="6" rx="3" fill="#E8C39E"/>
        <rect x="36" y="122" width="12" height="6" rx="3" fill="#333"/>
        <rect x="52" y="122" width="12" height="6" rx="3" fill="#333"/>
    </svg>''',
    "boy2": '''<svg viewBox="0 0 100 160" width="{w}" height="{h}">
        <circle cx="50" cy="30" r="22" fill="#D2B48C"/>
        <circle cx="42" cy="26" r="3" fill="#333"/>
        <circle cx="58" cy="26" r="3" fill="#333"/>
        <path d="M46 36 Q50 40 54 36" stroke="#333" fill="none" stroke-width="2"/>
        <path d="M30 15 Q50 -2 70 15 L70 22 Q55 5 35 22Z" fill="#8B0000"/>
        <rect x="35" y="52" width="30" height="40" rx="5" fill="#1e40af"/>
        <rect x="35" y="52" width="30" height="12" fill="white"/>
        <line x1="50" y1="52" x2="50" y2="64" stroke="#1e40af" stroke-width="1"/>
        <rect x="38" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="52" y="92" width="10" height="30" rx="3" fill="#1e3a5f"/>
        <rect x="22" y="55" width="13" height="6" rx="3" fill="#D2B48C"/>
        <rect x="65" y="55" width="13" height="6" rx="3" fill="#D2B48C"/>
        <rect x="36" y="122" width="12" height="6" rx="3" fill="#333"/>
        <rect x="52" y="122" width="12" height="6" rx="3" fill="#333"/>
    </svg>''',
    "teacher": '''<svg viewBox="0 0 100 180" width="{w}" height="{h}">
        <circle cx="50" cy="30" r="22" fill="#FDDCB5"/>
        <circle cx="42" cy="26" r="3" fill="#333"/>
        <circle cx="58" cy="26" r="3" fill="#333"/>
        <path d="M44 36 Q50 42 56 36" stroke="#333" fill="none" stroke-width="2"/>
        <path d="M25 18 Q50 -8 75 18 Q73 35 70 38 L65 15 Q50 2 35 15 L30 38 Q27 35 25 18Z" fill="#C4A882"/>
        <rect x="33" y="52" width="34" height="50" rx="5" fill="#059669"/>
        <rect x="33" y="52" width="34" height="14" fill="white"/>
        <rect x="38" y="102" width="10" height="35" rx="3" fill="#94A3B8"/>
        <rect x="52" y="102" width="10" height="35" rx="3" fill="#94A3B8"/>
        <rect x="20" y="56" width="13" height="6" rx="3" fill="#FDDCB5"/>
        <rect x="67" y="56" width="13" height="6" rx="3" fill="#FDDCB5"/>
        <rect x="36" y="137" width="12" height="6" rx="3" fill="#333"/>
        <rect x="52" y="137" width="12" height="6" rx="3" fill="#333"/>
    </svg>''',
}


def _svg(name: str, w: int = 60, h: int = 96) -> str:
    return _SVG_CHILDREN.get(name, "").replace("{w}", str(w)).replace("{h}", str(h))


def _speech_bubble(text: str, direction: str = "left", color: str = "#fff",
                   border: str = "#94a3b8", onclick_tts: bool = True) -> str:
    """CSS speech bubble with optional TTS on click."""
    arrow_css = "left:15px;" if direction == "left" else "right:15px;"
    tts_attr = f'onclick="speak(\'{text.replace(chr(39), "")}\' )" style="cursor:pointer;"' if onclick_tts else ""
    return f'''<div class="bubble" {tts_attr}>
        <div style="background:{color};border:2px solid {border};border-radius:14px;
            padding:8px 14px;font-size:15px;font-weight:600;position:relative;
            display:inline-block;max-width:220px;">
            {text}
            <div style="position:absolute;bottom:-10px;{arrow_css}
                width:0;height:0;border-left:8px solid transparent;
                border-right:8px solid transparent;border-top:10px solid {border};"></div>
        </div>
    </div>'''


# ── Page Builders ────────────────────────────────────────────────────────────

def _page_header(section: str, number: int, icon: str = "") -> str:
    colors = {
        "Speaking-Expression": ("#be123c", "#fecdd3"),
        "Speaking & Pronunciation": ("#7c2d12", "#fed7aa"),
        "Vocabulary": ("#1e40af", "#dbeafe"),
        "Listening": ("#7c3aed", "#ede9fe"),
        "Reading": ("#059669", "#d1fae5"),
        "Writing": ("#b45309", "#fef3c7"),
        "Grammar": ("#0891b2", "#cffafe"),
        "Fun Activity": ("#d946ef", "#fae8ff"),
    }
    bg, fg = colors.get(section, ("#94A3B8", "#f3f4f6"))
    return f'''<div style="background:{bg};color:white;padding:6px 18px;
        border-radius:0 0 16px 0;display:inline-block;font-size:16px;
        font-weight:800;font-style:italic;margin-bottom:10px;">
        {icon} {section}</div>
    <div style="position:absolute;top:12px;left:12px;width:32px;height:32px;
        border-radius:50%;border:2px solid {bg};display:flex;align-items:center;
        justify-content:center;font-size:16px;font-weight:800;color:{bg};">{number}</div>'''


def _tts_script() -> str:
    return '''<script>
    function speak(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.85; u.pitch = 1.1;
            window.speechSynthesis.speak(u);
        }
    }
    function speakSlow(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.6; u.pitch = 1.0;
            window.speechSynthesis.speak(u);
        }
    }
    </script>'''


def _base_style() -> str:
    return '''<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', sans-serif; }
    .page { width: 100%; min-height: 700px; padding: 20px; position: relative;
            background: #fff; border-radius: 12px; }
    .bubble:hover { transform: scale(1.05); transition: .2s; }
    .vocab-card { display: inline-flex; flex-direction: column; align-items: center;
        background: #f0f9ff; border: 2px solid #93c5fd; border-radius: 12px;
        padding: 10px 14px; margin: 6px; cursor: pointer; transition: .2s;
        min-width: 90px; text-align: center; }
    .vocab-card:hover { background: #dbeafe; transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,.15); }
    .vocab-card .emoji { font-size: 32px; }
    .vocab-card .word { font-size: 14px; font-weight: 700; color: #1e40af; margin-top: 4px; }
    .scene { display: flex; align-items: flex-end; gap: 10px; padding: 16px;
        background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 50%, #fef9c3 100%);
        border-radius: 16px; min-height: 260px; position: relative; }
    .scene-indoor { background: linear-gradient(180deg, #fef3c7 0%, #fff7ed 50%, #f5f5f4 100%); }
    .character { display: flex; flex-direction: column; align-items: center; }
    .activity-box { background: #111827; border: 2px dashed #94a3b8; border-radius: 12px;
        padding: 14px; margin: 10px 0; }
    .listen-btn { display: inline-flex; align-items: center; gap: 6px;
        background: linear-gradient(135deg, #7c3aed, #a855f7); color: white;
        border: none; border-radius: 20px; padding: 8px 16px; cursor: pointer;
        font-size: 14px; font-weight: 600; }
    .listen-btn:hover { transform: scale(1.05); }
    .number-circle { display: inline-flex; align-items: center; justify-content: center;
        width: 28px; height: 28px; border-radius: 50%; border: 2px solid;
        font-weight: 800; font-size: 14px; margin-right: 6px; }
    .teacher-tip { background: #ecfdf5; border-left: 4px solid #059669;
        border-radius: 0 8px 8px 0; padding: 8px 12px; margin: 8px 0;
        font-size: 12px; color: #065f46; }
    </style>'''


# ── BODY PARTS PAGE (Week 7 - "My Body") ────────────────────────────────────

def build_page_body_speaking(week_data: dict | None = None) -> str:
    """Speaking-Expression page: Body parts with 'I've got...' pattern."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">{_base_style()}{_tts_script()}</head>
<body>
<div class="page">
    {_page_header("Speaking-Expression", 6)}

    <h2 style="text-align:center;color:#94A3B8;margin:8px 0 4px;font-size:20px;">
        Let's play together.</h2>
    <div style="display:flex;gap:6px;justify-content:center;margin-bottom:10px;">
        <button class="listen-btn" onclick="speak('Let\\'s play together. I have got two eyes. I have got a nose. What have you got?')">
            Listen</button>
        <div class="teacher-tip" style="display:inline-block;">Teacher's Reminder: Use gestures!</div>
    </div>

    <!-- CLASSROOM SCENE -->
    <div class="scene scene-indoor">
        <!-- Furniture background -->
        <div style="position:absolute;left:10px;bottom:10px;width:60px;height:80px;
            background:#d4a574;border-radius:4px;border:2px solid #92400e;">
            <div style="position:absolute;top:5px;left:5px;right:5px;height:25px;
                background:#fbbf24;border-radius:2px;"></div></div>
        <div style="position:absolute;right:15px;bottom:10px;width:50px;height:90px;
            background:#8B4513;border-radius:2px;">
            <div style="height:20px;background:#60a5fa;margin:5px;border-radius:2px;"></div>
            <div style="height:20px;background:#f87171;margin:5px;border-radius:2px;"></div></div>

        <!-- Characters with speech bubbles -->
        <div class="character" style="margin-left:60px;">
            {_speech_bubble("I've got two ears.", "left", "#fff", "#60a5fa")}
            {_svg("girl1", 55, 88)}
        </div>
        <div class="character">
            {_speech_bubble("I've got a mouth.", "left", "#fff", "#f472b6")}
            {_svg("boy1", 55, 88)}
        </div>
        <div class="character">
            {_speech_bubble("I've got a nose.", "right", "#fff", "#34d399")}
            {_svg("girl2", 55, 88)}
        </div>

        <!-- Interactive question bubbles -->
        <div style="position:absolute;bottom:50px;right:80px;">
            <div class="bubble" onclick="speak('What have you got?')" style="cursor:pointer;">
                <div style="background:#fef3c7;border:2px solid #f59e0b;border-radius:14px;
                    padding:8px 14px;font-size:15px;font-weight:700;">
                    What have you got?</div>
            </div>
        </div>
        <div style="position:absolute;top:30px;right:20px;">
            <div class="bubble" onclick="speak('How many eyes have you got?')" style="cursor:pointer;">
                <div style="background:#dbeafe;border:2px solid #3b82f6;border-radius:14px;
                    padding:8px 14px;font-size:14px;font-weight:600;">
                    How many eyes<br>have you got?</div>
            </div>
        </div>
        <div class="character" style="margin-left:auto;">
            {_speech_bubble("I've got two eyes.", "right", "#fff", "#8b5cf6")}
            {_svg("boy2", 55, 88)}
        </div>
    </div>

    <!-- Vocabulary cards row -->
    <div style="text-align:center;margin-top:14px;">
        <div class="vocab-card" onclick="speak('head')">
            <div class="emoji">&#x1F9D1;</div><div class="word">head</div></div>
        <div class="vocab-card" onclick="speak('eye')">
            <div class="emoji">&#x1F441;</div><div class="word">eye</div></div>
        <div class="vocab-card" onclick="speak('ear')">
            <div class="emoji">&#x1F442;</div><div class="word">ear</div></div>
        <div class="vocab-card" onclick="speak('nose')">
            <div class="emoji">&#x1F443;</div><div class="word">nose</div></div>
        <div class="vocab-card" onclick="speak('mouth')">
            <div class="emoji">&#x1F444;</div><div class="word">mouth</div></div>
        <div class="vocab-card" onclick="speak('hand')">
            <div class="emoji">&#x270B;</div><div class="word">hand</div></div>
        <div class="vocab-card" onclick="speak('foot')">
            <div class="emoji">&#x1F9B6;</div><div class="word">foot</div></div>
        <div class="vocab-card" onclick="speak('arm')">
            <div class="emoji">&#x1F4AA;</div><div class="word">arm</div></div>
        <div class="vocab-card" onclick="speak('leg')">
            <div class="emoji">&#x1F9B5;</div><div class="word">leg</div></div>
        <div class="vocab-card" onclick="speak('finger')">
            <div class="emoji">&#x261D;</div><div class="word">finger</div></div>
    </div>
</div>
</body></html>'''


def build_page_body_pronunciation(week_data: dict | None = None) -> str:
    """Speaking & Pronunciation page: Listen and repeat body parts."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">{_base_style()}{_tts_script()}
<style>
    .word-row {{ display: flex; align-items: center; gap: 12px; padding: 8px 14px;
        background: #111827; border-radius: 10px; margin: 6px 0; cursor: pointer;
        transition: .2s; border: 2px solid transparent; }}
    .word-row:hover {{ background: #eff6ff; border-color: #93c5fd; transform: translateX(4px); }}
    .word-big {{ font-size: 22px; font-weight: 800; color: #1e40af; }}
    .word-phonetic {{ font-size: 14px; color: #6b7280; font-style: italic; }}
    .word-sentence {{ font-size: 13px; color: #94A3B8; }}
    .match-game {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 10px 0; }}
    .match-card {{ background: #f0f9ff; border: 2px solid #93c5fd; border-radius: 10px;
        padding: 12px; text-align: center; cursor: pointer; transition: .2s; }}
    .match-card:hover {{ background: #3b82f6; color: white; border-color: #1e40af; }}
    .match-card.correct {{ background: #059669; color: white; border-color: #047857; }}
</style>
</head>
<body>
<div class="page">
    {_page_header("Speaking & Pronunciation", 7)}

    <h2 style="text-align:center;color:#94A3B8;margin:8px 0 4px;font-size:20px;">
        Listen and repeat together.</h2>

    <div style="display:flex;gap:6px;justify-content:center;margin-bottom:12px;">
        <button class="listen-btn" onclick="speakSlow('head, eye, ear, nose, mouth, hand, foot, arm, leg, finger')">
            Listen All</button>
        <button class="listen-btn" style="background:linear-gradient(135deg,#059669,#34d399);"
            onclick="speak('Touch your head. Touch your nose. Touch your ears.')">
            TPR Commands</button>
    </div>

    <!-- Word list with pronunciation -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">
        <div class="word-row" onclick="speakSlow('head')">
            <span style="font-size:28px;">&#x1F9D1;</span>
            <div><div class="word-big">head</div>
            <div class="word-phonetic">/hed/</div>
            <div class="word-sentence">Touch your <b>head</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('eye')">
            <span style="font-size:28px;">&#x1F441;</span>
            <div><div class="word-big">eye</div>
            <div class="word-phonetic">/aI/</div>
            <div class="word-sentence">I've got two <b>eyes</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('ear')">
            <span style="font-size:28px;">&#x1F442;</span>
            <div><div class="word-big">ear</div>
            <div class="word-phonetic">/Ir/</div>
            <div class="word-sentence">I can hear with my <b>ears</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('nose')">
            <span style="font-size:28px;">&#x1F443;</span>
            <div><div class="word-big">nose</div>
            <div class="word-phonetic">/noUz/</div>
            <div class="word-sentence">This is my <b>nose</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('mouth')">
            <span style="font-size:28px;">&#x1F444;</span>
            <div><div class="word-big">mouth</div>
            <div class="word-phonetic">/maUT/</div>
            <div class="word-sentence">Open your <b>mouth</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('hand')">
            <span style="font-size:28px;">&#x270B;</span>
            <div><div class="word-big">hand</div>
            <div class="word-phonetic">/h&aelig;nd/</div>
            <div class="word-sentence">Clap your <b>hands</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('foot')">
            <span style="font-size:28px;">&#x1F9B6;</span>
            <div><div class="word-big">foot</div>
            <div class="word-phonetic">/fUt/</div>
            <div class="word-sentence">Stamp your <b>feet</b>.</div></div>
        </div>
        <div class="word-row" onclick="speakSlow('arm')">
            <span style="font-size:28px;">&#x1F4AA;</span>
            <div><div class="word-big">arm</div>
            <div class="word-phonetic">/A:rm/</div>
            <div class="word-sentence">Raise your <b>arms</b>.</div></div>
        </div>
    </div>

    <!-- Matching Game -->
    <div style="margin-top:14px;">
        <h3 style="color:#7c3aed;font-size:16px;margin-bottom:6px;">
            <span class="number-circle" style="border-color:#7c3aed;color:#7c3aed;">8</span>
            Match the word to the picture!</h3>
        <div class="match-game" id="matchGame">
            <div class="match-card" onclick="checkMatch(this,'head','&#x1F9D1;')" data-word="head">
                <div style="font-size:36px;">&#x1F9D1;</div><div style="margin-top:4px;">?</div></div>
            <div class="match-card" onclick="checkMatch(this,'eye','&#x1F441;')" data-word="eye">
                <div style="font-size:36px;">&#x1F441;</div><div style="margin-top:4px;">?</div></div>
            <div class="match-card" onclick="checkMatch(this,'hand','&#x270B;')" data-word="hand">
                <div style="font-size:36px;">&#x270B;</div><div style="margin-top:4px;">?</div></div>
            <div class="match-card" onclick="checkMatch(this,'ear','&#x1F442;')" data-word="ear">
                <div style="font-size:36px;">&#x1F442;</div><div style="margin-top:4px;">?</div></div>
            <div class="match-card" onclick="checkMatch(this,'nose','&#x1F443;')" data-word="nose">
                <div style="font-size:36px;">&#x1F443;</div><div style="margin-top:4px;">?</div></div>
            <div class="match-card" onclick="checkMatch(this,'mouth','&#x1F444;')" data-word="mouth">
                <div style="font-size:36px;">&#x1F444;</div><div style="margin-top:4px;">?</div></div>
        </div>
    </div>

    <!-- Song: Head, Shoulders, Knees and Toes -->
    <div style="background:linear-gradient(135deg,#fef3c7,#fff7ed);border:2px solid #f59e0b;
        border-radius:12px;padding:12px 16px;margin-top:12px;">
        <h3 style="color:#92400e;font-size:15px;margin-bottom:6px;">
            Head, Shoulders, Knees and Toes
            <button class="listen-btn" style="font-size:12px;padding:4px 10px;
                background:linear-gradient(135deg,#f59e0b,#fbbf24);"
                onclick="speak('Head, shoulders, knees and toes, knees and toes. Head, shoulders, knees and toes, knees and toes. And eyes and ears and mouth and nose. Head, shoulders, knees and toes, knees and toes.')">
                Sing Along</button></h3>
        <p style="font-size:14px;color:#78350f;line-height:1.6;">
            <b>Head</b>, shoulders, <b>knees</b> and <b>toes</b>, knees and toes.<br>
            <b>Head</b>, shoulders, <b>knees</b> and <b>toes</b>, knees and toes.<br>
            And <b>eyes</b> and <b>ears</b> and <b>mouth</b> and <b>nose</b>.<br>
            <b>Head</b>, shoulders, <b>knees</b> and <b>toes</b>, knees and toes.</p>
    </div>
</div>

<script>
var answers = {{}};
function checkMatch(el, word, emoji) {{
    var input = prompt('Type the word for ' + emoji + ':');
    if (input && input.trim().toLowerCase() === word) {{
        el.classList.add('correct');
        el.querySelector('div:last-child').textContent = word;
        speak('Correct! ' + word);
    }} else {{
        el.style.borderColor = '#dc2626';
        setTimeout(function(){{ el.style.borderColor = '#93c5fd'; }}, 1000);
        speak('Try again!');
    }}
}}
</script>
</body></html>'''


# ── Generic page builder from curriculum ─────────────────────────────────────

def build_activity_pages(grade: int, week_num: int, curriculum_weeks: list) -> list[str]:
    """Build activity book pages for a given week.

    Returns list of HTML strings (each is a full page).
    For Grade 2 week 7 (My Body), returns the EBA-style demo pages.
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break

    if not week_data:
        return []

    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    structure = week_data.get("structure", "")

    # Build vocab emoji map
    _emoji_map = {
        "head": "&#x1F9D1;", "eye": "&#x1F441;", "ear": "&#x1F442;",
        "nose": "&#x1F443;", "mouth": "&#x1F444;", "hand": "&#x270B;",
        "foot": "&#x1F9B6;", "arm": "&#x1F4AA;", "leg": "&#x1F9B5;",
        "finger": "&#x261D;", "hello": "&#x1F44B;", "goodbye": "&#x1F44B;",
        "mother": "&#x1F469;", "father": "&#x1F468;", "sister": "&#x1F467;",
        "brother": "&#x1F466;", "baby": "&#x1F476;", "family": "&#x1F46A;",
        "cat": "&#x1F431;", "dog": "&#x1F436;", "bird": "&#x1F426;",
        "fish": "&#x1F41F;", "apple": "&#x1F34E;", "banana": "&#x1F34C;",
        "milk": "&#x1F95B;", "bread": "&#x1F35E;", "water": "&#x1F4A7;",
        "red": "&#x1F534;", "blue": "&#x1F535;", "green": "&#x1F7E2;",
        "yellow": "&#x1F7E1;", "book": "&#x1F4D5;", "pencil": "&#x270F;",
        "desk": "&#x1F4DA;", "chair": "&#x1FA91;", "school": "&#x1F3EB;",
        "sun": "&#x2600;", "rain": "&#x1F327;", "tree": "&#x1F333;",
        "flower": "&#x1F33B;", "house": "&#x1F3E0;", "car": "&#x1F697;",
        "bus": "&#x1F68C;", "ball": "&#x26BD;", "doll": "&#x1F9F8;",
        "one": "1&#xFE0F;&#x20E3;", "two": "2&#xFE0F;&#x20E3;",
        "three": "3&#xFE0F;&#x20E3;", "four": "4&#xFE0F;&#x20E3;",
        "five": "5&#xFE0F;&#x20E3;",
    }

    # Page 1: Speaking-Expression with scene
    vocab_cards = ""
    for v in vocab[:10]:
        emoji = _emoji_map.get(v, "&#x1F4AC;")
        vocab_cards += f'''<div class="vocab-card" onclick="speak('{v}')">
            <div class="emoji">{emoji}</div><div class="word">{v}</div></div>'''

    # Build character scene with speech bubbles from structure
    phrases = [p.strip() for p in structure.replace("?", "?.").split(".") if p.strip()][:4]
    chars = ["girl1", "boy1", "girl2", "boy2"]
    char_html = ""
    for i, phrase in enumerate(phrases):
        char_html += f'''<div class="character">
            {_speech_bubble(phrase, "left" if i % 2 == 0 else "right")}
            {_svg(chars[i % 4], 50, 80)}
        </div>'''

    page1 = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">{_base_style()}{_tts_script()}</head>
<body>
<div class="page">
    {_page_header("Speaking-Expression", week_num)}
    <h2 style="text-align:center;color:#94A3B8;margin:8px 0;font-size:20px;">
        {theme}</h2>
    <p style="text-align:center;color:#6b7280;font-size:13px;margin-bottom:10px;">{theme_tr}</p>
    <button class="listen-btn" style="display:block;margin:0 auto 10px;"
        onclick="speak('{structure.replace(chr(39), "")}')">Listen</button>
    <div class="scene">{char_html}</div>
    <div style="text-align:center;margin-top:12px;">{vocab_cards}</div>
</div>
</body></html>'''

    # Page 2: Pronunciation + Activity
    word_rows = ""
    for v in vocab[:8]:
        emoji = _emoji_map.get(v, "&#x1F4AC;")
        word_rows += f'''<div class="word-row" onclick="speakSlow('{v}')">
            <span style="font-size:28px;">{emoji}</span>
            <div><div class="word-big">{v}</div>
            <div class="word-sentence">This is my <b>{v}</b>.</div></div>
        </div>'''

    match_cards = ""
    for v in vocab[:6]:
        emoji = _emoji_map.get(v, "&#x1F4AC;")
        match_cards += f'''<div class="match-card" onclick="checkMatch(this,'{v}','{emoji}')" data-word="{v}">
            <div style="font-size:32px;">{emoji}</div><div style="margin-top:4px;">?</div></div>'''

    page2 = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">{_base_style()}{_tts_script()}
<style>
    .word-row {{ display:flex;align-items:center;gap:12px;padding:8px 14px;
        background:#111827;border-radius:10px;margin:6px 0;cursor:pointer;
        transition:.2s;border:2px solid transparent; }}
    .word-row:hover {{ background:#eff6ff;border-color:#93c5fd; }}
    .word-big {{ font-size:20px;font-weight:800;color:#1e40af; }}
    .word-sentence {{ font-size:13px;color:#94A3B8; }}
    .match-game {{ display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0; }}
    .match-card {{ background:#f0f9ff;border:2px solid #93c5fd;border-radius:10px;
        padding:10px;text-align:center;cursor:pointer;transition:.2s; }}
    .match-card:hover {{ background:#3b82f6;color:white; }}
    .match-card.correct {{ background:#059669;color:white;border-color:#047857; }}
</style>
</head>
<body>
<div class="page">
    {_page_header("Speaking & Pronunciation", week_num)}
    <h2 style="text-align:center;color:#94A3B8;margin:8px 0;font-size:18px;">
        Listen and repeat together.</h2>
    <button class="listen-btn" style="display:block;margin:0 auto 10px;"
        onclick="speakSlow('{' '.join(vocab[:8])}')">Listen All</button>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">{word_rows}</div>
    <h3 style="color:#7c3aed;font-size:15px;margin:12px 0 6px;">Match the word!</h3>
    <div class="match-game">{match_cards}</div>
</div>
<script>
function checkMatch(el, word, emoji) {{
    var input = prompt('Type the word:');
    if (input && input.trim().toLowerCase() === word) {{
        el.classList.add('correct');
        el.querySelector('div:last-child').textContent = word;
        speak('Correct! ' + word);
    }} else {{
        el.style.borderColor = '#dc2626';
        setTimeout(function(){{ el.style.borderColor = '#93c5fd'; }}, 1000);
        speak('Try again!');
    }}
}}
</script>
</body></html>'''

    return [page1, page2]
