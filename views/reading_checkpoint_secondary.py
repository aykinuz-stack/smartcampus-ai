# -*- coding: utf-8 -*-
"""Reading & Checkpoint — Ortaokul (5-8) Reading + Assessment Kitabı.

Interactive HTML pages for secondary school reading & assessment.
Activity types (5 pages per week):
  1. Reading Passage (Okuma parçası + bilgi metinleri)
  2. Dialog & Functional Text (Diyaloglar + günlük metin)
  3. Comprehension Deep (Ana fikir + detay + çıkarım soruları)
  4. Unit Checkpoint (Ünite checkpoint testi — beceri temelli)
  5. Review & Assessment (Dönem tekrar testi — karma)

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
    5: {"label": "5th Grade", "cefr": "A1", "font_size": "17px",
        "passage_sentences": 8, "dialog_turns": 5,
        "comp_questions": 6, "checkpoint_q": 8, "review_q": 10,
        "color_primary": "#E91E63", "color_accent": "#AD1457", "color_bg": "#FCE4EC"},
    6: {"label": "6th Grade", "cefr": "A1+", "font_size": "16px",
        "passage_sentences": 10, "dialog_turns": 6,
        "comp_questions": 7, "checkpoint_q": 10, "review_q": 12,
        "color_primary": "#9C27B0", "color_accent": "#6A1B9A", "color_bg": "#F3E5F5"},
    7: {"label": "7th Grade", "cefr": "A2", "font_size": "15px",
        "passage_sentences": 12, "dialog_turns": 7,
        "comp_questions": 8, "checkpoint_q": 12, "review_q": 14,
        "color_primary": "#00897B", "color_accent": "#00695C", "color_bg": "#E0F2F1"},
    8: {"label": "8th Grade", "cefr": "A2+", "font_size": "15px",
        "passage_sentences": 14, "dialog_turns": 8,
        "comp_questions": 9, "checkpoint_q": 14, "review_q": 16,
        "color_primary": "#1565C0", "color_accent": "#0D47A1", "color_bg": "#E3F2FD"},
}

# ══════════════════════════════════════════════════════════════════════════════
# READING PASSAGE TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

_PASSAGE_TEMPLATES = [
    {"title": "A Special Day at School", "category": "school", "emoji": "🏫",
     "sentences": [
         "Last week, something special happened at {name}'s school.",
         "The students organized a science fair for the first time.",
         "Each student prepared a project about a topic they chose.",
         "{name} decided to make a project about {topic}.",
         "It took {name} two weeks to prepare everything.",
         "On the day of the fair, all the parents came to school.",
         "The gym was full of colorful posters and experiments.",
         "{name}'s project was about how plants grow in different conditions.",
         "Some students made robots, while others demonstrated chemical reactions.",
         "The teachers were very impressed with the students' work.",
         "At the end of the day, the principal gave awards to the best projects.",
         "{name} won the second prize and felt very proud.",
         "Everyone agreed that the science fair was a great success.",
         "They decided to organize it again next year.",
     ]},
    {"title": "The Lost Dog", "category": "animals", "emoji": "🐕",
     "sentences": [
         "One Saturday morning, {name} found a small dog in the park.",
         "The dog looked hungry and scared.",
         "It had brown fur and big, sad eyes.",
         "{name} gave the dog some water and a piece of bread.",
         "The dog started wagging its tail happily.",
         "{name} noticed that the dog had a collar with a phone number on it.",
         "'{name2}, can you help me call this number?' {name} asked a friend.",
         "They called the number and spoke to the dog's owner, Mrs. Johnson.",
         "She was very worried and said the dog's name was Buddy.",
         "Buddy had escaped from the garden that morning.",
         "Mrs. Johnson came to the park in fifteen minutes.",
         "She was so happy to see Buddy again.",
         "'Thank you so much for finding my dog!' she said.",
         "{name} felt good about helping Buddy get home safely.",
     ]},
    {"title": "Healthy Eating Habits", "category": "health", "emoji": "🥗",
     "sentences": [
         "Eating healthy food is very important for our bodies.",
         "We need different types of food to stay strong and healthy.",
         "Fruits and vegetables give us vitamins and minerals.",
         "We should eat at least five portions of fruit and vegetables every day.",
         "Protein foods like meat, fish, eggs, and beans help our muscles grow.",
         "Dairy products such as milk, cheese, and yogurt are good for our bones.",
         "Whole grains like bread, rice, and pasta give us energy.",
         "We should also drink plenty of water throughout the day.",
         "It's better to avoid too much sugar and junk food.",
         "Eating a balanced breakfast helps us concentrate at school.",
         "Studies show that students who eat breakfast perform better in exams.",
         "We should try to eat our meals at regular times.",
         "Cooking at home is healthier than eating fast food.",
         "Remember: a healthy diet leads to a healthy life!",
     ]},
    {"title": "Technology and Daily Life", "category": "technology", "emoji": "💻",
     "sentences": [
         "Technology has changed the way we live in many ways.",
         "Smartphones help us communicate with people all around the world.",
         "We can send messages, make video calls, and share photos instantly.",
         "The internet allows us to find information about almost anything.",
         "Students use computers and tablets for their homework and research.",
         "Online education became very popular in recent years.",
         "Many people now work from home thanks to technology.",
         "Social media connects millions of people every day.",
         "However, spending too much time on screens is not healthy.",
         "Experts recommend taking breaks every 30 minutes while using devices.",
         "It's important to balance screen time with outdoor activities.",
         "Technology is a great tool, but we should use it wisely.",
         "We must also be careful about our online safety and privacy.",
         "The future will bring even more technological changes to our lives.",
     ]},
    {"title": "Traveling by Train", "category": "travel", "emoji": "🚂",
     "sentences": [
         "{name} and the family were going on a holiday by train.",
         "They arrived at the train station early in the morning.",
         "The station was crowded with travelers carrying their suitcases.",
         "{name} looked at the big departure board to find their platform.",
         "'Our train departs from Platform 3 at 9:15,' said {name}'s father.",
         "They bought some snacks and magazines for the journey.",
         "When the train arrived, they found their seats and sat down.",
         "The train started moving slowly, then picked up speed.",
         "{name} watched the beautiful scenery through the window.",
         "Green fields, small villages, and rivers passed by quickly.",
         "The journey took about three hours.",
         "They had sandwiches and juice during the trip.",
         "Finally, the train arrived at the seaside town.",
         "{name} could see the blue sea from the station and felt excited.",
     ]},
    {"title": "The Environment and Recycling", "category": "environment", "emoji": "♻️",
     "sentences": [
         "Taking care of our environment is everyone's responsibility.",
         "Every year, millions of tons of waste end up in landfills and oceans.",
         "Recycling is one of the most effective ways to reduce waste.",
         "We can recycle paper, glass, plastic, and metal.",
         "Recycling one ton of paper saves 17 trees.",
         "Using reusable bags instead of plastic bags helps the environment.",
         "We should also try to save water and electricity at home.",
         "Turning off lights when leaving a room is a simple but effective habit.",
         "Planting trees helps clean the air and provides homes for animals.",
         "Many schools now have eco-clubs where students learn about nature.",
         "Some cities have started using solar energy and wind power.",
         "Everyone can make a difference by making small changes in daily life.",
         "If we all work together, we can protect our planet for future generations.",
         "Remember: reduce, reuse, and recycle!",
     ]},
]

_DIALOG_TEMPLATES = [
    {"title": "At the Library", "emoji": "📚",
     "speakers": ["{name}", "Librarian"],
     "lines": [
         ("{name}", "Excuse me, I'm looking for a book about {topic}."),
         ("Librarian", "Of course! We have several books on that topic. Follow me."),
         ("{name}", "Thank you. Can I borrow it for two weeks?"),
         ("Librarian", "Yes, you can keep it for 14 days. Do you have your library card?"),
         ("{name}", "Yes, here it is."),
         ("Librarian", "Great. The book is due on the 25th. Don't forget to return it on time."),
         ("{name}", "I won't. Thank you for your help!"),
         ("Librarian", "You're welcome. Enjoy reading!"),
     ]},
    {"title": "Planning a Trip", "emoji": "✈️",
     "speakers": ["{name}", "{name2}"],
     "lines": [
         ("{name}", "Hey {name2}, have you thought about where to go for the holiday?"),
         ("{name2}", "I was thinking about going to the beach. What do you think?"),
         ("{name}", "That sounds great! How long should we stay?"),
         ("{name2}", "Maybe four or five days. We can stay at a hotel."),
         ("{name}", "Good idea. Should we go by bus or by train?"),
         ("{name2}", "Let's take the train. It's faster and more comfortable."),
         ("{name}", "Alright. I'll check the ticket prices online."),
         ("{name2}", "Perfect. Let's talk to our parents and make a plan."),
     ]},
    {"title": "At the Doctor's Office", "emoji": "🏥",
     "speakers": ["Doctor", "{name}"],
     "lines": [
         ("Doctor", "Hello {name}, what seems to be the problem?"),
         ("{name}", "I've had a sore throat and a headache since yesterday."),
         ("Doctor", "Let me check. Please open your mouth and say 'aah'."),
         ("{name}", "Aah... Is it serious, doctor?"),
         ("Doctor", "No, it's just a cold. You need to rest and drink warm fluids."),
         ("{name}", "Should I take any medicine?"),
         ("Doctor", "I'll prescribe some medicine. Take it three times a day after meals."),
         ("{name}", "Thank you, doctor. When should I come back?"),
     ]},
    {"title": "A Phone Conversation", "emoji": "📱",
     "speakers": ["{name}", "{name2}"],
     "lines": [
         ("{name}", "Hello, {name2}? Are you free this afternoon?"),
         ("{name2}", "Hi, {name}! Yes, I don't have any plans. Why?"),
         ("{name}", "There's a new film at the cinema. Do you want to come?"),
         ("{name2}", "Sure! What time does it start?"),
         ("{name}", "The show starts at 3 o'clock. Let's meet at 2:30 in front of the cinema."),
         ("{name2}", "Sounds good. Should I bring anything?"),
         ("{name}", "Just yourself! I'll buy the tickets online."),
         ("{name2}", "Great, see you there! I can't wait."),
     ]},
    {"title": "Shopping for Clothes", "emoji": "🛍️",
     "speakers": ["{name}", "Shop Assistant"],
     "lines": [
         ("Shop Assistant", "Welcome! Can I help you find anything?"),
         ("{name}", "Yes, I'm looking for a jacket for the winter."),
         ("Shop Assistant", "What size do you wear?"),
         ("{name}", "I think medium. Can I try on that blue one?"),
         ("Shop Assistant", "Of course! The fitting rooms are on the right."),
         ("{name}", "It fits well, but do you have it in black?"),
         ("Shop Assistant", "Let me check... Yes, here you go."),
         ("{name}", "Perfect. How much is it?"),
     ]},
    {"title": "Asking for Directions", "emoji": "🗺️",
     "speakers": ["{name}", "Stranger"],
     "lines": [
         ("{name}", "Excuse me, could you tell me how to get to the museum?"),
         ("Stranger", "Sure! Go straight ahead for two blocks."),
         ("{name}", "Two blocks straight. Then what?"),
         ("Stranger", "Then turn left at the traffic lights. The museum is on the right."),
         ("{name}", "Is it far from here? Can I walk?"),
         ("Stranger", "It's about ten minutes on foot. You can also take bus number 7."),
         ("{name}", "I'll walk. Thank you very much!"),
         ("Stranger", "No problem. You can't miss it — it's a big white building."),
     ]},
]

_INFO_TEXTS = [
    {"title": "The Water Cycle", "emoji": "💧", "category": "science",
     "text": [
         "The water cycle is one of the most important processes on Earth.",
         "It describes how water moves continuously between the land, oceans, and atmosphere.",
         "First, the sun heats the water in rivers, lakes, and oceans.",
         "This causes the water to evaporate and turn into water vapor.",
         "The water vapor rises into the atmosphere and cools down.",
         "As it cools, it condenses and forms clouds.",
         "When the clouds become heavy with water droplets, precipitation occurs.",
         "Precipitation can be rain, snow, sleet, or hail.",
         "Some of this water flows into rivers and streams and returns to the ocean.",
         "Some of it seeps into the ground and becomes groundwater.",
         "This cycle repeats endlessly, keeping water available for all living things.",
     ]},
    {"title": "The Solar System", "emoji": "🪐", "category": "science",
     "text": [
         "Our solar system consists of the Sun and everything that orbits around it.",
         "There are eight planets in our solar system.",
         "The four inner planets — Mercury, Venus, Earth, and Mars — are rocky.",
         "The four outer planets — Jupiter, Saturn, Uranus, and Neptune — are gas giants.",
         "Earth is the third planet from the Sun and the only one known to support life.",
         "The Moon is Earth's only natural satellite.",
         "Jupiter is the largest planet, while Mercury is the smallest.",
         "Saturn is famous for its beautiful rings made of ice and rock.",
         "The Sun is a star at the center of our solar system.",
         "It provides the light and heat needed for life on Earth.",
         "Scientists continue to explore our solar system using telescopes and spacecraft.",
     ]},
    {"title": "Famous Inventors", "emoji": "💡", "category": "history",
     "text": [
         "Throughout history, many inventors have changed the world with their ideas.",
         "Thomas Edison invented the practical light bulb in 1879.",
         "Before his invention, people used candles and gas lamps for light.",
         "Alexander Graham Bell invented the telephone in 1876.",
         "His invention made it possible to talk to people far away.",
         "The Wright Brothers built and flew the first successful airplane in 1903.",
         "Their flight lasted only 12 seconds, but it changed transportation forever.",
         "Marie Curie discovered radioactivity and won two Nobel Prizes.",
         "Tim Berners-Lee invented the World Wide Web in 1989.",
         "Thanks to his invention, billions of people can now access information online.",
         "These inventors show us that curiosity and hard work can change the world.",
     ]},
]

_FILL_DATA = {
    "name": ["Tom", "Lily", "Jack", "Emma", "Sam", "Mia", "Ben", "Zoe", "Max", "Ava",
             "Oliver", "Sophie", "Leo", "Ruby", "Noah"],
    "name2": ["Alex", "Kate", "Chris", "Ella", "Ryan", "Amy"],
    "topic": ["space", "animals", "technology", "history", "nature", "sports",
              "music", "geography", "science", "art"],
}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _deterministic_seed(grade: int, week: int) -> int:
    return int(hashlib.md5(f"rc_{grade}_{week}".encode()).hexdigest()[:8], 16)


def _fill(text: str, rng: random.Random, vocab: list) -> str:
    result = text
    for key, values in _FILL_DATA.items():
        placeholder = "{" + key + "}"
        while placeholder in result:
            pool = list(values)
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
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, {bg} 0%, #f8f9fa 100%);
        color: #2d3436; font-size: {fs}; padding: 18px; line-height:1.65;
    }}
    .page-title {{
        text-align:center; font-size:1.6em; font-weight:800;
        background: linear-gradient(135deg, {cp}, {ca});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        margin-bottom:4px;
    }}
    .page-subtitle {{ text-align:center; font-size:.82em; color:#6b7280; margin-bottom:16px; }}
    .week-badge {{
        display:inline-block; background:{cp}; color:#fff;
        padding:3px 14px; border-radius:20px; font-size:.7em; font-weight:700;
        margin-bottom:10px;
    }}
    .cefr-badge {{
        display:inline-block; background:{ca}; color:#fff;
        padding:2px 10px; border-radius:12px; font-size:.65em; font-weight:700;
        margin-left:6px;
    }}
    .card {{
        background:#fff; border-radius:14px;
        box-shadow:0 3px 12px rgba(0,0,0,.07);
        padding:16px; margin-bottom:14px;
        border-left:4px solid {cp}; transition:transform .2s;
    }}
    .card:hover {{ transform:translateY(-1px); }}
    .card-title {{ font-size:1.1em; font-weight:700; color:{cp}; margin-bottom:6px; }}
    .passage-line {{
        padding:8px 14px; border-radius:10px; margin:4px 0;
        cursor:pointer; transition:all .2s; line-height:1.7;
        border:1px solid transparent;
    }}
    .passage-line:hover {{ background:{bg}; border-color:rgba(0,0,0,.06); }}
    .passage-line .line-num {{
        display:inline-block; width:24px; font-weight:800;
        color:{ca}; font-size:.8em; margin-right:4px;
    }}
    .dialog-row {{ display:flex; margin:6px 0; gap:8px; }}
    .bubble {{
        padding:10px 14px; border-radius:16px; font-size:.92em;
        max-width:80%; font-weight:500; cursor:pointer; transition:all .2s;
    }}
    .bubble:hover {{ transform:scale(1.01); }}
    .bubble-l {{
        background:linear-gradient(135deg, #e3f2fd, #bbdefb);
        border:1.5px solid #90caf9; border-bottom-left-radius:4px;
    }}
    .bubble-r {{
        background:linear-gradient(135deg, #f3e5f5, #e1bee7);
        border:1.5px solid #ce93d8; border-bottom-right-radius:4px;
        margin-left:auto;
    }}
    .speaker {{ font-size:.65em; font-weight:800; color:{ca}; margin-bottom:2px; }}
    .q-box {{
        background:#fff; border:2px solid {cp}; border-radius:12px;
        padding:14px; margin:10px 0;
    }}
    .q-num {{
        display:inline-block; background:{cp}; color:#fff;
        width:28px; height:28px; border-radius:50%; text-align:center;
        line-height:28px; font-size:.8em; font-weight:800; margin-right:6px;
    }}
    .q-text {{ font-weight:700; font-size:.95em; margin-bottom:8px; }}
    .q-type {{
        display:inline-block; background:{bg}; color:{cp};
        padding:2px 8px; border-radius:8px; font-size:.6em; font-weight:700;
        margin-left:4px;
    }}
    .opt-btn {{
        display:block; width:100%; text-align:left;
        padding:9px 14px; margin:3px 0;
        border:2px solid #e8e8e8; border-radius:10px;
        background:#fafafa; cursor:pointer;
        font-family:inherit; font-size:.88em; font-weight:600;
        transition:all .2s;
    }}
    .opt-btn:hover {{ border-color:{cp}; background:{bg}; }}
    .tf-btn {{
        display:inline-block; padding:8px 22px;
        border:2px solid #e0e0e0; border-radius:18px;
        cursor:pointer; font-weight:700; margin:3px 6px;
        transition:all .2s; font-size:.85em;
    }}
    .tf-true {{ color:#27ae60; }} .tf-true:hover {{ border-color:#27ae60; background:#e8f5e9; }}
    .tf-false {{ color:#e74c3c; }} .tf-false:hover {{ border-color:#e74c3c; background:#fce4ec; }}
    .fb {{ margin-top:5px; font-weight:700; display:none; font-size:.85em; }}
    .score-bar {{
        text-align:center; font-size:1.4em; font-weight:800;
        color:{cp}; margin:14px 0; padding:8px;
        background:#fff; border-radius:12px;
        box-shadow:0 2px 8px rgba(0,0,0,.06);
    }}
    .checkpoint-header {{
        background:linear-gradient(135deg, {cp}, {ca});
        color:#fff; padding:14px 20px; border-radius:14px;
        text-align:center; margin-bottom:16px;
    }}
    .checkpoint-header h2 {{ margin:0; font-size:1.3em; }}
    .checkpoint-header p {{ margin:4px 0 0; font-size:.8em; opacity:.9; }}
    .btn {{
        display:inline-block; padding:9px 20px;
        border:none; border-radius:22px; cursor:pointer;
        font-family:inherit; font-size:.82em; font-weight:700;
        color:#fff; transition:all .2s;
    }}
    .btn-primary {{ background:linear-gradient(135deg, {cp}, {ca}); }}
    .btn-primary:hover {{ transform:scale(1.04); }}
    .btn-speak {{ background:linear-gradient(135deg, #4FC3F7, #00BCD4); }}
    .btn-speak:hover {{ transform:scale(1.04); }}
    .progress-bar {{
        width:100%; height:8px; background:#e0e0e0; border-radius:4px;
        margin:8px 0; overflow:hidden;
    }}
    .progress-fill {{
        height:100%; background:linear-gradient(90deg, {cp}, {ca});
        border-radius:4px; transition:width .5s ease;
    }}
    </style>"""


