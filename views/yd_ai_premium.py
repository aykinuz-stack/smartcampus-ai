"""
Premium AI Ders Asistani — Tier 1/2/3
OpenAI TTS, Interactive Board, Quiz, Flashcards, Summary, Chat, Progress, Gamification
"""
from __future__ import annotations
import json, os, time, logging, base64
from datetime import datetime, timedelta
import streamlit as st

_logger = logging.getLogger("yd_ai_premium")
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "english")

# ════════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════════
AI_TEACHERS = {
    "mr_james": {"name": "Mr. James", "emoji": "\U0001F468\u200D\U0001F3EB", "voice": "echo",
                 "skin": "#DEB887", "hair": "#2C1810", "shirt": "#2563eb", "is_female": False},
    "ms_emily": {"name": "Ms. Emily", "emoji": "\U0001F469\u200D\U0001F3EB", "voice": "nova",
                 "skin": "#F5D0A9", "hair": "#4A2800", "shirt": "#7c3aed", "is_female": True},
    "prof_ali": {"name": "Prof. Ali", "emoji": "\U0001F468\u200D\U0001F3EB", "voice": "alloy",
                 "skin": "#C68642", "hair": "#1a1a2e", "shirt": "#059669", "is_female": False},
}
DIFFICULTY_MAP = {"easy": "Kolay", "normal": "Normal", "hard": "Zor"}

# XP & Badge constants
BADGE_DEFS = [
    {"id": "first_lesson", "name": "Ilk Ders", "icon": "\U0001F31F", "req": 1},
    {"id": "five_lessons", "name": "Caliskan", "icon": "\U0001F4DA", "req": 5},
    {"id": "ten_lessons", "name": "Uzman", "icon": "\U0001F393", "req": 10},
    {"id": "streak_3", "name": "3 Gun Seri", "icon": "\U0001F525", "req_streak": 3},
    {"id": "streak_7", "name": "7 Gun Seri", "icon": "\U0001F4A5", "req_streak": 7},
    {"id": "perfect_quiz", "name": "Tam Puan", "icon": "\U0001F3C6", "req_score": 100},
    {"id": "twenty_five", "name": "25 Ders", "icon": "\U0001F48E", "req": 25},
]

