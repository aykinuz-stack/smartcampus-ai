"""
YD Core — Yabanci Dil modulu paylasilan yardimci fonksiyonlar.
Tum yd_*.py dosyalari buradan import eder (circular import onlenir).
"""
from __future__ import annotations

import json as _json
import os
import logging as _logging

import streamlit as st

_logger = _logging.getLogger("yabanci_dil")

# ── Veri Yollari ──
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "english")
_WP_PATH = os.path.join(_DATA_DIR, "weekly_plans.json")
_YP_PATH = os.path.join(_DATA_DIR, "year_plans.json")


def _data_path(filename: str) -> str:
    """Return full path for a file in data/english/."""
    return os.path.join(_DATA_DIR, filename)


def _load_json_cached(filename: str, force: bool = False) -> dict | list:
    """Load JSON file with session-level caching."""
    cache_key = f"_yd_cache_{filename}"
    if not force and cache_key in st.session_state:
        return st.session_state[cache_key]
    path = _data_path(filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = _json.load(f)
            st.session_state[cache_key] = data
            return data
        except (_json.JSONDecodeError, OSError) as e:
            _logger.warning("Failed to load %s: %s", filename, e)
            return {}
    return {}


def _save_json_cached(filename: str, data) -> bool:
    """Save JSON and update cache."""
    path = _data_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
        cache_key = f"_yd_cache_{filename}"
        st.session_state[cache_key] = data
        return True
    except OSError as e:
        _logger.error("Failed to save %s: %s", filename, e)
        return False


def _validate_grade(grade_str: str) -> str:
    """Validate and sanitize grade input."""
    valid = {"preschool", "grade1", "grade2", "grade3", "grade4",
             "grade5", "grade6", "grade7", "grade8",
             "grade9", "grade10", "grade11", "grade12",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}
    return grade_str if grade_str in valid else "grade5"


def _validate_week(week: int) -> int:
    """Validate week number is within bounds."""
    return max(1, min(36, int(week)))


def _sanitize_html(text: str) -> str:
    """Basic HTML sanitization for user-generated content."""
    if not isinstance(text, str):
        return str(text)
    return text.replace("<script", "&lt;script").replace("</script", "&lt;/script").replace("javascript:", "")


# ── Renk Paleti ──
_CLR_BLUE = "#4472C4"
_CLR_DARK = "#0B0F19"
_CLR_GREEN = "#70AD47"
_CLR_ORANGE = "#ED7D31"
_CLR_PURPLE = "#7c3aed"
_CLR_RED = "#dc2626"
_CLR_TEAL = "#2563eb"
_CLR_CYAN = "#0891b2"


# ── Duplicate render guard ──
_comp_rendered_keys: set = set()


def _get_academic_year_str() -> str:
    """Akademik yil string: 2025-2026."""
    from datetime import datetime
    today = datetime.now().date()
    start = today.year if today.month >= 9 else today.year - 1
    return f"{start}-{start + 1}"


def _get_sinif_sube_options() -> list[tuple[int, str]]:
    """Mevcut ogrenci verilerinden benzersiz sinif/sube listesi."""
    from utils.shared_data import load_shared_students
    students = load_shared_students()
    pairs = set()
    for s in students:
        sinif = s.get("sinif")
        sube = s.get("sube", "")
        if sinif and sube:
            try:
                pairs.add((int(sinif), sube))
            except (ValueError, TypeError):
                pass
    return sorted(pairs)


def _yd_sinif_to_level(sinif):
    """Global sinif -> mufredat seviyesi. None = genel."""
    if sinif is None:
        return None
    sinif_str = str(sinif).lower()
    if "anas" in sinif_str or "okul " in sinif_str and "nc" in sinif_str:
        return "preschool"
    try:
        sinif = int(sinif)
    except (ValueError, TypeError):
        return None
    if sinif == 0:
        return "preschool"
    return f"grade{sinif}" if 1 <= sinif <= 12 else None


def _academic_week_dates(week_num: int) -> tuple:
    """Hafta numarasindan (Pzt, Cum) tarihlerini hesapla."""
    from datetime import date, timedelta
    today = date.today()
    yr = today.year if today.month >= 9 else today.year - 1
    sep1 = date(yr, 9, 1)
    days_to_mon = (7 - sep1.weekday()) % 7
    first_mon = sep1 + timedelta(days=days_to_mon) if sep1.weekday() != 0 else sep1
    start = first_mon + timedelta(weeks=1)
    if week_num < 1 or week_num > 36:
        return (None, None)
    if week_num <= 18:
        monday = start + timedelta(weeks=week_num - 1)
    else:
        monday = start + timedelta(weeks=week_num - 1 + 2)
    friday = monday + timedelta(days=4)
    return (monday, friday)


def _get_today_plan_info():
    """Bugunun akademik hafta, gun ve plan bilgisini dondurur."""
    from datetime import date, timedelta
    today = date.today()
    yr = today.year if today.month >= 9 else today.year - 1
    sep1 = date(yr, 9, 1)
    days_to_mon = (7 - sep1.weekday()) % 7
    first_mon = sep1 + timedelta(days=days_to_mon) if sep1.weekday() != 0 else sep1
    start = first_mon + timedelta(weeks=1)
    delta = (today - start).days
    _day_keys = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    _day_names = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
    dow = today.weekday()
    is_school = dow < 5
    day_key = _day_keys[dow] if dow < 5 else None
    day_name = _day_names[dow]
    if delta < 0:
        week_num = 1
    else:
        raw_week = delta // 7 + 1
        sem1_end = start + timedelta(weeks=18)
        sem2_start = sem1_end + timedelta(weeks=2)
        if today < sem1_end:
            week_num = raw_week
        elif today < sem2_start:
            week_num = 18
            is_school = False
        else:
            week_num = (today - sem2_start).days // 7 + 19
        week_num = max(1, min(36, week_num))
    _wp_cache_key = "_yd_weekly_plans_cache"
    if _wp_cache_key not in st.session_state:
        try:
            with open(_WP_PATH, "r", encoding="utf-8") as _f:
                st.session_state[_wp_cache_key] = _json.load(_f)
        except Exception:
            st.session_state[_wp_cache_key] = {}
    _wp = st.session_state[_wp_cache_key]
    return {
        "week_num": week_num,
        "day_key": day_key,
        "day_name": day_name,
        "date_str": today.strftime("%d.%m.%Y"),
        "is_school_day": is_school,
        "all_plans": _wp,
    }


def _render_daily_plan_panel(grade_key, plan_info=None):
    """Belirli bir sinif icin bugunun gunluk planini gosterir."""
    if plan_info is None:
        plan_info = _get_today_plan_info()
    _wn = plan_info["week_num"]
    _dk = plan_info["day_key"]
    _dn = plan_info["day_name"]
    _ds = plan_info["date_str"]
    _is_school = plan_info["is_school_day"]
    _wp = plan_info["all_plans"]
    _grade_weeks = _wp.get(str(grade_key), [])
    _week_data = None
    for w in _grade_weeks:
        if w.get("week") == _wn:
            _week_data = w
            break
    _theme_name = ""
    _theme_tr = ""
    if _week_data:
        _theme_name = _week_data.get("unit_theme") or _week_data.get("theme", "")
        _theme_tr = _week_data.get("unit_theme_tr") or _week_data.get("theme_tr", "")
    _mon, _fri = _academic_week_dates(_wn)
    _date_range = ""
    if _mon and _fri:
        _date_range = f" ({_mon.strftime('%d.%m')} - {_fri.strftime('%d.%m')})"
    _theme_display = _theme_name
    if _theme_tr:
        _theme_display = f"{_theme_name} ({_theme_tr})" if _theme_name else _theme_tr
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#111827,#eef2ff);'
        f'border:1.5px solid #c7d2fe;border-radius:14px;padding:16px 20px;margin:14px 0;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.04);">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">'
        f'<div>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#4f46e5;">'
        f'&#x1F4C5; Gunluk Plan &mdash; {_dn}, {_ds}</div>'
        f'<div style="font-size:.8rem;color:#6366f1;margin-top:2px;">'
        f'Hafta {_wn}/36{_date_range}</div></div>'
        f'<div style="font-size:.75rem;color:#64748b;text-align:right;">'
        f'{_theme_display}'
        f'{"" if _is_school else " &mdash; <span style=color:#f87171;font-weight:700>Okul Disi Gun</span>"}'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )
    if not _is_school:
        return
    if not _week_data:
        st.caption("Bu hafta icin plan verisi bulunamadi.")
        return
    _days = _week_data.get("days", {})
    _today = _days.get(_dk, {}) if _dk else {}
    _hours = _today.get("hours", [])
    if not _hours:
        st.caption(f"{_dn} icin ders saati tanimli degil.")
        return
    _cols_h = st.columns(min(len(_hours), 5))
    for _hi, _hd in enumerate(_hours[:5]):
        with _cols_h[_hi]:
            _slot = _hd.get("slot", "MAIN COURSE")
            _focus = _hd.get("focus", "—")
            _dur = _hd.get("duration", "40 dk")
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0c4a6e20,#0ea5e910);'
                f'border:1px solid #0ea5e933;border-radius:10px;padding:10px 12px;'
                f'text-align:center;min-height:100px;">'
                f'<div style="font-size:.7rem;color:#38bdf8;font-weight:700;">'
                f'{_hd.get("hour","?")}. Saat</div>'
                f'<div style="font-size:.68rem;color:#7dd3fc;margin:2px 0;">{_slot}</div>'
                f'<div style="font-size:.72rem;color:#e2e8f0;font-weight:600;'
                f'margin:4px 0;line-height:1.3;">{_focus[:50]}</div>'
                f'<div style="font-size:.62rem;color:#64748b;">{_dur}</div></div>',
                unsafe_allow_html=True,
            )


