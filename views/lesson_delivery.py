"""
SmartCampusAI — Premium Lesson Delivery Engine v3
===================================================
TAM OTOMATİK DERS ANLATIM MOTORU
Öğretmen açar → bugünün dersi eksiksiz akar.
Plan + 4 Kitap + Etkinlikler + Telaffuz + Alıştırma = Tek akış.
0-12. sınıf tüm kademeler.
"""

from __future__ import annotations

import json
import streamlit as st
import streamlit.components.v1 as components

from models.lesson_delivery import (
    BTN_TO_AI_CONTENT, BTN_TO_BOOKS, BOOK_LABELS, BTN_LABELS, DAY_NAMES,
    week_to_unit, get_grade_num, load_unit_content,
    get_content_for_step, get_books_for_step, get_step_label,
    get_today_info, LessonDeliveryStore, StudentResponse,
)
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("yabanci_dil")
except Exception:
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# CSS — Premium dark theme
# ═══════════════════════════════════════════════════════════════════════════════

_CSS = """<style>
.ld-hero{background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);
border-radius:16px;padding:24px 28px;margin-bottom:16px;border:1.5px solid rgba(99,102,241,.25);}
.ld-hero h2{margin:0;color:#c7d2fe;font-size:1.3rem;}
.ld-hero .sub{color:#818cf8;font-size:.88rem;margin-top:4px;}
.ld-hero .meta{color:#64748b;font-size:.78rem;margin-top:6px;}
.ld-phase{background:linear-gradient(135deg,#131825,#1a2035);border-radius:14px;
padding:18px 22px;margin:14px 0;border:1px solid rgba(99,102,241,.15);}
.ld-phase-title{font-size:1.05rem;font-weight:700;margin:0 0 4px 0;}
.ld-phase-sub{font-size:.78rem;color:#94A3B8;margin:0;}
.ld-card{background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.1);
border-radius:12px;padding:16px 20px;margin:8px 0;}
.ld-card-title{font-size:.95rem;font-weight:700;color:#818cf8;margin-bottom:8px;
padding-bottom:6px;border-bottom:1px solid rgba(99,102,241,.1);}
.ld-vocab{display:inline-block;background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.15);
border-radius:8px;padding:8px 14px;margin:4px;text-align:center;min-width:90px;}
.ld-vocab b{display:block;color:#818cf8;font-size:.95rem;}
.ld-vocab small{color:#94A3B8;font-size:.72rem;}
.ld-story{background:rgba(139,92,246,.06);border-left:4px solid #8B5CF6;
border-radius:0 10px 10px 0;padding:16px 20px;margin:10px 0;color:#cbd5e1;
font-size:.92rem;line-height:1.7;}
.ld-rule{background:rgba(16,185,129,.06);border-left:4px solid #10B981;
border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;}
.ld-rule b{color:#10B981;} .ld-rule span{color:#94A3B8;}
.ld-dlg{padding:5px 0;font-size:.9rem;}
.ld-dlg .a{color:#60a5fa;font-weight:600;} .ld-dlg .b{color:#34d399;font-weight:600;}
.ld-song{text-align:center;color:#c084fc;font-size:.92rem;padding:3px 0;}
.ld-fact{background:rgba(245,158,11,.06);border-left:4px solid #f59e0b;
border-radius:0 10px 10px 0;padding:12px 16px;margin:10px 0;}
.ld-fact b{color:#f59e0b;} .ld-fact span{color:#94A3B8;}
.ld-badge{display:inline-block;border-radius:6px;padding:2px 8px;
font-size:.7rem;font-weight:600;margin:2px 4px 2px 0;}
.ld-badge-book{background:rgba(16,185,129,.1);color:#10B981;}
.ld-badge-time{background:rgba(99,102,241,.15);color:#818cf8;}
.ld-progress{background:rgba(99,102,241,.1);border-radius:8px;height:8px;overflow:hidden;}
.ld-progress-fill{background:linear-gradient(90deg,#6366F1,#8B5CF6);height:100%;border-radius:8px;}
</style>"""


def _css():
    st.markdown(_CSS, unsafe_allow_html=True)


def _ld_write_gunluk_ozet(session_data: dict, done_list: list):
    """Tamamlanan ders oturumunu gunluk_ozet.json'a yaz."""
    try:
        from views.yd_tools import _save_eng_gunluk_ozet
        from datetime import date

        sinif = session_data.get("sinif") or session_data.get("grade", 0)
        sube = session_data.get("sube", "")
        week = session_data.get("week", 1)
        theme = session_data.get("theme", "")
        theme_tr = session_data.get("theme_tr", "")
        vocab = session_data.get("vocab", [])
        structure = session_data.get("structure", "")
        unit_num = session_data.get("unit_num", 1)
        teacher_name = session_data.get("teacher_name", "")
        total_phases = 9  # warmup, vocab, grammar, listening, reading, writing, song, exercises, review
        done_count = len(done_list) if done_list else 0

        ozet = {
            "tarih": date.today().isoformat(),
            "sinif": sinif,
            "sube": sube,
            "hafta": week,
            "unite": unit_num,
            "theme": theme,
            "theme_tr": theme_tr,
            "vocab": vocab,
            "structure": structure,
            "ogretmen": teacher_name,
            "islendi": True,
            "tamamlanan_fazlar": done_list or [],
            "faz_sayisi": f"{done_count}/{total_phases}",
            "tamamlanma_yuzde": round(done_count / total_phases * 100) if total_phases else 0,
            "session_id": session_data.get("id", ""),
            "kaynak": "ders_isleme_motoru",
        }
        _save_eng_gunluk_ozet(ozet)
    except Exception:
        pass  # Gunluk ozet yazimi UI'yi bloke etmemeli


# ═══════════════════════════════════════════════════════════════════════════════
# FAZ TANIMLARI — Öğretmen Ders Akışı
# ═══════════════════════════════════════════════════════════════════════════════

_TEACHER_PHASES = [
    {"key": "warmup", "icon": "\U0001F31F", "label": "Warm-up \u00B7 Is\u0131nma",
     "lesson": 1, "minutes": 5,
     "desc": "Derse haz\u0131rl\u0131k \u2014 motivasyon ve \u00F6n bilgi aktivasyonu"},
    {"key": "vocabulary", "icon": "\U0001F4DA", "label": "Vocabulary \u00B7 Kelime",
     "lesson": 1, "minutes": 15,
     "desc": "Yeni kelimeler \u2014 tan\u0131m, \u00F6rnek, telaffuz, oyun"},
    {"key": "grammar", "icon": "\U0001F4DD", "label": "Grammar \u00B7 Dilbilgisi",
     "lesson": 1, "minutes": 15,
     "desc": "Yap\u0131 \u00F6\u011Fretimi \u2014 kural, \u00F6rnek, uygulama"},
    {"key": "listening", "icon": "\U0001F3A7", "label": "Listening & Speaking",
     "lesson": 1, "minutes": 5,
     "desc": "Diyalog, telaffuz, ileti\u015Fim becerileri"},
    {"key": "reading", "icon": "\U0001F4D6", "label": "Reading \u00B7 Okuma",
     "lesson": 2, "minutes": 10,
     "desc": "Okuma metni \u2014 anlama, analiz, kelime \u00E7al\u0131\u015Fmas\u0131"},
    {"key": "writing", "icon": "\u270D\uFE0F", "label": "Writing \u00B7 Yazma",
     "lesson": 2, "minutes": 10,
     "desc": "Y\u00F6nlendirilmi\u015F yazma \u2014 planlama, yazma, d\u00FCzeltme"},
    {"key": "song", "icon": "\U0001F3B5", "label": "Song & Culture",
     "lesson": 2, "minutes": 5,
     "desc": "M\u00FCzik ile \u00F6\u011Frenme ve k\u00FClt\u00FCrler aras\u0131 fark\u0131ndal\u0131k"},
    {"key": "exercises", "icon": "\U0001F4DD", "label": "Exercises \u00B7 Al\u0131\u015Ft\u0131rma",
     "lesson": 2, "minutes": 10,
     "desc": "Peki\u015Ftirme \u2014 doldurun, e\u015Fleyin, s\u0131ralay\u0131n"},
    {"key": "review", "icon": "\U0001F3C6", "label": "Review \u00B7 Tekrar",
     "lesson": 2, "minutes": 5,
     "desc": "\u00D6\u011Frenilenlerin tekrar\u0131 ve de\u011Ferlendirme"},
]


def _render_teacher_phase(key, ai, vocab, theme, theme_tr, structure, week_data, level, ukey):
    """Tek bir faz\u0131 render et."""
    if key == "warmup":
        _phase_warmup(ai, vocab, theme, theme_tr)
    elif key == "vocabulary":
        _phase_vocabulary(ai, vocab, theme, week_data, level)
    elif key == "grammar":
        _phase_grammar(ai, structure, week_data, level, ukey)
    elif key == "reading":
        _phase_reading(ai, week_data, level, ukey)
    elif key == "listening":
        _phase_listening_speaking(ai, vocab, week_data, level)
    elif key == "writing":
        _phase_writing(ai, theme, week_data, level, ukey)
    elif key == "song":
        _phase_song_culture(ai, week_data, level)
    elif key == "exercises":
        _phase_exercises(ai, ukey)
    elif key == "review":
        _phase_review(ai, vocab, theme, ukey)


# ═══════════════════════════════════════════════════════════════════════════════
# 1) GERİ SAYIM ZAMANLAYICISI
# ═══════════════════════════════════════════════════════════════════════════════

def _countdown_timer(minutes: int, phase_key: str):
    """JS tabanl\u0131 geri say\u0131m timer\u0131 \u2014 alarm sesli."""
    secs = minutes * 60
    components.html(f"""
    <div id="timer_{phase_key}" style="font-family:system-ui;text-align:center;
    background:linear-gradient(135deg,#0f172a,#1e1b4b);border-radius:12px;
    padding:12px 20px;border:1.5px solid rgba(99,102,241,.2);margin-bottom:10px;">
    <div style="display:flex;align-items:center;justify-content:center;gap:14px;">
    <div id="disp_{phase_key}" style="font-size:1.6rem;font-weight:800;
    color:#818cf8;font-variant-numeric:tabular-nums;letter-spacing:2px;">
    {minutes:02d}:00</div>
    <button id="btn_{phase_key}" onclick="toggleTimer()" style="background:#6366F1;
    color:#fff;border:none;padding:6px 16px;border-radius:8px;font-weight:700;
    cursor:pointer;font-size:13px;">\u25B6 Ba\u015Flat</button>
    <button onclick="resetTimer()" style="background:rgba(255,255,255,.08);
    color:#94A3B8;border:1px solid rgba(255,255,255,.1);padding:6px 12px;
    border-radius:8px;font-size:12px;cursor:pointer;">\u21BB</button>
    </div>
    <div style="background:rgba(99,102,241,.1);border-radius:4px;height:4px;
    margin-top:8px;overflow:hidden;">
    <div id="bar_{phase_key}" style="height:100%;width:100%;
    background:linear-gradient(90deg,#6366F1,#8B5CF6);border-radius:4px;
    transition:width 1s linear;"></div></div></div>
    <script>
    (function(){{
      let total={secs},left={secs},running=false,iv=null;
      const d=document.getElementById('disp_{phase_key}');
      const b=document.getElementById('btn_{phase_key}');
      const bar=document.getElementById('bar_{phase_key}');
      function fmt(s){{const m=Math.floor(s/60);const ss=s%60;
        return String(m).padStart(2,'0')+':'+String(ss).padStart(2,'0');}}
      function tick(){{
        if(left<=0){{clearInterval(iv);running=false;
          d.style.color='#ef4444';d.textContent='00:00';
          b.textContent='\u25B6 Ba\u015Flat';
          try{{const ac=new(window.AudioContext||window.webkitAudioContext)();
            const o=ac.createOscillator();o.type='sine';o.frequency.value=880;
            const g=ac.createGain();g.gain.value=0.3;o.connect(g);g.connect(ac.destination);
            o.start();setTimeout(()=>o.stop(),600);}}catch(e){{}}
          return;}}
        left--;d.textContent=fmt(left);
        bar.style.width=(left/total*100)+'%';
        if(left<=60)d.style.color='#f59e0b';
        if(left<=10)d.style.color='#ef4444';
      }}
      window.toggleTimer=function(){{
        if(running){{clearInterval(iv);running=false;b.textContent='\u25B6 Devam';}}
        else{{running=true;b.textContent='\u23F8 Duraklat';iv=setInterval(tick,1000);}}
      }};
      window.resetTimer=function(){{
        clearInterval(iv);running=false;left=total;
        d.textContent=fmt(left);d.style.color='#818cf8';
        bar.style.width='100%';b.textContent='\u25B6 Ba\u015Flat';
      }};
    }})();
    </script>""", height=80)


