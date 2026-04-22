# -*- coding: utf-8 -*-
"""Reading Adventures — İlkokul (1-4) Reading Destek Kitabı.

Interactive HTML pages for primary school reading development.
Activity types (5 pages per week):
  1. Short Story (Kısa hikâye + resim destekli okuma)
  2. Daily Life Text (Günlük yaşam metinleri + diyaloglar)
  3. Comprehension Questions (Okuduğunu anlama: ana fikir, detay, D/Y)
  4. Sequencing & Matching (Sıralama + eşleştirme çalışmaları)
  5. Reading Review Game (Karma okuma oyunu — quiz + challenge)

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
    1: {"label": "1st Grade", "font_size": "22px", "sentence_len": "short",
        "story_sentences": 5, "dialog_turns": 3, "comp_questions": 4,
        "seq_items": 4, "review_count": 5,
        "color_primary": "#FF6B6B", "color_accent": "#EE5A24", "color_bg": "#FFF5F5"},
    2: {"label": "2nd Grade", "font_size": "20px", "sentence_len": "short",
        "story_sentences": 6, "dialog_turns": 4, "comp_questions": 5,
        "seq_items": 5, "review_count": 6,
        "color_primary": "#A29BFE", "color_accent": "#6C5CE7", "color_bg": "#F3F0FF"},
    3: {"label": "3rd Grade", "font_size": "18px", "sentence_len": "medium",
        "story_sentences": 8, "dialog_turns": 5, "comp_questions": 6,
        "seq_items": 5, "review_count": 7,
        "color_primary": "#00B894", "color_accent": "#00897B", "color_bg": "#E8F8F5"},
    4: {"label": "4th Grade", "font_size": "16px", "sentence_len": "medium",
        "story_sentences": 10, "dialog_turns": 6, "comp_questions": 7,
        "seq_items": 6, "review_count": 8,
        "color_primary": "#0984E3", "color_accent": "#0652DD", "color_bg": "#EBF5FB"},
}


# ══════════════════════════════════════════════════════════════════════════════
# STORY TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

_STORY_TEMPLATES = {
    "animals": [
        {"title": "The Little {animal}", "emoji": "🐾",
         "sentences": [
             "{name} has a little {animal}.",
             "The {animal} is {color} and {adj}.",
             "Every day, {name} and the {animal} go to the {place}.",
             "They like to {action} together.",
             "The {animal} can {skill} very well.",
             "One day, they see a big {thing} in the {place}.",
             "{name} says, 'Look! A {thing}!'",
             "The {animal} is {emotion} and runs to it.",
             "They play with the {thing} all day.",
             "At the end of the day, they go home happy.",
         ]},
        {"title": "A Day at the {place}", "emoji": "🌳",
         "sentences": [
             "Today is a sunny day.",
             "{name} goes to the {place} with friends.",
             "They see many {animal}s there.",
             "A {color} {animal} is eating {food}.",
             "A baby {animal} is sleeping under a {thing}.",
             "{name} takes a photo of the {animal}.",
             "'It's so {adj}!' says {name}.",
             "They also see a {color} bird in the tree.",
             "The bird sings a beautiful song.",
             "What a wonderful day at the {place}!",
         ]},
    ],
    "school": [
        {"title": "My School Day", "emoji": "🏫",
         "sentences": [
             "{name} wakes up early in the morning.",
             "{name} eats {food} for breakfast.",
             "Then {name} goes to school by {transport}.",
             "At school, {name} sees friends.",
             "The first class is {subject}.",
             "The teacher says, 'Open your {thing}s!'",
             "{name} likes {subject} very much.",
             "At lunch, they eat {food} in the cafeteria.",
             "After school, {name} plays {sport} with friends.",
             "{name} goes home and does homework.",
         ]},
    ],
    "family": [
        {"title": "{name}'s Family", "emoji": "👨‍👩‍👧‍👦",
         "sentences": [
             "{name} has a {adj} family.",
             "There are {number} people in the family.",
             "{name}'s mother likes to {action}.",
             "{name}'s father can {skill} very well.",
             "They have a pet {animal} at home.",
             "On weekends, they go to the {place}.",
             "They like to eat {food} together.",
             "{name} helps mother in the kitchen.",
             "The family is very happy.",
             "They love each other very much.",
         ]},
    ],
    "food": [
        {"title": "The {adj} {food}", "emoji": "🍽️",
         "sentences": [
             "{name} is hungry today.",
             "{name} goes to the kitchen.",
             "Mother is making {food}.",
             "It smells {adj}!",
             "'{name}, do you want some {food}?' asks mother.",
             "'Yes, please!' says {name}.",
             "The {food} is {color} and {adj}.",
             "{name} takes a big bite.",
             "'Mmm, it's {adj}!' says {name}.",
             "{name} eats all the {food}.",
         ]},
    ],
    "weather": [
        {"title": "A {weather} Day", "emoji": "🌤️",
         "sentences": [
             "Today is a {weather} day.",
             "{name} looks out the window.",
             "The sky is {color}.",
             "'{name}, wear your {clothing}!' says mother.",
             "{name} puts on the {clothing} and goes outside.",
             "In the {place}, children are playing.",
             "They are {action} in the {weather}.",
             "A {animal} is hiding under a {thing}.",
             "{name} plays with friends until evening.",
             "What a fun {weather} day!",
         ]},
    ],
}

_FILL_DATA = {
    "name": ["Tom", "Lily", "Jack", "Emma", "Sam", "Mia", "Ben", "Zoe", "Max", "Ava"],
    "animal": ["cat", "dog", "rabbit", "bird", "fish", "turtle", "hamster", "duck"],
    "color": ["red", "blue", "green", "yellow", "brown", "white", "orange", "pink"],
    "adj": ["happy", "little", "big", "beautiful", "funny", "cute", "nice", "good", "delicious", "wonderful"],
    "place": ["park", "garden", "school", "zoo", "beach", "forest", "playground", "farm"],
    "action": ["play", "run", "sing", "dance", "read", "draw", "cook", "swim"],
    "skill": ["run fast", "jump high", "swim", "sing", "dance", "climb trees"],
    "thing": ["tree", "ball", "box", "rock", "flower", "book", "bench", "table"],
    "emotion": ["happy", "excited", "surprised", "curious"],
    "food": ["apple", "pizza", "cake", "sandwich", "soup", "salad", "bread", "rice"],
    "transport": ["bus", "car", "bicycle", "walking"],
    "subject": ["English", "Math", "Art", "Music", "Science"],
    "sport": ["football", "basketball", "tennis", "running"],
    "number": ["four", "five", "six"],
    "weather": ["sunny", "rainy", "snowy", "windy", "cloudy"],
    "clothing": ["coat", "hat", "boots", "scarf", "umbrella", "jacket"],
}


# ══════════════════════════════════════════════════════════════════════════════
# DIALOG TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

_DIALOG_TEMPLATES = [
    {"title": "At the Shop", "emoji": "🛒",
     "speakers": ["Shopkeeper", "Customer"],
     "lines": [
         ("Shopkeeper", "Hello! Can I help you?"),
         ("Customer", "Yes, please. I want a {food}."),
         ("Shopkeeper", "Here you are. It's {number} pounds."),
         ("Customer", "Thank you! Here is the money."),
         ("Shopkeeper", "Thank you! Have a nice day!"),
         ("Customer", "Goodbye!"),
     ]},
    {"title": "Meeting a Friend", "emoji": "🤝",
     "speakers": ["{name}", "{name2}"],
     "lines": [
         ("{name}", "Hi, {name2}! How are you?"),
         ("{name2}", "I'm fine, thank you. And you?"),
         ("{name}", "I'm great! Do you want to play?"),
         ("{name2}", "Yes! Let's go to the {place}."),
         ("{name}", "OK! Let's play {sport}!"),
         ("{name2}", "That's a good idea! Let's go!"),
     ]},
    {"title": "At the Doctor", "emoji": "🏥",
     "speakers": ["Doctor", "Patient"],
     "lines": [
         ("Doctor", "Hello! What's the matter?"),
         ("Patient", "I have a headache."),
         ("Doctor", "Let me check. Open your mouth, please."),
         ("Patient", "OK, doctor."),
         ("Doctor", "You need to rest and drink water."),
         ("Patient", "Thank you, doctor!"),
     ]},
    {"title": "In the Classroom", "emoji": "📚",
     "speakers": ["Teacher", "Student"],
     "lines": [
         ("Teacher", "Good morning, class!"),
         ("Student", "Good morning, teacher!"),
         ("Teacher", "Open your {thing}s to page {number}."),
         ("Student", "OK, teacher. What are we learning today?"),
         ("Teacher", "Today we are learning about {animal}s."),
         ("Student", "That sounds {adj}!"),
     ]},
    {"title": "On the Phone", "emoji": "📱",
     "speakers": ["{name}", "{name2}"],
     "lines": [
         ("{name}", "Hello! Is {name2} there?"),
         ("{name2}", "Hi, {name}! It's me!"),
         ("{name}", "What are you doing?"),
         ("{name2}", "I'm reading a {thing}. And you?"),
         ("{name}", "I'm drawing a {animal}. It's {color}!"),
         ("{name2}", "Cool! Can I see it tomorrow?"),
     ]},
    {"title": "At the Restaurant", "emoji": "🍴",
     "speakers": ["Waiter", "Customer"],
     "lines": [
         ("Waiter", "Welcome! Here is the menu."),
         ("Customer", "Thank you. I'd like some {food}, please."),
         ("Waiter", "Would you like something to drink?"),
         ("Customer", "Yes, some water, please."),
         ("Waiter", "Here you are. Enjoy your meal!"),
         ("Customer", "Thank you very much!"),
     ]},
]

_DAILY_TEXTS = [
    {"title": "My Morning Routine", "emoji": "🌅",
     "text": [
         "I wake up at 7 o'clock every morning.",
         "First, I wash my face and brush my teeth.",
         "Then, I put on my school clothes.",
         "I eat {food} for breakfast.",
         "I drink a glass of milk.",
         "I put my {thing}s in my bag.",
         "I say goodbye to my {animal}.",
         "I walk to the bus stop.",
         "The school bus comes at 8 o'clock.",
         "I sit next to my friend {name}.",
     ]},
    {"title": "My Bedroom", "emoji": "🛏️",
     "text": [
         "This is my bedroom.",
         "It is {adj} and {color}.",
         "There is a bed near the window.",
         "There is a desk next to the bed.",
         "I do my homework at the desk.",
         "There are {thing}s on the shelf.",
         "My {animal} sleeps on my bed.",
         "I have a poster of a {animal} on the wall.",
         "I like my bedroom very much.",
         "It is my favourite room in the house.",
     ]},
    {"title": "The Weather Report", "emoji": "🌤️",
     "text": [
         "Good morning! Here is the weather report.",
         "Today is a {weather} day.",
         "The temperature is {number} degrees.",
         "In the morning, it will be {weather}.",
         "In the afternoon, it will be {adj}.",
         "Please wear your {clothing}.",
         "Tomorrow will be a {weather} day too.",
         "Have a good day!",
     ]},
    {"title": "A Letter to My Friend", "emoji": "✉️",
     "text": [
         "Dear {name},",
         "How are you? I am fine.",
         "I am writing to tell you about my week.",
         "On Monday, I went to the {place}.",
         "On Tuesday, I played {sport} with my friends.",
         "On Wednesday, I ate {food} for dinner.",
         "On Thursday, I read a {thing} about {animal}s.",
         "On Friday, I drew a {color} {animal}.",
         "I hope you are having a good week too!",
         "Your friend, {name2}",
     ]},
]


# ══════════════════════════════════════════════════════════════════════════════
# EMOJI MAP for illustrations
# ══════════════════════════════════════════════════════════════════════════════

_EMOJI_MAP = {
    "cat": "🐱", "dog": "🐶", "rabbit": "🐰", "bird": "🐦", "fish": "🐟",
    "turtle": "🐢", "hamster": "🐹", "duck": "🦆", "park": "🏞️", "garden": "🌻",
    "school": "🏫", "zoo": "🦁", "beach": "🏖️", "forest": "🌲", "playground": "🎠",
    "farm": "🐔", "apple": "🍎", "pizza": "🍕", "cake": "🎂", "sandwich": "🥪",
    "soup": "🍲", "salad": "🥗", "bread": "🍞", "rice": "🍚", "bus": "🚌",
    "car": "🚗", "bicycle": "🚲", "tree": "🌳", "ball": "⚽", "box": "📦",
    "rock": "🪨", "flower": "🌸", "book": "📕", "bench": "🪑", "football": "⚽",
    "basketball": "🏀", "tennis": "🎾", "sunny": "☀️", "rainy": "🌧️",
    "snowy": "❄️", "windy": "💨", "cloudy": "☁️", "coat": "🧥", "hat": "🎩",
    "boots": "👢", "scarf": "🧣", "umbrella": "☂️", "jacket": "🧥",
    "English": "🇬🇧", "Math": "🔢", "Art": "🎨", "Music": "🎵", "Science": "🔬",
}

def _emoji(word: str) -> str:
    return _EMOJI_MAP.get(word, "📌")


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"ra_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _fill_template(text: str, rng: random.Random, vocab: list) -> str:
    """Replace {placeholders} in text with random data, using vocab when possible."""
    result = text
    # Handle {name2} separately
    if "{name2}" in result:
        names = list(_FILL_DATA["name"])
        rng.shuffle(names)
        result = result.replace("{name2}", names[1] if len(names) > 1 else "Alex")

    for key, values in _FILL_DATA.items():
        placeholder = "{" + key + "}"
        while placeholder in result:
            pool = list(values)
            # Integrate vocab words where applicable
            if key in ("food", "animal", "thing", "color") and vocab:
                for v in vocab:
                    if v.lower() not in [p.lower() for p in pool]:
                        pool.append(v.lower())
            rng.shuffle(pool)
            result = result.replace(placeholder, pool[0], 1)
    return result


def _js_safe(text: str) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")


def _base_css(cfg: dict) -> str:
    cp = cfg["color_primary"]
    ca = cfg["color_accent"]
    bg = cfg["color_bg"]
    fs = cfg["font_size"]
    return f"""
    <style>
    /* font: sistem fontu kullaniliyor */
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
        font-family: 'Nunito', sans-serif;
        background: linear-gradient(135deg, {bg} 0%, #f8f9fa 100%);
        color: #2d3436; font-size: {fs};
        padding: 18px;
    }}
    .page-title {{
        text-align:center; font-size:1.7em; font-weight:800;
        background: linear-gradient(135deg, {cp}, {ca});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        margin-bottom:6px;
    }}
    .page-subtitle {{
        text-align:center; font-size:.85em; color:#6b7280;
        margin-bottom:18px;
    }}
    .week-badge {{
        display:inline-block; background:{cp};
        color:#fff; padding:3px 14px; border-radius:20px;
        font-size:.7em; font-weight:700; margin-bottom:12px;
    }}
    .card {{
        background:#fff; border-radius:16px;
        box-shadow:0 4px 15px rgba(0,0,0,.08);
        padding:18px; margin-bottom:16px;
        border-left:5px solid {cp};
        transition: transform .2s;
    }}
    .card:hover {{ transform:translateY(-2px); }}
    .card-title {{
        font-size:1.15em; font-weight:700;
        color:{cp}; margin-bottom:8px;
    }}
    .story-line {{
        background: linear-gradient(135deg, {bg}, #fff);
        padding:10px 16px; border-radius:12px;
        margin:5px 0; font-size:1.0em;
        line-height:1.6; cursor:pointer;
        border:1px solid rgba(0,0,0,.06);
        transition:all .2s;
    }}
    .story-line:hover {{ background:#fff; box-shadow:0 2px 8px rgba(0,0,0,.08); }}
    .dialog-bubble {{
        padding:10px 16px; border-radius:16px;
        margin:6px 0; font-size:.95em; max-width:85%;
        font-weight:600; position:relative;
    }}
    .bubble-left {{
        background:linear-gradient(135deg, #e3f2fd, #bbdefb);
        border:2px solid #90caf9; margin-right:auto;
        border-bottom-left-radius:4px;
    }}
    .bubble-right {{
        background:linear-gradient(135deg, #f3e5f5, #e1bee7);
        border:2px solid #ce93d8; margin-left:auto;
        border-bottom-right-radius:4px;
    }}
    .speaker-label {{
        font-size:.65em; font-weight:800; color:{ca};
        margin-bottom:2px;
    }}
    .question-box {{
        background:#fff; border:2px solid {cp};
        border-radius:14px; padding:14px; margin:10px 0;
    }}
    .q-text {{
        font-weight:700; font-size:1.0em; margin-bottom:8px;
        color:#2d3436;
    }}
    .option-btn {{
        display:block; width:100%; text-align:left;
        padding:10px 16px; margin:4px 0;
        border:2px solid #e0e0e0; border-radius:12px;
        background:#fafafa; cursor:pointer;
        font-family:inherit; font-size:.9em; font-weight:600;
        transition:all .2s;
    }}
    .option-btn:hover {{ border-color:{cp}; background:{bg}; }}
    .btn {{
        display:inline-block; padding:10px 22px;
        border:none; border-radius:25px; cursor:pointer;
        font-family:inherit; font-size:.85em; font-weight:700;
        color:#fff; transition:all .2s;
    }}
    .btn-primary {{ background: linear-gradient(135deg, {cp}, {ca}); }}
    .btn-primary:hover {{ transform:scale(1.05); box-shadow:0 4px 15px rgba(0,0,0,.15); }}
    .btn-speak {{ background: linear-gradient(135deg, #4FC3F7, #00BCD4); }}
    .btn-speak:hover {{ transform:scale(1.05); }}
    .seq-item {{
        display:flex; align-items:center; gap:10px;
        background:#fff; padding:12px 16px; border-radius:12px;
        margin:6px 0; border:2px solid #e0e0e0;
        cursor:grab; font-weight:600; transition:all .2s;
    }}
    .seq-item:hover {{ border-color:{cp}; }}
    .seq-num {{
        background:{cp}; color:#fff;
        width:32px; height:32px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:.85em; font-weight:800; flex-shrink:0;
    }}
    .match-left, .match-right {{
        display:inline-block; padding:10px 16px;
        border:2px solid #e0e0e0; border-radius:12px;
        margin:4px; cursor:pointer; font-weight:600;
        transition:all .2s; min-width:120px; text-align:center;
    }}
    .match-left:hover {{ border-color:{cp}; background:{bg}; }}
    .match-right:hover {{ border-color:{ca}; background:#fff3e0; }}
    .tf-btn {{
        display:inline-block; padding:10px 24px;
        border:2px solid #e0e0e0; border-radius:20px;
        cursor:pointer; font-weight:700; margin:4px 8px;
        transition:all .2s; font-size:.9em;
    }}
    .tf-true {{ color:#27ae60; }}
    .tf-true:hover {{ border-color:#27ae60; background:#e8f5e9; }}
    .tf-false {{ color:#e74c3c; }}
    .tf-false:hover {{ border-color:#e74c3c; background:#fce4ec; }}
    .feedback {{ margin-top:6px; font-weight:700; display:none; font-size:.9em; }}
    .score-bar {{
        text-align:center; font-size:1.5em; font-weight:800;
        color:{cp}; margin:16px 0;
    }}
    .illustration {{
        text-align:center; font-size:3em; margin:10px 0;
        filter:drop-shadow(0 2px 4px rgba(0,0,0,.1));
    }}
    </style>"""


def _tts_script() -> str:
    return """
    <script>
    function speak(text, rate) {
        rate = rate || 0.75;
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-US'; u.rate = rate; u.pitch = 1.0;
        window.speechSynthesis.speak(u);
    }
    function speakSlow(text) { speak(text, 0.6); }
    function speakNormal(text) { speak(text, 0.8); }

    var totalQ = 0, correctQ = 0;

    function checkOption(btn, correct, fbId) {
        var parent = btn.parentElement;
        var btns = parent.querySelectorAll('.option-btn');
        btns.forEach(function(b){ b.disabled = true; b.style.opacity='0.5'; });
        totalQ++;
        var fb = document.getElementById(fbId);
        if(correct) {
            btn.style.background = '#d4edda'; btn.style.borderColor = '#27ae60';
            btn.style.opacity = '1';
            correctQ++;
            if(fb){ fb.innerHTML = '✅ Correct!'; fb.style.color = '#27ae60'; }
        } else {
            btn.style.background = '#f8d7da'; btn.style.borderColor = '#e74c3c';
            btn.style.opacity = '1';
            if(fb){ fb.innerHTML = '❌ Not quite!'; fb.style.color = '#e74c3c'; }
        }
        if(fb) fb.style.display = 'block';
        updateScore();
    }

    function checkTF(btn, correct, fbId) {
        totalQ++;
        var fb = document.getElementById(fbId);
        var parent = btn.parentElement;
        var btns = parent.querySelectorAll('.tf-btn');
        btns.forEach(function(b){ b.style.pointerEvents='none'; b.style.opacity='0.5'; });
        if(correct) {
            btn.style.background = '#d4edda'; btn.style.borderColor = '#27ae60';
            btn.style.opacity = '1';
            correctQ++;
            if(fb){ fb.innerHTML = '✅ True!'; fb.style.color = '#27ae60'; }
        } else {
            btn.style.background = '#f8d7da'; btn.style.borderColor = '#e74c3c';
            btn.style.opacity = '1';
            if(fb){ fb.innerHTML = '❌ False!'; fb.style.color = '#e74c3c'; }
        }
        if(fb) fb.style.display = 'block';
        updateScore();
    }

    function checkMatch(el, pairId) {
        if(!window._matchSel) window._matchSel = null;
        if(!window._matchSel) {
            window._matchSel = {el: el, pair: pairId};
            el.style.borderColor = '#ff9800'; el.style.background = '#fff3e0';
        } else {
            if(window._matchSel.pair === pairId && window._matchSel.el !== el) {
                window._matchSel.el.style.background = '#d4edda';
                window._matchSel.el.style.borderColor = '#27ae60';
                window._matchSel.el.style.pointerEvents = 'none';
                el.style.background = '#d4edda';
                el.style.borderColor = '#27ae60';
                el.style.pointerEvents = 'none';
                correctQ++; totalQ++;
                updateScore();
            } else {
                window._matchSel.el.style.borderColor = '#e74c3c';
                el.style.borderColor = '#e74c3c';
                totalQ++;
                setTimeout(function(){
                    window._matchSel.el.style.borderColor = '#e0e0e0';
                    window._matchSel.el.style.background = '#fff';
                    el.style.borderColor = '#e0e0e0';
                }, 800);
                updateScore();
            }
            window._matchSel = null;
        }
    }

    function updateScore() {
        var el = document.getElementById('scoreDisplay');
        if(el) {
            var pct = totalQ > 0 ? Math.round(correctQ/totalQ*100) : 0;
            var stars = pct >= 80 ? '⭐⭐⭐' : pct >= 60 ? '⭐⭐' : pct >= 40 ? '⭐' : '';
            el.innerHTML = correctQ + '/' + totalQ + ' ' + stars;
        }
    }
    </script>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Short Story (Kısa hikâye + resim destekli okuma)
# ══════════════════════════════════════════════════════════════════════════════

def _build_story_page(vocab: list, theme: str, theme_tr: str,
                      grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)

    # Pick a story category based on theme keywords
    category = "animals"
    theme_lower = theme.lower()
    for cat in _STORY_TEMPLATES:
        if cat in theme_lower:
            category = cat
            break

    templates = _STORY_TEMPLATES.get(category, _STORY_TEMPLATES["animals"])
    template = rng.choice(templates)
    title = _fill_template(template["title"], rng, vocab)
    emoji_icon = template["emoji"]

    max_sent = cfg["story_sentences"]
    sentences = template["sentences"][:max_sent]
    filled = [_fill_template(s, rng, vocab) for s in sentences]

    lines_html = ""
    for i, sent in enumerate(filled):
        lines_html += f"""
        <div class="story-line" onclick="speakNormal('{_js_safe(sent)}')">
            <span style="color:{cfg['color_accent']};font-weight:800;margin-right:6px;">
                {i+1}.
            </span>
            {sent}
        </div>"""

    # Vocab highlight
    vocab_html = ""
    for w in vocab[:6]:
        vocab_html += f"""
        <span style="display:inline-block;background:{cfg['color_bg']};
              border:2px solid {cfg['color_primary']};padding:4px 12px;
              border-radius:16px;margin:3px;cursor:pointer;font-weight:700;
              font-size:.85em;"
              onclick="speakSlow('{_js_safe(w)}')">
            {_emoji(w)} {w}
        </span>"""

    # Read-aloud full story
    full_text = " ".join(filled)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">📖 Short Story</div>
    <div class="page-subtitle">Read and listen! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>

    <div class="card">
        <div class="card-title">{emoji_icon} {title}</div>
        <div class="illustration">{emoji_icon}</div>
        {lines_html}
        <div style="text-align:center;margin-top:14px;">
            <button class="btn btn-primary"
                    onclick="speakNormal('{_js_safe(full_text)}')">
                🔊 Read Aloud (Full Story)
            </button>
        </div>
    </div>

    <div class="card" style="border-left-color:{cfg['color_accent']};">
        <div class="card-title">📝 Key Words</div>
        <p style="font-size:.82em;color:#6b7280;">Tap each word to hear:</p>
        <div style="text-align:center;">{vocab_html}</div>
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Daily Life Text & Dialogs
# ══════════════════════════════════════════════════════════════════════════════

def _build_daily_dialog_page(vocab: list, theme: str, theme_tr: str,
                              grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 1)

    # Daily text
    daily = rng.choice(_DAILY_TEXTS)
    daily_title = daily["title"]
    daily_emoji = daily["emoji"]
    max_lines = cfg["story_sentences"]
    daily_lines = daily["text"][:max_lines]
    filled_daily = [_fill_template(l, rng, vocab) for l in daily_lines]

    daily_html = ""
    for line in filled_daily:
        daily_html += f"""
        <div class="story-line" onclick="speakNormal('{_js_safe(line)}')">
            {line}
        </div>"""

    full_daily = " ".join(filled_daily)

    # Dialog
    dialog_tmpl = rng.choice(_DIALOG_TEMPLATES)
    dialog_title = dialog_tmpl["title"]
    dialog_emoji = dialog_tmpl["emoji"]
    max_turns = cfg["dialog_turns"]
    dialog_lines = dialog_tmpl["lines"][:max_turns]

    names = list(_FILL_DATA["name"])
    rng.shuffle(names)

    dialog_html = ""
    for i, (speaker, line) in enumerate(dialog_lines):
        sp = _fill_template(speaker, rng, vocab)
        ln = _fill_template(line, rng, vocab)
        side = "left" if i % 2 == 0 else "right"
        dialog_html += f"""
        <div style="display:flex;justify-content:{'flex-start' if side == 'left' else 'flex-end'};">
            <div class="dialog-bubble bubble-{side}" onclick="speakNormal('{_js_safe(ln)}')">
                <div class="speaker-label">{sp}</div>
                {ln}
            </div>
        </div>"""

    full_dialog = " ".join([_fill_template(l, rng, vocab) for _, l in dialog_lines])

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">📰 Daily Life Reading</div>
    <div class="page-subtitle">Read about everyday situations! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>

    <div class="card">
        <div class="card-title">{daily_emoji} {daily_title}</div>
        {daily_html}
        <div style="text-align:center;margin-top:12px;">
            <button class="btn btn-primary"
                    onclick="speakNormal('{_js_safe(full_daily)}')">
                🔊 Listen to Full Text
            </button>
        </div>
    </div>

    <div class="card" style="border-left-color:#CE93D8;">
        <div class="card-title">{dialog_emoji} Dialog: {dialog_title}</div>
        <div style="padding:6px 0;">{dialog_html}</div>
        <div style="text-align:center;margin-top:10px;">
            <button class="btn btn-speak"
                    onclick="speakNormal('{_js_safe(full_dialog)}')">
                🔊 Listen to Dialog
            </button>
        </div>
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Comprehension Questions (Ana fikir, detay, D/Y)
# ══════════════════════════════════════════════════════════════════════════════

def _build_comprehension_page(vocab: list, theme: str, theme_tr: str,
                               grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 2)

    # Generate a short story for comprehension
    category = "animals"
    for cat in _STORY_TEMPLATES:
        if cat in theme.lower():
            category = cat
            break
    templates = _STORY_TEMPLATES.get(category, _STORY_TEMPLATES["animals"])
    tmpl = rng.choice(templates)
    max_sent = cfg["story_sentences"]
    sentences = [_fill_template(s, rng, vocab) for s in tmpl["sentences"][:max_sent]]
    title = _fill_template(tmpl["title"], rng, vocab)
    full_text = " ".join(sentences)

    # Display story briefly
    story_html = ""
    for s in sentences:
        story_html += f'<div class="story-line" onclick="speakNormal(\'{_js_safe(s)}\')">{s}</div>'

    # Generate questions
    questions_html = ""
    q_num = 0

    # Q1: Main idea (multiple choice)
    q_num += 1
    main_idea = f"The story is about {_fill_template('{name}', rng, vocab)} and a {_fill_template('{animal}', rng, vocab)}."
    wrong1 = f"The story is about cooking {_fill_template('{food}', rng, vocab)}."
    wrong2 = f"The story is about going to the {_fill_template('{place}', rng, vocab)}."
    opts = [main_idea, wrong1, wrong2]
    rng.shuffle(opts)
    opts_html = ""
    for opt in opts:
        correct = "true" if opt == main_idea else "false"
        opts_html += f"""
        <button class="option-btn" onclick="checkOption(this,{correct},'fb_{q_num}')">
            {opt}
        </button>"""
    questions_html += f"""
    <div class="question-box">
        <div class="q-text">❓ Q{q_num}. What is the main idea of the story?</div>
        {opts_html}
        <div class="feedback" id="fb_{q_num}"></div>
    </div>"""

    # Q2-Q3: Detail questions (MCQ)
    for i in range(min(2, cfg["comp_questions"] - 1)):
        q_num += 1
        if i == 0 and len(sentences) > 1:
            q_text = f"In sentence 2, what is described?"
            correct_ans = sentences[1] if len(sentences) > 1 else "Something happens."
            # Shorten
            correct_short = correct_ans[:60] + "..." if len(correct_ans) > 60 else correct_ans
            w1 = _fill_template("A {color} {animal} goes to school.", rng, vocab)
            w2 = _fill_template("{name} eats {food} for dinner.", rng, vocab)
        else:
            q_text = "What happens at the end of the story?"
            correct_short = sentences[-1][:60] + "..." if len(sentences[-1]) > 60 else sentences[-1]
            w1 = _fill_template("{name} goes to sleep.", rng, vocab)
            w2 = _fill_template("It starts to rain.", rng, vocab)

        opts = [correct_short, w1, w2]
        rng.shuffle(opts)
        opts_html = ""
        for opt in opts:
            correct = "true" if opt == correct_short else "false"
            opts_html += f"""
            <button class="option-btn" onclick="checkOption(this,{correct},'fb_{q_num}')">
                {opt}
            </button>"""
        questions_html += f"""
        <div class="question-box">
            <div class="q-text">❓ Q{q_num}. {q_text}</div>
            {opts_html}
            <div class="feedback" id="fb_{q_num}"></div>
        </div>"""

    # Q4+: True/False questions
    tf_statements = []
    if len(sentences) > 0:
        tf_statements.append((sentences[0], True))
    tf_statements.append((_fill_template("{name} flies to the moon.", rng, vocab), False))
    if len(sentences) > 2:
        tf_statements.append((sentences[2], True))
    tf_statements.append((_fill_template("The {animal} can talk.", rng, vocab), False))
    tf_statements.append((_fill_template("{name} has ten {animal}s.", rng, vocab), False))

    for stmt, is_true in tf_statements[:cfg["comp_questions"] - q_num]:
        q_num += 1
        questions_html += f"""
        <div class="question-box">
            <div class="q-text">❓ Q{q_num}. True or False?</div>
            <p style="font-weight:600;font-size:.95em;margin:6px 0;">"{stmt}"</p>
            <div>
                <span class="tf-btn tf-true"
                      onclick="checkTF(this,{'true' if is_true else 'false'},'fb_{q_num}')">
                    ✅ True
                </span>
                <span class="tf-btn tf-false"
                      onclick="checkTF(this,{'true' if not is_true else 'false'},'fb_{q_num}')">
                    ❌ False
                </span>
            </div>
            <div class="feedback" id="fb_{q_num}"></div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">❓ Comprehension</div>
    <div class="page-subtitle">Read the story, then answer! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>

    <div class="card">
        <div class="card-title">📖 {title}</div>
        {story_html}
        <div style="text-align:center;margin-top:10px;">
            <button class="btn btn-primary" onclick="speakNormal('{_js_safe(full_text)}')">
                🔊 Listen
            </button>
        </div>
    </div>

    <div class="score-bar" id="scoreDisplay">0/0</div>

    {questions_html}

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Sequencing & Matching
# ══════════════════════════════════════════════════════════════════════════════

def _build_sequencing_page(vocab: list, theme: str, theme_tr: str,
                            grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 3)

    # Sequencing: put sentences in order
    seq_sentences = [
        _fill_template("{name} wakes up in the morning.", rng, vocab),
        _fill_template("{name} eats breakfast.", rng, vocab),
        _fill_template("{name} goes to school.", rng, vocab),
        _fill_template("{name} studies in class.", rng, vocab),
        _fill_template("{name} plays with friends.", rng, vocab),
        _fill_template("{name} goes home.", rng, vocab),
    ][:cfg["seq_items"]]

    correct_order = list(range(len(seq_sentences)))
    shuffled = list(correct_order)
    rng.shuffle(shuffled)

    seq_html = ""
    for display_idx, orig_idx in enumerate(shuffled):
        seq_html += f"""
        <div class="seq-item" onclick="speakNormal('{_js_safe(seq_sentences[orig_idx])}')">
            <div class="seq-num">?</div>
            <span>{seq_sentences[orig_idx]}</span>
        </div>"""

    # Answer reveal
    answer_html = ""
    for i, sent in enumerate(seq_sentences):
        answer_html += f"""
        <div class="seq-item" style="border-color:{cfg['color_primary']};">
            <div class="seq-num">{i+1}</div>
            <span>{sent}</span>
        </div>"""

    # Matching: word-picture pairs
    match_words = vocab[:5] if len(vocab) >= 5 else ["cat", "dog", "apple", "book", "sun"]
    match_pairs = [(w, _emoji(w)) for w in match_words]
    rng_copy = random.Random(seed + 33)

    left_items = list(match_pairs)
    right_items = list(match_pairs)
    rng_copy.shuffle(right_items)

    left_html = ""
    right_html = ""
    for i, (word, em) in enumerate(left_items):
        left_html += f"""
        <div class="match-left" onclick="checkMatch(this,'{_js_safe(word)}')" style="display:block;margin:6px 0;">
            📝 {word}
        </div>"""
    for i, (word, em) in enumerate(right_items):
        right_html += f"""
        <div class="match-right" onclick="checkMatch(this,'{_js_safe(word)}')" style="display:block;margin:6px 0;">
            {em} {word[0]}...
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">🔢 Sequencing & Matching</div>
    <div class="page-subtitle">Put in order and match! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>

    <div class="score-bar" id="scoreDisplay">0/0</div>

    <div class="card">
        <div class="card-title">🔢 Put the Story in Order</div>
        <p style="font-size:.82em;color:#6b7280;margin-bottom:8px;">
            Read each sentence and think about the correct order. Tap to listen!
        </p>
        {seq_html}
        <details style="margin-top:12px;">
            <summary style="cursor:pointer;color:{cfg['color_primary']};font-weight:700;">
                ✅ Show Correct Order
            </summary>
            <div style="margin-top:8px;">{answer_html}</div>
        </details>
    </div>

    <div class="card" style="border-left-color:{cfg['color_accent']};">
        <div class="card-title">🔗 Match Words with Pictures</div>
        <p style="font-size:.82em;color:#6b7280;margin-bottom:8px;">
            Tap a word, then tap the matching picture!
        </p>
        <div style="display:flex;gap:16px;">
            <div style="flex:1;">{left_html}</div>
            <div style="flex:1;">{right_html}</div>
        </div>
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Reading Review Game
# ══════════════════════════════════════════════════════════════════════════════

def _build_review_game_page(vocab: list, theme: str, theme_tr: str,
                             grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 4)

    # Speed reading challenge
    speed_words = list(vocab[:8]) if len(vocab) >= 8 else list(vocab) + ["happy", "big", "run", "play", "eat", "go", "see", "like"]
    speed_words = speed_words[:8]
    rng.shuffle(speed_words)

    speed_html = ""
    for w in speed_words:
        speed_html += f"""
        <div style="display:inline-block;text-align:center;margin:8px;cursor:pointer;"
             onclick="speakNormal('{_js_safe(w)}')">
            <div style="font-size:1.6em;background:linear-gradient(135deg,#fff9c4,#ffe0b2);
                        width:80px;height:80px;border-radius:16px;display:flex;
                        align-items:center;justify-content:center;margin:auto;
                        border:2px solid #ffcc02;font-weight:800;
                        color:{cfg['color_primary']};">{w}</div>
        </div>"""

    # Sentence completion quiz
    quiz_html = ""
    completions = [
        ("The {animal} is ___.", ["big", "happy", "small"], ["car", "table"]),
        ("{name} goes to the ___.", ["park", "school", "shop"], ["running", "sleeping"]),
        ("I like to eat ___.", ["apple", "pizza", "cake"], ["chair", "book"]),
        ("The sky is ___.", ["blue", "cloudy", "sunny"], ["hungry", "tall"]),
        ("My friend is very ___.", ["kind", "funny", "smart"], ["rainy", "round"]),
        ("We play in the ___.", ["garden", "playground", "park"], ["pencil", "milk"]),
        ("The {animal} can ___.", ["run", "jump", "swim"], ["read", "drive"]),
        ("I drink ___ in the morning.", ["milk", "water", "juice"], ["desk", "door"]),
    ]
    rng.shuffle(completions)
    for i, (sent, corrects, wrongs) in enumerate(completions[:cfg["review_count"]]):
        filled_sent = _fill_template(sent, rng, vocab)
        correct_word = rng.choice(corrects)
        wrong_word = rng.choice(wrongs)
        another_correct = rng.choice([c for c in corrects if c != correct_word])

        opts = [correct_word, wrong_word, another_correct]
        rng.shuffle(opts)

        opts_html = ""
        for opt in opts:
            is_correct = "true" if opt in corrects else "false"
            opts_html += f"""
            <button class="option-btn" style="display:inline-block;width:auto;padding:8px 18px;"
                    onclick="checkOption(this,{is_correct},'rfb_{i}')">
                {opt}
            </button>"""

        quiz_html += f"""
        <div class="question-box">
            <div class="q-text">📝 {filled_sent}</div>
            <div>{opts_html}</div>
            <div class="feedback" id="rfb_{i}"></div>
        </div>"""

    # Word search hint
    ws_words = vocab[:5] if len(vocab) >= 5 else ["cat", "dog", "sun", "hat", "red"]
    ws_html = ""
    for w in ws_words:
        letters_html = ""
        for ch in w.upper():
            letters_html += f"""
            <span style="display:inline-block;width:36px;height:36px;
                         background:#fff;border:2px solid {cfg['color_primary']};
                         border-radius:8px;text-align:center;line-height:36px;
                         font-weight:800;font-size:1.1em;margin:2px;
                         color:{cfg['color_primary']};">{ch}</span>"""
        ws_html += f"""
        <div style="margin:8px 0;cursor:pointer;" onclick="speakSlow('{_js_safe(w)}')">
            {letters_html}
            <span style="font-size:.75em;color:#6b7280;margin-left:8px;">({w})</span>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">🎮 Reading Review</div>
    <div class="page-subtitle">Test your reading skills! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>

    <div class="score-bar" id="scoreDisplay">0/0</div>

    <div class="card" style="border-left-color:#FFD93D;">
        <div class="card-title">⚡ Speed Reading Challenge</div>
        <p style="font-size:.82em;color:#6b7280;">Read each word as fast as you can! Tap to hear:</p>
        <div style="text-align:center;">{speed_html}</div>
    </div>

    <div class="card">
        <div class="card-title">📝 Complete the Sentence</div>
        <p style="font-size:.82em;color:#6b7280;">Choose the best word to complete each sentence:</p>
        {quiz_html}
    </div>

    <div class="card" style="border-left-color:{cfg['color_accent']};">
        <div class="card-title">🔍 Spell & Read</div>
        <p style="font-size:.82em;color:#6b7280;">Read each word letter by letter, then say the word!</p>
        {ws_html}
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_NAMES = [
    "📖 Short Story",
    "📰 Daily Life Text",
    "❓ Comprehension",
    "🔢 Sequencing & Matching",
    "🎮 Reading Review",
]


def build_reading_adventures_pages(grade: int, week_num: int,
                                    curriculum_weeks: list) -> list[str]:
    """Build 5 Reading Adventures pages for a given grade/week.

    Returns list of 5 HTML strings.
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[1])
    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    return [
        _build_story_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_daily_dialog_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_comprehension_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_sequencing_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_review_game_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
    ]


def build_full_reading_adventures(grade: int, curriculum_weeks: list,
                                   selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Reading Adventures book for all weeks.

    Returns list of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    result = []
    for w in curriculum_weeks:
        wn = w.get("week", 0)
        if selected_weeks and wn not in selected_weeks:
            continue
        pages = build_reading_adventures_pages(grade, wn, curriculum_weeks)
        if pages:
            result.append({
                "week": wn,
                "theme": w.get("theme", f"Week {wn}"),
                "pages": pages,
            })
    return result