def _tts_script() -> str:
    return """
    <script>
    function speak(t,r){r=r||0.8;if(!window.speechSynthesis)return;
    window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);
    u.lang='en-US';u.rate=r;u.pitch=1.0;window.speechSynthesis.speak(u);}
    function speakSlow(t){speak(t,0.65);}
    function speakNormal(t){speak(t,0.8);}

    var totalQ=0,correctQ=0;

    function checkOpt(btn,ok,fbId){
        var p=btn.parentElement;
        p.querySelectorAll('.opt-btn').forEach(function(b){b.disabled=true;b.style.opacity='0.45';});
        totalQ++;
        var fb=document.getElementById(fbId);
        if(ok){
            btn.style.background='#d4edda';btn.style.borderColor='#27ae60';btn.style.opacity='1';
            correctQ++;
            if(fb){fb.innerHTML='✅ Correct!';fb.style.color='#27ae60';}
        }else{
            btn.style.background='#f8d7da';btn.style.borderColor='#e74c3c';btn.style.opacity='1';
            if(fb){fb.innerHTML='❌ Not quite — try to find the answer in the text!';fb.style.color='#e74c3c';}
        }
        if(fb)fb.style.display='block';
        updateScore();
    }

    function checkTF(btn,ok,fbId){
        totalQ++;
        var p=btn.parentElement;
        p.querySelectorAll('.tf-btn').forEach(function(b){b.style.pointerEvents='none';b.style.opacity='0.45';});
        var fb=document.getElementById(fbId);
        if(ok){
            btn.style.background='#d4edda';btn.style.borderColor='#27ae60';btn.style.opacity='1';
            correctQ++;
            if(fb){fb.innerHTML='✅ Correct!';fb.style.color='#27ae60';}
        }else{
            btn.style.background='#f8d7da';btn.style.borderColor='#e74c3c';btn.style.opacity='1';
            if(fb){fb.innerHTML='❌ Wrong!';fb.style.color='#e74c3c';}
        }
        if(fb)fb.style.display='block';
        updateScore();
    }

    function updateScore(){
        var el=document.getElementById('scoreDisplay');
        if(!el)return;
        var pct=totalQ>0?Math.round(correctQ/totalQ*100):0;
        var stars=pct>=80?'⭐⭐⭐':pct>=60?'⭐⭐':pct>=40?'⭐':'';
        el.innerHTML='Score: '+correctQ+'/'+totalQ+' ('+pct+'%) '+stars;
        var bar=document.getElementById('progressFill');
        if(bar)bar.style.width=pct+'%';
    }
    </script>"""