# ═══════════════════════════════════════════════════════════════════════════════
# 2) ÖĞRETMEN REHBER NOTLARI
# ═══════════════════════════════════════════════════════════════════════════════

_TEACHER_GUIDES: dict[str, dict] = {
    "warmup": {
        "title": "\U0001F31F Is\u0131nma Rehberi",
        "steps": [
            "\U0001F44B S\u0131n\u0131f\u0131 selamla: 'Good morning/afternoon, class!'",
            "\U0001F4AC G\u00FCn\u00FCn sorusu sor: 'How are you today?' \u2014 birka\u00E7 \u00F6\u011Frenciden cevap al",
            "\U0001F4A1 Fun Fact'i oku veya projeksiyonda g\u00F6ster",
            "\U0001F4DA Haftan\u0131n anahtar kelimelerini tahtaya yaz, \u00F6\u011Frencilere tekrarlat",
            "\u23F0 5 dakikay\u0131 ge\u00E7me \u2014 enerjiyi y\u00FCksek tut, h\u0131zl\u0131 ge\u00E7",
        ],
        "tip": "\u00D6\u011Frencilerin dikkatini \u00E7ekmek i\u00E7in ilk 30 saniye kritik. G\u00FCleryy\u00FCzle ba\u015Fla, enerji ver.",
    },
    "vocabulary": {
        "title": "\U0001F4DA Kelime \u00D6\u011Fretim Rehberi",
        "steps": [
            "\U0001F4DD Kelimeleri birer birer tan\u0131t: s\u00F6yle \u2192 tekrarlat \u2192 anlam\u0131n\u0131 sor",
            "\U0001F50A Her kelimeyi 3 kez sesli tekrarlat (choral repetition)",
            "\U0001F3AE Flashcard etkinli\u011Fini projeksiyonda a\u00E7, \u00F6\u011Frencileri kat",
            "\U0001F4AC C\u00FCmle i\u00E7inde kulland\u0131r: 'Make a sentence with [word]'",
            "\u270D\uFE0F Defterlerine yazd\u0131r: kelime + anlam + \u00F6rnek c\u00FCmle",
        ],
        "tip": "Kelime ba\u015F\u0131na 1-1.5 dk ay\u0131r. 10+ kelimeyi 15 dk'da bitirmek i\u00E7in tempo \u00F6nemli.",
    },
    "grammar": {
        "title": "\U0001F4DD Dilbilgisi \u00D6\u011Fretim Rehberi",
        "steps": [
            "\U0001F4D0 Kural\u0131 tahtaya yaz veya projeksiyonda g\u00F6ster",
            "\u2705 2-3 \u00F6rnek c\u00FCmle yaz, \u00F6\u011Frencilerden de \u00F6rnek iste",
            "\u274C Yanl\u0131\u015F \u00F6rnek ver, 'What's wrong?' diye sor",
            "\U0001F3AE \u0130nteraktif grammar etkinli\u011Fini a\u00E7, s\u0131n\u0131f\u00E7a \u00E7\u00F6z\u00FCn",
            "\u270D\uFE0F Fill in the blanks al\u0131\u015Ft\u0131rmas\u0131n\u0131 bireysel yapt\u0131r",
        ],
        "tip": "Kural\u0131 ezberletme, kal\u0131p olarak \u00F6\u011Fret. '\u015Eimdi + fiil' gibi basit form\u00FCl ver.",
    },
    "listening": {
        "title": "\U0001F3A7 Dinleme & Konu\u015Fma Rehberi",
        "steps": [
            "\U0001F50A Diyalogu \u00F6nce dinletin (TTS butonu), kitap kapal\u0131",
            "\u2753 'What did you hear?' \u2014 genel anlama sorusu sor",
            "\U0001F50A \u0130kinci dinlemede metni g\u00F6ster, takip ettir",
            "\U0001F465 Pair work: \u00D6\u011Frenciler ikili diyalog pratik yaps\u0131n",
            "\U0001F3A4 G\u00F6n\u00FCll\u00FCleri s\u0131n\u0131f \u00F6n\u00FCnde canland\u0131rmaya davet et",
        ],
        "tip": "Dinleme zor olabilir \u2014 h\u0131z\u0131 yava\u015Flat, 2 kez dinlet. Anlamad\u0131lar m\u0131 bir daha \u00E7al.",
    },
    "reading": {
        "title": "\U0001F4D6 Okuma Rehberi",
        "steps": [
            "\U0001F4D6 \u00D6nce ba\u015Fl\u0131k ve resimlere bak: 'What do you think this is about?'",
            "\U0001F50A Sessiz okuma (2 dk), sonra sesli okuma (\u00F6\u011Frenciler s\u0131rayla)",
            "\U0001F4AC Anlama sorular\u0131n\u0131 s\u00F6zel sor, sonra yaz\u0131l\u0131 yapt\u0131r",
            "\U0001F4DD Bilmedi\u011Fi kelimeleri i\u015Faretlettir, birlikte \u00E7\u00F6z\u00FCn",
            "\U0001F3AE \u0130nteraktif okuma etkinli\u011Fini a\u00E7",
        ],
        "tip": "Okuma \u00F6ncesi tahmin (prediction) yapt\u0131r \u2014 motivasyonu art\u0131r\u0131r.",
    },
    "writing": {
        "title": "\u270D\uFE0F Yazma Rehberi",
        "steps": [
            "\U0001F4AC \u00D6nce s\u00F6zel beyin f\u0131rt\u0131nas\u0131: 'What can we write about [topic]?'",
            "\U0001F4D0 Tahtada \u00F6rnek c\u00FCmle yaz\u0131n (model writing)",
            "\u270D\uFE0F \u00D6\u011Frenciler bireysel yazs\u0131n (5-7 dk sessiz \u00E7al\u0131\u015Fma)",
            "\U0001F465 Pair check: Birbirlerinin yaz\u0131s\u0131n\u0131 okusun",
            "\U0001F44F 2-3 g\u00F6n\u00FCll\u00FC s\u0131n\u0131fa okusun",
        ],
        "tip": "Hata d\u00FCzeltmeyi hemen yapma. \u00D6nce i\u00E7eri\u011Fi takdir et, sonra 1-2 d\u00FCzeltme \u00F6ner.",
    },
    "song": {
        "title": "\U0001F3B5 \u015Eark\u0131 & K\u00FClt\u00FCr Rehberi",
        "steps": [
            "\U0001F3B5 \u015Eark\u0131y\u0131 \u00F6nce dinletin, sonra s\u00F6zlerle birlikte",
            "\U0001F3A4 Hep birlikte s\u00F6yleyin (en az 2 kez)",
            "\U0001F30D K\u00FClt\u00FCr k\u00F6\u015Fesini okuyun, T\u00FCrkiye ile kar\u015F\u0131la\u015Ft\u0131r\u0131n",
            "\U0001F4AC '\u00DClkemizde bu nas\u0131l?' sorusu ile tart\u0131\u015Fma a\u00E7",
        ],
        "tip": "\u015Eark\u0131da hareket/el i\u015Fareti ekle \u2014 k\u00FC\u00E7\u00FCk s\u0131n\u0131flarda \u00E7ok etkili.",
    },
    "exercises": {
        "title": "\U0001F4DD Al\u0131\u015Ft\u0131rma Rehberi",
        "steps": [
            "\U0001F4CB \u0130lk soruyu birlikte \u00E7\u00F6z\u00FCn (\u00F6rnek g\u00F6ster)",
            "\u270D\uFE0F Kalan\u0131 bireysel \u00E7\u00F6zs\u00FCnler (5-7 dk)",
            "\u2705 S\u0131n\u0131f\u00E7a kontrol: 'Number 1, who has the answer?'",
            "\U0001F465 Zorlananlara pair help \u00F6ner",
        ],
        "tip": "H\u0131zl\u0131 bitirenlere bonus soru ver \u2014 beklemek can s\u0131k\u0131nt\u0131s\u0131 yarat\u0131r.",
    },
    "review": {
        "title": "\U0001F3C6 Tekrar & Kapan\u0131\u015F Rehberi",
        "steps": [
            "\U0001F4AC 'What did we learn today?' sorusu ile ba\u015Flat",
            "\U0001F9E0 Mini quiz'i projeksiyonda g\u00F6ster, el kald\u0131rarak cevaplay\u0131n",
            "\U0001F4DD \u00D6dev varsa a\u00E7\u0131kla",
            "\U0001F44F 'Well done, class! See you next time!'",
        ],
        "tip": "Son 1 dk'da mutlaka olumlu kapat. 'Harika \u00E7al\u0131\u015Ft\u0131n\u0131z!' motivasyonu korur.",
    },
}


