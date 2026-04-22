# -*- coding: utf-8 -*-
"""Sing, Move & Smile — Okul Öncesi Şarkı / Hareket / Eğlenceli Dil Uygulama Kitabı.

Interactive HTML pages for preschool music, movement & fun language practice.
Activity types (5 pages per week):
  1. Chants & Rhymes (Tekerleme ve ritim çalışmaları)
  2. Action Songs (Hareketli şarkılar — TPR temelli)
  3. Drama & Imitation (Drama ve taklit çalışmaları)
  4. Daily Patterns & Routines (Günlük tekrar kalıpları)
  5. Karaoke & Fun Review (Karaoke + eğlenceli karma tekrar)

All content is dynamically generated from curriculum data.
Each week produces 5 HTML pages — one per activity type.
"""
from __future__ import annotations
import random
import hashlib


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

_CFG = {
    "font_size": "22px",
    "color_primary": "#FF6B9D",
    "color_accent": "#C850C0",
    "color_bg": "#FFF0F5",
    "color_green": "#43B581",
    "color_orange": "#FF9A3C",
    "color_yellow": "#FFD93D",
    "color_blue": "#4FC3F7",
    "chant_count": 3,
    "action_song_count": 3,
    "drama_count": 4,
    "routine_count": 5,
    "review_count": 6,
}


# ══════════════════════════════════════════════════════════════════════════════
# CHANT & SONG DATA
# ══════════════════════════════════════════════════════════════════════════════

_CHANTS = [
    {"title": "Head, Shoulders, Knees and Toes",
     "lines": ["Head, shoulders, knees and toes,", "Knees and toes!",
               "Head, shoulders, knees and toes,", "Knees and toes!",
               "Eyes and ears and mouth and nose,",
               "Head, shoulders, knees and toes,", "Knees and toes!"],
     "actions": ["Touch your head", "Touch your shoulders", "Touch your knees", "Touch your toes",
                  "Point to eyes", "Point to ears", "Point to mouth", "Point to nose"],
     "emoji": "🧑", "topic": "body"},

    {"title": "If You're Happy and You Know It",
     "lines": ["If you're happy and you know it, clap your hands! 👏",
               "If you're happy and you know it, clap your hands! 👏",
               "If you're happy and you know it, and you really want to show it,",
               "If you're happy and you know it, clap your hands! 👏"],
     "actions": ["Clap your hands", "Stomp your feet", "Shout hooray!", "Do all three"],
     "emoji": "😊", "topic": "feelings"},

    {"title": "The Wheels on the Bus",
     "lines": ["The wheels on the bus go round and round,",
               "Round and round, round and round.",
               "The wheels on the bus go round and round,",
               "All through the town!"],
     "actions": ["Roll hands", "Swish swish swish (wipers)", "Open and shut (doors)",
                  "Wah wah wah (baby)", "Shh shh shh (mommy)"],
     "emoji": "🚌", "topic": "transport"},

    {"title": "Five Little Monkeys",
     "lines": ["Five little monkeys jumping on the bed,",
               "One fell off and bumped his head.",
               "Mama called the doctor and the doctor said:",
               "No more monkeys jumping on the bed!"],
     "actions": ["Hold up 5 fingers", "Jump up and down", "Touch your head",
                  "Wag your finger — no no no!"],
     "emoji": "🐒", "topic": "numbers"},

    {"title": "Old MacDonald Had a Farm",
     "lines": ["Old MacDonald had a farm, E-I-E-I-O!",
               "And on his farm he had a cow, E-I-E-I-O!",
               "With a moo-moo here and a moo-moo there,",
               "Here a moo, there a moo, everywhere a moo-moo!"],
     "actions": ["Pretend to drive a tractor", "Make cow horns", "Moo loudly",
                  "Point here and there"],
     "emoji": "🐄", "topic": "animals"},

    {"title": "Twinkle Twinkle Little Star",
     "lines": ["Twinkle, twinkle, little star,",
               "How I wonder what you are!",
               "Up above the world so high,",
               "Like a diamond in the sky."],
     "actions": ["Open and close hands (twinkle)", "Tap chin (wonder)",
                  "Point up high", "Make diamond shape with hands"],
     "emoji": "⭐", "topic": "sky"},

    {"title": "Baby Shark",
     "lines": ["Baby shark, doo-doo-doo-doo-doo-doo!",
               "Baby shark, doo-doo-doo-doo-doo-doo!",
               "Baby shark, doo-doo-doo-doo-doo-doo!",
               "Baby shark!"],
     "actions": ["Small pinch (baby)", "Medium clap (mommy)", "Big clap (daddy)",
                  "Big arms (grandma)", "Swimming motion (let's go hunt)"],
     "emoji": "🦈", "topic": "sea"},

    {"title": "Itsy Bitsy Spider",
     "lines": ["The itsy bitsy spider climbed up the water spout,",
               "Down came the rain and washed the spider out.",
               "Out came the sun and dried up all the rain,",
               "And the itsy bitsy spider climbed up the spout again."],
     "actions": ["Fingers climbing up", "Hands rain down", "Make a big sun circle",
                  "Fingers climbing again"],
     "emoji": "🕷️", "topic": "weather"},

    {"title": "One Two Buckle My Shoe",
     "lines": ["One, two — buckle my shoe!",
               "Three, four — knock at the door!",
               "Five, six — pick up sticks!",
               "Seven, eight — lay them straight!",
               "Nine, ten — a big fat hen!"],
     "actions": ["Show 1-2 fingers", "Knock motion", "Pick up motion",
                  "Lay flat motion", "Flap arms like chicken"],
     "emoji": "👟", "topic": "numbers"},

    {"title": "Rain Rain Go Away",
     "lines": ["Rain, rain, go away,",
               "Come again another day.",
               "Little Johnny wants to play,",
               "Rain, rain, go away!"],
     "actions": ["Wave hands away", "Beckon motion", "Clap and jump",
                  "Wave hands away again"],
     "emoji": "🌧️", "topic": "weather"},

    {"title": "Bingo",
     "lines": ["There was a farmer had a dog,",
               "And Bingo was his name-o.",
               "B-I-N-G-O, B-I-N-G-O, B-I-N-G-O,",
               "And Bingo was his name-o!"],
     "actions": ["Clap for each letter", "Replace one letter with clap each round",
                  "Spell out loud", "Final round — all claps!"],
     "emoji": "🐕", "topic": "animals"},

    {"title": "Hokey Pokey",
     "lines": ["You put your right hand in,",
               "You put your right hand out,",
               "You put your right hand in,",
               "And you shake it all about!",
               "You do the Hokey Pokey and you turn yourself around,",
               "That's what it's all about!"],
     "actions": ["Put right hand in", "Put right hand out", "Shake hand",
                  "Turn around", "Clap!"],
     "emoji": "🕺", "topic": "body"},

    {"title": "Row Row Row Your Boat",
     "lines": ["Row, row, row your boat,",
               "Gently down the stream.",
               "Merrily, merrily, merrily, merrily,",
               "Life is but a dream!"],
     "actions": ["Rowing motion", "Gentle waves with hands",
                  "Clap on each merrily", "Put hands together and rest head"],
     "emoji": "🚣", "topic": "transport"},

    {"title": "London Bridge Is Falling Down",
     "lines": ["London Bridge is falling down,",
               "Falling down, falling down.",
               "London Bridge is falling down,",
               "My fair lady!"],
     "actions": ["Arms make bridge", "Slowly lower arms", "Arms fall down",
                  "Bow or curtsy"],
     "emoji": "🌉", "topic": "buildings"},

    {"title": "I'm a Little Teapot",
     "lines": ["I'm a little teapot, short and stout,",
               "Here is my handle, here is my spout.",
               "When I get all steamed up, hear me shout:",
               "Tip me over and pour me out!"],
     "actions": ["Hands on hips (handle)", "One arm out (spout)",
                  "Shake body (steamed up)", "Lean to the side (pour)"],
     "emoji": "🫖", "topic": "food"},
]