# ── English Progress Helpers ──
_comp_rendered_keys: set = set()


def _get_eng_store():
    """English progress store singleton-benzeri erisim."""
    from models.english_progress import EnglishProgressStore
    return EnglishProgressStore()


def _get_eng_student_id() -> str:
    """Mevcut ogrenci ID'sini dondurur."""
    return st.session_state.get("auth_user", {}).get("username", "anonymous")


def _eng_load_completions_cache(key_prefix: str) -> set[str]:
    """Tamamlanan alistirma ID'lerini session_state cache'ine yukler."""
    cache_key = f"_eng_comp_cache_{key_prefix}"
    if cache_key not in st.session_state:
        sid = _get_eng_student_id()
        if sid == "anonymous":
            st.session_state[cache_key] = set()
        else:
            store = _get_eng_store()
            st.session_state[cache_key] = store.get_completed_exercise_ids(sid, key_prefix)
    return st.session_state[cache_key]


def _eng_is_completed(key_prefix: str, tab_type: str, index: int) -> bool:
    """Belirli bir alistirmanin tamamlanip tamamlanmadigini kontrol eder."""
    return f"{key_prefix}_{tab_type}_{index}" in _eng_load_completions_cache(key_prefix)


def _eng_render_completion_button(key_prefix: str, tab_type: str, index: int, exercise_name: str):
    """Alistirma iframe'i altinda 'Tamamladim' butonu gosterir."""
    from models.english_progress import ExerciseCompletion, award_xp_and_check_badges
    sid = _get_eng_student_id()
    if sid == "anonymous":
        return
    _dup_key = f"{key_prefix}_{tab_type}_{index}"
    if _dup_key in _comp_rendered_keys:
        return
    _comp_rendered_keys.add(_dup_key)
    exercise_id = f"{key_prefix}_{tab_type}_{index}"
    already = _eng_is_completed(key_prefix, tab_type, index)
    if already:
        st.markdown(
            '<div style="text-align:center;padding:6px;margin-top:-8px;">'
            '<span style="background:#059669;color:#fff;padding:4px 16px;border-radius:20px;'
            'font-size:13px;font-weight:600;">\u2705 Bu alistirmayi tamamladiniz!</span></div>',
            unsafe_allow_html=True,
        )
    else:
        if st.button(
            "\u2705 Tamamladim",
            key=f"comp_{key_prefix}_{tab_type}_{index}",
            use_container_width=True,
        ):
            comp = ExerciseCompletion(
                student_id=sid,
                exercise_id=exercise_id,
                exercise_name=exercise_name,
                level=key_prefix,
                tab_type=tab_type,
                tab_index=index,
            )
            store = _get_eng_store()
            store.upsert("completions", comp)
            new_badges = award_xp_and_check_badges(store, sid, key_prefix)
            if new_badges:
                st.session_state["_eng_new_badges"] = new_badges
            st.session_state.pop(f"_eng_comp_cache_{key_prefix}", None)
            st.rerun()