def _render_teacher_guide(phase_key: str):
    """Faz i\u00E7in \u00F6\u011Fretmen rehber notlar\u0131n\u0131 g\u00F6ster."""
    guide = _TEACHER_GUIDES.get(phase_key)
    if not guide:
        return
    with st.expander(f"{guide['title']} — Ne Söyle, Ne Yap", expanded=False):
        for step in guide["steps"]:
            st.markdown(f"- {step}")
        if guide.get("tip"):
            st.info(f"\U0001F4A1 **\u0130pucu:** {guide['tip']}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3) RASTGELE ÖĞRENCİ SEÇİCİ
# ═══════════════════════════════════════════════════════════════════════════════

def _random_student_picker(sinif: int, sube: str):
    """S\u0131n\u0131f listesinden rastgele \u00F6\u011Frenci se\u00E7 \u2014 animasyonlu JS."""
    # Öğrenci listesini yükle
    try:
        from utils.shared_data import load_shared_students
        students = load_shared_students()
        names = [s.get("ad", "") + " " + s.get("soyad", "")
                 for s in students
                 if s.get("sinif") == str(sinif) and s.get("sube", "A") == sube]
    except Exception:
        names = []

    if not names:
        names = [f"\u00D6\u011Frenci {i+1}" for i in range(25)]

    names_js = json.dumps(names, ensure_ascii=False)
    components.html(f"""
    <div style="font-family:system-ui;text-align:center;background:linear-gradient(135deg,#0f172a,#1e1b4b);
    border-radius:12px;padding:16px;border:1.5px solid rgba(99,102,241,.2);">
    <div style="font-size:.8rem;color:#64748b;margin-bottom:6px;">\U0001F3B2 S\u0131radaki Kim?</div>
    <div id="rsp_name" style="font-size:1.4rem;font-weight:800;color:#818cf8;
    min-height:36px;margin-bottom:10px;">\u2014</div>
    <button id="rsp_btn" onclick="pick()" style="background:linear-gradient(135deg,#6366F1,#8B5CF6);
    color:#fff;border:none;padding:8px 24px;border-radius:10px;font-weight:700;
    cursor:pointer;font-size:14px;transition:all .2s;">\U0001F3B2 Se\u00E7</button>
    </div>
    <script>
    (function(){{
      const N={names_js};
      const el=document.getElementById('rsp_name');
      const btn=document.getElementById('rsp_btn');
      let iv=null;
      window.pick=function(){{
        btn.disabled=true;
        let count=0;const total=15;
        iv=setInterval(()=>{{
          el.textContent=N[Math.floor(Math.random()*N.length)];
          el.style.color=count<total-3?'#94A3B8':'#f59e0b';
          count++;
          if(count>=total){{
            clearInterval(iv);
            const winner=N[Math.floor(Math.random()*N.length)];
            el.textContent='\U0001F31F '+winner+' \U0001F31F';
            el.style.color='#22c55e';el.style.fontSize='1.6rem';
            btn.disabled=false;
            setTimeout(()=>{{el.style.fontSize='1.4rem';}},2000);
          }}
        }},100);
      }};
    }})();
    </script>""", height=120)


# ═══════════════════════════════════════════════════════════════════════════════
# 4) SUNUM MODU CSS
# ═══════════════════════════════════════════════════════════════════════════════

def _toggle_presentation_mode():
    """Sunum modu toggle \u2014 projeksiyon i\u00E7in b\u00FCy\u00FCk font, temiz g\u00F6r\u00FCn\u00FCm."""
    key = "_ld_presentation"
    is_on = st.session_state.get(key, False)
    if st.button(
            "\U0001F4FA Sunum Modu: A\u00C7IK" if is_on else "\U0001F4FA Sunum Modu",
            type="primary" if is_on else "secondary"):
        st.session_state[key] = not is_on
        st.rerun()

    if is_on:
        st.markdown("""<style>
        /* Sunum modu — projeksiyon/akıllı tahta */
        section[data-testid="stSidebar"]{display:none !important;}
        header[data-testid="stHeader"]{display:none !important;}
        .block-container{padding:1rem 2rem !important;max-width:100% !important;}
        .ld-phase-title{font-size:1.5rem !important;}
        .ld-phase-sub{font-size:1rem !important;}
        .ld-card{font-size:1.1rem !important;}
        .ld-card-title{font-size:1.2rem !important;}
        .ld-vocab b{font-size:1.3rem !important;}
        .ld-story{font-size:1.1rem !important;line-height:2 !important;}
        .ld-rule b,.ld-rule span{font-size:1.1rem !important;}
        .ld-dlg{font-size:1.1rem !important;}
        .ld-song{font-size:1.1rem !important;}
        div[data-testid="stMarkdownContainer"] p{font-size:1.05rem !important;}
        div[data-testid="stExpander"] summary{font-size:1.1rem !important;}
        </style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 5) ÇIKIŞ BİLETİ (EXIT TICKET)
# ═══════════════════════════════════════════════════════════════════════════════

def _exit_ticket(ai: dict, vocab: list[str], theme: str, ukey: str):
    """\u00C7\u0131k\u0131\u015F bileti \u2014 ders sonu 3 soru h\u0131zl\u0131 de\u011Ferlendirme."""
    st.markdown(
        '<div class="ld-phase" style="border-left:4px solid #f59e0b;">'
        '<p class="ld-phase-title" style="color:#f59e0b;">'
        '\U0001F3AB \u00C7\u0131k\u0131\u015F Bileti \u2014 Exit Ticket</p>'
        '<p class="ld-phase-sub">'
        '3 h\u0131zl\u0131 soru \u2014 \u00F6\u011Frenciler ka\u011F\u0131da veya s\u00F6zel cevaplar</p>'
        '</div>', unsafe_allow_html=True)

    questions = []

    # Q1: Kelime sorusu
    ve = ai.get("vocabulary_enrichment", {}) if ai else {}
    defs = ve.get("definitions", [])
    if defs and len(defs) >= 2:
        import random
        picks = random.sample(defs, min(2, len(defs)))
        questions.append({
            "q": f"'{picks[0].get('word', '')}' ne demek?",
            "answer": picks[0].get("definition", ""),
            "type": "vocab",
        })
    elif vocab and len(vocab) >= 1:
        questions.append({
            "q": f"'{vocab[0]}' kelimesini bir c\u00FCmlede kullan.",
            "answer": "",
            "type": "open",
        })

    # Q2: Grammar sorusu
    gf = ai.get("grammar_focus", {}) if ai else {}
    if gf and gf.get("examples"):
        ex = gf["examples"][0] if gf["examples"] else ""
        questions.append({
            "q": f"Bu c\u00FCmledeki kural\u0131 a\u00E7\u0131kla: \"{ex}\"",
            "answer": gf.get("rule", ""),
            "type": "grammar",
        })
    else:
        questions.append({
            "q": f"'{theme}' konusuyla ilgili 2 c\u00FCmle yaz.",
            "answer": "",
            "type": "open",
        })

    # Q3: Genel anlama
    questions.append({
        "q": f"Bug\u00FCn ne \u00F6\u011Frendin? En \u00F6nemli 1 \u015Feyi yaz.",
        "answer": "",
        "type": "reflection",
    })

    _type_icons = {"vocab": "\U0001F4DA", "grammar": "\U0001F4DD",
                   "open": "\u270D\uFE0F", "reflection": "\U0001F4AD"}
    for i, q in enumerate(questions[:3]):
        icon = _type_icons.get(q["type"], "\u2753")
        st.markdown(f"**{icon} Soru {i+1}:** {q['q']}")
        ans = st.text_input("",
                            label_visibility="collapsed", placeholder="Cevap...")
        if ans and q.get("answer"):
            if ans.strip().lower() in q["answer"].strip().lower():
                st.success("\u2705 Do\u011Fru!")
            else:
                st.caption(f"\U0001F4A1 Beklenen: {q['answer'][:80]}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6) OTOMATİK ÖDEV OLUŞTURUCU
# ═══════════════════════════════════════════════════════════════════════════════

def _auto_homework(ai: dict, vocab: list[str], theme: str, structure: str,
                   grade: int, unit_num: int, ukey: str):
    """Ders i\u00E7eri\u011Finden otomatik \u00F6dev olu\u015Ftur."""
    with st.expander("Otomatik Ödev Oluştur", expanded=False):
        hw_items = []

        # 1. Kelime ödevi
        if vocab:
            hw_items.append(
                f"**\U0001F4DA Vocabulary:** A\u015Fa\u011F\u0131daki kelimelerin anlam\u0131n\u0131 yaz "
                f"ve her biriyle bir c\u00FCmle kur:\n"
                + "\n".join(f"   {i+1}. {w}" for i, w in enumerate(vocab[:8])))

        # 2. Grammar ödevi
        gf = ai.get("grammar_focus", {}) if ai else {}
        if gf and gf.get("rule"):
            hw_items.append(
                f"**\U0001F4DD Grammar:** '{gf['rule'][:100]}' "
                f"kural\u0131n\u0131 kullanarak 5 c\u00FCmle yaz.")

        # 3. Reading ödevi
        rp = ai.get("reading_passage", ai.get("story", {})) if ai else {}
        if rp and rp.get("text"):
            hw_items.append(
                "**\U0001F4D6 Reading:** Ders kitab\u0131ndaki "
                f"'{rp.get('title', 'passage')}' metnini tekrar oku "
                "ve 3 soru cevapla.")

        # 4. Writing ödevi
        hw_items.append(
            f"**\u270D\uFE0F Writing:** '{theme}' konusunda "
            "en az 5 c\u00FCmlelik bir paragraf yaz. "
            f"Bu kelimeleri kullan: {', '.join(vocab[:5])}")

        if hw_items:
            hw_text = (f"## \U0001F4DD Ev \u00D6devi \u2014 Unit {unit_num}: {theme}\n"
                       f"**S\u0131n\u0131f:** {grade}. S\u0131n\u0131f | "
                       f"**Teslim:** Bir sonraki ders\n\n---\n\n"
                       + "\n\n".join(hw_items)
                       + "\n\n---\n*SmartCampusAI \u2014 Otomatik \u00D6dev*")

            st.markdown(hw_text)
            st.download_button(
                "\U0001F4E5 \u00D6devi \u0130ndir (.txt)",
                hw_text,
                file_name=f"homework_unit{unit_num}_{theme.replace(' ','_')[:20]}.txt",
                mime="text/plain")
        else:
            st.info("\u0130\u00E7erik y\u00FCklenmedi \u2014 \u00F6dev olu\u015Fturulamad\u0131.")


# ═══════════════════════════════════════════════════════════════════════════════
# A4) HIZLI YOKLAMA (QUICK POLL)
# ═══════════════════════════════════════════════════════════════════════════════

def _quick_poll(phase_key: str, ai: dict, vocab: list[str], ukey: str):
    """Faz sonunda 1 soruluk h\u0131zl\u0131 anlama kontrol\u00FC."""
    poll_key = f"_ld_poll_{ukey}_{phase_key}"
    if st.session_state.get(poll_key):
        # Zaten cevaplanmış
        r = st.session_state[poll_key]
        st.markdown(
            f'<div style="background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.2);'
            f'border-radius:10px;padding:10px 16px;text-align:center;">'
            f'<span style="color:#22c55e;font-weight:600;">\u2705 Yoklama Tamamland\u0131</span>'
            f' \u2014 <span style="color:#818cf8;">'
            f'{r.get("yes",0)} Anlad\u0131 / {r.get("no",0)} Anlamad\u0131'
            f' (%{r.get("pct",0)} ba\u015Far\u0131)</span></div>',
            unsafe_allow_html=True)
        return

    with st.expander(f"Hizli Yoklama - Anladilar mi? ({phase_key})", expanded=False):
        st.markdown(
            '<div style="color:#94A3B8;font-size:.85rem;margin-bottom:8px;">'
            '\u00D6\u011Frencilere sorun: "Anlayan el kald\u0131rs\u0131n!" '
            'veya parmak say\u0131s\u0131 ile (1-5) de\u011Ferlendirin.</div>',
            unsafe_allow_html=True)
        pc1, pc2 = st.columns(2)
        with pc1:
            yes = st.number_input(
                "\u2705 Anlayan", min_value=0, max_value=50, value=0,
                key=f"ld_poll_yes_{ukey}_{phase_key}")
        with pc2:
            no = st.number_input(
                "\u274C Anlamayan", min_value=0, max_value=50, value=0,
                key=f"ld_poll_no_{ukey}_{phase_key}")
        if st.button("\U0001F4CA Kaydet", key=f"ld_poll_save_{ukey}_{phase_key}"):
            total = yes + no
            pct = round(yes / total * 100) if total > 0 else 0
            st.session_state[poll_key] = {"yes": yes, "no": no, "pct": pct}
            if pct < 50:
                st.error(f"\u26A0\uFE0F %{pct} \u2014 Konuyu tekrar a\u00E7\u0131klay\u0131n!")
            elif pct < 75:
                st.warning(f"\U0001F7E1 %{pct} \u2014 Birka\u00E7 \u00F6rnek daha yap\u0131n")
            else:
                st.success(f"\u2705 %{pct} \u2014 Harika! Devam edebilirsiniz")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# B8) VELİ BİLDİRİMİ
# ═══════════════════════════════════════════════════════════════════════════════

def _parent_notification(theme: str, vocab: list[str], structure: str,
                         grade: int, unit_num: int, ukey: str):
    """Bug\u00FCn ne \u00F6\u011Frenildi\u011Fini veliye bildir."""
    with st.expander("Veli Bildirimi Oluştur", expanded=False):
        word_list = ", ".join(vocab[:8])
        msg = (
            f"\U0001F4DA Say\u0131n Veli,\n\n"
            f"Bug\u00FCnk\u00FC \u0130ngilizce dersinde ({grade}. S\u0131n\u0131f):\n\n"
            f"\U0001F4D8 **\u00DCnite {unit_num}: {theme}**\n"
            f"\U0001F4DA **Kelimeler:** {word_list}\n"
            f"\U0001F4DD **Dilbilgisi:** {structure[:120] if structure else 'Genel pratik'}\n"
            f"\U0001F3AF **Beceriler:** Dinleme, Konu\u015Fma, Okuma, Yazma\n\n"
            f"\u2705 Evde yapabilece\u011Fi \u00E7al\u0131\u015Fmalar:\n"
            f"- Yeni kelimeleri sesli tekrarlas\u0131n\n"
            f"- Her kelimeyle bir c\u00FCmle kursun\n"
            f"- Ders kitab\u0131ndaki metni tekrar okusun\n\n"
            f"\u0130yi \u00E7al\u0131\u015Fmalar \U0001F4AA\n"
            f"*SmartCampusAI \u2014 Yabanc\u0131 Dil Mod\u00FCl\u00FC*"
        )
        st.text_area("Mesaj \u00D6nizleme", msg, height=250)
        vc1, vc2 = st.columns(2)
        with vc1:
            st.download_button(
                "\U0001F4E5 Mesaj\u0131 \u0130ndir (.txt)", msg,
                file_name=f"veli_bildirim_unit{unit_num}.txt",
                mime="text/plain")
        with vc2:
            if st.button("\U0001F4CB Panoya Kopyala"):
                st.code(msg, language=None)
                st.info("Yukar\u0131daki metni se\u00E7ip kopyalayabilirsiniz.")


# ═══════════════════════════════════════════════════════════════════════════════
# B9) DEVAMSIZ ÖĞRENCİ PAKETİ
# ═══════════════════════════════════════════════════════════════════════════════

def _absent_student_pack(ai: dict, vocab: list[str], theme: str,
                         structure: str, grade: int, unit_num: int, ukey: str):
    """Devams\u0131z \u00F6\u011Frenciler i\u00E7in ders \u00F6zeti + al\u0131\u015Ft\u0131rma paketi."""
    with st.expander("Devamsız Öğrenci Paketi", expanded=False):
        sections = []

        # Ders özeti
        sections.append(
            f"# \U0001F4D8 Ders \u00D6zeti \u2014 Unit {unit_num}: {theme}\n"
            f"**S\u0131n\u0131f:** {grade}. S\u0131n\u0131f\n\n---\n")

        # Kelimeler
        ve = ai.get("vocabulary_enrichment", {}) if ai else {}
        defs = ve.get("definitions", [])
        if defs:
            vocab_section = "## \U0001F4DA Kelimeler\n"
            for d in defs:
                vocab_section += (
                    f"- **{d.get('word','')}**: {d.get('definition','')} "
                    f"\u2014 *\"{d.get('example','')}\"*\n")
            sections.append(vocab_section)
        elif vocab:
            sections.append(
                "## \U0001F4DA Kelimeler\n"
                + "\n".join(f"- {w}" for w in vocab) + "\n")

        # Dilbilgisi
        gf = ai.get("grammar_focus", {}) if ai else {}
        if gf and gf.get("rule"):
            gram = f"## \U0001F4DD Dilbilgisi\n**Kural:** {gf['rule']}\n\n"
            for ex in gf.get("examples", []):
                gram += f"- *{ex}*\n"
            sections.append(gram)

        # Okuma
        story = ai.get("story", ai.get("reading_passage", {})) if ai else {}
        if story and story.get("text"):
            sections.append(
                f"## \U0001F4D6 Okuma: {story.get('title','')}\n"
                f"{story['text'][:500]}{'...' if len(story.get('text',''))>500 else ''}\n")

        # Alıştırma
        ex = ai.get("exercises", {}) if ai else {}
        fb = ex.get("fill_blanks", [])
        if fb:
            ex_section = "## \u270D\uFE0F Al\u0131\u015Ft\u0131rmalar\n"
            for i, f in enumerate(fb[:6]):
                ex_section += f"{i+1}. {f.get('sentence','')}\n"
            sections.append(ex_section)

        # Ev ödevi
        sections.append(
            "## \U0001F3E0 Yapman Gerekenler\n"
            "1. Kelimelerin anlam\u0131n\u0131 \u00F6\u011Fren ve defterine yaz\n"
            "2. Dilbilgisi kural\u0131n\u0131 \u00F6\u011Fren, 3 \u00F6rnek c\u00FCmle yaz\n"
            "3. Okuma metnini oku, sorular\u0131 cevapla\n"
            "4. Al\u0131\u015Ft\u0131rmalar\u0131 tamamla\n")

        pack_text = "\n\n".join(sections)
        st.markdown(pack_text)
        st.download_button(
            "\U0001F4E5 Paketi \u0130ndir (.txt)", pack_text,
            file_name=f"devamsiz_paket_unit{unit_num}_{theme.replace(' ','_')[:20]}.txt",
            mime="text/plain")


# ═══════════════════════════════════════════════════════════════════════════════
# C10) VIDEO/GÖRSEL ENTEGRASYONCategoría
# ═══════════════════════════════════════════════════════════════════════════════

# Ünite temaları için önerilen eğitim video anahtar kelimeleri
_VIDEO_SUGGESTIONS: dict[str, list[dict]] = {
    "default": [
        {"title": "English vocabulary for kids", "icon": "\U0001F4DA",
         "search": "learn english vocabulary kids animated"},
        {"title": "Grammar song for children", "icon": "\U0001F3B5",
         "search": "english grammar song children"},
    ],
}


def _video_suggestions(theme: str, vocab: list[str], grade: int):
    """Ders i\u00E7eri\u011Fine uygun video \u00F6nerileri."""
    with st.expander("Video & Görsel Kaynaklar", expanded=False):
        st.markdown(
            '<div style="color:#94A3B8;font-size:.85rem;margin-bottom:10px;">'
            'Ders i\u00E7eri\u011Fine uygun video \u00F6nerileri \u2014 '
            'projeksiyonda g\u00F6sterebilirsiniz.</div>',
            unsafe_allow_html=True)

        # Tema bazlı arama önerileri
        level = "kids" if grade <= 4 else ("teens" if grade <= 8 else "students")
        suggestions = [
            {"icon": "\U0001F4DA", "title": f"{theme} vocabulary",
             "query": f"learn english {theme} vocabulary {level} animated"},
            {"icon": "\U0001F3B5", "title": f"{theme} song",
             "query": f"english {theme} song for {level}"},
            {"icon": "\U0001F4D6", "title": f"{theme} story",
             "query": f"english short story about {theme} {level}"},
        ]
        if vocab:
            word_sample = " ".join(vocab[:3])
            suggestions.append({
                "icon": "\U0001F50D", "title": f"Vocabulary: {word_sample}",
                "query": f"english words {word_sample} meaning pronunciation"})

        for s in suggestions:
            yt_url = f"https://www.youtube.com/results?search_query={s['query'].replace(' ', '+')}"
            st.markdown(
                f'{s["icon"]} **{s["title"]}** \u2014 '
                f'[YouTube\'da Ara]({yt_url})')
        st.caption(
            "\U0001F6E1\uFE0F Videolar\u0131 \u00F6nce kendiniz izleyin, "
            "uygunsa s\u0131n\u0131fta g\u00F6sterin.")


# ═══════════════════════════════════════════════════════════════════════════════
# C11) SEVİYE FARKLILAŞTIRMA
# ═══════════════════════════════════════════════════════════════════════════════

def _differentiation_panel(phase_key: str, ai: dict, vocab: list[str],
                           theme: str, structure: str):
    """Ayn\u0131 faz i\u00E7in 3 zorluk seviyesi \u00F6nerisi."""
    with st.expander(f"Seviye Farklilastirma - Starter / Core / Extension ({phase_key})", expanded=False):
        diff = _DIFFERENTIATION_DATA.get(phase_key, _DIFFERENTIATION_DATA.get("default"))
        if not diff:
            return
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.markdown(
                '<div style="background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.2);'
                'border-radius:10px;padding:12px;">'
                '<div style="color:#22c55e;font-weight:700;font-size:.9rem;margin-bottom:6px;">'
                '\U0001F7E2 Starter (Kolay)</div>'
                f'<div style="color:#94A3B8;font-size:.82rem;">{diff["starter"]}</div>'
                '</div>', unsafe_allow_html=True)
        with dc2:
            st.markdown(
                '<div style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.2);'
                'border-radius:10px;padding:12px;">'
                '<div style="color:#818cf8;font-weight:700;font-size:.9rem;margin-bottom:6px;">'
                '\U0001F535 Core (Orta)</div>'
                f'<div style="color:#94A3B8;font-size:.82rem;">{diff["core"]}</div>'
                '</div>', unsafe_allow_html=True)
        with dc3:
            st.markdown(
                '<div style="background:rgba(168,85,247,.06);border:1px solid rgba(168,85,247,.2);'
                'border-radius:10px;padding:12px;">'
                '<div style="color:#A855F7;font-weight:700;font-size:.9rem;margin-bottom:6px;">'
                '\U0001F7E3 Extension (Zor)</div>'
                f'<div style="color:#94A3B8;font-size:.82rem;">{diff["extension"]}</div>'
                '</div>', unsafe_allow_html=True)


_DIFFERENTIATION_DATA = {
    "warmup": {
        "starter": "Kelimeleri resimlerle e\u015Fle\u015Ftir. Tek kelimelik cevap yeterli.",
        "core": "Kelimeleri c\u00FCmle i\u00E7inde kullan. 'I see a...' kal\u0131b\u0131yla.",
        "extension": "Tema hakk\u0131nda 3 c\u00FCmle s\u00F6yle. Sebep-sonu\u00E7 kullan.",
    },
    "vocabulary": {
        "starter": "5 kelime \u00F6\u011Fren. Resimle e\u015Fle\u015Ftir, sesli tekrarla.",
        "core": "T\u00FCm kelimeler + anlam + \u00F6rnek c\u00FCmle yaz.",
        "extension": "Kelimelerin word families'\u0131n\u0131 bul (noun/verb/adj). Paragrafta kullan.",
    },
    "grammar": {
        "starter": "Haz\u0131r c\u00FCmlelerdeki bo\u015Fluklar\u0131 doldur (se\u00E7enekli).",
        "core": "Kural\u0131 \u00F6\u011Fren, 5 c\u00FCmle yaz.",
        "extension": "Kural\u0131 farkl\u0131 ba\u011Flamlarda kullan. Hatal\u0131 c\u00FCmleleri d\u00FCzelt.",
    },
    "listening": {
        "starter": "Diyalogu 3 kez dinle. Ana fikri s\u00F6yle.",
        "core": "Diyalogu dinle, sorular\u0131 cevapla.",
        "extension": "Diyalo\u011Fu geni\u015Flet, yeni bir sahne yaz.",
    },
    "reading": {
        "starter": "Metindeki bildi\u011Fin kelimeleri i\u015Faretle. Resimlere bakarak anlat.",
        "core": "Metni oku, 5 soruyu cevapla.",
        "extension": "Metnin devam\u0131n\u0131 yaz. Karakterlere mektup yaz.",
    },
    "writing": {
        "starter": "Verilen c\u00FCmleleri kopyala ve bo\u015Fluklar\u0131 doldur.",
        "core": "5-7 c\u00FCmlelik paragraf yaz.",
        "extension": "10+ c\u00FCmlelik yaz\u0131. Linking words kullan (however, because, also).",
    },
    "song": {
        "starter": "\u015Eark\u0131y\u0131 dinle, tekrarla. Hareketleri taklit et.",
        "core": "\u015Eark\u0131 s\u00F6zlerini oku, anlamlar\u0131 bul.",
        "extension": "\u015Eark\u0131ya yeni bir k\u0131ta yaz.",
    },
    "exercises": {
        "starter": "\u0130lk 3 soruyu \u00E7\u00F6z. Yard\u0131m alabilir.",
        "core": "T\u00FCm sorular\u0131 bireysel \u00E7\u00F6z.",
        "extension": "Ekstra 3 soru \u00E7\u00F6z + kendi sorular\u0131n\u0131 yaz.",
    },
    "review": {
        "starter": "3 kelimeyi hat\u0131rla ve s\u00F6yle.",
        "core": "Quiz'i tamamla, hatalar\u0131n\u0131 d\u00FCzelt.",
        "extension": "Arkada\u015F\u0131na dersi anlat. 'Teach-back' y\u00F6ntemi.",
    },
    "default": {
        "starter": "Temel seviye \u2014 yard\u0131ml\u0131 \u00E7al\u0131\u015Fma.",
        "core": "Standart seviye \u2014 bireysel \u00E7al\u0131\u015Fma.",
        "extension": "\u0130leri seviye \u2014 ba\u011F\u0131ms\u0131z ve yarat\u0131c\u0131 \u00E7al\u0131\u015Fma.",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# C12) FAZ GEÇİŞ ANİMASYONU
# ═══════════════════════════════════════════════════════════════════════════════

def _phase_transition(prev_phase: dict | None, next_phase: dict):
    """Fazlar aras\u0131 motivasyon ekran\u0131."""
    if prev_phase:
        prev_txt = f"<div style='color:#22c55e;font-size:.85rem;'>\u2705 {prev_phase['icon']} {prev_phase['label']} tamamland\u0131!</div>"
    else:
        prev_txt = ""
    components.html(f"""
    <div style="font-family:system-ui;text-align:center;
    background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);
    border-radius:14px;padding:24px;border:1.5px solid rgba(99,102,241,.25);
    animation:fadeSlide .5s ease;">
    {prev_txt}
    <div style="font-size:2.5rem;margin:10px 0;">{next_phase['icon']}</div>
    <div style="font-size:1.2rem;font-weight:800;color:#c7d2fe;">
    {next_phase['label']}</div>
    <div style="font-size:.85rem;color:#818cf8;margin-top:4px;">
    {next_phase['desc']}</div>
    <div style="font-size:.75rem;color:#f59e0b;margin-top:8px;">
    \u23F1 {next_phase['minutes']} dakika</div>
    </div>
    <style>
    @keyframes fadeSlide{{
      from{{opacity:0;transform:translateY(20px);}}
      to{{opacity:1;transform:translateY(0);}}
    }}
    </style>""", height=160)


# ═══════════════════════════════════════════════════════════════════════════════
# TTS PRONUNCIATION — Tarayıcı Speech API
# ═══════════════════════════════════════════════════════════════════════════════

def _tts_words(words: list[str], title: str = "Pronunciation"):
    """Kelime telaffuz paneli — tıkla dinle + toplu dinle."""
    if not words:
        return
    js_arr = json.dumps(words[:16])
    h = f"""
    <div style="font-family:system-ui;background:#0f172a;padding:14px;border-radius:12px;">
    <div style="color:#f59e0b;font-weight:700;font-size:.9rem;margin-bottom:10px;">🎤 {title}</div>
    <div id="pc" style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;"></div>
    <div style="text-align:center;margin-top:12px;">
    <button onclick="pa()" style="background:#f59e0b;color:#000;border:none;padding:7px 18px;
    border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;">🔊 Listen All</button>
    <button onclick="ps()" style="background:#8B5CF6;color:#fff;border:none;padding:7px 18px;
    border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;margin-left:6px;">🐢 Slow</button>
    </div></div>
    <script>
    const W={js_arr},C=document.getElementById('pc');
    W.forEach(w=>{{const d=document.createElement('div');
    d.style.cssText='background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:8px;padding:8px 14px;cursor:pointer;text-align:center;min-width:80px;';
    d.innerHTML='<b style="color:#f59e0b;font-size:.95rem;">'+w+'</b>';
    d.onclick=()=>{{const u=new SpeechSynthesisUtterance(w);u.lang='en-US';u.rate=.85;speechSynthesis.speak(u);
    d.style.background='rgba(245,158,11,.25)';setTimeout(()=>d.style.background='rgba(245,158,11,.08)',1200);}};
    C.appendChild(d);}});
    function pa(){{let i=0;(function n(){{if(i>=W.length)return;const u=new SpeechSynthesisUtterance(W[i]);
    u.lang='en-US';u.rate=.85;u.onend=()=>{{i++;setTimeout(n,500);}};speechSynthesis.speak(u);}}())}}
    function ps(){{let i=0;(function n(){{if(i>=W.length)return;const u=new SpeechSynthesisUtterance(W[i]);
    u.lang='en-US';u.rate=.5;u.onend=()=>{{i++;setTimeout(n,800);}};speechSynthesis.speak(u);}}())}}
    </script>"""
    components.html(h, height=220)


def _tts_text(text: str, label: str = "Listen"):
    """Metin okuma butonu."""
    clean = text.replace("'", "\\'").replace("\n", ". ")[:500]
    h = f"""<div style="text-align:center;margin:8px 0;">
    <button onclick="(function(){{const u=new SpeechSynthesisUtterance('{clean}');
    u.lang='en-US';u.rate=.8;speechSynthesis.speak(u)}})()"
    style="background:#6366F1;color:#fff;border:none;padding:7px 18px;border-radius:8px;
    cursor:pointer;font-weight:600;font-size:13px;">🔊 {label}</button></div>"""
    components.html(h, height=50)


