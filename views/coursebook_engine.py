"""
Anime-style Main Course Book Engine
Generates interactive HTML5 flipbook coursebooks for preschool and grades 1-12.
Canvas-drawn anime characters, colorful illustrations, interactive elements.
"""

import json
import html as html_mod


def build_anime_coursebook(grade: int, curriculum_weeks: list, mode: str = "student") -> str:
    """Build anime-style interactive HTML5 coursebook.

    Args:
        grade: 0=preschool, 1-4=elementary, 5-8=middle, 9-12=high
        curriculum_weeks: List of week dicts from curriculum_*.py
        mode: 'student' | 'teacher' | 'parent'

    Returns:
        Complete HTML string with embedded CSS+JS+Canvas
    """
    grade = max(0, min(12, grade))

    # --- Grade config ---
    GRADE_COLORS = {
        0: "#f472b6", 1: "#38bdf8", 2: "#4ade80", 3: "#a78bfa", 4: "#fb923c",
        5: "#06b6d4", 6: "#8b5cf6", 7: "#ec4899", 8: "#14b8a6",
        9: "#f43f5e", 10: "#3b82f6", 11: "#10b981", 12: "#f59e0b",
    }
    GRADE_LABELS = {
        0: "Preschool", 1: "Grade 1", 2: "Grade 2", 3: "Grade 3", 4: "Grade 4",
        5: "Grade 5", 6: "Grade 6", 7: "Grade 7", 8: "Grade 8",
        9: "Grade 9", 10: "Grade 10", 11: "Grade 11", 12: "Grade 12",
    }
    FONT_SIZES = {
        0: 24, 1: 20, 2: 18, 3: 15, 4: 14,
        5: 14, 6: 13, 7: 13, 8: 13,
        9: 13, 10: 12, 11: 12, 12: 12,
    }
    accent = GRADE_COLORS[grade]
    font_sz = FONT_SIZES[grade]
    label = GRADE_LABELS[grade]
    if grade == 0:
        book_title = "Early Steps"
    elif grade <= 4:
        book_title = f"Bright Start {grade}"
    elif grade <= 8:
        book_title = f"Next Level {grade}"
    else:
        book_title = f"English Core {grade}"

    # --- Build pages ---
    if not curriculum_weeks:
        curriculum_weeks = [{"theme": f"Week {i+1}", "vocab": [], "skills": {}, "structure": ""} for i in range(36)]

    weeks_per_unit = max(1, len(curriculum_weeks) // 10) if len(curriculum_weeks) >= 10 else max(1, len(curriculum_weeks))
    units = []
    for i in range(0, len(curriculum_weeks), weeks_per_unit):
        uw = curriculum_weeks[i:i + weeks_per_unit]
        units.append({
            "num": len(units) + 1,
            "title": uw[0].get("theme", f"Unit {len(units) + 1}"),
            "weeks": uw,
        })

    pages = [{"type": "cover", "title": book_title, "grade": grade}]

    for unit in units:
        pages.append({"type": "unit_opener", "unit": unit["num"], "title": unit["title"]})

        all_vocab = []
        for w in unit["weeks"]:
            all_vocab.extend(w.get("vocab", []))
        all_vocab = list(dict.fromkeys(all_vocab))

        pages.append({"type": "vocabulary", "unit": unit["num"], "words": all_vocab})
        pages.append({"type": "story", "unit": unit["num"], "title": unit["title"], "words": all_vocab[:8]})
        pages.append({"type": "song", "unit": unit["num"], "theme": unit["title"]})

        # Grammar — grade 3+
        if grade >= 3:
            structure = unit["weeks"][0].get("structure", "")
            pages.append({"type": "grammar", "unit": unit["num"], "rule": structure})

        # Dialogue — grade 5+
        if grade >= 5:
            pages.append({"type": "dialogue", "unit": unit["num"], "title": unit["title"], "words": all_vocab[:8]})

        # Writing Model — grade 7+
        if grade >= 7:
            pages.append({"type": "writing", "unit": unit["num"], "title": unit["title"]})

        pages.append({"type": "activity", "unit": unit["num"], "words": all_vocab})

        skills = unit["weeks"][0].get("skills", {})
        pages.append({"type": "review", "unit": unit["num"], "skills": skills})

    pages.append({"type": "back_cover"})

    pages_json = json.dumps(pages, ensure_ascii=False)
    mode_json = json.dumps(mode)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#0B0F19;color:#E2E8F0;font-family:'Segoe UI',system-ui,sans-serif;font-size:{font_sz}px;overflow-x:hidden;}}
.book-container{{max-width:820px;margin:0 auto;padding:12px;}}
.page{{background:#131825;border-radius:16px;padding:30px;min-height:520px;position:relative;
  border-top:4px solid {accent};transition:opacity .4s,transform .5s;}}
.page.flip-out{{opacity:0;transform:perspective(800px) rotateY(-90deg);}}
.page.flip-in{{opacity:0;transform:perspective(800px) rotateY(90deg);}}
.page.active{{opacity:1;transform:perspective(800px) rotateY(0deg);}}
.nav-bar{{display:flex;justify-content:center;align-items:center;gap:14px;padding:14px 0;}}
.nav-btn{{background:#1A2035;border:1px solid {accent};color:{accent};border-radius:10px;
  padding:10px 22px;cursor:pointer;font-size:15px;font-weight:600;transition:.2s;}}
.nav-btn:hover{{background:{accent};color:#0B0F19;}}
.nav-btn:disabled{{opacity:.35;cursor:default;}}
.page-indicator{{color:#94A3B8;font-size:13px;min-width:80px;text-align:center;}}
canvas.char-canvas{{display:block;margin:0 auto 12px;}}
.page-title{{font-size:{font_sz + 10}px;font-weight:800;text-align:center;margin:10px 0 18px;
  background:linear-gradient(135deg,{accent},#6366F1);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;}}
.sub-title{{font-size:{font_sz + 2}px;color:#94A3B8;text-align:center;margin-bottom:14px;}}
.vocab-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;margin:16px 0;}}
.vocab-card{{background:#1A2035;border:1px solid #2D3555;border-radius:12px;padding:16px 10px;
  text-align:center;cursor:pointer;transition:.25s;user-select:none;}}
.vocab-card:hover{{transform:scale(1.07);border-color:{accent};box-shadow:0 0 14px {accent}44;}}
.vocab-card .word{{font-size:{font_sz + 4}px;font-weight:700;color:{accent};}}
.vocab-card .icon{{font-size:28px;margin-bottom:6px;}}
.vocab-card .speaker{{font-size:18px;margin-top:6px;opacity:.6;}}
.speech-bubble{{background:#1A2035;border:1px solid #2D3555;border-radius:16px;padding:14px 18px;
  margin:10px 0;position:relative;font-size:{font_sz}px;line-height:1.6;}}
.speech-bubble::before{{content:'';position:absolute;left:30px;top:-10px;
  border-left:10px solid transparent;border-right:10px solid transparent;border-bottom:10px solid #2D3555;}}
.song-line{{padding:6px 0;font-size:{font_sz + 1}px;}}
.song-line .note{{color:{accent};margin-right:6px;}}
.grammar-box{{background:#1E2540;border-left:4px solid {accent};border-radius:8px;padding:18px;margin:14px 0;}}
.grammar-box h3{{color:{accent};margin-bottom:8px;}}
.activity-area{{background:#1A2035;border-radius:12px;padding:20px;margin:14px 0;}}
.fill-blank{{display:inline-block;border-bottom:2px dashed {accent};min-width:80px;padding:2px 8px;
  color:{accent};cursor:pointer;margin:0 4px;}}
.review-item{{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #1E2540;}}
.star-btn{{cursor:pointer;font-size:22px;transition:.2s;}}
.star-btn:hover{{transform:scale(1.3);}}
.cover-page{{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:500px;}}
.cover-page .big-title{{font-size:{font_sz + 18}px;font-weight:900;text-align:center;
  background:linear-gradient(135deg,{accent},#818CF8,#6366F1);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;margin:16px 0;}}
.cover-page .grade-badge{{background:{accent};color:#0B0F19;padding:8px 24px;border-radius:20px;
  font-weight:700;font-size:{font_sz + 2}px;margin-top:8px;}}
.culture-box{{background:#1A2540;border-radius:12px;padding:16px;margin:10px 0;
  border:1px solid #2D3555;}}
.teacher-note{{background:#2D1B4E;border-left:3px solid #A78BFA;border-radius:8px;
  padding:12px;margin:10px 0;font-style:italic;color:#C4B5FD;display:{{"block" if mode == "teacher" else "none"}};}}
.grade-5 .page{{border-top:4px solid #06b6d4;}}
.grade-6 .page{{border-top:4px solid #8b5cf6;}}
.grade-7 .page{{border-top:4px solid #ec4899;}}
.grade-8 .page{{border-top:4px solid #14b8a6;}}
.grade-9 .page{{border-top:4px solid #f43f5e;}}
.grade-10 .page{{border-top:4px solid #3b82f6;}}
.grade-11 .page{{border-top:4px solid #10b981;}}
.grade-12 .page{{border-top:4px solid #f59e0b;}}
.dialogue-container{{margin:16px 0;}}
.dialogue-line{{display:flex;align-items:flex-start;gap:12px;margin:10px 0;}}
.dialogue-line.right{{flex-direction:row-reverse;}}
.dialogue-line .dlg-bubble{{background:#1A2035;border:1px solid #2D3555;border-radius:14px;padding:12px 16px;
  max-width:70%;cursor:pointer;transition:.2s;}}
.dialogue-line .dlg-bubble:hover{{border-color:{accent};}}
.dialogue-line .dlg-name{{font-weight:700;font-size:12px;margin-bottom:4px;}}
.writing-section{{background:#1A2035;border-radius:12px;padding:20px;margin:14px 0;}}
.writing-model{{background:#131825;border-radius:8px;padding:16px;margin:10px 0;line-height:1.8;
  border-left:3px solid {accent};}}
.writing-prompt{{background:#1E2540;border-radius:8px;padding:14px;margin:10px 0;
  border:1px dashed {accent};}}
.key-phrase{{background:{accent}22;color:{accent};padding:2px 6px;border-radius:4px;font-weight:600;}}
</style>
</head>
<body>
<div class="book-container grade-{grade}">
  <div class="page active" id="pageArea"></div>
  <div class="nav-bar">
    <button class="nav-btn" id="btnPrev" onclick="navigate(-1)">&larr; Onceki</button>
    <span class="page-indicator" id="pageInd">1 / 1</span>
    <button class="nav-btn" id="btnNext" onclick="navigate(1)">Sonraki &rarr;</button>
  </div>
</div>

<script>
(function(){{
"use strict";
const PAGES={pages_json};
const GRADE={grade};
const ACCENT="{accent}";
const MODE={mode_json};
const FONT_SZ={font_sz};
let curPage=0;
let animating=false;
const pageEl=document.getElementById("pageArea");
const indEl=document.getElementById("pageInd");
const btnP=document.getElementById("btnPrev");
const btnN=document.getElementById("btnNext");

// ── Emoji helpers ──
const WORD_ICONS={{"hello":"👋","hi":"👋","cat":"🐱","dog":"🐕","bird":"🐦","fish":"🐟",
"apple":"🍎","banana":"🍌","water":"💧","milk":"🥛","book":"📖","pen":"🖊️","school":"🏫",
"teacher":"👩‍🏫","friend":"👫","family":"👨‍👩‍👧‍👦","house":"🏠","home":"🏠","car":"🚗","bus":"🚌",
"tree":"🌳","flower":"🌸","sun":"☀️","moon":"🌙","star":"⭐","red":"🔴","blue":"🔵",
"green":"🟢","yellow":"🟡","happy":"😊","sad":"😢","big":"🐘","small":"🐜","one":"1️⃣",
"two":"2️⃣","three":"3️⃣","mother":"👩","father":"👨","sister":"👧","brother":"👦",
"rain":"🌧️","snow":"❄️","hot":"🔥","cold":"🥶","eat":"🍽️","drink":"🥤","play":"⚽",
"run":"🏃","jump":"🤸","sing":"🎤","dance":"💃","read":"📚","write":"✏️","color":"🎨",
"number":"🔢","animal":"🐾","food":"🍔","toy":"🧸","ball":"⚽","baby":"👶","boy":"👦","girl":"👧"}};
function wordIcon(w){{let k=w.toLowerCase().trim();return WORD_ICONS[k]||"📝";}}

// ── TTS ──
function speak(text){{
  if(!window.speechSynthesis)return;
  window.speechSynthesis.cancel();
  let u=new SpeechSynthesisUtterance(text);
  u.lang="en-US";u.rate=GRADE<=1?0.75:0.9;
  window.speechSynthesis.speak(u);
}}

// ── Canvas character drawing ──
function createCanvas(w,h){{
  let c=document.createElement("canvas");
  c.width=w;c.height=h;c.className="char-canvas";
  return c;
}}

function drawCharPreschool(ctx,x,y,sz,emotion){{
  // Body
  ctx.fillStyle="#FFD93D";
  ctx.beginPath();ctx.ellipse(x,y+sz*0.6,sz*0.3,sz*0.35,0,0,Math.PI*2);ctx.fill();
  // Head
  ctx.fillStyle="#FFEAA7";
  ctx.beginPath();ctx.arc(x,y,sz*0.4,0,Math.PI*2);ctx.fill();
  // Eyes
  let ey=y-sz*0.05;
  ctx.fillStyle="#2D3436";
  ctx.beginPath();ctx.arc(x-sz*0.12,ey,sz*0.06,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.12,ey,sz*0.06,0,Math.PI*2);ctx.fill();
  // Eye highlights
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.arc(x-sz*0.1,ey-sz*0.02,sz*0.02,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.14,ey-sz*0.02,sz*0.02,0,Math.PI*2);ctx.fill();
  // Cheeks
  ctx.fillStyle="rgba(244,114,182,0.4)";
  ctx.beginPath();ctx.arc(x-sz*0.22,y+sz*0.08,sz*0.07,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.22,y+sz*0.08,sz*0.07,0,Math.PI*2);ctx.fill();
  // Mouth
  ctx.strokeStyle="#2D3436";ctx.lineWidth=2;
  ctx.beginPath();
  if(emotion==="happy"||emotion==="excited"){{ctx.arc(x,y+sz*0.12,sz*0.1,0,Math.PI);}}
  else if(emotion==="surprised"){{ctx.fillStyle="#2D3436";ctx.beginPath();ctx.arc(x,y+sz*0.14,sz*0.05,0,Math.PI*2);ctx.fill();return;}}
  else if(emotion==="thinking"){{ctx.moveTo(x-sz*0.06,y+sz*0.15);ctx.lineTo(x+sz*0.06,y+sz*0.15);}}
  else{{ctx.arc(x,y+sz*0.12,sz*0.08,0,Math.PI);}}
  ctx.stroke();
  // Arms
  ctx.strokeStyle="#FFEAA7";ctx.lineWidth=sz*0.06;
  ctx.beginPath();ctx.moveTo(x-sz*0.28,y+sz*0.5);ctx.lineTo(x-sz*0.45,y+sz*0.35);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x+sz*0.28,y+sz*0.5);ctx.lineTo(x+sz*0.45,y+sz*0.35);ctx.stroke();
  if(emotion==="excited"){{
    // sparkles
    ctx.fillStyle=ACCENT;ctx.font=(sz*0.15)+"px sans-serif";
    ctx.fillText("✨",x-sz*0.5,y-sz*0.35);ctx.fillText("✨",x+sz*0.35,y-sz*0.3);
  }}
}}

function drawCharElementary(ctx,x,y,sz,emotion,gender){{
  let skinC="#FFEAA7",hairC=gender==="girl"?"#A0522D":"#2D3436";
  // Legs
  ctx.fillStyle="#2D3555";
  ctx.fillRect(x-sz*0.12,y+sz*0.65,sz*0.09,sz*0.25);
  ctx.fillRect(x+sz*0.03,y+sz*0.65,sz*0.09,sz*0.25);
  // Body (uniform)
  ctx.fillStyle="#38bdf8";
  ctx.beginPath();ctx.ellipse(x,y+sz*0.45,sz*0.22,sz*0.28,0,0,Math.PI*2);ctx.fill();
  // Collar
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.moveTo(x,y+sz*0.2);ctx.lineTo(x-sz*0.1,y+sz*0.32);ctx.lineTo(x+sz*0.1,y+sz*0.32);ctx.fill();
  // Head
  ctx.fillStyle=skinC;
  ctx.beginPath();ctx.arc(x,y,sz*0.3,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=hairC;
  ctx.beginPath();ctx.arc(x,y-sz*0.08,sz*0.32,Math.PI,Math.PI*2);ctx.fill();
  if(gender==="girl"){{
    ctx.beginPath();ctx.arc(x-sz*0.3,y-sz*0.05,sz*0.08,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(x+sz*0.3,y-sz*0.05,sz*0.08,0,Math.PI*2);ctx.fill();
    // Bow
    ctx.fillStyle="#f472b6";
    ctx.beginPath();ctx.moveTo(x+sz*0.25,y-sz*0.22);
    ctx.lineTo(x+sz*0.38,y-sz*0.32);ctx.lineTo(x+sz*0.35,y-sz*0.18);ctx.fill();
    ctx.beginPath();ctx.moveTo(x+sz*0.25,y-sz*0.22);
    ctx.lineTo(x+sz*0.38,y-sz*0.12);ctx.lineTo(x+sz*0.35,y-sz*0.28);ctx.fill();
  }}
  // Eyes (anime oval)
  let ey=y-sz*0.02;
  ctx.fillStyle="#2D3436";
  ctx.beginPath();ctx.ellipse(x-sz*0.1,ey,sz*0.04,sz*0.06,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(x+sz*0.1,ey,sz*0.04,sz*0.06,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.arc(x-sz*0.08,ey-sz*0.02,sz*0.018,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.12,ey-sz*0.02,sz*0.018,0,Math.PI*2);ctx.fill();
  // Mouth
  ctx.strokeStyle="#2D3436";ctx.lineWidth=1.5;
  ctx.beginPath();
  if(emotion==="happy")ctx.arc(x,y+sz*0.1,sz*0.06,0,Math.PI);
  else ctx.arc(x,y+sz*0.1,sz*0.04,0.1,Math.PI-0.1);
  ctx.stroke();
  // Cheeks
  ctx.fillStyle="rgba(244,114,182,0.3)";
  ctx.beginPath();ctx.arc(x-sz*0.18,y+sz*0.05,sz*0.04,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.18,y+sz*0.05,sz*0.04,0,Math.PI*2);ctx.fill();
  // Arms
  ctx.strokeStyle=skinC;ctx.lineWidth=sz*0.05;ctx.lineCap="round";
  ctx.beginPath();ctx.moveTo(x-sz*0.22,y+sz*0.35);ctx.lineTo(x-sz*0.38,y+sz*0.55);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x+sz*0.22,y+sz*0.35);ctx.lineTo(x+sz*0.38,y+sz*0.55);ctx.stroke();
}}

function drawCharTeacher(ctx,x,y,sz){{
  // Legs
  ctx.fillStyle="#2D3555";
  ctx.fillRect(x-sz*0.1,y+sz*0.75,sz*0.08,sz*0.2);
  ctx.fillRect(x+sz*0.02,y+sz*0.75,sz*0.08,sz*0.2);
  // Body
  ctx.fillStyle="#6366F1";
  ctx.beginPath();ctx.ellipse(x,y+sz*0.48,sz*0.24,sz*0.32,0,0,Math.PI*2);ctx.fill();
  // Head
  ctx.fillStyle="#FFEAA7";
  ctx.beginPath();ctx.arc(x,y-sz*0.05,sz*0.28,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle="#5B3A1A";
  ctx.beginPath();ctx.arc(x,y-sz*0.15,sz*0.3,Math.PI,Math.PI*2);ctx.fill();
  // Glasses
  ctx.strokeStyle="#94A3B8";ctx.lineWidth=2;
  ctx.beginPath();ctx.arc(x-sz*0.1,y-sz*0.03,sz*0.07,0,Math.PI*2);ctx.stroke();
  ctx.beginPath();ctx.arc(x+sz*0.1,y-sz*0.03,sz*0.07,0,Math.PI*2);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x-sz*0.03,y-sz*0.03);ctx.lineTo(x+sz*0.03,y-sz*0.03);ctx.stroke();
  // Eyes behind glasses
  ctx.fillStyle="#2D3436";
  ctx.beginPath();ctx.arc(x-sz*0.1,y-sz*0.02,sz*0.03,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.1,y-sz*0.02,sz*0.03,0,Math.PI*2);ctx.fill();
  // Smile
  ctx.strokeStyle="#2D3436";ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(x,y+sz*0.1,sz*0.06,0,Math.PI);ctx.stroke();
  // Pointer stick
  ctx.strokeStyle="#FB923C";ctx.lineWidth=3;
  ctx.beginPath();ctx.moveTo(x+sz*0.24,y+sz*0.3);ctx.lineTo(x+sz*0.55,y);ctx.stroke();
  ctx.fillStyle="#FB923C";
  ctx.beginPath();ctx.arc(x+sz*0.55,y,sz*0.03,0,Math.PI*2);ctx.fill();
}}

function drawCharMiddleSchool(ctx,x,y,sz,emotion,gender){{
  let skinC="#FFEAA7",hairC=gender==="girl"?"#8B4513":"#1A1A2E";
  // Legs (taller)
  ctx.fillStyle="#2D3555";
  ctx.fillRect(x-sz*0.1,y+sz*0.7,sz*0.08,sz*0.3);
  ctx.fillRect(x+sz*0.02,y+sz*0.7,sz*0.08,sz*0.3);
  // Body (school uniform - slightly taller proportions)
  ctx.fillStyle="#06b6d4";
  ctx.beginPath();ctx.ellipse(x,y+sz*0.45,sz*0.2,sz*0.3,0,0,Math.PI*2);ctx.fill();
  // Collar
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.moveTo(x,y+sz*0.18);ctx.lineTo(x-sz*0.09,y+sz*0.3);ctx.lineTo(x+sz*0.09,y+sz*0.3);ctx.fill();
  // Tie
  ctx.fillStyle="#f43f5e";
  ctx.beginPath();ctx.moveTo(x,y+sz*0.22);ctx.lineTo(x-sz*0.03,y+sz*0.35);ctx.lineTo(x+sz*0.03,y+sz*0.35);ctx.fill();
  ctx.beginPath();ctx.moveTo(x-sz*0.04,y+sz*0.35);ctx.lineTo(x,y+sz*0.48);ctx.lineTo(x+sz*0.04,y+sz*0.35);ctx.fill();
  // Head
  ctx.fillStyle=skinC;
  ctx.beginPath();ctx.arc(x,y,sz*0.26,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=hairC;
  ctx.beginPath();ctx.arc(x,y-sz*0.08,sz*0.28,Math.PI,Math.PI*2);ctx.fill();
  if(gender==="girl"){{
    ctx.beginPath();ctx.arc(x-sz*0.26,y-sz*0.02,sz*0.06,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(x+sz*0.26,y-sz*0.02,sz*0.06,0,Math.PI*2);ctx.fill();
    // Hair clip
    ctx.fillStyle="#ec4899";
    ctx.beginPath();ctx.arc(x+sz*0.22,y-sz*0.18,sz*0.035,0,Math.PI*2);ctx.fill();
  }}
  // Eyes (anime style - larger, more detailed)
  let ey=y-sz*0.02;
  ctx.fillStyle="#2D3436";
  ctx.beginPath();ctx.ellipse(x-sz*0.09,ey,sz*0.035,sz*0.055,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(x+sz*0.09,ey,sz*0.035,sz*0.055,0,0,Math.PI*2);ctx.fill();
  // Eye highlights (double)
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.arc(x-sz*0.075,ey-sz*0.02,sz*0.015,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.105,ey-sz*0.02,sz*0.015,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x-sz*0.095,ey+sz*0.015,sz*0.008,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.085,ey+sz*0.015,sz*0.008,0,Math.PI*2);ctx.fill();
  // Mouth
  ctx.strokeStyle="#2D3436";ctx.lineWidth=1.5;
  ctx.beginPath();
  if(emotion==="happy")ctx.arc(x,y+sz*0.09,sz*0.05,0,Math.PI);
  else if(emotion==="thinking"){{ctx.moveTo(x-sz*0.03,y+sz*0.1);ctx.lineTo(x+sz*0.03,y+sz*0.1);}}
  else ctx.arc(x,y+sz*0.09,sz*0.035,0.1,Math.PI-0.1);
  ctx.stroke();
  // Cheeks
  ctx.fillStyle="rgba(244,114,182,0.25)";
  ctx.beginPath();ctx.arc(x-sz*0.16,y+sz*0.04,sz*0.035,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.16,y+sz*0.04,sz*0.035,0,Math.PI*2);ctx.fill();
  // Arms
  ctx.strokeStyle=skinC;ctx.lineWidth=sz*0.045;ctx.lineCap="round";
  ctx.beginPath();ctx.moveTo(x-sz*0.2,y+sz*0.35);ctx.lineTo(x-sz*0.35,y+sz*0.55);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x+sz*0.2,y+sz*0.35);ctx.lineTo(x+sz*0.35,y+sz*0.55);ctx.stroke();
  // School bag strap
  ctx.strokeStyle="#8b5cf6";ctx.lineWidth=sz*0.03;
  ctx.beginPath();ctx.moveTo(x-sz*0.12,y+sz*0.2);ctx.lineTo(x-sz*0.15,y+sz*0.55);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x+sz*0.12,y+sz*0.2);ctx.lineTo(x+sz*0.15,y+sz*0.55);ctx.stroke();
  // Bag on back
  ctx.fillStyle="#8b5cf6";
  ctx.beginPath();ctx.roundRect(x-sz*0.18,y+sz*0.4,sz*0.36,sz*0.22,4);ctx.fill();
  ctx.fillStyle="#6d28d9";
  ctx.fillRect(x-sz*0.08,y+sz*0.45,sz*0.16,sz*0.04);
}}

function drawCharHighSchool(ctx,x,y,sz,emotion,gender){{
  let skinC="#FFEAA7",hairC=gender==="girl"?"#6B3FA0":"#1A1A2E";
  // Legs (tallest)
  ctx.fillStyle="#2D3555";
  ctx.fillRect(x-sz*0.09,y+sz*0.75,sz*0.07,sz*0.35);
  ctx.fillRect(x+sz*0.02,y+sz*0.75,sz*0.07,sz*0.35);
  // Shoes
  ctx.fillStyle="#1A1A2E";
  ctx.fillRect(x-sz*0.11,y+sz*1.05,sz*0.12,sz*0.05);
  ctx.fillRect(x+sz*0.0,y+sz*1.05,sz*0.12,sz*0.05);
  // Body (blazer style)
  ctx.fillStyle="#1E293B";
  ctx.beginPath();ctx.ellipse(x,y+sz*0.48,sz*0.2,sz*0.32,0,0,Math.PI*2);ctx.fill();
  // Blazer lapels
  ctx.fillStyle="#334155";
  ctx.beginPath();ctx.moveTo(x-sz*0.08,y+sz*0.2);ctx.lineTo(x-sz*0.18,y+sz*0.4);ctx.lineTo(x-sz*0.04,y+sz*0.4);ctx.fill();
  ctx.beginPath();ctx.moveTo(x+sz*0.08,y+sz*0.2);ctx.lineTo(x+sz*0.18,y+sz*0.4);ctx.lineTo(x+sz*0.04,y+sz*0.4);ctx.fill();
  // Shirt collar
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.moveTo(x,y+sz*0.17);ctx.lineTo(x-sz*0.07,y+sz*0.28);ctx.lineTo(x+sz*0.07,y+sz*0.28);ctx.fill();
  // Head
  ctx.fillStyle=skinC;
  ctx.beginPath();ctx.arc(x,y,sz*0.24,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=hairC;
  ctx.beginPath();ctx.arc(x,y-sz*0.07,sz*0.26,Math.PI,Math.PI*2);ctx.fill();
  if(gender==="girl"){{
    // Longer hair sides
    ctx.fillRect(x-sz*0.26,y-sz*0.05,sz*0.06,sz*0.25);
    ctx.fillRect(x+sz*0.2,y-sz*0.05,sz*0.06,sz*0.25);
  }}
  // Eyes (most detailed anime)
  let ey=y-sz*0.02;
  // Eye outlines
  ctx.strokeStyle="#2D3436";ctx.lineWidth=1;
  ctx.beginPath();ctx.ellipse(x-sz*0.08,ey,sz*0.04,sz*0.05,0,0,Math.PI*2);ctx.stroke();
  ctx.beginPath();ctx.ellipse(x+sz*0.08,ey,sz*0.04,sz*0.05,0,0,Math.PI*2);ctx.stroke();
  // Iris
  ctx.fillStyle="#4A90D9";
  ctx.beginPath();ctx.ellipse(x-sz*0.08,ey,sz*0.032,sz*0.045,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(x+sz*0.08,ey,sz*0.032,sz*0.045,0,0,Math.PI*2);ctx.fill();
  // Pupil
  ctx.fillStyle="#2D3436";
  ctx.beginPath();ctx.arc(x-sz*0.08,ey,sz*0.018,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.08,ey,sz*0.018,0,Math.PI*2);ctx.fill();
  // Highlights
  ctx.fillStyle="#FFF";
  ctx.beginPath();ctx.arc(x-sz*0.065,ey-sz*0.018,sz*0.012,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.095,ey-sz*0.018,sz*0.012,0,Math.PI*2);ctx.fill();
  // Mouth
  ctx.strokeStyle="#2D3436";ctx.lineWidth=1.5;
  ctx.beginPath();
  if(emotion==="happy")ctx.arc(x,y+sz*0.08,sz*0.04,0,Math.PI);
  else if(emotion==="thinking"){{ctx.moveTo(x-sz*0.02,y+sz*0.09);ctx.lineTo(x+sz*0.04,y+sz*0.085);}}
  else ctx.arc(x,y+sz*0.08,sz*0.03,0.1,Math.PI-0.1);
  ctx.stroke();
  // Cheeks
  ctx.fillStyle="rgba(244,114,182,0.2)";
  ctx.beginPath();ctx.arc(x-sz*0.14,y+sz*0.03,sz*0.03,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(x+sz*0.14,y+sz*0.03,sz*0.03,0,Math.PI*2);ctx.fill();
  // Arms
  ctx.strokeStyle=skinC;ctx.lineWidth=sz*0.04;ctx.lineCap="round";
  ctx.beginPath();ctx.moveTo(x-sz*0.2,y+sz*0.32);ctx.lineTo(x-sz*0.35,y+sz*0.55);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x+sz*0.2,y+sz*0.32);ctx.lineTo(x+sz*0.32,y+sz*0.5);ctx.stroke();
  // Book in hand
  ctx.fillStyle="#3b82f6";
  ctx.save();ctx.translate(x+sz*0.32,y+sz*0.5);ctx.rotate(-0.3);
  ctx.fillRect(-sz*0.06,-sz*0.08,sz*0.12,sz*0.16);
  ctx.fillStyle="#FFF";ctx.fillRect(-sz*0.04,-sz*0.06,sz*0.08,sz*0.02);
  ctx.restore();
  // Graduation cap (for grade 12 or subtle for all high school)
  ctx.fillStyle="#1A1A2E";
  ctx.beginPath();ctx.moveTo(x-sz*0.22,y-sz*0.22);ctx.lineTo(x+sz*0.22,y-sz*0.22);
  ctx.lineTo(x+sz*0.18,y-sz*0.28);ctx.lineTo(x-sz*0.18,y-sz*0.28);ctx.fill();
  // Cap top
  ctx.beginPath();ctx.moveTo(x-sz*0.28,y-sz*0.28);ctx.lineTo(x+sz*0.28,y-sz*0.28);
  ctx.lineTo(x+sz*0.2,y-sz*0.32);ctx.lineTo(x-sz*0.2,y-sz*0.32);ctx.fill();
  // Tassel
  ctx.strokeStyle="#f59e0b";ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(x+sz*0.2,y-sz*0.3);ctx.lineTo(x+sz*0.28,y-sz*0.18);ctx.stroke();
  ctx.fillStyle="#f59e0b";
  ctx.beginPath();ctx.arc(x+sz*0.28,y-sz*0.18,sz*0.02,0,Math.PI*2);ctx.fill();
}}

function drawCharForPage(container,type,unit){{
  let sz=GRADE===0?90:(GRADE<=2?80:(GRADE<=4?70:(GRADE<=8?75:70)));
  let cW=sz*2.5,cH=GRADE>=5?sz*2.6:sz*2.2;
  let c=createCanvas(cW,cH);
  container.prepend(c);
  let ctx=c.getContext("2d");
  let cx=cW/2,cy=cH*0.38;
  let emotions=["happy","excited","thinking","surprised"];
  let em=emotions[(unit||0)%emotions.length];
  if(type==="grammar"||type==="culture"){{drawCharTeacher(ctx,cx,cy,sz);}}
  else if(GRADE===0){{drawCharPreschool(ctx,cx,cy,sz,em);}}
  else if(GRADE<=4){{let g=(unit||0)%2===0?"boy":"girl";drawCharElementary(ctx,cx,cy,sz,em,g);}}
  else if(GRADE<=8){{let g=(unit||0)%2===0?"boy":"girl";drawCharMiddleSchool(ctx,cx,cy,sz,em,g);}}
  else{{let g=(unit||0)%2===0?"boy":"girl";drawCharHighSchool(ctx,cx,cy,sz,em,g);}}
}}

// ── Page renderers ──
function renderCover(p){{
  let d=document.createElement("div");d.className="cover-page";
  let cH=GRADE>=5?220:200;
  let c=createCanvas(220,cH);d.appendChild(c);
  let ctx=c.getContext("2d");
  if(GRADE===0)drawCharPreschool(ctx,110,70,80,"excited");
  else if(GRADE<=4)drawCharElementary(ctx,110,70,80,"happy","girl");
  else if(GRADE<=8)drawCharMiddleSchool(ctx,110,70,80,"happy","girl");
  else drawCharHighSchool(ctx,110,70,80,"happy","girl");
  d.innerHTML+=`<div class="big-title">${{esc(p.title)}}</div>
    <div class="grade-badge">${{esc(GRADE===0?"Preschool":"Grade "+GRADE)}}</div>
    <div class="sub-title" style="margin-top:18px">Interactive English Coursebook</div>`;
  return d;
}}

function renderUnitOpener(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">Unit ${{p.unit}}</div><div class="sub-title">${{esc(p.title)}}</div>`;
  drawCharForPage(d,"unit_opener",p.unit);
  if(MODE==="teacher")d.innerHTML+=`<div class="teacher-note">Ogretmen Notu: Bu unite ${{p.title}} temasini kapsar.</div>`;
  return d;
}}

function renderVocabulary(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">📝 Vocabulary - Unit ${{p.unit}}</div>`;
  let grid=document.createElement("div");grid.className="vocab-grid";
  (p.words||[]).forEach(w=>{{
    let card=document.createElement("div");card.className="vocab-card";
    card.innerHTML=`<div class="icon">${{wordIcon(w)}}</div><div class="word">${{esc(w)}}</div><div class="speaker">🔊</div>`;
    card.onclick=()=>speak(w);
    grid.appendChild(card);
  }});
  d.appendChild(grid);
  drawCharForPage(d,"vocabulary",p.unit);
  return d;
}}

function renderStory(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">📖 Story Time - Unit ${{p.unit}}</div>`;
  drawCharForPage(d,"story",p.unit);
  let words=p.words||[];
  let title=p.title||"Adventure";
  // Auto-generate simple story lines using theme words
  let lines=buildStoryLines(title,words);
  let genders=["girl","boy"];
  lines.forEach((line,i)=>{{
    let bubble=document.createElement("div");bubble.className="speech-bubble";
    let name=i%2===0?"Mia":"Tom";
    bubble.innerHTML=`<strong style="color:${{ACCENT}}">${{name}}:</strong> ${{esc(line)}}`;
    bubble.style.cursor="pointer";
    bubble.onclick=()=>speak(line);
    d.appendChild(bubble);
  }});
  return d;
}}

function buildStoryLines(theme,words){{
  let t=theme.toLowerCase();
  let w=words.length>0?words:["hello","friend"];
  let templates=[
    `Hello! Today we learn about ${{t}}.`,
    `Look! I can see a ${{w[0]||"thing"}}!`,
    `Wow, that is so cool! Do you like ${{w[1]||w[0]||"it"}}?`,
    `Yes! ${{w[0]||"It"}} is my favorite!`,
    `Let's practice together! Ready?`,
  ];
  if(GRADE>=5){{
    templates.push(`I've been studying ${{t}} for a while now.`);
    templates.push(`Can you explain more about ${{w[2]||w[0]||"this topic"}}?`);
    templates.push(`Sure! Let me share what I know about ${{t}}.`);
  }}
  if(GRADE>=9){{
    templates.push(`This connects to what we discussed about ${{w[3]||w[1]||"the concept"}}.`);
    templates.push(`That's a great analysis! Let's explore further.`);
  }}
  if(GRADE===0)return templates.slice(0,3);
  if(GRADE<=2)return templates.slice(0,4);
  if(GRADE<=4)return templates.slice(0,5);
  if(GRADE<=8)return templates.slice(0,8);
  return templates;
}}

function renderSong(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">🎵 Song Time - Unit ${{p.unit}}</div>`;
  drawCharForPage(d,"song",p.unit);
  let theme=p.theme||"Fun";
  let lines=buildSongLines(theme);
  lines.forEach(line=>{{
    let div=document.createElement("div");div.className="song-line";
    div.innerHTML=`<span class="note">♫</span>${{esc(line)}}`;
    div.style.cursor="pointer";div.onclick=()=>speak(line);
    d.appendChild(div);
  }});
  let btn=document.createElement("button");
  btn.className="nav-btn";btn.style.marginTop="16px";
  btn.textContent="🔊 Sarkiyi Dinle";
  btn.onclick=()=>{{lines.forEach((l,i)=>setTimeout(()=>speak(l),i*2500));}};
  d.appendChild(btn);
  return d;
}}

function buildSongLines(theme){{
  let t=theme.toLowerCase();
  return [
    `${{theme}}, ${{theme}}, let's have fun!`,
    `Learning English, everyone!`,
    `Clap your hands and sing along,`,
    `${{theme}} makes us strong!`,
    `La la la, we love to learn,`,
    `Now it's your turn!`,
  ];
}}

function renderGrammar(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">📐 Grammar - Unit ${{p.unit}}</div>`;
  drawCharForPage(d,"grammar",p.unit);
  let rule=p.rule||"Simple Present Tense";
  let box=document.createElement("div");box.className="grammar-box";
  box.innerHTML=`<h3>📌 Rule: ${{esc(rule)}}</h3>
    <p style="margin:8px 0;color:#CBD5E1;">Study the pattern and examples below:</p>
    <div style="background:#131825;border-radius:8px;padding:12px;margin-top:8px;">
      <p style="color:${{ACCENT}};font-weight:600;">Example:</p>
      <p>"I <strong>like</strong> apples." ✓</p>
      <p>"She <strong>likes</strong> apples." ✓</p>
    </div>`;
  d.appendChild(box);
  if(MODE==="teacher")d.innerHTML+=`<div class="teacher-note">Bu gramer konusunu somut orneklerle pekistirin.</div>`;
  return d;
}}

function renderActivity(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">🎮 Activity - Unit ${{p.unit}}</div>`;
  let area=document.createElement("div");area.className="activity-area";
  let words=p.words||[];
  if(words.length>=2){{
    area.innerHTML=`<p style="margin-bottom:12px;font-weight:600;">Fill in the blanks with the correct word:</p>`;
    let shuffled=[...words].sort(()=>Math.random()-0.5).slice(0,Math.min(4,words.length));
    shuffled.forEach((w,i)=>{{
      let sent=document.createElement("p");sent.style.margin="10px 0";
      let blank=document.createElement("span");blank.className="fill-blank";
      blank.textContent="???";blank.dataset.answer=w;
      blank.onclick=function(){{this.textContent=this.dataset.answer;this.style.color="#4ade80";}};
      sent.appendChild(document.createTextNode(`${{i+1}}. I like `));
      sent.appendChild(blank);
      sent.appendChild(document.createTextNode(`. ${{wordIcon(w)}}`));
      area.appendChild(sent);
    }});
    // Word bank
    let bank=document.createElement("div");
    bank.style.cssText="margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;";
    [...shuffled].sort(()=>Math.random()-0.5).forEach(w=>{{
      let chip=document.createElement("span");
      chip.style.cssText=`background:${{ACCENT}}22;border:1px solid ${{ACCENT}};border-radius:8px;padding:4px 12px;cursor:pointer;`;
      chip.textContent=w;chip.onclick=()=>speak(w);
      bank.appendChild(chip);
    }});
    area.appendChild(bank);
  }} else {{
    area.innerHTML=`<p>Practice the words you learned in this unit!</p>`;
  }}
  d.appendChild(area);
  drawCharForPage(d,"activity",p.unit);
  return d;
}}

function renderReview(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">✅ Review - Unit ${{p.unit}}</div>
    <div class="sub-title">How well did you learn?</div>`;
  let skills=p.skills||{{}};
  let items=Object.keys(skills).length>0?Object.entries(skills):
    [["Listening","I can understand new words"],["Speaking","I can say the words"],
     ["Reading","I can read the words"],["Writing","I can write the words"]];
  items.forEach(([k,v])=>{{
    let row=document.createElement("div");row.className="review-item";
    let stars="";for(let i=0;i<3;i++){{
      stars+=`<span class="star-btn" onclick="this.textContent=this.textContent==='⭐'?'☆':'⭐'">☆</span>`;
    }}
    row.innerHTML=`<div style="flex:1"><strong style="color:${{ACCENT}}">${{esc(String(k))}}</strong><br>
      <span style="color:#94A3B8;font-size:${{FONT_SZ-1}}px">${{esc(String(v))}}</span></div><div>${{stars}}</div>`;
    d.appendChild(row);
  }});
  drawCharForPage(d,"review",p.unit);
  return d;
}}

function renderDialogue(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">💬 Dialogue - Unit ${{p.unit}}</div>
    <div class="sub-title">${{esc(p.title||"Conversation Practice")}}</div>`;
  let container=document.createElement("div");container.className="dialogue-container";
  let words=p.words||[];
  let topic=(p.title||"topic").toLowerCase();
  let dialogueLines=[
    {{name:"Alex",text:`Hi! Have you heard about ${{topic}}?`,side:"left"}},
    {{name:"Sam",text:`Yes! I find ${{topic}} really interesting.`,side:"right"}},
    {{name:"Alex",text:`Do you know the word "${{words[0]||"vocabulary"}}"?`,side:"left"}},
    {{name:"Sam",text:`Of course! It means... can you help me remember?`,side:"right"}},
    {{name:"Alex",text:`Sure! Let me explain. It is related to ${{words[1]||words[0]||"our lesson"}}.`,side:"left"}},
    {{name:"Sam",text:`That makes sense! What about "${{words[2]||words[0]||"this one"}}"?`,side:"right"}},
    {{name:"Alex",text:`Great question! Let's practice using it in a sentence.`,side:"left"}},
    {{name:"Sam",text:`OK! "${{words[3]||words[0]||"Learning"}} is fun when we work together!"`,side:"right"}},
  ];
  dialogueLines.forEach(line=>{{
    let row=document.createElement("div");
    row.className="dialogue-line"+(line.side==="right"?" right":"");
    let bubble=document.createElement("div");bubble.className="dlg-bubble";
    bubble.innerHTML=`<div class="dlg-name" style="color:${{line.side==="left"?ACCENT:"#a78bfa"}}">${{line.name}}</div>
      <div>${{esc(line.text)}}</div>`;
    bubble.onclick=()=>speak(line.text);
    row.appendChild(bubble);
    container.appendChild(row);
  }});
  d.appendChild(container);
  // TTS button for full dialogue
  let btn=document.createElement("button");btn.className="nav-btn";btn.style.marginTop="12px";
  btn.textContent="🔊 Play Full Dialogue";
  btn.onclick=()=>{{dialogueLines.forEach((l,i)=>setTimeout(()=>speak(l.text),i*3000));}};
  d.appendChild(btn);
  drawCharForPage(d,"dialogue",p.unit);
  return d;
}}

function renderWriting(p){{
  let d=document.createElement("div");
  d.innerHTML=`<div class="page-title">✍️ Writing Model - Unit ${{p.unit}}</div>`;
  let section=document.createElement("div");section.className="writing-section";
  let topic=(p.title||"My Experience").toLowerCase();
  // Model text
  section.innerHTML+=`<h3 style="color:${{ACCENT}};margin-bottom:10px;">📄 Model Text</h3>`;
  let model=document.createElement("div");model.className="writing-model";
  let modelText=`<p>Last week, I had an interesting experience with <span class="key-phrase">${{topic}}</span>. `+
    `It made me think about how important it is to <span class="key-phrase">practice regularly</span>. `+
    `<span class="key-phrase">First</span>, I started by reading about the topic. `+
    `<span class="key-phrase">Then</span>, I discussed it with my classmates. `+
    `<span class="key-phrase">Finally</span>, I wrote my own thoughts about it. `+
    `I believe that learning about <span class="key-phrase">${{topic}}</span> will help me in the future.</p>`;
  model.innerHTML=modelText;
  section.appendChild(model);
  // Key phrases
  section.innerHTML+=`<h3 style="color:${{ACCENT}};margin:14px 0 8px;">🔑 Key Phrases</h3>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
      <span class="key-phrase">First / Then / Finally</span>
      <span class="key-phrase">I believe that...</span>
      <span class="key-phrase">It made me think...</span>
      <span class="key-phrase">In my opinion...</span>
    </div>`;
  // Writing prompt
  let prompt=document.createElement("div");prompt.className="writing-prompt";
  prompt.innerHTML=`<h3 style="color:${{ACCENT}};margin-bottom:8px;">📝 Your Turn!</h3>
    <p>Write a short paragraph (5-7 sentences) about <strong>${{esc(p.title||"the topic")}}</strong>.</p>
    <p style="color:#94A3B8;margin-top:6px;">Use the key phrases above. Include your personal opinion.</p>`;
  section.appendChild(prompt);
  d.appendChild(section);
  if(MODE==="teacher")d.innerHTML+=`<div class="teacher-note">Ogrencilerin model metni incelemesini ve anahtar ifadeleri kendi yazilarinda kullanmasini saglayin.</div>`;
  return d;
}}

function renderBackCover(){{
  let d=document.createElement("div");d.className="cover-page";
  let c=createCanvas(220,200);d.appendChild(c);
  let ctx=c.getContext("2d");
  if(GRADE===0)drawCharPreschool(ctx,110,70,80,"happy");
  else if(GRADE<=4){{drawCharElementary(ctx,70,70,60,"happy","girl");drawCharElementary(ctx,150,70,60,"happy","boy");}}
  else if(GRADE<=8){{drawCharMiddleSchool(ctx,70,70,60,"happy","girl");drawCharMiddleSchool(ctx,150,70,60,"happy","boy");}}
  else{{drawCharHighSchool(ctx,70,70,60,"happy","girl");drawCharHighSchool(ctx,150,70,60,"happy","boy");}}
  d.innerHTML+=`<div class="big-title">Great Job! 🎉</div>
    <div class="sub-title">You finished the book!</div>
    <div style="margin-top:12px;font-size:${{FONT_SZ}}px;color:#94A3B8;">Keep practicing every day!</div>`;
  return d;
}}

function esc(s){{return s?String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"):""}}

// ── Render + Navigate ──
const RENDERERS={{
  cover:renderCover, unit_opener:renderUnitOpener, vocabulary:renderVocabulary,
  story:renderStory, song:renderSong, grammar:renderGrammar,
  dialogue:renderDialogue, writing:renderWriting,
  activity:renderActivity, review:renderReview, back_cover:renderBackCover,
}};

function renderPage(idx){{
  let p=PAGES[idx];
  let fn=RENDERERS[p.type];
  pageEl.innerHTML="";
  if(fn){{let el=fn(p);pageEl.appendChild(el);}}
  else{{pageEl.innerHTML=`<div class="page-title">${{esc(p.type)}}</div>`;}}
  indEl.textContent=`${{idx+1}} / ${{PAGES.length}}`;
  btnP.disabled=idx===0;btnN.disabled=idx===PAGES.length-1;
}}

window.navigate=function(dir){{
  if(animating)return;
  let next=curPage+dir;
  if(next<0||next>=PAGES.length)return;
  animating=true;
  pageEl.classList.add(dir>0?"flip-out":"flip-in");
  setTimeout(()=>{{
    curPage=next;renderPage(curPage);
    pageEl.classList.remove("flip-out","flip-in");
    pageEl.classList.add(dir>0?"flip-in":"flip-out");
    requestAnimationFrame(()=>{{
      pageEl.classList.remove("flip-in","flip-out");
      pageEl.classList.add("active");
      animating=false;
    }});
  }},300);
}};

// Keyboard navigation
document.addEventListener("keydown",function(e){{
  if(e.key==="ArrowRight"||e.key==="ArrowDown")window.navigate(1);
  if(e.key==="ArrowLeft"||e.key==="ArrowUp")window.navigate(-1);
}});

renderPage(0);
}})();
</script>
</body>
</html>"""
    return html


# ══════════════════════════════════════════════════════════════════════════════
# PDF Export — Ultra Premium Coursebook
# ══════════════════════════════════════════════════════════════════════════════

def build_anime_coursebook_pdf(grade: int, curriculum_weeks: list) -> bytes | None:
    """Build ultra-premium coursebook PDF that looks like a professionally published textbook.

    Uses BaseDocTemplate with custom PageTemplate for consistent headers/footers,
    canvas-drawn decorative elements, and grade-specific color theming.

    Args:
        grade: 0=preschool, 1-4=elementary, 5-8=middle, 9-12=high
        curriculum_weeks: List of week dicts from curriculum_*.py

    Returns:
        PDF bytes or None on failure.
    """
    try:
        import io
        import math
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm, cm
        from reportlab.lib.colors import HexColor, white, black, Color
        from reportlab.platypus import (
            BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
            Table, TableStyle, PageBreak, KeepTogether, Flowable,
            NextPageTemplate,
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String
        from reportlab.graphics import renderPDF
        from utils.shared_data import ensure_turkish_pdf_fonts
    except ImportError:
        return None

    font_name, font_bold = ensure_turkish_pdf_fonts()

    grade = max(0, min(12, grade))
    PAGE_W, PAGE_H = A4  # 595.27, 841.89

    # ─── Grade Theme System ───
    GRADE_THEMES = {
        0: {"primary": "#EC4899", "secondary": "#F9A8D4", "bg": "#FDF2F8", "dark": "#831843", "name": "Early Steps"},
        1: {"primary": "#0EA5E9", "secondary": "#7DD3FC", "bg": "#F0F9FF", "dark": "#0C4A6E", "name": "Bright Start 1"},
        2: {"primary": "#22C55E", "secondary": "#86EFAC", "bg": "#F0FDF4", "dark": "#14532D", "name": "Bright Start 2"},
        3: {"primary": "#8B5CF6", "secondary": "#C4B5FD", "bg": "#F5F3FF", "dark": "#4C1D95", "name": "Bright Start 3"},
        4: {"primary": "#F97316", "secondary": "#FDBA74", "bg": "#FFF7ED", "dark": "#7C2D12", "name": "Bright Start 4"},
        5: {"primary": "#06B6D4", "secondary": "#67E8F9", "bg": "#ECFEFF", "dark": "#164E63", "name": "Next Level 5"},
        6: {"primary": "#8B5CF6", "secondary": "#C4B5FD", "bg": "#F5F3FF", "dark": "#4C1D95", "name": "Next Level 6"},
        7: {"primary": "#EC4899", "secondary": "#F9A8D4", "bg": "#FDF2F8", "dark": "#831843", "name": "Next Level 7"},
        8: {"primary": "#14B8A6", "secondary": "#5EEAD4", "bg": "#F0FDFA", "dark": "#134E4A", "name": "Next Level 8"},
        9: {"primary": "#F43F5E", "secondary": "#FDA4AF", "bg": "#FFF1F2", "dark": "#881337", "name": "English Core 9"},
        10: {"primary": "#3B82F6", "secondary": "#93C5FD", "bg": "#EFF6FF", "dark": "#1E3A8A", "name": "English Core 10"},
        11: {"primary": "#10B981", "secondary": "#6EE7B7", "bg": "#ECFDF5", "dark": "#064E3B", "name": "English Core 11"},
        12: {"primary": "#F59E0B", "secondary": "#FCD34D", "bg": "#FFFBEB", "dark": "#78350F", "name": "English Core 12"},
    }

    theme = GRADE_THEMES[grade]
    C_PRIMARY = HexColor(theme["primary"])
    C_SECONDARY = HexColor(theme["secondary"])
    C_BG = HexColor(theme["bg"])
    C_DARK = HexColor(theme["dark"])
    book_title = theme["name"]

    GRADE_LABELS = {
        0: "Preschool", 1: "Grade 1", 2: "Grade 2", 3: "Grade 3", 4: "Grade 4",
        5: "Grade 5", 6: "Grade 6", 7: "Grade 7", 8: "Grade 8",
        9: "Grade 9", 10: "Grade 10", 11: "Grade 11", 12: "Grade 12",
    }
    label = GRADE_LABELS[grade]

    # Grade-appropriate font sizes (bigger for younger)
    BASE_FONT = {
        0: 18, 1: 16, 2: 15, 3: 14, 4: 13,
        5: 12, 6: 12, 7: 11, 8: 11,
        9: 11, 10: 11, 11: 10, 12: 10,
    }
    font_sz = BASE_FONT[grade]

    # ─── Build unit structure ───
    if not curriculum_weeks:
        curriculum_weeks = [{"theme": f"Week {i+1}", "vocab": [], "skills": {}, "structure": ""} for i in range(36)]

    weeks_per_unit = max(1, len(curriculum_weeks) // 10) if len(curriculum_weeks) >= 10 else max(1, len(curriculum_weeks))
    units = []
    for i in range(0, len(curriculum_weeks), weeks_per_unit):
        uw = curriculum_weeks[i:i + weeks_per_unit]
        units.append({
            "num": len(units) + 1,
            "title": uw[0].get("theme", f"Unit {len(units) + 1}"),
            "weeks": uw,
        })

    # ─── Margin / layout constants ───
    MARGIN_LEFT = 22 * mm
    MARGIN_RIGHT = 22 * mm
    MARGIN_TOP = 28 * mm  # space for header
    MARGIN_BOTTOM = 22 * mm  # space for footer
    CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT

    # ─── Helper: hex to reportlab Color ───
    def _hex_alpha(hex_str, alpha):
        """Return a Color from hex string with alpha transparency."""
        c = HexColor(hex_str)
        return Color(c.red, c.green, c.blue, alpha)

    # ─── Canvas drawing helpers ───
    def _draw_rounded_rect(canvas, x, y, w, h, r, fill_color=None, stroke_color=None, stroke_width=1):
        """Draw a rounded rectangle on the canvas."""
        canvas.saveState()
        p = canvas.beginPath()
        p.roundRect(x, y, w, h, r)
        if fill_color:
            canvas.setFillColor(fill_color)
        if stroke_color:
            canvas.setStrokeColor(stroke_color)
            canvas.setLineWidth(stroke_width)
        else:
            canvas.setStrokeColor(fill_color if fill_color else white)
            canvas.setLineWidth(0)
        if fill_color:
            canvas.drawPath(p, fill=1, stroke=1 if stroke_color else 0)
        else:
            canvas.drawPath(p, fill=0, stroke=1)
        canvas.restoreState()

    def _draw_diamond(canvas, cx, cy, size, color):
        """Draw a small diamond shape."""
        canvas.saveState()
        canvas.setFillColor(color)
        p = canvas.beginPath()
        p.moveTo(cx, cy + size)
        p.lineTo(cx + size, cy)
        p.lineTo(cx, cy - size)
        p.lineTo(cx - size, cy)
        p.close()
        canvas.drawPath(p, fill=1, stroke=0)
        canvas.restoreState()

    def _draw_star(canvas, cx, cy, outer_r, inner_r, color, points=5):
        """Draw a star shape."""
        canvas.saveState()
        canvas.setFillColor(color)
        p = canvas.beginPath()
        for i in range(points * 2):
            angle = math.pi / 2 + i * math.pi / points
            r = outer_r if i % 2 == 0 else inner_r
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                p.moveTo(x, y)
            else:
                p.lineTo(x, y)
        p.close()
        canvas.drawPath(p, fill=1, stroke=0)
        canvas.restoreState()

    def _draw_circle(canvas, cx, cy, r, color):
        """Draw a filled circle."""
        canvas.saveState()
        canvas.setFillColor(color)
        canvas.circle(cx, cy, r, fill=1, stroke=0)
        canvas.restoreState()

    # ─── Page metadata tracker ───
    # We use a mutable dict so the canvasmaker callbacks can read/write it
    _page_meta = {"page_type": "content", "current_page": 0, "total_units": len(units)}

    # ─── Page template callbacks ───
    def _header_footer(canvas, doc):
        """Draw header and footer on content pages."""
        canvas.saveState()
        page_num = canvas.getPageNumber()

        # --- HEADER ---
        # Thin accent strip at very top
        canvas.setFillColor(C_PRIMARY)
        canvas.rect(0, PAGE_H - 4 * mm, PAGE_W, 4 * mm, fill=1, stroke=0)

        # Secondary thin line below
        canvas.setFillColor(C_SECONDARY)
        canvas.rect(0, PAGE_H - 5.5 * mm, PAGE_W, 1.5 * mm, fill=1, stroke=0)

        # Book title left
        canvas.setFont(font_bold, 8)
        canvas.setFillColor(C_DARK)
        canvas.drawString(MARGIN_LEFT, PAGE_H - 14 * mm, book_title)

        # Grade badge right
        badge_text = label
        badge_w = canvas.stringWidth(badge_text, font_bold, 8) + 16
        badge_x = PAGE_W - MARGIN_RIGHT - badge_w
        badge_y = PAGE_H - 16.5 * mm
        _draw_rounded_rect(canvas, badge_x, badge_y, badge_w, 12, 3, fill_color=C_PRIMARY)
        canvas.setFont(font_bold, 7)
        canvas.setFillColor(white)
        canvas.drawString(badge_x + 8, badge_y + 3, badge_text)

        # Subtle separator line
        canvas.setStrokeColor(_hex_alpha(theme["primary"], 0.2))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_LEFT, PAGE_H - 20 * mm, PAGE_W - MARGIN_RIGHT, PAGE_H - 20 * mm)

        # --- FOOTER ---
        # Accent line
        canvas.setStrokeColor(C_PRIMARY)
        canvas.setLineWidth(1)
        canvas.line(MARGIN_LEFT, MARGIN_BOTTOM - 6 * mm, PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 6 * mm)

        # Secondary thin line
        canvas.setStrokeColor(C_SECONDARY)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN_LEFT, MARGIN_BOTTOM - 7.5 * mm, PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 7.5 * mm)

        # Page number centered
        canvas.setFont(font_bold, 9)
        canvas.setFillColor(C_PRIMARY)
        page_str = str(page_num)
        pw = canvas.stringWidth(page_str, font_bold, 9)
        canvas.drawString(PAGE_W / 2 - pw / 2, MARGIN_BOTTOM - 14 * mm, page_str)

        # Small decorative diamonds around page number
        _draw_diamond(canvas, PAGE_W / 2 - pw / 2 - 8, MARGIN_BOTTOM - 11.5 * mm, 2, C_SECONDARY)
        _draw_diamond(canvas, PAGE_W / 2 + pw / 2 + 8, MARGIN_BOTTOM - 11.5 * mm, 2, C_SECONDARY)

        # "SmartCampusAI" right
        canvas.setFont(font_name, 7)
        canvas.setFillColor(_hex_alpha("#94A3B8", 1.0))
        canvas.drawRightString(PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 14 * mm, "SmartCampusAI")

        canvas.restoreState()

    def _cover_page_bg(canvas, doc):
        """Draw cover page background (no header/footer)."""
        # Handled entirely by CoverFlowable
        pass

    def _blank_page_bg(canvas, doc):
        """No decoration (for unit openers, back cover)."""
        pass

    # ─── Paragraph Styles ───
    styles = getSampleStyleSheet()

    s_cover_title = ParagraphStyle(
        "CoverTitle", parent=styles["Title"],
        fontName=font_bold, fontSize=40, textColor=white,
        alignment=TA_CENTER, leading=48, spaceAfter=8,
    )
    s_cover_subtitle = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontName=font_name, fontSize=16, textColor=white,
        alignment=TA_CENTER, leading=22, spaceAfter=6,
    )
    s_cover_year = ParagraphStyle(
        "CoverYear", parent=styles["Normal"],
        fontName=font_bold, fontSize=18, textColor=white,
        alignment=TA_CENTER, leading=24, spaceAfter=6,
    )
    s_cover_institution = ParagraphStyle(
        "CoverInstitution", parent=styles["Normal"],
        fontName=font_name, fontSize=11, textColor=HexColor("#94A3B8"),
        alignment=TA_CENTER, leading=16,
    )
    s_page_title = ParagraphStyle(
        "PageTitle", parent=styles["Heading1"],
        fontName=font_bold, fontSize=font_sz + 10, textColor=C_DARK,
        alignment=TA_LEFT, spaceAfter=6, spaceBefore=4,
    )
    s_page_title_center = ParagraphStyle(
        "PageTitleCenter", parent=s_page_title,
        alignment=TA_CENTER,
    )
    s_section_header = ParagraphStyle(
        "SectionHeader", parent=styles["Heading2"],
        fontName=font_bold, fontSize=font_sz + 4, textColor=C_PRIMARY,
        alignment=TA_LEFT, spaceAfter=6, spaceBefore=8,
    )
    s_body = ParagraphStyle(
        "PremiumBody", parent=styles["Normal"],
        fontName=font_name, fontSize=font_sz, textColor=HexColor("#1E293B"),
        leading=font_sz + 7, spaceAfter=4,
    )
    s_body_center = ParagraphStyle(
        "PremiumBodyCenter", parent=s_body, alignment=TA_CENTER,
    )
    s_body_italic = ParagraphStyle(
        "PremiumBodyItalic", parent=s_body,
        fontName=font_name, textColor=HexColor("#475569"),
    )
    s_vocab_word = ParagraphStyle(
        "PremiumVocab", parent=styles["Normal"],
        fontName=font_bold, fontSize=font_sz + 1, textColor=C_DARK,
        alignment=TA_LEFT, leading=font_sz + 8,
    )
    s_song_line = ParagraphStyle(
        "PremiumSong", parent=styles["Normal"],
        fontName=font_name, fontSize=font_sz + 1, textColor=HexColor("#1E293B"),
        leading=font_sz + 10, spaceAfter=3, alignment=TA_CENTER,
    )
    s_grammar_rule = ParagraphStyle(
        "PremiumGrammar", parent=styles["Normal"],
        fontName=font_bold, fontSize=font_sz + 2, textColor=HexColor("#1E293B"),
        leading=font_sz + 8, spaceAfter=6,
    )
    s_dialogue = ParagraphStyle(
        "PremiumDialogue", parent=styles["Normal"],
        fontName=font_name, fontSize=font_sz, textColor=HexColor("#1E293B"),
        leading=font_sz + 7, spaceAfter=4,
    )
    s_checklist = ParagraphStyle(
        "PremiumChecklist", parent=styles["Normal"],
        fontName=font_name, fontSize=font_sz, textColor=HexColor("#1E293B"),
        leading=font_sz + 9, spaceAfter=5, leftIndent=6,
    )
    s_instruction = ParagraphStyle(
        "PremiumInstruction", parent=styles["Normal"],
        fontName=font_name, fontSize=font_sz - 1, textColor=HexColor("#64748B"),
        leading=font_sz + 5, spaceAfter=4, alignment=TA_CENTER,
    )
    s_unit_num = ParagraphStyle(
        "UnitNum", parent=styles["Title"],
        fontName=font_bold, fontSize=48, textColor=white,
        alignment=TA_CENTER, leading=56,
    )
    s_unit_title = ParagraphStyle(
        "UnitTitle", parent=styles["Title"],
        fontName=font_bold, fontSize=28, textColor=C_DARK,
        alignment=TA_CENTER, leading=34, spaceAfter=8,
    )
    s_unit_weeks = ParagraphStyle(
        "UnitWeeks", parent=styles["Normal"],
        fontName=font_name, fontSize=12, textColor=HexColor("#64748B"),
        alignment=TA_CENTER, leading=16, spaceAfter=6,
    )
    s_skill_label = ParagraphStyle(
        "SkillLabel", parent=styles["Normal"],
        fontName=font_bold, fontSize=10, textColor=C_DARK,
        alignment=TA_CENTER, leading=14,
    )

    # ─── Custom Flowables ───
    class CoverFlowable(Flowable):
        """Full-page cover with gradient block, title, and decorative elements."""
        def __init__(self, width, height):
            Flowable.__init__(self)
            self.width = width
            self.height = height

        def wrap(self, availWidth, availHeight):
            return (self.width, self.height)

        def draw(self):
            c = self.canv
            w = self.width
            h = self.height
            # We draw relative to (0,0) at bottom-left of the flowable space

            # ── Top colored block (60% of page) ──
            block_h = h * 0.60
            block_y = h - block_h

            # Main gradient block
            c.saveState()
            c.setFillColor(C_PRIMARY)
            c.rect(0, block_y, w, block_h, fill=1, stroke=0)

            # Secondary overlay stripe for depth
            c.setFillColor(_hex_alpha(theme["dark"], 0.3))
            c.rect(0, block_y, w, block_h * 0.12, fill=1, stroke=0)

            # Decorative circles (subtle)
            c.setFillColor(_hex_alpha(theme["secondary"], 0.15))
            c.circle(w * 0.85, block_y + block_h * 0.7, 80, fill=1, stroke=0)
            c.circle(w * 0.15, block_y + block_h * 0.3, 50, fill=1, stroke=0)
            c.circle(w * 0.7, block_y + block_h * 0.15, 35, fill=1, stroke=0)
            c.restoreState()

            # ── Title text on colored block ──
            c.saveState()
            c.setFillColor(white)

            # Small decorative line above title
            line_w = 60
            c.setStrokeColor(_hex_alpha("#FFFFFF", 0.6))
            c.setLineWidth(2)
            c.line(w / 2 - line_w / 2, block_y + block_h * 0.72, w / 2 + line_w / 2, block_y + block_h * 0.72)

            # Book title
            c.setFont(font_bold, 42)
            title_y = block_y + block_h * 0.55
            tw = c.stringWidth(book_title, font_bold, 42)
            c.drawString(w / 2 - tw / 2, title_y, book_title)

            # Decorative line below title
            c.setLineWidth(1.5)
            c.line(w / 2 - line_w / 2, title_y - 12, w / 2 + line_w / 2, title_y - 12)

            # Grade label
            c.setFont(font_bold, 20)
            grade_y = title_y - 40
            gw = c.stringWidth(label, font_bold, 20)
            # Badge background
            badge_pad = 12
            _draw_rounded_rect(c, w / 2 - gw / 2 - badge_pad, grade_y - 6,
                               gw + badge_pad * 2, 30, 6,
                               fill_color=_hex_alpha(theme["dark"], 0.4))
            c.setFillColor(white)
            c.drawString(w / 2 - gw / 2, grade_y, label)

            # Program subtitle
            c.setFont(font_name, 14)
            sub_text = "SmartCampusAI English Language Program"
            stw = c.stringWidth(sub_text, font_name, 14)
            c.setFillColor(_hex_alpha("#FFFFFF", 0.85))
            c.drawString(w / 2 - stw / 2, grade_y - 36, sub_text)

            c.restoreState()

            # ── Bottom white section ──
            bottom_h = h * 0.40

            # Year
            c.saveState()
            c.setFont(font_bold, 22)
            c.setFillColor(C_PRIMARY)
            year_text = "2025 - 2026"
            yw = c.stringWidth(year_text, font_bold, 22)
            year_y = block_y - 50
            c.drawString(w / 2 - yw / 2, year_y, year_text)

            # Decorative diamonds around year
            _draw_diamond(c, w / 2 - yw / 2 - 16, year_y + 8, 4, C_SECONDARY)
            _draw_diamond(c, w / 2 + yw / 2 + 16, year_y + 8, 4, C_SECONDARY)

            # Accent lines
            c.setStrokeColor(C_SECONDARY)
            c.setLineWidth(1)
            line_half = 80
            c.line(w / 2 - line_half, year_y - 16, w / 2 + line_half, year_y - 16)

            # Institution placeholder
            c.setFont(font_name, 11)
            c.setFillColor(HexColor("#94A3B8"))
            inst_text = "Your School Name Here"
            iw = c.stringWidth(inst_text, font_name, 11)
            c.drawString(w / 2 - iw / 2, year_y - 42, inst_text)

            # Bottom accent strip
            c.setFillColor(C_PRIMARY)
            c.rect(0, 0, w, 6, fill=1, stroke=0)
            c.setFillColor(C_SECONDARY)
            c.rect(0, 6, w, 2, fill=1, stroke=0)

            c.restoreState()

    class SectionHeaderFlowable(Flowable):
        """Draws a decorated section header with icon symbol and accent bar."""
        def __init__(self, title, icon_char="", width=CONTENT_W):
            Flowable.__init__(self)
            self.title = title
            self.icon_char = icon_char
            self._width = width

        def wrap(self, availWidth, availHeight):
            return (self._width, 36)

        def draw(self):
            c = self.canv
            w = self._width
            h = 36

            # Accent bar left
            _draw_rounded_rect(c, 0, 2, 5, h - 4, 2, fill_color=C_PRIMARY)

            # Background
            _draw_rounded_rect(c, 8, 0, w - 8, h, 6, fill_color=C_BG)

            # Icon circle
            _draw_circle(c, 28, h / 2, 12, C_PRIMARY)
            c.saveState()
            c.setFont(font_bold, 12)
            c.setFillColor(white)
            iw = c.stringWidth(self.icon_char, font_bold, 12)
            c.drawString(28 - iw / 2, h / 2 - 4, self.icon_char)
            c.restoreState()

            # Title text
            c.saveState()
            c.setFont(font_bold, font_sz + 6)
            c.setFillColor(C_DARK)
            c.drawString(46, h / 2 - (font_sz + 6) / 2 + 1, self.title)
            c.restoreState()

    class UnitOpenerFlowable(Flowable):
        """Full-height unit opener with banner, title, skills."""
        def __init__(self, unit_num, unit_title, week_start, week_end, width=CONTENT_W, height=PAGE_H - MARGIN_TOP - MARGIN_BOTTOM):
            Flowable.__init__(self)
            self.unit_num = unit_num
            self.unit_title = unit_title
            self.week_start = week_start
            self.week_end = week_end
            self._width = width
            self._height = height

        def wrap(self, availWidth, availHeight):
            return (self._width, self._height)

        def draw(self):
            c = self.canv
            w = self.width
            h = self.height

            # ── Large accent banner at top ──
            banner_h = 120
            banner_y = h - banner_h
            _draw_rounded_rect(c, 0, banner_y, w, banner_h, 12, fill_color=C_PRIMARY)

            # Decorative overlay on banner
            _draw_rounded_rect(c, 0, banner_y, w * 0.35, banner_h, 12,
                               fill_color=_hex_alpha(theme["dark"], 0.2))

            # "UNIT X" text
            c.saveState()
            c.setFont(font_bold, 52)
            c.setFillColor(white)
            unit_text = f"UNIT {self.unit_num}"
            uw = c.stringWidth(unit_text, font_bold, 52)
            c.drawString(w / 2 - uw / 2, banner_y + banner_h / 2 - 5, unit_text)

            # Decorative diamonds on banner
            _draw_diamond(c, 30, banner_y + banner_h / 2, 6, _hex_alpha("#FFFFFF", 0.3))
            _draw_diamond(c, w - 30, banner_y + banner_h / 2, 6, _hex_alpha("#FFFFFF", 0.3))
            _draw_diamond(c, 55, banner_y + 20, 4, _hex_alpha("#FFFFFF", 0.2))
            _draw_diamond(c, w - 55, banner_y + banner_h - 20, 4, _hex_alpha("#FFFFFF", 0.2))
            c.restoreState()

            # ── Theme title ──
            c.saveState()
            c.setFont(font_bold, 30)
            c.setFillColor(C_DARK)
            ttw = c.stringWidth(self.unit_title, font_bold, 30)
            title_y = banner_y - 50
            # Truncate if too wide
            display_title = self.unit_title
            if ttw > w - 20:
                while c.stringWidth(display_title + "...", font_bold, 30) > w - 20 and len(display_title) > 5:
                    display_title = display_title[:-1]
                display_title += "..."
                ttw = c.stringWidth(display_title, font_bold, 30)
            c.drawString(w / 2 - ttw / 2, title_y, display_title)

            # Decorative line under title
            c.setStrokeColor(C_SECONDARY)
            c.setLineWidth(2)
            dec_w = min(ttw + 40, w - 40)
            c.line(w / 2 - dec_w / 2, title_y - 14, w / 2 + dec_w / 2, title_y - 14)
            c.restoreState()

            # ── Week range ──
            c.saveState()
            c.setFont(font_name, 13)
            c.setFillColor(HexColor("#64748B"))
            week_text = f"Weeks {self.week_start} - {self.week_end}"
            ww = c.stringWidth(week_text, font_name, 13)
            c.drawString(w / 2 - ww / 2, title_y - 38, week_text)
            c.restoreState()

            # ── 4 Skill icons ──
            skills_data = [
                ("L", "Listening"),
                ("S", "Speaking"),
                ("R", "Reading"),
                ("W", "Writing"),
            ]
            icon_y = title_y - 120
            icon_spacing = w / 5
            for idx, (icon_letter, skill_name) in enumerate(skills_data):
                cx = icon_spacing * (idx + 0.5) + icon_spacing * 0.25
                # Circle background
                _draw_circle(c, cx, icon_y + 20, 24, C_BG)
                _draw_circle(c, cx, icon_y + 20, 22, C_PRIMARY)
                # Letter
                c.saveState()
                c.setFont(font_bold, 18)
                c.setFillColor(white)
                lw = c.stringWidth(icon_letter, font_bold, 18)
                c.drawString(cx - lw / 2, icon_y + 14, icon_letter)
                c.restoreState()
                # Label
                c.saveState()
                c.setFont(font_name, 9)
                c.setFillColor(C_DARK)
                slw = c.stringWidth(skill_name, font_name, 9)
                c.drawString(cx - slw / 2, icon_y - 12, skill_name)
                c.restoreState()

            # ── Bottom accent line ──
            c.saveState()
            c.setStrokeColor(C_SECONDARY)
            c.setLineWidth(1.5)
            c.line(w * 0.2, 30, w * 0.8, 30)
            _draw_diamond(c, w / 2, 30, 4, C_PRIMARY)
            c.restoreState()

    class AccentDivider(Flowable):
        """A decorative horizontal divider with diamond center."""
        def __init__(self, width=CONTENT_W):
            Flowable.__init__(self)
            self._width = width

        def wrap(self, availWidth, availHeight):
            return (self._width, 16)

        def draw(self):
            c = self.canv
            w = self._width
            y = 8
            c.saveState()
            c.setStrokeColor(C_SECONDARY)
            c.setLineWidth(0.8)
            c.line(w * 0.15, y, w * 0.42, y)
            c.line(w * 0.58, y, w * 0.85, y)
            _draw_diamond(c, w / 2, y, 4, C_PRIMARY)
            c.restoreState()

    class WritingLines(Flowable):
        """Draw horizontal writing lines for student response area."""
        def __init__(self, num_lines=6, width=CONTENT_W):
            Flowable.__init__(self)
            self.num_lines = num_lines
            self._width = width

        def wrap(self, availWidth, availHeight):
            return (self._width, self.num_lines * 24 + 10)

        def draw(self):
            c = self.canv
            w = self._width
            c.saveState()
            c.setStrokeColor(_hex_alpha(theme["primary"], 0.25))
            c.setLineWidth(0.5)
            for i in range(self.num_lines):
                y = (self.num_lines - 1 - i) * 24 + 10
                c.line(20, y, w - 20, y)
            c.restoreState()

    class SelfAssessmentStars(Flowable):
        """Draw self-assessment with 3 star levels."""
        def __init__(self, width=CONTENT_W):
            Flowable.__init__(self)
            self._width = width

        def wrap(self, availWidth, availHeight):
            return (self._width, 60)

        def draw(self):
            c = self.canv
            w = self._width
            labels = ["Need Practice", "Good", "Great!"]
            star_counts = [1, 2, 3]
            spacing = w / 4

            for idx, (lbl, count) in enumerate(zip(labels, star_counts)):
                cx = spacing * (idx + 0.75)
                # Stars
                for s in range(count):
                    sx = cx - (count - 1) * 10 / 2 + s * 10
                    _draw_star(c, sx, 38, 8, 4, C_SECONDARY if count < 3 else C_PRIMARY)
                # Label
                c.saveState()
                c.setFont(font_name, 8)
                c.setFillColor(C_DARK)
                lw = c.stringWidth(lbl, font_name, 8)
                c.drawString(cx - lw / 2, 12, lbl)
                c.restoreState()

    class CheckboxItem(Flowable):
        """Draw a checkbox with text."""
        def __init__(self, text, width=CONTENT_W):
            Flowable.__init__(self)
            self.text = text
            self._width = width

        def wrap(self, availWidth, availHeight):
            return (self._width, font_sz + 10)

        def draw(self):
            c = self.canv
            h = font_sz + 10
            box_size = 11
            # Draw checkbox square
            c.saveState()
            c.setStrokeColor(C_PRIMARY)
            c.setLineWidth(1.2)
            c.rect(8, h / 2 - box_size / 2, box_size, box_size, fill=0, stroke=1)
            # Text
            c.setFont(font_name, font_sz)
            c.setFillColor(HexColor("#1E293B"))
            c.drawString(26, h / 2 - font_sz / 2 + 1, self.text)
            c.restoreState()

    class BackCoverFlowable(Flowable):
        """Elegant back cover page."""
        def __init__(self, total_units, total_words):
            Flowable.__init__(self)
            self.total_units = total_units
            self.total_words = total_words
            self.width = PAGE_W - 40 * mm
            self.height = PAGE_H - 40 * mm

        def wrap(self, availWidth, availHeight):
            return (self.width, self.height)

        def draw(self):
            c = self.canv
            w = self.width
            h = self.height

            # Bottom accent strip
            c.saveState()
            c.setFillColor(C_PRIMARY)
            c.rect(0, 0, w, 6, fill=1, stroke=0)
            c.setFillColor(C_SECONDARY)
            c.rect(0, 6, w, 2, fill=1, stroke=0)
            c.restoreState()

            # Centered content
            center_y = h * 0.55

            # Congratulations
            c.saveState()
            c.setFont(font_bold, 32)
            c.setFillColor(C_PRIMARY)
            cong_text = "Congratulations!"
            cw = c.stringWidth(cong_text, font_bold, 32)
            c.drawString(w / 2 - cw / 2, center_y + 60, cong_text)
            c.restoreState()

            # Decorative line
            c.saveState()
            c.setStrokeColor(C_SECONDARY)
            c.setLineWidth(1.5)
            c.line(w / 2 - 50, center_y + 46, w / 2 + 50, center_y + 46)
            _draw_diamond(c, w / 2, center_y + 46, 4, C_PRIMARY)
            c.restoreState()

            # Summary text
            c.saveState()
            c.setFont(font_name, 14)
            c.setFillColor(HexColor("#475569"))

            line1 = f"You have completed {self.total_units} units"
            l1w = c.stringWidth(line1, font_name, 14)
            c.drawString(w / 2 - l1w / 2, center_y + 14, line1)

            line2 = f"and learned {self.total_words}+ new words!"
            l2w = c.stringWidth(line2, font_name, 14)
            c.drawString(w / 2 - l2w / 2, center_y - 8, line2)
            c.restoreState()

            # Stars
            for i in range(5):
                sx = w / 2 - 40 + i * 20
                _draw_star(c, sx, center_y - 44, 10, 5, C_PRIMARY)

            # Branding
            c.saveState()
            c.setFont(font_bold, 18)
            c.setFillColor(C_PRIMARY)
            brand = "SmartCampusAI"
            bw = c.stringWidth(brand, font_bold, 18)
            c.drawString(w / 2 - bw / 2, center_y - 100, brand)

            c.setFont(font_name, 10)
            c.setFillColor(HexColor("#94A3B8"))
            tagline = "English Language Program"
            tw = c.stringWidth(tagline, font_name, 10)
            c.drawString(w / 2 - tw / 2, center_y - 118, tagline)
            c.restoreState()

    # ─── Content helpers (story, song, dialogue generators) ───
    def _story_lines(theme_title: str, words: list) -> list[str]:
        t = theme_title.lower() if theme_title else "adventure"
        w = words if words else ["hello", "friend"]
        lines = [
            f"Hello! Today we learn about {t}.",
            f"Look! I can see a {w[0]}!",
            f"Wow, that is so cool! Do you like {w[1] if len(w) > 1 else w[0]}?",
            f"Yes! {w[0]} is my favorite!",
            "Let's practice together! Ready?",
        ]
        if grade >= 5:
            lines.append(f"I've been studying {t} for a while now.")
            lines.append(f"Can you explain more about {w[2] if len(w) > 2 else w[0]}?")
            lines.append(f"Sure! Let me share what I know about {t}.")
        if grade >= 9:
            lines.append(f"This connects to what we discussed about {w[3] if len(w) > 3 else (w[1] if len(w) > 1 else 'the concept')}.")
            lines.append("That's a great analysis! Let's explore further.")
        if grade == 0:
            return lines[:3]
        if grade <= 2:
            return lines[:4]
        if grade <= 4:
            return lines[:5]
        if grade <= 8:
            return lines[:8]
        return lines

    def _song_lines(theme_title: str) -> list[str]:
        t = theme_title if theme_title else "Fun"
        return [
            f"{t}, {t}, let's have fun!",
            "Learning English, everyone!",
            "Clap your hands and sing along,",
            f"{t} makes us strong!",
            "La la la, we love to learn,",
            "Now it's your turn!",
        ]

    def _dialogue_lines(title: str, words: list) -> list[tuple[str, str]]:
        topic = (title or "topic").lower()
        w = words if words else ["vocabulary"]
        return [
            ("Alex", f"Hi! Have you heard about {topic}?"),
            ("Sam", f"Yes! I find {topic} really interesting."),
            ("Alex", f'Do you know the word "{w[0]}"?'),
            ("Sam", "Of course! It means... can you help me remember?"),
            ("Alex", f"Sure! Let me explain. It is related to {w[1] if len(w) > 1 else w[0]}."),
            ("Sam", f'That makes sense! What about "{w[2] if len(w) > 2 else w[0]}"?'),
            ("Alex", "Great question! Let's practice using it in a sentence."),
            ("Sam", f'OK! "{w[3] if len(w) > 3 else w[0]} is fun when we work together!"'),
        ]

    # ─── Build document ───
    buf = io.BytesIO()

    # Define frames
    cover_frame = Frame(
        15 * mm, 15 * mm,
        PAGE_W - 30 * mm, PAGE_H - 30 * mm,
        id="cover_frame",
        showBoundary=0,
    )
    content_frame = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM,
        CONTENT_W, PAGE_H - MARGIN_TOP - MARGIN_BOTTOM,
        id="content_frame",
        showBoundary=0,
    )
    blank_frame = Frame(
        15 * mm, 15 * mm,
        PAGE_W - 30 * mm, PAGE_H - 30 * mm,
        id="blank_frame",
        showBoundary=0,
    )

    # Page templates
    cover_template = PageTemplate(id="cover", frames=[cover_frame], onPage=_cover_page_bg)
    content_template = PageTemplate(id="content", frames=[content_frame], onPage=_header_footer)
    blank_template = PageTemplate(id="blank", frames=[blank_frame], onPage=_blank_page_bg)

    doc = BaseDocTemplate(
        buf, pagesize=A4,
        title=book_title,
        author="SmartCampusAI",
        pageTemplates=[cover_template, content_template, blank_template],
    )

    elements: list = []

    # ══════════════════════════════════════════
    #  COVER PAGE
    # ══════════════════════════════════════════
    elements.append(CoverFlowable(PAGE_W - 40 * mm, PAGE_H - 40 * mm))
    elements.append(NextPageTemplate("content"))
    elements.append(PageBreak())

    # ══════════════════════════════════════════
    #  TABLE OF CONTENTS
    # ══════════════════════════════════════════
    elements.append(SectionHeaderFlowable("TABLE OF CONTENTS", "T"))
    elements.append(Spacer(1, 16))

    toc_rows = []
    for unit in units:
        toc_rows.append([
            Paragraph(f'<font color="{theme["primary"]}"><b>Unit {unit["num"]}</b></font>', s_body),
            Paragraph(unit["title"], s_body),
        ])
    if toc_rows:
        toc_table = Table(toc_rows, colWidths=[CONTENT_W * 0.2, CONTENT_W * 0.8])
        toc_table.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, _hex_alpha(theme["primary"], 0.15)),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, C_BG]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(toc_table)

    elements.append(NextPageTemplate("blank"))
    elements.append(PageBreak())

    # ══════════════════════════════════════════
    #  UNIT PAGES
    # ══════════════════════════════════════════
    total_words_count = 0

    for unit in units:
        u_num = unit["num"]
        u_title = unit["title"]
        all_vocab = []
        for w in unit["weeks"]:
            all_vocab.extend(w.get("vocab", []))
        all_vocab = list(dict.fromkeys(all_vocab))
        total_words_count += len(all_vocab)

        week_start = (u_num - 1) * weeks_per_unit + 1
        week_end = min(u_num * weeks_per_unit, len(curriculum_weeks))

        # ── UNIT OPENER PAGE (blank template - no header/footer) ──
        elements.append(UnitOpenerFlowable(u_num, u_title, week_start, week_end))
        elements.append(NextPageTemplate("content"))
        elements.append(PageBreak())

        # ── VOCABULARY PAGE ──
        elements.append(SectionHeaderFlowable("WORD BANK", "W"))
        elements.append(Spacer(1, 12))

        if all_vocab:
            # 3-column grid with accent left border per cell
            rows = []
            row = []
            for idx, word in enumerate(all_vocab):
                row.append(Paragraph(f'<b>{word}</b>', s_vocab_word))
                if len(row) == 3:
                    rows.append(row)
                    row = []
            if row:
                while len(row) < 3:
                    row.append(Paragraph("", s_vocab_word))
                rows.append(row)

            col_w = CONTENT_W / 3
            vocab_table = Table(rows, colWidths=[col_w] * 3)

            # Build style commands
            vocab_style_cmds = [
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, _hex_alpha(theme["primary"], 0.2)),
            ]
            # Alternate row background
            for r_idx in range(len(rows)):
                bg = C_BG if r_idx % 2 == 0 else white
                vocab_style_cmds.append(("BACKGROUND", (0, r_idx), (-1, r_idx), bg))
            # Left border accent on each cell
            for r_idx in range(len(rows)):
                for c_idx in range(3):
                    vocab_style_cmds.append(
                        ("LINEBEFOREDECOR", (c_idx, r_idx), (c_idx, r_idx), 3, C_PRIMARY)
                    )

            vocab_table.setStyle(TableStyle(vocab_style_cmds))
            elements.append(vocab_table)
        else:
            elements.append(Paragraph("(No vocabulary for this unit)", s_body_center))

        elements.append(PageBreak())

        # ── STORY PAGE ──
        elements.append(SectionHeaderFlowable("STORY TIME", "S"))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("<i>Read and listen</i>", s_instruction))
        elements.append(Spacer(1, 8))

        story_words = all_vocab[:8]
        lines = _story_lines(u_title, story_words)
        speakers = ["Mia", "Tom"]

        # Story in a rounded box via table with background
        story_paragraphs = []
        for i, line in enumerate(lines):
            speaker = speakers[i % 2]
            display_line = line
            for vw in story_words:
                if vw.lower() in display_line.lower():
                    display_line = display_line.replace(
                        vw, f'<font color="{theme["primary"]}"><b>{vw}</b></font>'
                    )
            story_paragraphs.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>{speaker}:</b></font> {display_line}',
                s_body,
            ))
            story_paragraphs.append(Spacer(1, 3))

        story_cell = [[story_paragraphs]]
        story_table = Table(story_cell, colWidths=[CONTENT_W - 10])
        story_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), C_BG),
            ("BOX", (0, 0), (-1, -1), 1.5, C_SECONDARY),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LEFTPADDING", (0, 0), (-1, -1), 18),
            ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ]))
        elements.append(story_table)
        elements.append(PageBreak())

        # ── SONG PAGE ──
        elements.append(SectionHeaderFlowable("SING ALONG", "M"))
        elements.append(Spacer(1, 12))

        song = _song_lines(u_title)
        for s_idx, sl in enumerate(song):
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}">&#9835;</font>  <i>{sl}</i>',
                s_song_line,
            ))
            # Decorative line between verses (every 2 lines)
            if s_idx % 2 == 1 and s_idx < len(song) - 1:
                elements.append(AccentDivider())

        elements.append(Spacer(1, 16))
        elements.append(AccentDivider())
        elements.append(Spacer(1, 8))
        elements.append(Paragraph("<i>Sing along with your friends!</i>", s_instruction))
        elements.append(PageBreak())

        # ── GRAMMAR PAGE (grade 3+) ──
        if grade >= 3:
            elements.append(SectionHeaderFlowable("GRAMMAR FOCUS", "G"))
            elements.append(Spacer(1, 10))

            structure = unit["weeks"][0].get("structure", "")
            rule = structure if structure else "Simple Present Tense"

            # Rule in prominent box with accent left border
            rule_data = [[Paragraph(
                f'<font color="{theme["primary"]}"><b>Structure:</b></font><br/>'
                f'<b>{rule}</b>',
                s_grammar_rule,
            )]]
            rule_table = Table(rule_data, colWidths=[CONTENT_W - 16])
            rule_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_BG),
                ("LINEBEFOREDECOR", (0, 0), (0, -1), 5, C_PRIMARY),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ]))
            elements.append(rule_table)
            elements.append(Spacer(1, 12))

            # Examples in numbered list with light background
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>Examples:</b></font>',
                s_section_header,
            ))
            examples = [
                f'1. "I <b>like</b> apples."',
                f'2. "She <b>likes</b> apples."',
                f'3. "They <b>like</b> apples too."',
            ]
            ex_items = []
            for ex in examples:
                ex_items.append([Paragraph(ex, s_body)])

            ex_table = Table(ex_items, colWidths=[CONTENT_W - 40])
            ex_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FAFBFC")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, _hex_alpha(theme["primary"], 0.1)),
            ]))
            elements.append(ex_table)
            elements.append(Spacer(1, 12))

            # "Remember!" tip box
            tip_data = [[Paragraph(
                f'<font color="{theme["primary"]}"><b>Remember!</b></font> '
                f'Practice makes perfect. Try making your own sentences using this structure.',
                s_body,
            )]]
            tip_table = Table(tip_data, colWidths=[CONTENT_W - 16])
            tip_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), _hex_alpha(theme["secondary"], 0.15)),
                ("BOX", (0, 0), (-1, -1), 1.2, C_SECONDARY),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ]))
            elements.append(tip_table)
            elements.append(PageBreak())

        # ── DIALOGUE PAGE (grade 5+) ──
        if grade >= 5:
            elements.append(SectionHeaderFlowable("LET'S TALK", "D"))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"<i>Topic: {u_title}</i>", s_instruction))
            elements.append(Spacer(1, 10))

            dlg = _dialogue_lines(u_title, all_vocab[:8])
            dlg_rows = []
            for speaker_name, text in dlg:
                is_alex = speaker_name == "Alex"
                if is_alex:
                    # Left-aligned accent bubble
                    bubble_data = [[Paragraph(
                        f'<font color="{theme["primary"]}"><b>{speaker_name}:</b></font> {text}',
                        s_dialogue,
                    )]]
                    bubble = Table(bubble_data, colWidths=[CONTENT_W * 0.72])
                    bubble.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), C_BG),
                        ("BOX", (0, 0), (-1, -1), 1, C_SECONDARY),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ]))
                    dlg_rows.append([bubble, ""])
                else:
                    # Right-aligned gray bubble
                    bubble_data = [[Paragraph(
                        f'<font color="#64748B"><b>{speaker_name}:</b></font> {text}',
                        s_dialogue,
                    )]]
                    bubble = Table(bubble_data, colWidths=[CONTENT_W * 0.72])
                    bubble.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F1F5F9")),
                        ("BOX", (0, 0), (-1, -1), 1, HexColor("#CBD5E1")),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ]))
                    dlg_rows.append(["", bubble])

            if dlg_rows:
                dlg_table = Table(dlg_rows, colWidths=[CONTENT_W * 0.5, CONTENT_W * 0.5])
                dlg_style_cmds = [
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ]
                # Align Alex left, Sam right
                for r_idx in range(len(dlg_rows)):
                    if dlg_rows[r_idx][0] != "":
                        dlg_style_cmds.append(("ALIGN", (0, r_idx), (0, r_idx), "LEFT"))
                    else:
                        dlg_style_cmds.append(("ALIGN", (1, r_idx), (1, r_idx), "RIGHT"))
                    dlg_style_cmds.append(("VALIGN", (0, r_idx), (-1, r_idx), "MIDDLE"))

                dlg_table.setStyle(TableStyle(dlg_style_cmds))
                elements.append(dlg_table)

            elements.append(Spacer(1, 12))
            elements.append(Paragraph("<i>Practice with a friend!</i>", s_instruction))
            elements.append(PageBreak())

        # ── WRITING PAGE (grade 7+) ──
        if grade >= 7:
            elements.append(SectionHeaderFlowable("WRITING WORKSHOP", "P"))
            elements.append(Spacer(1, 10))

            topic = (u_title or "My Experience").lower()

            # Model text in bordered box
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>Model Text</b></font>',
                s_section_header,
            ))
            model_text = (
                f'Last week, I had an interesting experience with '
                f'<font color="{theme["primary"]}"><u><b>{topic}</b></u></font>. '
                f'It made me think about how important it is to '
                f'<font color="{theme["primary"]}"><u><b>practice regularly</b></u></font>. '
                f'<font color="{theme["primary"]}"><u><b>First</b></u></font>, I started by reading about the topic. '
                f'<font color="{theme["primary"]}"><u><b>Then</b></u></font>, I discussed it with my classmates. '
                f'<font color="{theme["primary"]}"><u><b>Finally</b></u></font>, I wrote my own thoughts about it. '
                f'I believe that learning about '
                f'<font color="{theme["primary"]}"><u><b>{topic}</b></u></font> will help me in the future.'
            )
            model_data = [[Paragraph(model_text, s_body)]]
            model_table = Table(model_data, colWidths=[CONTENT_W - 16])
            model_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_BG),
                ("LINEBEFOREDECOR", (0, 0), (0, -1), 4, C_PRIMARY),
                ("BOX", (0, 0), (-1, -1), 1, C_SECONDARY),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ]))
            elements.append(model_table)
            elements.append(Spacer(1, 10))

            # Key phrases highlighted
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>Key Phrases</b></font>',
                s_section_header,
            ))
            phrases = ["First / Then / Finally", "I believe that...",
                       "It made me think...", "In my opinion..."]
            phrase_cells = []
            for ph in phrases:
                phrase_cells.append([Paragraph(
                    f'<font color="{theme["primary"]}"><b>{ph}</b></font>', s_body,
                )])
            ph_table = Table(phrase_cells, colWidths=[CONTENT_W - 40])
            ph_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), _hex_alpha(theme["secondary"], 0.1)),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("LINEBELOW", (0, 0), (-1, -2), 0.3, _hex_alpha(theme["primary"], 0.1)),
            ]))
            elements.append(ph_table)
            elements.append(Spacer(1, 12))

            # "Now you try:" prompt with lined area
            prompt_data = [[Paragraph(
                f'<font color="{theme["primary"]}"><b>Now you try!</b></font><br/>'
                f'Write a short paragraph (5-7 sentences) about <b>{u_title}</b>.<br/>'
                f'<font color="#64748B">Use the key phrases above. Include your personal opinion.</font>',
                s_body,
            )]]
            prompt_table = Table(prompt_data, colWidths=[CONTENT_W - 16])
            prompt_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), _hex_alpha(theme["primary"], 0.05)),
                ("BOX", (0, 0), (-1, -1), 1.5, C_PRIMARY),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
            ]))
            elements.append(prompt_table)
            elements.append(Spacer(1, 8))
            elements.append(WritingLines(num_lines=7))
            elements.append(PageBreak())

        # ── ACTIVITY PAGE ──
        elements.append(SectionHeaderFlowable("PRACTICE TIME", "A"))
        elements.append(Spacer(1, 10))

        if len(all_vocab) >= 2:
            # Fill-in-the-blank exercises
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>A. Fill in the blanks with the correct word:</b></font>',
                s_section_header,
            ))
            blanks = all_vocab[:4]
            # Word bank hint
            word_bank_text = " | ".join([f'<b>{bw}</b>' for bw in blanks])
            wb_data = [[Paragraph(
                f'<font color="{theme["primary"]}">Word Bank:</font> {word_bank_text}',
                s_body,
            )]]
            wb_table = Table(wb_data, colWidths=[CONTENT_W - 16])
            wb_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), C_BG),
                ("BOX", (0, 0), (-1, -1), 1, C_SECONDARY),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]))
            elements.append(wb_table)
            elements.append(Spacer(1, 8))

            for idx_b, bw in enumerate(blanks, 1):
                elements.append(Paragraph(
                    f'{idx_b}. I like _________________________ .',
                    s_body,
                ))
                elements.append(Spacer(1, 2))

            elements.append(Spacer(1, 14))

            # Match words exercise
            elements.append(Paragraph(
                f'<font color="{theme["primary"]}"><b>B. Match the words:</b></font>',
                s_section_header,
            ))

            match_left = all_vocab[:min(5, len(all_vocab))]
            import random as _rnd
            match_right = list(match_left)
            _rnd.shuffle(match_right)

            match_rows = []
            for ml, mr in zip(match_left, match_right):
                match_rows.append([
                    Paragraph(f'<b>{match_left.index(ml) + 1}.</b> {ml}', s_body),
                    Paragraph("", s_body_center),
                    Paragraph(f'<b>{chr(65 + match_right.index(mr))}.</b> {mr}', s_body),
                ])
            if match_rows:
                match_table = Table(match_rows, colWidths=[CONTENT_W * 0.38, CONTENT_W * 0.24, CONTENT_W * 0.38])
                match_style = [
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.5, _hex_alpha(theme["primary"], 0.15)),
                ]
                # Alternate rows
                for r_idx in range(len(match_rows)):
                    if r_idx % 2 == 0:
                        match_style.append(("BACKGROUND", (0, r_idx), (-1, r_idx), C_BG))
                match_table.setStyle(TableStyle(match_style))
                elements.append(match_table)
        else:
            elements.append(Paragraph("Practice the words you learned in this unit!", s_body_center))

        elements.append(PageBreak())

        # ── REVIEW PAGE ──
        elements.append(SectionHeaderFlowable("UNIT REVIEW", "R"))
        elements.append(Spacer(1, 12))

        # Skills checklist with checkboxes
        skills = unit["weeks"][0].get("skills", {})
        if skills:
            items = list(skills.items())
        else:
            items = [
                ("Listening", "I can understand new words when I hear them."),
                ("Speaking", "I can say the new words and use them in sentences."),
                ("Reading", "I can read and understand the texts in this unit."),
                ("Writing", "I can write sentences using the new vocabulary."),
            ]

        elements.append(Paragraph(
            f'<font color="{theme["primary"]}"><b>Skills Checklist</b></font>',
            s_section_header,
        ))

        for skill_name, skill_desc in items:
            elements.append(CheckboxItem(f"I can... {skill_desc}  ({skill_name})"))
            elements.append(Spacer(1, 2))

        elements.append(Spacer(1, 16))
        elements.append(AccentDivider())
        elements.append(Spacer(1, 12))

        # Self-assessment stars
        elements.append(Paragraph(
            f'<font color="{theme["primary"]}"><b>How did I do?</b></font>',
            s_section_header,
        ))
        elements.append(SelfAssessmentStars())
        elements.append(Spacer(1, 16))
        elements.append(AccentDivider())
        elements.append(Spacer(1, 12))

        # Teacher's Note area
        elements.append(Paragraph(
            f'<font color="{theme["primary"]}"><b>Teacher\'s Note:</b></font>',
            s_section_header,
        ))
        elements.append(WritingLines(num_lines=4))

        elements.append(NextPageTemplate("blank"))
        elements.append(PageBreak())

    # ══════════════════════════════════════════
    #  BACK COVER
    # ══════════════════════════════════════════
    elements.append(BackCoverFlowable(len(units), total_words_count))

    # ─── Build PDF ───
    try:
        doc.build(elements)
        return buf.getvalue()
    except Exception:
        import traceback; traceback.print_exc()
        return None
