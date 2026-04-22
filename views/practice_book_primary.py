# -*- coding: utf-8 -*-
"""Practice Book (Alıştırma / Pekiştirme Kitabı) — Grades 1-4.

Generates interactive HTML exercise pages for each unit/week.
Exercise types:
  1. Fill in the blanks (Boşluk doldurma)
  2. Matching (Eşleştirme)
  3. Word completion (Kelime tamamlama)
  4. True / False (Doğru-yanlış)
  5. Mini Quiz (Kısa test)

All content is dynamically generated from curriculum data (vocab, structure, theme).
Each week produces 5 HTML pages — one per exercise type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# GRADE-LEVEL CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_GRADE_CFG = {
    1: {"label": "1st Grade", "font_size": "18px", "vocab_count": 8, "sentence_len": "short",
        "fill_count": 8, "match_count": 8, "tf_count": 8, "quiz_count": 6, "word_comp_count": 8,
        "color_primary": "#1e40af", "color_accent": "#3b82f6", "color_bg": "#eff6ff"},
    2: {"label": "2nd Grade", "font_size": "16px", "vocab_count": 10, "sentence_len": "short",
        "fill_count": 10, "match_count": 10, "tf_count": 8, "quiz_count": 8, "word_comp_count": 10,
        "color_primary": "#059669", "color_accent": "#34d399", "color_bg": "#ecfdf5"},
    3: {"label": "3rd Grade", "font_size": "15px", "vocab_count": 10, "sentence_len": "medium",
        "fill_count": 10, "match_count": 10, "tf_count": 10, "quiz_count": 8, "word_comp_count": 10,
        "color_primary": "#7c3aed", "color_accent": "#a78bfa", "color_bg": "#f5f3ff"},
    4: {"label": "4th Grade", "font_size": "14px", "vocab_count": 12, "sentence_len": "medium",
        "fill_count": 12, "match_count": 12, "tf_count": 10, "quiz_count": 10, "word_comp_count": 12,
        "color_primary": "#b45309", "color_accent": "#f59e0b", "color_bg": "#fffbeb"},
}


# ══════════════════════════════════════════════════════════════════════════════
# EMOJI MAP (shared across grades)
# ══════════════════════════════════════════════════════════════════════════════

_EMOJI_MAP = {
    # Greetings & People
    "hello": "👋", "hi": "👋", "goodbye": "👋", "bye": "👋",
    "name": "📛", "age": "🔢", "boy": "👦", "girl": "👧",
    "student": "🎒", "friend": "🤝", "teacher": "👩‍🏫",
    "mother": "👩", "father": "👨", "sister": "👧", "brother": "👦",
    "baby": "👶", "family": "👪", "pet": "🐾",
    # School
    "classroom": "🏫", "school": "🏫", "board": "📋", "desk": "📚",
    "chair": "🪑", "book": "📕", "pencil": "✏️", "pencil case": "✏️",
    "notebook": "📓", "ruler": "📏", "eraser": "🧽", "schoolbag": "🎒",
    "scissors": "✂️", "glue": "🧴", "sharpener": "🔧", "whiteboard": "📋",
    # Colors
    "red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡",
    "orange": "🟠", "purple": "🟣", "pink": "💗", "black": "⚫",
    "white": "⚪", "brown": "🟤",
    # Body
    "head": "🧑", "eye": "👁️", "ear": "👂", "nose": "👃",
    "mouth": "👄", "hand": "✋", "foot": "🦶", "arm": "💪",
    "leg": "🦵", "finger": "☝️",
    # Animals
    "cat": "🐱", "dog": "🐶", "bird": "🐦", "fish": "🐟",
    "rabbit": "🐰", "horse": "🐴", "cow": "🐄", "sheep": "🐑",
    # Food & Drink
    "apple": "🍎", "banana": "🍌", "milk": "🥛", "bread": "🍞",
    "water": "💧", "juice": "🧃", "cake": "🎂", "pizza": "🍕",
    "egg": "🥚", "cheese": "🧀", "chicken": "🍗",
    # Nature & Weather
    "sun": "☀️", "rain": "🌧️", "tree": "🌳", "flower": "🌻",
    "house": "🏠", "car": "🚗", "bus": "🚌", "ball": "⚽",
    # Numbers
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣",
    "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣",
    "nine": "9️⃣", "ten": "🔟",
    # Adjectives
    "big": "🔺", "small": "🔹", "tall": "📏", "short": "📐",
    "happy": "😊", "sad": "😢", "kind": "💕", "funny": "😄",
    "hot": "🔥", "cold": "❄️", "new": "✨", "old": "📜",
    # Clothes
    "shirt": "👕", "dress": "👗", "shoes": "👟", "hat": "🎩",
    "jacket": "🧥", "trousers": "👖", "skirt": "👗", "socks": "🧦",
    # Actions
    "run": "🏃", "jump": "🤸", "swim": "🏊", "read": "📖",
    "write": "✍️", "sing": "🎤", "dance": "💃", "play": "🎮",
    "eat": "🍽️", "drink": "🥤", "sleep": "😴", "walk": "🚶",
    # Places
    "park": "🌳", "hospital": "🏥", "market": "🏪", "library": "📚",
    # Days & Time
    "monday": "📅", "morning": "🌅", "afternoon": "🌤️", "night": "🌙",
    # Misc
    "hobby": "🎯", "favourite": "⭐", "country": "🌍", "city": "🏙️",
    "birthday": "🎂", "address": "📍", "like": "❤️", "live": "🏠",
    "good morning": "🌅", "good afternoon": "🌤️",
}


def _emoji(word: str) -> str:
    return _EMOJI_MAP.get(word.lower().strip(), "📝")


def _deterministic_seed(grade: int, week: int) -> int:
    """Deterministic seed for reproducible randomization per grade/week."""
    return int(hashlib.md5(f"pb_{grade}_{week}".encode()).hexdigest()[:8], 16)


# ══════════════════════════════════════════════════════════════════════════════
# SENTENCE TEMPLATES — used for fill-in-blank, T/F, quiz
# ══════════════════════════════════════════════════════════════════════════════

def _make_sentences(vocab: list, structure: str, theme: str, grade: int) -> list[dict]:
    """Generate simple sentences from vocab + structure for exercises."""
    sentences = []
    # Parse structure patterns
    patterns = [p.strip() for p in structure.replace("?", "?.").split(".") if p.strip()]

    # Pattern-based sentences
    for v in vocab:
        for pat in patterns[:3]:
            if "..." in pat:
                sent = pat.replace("...", f" {v}")
                sentences.append({"sentence": sent.strip(), "word": v, "original": pat})
            elif "{" not in pat and v.lower() not in pat.lower():
                sentences.append({"sentence": f"{pat} {v}.", "word": v, "original": pat})

    # Fallback simple sentences
    _simple = [
        "I like {w}.", "This is a {w}.", "I have a {w}.", "It is {w}.",
        "I can see a {w}.", "Do you like {w}?", "Look at the {w}.",
        "The {w} is here.", "I have got a {w}.", "She has a {w}.",
    ]
    for v in vocab:
        pat = _simple[hash(v) % len(_simple)]
        sentences.append({"sentence": pat.format(w=v), "word": v, "original": pat})

    return sentences


# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE GENERATORS (return HTML fragments)
# ══════════════════════════════════════════════════════════════════════════════

def _build_fill_in_blank(vocab: list, structure: str, grade: int, cfg: dict, seed: int) -> str:
    """Exercise 1: Fill in the blanks."""
    rng = random.Random(seed)
    sentences = _make_sentences(vocab, structure, "", grade)
    rng.shuffle(sentences)
    items = sentences[:cfg["fill_count"]]

    # Word bank
    bank_words = list({s["word"] for s in items})
    rng.shuffle(bank_words)
    bank_html = " ".join(
        f'<span class="word-chip" onclick="selectWord(this)">{w}</span>'
        for w in bank_words
    )

    rows = ""
    for i, item in enumerate(items):
        blank_sent = item["sentence"].replace(item["word"], '<input type="text" class="blank-input" '
                      f'data-answer="{item["word"]}" placeholder="..." '
                      f'onfocus="this.placeholder=\'\'" '
                      f'onblur="checkBlank(this)">')
        rows += f'''<div class="exercise-row">
            <span class="q-num">{i+1}</span>
            <span class="q-text">{blank_sent}</span>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#3b82f6;">
        <div class="section-title" style="background:#3b82f6;">
            <span class="section-icon">✏️</span> Fill in the Blanks</div>
        <div class="word-bank">{bank_html}</div>
        {rows}
    </div>'''


def _build_matching(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    """Exercise 2: Match word to emoji/picture."""
    rng = random.Random(seed + 1)
    words = vocab[:cfg["match_count"]]
    shuffled_emojis = [(w, _emoji(w)) for w in words]
    rng.shuffle(shuffled_emojis)

    left_col = ""
    right_col = ""
    for i, w in enumerate(words):
        left_col += f'''<div class="match-item match-left" data-pair="{w}"
            onclick="selectMatch(this,'{w}','left')">
            <span class="q-num">{i+1}</span> {w}</div>'''

    for i, (w, em) in enumerate(shuffled_emojis):
        letter = chr(65 + i)
        right_col += f'''<div class="match-item match-right" data-pair="{w}"
            onclick="selectMatch(this,'{w}','right')">
            <span style="font-size:28px;">{em}</span>
            <span class="match-letter">{letter}</span></div>'''

    return f'''
    <div class="section-box" style="border-color:#059669;">
        <div class="section-title" style="background:#059669;">
            <span class="section-icon">🔗</span> Match the Words</div>
        <div class="match-grid">
            <div class="match-column">{left_col}</div>
            <div class="match-column">{right_col}</div>
        </div>
    </div>'''


def _build_word_completion(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    """Exercise 3: Complete the missing letters."""
    rng = random.Random(seed + 2)
    words = vocab[:cfg["word_comp_count"]]

    rows = ""
    for i, w in enumerate(words):
        em = _emoji(w)
        # Remove 30-50% of letters
        chars = list(w)
        n_hide = max(1, len(chars) // 3 if grade <= 2 else len(chars) * 2 // 5)
        indices = list(range(len(chars)))
        rng.shuffle(indices)
        hide_idx = set(indices[:n_hide])

        letter_html = ""
        for ci, ch in enumerate(chars):
            if ch == " ":
                letter_html += '<span class="letter-box space">&nbsp;</span>'
            elif ci in hide_idx:
                letter_html += (f'<input type="text" class="letter-input" maxlength="1" '
                               f'data-answer="{ch}" onkeyup="checkLetter(this)">')
            else:
                letter_html += f'<span class="letter-box filled">{ch}</span>'

        rows += f'''<div class="word-comp-row">
            <span style="font-size:32px;min-width:40px;text-align:center;">{em}</span>
            <div class="letter-group">{letter_html}</div>
            <button class="hint-btn" onclick="speak('{w}')">🔊</button>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#7c3aed;">
        <div class="section-title" style="background:#7c3aed;">
            <span class="section-icon">🔤</span> Complete the Word</div>
        {rows}
    </div>'''


def _build_true_false(vocab: list, structure: str, grade: int, cfg: dict, seed: int) -> str:
    """Exercise 4: True or False statements."""
    rng = random.Random(seed + 3)
    sentences = _make_sentences(vocab, structure, "", grade)

    items = []
    used = set()
    for s in sentences:
        if s["word"] not in used and len(items) < cfg["tf_count"]:
            used.add(s["word"])
            is_true = rng.random() > 0.45
            if is_true:
                items.append({"text": s["sentence"], "answer": "true"})
            else:
                # Create false version by swapping the word
                others = [v for v in vocab if v != s["word"]]
                if others:
                    wrong = rng.choice(others)
                    false_sent = s["sentence"].replace(s["word"], wrong)
                    items.append({"text": false_sent, "answer": "false", "correct_word": s["word"]})

    rng.shuffle(items)
    rows = ""
    for i, item in enumerate(items):
        rows += f'''<div class="tf-row">
            <span class="q-num">{i+1}</span>
            <span class="q-text">{item["text"]}</span>
            <div class="tf-buttons">
                <button class="tf-btn tf-true" onclick="checkTF(this,'{item["answer"]}','true')">
                    ✓ True</button>
                <button class="tf-btn tf-false" onclick="checkTF(this,'{item["answer"]}','false')">
                    ✗ False</button>
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#dc2626;">
        <div class="section-title" style="background:#dc2626;">
            <span class="section-icon">⚖️</span> True or False?</div>
        {rows}
    </div>'''


def _build_quiz(vocab: list, structure: str, grade: int, cfg: dict, seed: int) -> str:
    """Exercise 5: Multiple choice mini quiz."""
    rng = random.Random(seed + 4)
    sentences = _make_sentences(vocab, structure, "", grade)

    items = []
    used = set()
    for s in sentences:
        if s["word"] not in used and len(items) < cfg["quiz_count"]:
            used.add(s["word"])
            blank = s["sentence"].replace(s["word"], "______")
            others = [v for v in vocab if v != s["word"]]
            rng.shuffle(others)
            distractors = others[:3 if grade >= 3 else 2]
            options = [s["word"]] + distractors
            rng.shuffle(options)
            items.append({"question": blank, "answer": s["word"], "options": options})

    rng.shuffle(items)
    rows = ""
    for i, item in enumerate(items):
        opts_html = ""
        for opt in item["options"]:
            opts_html += (f'<button class="quiz-opt" '
                         f'onclick="checkQuiz(this,\'{item["answer"]}\',\'{opt}\')">'
                         f'{opt}</button>')
        rows += f'''<div class="quiz-row">
            <div class="q-line">
                <span class="q-num">{i+1}</span>
                <span class="q-text">{item["question"]}</span>
            </div>
            <div class="quiz-options">{opts_html}</div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#f59e0b;">
        <div class="section-title" style="background:#f59e0b;">
            <span class="section-icon">🧠</span> Mini Quiz</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _practice_styles(cfg: dict) -> str:
    cp = cfg["color_primary"]
    ca = cfg["color_accent"]
    cb = cfg["color_bg"]
    fs = cfg["font_size"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Comic Sans MS','Chalkboard SE','Segoe UI',sans-serif;
           font-size:{fs}; background:{cb}; }}
    .page {{ max-width:800px; margin:0 auto; padding:16px; }}

    /* Header */
    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:16px; padding:18px 24px; margin-bottom:16px;
        text-align:center; position:relative; overflow:hidden; }}
    .book-header h1 {{ font-size:22px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:13px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.25); padding:4px 12px; border-radius:20px;
        font-size:12px; font-weight:700; }}

    /* Score tracker */
    .score-bar {{ background:#fff; border:2px solid {ca}; border-radius:12px;
        padding:10px 16px; margin-bottom:14px; display:flex;
        justify-content:space-between; align-items:center; }}
    .score-bar .stars {{ font-size:20px; }}
    .score-bar .counter {{ font-weight:800; color:{cp}; font-size:16px; }}

    /* Sections */
    .section-box {{ background:#fff; border:3px solid #ddd; border-radius:14px;
        margin-bottom:16px; overflow:hidden; }}
    .section-title {{ color:#fff; padding:10px 16px; font-weight:800;
        font-size:15px; display:flex; align-items:center; gap:8px; }}
    .section-icon {{ font-size:18px; }}

    /* Exercise rows */
    .exercise-row, .tf-row, .quiz-row, .word-comp-row {{
        padding:10px 16px; border-bottom:1px solid #1A2035;
        display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
    .exercise-row:last-child, .tf-row:last-child, .quiz-row:last-child,
    .word-comp-row:last-child {{ border-bottom:none; }}
    .q-num {{ background:{cp}; color:#fff; width:26px; height:26px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:13px; flex-shrink:0; }}
    .q-text {{ flex:1; font-size:inherit; line-height:1.5; }}
    .q-line {{ display:flex; align-items:center; gap:10px; width:100%; }}

    /* Fill blank */
    .blank-input {{ width:90px; border:none; border-bottom:3px dashed {ca};
        background:transparent; font-size:inherit; font-weight:700;
        color:{cp}; text-align:center; padding:2px 4px; outline:none; }}
    .blank-input:focus {{ border-bottom-color:{cp}; background:#f0f9ff; }}
    .blank-input.correct {{ border-bottom-color:#059669; color:#059669;
        background:#ecfdf5; }}
    .blank-input.wrong {{ border-bottom-color:#dc2626; color:#dc2626;
        background:#fef2f2; }}
    .word-bank {{ padding:10px 16px; background:#111827; display:flex;
        flex-wrap:wrap; gap:6px; border-bottom:2px solid #e2e8f0; }}
    .word-chip {{ background:#dbeafe; color:#1e40af; padding:4px 12px;
        border-radius:20px; font-weight:700; font-size:13px; cursor:pointer;
        transition:.2s; border:2px solid transparent; }}
    .word-chip:hover {{ background:#bfdbfe; transform:scale(1.05); }}
    .word-chip.selected {{ background:#1e40af; color:#fff; }}
    .word-chip.used {{ opacity:.4; text-decoration:line-through; }}

    /* Matching */
    .match-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px;
        padding:12px 16px; }}
    .match-column {{ display:flex; flex-direction:column; gap:8px; }}
    .match-item {{ padding:10px 14px; border:2px solid #e2e8f0; border-radius:10px;
        cursor:pointer; transition:.2s; display:flex; align-items:center; gap:8px;
        font-weight:600; }}
    .match-item:hover {{ border-color:{ca}; background:{cb}; }}
    .match-item.selected {{ border-color:{cp}; background:{cb};
        box-shadow:0 0 0 3px {ca}44; }}
    .match-item.correct {{ border-color:#059669; background:#ecfdf5; }}
    .match-item.wrong {{ border-color:#dc2626; background:#fef2f2; }}
    .match-letter {{ background:#e2e8f0; width:24px; height:24px; border-radius:50%;
        display:inline-flex; align-items:center; justify-content:center;
        font-weight:800; font-size:12px; color:#475569; }}

    /* Word completion */
    .letter-group {{ display:flex; gap:4px; align-items:center; flex-wrap:wrap; }}
    .letter-box {{ width:32px; height:36px; border:2px solid #cbd5e1;
        border-radius:6px; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:18px; color:{cp}; }}
    .letter-box.filled {{ background:#f0f9ff; border-color:{ca}; }}
    .letter-box.space {{ border:none; width:12px; }}
    .letter-input {{ width:32px; height:36px; border:2px dashed {ca};
        border-radius:6px; text-align:center; font-weight:800; font-size:18px;
        color:{cp}; background:#fffbeb; outline:none; text-transform:lowercase; }}
    .letter-input:focus {{ border-color:{cp}; background:#fff; }}
    .letter-input.correct {{ border-color:#059669; background:#ecfdf5; color:#059669; }}
    .letter-input.wrong {{ border-color:#dc2626; background:#fef2f2; }}
    .hint-btn {{ background:none; border:none; font-size:20px; cursor:pointer;
        transition:.2s; }}
    .hint-btn:hover {{ transform:scale(1.2); }}

    /* True/False */
    .tf-buttons {{ display:flex; gap:6px; margin-left:auto; }}
    .tf-btn {{ padding:6px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:700; font-size:13px; cursor:pointer; transition:.2s;
        background:#fff; }}
    .tf-true:hover {{ background:#ecfdf5; border-color:#059669; }}
    .tf-false:hover {{ background:#fef2f2; border-color:#dc2626; }}
    .tf-btn.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .tf-btn.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .tf-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Quiz */
    .quiz-options {{ display:flex; flex-wrap:wrap; gap:6px; padding:4px 0 4px 36px; }}
    .quiz-opt {{ padding:6px 16px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:13px; cursor:pointer; transition:.2s;
        background:#fff; }}
    .quiz-opt:hover {{ border-color:{ca}; background:{cb}; }}
    .quiz-opt.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .quiz-opt.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .quiz-opt.disabled {{ pointer-events:none; opacity:.5; }}

    /* Animations */
    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.15)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-5px)}} 75%{{transform:translateX(5px)}} }}
    .shake {{ animation:shake .3s ease; }}
    </style>'''


def _practice_scripts() -> str:
    return '''<script>
    var totalScore = 0;
    var totalQuestions = 0;

    function updateScore(correct) {
        totalQuestions++;
        if (correct) totalScore++;
        var pct = totalQuestions > 0 ? Math.round(totalScore / totalQuestions * 100) : 0;
        var el = document.getElementById('scoreCounter');
        if (el) el.textContent = totalScore + ' / ' + totalQuestions + ' (' + pct + '%)';
        var stars = document.getElementById('scoreStars');
        if (stars) {
            var s = pct >= 90 ? '⭐⭐⭐' : pct >= 70 ? '⭐⭐' : pct >= 40 ? '⭐' : '';
            stars.textContent = s;
        }
    }

    /* TTS */
    function speak(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.85; u.pitch = 1.1;
            window.speechSynthesis.speak(u);
        }
    }

    /* Fill in blank */
    var selectedWord = null;
    function selectWord(el) {
        document.querySelectorAll('.word-chip').forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        selectedWord = el.textContent.trim();
    }
    function checkBlank(el) {
        var ans = el.dataset.answer.toLowerCase().trim();
        var val = el.value.toLowerCase().trim();
        if (!val) return;
        if (val === ans) {
            el.classList.remove('wrong');
            el.classList.add('correct', 'pop');
            el.disabled = true;
            updateScore(true);
            speak('Correct!');
            /* mark word as used */
            document.querySelectorAll('.word-chip').forEach(c => {
                if (c.textContent.trim().toLowerCase() === ans) c.classList.add('used');
            });
        } else {
            el.classList.remove('correct');
            el.classList.add('wrong', 'shake');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    /* Matching */
    var matchSelected = {left: null, right: null, leftEl: null, rightEl: null};
    function selectMatch(el, word, side) {
        if (el.classList.contains('correct')) return;
        document.querySelectorAll('.match-' + side).forEach(c => c.classList.remove('selected'));
        el.classList.add('selected');
        matchSelected[side] = word;
        matchSelected[side + 'El'] = el;
        if (matchSelected.left && matchSelected.right) {
            if (matchSelected.left === matchSelected.right) {
                matchSelected.leftEl.classList.add('correct', 'pop');
                matchSelected.rightEl.classList.add('correct', 'pop');
                updateScore(true);
                speak('Great!');
            } else {
                matchSelected.leftEl.classList.add('wrong', 'shake');
                matchSelected.rightEl.classList.add('wrong', 'shake');
                updateScore(false);
                setTimeout(() => {
                    matchSelected.leftEl.classList.remove('wrong','shake','selected');
                    matchSelected.rightEl.classList.remove('wrong','shake','selected');
                }, 600);
            }
            matchSelected = {left:null, right:null, leftEl:null, rightEl:null};
        }
    }

    /* Letter completion */
    function checkLetter(el) {
        var val = el.value.toLowerCase().trim();
        var ans = el.dataset.answer.toLowerCase();
        if (!val) { el.classList.remove('correct','wrong'); return; }
        if (val === ans) {
            el.classList.remove('wrong');
            el.classList.add('correct');
            el.disabled = true;
            /* auto-focus next empty input */
            var next = el.parentElement.querySelector('input:not([disabled])');
            if (next) next.focus();
            else { updateScore(true); speak('Well done!'); }
        } else {
            el.classList.remove('correct');
            el.classList.add('wrong', 'shake');
            setTimeout(() => { el.classList.remove('shake'); el.value=''; }, 500);
        }
    }

    /* True/False */
    function checkTF(el, answer, chosen) {
        var parent = el.closest('.tf-row');
        var btns = parent.querySelectorAll('.tf-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct', 'pop');
            updateScore(true);
            speak('Correct!');
        } else {
            el.classList.add('wrong', 'shake');
            btns.forEach(b => { if (!b.classList.contains('wrong')) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    /* Quiz */
    function checkQuiz(el, answer, chosen) {
        var parent = el.closest('.quiz-row');
        var opts = parent.querySelectorAll('.quiz-opt');
        opts.forEach(o => o.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct', 'pop');
            updateScore(true);
            speak('Excellent!');
        } else {
            el.classList.add('wrong', 'shake');
            opts.forEach(o => {
                if (o.textContent.trim() === answer) o.classList.add('correct');
            });
            updateScore(false);
        }
    }
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocab_review(vocab: list) -> str:
    """Vocabulary review card with TTS and emoji."""
    html = '<div class="section-box" style="border-color:#6366f1;">'
    html += '<div class="section-title" style="background:#6366f1;">'
    html += '<span class="section-icon">📚</span> Vocabulary Review — Click to Listen</div>'
    html += '<div style="display:flex;flex-wrap:wrap;gap:10px;padding:14px 16px;justify-content:center;">'
    for v in vocab:
        em = _emoji(v)
        html += (f'<div style="background:#f0f9ff;border:2px solid #93c5fd;'
                f'border-radius:12px;padding:10px 16px;text-align:center;'
                f'cursor:pointer;transition:.2s;min-width:90px;" '
                f'onclick="speak(\'{v}\')">'
                f'<div style="font-size:32px;">{em}</div>'
                f'<div style="font-weight:700;color:#1e40af;font-size:15px;'
                f'margin-top:5px;">{v}</div></div>')
    html += '</div></div>'
    return html


def build_practice_pages(grade: int, week_num: int,
                         curriculum_weeks: list) -> list[str]:
    """Build Practice Book pages for a given grade/week.

    Args:
        grade: 1-4
        week_num: 1-36
        curriculum_weeks: Full curriculum list for the grade

    Returns:
        List of 5 HTML strings — one page per exercise type:
        Page 1: Fill in the Blanks
        Page 2: Matching
        Page 3: Word Completion
        Page 4: True / False
        Page 5: Mini Quiz
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[2])
    vocab = week_data.get("vocab", [])[:cfg["vocab_count"]]
    structure = week_data.get("structure", "")
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    if not vocab:
        return []

    # Unit number (approx 3-4 weeks per unit)
    unit_num = max(1, (week_num - 1) // 4 + 1)

    _page_titles = [
        "✏️ Fill in the Blanks",
        "🔗 Matching",
        "🔤 Word Completion",
        "⚖️ True or False",
        "🧠 Mini Quiz",
    ]

    styles = _practice_styles(cfg)
    scripts = _practice_scripts()
    vocab_review = _build_vocab_review(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>📘 Practice Book — Unit {unit_num}</h1>
            <div class="subtitle">{theme} — {theme_tr} | Week {week_num} | Page {page_num}/5</div>
            <div style="font-size:11px;opacity:.7;margin-top:2px;">{_page_titles[page_num - 1]}</div>
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

    # ── PAGE 1: Fill in the Blanks ──
    page1 = _wrap(1, _build_fill_in_blank(vocab, structure, grade, cfg, seed))

    # ── PAGE 2: Matching ──
    page2 = _wrap(2, _build_matching(vocab, grade, cfg, seed))

    # ── PAGE 3: Word Completion ──
    page3 = _wrap(3, _build_word_completion(vocab, grade, cfg, seed))

    # ── PAGE 4: True / False ──
    page4 = _wrap(4, _build_true_false(vocab, structure, grade, cfg, seed))

    # ── PAGE 5: Mini Quiz ──
    page5 = _wrap(5, _build_quiz(vocab, structure, grade, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_practice_book(grade: int, curriculum_weeks: list,
                              selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Practice Book for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_practice_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