# ══════════════════════════════════════════════════════════════════════════════
# QUESTION GENERATOR HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _make_mcq(q_num: int, q_text: str, correct: str, wrongs: list,
              rng: random.Random, q_type: str = "detail") -> str:
    opts = [correct] + wrongs[:2]
    rng.shuffle(opts)
    opts_html = ""
    for o in opts:
        is_c = "true" if o == correct else "false"
        opts_html += f"""<button class="opt-btn" onclick="checkOpt(this,{is_c},'fb{q_num}')">{o}</button>"""
    return f"""
    <div class="q-box">
        <div class="q-text"><span class="q-num">{q_num}</span> {q_text}
            <span class="q-type">{q_type}</span></div>
        <div>{opts_html}</div>
        <div class="fb" id="fb{q_num}"></div>
    </div>"""


def _make_tf(q_num: int, statement: str, is_true: bool) -> str:
    return f"""
    <div class="q-box">
        <div class="q-text"><span class="q-num">{q_num}</span> True or False?
            <span class="q-type">true/false</span></div>
        <p style="font-weight:600;margin:4px 0;">"{statement}"</p>
        <div>
            <span class="tf-btn tf-true" onclick="checkTF(this,{'true' if is_true else 'false'},'fb{q_num}')">✅ True</span>
            <span class="tf-btn tf-false" onclick="checkTF(this,{'true' if not is_true else 'false'},'fb{q_num}')">❌ False</span>
        </div>
        <div class="fb" id="fb{q_num}"></div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Reading Passage
# ══════════════════════════════════════════════════════════════════════════════

def _build_passage_page(vocab: list, theme: str, theme_tr: str,
                        grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed)
    tmpl = rng.choice(_PASSAGE_TEMPLATES)
    title = _fill(tmpl["title"], rng, vocab)
    max_s = cfg["passage_sentences"]
    sentences = [_fill(s, rng, vocab) for s in tmpl["sentences"][:max_s]]
    full = " ".join(sentences)

    lines_html = ""
    for i, s in enumerate(sentences):
        lines_html += f"""
        <div class="passage-line" onclick="speakNormal('{_js_safe(s)}')">
            <span class="line-num">{i+1}</span>{s}
        </div>"""

    # Vocab sidebar
    voc_html = ""
    for w in vocab[:8]:
        voc_html += f"""
        <span style="display:inline-block;background:{cfg['color_bg']};
              border:1.5px solid {cfg['color_primary']};padding:3px 10px;
              border-radius:14px;margin:2px;cursor:pointer;font-weight:600;
              font-size:.8em;" onclick="speakSlow('{_js_safe(w)}')">{w}</span>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">📖 Reading Passage</div>
    <div class="page-subtitle">Read carefully and understand! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>
    <span class="cefr-badge">CEFR {cfg['cefr']}</span>

    <div class="card">
        <div class="card-title">{tmpl['emoji']} {title}</div>
        {lines_html}
        <div style="text-align:center;margin-top:12px;">
            <button class="btn btn-primary" onclick="speakNormal('{_js_safe(full)}')">
                🔊 Listen to Full Text
            </button>
        </div>
    </div>

    <div class="card" style="border-left-color:{cfg['color_accent']};">
        <div class="card-title">📝 Key Vocabulary</div>
        <div style="text-align:center;">{voc_html}</div>
    </div>
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Dialog & Functional Text
# ══════════════════════════════════════════════════════════════════════════════