_ACTION_SONGS = [
    {"title": "Walking Walking",
     "lyrics": ["Walking, walking, walking, walking.",
                 "Hop, hop, hop! Hop, hop, hop!",
                 "Running, running, running!",
                 "Running, running, running!",
                 "Now let's stop. Now let's stop."],
     "moves": ["Walk in place", "Hop on both feet", "Run in place",
                "Freeze like a statue"],
     "emoji": "🚶", "speed": "medium"},

    {"title": "Shake Your Sillies Out",
     "lyrics": ["Gotta shake, shake, shake your sillies out!",
                 "Shake, shake, shake your sillies out!",
                 "Wiggle your waggles away!"],
     "moves": ["Shake whole body", "Wiggle arms", "Jump up and down",
                "Spin around slowly"],
     "emoji": "🤪", "speed": "fast"},

    {"title": "Open Shut Them",
     "lyrics": ["Open, shut them. Open, shut them.",
                 "Give a little clap, clap, clap.",
                 "Open, shut them. Open, shut them.",
                 "Lay them in your lap, lap, lap."],
     "moves": ["Open hands wide", "Close hands to fists", "Clap three times",
                "Put hands on lap"],
     "emoji": "👐", "speed": "slow"},

    {"title": "Stand Up Sit Down",
     "lyrics": ["Stand up, sit down. Stand up, sit down.",
                 "Clap, clap, clap!",
                 "Point up, point down. Turn around.",
                 "Jump, jump, jump!"],
     "moves": ["Stand up quickly", "Sit down quickly", "Clap hands",
                "Point up then down", "Turn around", "Jump three times"],
     "emoji": "🏃", "speed": "fast"},

    {"title": "Sleeping Bunnies",
     "lyrics": ["See the sleeping bunnies sleeping till it's noon.",
                 "Shall we wake them with a merry tune?",
                 "Oh so still... Are they ill?",
                 "Wake up, bunnies! Hop, hop, hop!"],
     "moves": ["Pretend to sleep", "Put finger to lips", "Stay very still",
                "Jump up and hop around"],
     "emoji": "🐰", "speed": "slow_then_fast"},

    {"title": "Freeze Dance",
     "lyrics": ["Dance, dance, dance around!",
                 "Move your body to the sound!",
                 "When the music stops — FREEZE!",
                 "Don't move, if you please!"],
     "moves": ["Dance freely", "Wiggle and shake", "FREEZE in place",
                "Hold your pose — don't move!"],
     "emoji": "🎶", "speed": "variable"},

    {"title": "Simon Says",
     "lyrics": ["Simon says touch your nose!",
                 "Simon says clap your hands!",
                 "Simon says jump up high!",
                 "Touch your toes! — Wait, Simon didn't say!"],
     "moves": ["Touch nose", "Clap hands", "Jump high",
                "Stay still — it's a trick!"],
     "emoji": "🎯", "speed": "medium"},

    {"title": "The Goldfish",
     "lyrics": ["I'm a little goldfish swimming in the sea,",
                 "I wiggle my tail — come swim with me!",
                 "I blow some bubbles — one, two, three!",
                 "I'm a happy goldfish, as happy as can be!"],
     "moves": ["Swimming motion", "Wiggle hips", "Blow bubbles motion",
                "Smile and swim around"],
     "emoji": "🐠", "speed": "slow"},
]