# ═══════════════════════════════════════════════════════════════════════════════
# DERS FAZI RENDER'LARI — Her faz tam otonom
# ═══════════════════════════════════════════════════════════════════════════════

def _phase_warmup(ai: dict, vocab: list[str], theme: str, theme_tr: str):
    """ISSINMA FAZI — fun fact + kelime ön izleme."""
    # Fun fact
    ff = ai.get("fun_fact", "") if ai else ""
    if ff:
        st.markdown(f'<div class="ld-fact"><b>💡 Did You Know?</b> <span>{ff}</span></div>',
                    unsafe_allow_html=True)

    # Tema tanıtımı
    intro = ai.get("theme_intro", "") if ai else ""
    if intro:
        st.markdown(f'<div class="ld-card"><div class="ld-card-title">📘 Theme Introduction</div>{intro}</div>',
                    unsafe_allow_html=True)
    elif theme:
        st.markdown(f'<div class="ld-card"><div class="ld-card-title">📘 Today\'s Topic</div>'
                    f'Today we will learn about <b>{theme}</b> ({theme_tr}).</div>',
                    unsafe_allow_html=True)

    # Kelime ön izleme
    if vocab:
        word_html = "".join(f'<span class="ld-vocab"><b>{w}</b></span>' for w in vocab[:12])
        st.markdown(f'<div class="ld-card"><div class="ld-card-title">📚 Key Words</div>{word_html}</div>',
                    unsafe_allow_html=True)