def _build_dialog_page(vocab: list, theme: str, theme_tr: str,
                       grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 1)

    # Dialog
    dtmpl = rng.choice(_DIALOG_TEMPLATES)
    d_title = dtmpl["title"]
    d_emoji = dtmpl["emoji"]
    max_t = cfg["dialog_turns"]
    d_lines = dtmpl["lines"][:max_t]

    dialog_html = ""
    for i, (speaker, line) in enumerate(d_lines):
        sp = _fill(speaker, rng, vocab)
        ln = _fill(line, rng, vocab)
        side = "l" if i % 2 == 0 else "r"
        align = "flex-start" if side == "l" else "flex-end"
        dialog_html += f"""
        <div class="dialog-row" style="justify-content:{align};">
            <div class="bubble bubble-{side}" onclick="speakNormal('{_js_safe(ln)}')">
                <div class="speaker">{sp}</div>{ln}
            </div>
        </div>"""

    full_dialog = " ".join([_fill(l, rng, vocab) for _, l in d_lines])

    # Info text
    info = rng.choice(_INFO_TEXTS)
    i_title = info["title"]
    i_emoji = info["emoji"]
    max_il = min(cfg["passage_sentences"], len(info["text"]))
    i_lines = info["text"][:max_il]

    info_html = ""
    for i, ln in enumerate(i_lines):
        info_html += f"""
        <div class="passage-line" onclick="speakNormal('{_js_safe(ln)}')">
            <span class="line-num">{i+1}</span>{ln}
        </div>"""

    full_info = " ".join(i_lines)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">💬 Dialog & Info Text</div>
    <div class="page-subtitle">Real-life communication! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>
    <span class="cefr-badge">CEFR {cfg['cefr']}</span>

    <div class="card">
        <div class="card-title">{d_emoji} Dialog: {d_title}</div>
        {dialog_html}
        <div style="text-align:center;margin-top:10px;">
            <button class="btn btn-speak" onclick="speakNormal('{_js_safe(full_dialog)}')">
                🔊 Listen to Dialog
            </button>
        </div>
    </div>

    <div class="card" style="border-left-color:#FF9800;">
        <div class="card-title">{i_emoji} Info Text: {i_title}</div>
        {info_html}
        <div style="text-align:center;margin-top:10px;">
            <button class="btn btn-primary" onclick="speakNormal('{_js_safe(full_info)}')">
                🔊 Listen to Full Text
            </button>
        </div>
    </div>
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Comprehension Deep
# ══════════════════════════════════════════════════════════════════════════════