_DRAMA_SCENARIOS = [
    {"title": "Be a Cat!", "instruction": "Pretend you are a cat.",
     "actions": ["Walk on all fours", "Say 'Meow!'", "Lick your paw", "Stretch and yawn"],
     "emoji": "🐱", "sound": "Meow!"},

    {"title": "Be a Robot!", "instruction": "Walk like a robot.",
     "actions": ["Stiff arms", "Walk step by step", "Say 'Beep boop!'", "Turn slowly"],
     "emoji": "🤖", "sound": "Beep boop!"},

    {"title": "Be a Bird!", "instruction": "Fly like a bird.",
     "actions": ["Spread your arms", "Flap slowly", "Fly around the room", "Land gently"],
     "emoji": "🐦", "sound": "Tweet tweet!"},

    {"title": "Be a Frog!", "instruction": "Jump like a frog.",
     "actions": ["Squat down low", "Jump high", "Say 'Ribbit!'", "Catch a fly — tongue out!"],
     "emoji": "🐸", "sound": "Ribbit!"},

    {"title": "Be an Elephant!", "instruction": "Walk like an elephant.",
     "actions": ["Swing your trunk (arm)", "Take big heavy steps", "Stomp stomp stomp!",
                  "Spray water — pshhhh!"],
     "emoji": "🐘", "sound": "Trumpet!"},

    {"title": "Be a Chef!", "instruction": "Pretend you are cooking.",
     "actions": ["Stir the pot", "Chop chop chop!", "Taste the soup — mmm!", "Serve the food"],
     "emoji": "👨‍🍳", "sound": "Yummy!"},

    {"title": "Be a Firefighter!", "instruction": "Put out the fire!",
     "actions": ["Put on your helmet", "Slide down the pole", "Hold the hose — whoosh!",
                  "Fire is out — hooray!"],
     "emoji": "🧑‍🚒", "sound": "Nee-naw!"},

    {"title": "Be a Fish!", "instruction": "Swim like a fish.",
     "actions": ["Put hands together (fins)", "Swim side to side", "Blow bubbles",
                  "Dive deep down"],
     "emoji": "🐟", "sound": "Blub blub!"},

    {"title": "Be a Superhero!", "instruction": "You have superpowers!",
     "actions": ["Put on your cape", "Strike a hero pose", "Fly through the sky — zoom!",
                  "Save the day — hooray!"],
     "emoji": "🦸", "sound": "Zoom!"},

    {"title": "Be a Monster!", "instruction": "Walk like a friendly monster.",
     "actions": ["Big stompy steps", "Roar gently", "Make silly monster face",
                  "Tickle your friends — haha!"],
     "emoji": "👾", "sound": "Rawr!"},
]

