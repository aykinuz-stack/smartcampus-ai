"""
Bilgi Treni — Eğitim Treni Modülü
Her sınıf bir vagon (1-12), her vagon 10 kompartıman içerir.
Kompartımanlar: Konu Anlatımı, Kültür & Sanat, Bilim & Teknik, Edebiyat,
Bilgi Yarışması, Eğlence & Oyun, Matematik Atölyesi, Yabancı Dil, Deney Lab, Genel Kültür.
"""
from __future__ import annotations
import os, json as _json
import streamlit as st
import streamlit.components.v1 as components
from utils.ui_common import inject_common_css, _render_html
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("default")
except Exception:
    pass

_BASE = os.path.dirname(os.path.dirname(__file__))

# ── Config & Content imports ──
from data.bilgi_treni.config import (
    GRADE_CEFR, GRADE_SUBJECTS, SUBJECT_ICONS, SINIF_LABELS, SINIF_THEMES,
    KOMPARTIMAN_LIST, CEFR_SHORT,
)
from data.bilgi_treni.content_konu_anlatimi import GRADE_LESSONS
from data.bilgi_treni.content_quiz import get_quiz_questions
from data.bilgi_treni.content_matematik import MATH_DATA
from data.bilgi_treni.content_oyun import RIDDLES, MEMORY_EMOJIS
from data.bilgi_treni.content_deney import SCIENCE
from data.bilgi_treni.games import (
    build_memory_html as _game_memory, build_riddle_html as _game_riddle,
    build_word_scramble_html as _game_word, build_true_false_html as _game_tf,
    build_speed_math_html as _game_speed, build_stroop_html as _game_stroop,
    build_number_sort_html as _game_sort, build_emoji_guess_html as _game_emoji,
)
from data.bilgi_treni.math_games import (
    build_classic_math as _math_classic, build_speed_race as _math_race,
    build_number_guess as _math_guess, build_equation_solver as _math_eq,
    build_multiplication_master as _math_mult, build_math_chain as _math_chain,
)
# kiosk_mode kaldırıldı
from data.bilgi_treni.content_kultur_sanat import KULTUR_SANAT
from data.bilgi_treni.content_bilim_teknik import BILIM_TEKNIK
from data.bilgi_treni.content_edebiyat import EDEBIYAT
from data.bilgi_treni.content_genel_kultur import GENEL_KULTUR
from data.bilgi_treni.content_language import MULTI_LANG_WORDS, LANG_CONFIG
from data.bilgi_treni.daily import get_daily_content
from data.bilgi_treni.features import (
    BADGES, check_badges, CONCEPT_MAP, get_related_concepts,
    VIDEO_SUGGESTIONS, get_video_suggestions, LIBRARY,
    generate_study_plan, get_recommendations, PODCAST_SCRIPTS,
    generate_duel_questions,
)

# ══════════════════════════════════════════════════════════════════════════════
# AI KONU ÜRETİCİ
# ══════════════════════════════════════════════════════════════════════════════

