"""
Akademik Takip Modulu
=====================
SmartCampus AI için akademik takip yonetimi.
Ogrenci basarisi, ders takibi, sinav sonuclari ve akademik performans izleme.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from typing import Optional

import pandas as pd
import streamlit as st

from utils.tenant import tenant_key, get_tenant_dir
from utils.report_utils import ReportStyler, get_institution_info
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("akademik_takip")
except Exception:
    pass

# ==================== PATHS ====================


def get_calendar_path() -> str:
    return os.path.join(get_tenant_dir(), "academic_calendar.json")


# ==================== DATA I/O ====================

def load_calendar_data() -> dict:
    """Takvim verilerini yukle"""
    path = get_calendar_path()
    if not os.path.exists(path):
        return {
            "events": [],
            "semesters": [],
            "holidays": [],
            "exam_periods": []
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "events": [],
            "semesters": [],
            "holidays": [],
            "exam_periods": []
        }


def save_calendar_data(data: dict) -> None:
    """Takvim verilerini kaydet"""
    path = get_calendar_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==================== CONSTANTS ====================

EVENT_TYPES = [
    # Akademik Yil Yapisi
    "Akademik Yil Baslangic",
    "Akademik Yil Bitis",
    "1. Donem Baslangic",
    "1. Donem Bitis",
    "2. Donem Baslangic",
    "2. Donem Bitis",
    # Tatiller
    "Yariyil Tatili",
    "Ara Tatil",
    "Somestre Tatili",
    "Resmi Tatil",
    "Idari Tatil",
    # Sinav & Olcme
    "Sinav",
    "Yazili Sinav",
    "Sozlu Sinav",
    "Deneme Sinavi (LGS/TYT/AYT)",
    "Performans Gorevi",
    "Proje Teslim",
    "KYT (Kazanim Olcme)",
    # Toplanti & Kurul
    "Toplanti",
    "Ogretmenler Kurulu",
    "Zumre Toplantisi",
    "Veli Toplantisi",
    "Veli Gorusmesi",
    "Kurul/Komisyon",
    # Etkinlik & Sosyal
    "Gezi / Gozlem",
    "Seminer / Konferans",
    "Panel / Soylesi",
    "Atolye Calismasi",
    "Spor Etkinligi",
    "Spor Yarismasi / Turnuva",
    "Kultur Sanat",
    "Tiyatro / Gosteri",
    "Konser / Muzik",
    "Sergi / Fuar",
    "Bilim Festivali",
    "STEM / Robotik",
    "Kutlama / Anma / Toren",
    "Mezuniyet",
    "Kermes / Yardim",
    # Kayit & Tanitim
    "Ogrenci Kayit Donemi",
    "Acik Kapi Gunu",
    "Tanitim Etkinligi",
    "Kampanya Donemi",
    # Karne & Rapor
    "Karne Gunu",
    "Rapor Teslim",
    # Saglik & Guvenlik
    "Saglik Taramasi",
    "Tatbikat (Yangin/Deprem)",
    "Ilk Yardim Egitimi",
    # Egitim & Gelisim
    "Ogretmen Egitimi / Seminer",
    "Personel Gelisim",
    "Mesleki Calisma",
    # Diger
    "Genel Etkinlik",
    "Diger",
]

EVENT_COLORS = {
    "Akademik Yil Baslangic": "#1a237e", "Akademik Yil Bitis": "#1a237e",
    "1. Donem Baslangic": "#0d47a1", "1. Donem Bitis": "#0d47a1",
    "2. Donem Baslangic": "#0d47a1", "2. Donem Bitis": "#0d47a1",
    "Yariyil Tatili": "#9C27B0", "Ara Tatil": "#9C27B0", "Somestre Tatili": "#9C27B0",
    "Resmi Tatil": "#d32f2f", "Idari Tatil": "#c62828",
    "Sinav": "#F44336", "Yazili Sinav": "#e53935", "Sozlu Sinav": "#ef5350",
    "Deneme Sinavi (LGS/TYT/AYT)": "#b71c1c", "Performans Gorevi": "#ff7043",
    "Proje Teslim": "#ff5722", "KYT (Kazanim Olcme)": "#e64a19",
    "Toplanti": "#2196F3", "Ogretmenler Kurulu": "#1565c0",
    "Zumre Toplantisi": "#1976d2", "Veli Toplantisi": "#FF9800",
    "Veli Gorusmesi": "#FB8C00", "Kurul/Komisyon": "#42a5f5",
    "Gezi / Gozlem": "#CDDC39", "Seminer / Konferans": "#7c4dff",
    "Panel / Soylesi": "#651fff", "Atolye Calismasi": "#00bfa5",
    "Spor Etkinligi": "#8BC34A", "Spor Yarismasi / Turnuva": "#689f38",
    "Kultur Sanat": "#673AB7", "Tiyatro / Gosteri": "#7b1fa2",
    "Konser / Muzik": "#ab47bc", "Sergi / Fuar": "#4a148c",
    "Bilim Festivali": "#03A9F4", "STEM / Robotik": "#0288d1",
    "Kutlama / Anma / Toren": "#e91e63", "Mezuniyet": "#E91E63",
    "Kermes / Yardim": "#f06292",
    "Ogrenci Kayit Donemi": "#795548", "Acik Kapi Gunu": "#8d6e63",
    "Tanitim Etkinligi": "#a1887f", "Kampanya Donemi": "#6d4c41",
    "Karne Gunu": "#00BCD4", "Rapor Teslim": "#0097a7",
    "Saglik Taramasi": "#43a047", "Tatbikat (Yangin/Deprem)": "#c62828",
    "Ilk Yardim Egitimi": "#2e7d32",
    "Ogretmen Egitimi / Seminer": "#5c6bc0", "Personel Gelisim": "#3f51b5",
    "Mesleki Calisma": "#283593",
    "Genel Etkinlik": "#4CAF50", "Diger": "#607D8B",
}

MONTHS_TR = [
    "Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
    "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"
]

DAYS_TR = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]

KADEMELER = [
    "Anaokulu",
    "İlkokul",
    "Ortaokul",
    "Lise",
    "Tüm Kademeler"
]


# ==================== HELPER FUNCTIONS ====================

def get_month_calendar(year: int, month: int) -> list[list[Optional[int]]]:
    """Ay için takvim grid'i olustur"""
    import calendar
    cal = calendar.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdayscalendar(year, month):
        weeks.append([day if day != 0 else None for day in week])
    return weeks