def _build_comprehension_page(vocab: list, theme: str, theme_tr: str,
                               grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 2)
    tmpl = rng.choice(_PASSAGE_TEMPLATES)
    title = _fill(tmpl["title"], rng, vocab)
    max_s = cfg["passage_sentences"]
    sentences = [_fill(s, rng, vocab) for s in tmpl["sentences"][:max_s]]
    full = " ".join(sentences)

    lines_html = ""
    for i, s in enumerate(sentences):
        lines_html += f"""
        <div class="passage-line" onclick="speakNormal('{_js_safe(s)}')">
            <span class="line-num">{i+1}</span>{s}
        </div>"""

    q_html = ""
    qn = 0

    # Main idea question
    qn += 1
    correct_main = f"It is about {tmpl['category']} and daily experiences."
    wrongs_main = [
        "It is about cooking dinner at home.",
        "It is about playing video games all day.",
    ]
    q_html += _make_mcq(qn, "What is the main idea of this passage?",
                        correct_main, wrongs_main, rng, "main idea")

    # Detail questions
    for i in range(min(3, len(sentences) - 1)):
        qn += 1
        sent = sentences[min(i + 1, len(sentences) - 1)]
        short = sent[:70] + "..." if len(sent) > 70 else sent
        wrongs = [
            _fill("It happened in the {topic} class.", rng, vocab),
            _fill("{name} went to the {topic} festival.", rng, vocab),
        ]
        q_html += _make_mcq(qn, f"According to the text, what do we learn from sentence {i+2}?",
                            short, wrongs, rng, "detail")

    # Inference questions
    inferences = [
        ("What can we infer from the passage?",
         f"The author thinks {tmpl['category']} is important in daily life.",
         ["The author dislikes school.", "The text is about a fantasy story."]),
        ("What would probably happen next?",
         "The characters would continue with their activities.",
         ["They would fly to the moon.", "They would stop talking forever."]),
    ]
    for q_text, correct, wrongs in inferences[:max(1, cfg["comp_questions"] - qn)]:
        qn += 1
        q_html += _make_mcq(qn, q_text, correct, wrongs, rng, "inference")

    # True/False
    if qn < cfg["comp_questions"] and len(sentences) > 2:
        qn += 1
        q_html += _make_tf(qn, sentences[0], True)
    if qn < cfg["comp_questions"]:
        qn += 1
        q_html += _make_tf(qn, _fill("{name} traveled to Mars in the story.", rng, vocab), False)

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>
    <div class="page-title">🔍 Comprehension</div>
    <div class="page-subtitle">Main idea • Detail • Inference — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week} • {cfg['label']}</span>
    <span class="cefr-badge">CEFR {cfg['cefr']}</span>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%;"></div></div>

    <div class="card">
        <div class="card-title">{tmpl['emoji']} {title}</div>
        {lines_html}
        <div style="text-align:center;margin-top:10px;">
            <button class="btn btn-primary" onclick="speakNormal('{_js_safe(full)}')">🔊 Listen</button>
        </div>
    </div>

    {q_html}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Unit Checkpoint
