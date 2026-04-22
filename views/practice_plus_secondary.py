# -*- coding: utf-8 -*-
"""Practice Plus — Ortaokul (5-8) Alıştırma / Pekiştirme Kitabı.

Interactive HTML exercise pages for middle school English learners.
Exercise types (5 pages per week):
  1. Grammar Practice (Dilbilgisi uygulamaları)
  2. Vocabulary Review (Kelime tekrarları)
  3. Multiple Choice & Paragraph Completion (Çoktan seçmeli + paragraf tamamlama)
  4. Mini Writing Tasks (Kısa yazma görevleri)
  5. Unit Test (Ünite testi)

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
        "grammar_count": 8, "mcq_count": 8, "writing_count": 3, "test_count": 10,
        "color_primary": "#1e40af", "color_accent": "#3b82f6", "color_bg": "#eff6ff"},
    6: {"label": "6th Grade", "font_size": "14px", "vocab_count": 14,
        "grammar_count": 10, "mcq_count": 10, "writing_count": 4, "test_count": 12,
        "color_primary": "#059669", "color_accent": "#34d399", "color_bg": "#ecfdf5"},
    7: {"label": "7th Grade", "font_size": "14px", "vocab_count": 14,
        "grammar_count": 10, "mcq_count": 10, "writing_count": 4, "test_count": 12,
        "color_primary": "#7c3aed", "color_accent": "#a78bfa", "color_bg": "#f5f3ff"},
    8: {"label": "8th Grade", "font_size": "13px", "vocab_count": 16,
        "grammar_count": 12, "mcq_count": 12, "writing_count": 5, "test_count": 15,
        "color_primary": "#b45309", "color_accent": "#f59e0b", "color_bg": "#fffbeb"},
}


def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"pp_{grade}_{week}".encode()).hexdigest()[:8], 16)


# ══════════════════════════════════════════════════════════════════════════════
# SENTENCE / GRAMMAR GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def _make_grammar_items(structure: str, vocab: list, grammar_topics: list,
                        count: int, seed: int) -> list[dict]:
    """Generate grammar exercise items from structure patterns."""
    rng = random.Random(seed)
    items = []

    # Parse structure into patterns
    patterns = [p.strip() for p in structure.replace("?", "?.").split(".")
                if p.strip() and len(p.strip()) > 5]

    # Type 1: Fill the gap with correct form
    for v in vocab[:count]:
        for pat in patterns[:2]:
            if "..." in pat:
                sent = pat.replace("...", f" ______ ({v})")
                items.append({
                    "type": "fill",
                    "question": sent.strip(),
                    "answer": v,
                    "hint": grammar_topics[0] if grammar_topics else "",
                })
            elif v.lower() not in pat.lower():
                items.append({
                    "type": "fill",
                    "question": f"{pat} ______ ({v}).",
                    "answer": v,
                    "hint": grammar_topics[0] if grammar_topics else "",
                })

    # Type 2: Sentence reordering
    for pat in patterns[:3]:
        words = pat.split()
        if len(words) >= 4:
            shuffled = list(words)
            rng.shuffle(shuffled)
            items.append({
                "type": "reorder",
                "question": " / ".join(shuffled),
                "answer": pat,
                "hint": "Put the words in the correct order",
            })

    # Type 3: Error correction
    for pat in patterns[:2]:
        words = pat.split()
        if len(words) >= 3:
            idx = rng.randint(0, len(words) - 1)
            wrong_words = list(words)
            # Simple error: swap two adjacent words
            if idx < len(words) - 1:
                wrong_words[idx], wrong_words[idx + 1] = wrong_words[idx + 1], wrong_words[idx]
            items.append({
                "type": "error",
                "question": " ".join(wrong_words),
                "answer": pat,
                "hint": "Find and fix the error",
            })

    rng.shuffle(items)
    return items[:count]


def _make_sentences(vocab: list, structure: str, count: int, seed: int) -> list[dict]:
    """Generate sentences for MCQ / paragraph exercises."""
    rng = random.Random(seed)
    sentences = []
    patterns = [p.strip() for p in structure.replace("?", "?.").split(".")
                if p.strip() and len(p.strip()) > 3]

    for v in vocab:
        for pat in patterns[:3]:
            if "..." in pat:
                sent = pat.replace("...", f" {v}")
                sentences.append({"sentence": sent.strip(), "word": v, "original": pat})
            elif v.lower() not in pat.lower():
                sentences.append({"sentence": f"{pat} {v}.", "word": v, "original": pat})

    _fallback = [
        "I like {w}.", "She has {w}.", "We need {w}.", "They want {w}.",
        "He can {w}.", "Do you have {w}?", "There is a {w} here.",
        "I usually {w} after school.", "We often {w} on weekends.",
        "Can you {w}?", "I would like to {w}.", "He doesn't {w}.",
    ]
    for v in vocab:
        pat = _fallback[hash(v) % len(_fallback)]
        sentences.append({"sentence": pat.format(w=v), "word": v, "original": pat})

    rng.shuffle(sentences)
    return sentences[:count * 2]


# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE GENERATORS (return HTML fragments)
# ══════════════════════════════════════════════════════════════════════════════

def _build_grammar_practice(vocab: list, structure: str, grammar_topics: list,
                            grade: int, cfg: dict, seed: int) -> str:
    """Page 1: Grammar exercises — fill gaps, reorder, error correction."""
    items = _make_grammar_items(structure, vocab, grammar_topics, cfg["grammar_count"], seed)

    # Grammar topic header
    topics_html = ""
    if grammar_topics:
        topics_html = '<div class="grammar-topics">' + " • ".join(
            f'<span class="topic-tag">{t}</span>' for t in grammar_topics[:3]
        ) + '</div>'

    rows = ""
    for i, item in enumerate(items):
        if item["type"] == "fill":
            rows += f'''<div class="exercise-row">
                <span class="q-num">{i+1}</span>
                <div class="q-body">
                    <div class="q-badge">Fill in</div>
                    <div class="q-text">{item["question"]}</div>
                    <input type="text" class="answer-input" data-answer="{item["answer"]}"
                           placeholder="Type your answer..." onblur="checkAnswer(this)">
                </div>
            </div>'''
        elif item["type"] == "reorder":
            rows += f'''<div class="exercise-row">
                <span class="q-num">{i+1}</span>
                <div class="q-body">
                    <div class="q-badge reorder">Reorder</div>
                    <div class="q-text">{item["question"]}</div>
                    <input type="text" class="answer-input" data-answer="{item["answer"]}"
                           placeholder="Write the correct sentence..." onblur="checkAnswer(this)">
                </div>
            </div>'''
        elif item["type"] == "error":
            rows += f'''<div class="exercise-row">
                <span class="q-num">{i+1}</span>
                <div class="q-body">
                    <div class="q-badge error">Fix it</div>
                    <div class="q-text" style="text-decoration:underline wavy #dc2626;">{item["question"]}</div>
                    <input type="text" class="answer-input" data-answer="{item["answer"]}"
                           placeholder="Write the corrected sentence..." onblur="checkAnswer(this)">
                </div>
            </div>'''

    return f'''
    <div class="section-box" style="border-color:#3b82f6;">
        <div class="section-title" style="background:linear-gradient(135deg,#1e40af,#3b82f6);">
            <span class="section-icon">📝</span> Grammar Practice</div>
        {topics_html}
        {rows}
    </div>'''


def _build_vocabulary_review(vocab: list, grade: int, cfg: dict, seed: int) -> str:
    """Page 2: Vocabulary review — definitions, synonyms, usage."""
    rng = random.Random(seed + 10)
    words = vocab[:cfg["vocab_count"]]

    # Part A: Match word to definition/usage
    match_items = ""
    shuffled = list(words)
    rng.shuffle(shuffled)
    for i, w in enumerate(words):
        match_items += f'''<div class="vocab-match-row">
            <span class="q-num">{i+1}</span>
            <span class="vocab-word" onclick="speak('{w}')">{w} 🔊</span>
            <input type="text" class="answer-input short" data-answer="{w}"
                   placeholder="Use in a sentence..." onblur="checkAnswer(this)">
        </div>'''

    # Part B: Word scramble
    scramble_items = ""
    for i, w in enumerate(words[:6]):
        chars = list(w)
        rng.shuffle(chars)
        scrambled = "".join(chars)
        scramble_items += f'''<div class="vocab-match-row">
            <span class="q-num">{i+1}</span>
            <span class="scrambled">{scrambled}</span>
            <input type="text" class="answer-input short" data-answer="{w}"
                   placeholder="Unscramble..." onblur="checkAnswer(this)">
        </div>'''

    # Part C: Odd one out
    odd_items = ""
    for i in range(0, min(len(words) - 3, 4)):
        group = words[i:i+3]
        # Add one random word from later in the list
        odd_word = words[-(i+1)] if len(words) > i + 4 else "banana"
        options = group + [odd_word]
        rng.shuffle(options)
        odd_items += f'''<div class="odd-row">
            <span class="q-num">{i+1}</span>
            <div class="odd-options">
                {"".join(f'<button class="odd-btn" onclick="checkOdd(this,\'{odd_word}\',\'{o}\')">{o}</button>' for o in options)}
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#059669;">
        <div class="section-title" style="background:linear-gradient(135deg,#059669,#34d399);">
            <span class="section-icon">📚</span> Vocabulary Review</div>

        <div class="sub-section">
            <div class="sub-title">A. Use each word in a sentence</div>
            {match_items}
        </div>

        <div class="sub-section">
            <div class="sub-title">B. Unscramble the words</div>
            {scramble_items}
        </div>

        <div class="sub-section">
            <div class="sub-title">C. Odd One Out — Find the word that doesn't belong</div>
            {odd_items}
        </div>
    </div>'''


def _build_mcq_paragraph(vocab: list, structure: str, grade: int, cfg: dict, seed: int) -> str:
    """Page 3: Multiple choice + paragraph completion."""
    rng = random.Random(seed + 20)
    sentences = _make_sentences(vocab, structure, cfg["mcq_count"], seed + 20)

    # Part A: MCQ
    mcq_html = ""
    used = set()
    q_num = 0
    for s in sentences:
        if s["word"] in used or q_num >= cfg["mcq_count"]:
            continue
        used.add(s["word"])
        q_num += 1
        blank = s["sentence"].replace(s["word"], "______")
        others = [v for v in vocab if v != s["word"]]
        rng.shuffle(others)
        distractors = others[:3]
        options = [s["word"]] + distractors
        rng.shuffle(options)
        opts_html = " ".join(
            f'<button class="mcq-opt" onclick="checkMCQ(this,\'{s["word"]}\',\'{o}\')">{o}</button>'
            for o in options
        )
        mcq_html += f'''<div class="mcq-row">
            <div class="q-line"><span class="q-num">{q_num}</span>
                <span class="q-text">{blank}</span></div>
            <div class="mcq-options">{opts_html}</div>
        </div>'''

    # Part B: Paragraph completion (cloze)
    para_words = vocab[:5]
    rng2 = random.Random(seed + 25)
    para_sentences = []
    for w in para_words:
        tmpl = rng2.choice([
            f"I really enjoy {w}.",
            f"We always {w} at school.",
            f"My friend likes {w} very much.",
            f"Yesterday, we talked about {w}.",
            f"The teacher showed us {w}.",
        ])
        para_sentences.append((tmpl, w))

    rng2.shuffle(para_sentences)
    para_html = ""
    bank_words = [w for _, w in para_sentences]
    rng2.shuffle(bank_words)

    para_html += '<div class="word-bank">' + " ".join(
        f'<span class="word-chip">{w}</span>' for w in bank_words
    ) + '</div>'
    para_html += '<div class="paragraph-box">'
    for i, (sent, word) in enumerate(para_sentences):
        blank_sent = sent.replace(word,
            f'<input type="text" class="blank-input" data-answer="{word}" '
            f'placeholder="..." onblur="checkAnswer(this)">')
        para_html += f'<span class="para-sent">{i+1}. {blank_sent} </span>'
    para_html += '</div>'

    return f'''
    <div class="section-box" style="border-color:#7c3aed;">
        <div class="section-title" style="background:linear-gradient(135deg,#7c3aed,#a78bfa);">
            <span class="section-icon">✅</span> Multiple Choice & Paragraph Completion</div>

        <div class="sub-section">
            <div class="sub-title">A. Choose the correct answer</div>
            {mcq_html}
        </div>

        <div class="sub-section">
            <div class="sub-title">B. Complete the paragraph with the words from the box</div>
            {para_html}
        </div>
    </div>'''


def _build_writing_tasks(vocab: list, structure: str, theme: str, theme_tr: str,
                         writings: list, grade: int, cfg: dict, seed: int) -> str:
    """Page 4: Mini writing tasks."""
    rng = random.Random(seed + 30)

    tasks = []
    # Task 1: Guided sentence writing
    tasks.append({
        "title": "Write 5 sentences about: " + theme,
        "instruction": f"Use these words: {', '.join(vocab[:5])}",
        "type": "sentences",
        "min_lines": 5,
    })

    # Task 2: Short paragraph
    tasks.append({
        "title": f"Write a short paragraph about '{theme}'",
        "instruction": f"Use the structure: {structure[:80]}..." if len(structure) > 80 else f"Use the structure: {structure}",
        "type": "paragraph",
        "min_lines": 4,
    })

    # Task 3: From curriculum writing topics
    if writings:
        w_topic = writings[0] if isinstance(writings, list) else str(writings)
        tasks.append({
            "title": f"Writing Task: {w_topic}",
            "instruction": "Write at least 6 sentences. Use correct grammar and punctuation.",
            "type": "extended",
            "min_lines": 6,
        })

    # Task 4: Creative prompt
    prompts = [
        f"Imagine you are a {vocab[0] if vocab else 'student'}. Write about your day.",
        f"Write a short dialogue between two friends about {theme}.",
        f"Describe your favourite {theme.lower()} in 5-6 sentences.",
        f"Write an email to your friend about {theme}.",
    ]
    tasks.append({
        "title": rng.choice(prompts),
        "instruction": "Be creative! Use at least 5 different vocabulary words from this unit.",
        "type": "creative",
        "min_lines": 5,
    })

    tasks = tasks[:cfg["writing_count"]]

    tasks_html = ""
    for i, task in enumerate(tasks):
        type_badge = {"sentences": "📝 Sentences", "paragraph": "📄 Paragraph",
                      "extended": "📖 Extended", "creative": "✨ Creative"}.get(task["type"], "📝")
        textarea_rows = task["min_lines"] + 2
        tasks_html += f'''<div class="writing-task">
            <div class="writing-header">
                <span class="q-num">{i+1}</span>
                <span class="writing-badge">{type_badge}</span>
                <span class="writing-title">{task["title"]}</span>
            </div>
            <div class="writing-instruction">{task["instruction"]}</div>
            <textarea class="writing-area" rows="{textarea_rows}"
                      placeholder="Start writing here..."></textarea>
            <div class="writing-tools">
                <span class="word-counter" id="wc_{i}">0 words</span>
                <button class="hint-btn" onclick="speak('{task['title']}')" title="Listen">🔊</button>
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#f59e0b;">
        <div class="section-title" style="background:linear-gradient(135deg,#b45309,#f59e0b);">
            <span class="section-icon">✍️</span> Mini Writing Tasks</div>
        {tasks_html}
    </div>'''


def _build_unit_test(vocab: list, structure: str, grammar_topics: list,
                     grade: int, cfg: dict, seed: int) -> str:
    """Page 5: Unit test — mixed question types."""
    rng = random.Random(seed + 40)
    sentences = _make_sentences(vocab, structure, cfg["test_count"], seed + 40)

    questions = ""
    q_num = 0

    # Section A: MCQ (40%)
    questions += '<div class="test-section"><div class="test-section-title">A. Choose the correct answer (4 points each)</div>'
    used = set()
    for s in sentences:
        if s["word"] in used or q_num >= 5:
            continue
        used.add(s["word"])
        q_num += 1
        blank = s["sentence"].replace(s["word"], "______")
        others = [v for v in vocab if v != s["word"]]
        rng.shuffle(others)
        options = [s["word"]] + others[:3]
        rng.shuffle(options)
        letters = ["A", "B", "C", "D"]
        opts = " ".join(
            f'<button class="test-opt" onclick="checkMCQ(this,\'{s["word"]}\',\'{o}\')">'
            f'{letters[j]}) {o}</button>'
            for j, o in enumerate(options)
        )
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{blank}</span>
            <div class="test-options">{opts}</div>
        </div>'''
    questions += '</div>'

    # Section B: True/False (20%)
    questions += '<div class="test-section"><div class="test-section-title">B. True or False (4 points each)</div>'
    tf_items = []
    for s in sentences[5:]:
        if s["word"] in used or len(tf_items) >= 3:
            continue
        used.add(s["word"])
        is_true = rng.random() > 0.45
        if is_true:
            tf_items.append({"text": s["sentence"], "answer": "true"})
        else:
            others = [v for v in vocab if v != s["word"]]
            if others:
                wrong = rng.choice(others)
                tf_items.append({"text": s["sentence"].replace(s["word"], wrong), "answer": "false"})

    for item in tf_items:
        q_num += 1
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{item["text"]}</span>
            <div class="tf-buttons">
                <button class="tf-btn" onclick="checkTF(this,'{item["answer"]}','true')">✓ True</button>
                <button class="tf-btn" onclick="checkTF(this,'{item["answer"]}','false')">✗ False</button>
            </div>
        </div>'''
    questions += '</div>'

    # Section C: Fill in the blanks (20%)
    questions += '<div class="test-section"><div class="test-section-title">C. Fill in the blanks (4 points each)</div>'
    fill_words = [v for v in vocab if v not in used][:3]
    for w in fill_words:
        q_num += 1
        tmpl = rng.choice([
            f"We ______ every day at school.",
            f"My teacher said we should ______.",
            f"I always ______ after lunch.",
        ])
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{tmpl}</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="({w[0]}...)" onblur="checkAnswer(this)">
        </div>'''
    questions += '</div>'

    # Section D: Writing (20%)
    q_num += 1
    questions += f'''<div class="test-section">
        <div class="test-section-title">D. Writing (20 points)</div>
        <div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">Write 5-6 sentences about "<b>{vocab[0] if vocab else "your day"}</b>".
            Use at least 4 vocabulary words from this unit.</span>
            <textarea class="writing-area" rows="6" placeholder="Write here..."></textarea>
        </div>
    </div>'''

    return f'''
    <div class="section-box" style="border-color:#dc2626;">
        <div class="section-title" style="background:linear-gradient(135deg,#991b1b,#dc2626);">
            <span class="section-icon">📋</span> Unit Test — Total: 100 points</div>
        <div class="test-info">⏱ Time: 30 minutes | 📊 Passing score: 60%</div>
        {questions}
        <div class="test-score-bar">
            <span>Your Score:</span>
            <span class="counter" id="testScore">0</span> / 100
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _pp_styles(cfg: dict) -> str:
    cp = cfg["color_primary"]
    ca = cfg["color_accent"]
    cb = cfg["color_bg"]
    fs = cfg["font_size"]
    return f'''<style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Segoe UI','Inter',sans-serif;
           font-size:{fs}; background:{cb}; color:#94A3B8; }}
    .page {{ max-width:840px; margin:0 auto; padding:16px; }}

    .book-header {{ background:linear-gradient(135deg,{cp},{ca});
        color:#fff; border-radius:14px; padding:18px 24px; margin-bottom:14px;
        text-align:center; position:relative; }}
    .book-header h1 {{ font-size:22px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:13px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.2); padding:4px 12px; border-radius:20px;
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

    .q-num {{ background:{cp}; color:#fff; min-width:26px; height:26px;
        border-radius:50%; display:inline-flex; align-items:center;
        justify-content:center; font-weight:800; font-size:12px; flex-shrink:0; }}
    .q-text {{ flex:1; line-height:1.6; }}
    .q-line {{ display:flex; align-items:center; gap:10px; width:100%; }}

    .exercise-row {{ padding:12px 18px; border-bottom:1px solid #1A2035;
        display:flex; gap:10px; align-items:flex-start; }}
    .exercise-row:last-child {{ border-bottom:none; }}
    .q-body {{ flex:1; }}
    .q-badge {{ display:inline-block; font-size:11px; font-weight:700;
        padding:2px 8px; border-radius:6px; margin-bottom:4px;
        background:#dbeafe; color:#1e40af; }}
    .q-badge.reorder {{ background:#fef3c7; color:#92400e; }}
    .q-badge.error {{ background:#fee2e2; color:#991b1b; }}

    .answer-input {{ width:100%; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; padding:6px 4px;
        color:{cp}; font-weight:600; outline:none; margin-top:6px; }}
    .answer-input:focus {{ border-bottom-color:{cp}; background:#111827; }}
    .answer-input.correct {{ border-bottom-color:#059669; color:#059669; background:#ecfdf5; }}
    .answer-input.wrong {{ border-bottom-color:#dc2626; color:#dc2626; background:#fef2f2; }}
    .answer-input.short {{ max-width:300px; }}

    .blank-input {{ width:100px; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; font-weight:600;
        color:{cp}; text-align:center; padding:2px 4px; outline:none; }}
    .blank-input.correct {{ border-bottom-color:#059669; color:#059669; background:#ecfdf5; }}
    .blank-input.wrong {{ border-bottom-color:#dc2626; color:#dc2626; background:#fef2f2; }}

    .word-bank {{ padding:10px 18px; background:#111827; display:flex;
        flex-wrap:wrap; gap:6px; border-bottom:2px solid #e2e8f0; }}
    .word-chip {{ background:#dbeafe; color:#1e40af; padding:4px 12px;
        border-radius:20px; font-weight:700; font-size:12px; }}

    .grammar-topics {{ padding:10px 18px; background:#111827;
        border-bottom:1px solid #e2e8f0; display:flex; gap:8px; flex-wrap:wrap; }}
    .topic-tag {{ background:{cp}22; color:{cp}; padding:3px 10px;
        border-radius:8px; font-size:12px; font-weight:600; }}

    /* Vocab */
    .vocab-match-row {{ padding:10px 18px; border-bottom:1px solid #1A2035;
        display:flex; align-items:center; gap:10px; }}
    .vocab-word {{ font-weight:700; color:{cp}; min-width:100px; cursor:pointer; }}
    .vocab-word:hover {{ text-decoration:underline; }}
    .scrambled {{ font-family:monospace; font-size:16px; font-weight:700;
        color:#94a3b8; letter-spacing:3px; min-width:100px; }}

    .odd-row {{ padding:10px 18px; border-bottom:1px solid #1A2035;
        display:flex; align-items:center; gap:10px; }}
    .odd-options {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .odd-btn {{ padding:6px 14px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .odd-btn:hover {{ border-color:{ca}; background:{cb}; }}
    .odd-btn.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .odd-btn.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .odd-btn.disabled {{ pointer-events:none; opacity:.5; }}

    /* MCQ */
    .mcq-row {{ padding:10px 18px; border-bottom:1px solid #1A2035; }}
    .mcq-options {{ display:flex; flex-wrap:wrap; gap:6px; padding:6px 0 0 36px; }}
    .mcq-opt {{ padding:6px 16px; border:2px solid #e2e8f0; border-radius:10px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .mcq-opt:hover {{ border-color:{ca}; background:{cb}; }}
    .mcq-opt.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .mcq-opt.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .mcq-opt.disabled {{ pointer-events:none; opacity:.5; }}

    .paragraph-box {{ padding:14px 18px; line-height:2; }}
    .para-sent {{ display:inline; }}

    /* Writing */
    .writing-task {{ padding:14px 18px; border-bottom:1px solid #1A2035; }}
    .writing-task:last-child {{ border-bottom:none; }}
    .writing-header {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; }}
    .writing-badge {{ font-size:11px; font-weight:700; padding:2px 8px;
        border-radius:6px; background:#fef3c7; color:#92400e; }}
    .writing-title {{ font-weight:700; color:#94A3B8; }}
    .writing-instruction {{ font-size:13px; color:#64748b; margin-bottom:8px;
        padding-left:36px; font-style:italic; }}
    .writing-area {{ width:100%; border:2px solid #e2e8f0; border-radius:10px;
        padding:12px; font-size:inherit; font-family:inherit; resize:vertical;
        outline:none; min-height:80px; }}
    .writing-area:focus {{ border-color:{ca}; }}
    .writing-tools {{ display:flex; justify-content:space-between; align-items:center;
        padding:4px 0; }}
    .word-counter {{ font-size:12px; color:#94a3b8; }}
    .hint-btn {{ background:none; border:none; font-size:18px; cursor:pointer; }}

    /* Test */
    .test-info {{ padding:10px 18px; background:#fef2f2; font-size:13px;
        color:#991b1b; font-weight:600; border-bottom:1px solid #fecaca; }}
    .test-section {{ padding:10px 0; }}
    .test-section-title {{ padding:8px 18px; font-weight:700; font-size:14px;
        color:{cp}; background:#111827; border-bottom:1px solid #e2e8f0; }}
    .test-q {{ padding:10px 18px; border-bottom:1px solid #1A2035;
        display:flex; align-items:flex-start; gap:10px; flex-wrap:wrap; }}
    .test-options {{ display:flex; flex-wrap:wrap; gap:6px; width:100%; padding-left:36px; }}
    .test-opt {{ padding:5px 14px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .test-opt:hover {{ border-color:{ca}; }}
    .test-opt.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .test-opt.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .test-opt.disabled {{ pointer-events:none; opacity:.5; }}
    .tf-buttons {{ display:flex; gap:6px; margin-left:auto; }}
    .tf-btn {{ padding:5px 12px; border:2px solid #e2e8f0; border-radius:8px;
        font-weight:600; font-size:13px; cursor:pointer; background:#fff; transition:.2s; }}
    .tf-btn.correct {{ background:#059669; color:#fff; border-color:#059669; }}
    .tf-btn.wrong {{ background:#dc2626; color:#fff; border-color:#dc2626; }}
    .tf-btn.disabled {{ pointer-events:none; opacity:.5; }}
    .test-score-bar {{ padding:14px 18px; background:#111827; text-align:center;
        font-weight:700; font-size:16px; color:{cp}; border-top:2px solid #e2e8f0; }}

    @keyframes pop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.1)}} 100%{{transform:scale(1)}} }}
    .pop {{ animation:pop .3s ease; }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-4px)}} 75%{{transform:translateX(4px)}} }}
    .shake {{ animation:shake .3s ease; }}
    </style>'''


def _pp_scripts() -> str:
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

    function checkTF(el, answer, chosen) {
        var parent = el.closest('.test-q');
        var btns = parent.querySelectorAll('.tf-btn');
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

    function checkOdd(el, oddWord, chosen) {
        var parent = el.closest('.odd-row');
        var btns = parent.querySelectorAll('.odd-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === oddWord) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => { if (b.textContent.trim() === oddWord) b.classList.add('correct'); });
            updateScore(false);
        }
    }

    /* Word counter for writing areas */
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.writing-area').forEach(function(ta, idx) {
            ta.addEventListener('input', function() {
                var words = ta.value.trim().split(/\\s+/).filter(w => w.length > 0).length;
                var counter = document.getElementById('wc_' + idx);
                if (counter) counter.textContent = words + ' words';
            });
        });
    });
    </script>'''


# ══════════════════════════════════════════════════════════════════════════════
# VOCAB REVIEW HEADER
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
    "📝 Grammar Practice",
    "📚 Vocabulary Review",
    "✅ Multiple Choice & Paragraph",
    "✍️ Mini Writing Tasks",
    "📋 Unit Test",
]


def build_practice_plus_pages(grade: int, week_num: int,
                               curriculum_weeks: list) -> list[str]:
    """Build Practice Plus pages for a given grade/week.

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

    # Extract grammar topics and writing prompts from linked_content
    linked = week_data.get("linked_content", {})
    grammar_topics = linked.get("grammar", [])
    writings = linked.get("writings", [])

    unit_num = max(1, (week_num - 1) // 4 + 1)

    styles = _pp_styles(cfg)
    scripts = _pp_scripts()
    vocab_header = _build_vocab_header(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>📘 Practice Plus — Unit {unit_num}</h1>
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

    page1 = _wrap(1, _build_grammar_practice(vocab, structure, grammar_topics, grade, cfg, seed))
    page2 = _wrap(2, _build_vocabulary_review(vocab, grade, cfg, seed))
    page3 = _wrap(3, _build_mcq_paragraph(vocab, structure, grade, cfg, seed))
    page4 = _wrap(4, _build_writing_tasks(vocab, structure, theme, theme_tr, writings, grade, cfg, seed))
    page5 = _wrap(5, _build_unit_test(vocab, structure, grammar_topics, grade, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_practice_plus(grade: int, curriculum_weeks: list,
                              selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Practice Plus for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_practice_plus_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