def _eng_render_progress_dashboard(key_prefix: str):
    """Seviye basinda mini ilerleme dashboard'u."""
    from models.english_progress import get_total_exercises
    sid = _get_eng_student_id()
    if sid == "anonymous":
        return
    store = _get_eng_store()
    comps = store.get_student_completions(sid, level=key_prefix)
    total = get_total_exercises(key_prefix)
    done = len({c["exercise_id"] for c in comps})
    streak = store.calculate_streak(sid)
    pct = round(done / total * 100) if total > 0 else 0
    last_act = comps[-1]["completed_at"][:10] if comps else "---"
    stats = [
        ("\u2705 Tamamlanan", f"{done}/{total}", "#059669"),
        ("\U0001F4CA Ilerleme", f"%{pct}", "#2563eb"),
        ("\U0001F525 Seri", f"{streak} gun", "#2563eb"),
        ("\U0001F570 Son Aktivite", last_act, "#7c3aed"),
    ]
    cols = st.columns(len(stats))
    for col, (label, value, color) in zip(cols, stats):
        with col:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{color},{color}cc);color:#fff;'
                f'border-radius:10px;padding:10px 8px;text-align:center;">'
                f'<div style="font-size:1.2rem;font-weight:800;">{value}</div>'
                f'<div style="font-size:0.7rem;opacity:0.9;margin-top:2px;">{label}</div></div>',
                unsafe_allow_html=True,
            )