def get_events_for_date(events: list[dict], target_date: str) -> list[dict]:
    """Belirli bir tarihteki etkinlikleri getir"""
    return [e for e in events if (e.get("date") or e.get("tarih") or "") == target_date]


def get_events_for_month(events: list[dict], year: int, month: int) -> list[dict]:
    """Belirli bir aydaki etkinlikleri getir"""
    prefix = f"{year:04d}-{month:02d}"
    return [e for e in events if (e.get("date") or e.get("tarih") or "").startswith(prefix)]


def format_date_turkish(date_str: str) -> str:
    """Tarihi Turkce formatta goster"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.day} {MONTHS_TR[dt.month - 1]} {dt.year}"
    except Exception:
        return date_str


_AY_AD = {1:"Ocak",2:"Subat",3:"Mart",4:"Nisan",5:"Mayis",6:"Haziran",
          7:"Temmuz",8:"Agustos",9:"Eylul",10:"Ekim",11:"Kasim",12:"Aralik"}


def _quick_pdf_buttons(events: list, data: dict, prefix: str, bugun_override=None) -> None:
    """Aylik + Yillik PDF indirme buton cifti (tekrar eden kodu birlestir)."""
    _b = bugun_override or date.today()
    _yb = _b.year if _b.month >= 9 else _b.year - 1
    _ey = f"{_yb}-{_yb + 1}"
    _ey_bas = f"{_yb}-09-01"
    _ey_bit = f"{_yb + 1}-08-31"
    _yevts = [e for e in events if _ey_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= _ey_bit]

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📑 Aylık Plan PDF", key=f"{prefix}_aylik", use_container_width=True,
                      type="primary" if prefix.endswith("ust") else "secondary"):
            try:
                from views._akt_yillik_plan import _generate_yillik_plan_pdf
                _pdf = _generate_yillik_plan_pdf(_yevts, _ey, _yb, _yb + 1, data.get("semesters", []), _b.month)
                if _pdf:
                    st.download_button(f"📥 {_AY_AD.get(_b.month,'')} {_b.year} PDF", _pdf,
                                       file_name=f"aylik_plan_{_AY_AD.get(_b.month,'')}_{_b.year}.pdf",
                                       mime="application/pdf", use_container_width=True, key=f"{prefix}_aylik_dl")
                else:
                    st.warning("PDF olusturulamadi.")
            except Exception as _e:
                st.error(f"PDF hatasi: {_e}")
    with c2:
        if st.button("📑 Yıllık Plan PDF", key=f"{prefix}_yillik", use_container_width=True,
                      type="primary" if prefix.endswith("ust") else "secondary"):
            try:
                from views._akt_yillik_plan import _generate_yillik_plan_pdf
                _pdf = _generate_yillik_plan_pdf(_yevts, _ey, _yb, _yb + 1, data.get("semesters", []), None)
                if _pdf:
                    st.download_button(f"📥 {_ey} Yıllık PDF", _pdf,
                                       file_name=f"yillik_calisma_plani_{_ey}.pdf",
                                       mime="application/pdf", use_container_width=True, key=f"{prefix}_yillik_dl")
                else:
                    st.warning("PDF olusturulamadi.")
            except Exception as _e:
                st.error(f"PDF hatasi: {_e}")


# ==================== UI COMPONENTS ====================

def render_calendar_grid(year: int, month: int, events: list[dict]) -> None:
    """Ay takvim grid'ini render et"""
    weeks = get_month_calendar(year, month)
    month_events = get_events_for_month(events, year, month)
    
    # Header - Gun isimleri
    cols = st.columns(7)
    for i, day_name in enumerate(DAYS_TR):
        with cols[i]:
            st.markdown(f"<div style='text-align:center;font-weight:bold;color:#666;padding:8px;'>{day_name}</div>", unsafe_allow_html=True)
    
    # Gunler
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day is not None:
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    day_events = get_events_for_date(month_events, date_str)
                    
                    # Bugun mu kontrol et
                    is_today = date_str == date.today().strftime("%Y-%m-%d")
                    
                    # Stil
                    bg_color = "#e3f2fd" if is_today else "#fafafa"
                    border = "2px solid #1976d2" if is_today else "1px solid #e0e0e0"
                    
                    # Etkinlik noktalari
                    event_dots = ""
                    if day_events:
                        dots = []
                        for evt in day_events[:3]:
                            color = EVENT_COLORS.get(evt.get("type", ""), "#607D8B")
                            dots.append(f"<span style='display:inline-block;width:8px;height:8px;border-radius:50%;background:{color};margin:1px;'></span>")
                        event_dots = "".join(dots)
                        if len(day_events) > 3:
                            event_dots += f"<span style='font-size:10px;'>+{len(day_events)-3}</span>"
                    
                    st.markdown(f"""
                        <div style='
                            background:{bg_color};
                            border:{border};
                            border-radius:8px;
                            padding:8px;
                            min-height:60px;
                            text-align:center;
                            margin:2px;
                        '>
                            <div style='font-size:1.1rem;font-weight:{"bold" if is_today else "normal"};'>{day}</div>
                            <div style='margin-top:4px;'>{event_dots}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='min-height:60px;'></div>", unsafe_allow_html=True)


def render_event_list(events: list[dict], year: int, month: int, data: dict | None = None) -> None:
    """Etkinlik listesini goster"""
    month_events = get_events_for_month(events, year, month)
    
    if not month_events:
        st.info("Bu ay için kayitli etkinlik bulunmuyor.")
        return
    
    # Tarihe gore sirala
    sorted_events = sorted(month_events, key=lambda x: x.get("date", ""))
    
    for event in sorted_events:
        color = EVENT_COLORS.get(event.get("type", ""), "#607D8B")
        eid = event.get("id", "")
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                evt_date = (event.get("date") or event.get("tarih") or "2025-01-01")[:10]
                try:
                    _day = evt_date[8:10]
                    _mon = MONTHS_TR[int(evt_date[5:7]) - 1][:3]
                except Exception:
                    _day, _mon = "?", "?"
                st.markdown(f"""
                    <div style='
                        background:{color};
                        color:white;
                        padding:8px 12px;
                        border-radius:8px;
                        text-align:center;
                        font-size:0.85rem;
                    '>
                        {_day}<br>
                        <small>{_mon}</small>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{event.get('title', 'Etkinlik')}**")
                st.caption(f"📍 {event.get('location', 'Belirtilmedi')} | 🏫 {event.get('kademe', 'Tüm Kademeler')} | 🏷️ {event.get('type', 'Genel')}")
                if event.get("description"):
                    st.write(event.get("description", ""))
            with col3:
                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("✏️", key=f"edit_{eid}"):
                        st.session_state["event_to_edit"] = eid
                with bc2:
                    if st.button("🗑���", key=f"del_{eid}"):
                        st.session_state["event_to_delete"] = eid
            st.divider()

    # ── DÜZENLEME FORMU (inline) ──
    if data:
        _render_edit_event_form(data, events)


# ==================== ÇAKIŞMA KONTROLÜ ====================

def _check_conflicts(events: list, target_date: str, kademe: str, exclude_id: str = "") -> list[dict]:
    """Ayni gun + ayni kademe'de cakisan etkinlikleri bul."""
    conflicts = []
    for e in events:
        if exclude_id and e.get("id") == exclude_id:
            continue
        e_date = (e.get("date") or e.get("tarih") or "")[:10]
        e_kademe = e.get("kademe", "")
        if e_date == target_date:
            # Ayni kademe veya biri "Tum Kademeler" ise cakisma var
            if kademe == e_kademe or kademe == "T��m Kademeler" or e_kademe == "Tüm Kademeler":
                conflicts.append(e)
    return conflicts


# ==================== ETKİNLİK DÜZENLEME ====================

def _render_edit_event_form(data: dict, events: list) -> None:
    """Secili etkinligi duzenle."""
    edit_id = st.session_state.get("event_to_edit")
    if not edit_id:
        return

    event = next((e for e in events if e.get("id") == edit_id), None)
    if not event:
        st.session_state["event_to_edit"] = None
        return

    st.markdown("---")
    st.subheader("✏️ Etkinlik Duzenle")

    with st.form("edit_event_form"):
        col1, col2 = st.columns(2)
        with col1:
            ed_title = st.text_input("Etkinlik Adi*", value=event.get("title", ""), key="ed_title")
            ed_type_idx = EVENT_TYPES.index(event.get("type", EVENT_TYPES[0])) if event.get("type") in EVENT_TYPES else 0
            ed_type = st.selectbox("Etkinlik Turu", EVENT_TYPES, index=ed_type_idx, key="ed_type")
            try:
                ed_date_val = date.fromisoformat((event.get("date") or event.get("tarih", ""))[:10])
            except Exception:
                ed_date_val = date.today()
            ed_date = st.date_input("Tarih*", value=ed_date_val, key="ed_date")

        with col2:
            ed_location = st.text_input("Konum", value=event.get("location", ""), key="ed_loc")
            ed_kademe_idx = KADEMELER.index(event.get("kademe", "Tüm Kademeler")) if event.get("kademe") in KADEMELER else len(KADEMELER) - 1
            ed_kademe = st.selectbox("Kademe", KADEMELER, index=ed_kademe_idx, key="ed_kademe")
            ed_end_raw = event.get("end_date") or event.get("bitis_tarihi") or ""
            try:
                ed_end_val = date.fromisoformat(ed_end_raw[:10]) if ed_end_raw else None
            except Exception:
                ed_end_val = None
            ed_end = st.date_input("Bitis Tarihi", value=ed_end_val, key="ed_end")

        ed_desc = st.text_area("Aciklama", value=event.get("description", ""), height=80, key="ed_desc")

        submitted = st.form_submit_button("💾 Guncelle", use_container_width=True)

        if submitted:
            if not ed_title:
                st.error("Etkinlik adi zorunludur!")
            else:
                event["title"] = ed_title
                event["type"] = ed_type
                event["date"] = ed_date.strftime("%Y-%m-%d")
                event["end_date"] = ed_end.strftime("%Y-%m-%d") if ed_end else None
                event["location"] = ed_location
                event["kademe"] = ed_kademe
                event["description"] = ed_desc
                event["updated_at"] = datetime.now().isoformat()
                save_calendar_data(data)
                st.success(f"'{ed_title}' guncellendi!")
                st.session_state["event_to_edit"] = None
                st.rerun()

    if st.button("Duzenlemeyi Iptal Et", key="ed_cancel"):
        st.session_state["event_to_edit"] = None
        st.rerun()


def render_add_event_form(data: dict) -> None:
    """Yeni etkinlik ekleme formu — cakisma kontrolu + tekrarlayan etkinlik destegi."""
    events = data.get("events", [])

    st.subheader("➕ Yeni Etkinlik Ekle")

    with st.form("add_event_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Etkinlik Adi*", placeholder="Ornek: 1. Donem Sinav Haftasi")
            event_type = st.selectbox("Etkinlik Turu", EVENT_TYPES)
            event_date = st.date_input("Tarih*", value=date.today())

        with col2:
            location = st.text_input("Konum", placeholder="Ornek: Ana Kampus, Spor Salonu")
            kademe = st.selectbox("Kademe", KADEMELER)
            end_date = st.date_input("Bitis Tarihi (Opsiyonel)", value=None)

        description = st.text_area("Aciklama", placeholder="Etkinlik ile ilgili detaylar...", height=100)

        # ── TEKRARLAYAN ETKİNLİK ──
        st.markdown("---")
        st.markdown("**Tekrarlayan Etkinlik (Opsiyonel)**")
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            tekrar_tipi = st.selectbox("Tekrar", ["Tekrar Yok", "Haftalik", "2 Haftada Bir", "Aylik"], key="add_tekrar")
        with tc2:
            tekrar_sayisi = st.number_input("Kac Kez Tekrar", min_value=1, max_value=52, value=4, key="add_tekrar_sayi")
        with tc3:
            st.caption("Ornek: 'Haftalik + 12' = 12 hafta boyunca ayni gun")

        submitted = st.form_submit_button("💾 Etkinligi Kaydet", use_container_width=True)

        if submitted:
            if not title:
                st.error("Etkinlik adi zorunludur!")
                return

            # Tekrarlayan tarihleri olustur
            from datetime import timedelta
            tarihler = [event_date]
            if tekrar_tipi == "Haftalik":
                for i in range(1, tekrar_sayisi):
                    tarihler.append(event_date + timedelta(weeks=i))
            elif tekrar_tipi == "2 Haftada Bir":
                for i in range(1, tekrar_sayisi):
                    tarihler.append(event_date + timedelta(weeks=i * 2))
            elif tekrar_tipi == "Aylik":
                for i in range(1, tekrar_sayisi):
                    ay = event_date.month + i
                    yil = event_date.year + (ay - 1) // 12
                    ay = ((ay - 1) % 12) + 1
                    try:
                        tarihler.append(event_date.replace(year=yil, month=ay))
                    except ValueError:
                        # Ay sonu tasma (31 -> 28 gibi)
                        import calendar as _cal
                        son_gun = _cal.monthrange(yil, ay)[1]
                        tarihler.append(event_date.replace(year=yil, month=ay, day=min(event_date.day, son_gun)))

            # Cakisma kontrolu
            cakismalar = []
            for t in tarihler:
                t_str = t.strftime("%Y-%m-%d")
                c = _check_conflicts(events, t_str, kademe)
                for cc in c:
                    cakismalar.append((t_str, cc.get("title", "?"), cc.get("type", "")))

            if cakismalar:
                st.warning(f"Cakisma uyarisi: {len(cakismalar)} etkinlikle cakisma tespit edildi!")
                for t_str, c_title, c_type in cakismalar[:5]:
                    st.caption(f"  {t_str}: **{c_title}** ({c_type})")
                st.info("Etkinlik yine de eklendi. Gerekirse listeden duzenleyebilirsiniz.")

            # Etkinlikleri ekle
            eklenen = 0
            for idx, t in enumerate(tarihler):
                new_event = {
                    "id": f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{idx}",
                    "title": title if len(tarihler) == 1 else f"{title} ({idx + 1}/{len(tarihler)})",
                    "type": event_type,
                    "date": t.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d") if end_date and idx == 0 else None,
                    "location": location,
                    "kademe": kademe,
                    "description": description,
                    "created_at": datetime.now().isoformat(),
                }
                if len(tarihler) > 1:
                    new_event["tekrar_grubu"] = f"tg_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                data.setdefault("events", []).append(new_event)
                eklenen += 1

            save_calendar_data(data)
            if eklenen == 1:
                st.success(f"'{title}' etkinligi basariyla eklendi!")
            else:
                st.success(f"'{title}' — {eklenen} tekrarlayan etkinlik eklendi!")
            st.rerun()


def render_semester_management(data: dict) -> None:
    """Donem yonetimi"""
    st.subheader("📚 Donem Yönetimi")
    
    semesters = data.get("semesters", [])
    
    if semesters:
        for sem in semesters:
            with st.expander(f"📅 {sem.get('name', 'Donem')}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Başlangıç:** {format_date_turkish(sem.get('start_date', ''))}")
                with col2:
                    st.write(f"**Bitis:** {format_date_turkish(sem.get('end_date', ''))}")
                with col3:
                    st.write(f"**Durum:** {'🟢 Aktif' if sem.get('is_active') else '⚪ Pasif'}")
    
    st.divider()
    
    with st.form("add_semester_form"):
        st.markdown("**Yeni Donem Ekle**")
        col1, col2 = st.columns(2)
        
        with col1:
            sem_name = st.text_input("Donem Adi", placeholder="2024-2025 1. Donem")

            start_date = st.date_input("Başlangıç Tarihi")

        
        with col2:
            academic_year = st.text_input("Akademik Yil", placeholder="2024-2025")

            end_date = st.date_input("Bitis Tarihi")

        
        is_active = st.checkbox("Aktif Donem")

        
        if st.form_submit_button("Donemi Kaydet"):
            if sem_name and start_date and end_date:
                new_semester = {
                    "id": f"sem_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": sem_name,
                    "academic_year": academic_year,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "is_active": is_active
                }
                data["semesters"].append(new_semester)
                save_calendar_data(data)
                st.success("Donem eklendi!")
                st.rerun()


def render_upcoming_events(events: list[dict]) -> None:
    """Yaklasan etkinlikler"""
    st.subheader("🔔 Yaklasan Etkinlikler")
    
    today = date.today().strftime("%Y-%m-%d")
    future_events = [e for e in events if e.get("date", "") >= today]
    future_events = sorted(future_events, key=lambda x: x.get("date", ""))[:5]
    
    if not future_events:
        st.info("Yaklasan etkinlik bulunmuyor.")
        return
    
    for event in future_events:
        color = EVENT_COLORS.get(event.get("type", ""), "#607D8B")
        evt_date = event.get("date") or event.get("tarih") or ""
        if not evt_date:
            continue
        try:
            days_left = (datetime.strptime(evt_date, "%Y-%m-%d").date() - date.today()).days
        except (ValueError, TypeError):
            continue
        
        days_text = "Bugün" if days_left == 0 else f"{days_left} gun sonra"
        
        st.markdown(f"""
            <div style='
                display:flex;
                align-items:center;
                padding:12px;
                background:linear-gradient(90deg, {color}22, transparent);
                border-left:4px solid {color};
                border-radius:0 8px 8px 0;
                margin-bottom:8px;
            '>
                <div style='flex:1;'>
                    <strong>{event.get('title', '')}</strong><br>
                    <small style='color:#666;'>{format_date_turkish(event.get('date', ''))}</small>
                </div>
                <div style='
                    background:{color};
                    color:white;
                    padding:4px 12px;
                    border-radius:12px;
                    font-size:0.8rem;
                '>
                    {days_text}
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_statistics(data: dict) -> None:
    """Takvim istatistikleri"""
    events = data.get("events", [])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Toplam Etkinlik", len(events))
    
    with col2:
        today = date.today().strftime("%Y-%m-%d")
        upcoming = len([e for e in events if e.get("date", "") >= today])
        st.metric("🔜 Yaklasan", upcoming)
    
    with col3:
        exams = len([e for e in events if e.get("type") == "Sınav"])
        st.metric("📝 Sınav", exams)
    
    with col4:
        holidays = len([e for e in events if e.get("type") == "Tatil"])
        st.metric("🎉 Tatil", holidays)


# ==================== DASHBOARD ====================

def _cal_stat_row(stats):
    """Dashboard KPI stat kartlari."""
    cols = st.columns(len(stats))
    for i, (label, value, color, icon) in enumerate(stats):
        with cols[i]:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{color}15,{color}08);'
                f'border-radius:12px;padding:8px 12px;text-align:center;border:1px solid {color}30;">'
                f'<div style="font-size:0.85rem;margin-bottom:2px">{icon}</div>'
                f'<div style="font-size:1.35rem;font-weight:800;color:{color};line-height:1.1">{value}</div>'
                f'<div style="font-size:0.65rem;color:#64748b;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:.4px;margin-top:2px">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )


def _render_calendar_dashboard(data: dict, events: list[dict]) -> None:
    """Akademik Takvim Dashboard - ozet gorunum."""
    today_str = date.today().strftime("%Y-%m-%d")
    semesters = data.get("semesters", [])

    # -- KPI Kartlar --
    total_events = len(events)
    exam_count = len([e for e in events if e.get("type") == "Sınav"])
    holiday_count = len([e for e in events if e.get("type") == "Tatil"])
    meeting_count = len([e for e in events if e.get("type") == "Toplanti"])
    active_semesters = len([s for s in semesters if s.get("is_active")])
    future_events = [e for e in events if e.get("date", "") >= today_str]
    future_count = len(future_events)

    _cal_stat_row([
        ("Toplam Etkinlik", total_events, "#2563eb", "\U0001F4C5"),
        ("Sınav Sayısı", exam_count, "#F44336", "\U0001F4DD"),
        ("Tatil Sayısı", holiday_count, "#9C27B0", "\U0001F389"),
        ("Toplanti", meeting_count, "#2196F3", "\U0001F91D"),
        ("Aktif Donem", active_semesters, "#10b981", "\U0001F393"),
        ("Gelecek Etkinlik", future_count, "#FF9800", "\U0001F4C6"),
    ])

    # ── PDF HIZLI İNDİRME (KPI altında, hemen görünür) ──
    _quick_pdf_buttons(events, data, "akt_ust")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # -- 2 Sutunlu Grafikler --
    col_left, col_right = st.columns(2)

    # Sol: Etkinlik Turu Dagilimi (Donut)
    with col_left:
        st.markdown(
            ReportStyler.section_divider_html("Etkinlik Turu Dagilimi", "#2563eb"),
            unsafe_allow_html=True,
        )
        type_counts: dict[str, int] = {}
        for e in events:
            etype = e.get("type", "Diger")
            type_counts[etype] = type_counts.get(etype, 0) + 1

        if type_counts:
            donut_colors = [EVENT_COLORS.get(t, "#607D8B") for t in type_counts]
            donut_data = {k: float(v) for k, v in type_counts.items()}
            st.markdown(
                ReportStyler.donut_chart_svg(donut_data, colors=donut_colors, size=155),
                unsafe_allow_html=True,
            )
        else:
            st.info("Henuz etkinlik bulunmuyor.")

    # Sag: Aylik Etkinlik Dagilimi (Yatay bar)
    with col_right:
        st.markdown(
            ReportStyler.section_divider_html("Aylık Etkinlik Dagilimi", "#10b981"),
            unsafe_allow_html=True,
        )
        month_counts: dict[str, int] = {}
        for e in events:
            d = e.get("date", "")
            if len(d) >= 7:
                try:
                    m_idx = int(d[5:7]) - 1
                    month_name = MONTHS_TR[m_idx]
                    month_counts[month_name] = month_counts.get(month_name, 0) + 1
                except (ValueError, IndexError):
                    pass

        if month_counts:
            # Aylari takvim sirasina gore sirala
            ordered_months: dict[str, float] = {}
            for m in MONTHS_TR:
                if m in month_counts:
                    ordered_months[m] = float(month_counts[m])
            st.markdown(
                ReportStyler.horizontal_bar_html(ordered_months, color="#10b981"),
                unsafe_allow_html=True,
            )
        else:
            st.info("Henuz etkinlik bulunmuyor.")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # -- Yaklasan Etkinlikler --
    st.markdown(
        ReportStyler.section_divider_html("Yaklasan Etkinlikler", "#FF9800"),
        unsafe_allow_html=True,
    )

    upcoming = sorted(future_events, key=lambda x: x.get("date", ""))[:8]

    if not upcoming:
        st.info("Yaklasan etkinlik bulunmuyor.")
    else:
        for event in upcoming:
            color = EVENT_COLORS.get(event.get("type", ""), "#607D8B")
            evt_date = event.get("date", "")
            try:
                days_left = (datetime.strptime(evt_date, "%Y-%m-%d").date() - date.today()).days
            except Exception:
                days_left = 0
            days_text = "Bugün" if days_left == 0 else f"{days_left} gun sonra"

            st.markdown(f"""
                <div style="
                    display:flex;align-items:center;padding:14px 16px;
                    background:linear-gradient(90deg,{color}12,transparent);
                    border-left:4px solid {color};border-radius:0 12px 12px 0;
                    margin-bottom:8px;box-shadow:0 2px 6px rgba(0,0,0,0.04);
                ">
                    <div style="flex:1;">
                        <div style="font-weight:700;font-size:14px;color:#94A3B8;">
                            {event.get('title', '')}
                        </div>
                        <div style="font-size:12px;color:#64748b;margin-top:4px;">
                            {format_date_turkish(evt_date)}
                            &nbsp;|&nbsp;{event.get('type', 'Genel')}
                            &nbsp;|&nbsp;{event.get('kademe', 'Tüm Kademeler')}
                        </div>
                    </div>
                    <div style="
                        background:{color};color:white;padding:5px 14px;
                        border-radius:12px;font-size:12px;font-weight:600;
                        white-space:nowrap;
                    ">
                        {days_text}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ── PDF İNDİRME BUTONLARI ──
    st.markdown("---")
    _quick_pdf_buttons(events, data, "akt_db")


# ==================== AKT RAPORLAR ====================

def _render_akt_raporlar(data: dict, events: list[dict]) -> None:
    """AKT Raporlar - Akademik Takvim raporlari."""
    st.markdown('''<div style="background:linear-gradient(135deg,#ffffff,#e0f2fe);
        color:#0B0F19;padding:18px 24px;border-radius:14px;margin-bottom:16px;border:1px solid #bae6fd;">
        <h3 style="margin:0;font-size:18px;color:#0c4a6e;">📊 AKT Raporlar</h3>
        <p style="margin:4px 0 0 0;opacity:0.7;font-size:13px;color:#475569;">Akademik Takvim Raporlari ve Analiz</p>
    </div>''', unsafe_allow_html=True)

    from datetime import date as _date
    bugun = _date.today()

    toplam = len(events)
    gelecek = sum(1 for e in events if e.get("date", "") >= bugun.isoformat())
    gecmis = toplam - gelecek
    sinav = sum(1 for e in events if e.get("type") == "Sınav")
    tatil = sum(1 for e in events if e.get("type") == "Tatil")

    # KPI
    _cal_stat_row([
        ("Toplam Etkinlik", toplam, "#2563eb", "📅"),
        ("Gelecek", gelecek, "#10b981", "⏳"),
        ("Geçmiş", gecmis, "#64748b", "✅"),
        ("Sınav", sinav, "#ef4444", "📝"),
        ("Tatil", tatil, "#8b5cf6", "🏖"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<h4 style="color:#94A3B8;margin:16px 0 8px;">Etkinlik Turu Dagilimi</h4>', unsafe_allow_html=True)
        type_dist = {}
        for e in events:
            t = e.get("type", "Diger")
            type_dist[t] = type_dist.get(t, 0) + 1
        if type_dist:
            colors = [EVENT_COLORS.get(k, "#64748b") for k in type_dist.keys()]
            st.markdown(ReportStyler.donut_chart_svg(type_dist, colors=colors), unsafe_allow_html=True)
        else:
            st.info("Henuz etkinlik yok.")

    with c2:
        st.markdown('<h4 style="color:#94A3B8;margin:16px 0 8px;">Aylık Etkinlik Sayısı</h4>', unsafe_allow_html=True)
        ay_dist = {}
        for e in events:
            d = e.get("date", "")
            if len(d) >= 7:
                ay = d[:7]  # YYYY-MM
                ay_dist[ay] = ay_dist.get(ay, 0) + 1
        if ay_dist:
            for ay, cnt in sorted(ay_dist.items()):
                st.markdown(ReportStyler.horizontal_bar_html({ay: float(cnt)}, color="#2563eb"), unsafe_allow_html=True)
        else:
            st.info("Ay bazli veri yok.")

    # Kademe dagilimi
    st.markdown('<h4 style="color:#94A3B8;margin:16px 0 8px;">Kademe Bazli Etkinlik</h4>', unsafe_allow_html=True)
    kademe_dist = {}
    for e in events:
        k = e.get("kademe", "Tüm Kademeler")
        kademe_dist[k] = kademe_dist.get(k, 0) + 1
    if kademe_dist:
        st.markdown(ReportStyler.donut_chart_svg(kademe_dist, colors=["#2563eb", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]), unsafe_allow_html=True)

    # AI Onerileri
    st.markdown('''<div style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);
        border-radius:12px;padding:16px;margin:16px 0;border:1px solid #c4b5fd;">
        <h4 style="margin:0 0 10px 0;color:#7c3aed;">💡 AI Onerileri</h4>''', unsafe_allow_html=True)

    recs = []
    if sinav > toplam * 0.4:
        recs.append("Sınav yogunlugu yuksek. Öğrenci motivasyonu için sosyal etkinlik dengesini gozden gecirin.")
    if gelecek < 5:
        recs.append("Yaklasan etkinlik sayisi az. Planlama takvimini guncelleyin.")
    if tatil == 0:
        recs.append("Tatil planlamasi yapilmamis. Resmi tatilleri eklemeyi unutmayin.")
    if not recs:
        recs.append("Akademik takvim dengeli gorunuyor. Duzgun ilerliyorsunuz.")

    for r in recs:
        st.markdown(f'<p style="margin:4px 0;color:#4c1d95;">• {r}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Detay tablosu
    st.markdown('<h4 style="color:#94A3B8;margin:16px 0 8px;">Etkinlik Detay Tablosu</h4>', unsafe_allow_html=True)
    if events:
        import pandas as _pd
        rows = []
        for e in events:
            rows.append({
                "Tarih": e.get("date", ""),
                "Başlık": e.get("title", ""),
                "Tur": e.get("type", ""),
                "Kademe": e.get("kademe", ""),
                "Lokasyon": e.get("location", ""),
            })
        df = _pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ---- Performans Karsilastirma ----
    try:
        from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                         generate_module_pdf, render_pdf_download_button,
                                         render_report_kunye_html, ReportStyler)
        from datetime import timedelta as _td_akt

        _now_akt = bugun
        _cur_month_akt = _now_akt.strftime("%Y-%m")
        _prev_month_akt = (_now_akt.replace(day=1) - _td_akt(days=1)).strftime("%Y-%m")

        st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

        # Monthly event count
        cur_events = sum(1 for e in events if str(e.get("date", "")).startswith(_cur_month_akt))
        prev_events = sum(1 for e in events if str(e.get("date", "")).startswith(_prev_month_akt))

        # Monthly sinav count
        cur_sinav = sum(1 for e in events if str(e.get("date", "")).startswith(_cur_month_akt) and e.get("type") == "Sınav")
        prev_sinav = sum(1 for e in events if str(e.get("date", "")).startswith(_prev_month_akt) and e.get("type") == "Sınav")

        # Monthly sosyal etkinlik count
        cur_sosyal = sum(1 for e in events if str(e.get("date", "")).startswith(_cur_month_akt) and e.get("type") not in ("Sınav", "Tatil"))
        prev_sosyal = sum(1 for e in events if str(e.get("date", "")).startswith(_prev_month_akt) and e.get("type") not in ("Sınav", "Tatil"))

        akt_comparisons = [
            {"label": "Toplam Etkinlik", "current": cur_events, "previous": prev_events},
            {"label": "Sınav Sayısı", "current": cur_sinav, "previous": prev_sinav},
            {"label": "Sosyal Etkinlik", "current": cur_sosyal, "previous": prev_sosyal},
        ]
        st.markdown(period_comparison_row_html(akt_comparisons), unsafe_allow_html=True)

        # ---- Enhanced AI Onerileri ----
        akt_insights = []
        if toplam > 0 and sinav / toplam > 0.5:
            akt_insights.append({
                "icon": "📝", "title": "Sınav Yogunlugu Uyarisi",
                "text": f"Etkinliklerin %{sinav/toplam*100:.0f}'i sinavlardan olusuyor. Sosyal ve kulturel etkinliklerle dengelemeyi dusunun.",
                "color": "#ef4444"
            })
        if gelecek < 3:
            akt_insights.append({
                "icon": "📅", "title": "Yaklasan Etkinlik Azligi",
                "text": f"Sadece {gelecek} yaklasan etkinlik var. Planlama takvimini guncelleyerek onumuzdeki donemi sekillendin.",
                "color": "#f59e0b"
            })
        if tatil == 0:
            akt_insights.append({
                "icon": "🏖", "title": "Tatil Planlamasi Eksik",
                "text": "Henuz tatil planlanmamis. Resmi tatilleri, yariyil tatillerini ve ozel gunleri eklemeyi unutmayin.",
                "color": "#8b5cf6"
            })

        # Kademe coverage check
        kademeler_used = set(e.get("kademe", "") for e in events if e.get("kademe"))
        if len(kademeler_used) < 2 and toplam > 5:
            akt_insights.append({
                "icon": "🎓", "title": "Kademe Cesitliligi Yetersiz",
                "text": f"Etkinlikler yalnizca {len(kademeler_used)} kademeyi kapsiyor. Tüm kademelere yonelik etkinlik planlayarak kapsami genisletin.",
                "color": "#2563eb"
            })

        akt_insights.append({
            "icon": "🔄", "title": "Donemsel Değerlendirme",
            "text": "Her donem sonunda takvim gerceklesme oranini analiz edin. Ertelenen etkinlikler için telafi plani olusturun.",
            "color": "#0d9488"
        })

        if not akt_insights:
            akt_insights.append({
                "icon": "✅", "title": "Takvim Dengeli",
                "text": "Akademik takvim dengeli gorunuyor. Planlamayi surdurun.",
                "color": "#10b981"
            })

        st.markdown(ai_recommendations_html(akt_insights), unsafe_allow_html=True)

        # ---- Kurumsal Kunye ----
        st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

        # ---- PDF Export ----
        st.markdown(ReportStyler.section_divider_html("PDF Rapor", "#1e40af"), unsafe_allow_html=True)
        if st.button("📥 AKT Raporu (PDF)", key="akt_pdf_btn", use_container_width=True):
            akt_pdf_sections = [
                {
                    "title": "Akademik Takvim Özet",
                    "metrics": [
                        ("Toplam", toplam, "#2563eb"),
                        ("Gelecek", gelecek, "#10b981"),
                        ("Sınav", sinav, "#ef4444"),
                        ("Tatil", tatil, "#8b5cf6"),
                    ],
                    "text": f"Toplam {toplam} etkinlik, {gelecek} gelecek, {gecmis} gecmis.",
                },
                {
                    "title": "Etkinlik Turu Dagilimi",
                    "donut_data": {k: float(v) for k, v in type_dist.items()} if type_dist else {},
                    "donut_title": "Tur Dagilimi",
                },
            ]
            if events:
                akt_pdf_sections.append({
                    "title": "Etkinlik Listesi",
                    "table": df,
                    "table_color": "#2563eb",
                })
            akt_pdf_bytes = generate_module_pdf("AKT Raporu", akt_pdf_sections)
            render_pdf_download_button(akt_pdf_bytes, "akt_raporu.pdf", "AKT Raporu", "akt_dl")
    except Exception as _akt_err:
        st.caption(f"Rapor bilesenleri yuklenemedi: {_akt_err}")

    # ── YILLIK / AYLIK ÇALIŞMA PLANI PDF ──
    st.markdown("---")
    styled_section("Yillik Calisma Plani PDF", "#1a237e")
    _quick_pdf_buttons(events, data, "akt_rap", bugun_override=bugun)


# ==================== MAIN RENDER ====================


def render_academic_calendar() -> None:
    """Ana render fonksiyonu"""
    styled_header("Akademik Takvim", "Eğitim dönemi, sınav tarihleri, tatiller ve önemli etkinliklerin yönetimi", icon="📅")
    
    # Veri yukle
    data = load_calendar_data()
    events = data.get("events", [])
    
    # Silme islemi
    if st.session_state.get("event_to_delete"):
        event_id = st.session_state["event_to_delete"]
        data["events"] = [e for e in events if e.get("id") != event_id]
        save_calendar_data(data)
        st.session_state["event_to_delete"] = None
        st.rerun()
    
    # Istatistikler
    render_statistics(data)
    st.divider()
    
    # Tabs
    render_smarti_welcome("academic_calendar")
    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("academic_calendar_egitim_yili")
    # -- Tab Gruplama (16 tab -> 3 grup) --
    _GRP_TABS = {
        "📋 Grup A": [("📊 Dashboard", 0), ("📆 Takvim Görünümu", 1), ("📋 Liste Görünümu", 2), ("➕ Etkinlik Ekle", 3), ("📚 Donem Yönetimi", 4), ("📈 AKT Raporlar", 5), ("🌐 Süper Takvim", 6)],
        "📊 Grup B": [("🧠 AI Planlama", 7), ("🎛️ Komuta", 8), ("📑 Yıllık Plan", 9), ("📤 Toplu Yükle", 10), ("🏛️ MEB Takvim", 11), ("📋 Durum Takip", 12), ("📊 Yıl Karşılaştır", 13)],
        "🔧 Grup C": [("🎓 Paylaş", 14), ("🤖 Smarti", 15)],
    }
    _sg_grp_3561 = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg_grp_3561")
    _gt_grp_3561 = _GRP_TABS[_sg_grp_3561]
    _tn_grp_3561 = [t[0] for t in _gt_grp_3561]
    _ti_grp_3561 = [t[1] for t in _gt_grp_3561]
    _tabs_grp_3561 = st.tabs(_tn_grp_3561)
    _tmap_grp_3561 = {i: t for i, t in zip(_ti_grp_3561, _tabs_grp_3561)}
    tab_dashboard = _tmap_grp_3561.get(0)
    tab_calendar = _tmap_grp_3561.get(1)
    tab_list = _tmap_grp_3561.get(2)
    tab_add = _tmap_grp_3561.get(3)
    tab_semesters = _tmap_grp_3561.get(4)
    tab_akt_raporlar = _tmap_grp_3561.get(5)
    tab_super = _tmap_grp_3561.get(6)
    tab_planlama = _tmap_grp_3561.get(7)
    tab_komuta = _tmap_grp_3561.get(8)
    tab_yillik = _tmap_grp_3561.get(9)
    tab_toplu = _tmap_grp_3561.get(10)
    tab_meb = _tmap_grp_3561.get(11)
    tab_durum = _tmap_grp_3561.get(12)
    tab_karsilastir = _tmap_grp_3561.get(13)
    tab_paylas = _tmap_grp_3561.get(14)
    tab_smarti = _tmap_grp_3561.get(15)
    
    # Sidebar - Ay/Yil secimi
    with st.sidebar:
        st.subheader("📅 Takvim Navigasyonu")
        current_year = st.number_input("Yil", min_value=2020, max_value=2030, value=date.today().year)

        current_month = st.selectbox("Ay", MONTHS_TR, index=date.today().month - 1)

        month_index = MONTHS_TR.index(current_month) + 1
        
        st.divider()
        render_upcoming_events(events)
    
    if tab_dashboard is not None:
      with tab_dashboard:
        _render_calendar_dashboard(data, events)

    if tab_calendar is not None:
      with tab_calendar:
        st.subheader(f"📆 {current_month} {current_year}")
        render_calendar_grid(current_year, month_index, events)
        
        # Etkinlik turu renk aciklamasi
        st.divider()
        st.caption("Etkinlik Turleri:")
        color_cols = st.columns(4)
        color_items = list(EVENT_COLORS.items())
        for i, (etype, color) in enumerate(color_items):
            with color_cols[i % 4]:
                st.markdown(f"<span style='display:inline-block;width:12px;height:12px;background:{color};border-radius:50%;margin-right:6px;'></span>{etype}", unsafe_allow_html=True)
    
    if tab_list is not None:
      with tab_list:
        st.subheader(f"📋 {current_month} {current_year} Etkinlikleri")
        render_event_list(events, current_year, month_index, data)
    
    if tab_add is not None:
      with tab_add:
        render_add_event_form(data)
    
    if tab_semesters is not None:
      with tab_semesters:
        render_semester_management(data)

    if tab_akt_raporlar is not None:
      with tab_akt_raporlar:
        _render_akt_raporlar(data, events)

    # ZIRVE: Birlesik Super Takvim
    if tab_super is not None:
      with tab_super:
        try:
            from views._akt_zirve import render_super_takvim
            render_super_takvim(events, current_year, month_index)
        except Exception as _e:
            st.error(f"Super Takvim yuklenemedi: {_e}")

    # ZIRVE: AI Planlama Asistani
    if tab_planlama is not None:
      with tab_planlama:
        try:
            from views._akt_zirve import render_ai_planlama
            render_ai_planlama(events)
        except Exception as _e:
            st.error(f"AI Planlama yuklenemedi: {_e}")

    # ZIRVE: Komuta + Geri Sayim
    if tab_komuta is not None:
      with tab_komuta:
        try:
            from views._akt_zirve import render_takvim_komuta
            render_takvim_komuta(events)
        except Exception as _e:
            st.error(f"Takvim Komuta yuklenemedi: {_e}")

    # YILLIK CALISMA PLANI + PDF
    if tab_yillik is not None:
      with tab_yillik:
        try:
            from views._akt_yillik_plan import render_yillik_calisma_plani
            render_yillik_calisma_plani(data, events)
        except Exception as _e:
            st.error(f"Yillik Plan yuklenemedi: {_e}")

    # TOPLU YUKLEME
    if tab_toplu is not None:
      with tab_toplu:
        try:
            from views._akt_tamamlayici import render_toplu_yukleme
            render_toplu_yukleme(data)
        except Exception as _e:
            st.error(f"Toplu Yukleme yuklenemedi: {_e}")

    # MEB TAKVIM
    if tab_meb is not None:
      with tab_meb:
        try:
            from views._akt_tamamlayici import render_meb_takvim
            render_meb_takvim(data)
        except Exception as _e:
            st.error(f"MEB Takvim yuklenemedi: {_e}")

    # DURUM TAKIP
    if tab_durum is not None:
      with tab_durum:
        try:
            from views._akt_tamamlayici import render_durum_takip
            render_durum_takip(data, events)
        except Exception as _e:
            st.error(f"Durum Takip yuklenemedi: {_e}")

    # YIL KARSILASTIR
    if tab_karsilastir is not None:
      with tab_karsilastir:
        try:
            from views._akt_tamamlayici import render_yil_karsilastir
            render_yil_karsilastir(events)
        except Exception as _e:
            st.error(f"Yil Karsilastir yuklenemedi: {_e}")

    # PAYLAS
    if tab_paylas is not None:
      with tab_paylas:
        try:
            from views._akt_tamamlayici import render_takvim_paylas
            render_takvim_paylas(data, events)
        except Exception as _e:
            st.error(f"Takvim Paylas yuklenemedi: {_e}")

    if tab_smarti is not None:
      with tab_smarti:
        def _akt_smarti_context() -> str:
            try:
                cal_data = load_calendar_data()
                all_events = cal_data.get("events", [])
                total = len(all_events)
                type_counts = {}
                for ev in all_events:
                    t = ev.get("type", "Diger")
                    type_counts[t] = type_counts.get(t, 0) + 1
                type_str = ", ".join(f"{k}: {v}" for k, v in type_counts.items())
                return f"Toplam etkinlik: {total}. Etkinlik turleri: {type_str}."
            except Exception:
                return "Takvim verisi yuklenemedi."
        render_smarti_chat("academic_calendar", _akt_smarti_context)
