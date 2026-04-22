# -*- coding: utf-8 -*-
"""
KDG Interaktif - Oyun & Gelismis Aktivite Modulu
SmartCampusAI - Kisisel Dil Gelisimi Hub
Diamond Premium Theme - 6 Mini Oyun + Gelismis Gramer/Diyalog/Dinleme/Quiz
"""
import json
from views.kdg_interaktif import _DIAMOND_CSS, _base_js, _lang_bar_html


# ---------------------------------------------------------------------------
# 1) GAMES HTML  (6 mini-game)
# ---------------------------------------------------------------------------

def build_games_html(data: dict) -> str:
    """Return a single HTML component with 6 vocabulary mini-games."""
    topics = data.get("vocab", [])
    grammar = data.get("grammar", [])
    all_words = []
    for t in topics:
        for w in t.get("words", []):
            all_words.append(w)
    words_json = json.dumps(all_words, ensure_ascii=False)
    grammar_json = json.dumps(grammar, ensure_ascii=False)

    return _DIAMOND_CSS + _lang_bar_html() + _base_js() + f"""
<style>
.game-selector {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; padding: 12px; }}
.game-card {{ background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 14px; padding: 18px 14px; text-align: center; cursor: pointer; transition: all 0.35s ease; }}
.game-card:hover {{ transform: translateY(-4px); border-color: #c7a55d; box-shadow: 0 6px 25px rgba(199,165,93,0.25); }}
.game-card.active {{ border-color: #c7a55d; background: linear-gradient(145deg, #1a1f5e, #222878); box-shadow: 0 0 20px rgba(199,165,93,0.15); }}
.game-icon {{ font-size: 36px; margin-bottom: 6px; }}
.game-title {{ font-size: 15px; font-weight: bold; color: #c7a55d; }}
.game-desc {{ font-size: 11px; color: #8888aa; margin-top: 4px; }}
.game-area {{ margin-top: 16px; min-height: 400px; }}
/* Memory */
.mem-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; max-width: 500px; margin: 0 auto; }}
.mem-card {{ height: 90px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.25); border-radius: 10px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 15px; color: #e0e0e0; transition: all 0.4s; perspective: 600px; user-select: none; word-break: break-word; padding: 6px; text-align: center; }}
.mem-card.flipped {{ background: linear-gradient(145deg,#1a1f5e,#222878); border-color: #c7a55d; }}
.mem-card.matched {{ background: rgba(74,222,128,0.15); border-color: #4ade80; color: #4ade80; pointer-events: none; }}
.mem-card .face {{ display: none; }}
.mem-card.flipped .face, .mem-card.matched .face {{ display: block; }}
.mem-card .back {{ font-size: 24px; }}
.mem-card.flipped .back, .mem-card.matched .back {{ display: none; }}
/* Scramble */
.scr-letter {{ display: inline-block; padding: 10px 16px; margin: 4px; background: linear-gradient(135deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.3); border-radius: 8px; cursor: pointer; font-size: 18px; color: #c7a55d; font-weight: bold; transition: all 0.2s; }}
.scr-letter:hover {{ border-color: #c7a55d; transform: scale(1.1); }}
.scr-letter.used {{ opacity: 0.3; pointer-events: none; }}
.scr-answer {{ min-height: 50px; background: rgba(10,14,39,0.6); border: 2px dashed rgba(199,165,93,0.3); border-radius: 10px; padding: 10px; margin: 12px 0; display: flex; gap: 4px; flex-wrap: wrap; align-items: center; justify-content: center; }}
.scr-placed {{ display: inline-block; padding: 8px 14px; margin: 2px; background: linear-gradient(135deg,#c7a55d,#a08040); color: #0a0e27; border-radius: 6px; font-weight: bold; font-size: 16px; cursor: pointer; }}
/* Speed Quiz */
.speed-timer {{ font-size: 28px; color: #c7a55d; font-weight: bold; text-align: center; margin: 10px 0; }}
.speed-word {{ font-size: 24px; text-align: center; color: #e0e0e0; margin: 16px 0; }}
.speed-opts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-width: 500px; margin: 0 auto; }}
.speed-opt {{ padding: 14px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.25); border-radius: 10px; text-align: center; cursor: pointer; font-size: 16px; color: #e0e0e0; transition: all 0.2s; }}
.speed-opt:hover {{ border-color: #c7a55d; }}
.speed-opt.correct {{ background: rgba(74,222,128,0.2); border-color: #4ade80; color: #4ade80; }}
.speed-opt.wrong {{ background: rgba(248,113,113,0.2); border-color: #f87171; color: #f87171; }}
/* Hangman */
.hm-word {{ font-size: 28px; letter-spacing: 10px; text-align: center; color: #c7a55d; margin: 16px 0; font-family: monospace; }}
.hm-kb {{ display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; max-width: 500px; margin: 12px auto; }}
.hm-key {{ width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; background: linear-gradient(145deg,#141852,#1a1f5e); border: 1px solid rgba(199,165,93,0.3); border-radius: 6px; cursor: pointer; color: #c7a55d; font-weight: bold; transition: all 0.2s; }}
.hm-key:hover {{ border-color: #c7a55d; }}
.hm-key.hit {{ background: rgba(74,222,128,0.2); border-color: #4ade80; color: #4ade80; pointer-events: none; }}
.hm-key.miss {{ background: rgba(248,113,113,0.15); border-color: #f87171; color: #f87171; pointer-events: none; }}
.hm-figure {{ font-family: monospace; white-space: pre; text-align: center; color: #f87171; font-size: 16px; line-height: 1.3; margin: 10px 0; }}
/* Balloon */
.bln-area {{ position: relative; height: 320px; overflow: hidden; background: rgba(10,14,39,0.5); border-radius: 14px; border: 1px solid rgba(199,165,93,0.2); }}
.bln-balloon {{ position: absolute; width: 90px; text-align: center; cursor: pointer; transition: bottom 0.05s linear; user-select: none; }}
.bln-ball {{ width: 70px; height: 85px; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; color: #fff; margin: 0 auto; text-shadow: 0 1px 3px rgba(0,0,0,0.5); padding: 6px; word-break: break-word; }}
.bln-string {{ width: 2px; height: 20px; background: #888; margin: 0 auto; }}
.bln-pop {{ animation: popAnim 0.3s forwards; }}
@keyframes popAnim {{ to {{ transform: scale(1.5); opacity: 0; }} }}
/* Sentence Builder */
.sb-chip {{ display: inline-block; padding: 8px 16px; margin: 4px; background: linear-gradient(135deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.3); border-radius: 8px; cursor: pointer; font-size: 15px; color: #e0e0e0; transition: all 0.2s; }}
.sb-chip:hover {{ border-color: #c7a55d; }}
.sb-chip.used {{ opacity: 0.3; pointer-events: none; }}
.sb-placed {{ display: inline-block; padding: 6px 14px; margin: 2px; background: linear-gradient(135deg,#c7a55d,#a08040); color: #0a0e27; border-radius: 6px; font-weight: bold; cursor: pointer; }}
/* Shared */
.game-stats {{ display: flex; justify-content: center; gap: 24px; margin: 12px 0; }}
.game-stat {{ text-align: center; }}
.game-stat-val {{ font-size: 22px; font-weight: bold; color: #c7a55d; }}
.game-stat-lbl {{ font-size: 11px; color: #8888aa; }}
.game-msg {{ text-align: center; padding: 16px; font-size: 20px; color: #c7a55d; font-weight: bold; }}
.game-restart {{ display: block; margin: 12px auto; background: linear-gradient(135deg,#c7a55d,#a08040); border: none; color: #0a0e27; padding: 10px 28px; border-radius: 10px; cursor: pointer; font-size: 15px; font-weight: bold; }}
.game-restart:hover {{ opacity: 0.85; }}
.progress-bar {{ height: 6px; background: rgba(199,165,93,0.15); border-radius: 3px; margin: 8px 0; overflow: hidden; }}
.progress-fill {{ height: 100%; background: linear-gradient(90deg,#c7a55d,#a08040); border-radius: 3px; transition: width 0.3s; }}
.score-stars {{ font-size: 32px; text-align: center; margin: 8px 0; }}
/* Kelime Avi (Word Hunt) */
.wh-grid {{ display: grid; grid-template-columns: repeat(5,1fr); gap: 6px; max-width: 450px; margin: 10px auto; }}
.wh-cell {{ height: 55px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 18px; font-weight: bold; color: #c7a55d; transition: all 0.2s; user-select: none; }}
.wh-cell:hover {{ border-color: #c7a55d; background: rgba(199,165,93,0.1); }}
.wh-cell.selected {{ background: rgba(199,165,93,0.25); border-color: #c7a55d; }}
.wh-cell.found {{ background: rgba(74,222,128,0.2); border-color: #4ade80; color: #4ade80; }}
/* Dogru Ceviri (Translation Match) */
.tm-pair {{ display: flex; gap: 12px; align-items: center; justify-content: center; margin: 10px 0; }}
.tm-word {{ padding: 14px 20px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.25); border-radius: 10px; font-size: 16px; color: #c7a55d; font-weight: bold; min-width: 140px; text-align: center; }}
.tm-opts {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }}
.tm-opt {{ padding: 10px 18px; background: rgba(20,24,82,0.5); border: 2px solid rgba(199,165,93,0.2); border-radius: 10px; cursor: pointer; font-size: 15px; color: #e0e0e0; transition: all 0.2s; }}
.tm-opt:hover {{ border-color: #c7a55d; }}
.tm-opt.correct {{ background: rgba(74,222,128,0.2); border-color: #4ade80; color: #4ade80; }}
.tm-opt.wrong {{ background: rgba(248,113,113,0.2); border-color: #f87171; color: #f87171; }}
/* Kategori Siralama (Category Sort) */
.cs-cats {{ display: flex; gap: 10px; justify-content: center; margin: 10px 0; flex-wrap: wrap; }}
.cs-cat {{ padding: 10px 20px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.25); border-radius: 12px; min-width: 120px; min-height: 100px; text-align: center; transition: all 0.3s; }}
.cs-cat-title {{ color: #c7a55d; font-weight: bold; font-size: 14px; margin-bottom: 6px; }}
.cs-cat.over {{ border-color: #c7a55d; box-shadow: 0 0 15px rgba(199,165,93,0.3); }}
.cs-word-chip {{ display: inline-block; padding: 8px 16px; margin: 4px; background: rgba(199,165,93,0.15); border: 1px solid rgba(199,165,93,0.3); border-radius: 20px; color: #e0e0e0; cursor: grab; font-size: 14px; transition: all 0.2s; user-select: none; }}
.cs-word-chip:hover {{ border-color: #c7a55d; }}
.cs-word-chip.placed {{ background: rgba(74,222,128,0.15); border-color: #4ade80; color: #4ade80; pointer-events: none; }}
.cs-word-chip.wrong-place {{ background: rgba(248,113,113,0.15); border-color: #f87171; color: #f87171; }}
/* Hizli Yazma (Speed Type) */
.st-input {{ background: rgba(10,14,39,0.8); border: 2px solid rgba(199,165,93,0.3); color: #e0e0e0; padding: 12px 16px; border-radius: 10px; font-size: 18px; width: 300px; text-align: center; outline: none; }}
.st-input:focus {{ border-color: #c7a55d; }}
.st-input.correct {{ border-color: #4ade80; background: rgba(74,222,128,0.1); }}
.st-input.wrong {{ border-color: #f87171; background: rgba(248,113,113,0.1); }}
</style>

<div class="game-selector" id="gameSel">
  <div class="game-card" onclick="loadGame(0)" id="gc0"><div class="game-icon">&#129504;</div><div class="game-title">Hafiza Oyunu</div><div class="game-desc">Kartlari esle, hafizani test et</div></div>
  <div class="game-card" onclick="loadGame(1)" id="gc1"><div class="game-icon">&#128292;</div><div class="game-title">Harf Karistirma</div><div class="game-desc">Karisik harfleri sirala</div></div>
  <div class="game-card" onclick="loadGame(2)" id="gc2"><div class="game-icon">&#9889;</div><div class="game-title">Hiz Testi</div><div class="game-desc">60 saniyede en cok dogru</div></div>
  <div class="game-card" onclick="loadGame(3)" id="gc3"><div class="game-icon">&#128128;</div><div class="game-title">Adam Asmaca</div><div class="game-desc">Kelimeyi bul, adami kurtar</div></div>
  <div class="game-card" onclick="loadGame(4)" id="gc4"><div class="game-icon">&#127880;</div><div class="game-title">Balon Patlatma</div><div class="game-desc">Dogru balonu patlat</div></div>
  <div class="game-card" onclick="loadGame(5)" id="gc5"><div class="game-icon">&#128295;</div><div class="game-title">Cumle Kurma</div><div class="game-desc">Kelimeleri dogru sirala</div></div>
  <div class="game-card" onclick="loadGame(6)" id="gc6"><div class="game-icon">&#128270;</div><div class="game-title">Kelime Avi</div><div class="game-desc">Harf tablosunda kelime bul</div></div>
  <div class="game-card" onclick="loadGame(7)" id="gc7"><div class="game-icon">&#9989;</div><div class="game-title">Dogru Ceviri</div><div class="game-desc">Hizla dogru ceviriyi sec</div></div>
  <div class="game-card" onclick="loadGame(8)" id="gc8"><div class="game-icon">&#128230;</div><div class="game-title">Kategori Siralama</div><div class="game-desc">Kelimeleri kategorilere yerlestir</div></div>
  <div class="game-card" onclick="loadGame(9)" id="gc9"><div class="game-icon">&#9000;</div><div class="game-title">Hizli Yazma</div><div class="game-desc">Ceviriyi hizla yaz</div></div>
</div>
<div class="game-area" id="gameArea"></div>

<script>
const allWords = {words_json};
const grammarData = {grammar_json};
const vocabTopics = {json.dumps([t for t in topics], ensure_ascii=False)};
let activeGame = -1;

function shuffle(a) {{ const b=[...a]; for(let i=b.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]; }} return b; }}
function pick(arr,n) {{ return shuffle(arr).slice(0,Math.min(n,arr.length)); }}
function stars(pct) {{ const s=pct>=90?5:pct>=75?4:pct>=60?3:pct>=40?2:1; return '&#11088;'.repeat(s)+'&#9734;'.repeat(5-s); }}

function loadGame(idx) {{
    activeGame = idx;
    document.querySelectorAll('.game-card').forEach((c,i)=>c.classList.toggle('active',i===idx));
    const area = document.getElementById('gameArea');
    area.innerHTML = '';
    [startMemory, startScramble, startSpeed, startHangman, startBalloon, startSentence, startWordHunt, startTransMatch, startCategorySort, startSpeedType][idx]();
}}

/* ── MEMORY MATCH ─────────────────────────────────── */
function startMemory() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 8);
    let cards = [];
    words.forEach(w => {{
        cards.push({{ type:'tr', text: w.tr, id: w.tr }});
        const t = w[currentLang] || w.en;
        cards.push({{ type:'lang', text: t, id: w.tr }});
    }});
    cards = shuffle(cards);
    let flipped = [], matched = 0, moves = 0, startT = Date.now();
    let lockBoard = false;

    area.innerHTML = `
        <div class="game-stats">
            <div class="game-stat"><div class="game-stat-val" id="memMoves">0</div><div class="game-stat-lbl">Hamle</div></div>
            <div class="game-stat"><div class="game-stat-val" id="memTime">0s</div><div class="game-stat-lbl">Sure</div></div>
            <div class="game-stat"><div class="game-stat-val" id="memPairs">0/8</div><div class="game-stat-lbl">Eslesme</div></div>
        </div>
        <div class="mem-grid" id="memGrid"></div>
        <div id="memMsg"></div>`;

    const grid = document.getElementById('memGrid');
    cards.forEach((c,i) => {{
        const div = document.createElement('div');
        div.className = 'mem-card';
        div.innerHTML = `<span class="back">&#10067;</span><span class="face">${{c.text}}</span>`;
        div.onclick = () => flipCard(i, div, c);
        grid.appendChild(div);
    }});

    const timer = setInterval(() => {{
        document.getElementById('memTime').textContent = Math.floor((Date.now()-startT)/1000)+'s';
    }}, 1000);

    function flipCard(i, div, c) {{
        if (lockBoard || div.classList.contains('flipped') || div.classList.contains('matched')) return;
        div.classList.add('flipped');
        flipped.push({{ idx:i, el:div, card:c }});
        if (flipped.length === 2) {{
            moves++;
            document.getElementById('memMoves').textContent = moves;
            lockBoard = true;
            const [a, b] = flipped;
            if (a.card.id === b.card.id && a.card.type !== b.card.type) {{
                a.el.classList.add('matched');
                b.el.classList.add('matched');
                matched++;
                document.getElementById('memPairs').textContent = matched+'/8';
                flipped = [];
                lockBoard = false;
                if (matched === 8) {{
                    clearInterval(timer);
                    const secs = Math.floor((Date.now()-startT)/1000);
                    const pct = Math.max(0, Math.round(100 - (moves-8)*4 - secs));
                    document.getElementById('memMsg').innerHTML = `<div class="game-msg">&#127942; Tebrikler! ${{moves}} hamlede, ${{secs}} saniyede tamamladin!</div><div class="score-stars">${{stars(pct)}}</div><button class="game-restart" onclick="startMemory()">Tekrar Oyna</button>`;
                }}
            }} else {{
                setTimeout(() => {{ a.el.classList.remove('flipped'); b.el.classList.remove('flipped'); flipped=[]; lockBoard=false; }}, 800);
            }}
        }}
    }}
}}

/* ── WORD SCRAMBLE ────────────────────────────────── */
function startScramble() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 10);
    let round = 0, score = 0, placed = [];

    function renderRound() {{
        if (round >= words.length) {{
            const pct = Math.round(score/words.length*100);
            area.innerHTML = `<div class="game-msg">&#127942; Skor: ${{score}}/${{words.length}} (%${{pct}})</div><div class="score-stars">${{stars(pct)}}</div><button class="game-restart" onclick="startScramble()">Tekrar Oyna</button>`;
            return;
        }}
        placed = [];
        const w = words[round];
        const target = (w[currentLang] || w.en).toLowerCase();
        const letters = shuffle(target.split(''));
        area.innerHTML = `
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val">${{round+1}}/${{words.length}}</div><div class="game-stat-lbl">Soru</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{score}}</div><div class="game-stat-lbl">Dogru</div></div>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:${{round/words.length*100}}%"></div></div>
            <div style="text-align:center;margin:16px 0;">
                <div style="color:#8888aa;font-size:13px;">Turkce anlami:</div>
                <div style="font-size:22px;color:#c7a55d;font-weight:bold;margin:6px 0;">${{w.tr}}</div>
                <div style="color:#8888aa;font-size:12px;">${{w.img||''}}</div>
            </div>
            <div class="scr-answer" id="scrAnswer"></div>
            <div style="text-align:center;" id="scrLetters">
                ${{letters.map((l,i) => `<span class="scr-letter" id="sl${{i}}" onclick="scrClick(${{i}},'${{l.replace("'","\\\\'")}}')">${{l}}</span>`).join('')}}
            </div>
            <div style="text-align:center;margin-top:10px;">
                <button class="game-restart" style="padding:6px 16px;font-size:13px;" onclick="scrClear()">Temizle</button>
            </div>
            <div id="scrFeedback" style="text-align:center;margin-top:8px;"></div>`;
        window._scrTarget = target;
    }}

    window.scrClick = (i, l) => {{
        document.getElementById('sl'+i).classList.add('used');
        placed.push({{ idx:i, letter:l }});
        const ans = document.getElementById('scrAnswer');
        ans.innerHTML += `<span class="scr-placed" onclick="scrRemove(${{placed.length-1}})">${{l}}</span>`;
        if (placed.length === window._scrTarget.length) {{
            const attempt = placed.map(p=>p.letter).join('');
            if (attempt === window._scrTarget) {{
                score++;
                document.getElementById('scrFeedback').innerHTML = '<span class="result-ok" style="font-size:18px;">&#10004; Dogru!</span>';
                speak(words[round][currentLang]||words[round].en, currentLang);
            }} else {{
                document.getElementById('scrFeedback').innerHTML = `<span class="result-fail" style="font-size:18px;">&#10008; Yanlis! Dogru: ${{window._scrTarget}}</span>`;
            }}
            setTimeout(() => {{ round++; renderRound(); }}, 1500);
        }}
    }};
    window.scrClear = () => {{
        placed.forEach(p => document.getElementById('sl'+p.idx).classList.remove('used'));
        placed = [];
        document.getElementById('scrAnswer').innerHTML = '';
        document.getElementById('scrFeedback').innerHTML = '';
    }};
    window.scrRemove = (pi) => {{
        const removed = placed.splice(pi);
        removed.forEach(p => document.getElementById('sl'+p.idx).classList.remove('used'));
        const ans = document.getElementById('scrAnswer');
        ans.innerHTML = placed.map((p,i) => `<span class="scr-placed" onclick="scrRemove(${{i}})">${{p.letter}}</span>`).join('');
    }};
    renderRound();
}}

/* ── SPEED QUIZ ───────────────────────────────────── */
function startSpeed() {{
    const area = document.getElementById('gameArea');
    let timeLeft = 60, correct = 0, wrong = 0, total = 0;
    let timerRef;

    function showQuestion() {{
        if (timeLeft <= 0) return endSpeed();
        const w = allWords[Math.floor(Math.random()*allWords.length)];
        const correctAns = w[currentLang] || w.en;
        let opts = [correctAns];
        while (opts.length < 4) {{
            const rw = allWords[Math.floor(Math.random()*allWords.length)];
            const rv = rw[currentLang] || rw.en;
            if (!opts.includes(rv)) opts.push(rv);
        }}
        opts = shuffle(opts);
        total++;
        area.innerHTML = `
            <div class="speed-timer" id="speedTimer">${{timeLeft}}s</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{correct}}</div><div class="game-stat-lbl">Dogru</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#f87171;">${{wrong}}</div><div class="game-stat-lbl">Yanlis</div></div>
            </div>
            <div class="speed-word">${{w.img||''}} ${{w.tr}}</div>
            <div class="speed-opts">
                ${{opts.map(o => `<div class="speed-opt" onclick="speedPick(this,'${{o.replace(/'/g,"\\\\'")}}','${{correctAns.replace(/'/g,"\\\\'")}}')">${{o}}</div>`).join('')}}
            </div>`;
    }}

    window.speedPick = (el, picked, ans) => {{
        document.querySelectorAll('.speed-opt').forEach(o => o.style.pointerEvents='none');
        if (picked === ans) {{
            el.classList.add('correct');
            correct++;
        }} else {{
            el.classList.add('wrong');
            wrong++;
            document.querySelectorAll('.speed-opt').forEach(o => {{ if(o.textContent===ans) o.classList.add('correct'); }});
        }}
        setTimeout(showQuestion, 600);
    }};

    function endSpeed() {{
        clearInterval(timerRef);
        const pct = total > 0 ? Math.round(correct/total*100) : 0;
        area.innerHTML = `<div class="game-msg">&#9889; Hiz Testi Bitti!</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val">${{total}}</div><div class="game-stat-lbl">Toplam</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{correct}}</div><div class="game-stat-lbl">Dogru</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#f87171;">${{wrong}}</div><div class="game-stat-lbl">Yanlis</div></div>
            </div>
            <div class="score-stars">${{stars(pct)}}</div>
            <button class="game-restart" onclick="startSpeed()">Tekrar Oyna</button>`;
    }}

    timerRef = setInterval(() => {{
        timeLeft--;
        const el = document.getElementById('speedTimer');
        if (el) el.textContent = timeLeft+'s';
        if (timeLeft <= 0) endSpeed();
    }}, 1000);
    showQuestion();
}}

/* ── HANGMAN ──────────────────────────────────────── */
function startHangman() {{
    const area = document.getElementById('gameArea');
    const w = allWords[Math.floor(Math.random()*allWords.length)];
    const word = (w[currentLang] || w.en).toLowerCase();
    let guessed = new Set(), wrong = 0, wins = 0, losses = 0;
    const maxWrong = 6;
    const figures = [
        "  +---+\\n  |   |\\n      |\\n      |\\n      |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n      |\\n      |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n  |   |\\n      |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n /|   |\\n      |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n /|\\\\  |\\n      |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n /|\\\\  |\\n /    |\\n=========",
        "  +---+\\n  |   |\\n  O   |\\n /|\\\\  |\\n / \\\\  |\\n========="
    ];
    const alpha = 'abcdefghijklmnopqrstuvwxyzäöüßàâéèêëïîôùûçñ';

    function render() {{
        const display = word.split('').map(c => c===' '?' ': (guessed.has(c)?c:'_')).join(' ');
        const won = word.split('').filter(c=>c!==' ').every(c=>guessed.has(c));
        const lost = wrong >= maxWrong;
        let kb = '';
        for (const c of alpha) {{
            if (word.includes(c) || 'abcdefghijklmnopqrstuvwxyz'.includes(c)) {{
                const cls = guessed.has(c) ? (word.includes(c)?'hit':'miss') : '';
                const disabled = guessed.has(c) || won || lost;
                kb += `<div class="hm-key ${{cls}}" ${{disabled?'style="pointer-events:none"':''}} onclick="hmGuess('${{c}}')">${{c}}</div>`;
            }}
        }}
        area.innerHTML = `
            <div style="text-align:center;margin:10px 0;">
                <div style="color:#8888aa;font-size:13px;">Ipucu (Turkce):</div>
                <div style="font-size:18px;color:#c7a55d;font-weight:bold;">${{w.img||''}} ${{w.tr}}</div>
            </div>
            <div class="hm-figure">${{figures[wrong]}}</div>
            <div class="hm-word">${{display}}</div>
            <div class="hm-kb">${{kb}}</div>
            <div id="hmMsg" style="text-align:center;margin-top:10px;"></div>`;

        if (won) {{
            document.getElementById('hmMsg').innerHTML = '<div class="game-msg" style="color:#4ade80;">&#127881; Kazandin!</div><button class="game-restart" onclick="startHangman()">Yeni Kelime</button>';
            speak(w[currentLang]||w.en, currentLang);
        }} else if (lost) {{
            document.getElementById('hmMsg').innerHTML = `<div class="game-msg" style="color:#f87171;">&#128128; Kaybettin! Kelime: ${{word}}</div><button class="game-restart" onclick="startHangman()">Yeni Kelime</button>`;
        }}
    }}

    window.hmGuess = (c) => {{
        if (guessed.has(c)) return;
        guessed.add(c);
        if (!word.includes(c)) wrong++;
        render();
    }};
    render();
}}

/* ── BALLOON POP ──────────────────────────────────── */
function startBalloon() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 10);
    let round = 0, score = 0;
    const colors = ['#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6'];

    function showRound() {{
        if (round >= words.length) {{
            const pct = Math.round(score/words.length*100);
            area.innerHTML = `<div class="game-msg">&#127880; Balon Oyunu Bitti!</div>
                <div class="game-stats"><div class="game-stat"><div class="game-stat-val">${{score}}/${{words.length}}</div><div class="game-stat-lbl">Dogru</div></div></div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="startBalloon()">Tekrar Oyna</button>`;
            return;
        }}
        const w = words[round];
        const correctAns = w[currentLang] || w.en;
        let opts = [correctAns];
        while (opts.length < 5 && opts.length < allWords.length) {{
            const rw = allWords[Math.floor(Math.random()*allWords.length)];
            const rv = rw[currentLang] || rw.en;
            if (!opts.includes(rv)) opts.push(rv);
        }}
        opts = shuffle(opts);

        area.innerHTML = `
            <div class="progress-bar"><div class="progress-fill" style="width:${{round/words.length*100}}%"></div></div>
            <div style="text-align:center;margin:10px 0;">
                <span style="color:#8888aa;">Turkce:</span>
                <span style="color:#c7a55d;font-weight:bold;font-size:20px;margin-left:8px;">${{w.img||''}} ${{w.tr}}</span>
                <span style="color:#8888aa;margin-left:10px;">(${{round+1}}/${{words.length}})</span>
            </div>
            <div class="bln-area" id="blnArea"></div>
            <div id="blnFb" style="text-align:center;margin-top:8px;"></div>`;

        const blnArea = document.getElementById('blnArea');
        opts.forEach((o,i) => {{
            const bln = document.createElement('div');
            bln.className = 'bln-balloon';
            bln.style.left = (10 + i * 18) + '%';
            bln.style.bottom = '-100px';
            bln.innerHTML = `<div class="bln-ball" style="background:${{colors[i%5]}}">${{o}}</div><div class="bln-string"></div>`;
            bln.onclick = () => blnPick(bln, o, correctAns);
            blnArea.appendChild(bln);
        }});

        // Animate upward
        let pos = -100;
        const anim = setInterval(() => {{
            pos += 1.5;
            document.querySelectorAll('.bln-balloon').forEach(b => {{
                if (!b.classList.contains('bln-pop')) b.style.bottom = pos + 'px';
            }});
            if (pos > 350) {{
                clearInterval(anim);
                document.getElementById('blnFb').innerHTML = '<span class="result-fail">Sure doldu!</span>';
                setTimeout(() => {{ round++; showRound(); }}, 1000);
            }}
        }}, 40);
        window._blnAnim = anim;
    }}

    window.blnPick = (el, picked, ans) => {{
        clearInterval(window._blnAnim);
        document.querySelectorAll('.bln-balloon').forEach(b => b.style.pointerEvents='none');
        if (picked === ans) {{
            el.querySelector('.bln-ball').style.background = '#4ade80';
            document.getElementById('blnFb').innerHTML = '<span class="result-ok" style="font-size:18px;">&#10004; Dogru!</span>';
            score++;
            speak(ans, currentLang);
        }} else {{
            el.classList.add('bln-pop');
            document.getElementById('blnFb').innerHTML = `<span class="result-fail" style="font-size:18px;">&#10008; Yanlis! Dogru: ${{ans}}</span>`;
        }}
        setTimeout(() => {{ round++; showRound(); }}, 1200);
    }};
    showRound();
}}

/* ── SENTENCE BUILDER ─────────────────────────────── */
function startSentence() {{
    const area = document.getElementById('gameArea');
    // Collect sentences from grammar examples
    let sentences = [];
    grammarData.forEach(g => {{
        (g.examples || []).forEach(ex => {{
            const src = ex[currentLang] || ex.en;
            const tr = ex.tr;
            if (src && tr && src.split(' ').length >= 3) sentences.push({{ src, tr }});
        }});
    }});
    if (sentences.length === 0) {{
        // Fallback: build simple sentences from vocab
        allWords.slice(0,5).forEach(w => {{
            sentences.push({{ src: w[currentLang]||w.en, tr: w.tr }});
        }});
    }}
    sentences = pick(sentences, 5);
    let round = 0, score = 0, placed = [];

    function renderRound() {{
        if (round >= sentences.length) {{
            const pct = Math.round(score/sentences.length*100);
            area.innerHTML = `<div class="game-msg">&#128295; Cumle Kurma Bitti!</div>
                <div class="game-stats"><div class="game-stat"><div class="game-stat-val">${{score}}/${{sentences.length}}</div><div class="game-stat-lbl">Dogru</div></div></div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="startSentence()">Tekrar Oyna</button>`;
            return;
        }}
        placed = [];
        const s = sentences[round];
        const wordsArr = s.src.split(/\\s+/);
        const scrambled = shuffle(wordsArr.map((w,i)=>({{w,i}})));
        area.innerHTML = `
            <div class="progress-bar"><div class="progress-fill" style="width:${{round/sentences.length*100}}%"></div></div>
            <div style="text-align:center;margin:16px 0;">
                <div style="color:#8888aa;font-size:13px;">Turkce cumle:</div>
                <div style="font-size:18px;color:#c7a55d;font-weight:bold;margin:6px 0;">${{s.tr}}</div>
            </div>
            <div class="scr-answer" id="sbAnswer" style="min-height:50px;"></div>
            <div style="text-align:center;margin:10px 0;" id="sbChips">
                ${{scrambled.map((o,i)=>`<span class="sb-chip" id="sbc${{i}}" onclick="sbClick(${{i}},${{o.i}},'${{o.w.replace(/'/g,"\\\\'").replace(/"/g,'&quot;')}}')">${{o.w}}</span>`).join('')}}
            </div>
            <div style="text-align:center;">
                <button class="game-restart" style="padding:6px 16px;font-size:13px;" onclick="sbClear()">Temizle</button>
            </div>
            <div id="sbFb" style="text-align:center;margin-top:8px;"></div>`;
        window._sbTarget = wordsArr;
    }}

    window.sbClick = (chipIdx, origIdx, word) => {{
        document.getElementById('sbc'+chipIdx).classList.add('used');
        placed.push({{ chipIdx, origIdx, word }});
        document.getElementById('sbAnswer').innerHTML = placed.map((p,i)=>`<span class="sb-placed" onclick="sbRemove(${{i}})">${{p.word}}</span>`).join(' ');
        if (placed.length === window._sbTarget.length) {{
            const attempt = placed.map(p=>p.word).join(' ');
            const target = window._sbTarget.join(' ');
            if (attempt.toLowerCase() === target.toLowerCase()) {{
                score++;
                document.getElementById('sbFb').innerHTML = '<span class="result-ok" style="font-size:18px;">&#10004; Dogru!</span>';
                speak(target, currentLang);
            }} else {{
                document.getElementById('sbFb').innerHTML = `<span class="result-fail" style="font-size:18px;">&#10008; Yanlis! Dogru: ${{target}}</span>`;
            }}
            setTimeout(() => {{ round++; renderRound(); }}, 1500);
        }}
    }};
    window.sbClear = () => {{
        placed.forEach(p=>document.getElementById('sbc'+p.chipIdx).classList.remove('used'));
        placed = [];
        document.getElementById('sbAnswer').innerHTML = '';
        document.getElementById('sbFb').innerHTML = '';
    }};
    window.sbRemove = (pi) => {{
        const removed = placed.splice(pi);
        removed.forEach(p=>document.getElementById('sbc'+p.chipIdx).classList.remove('used'));
        document.getElementById('sbAnswer').innerHTML = placed.map((p,i)=>`<span class="sb-placed" onclick="sbRemove(${{i}})">${{p.word}}</span>`).join(' ');
    }};
    renderRound();
}}

/* ── WORD HUNT (Kelime Avi) ─────────────────────────── */
function startWordHunt() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 5);
    const gridSize = 8;
    const grid = [];
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    // Fill grid with random letters
    for (let r=0; r<gridSize; r++) {{
        grid[r] = [];
        for (let c=0; c<gridSize; c++) grid[r][c] = alphabet[Math.floor(Math.random()*26)];
    }}
    // Place words horizontally or vertically
    const placements = [];
    words.forEach((w, wi) => {{
        const word = (w[currentLang]||w.en).toUpperCase().replace(/[^A-Z]/g,'');
        if (word.length > gridSize) return;
        let placed = false;
        for (let attempt=0; attempt<50 && !placed; attempt++) {{
            const horiz = Math.random()>0.5;
            const r = Math.floor(Math.random()*gridSize);
            const c = Math.floor(Math.random()*(gridSize - (horiz?word.length:0)));
            const startR = horiz ? r : Math.min(r, gridSize-word.length);
            let ok = true;
            for (let i=0; i<word.length && ok; i++) {{
                const gr = horiz ? startR : startR+i;
                const gc = horiz ? c+i : c;
                if (gr>=gridSize||gc>=gridSize) ok=false;
            }}
            if (ok) {{
                const cells = [];
                for (let i=0; i<word.length; i++) {{
                    const gr = horiz ? startR : startR+i;
                    const gc = horiz ? c+i : c;
                    grid[gr][gc] = word[i];
                    cells.push(gr*gridSize+gc);
                }}
                placements.push({{ word, tr: w.tr, cells: new Set(cells) }});
                placed = true;
            }}
        }}
    }});

    let found = 0;
    let selected = new Set();
    const totalWords = placements.length;

    const gridHtml = grid.map((row,r) =>
        row.map((ch,c) => `<div class="wh-cell" id="wh${{r*gridSize+c}}" onclick="whClick(${{r*gridSize+c}})">${{ch}}</div>`).join('')
    ).join('');

    const wordList = placements.map((p,i) => `<span id="whw${{i}}" style="padding:4px 10px;margin:3px;display:inline-block;border:1px solid rgba(199,165,93,0.3);border-radius:8px;color:#8888aa;font-size:13px;">${{p.tr}}</span>`).join('');

    area.innerHTML = `
        <div class="game-msg" style="font-size:16px;">&#128270; Harf tablosunda ${{totalWords}} kelime gizli. Harflere tiklayarak bul!</div>
        <div style="text-align:center;margin:8px 0;">${{wordList}}</div>
        <div style="display:grid;grid-template-columns:repeat(${{gridSize}},1fr);gap:4px;max-width:420px;margin:10px auto;">${{gridHtml}}</div>
        <div id="whStatus" style="text-align:center;margin-top:10px;color:#c7a55d;font-size:14px;">Bulunan: 0/${{totalWords}}</div>`;

    window.whClick = (idx) => {{
        const el = document.getElementById('wh'+idx);
        if (el.classList.contains('found')) return;
        el.classList.toggle('selected');
        if (el.classList.contains('selected')) selected.add(idx); else selected.delete(idx);
        // Check if any word is fully selected
        placements.forEach((p,i) => {{
            if (document.getElementById('whw'+i).style.color==='rgb(74, 222, 128)') return;
            let allSel = true;
            p.cells.forEach(c => {{ if (!selected.has(c)) allSel=false; }});
            if (allSel) {{
                found++;
                p.cells.forEach(c => {{
                    const cel = document.getElementById('wh'+c);
                    cel.classList.remove('selected');
                    cel.classList.add('found');
                    selected.delete(c);
                }});
                document.getElementById('whw'+i).style.color='#4ade80';
                document.getElementById('whw'+i).style.borderColor='#4ade80';
                speak(p.word, currentLang);
                document.getElementById('whStatus').innerHTML = `Bulunan: ${{found}}/${{totalWords}}`;
                if (found >= totalWords) {{
                    document.getElementById('whStatus').innerHTML = `<div class="game-msg">&#127881; Tebrikler! Tum kelimeleri buldun!</div><button class="game-restart" onclick="startWordHunt()">Tekrar Oyna</button>`;
                }}
            }}
        }});
    }};
}}

/* ── TRANSLATION MATCH (Dogru Ceviri) ────────────────── */
function startTransMatch() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 12);
    let round = 0, score = 0, total = words.length;
    let answered = false;

    function showRound() {{
        if (round >= total) {{
            const pct = Math.round(score/total*100);
            area.innerHTML = `<div class="game-msg">&#9989; Dogru Ceviri Bitti!</div>
                <div class="game-stats">
                    <div class="game-stat"><div class="game-stat-val">${{score}}/${{total}}</div><div class="game-stat-lbl">Dogru</div></div>
                    <div class="game-stat"><div class="game-stat-val">%${{pct}}</div><div class="game-stat-lbl">Basari</div></div>
                </div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="startTransMatch()">Tekrar Oyna</button>`;
            return;
        }}
        answered = false;
        const w = words[round];
        const correct = w[currentLang]||w.en;
        const wrongPool = allWords.filter(x => (x[currentLang]||x.en) !== correct);
        const wrongs = pick(wrongPool, 3).map(x => x[currentLang]||x.en);
        const opts = shuffle([correct, ...wrongs]);
        const correctIdx = opts.indexOf(correct);

        area.innerHTML = `
            <div class="progress-bar"><div class="progress-fill" style="width:${{round/total*100}}%"></div></div>
            <div style="text-align:center;margin:16px 0;">
                <div style="color:#8888aa;font-size:13px;">Soru ${{round+1}}/${{total}}</div>
                <div style="font-size:13px;color:#c7a55d;margin-top:4px;">Skor: ${{score}}</div>
            </div>
            <div class="tm-pair">
                <div class="tm-word">${{w.tr}} ${{w.img||''}}</div>
                <span style="font-size:24px;color:#c7a55d;">&#8594;</span>
                <span style="font-size:14px;color:#8888aa;">?</span>
            </div>
            <div class="tm-opts">
                ${{opts.map((o,i) => `<div class="tm-opt" id="tmo${{i}}" onclick="tmClick(${{i}},${{correctIdx}})">${{o}}</div>`).join('')}}
            </div>
            <div id="tmFb" style="text-align:center;margin-top:12px;"></div>`;
    }}

    window.tmClick = (idx, correctIdx) => {{
        if (answered) return;
        answered = true;
        document.querySelectorAll('.tm-opt').forEach(o => o.style.pointerEvents='none');
        if (idx === correctIdx) {{
            score++;
            document.getElementById('tmo'+idx).classList.add('correct');
            speak(document.getElementById('tmo'+idx).textContent, currentLang);
            document.getElementById('tmFb').innerHTML = '<span class="result-ok" style="font-size:16px;">&#10004; Dogru!</span>';
        }} else {{
            document.getElementById('tmo'+idx).classList.add('wrong');
            document.getElementById('tmo'+correctIdx).classList.add('correct');
            document.getElementById('tmFb').innerHTML = '<span class="result-fail" style="font-size:16px;">&#10008; Yanlis!</span>';
        }}
        setTimeout(() => {{ round++; showRound(); }}, 1200);
    }};
    showRound();
}}

/* ── CATEGORY SORT (Kategori Siralama) ───────────────── */
function startCategorySort() {{
    const area = document.getElementById('gameArea');
    const topics = (typeof vocabTopics !== 'undefined') ? vocabTopics : [];
    // Pick 3 random categories with their words
    let catData = [];
    if (topics.length >= 3) {{
        const picked = pick(topics, 3);
        picked.forEach(t => {{
            const ws = pick(t.words, 4);
            catData.push({{ name: t.topic, emoji: t.emoji||'', words: ws }});
        }});
    }} else {{
        // Fallback: split allWords into 3 groups
        const ws = pick(allWords, 12);
        for (let i=0; i<3; i++) {{
            catData.push({{ name: 'Grup '+(i+1), emoji: '', words: ws.slice(i*4, i*4+4) }});
        }}
    }}
    const allChips = [];
    catData.forEach((cat, ci) => {{
        cat.words.forEach(w => {{
            allChips.push({{ word: w[currentLang]||w.en, tr: w.tr, catIdx: ci, img: w.img||'' }});
        }});
    }});
    const shuffledChips = shuffle(allChips);
    let placed = 0;
    const totalChips = shuffledChips.length;

    const catsHtml = catData.map((c,i) => `<div class="cs-cat" id="cscat${{i}}" onclick="csDrop(${{i}})"><div class="cs-cat-title">${{c.emoji}} ${{c.name}}</div><div id="csdrop${{i}}"></div></div>`).join('');
    const chipsHtml = shuffledChips.map((ch,i) => `<span class="cs-word-chip" id="csc${{i}}" onclick="csSelect(${{i}})">${{ch.img}} ${{ch.word}}</span>`).join('');

    area.innerHTML = `
        <div class="game-msg" style="font-size:16px;">&#128230; Her kelimeyi dogru kategoriye yerlestir!</div>
        <div class="cs-cats">${{catsHtml}}</div>
        <div style="text-align:center;margin:12px 0;padding:10px;" id="csChips">${{chipsHtml}}</div>
        <div id="csFb" style="text-align:center;margin-top:8px;font-size:14px;color:#c7a55d;">Kalan: ${{totalChips}}</div>`;

    let selectedChip = -1;

    window.csSelect = (idx) => {{
        document.querySelectorAll('.cs-word-chip').forEach(c => c.style.borderColor='rgba(199,165,93,0.3)');
        const el = document.getElementById('csc'+idx);
        if (el.classList.contains('placed')) return;
        el.style.borderColor='#c7a55d';
        selectedChip = idx;
    }};

    window.csDrop = (catIdx) => {{
        if (selectedChip < 0) return;
        const chip = shuffledChips[selectedChip];
        const el = document.getElementById('csc'+selectedChip);
        if (chip.catIdx === catIdx) {{
            el.classList.add('placed');
            const dropZone = document.getElementById('csdrop'+catIdx);
            dropZone.innerHTML += `<span style="display:inline-block;padding:3px 8px;margin:2px;background:rgba(74,222,128,0.15);border:1px solid #4ade80;border-radius:6px;font-size:12px;color:#4ade80;">${{chip.word}}</span>`;
            placed++;
            speak(chip.word, currentLang);
            document.getElementById('csFb').innerHTML = placed>=totalChips ? '' : `Kalan: ${{totalChips-placed}}`;
            if (placed >= totalChips) {{
                document.getElementById('csFb').innerHTML = `<div class="game-msg">&#127881; Harika! Tum kelimeleri dogru yerlestirdin!</div><div class="score-stars">${{stars(100)}}</div><button class="game-restart" onclick="startCategorySort()">Tekrar Oyna</button>`;
            }}
        }} else {{
            el.classList.add('wrong-place');
            setTimeout(() => el.classList.remove('wrong-place'), 600);
        }}
        selectedChip = -1;
    }};
}}

/* ── SPEED TYPE (Hizli Yazma) ────────────────────────── */
function startSpeedType() {{
    const area = document.getElementById('gameArea');
    const words = pick(allWords, 15);
    let round = 0, score = 0, total = words.length;
    let startTime = Date.now();

    function showRound() {{
        if (round >= total) {{
            const elapsed = Math.round((Date.now()-startTime)/1000);
            const pct = Math.round(score/total*100);
            area.innerHTML = `<div class="game-msg">&#9000; Hizli Yazma Bitti!</div>
                <div class="game-stats">
                    <div class="game-stat"><div class="game-stat-val">${{score}}/${{total}}</div><div class="game-stat-lbl">Dogru</div></div>
                    <div class="game-stat"><div class="game-stat-val">${{elapsed}}s</div><div class="game-stat-lbl">Sure</div></div>
                    <div class="game-stat"><div class="game-stat-val">%${{pct}}</div><div class="game-stat-lbl">Basari</div></div>
                </div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="startSpeedType()">Tekrar Oyna</button>`;
            return;
        }}
        const w = words[round];
        area.innerHTML = `
            <div class="progress-bar"><div class="progress-fill" style="width:${{round/total*100}}%"></div></div>
            <div style="text-align:center;margin:20px 0;">
                <div style="color:#8888aa;font-size:13px;">Soru ${{round+1}}/${{total}} | Skor: ${{score}}</div>
                <div style="font-size:28px;margin:16px 0;">${{w.img||''}} <span style="color:#c7a55d;font-weight:bold;">${{w.tr}}</span></div>
                <div style="color:#8888aa;font-size:13px;margin-bottom:12px;">Ceviriyi yaz ve Enter'a bas</div>
                <input class="st-input" id="stInp" type="text" autocomplete="off" autofocus onkeydown="if(event.key==='Enter')stCheck()">
                <br><button class="check-btn" style="margin-top:10px;" onclick="stCheck()">Kontrol</button>
                <div id="stFb" style="margin-top:10px;"></div>
            </div>`;
        setTimeout(()=>{{const inp=document.getElementById('stInp');if(inp)inp.focus();}},100);
    }}

    window.stCheck = () => {{
        const inp = document.getElementById('stInp');
        const fb = document.getElementById('stFb');
        const w = words[round];
        const correct = (w[currentLang]||w.en);
        const userAns = (inp.value||'').trim();
        const norm = s => s.toLowerCase().replace(/[.!?,;:¿¡'"]/g,'').trim();
        if (norm(userAns) === norm(correct)) {{
            score++;
            inp.classList.add('correct');
            fb.innerHTML = '<span class="result-ok" style="font-size:16px;">&#10004; Dogru!</span>';
            speak(correct, currentLang);
        }} else {{
            inp.classList.add('wrong');
            fb.innerHTML = `<span class="result-fail">&#10008; Yanlis! Dogru: <b style="color:#c7a55d;">${{correct}}</b></span>`;
        }}
        setTimeout(() => {{ round++; showRound(); }}, 1300);
    }};
    showRound();
}}

</script>
"""


