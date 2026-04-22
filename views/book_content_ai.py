"""
AI-Powered Original Course Book Content Generator
=================================================
Her ünite için OpenAI ile orijinal, zengin içerik üretir ve cache'ler.
Bir kez üretilen içerik JSON dosyasına kaydedilir — tekrar API çağrısı yapılmaz.
"""
import json
import os
from typing import Any

_CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "book_content")


def _get_client():
    """OpenAI client oluştur."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            for line in open(env_path, encoding="utf-8"):
                if line.strip().startswith("OPENAI_API_KEY"):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        return None
    from openai import OpenAI
    return OpenAI(api_key=api_key)


def _cache_path(grade: int, unit_num: int) -> str:
    """Cache dosya yolu."""
    os.makedirs(_CACHE_DIR, exist_ok=True)
    return os.path.join(_CACHE_DIR, f"grade{grade}_unit{unit_num}.json")


def _load_cache(grade: int, unit_num: int) -> dict | None:
    """Cache'den yükle."""
    path = _cache_path(grade, unit_num)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def _save_cache(grade: int, unit_num: int, content: dict):
    """Cache'e kaydet."""
    path = _cache_path(grade, unit_num)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


BOOK_NAMES = {
    0: "Early Steps", 1: "Bright Start 1", 2: "Bright Start 2",
    3: "Bright Start 3", 4: "Bright Start 4",
    5: "Next Level 5", 6: "Next Level 6", 7: "Next Level 7", 8: "Next Level 8",
    9: "English Core 9", 10: "English Core 10", 11: "English Core 11", 12: "English Core 12",
}