def _phase_vocabulary(ai: dict, vocab: list[str], theme: str, week_data: dict, level: str):
    """KELİME FAZI — kartlar + tanımlar + telaffuz + etkinlik."""
    ve = ai.get("vocabulary_enrichment", {}) if ai else {}
    defs = ve.get("definitions", [])

    # Kelime kartları (tanımlı) + her karta telaffuz butonu
    if defs:
        _vocab_words_js = json.dumps([vd.get("word", "") for vd in defs], ensure_ascii=False)
        _vocab_html_cards = ""
        for i, vd in enumerate(defs):
            w = vd.get("word", "")
            d = vd.get("definition", "").replace("'", "&#39;")
            ex = vd.get("example", "").replace("'", "&#39;")
            tr = vd.get("turkish_hint", "")
            tr_line = f'<div style="color:#f59e0b;font-size:.72rem;margin-top:2px;">TR: {tr}</div>' if tr else ''
            _vocab_html_cards += (
                f'<div style="background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.1);'
                f'border-left:3px solid #818cf8;border-radius:12px;padding:12px 16px;margin:6px 0;'
                f'display:flex;align-items:flex-start;gap:10px;">'
                f'<button onclick="(function(){{var u=new SpeechSynthesisUtterance(\'{w}\');'
                f'u.lang=\'en-US\';u.rate=0.8;speechSynthesis.speak(u)}})()" '
                f'style="background:#f59e0b;color:#000;border:none;border-radius:50%;'
                f'width:32px;height:32px;min-width:32px;cursor:pointer;font-size:14px;'
                f'display:flex;align-items:center;justify-content:center;margin-top:2px;" '
                f'title="Dinle: {w}">🔊</button>'
                f'<div style="flex:1;">'
                f'<div style="font-size:1.05rem;font-weight:700;color:#818cf8;">{w}</div>'
                f'<div style="font-size:.85rem;color:#94A3B8;margin-top:3px;">{d}</div>'
                f'<div style="font-size:.8rem;color:#64748b;font-style:italic;margin-top:2px;">"{ex}"</div>'
                f'{tr_line}'
                f'</div></div>'
            )

        # Toplu dinleme butonları
        _vocab_all_html = (
            f'<div style="font-family:system-ui;background:#0f172a;border-radius:14px;'
            f'padding:16px;border:1.5px solid rgba(99,102,241,.2);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'
            f'<div style="color:#818cf8;font-weight:700;font-size:.95rem;">📚 Vocabulary Cards</div>'
            f'<div style="display:flex;gap:6px;">'
            f'<button onclick="(function(){{var W={_vocab_words_js};var i=0;'
            f'(function n(){{if(i>=W.length)return;var u=new SpeechSynthesisUtterance(W[i]);'
            f'u.lang=\'en-US\';u.rate=0.85;u.onend=function(){{i++;setTimeout(n,500)}};'
            f'speechSynthesis.speak(u)}}())}})()\" '
            f'style="background:#6366F1;color:#fff;border:none;padding:6px 14px;'
            f'border-radius:8px;font-weight:700;cursor:pointer;font-size:12px;">🔊 Tümünü Dinle</button>'
            f'<button onclick="(function(){{var W={_vocab_words_js};var i=0;'
            f'(function n(){{if(i>=W.length)return;var u=new SpeechSynthesisUtterance(W[i]);'
            f'u.lang=\'en-US\';u.rate=0.5;u.onend=function(){{i++;setTimeout(n,800)}};'
            f'speechSynthesis.speak(u)}}())}})()\" '
            f'style="background:#8B5CF6;color:#fff;border:none;padding:6px 14px;'
            f'border-radius:8px;font-weight:700;cursor:pointer;font-size:12px;">🐢 Yavaş</button>'
            f'<button onclick="speechSynthesis.cancel()" '
            f'style="background:rgba(255,255,255,.08);color:#94A3B8;border:1px solid rgba(255,255,255,.1);'
            f'padding:6px 12px;border-radius:8px;cursor:pointer;font-size:12px;">⏹ Dur</button>'
            f'</div></div>'
            f'{_vocab_html_cards}'
            f'</div>'
        )
        card_count = len(defs)
        card_height = max(250, min(800, card_count * 90 + 80))
        components.html(_vocab_all_html, height=card_height, scrolling=True)

    # İnteraktif flashcard etkinliği
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("flashcard", week_data, level)
        if html:
            with st.expander("Interactive Flashcards", expanded=False):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass

    # Word families
    families = ve.get("word_families", [])
    if families:
        with st.expander("Word Families", expanded=False):
            for wf in families:
                st.markdown(f"**{wf.get('base','')}** → Noun: *{wf.get('noun','—')}* | "
                            f"Verb: *{wf.get('verb','—')}* | Adj: *{wf.get('adjective','—')}*")