def _eng_render_gamification_banner(key_prefix: str):
    """XP bar + rozetler + streak gosterimi."""
    from models.english_progress import BADGE_DEFINITIONS
    sid = _get_eng_student_id()
    if sid == "anonymous":
        return
    store = _get_eng_store()
    profile = store.get_gamification_profile(sid)
    if not profile:
        return
    xp = profile.xp
    badges = profile.badges or []
    streak = profile.streak_days
    level_num = xp // 100 + 1
    level_pct = xp % 100
    badge_html = ""
    for b in badges:
        bd = BADGE_DEFINITIONS.get(b, {})
        badge_html += f'<span title="{bd.get("name", b)}: {bd.get("desc", "")}" style="font-size:20px;margin:0 2px;cursor:help;">{bd.get("emoji", "\U0001F3C5")}</span>'
    with st.expander(f"\U0001F3C6 XP: {xp} | Seviye: {level_num} | \U0001F525 {streak} gun | Rozetler: {len(badges)}", expanded=False):
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:12px;padding:12px 16px;margin-bottom:8px;">'
            f'<div style="display:flex;justify-content:space-between;color:#c4b5fd;font-size:13px;margin-bottom:4px;">'
            f'<span>Seviye {level_num}</span><span>{level_pct}/100 XP</span></div>'
            f'<div style="background:rgba(168,85,247,0.2);border-radius:8px;height:12px;overflow:hidden;">'
            f'<div style="background:linear-gradient(90deg,#7c3aed,#a855f7);width:{level_pct}%;height:100%;'
            f'border-radius:8px;transition:width 0.5s;"></div></div></div>',
            unsafe_allow_html=True,
        )
        if badge_html:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:12px;'
                f'padding:12px;text-align:center;">'
                f'<div style="font-size:12px;color:#a78bfa;margin-bottom:6px;">Kazanilan Rozetler</div>'
                f'{badge_html}</div>',
                unsafe_allow_html=True,
            )


def _eng_render_adaptive_recommendations(key_prefix: str):
    """Kisisellestirilmis oneri banner'i."""
    from models.english_progress import AdaptiveLearningEngine
    sid = _get_eng_student_id()
    if sid == "anonymous":
        return
    store = _get_eng_store()
    rec = AdaptiveLearningEngine.get_recommendations(store, sid, key_prefix)
    if rec["type"] == "zor_set":
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#059669,#047857);color:#fff;'
            f'padding:14px 18px;border-radius:12px;margin-bottom:12px;">'
            f'<div style="font-weight:700;font-size:15px;">\U0001F680 Zor Set Onerisi</div>'
            f'<div style="font-size:13px;margin-top:4px;">{rec["message"]}</div></div>',
            unsafe_allow_html=True,
        )
    elif rec["type"] == "tekrar_set":
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#2563eb,#1e40af);color:#fff;'
            f'padding:14px 18px;border-radius:12px;margin-bottom:12px;">'
            f'<div style="font-weight:700;font-size:15px;">\U0001F4D6 Tekrar Onerisi</div>'
            f'<div style="font-size:13px;margin-top:4px;">{rec["message"]}</div></div>',
            unsafe_allow_html=True,
        )
