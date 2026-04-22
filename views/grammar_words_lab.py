# -*- coding: utf-8 -*-
"""Grammar & Words Lab — Ortaokul (5-8) Grammar + Vocabulary Destek Kitabı.

Interactive HTML exercise pages for middle school grammar & vocabulary mastery.
Exercise types (5 pages per week):
  1. Structure Lab (Tense yapıları, Modals, Comparisons, Prepositions)
  2. Word Families & Collocations (Kelime aileleri + eşdizimli kullanımlar)
  3. Theme Vocabulary Workshop (Tema bazlı kelime çalışmaları)
  4. Schema & Table Drills (Şema/tablo destekli yapı kontrolü)
  5. Topic Test (Konu sonu test — grammar + vocabulary)

All content is dynamically generated from curriculum data.
Each week produces 5 HTML pages — one per exercise type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# GRADE-LEVEL CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_GRADE_CFG = {
    5: {"label": "5th Grade", "font_size": "15px", "vocab_count": 12,
        "structure_count": 8, "family_count": 6, "theme_count": 8,
        "table_count": 6, "test_count": 15,
        "color_primary": "#00695c", "color_accent": "#26a69a", "color_bg": "#e0f2f1"},
    6: {"label": "6th Grade", "font_size": "14px", "vocab_count": 14,
        "structure_count": 10, "family_count": 8, "theme_count": 10,
        "table_count": 8, "test_count": 18,
        "color_primary": "#4527a0", "color_accent": "#7e57c2", "color_bg": "#ede7f6"},
    7: {"label": "7th Grade", "font_size": "14px", "vocab_count": 16,
        "structure_count": 10, "family_count": 8, "theme_count": 10,
        "table_count": 8, "test_count": 18,
        "color_primary": "#bf360c", "color_accent": "#ff7043", "color_bg": "#fbe9e7"},
    8: {"label": "8th Grade", "font_size": "13px", "vocab_count": 18,
        "structure_count": 12, "family_count": 10, "theme_count": 12,
        "table_count": 10, "test_count": 20,
        "color_primary": "#1565c0", "color_accent": "#42a5f5", "color_bg": "#e3f2fd"},
}

# Grammar structure templates by category
_GRAMMAR_CATEGORIES = {
    "tenses": {
        "label": "Tenses",
        "icon": "⏰",
        "patterns": [
            ("Present Simple", "S + V1 / V1+s", "She {v}s every day.", "She doesn't {v} every day."),
            ("Present Continuous", "S + am/is/are + V-ing", "He is {v}ing now.", "He isn't {v}ing now."),
            ("Past Simple", "S + V2", "They {v}ed yesterday.", "They didn't {v} yesterday."),
            ("Future (will)", "S + will + V1", "I will {v} tomorrow.", "I won't {v} tomorrow."),
            ("Future (going to)", "S + am/is/are + going to + V1", "She is going to {v}.", "She isn't going to {v}."),
            ("Present Perfect", "S + have/has + V3", "We have {v}ed.", "We haven't {v}ed."),
        ],
    },
    "modals": {
        "label": "Modals",
        "icon": "🔑",
        "patterns": [
            ("can", "ability", "I can {v}.", "I can't {v}."),
            ("must", "obligation", "You must {v}.", "You mustn't {v}."),
            ("should", "advice", "He should {v}.", "He shouldn't {v}."),
            ("may", "permission", "May I {v}?", "You may not {v}."),
            ("have to", "necessity", "She has to {v}.", "She doesn't have to {v}."),
        ],
    },
    "comparisons": {
        "label": "Comparisons",
        "icon": "⚖️",
        "patterns": [
            ("Comparative (-er)", "adj + er + than", "A cat is small{_}er than a horse.", ""),
            ("Superlative (-est)", "the + adj + est", "The sun is the bigg{_}est star.", ""),
            ("More/Most", "more + adj / most + adj", "This is more {v} than that.", ""),
            ("As...as", "as + adj + as", "He is as tall as his brother.", ""),
        ],
    },
    "prepositions": {
        "label": "Prepositions",
        "icon": "📍",
        "patterns": [
            ("in", "location/time", "The book is in the bag.", "I wake up in the morning."),
            ("on", "surface/day", "The cup is on the table.", "We have class on Monday."),
            ("at", "point/time", "She is at school.", "The movie starts at 7."),
            ("to", "direction", "I go to school.", "She walked to the park."),
            ("from", "origin", "He is from Turkey.", "The letter is from my friend."),
            ("with", "accompaniment", "I play with my friends.", "She writes with a pencil."),
            ("for", "purpose/duration", "This gift is for you.", "I waited for two hours."),
            ("about", "topic", "The book is about animals.", "Tell me about your day."),
        ],
    },
}

# Word family suffixes
_WORD_FAMILIES = {
    "noun": ["-tion", "-ment", "-ness", "-er", "-or", "-ist", "-ity", "-ance"],
    "adjective": ["-ful", "-less", "-ous", "-ive", "-able", "-al", "-ic", "-ly"],
    "verb": ["-ise", "-ify", "-en", "-ate"],
    "adverb": ["-ly"],
}

# Common collocations
_COLLOCATIONS = [
    ("make", ["a mistake", "a decision", "friends", "progress", "an effort", "a plan"]),
    ("do", ["homework", "exercise", "research", "the dishes", "your best", "a favour"]),
    ("take", ["a photo", "a break", "notes", "a test", "a shower", "care of"]),
    ("have", ["lunch", "fun", "a meeting", "a good time", "a look", "a problem"]),
    ("get", ["ready", "up", "dressed", "lost", "better", "angry"]),
    ("go", ["shopping", "swimming", "home", "to bed", "online", "for a walk"]),
]


def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"gwl_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _extract_patterns(structure: str) -> list[str]:
    return [p.strip() for p in structure.replace("?", "?.").split(".")
            if p.strip() and len(p.strip()) > 5]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Structure Lab
# ══════════════════════════════════════════════════════════════════════════════

def _build_structure_lab(vocab: list, structure: str, grammar_topics: list,
                          grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)

    # Pick grammar categories relevant to this week
    all_cats = list(_GRAMMAR_CATEGORIES.keys())
    if grammar_topics:
        # Try to match grammar topics to categories
        selected_cats = []
        for gt in grammar_topics:
            gl = gt.lower()
            for ck in all_cats:
                if ck in gl or any(p[0].lower() in gl for p in _GRAMMAR_CATEGORIES[ck]["patterns"]):
                    if ck not in selected_cats:
                        selected_cats.append(ck)
        if not selected_cats:
            selected_cats = all_cats[:2]
    else:
        rng.shuffle(all_cats)
        selected_cats = all_cats[:2]

    rows = ""
    q_num = 0

    for cat_key in selected_cats[:2]:
        cat = _GRAMMAR_CATEGORIES[cat_key]
        patterns = cat["patterns"]
        rng.shuffle(patterns)

        # Category header
        rows += f'''
        <div class="cat-header">
            <span class="cat-icon">{cat["icon"]}</span>
            <span class="cat-label">{cat["label"]}</span>
        </div>'''

        # Structure table
        rows += '<div class="struct-table"><table>'
        rows += '<tr><th>Structure</th><th>Formula</th><th>Example (+)</th><th>Example (−)</th></tr>'
        for name, formula, pos, neg in patterns[:3]:
            v = vocab[q_num % len(vocab)] if vocab else "study"
            pos_ex = pos.replace("{v}", v).replace("{_}", "")
            neg_ex = neg.replace("{v}", v).replace("{_}", "") if neg else "—"
            rows += f'<tr><td><b>{name}</b></td><td><code>{formula}</code></td>'
            rows += f'<td class="ex-pos">{pos_ex}</td><td class="ex-neg">{neg_ex}</td></tr>'
        rows += '</table></div>'

        # Exercises
        for name, formula, pos, neg in patterns[:cfg["structure_count"] // 2]:
            q_num += 1
            v = vocab[q_num % len(vocab)] if vocab else "learn"
            answer = pos.replace("{v}", v).replace("{_}", "")

            rows += f'''
            <div class="exercise-row">
                <span class="q-num">{q_num}</span>
                <div class="q-body">
                    <div class="q-badge">{name}</div>
                    <div class="q-hint">Formula: <code>{formula}</code></div>
                    <div class="q-text">Complete using <b>{name}</b>: ({v})</div>
                    <input type="text" class="answer-input" data-answer="{answer}"
                           placeholder="Write the sentence..." onblur="checkAnswer(this)">
                </div>
            </div>'''

    # Negative/Question transformation
    rows += '''
    <div class="sub-section">
        <div class="sub-title">🔄 Transform the Sentences</div>'''

    patterns = _extract_patterns(structure)
    _transforms = [
        ("Make it negative", "negative"),
        ("Make it a question", "question"),
        ("Change the tense", "tense"),
    ]
    for i, pat in enumerate(patterns[:3]):
        q_num += 1
        t_type = _transforms[i % len(_transforms)]
        rows += f'''
        <div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-badge transform">{t_type[0]}</div>
                <div class="q-text">{pat}</div>
                <textarea class="transform-area" rows="2"
                          placeholder="Write your answer..."></textarea>
            </div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:{cfg["color_accent"]};">
        <div class="section-title" style="background:linear-gradient(135deg,{cfg["color_primary"]},{cfg["color_accent"]});">
            <span class="section-icon">🏗️</span> Structure Lab — Grammar Workshop</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Word Families & Collocations
# ══════════════════════════════════════════════════════════════════════════════

def _build_word_families(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 10)
    words = vocab[:cfg["family_count"]]

    rows = ""
    q_num = 0

    # Part A: Word family table
    rows += '<div class="sub-section"><div class="sub-title">🌳 A. Word Families</div>'
    rows += '<div class="hint-text">Complete the word family table. Write the missing forms.</div>'

    rows += '<div class="family-table"><table>'
    rows += '<tr><th>Base Word</th><th>Noun (-tion/-ment/-ness)</th><th>Adjective (-ful/-less/-ous)</th><th>Adverb (-ly)</th></tr>'
    for w in words[:6]:
        q_num += 1
        rows += f'''<tr>
            <td><b onclick="speak('{w}')" style="cursor:pointer;">{w} 🔊</b></td>
            <td><input type="text" class="table-input" placeholder="noun form..."></td>
            <td><input type="text" class="table-input" placeholder="adjective form..."></td>
            <td><input type="text" class="table-input" placeholder="adverb form..."></td>
        </tr>'''
    rows += '</table></div>'
    rows += '</div>'

    # Part B: Suffix sorting
    rows += '<div class="sub-section"><div class="sub-title">📦 B. Sort by Suffix</div>'
    rows += '<div class="hint-text">Which part of speech does each suffix create?</div>'

    _suffix_q = [
        ("-ful", "adjective"), ("-tion", "noun"), ("-ly", "adverb"),
        ("-ness", "noun"), ("-less", "adjective"), ("-ment", "noun"),
        ("-ous", "adjective"), ("-er", "noun"),
    ]
    rng.shuffle(_suffix_q)
    for suffix, pos in _suffix_q[:cfg["family_count"]]:
        q_num += 1
        options = ["noun", "adjective", "adverb", "verb"]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="pos-btn" onclick="checkPOS(this,\'{pos}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''
        <div class="suffix-row">
            <span class="q-num">{q_num}</span>
            <span class="suffix-tag">{suffix}</span>
            <div class="pos-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Collocations
    rows += '<div class="sub-section"><div class="sub-title">🤝 C. Collocations — Match the Pairs</div>'
    rows += '<div class="hint-text">Which verb goes with which phrase? Choose correctly!</div>'

    used_collocations = list(_COLLOCATIONS)
    rng.shuffle(used_collocations)
    for verb, phrases in used_collocations[:4]:
        q_num += 1
        correct = rng.choice(phrases)
        # Get distractors from other verbs
        other_phrases = []
        for ov, op in _COLLOCATIONS:
            if ov != verb:
                other_phrases.extend(op)
        rng.shuffle(other_phrases)
        options = [correct] + other_phrases[:2]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="coll-btn" onclick="checkColl(this,\'{correct}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''
        <div class="coll-row">
            <span class="q-num">{q_num}</span>
            <span class="coll-verb">{verb}</span>
            <span class="coll-plus">+</span>
            <div class="coll-options">{btns}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF9800;">
        <div class="section-title" style="background:linear-gradient(135deg,#e65100,#FF9800);">
            <span class="section-icon">🌳</span> Word Families & Collocations</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Theme Vocabulary Workshop
# ══════════════════════════════════════════════════════════════════════════════

def _build_theme_vocabulary(vocab: list, theme: str, theme_tr: str,
                             grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 20)
    words = vocab[:cfg["theme_count"]]

    rows = ""
    q_num = 0

    # Part A: Vocabulary cards with context
    rows += '<div class="sub-section"><div class="sub-title">📚 A. Key Words — Listen & Learn</div>'
    rows += f'<div class="hint-text">This week\'s theme: <b>{theme}</b> ({theme_tr})</div>'

    card_html = '<div class="vocab-grid">'
    for w in words:
        card_html += f'''
        <div class="vocab-card" onclick="speak('{w}')">
            <div class="vc-word">{w}</div>
            <div class="vc-speaker">🔊 tap to hear</div>
        </div>'''
    card_html += '</div>'
    rows += card_html
    rows += '</div>'

    # Part B: Fill in context sentences
    rows += '<div class="sub-section"><div class="sub-title">✏️ B. Use in Context</div>'
    rows += '<div class="hint-text">Complete each sentence with the correct word from the box.</div>'

    rows += '<div class="word-bank">'
    shuffled = list(words)
    rng.shuffle(shuffled)
    for w in shuffled:
        rows += f'<span class="word-chip">{w}</span>'
    rows += '</div>'

    _templates = [
        "We learned about {w} in class today.",
        "My favourite topic is {w}.",
        "The teacher explained {w} very clearly.",
        "Can you tell me about {w}?",
        "I want to understand {w} better.",
        "Everyone should know about {w}.",
        "She wrote a paragraph about {w}.",
        "They discussed {w} during the meeting.",
        "He is really good at {w}.",
        "The project was about {w}.",
        "We need to practise {w} more.",
        "The book explains {w} in detail.",
    ]
    rng.shuffle(_templates)

    for i, w in enumerate(words[:cfg["theme_count"] // 2 + 1]):
        q_num += 1
        tmpl = _templates[i % len(_templates)]
        blank = tmpl.replace("{w}", "______")
        rows += f'''
        <div class="ctx-row">
            <span class="q-num">{q_num}</span>
            <span class="ctx-sent">{blank}</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="..." onblur="checkAnswer(this)">
        </div>'''
    rows += '</div>'

    # Part C: Categorise the words
    rows += '<div class="sub-section"><div class="sub-title">📦 C. Categorise</div>'
    rows += '<div class="hint-text">Drag or type each word into the correct category.</div>'

    categories = ["Noun", "Verb", "Adjective"]
    for cat in categories:
        rows += f'''
        <div class="cat-box">
            <div class="cat-title">{cat}</div>
            <textarea class="cat-area" rows="2"
                      placeholder="Write {cat.lower()}s from the word list..."></textarea>
        </div>'''
    rows += '</div>'

    # Part D: Word map
    rows += '<div class="sub-section"><div class="sub-title">🗺️ D. Word Map</div>'
    rows += f'<div class="hint-text">Create a word map for: <b>{theme}</b></div>'

    center_word = theme.split()[0] if theme else "Topic"
    rows += f'''
    <div class="word-map">
        <div class="wm-center">{center_word}</div>
        <div class="wm-branches">
            <div class="wm-branch">
                <div class="wm-label">Related Words</div>
                <textarea class="wm-input" rows="2" placeholder="Write related words..."></textarea>
            </div>
            <div class="wm-branch">
                <div class="wm-label">Example Sentence</div>
                <textarea class="wm-input" rows="2" placeholder="Write a sentence..."></textarea>
            </div>
            <div class="wm-branch">
                <div class="wm-label">Synonyms</div>
                <textarea class="wm-input" rows="2" placeholder="Write synonyms..."></textarea>
            </div>
        </div>
    </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#4CAF50;">
        <div class="section-title" style="background:linear-gradient(135deg,#2e7d32,#4CAF50);">
            <span class="section-icon">📚</span> Theme Vocabulary Workshop</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Schema & Table Drills
# ══════════════════════════════════════════════════════════════════════════════

def _build_schema_drills(vocab: list, structure: str, grammar_topics: list,
                          grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 30)

    rows = ""
    q_num = 0

    # Part A: Tense comparison table
    rows += '<div class="sub-section"><div class="sub-title">📊 A. Tense Comparison Chart</div>'
    rows += '<div class="hint-text">Complete the table with the correct forms.</div>'

    verbs_for_table = vocab[:4] if vocab else ["play", "study", "read", "write"]
    rows += '<div class="drill-table"><table>'
    rows += '<tr><th>Verb</th><th>Present Simple</th><th>Past Simple</th>'
    rows += '<th>Present Continuous</th><th>Future (will)</th></tr>'
    for v in verbs_for_table:
        q_num += 1
        rows += f'''<tr>
            <td><b>{v}</b></td>
            <td><input type="text" class="table-input" placeholder="He ___s"></td>
            <td><input type="text" class="table-input" placeholder="He ___ed"></td>
            <td><input type="text" class="table-input" placeholder="He is ___ing"></td>
            <td><input type="text" class="table-input" placeholder="He will ___"></td>
        </tr>'''
    rows += '</table></div>'
    rows += '</div>'

    # Part B: Preposition map
    rows += '<div class="sub-section"><div class="sub-title">📍 B. Preposition Check</div>'
    rows += '<div class="hint-text">Choose the correct preposition for each sentence.</div>'

    _prep_sentences = [
        ("The cat is ___ the table.", "on", ["in", "at", "to"]),
        ("She goes ___ school every day.", "to", ["at", "on", "in"]),
        ("We have English ___ Monday.", "on", ["in", "at", "for"]),
        ("He lives ___ Istanbul.", "in", ["on", "at", "to"]),
        ("I wake up ___ 7 o'clock.", "at", ["in", "on", "for"]),
        ("The book is ___ my bag.", "in", ["on", "at", "to"]),
        ("She is good ___ maths.", "at", ["in", "on", "for"]),
        ("I got a gift ___ my friend.", "from", ["to", "at", "in"]),
        ("Tell me ___ your holiday.", "about", ["for", "with", "to"]),
        ("I play ___ my friends.", "with", ["for", "about", "from"]),
    ]
    rng.shuffle(_prep_sentences)

    for sent, correct, distractors in _prep_sentences[:cfg["table_count"]]:
        q_num += 1
        options = [correct] + distractors
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="prep-btn" onclick="checkPrep(this,\'{correct}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''
        <div class="prep-row">
            <span class="q-num">{q_num}</span>
            <span class="prep-sent">{sent}</span>
            <div class="prep-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Modal chart
    rows += '<div class="sub-section"><div class="sub-title">🔑 C. Modal Verbs Chart</div>'
    rows += '<div class="hint-text">Match each modal to its function and write an example.</div>'

    _modal_funcs = [
        ("can", "ability"), ("must", "obligation"), ("should", "advice"),
        ("may", "permission"), ("have to", "necessity"),
    ]
    rng.shuffle(_modal_funcs)

    rows += '<div class="drill-table"><table>'
    rows += '<tr><th>Modal</th><th>Function</th><th>Your Example</th></tr>'
    for modal, func in _modal_funcs[:4]:
        funcs_all = ["ability", "obligation", "advice", "permission", "necessity"]
        rng.shuffle(funcs_all)
        options = [func] + [f for f in funcs_all if f != func][:2]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="func-btn" onclick="checkFunc(this,\'{func}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''<tr>
            <td><b>{modal}</b></td>
            <td><div class="func-options">{btns}</div></td>
            <td><input type="text" class="table-input wide" placeholder="Write a sentence with '{modal}'..."></td>
        </tr>'''
    rows += '</table></div>'
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#9C27B0;">
        <div class="section-title" style="background:linear-gradient(135deg,#6a1b9a,#9C27B0);">
            <span class="section-icon">📊</span> Schema & Table Drills</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Topic Test
# ══════════════════════════════════════════════════════════════════════════════

def _build_topic_test(vocab: list, structure: str, grammar_topics: list,
                       theme: str, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 40)

    questions = ""
    q_num = 0
    total_pts = 0
    patterns = _extract_patterns(structure)

    # Section A: Grammar MCQ (30 pts)
    questions += '<div class="test-section"><div class="test-section-title">A. Grammar — Choose the correct answer (3 pts each)</div>'

    _grammar_mcqs = [
        ("She ___ to school every day.", "goes", ["go", "going", "went"]),
        ("They ___ playing football now.", "are", ["is", "was", "were"]),
        ("He ___ his homework yesterday.", "did", ["does", "do", "doing"]),
        ("We ___ visit our grandparents next week.", "will", ["are", "do", "did"]),
        ("I ___ swim when I was five.", "could", ["can", "will", "must"]),
        ("You ___ eat more vegetables.", "should", ["can", "will", "may"]),
        ("The book is ___ the shelf.", "on", ["in", "at", "to"]),
        ("She is ___ than her sister.", "taller", ["tall", "tallest", "more tall"]),
        ("This is the ___ movie I've ever seen.", "best", ["good", "better", "most good"]),
        ("He ___ already finished his work.", "has", ["have", "is", "was"]),
    ]
    rng.shuffle(_grammar_mcqs)

    for sent, correct, distractors in _grammar_mcqs[:6]:
        q_num += 1
        total_pts += 3
        options = [correct] + distractors
        rng.shuffle(options)
        letters = ["A", "B", "C", "D"]
        opts = " ".join(
            f'<button class="test-opt" onclick="checkMCQ(this,\'{correct}\',\'{o}\')">'
            f'{letters[j]}) {o}</button>'
            for j, o in enumerate(options)
        )
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{sent}</span>
            <div class="test-options">{opts}</div>
        </div>'''
    questions += '</div>'

    # Section B: Vocabulary Fill (20 pts)
    questions += '<div class="test-section"><div class="test-section-title">B. Vocabulary — Fill in the blanks (4 pts each)</div>'

    _vocab_templates = [
        "We discussed {w} in today's class.",
        "The article is about {w}.",
        "She is really interested in {w}.",
        "He wants to learn more about {w}.",
        "The project focuses on {w}.",
    ]
    used = set()
    for tmpl in _vocab_templates:
        for w in vocab:
            if w in used or q_num >= 11:
                continue
            q_num += 1
            total_pts += 4
            used.add(w)
            blank = tmpl.replace("{w}", "______")
            questions += f'''<div class="test-q">
                <span class="q-num">{q_num}</span>
                <span class="q-text">{blank}</span>
                <input type="text" class="answer-input" data-answer="{w}"
                       placeholder="({w[0]}...)" onblur="checkAnswer(this)">
            </div>'''
            break
    questions += '</div>'

    # Section C: Collocation Match (15 pts)
    questions += '<div class="test-section"><div class="test-section-title">C. Collocations — Match correctly (3 pts each)</div>'

    coll_list = list(_COLLOCATIONS)
    rng.shuffle(coll_list)
    for verb, phrases in coll_list[:5]:
        q_num += 1
        total_pts += 3
        correct = rng.choice(phrases)
        other_ph = []
        for ov, op in _COLLOCATIONS:
            if ov != verb:
                other_ph.extend(op)
        rng.shuffle(other_ph)
        options = [correct] + other_ph[:2]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="test-opt" onclick="checkMCQ(this,\'{correct}\',\'{o}\')">{o}</button>'
            for o in options
        )
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text"><b>{verb}</b> + ___</span>
            <div class="test-options">{btns}</div>
        </div>'''
    questions += '</div>'

    # Section D: Sentence transformation (20 pts)
    questions += '<div class="test-section"><div class="test-section-title">D. Transform the sentences (5 pts each)</div>'
    _t_instructions = [
        "Make it negative", "Make it a question",
        "Change to past tense", "Change to future tense",
    ]
    for i, pat in enumerate(patterns[:4]):
        q_num += 1
        total_pts += 5
        instr = _t_instructions[i % len(_t_instructions)]
        questions += f'''<div class="test-q" style="flex-direction:column;">
            <div style="display:flex;gap:10px;align-items:center;">
                <span class="q-num">{q_num}</span>
                <span class="q-text">{pat}</span>
            </div>
            <div class="q-hint" style="margin-left:38px;">→ {instr}</div>
            <textarea class="transform-area" rows="2" style="margin-left:38px;margin-top:6px;"
                      placeholder="Write your answer..."></textarea>
        </div>'''
    questions += '</div>'

    # Section E: Writing (15 pts)
    q_num += 1
    total_pts += 15
    questions += f'''<div class="test-section">
        <div class="test-section-title">E. Writing (15 pts)</div>
        <div class="test-q" style="flex-direction:column;">
            <div style="display:flex;gap:10px;align-items:center;">
                <span class="q-num">{q_num}</span>
                <span class="q-text">Write 6 sentences about "<b>{theme}</b>".
                Use at least 3 different tenses and 4 vocabulary words.</span>
            </div>
            <textarea class="writing-area" rows="8" style="margin-top:8px;"
                      placeholder="Write here..."></textarea>
            <div class="writing-tools">
                <span class="word-counter" id="wc_test">0 words</span>
            </div>
        </div>
    </div>'''

    return f'''
    <div class="section-box" style="border-color:#f44336;">
        <div class="section-title" style="background:linear-gradient(135deg,#c62828,#f44336);">
            <span class="section-icon">📋</span> Topic Test — Total: {total_pts} points</div>
        <div class="test-info">⏱ Time: 35 minutes | 📊 Passing: 60% | Grammar + Vocabulary + Writing</div>
        {questions}
        <div class="test-score-bar">
            <span>Your Score:</span>
            <span class="counter" id="testScore">0</span> / {total_pts}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _gwl_styles(cfg: dict) -> str:
    cp = cfg["color_primary"]
    ca = cfg["color_accent"]
    cb = cfg["color_bg"]
    fs = cfg["font_size"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Segoe UI','Inter',sans-serif;
           font-size:{fs}; background:{cb}; color:#94A3B8; }}
    .page {{ max-width:860px; margin:0 auto; padding:16px; }}

    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:14px; padding:20px 24px; margin-bottom:14px;
        text-align:center; position:relative;
        box-shadow:0 4px 16px {cp}44; }}
    .book-header h1 {{ font-size:22px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:13px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.22); padding:4px 14px; border-radius:20px;
        font-size:12px; font-weight:700; }}

    .score-bar {{ background:#fff; border:2px solid {ca}; border-radius:12px;
        padding:10px 16px; margin-bottom:14px; display:flex;
        justify-content:space-between; align-items:center; }}
    .counter {{ font-weight:800; color:{cp}; font-size:16px; }}

    .section-box {{ background:#fff; border:2px solid #e2e8f0; border-radius:14px;
        margin-bottom:16px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.06); }}
    .section-title {{ color:#fff; padding:12px 18px; font-weight:700;
        font-size:15px; display:flex; align-items:center; gap:8px; }}
    .section-icon {{ font-size:18px; }}

    .sub-section {{ padding:14px 18px; border-bottom:1px solid #1A2035; }}
    .sub-section:last-child {{ border-bottom:none; }}
    .sub-title {{ font-weight:700; color:{cp}; font-size:14px; margin-bottom:10px;
        padding-bottom:6px; border-bottom:2px solid {ca}33; }}
    .hint-text {{ font-size:12px; color:#64748b; margin-bottom:10px; font-style:italic; }}

    .q-num {{ background:{cp}; color:#fff; min-width:26px; height:26px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:12px; flex-shrink:0; }}
    .q-text {{ flex:1; line-height:1.6; }}
    .q-hint {{ font-size:12px; color:#64748b; font-style:italic; margin-top:2px; }}

    /* Category header */
    .cat-header {{ padding:10px 18px; background:linear-gradient(135deg,{cp}10,{ca}08);
        border-bottom:2px solid {ca}33; display:flex; align-items:center; gap:8px; }}
    .cat-icon {{ font-size:20px; }}
    .cat-label {{ font-weight:800; color:{cp}; font-size:15px; }}

    /* Tables */
    .struct-table, .drill-table, .family-table {{ padding:10px 18px; overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; }}
    th {{ background:{cp}; color:#fff; padding:8px 10px; text-align:left; font-size:12px; }}
    td {{ padding:8px 10px; border-bottom:1px solid #e2e8f0; }}
    tr:nth-child(even) td {{ background:#111827; }}
    .ex-pos {{ color:#2e7d32; font-style:italic; }}
    .ex-neg {{ color:#c62828; font-style:italic; }}
    code {{ background:#1A2035; padding:2px 6px; border-radius:4px; font-size:12px; }}
    .table-input {{ width:100%; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; padding:4px; color:{cp};
        font-weight:600; outline:none; }}
    .table-input:focus {{ border-bottom-color:{cp}; background:#111827; }}
    .table-input.wide {{ min-width:200px; }}

    /* Exercises */
    .exercise-row {{ padding:12px 18px; border-bottom:1px solid #1A2035;
        display:flex; gap:10px; align-items:flex-start; }}
    .q-body {{ flex:1; }}
    .q-badge {{ display:inline-block; font-size:11px; font-weight:700;
        padding:2px 8px; border-radius:6px; margin-bottom:4px;
        background:#dbeafe; color:#1e40af; }}
    .q-badge.transform {{ background:#ede9fe; color:#5b21b6; }}

    .answer-input {{ width:100%; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; padding:6px 4px;
        color:{cp}; font-weight:600; outline:none; margin-top:6px; }}
    .answer-input:focus {{ border-bottom-color:{cp}; background:#111827; }}
    .answer-input.correct {{ border-bottom-color:#4CAF50; color:#4CAF50; background:#e8f5e9; }}
    .answer-input.wrong {{ border-bottom-color:#f44336; color:#f44336; background:#ffebee; }}

    .transform-area {{ width:100%; border:2px solid #e2e8f0; border-radius:8px;
        padding:8px 12px; font-size:inherit; font-family:inherit; resize:vertical;
        outline:none; margin-top:6px; }}
    .transform-area:focus {{ border-color:{ca}; }}

    /* Suffix / POS */
    .suffix-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .suffix-tag {{ font-weight:800; color:#e65100; font-size:16px;
        background:#fff3e0; padding:4px 12px; border-radius:8px; min-width:60px;
        text-align:center; }}
    .pos-options {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .pos-btn, .func-btn {{ padding:5px 12px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:12px; cursor:pointer; background:#fff; transition:.2s; }}
    .pos-btn:hover, .func-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .pos-btn.correct, .func-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .pos-btn.wrong, .func-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .pos-btn.disabled, .func-btn.disabled {{ pointer-events:none; opacity:.5; }}
    .func-options {{ display:flex; gap:4px; flex-wrap:wrap; }}

    /* Collocations */
    .coll-row {{ display:flex; align-items:center; gap:8px; padding:8px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .coll-verb {{ font-weight:800; color:{cp}; font-size:16px; min-width:60px; }}
    .coll-plus {{ font-weight:900; color:#94a3b8; }}
    .coll-options {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .coll-btn {{ padding:6px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .coll-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .coll-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .coll-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .coll-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Vocab */
    .vocab-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr));
        gap:8px; }}
    .vocab-card {{ padding:14px 10px; border:2px solid #e2e8f0; border-radius:12px;
        text-align:center; cursor:pointer; background:#fff; transition:.3s; }}
    .vocab-card:hover {{ border-color:{ca}; transform:translateY(-2px);
        box-shadow:0 4px 12px rgba(0,0,0,.1); }}
    .vc-word {{ font-weight:800; color:{cp}; font-size:15px; }}
    .vc-speaker {{ font-size:11px; color:#94a3b8; margin-top:4px; }}

    .word-bank {{ padding:10px 18px; background:#111827; display:flex;
        flex-wrap:wrap; gap:6px; border-bottom:2px solid #e2e8f0; }}
    .word-chip {{ background:#dbeafe; color:#1e40af; padding:4px 12px;
        border-radius:20px; font-weight:700; font-size:12px; }}

    .ctx-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; }}
    .ctx-sent {{ flex:1; line-height:1.6; }}

    .cat-box {{ display:inline-block; width:30%; min-width:200px;
        border:2px solid #e2e8f0; border-radius:10px; margin:4px;
        overflow:hidden; vertical-align:top; }}
    .cat-title {{ padding:8px 12px; background:{cp}; color:#fff;
        font-weight:700; font-size:13px; text-align:center; }}
    .cat-area {{ width:100%; border:none; padding:8px; font-size:inherit;
        font-family:inherit; resize:vertical; outline:none; min-height:50px; }}

    /* Word Map */
    .word-map {{ text-align:center; padding:10px 0; }}
    .wm-center {{ display:inline-block; padding:14px 28px; background:{cp};
        color:#fff; border-radius:50%; font-weight:900; font-size:18px;
        margin-bottom:14px; box-shadow:0 4px 12px {cp}44; }}
    .wm-branches {{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }}
    .wm-branch {{ flex:1; min-width:180px; border:2px solid #e2e8f0;
        border-radius:10px; overflow:hidden; }}
    .wm-label {{ padding:6px 10px; background:{ca}22; color:{cp};
        font-weight:700; font-size:12px; text-align:center; }}
    .wm-input {{ width:100%; border:none; padding:8px; font-size:inherit;
        font-family:inherit; resize:vertical; outline:none; }}

    /* Prep */
    .prep-row {{ display:flex; align-items:center; gap:8px; padding:8px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .prep-sent {{ flex:1; font-weight:600; }}
    .prep-options {{ display:flex; gap:6px; }}
    .prep-btn {{ padding:5px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:700; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .prep-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .prep-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .prep-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .prep-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Test */
    .test-info {{ padding:10px 18px; background:#ffebee; font-size:13px;
        color:#c62828; font-weight:600; border-bottom:1px solid #ffcdd2; }}
    .test-section {{ padding:10px 0; }}
    .test-section-title {{ padding:8px 18px; font-weight:700; font-size:14px;
        color:{cp}; background:#111827; border-bottom:1px solid #e2e8f0; }}
    .test-q {{ padding:10px 18px; border-bottom:1px solid #1A2035;
        display:flex; align-items:flex-start; gap:10px; flex-wrap:wrap; }}
    .test-options {{ display:flex; flex-wrap:wrap; gap:6px; width:100%; padding-left:36px; }}
    .test-opt {{ padding:5px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .test-opt:hover {{ border-color:{ca}; }}
    .test-opt.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .test-opt.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .test-opt.disabled {{ pointer-events:none; opacity:.5; }}

    .writing-area {{ width:100%; border:2px solid #e2e8f0; border-radius:10px;
        padding:12px; font-size:inherit; font-family:inherit; resize:vertical;
        outline:none; min-height:80px; }}
    .writing-area:focus {{ border-color:{ca}; }}
    .writing-tools {{ display:flex; justify-content:space-between; align-items:center;
        padding:4px 0; }}
    .word-counter {{ font-size:12px; color:#94a3b8; }}

    .test-score-bar {{ padding:14px 18px; background:#111827; text-align:center;
        font-weight:700; font-size:16px; color:{cp}; border-top:2px solid #e2e8f0; }}

    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.1)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-4px)}} 75%{{transform:translateX(4px)}} }}
    .shake {{ animation:shake .3s ease; }}
    </style>'''


def _gwl_scripts() -> str:
    return '''<script>
    var totalScore = 0, totalQ = 0;

    function updateScore(correct) {
        totalQ++;
        if (correct) totalScore++;
        var pct = totalQ > 0 ? Math.round(totalScore / totalQ * 100) : 0;
        var el = document.getElementById('scoreCounter');
        if (el) el.textContent = totalScore + ' / ' + totalQ + ' (' + pct + '%)';
    }

    function speak(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US'; u.rate = 0.85;
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

    function checkMCQ(el, answer, chosen) {
        var parent = el.closest('.test-q') || el.closest('.mcq-row');
        var opts = parent.querySelectorAll('.test-opt,.mcq-opt');
        opts.forEach(o => o.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            opts.forEach(o => { if (o.textContent.includes(answer)) o.classList.add('correct'); });
            updateScore(false);
        }
    }

    function checkPOS(el, answer, chosen) {
        var parent = el.closest('.suffix-row');
        var btns = parent.querySelectorAll('.pos-btn');
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

    function checkColl(el, answer, chosen) {
        var parent = el.closest('.coll-row');
        var btns = parent.querySelectorAll('.coll-btn');
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

    function checkPrep(el, answer, chosen) {
        var parent = el.closest('.prep-row');
        var btns = parent.querySelectorAll('.prep-btn');
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

    function checkFunc(el, answer, chosen) {
        var parent = el.closest('td');
        var btns = parent.querySelectorAll('.func-btn');
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

    /* Word counter */
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.writing-area').forEach(function(ta) {
            ta.addEventListener('input', function() {
                var words = ta.value.trim().split(/\\s+/).filter(w => w.length > 0).length;
                var counter = document.getElementById('wc_test');
                if (counter) counter.textContent = words + ' words';
            });
        });
    });
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# VOCAB HEADER
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocab_header(vocab: list) -> str:
    html = '<div class="section-box" style="border-color:#6366f1;">'
    html += '<div class="section-title" style="background:linear-gradient(135deg,#4f46e5,#6366f1);">'
    html += '<span class="section-icon">📚</span> Key Vocabulary — Click to Listen</div>'
    html += '<div style="display:flex;flex-wrap:wrap;gap:8px;padding:12px 16px;">'
    for v in vocab:
        html += (f'<span class="word-chip" style="cursor:pointer;" '
                f'onclick="speak(\'{v}\')">{v} 🔊</span>')
    html += '</div></div>'
    return html


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_TITLES = [
    "🏗️ Structure Lab",
    "🌳 Word Families & Collocations",
    "📚 Theme Vocabulary",
    "📊 Schema & Table Drills",
    "📋 Topic Test",
]


def build_grammar_words_pages(grade: int, week_num: int,
                               curriculum_weeks: list) -> list[str]:
    """Build Grammar & Words Lab pages for a given grade/week.

    Returns:
        List of 5 HTML strings — one page per exercise type.
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[5])
    vocab = week_data.get("vocab", [])[:cfg["vocab_count"]]
    structure = week_data.get("structure", "")
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    if not vocab:
        return []

    linked = week_data.get("linked_content", {})
    grammar_topics = linked.get("grammar", [])

    unit_num = max(1, (week_num - 1) // 4 + 1)

    styles = _gwl_styles(cfg)
    scripts = _gwl_scripts()
    vocab_header = _build_vocab_header(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>🧪 Grammar & Words Lab — Unit {unit_num}</h1>
            <div class="subtitle">{theme} — {theme_tr} | Week {week_num} | Page {page_num}/5</div>
            <div style="font-size:11px;opacity:.7;margin-top:2px;">{_PAGE_TITLES[page_num - 1]}</div>
        </div>
        <div class="score-bar">
            <div><b>🎯 Score:</b> <span class="counter" id="scoreCounter">0 / 0</span></div>
        </div>'''

    def _wrap(page_num: int, body: str) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{styles}{scripts}</head>
<body>
<div class="page">
    {_header(page_num)}
    {vocab_header}
    {body}
</div>
</body></html>'''

    page1 = _wrap(1, _build_structure_lab(vocab, structure, grammar_topics, grade, cfg, seed))
    page2 = _wrap(2, _build_word_families(vocab, grade, cfg, seed))
    page3 = _wrap(3, _build_theme_vocabulary(vocab, theme, theme_tr, grade, cfg, seed))
    page4 = _wrap(4, _build_schema_drills(vocab, structure, grammar_topics, grade, cfg, seed))
    page5 = _wrap(5, _build_topic_test(vocab, structure, grammar_topics, theme, grade, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_grammar_words(grade: int, curriculum_weeks: list,
                              selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Grammar & Words Lab for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_grammar_words_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
