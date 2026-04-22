# -*- coding: utf-8 -*-
"""Performance Book — Lise (9-12) Alıştırma / Pekiştirme Kitabı.

Interactive HTML exercise pages for high school English learners.
Exercise types (5 pages per week):
  1. Grammar & Sentence Transformations (Dilbilgisi + Cümle dönüşümleri)
  2. Vocabulary Practice (Kelime çalışmaları)
  3. Reading Comprehension (Okuduğunu anlama soruları)
  4. Paragraph & Writing Tasks (Paragraf çalışmaları + Yazma görevleri)
  5. Mixed Review Test (Karma tekrar testi)

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
        "grammar_count": 10, "transform_count": 6, "reading_count": 8,
        "writing_count": 3, "test_count": 15, "para_count": 5,
        "color_primary": "#0d47a1", "color_accent": "#42a5f5", "color_bg": "#e3f2fd"},
    10: {"label": "10th Grade • B1.2", "font_size": "14px", "vocab_count": 18,
         "grammar_count": 12, "transform_count": 8, "reading_count": 10,
         "writing_count": 4, "test_count": 18, "para_count": 6,
         "color_primary": "#4a148c", "color_accent": "#ab47bc", "color_bg": "#f3e5f5"},
    11: {"label": "11th Grade • B2.1", "font_size": "13px", "vocab_count": 20,
         "grammar_count": 12, "transform_count": 8, "reading_count": 10,
         "writing_count": 4, "test_count": 20, "para_count": 6,
         "color_primary": "#1b5e20", "color_accent": "#66bb6a", "color_bg": "#e8f5e9"},
    12: {"label": "12th Grade • B2.2", "font_size": "13px", "vocab_count": 22,
         "grammar_count": 14, "transform_count": 10, "reading_count": 12,
         "writing_count": 5, "test_count": 22, "para_count": 8,
         "color_primary": "#b71c1c", "color_accent": "#ef5350", "color_bg": "#ffebee"},
}


def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"perf_{grade}_{week}".encode()).hexdigest()[:8], 16)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def _extract_patterns(structure: str) -> list[str]:
    return [p.strip() for p in structure.replace("?", "?.").split(".")
            if p.strip() and len(p.strip()) > 5]


def _make_sentences(vocab: list, structure: str, count: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    sentences = []
    patterns = _extract_patterns(structure)

    for v in vocab:
        for pat in patterns[:3]:
            if "..." in pat:
                sent = pat.replace("...", f" {v}")
                sentences.append({"sentence": sent.strip(), "word": v, "original": pat})
            elif v.lower() not in pat.lower():
                sentences.append({"sentence": f"{pat} {v}.", "word": v, "original": pat})

    _fallback = [
        "The teacher explained {w} clearly.",
        "We discussed {w} in class.",
        "She demonstrated {w} with examples.",
        "The article describes {w} in detail.",
        "They analysed {w} thoroughly.",
        "He presented {w} at the seminar.",
        "The documentary covered {w} extensively.",
        "Students should understand {w} before the exam.",
        "Research shows that {w} is important.",
        "The professor emphasised the role of {w}.",
    ]
    for v in vocab:
        pat = _fallback[hash(v) % len(_fallback)]
        sentences.append({"sentence": pat.format(w=v), "word": v, "original": pat})

    rng.shuffle(sentences)
    return sentences[:count * 2]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Grammar & Sentence Transformations
# ══════════════════════════════════════════════════════════════════════════════

def _build_grammar_transformations(vocab: list, structure: str, grammar_topics: list,
                                    grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)
    patterns = _extract_patterns(structure)

    # Grammar topic header
    topics_html = ""
    if grammar_topics:
        topics_html = '<div class="grammar-topics">' + " • ".join(
            f'<span class="topic-tag">{t}</span>' for t in grammar_topics[:4]
        ) + '</div>'

    rows = ""
    q_num = 0

    # Part A: Fill in the correct form
    rows += '<div class="sub-section"><div class="sub-title">A. Complete with the correct form</div>'
    for v in vocab[:cfg["grammar_count"] // 2]:
        for pat in patterns[:2]:
            if q_num >= cfg["grammar_count"]:
                break
            q_num += 1
            if "..." in pat:
                sent = pat.replace("...", f" ______ ({v})")
            else:
                sent = f"{pat} ______ ({v})."
            rows += f'''<div class="exercise-row">
                <span class="q-num">{q_num}</span>
                <div class="q-body">
                    <div class="q-badge">Fill in</div>
                    <div class="q-text">{sent.strip()}</div>
                    <input type="text" class="answer-input" data-answer="{v}"
                           placeholder="Type your answer..." onblur="checkAnswer(this)">
                </div>
            </div>'''
        if q_num >= cfg["grammar_count"]:
            break
    rows += '</div>'

    # Part B: Sentence transformations
    rows += '<div class="sub-section"><div class="sub-title">B. Rewrite the sentences as directed</div>'
    _transform_types = [
        ("Active → Passive", "Rewrite in passive voice"),
        ("Direct → Indirect", "Change to reported speech"),
        ("Positive → Negative", "Make the sentence negative"),
        ("Statement → Question", "Turn into a question"),
        ("Simple → Complex", "Combine using a relative clause"),
        ("Formal → Informal", "Rewrite in informal English"),
        ("If-clause transformation", "Rewrite using a conditional"),
        ("Too/Enough transformation", "Rewrite using too/enough"),
    ]

    t_count = 0
    for pat in patterns[:cfg["transform_count"]]:
        if t_count >= cfg["transform_count"]:
            break
        t_type = _transform_types[t_count % len(_transform_types)]
        t_count += 1
        q_num += 1
        rows += f'''<div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-badge transform">{t_type[0]}</div>
                <div class="q-text">{pat}</div>
                <div class="q-hint">→ {t_type[1]}</div>
                <textarea class="transform-area" rows="2"
                          placeholder="Write your answer..."></textarea>
            </div>
        </div>'''
    rows += '</div>'

    # Part C: Error correction
    rows += '<div class="sub-section"><div class="sub-title">C. Find and correct the errors</div>'
    for pat in patterns[:3]:
        words = pat.split()
        if len(words) >= 4:
            q_num += 1
            idx = rng.randint(1, min(len(words) - 1, len(words) - 2))
            wrong = list(words)
            wrong[idx], wrong[idx - 1] = wrong[idx - 1], wrong[idx]
            rows += f'''<div class="exercise-row">
                <span class="q-num">{q_num}</span>
                <div class="q-body">
                    <div class="q-badge error">Find & Fix</div>
                    <div class="q-text" style="text-decoration:underline wavy #dc2626;">
                        {" ".join(wrong)}</div>
                    <input type="text" class="answer-input" data-answer="{pat}"
                           placeholder="Write the corrected sentence..." onblur="checkAnswer(this)">
                </div>
            </div>'''
    rows += '</div>'

    return f'''
    <div class="section-box" style="border-color:#42a5f5;">
        <div class="section-title" style="background:linear-gradient(135deg,#0d47a1,#42a5f5);">
            <span class="section-icon">📝</span> Grammar & Sentence Transformations</div>
        {topics_html}
        {rows}
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Vocabulary Practice
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocabulary_practice(vocab: list, structure: str, grade: int,
                                cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 10)
    words = vocab[:cfg["vocab_count"]]

    # Part A: Contextual usage — fill the gap
    ctx_items = ""
    patterns = _extract_patterns(structure)
    q_num = 0
    for w in words[:8]:
        q_num += 1
        if patterns:
            pat = patterns[q_num % len(patterns)]
            if "..." in pat:
                sent = pat.replace("...", "______")
            else:
                sent = f"{pat} ______."
        else:
            sent = f"We should ______ every day."
        ctx_items += f'''<div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <div class="q-text">{sent}</div>
                <input type="text" class="answer-input" data-answer="{w}"
                       placeholder="({w[0]}...)" onblur="checkAnswer(this)">
            </div>
        </div>'''

    # Part B: Word formation (derivation)
    formation_items = ""
    _suffixes = [
        ("-tion/-sion", "noun form"), ("-ment", "noun form"),
        ("-ful/-less", "adjective form"), ("-ly", "adverb form"),
        ("-ive/-ous", "adjective form"), ("-er/-or", "agent noun"),
        ("-ness", "noun form"), ("-able/-ible", "adjective form"),
    ]
    for i, w in enumerate(words[:6]):
        q_num += 1
        suffix = _suffixes[i % len(_suffixes)]
        formation_items += f'''<div class="vocab-match-row">
            <span class="q-num">{q_num}</span>
            <span class="vocab-word" onclick="speak('{w}')">{w} 🔊</span>
            <span class="formation-hint">{suffix[0]} → {suffix[1]}</span>
            <input type="text" class="answer-input short"
                   placeholder="Derived form..." >
        </div>'''

    # Part C: Synonyms & Antonyms matching
    match_items = ""
    shuffled = list(words[:8])
    rng.shuffle(shuffled)
    for i, w in enumerate(shuffled[:6]):
        q_num += 1
        match_items += f'''<div class="vocab-match-row">
            <span class="q-num">{q_num}</span>
            <span class="vocab-word" onclick="speak('{w}')">{w} 🔊</span>
            <input type="text" class="answer-input short"
                   placeholder="Write a synonym..." >
            <input type="text" class="answer-input short"
                   placeholder="Write an antonym..." >
        </div>'''

    # Part D: Use in a sentence
    sentence_items = ""
    for i, w in enumerate(words[:4]):
        q_num += 1
        sentence_items += f'''<div class="exercise-row">
            <span class="q-num">{q_num}</span>
            <div class="q-body">
                <span class="vocab-word" style="display:inline-block;margin-bottom:6px;"
                      onclick="speak('{w}')">{w} 🔊</span>
                <textarea class="transform-area" rows="2"
                          placeholder="Write a sentence using '{w}'..."></textarea>
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#66bb6a;">
        <div class="section-title" style="background:linear-gradient(135deg,#1b5e20,#66bb6a);">
            <span class="section-icon">📚</span> Vocabulary Practice</div>

        <div class="sub-section">
            <div class="sub-title">A. Fill in with the correct word</div>
            {ctx_items}
        </div>

        <div class="sub-section">
            <div class="sub-title">B. Word Formation — Write the derived form</div>
            {formation_items}
        </div>

        <div class="sub-section">
            <div class="sub-title">C. Synonyms & Antonyms</div>
            {match_items}
        </div>

        <div class="sub-section">
            <div class="sub-title">D. Use each word in a meaningful sentence</div>
            {sentence_items}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Reading Comprehension
# ══════════════════════════════════════════════════════════════════════════════

def _build_reading_comprehension(vocab: list, structure: str, theme: str,
                                  theme_tr: str, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 20)

    # Generate a reading passage from vocab and theme
    _passage_templates = [
        "In today's world, {theme} plays an important role in our daily lives. "
        "Many people {v1} as part of their routine. Experts suggest that {v2} "
        "can lead to significant improvements. Furthermore, {v3} has become "
        "increasingly popular among young people. Studies show that those who "
        "{v4} regularly tend to be more successful. It is important to note that "
        "{v5} requires dedication and practice. In conclusion, {theme} continues "
        "to shape the way we think and act.",

        "The concept of {theme} has evolved significantly over the past decades. "
        "Researchers have found that {v1} contributes to personal development. "
        "While some argue that {v2} is unnecessary, others believe it is essential. "
        "A recent survey revealed that {v3} is the most valued aspect of {theme}. "
        "Moreover, the ability to {v4} distinguishes successful individuals from others. "
        "As we move forward, understanding {v5} will become even more critical. "
        "Therefore, investing time in {theme} is highly recommended.",

        "{theme} is a topic that has attracted considerable attention recently. "
        "According to specialists, {v1} and {v2} are closely interconnected. "
        "The benefits of {v3} extend beyond personal growth to societal improvement. "
        "However, challenges such as {v4} can hinder progress. "
        "Despite these obstacles, {v5} remains a priority for educators worldwide. "
        "By embracing {theme}, individuals can unlock their full potential "
        "and contribute meaningfully to their communities.",
    ]

    vlist = vocab[:6] if len(vocab) >= 6 else vocab + ["learning"] * (6 - len(vocab))
    template = rng.choice(_passage_templates)
    passage = template.format(
        theme=theme.lower(),
        v1=vlist[0], v2=vlist[1], v3=vlist[2],
        v4=vlist[3], v5=vlist[4],
    )

    # Part A: Comprehension MCQ
    _comp_questions = [
        (f"What is the main idea of the passage?",
         f"The importance of {theme.lower()}", f"The history of sports",
         f"How to cook", f"Travel destinations"),
        (f"According to the passage, what contributes to success?",
         f"Regular practice of {vlist[0]}", f"Watching television",
         f"Skipping classes", f"Sleeping late"),
        (f"Which word best describes the tone of the passage?",
         "Informative", "Humorous", "Angry", "Fictional"),
        (f"The word '{vlist[2]}' in the passage is closest in meaning to:",
         "activity", "problem", "location", "animal"),
        (f"What can be inferred from the passage?",
         f"{theme} is beneficial", f"{theme} is harmful",
         f"{theme} is outdated", f"{theme} is irrelevant"),
    ]

    mcq_html = ""
    for i, (q, correct, *wrong) in enumerate(_comp_questions[:cfg["reading_count"] // 2]):
        options = [correct] + list(wrong)
        rng.shuffle(options)
        letters = ["A", "B", "C", "D"]
        opts = " ".join(
            f'<button class="mcq-opt" onclick="checkMCQ(this,\'{correct}\',\'{o}\')">'
            f'{letters[j]}) {o}</button>'
            for j, o in enumerate(options)
        )
        mcq_html += f'''<div class="mcq-row">
            <div class="q-line"><span class="q-num">{i+1}</span>
                <span class="q-text">{q}</span></div>
            <div class="mcq-options">{opts}</div>
        </div>'''

    # Part B: True/False/Not Given
    _tf_items = [
        (f"{theme} has become less important over time.", "false"),
        (f"The passage mentions the role of {vlist[0]}.", "true"),
        (f"The author provides statistical data.", "not given"),
        (f"{vlist[2].capitalize()} is described as popular.", "true"),
        (f"The passage criticises modern education.", "false"),
    ]

    tf_html = ""
    for i, (stmt, answer) in enumerate(_tf_items[:cfg["reading_count"] // 2]):
        q_num = len(_comp_questions[:cfg["reading_count"] // 2]) + i + 1
        tf_html += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{stmt}</span>
            <div class="tf-buttons">
                <button class="tf-btn" onclick="checkTF3(this,'{answer}','true')">✓ True</button>
                <button class="tf-btn" onclick="checkTF3(this,'{answer}','false')">✗ False</button>
                <button class="tf-btn" onclick="checkTF3(this,'{answer}','not given')">? Not Given</button>
            </div>
        </div>'''

    return f'''
    <div class="section-box" style="border-color:#7c3aed;">
        <div class="section-title" style="background:linear-gradient(135deg,#4a148c,#7c3aed);">
            <span class="section-icon">📖</span> Reading Comprehension</div>

        <div class="reading-passage">
            <div class="passage-title">Read the following passage carefully:</div>
            <div class="passage-text">{passage}</div>
        </div>

        <div class="sub-section">
            <div class="sub-title">A. Choose the correct answer</div>
            {mcq_html}
        </div>

        <div class="sub-section">
            <div class="sub-title">B. True / False / Not Given</div>
            {tf_html}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Paragraph Work & Writing Tasks
# ══════════════════════════════════════════════════════════════════════════════

def _build_paragraph_writing(vocab: list, structure: str, theme: str, theme_tr: str,
                              writings: list, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 30)

    # Part A: Paragraph completion (cloze)
    para_words = vocab[:cfg["para_count"]]
    rng2 = random.Random(seed + 35)
    para_sentences = []
    _templates = [
        f"Education is important because {{w}} helps students grow.",
        f"Many people believe that {{w}} is essential for success.",
        f"In modern society, {{w}} has become a key factor.",
        f"Research indicates that {{w}} improves critical thinking.",
        f"The school curriculum emphasises {{w}} at every level.",
        f"Students who practise {{w}} show better results.",
        f"Cultural awareness includes understanding {{w}} deeply.",
        f"Technology has transformed how we approach {{w}}.",
    ]
    for w in para_words:
        tmpl = rng2.choice(_templates)
        para_sentences.append((tmpl.format(w=w), w))

    rng2.shuffle(para_sentences)
    bank_words = [w for _, w in para_sentences]
    rng2.shuffle(bank_words)

    para_html = '<div class="word-bank">' + " ".join(
        f'<span class="word-chip">{w}</span>' for w in bank_words
    ) + '</div>'
    para_html += '<div class="paragraph-box">'
    for i, (sent, word) in enumerate(para_sentences):
        blank_sent = sent.replace(word,
            f'<input type="text" class="blank-input" data-answer="{word}" '
            f'placeholder="..." onblur="checkAnswer(this)">')
        para_html += f'<span class="para-sent">{i+1}. {blank_sent} </span>'
    para_html += '</div>'

    # Part B: Writing tasks
    tasks = []
    tasks.append({
        "title": f"Write a well-structured paragraph about: {theme}",
        "instruction": f"Use at least 5 vocabulary words: {', '.join(vocab[:5])}. "
                       "Include a topic sentence, supporting sentences, and a concluding sentence.",
        "type": "paragraph",
        "min_lines": 6,
    })

    if writings:
        w_topic = writings[0] if isinstance(writings, list) else str(writings)
        tasks.append({
            "title": f"Essay Task: {w_topic}",
            "instruction": "Write at least 8-10 sentences. Use appropriate grammar structures "
                           "and a variety of vocabulary. Organise your ideas clearly.",
            "type": "essay",
            "min_lines": 8,
        })

    _creative = [
        f"Write a formal email about {theme} to your school principal.",
        f"Write a compare-and-contrast paragraph about two aspects of {theme}.",
        f"Write an opinion paragraph: 'Do you agree that {theme.lower()} is essential?'",
        f"Write a cause-and-effect paragraph about {theme}.",
    ]
    tasks.append({
        "title": rng.choice(_creative),
        "instruction": "Use formal language. Include linking words (however, moreover, in addition, etc.).",
        "type": "formal",
        "min_lines": 7,
    })

    tasks.append({
        "title": f"Summarise this topic in your own words: {theme}",
        "instruction": "Write a 4-5 sentence summary using paraphrasing techniques.",
        "type": "summary",
        "min_lines": 5,
    })

    tasks = tasks[:cfg["writing_count"] + 1]

    tasks_html = ""
    for i, task in enumerate(tasks):
        type_badge = {"paragraph": "📄 Paragraph", "essay": "📖 Essay",
                      "formal": "📝 Formal", "creative": "✨ Creative",
                      "summary": "📋 Summary"}.get(task["type"], "📝")
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
        <div class="section-title" style="background:linear-gradient(135deg,#e65100,#f59e0b);">
            <span class="section-icon">✍️</span> Paragraph Work & Writing Tasks</div>

        <div class="sub-section">
            <div class="sub-title">A. Complete the paragraph with the words from the box</div>
            {para_html}
        </div>

        <div class="sub-section">
            <div class="sub-title">B. Writing Tasks</div>
            {tasks_html}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Mixed Review Test
# ══════════════════════════════════════════════════════════════════════════════

def _build_mixed_review_test(vocab: list, structure: str, grammar_topics: list,
                              theme: str, grade: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 40)
    sentences = _make_sentences(vocab, structure, cfg["test_count"], seed + 40)

    questions = ""
    q_num = 0
    total_pts = 0

    # Section A: MCQ — Grammar & Vocabulary (30 pts)
    questions += '<div class="test-section"><div class="test-section-title">A. Choose the correct answer (3 points each)</div>'
    used = set()
    for s in sentences:
        if s["word"] in used or q_num >= 6:
            continue
        used.add(s["word"])
        q_num += 1
        total_pts += 3
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

    # Section B: True/False (15 pts)
    questions += '<div class="test-section"><div class="test-section-title">B. True or False (3 points each)</div>'
    tf_items = []
    for s in sentences[6:]:
        if s["word"] in used or len(tf_items) >= 5:
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
        total_pts += 3
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{item["text"]}</span>
            <div class="tf-buttons">
                <button class="tf-btn" onclick="checkTF(this,'{item["answer"]}','true')">✓ True</button>
                <button class="tf-btn" onclick="checkTF(this,'{item["answer"]}','false')">✗ False</button>
            </div>
        </div>'''
    questions += '</div>'

    # Section C: Fill in the blanks (15 pts)
    questions += '<div class="test-section"><div class="test-section-title">C. Fill in the blanks (3 points each)</div>'
    fill_words = [v for v in vocab if v not in used][:5]
    _fill_templates = [
        "The students ______ to improve their skills.",
        "We should ______ more attention to details.",
        "She always ______ before making a decision.",
        "They ______ the importance of teamwork.",
        "He ______ the results of the experiment.",
    ]
    for i, w in enumerate(fill_words):
        q_num += 1
        total_pts += 3
        tmpl = _fill_templates[i % len(_fill_templates)]
        questions += f'''<div class="test-q">
            <span class="q-num">{q_num}</span>
            <span class="q-text">{tmpl}</span>
            <input type="text" class="answer-input" data-answer="{w}"
                   placeholder="({w[0]}...)" onblur="checkAnswer(this)">
        </div>'''
    questions += '</div>'

    # Section D: Sentence Transformation (20 pts)
    questions += '<div class="test-section"><div class="test-section-title">D. Rewrite as directed (5 points each)</div>'
    patterns = _extract_patterns(structure)
    _transforms = [
        "Rewrite in passive voice", "Change to reported speech",
        "Rewrite using a conditional", "Turn into a question",
    ]
    for i, pat in enumerate(patterns[:4]):
        q_num += 1
        total_pts += 5
        t_instr = _transforms[i % len(_transforms)]
        questions += f'''<div class="test-q" style="flex-direction:column;">
            <div style="display:flex;gap:10px;align-items:center;">
                <span class="q-num">{q_num}</span>
                <span class="q-text">{pat}</span>
            </div>
            <div class="q-hint" style="margin-left:36px;">→ {t_instr}</div>
            <textarea class="transform-area" rows="2" style="margin-left:36px;margin-top:6px;"
                      placeholder="Write your answer..."></textarea>
        </div>'''
    questions += '</div>'

    # Section E: Writing (20 pts)
    q_num += 1
    total_pts += 20
    questions += f'''<div class="test-section">
        <div class="test-section-title">E. Writing (20 points)</div>
        <div class="test-q" style="flex-direction:column;">
            <div style="display:flex;gap:10px;align-items:center;">
                <span class="q-num">{q_num}</span>
                <span class="q-text">Write a well-organised paragraph (8-10 sentences) about
                "<b>{theme}</b>". Use at least 5 vocabulary words from this unit.
                Include an introduction, body, and conclusion.</span>
            </div>
            <textarea class="writing-area" rows="10" style="margin-top:8px;"
                      placeholder="Write your essay here..."></textarea>
            <div class="writing-tools">
                <span class="word-counter" id="wc_test">0 words</span>
            </div>
        </div>
    </div>'''

    return f'''
    <div class="section-box" style="border-color:#dc2626;">
        <div class="section-title" style="background:linear-gradient(135deg,#b71c1c,#dc2626);">
            <span class="section-icon">📋</span> Mixed Review Test — Total: {total_pts} points</div>
        <div class="test-info">⏱ Time: 45 minutes | 📊 Passing score: 60% |
            Grammar • Vocabulary • Reading • Writing</div>
        {questions}
        <div class="test-score-bar">
            <span>Your Score:</span>
            <span class="counter" id="testScore">0</span> / {total_pts}
        </div>
    </div>'''


# ══════════════════════════════════════════════════════════════════════════════
# STYLES & SCRIPTS
# ══════════════════════════════════════════════════════════════════════════════

def _perf_styles(cfg: dict) -> str:
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
        text-align:center; position:relative; }}
    .book-header h1 {{ font-size:22px; margin-bottom:4px; }}
    .book-header .subtitle {{ font-size:13px; opacity:.85; }}
    .book-header .grade-badge {{ position:absolute; top:10px; right:14px;
        background:rgba(255,255,255,.2); padding:4px 14px; border-radius:20px;
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
    .q-hint {{ font-size:12px; color:#64748b; font-style:italic; margin-top:4px; }}

    .exercise-row {{ padding:12px 18px; border-bottom:1px solid #1A2035;
        display:flex; gap:10px; align-items:flex-start; }}
    .exercise-row:last-child {{ border-bottom:none; }}
    .q-body {{ flex:1; }}
    .q-badge {{ display:inline-block; font-size:11px; font-weight:700;
        padding:2px 8px; border-radius:6px; margin-bottom:4px;
        background:#dbeafe; color:#1e40af; }}
    .q-badge.transform {{ background:#ede9fe; color:#5b21b6; }}
    .q-badge.error {{ background:#fee2e2; color:#991b1b; }}

    .answer-input {{ width:100%; border:none; border-bottom:2px dashed {ca};
        background:transparent; font-size:inherit; padding:6px 4px;
        color:{cp}; font-weight:600; outline:none; margin-top:6px; }}
    .answer-input:focus {{ border-bottom-color:{cp}; background:#111827; }}
    .answer-input.correct {{ border-bottom-color:#059669; color:#059669; background:#ecfdf5; }}
    .answer-input.wrong {{ border-bottom-color:#dc2626; color:#dc2626; background:#fef2f2; }}
    .answer-input.short {{ max-width:200px; display:inline-block; margin:0 6px; }}

    .transform-area {{ width:100%; border:2px solid #e2e8f0; border-radius:8px;
        padding:8px 12px; font-size:inherit; font-family:inherit; resize:vertical;
        outline:none; margin-top:6px; }}
    .transform-area:focus {{ border-color:{ca}; }}

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
        display:flex; align-items:center; gap:10px; flex-wrap:wrap; }}
    .vocab-word {{ font-weight:700; color:{cp}; min-width:100px; cursor:pointer; }}
    .vocab-word:hover {{ text-decoration:underline; }}
    .formation-hint {{ font-size:12px; color:#64748b; background:#1A2035;
        padding:2px 8px; border-radius:6px; }}

    /* Reading */
    .reading-passage {{ padding:18px; background:#fafbfc; border-bottom:2px solid #e2e8f0; }}
    .passage-title {{ font-weight:700; color:{cp}; margin-bottom:10px; font-size:14px; }}
    .passage-text {{ line-height:1.8; text-align:justify; color:#94A3B8;
        font-size:14px; padding:12px 16px; background:#fff; border-radius:8px;
        border-left:4px solid {ca}; }}

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


def _perf_scripts() -> str:
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

    function checkTF3(el, answer, chosen) {
        var parent = el.closest('.test-q');
        var btns = parent.querySelectorAll('.tf-btn');
        btns.forEach(b => b.classList.add('disabled'));
        if (chosen === answer) {
            el.classList.add('correct','pop');
            updateScore(true);
        } else {
            el.classList.add('wrong','shake');
            btns.forEach(b => {
                if (b.textContent.toLowerCase().includes(answer)) b.classList.add('correct');
            });
            updateScore(false);
        }
    }

    /* Word counter for writing areas */
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.writing-area').forEach(function(ta, idx) {
            ta.addEventListener('input', function() {
                var words = ta.value.trim().split(/\\s+/).filter(w => w.length > 0).length;
                var counter = document.getElementById('wc_' + idx) || document.getElementById('wc_test');
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
    "📝 Grammar & Transformations",
    "📚 Vocabulary Practice",
    "📖 Reading Comprehension",
    "✍️ Paragraph & Writing",
    "📋 Mixed Review Test",
]


def build_performance_pages(grade: int, week_num: int,
                             curriculum_weeks: list) -> list[str]:
    """Build Performance Book pages for a given grade/week.

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
    writings = linked.get("writings", [])

    unit_num = max(1, (week_num - 1) // 4 + 1)

    styles = _perf_styles(cfg)
    scripts = _perf_scripts()
    vocab_header = _build_vocab_header(vocab)

    def _header(page_num: int) -> str:
        return f'''<div class="book-header">
            <div class="grade-badge">{cfg["label"]}</div>
            <h1>📘 Performance Book — Unit {unit_num}</h1>
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

    page1 = _wrap(1, _build_grammar_transformations(vocab, structure, grammar_topics, grade, cfg, seed))
    page2 = _wrap(2, _build_vocabulary_practice(vocab, structure, grade, cfg, seed))
    page3 = _wrap(3, _build_reading_comprehension(vocab, structure, theme, theme_tr, grade, cfg, seed))
    page4 = _wrap(4, _build_paragraph_writing(vocab, structure, theme, theme_tr, writings, grade, cfg, seed))
    page5 = _wrap(5, _build_mixed_review_test(vocab, structure, grammar_topics, theme, grade, cfg, seed))

    return [page1, page2, page3, page4, page5]


def build_full_performance_book(grade: int, curriculum_weeks: list,
                                 selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Performance Book for all weeks.

    Returns:
        List of dicts: [{"week": 1, "theme": "...", "pages": [html1..html5]}, ...]
    """
    weeks_to_gen = selected_weeks or [w["week"] for w in curriculum_weeks]
    result = []
    for wk in weeks_to_gen:
        pages = build_performance_pages(grade, wk, curriculum_weeks)
        if pages:
            theme = ""
            for w in curriculum_weeks:
                if w["week"] == wk:
                    theme = w.get("theme", "")
                    break
            result.append({"week": wk, "theme": theme, "pages": pages})
    return result
