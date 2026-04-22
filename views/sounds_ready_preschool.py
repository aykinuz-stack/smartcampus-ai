# -*- coding: utf-8 -*-
"""Sounds Ready — Okul Öncesi Phonics Hazırlık Kitabı.

Interactive HTML pages for preschool phonics readiness.
Activity types (5 pages per week):
  1. Initial Sound Discovery (Başlangıç sesi bulma)
  2. Sound Repetition & Listening (Ses tekrarları + dinleme odaklı dikkat)
  3. Upper/Lower Case Awareness (Büyük-küçük harf farkındalığı)
  4. Visual-Sound Matching (Görsel-ses eşleştirme)
  5. Phonics Review Game (Ses oyunu — karma tekrar)

All content is dynamically generated from curriculum data.
Each week produces 5 HTML pages — one per activity type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_CFG = {
    "font_size": "22px",
    "color_primary": "#6C63FF",
    "color_accent": "#FF6584",
    "color_bg": "#F0EFFF",
    "color_green": "#43B581",
    "color_orange": "#FF9A3C",
    "color_yellow": "#FFD93D",
    "initial_sound_count": 6,
    "repetition_count": 6,
    "case_count": 8,
    "visual_match_count": 6,
    "review_count": 8,
}


# ══════════════════════════════════════════════════════════════════════════════
# LETTER-SOUND DATA
# ══════════════════════════════════════════════════════════════════════════════

_LETTER_SOUNDS = {
    "A": {"sound": "/æ/", "keyword": "apple", "emoji": "🍎",
           "words": ["ant", "alligator", "astronaut", "arrow", "acorn"]},
    "B": {"sound": "/b/", "keyword": "ball", "emoji": "⚽",
           "words": ["bear", "bus", "bird", "book", "banana"]},
    "C": {"sound": "/k/", "keyword": "cat", "emoji": "🐱",
           "words": ["car", "cup", "cake", "cow", "cloud"]},
    "D": {"sound": "/d/", "keyword": "dog", "emoji": "🐶",
           "words": ["duck", "door", "drum", "doll", "dinosaur"]},
    "E": {"sound": "/ɛ/", "keyword": "elephant", "emoji": "🐘",
           "words": ["egg", "elbow", "engine", "envelope", "exit"]},
    "F": {"sound": "/f/", "keyword": "fish", "emoji": "🐟",
           "words": ["frog", "flower", "fork", "fire", "fan"]},
    "G": {"sound": "/g/", "keyword": "grapes", "emoji": "🍇",
           "words": ["goat", "guitar", "girl", "gate", "gift"]},
    "H": {"sound": "/h/", "keyword": "hat", "emoji": "🎩",
           "words": ["horse", "house", "hand", "heart", "honey"]},
    "I": {"sound": "/ɪ/", "keyword": "igloo", "emoji": "🏠",
           "words": ["insect", "iguana", "ice cream", "island", "ink"]},
    "J": {"sound": "/dʒ/", "keyword": "juice", "emoji": "🧃",
           "words": ["jet", "jam", "jump", "jungle", "jelly"]},
    "K": {"sound": "/k/", "keyword": "kite", "emoji": "🪁",
           "words": ["king", "key", "kangaroo", "kitchen", "koala"]},
    "L": {"sound": "/l/", "keyword": "lion", "emoji": "🦁",
           "words": ["lamp", "leaf", "lemon", "ladder", "ladybug"]},
    "M": {"sound": "/m/", "keyword": "moon", "emoji": "🌙",
           "words": ["monkey", "milk", "map", "mouse", "mountain"]},
    "N": {"sound": "/n/", "keyword": "nest", "emoji": "🪺",
           "words": ["nose", "nut", "nine", "nurse", "noodle"]},
    "O": {"sound": "/ɒ/", "keyword": "octopus", "emoji": "🐙",
           "words": ["orange", "owl", "oven", "olive", "ostrich"]},
    "P": {"sound": "/p/", "keyword": "penguin", "emoji": "🐧",
           "words": ["pig", "pizza", "piano", "pencil", "parrot"]},
    "Q": {"sound": "/kw/", "keyword": "queen", "emoji": "👑",
           "words": ["quilt", "question", "quiet", "quiz", "quarter"]},
    "R": {"sound": "/r/", "keyword": "rainbow", "emoji": "🌈",
           "words": ["rabbit", "rain", "robot", "rocket", "ring"]},
    "S": {"sound": "/s/", "keyword": "sun", "emoji": "☀️",
           "words": ["star", "snake", "sock", "soap", "spider"]},
    "T": {"sound": "/t/", "keyword": "tree", "emoji": "🌳",
           "words": ["tiger", "train", "turtle", "table", "tooth"]},
    "U": {"sound": "/ʌ/", "keyword": "umbrella", "emoji": "☂️",
           "words": ["unicorn", "up", "under", "uncle", "uniform"]},
    "V": {"sound": "/v/", "keyword": "violin", "emoji": "🎻",
           "words": ["van", "vase", "vest", "volcano", "vegetables"]},
    "W": {"sound": "/w/", "keyword": "whale", "emoji": "🐳",
           "words": ["water", "window", "watch", "wind", "worm"]},
    "X": {"sound": "/ks/", "keyword": "xylophone", "emoji": "🎵",
           "words": ["x-ray", "fox", "box", "mix", "six"]},
    "Y": {"sound": "/j/", "keyword": "yacht", "emoji": "⛵",
           "words": ["yellow", "yogurt", "yoyo", "yarn", "yawn"]},
    "Z": {"sound": "/z/", "keyword": "zebra", "emoji": "🦓",
           "words": ["zoo", "zero", "zipper", "zigzag", "zucchini"]},
}

# Emoji map for common preschool words
_EMOJI_MAP = {
    "apple": "🍎", "ant": "🐜", "alligator": "🐊", "arrow": "➡️", "acorn": "🌰",
    "bear": "🐻", "bus": "🚌", "bird": "🐦", "book": "📕", "banana": "🍌", "ball": "⚽",
    "cat": "🐱", "car": "🚗", "cup": "☕", "cake": "🎂", "cow": "🐄", "cloud": "☁️",
    "dog": "🐶", "duck": "🦆", "door": "🚪", "drum": "🥁", "doll": "🪆", "dinosaur": "🦕",
    "egg": "🥚", "elephant": "🐘", "engine": "🚂", "envelope": "✉️",
    "fish": "🐟", "frog": "🐸", "flower": "🌸", "fork": "🍴", "fire": "🔥", "fan": "💨",
    "grapes": "🍇", "goat": "🐐", "guitar": "🎸", "girl": "👧", "gift": "🎁",
    "hat": "🎩", "horse": "🐴", "house": "🏠", "hand": "✋", "heart": "❤️", "honey": "🍯",
    "igloo": "🏠", "insect": "🐛", "ice cream": "🍦", "island": "🏝️",
    "juice": "🧃", "jet": "✈️", "jam": "🫙", "jungle": "🌴", "jelly": "🍮",
    "kite": "🪁", "king": "🤴", "key": "🔑", "kangaroo": "🦘", "koala": "🐨",
    "lion": "🦁", "lamp": "💡", "leaf": "🍃", "lemon": "🍋", "ladybug": "🐞",
    "moon": "🌙", "monkey": "🐵", "milk": "🥛", "map": "🗺️", "mouse": "🐭", "mountain": "⛰️",
    "nest": "🪺", "nose": "👃", "nut": "🥜", "nine": "9️⃣", "noodle": "🍜",
    "octopus": "🐙", "orange": "🍊", "owl": "🦉", "olive": "🫒", "ostrich": "🦩",
    "penguin": "🐧", "pig": "🐷", "pizza": "🍕", "piano": "🎹", "pencil": "✏️", "parrot": "🦜",
    "queen": "👑", "quilt": "🛏️",
    "rainbow": "🌈", "rabbit": "🐰", "rain": "🌧️", "robot": "🤖", "rocket": "🚀", "ring": "💍",
    "sun": "☀️", "star": "⭐", "snake": "🐍", "sock": "🧦", "soap": "🧼", "spider": "🕷️",
    "tree": "🌳", "tiger": "🐯", "train": "🚂", "turtle": "🐢", "table": "🪑", "tooth": "🦷",
    "umbrella": "☂️", "unicorn": "🦄",
    "violin": "🎻", "van": "🚐", "volcano": "🌋", "vegetables": "🥦",
    "whale": "🐳", "water": "💧", "window": "🪟", "watch": "⌚", "wind": "💨", "worm": "🪱",
    "xylophone": "🎵", "x-ray": "🩻", "fox": "🦊", "box": "📦",
    "yacht": "⛵", "yellow": "💛", "yogurt": "🥛", "yoyo": "🪀",
    "zebra": "🦓", "zoo": "🦁", "zero": "0️⃣", "zipper": "🔗",
    # Curriculum vocab extras
    "astronaut": "👨‍🚀", "gate": "🚧", "ladder": "🪜", "nurse": "👩‍⚕️",
    "kitchen": "🍳", "question": "❓", "quiet": "🤫",
    "vase": "🏺", "vest": "🦺", "yarn": "🧶",
}


def _deterministic_seed(week: int) -> int:
    return int(hashlib.md5(f"sr_{week}".encode()).hexdigest()[:8], 16)


def _get_week_letters(week: int) -> list[str]:
    """Return 2-3 focus letters per week, cycling through alphabet."""
    all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    start = ((week - 1) * 3) % 26
    letters = []
    for i in range(3):
        letters.append(all_letters[(start + i) % 26])
    return letters


def _emoji(word: str) -> str:
    return _EMOJI_MAP.get(word.lower(), "📌")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Initial Sound Discovery (Başlangıç sesi bulma)
# ══════════════════════════════════════════════════════════════════════════════

def _build_initial_sound(vocab: list, week: int, seed: int) -> str:
    rng = random.Random(seed)
    letters = _get_week_letters(week)

    rows = ""
    q_num = 0

    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        keyword = data.get("keyword", "")
        emoji = data.get("emoji", "")
        sound = data.get("sound", "")
        words = data.get("words", [])[:4]

        # Add some distractors from other letters
        other_letters = [l for l in _LETTER_SOUNDS if l != letter]
        rng.shuffle(other_letters)
        distractors = []
        for ol in other_letters[:2]:
            d_words = _LETTER_SOUNDS[ol].get("words", [])
            if d_words:
                distractors.append(rng.choice(d_words))

        all_options = words[:3] + distractors
        rng.shuffle(all_options)

        q_num += 1
        # Header for this letter
        rows += f'''
        <div class="letter-section">
            <div class="letter-hero" onclick="speakSlow('{letter}, {sound}, {keyword}')">
                <span class="big-letter">{letter}</span>
                <span class="letter-emoji">{emoji}</span>
                <span class="letter-sound">{sound}</span>
                <span class="letter-keyword">{keyword}</span>
                <span class="speaker-icon">🔊</span>
            </div>
            <div class="instruction">
                🎯 Tap the pictures that start with the <b>"{letter}" {sound}</b> sound!
            </div>
            <div class="sound-grid">'''

        for opt in all_options:
            is_correct = opt.lower().startswith(letter.lower())
            correct_str = "true" if is_correct else "false"
            opt_emoji = _emoji(opt)
            rows += f'''
                <button class="sound-card" onclick="checkSound(this, {correct_str})"
                        data-word="{opt}">
                    <span class="card-emoji">{opt_emoji}</span>
                    <span class="card-word">{opt}</span>
                </button>'''

        rows += '''
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#6C63FF;">
        <div class="section-title" style="background:linear-gradient(135deg,#6C63FF,#8B83FF);">
            <span class="section-icon">🔍</span> Initial Sound Discovery</div>
        <div class="activity-instruction">
            Listen to the letter sound and tap the pictures that start with that sound!
        </div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Sound Repetition & Listening (Ses tekrarları + dinleme)
# ══════════════════════════════════════════════════════════════════════════════

def _build_sound_repetition(vocab: list, week: int, seed: int) -> str:
    rng = random.Random(seed + 10)
    letters = _get_week_letters(week)

    rows = ""

    # Part A: Listen & Repeat
    rows += '<div class="sub-section"><div class="sub-title">🎧 A. Listen & Repeat</div>'
    rows += '<div class="repeat-instruction">Click each card, listen carefully, then repeat the sound out loud!</div>'

    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        keyword = data.get("keyword", "")
        emoji = data.get("emoji", "")
        sound = data.get("sound", "")
        words = data.get("words", [])[:3]

        word_cards = ""
        for w in words:
            w_emoji = _emoji(w)
            word_cards += f'''
                <div class="repeat-word" onclick="speakSlow('{w}')">
                    <span>{w_emoji}</span> <span>{w}</span> <span class="mini-speaker">🔊</span>
                </div>'''

        rows += f'''
        <div class="repeat-row">
            <div class="repeat-letter" onclick="speakSlow('{letter} says {sound}, {keyword}')">
                <span class="rl-letter">{letter}{letter.lower()}</span>
                <span class="rl-emoji">{emoji}</span>
                <span class="rl-sound">{sound}</span>
                <span class="mini-speaker">🔊</span>
            </div>
            <div class="repeat-words">{word_cards}</div>
        </div>'''
    rows += '</div>'

    # Part B: Sound Chain — which word comes next?
    rows += '<div class="sub-section"><div class="sub-title">🔗 B. Sound Chain</div>'
    rows += '<div class="repeat-instruction">Each row has words starting with the same sound. Find the one that does NOT belong!</div>'

    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        words = data.get("words", [])[:3]
        # Add an intruder
        other = [l for l in _LETTER_SOUNDS if l != letter]
        rng.shuffle(other)
        intruder_data = _LETTER_SOUNDS[rng.choice(other)]
        intruder = rng.choice(intruder_data.get("words", ["banana"]))

        options = words + [intruder]
        rng.shuffle(options)

        btns = ""
        for o in options:
            o_emoji = _emoji(o)
            btns += f'''<button class="chain-btn" onclick="checkOddSound(this,'{intruder}','{o}')">
                <span>{o_emoji}</span> {o}
            </button>'''

        rows += f'''
        <div class="chain-row">
            <span class="chain-letter">{letter}</span>
            <div class="chain-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Clap the Syllables
    rows += '<div class="sub-section"><div class="sub-title">👏 C. Clap the Syllables</div>'
    rows += '<div class="repeat-instruction">Click the word, count the syllables, then tap the correct number!</div>'

    _syllable_words = [
        ("cat", 1), ("dog", 1), ("apple", 2), ("banana", 3),
        ("elephant", 3), ("umbrella", 3), ("fish", 1), ("butterfly", 3),
        ("robot", 2), ("dinosaur", 3), ("sun", 1), ("penguin", 2),
        ("kangaroo", 3), ("tiger", 2), ("octopus", 3), ("tree", 1),
    ]
    rng.shuffle(_syllable_words)

    for word, syllables in _syllable_words[:_CFG["repetition_count"]]:
        w_emoji = _emoji(word)
        clap_btns = ""
        for n in range(1, 4):
            clap_btns += f'''<button class="clap-btn" onclick="checkClap(this,{syllables},{n})">
                {"👏" * n} {n}
            </button>'''

        rows += f'''
        <div class="clap-row">
            <div class="clap-word" onclick="speakSlow('{word}')">
                <span>{w_emoji}</span> <b>{word}</b> <span class="mini-speaker">🔊</span>
            </div>
            <div class="clap-options">{clap_btns}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF6584;">
        <div class="section-title" style="background:linear-gradient(135deg,#FF6584,#FF8FA3);">
            <span class="section-icon">🎧</span> Sound Repetition & Listening</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Upper/Lower Case Awareness (Büyük-küçük harf farkındalığı)
# ══════════════════════════════════════════════════════════════════════════════

def _build_case_awareness(vocab: list, week: int, seed: int) -> str:
    rng = random.Random(seed + 20)
    letters = _get_week_letters(week)

    rows = ""

    # Part A: Match upper to lower
    rows += '<div class="sub-section"><div class="sub-title">🔤 A. Match the Letters</div>'
    rows += '<div class="repeat-instruction">Draw a line from each big letter to its small letter!</div>'

    # Use focus letters + some extras
    extra_letters = [l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if l not in letters]
    rng.shuffle(extra_letters)
    all_letters = letters + extra_letters[:3]
    rng.shuffle(all_letters)

    lower_shuffled = [l.lower() for l in all_letters]
    rng.shuffle(lower_shuffled)

    upper_btns = ""
    for l in all_letters:
        upper_btns += f'<button class="case-btn upper-btn" data-letter="{l}" onclick="selectCase(this,\'upper\')">{l}</button>'

    lower_btns = ""
    for l in lower_shuffled:
        lower_btns += f'<button class="case-btn lower-btn" data-letter="{l.upper()}" onclick="selectCase(this,\'lower\')">{l}</button>'

    rows += f'''
    <div class="case-match-area">
        <div class="case-column">
            <div class="case-label">BIG Letters</div>
            {upper_btns}
        </div>
        <div class="case-column">
            <div class="case-label">small letters</div>
            {lower_btns}
        </div>
    </div>'''
    rows += '</div>'

    # Part B: Circle the correct case
    rows += '<div class="sub-section"><div class="sub-title">⭕ B. Find the Matching Pair</div>'
    rows += '<div class="repeat-instruction">Tap the correct lowercase letter for each uppercase letter shown!</div>'

    for letter in letters:
        # Show uppercase, pick correct lowercase + 2 distractors
        others = [l.lower() for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if l != letter]
        rng.shuffle(others)
        options = [letter.lower()] + others[:2]
        rng.shuffle(options)

        btns = ""
        for o in options:
            btns += f'''<button class="case-pick-btn" onclick="checkCasePick(this,'{letter.lower()}','{o}')">
                {o}
            </button>'''

        rows += f'''
        <div class="case-pick-row">
            <span class="case-big">{letter}</span>
            <span class="case-arrow">→</span>
            <div class="case-pick-opts">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Trace the letter (visual)
    rows += '<div class="sub-section"><div class="sub-title">✏️ C. Trace the Letters</div>'
    rows += '<div class="repeat-instruction">Trace each letter with your finger or mouse!</div>'

    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        emoji = data.get("emoji", "")
        rows += f'''
        <div class="trace-row">
            <div class="trace-box">
                <span class="trace-letter" style="color:#e2e8f0;font-size:120px;
                    -webkit-text-stroke:3px #6C63FF;">{letter}</span>
                <span class="trace-small" style="color:#e2e8f0;font-size:120px;
                    -webkit-text-stroke:3px #FF6584;">{letter.lower()}</span>
            </div>
            <div class="trace-info">
                <span>{emoji}</span>
                <span class="trace-word">{data.get("keyword", "")}</span>
                <button class="trace-speak" onclick="speakSlow('{letter}')" title="Listen">🔊</button>
            </div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#43B581;">
        <div class="section-title" style="background:linear-gradient(135deg,#2d8f5e,#43B581);">
            <span class="section-icon">🔤</span> Upper & Lower Case</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Visual-Sound Matching (Görsel-ses eşleştirme)
# ══════════════════════════════════════════════════════════════════════════════

def _build_visual_sound_match(vocab: list, week: int, seed: int) -> str:
    rng = random.Random(seed + 30)
    letters = _get_week_letters(week)

    rows = ""

    # Part A: Which picture starts with this sound?
    rows += '<div class="sub-section"><div class="sub-title">🖼️ A. Picture Sound Match</div>'
    rows += '<div class="repeat-instruction">Listen to the sound and pick ALL pictures that start with it!</div>'

    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        sound = data.get("sound", "")
        words = data.get("words", [])[:3]

        # Get distractors
        other_keys = [l for l in _LETTER_SOUNDS if l != letter]
        rng.shuffle(other_keys)
        distractors = []
        for ok in other_keys[:3]:
            dw = _LETTER_SOUNDS[ok].get("words", [])
            if dw:
                distractors.append(rng.choice(dw))

        all_opts = words + distractors
        rng.shuffle(all_opts)

        cards = ""
        for opt in all_opts:
            is_match = opt.lower().startswith(letter.lower())
            cards += f'''
            <button class="vs-card" onclick="checkSound(this, {'true' if is_match else 'false'})"
                    data-word="{opt}">
                <span class="vs-emoji">{_emoji(opt)}</span>
                <span class="vs-word">{opt}</span>
            </button>'''

        rows += f'''
        <div class="vs-row">
            <div class="vs-prompt" onclick="speakSlow('{letter} says {sound}')">
                <span class="vs-letter">{letter}</span>
                <span class="vs-sound">{sound}</span>
                <span class="mini-speaker">🔊</span>
            </div>
            <div class="vs-options">{cards}</div>
        </div>'''
    rows += '</div>'

    # Part B: Listen & Choose the right letter
    rows += '<div class="sub-section"><div class="sub-title">👂 B. Listen & Choose the Letter</div>'
    rows += '<div class="repeat-instruction">Click the speaker, then choose which letter makes that sound!</div>'

    all_letters_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        keyword = data.get("keyword", "")
        sound = data.get("sound", "")
        emoji = data.get("emoji", "")

        # 3 options: correct + 2 distractors
        distr = [l for l in all_letters_list if l != letter]
        rng.shuffle(distr)
        options = [letter] + distr[:2]
        rng.shuffle(options)

        btns = ""
        for o in options:
            o_data = _LETTER_SOUNDS.get(o, {})
            o_emoji = o_data.get("emoji", "📌")
            btns += f'''<button class="listen-pick-btn" onclick="checkLetterPick(this,'{letter}','{o}')">
                <span class="lp-letter">{o}</span>
                <span class="lp-emoji">{o_emoji}</span>
            </button>'''

        rows += f'''
        <div class="listen-row">
            <button class="listen-speaker" onclick="speakSlow('{keyword}')">
                🔊 <span class="listen-hint">{emoji} ???</span>
            </button>
            <div class="listen-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Rhyme Time
    rows += '<div class="sub-section"><div class="sub-title">🎵 C. Rhyme Time</div>'
    rows += '<div class="repeat-instruction">Which words sound alike at the end? Tap the rhyming pair!</div>'

    _rhyme_pairs = [
        ("cat", "hat"), ("dog", "frog"), ("sun", "fun"), ("bee", "tree"),
        ("star", "car"), ("cake", "lake"), ("ring", "king"), ("moon", "spoon"),
        ("rain", "train"), ("ball", "wall"), ("fish", "dish"), ("bear", "chair"),
    ]
    rng.shuffle(_rhyme_pairs)

    for w1, w2 in _rhyme_pairs[:3]:
        # Add a non-rhyming word
        non_rhyme = rng.choice(["book", "lamp", "cloud", "nose", "hand", "sock"])
        options = [w2, non_rhyme]
        rng.shuffle(options)

        btns = ""
        for o in options:
            btns += f'''<button class="rhyme-btn" onclick="checkRhyme(this,'{w2}','{o}')">
                {_emoji(o)} {o}
            </button>'''

        rows += f'''
        <div class="rhyme-row">
            <div class="rhyme-prompt" onclick="speakSlow('{w1}')">
                {_emoji(w1)} <b>{w1}</b> 🔊
            </div>
            <span class="rhyme-q">rhymes with?</span>
            <div class="rhyme-options">{btns}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF9A3C;">
        <div class="section-title" style="background:linear-gradient(135deg,#e07800,#FF9A3C);">
            <span class="section-icon">🖼️</span> Visual–Sound Matching</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Phonics Review Game (Karma tekrar)
# ══════════════════════════════════════════════════════════════════════════════

def _build_phonics_review(vocab: list, week: int, seed: int) -> str:
    rng = random.Random(seed + 40)
    letters = _get_week_letters(week)

    rows = ""

    # Game 1: Letter Pop — tap the target letter
    rows += '<div class="sub-section"><div class="sub-title">🎯 Game 1: Letter Pop!</div>'
    rows += '<div class="repeat-instruction">Pop only the balloons with the target letter!</div>'

    target = letters[0]
    all_l = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rng.shuffle(all_l)
    balloon_letters = [target] * 4 + [l for l in all_l if l != target][:8]
    rng.shuffle(balloon_letters)

    _balloon_colors = ["#FF6B6B", "#6C63FF", "#43B581", "#FF9A3C", "#FFD93D",
                       "#FF6584", "#00B4D8", "#E040FB", "#7C4DFF", "#FF5722"]

    balloons = ""
    for i, bl in enumerate(balloon_letters):
        color = _balloon_colors[i % len(_balloon_colors)]
        is_target = bl == target
        balloons += f'''<button class="balloon" style="background:{color};"
            onclick="popBalloon(this,{'true' if is_target else 'false'})">{bl}</button>'''

    rows += f'''
    <div class="balloon-game">
        <div class="balloon-target">Find: <span class="target-letter">{target}</span></div>
        <div class="balloon-grid">{balloons}</div>
    </div>'''
    rows += '</div>'

    # Game 2: Sound Bingo
    rows += '<div class="sub-section"><div class="sub-title">🎲 Game 2: Sound Bingo</div>'
    rows += '<div class="repeat-instruction">Click the speaker, then mark the matching picture on your bingo card!</div>'

    bingo_items = []
    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        words = data.get("words", [])[:2]
        for w in words:
            bingo_items.append((w, letter))

    rng.shuffle(bingo_items)
    bingo_items = bingo_items[:6]

    bingo_cards = ""
    for w, letter in bingo_items:
        w_emoji = _emoji(w)
        bingo_cards += f'''
        <div class="bingo-card" onclick="markBingo(this)">
            <span class="bingo-emoji">{w_emoji}</span>
            <span class="bingo-word">{w}</span>
            <span class="bingo-letter">{letter}</span>
        </div>'''

    rows += f'''
    <div class="bingo-grid">{bingo_cards}</div>
    <div class="bingo-speaker-row">'''
    for w, letter in bingo_items:
        rows += f'<button class="bingo-speak-btn" onclick="speakSlow(\'{w}\')">🔊 {_emoji(w)}</button>'
    rows += '</div>'
    rows += '</div>'

    # Game 3: Quick Quiz
    rows += '<div class="sub-section"><div class="sub-title">⚡ Game 3: Quick Quiz</div>'
    rows += '<div class="repeat-instruction">Answer as fast as you can!</div>'

    quiz_items = []
    for letter in letters:
        data = _LETTER_SOUNDS.get(letter, {})
        keyword = data.get("keyword", "")
        emoji = data.get("emoji", "")
        sound = data.get("sound", "")
        quiz_items.append({
            "q": f"What sound does {emoji} <b>{letter}</b> make?",
            "answer": sound,
            "options": [sound, _LETTER_SOUNDS.get(rng.choice([l for l in all_l if l != letter]), {}).get("sound", "/x/")],
        })
        quiz_items.append({
            "q": f"Which word starts with <b>{letter}</b>?",
            "answer": keyword,
            "options": [keyword,
                        _LETTER_SOUNDS.get(rng.choice([l for l in all_l if l != letter]), {}).get("keyword", "banana")],
        })

    for i, qi in enumerate(quiz_items):
        rng.shuffle(qi["options"])
        btns = ""
        for o in qi["options"]:
            btns += f'''<button class="quiz-btn" onclick="checkQuiz(this,'{qi["answer"]}','{o}')">
                {o}
            </button>'''
        rows += f'''
        <div class="quiz-row">
            <span class="q-num">{i+1}</span>
            <span class="quiz-q">{qi["q"]}</span>
            <div class="quiz-opts">{btns}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#7C4DFF;">
        <div class="section-title" style="background:linear-gradient(135deg,#5e35b1,#7C4DFF);">
            <span class="section-icon">🎮</span> Phonics Review Games</div>
        <div class="game-score-bar">
            🌟 Stars: <span class="counter" id="gameStars">0</span>
        </div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _sr_styles() -> str:
    cp = _CFG["color_primary"]
    ca = _CFG["color_accent"]
    cb = _CFG["color_bg"]
    cg = _CFG["color_green"]
    co = _CFG["color_orange"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Segoe UI','Comic Sans MS',sans-serif;
           font-size:{_CFG["font_size"]}; background:{cb}; color:#94A3B8; }}
    .page {{ max-width:860px; margin:0 auto; padding:16px; }}

    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:18px; padding:22px 24px; margin-bottom:14px;
        text-align:center; position:relative;
        box-shadow:0 6px 20px rgba(108,99,255,.3); }}
    .book-header h1 {{ font-size:26px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:14px; opacity:.85; }}
    .book-header .week-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.25); padding:6px 14px; border-radius:20px;
        font-size:13px; font-weight:700; }}
    .book-header .letters-row {{ margin-top:8px; font-size:28px; letter-spacing:10px;
        font-weight:900; text-shadow:2px 2px 4px rgba(0,0,0,.2); }}

    .score-bar {{ background:#fff; border:2px solid {ca}; border-radius:14px;
        padding:12px 18px; margin-bottom:14px; display:flex;
        justify-content:space-between; align-items:center;
        font-size:16px; font-weight:700; }}
    .counter {{ font-weight:900; color:{cp}; font-size:18px; }}

    .section-box {{ background:#fff; border:2px solid #e2e8f0; border-radius:16px;
        margin-bottom:18px; overflow:hidden;
        box-shadow:0 2px 8px rgba(0,0,0,.06); }}
    .section-title {{ color:#fff; padding:14px 20px; font-weight:700;
        font-size:17px; display:flex; align-items:center; gap:8px; }}
    .section-icon {{ font-size:22px; }}

    .activity-instruction {{ padding:12px 20px; background:#111827;
        font-size:14px; color:#64748b; border-bottom:1px solid #e2e8f0;
        font-style:italic; }}

    .sub-section {{ padding:16px 20px; border-bottom:1px solid #1A2035; }}
    .sub-section:last-child {{ border-bottom:none; }}
    .sub-title {{ font-weight:800; color:{cp}; font-size:16px; margin-bottom:12px;
        padding-bottom:8px; border-bottom:3px solid {cp}33; }}
    .repeat-instruction {{ font-size:13px; color:#64748b; margin-bottom:14px;
        font-style:italic; }}

    .q-num {{ background:{cp}; color:#fff; min-width:28px; height:28px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:13px; flex-shrink:0; }}

    /* Letter Hero */
    .letter-section {{ padding:16px 20px; border-bottom:2px solid #1A2035; }}
    .letter-hero {{ display:flex; align-items:center; gap:12px; padding:14px 18px;
        background:linear-gradient(135deg,{cp}15,{ca}10); border-radius:14px;
        cursor:pointer; margin-bottom:12px; transition:.2s; }}
    .letter-hero:hover {{ transform:scale(1.02); box-shadow:0 4px 12px rgba(108,99,255,.2); }}
    .big-letter {{ font-size:64px; font-weight:900; color:{cp};
        text-shadow:2px 2px 4px rgba(0,0,0,.1); }}
    .letter-emoji {{ font-size:40px; }}
    .letter-sound {{ font-size:18px; color:{ca}; font-weight:700;
        background:#fff; padding:4px 12px; border-radius:10px; }}
    .letter-keyword {{ font-size:16px; color:#64748b; font-weight:600; }}
    .speaker-icon {{ font-size:24px; margin-left:auto; }}
    .mini-speaker {{ font-size:14px; cursor:pointer; }}

    .instruction {{ font-size:14px; color:#475569; margin-bottom:10px;
        padding:6px 12px; background:#f0f9ff; border-radius:8px; }}

    /* Sound Grid */
    .sound-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr));
        gap:10px; padding:4px 0; }}
    .sound-card {{ display:flex; flex-direction:column; align-items:center;
        padding:14px 10px; border:3px solid #e2e8f0; border-radius:14px;
        cursor:pointer; background:#fff; transition:.3s; font-size:14px; }}
    .sound-card:hover {{ border-color:{ca}; transform:translateY(-2px);
        box-shadow:0 4px 12px rgba(0,0,0,.1); }}
    .card-emoji {{ font-size:36px; margin-bottom:6px; }}
    .card-word {{ font-weight:700; color:#94A3B8; }}
    .sound-card.correct {{ background:#d1fae5; border-color:{cg};
        animation:pop .3s ease; }}
    .sound-card.wrong {{ background:#fee2e2; border-color:#ef4444;
        animation:shake .3s ease; }}
    .sound-card.disabled {{ pointer-events:none; opacity:.6; }}

    /* Repeat */
    .repeat-row {{ display:flex; gap:14px; align-items:center;
        padding:12px 0; border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .repeat-letter {{ display:flex; align-items:center; gap:8px;
        padding:10px 16px; background:linear-gradient(135deg,{cp}15,{ca}10);
        border-radius:12px; cursor:pointer; transition:.2s; min-width:180px; }}
    .repeat-letter:hover {{ transform:scale(1.03); }}
    .rl-letter {{ font-size:28px; font-weight:900; color:{cp}; }}
    .rl-emoji {{ font-size:24px; }}
    .rl-sound {{ font-size:14px; color:{ca}; font-weight:700; }}
    .repeat-words {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .repeat-word {{ display:flex; align-items:center; gap:6px; padding:8px 14px;
        background:#111827; border:2px solid #e2e8f0; border-radius:10px;
        cursor:pointer; font-size:14px; font-weight:600; transition:.2s; }}
    .repeat-word:hover {{ border-color:{ca}; background:{cb}; }}

    /* Chain */
    .chain-row {{ display:flex; align-items:center; gap:10px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .chain-letter {{ font-size:28px; font-weight:900; color:{cp};
        min-width:40px; text-align:center; }}
    .chain-options {{ display:flex; gap:8px; flex-wrap:wrap; }}
    .chain-btn {{ padding:8px 16px; border:2px solid #e2e8f0; border-radius:12px;
        font-weight:600; font-size:14px; cursor:pointer; background:#fff; transition:.2s; }}
    .chain-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .chain-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .chain-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .chain-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Clap */
    .clap-row {{ display:flex; align-items:center; gap:12px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .clap-word {{ display:flex; align-items:center; gap:6px; font-size:16px;
        cursor:pointer; min-width:140px; }}
    .clap-options {{ display:flex; gap:8px; }}
    .clap-btn {{ padding:8px 16px; border:2px solid #e2e8f0; border-radius:12px;
        font-weight:600; font-size:14px; cursor:pointer; background:#fff; transition:.2s; }}
    .clap-btn:hover {{ border-color:{co}; background:#fff7ed; }}
    .clap-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .clap-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .clap-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Case Awareness */
    .case-match-area {{ display:flex; gap:30px; justify-content:center;
        padding:10px 0; flex-wrap:wrap; }}
    .case-column {{ display:flex; flex-direction:column; gap:8px; align-items:center; }}
    .case-label {{ font-weight:800; color:{cp}; margin-bottom:6px; font-size:14px; }}
    .case-btn {{ width:56px; height:56px; border:3px solid #e2e8f0; border-radius:12px;
        font-size:24px; font-weight:900; cursor:pointer; background:#fff;
        transition:.3s; display:flex; align-items:center; justify-content:center; }}
    .case-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .case-btn.selected {{ border-color:{cp}; background:{cp}22; }}
    .case-btn.matched {{ border-color:{cg}; background:#d1fae5; color:{cg};
        pointer-events:none; }}

    .case-pick-row {{ display:flex; align-items:center; gap:14px; padding:12px 0;
        border-bottom:1px solid #1A2035; }}
    .case-big {{ font-size:42px; font-weight:900; color:{cp}; min-width:60px;
        text-align:center; }}
    .case-arrow {{ font-size:24px; color:#94a3b8; }}
    .case-pick-opts {{ display:flex; gap:8px; }}
    .case-pick-btn {{ width:50px; height:50px; border:3px solid #e2e8f0; border-radius:12px;
        font-size:22px; font-weight:700; cursor:pointer; background:#fff; transition:.2s; }}
    .case-pick-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .case-pick-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .case-pick-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .case-pick-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Trace */
    .trace-row {{ display:flex; align-items:center; gap:20px; padding:16px 0;
        border-bottom:1px solid #1A2035; }}
    .trace-box {{ display:flex; gap:10px; }}
    .trace-info {{ display:flex; align-items:center; gap:10px; font-size:18px; }}
    .trace-word {{ font-weight:700; color:{cp}; }}
    .trace-speak {{ background:none; border:none; font-size:24px; cursor:pointer; }}

    /* Visual-Sound Match */
    .vs-row {{ padding:14px 0; border-bottom:2px solid #1A2035; }}
    .vs-prompt {{ display:inline-flex; align-items:center; gap:10px; padding:10px 18px;
        background:linear-gradient(135deg,{co}20,{co}08); border-radius:12px;
        cursor:pointer; margin-bottom:10px; transition:.2s; }}
    .vs-prompt:hover {{ transform:scale(1.03); }}
    .vs-letter {{ font-size:36px; font-weight:900; color:{co}; }}
    .vs-sound {{ font-size:16px; color:#6b7280; font-weight:600; }}
    .vs-options {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr));
        gap:8px; }}
    .vs-card {{ display:flex; flex-direction:column; align-items:center;
        padding:12px 8px; border:3px solid #e2e8f0; border-radius:12px;
        cursor:pointer; background:#fff; transition:.3s; }}
    .vs-card:hover {{ border-color:{co}; transform:translateY(-2px); }}
    .vs-emoji {{ font-size:30px; margin-bottom:4px; }}
    .vs-word {{ font-weight:600; font-size:13px; color:#94A3B8; }}
    .vs-card.correct {{ background:#d1fae5; border-color:{cg}; }}
    .vs-card.wrong {{ background:#fee2e2; border-color:#ef4444; }}
    .vs-card.disabled {{ pointer-events:none; opacity:.6; }}

    /* Listen & Choose */
    .listen-row {{ display:flex; align-items:center; gap:14px; padding:12px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .listen-speaker {{ padding:10px 20px; background:{ca}; color:#fff;
        border:none; border-radius:12px; font-size:18px; cursor:pointer;
        font-weight:700; transition:.2s; }}
    .listen-speaker:hover {{ transform:scale(1.05); }}
    .listen-hint {{ font-size:14px; }}
    .listen-options {{ display:flex; gap:8px; }}
    .listen-pick-btn {{ display:flex; flex-direction:column; align-items:center;
        padding:10px 16px; border:3px solid #e2e8f0; border-radius:12px;
        cursor:pointer; background:#fff; transition:.2s; }}
    .listen-pick-btn:hover {{ border-color:{ca}; }}
    .lp-letter {{ font-size:28px; font-weight:900; }}
    .lp-emoji {{ font-size:20px; }}
    .listen-pick-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .listen-pick-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .listen-pick-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Rhyme */
    .rhyme-row {{ display:flex; align-items:center; gap:12px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .rhyme-prompt {{ display:flex; align-items:center; gap:6px; font-size:18px;
        cursor:pointer; padding:8px 14px; background:{cp}10; border-radius:10px; }}
    .rhyme-q {{ font-size:14px; color:#64748b; font-style:italic; }}
    .rhyme-options {{ display:flex; gap:8px; }}
    .rhyme-btn {{ padding:10px 18px; border:2px solid #e2e8f0; border-radius:12px;
        font-weight:600; font-size:14px; cursor:pointer; background:#fff; transition:.2s; }}
    .rhyme-btn:hover {{ border-color:{ca}; }}
    .rhyme-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .rhyme-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .rhyme-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Balloon Game */
    .balloon-game {{ text-align:center; }}
    .balloon-target {{ font-size:18px; font-weight:700; margin-bottom:12px;
        color:{cp}; }}
    .target-letter {{ font-size:32px; color:{ca}; }}
    .balloon-grid {{ display:grid; grid-template-columns:repeat(4,1fr);
        gap:10px; max-width:400px; margin:0 auto; }}
    .balloon {{ width:70px; height:70px; border-radius:50%; border:none;
        font-size:24px; font-weight:900; color:#fff; cursor:pointer;
        transition:.3s; box-shadow:0 4px 12px rgba(0,0,0,.15); }}
    .balloon:hover {{ transform:scale(1.1); }}
    .balloon.popped {{ transform:scale(0); opacity:0; transition:.3s; }}
    .balloon.wrong-pop {{ animation:shake .3s ease; opacity:.4; }}

    /* Bingo */
    .bingo-grid {{ display:grid; grid-template-columns:repeat(3,1fr);
        gap:10px; max-width:400px; margin:0 auto 12px; }}
    .bingo-card {{ padding:14px; border:3px solid #e2e8f0; border-radius:14px;
        text-align:center; cursor:pointer; background:#fff; transition:.3s; }}
    .bingo-card:hover {{ border-color:{cp}; background:{cb}; }}
    .bingo-card.marked {{ background:#d1fae5; border-color:{cg}; }}
    .bingo-emoji {{ font-size:32px; display:block; }}
    .bingo-word {{ font-weight:700; font-size:13px; color:#94A3B8; }}
    .bingo-letter {{ font-size:11px; color:#94a3b8; display:block; }}
    .bingo-speaker-row {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }}
    .bingo-speak-btn {{ padding:6px 14px; border:2px solid {ca}; border-radius:10px;
        background:#fff; cursor:pointer; font-size:16px; transition:.2s; }}
    .bingo-speak-btn:hover {{ background:{ca}; color:#fff; }}

    /* Quiz */
    .quiz-row {{ display:flex; align-items:center; gap:10px; padding:10px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .quiz-q {{ flex:1; font-size:15px; }}
    .quiz-opts {{ display:flex; gap:8px; }}
    .quiz-btn {{ padding:8px 18px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:14px; cursor:pointer; background:#fff; transition:.2s; }}
    .quiz-btn:hover {{ border-color:{cp}; background:{cb}; }}
    .quiz-btn.correct {{ background:{cg}; color:#fff; border-color:{cg}; }}
    .quiz-btn.wrong {{ background:#ef4444; color:#fff; border-color:#ef4444; }}
    .quiz-btn.disabled {{ pointer-events:none; opacity:.5; }}

    .game-score-bar {{ padding:10px 20px; background:#faf5ff;
        font-size:16px; font-weight:700; color:{cp};
        border-bottom:2px solid {cp}33; text-align:center; }}

    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.15)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-5px)}} 75%{{transform:translateX(5px)}} }}
    .shake {{ animation:shake .3s ease; }}
    @keyframes bounce {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-8px)}} }}
    .bounce {{ animation:bounce .4s ease; }}
    </style>'''


def _sr_scripts() -> str:
    return '''<script>
    var totalScore = 0, totalQ = 0, stars = 0;

    function updateScore(correct) {
        totalQ++;
        if (correct) { totalScore++; stars++; }
        var pct = totalQ > 0 ? Math.round(totalScore / totalQ * 100) : 0;
        var el = document.getElementById('scoreCounter');
        if (el) el.textContent = totalScore + ' / ' + totalQ + ' (' + pct + '%)';
        var stEl = document.getElementById('gameStars');
        if (stEl) stEl.textContent = stars;
    }

    function speakSlow(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.65; u.pitch = 1.1;
            window.speechSynthesis.speak(u);
        }
    }

    function checkSound(el, isCorrect) {
        if (el.classList.contains('disabled')) return;
        if (isCorrect) {
            el.classList.add('correct','pop','disabled');
            updateScore(true);
            speakSlow(el.dataset.word);
        } else {
            el.classList.add('wrong','shake','disabled');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    function checkOddSound(el, oddWord, chosen) {
        var parent = el.closest('.chain-row');
        var btns = parent.querySelectorAll('.chain-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === oddWord) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (b.textContent.trim().split(' ').pop() === oddWord) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    function checkClap(el, answer, chosen) {
        var parent = el.closest('.clap-row');
        var btns = parent.querySelectorAll('.clap-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (parseInt(b.textContent.trim().slice(-1)) === answer) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    var selectedUpper = null;
    function selectCase(el, type) {
        if (el.classList.contains('matched')) return;
        if (type === 'upper') {
            document.querySelectorAll('.upper-btn').forEach(b => b.classList.remove('selected'));
            el.classList.add('selected');
            selectedUpper = el.dataset.letter;
        } else if (type === 'lower' && selectedUpper) {
            if (el.dataset.letter === selectedUpper) {
                el.classList.add('matched','pop');
                document.querySelectorAll('.upper-btn').forEach(b => {
                    if (b.dataset.letter === selectedUpper) b.classList.add('matched','pop');
                    b.classList.remove('selected');
                });
                updateScore(true);
            } else {
                el.classList.add('shake');
                setTimeout(() => el.classList.remove('shake'), 400);
                updateScore(false);
            }
            selectedUpper = null;
        }
    }

    function checkCasePick(el, answer, chosen) {
        var parent = el.closest('.case-pick-row');
        var btns = parent.querySelectorAll('.case-pick-btn');
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

    function checkLetterPick(el, answer, chosen) {
        var parent = el.closest('.listen-row');
        var btns = parent.querySelectorAll('.listen-pick-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => {
                if (b.querySelector('.lp-letter').textContent.trim() === answer) b.classList.add('correct');
            });
            updateScore(false);
        }
    }

    function checkRhyme(el, answer, chosen) {
        var parent = el.closest('.rhyme-row');
        var btns = parent.querySelectorAll('.rhyme-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (b.textContent.includes(answer)) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    function popBalloon(el, isTarget) {
        if (isTarget) {
            el.classList.add('popped');
            updateScore(true);
        } else {
            el.classList.add('wrong-pop','shake');
            updateScore(false);
            setTimeout(() => el.classList.remove('shake'), 400);
        }
    }

    function markBingo(el) {
        el.classList.toggle('marked', key="sounds_rea_m1");
        el.classList.add('bounce');
        setTimeout(() => el.classList.remove('bounce'), 400);
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
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_TITLES = [
    "🔍 Initial Sound Discovery",
    "🎧 Sound Repetition & Listening",
    "🔤 Upper & Lower Case",
    "🖼️ Visual–Sound Matching",
    "🎮 Phonics Review Games",
]


def build_sounds_ready_pages(week_num: int, curriculum_weeks: list) -> list[str]:
    """Build Sounds Ready pages for a given week.

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

    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(week_num)
    letters = _get_week_letters(week_num)

    styles = _sr_styles()
    scripts = _sr_scripts()

    def _header(page_num: int) -> str:
        letters_display = " ".join(letters)
        return f'''<div class="book-header">
            <div class="week-badge">Week {week_num}</div>
            <h1>🔊 Sounds Ready</h1>
            <div class="subtitle">{theme} — {theme_tr} | Page {page_num}/5</div>
            <div class="letters-row">{letters_display}</div>
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

    page1 = _wrap(1, _build_initial_sound(vocab, week_num, seed))
    page2 = _wrap(2, _build_sound_repetition(vocab, week_num, seed))
    page3 = _wrap(3, _build_case_awareness(vocab, week_num, seed))
    page4 = _wrap(4, _build_visual_sound_match(vocab, week_num, seed))
    page5 = _wrap(5, _build_phonics_review(vocab, week_num, seed))

    return [page1, page2, page3, page4, page5]


def build_full_sounds_ready(curriculum_weeks: list,
                             selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Sounds Ready book for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_sounds_ready_pages(wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
