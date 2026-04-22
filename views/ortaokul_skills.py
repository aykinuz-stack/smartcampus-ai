"""
Skill-Based Interactive Content Builders (Grade 1-8)
=====================================================
International Language Model — CEFR A1.1→A2.4
10 skill areas: Listening, Speaking, Reading, Writing,
Grammar, Vocabulary, Pronunciation, Spelling,
Functional Language, Communication Strategies

Each builder returns self-contained HTML/JS/CSS.
"""

from __future__ import annotations
import json as _json
from pathlib import Path as _Path

# ── JSON veri yukleyici ──
_DATA_DIR = _Path(__file__).resolve().parent.parent / "data" / "english"


def _load_json(name: str) -> dict:
    """Load a JSON data file from data/english/."""
    fp = _DATA_DIR / f"{name}.json"
    if fp.exists():
        with open(fp, "r", encoding="utf-8") as f:
            return _json.load(f)
    return {}

# ── Grade-level CEFR config ──
_GRADE_CFG = {
    "1": {"cefr": "A1.1", "label": "Baslangic", "color": "#e91e63"},
    "2": {"cefr": "A1.1", "label": "Baslangic+", "color": "#9c27b0"},
    "3": {"cefr": "A1.2", "label": "Temel", "color": "#673ab7"},
    "4": {"cefr": "A1.3", "label": "Temel+", "color": "#3f51b5"},
    "5": {"cefr": "A2.1", "label": "Temel Iletisim", "color": "#4caf50"},
    "6": {"cefr": "A2.2", "label": "Gelisim", "color": "#2196f3"},
    "7": {"cefr": "A2.3", "label": "Pekistirme", "color": "#ff9800"},
    "8": {"cefr": "A2.4", "label": "Tamamlama", "color": "#f44336"},
    "9": {"cefr": "B1.1", "label": "Bagimsiz Baslangic", "color": "#00897b"},
    "10": {"cefr": "B1.2", "label": "Bagimsiz Gelisim", "color": "#5c6bc0"},
    "11": {"cefr": "B1.3", "label": "Bagimsiz Pekistirme", "color": "#8e24aa"},
    "12": {"cefr": "B1.4", "label": "Bagimsiz Tamamlama", "color": "#c62828"},
}

# ── TIER 2.2: MEB Unite Eslestirmesi ──
_MEB_UNITS = {
    "1": [
        {"unit": 1, "theme": "Hello", "topics": "Greetings, introductions, colours"},
        {"unit": 2, "theme": "My Classroom", "topics": "School objects, numbers 1-20"},
        {"unit": 3, "theme": "My Family", "topics": "Family members, descriptions"},
        {"unit": 4, "theme": "Animals", "topics": "Pets, farm animals, wild animals"},
        {"unit": 5, "theme": "My Body", "topics": "Body parts, actions"},
        {"unit": 6, "theme": "Fruits & Vegetables", "topics": "Food, likes/dislikes"},
        {"unit": 7, "theme": "Toys & Games", "topics": "Toys, play, have/has"},
        {"unit": 8, "theme": "Weather", "topics": "Weather, seasons, clothes"},
        {"unit": 9, "theme": "My House", "topics": "Rooms, furniture"},
        {"unit": 10, "theme": "Jobs", "topics": "Professions, what do you do"},
    ],
    "2": [
        {"unit": 1, "theme": "My Friends", "topics": "Describing people, adjectives"},
        {"unit": 2, "theme": "My Town", "topics": "Places, directions, prepositions"},
        {"unit": 3, "theme": "Sports & Hobbies", "topics": "Can/can't, free time activities"},
        {"unit": 4, "theme": "My Daily Routine", "topics": "Daily activities, time"},
        {"unit": 5, "theme": "Health", "topics": "Illnesses, advice, should"},
        {"unit": 6, "theme": "At the Fair", "topics": "Fun activities, want to"},
        {"unit": 7, "theme": "Holidays", "topics": "Celebrations, past simple intro"},
        {"unit": 8, "theme": "My Neighbourhood", "topics": "Community, there is/are"},
        {"unit": 9, "theme": "Shopping", "topics": "Clothes, prices, how much"},
        {"unit": 10, "theme": "Technology", "topics": "Devices, present continuous"},
    ],
    "3": [
        {"unit": 1, "theme": "Appearance", "topics": "Physical descriptions, comparisons"},
        {"unit": 2, "theme": "Biographies", "topics": "Famous people, past simple"},
        {"unit": 3, "theme": "Sports", "topics": "Sports events, superlatives"},
        {"unit": 4, "theme": "Wild Animals", "topics": "Habitats, abilities, must/mustn't"},
        {"unit": 5, "theme": "Television", "topics": "TV shows, preferences"},
        {"unit": 6, "theme": "Celebrations", "topics": "Festivals, traditions, will/going to"},
        {"unit": 7, "theme": "Dreams", "topics": "Future plans, would like to"},
        {"unit": 8, "theme": "Public Buildings", "topics": "City places, asking directions"},
        {"unit": 9, "theme": "Environment", "topics": "Nature, recycling, should/shouldn't"},
        {"unit": 10, "theme": "Planets", "topics": "Solar system, space facts"},
    ],
    "4": [
        {"unit": 1, "theme": "My Daily Routine", "topics": "Routines, adverbs of frequency"},
        {"unit": 2, "theme": "Yummy Breakfast", "topics": "Food, countable/uncountable"},
        {"unit": 3, "theme": "Games & Hobbies", "topics": "Free time, like + gerund"},
        {"unit": 4, "theme": "In The City", "topics": "Transport, directions, prepositions"},
        {"unit": 5, "theme": "Fun with Science", "topics": "Experiments, imperatives"},
        {"unit": 6, "theme": "My House", "topics": "Rooms, furniture, there is/are"},
        {"unit": 7, "theme": "Jobs", "topics": "Occupations, would like to be"},
        {"unit": 8, "theme": "Clothes & Weather", "topics": "Seasons, clothes, present continuous"},
        {"unit": 9, "theme": "Animal Shelter", "topics": "Animals, past simple"},
        {"unit": 10, "theme": "Festivals", "topics": "Celebrations, traditions, culture"},
    ],
    "5": [
        {"unit": 1, "theme": "Hello!", "topics": "Meeting people, nationalities"},
        {"unit": 2, "theme": "My Town", "topics": "Places, giving directions"},
        {"unit": 3, "theme": "Games & Hobbies", "topics": "Likes, dislikes, frequency adverbs"},
        {"unit": 4, "theme": "My Daily Routine", "topics": "Telling time, daily activities"},
        {"unit": 5, "theme": "Health", "topics": "Illnesses, giving advice"},
        {"unit": 6, "theme": "Movies", "topics": "Types of movies, adjectives"},
        {"unit": 7, "theme": "Party Time", "topics": "Making suggestions, invitations"},
        {"unit": 8, "theme": "Fitness", "topics": "Sports, abilities, comparisons"},
        {"unit": 9, "theme": "Animal Shelter", "topics": "Animals, descriptions, must/mustn't"},
        {"unit": 10, "theme": "Festivals", "topics": "Cultural events, traditions"},
    ],
    "6": [
        {"unit": 1, "theme": "Life", "topics": "Personal information, present simple"},
        {"unit": 2, "theme": "Yummy Breakfast", "topics": "Food, countable/uncountable, some/any"},
        {"unit": 3, "theme": "Downtown", "topics": "City, directions, prepositions of place"},
        {"unit": 4, "theme": "Weather & Emotions", "topics": "Weather, feelings, present continuous"},
        {"unit": 5, "theme": "At the Fair", "topics": "Fun activities, can/can't"},
        {"unit": 6, "theme": "Occupations", "topics": "Jobs, daily routines, would like"},
        {"unit": 7, "theme": "Holidays", "topics": "Past events, past simple regular"},
        {"unit": 8, "theme": "Bookworms", "topics": "Books, past simple irregular"},
        {"unit": 9, "theme": "Saving the Planet", "topics": "Environment, should/shouldn't"},
        {"unit": 10, "theme": "Democracy", "topics": "Rights, responsibilities, modals"},
    ],
    "7": [
        {"unit": 1, "theme": "Appearance & Personality", "topics": "Describing people, comparatives"},
        {"unit": 2, "theme": "Sports", "topics": "Sports, superlatives"},
        {"unit": 3, "theme": "Biographies", "topics": "Past simple, time expressions"},
        {"unit": 4, "theme": "Wild Animals", "topics": "Habitats, present simple passive"},
        {"unit": 5, "theme": "Television", "topics": "Preferences, conjunctions"},
        {"unit": 6, "theme": "Celebrations", "topics": "Festivals, going to future"},
        {"unit": 7, "theme": "Dreams", "topics": "Future plans, will/won't"},
        {"unit": 8, "theme": "Public Buildings", "topics": "Directions, imperatives"},
        {"unit": 9, "theme": "Environment", "topics": "Recycling, obligation, must"},
        {"unit": 10, "theme": "Planets", "topics": "Space, past continuous"},
    ],
    "8": [
        {"unit": 1, "theme": "Friendship", "topics": "Personality, present perfect"},
        {"unit": 2, "theme": "Teen Life", "topics": "Preferences, used to"},
        {"unit": 3, "theme": "Cooking", "topics": "Food, recipes, imperatives, sequence"},
        {"unit": 4, "theme": "Communication", "topics": "Technology, present perfect continuous"},
        {"unit": 5, "theme": "The Internet", "topics": "Online safety, relative clauses"},
        {"unit": 6, "theme": "Adventures", "topics": "Travel, past experiences"},
        {"unit": 7, "theme": "Tourism", "topics": "Countries, passive voice"},
        {"unit": 8, "theme": "Chores", "topics": "Housework, too/enough"},
        {"unit": 9, "theme": "Science", "topics": "Inventions, if clauses type 1"},
        {"unit": 10, "theme": "Natural Forces", "topics": "Disasters, reported speech"},
    ],
    "9": [
        {"unit": 1, "theme": "Studying Abroad", "topics": "Education, future plans, present perfect"},
        {"unit": 2, "theme": "My Environment", "topics": "Environment, conditionals type 2"},
        {"unit": 3, "theme": "Movies", "topics": "Film genres, passive voice, reviews"},
        {"unit": 4, "theme": "Human in Nature", "topics": "Natural world, relative clauses"},
        {"unit": 5, "theme": "Inspirational People", "topics": "Biographies, past perfect"},
        {"unit": 6, "theme": "Bridging Cultures", "topics": "Cultural diversity, wish clauses"},
        {"unit": 7, "theme": "World Heritage", "topics": "Historical sites, passive structures"},
        {"unit": 8, "theme": "Emergency & Health", "topics": "Health issues, modals of obligation"},
        {"unit": 9, "theme": "Invitations & Celebrations", "topics": "Social events, formal/informal register"},
        {"unit": 10, "theme": "Television & Social Media", "topics": "Media literacy, reported speech"},
    ],
    "10": [
        {"unit": 1, "theme": "School Life", "topics": "Education systems, present tenses review"},
        {"unit": 2, "theme": "Plans", "topics": "Future plans, be going to vs will"},
        {"unit": 3, "theme": "Legendary Figures", "topics": "Historical narratives, past tenses"},
        {"unit": 4, "theme": "Traditions", "topics": "Cultural practices, used to/would"},
        {"unit": 5, "theme": "Travel", "topics": "Tourism, conditionals type 1-2"},
        {"unit": 6, "theme": "Helpful Tips", "topics": "Advice, modals, gerunds/infinitives"},
        {"unit": 7, "theme": "Food & Festivals", "topics": "Cuisine, quantifiers, articles"},
        {"unit": 8, "theme": "Digital Era", "topics": "Technology, passive voice review"},
        {"unit": 9, "theme": "Modern Heroes", "topics": "Role models, relative clauses"},
        {"unit": 10, "theme": "Shopping", "topics": "Consumer culture, comparisons, too/enough"},
    ],
    "11": [
        {"unit": 1, "theme": "Future Jobs", "topics": "Career planning, future continuous/perfect"},
        {"unit": 2, "theme": "Hobbies & Skills", "topics": "Talents, gerunds/infinitives advanced"},
        {"unit": 3, "theme": "Hard Times", "topics": "Challenges, wish/if only, past perfect"},
        {"unit": 4, "theme": "What a Life!", "topics": "Life stories, narrative tenses"},
        {"unit": 5, "theme": "Back to the Past", "topics": "History, conditionals type 3"},
        {"unit": 6, "theme": "Open Your Heart", "topics": "Volunteering, causative structures"},
        {"unit": 7, "theme": "Facts About Turkey", "topics": "Geography, passive review"},
        {"unit": 8, "theme": "Sports", "topics": "Athletics, reported speech advanced"},
        {"unit": 9, "theme": "My Friends", "topics": "Relationships, defining/non-defining clauses"},
        {"unit": 10, "theme": "Values & Norms", "topics": "Ethics, modals of deduction"},
    ],
    "12": [
        {"unit": 1, "theme": "Music", "topics": "Music genres, present/past participles"},
        {"unit": 2, "theme": "Friendship", "topics": "Social bonds, mixed conditionals"},
        {"unit": 3, "theme": "Human Rights", "topics": "Rights, passive advanced, formal writing"},
        {"unit": 4, "theme": "Coming Soon", "topics": "Future predictions, future perfect continuous"},
        {"unit": 5, "theme": "Psychology", "topics": "Behavior, reported speech, inversion"},
        {"unit": 6, "theme": "Favors", "topics": "Requests, causative have/get"},
        {"unit": 7, "theme": "News Stories", "topics": "Media, headline grammar, indirect questions"},
        {"unit": 8, "theme": "Alternative Energy", "topics": "Sustainability, academic vocabulary"},
        {"unit": 9, "theme": "Technology", "topics": "Innovation, all tenses review"},
        {"unit": 10, "theme": "Dilemmas", "topics": "Decision-making, advanced modals, essay writing"},
    ],
}