def _phase_grammar(ai: dict, structure: str, week_data: dict, level: str, ukey: str):
    """DİLBİLGİSİ FAZI — kural + örnek + alıştırma + etkinlik."""
    gf = ai.get("grammar_focus", {}) if ai else {}
    rule = gf.get("rule", "")
    examples = gf.get("examples", [])
    tip = gf.get("tip", "")

    if rule:
        st.markdown(f'<div class="ld-rule"><b>📐 Rule:</b> <span>{rule}</span></div>',
                    unsafe_allow_html=True)
    elif structure:
        st.markdown(f'<div class="ld-rule"><b>📐 Structure:</b> <span>{structure}</span></div>',
                    unsafe_allow_html=True)

    if examples:
        st.markdown("**Examples:**")
        for ex in examples:
            st.markdown(f"- *{ex}*")

    if tip:
        st.info(f"💡 **Tip:** {tip}")

    # İnteraktif etkinlik
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("grammar", week_data, level)
        if html:
            with st.expander("Interactive Grammar Practice", expanded=True):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass

    # Alıştırma soruları
    exercises = ai.get("exercises", {}) if ai else {}
    fill_blanks = exercises.get("fill_blanks", [])
    if fill_blanks:
        st.markdown("#### ✏️ Practice — Fill in the Blanks")
        for i, fb in enumerate(fill_blanks[:6]):
            sent = fb.get("sentence", "")
            answer = fb.get("answer", "")
            opts = fb.get("options", [])
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{i+1}.** {sent}")
                if opts:
                    st.caption(f"({' / '.join(opts)})")
            with c2:
                user = st.text_input("",
                                      label_visibility="collapsed", placeholder="?")
                if user and answer:
                    if user.strip().lower() == answer.strip().lower():
                        st.success("✅")
                    else:
                        st.error(f"❌ {answer}")


def _phase_reading(ai: dict, week_data: dict, level: str, ukey: str):
    """OKUMA FAZI — metin + anlama + etkinlik."""
    # Story
    story = ai.get("story", {}) if ai else {}
    if story and story.get("text"):
        st.markdown(f"**📖 {story.get('title', 'Story')}**")
        st.markdown(f'<div class="ld-story">{story["text"]}</div>', unsafe_allow_html=True)
        _tts_text(story["text"], "Listen to the Story")
        moral = story.get("moral", "")
        if moral:
            st.success(f"✨ **Moral:** {moral}")

    # Reading passage
    rp = ai.get("reading_passage", {}) if ai else {}
    if rp and rp.get("text"):
        st.markdown(f"**📖 {rp.get('title', 'Reading Passage')}**")
        st.markdown(f'<div class="ld-story" style="border-left-color:#059669;">{rp["text"]}</div>',
                    unsafe_allow_html=True)
        _tts_text(rp["text"], "Listen to the Passage")

        # Comprehension questions
        questions = rp.get("questions", [])
        if questions:
            st.markdown("#### 📝 Comprehension Questions")
            for i, q in enumerate(questions):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{i+1}.** {q}")
                with c2:
                    st.text_input("",
                                   label_visibility="collapsed", placeholder="Answer...",
                                   key=f"ld_read_q_{ukey}_{i}")

    # İnteraktif etkinlik
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("reading", week_data, level)
        if html:
            with st.expander("Interactive Reading Activity", expanded=False):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass


def _phase_listening_speaking(ai: dict, vocab: list[str], week_data: dict, level: str):
    """DİNLEME & KONUŞMA FAZI — diyalog + telaffuz + etkinlik."""
    # Dialogue
    dlg = ai.get("dialogue", {}) if ai else {}
    if dlg and dlg.get("lines"):
        speakers = dlg.get("speakers", ["A", "B"])
        title = dlg.get("title", "")
        if title:
            st.markdown(f"*{title}*")

        for line in dlg["lines"]:
            sp_idx = line.get("speaker", 0)
            sp = speakers[sp_idx] if sp_idx < len(speakers) else "?"
            cls = "a" if sp_idx == 0 else "b"
            st.markdown(f'<div class="ld-dlg"><span class="{cls}">{sp}:</span> {line.get("text","")}</div>',
                        unsafe_allow_html=True)

        # Diyalog dinleme
        all_text = ". ".join(
            f'{speakers[l.get("speaker",0)] if l.get("speaker",0)<len(speakers) else ""}. {l.get("text","")}'
            for l in dlg["lines"])
        _tts_text(all_text, "Listen to the Dialogue")

    # İnteraktif diyalog etkinliği
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("dialog", week_data, level)
        if html:
            with st.expander("Interactive Dialogue Practice", expanded=False):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass

    # Listening etkinliği
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("listening", week_data, level)
        if html:
            with st.expander("Listening Activity", expanded=False):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass

    # Pronunciation
    st.markdown("---")
    _tts_words(vocab[:12], "Pronunciation Practice — Tekrarla")


def _phase_writing(ai: dict, theme: str, week_data: dict, level: str, ukey: str):
    """YAZMA FAZI — yönlendirilmiş yazma + etkinlik."""
    ex = ai.get("exercises", {}) if ai else {}
    wp = ex.get("writing_prompt", "")

    if wp:
        st.info(f"**✍️ Writing Task:** {wp}")
    else:
        st.info(f"**✍️ Writing Task:** Write a paragraph about {theme} using at least 5 new words.")

    st.text_area("Your writing:", height=150,
                  label_visibility="collapsed", placeholder="Start writing here...")

    # İnteraktif etkinlik
    try:
        from views.yd_tools import _dispatch_activity_html
        html = _dispatch_activity_html("writing", week_data, level)
        if html:
            with st.expander("Interactive Writing Activity", expanded=False):
                components.html(html, height=500, scrolling=True)
    except Exception:
        pass


def _phase_song_culture(ai: dict, week_data: dict, level: str):
    """ŞARKI & KÜLTÜR FAZI."""
    song = ai.get("song_chant", {}) if ai else {}
    cc = ai.get("culture_corner", {}) if ai else {}

    if not song and not cc:
        return

    if song and song.get("lyrics"):
        st.markdown(f"**🎵 {song.get('title', 'Song')}**")
        for line in song["lyrics"].split("\n"):
            if line.strip():
                st.markdown(f'<div class="ld-song">♫ {line.strip()}</div>', unsafe_allow_html=True)
        _tts_text(song["lyrics"].replace("\n", ". "), "Listen to the Song")

        # Song etkinliği
        try:
            from views.yd_tools import _dispatch_activity_html
            html = _dispatch_activity_html("song", week_data, level)
            if html:
                with st.expander("Sing Along Activity", expanded=False):
                    components.html(html, height=500, scrolling=True)
        except Exception:
            pass

    if cc and cc.get("text"):
        st.markdown("---")
        st.markdown(f"**🌍 {cc.get('title', 'Culture Corner')}**")
        st.markdown(f'<div class="ld-story" style="border-left-color:#0EA5E9;">{cc["text"]}</div>',
                    unsafe_allow_html=True)


def _phase_exercises(ai: dict, ukey: str):
    """ALIŞTIRMA FAZI — tüm exercise tipleri doldurulabilir."""
    ex = ai.get("exercises", {}) if ai else {}
    matching = ex.get("matching", [])
    fill_blanks = ex.get("fill_blanks", [])
    reorder = ex.get("reorder", [])

    if not matching and not fill_blanks and not reorder:
        return

    if fill_blanks:
        st.markdown("#### ✏️ Fill in the Blanks")
        for i, fb in enumerate(fill_blanks):
            sent = fb.get("sentence", "")
            answer = fb.get("answer", "")
            opts = fb.get("options", [])
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{i+1}.** {sent}")
                if opts:
                    st.caption(f"({' / '.join(opts)})")
            with c2:
                user = st.text_input("",
                                      label_visibility="collapsed", placeholder="?")
                if user and answer:
                    st.success("✅") if user.strip().lower() == answer.strip().lower() else st.error(f"❌ {answer}")

    if matching:
        st.markdown("#### 🔗 Matching")
        right_opts = [m.get("right", "") for m in matching]
        for i, md in enumerate(matching):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.markdown(f"**{i+1}.** {md.get('left', '')}")
            with c2:
                sel = st.selectbox("", ["--"] + right_opts,
                                    label_visibility="collapsed")
            with c3:
                if sel != "--":
                    st.success("✅") if sel == md.get("right", "") else st.error("❌")

    if reorder:
        st.markdown("#### 🔄 Put in Order")
        for i, ro in enumerate(reorder):
            words = ro.get("words", [])
            answer = ro.get("answer", "")
            st.markdown(f"**{i+1}.** {' / '.join(words)}")
            user = st.text_input("",
                                  label_visibility="collapsed", placeholder="Correct sentence...")
            if user and answer:
                st.success("✅") if user.strip().lower() == answer.strip().lower() else st.error(f"❌ {answer}")