# ---------------------------------------------------------------------------
# 2) ENHANCED GRAMMAR
# ---------------------------------------------------------------------------

def build_enhanced_grammar_html(data: dict) -> str:
    """Enhanced grammar tab with sentence ordering, error correction, grammar quiz."""
    items = data.get("grammar", [])
    if not items:
        return "<p>Icerik hazirlaniyor...</p>"

    grammar_json = json.dumps(items, ensure_ascii=False)

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    # Render existing grammar boxes
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
            <div style="margin-top:12px;"><b style="color:#c7a55d;">Alistirma:</b></div>
            {exercises_html}
        </div>""")

    # Enhanced sections container
    html_parts.append("""
<style>
.enh-section { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.enh-title { font-size: 17px; color: #c7a55d; font-weight: bold; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(199,165,93,0.2); }
.so-chip { display: inline-block; padding: 8px 14px; margin: 3px; background: rgba(20,24,82,0.6); border: 1px solid rgba(199,165,93,0.3); border-radius: 8px; cursor: pointer; color: #e0e0e0; font-size: 14px; transition: all 0.2s; }
.so-chip:hover { border-color: #c7a55d; }
.so-chip.used { opacity: 0.3; pointer-events: none; }
.so-answer-area { min-height: 44px; background: rgba(10,14,39,0.5); border: 2px dashed rgba(199,165,93,0.2); border-radius: 8px; padding: 8px; margin: 8px 0; display: flex; flex-wrap: wrap; gap: 4px; }
.so-placed { display: inline-block; padding: 6px 12px; margin: 2px; background: linear-gradient(135deg,#c7a55d,#a08040); color: #0a0e27; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 13px; }
.ec-word { display: inline-block; padding: 4px 8px; margin: 2px; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
.ec-word:hover { background: rgba(199,165,93,0.15); }
.ec-word.selected { background: rgba(248,113,113,0.2); border-bottom: 2px solid #f87171; }
.ec-word.corrected { background: rgba(74,222,128,0.2); color: #4ade80; font-weight: bold; }
.gq-option { display: block; padding: 8px 14px; margin: 4px 0; border: 1px solid rgba(199,165,93,0.2); border-radius: 8px; cursor: pointer; color: #c0c0c0; font-size: 14px; transition: all 0.2s; }
.gq-option:hover { border-color: #c7a55d; background: rgba(199,165,93,0.08); }
.gq-option.correct { border-color: #4ade80; background: rgba(74,222,128,0.1); color: #4ade80; }
.gq-option.wrong { border-color: #f87171; background: rgba(248,113,113,0.1); color: #f87171; }
.progress-bar { height: 6px; background: rgba(199,165,93,0.15); border-radius: 3px; margin: 8px 0; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#c7a55d,#a08040); border-radius: 3px; transition: width 0.3s; }
.score-stars { font-size: 28px; text-align: center; margin: 8px 0; }
.game-msg { text-align: center; padding: 12px; font-size: 18px; color: #c7a55d; font-weight: bold; }
.game-restart { display: block; margin: 10px auto; background: linear-gradient(135deg,#c7a55d,#a08040); border: none; color: #0a0e27; padding: 8px 22px; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>

<div class="enh-section">
    <div class="enh-title">&#128260; Cumle Siralama</div>
    <div id="soArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#128270; Hata Duzeltme</div>
    <div id="ecArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#127891; Gramer Quiz</div>
    <div class="progress-bar"><div class="progress-fill" id="gqProgress" style="width:0%"></div></div>
    <div id="gqArea"></div>
</div>
""")

    html_parts.append(_base_js())
    html_parts.append(f"""<script>
const gData = {grammar_json};

function checkGrammar(id, answer) {{
    const inp = document.getElementById('inp_'+id);
    const res = document.getElementById('res_'+id);
    if (inp.value.trim().toLowerCase() === answer.toLowerCase()) {{
        res.innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
    }} else {{
        res.innerHTML = '<span class="result-fail">&#10008; Yanlis. Dogru: ' + answer + '</span>';
    }}
}}

function shuffle(a) {{ const b=[...a]; for(let i=b.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]; }} return b; }}
function stars(pct) {{ const s=pct>=90?5:pct>=75?4:pct>=60?3:pct>=40?2:1; return '&#11088;'.repeat(s)+'&#9734;'.repeat(5-s); }}

/* ── Sentence Ordering ─────────────── */
(function() {{
    const area = document.getElementById('soArea');
    let sentences = [];
    gData.forEach(g => (g.examples||[]).forEach(ex => {{
        const s = ex[currentLang] || ex.en;
        if (s && s.split(' ').length >= 3) sentences.push({{ src: s, tr: ex.tr || '' }});
    }}));
    sentences = shuffle(sentences).slice(0, 3);
    if (sentences.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Yeterli veri yok.</p>'; return; }}

    let html = '';
    sentences.forEach((s, si) => {{
        const wordsArr = s.src.split(/\\s+/);
        const scrambled = shuffle(wordsArr.map((w,i) => ({{ w, i }})));
        html += `<div style="margin-bottom:14px;padding:10px;background:rgba(10,14,39,0.4);border-radius:8px;">
            <div style="color:#8888aa;font-size:13px;margin-bottom:4px;">Turkce: <span style="color:#c7a55d;">${{s.tr}}</span></div>
            <div class="so-answer-area" id="soAns${{si}}"></div>
            <div id="soChips${{si}}">
                ${{scrambled.map((o,ci) => `<span class="so-chip" id="soc${{si}}_${{ci}}" onclick="soClick(${{si}},${{ci}},'${{o.w.replace(/'/g,"\\\\'").replace(/"/g,'&quot;')}}')">${{o.w}}</span>`).join('')}}
            </div>
            <div style="margin-top:6px;">
                <button class="check-btn" style="font-size:12px;" onclick="soCheck(${{si}})">Kontrol</button>
                <button class="check-btn" style="font-size:12px;background:rgba(199,165,93,0.3);color:#c7a55d;" onclick="soClear(${{si}})">Temizle</button>
                <span id="soFb${{si}}" style="margin-left:8px;"></span>
            </div>
        </div>`;
        window['_soTarget'+si] = wordsArr;
    }});
    area.innerHTML = html;

    window._soPlaced = {{}};
    sentences.forEach((s,si) => window._soPlaced[si] = []);

    window.soClick = (si, ci, word) => {{
        document.getElementById('soc'+si+'_'+ci).classList.add('used');
        window._soPlaced[si].push({{ ci, word }});
        document.getElementById('soAns'+si).innerHTML = window._soPlaced[si].map((p,i) =>
            `<span class="so-placed" onclick="soRemoveFrom(${{si}},${{i}})">${{p.word}}</span>`
        ).join('');
    }};
    window.soClear = (si) => {{
        window._soPlaced[si].forEach(p => document.getElementById('soc'+si+'_'+p.ci).classList.remove('used'));
        window._soPlaced[si] = [];
        document.getElementById('soAns'+si).innerHTML = '';
        document.getElementById('soFb'+si).innerHTML = '';
    }};
    window.soRemoveFrom = (si, pi) => {{
        const removed = window._soPlaced[si].splice(pi);
        removed.forEach(p => document.getElementById('soc'+si+'_'+p.ci).classList.remove('used'));
        document.getElementById('soAns'+si).innerHTML = window._soPlaced[si].map((p,i) =>
            `<span class="so-placed" onclick="soRemoveFrom(${{si}},${{i}})">${{p.word}}</span>`
        ).join('');
    }};
    window.soCheck = (si) => {{
        const target = window['_soTarget'+si];
        const attempt = window._soPlaced[si].map(p=>p.word).join(' ');
        const fb = document.getElementById('soFb'+si);
        if (attempt.toLowerCase() === target.join(' ').toLowerCase()) {{
            fb.innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
        }} else {{
            fb.innerHTML = `<span class="result-fail">&#10008; Yanlis! Dogru: ${{target.join(' ')}}</span>`;
        }}
    }};
}})();

/* ── Error Correction ──────────────── */
(function() {{
    const area = document.getElementById('ecArea');
    let sentences = [];
    gData.forEach(g => (g.examples||[]).forEach(ex => {{
        const s = ex[currentLang] || ex.en;
        if (s && s.split(' ').length >= 3) sentences.push({{ src: s, tr: ex.tr || '' }});
    }}));
    sentences = shuffle(sentences).slice(0, 3);
    if (sentences.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Yeterli veri yok.</p>'; return; }}

    let html = '';
    sentences.forEach((s, si) => {{
        const wordsArr = s.src.split(/\\s+/);
        // Replace one random word with a wrong one
        const errIdx = Math.floor(Math.random() * wordsArr.length);
        const original = wordsArr[errIdx];
        // Create wrong word by shuffling letters
        let wrong = shuffle(original.split('')).join('');
        if (wrong === original) wrong = original + 'x';
        const display = [...wordsArr];
        display[errIdx] = wrong;

        html += `<div style="margin-bottom:14px;padding:10px;background:rgba(10,14,39,0.4);border-radius:8px;">
            <div style="color:#8888aa;font-size:13px;margin-bottom:6px;">Turkce: <span style="color:#c7a55d;">${{s.tr}}</span></div>
            <div style="font-size:15px;line-height:2;" id="ecSent${{si}}">
                ${{display.map((w,wi) => `<span class="ec-word" id="ecw${{si}}_${{wi}}" onclick="ecSelect(${{si}},${{wi}})">${{w}}</span>`).join(' ')}}
            </div>
            <div id="ecFix${{si}}" style="margin-top:6px;display:none;">
                <input type="text" class="exercise-input" id="ecInp${{si}}" placeholder="Dogru kelime...">
                <button class="check-btn" onclick="ecCheck(${{si}})">Duzelt</button>
            </div>
            <span id="ecFb${{si}}" style="margin-left:8px;"></span>
        </div>`;
        window['_ecErr'+si] = {{ idx: errIdx, original: original }};
    }});
    area.innerHTML = html;

    window._ecSelected = {{}};
    window.ecSelect = (si, wi) => {{
        document.querySelectorAll('#ecSent'+si+' .ec-word').forEach(w => w.classList.remove('selected'));
        document.getElementById('ecw'+si+'_'+wi).classList.add('selected');
        window._ecSelected[si] = wi;
        document.getElementById('ecFix'+si).style.display = 'block';
    }};
    window.ecCheck = (si) => {{
        const err = window['_ecErr'+si];
        const sel = window._ecSelected[si];
        const inp = document.getElementById('ecInp'+si).value.trim();
        const fb = document.getElementById('ecFb'+si);
        if (sel === err.idx && inp.toLowerCase() === err.original.toLowerCase()) {{
            fb.innerHTML = '<span class="result-ok">&#10004; Dogru! Hatali kelimeyi buldun ve duzelttin.</span>';
            document.getElementById('ecw'+si+'_'+sel).classList.remove('selected');
            document.getElementById('ecw'+si+'_'+sel).classList.add('corrected');
            document.getElementById('ecw'+si+'_'+sel).textContent = err.original;
        }} else if (sel !== err.idx) {{
            fb.innerHTML = '<span class="result-fail">&#10008; Yanlis kelime sectiniz. Tekrar deneyin.</span>';
        }} else {{
            fb.innerHTML = `<span class="result-fail">&#10008; Dogru kelime: ${{err.original}}</span>`;
        }}
    }};
}})();

/* ── Grammar Quiz ──────────────────── */
(function() {{
    const area = document.getElementById('gqArea');
    // Build quiz from exercises
    let questions = [];
    gData.forEach(g => {{
        (g.exercises||[]).forEach(ex => {{
            questions.push({{
                prompt: ex.prompt,
                answer: ex.answer,
                hint: ex.hint || '',
                title: g.title
            }});
        }});
    }});
    questions = shuffle(questions).slice(0, 5);
    if (questions.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Yeterli soru yok.</p>'; return; }}

    let qi = 0, score = 0;
    function renderQ() {{
        if (qi >= questions.length) {{
            const pct = Math.round(score/questions.length*100);
            area.innerHTML = `<div class="game-msg">&#127891; Gramer Quiz Sonucu: ${{score}}/${{questions.length}} (%${{pct}})</div><div class="score-stars">${{stars(pct)}}</div>`;
            document.getElementById('gqProgress').style.width = '100%';
            return;
        }}
        document.getElementById('gqProgress').style.width = (qi/questions.length*100)+'%';
        const q = questions[qi];
        area.innerHTML = `
            <div style="margin:10px 0;color:#8888aa;font-size:12px;">${{q.title}}</div>
            <div style="font-size:15px;color:#e0e0e0;margin-bottom:8px;">${{qi+1}}. ${{q.prompt}}</div>
            <div style="display:flex;gap:8px;align-items:center;">
                <input type="text" class="exercise-input" id="gqInp" placeholder="Cevabin..." style="width:180px;">
                <button class="check-btn" onclick="gqCheck()">Kontrol</button>
            </div>
            <div style="color:#8888aa;font-size:11px;margin-top:4px;">Ipucu: ${{q.hint}}</div>
            <div id="gqFb" style="margin-top:8px;"></div>`;
    }}
    window.gqCheck = () => {{
        const q = questions[qi];
        const inp = document.getElementById('gqInp').value.trim();
        const fb = document.getElementById('gqFb');
        if (inp.toLowerCase() === q.answer.toLowerCase()) {{
            score++;
            fb.innerHTML = '<span class="result-ok" style="font-size:16px;">&#10004; Dogru!</span>';
        }} else {{
            fb.innerHTML = `<span class="result-fail" style="font-size:16px;">&#10008; Yanlis! Dogru: ${{q.answer}}</span>`;
        }}
        qi++;
        setTimeout(renderQ, 1200);
    }};
    renderQ();
}})();
</script>""")

    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# 3) ENHANCED DIALOGUE
# ---------------------------------------------------------------------------

def build_enhanced_dialogue_html(data: dict) -> str:
    """Enhanced dialogue tab with role play, dialogue builder, listen & repeat."""
    dialogues = data.get("dialogues", [])
    if not dialogues:
        return "<p>Icerik hazirlaniyor...</p>"

    dialogues_json = json.dumps(dialogues, ensure_ascii=False)

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]
    html_parts.append("""
<style>
.chat-container { max-width: 550px; margin: 0 auto; }
.chat-bubble { max-width: 75%; padding: 10px 14px; border-radius: 14px; margin: 6px 0; font-size: 14px; position: relative; }
.chat-left { margin-right: auto; background: linear-gradient(145deg,#141852,#1a1f5e); border: 1px solid rgba(199,165,93,0.2); border-bottom-left-radius: 4px; }
.chat-right { margin-left: auto; background: linear-gradient(135deg,rgba(199,165,93,0.15),rgba(199,165,93,0.08)); border: 1px solid rgba(199,165,93,0.3); border-bottom-right-radius: 4px; text-align: right; }
.chat-speaker { font-size: 11px; color: #c7a55d; font-weight: bold; margin-bottom: 4px; }
.chat-text { color: #e0e0e0; }
.chat-tr { color: #8888aa; font-size: 12px; margin-top: 3px; }
.chat-tts { background: none; border: none; color: #c7a55d; cursor: pointer; font-size: 14px; padding: 2px 6px; }
.mode-tabs { display: flex; gap: 8px; justify-content: center; margin: 12px 0; flex-wrap: wrap; }
.mode-tab { padding: 8px 16px; border: 1px solid rgba(199,165,93,0.3); background: rgba(20,24,82,0.5); color: #c7a55d; border-radius: 20px; cursor: pointer; font-size: 13px; transition: all 0.3s; }
.mode-tab.active { background: rgba(199,165,93,0.2); border-color: #c7a55d; font-weight: bold; }
.rp-input { width: 100%; padding: 8px 12px; background: rgba(10,14,39,0.8); border: 1px solid rgba(199,165,93,0.3); color: #e0e0e0; border-radius: 8px; font-size: 14px; margin-top: 6px; }
.db-option { display: block; padding: 8px 14px; margin: 4px 0; border: 1px solid rgba(199,165,93,0.2); border-radius: 8px; cursor: pointer; color: #c0c0c0; font-size: 14px; transition: all 0.2s; }
.db-option:hover { border-color: #c7a55d; background: rgba(199,165,93,0.08); }
.db-option.correct { border-color: #4ade80; background: rgba(74,222,128,0.1); color: #4ade80; }
.db-option.wrong { border-color: #f87171; background: rgba(248,113,113,0.1); color: #f87171; }
.lr-line { display: flex; align-items: center; gap: 10px; padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }
.mic-btn { background: linear-gradient(135deg,#e74c3c,#c0392b); border: none; color: #fff; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; font-size: 16px; transition: all 0.2s; }
.mic-btn:hover { transform: scale(1.1); }
.enh-section { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.enh-title { font-size: 17px; color: #c7a55d; font-weight: bold; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(199,165,93,0.2); }
.result-ok { color: #4ade80; font-weight: bold; }
.result-fail { color: #f87171; font-weight: bold; }
</style>
""")

    # Render existing dialogues in chat style
    for di, d in enumerate(dialogues):
        lines_html = ""
        speakers = list(set(line.get("speaker","") for line in d.get("lines",[])))
        for li, line in enumerate(d.get("lines", [])):
            lang_data = json.dumps({k: line.get(k, "") for k in ["en","de","fr","it","es"]}, ensure_ascii=False).replace("'", "&#39;")
            side = "chat-left" if line.get("speaker","") == speakers[0] else "chat-right"
            lines_html += f"""<div class="chat-bubble {side}">
                <div class="chat-speaker">{line['speaker']}</div>
                <div class="chat-text" data-lang-content='{lang_data}'>{line.get('en','')}</div>
                <div class="chat-tr">{line.get('tr','')}</div>
                <button class="chat-tts" onclick="var d=JSON.parse(this.parentElement.querySelector('[data-lang-content]').dataset.langContent); speak(d[currentLang],currentLang);">&#128266;</button>
            </div>"""

        html_parts.append(f"""
        <div class="enh-section">
            <div class="enh-title">{d['title']}</div>
            <div class="chat-container">{lines_html}</div>
            <div style="text-align:center;margin-top:10px;">
                <button class="play-btn" onclick="playDlg({di})">&#9654; Tum Diyalogu Dinle</button>
            </div>
        </div>""")

    # Enhanced sections
    html_parts.append("""
<div class="enh-section">
    <div class="enh-title">&#127917; Rol Yapma Modu</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">Bir konusmacinin satirlari gizlenir. Dogru cevabi yazin.</p>
    <div id="rpArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#128172; Diyalog Kurucu</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">Bagrama gore dogru cevabi secin.</p>
    <div id="dbArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#127908; Dinle ve Tekrarla</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">Her satiri dinleyin, mikrofon ikonuna basip tekrarlayin.</p>
    <div id="lrArea"></div>
</div>
""")

    html_parts.append(_base_js())
    html_parts.append(f"""<script>
const dlgData = {dialogues_json};

function shuffle(a) {{ const b=[...a]; for(let i=b.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]; }} return b; }}

function playDlg(di) {{
    const lines = dlgData[di].lines;
    let i = 0;
    function next() {{
        if (i >= lines.length) return;
        const text = lines[i][currentLang] || lines[i].en || '';
        const u = new SpeechSynthesisUtterance(text);
        u.lang = langCodes[currentLang] || 'en-US';
        u.rate = 0.8;
        u.onend = () => {{ i++; setTimeout(next, 400); }};
        window.speechSynthesis.speak(u);
        i++;
    }}
    window.speechSynthesis.cancel();
    i = 0;
    next();
}}

/* ── Role Play ─────────────────────── */
(function() {{
    const area = document.getElementById('rpArea');
    if (dlgData.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Diyalog verisi yok.</p>'; return; }}
    const dlg = dlgData[0];
    const lines = dlg.lines || [];
    if (lines.length < 2) {{ area.innerHTML = '<p style="color:#8888aa;">Yeterli satir yok.</p>'; return; }}

    // Hide every other line (speaker B)
    const speakers = [...new Set(lines.map(l => l.speaker))];
    const hideSpk = speakers[1] || speakers[0];
    let html = '<div class="chat-container">';
    lines.forEach((line, li) => {{
        const text = line[currentLang] || line.en || '';
        const side = line.speaker === speakers[0] ? 'chat-left' : 'chat-right';
        if (line.speaker === hideSpk) {{
            html += `<div class="chat-bubble ${{side}}">
                <div class="chat-speaker">${{line.speaker}}</div>
                <input type="text" class="rp-input" id="rpInp${{li}}" placeholder="Cevabi yazin...">
                <button class="check-btn" style="margin-top:4px;font-size:12px;" onclick="rpCheck(${{li}})">Kontrol</button>
                <div id="rpFb${{li}}" style="margin-top:4px;"></div>
            </div>`;
        }} else {{
            html += `<div class="chat-bubble ${{side}}">
                <div class="chat-speaker">${{line.speaker}}</div>
                <div class="chat-text">${{text}}</div>
                <div class="chat-tr">${{line.tr || ''}}</div>
            </div>`;
        }}
    }});
    html += '</div>';
    area.innerHTML = html;

    window.rpCheck = (li) => {{
        const line = lines[li];
        const correct = (line[currentLang] || line.en || '').toLowerCase();
        const inp = document.getElementById('rpInp'+li).value.trim().toLowerCase();
        const fb = document.getElementById('rpFb'+li);
        if (inp === correct) {{
            fb.innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
        }} else {{
            fb.innerHTML = `<span class="result-fail">&#10008; Dogru cevap: ${{line[currentLang]||line.en}}</span>`;
        }}
    }};
}})();

/* ── Dialogue Builder ──────────────── */
(function() {{
    const area = document.getElementById('dbArea');
    if (dlgData.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Diyalog verisi yok.</p>'; return; }}

    let html = '';
    const dlg = dlgData[Math.floor(Math.random()*dlgData.length)];
    const lines = dlg.lines || [];
    // For some lines, show options
    lines.forEach((line, li) => {{
        const text = line[currentLang] || line.en || '';
        if (li > 0 && li % 2 === 1) {{
            // Build options: correct + 2 wrong from other lines
            let opts = [text];
            lines.forEach((ol, oi) => {{
                if (oi !== li && opts.length < 3) opts.push(ol[currentLang]||ol.en||'');
            }});
            opts = shuffle(opts);
            html += `<div style="margin:8px 0;padding:8px;background:rgba(10,14,39,0.4);border-radius:8px;">
                <div style="color:#8888aa;font-size:12px;margin-bottom:4px;"><b>${{line.speaker}}</b> ne der?</div>
                <div style="color:#c7a55d;font-size:12px;margin-bottom:6px;">Ipucu: ${{line.tr||''}}</div>
                ${{opts.map(o => `<div class="db-option" onclick="dbPick(this,'${{o.replace(/'/g,"\\\\'")}}','${{text.replace(/'/g,"\\\\'")}}')">${{o}}</div>`).join('')}}
                <div id="dbFb${{li}}" style="margin-top:4px;"></div>
            </div>`;
        }} else {{
            html += `<div style="margin:8px 0;padding:8px;">
                <span style="color:#c7a55d;font-weight:bold;font-size:12px;">${{line.speaker}}:</span>
                <span style="color:#e0e0e0;font-size:14px;margin-left:6px;">${{text}}</span>
                <span style="color:#8888aa;font-size:12px;margin-left:6px;">(${{line.tr||''}})</span>
            </div>`;
        }}
    }});
    area.innerHTML = html;

    window.dbPick = (el, picked, correct) => {{
        el.parentElement.querySelectorAll('.db-option').forEach(o => o.style.pointerEvents='none');
        if (picked === correct) {{
            el.classList.add('correct');
            speak(correct, currentLang);
        }} else {{
            el.classList.add('wrong');
            el.parentElement.querySelectorAll('.db-option').forEach(o => {{
                if (o.textContent === correct) o.classList.add('correct');
            }});
        }}
    }};
}})();

/* ── Listen & Repeat ───────────────── */
(function() {{
    const area = document.getElementById('lrArea');
    if (dlgData.length === 0) {{ area.innerHTML = '<p style="color:#8888aa;">Diyalog verisi yok.</p>'; return; }}

    const dlg = dlgData[0];
    let html = '';
    (dlg.lines||[]).forEach((line, li) => {{
        const text = line[currentLang] || line.en || '';
        html += `<div class="lr-line">
            <button class="tts-btn" onclick="speak('${{text.replace(/'/g,"\\\\'")}}',currentLang)">&#128266; Dinle</button>
            <span style="color:#c7a55d;font-weight:bold;font-size:12px;">${{line.speaker}}</span>
            <span style="color:#e0e0e0;font-size:14px;">${{text}}</span>
            <button class="mic-btn" title="Tekrarla" onclick="lrRecord(this)">&#127908;</button>
        </div>`;
    }});
    area.innerHTML = html;

    window.lrRecord = (btn) => {{
        // Visual feedback - microphone is "active"
        btn.style.background = 'linear-gradient(135deg,#4ade80,#22c55e)';
        btn.textContent = '...';
        setTimeout(() => {{
            btn.style.background = 'linear-gradient(135deg,#e74c3c,#c0392b)';
            btn.innerHTML = '&#127908;';
        }}, 3000);
        // Note: Full speech recognition requires HTTPS + user permission
        if (window.SpeechRecognition || window.webkitSpeechRecognition) {{
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            const rec = new SR();
            rec.lang = langCodes[currentLang] || 'en-US';
            rec.onresult = (e) => {{
                const result = e.results[0][0].transcript;
                btn.parentElement.insertAdjacentHTML('beforeend',
                    `<span style="color:#4ade80;font-size:12px;margin-left:8px;">Soylediniz: ${{result}}</span>`);
                btn.style.background = 'linear-gradient(135deg,#e74c3c,#c0392b)';
                btn.innerHTML = '&#127908;';
            }};
            rec.onerror = () => {{
                btn.style.background = 'linear-gradient(135deg,#e74c3c,#c0392b)';
                btn.innerHTML = '&#127908;';
            }};
            rec.start();
        }}
    }};
}})();
</script>""")

    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# 4) ENHANCED LISTENING
# ---------------------------------------------------------------------------

def build_enhanced_listening_html(data: dict) -> str:
    """Enhanced listening tab with dictation, word recognition, speed listening."""
    readings = data.get("reading", [])
    vocab = data.get("vocab", [])
    all_words = []
    for t in vocab:
        for w in t.get("words", []):
            all_words.append(w)
    words_json = json.dumps(all_words, ensure_ascii=False)
    readings_json = json.dumps(readings, ensure_ascii=False)

    html_parts = [_DIAMOND_CSS, _lang_bar_html()]

    # Existing listening content
    for ri, r in enumerate(readings):
        text_data = json.dumps(r.get("text", {}), ensure_ascii=False).replace("'", "&#39;")
        questions_html = ""
        for qi, q in enumerate(r.get("questions", [])):
            opts_html = ""
            for oi, opt in enumerate(q["options"]):
                lid = f"l{ri}q{qi}"
                opts_html += f'<label class="quiz-opt" onclick="selectOpt(\'{lid}\',{oi},{q["answer"]},this)">{opt}</label>'
            questions_html += f"""<div class="quiz-q">
                <div class="quiz-q-text">{qi+1}. {q['q_tr']}</div>
                {opts_html}
                <div id="res_{lid}" style="margin-top:6px;"></div>
            </div>"""

        html_parts.append(f"""
        <div class="listening-area" style="margin-bottom:16px;">
            <div class="section-title">&#127911; Dinleme: {r['title']}</div>
            <p style="color:#8888aa;margin:8px 0;">Metni dinleyin ve sorulari cevaplayin.</p>
            <button class="play-btn" onclick="var d=JSON.parse('{text_data.replace(chr(39),'&#39;')}'); speak(d[currentLang],currentLang);">&#9654; Dinle</button>
            <button class="play-btn" style="background:rgba(199,165,93,0.3);color:#c7a55d;" onclick="var d=JSON.parse('{text_data.replace(chr(39),'&#39;')}'); speakSlow(d[currentLang],currentLang);">&#128034; Yavas Dinle</button>
        </div>
        {questions_html}
        """)

    # Enhanced sections
    html_parts.append("""
<style>
.enh-section { background: linear-gradient(145deg, #141852, #1a1f5e); border: 1px solid rgba(199,165,93,0.25); border-radius: 12px; padding: 16px; margin-bottom: 14px; }
.enh-title { font-size: 17px; color: #c7a55d; font-weight: bold; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(199,165,93,0.2); }
.dict-input { width: 100%; padding: 10px 14px; background: rgba(10,14,39,0.8); border: 1px solid rgba(199,165,93,0.3); color: #e0e0e0; border-radius: 8px; font-size: 15px; margin: 8px 0; }
.wr-card { display: inline-block; padding: 12px 20px; margin: 6px; background: linear-gradient(145deg,#141852,#1a1f5e); border: 2px solid rgba(199,165,93,0.2); border-radius: 10px; cursor: pointer; font-size: 15px; color: #e0e0e0; transition: all 0.2s; text-align: center; min-width: 100px; }
.wr-card:hover { border-color: #c7a55d; }
.wr-card.correct { border-color: #4ade80; background: rgba(74,222,128,0.1); color: #4ade80; }
.wr-card.wrong { border-color: #f87171; background: rgba(248,113,113,0.1); color: #f87171; }
.progress-bar { height: 6px; background: rgba(199,165,93,0.15); border-radius: 3px; margin: 8px 0; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#c7a55d,#a08040); border-radius: 3px; transition: width 0.3s; }
.score-stars { font-size: 28px; text-align: center; margin: 8px 0; }
.game-msg { text-align: center; padding: 12px; font-size: 18px; color: #c7a55d; font-weight: bold; }
.game-restart { display: block; margin: 10px auto; background: linear-gradient(135deg,#c7a55d,#a08040); border: none; color: #0a0e27; padding: 8px 22px; border-radius: 8px; cursor: pointer; font-weight: bold; }
.game-stats { display: flex; justify-content: center; gap: 24px; margin: 10px 0; }
.game-stat { text-align: center; }
.game-stat-val { font-size: 20px; font-weight: bold; color: #c7a55d; }
.game-stat-lbl { font-size: 11px; color: #8888aa; }
.speed-timer { font-size: 24px; color: #c7a55d; font-weight: bold; text-align: center; margin: 8px 0; }
</style>

<div class="enh-section">
    <div class="enh-title">&#9999;&#65039; Dikte</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">Kelimeyi dinleyin ve duydugunuzu yazin.</p>
    <div id="dictArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#128065; Kelime Tanima</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">Kelimeyi dinleyin, 4 secenekten dogru olani secin.</p>
    <div id="wrArea"></div>
</div>
<div class="enh-section">
    <div class="enh-title">&#9889; Hizli Dinleme</div>
    <p style="color:#8888aa;font-size:13px;margin-bottom:8px;">10 kelimeyi dinleyin, Turkce anlamini secin. Sureli!</p>
    <div id="slArea"></div>
</div>
""")

    html_parts.append(_base_js())
    html_parts.append(f"""<script>
const lstWords = {words_json};

function shuffle(a) {{ const b=[...a]; for(let i=b.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]; }} return b; }}
function pick(arr,n) {{ return shuffle(arr).slice(0,Math.min(n,arr.length)); }}
function stars(pct) {{ const s=pct>=90?5:pct>=75?4:pct>=60?3:pct>=40?2:1; return '&#11088;'.repeat(s)+'&#9734;'.repeat(5-s); }}

function speakSlow(text, lang) {{
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = langCodes[lang || currentLang] || 'en-US';
    u.rate = 0.55;
    window.speechSynthesis.speak(u);
}}

function selectOpt(qid, idx, correct, el) {{
    const parent = el.parentElement;
    parent.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('selected','correct','wrong'));
    if (idx === correct) {{
        el.classList.add('correct');
        document.getElementById('res_'+qid).innerHTML = '<span class="result-ok">Dogru!</span>';
    }} else {{
        el.classList.add('wrong');
        document.getElementById('res_'+qid).innerHTML = '<span class="result-fail">Yanlis!</span>';
        parent.querySelectorAll('.quiz-opt')[correct].classList.add('correct');
    }}
}}

/* ── Dictation ─────────────────────── */
(function() {{
    const area = document.getElementById('dictArea');
    const words = pick(lstWords, 5);
    let html = '';
    words.forEach((w, i) => {{
        const target = w[currentLang] || w.en;
        html += `<div style="margin-bottom:10px;padding:8px;background:rgba(10,14,39,0.4);border-radius:8px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <button class="play-btn" style="padding:6px 14px;font-size:13px;" onclick="speak('${{target.replace(/'/g,"\\\\'")}}',currentLang)">&#128266; Dinle</button>
            <button class="tts-btn" onclick="speakSlow('${{target.replace(/'/g,"\\\\'")}}',currentLang)">&#128034; Yavas</button>
            <input type="text" class="dict-input" id="dictInp${{i}}" placeholder="Duydugunuzu yazin..." style="flex:1;min-width:150px;margin:0;">
            <button class="check-btn" onclick="dictCheck(${{i}},'${{target.replace(/'/g,"\\\\'")}}')">Kontrol</button>
            <span id="dictFb${{i}}"></span>
        </div>`;
    }});
    area.innerHTML = html;

    window.dictCheck = (i, target) => {{
        const inp = document.getElementById('dictInp'+i).value.trim();
        const fb = document.getElementById('dictFb'+i);
        if (inp.toLowerCase() === target.toLowerCase()) {{
            fb.innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
        }} else {{
            fb.innerHTML = `<span class="result-fail">&#10008; Dogru: ${{target}}</span>`;
        }}
    }};
}})();

/* ── Word Recognition ──────────────── */
(function() {{
    const area = document.getElementById('wrArea');
    const words = pick(lstWords, 5);
    let qi = 0, score = 0;

    function renderQ() {{
        if (qi >= words.length) {{
            const pct = Math.round(score/words.length*100);
            area.innerHTML = `<div class="game-msg">&#128065; Kelime Tanima Sonucu: ${{score}}/${{words.length}}</div><div class="score-stars">${{stars(pct)}}</div><button class="game-restart" onclick="location.reload()">Tekrar</button>`;
            return;
        }}
        const w = words[qi];
        const correct = w.tr;
        let opts = [correct];
        while (opts.length < 4) {{
            const rw = lstWords[Math.floor(Math.random()*lstWords.length)];
            if (!opts.includes(rw.tr)) opts.push(rw.tr);
        }}
        opts = shuffle(opts);
        const target = w[currentLang] || w.en;

        area.innerHTML = `
            <div class="progress-bar"><div class="progress-fill" style="width:${{qi/words.length*100}}%"></div></div>
            <div style="text-align:center;margin:12px 0;">
                <button class="play-btn" onclick="speak('${{target.replace(/'/g,"\\\\'")}}',currentLang)">&#128266; Kelimeyi Dinle</button>
                <div style="color:#8888aa;font-size:12px;margin-top:6px;">${{qi+1}}/${{words.length}}</div>
            </div>
            <div style="text-align:center;">
                ${{opts.map(o => `<span class="wr-card" onclick="wrPick(this,'${{o.replace(/'/g,"\\\\'")}}','${{correct.replace(/'/g,"\\\\'")}}')">${{o}}</span>`).join('')}}
            </div>
            <div id="wrFb" style="text-align:center;margin-top:8px;"></div>`;
        // Auto-speak the word
        setTimeout(() => speak(target, currentLang), 300);
    }}

    window.wrPick = (el, picked, correct) => {{
        document.querySelectorAll('.wr-card').forEach(c => c.style.pointerEvents='none');
        if (picked === correct) {{
            el.classList.add('correct');
            score++;
        }} else {{
            el.classList.add('wrong');
            document.querySelectorAll('.wr-card').forEach(c => {{ if(c.textContent===correct) c.classList.add('correct'); }});
        }}
        qi++;
        setTimeout(renderQ, 1000);
    }};
    renderQ();
}})();

/* ── Speed Listening ───────────────── */
(function() {{
    const area = document.getElementById('slArea');
    const words = pick(lstWords, 10);
    let qi = 0, score = 0, timeLeft = 60;

    area.innerHTML = `<div style="text-align:center;"><button class="play-btn" onclick="startSL()">&#9889; Basla</button></div>`;

    window.startSL = () => {{
        qi = 0; score = 0; timeLeft = 60;
        renderSLQ();
        window._slTimer = setInterval(() => {{
            timeLeft--;
            const el = document.getElementById('slTimer');
            if (el) el.textContent = timeLeft+'s';
            if (timeLeft <= 0) {{ clearInterval(window._slTimer); endSL(); }}
        }}, 1000);
    }};

    function renderSLQ() {{
        if (qi >= words.length) {{ clearInterval(window._slTimer); endSL(); return; }}
        const w = words[qi];
        const target = w[currentLang] || w.en;
        let opts = [w.tr];
        while (opts.length < 4) {{
            const rw = lstWords[Math.floor(Math.random()*lstWords.length)];
            if (!opts.includes(rw.tr)) opts.push(rw.tr);
        }}
        opts = shuffle(opts);

        area.innerHTML = `
            <div class="speed-timer" id="slTimer">${{timeLeft}}s</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{score}}</div><div class="game-stat-lbl">Dogru</div></div>
                <div class="game-stat"><div class="game-stat-val">${{qi+1}}/${{words.length}}</div><div class="game-stat-lbl">Soru</div></div>
            </div>
            <div style="text-align:center;margin:8px 0;">
                <button class="play-btn" style="padding:6px 14px;" onclick="speak('${{target.replace(/'/g,"\\\\'")}}',currentLang)">&#128266; Tekrar Dinle</button>
            </div>
            <div style="text-align:center;">
                ${{opts.map(o => `<span class="wr-card" onclick="slPick(this,'${{o.replace(/'/g,"\\\\'")}}','${{w.tr.replace(/'/g,"\\\\'")}}')">${{o}}</span>`).join('')}}
            </div>`;
        setTimeout(() => speak(target, currentLang), 200);
    }}

    window.slPick = (el, picked, correct) => {{
        document.querySelectorAll('.wr-card').forEach(c => c.style.pointerEvents='none');
        if (picked === correct) {{
            el.classList.add('correct');
            score++;
        }} else {{
            el.classList.add('wrong');
            document.querySelectorAll('.wr-card').forEach(c => {{ if(c.textContent===correct) c.classList.add('correct'); }});
        }}
        qi++;
        setTimeout(renderSLQ, 700);
    }};

    function endSL() {{
        const pct = words.length>0 ? Math.round(score/words.length*100) : 0;
        area.innerHTML = `<div class="game-msg">&#9889; Hizli Dinleme Bitti!</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val">${{score}}/${{words.length}}</div><div class="game-stat-lbl">Dogru</div></div>
            </div>
            <div class="score-stars">${{stars(pct)}}</div>
            <button class="game-restart" onclick="startSL()">Tekrar</button>`;
    }}
}})();
</script>""")

    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# 5) ENHANCED QUIZ
# ---------------------------------------------------------------------------

def build_enhanced_quiz_html(data: dict) -> str:
    """Enhanced quiz with timed mode, fill in blank, match pairs, confetti."""
    questions = data.get("quiz", [])
    vocab = data.get("vocab", [])
    all_words = []
    for t in vocab:
        for w in t.get("words", []):
            all_words.append(w)
    q_json = json.dumps(questions, ensure_ascii=False)
    words_json = json.dumps(all_words, ensure_ascii=False)

    return _DIAMOND_CSS + _lang_bar_html() + """
<style>
.quiz-mode-tabs { display: flex; gap: 8px; justify-content: center; margin: 12px 0; flex-wrap: wrap; }
.qm-tab { padding: 8px 16px; border: 1px solid rgba(199,165,93,0.3); background: rgba(20,24,82,0.5); color: #c7a55d; border-radius: 20px; cursor: pointer; font-size: 13px; transition: all 0.3s; }
.qm-tab.active { background: rgba(199,165,93,0.2); border-color: #c7a55d; font-weight: bold; }
.progress-bar { height: 8px; background: rgba(199,165,93,0.15); border-radius: 4px; margin: 10px 0; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg,#c7a55d,#a08040); border-radius: 4px; transition: width 0.3s; }
.fib-input { padding: 8px 14px; background: rgba(10,14,39,0.8); border: 1px solid rgba(199,165,93,0.3); color: #e0e0e0; border-radius: 8px; font-size: 15px; width: 200px; }
.mp-item { display: inline-block; padding: 10px 18px; margin: 6px; border: 2px solid rgba(199,165,93,0.25); border-radius: 10px; cursor: pointer; font-size: 14px; transition: all 0.2s; }
.mp-item:hover { border-color: #c7a55d; }
.mp-item.selected { border-color: #c7a55d; background: rgba(199,165,93,0.15); color: #c7a55d; }
.mp-item.matched { border-color: #4ade80; background: rgba(74,222,128,0.1); color: #4ade80; pointer-events: none; }
.mp-item.wrong { border-color: #f87171; animation: shake 0.3s; }
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-5px)} 75%{transform:translateX(5px)} }
.score-stars { font-size: 32px; text-align: center; margin: 10px 0; }
.game-msg { text-align: center; padding: 14px; font-size: 20px; color: #c7a55d; font-weight: bold; }
.game-restart { display: block; margin: 12px auto; background: linear-gradient(135deg,#c7a55d,#a08040); border: none; color: #0a0e27; padding: 10px 28px; border-radius: 10px; cursor: pointer; font-size: 15px; font-weight: bold; }
.game-stats { display: flex; justify-content: center; gap: 24px; margin: 10px 0; }
.game-stat { text-align: center; }
.game-stat-val { font-size: 22px; font-weight: bold; color: #c7a55d; }
.game-stat-lbl { font-size: 11px; color: #8888aa; }
.speed-timer { font-size: 28px; color: #c7a55d; font-weight: bold; text-align: center; margin: 8px 0; }
.confetti-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; }
</style>

<div class="quiz-mode-tabs">
    <button class="qm-tab active" onclick="quizMode(0,this)">&#127919; Klasik Quiz</button>
    <button class="qm-tab" onclick="quizMode(1,this)">&#9201; Sureli Mod</button>
    <button class="qm-tab" onclick="quizMode(2,this)">&#9999;&#65039; Bosluk Doldur</button>
    <button class="qm-tab" onclick="quizMode(3,this)">&#128279; Eslestir</button>
</div>
<div class="progress-bar"><div class="progress-fill" id="quizProg" style="width:0%"></div></div>
<div id="quizMain"></div>
<canvas id="confettiCanvas" class="confetti-canvas" style="display:none;"></canvas>
""" + _base_js() + f"""
<script>
const qzData = {q_json};
const qzWords = {words_json};

function shuffle(a) {{ const b=[...a]; for(let i=b.length-1;i>0;i--){{ const j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]; }} return b; }}
function pick(arr,n) {{ return shuffle(arr).slice(0,Math.min(n,arr.length)); }}
function stars(pct) {{ const s=pct>=90?5:pct>=75?4:pct>=60?3:pct>=40?2:1; return '&#11088;'.repeat(s)+'&#9734;'.repeat(5-s); }}

function quizMode(idx, btn) {{
    document.querySelectorAll('.qm-tab').forEach(t=>t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('quizProg').style.width='0%';
    [classicQuiz, timedQuiz, fillBlankQuiz, matchPairs][idx]();
}}

/* ── Confetti ──────────────────────── */
function fireConfetti() {{
    const canvas = document.getElementById('confettiCanvas');
    canvas.style.display = 'block';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext('2d');
    const pieces = [];
    const colors = ['#c7a55d','#4ade80','#f87171','#3b82f6','#fbbf24','#a78bfa'];
    for (let i=0;i<150;i++) {{
        pieces.push({{
            x: Math.random()*canvas.width,
            y: -10 - Math.random()*200,
            w: 6+Math.random()*6,
            h: 10+Math.random()*8,
            rot: Math.random()*360,
            color: colors[Math.floor(Math.random()*colors.length)],
            vy: 2+Math.random()*3,
            vx: -1+Math.random()*2,
            vr: -2+Math.random()*4
        }});
    }}
    let frames = 0;
    function draw() {{
        ctx.clearRect(0,0,canvas.width,canvas.height);
        pieces.forEach(p => {{
            ctx.save();
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot * Math.PI/180);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);
            ctx.restore();
            p.y += p.vy;
            p.x += p.vx;
            p.rot += p.vr;
        }});
        frames++;
        if (frames < 180) requestAnimationFrame(draw);
        else canvas.style.display = 'none';
    }}
    draw();
}}

/* ── Classic Quiz (dynamic from vocab + selected language) ── */
function classicQuiz() {{
    const area = document.getElementById('quizMain');
    const total = 15;
    const words = pick(qzWords, total);
    let qi = 0, score = 0;
    let answered = false;

    function renderQ() {{
        if (qi >= words.length) {{
            const pct = Math.round(score/words.length*100);
            document.getElementById('quizProg').style.width='100%';
            area.innerHTML = `<div class="game-msg">&#127942; Quiz Sonucu: ${{score}}/${{words.length}} (%${{pct}})</div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="classicQuiz()">Tekrar Dene</button>`;
            if (pct >= 90) fireConfetti();
            return;
        }}
        answered = false;
        document.getElementById('quizProg').style.width = (qi/words.length*100)+'%';
        const w = words[qi];
        const correct = w[currentLang] || w.en;
        // Random question type: 0=TR->Lang, 1=Lang->TR, 2=TF
        const qType = Math.floor(Math.random()*3);

        if (qType <= 1) {{
            // Multiple choice
            const isTrToLang = qType === 0;
            const prompt = isTrToLang ? w.tr : (correct + ' ' + (w.img||''));
            const answer = isTrToLang ? correct : w.tr;
            const wrongPool = qzWords.filter(x => x.tr !== w.tr);
            const wrongs = pick(wrongPool, 3).map(x => isTrToLang ? (x[currentLang]||x.en) : x.tr);
            const opts = shuffle([answer, ...wrongs]);
            const correctIdx = opts.indexOf(answer);
            const label = isTrToLang ? 'Turkce &#8594; Ceviri' : 'Ceviri &#8594; Turkce';
            let html = `<div class="quiz-q"><div style="font-size:11px;color:#8888aa;margin-bottom:4px;">${{label}}</div>
                <div class="quiz-q-text">${{qi+1}}. ${{w.img||''}} <b style="color:#c7a55d;">${{prompt}}</b></div>`;
            opts.forEach((o,oi) => {{
                html += `<label class="quiz-opt" onclick="cqPick(${{oi}},${{correctIdx}},this)">${{String.fromCharCode(65+oi)}}) ${{o}}</label>`;
            }});
            html += `<div id="cqFb" style="margin-top:6px;"></div></div>`;
            area.innerHTML = html;
        }} else {{
            // True/False
            const isCorrect = Math.random() > 0.4;
            const shownTranslation = isCorrect ? correct : pick(qzWords.filter(x=>x.tr!==w.tr),1).map(x=>x[currentLang]||x.en)[0] || correct;
            area.innerHTML = `<div class="quiz-q">
                <div style="font-size:11px;color:#8888aa;margin-bottom:4px;">Dogru / Yanlis</div>
                <div class="quiz-q-text">${{qi+1}}. ${{w.img||''}} <b style="color:#c7a55d;">${{w.tr}}</b> = <b>${{shownTranslation}}</b></div>
                <div class="tf-btns">
                    <button class="tf-btn" onclick="cqPickTF(true,${{isCorrect}},this)">&#9989; Dogru</button>
                    <button class="tf-btn" onclick="cqPickTF(false,${{isCorrect}},this)">&#10060; Yanlis</button>
                </div>
                <div id="cqFb" style="margin-top:6px;"></div></div>`;
        }}
    }}

    window.cqPick = (oi, ans, el) => {{
        if (answered) return; answered = true;
        el.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.style.pointerEvents='none');
        if (oi === ans) {{
            el.classList.add('correct');
            score++;
            speak(el.textContent.slice(3), currentLang);
            document.getElementById('cqFb').innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
        }} else {{
            el.classList.add('wrong');
            el.parentElement.querySelectorAll('.quiz-opt')[ans].classList.add('correct');
            document.getElementById('cqFb').innerHTML = '<span class="result-fail">&#10008; Yanlis!</span>';
        }}
        qi++;
        setTimeout(renderQ, 1100);
    }};
    window.cqPickTF = (val, ans, el) => {{
        if (answered) return; answered = true;
        el.parentElement.querySelectorAll('.tf-btn').forEach(b => b.style.pointerEvents='none');
        if (val === ans) {{
            el.style.borderColor = '#4ade80'; el.style.color = '#4ade80';
            score++;
            document.getElementById('cqFb').innerHTML = '<span class="result-ok">&#10004; Dogru!</span>';
        }} else {{
            el.style.borderColor = '#f87171'; el.style.color = '#f87171';
            document.getElementById('cqFb').innerHTML = '<span class="result-fail">&#10008; Yanlis!</span>';
        }}
        qi++;
        setTimeout(renderQ, 1100);
    }};
    renderQ();
}}

/* ── Timed Quiz (dynamic from vocab + selected language) ── */
function timedQuiz() {{
    const area = document.getElementById('quizMain');
    let timeLeft = 90, correct = 0, wrong = 0, total = 0;
    const words = shuffle([...qzWords]);
    let qi = 0;
    let answered = false;

    const timer = setInterval(() => {{
        timeLeft--;
        const el = document.getElementById('tqTimer');
        if (el) el.textContent = timeLeft+'s';
        if (timeLeft <= 10 && el) el.style.color = '#f87171';
        if (timeLeft <= 0) {{ clearInterval(timer); endTimed(); }}
    }}, 1000);

    function showQ() {{
        if (qi >= words.length || timeLeft <= 0) {{ clearInterval(timer); endTimed(); return; }}
        answered = false;
        total++;
        const w = words[qi];
        const correctAns = w[currentLang] || w.en;
        const wrongPool = qzWords.filter(x => (x[currentLang]||x.en) !== correctAns);
        const wrongs = pick(wrongPool, 3).map(x => x[currentLang]||x.en);
        const opts = shuffle([correctAns, ...wrongs]);
        const correctIdx = opts.indexOf(correctAns);

        area.innerHTML = `<div class="speed-timer" id="tqTimer" style="color:${{timeLeft<=10?'#f87171':'#c7a55d'}}">${{timeLeft}}s</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{correct}}</div><div class="game-stat-lbl">Dogru</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#f87171;">${{wrong}}</div><div class="game-stat-lbl">Yanlis</div></div>
            </div>
            <div class="quiz-q">
                <div class="quiz-q-text">${{w.img||''}} <b style="color:#c7a55d;font-size:20px;">${{w.tr}}</b></div>
                ${{opts.map((o,oi) => `<label class="quiz-opt" onclick="tqPick(${{oi}},${{correctIdx}},this)">${{String.fromCharCode(65+oi)}}) ${{o}}</label>`).join('')}}
            </div>`;
    }}

    window.tqPick = (oi, ans, el) => {{
        if (answered) return; answered = true;
        el.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.style.pointerEvents='none');
        if (oi === ans) {{ el.classList.add('correct'); correct++; }}
        else {{ el.classList.add('wrong'); wrong++; el.parentElement.querySelectorAll('.quiz-opt')[ans].classList.add('correct'); }}
        qi++;
        setTimeout(showQ, 500);
    }};

    function endTimed() {{
        const pct = total>0 ? Math.round(correct/total*100) : 0;
        document.getElementById('quizProg').style.width='100%';
        area.innerHTML = `<div class="game-msg">&#9201; Sureli Quiz Bitti!</div>
            <div class="game-stats">
                <div class="game-stat"><div class="game-stat-val">${{total}}</div><div class="game-stat-lbl">Toplam</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#4ade80;">${{correct}}</div><div class="game-stat-lbl">Dogru</div></div>
                <div class="game-stat"><div class="game-stat-val" style="color:#f87171;">${{wrong}}</div><div class="game-stat-lbl">Yanlis</div></div>
            </div>
            <div class="score-stars">${{stars(pct)}}</div>
            <button class="game-restart" onclick="timedQuiz()">Tekrar</button>`;
        if (pct >= 90) fireConfetti();
    }}
    showQ();
}}

/* ── Fill in the Blank ─────────────── */
function fillBlankQuiz() {{
    const area = document.getElementById('quizMain');
    const words = pick(qzWords, 8);
    let qi = 0, score = 0;

    function renderQ() {{
        if (qi >= words.length) {{
            const pct = Math.round(score/words.length*100);
            document.getElementById('quizProg').style.width='100%';
            area.innerHTML = `<div class="game-msg">&#9999;&#65039; Bosluk Doldur Sonucu: ${{score}}/${{words.length}}</div>
                <div class="score-stars">${{stars(pct)}}</div>
                <button class="game-restart" onclick="fillBlankQuiz()">Tekrar</button>`;
            if (pct >= 90) fireConfetti();
            return;
        }}
        document.getElementById('quizProg').style.width = (qi/words.length*100)+'%';
        const w = words[qi];
        const target = w[currentLang] || w.en;
        // Show first and last letter as hint
        const hint = target[0] + '_'.repeat(Math.max(1,target.length-2)) + (target.length>1 ? target[target.length-1] : '');
        area.innerHTML = `
            <div class="quiz-q">
                <div class="quiz-q-text">${{qi+1}}. Turkce: <b style="color:#c7a55d;">${{w.tr}}</b> ${{w.img||''}}</div>
                <div style="color:#8888aa;font-size:13px;margin:6px 0;">Ipucu: ${{hint}}</div>
                <div style="display:flex;gap:8px;align-items:center;margin-top:8px;">
                    <input type="text" class="fib-input" id="fibInp" placeholder="Cevir...">
                    <button class="check-btn" onclick="fibCheck()">Kontrol</button>
                </div>
                <div id="fibFb" style="margin-top:6px;"></div>
            </div>`;
    }}

    window.fibCheck = () => {{
        const w = words[qi];
        const target = (w[currentLang] || w.en).toLowerCase();
        const inp = document.getElementById('fibInp').value.trim().toLowerCase();
        const fb = document.getElementById('fibFb');
        if (inp === target) {{
            score++;
            fb.innerHTML = '<span class="result-ok" style="font-size:16px;">&#10004; Dogru!</span>';
            speak(w[currentLang]||w.en, currentLang);
        }} else {{
            fb.innerHTML = `<span class="result-fail" style="font-size:16px;">&#10008; Dogru: ${{w[currentLang]||w.en}}</span>`;
        }}
        qi++;
        setTimeout(renderQ, 1200);
    }};
    renderQ();
}}

/* ── Match Pairs ───────────────────── */
function matchPairs() {{
    const area = document.getElementById('quizMain');
    const words = pick(qzWords, 5);
    let selected = null, matched = 0;
    const trItems = shuffle(words.map((w,i) => ({{ text: w.tr, id: i, side: 'tr' }})));
    const langItems = shuffle(words.map((w,i) => ({{ text: w[currentLang]||w.en, id: i, side: 'lang' }})));

    function render() {{
        document.getElementById('quizProg').style.width = (matched/words.length*100)+'%';
        let html = `<div style="text-align:center;margin-bottom:8px;color:#8888aa;font-size:13px;">Turkce kelimeleri cevrileriyle esleyin (${{matched}}/${{words.length}})</div>`;
        html += '<div style="display:flex;justify-content:center;gap:30px;flex-wrap:wrap;">';
        html += '<div style="text-align:center;"><div style="color:#c7a55d;font-size:13px;margin-bottom:6px;">Turkce</div>';
        trItems.forEach((item,i) => {{
            const cls = item.matched ? 'matched' : (selected && selected.side==='tr' && selected.idx===i ? 'selected' : '');
            html += `<div class="mp-item ${{cls}}" onclick="mpClick('tr',${{i}})">${{item.text}}</div><br>`;
        }});
        html += '</div><div style="text-align:center;"><div style="color:#c7a55d;font-size:13px;margin-bottom:6px;">Ceviri</div>';
        langItems.forEach((item,i) => {{
            const cls = item.matched ? 'matched' : (selected && selected.side==='lang' && selected.idx===i ? 'selected' : '');
            html += `<div class="mp-item ${{cls}}" onclick="mpClick('lang',${{i}})">${{item.text}}</div><br>`;
        }});
        html += '</div></div>';

        if (matched === words.length) {{
            html += `<div class="game-msg">&#127881; Tebrikler! Tum eslesmeleri buldun!</div>
                <div class="score-stars">${{stars(100)}}</div>
                <button class="game-restart" onclick="matchPairs()">Tekrar</button>`;
            area.innerHTML = html;
            fireConfetti();
            return;
        }}
        area.innerHTML = html;
    }}

    window.mpClick = (side, idx) => {{
        const items = side==='tr' ? trItems : langItems;
        if (items[idx].matched) return;

        if (!selected) {{
            selected = {{ side, idx }};
            render();
        }} else {{
            if (selected.side === side) {{
                selected = {{ side, idx }};
                render();
            }} else {{
                const a = selected.side==='tr' ? trItems[selected.idx] : langItems[selected.idx];
                const b = side==='tr' ? trItems[idx] : langItems[idx];
                if (a.id === b.id) {{
                    a.matched = true;
                    b.matched = true;
                    matched++;
                    selected = null;
                    render();
                }} else {{
                    // Wrong match - flash
                    selected = null;
                    render();
                    const allItems = document.querySelectorAll('.mp-item');
                    // Brief red flash handled by CSS animation
                }}
            }}
        }}
    }};
    render();
}}

// Start with classic quiz by default
classicQuiz();
</script>
"""