# ════════════════════════════════════════════════════════════
# OPENAI CLIENT
# ════════════════════════════════════════════════════════════
def _get_client():
    try:
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if api_key:
            return OpenAI(api_key=api_key)
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("OPENAI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip()
                        if api_key:
                            return OpenAI(api_key=api_key)
    except Exception as e:
        _logger.error(f"OpenAI client: {e}")
    return None

# ════════════════════════════════════════════════════════════
# STRUCTURED AI LESSON
# ════════════════════════════════════════════════════════════
def ai_explain_structured(konu: str, grade: int, difficulty: str = "normal") -> dict | None:
    client = _get_client()
    if not client:
        return None
    diff_inst = {
        "easy": "Very simple. Short sentences. Translate ALL to Turkish. 16-20 sections. 5 vocab words. Each text section MUST be at least 3-4 sentences long.",
        "normal": "Balanced. Clear explanations. Turkish for key parts. 20-26 sections. 8 vocab words. Each text section MUST be at least 4-5 sentences long. Stories and analogies MUST be at least 5-6 sentences.",
        "hard": "Challenging. Complex sentences. Minimal Turkish. 22-30 sections. 10+ vocab words. Each text section MUST be at least 5-6 sentences long.",
    }
    level_map = {
        1: "Grade 1, Pre-A1. Translate ALL sentences to Turkish.",
        2: "Grade 2, Pre-A1. Simple with fun. Translate ALL.",
        3: "Grade 3, A1. Simple English. Translate key sentences.",
        4: "Grade 4, A1. Clear English. Translate key parts.",
        5: "Grade 5, A1-A2. English instruction. Turkish for grammar.",
        6: "Grade 6, A2. Mostly English. Turkish for complex grammar.",
        7: "Grade 7, A2-B1. English. Turkish for hard concepts.",
        8: "Grade 8, A2-B1. English-dominant. LGS focus.",
        9: "Grade 9, B1. Full English. Turkish for abstract grammar.",
        10: "Grade 10, B1-B2. Full English. Minimal Turkish.",
        11: "Grade 11, B2. Full English. YDT tips.",
        12: "Grade 12, B2+. Full English. YDS/YDT strategies.",
    }
    system_msg = f"""You are an expert, charismatic, and inspiring English teacher at a Turkish school.
DO NOT teach like a textbook. Teach like a LIVE CLASS — engaging, warm, and interactive.
Level: {level_map.get(grade, f"Grade {grade}")}
Difficulty: {diff_inst.get(difficulty, diff_inst["normal"])}

═══ TEACHING STYLE (VERY IMPORTANT) ═══
You are NOT a book. You are a TEACHER in a real classroom. Teach like this:
1. ALWAYS START WITH A GREETING: "Hey everyone! 👋 Welcome back!", "Good morning class! 🌟 Ready for something fun?"
2. INTRODUCE THE TOPIC with excitement: "Today we're diving into... and trust me, this one's going to be awesome!"
3. USE STORIES/SCENARIOS: "Tom went to a restaurant and...", "A tourist in Istanbul asked..."
4. DAILY LIFE ANALOGIES: "Think of grammar like building blocks...", "Verbs are like action heroes..."
5. ASK THE STUDENT throughout: "What do you think? 🤔", "Can you guess? 💭", "Which one sounds right?"
6. SHARE FUN FACTS: "Did you know? 🧠", "Here's something mind-blowing! 🤯"
7. SHOW COMMON MISTAKES: "Turkish students often say X, but the correct way is Y..."
8. USE EMOJIS in content to make it visual and fun (but relevant to the topic!)
9. BE ENCOURAGING: "You're doing amazing! 🎉", "See? Not that hard, right? 💪"
10. ADD VISUAL BREAKS with topic-relevant emojis: 📚🎯✨🌟💡🎭🗣️🏆
FORBIDDEN: Dry, encyclopedic listing. "X is Y. Z is W." style flat information dumps.
GOAL: Student says "Wow, English is fun!" not "What a boring lesson."

Return your response as valid JSON with this EXACT structure:
{{
  "title": "Lesson title (max 50 chars)",
  "sections": [
    {{"type": "greeting", "teacher_name": "Mr. James", "message": "Hey everyone! 👋 Great to see you today! Are you ready for something exciting?", "topic_intro": "Today we're going to explore [TOPIC] — and I promise, by the end of this lesson, you'll feel like a pro! 🌟"}},
    {{"type": "header", "text": "📚 Section Title", "emoji": "📚"}},
    {{"type": "text", "content": "Explanation paragraph with emojis where relevant..."}},
    {{"type": "visual", "emoji": "🏗️", "title": "Visual Concept", "content": "A visual/emoji-rich explanation that uses symbols to make the concept memorable. Example: 🔵 Subject + 🔴 Verb + 🟢 Object = ✅ Sentence!"}},
    {{"type": "story", "title": "📖 Story Title", "content": "A scenario/story that teaches the concept through engaging narrative with emojis..."}},
    {{"type": "curiosity", "content": "🤯 A surprising or fun fact! Something that makes the student say Wow! Use emojis to highlight key parts."}},
    {{"type": "analogy", "source": "Daily life thing", "target": "Grammar concept", "content": "Detailed analogy explanation with visual emojis..."}},
    {{"type": "challenge", "question": "🎯 Think about this: ...?", "hint": "💡 Hint: ...", "answer": "✅ Answer and explanation..."}},
    {{"type": "mistake", "wrong": "Common mistake Turkish students make", "correct": "The correct form", "explanation": "Why it's wrong and how to fix it"}},
    {{"type": "example", "en": "English sentence.", "tr": "Turkish translation."}},
    {{"type": "dialogue", "title": "🎭 Dialogue Title", "lines": [{{"speaker": "Tom", "text": "Hello!"}}, {{"speaker": "Emma", "text": "Hi!"}}]}},
    {{"type": "tip", "content": "💡 Grammar tip or note..."}},
    {{"type": "practice", "content": "✏️ Fill in: I ___ (go) to school."}},
    {{"type": "encouragement", "message": "🎉 You're doing fantastic! Let's keep going — the best part is coming up!"}},
    {{"type": "mini_quiz", "question": "🧐 Quick check! Which one is correct?", "options": ["Option A", "Option B", "Option C"], "correct": 0, "feedback_correct": "🎉 Excellent! You nailed it!", "feedback_wrong": "🤔 Not quite! The answer is A because..."}},
    {{"type": "recap", "title": "📋 Quick Recap", "points": ["✅ Point 1", "✅ Point 2", "✅ Point 3"]}},
    {{"type": "wrapup", "title": "🎓 Bugün Ne Öğrendik?", "learned": ["Today we learned that...", "We discovered how to...", "We practiced..."], "teacher_message": "Great job today, everyone! You worked really hard. Practice what we learned and I'll see you next time! 🌟👋", "homework_hint": "Try using [topic] in 3 sentences today!"}}
  ],
  "vocabulary": [
    {{"en": "word", "tr": "kelime", "phonetic": "/wɜːrd/", "example": "Example sentence."}}
  ],
  "quiz": [
    {{"question": "Question?", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "Why A is correct."}}
  ],
  "summary": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
  "tts_text": "MUST be 2500-4000 characters long! Start with: Hey everyone! Welcome to class! I'm so excited to see you today! Are you ready? Because today we're going to learn about [TOPIC] and trust me, it's going to be super fun! Then explain the ENTIRE lesson content in detail — cover every major concept, give examples, ask questions. Continue like a warm, engaging teacher. Ask questions: Right? Got it? Makes sense? Cool! Use encouraging phrases: You're doing great! See how easy that was? Awesome job! The tts_text should cover the FULL lesson and take at least 2-3 minutes to read aloud. No special characters."
}}

═══ SECTION MIX RULES ═══
REQUIRED sections (MUST include ALL of these — WRITE LONG, DETAILED CONTENT):
- 1x greeting (ALWAYS FIRST — greet students, introduce topic with excitement, 3-4 sentences)
- 3-4x header (section dividers with topic-relevant emoji)
- 4-6x text (DETAILED explanations, each at least 4-5 sentences! NOT short paragraphs!)
- 2x visual (emoji-rich visual concept breakdown)
- 1x story (engaging narrative, at least 5-6 sentences with a beginning, middle, end)
- 1x analogy (creative analogy with detailed explanation, 4+ sentences)
- 2x curiosity (fun facts / surprising info)
- 2x challenge (make the student think, include detailed hints and answers)
- 2-3x mini_quiz (INLINE QUIZ during the lesson! Place after teaching a concept to check understanding. 3 options, feedback for correct/wrong. CRITICAL for engagement!)
- 1x mistake (common errors Turkish students make, detailed explanation)
- 1x dialogue (realistic conversation, at least 6-8 lines back and forth)
- 2-3x example (with translation)
- 1-2x encouragement (mid-lesson and near-end motivation boost)
- 2x tip (grammar/usage tips)
- 1-2x practice (fill-in, complete the sentence)
- 1x recap (end summary with 5+ checkmark points)
- 1x wrapup (ALWAYS LAST — "Bugün Ne Öğrendik?" summary + teacher farewell + homework hint)
- Total: AT LEAST 24 sections, ideally 28-32. THIS IS CRITICAL — DO NOT MAKE SHORT LESSONS!

IMPORTANT — CONTENT LENGTH:
- Each "text" section MUST be at least 4-5 full sentences (not bullet points).
- Stories MUST be at least 6 sentences with characters and dialogue.
- Dialogues MUST have at least 6 lines (3 turns each speaker).
- mini_quiz questions MUST test what was just taught (not random!)
- The ENTIRE lesson should feel like a full 10-15 minute class, NOT a 2-minute summary.

IDEAL FLOW:
greeting -> header -> text (intro) -> story -> text (explain) -> visual ->
★ mini_quiz (test what was just taught!) ->
curiosity -> encouragement -> header -> text (detail) -> analogy ->
★ mini_quiz (check understanding of analogy!) ->
challenge -> dialogue -> header -> text (practice intro) -> mistake ->
example -> example -> tip ->
★ mini_quiz (final quick check!) ->
challenge -> practice -> tip -> encouragement -> recap -> wrapup

═══ EMOJI RULES (CRITICAL) ═══
- Emojis MUST be relevant to the lesson topic and learning outcomes!
- Grammar topics: 📝✏️🔤📚🧩🔗 (building/connecting things)
- Vocabulary topics: 🗣️💬🎭🌍📖 (speaking/communication)
- Reading/Comprehension: 📖👀🔍🧠💡 (thinking/reading)
- Daily life/Routines: 🏠🍳⏰🚌🎒 (daily objects)
- Travel/Places: ✈️🗺️🏖️🌍🚂 (travel)
- Sports/Health: ⚽💪🏃‍♂️🏆🎯 (sports)
- Nature/Animals: 🌳🐶🦁🌊🌸 (nature)
- Technology: 💻📱🎮🤖🌐 (tech)
- Food: 🍕🍎🧁☕🍴 (food)
- DO NOT use random/unrelated emojis! Match them to the kazanım/topic!

OTHER RULES:
- vocabulary: 6-10 words with phonetic and example.
- quiz: Exactly 5 MCQ. 4 options each. "correct" is 0-based index.
- summary: Exactly 5 key takeaway points.
- tts_text: MUST be 2500-4000 characters! Start with enthusiastic greeting. Cover ALL major concepts from the lesson. Speak like a WARM teacher. Ask questions throughout. Use encouraging phrases. Should take 2-3 minutes to read aloud. No special chars.
- EVERY section should feel alive, warm, student-facing, and visually fun with emojis."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Topic: {konu}"},
            ],
            max_tokens=6000,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        if "sections" not in data:
            return None
        # Defaults
        data.setdefault("vocabulary", [])
        data.setdefault("quiz", [])
        data.setdefault("summary", [])
        data.setdefault("tts_text", "")
        data.setdefault("title", konu[:50])
        return data
    except Exception as e:
        _logger.error(f"Structured AI: {e}")
        return None

# ════════════════════════════════════════════════════════════
# OPENAI TTS
# ════════════════════════════════════════════════════════════
def ai_generate_tts(text: str, voice: str = "nova") -> str | None:
    client = _get_client()
    if not client:
        return None
    try:
        # Limit + split
        max_len = 4000
        if len(text) <= max_len:
            chunks = [text]
        else:
            chunks, cur = [], ""
            for sent in text.replace(". ", ".|").split("|"):
                if len(cur) + len(sent) > max_len:
                    if cur:
                        chunks.append(cur.strip())
                    cur = sent
                else:
                    cur += sent
            if cur.strip():
                chunks.append(cur.strip())

        audio_parts = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            resp = client.audio.speech.create(
                model="tts-1", voice=voice,
                input=chunk.strip(), response_format="mp3",
            )
            audio_parts.append(resp.content)
        if not audio_parts:
            return None
        return base64.b64encode(b"".join(audio_parts)).decode()
    except Exception as e:
        _logger.error(f"TTS: {e}")
        return None

# ════════════════════════════════════════════════════════════
# LESSON STORAGE
# ════════════════════════════════════════════════════════════
def _lessons_dir():
    d = os.path.join(_DATA_DIR, "ai_lessons")
    os.makedirs(d, exist_ok=True)
    return d

def save_lesson(data: dict, grade: int, topic: str, tts_b64: str | None = None):
    rec = {
        "grade": grade, "topic": topic, "lesson": data,
        "tts_b64": tts_b64, "timestamp": time.time(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    fname = f"lesson_{grade}_{int(time.time())}.json"
    with open(os.path.join(_lessons_dir(), fname), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False)
    return fname

def load_saved_lessons(grade: int) -> list:
    d = _lessons_dir()
    lessons = []
    for fname in sorted(os.listdir(d), reverse=True):
        if fname.startswith(f"lesson_{grade}_") and fname.endswith(".json"):
            try:
                with open(os.path.join(d, fname), "r", encoding="utf-8") as f:
                    lessons.append(json.load(f))
            except Exception:
                pass
    return lessons[:20]

# ════════════════════════════════════════════════════════════
# PROGRESS TRACKING
# ════════════════════════════════════════════════════════════
def _progress_path():
    return os.path.join(_DATA_DIR, "ai_progress.json")

def load_progress() -> dict:
    p = _progress_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def update_progress(grade: int, topic: str, quiz_score: float = 0):
    prog = load_progress()
    gk = str(grade)
    if gk not in prog:
        prog[gk] = {"topics": {}, "total_lessons": 0, "total_xp": 0, "streak": 0, "last_date": ""}
    gd = prog[gk]
    gd["topics"][topic[:80]] = {
        "completed": True, "quiz_score": quiz_score,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    gd["total_lessons"] += 1
    xp_earned = int(50 + quiz_score * 0.5)
    gd["total_xp"] = gd.get("total_xp", 0) + xp_earned
    # Streak
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if gd.get("last_date") in (yesterday, today):
        if gd.get("last_date") != today:
            gd["streak"] = gd.get("streak", 0) + 1
    else:
        gd["streak"] = 1
    gd["last_date"] = today
    with open(_progress_path(), "w", encoding="utf-8") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)
    return xp_earned

def get_earned_badges(grade: int) -> list:
    prog = load_progress()
    gd = prog.get(str(grade), {})
    total = gd.get("total_lessons", 0)
    streak = gd.get("streak", 0)
    badges = []
    for b in BADGE_DEFS:
        if "req" in b and total >= b["req"]:
            badges.append(b)
        elif "req_streak" in b and streak >= b["req_streak"]:
            badges.append(b)
    return badges

# ════════════════════════════════════════════════════════════
# PREMIUM SCENE BUILDER
# ════════════════════════════════════════════════════════════
_SCENE_CSS = """
/* font: sistem fontu kullaniliyor */
    *{margin:0;padding:0;box-sizing:border-box}
body{background:#2c1810;overflow:hidden;font-family:'Nunito','Segoe UI',system-ui,sans-serif}
/* ── CLASSROOM LAYOUT ── */
.scene{display:flex;width:100%;height:100vh;
  background:linear-gradient(180deg,#3d2317 0%,#2c1810 100%);padding:6px}
/* ── FULLSCREEN ── */
.fs-btn{position:absolute;top:6px;right:6px;z-index:20;background:rgba(107,63,31,0.85);
  border:1px solid #a07850;color:#fde68a;padding:4px 10px;border-radius:6px;
  cursor:pointer;font-size:11px;font-weight:700;transition:all 0.2s;
  font-family:'Nunito',sans-serif;backdrop-filter:blur(4px)}
.fs-btn:hover{background:rgba(160,120,80,0.9);box-shadow:0 2px 8px rgba(251,191,36,0.3)}
/* ── TEACHER AREA ── */
.t-area{width:190px;min-width:190px;display:flex;flex-direction:column;align-items:center;
  justify-content:flex-end;padding-bottom:10px;
  background:linear-gradient(180deg,#3a2518 0%,#2a1a10 100%);
  border-right:4px solid #5c3a24;position:relative}
.t-area::before{content:'';position:absolute;top:0;right:-6px;width:8px;height:100%;
  background:linear-gradient(90deg,#7a4e30,#5c3a24,#7a4e30);border-radius:2px}
.t-name{color:#fbbf24;font-size:13px;font-weight:700;margin-bottom:6px;
  font-family:'Patrick Hand',cursive;letter-spacing:1px;
  text-shadow:0 1px 3px rgba(0,0,0,0.5)}
/* ── BOARD AREA (wooden frame) ── */
.b-area{flex:1;display:flex;flex-direction:column;padding:6px 8px 6px 10px;
  min-height:0;position:relative}
.board-frame{flex:1;display:flex;flex-direction:column;min-height:0;
  border:12px solid #6b3f1f;border-image:linear-gradient(135deg,#8B5E3C,#6b3f1f,#A0714F,#6b3f1f,#8B5E3C) 12;
  border-radius:4px;position:relative;
  box-shadow:inset 0 0 30px rgba(0,0,0,0.3),0 4px 20px rgba(0,0,0,0.5)}
.board-frame::before{content:'';position:absolute;inset:-12px;
  border:3px solid #a07850;border-radius:6px;pointer-events:none;z-index:1}
.board-frame::after{content:'';position:absolute;bottom:-20px;left:20%;right:20%;height:6px;
  background:linear-gradient(90deg,transparent,#8B5E3C,#A0714F,#8B5E3C,transparent);
  border-radius:0 0 4px 4px}
/* ── BOARD HEADER (chalk tray style) ── */
.b-hdr{background:linear-gradient(135deg,#1a3a2a,#1e4d36);
  padding:8px 14px;display:flex;align-items:center;gap:8px;
  border-bottom:3px solid #2d5a3f}
.b-hdr .dot{width:8px;height:8px;border-radius:50%}
.b-title{color:#fbbf24;font-size:14px;font-weight:700;flex:1;
  font-family:'Patrick Hand',cursive;letter-spacing:0.5px;
  text-shadow:0 1px 2px rgba(0,0,0,0.4)}
.b-badge{background:linear-gradient(135deg,#d97706,#f59e0b);color:#fff;
  padding:3px 12px;border-radius:10px;font-size:11px;font-weight:700;
  box-shadow:0 2px 6px rgba(217,119,6,0.4)}
/* ── BOARD CONTENT (green chalkboard) ── */
.b-cnt{flex:1;background:linear-gradient(180deg,#1a3a2a 0%,#173323 50%,#143020 100%);
  padding:16px 18px;overflow-y:auto;overflow-x:hidden;position:relative;
  min-height:0}
/* ── SCROLLBAR (wooden chalk style) ── */
.b-cnt::-webkit-scrollbar{width:8px}
.b-cnt::-webkit-scrollbar-track{background:rgba(0,0,0,0.2);border-radius:4px}
.b-cnt::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#8B5E3C,#6b3f1f);
  border-radius:4px;border:1px solid rgba(160,120,80,0.3)}
.b-cnt::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#A0714F,#8B5E3C)}
.b-cnt::before{content:'';position:absolute;inset:0;
  background:url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events:none;opacity:0.5}
/* ── SECTIONS (chalk-on-board style) ── */
.sec{opacity:0;transform:translateY(10px);transition:all 0.5s;margin-bottom:10px;position:relative}
.sec.show{opacity:1;transform:translateY(0)}
.s-hdr{background:linear-gradient(135deg,rgba(251,191,36,0.15),rgba(217,119,6,0.1));
  color:#fbbf24;padding:9px 16px;border-radius:8px;font-weight:800;font-size:15px;
  font-family:'Patrick Hand',cursive;letter-spacing:0.5px;
  border-left:4px solid #f59e0b;text-shadow:0 1px 2px rgba(0,0,0,0.3)}
.s-txt{color:#e8efe8;font-size:14px;line-height:1.8;padding:6px 2px;
  text-shadow:0 1px 1px rgba(0,0,0,0.2)}
.s-ex{border-left:3px solid #fbbf24;padding:10px 14px;border-radius:0 8px 8px 0;
  background:rgba(251,191,36,0.08)}
.s-en{color:#fde68a;font-weight:700;font-size:14px;text-shadow:0 1px 1px rgba(0,0,0,0.2)}
.s-tr{color:#a7c4a7;font-style:italic;font-size:13px;margin-top:3px}
.s-dlg{background:rgba(255,255,255,0.04);border-radius:10px;padding:12px;
  border:1px solid rgba(255,255,255,0.08)}
.s-dlg-t{color:#fbbf24;font-weight:700;font-size:13px;margin-bottom:8px;
  font-family:'Patrick Hand',cursive}
.s-bub{background:rgba(255,255,255,0.07);border-radius:12px;padding:6px 14px;margin:4px 0;
  font-size:14px;color:#e8efe8;display:inline-block;max-width:85%;
  border:1px solid rgba(255,255,255,0.06)}
.s-bub b{color:#fde68a}
.s-tip{border-left:3px solid #4ade80;padding:10px 14px;
  background:rgba(74,222,128,0.06);border-radius:0 8px 8px 0;
  color:#bbf7d0;font-size:14px;line-height:1.7}
.s-prc{border:2px dashed rgba(251,146,60,0.4);border-radius:10px;padding:12px 14px;
  color:#fed7aa;font-size:14px;line-height:1.7;
  background:rgba(251,146,60,0.06)}
.s-story{background:linear-gradient(135deg,rgba(167,139,250,0.08),rgba(139,92,246,0.12));
  border:1px solid rgba(167,139,250,0.25);border-radius:12px;padding:16px 18px;position:relative}
.s-story-t{color:#c4b5fd;font-weight:800;font-size:14px;margin-bottom:10px;
  font-family:'Patrick Hand',cursive}
.s-story-cnt{color:#e8efe8;font-size:14px;line-height:1.9;font-style:italic;
  border-left:2px solid rgba(167,139,250,0.35);padding-left:14px}
.s-curiosity{background:linear-gradient(135deg,rgba(251,191,36,0.08),rgba(234,179,8,0.12));
  border:1px solid rgba(251,191,36,0.3);border-radius:12px;padding:16px 18px}
.s-curiosity-lbl{color:#fbbf24;font-weight:800;font-size:12px;text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:8px;font-family:'Patrick Hand',cursive}
.s-curiosity-cnt{color:#fef9c3;font-size:15px;line-height:1.8;font-weight:600;
  text-shadow:0 1px 1px rgba(0,0,0,0.2)}
.s-analogy{background:linear-gradient(135deg,rgba(34,211,238,0.06),rgba(6,182,212,0.1));
  border:1px solid rgba(34,211,238,0.25);border-radius:12px;padding:16px 18px}
.s-analogy-map{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.s-analogy-box{background:rgba(34,211,238,0.12);border:1px solid rgba(34,211,238,0.3);
  border-radius:8px;padding:8px 14px;color:#a5f3fc;font-weight:700;font-size:14px;
  font-family:'Patrick Hand',cursive}
.s-analogy-arrow{color:#22d3ee;font-size:20px;font-weight:900}
.s-analogy-cnt{color:#e8efe8;font-size:14px;line-height:1.8}
.s-challenge{background:linear-gradient(135deg,rgba(251,146,60,0.06),rgba(249,115,22,0.08));
  border:2px solid rgba(251,146,60,0.25);border-radius:12px;padding:16px 18px}
.s-challenge-q{color:#fed7aa;font-weight:700;font-size:15px;line-height:1.7;margin-bottom:10px;
  font-family:'Patrick Hand',cursive}
.s-challenge-hint{color:#fde68a;font-size:13px;padding:8px 12px;
  background:rgba(251,191,36,0.08);border-radius:8px;margin-bottom:10px;
  border-left:2px solid #f59e0b}
.s-challenge-ans{color:#bbf7d0;font-size:14px;padding:10px 14px;
  background:rgba(74,222,128,0.06);border-radius:8px;border-left:2px solid #4ade80}
.s-challenge-reveal{color:#a7c4a7;font-size:12px;text-align:center;margin-top:6px;
  font-style:italic;cursor:pointer}
.s-mistake{background:linear-gradient(135deg,rgba(248,113,113,0.06),rgba(74,222,128,0.04));
  border:1px solid rgba(248,113,113,0.2);border-radius:12px;padding:16px 18px}
.s-mistake-row{display:flex;gap:12px;margin-bottom:10px;flex-wrap:wrap}
.s-mistake-wrong{flex:1;min-width:120px;background:rgba(248,113,113,0.08);
  border:1px solid rgba(248,113,113,0.25);border-radius:8px;padding:10px 14px}
.s-mistake-wrong::before{content:'\\274C WRONG';display:block;color:#f87171;font-weight:800;
  font-size:11px;margin-bottom:6px;font-family:'Patrick Hand',cursive}
.s-mistake-wrong-t{color:#fecaca;font-size:14px;line-height:1.6}
.s-mistake-right{flex:1;min-width:120px;background:rgba(74,222,128,0.08);
  border:1px solid rgba(74,222,128,0.25);border-radius:8px;padding:10px 14px}
.s-mistake-right::before{content:'\\2705 CORRECT';display:block;color:#4ade80;font-weight:800;
  font-size:11px;margin-bottom:6px;font-family:'Patrick Hand',cursive}
.s-mistake-right-t{color:#bbf7d0;font-size:14px;line-height:1.6}
.s-mistake-exp{color:#a7c4a7;font-size:13px;line-height:1.6;margin-top:8px;
  padding-top:8px;border-top:1px solid rgba(255,255,255,0.08)}
.s-mnemonic{background:linear-gradient(135deg,rgba(244,114,182,0.08),rgba(236,72,153,0.12));
  border:1px solid rgba(244,114,182,0.25);border-radius:12px;padding:16px 18px}
.s-mnemonic-lbl{color:#f9a8d4;font-weight:800;font-size:12px;text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:8px;font-family:'Patrick Hand',cursive}
.s-mnemonic-tech{display:inline-block;background:rgba(244,114,182,0.15);color:#fbcfe8;
  padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;margin-left:6px}
.s-mnemonic-cnt{color:#e8efe8;font-size:14px;line-height:1.8}
.s-mnemonic-remember{background:linear-gradient(135deg,rgba(244,114,182,0.1),rgba(244,114,182,0.15));
  border:1px dashed rgba(244,114,182,0.3);border-radius:8px;padding:10px 14px;margin-top:10px;
  color:#fbcfe8;font-weight:700;font-size:15px;text-align:center;
  font-family:'Patrick Hand',cursive}
.s-recap{background:linear-gradient(135deg,rgba(56,189,248,0.08),rgba(14,165,233,0.12));
  border:2px solid rgba(56,189,248,0.25);border-radius:12px;padding:18px}
.s-recap-t{color:#7dd3fc;font-weight:800;font-size:15px;margin-bottom:12px;
  font-family:'Patrick Hand',cursive}
.s-recap-pts{list-style:none;padding:0;margin:0}
.s-recap-pts li{color:#e8efe8;font-size:14px;line-height:1.8;padding:5px 0 5px 28px;position:relative}
.s-recap-pts li::before{content:'\\2705';position:absolute;left:0;top:6px;font-size:13px}
.s-realq{background:linear-gradient(135deg,rgba(167,139,250,0.06),rgba(139,92,246,0.1));
  border:1px solid rgba(167,139,250,0.2);border-radius:12px;padding:16px 18px}
.s-realq-q{background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.2);
  border-radius:10px;padding:10px 16px;color:#ddd6fe;font-size:14px;font-weight:600;
  font-style:italic;margin-bottom:12px}
.s-realq-a{color:#e8efe8;font-size:14px;line-height:1.8;padding-left:14px;
  border-left:2px solid rgba(167,139,250,0.35)}
/* ── CONTROLS (below board, wooden tray) ── */
.ctrl-tray{background:linear-gradient(180deg,#6b3f1f,#5c3520,#4a2a18);
  padding:4px 14px 6px;border-radius:0 0 4px 4px;
  box-shadow:inset 0 2px 4px rgba(0,0,0,0.3)}
.tl-wrap{display:flex;align-items:center;gap:8px;padding:4px 0}
.tl-time{color:#d4a574;font-size:11px;min-width:32px;font-family:monospace}
.tl-bar{flex:1;height:5px;background:rgba(255,255,255,0.1);border-radius:3px;
  cursor:pointer;position:relative}
.tl-fill{height:100%;background:linear-gradient(90deg,#f59e0b,#fbbf24);border-radius:3px;
  transition:width 0.3s;width:0;box-shadow:0 0 6px rgba(251,191,36,0.4)}
.ctrls{display:flex;gap:6px;padding:4px 0;align-items:center;justify-content:center;flex-wrap:wrap}
.cb{background:linear-gradient(135deg,#3a2518,#4a3020);
  border:1px solid rgba(251,191,36,0.3);color:#fde68a;
  padding:5px 14px;border-radius:8px;cursor:pointer;font-size:12px;
  font-weight:700;transition:all 0.2s;font-family:'Nunito',sans-serif}
.cb:hover{background:linear-gradient(135deg,#4a3020,#5a3828);border-color:#f59e0b;
  box-shadow:0 2px 8px rgba(251,191,36,0.2)}
.cb.on{background:linear-gradient(135deg,#d97706,#f59e0b);color:#fff;
  box-shadow:0 2px 8px rgba(217,119,6,0.4)}
.vol-w{display:flex;align-items:center;gap:4px;margin-left:6px;color:#d4a574;font-size:12px}
.vol-w input[type=range]{width:55px;height:3px;accent-color:#f59e0b}
.sub-bar{text-align:center;color:#a7c4a7;font-size:13px;min-height:20px;padding:4px 0;
  font-style:italic;transition:all 0.3s;font-family:'Patrick Hand',cursive}
.sec-nav{display:flex;gap:4px;justify-content:center;padding:4px 0;flex-wrap:wrap}
.sec-dot{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,0.12);
  cursor:pointer;transition:all 0.3s}
.sec-dot.done{background:rgba(74,222,128,0.5)}
.sec-dot.current{background:#fbbf24;box-shadow:0 0 8px rgba(251,191,36,0.5);transform:scale(1.4)}
.sec-dot:hover{background:rgba(251,191,36,0.6);transform:scale(1.3)}
/* ── Section entry animations ── */
.sec.enter-slide{opacity:0;transform:translateX(-40px) scale(0.97)}
.sec.enter-slide.show{opacity:1;transform:translateX(0) scale(1)}
.sec.enter-zoom{opacity:0;transform:scale(0.7)}
.sec.enter-zoom.show{opacity:1;transform:scale(1)}
.sec.enter-bounce{opacity:0;transform:translateY(30px)}
.sec.enter-bounce.show{opacity:1;transform:translateY(0);animation:secBounce 0.6s ease}
@keyframes secBounce{0%{transform:translateY(30px)}40%{transform:translateY(-8px)}60%{transform:translateY(4px)}100%{transform:translateY(0)}}
.sec.enter-flip{opacity:0;transform:perspective(600px) rotateX(90deg)}
.sec.enter-flip.show{opacity:1;transform:perspective(600px) rotateX(0deg)}
.sec.enter-fade-up{opacity:0;transform:translateY(20px) scale(0.98)}
.sec.enter-fade-up.show{opacity:1;transform:translateY(0) scale(1)}
.typewriter-cursor{display:inline-block;width:2px;height:1em;background:#fbbf24;margin-left:2px;
  animation:twBlink 0.7s step-end infinite;vertical-align:text-bottom}
@keyframes twBlink{0%,100%{opacity:1}50%{opacity:0}}
.sec.active-sec::after{content:'';position:absolute;inset:-2px;border-radius:14px;
  border:1px solid rgba(251,191,36,0.25);pointer-events:none;
  animation:activeGlow 2s ease-in-out infinite}
@keyframes activeGlow{0%,100%{box-shadow:0 0 0 rgba(251,191,36,0)}50%{box-shadow:0 0 12px rgba(251,191,36,0.12)}}
.sec.past-sec{opacity:0.55;filter:brightness(0.8);transition:opacity 0.5s,filter 0.5s}
.sec.past-sec:hover{opacity:1;filter:brightness(1)}
.mood-particle{position:absolute;pointer-events:none;font-size:16px;opacity:0;z-index:5;
  animation:moodFloat 3s ease-out forwards}
@keyframes moodFloat{0%{opacity:0.8;transform:translateY(0) scale(1)}100%{opacity:0;transform:translateY(-60px) scale(0.3)}}
.flip-card{perspective:800px;cursor:pointer;min-height:80px}
.flip-card-inner{position:relative;width:100%;height:100%;
  transition:transform 0.6s cubic-bezier(0.4,0,0.2,1);transform-style:preserve-3d}
.flip-card.flipped .flip-card-inner{transform:rotateY(180deg)}
.flip-card-front,.flip-card-back{backface-visibility:hidden;border-radius:10px;padding:14px 18px}
.flip-card-back{transform:rotateY(180deg);position:absolute;top:0;left:0;right:0}
/* ── NEW SECTION TYPES ── */
.s-greeting{background:linear-gradient(135deg,rgba(167,139,250,0.1),rgba(99,102,241,0.14));
  border:2px solid rgba(167,139,250,0.3);border-radius:16px;padding:20px 22px;text-align:center}
.s-greeting-wave{font-size:40px;margin-bottom:10px;animation:waveHand 1.5s ease-in-out 2}
@keyframes waveHand{0%,100%{transform:rotate(0deg)}15%{transform:rotate(14deg)}30%{transform:rotate(-8deg)}45%{transform:rotate(14deg)}60%{transform:rotate(-4deg)}75%{transform:rotate(10deg)}}
.s-greeting-msg{color:#ddd6fe;font-size:17px;font-weight:700;line-height:1.6;margin-bottom:10px;
  font-family:'Patrick Hand',cursive;text-shadow:0 1px 2px rgba(0,0,0,0.3)}
.s-greeting-topic{color:#e8efe8;font-size:15px;line-height:1.7;font-style:italic;
  padding:12px 16px;background:rgba(167,139,250,0.08);border-radius:10px;margin-top:8px}
.s-visual{background:linear-gradient(135deg,rgba(52,211,153,0.08),rgba(16,185,129,0.12));
  border:1px solid rgba(52,211,153,0.3);border-radius:14px;padding:18px 20px}
.s-visual-emoji{font-size:46px;text-align:center;margin-bottom:12px;line-height:1.4}
.s-visual-title{color:#6ee7b7;font-weight:800;font-size:14px;text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:10px;text-align:center;
  font-family:'Patrick Hand',cursive}
.s-visual-cnt{color:#e8efe8;font-size:15px;line-height:2;text-align:center;font-weight:600;
  text-shadow:0 1px 1px rgba(0,0,0,0.2)}
.s-encourage{background:linear-gradient(135deg,rgba(251,191,36,0.08),rgba(245,158,11,0.12));
  border:2px dashed rgba(251,191,36,0.35);border-radius:14px;padding:16px 20px;text-align:center}
.s-encourage-icon{font-size:36px;margin-bottom:8px}
.s-encourage-msg{color:#fef3c7;font-size:16px;font-weight:700;line-height:1.6;
  font-family:'Patrick Hand',cursive;text-shadow:0 1px 2px rgba(0,0,0,0.3)}
/* ── MINI QUIZ (inline during lesson) ── */
.s-miniq{background:linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.14));
  border:2px solid rgba(99,102,241,0.35);border-radius:14px;padding:18px 20px}
.s-miniq-label{color:#a78bfa;font-weight:800;font-size:12px;text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:8px;font-family:'Patrick Hand',cursive}
.s-miniq-q{color:#e8efe8;font-size:15px;font-weight:700;line-height:1.7;margin-bottom:12px;
  font-family:'Patrick Hand',cursive}
.s-miniq-opt{display:block;width:100%;text-align:left;background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:10px 16px;margin:5px 0;
  color:#e8efe8;font-size:14px;font-weight:600;cursor:pointer;transition:all 0.25s;
  font-family:'Nunito',sans-serif}
.s-miniq-opt:hover{background:rgba(167,139,250,0.15);border-color:rgba(167,139,250,0.4);
  transform:translateX(4px)}
.s-miniq-opt.correct{background:rgba(74,222,128,0.15)!important;
  border-color:#4ade80!important;color:#bbf7d0!important}
.s-miniq-opt.wrong{background:rgba(248,113,113,0.12)!important;
  border-color:#f87171!important;color:#fecaca!important;opacity:0.7}
.s-miniq-opt.disabled{pointer-events:none;opacity:0.6}
.s-miniq-fb{margin-top:10px;padding:10px 14px;border-radius:10px;font-size:14px;
  font-weight:600;line-height:1.6;display:none}
.s-miniq-fb.show{display:block;animation:fbPop 0.4s ease}
@keyframes fbPop{0%{opacity:0;transform:scale(0.9)}100%{opacity:1;transform:scale(1)}}
.s-miniq-fb.ok{background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.3);color:#bbf7d0}
.s-miniq-fb.no{background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.3);color:#fecaca}
/* ── WRAPUP (end of lesson) ── */
.s-wrapup{background:linear-gradient(135deg,rgba(251,191,36,0.1),rgba(217,119,6,0.08));
  border:3px solid rgba(251,191,36,0.35);border-radius:16px;padding:20px 22px;position:relative;
  overflow:hidden}
.s-wrapup::before{content:'🎓';position:absolute;top:-10px;right:-10px;font-size:80px;
  opacity:0.06;pointer-events:none}
.s-wrapup-title{color:#fbbf24;font-weight:800;font-size:18px;margin-bottom:14px;
  font-family:'Patrick Hand',cursive;text-align:center;
  text-shadow:0 2px 4px rgba(0,0,0,0.3)}
.s-wrapup-list{list-style:none;padding:0;margin:0 0 14px 0}
.s-wrapup-list li{color:#e8efe8;font-size:14px;line-height:1.8;padding:6px 0 6px 30px;
  position:relative;border-bottom:1px solid rgba(255,255,255,0.04)}
.s-wrapup-list li::before{content:'🌟';position:absolute;left:0;top:7px;font-size:14px}
.s-wrapup-msg{background:rgba(251,191,36,0.08);border-radius:12px;padding:14px 18px;
  text-align:center;margin-top:10px}
.s-wrapup-msg-text{color:#fef3c7;font-size:15px;font-weight:600;line-height:1.7;
  font-family:'Patrick Hand',cursive}
.s-wrapup-hw{margin-top:10px;padding:10px 16px;background:rgba(99,102,241,0.08);
  border-radius:10px;border-left:3px solid #a78bfa}
.s-wrapup-hw-text{color:#ddd6fe;font-size:13px;font-weight:600}
.s-wrapup-confetti{position:absolute;pointer-events:none;font-size:18px;
  animation:confettiFall 3s ease-out forwards;opacity:0}
@keyframes confettiFall{0%{opacity:1;transform:translateY(-20px) rotate(0deg)}
  100%{opacity:0;transform:translateY(80px) rotate(360deg)}}
/* ── CHALK DUST on board edges ── */
.b-cnt::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent)}
"""

_SCENE_JS_TEACHER = """
const cv=document.getElementById('tchr');
const ctx=cv.getContext('2d');
const W=cv.width,H=cv.height;
let breathPhase=0,mouthOpen=0,blinkTimer=0,eyesClosed=false,gestureAngle=0,
    animPlaying=true,pointingAt=false,thinkingPose=false,talkCounter=0;
let eyebrowRaise=0,smileAmount=0,surpriseAmount=0,headTilt=0;
let targetEyebrow=0,targetSmile=0,targetSurprise=0,targetHeadTilt=0;
function setExpression(type){
  switch(type){
    case 'greeting':case 'encouragement':case 'wrapup':targetEyebrow=3;targetSmile=0.8;targetSurprise=0.2;targetHeadTilt=0;break;
    case 'mini_quiz':targetEyebrow=5;targetSmile=0.2;targetSurprise=0.6;targetHeadTilt=0.06;break;
    case 'visual':targetEyebrow=2;targetSmile=0.5;targetSurprise=0.4;targetHeadTilt=0.03;break;
    case 'curiosity':case 'tip':targetEyebrow=4;targetSmile=0.3;targetSurprise=0.5;targetHeadTilt=0.05;break;
    case 'story':case 'analogy':targetEyebrow=1;targetSmile=0.6;targetSurprise=0;targetHeadTilt=-0.03;break;
    case 'challenge':case 'real_question':targetEyebrow=3;targetSmile=0;targetSurprise=0.3;targetHeadTilt=0.04;break;
    case 'mistake':targetEyebrow=-2;targetSmile=0;targetSurprise=0;targetHeadTilt=-0.02;break;
    case 'recap':case 'mnemonic':targetEyebrow=2;targetSmile=0.4;targetSurprise=0;targetHeadTilt=0;break;
    default:targetEyebrow=0;targetSmile=0.2;targetSurprise=0;targetHeadTilt=0;
  }
}
function drawTeacher(){
  ctx.clearRect(0,0,W,H);
  const cx=W/2,by=H-8,bo=Math.sin(breathPhase)*1.5;
  eyebrowRaise+=(targetEyebrow-eyebrowRaise)*0.08;
  smileAmount+=(targetSmile-smileAmount)*0.06;
  surpriseAmount+=(targetSurprise-surpriseAmount)*0.06;
  headTilt+=(targetHeadTilt-headTilt)*0.04;
  ctx.fillStyle=SHIRT;ctx.beginPath();
  ctx.moveTo(cx-32,by-115+bo);ctx.quadraticCurveTo(cx-36,by-55,cx-28,by-8);
  ctx.lineTo(cx+28,by-8);ctx.quadraticCurveTo(cx+36,by-55,cx+32,by-115+bo);
  ctx.closePath();ctx.fill();
  if(!IS_FEMALE){ctx.fillStyle='#1e40af';ctx.beginPath();
    ctx.moveTo(cx-10,by-115+bo);ctx.lineTo(cx,by-98+bo);ctx.lineTo(cx+10,by-115+bo);
    ctx.closePath();ctx.fill();
    ctx.fillStyle='#dc2626';ctx.beginPath();
    ctx.moveTo(cx-4,by-113+bo);ctx.lineTo(cx,by-72+bo);ctx.lineTo(cx+4,by-113+bo);
    ctx.closePath();ctx.fill();
  }else{ctx.strokeStyle='#e879f9';ctx.lineWidth=2;ctx.beginPath();
    ctx.arc(cx,by-110+bo,10,0.2,Math.PI-0.2);ctx.stroke();}
  ctx.fillStyle=SKIN;ctx.fillRect(cx-7,by-130+bo,14,18);
  const hy=by-168+bo;
  ctx.fillStyle=SKIN;ctx.beginPath();ctx.ellipse(cx,hy,26,30,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=HAIR;
  if(IS_FEMALE){ctx.beginPath();ctx.ellipse(cx,hy-7,28,26,0,Math.PI,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx-26,hy+5,7,22,0.2,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx+26,hy+5,7,22,-0.2,0,Math.PI*2);ctx.fill();
  }else{ctx.beginPath();ctx.ellipse(cx,hy-9,27,20,0,Math.PI,Math.PI*2);ctx.fill();}
  const ey=hy-2,es=9;
  if(eyesClosed){ctx.strokeStyle='#333';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(cx-es-4,ey);ctx.lineTo(cx-es+4,ey);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx+es-4,ey);ctx.lineTo(cx+es+4,ey);ctx.stroke();
  }else{ctx.fillStyle='#fff';
    ctx.beginPath();ctx.ellipse(cx-es,ey,5,4,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(cx+es,ey,5,4,0,0,Math.PI*2);ctx.fill();
    const po=pointingAt?2:1;ctx.fillStyle='#2C1810';
    ctx.beginPath();ctx.arc(cx-es+po,ey,2.2,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+es+po,ey,2.2,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,0.6)';
    ctx.beginPath();ctx.arc(cx-es+po-1,ey-1,0.8,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+es+po-1,ey-1,0.8,0,Math.PI*2);ctx.fill();}
  ctx.strokeStyle=HAIR;ctx.lineWidth=1.8;
  ctx.beginPath();ctx.moveTo(cx-es-5,ey-7);ctx.quadraticCurveTo(cx-es,ey-10,cx-es+5,ey-7);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx+es-5,ey-7);ctx.quadraticCurveTo(cx+es,ey-10,cx+es+5,ey-7);ctx.stroke();
  if(!IS_FEMALE){ctx.strokeStyle='#555';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.roundRect(cx-es-7,ey-6,14,12,3);ctx.stroke();
    ctx.beginPath();ctx.roundRect(cx+es-7,ey-6,14,12,3);ctx.stroke();
    ctx.beginPath();ctx.moveTo(cx-es+7,ey);ctx.lineTo(cx+es-7,ey);ctx.stroke();}
  const my=hy+14;
  if(mouthOpen>0.3){ctx.fillStyle='#c0392b';ctx.beginPath();
    ctx.ellipse(cx,my,7,2.5+mouthOpen*3.5,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';ctx.fillRect(cx-4,my-2,8,2);
  }else{ctx.strokeStyle='#c0392b';ctx.lineWidth=2;ctx.beginPath();
    ctx.arc(cx,my-2,7,0.15,Math.PI-0.15);ctx.stroke();}
  ctx.fillStyle='rgba(255,150,150,0.15)';
  ctx.beginPath();ctx.ellipse(cx-16,my-2,5,3,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(cx+16,my-2,5,3,0,0,Math.PI*2);ctx.fill();
  const ay=by-110+bo;ctx.strokeStyle=SHIRT;ctx.lineWidth=11;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(cx-32,ay);
  if(thinkingPose){ctx.quadraticCurveTo(cx-45,ay+18,cx-18,hy+22);}
  else{const ls=Math.sin(gestureAngle)*4;ctx.quadraticCurveTo(cx-50,ay+28+ls,cx-40,ay+55+ls);}
  ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx+32,ay);
  if(pointingAt){ctx.quadraticCurveTo(cx+55,ay-18,cx+82,ay-35);
    ctx.strokeStyle=SKIN;ctx.lineWidth=3;ctx.beginPath();
    ctx.moveTo(cx+80,ay-37);ctx.lineTo(cx+92,ay-42);ctx.stroke();
    ctx.strokeStyle=SHIRT;ctx.lineWidth=11;
  }else{const rs=Math.sin(gestureAngle+1)*6;
    ctx.quadraticCurveTo(cx+50,ay+22+rs,cx+40,ay+50+rs);}
  ctx.stroke();
  ctx.fillStyle=SKIN;
  if(thinkingPose){ctx.beginPath();ctx.arc(cx-18,hy+22,5,0,Math.PI*2);ctx.fill();}
  else if(!pointingAt){const ls=Math.sin(gestureAngle)*4;const rs=Math.sin(gestureAngle+1)*6;
    ctx.beginPath();ctx.arc(cx-40,ay+55+ls,5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(cx+40,ay+50+rs,5,0,Math.PI*2);ctx.fill();}
}
function updateAnim(){
  breathPhase+=0.03;blinkTimer++;
  if(blinkTimer>180+Math.random()*120){eyesClosed=true;blinkTimer=0;setTimeout(()=>{eyesClosed=false},150);}
  if(animPlaying){
    talkCounter++;mouthOpen=Math.abs(Math.sin(talkCounter*0.3))*0.8;gestureAngle+=0.04;
    const f=talkCounter%200;
    if(f<60){pointingAt=true;thinkingPose=false;}
    else if(f<80){pointingAt=false;thinkingPose=true;}
    else{pointingAt=false;thinkingPose=false;}
  }else{mouthOpen*=0.9;pointingAt=false;thinkingPose=false;}
  drawTeacher();requestAnimationFrame(updateAnim);
}
updateAnim();
"""

_SCENE_JS_BOARD = """
var _sfx={};
(function(){
  var AC=window.AudioContext||window.webkitAudioContext;
  if(!AC)return;var actx=new AC();
  function mkBeep(freq,dur,type){
    return function(){try{var o=actx.createOscillator(),g=actx.createGain();o.type=type||'sine';o.frequency.value=freq;g.gain.setValueAtTime(0.08,actx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,actx.currentTime+dur);o.connect(g);g.connect(actx.destination);o.start();o.stop(actx.currentTime+dur);}catch(e){}};
  }
  _sfx.pop=mkBeep(880,0.1,'sine');_sfx.ding=mkBeep(1200,0.15,'sine');
  _sfx.transition=mkBeep(440,0.08,'sine');_sfx.reveal=mkBeep(600,0.12,'triangle');
  _sfx.correct=function(){mkBeep(523,0.1,'sine')();setTimeout(function(){mkBeep(659,0.1,'sine')();},100);setTimeout(function(){mkBeep(784,0.15,'sine')();},200);};
})();
var _moodEmojis={greeting:['\\uD83D\\uDC4B','\\uD83C\\uDF1F','\\uD83C\\uDF89','\\u2728','\\uD83D\\uDE0A'],visual:['\\uD83C\\uDFA8','\\u2728','\\uD83D\\uDC40','\\uD83C\\uDF08','\\uD83D\\uDDBC'],encouragement:['\\uD83C\\uDF1F','\\uD83D\\uDCAA','\\uD83C\\uDF89','\\uD83D\\uDC4F','\\u2728'],mini_quiz:['\\uD83E\\uDDD0','\\u2753','\\uD83C\\uDFAF','\\uD83D\\uDCA1','\\u2705'],wrapup:['\\uD83C\\uDF93','\\uD83C\\uDF1F','\\uD83C\\uDFC6','\\uD83D\\uDC4B','\\uD83C\\uDF89'],story:['\\uD83D\\uDCD6','\\uD83C\\uDFAC','\\u2728','\\uD83C\\uDF1F'],curiosity:['\\uD83D\\uDCA1','\\u2B50','\\uD83E\\uDD2F','\\uD83E\\uDDE0'],challenge:['\\uD83C\\uDFAF','\\uD83E\\uDD14','\\u2753','\\uD83D\\uDCAA'],mistake:['\\u26A0\\uFE0F','\\u274C','\\u2705'],mnemonic:['\\uD83E\\uDDE0','\\uD83D\\uDCA0','\\uD83D\\uDD11'],recap:['\\uD83D\\uDCCB','\\u2705','\\uD83D\\uDCCC','\\uD83C\\uDFC1'],tip:['\\uD83D\\uDCA1','\\u2728','\\u261D'],dialogue:['\\uD83D\\uDCAC','\\uD83C\\uDFAD','\\uD83D\\uDDE3'],example:['\\u25B6','\\uD83D\\uDCDD','\\u2705'],practice:['\\u270F','\\uD83C\\uDFAF','\\uD83D\\uDCAA']};
function spawnMoodParticles(el,type){var emojis=_moodEmojis[type]||['\\u2728'];for(var i=0;i<3;i++){var p=document.createElement('span');p.className='mood-particle';p.textContent=emojis[Math.floor(Math.random()*emojis.length)];p.style.left=(10+Math.random()*80)+'%';p.style.top=(Math.random()*40)+'%';p.style.animationDelay=(i*0.3)+'s';el.style.position='relative';el.appendChild(p);setTimeout(function(){p.remove();},3500);}}
function typewriterEffect(el,text,speed){if(!el||!text)return;var spd=speed||25;el.textContent='';var cursor=document.createElement('span');cursor.className='typewriter-cursor';el.appendChild(cursor);var idx=0;function typeChar(){if(idx<text.length){el.insertBefore(document.createTextNode(text[idx]),cursor);idx++;setTimeout(typeChar,spd);}else{setTimeout(function(){cursor.remove();},1500);}}typeChar();}
function handleMiniQuiz(btn){
  var mqid=btn.getAttribute('data-mqid');
  var idx=parseInt(btn.getAttribute('data-idx'));
  var correct=parseInt(btn.getAttribute('data-correct'));
  var fbOk=btn.getAttribute('data-fb-ok');
  var fbNo=btn.getAttribute('data-fb-no');
  var allBtns=document.querySelectorAll('[data-mqid="'+mqid+'"]');
  allBtns.forEach(function(b){b.classList.add('disabled');
    if(parseInt(b.getAttribute('data-idx'))===correct)b.classList.add('correct');
  });
  var fbEl=document.getElementById('fb_'+mqid);
  if(idx===correct){
    btn.classList.add('correct');
    fbEl.className='s-miniq-fb show ok';fbEl.textContent=fbOk;
    _sfx.correct&&_sfx.correct();
    spawnMoodParticles(btn.parentElement,'mini_quiz');
  }else{
    btn.classList.add('wrong');
    fbEl.className='s-miniq-fb show no';fbEl.textContent=fbNo;
    _sfx.pop&&_sfx.pop();
  }
}
function spawnWrapupConfetti(el){
  var confetti=['\\uD83C\\uDF89','\\uD83C\\uDF8A','\\u2B50','\\uD83C\\uDF1F','\\uD83C\\uDFC6','\\uD83D\\uDC4F','\\u2728'];
  for(var i=0;i<12;i++){
    var c=document.createElement('span');c.className='s-wrapup-confetti';
    c.textContent=confetti[Math.floor(Math.random()*confetti.length)];
    c.style.left=(5+Math.random()*90)+'%';c.style.top='-10px';
    c.style.animationDelay=(i*0.15)+'s';c.style.opacity='1';
    el.appendChild(c);setTimeout(function(x){x.remove();},(i*150)+3500,c);
  }
}
function setTeacherPose(type){if(typeof setExpression==='function')setExpression(type);switch(type){case 'greeting':case 'encouragement':case 'wrapup':pointingAt=false;thinkingPose=false;gestureAngle+=1;break;case 'mini_quiz':pointingAt=true;thinkingPose=false;break;case 'visual':case 'example':pointingAt=true;thinkingPose=false;break;case 'challenge':case 'real_question':pointingAt=false;thinkingPose=true;break;case 'story':case 'analogy':pointingAt=false;thinkingPose=false;gestureAngle+=0.5;break;case 'curiosity':case 'tip':pointingAt=true;thinkingPose=false;break;default:pointingAt=false;thinkingPose=false;}}
var _entryMap={greeting:'enter-zoom',visual:'enter-bounce',encouragement:'enter-zoom',mini_quiz:'enter-zoom',wrapup:'enter-zoom',header:'enter-fade-up',text:'enter-fade-up',story:'enter-slide',analogy:'enter-slide',challenge:'enter-zoom',practice:'enter-zoom',tip:'enter-bounce',curiosity:'enter-bounce',mistake:'enter-flip',mnemonic:'enter-slide',recap:'enter-fade-up',real_question:'enter-slide',dialogue:'enter-slide'};
var secNavEl=document.getElementById('secnav');
function buildSecNav(){if(!secNavEl)return;secNavEl.innerHTML='';for(var i=0;i<sections.length;i++){var dot=document.createElement('span');dot.className='sec-dot';secNavEl.appendChild(dot);}}
function updateSecNav(idx){if(!secNavEl)return;var dots=secNavEl.querySelectorAll('.sec-dot');dots.forEach(function(d,i){d.classList.remove('current','done');if(i<idx)d.classList.add('done');if(i===idx)d.classList.add('current');});}
buildSecNav();
const board=document.getElementById('board');
const aud=document.getElementById('aud');
const subBar=document.getElementById('subbar');
let secIdx=0,speed=1;
let timestamps=[];
let cumTime=0.8;
for(let s of sections){
  timestamps.push(cumTime);
  let txt=s.text||s.content||s.message||s.en||s.question||'';
  if(s.topic_intro) txt+=' '+s.topic_intro;
  if(s.lines) txt=s.lines.map(l=>l.text).join(' ');
  if(s.source) txt+='. Like '+s.source+': '+s.target;
  if(s.answer) txt+=' '+s.answer;
  if(s.wrong) txt+='Wrong: '+s.wrong+'. Correct: '+(s.correct||'');
  if(s.hint) txt+=' '+s.hint;
  if(s.learned) txt+=' '+s.learned.join(' ');
  if(s.teacher_message) txt+=' '+s.teacher_message;
  if(s.options&&s.type==='mini_quiz') txt+=' '+s.options.join(' ');
  if(s.feedback_correct) txt+=' '+s.feedback_correct;
  let wc=txt.split(/\\s+/).filter(w=>w).length;
  var extraDelay=0;
  if(s.type==='mini_quiz') extraDelay=5;
  if(s.type==='wrapup') extraDelay=3;
  cumTime+=Math.max(2,wc/2.5)+0.4+extraDelay;
}
function mkSec(s){
  let d=document.createElement('div');
  var entryClass=_entryMap[s.type]||'enter-fade-up';
  d.className='sec '+entryClass;let h='';
  switch(s.type){
    case 'greeting':
      h='<div class="s-greeting"><div class="s-greeting-wave">\\uD83D\\uDC4B</div>'
        +'<div class="s-greeting-msg">'+(s.message||'Hey everyone! Welcome to class!')+'</div>'
        +(s.topic_intro?'<div class="s-greeting-topic">'+s.topic_intro+'</div>':'')
        +'</div>';break;
    case 'visual':
      h='<div class="s-visual"><div class="s-visual-emoji">'+(s.emoji||'\\u2728')+'</div>'
        +'<div class="s-visual-title">'+(s.title||'Visual Concept')+'</div>'
        +'<div class="s-visual-cnt">'+(s.content||'')+'</div></div>';break;
    case 'encouragement':
      h='<div class="s-encourage"><div class="s-encourage-icon">\\uD83C\\uDF1F</div>'
        +'<div class="s-encourage-msg">'+(s.message||s.content||'You\\'re doing great!')+'</div></div>';break;
    case 'mini_quiz':
      var mqid='mq_'+Math.random().toString(36).substr(2,6);
      var mqCorrect=s.correct||0;
      var mqOpts=s.options||[];
      h='<div class="s-miniq"><div class="s-miniq-label">\\uD83E\\uDDD0 Quick Check!</div>'
        +'<div class="s-miniq-q">'+(s.question||'')+'</div>';
      for(var oi=0;oi<mqOpts.length;oi++){
        h+='<button class="s-miniq-opt" data-mqid="'+mqid+'" data-idx="'+oi+'" data-correct="'+mqCorrect+'"'
          +' data-fb-ok="'+(s.feedback_correct||'\\uD83C\\uDF89 Correct!').replace(/"/g,'&quot;')+'"'
          +' data-fb-no="'+(s.feedback_wrong||'\\uD83E\\uDD14 Not quite!').replace(/"/g,'&quot;')+'"'
          +' onclick="handleMiniQuiz(this)">'
          +String.fromCharCode(65+oi)+') '+mqOpts[oi]+'</button>';
      }
      h+='<div class="s-miniq-fb" id="fb_'+mqid+'"></div></div>';break;
    case 'wrapup':
      h='<div class="s-wrapup"><div class="s-wrapup-title">'+(s.title||'\\uD83C\\uDF93 Bug\\u00FCn Ne \\u00D6\\u011Frendik?')+'</div>';
      h+='<ul class="s-wrapup-list">';
      for(var li of(s.learned||[]))h+='<li>'+li+'</li>';
      h+='</ul>';
      if(s.teacher_message)h+='<div class="s-wrapup-msg"><div class="s-wrapup-msg-text">'+s.teacher_message+'</div></div>';
      if(s.homework_hint)h+='<div class="s-wrapup-hw"><div class="s-wrapup-hw-text">\\uD83D\\uDCDD '+s.homework_hint+'</div></div>';
      h+='</div>';break;
    case 'header':h='<div class="s-hdr">'+(s.emoji?s.emoji+' ':'')+s.text+'</div>';break;
    case 'text':h='<div class="s-txt">'+s.content+'</div>';break;
    case 'example':h='<div class="s-ex"><div class="s-en">\\u25B6 '+s.en+'</div><div class="s-tr">\\u2192 '+s.tr+'</div></div>';break;
    case 'dialogue':
      h='<div class="s-dlg">';
      if(s.title)h+='<div class="s-dlg-t">\\uD83D\\uDCAC '+s.title+'</div>';
      for(let l of(s.lines||[]))h+='<div class="s-bub"><b>'+l.speaker+':</b> '+l.text+'</div><br>';
      h+='</div>';break;
    case 'tip':h='<div class="s-tip">\\uD83D\\uDCA1 '+s.content+'</div>';break;
    case 'practice':h='<div class="s-prc">\\u270F\\uFE0F '+s.content+'</div>';break;
    case 'story':
      h='<div class="s-story"><div class="s-story-t">'+(s.title||'Story')+'</div>'
        +'<div class="s-story-cnt">'+s.content+'</div></div>';break;
    case 'curiosity':
      h='<div class="s-curiosity"><div class="s-curiosity-lbl">\\uD83D\\uDCA1 Did you know?</div>'
        +'<div class="s-curiosity-cnt">'+s.content+'</div></div>';break;
    case 'analogy':
      h='<div class="s-analogy"><div class="s-analogy-map">'
        +'<div class="s-analogy-box">'+(s.source||'')+'</div>'
        +'<div class="s-analogy-arrow">\\u27A1</div>'
        +'<div class="s-analogy-box">'+(s.target||'')+'</div></div>'
        +'<div class="s-analogy-cnt">'+s.content+'</div></div>';break;
    case 'challenge':
      var cid='ch_'+Math.random().toString(36).substr(2,6);
      h='<div class="s-challenge"><div class="s-challenge-q">\\uD83C\\uDFAF '+(s.question||'')+'</div>'
        +(s.hint?'<div class="s-challenge-hint">\\uD83D\\uDCA1 '+s.hint+'</div>':'')
        +'<div class="s-challenge-ans" id="'+cid+'" style="display:none">\\u2705 '+
        (s.answer||'')+'</div>'
        +'<div class="s-challenge-reveal" onclick="document.getElementById(\\''+cid+'\\').style.display=\\'block\\';this.style.display=\\'none\\';"'
        +' style="cursor:pointer;color:#6366F1;font-weight:600">\\uD83D\\uDC47 Click to see the answer</div></div>';break;
    case 'mistake':
      var mid='mk_'+Math.random().toString(36).substr(2,6);
      h='<div class="s-mistake">'
        +'<div class="flip-card" id="'+mid+'" onclick="this.classList.toggle(\\'flipped\\');_sfx.reveal&&_sfx.reveal(key="yd_ai_prem_m1");">'
        +'<div class="flip-card-inner">'
        +'<div class="flip-card-front" style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25)">'
        +'<div style="color:#ef4444;font-weight:800;font-size:10px;margin-bottom:4px">\\u274C WRONG (click to flip)</div>'
        +'<div class="s-mistake-wrong-t">'+(s.wrong||'')+'</div></div>'
        +'<div class="flip-card-back" style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25)">'
        +'<div style="color:#22c55e;font-weight:800;font-size:10px;margin-bottom:4px">\\u2705 CORRECT</div>'
        +'<div class="s-mistake-right-t">'+(s.correct||'')+'</div>'
        +(s.explanation?'<div class="s-mistake-exp" style="margin-top:6px">'+s.explanation+'</div>':'')
        +'</div></div></div></div>';break;
    case 'mnemonic':
      h='<div class="s-mnemonic"><div class="s-mnemonic-lbl">\\uD83E\\uDDE0 Memory Trick'
        +(s.technique?'<span class="s-mnemonic-tech">'+s.technique+'</span>':'')+'</div>'
        +'<div class="s-mnemonic-cnt">'+s.content+'</div>'
        +(s.remember?'<div class="s-mnemonic-remember">'+s.remember+'</div>':'')
        +'</div>';break;
    case 'recap':
      h='<div class="s-recap"><div class="s-recap-t">'+(s.title||'Quick Recap')+'</div>'
        +'<ul class="s-recap-pts">';
      for(let p of(s.points||[]))h+='<li>'+p+'</li>';
      h+='</ul></div>';break;
    case 'real_question':
      h='<div class="s-realq"><div class="s-realq-q">'+(s.student||'')+'</div>'
        +'<div class="s-realq-a">'+(s.answer||'')+'</div></div>';break;
    default:h='<div class="s-txt">'+(s.content||s.text||'')+'</div>';
  }
  d.innerHTML=h;return d;
}
var _allShownEls=[];
function showSec(i){
  if(i>=sections.length)return;
  var secType=sections[i].type;
  _sfx.transition&&_sfx.transition();
  setTeacherPose(secType);
  _allShownEls.forEach(function(el){el.classList.remove('active-sec');el.classList.add('past-sec');});
  let el=mkSec(sections[i]);board.appendChild(el);
  _allShownEls.push(el);
  el.classList.add('active-sec');
  setTimeout(function(){el.classList.add('show');},30);
  if(_moodEmojis[secType])setTimeout(function(){spawnMoodParticles(el,secType);},400);
  if(secType==='story'){var stCnt=el.querySelector('.s-story-cnt');if(stCnt){var origText=stCnt.textContent;typewriterEffect(stCnt,origText,20);}}
  if(secType==='wrapup'){setTimeout(function(){var wu=el.querySelector('.s-wrapup');if(wu)spawnWrapupConfetti(wu);},300);}
  board.scrollTop=board.scrollHeight;
  var txt=sections[i].text||sections[i].content||sections[i].message||sections[i].en||'';
  if(subBar)subBar.textContent=txt.substring(0,120);
  updateSecNav(i);
}
function fmt(s){let m=Math.floor(s/60);let ss=Math.floor(s%60);return m+':'+(ss<10?'0':'')+ss;}
if(aud&&aud.querySelector('source')&&aud.querySelector('source').src.length>50){
  aud.addEventListener('timeupdate',function(){
    let t=aud.currentTime;
    while(secIdx<sections.length&&timestamps[secIdx]<=t){showSec(secIdx);secIdx++;}
    if(aud.duration){
      document.getElementById('tlfill').style.width=(t/aud.duration*100)+'%';
      document.getElementById('tcur').textContent=fmt(t);
      document.getElementById('ttot').textContent=fmt(aud.duration);
    }
    animPlaying=!aud.paused;
  });
  aud.addEventListener('ended',function(){
    animPlaying=false;
    while(secIdx<sections.length){showSec(secIdx);secIdx++;}
    if(subBar)subBar.textContent='\\u2705 Ders tamamlandi!';
  });
  /* Autoplay kaldirildi — kullanici tiklamadan ses calmaz */
}else{
  let tmr;
  function showNext(){
    if(secIdx>=sections.length){animPlaying=false;
      if(subBar)subBar.textContent='\\u2705 Ders tamamlandi!';return;}
    showSec(secIdx);
    let txt=sections[secIdx].text||sections[secIdx].content||sections[secIdx].message||sections[secIdx].en||'';
    if(sections[secIdx].topic_intro) txt+=' '+sections[secIdx].topic_intro;
    if(sections[secIdx].lines) txt=sections[secIdx].lines.map(l=>l.text).join(' ');
    let wc=txt.split(/\\s+/).filter(w=>w).length;
    let delay=Math.max(2000,wc/2.5*1000)+300;
    secIdx++;
    document.getElementById('tlfill').style.width=(secIdx/sections.length*100)+'%';
    tmr=setTimeout(showNext,delay/speed);
  }
  // Browser TTS fallback
  let synth=null;
  try{synth=window.speechSynthesis}catch(e){}
  if(!synth){try{synth=window.parent.speechSynthesis}catch(e2){}}
  if(synth){
    let si=0;
    function spkFallback(){
      if(si>=sections.length)return;
      let txt=sections[si].text||sections[si].content||sections[si].message||sections[si].en||'';
      if(sections[si].topic_intro) txt+=' '+sections[si].topic_intro;
      if(sections[si].lines) txt=sections[si].lines.map(l=>l.text).join('. ');
      showSec(si);si++;
      document.getElementById('tlfill').style.width=(si/sections.length*100)+'%';
      let u=new SpeechSynthesisUtterance(txt);u.lang='en-US';u.rate=0.85*speed;
      u.onend=function(){if(si<sections.length)spkFallback();
        else{animPlaying=false;if(subBar)subBar.textContent='\\u2705 Ders tamamlandi!';}};
      u.onerror=function(){si++;if(si<sections.length)spkFallback();};
      synth.speak(u);board.scrollTop=board.scrollHeight;
    }
    setTimeout(spkFallback,800);
  }else{setTimeout(showNext,800);}
}
function togglePlay(){
  let btn=document.getElementById('btnPlay');
  if(aud&&aud.querySelector('source')&&aud.querySelector('source').src.length>50){
    if(aud.paused){aud.play();btn.innerHTML='\\u23F8 DURAKLAT';btn.style.background='';animPlaying=true;}
    else{aud.pause();btn.innerHTML='\\u25B6 DEVAM';btn.style.background='#15803d';animPlaying=false;}
  }
}
function skipSec(){
  if(aud&&!aud.paused&&secIdx<timestamps.length){
    aud.currentTime=timestamps[Math.min(secIdx,timestamps.length-1)];
  }
}
function doRestart(){
  secIdx=0;board.innerHTML='';animPlaying=true;
  if(aud&&aud.querySelector('source')&&aud.querySelector('source').src.length>50){
    aud.currentTime=0;aud.play().catch(()=>{});
  }
  document.getElementById('btnPlay').innerHTML='\\u23F8 DURAKLAT';
  document.getElementById('btnPlay').style.background='';
  document.getElementById('tlfill').style.width='0%';
}
function setSpd(s){
  speed=s;if(aud)aud.playbackRate=s;
  ['b1x','b15x','b2x'].forEach(id=>{document.getElementById(id).style.borderColor='rgba(251,191,36,0.3)';});
  let map={1:'b1x',1.5:'b15x',2:'b2x'};
  if(map[s])document.getElementById(map[s]).style.borderColor='#f59e0b';
  document.getElementById('spdInfo').textContent={1:'Normal',1.5:'Hizli',2:'Cok hizli'}[s]||'';
}
function setVol(v){if(aud)aud.volume=v/100;}
/* ── AUTO-STOP: iframe kaldirilinca / gizlenince sesi durdur ── */
function _killAudio(){
  try{if(aud){aud.pause();aud.currentTime=0;aud.src='';}}catch(e){}
  try{if(typeof speechSynthesis!=='undefined')speechSynthesis.cancel();}catch(e){}
  animPlaying=false;
}
window.addEventListener('beforeunload',_killAudio);
window.addEventListener('pagehide',_killAudio);
document.addEventListener('visibilitychange',function(){if(document.hidden)_killAudio();});
/* MutationObserver: iframe DOM'dan cikarilirsa */
try{
  var _mo=new MutationObserver(function(muts){
    for(var m of muts){for(var n of m.removedNodes){
      if(n===document.documentElement||n.contains&&n.contains(aud)){_killAudio();_mo.disconnect();return;}
    }}
  });
  if(window.frameElement&&window.frameElement.parentNode){
    _mo.observe(window.frameElement.parentNode,{childList:true,subtree:true});
  }
}catch(e){}
/* ── FULLSCREEN TOGGLE ── */
function toggleFS(){
  var el=document.documentElement;
  var fsBtn=document.getElementById('fsBtn');
  if(!document.fullscreenElement&&!document.webkitFullscreenElement){
    var rq=el.requestFullscreen||el.webkitRequestFullscreen||el.msRequestFullscreen;
    if(rq)rq.call(el);
    if(fsBtn)fsBtn.textContent='\\u2716 Kucult';
  }else{
    var ex=document.exitFullscreen||document.webkitExitFullscreen||document.msExitFullscreen;
    if(ex)ex.call(document);
    if(fsBtn)fsBtn.textContent='\\u26F6 Tam Ekran';
  }
}
document.addEventListener('fullscreenchange',function(){
  var fsBtn=document.getElementById('fsBtn');
  if(fsBtn)fsBtn.textContent=document.fullscreenElement?'\\u2716 Kucult':'\\u26F6 Tam Ekran';
});
/* ── iframe fullscreen: parent iframe'i genislet ── */
try{
  if(window.frameElement){
    window.frameElement.setAttribute('allowfullscreen','true');
    window.frameElement.setAttribute('webkitallowfullscreen','true');
  }
}catch(e){}
"""

def build_premium_scene(lesson_data: dict, grade: int, teacher_key: str = "mr_james",
                        tts_b64: str | None = None) -> str:
    t = AI_TEACHERS.get(teacher_key, AI_TEACHERS["mr_james"])
    title = lesson_data.get("title", "Lesson")[:120]
    title_safe = title.replace("'", "\\'").replace('"', '\\"')
    sections_json = json.dumps(lesson_data.get("sections", []), ensure_ascii=False)

    audio_src = ""
    if tts_b64:
        audio_src = f"data:audio/mp3;base64,{tts_b64}"

    script_vars = (
        f"const SKIN='{t['skin']}';const HAIR='{t['hair']}';const SHIRT='{t['shirt']}';"
        f"const IS_FEMALE={'true' if t['is_female'] else 'false'};"
        f"const sections={sections_json};"
    )

    html_body = (
        f"<div class='scene'>"
        f"<button class='fs-btn' id='fsBtn' onclick='toggleFS()'>\u26F6 Tam Ekran</button>"
        f"<div class='t-area'>"
        f"<canvas id='tchr' width='180' height='320'></canvas>"
        f"<div class='t-name'>{t['emoji']} {t['name']}</div>"
        f"</div>"
        f"<div class='b-area'>"
        f"<div class='board-frame'>"
        f"<div class='b-hdr'>"
        f"<div class='dot' style='background:#ef4444'></div>"
        f"<div class='dot' style='background:#fbbf24'></div>"
        f"<div class='dot' style='background:#4ade80'></div>"
        f"<div class='b-title'>\U0001F4D6 {title_safe}</div>"
        f"<span class='b-badge'>{grade}. Sinif</span>"
        f"</div>"
        f"<div class='b-cnt' id='board'></div>"
        f"</div>"
        f"<div class='ctrl-tray'>"
        f"<div class='sub-bar' id='subbar'></div>"
        f"<div class='sec-nav' id='secnav'></div>"
        f"<div class='tl-wrap'>"
        f"<span class='tl-time' id='tcur'>0:00</span>"
        f"<div class='tl-bar'><div class='tl-fill' id='tlfill'></div></div>"
        f"<span class='tl-time' id='ttot'>0:00</span>"
        f"</div>"
        f"<div class='ctrls'>"
        f"<button class='cb on' id='btnPlay' onclick='togglePlay()'>\u23F8 DURAKLAT</button>"
        f"<button class='cb' onclick='skipSec()'>\u23ED Atla</button>"
        f"<button class='cb' onclick='doRestart()'>\U0001F504 Bastan</button>"
        f"<button class='cb' id='b1x' onclick='setSpd(1)' style='border-color:#f59e0b'>1x</button>"
        f"<button class='cb' id='b15x' onclick='setSpd(1.5)'>1.5x</button>"
        f"<button class='cb' id='b2x' onclick='setSpd(2)'>2x</button>"
        f"<button class='cb' onclick='toggleFS()'>\u26F6</button>"
        f"<span class='vol-w'>\U0001F50A <input type='range' id='vol' min='0' max='100' value='80'"
        f" oninput='setVol(this.value)'></span>"
        f"<span style='color:#d4a574;font-size:11px;margin-left:4px' id='spdInfo'>Normal</span>"
        f"</div>"
        f"</div>"
        f"</div></div>"
        f"<audio id='aud'><source src='{audio_src}' type='audio/mpeg'></audio>"
    )

    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        + _SCENE_CSS
        + "</style></head><body>"
        + html_body
        + "<script>"
        + script_vars
        + _SCENE_JS_TEACHER
        + _SCENE_JS_BOARD
        + "</script></body></html>"
    )

# ════════════════════════════════════════════════════════════
# POST-LESSON UI — Quiz
# ════════════════════════════════════════════════════════════
def render_quiz(quiz_data: list, kp: str) -> float | None:
    """Render quiz and return score if submitted."""
    if not quiz_data:
        st.info("Bu ders icin quiz bulunmuyor.")
        return None

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0c4a6e,#0369a1);'
        'border-radius:12px;padding:12px 16px;margin-bottom:12px">'
        '<span style="color:#fff;font-weight:800;font-size:1.1rem">'
        '\U0001F3AF Ders Sonu Quiz — 5 Soru</span></div>',
        unsafe_allow_html=True,
    )

    answers = {}
    for i, q in enumerate(quiz_data[:5]):
        st.markdown(
            f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
            f'padding:12px 14px;margin-bottom:8px">'
            f'<div style="color:#0B0F19;font-weight:700;font-size:.95rem">'
            f'Soru {i+1}: {q.get("question","")}</div></div>',
            unsafe_allow_html=True,
        )
        opts = q.get("options", [])
        if opts:
            sel = st.radio(
                f"Cevap {i+1}:", opts,
                key=f"{kp}_quiz_q{i}", index=None,
                label_visibility="collapsed",
            )
            if sel is not None:
                answers[i] = opts.index(sel) if sel in opts else -1

    # Submit
    submitted = st.session_state.get(f"{kp}_quiz_submitted", False)
    if not submitted:
        def _submit_quiz():
            st.session_state[f"{kp}_quiz_submitted"] = True
            st.session_state[f"{kp}_quiz_answers"] = answers
        st.button("\u2705 Cevaplari Gonder", key=f"{kp}_quiz_submit",
                  use_container_width=True, type="primary", on_click=_submit_quiz)
    else:
        answers = st.session_state.get(f"{kp}_quiz_answers", answers)
        correct = 0
        for i, q in enumerate(quiz_data[:5]):
            user_ans = answers.get(i, -1)
            correct_ans = q.get("correct", 0)
            is_correct = user_ans == correct_ans
            if is_correct:
                correct += 1
            icon = "\u2705" if is_correct else "\u274C"
            color = "#22c55e" if is_correct else "#ef4444"
            st.markdown(
                f'<div style="border-left:3px solid {color};padding:6px 10px;margin:4px 0;'
                f'border-radius:0 8px 8px 0;background:{"rgba(34,197,94,0.05)" if is_correct else "rgba(239,68,68,0.05)"}">'
                f'<span style="font-weight:700">{icon} Soru {i+1}:</span> '
                f'<span style="color:#64748b;font-size:.85rem">{q.get("explanation","")}</span></div>',
                unsafe_allow_html=True,
            )
        score = (correct / max(len(quiz_data[:5]), 1)) * 100
        _color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
        st.markdown(
            f'<div style="background:#111827;'
            f'border:2px solid {_color};border-radius:12px;padding:16px;text-align:center;margin:12px 0">'
            f'<div style="color:{_color};font-size:2rem;font-weight:900">{int(score)}/100</div>'
            f'<div style="color:#64748b;font-size:.85rem">{correct}/{len(quiz_data[:5])} dogru</div></div>',
            unsafe_allow_html=True,
        )
        return score
    return None

# ════════════════════════════════════════════════════════════
# POST-LESSON UI — Flashcards
# ════════════════════════════════════════════════════════════
def render_flashcards(vocab_data: list, kp: str):
    if not vocab_data:
        st.info("Bu ders icin kelime karti bulunmuyor.")
        return

    st.markdown(
        '<div style="background:linear-gradient(135deg,#4c1d95,#6d28d9);'
        'border-radius:12px;padding:12px 16px;margin-bottom:12px">'
        '<span style="color:#fff;font-weight:800;font-size:1.1rem">'
        '\U0001F4DA Kelime Kartlari — Tikla \u00C7evir</span></div>',
        unsafe_allow_html=True,
    )

    cards_html = '<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">'
    for i, v in enumerate(vocab_data[:12]):
        en = v.get("en", "")
        tr = v.get("tr", "")
        phonetic = v.get("phonetic", "")
        example = v.get("example", "")
        card_id = f"fc_{kp}_{i}"
        cards_html += (
            f'<div onclick="document.getElementById(\'{card_id}_b\').style.display='
            f'document.getElementById(\'{card_id}_b\').style.display===\'none\'?\'block\':\'none\';"'
            f' style="width:150px;min-height:120px;background:linear-gradient(135deg,#1e1b4b,#312e81);'
            f'border:1px solid rgba(124,58,237,0.4);border-radius:12px;padding:14px;cursor:pointer;'
            f'text-align:center;transition:all 0.3s;box-shadow:0 4px 12px rgba(0,0,0,0.3)">'
            f'<div style="color:#c4b5fd;font-size:1.1rem;font-weight:700">{en}</div>'
            f'<div style="color:#7c3aed;font-size:.7rem;margin:4px 0">{phonetic}</div>'
            f'<div id="{card_id}_b" style="display:none;margin-top:8px;'
            f'border-top:1px solid rgba(124,58,237,0.3);padding-top:8px">'
            f'<div style="color:#fbbf24;font-weight:700;font-size:.95rem">{tr}</div>'
            f'<div style="color:#94a3b8;font-size:.7rem;margin-top:4px;font-style:italic">{example}</div>'
            f'</div></div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# POST-LESSON UI — Summary
# ════════════════════════════════════════════════════════════
def render_summary(summary_data: list):
    if not summary_data:
        st.info("Ozet bulunamadi.")
        return
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f4c35,#059669);'
        'border-radius:12px;padding:12px 16px;margin-bottom:12px">'
        '<span style="color:#fff;font-weight:800;font-size:1.1rem">'
        '\U0001F4CB Bugunun Ozeti</span></div>',
        unsafe_allow_html=True,
    )
    html = '<div style="background:#f0fdf4;border:1px solid #86efac;border-radius:10px;padding:14px">'
    for i, point in enumerate(summary_data[:5]):
        html += (
            f'<div style="display:flex;gap:8px;margin-bottom:8px;align-items:flex-start">'
            f'<span style="background:#059669;color:#fff;border-radius:50%;width:24px;height:24px;'
            f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;'
            f'flex-shrink:0">{i+1}</span>'
            f'<span style="color:#0B0F19;font-size:.9rem;line-height:1.5">{point}</span></div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# POST-LESSON UI — Chat Mode
# ════════════════════════════════════════════════════════════
def render_chat(lesson_data: dict, grade: int, kp: str):
    from views.ai_premium import (
        _find_teacher_from_schedule, _get_available_classes, _save_teacher_question,
    )
    ders = "İngilizce"
    st.markdown(
        '<div style="background:linear-gradient(135deg,#78350f,#d97706);'
        'border-radius:12px;padding:12px 16px;margin-bottom:12px">'
        '<span style="color:#fff;font-weight:800;font-size:1.1rem">'
        '\U0001F4AC \u00D6\u011Fretmene Sor</span></div>',
        unsafe_allow_html=True,
    )

    # Sınıf / Şube seçimi
    available_classes = _get_available_classes()
    if not available_classes:
        st.warning("Ders programında henüz sınıf/şube tanımlanmamış.")
        return

    class_labels = [f"{s}. Sınıf {sb}" for s, sb in available_classes]
    c1, c2 = st.columns([1, 2])
    with c1:
        sel_idx = st.selectbox(
            "\U0001F3EB S\u0131n\u0131f / \u015Eube",
            range(len(class_labels)),
            format_func=lambda i: class_labels[i],
            key=f"{kp}_chat_sinif",
        )
    sel_sinif, sel_sube = available_classes[sel_idx]

    teacher = _find_teacher_from_schedule(ders, sel_sinif, sel_sube)
    with c2:
        if teacher and teacher["ad"]:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#dcfce7,#bbf7d0);'
                f'border:1px solid #86efac;border-radius:10px;padding:10px 14px;margin-top:24px">'
                f'\U0001F468\u200D\U0001F3EB <b style="color:#166534">{teacher["ad"]}</b>'
                f' <span style="color:#15803d;font-size:.85rem">(\u0130ngilizce \u00D6\u011Fretmeni)</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="background:#fef9c3;border:1px solid #fde047;'
                f'border-radius:10px;padding:10px 14px;margin-top:24px">'
                f'\u26A0\uFE0F <span style="color:#854d0e">Bu s\u0131n\u0131f/\u015Fubede '
                f'<b>\u0130ngilizce</b> dersi i\u00E7in \u00F6\u011Fretmen atanmam\u0131\u015F.</span></div>',
                unsafe_allow_html=True,
            )

    # Gönderilmiş sorular
    q_file = os.path.join("data", "akademik", "ogretmen_sorulari.json")
    try:
        with open(q_file, "r", encoding="utf-8") as f:
            all_questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_questions = []

    from utils.auth import AuthManager
    current_user = AuthManager.get_current_user()
    my_questions = [
        q for q in all_questions
        if q.get("soran_user") == current_user.get("username", "")
        and q.get("sinif") == sel_sinif and q.get("sube") == sel_sube
        and "ngilizce" in q.get("ders", "")
    ]

    if my_questions:
        st.markdown(
            '<div style="background:#111827;border:1px solid #e2e8f0;border-radius:8px;'
            'padding:8px 12px;margin:8px 0">'
            '<span style="color:#475569;font-weight:700;font-size:.95rem">'
            '\U0001F4CB G\u00F6nderilen Sorular\u0131n</span></div>',
            unsafe_allow_html=True,
        )
        for q in reversed(my_questions[-10:]):
            durum_icon = {
                "beklemede": "\U0001F7E1", "okundu": "\U0001F535", "cevaplandi": "\U0001F7E2",
            }.get(q.get("durum", "beklemede"), "\U0001F7E1")
            st.markdown(
                f'<div style="border-left:3px solid #3b82f6;background:#dbeafe;'
                f'border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0">'
                f'\U0001F9D1\u200D\U0001F393 <span style="color:#94A3B8;font-size:.9rem">'
                f'{q["soru"]}</span>'
                f'<div style="color:#64748b;font-size:.75rem;margin-top:4px">'
                f'{durum_icon} {q.get("durum","beklemede").capitalize()} \u2022 {q.get("tarih","")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if q.get("cevap"):
                st.markdown(
                    f'<div style="border-left:3px solid #22c55e;background:#dcfce7;'
                    f'border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0 8px 16px">'
                    f'\U0001F468\u200D\U0001F3EB <span style="color:#94A3B8;font-size:.9rem">'
                    f'{q["cevap"]}</span>'
                    f'<div style="color:#64748b;font-size:.75rem;margin-top:4px">'
                    f'{q.get("cevap_tarih","")}</div></div>',
                    unsafe_allow_html=True,
                )

    # Soru gönderme
    konu = lesson_data.get("topic", lesson_data.get("title", ""))
    user_q = st.text_input(
        "\u2753 Sorunuzu yaz\u0131n:",
        key=f"{kp}_chat_input",
        placeholder="\u0130ngilizce \u00F6\u011Fretmeninize soru sorun...",
    )
    if st.button("\U0001F4E8 G\u00F6nder", key=f"{kp}_chat_send", type="primary") and user_q:
        if not teacher or not teacher["ad"]:
            st.error("Bu s\u0131n\u0131f/\u015Fubede \u0130ngilizce i\u00E7in \u00F6\u011Fretmen bulunamad\u0131.")
        else:
            _save_teacher_question(
                soru=user_q, ders=ders, konu=konu,
                sinif=sel_sinif, sube=sel_sube,
                ogretmen_ad=teacher["ad"], ogretmen_id=teacher.get("id", ""),
            )
            st.success(f"\u2705 Sorunuz **{teacher['ad']}** \u00F6\u011Fretmene g\u00F6nderildi!")
            st.rerun()

# ════════════════════════════════════════════════════════════
# GAMIFICATION
# ════════════════════════════════════════════════════════════
def render_gamification(grade: int, xp_earned: int = 0, quiz_score: float = 0):
    prog = load_progress()
    gd = prog.get(str(grade), {})
    total_xp = gd.get("total_xp", 0)
    total_lessons = gd.get("total_lessons", 0)
    streak = gd.get("streak", 0)
    level = total_xp // 200 + 1
    level_progress = (total_xp % 200) / 200 * 100
    badges = get_earned_badges(grade)

    # Perfect quiz badge check
    if quiz_score >= 100:
        has_perfect = any(b["id"] == "perfect_quiz" for b in badges)
        if not has_perfect:
            badges.append({"id": "perfect_quiz", "name": "Tam Puan", "icon": "\U0001F3C6"})

    st.markdown(
        '<div style="background:linear-gradient(135deg,#111827,#eef2ff);'
        'border:2px solid #6366f1;border-radius:14px;padding:16px;margin:12px 0">'
        '<div style="color:#4f46e5;font-weight:900;font-size:1.2rem;margin-bottom:12px">'
        '\U0001F3AE Oyuncu Profili</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div style="text-align:center;background:#94A3B8;border-radius:10px;padding:10px">'
            f'<div style="font-size:1.8rem">\u2B50</div>'
            f'<div style="color:#fbbf24;font-weight:800;font-size:1.3rem">Lv.{level}</div>'
            f'<div style="color:#64748b;font-size:.7rem">{total_xp} XP</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="text-align:center;background:#94A3B8;border-radius:10px;padding:10px">'
            f'<div style="font-size:1.8rem">\U0001F4DA</div>'
            f'<div style="color:#38bdf8;font-weight:800;font-size:1.3rem">{total_lessons}</div>'
            f'<div style="color:#64748b;font-size:.7rem">Ders</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div style="text-align:center;background:#94A3B8;border-radius:10px;padding:10px">'
            f'<div style="font-size:1.8rem">\U0001F525</div>'
            f'<div style="color:#f97316;font-weight:800;font-size:1.3rem">{streak}</div>'
            f'<div style="color:#64748b;font-size:.7rem">Seri</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div style="text-align:center;background:#94A3B8;border-radius:10px;padding:10px">'
            f'<div style="font-size:1.8rem">\U0001F3C6</div>'
            f'<div style="color:#a78bfa;font-weight:800;font-size:1.3rem">{len(badges)}</div>'
            f'<div style="color:#64748b;font-size:.7rem">Rozet</div></div>',
            unsafe_allow_html=True,
        )

    # XP bar
    st.markdown(
        f'<div style="margin-top:10px">'
        f'<div style="display:flex;justify-content:space-between;color:#64748b;font-size:.75rem">'
        f'<span>Lv.{level}</span><span>Lv.{level+1}</span></div>'
        f'<div style="background:#94A3B8;border-radius:4px;height:8px;overflow:hidden">'
        f'<div style="background:linear-gradient(90deg,#0ea5e9,#38bdf8);height:100%;'
        f'width:{level_progress}%;border-radius:4px;transition:width 0.5s"></div></div></div>',
        unsafe_allow_html=True,
    )

    # XP earned this lesson
    if xp_earned > 0:
        st.markdown(
            f'<div style="text-align:center;margin:8px 0;color:#22c55e;font-weight:700">'
            f'+{xp_earned} XP kazanildi!</div>',
            unsafe_allow_html=True,
        )

    # Badges
    if badges:
        badges_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">'
        for b in badges:
            badges_html += (
                f'<div style="background:#312e81;border:1px solid #7c3aed;border-radius:8px;'
                f'padding:4px 10px;text-align:center;min-width:60px">'
                f'<div style="font-size:1.2rem">{b.get("icon","")}</div>'
                f'<div style="color:#c4b5fd;font-size:.65rem;font-weight:600">{b.get("name","")}</div></div>'
            )
        badges_html += '</div>'
        st.markdown(badges_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SAVED LESSONS LIST
# ════════════════════════════════════════════════════════════
def render_saved_lessons(grade: int, kp: str) -> dict | None:
    lessons = load_saved_lessons(grade)
    if not lessons:
        st.info("Henuz kayitli ders bulunmuyor.")
        return None
    st.markdown(
        f'<div style="color:#38bdf8;font-weight:700;font-size:.95rem;margin-bottom:8px">'
        f'\U0001F4BE Kayitli Dersler ({len(lessons)})</div>',
        unsafe_allow_html=True,
    )
    for i, rec in enumerate(lessons[:10]):
        topic = rec.get("topic", "?")[:50]
        date = rec.get("date", "?")
        def _replay(r=rec):
            st.session_state[f"{kp}_lesson"] = r["lesson"]
            st.session_state[f"{kp}_tts"] = r.get("tts_b64")
            st.session_state[f"{kp}_phase"] = "playing"
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f'<div style="color:#e2e8f0;font-size:.85rem">\U0001F4D6 {topic}'
                f'<span style="color:#64748b;margin-left:8px;font-size:.75rem">{date}</span></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.button("\u25B6", key=f"{kp}_replay_{i}", on_click=_replay)
    return None