_DAILY_ROUTINES = [
    {"title": "Good Morning!", "pattern": "Good morning, teacher! Good morning, friends!",
     "response": "Good morning! How are you today?",
     "practice": ["I'm happy!", "I'm sleepy!", "I'm hungry!", "I'm great!"],
     "emoji": "🌅"},

    {"title": "Weather Check", "pattern": "What's the weather today?",
     "response": "Look outside! Is it sunny, cloudy, or rainy?",
     "practice": ["It's sunny! ☀️", "It's cloudy! ☁️", "It's rainy! 🌧️", "It's windy! 💨"],
     "emoji": "🌤️"},

    {"title": "How Many?", "pattern": "Let's count together!",
     "response": "One, two, three, four, five!",
     "practice": ["How many fingers?", "How many eyes?", "How many books?", "How many friends?"],
     "emoji": "🔢"},

    {"title": "Colors Around Us", "pattern": "What color is this?",
     "response": "It's red! / It's blue! / It's green!",
     "practice": ["Point to something red!", "Find something blue!", "Show me green!",
                   "Where is yellow?"],
     "emoji": "🎨"},

    {"title": "Goodbye Song", "pattern": "Goodbye, teacher! Goodbye, friends!",
     "response": "See you tomorrow! Have a nice day!",
     "practice": ["Bye bye!", "See you!", "Have fun!", "Take care!"],
     "emoji": "👋"},

    {"title": "Snack Time", "pattern": "I'm hungry! Can I have a snack?",
     "response": "Yes, please! / No, thank you!",
     "practice": ["I like apples!", "I want milk!", "Yummy!", "More, please!"],
     "emoji": "🍎"},

    {"title": "Clean Up Time", "pattern": "Clean up, clean up, everybody clean up!",
     "response": "Put the toys away! Clean up time!",
     "practice": ["Put it here!", "In the box!", "All done!", "Nice and clean!"],
     "emoji": "🧹"},

    {"title": "Line Up!", "pattern": "Line up, please! Stand in a line!",
     "response": "I'm first! / I'm next! / I'm last!",
     "practice": ["Stand here!", "After me!", "Let's go!", "Follow me!"],
     "emoji": "🚶‍♂️"},
]


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _deterministic_seed(week: int) -> int:
    return int(hashlib.md5(f"sms_{week}".encode()).hexdigest()[:8], 16)


def _base_css() -> str:
    return f"""
    <style>
    /* font: sistem fontu kullaniliyor */
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
        font-family: 'Nunito', sans-serif;
        background: linear-gradient(135deg, {_CFG['color_bg']} 0%, #E8F4FD 100%);
        color: #2d3436; font-size: {_CFG['font_size']};
        padding: 18px;
    }}
    .page-title {{
        text-align:center; font-size:1.7em; font-weight:800;
        background: linear-gradient(135deg, {_CFG['color_primary']}, {_CFG['color_accent']});
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        margin-bottom:6px;
    }}
    .page-subtitle {{
        text-align:center; font-size:.85em; color:#6b7280;
        margin-bottom:18px;
    }}
    .week-badge {{
        display:inline-block; background:{_CFG['color_primary']};
        color:#fff; padding:3px 14px; border-radius:20px;
        font-size:.7em; font-weight:700; margin-bottom:12px;
    }}
    .card {{
        background:#fff; border-radius:16px;
        box-shadow:0 4px 15px rgba(0,0,0,.08);
        padding:18px; margin-bottom:16px;
        border-left:5px solid {_CFG['color_primary']};
        transition: transform .2s;
    }}
    .card:hover {{ transform:translateY(-2px); }}
    .card-title {{
        font-size:1.15em; font-weight:700;
        color:{_CFG['color_primary']}; margin-bottom:8px;
    }}
    .song-line {{
        background: linear-gradient(135deg, #ffeef8, #f0efff);
        padding:10px 16px; border-radius:12px;
        margin:5px 0; font-size:1.05em;
        font-weight:600; text-align:center;
        border:1px solid #f0d0e8;
    }}
    .action-badge {{
        display:inline-block; background:{_CFG['color_accent']};
        color:#fff; padding:4px 12px; border-radius:16px;
        font-size:.75em; font-weight:700; margin:3px 4px;
    }}
    .move-badge {{
        display:inline-block; background:{_CFG['color_blue']};
        color:#fff; padding:4px 12px; border-radius:16px;
        font-size:.75em; font-weight:700; margin:3px 4px;
    }}
    .btn {{
        display:inline-block; padding:10px 22px;
        border:none; border-radius:25px; cursor:pointer;
        font-family:inherit; font-size:.85em; font-weight:700;
        color:#fff; transition:all .2s;
    }}
    .btn-play {{ background: linear-gradient(135deg, {_CFG['color_primary']}, {_CFG['color_accent']}); }}
    .btn-play:hover {{ transform:scale(1.05); box-shadow:0 4px 15px rgba(255,107,157,.4); }}
    .btn-speak {{ background: linear-gradient(135deg, {_CFG['color_blue']}, #00BCD4); }}
    .btn-speak:hover {{ transform:scale(1.05); }}
    .btn-check {{ background: linear-gradient(135deg, {_CFG['color_green']}, #2ecc71); }}
    .btn-check:hover {{ transform:scale(1.05); }}
    .drama-step {{
        display:flex; align-items:center; gap:10px;
        background:#f8f0ff; padding:10px 14px; border-radius:12px;
        margin:5px 0; font-weight:600;
    }}
    .drama-num {{
        background:{_CFG['color_accent']}; color:#fff;
        width:30px; height:30px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:.8em; font-weight:800; flex-shrink:0;
    }}
    .routine-bubble {{
        background:linear-gradient(135deg, #e0f7fa, #f3e5f5);
        padding:12px 18px; border-radius:18px;
        margin:6px 0; font-size:1.05em; font-weight:600;
        border:2px solid {_CFG['color_blue']};
    }}
    .routine-response {{
        background:#fff3e0; padding:10px 16px;
        border-radius:14px; margin:4px 0 4px 20px;
        font-weight:600; font-style:italic;
        border-left:4px solid {_CFG['color_orange']};
    }}
    .practice-chip {{
        display:inline-block; background:#e8f5e9;
        color:#2e7d32; padding:6px 14px; border-radius:20px;
        font-size:.8em; font-weight:700; margin:3px;
        border:2px solid #a5d6a7; cursor:pointer;
        transition:all .2s;
    }}
    .practice-chip:hover {{ background:#c8e6c9; transform:scale(1.05); }}
    .karaoke-line {{
        font-size:1.3em; font-weight:700; text-align:center;
        padding:14px; margin:6px 0; border-radius:14px;
        background:linear-gradient(135deg, #fff9c4, #ffe0b2);
        border:2px solid #ffcc02;
        cursor:pointer; transition:all .3s;
    }}
    .karaoke-line:hover {{ transform:scale(1.02); box-shadow:0 4px 15px rgba(255,204,2,.4); }}
    .karaoke-active {{
        background:linear-gradient(135deg, {_CFG['color_primary']}, {_CFG['color_accent']}) !important;
        color:#fff !important; border-color:{_CFG['color_primary']} !important;
    }}
    .score-display {{
        text-align:center; font-size:1.8em; font-weight:800;
        color:{_CFG['color_primary']}; margin:12px 0;
    }}
    .star {{ color:#FFD700; font-size:1.6em; }}
    @keyframes bounce {{
        0%,100% {{ transform:translateY(0); }}
        50% {{ transform:translateY(-8px); }}
    }}
    .bounce {{ animation:bounce .6s ease infinite; }}
    @keyframes pulse {{
        0%,100% {{ transform:scale(1); }}
        50% {{ transform:scale(1.1); }}
    }}
    .pulse {{ animation:pulse 1s ease infinite; }}
    @keyframes wiggle {{
        0%,100% {{ transform:rotate(0deg); }}
        25% {{ transform:rotate(-5deg); }}
        75% {{ transform:rotate(5deg); }}
    }}
    .wiggle {{ animation:wiggle .5s ease infinite; }}
    </style>"""