# ══════════════════════════════════════════════════════════════════════════════

def _build_checkpoint_page(vocab: list, theme: str, theme_tr: str,
                            grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 3)

    q_html = ""
    qn = 0

    # Vocabulary checkpoint
    vocab_pool = list(vocab[:10]) if len(vocab) >= 10 else list(vocab) + [
        "important", "different", "because", "between", "before", "through"]
    rng.shuffle(vocab_pool)

    definitions = {
        "important": "having great value or meaning",
        "different": "not the same as another",
        "because": "for the reason that",
        "between": "in the space separating two things",
        "before": "earlier in time",
        "through": "moving in one side and out the other",
    }

    for w in vocab_pool[:3]:
        qn += 1
        defn = definitions.get(w, f"related to the topic of {theme}")
        wrongs = [
            f"a type of {rng.choice(['food', 'animal', 'sport'])}",
            f"the opposite of {rng.choice(['happy', 'big', 'fast'])}",
        ]
        q_html += _make_mcq(qn, f'What does "<strong>{w}</strong>" mean?',
                            defn, wrongs, rng, "vocabulary")

    # Grammar in context
    grammar_qs = [
        ("She ___ to school every day.", "goes",
         ["go", "going"], "grammar"),
        ("They ___ playing football now.", "are",
         ["is", "was"], "grammar"),
        ("He ___ his homework yesterday.", "did",
         ["does", "do"], "grammar"),
        ("We ___ visited that museum before.", "have",
         ["has", "had"], "grammar"),
        ("The book ___ on the table.", "is",
         ["are", "were"], "grammar"),
        ("She ___ read this novel last summer.", "didn't",
         ["doesn't", "don't"], "grammar"),
        ("If it rains, we ___ stay at home.", "will",
         ["would", "can"], "grammar"),
        ("The cake was ___ by my mother.", "made",
         ["make", "making"], "grammar"),
    ]
    rng.shuffle(grammar_qs)
    for sent, correct, wrongs, qtype in grammar_qs[:3]:
        qn += 1
        q_html += _make_mcq(qn, f"Complete: {sent}", correct, wrongs, rng, qtype)

    # Reading mini-passage + questions
    mini = rng.choice(_INFO_TEXTS)
    mini_sents = mini["text"][:5]
    mini_filled = " ".join(mini_sents)
    qn += 1
    q_html += _make_mcq(qn, f"Read: \"{mini_sents[0]}\" — What is this text about?",
                        f"It's about {mini['category']}.",
                        ["It's about cooking recipes.", "It's about fashion trends."],
                        rng, "reading")

    # True/False
    if len(mini_sents) > 1:
        qn += 1
        q_html += _make_tf(qn, mini_sents[1], True)
    qn += 1
    q_html += _make_tf(qn, _fill("The text says {name} won a gold medal.", rng, vocab), False)

    # Fill remaining with mixed
    while qn < cfg["checkpoint_q"]:
        qn += 1
        gq = grammar_qs[min(qn % len(grammar_qs), len(grammar_qs) - 1)]
        q_html += _make_mcq(qn, f"Complete: {gq[0]}", gq[1], gq[2], rng, gq[3])

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>

    <div class="checkpoint-header">
        <h2>📋 Unit Checkpoint</h2>
        <p>Week {week} • {theme} • {cfg['label']} ({cfg['cefr']})</p>
    </div>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%;"></div></div>

    {q_html}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Review & Assessment
