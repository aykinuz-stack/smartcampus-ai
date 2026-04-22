# -*- coding: utf-8 -*-
"""
KDG Interaktif Calisma Modulu - CEFR Uyumlu, 5 Dil Destekli
SmartCampusAI - Kisisel Dil Gelisimi Hub
Diamond Premium Theme - Web Speech API TTS
"""
import json
import streamlit as st
import streamlit.components.v1 as components

from views._kdg_data_prea1 import DATA_PREA1
from views._kdg_data_a1 import DATA_A1
from views._kdg_data_a1plus import DATA_A1PLUS
from views._kdg_data_a2 import DATA_A2
from views._kdg_data_b1 import DATA_B1
from views._kdg_data_b2 import DATA_B2
from views._kdg_data_c1 import DATA_C1

# ── LEVEL MAPPING ────────────────────────────────────────────────────────────
_LEVEL_GROUP = {
    "preschool": "preschool",
    "grade1": "grade1_2", "grade2": "grade1_2",
    "grade3": "grade3_4", "grade4": "grade3_4",
    "grade5": "grade5_6", "grade6": "grade5_6",
    "grade7": "grade7_8", "grade8": "grade7_8",
    "grade9": "grade9_10", "grade10": "grade9_10",
    "grade11": "grade11_12", "grade12": "grade11_12",
}

_LEVEL_LABELS = {
    "preschool": "Pre-A1 (Okul Oncesi)",
    "grade1_2": "A1 (1-2. Sinif)",
    "grade3_4": "A1+/A2 (3-4. Sinif)",
    "grade5_6": "A2/A2+ (5-6. Sinif)",
    "grade7_8": "B1 (7-8. Sinif)",
    "grade9_10": "B1+/B2 (9-10. Sinif)",
    "grade11_12": "B2+/C1 (11-12. Sinif)",
}

# ── LEVEL DATA (imported from separate files) ────────────────────────────────
LEVEL_DATA = {
    "preschool": DATA_PREA1,
    "grade1_2": DATA_A1,
    "grade3_4": DATA_A1PLUS,
    "grade5_6": DATA_A2,
    "grade7_8": DATA_B1,
    "grade9_10": DATA_B2,
    "grade11_12": DATA_C1,
}


# ── LANGUAGE CONFIG ──────────────────────────────────────────────────────────
_LANG_CONFIG = {
    "en": {"label": "\U0001f1ec\U0001f1e7 English", "code": "en-US", "name": "English"},
    "de": {"label": "\U0001f1e9\U0001f1ea Almanca", "code": "de-DE", "name": "Deutsch"},
    "fr": {"label": "\U0001f1eb\U0001f1f7 Fransizca", "code": "fr-FR", "name": "Francais"},
    "it": {"label": "\U0001f1ee\U0001f1f9 Italyanca", "code": "it-IT", "name": "Italiano"},
    "es": {"label": "\U0001f1ea\U0001f1f8 Ispanyolca", "code": "es-ES", "name": "Espanol"},
}

