# -*- coding: utf-8 -*-
"""Professional English Coursebook PDF Generator — Grades 5-8.

Generates print-ready, commercially competitive English coursebooks
for grades 5 through 8, fully aligned with the SmartCampus curriculum.
All content is in English. Each unit follows international ELT standards:

Unit Structure (per unit):
  1. Unit Opener (theme visual area, objectives, key vocabulary preview)
  2. Lead-In & Warm-Up (discussion questions, brainstorming)
  3. Vocabulary Workshop (word bank, collocations, exercises)
  4. Reading (passage + comprehension: MCQ, T/F, open-ended, inference)
  5. Grammar Focus (discovery, rule box, controlled + freer practice)
  6. Listening & Speaking (task-based, pair work, role-play)
  7. Writing Workshop (model text, planning, drafting, checklist)
  8. Pronunciation Corner (phonemes, stress, intonation)
  9. Communication Skills (functional language, real-world tasks)
  10. Review & Self-Assessment (can-do statements, reflection)
"""

from __future__ import annotations
import os
import json as _json
from io import BytesIO
from datetime import datetime


# ══════════════════════════════════════════════════════════════════════════════
# PAGE MAP TRACKER — Records page numbers per unit/section during PDF build
# ══════════════════════════════════════════════════════════════════════════════

def _make_page_marker(Flowable_cls, tracker: dict, key: str):
    """Create an invisible Flowable that records current page number when drawn.
    Must be called after importing reportlab.platypus.Flowable."""

    class _PM(Flowable_cls):
        width = 0
        height = 0

        def __init__(self):
            Flowable_cls.__init__(self)

        def wrap(self, aW, aH):
            return (0, 0)

        def draw(self):
            tracker[key] = self.canv.getPageNumber()

    return _PM()


def _save_page_map(grade: int, page_map: dict):
    """Save coursebook page map to JSON for DLP/report cross-reference."""
    _dir = os.path.join("data", "english")
    os.makedirs(_dir, exist_ok=True)
    _path = os.path.join(_dir, f"coursebook_page_map_{grade}.json")
    with open(_path, "w", encoding="utf-8") as f:
        _json.dump(page_map, f, ensure_ascii=False, indent=2)


def load_page_map(grade: int) -> dict:
    """Load coursebook page map for a given grade. Returns empty dict if not found."""
    _path = os.path.join("data", "english", f"coursebook_page_map_{grade}.json")
    if os.path.exists(_path):
        try:
            with open(_path, "r", encoding="utf-8") as f:
                return _json.load(f)
        except Exception:
            pass
    return {}

# ══════════════════════════════════════════════════════════════════════════════
# GRADE CONFIGURATIONS
# ══════════════════════════════════════════════════════════════════════════════

GRADE_CONFIG = {
    0: {"cefr": "Pre-A1", "label": "Starter — Language Awareness", "hours": 4,
        "desc": "First Steps in English Through Songs, Colours and Play"},
    1: {"cefr": "Pre-A1", "label": "Starter — Beginner", "hours": 4,
        "desc": "Basic Greetings, Colours, Numbers, Family and Animals"},
    2: {"cefr": "Pre-A1+", "label": "Starter — Elementary", "hours": 6,
        "desc": "Simple Sentences, Daily Routines, My World"},
    3: {"cefr": "A1", "label": "Elementary", "hours": 6,
        "desc": "Basic Communication About Familiar Topics"},
    4: {"cefr": "A1+", "label": "Elementary Plus", "hours": 8,
        "desc": "Describing People, Places and Simple Events"},
    5: {"cefr": "A2.1", "label": "Elementary", "hours": 10,
        "desc": "Building Foundations for Daily Communication"},
    6: {"cefr": "A2.2", "label": "Pre-Intermediate", "hours": 10,
        "desc": "Expanding Social & Academic Language"},
    7: {"cefr": "A2.3", "label": "Intermediate Foundation", "hours": 10,
        "desc": "Strengthening Independent Language Use"},
    8: {"cefr": "B1", "label": "Intermediate", "hours": 10,
        "desc": "Achieving Independent User Proficiency"},
    9: {"cefr": "B1+", "label": "Intermediate Plus", "hours": 8,
        "desc": "Academic English, Complex Texts, Structured Writing"},
    10: {"cefr": "B1-B2", "label": "Upper-Intermediate Foundation", "hours": 8,
         "desc": "Advanced Reading, Debate, Essay Writing, Literature"},
    11: {"cefr": "B2", "label": "Upper-Intermediate", "hours": 8,
         "desc": "Fluent Interaction, Professional English, Critical Analysis"},
    12: {"cefr": "B2-C1", "label": "Advanced Foundation", "hours": 6,
         "desc": "Academic Proficiency, Research Writing, Exam Preparation"},
}

# ══════════════════════════════════════════════════════════════════════════════
# UNIT GROUPINGS: 36 weeks -> 10 thematic units per grade
# ══════════════════════════════════════════════════════════════════════════════

def build_unit_groups(grade: int, curriculum_weeks: list) -> list:
    """Dynamically build unit groups from curriculum data."""
    n = len(curriculum_weeks)
    # Split into 10 groups (roughly 3-4 weeks each)
    splits = [0]
    base = n // 10
    remainder = n % 10
    for i in range(10):
        splits.append(splits[-1] + base + (1 if i < remainder else 0))

    groups = []
    for i in range(10):
        start = splits[i]
        end = splits[i + 1]
        weeks_slice = curriculum_weeks[start:end]
        if not weeks_slice:
            continue
        first = weeks_slice[0]
        # Collect all vocab & themes
        themes = [w.get("theme", "") for w in weeks_slice]
        main_theme = first.get("theme", f"Unit {i+1}")
        groups.append({
            "unit": i + 1,
            "title": main_theme,
            "weeks": list(range(start + 1, end + 1)),
            "week_data": weeks_slice,
            "themes": themes,
        })
    return groups


# ══════════════════════════════════════════════════════════════════════════════
# READING PASSAGE GENERATOR (grade-adaptive)
# ══════════════════════════════════════════════════════════════════════════════

def _generate_reading(grade: int, unit: int, theme: str, vocab: list, structure: str) -> dict:
    """Generate a grade-appropriate reading passage with exercises."""
    # Word count targets by grade (tier-adapted)
    wc = {0: 30, 1: 40, 2: 50, 3: 70, 4: 90,
          5: 120, 6: 160, 7: 200, 8: 250,
          9: 280, 10: 320, 11: 350, 12: 400}
    target = wc.get(grade, 150)

    # Pre-built passage banks per grade and unit
    passages = _READING_BANK.get(grade, {}).get(unit, None)
    if passages:
        return passages

    # Fallback: minimal passage template
    return {
        "title": f"Reading: {theme}",
        "text": f"Read the following text about {theme.lower()} and answer the questions below.",
        "questions": [
            {"type": "open", "q": f"What is the main idea of the text?",
             "lines": 2},
            {"type": "tf", "q": f"The text is about {theme.lower()}.", "answer": "T"},
            {"type": "open", "q": "Find two key details from the text.", "lines": 2},
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# GRAMMAR BOXES (grade-adaptive)
# ══════════════════════════════════════════════════════════════════════════════

def _get_grammar(grade: int, unit: int, structure: str) -> dict:
    """Get grammar content for a specific grade and unit."""
    bank = _GRAMMAR_BANK.get(grade, {}).get(unit, None)
    if bank:
        # Normalize varying key names across grades:
        # grade5: title/rule/formula/examples/exercises
        # grade3: rule(=title)/explanation(=rule)/examples/exercises
        # grade4,6,7: topic(=title)/explanation(=rule)/examples/exercises/tip
        # grade8: topic(=title)/explanation(=rule)/examples/rules/practice
        has_title = "title" in bank
        has_topic = "topic" in bank
        if has_title:
            t = bank["title"]
            r = bank.get("rule") or bank.get("explanation", "")
        elif has_topic:
            t = bank["topic"]
            r = bank.get("explanation") or bank.get("rule", "")
        else:
            # grade3 style: 'rule' is actually the title, 'explanation' is the rule
            t = bank.get("rule", "Grammar Focus")
            r = bank.get("explanation", "")
        # Normalize examples to list of (text, type) tuples
        raw_ex = bank.get("examples", [])
        if raw_ex and isinstance(raw_ex[0], str):
            raw_ex = [(e, "+") for e in raw_ex]
        elif raw_ex and isinstance(raw_ex[0], dict):
            raw_ex = [(e.get("sentence", str(e)), e.get("type", "+")) for e in raw_ex]
        # Normalize exercises to list of (question, answer) tuples
        raw_exercises = bank.get("exercises") or bank.get("practice", [])
        if raw_exercises and isinstance(raw_exercises[0], dict):
            normalized = []
            for e in raw_exercises:
                if "items" in e:
                    # grade4 style: {instruction, items}
                    for item in e["items"]:
                        normalized.append((item, ""))
                else:
                    q = e.get("q", e.get("question", ""))
                    a = e.get("answer", e.get("ans", e.get("a", "")))
                    normalized.append((q, a))
            raw_exercises = normalized
        return {
            "title": t,
            "rule": r,
            "formula": bank.get("formula", ""),
            "examples": raw_ex,
            "exercises": raw_exercises,
        }
    return {
        "title": "Grammar Focus",
        "rule": structure if structure else "Study the pattern below.",
        "formula": "",
        "examples": [],
        "exercises": [],
    }


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT BANKS — GRADE 5
# ══════════════════════════════════════════════════════════════════════════════

_READING_BANK = {
    5: {
        1: {
            "title": "A New School Year",
            "text": (
                "Hi! My name is Elif. I am eleven years old and I am in the 5th grade at Ataturk "
                "Middle School. Today is the first day of school and I am very excited! My favourite "
                "subjects are English and Science. I also enjoy Art because I love drawing pictures. "
                "I have Maths on Monday and Wednesday, and English on Tuesday, Thursday and Friday. "
                "I usually wake up at seven o'clock. First, I brush my teeth and wash my face. "
                "Then I get dressed and put on my school uniform. After that, I have breakfast with "
                "my family — we usually eat cheese, olives, bread and drink tea. I go to school by "
                "bus every day. The bus stop is near my house, so I walk there in two minutes. "
                "School starts at half past eight. I have six lessons every day. My favourite teacher "
                "is Ms. Aylin — she teaches us English and always makes the lessons fun with games "
                "and songs. After school, I do my homework first. Then I play with my friends in "
                "the park until six o'clock. I always go to bed at ten o'clock because sleep is "
                "important for growing children. I love my school and I can't wait to learn new things!"
            ),
            "questions": [
                {"type": "mcq", "q": "What are Elif's favourite subjects?",
                 "opts": ["a) Maths and Art", "b) English and Science", "c) History and PE", "d) Music and Turkish"],
                 "answer": "b"},
                {"type": "open", "q": "What time does Elif wake up and what does she do first?", "lines": 2},
                {"type": "tf", "q": "Elif goes to school by car.", "answer": "F"},
                {"type": "tf", "q": "School starts at 8:30.", "answer": "T"},
                {"type": "mcq", "q": "Why does Elif like Ms. Aylin's lessons?",
                 "opts": ["a) Because they are short", "b) Because she gives no homework",
                          "c) Because she uses games and songs", "d) Because she speaks Turkish"],
                 "answer": "c"},
                {"type": "open", "q": "What does Elif do after school? Write three things in order.", "lines": 2},
            ],
        },
        2: {
            "title": "My Family Album",
            "text": (
                "Look at my family photo! We took this picture last Sunday at my grandmother's "
                "garden. This is my father, Ahmet. He is tall and has short dark hair. He is an "
                "engineer and works in a big office in the city centre. He always helps me with my "
                "Maths homework. My mother is Ayse. She has long brown hair and warm brown eyes. "
                "She is very kind and patient. She is a primary school teacher. I have one brother "
                "and one sister. My brother Emre is fourteen years old. He is taller than me and "
                "has straight black hair. He likes playing football and supports Fenerbahce. My "
                "sister Zeynep is seven. She has curly blonde hair and big green eyes. She is very "
                "cheerful and always laughing! She loves playing with her dolls and watching "
                "cartoons. My grandmother Fatma lives with us too. She is sixty-eight years old "
                "and has short grey hair. She makes the best cookies in the world! Every Sunday "
                "evening, we sit together in the living room, drink tea, eat her cookies and talk "
                "about our week. We are a happy family and I love them all very much."
            ),
            "questions": [
                {"type": "mcq", "q": "What does Elif's father do?",
                 "opts": ["a) He is a teacher", "b) He is a doctor", "c) He is an engineer", "d) He is a pilot"],
                 "answer": "c"},
                {"type": "tf", "q": "Emre is younger than Elif.", "answer": "F"},
                {"type": "tf", "q": "Zeynep has curly blonde hair.", "answer": "T"},
                {"type": "open", "q": "Describe Elif's mother using at least 3 details from the text.", "lines": 2},
                {"type": "mcq", "q": "What does the family do every Sunday evening?",
                 "opts": ["a) Go to a restaurant", "b) Watch a film",
                          "c) Drink tea and eat cookies together", "d) Play football"],
                 "answer": "c"},
                {"type": "open", "q": "Describe YOUR family. Write about at least 3 family members.", "lines": 4},
            ],
        },
        3: {
            "title": "A Walk Through My Neighbourhood",
            "text": (
                "I live in a nice and busy neighbourhood in Ankara called Bahcelievler. There is "
                "a big park with tall trees and a playground next to my apartment building. Every "
                "morning, I see people jogging and walking their dogs there. The bakery is across "
                "from the park. I buy fresh bread there every morning — the smell is amazing! The "
                "school is between the mosque and the public library. I love the library because "
                "they have hundreds of English books for children. To get to school from my house, "
                "I go straight for two blocks, then turn left at the traffic lights. The school is "
                "on the right — you can see the Turkish flag on the roof. There is a small hospital "
                "near the post office, and a new shopping centre opened last month behind the bus "
                "station. My favourite place in the neighbourhood is the bookshop — it is opposite "
                "the pharmacy. The owner, Mr. Kemal, always recommends interesting books to me. "
                "I walk to school every day and it takes about ten minutes. I know every street, "
                "every shop and every corner in my neighbourhood. It feels like home!"
            ),
            "questions": [
                {"type": "mcq", "q": "Where is the bakery?",
                 "opts": ["a) Next to the school", "b) Across from the park", "c) Near the hospital", "d) Behind the library"],
                 "answer": "b"},
                {"type": "open", "q": "How does the writer get to school? Write the directions step by step.", "lines": 3},
                {"type": "tf", "q": "The bookshop is next to the pharmacy.", "answer": "F"},
                {"type": "tf", "q": "It takes ten minutes to walk to school.", "answer": "T"},
                {"type": "mcq", "q": "What is between the mosque and the library?",
                 "opts": ["a) The park", "b) The hospital", "c) The school", "d) The bakery"],
                 "answer": "c"},
                {"type": "open", "q": "Describe YOUR neighbourhood. Include at least 5 places and use prepositions.", "lines": 4},
            ],
        },
        4: {
            "title": "Seasons and Weather in Turkey",
            "text": (
                "Turkey has four beautiful seasons, and each one brings something special. In "
                "spring, the weather is warm and sunny. Flowers bloom everywhere — especially tulips "
                "in Istanbul's parks. Birds start singing early in the morning and it sometimes "
                "rains in April. I love the fresh smell after a spring shower! Summer is very hot, "
                "especially in southern cities like Antalya and Mersin. Temperatures can reach 40 "
                "degrees! Many families go to the beach or swim in the sea. Children play outside "
                "all day long and eat ice cream to cool down. Autumn is cool and windy. The leaves "
                "on the trees change colour — they turn beautiful shades of yellow, orange and red. "
                "Students go back to school in September. I like autumn because the weather is "
                "perfect for playing football in the park. Winter is cold and sometimes snowy, "
                "especially in eastern Turkey and cities like Erzurum and Kars. Children there love "
                "making snowmen and having snowball fights! In Istanbul, winter is mostly rainy and "
                "grey. My favourite season is spring because everything looks fresh, colourful and "
                "full of life. What is your favourite season?"
            ),
            "questions": [
                {"type": "mcq", "q": "When does it sometimes rain in spring?",
                 "opts": ["a) In January", "b) In April", "c) In July", "d) In October"],
                 "answer": "b"},
                {"type": "open", "q": "What colours do leaves turn in autumn?", "lines": 1},
                {"type": "tf", "q": "Eastern Turkey gets a lot of snow in winter.", "answer": "T"},
                {"type": "tf", "q": "Summer temperatures never reach 40 degrees.", "answer": "F"},
                {"type": "mcq", "q": "Why does the writer like spring?",
                 "opts": ["a) Because of the snow", "b) Because school starts",
                          "c) Because everything looks fresh and colourful", "d) Because it is hot"],
                 "answer": "c"},
                {"type": "open", "q": "What is your favourite season? Why? Write 4-5 sentences.", "lines": 4},
            ],
        },
        5: {
            "title": "A Day at the Market",
            "text": (
                "It is Saturday morning and the sun is shining brightly. Elif and her mother are "
                "at the local street market in their neighbourhood. They come here every week to "
                "buy fresh food for the family. 'Can I have two kilos of tomatoes, please?' asks "
                "Elif's mother. 'Of course! These are very fresh — from Antalya. That will be "
                "twelve liras,' says the friendly greengrocer. Then they walk to the bakery stall "
                "for a loaf of warm bread and some white cheese. 'How much is the cheese?' asks Mum. "
                "'Thirty liras per kilo,' the baker replies. While Mum is paying, Elif spots the "
                "chocolate section at the next stall. 'How much is this chocolate bar?' she asks "
                "excitedly. 'Five liras each, or two for eight liras,' says the shopkeeper. 'May I "
                "have two, please?' Elif pays with her own pocket money — she has been saving it "
                "for two weeks! At home, they unpack everything and prepare delicious cheese "
                "sandwiches for lunch together. 'Shopping with you is always fun, Mum!' says Elif "
                "with a big smile. 'You are a great helper,' Mum replies."
            ),
            "questions": [
                {"type": "mcq", "q": "How much do the tomatoes cost?",
                 "opts": ["a) 5 liras", "b) 10 liras", "c) 12 liras", "d) 15 liras"],
                 "answer": "c"},
                {"type": "open", "q": "What do they buy at the bakery stall?", "lines": 1},
                {"type": "tf", "q": "Each chocolate bar costs ten liras.", "answer": "F"},
                {"type": "mcq", "q": "How much does Elif spend on two chocolate bars?",
                 "opts": ["a) 5 liras", "b) 8 liras", "c) 10 liras", "d) 12 liras"],
                 "answer": "b"},
                {"type": "open", "q": "How much money does the family spend in total at the market?", "lines": 2},
                {"type": "open", "q": "Write a short shopping dialogue between a customer and a shopkeeper (8 lines).", "lines": 5},
            ],
        },
        6: {
            "title": "My Hobbies and Free Time",
            "text": (
                "My name is Kerem and I love weekends because I can do all the things I enjoy! On "
                "Saturdays, I usually watch a movie with my family after lunch. We enjoy comedies "
                "and adventure films. My all-time favourite film is about a robot that travels "
                "around the world helping people. After the movie, I play video games on my tablet "
                "for about an hour — my parents don't allow me to play longer than that. On "
                "Sundays, I go to my guitar class at the music school near the park. My teacher, "
                "Mr. Ozan, says I am getting much better every week. I can now play five songs! "
                "In the afternoon, I either read comic books in my room or ride my bicycle around "
                "the neighbourhood with my best friend, Arda. Sometimes other friends come over and "
                "we play board games like Monopoly and Scrabble in the garden. Scrabble is great "
                "for learning new English words! I also enjoy drawing — I keep a sketchbook and "
                "draw something new every day. I believe hobbies make life more interesting, help "
                "us discover new talents, and teach us important skills like patience and teamwork."
            ),
            "questions": [
                {"type": "mcq", "q": "What kind of films does Kerem's family enjoy?",
                 "opts": ["a) Horror and drama", "b) Comedies and adventure", "c) Documentaries", "d) Musicals"],
                 "answer": "b"},
                {"type": "open", "q": "What instrument is Kerem learning and who is his teacher?", "lines": 1},
                {"type": "tf", "q": "Kerem plays video games all day.", "answer": "F"},
                {"type": "tf", "q": "Scrabble helps Kerem learn English words.", "answer": "T"},
                {"type": "open", "q": "List four of Kerem's hobbies from the text.", "lines": 2},
                {"type": "open", "q": "What are YOUR hobbies? Write 5-6 sentences about your free time.", "lines": 4},
            ],
        },
        7: {
            "title": "A Day at the Zoo",
            "text": (
                "Last weekend, our class went on a field trip to the zoo. It was a beautiful sunny "
                "day and all thirty students were very excited. Our teacher, Mr. Yilmaz, told us "
                "to stay together and take notes about the animals. First, we visited the elephant "
                "enclosure. The African elephants were much bigger than I expected — the largest "
                "one was about four metres tall! Next, we walked to the monkey area. The monkeys "
                "were the funniest animals in the zoo — they jumped from branch to branch, made "
                "silly faces and even threw banana peels at each other! Everyone laughed so much. "
                "After that, we went to the reptile house. I saw a python that was longer than "
                "three metres! My friend Ali was a bit scared, but I found it absolutely "
                "fascinating. The zookeeper told us that pythons are not dangerous to humans. "
                "At lunchtime, we ate our packed sandwiches by a beautiful lake where pink "
                "flamingos were standing in the water on one leg. In the afternoon, we visited "
                "the penguin exhibit — they were smaller but faster than I thought! The zoo was "
                "far more interesting than I had imagined. I wrote two pages of notes and I "
                "definitely want to visit again next month!"
            ),
            "questions": [
                {"type": "mcq", "q": "What were the funniest animals?",
                 "opts": ["a) Elephants", "b) Snakes", "c) Monkeys", "d) Flamingos"],
                 "answer": "c"},
                {"type": "open", "q": "How tall was the largest elephant?", "lines": 1},
                {"type": "tf", "q": "Ali enjoyed watching the snake.", "answer": "F"},
                {"type": "tf", "q": "They had lunch near a lake.", "answer": "T"},
                {"type": "mcq", "q": "What did the zookeeper say about pythons?",
                 "opts": ["a) They are very fast", "b) They are not dangerous to humans",
                          "c) They eat bananas", "d) They live in water"],
                 "answer": "b"},
                {"type": "open", "q": "Compare two animals from the text using comparative adjectives (bigger, funnier, etc.).", "lines": 3},
            ],
        },
        8: {
            "title": "Our Summer Holiday Plans",
            "text": (
                "Summer holiday is just around the corner and our family is very excited! We are "
                "going to visit my grandparents in Antalya this July. They live in a lovely stone "
                "house near the Mediterranean Sea, just five minutes from the beach. My grandfather "
                "has a small orange garden and he is going to teach me how to pick oranges this "
                "year. I am going to swim in the sea every single day and build enormous sandcastles "
                "on the beach with my cousin Defne. She is the same age as me and we always have "
                "so much fun together! My father is going to drive us there — the journey from "
                "Ankara takes about six hours, but we are going to stop at a restaurant halfway "
                "for a rest and some delicious kebabs. We are going to stay for three wonderful "
                "weeks. I am also going to try snorkelling for the first time! I am a little "
                "nervous but extremely excited to see colourful fish underwater. Mum says we should "
                "also visit the ancient Roman ruins in the old city — she loves history. My father "
                "is going to take us fishing early in the morning. Most importantly, we must "
                "respect nature when we visit the beach — we must not leave any rubbish behind "
                "and we should protect the sea turtles that nest on the shore."
            ),
            "questions": [
                {"type": "mcq", "q": "How long will they stay in Antalya?",
                 "opts": ["a) One week", "b) Two weeks", "c) Three weeks", "d) One month"],
                 "answer": "c"},
                {"type": "open", "q": "What is the writer going to try for the first time?", "lines": 1},
                {"type": "tf", "q": "They are going to Antalya by plane.", "answer": "F"},
                {"type": "tf", "q": "The journey takes about six hours.", "answer": "T"},
                {"type": "mcq", "q": "What animals must they protect on the beach?",
                 "opts": ["a) Dolphins", "b) Seagulls", "c) Sea turtles", "d) Crabs"],
                 "answer": "c"},
                {"type": "open", "q": "Write about YOUR holiday plans using 'going to' at least 4 times.", "lines": 4},
            ],
        },
        9: {
            "title": "Dream Careers",
            "text": (
                "In our class today, we had a very interesting discussion about our dream jobs. "
                "Our teacher asked each student to stand up and talk about their future career. "
                "My friend Selin wants to become a doctor because she wants to help sick people "
                "get better. She says she should study Biology and Chemistry very hard. Burak "
                "dreams of being a pilot — he loves the idea of travelling to different countries "
                "and flying above the clouds. He must learn English very well because all pilots "
                "communicate in English. Deniz is interested in journalism; she enjoys writing "
                "stories and asking important questions. She has to practise writing every day. "
                "I want to be a software engineer because I am passionate about computers and "
                "coding. Last month, I created my first simple game using Scratch! My father says "
                "I should study Maths and learn English well because they are essential for "
                "technology careers. Our teacher told us: 'You should believe in yourselves. Work "
                "hard, stay curious, and never give up on your dreams! Every big achievement "
                "starts with a small step.' Her words really motivated everyone in the classroom. "
                "After the discussion, we each drew a poster about our dream job and hung them "
                "on the classroom wall."
            ),
            "questions": [
                {"type": "mcq", "q": "Why does Burak want to be a pilot?",
                 "opts": ["a) He likes aeroplanes", "b) He wants to travel and fly above the clouds",
                          "c) His father is a pilot", "d) He likes uniforms"],
                 "answer": "b"},
                {"type": "open", "q": "What advice did the teacher give? Write at least 2 pieces of advice.", "lines": 2},
                {"type": "tf", "q": "The writer wants to be a journalist.", "answer": "F"},
                {"type": "tf", "q": "The writer created a game using Scratch.", "answer": "T"},
                {"type": "mcq", "q": "Why is English important for pilots?",
                 "opts": ["a) For reading books", "b) For communication",
                          "c) For cooking", "d) For sports"],
                 "answer": "b"},
                {"type": "open", "q": "What is YOUR dream job? Why? Use 'should', 'must' or 'have to' at least twice.", "lines": 4},
            ],
        },
        10: {
            "title": "Stories, Heritage and Digital Life",
            "text": (
                "Turkey has a rich tradition of storytelling that goes back thousands of years. "
                "One of the most beloved characters is Nasreddin Hodja, a wise and witty man who "
                "lived in Aksehir centuries ago. In one famous story, a neighbour asked him: 'Hodja, "
                "how old is the Earth?' He smiled and replied: 'I am not sure, but it must be very "
                "patient!' People loved his clever humour because his jokes always had a hidden "
                "lesson. Another popular figure is Keloglan, a bald boy who uses his intelligence "
                "to solve problems. These stories teach us important values like honesty, kindness "
                "and wisdom. Turkey is also known for remarkable contributions to world culture. "
                "Did you know that Turkish coffee has a history of over 500 years and is on "
                "UNESCO's cultural heritage list? Or that the tulip flower was first cultivated in "
                "Turkey, not the Netherlands? The world's oldest known settlement, Catalhoyuk, is "
                "in central Turkey — it is about 9,000 years old! Today, as students, we can use "
                "technology and social media responsibly to share our amazing cultural heritage "
                "with people around the world. However, we must be careful online — being a good "
                "digital citizen means being respectful, checking facts before sharing, protecting "
                "our personal information, and never cyberbullying others."
            ),
            "questions": [
                {"type": "mcq", "q": "Who was Nasreddin Hodja?",
                 "opts": ["a) A king", "b) A soldier", "c) A wise and witty man", "d) A scientist"],
                 "answer": "c"},
                {"type": "open", "q": "What is Keloglan known for? Write 2 sentences.", "lines": 2},
                {"type": "tf", "q": "Turkish coffee is about 200 years old.", "answer": "F"},
                {"type": "tf", "q": "Being a digital citizen means being respectful online.", "answer": "T"},
                {"type": "mcq", "q": "How old is Catalhoyuk?",
                 "opts": ["a) About 2,000 years", "b) About 5,000 years",
                          "c) About 9,000 years", "d) About 500 years"],
                 "answer": "c"},
                {"type": "open", "q": "Write 4 rules for being a good digital citizen.", "lines": 4},
            ],
        },
    },
    6: {
        1: {"title": "City Life vs Country Life",
            "text": ("Emma lives in London, a busy city with millions of people. She takes the "
                     "underground to school every day. Her cousin Tom lives on a farm in the countryside. "
                     "He wakes up early to feed the animals before school. Emma enjoys museums, theatres "
                     "and shopping centres, but she sometimes wishes for fresh air and open spaces. Tom "
                     "loves the peace and quiet of the countryside, but he gets bored without cinemas "
                     "nearby. Last summer, they swapped homes for a week. Emma tried milking cows and "
                     "picking strawberries. Tom explored the city, visited the science museum and rode "
                     "on a double-decker bus for the first time. They both learned that each place has "
                     "its own advantages and disadvantages. 'There is no perfect place,' said Emma. "
                     "'But there are wonderful things everywhere!'"),
            "questions": [
                {"type": "mcq", "q": "How does Emma get to school?",
                 "opts": ["a) By bus", "b) By underground", "c) On foot", "d) By bicycle"], "answer": "b"},
                {"type": "open", "q": "What did they do during the home swap? Write about each person.", "lines": 3},
                {"type": "tf", "q": "Tom lives in a busy city.", "answer": "F"},
                {"type": "open", "q": "Compare city life and country life. Which do you prefer? Why?", "lines": 4},
            ]},
        2: {"title": "A Remarkable Life: Marie Curie",
            "text": ("Marie Curie was born in Warsaw, Poland, in 1867. She moved to Paris to study "
                     "physics and mathematics at the Sorbonne University. There she met Pierre Curie, "
                     "and they married in 1895. Together, they discovered two new chemical elements: "
                     "polonium and radium. Marie became the first woman to win a Nobel Prize in 1903, "
                     "and she won a second Nobel Prize in 1911 — the only person at that time to win "
                     "two. She worked incredibly hard in her laboratory, often forgetting to eat. During "
                     "World War I, she developed mobile X-ray units to help wounded soldiers. Marie Curie "
                     "died in 1934, but her discoveries continue to save lives through modern medicine "
                     "and cancer treatment. She proved that determination and curiosity can change the world."),
            "questions": [
                {"type": "mcq", "q": "How many Nobel Prizes did Marie Curie win?",
                 "opts": ["a) One", "b) Two", "c) Three", "d) None"], "answer": "b"},
                {"type": "open", "q": "What did she do during World War I?", "lines": 2},
                {"type": "tf", "q": "Marie Curie was born in France.", "answer": "F"},
                {"type": "open", "q": "Write a short biography of someone you admire (6-8 sentences).", "lines": 5},
            ]},
        3: {"title": "Smart Homes of the Future",
            "text": ("Imagine waking up in a smart home. Your alarm goes off and the curtains open "
                     "automatically. The kitchen starts making your breakfast while you take a shower. "
                     "Smart homes use technology to make daily life easier and more energy-efficient. "
                     "Sensors can detect when you leave a room and turn off the lights. The heating "
                     "system learns your preferred temperature and adjusts itself. You can control "
                     "everything from your smartphone — even when you are not at home. Some smart "
                     "homes have robots that vacuum the floors and mow the lawn. However, experts "
                     "warn that we should be careful about privacy and cybersecurity. Smart homes "
                     "collect a lot of personal data, and this information must be protected."),
            "questions": [
                {"type": "mcq", "q": "What happens when you leave a room in a smart home?",
                 "opts": ["a) Music plays", "b) Lights turn off", "c) The door locks", "d) The TV turns on"], "answer": "b"},
                {"type": "open", "q": "List three features of a smart home from the text.", "lines": 2},
                {"type": "tf", "q": "Smart homes have no disadvantages.", "answer": "F"},
                {"type": "open", "q": "Design your dream smart home. What features would it have?", "lines": 4},
            ]},
        4: {"title": "First Experiences",
            "text": ("Everyone remembers their first experiences. Liam still remembers his first day "
                     "at secondary school. He was nervous because he did not know anyone. By lunchtime, "
                     "he had already made three new friends. Aisha remembers her first time on a plane. "
                     "She was excited but also a little scared during take-off. She looked out of the "
                     "window and saw tiny houses and roads below — it was amazing! Carlos will never "
                     "forget his first cooking experience. He tried to make pancakes for his family, "
                     "but he accidentally put salt instead of sugar. Everyone laughed, but they ate "
                     "them anyway! First experiences teach us that it is perfectly normal to make "
                     "mistakes. What matters is that we try new things and learn from them."),
            "questions": [
                {"type": "mcq", "q": "What mistake did Carlos make?",
                 "opts": ["a) He burned the food", "b) He used salt instead of sugar", "c) He forgot the eggs", "d) He dropped the pan"], "answer": "b"},
                {"type": "open", "q": "How did Liam feel on his first day at school?", "lines": 1},
                {"type": "tf", "q": "Aisha was bored on the plane.", "answer": "F"},
                {"type": "open", "q": "Write about one of your memorable first experiences (5-6 sentences).", "lines": 4},
            ]},
        5: {"title": "Food Around the World",
            "text": ("Food is not just about eating — it is about culture, history and identity. "
                     "In Japan, sushi is a national treasure. It takes years for a sushi chef to master "
                     "the art of preparing perfect rice. In Mexico, tacos have been a staple food for "
                     "thousands of years. The ancient Aztecs used tortillas as both food and plates! "
                     "In Turkey, breakfast is a social event with dozens of different dishes on the table: "
                     "cheeses, olives, honey, eggs, and fresh bread. Italian pizza was originally a "
                     "simple food for the poor in Naples, but it is now loved worldwide. Indian curry "
                     "uses spices that have been traded for over 4,000 years. No matter where you go "
                     "in the world, sharing a meal with others is a universal way to build friendships."),
            "questions": [
                {"type": "mcq", "q": "What did the Aztecs use tortillas for?",
                 "opts": ["a) Decoration", "b) Food and plates", "c) Building", "d) Clothing"], "answer": "b"},
                {"type": "open", "q": "Describe a traditional Turkish breakfast according to the text.", "lines": 2},
                {"type": "tf", "q": "Pizza was originally expensive food.", "answer": "F"},
                {"type": "open", "q": "Write about your favourite food. Where does it come from?", "lines": 4},
            ]},
        6: {"title": "Travel Postcards",
            "text": ("Dear Mum and Dad, Greetings from Cappadocia! We arrived yesterday and took a hot-air "
                     "balloon ride at sunrise. The fairy chimneys looked incredible from above — like a "
                     "landscape from another planet. After landing, we visited an underground city called "
                     "Kaymakli. Ancient people carved homes, churches and even stables deep into the rock "
                     "to protect themselves from invaders. It was cool and dark inside, and some tunnels "
                     "were so narrow that we had to crawl! In the afternoon, we explored Goreme Open Air "
                     "Museum, where monks painted beautiful frescoes on cave walls over a thousand years "
                     "ago. For dinner, we tried testi kebab — a lamb stew cooked inside a sealed clay pot. "
                     "The waiter broke the pot at our table with a hammer — what a show! Tomorrow we are "
                     "going to try pottery-making in Avanos. I have already bought you a beautiful hand-"
                     "painted ceramic bowl from a local workshop. See you on Sunday! Love, Elif"),
            "questions": [
                {"type": "mcq", "q": "What did Elif do at sunrise?",
                 "opts": ["a) Visited a museum", "b) Took a balloon ride", "c) Made pottery", "d) Ate breakfast"], "answer": "b"},
                {"type": "open", "q": "Why did ancient people build underground cities?", "lines": 2},
                {"type": "tf", "q": "Testi kebab is served in a glass bowl.", "answer": "F"},
                {"type": "tf", "q": "Elif bought a ceramic bowl for her parents.", "answer": "T"},
                {"type": "mcq", "q": "Where did monks paint frescoes?",
                 "opts": ["a) On buildings", "b) On canvas", "c) On cave walls", "d) On paper"], "answer": "c"},
                {"type": "open", "q": "Write a postcard from a place you have visited or would like to visit.", "lines": 5},
            ]},
        7: {"title": "Hidden Talents",
            "text": ("Everyone has a talent, but not everyone has discovered it yet. Talent shows have "
                     "become popular worldwide because they give ordinary people a chance to shine. Take "
                     "the story of Barish, a 14-year-old from Ankara. He was shy and quiet at school, and "
                     "nobody knew he could sing. One day, his music teacher heard him humming in the corridor "
                     "and invited him to join the school choir. Within months, Barish was performing solo at "
                     "concerts. His confidence grew enormously. Similarly, Zeynep discovered her talent for "
                     "coding at a weekend workshop. She had never used a programming language before, but "
                     "she created a simple app in just two days. Now she wants to study computer science. "
                     "Research shows that trying new activities is the best way to discover hidden talents. "
                     "Sports, art, music, writing, cooking, robotics — the possibilities are endless. The "
                     "key is to stay curious and never be afraid of failure, because every expert was once "
                     "a beginner."),
            "questions": [
                {"type": "mcq", "q": "How did Barish's teacher discover his talent?",
                 "opts": ["a) He won a competition", "b) She heard him humming", "c) He uploaded a video", "d) His parents told her"], "answer": "b"},
                {"type": "open", "q": "What happened to Zeynep at the coding workshop?", "lines": 2},
                {"type": "tf", "q": "Barish was always confident on stage.", "answer": "F"},
                {"type": "tf", "q": "Trying new activities helps discover talents.", "answer": "T"},
                {"type": "mcq", "q": "What is the main message of the text?",
                 "opts": ["a) Only gifted people have talents", "b) Everyone has hidden talents to discover",
                          "c) Talent shows are bad", "d) School is not important"], "answer": "b"},
                {"type": "open", "q": "What talents do you have? How did you discover them? Write 5-6 sentences.", "lines": 4},
            ]},
        8: {"title": "Wonders of the World",
            "text": ("Our planet is home to incredible natural and man-made wonders. The Grand Canyon in "
                     "Arizona, USA, is over 1.6 kilometres deep and was carved by the Colorado River over "
                     "millions of years. The Great Barrier Reef in Australia is the largest living structure "
                     "on Earth — it can even be seen from space! In Turkey, Pamukkale's white terraces "
                     "are formed by mineral-rich thermal waters that have been flowing for thousands of years. "
                     "UNESCO has listed it as a World Heritage Site. The Northern Lights (Aurora Borealis) "
                     "create breathtaking displays of colour in the sky near the North Pole. They occur when "
                     "charged particles from the Sun interact with Earth's atmosphere. Mount Nemrut in "
                     "southeastern Turkey features giant stone heads built by King Antiochus over 2,000 years "
                     "ago. At sunrise, the statues glow golden — one of the most magical sights in the country. "
                     "These wonders remind us to protect our planet and its extraordinary heritage."),
            "questions": [
                {"type": "mcq", "q": "What carved the Grand Canyon?",
                 "opts": ["a) Earthquakes", "b) Glaciers", "c) The Colorado River", "d) Volcanic eruptions"], "answer": "c"},
                {"type": "open", "q": "Why is Pamukkale a UNESCO World Heritage Site?", "lines": 2},
                {"type": "tf", "q": "The Great Barrier Reef can be seen from space.", "answer": "T"},
                {"type": "tf", "q": "The Northern Lights happen near the South Pole only.", "answer": "F"},
                {"type": "mcq", "q": "Who built the statues on Mount Nemrut?",
                 "opts": ["a) Romans", "b) Greeks", "c) King Antiochus", "d) Ottomans"], "answer": "c"},
                {"type": "open", "q": "Choose a natural or man-made wonder. Research and write about it.", "lines": 5},
            ]},
        9: {"title": "The Power of Friendship",
            "text": ("True friendship is one of the most valuable things in life. Scientists have found "
                     "that strong friendships improve both mental and physical health. People with close "
                     "friends are happier, less stressed, and even live longer! But what makes a good friend? "
                     "Research suggests that trust, honesty, and empathy are the three most important "
                     "qualities. A real friend listens without judging, supports you during difficult times, "
                     "and celebrates your successes without jealousy. In today's digital age, many young "
                     "people have hundreds of online 'friends' but fewer deep, meaningful friendships. Studies "
                     "show that face-to-face interaction is much more beneficial than online communication. "
                     "Playing sports together, studying in groups, or simply chatting during break time "
                     "builds stronger bonds than sending messages. Of course, conflicts happen in every "
                     "friendship. The key is to communicate openly, apologise when you are wrong, and forgive "
                     "when your friend makes a mistake. As the Turkish proverb says, 'A friend in need is a "
                     "friend indeed.'"),
            "questions": [
                {"type": "mcq", "q": "According to scientists, strong friendships...",
                 "opts": ["a) Cause stress", "b) Improve health", "c) Make people lonely", "d) Are not important"], "answer": "b"},
                {"type": "open", "q": "What are the three most important qualities of a good friend?", "lines": 2},
                {"type": "tf", "q": "Online friendships are more beneficial than face-to-face ones.", "answer": "F"},
                {"type": "tf", "q": "Conflicts are normal in friendships.", "answer": "T"},
                {"type": "mcq", "q": "What does the Turkish proverb mean?",
                 "opts": ["a) Friends should lend money", "b) True friends help during hard times",
                          "c) Friends should always agree", "d) Friendship is temporary"], "answer": "b"},
                {"type": "open", "q": "Describe your best friend. What qualities make them special?", "lines": 4},
            ]},
        10: {"title": "Healthy Living in the Modern Age",
            "text": ("Living a healthy life in the 21st century comes with unique challenges. We have more "
                     "technology and comfort than ever, but we also face new health problems. Obesity rates "
                     "among young people have tripled in the last 40 years, largely due to processed food "
                     "and sedentary lifestyles. The World Health Organisation recommends that children and "
                     "teenagers get at least 60 minutes of physical activity every day. However, many young "
                     "people spend more than 7 hours a day looking at screens. Sleep is equally important — "
                     "teenagers need 8-10 hours per night, but studies show most get less than 7. Poor sleep "
                     "affects concentration, mood, and even weight. Mental health is just as important as "
                     "physical health. Talking to trusted adults about worries, practising mindfulness, and "
                     "maintaining social connections all help build resilience. Eating a balanced diet rich "
                     "in fruit, vegetables, whole grains and protein gives your body and brain the fuel they "
                     "need. Small daily habits — walking to school, drinking water instead of sugary drinks, "
                     "and taking screen breaks — can make a big difference over time."),
            "questions": [
                {"type": "mcq", "q": "How much exercise does the WHO recommend daily for teenagers?",
                 "opts": ["a) 20 minutes", "b) 30 minutes", "c) 45 minutes", "d) 60 minutes"], "answer": "d"},
                {"type": "open", "q": "Why is sleep important for teenagers?", "lines": 2},
                {"type": "tf", "q": "Most teenagers get enough sleep.", "answer": "F"},
                {"type": "tf", "q": "Mental health is as important as physical health.", "answer": "T"},
                {"type": "mcq", "q": "What has caused the rise in youth obesity?",
                 "opts": ["a) Too much sport", "b) Processed food and inactivity",
                          "c) Too much sleep", "d) Cold weather"], "answer": "b"},
                {"type": "open", "q": "Create a daily healthy living plan for a teenager. Include exercise, diet, sleep and screen time.", "lines": 5},
            ]},
    },
    7: {
        1: {"title": "Who Am I? Exploring Identity",
            "text": ("Identity is a complex concept that goes beyond our name and appearance. It includes "
                     "our values, beliefs, interests, and the communities we belong to. Psychologists "
                     "say that adolescence is a critical time for identity formation. During these years, "
                     "young people begin to question who they are and what they stand for. Some find their "
                     "identity through sports or music, while others discover it through volunteering or "
                     "academic pursuits. Cultural background also plays a significant role — our traditions, "
                     "language, and family customs shape how we see the world. It is important to respect "
                     "diverse identities and understand that everyone's journey of self-discovery is unique. "
                     "As the philosopher Socrates said, 'Know thyself.' This ancient wisdom remains relevant today."),
            "questions": [
                {"type": "mcq", "q": "According to the text, when is identity formation critical?",
                 "opts": ["a) In childhood", "b) In adolescence", "c) In adulthood", "d) In old age"], "answer": "b"},
                {"type": "open", "q": "What factors contribute to our identity? List at least three.", "lines": 2},
                {"type": "tf", "q": "Identity is only about our physical appearance.", "answer": "F"},
                {"type": "open", "q": "Write a paragraph about what makes you 'you'. Consider your values, interests and background.", "lines": 5},
            ]},
        2: {"title": "Traditions Across Cultures",
            "text": ("Every culture has unique traditions that connect generations. In Japan, the cherry "
                     "blossom festival (Hanami) celebrates the beauty of spring. Families and friends "
                     "gather in parks to enjoy picnics under the blooming trees. In Brazil, Carnival is "
                     "one of the world's largest celebrations, featuring colourful parades, samba music "
                     "and elaborate costumes. Turkey's oil wrestling festival in Kirkpinar is the oldest "
                     "continuously held sporting competition in the world, dating back to 1362. In India, "
                     "Diwali — the festival of lights — symbolises the victory of light over darkness. "
                     "While these traditions differ greatly, they all serve a common purpose: bringing "
                     "people together, preserving cultural heritage, and creating lasting memories."),
            "questions": [
                {"type": "mcq", "q": "How old is the Kirkpinar wrestling festival?",
                 "opts": ["a) About 200 years", "b) About 400 years", "c) About 660 years", "d) About 1000 years"], "answer": "c"},
                {"type": "open", "q": "What do all these traditions have in common?", "lines": 2},
                {"type": "tf", "q": "Carnival in Brazil features quiet, peaceful ceremonies.", "answer": "F"},
                {"type": "open", "q": "Describe a tradition from your culture. Why is it important?", "lines": 5},
            ]},
        3: {"title": "Dream Careers",
            "text": ("Choosing a career is one of the most important decisions in life. According to a recent "
                     "survey, the top dream jobs among Turkish teenagers are software engineering, medicine, "
                     "architecture and teaching. But the job market is changing rapidly. Experts predict that "
                     "65 per cent of today's primary school students will work in jobs that do not yet exist. "
                     "Fields like artificial intelligence, renewable energy and space tourism are creating "
                     "entirely new professions. Soft skills — such as communication, teamwork, creativity "
                     "and adaptability — are becoming more important than ever. Employers now value problem-"
                     "solving ability as much as technical knowledge. Internships and work experience programmes "
                     "help young people explore different careers before making a decision. Many successful "
                     "people changed careers several times before finding their true passion. The key is to "
                     "stay open-minded and keep learning throughout your life."),
            "questions": [
                {"type": "mcq", "q": "What percentage of students will work in jobs that don't exist yet?",
                 "opts": ["a) 25%", "b) 45%", "c) 65%", "d) 85%"], "answer": "c"},
                {"type": "open", "q": "What are 'soft skills'? Give three examples from the text.", "lines": 2},
                {"type": "tf", "q": "Technical knowledge is the only thing employers value.", "answer": "F"},
                {"type": "open", "q": "What is your dream career? What skills do you need for it?", "lines": 4},
            ]},
        4: {"title": "Media Literacy in the Digital Age",
            "text": ("We live in an era of information overload. Every day, we encounter news articles, "
                     "social media posts, advertisements and videos competing for our attention. But how much "
                     "of this information is reliable? Fake news — deliberately false stories designed to "
                     "mislead — has become a serious problem. Studies show that false information spreads "
                     "six times faster than true information on social media. Media literacy is the ability "
                     "to critically analyse and evaluate media messages. It involves asking key questions: "
                     "Who created this message? What is the purpose? Is the source credible? Are facts "
                     "supported by evidence? Critical thinkers check multiple sources before believing or "
                     "sharing information. They look for primary sources, verify statistics, and consider "
                     "different perspectives. Schools are now teaching media literacy as an essential skill "
                     "for the 21st century. Being media literate does not mean distrusting everything — it "
                     "means making informed decisions about what to believe and share."),
            "questions": [
                {"type": "mcq", "q": "How much faster does false information spread than true information?",
                 "opts": ["a) 2 times", "b) 4 times", "c) 6 times", "d) 10 times"], "answer": "c"},
                {"type": "open", "q": "What questions should a media-literate person ask?", "lines": 3},
                {"type": "tf", "q": "Media literacy means distrusting all information.", "answer": "F"},
                {"type": "open", "q": "Have you ever encountered fake news? How did you identify it?", "lines": 4},
            ]},
        5: {"title": "Mental Health Matters",
            "text": ("Mental health is just as important as physical health, yet it is often overlooked. "
                     "The World Health Organisation reports that one in seven adolescents worldwide experiences "
                     "a mental health condition. Anxiety and depression are the most common issues among "
                     "teenagers. Warning signs include persistent sadness, withdrawal from friends, changes "
                     "in sleep or appetite, and difficulty concentrating. Fortunately, there are many ways to "
                     "support mental well-being. Regular exercise releases endorphins — chemicals that improve "
                     "mood naturally. Spending time in nature has been shown to reduce stress and anxiety. "
                     "Maintaining strong social connections provides emotional support. Practising gratitude "
                     "by writing down three good things each day can significantly improve outlook. Most "
                     "importantly, talking about feelings is not a sign of weakness — it is a sign of strength. "
                     "Schools in Turkey are increasingly providing counselling services and mental health "
                     "awareness programmes."),
            "questions": [
                {"type": "mcq", "q": "What fraction of adolescents experience mental health issues?",
                 "opts": ["a) 1 in 3", "b) 1 in 5", "c) 1 in 7", "d) 1 in 10"], "answer": "c"},
                {"type": "open", "q": "List three warning signs of mental health problems.", "lines": 2},
                {"type": "tf", "q": "Talking about feelings is a sign of weakness.", "answer": "F"},
                {"type": "open", "q": "What do you do to maintain your mental health? Write 5 sentences.", "lines": 4},
            ]},
        6: {"title": "Space Exploration: Past and Future",
            "text": ("Humanity's journey into space began on 12 April 1961 when Yuri Gagarin became the "
                     "first person to orbit Earth. Eight years later, Neil Armstrong took 'one small step' "
                     "on the Moon. Since then, we have sent rovers to Mars, probes to the outer planets, "
                     "and the Hubble Space Telescope has captured images of galaxies billions of light-years "
                     "away. The International Space Station (ISS) has been continuously occupied since 2000, "
                     "with astronauts conducting experiments in microgravity. Turkey established its space "
                     "agency (TUA) in 2018, and in 2023, Alper Gezeravci became the first Turkish astronaut "
                     "to travel to the ISS. The future of space exploration includes plans to build a permanent "
                     "base on the Moon, send humans to Mars by the 2030s, and mine asteroids for precious "
                     "metals. Private companies like SpaceX are making space travel cheaper and more accessible. "
                     "Some scientists even envision space tourism becoming routine within our lifetimes."),
            "questions": [
                {"type": "mcq", "q": "When did Yuri Gagarin orbit Earth?",
                 "opts": ["a) 1957", "b) 1961", "c) 1969", "d) 1975"], "answer": "b"},
                {"type": "open", "q": "Who was the first Turkish astronaut? What did he do?", "lines": 2},
                {"type": "tf", "q": "Turkey established its space agency in 2023.", "answer": "F"},
                {"type": "open", "q": "Would you like to travel to space? Write a paragraph explaining why or why not.", "lines": 5},
            ]},
        7: {"title": "Migration and Cultural Exchange",
            "text": ("Throughout history, migration has shaped civilisations and cultures. The Silk Road, one "
                     "of the earliest trade routes, connected China to Europe and facilitated the exchange of "
                     "goods, ideas, religions and technologies. Turkish history is deeply connected to migration "
                     "— the Turkic peoples migrated westward from Central Asia over centuries, eventually "
                     "establishing the Ottoman Empire, which itself was a remarkable multicultural society. "
                     "Today, migration continues to reshape societies. There are approximately 281 million "
                     "international migrants worldwide. Migrants bring diverse perspectives, skills and cultural "
                     "practices to their new communities. Turkish cuisine, for example, has been enriched by "
                     "influences from Central Asian, Arab, Persian and Balkan cooking traditions. However, "
                     "migration also presents challenges, including language barriers, cultural adjustment and "
                     "social integration. Successful multicultural societies find ways to celebrate diversity "
                     "while building common ground."),
            "questions": [
                {"type": "mcq", "q": "What was the Silk Road?",
                 "opts": ["a) A river", "b) A trade route", "c) A mountain range", "d) A railway"], "answer": "b"},
                {"type": "open", "q": "How has migration influenced Turkish cuisine?", "lines": 2},
                {"type": "tf", "q": "Migration always brings only benefits.", "answer": "F"},
                {"type": "open", "q": "Write about how different cultures have influenced your daily life.", "lines": 5},
            ]},
        8: {"title": "The Magic of Cinema",
            "text": ("Cinema has been entertaining and educating audiences for over a century. The Lumiere "
                     "brothers held the first public film screening in Paris in 1895. Early films were short, "
                     "silent and in black and white. Sound was added in 1927 with 'The Jazz Singer,' and "
                     "colour became standard in the 1960s. Today, films use computer-generated imagery (CGI) "
                     "to create entire worlds from scratch. Turkey has a rich film tradition called Yesilcam, "
                     "named after the Istanbul street where studios were located. In recent years, Turkish "
                     "cinema has gained international recognition — Nuri Bilge Ceylan won the Palme d'Or at "
                     "Cannes in 2014. Films are powerful because they combine storytelling, music, visual art "
                     "and performance. A well-made film can change how we see the world, build empathy for "
                     "people different from ourselves, and start important conversations about social issues."),
            "questions": [
                {"type": "mcq", "q": "When was the first public film screening?",
                 "opts": ["a) 1875", "b) 1895", "c) 1910", "d) 1927"], "answer": "b"},
                {"type": "open", "q": "What is Yesilcam? Explain using information from the text.", "lines": 2},
                {"type": "tf", "q": "Sound was always part of cinema.", "answer": "F"},
                {"type": "open", "q": "Write a review of your favourite film. Include plot, characters and your opinion.", "lines": 5},
            ]},
        9: {"title": "Technology and Artificial Intelligence",
            "text": ("Artificial intelligence (AI) is no longer science fiction — it is part of our daily lives. "
                     "Virtual assistants like Siri and Google Assistant use AI to understand and respond to voice "
                     "commands. Recommendation algorithms on Netflix, YouTube and Spotify analyse your preferences "
                     "to suggest content you might enjoy. Self-driving cars use AI to navigate roads safely. In "
                     "medicine, AI can analyse X-rays and detect diseases earlier than human doctors. However, AI "
                     "also raises ethical concerns. Will machines replace human workers? Can AI make fair decisions? "
                     "Who is responsible when an AI system makes a mistake? Experts emphasise that AI should be used "
                     "as a tool to enhance human capabilities, not replace them. The most successful applications "
                     "of AI combine machine efficiency with human creativity and judgment. Understanding AI is "
                     "becoming an essential skill, and many Turkish schools are now offering coding and robotics "
                     "programmes."),
            "questions": [
                {"type": "mcq", "q": "Which is NOT an example of AI mentioned in the text?",
                 "opts": ["a) Virtual assistants", "b) Self-driving cars", "c) Video games", "d) Medical diagnosis"], "answer": "c"},
                {"type": "open", "q": "What ethical concerns does AI raise? Mention at least two.", "lines": 3},
                {"type": "tf", "q": "AI should completely replace human workers.", "answer": "F"},
                {"type": "open", "q": "How do you use AI in your daily life? Do you think it is helpful or dangerous? Write your opinion.", "lines": 5},
            ]},
        10: {"title": "Making a Difference: Youth Activism",
            "text": ("Young people around the world are proving that age is no barrier to making a difference. "
                     "Malala Yousafzai campaigned for girls' education in Pakistan and became the youngest Nobel "
                     "Prize laureate at age 17. Greta Thunberg started a global climate movement with her solo "
                     "school strike in Sweden. In Turkey, young volunteers have organised beach clean-ups, tree-"
                     "planting campaigns and food drives for those in need. The United Nations Sustainable "
                     "Development Goals (SDGs) provide a framework for addressing global challenges including "
                     "poverty, inequality, climate change and environmental degradation. Goal 4 focuses on quality "
                     "education for all, while Goal 13 calls for urgent action on climate change. Every individual "
                     "can contribute — from reducing plastic waste and conserving water to volunteering in the "
                     "community and raising awareness on social media. As Margaret Mead said, 'Never doubt that a "
                     "small group of thoughtful, committed citizens can change the world.'"),
            "questions": [
                {"type": "mcq", "q": "At what age did Malala win the Nobel Prize?",
                 "opts": ["a) 14", "b) 15", "c) 17", "d) 19"], "answer": "c"},
                {"type": "open", "q": "What are the UN Sustainable Development Goals? Mention two from the text.", "lines": 2},
                {"type": "tf", "q": "Only adults can make a difference in society.", "answer": "F"},
                {"type": "open", "q": "Choose a social or environmental issue you care about. Write an action plan to address it.", "lines": 5},
            ]},
    },
    8: {
        1: {"title": "The Power of Self-Reflection",
            "text": ("In today's fast-paced world, self-reflection has become more important than ever. "
                     "It is the practice of examining our thoughts, emotions and actions to gain a deeper "
                     "understanding of ourselves. Research shows that people who regularly reflect on "
                     "their experiences tend to make better decisions and have stronger relationships. "
                     "Journaling is one of the most effective methods of self-reflection. Writing down "
                     "your thoughts helps you process complex emotions and identify patterns in your "
                     "behaviour. Another powerful tool is mindfulness meditation, which trains your brain "
                     "to focus on the present moment without judgement. Schools around the world are "
                     "beginning to incorporate self-reflection activities into their curricula. Students "
                     "who practise self-reflection report higher levels of motivation, improved academic "
                     "performance and greater emotional resilience."),
            "questions": [
                {"type": "mcq", "q": "What does research show about people who reflect regularly?",
                 "opts": ["a) They sleep better", "b) They make better decisions", "c) They earn more money", "d) They exercise more"], "answer": "b"},
                {"type": "open", "q": "Explain two methods of self-reflection mentioned in the text.", "lines": 3},
                {"type": "tf", "q": "Self-reflection has no impact on academic performance.", "answer": "F"},
                {"type": "open", "q": "Write a reflective paragraph about a challenge you have overcome recently.", "lines": 5},
            ]},
        2: {"title": "The World's Languages",
            "text": ("There are approximately 7,000 languages spoken in the world today. However, "
                     "linguists estimate that nearly half of them will disappear by the end of this "
                     "century. A language dies when its last native speaker passes away. This is called "
                     "'language death,' and it represents the loss of an entire worldview, cultural "
                     "knowledge and historical memory. Some organisations are working to preserve "
                     "endangered languages through documentation, education programmes and technology. "
                     "For instance, apps and websites can help speakers of endangered languages teach "
                     "their mother tongue to younger generations. Multilingualism — the ability to speak "
                     "several languages — is increasingly valued in our globalised world. Studies suggest "
                     "that bilingual people have cognitive advantages, including better problem-solving "
                     "skills and delayed onset of age-related cognitive decline."),
            "questions": [
                {"type": "mcq", "q": "How many languages are spoken today?",
                 "opts": ["a) About 3,000", "b) About 5,000", "c) About 7,000", "d) About 10,000"], "answer": "c"},
                {"type": "open", "q": "What happens when a language dies? Use your own words.", "lines": 3},
                {"type": "tf", "q": "All languages are expected to survive this century.", "answer": "F"},
                {"type": "open", "q": "Should endangered languages be preserved? Write an opinion paragraph with reasons.", "lines": 5},
            ]},
        3: {"title": "Science, Ethics and Society",
            "text": ("Scientific progress has always raised ethical questions. When the first cloned animal, "
                     "Dolly the sheep, was created in 1996, debates erupted about whether cloning should be "
                     "applied to humans. Gene editing technology CRISPR now allows scientists to modify DNA "
                     "with unprecedented precision — potentially eliminating genetic diseases, but also raising "
                     "concerns about 'designer babies.' Nuclear energy provides clean electricity but carries "
                     "risks of catastrophic accidents, as seen in Chernobyl (1986) and Fukushima (2011). "
                     "Social media algorithms maximise engagement but may contribute to anxiety and polarisation. "
                     "The scientific community has developed ethical frameworks to guide research. Key principles "
                     "include informed consent, transparency, minimising harm, and ensuring that benefits are "
                     "distributed fairly. Ethics committees review proposed experiments to assess potential risks. "
                     "As citizens, we all have a responsibility to engage in these discussions, because science "
                     "affects every aspect of our lives."),
            "questions": [
                {"type": "mcq", "q": "When was Dolly the sheep cloned?",
                 "opts": ["a) 1986", "b) 1996", "c) 2001", "d) 2011"], "answer": "b"},
                {"type": "open", "q": "What ethical concerns does gene editing raise?", "lines": 3},
                {"type": "tf", "q": "Nuclear energy has no associated risks.", "answer": "F"},
                {"type": "open", "q": "Choose a scientific issue and argue both sides. Which side do you support?", "lines": 5},
            ]},
        4: {"title": "Digital Storytelling",
            "text": ("Storytelling is one of humanity's oldest arts, and technology has transformed how we "
                     "tell and consume stories. Digital storytelling combines traditional narrative with "
                     "multimedia elements — images, video, audio and interactive features. Podcasts have "
                     "become a powerful storytelling medium, with over 460 million listeners worldwide. "
                     "Social media platforms like Instagram and TikTok have created new forms of micro-"
                     "storytelling, where creators convey meaning in seconds. Video essays on YouTube "
                     "combine visual analysis with narration to explore complex topics. Interactive fiction "
                     "lets readers choose their own path through a story. Virtual reality (VR) takes storytelling "
                     "even further by placing the audience inside the narrative. In journalism, data visualisation "
                     "transforms statistics into compelling visual stories. Despite these technological advances, "
                     "the fundamentals of good storytelling remain unchanged: a compelling character, a clear "
                     "conflict, and an emotional resolution."),
            "questions": [
                {"type": "mcq", "q": "How many podcast listeners are there worldwide?",
                 "opts": ["a) 100 million", "b) 260 million", "c) 460 million", "d) 800 million"], "answer": "c"},
                {"type": "open", "q": "What are the fundamentals of good storytelling?", "lines": 2},
                {"type": "tf", "q": "Technology has completely changed the rules of storytelling.", "answer": "F"},
                {"type": "open", "q": "Create a short digital story outline. Choose your medium and explain why.", "lines": 5},
            ]},
        5: {"title": "Turkey's Geographic Wonders",
            "text": ("Turkey occupies a unique geographic position, straddling two continents and surrounded "
                     "by three seas. This extraordinary location has produced remarkable natural diversity. "
                     "Eastern Turkey contains Mount Ararat (5,137 m), the country's highest peak, and Lake "
                     "Van, the largest lake. The Mediterranean coast features stunning turquoise waters and "
                     "ancient Lycian ruins. Cappadocia's fairy chimneys were formed by volcanic eruptions "
                     "millions of years ago. The Black Sea region receives the most rainfall and is covered "
                     "with dense forests and tea plantations. Pamukkale's white calcium terraces and thermal "
                     "pools have attracted visitors since Roman times. The Bosphorus strait divides Istanbul "
                     "between Europe and Asia — one of only a handful of transcontinental cities in the world. "
                     "Turkey's biodiversity is remarkable too: it is home to over 12,000 plant species, more "
                     "than 450 bird species, and several endangered animals including the Anatolian leopard "
                     "and Mediterranean monk seal."),
            "questions": [
                {"type": "mcq", "q": "How high is Mount Ararat?",
                 "opts": ["a) 3,137 m", "b) 4,137 m", "c) 5,137 m", "d) 6,137 m"], "answer": "c"},
                {"type": "open", "q": "What makes Turkey's geographic position unique?", "lines": 2},
                {"type": "tf", "q": "The Black Sea region is the driest part of Turkey.", "answer": "F"},
                {"type": "open", "q": "Choose a Turkish geographic wonder and write a travel guide paragraph.", "lines": 5},
            ]},
        6: {"title": "Social Media: Connecting or Dividing?",
            "text": ("Social media has fundamentally altered how humans communicate. Platforms like Instagram, "
                     "Twitter and TikTok connect billions of people across borders. Movements like #MeToo and "
                     "#FridaysForFuture demonstrate social media's power to mobilise collective action. During "
                     "natural disasters, social media enables rapid coordination of relief efforts. However, "
                     "critics raise serious concerns. The 'echo chamber' effect means algorithms show users "
                     "content that reinforces their existing beliefs, limiting exposure to diverse viewpoints. "
                     "Cyberbullying affects approximately 37 per cent of young people globally. The pressure "
                     "to present a perfect online image contributes to body image issues and low self-esteem. "
                     "Screen addiction is increasingly recognised as a mental health concern. Research suggests "
                     "that limiting social media use to 30 minutes daily significantly improves well-being. "
                     "The challenge for our generation is to harness social media's benefits while mitigating "
                     "its harms — developing digital literacy, practising responsible sharing, and maintaining "
                     "a healthy balance between online and offline life."),
            "questions": [
                {"type": "mcq", "q": "What percentage of young people are affected by cyberbullying?",
                 "opts": ["a) 17%", "b) 27%", "c) 37%", "d) 47%"], "answer": "c"},
                {"type": "open", "q": "What is the 'echo chamber' effect? Explain in your own words.", "lines": 3},
                {"type": "tf", "q": "Social media has only positive effects on society.", "answer": "F"},
                {"type": "open", "q": "Write a balanced essay: Is social media a force for good or harm?", "lines": 6},
            ]},
        7: {"title": "Heroes Through History",
            "text": ("Every era produces heroes who change the course of history through courage, vision and "
                     "determination. Mustafa Kemal Ataturk founded the Turkish Republic in 1923 and introduced "
                     "sweeping reforms including women's suffrage, the Latin alphabet and secular education. "
                     "Mahatma Gandhi led India to independence through non-violent resistance. Rosa Parks refused "
                     "to give up her bus seat in 1955, sparking the American civil rights movement. Marie Curie "
                     "overcame gender barriers to become the first person to win Nobel Prizes in two different "
                     "sciences. Nelson Mandela endured 27 years in prison before becoming South Africa's first "
                     "democratically elected president. These individuals shared common traits: unwavering "
                     "commitment to their principles, the ability to inspire others, and willingness to "
                     "sacrifice personal comfort for the greater good. Importantly, heroism is not limited "
                     "to famous figures — teachers, doctors, firefighters and ordinary citizens perform heroic "
                     "acts every day."),
            "questions": [
                {"type": "mcq", "q": "When was the Turkish Republic founded?",
                 "opts": ["a) 1919", "b) 1920", "c) 1923", "d) 1938"], "answer": "c"},
                {"type": "open", "q": "What reforms did Ataturk introduce? Mention at least three.", "lines": 3},
                {"type": "tf", "q": "Heroism is only about famous people.", "answer": "F"},
                {"type": "open", "q": "Who is your personal hero? Write about their qualities and achievements.", "lines": 5},
            ]},
        8: {"title": "The Art of Narrative Writing",
            "text": ("Narrative writing tells a story — real or imagined — with a clear beginning, middle and "
                     "end. Great narratives create vivid images in the reader's mind through descriptive "
                     "language and sensory details. Instead of writing 'She was scared,' a skilled writer "
                     "might write 'Her heart pounded like a drum, and her hands trembled as she reached for "
                     "the door handle.' This technique is called 'show, don't tell.' Character development "
                     "is essential — readers need to care about the protagonist and understand their "
                     "motivations. Dialogue brings characters to life and moves the plot forward. A strong "
                     "narrative also includes conflict — a problem that the character must overcome. The "
                     "resolution should feel satisfying but not necessarily predictable. Literary devices "
                     "like metaphors, similes and foreshadowing add depth to the writing. Famous Turkish "
                     "writers like Orhan Pamuk and Elif Safak are masters of narrative technique, weaving "
                     "historical and cultural elements into compelling stories."),
            "questions": [
                {"type": "mcq", "q": "What does 'show, don't tell' mean in writing?",
                 "opts": ["a) Use pictures instead of words", "b) Use descriptive language instead of simple statements",
                          "c) Write shorter sentences", "d) Use more dialogue"], "answer": "b"},
                {"type": "open", "q": "Rewrite 'He was happy' using the 'show, don't tell' technique.", "lines": 2},
                {"type": "tf", "q": "A good narrative does not need conflict.", "answer": "F"},
                {"type": "open", "q": "Write the opening paragraph of a short story. Include setting, character and a hint of conflict.", "lines": 6},
            ]},
        9: {"title": "Global Citizenship",
            "text": ("In an increasingly interconnected world, the concept of global citizenship has gained "
                     "prominence. A global citizen is someone who is aware of the wider world, respects "
                     "diversity, understands how the world works economically, politically and culturally, "
                     "and takes action to make the world more equitable and sustainable. The COVID-19 pandemic "
                     "demonstrated how interconnected our world truly is — a virus that originated in one city "
                     "affected every country on Earth within months. Climate change is another challenge that "
                     "requires global cooperation. No single country can solve it alone. The Paris Agreement, "
                     "signed by 196 nations, aims to limit global warming to 1.5 degrees Celsius. Turkey "
                     "ratified the agreement in 2021. Global citizenship education helps young people develop "
                     "cross-cultural understanding, critical thinking and a sense of shared responsibility. "
                     "As students, you can start by learning about other cultures, engaging in community service, "
                     "and considering the global impact of your daily choices."),
            "questions": [
                {"type": "mcq", "q": "How many nations signed the Paris Agreement?",
                 "opts": ["a) 96", "b) 146", "c) 196", "d) 216"], "answer": "c"},
                {"type": "open", "q": "What are the qualities of a global citizen?", "lines": 3},
                {"type": "tf", "q": "Climate change can be solved by one country alone.", "answer": "F"},
                {"type": "open", "q": "How can you be a better global citizen? Write an action plan with 5 specific steps.", "lines": 5},
            ]},
        10: {"title": "Critical Thinking: Your Most Important Skill",
            "text": ("Critical thinking is the ability to analyse information objectively, evaluate evidence, "
                     "and form reasoned judgements. It is widely considered the most important skill for success "
                     "in the 21st century. Unlike memorisation, critical thinking involves questioning assumptions, "
                     "identifying biases, considering alternative perspectives and drawing logical conclusions. "
                     "The Socratic method, developed by the ancient Greek philosopher Socrates, remains one of "
                     "the most effective tools for developing critical thinking. It involves asking probing "
                     "questions to challenge beliefs and uncover deeper truths. In everyday life, critical "
                     "thinking helps us evaluate news reports, make informed consumer choices, solve complex "
                     "problems and avoid manipulation by misleading advertisements or propaganda. Studies show "
                     "that students who receive explicit critical thinking instruction perform better across all "
                     "subjects and are better prepared for university and careers. The good news is that critical "
                     "thinking is not an innate talent — it is a skill that can be developed through practice, "
                     "reading widely, engaging in debates and maintaining intellectual curiosity."),
            "questions": [
                {"type": "mcq", "q": "Who developed the Socratic method?",
                 "opts": ["a) Aristotle", "b) Plato", "c) Socrates", "d) Homer"], "answer": "c"},
                {"type": "open", "q": "What are the key components of critical thinking? List at least four.", "lines": 3},
                {"type": "tf", "q": "Critical thinking is an innate talent that cannot be learned.", "answer": "F"},
                {"type": "open", "q": "Apply critical thinking to a current news story. Analyse the source, evidence and potential biases.", "lines": 6},
            ]},
    },
}

_GRAMMAR_BANK = {
    5: {
        1: {"title": "Present Simple Tense", "rule": "Use the Present Simple for habits, routines and general facts.",
            "formula": "I/You/We/They + V1  |  He/She/It + V1 + s/es\nNegative: don't / doesn't + V1  |  Question: Do/Does + S + V1?",
            "examples": [("I wake up at seven every day.", "+"), ("She goes to school by bus.", "+"),
                         ("We don't watch TV on weekdays.", "-"), ("Does he play tennis?", "?")],
            "exercises": [("I always _____ (brush) my teeth after breakfast.", "brush"),
                         ("She _____ (have) lunch at twelve o'clock.", "has"),
                         ("_____ you _____ (like) Science? (question)", "Do ... like"),
                         ("He _____ (not/play) basketball on Sundays.", "doesn't play"),
                         ("My parents _____ (work) in an office.", "work"),
                         ("The Earth _____ (go) around the Sun.", "goes")]},
        2: {"title": "Have/Has & Possessive Adjectives", "rule": "Use 'have/has' to describe features. Possessive adjectives show ownership.",
            "formula": "I/You/We/They + have  |  He/She/It + has\nPossessives: my, your, his, her, its, our, their",
            "examples": [("She has long brown hair.", "+"), ("He has blue eyes.", "+"),
                         ("My brother is tall.", "adj"), ("Their house is big.", "adj")],
            "exercises": [("My sister _____ (have) curly hair.", "has"),
                         ("_____ (I) father is a doctor.", "My"),
                         ("They _____ (have) two cats.", "have"),
                         ("_____ (She) name is Zeynep.", "Her"),
                         ("We _____ (have) a big garden.", "have"),
                         ("Is that _____ (you) bag?", "your")]},
        3: {"title": "There is/are & Prepositions of Place", "rule": "Use 'there is' for singular and 'there are' for plural. Prepositions show location.",
            "formula": "There is + singular  |  There are + plural\nPrepositions: next to, opposite, between, near, across from, behind, in front of",
            "examples": [("There is a park next to my house.", "+"), ("There are two shops on this street.", "+"),
                         ("The bank is opposite the hospital.", "prep"), ("Go straight and turn left.", "dir")],
            "exercises": [("There _____ a library near the school.", "is"),
                         ("There _____ three cinemas in our town.", "are"),
                         ("The park is _____ the mosque and the school.", "between"),
                         ("_____ there any shops near here?", "Are"),
                         ("The pharmacy is _____ _____ the bakery.", "across from"),
                         ("There _____ (not) a swimming pool in our neighbourhood.", "isn't")]},
        4: {"title": "Can/Can't & Present Continuous", "rule": "Use 'can' for ability. Use Present Continuous for actions happening right now.",
            "formula": "can/can't + V1 (base form)\nam/is/are + V-ing (for actions happening now)",
            "examples": [("I can swim very well.", "+"), ("She can't play the guitar.", "-"),
                         ("It is raining outside.", "cont"), ("They are playing football now.", "cont")],
            "exercises": [("I _____ ride a bicycle. (ability: yes)", "can"),
                         ("She _____ speak three languages. (ability: no)", "can't"),
                         ("Look! It _____ (snow) outside!", "is snowing"),
                         ("We _____ (play) tennis right now.", "are playing"),
                         ("_____ you _____ (do) your homework now?", "Are ... doing"),
                         ("He _____ (not/listen) to music at the moment.", "isn't listening")]},
        5: {"title": "Countable & Uncountable Nouns", "rule": "Countable nouns can be singular or plural. Uncountable nouns have no plural form.",
            "formula": "How many + countable (plural)?  |  How much + uncountable?\nQuantifiers: some, any, a lot of, a few (countable), a little (uncountable)",
            "examples": [("How many apples do you want?", "count"), ("How much water do you need?", "uncount"),
                         ("There is some milk in the fridge.", "+"), ("Are there any eggs?", "?")],
            "exercises": [("How _____ oranges are there?", "many"),
                         ("How _____ sugar do we need?", "much"),
                         ("There is _____ bread on the table.", "some"),
                         ("Are there _____ tomatoes in the basket?", "any"),
                         ("We have _____ _____ butter left. (small amount)", "a little"),
                         ("I bought _____ _____ bananas. (small number)", "a few")]},
        6: {"title": "Like/Enjoy/Love + V-ing", "rule": "Use verb + -ing after like, love, enjoy, hate, prefer, don't mind.",
            "formula": "Subject + like/love/enjoy/hate + V-ing\nAdverbs of frequency: always > usually > often > sometimes > rarely > never",
            "examples": [("I love playing the guitar.", "+"), ("She enjoys reading books.", "+"),
                         ("He hates getting up early.", "-"), ("I sometimes watch horror films.", "freq")],
            "exercises": [("I enjoy _____ (swim) in the sea.", "swimming"),
                         ("She likes _____ (dance) to pop music.", "dancing"),
                         ("We don't mind _____ (wait) for a few minutes.", "waiting"),
                         ("He hates _____ (do) housework.", "doing"),
                         ("Do you enjoy _____ (cook)?", "cooking"),
                         ("They love _____ (travel) to new places.", "travelling")]},
        7: {"title": "Simple Past Tense", "rule": "Use the Simple Past for completed actions in the past.",
            "formula": "Regular: V + ed (played, watched, visited)\nIrregular: go→went, see→saw, eat→ate, buy→bought, make→made\nNeg: didn't + V1  |  Q: Did + S + V1?",
            "examples": [("I visited the zoo last week.", "+"), ("She went to Istanbul yesterday.", "+"),
                         ("We didn't buy any souvenirs.", "-"), ("Did you see the elephants?", "?")],
            "exercises": [("I _____ (visit) my grandmother last Sunday.", "visited"),
                         ("She _____ (go) to school by bus yesterday.", "went"),
                         ("We _____ (see) a great film last night.", "saw"),
                         ("_____ you _____ (eat) breakfast this morning?", "Did ... eat"),
                         ("They _____ (not/play) tennis yesterday.", "didn't play"),
                         ("He _____ (buy) a new book last week.", "bought")]},
        8: {"title": "Be Going To (Future Plans)", "rule": "Use 'be going to + V1' for future plans and intentions.",
            "formula": "am/is/are + going to + V1\nNeg: am/is/are + not + going to + V1\nQ: Am/Is/Are + S + going to + V1?",
            "examples": [("I am going to visit Antalya.", "+"), ("She is going to study medicine.", "+"),
                         ("We aren't going to play tomorrow.", "-"), ("Are you going to travel?", "?")],
            "exercises": [("I _____ (go/visit) my aunt next week.", "am going to visit"),
                         ("She _____ (go/buy) a new phone.", "is going to buy"),
                         ("We _____ (not/go/travel) this summer.", "aren't going to travel"),
                         ("_____ they _____ (go/come) to the party?", "Are ... going to come"),
                         ("He _____ (go/learn) Spanish next year.", "is going to learn"),
                         ("I _____ (go/be) a doctor when I grow up.", "am going to be")]},
        9: {"title": "Should / Must / Have to", "rule": "Should = advice | Must = strong obligation | Have to = external obligation",
            "formula": "should/must/have to + V1 (base form)\nNeg: shouldn't / mustn't / don't have to + V1",
            "examples": [("You should eat more vegetables.", "advice"), ("Students must be quiet in the library.", "oblig"),
                         ("I have to wear a uniform at school.", "ext"), ("You mustn't run in the corridor.", "prohib")],
            "exercises": [("You _____ drink more water. (advice)", "should"),
                         ("Students _____ cheat in exams. (prohibition)", "mustn't"),
                         ("I _____ _____ _____ finish my project by Friday. (external obligation)", "have to"),
                         ("You _____ be more careful when crossing the road. (advice)", "should"),
                         ("We _____ respect our teachers. (strong obligation)", "must"),
                         ("She _____ _____ _____ wake up early tomorrow. (no obligation)", "doesn't have to")]},
        10: {"title": "Linking Words & Sequencing", "rule": "Use linking words to connect ideas and organise your writing.",
             "formula": "Sequence: first, then, next, after that, finally\nReason: because, so, therefore\nContrast: but, however, although",
             "examples": [("First, I woke up. Then, I had breakfast.", "seq"), ("I studied hard because I wanted to pass.", "reason"),
                          ("It was raining, but we went out.", "contrast"), ("She was tired, so she went to bed.", "result")],
             "exercises": [("_____, wash your hands. _____, sit down for dinner.", "First ... Then"),
                          ("I like swimming _____ I don't like running.", "but"),
                          ("She studied hard _____ she wanted to get good marks.", "because"),
                          ("It was cold. _____, we stayed inside.", "Therefore"),
                          ("_____ it was raining, we had a picnic.", "Although"),
                          ("He finished his homework. _____, he played games.", "After that")]},
    },
    6: {
        1: {"title": "Comparative & Superlative Adjectives",
            "rule": "Use comparatives to compare two things. Use superlatives to compare three or more.",
            "formula": "Short adj: adj+er ... than / the adj+est\nLong adj: more + adj ... than / the most + adj\nIrregular: good→better→best, bad→worse→worst",
            "examples": [("Cities are bigger than villages.", "comp"), ("Tokyo is the largest city in the world.", "super"),
                         ("Country life is more peaceful than city life.", "comp"), ("This is the most interesting book I've read.", "super")],
            "exercises": [("Istanbul is _____ (big) than Ankara.", "bigger"),
                         ("She is the _____ (intelligent) student in our class.", "most intelligent"),
                         ("This film is _____ (good) than the last one.", "better"),
                         ("Mount Everest is the _____ (high) mountain in the world.", "highest"),
                         ("English is _____ (easy) than Chinese for Turkish speakers.", "easier"),
                         ("What is the _____ (bad) weather you have ever experienced?", "worst")]},
        2: {"title": "Past Simple — Biographies",
            "rule": "Use the Past Simple to describe events in a person's life. Use time expressions to sequence events.",
            "formula": "was/were born in + year/place\nV2 (past form) for completed actions\nTime expressions: in 1867, at the age of, when, after, later",
            "examples": [("Marie Curie was born in Warsaw in 1867.", "+"), ("She moved to Paris when she was 24.", "+"),
                         ("They discovered radium in 1898.", "+"), ("She won two Nobel Prizes.", "+")],
            "exercises": [("Ataturk _____ (be born) in 1881 in Thessaloniki.", "was born"),
                         ("He _____ (study) at the Military Academy.", "studied"),
                         ("She _____ (become) famous after her discovery.", "became"),
                         ("Einstein _____ (not/go) to a regular school.", "didn't go"),
                         ("_____ Da Vinci _____ (paint) the Mona Lisa?", "Did ... paint"),
                         ("They _____ (win) the Nobel Prize in 1903.", "won")]},
        3: {"title": "There is/are & Quantifiers (Review)",
            "rule": "Describe rooms and houses using there is/are with quantifiers.",
            "formula": "There is + a/an/some + uncountable/singular\nThere are + some/many/a few + plural\nQuestion: Is/Are there...?\nNeg: There isn't/aren't...",
            "examples": [("There is a big garden behind the house.", "+"), ("There are three bedrooms upstairs.", "+"),
                         ("Is there a swimming pool?", "?"), ("There aren't any shops nearby.", "-")],
            "exercises": [("There _____ a fireplace in the living room.", "is"),
                         ("_____ there _____ bookshelves in your room?", "Are ... any"),
                         ("There _____ some milk in the fridge.", "is"),
                         ("There _____ (not) any parks near my house.", "aren't"),
                         ("How many rooms _____ there in your house?", "are"),
                         ("There _____ a lot of traffic in the city centre.", "is")]},
        4: {"title": "Present Perfect with ever/never/just/already/yet",
            "rule": "Use Present Perfect to talk about experiences and recent events.",
            "formula": "Have you ever + V3? (experience)\nI have never + V3. (no experience)\njust = a moment ago | already = sooner than expected | yet = until now (neg/question)",
            "examples": [("Have you ever ridden a horse?", "?"), ("I have never seen snow.", "-"),
                         ("She has just arrived.", "recent"), ("They haven't finished yet.", "-")],
            "exercises": [("_____ you ever _____ (eat) sushi?", "Have ... eaten"),
                         ("I have _____ (never/visit) Paris.", "never visited"),
                         ("He has _____ (just/finish) his homework.", "just finished"),
                         ("We haven't _____ (start) the project _____.", "started ... yet"),
                         ("She has _____ (already/read) that book.", "already read"),
                         ("_____ they _____ (arrive) yet?", "Have ... arrived")]},
        5: {"title": "Countable/Uncountable & some/any/much/many",
            "rule": "Distinguish countable and uncountable food nouns. Use correct quantifiers.",
            "formula": "Countable: a/an, many, a few, How many?\nUncountable: some, much, a little, How much?\nsome = affirmative | any = negative/question",
            "examples": [("How many tomatoes do we need?", "count"), ("How much rice is there?", "uncount"),
                         ("There are some bananas.", "+"), ("There isn't any butter.", "-")],
            "exercises": [("How _____ eggs do we need for the cake?", "many"),
                         ("There isn't _____ cheese left.", "any"),
                         ("I need a _____ sugar for my tea. (small amount)", "little"),
                         ("How _____ flour do we need?", "much"),
                         ("There are _____ _____ apples in the basket. (small number)", "a few"),
                         ("Would you like _____ tea?", "some")]},
        6: {"title": "Going to & Will (Future)",
            "rule": "Use 'going to' for plans. Use 'will' for spontaneous decisions and predictions.",
            "formula": "Plans: am/is/are + going to + V1\nDecisions: will + V1\nPredictions: will + V1 / be going to + V1",
            "examples": [("We are going to visit Antalya next summer.", "plan"), ("I think it will rain tomorrow.", "predict"),
                         ("I'll help you carry those bags.", "decision"), ("She is going to study medicine.", "plan")],
            "exercises": [("I _____ (go/visit) my grandparents this weekend. (plan)", "am going to visit"),
                         ("Oh no, I forgot! I _____ (call) her right now. (decision)", "will call"),
                         ("Look at those clouds! It _____ (go/rain). (evidence)", "is going to rain"),
                         ("I think Turkey _____ (win) the match. (prediction)", "will win"),
                         ("We _____ (not/go/travel) abroad this year. (plan)", "aren't going to travel"),
                         ("_____ you _____ (help) me with my homework? (request)", "Will ... help")]},
        7: {"title": "Ability: can/could/be able to",
            "rule": "Express abilities and talents using can, could and be able to.",
            "formula": "Present: can/can't + V1\nPast: could/couldn't + V1\nFuture/Perfect: will be able to + V1 / have been able to + V1",
            "examples": [("She can play the violin beautifully.", "+"), ("I couldn't swim when I was five.", "-"),
                         ("He will be able to speak three languages.", "fut"), ("Can you ride a bike?", "?")],
            "exercises": [("My sister _____ speak four languages. (present ability)", "can"),
                         ("I _____ (not/swim) when I was three, but now I can.", "couldn't"),
                         ("_____ you _____ (play) chess?", "Can ... play"),
                         ("After this course, you _____ _____ _____ use the software. (future)", "will be able to"),
                         ("She _____ (could/read) when she was four.", "could read"),
                         ("He _____ (not/can) come to the party yesterday.", "couldn't")]},
        8: {"title": "Superlatives & Geography",
            "rule": "Use superlatives to describe extreme features of places.",
            "formula": "the + adj+est (short adj) | the most + adj (long adj)\nIrregular: the best, the worst, the farthest/furthest",
            "examples": [("The Nile is the longest river in Africa.", "+"), ("Everest is the highest mountain.", "+"),
                         ("Istanbul is the most visited city in Turkey.", "+"), ("Antarctica is the coldest continent.", "+")],
            "exercises": [("Lake Van is the _____ (large) lake in Turkey.", "largest"),
                         ("The Amazon is the _____ (wide) river in the world.", "widest"),
                         ("What is the _____ (beautiful) place you have ever visited?", "most beautiful"),
                         ("The cheetah is the _____ (fast) animal on land.", "fastest"),
                         ("This is the _____ (good) holiday I have ever had!", "best"),
                         ("Antarctica is the _____ (cold) and _____ (dry) continent.", "coldest ... driest")]},
        9: {"title": "Should/Must/Have to (Obligations & Advice)",
            "rule": "Express obligations, advice and rules using modal verbs.",
            "formula": "should = advice (You should study.)\nmust = strong obligation (You must wear a seatbelt.)\nhave to = external rule (I have to wear a uniform.)\nmustn't = prohibition | don't have to = no obligation",
            "examples": [("You should drink more water.", "advice"), ("Students must be on time.", "obligation"),
                         ("We have to wear uniforms at school.", "rule"), ("You mustn't use your phone in class.", "prohib")],
            "exercises": [("You _____ eat more vegetables. (advice)", "should"),
                         ("Students _____ run in the corridors. (prohibition)", "mustn't"),
                         ("I _____ _____ _____ wake up early on Saturdays. (no obligation)", "don't have to"),
                         ("You _____ wear a helmet when cycling. (strong rule)", "must"),
                         ("He _____ (should/study) harder for the exam.", "should study"),
                         ("We _____ _____ _____ submit the project by Friday. (external deadline)", "have to")]},
        10: {"title": "Giving Advice: If I were you...",
            "rule": "Give advice using second conditional and fixed expressions.",
            "formula": "If I were you, I would + V1.\nYou'd better + V1.\nWhy don't you + V1?\nHow about + V-ing?",
            "examples": [("If I were you, I would see a doctor.", "advice"), ("You'd better study tonight.", "strong"),
                         ("Why don't you join a sports club?", "suggest"), ("How about taking a break?", "suggest")],
            "exercises": [("If I _____ you, I _____ apologise to her.", "were ... would"),
                         ("You'd _____ hurry up or we'll be late.", "better"),
                         ("_____ don't you try a different approach?", "Why"),
                         ("How _____ going for a walk?", "about"),
                         ("If I were you, I _____ (not/eat) so much junk food.", "wouldn't eat"),
                         ("You _____ talk to your teacher about it. (advice)", "should")]},
    },
    7: {
        1: {"title": "Present Perfect Tense",
            "rule": "Use the Present Perfect for experiences, recent events, and situations that started in the past and continue now.",
            "formula": "have/has + V3 (past participle)\nKey words: ever, never, already, yet, just, since, for",
            "examples": [("I have visited three countries.", "exp"), ("She has never eaten sushi.", "exp"),
                         ("They have just finished their project.", "recent"), ("He has lived here since 2019.", "cont")],
            "exercises": [("I _____ never _____ (see) a whale.", "have ... seen"),
                         ("She _____ already _____ (finish) her homework.", "has ... finished"),
                         ("_____ you ever _____ (travel) abroad?", "Have ... travelled"),
                         ("We _____ (know) each other since primary school.", "have known"),
                         ("He _____ (not/try) Turkish coffee yet.", "hasn't tried"),
                         ("They _____ (live) in this city for ten years.", "have lived")]},
        2: {"title": "Past Simple vs Present Perfect",
            "rule": "Past Simple = finished time. Present Perfect = unfinished time or no specific time.",
            "formula": "Past Simple: V2 + ago/yesterday/last week/in 2020\nPresent Perfect: have/has + V3 + ever/never/just/already/yet/since/for",
            "examples": [("I visited London last summer. (finished)", "PS"), ("I have visited London three times. (no specific time)", "PP"),
                         ("She lived there for five years. (she doesn't live there now)", "PS"), ("She has lived there since 2020. (she still lives there)", "PP")],
            "exercises": [("I _____ (go) to Antalya last July.", "went"),
                         ("She _____ (be) to Paris twice.", "has been"),
                         ("We _____ (move) here in 2019.", "moved"),
                         ("_____ you _____ (see) that film yet?", "Have ... seen"),
                         ("He _____ (break) his leg last month.", "broke"),
                         ("They _____ (not/finish) the project yet.", "haven't finished")]},
        3: {"title": "Relative Clauses (who/which/that/where)",
            "rule": "Use relative clauses to give extra information about people, things and places.",
            "formula": "who = people | which = things | that = people/things | where = places\nDefining: essential info (no commas) | Non-defining: extra info (commas)",
            "examples": [("The teacher who teaches us English is very kind.", "who"), ("This is the book which I told you about.", "which"),
                         ("The city where I was born is Istanbul.", "where"), ("She is the girl that won the competition.", "that")],
            "exercises": [("The man _____ lives next door is a doctor.", "who"),
                         ("This is the phone _____ I bought yesterday.", "which/that"),
                         ("The school _____ I study is very modern.", "where"),
                         ("The students _____ passed the exam are very happy.", "who/that"),
                         ("The film _____ we watched last night was amazing.", "which/that"),
                         ("Istanbul, _____ is Turkey's largest city, has 16 million people.", "which")]},
        4: {"title": "Passive Voice (Present & Past)",
            "rule": "Use the passive when the action is more important than who does it.",
            "formula": "Present: am/is/are + V3\nPast: was/were + V3\nBy + agent (optional)",
            "examples": [("English is spoken all over the world.", "present"), ("The Pyramids were built thousands of years ago.", "past"),
                         ("This song was written by a Turkish composer.", "by"), ("Fake news is shared on social media every day.", "present")],
            "exercises": [("English _____ (speak) in many countries.", "is spoken"),
                         ("The school _____ (build) in 1965.", "was built"),
                         ("These photos _____ (take) by my sister.", "were taken"),
                         ("Millions of emails _____ (send) every day.", "are sent"),
                         ("The book _____ (write) by Orhan Pamuk.", "was written"),
                         ("_____ this bridge _____ (design) by a famous architect?", "Was ... designed")]},
        5: {"title": "Conditionals: First & Second",
            "rule": "First conditional = real/possible future. Second conditional = unreal/imaginary present.",
            "formula": "First: If + Present Simple, will + V1 (If it rains, I will stay home.)\nSecond: If + Past Simple, would + V1 (If I had wings, I would fly.)",
            "examples": [("If you study hard, you will pass the exam.", "1st"), ("If I were a bird, I would fly to Africa.", "2nd"),
                         ("If it rains tomorrow, we won't go to the park.", "1st"), ("If I had a million dollars, I would travel the world.", "2nd")],
            "exercises": [("If she _____ (study) hard, she _____ (pass) the exam.", "studies ... will pass"),
                         ("If I _____ (be) you, I _____ (apologise).", "were ... would apologise"),
                         ("If it _____ (rain) tomorrow, we _____ (stay) home.", "rains ... will stay"),
                         ("If I _____ (have) a time machine, I _____ (visit) ancient Rome.", "had ... would visit"),
                         ("We _____ (go) to the beach if the weather _____ (be) nice.", "will go ... is"),
                         ("If she _____ (can) fly, she _____ (visit) every country.", "could ... would visit")]},
        6: {"title": "Quantifiers & Articles (Review)",
            "rule": "Use quantifiers and articles correctly with science and space vocabulary.",
            "formula": "a/an = one (non-specific) | the = specific/unique\nsome/any | much/many | a lot of | a few/a little | every/each | no/none",
            "examples": [("The Sun is a star.", "the"), ("There are a lot of galaxies in the universe.", "quant"),
                         ("Every planet has a different atmosphere.", "every"), ("There is no life on Mars (as far as we know).", "no")],
            "exercises": [("_____ Moon orbits _____ Earth.", "The ... the"),
                         ("There are _____ _____ _____ stars in the galaxy.", "a lot of"),
                         ("Is there _____ water on Mars?", "any"),
                         ("_____ astronaut needs special training.", "Every"),
                         ("There is _____ oxygen on the Moon.", "no"),
                         ("Scientists have found _____ _____ evidence of water. (small amount)", "a little")]},
        7: {"title": "Used to & Would (Past Habits)",
            "rule": "Describe past habits and situations that are no longer true.",
            "formula": "used to + V1 (past habits/states that changed)\nwould + V1 (repeated past actions only, NOT states)\ndidn't use to + V1 | Did you use to + V1?",
            "examples": [("I used to live in Ankara.", "state"), ("We would play football every weekend.", "habit"),
                         ("She didn't use to like vegetables.", "-"), ("Did you use to walk to school?", "?")],
            "exercises": [("I _____ _____ _____ play in the park every day. (past habit)", "used to"),
                         ("She _____ _____ _____ like English, but now she loves it.", "didn't use to"),
                         ("We _____ visit our grandparents every Sunday. (repeated action)", "would"),
                         ("_____ you _____ _____ have a pet when you were young?", "Did ... use to"),
                         ("He _____ _____ _____ be very shy. (past state)", "used to"),
                         ("They _____ go camping every summer. (repeated past action)", "would")]},
        8: {"title": "Present Perfect Continuous",
            "rule": "Use Present Perfect Continuous for actions that started in the past and are still continuing.",
            "formula": "have/has + been + V-ing\nKey words: for, since, all day, How long...?",
            "examples": [("I have been studying English for six years.", "+"), ("She has been reading since morning.", "+"),
                         ("How long have you been waiting?", "?"), ("It has been raining all day.", "+")],
            "exercises": [("She _____ _____ _____ (work) here since 2020.", "has been working"),
                         ("How long _____ you _____ _____ (learn) English?", "have ... been learning"),
                         ("We _____ _____ _____ (wait) for an hour.", "have been waiting"),
                         ("It _____ _____ _____ (snow) all morning.", "has been snowing"),
                         ("They _____ _____ _____ (live) in this city for ten years.", "have been living"),
                         ("I _____ _____ _____ (study) since 3 o'clock.", "have been studying")]},
        9: {"title": "Causative: have/get something done",
            "rule": "Use causative to say someone else does something for you.",
            "formula": "have + object + V3 (He had his car washed.)\nget + object + V3 (She got her hair cut.)\nneed + V-ing / need to be + V3",
            "examples": [("I had my phone repaired.", "have"), ("She got her hair dyed.", "get"),
                         ("The car needs washing.", "need"), ("This document needs to be signed.", "need")],
            "exercises": [("I need to _____ my passport _____ (renew).", "have ... renewed"),
                         ("She _____ her nails _____ (do) every week.", "gets ... done"),
                         ("We _____ the house _____ (paint) last month.", "had ... painted"),
                         ("This shirt needs _____ (iron).", "ironing"),
                         ("He _____ his eyes _____ (test) yesterday.", "had ... tested"),
                         ("The garden needs _____ _____ _____ (cut).", "to be cut")]},
        10: {"title": "Connectors & Linking Words",
            "rule": "Use connectors to link ideas in paragraphs and essays.",
            "formula": "Addition: also, moreover, furthermore, in addition\nContrast: however, although, despite, on the other hand\nCause/Effect: because, therefore, as a result, due to\nSequence: firstly, then, finally, in conclusion",
            "examples": [("Although it was raining, we went out.", "contrast"), ("She studied hard; therefore, she passed.", "result"),
                         ("Moreover, the project was completed on time.", "addition"), ("In conclusion, education is essential.", "sequence")],
            "exercises": [("_____ it was cold, we enjoyed the trip.", "Although"),
                         ("She was tired; _____, she kept working.", "however"),
                         ("He failed the exam _____ he didn't study.", "because"),
                         ("The roads were icy. _____ _____ _____, many accidents occurred.", "As a result"),
                         ("_____, I would like to thank everyone.", "Finally"),
                         ("_____ _____ the rain, the match was cancelled.", "Due to")]},
    },
    8: {
        1: {"title": "Reported Speech",
            "rule": "Use reported speech to tell someone what another person said. Change tense, pronouns and time expressions.",
            "formula": "Direct: 'I am happy,' she said.\nReported: She said (that) she was happy.\nPresent→Past | will→would | can→could | here→there | today→that day",
            "examples": [("'I love English,' he said. → He said he loved English.", "state"),
                         ("'I will help you,' she said. → She said she would help me.", "will"),
                         ("'Can you swim?' he asked. → He asked if I could swim.", "question")],
            "exercises": [("'I am tired,' she said. → She said she _____ tired.", "was"),
                         ("'We will come tomorrow,' they said. → They said they _____ come the next day.", "would"),
                         ("'I can speak French,' he said. → He said he _____ speak French.", "could"),
                         ("'Do you like pizza?' she asked. → She asked _____ I liked pizza.", "if/whether"),
                         ("'I have finished,' he said. → He said he _____ finished.", "had"),
                         ("'Don't run!' the teacher said. → The teacher told us _____ to run.", "not")]},
        2: {"title": "Passive Voice (All Tenses)",
            "rule": "Form passive in present, past, future and perfect tenses.",
            "formula": "Present: is/are + V3 | Past: was/were + V3\nFuture: will be + V3 | Present Perfect: has/have been + V3\nModal: can/should/must + be + V3",
            "examples": [("The report will be published tomorrow.", "fut"), ("The bridge has been repaired.", "pp"),
                         ("This problem can be solved easily.", "modal"), ("The decision was made by the committee.", "past")],
            "exercises": [("The new hospital _____ _____ (build) next year.", "will be built"),
                         ("The homework _____ already _____ _____ (submit).", "has ... been submitted"),
                         ("This essay _____ _____ (write) in one hour.", "can be written"),
                         ("The invitations _____ _____ _____ (send) yet.", "haven't been sent"),
                         ("The Hagia Sophia _____ (convert) into a mosque in 2020.", "was converted"),
                         ("_____ the results _____ _____ (announce) yet?", "Have ... been announced")]},
        3: {"title": "Wish Clauses & If only",
            "rule": "Express wishes about unreal present or past situations.",
            "formula": "Present wish: I wish + Past Simple (I wish I knew the answer.)\nPast wish: I wish + Past Perfect (I wish I had studied harder.)\nIf only = stronger wish",
            "examples": [("I wish I spoke better English.", "present"), ("If only I had listened to my teacher.", "past"),
                         ("She wishes she could fly.", "present"), ("I wish I hadn't said that.", "past regret")],
            "exercises": [("I wish I _____ (know) the answer. (but I don't)", "knew"),
                         ("If only she _____ (study) harder last year. (regret)", "had studied"),
                         ("He wishes he _____ (can) play the piano.", "could"),
                         ("I wish I _____ (not/eat) so much yesterday.", "hadn't eaten"),
                         ("If only we _____ (have) more time.", "had"),
                         ("She wishes she _____ (be) taller.", "were")]},
        4: {"title": "Relative Clauses: Defining & Non-defining",
            "rule": "Use relative clauses to add information. Non-defining clauses use commas.",
            "formula": "Defining: The man who called is my uncle. (essential — no commas)\nNon-defining: My uncle, who lives in Ankara, called me. (extra info — commas)\nwhose = possession | whom = formal object",
            "examples": [("The scientist whose research won the prize is Turkish.", "whose"), ("Ankara, which is the capital, is in central Turkey.", "non-def"),
                         ("The teacher whom I admire most is retiring.", "whom"), ("That's the book that changed my life.", "def")],
            "exercises": [("The woman _____ bag was stolen called the police.", "whose"),
                         ("Istanbul, _____ has 16 million people, is Turkey's largest city.", "which"),
                         ("The author _____ I met at the book fair was very kind.", "whom/who"),
                         ("The student _____ won the prize is from our class.", "who/that"),
                         ("CERN, _____ is in Switzerland, studies particle physics.", "which"),
                         ("The country _____ flag has a crescent is Turkey.", "whose")]},
        5: {"title": "Third Conditional (Past Unreal)",
            "rule": "Talk about imaginary past situations and their results.",
            "formula": "If + Past Perfect, would have + V3\nIf I had studied, I would have passed.\nMixed: If + Past Perfect, would + V1 (past cause → present result)",
            "examples": [("If I had woken up earlier, I wouldn't have missed the bus.", "3rd"), ("If she had studied, she would have passed.", "3rd"),
                         ("If they had invented the internet earlier, life would be different now.", "mixed")],
            "exercises": [("If I _____ (study) harder, I _____ _____ _____ (pass) the exam.", "had studied ... would have passed"),
                         ("If she _____ (not/miss) the train, she _____ _____ _____ (arrive) on time.", "hadn't missed ... would have arrived"),
                         ("If we _____ (know) about the traffic, we _____ _____ _____ (leave) earlier.", "had known ... would have left"),
                         ("He _____ _____ _____ (not/get) lost if he _____ (use) a map.", "wouldn't have got ... had used"),
                         ("If they _____ (listen) to the warning, the accident _____ _____ _____ (not/happen).", "had listened ... wouldn't have happened"),
                         ("What _____ you _____ _____ (do) if you _____ (be) there?", "would ... have done ... had been")]},
        6: {"title": "Modals of Deduction (must/might/can't)",
            "rule": "Make deductions and express degrees of certainty.",
            "formula": "must + V1 = almost certain (She must be at home.)\nmight/may/could + V1 = possible (He might be ill.)\ncan't + V1 = almost certain NOT (That can't be true.)\nmust have + V3 / can't have + V3 = past deduction",
            "examples": [("She must be tired — she worked all day.", "certain"), ("He might be at the library.", "possible"),
                         ("That can't be right — check the facts.", "impossible"), ("They must have left already.", "past")],
            "exercises": [("She's not answering. She _____ be asleep.", "must"),
                         ("I'm not sure. He _____ be at the gym.", "might"),
                         ("He's only 10. He _____ drive a car.", "can't"),
                         ("They _____ _____ _____ (leave) already — the car is gone.", "must have left"),
                         ("She _____ _____ _____ (forget) — she never forgets.", "can't have forgotten"),
                         ("He _____ _____ _____ (take) the wrong bus.", "might have taken")]},
        7: {"title": "Past Perfect & Narrative Tenses",
            "rule": "Use Past Perfect to describe an action before another past action.",
            "formula": "had + V3 (before another past event)\nPast Simple for the main event\nBy the time + Past Simple, ... had + V3",
            "examples": [("When I arrived, the film had already started.", "+"), ("She had never seen snow before she went to Uludag.", "+"),
                         ("By the time we got home, it had stopped raining.", "+"), ("After he had finished dinner, he went to bed.", "+")],
            "exercises": [("When I arrived, the train _____ already _____ (leave).", "had ... left"),
                         ("She _____ never _____ (travel) abroad before 2020.", "had ... travelled"),
                         ("By the time we reached the cinema, the film _____ (start).", "had started"),
                         ("After he _____ (read) the letter, he smiled.", "had read"),
                         ("I _____ (not/eat) anything all day, so I was very hungry.", "hadn't eaten"),
                         ("_____ you _____ (finish) your homework before your friends came?", "Had ... finished")]},
        8: {"title": "Phrasal Verbs & Collocations",
            "rule": "Learn common phrasal verbs and collocations for storytelling.",
            "formula": "Phrasal verb = verb + particle (look up, give up, turn out, carry on)\nCollocation = words that go together (make a decision, take a photo, do research)",
            "examples": [("I looked up the word in the dictionary.", "PV"), ("She gave up smoking last year.", "PV"),
                         ("The project turned out well.", "PV"), ("We need to make a decision soon.", "coll")],
            "exercises": [("Don't _____ _____! Keep trying! (stop trying)", "give up"),
                         ("Can you _____ _____ the volume? It's too quiet.", "turn up"),
                         ("I need to _____ _____ a new word. (search for info)", "look up"),
                         ("She _____ a mistake on the test. (make/do)", "made"),
                         ("We should _____ research before the presentation. (make/do)", "do"),
                         ("He _____ a photo of the sunset. (make/take)", "took")]},
        9: {"title": "Gerunds & Infinitives",
            "rule": "Some verbs are followed by gerund (-ing), some by infinitive (to + V1).",
            "formula": "V + -ing: enjoy, avoid, consider, mind, suggest, practise, finish\nV + to + V1: want, decide, hope, plan, agree, refuse, learn\nBoth (meaning change): stop, remember, forget, try",
            "examples": [("I enjoy learning new languages.", "ger"), ("She decided to study abroad.", "inf"),
                         ("He stopped smoking. (quit)", "ger"), ("He stopped to smoke. (paused in order to)", "inf")],
            "exercises": [("I enjoy _____ (read) science fiction novels.", "reading"),
                         ("She decided _____ (apply) for the scholarship.", "to apply"),
                         ("Would you mind _____ (close) the window?", "closing"),
                         ("He agreed _____ (help) us with the project.", "to help"),
                         ("I remember _____ (visit) Cappadocia as a child. (memory)", "visiting"),
                         ("Don't forget _____ (bring) your passport. (reminder)", "to bring")]},
        10: {"title": "All Tenses Review & Error Correction",
            "rule": "Identify and correct common tense errors in complex sentences.",
            "formula": "12 tenses: Present/Past/Future × Simple/Continuous/Perfect/Perfect Continuous\nKey: match the tense to the time expression and context",
            "examples": [("I have been living here since 2010.", "PP Cont"), ("By the time he arrives, we will have finished.", "Fut Perf"),
                         ("She was reading while he was cooking.", "Past Cont"), ("If I had known, I would have helped.", "3rd Cond")],
            "exercises": [("She _____ (live) in Istanbul since she was born.", "has lived / has been living"),
                         ("By next June, I _____ _____ _____ (study) English for 8 years.", "will have been studying"),
                         ("While I _____ (walk) home, I _____ (see) an accident.", "was walking ... saw"),
                         ("He _____ (not/finish) the book yet.", "hasn't finished"),
                         ("If she _____ (tell) me, I _____ _____ _____ (help) her.", "had told ... would have helped"),
                         ("By the time you read this, I _____ already _____ (leave).", "will ... have left")]},
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# DIALOGUE BANK — Grade 5 (real-life conversations)
# ══════════════════════════════════════════════════════════════════════════════

_DIALOGUE_BANK = {
    5: {
        1: {"title": "First Day at School", "setting": "In the classroom",
            "lines": [
                ("A (Teacher)", "Good morning, class! Welcome to 5th grade. My name is Ms. Johnson."),
                ("B (Student)", "Good morning, Ms. Johnson! My name is Elif. Nice to meet you."),
                ("A", "Nice to meet you too, Elif. What is your favourite subject?"),
                ("B", "I love English and Science. What about the others?"),
                ("A", "That's great! We have English on Monday, Wednesday and Friday."),
                ("B", "Wonderful! I can't wait to start learning!"),
            ],
            "task": "Practise the dialogue with a partner. Then change the names and subjects to make your own version."},
        2: {"title": "Describing a Friend", "setting": "At the park",
            "lines": [
                ("A", "Hey, do you know the new student in our class?"),
                ("B", "Yes! Her name is Zeynep. She has long brown hair and green eyes."),
                ("A", "Is she tall or short?"),
                ("B", "She is medium height. She is very friendly and cheerful."),
                ("A", "What does she like doing?"),
                ("B", "She loves reading books and playing volleyball."),
            ],
            "task": "Describe your best friend to your partner using at least 5 adjectives."},
        3: {"title": "Asking for Directions", "setting": "On the street",
            "lines": [
                ("A (Tourist)", "Excuse me, how can I get to the post office?"),
                ("B (Local)", "Go straight for two blocks. Then turn left at the traffic lights."),
                ("A", "Is it far from here?"),
                ("B", "No, it's about a five-minute walk. It's next to the bakery."),
                ("A", "Thank you very much!"),
                ("B", "You're welcome. Have a nice day!"),
            ],
            "task": "Role-play giving directions from your school to the nearest park."},
        4: {"title": "Talking About the Weather", "setting": "At home",
            "lines": [
                ("A (Mum)", "What's the weather like today, Kerem?"),
                ("B (Kerem)", "It's cloudy and a bit windy. I think it's going to rain."),
                ("A", "You should take your umbrella then."),
                ("B", "Good idea! What about tomorrow?"),
                ("A", "The weather forecast says it will be sunny and warm."),
                ("B", "Great! We can go to the park after school!"),
            ],
            "task": "Talk about today's weather and your plans for the weekend."},
        5: {"title": "At the Market", "setting": "Greengrocer's shop",
            "lines": [
                ("A (Customer)", "Good morning! Can I have one kilo of tomatoes, please?"),
                ("B (Shopkeeper)", "Of course! Anything else?"),
                ("A", "How much are the oranges?"),
                ("B", "They are eight liras per kilo."),
                ("A", "I'll take two kilos, please. How much is it altogether?"),
                ("B", "That's twenty-two liras in total. Here you go!"),
            ],
            "task": "Create a shopping dialogue. Use 'How much...?' and 'Can I have...?' at least twice."},
        6: {"title": "Free Time Activities", "setting": "After school",
            "lines": [
                ("A", "What do you usually do after school?"),
                ("B", "I usually do my homework first. Then I play video games."),
                ("A", "Do you like sports?"),
                ("B", "Yes, I love playing basketball. I go to practice on Thursdays."),
                ("A", "That sounds fun! I prefer swimming. I go every Saturday."),
                ("B", "Maybe we can try each other's hobbies sometime!"),
            ],
            "task": "Interview three classmates about their free time activities. Report your findings."},
        7: {"title": "Buying a Ticket", "setting": "At the zoo entrance",
            "lines": [
                ("A (Visitor)", "Hello! Two student tickets, please."),
                ("B (Cashier)", "That's fifteen liras each. Thirty liras in total."),
                ("A", "What time does the zoo close?"),
                ("B", "It closes at five o'clock. The feeding show starts at two."),
                ("A", "Where is the elephant enclosure?"),
                ("B", "Go straight and turn right after the cafe. You can't miss it!"),
            ],
            "task": "Create a dialogue at a cinema, museum, or theme park ticket booth."},
        8: {"title": "Making Holiday Plans", "setting": "At the dinner table",
            "lines": [
                ("A (Dad)", "Where are we going to go this summer?"),
                ("B (Child)", "Can we go to Antalya? I want to swim in the sea!"),
                ("A", "That's a great idea. How are we going to get there?"),
                ("B", "Can we drive? I love road trips!"),
                ("A", "OK! We're going to stay for two weeks. Pack your sunscreen!"),
                ("B", "Yay! I'm going to build the biggest sandcastle ever!"),
            ],
            "task": "Plan a holiday with your partner. Decide: Where? How? How long? What activities?"},
        9: {"title": "At the Doctor's", "setting": "Doctor's office",
            "lines": [
                ("A (Doctor)", "Good morning. What's the problem?"),
                ("B (Patient)", "I have a terrible headache and a sore throat."),
                ("A", "How long have you had these symptoms?"),
                ("B", "Since yesterday morning. I also feel very tired."),
                ("A", "You should rest at home and drink plenty of water."),
                ("B", "Thank you, Doctor. Should I take any medicine?"),
            ],
            "task": "Role-play a visit to the doctor. Use 'should' for giving advice."},
        10: {"title": "Talking About the Future", "setting": "In the classroom",
            "lines": [
                ("A", "What do you want to be when you grow up?"),
                ("B", "I want to be a software engineer because I love coding."),
                ("A", "That sounds amazing! You should study maths and English."),
                ("B", "What about you? What's your dream job?"),
                ("A", "I dream of being a vet. I love animals so much!"),
                ("B", "We should both work hard and never give up on our dreams!"),
            ],
            "task": "Interview five classmates about their dream jobs. Create a class survey chart."},
    },
    6: {
        1: {"title": "City vs Country Life", "setting": "In the school canteen",
            "lines": [("A", "I moved here from a village last month."), ("B", "Really? What was it like?"),
                      ("A", "It was quieter and the air was fresher, but there were no cinemas."),
                      ("B", "I've always lived in the city. I think the countryside is boring."),
                      ("A", "Actually, there's a lot to do! I used to go fishing and ride horses."),
                      ("B", "That sounds fun! Maybe I should visit a village sometime.")],
            "task": "Debate with a partner: Is city life better than country life?"},
        2: {"title": "Biography Interview", "setting": "A TV studio",
            "lines": [("A (Host)", "Welcome to our show! Today we have a very special guest."),
                      ("B (Guest)", "Thank you for having me. It's great to be here."),
                      ("A", "Tell us about your childhood. Where were you born?"),
                      ("B", "I was born in a small town near Izmir in 1990."),
                      ("A", "When did you first become interested in science?"),
                      ("B", "When I was ten, my teacher showed us an experiment and I was fascinated.")],
            "task": "Interview a classmate as if they are a famous person. Use Past Simple."},
        3: {"title": "Describing Your Dream Home", "setting": "At a furniture shop",
            "lines": [("A", "I want to buy a new sofa. What do you recommend?"),
                      ("B (Staff)", "How big is your living room? Is there much space?"),
                      ("A", "There are three windows and a large fireplace."),
                      ("B", "Then I'd suggest this L-shaped sofa. It fits perfectly in large rooms."),
                      ("A", "How much is it? I don't have a big budget."),
                      ("B", "It's on sale this week — 30% off!")],
            "task": "Design your dream room and present it to the class."},
        4: {"title": "Talking About First Experiences", "setting": "At a cafe",
            "lines": [("A", "Have you ever been on a plane?"), ("B", "Yes! I flew to London last year. It was my first time."),
                      ("A", "Were you scared?"), ("B", "A little, but the view from the window was incredible!"),
                      ("A", "I've never been on a plane, but I'd love to."),
                      ("B", "You should try it! The first time is always the most exciting.")],
            "task": "Share 3 'first experiences' with a partner using Present Perfect and Past Simple."},
        5: {"title": "Ordering Food at a Restaurant", "setting": "A Turkish restaurant",
            "lines": [("A (Waiter)", "Good evening! Are you ready to order?"), ("B", "Yes, what do you recommend?"),
                      ("A", "Our Iskender kebab is very popular. It's made with tender meat and tomato sauce."),
                      ("B", "That sounds delicious. I'll have that, please. How much is it?"),
                      ("A", "It's 250 lira. Would you like anything to drink?"),
                      ("B", "A glass of ayran, please.")],
            "task": "Role-play ordering a meal. One student is the waiter, the other is the customer."},
        6: {"title": "Planning a Trip", "setting": "At a travel agency",
            "lines": [("A", "We're going to visit Cappadocia next month."), ("B", "How exciting! How long are you going to stay?"),
                      ("A", "We're planning to stay for five days."), ("B", "Are you going to take a balloon ride?"),
                      ("A", "Definitely! And we're going to explore the underground cities."),
                      ("B", "I went there last year. You're going to love it!")],
            "task": "Plan a 3-day trip to a Turkish city with a partner. Use 'going to'."},
        7: {"title": "Talent Show Audition", "setting": "School hall",
            "lines": [("A (Judge)", "Hello! What's your name and what can you do?"), ("B", "I'm Yusuf. I can play the guitar and sing."),
                      ("A", "How long have you been playing?"), ("B", "I've been playing since I was eight."),
                      ("A", "That's impressive! Could you play something for us?"),
                      ("B", "Of course! I'd like to play a traditional Turkish folk song.")],
            "task": "Conduct a talent show audition. Ask about abilities using can/could."},
        8: {"title": "At a Tourist Information Centre", "setting": "Information desk",
            "lines": [("A (Tourist)", "Excuse me, what is the most famous place to visit here?"),
                      ("B (Staff)", "Pamukkale is the most popular. It's the most beautiful natural wonder in the region."),
                      ("A", "Is it farther than Ephesus?"), ("B", "Yes, it's about 2 hours by bus. Ephesus is closer."),
                      ("A", "Which is more interesting?"), ("B", "Both are amazing, but Pamukkale is more unique.")],
            "task": "Create a tourist guide dialogue for your city using comparatives and superlatives."},
        9: {"title": "Resolving a Conflict", "setting": "In the schoolyard",
            "lines": [("A", "Hey, why did you tell everyone my secret?"), ("B", "I'm sorry, I didn't mean to. It just slipped out."),
                      ("A", "That really hurt my feelings. A real friend wouldn't do that."),
                      ("B", "You're right. I should have been more careful. Can you forgive me?"),
                      ("A", "I forgive you, but please don't do it again."), ("B", "I promise. Our friendship is important to me.")],
            "task": "Write and perform a dialogue about solving a problem between friends."},
        10: {"title": "At the Doctor's Office", "setting": "Health clinic",
            "lines": [("A (Doctor)", "What seems to be the problem?"), ("B", "I've had a headache for three days and I feel tired."),
                      ("A", "Do you sleep enough? How many hours a night?"), ("B", "About five or six hours."),
                      ("A", "You should sleep at least eight hours. Also, you must drink more water."),
                      ("B", "Should I take any medicine?")],
            "task": "Role-play a doctor visit. The doctor gives advice using should/must."},
    },
    7: {
        1: {"title": "Getting to Know You", "setting": "First day at a new school",
            "lines": [("A", "Hi, I'm new here. What's this school like?"), ("B", "Welcome! It's great. I've been here since Year 5."),
                      ("A", "What are you interested in?"), ("B", "I'm passionate about robotics and debate. What about you?"),
                      ("A", "I enjoy photography. It helps me express my identity."),
                      ("B", "That's cool! Our school has a photography club. You should join!")],
            "task": "Interview a partner about their identity, interests and values."},
        2: {"title": "Comparing Cultural Traditions", "setting": "International student exchange",
            "lines": [("A", "In my country, we celebrate a harvest festival every autumn."), ("B", "That's interesting! We have something similar in Turkey."),
                      ("A", "Really? What's it called?"), ("B", "We don't have a specific harvest festival, but we celebrate Hidirellez in spring."),
                      ("A", "What do people do during Hidirellez?"), ("B", "People write wishes on paper and tie them to trees.")],
            "task": "Compare a tradition from two different cultures with a partner."},
        3: {"title": "Job Interview Practice", "setting": "An office",
            "lines": [("A (Interviewer)", "Thank you for coming. Why are you interested in this position?"),
                      ("B", "I've always been passionate about technology, and your company is a leader in AI."),
                      ("A", "What are your strongest skills?"), ("B", "I'm good at problem-solving and I work well in teams."),
                      ("A", "Where do you see yourself in five years?"), ("B", "I hope to be leading innovative projects.")],
            "task": "Conduct a mock job interview with a partner. Switch roles."},
        4: {"title": "Discussing a News Article", "setting": "In the school library",
            "lines": [("A", "Did you read that article about fake news?"), ("B", "Yes! It said false stories spread six times faster than true ones."),
                      ("A", "Do you think we should teach media literacy in schools?"), ("B", "Absolutely. We need to learn how to check sources."),
                      ("A", "I agree. I was fooled by a fake story last month."), ("B", "What happened?")],
            "task": "Discuss a news article with a partner. Is it reliable? Why or why not?"},
        5: {"title": "At the School Counsellor", "setting": "Counsellor's office",
            "lines": [("A (Counsellor)", "How are you feeling today?"), ("B", "I've been feeling stressed about exams."),
                      ("A", "That's completely normal. How have you been coping?"), ("B", "I've been staying up late studying, but I can't concentrate."),
                      ("A", "You should try studying in short blocks with breaks."), ("B", "That sounds like good advice. Thank you.")],
            "task": "Role-play a counselling session. One student shares a problem, the other gives advice."},
        6: {"title": "Space Station Communication", "setting": "Mission control",
            "lines": [("A (Astronaut)", "Mission Control, this is ISS. We have completed the experiment."),
                      ("B (Controller)", "Copy that. What were the results?"), ("A", "The plant samples have been growing faster than expected."),
                      ("B", "Excellent! How long have you been monitoring them?"), ("A", "We've been observing them for two weeks."),
                      ("B", "Please send the data. We'll analyse it here on Earth.")],
            "task": "Create a space mission dialogue using Present Perfect and Passive Voice."},
        7: {"title": "Cultural Exchange Discussion", "setting": "Video call between students",
            "lines": [("A", "Hi! I'm calling from Istanbul. Where are you?"), ("B", "I'm in Berlin. My family used to live in Turkey."),
                      ("A", "Really? When did you move?"), ("B", "We moved when I was seven. I still miss Turkish food!"),
                      ("A", "Do you still speak Turkish?"), ("B", "Yes, I speak Turkish at home and German at school.")],
            "task": "Role-play a video call between students from different countries."},
        8: {"title": "Film Review Discussion", "setting": "After leaving a cinema",
            "lines": [("A", "What did you think of the film?"), ("B", "The plot was exciting, but the ending was disappointing."),
                      ("A", "I disagree. I thought the ending was the best part!"), ("B", "The special effects were incredible, though."),
                      ("A", "True. The director has won several awards."), ("B", "Have you seen any of his other films?")],
            "task": "Discuss a film you've seen. Give your opinion with reasons."},
        9: {"title": "Tech Support Call", "setting": "On the phone",
            "lines": [("A (User)", "Hello, I'm having problems with my computer."), ("B (Support)", "What seems to be the issue?"),
                      ("A", "It's been running very slowly since I installed a new programme."), ("B", "Have you tried restarting it?"),
                      ("A", "Yes, but it didn't help. Could it be a virus?"), ("B", "It's possible. I'd recommend running a security scan.")],
            "task": "Create a tech support dialogue for a common problem."},
        10: {"title": "Community Project Planning", "setting": "School meeting room",
            "lines": [("A", "We need to choose our community service project."), ("B", "How about a beach clean-up?"),
                      ("A", "Good idea! If we organise it well, many students will participate."),
                      ("B", "We should also plant trees in the school garden."),
                      ("A", "If we do both, it would make a bigger difference."), ("B", "Let's present our plan to the headteacher.")],
            "task": "Plan a community project with your group. Present it to the class."},
    },
    8: {
        1: {"title": "Self-Reflection Interview", "setting": "School podcast studio",
            "lines": [("A (Host)", "Welcome to our Student Voices podcast. Tell us about yourself."),
                      ("B", "I've been doing a lot of self-reflection recently. I realised I need to manage my time better."),
                      ("A", "What methods do you use?"), ("B", "I started journaling. It helps me process my thoughts."),
                      ("A", "Has it made a difference?"), ("B", "Definitely. I feel more organised and less anxious.")],
            "task": "Record a podcast episode about a personal growth experience."},
        2: {"title": "Language Learning Strategies", "setting": "After English class",
            "lines": [("A", "How many languages can you speak?"), ("B", "Three — Turkish, English and some German."),
                      ("A", "Wow! How did you learn them?"), ("B", "Turkish is my mother tongue. I've been learning English since primary school."),
                      ("A", "What's the best way to learn a language?"), ("B", "Immersion. I watch films in English and read books.")],
            "task": "Share language learning tips. Create a 'Top 5 Tips' poster."},
        3: {"title": "Ethics Debate", "setting": "Debate club",
            "lines": [("A", "Today's topic: Should scientists clone animals?"), ("B", "I believe they should, for conservation purposes."),
                      ("A", "But what about the ethical implications?"), ("B", "If it saves endangered species, the benefits outweigh the risks."),
                      ("A", "However, cloning could lead to unintended consequences."), ("B", "That's why we need strict ethical guidelines.")],
            "task": "Choose a scientific ethics topic and hold a class debate."},
        4: {"title": "Creating a Digital Story", "setting": "Computer lab",
            "lines": [("A", "I'm making a digital story for our project. Have you started yours?"),
                      ("B", "Yes, I've been working on a video essay about climate change."),
                      ("A", "What software are you using?"), ("B", "I'm using free video editing software. It's quite easy to learn."),
                      ("A", "Could you show me how to add subtitles?"), ("B", "Sure! It's done automatically using AI now.")],
            "task": "Plan a digital story with a partner. Choose format, topic and audience."},
        5: {"title": "Geography Quiz Show", "setting": "TV studio",
            "lines": [("A (Host)", "Welcome to Geography Challenge! First question: What's the longest river in Turkey?"),
                      ("B", "Is it the Kizilirmak? It's 1,355 kilometres long."), ("A", "Correct! For 100 points."),
                      ("B", "I'd like to try the bonus question."), ("A", "What is the deepest lake in Turkey?"),
                      ("B", "I think it's Lake Van... no, wait. It must be Lake Tortum or Nemrut crater lake.")],
            "task": "Create a geography quiz with 10 questions about Turkey."},
        6: {"title": "Social Media Discussion", "setting": "Youth forum",
            "lines": [("A", "How much time do you spend on social media daily?"), ("B", "Probably about three hours. I know it's too much."),
                      ("A", "Research says 30 minutes is the healthy limit."), ("B", "Really? That's much less than I expected."),
                      ("A", "I've been trying to reduce my screen time. It's not easy."), ("B", "Maybe we should support each other.")],
            "task": "Survey your class about social media habits. Present the results."},
        7: {"title": "History Presentation", "setting": "History classroom",
            "lines": [("A", "Today I'm presenting about Ataturk's reforms."), ("B (Teacher)", "Excellent topic. What will you focus on?"),
                      ("A", "I'll talk about the alphabet reform, women's rights and secular education."),
                      ("B", "Those are fundamental changes. What sources have you used?"),
                      ("A", "I've read three books and two academic articles."), ("B", "Very thorough. Please begin when you're ready.")],
            "task": "Prepare and deliver a 3-minute presentation about a historical figure."},
        8: {"title": "Book Club Discussion", "setting": "School library",
            "lines": [("A", "Has everyone finished the book?"), ("B", "Yes. I think the protagonist was very brave."),
                      ("A", "I disagree. I think she was reckless, not brave."), ("C", "That's an interesting point. Can you give an example?"),
                      ("A", "In chapter 5, she went into the forest alone at night without telling anyone."),
                      ("B", "True, but she did it to save her brother. That's courageous.")],
            "task": "Hold a book club discussion about a story you've read. Use opinion phrases."},
        9: {"title": "Model UN Simulation", "setting": "Conference hall",
            "lines": [("A (Chair)", "The delegate from Turkey has the floor."), ("B (Turkey)", "Thank you, Chair. Climate change affects all nations equally."),
                      ("A", "Does the delegate from Brazil wish to respond?"), ("C (Brazil)", "Yes. Developing countries are affected more severely."),
                      ("B", "We agree. Therefore, wealthier nations should provide more funding."), ("C", "We support this proposal.")],
            "task": "Simulate a UN debate on a global issue. Each student represents a country."},
        10: {"title": "Critical Analysis Discussion", "setting": "Philosophy club",
            "lines": [("A", "Today's question: Can artificial intelligence be truly creative?"), ("B", "AI can produce art, but is it really creativity?"),
                      ("A", "It depends on how you define creativity."), ("B", "If creativity requires consciousness, then no."),
                      ("A", "But what if creativity is just novel combinations of existing ideas?"), ("B", "In that case, AI might already be creative.")],
            "task": "Discuss a philosophical question with evidence and reasoning."},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# CULTURE CORNER BANK — Grade 5
# ══════════════════════════════════════════════════════════════════════════════

_CULTURE_CORNER_BANK = {
    5: {
        1: {"title": "Schools Around the World",
            "text": ("Did you know that in Japan, students clean their own classrooms? "
                     "There are no janitors in most Japanese schools. In Finland, children don't start school "
                     "until they are seven years old, and they have very little homework. In Brazil, some "
                     "students go to school in the morning and others go in the afternoon because there aren't "
                     "enough classrooms. In Kenya, some children walk more than 10 kilometres to get to school "
                     "every day. Despite these differences, children everywhere share the same love of learning!"),
            "question": "How is your school different from schools in Japan, Finland, or Kenya?",
            "country_flag": "JP, FI, BR, KE"},
        2: {"title": "Family Traditions",
            "text": ("Families around the world have different traditions. In Italy, Sunday lunch is sacred "
                     "-- the whole extended family gathers for a big pasta meal that can last for hours. "
                     "In South Korea, family members bow to their elders as a sign of respect, especially "
                     "during Chuseok (Korean Thanksgiving). In Mexico, 'La Quincea\u00f1era' celebrates a girl's "
                     "15th birthday with a huge party. In Turkey, families often drink tea together after "
                     "dinner and share stories. These traditions keep families close and connected."),
            "question": "What special traditions does your family have? Write about one.",
            "country_flag": "IT, KR, MX, TR"},
        3: {"title": "Famous Landmarks",
            "text": ("Every country has landmarks that make it special. The Eiffel Tower in Paris, France, "
                     "was built in 1889 and is 330 metres tall. The Great Wall of China stretches over 21,000 "
                     "kilometres -- you can even see parts of it from space! In Turkey, Hagia Sophia in "
                     "Istanbul is nearly 1,500 years old and has been both a church and a mosque. The Statue "
                     "of Liberty in New York was a gift from France to the USA in 1886. These landmarks "
                     "tell us stories about history, culture, and human achievement."),
            "question": "Which landmark would you most like to visit? Why?",
            "country_flag": "FR, CN, TR, US"},
        4: {"title": "Weather and Festivals",
            "text": ("People around the world celebrate the seasons in unique ways. In India, Holi (the "
                     "Festival of Colours) marks the arrival of spring -- people throw coloured powder at "
                     "each other! In Sweden, Midsommar celebrates the longest day of the year with dancing "
                     "around a maypole. In China, the Mid-Autumn Festival celebrates the harvest moon with "
                     "mooncakes and lanterns. In Turkey, Nevruz (21 March) celebrates the beginning of spring "
                     "with bonfires and traditional foods. Nature inspires celebration everywhere!"),
            "question": "Describe a festival or celebration connected to a season in your culture.",
            "country_flag": "IN, SE, CN, TR"},
        5: {"title": "Money Around the World",
            "text": ("Different countries use different currencies. The UK uses the pound sterling, the USA "
                     "uses the dollar, Japan uses the yen, and Turkey uses the Turkish lira. In the European "
                     "Union, 20 countries share the same currency: the euro. Did you know that Sweden is almost "
                     "cashless? Most people there pay with cards or phones. In some rural areas of Africa, "
                     "people still use mobile phone credit as a form of currency. Money has come a long way "
                     "from shells and gold coins to digital payments!"),
            "question": "Design your own banknote! What picture would you put on it and why?",
            "country_flag": "GB, US, JP, SE"},
        6: {"title": "Sports Around the World",
            "text": ("Football is the world's most popular sport, played in almost every country. But did "
                     "you know that cricket is the second most popular sport, with 2.5 billion fans, mostly "
                     "in India, Pakistan, and Australia? In Canada, ice hockey is the national sport. In "
                     "Japan, sumo wrestling has a history of over 1,500 years. Turkey's national sport is "
                     "oil wrestling ('yagli gures'), where wrestlers cover themselves in olive oil! In New "
                     "Zealand, the rugby team performs the 'haka,' a traditional Maori war dance, before "
                     "every match. Sports bring people together across cultures."),
            "question": "What is the most popular sport in your area? Why do you think people love it?",
            "country_flag": "IN, CA, JP, NZ"},
        7: {"title": "Animals and Their Habitats",
            "text": ("Every continent has unique animals. Australia has kangaroos and koalas that live "
                     "nowhere else on Earth. The Amazon Rainforest in South America is home to pink river "
                     "dolphins and poison dart frogs. In Africa, the 'Big Five' (lion, elephant, buffalo, "
                     "leopard, rhino) attract millions of tourists. Turkey is home to the Anatolian leopard "
                     "and the loggerhead sea turtle, which nests on Mediterranean beaches. Sadly, many animals "
                     "are endangered because of habitat loss. We must protect biodiversity for future generations."),
            "question": "Choose an endangered animal. Write 5 facts about it and explain why we should protect it.",
            "country_flag": "AU, BR, ZA, TR"},
        8: {"title": "Traditional Foods",
            "text": ("Food is a window into culture. In Japan, people eat sushi and ramen with chopsticks. "
                     "In India, many dishes use colourful spices like turmeric and cumin, and people often "
                     "eat with their right hand. In Italy, pasta and pizza are everyday foods, but each "
                     "region has its own special recipe. Turkey is famous for kebabs, baklava, and the "
                     "world's best breakfast spread. In Peru, ceviche (raw fish in lime juice) has been "
                     "eaten for over 2,000 years! Trying new foods is one of the best ways to learn about "
                     "other cultures."),
            "question": "Write a recipe for your favourite dish in English. Include ingredients and steps.",
            "country_flag": "JP, IN, IT, PE"},
        9: {"title": "Young Inventors",
            "text": ("You don't have to be an adult to change the world! Gitanjali Rao from the USA invented "
                     "a device to detect lead in drinking water when she was just 11 years old. In South Africa, "
                     "Kiara Nirghin (16) created a super-absorbent material to help fight droughts. In Turkey, "
                     "a group of students from Bursa designed a smart recycling bin that sorts waste automatically. "
                     "Louis Braille invented the Braille reading system for blind people when he was only 15! "
                     "These young innovators prove that age is just a number when it comes to making a difference."),
            "question": "If you could invent something, what would it be? Draw it and explain how it works.",
            "country_flag": "US, ZA, TR, FR"},
        10: {"title": "Digital Citizenship",
            "text": ("The internet connects over 5 billion people worldwide. In South Korea, 97% of the "
                     "population uses the internet -- it has the fastest internet speeds in the world. "
                     "In Estonia, students learn coding from the age of 7, and citizens can vote online. "
                     "However, being online comes with responsibilities. Cyberbullying, fake news, and "
                     "privacy concerns affect people everywhere. Turkey has been working on digital literacy "
                     "programmes for students. Remember: think before you post, be kind online, protect your "
                     "personal information, and always verify information before sharing it."),
            "question": "Write 5 rules for being a good digital citizen. Share them with your class.",
            "country_flag": "KR, EE, TR"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# FUN FACTS BANK — Grade 5 (Did You Know? boxes)
# ══════════════════════════════════════════════════════════════════════════════

_FUN_FACTS_BANK = {
    5: {
        1: [
            "The word 'school' comes from the ancient Greek word 'schole,' which actually meant 'leisure time'!",
            "An octopus has three hearts and blue blood.",
            "You blink about 15-20 times per minute -- that's up to 28,800 times a day!",
        ],
        2: [
            "Identical twins have different fingerprints, even though they share the same DNA.",
            "The longest word in English is 'pneumonoultramicroscopicsilicovolcanoconiosis' (45 letters).",
            "A group of flamingos is called a 'flamboyance.'",
        ],
        3: [
            "The shortest street in the world is Ebenezer Place in Scotland -- it is only 2.06 metres long!",
            "Istanbul is the only city in the world that sits on two continents: Europe and Asia.",
            "There are more than 200 languages spoken in London.",
        ],
        4: [
            "A bolt of lightning is five times hotter than the surface of the Sun!",
            "It can rain diamonds on Jupiter and Saturn.",
            "Snow appears white, but each snowflake is actually transparent.",
        ],
        5: [
            "The first vending machine was invented in ancient Egypt to dispense holy water!",
            "Honey never goes bad. Archaeologists found 3,000-year-old honey in Egyptian tombs -- and it was still edible!",
            "Apples float in water because they are 25% air.",
        ],
        6: [
            "Playing video games can improve your eyesight, reaction time, and problem-solving skills.",
            "The guitar is the most popular instrument in the world, with over 50 million players.",
            "Listening to music can help you study better by reducing stress.",
        ],
        7: [
            "An elephant's brain weighs about 5 kilograms -- the largest brain of any land animal.",
            "Penguins propose to their partners by giving them a pebble.",
            "A cat has 32 muscles in each ear!",
        ],
        8: [
            "The Mediterranean Sea is named after a Latin word meaning 'middle of the Earth.'",
            "Turkey has more than 80,000 mosques -- more than any other country in the world.",
            "The world's oldest known recipe is for beer, from ancient Sumeria (about 4,000 years old).",
        ],
        9: [
            "The human brain can store approximately 2.5 petabytes of information -- that's 3 million hours of TV!",
            "By 2030, there will be about 800 million jobs done by robots.",
            "The first computer programmer was a woman: Ada Lovelace, in the 1840s.",
        ],
        10: [
            "Turkish coffee was added to UNESCO's Intangible Cultural Heritage list in 2013.",
            "The tulip flower was first cultivated in Turkey, not the Netherlands.",
            "The world's oldest known map was found in Turkey -- the Catalhoyuk map is about 8,000 years old.",
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PROJECT WORK BANK — Grade 5 (end-of-unit creative projects)
# ══════════════════════════════════════════════════════════════════════════════

_PROJECT_BANK = {
    5: {
        1: {"title": "My Class Profile Poster",
            "desc": "Create a colourful poster about your class.",
            "steps": ["Interview 5 classmates (name, age, favourite subject, hobby).",
                      "Draw or print a picture of your classroom.",
                      "Write a short paragraph about your class using Present Simple.",
                      "Add a bar chart showing favourite subjects.",
                      "Present your poster to the class in English."],
            "materials": "A3 paper, coloured pencils, stickers, photos"},
        2: {"title": "Family Tree Project",
            "desc": "Design a creative family tree with descriptions.",
            "steps": ["Draw a family tree with at least 8 family members.",
                      "Write 2-3 sentences describing each person (appearance + personality).",
                      "Use 'have/has' and possessive adjectives correctly.",
                      "Add photos or drawings of each family member.",
                      "Present your family tree to a partner."],
            "materials": "Poster board, family photos, markers"},
        3: {"title": "My Neighbourhood Map",
            "desc": "Draw a detailed map of your neighbourhood.",
            "steps": ["Walk around your neighbourhood and note important places.",
                      "Draw a map with at least 10 locations labelled in English.",
                      "Write directions from your home to three different places.",
                      "Use prepositions: next to, opposite, between, near, across from.",
                      "Give a 'guided tour' presentation to your class."],
            "materials": "Large paper, rulers, coloured pens, compass"},
        4: {"title": "Season Brochure",
            "desc": "Create a travel brochure for your favourite season in Turkey.",
            "steps": ["Choose a season and a region of Turkey.",
                      "Write about the weather, activities, and clothing for that season.",
                      "Include at least 5 adjectives and 3 'can' sentences.",
                      "Design the brochure with pictures and a catchy title.",
                      "Try to 'sell' the season to your classmates!"],
            "materials": "A4 paper (folded), magazines for cutting, glue"},
        5: {"title": "My Mini Shop",
            "desc": "Set up a role-play shop in the classroom.",
            "steps": ["Choose a type of shop (bakery, greengrocer, bookshop, etc.).",
                      "Create price labels for at least 10 items in English.",
                      "Write a shopping dialogue script with a partner.",
                      "Practise using 'How much...?', 'Can I have...?', numbers.",
                      "Role-play the shopping scene for the class."],
            "materials": "Cardboard, play money, product pictures, price tags"},
        6: {"title": "Hobby Magazine",
            "desc": "Create a one-page magazine about your hobbies.",
            "steps": ["Write an article about your top 3 hobbies (50+ words each).",
                      "Include a 'Top 5 Hobbies in Our Class' survey result.",
                      "Add a 'Hobby of the Month' recommendation box.",
                      "Design the layout like a real magazine page.",
                      "Share and compare magazines with classmates."],
            "materials": "A3 paper, photos, scissors, glue, markers"},
        7: {"title": "Animal Fact File",
            "desc": "Research and present an endangered animal.",
            "steps": ["Choose an endangered animal and research 10 facts.",
                      "Write about: habitat, diet, size, lifespan, why it's endangered.",
                      "Use comparative adjectives (bigger than, faster than...).",
                      "Create an 'animal ID card' with a drawing.",
                      "Present your animal to the class using Simple Past for history."],
            "materials": "Card stock, encyclopaedia/internet access, art supplies"},
        8: {"title": "Holiday Planner",
            "desc": "Plan a dream holiday and present it to the class.",
            "steps": ["Choose a destination and research it.",
                      "Plan a 7-day itinerary using 'going to' for each day.",
                      "Calculate a budget (transport, hotel, food, activities).",
                      "Create a mini travel guide with useful phrases.",
                      "Present your plan to the class. Vote for the best trip!"],
            "materials": "Notebook, internet access, printed maps, calculator"},
        9: {"title": "Career Day Presentation",
            "desc": "Research your dream job and give a mini presentation.",
            "steps": ["Choose a career you're interested in.",
                      "Interview someone who does this job (or research online).",
                      "Write about: what they do, skills needed, why you chose it.",
                      "Use 'should', 'must', and 'have to' in your presentation.",
                      "Create a 'Job Advertisement' poster for this career."],
            "materials": "Poster paper, photos, interview notes, markers"},
        10: {"title": "Digital Story: Our Heritage",
            "desc": "Create a digital or hand-drawn storybook about Turkish culture.",
            "steps": ["Choose a topic: traditional story, food, festival, or landmark.",
                      "Write a 10-sentence story using sequencing words.",
                      "Create illustrations for each page (min 6 pages).",
                      "Include a 'Did You Know?' fact box on each page.",
                      "Read your storybook to younger students."],
            "materials": "A4 paper stapled as book, art supplies, or a computer"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# SONG & RHYME BANK — Grade 5
# ══════════════════════════════════════════════════════════════════════════════

_SONG_BANK = {
    5: {
        1: {"title": "The School Day Song", "type": "Song",
            "lyrics": (
                "Wake up, wake up, it's time for school,\n"
                "Brush your teeth, that's the rule.\n"
                "Pack your bag, tie your shoe,\n"
                "Seven thirty, time to go -- woo-hoo!\n\n"
                "Maths and English, Science too,\n"
                "So many things to learn and do.\n"
                "Read and write, count and play,\n"
                "I love every single day!\n"
            ),
            "activity": "Clap the rhythm and sing along. Then change the subjects to your own timetable."},
        2: {"title": "My Family Rap", "type": "Rap",
            "lyrics": (
                "My dad is tall, my mum is kind,\n"
                "The best family you could ever find.\n"
                "My brother's funny, my sister's smart,\n"
                "They all have a special place in my heart.\n\n"
                "Grandma's cookies, grandpa's tales,\n"
                "Family love never fails.\n"
                "Big or small, short or tall,\n"
                "I love my family -- one and all!\n"
            ),
            "activity": "Write a new verse about YOUR family. Perform it as a rap!"},
        3: {"title": "The Direction Chant", "type": "Chant",
            "lyrics": (
                "Go straight, go straight, don't turn around,\n"
                "Turn left, turn right, look what I found!\n"
                "Next to the park, across the street,\n"
                "The library is where readers meet.\n\n"
                "Between the bank and the old cafe,\n"
                "That's the bookshop -- hip hooray!\n"
                "Opposite the school, behind the mall,\n"
                "I know directions -- I know them all!\n"
            ),
            "activity": "March around the classroom and chant the directions. Add actions!"},
        4: {"title": "Weather Song", "type": "Song",
            "lyrics": (
                "What's the weather, what's the weather,\n"
                "Look outside today!\n"
                "Is it sunny, is it rainy,\n"
                "Can we go out and play?\n\n"
                "Spring is warm, summer's hot,\n"
                "Autumn's cool -- like it or not.\n"
                "Winter's cold with snow and ice,\n"
                "Every season's rather nice!\n"
            ),
            "activity": "Sing the song with weather actions. Draw weather symbols for each verse."},
        5: {"title": "Shopping Rhyme", "type": "Rhyme",
            "lyrics": (
                "One potato, two potatoes, in my shopping bag,\n"
                "Three tomatoes, four tomatoes, on the price tag.\n"
                "How much is it? How much is that?\n"
                "Can I have some cheese and a chocolate bar -- just like that!\n\n"
                "Five bananas, six oranges, fresh from the farm,\n"
                "Seven apples, eight peaches, carried on my arm.\n"
                "Thank you, goodbye, see you next week,\n"
                "Shopping in English -- isn't that unique!\n"
            ),
            "activity": "Add up the items in the rhyme. How much would they cost at your local shop?"},
        6: {"title": "Hobby Rock", "type": "Song",
            "lyrics": (
                "I like swimming, I like reading,\n"
                "I like games that keep me dreaming.\n"
                "Playing guitar, riding my bike,\n"
                "Tell me, tell me, what do you like?\n\n"
                "Do you like dancing? Do you like art?\n"
                "Hobbies are good for your mind and heart.\n"
                "Try something new, don't be shy,\n"
                "Give it a go, give it a try!\n"
            ),
            "activity": "Replace the hobbies with your own and perform the song for a partner."},
        7: {"title": "Animal Chant", "type": "Chant",
            "lyrics": (
                "The elephant is bigger than the cat,\n"
                "The monkey is funnier -- imagine that!\n"
                "The snake is longer than a rope,\n"
                "The parrot is more colourful -- I hope!\n\n"
                "What's the fastest? What's the tallest?\n"
                "What's the biggest? What's the smallest?\n"
                "Animals are amazing, that is true,\n"
                "Let's protect them -- me and you!\n"
            ),
            "activity": "Add four more animal comparisons to the chant using -er/more + adjective."},
        8: {"title": "Holiday Dreams", "type": "Song",
            "lyrics": (
                "I'm going to swim in the deep blue sea,\n"
                "I'm going to climb a coconut tree.\n"
                "I'm going to build a castle in the sand,\n"
                "Holiday time is going to be grand!\n\n"
                "We're going to travel near and far,\n"
                "We're going to drive in daddy's car.\n"
                "Pack your bags and pack your dreams,\n"
                "Summer holiday is what it seems!\n"
            ),
            "activity": "Change the activities to YOUR holiday plans. Use 'going to' in every line."},
        9: {"title": "Dream Job Rap", "type": "Rap",
            "lyrics": (
                "Doctor, lawyer, engineer,\n"
                "What do you want to be next year?\n"
                "Pilot, teacher, scientist too,\n"
                "The future's waiting just for you!\n\n"
                "You should study, you should read,\n"
                "Hard work is all you really need.\n"
                "Believe in yourself, follow your dream,\n"
                "You're part of an amazing team!\n"
            ),
            "activity": "Add your dream job to the rap. Perform it with confidence!"},
        10: {"title": "Heritage Rhyme", "type": "Rhyme",
            "lyrics": (
                "From east to west, our land is great,\n"
                "Stories and legends that fascinate.\n"
                "Hodja's wisdom, tulips in spring,\n"
                "Turkish coffee -- let the cups ring!\n\n"
                "Share your culture, share your pride,\n"
                "With the whole world, side by side.\n"
                "Digital citizens, kind and true,\n"
                "The future starts with me and you!\n"
            ),
            "activity": "Write a verse about your own cultural heritage. Share it with the class."},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# IRREGULAR VERBS TABLE — Grade 5 level
# ══════════════════════════════════════════════════════════════════════════════

_IRREGULAR_VERBS_G5 = [
    ("be", "was/were", "been"), ("become", "became", "become"), ("begin", "began", "begun"),
    ("break", "broke", "broken"), ("bring", "brought", "brought"), ("build", "built", "built"),
    ("buy", "bought", "bought"), ("can", "could", "--"), ("catch", "caught", "caught"),
    ("choose", "chose", "chosen"), ("come", "came", "come"), ("cut", "cut", "cut"),
    ("do", "did", "done"), ("draw", "drew", "drawn"), ("drink", "drank", "drunk"),
    ("drive", "drove", "driven"), ("eat", "ate", "eaten"), ("fall", "fell", "fallen"),
    ("feel", "felt", "felt"), ("find", "found", "found"), ("fly", "flew", "flown"),
    ("forget", "forgot", "forgotten"), ("get", "got", "got"), ("give", "gave", "given"),
    ("go", "went", "gone"), ("grow", "grew", "grown"), ("have", "had", "had"),
    ("hear", "heard", "heard"), ("hit", "hit", "hit"), ("hold", "held", "held"),
    ("keep", "kept", "kept"), ("know", "knew", "known"), ("learn", "learnt", "learnt"),
    ("leave", "left", "left"), ("let", "let", "let"), ("lose", "lost", "lost"),
    ("make", "made", "made"), ("mean", "meant", "meant"), ("meet", "met", "met"),
    ("pay", "paid", "paid"), ("put", "put", "put"), ("read", "read", "read"),
    ("ride", "rode", "ridden"), ("run", "ran", "run"), ("say", "said", "said"),
    ("see", "saw", "seen"), ("sell", "sold", "sold"), ("send", "sent", "sent"),
    ("show", "showed", "shown"), ("sing", "sang", "sung"), ("sit", "sat", "sat"),
    ("sleep", "slept", "slept"), ("speak", "spoke", "spoken"), ("spend", "spent", "spent"),
    ("stand", "stood", "stood"), ("swim", "swam", "swum"), ("take", "took", "taken"),
    ("teach", "taught", "taught"), ("tell", "told", "told"), ("think", "thought", "thought"),
    ("understand", "understood", "understood"), ("wake", "woke", "woken"),
    ("wear", "wore", "worn"), ("win", "won", "won"), ("write", "wrote", "written"),
]

# ══════════════════════════════════════════════════════════════════════════════
# PHONETIC SYMBOLS TABLE
# ══════════════════════════════════════════════════════════════════════════════

_PHONETIC_CHART = [
    ("Vowels", [
        ("/i:/", "see, tree, key"), ("/I/", "sit, fish, bit"), ("/e/", "bed, red, ten"),
        ("/ae/", "cat, hat, map"), ("/a:/", "car, far, heart"), ("/o/", "hot, dog, lot"),
        ("/o:/", "door, four, more"), ("/u/", "put, book, look"), ("/u:/", "too, blue, shoe"),
        ("/^/", "cup, bus, sun"), ("/3:/", "bird, turn, learn"), ("/@/", "about, banana, sofa"),
    ]),
    ("Diphthongs", [
        ("/eI/", "day, play, rain"), ("/aI/", "my, time, fly"), ("/oI/", "boy, coin, toy"),
        ("/aU/", "how, now, house"), ("/@U/", "go, know, show"), ("/I@/", "here, near, dear"),
        ("/e@/", "there, hair, care"), ("/U@/", "tour, pure, sure"),
    ]),
    ("Consonants", [
        ("/p/", "pen, cup"), ("/b/", "book, baby"), ("/t/", "ten, hat"), ("/d/", "day, red"),
        ("/k/", "cat, key"), ("/g/", "go, big"), ("/f/", "fish, off"), ("/v/", "very, live"),
        ("/s/", "sun, miss"), ("/z/", "zoo, is"), ("/h/", "hat, he"), ("/m/", "man, swim"),
        ("/n/", "no, ten"), ("/l/", "leg, all"), ("/r/", "red, run"), ("/w/", "we, win"),
        ("/j/", "yes, you"), ("/tS/", "church, watch"), ("/dZ/", "jam, bridge"),
        ("/T/", "think, bath"), ("/D/", "this, mother"), ("/S/", "she, fish"),
        ("/Z/", "television, measure"), ("/N/", "sing, ring"),
    ]),
]

# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS CHECK QUESTIONS — Grade 5 (every 3 units)
# ══════════════════════════════════════════════════════════════════════════════

_PROGRESS_CHECK_BANK = {
    5: {
        1: {  # Unit 1 — School Year / Daily Routines
            "title": "Progress Check — Unit 1",
            "vocab": [
                ("1. I go to _____ every morning.", "school"),
                ("2. My favourite _____ is English.", "subject"),
                ("3. I _____ my teeth after breakfast.", "brush"),
                ("4. School starts at half past _____.", "eight"),
                ("5. I wear a _____ to school.", "uniform"),
            ],
            "grammar": [
                ("1. She _____ (get) up at seven o'clock.", "gets"),
                ("2. I _____ (have) breakfast every day.", "have"),
                ("3. _____ he like Science? (question)", "Does"),
                ("4. We _____ (not/watch) TV in the morning.", "don't watch"),
                ("5. Elif always _____ (go) to bed at ten.", "goes"),
            ],
            "reading_text": (
                "Ali is in the 5th grade. He wakes up at seven o'clock every morning. "
                "He has breakfast with his family. His favourite subject is Maths. "
                "After school, he plays football with his friends in the park."
            ),
            "reading_qs": [
                ("1. What time does Ali wake up?", "Seven o'clock"),
                ("2. What is his favourite subject?", "Maths"),
                ("3. What does he do after school?", "Plays football with his friends"),
            ],
        },
        2: {  # Unit 2 — Family / Appearance
            "title": "Progress Check — Unit 2",
            "vocab": [
                ("1. My mother's sister is my _____.", "aunt"),
                ("2. She has long _____ hair.", "brown"),
                ("3. My _____ is very tall.", "father"),
                ("4. He wears _____.", "glasses"),
                ("5. My baby brother is very _____.", "cute"),
            ],
            "grammar": [
                ("1. My sister _____ (have) blue eyes.", "has"),
                ("2. _____ is your brother? He is tall.", "What ... like"),
                ("3. I have got a _____ (young) sister.", "younger"),
                ("4. She _____ (not/have) curly hair.", "doesn't have"),
                ("5. My parents _____ (be) very kind.", "are"),
            ],
            "reading_text": (
                "Zeynep has a big family. She has two brothers and one sister. Her mother "
                "has brown eyes and long hair. Her father is tall and wears glasses. "
                "They live in a flat in Ankara. Zeynep loves spending time with her family."
            ),
            "reading_qs": [
                ("1. How many brothers does Zeynep have?", "Two"),
                ("2. What does her father look like?", "He is tall and wears glasses"),
                ("3. Where do they live?", "In a flat in Ankara"),
            ],
        },
        3: {  # After Unit 3
            "title": "Progress Check 1 (Units 1-3)",
            "vocab": [
                ("1. The place where we learn is called _____.", "school"),
                ("2. My father's mother is my _____.", "grandmother"),
                ("3. The building where you can borrow books is a _____.", "library"),
                ("4. The opposite of 'tall' is _____.", "short"),
                ("5. We buy bread at the _____.", "bakery"),
            ],
            "grammar": [
                ("1. She _____ (go) to school every day.", "goes"),
                ("2. There _____ two parks in my neighbourhood.", "are"),
                ("3. My sister _____ (have) curly hair.", "has"),
                ("4. _____ you like Maths? (question)", "Do"),
                ("5. The bank is _____ the hospital and the school.", "between"),
            ],
            "reading_text": (
                "Tom is from London. He is twelve years old. He has short brown hair and blue eyes. "
                "He lives in a flat near the city centre. There is a park opposite his building. "
                "His school is next to the library. He walks to school every morning."
            ),
            "reading_qs": [
                ("1. Where is Tom from?", "London"),
                ("2. Where does he live?", "In a flat near the city centre"),
                ("3. What is opposite his building?", "A park"),
            ],
        },
        4: {  # Unit 4 — Seasons & Weather
            "title": "Progress Check — Unit 4",
            "vocab": [
                ("1. In _____, the leaves turn orange and fall.", "autumn"),
                ("2. It is very _____ in January.", "cold"),
                ("3. Take your _____ — it might rain.", "umbrella"),
                ("4. The _____ is shining brightly today.", "sun"),
                ("5. We build a _____ when it snows.", "snowman"),
            ],
            "grammar": [
                ("1. Look! It _____ (snow) outside.", "is snowing"),
                ("2. In summer, we usually _____ (go) to the beach.", "go"),
                ("3. She _____ (wear) a coat in winter.", "wears"),
                ("4. _____ it cold today? (question)", "Is"),
                ("5. We _____ (not/like) rainy days.", "don't like"),
            ],
            "reading_text": (
                "Turkey has four seasons. Spring is warm and flowers bloom everywhere. "
                "Summer is hot and families go to the beach. In autumn, leaves change colour "
                "and fall from the trees. Winter is cold and sometimes it snows in Ankara."
            ),
            "reading_qs": [
                ("1. How many seasons does Turkey have?", "Four"),
                ("2. What happens in spring?", "It is warm and flowers bloom"),
                ("3. Where does it sometimes snow?", "In Ankara"),
            ],
        },
        5: {  # Unit 5 — Market / Shopping
            "title": "Progress Check — Unit 5",
            "vocab": [
                ("1. We buy fruit and vegetables at the _____.", "market"),
                ("2. How _____ is this shirt?", "much"),
                ("3. I need a _____ of milk.", "bottle"),
                ("4. She paid with a fifty-lira _____.", "note"),
                ("5. The apples are two lira per _____.", "kilo"),
            ],
            "grammar": [
                ("1. How _____ oranges do you want?", "many"),
                ("2. There is _____ bread on the table.", "some"),
                ("3. We _____ (not/have) any eggs.", "don't have"),
                ("4. I would like _____ water, please.", "some"),
                ("5. _____ there any cheese? (question)", "Is"),
            ],
            "reading_text": (
                "Every Saturday, Ayse goes to the market with her mother. They buy fresh fruit "
                "and vegetables. Ayse likes choosing the tomatoes and cucumbers. Her mother "
                "always buys olives, cheese and bread. They also get some flowers for the house."
            ),
            "reading_qs": [
                ("1. When does Ayse go to the market?", "Every Saturday"),
                ("2. What does Ayse like choosing?", "Tomatoes and cucumbers"),
                ("3. What else does her mother buy?", "Olives, cheese and bread"),
            ],
        },
        6: {  # After Unit 6
            "title": "Progress Check 2 (Units 4-6)",
            "vocab": [
                ("1. The season after summer is _____.", "autumn"),
                ("2. You pay for things with _____.", "money"),
                ("3. Playing guitar is my favourite _____.", "hobby"),
                ("4. It is very hot in _____.", "summer"),
                ("5. We use an _____ when it rains.", "umbrella"),
            ],
            "grammar": [
                ("1. I _____ swim very well. (ability)", "can"),
                ("2. How _____ apples do you want?", "many"),
                ("3. She enjoys _____ (read) books.", "reading"),
                ("4. Look! It _____ (rain) now.", "is raining"),
                ("5. There is _____ milk in the fridge.", "some"),
            ],
            "reading_text": (
                "Selin loves weekends. On Saturdays, she plays tennis with her friend. "
                "After that, she usually watches a film. On Sundays, she helps her mother "
                "cook lunch. She can make very good pasta. In the afternoon, she reads comics."
            ),
            "reading_qs": [
                ("1. What sport does Selin play?", "Tennis"),
                ("2. What can she cook?", "Pasta"),
                ("3. What does she do on Sunday afternoons?", "Reads comics"),
            ],
        },
        7: {  # Unit 7 — Zoo / Animals
            "title": "Progress Check — Unit 7",
            "vocab": [
                ("1. The biggest land animal is the _____.", "elephant"),
                ("2. Lions live in the _____ in Africa.", "wild"),
                ("3. A _____ has black and white stripes.", "zebra"),
                ("4. Penguins live in very _____ places.", "cold"),
                ("5. We saw many animals at the _____.", "zoo"),
            ],
            "grammar": [
                ("1. I _____ (see) a giraffe at the zoo yesterday.", "saw"),
                ("2. The monkey _____ (climb) the tree right now.", "is climbing"),
                ("3. Elephants _____ (be) the largest land animals.", "are"),
                ("4. _____ you ever _____ (visit) a zoo?", "Have ... visited"),
                ("5. The flamingos _____ (stand) on one leg.", "were standing"),
            ],
            "reading_text": (
                "The zoo is a wonderful place. You can see animals from all around the world. "
                "Lions are strong and brave. Monkeys are funny — they jump and play all day. "
                "Penguins waddle and swim very fast. Every animal is special and we must protect them."
            ),
            "reading_qs": [
                ("1. What are lions like?", "Strong and brave"),
                ("2. What do monkeys do?", "They jump and play all day"),
                ("3. Why must we protect animals?", "Because every animal is special"),
            ],
        },
        8: {  # Unit 8 — Summer Holiday Plans
            "title": "Progress Check — Unit 8",
            "vocab": [
                ("1. We are going to the _____ this summer.", "beach"),
                ("2. I want to _____ in the sea.", "swim"),
                ("3. Don't forget to put on _____.", "sunscreen"),
                ("4. We will stay in a _____ near the sea.", "hotel"),
                ("5. My family loves going on _____.", "holiday"),
            ],
            "grammar": [
                ("1. We are going _____ (visit) Antalya.", "to visit"),
                ("2. I _____ (travel) to Bodrum next week.", "am going to travel"),
                ("3. She _____ (pack) her suitcase now.", "is packing"),
                ("4. _____ you going to swim every day?", "Are"),
                ("5. They _____ (not/stay) at a hotel.", "aren't going to stay"),
            ],
            "reading_text": (
                "This summer, Burak and his family are going to Antalya. They are going to stay "
                "at a hotel near the beach. Burak wants to swim every day and build sandcastles. "
                "His sister wants to collect shells. They are very excited about the holiday!"
            ),
            "reading_qs": [
                ("1. Where are they going this summer?", "Antalya"),
                ("2. What does Burak want to do?", "Swim every day and build sandcastles"),
                ("3. What does his sister want to collect?", "Shells"),
            ],
        },
        9: {  # After Unit 9
            "title": "Progress Check 3 (Units 7-9)",
            "vocab": [
                ("1. A very large grey animal with a trunk is an _____.", "elephant"),
                ("2. The place where you can swim in the sea is a _____.", "beach"),
                ("3. A person who helps sick people is a _____.", "doctor"),
                ("4. You should study hard for your _____.", "exams"),
                ("5. We _____ respect our teachers.", "must/should"),
            ],
            "grammar": [
                ("1. I _____ (visit) the zoo last Sunday.", "visited"),
                ("2. She _____ (go) to Antalya yesterday.", "went"),
                ("3. We are _____ (go) to travel next summer.", "going"),
                ("4. You _____ eat more vegetables. (advice)", "should"),
                ("5. _____ you _____ (see) the film last night?", "Did ... see"),
            ],
            "reading_text": (
                "Last weekend, Emre went to the zoo with his family. He saw elephants, monkeys "
                "and flamingos. The monkeys were the funniest animals. After the zoo, they "
                "went to a restaurant. Emre ate a hamburger and drank orange juice. "
                "It was a wonderful day!"
            ),
            "reading_qs": [
                ("1. Which animals were the funniest?", "Monkeys"),
                ("2. Where did they go after the zoo?", "A restaurant"),
                ("3. What did Emre eat?", "A hamburger"),
            ],
        },
        10: {  # Unit 10 — Stories, Heritage & Digital Life
            "title": "Progress Check — Unit 10 (Year Review)",
            "vocab": [
                ("1. A traditional story passed down through generations is a _____.", "legend"),
                ("2. The internet allows us to _____ information.", "share"),
                ("3. Turkey is famous for its cultural _____.", "heritage"),
                ("4. We should use technology _____.", "responsibly"),
                ("5. Reading books helps us use our _____.", "imagination"),
            ],
            "grammar": [
                ("1. I _____ (learn) a lot this year.", "have learned"),
                ("2. She _____ (read) three books last month.", "read"),
                ("3. We _____ (not/use) phones in class.", "mustn't use"),
                ("4. He said he _____ (enjoy) the school trip.", "enjoyed"),
                ("5. Next year, I _____ (be) in the 6th grade.", "will be"),
            ],
            "reading_text": (
                "This year was amazing! We learned about many topics: our families, "
                "our neighbourhood, weather, shopping, hobbies, animals and holidays. "
                "We also discovered Turkish legends and how to use technology safely. "
                "English class was fun because we did projects, sang songs and worked "
                "together. I am ready for the 6th grade!"
            ),
            "reading_qs": [
                ("1. What topics did they learn about?", "Families, neighbourhood, weather, shopping, hobbies, animals and holidays"),
                ("2. What did they discover about Turkey?", "Turkish legends"),
                ("3. Why was English class fun?", "Because they did projects, sang songs and worked together"),
            ],
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# LISTENING SCRIPTS — Grade 5 (real audio transcripts per unit)
# ══════════════════════════════════════════════════════════════════════════════

_LISTENING_SCRIPT_BANK = {
    5: {
        1: {"title": "My New Timetable",
            "script": (
                "Narrator: Listen to Elif talking about her school timetable. Complete the table.\n\n"
                "Elif: Hi! My name is Elif and I'm in the 5th grade. Let me tell you about my weekly timetable. "
                "On Monday, I have Maths first, then Turkish, and English after the break. I love Mondays because "
                "English is my favourite! On Tuesday, I have Science in the morning and Music in the afternoon. "
                "Wednesday is a long day — I have Maths, Art, and PE. PE is fun because we play basketball! "
                "On Thursday, I have English again — two hours! We also have Social Studies. Friday is the "
                "best day because we have Art in the morning and finish early at two o'clock. After school on "
                "Fridays, I always go to the bookshop with my best friend, Sude."),
            "tasks": [
                "1. Complete the timetable with the correct subjects.",
                "2. What is Elif's favourite day? Why?",
                "3. What does Elif do on Friday afternoons?",
            ]},
        2: {"title": "Describing People",
            "script": (
                "Narrator: Listen to Kerem describing his family for a school project.\n\n"
                "Kerem: OK, so this is my family photo. In the middle, that's my dad. He's quite tall — about "
                "one metre eighty. He has short black hair and brown eyes. He's wearing a blue shirt in this "
                "photo. Next to him is my mum. She's shorter than my dad. She has long, wavy brown hair and "
                "she's wearing her favourite green dress. She's really kind — everyone loves her! The boy on "
                "the left is my big brother, Can. He's sixteen and he looks like my dad — tall, dark hair. "
                "He's the sporty one in our family. And the little girl sitting on the floor is my sister, Ece. "
                "She's only five! She has curly blonde hair and the biggest smile you've ever seen. Oh, and "
                "the dog next to her is Boncuk — he's part of the family too!"),
            "tasks": [
                "1. Match each family member with their description.",
                "2. Who is the tallest person in the family?",
                "3. How old is Kerem's sister?",
            ]},
        3: {"title": "Finding the Library",
            "script": (
                "Narrator: Listen to a tourist asking for directions. Follow the route on the map.\n\n"
                "Tourist: Excuse me, can you help me? I'm looking for the public library.\n"
                "Local: Of course! It's not far from here. Go straight along this road for about two hundred "
                "metres. You'll pass a big white mosque on your left. Keep going straight until you reach "
                "the traffic lights.\n"
                "Tourist: OK, straight ahead to the traffic lights...\n"
                "Local: Right. At the traffic lights, turn left. Walk past the bakery — you'll smell the "
                "fresh bread! — and then past the pharmacy. The library is the big brown building on your "
                "right, between the pharmacy and the post office. There's a Turkish flag outside.\n"
                "Tourist: So, straight, left at the lights, past the bakery and pharmacy...\n"
                "Local: Exactly! It takes about five minutes on foot.\n"
                "Tourist: Thank you so much!\n"
                "Local: You're welcome! Enjoy the library — it has a great children's section."),
            "tasks": [
                "1. Draw the route on your map.",
                "2. What is next to the library?",
                "3. How long does it take to walk there?",
            ]},
        4: {"title": "Weather Forecast",
            "script": (
                "Narrator: Listen to the weather forecast for this week in Turkey.\n\n"
                "Presenter: Good morning! Here is your weekly weather forecast. Today, Monday, it is sunny and "
                "warm in Istanbul — twenty-two degrees. But take your umbrella tomorrow! On Tuesday, we expect "
                "heavy rain all day with temperatures dropping to fifteen degrees. Wednesday will be cloudy "
                "but dry — a good day for a walk in the park. Now, let's look at the south. Antalya is "
                "having beautiful weather all week — sunny skies and thirty degrees! Perfect beach weather. "
                "Moving east, Erzurum will be quite cold this week — only five degrees on Thursday and there "
                "may be snow on Friday! If you're in Ankara, expect a mix — sunny on Monday and Tuesday, but "
                "windy and cool for the rest of the week, around twelve degrees. Have a great week, everyone!"),
            "tasks": [
                "1. Complete the weather table for each city.",
                "2. Which city is the warmest this week?",
                "3. When will it rain in Istanbul?",
            ]},
        5: {"title": "At the School Canteen",
            "script": (
                "Narrator: Listen to the conversation at the school canteen. Answer the questions.\n\n"
                "Canteen Lady: Good morning! What would you like today?\n"
                "Student 1 (Elif): Can I have a cheese sandwich and an apple juice, please?\n"
                "Canteen Lady: Of course. That's six liras altogether.\n"
                "Elif: Here you are. Thank you!\n"
                "Canteen Lady: You're welcome, dear. Next!\n"
                "Student 2 (Burak): Hello! How much is the chicken wrap?\n"
                "Canteen Lady: It's eight liras. Would you like anything to drink?\n"
                "Burak: Yes, please. A bottle of water. How much is that?\n"
                "Canteen Lady: Water is two liras. So that's ten liras in total.\n"
                "Burak: Oh, I only have nine liras!\n"
                "Canteen Lady: Don't worry, you can have the water for one lira today.\n"
                "Burak: Really? Thank you so much!"),
            "tasks": [
                "1. What does Elif buy? How much does she pay?",
                "2. Why can't Burak pay the full price?",
                "3. How much does Burak pay in the end?",
            ]},
        6: {"title": "Weekend Plans",
            "script": (
                "Narrator: Listen to three friends talking about their weekend plans.\n\n"
                "Selin: So, what are you guys doing this weekend?\n"
                "Kerem: Well, on Saturday morning, I'm going to my guitar lesson as usual. In the afternoon, "
                "I'm playing football with the neighbourhood team. What about you, Selin?\n"
                "Selin: I'm visiting my grandmother on Saturday. She lives in Bolu and we're going to make "
                "mantı together — it's my favourite food! On Sunday, I'm going to read my new Harry Potter "
                "book. I love reading!\n"
                "Deniz: That sounds great! I'm going to the cinema on Saturday. There's a new animated film. "
                "On Sunday morning, I have swimming practice at the sports centre. After that, I'm going to "
                "work on my science project. It's about volcanoes!\n"
                "Kerem: Cool! On Sunday, I don't have any plans. Maybe I'll just play video games and relax.\n"
                "Selin: Lazy! You should come to Bolu with me — grandma makes amazing cookies too!"),
            "tasks": [
                "1. Complete the table: Who does what on Saturday/Sunday?",
                "2. What is Deniz's science project about?",
                "3. What does Selin invite Kerem to do?",
            ]},
        7: {"title": "The School Trip",
            "script": (
                "Narrator: Listen to a teacher giving information about a school trip.\n\n"
                "Mr. Yilmaz: Good morning, class! I have exciting news. Next Wednesday, we're going on a "
                "trip to the Natural History Museum. The bus will leave from the school gate at eight thirty, "
                "so please be here by eight fifteen. Don't be late! The journey takes about forty-five minutes. "
                "When we arrive, we'll first visit the dinosaur hall. The museum has a real T-Rex skeleton — "
                "it's the biggest dinosaur in Turkey! After that, we'll see the ocean life section with sharks, "
                "whales and dolphins. Then we'll have lunch in the museum garden — please bring a packed lunch "
                "and a bottle of water. In the afternoon, there's a special workshop about fossils where "
                "you can touch real fossils that are millions of years old! We'll leave the museum at three "
                "o'clock and be back at school by four. Oh, and one more thing — please wear comfortable shoes "
                "because we'll walk a lot. Any questions?"),
            "tasks": [
                "1. What time should students arrive at school?",
                "2. What will they see first at the museum?",
                "3. What should students bring with them?",
            ]},
        8: {"title": "Booking a Holiday",
            "script": (
                "Narrator: Listen to a family calling a hotel to book a holiday.\n\n"
                "Receptionist: Good afternoon, Sunshine Hotel Antalya. How can I help you?\n"
                "Dad: Hello! I'd like to book a family room for July, please.\n"
                "Receptionist: Of course. How many people?\n"
                "Dad: Four — two adults and two children. The children are eleven and seven.\n"
                "Receptionist: Perfect. We have a lovely family room with a sea view. When would you "
                "like to arrive?\n"
                "Dad: On the fifth of July, and we'd like to stay for two weeks.\n"
                "Receptionist: Let me check... Yes, that's available. The room is three hundred liras per "
                "night, but for two weeks, we can offer a discount — two hundred and fifty liras per night.\n"
                "Dad: That sounds great! Is breakfast included?\n"
                "Receptionist: Yes, breakfast and dinner are both included. We also have a swimming pool, "
                "a kids' club and a private beach.\n"
                "Dad: Wonderful! I'd like to book it, please.\n"
                "Receptionist: Excellent! Can I have your name, please?"),
            "tasks": [
                "1. How many people are in the family?",
                "2. What is the discounted price per night?",
                "3. What is included in the price?",
            ]},
        9: {"title": "Career Talk",
            "script": (
                "Narrator: Listen to a guest speaker at school talking about her job.\n\n"
                "Guest: Good morning, everyone! My name is Dr. Zeynep Kaya and I'm a marine biologist. "
                "That means I study life in the ocean — fish, dolphins, coral reefs and even tiny "
                "organisms you can't see with your eyes. I work at a research centre in Izmir, but I "
                "also travel to different countries. Last year, I went to Australia to study the Great "
                "Barrier Reef. It was amazing! I became interested in the ocean when I was your age — "
                "about eleven. My father took me snorkelling in Kas and I saw so many beautiful fish! "
                "From that day, I knew I wanted to study the sea. To become a marine biologist, you "
                "should love science and nature. You must study Biology and Chemistry at university. "
                "You also have to learn English because all scientific papers are in English. My advice "
                "to you: follow your passion, work hard, and never stop being curious about the world!"),
            "tasks": [
                "1. What does a marine biologist study?",
                "2. Where did Dr. Kaya travel last year?",
                "3. What subjects should you study to be a marine biologist?",
            ]},
        10: {"title": "A Radio Programme About Turkey",
            "script": (
                "Narrator: Listen to a children's radio programme about Turkish culture.\n\n"
                "Host: Welcome to 'Kids Explore!' Today we're learning about Turkey — one of the most "
                "fascinating countries in the world! Let's start with some amazing facts. Did you know that "
                "Turkey is on two continents? The European part is called Thrace and the Asian part is Anatolia, "
                "connected by the famous Bosphorus Bridge in Istanbul. Here's another fact — Turkey has been "
                "home to many ancient civilisations. The city of Troy, from the famous Trojan War, was in "
                "Turkey! And Turkish people gave the world many wonderful things. For example, tulips — yes, "
                "the flower we associate with the Netherlands was actually first grown in Ottoman Turkey! "
                "Turkish cuisine is world-famous too. Kebabs, baklava, Turkish delight and of course Turkish "
                "tea and coffee. The tradition of Turkish coffee is so important that UNESCO added it to its "
                "cultural heritage list in twenty thirteen. And finally, let's talk about Nasreddin Hodja — "
                "a legendary figure known for his wisdom and humour. His stories have been told for over "
                "seven hundred years and they're still funny today! That's all for today, kids. See you next week!"),
            "tasks": [
                "1. On which two continents is Turkey?",
                "2. Name three Turkish foods mentioned in the programme.",
                "3. When was Turkish coffee added to UNESCO's list?",
            ]},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# MODEL WRITING TEXTS — Grade 5 (example texts for Writing Workshop)
# ══════════════════════════════════════════════════════════════════════════════

_MODEL_WRITING_BANK = {
    5: {
        1: {"type": "Paragraph", "title": "My Typical School Day",
            "text": ("I wake up at seven o'clock every morning. First, I brush my teeth and wash my face. "
                     "Then I put on my school uniform and have breakfast with my family. I usually eat "
                     "cheese, bread and olives. I go to school by bus. School starts at half past eight "
                     "and finishes at three o'clock. My favourite lesson is English because the teacher "
                     "makes it fun. After school, I do my homework, play with my friends and read a book "
                     "before bed. I really enjoy my school days!"),
            "focus": "Present Simple for daily routines, time expressions, sequencing words (first, then, after)"},
        2: {"type": "Description", "title": "My Best Friend",
            "text": ("My best friend is Arda. He is eleven years old and he is in my class. He is tall "
                     "and thin with short brown hair and dark eyes. He always wears a big smile! Arda is "
                     "very kind and funny — he makes everyone laugh. His favourite subject is Maths because "
                     "he loves numbers. After school, we usually ride our bikes together in the park. He "
                     "has a dog called Pamuk and a cat called Tekir. I think Arda is the best friend in "
                     "the world because he always helps me when I need him."),
            "focus": "Have/has for descriptions, adjectives for appearance and personality, possessive adjectives"},
        3: {"type": "Description", "title": "My Dream Neighbourhood",
            "text": ("In my dream neighbourhood, there is a big park with tall trees and a lake in the "
                     "middle. Next to the park, there is a modern library with thousands of books and free "
                     "Wi-Fi. Across from the library, there is a sports centre where you can swim, play "
                     "basketball and do gymnastics. Between the sports centre and the school, there is "
                     "a pet shop with cute puppies in the window. My house is opposite the park, so I can "
                     "see the trees from my bedroom. The best thing about my dream neighbourhood is that "
                     "everything is within walking distance!"),
            "focus": "There is/are, prepositions of place (next to, across from, between, opposite)"},
        4: {"type": "Postcard", "title": "A Holiday Postcard",
            "text": ("Dear Selin,\n\nGreetings from Antalya! The weather here is amazing — it is sunny "
                     "and very hot, about 35 degrees! I am having a wonderful time. Yesterday, I swam in "
                     "the sea and built a huge sandcastle. Today, it is a bit cloudy, so we are visiting "
                     "the old town. The streets are beautiful and there are so many shops! Tomorrow, if it "
                     "is sunny again, we are going to try parasailing. I am a little nervous but excited! "
                     "I can't wait to tell you all about it when I get back.\n\nSee you soon,\nElif"),
            "focus": "Weather expressions, Present Continuous for now, can/can't, informal letter format"},
        5: {"type": "Dialogue", "title": "At the Supermarket",
            "text": ("Customer: Good morning! Can I have a loaf of bread, please?\n"
                     "Shopkeeper: Of course! Would you like white or brown bread?\n"
                     "Customer: Brown bread, please. How much is it?\n"
                     "Shopkeeper: It's four liras. Anything else?\n"
                     "Customer: Yes, I need some cheese. How much is a kilo of white cheese?\n"
                     "Shopkeeper: Thirty-five liras per kilo.\n"
                     "Customer: That's a bit expensive! Can I have half a kilo?\n"
                     "Shopkeeper: Sure. That's seventeen liras fifty. So, bread and cheese — twenty-one "
                     "liras fifty in total.\n"
                     "Customer: Here you are. Thank you!\n"
                     "Shopkeeper: Thank you! Have a nice day!"),
            "focus": "How much...?, Can I have...?, numbers and prices, polite requests"},
        6: {"type": "Blog Post", "title": "My Favourite Hobby",
            "text": ("My Favourite Hobby by Kerem, Age 11\n\n"
                     "I love playing the guitar! I started learning two years ago and now I can play "
                     "ten songs. I go to guitar class every Sunday morning. My teacher, Mr. Ozan, is "
                     "really patient and encouraging. I enjoy playing pop songs the most, but I also like "
                     "playing folk music. My favourite thing is when my family sits in the garden and I "
                     "play songs for them. They always clap and say 'Bravo!' I think playing an instrument "
                     "is a great hobby because it makes you happy, creative and confident. I recommend "
                     "everyone to try learning an instrument — it's never too late to start!"),
            "focus": "Like/enjoy/love + V-ing, adverbs of frequency, giving opinions and recommendations"},
        7: {"type": "Report", "title": "My Favourite Animal: The Elephant",
            "text": ("The African elephant is the largest land animal in the world. It can grow up to "
                     "four metres tall and weigh more than six thousand kilograms! Elephants are herbivores "
                     "— they eat grass, leaves, bark and fruit. They can eat up to 150 kilograms of food "
                     "per day! Elephants are very intelligent and have excellent memories. They live in "
                     "family groups led by the oldest female, called the matriarch. Baby elephants stay "
                     "with their mothers for many years. Sadly, elephants are endangered because of habitat "
                     "loss and illegal hunting. We must protect these amazing animals for future generations."),
            "focus": "Simple Past for facts, can for ability, comparatives (bigger than, larger than), must for obligation"},
        8: {"type": "Plan", "title": "My Summer Holiday Plan",
            "text": ("This summer, I am going to have an amazing holiday! In July, my family and I are "
                     "going to travel to Bodrum by car. We are going to stay in a hotel near the beach "
                     "for ten days. I am going to swim every morning and learn windsurfing in the afternoon. "
                     "My sister is going to join a kids' art club at the hotel. In the evening, we are "
                     "going to walk along the harbour and eat ice cream. My dad is going to take us on "
                     "a boat trip to a nearby island. I am also going to read three books — I've already "
                     "chosen them! I can't wait for summer to begin!"),
            "focus": "Be going to for future plans, time expressions (in July, every morning, in the evening)"},
        9: {"type": "Opinion", "title": "The Best Job in the World",
            "text": ("I think being a teacher is the best job in the world. First, teachers help children "
                     "learn new things every day. They should be patient because every student learns at a "
                     "different speed. Second, teachers must be creative to make lessons interesting. A good "
                     "teacher uses games, videos and projects — not just textbooks! Third, teachers have to "
                     "be good listeners because students sometimes have problems. Finally, I believe teachers "
                     "change lives. My English teacher, Ms. Aylin, always tells us: 'You should believe in "
                     "yourselves.' Because of her, I love learning English. That's why I think teaching is "
                     "the most important job."),
            "focus": "Should/must/have to for advice and obligation, sequencing (first, second, finally), opinion phrases"},
        10: {"type": "Story", "title": "A Special Day",
            "text": ("Last weekend, something very special happened. First, my grandmother came to visit us "
                     "from Konya. We were very happy to see her because she hadn't visited for six months. "
                     "Then my father cooked a big breakfast — eggs, sausages, cheese, olives and fresh bread. "
                     "After that, we went to the park and my grandmother told us stories about her childhood. "
                     "She said life was very different fifty years ago — there were no computers, no phones, "
                     "and children played outside all day! Next, we visited the old bazaar and bought Turkish "
                     "delight for dessert. Finally, in the evening, we sat together and looked at old family "
                     "photos. Although it was a simple day, it was one of the best days of my life because "
                     "we were all together."),
            "focus": "Linking words (first, then, after that, next, finally, because, although), Simple Past tense"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PRONUNCIATION CORNER — Grade 5
# ══════════════════════════════════════════════════════════════════════════════

_PRONUNCIATION_BANK = {
    5: {
        1: {"focus": "The /s/ and /z/ sounds in 3rd person",
            "rule": "After voiceless sounds (p, t, k, f), add /s/. After voiced sounds, add /z/.",
            "examples": [("walks /s/", "runs /z/"), ("eats /s/", "plays /z/"),
                         ("likes /s/", "goes /z/"), ("stops /s/", "lives /z/")],
            "practice": ["reads", "writes", "takes", "gives", "wakes", "sings"],
            "tongue_twister": "She sells seashells by the seashore."},
        2: {"focus": "Short vowels: /ae/ vs /e/",
            "rule": "/ae/ is in 'cat, hat, man'. /e/ is in 'bed, red, ten'. Open your mouth wide for /ae/.",
            "examples": [("man /ae/", "men /e/"), ("bad /ae/", "bed /e/"),
                         ("hat /ae/", "het -"), ("pan /ae/", "pen /e/")],
            "practice": ["dad", "said", "land", "lend", "sat", "set"],
            "tongue_twister": "A fat cat sat on a flat mat and had a chat."},
        3: {"focus": "The /th/ sounds: /T/ and /D/",
            "rule": "/T/ (thin, think) is voiceless. /D/ (this, that) is voiced. Put your tongue between your teeth!",
            "examples": [("think /T/", "this /D/"), ("three /T/", "there /D/"),
                         ("bath /T/", "bathe /D/"), ("thank /T/", "that /D/")],
            "practice": ["the", "them", "with", "north", "south", "mother"],
            "tongue_twister": "The thirty-three thieves thought that they thrilled the throne."},
        4: {"focus": "Word stress in two-syllable words",
            "rule": "Most nouns stress the FIRST syllable: WEAther, WINter. Most verbs stress the SECOND: enJOY, beLIEVE.",
            "examples": [("WEA-ther", "en-JOY"), ("SUM-mer", "be-GIN"),
                         ("WIN-ter", "be-LIEVE"), ("AU-tumn", "for-GET")],
            "practice": ["season", "listen", "answer", "prefer", "repeat", "compare"],
            "tongue_twister": "Whether the weather is fine or whether the weather is not."},
        5: {"focus": "Numbers and prices: stress patterns",
            "rule": "Stress the important number word. 'FIFteen' (15) vs 'FIFty' (50). Listen carefully to avoid confusion!",
            "examples": [("FIF-teen (15)", "FIF-ty (50)"), ("THIR-teen (13)", "THIR-ty (30)"),
                         ("FOUR-teen (14)", "FOR-ty (40)"), ("SIX-teen (16)", "SIX-ty (60)")],
            "practice": ["eighteen / eighty", "nineteen / ninety", "fifteen / fifty"],
            "tongue_twister": "Fifteen flies flew from the fifty-fifth floor."},
        6: {"focus": "The /I/ and /i:/ sounds",
            "rule": "/I/ is short (sit, bit, fish). /i:/ is long (see, tree, key). /i:/ takes longer to say.",
            "examples": [("sit /I/", "seat /i:/"), ("bit /I/", "beat /i:/"),
                         ("ship /I/", "sheep /i:/"), ("live /I/", "leave /i:/")],
            "practice": ["fill / feel", "hit / heat", "lip / leap", "rich / reach"],
            "tongue_twister": "She sees cheese and she seizes the cheese she sees."},
        7: {"focus": "Past tense -ed pronunciation",
            "rule": "After /t/ or /d/ say /Id/ (visited). After voiceless sounds say /t/ (walked). Otherwise say /d/ (played).",
            "examples": [("visited /Id/", "walked /t/"), ("wanted /Id/", "stopped /t/"),
                         ("started /Id/", "played /d/"), ("needed /Id/", "loved /d/")],
            "practice": ["watched", "opened", "landed", "helped", "enjoyed", "painted"],
            "tongue_twister": "He walked, talked, and started to study."},
        8: {"focus": "Sentence stress and intonation",
            "rule": "Stress content words (nouns, verbs, adjectives). Unstress grammar words (a, the, is, to).",
            "examples": [("I'm GOING to SWIM.", ""), ("We're going to STAY for THREE WEEKS.", ""),
                         ("She's going to VISIT her GRANDmother.", "")],
            "practice": ["I'm going to BUILD a sandcastle.", "We're going to DRIVE to Antalya.",
                         "He's going to TRY snorkelling."],
            "tongue_twister": "I'm going to go to the going-away party that's going on."},
        9: {"focus": "Modal verbs: weak and strong forms",
            "rule": "'Should' is often weak /Sd/. 'Must' is strong /m^st/. 'Can' is weak /kn/ in statements, strong /kaen/ in questions.",
            "examples": [("You should /Sd/ study.", "You MUST /m^st/ stop!"),
                         ("I can /kn/ swim.", "CAN /kaen/ you swim?")],
            "practice": ["You should try.", "You must listen.", "Can you help?",
                         "I can't go.", "You have to wait."],
            "tongue_twister": "Can you can a can as a canner can can a can?"},
        10: {"focus": "Linking words in connected speech",
            "rule": "In natural speech, words connect: 'an apple' sounds like 'a-napple'. Final consonant links to next vowel.",
            "examples": [("an_apple", "turn_off"), ("look_at", "come_in"),
                         ("first_of_all", "not_at_all")],
            "practice": ["pick it up", "look at it", "turn it on", "a lot of", "kind of", "sort of"],
            "tongue_twister": "An ape ate an acorn and an orange after an awful afternoon."},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# WORKBOOK EXERCISES — Grade 5 (extra practice per unit)
# ══════════════════════════════════════════════════════════════════════════════

_WORKBOOK_BANK = {
    5: {
        1: {"exercises": [
            {"type": "unscramble", "instr": "Unscramble the words to make sentences.",
             "items": ["school / goes / She / to / every day", "at / wakes / He / up / seven",
                       "have / Mondays / We / English / on", "homework / my / I / after / do / school"]},
            {"type": "correct", "instr": "Find and correct the mistakes.",
             "items": ["She go to school by bus.", "I doesn't like Maths.",
                       "Do he play football?", "They plays tennis on Fridays."]},
            {"type": "complete", "instr": "Complete the text with the correct form of the verbs.",
             "items": ["Elif _____ (wake) up at seven. She _____ (brush) her teeth and _____ (have) "
                       "breakfast. She _____ (go) to school by bus. She _____ (not/like) Maths but "
                       "she _____ (love) English."]},
        ]},
        2: {"exercises": [
            {"type": "match", "instr": "Match the descriptions with the pictures (write the name).",
             "items": ["She has long brown hair and blue eyes.", "He is tall and has short black hair.",
                       "She has curly blonde hair and is very cheerful.", "He has a beard and wears glasses."]},
            {"type": "fill", "instr": "Fill in with my, your, his, her, its, our, their.",
             "items": ["This is _____ sister. (I)", "Is that _____ book? (you)",
                       "She loves _____ dog. (she)", "We live in _____ house. (we)",
                       "They wash _____ hands before lunch. (they)"]},
            {"type": "write", "instr": "Write 6 sentences describing your family members.",
             "items": ["Use: have/has, be + adjective, possessive adjectives"]},
        ]},
        3: {"exercises": [
            {"type": "map", "instr": "Look at the map and complete the sentences with prepositions.",
             "items": ["The bank is _____ the school.", "The park is _____ the mosque and the library.",
                       "The hospital is _____ the post office.", "The bakery is _____ _____ the pharmacy."]},
            {"type": "directions", "instr": "Write directions from the school to the hospital.",
             "items": ["Use: go straight, turn left/right, it's on your left/right, next to, opposite"]},
            {"type": "correct", "instr": "Correct the mistakes.",
             "items": ["There is three shops.", "There are a park.", "The bank is among the two buildings.",
                       "Go straight and turn to left."]},
        ]},
        4: {"exercises": [
            {"type": "fill", "instr": "Complete with can, can't, is/are + V-ing.",
             "items": ["She _____ swim very well. (ability: yes)", "Look! It _____ (snow) outside!",
                       "I _____ play the piano. (ability: no)", "They _____ (play) football right now.",
                       "We _____ speak three languages. (ability: yes)"]},
            {"type": "weather", "instr": "Look at the weather icons and write sentences.",
             "items": ["[sun] Istanbul: _____", "[rain] London: _____",
                       "[snow] Erzurum: _____", "[cloud] Ankara: _____"]},
            {"type": "write", "instr": "Write about your abilities. Use can/can't.",
             "items": ["Write 6 sentences: 3 things you CAN do and 3 things you CAN'T do."]},
        ]},
        5: {"exercises": [
            {"type": "fill", "instr": "Complete with some, any, much, many, a few, a little.",
             "items": ["How _____ apples do we need?", "There isn't _____ milk in the fridge.",
                       "I have _____ _____ money left. (small amount)", "Are there _____ eggs?",
                       "We need _____ sugar for the cake."]},
            {"type": "prices", "instr": "Read the price list and answer the questions.",
             "items": ["Tomatoes: 8 TL/kg | Cheese: 35 TL/kg | Bread: 4 TL | Milk: 12 TL/L",
                       "1. How much is 2 kg of tomatoes?", "2. How much is half a kilo of cheese?",
                       "3. You buy bread, 1L milk and 1kg tomatoes. Total = ?"]},
            {"type": "dialogue", "instr": "Write a shopping dialogue (at least 10 lines).",
             "items": ["Use: How much...?, Can I have...?, Here you are, Anything else?"]},
        ]},
        6: {"exercises": [
            {"type": "fill", "instr": "Complete with the -ing form.",
             "items": ["I enjoy _____ (swim).", "She likes _____ (dance).",
                       "He hates _____ (get up) early.", "We love _____ (travel).",
                       "Do you mind _____ (wait)?"]},
            {"type": "survey", "instr": "Do a class survey about hobbies. Ask 5 classmates.",
             "items": ["Name | Hobby 1 | Hobby 2 | Favourite | How often?",
                       "Write a report: 'Three students like..., Two students enjoy...'"]},
            {"type": "write", "instr": "Write a blog post about YOUR favourite hobby (60+ words).",
             "items": ["Include: what it is, when you do it, why you like it, who you do it with"]},
        ]},
        7: {"exercises": [
            {"type": "fill", "instr": "Write the Past Simple form.",
             "items": ["go → _____", "see → _____", "eat → _____", "buy → _____",
                       "make → _____", "take → _____", "swim → _____", "write → _____"]},
            {"type": "negative", "instr": "Make these sentences negative.",
             "items": ["I visited the zoo.", "She went to school.", "They ate pizza.",
                       "We played football.", "He bought a book."]},
            {"type": "write", "instr": "Write about a trip you took. Use Past Simple (80+ words).",
             "items": ["Include: Where? When? Who with? What did you see? Did you enjoy it?"]},
        ]},
        8: {"exercises": [
            {"type": "fill", "instr": "Complete with going to.",
             "items": ["I _____ (visit) my aunt next week.", "She _____ (buy) a new phone.",
                       "We _____ (not/travel) this summer.", "_____ they _____ (come) to the party?",
                       "He _____ (learn) Spanish next year."]},
            {"type": "plan", "instr": "Write a 7-day holiday plan using 'going to'.",
             "items": ["Day 1: _____ | Day 2: _____ | ... | Day 7: _____",
                       "Example: On Day 1, I'm going to arrive at the hotel and swim."]},
            {"type": "postcard", "instr": "Write a holiday postcard to your friend (60+ words).",
             "items": ["Include: where you are, weather, what you did, what you're going to do"]},
        ]},
        9: {"exercises": [
            {"type": "match", "instr": "Match the advice with the situation.",
             "items": ["I'm tired. → You should _____ .", "I have a test tomorrow. → You must _____ .",
                       "It's raining. → You should _____ .", "I want to be a pilot. → You have to _____ ."]},
            {"type": "fill", "instr": "Complete with should, must, have to, don't have to.",
             "items": ["You _____ wear a uniform at school. (rule)", "You _____ eat more fruit. (advice)",
                       "Students _____ run in the corridors. (prohibition)",
                       "You _____ come tomorrow — it's a holiday. (not necessary)"]},
            {"type": "write", "instr": "Write advice for a new student at your school (8 sentences).",
             "items": ["Use should, must, have to, and don't have to at least twice each."]},
        ]},
        10: {"exercises": [
            {"type": "order", "instr": "Put the sentences in the correct order to make a story.",
             "items": ["Finally, they all lived happily.", "First, there was a clever boy called Keloglan.",
                       "Then, the king gave him a difficult task.", "After that, he solved the problem.",
                       "Next, he travelled to the palace."]},
            {"type": "fill", "instr": "Complete with linking words: first, then, because, but, although, finally.",
             "items": ["_____, I woke up early. _____, I had breakfast.",
                       "I was tired _____ I studied all night.",
                       "_____ it was cold, we went to the park.",
                       "She wanted to go _____ she was sick."]},
            {"type": "write", "instr": "Write a short story about a cultural tradition (80+ words).",
             "items": ["Use at least 5 linking words. Include: first, then, next, after that, finally."]},
        ]},
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# STORY UNIVERSE — Grade 5 (recurring characters + episode per unit)
# ══════════════════════════════════════════════════════════════════════════════

_STORY_CHARACTERS = {
    5: {
        "main": [
            {"name": "Elif", "age": 10, "desc": "Curious and brave. Loves reading and solving puzzles.", "emoji": "girl"},
            {"name": "Can", "age": 11, "desc": "Sporty and funny. Always makes everyone laugh.", "emoji": "boy"},
            {"name": "Sude", "age": 10, "desc": "Creative and kind. Loves drawing and animals.", "emoji": "girl"},
            {"name": "Boncuk", "age": 3, "desc": "A clever golden retriever who understands everything!", "emoji": "dog"},
        ],
        "teacher": {"name": "Ms. Yildiz", "desc": "Their English teacher. Gives them special missions."},
    }
}

_STORY_BANK = {
    5: {
        1: {"title": "The Mysterious Map",
            "previously": None,
            "episode": (
                "It is the first day of school. Elif, Can and Sude are in the same class again — 5-A! "
                "Their new English teacher, Ms. Yildiz, walks in with a big smile. 'Welcome, everyone! "
                "This year, we have a special project,' she says. She opens an old wooden box and takes "
                "out a yellowed map. 'This is a treasure map of our school. There are 10 hidden clues. "
                "If you find all of them, you will discover a fantastic surprise at the end of the year!' "
                "Elif's eyes grow wide. Can whispers, 'This is going to be awesome!' Sude looks at Boncuk "
                "waiting outside the window. Even he looks excited! Ms. Yildiz gives them the first clue: "
                "'The first clue is hidden where you keep your favourite stories.' 'The library!' they all "
                "shout together. The adventure begins!"),
            "cliffhanger": "But when they run to the library, they find a locked door and a note in English on it... What does the note say?",
            "vocab_tie": ["map", "treasure", "clue", "library", "adventure"]},
        2: {"title": "The Note on the Door",
            "previously": "Ms. Yildiz gave them a treasure map with 10 clues. The first clue led to the library, but the door was locked!",
            "episode": (
                "The note on the library door says: 'Describe yourself in five sentences. Leave it under "
                "the big tree.' Elif thinks for a moment. 'I am ten years old. I have long brown hair "
                "and brown eyes. I am curious and I love books.' Can writes: 'I am tall. I have short "
                "black hair. I am sporty and funny.' Sude draws a small self-portrait next to her sentences. "
                "They put their papers under the old oak tree in the schoolyard. When they come back after lunch, "
                "the papers are gone! In their place, there is a small golden key and a new note: 'Well done! "
                "Use this key to open the library. Clue 2 is inside the book with a red cover on shelf 3.' "
                "They rush to the library, open the door, and find shelf 3. There are FIVE books with red covers! "
                "Which one has the clue?"),
            "cliffhanger": "Each red book has a different title. They must describe each book to find the right one. Can you help them?",
            "vocab_tie": ["describe", "tall", "short", "hair", "eyes"]},
        3: {"title": "The Hidden Message",
            "previously": "They found a golden key and opened the library. Now they must find a red book on shelf 3.",
            "episode": (
                "Sude reads the titles: 'Fairy Tales, Science World, City Maps, Animal Planet, Art for Kids.' "
                "Elif says, 'The first clue was about directions — the map! So maybe it is City Maps!' She opens "
                "the book. Inside, there is a folded paper with a hand-drawn map of the school neighbourhood. "
                "The map shows the school, the park, the mosque, the bakery and a big X near the post office. "
                "'X marks the spot!' says Can. 'But we need to follow the directions on the map.' The map says: "
                "'Go straight from the school gate. Turn left at the mosque. Walk past the bakery. The clue is "
                "between the post office and the pharmacy.' They follow the directions carefully. Between the "
                "two buildings, they find a small metal box buried in the flower bed. Inside is Clue 3: "
                "a photograph of four seasons with the words 'I love this one the most' written on the back."),
            "cliffhanger": "Which season does the clue refer to? And what does the photograph have to do with the next hiding spot?",
            "vocab_tie": ["straight", "turn left", "between", "mosque", "post office"]},
        4: {"title": "The Season Puzzle",
            "previously": "They followed a map to find a metal box. Inside was a photo of four seasons.",
            "episode": (
                "Elif studies the photograph. Each season has a different object: a snowman in winter, "
                "a kite in spring, a beach ball in summer, and a red leaf in autumn. 'I love this one the most' — "
                "but whose favourite season is it? They ask Ms. Yildiz. She smiles and says: 'It is sunny and hot. "
                "People swim and eat ice cream.' 'Summer!' they shout. Can looks at the map again. There is a "
                "small sun symbol near the school swimming pool. They run there! Behind the pool house, they find "
                "a waterproof envelope taped to the wall. Inside is a menu from a restaurant with some prices "
                "circled: 'Soup — 25 TL, Salad — 30 TL, Juice — 15 TL.' Under the menu, there is a question: "
                "'How much is lunch for two people?' Sude does the maths: 'Two soups, two salads and two juices... "
                "that is 140 TL!' A message appears at the bottom of the menu: 'Table 14 at the cafeteria.'"),
            "cliffhanger": "They go to the cafeteria but Table 14 is occupied by the school's mysterious janitor, Mr. Kemal...",
            "vocab_tie": ["sunny", "hot", "summer", "how much", "price"]},
        5: {"title": "Mr. Kemal's Secret",
            "previously": "A restaurant menu with maths led them to Table 14 in the cafeteria, where the school janitor Mr. Kemal sits.",
            "episode": (
                "Mr. Kemal looks up from his tea. 'Ah, you found me!' he says in English — perfect English! "
                "The children are shocked. 'I lived in London for ten years,' he explains with a wink. "
                "'I have something for you, but first you must go shopping for me.' He gives them a list: "
                "'I need a kilo of apples, half a kilo of cheese, two loaves of bread and a bottle of olive oil. "
                "Here is 100 TL. Bring me the receipt and the change.' They go to the school market. Apples are "
                "12 TL per kilo, cheese is 60 TL per kilo, bread is 8 TL per loaf, and olive oil is 45 TL. "
                "Can calculates: '12 + 30 + 16 + 45 = 103 TL. We don't have enough!' Elif has an idea: "
                "'Let's buy half a kilo of apples instead — 6 TL. Total: 97 TL. Change: 3 TL!' "
                "They bring everything to Mr. Kemal. He smiles and gives them Clue 5: a bus ticket with "
                "'Platform 6, Seat 14' written on it."),
            "cliffhanger": "There are no buses at school! But the old school bus in the parking lot has never been moved in years...",
            "vocab_tie": ["shopping", "kilo", "how much", "change", "receipt"]},
        6: {"title": "The Old School Bus",
            "previously": "Mr. Kemal gave them a bus ticket — Platform 6, Seat 14. The old school bus sits in the parking lot.",
            "episode": (
                "The old bus is dusty and covered in leaves. Can pulls the door open — it creaks loudly! "
                "They count the seats: 1, 2, 3... 14! Under seat 14, Sude finds a small speaker and a note: "
                "'Press play.' She presses the button. A recorded voice says: 'Hello, treasure hunters! "
                "I am the school's founder, Ahmet Bey. I built this school in 1965. I hid this treasure "
                "for future students who love learning. Listen carefully: I visit the art room every day at noon. "
                "I sit in the green chair. I paint with watercolours. I always clean my brushes after painting.' "
                "Elif writes every word. 'The art room!' says Sude. 'But which green chair? There are six!' "
                "Can reads the clue again: 'I always clean my brushes AFTER painting.' 'After! The cleaning "
                "area in the art room — where you wash brushes!' They run to the art room. Behind the sink, "
                "taped inside a cupboard, they find Clue 6: a small compass with a note: 'Go North.'"),
            "cliffhanger": "But the compass needle spins wildly and won't settle. Is it broken, or is something magnetic nearby?",
            "vocab_tie": ["listen", "daily routine", "always", "clean", "after"]},
        7: {"title": "The Compass Mystery",
            "previously": "They found a compass in the art room, but the needle keeps spinning!",
            "episode": (
                "Elif remembers something from Science class: 'Magnets make compasses go crazy!' They look "
                "around. There is a large magnet on the art room whiteboard! They move away from it. "
                "The compass settles — pointing north. 'North from the school is... the football field!' "
                "says Can, who knows every corner of the school. They walk north. At the football field, "
                "they find a small flag at the centre circle. Under it is a photo album with labels: "
                "'Sports Day 2020 — We WON the match!' 'School Trip 2019 — We VISITED the museum.' "
                "'Art Competition 2021 — Sude's sister DREW the best picture!' Can notices something: "
                "'All the labels are in the PAST TENSE!' Under the last photo, there is a question: "
                "'What DID Ahmet Bey DO every Saturday? Find his favourite place in the school.' "
                "They think hard. Elif says: 'He painted every day. On Saturdays, artists have exhibitions. "
                "The school hall — where we have exhibitions!'"),
            "cliffhanger": "The school hall is locked for renovation. They can hear strange sounds coming from inside...",
            "vocab_tie": ["visited", "won", "drew", "yesterday", "last week"]},
        8: {"title": "Behind the Curtain",
            "previously": "Past tense clues pointed to the school hall, but it's locked and strange sounds are coming from inside!",
            "episode": (
                "Can puts his ear to the door. 'It sounds like... music?' Boncuk barks and scratches at "
                "the side door. It is open! They tiptoe inside. The hall is dark, but on the stage, behind "
                "the curtain, there is a projector showing old photos of the school. A recorded voice says: "
                "'One day, I am going to build the best school in Turkey. I am going to plant a garden. "
                "Students are going to learn English and travel the world.' 'Going to!' says Elif. "
                "'He is talking about his FUTURE PLANS!' Under the projector, there is an envelope: "
                "'Clue 8: I am going to leave my most valuable thing in the place where new life begins.' "
                "Sude gasps: 'The school garden! He said he was going to plant a garden!' "
                "They run to the school garden. It is beautiful — full of flowers, vegetables and fruit "
                "trees. In the centre, there is an old stone bench with the words: 'SIT HERE AND THINK "
                "ABOUT TOMORROW.' Under the bench: Clue 8 — a sealed letter."),
            "cliffhanger": "The letter says: 'Do NOT open until you find Clue 9. You are going to need ALL the clues together.'",
            "vocab_tie": ["going to", "plan", "tomorrow", "future", "build"]},
        9: {"title": "The Teacher's Riddle",
            "previously": "They found a sealed letter under a bench in the garden. They need Clue 9 before opening it.",
            "episode": (
                "The next morning, Ms. Yildiz gives them a special task: 'Today you should work as a team. "
                "You must solve my riddle. You should listen carefully. You shouldn't give up!' Her riddle: "
                "'You should look where knowledge lives but books don't stay. You must ask the person who "
                "knows every student's name. You shouldn't forget — the answer is in your hands every day.' "
                "They think. 'Where knowledge lives but books don't stay...' Elif says: 'The computer lab! "
                "Knowledge lives there, but books don't stay — it is all digital!' 'The person who knows "
                "every student's name...' Can says: 'The headmaster!' They go to the headmaster, Mr. Demir. "
                "He smiles: 'Ms. Yildiz told me you would come. The answer is IN YOUR HANDS every day.' "
                "Sude looks at her hands. Her SCHOOL ID CARD! She flips it over. On the back, in tiny letters: "
                "'QR CODE — SCAN ME.' They scan it with a tablet. A video plays: Ahmet Bey, now very old, "
                "says: 'Congratulations! You have found 9 clues. The last clue... is each other.'"),
            "cliffhanger": "What does 'the last clue is each other' mean? They have the sealed letter, nine clues, and a big question...",
            "vocab_tie": ["should", "must", "shouldn't", "riddle", "team"]},
        10: {"title": "The Greatest Treasure",
             "previously": "Ahmet Bey's video said: 'The last clue is each other.' They have 9 clues and a sealed letter.",
             "episode": (
                 "They gather all their clues: the map, the golden key, the photograph, the menu, the bus ticket, "
                 "the compass, the photo album, the sealed letter and the QR code. Elif opens the sealed letter. "
                 "It reads: 'Dear future students, the treasure is not gold or jewels. The treasure is what you "
                 "have done together. You READ English to find clues. You SPOKE English to ask for help. You "
                 "LISTENED to recordings. You WROTE descriptions. You WORKED as a team. You LEARNED about your "
                 "school, your neighbourhood and your culture. The real treasure is YOUR ENGLISH and YOUR "
                 "FRIENDSHIP. Now, use your skills to write your OWN story and share it with the world.' "
                 "Ms. Yildiz walks in with a cake! 'You did it! Every skill you used this year helped you "
                 "solve the treasure hunt. I am so proud of you!' Can says: 'So the treasure was the adventure "
                 "itself?' Elif smiles: 'And the English we learned along the way.' Sude hugs Boncuk: "
                 "'And the friends we did it with.' THE END... or is it? On the last page of the map, "
                 "in tiny letters: 'P.S. Grade 6 has a NEW map. See you next year!'"),
             "cliffhanger": None,
             "vocab_tie": ["treasure", "friendship", "adventure", "skills", "together"]},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# TURKEY CORNER — Grade 5 (Turkish culture in English)
# ══════════════════════════════════════════════════════════════════════════════

_TURKEY_CORNER_BANK = {
    5: {
        1: {"title": "Turkish Schools Around the World",
            "text": ("Did you know that there are Turkish schools in more than 40 countries? From "
                     "Kazakhstan to Kenya, students learn Turkish, English and local languages together. "
                     "In Turkey, the school year starts in September and ends in June. Students wear "
                     "uniforms and have a 15-minute break after every 40-minute lesson. The Turkish "
                     "education system has 4+4+4 structure: four years of primary, four years of "
                     "middle school and four years of high school. The most famous school tradition "
                     "is the first day ceremony where first graders walk through a balloon arch!"),
            "famous_person": "Hasan Ali Yucel — Minister of Education who started the Village Institutes (Koy Enstituleri) in 1940.",
            "activity": "Compare your school with a typical school in England. Write 5 differences.",
            "recipe": None},
        2: {"title": "Turkish Family Life",
            "text": ("Turkish families are often close and large. Grandparents, uncles, aunts and cousins "
                     "usually live nearby and visit each other regularly. Family meals are very important — "
                     "especially Sunday breakfast (kahvalti), which can have 20 different dishes! Turkish "
                     "people show respect to elders by kissing their hand and touching it to their forehead. "
                     "Children call older people 'abi' (big brother) or 'abla' (big sister) even if they "
                     "are not related. Bayram visits are special — children visit relatives, kiss hands "
                     "and receive money or sweets. Family is the heart of Turkish culture."),
            "famous_person": "Aziz Sancar — Nobel Prize-winning Turkish scientist who always thanks his family in speeches.",
            "activity": "Draw your family tree and describe each person in English (name, age, appearance, personality).",
            "recipe": {"name": "Turkish Breakfast Menemen", "steps": ["Chop 2 tomatoes, 2 peppers, 1 onion.",
                        "Fry the onion in olive oil for 2 minutes.", "Add peppers, cook for 3 minutes.",
                        "Add tomatoes, salt and pepper. Cook for 5 minutes.", "Crack 3 eggs on top. Stir gently.",
                        "Cover and cook for 3 minutes. Serve with bread!"]}},
        3: {"title": "Amazing Places in Turkey",
            "text": ("Turkey is a bridge between Europe and Asia, and it has incredible places to visit. "
                     "Cappadocia is famous for its fairy chimneys — tall rock formations that look like "
                     "mushrooms! Thousands of tourists fly in hot air balloons over them every year. "
                     "Ephesus (Efes) is an ancient Roman city near Izmir with a huge library ruin. "
                     "Pamukkale, meaning 'Cotton Castle', has white travertine terraces filled with warm "
                     "thermal water. The Sumela Monastery hangs on a cliff in Trabzon, 1200 metres high. "
                     "And Istanbul's Grand Bazaar, built in 1461, is one of the oldest shopping centres "
                     "in the world with over 4,000 shops!"),
            "famous_person": "Evliya Celebi — the greatest Ottoman traveller who wrote a 10-volume travel book in the 1600s.",
            "activity": "Choose a place in Turkey. Write a postcard to a friend describing it in English.",
            "recipe": None},
        4: {"title": "Weather and Nature in Turkey",
            "text": ("Turkey has seven geographical regions, and each has different weather! The Black Sea "
                     "coast (Karadeniz) is rainy and green — perfect for tea plantations. The Mediterranean "
                     "coast is hot and sunny in summer, great for beach holidays. Central Anatolia has cold, "
                     "snowy winters and hot, dry summers. Eastern Turkey can reach -30°C in winter! Turkey "
                     "is also home to beautiful animals: the Van cat (with different-coloured eyes), the "
                     "Kangal dog (the strongest shepherd dog), and the loggerhead sea turtle (caretta caretta) "
                     "on Dalyan beach. The tulip — yes, the tulip! — originally came from Turkey, not Holland."),
            "famous_person": "Cahit Arf — Turkish mathematician; the Arf invariant is named after him worldwide.",
            "activity": "Create a weather forecast for 5 Turkish cities. Use: sunny, cloudy, rainy, snowy, windy.",
            "recipe": {"name": "Salep (Winter Drink)", "steps": ["Heat 2 cups of milk in a pan.",
                        "Add 1 tablespoon of salep powder and 2 tablespoons of sugar.",
                        "Stir continuously for 5 minutes until thick.",
                        "Pour into cups. Sprinkle cinnamon on top.", "Drink it warm on cold days!"]}},
        5: {"title": "Shopping and Money in Turkey",
            "text": ("The Turkish Lira (TL) is Turkey's currency. Turkish people love bazaars — open-air "
                     "markets where you can buy everything from fresh fruit to handmade carpets. The most "
                     "famous bazaar is the Grand Bazaar in Istanbul, but every city has weekly pazars. "
                     "At a pazar, you can practise maths: 'How much are the oranges? 15 TL per kilo, please.' "
                     "Turkish people are famous for bargaining — politely asking for a lower price. 'Is that "
                     "your best price?' is a useful phrase! Modern shopping malls are also popular, but "
                     "traditional bazaars are more exciting. Fun fact: Turkey is the world's largest producer "
                     "of hazelnuts (findik), figs (incir) and apricots (kayisi)!"),
            "famous_person": "Vecihi Hurkus — Turkey's first pilot and aircraft designer (1925).",
            "activity": "Create your own 'dream bazaar'. List 10 items with prices in English.",
            "recipe": {"name": "Turkish Delight (Lokum)", "steps": ["Mix 1 cup sugar and 1 cup water in a pot.",
                        "Boil until the sugar dissolves completely.", "Add 3 tablespoons of cornstarch mixed with water.",
                        "Stir for 20 minutes on low heat until very thick.",
                        "Add a few drops of rose water and food colouring.",
                        "Pour into a tray. Let it cool for 6 hours. Cut into cubes and cover with powdered sugar!"]}},
        6: {"title": "Turkish Food Around the World",
            "text": ("Turkish cuisine is one of the richest in the world! Kebab, baklava, lahmacun and "
                     "doner are now popular everywhere. But did you know Turkish breakfast is considered "
                     "the best in the world? A traditional Turkish breakfast includes cheese (at least 5 types!), "
                     "olives, tomatoes, cucumbers, eggs, honey, butter, jam, sucuk (spicy sausage), simit "
                     "and of course — cay (Turkish tea). Turkish people drink an average of 3.5 kg of tea per "
                     "person per year — the most in the world! Another unique tradition is Turkish coffee "
                     "(Turk kahvesi), which UNESCO added to its cultural heritage list in 2013. After drinking, "
                     "people turn the cup upside down and 'read' the coffee grounds to tell the future!"),
            "famous_person": "Nusret Gokce (Salt Bae) — Turkish chef who became world-famous for his meat-salting style.",
            "activity": "Design a menu for a Turkish restaurant in London. Write descriptions of 5 dishes in English.",
            "recipe": {"name": "Ayran (Traditional Yoghurt Drink)", "steps": ["Put 1 cup of plain yoghurt in a jug.",
                        "Add 1 cup of cold water.", "Add a pinch of salt.",
                        "Mix with a blender or whisk for 1 minute until frothy.",
                        "Pour into glasses with ice. Enjoy!"]}},
        7: {"title": "Turkish Sports Heroes",
            "text": ("Turkey has produced many world-class athletes. In football, the national team reached "
                     "the semi-finals of the 2002 World Cup — their best result ever! In basketball, Turkey "
                     "is a European powerhouse. In wrestling (gures), Turkey is legendary — oil wrestling "
                     "(yagli gures) in Edirne is the oldest sporting event in the world, held since 1362! "
                     "Wrestlers cover themselves in olive oil and compete on grass. Naim Suleymanoglu, known "
                     "as 'Pocket Hercules', won three Olympic gold medals in weightlifting. He could lift "
                     "three times his own body weight! In recent years, Turkish athletes have won medals in "
                     "archery, taekwondo and para-athletics, making the whole country proud."),
            "famous_person": "Naim Suleymanoglu — three-time Olympic champion, 'Pocket Hercules' of weightlifting.",
            "activity": "Write a sports biography. Choose a Turkish or international athlete. Include: born, grew up, started, won, is famous for.",
            "recipe": None},
        8: {"title": "Turkish Holidays and Celebrations",
            "text": ("Turkey celebrates many special days throughout the year. April 23rd is National Sovereignty "
                     "and Children's Day — the only national holiday in the world dedicated to children! On this "
                     "day, children 'take over' parliament and city halls. October 29th is Republic Day, "
                     "celebrating the founding of the Turkish Republic in 1923 by Mustafa Kemal Ataturk. "
                     "Bayram celebrations are very important: Ramazan Bayrami (after the fasting month) lasts "
                     "3 days, and Kurban Bayrami lasts 4 days. During bayram, families visit each other, "
                     "children kiss elders' hands, and everyone eats special sweets and meals together. "
                     "Hidirellez (May 6th) celebrates the arrival of spring — people write wishes on paper and "
                     "throw them into water or tie them to rose bushes!"),
            "famous_person": "Mustafa Kemal Ataturk — founder of the Turkish Republic, who said: 'Peace at home, peace in the world.'",
            "activity": "Write an invitation for a bayram celebration in English. Include: date, time, place, activities, dress code.",
            "recipe": {"name": "Bayram Cookies (Kurabiye)", "steps": ["Mix 250g butter with 1 cup sugar.",
                        "Add 2 eggs and mix well.", "Add 4 cups of flour and 1 teaspoon vanilla.",
                        "Knead into a soft dough. Shape into small rounds or crescents.",
                        "Place on a baking tray. Bake at 180°C for 15 minutes.",
                        "Sprinkle with powdered sugar when cool. Share with neighbours!"]}},
        9: {"title": "Turkish Art and Music",
            "text": ("Turkey has a rich artistic heritage. Ebru (marbling art) creates beautiful patterns by "
                     "floating paint on water — UNESCO recognized it as cultural heritage in 2014. Turkish "
                     "miniature painting, ceramic tiles from Iznik, and calligraphy are world-famous traditional "
                     "arts. In music, Turkey has everything: classical Ottoman music, folk songs (turku) from "
                     "different regions, arabesk, pop and rock. The saz (baglama) is the most popular traditional "
                     "instrument. Baris Manco and Cem Karaca are legendary rock musicians who mixed Turkish folk "
                     "with Western rock in the 1970s. Today, Turkish TV series (dizi) are watched in over 150 "
                     "countries — making Turkish culture known worldwide!"),
            "famous_person": "Ara Guler — world-famous Turkish photographer, called 'The Eye of Istanbul' by Time magazine.",
            "activity": "Design a poster for a Turkish arts festival. Write the programme in English: what, where, when.",
            "recipe": None},
        10: {"title": "Turkey and the World",
             "text": ("Turkey is a unique country connecting two continents. Istanbul is the only city in the "
                      "world that sits on both Europe and Asia! The Bosphorus Bridge connects the two sides. "
                      "Turkey is a member of NATO, G20 and many international organisations. Turkish Airlines "
                      "flies to more countries than any other airline in the world — over 120 countries! "
                      "Turkey hosts millions of international students and refugees, showing great hospitality "
                      "(misafirperverlik) — a core Turkish value. The Turkish word 'yoghurt' is used in English, "
                      "French, and many other languages. Other Turkish words in English include: kiosk (kosk), "
                      "tulip (tulbend) and sherbet (serbet). Turkey truly connects the East and the West!"),
             "famous_person": "Orhan Pamuk — Nobel Prize-winning Turkish novelist, author of 'My Name Is Red'.",
             "activity": "Write a letter to a pen pal in another country. Describe Turkey and invite them to visit.",
             "recipe": {"name": "Turkish Lemonade (Limonata)", "steps": ["Squeeze 4 lemons into a jug.",
                         "Add 1 litre of cold water and 4 tablespoons of sugar.",
                         "Add fresh mint leaves.", "Stir well and add ice cubes.",
                         "Pour into glasses. Best on a hot summer day!"]}},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# COMIC STRIP DATA — Grade 5 (grammar through comics)
# ══════════════════════════════════════════════════════════════════════════════

_COMIC_STRIP_BANK = {
    5: {
        1: {"title": "Elif's Morning Routine",
            "grammar_point": "Present Simple — Daily Routines",
            "panels": [
                {"scene": "Elif in bed, alarm ringing (07:00)", "speech": "Elif: I wake up at seven o'clock EVERY DAY.", "thought": None},
                {"scene": "Elif brushing teeth", "speech": "Elif: I always brush my teeth first.", "thought": "Narrator: always = her rutün"},
                {"scene": "Elif running to catch bus", "speech": "Can: She RUNS to school every morning!", "thought": None},
                {"scene": "Elif arriving late, teacher smiling", "speech": "Ms. Yildiz: Elif, you always come late! Class STARTS at 8:30.", "thought": "Elif (thinking): I need a new alarm clock!"},
            ],
            "your_turn": "Draw 4 panels showing YOUR morning routine. Use Present Simple."},
        2: {"title": "Can's Family Photo",
            "grammar_point": "Have/Has — Describing People",
            "panels": [
                {"scene": "Can holding a big family photo", "speech": "Can: This is my family! I HAVE a big family.", "thought": None},
                {"scene": "Pointing to dad", "speech": "Can: My dad HAS short black hair. He IS very tall.", "thought": None},
                {"scene": "Pointing to mum", "speech": "Can: My mum HAS long brown hair. She IS very kind.", "thought": None},
                {"scene": "Boncuk jumping into the photo", "speech": "Sude: And Boncuk HAS golden fur and a WET nose! Can: He IS part of the family too!", "thought": "Boncuk (thinking): I am the BEST member!"},
            ],
            "your_turn": "Draw your family and write descriptions using HAVE/HAS and IS/ARE."},
        3: {"title": "Lost in the Neighbourhood",
            "grammar_point": "There is/There are — Prepositions of Place",
            "panels": [
                {"scene": "Tourist looking confused at a crossroads", "speech": "Tourist: Excuse me! IS THERE a pharmacy near here?", "thought": None},
                {"scene": "Elif pointing left", "speech": "Elif: Yes! There IS a pharmacy NEXT TO the bakery.", "thought": None},
                {"scene": "Tourist still confused", "speech": "Tourist: And ARE THERE any restaurants?", "thought": None},
                {"scene": "Can pointing in multiple directions", "speech": "Can: There ARE three restaurants! One is BETWEEN the bank and the park. Sude: And there is a GREAT one OPPOSITE the mosque!", "thought": "Tourist (thinking): Turkish people are so helpful!"},
            ],
            "your_turn": "Draw a simple map. Write 5 sentences with THERE IS/ARE + prepositions."},
        4: {"title": "The Weather Report",
            "grammar_point": "Present Continuous + Weather",
            "panels": [
                {"scene": "TV studio, Sude as weather presenter", "speech": "Sude: Good morning! I AM PRESENTING the weather today!", "thought": None},
                {"scene": "Map showing rain in Istanbul", "speech": "Sude: It IS RAINING in Istanbul right now. People ARE CARRYING umbrellas.", "thought": None},
                {"scene": "Map showing sun in Antalya", "speech": "Sude: In Antalya, the sun IS SHINING! Tourists ARE SWIMMING in the sea.", "thought": None},
                {"scene": "Snow on the map, Can throwing snowball", "speech": "Sude: And in Erzurum, it IS SNOWING! Can: I AM MAKING a snowball! Watch out, Elif!", "thought": "Elif (thinking): I AM NOT going outside!"},
            ],
            "your_turn": "Be a weather presenter! Draw and describe today's weather using Present Continuous."},
        5: {"title": "At the Grand Bazaar",
            "grammar_point": "How much/How many — Can/Can't",
            "panels": [
                {"scene": "Children at a colourful market stall", "speech": "Elif: HOW MUCH is this scarf?", "thought": None},
                {"scene": "Seller showing price", "speech": "Seller: 50 TL. Elif: CAN I have a discount?", "thought": None},
                {"scene": "Can counting his money", "speech": "Can: HOW MANY liras do we have? Sude: We have 80 TL.", "thought": None},
                {"scene": "Everyone happy with shopping bags", "speech": "Seller: OK, 40 TL for you! Can: CAN we buy two? Seller: Of course you CAN!", "thought": "Boncuk (thinking): CAN I have a bone?"},
            ],
            "your_turn": "Draw a shop scene. Write a dialogue using HOW MUCH/MANY and CAN/CAN'T."},
        6: {"title": "Cooking Show Disaster",
            "grammar_point": "Countable/Uncountable — some/any",
            "panels": [
                {"scene": "Kitchen, Elif wearing a chef hat", "speech": "Elif: Today we are making menemen! We need SOME tomatoes and SOME peppers.", "thought": None},
                {"scene": "Can looking in empty fridge", "speech": "Can: We don't have ANY eggs! Is there ANY cheese?", "thought": None},
                {"scene": "Boncuk eating something", "speech": "Sude: There was SOME bread on the table... Where is it?", "thought": None},
                {"scene": "Boncuk licking lips, everyone laughing", "speech": "Can: Boncuk! You ate ALL the bread! Elif: We don't have ANY food left! Sude: Let's order pizza!", "thought": "Boncuk (thinking): It was SOME delicious bread!"},
            ],
            "your_turn": "Draw a cooking scene. Use SOME and ANY with countable and uncountable nouns."},
        7: {"title": "The Time Machine",
            "grammar_point": "Past Simple — Regular and Irregular",
            "panels": [
                {"scene": "A cardboard time machine in the classroom", "speech": "Can: I FOUND a time machine! Yesterday I WENT to 1923!", "thought": None},
                {"scene": "Old-timey scene", "speech": "Can: I SAW Ataturk! He SPOKE to the people. Everyone CHEERED!", "thought": None},
                {"scene": "Can back in class, excited", "speech": "Elif: DID you really go? Can: Yes! I WALKED in old Istanbul and ATE Ottoman food!", "thought": None},
                {"scene": "Ms. Yildiz smiling knowingly", "speech": "Ms. Yildiz: Can, you DIDN'T go anywhere. You FELL ASLEEP during the history film! The class LAUGHED.", "thought": "Can (thinking): But it FELT so real!"},
            ],
            "your_turn": "Draw a time travel adventure. Where did you go? What did you see? Use Past Simple."},
        8: {"title": "Summer Plans",
            "grammar_point": "Going to — Future Plans",
            "panels": [
                {"scene": "Calendar showing 'SUMMER' circled", "speech": "Elif: What ARE you GOING TO do this summer?", "thought": None},
                {"scene": "Can with surfboard", "speech": "Can: I AM GOING TO learn surfing in Alacati!", "thought": None},
                {"scene": "Sude with paintbrush", "speech": "Sude: I AM GOING TO paint in Cappadocia! I'm NOT GOING TO use a phone for a week!", "thought": None},
                {"scene": "Boncuk with suitcase", "speech": "Elif: We ARE GOING TO have the best summer ever! Boncuk IS GOING TO come too!", "thought": "Boncuk (thinking): I AM GOING TO eat SO many treats!"},
            ],
            "your_turn": "Draw your summer plans in 4 panels. Use GOING TO for future."},
        9: {"title": "The School Rules",
            "grammar_point": "Should/Must/Have to — Giving Advice",
            "panels": [
                {"scene": "New student looking confused", "speech": "New student: What SHOULD I do on my first day?", "thought": None},
                {"scene": "Elif explaining", "speech": "Elif: You MUST wear a uniform. You SHOULD be friendly!", "thought": None},
                {"scene": "Can at cafeteria", "speech": "Can: You SHOULDN'T run in the corridors. You HAVE TO eat in the cafeteria.", "thought": None},
                {"scene": "Everyone together, smiling", "speech": "Sude: You DON'T HAVE TO worry! We will help you! New student: I SHOULD have come here earlier!", "thought": "Boncuk (thinking): You MUST give me treats. That's the most important rule!"},
            ],
            "your_turn": "Write 6 school rules using MUST, SHOULD, HAVE TO."},
        10: {"title": "The Last Day",
             "grammar_point": "Review — All Tenses",
             "panels": [
                 {"scene": "Last day of school, everyone sad but smiling", "speech": "Elif: This year WAS amazing! We LEARNED so much!", "thought": None},
                 {"scene": "Looking at photos", "speech": "Can: We FOUND a treasure! We VISITED many places! We MADE new friends!", "thought": None},
                 {"scene": "Ms. Yildiz giving certificates", "speech": "Ms. Yildiz: You HAVE BEEN wonderful students. I AM so proud!", "thought": None},
                 {"scene": "Walking out together, sunset", "speech": "Sude: Next year IS GOING TO be even better! Elif: We WILL always be friends! Can: See you in Grade 6!", "thought": "Boncuk (thinking): I WILL miss the school lunches!"},
             ],
             "your_turn": "Draw YOUR year. Past, present and future in 4 panels. Use different tenses!"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# GAMIFICATION — Grade 5 (XP, badges, levels per unit)
# ══════════════════════════════════════════════════════════════════════════════

_GAMIFICATION_BANK = {
    5: {
        "levels": [
            {"name": "Bronze Explorer", "xp_min": 0, "xp_max": 99, "icon": "bronze"},
            {"name": "Silver Learner", "xp_min": 100, "xp_max": 249, "icon": "silver"},
            {"name": "Gold Achiever", "xp_min": 250, "xp_max": 449, "icon": "gold"},
            {"name": "Diamond Master", "xp_min": 450, "xp_max": 999, "icon": "diamond"},
        ],
        "unit_badges": {
            1: {"badge": "Schedule Star", "desc": "Complete all vocabulary and grammar exercises", "xp": 50},
            2: {"badge": "Description Detective", "desc": "Write a perfect family description", "xp": 50},
            3: {"badge": "Navigator", "desc": "Give directions to 3 places", "xp": 50},
            4: {"badge": "Weather Wizard", "desc": "Create a 5-city weather forecast", "xp": 50},
            5: {"badge": "Market Master", "desc": "Complete a shopping dialogue", "xp": 50},
            6: {"badge": "Chef Champion", "desc": "Write a recipe in English", "xp": 50},
            7: {"badge": "Time Traveller", "desc": "Write a story in Past Simple", "xp": 50},
            8: {"badge": "Future Planner", "desc": "Plan a holiday using going to", "xp": 50},
            9: {"badge": "Rule Maker", "desc": "Create a classroom rules poster", "xp": 50},
            10: {"badge": "English Champion", "desc": "Complete the whole book!", "xp": 100},
        },
        "bonus_xp": [
            {"action": "Perfect score on Progress Check", "xp": 30},
            {"action": "Complete a Real-World Mission", "xp": 25},
            {"action": "Escape Room solved", "xp": 40},
            {"action": "Family Corner signed by parent", "xp": 15},
            {"action": "Tongue Twister said 3 times fast", "xp": 10},
            {"action": "Comic Strip drawn", "xp": 20},
            {"action": "Project completed and presented", "xp": 35},
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# REAL-WORLD MISSIONS — Grade 5
# ══════════════════════════════════════════════════════════════════════════════

_MISSION_BANK = {
    5: {
        1: {"title": "My School Reporter",
            "mission": "Walk around your school. Find 10 signs or labels in English. Take photos or draw them. Write what each one means.",
            "evidence": "Photo collage or drawings with English labels and Turkish meanings.",
            "xp": 25, "difficulty": "Easy"},
        2: {"title": "Family Interview",
            "mission": "Interview a family member in English. Ask: What is your name? How old are you? What do you look like? What is your favourite food? Record or write the answers.",
            "evidence": "Written interview (at least 8 questions and answers) or audio recording.",
            "xp": 25, "difficulty": "Easy"},
        3: {"title": "Neighbourhood Explorer",
            "mission": "Draw a map of your neighbourhood. Label at least 8 places in English (school, mosque, park, bakery...). Write directions from your home to school.",
            "evidence": "Hand-drawn map with English labels and written directions.",
            "xp": 25, "difficulty": "Medium"},
        4: {"title": "Weather Diary",
            "mission": "Keep a weather diary for 7 days. Every day, write the date, temperature, weather and what you wore. Draw a small picture for each day.",
            "evidence": "7-day weather diary with drawings and descriptions.",
            "xp": 25, "difficulty": "Easy"},
        5: {"title": "Market Spy",
            "mission": "Go to a supermarket or pazar. Find 15 products with English words on them. Write the product name, the English words and the price.",
            "evidence": "List of 15 products with English labels and prices.",
            "xp": 25, "difficulty": "Medium"},
        6: {"title": "Recipe Challenge",
            "mission": "Ask a family member for a recipe. Write it in English: ingredients (with amounts) and steps. Bonus: Cook it together and take a photo!",
            "evidence": "Written recipe in English. Bonus: photo of the cooked dish.",
            "xp": 30, "difficulty": "Medium"},
        7: {"title": "History Detective",
            "mission": "Ask your grandparents: What did you do when you were 10? Write their story in Past Simple (at least 10 sentences). Compare with YOUR life.",
            "evidence": "Written story in past tense + comparison.",
            "xp": 25, "difficulty": "Medium"},
        8: {"title": "Dream Holiday Planner",
            "mission": "Plan a 3-day holiday. Choose a city. Write what you are going to do each day (morning, afternoon, evening). Include costs!",
            "evidence": "3-day plan with activities, times and budget.",
            "xp": 25, "difficulty": "Medium"},
        9: {"title": "Advice Column",
            "mission": "Write an advice column for your school newspaper. Choose 3 problems (e.g., 'I can't wake up early'). Give advice using should/must/have to.",
            "evidence": "3 problems with advice, written like a newspaper column.",
            "xp": 30, "difficulty": "Hard"},
        10: {"title": "English Day Organiser",
             "mission": "Plan an 'English Day' for your class. Write the programme: activities, games, songs, food. Present it to your teacher!",
             "evidence": "Full programme with timeline, activities and materials list.",
             "xp": 35, "difficulty": "Hard"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# ESCAPE ROOM — Grade 5 (after units 3, 6, 9)
# ══════════════════════════════════════════════════════════════════════════════

_ESCAPE_ROOM_BANK = {
    5: {
        1: {"title": "Escape from the Timetable Trap!",
            "story": "The school bell is broken and all the clocks show different times! Solve 5 puzzles to fix the master clock and escape!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: Y-A-D-N-O-M = ?", "answer": "MONDAY",
                 "hint": "The first school day of the week."},
                {"type": "grammar", "question": "Fill in: 'I _____ (have) English on Tuesdays.' (Simple Present)", "answer": "have",
                 "hint": "Use the base form for I/you/we/they."},
                {"type": "reading", "question": "Clue on the whiteboard: 'This lesson uses numbers and shapes. It comes after break.' What subject?",
                 "answer": "MATHS", "hint": "2 + 2 = 4"},
                {"type": "maths", "question": "School starts at 08:30. Each lesson is 40 minutes. Break is 10 min. What time does the 3rd lesson end?",
                 "answer": "10:40", "hint": "08:30 + 40 + 10 + 40 + 10 + 40"},
                {"type": "riddle", "question": "I ring but I am not a phone. I tell you when to go but I have no mouth. What am I?",
                 "answer": "BELL", "hint": "Ding ding!"},
            ],
            "final_code": "MONDAY-have-MATHS-10:40-BELL",
            "reward": "Clock fixed! +40 XP! Badge: Timetable Wizard"},
        2: {"title": "Escape from the Portrait Gallery!",
            "story": "You are trapped in a gallery of family portraits. Each painting hides a puzzle. Solve all 5 to open the exit!",
            "puzzles": [
                {"type": "vocabulary", "question": "Who is your mother's mother? _ _ _ _ _ _ _ _ _ _ _", "answer": "GRANDMOTHER",
                 "hint": "Grand + mother"},
                {"type": "grammar", "question": "Correct: 'She have got blue eyes and long hair.'", "answer": "She has got blue eyes and long hair.",
                 "hint": "She/he/it = HAS got"},
                {"type": "reading", "question": "Portrait caption: 'I am tall. I have a moustache. I wear glasses. I am your father's brother.' Who am I?",
                 "answer": "UNCLE", "hint": "Your dad's brother"},
                {"type": "maths", "question": "A family has 2 parents, 3 children and 4 grandparents. How many people in total?",
                 "answer": "9", "hint": "2 + 3 + 4"},
                {"type": "riddle", "question": "I am in your family but I am also you. When you look in the mirror, who do you see?",
                 "answer": "YOURSELF", "hint": "Look in the mirror!"},
            ],
            "final_code": "GRANDMOTHER-has-UNCLE-9-YOURSELF",
            "reward": "Gallery escaped! +40 XP! Badge: Family Detective"},
        3: {"title": "Escape from the Library!",
            "story": "Oh no! The library door has locked automatically. You have 20 minutes to solve 5 puzzles to find the exit code!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble: O-O-H-S-L-C = ?", "answer": "SCHOOL",
                 "hint": "You go here every day."},
                {"type": "grammar", "question": "Fill in: 'There _____ a book on the table.' (is/are)", "answer": "is",
                 "hint": "One book = singular."},
                {"type": "reading", "question": "Read the clue on the wall: 'I am between the bank and the post office. I sell medicine.' What am I?",
                 "answer": "PHARMACY", "hint": "People buy medicine here."},
                {"type": "maths", "question": "The code is: (number of days in a week) x (number of seasons) = ?",
                 "answer": "28", "hint": "7 x 4"},
                {"type": "riddle", "question": "I have hands but I can't clap. I have a face but I can't smile. What am I?",
                 "answer": "CLOCK", "hint": "Tick tock!"},
            ],
            "final_code": "SCHOOL-is-PHARMACY-28-CLOCK",
            "reward": "You escaped! +40 XP! Badge: Library Escape Artist"},
        6: {"title": "The Cafeteria Caper!",
            "story": "Someone has taken all the food from the cafeteria! Solve 5 clues to find out who did it and unlock the kitchen!",
            "puzzles": [
                {"type": "vocabulary", "question": "Put in order: expensive → cheap. 100 TL, 15 TL, 50 TL, 5 TL", "answer": "100, 50, 15, 5",
                 "hint": "Biggest number first."},
                {"type": "grammar", "question": "Correct the sentence: 'She don't like some milk.'", "answer": "She doesn't like any milk.",
                 "hint": "Negative = any, not some. Don't → doesn't for she."},
                {"type": "listening", "question": "The suspect said: 'I always eat lunch at twelve o'clock.' What time? Write in numbers.",
                 "answer": "12:00", "hint": "Twelve = 12"},
                {"type": "maths", "question": "The thief bought: 3 kg apples (10 TL/kg) + 2 loaves (8 TL each). Total?",
                 "answer": "46 TL", "hint": "30 + 16 = ?"},
                {"type": "riddle", "question": "I am golden on the outside, soft on the inside. You eat me for breakfast with tea. What am I?",
                 "answer": "SIMIT", "hint": "A ring-shaped Turkish bread."},
            ],
            "final_code": "100-doesn't-12:00-46-SIMIT",
            "reward": "Mystery solved! It was Boncuk! +40 XP! Badge: Cafeteria Detective"},
        4: {"title": "The Weather Station Lockdown!",
            "story": "A storm has knocked out the school weather station! Solve 5 puzzles to restore the forecast system!",
            "puzzles": [
                {"type": "vocabulary", "question": "Match: sunny=☀, rainy=🌧, snowy=❄, cloudy=☁, windy=🌬. What is left? T _ _ _ _ _ _ _ _ _ _ _",
                 "answer": "THUNDERSTORM", "hint": "Lightning + rain + loud noise"},
                {"type": "grammar", "question": "Fill in: 'It _____ (rain) right now. Look outside!' (Present Continuous)", "answer": "is raining",
                 "hint": "am/is/are + verb-ing"},
                {"type": "reading", "question": "Forecast says: 'Wear a thick coat, gloves and a hat. Temperature: -5°C.' What season?",
                 "answer": "WINTER", "hint": "Brrr! Very cold!"},
                {"type": "maths", "question": "Monday: 20°C, Tuesday: 18°C, Wednesday: 22°C, Thursday: 16°C, Friday: 24°C. What is the average?",
                 "answer": "20", "hint": "Add all, divide by 5: 100 ÷ 5"},
                {"type": "riddle", "question": "I fall from the sky but I am not rain. I am white and cold. Children love to play with me. What am I?",
                 "answer": "SNOW", "hint": "Build a snowman!"},
            ],
            "final_code": "THUNDERSTORM-is raining-WINTER-20-SNOW",
            "reward": "Weather station restored! +40 XP! Badge: Storm Chaser"},
        5: {"title": "The Market Maze!",
            "story": "You are lost in the Grand Bazaar! Every stall has a puzzle. Solve 5 to find your way out!",
            "puzzles": [
                {"type": "vocabulary", "question": "Put in order from cheapest to most expensive: diamond ring, pencil, bicycle, sandwich",
                 "answer": "pencil, sandwich, bicycle, diamond ring", "hint": "Think about real prices."},
                {"type": "grammar", "question": "Choose: 'Can I have _____ (some/any) apples, please?'", "answer": "some",
                 "hint": "Use SOME in polite requests."},
                {"type": "reading", "question": "Sign says: 'Buy 2, get 1 free! Apples: 10 TL each.' You buy 3. How much do you pay?",
                 "answer": "20 TL", "hint": "You pay for 2, the 3rd is free."},
                {"type": "maths", "question": "You have 100 TL. Bread: 15 TL, Cheese: 35 TL, Olives: 20 TL. How much change?",
                 "answer": "30 TL", "hint": "100 - 15 - 35 - 20"},
                {"type": "riddle", "question": "I have a head and a tail but no body. You can flip me. What am I?",
                 "answer": "COIN", "hint": "You use me to pay!"},
            ],
            "final_code": "pencil-some-20-30-COIN",
            "reward": "Bazaar escaped! +40 XP! Badge: Market Navigator"},
        7: {"title": "The Time Machine Malfunction!",
            "story": "You accidentally activated a time machine in the history room! Solve 5 puzzles to return to the present!",
            "puzzles": [
                {"type": "vocabulary", "question": "Past time words: y _ _ _ _ _ _ _ _ (the day before today)", "answer": "YESTERDAY",
                 "hint": "Today - 1 day"},
                {"type": "grammar", "question": "Change to Past Simple: 'I go to school. I see my friends. I eat lunch.'",
                 "answer": "I went to school. I saw my friends. I ate lunch.", "hint": "go→went, see→saw, eat→ate"},
                {"type": "reading", "question": "Diary entry: 'Dear Diary, today I visited Topkapi Palace. I saw the sultan's jewels.' When was this written?",
                 "answer": "IN THE PAST", "hint": "visited, saw = Past Simple"},
                {"type": "maths", "question": "The Republic of Turkey was founded in 1923. How many years ago is that from 2026?",
                 "answer": "103", "hint": "2026 - 1923"},
                {"type": "riddle", "question": "I go forward but never backward. You cannot stop me or catch me. What am I?",
                 "answer": "TIME", "hint": "Tick tock, tick tock..."},
            ],
            "final_code": "YESTERDAY-went-PAST-103-TIME",
            "reward": "Back to the present! +40 XP! Badge: Time Traveller"},
        8: {"title": "The Holiday Planner Panic!",
            "story": "Your holiday booking website crashed! Solve 5 puzzles to recover the data and save your vacation!",
            "puzzles": [
                {"type": "vocabulary", "question": "Unscramble these holiday items: TSUCEASI = ?", "answer": "SUITCASE",
                 "hint": "You pack your clothes in it."},
                {"type": "grammar", "question": "Fill in with 'going to': 'We _____ (visit) Antalya next summer.'",
                 "answer": "are going to visit", "hint": "We + are going to + base verb"},
                {"type": "reading", "question": "Brochure: 'Beautiful beaches, ancient ruins, delicious seafood. Average temp: 35°C.' Where in Turkey?",
                 "answer": "ANTALYA", "hint": "Mediterranean coast, very popular for tourism"},
                {"type": "maths", "question": "Flight: 500 TL per person. Hotel: 300 TL per night for 5 nights. Family of 4. Total cost?",
                 "answer": "3500 TL", "hint": "Flights: 4 x 500 = 2000. Hotel: 300 x 5 = 1500. Total: 2000 + 1500"},
                {"type": "riddle", "question": "I carry people through the sky. I have wings but I am not a bird. What am I?",
                 "answer": "AEROPLANE", "hint": "You board me at the airport."},
            ],
            "final_code": "SUITCASE-going to-ANTALYA-3500-AEROPLANE",
            "reward": "Holiday saved! +40 XP! Badge: Travel Agent"},
        9: {"title": "The Principal's Office Mystery!",
            "story": "The principal's computer is locked! He forgot the password. Solve 5 English puzzles to help him log in!",
            "puzzles": [
                {"type": "vocabulary", "question": "Synonyms: happy = j_____, big = l_____, fast = q_____", "answer": "joyful, large, quick",
                 "hint": "Think of other words with the same meaning."},
                {"type": "grammar", "question": "Past Simple: go → ?, see → ?, eat → ?", "answer": "went, saw, ate",
                 "hint": "Irregular verbs!"},
                {"type": "reading", "question": "The note says: 'You should look under the thing you sit on.' Where?",
                 "answer": "CHAIR", "hint": "You sit on it."},
                {"type": "maths", "question": "Password digit: Number of months that start with J (in English) = ?",
                 "answer": "3", "hint": "January, June, July"},
                {"type": "riddle", "question": "I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?",
                 "answer": "KEYBOARD", "hint": "You use it to type."},
            ],
            "final_code": "joyful-went-CHAIR-3-KEYBOARD",
            "reward": "Computer unlocked! +40 XP! Badge: Code Breaker"},
        10: {"title": "The Grand English Finale!",
             "story": "It is the last day of school and the trophy cabinet is locked! Solve 5 final puzzles to unlock it and claim your English Champion trophy!",
             "puzzles": [
                 {"type": "vocabulary", "question": "Find the odd one out: happy, joyful, sad, cheerful, glad", "answer": "SAD",
                  "hint": "All others mean happy!"},
                 {"type": "grammar", "question": "Which is correct? a) 'I have went to school.' b) 'I have gone to school.'",
                  "answer": "b", "hint": "have/has + past participle (gone, not went)"},
                 {"type": "reading", "question": "Certificate says: 'This student has completed all units, passed all tests, and earned 10 badges.' How many badges?",
                  "answer": "10", "hint": "Read carefully!"},
                 {"type": "maths", "question": "You earned these XP: Unit 1-5: 50 each. Unit 6-9: 40 each. Unit 10: 100. Total XP?",
                  "answer": "510", "hint": "(5 x 50) + (4 x 40) + 100"},
                 {"type": "riddle", "question": "I have pages but I am not a website. I have a spine but I am not a person. I teach you without speaking. What am I?",
                  "answer": "BOOK", "hint": "You read me!"},
             ],
             "final_code": "SAD-b-10-510-BOOK",
             "reward": "Trophy unlocked! +100 XP! Badge: ENGLISH CHAMPION! Congratulations!"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# FAMILY CORNER — Grade 5 (home activities with parents)
# ══════════════════════════════════════════════════════════════════════════════

_FAMILY_CORNER_BANK = {
    5: {
        1: {"title": "Family Timetable",
            "activity": "Make a weekly timetable for your whole family. Who does what and when? Write it in English.",
            "together": "Read your timetable to your family. They guess if it is TRUE or FALSE!",
            "parent_question": "Dear parent, please ask your child: 'What time do you wake up?' in English.",
            "signature": True},
        2: {"title": "Family Photo Album",
            "activity": "Choose 5 family photos. Write a caption for each one in English: who, where, when, what.",
            "together": "Show the photos to your family and read the captions aloud. Can they add more details?",
            "parent_question": "Dear parent, ask your child to describe YOU in English (5 sentences).",
            "signature": True},
        3: {"title": "Home Address in English",
            "activity": "Write your full home address in English. Then write directions from your home to the nearest park.",
            "together": "Walk the route with a family member. Give directions in English as you walk!",
            "parent_question": "Dear parent, ask: 'Where is the nearest pharmacy?' and let your child answer in English.",
            "signature": True},
        4: {"title": "Weather Watchers",
            "activity": "Watch the weather forecast on TV with your family. Write tomorrow's weather in English.",
            "together": "Every morning for a week, tell your family the weather in English before going to school.",
            "parent_question": "Dear parent, ask every morning: 'What is the weather like today?'",
            "signature": True},
        5: {"title": "Shopping List",
            "activity": "Write the weekly shopping list in English. Include quantities and prices if you can.",
            "together": "Go shopping with a family member. Try to say 5 items in English at the shop.",
            "parent_question": "Dear parent, ask: 'How much is the bread?' and let your child answer in English.",
            "signature": True},
        6: {"title": "Cook Together",
            "activity": "Choose a simple recipe. Write the ingredients and steps in English. Cook it with your family!",
            "together": "While cooking, say each step in English: 'First, we chop the onions. Then, we add oil.'",
            "parent_question": "Dear parent, ask: 'What are we cooking today?' Let your child explain in English.",
            "signature": True},
        7: {"title": "Grandparent Stories",
            "activity": "Ask a grandparent about their childhood. Write 5 sentences in Past Simple.",
            "together": "Read the story to your family at dinner. Ask everyone: 'What did YOU do when you were 10?'",
            "parent_question": "Dear parent, tell your child one memory from YOUR childhood. They will write it in English.",
            "signature": True},
        8: {"title": "Holiday Planning",
            "activity": "Plan a dream family holiday together. Where are you going to go? What are you going to do?",
            "together": "Present the plan to your family in English. Vote on the best destination!",
            "parent_question": "Dear parent, ask: 'Where are we going to go this summer?' Practice 'going to' together.",
            "signature": True},
        9: {"title": "House Rules",
            "activity": "Write 10 house rules in English using should/must/have to. Be creative!",
            "together": "Read the rules to your family. They decide: AGREE or DISAGREE with each rule.",
            "parent_question": "Dear parent, add YOUR own rule in English. Your child will help you say it correctly.",
            "signature": True},
        10: {"title": "English Celebration",
             "activity": "Write a THANK YOU letter to your family in English for supporting you all year.",
             "together": "Read the letter at a family dinner. Celebrate your English progress!",
             "parent_question": "Dear parent, tell your child ONE thing you are proud of about their English this year.",
             "signature": True},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# SEL (Social-Emotional Learning) — Grade 5
# ══════════════════════════════════════════════════════════════════════════════

_SEL_BANK = {
    5: {
        1: {"emotion": "Excited / Nervous",
            "prompt": "It is the first day of school. How do you feel? Circle: EXCITED / NERVOUS / HAPPY / SCARED",
            "activity": "Write 3 sentences: I feel _____ because _____.",
            "mindfulness": "Close your eyes. Take 3 deep breaths. Think of one good thing about today. Open your eyes and smile.",
            "discussion": "Talk to a partner: What makes you nervous about school? What makes you excited?"},
        2: {"emotion": "Love / Gratitude",
            "prompt": "Think about your family. Who makes you feel safe? Who makes you laugh?",
            "activity": "Write a 'Thank You Card' in English to someone in your family. Use at least 5 sentences.",
            "mindfulness": "Close your eyes. Picture your family around you. Feel the warmth. Send them a silent 'thank you'.",
            "discussion": "Share with a partner: What is the best thing about your family?"},
        3: {"emotion": "Helpful / Kind",
            "prompt": "Have you ever helped a stranger? Have you ever asked for help?",
            "activity": "Write about a time you helped someone OR someone helped you. What happened? How did you feel?",
            "mindfulness": "Think of one kind thing you can do today. It can be small: hold a door, share a pencil, say something nice.",
            "discussion": "Discuss: Why is it important to help people in our neighbourhood?"},
        4: {"emotion": "Calm / Worried",
            "prompt": "What do you do when the weather is bad and you cannot go outside?",
            "activity": "Write 5 things that make you feel CALM. Then write 5 things that make you WORRIED. Compare with a friend.",
            "mindfulness": "Imagine you are sitting by a warm fire on a rainy day. You have hot chocolate. Everything is peaceful.",
            "discussion": "How does weather affect your mood? Do you feel happier on sunny days?"},
        5: {"emotion": "Confident / Unsure",
            "prompt": "When you go shopping alone for the first time, how do you feel?",
            "activity": "Write about your first time doing something alone: shopping, cooking, riding a bus. Use: I felt _____.",
            "mindfulness": "Stand tall. Put your hands on your hips like a superhero. Say: 'I CAN do this!' three times.",
            "discussion": "When do you feel most confident? When do you feel unsure? How can you build confidence?"},
        6: {"emotion": "Sharing / Generous",
            "prompt": "Do you like sharing food? What is the best meal you have ever shared with friends?",
            "activity": "Imagine you have 100 TL. You MUST spend it on OTHER PEOPLE. Write what you would buy and for whom.",
            "mindfulness": "Think of something you have that you could share with someone who needs it. How would they feel?",
            "discussion": "Why does sharing make us feel good? Is it easy or hard to share?"},
        7: {"emotion": "Nostalgic / Proud",
            "prompt": "What is your favourite memory from the past? Why is it special?",
            "activity": "Write about your BEST DAY EVER. Use Past Simple. Where did you go? Who were you with? What did you do?",
            "mindfulness": "Close your eyes. Go back to that happy memory. See the colours, hear the sounds, feel the feelings.",
            "discussion": "Share your best memory with a partner. Ask questions about THEIR memory."},
        8: {"emotion": "Hopeful / Dreamy",
            "prompt": "What do you dream about for the future? What kind of person do you want to be?",
            "activity": "Write a letter to your FUTURE SELF (age 18). What are you going to do? What do you hope for?",
            "mindfulness": "Imagine yourself at 18. You are happy and successful. What did you do to get there? Smile at your future self.",
            "discussion": "What is the difference between a DREAM and a PLAN? How do you turn dreams into plans?"},
        9: {"emotion": "Responsible / Fair",
            "prompt": "What rules are important for a fair classroom? Why do we need rules?",
            "activity": "Write a 'Kindness Contract': 5 promises you make to your classmates (I will..., I won't...).",
            "mindfulness": "Think of a time someone was unfair to you. Now think of a time YOU were unfair. How can we be more fair?",
            "discussion": "Is it easy to follow rules? What happens when there are no rules?"},
        10: {"emotion": "Grateful / Connected",
             "prompt": "The school year is ending. What are you most grateful for?",
             "activity": "Write 3 thank-you messages: one to a TEACHER, one to a FRIEND, one to YOURSELF.",
             "mindfulness": "Put your hand on your heart. Think of 5 things you are grateful for this year. Breathe and smile.",
             "discussion": "How have you changed this year? What new things can you do in English now?"},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# STEAM BRIDGE — Grade 5 (cross-curricular English)
# ══════════════════════════════════════════════════════════════════════════════

_STEAM_BANK = {
    5: {
        1: {"subject": "Maths", "title": "My Timetable in Numbers",
            "task": "Calculate: How many hours do you spend at school per week? How many hours do you sleep? "
                    "How many hours of free time do you have? Make a pie chart and label it in English.",
            "vocab": ["calculate", "total", "per week", "percentage", "chart"]},
        2: {"subject": "Art", "title": "Portrait Gallery",
            "task": "Draw a portrait of a famous person. Write 5 descriptive sentences underneath using: "
                    "has/have, is/are, wears, looks like.",
            "vocab": ["portrait", "sketch", "shading", "expression", "feature"]},
        3: {"subject": "Geography", "title": "My City Map",
            "task": "Create a detailed map of an imaginary city. Include at least 12 buildings. Write directions "
                    "between 3 pairs of places. Use: go straight, turn left/right, next to, between, opposite.",
            "vocab": ["compass", "scale", "legend", "intersection", "roundabout"]},
        4: {"subject": "Science", "title": "Weather Station",
            "task": "Build a simple rain gauge (a plastic bottle with cm markings). Measure rainfall for 5 days. "
                    "Record results in English: 'On Monday, it rained 3 cm.'",
            "vocab": ["measure", "rainfall", "temperature", "record", "data"]},
        5: {"subject": "Maths", "title": "Budget Challenge",
            "task": "You have 500 TL to plan a birthday party for 10 friends. Write a budget: food, drinks, "
                    "decorations, games. Calculate the cost per person. Stay within budget!",
            "vocab": ["budget", "total", "per person", "cost", "afford"]},
        6: {"subject": "Science", "title": "Food Groups Poster",
            "task": "Make a poster showing 5 food groups (proteins, carbohydrates, fats, vitamins, minerals). "
                    "Draw 3 foods for each group. Label everything in English.",
            "vocab": ["nutrients", "vitamins", "protein", "carbohydrate", "balanced diet"]},
        7: {"subject": "History", "title": "Timeline of Inventions",
            "task": "Make a timeline of 10 important inventions. Write when they were invented and who invented them. "
                    "Use Past Simple: 'Alexander Graham Bell invented the telephone in 1876.'",
            "vocab": ["invention", "discover", "century", "ancient", "modern"]},
        8: {"subject": "Technology", "title": "Dream App Design",
            "task": "Design an app that solves a problem. Draw 3 screens. Write: What is it called? What does it do? "
                    "Who is it for? Use going to: 'It is going to help students...'",
            "vocab": ["application", "design", "feature", "user", "screen"]},
        9: {"subject": "Art", "title": "Advice Poster",
            "task": "Create a classroom poster with 8 rules for being a good student. Use: should/must/have to. "
                    "Make it colourful with illustrations for each rule.",
            "vocab": ["poster", "illustration", "rule", "behaviour", "respect"]},
        10: {"subject": "All", "title": "My Year in Numbers",
             "task": "Create an infographic about YOUR school year. Include: number of books read, words learned, "
                     "friends made, projects completed, best grades. Label everything in English.",
             "vocab": ["infographic", "statistics", "achievement", "progress", "improvement"]},
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PODCAST / AUDIO — Grade 5 (mini podcast episode per unit)
# ══════════════════════════════════════════════════════════════════════════════

_PODCAST_BANK = {
    5: {
        1: {"title": "Episode 1: My School, My World",
            "host": "Elif & Can",
            "summary": "Elif and Can talk about their school day, their favourite subjects and what makes their school special.",
            "segments": ["Intro (0:00): Hello and welcome!", "Topic (0:30): Our school timetable",
                         "Guest Interview (2:00): Ms. Yildiz — Why is English important?",
                         "Fun Fact (3:30): 'School' comes from a Greek word meaning 'free time'!",
                         "Challenge (4:00): Describe YOUR school in 5 sentences and record it!"],
            "student_task": "Record a 1-minute podcast about YOUR school. Say: name, location, subjects, best thing."},
        2: {"title": "Episode 2: Family Matters",
            "host": "Sude & Can",
            "summary": "Sude describes her family and Can asks questions. They discuss what makes a family special.",
            "segments": ["Intro (0:00): Welcome back!", "Topic (0:30): Describing our families",
                         "Game (2:00): 'Guess Who?' — describe a person, the other guesses",
                         "Fun Fact (3:00): The longest family name in the world has 666 letters!",
                         "Challenge (3:30): Describe a family member without saying their name. Can your friend guess?"],
            "student_task": "Record yourself describing 3 family members. Use: has, is, wears, likes."},
        3: {"title": "Episode 3: Around Town",
            "host": "Elif & Sude",
            "summary": "Elif gives Sude directions to a secret place. Sude follows the directions and guesses where she is going.",
            "segments": ["Intro (0:00): Today's challenge!", "Directions Game (0:30): Follow my directions!",
                         "Interview (2:00): A tourist's experience in a Turkish town",
                         "Fun Fact (3:00): The longest street name in the world is in New Zealand — 89 letters!",
                         "Challenge (3:30): Give directions from your home to school. Record them!"],
            "student_task": "Record directions from your home to your favourite place. Use: go straight, turn left/right."},
        4: {"title": "Episode 4: Weather Around Turkey",
            "host": "Can & Elif",
            "summary": "Can pretends to be a weather reporter. He gives the forecast for 5 Turkish cities.",
            "segments": ["Intro (0:00): Can's Weather Show!", "Forecast (0:30): Istanbul, Antalya, Erzurum, Izmir, Trabzon",
                         "Game (2:30): 'What am I wearing?' — guess the weather from the clothes",
                         "Fun Fact (3:30): It once rained frogs in Serbia!",
                         "Challenge (4:00): Be a weather reporter! Forecast tomorrow's weather in English."],
            "student_task": "Record a 1-minute weather forecast for your city. Use: It is sunny/cloudy/rainy/snowy/windy."},
        5: {"title": "Episode 5: Let's Go Shopping!",
            "host": "Sude & Can",
            "summary": "Sude and Can visit a market. They practise buying things, asking prices and counting change.",
            "segments": ["Intro (0:00): Market day!", "Shopping Dialogue (0:30): Buying fruit and cheese",
                         "Maths Challenge (2:00): Quick price calculations",
                         "Fun Fact (3:00): The Grand Bazaar has 4,000 shops and 250,000 daily visitors!",
                         "Challenge (3:30): Record a shopping dialogue with a friend!"],
            "student_task": "Record a 1-minute shopping dialogue. Use: How much is...? Can I have...? Here you are."},
        6: {"title": "Episode 6: What's Cooking?",
            "host": "Elif & Sude",
            "summary": "Elif reads a recipe while Sude tries to follow it. Funny mistakes happen!",
            "segments": ["Intro (0:00): Kitchen time!", "Recipe (0:30): How to make a cheese toast",
                         "Disaster (2:00): Sude puts salt instead of sugar!",
                         "Fun Fact (3:00): Turkish people eat 3 billion simits per year!",
                         "Challenge (3:30): Teach someone a recipe in English. Record it!"],
            "student_task": "Record yourself explaining how to make your favourite snack. Use: first, then, next, finally."},
        7: {"title": "Episode 7: The Time Capsule",
            "host": "Can & Elif",
            "summary": "Can and Elif talk about what they did last summer. They create a 'time capsule' of memories.",
            "segments": ["Intro (0:00): Let's go back in time!", "Summer Stories (0:30): What did you do?",
                         "Game (2:00): 'True or False?' — Did it really happen?",
                         "Fun Fact (3:00): The oldest time capsule was buried in 1795!",
                         "Challenge (3:30): Talk about YOUR best holiday memory!"],
            "student_task": "Record your best memory. Use Past Simple: I went, I saw, I ate, I played..."},
        8: {"title": "Episode 8: Future Dreams",
            "host": "Sude & Can",
            "summary": "Sude and Can talk about their plans and dreams for the future.",
            "segments": ["Intro (0:00): Dream big!", "Plans (0:30): What are you going to do this summer?",
                         "Dreams (2:00): What do you want to be when you grow up?",
                         "Fun Fact (3:00): 65% of today's students will have jobs that don't exist yet!",
                         "Challenge (3:30): Describe your future plans!"],
            "student_task": "Record your plans for the future. Use: I am going to... / I want to be..."},
        9: {"title": "Episode 9: School Survival Guide",
            "host": "Elif & Can & Sude",
            "summary": "All three give advice to new students. What should you do? What shouldn't you do?",
            "segments": ["Intro (0:00): New student guide!", "Advice (0:30): 10 tips for school success",
                         "Debate (2:00): Should students wear uniforms? Yes or No?",
                         "Fun Fact (3:00): Finnish students have no homework and they are the best in Europe!",
                         "Challenge (3:30): Record 5 pieces of advice for a new student!"],
            "student_task": "Record 5 tips for a new student at your school. Use: You should... You must... Don't..."},
        10: {"title": "Episode 10: The Grand Finale!",
             "host": "Elif & Can & Sude & Ms. Yildiz",
             "summary": "Everyone celebrates the end of the year. They share favourite moments and say goodbye.",
             "segments": ["Intro (0:00): The final episode!", "Best Moments (0:30): Our favourite memories this year",
                          "Quiz (2:00): End-of-year English quiz!",
                          "Thank You (3:30): Messages to listeners and classmates",
                          "Goodbye (4:00): See you in Grade 6!"],
             "student_task": "Record a 2-minute 'goodbye' message. What did you learn? Who do you want to thank?"},
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# CONTENT BANK LOADER — merges per-grade content into module-level banks
# ══════════════════════════════════════════════════════════════════════════════

def _load_all_content_banks():
    """Import content banks from views/content_banks/gradeN.py and merge."""
    # Map of bank attribute names in grade files -> module-level bank dicts
    _BANK_MAP = {
        "READING_BANK": _READING_BANK,
        "GRAMMAR_BANK": _GRAMMAR_BANK,
        "DIALOGUE_BANK": _DIALOGUE_BANK,
        "CULTURE_CORNER_BANK": _CULTURE_CORNER_BANK,
        "FUN_FACTS_BANK": _FUN_FACTS_BANK,
        "PROJECT_BANK": _PROJECT_BANK,
        "SONG_BANK": _SONG_BANK,
        "PROGRESS_CHECK_BANK": _PROGRESS_CHECK_BANK,
        "LISTENING_SCRIPT_BANK": _LISTENING_SCRIPT_BANK,
        "MODEL_WRITING_BANK": _MODEL_WRITING_BANK,
        "PRONUNCIATION_BANK": _PRONUNCIATION_BANK,
        "WORKBOOK_BANK": _WORKBOOK_BANK,
        "STORY_CHARACTERS": _STORY_CHARACTERS,
        "STORY_BANK": _STORY_BANK,
        "TURKEY_CORNER_BANK": _TURKEY_CORNER_BANK,
        "COMIC_STRIP_BANK": _COMIC_STRIP_BANK,
        "GAMIFICATION_BANK": _GAMIFICATION_BANK,
        "MISSION_BANK": _MISSION_BANK,
        "ESCAPE_ROOM_BANK": _ESCAPE_ROOM_BANK,
        "FAMILY_CORNER_BANK": _FAMILY_CORNER_BANK,
        "SEL_BANK": _SEL_BANK,
        "STEAM_BANK": _STEAM_BANK,
        "PODCAST_BANK": _PODCAST_BANK,
    }

    # Grades to load (5 already exists inline)
    for grade_num in [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]:
        try:
            mod = __import__(f"views.content_banks.grade{grade_num}",
                             fromlist=list(_BANK_MAP.keys()))
        except ImportError:
            continue
        for attr_name, target_dict in _BANK_MAP.items():
            src = getattr(mod, attr_name, None)
            if src and isinstance(src, dict):
                # GAMIFICATION_BANK has non-standard structure — skip normalization
                if attr_name == "GAMIFICATION_BANK":
                    target_dict.update(src)
                    continue
                # Normalize: unwrap list-wrapped unit values to single dict
                # Content banks for grades 9-12 use list-of-dicts per unit
                # but the PDF generator expects single dicts
                normalized_src = {}
                for gk, gv in src.items():
                    if isinstance(gv, dict):
                        norm_units = {}
                        for uk, uv in gv.items():
                            # Unwrap list-wrapped values
                            if isinstance(uv, list) and uv and isinstance(uv[0], dict):
                                uv = uv[0]
                            elif isinstance(uv, list) and uv and isinstance(uv[0], str) and attr_name == "STORY_BANK":
                                uv = {"title": f"Unit {uk} Story", "episode": " ".join(uv),
                                      "previously": None, "cliffhanger": None, "vocab_tie": []}
                            # Normalize key names for dict values
                            if isinstance(uv, dict):
                                uv = dict(uv)  # shallow copy
                                if attr_name == "CULTURE_CORNER_BANK":
                                    if "content" in uv and "text" not in uv:
                                        uv["text"] = uv.pop("content")
                                    if "discussion_questions" in uv and "question" not in uv:
                                        dqs = uv.pop("discussion_questions")
                                        uv["question"] = dqs[0] if isinstance(dqs, list) and dqs else str(dqs)
                                elif attr_name == "MODEL_WRITING_BANK":
                                    if "model" in uv and "text" not in uv:
                                        uv["text"] = uv.pop("model")
                                    if "key_features" in uv and "focus" not in uv:
                                        kf = uv.pop("key_features")
                                        uv["focus"] = ", ".join(kf) if isinstance(kf, list) else str(kf)
                                    if "topic" in uv and "title" not in uv:
                                        uv["title"] = uv.pop("topic")
                                elif attr_name == "PROJECT_BANK":
                                    if "description" in uv and "desc" not in uv:
                                        uv["desc"] = uv.pop("description")
                                elif attr_name == "READING_BANK":
                                    # Normalize question format
                                    qs = uv.get("questions", [])
                                    norm_qs = []
                                    for q in qs:
                                        if not isinstance(q, dict):
                                            norm_qs.append({"type": "open", "q": str(q)})
                                            continue
                                        nq = dict(q)
                                        if "question" in nq and "q" not in nq:
                                            nq["q"] = nq.pop("question")
                                        if "options" in nq and "opts" not in nq:
                                            nq["opts"] = nq.pop("options")
                                        if "type" not in nq:
                                            nq["type"] = "mcq" if nq.get("opts") else "open"
                                        if isinstance(nq.get("answer"), int) and nq.get("opts"):
                                            idx = nq["answer"]
                                            if 0 <= idx < len(nq["opts"]):
                                                nq["answer"] = nq["opts"][idx]
                                        norm_qs.append(nq)
                                    if norm_qs:
                                        uv["questions"] = norm_qs
                            norm_units[uk] = uv
                        normalized_src[gk] = norm_units
                    else:
                        normalized_src[gk] = gv
                target_dict.update(normalized_src)


# Run loader at module import time
_load_all_content_banks()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PDF GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_textbook_pdf(grade: int, curriculum_weeks: list,
                          institution_info: dict | None = None,
                          selected_units: list[int] | None = None) -> bytes:
    """Generate a professional English coursebook PDF.

    Args:
        grade: Grade number (5, 6, 7, or 8)
        curriculum_weeks: Curriculum week list (36 items)
        institution_info: Optional institution details
        selected_units: Unit numbers to include (1-10). None = all.

    Returns:
        PDF bytes
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.units import cm, mm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, PageBreak, Flowable)
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
        from utils.shared_data import ensure_turkish_pdf_fonts
        from utils.book_design_system import (
            build_reportlab_colors, build_paragraph_styles, get_tier_for_grade,
            get_unit_color, get_section_colors, get_color_hex, get_grade_config,
            draw_page_header_footer, build_section_header_table, build_content_box,
            build_tip_box, build_unit_opener, PAGE_LAYOUT, HEADER_FOOTER,
            UNIT_COLOR_SEQUENCE, SECTION_COLORS as DS_SECTION_COLORS,
        )
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()
    font_ok = font_name != "Helvetica"
    def _t(text):
        if font_ok:
            return str(text)
        _map = str.maketrans("ıİğĞüÜşŞöÖçÇ", "iIgGuUsSoOcC")
        return str(text).translate(_map)

    info = institution_info or {}
    cfg = GRADE_CONFIG.get(grade, GRADE_CONFIG[5])
    today = datetime.now().date()
    acad_start = today.year if today.month >= 9 else today.year - 1
    acad_year = f"{acad_start}-{acad_start + 1}"

    unit_groups = build_unit_groups(grade, curriculum_weeks)
    units_to_gen = selected_units or list(range(1, len(unit_groups) + 1))
    # Load existing page map for cross-references
    _page_map = load_page_map(grade)

    # ── Colours from Design System ──
    C = build_reportlab_colors(rl_colors)
    C_NAVY = C["navy"]
    C_DARK = C["dark"]
    C_BLUE = C["blue"]
    C_BLUE_D = C["blue_dark"]
    C_BLUE_L = C["blue_light"]
    C_GREEN = C["green"]
    C_GREEN_L = C["green_light"]
    C_PURPLE = C["purple"]
    C_PURPLE_L = C["purple_light"]
    C_ORANGE = C["orange"]
    C_ORANGE_L = C["orange_light"]
    C_RED = C["red"]
    C_RED_L = C["red_light"]
    C_TEAL = C["teal"]
    C_TEAL_L = C["teal_light"]
    C_GOLD = C["gold"]
    C_GOLD_L = C["gold_light"]
    C_PINK = C["pink"]
    C_PINK_L = C["pink_light"]
    C_SLATE = C["slate"]
    C_WHITE = rl_colors.white
    C_TEXT = C["text"]
    C_SUB = C["sub"]
    C_LIGHT = C["light"]
    C_BORDER = C["border"]

    UNIT_COLORS = [rl_colors.HexColor(get_unit_color(i+1)) for i in range(10)]
    UNIT_BG = [C_BLUE_L, C_GREEN_L, C_PURPLE_L, C_ORANGE_L, C_TEAL_L,
               C_RED_L, C_BLUE_L, C_PINK_L, C_GOLD_L, C_LIGHT]

    # Page layout from design system
    margin_l = PAGE_LAYOUT["margin_left"] * mm
    margin_r = PAGE_LAYOUT["margin_right"] * mm
    margin_t = PAGE_LAYOUT["margin_top"] * mm
    margin_b = PAGE_LAYOUT["margin_bottom"] * mm
    pw = A4[0] - margin_l - margin_r

    # ── Styles from Design System ──
    s = build_paragraph_styles(grade, font_name, font_bold, rl_colors)
    # Add aliases used throughout the code
    s["cover_t"] = s["cover_title"]
    s["cover_s"] = s["cover_subtitle"]
    s["cover_i"] = s.get("cover_info", ParagraphStyle("ci", fontName=font_name, fontSize=11, leading=15, alignment=TA_CENTER, textColor=rl_colors.HexColor("#CBD5E1")))
    s["unit_t"] = s["unit_title"]
    s["unit_s"] = s["unit_subtitle"]
    s["sec_t"] = s["section_title"]
    s["body_j"] = s.get("body_j", s["body"])
    s["body_s"] = s.get("body_s", s["body"])
    s["ex_i"] = s.get("ex_i", s["ex"])
    s["cell_w"] = s.get("cell_w", s["cell"])
    s["cell_s"] = s.get("cell_s", s["cell"])
    s["instr"] = s.get("instr", s["h3"])
    s["tip_t"] = s.get("tip_t", s["h3"])
    s["tip_b"] = s.get("tip_b", s["body"])
    s["fact_t"] = s.get("fact_t", s["h3"])
    s["fact_b"] = s.get("fact_b", s["body"])
    s["dlg_name"] = s.get("dlg_name", s["h3"])
    s["dlg_line"] = s.get("dlg_line", s["body"])
    s["proj_t"] = s.get("proj_t", s["h2"])
    s["proj_b"] = s.get("proj_b", s["body"])
    s["appendix_t"] = s.get("appendix_t", s["h1"])
    s["appendix_h"] = ParagraphStyle("aph", fontName=font_bold, fontSize=12, leading=16, textColor=C_TEXT, spaceBefore=10, spaceAfter=4)
    s["glossary"] = s.get("glossary", s["body_s"])

    # ── Tier-based adaptation parameters ──
    from utils.book_design_system import get_tier_name, get_sections_for_grade
    _tier_name = get_tier_name(grade)
    _tier = get_tier_for_grade(grade)
    _tier_sections = set(get_sections_for_grade(grade))

    # Tier-adaptive layout/content parameters
    _TIER_PARAMS = {
        "preschool":     {"illust_h": 4.5, "unit_illust_h": 5.0, "spacer": 0.6,
                          "vocab_cols": 2, "fill_blank_n": 3, "match_n": 3, "write_sent_n": 3,
                          "reading_lines": 1, "grammar_ex_max": 3, "grammar_write_n": 2,
                          "listen_lines": 1, "speak_lines": 2, "write_lines": 3,
                          "review_cando": 4, "note_area_h": 2.0, "project_notes_h": 2.0,
                          "show_pre_reading": False, "show_reading_strategy": False,
                          "show_warning_box": False, "show_irregular_verbs": False,
                          "show_phonetic_chart": False, "show_grammar_summary": False},
        "primary_lower": {"illust_h": 3.5, "unit_illust_h": 4.0, "spacer": 0.5,
                          "vocab_cols": 2, "fill_blank_n": 4, "match_n": 4, "write_sent_n": 3,
                          "reading_lines": 1, "grammar_ex_max": 4, "grammar_write_n": 3,
                          "listen_lines": 1, "speak_lines": 3, "write_lines": 4,
                          "review_cando": 5, "note_area_h": 2.5, "project_notes_h": 2.5,
                          "show_pre_reading": False, "show_reading_strategy": False,
                          "show_warning_box": False, "show_irregular_verbs": False,
                          "show_phonetic_chart": False, "show_grammar_summary": False},
        "primary_upper": {"illust_h": 3.0, "unit_illust_h": 3.5, "spacer": 0.4,
                          "vocab_cols": 3, "fill_blank_n": 5, "match_n": 5, "write_sent_n": 4,
                          "reading_lines": 2, "grammar_ex_max": 5, "grammar_write_n": 3,
                          "listen_lines": 1, "speak_lines": 3, "write_lines": 5,
                          "review_cando": 6, "note_area_h": 2.5, "project_notes_h": 2.5,
                          "show_pre_reading": True, "show_reading_strategy": False,
                          "show_warning_box": True, "show_irregular_verbs": False,
                          "show_phonetic_chart": False, "show_grammar_summary": True},
        "middle":        {"illust_h": 2.5, "unit_illust_h": 3.0, "spacer": 0.3,
                          "vocab_cols": 3, "fill_blank_n": 6, "match_n": 5, "write_sent_n": 5,
                          "reading_lines": 2, "grammar_ex_max": 6, "grammar_write_n": 4,
                          "listen_lines": 1, "speak_lines": 4, "write_lines": 6,
                          "review_cando": 8, "note_area_h": 3.0, "project_notes_h": 3.0,
                          "show_pre_reading": True, "show_reading_strategy": True,
                          "show_warning_box": True, "show_irregular_verbs": True,
                          "show_phonetic_chart": True, "show_grammar_summary": True},
        "high":          {"illust_h": 2.0, "unit_illust_h": 2.5, "spacer": 0.25,
                          "vocab_cols": 4, "fill_blank_n": 8, "match_n": 6, "write_sent_n": 6,
                          "reading_lines": 3, "grammar_ex_max": 8, "grammar_write_n": 5,
                          "listen_lines": 2, "speak_lines": 5, "write_lines": 8,
                          "review_cando": 10, "note_area_h": 3.0, "project_notes_h": 3.0,
                          "show_pre_reading": True, "show_reading_strategy": True,
                          "show_warning_box": True, "show_irregular_verbs": True,
                          "show_phonetic_chart": True, "show_grammar_summary": True},
    }
    tp = _TIER_PARAMS.get(_tier_name, _TIER_PARAMS["middle"])

    # Track current unit for header
    _current_unit_title = [""]
    book_title = "Early Steps" if grade == 0 else f"Bright Start {grade}" if grade <= 4 else f"Next Level {grade}" if grade <= 8 else f"English Core {grade}"

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=margin_t,
                            bottomMargin=margin_b,
                            leftMargin=margin_l,
                            rightMargin=margin_r)
    elements = []

    # ── Page Map Tracker — records page numbers per unit/section ──
    _page_tracker = {}
    def _pm(key):
        """Insert invisible page marker for section tracking."""
        return _make_page_marker(Flowable, _page_tracker, key)

    # ═══════════════════════════════════════════
    # COVER PAGE (Professional — from Design System)
    # ═══════════════════════════════════════════
    from utils.book_design_system import build_front_cover, build_back_cover
    kurum = info.get("name", "")
    kurum_display = _t(kurum) if kurum else ""

    cover_elements = build_front_cover(
        grade=grade, acad_year=acad_year,
        institution_name=kurum_display, pw=pw,
        font_name=font_name, font_bold=font_bold,
        unit_groups=unit_groups, units_to_gen=units_to_gen,
        rl_colors_module=rl_colors,
    )
    elements.extend(cover_elements)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════
    # Professional TOC header
    toc_hdr_data = [
        [Paragraph("TABLE OF CONTENTS", s["sec_t"])],
    ]
    toc_hdr = Table(toc_hdr_data, colWidths=[pw], rowHeights=[36])
    toc_hdr.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
    ]))
    elements.append(toc_hdr)
    elements.append(Spacer(1, 0.5 * cm))

    # "How to Use This Book" entry
    htub_row = Table([[
        Paragraph("", ParagraphStyle("tn0", fontName=font_bold, fontSize=10, leading=13,
                                      textColor=C_WHITE, alignment=TA_CENTER)),
        Paragraph('<b>How to Use This Book</b>',
                  ParagraphStyle("tt0", fontName=font_bold, fontSize=10, leading=14, textColor=C_TEXT)),
        Paragraph('Guide',
                  ParagraphStyle("tw0", fontName=font_name, fontSize=8, leading=11,
                                  textColor=C_SUB, alignment=TA_RIGHT)),
    ]], colWidths=[1 * cm, pw - 3.5 * cm, 2.5 * cm], rowHeights=[26])
    htub_row.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), C_SLATE),
        ("BACKGROUND", (1, 0), (-1, -1), C_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("BOX", (0, 0), (-1, -1), 0.3, C_BORDER),
    ]))
    elements.append(htub_row)
    elements.append(Spacer(1, 4))

    # Unit entries with sub-section indicators
    _toc_subsections = [
        "Vocabulary", "Reading", "Grammar", "Listening", "Writing",
        "Pronunciation", "Review", "Culture", "Project",
    ]
    for ug in unit_groups:
        if ug["unit"] not in units_to_gen:
            continue
        idx = ug["unit"] - 1
        clr = UNIT_COLORS[idx % 10]

        # Main unit row
        row = Table([[
            Paragraph(f'<font color="white"><b>{ug["unit"]}</b></font>',
                      ParagraphStyle("tn", fontName=font_bold, fontSize=10, leading=13,
                                      textColor=C_WHITE, alignment=TA_CENTER)),
            Paragraph(f'<b>{ug["title"]}</b>',
                      ParagraphStyle("tt", fontName=font_bold, fontSize=10, leading=14, textColor=C_TEXT)),
            Paragraph(f'Weeks {ug["weeks"][0]}-{ug["weeks"][-1]}',
                      ParagraphStyle("tw", fontName=font_name, fontSize=8, leading=11,
                                      textColor=C_SUB, alignment=TA_RIGHT)),
        ]], colWidths=[1 * cm, pw - 3.5 * cm, 2.5 * cm], rowHeights=[28])
        row.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), clr),
            ("BACKGROUND", (1, 0), (-1, -1), C_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("BOX", (0, 0), (-1, -1), 0.3, C_BORDER),
        ]))
        elements.append(row)

        # Sub-section dots under each unit
        sub_text = "  &bull;  ".join(f'<font size="6.5">{sec}</font>' for sec in _toc_subsections)
        sub_p = Paragraph(sub_text,
                          ParagraphStyle("tsub", fontName=font_name, fontSize=6.5, leading=9,
                                          textColor=C_SUB, leftIndent=1 * cm + 10))
        elements.append(sub_p)
        elements.append(Spacer(1, 4))

    # Section color legend
    ALL_SECTIONS = [
        ("Vocabulary", C_BLUE), ("Reading", C_GREEN), ("Grammar", C_PURPLE),
        ("Listen/Speak", C_ORANGE), ("Writing", C_TEAL), ("Dialogue", C_BLUE_D),
        ("Song", C_PINK), ("Culture", rl_colors.HexColor("#0369a1")),
        ("Project", C_GOLD), ("Review", C_RED),
    ]
    elements.append(Spacer(1, 0.3 * cm))
    leg_row = [[Paragraph(f'<font color="white"><b>{n}</b></font>',
                           ParagraphStyle("lgr", fontName=font_name, fontSize=6.5, leading=9,
                                           textColor=C_WHITE, alignment=TA_CENTER))
                for n, _ in ALL_SECTIONS]]
    leg = Table(leg_row, colWidths=[pw / len(ALL_SECTIONS)] * len(ALL_SECTIONS), rowHeights=[22])
    leg_sc = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 4),
              ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for ci, (_, clr) in enumerate(ALL_SECTIONS):
        leg_sc.append(("BACKGROUND", (ci, 0), (ci, 0), clr))
    leg.setStyle(TableStyle(leg_sc))
    elements.append(leg)

    # Appendix TOC
    elements.append(Spacer(1, 0.3 * cm))
    app_items = ["Glossary", "Answer Key", "Irregular Verbs", "Phonetic Chart",
                 "Grammar Summary", "Audio Scripts"]
    app_row = Table([[Paragraph(
        f'<b>Appendix:</b>  {" | ".join(app_items)}',
        ParagraphStyle("apx", fontName=font_name, fontSize=8, leading=11,
                        textColor=C_SUB, alignment=TA_CENTER))
    ]], colWidths=[pw])
    app_row.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.3, C_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    elements.append(app_row)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # HOW TO USE THIS BOOK
    # ═══════════════════════════════════════════
    htub_hdr = Table([[Paragraph("<b>HOW TO USE THIS BOOK</b>", s["sec_t"])]], colWidths=[pw], rowHeights=[34])
    htub_hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_NAVY), ("ALIGN",(0,0),(-1,-1),"CENTER"),
                                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("ROUNDEDCORNERS",[8,8,8,8])]))
    elements.append(htub_hdr)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("This coursebook is designed for maximum flexibility. Each unit has 3 layers:", s["body"]))
    elements.append(Spacer(1, 6))

    # Layer explanation
    layer_data = [
        [Paragraph("<b>Layer</b>", s["cell_w"]), Paragraph("<b>Where</b>", s["cell_w"]),
         Paragraph("<b>Sections</b>", s["cell_w"])],
        [Paragraph("<b>CORE</b><br/>(In Class)", s["cell"]),
         Paragraph("Classroom<br/>3-4 hours/week", s["cell_s"]),
         Paragraph("Story Episode, Vocabulary, Reading, Grammar, Listening &amp; Speaking, "
                   "Writing Workshop, Pronunciation, Review, Comic Strip", s["cell_s"])],
        [Paragraph("<b>HOMEWORK</b><br/>(At Home)", s["cell"]),
         Paragraph("Home<br/>self-study", s["cell_s"]),
         Paragraph("Workbook Exercises, Family Corner, Real-World Mission, Podcast Task", s["cell_s"])],
        [Paragraph("<b>BONUS</b><br/>(Optional)", s["cell"]),
         Paragraph("Anytime<br/>reward", s["cell_s"]),
         Paragraph("Gamification XP, SEL Corner, Escape Room, STEAM Bridge, Turkey Corner", s["cell_s"])],
    ]
    lt = Table(layer_data, colWidths=[2.5*cm, 3*cm, pw-5.5*cm])
    lt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_NAVY), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                             ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),6),
                             ("BOTTOMPADDING",(0,0),(-1,-1),6), ("LEFTPADDING",(0,0),(-1,-1),6),
                             ("BACKGROUND",(0,1),(0,1),C_BLUE_L), ("BACKGROUND",(0,2),(0,2),C_GREEN_L),
                             ("BACKGROUND",(0,3),(0,3),C_GOLD_L)]))
    elements.append(lt)
    elements.append(Spacer(1, 8))

    # Weekly plan template
    elements.append(Paragraph("<b>Suggested Weekly Lesson Plan (3 hours/week, 3.5 weeks per unit):</b>", s["h2"]))
    elements.append(Spacer(1, 4))
    wp_data = [
        [Paragraph("<b>Week</b>", s["cell_w"]), Paragraph("<b>Lesson 1 (40 min)</b>", s["cell_w"]),
         Paragraph("<b>Lesson 2 (40 min)</b>", s["cell_w"]), Paragraph("<b>Lesson 3 (40 min)</b>", s["cell_w"])],
        [Paragraph("<b>Week 1</b>", s["cell"]),
         Paragraph("Story Episode (15 min)\nVocabulary Workshop (25 min)", s["cell_s"]),
         Paragraph("Reading Comprehension (40 min)", s["cell_s"]),
         Paragraph("Grammar Focus (40 min)", s["cell_s"])],
        [Paragraph("<b>Week 2</b>", s["cell"]),
         Paragraph("Listening &amp; Speaking (40 min)", s["cell_s"]),
         Paragraph("Writing Workshop (25 min)\nPronunciation (15 min)", s["cell_s"]),
         Paragraph("Comic Strip (20 min)\nDialogue Corner (20 min)", s["cell_s"])],
        [Paragraph("<b>Week 3</b>", s["cell"]),
         Paragraph("Culture Corner (15 min)\nTurkey Corner (25 min)", s["cell_s"]),
         Paragraph("STEAM Bridge (20 min)\nProject Work (20 min)", s["cell_s"]),
         Paragraph("Review &amp; Self-Assessment (25 min)\nSong &amp; Rhyme (15 min)", s["cell_s"])],
        [Paragraph("<b>Week 3+</b>", s["cell"]),
         Paragraph("Digital Resources + Catch-up", s["cell_s"]),
         Paragraph("Progress Check (if applicable)", s["cell_s"]),
         Paragraph("Escape Room (if applicable)", s["cell_s"])],
    ]
    wpt = Table(wp_data, colWidths=[1.8*cm, (pw-1.8*cm)/3, (pw-1.8*cm)/3, (pw-1.8*cm)/3])
    wpt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_BLUE), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                              ("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),5),
                              ("BOTTOMPADDING",(0,0),(-1,-1),5), ("LEFTPADDING",(0,0),(-1,-1),5),
                              ("BACKGROUND",(0,1),(0,-1),C_BLUE_L)]))
    elements.append(wpt)
    elements.append(Spacer(1, 8))

    # Icons legend
    elements.append(Paragraph("<b>Special Features in This Book:</b>", s["h3"]))
    icon_data = [
        ["STORY", "Continuing adventure story with recurring characters"],
        ["QR CODE", "Scan for interactive digital activities on SmartCampus"],
        ["TIP", "Helpful advice and language learning strategies"],
        ["MISSION", "Real-world task to practise English outside school"],
        ["FAMILY", "Activity to do at home with your family"],
        ["XP", "Experience points — collect them to level up!"],
        ["ESCAPE", "Team puzzle challenge (after every 3 units)"],
        ["PODCAST", "Mini podcast episode — listen and record your own"],
    ]
    for ic_name, ic_desc in icon_data:
        elements.append(Paragraph(f'<b>[{ic_name}]</b>  {ic_desc}', s["body_s"]))
    elements.append(Spacer(1, 6))
    _htub_tip = Table([[Paragraph('<b>Audio &amp; Digital:</b> All QR codes link to SmartCampus. Scan with any phone camera to access '
                                   'listening exercises, speaking practice, games and more. Audio scripts are in the Appendix.',
                                   ParagraphStyle("htip", fontName=font_name, fontSize=9, leading=12.5, textColor=C_TEXT))]], colWidths=[pw])
    _htub_tip.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_GREEN_L), ("BOX",(0,0),(-1,-1),0.5,C_GREEN),
                                    ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),12),
                                    ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
                                    ("ROUNDEDCORNERS",[8,8,8,8])]))
    elements.append(_htub_tip)

    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # UNIT PAGES
    # ═══════════════════════════════════════════
    def _sec_hdr(title, color):
        """Professional section header bar with rounded top corners."""
        h = Table([[Paragraph(f'<b>{title}</b>', s["sec_t"])]], colWidths=[pw], rowHeights=[30])
        h.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("ROUNDEDCORNERS", [8, 8, 0, 0]),
        ]))
        return h

    def _box(text, bg, border, style_key="body"):
        """Content box with rounded bottom corners, pairs with _sec_hdr."""
        b = Table([[Paragraph(text, s[style_key])]], colWidths=[pw])
        b.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX", (0, 0), (-1, -1), 0.5, border),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [0, 0, 8, 8]),
        ]))
        return b

    def _lines(n, prefix=""):
        els = []
        for i in range(n):
            lbl = f"<b>{prefix}{i+1}.</b>  " if prefix else ""
            els.append(Paragraph(lbl + "_" * 75, ParagraphStyle("ln", fontName=font_name, fontSize=10,
                                                                  leading=20, textColor=C_BORDER)))
        return els

    # ── Styled box helpers ──
    def _tip_box(title, text, icon="TIP"):
        """Green tip/advice box."""
        rows = [
            [Paragraph(f'<b>{icon}: {title}</b>', s["tip_t"])],
            [Paragraph(text, s["tip_b"])],
        ]
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), C_GREEN),
            ("BACKGROUND", (0,1), (-1,1), C_GREEN_L),
            ("BOX", (0,0), (-1,-1), 0.5, C_GREEN),
            ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
            ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("ROUNDEDCORNERS", [8,8,8,8]),
        ]))
        return t

    def _warning_box(text):
        """Orange warning/note box."""
        rows = [[Paragraph(f'<b>NOTE:</b> {text}', s["tip_b"])]]
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), C_ORANGE_L),
            ("BOX", (0,0), (-1,-1), 0.5, C_ORANGE),
            ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
            ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("ROUNDEDCORNERS", [8,8,8,8]),
        ]))
        return t

    def _fact_box(facts_list):
        """Yellow 'Did You Know?' box with fun facts."""
        body = "<br/>".join(f"&bull; {f}" for f in facts_list)
        rows = [
            [Paragraph('<b>DID YOU KNOW?</b>', ParagraphStyle("fkh", fontName=font_bold, fontSize=10,
                        leading=14, textColor=rl_colors.HexColor("#92400e"), alignment=TA_CENTER))],
            [Paragraph(body, s["fact_b"])],
        ]
        t = Table(rows, colWidths=[pw])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), rl_colors.HexColor("#fef9c3")),
            ("BOX", (0,0), (-1,-1), 0.8, C_ORANGE),
            ("LEFTPADDING", (0,0), (-1,-1), 14), ("RIGHTPADDING", (0,0), (-1,-1), 14),
            ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("ROUNDEDCORNERS", [8,8,8,8]),
        ]))
        return t

    def _illustration_area(caption, height=2.5*cm):
        """Placeholder area for illustration/image."""
        rows = [[Paragraph(f'<i>[Illustration: {caption}]</i>',
                 ParagraphStyle("ill", fontName=font_name, fontSize=9, leading=12,
                                textColor=C_SUB, alignment=TA_CENTER))]]
        t = Table(rows, colWidths=[pw], rowHeights=[height])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), rl_colors.HexColor("#1A2035")),
            ("BOX", (0,0), (-1,-1), 1, rl_colors.HexColor("#cbd5e1")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("ROUNDEDCORNERS", [6,6,6,6]),
        ]))
        return t

    def _make_qr_image(url, size_cm=2):
        """Generate a real QR code image and return as ReportLab Image."""
        try:
            import qrcode
            from reportlab.platypus import Image as RLImage
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M,
                                box_size=6, border=1)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_buf = BytesIO()
            img.save(img_buf, format="PNG")
            img_buf.seek(0)
            return RLImage(img_buf, width=size_cm*cm, height=size_cm*cm)
        except Exception:
            return Paragraph(f'<b>[QR]</b>', ParagraphStyle("qrf", fontName=font_name,
                             fontSize=8, leading=10, textColor=C_SUB, alignment=TA_CENTER))

    def _get_base_url():
        """Get system base URL from kurum profili."""
        try:
            kp_path = os.path.join("data", "kurum_profili.json")
            if os.path.exists(kp_path):
                with open(kp_path, "r", encoding="utf-8") as f:
                    kp = _json.load(f)
                url = kp.get("app_base_url", "").strip().rstrip("/")
                if url:
                    return url
        except Exception:
            pass
        return "https://smartcampus.app"

    _base_url = _get_base_url()

    # Sekme index haritası — Yabancı Dil modülündeki sub_tabs indeksleri
    _TAB_INDEX = {
        "listening": 0, "speaking": 1, "reading": 2, "writing": 3,
        "grammar": 4, "vocabulary": 5, "pronunciation": 6, "spelling": 7,
        "functional": 8, "strategies": 9, "learning_path": 10, "kdg": 11,
        "kitaplar": 12, "kaynaklar": 13, "interactive": 14, "coursebook": 15,
        "song": None, "culture": None, "project": None,
    }

    def _qr_placeholder(label, qr_type="listening", unit_num=0):
        """Generate a real QR code box with URL pointing to SmartCampus content.

        qr_type maps to:
          - listening/speaking/reading/writing/grammar/vocabulary/pronunciation
            → İlgili beceri sekmesi (sub_tabs index)
          - kitaplar → Flipbook kitaplar sekmesi
          - kaynaklar → Dış kaynaklar sekmesi
          - interactive → İnteraktif oyunlar sekmesi
          - coursebook → Ders kitabı sekmesi
          - song/culture/project → Genel sınıf sayfası
        """
        import urllib.parse
        tab_idx = _TAB_INDEX.get(qr_type)
        params = {
            "modul": "yabanci_dil",
            "aksiyon": qr_type,
            "sinif": str(grade),
            "unite": str(unit_num),
        }
        if tab_idx is not None:
            params["sekme"] = str(tab_idx)
        url = f"{_base_url}?{urllib.parse.urlencode(params)}"
        qr_img = _make_qr_image(url, size_cm=1.8)
        rows = [[qr_img, Paragraph(f'<font size="6.5" color="#64748b">{label}</font>',
                 ParagraphStyle("qrl", fontName=font_name, fontSize=7, leading=9,
                                textColor=C_SUB))]]
        t = Table(rows, colWidths=[2.1*cm, 3*cm], rowHeights=[2*cm])
        t.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (0,0), 2),
            ("LEFTPADDING", (1,0), (1,0), 4),
        ]))
        return t

    def _qr_grid(unit_num):
        """Generate a grid of QR codes for all relevant tabs — placed at unit end."""
        qr_items = [
            ("listening", "Listening"),
            ("speaking", "Speaking"),
            ("reading", "Reading"),
            ("grammar", "Grammar"),
            ("vocabulary", "Vocabulary"),
            ("kitaplar", "Books"),
            ("kaynaklar", "Resources"),
            ("interactive", "Games"),
        ]
        rows = []
        row = []
        for qr_t, lbl in qr_items:
            cell = _qr_placeholder(f"{lbl}\nU{unit_num}", qr_type=qr_t, unit_num=unit_num)
            row.append(cell)
            if len(row) == 4:
                rows.append(row)
                row = []
        if row:
            row.extend([""] * (4 - len(row)))
            rows.append(row)
        if rows:
            grid = Table(rows, colWidths=[pw/4]*4)
            grid.setStyle(TableStyle([
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("TOPPADDING",(0,0),(-1,-1),4),
                ("BOTTOMPADDING",(0,0),(-1,-1),4),
            ]))
            return grid
        return Spacer(1, 1)

    # collector for glossary and answer key
    _glossary_words = []
    _answer_key = []

    for ug in unit_groups:
        if ug["unit"] not in units_to_gen:
            continue
        ui = ug["unit"] - 1
        clr = UNIT_COLORS[ui % 10]
        bg = UNIT_BG[ui % 10]
        weeks = ug["week_data"]
        # Track current unit for header/footer display
        _current_unit_title[0] = f'Unit {ug["unit"]} — {ug["title"]}'
        _u = ug["unit"]
        elements.append(_pm(f"unit_{_u}_opener"))
        all_vocab = []
        all_struct = []
        for w in weeks:
            all_vocab.extend(w.get("vocab", []))
            st2 = w.get("structure", "")
            if st2:
                all_struct.append(st2)
        unique_vocab = list(dict.fromkeys(all_vocab))

        # ─── 1. UNIT OPENER ───
        uhdr = Table([[Paragraph(f'<font size="32"><b>UNIT {ug["unit"]}</b></font>', s["unit_t"])]],
                     colWidths=[pw], rowHeights=[55])
        uhdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),clr), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                   ("LEFTPADDING",(0,0),(-1,-1),20), ("ROUNDEDCORNERS",[12,12,0,0])]))
        elements.append(uhdr)

        title_data = [
            [Paragraph(f'<b>{ug["title"]}</b>', ParagraphStyle("utt", fontName=font_bold, fontSize=22, leading=28, textColor=C_NAVY))],
            [Spacer(1, 4)],
            [Paragraph(f'CEFR {cfg["cefr"]}  |  Weeks {ug["weeks"][0]}-{ug["weeks"][-1]}  |  Grade {grade}',
                       ParagraphStyle("um", fontName=font_name, fontSize=9, leading=12, textColor=C_SUB))],
        ]
        if len(ug["themes"]) > 1:
            sub_themes = ", ".join(ug["themes"][1:])
            title_data.append([Paragraph(f'<i>Also covering: {sub_themes}</i>',
                                         ParagraphStyle("ust", fontName=font_name, fontSize=8.5, leading=11, textColor=C_SUB))])

        ttbl = Table(title_data, colWidths=[pw])
        ttbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg), ("LEFTPADDING",(0,0),(-1,-1),20),
                                   ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
                                   ("ROUNDEDCORNERS",[0,0,12,12]), ("BOX",(0,0),(-1,-1),0.5,clr)]))
        elements.append(ttbl)
        elements.append(Spacer(1, 0.4*cm))

        # Learning objectives
        elements.append(Paragraph("<b>In this unit, you will learn to:</b>", s["h2"]))
        obj_data = []
        skill_clrs = {"L": C_BLUE, "S": C_GREEN, "R": C_PURPLE, "W": C_ORANGE}
        for w in weeks[:2]:
            sk = w.get("skills", {})
            for key, label, letter in [("listening","Listening","L"), ("speaking","Speaking","S"),
                                        ("reading","Reading","R"), ("writing","Writing","W")]:
                desc = sk.get(key, "")
                if desc:
                    obj_data.append([
                        Paragraph(f'<font color="white"><b>{letter}</b></font>',
                                  ParagraphStyle("ol", fontName=font_bold, fontSize=8, leading=10, textColor=C_WHITE, alignment=TA_CENTER)),
                        Paragraph(desc, s["cell_s"]),
                    ])
        if obj_data:
            ot = Table(obj_data, colWidths=[0.8*cm, pw-0.8*cm])
            ost = [("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),3), ("BOTTOMPADDING",(0,0),(-1,-1),3),
                   ("LEFTPADDING",(1,0),(1,-1),8), ("GRID",(0,0),(-1,-1),0.3,C_BORDER)]
            for ri in range(len(obj_data)):
                for letter, c in skill_clrs.items():
                    txt = str(obj_data[ri][0])
                    if letter in txt:
                        ost.append(("BACKGROUND",(0,ri),(0,ri),c)); break
            ot.setStyle(TableStyle(ost))
            elements.append(ot)

        # Key structures preview
        if all_struct:
            elements.append(Spacer(1, 0.3*cm))
            struct_txt = "<b>Key Language:</b><br/>" + "<br/>".join(f"&bull; <i>{s2}</i>" for s2 in all_struct[:3])
            elements.append(_box(struct_txt, C_LIGHT, C_BORDER))

        # Illustration area for unit theme
        elements.append(Spacer(1, tp["spacer"]*cm))
        elements.append(_illustration_area(f"Unit {ug['unit']} Theme: {ug['title']}", height=tp["unit_illust_h"]*cm))

        # Collect vocab for glossary
        _glossary_words.extend(unique_vocab)

        elements.append(PageBreak())

        # ─── 1b. STORY EPISODE ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_story"))
        _story = _STORY_BANK.get(grade, {}).get(ug["unit"], None) if "story" in _tier_sections else None
        if _story:
            st_color = rl_colors.HexColor("#4c1d95")
            st_bg = rl_colors.HexColor("#ede9fe")
            elements.append(_sec_hdr(f'STORY: {_story.get("title", "Story").upper()}', st_color))
            elements.append(Spacer(1, 6))

            # Previously...
            if _story.get("previously"):
                prev_box = Table([[Paragraph(f'<i><b>Previously...</b> {_story["previously"]}</i>', s["body_s"])]], colWidths=[pw])
                prev_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), rl_colors.HexColor("#f5f3ff")),
                    ("BOX",(0,0),(-1,-1),0.5, st_color), ("LEFTPADDING",(0,0),(-1,-1),12),
                    ("RIGHTPADDING",(0,0),(-1,-1),12), ("TOPPADDING",(0,0),(-1,-1),8),
                    ("BOTTOMPADDING",(0,0),(-1,-1),8), ("ROUNDEDCORNERS",[8,8,8,8])]))
                elements.append(prev_box)
                elements.append(Spacer(1, 6))

            # Characters (only Unit 1)
            if ug["unit"] == 1:
                _chars = _STORY_CHARACTERS.get(grade, {}).get("main", [])
                if _chars:
                    elements.append(Paragraph("<b>Meet the Characters:</b>", s["h3"]))
                    char_rows = []
                    for ch in _chars:
                        if isinstance(ch, dict):
                            char_rows.append([
                                Paragraph(f'<b>{ch.get("name","")}</b> ({ch.get("age","")})', s["cell"]),
                                Paragraph(ch.get("desc", ""), s["cell_s"]),
                            ])
                        elif isinstance(ch, str):
                            char_rows.append([
                                Paragraph(f'<b>{ch}</b>', s["cell"]),
                                Paragraph("", s["cell_s"]),
                            ])
                    cht = Table(char_rows, colWidths=[3*cm, pw-3*cm])
                    cht.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1), st_bg), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                        ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),5),
                        ("BOTTOMPADDING",(0,0),(-1,-1),5), ("LEFTPADDING",(0,0),(-1,-1),6)]))
                    elements.append(cht)
                    elements.append(Spacer(1, 6))

            # Episode illustration
            elements.append(_illustration_area(f'Story Scene: {_story.get("title", "Story")}', height=tp["illust_h"]*cm))
            elements.append(Spacer(1, 6))

            # Episode text
            _ep_text = _story.get("episode") or _story.get("story") or _story.get("text", "")
            ep_box = Table([[Paragraph(_ep_text, s["body_j"])]], colWidths=[pw])
            ep_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), st_bg),
                ("BOX",(0,0),(-1,-1), 0.8, st_color), ("LEFTPADDING",(0,0),(-1,-1),14),
                ("RIGHTPADDING",(0,0),(-1,-1),14), ("TOPPADDING",(0,0),(-1,-1),12),
                ("BOTTOMPADDING",(0,0),(-1,-1),12), ("ROUNDEDCORNERS",[10,10,10,10])]))
            elements.append(ep_box)
            elements.append(Spacer(1, 6))

            # Cliffhanger
            if _story.get("cliffhanger"):
                elements.append(_warning_box(f'TO BE CONTINUED... {_story["cliffhanger"]}'))
                elements.append(Spacer(1, 4))

            # Vocabulary tie-in (Grade 0-7: vocab_tie, Grade 8+: vocabulary)
            _story_vocab = _story.get("vocab_tie") or _story.get("vocabulary", [])
            if _story_vocab:
                vt_text = "  |  ".join(_story_vocab)
                elements.append(Paragraph(f'<b>Story Words:</b> {vt_text}', s["body_s"]))
            # Moral (Grade 8+)
            if _story.get("moral"):
                elements.append(Spacer(1, 4))
                elements.append(_tip_box("Moral", _story["moral"], icon="TIP"))

            elements.append(PageBreak())

        # ─── 2. VOCABULARY WORKSHOP ─── (always included — core section)
        elements.append(_pm(f"unit_{_u}_vocabulary"))
        elements.append(_sec_hdr("VOCABULARY WORKSHOP", C_BLUE))
        elements.append(Spacer(1, 6))

        # Word bank grid
        if unique_vocab:
            elements.append(Paragraph("<b>A. Word Bank</b>", s["h3"]))
            vcols = tp["vocab_cols"]
            v_rows = []
            for vi in range(0, len(unique_vocab), vcols):
                row = []
                for ci in range(vcols):
                    if vi+ci < len(unique_vocab):
                        row.append(Paragraph(f'<b>{vi+ci+1}.</b> {unique_vocab[vi+ci]}', s["cell_s"]))
                    else:
                        row.append("")
                v_rows.append(row)
            vt = Table(v_rows, colWidths=[pw/vcols]*vcols)
            vs = [("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),4),
                  ("BOTTOMPADDING",(0,0),(-1,-1),4), ("LEFTPADDING",(0,0),(-1,-1),6),
                  ("GRID",(0,0),(-1,-1),0.3,C_BORDER)]
            for ri in range(len(v_rows)):
                vs.append(("BACKGROUND",(0,ri),(-1,ri), C_BLUE_L if ri%2==0 else C_WHITE))
            vt.setStyle(TableStyle(vs))
            elements.append(vt)
            elements.append(Spacer(1, 0.4*cm))

        # Exercises
        elements.append(Paragraph("<b>B. Fill in the blanks with words from the Word Bank.</b>", s["instr"]))
        for i in range(min(tp["fill_blank_n"], len(unique_vocab))):
            elements.append(Paragraph(f"<b>{i+1}.</b>  " + "_" * 70, s["ex"]))
            elements.append(Spacer(1, 2))

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>C. Match the words with their definitions.</b>", s["instr"]))
        cols_match = min(tp["match_n"], len(unique_vocab))
        for i in range(cols_match):
            elements.append(Paragraph(f"<b>{i+1}.</b>  {unique_vocab[i]}  {'.' * 40}  (   )", s["ex"]))

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(f"<b>D. Use {tp['write_sent_n']} words from the Word Bank to write your own sentences.</b>", s["instr"]))
        elements.extend(_lines(tp["write_sent_n"]))

        # Fun Facts box
        facts = _FUN_FACTS_BANK.get(grade, {}).get(ug["unit"], None)
        if facts:
            elements.append(Spacer(1, 0.4*cm))
            elements.append(_fact_box(facts))

        elements.append(PageBreak())

        # ─── 3. READING ───
        elements.append(_pm(f"unit_{_u}_reading"))
        elements.append(_sec_hdr("READING COMPREHENSION", C_GREEN))
        elements.append(Spacer(1, 6))

        passage = _generate_reading(grade, ug["unit"], ug["title"], unique_vocab, all_struct[0] if all_struct else "")
        elements.append(Paragraph(f'<b>{passage.get("title", "Reading")}</b>', s["h2"]))
        elements.append(Spacer(1, 4))

        # Pre-reading (tier-adapted)
        if tp["show_pre_reading"]:
            elements.append(Paragraph("<b>Before you read:</b> Look at the title. What do you think the text is about? "
                                      "Discuss with your partner.", s["sub"]))
            elements.append(Spacer(1, 4))
        if tp["show_reading_strategy"]:
            elements.append(_tip_box("Reading Strategy",
                "Before reading, look at the title, pictures and bold words. Try to predict what the text is about. "
                "This helps your brain get ready to understand new information.", icon="TIP"))
            elements.append(Spacer(1, 6))

        # Text box
        tb = Table([[Paragraph(passage.get("text", ""), s["body_j"])]], colWidths=[pw])
        tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_GREEN_L), ("BOX",(0,0),(-1,-1),0.5,C_GREEN),
                                 ("LEFTPADDING",(0,0),(-1,-1),14), ("RIGHTPADDING",(0,0),(-1,-1),14),
                                 ("TOPPADDING",(0,0),(-1,-1),12), ("BOTTOMPADDING",(0,0),(-1,-1),12),
                                 ("ROUNDEDCORNERS",[8,8,8,8])]))
        elements.append(tb)
        elements.append(Spacer(1, 0.4*cm))

        # Questions
        _unit_reading_answers = []
        for qi, q in enumerate(passage.get("questions", [])):
            qtype = q.get("type", "open")
            if qtype == "mcq":
                elements.append(Paragraph(f"<b>{qi+1}.</b>  {q['q']}", s["ex"]))
                for opt in q.get("opts", []):
                    elements.append(Paragraph(f"    {opt}", s["ex_i"]))
                _unit_reading_answers.append(f"R{qi+1}: {q.get('answer', '')}")
            elif qtype == "tf":
                elements.append(Paragraph(f"<b>{qi+1}.</b>  {q['q']}  (   T   /   F   )", s["ex"]))
                _unit_reading_answers.append(f"R{qi+1}: {q.get('answer', '')}")
            else:
                elements.append(Paragraph(f"<b>{qi+1}.</b>  {q['q']}", s["ex"]))
                elements.extend(_lines(q.get("lines", 2)))
            elements.append(Spacer(1, 4))

        elements.append(PageBreak())

        # ─── 4. GRAMMAR FOCUS ───
        elements.append(_pm(f"unit_{_u}_grammar"))
        elements.append(_sec_hdr("GRAMMAR FOCUS", C_PURPLE))
        elements.append(Spacer(1, 6))

        grammar = _get_grammar(grade, ug["unit"], all_struct[0] if all_struct else "")
        elements.append(Paragraph(f'<b>{grammar.get("title", "Grammar")}</b>', s["h2"]))
        elements.append(Spacer(1, 4))

        # Rule box
        formula_text = grammar.get("formula", "").replace("\n", "<br/>")
        rule_txt = (f'<b>RULE:</b> {grammar.get("rule", "")}<br/><br/>'
                    f'<b>FORM:</b><br/><font color="#7c3aed">{formula_text}</font>')
        elements.append(_box(rule_txt, C_PURPLE_L, C_PURPLE))
        elements.append(Spacer(1, 0.3*cm))

        # Examples
        if grammar.get("examples"):
            elements.append(Paragraph("<b>Examples:</b>", s["h3"]))
            for _gex_item in grammar.get("examples", []):
                if isinstance(_gex_item, (list, tuple)):
                    ex_text = _gex_item[0] if _gex_item else ""
                elif isinstance(_gex_item, dict):
                    ex_text = _gex_item.get("sentence", _gex_item.get("example", str(_gex_item)))
                else:
                    ex_text = str(_gex_item)
                elements.append(Paragraph(f"&bull;  <b>{ex_text}</b>", s["ex"]))
            elements.append(Spacer(1, 0.3*cm))

        # Warning box for common mistakes (tier-adapted)
        if tp["show_warning_box"]:
            elements.append(Spacer(1, 0.3*cm))
            elements.append(_warning_box(
                f"Common mistake: Students often confuse the forms. "
                f"Remember to study the FORM box carefully and practise with the exercises below."))
            elements.append(Spacer(1, 0.3*cm))

        # Exercises (tier-adapted count)
        _unit_grammar_answers = []
        if grammar.get("exercises"):
            elements.append(Paragraph("<b>A. Complete the sentences.</b>", s["instr"]))
            for ei, _gex in enumerate(grammar.get("exercises", [])[:tp["grammar_ex_max"]]):
                if isinstance(_gex, (list, tuple)) and len(_gex) >= 2:
                    eq, ans = _gex[0], _gex[1]
                elif isinstance(_gex, dict):
                    eq = _gex.get("q", _gex.get("question", str(_gex)))
                    ans = _gex.get("answer", _gex.get("ans", ""))
                else:
                    eq, ans = str(_gex), ""
                elements.append(Paragraph(f"<b>{ei+1}.</b>  {eq}", s["ex"]))
                elements.append(Spacer(1, 3))
                _unit_grammar_answers.append(f"G{ei+1}: {ans}")

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>B. Write your own sentences using the grammar rule above.</b>", s["instr"]))
        elements.extend(_lines(tp["grammar_write_n"]))

        # Collect answers for answer key
        _answer_key.append({
            "unit": ug["unit"],
            "title": ug["title"],
            "reading": _unit_reading_answers,
            "grammar": _unit_grammar_answers,
        })

        elements.append(PageBreak())

        # ─── 5. LISTENING & SPEAKING ───
        elements.append(_pm(f"unit_{_u}_listening"))
        elements.append(_sec_hdr("LISTENING & SPEAKING", C_ORANGE))
        elements.append(Spacer(1, 6))

        l_desc = s_desc = ""
        for w in weeks:
            sk = w.get("skills", {})
            if sk.get("listening") and not l_desc: l_desc = sk["listening"]
            if sk.get("speaking") and not s_desc: s_desc = sk["speaking"]

        elements.append(Paragraph("<b>A. Listening Task</b>", s["h2"]))
        if l_desc:
            elements.append(_box(f"<b>Task:</b> {l_desc}", C_ORANGE_L, C_ORANGE))
        elements.append(Spacer(1, 4))

        # Get listening script data
        _ls_data = _LISTENING_SCRIPT_BANK.get(grade, {}).get(ug["unit"], None)

        # QR code + audio instruction
        qr_row = Table([
            [_qr_placeholder(f"Listening Unit {ug['unit']}", qr_type="listening", unit_num=ug["unit"]),
             Paragraph("<b>Listen and complete the notes.</b><br/>"
                        '<font size="8" color="#64748b">Scan the QR code to listen to the audio. '
                        'Audio script is available in the Appendix.</font>', s["instr"])],
        ], colWidths=[5.5*cm, pw - 5.5*cm])
        qr_row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(1,0),(1,0),10)]))
        elements.append(qr_row)
        elements.append(Spacer(1, 4))

        # Listening script preview (first portion)
        if _ls_data and isinstance(_ls_data, dict):
            elements.append(Paragraph(f'<b>{_ls_data.get("title", "Listening Script")}</b>', s["h3"]))
            elements.append(Spacer(1, 3))
            # Show script in a styled box
            script_text = _ls_data.get("script", "").replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
            ls_box = Table([[Paragraph(script_text, s["body_s"])]], colWidths=[pw])
            ls_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), C_ORANGE_L),
                ("BOX",(0,0),(-1,-1), 0.5, C_ORANGE),
                ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),12),
                ("TOPPADDING",(0,0),(-1,-1),10), ("BOTTOMPADDING",(0,0),(-1,-1),10),
                ("ROUNDEDCORNERS",[8,8,8,8]),
            ]))
            elements.append(ls_box)
            elements.append(Spacer(1, 6))

            # Tasks
            _ls_tasks = _ls_data.get("tasks", [])
            if not _ls_tasks:
                # Fallback: extract from questions list
                for lq in _ls_data.get("questions", []):
                    if isinstance(lq, dict):
                        _ls_tasks.append(lq.get("question", lq.get("q", str(lq))))
                    else:
                        _ls_tasks.append(str(lq))
            elements.append(Paragraph("<b>Comprehension Tasks:</b>", s["h3"]))
            for task in _ls_tasks:
                elements.append(Paragraph(str(task), s["ex"]))
                elements.extend(_lines(1))
                elements.append(Spacer(1, 2))
        else:
            # Fallback note-taking table
            lt_rows = [[Paragraph("<b>Key Information</b>", s["cell_w"]),
                         Paragraph("<b>Details</b>", s["cell_w"]),
                         Paragraph("<b>Your Notes</b>", s["cell_w"])]]
            for i in range(4):
                lt_rows.append([Paragraph(f"{i+1}. _______", s["cell"]),
                               Paragraph("_______", s["cell"]),
                               Paragraph("_______", s["cell"])])
            lt = Table(lt_rows, colWidths=[pw/3]*3)
            lt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_ORANGE), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                                     ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),6),
                                     ("BOTTOMPADDING",(0,0),(-1,-1),6), ("LEFTPADDING",(0,0),(-1,-1),6)]))
            elements.append(lt)

        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph("<b>B. Speaking Practice</b>", s["h2"]))
        if s_desc:
            elements.append(_box(f"<b>Task:</b> {s_desc}", C_ORANGE_L, C_ORANGE))
        elements.append(Spacer(1, 4))

        # Dialogue framework
        structure = all_struct[0] if all_struct else ""
        parts = [p.strip() for p in structure.split(".") if p.strip()][:4]
        if parts:
            elements.append(Paragraph("<b>Practise the dialogue with a partner:</b>", s["instr"]))
            for di, part in enumerate(parts):
                sp = "A" if di % 2 == 0 else "B"
                elements.append(Paragraph(f"<b>{sp}:</b>  {part}.", s["ex"]))
            elements.append(Spacer(1, 6))

        elements.append(Paragraph("<b>C. Now create your own dialogue on the same topic.</b>", s["instr"]))
        _dlg_lines = tp["speak_lines"] if tp["speak_lines"] % 2 == 0 else tp["speak_lines"] + 1
        for di in range(_dlg_lines):
            sp = "A" if di % 2 == 0 else "B"
            elements.append(Paragraph(f"<b>{sp}:</b>  " + "_" * 65, s["ex"]))
            elements.append(Spacer(1, 3))

        elements.append(PageBreak())

        # ─── 6. WRITING WORKSHOP ───
        elements.append(_pm(f"unit_{_u}_writing"))
        elements.append(_sec_hdr("WRITING WORKSHOP", C_TEAL))
        elements.append(Spacer(1, 6))

        w_desc = ""
        for w in weeks:
            sk = w.get("skills", {})
            if sk.get("writing") and not w_desc: w_desc = sk["writing"]

        elements.append(Paragraph("<b>A. Writing Task</b>", s["h2"]))
        if w_desc:
            elements.append(_box(f"<b>Task:</b> {w_desc}", C_TEAL_L, C_TEAL))
        elements.append(Spacer(1, 4))

        # Model text from bank
        _mw_data = _MODEL_WRITING_BANK.get(grade, {}).get(ug["unit"], None)
        if _mw_data:
            elements.append(Paragraph(f'<b>Model Text ({_mw_data.get("type", "Text")}): {_mw_data.get("title", _mw_data.get("topic", ""))}</b>', s["h3"]))
            elements.append(Spacer(1, 3))
            _mw_txt = _mw_data.get("text") or _mw_data.get("model", "")
            model_text = _mw_txt.replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
            mw_box = Table([[Paragraph(model_text, s["body_j"])]], colWidths=[pw])
            mw_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), C_TEAL_L),
                ("BOX",(0,0),(-1,-1), 0.5, C_TEAL),
                ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),12),
                ("TOPPADDING",(0,0),(-1,-1),10), ("BOTTOMPADDING",(0,0),(-1,-1),10),
                ("ROUNDEDCORNERS",[8,8,8,8]),
            ]))
            elements.append(mw_box)
            elements.append(Spacer(1, 4))
            # Focus note
            _mw_focus = _mw_data.get("focus", "")
            if not _mw_focus and _mw_data.get("key_features"):
                _mw_focus = ", ".join(_mw_data["key_features"]) if isinstance(_mw_data["key_features"], list) else str(_mw_data["key_features"])
            if _mw_focus:
                elements.append(_tip_box("Writing Focus", _mw_focus, icon="TIP"))
            elements.append(Spacer(1, 6))

        # Word bank
        wb_words = unique_vocab[:min(12, len(unique_vocab))]
        if wb_words:
            elements.append(Paragraph("<b>Word Bank:</b>", s["h3"]))
            wb_text = "  |  ".join(wb_words)
            wbb = Table([[Paragraph(wb_text, ParagraphStyle("wbt", fontName=font_name, fontSize=9,
                                                              leading=12, textColor=C_TEAL, alignment=TA_CENTER))]], colWidths=[pw])
            wbb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_TEAL_L), ("BOX",(0,0),(-1,-1),0.3,C_TEAL),
                                      ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
                                      ("ROUNDEDCORNERS",[6,6,6,6])]))
            elements.append(wbb)

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>B. Plan your writing:</b>", s["instr"]))
        plan_rows = [
            [Paragraph("<b>Introduction</b>", s["cell_w"]), Paragraph("_" * 55, s["cell"])],
            [Paragraph("<b>Body</b>", s["cell_w"]), Paragraph("_" * 55, s["cell"])],
            [Paragraph("<b>Conclusion</b>", s["cell_w"]), Paragraph("_" * 55, s["cell"])],
        ]
        pln = Table(plan_rows, colWidths=[2.2*cm, pw-2.2*cm])
        pln.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),C_TEAL), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                                  ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),8),
                                  ("BOTTOMPADDING",(0,0),(-1,-1),8), ("LEFTPADDING",(0,0),(-1,-1),6)]))
        elements.append(pln)

        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph("<b>C. Write your text here:</b>", s["instr"]))
        elements.append(Paragraph("<b>Title:</b>  " + "_" * 65, s["ex"]))
        elements.append(Spacer(1, 6))
        _write_line_count = {
            "preschool": 6, "primary_lower": 8, "primary_upper": 10,
            "middle": 14, "high": 16,
        }.get(_tier_name, 14)
        elements.extend(_lines(_write_line_count))

        elements.append(Spacer(1, 0.3*cm))
        # Checklist
        elements.append(Paragraph("<b>D. Writing Checklist:</b>", s["h3"]))
        checks = ["I used capital letters and full stops correctly.",
                   "I used vocabulary from the Word Bank.",
                   "My sentences are clear and well-organised.",
                   "I included an introduction and conclusion.",
                   "I checked my spelling and grammar."]
        for ch in checks:
            elements.append(Paragraph(f"[   ]  {ch}", s["ex"]))

        elements.append(PageBreak())

        # ─── 6b. PRONUNCIATION CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_pronunciation"))
        _pron_data = _PRONUNCIATION_BANK.get(grade, {}).get(ug["unit"], None) if "pronunciation" in _tier_sections else None
        if _pron_data:
            elements.append(_sec_hdr("PRONUNCIATION CORNER", C_PINK))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>Focus: {_pron_data.get("focus", "Pronunciation")}</b>', s["h2"]))
            elements.append(Spacer(1, 4))

            # Rule box
            _pron_rule = _pron_data.get("rule") or _pron_data.get("explanation", "")
            if _pron_rule:
                elements.append(_tip_box("Rule", _pron_rule, icon="TIP"))
                elements.append(Spacer(1, 6))

            # Examples table
            elements.append(Paragraph("<b>A. Listen and repeat:</b>", s["h3"]))
            _pron_examples = _pron_data.get("examples", [])
            pron_rows = []
            if _pron_examples and isinstance(_pron_examples[0], (list, tuple)):
                # Tuple format: [(sound_a, sound_b), ...]
                pron_rows.append([Paragraph("<b>Sound A</b>", s["cell_w"]),
                                  Paragraph("<b>Sound B</b>", s["cell_w"])])
                for ex_a, ex_b in _pron_examples:
                    pron_rows.append([Paragraph(ex_a, s["cell"]), Paragraph(ex_b, s["cell"])])
            else:
                # String list format: ["example1", "example2", ...]
                pron_rows.append([Paragraph("<b>Example</b>", s["cell_w"]),
                                  Paragraph("<b>Pattern</b>", s["cell_w"])])
                for _pe in _pron_examples:
                    pron_rows.append([Paragraph(str(_pe), s["cell"]), Paragraph("", s["cell"])])
            prt = Table(pron_rows, colWidths=[pw/2]*2)
            prt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0), C_PINK), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),5),
                ("BOTTOMPADDING",(0,0),(-1,-1),5), ("LEFTPADDING",(0,0),(-1,-1),8),
                ("BACKGROUND",(0,1),(-1,-1), C_PINK_L),
            ]))
            elements.append(prt)
            elements.append(Spacer(1, 6))

            # Practice words
            elements.append(Paragraph("<b>B. Practise these words — circle the correct sound:</b>", s["h3"]))
            _prac_words = _pron_data.get("practice") or _pron_data.get("practice_words", [])
            prac_text = "  |  ".join(_prac_words) if _prac_words else ""
            prac_box = Table([[Paragraph(prac_text, ParagraphStyle("prb", fontName=font_name, fontSize=10,
                                                                     leading=14, textColor=C_PINK, alignment=TA_CENTER))]], colWidths=[pw])
            prac_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_PINK_L), ("BOX",(0,0),(-1,-1),0.3,C_PINK),
                                           ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
                                           ("ROUNDEDCORNERS",[6,6,6,6])]))
            elements.append(prac_box)
            elements.append(Spacer(1, 6))

            # Tongue twister
            elements.append(Paragraph("<b>C. Tongue Twister — say it fast!</b>", s["h3"]))
            tt_box = Table([[Paragraph(f'<i>"{_pron_data.get("tongue_twister", "")}"</i>',
                            ParagraphStyle("tt", fontName=font_name, fontSize=11, leading=16,
                                           textColor=C_NAVY, alignment=TA_CENTER))]], colWidths=[pw])
            tt_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), rl_colors.HexColor("#fdf2f8")),
                ("BOX",(0,0),(-1,-1), 0.8, C_PINK),
                ("TOPPADDING",(0,0),(-1,-1),12), ("BOTTOMPADDING",(0,0),(-1,-1),12),
                ("LEFTPADDING",(0,0),(-1,-1),16), ("RIGHTPADDING",(0,0),(-1,-1),16),
                ("ROUNDEDCORNERS",[10,10,10,10]),
            ]))
            elements.append(tt_box)
            elements.append(Spacer(1, 6))

        elements.append(PageBreak())

        # ─── 7. REVIEW & SELF-ASSESSMENT ───
        elements.append(_pm(f"unit_{_u}_review"))
        elements.append(_sec_hdr("REVIEW & SELF-ASSESSMENT", C_RED))
        elements.append(Spacer(1, 6))

        # Can-do statements
        elements.append(Paragraph("<b>A. How well can you do these things now?</b>", s["h2"]))
        elements.append(Spacer(1, 4))

        can_do = []
        for w in weeks:
            sk = w.get("skills", {})
            for key in ["listening", "speaking", "reading", "writing"]:
                d = sk.get(key, "")
                if d and d not in can_do and len(can_do) < tp["review_cando"]:
                    can_do.append(d)

        assess_rows = [[Paragraph("<b>I can...</b>", s["cell_w"]),
                        Paragraph("<b>Excellent</b>", s["cell_w"]),
                        Paragraph("<b>Good</b>", s["cell_w"]),
                        Paragraph("<b>Needs Work</b>", s["cell_w"])]]
        for cd in can_do:
            assess_rows.append([Paragraph(cd, s["cell_s"]), Paragraph("", s["cell"]),
                               Paragraph("", s["cell"]), Paragraph("", s["cell"])])
        at = Table(assess_rows, colWidths=[pw*0.52, pw*0.16, pw*0.16, pw*0.16])
        at.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_RED), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                                 ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),5),
                                 ("BOTTOMPADDING",(0,0),(-1,-1),5), ("LEFTPADDING",(0,0),(-1,-1),6)]))
        elements.append(at)

        elements.append(Spacer(1, 0.4*cm))

        # Vocabulary review
        elements.append(Paragraph("<b>B. Vocabulary Review — Write the meaning of these words:</b>", s["h3"]))
        rev = unique_vocab[:min(10, len(unique_vocab))]
        rev_rows = []
        for ri in range(0, len(rev), 2):
            row = []
            for ci in range(2):
                if ri+ci < len(rev):
                    row.append(Paragraph(f'<b>{rev[ri+ci]}</b> = _______________', s["cell"]))
                else:
                    row.append("")
            rev_rows.append(row)
        if rev_rows:
            rt = Table(rev_rows, colWidths=[pw/2]*2)
            rt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),6),
                                     ("BOTTOMPADDING",(0,0),(-1,-1),6), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                                     ("BACKGROUND",(0,0),(-1,-1),C_RED_L)]))
            elements.append(rt)

        elements.append(Spacer(1, 0.4*cm))

        # Reflection
        elements.append(Paragraph("<b>C. Reflection:</b>", s["h3"]))
        elements.append(Paragraph("What did you learn in this unit? What was the most interesting part?", s["body"]))
        elements.extend(_lines(4))

        elements.append(Spacer(1, 0.3*cm))
        # Notes box
        elements.append(Paragraph("<b>My Notes:</b>", s["h3"]))
        nb = Table([[Paragraph("", s["body"])]], colWidths=[pw], rowHeights=[2*cm])
        nb.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,C_BORDER), ("BACKGROUND",(0,0),(-1,-1),C_LIGHT),
                                 ("ROUNDEDCORNERS",[8,8,8,8])]))
        elements.append(nb)

        # ─── 7b. SEL CORNER ─── (tier-filtered)
        _sel = _SEL_BANK.get(grade, {}).get(ug["unit"], None) if "sel" in _tier_sections else None
        if _sel:
            sel_color = rl_colors.HexColor("#be185d")
            sel_bg = rl_colors.HexColor("#fce7f3")
            elements.append(Spacer(1, 0.4*cm))
            elements.append(_sec_hdr(f'HOW DO YOU FEEL? — {_sel.get("emotion", "")}', sel_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{_sel.get("prompt", "")}</b>', s["instr"]))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f'{_sel.get("activity", "")}', s["body"]))
            elements.extend(_lines(3))
            elements.append(Spacer(1, 6))
            # Mindfulness box
            mind_box = Table([[Paragraph(f'<b>Mindfulness Minute:</b> {_sel.get("mindfulness", "")}',
                              s["body_s"])]], colWidths=[pw])
            mind_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), sel_bg),
                ("BOX",(0,0),(-1,-1),0.5, sel_color), ("LEFTPADDING",(0,0),(-1,-1),12),
                ("RIGHTPADDING",(0,0),(-1,-1),12), ("TOPPADDING",(0,0),(-1,-1),8),
                ("BOTTOMPADDING",(0,0),(-1,-1),8), ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(mind_box)
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f'<b>Discuss:</b> {_sel.get("discussion", "")}', s["body_s"]))

        elements.append(PageBreak())

        # ─── 8. DIALOGUE CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_dialogue"))
        dlg = _DIALOGUE_BANK.get(grade, {}).get(ug["unit"], None) if "dialogue" in _tier_sections else None
        if dlg:
            elements.append(_sec_hdr("DIALOGUE CORNER", C_BLUE_D))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{dlg.get("title", dlg.get("setting", "Dialogue"))}</b>', s["h2"]))
            elements.append(Paragraph(f'<i>Setting: {dlg.get("setting", dlg.get("context", ""))}</i>', s["sub"]))
            elements.append(Spacer(1, 6))
            # Illustration placeholder
            elements.append(_illustration_area(f'Dialogue scene: {dlg.get("setting", "")}', height=2*cm))
            elements.append(Spacer(1, 6))
            # Dialogue lines in styled table
            dlg_rows = []
            raw_lines = dlg.get("lines") or dlg.get("dialogue") or []
            for dlg_item in raw_lines:
                if isinstance(dlg_item, dict):
                    speaker = dlg_item.get("speaker", dlg_item.get("character", ""))
                    line = dlg_item.get("line", dlg_item.get("text", ""))
                elif isinstance(dlg_item, (list, tuple)) and len(dlg_item) >= 2:
                    speaker, line = dlg_item[0], dlg_item[1]
                else:
                    speaker, line = "", str(dlg_item)
                dlg_rows.append([
                    Paragraph(f'<b>{speaker}:</b>', s["dlg_name"]),
                    Paragraph(str(line), s["dlg_line"]),
                ])
            if not dlg_rows:
                dlg_rows = [[Paragraph("<i>No dialogue lines available.</i>", s["body"]), Paragraph("", s["body"])]]
            dt = Table(dlg_rows, colWidths=[2.8*cm, pw - 2.8*cm])
            dt.setStyle(TableStyle([
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5),
                ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
                ("LINEBELOW",(0,0),(-1,-2),0.3,C_BORDER),
                ("BACKGROUND",(0,0),(-1,-1),rl_colors.HexColor("#eff6ff")),
                ("ROUNDEDCORNERS",[6,6,6,6]),
            ]))
            elements.append(dt)
            elements.append(Spacer(1, 8))
            elements.append(Paragraph(f'<b>Your Turn:</b> {dlg.get("task", "")}', s["instr"]))
            elements.extend(_lines(6))
            elements.append(Spacer(1, 0.3*cm))
            elements.append(_tip_box("Speaking Tip",
                "When practising dialogues, use natural intonation. "
                "Questions go UP at the end, statements go DOWN.", icon="TIP"))

        # ─── 9. SONG & RHYME ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_song"))
        song = _SONG_BANK.get(grade, {}).get(ug["unit"], None) if "song" in _tier_sections else None
        if song:
            elements.append(Spacer(1, 0.5*cm))
            song_color = C_PINK
            _song_type = song.get("type", "Song")
            elements.append(_sec_hdr(f'SONG & RHYME: {_song_type.upper()}', song_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{song.get("title", "Song")}</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            # QR for audio
            qr_song = Table([
                [_qr_placeholder(f"Song Unit {ug['unit']}", qr_type="song", unit_num=ug["unit"]),
                 Paragraph(f'<i>Scan to listen to the {_song_type.lower()}</i>', s["sub"])],
            ], colWidths=[5.5*cm, pw - 5.5*cm])
            qr_song.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(1,0),(1,0),10)]))
            elements.append(qr_song)
            elements.append(Spacer(1, 6))
            # Lyrics box
            lyrics_lines = song.get("lyrics", "").replace("\n", "<br/>")
            lyrics_box = Table([[Paragraph(lyrics_lines, s["song"])]], colWidths=[pw])
            lyrics_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), C_PINK_L),
                ("BOX",(0,0),(-1,-1), 0.8, song_color),
                ("LEFTPADDING",(0,0),(-1,-1),20), ("RIGHTPADDING",(0,0),(-1,-1),20),
                ("TOPPADDING",(0,0),(-1,-1),14), ("BOTTOMPADDING",(0,0),(-1,-1),14),
                ("ROUNDEDCORNERS",[10,10,10,10]),
            ]))
            elements.append(lyrics_box)
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>Activity:</b> {song.get("activity", "")}', s["instr"]))

        elements.append(PageBreak())

        # ─── 10. CULTURE CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_culture"))
        culture = _CULTURE_CORNER_BANK.get(grade, {}).get(ug["unit"], None) if "culture" in _tier_sections else None
        if culture:
            cc_color = rl_colors.HexColor("#0369a1")
            cc_bg = rl_colors.HexColor("#e0f2fe")
            elements.append(_sec_hdr("CULTURE CORNER", cc_color))
            elements.append(Spacer(1, 6))
            _cc_title = culture.get("title", "Culture Corner")
            _cc_text = culture.get("text") or culture.get("content", "")
            elements.append(Paragraph(f'<b>{_cc_title}</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            # Illustration
            elements.append(_illustration_area(f'Culture: {_cc_title}', height=tp["illust_h"]*cm))
            elements.append(Spacer(1, 6))
            # Text
            ct_box = Table([[Paragraph(_cc_text, s["body_j"])]], colWidths=[pw])
            ct_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), cc_bg),
                ("BOX",(0,0),(-1,-1), 0.5, cc_color),
                ("LEFTPADDING",(0,0),(-1,-1),14), ("RIGHTPADDING",(0,0),(-1,-1),14),
                ("TOPPADDING",(0,0),(-1,-1),12), ("BOTTOMPADDING",(0,0),(-1,-1),12),
                ("ROUNDEDCORNERS",[8,8,8,8]),
            ]))
            elements.append(ct_box)
            elements.append(Spacer(1, 8))
            # Countries
            if culture.get("country_flag"):
                elements.append(Paragraph(f'<b>Countries mentioned:</b> {culture["country_flag"]}', s["sub"]))
            elements.append(Spacer(1, 6))
            # Question
            _cc_q = culture.get("question", "")
            if not _cc_q and culture.get("discussion_questions"):
                dqs = culture["discussion_questions"]
                _cc_q = dqs[0] if isinstance(dqs, list) and dqs else str(dqs)
            if _cc_q:
                elements.append(Paragraph(f'<b>Think &amp; Write:</b> {_cc_q}', s["instr"]))
            elements.extend(_lines(5))

        # ─── 10b. TURKEY CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_turkey"))
        _turkey = _TURKEY_CORNER_BANK.get(grade, {}).get(ug["unit"], None) if "turkey" in _tier_sections else None
        if _turkey:
            tc_color = rl_colors.HexColor("#dc2626")
            tc_bg = rl_colors.HexColor("#fef2f2")
            elements.append(Spacer(1, 0.5*cm))
            elements.append(_sec_hdr("TURKEY CORNER", tc_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{_turkey.get("title", "Turkey Corner")}</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            # Illustration
            elements.append(_illustration_area(f'Turkey: {_turkey.get("title", "Turkey Corner")}', height=tp["illust_h"]*cm))
            elements.append(Spacer(1, 4))
            # Text
            tc_box = Table([[Paragraph(_turkey.get("text", ""), s["body_j"])]], colWidths=[pw])
            tc_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), tc_bg),
                ("BOX",(0,0),(-1,-1), 0.5, tc_color), ("LEFTPADDING",(0,0),(-1,-1),12),
                ("RIGHTPADDING",(0,0),(-1,-1),12), ("TOPPADDING",(0,0),(-1,-1),10),
                ("BOTTOMPADDING",(0,0),(-1,-1),10), ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(tc_box)
            elements.append(Spacer(1, 6))
            # Famous person
            if _turkey.get("famous_person"):
                elements.append(_tip_box("Famous Turk", _turkey["famous_person"], icon="TIP"))
                elements.append(Spacer(1, 4))
            # Recipe
            if _turkey.get("recipe"):
                rec = _turkey["recipe"]
                elements.append(Paragraph(f'<b>Recipe: {rec["name"]}</b>', s["h3"]))
                for ri, step in enumerate(rec["steps"]):
                    elements.append(Paragraph(f"<b>Step {ri+1}:</b> {step}", s["ex"]))
                elements.append(Spacer(1, 4))
            # Activity / Discussion
            _tc_activity = _turkey.get("activity") or _turkey.get("discussion_q", "")
            if _tc_activity:
                elements.append(Paragraph(f'<b>Your Turn:</b> {_tc_activity}', s["instr"]))
            elements.extend(_lines(4))

        # ─── 11. PROJECT WORK ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_project"))
        project = _PROJECT_BANK.get(grade, {}).get(ug["unit"], None) if "project" in _tier_sections else None
        if project:
            elements.append(Spacer(1, 0.5*cm))
            elements.append(_sec_hdr("PROJECT WORK", C_GOLD))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{project.get("title", "Project")}</b>', s["h2"]))
            elements.append(Paragraph(f'{project.get("desc", project.get("description", ""))}', s["body"]))
            elements.append(Spacer(1, 6))
            # Steps
            elements.append(Paragraph("<b>Steps:</b>", s["h3"]))
            for si, step in enumerate(project.get("steps", [])):
                elements.append(Paragraph(f"<b>Step {si+1}:</b> {step}", s["ex"]))
                elements.append(Spacer(1, 2))
            # Materials / Outcomes
            _proj_mat = project.get("materials") or ", ".join(project.get("outcomes", []))
            if _proj_mat:
                elements.append(Spacer(1, 6))
                elements.append(_warning_box(f"Materials needed: {_proj_mat}"))
            elements.append(Spacer(1, 6))
            # Project notes area
            elements.append(Paragraph("<b>My Project Notes:</b>", s["h3"]))
            pn = Table([[Paragraph("", s["body"])]], colWidths=[pw], rowHeights=[tp["project_notes_h"]*cm])
            pn.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,C_BORDER), ("BACKGROUND",(0,0),(-1,-1),C_LIGHT),
                                     ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(pn)

        # ─── 11b. STEAM BRIDGE ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_steam"))
        _steam = _STEAM_BANK.get(grade, {}).get(ug["unit"], None) if "steam" in _tier_sections else None
        if _steam:
            stm_color = rl_colors.HexColor("#0369a1")
            stm_bg = rl_colors.HexColor("#e0f2fe")
            elements.append(Spacer(1, 0.4*cm))
            _stm_subj = _steam.get("subject") or _steam.get("subject_link", "STEAM")
            elements.append(_sec_hdr(f'STEAM BRIDGE: {_stm_subj.upper()} + ENGLISH', stm_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{_steam.get("title", "STEAM Activity")}</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            # Task
            _stm_task = _steam.get("task") or _steam.get("activity", "")
            task_box = Table([[Paragraph(_stm_task, s["body_j"])]], colWidths=[pw])
            task_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), stm_bg),
                ("BOX",(0,0),(-1,-1),0.5, stm_color), ("LEFTPADDING",(0,0),(-1,-1),12),
                ("RIGHTPADDING",(0,0),(-1,-1),12), ("TOPPADDING",(0,0),(-1,-1),10),
                ("BOTTOMPADDING",(0,0),(-1,-1),10), ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(task_box)
            elements.append(Spacer(1, 4))
            # STEAM Vocab / Materials
            _stm_vocab = _steam.get("vocab") or _steam.get("materials", [])
            if _stm_vocab:
                stm_voc = "  |  ".join(_stm_vocab) if isinstance(_stm_vocab, list) else str(_stm_vocab)
                elements.append(Paragraph(f'<b>STEAM Vocabulary:</b> {stm_voc}', s["body_s"]))
            elements.append(Spacer(1, 4))
            # Work area
            elements.extend(_lines(5))

        elements.append(PageBreak())

        # ─── 12. DIGITAL RESOURCES — QR Code Grid ─── (always included)
        elements.append(_sec_hdr("DIGITAL RESOURCES", rl_colors.HexColor("#4f46e5")))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            "<b>Scan the QR codes below to access interactive activities, "
            "listening exercises, reading materials, games and more on SmartCampus.</b>", s["body_s"]))
        elements.append(Spacer(1, 6))
        elements.append(_qr_grid(ug["unit"]))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            '<font size="7.5" color="#64748b">'
            'Each QR code links to the corresponding section in the SmartCampus platform. '
            'Listening = audio activities | Speaking = dialogue practice | Reading = texts &amp; exercises | '
            'Grammar = interactive grammar | Vocabulary = word games | Books = digital flipbooks | '
            'Resources = external learning sites | Games = interactive language games'
            '</font>', s["sub"]))

        # ─── 13. WORKBOOK — Extra Exercises ─── (tier-filtered)
        _wb_data = _WORKBOOK_BANK.get(grade, {}).get(ug["unit"], None) if "workbook" in _tier_sections else None
        if _wb_data:
            elements.append(Spacer(1, 0.5*cm))
            wb_color = rl_colors.HexColor("#4338ca")
            wb_bg = rl_colors.HexColor("#e0e7ff")
            elements.append(_sec_hdr("WORKBOOK — Extra Exercises", wb_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>Unit {ug["unit"]}: {ug["title"]} — Practice Makes Perfect!</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            for ei, ex in enumerate(_wb_data.get("exercises", [])):
                _wb_instr = ex.get("instr") or ex.get("instruction", "")
                elements.append(Paragraph(f'<b>Exercise {ei+1}: {_wb_instr}</b>', s["instr"]))
                elements.append(Spacer(1, 3))
                for item in ex.get("items", []):
                    elements.append(Paragraph(f"• {item}", s["ex"]))
                    if ex.get("type", "") in ("write", "complete"):
                        elements.extend(_lines(2))
                    else:
                        elements.extend(_lines(1))
                    elements.append(Spacer(1, 2))
                elements.append(Spacer(1, 6))

        # ─── 14. COMIC STRIP ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_comic"))
        _comic = _COMIC_STRIP_BANK.get(grade, {}).get(ug["unit"], None) if "comic" in _tier_sections else None
        if _comic:
            cm_color = rl_colors.HexColor("#ea580c")
            cm_bg = rl_colors.HexColor("#fff7ed")
            elements.append(Spacer(1, 0.4*cm))
            _cm_gp = _comic.get("grammar_point") or _comic.get("language_focus", "")
            elements.append(_sec_hdr(f'COMIC STRIP: {_cm_gp.upper()}', cm_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>{_comic.get("title", "Comic Strip")}</b>', s["h2"]))
            elements.append(Spacer(1, 4))
            # Panels as grid
            for pi, panel in enumerate(_comic.get("panels", [])):
                if isinstance(panel, dict):
                    _pn_scene = panel.get("scene", "")
                    _pn_speech = panel.get("speech") or panel.get("dialogue", "")
                    _pn_thought = panel.get("thought", "")
                elif isinstance(panel, str):
                    _pn_scene, _pn_speech, _pn_thought = panel, "", ""
                else:
                    _pn_scene, _pn_speech, _pn_thought = str(panel), "", ""
                panel_data = [
                    [Paragraph(f'<b>Panel {pi+1}</b>', s["cell_w"]),
                     Paragraph(f'<i>[{_pn_scene}]</i>', s["cell_s"])],
                ]
                pt = Table(panel_data, colWidths=[2*cm, pw-2*cm])
                pt.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0), cm_color),
                    ("BACKGROUND",(1,0),(1,0), cm_bg), ("BOX",(0,0),(-1,-1),0.5,cm_color),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),5),
                    ("BOTTOMPADDING",(0,0),(-1,-1),5), ("LEFTPADDING",(0,0),(-1,-1),6)]))
                elements.append(pt)
                # Speech/Thought
                if _pn_speech:
                    elements.append(Paragraph(_pn_speech, s["ex"]))
                if _pn_thought:
                    elements.append(Paragraph(f'<i>{_pn_thought}</i>', s["ex_i"]))
                elements.append(Spacer(1, 3))
            elements.append(Spacer(1, 4))
            _cm_yt = _comic.get("your_turn") or _comic.get("drawing_task", "Draw your own comic strip!")
            elements.append(Paragraph(f'<b>Your Turn:</b> {_cm_yt}', s["instr"]))
            # Draw area
            draw_box = Table([[Paragraph("", s["body"])]], colWidths=[pw], rowHeights=[3*cm])
            draw_box.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.5,cm_color),
                ("BACKGROUND",(0,0),(-1,-1),C_LIGHT), ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(draw_box)

        elements.append(PageBreak())

        # ─── 15. REAL-WORLD MISSION ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_mission"))
        _mission = _MISSION_BANK.get(grade, {}).get(ug["unit"], None) if "mission" in _tier_sections else None
        if _mission:
            ms_color = rl_colors.HexColor("#059669")
            ms_bg = rl_colors.HexColor("#ecfdf5")
            elements.append(_sec_hdr(f'REAL-WORLD MISSION: {_mission.get("title", "Mission").upper()}', ms_color))
            elements.append(Spacer(1, 6))
            # Mission card — normalize keys
            _ms_desc = _mission.get("mission") or _mission.get("objective", "")
            _ms_evidence = _mission.get("evidence", "")
            if not _ms_evidence and _mission.get("tasks"):
                _ms_evidence = ", ".join(_mission["tasks"]) if isinstance(_mission["tasks"], list) else str(_mission["tasks"])
            _ms_diff = _mission.get("difficulty", "")
            _ms_xp = _mission.get("xp", "")
            if not _ms_xp and _mission.get("reward"):
                _ms_xp = _mission["reward"]
            ms_data = [
                [Paragraph("<b>YOUR MISSION</b>", s["cell_w"]), Paragraph(_ms_desc, s["body"])],
                [Paragraph("<b>EVIDENCE</b>", s["cell_w"]), Paragraph(_ms_evidence, s["body_s"])],
                [Paragraph("<b>DIFFICULTY</b>", s["cell_w"]), Paragraph(str(_ms_diff), s["body_s"])],
                [Paragraph("<b>XP REWARD</b>", s["cell_w"]), Paragraph(f'+{_ms_xp} XP' if _ms_xp else '', s["body_s"])],
            ]
            mst = Table(ms_data, colWidths=[2.5*cm, pw-2.5*cm])
            mst.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1), ms_color),
                ("BACKGROUND",(1,0),(1,-1), ms_bg), ("GRID",(0,0),(-1,-1),0.5,C_BORDER),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),6),
                ("BOTTOMPADDING",(0,0),(-1,-1),6), ("LEFTPADDING",(0,0),(-1,-1),8),
                ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(mst)
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("<b>Mission completed?</b>  [   ] YES  [   ] NO    Date: ___/___/______", s["instr"]))
            elements.append(Spacer(1, 4))

        # ─── 16. FAMILY CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_family"))
        _family = _FAMILY_CORNER_BANK.get(grade, {}).get(ug["unit"], None) if "family" in _tier_sections else None
        if _family:
            fc_color = rl_colors.HexColor("#9333ea")
            fc_bg = rl_colors.HexColor("#faf5ff")
            elements.append(Spacer(1, 0.4*cm))
            elements.append(_sec_hdr(f'FAMILY CORNER: {_family.get("title", "Family Corner").upper()}', fc_color))
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<b>Home Activity:</b> {_family.get("activity", "")}', s["body"]))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f'<b>Together:</b> {_family.get("together", "")}', s["body"]))
            elements.append(Spacer(1, 4))
            # Parent question box
            pq_box = Table([[Paragraph(f'{_family.get("parent_question", "")}', s["body_s"])]], colWidths=[pw])
            pq_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), fc_bg),
                ("BOX",(0,0),(-1,-1),0.5, fc_color), ("LEFTPADDING",(0,0),(-1,-1),12),
                ("RIGHTPADDING",(0,0),(-1,-1),12), ("TOPPADDING",(0,0),(-1,-1),8),
                ("BOTTOMPADDING",(0,0),(-1,-1),8), ("ROUNDEDCORNERS",[8,8,8,8])]))
            elements.append(pq_box)
            elements.append(Spacer(1, 6))
            # Parent signature
            elements.append(Paragraph("<b>Parent Signature:</b> _____________________    Date: ___/___/______", s["body_s"]))
            elements.append(Spacer(1, 4))

        # ─── 17. PODCAST CORNER ─── (tier-filtered)
        elements.append(_pm(f"unit_{_u}_podcast"))
        _pod = _PODCAST_BANK.get(grade, {}).get(ug["unit"], None) if "podcast" in _tier_sections else None
        if _pod:
            pod_color = rl_colors.HexColor("#7c3aed")
            pod_bg = rl_colors.HexColor("#ede9fe")
            elements.append(Spacer(1, 0.4*cm))
            elements.append(_sec_hdr(f'PODCAST: {_pod.get("title", "Podcast").upper()}', pod_color))
            elements.append(Spacer(1, 6))
            # QR for podcast
            qr_pod = Table([
                [_qr_placeholder(f"Podcast Unit {ug['unit']}", qr_type="listening", unit_num=ug["unit"]),
                 Paragraph(f'<b>Hosts: {_pod.get("host", "")}</b><br/><i>{_pod.get("summary", "")}</i>', s["body_s"])],
            ], colWidths=[5.5*cm, pw - 5.5*cm])
            qr_pod.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING",(1,0),(1,0),10)]))
            elements.append(qr_pod)
            elements.append(Spacer(1, 4))
            # Segments — handle both "segments" (list) and "script" (string)
            _pod_segs = _pod.get("segments", [])
            if not _pod_segs:
                _pod_scr = _pod.get("script", "")
                if _pod_scr and isinstance(_pod_scr, str):
                    _pod_segs = [s.strip() + "." for s in _pod_scr.split(". ")[:6] if s.strip()]
                elif isinstance(_pod_scr, list):
                    _pod_segs = [str(s) for s in _pod_scr[:6]]
            if _pod_segs:
                elements.append(Paragraph("<b>Segments:</b>", s["h3"]))
                for seg in _pod_segs:
                    elements.append(Paragraph(f"&bull; {seg}", s["body_s"]))
                elements.append(Spacer(1, 4))
            # Student task
            _pod_task = _pod.get("student_task", "")
            if _pod_task:
                elements.append(_tip_box("Your Podcast Task", _pod_task, icon="TIP"))
            elements.append(Spacer(1, 4))

        # ─── 18. GAMIFICATION — Achievement Tracker ─── (tier-filtered)
        _badge = _GAMIFICATION_BANK.get(grade, {}).get("unit_badges", {}).get(ug["unit"], None) if "gamification" in _tier_sections else None
        if _badge:
            gm_color = rl_colors.HexColor("#b45309")
            gm_bg = rl_colors.HexColor("#fffbeb")
            elements.append(Spacer(1, 0.4*cm))
            elements.append(_sec_hdr("ACHIEVEMENT UNLOCKED!", gm_color))
            elements.append(Spacer(1, 6))
            # Badge card
            _badge_name = _badge.get("badge") or _badge.get("name", "Badge")
            _badge_xp = _badge.get("xp", 100)
            _badge_desc = _badge.get("desc", "")
            badge_data = [
                [Paragraph(f'<b>Badge: {_badge_name}</b>', s["h2"]),
                 Paragraph(f'+{_badge_xp} XP', ParagraphStyle("xp", fontName=font_bold,
                           fontSize=14, leading=18, textColor=gm_color, alignment=TA_CENTER))],
                [Paragraph(f'<i>Challenge: {_badge_desc}</i>', s["body_s"]),
                 Paragraph("[   ] EARNED", s["instr"])],
            ]
            bgt = Table(badge_data, colWidths=[pw*0.7, pw*0.3])
            bgt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), gm_bg),
                ("BOX",(0,0),(-1,-1),0.8, gm_color), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
                ("LEFTPADDING",(0,0),(-1,-1),10), ("ROUNDEDCORNERS",[10,10,10,10])]))
            elements.append(bgt)
            elements.append(Spacer(1, 4))

            # XP Tracker
            elements.append(Paragraph("<b>My XP Tracker:</b>", s["h3"]))
            xp_rows = [[Paragraph("<b>Activity</b>", s["cell_w"]),
                        Paragraph("<b>XP</b>", s["cell_w"]),
                        Paragraph("<b>Done?</b>", s["cell_w"])]]
            xp_rows.append([Paragraph(f"Unit {ug['unit']} Badge", s["cell"]),
                           Paragraph(f"+{_badge_xp}", s["cell"]),
                           Paragraph("[   ]", s["cell"])])
            _bonus = _GAMIFICATION_BANK.get(grade, {}).get("bonus_xp", [])
            for bx in _bonus[:4]:
                _bx_action = bx.get("action") or bx.get("task", "")
                xp_rows.append([Paragraph(_bx_action, s["cell"]),
                               Paragraph(f"+{bx.get('xp', 50)}", s["cell"]),
                               Paragraph("[   ]", s["cell"])])
            xpt = Table(xp_rows, colWidths=[pw*0.6, pw*0.2, pw*0.2])
            xpt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0), gm_color),
                ("GRID",(0,0),(-1,-1),0.3,C_BORDER), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
                ("LEFTPADDING",(0,0),(-1,-1),6), ("BACKGROUND",(0,1),(-1,-1), gm_bg)]))
            elements.append(xpt)
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f"<b>Total XP this unit:</b> _____ / {_badge_xp + 120}    "
                                      f"<b>Level:</b> _______________", s["body_s"]))

        elements.append(PageBreak())

        # ─── PROGRESS CHECK (after every 3rd unit) ───
        pc = _PROGRESS_CHECK_BANK.get(grade, {}).get(ug["unit"], None)
        if pc:
            pc_color = rl_colors.HexColor("#7e22ce")
            pc_bg = rl_colors.HexColor("#f3e8ff")
            # Two formats: dict with title/vocab/grammar/reading (grade5-8)
            #              or dict with skill/task/criteria (grade9-12, unwrapped from list)
            if isinstance(pc, dict) and "title" in pc:
                # Standard format (grade 5-8)
                elements.append(_sec_hdr(pc["title"].upper(), pc_color))
                elements.append(Spacer(1, 8))
                # Vocabulary section
                elements.append(Paragraph("<b>A. Vocabulary: Complete the sentences.</b>", s["instr"]))
                for vq, _ in pc.get("vocab", []):
                    elements.append(Paragraph(vq, s["ex"]))
                    elements.append(Spacer(1, 2))
                elements.append(Spacer(1, 0.3*cm))
                # Grammar section
                elements.append(Paragraph("<b>B. Grammar: Fill in the blanks.</b>", s["instr"]))
                for gq, _ in pc.get("grammar", []):
                    elements.append(Paragraph(gq, s["ex"]))
                    elements.append(Spacer(1, 2))
                elements.append(Spacer(1, 0.3*cm))
                # Reading section
                if pc.get("reading_text"):
                    elements.append(Paragraph("<b>C. Reading: Read the text and answer.</b>", s["instr"]))
                    pc_tb = Table([[Paragraph(pc["reading_text"], s["body_j"])]], colWidths=[pw])
                    pc_tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),pc_bg),
                                                ("BOX",(0,0),(-1,-1),0.5,pc_color),
                                                ("LEFTPADDING",(0,0),(-1,-1),12), ("RIGHTPADDING",(0,0),(-1,-1),12),
                                                ("TOPPADDING",(0,0),(-1,-1),10), ("BOTTOMPADDING",(0,0),(-1,-1),10),
                                                ("ROUNDEDCORNERS",[8,8,8,8])]))
                    elements.append(pc_tb)
                    elements.append(Spacer(1, 6))
                    for rq, _ in pc.get("reading_qs", []):
                        elements.append(Paragraph(rq, s["ex"]))
                        elements.extend(_lines(1))
                        elements.append(Spacer(1, 2))
                # Score box
                elements.append(Spacer(1, 0.4*cm))
                score_box = Table([[
                    Paragraph("<b>My Score:</b>  _____ / 13", s["h3"]),
                    Paragraph("<b>Date:</b>  ____/____/________", s["h3"]),
                ]], colWidths=[pw/2]*2)
                score_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),pc_bg),
                                                ("BOX",(0,0),(-1,-1),0.5,pc_color),
                                                ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
                                                ("LEFTPADDING",(0,0),(-1,-1),10),
                                                ("ROUNDEDCORNERS",[6,6,6,6])]))
                elements.append(score_box)
            elif isinstance(pc, dict) and "skill" in pc:
                # Skill-based format (grade 9-12, single skill item)
                elements.append(_sec_hdr(f"PROGRESS CHECK — UNIT {ug['unit']}", pc_color))
                elements.append(Spacer(1, 8))
                elements.append(Paragraph(f'<b>{pc["skill"]}</b>', s["h3"]))
                elements.append(Spacer(1, 3))
                elements.append(_box(f'<b>Task:</b> {pc["task"]}', pc_bg, pc_color))
                elements.append(Spacer(1, 4))
                elements.append(Paragraph(f'<b>Criteria:</b> {pc["criteria"]}', s["body_s"]))
                elements.append(Spacer(1, 8))
                # Self-assessment
                sa_rows = [[Paragraph("<b>Skill</b>", s["cell_w"]),
                            Paragraph("<b>Can do well</b>", s["cell_w"]),
                            Paragraph("<b>Need practice</b>", s["cell_w"])]]
                sa_rows.append([Paragraph(pc["skill"], s["cell"]),
                               Paragraph("[   ]", s["cell"]),
                               Paragraph("[   ]", s["cell"])])
                sat = Table(sa_rows, colWidths=[pw*0.5, pw*0.25, pw*0.25])
                sat.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0), pc_color),
                    ("TEXTCOLOR",(0,0),(-1,0), rl_colors.white),
                    ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                    ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
                elements.append(sat)
            elements.append(PageBreak())

        # ─── ESCAPE ROOM (after every 3rd unit) ───
        _escape = _ESCAPE_ROOM_BANK.get(grade, {}).get(ug["unit"], None)
        if _escape:
            er_color = rl_colors.HexColor("#991b1b")
            er_bg = rl_colors.HexColor("#fef2f2")
            elements.append(_sec_hdr(f'ESCAPE ROOM: {_escape.get("title", "Escape Room").upper()}', er_color))
            elements.append(Spacer(1, 6))
            # Story intro
            story_box = Table([[Paragraph(f'<b>{_escape.get("story", "")}</b>', s["body"])]], colWidths=[pw])
            story_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), er_bg),
                ("BOX",(0,0),(-1,-1),0.8, er_color), ("LEFTPADDING",(0,0),(-1,-1),14),
                ("RIGHTPADDING",(0,0),(-1,-1),14), ("TOPPADDING",(0,0),(-1,-1),10),
                ("BOTTOMPADDING",(0,0),(-1,-1),10), ("ROUNDEDCORNERS",[10,10,10,10])]))
            elements.append(story_box)
            elements.append(Spacer(1, 8))
            # Puzzles
            for qi, puzzle in enumerate(_escape.get("puzzles", [])):
                elements.append(Paragraph(f'<b>Puzzle {qi+1} ({puzzle.get("type", "").title()}):</b> {puzzle.get("question", "")}', s["instr"]))
                elements.append(Paragraph(f'<font size="8" color="#64748b">Hint: {puzzle.get("hint", "")}</font>', s["sub"]))
                elements.append(Paragraph("Answer: _____________________", s["ex"]))
                elements.append(Spacer(1, 4))
            # Final code
            elements.append(Spacer(1, 6))
            code_box = Table([[Paragraph(f'<b>FINAL CODE:</b>  _____ — _____ — _____ — _____ — _____', s["h2"])]], colWidths=[pw])
            code_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), er_bg),
                ("BOX",(0,0),(-1,-1),1, er_color), ("TOPPADDING",(0,0),(-1,-1),10),
                ("BOTTOMPADDING",(0,0),(-1,-1),10), ("LEFTPADDING",(0,0),(-1,-1),14),
                ("ROUNDEDCORNERS",[10,10,10,10])]))
            elements.append(code_box)
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f'<b>Reward:</b> {_escape.get("reward", "")}', s["body_s"]))
            elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 1: GLOSSARY
    # ═══════════════════════════════════════════
    _current_unit_title[0] = "Appendix"
    elements.append(Paragraph("APPENDIX", s["appendix_t"]))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(_sec_hdr("GLOSSARY", C_BLUE))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("All key vocabulary from this coursebook, listed alphabetically.", s["sub"]))
    elements.append(Spacer(1, 6))

    # Deduplicate and sort
    _gl_unique = sorted(set(w.strip() for w in _glossary_words if w.strip()), key=str.lower)
    if _gl_unique:
        gl_rows = []
        gcols = 3
        for gi in range(0, len(_gl_unique), gcols):
            row = []
            for ci in range(gcols):
                if gi + ci < len(_gl_unique):
                    row.append(Paragraph(f'{gi+ci+1}. {_gl_unique[gi+ci]}  = __________', s["glossary"]))
                else:
                    row.append("")
            gl_rows.append(row)
        gt = Table(gl_rows, colWidths=[pw/gcols]*gcols)
        gst = [("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3),
               ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),4),
               ("GRID",(0,0),(-1,-1),0.2,C_BORDER)]
        for ri in range(len(gl_rows)):
            gst.append(("BACKGROUND",(0,ri),(-1,ri), C_BLUE_L if ri%2==0 else C_WHITE))
        gt.setStyle(TableStyle(gst))
        elements.append(gt)
    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 2: ANSWER KEY
    # ═══════════════════════════════════════════
    elements.append(_sec_hdr("ANSWER KEY", C_GREEN))
    elements.append(Spacer(1, 6))
    for ak in _answer_key:
        elements.append(Paragraph(f'<b>Unit {ak["unit"]}: {ak["title"]}</b>', s["h3"]))
        if ak["reading"]:
            elements.append(Paragraph(f'<b>Reading:</b> {" | ".join(ak["reading"])}', s["body_s"]))
        if ak["grammar"]:
            elements.append(Paragraph(f'<b>Grammar:</b> {" | ".join(ak["grammar"])}', s["body_s"]))
        elements.append(Spacer(1, 4))
    # Progress check answers
    for pc_unit, pc_data in sorted(_PROGRESS_CHECK_BANK.get(grade, {}).items()):
        if pc_unit not in units_to_gen:
            continue
        if isinstance(pc_data, dict) and "title" in pc_data:
            elements.append(Paragraph(f'<b>{pc_data["title"]}</b>', s["h3"]))
            v_ans = " | ".join(f"V{i+1}: {a}" for i, (_, a) in enumerate(pc_data.get("vocab", [])))
            g_ans = " | ".join(f"G{i+1}: {a}" for i, (_, a) in enumerate(pc_data.get("grammar", [])))
            r_ans = " | ".join(f"R{i+1}: {a}" for i, (_, a) in enumerate(pc_data.get("reading_qs", [])))
            elements.append(Paragraph(f'<b>Vocab:</b> {v_ans}', s["body_s"]))
            elements.append(Paragraph(f'<b>Grammar:</b> {g_ans}', s["body_s"]))
            elements.append(Paragraph(f'<b>Reading:</b> {r_ans}', s["body_s"]))
            elements.append(Spacer(1, 4))
        elif isinstance(pc_data, dict) and "skill" in pc_data:
            elements.append(Paragraph(f'<b>Unit {pc_unit} — {pc_data["skill"]}:</b> See criteria in main text.', s["body_s"]))
            elements.append(Spacer(1, 4))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 3: IRREGULAR VERBS (tier-filtered)
    # ═══════════════════════════════════════════
    if tp["show_irregular_verbs"]:
        elements.append(_sec_hdr("IRREGULAR VERBS", C_PURPLE))
        elements.append(Spacer(1, 6))
        iv_header = [Paragraph("<b>Base Form (V1)</b>", s["cell_w"]),
                     Paragraph("<b>Past Simple (V2)</b>", s["cell_w"]),
                     Paragraph("<b>Past Participle (V3)</b>", s["cell_w"])]
        iv_rows = [iv_header]
        for v1, v2, v3 in _IRREGULAR_VERBS_G5:
            iv_rows.append([Paragraph(v1, s["cell"]), Paragraph(v2, s["cell"]), Paragraph(v3, s["cell"])])
        ivt = Table(iv_rows, colWidths=[pw/3]*3)
        ivst = [("BACKGROUND",(0,0),(-1,0),C_PURPLE), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3),
                ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),6)]
        for ri in range(1, len(iv_rows)):
            ivst.append(("BACKGROUND",(0,ri),(-1,ri), C_PURPLE_L if ri%2==0 else C_WHITE))
        ivt.setStyle(TableStyle(ivst))
        elements.append(ivt)
        elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 4: PHONETIC CHART (tier-filtered)
    # ═══════════════════════════════════════════
    if tp["show_phonetic_chart"]:
        elements.append(_sec_hdr("PHONETIC CHART (IPA)", C_TEAL))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("The International Phonetic Alphabet helps you pronounce English words correctly.", s["sub"]))
        elements.append(Spacer(1, 6))
        for section_name, symbols in _PHONETIC_CHART:
            elements.append(Paragraph(f'<b>{section_name}</b>', s["h3"]))
            ph_rows = []
            for sym, example in symbols:
                ph_rows.append([Paragraph(f'<b>{sym}</b>', s["cell"]), Paragraph(example, s["cell_s"])])
            if ph_rows:
                pht = Table(ph_rows, colWidths=[2*cm, pw - 2*cm])
                phst = [("GRID",(0,0),(-1,-1),0.2,C_BORDER), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                        ("TOPPADDING",(0,0),(-1,-1),3), ("BOTTOMPADDING",(0,0),(-1,-1),3),
                        ("LEFTPADDING",(0,0),(-1,-1),6)]
                for ri in range(len(ph_rows)):
                    phst.append(("BACKGROUND",(0,ri),(-1,ri), C_TEAL_L if ri%2==0 else C_WHITE))
                pht.setStyle(TableStyle(phst))
                elements.append(pht)
                elements.append(Spacer(1, 6))
        elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 5: GRAMMAR SUMMARY (tier-filtered)
    # ═══════════════════════════════════════════
    if tp["show_grammar_summary"]:
        elements.append(_sec_hdr("GRAMMAR SUMMARY", C_PURPLE))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("Quick reference for all grammar topics covered in this book.", s["sub"]))
        elements.append(Spacer(1, 6))
        g_bank = _GRAMMAR_BANK.get(grade, {})
        for g_unit in sorted(g_bank.keys()):
            if g_unit not in units_to_gen:
                continue
            gdata = g_bank[g_unit]
            _gd_title = gdata.get("title") or gdata.get("topic", "Grammar")
            _gd_rule = gdata.get("rule") or gdata.get("explanation", "")
            elements.append(Paragraph(f'<b>Unit {g_unit}: {_gd_title}</b>', s["h3"]))
            formula_text = gdata.get("formula", "").replace("\n", "<br/>")
            gs_box = Table([[Paragraph(f'<b>Rule:</b> {_gd_rule}<br/>'
                                        f'<b>Form:</b> {formula_text}', s["body_s"])]], colWidths=[pw])
            gs_box.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_PURPLE_L),
                                         ("BOX",(0,0),(-1,-1),0.3,C_PURPLE),
                                         ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
                                         ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
                                         ("ROUNDEDCORNERS",[6,6,6,6])]))
            elements.append(gs_box)
            elements.append(Spacer(1, 4))
        elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # APPENDIX 6: AUDIO SCRIPTS
    # ═══════════════════════════════════════════
    elements.append(_sec_hdr("AUDIO SCRIPTS", C_ORANGE))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Transcripts of listening activities for each unit.", s["sub"]))
    elements.append(Spacer(1, 6))
    for ug in unit_groups:
        if ug["unit"] not in units_to_gen:
            continue
        elements.append(Paragraph(f'<b>Unit {ug["unit"]}: {ug["title"]}</b>', s["h3"]))
        # Use listening script bank first
        _ls = _LISTENING_SCRIPT_BANK.get(grade, {}).get(ug["unit"], None)
        if _ls and isinstance(_ls, dict):
            elements.append(Paragraph(f'<i>{_ls.get("title", "Audio Script")}</i>', s["body_s"]))
            elements.append(Spacer(1, 3))
            script_text = _ls.get("script", "").replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
            as_box = Table([[Paragraph(script_text, s["body_s"])]], colWidths=[pw])
            as_box.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,-1), C_ORANGE_L),
                ("BOX",(0,0),(-1,-1), 0.3, C_ORANGE),
                ("LEFTPADDING",(0,0),(-1,-1),10), ("RIGHTPADDING",(0,0),(-1,-1),10),
                ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
                ("ROUNDEDCORNERS",[6,6,6,6]),
            ]))
            elements.append(as_box)
        else:
            # Fallback to dialogue bank
            dlg = _DIALOGUE_BANK.get(grade, {}).get(ug["unit"], None)
            if dlg:
                script_lines = []
                for speaker, line in dlg["lines"]:
                    script_lines.append(f"<b>{speaker}:</b> {line}")
                elements.append(Paragraph("<br/>".join(script_lines), s["body_s"]))
            else:
                elements.append(Paragraph("<i>[Audio transcript for this unit]</i>", s["sub"]))
        elements.append(Spacer(1, 8))
    elements.append(PageBreak())

    # ═══════════════════════════════════════════
    # BACK COVER (Professional — from Design System)
    # ═══════════════════════════════════════════
    _current_unit_title[0] = "__BACK__"
    back_cover_elements = build_back_cover(
        grade=grade, acad_year=acad_year,
        institution_name=kurum_display, pw=pw,
        font_name=font_name, font_bold=font_bold,
        rl_colors_module=rl_colors,
    )
    elements.extend(back_cover_elements)

    # Build with professional header/footer from design system
    def _page_template(canvas, doc):
        draw_page_header_footer(
            canvas, doc, grade, font_name, font_bold,
            book_title=book_title,
            unit_title=_current_unit_title[0],
            rl_colors_module=rl_colors,
        )

    doc.build(elements, onFirstPage=_page_template, onLaterPages=_page_template)

    # ── Save page map for DLP/report cross-reference ──
    if _page_tracker:
        # Restructure: flat "unit_3_story" → nested {"3": {"story": 14}}
        _structured_map = {}
        for k, pg in _page_tracker.items():
            parts = k.split("_", 2)  # "unit", "3", "story"
            if len(parts) == 3:
                unit_num = parts[1]
                section = parts[2]
                _structured_map.setdefault(unit_num, {})[section] = pg
        try:
            _save_page_map(grade, _structured_map)
        except Exception:
            pass  # Non-critical — don't break PDF generation

    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# TEACHER'S GUIDE PDF GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_teacher_guide_pdf(grade: int, curriculum_weeks: list,
                                institution_info: dict | None = None) -> bytes:
    """Generate Teacher's Guide PDF with lesson plans, weekly templates,
    differentiation levels and assessment matrices."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.units import cm, mm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, PageBreak)
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
        from utils.shared_data import ensure_turkish_pdf_fonts
        from utils.book_design_system import (
            build_reportlab_colors, build_paragraph_styles,
            draw_page_header_footer, PAGE_LAYOUT,
        )
    except ImportError:
        return b""

    font_name, font_bold = ensure_turkish_pdf_fonts()
    info = institution_info or {}
    cfg = GRADE_CONFIG.get(grade, GRADE_CONFIG[5])
    unit_groups = build_unit_groups(grade, curriculum_weeks)

    # Colours from Design System
    C = build_reportlab_colors(rl_colors)
    C_NAVY = C["navy"]
    C_BLUE = C["blue"]
    C_BLUE_L = C["blue_light"]
    C_GREEN = C["green"]
    C_GREEN_L = C["green_light"]
    C_PURPLE = C["purple"]
    C_PURPLE_L = C["purple_light"]
    C_ORANGE = C["orange"]
    C_ORANGE_L = C["orange_light"]
    C_TEAL = C["teal"]
    C_TEAL_L = C["teal_light"]
    C_RED = C["red"]
    C_RED_L = C["red_light"]
    C_GOLD = C["gold"]
    C_GOLD_L = C["gold_light"]
    C_PINK = C["pink"]
    C_PINK_L = C["pink_light"]
    C_TEXT = C["text"]
    C_SUB = C["sub"]
    C_BORDER = C["border"]
    C_LIGHT = C["light"]
    C_WHITE = rl_colors.white

    # Page layout from design system
    margin_l = PAGE_LAYOUT["margin_left"] * mm
    margin_r = PAGE_LAYOUT["margin_right"] * mm
    margin_t = PAGE_LAYOUT["margin_top"] * mm
    margin_b = PAGE_LAYOUT["margin_bottom"] * mm
    pw = A4[0] - margin_l - margin_r

    # Styles from Design System
    s = build_paragraph_styles(grade, font_name, font_bold, rl_colors)
    s["cover_t"] = ParagraphStyle("ct", fontName=font_bold, fontSize=28, leading=36, alignment=TA_CENTER, textColor=C_WHITE)
    s["cover_s"] = ParagraphStyle("cs", fontName=font_name, fontSize=14, leading=20, alignment=TA_CENTER, textColor=rl_colors.HexColor("#93c5fd"))
    s["sec_t"] = s["section_title"]
    s["body_j"] = s.get("body_j", s["body"])
    s["body_s"] = s.get("body_s", s["body"])
    s["cell_w"] = s.get("cell_w", s["cell"])
    s["cell_s"] = s.get("cell_s", s["cell"])
    s["instr"] = s.get("instr", s["h3"])

    _tg_section = [""]
    tg_book_title = f"Teacher's Guide — Grade {grade}"

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=margin_t,
                            bottomMargin=margin_b,
                            leftMargin=margin_l,
                            rightMargin=margin_r)
    elements = []

    def _sec_hdr(title, color):
        h = Table([[Paragraph(f'<b>{title}</b>', s["sec_t"])]], colWidths=[pw], rowHeights=[28])
        h.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                ("LEFTPADDING",(0,0),(-1,-1),14), ("ROUNDEDCORNERS",[8,8,8,8])]))
        return h

    # ═══ COVER ═══
    elements.append(Spacer(1, 2*cm))
    cover_data = [
        [Spacer(1, 1*cm)],
        [Paragraph("TEACHER'S GUIDE", s["cover_t"])],
        [Paragraph("Early Steps" if grade == 0 else f"Bright Start {grade}" if grade <= 4 else f"Next Level {grade}" if grade <= 8 else f"English Core {grade}", s["cover_s"])],
        [Spacer(1, 8)],
        [Paragraph(f"CEFR {cfg['cefr']} | {cfg['label']}", ParagraphStyle("ci", fontName=font_name, fontSize=11, leading=15, alignment=TA_CENTER, textColor=rl_colors.HexColor("#CBD5E1")))],
        [Spacer(1, 12)],
        [Paragraph("Lesson Plans | Weekly Templates | Differentiation | Assessment", ParagraphStyle("ci2", fontName=font_name, fontSize=10, leading=14, alignment=TA_CENTER, textColor=rl_colors.HexColor("#CBD5E1")))],
        [Spacer(1, 1*cm)],
    ]
    kurum = info.get("name", "")
    if kurum:
        font_ok = font_name != "Helvetica"
        _map = str.maketrans("ıİğĞüÜşŞöÖçÇ", "iIgGuUsSoOcC")
        kn = kurum if font_ok else kurum.translate(_map)
        cover_data.append([Paragraph(kn, ParagraphStyle("kn", fontName=font_bold, fontSize=12, leading=16, alignment=TA_CENTER, textColor=C_GOLD))])
    ct = Table(cover_data, colWidths=[pw])
    ct.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_NAVY), ("ALIGN",(0,0),(-1,-1),"CENTER"),
                            ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),4),
                            ("BOTTOMPADDING",(0,0),(-1,-1),4), ("ROUNDEDCORNERS",[12,12,12,12])]))
    elements.append(ct)
    elements.append(PageBreak())

    # ═══ SECTION 1: UNIT LESSON PLANS ═══
    elements.append(Paragraph("SECTION 1: DETAILED UNIT LESSON PLANS", s["h1"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Each unit spans approximately 3.5 weeks (10-12 lesson hours). "
                              "Below is a detailed plan for each unit showing timing, activities, "
                              "materials and assessment methods.", s["body_j"]))
    elements.append(Spacer(1, 8))

    _section_plan = [
        ("Story Episode", 15, "Projector / printed story page", "Oral participation", C_PURPLE),
        ("Vocabulary Workshop", 25, "Flashcards, word bank handout", "Word quiz (10 words)", C_BLUE),
        ("Reading Comprehension", 40, "Coursebook + dictionary", "Comprehension questions (6 Qs)", C_GREEN),
        ("Grammar Focus", 40, "Whiteboard, grammar chart", "Gap-fill exercises (6 items)", C_PURPLE),
        ("Listening & Speaking", 40, "Audio player / QR phone, pair cards", "Listening task + dialogue", C_ORANGE),
        ("Writing Workshop", 25, "Model text handout, checklist", "Written text (graded by rubric)", C_TEAL),
        ("Pronunciation Corner", 15, "Audio, phonetic chart poster", "Tongue twister challenge", C_PINK),
        ("Comic Strip", 20, "Coloured pencils, blank panels", "Completed comic (peer review)", C_ORANGE),
        ("Dialogue Corner", 20, "Role cards", "Pair performance", C_BLUE),
        ("Culture + Turkey Corner", 25, "Map, culture cards, recipe", "Written response", rl_colors.HexColor("#0369a1")),
        ("STEAM Bridge", 20, "Subject-specific materials", "Cross-curricular project", rl_colors.HexColor("#0369a1")),
        ("Project Work", 20, "Materials per project", "Completed project + presentation", C_GOLD),
        ("Song & Rhyme", 15, "Audio / QR code", "Sing-along participation", C_PINK),
        ("Review & Self-Assessment", 25, "Self-assessment form", "Can-do checklist", C_RED),
        ("Real-World Mission", 0, "Assigned as homework", "Evidence portfolio", C_GREEN),
        ("Family Corner", 0, "Take-home sheet", "Parent signature", C_PURPLE),
        ("Podcast Task", 0, "Phone/tablet for recording", "Audio recording", C_ORANGE),
        ("Gamification", 5, "XP tracker in book", "XP total", C_GOLD),
    ]

    for ug in unit_groups:
        elements.append(_sec_hdr(f'UNIT {ug["unit"]}: {ug["title"].upper()}', C_BLUE))
        elements.append(Spacer(1, 6))
        weeks = ug.get("week_data", [])
        # Unit overview
        all_vocab = []
        for w in weeks:
            all_vocab.extend(w.get("vocab", []))
        all_vocab = list(dict.fromkeys(all_vocab))
        structures = list(dict.fromkeys(w.get("structure", "") for w in weeks if w.get("structure")))

        elements.append(Paragraph(f'<b>Weeks:</b> {ug["weeks"][0]}-{ug["weeks"][-1]} | '
                                  f'<b>Vocabulary:</b> {len(all_vocab)} words | '
                                  f'<b>Grammar:</b> {", ".join(structures[:2]) if structures else "See coursebook"}', s["body_s"]))
        elements.append(Spacer(1, 6))

        # Lesson plan table
        lp_rows = [[Paragraph("<b>Section</b>", s["cell_w"]),
                     Paragraph("<b>Time</b>", s["cell_w"]),
                     Paragraph("<b>Materials</b>", s["cell_w"]),
                     Paragraph("<b>Assessment</b>", s["cell_w"])]]
        for sec_name, mins, mats, assess, _ in _section_plan:
            t_label = f"{mins} min" if mins > 0 else "Homework"
            lp_rows.append([Paragraph(sec_name, s["cell_s"]),
                           Paragraph(t_label, s["cell_s"]),
                           Paragraph(mats, s["cell_s"]),
                           Paragraph(assess, s["cell_s"])])
        lpt = Table(lp_rows, colWidths=[3.5*cm, 1.8*cm, (pw-7.5*cm)/2, (pw-7.5*cm)/2])
        lpt_style = [("BACKGROUND",(0,0),(-1,0),C_NAVY), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                     ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3),
                     ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),4)]
        for ri in range(1, len(lp_rows)):
            lpt_style.append(("BACKGROUND",(0,ri),(-1,ri), C_LIGHT if ri%2==0 else C_WHITE))
        lpt.setStyle(TableStyle(lpt_style))
        elements.append(lpt)
        elements.append(Spacer(1, 6))

        # Teacher notes
        grammar = _GRAMMAR_BANK.get(grade, {}).get(ug["unit"], {})
        if grammar:
            _gt = grammar.get("title") or grammar.get("topic", "")
            _gr = grammar.get("rule") or grammar.get("explanation", "")
            elements.append(Paragraph(f'<b>Grammar Focus:</b> {_gt} — {_gr}', s["body_s"]))
        reading = _READING_BANK.get(grade, {}).get(ug["unit"], {})
        if reading:
            elements.append(Paragraph(f'<b>Reading Topic:</b> {reading.get("title", "")} ({reading.get("word_count", "~180")} words, '
                                      f'{len(reading.get("questions", []))} questions)', s["body_s"]))
        elements.append(Spacer(1, 4))
        # Potential difficulties
        elements.append(Paragraph("<b>Potential Difficulties &amp; Tips:</b>", s["h3"]))
        _pron = _PRONUNCIATION_BANK.get(grade, {}).get(ug["unit"], {})
        if _pron:
            elements.append(Paragraph(f"Pronunciation: {_pron.get('focus', '')} — {_pron.get('rule', '')}", s["body_s"]))
        elements.append(Spacer(1, 4))
        elements.append(PageBreak())

    # ═══ SECTION 2: WEEKLY PLANNING TEMPLATE ═══
    elements.append(Paragraph("SECTION 2: WEEKLY PLANNING TEMPLATE", s["h1"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Photocopy this template for each week. Fill in the sections you plan to cover.", s["body"]))
    elements.append(Spacer(1, 8))

    for week_num in range(1, 4):
        elements.append(_sec_hdr(f"WEEK {week_num} PLANNING TEMPLATE", C_TEAL))
        elements.append(Spacer(1, 6))
        template_rows = [
            [Paragraph("<b></b>", s["cell_w"]),
             Paragraph("<b>Lesson 1</b>", s["cell_w"]),
             Paragraph("<b>Lesson 2</b>", s["cell_w"]),
             Paragraph("<b>Lesson 3</b>", s["cell_w"])],
            [Paragraph("<b>Unit / Week</b>", s["cell"]),
             Paragraph("Unit: ___ Week: ___", s["cell_s"]),
             Paragraph("Date: ___/___/______", s["cell_s"]),
             Paragraph("Date: ___/___/______", s["cell_s"])],
            [Paragraph("<b>Sections</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Objectives</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Materials</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Activities</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Assessment</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Homework</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
            [Paragraph("<b>Notes</b>", s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"]),
             Paragraph("_" * 25, s["cell"])],
        ]
        tpt = Table(template_rows, colWidths=[2.2*cm, (pw-2.2*cm)/3, (pw-2.2*cm)/3, (pw-2.2*cm)/3])
        tpt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_TEAL), ("BACKGROUND",(0,1),(0,-1),C_TEAL_L),
                                  ("GRID",(0,0),(-1,-1),0.5,C_BORDER), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                  ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
                                  ("LEFTPADDING",(0,0),(-1,-1),5)]))
        elements.append(tpt)
        elements.append(Spacer(1, 8))
    elements.append(PageBreak())

    # ═══ SECTION 3: DIFFERENTIATION ═══
    elements.append(Paragraph("SECTION 3: LEVEL DIFFERENTIATION", s["h1"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Each unit can be taught at three levels. Use this guide to adapt activities for your students.", s["body_j"]))
    elements.append(Spacer(1, 8))

    _diff_sections = [
        ("Vocabulary", "Learn 5 key words with pictures", "Learn all 15 words, use in sentences", "Learn 15+ words, create word map, use in story"),
        ("Reading", "Read simplified version, answer 3 MCQ", "Read full text, answer all 6 questions", "Read + summarise, write 3 extra questions"),
        ("Grammar", "Copy rule, fill 3 gaps (word bank given)", "Complete all 6 exercises without help", "Write own examples + explain rule to partner"),
        ("Listening", "Listen 3 times, fill simple table", "Listen twice, complete all tasks", "Listen once, take detailed notes, retell"),
        ("Writing", "Write 4-5 sentences using model", "Write 8-10 sentences with plan", "Write 12+ sentences, self-edit, peer review"),
        ("Speaking", "Read prepared dialogue with partner", "Create own dialogue on topic", "Improvise role-play, present to class"),
        ("Project", "Follow all steps with teacher help", "Complete independently", "Extend project + present to class"),
    ]

    for ug in unit_groups:
        elements.append(_sec_hdr(f'UNIT {ug["unit"]}: {ug["title"]} — DIFFERENTIATION', C_PURPLE))
        elements.append(Spacer(1, 6))
        diff_rows = [[Paragraph("<b>Section</b>", s["cell_w"]),
                      Paragraph("<b>Starter</b>", s["cell_w"]),
                      Paragraph("<b>Standard</b>", s["cell_w"]),
                      Paragraph("<b>Advanced</b>", s["cell_w"])]]
        for sec, starter, standard, advanced in _diff_sections:
            diff_rows.append([Paragraph(f"<b>{sec}</b>", s["cell_s"]),
                             Paragraph(starter, s["cell_s"]),
                             Paragraph(standard, s["cell_s"]),
                             Paragraph(advanced, s["cell_s"])])
        dft = Table(diff_rows, colWidths=[2*cm, (pw-2*cm)/3, (pw-2*cm)/3, (pw-2*cm)/3])
        dft_style = [("BACKGROUND",(0,0),(-1,0),C_PURPLE), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                     ("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),4),
                     ("BOTTOMPADDING",(0,0),(-1,-1),4), ("LEFTPADDING",(0,0),(-1,-1),4),
                     ("BACKGROUND",(1,1),(1,-1),rl_colors.HexColor("#fef3c7")),
                     ("BACKGROUND",(2,1),(2,-1),C_GREEN_L),
                     ("BACKGROUND",(3,1),(3,-1),C_PURPLE_L)]
        dft.setStyle(TableStyle(dft_style))
        elements.append(dft)
        elements.append(Spacer(1, 8))
    elements.append(PageBreak())

    # ═══ SECTION 4: ASSESSMENT MATRIX ═══
    elements.append(Paragraph("SECTION 4: ASSESSMENT MATRIX", s["h1"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Use this matrix to track which skills each section assesses and how to score them.", s["body_j"]))
    elements.append(Spacer(1, 8))

    _assess_data = [
        ("Story Episode", "L, S, R", "Participation", "Oral response, story retelling", "5"),
        ("Vocabulary Workshop", "R, W", "Formative", "Word quiz, matching exercise", "10"),
        ("Reading Comprehension", "R", "Formative", "6 comprehension questions", "12"),
        ("Grammar Focus", "R, W", "Formative", "6 exercises, gap-fill", "12"),
        ("Listening & Speaking", "L, S", "Formative", "3 listening tasks + dialogue", "10"),
        ("Writing Workshop", "W", "Summative", "Written text graded by rubric", "15"),
        ("Pronunciation Corner", "L, S", "Informal", "Repeat, identify sounds", "5"),
        ("Comic Strip", "W, R", "Creative", "Completed comic with grammar", "10"),
        ("Dialogue Corner", "S, L", "Performance", "Pair dialogue performance", "5"),
        ("Review & Assessment", "All", "Self-assessment", "Can-do checklist", "N/A"),
        ("Real-World Mission", "All", "Portfolio", "Evidence of completion", "10"),
        ("Family Corner", "S, W", "Parent feedback", "Parent signature + response", "5"),
        ("Progress Check", "R, W", "Summative", "13-point written test", "13"),
        ("Escape Room", "All", "Collaborative", "Team puzzle completion", "Bonus"),
        ("Project Work", "All", "Summative", "Project + presentation rubric", "15"),
    ]

    am_rows = [[Paragraph("<b>Section</b>", s["cell_w"]),
                Paragraph("<b>Skills</b>", s["cell_w"]),
                Paragraph("<b>Type</b>", s["cell_w"]),
                Paragraph("<b>How to Assess</b>", s["cell_w"]),
                Paragraph("<b>Max Points</b>", s["cell_w"])]]
    for sec, skills, atype, how, pts in _assess_data:
        am_rows.append([Paragraph(sec, s["cell_s"]),
                       Paragraph(skills, s["cell_s"]),
                       Paragraph(atype, s["cell_s"]),
                       Paragraph(how, s["cell_s"]),
                       Paragraph(pts, s["cell_s"])])
    amt = Table(am_rows, colWidths=[3*cm, 1.5*cm, 2*cm, pw-8.5*cm, 2*cm])
    am_style = [("BACKGROUND",(0,0),(-1,0),C_RED), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3),
                ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),4)]
    for ri in range(1, len(am_rows)):
        am_style.append(("BACKGROUND",(0,ri),(-1,ri), C_RED_L if ri%2==0 else C_WHITE))
    amt.setStyle(TableStyle(am_style))
    elements.append(amt)
    elements.append(Spacer(1, 10))

    # Skill legend
    elements.append(Paragraph("<b>Skills Legend:</b>  L = Listening  |  S = Speaking  |  R = Reading  |  W = Writing", s["body_s"]))
    elements.append(Spacer(1, 8))

    # Grading rubric for writing
    elements.append(_sec_hdr("WRITING ASSESSMENT RUBRIC", C_TEAL))
    elements.append(Spacer(1, 6))
    wr_rows = [[Paragraph("<b>Criteria</b>", s["cell_w"]),
                Paragraph("<b>Excellent (5)</b>", s["cell_w"]),
                Paragraph("<b>Good (3-4)</b>", s["cell_w"]),
                Paragraph("<b>Needs Work (1-2)</b>", s["cell_w"])]]
    _rubric = [
        ("Content", "All points covered, ideas well-developed", "Most points covered, some development", "Few points, undeveloped"),
        ("Grammar", "Very few errors, good range of structures", "Some errors, limited structures", "Many errors, basic structures only"),
        ("Vocabulary", "Wide range, topic-appropriate", "Adequate range, some repetition", "Very limited, frequent repetition"),
        ("Organisation", "Clear paragraphs, logical flow", "Some structure, mostly logical", "No clear structure"),
        ("Spelling/Punctuation", "Very few errors", "Some errors but readable", "Many errors, hard to read"),
    ]
    for crit, exc, good, needs in _rubric:
        wr_rows.append([Paragraph(f"<b>{crit}</b>", s["cell_s"]),
                       Paragraph(exc, s["cell_s"]),
                       Paragraph(good, s["cell_s"]),
                       Paragraph(needs, s["cell_s"])])
    wrt = Table(wr_rows, colWidths=[2.2*cm, (pw-2.2*cm)/3, (pw-2.2*cm)/3, (pw-2.2*cm)/3])
    wrt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),C_TEAL), ("GRID",(0,0),(-1,-1),0.3,C_BORDER),
                              ("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),4),
                              ("BOTTOMPADDING",(0,0),(-1,-1),4), ("LEFTPADDING",(0,0),(-1,-1),4),
                              ("BACKGROUND",(1,1),(1,-1),C_GREEN_L),
                              ("BACKGROUND",(2,1),(2,-1),C_ORANGE_L),
                              ("BACKGROUND",(3,1),(3,-1),C_RED_L)]))
    elements.append(wrt)
    elements.append(Spacer(1, 10))

    # Student tracking sheet
    elements.append(PageBreak())
    elements.append(_sec_hdr("STUDENT PROGRESS TRACKING SHEET", C_GOLD))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Photocopy for each student. Track completion and scores across units.", s["body"]))
    elements.append(Spacer(1, 6))
    track_rows = [[Paragraph("<b>Student Name: _____________________  Class: _____</b>", s["cell"]),
                   Paragraph("", s["cell"]), Paragraph("", s["cell"]), Paragraph("", s["cell"]),
                   Paragraph("", s["cell"])]]
    track_rows.append([Paragraph("<b>Unit</b>", s["cell_w"]),
                       Paragraph("<b>Vocab Quiz</b>", s["cell_w"]),
                       Paragraph("<b>Writing</b>", s["cell_w"]),
                       Paragraph("<b>Progress Check</b>", s["cell_w"]),
                       Paragraph("<b>Total XP</b>", s["cell_w"])])
    for u in range(1, 11):
        track_rows.append([Paragraph(f"Unit {u}", s["cell"]),
                          Paragraph("___/10", s["cell"]),
                          Paragraph("___/15", s["cell"]),
                          Paragraph("___/13", s["cell"]),
                          Paragraph("___", s["cell"])])
    trt = Table(track_rows, colWidths=[pw/5]*5)
    trt.setStyle(TableStyle([("BACKGROUND",(0,1),(-1,1),C_GOLD),
                              ("GRID",(0,1),(-1,-1),0.5,C_BORDER),
                              ("SPAN",(0,0),(-1,0)),
                              ("BACKGROUND",(0,0),(-1,0),C_GOLD_L),
                              ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),5),
                              ("BOTTOMPADDING",(0,0),(-1,-1),5),
                              ("LEFTPADDING",(0,0),(-1,-1),6)]))
    elements.append(trt)

    # Build with professional header/footer from design system
    def _tg_page_template(canvas, doc):
        draw_page_header_footer(
            canvas, doc, grade, font_name, font_bold,
            book_title=tg_book_title,
            unit_title=_tg_section[0],
            rl_colors_module=rl_colors,
        )

    doc.build(elements, onFirstPage=_tg_page_template, onLaterPages=_tg_page_template)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# FLIPBOOK HTML BUILDER (with Web Speech API TTS)
# ══════════════════════════════════════════════════════════════════════════════

def _safe_get(d, *keys, default=""):
    """Get first matching key from dict, or default."""
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d:
            return d[k]
    return default


def _normalize_questions(qs):
    """Normalize question lists from various bank formats."""
    if not qs:
        return []
    result = []
    for q in qs:
        if isinstance(q, str):
            result.append(q)
        elif isinstance(q, dict):
            result.append(q.get("q", q.get("question", str(q))))
        else:
            result.append(str(q))
    return result


def build_coursebook_flipbook_html(grade: int, curriculum_weeks: list, mode: str = "student") -> str:
    """Build an interactive HTML5 flipbook with page-turning animation and TTS.

    Args:
        grade: Grade number (0-12)
        curriculum_weeks: Curriculum data
        mode: 'student' | 'teacher' | 'parent'

    Returns:
        Complete HTML string
    """
    import json as _json

    cfg = GRADE_CONFIG.get(grade, GRADE_CONFIG[5])
    unit_groups = build_unit_groups(grade, curriculum_weeks)

    # Build pages data
    pages = []
    # Cover
    grade_label = "Early Steps" if grade == 0 else f"Grade {grade}"
    _flipbook_title = "Early Steps" if grade == 0 else f"Bright Start {grade}" if grade <= 4 else f"Next Level {grade}" if grade <= 8 else f"English Core {grade}"
    pages.append({"type": "cover", "title": _flipbook_title, "sub": f"CEFR {cfg['cefr']} -- {cfg['label']}",
                  "desc": cfg["desc"]})

    for ug in unit_groups:
        u = ug["unit"]
        weeks = ug.get("week_data", [])
        vocab = []
        for w in weeks:
            vocab.extend(w.get("vocab", []))
        vocab = list(dict.fromkeys(vocab))

        # Unit opener
        pages.append({"type": "unit_opener", "unit": u, "title": ug["title"],
                      "weeks": f"{ug['weeks'][0]}-{ug['weeks'][-1]}"})

        # Story — handles dict (title/episode) or list-of-strings format
        story = _STORY_BANK.get(grade, {}).get(u)
        if story:
            if isinstance(story, dict):
                pages.append({"type": "story", "unit": u,
                              "title": story.get("title", f"Unit {u} Story"),
                              "text": story.get("episode") or story.get("story") or story.get("text", ""),
                              "cliffhanger": story.get("cliffhanger", "")})
            elif isinstance(story, list):
                pages.append({"type": "story", "unit": u,
                              "title": f"Unit {u} Story",
                              "text": " ".join(str(s) for s in story),
                              "cliffhanger": ""})

        # Vocabulary
        if vocab:
            pages.append({"type": "vocabulary", "unit": u, "words": vocab[:15]})

        # Reading — handles dict or list-of-dicts
        reading = _READING_BANK.get(grade, {}).get(u)
        if reading:
            if isinstance(reading, list) and reading:
                reading = reading[0] if isinstance(reading[0], dict) else {"text": " ".join(str(r) for r in reading)}
            if isinstance(reading, dict):
                r_text = _safe_get(reading, "text", "passage", "content")
                r_title = _safe_get(reading, "title", default=f"Unit {u} Reading")
                r_qs = _normalize_questions(reading.get("questions", []))
                r_vocab = reading.get("vocabulary", [])
                pages.append({"type": "reading", "unit": u, "title": r_title,
                              "text": r_text, "questions": r_qs,
                              "vocab_list": [v.get("word", "") + " - " + v.get("definition", "") if isinstance(v, dict) else str(v) for v in r_vocab] if r_vocab else []})

        # Grammar — handles dict or list-of-dicts
        grammar = _GRAMMAR_BANK.get(grade, {}).get(u)
        if grammar:
            if isinstance(grammar, list) and grammar:
                grammar = grammar[0] if isinstance(grammar[0], dict) else grammar
            if isinstance(grammar, dict):
                g_title = _safe_get(grammar, "title", "topic", default=f"Unit {u} Grammar")
                g_rule = _safe_get(grammar, "rule", "explanation", "content")
                g_formula = _safe_get(grammar, "formula")
                g_examples = grammar.get("examples", [])
                pages.append({"type": "grammar", "unit": u, "title": g_title,
                              "rule": g_rule, "formula": g_formula,
                              "examples": g_examples[:5] if isinstance(g_examples, list) else []})

        # Listening — handles dict or list-of-dicts
        listening = _LISTENING_SCRIPT_BANK.get(grade, {}).get(u)
        if listening:
            ls = listening
            if isinstance(ls, list) and ls:
                ls = ls[0] if isinstance(ls[0], dict) else ls
            if isinstance(ls, dict):
                l_title = _safe_get(ls, "title", default=f"Unit {u} Listening")
                l_script = _safe_get(ls, "script", "text", "content")
                l_tasks = ls.get("tasks", [])
                l_qs = ls.get("questions", [])
                task_list = l_tasks if l_tasks else [q.get("question", str(q)) if isinstance(q, dict) else str(q) for q in l_qs]
                pages.append({"type": "listening", "unit": u, "title": l_title,
                              "script": l_script, "tasks": task_list})

        # Writing model — handles dict or list-of-dicts
        writing = _MODEL_WRITING_BANK.get(grade, {}).get(u)
        if writing:
            if isinstance(writing, list) and writing:
                writing = writing[0] if isinstance(writing[0], dict) else writing
            if isinstance(writing, dict):
                w_title = _safe_get(writing, "title", default=f"Unit {u} Writing")
                w_model = _safe_get(writing, "text", "model", "content")
                w_focus = _safe_get(writing, "focus", "type", default="Writing Practice")
                pages.append({"type": "writing", "unit": u, "title": w_title,
                              "model": w_model, "focus": w_focus})

        # Song (preschool / primary / middle tiers)
        song = _SONG_BANK.get(grade, {}).get(u)
        if song:
            if isinstance(song, dict):
                pages.append({"type": "song", "unit": u,
                              "title": song.get("title", f"Unit {u} Song"),
                              "lyrics": song.get("lyrics", ""),
                              "activity": song.get("activity", "")})

        # Turkey Corner — handles various key names
        turkey = _TURKEY_CORNER_BANK.get(grade, {}).get(u)
        if turkey:
            if isinstance(turkey, dict):
                t_title = _safe_get(turkey, "title", default=f"Unit {u} Turkey Corner")
                t_text = _safe_get(turkey, "text", "content")
                t_famous = _safe_get(turkey, "famous_person", "famous", "discussion")
                pages.append({"type": "turkey", "unit": u, "title": t_title,
                              "text": t_text, "famous": t_famous})

        # Culture Corner — handles various key names
        culture = _CULTURE_CORNER_BANK.get(grade, {}).get(u)
        if culture:
            if isinstance(culture, list) and culture:
                culture = culture[0] if isinstance(culture[0], dict) else culture
            if isinstance(culture, dict):
                c_title = _safe_get(culture, "title", default=f"Unit {u} Culture Corner")
                c_text = _safe_get(culture, "text", "content")
                pages.append({"type": "culture", "unit": u, "title": c_title,
                              "text": c_text})

        # Fun Facts — handles dict with "facts" key or list
        fun_facts = _FUN_FACTS_BANK.get(grade, {}).get(u)
        if fun_facts:
            if isinstance(fun_facts, dict):
                raw = fun_facts.get("facts", [])
                facts = [str(f) for f in raw[:5]] if isinstance(raw, list) else [str(raw)]
            elif isinstance(fun_facts, list):
                facts = [str(f) for f in fun_facts[:5]]
            else:
                facts = [str(fun_facts)]
            if facts:
                pages.append({"type": "fun_facts", "unit": u, "facts": facts})

        # Progress Check
        progress = _PROGRESS_CHECK_BANK.get(grade, {}).get(u)
        if progress:
            if isinstance(progress, dict):
                pages.append({"type": "progress", "unit": u, "data": progress})

        # Dialogue
        dialogue = _DIALOGUE_BANK.get(grade, {}).get(u)
        if dialogue and isinstance(dialogue, dict):
            d_setting = dialogue.get("setting", "")
            d_chars = dialogue.get("characters", [])
            d_lines = dialogue.get("lines", [])
            d_focus = dialogue.get("focus_language", "")
            d_task = dialogue.get("task", "")
            line_list = []
            for ln in d_lines:
                if isinstance(ln, (list, tuple)) and len(ln) >= 2:
                    line_list.append({"speaker": str(ln[0]), "text": str(ln[1])})
                elif isinstance(ln, dict):
                    line_list.append({"speaker": ln.get("speaker", ""), "text": ln.get("text", ln.get("line", ""))})
            pages.append({"type": "dialogue", "unit": u, "setting": d_setting,
                          "characters": d_chars, "lines": line_list,
                          "focus": d_focus, "task": d_task})

        # Pronunciation
        pron = _PRONUNCIATION_BANK.get(grade, {}).get(u)
        if pron and isinstance(pron, dict):
            p_sound = pron.get("sound", pron.get("focus", ""))
            p_words = pron.get("words", pron.get("word_list", []))
            p_chant = pron.get("chant", pron.get("tongue_twister", ""))
            p_action = pron.get("action", pron.get("tip", pron.get("activity", "")))
            pages.append({"type": "pronunciation", "unit": u, "sound": p_sound,
                          "words": p_words[:10] if isinstance(p_words, list) else [],
                          "chant": p_chant, "action": p_action})

        # Workbook
        workbook = _WORKBOOK_BANK.get(grade, {}).get(u)
        if workbook and isinstance(workbook, dict):
            wb_acts = workbook.get("activities", [])
            wb_items = []
            for act in (wb_acts if isinstance(wb_acts, list) else []):
                if isinstance(act, dict):
                    wb_items.append({"type": act.get("type", "exercise"),
                                     "instruction": act.get("instruction", act.get("text", ""))})
                else:
                    wb_items.append({"type": "exercise", "instruction": str(act)})
            if wb_items:
                pages.append({"type": "workbook", "unit": u, "activities": wb_items})

        # Project
        project = _PROJECT_BANK.get(grade, {}).get(u)
        if project and isinstance(project, dict):
            pages.append({"type": "project", "unit": u,
                          "title": project.get("title", f"Unit {u} Project"),
                          "desc": project.get("description", project.get("task", project.get("objective", ""))),
                          "steps": project.get("steps", project.get("materials", [])),
                          "outcome": project.get("outcome", project.get("presentation", ""))})

        # Comic Strip
        comic = _COMIC_STRIP_BANK.get(grade, {}).get(u)
        if comic and isinstance(comic, dict):
            panels = comic.get("panels", [])
            panel_list = []
            for p_item in (panels if isinstance(panels, list) else []):
                if isinstance(p_item, dict):
                    panel_list.append({"scene": p_item.get("scene", ""),
                                       "speech": p_item.get("speech", p_item.get("dialogue", "")),
                                       "thought": p_item.get("thought", "")})
            pages.append({"type": "comic", "unit": u,
                          "title": comic.get("title", f"Unit {u} Comic"),
                          "panels": panel_list,
                          "task": comic.get("drawing_task", comic.get("task", ""))})

        # Mission
        mission = _MISSION_BANK.get(grade, {}).get(u)
        if mission and isinstance(mission, dict):
            pages.append({"type": "mission", "unit": u,
                          "title": mission.get("title", f"Mission {u}"),
                          "mission": mission.get("mission", mission.get("objective", "")),
                          "evidence": mission.get("evidence", ""),
                          "xp": mission.get("xp", 25),
                          "difficulty": mission.get("difficulty", "Medium")})

        # Escape Room
        escape = _ESCAPE_ROOM_BANK.get(grade, {}).get(u)
        if escape and isinstance(escape, dict):
            puzzles = escape.get("puzzles", [])
            puzzle_list = []
            for pz in (puzzles if isinstance(puzzles, list) else []):
                if isinstance(pz, dict):
                    puzzle_list.append({"type": pz.get("type", ""),
                                        "question": pz.get("question", ""),
                                        "hint": pz.get("hint", "")})
            pages.append({"type": "escape_room", "unit": u,
                          "title": escape.get("title", f"Escape Room {u}"),
                          "story": escape.get("story", ""),
                          "puzzles": puzzle_list,
                          "reward": escape.get("reward", "")})

        # Family Corner
        family = _FAMILY_CORNER_BANK.get(grade, {}).get(u)
        if family and isinstance(family, dict):
            pages.append({"type": "family", "unit": u,
                          "title": family.get("title", f"Family Corner {u}"),
                          "activity": family.get("activity", ""),
                          "together": family.get("together", ""),
                          "parent_q": family.get("parent_question", "")})

        # SEL (Social-Emotional Learning)
        sel = _SEL_BANK.get(grade, {}).get(u)
        if sel and isinstance(sel, dict):
            pages.append({"type": "sel", "unit": u,
                          "emotion": sel.get("emotion", ""),
                          "prompt": sel.get("prompt", ""),
                          "activity": sel.get("activity", ""),
                          "mindfulness": sel.get("mindfulness", ""),
                          "discussion": sel.get("discussion", "")})

        # STEAM
        steam = _STEAM_BANK.get(grade, {}).get(u)
        if steam and isinstance(steam, dict):
            pages.append({"type": "steam", "unit": u,
                          "subject": steam.get("subject", ""),
                          "title": steam.get("title", f"STEAM {u}"),
                          "task": steam.get("task", ""),
                          "vocab": steam.get("vocab", [])})

        # Podcast
        podcast = _PODCAST_BANK.get(grade, {}).get(u)
        if podcast and isinstance(podcast, dict):
            _pod_segs = podcast.get("segments", [])
            # Grade 1-8: "script" is a string, convert to single-item list
            if not _pod_segs:
                _pod_script = podcast.get("script", "")
                if _pod_script and isinstance(_pod_script, str):
                    _pod_segs = [_pod_script[:200] + "..."] if len(_pod_script) > 200 else [_pod_script]
                elif isinstance(_pod_script, list):
                    _pod_segs = _pod_script
            pages.append({"type": "podcast", "unit": u,
                          "title": podcast.get("title", f"Podcast {u}"),
                          "host": podcast.get("host", ""),
                          "summary": podcast.get("summary", podcast.get("description", "")),
                          "segments": _pod_segs,
                          "student_task": podcast.get("student_task", "")})

    pages_json = _json.dumps(pages, ensure_ascii=False)

    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#131825;color:#E2E8F0;
font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;min-height:100vh;overflow-x:hidden}}
.top-bar{{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;
background:linear-gradient(135deg,rgba(79,70,229,.08),rgba(79,70,229,.03));
border-bottom:1px solid rgba(79,70,229,.15)}}
.top-bar h1{{font-size:1.1rem;color:#6366F1;font-weight:800}}
.top-bar .info{{font-size:.75rem;color:#94A3B8}}
.controls{{display:flex;gap:8px;align-items:center}}
.controls button{{background:#0F1420;border:1px solid #1A2035;
color:#6366F1;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:.85rem;transition:all .2s}}
.controls button:hover{{background:rgba(79,70,229,.06);border-color:#6366F1}}
.controls button.active{{background:rgba(79,70,229,.1);border-color:#6366F1}}
.tts-btn{{background:linear-gradient(135deg,#059669,#047857)!important;color:#fff!important;
border:none!important;font-weight:700}}
.tts-btn:hover{{filter:brightness(1.2)}}
.tts-btn.speaking{{animation:pulse 1s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.6}}}}
.tts-sentence{{transition:all .3s ease;border-radius:6px;padding:2px 4px;display:inline;
position:relative;cursor:default}}
.tts-sentence.active{{background:linear-gradient(135deg,rgba(79,70,229,.12),rgba(99,102,241,.08));
color:#A5B4FC;box-shadow:0 0 12px rgba(79,70,229,.15);
border-radius:6px;padding:2px 6px}}
.tts-sentence.active::before{{content:"";position:absolute;left:-2px;top:0;bottom:0;width:3px;
background:linear-gradient(180deg,#fbbf24,#f59e0b);border-radius:2px;
box-shadow:0 0 8px rgba(251,191,36,.6)}}
.tts-sentence.done{{color:rgba(107,114,128,.5);transition:color .4s}}
.tts-word{{transition:background .15s,color .15s}}
.tts-word.active{{background:linear-gradient(135deg,#6366F1,#6366F1);color:#0F1420;
border-radius:4px;padding:1px 2px;box-shadow:0 0 8px rgba(79,70,229,.3)}}
.book-wrap{{max-width:780px;margin:20px auto;perspective:1500px;position:relative}}
.page{{background:#0F1420;border:1px solid #232B3E;
border-radius:16px;padding:30px 28px;min-height:480px;position:relative;
box-shadow:0 4px 12px rgba(0,0,0,0.06);
transition:transform .5s ease;transform-style:preserve-3d}}
.page.flip-left{{animation:flipL .5s ease}}
.page.flip-right{{animation:flipR .5s ease}}
@keyframes flipL{{0%{{transform:rotateY(0)}}50%{{transform:rotateY(-12deg)}}100%{{transform:rotateY(0)}}}}
@keyframes flipR{{0%{{transform:rotateY(0)}}50%{{transform:rotateY(12deg)}}100%{{transform:rotateY(0)}}}}
.page-num{{position:absolute;top:14px;right:18px;font-size:.7rem;color:#64748B;font-style:italic}}
.page-type{{display:inline-block;background:rgba(79,70,229,.12);color:#6366F1;padding:3px 12px;
border-radius:12px;font-size:.7rem;margin-bottom:14px;letter-spacing:1px;text-transform:uppercase}}
.page h2{{color:#E2E8F0;font-size:1.3rem;margin-bottom:12px;font-weight:800}}
.page h3{{color:#6366F1;font-size:1rem;margin:12px 0 8px;font-weight:700}}
.page .text-block{{background:rgba(79,70,229,.05);border-left:3px solid rgba(79,70,229,.3);
border-radius:0 10px 10px 0;padding:16px 18px;font-size:.9rem;line-height:1.8;margin:10px 0;color:#94A3B8}}
.page .highlight{{background:rgba(79,70,229,.08);border:1px solid rgba(79,70,229,.15);
border-radius:10px;padding:12px 16px;margin:10px 0;font-size:.85rem;color:#CBD5E1}}
.page .word-grid{{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}}
.page .word-chip{{background:rgba(37,99,235,.08);color:#2563EB;padding:6px 14px;border-radius:20px;
font-size:.85rem;border:1px solid rgba(37,99,235,.1);cursor:pointer;transition:all .2s}}
.page .word-chip:hover{{background:rgba(37,99,235,.12);transform:scale(1.05)}}
.page .question{{background:rgba(5,150,105,.05);border-left:3px solid rgba(5,150,105,.15);
padding:8px 14px;margin:6px 0;border-radius:0 8px 8px 0;font-size:.85rem;color:#059669}}
.page .rule-box{{background:linear-gradient(135deg,rgba(124,58,237,.06),rgba(124,58,237,.03));
border:1px solid rgba(124,58,237,.1);border-radius:12px;padding:16px;margin:10px 0;color:#7C3AED}}
.page .cover-title{{font-size:2.2rem;text-align:center;color:#6366F1;margin:40px 0 16px;font-weight:900;
text-shadow:0 2px 12px rgba(79,70,229,.3)}}
.page .cover-sub{{text-align:center;color:#94A3B8;font-size:1rem;margin-bottom:8px}}
.page .unit-badge{{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,var(--uc),rgba(0,0,0,.3));
color:#fff;padding:8px 18px;border-radius:20px;font-size:.85rem;font-weight:700;margin-bottom:14px}}
.nav-bar{{display:flex;justify-content:center;align-items:center;gap:16px;padding:14px;margin-top:8px}}
.nav-bar button{{background:linear-gradient(135deg,rgba(79,70,229,.15),rgba(79,70,229,.08));
border:1px solid rgba(79,70,229,.25);color:#6366F1;padding:10px 24px;border-radius:10px;
cursor:pointer;font-size:.9rem;font-weight:700;transition:all .2s}}
.nav-bar button:hover{{background:rgba(79,70,229,.25);transform:translateY(-1px)}}
.nav-bar .page-info{{color:#94A3B8;font-size:.85rem}}
.toc-list{{list-style:none;padding:0;margin:10px 0}}
.toc-list li{{padding:8px 12px;border-bottom:1px solid #E5E7EB;cursor:pointer;
font-size:.9rem;color:#94A3B8;transition:all .2s;border-radius:6px}}
.toc-list li:hover{{background:rgba(79,70,229,.1);color:#6366F1}}
.toc-list li .toc-unit{{color:#6366F1;font-weight:700;margin-right:8px}}
</style></head><body>
<div class="top-bar">
<div><h1>{"Early Steps" if grade == 0 else "Bright Start " + str(grade) if grade <= 4 else "Next Level " + str(grade) if grade <= 8 else "English Core " + str(grade)}</h1>
<div class="info">CEFR {cfg["cefr"]} | {cfg["label"]} | {len(unit_groups)} Units</div></div>
<div class="controls">
<button onclick="showTOC()" title="Table of Contents">Contents</button>
<button class="tts-btn" onclick="toggleTTS()" id="ttsBtn" title="Read Aloud">\U0001F50A Listen</button>
</div></div>
<div class="book-wrap"><div class="page" id="pageArea"></div></div>
<div class="nav-bar">
<button onclick="prevPage()">&#9664; Previous</button>
<span class="page-info" id="pageInfo">1 / 1</span>
<button onclick="nextPage()">Next &#9654;</button></div>
<div id="tocOverlay" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:100;
overflow-y:auto;padding:40px 20px">
<div style="max-width:600px;margin:0 auto;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
<h2 style="color:#6366F1;font-size:1.2rem">Table of Contents</h2>
<button onclick="closeTOC()" style="background:none;border:1px solid #6366F1;color:#6366F1;padding:6px 16px;
border-radius:8px;cursor:pointer;font-size:.85rem">Close</button></div>
<ul class="toc-list" id="tocList"></ul></div></div>
<script>
var pages={pages_json};
var cur=0,speaking=false,synth=window.speechSynthesis;
function render(){{
var p=pages[cur],el=document.getElementById("pageArea"),html="";
el.className="page";
html+='<div class="page-num">Page '+(cur+1)+' / '+pages.length+'</div>';
if(p.type==="cover"){{
html+='<div class="cover-title">'+p.title+'</div>';
html+='<div class="cover-sub">'+p.sub+'</div>';
html+='<div class="cover-sub" style="font-size:.85rem;color:#94A3B8;margin-top:16px">'+p.desc+'</div>';
html+='<div style="text-align:center;margin-top:40px;color:#64748B;font-size:.8rem">Swipe or use arrows to turn pages</div>';
}}else if(p.type==="unit_opener"){{
html+='<div class="unit-badge" style="--uc:#2563eb">Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="highlight">Weeks '+p.weeks+'</div>';
}}else if(p.type==="story"){{
html+='<div class="page-type">Story — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.text+'</div>';
if(p.cliffhanger)html+='<div class="highlight" style="border-color:rgba(220,38,38,.3);color:#DC2626"><strong>To be continued...</strong> '+p.cliffhanger+'</div>';
}}else if(p.type==="vocabulary"){{
html+='<div class="page-type">Vocabulary — Unit '+p.unit+'</div>';
html+='<h2>Word Bank</h2>';
html+='<div class="word-grid">';
p.words.forEach(function(w){{html+='<span class="word-chip" onclick="speakWord(this.textContent)">'+w+'</span>';}});
html+='</div><div class="highlight" style="margin-top:16px">Click any word to hear its pronunciation</div>';
}}else if(p.type==="reading"){{
html+='<div class="page-type">Reading — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.text+'</div>';
if(p.questions){{html+='<h3>Comprehension Questions</h3>';
p.questions.forEach(function(q){{html+='<div class="question">'+q+'</div>';}});}}
if(p.vocab_list&&p.vocab_list.length){{html+='<h3>Key Vocabulary</h3>';
p.vocab_list.forEach(function(v){{html+='<div class="highlight" style="margin:4px 0;padding:6px 12px">'+v+'</div>';}});}}
}}else if(p.type==="grammar"){{
html+='<div class="page-type">Grammar — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="rule-box" id="readText"><strong>Rule:</strong> '+p.rule+'</div>';
if(p.formula)html+='<div class="highlight"><strong>Formula:</strong><br>'+p.formula.replace(/\\n/g,"<br>")+'</div>';
if(p.examples&&p.examples.length){{html+='<h3>Examples</h3>';p.examples.forEach(function(e){{html+='<div class="question">'+e+'</div>';}});}}
}}else if(p.type==="listening"){{
html+='<div class="page-type">Listening — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.script.replace(/\\n/g,"<br>")+'</div>';
html+='<h3>Tasks</h3>';
p.tasks.forEach(function(t){{html+='<div class="question">'+t+'</div>';}});
}}else if(p.type==="writing"){{
html+='<div class="page-type">Writing Model — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.model.replace(/\\n/g,"<br>")+'</div>';
html+='<div class="highlight"><strong>Focus:</strong> '+p.focus+'</div>';
}}else if(p.type==="turkey"){{
html+='<div class="page-type">Turkey Corner — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.text+'</div>';
html+='<div class="highlight"><strong>Famous Turk:</strong> '+p.famous+'</div>';
}}else if(p.type==="culture"){{
html+='<div class="page-type">Culture Corner — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText">'+p.text+'</div>';
}}else if(p.type==="song"){{
html+='<div class="page-type" style="background:rgba(236,72,153,.12);color:#DB2777">Song — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText" style="border-color:rgba(236,72,153,.3);white-space:pre-line">'+p.lyrics+'</div>';
if(p.activity)html+='<div class="highlight" style="border-color:rgba(236,72,153,.15)"><strong>Activity:</strong> '+p.activity+'</div>';
}}else if(p.type==="fun_facts"){{
html+='<div class="page-type" style="background:rgba(251,191,36,.12);color:#D97706">Fun Facts — Unit '+p.unit+'</div>';
html+='<h2>Did You Know?</h2><div id="readText">';
p.facts.forEach(function(f,i){{html+='<div class="highlight" style="margin:8px 0;border-color:rgba(251,191,36,.15)"><strong>'+(i+1)+'.</strong> '+f+'</div>';}});
html+='</div>';
}}else if(p.type==="progress"){{
html+='<div class="page-type" style="background:rgba(16,185,129,.12);color:#059669">Progress Check — Unit '+p.unit+'</div>';
html+='<h2>Self-Assessment</h2><div id="readText">';
var d=p.data;
if(d.vocabulary){{html+='<h3>Vocabulary</h3>';d.vocabulary.forEach(function(v){{html+='<div class="question">'+(v.question||v.q||"")+'</div>';}});}}
if(d.grammar){{html+='<h3>Grammar</h3>';d.grammar.forEach(function(g){{html+='<div class="question">'+(g.question||g.q||"")+'</div>';}});}}
if(d.reading){{html+='<h3>Reading</h3>';d.reading.forEach(function(r){{html+='<div class="question">'+(r.question||r.q||"")+'</div>';}});}}
if(d.writing){{html+='<h3>Writing</h3>';html+='<div class="highlight">'+(d.writing.prompt||d.writing.task||"")+'</div>';}}
html+='</div>';
}}else if(p.type==="dialogue"){{
html+='<div class="page-type" style="background:rgba(59,130,246,.12);color:#2563EB">Dialogue — Unit '+p.unit+'</div>';
html+='<h2>'+p.setting+'</h2>';
if(p.characters&&p.characters.length)html+='<div class="highlight" style="font-size:.8rem"><strong>Characters:</strong> '+p.characters.join(", ")+'</div>';
html+='<div id="readText" style="margin:12px 0">';
var colors=["#93c5fd","#a5b4fc","#86efac","#fcd34d","#f9a8d4","#c4b5fd"];
p.lines.forEach(function(l,i){{var c=colors[i%colors.length];
html+='<div style="display:flex;gap:10px;margin:6px 0;padding:8px 12px;background:rgba(79,70,229,.02);border-radius:8px;border-left:3px solid '+c+'">';
html+='<strong style="color:'+c+';min-width:80px">'+l.speaker+':</strong>';
html+='<span style="color:#94A3B8">'+l.text+'</span></div>';}});
html+='</div>';
if(p.focus)html+='<div class="rule-box"><strong>Language Focus:</strong> '+p.focus+'</div>';
if(p.task)html+='<div class="highlight"><strong>Task:</strong> '+p.task+'</div>';
}}else if(p.type==="pronunciation"){{
html+='<div class="page-type" style="background:rgba(168,85,247,.12);color:#c084fc">Pronunciation — Unit '+p.unit+'</div>';
html+='<h2>'+p.sound+'</h2>';
if(p.words&&p.words.length){{html+='<div class="word-grid">';
p.words.forEach(function(w){{html+='<span class="word-chip" style="border-color:rgba(168,85,247,.3);color:#c084fc;background:rgba(168,85,247,.1)" onclick="speakWord(this.textContent)">'+w+'</span>';}});
html+='</div>';}}
if(p.chant)html+='<div class="text-block" id="readText" style="border-color:rgba(168,85,247,.3);white-space:pre-line;font-size:1rem;font-weight:600">'+p.chant+'</div>';
if(p.action)html+='<div class="highlight" style="border-color:rgba(168,85,247,.15)"><strong>Activity:</strong> '+p.action+'</div>';
}}else if(p.type==="workbook"){{
html+='<div class="page-type" style="background:rgba(245,158,11,.12);color:#D97706">Workbook — Unit '+p.unit+'</div>';
html+='<h2>Practice Activities</h2><div id="readText">';
p.activities.forEach(function(a,i){{
html+='<div style="background:rgba(245,158,11,.05);border:1px solid rgba(245,158,11,.15);border-radius:10px;padding:12px 16px;margin:8px 0">';
html+='<div style="color:#D97706;font-weight:700;font-size:.75rem;text-transform:uppercase;margin-bottom:4px">'+a.type+'</div>';
html+='<div style="color:#94A3B8;font-size:.9rem">'+a.instruction+'</div></div>';}});
html+='</div>';
}}else if(p.type==="project"){{
html+='<div class="page-type" style="background:rgba(6,182,212,.12);color:#22d3ee">Project — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
if(p.desc)html+='<div class="text-block" id="readText" style="border-color:rgba(6,182,212,.3)">'+p.desc+'</div>';
if(p.steps&&p.steps.length){{html+='<h3>Steps / Materials</h3>';
p.steps.forEach(function(s,i){{html+='<div class="question" style="border-color:rgba(6,182,212,.3);color:#0891B2">'+(i+1)+'. '+s+'</div>';}});}}
if(p.outcome)html+='<div class="highlight" style="border-color:rgba(6,182,212,.15)"><strong>Outcome:</strong> '+p.outcome+'</div>';
}}else if(p.type==="comic"){{
html+='<div class="page-type" style="background:rgba(244,63,94,.12);color:#E11D48">Comic Strip — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:12px 0" id="readText">';
p.panels.forEach(function(pn,i){{
html+='<div style="background:rgba(244,63,94,.05);border:2px solid rgba(244,63,94,.15);border-radius:12px;padding:12px">';
html+='<div style="font-size:.7rem;color:#E11D48;font-weight:700;margin-bottom:4px">Panel '+(i+1)+'</div>';
html+='<div style="font-size:.8rem;color:#94A3B8;margin-bottom:6px;font-style:italic">'+pn.scene+'</div>';
if(pn.speech)html+='<div style="background:rgba(79,70,229,.04);border-radius:8px;padding:6px 10px;margin:4px 0;font-size:.85rem;color:#E2E8F0">'+pn.speech+'</div>';
if(pn.thought)html+='<div style="background:rgba(79,70,229,.02);border-radius:8px;padding:6px 10px;margin:4px 0;font-size:.8rem;color:#94A3B8;font-style:italic">'+pn.thought+'</div>';
html+='</div>';}});
html+='</div>';
if(p.task)html+='<div class="highlight" style="border-color:rgba(244,63,94,.15)"><strong>Your Turn:</strong> '+p.task+'</div>';
}}else if(p.type==="mission"){{
html+='<div class="page-type" style="background:rgba(234,88,12,.12);color:#EA580C">Real-World Mission — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div style="display:flex;gap:8px;margin:10px 0"><span style="background:rgba(234,88,12,.15);color:#EA580C;padding:4px 12px;border-radius:12px;font-size:.75rem">'+p.difficulty+'</span>';
html+='<span style="background:rgba(234,88,12,.15);color:#EA580C;padding:4px 12px;border-radius:12px;font-size:.75rem">+'+p.xp+' XP</span></div>';
html+='<div class="text-block" id="readText" style="border-color:rgba(234,88,12,.3)">'+p.mission+'</div>';
if(p.evidence)html+='<div class="highlight" style="border-color:rgba(234,88,12,.15)"><strong>Evidence:</strong> '+p.evidence+'</div>';
}}else if(p.type==="escape_room"){{
html+='<div class="page-type" style="background:rgba(220,38,38,.12);color:#f87171">Escape Room — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
html+='<div class="text-block" id="readText" style="border-color:rgba(220,38,38,.3)">'+p.story+'</div>';
html+='<h3>Puzzles</h3>';
p.puzzles.forEach(function(pz,i){{
html+='<div style="background:rgba(220,38,38,.05);border:1px solid rgba(220,38,38,.15);border-radius:10px;padding:10px 14px;margin:6px 0">';
html+='<div style="font-size:.7rem;color:#f87171;font-weight:700;text-transform:uppercase;margin-bottom:4px">Puzzle '+(i+1)+' — '+pz.type+'</div>';
html+='<div style="color:#E2E8F0;font-size:.9rem">'+pz.question+'</div>';
if(pz.hint)html+='<div style="color:#94A3B8;font-size:.8rem;margin-top:4px;font-style:italic">Hint: '+pz.hint+'</div>';
html+='</div>';}});
if(p.reward)html+='<div class="highlight" style="border-color:rgba(220,38,38,.15)"><strong>Reward:</strong> '+p.reward+'</div>';
}}else if(p.type==="family"){{
html+='<div class="page-type" style="background:rgba(139,92,246,.12);color:#7C3AED">Family Corner — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
if(p.activity)html+='<div class="text-block" id="readText" style="border-color:rgba(139,92,246,.3)"><strong>Your Task:</strong> '+p.activity+'</div>';
if(p.together)html+='<div class="highlight" style="border-color:rgba(139,92,246,.15)"><strong>Together:</strong> '+p.together+'</div>';
if(p.parent_q)html+='<div class="rule-box" style="background:linear-gradient(135deg,rgba(139,92,246,.12),rgba(139,92,246,.05));border-color:rgba(139,92,246,.2)">'+p.parent_q+'</div>';
}}else if(p.type==="sel"){{
html+='<div class="page-type" style="background:rgba(236,72,153,.12);color:#DB2777">Social-Emotional Learning — Unit '+p.unit+'</div>';
html+='<h2>'+p.emotion+'</h2>';
if(p.prompt)html+='<div class="text-block" id="readText" style="border-color:rgba(236,72,153,.3)">'+p.prompt+'</div>';
if(p.activity)html+='<div class="highlight" style="border-color:rgba(236,72,153,.15)"><strong>Activity:</strong> '+p.activity+'</div>';
if(p.mindfulness)html+='<div class="rule-box" style="background:linear-gradient(135deg,rgba(236,72,153,.12),rgba(236,72,153,.05));border-color:rgba(236,72,153,.2)"><strong>Mindfulness:</strong> '+p.mindfulness+'</div>';
if(p.discussion)html+='<div class="question" style="border-color:rgba(236,72,153,.3);color:#f9a8d4"><strong>Discussion:</strong> '+p.discussion+'</div>';
}}else if(p.type==="steam"){{
html+='<div class="page-type" style="background:rgba(14,165,233,.12);color:#38bdf8">STEAM Bridge — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
if(p.subject)html+='<div style="display:inline-block;background:rgba(14,165,233,.15);color:#38bdf8;padding:4px 12px;border-radius:12px;font-size:.75rem;margin-bottom:10px">'+p.subject+'</div>';
if(p.task)html+='<div class="text-block" id="readText" style="border-color:rgba(14,165,233,.3)">'+p.task+'</div>';
if(p.vocab&&p.vocab.length){{html+='<h3>Key Vocabulary</h3><div class="word-grid">';
p.vocab.forEach(function(v){{html+='<span class="word-chip" style="border-color:rgba(14,165,233,.3);color:#38bdf8;background:rgba(14,165,233,.1)" onclick="speakWord(this.textContent)">'+v+'</span>';}});
html+='</div>';}}
}}else if(p.type==="podcast"){{
html+='<div class="page-type" style="background:rgba(99,102,241,.12);color:#818cf8">Podcast — Unit '+p.unit+'</div>';
html+='<h2>'+p.title+'</h2>';
if(p.host)html+='<div style="color:#818cf8;font-size:.85rem;margin-bottom:8px"><strong>Host:</strong> '+p.host+'</div>';
if(p.summary)html+='<div class="text-block" id="readText" style="border-color:rgba(99,102,241,.3)">'+p.summary+'</div>';
if(p.segments&&p.segments.length){{html+='<h3>Segments</h3>';
p.segments.forEach(function(s){{html+='<div class="question" style="border-color:rgba(99,102,241,.3);color:#a5b4fc">'+s+'</div>';}});}}
if(p.student_task)html+='<div class="highlight" style="border-color:rgba(99,102,241,.15)"><strong>Your Task:</strong> '+p.student_task+'</div>';
}}
el.innerHTML=html;
document.getElementById("pageInfo").textContent=(cur+1)+" / "+pages.length;
if(speaking)stopTTS();
}}
function nextPage(){{if(cur<pages.length-1){{cur++;var el=document.getElementById("pageArea");
el.classList.add("flip-left");setTimeout(function(){{el.classList.remove("flip-left")}},500);render();}}}}
function prevPage(){{if(cur>0){{cur--;var el=document.getElementById("pageArea");
el.classList.add("flip-right");setTimeout(function(){{el.classList.remove("flip-right")}},500);render();}}}}
function speakWord(w){{synth.cancel();var u=new SpeechSynthesisUtterance(w);u.lang="en-US";u.rate=0.85;synth.speak(u);}}
function toggleTTS(){{if(speaking){{stopTTS();}}else{{startTTS();}}}}
var _ttsOrigHTML="",_ttsSentences=[],_ttsCurSent=0,_ttsAbort=false;
function _splitSentences(text){{
var raw=text.replace(/\\s+/g," ").trim();
var parts=raw.match(/[^.!?\\n]+[.!?]+[\\s]*/g);
if(!parts)return[raw];
var rest=raw;parts.forEach(function(p){{rest=rest.replace(p,"");}});
if(rest.trim())parts.push(rest.trim());
return parts.map(function(s){{return s.trim();}}).filter(function(s){{return s.length>0;}});
}}
function _wrapSentences(el){{
_ttsOrigHTML=el.innerHTML;
var text=el.textContent||"";
var sents=_splitSentences(text);
var html="";
sents.forEach(function(s,i){{
html+='<span class="tts-sentence" data-si="'+i+'">'+s+'</span> ';
}});
el.innerHTML=html;
return el.querySelectorAll(".tts-sentence");
}}
function _clearHL(){{
var el=document.getElementById("readText");
if(el&&_ttsOrigHTML){{el.innerHTML=_ttsOrigHTML;_ttsOrigHTML="";}}
_ttsSentences=[];_ttsCurSent=0;
}}
function _speakNextSentence(){{
if(_ttsAbort||_ttsCurSent>=_ttsSentences.length){{
speaking=false;_ttsAbort=false;
document.getElementById("ttsBtn").classList.remove("speaking");
document.getElementById("ttsBtn").textContent="\U0001F50A Listen";
_clearHL();return;
}}
for(var i=0;i<_ttsSentences.length;i++){{
_ttsSentences[i].classList.remove("active");
if(i<_ttsCurSent)_ttsSentences[i].classList.add("done");
}}
var span=_ttsSentences[_ttsCurSent];
span.classList.add("active");
span.classList.remove("done");
span.scrollIntoView({{behavior:"smooth",block:"center"}});
var txt=span.textContent||"";
var u=new SpeechSynthesisUtterance(txt);u.lang="en-US";u.rate=0.82;
u.onend=function(){{
if(_ttsAbort)return;
span.classList.remove("active");span.classList.add("done");
_ttsCurSent++;_speakNextSentence();
}};
synth.speak(u);
}}
function startTTS(){{
_ttsAbort=false;
var el=document.getElementById("readText");
if(!el){{var p=pages[cur];
var txt=p.text||p.passage||p.script||p.model||p.rule||"";
if(!txt)return;
var u=new SpeechSynthesisUtterance(txt);u.lang="en-US";u.rate=0.82;
u.onend=function(){{speaking=false;document.getElementById("ttsBtn").classList.remove("speaking");
document.getElementById("ttsBtn").textContent="\U0001F50A Listen";}};
speaking=true;document.getElementById("ttsBtn").classList.add("speaking");
document.getElementById("ttsBtn").textContent="\u23F9 Stop";synth.speak(u);return;}}
_ttsSentences=Array.from(_wrapSentences(el));
_ttsCurSent=0;
speaking=true;
document.getElementById("ttsBtn").classList.add("speaking");
document.getElementById("ttsBtn").textContent="\u23F9 Stop";
_speakNextSentence();
}}
function stopTTS(){{_ttsAbort=true;synth.cancel();speaking=false;
document.getElementById("ttsBtn").classList.remove("speaking");
document.getElementById("ttsBtn").textContent="\U0001F50A Listen";_clearHL();}}
function showTOC(){{
var list=document.getElementById("tocList");list.innerHTML="";
pages.forEach(function(p,i){{
var li=document.createElement("li");
var label="";
if(p.type==="cover")label="Cover";
else if(p.type==="unit_opener")label='<span class="toc-unit">Unit '+p.unit+'</span>'+p.title;
else label='<span class="toc-unit">Unit '+(p.unit||"")+'</span>'+p.type.charAt(0).toUpperCase()+p.type.slice(1).replace("_"," ")+(p.title?" — "+p.title:"");
li.innerHTML=label;li.onclick=function(){{cur=i;render();closeTOC();}};list.appendChild(li);}});
document.getElementById("tocOverlay").style.display="block";}}
function closeTOC(){{document.getElementById("tocOverlay").style.display="none";}}
document.addEventListener("keydown",function(e){{if(e.key==="ArrowRight")nextPage();if(e.key==="ArrowLeft")prevPage();if(e.key==="Escape")closeTOC();}});
render();
</script></body></html>'''