# ══════════════════════════════════════════════════════════════════════════════

def _build_review_page(vocab: list, theme: str, theme_tr: str,
                       grade: int, week: int, cfg: dict, seed: int) -> str:
    rng = random.Random(seed + 4)

    q_html = ""
    qn = 0

    # Section A: Reading comprehension
    tmpl = rng.choice(_PASSAGE_TEMPLATES)
    max_s = min(6, cfg["passage_sentences"])
    sentences = [_fill(s, rng, vocab) for s in tmpl["sentences"][:max_s]]
    full = " ".join(sentences)

    passage_html = ""
    for i, s in enumerate(sentences):
        passage_html += f"""<div class="passage-line" onclick="speakNormal('{_js_safe(s)}')">
            <span class="line-num">{i+1}</span>{s}</div>"""

    q_html += f"""
    <div class="card">
        <div class="card-title">{tmpl['emoji']} Section A: Reading</div>
        {passage_html}
        <div style="text-align:center;margin-top:8px;">
            <button class="btn btn-speak" onclick="speakNormal('{_js_safe(full)}')">🔊 Listen</button>
        </div>
    </div>"""

    # Questions about the passage
    qn += 1
    q_html += _make_mcq(qn, "What is the passage mainly about?",
                        f"About {tmpl['category']}.",
                        ["About building houses.", "About cooking Italian food."],
                        rng, "main idea")

    if len(sentences) > 2:
        qn += 1
        q_html += _make_tf(qn, sentences[1], True)

    qn += 1
    q_html += _make_tf(qn, _fill("{name} went to space in the story.", rng, vocab), False)

    qn += 1
    q_html += _make_mcq(qn, "What can we understand from the text?",
                        "The topic is relevant to daily life.",
                        ["The text is about a fairy tale.", "Nothing happened in the story."],
                        rng, "inference")

    # Section B: Vocabulary
    q_html += f"""<div class="card" style="border-left-color:#FF9800;">
        <div class="card-title">📝 Section B: Vocabulary</div></div>"""

    vocab_qs = [
        ("Choose the correct word: I ___ very happy today.", "am", ["is", "are"]),
        ("The opposite of 'hot' is ___.", "cold", ["warm", "fast"]),
        ("Choose the synonym of 'big':", "large", ["small", "thin"]),
        ("'Quickly' means:", "in a fast way", ["slowly", "carefully"]),
        ("She speaks English ___.", "fluently", ["heavy", "bright"]),
        ("The ___ is shining brightly today.", "sun", ["moon", "rain"]),
    ]
    rng.shuffle(vocab_qs)
    for sent, correct, wrongs in vocab_qs[:3]:
        qn += 1
        q_html += _make_mcq(qn, sent, correct, wrongs, rng, "vocabulary")

    # Section C: Grammar
    q_html += f"""<div class="card" style="border-left-color:#4CAF50;">
        <div class="card-title">🧩 Section C: Grammar</div></div>"""

    grammar_review = [
        ("They ___ to the cinema last night.", "went", ["go", "goes"]),
        ("She has ___ her homework.", "finished", ["finish", "finishing"]),
        ("We ___ playing when it started to rain.", "were", ["was", "are"]),
        ("He ___ study harder if he wants to pass.", "must", ["can", "might"]),
        ("The letter ___ written by my sister.", "was", ["is", "were"]),
        ("I ___ been waiting for an hour.", "have", ["has", "had"]),
    ]
    rng.shuffle(grammar_review)
    for sent, correct, wrongs in grammar_review[:3]:
        qn += 1
        q_html += _make_mcq(qn, f"Complete: {sent}", correct, wrongs, rng, "grammar")

    # Section D: Dialog
    q_html += f"""<div class="card" style="border-left-color:#9C27B0;">
        <div class="card-title">💬 Section D: Functional Language</div></div>"""

    func_qs = [
        ("A: 'How are you?' — B: '___'", "I'm fine, thanks.",
         ["It's Monday.", "I like pizza."]),
        ("A: 'Can I help you?' — B: '___'", "Yes, please.",
         ["No, I'm a student.", "It's 3 o'clock."]),
        ("A: 'What time is it?' — B: '___'", "It's half past ten.",
         ["I'm 12 years old.", "It's sunny."]),
    ]
    rng.shuffle(func_qs)
    for sent, correct, wrongs in func_qs[:min(2, cfg["review_q"] - qn)]:
        qn += 1
        q_html += _make_mcq(qn, sent, correct, wrongs, rng, "functional")

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css(cfg)}{_tts_script()}</head><body>

    <div class="checkpoint-header">
        <h2>📝 Review & Assessment</h2>
        <p>Week {week} • {theme} • {cfg['label']} ({cfg['cefr']}) — Full Review Test</p>
    </div>

    <div class="score-bar" id="scoreDisplay">Score: 0/0 (0%)</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%;"></div></div>

    {q_html}
    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