def _tts_script() -> str:
    return """
    <script>
    function speak(text, rate) {
        rate = rate || 0.7;
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-US'; u.rate = rate; u.pitch = 1.1;
        window.speechSynthesis.speak(u);
    }
    function speakSlow(text) { speak(text, 0.55); }
    function speakNormal(text) { speak(text, 0.8); }
    function speakFast(text) { speak(text, 1.0); }

    function singLine(el, text) {
        el.classList.add('karaoke-active');
        speak(text, 0.65);
        setTimeout(function(){ el.classList.remove('karaoke-active'); }, 3000);
    }

    function playSong(lines) {
        var delay = 0;
        var els = document.querySelectorAll('.karaoke-line');
        lines.forEach(function(line, i) {
            setTimeout(function(){
                if(els[i]) { els[i].classList.add('karaoke-active'); }
                speak(line, 0.6);
                setTimeout(function(){
                    if(els[i]) els[i].classList.remove('karaoke-active');
                }, 3500);
            }, delay);
            delay += 4000;
        });
    }
    </script>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Chants & Rhymes
# ══════════════════════════════════════════════════════════════════════════════

def _build_chants_page(vocab: list, theme: str, week: int, seed: int) -> str:
    rng = random.Random(seed)
    available = list(_CHANTS)
    rng.shuffle(available)
    selected = available[:_CFG["chant_count"]]

    cards = ""
    for idx, ch in enumerate(selected):
        lines_html = ""
        for line in ch["lines"]:
            lines_html += f'<div class="song-line" onclick="speakSlow(\'{_js_safe(line)}\')">{line}</div>'

        actions_html = ""
        for act in ch["actions"]:
            actions_html += f'<span class="action-badge">👋 {act}</span>'

        lines_json = str([_js_safe(l) for l in ch["lines"]]).replace("'", '"')

        cards += f"""
        <div class="card">
            <div class="card-title">{ch['emoji']} {ch['title']}</div>
            {lines_html}
            <div style="margin-top:10px;">
                <strong style="color:{_CFG['color_accent']};">🎬 Actions:</strong><br>
                {actions_html}
            </div>
            <div style="margin-top:12px;text-align:center;">
                <button class="btn btn-play" onclick="playSong({lines_json})">
                    ▶️ Sing Along
                </button>
                <button class="btn btn-speak" onclick="speakSlow('{_js_safe(ch['title'])}')">
                    🔊 Title
                </button>
            </div>
        </div>"""

    # Vocabulary rhythm section
    vocab_rhythm = ""
    display_vocab = vocab[:6] if vocab else ["hello", "friend", "happy", "play", "sing", "dance"]
    for w in display_vocab:
        vocab_rhythm += f"""
        <span class="practice-chip" onclick="speakSlow('{_js_safe(w)}')"
              style="font-size:1em;">
            🎵 {w}
        </span>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css()}{_tts_script()}</head><body>
    <div class="page-title">🎵 Chants & Rhymes</div>
    <div class="page-subtitle">Sing, clap, and move! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week}</span>

    {cards}

    <div class="card" style="border-left-color:{_CFG['color_orange']};">
        <div class="card-title">🎵 Vocabulary Rhythm</div>
        <p style="font-size:.85em;color:#6b7280;">Clap and say each word! Tap to hear:</p>
        <div style="text-align:center;margin-top:8px;">
            {vocab_rhythm}
        </div>
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Action Songs
# ══════════════════════════════════════════════════════════════════════════════