# ── DIAMOND CSS ──────────────────────────────────────────────────────────────
_DIAMOND_CSS = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0e27; color: #e0e0e0; }
.lang-bar { display: flex; gap: 8px; justify-content: center; padding: 12px; background: linear-gradient(135deg, #0d1137 0%, #141852 100%); border-radius: 12px; margin-bottom: 16px; border: 1px solid rgba(199,165,93,0.3); }
.lang-btn { padding: 8px 16px; border: 2px solid rgba(199,165,93,0.3); background: rgba(20,24,82,0.6); color: #c7a55d; border-radius: 8px; cursor: pointer; font-size: 14px; transition: all 0.3s; }
.lang-btn:hover { background: rgba(199,165,93,0.15); border-color: #c7a55d; }
.lang-btn.active { background: linear-gradient(135deg, #c7a55d, #a08040); color: #0a0e27; border-color: #c7a55d; font-weight: bold; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; padding: 8px; }
.word-card { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 16px; text-align: center; transition: all 0.3s; cursor: pointer; }
.word-card:hover { transform: translateY(-3px); border-color: #c7a55d; box-shadow: 0 4px 20px rgba(199,165,93,0.2); }
.word-emoji { font-size: 36px; margin-bottom: 8px; }
.word-target { font-size: 18px; font-weight: bold; color: #c7a55d; }
.word-tr { font-size: 13px; color: #8888aa; margin-top: 4px; }
.tts-btn { background: linear-gradient(135deg, #c7a55d, #a08040); border: none; color: #0a0e27; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; margin-top: 6px; }
.tts-btn:hover { opacity: 0.85; }
.topic-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; padding: 8px; }
.topic-btn { padding: 6px 14px; border: 1px solid rgba(199,165,93,0.3); background: rgba(20,24,82,0.5); color: #c7a55d; border-radius: 20px; cursor: pointer; font-size: 13px; transition: all 0.3s; }
.topic-btn.active { background: rgba(199,165,93,0.2); border-color: #c7a55d; }
.section-title { font-size: 18px; color: #c7a55d; padding: 10px 16px; border-bottom: 2px solid rgba(199,165,93,0.3); margin-bottom: 12px; }
.grammar-box { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.grammar-rule { background: rgba(199,165,93,0.1); padding: 10px; border-radius: 8px; border-left: 3px solid #c7a55d; margin-bottom: 10px; color: #c7a55d; font-weight: bold; }
.example-line { padding: 6px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; }
.exercise-box { background: rgba(20,24,82,0.5); border: 1px solid rgba(199,165,93,0.2); border-radius: 8px; padding: 12px; margin: 6px 0; }
.exercise-input { background: rgba(10,14,39,0.8); border: 1px solid rgba(199,165,93,0.3); color: #e0e0e0; padding: 6px 10px; border-radius: 6px; font-size: 14px; width: 120px; }
.check-btn { background: linear-gradient(135deg, #c7a55d, #a08040); border: none; color: #0a0e27; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-left: 8px; }
.check-btn:hover { opacity: 0.85; }
.result-ok { color: #4ade80; font-weight: bold; }
.result-fail { color: #f87171; font-weight: bold; }
.dlg-line { display: flex; gap: 10px; padding: 8px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); align-items: center; }
.dlg-speaker { background: linear-gradient(135deg, #c7a55d, #a08040); color: #0a0e27; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; min-width: 60px; text-align: center; }
.reading-text { background: rgba(20,24,82,0.5); border: 1px solid rgba(199,165,93,0.2); border-radius: 12px; padding: 16px; line-height: 1.8; font-size: 15px; margin-bottom: 12px; }
.quiz-q { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 14px; margin-bottom: 10px; }
.quiz-q-text { font-size: 15px; margin-bottom: 8px; color: #e0e0e0; }
.quiz-opt { display: block; padding: 6px 12px; margin: 4px 0; border: 1px solid rgba(199,165,93,0.2); border-radius: 8px; cursor: pointer; transition: all 0.2s; font-size: 14px; color: #c0c0c0; }
.quiz-opt:hover { border-color: #c7a55d; background: rgba(199,165,93,0.1); }
.quiz-opt.selected { border-color: #c7a55d; background: rgba(199,165,93,0.15); color: #c7a55d; }
.quiz-opt.correct { border-color: #4ade80; background: rgba(74,222,128,0.1); color: #4ade80; }
.quiz-opt.wrong { border-color: #f87171; background: rgba(248,113,113,0.1); color: #f87171; }
.quiz-score { text-align: center; padding: 16px; font-size: 20px; color: #c7a55d; }
.tf-btns { display: flex; gap: 8px; margin-top: 6px; }
.tf-btn { padding: 6px 16px; border: 1px solid rgba(199,165,93,0.3); background: rgba(20,24,82,0.5); color: #c7a55d; border-radius: 8px; cursor: pointer; }
.listening-area { background: rgba(20,24,82,0.5); border: 1px solid rgba(199,165,93,0.2); border-radius: 12px; padding: 16px; text-align: center; }
.play-btn { background: linear-gradient(135deg, #c7a55d, #a08040); border: none; color: #0a0e27; padding: 10px 24px; border-radius: 10px; cursor: pointer; font-size: 16px; font-weight: bold; margin: 10px; }
.play-btn:hover { opacity: 0.85; }
.hint-text { color: #8888aa; font-size: 12px; font-style: italic; }
</style>
"""

# ── HTML BUILDER HELPERS ─────────────────────────────────────────────────────

def _base_js():
    """Shared JS for TTS and language switching."""
    return """
<script>
let currentLang = 'en';
const langCodes = {en:'en-US', de:'de-DE', fr:'fr-FR', it:'it-IT', es:'es-ES'};

function setLang(lang) {
    currentLang = lang;
    document.querySelectorAll('.lang-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.lang === lang);
    });
    // Update visible content
    document.querySelectorAll('[data-lang-content]').forEach(el => {
        const data = JSON.parse(el.dataset.langContent);
        el.textContent = data[currentLang] || data['en'] || '';
    });
}

function speak(text, lang) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = langCodes[lang || currentLang] || 'en-US';
    u.rate = 0.85;
    window.speechSynthesis.speak(u);
}

function speakFromEl(el) {
    const data = JSON.parse(el.dataset.langContent);
    speak(data[currentLang] || data['en'], currentLang);
}
</script>
"""

def _lang_bar_html():
    """Language selector bar."""
    btns = ""
    for key, cfg in _LANG_CONFIG.items():
        active = " active" if key == "en" else ""
        btns += f'<button class="lang-btn{active}" data-lang="{key}" onclick="setLang(\'{key}\')">{cfg["label"]}</button>'
    return f'<div class="lang-bar">{btns}</div>'


def _build_vocab_html(data):
    """Build vocabulary flashcard HTML."""
    topics = data.get("vocab", [])
    if not topics:
        return "<p>Icerik hazirlaniyor...</p>"

    topics_json = json.dumps(topics, ensure_ascii=False)

    return _DIAMOND_CSS + _lang_bar_html() + f"""
<div id="vocab-app">
    <div class="topic-bar" id="topic-bar"></div>
    <div class="card-grid" id="card-grid"></div>
</div>
{_base_js()}
<script>
const vocabTopics = {topics_json};
let currentTopic = 0;

function renderTopics() {{
    const bar = document.getElementById('topic-bar');
    bar.innerHTML = vocabTopics.map((t, i) =>
        '<button class="topic-btn' + (i===currentTopic?' active':'') + '" onclick="selectTopic('+i+')">' + (t.emoji||'') + ' ' + t.topic + '</button>'
    ).join('');
}}

function selectTopic(i) {{
    currentTopic = i;
    renderTopics();
    renderCards();
}}

function renderCards() {{
    const grid = document.getElementById('card-grid');
    const words = vocabTopics[currentTopic].words;
    grid.innerHTML = words.map((w, i) => {{
        const langData = JSON.stringify({{en:w.en, de:w.de, fr:w.fr, it:w.it, es:w.es}});
        return '<div class="word-card" onclick="speak(this.querySelector(\\'.word-target\\').textContent, currentLang)">' +
            '<div class="word-emoji">' + (w.img||'') + '</div>' +
            '<div class="word-target" data-lang-content=\\'' + langData.replace(/'/g,"&#39;") + '\\'>' + w.en + '</div>' +
            '<div class="word-tr">' + w.tr + '</div>' +
            '<button class="tts-btn" onclick="event.stopPropagation(); const d=' + JSON.stringify(langData).replace(/"/g,"&quot;") + '; const p=JSON.parse(d); speak(p[currentLang],currentLang);">&#128266; Dinle</button>' +
            '</div>';
    }}).join('');
    // update for current lang
    setLang(currentLang);
}}

renderTopics();
renderCards();
</script>
"""


def _build_grammar_html(data):
    """Build grammar exercises HTML."""
    items = data.get("grammar", [])
    if not items:
        return "<p>Icerik hazirlaniyor...</p>"

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    for gi, g in enumerate(items):
        examples_html = ""
        for ex in g.get("examples", []):
            lang_data = json.dumps({k: ex.get(k, "") for k in ["en","de","fr","it","es"]}, ensure_ascii=False).replace("'", "&#39;")
            examples_html += f"""<div class="example-line">
                <span data-lang-content='{lang_data}'>{ex.get('en','')}</span>
                <span class="word-tr" style="margin-left:8px;">({ex.get('tr','')})</span>
                <button class="tts-btn" onclick="var d=JSON.parse(this.previousElementSibling.previousElementSibling.dataset.langContent); speak(d[currentLang],currentLang);">&#128266;</button>
            </div>"""

        exercises_html = ""
        for ei, ex in enumerate(g.get("exercises", [])):
            eid = f"g{gi}e{ei}"
            exercises_html += f"""<div class="exercise-box">
                <span>{ex['prompt']}</span><br>
                <input type="text" class="exercise-input" id="inp_{eid}" placeholder="...">
                <button class="check-btn" onclick="checkGrammar('{eid}','{ex['answer']}')">Kontrol</button>
                <span id="res_{eid}"></span>
                <span class="hint-text">({ex.get('hint','')})</span>
            </div>"""

        html_parts.append(f"""
        <div class="grammar-box">
            <div class="section-title">{g['title']}</div>
            <div class="grammar-rule">{g.get('rule_tr','')}</div>
            {examples_html}
            <div style="margin-top:12px;"><b style="color:#c7a55d;">Aliştırma:</b></div>
            {exercises_html}
        </div>""")

    html_parts.append(_base_js())
    html_parts.append("""<script>
function checkGrammar(id, answer) {
    const inp = document.getElementById('inp_'+id);
    const res = document.getElementById('res_'+id);
    if (inp.value.trim().toLowerCase() === answer.toLowerCase()) {
        res.innerHTML = '<span class="result-ok">✓ Dogru!</span>';
    } else {
        res.innerHTML = '<span class="result-fail">✗ Yanlis. Dogru: ' + answer + '</span>';
    }
}
</script>""")

    return "\n".join(html_parts)


def _build_dialogue_html(data):
    """Build dialogue practice HTML."""
    dialogues = data.get("dialogues", [])
    if not dialogues:
        return "<p>Icerik hazirlaniyor...</p>"

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    for d in dialogues:
        lines_html = ""
        for line in d.get("lines", []):
            lang_data = json.dumps({k: line.get(k, "") for k in ["en","de","fr","it","es"]}, ensure_ascii=False).replace("'", "&#39;")
            lines_html += f"""<div class="dlg-line">
                <span class="dlg-speaker">{line['speaker']}</span>
                <span data-lang-content='{lang_data}'>{line.get('en','')}</span>
                <span class="word-tr">({line.get('tr','')})</span>
                <button class="tts-btn" onclick="var d=JSON.parse(this.parentElement.querySelector('[data-lang-content]').dataset.langContent); speak(d[currentLang],currentLang);">&#128266;</button>
            </div>"""

        html_parts.append(f"""
        <div class="grammar-box">
            <div class="section-title">{d['title']}</div>
            {lines_html}
            <div style="text-align:center;margin-top:10px;">
                <button class="play-btn" onclick="playAllLines(this.parentElement.parentElement)">&#9654; Tum Diyalogu Dinle</button>
            </div>
        </div>""")

    html_parts.append(_base_js())
    html_parts.append("""<script>
function playAllLines(box) {
    const lines = box.querySelectorAll('[data-lang-content]');
    let i = 0;
    function next() {
        if (i >= lines.length) return;
        const data = JSON.parse(lines[i].dataset.langContent);
        const text = data[currentLang] || data['en'];
        const u = new SpeechSynthesisUtterance(text);
        u.lang = langCodes[currentLang] || 'en-US';
        u.rate = 0.8;
        u.onend = () => { i++; setTimeout(next, 400); };
        lines[i].style.background = 'rgba(199,165,93,0.15)';
        setTimeout(() => { lines[i-1] && (lines[i-1].style.background = ''); }, 2000);
        window.speechSynthesis.speak(u);
        i++;
    }
    window.speechSynthesis.cancel();
    i = 0;
    next();
}
</script>""")

    return "\n".join(html_parts)


def _build_reading_html(data):
    """Build reading comprehension HTML."""
    readings = data.get("reading", [])
    if not readings:
        return "<p>Icerik hazirlaniyor...</p>"

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    for ri, r in enumerate(readings):
        text_data = json.dumps(r.get("text", {}), ensure_ascii=False).replace("'", "&#39;")

        questions_html = ""
        for qi, q in enumerate(r.get("questions", [])):
            opts_html = ""
            for oi, opt in enumerate(q["options"]):
                qid = f"r{ri}q{qi}"
                opts_html += f'<label class="quiz-opt" onclick="selectReadingOpt(\'{qid}\',{oi},{q["answer"]},this)">{opt}</label>'
            questions_html += f"""<div class="quiz-q">
                <div class="quiz-q-text">{qi+1}. {q['q_tr']}</div>
                {opts_html}
                <div id="rres_{qid}" style="margin-top:6px;"></div>
            </div>"""

        html_parts.append(f"""
        <div class="grammar-box">
            <div class="section-title">{r['title']}</div>
            <div class="reading-text" data-lang-content='{text_data}'>{r['text'].get('en','')}</div>
            <button class="tts-btn" style="margin-bottom:10px;" onclick="var d=JSON.parse(document.querySelector('.reading-text').dataset.langContent); speak(d[currentLang],currentLang);">&#128266; Metni Dinle</button>
            <div style="color:#c7a55d;font-weight:bold;margin:8px 0;">Anlama Sorulari:</div>
            {questions_html}
        </div>""")

    html_parts.append(_base_js())
    html_parts.append("""<script>
function selectReadingOpt(qid, idx, correct, el) {
    const parent = el.parentElement;
    parent.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected','correct','wrong'));
    if (idx === correct) {
        el.classList.add('correct');
        document.getElementById('rres_'+qid).innerHTML = '<span class="result-ok">Dogru!</span>';
    } else {
        el.classList.add('wrong');
        document.getElementById('rres_'+qid).innerHTML = '<span class="result-fail">Yanlis!</span>';
        parent.querySelectorAll('.quiz-opt')[correct].classList.add('correct');
    }
}
</script>""")

    return "\n".join(html_parts)


def _build_listening_html(data):
    """Build listening exercises HTML using TTS."""
    readings = data.get("reading", [])
    quiz_items = data.get("quiz", [])
    if not readings and not quiz_items:
        return "<p>Icerik hazirlaniyor...</p>"

    # Use reading texts as listening material + quiz questions as listening quiz
    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    for ri, r in enumerate(readings):
        text_data = json.dumps(r.get("text", {}), ensure_ascii=False).replace("'", "&#39;")
        questions_html = ""
        for qi, q in enumerate(r.get("questions", [])):
            opts_html = ""
            for oi, opt in enumerate(q["options"]):
                lid = f"l{ri}q{qi}"
                opts_html += f'<label class="quiz-opt" onclick="selectReadingOpt(\'{lid}\',{oi},{q["answer"]},this)">{opt}</label>'
            questions_html += f"""<div class="quiz-q">
                <div class="quiz-q-text">{qi+1}. {q['q_tr']}</div>
                {opts_html}
                <div id="rres_{lid}" style="margin-top:6px;"></div>
            </div>"""

        html_parts.append(f"""
        <div class="listening-area" style="margin-bottom:16px;">
            <div class="section-title">&#127911; Dinleme: {r['title']}</div>
            <p style="color:#8888aa; margin:8px 0;">Metni dinleyin ve sorulari cevaplayin.</p>
            <button class="play-btn" onclick="var d=JSON.parse('{text_data.replace(chr(39),"&#39;")}'); speak(d[currentLang],currentLang);">&#9654; Dinle</button>
            <button class="play-btn" style="background:rgba(199,165,93,0.3);color:#c7a55d;" onclick="var d=JSON.parse('{text_data.replace(chr(39),"&#39;")}'); speakSlow(d[currentLang],currentLang);">&#128034; Yavas Dinle</button>
        </div>
        {questions_html}
        """)

    html_parts.append(_base_js())
    html_parts.append("""<script>
function speakSlow(text, lang) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = langCodes[lang || currentLang] || 'en-US';
    u.rate = 0.55;
    window.speechSynthesis.speak(u);
}
function selectReadingOpt(qid, idx, correct, el) {
    const parent = el.parentElement;
    parent.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected','correct','wrong'));
    if (idx === correct) {
        el.classList.add('correct');
        document.getElementById('rres_'+qid).innerHTML = '<span class="result-ok">Dogru!</span>';
    } else {
        el.classList.add('wrong');
        document.getElementById('rres_'+qid).innerHTML = '<span class="result-fail">Yanlis!</span>';
        parent.querySelectorAll('.quiz-opt')[correct].classList.add('correct');
    }
}
</script>""")

    return "\n".join(html_parts)


def _build_quiz_html(data):
    """Build mini quiz HTML."""
    questions = data.get("quiz", [])
    if not questions:
        return "<p>Icerik hazirlaniyor...</p>"

    q_json = json.dumps(questions, ensure_ascii=False)

    return _DIAMOND_CSS + f"""
<div id="quiz-container"></div>
<div id="quiz-score" class="quiz-score" style="display:none;"></div>
<div style="text-align:center;margin-top:10px;">
    <button class="play-btn" id="quiz-submit" onclick="submitQuiz()">Sinavi Bitir</button>
    <button class="play-btn" id="quiz-restart" style="display:none;background:rgba(199,165,93,0.3);color:#c7a55d;" onclick="startQuiz()">Tekrar Dene</button>
</div>
""" + _base_js() + f"""
<script>
const quizData = {q_json};
let quizAnswers = {{}};

function startQuiz() {{
    quizAnswers = {{}};
    document.getElementById('quiz-score').style.display = 'none';
    document.getElementById('quiz-submit').style.display = '';
    document.getElementById('quiz-restart').style.display = 'none';
    const container = document.getElementById('quiz-container');
    container.innerHTML = quizData.map((q, i) => {{
        if (q.type === 'mc') {{
            const opts = q.options.map((o, oi) =>
                '<label class="quiz-opt" onclick="quizSelect('+i+','+oi+',this)">'+String.fromCharCode(65+oi)+') '+o+'</label>'
            ).join('');
            return '<div class="quiz-q"><div class="quiz-q-text">'+(i+1)+'. '+q.q_tr+'</div>'+opts+'</div>';
        }} else {{
            return '<div class="quiz-q"><div class="quiz-q-text">'+(i+1)+'. '+q.q_tr+'</div>' +
                '<div class="tf-btns">' +
                '<button class="tf-btn" onclick="quizSelectTF('+i+',true,this)">Dogru</button>' +
                '<button class="tf-btn" onclick="quizSelectTF('+i+',false,this)">Yanlis</button>' +
                '</div></div>';
        }}
    }}).join('');
}}

function quizSelect(qi, oi, el) {{
    quizAnswers[qi] = oi;
    el.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
}}

function quizSelectTF(qi, val, el) {{
    quizAnswers[qi] = val;
    el.parentElement.querySelectorAll('.tf-btn').forEach(b => b.style.borderColor = 'rgba(199,165,93,0.3)');
    el.style.borderColor = '#c7a55d';
}}

function submitQuiz() {{
    let score = 0;
    quizData.forEach((q, i) => {{
        const userAns = quizAnswers[i];
        let correct;
        if (q.type === 'mc') {{
            correct = userAns === q.answer;
        }} else {{
            correct = userAns === q.answer;
        }}
        if (correct) score++;
        // Mark answers
        const qDiv = document.querySelectorAll('.quiz-q')[i];
        if (q.type === 'mc') {{
            qDiv.querySelectorAll('.quiz-opt').forEach((o, oi) => {{
                if (oi === q.answer) o.classList.add('correct');
                else if (oi === userAns && !correct) o.classList.add('wrong');
            }});
        }} else {{
            const btns = qDiv.querySelectorAll('.tf-btn');
            btns.forEach(b => {{
                const bval = b.textContent === 'Dogru';
                if (bval === q.answer) b.style.borderColor = '#4ade80';
                else if (bval === userAns && !correct) b.style.borderColor = '#f87171';
            }});
        }}
    }});
    const pct = Math.round(score / quizData.length * 100);
    document.getElementById('quiz-score').innerHTML =
        '&#127942; Sonuc: <b>' + score + '/' + quizData.length + '</b> (%' + pct + ')' +
        (pct >= 80 ? ' - Harika!' : pct >= 50 ? ' - Iyi, biraz daha calis!' : ' - Tekrar dene!');
    document.getElementById('quiz-score').style.display = '';
    document.getElementById('quiz-submit').style.display = 'none';
    document.getElementById('quiz-restart').style.display = '';
}}

startQuiz();
</script>
"""


# ── MAIN RENDER FUNCTION ────────────────────────────────────────────────────

def render_interaktif_calisma(level: str, key_prefix: str):
    """Render interactive exercises for the given CEFR level.
    level: 'preschool', 'grade1', ..., 'grade12'
    key_prefix: unique key prefix for Streamlit widgets
    """
    group = _LEVEL_GROUP.get(level, "grade1_2")
    data = LEVEL_DATA.get(group)
    if not data:
        # Fallback to closest available
        data = LEVEL_DATA.get("grade1_2", {})

    label = data.get("label", _LEVEL_LABELS.get(group, level))
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0d1137,#141852);padding:10px 16px;'
        f'border-radius:10px;border:1px solid rgba(199,165,93,0.3);margin-bottom:10px;">'
        f'<span style="color:#c7a55d;font-size:16px;font-weight:bold;">'
        f'\U0001f4da Interaktif Calisma - {label}</span></div>',
        unsafe_allow_html=True,
    )

    try:
        from views._kdg_games import (
            build_games_html,
            build_enhanced_grammar_html,
            build_enhanced_dialogue_html,
            build_enhanced_listening_html,
            build_enhanced_quiz_html,
        )
    except ImportError:
        # Fallback to local builders
        build_enhanced_grammar_html = _build_grammar_html
        build_enhanced_dialogue_html = _build_dialogue_html
        build_enhanced_listening_html = _build_listening_html
        build_games_html = lambda data: _build_quiz_html(data)
        build_enhanced_quiz_html = _build_quiz_html

    tab_names = [
        "  \U0001f4d6 Kelime Ogren  ",
        "  \U0001f4dd Gramer  ",
        "  \U0001f4ac Diyalog  ",
        "  \U0001f4d6 Okuma  ",
        "  \U0001f3a7 Dinleme  ",
        "  \U0001f3ae Oyunlar  ",
        "  \U0001f3af Mini Sinav  ",
    ]

    tabs = st.tabs(tab_names)

    with tabs[0]:  # Kelime Ogren
        html = _build_vocab_html(data)
        components.html(html, height=650, scrolling=True)

    with tabs[1]:  # Gramer (Enhanced)
        html = build_enhanced_grammar_html(data)
        components.html(html, height=900, scrolling=True)

    with tabs[2]:  # Diyalog (Enhanced)
        html = build_enhanced_dialogue_html(data)
        components.html(html, height=800, scrolling=True)

    with tabs[3]:  # Okuma
        html = _build_reading_html(data)
        components.html(html, height=650, scrolling=True)

    with tabs[4]:  # Dinleme (Enhanced)
        html = build_enhanced_listening_html(data)
        components.html(html, height=850, scrolling=True)

    with tabs[5]:  # Oyunlar (NEW)
        html = build_games_html(data)
        components.html(html, height=900, scrolling=True)

    with tabs[6]:  # Mini Sinav (Enhanced)
        html = build_enhanced_quiz_html(data)
        components.html(html, height=850, scrolling=True)
