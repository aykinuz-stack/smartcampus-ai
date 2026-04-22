# -*- coding: utf-8 -*-
"""Grammar & Academic Words — Lise (9-12) Grammar + Academic Vocabulary Destek Kitabı.

Interactive HTML exercise pages for high school advanced grammar & academic vocabulary.
Exercise types (5 pages per week):
  1. Advanced Structure Lab (Passive, Conditionals, Relative Clauses, Reported Speech)
  2. Linking & Formal Language (Linking words, Formal register, Academic style)
  3. Academic Vocabulary & Phrasal Verbs (Academic word list, Phrasal verbs in context)
  4. Vocabulary in Context (Contextual usage, Collocations, Word formation)
  5. Mixed Topic Test (Grammar + Academic vocab + Writing)

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
    9: {"label": "9th Grade • B1.1", "font_size": "14px", "vocab_count": 16,
        "structure_count": 10, "linking_count": 8, "academic_count": 10,
        "context_count": 8, "test_count": 18,
        "color_primary": "#1a237e", "color_accent": "#5c6bc0", "color_bg": "#e8eaf6"},
    10: {"label": "10th Grade • B1.2", "font_size": "14px", "vocab_count": 18,
         "structure_count": 12, "linking_count": 10, "academic_count": 12,
         "context_count": 10, "test_count": 20,
         "color_primary": "#4a148c", "color_accent": "#9c27b0", "color_bg": "#f3e5f5"},
    11: {"label": "11th Grade • B2.1", "font_size": "13px", "vocab_count": 20,
         "structure_count": 14, "linking_count": 10, "academic_count": 14,
         "context_count": 12, "test_count": 22,
         "color_primary": "#004d40", "color_accent": "#00897b", "color_bg": "#e0f2f1"},
    12: {"label": "12th Grade • B2.2", "font_size": "13px", "vocab_count": 22,
         "structure_count": 14, "linking_count": 12, "academic_count": 16,
         "context_count": 12, "test_count": 25,
         "color_primary": "#b71c1c", "color_accent": "#e53935", "color_bg": "#ffebee"},
}

# ── Advanced Grammar Structures ──
_ADVANCED_GRAMMAR = {
    "passive": {
        "label": "Passive Voice", "icon": "🔄",
        "rules": [
            ("Present Simple Passive", "S + is/are + V3", "The book is read by many."),
            ("Past Simple Passive", "S + was/were + V3", "The letter was written yesterday."),
            ("Present Perfect Passive", "S + has/have been + V3", "The project has been completed."),
            ("Modal Passive", "S + modal + be + V3", "The task can be finished today."),
        ],
    },
    "conditionals": {
        "label": "Conditionals", "icon": "🔀",
        "rules": [
            ("Zero Conditional", "If + present, present", "If you heat ice, it melts."),
            ("First Conditional", "If + present, will + V1", "If it rains, I will stay home."),
            ("Second Conditional", "If + past, would + V1", "If I had money, I would travel."),
            ("Third Conditional", "If + past perfect, would have + V3", "If I had studied, I would have passed."),
        ],
    },
    "relative_clauses": {
        "label": "Relative Clauses", "icon": "🔗",
        "rules": [
            ("who", "for people (subject)", "The man who called is my uncle."),
            ("which", "for things", "The book which I read was great."),
            ("that", "people/things (defining)", "The car that he bought is red."),
            ("where", "for places", "The city where I was born is small."),
            ("whose", "for possession", "The girl whose bag was lost cried."),
        ],
    },
    "reported_speech": {
        "label": "Reported Speech", "icon": "💬",
        "rules": [
            ("Statement", "said (that) + backshift", '"I am tired" → He said he was tired.'),
            ("Question", "asked if/wh- + backshift", '"Are you ok?" → She asked if I was ok.'),
            ("Command", "told + to-infinitive", '"Sit down" → He told me to sit down.'),
            ("Request", "asked + to-infinitive", '"Please help" → She asked me to help.'),
        ],
    },
}

# ── Linking Words ──
_LINKING_WORDS = {
    "addition": {"label": "Addition", "words": ["moreover", "furthermore", "in addition", "besides", "also", "what is more"]},
    "contrast": {"label": "Contrast", "words": ["however", "nevertheless", "on the other hand", "although", "despite", "yet"]},
    "cause": {"label": "Cause & Effect", "words": ["therefore", "consequently", "as a result", "thus", "hence", "because of"]},
    "example": {"label": "Example", "words": ["for instance", "for example", "such as", "namely", "in particular", "specifically"]},
    "conclusion": {"label": "Conclusion", "words": ["in conclusion", "to sum up", "overall", "in summary", "all in all", "to conclude"]},
    "sequence": {"label": "Sequence", "words": ["firstly", "secondly", "then", "next", "finally", "subsequently"]},
}

# ── Academic Word List (AWL subset) ──
_ACADEMIC_WORDS = [
    ("analyse", "to examine in detail"), ("approach", "a method or way"),
    ("assume", "to suppose without proof"), ("concept", "an idea or principle"),
    ("consist", "to be made up of"), ("context", "circumstances or setting"),
    ("contribute", "to give or add to"), ("create", "to bring into existence"),
    ("define", "to state the meaning of"), ("demonstrate", "to show clearly"),
    ("distribute", "to share or spread"), ("environment", "surroundings"),
    ("establish", "to set up or found"), ("estimate", "to roughly calculate"),
    ("evaluate", "to assess or judge"), ("evidence", "proof or support"),
    ("factor", "an element or cause"), ("identify", "to recognise"),
    ("indicate", "to show or suggest"), ("interpret", "to explain the meaning"),
    ("involve", "to include or engage"), ("maintain", "to keep or sustain"),
    ("method", "a way of doing something"), ("occur", "to happen"),
    ("participate", "to take part in"), ("perceive", "to become aware of"),
    ("principle", "a fundamental rule"), ("process", "a series of steps"),
    ("require", "to need"), ("research", "systematic investigation"),
    ("respond", "to answer or react"), ("significant", "important or notable"),
    ("similar", "alike or resembling"), ("specific", "clearly defined"),
    ("strategy", "a plan of action"), ("structure", "arrangement or organisation"),
    ("theory", "a system of ideas"), ("vary", "to differ or change"),
]

# ── Phrasal Verbs ──
_PHRASAL_VERBS = [
    ("carry out", "to perform or conduct", "We carried out an experiment."),
    ("come up with", "to think of or produce", "She came up with a great idea."),
    ("figure out", "to understand or solve", "I figured out the answer."),
    ("look into", "to investigate", "The police looked into the case."),
    ("point out", "to indicate or mention", "He pointed out the mistake."),
    ("set up", "to establish or arrange", "They set up a new company."),
    ("turn out", "to prove to be", "It turned out to be false."),
    ("bring about", "to cause to happen", "The reform brought about changes."),
    ("break down", "to analyse into parts", "Let's break down the problem."),
    ("make up", "to constitute or invent", "Women make up 50% of the class."),
    ("put forward", "to propose or suggest", "She put forward a new theory."),
    ("rule out", "to exclude or eliminate", "We can't rule out that option."),
    ("take on", "to accept or undertake", "He took on extra responsibilities."),
    ("work out", "to solve or calculate", "Can you work out the total?"),
    ("draw up", "to prepare or draft", "They drew up a contract."),
    ("cut down", "to reduce", "We need to cut down on waste."),
]


def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"gaw_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _extract_patterns(structure: str) -> list[str]:
    return [p.strip() for p in structure.replace("?", "?.").split(".")
            if p.strip() and len(p.strip()) > 5]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Advanced Structure Lab
# ══════════════════════════════════════════════════════════════════════════════

def _build_structure_lab(vocab: list, structure: str, grammar_topics: list,
                          grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)
    all_cats = list(_ADVANCED_GRAMMAR.keys())

    # Select 2 grammar categories
    selected = []
    if grammar_topics:
        for gt in grammar_topics:
            gl = gt.lower()
            for ck in all_cats:
                if ck.replace("_", " ") in gl or _ADVANCED_GRAMMAR[ck]["label"].lower() in gl:
                    if ck not in selected:
                        selected.append(ck)
    if len(selected) < 2:
        remaining = [c for c in all_cats if c not in selected]
        rng.shuffle(remaining)
        selected.extend(remaining[:2 - len(selected)])

    rows = ""
    q_num = 0

    for cat_key in selected[:2]:
        cat = _ADVANCED_GRAMMAR[cat_key]
        rules = cat["rules"]

        # Category header + rule table
        rows += f'''
        <div class="cat-header">
            <span class="cat-icon">{cat["icon"]}</span>
            <span class="cat-label">{cat["label"]}</span>
        </div>
        <div class="rule-table"><table>
            <tr><th>Type</th><th>Formula</th><th>Example</th></tr>'''
        for name, formula, example in rules:
            rows += f'<tr><td><b>{name}</b></td><td><code>{formula}</code></td><td class="ex-pos">{example}</td></tr>'
        rows += '</table></div>'

        # Exercises: choose correct form
        for name, formula, example in rules[:cfg["structure_count"] // 4]:
            q_num += 1
            v = vocab[q_num % len(vocab)] if vocab else "study"

            if cat_key == "passive":
                q_text = f'Rewrite in <b>{name}</b>: "They {v} the report."'
            elif cat_key == "conditionals":
                q_text = f'Complete using <b>{name}</b>: "If I {v}..."'
            elif cat_key == "relative_clauses":
                pronoun = name
                q_text = f'Combine using <b>{pronoun}</b>: "The person ___. The person {v}s here."'
            else:
                q_text = f'Change to <b>{name}</b>: "I {v} every day."'

            rows += f'''
            <div class="exercise-row">
                <span class="q-num">{q_num}</span>
                <div class="q-body">
                    <div class="q-badge">{name}</div>
                    <div class="q-text">{q_text}</div>
                    <textarea class="transform-area" rows="2"
                              placeholder="Write your answer..."></textarea>
                </div>
            </div>'''

    # MCQ section
    rows += '<div class="sub-section"><div class="sub-title">✅ Choose the Correct Answer</div>'

    _structure_mcqs = [
        ("The report ___ by the students yesterday.", "was written", ["is written", "has written", "wrote"]),
        ("If I ___ more time, I would study abroad.", "had", ["have", "will have", "having"]),
        ("The city ___ I was born is very small.", "where", ["which", "who", "whose"]),
        ("She said that she ___ tired.", "was", ["is", "will be", "has been"]),
        ("The project ___ completed by next week.", "will be", ["is", "was", "has"]),
        ("If she had studied harder, she ___ passed.", "would have", ["will have", "has", "would"]),
        ("The man ___ car was stolen called the police.", "whose", ["who", "which", "that"]),
        ("He told me ___ the door.", "to close", ["close", "closing", "closed"]),
        ("The results ___ already been published.", "have", ["has", "is", "was"]),
        ("___ the weather was bad, we went out.", "Although", ["Because", "Therefore", "Moreover"]),
    ]
    rng.shuffle(_structure_mcqs)

    for sent, correct, distractors in _structure_mcqs[:4]:
        q_num += 1
        options = [correct] + distractors
        rng.shuffle(options)
        letters = ["A", "B", "C", "D"]
        opts = " ".join(
            f'<button class="mcq-opt" onclick="checkMCQ(this,\'{correct}\',\'{o}\')">'
            f'{letters[j]}) {o}</button>'
            for j, o in enumerate(options)
        )
        rows += f'''<div class="mcq-row">
            <div class="q-line"><span class="q-num">{q_num}</span>
                <span class="q-text">{sent}</span></div>
            <div class="mcq-options">{opts}</div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:{cfg["color_accent"]};">
        <div class="section-title" style="background:linear-gradient(135deg,{cfg["color_primary"]},{cfg["color_accent"]});">
            <span class="section-icon">🏗️</span> Advanced Structure Lab</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Linking & Formal Language
# ══════════════════════════════════════════════════════════════════════════════

def _build_linking_formal(vocab: list, theme: str, grade: int,
                           cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 10)

    rows = ""
    q_num = 0

    # Part A: Linking words reference + fill-in
    rows += '<div class="sub-section"><div class="sub-title">🔗 A. Linking Words — Learn & Use</div>'

    # Reference cards
    cards = ""
    cat_keys = list(_LINKING_WORDS.keys())
    rng.shuffle(cat_keys)
    for ck in cat_keys[:4]:
        cat = _LINKING_WORDS[ck]
        words_html = ", ".join(f'<span class="link-word">{w}</span>' for w in cat["words"][:4])
        cards += f'''
        <div class="link-card">
            <div class="link-cat">{cat["label"]}</div>
            <div class="link-words">{words_html}</div>
        </div>'''
    rows += f'<div class="link-grid">{cards}</div>'

    # Fill-in exercises
    _link_sentences = [
        ("She studied hard; ___, she passed the exam.", "therefore", "contrast"),
        ("The project was successful. ___, there were some issues.", "However", "addition"),
        ("There are many benefits. ___, it improves health.", "For instance", "cause"),
        ("He is smart. ___, he is very kind.", "Moreover", "example"),
        ("___, I would like to thank everyone.", "In conclusion", "sequence"),
        ("The plan failed ___ the lack of funding.", "because of", "conclusion"),
        ("___ the problems, they completed the task.", "Despite", "contrast"),
        ("The results were ___; ___, further research is needed.", "inconclusive; therefore", "cause"),
    ]
    rng.shuffle(_link_sentences)

    for sent, answer, category in _link_sentences[:cfg["linking_count"] // 2]:
        q_num += 1
        rows += f'''
        <div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-badge">{category}</div>
                <div class="q-text">{sent}</div>
                <input type="text" class="answer-input" data-answer="{answer}"
                       placeholder="Type the linking word..." onblur="checkAnswer(this)">
            </div>
        </div>'''
    rows += '</div>'

    # Part B: Formal vs Informal
    rows += '<div class="sub-section"><div class="sub-title">🎩 B. Formal vs Informal Register</div>'
    rows += '<div class="hint-text">Choose the more formal alternative for academic writing.</div>'

    _formal_pairs = [
        ("I think", "In my opinion", "formal"),
        ("lots of", "a significant number of", "formal"),
        ("get", "obtain", "formal"),
        ("help", "assist", "formal"),
        ("show", "demonstrate", "formal"),
        ("but", "however", "formal"),
        ("so", "therefore", "formal"),
        ("kind of", "somewhat", "formal"),
        ("find out", "discover", "formal"),
        ("talk about", "discuss", "formal"),
    ]
    rng.shuffle(_formal_pairs)

    for informal, formal, _ in _formal_pairs[:cfg["linking_count"] // 2]:
        q_num += 1
        options = [formal, informal]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="formal-btn" onclick="checkFormal(this,\'{formal}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''
        <div class="formal-row">
            <span class="q-num">{q_num}</span>
            <span class="formal-prompt">More formal?</span>
            <div class="formal-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Paragraph with linking words
    rows += '<div class="sub-section"><div class="sub-title">✍️ C. Write a Connected Paragraph</div>'
    rows += f'''<div class="hint-text">Write a short paragraph (5-6 sentences) about <b>{theme}</b>.
    Use at least 4 different linking words from the categories above.</div>
    <textarea class="writing-area" rows="8" placeholder="Start writing here..."></textarea>
    <div class="writing-tools">
        <span class="word-counter" id="wc_link">0 words</span>
    </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#FF9800;">
        <div class="section-title" style="background:linear-gradient(135deg,#e65100,#FF9800);">
            <span class="section-icon">🔗</span> Linking & Formal Language</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Academic Vocabulary & Phrasal Verbs
# ══════════════════════════════════════════════════════════════════════════════

def _build_academic_vocab(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 20)

    rows = ""
    q_num = 0

    # Select academic words for this week
    aw_start = ((seed % 30) * 2) % len(_ACADEMIC_WORDS)
    week_aw = []
    for i in range(cfg["academic_count"]):
        week_aw.append(_ACADEMIC_WORDS[(aw_start + i) % len(_ACADEMIC_WORDS)])

    # Part A: Academic word cards
    rows += '<div class="sub-section"><div class="sub-title">🎓 A. Academic Word List</div>'
    rows += '<div class="hint-text">Learn these academic words. Click to hear pronunciation.</div>'

    card_html = '<div class="aw-grid">'
    for word, definition in week_aw[:8]:
        card_html += f'''
        <div class="aw-card" onclick="speak('{word}')">
            <div class="aw-word">{word} 🔊</div>
            <div class="aw-def">{definition}</div>
        </div>'''
    card_html += '</div>'
    rows += card_html
    rows += '</div>'

    # Part B: Match word to definition
    rows += '<div class="sub-section"><div class="sub-title">📝 B. Match Word to Definition</div>'

    match_words = week_aw[:6]
    rng.shuffle(match_words)
    defs_shuffled = [(d, w) for w, d in match_words]
    rng.shuffle(defs_shuffled)

    for i, (defn, word) in enumerate(defs_shuffled):
        q_num += 1
        others = [w for w, _ in week_aw if w != word]
        rng.shuffle(others)
        options = [word] + others[:2]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="mcq-opt" onclick="checkMCQ(this,\'{word}\',\'{o}\')">{o}</button>'
            for o in options
        )
        rows += f'''<div class="mcq-row">
            <div class="q-line"><span class="q-num">{q_num}</span>
                <span class="q-text">"{defn}"</span></div>
            <div class="mcq-options">{btns}</div>
        </div>'''
    rows += '</div>'

    # Part C: Phrasal verbs
    rows += '<div class="sub-section"><div class="sub-title">🚀 C. Phrasal Verbs in Context</div>'

    pv_list = list(_PHRASAL_VERBS)
    rng.shuffle(pv_list)
    selected_pv = pv_list[:cfg["academic_count"] // 2]

    # Reference cards
    pv_cards = '<div class="pv-grid">'
    for pv, meaning, example in selected_pv[:4]:
        pv_cards += f'''
        <div class="pv-card">
            <div class="pv-verb">{pv}</div>
            <div class="pv-meaning">{meaning}</div>
            <div class="pv-example">{example}</div>
        </div>'''
    pv_cards += '</div>'
    rows += pv_cards

    # Fill-in exercises
    for pv, meaning, example in selected_pv[:4]:
        q_num += 1
        blank_sent = example.replace(pv.split()[0], "______").replace(
            pv.split()[1] if len(pv.split()) > 1 else "", "______", 1)
        # Simplified: just use the phrasal verb as answer
        rows += f'''
        <div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-hint">{meaning}</div>
                <div class="q-text">{blank_sent}</div>
                <input type="text" class="answer-input" data-answer="{pv}"
                       placeholder="Type the phrasal verb..." onblur="checkAnswer(this)">
            </div>
        </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#4CAF50;">
        <div class="section-title" style="background:linear-gradient(135deg,#1b5e20,#4CAF50);">
            <span class="section-icon">🎓</span> Academic Vocabulary & Phrasal Verbs</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Vocabulary in Context
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocab_in_context(vocab: list, structure: str, theme: str,
                             theme_tr: str, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 30)
    words = vocab[:cfg["context_count"]]

    rows = ""
    q_num = 0

    # Part A: Contextual fill-in
    rows += '<div class="sub-section"><div class="sub-title">📖 A. Vocabulary in Context</div>'
    rows += '<div class="hint-text">Complete each sentence with the most appropriate word.</div>'

    rows += '<div class="word-bank">'
    shuffled = list(words)
    rng.shuffle(shuffled)
    for w in shuffled:
        rows += f'<span class="word-chip">{w}</span>'
    rows += '</div>'

    _ctx_templates = [
        "The study aims to {w} the relationship between the variables.",
        "It is important to {w} the data before drawing conclusions.",
        "The article provides {w} evidence for the theory.",
        "Researchers need to {w} their findings carefully.",
        "The government decided to {w} a new policy.",
        "Students should {w} actively in classroom discussions.",
        "The experiment was designed to {w} the hypothesis.",
        "The results {w} that further research is needed.",
        "We need to {w} the potential risks involved.",
        "The report {w}s several key recommendations.",
        "The teacher asked students to {w} the text critically.",
        "The data {w}s a clear pattern of improvement.",
    ]
    rng.shuffle(_ctx_templates)

    for i, w in enumerate(words):
        q_num += 1
        tmpl = _ctx_templates[i % len(_ctx_templates)]
        blank = tmpl.replace("{w}", "______")
        rows += f'''
        <div class="ctx-row">
            <span class="q-num">{q_num}</span>
            <span class="ctx-sent">{blank}</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="({w[0]}...)" onblur="checkAnswer(this)">
        </div>'''
    rows += '</div>'

    # Part B: Word formation
    rows += '<div class="sub-section"><div class="sub-title">🔬 B. Word Formation</div>'
    rows += '<div class="hint-text">Write the correct form of the word in brackets.</div>'

    _formation_q = [
        ("The {w} of the project took six months.", "noun"),
        ("This is a very {w} approach.", "adjective"),
        ("He spoke {w} about the topic.", "adverb"),
        ("They need to {w} the situation.", "verb"),
    ]

    for i, w in enumerate(words[:4]):
        q_num += 1
        tmpl, pos = _formation_q[i % len(_formation_q)]
        sent = tmpl.replace("{w}", f"______ ({w})")
        rows += f'''
        <div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-badge">{pos}</div>
                <div class="q-text">{sent}</div>
                <input type="text" class="answer-input"
                       placeholder="Write the {pos} form...">
            </div>
        </div>'''
    rows += '</div>'

    # Part C: Collocations
    rows += '<div class="sub-section"><div class="sub-title">🤝 C. Academic Collocations</div>'
    rows += '<div class="hint-text">Match the verbs with their academic collocations.</div>'

    _acad_coll = [
        ("conduct", "research", ["homework", "a walk", "a nap"]),
        ("draw", "a conclusion", ["a picture", "a bath", "a card"]),
        ("raise", "awareness", ["a flag", "money", "a child"]),
        ("address", "an issue", ["a letter", "a crowd", "a problem"]),
        ("reach", "an agreement", ["a shelf", "a goal", "a peak"]),
        ("pose", "a question", ["for a photo", "a threat", "a problem"]),
    ]
    rng.shuffle(_acad_coll)

    for verb, correct, distractors in _acad_coll[:4]:
        q_num += 1
        options = [correct] + distractors[:2]
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
    <div class="section-box" style="border-color:#7c3aed;">
        <div class="section-title" style="background:linear-gradient(135deg,#4a148c,#7c3aed);">
            <span class="section-icon">📖</span> Vocabulary in Context</div>
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Mixed Topic Test
# ══════════════════════════════════════════════════════════════════════════════

def _build_topic_test(vocab: list, structure: str, grammar_topics: list,
                       theme: str, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 40)

    questions = ""
    q_num = 0
    total_pts = 0

    # Section A: Grammar MCQ (30 pts)
    questions += '<div class="test-section"><div class="test-section-title">A. Grammar — Choose the correct answer (3 pts each)</div>'

    _test_mcqs = [
        ("The bridge ___ in 1990.", "was built", ["built", "is built", "has built"]),
        ("If I ___ you, I would accept the offer.", "were", ["am", "was", "will be"]),
        ("She asked me ___ I had finished.", "whether", ["that", "what", "which"]),
        ("The scientist ___ discovered the cure won the prize.", "who", ["which", "whose", "whom"]),
        ("___ the rain, the match continued.", "Despite", ["Although", "Because", "Therefore"]),
        ("He suggested that we ___ the plan.", "change", ["changed", "changes", "changing"]),
        ("The results have ___ announced.", "been", ["being", "be", "was"]),
        ("If she had called, I ___ answered.", "would have", ["will have", "had", "would"]),
        ("___, the evidence supports the theory.", "Moreover", ["But", "So", "Or"]),
        ("The house ___ roof was damaged is being repaired.", "whose", ["which", "that", "who"]),
    ]
    rng.shuffle(_test_mcqs)

    for sent, correct, distractors in _test_mcqs[:6]:
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

    # Section B: Academic Vocabulary (20 pts)
    questions += '<div class="test-section"><div class="test-section-title">B. Academic Vocabulary (4 pts each)</div>'

    aw_start = ((seed % 30) * 2) % len(_ACADEMIC_WORDS)
    test_aw = [_ACADEMIC_WORDS[(aw_start + i) % len(_ACADEMIC_WORDS)] for i in range(8)]
    rng.shuffle(test_aw)

    for word, defn in test_aw[:5]:
        q_num += 1
        total_pts += 4
        others = [w for w, _ in _ACADEMIC_WORDS if w != word]
        rng.shuffle(others)
        options = [word] + others[:2]
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="test-opt" onclick="checkMCQ(this,\'{word}\',\'{o}\')">{o}</button>'
            for o in options
        )
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">"{defn}"</span>
            <div class="test-options">{btns}</div>
        </div>'''
    questions += '</div>'

    # Section C: Linking Words (15 pts)
    questions += '<div class="test-section"><div class="test-section-title">C. Linking Words (3 pts each)</div>'

    _link_test = [
        ("She was tired; ___, she continued working.", "however", ["moreover", "because", "although"]),
        ("___, the experiment was a success.", "Overall", ["But", "So", "Or"]),
        ("He failed the exam ___ he didn't study.", "because", ["although", "despite", "moreover"]),
        ("There are many advantages. ___, it saves time.", "For instance", ["However", "Therefore", "Although"]),
        ("___, I want to emphasise the importance of education.", "Finally", ["But", "So", "Or"]),
    ]
    rng.shuffle(_link_test)

    for sent, correct, distractors in _link_test[:5]:
        q_num += 1
        total_pts += 3
        options = [correct] + distractors
        rng.shuffle(options)
        btns = " ".join(
            f'<button class="test-opt" onclick="checkMCQ(this,\'{correct}\',\'{o}\')">{o}</button>'
            for o in options
        )
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{sent}</span>
            <div class="test-options">{btns}</div>
        </div>'''
    questions += '</div>'

    # Section D: Transformation (20 pts)
    questions += '<div class="test-section"><div class="test-section-title">D. Transform the sentences (5 pts each)</div>'
    patterns = _extract_patterns(structure)
    _t_instructions = [
        "Rewrite in passive voice",
        "Change to reported speech",
        "Combine using a relative clause",
        "Rewrite using a conditional",
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

    # Section E: Academic Writing (15 pts)
    q_num += 1
    total_pts += 15
    questions += f'''<div class="test-section">
        <div class="test-section-title">E. Academic Writing (15 pts)</div>
        <div class="test-q" style="flex-direction:column;">
            <div style="display:flex;gap:10px;align-items:center;">
                <span class="q-num">{q_num}</span>
                <span class="q-text">Write an academic paragraph (8-10 sentences) about
                "<b>{theme}</b>". Use formal language, linking words, and at least
                3 academic vocabulary items. Include a topic sentence and a conclusion.</span>
            </div>
            <textarea class="writing-area" rows="10" style="margin-top:8px;"
                      placeholder="Write your academic paragraph here..."></textarea>
            <div class="writing-tools">
                <span class="word-counter" id="wc_test">0 words</span>
            </div>
        </div>
    </div>'''

    return f'''
    <div class="section-box" style="border-color:#f44336;">
        <div class="section-title" style="background:linear-gradient(135deg,#c62828,#f44336);">
            <span class="section-icon">📋</span> Mixed Topic Test — Total: {total_pts} points</div>
        <div class="test-info">⏱ Time: 45 minutes | 📊 Passing: 60% |
            Grammar • Academic Vocab • Linking • Writing</div>
        {questions}
        <div class="test-score-bar">
            <span>Your Score:</span>
            <span class="counter" id="testScore">0</span> / {total_pts}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _gaw_styles(cfg: dict) -> str:
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
    .q-line {{ display:flex; align-items:center; gap:10px; width:100%; }}
    .q-hint {{ font-size:12px; color:#64748b; font-style:italic; margin-top:2px; }}

    .cat-header {{ padding:10px 18px; background:linear-gradient(135deg,{cp}10,{ca}08);
        border-bottom:2px solid {ca}33; display:flex; align-items:center; gap:8px; }}
    .cat-icon {{ font-size:20px; }}
    .cat-label {{ font-weight:800; color:{cp}; font-size:15px; }}

    .rule-table {{ padding:10px 18px; overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; }}
    th {{ background:{cp}; color:#fff; padding:8px 10px; text-align:left; font-size:12px; }}
    td {{ padding:8px 10px; border-bottom:1px solid #e2e8f0; }}
    tr:nth-child(even) td {{ background:#111827; }}
    .ex-pos {{ color:#2e7d32; font-style:italic; }}
    code {{ background:#1A2035; padding:2px 6px; border-radius:4px; font-size:12px; }}

    .exercise-row {{ padding:12px 18px; border-bottom:1px solid #1A2035;
        display:flex; gap:10px; align-items:flex-start; }}
    .q-body {{ flex:1; }}
    .q-badge {{ display:inline-block; font-size:11px; font-weight:700;
        padding:2px 8px; border-radius:6px; margin-bottom:4px;
        background:#dbeafe; color:#1e40af; }}

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

    .mcq-row {{ padding:10px 18px; border-bottom:1px solid #1A2035; }}
    .mcq-options {{ display:flex; flex-wrap:wrap; gap:6px; padding:6px 0 0 36px; }}
    .mcq-opt {{ padding:6px 16px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .mcq-opt:hover {{ border-color:{ca}; background:{cb}; }}
    .mcq-opt.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .mcq-opt.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .mcq-opt.disabled {{ pointer-events:none; opacity:.5; }}

    /* Linking */
    .link-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
        gap:8px; margin-bottom:14px; }}
    .link-card {{ padding:10px 14px; border:2px solid #e2e8f0; border-radius:10px;
        background:#fff; }}
    .link-cat {{ font-weight:800; color:{cp}; font-size:13px; margin-bottom:6px; }}
    .link-words {{ display:flex; flex-wrap:wrap; gap:4px; }}
    .link-word {{ font-size:12px; padding:2px 8px; background:{ca}15; color:{cp};
        border-radius:6px; font-weight:600; }}

    .formal-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .formal-prompt {{ font-weight:600; color:#64748b; font-size:13px; min-width:100px; }}
    .formal-options {{ display:flex; gap:6px; }}
    .formal-btn {{ padding:6px 16px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .formal-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .formal-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .formal-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .formal-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Academic Vocab */
    .aw-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
        gap:8px; }}
    .aw-card {{ padding:12px 14px; border:2px solid #e2e8f0; border-radius:12px;
        cursor:pointer; background:#fff; transition:.3s; }}
    .aw-card:hover {{ border-color:{ca}; transform:translateY(-2px);
        box-shadow:0 4px 12px rgba(0,0,0,.1); }}
    .aw-word {{ font-weight:800; color:{cp}; font-size:15px; margin-bottom:4px; }}
    .aw-def {{ font-size:12px; color:#64748b; font-style:italic; }}

    .pv-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
        gap:8px; margin-bottom:14px; }}
    .pv-card {{ padding:10px 14px; border:2px solid #e2e8f0; border-radius:10px;
        background:#111827; }}
    .pv-verb {{ font-weight:800; color:{cp}; font-size:14px; }}
    .pv-meaning {{ font-size:12px; color:#64748b; margin:2px 0; }}
    .pv-example {{ font-size:12px; color:#94A3B8; font-style:italic; }}

    /* Context */
    .word-bank {{ padding:10px 18px; background:#111827; display:flex;
        flex-wrap:wrap; gap:6px; border-bottom:2px solid #e2e8f0; }}
    .word-chip {{ background:#dbeafe; color:#1e40af; padding:4px 12px;
        border-radius:20px; font-weight:700; font-size:12px; }}

    .ctx-row {{ display:flex; align-items:center; gap:10px; padding:8px 0;
        border-bottom:1px solid #1A2035; }}
    .ctx-sent {{ flex:1; line-height:1.6; }}

    .coll-row {{ display:flex; align-items:center; gap:8px; padding:8px 0;
        border-bottom:1px solid #1A2035; flex-wrap:wrap; }}
    .coll-verb {{ font-weight:800; color:{cp}; font-size:16px; min-width:80px; }}
    .coll-plus {{ font-weight:900; color:#94a3b8; }}
    .coll-options {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .coll-btn {{ padding:6px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .coll-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .coll-btn.correct {{ background:#4CAF50; color:#fff; border-color:#4CAF50; }}
    .coll-btn.wrong {{ background:#f44336; color:#fff; border-color:#f44336; }}
    .coll-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* Writing */
    .writing-area {{ width:100%; border:2px solid #e2e8f0; border-radius:10px;
        padding:12px; font-size:inherit; font-family:inherit; resize:vertical;
        outline:none; min-height:80px; }}
    .writing-area:focus {{ border-color:{ca}; }}
    .writing-tools {{ display:flex; justify-content:space-between; align-items:center;
        padding:4px 0; }}
    .word-counter {{ font-size:12px; color:#94a3b8; }}

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

    .test-score-bar {{ padding:14px 18px; background:#111827; text-align:center;
        font-weight:700; font-size:16px; color:{cp}; border-top:2px solid #e2e8f0; }}

    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.1)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-4px)}} 75%{{transform:translateX(4px)}} }}
    .shake {{ animation:shake .3s ease; }}
    </style>'''


def _gaw_scripts() -> str:
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
        var parent = el.closest('.mcq-row') || el.closest('.test-q');
        var opts = parent.querySelectorAll('.mcq-opt,.test-opt');
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

    function checkFormal(el, answer, chosen) {
        var parent = el.closest('.formal-row');
        var btns = parent.querySelectorAll('.formal-btn');
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

    /* Word counter */
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.writing-area').forEach(function(ta) {
            ta.addEventListener('input', function() {
                var words = ta.value.trim().split(/\\s+/).filter(w => w.length > 0).length;
                var counters = [document.getElementById('wc_test'), document.getElementById('wc_link')];
                counters.forEach(c => { if (c) c.textContent = words + ' words'; });
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
    "🏗️ Advanced Structure Lab",
    "🔗 Linking & Formal Language",
    "🎓 Academic Vocab & Phrasal Verbs",
    "📖 Vocabulary in Context",
    "📋 Mixed Topic Test",
]


def build_grammar_academic_pages(grade: int, week_num: int,
                                  curriculum_weeks: list) -> list[str]:
    """Build Grammar & Academic Words pages for a given grade/week."""
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[9])
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

    styles = _gaw_styles(cfg)
    scripts = _gaw_scripts()
    vocab_header = _build_vocab_header(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>🎓 Grammar & Academic Words — Unit {unit_num}</h1>
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
    page2 = _wrap(2, _build_linking_formal(vocab, theme, grade, cfg, seed))
    page3 = _wrap(3, _build_academic_vocab(vocab, grade, cfg, seed))
    page4 = _wrap(4, _build_vocab_in_context(vocab, structure, theme, theme_tr, grade, cfg, seed))
    page5 = _wrap(5, _build_topic_test(vocab, structure, grammar_topics, theme, grade, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_grammar_academic(grade: int, curriculum_weeks: list,
                                 selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Grammar & Academic Words book for all weeks."""
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_grammar_academic_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