def _build_action_songs_page(vocab: list, theme: str, week: int, seed: int) -> str:
    rng = random.Random(seed + 1)
    available = list(_ACTION_SONGS)
    rng.shuffle(available)
    selected = available[:_CFG["action_song_count"]]

    cards = ""
    for idx, song in enumerate(selected):
        lyrics_html = ""
        for line in song["lyrics"]:
            lyrics_html += f'<div class="song-line" onclick="speakSlow(\'{_js_safe(line)}\')">{line}</div>'

        moves_html = ""
        for i, mv in enumerate(song["moves"]):
            moves_html += f'<span class="move-badge">🏃 {mv}</span>'

        speed_label = {"slow": "🐢 Slow", "medium": "🚶 Medium", "fast": "🏃 Fast",
                       "slow_then_fast": "🐢→🏃 Slow then Fast!", "variable": "🎲 Surprise!"
                       }.get(song.get("speed", "medium"), "🚶 Medium")

        lines_json = str([_js_safe(l) for l in song["lyrics"]]).replace("'", '"')

        cards += f"""
        <div class="card">
            <div class="card-title">{song['emoji']} {song['title']}
                <span style="float:right;font-size:.65em;background:#e8f5e9;
                      padding:2px 10px;border-radius:12px;color:#2e7d32;">
                    {speed_label}
                </span>
            </div>
            {lyrics_html}
            <div style="margin-top:10px;">
                <strong style="color:{_CFG['color_blue']};">💃 Moves:</strong><br>
                {moves_html}
            </div>
            <div style="margin-top:12px;text-align:center;">
                <button class="btn btn-play" onclick="playSong({lines_json})">
                    ▶️ Play & Move
                </button>
            </div>
        </div>"""

    # TPR warm-up
    tpr_words = vocab[:4] if len(vocab) >= 4 else ["jump", "clap", "spin", "stomp"]
    tpr_html = ""
    for w in tpr_words:
        tpr_html += f"""
        <div class="drama-step" onclick="speakNormal('{_js_safe(w)}')">
            <div class="drama-num" style="background:{_CFG['color_blue']};">▶</div>
            <span style="font-size:1.1em;">🎯 {w.upper()}!</span>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css()}{_tts_script()}</head><body>
    <div class="page-title">💃 Action Songs</div>
    <div class="page-subtitle">Move your body and sing! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week}</span>

    <div class="card" style="border-left-color:{_CFG['color_blue']};">
        <div class="card-title">🏃 TPR Warm-up</div>
        <p style="font-size:.82em;color:#6b7280;">Listen and do the action! Tap each word:</p>
        {tpr_html}
    </div>

    {cards}

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Drama & Imitation
# ══════════════════════════════════════════════════════════════════════════════

def _build_drama_page(vocab: list, theme: str, week: int, seed: int) -> str:
    rng = random.Random(seed + 2)
    available = list(_DRAMA_SCENARIOS)
    rng.shuffle(available)
    selected = available[:_CFG["drama_count"]]

    cards = ""
    for sc in selected:
        steps_html = ""
        for i, act in enumerate(sc["actions"]):
            steps_html += f"""
            <div class="drama-step">
                <div class="drama-num">{i+1}</div>
                <span>{act}</span>
            </div>"""

        cards += f"""
        <div class="card">
            <div class="card-title">{sc['emoji']} {sc['title']}</div>
            <div style="background:#f0efff;padding:10px 16px;border-radius:12px;
                        font-weight:700;font-size:1.05em;margin-bottom:8px;">
                🎭 {sc['instruction']}
            </div>
            {steps_html}
            <div style="margin-top:10px;text-align:center;">
                <button class="btn btn-play" onclick="speakSlow('{_js_safe(sc['sound'])}')">
                    🔊 Sound: "{sc['sound']}"
                </button>
                <button class="btn btn-speak" onclick="speakSlow('{_js_safe(sc['instruction'])}')">
                    🎯 Instruction
                </button>
            </div>
        </div>"""

    # Emotion mirror game
    emotions = [("😊", "Happy", "I'm happy!"), ("😢", "Sad", "I'm sad!"),
                ("😠", "Angry", "I'm angry!"), ("😲", "Surprised", "I'm surprised!"),
                ("😴", "Sleepy", "I'm sleepy!"), ("😄", "Excited", "I'm excited!")]
    rng.shuffle(emotions)
    em_html = ""
    for em, name, phrase in emotions[:4]:
        em_html += f"""
        <div style="display:inline-block;text-align:center;margin:8px;cursor:pointer;"
             onclick="speakSlow('{_js_safe(phrase)}')">
            <div style="font-size:2.5em;" class="bounce">{em}</div>
            <div style="font-size:.75em;font-weight:700;color:{_CFG['color_accent']};">{name}</div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css()}{_tts_script()}</head><body>
    <div class="page-title">🎭 Drama & Imitation</div>
    <div class="page-subtitle">Act it out! Be creative! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week}</span>

    <div class="card" style="border-left-color:{_CFG['color_yellow']};">
        <div class="card-title">🪞 Emotion Mirror</div>
        <p style="font-size:.82em;color:#6b7280;">Make the face and say the feeling! Tap to hear:</p>
        <div style="text-align:center;">{em_html}</div>
    </div>

    {cards}

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Daily Patterns & Routines
# ══════════════════════════════════════════════════════════════════════════════