def generate_unit_content(grade: int, unit_num: int, theme: str, vocab: list[str],
                          structure: str, skills: dict, theme_tr: str = "") -> dict | None:
    """Bir ünite için AI ile orijinal içerik üret. Cache varsa direkt döndür."""
    # Cache kontrol
    cached = _load_cache(grade, unit_num)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return None

    book_name = BOOK_NAMES.get(grade, f"Grade {grade}")
    vocab_str = ", ".join(vocab[:20])

    # Kademe bilgisi
    if grade == 0:
        level_desc = "Okul öncesi (5-6 yaş). Çok basit, kısa cümleler. Emoji ve resim açıklamaları ekle."
        word_count = "30-40"
        story_len = "4-5 cümle"
        dialog_len = "4 satır"
        exercise_level = "çok basit, resim eşleştirme tarzı"
    elif grade <= 2:
        level_desc = f"{grade}. sınıf ilkokul (6-8 yaş). Basit ve eğlenceli. Kısa cümleler."
        word_count = "50-70"
        story_len = "6-8 cümle"
        dialog_len = "6 satır"
        exercise_level = "basit, eşleştirme ve boşluk doldurma"
    elif grade <= 4:
        level_desc = f"{grade}. sınıf ilkokul (8-10 yaş). Orta zorluk. Paragraf düzeyinde."
        word_count = "80-100"
        story_len = "8-10 cümle"
        dialog_len = "8 satır"
        exercise_level = "orta zorluk, cümle kurma ve kısa paragraf"
    elif grade <= 8:
        level_desc = f"{grade}. sınıf ortaokul (10-14 yaş). Akademik dil. Paragraflar."
        word_count = "120-150"
        story_len = "12-15 cümle"
        dialog_len = "10 satır"
        exercise_level = "orta-ileri, paragraf yazma ve analiz"
    else:
        level_desc = f"{grade}. sınıf lise (14-18 yaş). İleri düzey. Akademik yazım."
        word_count = "150-200"
        story_len = "15-20 cümle"
        dialog_len = "12 satır"
        exercise_level = "ileri düzey, essay ve tartışma"

    prompt = f"""You are creating original English language textbook content for {book_name}, Unit {unit_num}.
Theme: {theme} ({theme_tr})
Level: {level_desc}
Target vocabulary: {vocab_str}
Grammar structure: {structure}
Skills: {json.dumps(skills, ensure_ascii=False)}

Create ORIGINAL, CREATIVE, ENGAGING content. NOT generic. Each piece must be unique and interesting.

Return a JSON object with these fields:

{{
  "theme_intro": "A warm, engaging introduction to the unit theme ({word_count} words). Address the student directly. Make them curious about the topic.",

  "story": {{
    "title": "An original story title",
    "text": "An original story ({story_len}) using the target vocabulary naturally. The story should be interesting, have a beginning-middle-end, and teach a life lesson. Use the vocabulary words in context.",
    "moral": "One sentence moral/lesson"
  }},

  "dialogue": {{
    "title": "Dialogue title (situation description)",
    "speakers": ["Speaker A name", "Speaker B name"],
    "lines": [
      {{"speaker": 0, "text": "First line..."}},
      {{"speaker": 1, "text": "Response..."}},
      // {dialog_len} total lines, natural conversation using vocabulary and structure
    ]
  }},

  "reading_passage": {{
    "title": "Reading passage title",
    "text": "An informative/interesting reading text ({word_count} words) related to the theme. Include facts, examples. Use target vocabulary.",
    "questions": [
      "Comprehension question 1?",
      "Comprehension question 2?",
      "Comprehension question 3?",
      "Inference question?",
      "Personal response question?"
    ]
  }},

  "grammar_focus": {{
    "rule": "Clear grammar rule explanation with the structure: {structure}",
    "examples": [
      "Example sentence 1 (with structure highlighted)",
      "Example sentence 2",
      "Example sentence 3",
      "Example sentence 4"
    ],
    "tip": "A helpful memory tip or mnemonic"
  }},

  "vocabulary_enrichment": {{
    "definitions": [
      {{"word": "word1", "definition": "Simple English definition", "example": "Word used in a sentence", "turkish_hint": "Türkçe ipucu"}},
      // for each vocabulary word
    ],
    "word_families": [
      {{"base": "word", "noun": "...", "verb": "...", "adjective": "..."}},
      // 3-4 word families
    ]
  }},

  "exercises": {{
    "fill_blanks": [
      {{"sentence": "I ___ to school every day.", "answer": "go", "options": ["go", "goes", "going", "went"]}},
      // 5 fill-in-the-blank with 4 options each
    ],
    "matching": [
      {{"left": "word/phrase", "right": "definition/translation"}},
      // 6 matching pairs
    ],
    "reorder": [
      {{"words": ["I", "like", "playing", "football"], "answer": "I like playing football."}},
      // 3 sentence reordering
    ],
    "writing_prompt": "A creative writing task related to the theme ({exercise_level})"
  }},

  "song_chant": {{
    "title": "Song/chant title",
    "lyrics": "4-6 line rhyming song/chant using vocabulary. Fun and memorable."
  }},

  "culture_corner": {{
    "title": "Culture corner title",
    "text": "Interesting cultural fact or comparison related to the theme (3-4 sentences)."
  }},

  "fun_fact": "An amazing, surprising fact related to the unit theme that students will love."
}}

IMPORTANT:
- ALL content must be in English (this is an English course)
- Use the target vocabulary naturally throughout
- Content must be AGE-APPROPRIATE for {level_desc}
- Be CREATIVE and ORIGINAL — no generic textbook language
- Make it FUN and ENGAGING
- Return VALID JSON only"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert English language textbook author. Create original, creative, grade-appropriate content. Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=3000,
            response_format={"type": "json_object"},
        )

        content_str = response.choices[0].message.content.strip()
        content = json.loads(content_str)
        content["_meta"] = {
            "grade": grade, "unit": unit_num, "theme": theme,
            "book": book_name, "vocab_count": len(vocab),
        }

        # Cache'e kaydet
        _save_cache(grade, unit_num, content)
        return content

    except Exception as e:
        print(f"AI content generation error: {e}")
        return None


def generate_all_units(grade: int, curriculum_weeks: list,
                       progress_callback=None) -> list[dict]:
    """Tüm ünitelerin içeriğini üret. Cache'de varsa hızlı döner."""
    # Ünite grupla
    units = []
    wpu = max(1, len(curriculum_weeks) // 10)
    for i in range(0, len(curriculum_weeks), wpu):
        uw = curriculum_weeks[i:i + wpu]
        all_vocab = []
        for w in uw:
            all_vocab.extend(w.get("vocab", []))
        all_vocab = list(dict.fromkeys(all_vocab))

        units.append({
            "num": len(units) + 1,
            "theme": uw[0].get("theme", f"Unit {len(units) + 1}"),
            "theme_tr": uw[0].get("theme_tr", ""),
            "vocab": all_vocab,
            "structure": uw[0].get("structure", ""),
            "skills": uw[0].get("skills", {}),
            "weeks": uw,
        })

    results = []
    for i, unit in enumerate(units):
        if progress_callback:
            progress_callback(i, len(units), unit["theme"])

        content = generate_unit_content(
            grade, unit["num"], unit["theme"], unit["vocab"],
            unit["structure"], unit["skills"], unit["theme_tr"],
        )
        results.append({
            "unit": unit,
            "content": content,
        })

    return results
