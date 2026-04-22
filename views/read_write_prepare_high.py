# -*- coding: utf-8 -*-
"""Read, Write & Prepare — Lise (9-12) Reading + Writing + Exam Practice Kitabı.

Interactive HTML pages for high school advanced reading, writing & exam prep.
Activity types (5 pages per week):
  1. Reading Passage & Analysis (Kısa/uzun parça + analiz + yorum soruları)
  2. Writing Workshop (Opinion, E-mail, Summary writing + rubrikler)
  3. Note Taking & Outlining (Not alma + ana fikir çıkarma + organize etme)
  4. Exam Practice (Sınav formatlı sorular — MCQ + open-ended + cloze)
  5. Full Review Test (Genel tekrar — Reading + Writing + Grammar karma)

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
    9:  {"label": "9th Grade", "cefr": "B1", "font_size": "15px",
         "passage_para": 2, "analysis_q": 5, "writing_tasks": 2,
         "note_items": 5, "exam_q": 10, "review_q": 12,
         "color_primary": "#5C6BC0", "color_accent": "#3949AB", "color_bg": "#E8EAF6"},
    10: {"label": "10th Grade", "cefr": "B1+", "font_size": "15px",
         "passage_para": 3, "analysis_q": 6, "writing_tasks": 2,
         "note_items": 6, "exam_q": 12, "review_q": 14,
         "color_primary": "#26A69A", "color_accent": "#00897B", "color_bg": "#E0F2F1"},
    11: {"label": "11th Grade", "cefr": "B2", "font_size": "14px",
         "passage_para": 3, "analysis_q": 7, "writing_tasks": 3,
         "note_items": 7, "exam_q": 14, "review_q": 16,
         "color_primary": "#EF5350", "color_accent": "#C62828", "color_bg": "#FFEBEE"},
    12: {"label": "12th Grade", "cefr": "B2+", "font_size": "14px",
         "passage_para": 4, "analysis_q": 8, "writing_tasks": 3,
         "note_items": 8, "exam_q": 16, "review_q": 18,
         "color_primary": "#7E57C2", "color_accent": "#4527A0", "color_bg": "#EDE7F6"},
}

# ══════════════════════════════════════════════════════════════════════════════
# READING PASSAGES (advanced topics)
# ══════════════════════════════════════════════════════════════════════════════

_PASSAGES = [
    {"title": "The Impact of Social Media on Modern Communication",
     "emoji": "📱", "category": "technology",
     "paragraphs": [
         "Social media has fundamentally transformed the way people communicate in the 21st century. Platforms such as Instagram, Twitter, and TikTok have created new forms of expression that were unimaginable just two decades ago. These digital tools allow users to share ideas, images, and videos with millions of people in real time, breaking down geographical barriers that once limited human interaction.",
         "However, this transformation has not come without significant concerns. Critics argue that social media encourages superficial connections at the expense of deeper, more meaningful relationships. Studies have shown that excessive social media use is correlated with increased feelings of loneliness, anxiety, and depression, particularly among teenagers and young adults.",
         "On the other hand, supporters of social media point to its role in democratizing information and giving voice to marginalized communities. Social movements such as climate activism and human rights campaigns have gained unprecedented momentum through viral social media content.",
         "The challenge for modern society lies in finding a balance between leveraging the benefits of digital communication while mitigating its potential harm. Media literacy education, screen time management, and thoughtful content consumption are essential skills for navigating this new landscape.",
     ]},
    {"title": "Artificial Intelligence: Promise and Peril",
     "emoji": "🤖", "category": "technology",
     "paragraphs": [
         "Artificial intelligence has emerged as one of the most transformative technologies of our era. From self-driving cars to medical diagnosis systems, AI applications are reshaping industries and challenging our understanding of what machines can accomplish. The rapid advancement of machine learning algorithms has accelerated this transformation beyond what many experts predicted.",
         "In healthcare, AI systems can now detect certain diseases with accuracy comparable to or exceeding that of human doctors. In education, adaptive learning platforms use AI to personalize instruction for individual students. These developments suggest a future where AI augments human capabilities rather than replacing them entirely.",
         "Nevertheless, the rise of AI raises profound ethical questions. Concerns about algorithmic bias, job displacement, and the concentration of power in technology companies have sparked intense debate among policymakers, academics, and the general public.",
         "As AI continues to evolve, the need for comprehensive regulatory frameworks becomes increasingly urgent. Societies must develop policies that encourage innovation while protecting fundamental human rights and ensuring that the benefits of AI are distributed equitably.",
     ]},
    {"title": "Climate Change: A Global Challenge",
     "emoji": "🌍", "category": "environment",
     "paragraphs": [
         "Climate change represents the most pressing environmental challenge of our time. Scientific evidence overwhelmingly demonstrates that human activities, particularly the burning of fossil fuels and deforestation, have led to a significant increase in global temperatures over the past century.",
         "The consequences of climate change are already visible across the globe. Rising sea levels threaten coastal communities, extreme weather events are becoming more frequent and severe, and biodiversity loss is accelerating at an alarming rate. These changes disproportionately affect developing nations, which often lack the resources to adapt.",
         "International efforts to combat climate change, such as the Paris Agreement, have set ambitious targets for reducing greenhouse gas emissions. However, progress toward these goals has been uneven, with many countries struggling to balance economic growth with environmental sustainability.",
         "Individual actions, while important, cannot solve the climate crisis alone. Systemic changes in energy production, transportation, agriculture, and industrial processes are necessary to achieve meaningful reductions in carbon emissions and secure a livable planet for future generations.",
     ]},
    {"title": "The Psychology of Decision Making",
     "emoji": "🧠", "category": "psychology",
     "paragraphs": [
         "Every day, humans make thousands of decisions, from trivial choices about what to eat to life-altering determinations about careers and relationships. Psychologists have long studied the cognitive processes underlying decision making, revealing that our choices are often influenced by factors we are not consciously aware of.",
         "Daniel Kahneman, a Nobel Prize-winning psychologist, proposed that human thinking operates through two systems: System 1, which is fast, automatic, and intuitive, and System 2, which is slow, deliberate, and analytical. Most of our daily decisions are made by System 1, which relies on mental shortcuts called heuristics.",
         "While heuristics are generally efficient, they can lead to systematic errors in judgment known as cognitive biases. Confirmation bias, for example, causes people to seek information that supports their existing beliefs while ignoring contradictory evidence. The anchoring effect causes people to rely too heavily on the first piece of information they encounter.",
         "Understanding these psychological mechanisms can help individuals make better decisions. Strategies such as considering multiple perspectives, seeking diverse opinions, and deliberately slowing down the decision-making process can counteract the influence of cognitive biases.",
     ]},
    {"title": "The Future of Work in a Digital Age",
     "emoji": "💼", "category": "economics",
     "paragraphs": [
         "The nature of work is undergoing a profound transformation driven by technological innovation, globalization, and shifting demographic patterns. Remote work, once considered a luxury, has become a mainstream option for millions of workers worldwide, fundamentally altering the relationship between employers and employees.",
         "Automation and artificial intelligence are expected to eliminate certain types of jobs while creating entirely new categories of employment. According to the World Economic Forum, by 2030, up to 85 million jobs may be displaced by automation, but 97 million new roles may emerge that are better adapted to the new division of labor between humans, machines, and algorithms.",
         "The gig economy, characterized by short-term contracts and freelance work, has grown significantly in recent years. While this model offers flexibility and autonomy, it also raises concerns about job security, benefits, and workers' rights.",
         "Preparing for the future of work requires a fundamental rethinking of education and training systems. Lifelong learning, adaptability, and digital literacy are becoming essential skills, and educational institutions must evolve to equip students with the competencies needed in a rapidly changing labor market.",
     ]},
]

# ══════════════════════════════════════════════════════════════════════════════
# WRITING TASK TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

_WRITING_TASKS = {
    "opinion": [
        {"prompt": "Do you think social media does more harm than good? Write an opinion essay (150-200 words) supporting your view with at least two reasons.",
         "structure": ["Introduction (state your opinion)", "Reason 1 + example", "Reason 2 + example", "Conclusion (restate opinion)"],
         "useful_phrases": ["In my opinion,", "I strongly believe that", "First of all,", "Furthermore,", "To conclude,", "For instance,"],
         "rubric": {"content": 5, "organization": 5, "language": 5, "mechanics": 5}},
        {"prompt": "Should students be allowed to use smartphones in school? Write a well-organized opinion essay (150-200 words).",
         "structure": ["Introduction with thesis", "Argument 1 + support", "Argument 2 + support", "Counter-argument + refutation", "Conclusion"],
         "useful_phrases": ["From my perspective,", "One significant reason is", "Additionally,", "Some may argue that", "However,", "In conclusion,"],
         "rubric": {"content": 5, "organization": 5, "language": 5, "mechanics": 5}},
        {"prompt": "Is it better to learn from books or from experience? Share your opinion in a structured essay (150-200 words).",
         "structure": ["Hook + thesis statement", "Body paragraph 1", "Body paragraph 2", "Conclusion"],
         "useful_phrases": ["It is widely debated whether", "I firmly believe", "On the one hand,", "On the other hand,", "All things considered,"],
         "rubric": {"content": 5, "organization": 5, "language": 5, "mechanics": 5}},
    ],
    "email": [
        {"prompt": "Write a formal e-mail to your school principal requesting permission to organize a cultural event. Include the date, purpose, and expected participants (120-150 words).",
         "structure": ["Subject line", "Greeting (Dear Mr./Ms. ...)", "Purpose of writing", "Details (date, time, participants)", "Closing request", "Formal sign-off"],
         "useful_phrases": ["I am writing to request", "I would like to propose", "The event is scheduled for", "I would be grateful if", "I look forward to hearing from you", "Yours sincerely,"],
         "rubric": {"format": 5, "content": 5, "tone": 5, "language": 5}},
        {"prompt": "Write an e-mail to a friend describing your plans for the summer holiday. Mention at least three activities (120-150 words).",
         "structure": ["Informal greeting", "Opening (How are you?)", "Main content (plans)", "Invitation or question", "Informal closing"],
         "useful_phrases": ["Hey! How's it going?", "I'm so excited because", "I'm planning to", "Would you like to join?", "Can't wait!", "Take care,"],
         "rubric": {"format": 5, "content": 5, "tone": 5, "language": 5}},
    ],
    "summary": [
        {"prompt": "Read the passage above and write a summary in 80-100 words. Include only the main ideas — do not add your personal opinion.",
         "structure": ["Opening sentence (topic + source)", "Main idea 1", "Main idea 2", "Concluding sentence"],
         "useful_phrases": ["The passage discusses", "According to the text,", "The author argues that", "In addition,", "Overall, the text highlights"],
         "rubric": {"accuracy": 5, "conciseness": 5, "paraphrasing": 5, "coherence": 5}},
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# EXAM-STYLE QUESTION POOLS
# ══════════════════════════════════════════════════════════════════════════════

_CLOZE_PASSAGES = [
    {"text": "Education is widely recognized as one of the most _1_ factors in personal and societal development. It not only provides individuals with knowledge and skills _2_ also shapes their values and perspectives. _3_, access to quality education remains unequal across the globe. Many children in developing countries _4_ attend school due to poverty, conflict, or lack of infrastructure. Addressing this _5_ requires coordinated efforts from governments, organizations, and communities.",
     "gaps": {
         "1": {"correct": "important", "options": ["important", "dangerous", "expensive"]},
         "2": {"correct": "but", "options": ["but", "so", "or"]},
         "3": {"correct": "However", "options": ["However", "Therefore", "Similarly"]},
         "4": {"correct": "cannot", "options": ["cannot", "must", "should"]},
         "5": {"correct": "challenge", "options": ["challenge", "solution", "celebration"]},
     }},
    {"text": "The rapid growth of technology has _1_ transformed the business world. Companies that fail to _2_ to digital innovations risk falling behind their competitors. E-commerce, for _3_, has revolutionized the retail industry by allowing consumers to purchase products from _4_ in the world. Meanwhile, data analytics enables businesses to make more _5_ decisions based on consumer behavior patterns.",
     "gaps": {
         "1": {"correct": "significantly", "options": ["significantly", "accidentally", "reluctantly"]},
         "2": {"correct": "adapt", "options": ["adapt", "object", "surrender"]},
         "3": {"correct": "instance", "options": ["instance", "conclusion", "comparison"]},
         "4": {"correct": "anywhere", "options": ["anywhere", "nowhere", "somewhere"]},
         "5": {"correct": "informed", "options": ["informed", "confused", "random"]},
     }},
]

_GRAMMAR_EXAM_QS = [
    ("If I ___ more time, I would travel the world.", "had", ["have", "will have"]),
    ("The report ___ by the committee last week.", "was submitted", ["submitted", "is submitted"]),
    ("She asked me where I ___ the previous day.", "had been", ["have been", "was being"]),
    ("Not only ___ intelligent, but she is also hardworking.", "is she", ["she is", "does she"]),
    ("By the time we arrived, the concert ___.", "had already started", ["already started", "has started"]),
    ("The scientist ___ research on this topic for ten years.", "has been conducting", ["is conducting", "conducts"]),
    ("___ the weather was terrible, we decided to go hiking.", "Although", ["Because", "Since"]),
    ("The project, ___ was due last Friday, has been postponed.", "which", ["what", "who"]),
    ("I wish I ___ a musical instrument when I was younger.", "had learned", ["learned", "would learn"]),
    ("He suggested that she ___ the meeting.", "attend", ["attends", "attended"]),
    ("The more you practice, the ___ you will become.", "better", ["best", "good"]),
    ("Neither the teacher ___ the students were aware of the change.", "nor", ["or", "and"]),
    ("Had I known about the delay, I ___ left earlier.", "would have", ["will have", "had"]),
    ("The book is worth ___.", "reading", ["to read", "read"]),
    ("She is used to ___ up early for school.", "getting", ["get", "got"]),
    ("It's high time we ___ about the environment.", "thought", ["think", "thinking"]),
]

_VOCAB_EXAM_QS = [
    ("The government needs to ___ new policies to address climate change.", "implement", ["ignore", "abandon"]),
    ("Scientists have ___ a strong link between diet and health.", "established", ["demolished", "forgotten"]),
    ("The ___ of the experiment surprised everyone.", "outcome", ["entrance", "departure"]),
    ("She made a ___ contribution to the research project.", "significant", ["negligible", "invisible"]),
    ("The article provides a ___ analysis of the current situation.", "comprehensive", ["superficial", "partial"]),
    ("Students should ___ their time wisely during exams.", "allocate", ["waste", "ignore"]),
    ("The data ___ that the trend is continuing.", "indicates", ["conceals", "contradicts"]),
    ("Critical thinking is ___ for academic success.", "essential", ["optional", "irrelevant"]),
    ("The researcher ___ his findings at the conference.", "presented", ["concealed", "destroyed"]),
    ("We need to ___ the benefits and drawbacks carefully.", "evaluate", ["overlook", "exaggerate"]),
]

_FILL_DATA = {
    "name": ["Alex", "Sarah", "James", "Emily", "David", "Olivia", "Daniel", "Sophie"],
}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"rwp_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _js_safe(t: str) -> str:
    return t.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")


def _base_css(cfg: dict) -> str:
    cp, ca, bg, fs = cfg["color_primary"], cfg["color_accent"], cfg["color_bg"], cfg["font_size"]
    return f"""
    <style>
    /* font: sistem fontu kullaniliyor */
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{font-family:'Inter',sans-serif;background:linear-gradient(135deg,{bg} 0%,#f5f5f5 100%);
    color:#2d3436;font-size:{fs};padding:18px;line-height:1.7;}}
    .page-title{{text-align:center;font-size:1.5em;font-weight:800;
    background:linear-gradient(135deg,{cp},{ca});
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;}}
    .page-sub{{text-align:center;font-size:.8em;color:#6b7280;margin-bottom:16px;}}
    .badge{{display:inline-block;color:#fff;padding:3px 12px;border-radius:18px;
    font-size:.65em;font-weight:700;margin-bottom:8px;}}
    .badge-week{{background:{cp};}} .badge-cefr{{background:{ca};margin-left:4px;}}
    .card{{background:#fff;border-radius:14px;box-shadow:0 3px 12px rgba(0,0,0,.06);
    padding:16px;margin-bottom:14px;border-left:4px solid {cp};transition:transform .2s;}}
    .card:hover{{transform:translateY(-1px);}}
    .card-t{{font-size:1.05em;font-weight:700;color:{cp};margin-bottom:6px;}}
    .para{{padding:10px 14px;margin:6px 0;line-height:1.8;border-radius:10px;
    background:rgba(0,0,0,.015);cursor:pointer;transition:all .2s;border:1px solid transparent;}}
    .para:hover{{background:{bg};border-color:rgba(0,0,0,.06);}}
    .q-box{{background:#fff;border:2px solid {cp};border-radius:12px;padding:14px;margin:10px 0;}}
    .q-num{{display:inline-block;background:{cp};color:#fff;width:26px;height:26px;
    border-radius:50%;text-align:center;line-height:26px;font-size:.75em;font-weight:800;margin-right:5px;}}
    .q-text{{font-weight:700;font-size:.92em;margin-bottom:6px;}}
    .q-type{{display:inline-block;background:{bg};color:{cp};padding:1px 7px;border-radius:6px;
    font-size:.58em;font-weight:700;margin-left:3px;}}
    .opt{{display:block;width:100%;text-align:left;padding:8px 13px;margin:3px 0;
    border:2px solid #e8e8e8;border-radius:10px;background:#fafafa;cursor:pointer;
    font-family:inherit;font-size:.86em;font-weight:600;transition:all .2s;}}
    .opt:hover{{border-color:{cp};background:{bg};}}
    .tf-btn{{display:inline-block;padding:7px 20px;border:2px solid #e0e0e0;border-radius:16px;
    cursor:pointer;font-weight:700;margin:3px 5px;transition:all .2s;font-size:.82em;}}
    .tf-t{{color:#27ae60;}}.tf-t:hover{{border-color:#27ae60;background:#e8f5e9;}}
    .tf-f{{color:#e74c3c;}}.tf-f:hover{{border-color:#e74c3c;background:#fce4ec;}}
    .fb{{margin-top:5px;font-weight:700;display:none;font-size:.82em;}}
    .score-bar{{text-align:center;font-size:1.3em;font-weight:800;color:{cp};margin:12px 0;
    padding:8px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.05);}}
    .prog{{width:100%;height:7px;background:#e0e0e0;border-radius:4px;margin:6px 0;overflow:hidden;}}
    .prog-fill{{height:100%;background:linear-gradient(90deg,{cp},{ca});border-radius:4px;
    transition:width .5s ease;}}
    .section-hdr{{background:linear-gradient(135deg,{cp},{ca});color:#fff;padding:12px 18px;
    border-radius:12px;text-align:center;margin:16px 0 10px;}}
    .section-hdr h3{{margin:0;font-size:1.1em;}} .section-hdr p{{margin:2px 0 0;font-size:.75em;opacity:.9;}}
    .btn{{display:inline-block;padding:8px 18px;border:none;border-radius:20px;cursor:pointer;
    font-family:inherit;font-size:.8em;font-weight:700;color:#fff;transition:all .2s;}}
    .btn-p{{background:linear-gradient(135deg,{cp},{ca});}}
    .btn-p:hover{{transform:scale(1.04);}}
    .btn-s{{background:linear-gradient(135deg,#4FC3F7,#00BCD4);}}
    .btn-s:hover{{transform:scale(1.04);}}
    .writing-area{{width:100%;min-height:140px;padding:12px;border:2px solid #e0e0e0;
    border-radius:12px;font-family:inherit;font-size:.9em;line-height:1.6;resize:vertical;
    transition:border-color .3s;}}
    .writing-area:focus{{outline:none;border-color:{cp};}}
    .rubric-table{{width:100%;border-collapse:collapse;margin:8px 0;font-size:.8em;}}
    .rubric-table th{{background:{cp};color:#fff;padding:6px 10px;text-align:left;}}
    .rubric-table td{{padding:6px 10px;border-bottom:1px solid #eee;}}
    .rubric-table tr:nth-child(even){{background:{bg};}}
    .note-card{{background:#fffde7;border:2px dashed #ffd54f;border-radius:12px;
    padding:14px;margin:8px 0;}}
    .note-line{{display:flex;align-items:flex-start;gap:8px;margin:6px 0;}}
    .note-bullet{{color:{cp};font-weight:800;font-size:1.1em;flex-shrink:0;}}
    .cloze-gap{{display:inline-block;min-width:100px;border-bottom:2px solid {cp};
    text-align:center;font-weight:700;color:{cp};margin:0 2px;padding:2px 4px;}}
    .phrase-chip{{display:inline-block;background:{bg};border:1.5px solid {cp};
    padding:3px 10px;border-radius:14px;margin:2px;font-size:.78em;font-weight:600;
    cursor:pointer;transition:all .2s;}}
    .phrase-chip:hover{{background:{cp};color:#fff;}}
    </style>"""


def _tts_script() -> str:
    return """
    <script>
    function speak(t,r){r=r||0.85;if(!window.speechSynthesis)return;
    window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);
    u.lang='en-US';u.rate=r;u.pitch=1.0;window.speechSynthesis.speak(u);}

    var totalQ=0,correctQ=0;
    function checkOpt(btn,ok,fbId){
        var p=btn.parentElement;
        p.querySelectorAll('.opt').forEach(function(b){b.disabled=true;b.style.opacity='0.4';});
        totalQ++;var fb=document.getElementById(fbId);
        if(ok){btn.style.background='#d4edda';btn.style.borderColor='#27ae60';btn.style.opacity='1';
        correctQ++;if(fb){fb.innerHTML='✅ Correct!';fb.style.color='#27ae60';}}
        else{btn.style.background='#f8d7da';btn.style.borderColor='#e74c3c';btn.style.opacity='1';
        if(fb){fb.innerHTML='❌ Incorrect';fb.style.color='#e74c3c';}}
        if(fb)fb.style.display='block';updateScore();}

    function checkTF(btn,ok,fbId){totalQ++;
        var p=btn.parentElement;
        p.querySelectorAll('.tf-btn').forEach(function(b){b.style.pointerEvents='none';b.style.opacity='0.4';});
        var fb=document.getElementById(fbId);
        if(ok){btn.style.background='#d4edda';btn.style.borderColor='#27ae60';btn.style.opacity='1';
        correctQ++;if(fb){fb.innerHTML='✅';fb.style.color='#27ae60';}}
        else{btn.style.background='#f8d7da';btn.style.borderColor='#e74c3c';btn.style.opacity='1';
        if(fb){fb.innerHTML='❌';fb.style.color='#e74c3c';}}
        if(fb)fb.style.display='block';updateScore();}

    function updateScore(){var el=document.getElementById('scoreDisplay');if(!el)return;
    var pct=totalQ>0?Math.round(correctQ/totalQ*100):0;
    var s=pct>=80?'⭐⭐⭐':pct>=60?'⭐⭐':pct>=40?'⭐':'';
    el.innerHTML='Score: '+correctQ+'/'+totalQ+' ('+pct+'%) '+s;
    var bar=document.getElementById('progFill');if(bar)bar.style.width=pct+'%';}

    function countWords(ta,cntId){var w=ta.value.trim().split(/\\s+/).filter(Boolean).length;
    document.getElementById(cntId).textContent=w+' words';}
    </script>"""


def _mcq(qn, text, correct, wrongs, rng, qtype="detail"):
    opts = [correct] + wrongs[:2]
    rng.shuffle(opts)
    h = ""
    for o in opts:
        c = "true" if o == correct else "false"
        h += f'<button class="opt" onclick="checkOpt(this,{c},\'f{qn}\')">{o}</button>'
    return f'<div class="q-box"><div class="q-text"><span class="q-num">{qn}</span> {text} <span class="q-type">{qtype}</span></div><div>{h}</div><div class="fb" id="f{qn}"></div></div>'


def _tf(qn, stmt, is_true):
    t = "true" if is_true else "false"
    f = "true" if not is_true else "false"
    return f'<div class="q-box"><div class="q-text"><span class="q-num">{qn}</span> True or False? <span class="q-type">T/F</span></div><p style="font-weight:600;margin:4px 0;">"{stmt}"</p><div><span class="tf-btn tf-t" onclick="checkTF(this,{t},\'f{qn}\')">✅ True</span><span class="tf-btn tf-f" onclick="checkTF(this,{f},\'f{qn}\')">❌ False</span></div><div class="fb" id="f{qn}"></div></div>'


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Reading Passage & Analysis
# ══════════════════════════════════════════════════════════════════════════════

def _build_reading_page(vocab, theme, theme_tr, grade, week, cfg, seed):
    rng = random.Random(seed)
    passage = rng.choice(_PASSAGES)
    paras = passage["paragraphs"][:cfg["passage_para"]]

    para_html = ""
    full_parts = []
    for i, p in enumerate(paras):
        para_html += f'<div class="para" onclick="speak(\'{_js_safe(p)}\')"><strong>§{i+1}</strong> {p}</div>'
        full_parts.append(p)
    full = " ".join(full_parts)

    # Analysis questions
    qh = ""
    qn = 0

    qn += 1
    qh += _mcq(qn, "What is the main topic of this passage?",
                f"It discusses {passage['category']} and its implications.",
                ["It is about cooking recipes.", "It describes a fictional story."], rng, "main idea")

    qn += 1
    qh += _mcq(qn, "What is the author's purpose in writing this text?",
                "To inform and analyze a contemporary issue.",
                ["To entertain with a funny story.", "To advertise a product."], rng, "purpose")

    if len(paras) > 1:
        qn += 1
        short_p2 = paras[1][:80] + "..."
        qh += _mcq(qn, f"In paragraph 2, the author suggests that:",
                    short_p2, ["Everything is perfect.", "There are no concerns."], rng, "detail")

    qn += 1
    qh += _mcq(qn, "Which of the following can be inferred from the passage?",
                "The topic has both positive and negative aspects.",
                ["Everyone agrees on the solution.", "The topic is irrelevant today."], rng, "inference")

    qn += 1
    qh += _tf(qn, paras[0][:90] + "...", True)

    while qn < cfg["analysis_q"]:
        qn += 1
        qh += _tf(qn, "The passage claims that there are no challenges related to this topic.", False)

    # Vocab
    voc = ""
    for w in vocab[:8]:
        voc += f'<span class="phrase-chip" onclick="speak(\'{_js_safe(w)}\')">{w}</span>'

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">📖 Reading & Analysis</div>
    <div class="page-sub">Critical reading + interpretation — Week {week}: {theme}</div>
    <span class="badge badge-week">Week {week} • {cfg['label']}</span>
    <span class="badge badge-cefr">CEFR {cfg['cefr']}</span>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="prog"><div class="prog-fill" id="progFill" style="width:0%;"></div></div>

    <div class="card"><div class="card-t">{passage['emoji']} {passage['title']}</div>
    {para_html}
    <div style="text-align:center;margin-top:10px;">
    <button class="btn btn-p" onclick="speak('{_js_safe(full)}')">🔊 Listen to Full Text</button></div></div>

    <div class="card" style="border-left-color:{cfg['color_accent']};"><div class="card-t">📝 Key Vocabulary</div>
    <div style="text-align:center;">{voc}</div></div>

    {qh}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Writing Workshop
# ══════════════════════════════════════════════════════════════════════════════

def _build_writing_page(vocab, theme, theme_tr, grade, week, cfg, seed):
    rng = random.Random(seed + 1)

    tasks_html = ""
    categories = list(_WRITING_TASKS.keys())
    rng.shuffle(categories)

    for cat_idx, cat in enumerate(categories[:cfg["writing_tasks"]]):
        pool = _WRITING_TASKS[cat]
        task = rng.choice(pool)

        struct_html = ""
        for i, s in enumerate(task["structure"]):
            struct_html += f'<div class="note-line"><span class="note-bullet">{i+1}.</span><span>{s}</span></div>'

        phrases_html = ""
        for ph in task["useful_phrases"]:
            phrases_html += f'<span class="phrase-chip" onclick="speak(\'{_js_safe(ph)}\')">{ph}</span>'

        rubric_html = "<table class='rubric-table'><tr><th>Criterion</th><th>Max Score</th></tr>"
        for k, v in task["rubric"].items():
            rubric_html += f"<tr><td>{k.title()}</td><td>{v}</td></tr>"
        total = sum(task["rubric"].values())
        rubric_html += f"<tr style='font-weight:800;'><td>TOTAL</td><td>{total}</td></tr></table>"

        ta_id = f"wa_{cat_idx}"
        wc_id = f"wc_{cat_idx}"
        cat_label = {"opinion": "📝 Opinion Essay", "email": "✉️ E-mail Writing", "summary": "📋 Summary Writing"}

        tasks_html += f"""
        <div class="card">
            <div class="card-t">{cat_label.get(cat, cat.title())}</div>
            <div style="background:{cfg['color_bg']};padding:12px;border-radius:10px;margin-bottom:10px;font-weight:600;">
                {task['prompt']}</div>
            <details><summary style="cursor:pointer;color:{cfg['color_primary']};font-weight:700;font-size:.88em;">
                📐 Structure Guide</summary><div class="note-card">{struct_html}</div></details>
            <details><summary style="cursor:pointer;color:{cfg['color_primary']};font-weight:700;font-size:.88em;margin-top:6px;">
                💡 Useful Phrases</summary><div style="margin:6px 0;">{phrases_html}</div></details>
            <textarea class="writing-area" id="{ta_id}" placeholder="Write your {cat} here..."
                      oninput="countWords(this,'{wc_id}')"></textarea>
            <div style="text-align:right;font-size:.75em;color:#6b7280;" id="{wc_id}">0 words</div>
            <details><summary style="cursor:pointer;color:{cfg['color_accent']};font-weight:700;font-size:.85em;margin-top:6px;">
                📊 Rubric</summary>{rubric_html}</details>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">✍️ Writing Workshop</div>
    <div class="page-sub">Opinion • E-mail • Summary — Week {week}: {theme}</div>
    <span class="badge badge-week">Week {week} • {cfg['label']}</span>
    <span class="badge badge-cefr">CEFR {cfg['cefr']}</span>
    {tasks_html}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Note Taking & Outlining
# ══════════════════════════════════════════════════════════════════════════════

def _build_notetaking_page(vocab, theme, theme_tr, grade, week, cfg, seed):
    rng = random.Random(seed + 2)
    passage = rng.choice(_PASSAGES)
    paras = passage["paragraphs"][:min(3, cfg["passage_para"])]

    para_html = ""
    for i, p in enumerate(paras):
        para_html += f'<div class="para" onclick="speak(\'{_js_safe(p)}\')"><strong>§{i+1}</strong> {p}</div>'

    # Note-taking template
    note_lines = ""
    for i in range(cfg["note_items"]):
        note_lines += f"""
        <div class="note-line">
            <span class="note-bullet">•</span>
            <input type="text" style="flex:1;border:none;border-bottom:1.5px dashed #bbb;
                   padding:4px;font-family:inherit;font-size:.9em;background:transparent;"
                   placeholder="Key point {i+1}...">
        </div>"""

    # Main idea extraction
    qh = ""
    qn = 0
    qn += 1
    qh += _mcq(qn, "What is the main idea of paragraph 1?",
                passage["paragraphs"][0][:70] + "...",
                ["It is about a cooking show.", "It describes a sports event."], rng, "main idea")

    if len(paras) > 1:
        qn += 1
        qh += _mcq(qn, "Which key detail supports the author's argument in paragraph 2?",
                    paras[1][:70] + "...",
                    ["There is no supporting detail.", "The text contradicts itself."], rng, "detail")

    qn += 1
    qh += _mcq(qn, "How would you organize the information from this text?",
                "By topic and supporting details.",
                ["Alphabetically.", "By color."], rng, "organization")

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">📋 Note Taking & Outlining</div>
    <div class="page-sub">Extract key ideas and organize information — Week {week}: {theme}</div>
    <span class="badge badge-week">Week {week} • {cfg['label']}</span>
    <span class="badge badge-cefr">CEFR {cfg['cefr']}</span>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="prog"><div class="prog-fill" id="progFill" style="width:0%;"></div></div>

    <div class="card"><div class="card-t">{passage['emoji']} {passage['title']}</div>{para_html}
    <div style="text-align:center;margin-top:8px;">
    <button class="btn btn-s" onclick="speak('{_js_safe(' '.join(paras))}')">🔊 Listen</button></div></div>

    <div class="card" style="border-left-color:#FF9800;">
        <div class="card-t">📝 Your Notes</div>
        <p style="font-size:.8em;color:#6b7280;margin-bottom:8px;">Write key points from the passage:</p>
        <div class="note-card">{note_lines}</div>
    </div>

    <div class="card" style="border-left-color:#4CAF50;">
        <div class="card-t">📋 Summary Writing</div>
        <p style="font-size:.8em;color:#6b7280;margin-bottom:6px;">Using your notes, write a short summary (60-80 words):</p>
        <textarea class="writing-area" id="sumArea" placeholder="Write your summary here..."
                  oninput="countWords(this,'sumWc')" style="min-height:100px;"></textarea>
        <div style="text-align:right;font-size:.75em;color:#6b7280;" id="sumWc">0 words</div>
    </div>

    {qh}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Exam Practice
# ══════════════════════════════════════════════════════════════════════════════

def _build_exam_page(vocab, theme, theme_tr, grade, week, cfg, seed):
    rng = random.Random(seed + 3)

    qh = ""
    qn = 0

    # Section A: Cloze test
    cloze = rng.choice(_CLOZE_PASSAGES)
    display_text = cloze["text"]
    for gid in cloze["gaps"]:
        display_text = display_text.replace(f"_{gid}_", f'<span class="cloze-gap">({gid})</span>')

    qh += f"""<div class="section-hdr"><h3>Section A: Cloze Test</h3>
    <p>Fill in the blanks with the correct word</p></div>
    <div class="card"><div style="line-height:2.0;">{display_text}</div></div>"""

    for gid, data in cloze["gaps"].items():
        qn += 1
        qh += _mcq(qn, f"Gap ({gid}):", data["correct"],
                    [o for o in data["options"] if o != data["correct"]], rng, "cloze")

    # Section B: Grammar
    qh += '<div class="section-hdr"><h3>Section B: Grammar</h3><p>Choose the correct option</p></div>'
    gram_pool = list(_GRAMMAR_EXAM_QS)
    rng.shuffle(gram_pool)
    for sent, correct, wrongs in gram_pool[:4]:
        qn += 1
        qh += _mcq(qn, f"Complete: {sent}", correct, wrongs, rng, "grammar")

    # Section C: Vocabulary
    qh += '<div class="section-hdr"><h3>Section C: Vocabulary</h3><p>Choose the best word</p></div>'
    voc_pool = list(_VOCAB_EXAM_QS)
    rng.shuffle(voc_pool)
    for sent, correct, wrongs in voc_pool[:3]:
        qn += 1
        qh += _mcq(qn, sent, correct, wrongs, rng, "vocabulary")

    # Fill remaining
    while qn < cfg["exam_q"]:
        qn += 1
        gq = gram_pool[qn % len(gram_pool)]
        qh += _mcq(qn, f"Complete: {gq[0]}", gq[1], gq[2], rng, "grammar")

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="section-hdr" style="margin-top:0;"><h3>📝 Exam Practice</h3>
    <p>Week {week} • {theme} • {cfg['label']} ({cfg['cefr']})</p></div>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="prog"><div class="prog-fill" id="progFill" style="width:0%;"></div></div>

    {qh}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Full Review Test
# ══════════════════════════════════════════════════════════════════════════════

def _build_review_page(vocab, theme, theme_tr, grade, week, cfg, seed):
    rng = random.Random(seed + 4)

    qh = ""
    qn = 0

    # Section A: Reading
    passage = rng.choice(_PASSAGES)
    paras = passage["paragraphs"][:2]
    para_html = ""
    for i, p in enumerate(paras):
        para_html += f'<div class="para" onclick="speak(\'{_js_safe(p)}\')">{p}</div>'

    qh += f"""<div class="section-hdr"><h3>Section A: Reading Comprehension</h3></div>
    <div class="card"><div class="card-t">{passage['emoji']} {passage['title']}</div>{para_html}</div>"""

    qn += 1
    qh += _mcq(qn, "What is the passage about?",
                f"It is about {passage['category']}.",
                ["It is about fashion.", "It is about cooking."], rng, "main idea")
    qn += 1
    qh += _tf(qn, paras[0][:80] + "...", True)
    qn += 1
    qh += _tf(qn, "The author believes this topic is completely unimportant.", False)
    qn += 1
    qh += _mcq(qn, "What can we infer from the passage?",
                "The topic is complex and has multiple dimensions.",
                ["There is only one viewpoint.", "The text has no conclusion."], rng, "inference")

    # Section B: Grammar
    qh += '<div class="section-hdr"><h3>Section B: Grammar & Use of English</h3></div>'
    gram = list(_GRAMMAR_EXAM_QS)
    rng.shuffle(gram)
    for s, c, w in gram[:4]:
        qn += 1
        qh += _mcq(qn, f"Complete: {s}", c, w, rng, "grammar")

    # Section C: Vocabulary
    qh += '<div class="section-hdr"><h3>Section C: Vocabulary</h3></div>'
    voc = list(_VOCAB_EXAM_QS)
    rng.shuffle(voc)
    for s, c, w in voc[:3]:
        qn += 1
        qh += _mcq(qn, s, c, w, rng, "vocabulary")

    # Section D: Writing
    rng2 = random.Random(seed + 44)
    cat = rng2.choice(["opinion", "email"])
    task = rng2.choice(_WRITING_TASKS[cat])
    cat_label = {"opinion": "Opinion Essay", "email": "E-mail"}

    qh += f"""<div class="section-hdr"><h3>Section D: Writing — {cat_label.get(cat, cat.title())}</h3></div>
    <div class="card">
        <div style="background:{cfg['color_bg']};padding:10px;border-radius:8px;font-weight:600;margin-bottom:8px;">
            {task['prompt']}</div>
        <textarea class="writing-area" id="revWrite" placeholder="Write here..."
                  oninput="countWords(this,'revWc')"></textarea>
        <div style="text-align:right;font-size:.75em;color:#6b7280;" id="revWc">0 words</div>
    </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="section-hdr" style="margin-top:0;"><h3>📝 Full Review Test</h3>
    <p>Week {week} • {theme} • {cfg['label']} ({cfg['cefr']}) — General Review</p></div>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="prog"><div class="prog-fill" id="progFill" style="width:0%;"></div></div>

    {qh}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_NAMES = [
    "📖 Reading & Analysis",
    "✍️ Writing Workshop",
    "📋 Note Taking",
    "📝 Exam Practice",
    "🏆 Review Test",
]


def build_rwp_pages(grade: int, week_num: int, curriculum_weeks: list) -> list[str]:
    """Build 5 Read, Write & Prepare pages for a given grade/week."""
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[9])
    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    return [
        _build_reading_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_writing_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_notetaking_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_exam_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_review_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
    ]


def build_full_rwp(grade: int, curriculum_weeks: list,
                    selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Read, Write & Prepare book for all weeks."""
    result = []
    for w in curriculum_weeks:
        wn = w.get("week", 0)
        if selected_weeks and wn not in selected_weeks:
            continue
        pages = build_rwp_pages(grade, wn, curriculum_weeks)
        if pages:
            result.append({"week": wn, "theme": w.get("theme", f"Week {wn}"), "pages": pages})
    return result