def _build_routines_page(vocab: list, theme: str, week: int, seed: int) -> str:
    rng = random.Random(seed + 3)
    available = list(_DAILY_ROUTINES)
    rng.shuffle(available)
    selected = available[:_CFG["routine_count"]]

    cards = ""
    for rt in selected:
        practice_html = ""
        for pr in rt["practice"]:
            practice_html += f"""
            <span class="practice-chip" onclick="speakSlow('{_js_safe(pr)}')">
                {pr}
            </span>"""

        cards += f"""
        <div class="card">
            <div class="card-title">{rt['emoji']} {rt['title']}</div>
            <div class="routine-bubble" onclick="speakSlow('{_js_safe(rt['pattern'])}')">
                🗣️ {rt['pattern']}
            </div>
            <div class="routine-response" onclick="speakSlow('{_js_safe(rt['response'])}')">
                💬 {rt['response']}
            </div>
            <div style="margin-top:8px;">
                <strong style="color:{_CFG['color_green']};font-size:.85em;">✅ Practice:</strong>
                <div>{practice_html}</div>
            </div>
        </div>"""

    # Weekly vocab routine
    vr_html = ""
    display_vocab = vocab[:8] if vocab else ["hello", "bye", "yes", "no", "please", "thank you"]
    for i, w in enumerate(display_vocab):
        vr_html += f"""
        <div style="display:inline-flex;align-items:center;gap:6px;
                    background:#fff;padding:6px 14px;border-radius:20px;margin:4px;
                    border:2px solid {_CFG['color_primary']};cursor:pointer;font-weight:700;"
             onclick="speakSlow('{_js_safe(w)}')">
            <span style="color:{_CFG['color_primary']};">#{i+1}</span> {w}
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css()}{_tts_script()}</head><body>
    <div class="page-title">📅 Daily Patterns</div>
    <div class="page-subtitle">Say it every day! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week}</span>

    {cards}

    <div class="card" style="border-left-color:{_CFG['color_green']};">
        <div class="card-title">📝 This Week's Words</div>
        <p style="font-size:.82em;color:#6b7280;">Tap each word to hear — say it 3 times!</p>
        <div style="text-align:center;margin-top:8px;">{vr_html}</div>
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Karaoke & Fun Review
# ══════════════════════════════════════════════════════════════════════════════

def _build_karaoke_page(vocab: list, theme: str, week: int, seed: int) -> str:
    rng = random.Random(seed + 4)

    # Pick one main song for karaoke
    all_songs = list(_CHANTS) + [{"title": s["title"], "lines": s["lyrics"],
                                   "emoji": s["emoji"], "actions": s["moves"]}
                                  for s in _ACTION_SONGS]
    rng.shuffle(all_songs)
    karaoke_song = all_songs[0]

    karaoke_lines = ""
    for i, line in enumerate(karaoke_song["lines"]):
        karaoke_lines += f"""
        <div class="karaoke-line" id="kl{i}"
             onclick="singLine(this, '{_js_safe(line)}')">
            {line}
        </div>"""

    lines_json = str([_js_safe(l) for l in karaoke_song["lines"]]).replace("'", '"')

    # Word singing game
    display_vocab = vocab[:6] if vocab else ["happy", "sunny", "rainbow", "music", "dance", "smile"]
    word_game = ""
    for w in display_vocab:
        word_game += f"""
        <div style="display:inline-block;text-align:center;margin:8px;cursor:pointer;"
             onclick="speakSlow('{_js_safe(w)}')">
            <div style="font-size:1.8em;background:linear-gradient(135deg,#fff9c4,#ffe0b2);
                        width:70px;height:70px;border-radius:50%;display:flex;
                        align-items:center;justify-content:center;margin:auto;
                        border:3px solid #ffcc02;" class="pulse">
                🎤
            </div>
            <div style="font-size:.8em;font-weight:700;margin-top:4px;
                        color:{_CFG['color_primary']};">{w}</div>
        </div>"""

    # Fun review quiz
    review_items = list(_CHANTS)[:3]
    rng.shuffle(review_items)
    quiz_html = ""
    for i, item in enumerate(review_items):
        opts = [item["title"]]
        others = [c["title"] for c in _CHANTS if c["title"] != item["title"]]
        rng.shuffle(others)
        opts.extend(others[:2])
        rng.shuffle(opts)

        btns = ""
        for opt in opts:
            correct = "true" if opt == item["title"] else "false"
            btns += f"""
            <button class="btn btn-check" style="margin:4px;font-size:.75em;"
                    onclick="checkKaraoke(this,{correct})">
                {opt}
            </button>"""

        quiz_html += f"""
        <div class="card" style="border-left-color:{_CFG['color_yellow']};">
            <div style="font-size:.85em;color:#6b7280;font-weight:600;">Question {i+1}</div>
            <div style="font-size:1.1em;font-weight:700;margin:6px 0;">
                {item['emoji']} Which song has this action: "{item['actions'][0]}"?
            </div>
            <div>{btns}</div>
            <div id="kr{i}" style="margin-top:6px;font-weight:700;display:none;"></div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    {_base_css()}{_tts_script()}
    <script>
    var karaokeScore = 0;
    function checkKaraoke(el, correct) {{
        var parent = el.parentElement;
        var btns = parent.querySelectorAll('button');
        btns.forEach(function(b){{ b.disabled = true; b.style.opacity='0.6'; }});
        if(correct) {{
            el.style.background = 'linear-gradient(135deg,#43B581,#2ecc71)';
            el.style.opacity = '1';
            karaokeScore++;
            el.parentElement.nextElementSibling.innerHTML = '✅ Correct! ⭐';
            el.parentElement.nextElementSibling.style.color = '#43B581';
        }} else {{
            el.style.background = '#e74c3c';
            el.style.opacity = '1';
            el.parentElement.nextElementSibling.innerHTML = '❌ Try again next time!';
            el.parentElement.nextElementSibling.style.color = '#e74c3c';
        }}
        el.parentElement.nextElementSibling.style.display = 'block';
    }}
    </script>
    </head><body>
    <div class="page-title">🎤 Karaoke & Fun Review</div>
    <div class="page-subtitle">Sing your heart out! — Week {week}: {theme}</div>
    <span class="week-badge">📅 Week {week}</span>

    <div class="card" style="border-left-color:#ffcc02;">
        <div class="card-title">🎤 Karaoke: {karaoke_song['emoji']} {karaoke_song['title']}</div>
        <p style="font-size:.82em;color:#6b7280;margin-bottom:8px;">
            Tap each line to sing, or press Play All!
        </p>
        {karaoke_lines}
        <div style="text-align:center;margin-top:14px;">
            <button class="btn btn-play" style="font-size:1em;padding:12px 30px;"
                    onclick="playSong({lines_json})">
                ▶️ Play All 🎵
            </button>
        </div>
    </div>

    <div class="card" style="border-left-color:{_CFG['color_primary']};">
        <div class="card-title">🎤 Word Singing Game</div>
        <p style="font-size:.82em;color:#6b7280;">Tap a word, listen, then sing it back!</p>
        <div style="text-align:center;">{word_game}</div>
    </div>

    <div style="margin:16px 0;">
        <div class="card-title" style="font-size:1.1em;color:{_CFG['color_accent']};
                                        margin-bottom:8px;">
            🧩 Song Quiz
        </div>
        {quiz_html}
    </div>

    </body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# HELPER — JS-safe string