def get_meb_units(grade: str) -> list:
    """Return MEB unit list for a grade."""
    return _MEB_UNITS.get(grade, [])

# ══════════════════════════════════════════════════════════════════════════════
# SHARED: Diamond Premium shell
# ══════════════════════════════════════════════════════════════════════════════

def _build_unit_bar(grade: str) -> str:
    """Build MEB unit theme tag bar for a grade."""
    units = _MEB_UNITS.get(grade, [])
    if not units:
        return ""
    tags = ""
    for u in units:
        unum = u["unit"]
        utopics = u["topics"]
        utheme = u["theme"]
        tags += (
            f"<span class='unit-tag' title='Unit {unum}: {utopics}'>"
            f"U{unum}: {utheme}</span>"
        )
    return (
        "<div class='unit-bar'>"
        "<div class='unit-label'>MEB Units / Themes</div>"
        f"{tags}</div>"
    )


def _shell(title: str, grade: str, body_html: str, extra_css: str = "", extra_js: str = "") -> str:
    """Wrap skill content in Diamond-themed responsive shell."""
    cfg = _GRADE_CFG.get(grade, _GRADE_CFG["5"])
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<style>"
        "*{margin:0;padding:0;box-sizing:border-box}"
        "body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;"
        "background:linear-gradient(135deg,#0a0a1a 0%,#1a1a3e 50%,#0d0d2b 100%);"
        "color:#e2e8f0;min-height:100vh;padding:16px}"
        ".shell-hdr{background:linear-gradient(135deg,#1e3a5f,#0d2137);border-radius:12px;"
        "padding:16px 20px;margin-bottom:16px;border:1px solid rgba(100,200,255,.15);"
        "display:flex;align-items:center;gap:14px}"
        f".shell-hdr .badge{{background:{cfg['color']};color:#fff;padding:4px 12px;"
        "border-radius:20px;font-size:.7rem;font-weight:700}}"
        ".shell-hdr h2{font-size:1.1rem;color:#e3f2fd;font-weight:700}"
        ".shell-hdr .sub{font-size:.75rem;color:#90caf9}"
        ".card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);"
        "border-radius:12px;padding:16px;margin-bottom:12px}"
        ".card h3{font-size:.95rem;color:#7dd3fc;margin-bottom:10px;font-weight:600}"
        ".btn{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:none;"
        "padding:10px 20px;border-radius:8px;cursor:pointer;font-weight:600;font-size:.85rem;"
        "transition:all .2s}"
        ".btn:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(37,99,235,.4)}"
        ".btn-sm{padding:6px 14px;font-size:.78rem;border-radius:6px}"
        ".btn-green{background:linear-gradient(135deg,#059669,#047857)}"
        ".btn-orange{background:linear-gradient(135deg,#d97706,#b45309)}"
        ".btn-purple{background:linear-gradient(135deg,#7c3aed,#6d28d9)}"
        ".tag{display:inline-block;padding:3px 10px;border-radius:12px;font-size:.7rem;"
        "font-weight:600;margin:2px}"
        ".tag-blue{background:rgba(59,130,246,.2);color:#93c5fd;border:1px solid rgba(59,130,246,.3)}"
        ".tag-green{background:rgba(16,185,129,.2);color:#6ee7b7;border:1px solid rgba(16,185,129,.3)}"
        ".grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}"
        ".grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}"
        ".opt{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);"
        "border-radius:8px;padding:10px 14px;cursor:pointer;transition:all .2s;text-align:center}"
        ".opt:hover{background:rgba(59,130,246,.15);border-color:rgba(59,130,246,.4)}"
        ".opt.correct{background:rgba(16,185,129,.2);border-color:#10b981}"
        ".opt.wrong{background:rgba(239,68,68,.2);border-color:#ef4444}"
        ".score-bar{background:rgba(255,255,255,.08);border-radius:20px;height:8px;overflow:hidden;margin:8px 0}"
        ".score-fill{height:100%;border-radius:20px;transition:width .5s}"
        ".fb{padding:10px 14px;border-radius:8px;margin-top:8px;font-size:.82rem}"
        ".fb-ok{background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);color:#6ee7b7}"
        ".fb-no{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.3);color:#fca5a5}"
        ".unit-bar{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);"
        "border-radius:10px;padding:10px 14px;margin-bottom:14px;overflow-x:auto;white-space:nowrap}"
        ".unit-tag{display:inline-block;padding:4px 10px;margin:2px 3px;border-radius:8px;"
        "font-size:.68rem;font-weight:600;cursor:default;border:1px solid rgba(255,255,255,.12);"
        "background:rgba(255,255,255,.06);color:#94a3b8;transition:all .2s}"
        ".unit-tag:hover{background:rgba(37,99,235,.15);border-color:rgba(37,99,235,.4);color:#93c5fd}"
        ".unit-label{font-size:.7rem;color:#64748b;font-weight:600;margin-bottom:6px;text-transform:uppercase;"
        "letter-spacing:.5px}"
        f"{extra_css}"
        "</style></head><body>"
        "<div class='shell-hdr'>"
        f"<div><h2>{title}</h2>"
        f"<div class='sub'>Grade {grade} — CEFR {cfg['cefr']} {cfg['label']}</div></div>"
        f"<div class='badge'>{cfg['cefr']}</div></div>"
        + _build_unit_bar(grade)
        + f"{body_html}"
        f"<script>{extra_js}</script>"
        "</body></html>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# 1. LISTENING
# ══════════════════════════════════════════════════════════════════════════════

_LISTENING_DATA = _load_json("listening_data")