_PAGE_NAMES = [
    "📖 Reading Passage",
    "💬 Dialog & Info",
    "🔍 Comprehension",
    "📋 Checkpoint",
    "📝 Review Test",
]


def build_reading_checkpoint_pages(grade: int, week_num: int,
                                    curriculum_weeks: list) -> list[str]:
    """Build 5 Reading & Checkpoint pages for a given grade/week."""
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    cfg = _GRADE_CFG.get(grade, _GRADE_CFG[5])
    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    theme_tr = week_data.get("theme_tr", "")
    seed = _deterministic_seed(grade, week_num)

    return [
        _build_passage_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_dialog_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_comprehension_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_checkpoint_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
        _build_review_page(vocab, theme, theme_tr, grade, week_num, cfg, seed),
    ]


def build_full_reading_checkpoint(grade: int, curriculum_weeks: list,
                                   selected_weeks: list[int] | None = None) -> list[dict]:
    """Build complete Reading & Checkpoint book for all weeks."""
    result = []
    for w in curriculum_weeks:
        wn = w.get("week", 0)
        if selected_weeks and wn not in selected_weeks:
            continue
        pages = build_reading_checkpoint_pages(grade, wn, curriculum_weeks)
        if pages:
            result.append({
                "week": wn,
                "theme": w.get("theme", f"Week {wn}"),
                "pages": pages,
            })
    return result