def _phase_review(ai: dict, vocab: list[str], theme: str, ukey: str):
    """DERS SONU — özet + mini quiz."""
    # Mini vocabulary quiz
    ve = ai.get("vocabulary_enrichment", {}) if ai else {}
    defs = ve.get("definitions", [])

    if defs:
        st.markdown("#### 🧠 Quick Vocabulary Quiz")
        st.markdown("*Write the correct word for each definition:*")
        for i, vd in enumerate(defs[:6]):
            defn = vd.get("definition", "")
            word = vd.get("word", "")
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{i+1}.** {defn}")
            with c2:
                user = st.text_input("",
                                      label_visibility="collapsed", placeholder="Word?")
                if user:
                    st.success("✅") if user.strip().lower() == word.strip().lower() else st.error(f"❌ {word}")

    # Fun fact tekrar
    ff = ai.get("fun_fact", "") if ai else ""
    if ff:
        st.markdown(f'<div class="ld-fact"><b>💡 Remember:</b> <span>{ff}</span></div>',
                    unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ÖĞRETMEN — TAM OTOMATİK DERS AKIŞI
# ═══════════════════════════════════════════════════════════════════════════════

def render_lesson_delivery_teacher(level: str | None = None):
    """Öğretmen açar → bugünün dersi eksiksiz akar."""
    _css()

    from views.yd_content import _CURRICULUM
    from views.yd_tools import _generate_detailed_daily_plan

    grade_options = {
        "Okul Öncesi": "preschool",
        **{f"{i}. Sınıf": f"grade{i}" for i in range(1, 13)},
    }

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        sel_label = st.selectbox("Sınıf", list(grade_options.keys()),
                                  index=5 if not level else list(grade_options.values()).index(level))
        sel_grade = grade_options[sel_label]

    curriculum = _CURRICULUM.get(sel_grade, [])
    if not curriculum:
        st.warning("Bu sınıf için müfredat bulunamadı.")
        return

    grade_num = get_grade_num(sel_grade)
    today = get_today_info(sel_grade)

    with c2:
        sel_week = st.selectbox("Hafta", list(range(1, len(curriculum) + 1)),
                                 index=min(today["week"] - 1, len(curriculum) - 1))
    with c3:
        sel_day = st.selectbox("Gün", list(DAY_NAMES.keys()),
                                index=list(DAY_NAMES.keys()).index(today["day_key"]),
                                format_func=lambda x: DAY_NAMES[x])

    # Hafta verisi
    week_data = next((w for w in curriculum if w.get("week") == sel_week), None)
    if not week_data:
        week_data = curriculum[min(sel_week - 1, len(curriculum) - 1)]

    unit_num = week_to_unit(sel_week, len(curriculum))
    theme = week_data.get("theme", "")
    theme_tr = week_data.get("theme_tr", "")
    vocab = week_data.get("vocab", [])
    structure = week_data.get("structure", "")
    ukey = f"g{grade_num}u{unit_num}w{sel_week}{sel_day}"

    # ── Ders tipi tespit (days verisinden) ──
    days_data = week_data.get("days", {})
    day_descs = days_data.get(sel_day, [])
    lesson1_type = ""  # Ana Ders / Native Speaker
    lesson2_type = ""  # Beceri Lab: Dinleme/Konuşma/Yazma/Proje / Native Speaker
    lesson1_label = "Ana Ders"
    lesson2_label = "Beceri Lab"

    if day_descs:
        d1 = day_descs[0] if len(day_descs) > 0 else ""
        d2 = day_descs[1] if len(day_descs) > 1 else ""

        # 1. Ders tipi
        if d1.startswith("Native Speaker"):
            lesson1_type = "native"
            lesson1_label = "Native Speaker"
            # Native detayı
            lesson1_detail = d1.replace("Native Speaker:", "").strip()[:80]
        elif d1.startswith("Ana Ders"):
            lesson1_type = "maincourse"
            lesson1_label = "Ana Ders (Main Course)"
            lesson1_detail = d1.replace("Ana Ders:", "").strip()[:80]
        else:
            lesson1_type = "maincourse"
            lesson1_detail = d1[:80]

        # 2. Ders tipi
        if d2.startswith("Native Speaker"):
            lesson2_type = "native"
            lesson2_label = "Native Speaker"
            lesson2_detail = d2.replace("Native Speaker:", "").strip()[:80]
        elif d2.startswith("Beceri Lab"):
            lesson2_type = "skill"
            # Beceri türünü çıkar: "Beceri Lab: Dinleme — ..." → "Dinleme"
            skill_part = d2.replace("Beceri Lab:", "").strip()
            if "—" in skill_part:
                skill_name = skill_part.split("—")[0].strip()
            elif "–" in skill_part:
                skill_name = skill_part.split("–")[0].strip()
            else:
                skill_name = skill_part.split()[0] if skill_part else "Beceri"
            lesson2_label = f"Beceri Lab: {skill_name} (Skill Lab)"
            lesson2_detail = d2.replace("Beceri Lab:", "").strip()[:80]
        else:
            lesson2_type = "skill"
            lesson2_detail = d2[:80]
    else:
        lesson1_detail = ""
        lesson2_detail = ""

    # Ders tipi renkleri
    _type_colors = {"maincourse": "#6366F1", "skill": "#10B981", "native": "#f59e0b"}
    _type_icons = {"maincourse": "📗", "skill": "📕", "native": "🌍"}

    l1_color = _type_colors.get(lesson1_type, "#6366F1")
    l2_color = _type_colors.get(lesson2_type, "#10B981")
    l1_icon = _type_icons.get(lesson1_type, "📗")
    l2_icon = _type_icons.get(lesson2_type, "📕")

    # ── SUNUM MODU TOGGLE ──
    _toggle_presentation_mode()

    # ── HERO HEADER ──
    st.markdown(f"""<div class="ld-hero">
    <h2>📘 Unit {unit_num}: {theme}</h2>
    <div class="sub">{theme_tr} · {sel_label} · Hafta {sel_week} · {DAY_NAMES[sel_day]}</div>
    <div class="meta">📝 {structure[:100]}{'...' if len(structure)>100 else ''} · 📚 {len(vocab)} kelime</div>
    <div style="display:flex;gap:12px;margin-top:10px;">
        <div style="background:rgba(99,102,241,.08);border:1px solid {l1_color}40;border-radius:8px;
        padding:8px 14px;flex:1;">
            <div style="color:{l1_color};font-weight:700;font-size:.85rem;">{l1_icon} 1. Ders: {lesson1_label}</div>
            <div style="color:#94A3B8;font-size:.75rem;margin-top:2px;">{lesson1_detail}</div>
        </div>
        <div style="background:rgba(99,102,241,.08);border:1px solid {l2_color}40;border-radius:8px;
        padding:8px 14px;flex:1;">
            <div style="color:{l2_color};font-weight:700;font-size:.85rem;">{l2_icon} 2. Ders: {lesson2_label}</div>
            <div style="color:#94A3B8;font-size:.75rem;margin-top:2px;">{lesson2_detail}</div>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    # ── AI içerik yükle ──
    ai = load_unit_content(grade_num, unit_num)

    # ── Bağlam izleme — sınıf/hafta/gün değişince faz sıfırla ──
    _ctx = f"{grade_num}_{sel_week}_{sel_day}"
    if st.session_state.get("_ld_ctx") != _ctx:
        st.session_state["_ld_ctx"] = _ctx
        st.session_state["_ld_phase_L1"] = 0
        st.session_state["_ld_phase_L2"] = 0
        st.session_state["_ld_done"] = []
        st.session_state["_ld_sid"] = ""

    l1_phases = [p for p in _TEACHER_PHASES if p["lesson"] == 1]
    l2_phases = [p for p in _TEACHER_PHASES if p["lesson"] == 2]
    l1_total_min = sum(p["minutes"] for p in l1_phases)
    l2_total_min = sum(p["minutes"] for p in l2_phases)

    # ══════════════════════════════════════════════════════════════════════════
    # 1) DERS PLANI — Dakika Bazlı Görünüm
    # ══════════════════════════════════════════════════════════════════════════
    with st.expander("Ders Planı — Dakika Bazlı", expanded=True):
        pc1, pc2 = st.columns(2)
        with pc1:
            rows1 = "".join(
                f'<div style="display:flex;justify-content:space-between;padding:5px 0;'
                f'border-bottom:1px solid rgba(255,255,255,.04);">'
                f'<span style="color:#c7d2fe;font-size:.85rem;">{p["icon"]} {p["label"]}</span>'
                f'<span style="color:#818cf8;font-size:.8rem;font-weight:600;">{p["minutes"]} dk</span>'
                f'</div>' for p in l1_phases
            )
            st.markdown(
                f'<div style="background:rgba(99,102,241,.06);border:1px solid {l1_color}30;'
                f'border-radius:12px;padding:14px;">'
                f'<div style="color:{l1_color};font-weight:700;font-size:.95rem;margin-bottom:8px;">'
                f'{l1_icon} 1. Ders: {lesson1_label} ({l1_total_min} dk)</div>'
                f'{rows1}</div>', unsafe_allow_html=True)
        with pc2:
            rows2 = "".join(
                f'<div style="display:flex;justify-content:space-between;padding:5px 0;'
                f'border-bottom:1px solid rgba(255,255,255,.04);">'
                f'<span style="color:#c7d2fe;font-size:.85rem;">{p["icon"]} {p["label"]}</span>'
                f'<span style="color:#818cf8;font-size:.8rem;font-weight:600;">{p["minutes"]} dk</span>'
                f'</div>' for p in l2_phases
            )
            st.markdown(
                f'<div style="background:rgba(16,185,129,.04);border:1px solid {l2_color}30;'
                f'border-radius:12px;padding:14px;">'
                f'<div style="color:{l2_color};font-weight:700;font-size:.95rem;margin-bottom:8px;">'
                f'{l2_icon} 2. Ders: {lesson2_label} ({l2_total_min} dk)</div>'
                f'{rows2}</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # 2) OTURUM KONTROLÜ — Ders Başlat / Bitir
    # ══════════════════════════════════════════════════════════════════════════
    _sid = st.session_state.get("_ld_sid", "")
    store = LessonDeliveryStore()
    done_list = st.session_state.get("_ld_done", [])
    done_count = len(done_list)

    _sc1, _sc2 = st.columns([3, 1])
    with _sc1:
        _status_txt = "\u23F1\uFE0F Ders devam ediyor" if _sid else "\u23F8\uFE0F Ders ba\u015Flamad\u0131"
        st.markdown(
            f'<div style="background:rgba(99,102,241,.06);border-radius:10px;padding:10px 16px;'
            f'display:flex;align-items:center;justify-content:space-between;">'
            f'<span style="color:#c7d2fe;font-weight:600;">{_status_txt}</span>'
            f'<span style="color:#818cf8;font-size:.85rem;">'
            f'{done_count}/{len(_TEACHER_PHASES)} faz</span></div>',
            unsafe_allow_html=True)
    with _sc2:
        if not _sid:
            if st.button("\u25B6\uFE0F Derse Ba\u015Fla",
                         type="primary", use_container_width=True):
                _ld_sinif = st.session_state.get("yd_sinif") or st.session_state.get("sinif") or grade_num
                _ld_sube = st.session_state.get("yd_sube") or st.session_state.get("sube") or "A"
                session = store.create_session(
                    teacher_id=st.session_state.get("user_id", "teacher"),
                    teacher_name=st.session_state.get("display_name", st.session_state.get("username", "")),
                    grade=grade_num, sinif=int(_ld_sinif) if _ld_sinif else grade_num,
                    sube=_ld_sube or "", level=sel_grade,
                    week=sel_week, day_key=sel_day, unit_num=unit_num,
                    theme=theme, theme_tr=theme_tr,
                    structure=structure[:200] if structure else "",
                    vocab=vocab[:12])
                st.session_state["_ld_sid"] = session.id
                st.rerun()
        else:
            if st.button("\U0001F3C1 Dersi Bitir",
                         use_container_width=True):
                _completed = store.complete_session(_sid, completed_phases=done_list)
                # Gunluk ozete kaydet
                if _completed:
                    _ld_write_gunluk_ozet(_completed, done_list)
                st.session_state["_ld_sid"] = ""
                st.balloons()
                st.success(
                    f"\u2705 Ders tamamland\u0131 \u2014 "
                    f"{done_count}/{len(_TEACHER_PHASES)} faz i\u015Flendi")

    # ══════════════════════════════════════════════════════════════════════════
    # 3) 1. DERS / 2. DERS SEKMELERİ + FAZ FAZ İLERLEME
    # ══════════════════════════════════════════════════════════════════════════
    lesson_tabs = st.tabs([
        f"{l1_icon} 1. Ders: {lesson1_label} ({l1_total_min} dk)",
        f"{l2_icon} 2. Ders: {lesson2_label} ({l2_total_min} dk)",
    ])

    for lesson_num, ltab in enumerate(lesson_tabs, 1):
        with ltab:
            phases = l1_phases if lesson_num == 1 else l2_phases
            pk = f"_ld_phase_L{lesson_num}"
            if pk not in st.session_state:
                st.session_state[pk] = 0
            ci = min(st.session_state.get(pk, 0), len(phases) - 1)
            phase = phases[ci]
            total = len(phases)
            elapsed = sum(p["minutes"] for p in phases[:ci])
            phase_id = f"L{lesson_num}_{phase['key']}"

            # ── Faz başlığı + ilerleme barı ──
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);'
                f'border-radius:12px;padding:14px 18px;margin-bottom:12px;'
                f'border:1.5px solid rgba(99,102,241,.25);">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div style="color:#818cf8;font-size:.85rem;font-weight:600;">'
                f'Faz {ci+1}/{total} \u00B7 {elapsed} dk ge\u00E7ti</div>'
                f'<div style="color:#f59e0b;font-size:.85rem;font-weight:600;">'
                f'\u23F1\uFE0F {phase["minutes"]} dakika</div></div>'
                f'<div style="font-size:1.15rem;font-weight:700;color:#c7d2fe;margin-top:6px;">'
                f'{phase["icon"]} {phase["label"]}</div>'
                f'<div style="color:#64748b;font-size:.82rem;margin-top:2px;">{phase["desc"]}</div>'
                f'<div style="background:rgba(99,102,241,.1);border-radius:6px;'
                f'height:6px;margin-top:10px;overflow:hidden;">'
                f'<div style="width:{(ci+1)/total*100}%;height:100%;'
                f'background:linear-gradient(90deg,#6366F1,#8B5CF6);'
                f'border-radius:6px;transition:width .4s;"></div></div>'
                f'</div>', unsafe_allow_html=True)

            # ── Faz mini-harita (dot progress) ──
            dots = ""
            for di, dp in enumerate(phases):
                dp_id = f"L{lesson_num}_{dp['key']}"
                if dp_id in done_list:
                    dot_clr = "#22c55e"
                elif di == ci:
                    dot_clr = "#818cf8"
                else:
                    dot_clr = "#334155"
                dots += (f'<div style="width:10px;height:10px;border-radius:50%;'
                         f'background:{dot_clr};"></div>')
            st.markdown(
                f'<div style="display:flex;gap:6px;justify-content:center;'
                f'margin-bottom:12px;">{dots}</div>',
                unsafe_allow_html=True)

            # ── C12: Faz Geçiş Animasyonu ──
            prev_p = phases[ci - 1] if ci > 0 else None
            _phase_transition(prev_p, phase)

            # ── A1: Zamanlayıcı + A3: Öğrenci Seçici ──
            _tc1, _tc2 = st.columns([2, 1])
            with _tc1:
                _countdown_timer(phase["minutes"], f"L{lesson_num}_{phase['key']}")
            with _tc2:
                _random_student_picker(grade_num, st.session_state.get("sube", "A"))

            # ── A5: Öğretmen Rehber Notları ──
            _render_teacher_guide(phase["key"])

            # ── C11: Seviye Farklılaştırma ──
            _differentiation_panel(phase["key"], ai, vocab, theme, structure)

            # ── Aktif fazı render et ──
            _render_teacher_phase(
                phase["key"], ai, vocab, theme, theme_tr,
                structure, week_data, sel_grade, ukey)

            # ── A4: Hızlı Yoklama ──
            _quick_poll(phase["key"], ai, vocab, ukey)

            # ── Navigasyon butonları ──
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if ci > 0:
                    if st.button("\u2190 \u00D6nceki"):
                        st.session_state[pk] = ci - 1
                        st.rerun()
            with nav2:
                if phase_id not in done_list:
                    if st.button(
                            "\u2705 Tamamla ve \u0130lerle",
                            type="primary", use_container_width=True):
                        done_list.append(phase_id)
                        st.session_state["_ld_done"] = done_list
                        if ci < total - 1:
                            st.session_state[pk] = ci + 1
                        st.rerun()
                else:
                    st.markdown(
                        '<div style="text-align:center;color:#22c55e;'
                        'font-weight:600;padding:8px;">'
                        '\u2713 Tamamland\u0131</div>',
                        unsafe_allow_html=True)
            with nav3:
                if ci < total - 1:
                    if st.button("Sonraki \u2192"):
                        st.session_state[pk] = ci + 1
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # 4) DERS SONU ÖZETİ
    # ══════════════════════════════════════════════════════════════════════════
    done_list = st.session_state.get("_ld_done", [])
    done_count = len(done_list)
    total_phases = len(_TEACHER_PHASES)
    pct = round(done_count / total_phases * 100) if total_phases else 0

    st.markdown(
        f'<div class="ld-phase" style="border-color:rgba(99,102,241,.3);">'
        f'<p class="ld-phase-title" style="color:#818cf8;">'
        f'\U0001F4CA Ders \u00D6zeti</p>'
        f'<p class="ld-phase-sub">{l1_icon} 1. Ders: {lesson1_label} \u00B7 '
        f'{l2_icon} 2. Ders: {lesson2_label} \u00B7 '
        f'\u0130lerleme: {done_count}/{total_phases} faz (%{pct})</p>'
        f'</div>', unsafe_allow_html=True)
    sc = st.columns(4)
    labels = ["\U0001F4D8 Main Course", "\U0001F4D5 Workbook",
              "\U0001F4D6 Reading", "\U0001F4DD Vocabulary"]
    checks = [
        bool(ai and (ai.get("grammar_focus") or ai.get("dialogue") or ai.get("song_chant"))),
        bool(ai and ai.get("exercises")),
        bool(ai and (ai.get("story") or ai.get("reading_passage") or ai.get("culture_corner"))),
        bool(ai and ai.get("vocabulary_enrichment")),
    ]
    for i, (lbl, chk) in enumerate(zip(labels, checks)):
        with sc[i]:
            st.metric(lbl, "\u2713 Used" if chk else "\u2014")

    # ══════════════════════════════════════════════════════════════════════════
    # 5) ÇIKIŞ BİLETİ + 6) OTOMATİK ÖDEV + B8-B9-C10
    # ══════════════════════════════════════════════════════════════════════════
    _exit_ticket(ai, vocab, theme, ukey)
    _auto_homework(ai, vocab, theme, structure, grade_num, unit_num, ukey)
    _parent_notification(theme, vocab, structure, grade_num, unit_num, ukey)
    _absent_student_pack(ai, vocab, theme, structure, grade_num, unit_num, ukey)
    _video_suggestions(theme, vocab, grade_num)


# ═══════════════════════════════════════════════════════════════════════════════
# ÖĞRENCİ — ETKİLEŞİMLİ KİTAP
# ═══════════════════════════════════════════════════════════════════════════════

def render_lesson_delivery_student(level: str, student_id: str = "",
                                    student_name: str = "", sinif: int = 0, sube: str = ""):
    """Öğrenci etkileşimli çalışma kitabı."""
    _css()

    grade_num = get_grade_num(level)
    store = LessonDeliveryStore()
    today = get_today_info(level)

    unit_num = st.selectbox("Ünite", list(range(1, 11)),
                             index=min(today["unit_num"] - 1, 9),
                             format_func=lambda x: f"Unit {x}")

    ai = load_unit_content(grade_num, unit_num)
    if not ai:
        st.warning("Bu ünite için içerik henüz üretilmemiş.")
        return

    theme = ai.get("_meta", {}).get("theme", f"Unit {unit_num}")
    progress = store.get_unit_progress(student_id, level, unit_num)
    pct = progress["percentage"]
    ukey = f"s_g{grade_num}u{unit_num}"

    st.markdown(f"""<div class="ld-hero">
    <h2>Unit {unit_num}: {theme}</h2>
    <div class="sub">{progress['total_responses']} cevap · {progress['correct']} doğru · %{pct}</div>
    <div class="ld-progress" style="margin-top:10px;">
    <div class="ld-progress-fill" style="width:{pct}%;"></div></div>
    </div>""", unsafe_allow_html=True)

    vocab = [d.get("word", "") for d in ai.get("vocabulary_enrichment", {}).get("definitions", [])]

    tabs = st.tabs(["📘 Main Course", "📕 Workbook", "📖 Reading", "📝 Vocabulary"])

    with tabs[0]:
        _phase_warmup(ai, vocab, theme, "")
        story = ai.get("story", {})
        if story and story.get("text"):
            st.markdown(f"**📖 {story.get('title','')}**")
            st.markdown(f'<div class="ld-story">{story["text"]}</div>', unsafe_allow_html=True)
            _tts_text(story["text"], "Listen")
        gf = ai.get("grammar_focus", {})
        if gf and gf.get("rule"):
            st.markdown(f'<div class="ld-rule"><b>Rule:</b> <span>{gf["rule"]}</span></div>',
                        unsafe_allow_html=True)
            for ex in gf.get("examples", []):
                st.markdown(f"- *{ex}*")
        dlg = ai.get("dialogue", {})
        if dlg and dlg.get("lines"):
            speakers = dlg.get("speakers", ["A", "B"])
            for line in dlg["lines"]:
                sp_idx = line.get("speaker", 0)
                sp = speakers[sp_idx] if sp_idx < len(speakers) else "?"
                cls = "a" if sp_idx == 0 else "b"
                st.markdown(f'<div class="ld-dlg"><span class="{cls}">{sp}:</span> {line.get("text","")}</div>',
                            unsafe_allow_html=True)
        song = ai.get("song_chant", {})
        if song and song.get("lyrics"):
            for line in song["lyrics"].split("\n"):
                if line.strip():
                    st.markdown(f'<div class="ld-song">♫ {line.strip()}</div>', unsafe_allow_html=True)

    with tabs[1]:
        _phase_exercises(ai, ukey)
        if st.button("📤 Cevapları Kaydet"):
            saved = 0
            ex = ai.get("exercises", {})
            for i, fb in enumerate(ex.get("fill_blanks", [])):
                ans = st.session_state.get(f"ld_fb_{ukey}_{i}", "")
                if ans:
                    store.save_response(student_id=student_id, student_name=student_name,
                                         sinif=sinif, sube=sube, level=level, unit_num=unit_num,
                                         section="exercises", exercise_type="fill_blanks",
                                         question_index=i, student_answer=ans,
                                         correct_answer=fb.get("answer", ""))
                    saved += 1
            for i, md in enumerate(ex.get("matching", [])):
                ans = st.session_state.get(f"ld_mt_{ukey}_{i}", "")
                if ans and ans != "--":
                    store.save_response(student_id=student_id, student_name=student_name,
                                         sinif=sinif, sube=sube, level=level, unit_num=unit_num,
                                         section="exercises", exercise_type="matching",
                                         question_index=i, student_answer=ans,
                                         correct_answer=md.get("right", ""))
                    saved += 1
            st.success(f"✅ {saved} cevap kaydedildi!")

    with tabs[2]:
        story = ai.get("story", {})
        if story and story.get("text"):
            st.markdown(f"**📖 {story.get('title','')}**")
            st.markdown(f'<div class="ld-story">{story["text"]}</div>', unsafe_allow_html=True)
            _tts_text(story["text"], "Listen to the Story")
        rp = ai.get("reading_passage", {})
        if rp and rp.get("text"):
            st.markdown(f"**📖 {rp.get('title','')}**")
            st.markdown(f'<div class="ld-story" style="border-left-color:#059669;">{rp["text"]}</div>',
                        unsafe_allow_html=True)
            _tts_text(rp["text"], "Listen to the Passage")
            for i, q in enumerate(rp.get("questions", [])):
                st.markdown(f"**{i+1}.** {q}")
                st.text_input("", label_visibility="collapsed")
        cc = ai.get("culture_corner", {})
        if cc and cc.get("text"):
            st.markdown(f"**🌍 {cc.get('title','')}**")
            st.markdown(f'<div class="ld-story" style="border-left-color:#0EA5E9;">{cc["text"]}</div>',
                        unsafe_allow_html=True)

    with tabs[3]:
        ve = ai.get("vocabulary_enrichment", {})
        defs = ve.get("definitions", []) if ve else []
        if defs:
            cols = st.columns(2)
            for i, vd in enumerate(defs):
                with cols[i % 2]:
                    st.markdown(f"""<div class="ld-card" style="border-left:3px solid #818cf8;">
                    <div style="font-size:1rem;font-weight:700;color:#818cf8;">{vd.get('word','')}</div>
                    <div style="font-size:.82rem;color:#94A3B8;">{vd.get('definition','')}</div>
                    <div style="font-size:.78rem;color:#64748b;font-style:italic;">"{vd.get('example','')}"</div>
                    </div>""", unsafe_allow_html=True)
            _tts_words([d.get("word", "") for d in defs], "Pronunciation")

            st.markdown("#### 🧠 Quiz")
            for i, vd in enumerate(defs[:8]):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{i+1}.** {vd.get('definition','')}")
                with c2:
                    user = st.text_input("",
                                          label_visibility="collapsed", placeholder="?")
                    if user:
                        w = vd.get("word", "")
                        st.success("✅") if user.strip().lower() == w.lower() else st.error(f"❌ {w}")

    with st.expander("Tüm Üniteler", expanded=False):
        all_p = store.get_all_unit_progress(student_id, level)
        pc = st.columns(5)
        for u in range(1, 11):
            with pc[(u-1) % 5]:
                p = all_p[u]
                color = "#10B981" if p["percentage"] >= 70 else "#F59E0B" if p["percentage"] >= 40 else "#64748b"
                st.markdown(f"""<div style="text-align:center;padding:6px;background:rgba(99,102,241,.05);
                border-radius:8px;margin:3px 0;"><div style="color:{color};font-weight:700;">U{u}</div>
                <div style="font-size:.75rem;color:#94A3B8;">%{p['percentage']}</div></div>""",
                            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ANA RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render_lesson_delivery():
    """Ana ders işleme — rol bazlı."""
    inject_common_css()
    styled_header("🎓 Ders İşleme Motoru",
                  "Premium İngilizce Ders Anlatımı — Plan + 4 Kitap + Etkinlik + Telaffuz")

    role = st.session_state.get("role", "teacher")
    if role in ("veli", "student", "ogrenci"):
        student_id = st.session_state.get("student_id", "")
        student_name = st.session_state.get("student_name", "")
        sinif = st.session_state.get("sinif", 5)
        sube = st.session_state.get("sube", "A")
        level = f"grade{sinif}" if sinif > 0 else "preschool"
        render_lesson_delivery_student(level, student_id, student_name, sinif, sube)
    else:
        render_lesson_delivery_teacher()
