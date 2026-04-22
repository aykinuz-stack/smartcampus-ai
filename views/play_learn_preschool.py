# -*- coding: utf-8 -*-
"""Play & Learn Book — Okul Öncesi (Preschool) Etkinlik / Pekiştirme Kitabı.

Interactive HTML activity pages for preschool English learners.
Activity types (5 pages per week):
  1. Coloring (Boyama)
  2. Matching (Eşleştirme)
  3. Maze (Labirent)
  4. Line Tracing (Çizgi tamamlama)
  5. Visual Classification (Görsel sınıflandırma)

All content is dynamically generated from curriculum data (vocab, theme).
Each week produces 5 HTML pages — one per activity type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_CFG = {
    "font_size": "20px",
    "color_primary": "#FF6B6B",
    "color_accent": "#FF8E53",
    "color_bg": "#FFF5F5",
    "color_yellow": "#FFD93D",
    "coloring_count": 6,
    "match_count": 6,
    "maze_count": 4,
    "tracing_count": 6,
    "classify_count": 8,
}


# ══════════════════════════════════════════════════════════════════════════════
# EMOJI & SVG MAPS
# ══════════════════════════════════════════════════════════════════════════════

_EMOJI_MAP = {
    "hello": "👋", "hi": "👋", "goodbye": "👋", "bye": "👋",
    "name": "📛", "boy": "👦", "girl": "👧", "friend": "🤝",
    "teacher": "👩‍🏫", "mother": "👩", "father": "👨",
    "sister": "👧", "brother": "👦", "baby": "👶", "family": "👪",
    "school": "🏫", "book": "📕", "pencil": "✏️", "bag": "🎒",
    "red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡",
    "orange": "🟠", "purple": "🟣", "pink": "💗", "black": "⚫",
    "white": "⚪", "brown": "🟤",
    "head": "🧑", "eye": "👁️", "ear": "👂", "nose": "👃",
    "mouth": "👄", "hand": "✋", "foot": "🦶",
    "cat": "🐱", "dog": "🐶", "bird": "🐦", "fish": "🐟",
    "rabbit": "🐰", "horse": "🐴", "cow": "🐄", "sheep": "🐑",
    "chicken": "🐔", "duck": "🦆", "frog": "🐸", "bee": "🐝",
    "apple": "🍎", "banana": "🍌", "milk": "🥛", "bread": "🍞",
    "water": "💧", "juice": "🧃", "cake": "🎂", "pizza": "🍕",
    "sun": "☀️", "rain": "🌧️", "tree": "🌳", "flower": "🌻",
    "house": "🏠", "car": "🚗", "bus": "🚌", "ball": "⚽",
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣",
    "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣",
    "big": "🔺", "small": "🔹", "happy": "😊", "sad": "😢",
    "hot": "🔥", "cold": "❄️",
    "shirt": "👕", "dress": "👗", "shoes": "👟", "hat": "🎩",
    "run": "🏃", "jump": "🤸", "swim": "🏊", "sing": "🎤",
    "dance": "💃", "play": "🎮", "eat": "🍽️", "sleep": "😴",
    "star": "⭐", "heart": "❤️", "circle": "⭕", "square": "🟧",
    "triangle": "🔺", "diamond": "💎",
    "park": "🌳", "garden": "🌷", "farm": "🐄", "zoo": "🦁",
    "morning": "🌅", "night": "🌙",
    "toy": "🧸", "teddy": "🧸", "doll": "🪆", "kite": "🪁",
    "balloon": "🎈", "cake": "🎂", "party": "🎉",
}

# Categories for visual classification
_CATEGORIES = {
    "animals": {"emoji": "🐾", "members": ["cat", "dog", "bird", "fish", "rabbit", "horse", "cow", "sheep", "duck", "frog"]},
    "food": {"emoji": "🍽️", "members": ["apple", "banana", "bread", "pizza", "cake", "milk", "juice", "water", "egg", "cheese"]},
    "colors": {"emoji": "🎨", "members": ["red", "blue", "green", "yellow", "orange", "purple", "pink", "black", "white", "brown"]},
    "body": {"emoji": "🧑", "members": ["head", "eye", "ear", "nose", "mouth", "hand", "foot"]},
    "transport": {"emoji": "🚗", "members": ["car", "bus", "bicycle", "train", "boat", "plane"]},
    "nature": {"emoji": "🌿", "members": ["sun", "rain", "tree", "flower", "star", "moon"]},
    "toys": {"emoji": "🧸", "members": ["ball", "teddy", "doll", "kite", "balloon", "toy"]},
    "clothes": {"emoji": "👕", "members": ["shirt", "dress", "shoes", "hat", "jacket", "socks"]},
}

# Simple SVG shapes for coloring
_SVG_SHAPES = {
    "cat": '<circle cx="50" cy="40" r="28" /><polygon points="30,15 25,0 40,12" /><polygon points="70,15 75,0 60,12" /><circle cx="40" cy="36" r="3" fill="#333"/><circle cx="60" cy="36" r="3" fill="#333"/><ellipse cx="50" cy="46" rx="4" ry="3" fill="#333"/>',
    "dog": '<circle cx="50" cy="42" r="26" /><ellipse cx="30" cy="22" rx="10" ry="14" /><ellipse cx="70" cy="22" rx="10" ry="14" /><circle cx="42" cy="38" r="3" fill="#333"/><circle cx="58" cy="38" r="3" fill="#333"/><ellipse cx="50" cy="48" rx="5" ry="3" fill="#333"/>',
    "fish": '<ellipse cx="50" cy="50" rx="35" ry="20" /><polygon points="85,50 100,35 100,65" /><circle cx="35" cy="45" r="3" fill="#333"/>',
    "star": '<polygon points="50,5 61,35 95,35 67,55 78,90 50,68 22,90 33,55 5,35 39,35" />',
    "flower": '<circle cx="50" cy="50" r="12" fill="#FFD93D"/><ellipse cx="50" cy="28" rx="10" ry="14" /><ellipse cx="50" cy="72" rx="10" ry="14" /><ellipse cx="28" cy="50" rx="14" ry="10" /><ellipse cx="72" cy="50" rx="14" ry="10" /><ellipse cx="34" cy="34" rx="10" ry="14" transform="rotate(-45,34,34)" /><ellipse cx="66" cy="34" rx="10" ry="14" transform="rotate(45,66,34)" /><ellipse cx="34" cy="66" rx="10" ry="14" transform="rotate(45,34,66)" /><ellipse cx="66" cy="66" rx="10" ry="14" transform="rotate(-45,66,66)" />',
    "house": '<rect x="20" y="40" width="60" height="45" /><polygon points="10,42 50,10 90,42" /><rect x="40" y="55" width="18" height="30" fill="#8B4513"/><rect x="25" y="50" width="12" height="12" fill="#87CEEB"/><rect x="62" y="50" width="12" height="12" fill="#87CEEB"/>',
    "tree": '<rect x="42" y="55" width="16" height="35" fill="#8B4513"/><circle cx="50" cy="35" r="28" />',
    "ball": '<circle cx="50" cy="50" r="35" /><path d="M 20,35 Q 50,20 80,35" fill="none" stroke="#333" stroke-width="2"/><path d="M 20,65 Q 50,80 80,65" fill="none" stroke="#333" stroke-width="2"/>',
    "apple": '<circle cx="50" cy="55" r="28" /><path d="M 50,28 Q 55,15 60,20" fill="none" stroke="#228B22" stroke-width="3"/><ellipse cx="55" cy="22" rx="8" ry="5" fill="#228B22"/>',
    "car": '<rect x="15" y="45" width="70" height="25" rx="5" /><path d="M 30,45 L 35,28 L 65,28 L 70,45" /><circle cx="30" cy="72" r="8" fill="#333"/><circle cx="70" cy="72" r="8" fill="#333"/><rect x="38" y="32" width="10" height="12" fill="#87CEEB"/><rect x="52" y="32" width="10" height="12" fill="#87CEEB"/>',
}

# Fallback shape
_DEFAULT_SHAPE = '<circle cx="50" cy="50" r="35" />'


def _emoji(word: str) -> str:
    return _EMOJI_MAP.get(word.lower().strip(), "📝")


def _deterministic_seed(week: int) -> int:
    return int(hashlib.md5(f"plb_preschool_{week}".encode()).hexdigest()[:8], 16)


def _get_svg(word: str) -> str:
    return _SVG_SHAPES.get(word.lower().strip(), _DEFAULT_SHAPE)


# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE for coloring activity
# ══════════════════════════════════════════════════════════════════════════════

_COLOR_PALETTE = [
    ("#FF6B6B", "Red"), ("#4ECDC4", "Green"), ("#45B7D1", "Blue"),
    ("#FFD93D", "Yellow"), ("#FF8E53", "Orange"), ("#A78BFA", "Purple"),
    ("#F472B6", "Pink"), ("#8B5CF6", "Violet"), ("#34D399", "Mint"),
    ("#FBBF24", "Gold"), ("#F87171", "Coral"), ("#60A5FA", "Sky Blue"),
]


# ══════════════════════════════════════════════════════════════════════════════
# ACTIVITY GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def _build_coloring(vocab: list, seed: int) -> str:
    """Activity 1: Color the pictures — click a color then click the shape."""
    rng = random.Random(seed)
    words = vocab[:_CFG["coloring_count"]]
    rng.shuffle(words)

    palette_html = ""
    for color_hex, color_name in _COLOR_PALETTE:
        palette_html += (
            f'<div class="color-swatch" style="background:{color_hex};" '
            f'onclick="selectColor(\'{color_hex}\',\'{color_name}\')" '
            f'title="{color_name}"></div>'
        )

    items_html = ""
    for i, w in enumerate(words):
        svg_inner = _get_svg(w)
        items_html += f'''<div class="color-card">
            <svg viewBox="0 0 100 90" class="color-svg" data-word="{w}"
                 onclick="applyColor(this)" style="cursor:pointer;">
                <g class="colorable" fill="#E5E7EB" stroke="#94A3B8" stroke-width="2">
                    {svg_inner}
                </g>
            </svg>
            <div class="color-label" onclick="speak('{w}')">{_emoji(w)} {w}</div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#FF6B6B;">
        <div class="section-title" style="background:linear-gradient(135deg,#FF6B6B,#FF8E53);">
            <span class="section-icon">🎨</span> Colour the Pictures!</div>
        <div class="color-palette">{palette_html}</div>
        <div class="color-grid">{items_html}</div>
        <div class="color-hint">👆 Pick a colour, then tap a picture to colour it!</div>
    </div>'''


def _build_matching(vocab: list, seed: int) -> str:
    """Activity 2: Match the word to the emoji/picture — drag-style click match."""
    rng = random.Random(seed + 1)
    words = vocab[:_CFG["match_count"]]
    shuffled = list(words)
    rng.shuffle(shuffled)

    left_col = ""
    for i, w in enumerate(words):
        left_col += (
            f'<div class="match-item match-left" data-pair="{w}" '
            f'onclick="selectMatch(this,\'{w}\',\'left\')">'
            f'<span class="q-num">{i+1}</span> '
            f'<span style="font-size:36px;">{_emoji(w)}</span></div>'
        )

    right_col = ""
    for i, w in enumerate(shuffled):
        letter = chr(65 + i)
        right_col += (
            f'<div class="match-item match-right" data-pair="{w}" '
            f'onclick="selectMatch(this,\'{w}\',\'right\')">'
            f'<span class="match-letter">{letter}</span> '
            f'<span style="font-size:18px;font-weight:700;">{w}</span></div>'
        )

    return f'''
    <div class="section-box" style="border-color:#4ECDC4;">
        <div class="section-title" style="background:linear-gradient(135deg,#059669,#34d399);">
            <span class="section-icon">🔗</span> Match the Pictures to Words!</div>
        <div class="match-grid">
            <div class="match-column">{left_col}</div>
            <div class="match-column">{right_col}</div>
        </div>
    </div>'''


def _build_maze(vocab: list, theme: str, seed: int) -> str:
    """Activity 3: Simple maze — follow the correct path by clicking steps."""
    rng = random.Random(seed + 2)
    target_word = vocab[0] if vocab else "star"
    target_emoji = _emoji(target_word)

    # Generate a simple grid maze path
    grid_size = 5
    # Create a path from top-left to bottom-right
    path = [(0, 0)]
    x, y = 0, 0
    rng2 = random.Random(seed + 20)
    while x < grid_size - 1 or y < grid_size - 1:
        moves = []
        if x < grid_size - 1:
            moves.append((x + 1, y))
        if y < grid_size - 1:
            moves.append((x, y + 1))
        if moves:
            x, y = rng2.choice(moves)
            path.append((x, y))
    path_set = set(path)

    # Create distractors (wrong words)
    other_words = [w for w in vocab[1:] if w != target_word][:3]

    cells_html = ""
    for row in range(grid_size):
        for col in range(grid_size):
            is_path = (col, row) in path_set
            is_start = (col == 0 and row == 0)
            is_end = (col == grid_size - 1 and row == grid_size - 1)

            if is_start:
                cell_content = "🚀"
                extra_class = "maze-start"
            elif is_end:
                cell_content = target_emoji
                extra_class = "maze-end"
            elif is_path:
                cell_content = _emoji(target_word)
                extra_class = "maze-path"
            else:
                # Distractor cell
                dw = rng.choice(other_words) if other_words else "x"
                cell_content = _emoji(dw)
                extra_class = "maze-wall"

            cells_html += (
                f'<div class="maze-cell {extra_class}" '
                f'data-correct="{"1" if is_path else "0"}" '
                f'onclick="clickMaze(this)">'
                f'{cell_content}</div>'
            )

    # Multiple mazes
    mazes_html = ""
    for m_idx in range(_CFG["maze_count"]):
        m_seed = seed + 200 + m_idx * 37
        m_rng = random.Random(m_seed)
        m_word = vocab[m_idx % len(vocab)] if vocab else "star"
        m_emoji = _emoji(m_word)
        m_others = [w for w in vocab if w != m_word][:3]

        m_path = [(0, 0)]
        mx, my = 0, 0
        while mx < grid_size - 1 or my < grid_size - 1:
            m_moves = []
            if mx < grid_size - 1:
                m_moves.append((mx + 1, my))
            if my < grid_size - 1:
                m_moves.append((mx, my + 1))
            if m_moves:
                mx, my = m_rng.choice(m_moves)
                m_path.append((mx, my))
        m_path_set = set(m_path)

        m_cells = ""
        for row in range(grid_size):
            for col in range(grid_size):
                is_p = (col, row) in m_path_set
                is_s = (col == 0 and row == 0)
                is_e = (col == grid_size - 1 and row == grid_size - 1)
                if is_s:
                    cc = "🚀"
                    ec = "maze-start"
                elif is_e:
                    cc = m_emoji
                    ec = "maze-end"
                elif is_p:
                    cc = m_emoji
                    ec = "maze-path"
                else:
                    dw2 = m_rng.choice(m_others) if m_others else "❌"
                    cc = _emoji(dw2) if m_others else "❌"
                    ec = "maze-wall"

                m_cells += (
                    f'<div class="maze-cell {ec}" '
                    f'data-correct="{"1" if is_p else "0"}" '
                    f'onclick="clickMaze(this)">{cc}</div>'
                )

        mazes_html += f'''<div class="maze-box">
            <div class="maze-label">Find the {m_word}! {m_emoji}</div>
            <div class="maze-grid">{m_cells}</div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#45B7D1;">
        <div class="section-title" style="background:linear-gradient(135deg,#1e40af,#3b82f6);">
            <span class="section-icon">🧩</span> Follow the Path!</div>
        <div class="maze-hint">🚀 Start → Follow the matching pictures → Reach the goal!</div>
        <div class="mazes-container">{mazes_html}</div>
    </div>'''


def _build_tracing(vocab: list, seed: int) -> str:
    """Activity 4: Letter/word tracing — trace the dotted letters."""
    rng = random.Random(seed + 3)
    words = vocab[:_CFG["tracing_count"]]

    rows_html = ""
    for i, w in enumerate(words):
        em = _emoji(w)
        # Create letter boxes for tracing
        letters_html = ""
        for ch in w.upper():
            if ch == " ":
                letters_html += '<span class="trace-space">&nbsp;</span>'
            else:
                letters_html += (
                    f'<div class="trace-letter-box">'
                    f'<span class="trace-guide">{ch}</span>'
                    f'<input type="text" class="trace-input" maxlength="1" '
                    f'data-answer="{ch.lower()}" '
                    f'onkeyup="checkTrace(this)" placeholder="·">'
                    f'</div>'
                )

        rows_html += f'''<div class="trace-row">
            <span style="font-size:40px;min-width:50px;text-align:center;">{em}</span>
            <div class="trace-word">
                <div class="trace-label">{w}</div>
                <div class="trace-letters">{letters_html}</div>
            </div>
            <button class="hint-btn" onclick="speak('{w}')">🔊</button>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#A78BFA;">
        <div class="section-title" style="background:linear-gradient(135deg,#7c3aed,#a78bfa);">
            <span class="section-icon">✍️</span> Trace the Letters!</div>
        <div class="trace-hint">👆 Look at the dotted letter and type it below!</div>
        {rows_html}
    </div>'''


def _build_classification(vocab: list, seed: int) -> str:
    """Activity 5: Visual classification — sort items into correct groups."""
    rng = random.Random(seed + 4)

    # Find 2 categories that have vocab overlap
    cat_scores = []
    for cat_name, cat_data in _CATEGORIES.items():
        overlap = [w for w in vocab if w.lower() in cat_data["members"]]
        cat_scores.append((cat_name, len(overlap), overlap))
    cat_scores.sort(key=lambda x: -x[1])

    # Pick best 2 categories
    if len(cat_scores) >= 2 and cat_scores[0][1] > 0:
        cat1_name = cat_scores[0][0]
        cat2_name = cat_scores[1][0] if cat_scores[1][1] > 0 else list(_CATEGORIES.keys())[1]
    else:
        cat1_name = "animals"
        cat2_name = "food"

    cat1 = _CATEGORIES[cat1_name]
    cat2 = _CATEGORIES[cat2_name]

    # Build items from both categories
    items_cat1 = [w for w in vocab if w.lower() in cat1["members"]]
    items_cat2 = [w for w in vocab if w.lower() in cat2["members"]]

    # Fill up if not enough from vocab
    if len(items_cat1) < 3:
        extras = [m for m in cat1["members"] if m not in items_cat1][:4 - len(items_cat1)]
        items_cat1.extend(extras)
    if len(items_cat2) < 3:
        extras = [m for m in cat2["members"] if m not in items_cat2][:4 - len(items_cat2)]
        items_cat2.extend(extras)

    items_cat1 = items_cat1[:4]
    items_cat2 = items_cat2[:4]

    all_items = [(w, cat1_name) for w in items_cat1] + [(w, cat2_name) for w in items_cat2]
    rng.shuffle(all_items)

    items_html = ""
    for w, cat in all_items:
        items_html += (
            f'<div class="classify-item" data-category="{cat}" '
            f'onclick="classifyItem(this,\'{cat}\')">'
            f'<span style="font-size:36px;">{_emoji(w)}</span>'
            f'<span class="classify-word">{w}</span>'
            f'</div>'
        )

    return f'''
    <div class="section-box" style="border-color:#F59E0B;">
        <div class="section-title" style="background:linear-gradient(135deg,#B45309,#F59E0B);">
            <span class="section-icon">📦</span> Sort the Pictures!</div>
        <div class="classify-hint">👆 Tap each picture to put it in the right group!</div>
        <div class="classify-bins">
            <div class="classify-bin" id="bin_{cat1_name}">
                <div class="bin-header">{cat1["emoji"]} {cat1_name.title()}</div>
                <div class="bin-items" id="bin_items_{cat1_name}"></div>
                <div class="bin-count"><span id="count_{cat1_name}">0</span> / {len(items_cat1)}</div>
            </div>
            <div class="classify-bin" id="bin_{cat2_name}">
                <div class="bin-header">{cat2["emoji"]} {cat2_name.title()}</div>
                <div class="bin-items" id="bin_items_{cat2_name}"></div>
                <div class="bin-count"><span id="count_{cat2_name}">0</span> / {len(items_cat2)}</div>
            </div>
        </div>
        <div class="classify-items-pool">{items_html}</div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _play_styles() -> str:
    cp = _CFG["color_primary"]
    ca = _CFG["color_accent"]
    cb = _CFG["color_bg"]
    cy = _CFG["color_yellow"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Comic Sans MS','Chalkboard SE','Segoe UI',sans-serif;
           font-size:{_CFG["font_size"]}; background:{cb}; }}
    .page {{ max-width:820px; margin:0 auto; padding:16px; }}

    /* Header */
    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:18px; padding:20px 24px; margin-bottom:16px;
        text-align:center; position:relative; overflow:hidden; }}
    .book-header h1 {{ font-size:24px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:14px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.25); padding:5px 14px; border-radius:20px;
        font-size:12px; font-weight:700; }}

    /* Score bar */
    .score-bar {{ background:#fff; border:3px solid {cy}; border-radius:14px;
        padding:10px 18px; margin-bottom:14px; display:flex;
        justify-content:space-between; align-items:center; }}
    .score-bar .stars {{ font-size:22px; }}
    .score-bar .counter {{ font-weight:800; color:{cp}; font-size:17px; }}

    /* Section boxes */
    .section-box {{ background:#fff; border:3px solid #ddd; border-radius:16px;
        margin-bottom:16px; overflow:hidden; }}
    .section-title {{ color:#fff; padding:12px 18px; font-weight:800;
        font-size:16px; display:flex; align-items:center; gap:8px; }}
    .section-icon {{ font-size:20px; }}
    .q-num {{ background:{cp}; color:#fff; width:28px; height:28px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:14px; flex-shrink:0; }}

    /* Coloring */
    .color-palette {{ display:flex; gap:8px; padding:12px 16px; flex-wrap:wrap;
        background:#111827; border-bottom:2px solid #e2e8f0; justify-content:center; }}
    .color-swatch {{ width:36px; height:36px; border-radius:50%; cursor:pointer;
        border:3px solid transparent; transition:.2s;
        box-shadow:0 2px 4px rgba(0,0,0,.15); }}
    .color-swatch:hover {{ transform:scale(1.15); }}
    .color-swatch.selected {{ border-color:#333; transform:scale(1.2);
        box-shadow:0 0 0 3px rgba(0,0,0,.2); }}
    .color-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px;
        padding:16px; }}
    .color-card {{ text-align:center; padding:10px; border:2px solid #e2e8f0;
        border-radius:14px; transition:.2s; cursor:pointer; }}
    .color-card:hover {{ border-color:{ca}; transform:scale(1.03); }}
    .color-svg {{ width:100%; max-width:120px; height:auto; }}
    .color-label {{ font-weight:700; font-size:14px; color:#475569; margin-top:6px;
        cursor:pointer; }}
    .color-label:hover {{ color:{cp}; }}
    .color-hint {{ text-align:center; padding:10px; font-size:13px; color:#94a3b8;
        font-style:italic; }}

    /* Matching */
    .match-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px;
        padding:14px 18px; }}
    .match-column {{ display:flex; flex-direction:column; gap:10px; }}
    .match-item {{ padding:12px 16px; border:3px solid #e2e8f0; border-radius:14px;
        cursor:pointer; transition:.2s; display:flex; align-items:center; gap:10px;
        font-weight:700; background:#fff; }}
    .match-item:hover {{ border-color:{ca}; background:{cb}; }}
    .match-item.selected {{ border-color:{cp}; background:{cb};
        box-shadow:0 0 0 3px {ca}44; }}
    .match-item.correct {{ border-color:#059669; background:#ecfdf5; }}
    .match-item.wrong {{ border-color:#dc2626; background:#fef2f2; }}
    .match-letter {{ background:#e2e8f0; width:28px; height:28px; border-radius:50%;
        display:inline-flex; align-items:center; justify-content:center;
        font-weight:800; font-size:13px; color:#475569; }}

    /* Maze */
    .mazes-container {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; padding:14px; }}
    .maze-box {{ border:2px solid #e2e8f0; border-radius:12px; padding:10px;
        text-align:center; }}
    .maze-label {{ font-weight:700; font-size:14px; color:#1e40af; margin-bottom:8px; }}
    .maze-grid {{ display:grid; grid-template-columns:repeat(5,1fr); gap:4px;
        max-width:220px; margin:0 auto; }}
    .maze-cell {{ width:40px; height:40px; border:2px solid #e2e8f0; border-radius:8px;
        display:flex; align-items:center; justify-content:center; font-size:20px;
        cursor:pointer; transition:.2s; background:#fff; }}
    .maze-cell:hover {{ background:#f0f9ff; }}
    .maze-cell.maze-start {{ background:#dbeafe; border-color:#3b82f6; }}
    .maze-cell.maze-end {{ background:#fef3c7; border-color:#f59e0b; }}
    .maze-cell.clicked-correct {{ background:#dcfce7; border-color:#059669; }}
    .maze-cell.clicked-wrong {{ background:#fef2f2; border-color:#dc2626; opacity:.5; }}
    .maze-hint {{ text-align:center; padding:10px; font-size:13px; color:#64748b; }}

    /* Tracing */
    .trace-row {{ padding:14px 18px; border-bottom:1px solid #1A2035;
        display:flex; align-items:center; gap:14px; }}
    .trace-row:last-child {{ border-bottom:none; }}
    .trace-word {{ flex:1; }}
    .trace-label {{ font-weight:700; color:#7c3aed; font-size:14px; margin-bottom:6px; }}
    .trace-letters {{ display:flex; gap:5px; flex-wrap:wrap; }}
    .trace-letter-box {{ position:relative; width:40px; height:48px; }}
    .trace-guide {{ position:absolute; top:2px; left:50%; transform:translateX(-50%);
        font-size:32px; font-weight:800; color:#e2e8f0; pointer-events:none;
        font-family:monospace; }}
    .trace-input {{ width:40px; height:48px; border:2px dashed #a78bfa;
        border-radius:8px; text-align:center; font-weight:800; font-size:24px;
        color:#7c3aed; background:transparent; outline:none;
        text-transform:uppercase; position:relative; z-index:1; }}
    .trace-input:focus {{ border-color:#7c3aed; background:rgba(167,139,250,.08); }}
    .trace-input.correct {{ border-color:#059669; color:#059669; background:#ecfdf5; }}
    .trace-input.wrong {{ border-color:#dc2626; background:#fef2f2; }}
    .trace-space {{ width:14px; }}
    .trace-hint {{ text-align:center; padding:10px; font-size:13px; color:#94a3b8; }}
    .hint-btn {{ background:none; border:none; font-size:24px; cursor:pointer;
        transition:.2s; }}
    .hint-btn:hover {{ transform:scale(1.2); }}

    /* Classification */
    .classify-bins {{ display:grid; grid-template-columns:1fr 1fr; gap:14px;
        padding:14px 18px; }}
    .classify-bin {{ border:3px dashed #cbd5e1; border-radius:14px; padding:12px;
        min-height:120px; text-align:center; transition:.3s; }}
    .classify-bin.highlight {{ border-color:{cy}; background:#fffbeb; }}
    .bin-header {{ font-weight:800; font-size:16px; color:#475569; margin-bottom:8px; }}
    .bin-items {{ display:flex; flex-wrap:wrap; gap:6px; justify-content:center;
        min-height:40px; }}
    .bin-count {{ font-size:12px; color:#94a3b8; margin-top:6px; }}
    .classify-items-pool {{ display:flex; flex-wrap:wrap; gap:10px; padding:14px 18px;
        justify-content:center; }}
    .classify-item {{ background:#f0f9ff; border:3px solid #93c5fd; border-radius:14px;
        padding:10px 16px; text-align:center; cursor:pointer; transition:.2s;
        min-width:80px; }}
    .classify-item:hover {{ transform:scale(1.08); border-color:#3b82f6; }}
    .classify-item.sorted {{ opacity:.3; pointer-events:none; transform:scale(.9); }}
    .classify-word {{ display:block; font-weight:700; font-size:13px; color:#1e40af;
        margin-top:4px; }}
    .classify-hint {{ text-align:center; padding:10px; font-size:13px; color:#64748b; }}

    /* Vocab review */
    .vocab-review {{ display:flex; flex-wrap:wrap; gap:10px; padding:14px 16px;
        justify-content:center; }}
    .vocab-card {{ background:#f0f9ff; border:2px solid #93c5fd; border-radius:12px;
        padding:10px 16px; text-align:center; cursor:pointer; transition:.2s;
        min-width:80px; }}
    .vocab-card:hover {{ transform:scale(1.08); }}

    /* Animations */
    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.2)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-6px)}} 75%{{transform:translateX(6px)}} }}
    .shake {{ animation:shake .3s ease; }}
    @keyframes bounce {{ 0%{{transform:translateY(0)}} 50%{{transform:translateY(-8px)}} 100%{{transform:translateY(0)}} }}
    .bounce {{ animation:bounce .4s ease; }}
    </style>'''


def _play_scripts() -> str:
    return '''<script>
    var totalScore = 0, totalQuestions = 0;

    function updateScore(correct) {
        totalQuestions++;
        if (correct) totalScore++;
        var pct = totalQuestions > 0 ? Math.round(totalScore / totalQuestions * 100) : 0;
        var el = document.getElementById('scoreCounter');
        if (el) el.textContent = totalScore + ' / ' + totalQuestions + ' (' + pct + '%)';
        var stars = document.getElementById('scoreStars');
        if (stars) {
            stars.textContent = pct >= 90 ? '⭐⭐⭐' : pct >= 70 ? '⭐⭐' : pct >= 40 ? '⭐' : '';
        }
    }

    /* TTS */
    function speak(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.75; u.pitch = 1.2;
            window.speechSynthesis.speak(u);
        }
    }

    /* Coloring */
    var selectedColor = null;
    function selectColor(hex, name) {
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        event.target.classList.add('selected');
        selectedColor = hex;
        speak(name);
    }
    function applyColor(svg) {
        if (!selectedColor) { alert('Pick a colour first! 🎨'); return; }
        var g = svg.querySelector('.colorable');
        if (g) {
            g.setAttribute('fill', selectedColor);
            svg.classList.add('pop');
            setTimeout(() => svg.classList.remove('pop'), 300);
            speak(svg.dataset.word);
        }
    }

    /* Matching */
    var matchSel = {left:null, right:null, leftEl:null, rightEl:null};
    function selectMatch(el, word, side) {
        if (el.classList.contains('correct')) return;
        document.querySelectorAll('.match-'+side).forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        matchSel[side] = word;
        matchSel[side+'El'] = el;
        if (matchSel.left && matchSel.right) {
            if (matchSel.left === matchSel.right) {
                matchSel.leftEl.classList.add('correct','pop');
                matchSel.rightEl.classList.add('correct','pop');
                updateScore(true);
                speak('Great!');
            } else {
                matchSel.leftEl.classList.add('wrong','shake');
                matchSel.rightEl.classList.add('wrong','shake');
                updateScore(false);
                setTimeout(() => {
                    matchSel.leftEl.classList.remove('wrong','shake','selected');
                    matchSel.rightEl.classList.remove('wrong','shake','selected');
                }, 600);
            }
            matchSel = {left:null, right:null, leftEl:null, rightEl:null};
        }
    }

    /* Maze */
    function clickMaze(el) {
        if (el.classList.contains('clicked-correct') || el.classList.contains('clicked-wrong')) return;
        if (el.dataset.correct === '1') {
            el.classList.add('clicked-correct','bounce');
            updateScore(true);
        } else {
            el.classList.add('clicked-wrong','shake');
            updateScore(false);
        }
    }

    /* Tracing */
    function checkTrace(el) {
        var val = el.value.toLowerCase().trim();
        var ans = el.dataset.answer.toLowerCase();
        if (!val) { el.classList.remove('correct','wrong'); return; }
        if (val === ans) {
            el.classList.remove('wrong');
            el.classList.add('correct');
            el.disabled = true;
            var next = el.closest('.trace-letters').querySelector('input:not([disabled])');
            if (next) next.focus();
            else { updateScore(true); speak('Well done!'); }
        } else {
            el.classList.remove('correct');
            el.classList.add('wrong','shake');
            setTimeout(() => { el.classList.remove('shake'); el.value=''; }, 500);
        }
    }

    /* Classification */
    var classifyCounts = {};
    function classifyItem(el, correctCat) {
        if (el.classList.contains('sorted')) return;
        var cat = el.dataset.category;
        if (cat === correctCat) {
            el.classList.add('sorted','pop');
            var binItems = document.getElementById('bin_items_' + cat);
            if (binItems) {
                var clone = document.createElement('span');
                clone.style.fontSize = '28px';
                clone.textContent = el.querySelector('span').textContent;
                clone.classList.add('bounce');
                binItems.appendChild(clone);
            }
            classifyCounts[cat] = (classifyCounts[cat] || 0) + 1;
            var countEl = document.getElementById('count_' + cat);
            if (countEl) countEl.textContent = classifyCounts[cat];
            updateScore(true);
            speak('Correct!');
        } else {
            el.classList.add('shake');
            setTimeout(() => el.classList.remove('shake'), 400);
            updateScore(false);
        }
    }
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# VOCAB REVIEW
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocab_review(vocab: list) -> str:
    html = '<div class="section-box" style="border-color:#FFD93D;">'
    html += '<div class="section-title" style="background:linear-gradient(135deg,#F59E0B,#FFD93D);">'
    html += '<span class="section-icon">📚</span> This Week\'s Words — Tap to Listen!</div>'
    html += '<div class="vocab-review">'
    for v in vocab:
        em = _emoji(v)
        html += (
            f'<div class="vocab-card" onclick="speak(\'{v}\')">'
            f'<div style="font-size:36px;">{em}</div>'
            f'<div style="font-weight:700;color:#B45309;font-size:15px;'
            f'margin-top:4px;">{v}</div></div>'
        )
    html += '</div></div>'
    return html


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_TITLES = [
    "🎨 Colour the Pictures",
    "🔗 Match Words & Pictures",
    "🧩 Follow the Path",
    "✍️ Trace the Letters",
    "📦 Sort the Pictures",
]


def build_play_learn_pages(week_num: int, curriculum_weeks: list) -> list[str]:
    """Build Play & Learn Book pages for a given week.

    Args:
        week_num: 1-36
        curriculum_weeks: Full preschool curriculum list

    Returns:
        List of 5 HTML strings — one page per activity type:
        Page 1: Coloring
        Page 2: Matching
        Page 3: Maze
        Page 4: Letter Tracing
        Page 5: Visual Classification
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    vocab = week_data.get("vocab", [])
    if not vocab:
        return []

    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(week_num)

    unit_num = max(1, (week_num - 1) // 4 + 1)

    styles = _play_styles()
    scripts = _play_scripts()
    vocab_review = _build_vocab_review(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">Preschool</div>
            <h1>🎈 Play & Learn — Unit {unit_num}</h1>
            <div class="subtitle">{theme} — {theme_tr} | Week {week_num} | Page {page_num}/5</div>
            <div style="font-size:12px;opacity:.7;margin-top:2px;">{_PAGE_TITLES[page_num - 1]}</div>
        </div>
        <div class="score-bar">
            <div><b>🎯 Score:</b> <span class="counter" id="scoreCounter">0 / 0</span></div>
            <div class="stars" id="scoreStars"></div>
        </div>'''

    def _wrap(page_num: int, body: str) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{styles}{scripts}</head>
<body>
<div class="page">
    {_header(page_num)}
    {vocab_review}
    {body}
</div>
</body></html>'''

    page1 = _wrap(1, _build_coloring(vocab, seed))
    page2 = _wrap(2, _build_matching(vocab, seed))
    page3 = _wrap(3, _build_maze(vocab, theme, seed))
    page4 = _wrap(4, _build_tracing(vocab, seed))
    page5 = _wrap(5, _build_classification(vocab, seed))

    return [page1, page2, page3, page4, page5]


def build_full_play_learn_book(curriculum_weeks: list,
                                selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Play & Learn Book for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_play_learn_pages(wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