# ══════════════════════════════════════════════════════════════════════════════

def _js_safe(text: str) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", " ")


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

def build_sing_move_pages(week_num: int, curriculum_weeks: list) -> list[str]:
    """Build 5 HTML pages for a given week.

    Returns list of HTML strings:
      [chants, action_songs, drama, routines, karaoke]
    """
    week_data = None
    for w in curriculum_weeks:
        if w.get("week") == week_num:
            week_data = w
            break
    if not week_data:
        return []

    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", f"Week {week_num}")
    seed = _deterministic_seed(week_num)

    return [
        _build_chants_page(vocab, theme, week_num, seed),
        _build_action_songs_page(vocab, theme, week_num, seed),
        _build_drama_page(vocab, theme, week_num, seed),
        _build_routines_page(vocab, theme, week_num, seed),
        _build_karaoke_page(vocab, theme, week_num, seed),
    ]


def build_full_sing_move(curriculum_weeks: list) -> list[dict]:
    """Build all weeks — returns [{week, theme, pages: [...]}]."""
    result = []
    for w in curriculum_weeks:
        wn = w.get("week", 0)
        pages = build_sing_move_pages(wn, curriculum_weeks)
        if pages:
            result.append({
                "week": wn,
                "theme": w.get("theme", f"Week {wn}"),
                "pages": pages,
            })
    return result
