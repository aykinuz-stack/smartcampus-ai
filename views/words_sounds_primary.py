# -*- coding: utf-8 -*-
"""Words & Sounds — İlkokul (1-4) Phonics + Vocabulary Destek Kitabı.

Interactive HTML pages for primary school phonics & vocabulary development.
Activity types (5 pages per week):
  1. Visual Dictionary (Tema bazlı görsel sözlük + TTS)
  2. Phonics Practice (Ses-harf ilişkisi çalışmaları)
  3. Spelling Activities (Heceleme çalışmaları)
  4. Pronunciation Drills (Telaffuz tekrarları + Flashcard)
  5. Review & Games (Karma tekrar oyunları)

All content is dynamically generated from curriculum data.
Each week produces 5 HTML pages — one per activity type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# GRADE-LEVEL CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_GRADE_CFG = {
    1: {"label": "1st Grade", "font_size": "22px", "vocab_count": 8,
        "phonics_count": 6, "spelling_count": 6, "pron_count": 6, "review_count": 8,
        "color_primary": "#e91e63", "color_accent": "#f06292", "color_bg": "#fce4ec"},
    2: {"label": "2nd Grade", "font_size": "20px", "vocab_count": 10,
        "phonics_count": 8, "spelling_count": 8, "pron_count": 8, "review_count": 10,
        "color_primary": "#9c27b0", "color_accent": "#ba68c8", "color_bg": "#f3e5f5"},
    3: {"label": "3rd Grade", "font_size": "18px", "vocab_count": 12,
        "phonics_count": 8, "spelling_count": 10, "pron_count": 8, "review_count": 10,
        "color_primary": "#00897b", "color_accent": "#4db6ac", "color_bg": "#e0f2f1"},
    4: {"label": "4th Grade", "font_size": "16px", "vocab_count": 14,
        "phonics_count": 10, "spelling_count": 10, "pron_count": 10, "review_count": 12,
        "color_primary": "#1565c0", "color_accent": "#42a5f5", "color_bg": "#e3f2fd"},
}

# Emoji map for common primary words
_EMOJI_MAP = {
    "hello": "👋", "hi": "👋", "goodbye": "👋", "name": "📛",
    "boy": "👦", "girl": "👧", "friend": "🤝", "teacher": "👩‍🏫",
    "mother": "👩", "father": "👨", "sister": "👧", "brother": "👦",
    "baby": "👶", "family": "👪", "school": "🏫", "book": "📕",
    "pencil": "✏️", "bag": "🎒", "desk": "🪑", "chair": "💺",
    "red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡",
    "orange": "🟠", "purple": "🟣", "pink": "💗", "black": "⚫",
    "white": "⚪", "brown": "🟤", "color": "🎨", "colours": "🎨",
    "cat": "🐱", "dog": "🐶", "fish": "🐟", "bird": "🐦",
    "rabbit": "🐰", "horse": "🐴", "cow": "🐄", "pig": "🐷",
    "apple": "🍎", "banana": "🍌", "cake": "🎂", "milk": "🥛",
    "water": "💧", "juice": "🧃", "bread": "🍞", "egg": "🥚",
    "sun": "☀️", "moon": "🌙", "star": "⭐", "tree": "🌳",
    "flower": "🌸", "rain": "🌧️", "cloud": "☁️", "snow": "❄️",
    "house": "🏠", "car": "🚗", "bus": "🚌", "train": "🚂",
    "ball": "⚽", "doll": "🪆", "game": "🎮", "toy": "🧸",
    "happy": "😊", "sad": "😢", "big": "🔵", "small": "🔹",
    "hot": "🔥", "cold": "🥶", "fast": "⚡", "slow": "🐢",
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣",
    "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣",
    "nine": "9️⃣", "ten": "🔟", "eye": "👁️", "nose": "👃",
    "mouth": "👄", "ear": "👂", "hand": "✋", "foot": "🦶",
    "head": "🧠", "arm": "💪", "leg": "🦵", "tooth": "🦷",
    "hat": "🎩", "shirt": "👕", "shoes": "👟", "dress": "👗",
    "day": "☀️", "night": "🌙", "morning": "🌅", "afternoon": "🌤️",
    "lion": "🦁", "tiger": "🐯", "bear": "🐻", "monkey": "🐵",
    "duck": "🦆", "frog": "🐸", "snake": "🐍", "turtle": "🐢",
    "eat": "🍽️", "drink": "🥤", "run": "🏃", "jump": "🤸",
    "sleep": "😴", "play": "🎮", "sing": "🎤", "dance": "💃",
    "read": "📖", "write": "✍️", "draw": "🎨", "swim": "🏊",
    "like": "❤️", "love": "💕", "want": "🙏", "have": "✅",
    "pizza": "🍕", "chicken": "🍗", "ice cream": "🍦", "chocolate": "🍫",
    "spring": "🌷", "summer": "☀️", "autumn": "🍂", "winter": "❄️",
    "monday": "📅", "tuesday": "📅", "wednesday": "📅",
    "food": "🍽️", "fruit": "🍎", "vegetable": "🥦", "meat": "🥩",
    "park": "🏞️", "garden": "🌻", "street": "🛣️", "shop": "🏪",
    "doctor": "👨‍⚕️", "police": "👮", "farmer": "👨‍🌾", "pilot": "👨‍✈️",
}

# Phonics data for common letter patterns
_PHONICS_PATTERNS = {
    "a": {"sound": "/æ/", "words": ["apple", "ant", "cat", "hat", "bag", "map", "van", "bat"]},
    "e": {"sound": "/ɛ/", "words": ["egg", "bed", "red", "pen", "ten", "hen", "leg", "net"]},
    "i": {"sound": "/ɪ/", "words": ["it", "big", "sit", "pig", "hit", "lip", "fin", "dig"]},
    "o": {"sound": "/ɒ/", "words": ["hot", "dog", "box", "fox", "top", "pot", "mop", "log"]},
    "u": {"sound": "/ʌ/", "words": ["up", "bus", "cup", "sun", "run", "fun", "nut", "bug"]},
    "sh": {"sound": "/ʃ/", "words": ["ship", "shop", "fish", "shoe", "shell", "shut", "she", "shake"]},
    "ch": {"sound": "/tʃ/", "words": ["chair", "cheese", "chicken", "chin", "check", "chat", "chip", "chop"]},
    "th": {"sound": "/θ/", "words": ["three", "think", "thick", "thin", "thank", "thumb", "bath", "tooth"]},
    "ee": {"sound": "/iː/", "words": ["tree", "bee", "see", "free", "green", "sleep", "feet", "teeth"]},
    "oo": {"sound": "/uː/", "words": ["moon", "food", "school", "cool", "pool", "room", "zoo", "too"]},
    "ai": {"sound": "/eɪ/", "words": ["rain", "train", "snail", "tail", "mail", "nail", "paint", "wait"]},
    "ow": {"sound": "/aʊ/", "words": ["cow", "how", "now", "brown", "down", "town", "owl", "wow"]},
}


def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"ws_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _emoji(word: str) -> str:
    return _EMOJI_MAP.get(word.lower(), "📌")


def _get_week_phonics(grade: int, week: int) -> list[str]:
    """Return 2-3 phonics patterns per week based on grade/week."""
    patterns = list(_PHONICS_PATTERNS.keys())
    # Grade 1-2: focus on single vowels; Grade 3-4: add digraphs
    if grade <= 2:
        pool = [p for p in patterns if len(p) == 1]
    else:
        pool = patterns
    start = ((week - 1) * 2) % len(pool)
    return [pool[(start + i) % len(pool)] for i in range(2 + (1 if grade >= 3 else 0))]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Visual Dictionary (Tema bazlı görsel sözlük)
# ══════════════════════════════════════════════════════════════════════════════

def _build_visual_dictionary(vocab: list, theme: str, theme_tr: str,
                              grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)
    words = vocab[:cfg["vocab_count"]]

    # Flashcard grid
    cards = ""
    for i, w in enumerate(words):
        em = _emoji(w)
        cards += f'''
        <div class="flash-card" onclick="speakWord('{w}')">
            <div class="flash-emoji">{em}</div>
            <div class="flash-word">{w}</div>
            <div class="flash-speaker">🔊 tap to hear</div>
        </div>'''

    # Word-picture matching
    shuffled = list(words[:6])
    rng.shuffle(shuffled)
    match_left = ""
    for w in words[:6]:
        match_left += f'<div class="dict-match-item" data-word="{w}" onclick="selectDictWord(this)">{_emoji(w)} {w}</div>'

    match_right = ""
    for w in shuffled:
        match_right += f'<div class="dict-match-item target" data-word="{w}" onclick="matchDictWord(this,\'{w}\')">{w[0]}____</div>'

    # Write the word
    write_items = ""
    for i, w in enumerate(words[:cfg["vocab_count"] // 2]):
        write_items += f'''
        <div class="write-row">
            <span class="q-num">{i+1}</span>
            <span class="write-emoji" onclick="speakWord('{w}')">{_emoji(w)} 🔊</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="Write the word..." onblur="checkAnswer(this)">
        </div>'''

    return f'''
    <div class="section-box" style="border-color:{cfg["color_accent"]};">
        <div class="section-title" style="background:linear-gradient(135deg,{cfg["color_primary"]},{cfg["color_accent"]});">
            <span class="section-icon">📖</span> Visual Dictionary — {theme}</div>
        <div class="theme-banner">
            <span class="theme-emoji">🎯</span>
            <span class="theme-text">{theme} — {theme_tr}</span>
        </div>

        <div class="sub-section">
            <div class="sub-title">A. Picture Cards — Tap to Listen</div>
            <div class="flash-grid">{cards}</div>
        </div>

        <div class="sub-section">
            <div class="sub-title">B. Match the Word to the Picture</div>
            <div class="dict-match-area">
                <div class="dict-col">{match_left}</div>
                <div class="dict-col">{match_right}</div>
            </div>
        </div>

        <div class="sub-section">
            <div class="sub-title">C. Listen and Write</div>
            {write_items}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Phonics Practice (Ses-harf ilişkisi)
# ══════════════════════════════════════════════════════════════════════════════

def _build_phonics_practice(vocab: list, grade: int, week: int,
                             cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 10)
    patterns = _get_week_phonics(grade, week)

    rows = ""

    # Part A: Sound introduction
    rows += '<div class="sub-section"><div class="sub-title">🔊 A. Learn the Sounds</div>'
    rows += '<div class="hint-text">Click each card to hear the sound!</div>'

    for pat in patterns:
        data = _PHONICS_PATTERNS.get(pat, {})
        sound = data.get("sound", "")
        p_words = data.get("words", [])[:4]

        word_chips = ""
        for w in p_words:
            word_chips += f'''<span class="phon-word" onclick="speakWord('{w}')">
                {_emoji(w)} {w} 🔊</span>'''

        rows += f'''
        <div class="phon-row">
            <div class="phon-hero" onclick="speakWord('{pat} says {sound}')">
                <span class="phon-letter">{pat}</span>
                <span class="phon-sound">{sound}</span>
                <span class="mini-speaker">🔊</span>
            </div>
            <div class="phon-words">{word_chips}</div>
        </div>'''
    rows += '</div>'

    # Part B: Which word has this sound?
    rows += '<div class="sub-section"><div class="sub-title">👂 B. Find the Sound</div>'
    rows += '<div class="hint-text">Tap all words that contain the highlighted sound!</div>'

    for pat in patterns:
        data = _PHONICS_PATTERNS.get(pat, {})
        p_words = data.get("words", [])[:3]
        # Distractors
        other_pats = [p for p in _PHONICS_PATTERNS if p != pat]
        rng.shuffle(other_pats)
        distractors = []
        for op in other_pats[:2]:
            dw = _PHONICS_PATTERNS[op].get("words", [])
            if dw:
                distractors.append(rng.choice(dw))

        all_opts = p_words + distractors
        rng.shuffle(all_opts)

        btns = ""
        for w in all_opts:
            has_sound = pat in w.lower() or (len(pat) == 1 and w.lower().startswith(pat))
            # More accurate check for single vowels
            if len(pat) == 1:
                has_sound = w.lower() in _PHONICS_PATTERNS.get(pat, {}).get("words", [])
            btns += f'''<button class="sound-pick-btn" onclick="checkSound(this,{'true' if has_sound else 'false'})">
                {_emoji(w)} {w}</button>'''

        rows += f'''
        <div class="find-sound-row">
            <div class="find-label" onclick="speakWord('{pat}')">
                <span class="find-letter">{pat}</span> 🔊
            </div>
            <div class="find-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Beginning sound sort
    rows += '<div class="sub-section"><div class="sub-title">📦 C. Sort by Beginning Sound</div>'
    rows += '<div class="hint-text">Which letter does each word start with?</div>'

    sort_words = []
    for pat in patterns[:2]:
        for w in _PHONICS_PATTERNS.get(pat, {}).get("words", [])[:3]:
            sort_words.append((w, pat[0].upper()))
    rng.shuffle(sort_words)

    for i, (w, first_letter) in enumerate(sort_words[:cfg["phonics_count"]]):
        em = _emoji(w)
        # Options: correct letter + 2 distractors
        all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        distr = [l for l in all_letters if l != first_letter]
        rng.shuffle(distr)
        options = [first_letter] + distr[:2]
        rng.shuffle(options)
        btns = ""
        for o in options:
            btns += f'''<button class="letter-pick" onclick="checkLetterSort(this,'{first_letter}','{o}')">
                {o}</button>'''

        rows += f'''
        <div class="sort-row">
            <span class="q-num">{i+1}</span>
            <span class="sort-word" onclick="speakWord('{w}')">{em} {w} 🔊</span>
            <div class="sort-options">{btns}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF9800;">
        <div class="section-title" style="background:linear-gradient(135deg,#e65100,#FF9800);">
            <span class="section-icon">🔤</span> Phonics Practice</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Spelling Activities (Heceleme çalışmaları)
# ══════════════════════════════════════════════════════════════════════════════

def _build_spelling(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 20)
    words = vocab[:cfg["spelling_count"]]

    rows = ""

    # Part A: Missing letter
    rows += '<div class="sub-section"><div class="sub-title">🔍 A. Find the Missing Letter</div>'
    rows += '<div class="hint-text">Which letter is missing? Type it in!</div>'

    for i, w in enumerate(words):
        if len(w) < 2:
            continue
        idx = rng.randint(0, len(w) - 1)
        display = list(w)
        missing = display[idx]
        display[idx] = "_"
        shown = "".join(display)

        rows += f'''
        <div class="spell-row">
            <span class="q-num">{i+1}</span>
            <span class="spell-emoji" onclick="speakWord('{w}')">{_emoji(w)} 🔊</span>
            <span class="spell-word">{shown}</span>
            <input type="text" class="letter-input" data-answer="{missing}"
                   maxlength="1" placeholder="?" onblur="checkLetter(this)">
        </div>'''
    rows += '</div>'

    # Part B: Unscramble
    rows += '<div class="sub-section"><div class="sub-title">🔀 B. Unscramble the Word</div>'
    rows += '<div class="hint-text">Put the letters in the correct order!</div>'

    for i, w in enumerate(words[:cfg["spelling_count"] // 2 + 1]):
        chars = list(w)
        rng.shuffle(chars)
        scrambled = " ".join(chars).upper()

        rows += f'''
        <div class="spell-row">
            <span class="q-num">{i+1}</span>
            <span class="spell-emoji" onclick="speakWord('{w}')">{_emoji(w)} 🔊</span>
            <span class="scrambled-letters">{scrambled}</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="Write the word..." onblur="checkAnswer(this)">
        </div>'''
    rows += '</div>'

    # Part C: Listen and spell
    rows += '<div class="sub-section"><div class="sub-title">🎧 C. Listen and Spell</div>'
    rows += '<div class="hint-text">Click the speaker, listen to the word, then spell it!</div>'

    for i, w in enumerate(words):
        rows += f'''
        <div class="spell-row">
            <span class="q-num">{i+1}</span>
            <button class="listen-btn" onclick="speakWord('{w}')">🔊 Listen</button>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="Spell the word..." onblur="checkAnswer(this)">
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#4CAF50;">
        <div class="section-title" style="background:linear-gradient(135deg,#2e7d32,#4CAF50);">
            <span class="section-icon">✏️</span> Spelling Activities</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Pronunciation Drills (Telaffuz tekrarları)
# ══════════════════════════════════════════════════════════════════════════════

def _build_pronunciation(vocab: list, structure: str, grade: int,
                          cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 30)
    words = vocab[:cfg["pron_count"]]

    rows = ""

    # Part A: Word pronunciation cards
    rows += '<div class="sub-section"><div class="sub-title">🗣️ A. Say It Right — Listen & Repeat</div>'
    rows += '<div class="hint-text">Click each word, listen carefully, then say it out loud 3 times!</div>'

    for w in words:
        syllable_count = max(1, sum(1 for c in w.lower() if c in "aeiou"))
        dots = "•" * syllable_count

        rows += f'''
        <div class="pron-card" onclick="speakSlow('{w}')">
            <span class="pron-emoji">{_emoji(w)}</span>
            <span class="pron-word">{w}</span>
            <span class="pron-dots">{dots} ({syllable_count} syllable{"s" if syllable_count > 1 else ""})</span>
            <span class="pron-speaker">🔊</span>
        </div>'''
    rows += '</div>'

    # Part B: Minimal pairs
    rows += '<div class="sub-section"><div class="sub-title">👂 B. Same or Different?</div>'
    rows += '<div class="hint-text">Listen to both words. Do they sound the same or different?</div>'

    _minimal_pairs = [
        ("cat", "cut"), ("ship", "sheep"), ("bed", "bad"), ("sit", "set"),
        ("hot", "hat"), ("pen", "pan"), ("run", "ran"), ("big", "bag"),
        ("cup", "cap"), ("bit", "beat"), ("dog", "dig"), ("fun", "fan"),
    ]
    rng.shuffle(_minimal_pairs)

    for w1, w2 in _minimal_pairs[:4]:
        is_same = w1 == w2
        rows += f'''
        <div class="pair-row">
            <button class="pair-word" onclick="speakWord('{w1}')">{_emoji(w1)} {w1} 🔊</button>
            <span class="pair-vs">vs</span>
            <button class="pair-word" onclick="speakWord('{w2}')">{_emoji(w2)} {w2} 🔊</button>
            <div class="pair-btns">
                <button class="pair-btn" onclick="checkPair(this,'different','same')">Same</button>
                <button class="pair-btn" onclick="checkPair(this,'different','different')">Different</button>
            </div>
        </div>'''
    rows += '</div>'

    # Part C: Sentence pronunciation
    rows += '<div class="sub-section"><div class="sub-title">📢 C. Say the Sentence</div>'
    rows += '<div class="hint-text">Click to hear the sentence, then practise saying it!</div>'

    _sentence_templates = [
        "I like {w}.", "This is a {w}.", "I can see a {w}.",
        "Do you have a {w}?", "The {w} is big.", "I want a {w}.",
    ]

    for i, w in enumerate(words[:4]):
        tmpl = _sentence_templates[i % len(_sentence_templates)]
        sent = tmpl.format(w=w)

        rows += f'''
        <div class="sent-pron-row" onclick="speakSlow('{sent}')">
            <span class="q-num">{i+1}</span>
            <span class="sent-text">{sent}</span>
            <span class="pron-speaker">🔊</span>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#2196F3;">
        <div class="section-title" style="background:linear-gradient(135deg,#0d47a1,#2196F3);">
            <span class="section-icon">🗣️</span> Pronunciation Drills</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Review & Games (Karma tekrar)
# ══════════════════════════════════════════════════════════════════════════════

def _build_review_games(vocab: list, grade: int, week: int,
                         cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 40)
    words = vocab[:cfg["review_count"]]

    rows = ""

    # Game 1: Word Bingo
    rows += '<div class="sub-section"><div class="sub-title">🎲 Game 1: Word Bingo</div>'
    rows += '<div class="hint-text">Click the speaker buttons below, then mark the matching word on the board!</div>'

    rng2 = random.Random(seed + 41)
    bingo_words = list(words[:6])
    rng2.shuffle(bingo_words)

    bingo_grid = ""
    for w in bingo_words:
        bingo_grid += f'''
        <div class="bingo-card" onclick="markBingo(this)">
            <span class="bingo-emoji">{_emoji(w)}</span>
            <span class="bingo-word">{w}</span>
        </div>'''

    speaker_row = ""
    rng2.shuffle(bingo_words)
    for w in bingo_words:
        speaker_row += f'<button class="bingo-speak" onclick="speakWord(\'{w}\')">🔊 {_emoji(w)}</button>'

    rows += f'''
    <div class="bingo-area">
        <div class="bingo-grid">{bingo_grid}</div>
        <div class="bingo-speakers">{speaker_row}</div>
    </div>'''
    rows += '</div>'

    # Game 2: Speed Quiz
    rows += '<div class="sub-section"><div class="sub-title">⚡ Game 2: Speed Quiz</div>'
    rows += '<div class="hint-text">Choose the correct word for each picture as fast as you can!</div>'

    for i, w in enumerate(words[:cfg["review_count"] // 2]):
        others = [v for v in words if v != w]
        rng.shuffle(others)
        options = [w] + others[:2]
        rng.shuffle(options)

        btns = ""
        for o in options:
            btns += f'''<button class="quiz-btn" onclick="checkQuiz(this,'{w}','{o}')">{o}</button>'''

        rows += f'''
        <div class="quiz-row">
            <span class="q-num">{i+1}</span>
            <span class="quiz-emoji" onclick="speakWord('{w}')">{_emoji(w)} 🔊</span>
            <div class="quiz-opts">{btns}</div>
        </div>'''
    rows += '</div>'

    # Game 3: Memory Match (word + emoji pairs)
    rows += '<div class="sub-section"><div class="sub-title">🧠 Game 3: Memory Match</div>'
    rows += '<div class="hint-text">Find the matching pairs! Click two cards to flip them.</div>'

    mem_words = words[:4]
    mem_cards = []
    for w in mem_words:
        mem_cards.append({"type": "word", "value": w, "match_id": w})
        mem_cards.append({"type": "emoji", "value": _emoji(w), "match_id": w})
    rng.shuffle(mem_cards)

    mem_html = ""
    for i, card in enumerate(mem_cards):
        mem_html += f'''
        <div class="mem-card" data-id="{card['match_id']}" data-idx="{i}" onclick="flipCard(this)">
            <div class="mem-front">?</div>
            <div class="mem-back">{card["value"]}</div>
        </div>'''

    rows += f'<div class="memory-grid">{mem_html}</div>'
    rows += '</div>'

    # Game 4: Word Chain
    rows += '<div class="sub-section"><div class="sub-title">🔗 Game 4: Word Chain</div>'
    rows += '<div class="hint-text">Type a word that starts with the last letter of the previous word!</div>'

    chain_start = words[0] if words else "cat"
    rows += f'''
    <div class="chain-area">
        <div class="chain-start" onclick="speakWord('{chain_start}')">
            {_emoji(chain_start)} <b>{chain_start}</b> 🔊
        </div>
        <div class="chain-arrow">→ starts with "{chain_start[-1].upper()}"</div>
        <input type="text" class="chain-input" id="chainInput"
               placeholder="Type a word starting with '{chain_start[-1].upper()}'..."
               onkeydown="if(event.key==='Enter')addChainWord(this,'{chain_start[-1].lower()}')">
        <div class="chain-words" id="chainWords"></div>
    </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF5722;">
        <div class="section-title" style="background:linear-gradient(135deg,#bf360c,#FF5722);">
            <span class="section-icon">🎮</span> Review & Games</div>
        <div class="game-score-bar">
            🌟 Score: <span class="counter" id="gameScore">0</span>
        </div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _ws_styles(cfg: dict) -> str:
    cp = cfg["color_primary"]
    ca = cfg["color_accent"]
    cb = cfg["color_bg"]
    fs = cfg["font_size"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Segoe UI','Comic Sans MS',sans-serif;
           font-size:{fs}; background:{cb}; color:#94A3B8; }}
    .page {{ max-width:860px; margin:0 auto; padding:16px; }}

    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:16px; padding:20px 24px; margin-bottom:14px;
        text-align:center; position:relative;
        box-shadow:0 6px 20px {cp}44; }}
    .book-header h1 {{ font-size:24px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:13px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.25); padding:5px 14px; border-radius:20px;
        font-size:12px; font-weight:700; }}

    .score-bar {{ background:#fff; border:2px solid {ca}; border-radius:12px;
        padding:10px 16px; margin-bottom:14px; display:flex;
        justify-content:space-between; align-items:center; }}
    .counter {{ font-weight:900; color:{cp}; font-size:18px; }}

    .section-box {{ background:#fff; border:2px solid #e2e8f0; border-radius:16px;
        margin-bottom:18px; overflow:hidden;
        box-shadow:0 2px 8px rgba(0,0,0,.06); }}
    .section-title {{ color:#fff; padding:14px 20px; font-weight:700;
        font-size:16px; display:flex; align-items:center; gap:8px; }}
    .section-icon {{ font-size:20px; }}

    .sub-section {{ padding:16px 20px; border-bottom:1px solid #1A2035; }}
    .sub-section:last-child {{ border-bottom:none; }}
    .sub-title {{ font-weight:800; color:{cp}; font-size:15px; margin-bottom:10px;
        padding-bottom:6px; border-bottom:3px solid {ca}33; }}
    .hint-text {{ font-size:13px; color:#64748b; margin-bottom:12px; font-style:italic; }}

    .q-num {{ background:{cp}; color:#fff; min-width:28px; height:28px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:13px; flex-shrink:0; }}

    .theme-banner {{ padding:10px 20px; background:linear-gradient(135deg,{cp}10,{ca}08);
        display:flex; align-items:center; gap:10px; border-bottom:2px solid #e2e8f0; }}
    .theme-emoji {{ font-size:24px; }}
    .theme-text {{ font-weight:700; color:{cp}; font-size:15px; }}

    /* Visual Dictionary */
    .flash-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr));
        gap:10px; }}
    .flash-card {{ display:flex; flex-direction:column; align-items:center;
        padding:16px 10px; border:3px solid #e2e8f0; border-radius:14px;
        cursor:pointer; background:#fff; transition:.3s; text-align:center; }}
    .flash-card:hover {{ border-color:{ca}; transform:translateY(-3px);
        box-shadow:0 6px 16px rgba(0,0,0,.1); }}
    .flash-emoji {{ font-size:42px; margin-bottom:6px; }}
    .flash-word {{ font-weight:800; color:{cp}; font-size:16px; }}
    .flash-speaker {{ font-size:11px; color:#94a3b8; margin-top:4px; }}

    .dict-match-area {{ display:flex; gap:20px; justify-content:center; flex-wrap:wrap; }}
    .dict-col {{ display:flex; flex-direction:column; gap:8px; }}
    .dict-match-item {{ padding:10px 16px; border:2px solid #e2e8f0; border-radius:10px;
        cursor:pointer; font-weight:600; font-size:14px; transition:.2s; background:#fff; }}
    .dict-match-item:hover {{ border-color:{ca}; background:{cb}; }}
    .dict-match-item.selected {{ border-color:{cp}; background:{cp}15; }}
    .dict-match-item.matched {{ border-color:#4CAF50; background:#e8f5e9; pointer-events:none; }}

    .write-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; }}
    .write-emoji {{ font-size:28px; cursor:pointer; }}

    .answer-input {{ flex:1; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; padding:6px 4px;
        color:{cp}; font-weight:600; outline:none; }}
    .answer-input:focus {{ border-bottom-color:{cp}; background:#111827; }}
    .answer-input.correct {{ border-bottom-color:#4CAF50; color:#4CAF50; background:#e8f5e9; }}
    .answer-input.wrong {{ border-bottom-color:#f44336; color:#f44336; background:#ffebee; }}

    /* Phonics */
    .phon-row {{ display:flex; align-items:center; gap:14px; padding:12px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .phon-hero {{ display:flex; align-items:center; gap:8px; padding:10px 16px;
        background:linear-gradient(135deg,#FF980015,#FF980008); border-radius:12px;
        cursor:pointer; transition:.2s; min-width:140px; }}
    .phon-hero:hover {{ transform:scale(1.03); }}
    .phon-letter {{ font-size:32px; font-weight:900; color:#e65100; }}
    .phon-sound {{ font-size:14px; color:#bf360c; font-weight:700;
        background:#fff; padding:3px 10px; border-radius:8px; }}
    .mini-speaker {{ font-size:14px; }}
    .phon-words {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .phon-word {{ display:inline-flex; align-items:center; gap:4px;
        padding:6px 12px; background:#fff3e0; border-radius:8px;
        cursor:pointer; font-size:13px; font-weight:600; transition:.2s; }}
    .phon-word:hover {{ background:#ffe0b2; }}

    .find-sound-row {{ display:flex; align-items:center; gap:12px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .find-label {{ font-size:24px; font-weight:900; color:#e65100; cursor:pointer;
        min-width:60px; text-align:center; }}
    .find-letter {{ font-size:28px; }}
    .find-options {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .sound-pick-btn {{ padding:8px 14px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .sound-pick-btn:hover {{ border-color:#FF9800; background:#fff3e0; }}
    .sound-pick-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .sound-pick-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .sound-pick-btn.disabled {{ pointer-events:none; opacity:.5; }}

    .sort-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; }}
    .sort-word {{ font-weight:700; font-size:16px; cursor:pointer; min-width:120px; }}
    .sort-options {{ display:flex; gap:6px; }}
    .letter-pick {{ width:42px; height:42px; border:2px solid #e2e8f0; border-radius:10px;
        font-size:18px; font-weight:900; cursor:pointer; background:#fff; transition:.2s; }}
    .letter-pick:hover {{ border-color:{ca}; background:{cb}; }}
    .letter-pick.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .letter-pick.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .letter-pick.disabled {{ pointer-events:none; opacity:.5; }}

    /* Spelling */
    .spell-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; }}
    .spell-emoji {{ font-size:28px; cursor:pointer; }}
    .spell-word {{ font-size:22px; font-weight:900; letter-spacing:4px; color:#475569; }}
    .letter-input {{ width:40px; height:40px; border:2px dashed {ca}; border-radius:8px;
        font-size:20px; font-weight:900; text-align:center; text-transform:lowercase;
        color:{cp}; outline:none; background:transparent; }}
    .letter-input.correct {{ border-color:#4CAF50; color:#4CAF50; background:#e8f5e9; }}
    .letter-input.wrong {{ border-color:#f44336; color:#f44336; background:#ffebee; }}
    .scrambled-letters {{ font-family:monospace; font-size:18px; font-weight:900;
        letter-spacing:6px; color:#94a3b8; min-width:120px; }}
    .listen-btn {{ padding:8px 16px; background:{ca}; color:#fff; border:none;
        border-radius:10px; font-size:16px; cursor:pointer; font-weight:700; transition:.2s; }}
    .listen-btn:hover {{ transform:scale(1.05); }}

    /* Pronunciation */
    .pron-card {{ display:flex; align-items:center; gap:12px; padding:12px 16px;
        border:2px solid #e2e8f0; border-radius:12px; cursor:pointer;
        background:#fff; transition:.3s; margin-bottom:8px; }}
    .pron-card:hover {{ border-color:#2196F3; background:#e3f2fd;
        transform:translateX(4px); }}
    .pron-emoji {{ font-size:32px; }}
    .pron-word {{ font-size:18px; font-weight:800; color:#0d47a1; }}
    .pron-dots {{ font-size:12px; color:#64748b; }}
    .pron-speaker {{ font-size:20px; margin-left:auto; }}

    .pair-row {{ display:flex; align-items:center; gap:10px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .pair-word {{ padding:8px 14px; border:2px solid #e2e8f0; border-radius:10px;
        cursor:pointer; font-weight:600; background:#fff; transition:.2s; font-size:14px; }}
    .pair-word:hover {{ border-color:#2196F3; background:#e3f2fd; }}
    .pair-vs {{ font-weight:900; color:#94a3b8; font-size:12px; }}
    .pair-btns {{ display:flex; gap:6px; margin-left:auto; }}
    .pair-btn {{ padding:6px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .pair-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .pair-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .pair-btn.disabled {{ pointer-events:none; opacity:.5; }}

    .sent-pron-row {{ display:flex; align-items:center; gap:10px; padding:10px 0;
        border-bottom:1px solid #1A2035; cursor:pointer; transition:.2s; }}
    .sent-pron-row:hover {{ background:#e3f2fd; border-radius:8px; padding-left:8px; }}
    .sent-text {{ flex:1; font-size:16px; font-weight:600; }}

    /* Games */
    .game-score-bar {{ padding:10px 20px; background:#fff3e0;
        font-size:16px; font-weight:700; color:#e65100;
        border-bottom:2px solid #ffe0b2; text-align:center; }}

    .bingo-area {{ text-align:center; }}
    .bingo-grid {{ display:grid; grid-template-columns:repeat(3,1fr);
        gap:8px; max-width:360px; margin:0 auto 12px; }}
    .bingo-card {{ padding:14px; border:3px solid #e2e8f0; border-radius:14px;
        text-align:center; cursor:pointer; background:#fff; transition:.3s; }}
    .bingo-card:hover {{ border-color:{cp}; background:{cb}; }}
    .bingo-card.marked {{ background:#e8f5e9; border-color:#4CAF50; }}
    .bingo-emoji {{ font-size:28px; display:block; }}
    .bingo-word {{ font-weight:700; font-size:13px; color:#94A3B8; }}
    .bingo-speakers {{ display:flex; gap:6px; justify-content:center; flex-wrap:wrap; }}
    .bingo-speak {{ padding:6px 12px; border:2px solid {ca}; border-radius:10px;
        background:#fff; cursor:pointer; font-size:16px; transition:.2s; }}
    .bingo-speak:hover {{ background:{ca}; color:#fff; }}

    .quiz-row {{ display:flex; align-items:center; gap:10px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .quiz-emoji {{ font-size:32px; cursor:pointer; }}
    .quiz-opts {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .quiz-btn {{ padding:8px 16px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:14px; cursor:pointer; background:#fff; transition:.2s; }}
    .quiz-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .quiz-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .quiz-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .quiz-btn.disabled {{ pointer-events:none; opacity:.5; }}

    .memory-grid {{ display:grid; grid-template-columns:repeat(4,1fr);
        gap:8px; max-width:400px; margin:0 auto; }}
    .mem-card {{ width:80px; height:80px; border:3px solid #e2e8f0; border-radius:12px;
        cursor:pointer; position:relative; transition:.3s; background:#fff; }}
    .mem-card:hover {{ border-color:{ca}; }}
    .mem-front {{ position:absolute; inset:0; display:flex; align-items:center;
        justify-content:center; font-size:28px; font-weight:900; color:{ca};
        background:{cb}; border-radius:9px; }}
    .mem-back {{ position:absolute; inset:0; display:flex; align-items:center;
        justify-content:center; font-size:16px; font-weight:700; color:{cp};
        background:#fff; border-radius:9px; opacity:0; }}
    .mem-card.flipped .mem-front {{ opacity:0; }}
    .mem-card.flipped .mem-back {{ opacity:1; }}
    .mem-card.matched {{ border-color:#4CAF50; background:#e8f5e9; pointer-events:none; }}
    .mem-card.matched .mem-front {{ opacity:0; }}
    .mem-card.matched .mem-back {{ opacity:1; }}

    .chain-area {{ text-align:center; padding:10px 0; }}
    .chain-start {{ display:inline-flex; align-items:center; gap:6px;
        padding:10px 18px; background:{cp}10; border-radius:12px;
        font-size:18px; cursor:pointer; margin-bottom:10px; }}
    .chain-arrow {{ font-size:14px; color:#64748b; margin-bottom:10px; }}
    .chain-input {{ width:100%; max-width:300px; padding:10px 14px; border:2px dashed {ca};
        border-radius:10px; font-size:16px; font-weight:600; outline:none;
        text-align:center; }}
    .chain-input:focus {{ border-color:{cp}; background:#111827; }}
    .chain-words {{ margin-top:10px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center; }}
    .chain-word-tag {{ padding:4px 12px; background:{cp}15; color:{cp};
        border-radius:8px; font-weight:600; font-size:13px; }}

    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.12)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-4px)}} 75%{{transform:translateX(4px)}} }}
    .shake {{ animation:shake .3s ease; }}
    @keyframes bounce {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-6px)}} }}
    .bounce {{ animation:bounce .4s ease; }}
    </style>'''


def _ws_scripts() -> str:
    return '''<script>
    var totalScore = 0, totalQ = 0;

    function updateScore(correct) {
        totalQ++;
        if (correct) totalScore++;
        var pct = totalQ > 0 ? Math.round(totalScore / totalQ * 100) : 0;
        var el = document.getElementById('scoreCounter');
        if (el) el.textContent = totalScore + ' / ' + totalQ + ' (' + pct + '%)';
        var gs = document.getElementById('gameScore');
        if (gs) gs.textContent = totalScore;
    }

    function speakWord(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.75; u.pitch = 1.1;
            window.speechSynthesis.speak(u);
        }
    }

    function speakSlow(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.6; u.pitch = 1.1;
            window.speechSynthesis.speak(u);
        }
    }

    function checkAnswer(el) {
        var val = el.value.trim().toLowerCase();
        var ans = el.dataset.answer.toLowerCase().trim();
        if (!val) return;
        if (val === ans) {
            el.classList.remove('wrong');
            el.classList.add('correct','pop');
            el.disabled = true;
            updateScore(true);
        } else {
            el.classList.remove('correct');
            el.classList.add('wrong','shake');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    function checkLetter(el) {
        var val = el.value.trim().toLowerCase();
        var ans = el.dataset.answer.toLowerCase();
        if (!val) return;
        if (val === ans) {
            el.classList.remove('wrong');
            el.classList.add('correct','pop');
            el.disabled = true;
            updateScore(true);
        } else {
            el.classList.remove('correct');
            el.classList.add('wrong','shake');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    function checkSound(el, isCorrect) {
        if (el.classList.contains('disabled')) return;
        el.classList.add('disabled');
        if (isCorrect) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    function checkLetterSort(el, answer, chosen) {
        var parent = el.closest('.sort-row');
        var btns = parent.querySelectorAll('.letter-pick');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (b.textContent.trim() === answer) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    function checkPair(el, answer, chosen) {
        var parent = el.closest('.pair-row');
        var btns = parent.querySelectorAll('.pair-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (!b.classList.contains('wrong')) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    function checkQuiz(el, answer, chosen) {
        var parent = el.closest('.quiz-row');
        var btns = parent.querySelectorAll('.quiz-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (b.textContent.trim() === answer) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    function markBingo(el) {
        el.classList.toggle('marked', key="words_soun_m1");
        el.classList.add('bounce');
        setTimeout(() => el.classList.remove('bounce'), 400);
    }

    /* Dictionary matching */
    var selectedDictWord = null;
    function selectDictWord(el) {
        document.querySelectorAll('.dict-match-item:not(.target)').forEach(
            e => e.classList.remove('selected'));
        el.classList.add('selected');
        selectedDictWord = el.dataset.word;
    }
    function matchDictWord(el, word) {
        if (!selectedDictWord || el.classList.contains('matched')) return;
        if (selectedDictWord === word) {
            el.classList.add('matched','pop');
            document.querySelectorAll('.dict-match-item:not(.target)').forEach(e => {
                if (e.dataset.word === word) e.classList.add('matched','pop');
                e.classList.remove('selected');
            });
            updateScore(true);
        } else {
            el.classList.add('shake');
            setTimeout(() => el.classList.remove('shake'), 400);
            updateScore(false);
        }
        selectedDictWord = null;
    }

    /* Memory match */
    var flipped = [], memLock = false;
    function flipCard(el) {
        if (memLock || el.classList.contains('flipped') || el.classList.contains('matched')) return;
        el.classList.add('flipped');
        flipped.push(el);
        if (flipped.length === 2) {
            memLock = true;
            var a = flipped[0], b = flipped[1];
            if (a.dataset.id === b.dataset.id && a.dataset.idx !== b.dataset.idx) {
                setTimeout(() => {
                    a.classList.add('matched','pop');
                    b.classList.add('matched','pop');
                    updateScore(true);
                    flipped = []; memLock = false;
                }, 500);
            } else {
                setTimeout(() => {
                    a.classList.remove('flipped');
                    b.classList.remove('flipped');
                    updateScore(false);
                    flipped = []; memLock = false;
                }, 800);
            }
        }
    }

    /* Word chain */
    function addChainWord(el, startLetter) {
        var val = el.value.trim().toLowerCase();
        if (!val) return;
        if (val[0] === startLetter) {
            var tag = document.createElement('span');
            tag.className = 'chain-word-tag pop';
            tag.textContent = val;
            tag.onclick = function() { speakWord(val); };
            document.getElementById('chainWords').appendChild(tag);
            el.value = '';
            el.placeholder = "Now starts with '" + val[val.length-1].toUpperCase() + "'...";
            startLetter = val[val.length-1];
            el.onkeydown = function(e) {
                if (e.key === 'Enter') addChainWord(el, startLetter);
            };
            updateScore(true);
        } else {
            el.classList.add('shake');
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_TITLES = [
    "📖 Visual Dictionary",
    "🔤 Phonics Practice",
    "✏️ Spelling Activities",
    "🗣️ Pronunciation Drills",
    "🎮 Review & Games",
]


def build_words_sounds_pages(grade: int, week_num: int,
                              curriculum_weeks: list) -> list[str]:
    """Build Words & Sounds pages for a given grade/week.

    Returns:
        List of 5 HTML strings — one page per activity type.
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[1])
    vocab = week_data.get("vocab", [])[:cfg["vocab_count"]]
    structure = week_data.get("structure", "")
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    if not vocab:
        return []

    unit_num = max(1, (week_num - 1) // 4 + 1)

    styles = _ws_styles(cfg)
    scripts = _ws_scripts()

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>🔊 Words & Sounds — Unit {unit_num}</h1>
            <div class="subtitle">{theme} — {theme_tr} | Week {week_num} | Page {page_num}/5</div>
            <div style="font-size:11px;opacity:.7;margin-top:2px;">{_PAGE_TITLES[page_num - 1]}</div>
        </div>
        <div class="score-bar">
            <div><b>🌟 Score:</b> <span class="counter" id="scoreCounter">0 / 0</span></div>
        </div>'''

    def _wrap(page_num: int, body: str) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{styles}{scripts}</head>
<body>
<div class="page">
    {_header(page_num)}
    {body}
</div>
</body></html>'''

    page1 = _wrap(1, _build_visual_dictionary(vocab, theme, theme_tr, grade, cfg, seed))
    page2 = _wrap(2, _build_phonics_practice(vocab, grade, week_num, cfg, seed))
    page3 = _wrap(3, _build_spelling(vocab, grade, cfg, seed))
    page4 = _wrap(4, _build_pronunciation(vocab, structure, grade, cfg, seed))
    page5 = _wrap(5, _build_review_games(vocab, grade, week_num, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_words_sounds(grade: int, curriculum_weeks: list,
                             selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Words & Sounds book for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_words_sounds_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