def build_listening_html(grade: str, start_index: int = 0) -> str:
    """Interactive listening comprehension with TTS and MCQ."""
    data = _LISTENING_DATA.get(grade, _LISTENING_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    _tts_css = (
        ".tts-sent{transition:all .3s ease;border-radius:6px;padding:2px 4px;display:inline;position:relative}"
        ".tts-sent.active{background:linear-gradient(135deg,rgba(251,191,36,.22),rgba(245,158,11,.15));"
        "color:#fde68a;box-shadow:0 0 18px rgba(251,191,36,.25),0 0 35px rgba(251,191,36,.08);"
        "text-shadow:0 0 6px rgba(251,191,36,.3);padding:2px 6px}"
        ".tts-sent.active::before{content:'';position:absolute;left:-2px;top:0;bottom:0;width:3px;"
        "background:linear-gradient(180deg,#fbbf24,#f59e0b);border-radius:2px;"
        "box-shadow:0 0 8px rgba(251,191,36,.6)}"
        ".tts-sent.done{opacity:.45;transition:opacity .4s}"
    )
    body = (
        "<div class='card'>"
        "<h3>🎧 Listening Comprehension</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Click <b>Listen</b> to hear the passage, then answer the questions.</p>"
        "<div id='lArea'><div style='text-align:center;padding:40px;color:#94a3b8'>"
        "⏳ Loading listening content...</div></div></div>"
    )
    js = f"""
    (function(){{
    var DATA={json.dumps(data, ensure_ascii=False)};
    var ci={start_index},score=0,total=0;
    var _ttsSpans=[],_ttsCur=0,_ttsAbort=false,_ttsSpeaking=false;
    function _splitSent(txt){{
        var raw=txt.replace(/\\s+/g,' ').trim();
        var parts=raw.match(/[^.!?\\n]+[.!?]+[\\s]*/g);
        if(!parts)return[raw];
        var rest=raw;parts.forEach(function(p){{rest=rest.replace(p,'');}});
        if(rest.trim())parts.push(rest.trim());
        return parts.map(function(s){{return s.trim();}}).filter(function(s){{return s.length>0;}});
    }}
    function _wrapSentences(el,txt){{
        var sents=_splitSent(txt);
        var h='';sents.forEach(function(s,i){{h+='<span class="tts-sent" data-i="'+i+'">'+s+'</span> ';}});
        el.innerHTML=h;return Array.from(el.querySelectorAll('.tts-sent'));
    }}
    function _speakNext(){{
        if(_ttsAbort||_ttsCur>=_ttsSpans.length){{_finishTTS();return;}}
        _ttsSpans.forEach(function(el,i){{el.classList.remove('active');if(i<_ttsCur)el.classList.add('done');}});
        var sp=_ttsSpans[_ttsCur];sp.classList.add('active');sp.classList.remove('done');
        sp.scrollIntoView({{behavior:'smooth',block:'center'}});
        var u=new SpeechSynthesisUtterance(sp.textContent);u.lang='en-US';u.rate=window._ttsRate||0.85;
        u.onend=function(){{if(_ttsAbort)return;sp.classList.remove('active');sp.classList.add('done');_ttsCur++;_speakNext();}};
        speechSynthesis.speak(u);
    }}
    function _finishTTS(){{
        _ttsSpeaking=false;_ttsAbort=false;
        var b=document.getElementById('ttsBtn');if(b){{b.textContent='🔊 Listen';b.classList.remove('speaking');}}
        var st=document.getElementById('ttsStatus');if(st)st.textContent='';
        _ttsSpans.forEach(function(el){{el.classList.remove('active','done');}});
    }}
    function init(){{
        var area=document.getElementById('lArea');
        if(!area){{setTimeout(init,100);return;}}
        window._lArea=area;window._ttsRate=0.85;
        render();
    }}
    function render(){{
        var area=window._lArea;
        var d=DATA[ci];
        var h='<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px">'
        +'<button class="btn" id="ttsBtn" onclick="toggleSpeak()">🔊 Listen (Passage '+(ci+1)+'/'+DATA.length+')</button>'
        +'<select class="btn-sm" style="background:#94A3B8;color:#94a3b8;border:1px solid rgba(255,255,255,.15);border-radius:6px;padding:6px 8px;font-size:.78rem" onchange="window._ttsRate=parseFloat(this.value)">'
        +'<option value="0.65">🐢 Yavas</option><option value="0.85" selected>Normal</option>'
        +'<option value="1.0">Hizli</option><option value="1.2">Cok Hizli</option></select>'
        +'<span id="ttsStatus" style="font-size:.75rem;color:#94a3b8"></span></div>'
        +'<div id="passageText" style="background:rgba(255,255,255,.05);padding:14px;border-radius:10px;'
        +'margin-bottom:14px;font-size:.88rem;color:#cbd5e1;line-height:1.8">'+d.text+'</div>';
        d.qs.forEach(function(q,qi){{
            h+='<div class="card" id="q'+qi+'" style="margin-top:8px"><div style="font-weight:600;font-size:.88rem;margin-bottom:8px">'
            +(qi+1)+'. '+q.q+'</div><div class="grid2">';
            q.opts.forEach(function(o,oi){{
                h+='<div class="opt" onclick="checkAns('+qi+','+oi+','+q.ans+')" id="o'+qi+'_'+oi+'">'+o+'</div>';
            }});
            h+='</div><div id="fb'+qi+'" style="margin-top:6px"></div></div>';
        }});
        h+='<div id="nextArea" style="margin-top:14px"></div>';
        area.innerHTML=h;
    }}
    window.render=render;
    var answered={{}};
    var answeredCount=0;
    window.toggleSpeak=function(){{
        if(_ttsSpeaking){{_ttsAbort=true;speechSynthesis.cancel();_finishTTS();return;}}
        var el=document.getElementById('passageText');if(!el)return;
        _ttsSpans=_wrapSentences(el,DATA[ci].text);_ttsCur=0;_ttsAbort=false;_ttsSpeaking=true;
        var b=document.getElementById('ttsBtn');b.textContent='⏹ Stop';b.classList.add('speaking');
        _speakNext();
    }};
    window.checkAns=function(qi,oi,ans){{
        if(answered[qi])return;
        answered[qi]=true;answeredCount++;total++;
        var opts=document.querySelectorAll('#q'+qi+' .opt');
        for(var i=0;i<opts.length;i++){{opts[i].style.pointerEvents='none';if(i===ans)opts[i].classList.add('correct');}}
        if(oi===ans){{
            score++;
            document.getElementById('fb'+qi).innerHTML='<div class="fb fb-ok">✅ Correct!</div>';
        }}else{{
            document.getElementById('o'+qi+'_'+oi).classList.add('wrong');
            document.getElementById('fb'+qi).innerHTML='<div class="fb fb-no">❌ The correct answer is: '+DATA[ci].qs[qi].opts[ans]+'</div>';
        }}
        if(answeredCount===DATA[ci].qs.length){{
            var na=document.getElementById('nextArea');
            if(ci<DATA.length-1){{
                na.innerHTML='<button class="btn btn-green" onclick="nextPassage()">Next Passage ➜</button>'
                +'<span style="margin-left:12px;color:#94a3b8;font-size:.85rem">Score: '+score+'/'+total+'</span>';
            }}else{{
                na.innerHTML='<div class="fb fb-ok" style="font-size:1rem;text-align:center;padding:16px">'
                +'🏆 Finished! Final Score: '+score+'/'+total+'</div>';
            }}
        }}
    }};
    window.nextPassage=function(){{
        if(_ttsSpeaking){{_ttsAbort=true;speechSynthesis.cancel();_finishTTS();}}
        ci++;answered={{}};answeredCount=0;render();
    }};
    if(document.readyState==='loading'){{document.addEventListener('DOMContentLoaded',init);}}
    else{{init();}}
    }})();
    """
    return _shell("🎧 Listening Skills", grade, body, extra_css=_tts_css, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 2. SPEAKING
# ══════════════════════════════════════════════════════════════════════════════

_SPEAKING_DATA = _load_json("speaking_data")



def build_speaking_html(grade: str, start_index: int = 0) -> str:
    """Speaking practice with prompts, recording, and tongue twisters."""
    data = _SPEAKING_DATA.get(grade, _SPEAKING_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>🗣️ Speaking Practice</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Choose a topic, listen to the prompt, then record yourself!</p>"
        "<div id='spArea'><div style='text-align:center;padding:40px;color:#94a3b8'>"
        "⏳ Loading speaking content...</div></div></div>"
    )
    js = f"""
    (function(){{
    var DATA={json.dumps(data, ensure_ascii=False)};
    var selIdx={start_index};
    function init(){{
        var area=document.getElementById('spArea');
        if(!area){{setTimeout(init,100);return;}}
        window._spArea=area;
        render();
    }}
    function render(){{
        var area=window._spArea;
        var h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">';
        for(var i=0;i<DATA.prompts.length;i++){{
            var label=DATA.prompts[i].length>35?DATA.prompts[i].substring(0,32)+'...':DATA.prompts[i];
            h+='<button class="btn btn-sm'+(i===selIdx?' btn-green':'')+'" onclick="window._spSel('+i+')">'+(i+1)+'</button>';
        }}
        h+='</div>';
        var p=DATA.prompts[selIdx];
        h+='<div class="card"><div style="font-weight:700;font-size:.95rem;color:#fbbf24;margin-bottom:8px">🎯 Topic '+(selIdx+1)+'</div>';
        h+='<div style="background:rgba(255,255,255,.06);padding:12px;border-radius:8px;font-size:.92rem;'
        +'line-height:1.7;color:#e2e8f0;margin-bottom:10px">'+p+'</div>';
        h+='<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">'
        +'<button class="btn btn-purple" onclick="window._spSpeak()">🔊 Listen</button>'
        +'<button class="btn btn-sm btn-orange" onclick="window._spSpeak(0.7)">🐢 Slow</button>'
        +'<button class="btn btn-orange" id="recBtn" onclick="window._spRec()">🎤 Record</button>'
        +'<button class="btn btn-sm btn-purple" id="evalBtn" onclick="window._spEval()">🎯 Evaluate</button></div>'
        +'<div id="recStatus" style="margin-top:8px;font-size:.8rem;color:#94a3b8"></div>'
        +'<div id="evalArea"></div>'
        +'</div>';
        h+='<div class="card" style="margin-top:12px"><div style="font-weight:600;font-size:.88rem;color:#c4b5fd;margin-bottom:8px">'
        +'👅 Tongue Twisters — Speed Challenge</div>';
        for(var j=0;j<DATA.tongue_twisters.length;j++){{
            h+='<div style="background:rgba(255,255,255,.05);padding:10px 14px;border-radius:8px;margin-bottom:6px;'
            +'display:flex;justify-content:space-between;align-items:center">'
            +'<span style="font-size:.88rem;color:#e2e8f0">'+(j+1)+'. '+DATA.tongue_twisters[j]+'</span>'
            +'<button class="btn btn-sm" onclick="window._spTT('+j+')">🔊</button></div>';
        }}
        h+='</div>';
        area.innerHTML=h;
    }}
    window.render=render;
    window._spSel=function(i){{selIdx=i;render();}};
    window._spSpeak=function(rate){{
        var u=new SpeechSynthesisUtterance(DATA.prompts[selIdx]);
        u.lang='en-US';u.rate=rate||1;
        window.speechSynthesis.cancel();window.speechSynthesis.speak(u);
    }};
    window._spTT=function(i){{
        var u=new SpeechSynthesisUtterance(DATA.tongue_twisters[i]);
        u.lang='en-US';u.rate=0.9;
        window.speechSynthesis.cancel();window.speechSynthesis.speak(u);
    }};
    var recording=false,mediaRec=null,mediaStream=null;
    window._spRec=function(){{
        if(!recording){{
            navigator.mediaDevices.getUserMedia({{audio:true}}).then(function(s){{
                mediaStream=s;
                mediaRec=new MediaRecorder(s);
                var chunks=[];
                mediaRec.ondataavailable=function(e){{chunks.push(e.data);}};
                mediaRec.onstop=function(){{
                    var blob=new Blob(chunks,{{type:'audio/webm'}});
                    var url=URL.createObjectURL(blob);
                    var st=document.getElementById('recStatus');
                    if(st)st.innerHTML=
                    '<audio controls src="'+url+'" style="margin-top:6px"></audio>'
                    +'<div style="margin-top:4px;color:#6ee7b7">✅ Recording saved! Use 🎯 Evaluate below to check pronunciation.</div>';
                    s.getTracks().forEach(function(t){{t.stop();}});
                }};
                mediaRec.start();recording=true;
                document.getElementById('recBtn').textContent='⏹ Stop';
                document.getElementById('recBtn').className='btn btn-sm';
                document.getElementById('recStatus').textContent='🔴 Recording...';
            }}).catch(function(){{
                document.getElementById('recStatus').textContent='⚠️ Microphone access denied.';
            }});
        }}else{{
            mediaRec.stop();recording=false;
            document.getElementById('recBtn').textContent='🎤 Record';
            document.getElementById('recBtn').className='btn btn-orange';
        }}
    }};
    // TIER 3.2: Speech Recognition evaluation
    var SpeechRec=window.SpeechRecognition||window.webkitSpeechRecognition;
    var recognizing=false;
    window._spEval=function(){{
        if(!SpeechRec){{
            document.getElementById('evalArea').innerHTML='<div style="color:#f87171;font-size:.82rem">⚠️ Speech Recognition is not supported in this browser. Try Chrome.</div>';
            return;
        }}
        if(recognizing)return;
        var rec=new SpeechRec();
        rec.lang='en-US';rec.interimResults=false;rec.maxAlternatives=3;rec.continuous=false;
        recognizing=true;
        var evalBtn=document.getElementById('evalBtn');
        if(evalBtn){{evalBtn.textContent='🎤 Listening...';evalBtn.className='btn btn-sm';}}
        document.getElementById('evalArea').innerHTML='<div style="color:#fbbf24;font-size:.82rem;margin-top:6px">🎤 Speak the text now...</div>';
        rec.onresult=function(e){{
            recognizing=false;
            if(evalBtn){{evalBtn.textContent='🎯 Evaluate';evalBtn.className='btn btn-sm btn-purple';}}
            var transcript=e.results[0][0].transcript.toLowerCase().trim();
            var confidence=Math.round(e.results[0][0].confidence*100);
            var target=DATA.prompts[selIdx].replace(/<[^>]+>/g,'').replace(/[\\u201C\\u201D\\u0022]/g,'').toLowerCase().trim();
            // Word comparison
            var targetWords=target.split(/\\s+/).map(function(w){{return w.replace(/[^a-z0-9']/g,'');}}).filter(function(w){{return w.length>0;}});
            var spokenWords=transcript.split(/\\s+/).map(function(w){{return w.replace(/[^a-z0-9']/g,'');}}).filter(function(w){{return w.length>0;}});
            var matched=0;var matchMap={{}};
            targetWords.forEach(function(tw,i){{
                for(var j=0;j<spokenWords.length;j++){{
                    if(!matchMap[j]&&(spokenWords[j]===tw||_sim(spokenWords[j],tw)>0.7)){{matchMap[j]=true;matched++;break;}}
                }}
            }});
            var accuracy=targetWords.length>0?Math.round(matched/targetWords.length*100):0;
            var score=Math.round((accuracy*0.6+confidence*0.4));
            var clr=score>=80?'#10b981':score>=60?'#fbbf24':score>=40?'#f97316':'#ef4444';
            var stars=score>=90?'⭐⭐⭐':score>=70?'⭐⭐':score>=40?'⭐':'';
            // Highlighted comparison
            var hlWords=targetWords.map(function(tw){{
                var found=false;
                for(var j=0;j<spokenWords.length;j++){{
                    if(spokenWords[j]===tw||_sim(spokenWords[j],tw)>0.7){{found=true;break;}}
                }}
                return found?'<span style="color:#10b981;font-weight:600">'+tw+'</span>'
                :'<span style="color:#ef4444;text-decoration:underline">'+tw+'</span>';
            }}).join(' ');
            var h='<div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:10px;padding:14px;margin-top:10px">';
            h+='<div style="font-weight:700;color:#10b981;font-size:.9rem;margin-bottom:10px">🎯 Pronunciation Result '+stars+'</div>';
            h+='<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">'
            +'<div style="font-size:2rem;font-weight:800;color:'+clr+'">'+score+'%</div>'
            +'<div style="flex:1"><div style="background:rgba(255,255,255,.1);border-radius:8px;height:10px;overflow:hidden">'
            +'<div style="background:'+clr+';height:100%;width:'+score+'%;border-radius:8px;transition:width .5s"></div></div>'
            +'<div style="display:flex;justify-content:space-between;margin-top:4px;font-size:.7rem;color:#94a3b8">'
            +'<span>Accuracy: '+accuracy+'%</span><span>Confidence: '+confidence+'%</span></div></div></div>';
            h+='<div style="font-size:.78rem;color:#7dd3fc;font-weight:600;margin-bottom:4px">Word Match:</div>'
            +'<div style="font-size:.85rem;line-height:1.8;padding:8px;background:rgba(255,255,255,.04);border-radius:8px;margin-bottom:8px">'+hlWords+'</div>';
            h+='<div style="font-size:.78rem;color:#94a3b8;margin-bottom:4px">You said: <span style="color:#e2e8f0;font-style:italic">"'+transcript+'"</span></div>';
            // Tips
            var tips=[];
            if(score>=80)tips.push('🌟 Excellent pronunciation!');
            else if(score>=60)tips.push('👍 Good job! Practice the red words.');
            else tips.push('💪 Keep practicing! Listen to the prompt again and try to match it.');
            if(accuracy<70)tips.push('Focus on the underlined words — they were missed or unclear.');
            h+='<div style="margin-top:8px">';
            tips.forEach(function(t){{h+='<div style="font-size:.78rem;color:#fbbf24;padding:2px 0">'+t+'</div>';}});
            h+='</div></div>';
            document.getElementById('evalArea').innerHTML=h;
        }};
        rec.onerror=function(e){{
            recognizing=false;
            if(evalBtn){{evalBtn.textContent='🎯 Evaluate';evalBtn.className='btn btn-sm btn-purple';}}
            var msg=e.error==='no-speech'?'No speech detected. Try again.':'Error: '+e.error;
            document.getElementById('evalArea').innerHTML='<div style="color:#f87171;font-size:.82rem;margin-top:6px">⚠️ '+msg+'</div>';
        }};
        rec.onend=function(){{
            recognizing=false;
            if(evalBtn&&evalBtn.textContent==='🎤 Listening...'){{
                evalBtn.textContent='🎯 Evaluate';evalBtn.className='btn btn-sm btn-purple';
            }}
        }};
        rec.start();
    }};
    // Levenshtein similarity
    function _sim(a,b){{
        if(a===b)return 1;
        var la=a.length,lb=b.length;
        if(!la||!lb)return 0;
        var mx=Math.max(la,lb);
        var d=Array(la+1);
        for(var i=0;i<=la;i++){{d[i]=Array(lb+1);d[i][0]=i;}}
        for(var j=0;j<=lb;j++)d[0][j]=j;
        for(var i=1;i<=la;i++)for(var j=1;j<=lb;j++){{
            d[i][j]=Math.min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]!==b[j-1]?1:0));
        }}
        return 1-d[la][lb]/mx;
    }}
    if(document.readyState==='loading'){{document.addEventListener('DOMContentLoaded',init);}}
    else{{init();}}
    }})();
    """
    return _shell("🗣️ Speaking Skills", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 3. READING
# ══════════════════════════════════════════════════════════════════════════════

_READING_DATA = _load_json("reading_data")



def build_reading_html(grade: str, start_index: int = 0) -> str:
    """Reading comprehension with passages, vocab highlights, and MCQ."""
    data = _READING_DATA.get(grade, _READING_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    _tts_css_r = (
        ".tts-sent{transition:all .3s ease;border-radius:6px;padding:2px 4px;display:inline;position:relative}"
        ".tts-sent.active{background:linear-gradient(135deg,rgba(251,191,36,.22),rgba(245,158,11,.15));"
        "color:#fde68a;box-shadow:0 0 18px rgba(251,191,36,.25),0 0 35px rgba(251,191,36,.08);"
        "text-shadow:0 0 6px rgba(251,191,36,.3);padding:2px 6px}"
        ".tts-sent.active::before{content:'';position:absolute;left:-2px;top:0;bottom:0;width:3px;"
        "background:linear-gradient(180deg,#fbbf24,#f59e0b);border-radius:2px;"
        "box-shadow:0 0 8px rgba(251,191,36,.6)}"
        ".tts-sent.done{opacity:.45;transition:opacity .4s}"
    )
    body = (
        "<div class='card'>"
        "<h3>📖 Reading Comprehension</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Read the passage carefully, then answer the questions below.</p>"
        "<div id='rArea'><div style='text-align:center;padding:40px;color:#94a3b8'>"
        "⏳ Loading reading content...</div></div></div>"
    )
    js = f"""
    (function(){{
    var DATA={json.dumps(data, ensure_ascii=False)};
    var ci={start_index},score=0,total=0;
    var _rSpans=[],_rCur=0,_rAbort=false,_rSpeaking=false;
    function _splitSent(txt){{
        var raw=txt.replace(/\\s+/g,' ').trim();
        var parts=raw.match(/[^.!?\\n]+[.!?]+[\\s]*/g);
        if(!parts)return[raw];
        var rest=raw;parts.forEach(function(p){{rest=rest.replace(p,'');}});
        if(rest.trim())parts.push(rest.trim());
        return parts.map(function(s){{return s.trim();}}).filter(function(s){{return s.length>0;}});
    }}
    function _wrapSent(el,txt){{
        var sents=_splitSent(txt);var h='';
        sents.forEach(function(s,i){{h+='<span class="tts-sent" data-i="'+i+'">'+s+'</span> ';}});
        el.innerHTML=h;return Array.from(el.querySelectorAll('.tts-sent'));
    }}
    function _rSpeakNext(){{
        if(_rAbort||_rCur>=_rSpans.length){{_rFinish();return;}}
        _rSpans.forEach(function(el,i){{el.classList.remove('active');if(i<_rCur)el.classList.add('done');}});
        var sp=_rSpans[_rCur];sp.classList.add('active');sp.classList.remove('done');
        sp.scrollIntoView({{behavior:'smooth',block:'center'}});
        var st=document.getElementById('rTtsStatus');if(st)st.textContent=(_rCur+1)+'/'+_rSpans.length;
        var u=new SpeechSynthesisUtterance(sp.textContent);u.lang='en-US';u.rate=window._rRate||0.85;
        u.onend=function(){{if(_rAbort)return;sp.classList.remove('active');sp.classList.add('done');_rCur++;_rSpeakNext();}};
        speechSynthesis.speak(u);
    }}
    function _rFinish(){{
        _rSpeaking=false;_rAbort=false;
        var b=document.getElementById('rTtsBtn');if(b){{b.textContent='🔊 Listen';b.classList.remove('speaking');}}
        var st=document.getElementById('rTtsStatus');if(st)st.textContent='';
        _rSpans.forEach(function(el){{el.classList.remove('active','done');}});
    }}
    function init(){{
        var area=document.getElementById('rArea');
        if(!area){{setTimeout(init,100);return;}}
        window._rArea=area;window._rRate=0.85;
        render();
    }}
    function render(){{
        var area=window._rArea;
        var d=DATA[ci];
        var h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">';
        for(var i=0;i<DATA.length;i++){{
            h+='<button class="btn btn-sm'+(i===ci?' btn-green':'')+'" onclick="switchPassage('+i+')">'
            +(i+1)+'. '+DATA[i].title+'</button>';
        }}
        h+='</div>';
        h+='<div style="background:rgba(255,255,255,.06);padding:16px;border-radius:10px;margin-bottom:14px">'
        +'<div style="display:flex;gap:8px;align-items:center;margin-bottom:10px">'
        +'<span style="font-weight:700;font-size:1rem;color:#fbbf24">📄 '+d.title+'</span>'
        +'<button class="btn btn-sm" id="rTtsBtn" onclick="rToggleTTS()" style="margin-left:auto">🔊 Listen</button>'
        +'<select class="btn-sm" style="background:#94A3B8;color:#94a3b8;border:1px solid rgba(255,255,255,.15);border-radius:6px;padding:4px 6px;font-size:.72rem" onchange="window._rRate=parseFloat(this.value)">'
        +'<option value="0.65">Yavas</option><option value="0.85" selected>Normal</option>'
        +'<option value="1.0">Hizli</option></select>'
        +'<span id="rTtsStatus" style="font-size:.72rem;color:#94a3b8"></span></div>'
        +'<div id="rPassageText" style="font-size:.88rem;color:#e2e8f0;line-height:1.8">'+d.text+'</div>';
        if(d.vocab){{
            h+='<div style="margin-top:10px;padding-top:8px;border-top:1px solid rgba(255,255,255,.1)">'
            +'<span style="font-size:.75rem;color:#7dd3fc;font-weight:600">📚 Vocabulary: </span>';
            for(var v=0;v<d.vocab.length;v++){{h+='<span class="tag tag-blue">'+d.vocab[v]+'</span> ';}}
            h+='</div>';
        }}
        h+='</div>';
        d.qs.forEach(function(q,qi){{
            h+='<div class="card" id="rq'+qi+'"><div style="font-weight:600;font-size:.88rem;margin-bottom:8px">'
            +(qi+1)+'. '+q.q+'</div><div class="grid2">';
            q.opts.forEach(function(o,oi){{
                h+='<div class="opt" onclick="rCheck('+qi+','+oi+','+q.ans+')" id="ro'+qi+'_'+oi+'">'+o+'</div>';
            }});
            h+='</div><div id="rfb'+qi+'"></div></div>';
        }});
        h+='<div style="margin-top:10px;text-align:center;font-size:.85rem;color:#94a3b8">Score: '+score+'/'+total+'</div>';
        area.innerHTML=h;
    }}
    window.render=render;
    var answered={{}};
    var answeredCount=0;
    window.rToggleTTS=function(){{
        if(_rSpeaking){{_rAbort=true;speechSynthesis.cancel();_rFinish();return;}}
        var el=document.getElementById('rPassageText');if(!el)return;
        _rSpans=_wrapSent(el,DATA[ci].text);_rCur=0;_rAbort=false;_rSpeaking=true;
        var b=document.getElementById('rTtsBtn');b.textContent='⏹ Stop';b.classList.add('speaking');
        _rSpeakNext();
    }};
    window.switchPassage=function(idx){{
        if(_rSpeaking){{_rAbort=true;speechSynthesis.cancel();_rFinish();}}
        ci=idx;answered={{}};answeredCount=0;render();
    }};
    window.rCheck=function(qi,oi,ans){{
        if(answered[qi])return;answered[qi]=true;answeredCount++;total++;
        var opts=document.querySelectorAll('#rq'+qi+' .opt');
        for(var i=0;i<opts.length;i++){{opts[i].style.pointerEvents='none';if(i===ans)opts[i].classList.add('correct');}}
        if(oi===ans){{score++;document.getElementById('rfb'+qi).innerHTML='<div class="fb fb-ok">✅ Correct!</div>';}}
        else{{document.getElementById('ro'+qi+'_'+oi).classList.add('wrong');
        document.getElementById('rfb'+qi).innerHTML='<div class="fb fb-no">❌ Correct: '+DATA[ci].qs[qi].opts[ans]+'</div>';}}
    }};
    if(document.readyState==='loading'){{document.addEventListener('DOMContentLoaded',init);}}
    else{{init();}}
    }})();
    """
    return _shell("📖 Reading Skills", grade, body, extra_css=_tts_css_r, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 4. WRITING
# ══════════════════════════════════════════════════════════════════════════════

_WRITING_DATA = _load_json("writing_data")



def build_writing_html(grade: str, start_index: int = 0) -> str:
    """Interactive writing workshop with guided prompts, feedback system, and self-check."""
    data = _WRITING_DATA.get(grade, _WRITING_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    # Grade-based word count targets
    _targets = {"1": 15, "2": 25, "3": 40, "4": 60, "5": 80, "6": 120, "7": 150, "8": 200}
    target_wc = _targets.get(grade, 80)
    body = (
        "<div class='card'>"
        "<h3>✍️ Writing Workshop</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Follow the prompts to write, then get instant feedback on your writing!</p>"
        "<div id='wArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const TARGET_WC={target_wc};
    const GRADE="{grade}";
    const area=document.getElementById('wArea');
    let ti={start_index},fbVisible=false,lastFeedback=null;
    function render(){{
        let h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">';
        DATA.tasks.forEach((t,i)=>{{
            h+='<button class="btn btn-sm'+(i===ti?' btn-green':'')+'" onclick="ti='+i+';fbVisible=false;lastFeedback=null;render()">'+t.title+'</button>';
        }});
        h+='</div>';
        const t=DATA.tasks[ti];
        h+='<div class="card"><div style="font-weight:700;color:#fbbf24;margin-bottom:10px">✏️ '+t.title+'</div>';
        if(t.hint){{h+='<div style="font-size:.78rem;color:#94a3b8;margin-bottom:8px;font-style:italic">💡 '+t.hint+'</div>';}}
        h+='<div style="font-size:.82rem;color:#7dd3fc;font-weight:600;margin-bottom:8px">Writing Guide:</div>';
        h+='<div style="background:rgba(255,255,255,.05);padding:12px;border-radius:8px;margin-bottom:12px">';
        t.prompts.forEach((p,i)=>{{
            h+='<div style="font-size:.85rem;color:#cbd5e1;padding:4px 0;border-bottom:1px dotted rgba(255,255,255,.1)">'
            +'<span style="color:#c4b5fd;font-weight:600">'+(i+1)+'.</span> '+p+'</div>';
        }});
        h+='</div>';
        h+='<textarea id="wText" style="width:100%;height:180px;background:rgba(255,255,255,.06);color:#e2e8f0;'
        +'border:1px solid rgba(255,255,255,.15);border-radius:8px;padding:12px;font-size:.88rem;resize:vertical;'
        +'font-family:inherit;line-height:1.7" placeholder="Start writing here..." oninput="liveCount()"></textarea>';
        h+='<div id="liveWC" style="font-size:.72rem;color:#64748b;margin-top:4px;text-align:right">0 / '+TARGET_WC+' words</div>';
        h+='<div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">'
        +'<button class="btn btn-sm btn-green" onclick="analyzeFeedback()">🤖 Get Feedback</button>'
        +'<button class="btn btn-sm" onclick="speakText()">🔊 Listen</button>'
        +'</div>';
        h+='<div id="fbArea"></div>';
        if(fbVisible&&lastFeedback){{h+='<script>setTimeout(function(){{document.getElementById("fbArea").innerHTML=lastFeedback}},50)</'+'script>';}}
        h+='</div>';
        area.innerHTML=h;
    }}
    function liveCount(){{
        const el=document.getElementById('wText');
        if(!el)return;
        const text=el.value.trim();
        const wc=text?text.split(/\\s+/).length:0;
        const lbl=document.getElementById('liveWC');
        if(lbl){{
            const pct=Math.min(100,Math.round(wc/TARGET_WC*100));
            const clr=pct>=100?'#10b981':pct>=60?'#fbbf24':'#94a3b8';
            lbl.innerHTML=wc+' / '+TARGET_WC+' words <span style="color:'+clr+';font-weight:600">('+pct+'%)</span>';
        }}
    }}
    function speakText(){{
        const text=document.getElementById('wText')?.value?.trim();
        if(!text)return;
        try{{window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=0.85;window.speechSynthesis.speak(u);}}catch(e){{}}
    }}
    function analyzeFeedback(){{
        const text=document.getElementById('wText')?.value?.trim();
        if(!text||text.length<3){{
            document.getElementById('fbArea').innerHTML='<div style="color:#f87171;font-size:.82rem;margin-top:8px">✏️ Please write something first!</div>';
            return;
        }}
        const words=text.split(/\\s+/);
        const wc=words.length;
        const sentences=text.split(/[.!?]+/).filter(s=>s.trim().length>0);
        const sc=sentences.length;
        const avgSL=sc>0?Math.round(wc/sc*10)/10:0;
        const uniqueW=new Set(words.map(w=>w.toLowerCase().replace(/[^a-z]/g,'')).filter(w=>w.length>0));
        const diversity=wc>0?Math.round(uniqueW.size/wc*100):0;
        // Capitalization check
        let capIssues=0;
        sentences.forEach(s=>{{const t=s.trim();if(t&&t[0]!==t[0].toUpperCase())capIssues++;}});
        // Punctuation check
        const lastChar=text[text.length-1];
        const endsOk=/[.!?]/.test(lastChar);
        // Common grammar patterns
        let grammarNotes=[];
        if(/\\bi\\b/.test(text))grammarNotes.push('"i" should be capitalized as "I"');
        if(/\\b(dont|doesnt|cant|wont|isnt|arent|didnt|hasnt|havent|shouldnt|wouldnt|couldnt)\\b/i.test(text))
            grammarNotes.push('Use apostrophes in contractions (don\\'t, doesn\\'t, can\\'t)');
        if(/\\b(me and|me and \\w+)\\b/i.test(text))grammarNotes.push('Consider "... and I" instead of "me and..."');
        if(/\\b(alot)\\b/i.test(text))grammarNotes.push('"alot" should be "a lot"');
        if(/\\b(becouse|becuz|becuse)\\b/i.test(text))grammarNotes.push('Spelling: "because"');
        if(/\\b(wich|witch)\\b/i.test(text)&&!/\\bwitch\\b/i.test(text))grammarNotes.push('Spelling: "which"');
        if(/\\b(thier|teh|hte)\\b/i.test(text))grammarNotes.push('Check for common typos');
        // Connectors check (higher grades)
        const connectors=['however','moreover','furthermore','therefore','although','nevertheless','in addition','on the other hand','firstly','secondly','in conclusion'];
        const usedConn=connectors.filter(c=>text.toLowerCase().includes(c));
        // Scoring
        let scores={{}};
        // Length score (0-25)
        scores.length=Math.min(25,Math.round(wc/TARGET_WC*25));
        // Structure score (0-25)
        let structScore=25;
        if(sc<2)structScore-=10;
        if(capIssues>0)structScore-=Math.min(8,capIssues*3);
        if(!endsOk)structScore-=5;
        scores.structure=Math.max(0,structScore);
        // Vocabulary score (0-25)
        scores.vocabulary=Math.min(25,Math.round(diversity/100*30));
        // Grammar score (0-25)
        scores.grammar=Math.max(0,25-grammarNotes.length*5);
        const total=scores.length+scores.structure+scores.vocabulary+scores.grammar;
        // Build feedback HTML
        let fb='<div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.25);border-radius:10px;padding:16px;margin-top:14px">';
        fb+='<div style="font-weight:700;color:#10b981;font-size:.95rem;margin-bottom:12px">🤖 Writing Feedback</div>';
        // Score bar
        const scoreClr=total>=80?'#10b981':total>=60?'#fbbf24':total>=40?'#f97316':'#ef4444';
        fb+='<div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">'
        +'<div style="font-size:1.8rem;font-weight:800;color:'+scoreClr+'">'+total+'</div>'
        +'<div style="flex:1"><div style="font-size:.72rem;color:#94a3b8;margin-bottom:3px">Overall Score</div>'
        +'<div style="background:rgba(255,255,255,.1);border-radius:8px;height:10px;overflow:hidden">'
        +'<div style="background:'+scoreClr+';height:100%;width:'+total+'%;border-radius:8px;transition:width .5s"></div></div></div></div>';
        // Category breakdown
        const cats=[
            {{name:'Length',score:scores.length,max:25,icon:'📏',clr:'#60a5fa'}},
            {{name:'Structure',score:scores.structure,max:25,icon:'🏗️',clr:'#c084fc'}},
            {{name:'Vocabulary',score:scores.vocabulary,max:25,icon:'📚',clr:'#fbbf24'}},
            {{name:'Grammar',score:scores.grammar,max:25,icon:'📝',clr:'#34d399'}}
        ];
        fb+='<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">';
        cats.forEach(c=>{{
            const pct=Math.round(c.score/c.max*100);
            fb+='<div style="background:rgba(255,255,255,.04);border-radius:8px;padding:8px 10px">'
            +'<div style="font-size:.72rem;color:#94a3b8">'+c.icon+' '+c.name+'</div>'
            +'<div style="display:flex;align-items:center;gap:6px;margin-top:3px">'
            +'<div style="flex:1;background:rgba(255,255,255,.08);border-radius:4px;height:5px">'
            +'<div style="background:'+c.clr+';height:100%;width:'+pct+'%;border-radius:4px"></div></div>'
            +'<span style="font-size:.72rem;font-weight:700;color:'+c.clr+'">'+c.score+'/'+c.max+'</span></div></div>';
        }});
        fb+='</div>';
        // Stats
        fb+='<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;font-size:.78rem;color:#cbd5e1">'
        +'<span>📊 '+wc+' words</span><span>📃 '+sc+' sentences</span>'
        +'<span>📐 Avg '+avgSL+' words/sentence</span><span>🔤 '+diversity+'% vocabulary diversity</span></div>';
        // Tips
        fb+='<div style="font-size:.8rem;font-weight:600;color:#7dd3fc;margin-bottom:6px">💡 Tips:</div>';
        let tips=[];
        if(wc<TARGET_WC)tips.push('Try to write at least '+TARGET_WC+' words (you have '+wc+').');
        if(sc<3)tips.push('Write more sentences to develop your ideas.');
        if(avgSL>20)tips.push('Some sentences are very long. Try to break them up.');
        if(avgSL<5&&sc>1)tips.push('Your sentences are quite short. Try combining some ideas.');
        if(capIssues>0)tips.push('Start each sentence with a capital letter ('+capIssues+' found).');
        if(!endsOk)tips.push('End your writing with a period (.), exclamation mark (!), or question mark (?).');
        if(diversity<40&&wc>10)tips.push('Try using more varied vocabulary — avoid repeating the same words.');
        if(parseInt(GRADE)>=5&&usedConn.length===0)tips.push('Use linking words: however, moreover, therefore, firstly...');
        if(parseInt(GRADE)>=5&&usedConn.length>0)tips.push('Good use of connectors: '+usedConn.join(', ')+'!');
        grammarNotes.forEach(g=>tips.push('⚠️ '+g));
        if(tips.length===0)tips.push('Excellent work! Keep writing to improve even further.');
        tips.forEach(t=>{{
            const isGood=t.includes('Good')||t.includes('Excellent');
            fb+='<div style="font-size:.78rem;color:'+(isGood?'#10b981':'#fbbf24')+';padding:2px 0">• '+t+'</div>';
        }});
        fb+='</div>';
        lastFeedback=fb;fbVisible=true;
        document.getElementById('fbArea').innerHTML=fb;
    }}
    render();
    """
    return _shell("✍️ Writing Skills", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 5. GRAMMAR
# ══════════════════════════════════════════════════════════════════════════════

_GRAMMAR_DATA = _load_json("grammar_data")



def build_grammar_html(grade: str, start_index: int = 0) -> str:
    """Interactive grammar exercises with rules, examples, and practice."""
    data = _GRAMMAR_DATA.get(grade, _GRAMMAR_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>📝 Grammar Practice</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Learn the rule, study examples, then test yourself!</p>"
        "<div id='gArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('gArea');
    let ti={start_index},score=0,total=0,answered=new Set();
    function render(){{
        let h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">';
        DATA.topics.forEach((t,i)=>{{
            h+='<button class="btn btn-sm'+(i===ti?' btn-green':'')+'" onclick="ti='+i+';score=0;total=0;answered=new Set();render()">'+t.name+'</button>';
        }});
        h+='</div>';
        const t=DATA.topics[ti];
        h+='<div style="background:rgba(37,99,235,.1);border:1px solid rgba(37,99,235,.25);border-radius:10px;padding:14px;margin-bottom:14px">'
        +'<div style="font-weight:700;color:#93c5fd;font-size:.9rem;margin-bottom:6px">📏 Rule</div>'
        +'<div style="font-size:.85rem;color:#e2e8f0;line-height:1.6">'+t.rule+'</div>'
        +'<div style="margin-top:10px;font-weight:600;color:#7dd3fc;font-size:.82rem">Examples:</div>';
        t.examples.forEach(e=>{{h+='<div style="font-size:.84rem;color:#cbd5e1;padding:3px 0">• '+e+'</div>';}});
        h+='</div>';
        h+='<div style="font-weight:600;color:#fbbf24;font-size:.9rem;margin-bottom:10px">🎯 Practice ('+score+'/'+total+')</div>';
        t.exercises.forEach((ex,qi)=>{{
            h+='<div class="card" id="gq'+qi+'" style="padding:12px"><div style="font-weight:600;font-size:.86rem;margin-bottom:8px">'
            +(qi+1)+'. '+ex.q+'</div><div style="display:flex;gap:8px;flex-wrap:wrap">';
            ex.opts.forEach((o,oi)=>{{
                h+='<div class="opt" style="flex:1;min-width:100px" onclick="gCheck('+qi+','+oi+','+ex.ans+')" id="go'+qi+'_'+oi+'">'+o+'</div>';
            }});
            h+='</div><div id="gfb'+qi+'"></div></div>';
        }});
        area.innerHTML=h;
    }}
    function gCheck(qi,oi,ans){{
        if(answered.has(qi))return;answered.add(qi);total++;
        const opts=document.querySelectorAll('#gq'+qi+' .opt');
        opts.forEach((o,i)=>{{o.style.pointerEvents='none';if(i===ans)o.classList.add('correct');}});
        if(oi===ans){{score++;document.getElementById('gfb'+qi).innerHTML='<div class="fb fb-ok">✅ Correct!</div>';}}
        else{{document.getElementById('go'+qi+'_'+oi).classList.add('wrong');
        document.getElementById('gfb'+qi).innerHTML='<div class="fb fb-no">❌ Correct: '+DATA.topics[ti].exercises[qi].opts[ans]+'</div>';}}
        if(answered.size===DATA.topics[ti].exercises.length)render();
    }}
    render();
    """
    return _shell("📝 Grammar", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 6. VOCABULARY
# ══════════════════════════════════════════════════════════════════════════════

_VOCAB_DATA = _load_json("vocabulary_data")



def build_vocabulary_html(grade: str, start_index: int = 0) -> str:
    """Vocabulary flashcards with categories, examples, and quiz mode."""
    data = _VOCAB_DATA.get(grade, _VOCAB_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>📚 Vocabulary Builder</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Learn words with flashcards, then test yourself in quiz mode!</p>"
        "<div id='vArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('vArea');
    let si={start_index},mode='cards',qi=0,qScore=0,qList=[];
    function render(){{
        let h='<div style="display:flex;gap:8px;margin-bottom:12px">';
        DATA.sets.forEach((s,i)=>{{h+='<button class="btn btn-sm'+(i===si?' btn-green':'')+'" onclick="si='+i+';mode=\\'cards\\';render()">'+s.cat+'</button>';}});
        h+='<button class="btn btn-sm btn-purple" onclick="startQuiz()">🎯 Quiz Mode</button></div>';
        if(mode==='cards'){{
            const s=DATA.sets[si];
            h+='<div class="grid2">';
            s.words.forEach((w,i)=>{{
                h+='<div class="card" style="cursor:pointer;text-align:center;transition:all .3s" onclick="flipCard('+i+')" id="vc'+i+'">'
                +'<div style="font-size:1.3rem;margin-bottom:4px" id="vcf'+i+'">'+w.en+'</div>'
                +'<div style="font-size:.75rem;color:#94a3b8" id="vcb'+i+'" style="display:none"></div>'
                +'<div style="font-size:.75rem;color:#64748b;margin-top:4px;font-style:italic" id="vce'+i+'"></div>'
                +'<button class="btn btn-sm" style="margin-top:6px" onclick="event.stopPropagation();speakW(\\''+w.en+'\\')">🔊</button></div>';
            }});
            h+='</div>';
        }}else{{
            h+=renderQuiz();
        }}
        area.innerHTML=h;
    }}
    function flipCard(i){{
        const w=DATA.sets[si].words[i];
        const b=document.getElementById('vcb'+i);
        const e=document.getElementById('vce'+i);
        if(b.textContent){{b.textContent='';e.textContent='';}}
        else{{b.textContent=w.tr;b.style.display='block';b.style.color='#fbbf24';b.style.fontWeight='600';
        e.textContent=w.ex;e.style.display='block';}}
    }}
    function speakW(w){{const u=new SpeechSynthesisUtterance(w);u.lang='en-US';u.rate=0.9;speechSynthesis.cancel();speechSynthesis.speak(u);}}
    function startQuiz(){{
        mode='quiz';qi=0;qScore=0;
        const words=DATA.sets[si].words;
        qList=words.map(w=>{{
            let wrong=words.filter(x=>x.tr!==w.tr).sort(()=>Math.random()-.5).slice(0,3).map(x=>x.tr);
            let opts=[w.tr,...wrong].sort(()=>Math.random()-.5);
            return{{en:w.en,correct:w.tr,opts:opts}};
        }}).sort(()=>Math.random()-.5);
        render();
    }}
    function renderQuiz(){{
        if(qi>=qList.length)return '<div class="fb fb-ok" style="text-align:center;padding:20px;font-size:1.1rem">'
        +'🏆 Quiz Complete! Score: '+qScore+'/'+qList.length+'</div>'
        +'<div style="text-align:center;margin-top:10px"><button class="btn" onclick="mode=\\'cards\\';render()">Back to Cards</button></div>';
        const q=qList[qi];
        let h='<div style="text-align:center;font-size:.82rem;color:#94a3b8;margin-bottom:8px">Question '+(qi+1)+'/'+qList.length+'</div>'
        +'<div style="text-align:center;font-size:1.3rem;font-weight:700;color:#e2e8f0;margin-bottom:16px">'+q.en+'</div>'
        +'<div style="text-align:center;font-size:.85rem;color:#7dd3fc;margin-bottom:12px">What is the Turkish meaning?</div>'
        +'<div class="grid2">';
        q.opts.forEach((o,i)=>{{
            h+='<div class="opt" onclick="quizAns('+i+')">'+o+'</div>';
        }});
        h+='</div><div id="qfb" style="margin-top:8px"></div>';
        return h;
    }}
    function quizAns(i){{
        const q=qList[qi];
        const opts=document.querySelectorAll('.opt');
        opts.forEach((o,j)=>{{o.style.pointerEvents='none';if(o.textContent===q.correct)o.classList.add('correct');}});
        if(q.opts[i]===q.correct){{qScore++;document.getElementById('qfb').innerHTML='<div class="fb fb-ok">✅ Correct!</div>';}}
        else{{opts[i].classList.add('wrong');document.getElementById('qfb').innerHTML='<div class="fb fb-no">❌ '+q.correct+'</div>';}}
        setTimeout(()=>{{qi++;render();}},1200);
    }}
    render();
    """
    return _shell("📚 Vocabulary", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 7. PRONUNCIATION
# ══════════════════════════════════════════════════════════════════════════════

_PRONUN_DATA = _load_json("pronunciation_data")


def build_pronunciation_html(grade: str, start_index: int = 0) -> str:
    """Pronunciation practice: minimal pairs, word stress, TTS comparison."""
    data = _PRONUN_DATA.get(grade, _PRONUN_DATA["5"])
    import json
    body = (
        "<div class='card'>"
        "<h3>🔤 Pronunciation Lab</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Listen to minimal pairs, practise word stress, and improve your pronunciation!</p>"
        "<div id='pArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('pArea');
    function render(){{
        let h='<div style="font-weight:700;color:#fbbf24;font-size:.92rem;margin-bottom:10px">👂 Minimal Pairs — Listen & Compare</div>';
        DATA.pairs.forEach(p=>{{
            h+='<div class="card"><div style="font-weight:600;color:#7dd3fc;margin-bottom:8px">'+p.title+'</div><div class="grid2">';
            p.pairs.forEach(pair=>{{
                if(typeof pair[0]==='string'){{
                    const w1=pair[0].split(' ')[0],w2=pair[1].split(' ')[0];
                    h+='<div style="display:flex;gap:6px;align-items:center;margin-bottom:6px">'
                    +'<button class="btn btn-sm" onclick="say(\\''+w1+'\\')">🔊</button>'
                    +'<span style="font-size:.88rem;color:#e2e8f0">'+pair[0]+'</span>'
                    +'<span style="color:#475569;margin:0 4px">vs</span>'
                    +'<button class="btn btn-sm" onclick="say(\\''+w2+'\\')">🔊</button>'
                    +'<span style="font-size:.88rem;color:#e2e8f0">'+pair[1]+'</span></div>';
                }}
            }});
            h+='</div></div>';
        }});
        h+='<div style="font-weight:700;color:#fbbf24;font-size:.92rem;margin:16px 0 10px">🎯 Word Stress Practice</div>';
        h+='<div class="grid2">';
        DATA.stress.forEach(s=>{{
            h+='<div class="card" style="text-align:center">'
            +'<div style="font-size:1.1rem;font-weight:700;color:#e2e8f0">'+s.word+'</div>'
            +'<div style="font-size:.85rem;color:#c4b5fd;margin:4px 0">'+s.stress+'</div>'
            +'<div style="font-size:1.2rem;letter-spacing:4px;margin:4px 0">'
            +s.pattern.split('').map(c=>c==='O'?'<span style="color:#fbbf24;font-weight:800">●</span>':'<span style="color:#475569">○</span>').join('')
            +'</div>'
            +'<button class="btn btn-sm" style="margin-top:6px" onclick="say(\\''+s.word+'\\',0.8)">🔊 Listen</button></div>';
        }});
        h+='</div>';
        area.innerHTML=h;
    }}
    function say(w,rate){{const u=new SpeechSynthesisUtterance(w);u.lang='en-US';u.rate=rate||0.9;speechSynthesis.cancel();speechSynthesis.speak(u);}}
    render();
    """
    return _shell("🔤 Pronunciation", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 8. SPELLING
# ══════════════════════════════════════════════════════════════════════════════

_SPELLING_DATA = _load_json("spelling_data")


def build_spelling_html(grade: str, start_index: int = 0) -> str:
    """Spelling bee with dictation, word building, and pattern recognition."""
    data = _SPELLING_DATA.get(grade, _SPELLING_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>✏️ Spelling Bee</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Listen to the word, then type the correct spelling!</p>"
        "<div id='sArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('sArea');
    let wi={start_index},score=0,mode='bee';
    function render(){{
        let h='<div style="display:flex;gap:8px;margin-bottom:14px">'
        +'<button class="btn btn-sm'+(mode==='bee'?' btn-green':'')+'" onclick="mode=\\'bee\\';wi=0;score=0;render()">🐝 Spelling Bee</button>'
        +'<button class="btn btn-sm'+(mode==='rules'?' btn-green':'')+'" onclick="mode=\\'rules\\';render()">📏 Spelling Rules</button></div>';
        if(mode==='bee'){{
            h+='<div style="text-align:center;font-size:.82rem;color:#94a3b8;margin-bottom:8px">Word '+(wi+1)+'/'+DATA.words.length+'  |  Score: '+score+'</div>';
            h+='<div style="text-align:center;margin-bottom:16px">'
            +'<button class="btn btn-purple" onclick="sayWord()">🔊 Listen to the Word</button>'
            +'<button class="btn btn-sm btn-orange" style="margin-left:8px" onclick="sayWord(0.6)">🐢 Slow</button></div>';
            h+='<div style="text-align:center;margin-bottom:12px">'
            +'<input type="text" id="spInput" style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);'
            +'border-radius:8px;padding:12px 20px;font-size:1.1rem;color:#e2e8f0;text-align:center;width:300px;'
            +'font-family:monospace" placeholder="Type the word..." autocomplete="off" '
            +'onkeydown="if(event.key===\\'Enter\\')checkSpelling()">'
            +'</div><div style="text-align:center">'
            +'<button class="btn" onclick="checkSpelling()">Check ✓</button></div>'
            +'<div id="spFb" style="margin-top:10px;text-align:center"></div>';
            h+='<div class="score-bar"><div class="score-fill" style="width:'+(DATA.words.length>0?(score/DATA.words.length*100):0)
            +'%;background:linear-gradient(90deg,#10b981,#34d399)"></div></div>';
        }}else{{
            DATA.rules.forEach(r=>{{
                h+='<div class="card"><div style="font-weight:600;color:#fbbf24;margin-bottom:6px">📏 '+r.rule+'</div>'
                +'<div style="display:flex;gap:8px;flex-wrap:wrap">';
                r.examples.forEach(e=>{{h+='<span class="tag tag-green" style="cursor:pointer" onclick="say(\\''+e+'\\')">🔊 '+e+'</span>';}});
                h+='</div></div>';
            }});
        }}
        area.innerHTML=h;
        if(mode==='bee'){{const inp=document.getElementById('spInput');if(inp)inp.focus();}}
    }}
    function sayWord(rate){{
        const u=new SpeechSynthesisUtterance(DATA.words[wi]);u.lang='en-US';u.rate=rate||0.9;
        speechSynthesis.cancel();speechSynthesis.speak(u);
    }}
    function say(w){{const u=new SpeechSynthesisUtterance(w);u.lang='en-US';u.rate=0.85;speechSynthesis.cancel();speechSynthesis.speak(u);}}
    function checkSpelling(){{
        const inp=document.getElementById('spInput');
        const ans=inp.value.trim().toLowerCase();
        const correct=DATA.words[wi].toLowerCase();
        const fb=document.getElementById('spFb');
        if(ans===correct){{
            score++;
            fb.innerHTML='<div class="fb fb-ok" style="display:inline-block">✅ Correct! <b>'+DATA.words[wi]+'</b></div>';
        }}else{{
            fb.innerHTML='<div class="fb fb-no" style="display:inline-block">❌ Correct spelling: <b>'+DATA.words[wi]+'</b></div>';
        }}
        setTimeout(()=>{{
            wi++;
            if(wi>=DATA.words.length){{
                area.innerHTML='<div class="fb fb-ok" style="text-align:center;padding:24px;font-size:1.1rem">'
                +'🏆 Spelling Bee Complete! Score: '+score+'/'+DATA.words.length+'</div>'
                +'<div style="text-align:center;margin-top:12px"><button class="btn" onclick="wi=0;score=0;render()">Try Again</button></div>';
            }}else render();
        }},1500);
    }}
    render();
    """
    return _shell("✏️ Spelling", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 9. FUNCTIONAL LANGUAGE
# ══════════════════════════════════════════════════════════════════════════════

_FUNC_LANG_DATA = _load_json("functional_lang_data")


def build_functional_lang_html(grade: str, start_index: int = 0) -> str:
    """Functional language: everyday phrases, dialogues, and role-play."""
    data = _FUNC_LANG_DATA.get(grade, _FUNC_LANG_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>💬 Functional Language</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Learn practical phrases for real-life situations. Listen, repeat, and practise!</p>"
        "<div id='flArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('flArea');
    let si={start_index};
    function render(){{
        let h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">';
        DATA.situations.forEach((s,i)=>{{
            h+='<button class="btn btn-sm'+(i===si?' btn-green':'')+'" onclick="si='+i+';render()">'+s.title+'</button>';
        }});
        h+='</div>';
        const s=DATA.situations[si];
        s.phrases.forEach((p,i)=>{{
            h+='<div class="card" style="border-left:3px solid #3b82f6">'
            +'<div style="font-size:.72rem;color:#64748b;margin-bottom:4px">📌 '+p.context+'</div>'
            +'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:6px">'
            +'<div style="background:rgba(59,130,246,.15);border-radius:12px 12px 12px 2px;padding:10px 14px;flex:1">'
            +'<div style="font-size:.72rem;color:#93c5fd;margin-bottom:2px">Speaker A:</div>'
            +'<div style="font-size:.88rem;color:#e2e8f0">'+p.phrase+'</div></div>'
            +'<button class="btn btn-sm" onclick="say(\\''+p.phrase.replace(/'/g,"\\\\'")+'\\')">🔊</button></div>'
            +'<div style="display:flex;gap:10px;align-items:flex-start">'
            +'<div style="background:rgba(16,185,129,.15);border-radius:12px 12px 2px 12px;padding:10px 14px;flex:1">'
            +'<div style="font-size:.72rem;color:#6ee7b7;margin-bottom:2px">Speaker B:</div>'
            +'<div style="font-size:.88rem;color:#e2e8f0">'+p.response+'</div></div>'
            +'<button class="btn btn-sm btn-green" onclick="say(\\''+p.response.replace(/'/g,"\\\\'")+'\\')">🔊</button></div>'
            +'</div>';
        }});
        h+='<div style="text-align:center;margin-top:14px;padding:14px;background:rgba(124,58,237,.1);border-radius:10px">'
        +'<div style="font-size:.85rem;color:#c4b5fd;font-weight:600">🎭 Role-Play Challenge</div>'
        +'<div style="font-size:.8rem;color:#94a3b8;margin-top:4px">Practise both roles with a partner or record yourself!</div></div>';
        area.innerHTML=h;
    }}
    function say(t){{const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=0.85;speechSynthesis.cancel();speechSynthesis.speak(u);}}
    render();
    """
    return _shell("💬 Functional Language", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 10. COMMUNICATION STRATEGIES
# ══════════════════════════════════════════════════════════════════════════════

_COMM_STRAT_DATA = _load_json("comm_strategies_data")


def build_comm_strategies_html(grade: str, start_index: int = 0) -> str:
    """Communication strategies with interactive scenarios and practice."""
    data = _COMM_STRAT_DATA.get(grade, _COMM_STRAT_DATA["5"])
    start_index = max(0, min(start_index, len(data) - 1)) if data else 0
    import json
    body = (
        "<div class='card'>"
        "<h3>🤝 Communication Strategies</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:12px'>"
        "Learn techniques that help you communicate effectively, even when you don't know all the words!</p>"
        "<div id='csArea'></div></div>"
    )
    js = f"""
    const DATA={json.dumps(data)};
    const area=document.getElementById('csArea');
    let si={start_index};
    function render(){{
        let h='<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">';
        DATA.strategies.forEach((s,i)=>{{
            h+='<button class="btn btn-sm'+(i===si?' btn-green':'')+'" onclick="si='+i+';render()">'+s.icon+' '+s.name+'</button>';
        }});
        h+='</div>';
        const s=DATA.strategies[si];
        h+='<div class="card"><div style="font-size:1.5rem;text-align:center;margin-bottom:8px">'+s.icon+'</div>'
        +'<div style="font-weight:700;color:#fbbf24;font-size:1rem;text-align:center;margin-bottom:12px">'+s.name+'</div>';
        h+='<div style="font-weight:600;color:#7dd3fc;font-size:.82rem;margin-bottom:8px">Key Phrases:</div>';
        s.phrases.forEach(p=>{{
            h+='<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;'
            +'background:rgba(255,255,255,.04);border-radius:8px;margin-bottom:6px">'
            +'<button class="btn btn-sm" onclick="say(\\''+p.replace(/'/g,"\\\\'")+'\\')">🔊</button>'
            +'<span style="font-size:.88rem;color:#e2e8f0">'+p+'</span></div>';
        }});
        h+='<div style="margin-top:14px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.25);'
        +'border-radius:10px;padding:14px">'
        +'<div style="font-weight:600;color:#fbbf24;font-size:.85rem;margin-bottom:6px">🎯 Practice Activity:</div>'
        +'<div style="font-size:.85rem;color:#e2e8f0;line-height:1.6">'+s.practice+'</div></div>';
        h+='</div>';
        area.innerHTML=h;
    }}
    function say(t){{const u=new SpeechSynthesisUtterance(t);u.lang='en-US';u.rate=0.85;speechSynthesis.cancel();speechSynthesis.speak(u);}}
    render();
    """
    return _shell("🤝 Communication Strategies", grade, body, extra_js=js)


# ══════════════════════════════════════════════════════════════════════════════
# 11. LEARNING PATH
# ══════════════════════════════════════════════════════════════════════════════

_LEARNING_PATH_SKILLS = [
    {"id": "listening", "name": "Listening", "icon": "🎧", "color": "#60a5fa"},
    {"id": "speaking", "name": "Speaking", "icon": "🗣️", "color": "#f472b6"},
    {"id": "reading", "name": "Reading", "icon": "📖", "color": "#34d399"},
    {"id": "writing", "name": "Writing", "icon": "✍️", "color": "#fbbf24"},
    {"id": "grammar", "name": "Grammar", "icon": "📝", "color": "#a78bfa"},
    {"id": "vocabulary", "name": "Vocabulary", "icon": "📚", "color": "#fb923c"},
    {"id": "pronunciation", "name": "Pronunciation", "icon": "🔤", "color": "#38bdf8"},
    {"id": "spelling", "name": "Spelling", "icon": "✏️", "color": "#4ade80"},
    {"id": "functional", "name": "Functional Language", "icon": "💬", "color": "#e879f9"},
    {"id": "strategies", "name": "Communication Strategies", "icon": "🤝", "color": "#f87171"},
]


def build_learning_path_html(grade: str, completions: dict | None = None) -> str:
    """Visual learning path showing skill progression with unlock mechanism.

    completions: dict mapping skill_id -> bool (True if completed)
    """
    import json
    comps = completions or {}
    cfg = _GRADE_CFG.get(grade, _GRADE_CFG["5"])
    skills_json = json.dumps(_LEARNING_PATH_SKILLS)
    comps_json = json.dumps(comps)

    body = (
        "<div class='card'>"
        "<h3>🗺️ Learning Path</h3>"
        "<p style='font-size:.8rem;color:#94a3b8;margin-bottom:4px'>"
        f"Grade {grade} — CEFR {cfg['cefr']} | Complete skills in order to unlock the next!</p>"
        "<div id='lpArea'></div></div>"
    )
    js = f"""
    const SKILLS={skills_json};
    const COMPS={comps_json};
    const GRADE="{grade}";
    const area=document.getElementById('lpArea');
    function render(){{
        let completed=0;
        SKILLS.forEach(s=>{{if(COMPS[s.id])completed++;}});
        const pct=Math.round(completed/SKILLS.length*100);
        let h='<div style="margin-bottom:16px">'
        +'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
        +'<span style="font-size:.82rem;color:#94a3b8">Overall Progress</span>'
        +'<span style="font-size:.9rem;font-weight:700;color:#10b981">'+pct+'%</span></div>'
        +'<div style="background:rgba(255,255,255,.08);border-radius:10px;height:12px;overflow:hidden">'
        +'<div style="background:linear-gradient(90deg,#10b981,#34d399);height:100%;width:'+pct+'%;border-radius:10px;'
        +'transition:width .5s"></div></div>'
        +'<div style="font-size:.72rem;color:#64748b;margin-top:3px">'+completed+'/'+SKILLS.length+' skills completed</div></div>';
        // Path nodes
        h+='<div style="position:relative;padding:0 20px">';
        SKILLS.forEach((s,i)=>{{
            const done=!!COMPS[s.id];
            const unlocked=i===0||!!COMPS[SKILLS[i-1].id];
            const current=unlocked&&!done;
            const locked=!unlocked&&!done;
            const opacity=locked?'0.4':'1';
            const bg=done?'rgba(16,185,129,.15)':current?'rgba(251,191,36,.1)':'rgba(255,255,255,.03)';
            const border=done?'rgba(16,185,129,.4)':current?'rgba(251,191,36,.4)':'rgba(255,255,255,.08)';
            // Connector line
            if(i>0){{
                h+='<div style="position:relative;height:24px;display:flex;align-items:center;justify-content:center">'
                +'<div style="width:3px;height:100%;background:'+(done||current?'linear-gradient(180deg,'+SKILLS[i-1].color+','+s.color+')':'rgba(255,255,255,.1)')
                +';border-radius:2px"></div></div>';
            }}
            // Node
            h+='<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;border-radius:12px;'
            +'background:'+bg+';border:1px solid '+border+';opacity:'+opacity+';position:relative;'
            +(current?'box-shadow:0 0 12px rgba(251,191,36,.15);':'')
            +'">';
            // Icon circle
            const iconBg=done?'#10b981':current?s.color:'#475569';
            h+='<div style="width:44px;height:44px;border-radius:50%;background:'+iconBg+';display:flex;'
            +'align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;'
            +(current?'animation:pulse 2s infinite;':'')
            +'">'+(done?'✅':locked?'🔒':s.icon)+'</div>';
            // Info
            h+='<div style="flex:1"><div style="font-weight:700;color:'+(done?'#10b981':current?'#fbbf24':'#94a3b8')
            +';font-size:.88rem">'+s.name+'</div>';
            if(done)h+='<div style="font-size:.72rem;color:#6ee7b7">Completed!</div>';
            else if(current)h+='<div style="font-size:.72rem;color:#fbbf24">⬅ Current — start this skill!</div>';
            else if(locked)h+='<div style="font-size:.72rem;color:#64748b">Complete previous skill to unlock</div>';
            h+='</div>';
            // Step number
            h+='<div style="font-size:.7rem;color:#64748b;font-weight:600">'+( i+1)+'/'+SKILLS.length+'</div>';
            h+='</div>';
        }});
        h+='</div>';
        // Pulse animation
        h+='<style>@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(251,191,36,.3)}}50%{{box-shadow:0 0 0 8px rgba(251,191,36,0)}}}}</style>';
        area.innerHTML=h;
    }}
    render();
    """
    return _shell("🗺️ Learning Path", grade, body, extra_js=js)