def _generate_ai_topic(grade: int, subject: str, topic: str, outcomes: list) -> str | None:
    """OpenAI ile konu anlatımı üret."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        # .env dosyasından dene
        env_path = os.path.join(_BASE, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("OPENAI_API_KEY"):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        outcomes_text = "\n".join(f"- {o}" for o in outcomes[:5]) if outcomes else "Belirtilmemiş"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Sen Türkiye'de {grade}. sınıf {subject} dersi öğretmenisin. "
                        "Öğrenciye yönelik, anlaşılır ve eğlenceli konu anlatımları yazarsın. "
                        "Türkçe yaz. Markdown KULLANMA, düz metin yaz."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Konu: {topic}\n"
                        f"Sınıf: {grade}. sınıf\n"
                        f"Ders: {subject}\n"
                        f"Kazanımlar:\n{outcomes_text}\n\n"
                        "Bu konu için öğrenciye yönelik bir konu anlatımı yaz.\n"
                        "Format:\n"
                        "1) Konunun kısa tanıtımı (2-3 cümle)\n"
                        "2) Temel kavramlar ve açıklamaları (madde madde)\n"
                        "3) Günlük hayattan örnekler\n"
                        "4) Özet (3-4 cümlelik)\n\n"
                        "Toplam 200-400 kelime olsun. Samimi ve anlaşılır bir dil kullan."
                    ),
                },
            ],
            temperature=0.6,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI içerik oluşturulurken hata: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600)
def _load_annual_plans():
    path = os.path.join(_BASE, "data", "olcme", "annual_plans.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = _json.load(f)
    result = {}
    for rec in data:
        g = rec.get("grade"); subj = rec.get("subject", ""); unit = rec.get("unit", "").strip()
        topic = rec.get("topic", "").strip(); outcomes = rec.get("learning_outcomes", [])
        if not g or not subj or not unit: continue
        result.setdefault(g, {}).setdefault(subj, {}).setdefault(unit, [])
        if topic or outcomes:
            result[g][subj][unit].append({"topic": topic, "outcomes": [o.strip() for o in outcomes if o.strip()], "hours": rec.get("hours", ""), "week": rec.get("week", "")})
    return result

@st.cache_data(ttl=600)
def _load_cefr_words():
    path = os.path.join(_BASE, "data", "english", "cefr_words.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return _json.load(f)


# ══════════════════════════════════════════════════════════════════════════════
# TÜM İÇERİK VERİLERİ data/bilgi_treni/ altındaki dosyalardan import edilir:
# GRADE_LESSONS, QUIZ_DATA, MATH_DATA, RIDDLES, SCIENCE, MEMORY_EMOJIS,
# KULTUR_SANAT, BILIM_TEKNIK, EDEBIYAT, GENEL_KULTUR
# ══════════════════════════════════════════════════════════════════════════════


# (Tüm inline veriler data/bilgi_treni/ altına taşındı)


# ══════════════════════════════════════════════════════════════════════════════
# KOMPARTIMAN GÖRSEL ÇERÇEVESİ
# ══════════════════════════════════════════════════════════════════════════════

def _compartment_header(comp_idx: int, grade: int) -> str:
    """Kompartıman başlık HTML'i — tren penceresi ve plaka görünümü."""
    icon, title, desc = KOMPARTIMAN_LIST[comp_idx]
    label = SINIF_LABELS[grade]
    return (
        f'<div style="background:linear-gradient(180deg,#080822 0%,#0B0F19 30%,#131825 100%);'
        f'border:2px solid rgba(212,175,55,0.3);border-radius:16px;overflow:hidden;margin-bottom:14px;">'
        # Pencere şeridi
        f'<div style="display:flex;gap:12px;padding:10px 16px;background:linear-gradient(180deg,#060618,#0B0F19);'
        f'border-bottom:2px solid rgba(212,175,55,0.2);">'
        f'<div style="flex:1;height:32px;background:linear-gradient(180deg,rgba(212,175,55,0.08),rgba(212,175,55,0.02));'
        f'border:1px solid rgba(212,175,55,0.15);border-radius:6px;'
        f'box-shadow:inset 0 0 15px rgba(212,175,55,0.05);"></div>'
        f'<div style="flex:1;height:32px;background:linear-gradient(180deg,rgba(212,175,55,0.08),rgba(212,175,55,0.02));'
        f'border:1px solid rgba(212,175,55,0.15);border-radius:6px;'
        f'box-shadow:inset 0 0 15px rgba(212,175,55,0.05);"></div>'
        f'<div style="flex:1;height:32px;background:linear-gradient(180deg,rgba(212,175,55,0.08),rgba(212,175,55,0.02));'
        f'border:1px solid rgba(212,175,55,0.15);border-radius:6px;'
        f'box-shadow:inset 0 0 15px rgba(212,175,55,0.05);"></div>'
        f'</div>'
        # Bagaj rafı
        f'<div style="height:4px;background:linear-gradient(90deg,#A5B4FC,#6366F1,#A5B4FC);'
        f'box-shadow:0 2px 8px rgba(212,175,55,0.2);"></div>'
        # Kompartıman plakası
        f'<div style="padding:12px 18px;display:flex;align-items:center;gap:14px;">'
        f'<div style="width:48px;height:48px;background:linear-gradient(135deg,#A5B4FC,#6366F1);'
        f'border-radius:12px;display:flex;align-items:center;justify-content:center;'
        f'font-size:1.5rem;box-shadow:0 4px 15px rgba(212,175,55,0.3);'
        f'border:1px solid rgba(255,255,255,0.1);">{icon}</div>'
        f'<div>'
        f'<div style="font-size:0.65rem;color:rgba(212,175,55,0.6);font-weight:600;letter-spacing:1px;'
        f'text-transform:uppercase;">Kompartıman {comp_idx+1}</div>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#6366F1;margin-top:1px;">{title}</div>'
        f'<div style="font-size:0.75rem;color:#94A3B8;margin-top:1px;">{label} — {desc}</div>'
        f'</div>'
        f'</div>'
        # Alt ray şeridi
        f'<div style="height:3px;background:linear-gradient(90deg,rgba(212,175,55,0.1),rgba(212,175,55,0.3),rgba(212,175,55,0.1));"></div>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE HTML COMPONENT BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def _build_quiz_html() -> str:
    # TÜM havuzu JS'e gönder — JS tarafında her turda farklı 15 soru seçer
    from data.bilgi_treni.content_quiz import get_quiz_pool
    pool = get_quiz_pool()
    pool_json = _json.dumps(pool, ensure_ascii=False)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',system-ui,sans-serif;padding:20px}}
.quiz-title{{text-align:center;font-size:1.3rem;font-weight:800;color:#6366F1;margin-bottom:4px}}
.quiz-sub{{text-align:center;font-size:0.75rem;color:#94A3B8;margin-bottom:10px}}
.prog{{display:flex;gap:5px;justify-content:center;margin:10px 0;flex-wrap:wrap}}
.dot{{width:26px;height:26px;border-radius:50%;background:#131825;border:2px solid rgba(212,175,55,0.2);display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;color:#94A3B8}}
.dot.a{{border-color:#6366F1;color:#6366F1}}.dot.c{{background:#10b981;border-color:#10b981;color:#fff}}.dot.w{{background:#ef4444;border-color:#ef4444;color:#fff}}
.qcard{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:14px;padding:20px;margin:10px 0;animation:si .4s ease}}
@keyframes si{{0%{{opacity:0;transform:translateX(20px)}}100%{{opacity:1;transform:translateX(0)}}}}
.qt{{font-size:1rem;font-weight:700;margin-bottom:14px;line-height:1.5}}.qn{{color:#6366F1;font-size:0.75rem;font-weight:600;margin-bottom:6px}}
.opts{{display:flex;flex-direction:column;gap:7px}}
.opt{{background:#131825;border:2px solid rgba(212,175,55,0.15);border-radius:10px;padding:10px 14px;cursor:pointer;transition:.25s;font-size:0.9rem}}
.opt:hover{{border-color:rgba(212,175,55,0.5);transform:translateX(3px)}}
.opt.c{{border-color:#10b981;background:rgba(16,185,129,0.15);color:#10b981}}
.opt.w{{border-color:#ef4444;background:rgba(239,68,68,0.15);color:#ef4444}}
.res{{text-align:center;padding:24px}}.ri{{font-size:2.5rem}}.rs{{font-size:1.5rem;font-weight:900;color:#6366F1;margin-top:6px}}
.btn{{background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:10px;padding:9px 20px;font-weight:700;cursor:pointer;margin-top:10px;transition:.2s}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(212,175,55,0.3)}}
.round-info{{text-align:center;font-size:0.8rem;color:#94A3B8;margin-bottom:6px}}
</style></head><body>
<div class="quiz-title">❓ Bilgi Yarışması</div>
<div class="quiz-sub">Her turda farklı 15 soru — havuzda {len(pool)}+ soru!</div>
<div class="round-info" id="ri">Tur 1</div>
<div class="prog" id="p"></div>
<div id="q"></div>
<script>
const POOL={pool_json};
let Q=[],cur=0,sc=0,ans=[],roundNum=0,totalCorrect=0,totalPlayed=0;

function shuffle(a){{for(let i=a.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}}return a;}}

function newRound(){{
    roundNum++;
    Q=shuffle([...POOL]).slice(0,15);
    cur=0;sc=0;ans=[];
    document.getElementById('ri').textContent='Tur '+roundNum+' | Toplam: '+totalCorrect+'/'+totalPlayed+' doğru';
    show();
}}

function bp(){{const p=document.getElementById('p');p.innerHTML='';Q.forEach((_,i)=>{{const d=document.createElement('div');d.className='dot'+(i===cur?' a':'')+(ans[i]!==undefined?(ans[i]?' c':' w'):'');d.textContent=i+1;p.appendChild(d);}});}}

function show(){{
    if(cur>=Q.length){{res();return;}}
    bp();const q=Q[cur];
    let h=`<div class="qcard"><div class="qn">Soru ${{cur+1}}/${{Q.length}}</div><div class="qt">${{q.q}}</div><div class="opts">`;
    q.opts.forEach((o,i)=>{{h+=`<div class="opt" onclick="pick(${{i}})">${{String.fromCharCode(65+i)}}) ${{o}}</div>`;}});
    h+=`</div></div>`;document.getElementById('q').innerHTML=h;
}}

function pick(i){{
    const q=Q[cur];const ok=i===q.ans;if(ok)sc++;ans[cur]=ok;
    document.querySelectorAll('.opt').forEach((o,j)=>{{o.style.pointerEvents='none';if(j===q.ans)o.classList.add('c');if(j===i&&!ok)o.classList.add('w');}});
    setTimeout(()=>{{cur++;show();}},1000);
}}

function res(){{
    bp();
    totalCorrect+=sc;totalPlayed+=Q.length;
    const p=Math.round(sc/Q.length*100);
    const tp=Math.round(totalCorrect/totalPlayed*100);
    const ic=p>=80?'🏆':p>=60?'⭐':'💪';
    const msg=p>=80?'Mükemmel!':p>=60?'Çok İyi!':p>=40?'İyi!':'Daha çalış!';
    document.getElementById('q').innerHTML=`
        <div class="res">
            <div class="ri">${{ic}}</div>
            <div class="rs">${{sc}}/${{Q.length}} (%${{p}})</div>
            <div style="font-size:1rem;color:#6366F1;margin-top:4px">${{msg}}</div>
            <div style="color:#94A3B8;font-size:0.8rem;margin-top:8px">
                Toplam: ${{totalCorrect}}/${{totalPlayed}} (%${{tp}}) | ${{roundNum}} tur oynandı
            </div>
            <button class="btn" onclick="newRound()">🔄 Yeni 15 Soru</button>
            <div style="color:#94A3B8;font-size:0.7rem;margin-top:6px">Havuzda ${{POOL.length}}+ soru — her tur farklı!</div>
        </div>`;
    document.getElementById('ri').textContent='Tur '+roundNum+' | Toplam: '+totalCorrect+'/'+totalPlayed+' doğru';
}}

newRound();
</script></body></html>"""

def _build_memory_html() -> str:
    emojis = MEMORY_EMOJIS
    ej = _json.dumps(emojis, ensure_ascii=False)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;font-family:'Segoe UI',sans-serif;padding:14px;text-align:center}}h2{{color:#6366F1;font-size:1.2rem;margin-bottom:10px}}.st{{display:flex;justify-content:center;gap:16px;margin-bottom:10px;color:#6366F1;font-weight:700;font-size:0.85rem}}.g{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;max-width:480px;margin:0 auto}}.c{{aspect-ratio:1;background:#131825;border:2px solid rgba(212,175,55,0.2);border-radius:10px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.8rem;transition:.3s}}.c:hover{{border-color:rgba(212,175,55,0.5);transform:scale(1.05)}}.c .f{{display:none}}.c .b{{display:flex;color:rgba(212,175,55,0.3);font-size:1.3rem}}.c.fl{{background:rgba(212,175,55,0.1);border-color:#6366F1}}.c.fl .f{{display:flex}}.c.fl .b{{display:none}}.c.m{{background:rgba(16,185,129,0.15);border-color:#10b981;pointer-events:none}}.c.m .f{{display:flex}}.c.m .b{{display:none}}.w{{margin-top:14px;font-size:1.3rem;font-weight:800;color:#6366F1}}.btn{{background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:10px;padding:7px 18px;font-weight:700;cursor:pointer;margin-top:10px}}
</style></head><body>
<h2>🧠 Hafıza Oyunu</h2><div class="st"><span>Hamle: <span id="mv">0</span></span><span>Eşleşme: <span id="pr">0</span>/12</span></div><div class="g" id="g"></div><div id="wa"></div>
<script>
const E={ej};let cards=[],fl=[],mt=0,mv=0,lk=false;
function sh(a){{for(let i=a.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}}return a;}}
function init(){{const d=sh([...E,...E]);cards=d;fl=[];mt=0;mv=0;lk=false;document.getElementById('mv').textContent='0';document.getElementById('pr').textContent='0';document.getElementById('wa').innerHTML='';const g=document.getElementById('g');g.innerHTML='';d.forEach((e,i)=>{{const c=document.createElement('div');c.className='c';c.innerHTML=`<span class="f">${{e}}</span><span class="b">?</span>`;c.onclick=()=>fp(i,c);g.appendChild(c);}});}}
function fp(i,el){{if(lk||el.classList.contains('fl')||el.classList.contains('m'))return;el.classList.add('fl');fl.push({{i,el}});if(fl.length===2){{lk=true;mv++;document.getElementById('mv').textContent=mv;const[a,b]=fl;if(cards[a.i]===cards[b.i]){{a.el.classList.add('m');b.el.classList.add('m');mt++;document.getElementById('pr').textContent=mt;fl=[];lk=false;if(mt===E.length)document.getElementById('wa').innerHTML=`<div class="w">🏆 ${{mv}} hamlede!</div><button class="btn" onclick="init()">🔄</button>`;}}else setTimeout(()=>{{a.el.classList.remove('fl');b.el.classList.remove('fl');fl=[];lk=false;}},700);}}}}
init();
</script></body></html>"""

def _build_math_html() -> str:
    import random as _rnd
    probs = list(MATH_DATA); _rnd.shuffle(probs); probs = probs[:12]
    pj = _json.dumps([{"q":q,"a":a} for q,a in probs], ensure_ascii=False)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',sans-serif;padding:18px}}.t{{text-align:center;font-size:1.2rem;font-weight:800;color:#6366F1;margin-bottom:12px}}.sb{{text-align:center;font-size:0.8rem;color:#94A3B8;margin-bottom:10px}}.sb span{{color:#6366F1;font-weight:700}}.cd{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:14px;padding:20px;text-align:center}}.pr{{font-size:1.6rem;font-weight:900;color:#6366F1;margin:12px 0}}.ir{{display:flex;justify-content:center;gap:8px;margin:12px 0}}input{{background:#131825;border:2px solid rgba(212,175,55,0.3);border-radius:8px;padding:8px 14px;color:#E2E8F0;font-size:1rem;text-align:center;width:160px;outline:none}}input:focus{{border-color:#6366F1}}.btn{{background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:8px;padding:8px 16px;font-weight:700;cursor:pointer}}.fb{{margin-top:10px;font-size:1rem;font-weight:700}}.fc{{color:#10b981}}.fw{{color:#ef4444}}.fn{{text-align:center;padding:16px}}.fi{{font-size:2.5rem}}.fs{{font-size:1.3rem;font-weight:900;color:#6366F1;margin-top:6px}}
</style></head><body>
<div class="t">🔢 Matematik Atölyesi</div><div class="sb">Skor: <span id="sc">0</span>/<span id="tt">0</span> | Seri: <span id="st">0</span>🔥</div><div id="a"></div>
<script>
const P={pj};let idx=0,sc=0,str=0,bst=0;
function sh(){{if(idx>=P.length){{fin();return;}}document.getElementById('sc').textContent=sc;document.getElementById('tt').textContent=idx;document.getElementById('st').textContent=str;const p=P[idx];document.getElementById('a').innerHTML=`<div class="cd"><div style="font-size:0.75rem;color:#94A3B8">${{idx+1}}/${{P.length}}</div><div class="pr">${{p.q}}</div><div class="ir"><input id="ans" placeholder="Cevap..." onkeypress="if(event.key==='Enter')chk()"><button class="btn" onclick="chk()">✓</button></div><div id="fb"></div></div>`;document.getElementById('ans').focus();}}
function norm(s){{return s.toString().trim().toLowerCase().replace(/\\s+/g,'');}}
function chk(){{const a=norm(document.getElementById('ans').value),c=norm(P[idx].a),fb=document.getElementById('fb');if(a===c){{sc++;str++;if(str>bst)bst=str;fb.innerHTML=`<div class="fb fc">✅ Doğru!</div>`;}}else{{str=0;fb.innerHTML=`<div class="fb fw">❌ Cevap: ${{P[idx].a}}</div>`;}}setTimeout(()=>{{idx++;sh();}},1200);}}
function fin(){{document.getElementById('sc').textContent=sc;document.getElementById('tt').textContent=P.length;const p=Math.round(sc/P.length*100);document.getElementById('a').innerHTML=`<div class="fn"><div class="fi">${{p>=80?'🏆':p>=60?'⭐':'💪'}}</div><div class="fs">${{sc}}/${{P.length}} (%${{p}})</div><div style="color:#94A3B8;margin-top:4px">En uzun seri: ${{bst}}🔥</div><button class="btn" onclick="idx=0;sc=0;str=0;bst=0;sh()" style="margin-top:10px">🔄 Tekrar</button></div>`;}}
sh();
</script></body></html>"""

def _build_riddle_html() -> str:
    rj = _json.dumps([{"q":q,"a":a} for q,a in RIDDLES], ensure_ascii=False)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',sans-serif;padding:18px}}.t{{text-align:center;font-size:1.2rem;font-weight:800;color:#6366F1;margin-bottom:14px}}.rs{{display:flex;flex-direction:column;gap:10px;max-width:480px;margin:0 auto}}.r{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:14px;cursor:pointer;transition:.3s}}.r:hover{{border-color:rgba(212,175,55,0.5);transform:translateX(3px)}}.rq{{font-weight:600;margin-bottom:6px}}.ra{{display:none;background:rgba(212,175,55,0.1);border-radius:6px;padding:8px;color:#6366F1;font-weight:700;margin-top:6px}}.r.o .ra{{display:block}}.rh{{font-size:0.7rem;color:#94A3B8;margin-top:3px}}.r.o .rh{{display:none}}.n{{color:#6366F1;font-weight:700;margin-right:4px}}
</style></head><body>
<div class="t">🧩 Bilmece & Bulmaca</div><div class="rs" id="c"></div>
<script>
const R={rj};const c=document.getElementById('c');
R.forEach((r,i)=>{{const d=document.createElement('div');d.className='r';d.innerHTML=`<div class="rq"><span class="n">#${{i+1}}</span>${{r.q}}</div><div class="rh">Cevap için tıkla</div><div class="ra">💡 ${{r.a}}</div>`;d.onclick=()=>d.classList.toggle('o');c.appendChild(d);}});
</script></body></html>"""

def _build_science_html() -> str:
    exps = SCIENCE
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',sans-serif;padding:18px}}.t{{text-align:center;font-size:1.2rem;font-weight:800;color:#6366F1;margin-bottom:14px}}.es{{display:flex;flex-direction:column;gap:12px;max-width:520px;margin:0 auto}}.e{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:16px}}.et{{font-size:1rem;font-weight:800;color:#6366F1;margin-bottom:5px}}.em{{background:rgba(212,175,55,0.08);border-radius:6px;padding:6px 10px;font-size:0.8rem;color:#c0c0d8;margin-bottom:6px;border-left:3px solid #6366F1}}.es2{{font-size:0.85rem;line-height:1.5;margin-bottom:6px}}.er{{background:rgba(16,185,129,0.1);border-radius:6px;padding:6px 10px;font-size:0.8rem;color:#10b981;font-weight:600;border-left:3px solid #10b981}}
</style></head><body>
<div class="t">🧪 Deney Laboratuvarı</div><div class="es">
{''.join(f'<div class="e"><div class="et">{e[0]}</div><div class="em">📦 {e[1]}</div><div class="es2">{e[2]}</div><div class="er">💡 {e[3]}</div></div>' for e in exps)}
</div></body></html>"""

def _build_cefr_flashcard_html(grade: int, level: str, category: str, cards: list) -> str:
    cj = _json.dumps(cards, ensure_ascii=False)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',sans-serif;padding:14px;text-align:center}}.t{{font-size:1.1rem;font-weight:800;color:#6366F1;margin-bottom:12px}}.ca{{perspective:1000px;margin:0 auto;max-width:340px}}.fc{{position:relative;width:100%;min-height:180px;cursor:pointer;transition:transform .5s;transform-style:preserve-3d}}.fc.fl{{transform:rotateY(180deg)}}.ff,.fb{{position:absolute;inset:0;backface-visibility:hidden;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:18px}}.ff{{background:linear-gradient(135deg,#131825,#232B3E);border:2px solid rgba(212,175,55,0.3)}}.fb{{background:linear-gradient(135deg,#232B3E,#131825);border:2px solid #6366F1;transform:rotateY(180deg)}}.tw{{font-size:1.8rem;font-weight:900;color:#6366F1;margin:6px 0}}.ew{{font-size:1.6rem;font-weight:800;color:#E2E8F0;margin:6px 0}}.lb{{background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);border-radius:20px;padding:2px 10px;font-size:0.65rem;color:#6366F1;font-weight:600}}.sp{{background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);border-radius:50%;width:32px;height:32px;cursor:pointer;font-size:1rem;margin-top:6px;color:#6366F1}}.nv{{display:flex;justify-content:center;gap:8px;margin-top:12px}}.nb{{background:#131825;border:2px solid rgba(212,175,55,0.3);border-radius:8px;padding:6px 16px;color:#6366F1;font-weight:700;cursor:pointer;font-size:0.85rem}}.ct{{color:#94A3B8;font-size:0.75rem;margin-top:5px}}
</style></head><body>
<div class="t">CEFR {level} — {category}</div>
<div class="ca"><div class="fc" id="fc" onclick="flip()"><div class="ff" id="fr"></div><div class="fb" id="bk"></div></div></div>
<div class="nv"><button class="nb" onclick="prev()">◀</button><button class="nb" onclick="next()">▶</button></div><div class="ct" id="ct"></div>
<script>
const C={cj};let idx=0,fl=false;
let _vc={{}};function _bv(lc){{if(_vc[lc])return _vc[lc];const vs=speechSynthesis.getVoices();const fh=['female','Filiz','Emel','Hedda','Helena','Paulina','Elsa','Google'];let b=vs.find(v=>v.lang.startsWith(lc.split('-')[0])&&fh.some(h=>v.name.toLowerCase().includes(h.toLowerCase())));if(!b)b=vs.find(v=>v.lang.startsWith(lc.split('-')[0]));if(b)_vc[lc]=b;return b;}}speechSynthesis.onvoiceschanged=()=>_vc={{}};function sp(t,l){{try{{const u=new SpeechSynthesisUtterance(t);u.lang=l;u.rate=0.82;u.pitch=1.12;u.volume=1.0;const v=_bv(l);if(v)u.voice=v;speechSynthesis.cancel();speechSynthesis.speak(u);}}catch(e){{}}}}
function render(){{fl=false;document.getElementById('fc').classList.remove('fl');const c=C[idx];document.getElementById('fr').innerHTML=`<div style="font-size:2rem;margin-bottom:4px">📝</div><div class="tw">${{c.tr}}</div><span class="lb">CEFR {level}</span><div style="color:#94A3B8;font-size:0.75rem;margin-top:6px">Çevir →</div>`;document.getElementById('bk').innerHTML=`<div class="ew">${{c.en}}</div><button class="sp" onclick="event.stopPropagation();sp(c.en,'en-US')">🔊</button>`;document.getElementById('ct').textContent=(idx+1)+'/'+C.length;}}
function flip(){{fl=!fl;document.getElementById('fc').classList.toggle('fl');}}
function next(){{idx=(idx+1)%C.length;render();}}
function prev(){{idx=(idx-1+C.length)%C.length;render();}}
render();
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# TRAIN HUB ANIMATION
# ══════════════════════════════════════════════════════════════════════════════

def _build_train_hub_html() -> str:
    wagon_html = ""
    for g in range(1, 13):
        theme = SINIF_THEMES[g][0]
        wagon_html += f"""<div class="wagon" onclick="selectWagon({g})" title="{SINIF_LABELS[g]}"><div class="wc"></div><div class="wb"><div class="wr"></div><div class="wi"><div class="wg">{g}</div><div class="wl">{SINIF_LABELS[g]}</div></div><div class="ww w1"></div><div class="ww w2"></div></div><div class="wh"><div class="whl"></div><div class="whl"></div></div></div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;overflow-x:hidden;font-family:'Segoe UI',sans-serif}}
.sc{{position:relative;width:100%;height:560px;overflow:hidden;background:linear-gradient(180deg,#05051a,#0B0F19 40%,#131825 70%,#1A2035)}}
.stars{{position:absolute;width:100%;height:60%}}.star{{position:absolute;border-radius:50%;background:#6366F1;animation:tw 2s ease-in-out infinite alternate}}@keyframes tw{{0%{{opacity:.3;transform:scale(.8)}}100%{{opacity:1;transform:scale(1.2)}}}}
.moon{{position:absolute;top:30px;right:80px;width:55px;height:55px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#6366F1,#6366F1);box-shadow:0 0 40px rgba(212,175,55,.4)}}
.mts{{position:absolute;bottom:120px;width:200%;height:160px;background:linear-gradient(135deg,transparent 33%,#0c0c30 33%,#0c0c30 66%,transparent 66%),linear-gradient(225deg,transparent 33%,#0a0a28 33%,#0a0a28 66%,transparent 66%);background-size:200px 160px}}
.gnd{{position:absolute;bottom:0;width:100%;height:120px;background:linear-gradient(180deg,#131825,#0e0e30);border-top:2px solid rgba(212,175,55,.15)}}
.rl{{position:absolute;bottom:58px;width:200%;height:4px;background:linear-gradient(90deg,#6366F1,#A5B4FC,#6366F1,#A5B4FC);background-size:200px;box-shadow:0 0 8px rgba(212,175,55,.3)}}.rl2{{bottom:42px}}
.ties{{position:absolute;bottom:38px;width:200%;height:24px;background:repeating-linear-gradient(90deg,#2a2a50 0px,#2a2a50 6px,transparent 6px,transparent 40px)}}
.ta{{position:absolute;top:18px;left:50%;transform:translateX(-50%);text-align:center;z-index:20}}
.tm{{font-size:2rem;font-weight:900;color:#6366F1;text-shadow:0 0 20px rgba(212,175,55,.5),0 2px 4px rgba(0,0,0,.5);letter-spacing:2px}}
.ts{{font-size:.85rem;color:#94A3B8;margin-top:3px}}.tb{{display:inline-block;margin-top:6px;padding:4px 14px;background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border-radius:20px;font-size:.7rem;font-weight:700}}
.tsc{{position:absolute;bottom:55px;left:0;right:0;overflow-x:auto;overflow-y:visible;white-space:nowrap;padding:0 50px 20px;z-index:10;scroll-behavior:smooth;cursor:grab;scrollbar-width:thin;scrollbar-color:rgba(212,175,55,.4) rgba(10,10,46,.5)}}
.trn{{display:inline-flex;align-items:flex-end;gap:0;padding-bottom:15px;animation:idle 3s ease-in-out infinite}}@keyframes idle{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-2px)}}}}
.trn.dep{{animation:dep 2s ease-in forwards!important}}@keyframes dep{{0%{{transform:translateX(0)}}30%{{transform:translateX(10px) translateY(-3px)}}100%{{transform:translateX(120vw)}}}}
.na{{position:absolute;bottom:85px;z-index:20;width:38px;height:38px;background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:50%;cursor:pointer;font-size:1.1rem;font-weight:900;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 15px rgba(212,175,55,.4);opacity:.9}}.na:hover{{transform:scale(1.15);opacity:1}}.na.l{{left:8px}}.na.r{{right:8px}}.na.h{{opacity:.2;pointer-events:none}}
.loco{{display:inline-block;position:relative;width:170px;height:125px;vertical-align:bottom}}
.lb2{{position:absolute;bottom:25px;left:20px;width:140px;height:65px;background:linear-gradient(180deg,#232B3E,#131825);border:2px solid #6366F1;border-radius:8px 25px 4px 4px;box-shadow:0 0 12px rgba(212,175,55,.2)}}
.lca{{position:absolute;bottom:60px;right:25px;width:55px;height:45px;background:linear-gradient(180deg,#1A2035,#131825);border:2px solid #6366F1;border-radius:6px 6px 0 0}}
.lcw{{position:absolute;top:7px;left:7px;width:18px;height:16px;background:rgba(212,175,55,.3);border-radius:3px;border:1px solid #6366F1}}.lcw.r{{left:auto;right:7px}}
.ch{{position:absolute;bottom:88px;left:32px;width:18px;height:30px;background:linear-gradient(180deg,#6366F1,#A5B4FC);border-radius:4px 4px 2px 2px}}.cht{{position:absolute;top:-5px;left:-3px;width:24px;height:7px;background:#6366F1;border-radius:3px}}
.hl{{position:absolute;bottom:48px;left:14px;width:12px;height:12px;background:radial-gradient(circle,#6366F1,#6366F1);border-radius:50%;box-shadow:0 0 18px #6366F1}}
.cc{{position:absolute;bottom:15px;left:5px;width:28px;height:12px;background:linear-gradient(180deg,#6366F1,#A5B4FC);clip-path:polygon(0 0,100% 0,80% 100%,20% 100%)}}
.ls{{position:absolute;bottom:42px;left:20px;width:140px;height:3px;background:#6366F1}}
.lw{{position:absolute;bottom:8px;width:26px;height:26px;border-radius:50%;border:3px solid #6366F1;background:radial-gradient(circle,#232B3E 40%,#131825);animation:ws 1s linear infinite paused}}.lw::after{{content:'';position:absolute;top:50%;left:50%;width:10px;height:2px;background:#6366F1;transform:translate(-50%,-50%)}}.lw1{{left:24px}}.lw2{{left:60px}}.lw3{{left:108px;width:30px;height:30px;bottom:6px}}
@keyframes ws{{0%{{transform:rotate(0)}}100%{{transform:rotate(360deg)}}}}.trn.dep .lw,.trn.dep .whl{{animation-play-state:running!important}}
.stc{{position:absolute;bottom:125px;left:28px;width:35px;height:70px;overflow:visible;z-index:5}}
.stm{{position:absolute;bottom:0;border-radius:50%;background:radial-gradient(circle,rgba(212,175,55,.25),rgba(212,175,55,.05));animation:sr 2.5s ease-out infinite}}
@keyframes sr{{0%{{opacity:.7;transform:translateY(0) scale(.3)}}50%{{opacity:.4;transform:translateY(-35px) translateX(8px) scale(1)}}100%{{opacity:0;transform:translateY(-70px) translateX(18px) scale(1.5)}}}}
.stm.s1{{width:16px;height:16px;left:4px}}.stm.s2{{width:22px;height:22px;left:8px;animation-delay:.5s}}.stm.s3{{width:14px;height:14px;animation-delay:1s}}.stm.s4{{width:18px;height:18px;left:10px;animation-delay:1.5s}}
.wagon{{display:inline-block;position:relative;width:130px;height:105px;vertical-align:bottom;cursor:pointer;transition:transform .3s,filter .3s}}
.wagon:hover{{transform:translateY(-7px) scale(1.05);filter:brightness(1.2)}}
.wc{{position:absolute;bottom:33px;left:-7px;width:14px;height:5px;background:#6366F1;border-radius:2px}}
.wb{{position:absolute;bottom:20px;left:8px;right:8px;height:68px;background:linear-gradient(180deg,#1A2035,#131825);border:2px solid rgba(212,175,55,.5);border-radius:5px;box-shadow:0 0 8px rgba(212,175,55,.15);overflow:hidden}}
.wr{{position:absolute;top:-3px;left:-2px;right:-2px;height:5px;background:linear-gradient(90deg,#A5B4FC,#6366F1,#A5B4FC);border-radius:3px}}
.wi{{position:absolute;inset:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.wg{{font-size:1.7rem;font-weight:900;color:#6366F1;text-shadow:0 0 8px rgba(212,175,55,.5);line-height:1}}
.wl{{font-size:.6rem;color:#c0c0d8;font-weight:600;margin-top:2px}}
.ww{{position:absolute;width:12px;height:12px;background:rgba(212,175,55,.2);border:1px solid rgba(212,175,55,.4);border-radius:2px}}.ww.w1{{top:8px;left:10px}}.ww.w2{{top:8px;right:10px}}
.wh{{position:absolute;bottom:6px;left:8px;right:8px;display:flex;justify-content:space-between;padding:0 12px}}
.whl{{width:18px;height:18px;border-radius:50%;border:2px solid #6366F1;background:radial-gradient(circle,#232B3E 40%,#131825);animation:ws .8s linear infinite paused}}
.do{{display:none;position:fixed;inset:0;z-index:100;background:rgba(10,10,46,.95);flex-direction:column;align-items:center;justify-content:center}}.do.a{{display:flex;animation:fi .3s ease}}@keyframes fi{{0%{{opacity:0}}100%{{opacity:1}}}}.dt{{font-size:1.8rem;font-weight:900;color:#6366F1;text-shadow:0 0 25px rgba(212,175,55,.5)}}.dg{{font-size:2.5rem;margin-top:8px}}.ds{{color:#94A3B8;margin-top:6px}}
.sh{{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);font-size:.7rem;color:rgba(212,175,55,.5);z-index:15}}
</style></head><body>
<div class="sc">
<div class="stars" id="st"></div><div class="moon"></div>
<div class="ta"><div class="tm">🚂 AI TRENİ</div><div class="ts">Her Vagon Bir Eğitim Dünyası • 15 Kompartıman</div><div class="tb">12 SINIF • 15 KOMPARTIMAN • AI DESTEKLİ • SONSUZ KEŞİF</div></div>
<div class="mts"></div>
<div class="gnd"><div class="ties"></div><div class="rl"></div><div class="rl rl2"></div></div>
<div class="tsc">
<div class="trn" id="trn">
<div class="loco"><div class="stc"><div class="stm s1"></div><div class="stm s2"></div><div class="stm s3"></div><div class="stm s4"></div></div><div class="ch"><div class="cht"></div></div><div class="lca"><div class="lcw"></div><div class="lcw r"></div></div><div class="lb2"></div><div class="ls"></div><div class="hl"></div><div class="cc"></div><div class="lw lw1"></div><div class="lw lw2"></div><div class="lw lw3"></div></div>
{wagon_html}
</div></div>
<div class="sh">◀ Sürükle veya ok tuşları ile vagonları keşfet ▶</div>
<button class="na l" id="al" onclick="scr(-280)">◀</button>
<button class="na r" id="ar" onclick="scr(280)">▶</button>
<div class="do" id="dov"><div class="dt" id="dtx">🚂 Tren Kalkıyor!</div><div class="dg" id="dgr"></div><div class="ds" id="dsb"></div></div>
</div>
<script>
(function(){{const c=document.getElementById('st');for(let i=0;i<70;i++){{const s=document.createElement('div');s.className='star';const z=Math.random()*3+1;s.style.cssText=`width:${{z}}px;height:${{z}}px;top:${{Math.random()*100}}%;left:${{Math.random()*100}}%;animation-delay:${{Math.random()*3}}s;animation-duration:${{1.5+Math.random()*2}}s`;c.appendChild(s);}}}})();
function playS(){{try{{const c=new(window.AudioContext||window.webkitAudioContext)();const o=c.createOscillator();const g=c.createGain();o.type='sine';o.frequency.setValueAtTime(700,c.currentTime);o.frequency.linearRampToValueAtTime(500,c.currentTime+.4);o.frequency.linearRampToValueAtTime(700,c.currentTime+.8);g.gain.setValueAtTime(.12,c.currentTime);g.gain.linearRampToValueAtTime(0,c.currentTime+1);o.connect(g);g.connect(c.destination);o.start();o.stop(c.currentTime+1);}}catch(e){{}}}}
const N={{{','.join(f'{g}:"{SINIF_LABELS[g]}"' for g in range(1,13))}}};
function selectWagon(g){{playS();document.getElementById('dgr').textContent=g+'. Sınıf';document.getElementById('dsb').textContent='Vagona biniliyor...';document.getElementById('trn').classList.add('dep');setTimeout(()=>document.getElementById('dov').classList.add('a'),500);setTimeout(()=>{{try{{const u=new URL(window.parent.location.href);u.searchParams.set('bt_grade',g);window.parent.location.href=u;}}catch(e){{try{{window.parent.location.search='?bt_grade='+g;}}catch(e2){{}}}}}},1600);}}
const se=document.querySelector('.tsc');
function scr(d){{se.scrollBy({{left:d,behavior:'smooth'}});}}
function ua(){{const al=document.getElementById('al'),ar=document.getElementById('ar');if(al)al.classList.toggle('h',se.scrollLeft<10);if(ar)ar.classList.toggle('h',se.scrollLeft>=se.scrollWidth-se.clientWidth-10);}}
se.addEventListener('scroll',ua);ua();
let dr=false,sx=0,ss=0;
se.addEventListener('mousedown',e=>{{dr=true;sx=e.pageX;ss=se.scrollLeft;se.style.cursor='grabbing';e.preventDefault();}});
document.addEventListener('mousemove',e=>{{if(!dr)return;se.scrollLeft=ss-(e.pageX-sx);}});
document.addEventListener('mouseup',()=>{{dr=false;se.style.cursor='grab';}});
se.addEventListener('touchstart',e=>{{sx=e.touches[0].pageX;ss=se.scrollLeft;}},{{passive:true}});
se.addEventListener('touchmove',e=>{{se.scrollLeft=ss-(e.touches[0].pageX-sx);}},{{passive:true}});
let asd=false;setTimeout(()=>{{if(asd)return;const mx=se.scrollWidth-se.clientWidth;if(mx<=0)return;let p=0;const st=()=>{{if(dr||asd)return;p+=1.5;se.scrollLeft=p;if(p<mx)requestAnimationFrame(st);else{{asd=true;setTimeout(()=>se.scrollTo({{left:0,behavior:'smooth'}}),700);}}}};requestAnimationFrame(st);}},1200);
se.addEventListener('mousedown',()=>asd=true);se.addEventListener('touchstart',()=>asd=true,{{passive:true}});
document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight')scr(180);if(e.key==='ArrowLeft')scr(-180);}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# WAGON RENDERER — 10 Kompartıman
# ══════════════════════════════════════════════════════════════════════════════

def _render_wagon(grade: int):
    label = SINIF_LABELS[grade]
    theme = SINIF_THEMES[grade][0]

    c1, c2 = st.columns([0.18, 0.82])
    with c1:
        if st.button("🚂 Trene Dön", key="bt_back", use_container_width=True, type="primary"):
            st.session_state["bt_sinif"] = None
            st.rerun()
    with c2:
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#131825,#1A2035,#232B3E);padding:12px 18px;border-radius:14px;border:1px solid rgba(212,175,55,0.15);">'
            f'<div style="font-size:1.15rem;font-weight:900;color:#6366F1;">🚃 Vagon {grade} — {label}</div>'
            f'<div style="font-size:0.75rem;color:#94A3B8;margin-top:2px;">{theme} • 15 Kompartıman</div></div>', unsafe_allow_html=True)

    # ── GÜNÜN BİLGİSİ WIDGET (tüm vagonlarda gösterilir) ──
    daily = get_daily_content()
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#131825,#232B3E);border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:12px 16px;margin:8px 0;">'
        f'<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;">'
        f'<div style="flex:1;min-width:200px;">'
        f'<div style="font-size:0.65rem;color:#94A3B8;text-transform:uppercase;letter-spacing:1px;">📅 Günün Bilgisi</div>'
        f'<div style="font-size:0.85rem;color:#E2E8F0;margin-top:3px;">🤯 {daily["fact"]}</div></div>'
        f'<div style="flex:1;min-width:180px;">'
        f'<div style="font-size:0.65rem;color:#94A3B8;">🌍 Günün Kelimesi</div>'
        f'<div style="font-size:0.85rem;margin-top:3px;"><b style="color:#6366F1;">{daily["word"]["tr"]}</b>'
        f' 🇬🇧 {daily["word"]["en"]} • 🇩🇪 {daily["word"]["de"]} • 🇫🇷 {daily["word"]["fr"]}</div></div>'
        f'<div style="flex:1;min-width:200px;">'
        f'<div style="font-size:0.65rem;color:#94A3B8;">💬 Günün Sözü</div>'
        f'<div style="font-size:0.85rem;color:#E2E8F0;font-style:italic;margin-top:3px;">"{daily["quote"][1]}" — <span style="color:#6366F1;">{daily["quote"][0]}</span></div></div>'
        f'</div></div>', unsafe_allow_html=True)

    # ── LOKOMOTİF: AI Bireysel Eğitim (en öne) + 14 KOMPARTIMAN ──
    lokomotif = [("🚂","AI Bireysel Eğitim")]
    extra_tabs = [("📻","Sesli İçerik"),("🧩","Kavram Haritası"),("🎬","Video & Kaynak"),("🏅","Başarılar & Plan")]
    all_tabs = lokomotif + KOMPARTIMAN_LIST + extra_tabs
    tab_labels = [f"{k[0]} {k[1]}" for k in all_tabs]
    tabs = st.tabs(tab_labels)

    # ── LOKOMOTİF: AI Bireysel Eğitim (İLK SEKME) ──
    with tabs[0]:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#131825,#1a1a50);border:2px solid #6366F1;border-radius:14px;padding:16px 20px;margin-bottom:14px;">'
            '<div style="font-size:1.2rem;font-weight:900;background:linear-gradient(135deg,#6366F1,#6366F1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">🚂 AI Bireysel Eğitim — Lokomotif</div>'
            '<div style="font-size:0.82rem;color:#94A3B8;margin-top:4px;">Konu Anlat, Kazanım Anlat, 3D Görsel, Mini Quiz, İstatistik, Geçmiş, Yabancı Dil</div></div>', unsafe_allow_html=True)
        try:
            from views.dijital_kutuphane import render_ai_asistan
            render_ai_asistan()
        except Exception as _ai_err:
            st.error(f"AI Bireysel Eğitim yüklenirken hata: {_ai_err}")
            st.info("Bu özellik için Dijital Kütüphane modülünün aktif olması gerekir.")

    # ── K1: Konu Anlatımı (AI destekli arama + sınıf bazlı içerik) ──
    with tabs[1]:
        st.markdown(_compartment_header(0, grade), unsafe_allow_html=True)  # Konu Anlatımı

        # ── AI Destekli Akıllı Arama ──
        import re as _re
        search_q = st.text_input("🔍 Konu ara (tüm sınıflarda arar)...", key=f"bt_search_{grade}", placeholder="Örn: hücre, Newton, kesir, DNA, Atatürk...")

        if search_q and len(search_q) >= 2:
            q = search_q.lower().strip()
            results = []
            for g in range(1, 13):
                for title, subject, content, concepts in GRADE_LESSONS.get(g, []):
                    score = 0
                    text_all = f"{title} {subject} {content} {' '.join(concepts)}".lower()
                    if q in text_all:
                        # Başlıkta bulunursa yüksek skor
                        if q in title.lower(): score += 10
                        # Kavramlarda bulunursa orta skor
                        if any(q in c.lower() for c in concepts): score += 5
                        # İçerikte bulunursa temel skor + kaç kez geçtiğine göre
                        score += text_all.count(q)
                        results.append((score, g, title, subject, content, concepts))
            results.sort(key=lambda x: -x[0])

            if results:
                st.markdown(f'<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:8px 14px;margin:8px 0;font-size:0.85rem;color:#10b981;font-weight:600;">🎯 "{search_q}" için {len(results)} sonuç bulundu (tüm sınıflarda)</div>', unsafe_allow_html=True)
                for score, g, title, subject, content, concepts in results[:10]:
                    icon = SUBJECT_ICONS.get(subject, "📘")
                    # Arama terimini vurgula (highlight)
                    def _highlight(text, term):
                        pattern = _re.compile(_re.escape(term), _re.IGNORECASE)
                        return pattern.sub(lambda m: f'<mark style="background:#6366F1;color:#0B0F19;padding:1px 3px;border-radius:3px;font-weight:700;">{m.group()}</mark>', text)
                    h_title = _highlight(title, search_q)
                    h_content = _highlight(content, search_q)
                    h_concepts = [_highlight(c, search_q) for c in concepts]

                    with st.expander(f"📌 {SINIF_LABELS[g]} — {title} ({icon} {subject})"):
                        st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.6;color:#E2E8F0;">{h_content}</div>', unsafe_allow_html=True)
                        st.markdown(" ".join(f'<span style="display:inline-block;background:rgba(212,175,55,0.12);border:1px solid rgba(212,175,55,0.25);border-radius:20px;padding:2px 10px;font-size:0.75rem;color:#6366F1;font-weight:600;margin:2px;">{c}</span>' for c in h_concepts), unsafe_allow_html=True)
            else:
                # Eşleşme yok — AI ile üret
                ai_search_key = f"bt_ai_search_{grade}_{search_q}"
                st.markdown(
                    f'<div style="background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.2);'
                    f'border-radius:10px;padding:10px 14px;margin:8px 0;">'
                    f'<span style="font-size:0.85rem;color:#6366F1;font-weight:600;">'
                    f'🔍 "{search_q}" hazır konularda bulunamadı.</span></div>',
                    unsafe_allow_html=True,
                )
                if ai_search_key in st.session_state:
                    ai_content = st.session_state[ai_search_key]
                    st.markdown(
                        f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #10b981;'
                        f'padding:12px 16px;border-radius:0 10px 10px 0;font-size:0.9rem;'
                        f'line-height:1.7;color:#E2E8F0;white-space:pre-wrap;margin-top:8px;">{ai_content}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button(f"🤖 AI ile \"{search_q}\" konusunu anlat", key=f"bt_ai_srch_{grade}"):
                        with st.spinner(f"AI \"{search_q}\" konusunu hazırlıyor..."):
                            # Sınıfa uygun ders tahmini
                            subj_guess = GRADE_SUBJECTS.get(grade, ["Genel"])[0]
                            ai_result = _generate_ai_topic(grade, subj_guess, search_q, [])
                        if ai_result:
                            st.session_state[ai_search_key] = ai_result
                            st.rerun()
                        else:
                            st.error("AI servisi kullanılamıyor. OPENAI_API_KEY kontrol edin.")
        else:
            # Normal görünüm — seçili sınıfın konuları
            lessons = GRADE_LESSONS.get(grade, [])

            # ── AI + MEB konularını hesapla ──
            plans = _load_annual_plans()
            gd = plans.get(grade, {})
            meb_topics = []
            if gd:
                existing = set()
                for t, s, c, k in lessons:
                    existing.add(t.lower().strip())
                    clean = t.strip()
                    for ch in "🏠📐🔢🌍🧪⚡🧬🔬📖🎨🌱💡🔭📊🧮🏛️":
                        clean = clean.replace(ch, "")
                    existing.add(clean.strip().lower())

                for subj in GRADE_SUBJECTS.get(grade, []):
                    if subj not in gd:
                        continue
                    for unit_name, entries in gd[subj].items():
                        for entry in entries:
                            topic = entry.get("topic", "").strip()
                            outcomes = entry.get("learning_outcomes", [])
                            if not topic and not outcomes:
                                continue
                            label = topic if topic else (outcomes[0] if outcomes else unit_name)
                            if label.lower() in existing:
                                continue
                            meb_topics.append({
                                "subject": subj,
                                "unit": unit_name,
                                "topic": label,
                                "outcomes": outcomes,
                            })

            # ── Sekme: Hazır Konular / AI Konular ──
            t_hazir, t_ai, t_meb = st.tabs([
                f"📚 Hazır Konular ({len(lessons)})",
                f"🤖 AI Konu Anlatımı ({len(meb_topics)})",
                "📋 MEB Müfredat",
            ])

            # ── TAB 1: Hazır Konular ──
            with t_hazir:
                if lessons:
                    st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">📚 {SINIF_LABELS[grade]} — {len(lessons)} konu</div>', unsafe_allow_html=True)
                else:
                    st.info("Bu sınıf için henüz hazır konu özeti eklenmemiş. 🤖 AI sekmesinden üretebilirsiniz.")
                for title, subject, content, concepts in lessons:
                    icon = SUBJECT_ICONS.get(subject, "📘")
                    with st.expander(f"{title} ({icon} {subject})"):
                        st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.6;color:#E2E8F0;">{content}</div>', unsafe_allow_html=True)
                        st.markdown(" ".join(f'<span style="display:inline-block;background:rgba(212,175,55,0.12);border:1px solid rgba(212,175,55,0.25);border-radius:20px;padding:2px 10px;font-size:0.75rem;color:#6366F1;font-weight:600;margin:2px;">{c}</span>' for c in concepts), unsafe_allow_html=True)

            # ── TAB 2: AI Konu Üretimi ──
            with t_ai:
                if meb_topics:
                    st.markdown(
                        f'<div style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);'
                        f'border-radius:12px;padding:12px 16px;margin-bottom:10px;">'
                        f'<span style="font-size:0.85rem;font-weight:700;color:#10b981;">'
                        f'🤖 MEB müfredatında {len(meb_topics)} ek konu bulundu</span>'
                        f'<br><span style="font-size:0.75rem;color:#94A3B8;">'
                        f'Butona tıklayarak AI destekli konu anlatımı oluşturun.</span></div>',
                        unsafe_allow_html=True,
                    )

                    by_subj = {}
                    for t in meb_topics:
                        by_subj.setdefault(t["subject"], []).append(t)

                    for subj, topics in by_subj.items():
                        icon = SUBJECT_ICONS.get(subj, "📘")
                        with st.expander(f"🤖 {icon} {subj} — {len(topics)} konu"):
                            for tidx, t in enumerate(topics):
                                topic_key = f"bt_ai_{grade}_{subj}_{tidx}"
                                cache_key = f"bt_ai_cache_{grade}_{subj}_{tidx}"

                                st.markdown(
                                    f'<div style="font-size:0.82rem;color:#6366F1;font-weight:600;'
                                    f'margin:6px 0 2px 0;">📌 {t["topic"]}</div>',
                                    unsafe_allow_html=True,
                                )
                                if t["outcomes"]:
                                    st.caption("Kazanımlar: " + " • ".join(t["outcomes"][:3]))

                                if cache_key in st.session_state:
                                    ai_content = st.session_state[cache_key]
                                    st.markdown(
                                        f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #10b981;'
                                        f'padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.88rem;'
                                        f'line-height:1.7;color:#E2E8F0;white-space:pre-wrap;">{ai_content}</div>',
                                        unsafe_allow_html=True,
                                    )
                                else:
                                    if st.button(f"🤖 AI ile Anlat: {t['topic'][:40]}", key=topic_key):
                                        with st.spinner("AI konu anlatımı oluşturuluyor..."):
                                            ai_result = _generate_ai_topic(grade, subj, t["topic"], t["outcomes"])
                                        if ai_result:
                                            st.session_state[cache_key] = ai_result
                                            st.rerun()
                                        else:
                                            st.error("AI servisi kullanılamıyor. OPENAI_API_KEY kontrol edin.")
                else:
                    st.info("Bu sınıf için MEB müfredatında ek konu bulunamadı.")

            # ── TAB 3: MEB Müfredat Referansı ──
            with t_meb:
                if gd:
                    for subj in [s for s in GRADE_SUBJECTS.get(grade, []) if s in gd]:
                        st.markdown(f"**{SUBJECT_ICONS.get(subj,'📘')} {subj}** — {len(gd[subj])} Ünite")
                        for u, entries in gd[subj].items():
                            st.caption(f"📌 {u}")
                else:
                    st.info("Bu sınıf için MEB müfredat verisi bulunamadı.")

    # ── Yardımcı: kategori başlığı ──
    def _cat(title):
        st.markdown(f'<div style="background:rgba(212,175,55,0.06);border-left:3px solid #6366F1;padding:6px 12px;border-radius:0 6px 6px 0;margin:8px 0;font-weight:700;color:#6366F1;font-size:0.9rem;">{title}</div>', unsafe_allow_html=True)

    # ── K2: Kültür & Sanat (GENEL) ──
    with tabs[2]:
        st.markdown(_compartment_header(1, grade), unsafe_allow_html=True)
        ks_map = {"gorsel_sanat":"🎨 Görsel Sanatlar","muzik":"🎵 Müzik","tiyatro_sinema":"🎭 Tiyatro & Sinema","miras":"🏛️ Kültürel Miras","dans_folklor":"💃 Dans & Folklor","el_sanatlari":"🧵 El Sanatları"}
        for key, cat_title in ks_map.items():
            items = KULTUR_SANAT.get(key, [])
            if items:
                _cat(cat_title)
                for title, content, fact in items:
                    with st.expander(title):
                        st.markdown(content)
                        st.info(f"💡 {fact}")

    # ── K3: Bilim & Teknik (GENEL) ──
    with tabs[3]:
        st.markdown(_compartment_header(2, grade), unsafe_allow_html=True)
        bt_map = {"kesifler":"🔭 Bilimsel Keşifler","icatlar":"💡 İcatlar","teknoloji":"💻 Teknoloji","bilim_insanlari":"👨‍🔬 Bilim İnsanları"}
        for key, cat_title in bt_map.items():
            items = BILIM_TEKNIK.get(key, [])
            if items:
                _cat(cat_title)
                for title, content, fact in items:
                    with st.expander(title):
                        st.markdown(content)
                        st.info(f"💡 {fact}")

    # ── K4: Edebiyat (GENEL — 100 şiir, 100 roman, hikaye, atasözü, yazar, akım) ──
    with tabs[4]:
        st.markdown(_compartment_header(3, grade), unsafe_allow_html=True)
        ed_tabs = st.tabs(["📜 100 Şiir", "📖 100 Roman Özeti", "📚 Hikayeler", "🗣️ Atasözleri", "✍️ Yazarlar", "📚 Akımlar"])

        with ed_tabs[0]:
            siirler = EDEBIYAT.get("siirler_100", [])
            st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">📜 {len(siirler)} şiir — Türk ve Dünya edebiyatından seçmeler</div>', unsafe_allow_html=True)
            # Arama
            siir_q = st.text_input("🔍 Şiir/Şair ara:", key="siir_search", placeholder="Örn: Nâzım, Yunus Emre, aşk, bayrak...")
            if siir_q and len(siir_q) >= 2:
                filtered = [s for s in siirler if siir_q.lower() in f"{s[0]} {s[1]} {s[2]}".lower()]
                st.caption(f"{len(filtered)} sonuç bulundu")
            else:
                filtered = siirler
            for s in filtered:
                is_full = len(s) < 4 or s[3] is None
                badge = "✅ Tam Metin" if is_full else "📋 İlk Kıta"
                badge_color = "#10b981" if is_full else "#f97316"
                with st.expander(f"📜 {s[0]} — {s[1]}"):
                    st.markdown(f'<span style="background:rgba({badge_color.replace("#","")},0.15);border:1px solid {badge_color};border-radius:12px;padding:2px 10px;font-size:0.7rem;color:{badge_color};font-weight:600;">{badge}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:2px solid #6366F1;padding:12px 16px;font-style:italic;white-space:pre-wrap;color:#E2E8F0;line-height:1.8;font-size:0.95rem;margin-top:6px;">{s[2]}</div>', unsafe_allow_html=True)
                    if not is_full and len(s) >= 4 and s[3]:
                        st.markdown(f'<div style="background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:8px;padding:6px 12px;margin-top:6px;font-size:0.78rem;color:#f97316;">📖 {s[3]}</div>', unsafe_allow_html=True)
                    st.caption(f"Şair: {s[1]}")

        with ed_tabs[1]:
            romanlar = EDEBIYAT.get("roman_ozetleri_100", [])
            st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">📖 {len(romanlar)} roman özeti — Türk ve Dünya edebiyatı</div>', unsafe_allow_html=True)
            roman_q = st.text_input("🔍 Roman/Yazar ara:", key="roman_search", placeholder="Örn: Yaşar Kemal, Dostoyevski, aşk, savaş...")
            if roman_q and len(roman_q) >= 2:
                r_filtered = [r for r in romanlar if roman_q.lower() in f"{r[0]} {r[1]} {r[3]} {r[4]}".lower()]
                st.caption(f"{len(r_filtered)} sonuç bulundu")
            else:
                r_filtered = romanlar
            for r in r_filtered:
                with st.expander(f"📖 {r[0]} — {r[1]} ({r[2]})"):
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:12px 16px;border-radius:0 10px 10px 0;font-size:0.9rem;line-height:1.7;color:#E2E8F0;">{r[3]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="margin-top:6px;"><span style="background:rgba(212,175,55,0.12);border:1px solid rgba(212,175,55,0.25);border-radius:20px;padding:3px 12px;font-size:0.78rem;color:#6366F1;font-weight:600;">🎯 {r[4]}</span></div>', unsafe_allow_html=True)

        with ed_tabs[2]:
            if EDEBIYAT.get("hikayeler"):
                for h in EDEBIYAT["hikayeler"]:
                    with st.expander(f"📖 {h[0]}"):
                        st.markdown(h[1])
                        st.success(f"💡 {h[2]}")

        with ed_tabs[3]:
            if EDEBIYAT.get("atasozleri"):
                for a in EDEBIYAT["atasozleri"]:
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:2px solid #6366F1;padding:6px 12px;border-radius:0 6px 6px 0;margin:3px 0;"><b style="color:#6366F1;">"{a[0]}"</b> — <span style="color:#94A3B8;">{a[1]}</span></div>', unsafe_allow_html=True)

        with ed_tabs[4]:
            if EDEBIYAT.get("yazarlar"):
                for w in EDEBIYAT["yazarlar"]:
                    with st.expander(f"✍️ {w[0]}"):
                        st.markdown(w[1])

        with ed_tabs[5]:
            if EDEBIYAT.get("edebi_akimlar"):
                for a in EDEBIYAT["edebi_akimlar"]:
                    with st.expander(a[0]):
                        st.markdown(a[1])

    # ── K5: Bilgi Yarışması (GENEL — her turda farklı sorular) ──
    with tabs[5]:
        st.markdown(_compartment_header(4, grade), unsafe_allow_html=True)
        components.html(_build_quiz_html(), height=600, scrolling=True)

    # ── K6: Eğlence & Oyun (GENEL — 8 oyun) ──
    with tabs[6]:
        st.markdown(_compartment_header(5, grade), unsafe_allow_html=True)
        game_tabs = st.tabs([
            "🧠 Hafıza", "🧩 Bilmece", "🔤 Kelime Avı", "🎯 Doğru-Yanlış",
            "⚡ Hızlı Hesap", "🎨 Renk Testi", "🔢 Sayı Sırala", "🎯 Emoji Tahmin",
        ])
        with game_tabs[0]:
            components.html(_game_memory(), height=520, scrolling=True)
        with game_tabs[1]:
            # Use local riddle builder (enhanced version)
            components.html(_build_riddle_html(), height=600, scrolling=True)
        with game_tabs[2]:
            components.html(_game_word(), height=480, scrolling=True)
        with game_tabs[3]:
            components.html(_game_tf(), height=500, scrolling=True)
        with game_tabs[4]:
            components.html(_game_speed(), height=480, scrolling=True)
        with game_tabs[5]:
            components.html(_game_stroop(), height=480, scrolling=True)
        with game_tabs[6]:
            components.html(_game_sort(), height=500, scrolling=True)
        with game_tabs[7]:
            components.html(_game_emoji(), height=520, scrolling=True)

    # ── K7: Matematik Atölyesi (GENEL — 6 oyun) ──
    with tabs[7]:
        st.markdown(_compartment_header(6, grade), unsafe_allow_html=True)
        math_tabs = st.tabs([
            "🧮 Soru-Cevap", "⚡ Hız Yarışı", "🎯 Sayı Tahmin",
            "🧩 Denklem Çöz", "✖️ Çarpım Ustası", "🔗 Mat. Zinciri",
        ])
        with math_tabs[0]:
            components.html(_math_classic(), height=480, scrolling=True)
        with math_tabs[1]:
            components.html(_math_race(), height=500, scrolling=True)
        with math_tabs[2]:
            components.html(_math_guess(), height=520, scrolling=True)
        with math_tabs[3]:
            components.html(_math_eq(), height=480, scrolling=True)
        with math_tabs[4]:
            components.html(_math_mult(), height=460, scrolling=True)
        with math_tabs[5]:
            components.html(_math_chain(), height=520, scrolling=True)

    # ── K8: Yabancı Dil (6 dil, sesli telaffuz, okunuş) ──
    with tabs[8]:
        st.markdown(_compartment_header(7, grade), unsafe_allow_html=True)
        import random as _rnd2
        words = list(MULTI_LANG_WORDS); _rnd2.shuffle(words); words = words[:20]
        wj = _json.dumps(words, ensure_ascii=False)
        lj = _json.dumps(LANG_CONFIG, ensure_ascii=False)
        components.html(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',system-ui,sans-serif;padding:14px;text-align:center}}
.title{{font-size:1.2rem;font-weight:800;color:#6366F1;margin-bottom:4px}}
.sub{{color:#94A3B8;font-size:0.75rem;margin-bottom:12px}}
.card{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:16px;padding:18px;max-width:500px;margin:0 auto}}
.tr-word{{font-size:2.2rem;font-weight:900;color:#6366F1;margin:10px 0;text-shadow:0 0 10px rgba(212,175,55,0.3)}}
.tr-label{{font-size:0.7rem;color:#94A3B8;margin-bottom:6px}}
.lang-grid{{display:flex;flex-direction:column;gap:8px;margin:12px 0;text-align:left}}
.lang-row{{display:flex;align-items:center;gap:10px;background:#131825;border:1px solid rgba(212,175,55,0.1);border-radius:10px;padding:8px 12px;transition:.2s}}
.lang-row:hover{{border-color:rgba(212,175,55,0.3);background:rgba(212,175,55,0.03)}}
.flag{{font-size:1.4rem;min-width:28px}}
.lang-name{{font-size:0.65rem;color:#94A3B8;min-width:65px}}
.word{{font-size:1rem;font-weight:700;color:#E2E8F0;min-width:100px}}
.phonetic{{font-size:0.8rem;color:#6366F1;font-style:italic;opacity:0.8}}
.speak{{background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.3);border-radius:50%;width:30px;height:30px;cursor:pointer;font-size:0.9rem;color:#6366F1;display:flex;align-items:center;justify-content:center;transition:.2s;margin-left:auto;flex-shrink:0}}
.speak:hover{{background:rgba(212,175,55,0.25);transform:scale(1.1)}}
.nav{{display:flex;justify-content:center;gap:10px;margin-top:14px}}
.nav-btn{{background:#131825;border:2px solid rgba(212,175,55,0.3);border-radius:10px;padding:7px 18px;color:#6366F1;font-weight:700;cursor:pointer;font-size:0.85rem;transition:.2s}}
.nav-btn:hover{{background:rgba(212,175,55,0.1);border-color:#6366F1}}
.counter{{color:#94A3B8;font-size:0.75rem;margin-top:6px}}
.speak-all{{background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:10px;padding:8px 16px;font-weight:700;cursor:pointer;margin-top:8px;font-size:0.8rem}}
</style></head><body>
<div class="title">🌍 Çok Dilli Kelime Kartları</div>
<div class="sub">6 dilde öğren — 🔊 sesli telaffuz — her seferinde farklı 20 kelime</div>
<div class="card">
    <div class="tr-label">🇹🇷 TÜRKÇE</div>
    <div class="tr-word" id="trw"></div>
    <div class="lang-grid" id="grid"></div>
    <button class="speak-all" onclick="speakAll()">🔊 Tüm Dillerde Dinle</button>
</div>
<div class="nav">
    <button class="nav-btn" onclick="prev()">◀ Önceki</button>
    <button class="nav-btn" onclick="next()">Sonraki ▶</button>
</div>
<div class="counter" id="cnt"></div>
<script>
const W={wj};
const L={lj};
const langs=['en','de','es','it','fr'];
let idx=0;
// Premium kadın sesi seçici
let voiceCache={{}};
function getBestVoice(langCode){{
    if(voiceCache[langCode])return voiceCache[langCode];
    const voices=speechSynthesis.getVoices();
    // Kadın sesi tercih et
    const femaleHints=['female','kadın','woman','Filiz','Emel','Hedda','Helena','Paulina','Elsa','Cosimo','Google'];
    let best=voices.find(v=>v.lang.startsWith(langCode.split('-')[0])&&femaleHints.some(h=>v.name.toLowerCase().includes(h.toLowerCase())));
    if(!best)best=voices.find(v=>v.lang.startsWith(langCode.split('-')[0]));
    if(best)voiceCache[langCode]=best;
    return best;
}}
speechSynthesis.onvoiceschanged=()=>voiceCache={{}};

function speak(text,langCode){{
    try{{
        const u=new SpeechSynthesisUtterance(text);
        u.lang=langCode;
        u.rate=0.82;
        u.pitch=1.12;
        u.volume=1.0;
        const v=getBestVoice(langCode);
        if(v)u.voice=v;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(u);
    }}catch(e){{}}
}}
function speakAll(){{
    const w=W[idx];let delay=0;
    langs.forEach(lang=>{{
        setTimeout(()=>speak(w[lang],L[lang].code),delay);
        delay+=1500;
    }});
}}
function render(){{
    const w=W[idx];
    document.getElementById('trw').textContent=w.tr;
    const grid=document.getElementById('grid');
    grid.innerHTML='';
    langs.forEach(lang=>{{
        const cfg=L[lang];
        const row=document.createElement('div');
        row.className='lang-row';
        row.innerHTML=`
            <span class="flag">${{cfg.flag}}</span>
            <span class="lang-name">${{cfg.name}}</span>
            <span class="word">${{w[lang]}}</span>
            <span class="phonetic">[${{w[lang+'_ph']}}]</span>
            <button class="speak" onclick="event.stopPropagation();speak('${{w[lang].replace("'","\\\\'")}}',${{JSON.stringify(cfg.code)}})" title="${{cfg.name}} telaffuz">🔊</button>
        `;
        grid.appendChild(row);
    }});
    document.getElementById('cnt').textContent=(idx+1)+' / '+W.length;
}}
function next(){{idx=(idx+1)%W.length;render();}}
function prev(){{idx=(idx-1+W.length)%W.length;render();}}
render();
</script></body></html>""", height=580, scrolling=True)

        # CEFR Flashcard section
        cefr_level = GRADE_CEFR.get(grade, "A1")
        cefr_data = _load_cefr_words()
        if cefr_data:
            level_words = cefr_data.get(cefr_level, {})
            if level_words:
                first_cat = next(iter(level_words), None)
                if first_cat:
                    cards = [{"en": w, "tr": w} for w in level_words[first_cat][:20]] if isinstance(level_words[first_cat], list) else []
                    if cards:
                        st.markdown(f"**CEFR {cefr_level} Flashcards**")
                        components.html(_build_cefr_flashcard_html(grade, cefr_level, first_cat, cards), height=400, scrolling=False)

    # ── K9: Deney Lab (GENEL — kategorili, zorluklu, 40+ deney) ──
    with tabs[9]:
        st.markdown(_compartment_header(8, grade), unsafe_allow_html=True)
        # Quick interactive view option
        if st.checkbox("Kompakt HTML gorunumu", key=f"bt_sci_html_{grade}"):
            components.html(_build_science_html(), height=600, scrolling=True)
        # Kategori filtresi
        cat_map = {"tumu": "🧪 Tümü", "fizik": "⚡ Fizik", "kimya": "⚗️ Kimya", "biyoloji": "🧬 Biyoloji", "doga": "🌿 Doğa", "muhendislik": "🔧 Mühendislik", "uzay": "🚀 Uzay"}
        diff_stars = {1: "⭐", 2: "⭐⭐", 3: "⭐⭐⭐"}
        c1, c2 = st.columns([0.6, 0.4])
        with c1:
            sel_cat = st.selectbox("Kategori:", list(cat_map.keys()), format_func=lambda x: cat_map[x], key="deney_cat")
        with c2:
            sel_diff = st.selectbox("Zorluk:", [0, 1, 2, 3], format_func=lambda x: "Tümü" if x == 0 else diff_stars[x], key="deney_diff")
        filtered = [e for e in SCIENCE if (sel_cat == "tumu" or e[1] == sel_cat) and (sel_diff == 0 or e[2] == sel_diff)]
        st.caption(f"📊 {len(filtered)} deney bulundu")
        for exp in filtered:
            title, cat, diff, materials, steps, result, safety = exp
            cat_icon = {"fizik": "⚡", "kimya": "⚗️", "biyoloji": "🧬", "doga": "🌿", "muhendislik": "🔧", "uzay": "🚀"}.get(cat, "🧪")
            stars = diff_stars.get(diff, "⭐")
            with st.expander(f"{title} | {cat_icon} {cat.capitalize()} | {stars}"):
                if safety:
                    st.markdown(f'<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:8px 12px;margin-bottom:8px;font-size:0.8rem;color:#ef4444;font-weight:600;">⚠️ {safety}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:rgba(212,175,55,0.06);border-left:3px solid #6366F1;padding:8px 12px;border-radius:0 8px 8px 0;margin-bottom:8px;font-size:0.8rem;color:#c0c0d8;">📦 <b>Malzemeler:</b> {materials}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:rgba(212,175,55,0.03);padding:10px 12px;border-radius:8px;margin-bottom:8px;font-size:0.85rem;line-height:1.7;color:#E2E8F0;">🔬 <b>Adımlar:</b><br>{steps}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:rgba(16,185,129,0.08);border-left:3px solid #10b981;padding:8px 12px;border-radius:0 8px 8px 0;font-size:0.85rem;color:#10b981;font-weight:600;line-height:1.6;">💡 <b>Bilimsel Açıklama:</b> {result}</div>', unsafe_allow_html=True)

    # ── K10: Genel Kültür (GENEL — 10 kategori, 250+ madde) ──
    with tabs[10]:
        st.markdown(_compartment_header(9, grade), unsafe_allow_html=True)
        gk_tabs = st.tabs([
            "🤯 İlginç", "🏆 Rekorlar", "💡 Biliyor Muydun", "📅 Tarihte Bugün", "🇹🇷 Türkiye",
            "🌍 Ülkeler", "💡 Buluşlar", "🌏 Yeryüzü", "🔢 Sayılar", "💬 Sözler", "🧭 Keşifler", "⚽ Spor",
            "🍽️ Yemek", "🎬 Sinema", "🧠 Psikoloji", "🌿 Çevre", "💰 Ekonomi", "🔮 Mitoloji", "🏗️ Mimari", "🐾 Hayvanlar",
        ])
        with gk_tabs[0]:
            import random as _rnd
            items = list(GENEL_KULTUR.get("ilginc", []))
            _rnd.shuffle(items)
            for i, b in enumerate(items[:20]):
                st.markdown(f"**{i+1}.** {b}")
            if len(items) > 20:
                with st.expander(f"➕ Tümünü göster ({len(items)} bilgi)"):
                    for i, b in enumerate(items):
                        st.markdown(f"{i+1}. {b}")
        with gk_tabs[1]:
            for r in GENEL_KULTUR.get("rekorlar", []):
                st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:6px 12px;border-radius:0 6px 6px 0;margin:4px 0;"><b style="color:#6366F1">{r[0]}</b> — {r[1]}</div>', unsafe_allow_html=True)
        with gk_tabs[2]:
            items2 = list(GENEL_KULTUR.get("biliyor_muydun", []))
            _rnd.shuffle(items2)
            for b in items2[:15]:
                st.markdown(f"💡 {b}")
            if len(items2) > 15:
                with st.expander(f"➕ Daha fazla ({len(items2)} bilgi)"):
                    for b in items2:
                        st.markdown(f"• {b}")
        with gk_tabs[3]:
            for t in GENEL_KULTUR.get("tarihte_bugun", []):
                st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:6px 12px;border-radius:0 6px 6px 0;margin:4px 0;"><b style="color:#6366F1">{t[0]}</b> — {t[1]}</div>', unsafe_allow_html=True)
        with gk_tabs[4]:
            for item in GENEL_KULTUR.get("turkiye", []):
                with st.expander(item[0]):
                    st.markdown(item[1])
        with gk_tabs[5]:
            for item in GENEL_KULTUR.get("ulkeler", []):
                with st.expander(item[0]):
                    st.markdown(item[1])
        with gk_tabs[6]:
            _cat("💡 İcatlar ve Buluşlar Zaman Çizgisi")
            for item in GENEL_KULTUR.get("bulus_zamancizgisi", []):
                st.markdown(f'<div style="display:flex;gap:12px;align-items:center;margin:4px 0;padding:6px 10px;background:rgba(212,175,55,0.03);border-radius:6px;"><span style="min-width:70px;color:#6366F1;font-weight:800;font-size:0.85rem;">{item[0]}</span><span style="color:#E2E8F0;font-weight:600;">{item[1]}</span><span style="color:#94A3B8;font-size:0.8rem;">— {item[2]}</span></div>', unsafe_allow_html=True)
        with gk_tabs[7]:
            for item in GENEL_KULTUR.get("yeryuzu", []):
                with st.expander(item[0]):
                    st.markdown(item[1])
        with gk_tabs[8]:
            for item in GENEL_KULTUR.get("sayilar", []):
                with st.expander(item[0]):
                    st.markdown(item[1])
        with gk_tabs[9]:
            for item in GENEL_KULTUR.get("meshur_sozler", []):
                st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:8px 14px;border-radius:0 8px 8px 0;margin:5px 0;"><span style="color:#E2E8F0;font-style:italic;">"{item[1]}"</span><br><span style="color:#6366F1;font-weight:700;font-size:0.8rem;">— {item[0]}</span></div>', unsafe_allow_html=True)

        with gk_tabs[10]:
            kesifler = GENEL_KULTUR.get("kesifler_kasifler", [])
            st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">🧭 {len(kesifler)} keşif & kaşif — coğrafya, bilim, teknoloji, uzay, tarihî ilkler</div>', unsafe_allow_html=True)
            kesif_q = st.text_input("🔍 Keşif/Kaşif ara:", key="kesif_search", placeholder="Örn: Kolomb, DNA, Ay, Tesla, matbaa...")
            if kesif_q and len(kesif_q) >= 2:
                filtered_k = [k for k in kesifler if kesif_q.lower() in f"{k[0]} {k[1]}".lower()]
                st.caption(f"{len(filtered_k)} sonuç")
            else:
                filtered_k = kesifler
            for item in filtered_k:
                with st.expander(item[0]):
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.7;color:#E2E8F0;">{item[1]}</div>', unsafe_allow_html=True)

        with gk_tabs[11]:
            sporlar = GENEL_KULTUR.get("spor", [])
            st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">⚽ {len(sporlar)} spor konusu</div>', unsafe_allow_html=True)
            spor_q = st.text_input("🔍 Spor ara:", key="spor_search", placeholder="Örn: futbol, Messi, olimpiyat...")
            filtered_s = [s for s in sporlar if not spor_q or len(spor_q) < 2 or spor_q.lower() in f"{s[0]} {s[1]}".lower()]
            for item in filtered_s:
                with st.expander(item[0]):
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.7;color:#E2E8F0;">{item[1]}</div>', unsafe_allow_html=True)

        # Yardımcı: expander listesi render eden fonksiyon
        def _render_gk_tab(tab_idx, data_key, emoji, label, search_key, search_hint):
            with gk_tabs[tab_idx]:
                items = GENEL_KULTUR.get(data_key, [])
                st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">{emoji} {len(items)} madde</div>', unsafe_allow_html=True)
                sq = st.text_input(f"🔍 {label} ara:", key=search_key, placeholder=search_hint)
                flt = [i for i in items if not sq or len(sq) < 2 or sq.lower() in f"{i[0]} {i[1]}".lower()]
                for item in flt:
                    with st.expander(item[0]):
                        st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.7;color:#E2E8F0;">{item[1]}</div>', unsafe_allow_html=True)

        _render_gk_tab(12, "yemek_mutfak", "🍽️", "Yemek", "yemek_s", "Örn: pizza, baklava, kahve...")
        _render_gk_tab(13, "sinema_dizi", "🎬", "Sinema", "sinema_s", "Örn: Oscar, Yeşilçam, Marvel...")
        _render_gk_tab(14, "psikoloji", "🧠", "Psikoloji", "psiko_s", "Örn: beyin, uyku, stres...")
        _render_gk_tab(15, "cevre", "🌿", "Çevre", "cevre_s", "Örn: iklim, plastik, enerji...")
        _render_gk_tab(16, "ekonomi", "💰", "Ekonomi", "eko_s", "Örn: borsa, startup, para...")
        _render_gk_tab(17, "mitoloji", "🔮", "Mitoloji", "mito_s", "Örn: Zeus, Truva, Bozkurt...")
        _render_gk_tab(18, "mimari", "🏗️", "Mimari", "mim_s", "Örn: piramit, Sinan, Eiffel...")
        _render_gk_tab(19, "hayvanlar", "🐾", "Hayvan", "hayvan_s", "Örn: balina, kartal, arı...")

    # ══════════════════════════════════════════════════════════════════
    # K11: SESLİ İÇERİK (Podcast — TTS)
    # ══════════════════════════════════════════════════════════════════
    with tabs[11]:
        st.markdown(
            '<div style="background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:12px 16px;margin-bottom:12px;">'
            '<div style="font-size:1rem;font-weight:800;color:#6366F1;">📻 Sesli İçerik — Mini Podcast</div>'
            '<div style="font-size:0.78rem;color:#94A3B8;">🔊 butonu ile sesli dinle (tarayıcı TTS)</div></div>', unsafe_allow_html=True)
        for pod in PODCAST_SCRIPTS:
            with st.expander(f"🎙️ {pod['title']} ({pod['duration']})"):
                st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:10px 14px;border-radius:0 8px 8px 0;font-size:0.9rem;line-height:1.7;color:#E2E8F0;">{pod["text"]}</div>', unsafe_allow_html=True)
                # TTS butonu — premium kadın sesi
                tts_text = pod["text"].replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
                components.html(f"""
<div style="display:flex;gap:6px;align-items:center;font-family:'Segoe UI',sans-serif;">
<button id="playBtn" onclick="premiumSpeak()" style="background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:10px;padding:10px 20px;font-weight:700;cursor:pointer;font-size:0.85rem;transition:.2s;display:flex;align-items:center;gap:6px;">
<span id="playIcon">🔊</span> <span id="playText">Sesli Dinle</span></button>
<button onclick="speechSynthesis.cancel();document.getElementById('playIcon').textContent='🔊';document.getElementById('playText').textContent='Sesli Dinle';" style="background:#232B3E;color:#6366F1;border:1px solid rgba(212,175,55,0.3);border-radius:10px;padding:10px 14px;cursor:pointer;font-size:0.85rem;">⏹️ Durdur</button>
<span id="status" style="font-size:0.7rem;color:#94A3B8;"></span>
</div>
<script>
let femaleVoice=null;
function loadVoices(){{
    const voices=speechSynthesis.getVoices();
    // Türkçe kadın sesi öncelik sırası
    const prefs=['Filiz','Microsoft Emel','Google Türkçe','tr-TR','Turkish'];
    for(const pref of prefs){{
        const v=voices.find(v=>(v.name.includes(pref)||v.lang.includes('tr'))&&
            (v.name.toLowerCase().includes('female')||v.name.includes('Filiz')||v.name.includes('Emel')||
             v.name.includes('Yelda')||v.name.includes('Seda')||!v.name.toLowerCase().includes('male')));
        if(v){{femaleVoice=v;break;}}
    }}
    // Fallback: herhangi bir Türkçe ses
    if(!femaleVoice)femaleVoice=voices.find(v=>v.lang.startsWith('tr'))||null;
}}
speechSynthesis.onvoiceschanged=loadVoices;
loadVoices();

function premiumSpeak(){{
    speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance('{tts_text}');
    u.lang='tr-TR';
    u.rate=0.92;
    u.pitch=1.15;
    u.volume=1.0;
    if(femaleVoice)u.voice=femaleVoice;
    document.getElementById('playIcon').textContent='🔈';
    document.getElementById('playText').textContent='Okunuyor...';
    document.getElementById('status').textContent=femaleVoice?'🎙️ '+femaleVoice.name:'';
    u.onend=()=>{{document.getElementById('playIcon').textContent='🔊';document.getElementById('playText').textContent='Tekrar Dinle';}};
    speechSynthesis.speak(u);
}}
</script>""", height=55)

    # ══════════════════════════════════════════════════════════════════
    # K12: KAVRAM HARİTASI
    # ══════════════════════════════════════════════════════════════════
    with tabs[12]:
        st.markdown(
            '<div style="background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:12px 16px;margin-bottom:12px;">'
            '<div style="font-size:1rem;font-weight:800;color:#6366F1;">🧩 Kavram Haritası</div>'
            '<div style="font-size:0.78rem;color:#94A3B8;">Bir kavram yaz → ilişkili konuları keşfet</div></div>', unsafe_allow_html=True)
        concept_q = st.text_input("Kavram ara:", key="bt_concept", placeholder="Örn: Hücre, Atom, Newton, Kesir, DNA...")
        if concept_q and len(concept_q) >= 2:
            related = get_related_concepts(concept_q)
            if related:
                st.markdown(f'<div style="margin:8px 0;font-size:0.85rem;color:#10b981;">🔗 <b>{concept_q}</b> ile ilişkili {len(related)} kavram:</div>', unsafe_allow_html=True)
                cols_per_row = 4
                for i in range(0, len(related), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        idx = i + j
                        if idx < len(related):
                            with col:
                                st.markdown(f'<div style="background:rgba(212,175,55,0.06);border:1px solid rgba(212,175,55,0.2);border-radius:10px;padding:8px;text-align:center;font-weight:600;color:#6366F1;font-size:0.85rem;">{related[idx]}</div>', unsafe_allow_html=True)
                # Video önerisi
                videos = get_video_suggestions(concept_q)
                if videos:
                    st.markdown("---")
                    st.markdown("**🎬 Bu konuyla ilgili video önerileri:**")
                    for vid in videos:
                        v_title, v_desc, v_url = vid[0], vid[1], vid[2]
                        v_lang = vid[4] if len(vid) > 4 else ""
                        st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:8px 12px;border-radius:0 6px 6px 0;margin:4px 0;">📺 <a href="{v_url}" target="_blank" style="color:#6366F1;font-weight:700;text-decoration:none;">{v_title}</a> {v_lang}<br><span style="color:#94A3B8;font-size:0.8rem;">{v_desc}</span></div>', unsafe_allow_html=True)
            else:
                st.info("Bu kavram haritada bulunamadı. Farklı kelimeler deneyin.")
        else:
            st.markdown("**Mevcut kavram ağacı:**")
            for concept, links in list(CONCEPT_MAP.items())[:10]:
                st.markdown(f'**{concept}** → {", ".join(links)}')

    # ══════════════════════════════════════════════════════════════════
    # K13: VİDEO & KAYNAK (Dijital Kütüphane + Video)
    # ══════════════════════════════════════════════════════════════════
    with tabs[13]:
        st.markdown(
            '<div style="background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:12px 16px;margin-bottom:12px;">'
            '<div style="font-size:1rem;font-weight:800;color:#6366F1;">🎬 Video & Kaynak Kütüphanesi</div>'
            '<div style="font-size:0.78rem;color:#94A3B8;">Konu bazlı video önerileri + kitap tavsiyeleri</div></div>', unsafe_allow_html=True)
        vk_tabs = st.tabs(["📺 Video Önerileri", "📚 Dijital Kütüphane"])
        with vk_tabs[0]:
            st.markdown(f'<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:8px;">🎬 {len(VIDEO_SUGGESTIONS)} konu, {sum(len(v) for v in VIDEO_SUGGESTIONS.values())}+ video — tıkla izle!</div>', unsafe_allow_html=True)
            for topic, videos in VIDEO_SUGGESTIONS.items():
                with st.expander(f"📺 {topic} ({len(videos)} video)"):
                    for vid in videos:
                        v_title, v_desc, v_url = vid[0], vid[1], vid[2]
                        v_platform = vid[3] if len(vid) > 3 else "YouTube"
                        v_lang = vid[4] if len(vid) > 4 else ""
                        st.markdown(
                            f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:8px 12px;border-radius:0 8px 8px 0;margin:5px 0;">'
                            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                            f'<div><a href="{v_url}" target="_blank" style="color:#6366F1;font-weight:700;text-decoration:none;font-size:0.95rem;">▶️ {v_title}</a>'
                            f'<span style="font-size:0.7rem;color:#94A3B8;margin-left:8px;">{v_lang}</span></div>'
                            f'<a href="{v_url}" target="_blank" style="background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;padding:4px 12px;border-radius:6px;font-size:0.7rem;font-weight:700;text-decoration:none;">İZLE →</a>'
                            f'</div>'
                            f'<div style="color:#94A3B8;font-size:0.78rem;margin-top:3px;">{v_desc}</div>'
                            f'</div>', unsafe_allow_html=True)
        with vk_tabs[1]:
            for category, books in LIBRARY.items():
                with st.expander(f"📚 {category} ({len(books)} kitap)"):
                    for b_icon_title, author, desc in books:
                        st.markdown(f"**{b_icon_title}** — *{author}*")
                        st.caption(desc)

    # ══════════════════════════════════════════════════════════════════
    # K14: BAŞARILAR & ÇALIŞMA PLANI & KİŞİSEL ÖNERİ
    # ══════════════════════════════════════════════════════════════════
    with tabs[14]:
        st.markdown(
            '<div style="background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:12px;padding:12px 16px;margin-bottom:12px;">'
            '<div style="font-size:1rem;font-weight:800;color:#6366F1;">🏅 Başarılar & Kişisel Plan</div>'
            '<div style="font-size:0.78rem;color:#94A3B8;">Rozetler, çalışma planı, kişisel öneriler</div></div>', unsafe_allow_html=True)
        bp_tabs = st.tabs(["🏅 Rozetler", "📋 Çalışma Planı", "🌟 Kişisel Öneriler", "👥 Quiz Düellosu"])

        with bp_tabs[0]:
            # İstatistik takibi (session state)
            if "bt_stats" not in st.session_state:
                st.session_state["bt_stats"] = {"visit_count": 1, "quiz_count": 0, "game_count": 0, "math_count": 0, "deney_count": 0, "lang_count": 0, "streak": 1, "compartments_visited": 1, "quiz_avg_pct": 0, "math_avg_pct": 0}
            stats = st.session_state["bt_stats"]
            earned = check_badges(stats)
            st.markdown(f"**Kazanılan Rozetler: {len(earned)}/{len(BADGES)}**")
            cols = st.columns(4)
            for i, b in enumerate(BADGES):
                with cols[i % 4]:
                    is_earned = b in earned
                    opacity = "1" if is_earned else "0.3"
                    border = "#6366F1" if is_earned else "rgba(212,175,55,0.15)"
                    st.markdown(f'<div style="background:rgba(212,175,55,0.04);border:2px solid {border};border-radius:12px;padding:10px;text-align:center;margin:4px 0;opacity:{opacity};"><div style="font-size:1.8rem;">{b["icon"]}</div><div style="font-size:0.75rem;font-weight:700;color:#6366F1;margin-top:2px;">{b["name"]}</div><div style="font-size:0.65rem;color:#94A3B8;">{b["desc"]}</div></div>', unsafe_allow_html=True)

        with bp_tabs[1]:
            st.markdown("**📋 Kişisel Çalışma Planı Oluştur**")
            c1, c2 = st.columns(2)
            with c1:
                days = st.slider("Haftada kaç gün?", 1, 7, 3, key="plan_days")
            with c2:
                mins = st.slider("Günde kaç dakika?", 10, 60, 30, key="plan_mins")
            focus = st.multiselect("Odak alanları:", ["Fen Bilimleri", "Matematik", "Edebiyat", "Tarih", "Genel Kültür", "Yabancı Dil", "Bilim & Teknik"], default=["Fen Bilimleri", "Matematik", "Yabancı Dil"], key="plan_focus")
            if st.button("📋 Plan Oluştur", key="gen_plan"):
                plan = generate_study_plan(days, mins, focus if focus else None)
                for p in plan:
                    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;background:rgba(212,175,55,0.04);border-left:3px solid #6366F1;padding:8px 14px;border-radius:0 8px 8px 0;margin:4px 0;"><b style="color:#6366F1;min-width:80px;">{p["day"]}</b><span>{p["area"]}</span><span style="color:#94A3B8;">— {p["activity"]} ({p["duration"]} dk)</span></div>', unsafe_allow_html=True)

        with bp_tabs[2]:
            st.markdown("**🌟 Sana Özel Öneriler**")
            stats = st.session_state.get("bt_stats", {})
            recs = get_recommendations(stats)
            for r in recs:
                color = {"high": "#ef4444", "medium": "#f97316", "low": "#94A3B8", "positive": "#10b981"}.get(r["priority"], "#94A3B8")
                st.markdown(f'<div style="background:rgba(212,175,55,0.04);border-left:3px solid {color};padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;"><div style="font-size:1rem;font-weight:700;color:#E2E8F0;">{r["icon"]} {r["title"]}</div><div style="font-size:0.85rem;color:#94A3B8;margin-top:3px;">{r["desc"]}</div></div>', unsafe_allow_html=True)

        with bp_tabs[3]:
            st.markdown("**👥 Quiz Düellosu — 2 Oyuncu**")
            st.info("Aynı ekranda 2 kişi aynı soruları çözer, kim daha çok bilir?")
            if st.button("🎯 Düello Başlat", key="duel_start"):
                duel_qs = generate_duel_questions(8)
                duel_json = _json.dumps(duel_qs, ensure_ascii=False)
                components.html(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',sans-serif;padding:14px}}
.header{{text-align:center;margin-bottom:14px}}.title{{font-size:1.2rem;font-weight:800;color:#6366F1}}
.players{{display:flex;gap:12px;margin:10px 0}}.player{{flex:1;background:#131825;border:2px solid rgba(212,175,55,0.2);border-radius:12px;padding:14px;text-align:center}}
.player h3{{color:#6366F1;font-size:0.9rem;margin-bottom:6px}}.pscore{{font-size:2rem;font-weight:900;color:#6366F1}}
.question{{background:#131825;border:1px solid rgba(212,175,55,0.2);border-radius:14px;padding:18px;margin:10px 0;text-align:center}}
.qt{{font-size:1.1rem;font-weight:700;margin-bottom:14px}}.qn{{color:#6366F1;font-size:0.75rem;margin-bottom:6px}}
.opts{{display:flex;flex-direction:column;gap:6px}}.opt{{background:#131825;border:2px solid rgba(212,175,55,0.15);border-radius:10px;padding:10px;cursor:pointer;font-size:0.9rem;transition:.2s}}
.opt:hover{{border-color:#6366F1;transform:translateX(3px)}}.opt.c{{border-color:#10b981;background:rgba(16,185,129,0.15);color:#10b981}}.opt.w{{border-color:#ef4444;background:rgba(239,68,68,0.15);color:#ef4444}}
.turn{{text-align:center;font-size:0.85rem;color:#6366F1;margin:8px 0;font-weight:700}}
.btn{{background:linear-gradient(135deg,#A5B4FC,#6366F1);color:#0B0F19;border:none;border-radius:10px;padding:9px 20px;font-weight:700;cursor:pointer;margin-top:10px}}
</style></head><body>
<div class="header"><div class="title">👥 Quiz Düellosu</div></div>
<div class="players"><div class="player"><h3>🔵 Oyuncu 1</h3><div class="pscore" id="s1">0</div></div><div class="player"><h3>🔴 Oyuncu 2</h3><div class="pscore" id="s2">0</div></div></div>
<div class="turn" id="turn">🔵 Oyuncu 1'in sırası</div>
<div id="area"></div>
<script>
const Q={duel_json};let idx=0,s1=0,s2=0,player=1;
function show(){{if(idx>=Q.length){{document.getElementById('area').innerHTML=`<div class="question"><div class="title">🏆 Düello Bitti!</div><div style="font-size:1.5rem;margin:10px;color:#6366F1">🔵 ${{s1}} — ${{s2}} 🔴</div><div style="font-size:1.2rem;color:#10b981;font-weight:800">${{s1>s2?'🔵 Oyuncu 1 Kazandı!':s2>s1?'🔴 Oyuncu 2 Kazandı!':'🤝 Berabere!'}}</div><button class="btn" onclick="location.reload()">🔄 Yeni Düello</button></div>`;return;}}
const q=Q[idx];document.getElementById('turn').textContent=(player===1?'🔵 Oyuncu 1':'🔴 Oyuncu 2')+"'in sırası";
let h=`<div class="question"><div class="qn">Soru ${{idx+1}}/${{Q.length}}</div><div class="qt">${{q.q}}</div><div class="opts">`;
q.opts.forEach((o,i)=>{{h+=`<div class="opt" onclick="pick(${{i}})">${{String.fromCharCode(65+i)}}) ${{o}}</div>`;}});
h+=`</div></div>`;document.getElementById('area').innerHTML=h;}}
function pick(i){{const q=Q[idx];const ok=i===q.ans;if(ok){{if(player===1)s1++;else s2++;}}
document.querySelectorAll('.opt').forEach((o,j)=>{{o.style.pointerEvents='none';if(j===q.ans)o.classList.add('c');if(j===i&&!ok)o.classList.add('w');}});
document.getElementById('s1').textContent=s1;document.getElementById('s2').textContent=s2;
setTimeout(()=>{{if(player===1){{player=2;}}else{{player=1;idx++;}}show();}},1000);}}
show();
</script></body></html>""", height=550, scrolling=True)

    # ══════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# TRAIN HUB RENDERER
# ══════════════════════════════════════════════════════════════════════════════

def _render_train_hub():
    components.html(_build_train_hub_html(), height=400, scrolling=False)

    # ── LOKOMOTİF: AI Bireysel Eğitim — sınıf bağımsız ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#131825,#1a1a50);border:2px solid #6366F1;'
        'border-radius:14px;padding:16px 20px;margin:8px 0;">'
        '<div style="font-size:1.1rem;font-weight:900;'
        'background:linear-gradient(135deg,#6366F1,#6366F1);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text;">🚂 LOKOMOTİF — AI Bireysel Eğitim</div>'
        '<div style="font-size:0.78rem;color:#94A3B8;margin-top:4px;">'
        'Sınıf seçmeden doğrudan AI destekli eğitime başla: Konu Anlat, Kazanım Anlat, 3D Görsel, Mini Quiz</div>'
        '</div>', unsafe_allow_html=True)
    if st.button("🚂 AI Bireysel Eğitim'e Gir", key="bt_lokomotif", use_container_width=True, type="primary"):
        st.session_state["bt_sinif"] = "lokomotif"
        st.rerun()

    # ── Vagon Seçimi ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#131825,#1A2035);padding:14px 18px;border-radius:14px;margin:6px 0;border:1px solid rgba(212,175,55,0.15);">'
        '<div style="font-size:1rem;font-weight:800;color:#6366F1;">🎫 Vagon Seçimi — Sınıfını seç, yolculuğa başla!</div>'
        '<div style="font-size:0.75rem;color:#94A3B8;">Her vagon 15 kompartıman: AI Bireysel Eğitim, Konu Anlatımı, Kültür & Sanat, Bilim & Teknik, Edebiyat, Quiz, Oyunlar, Matematik, Yabancı Dil, Deney Lab, Genel Kültür ve daha fazlası</div>'
        '</div>', unsafe_allow_html=True)
    for row in range(1, 13, 4):
        cols = st.columns(4)
        for i, col in enumerate(cols):
            g = row + i
            if g > 12: break
            with col:
                if st.button(f"{SINIF_LABELS[g]}", key=f"bt_w_{g}", use_container_width=True, type="primary"):
                    st.session_state["bt_sinif"] = g
                    st.rerun()

    # ── SÜPER ÖZELLİKLER ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#131825,#1A2035);padding:14px 18px;border-radius:14px;margin:10px 0;border:1px solid rgba(212,175,55,0.15);">'
        '<div style="font-size:1rem;font-weight:800;color:#c9a84c;">🌟 Tren Istasyonu Ozel Bolumler</div>'
        '<div style="font-size:0.75rem;color:#94A3B8;">Yolculuk haritasi, vagon yarisi, gunluk gorevler</div>'
        '</div>', unsafe_allow_html=True)
    _sp_cols = st.columns(3)
    with _sp_cols[0]:
        if st.button("🗺️ Yolculuk Haritasi", key="bt_sp_harita", use_container_width=True):
            st.session_state["bt_sinif"] = "harita"
            st.rerun()
    with _sp_cols[1]:
        if st.button("🏆 Vagon Yarisi", key="bt_sp_yaris", use_container_width=True):
            st.session_state["bt_sinif"] = "yaris"
            st.rerun()
    with _sp_cols[2]:
        if st.button("🤖 Gunluk Gorev", key="bt_sp_gorev", use_container_width=True):
            st.session_state["bt_sinif"] = "gorev"
            st.rerun()

    # ── MEGA ÖZELLİKLER ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#1a0a0a,#1A2035);padding:14px 18px;border-radius:14px;margin:10px 0;border:1px solid rgba(239,68,68,0.2);">'
        '<div style="font-size:1rem;font-weight:800;color:#ef4444;">⚔️ Mega Tren Ozellikleri</div>'
        '<div style="font-size:0.75rem;color:#94A3B8;">Multiplayer duello, makinist paneli, ulusal siralama</div>'
        '</div>', unsafe_allow_html=True)
    _mg_cols = st.columns(3)
    with _mg_cols[0]:
        if st.button("⚔️ Multiplayer Duello", key="bt_mg_duello", use_container_width=True):
            st.session_state["bt_sinif"] = "duello"
            st.rerun()
    with _mg_cols[1]:
        if st.button("📡 Makinist Paneli", key="bt_mg_makinist", use_container_width=True):
            st.session_state["bt_sinif"] = "makinist"
            st.rerun()
    with _mg_cols[2]:
        if st.button("🌍 Ulusal Siralama", key="bt_mg_ulusal", use_container_width=True):
            st.session_state["bt_sinif"] = "ulusal"
            st.rerun()

    # ── ZİRVE ÖZELLİKLER ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#1a1a2e,#c9a84c10);padding:14px 18px;border-radius:14px;margin:10px 0;border:1px solid rgba(201,168,76,0.3);">'
        '<div style="font-size:1rem;font-weight:800;color:#c9a84c;">👑 Zirve Tren Ozellikleri</div>'
        '<div style="font-size:0.75rem;color:#94A3B8;">Hikaye modu, kisisel rota, tren muzesi</div>'
        '</div>', unsafe_allow_html=True)
    _zr_cols = st.columns(3)
    with _zr_cols[0]:
        if st.button("🎭 Hikaye Modu", key="bt_zr_hikaye", use_container_width=True):
            st.session_state["bt_sinif"] = "hikaye"
            st.rerun()
    with _zr_cols[1]:
        if st.button("🧬 Kisisel Rota", key="bt_zr_rota", use_container_width=True):
            st.session_state["bt_sinif"] = "rota"
            st.rerun()
    with _zr_cols[2]:
        if st.button("🏛️ Tren Muzesi", key="bt_zr_muze", use_container_width=True):
            st.session_state["bt_sinif"] = "muze"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render_bilgi_treni():
    inject_common_css("bt")
    if "bt_sinif" not in st.session_state:
        st.session_state["bt_sinif"] = None
    qp = st.query_params.get("bt_grade", "")
    if qp and qp.isdigit():
        g = int(qp)
        if 1 <= g <= 12:
            st.session_state["bt_sinif"] = g
        try: del st.query_params["bt_grade"]
        except Exception: pass
        st.rerun()
    if st.session_state["bt_sinif"] is None:
        _render_train_hub()
    elif st.session_state["bt_sinif"] == "harita":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_harita", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_super_features import render_yolculuk_haritasi
            render_yolculuk_haritasi()
        except Exception as _e:
            st.error(f"Yolculuk Haritasi yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "yaris":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_yaris", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_super_features import render_vagon_yarisi
            render_vagon_yarisi()
        except Exception as _e:
            st.error(f"Vagon Yarisi yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "gorev":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_gorev", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_super_features import render_adaptif_motor
            render_adaptif_motor()
        except Exception as _e:
            st.error(f"Adaptif Motor yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "hikaye":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_hikaye", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_zirve_features import render_hikaye_modu
            render_hikaye_modu()
        except Exception as _e:
            st.error(f"Hikaye Modu yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "rota":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_rota", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_zirve_features import render_kisisel_rota
            render_kisisel_rota()
        except Exception as _e:
            st.error(f"Kisisel Rota yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "muze":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_muze", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_zirve_features import render_tren_muzesi
            render_tren_muzesi()
        except Exception as _e:
            st.error(f"Tren Muzesi yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "duello":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_duello", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_mega_features import render_multiplayer_quiz
            render_multiplayer_quiz()
        except Exception as _e:
            st.error(f"Multiplayer yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "makinist":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_makinist", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_mega_features import render_makinist_paneli
            render_makinist_paneli()
        except Exception as _e:
            st.error(f"Makinist Paneli yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "ulusal":
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_ulusal", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        try:
            from views._bt_mega_features import render_ulusal_siralama
            render_ulusal_siralama()
        except Exception as _e:
            st.error(f"Ulusal Siralama yuklenemedi: {_e}")
    elif st.session_state["bt_sinif"] == "lokomotif":
        # Lokomotif: AI Bireysel Eğitim — sınıf bağımsız
        c1, c2 = st.columns([0.18, 0.82])
        with c1:
            if st.button("🚂 Trene Dön", key="bt_back_loko", use_container_width=True, type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
        with c2:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#131825,#1a1a50);border:2px solid #6366F1;'
                'border-radius:10px;padding:8px 16px;display:inline-flex;align-items:center;gap:8px;">'
                '<span style="font-size:1.1rem;font-weight:900;'
                'background:linear-gradient(135deg,#6366F1,#6366F1);'
                '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
                'background-clip:text;">🚂 LOKOMOTİF — AI Bireysel Eğitim</span></div>',
                unsafe_allow_html=True)
        try:
            from views.dijital_kutuphane import render_ai_asistan
            render_ai_asistan()
        except Exception as _ai_err:
            st.error(f"AI Bireysel Eğitim yüklenirken hata: {_ai_err}")
    else:
        try:
            _render_wagon(st.session_state["bt_sinif"])
        except Exception as e:
            st.error(f"Vagon yüklenirken hata: {e}")
            if st.button("🚂 Trene Geri Dön", key="bt_back_err", type="primary"):
                st.session_state["bt_sinif"] = None
                st.rerun()
