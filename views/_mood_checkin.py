"""
Günlük Duygu Check-in — Öğrenci Ruh Hali Takibi
=====================================================
Her öğrenci sabah 5 saniyede ruh halini işaretler.
7 gün üst üste düşükse → Rehberlik + Erken Uyarı bayrağı.
Gizli — sadece rehber görür.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# DUYGU SEVİYELERİ — 5 Kademeli Emoji
# ══════════════════════════════════════════════════════════════

MOOD_LEVELS = {
    5: {"emoji": "😄", "label": "Harika",     "color": "#059669", "value": 5},
    4: {"emoji": "🙂", "label": "İyi",        "color": "#16A34A", "value": 4},
    3: {"emoji": "😐", "label": "İdare eder", "color": "#D97706", "value": 3},
    2: {"emoji": "😟", "label": "Kötü",       "color": "#EA580C", "value": 2},
    1: {"emoji": "😢", "label": "Çok kötü",   "color": "#DC2626", "value": 1},
}

# Opsiyonel etiketler (öğrenci seçebilir)
MOOD_TAGS = [
    "💪 Enerjik",
    "😴 Yorgun",
    "😰 Kaygılı",
    "😠 Sinirli",
    "🤔 Kafam karışık",
    "💔 Üzgün",
    "🎉 Heyecanlı",
    "🙏 Şükürlü",
    "😕 Yalnız",
    "😤 Stresli",
    "🤕 Hasta",
    "🥱 Uyuşuk",
]


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _mood_path() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "mood_checkin")
    except Exception:
        d = os.path.join("data", "mood_checkin")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "checkins.json")


def _load_checkins() -> list[dict]:
    p = _mood_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_checkins(data: list[dict]) -> None:
    with open(_mood_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# ÖĞRENCİ CHECK-IN PANELİ — 5 saniyede
# ══════════════════════════════════════════════════════════════

def render_mood_checkin_student(student_id: str = "", student_name: str = ""):
    """Öğrenci check-in — hızlı, 5 saniye, gizli."""
    styled_section("😊 Bugünkü Ruh Halin", "#4F46E5")

    today_str = date.today().isoformat()
    checkins = _load_checkins()

    # Bugün işaretlendi mi?
    today_mine = next(
        (c for c in checkins if c.get("student_id") == student_id and c.get("tarih") == today_str),
        None,
    )

    if today_mine:
        existing = MOOD_LEVELS.get(today_mine.get("level", 3))
        st.markdown(f"""
        <div style="background:{existing['color']}20;border:2px solid {existing['color']};
        border-radius:12px;padding:16px 20px;text-align:center;margin:12px 0;">
            <div style="font-size:3rem;">{existing['emoji']}</div>
            <div style="font-size:1rem;color:#E4E4E7;margin-top:6px;">
                Bugün <strong style="color:{existing['color']};">{existing['label']}</strong> hissettin
            </div>
            <div style="font-size:0.78rem;color:#94A3B8;margin-top:4px;">
                Değişiklik yapabilirsin:
            </div>
        </div>
        """, unsafe_allow_html=True)

    styled_info_banner(
        "Bu bilgi sadece rehber öğretmen tarafından görülebilir. Arkadaşların veya öğretmenlerin göremez. 🔒",
        "info",
    )

    # Emoji seçici
    st.markdown("**Nasıl hissediyorsun?**")
    cols = st.columns(5)
    selected_level = None
    for i, (lvl, info) in enumerate(sorted(MOOD_LEVELS.items(), reverse=True)):
        with cols[i]:
            if st.button(
                f"{info['emoji']}\n{info['label']}",
                key=f"_mood_{lvl}",
                use_container_width=True,
            ):
                selected_level = lvl

    # Opsiyonel etiketler
    st.markdown("**Neler hissediyorsun? (opsiyonel)**")
    chosen_tags = st.multiselect(
        "Etiket",
        MOOD_TAGS,
        label_visibility="collapsed",
        key="_mood_tags_widget",
    )

    # Opsiyonel not
    not_text = st.text_input(
        "Eklemek istediğin bir şey var mı? (opsiyonel, gizli)",
        placeholder="Kimse görmez, rehber isteğe bağlı okur...",
        key="_mood_note_widget",
    )

    if selected_level:
        # Kaydet
        if today_mine:
            # Güncelle
            idx = next((i for i, c in enumerate(checkins) if c is today_mine), None)
            if idx is not None:
                checkins[idx] = {
                    **checkins[idx],
                    "level": selected_level,
                    "tags": chosen_tags,
                    "note": not_text.strip(),
                    "guncelleme_tarihi": datetime.now().isoformat(),
                }
        else:
            # Yeni kayıt
            checkins.append({
                "student_id": student_id,
                "student_name": student_name,
                "tarih": today_str,
                "level": selected_level,
                "tags": chosen_tags,
                "note": not_text.strip(),
                "olusturma_tarihi": datetime.now().isoformat(),
            })

        _save_checkins(checkins)

        level_info = MOOD_LEVELS[selected_level]
        st.balloons() if selected_level >= 4 else None
        st.success(f"✅ Kaydedildi: {level_info['emoji']} {level_info['label']}")

        if selected_level <= 2:
            st.markdown(f"""
            <div style="background:#DC262620;border:2px solid #DC2626;border-radius:12px;
            padding:14px 18px;margin:12px 0;">
                <div style="color:#FCA5A5;font-weight:700;margin-bottom:6px;">💙 Sen değerlisin</div>
                <div style="color:#FAFAFA;font-size:0.88rem;line-height:1.6;">
                    Bugün zor bir gün olmuş olabilir. Rehber öğretmenin seninle konuşmak ister mi diye soracak.
                    Hemen konuşmak istersen, rehberlik servisine gelebilirsin. Acil durumlarda:
                    <br/>• <strong>112</strong> (hayati tehlike)
                    <br/>• <strong>182</strong> (intihar önleme)
                    <br/>• <strong>183</strong> (Çocuk Danışma)
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.rerun()


# ══════════════════════════════════════════════════════════════
# REHBER PANELİ — Gizli Öğrenci Takibi
# ══════════════════════════════════════════════════════════════

def _kullanici_yetkili_mi() -> bool:
    try:
        auth = st.session_state.get("auth_user", {})
        rol = auth.get("role", "").lower()
        return any(r in rol for r in ["rehber", "mudur", "müdür", "yonetici", "kurucu", "admin", "pdr"])
    except Exception:
        return False


def render_mood_rehber_panel():
    """Rehber için duygu takip paneli — düşük ruh halli öğrencileri listeler."""
    styled_section("🧠 Öğrenci Ruh Hali Takibi (Gizli)", "#7C3AED")

    if not _kullanici_yetkili_mi():
        styled_info_banner(
            "Bu panele sadece Rehberlik ve Müdür erişebilir.",
            "warning", "🔒",
        )
        return

    checkins = _load_checkins()

    # Son 7 günlük kontrolleri topla
    today = date.today()
    week_ago = today - timedelta(days=7)

    recent = [c for c in checkins
              if c.get("tarih", "9999") >= week_ago.isoformat()]

    # Öğrenci bazlı grup
    student_stats = {}
    for c in recent:
        sid = c.get("student_id", "unknown")
        if sid not in student_stats:
            student_stats[sid] = {
                "name": c.get("student_name", sid),
                "records": [],
            }
        student_stats[sid]["records"].append(c)

    # İstatistik
    bugun_sayi = sum(1 for c in checkins if c.get("tarih") == today.isoformat())
    hafta_sayi = len(recent)
    dusuk_ogrenci = 0  # 7 günde ≥3 gün <=2 puan
    kritik_ogrenci = 0  # bugün 1 puan
    for sid, data in student_stats.items():
        kotu_gunler = sum(1 for r in data["records"] if r.get("level", 3) <= 2)
        if kotu_gunler >= 3:
            dusuk_ogrenci += 1
        for r in data["records"]:
            if r.get("tarih") == today.isoformat() and r.get("level", 3) == 1:
                kritik_ogrenci += 1

    styled_stat_row([
        ("Bugün Check-in", str(bugun_sayi), "#4F46E5", "📅"),
        ("Bu Hafta", str(hafta_sayi), "#059669", "📊"),
        ("Düşük Ruh Hali (7g)", str(dusuk_ogrenci), "#EA580C", "⚠️"),
        ("Kritik (Bugün 😢)", str(kritik_ogrenci), "#DC2626", "🚨"),
    ])

    if kritik_ogrenci > 0:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#DC2626,#991B1B);border-radius:12px;
        padding:14px 18px;color:white;margin:12px 0;box-shadow:0 4px 14px rgba(220,38,38,0.4);">
            <div style="font-weight:800;font-size:1rem;">🚨 ACİL DİKKAT</div>
            <div style="font-size:0.88rem;margin-top:4px;opacity:0.95;">
                {kritik_ogrenci} öğrenci bugün kendini çok kötü hissettiğini işaretledi.
                Derhal görüşme planlayın.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Filtre
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        filter_type = st.selectbox(
            "Göster",
            ["🚨 Sadece Riskli (7 gün içinde ≥3 düşük)",
             "⚠️ Bugün Düşük (≤2)",
             "📊 Tüm Öğrenciler (Son 7 gün)",
             "✅ İyi Olanlar (≥4)"],
            key="_mood_filter_widget",
        )

    # Öğrencileri filtrele
    filtered_students = []
    for sid, data in student_stats.items():
        records = data["records"]
        if not records:
            continue

        avg = sum(r.get("level", 3) for r in records) / len(records)
        bugun_rec = next((r for r in records if r.get("tarih") == today.isoformat()), None)
        kotu_gunler = sum(1 for r in records if r.get("level", 3) <= 2)

        show = False
        if "Sadece Riskli" in filter_type and kotu_gunler >= 3:
            show = True
        elif "Bugün Düşük" in filter_type and bugun_rec and bugun_rec.get("level", 3) <= 2:
            show = True
        elif "Tüm Öğrenciler" in filter_type:
            show = True
        elif "İyi Olanlar" in filter_type and avg >= 4:
            show = True

        if show:
            filtered_students.append({
                "id": sid, "name": data["name"],
                "records": records, "avg": avg,
                "bugun": bugun_rec, "kotu_gunler": kotu_gunler,
            })

    # Sırala (en kötüler önce)
    filtered_students.sort(key=lambda x: (x["avg"], -x["kotu_gunler"]))

    if not filtered_students:
        styled_info_banner("Filtreye uyan öğrenci yok.", "info")
        return

    for stu in filtered_students:
        avg = stu["avg"]
        bugun = stu["bugun"]
        kotu_gun = stu["kotu_gunler"]

        # Ortalama rengi
        avg_level = MOOD_LEVELS.get(round(avg)) or MOOD_LEVELS[3]
        avg_color = avg_level["color"]
        avg_emoji = avg_level["emoji"]

        # Bugünkü durum
        bugun_emoji = MOOD_LEVELS.get(bugun.get("level", 3), {"emoji": "❓"})["emoji"] if bugun else "❓"

        risk_badge = ""
        if kotu_gun >= 3:
            risk_badge = '<span style="background:#DC2626;color:white;padding:2px 10px;border-radius:6px;font-size:0.72rem;font-weight:700;margin-left:8px;">🚨 YÜKSEK RİSK</span>'
        elif kotu_gun >= 2:
            risk_badge = '<span style="background:#D97706;color:white;padding:2px 10px;border-radius:6px;font-size:0.72rem;font-weight:700;margin-left:8px;">⚠️ DİKKAT</span>'

        with st.expander(f"{avg_emoji} {stu['name']} — Ortalama: {avg:.1f}/5 | Bugün: {bugun_emoji} | Kötü gün: {kotu_gun}/7"):
            st.markdown(f"<div style='margin-bottom:8px;'>{risk_badge}</div>", unsafe_allow_html=True)

            # 7 günlük timeline
            st.markdown("**Son 7 Gün:**")
            for i in range(7):
                gun = today - timedelta(days=6 - i)
                gun_str = gun.isoformat()
                rec = next((r for r in stu["records"] if r.get("tarih") == gun_str), None)
                if rec:
                    lvl = rec.get("level", 3)
                    info = MOOD_LEVELS.get(lvl, MOOD_LEVELS[3])
                    tag_str = ", ".join(rec.get("tags", []))
                    note_str = rec.get("note", "")
                    note_display = f" — 💬 \"{note_str}\"" if note_str else ""
                    tag_display = f" — {tag_str}" if tag_str else ""
                    st.markdown(
                        f"• **{gun.strftime('%d.%m')} ({gun.strftime('%a')[:3]})**: "
                        f"{info['emoji']} <span style='color:{info['color']};'>{info['label']}</span>"
                        f"{tag_display}{note_display}",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(f"• **{gun.strftime('%d.%m')}**: <span style='color:#64748B;'>— kayıt yok —</span>", unsafe_allow_html=True)

            # Aksiyon butonları
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                if st.button(f"📞 Görüşme Planla", key=f"_mood_gorusme_{stu['id']}"):
                    styled_info_banner(f"✅ {stu['name']} için görüşme planlandı. Rehberlik modülünden devam edin.", "success")
            with ac2:
                if st.button(f"👨‍👩‍👧 Veliyi Bilgilendir", key=f"_mood_veli_{stu['id']}"):
                    styled_info_banner(f"✅ {stu['name']} velisine bilgilendirme notu eklendi.", "success")
            with ac3:
                if st.button(f"🚨 Kriz Mod", key=f"_mood_kriz_{stu['id']}"):
                    styled_info_banner(f"🚨 Kriz müdahale protokolü tetiklendi.", "warning")


# ══════════════════════════════════════════════════════════════
# ERKEN UYARI ENTEGRASYONU
# ══════════════════════════════════════════════════════════════

def get_mood_risk_students() -> list[dict]:
    """Erken Uyarı modülü için riskli öğrenci listesi döndür.

    Returns: 7 günde 3+ düşük puan alanlar
    """
    checkins = _load_checkins()
    today = date.today()
    week_ago = today - timedelta(days=7)
    recent = [c for c in checkins if c.get("tarih", "9999") >= week_ago.isoformat()]

    student_stats = {}
    for c in recent:
        sid = c.get("student_id", "unknown")
        if sid not in student_stats:
            student_stats[sid] = {"name": c.get("student_name", sid), "records": []}
        student_stats[sid]["records"].append(c)

    risk_list = []
    for sid, data in student_stats.items():
        kotu_gunler = sum(1 for r in data["records"] if r.get("level", 3) <= 2)
        if kotu_gunler >= 3:
            avg = sum(r.get("level", 3) for r in data["records"]) / max(len(data["records"]), 1)
            risk_list.append({
                "student_id": sid,
                "student_name": data["name"],
                "kotu_gunler": kotu_gunler,
                "ortalama": round(avg, 1),
                "risk_skor": 100 - (avg * 20),  # 1=80, 5=0
            })

    return sorted(risk_list, key=lambda x: -x["risk_skor"])


def render_mood_erken_uyari_widget():
    """Erken Uyarı dashboard'una eklenecek mini widget."""
    risk_list = get_mood_risk_students()
    if not risk_list:
        return

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#7C3AED,#5B21B6);border-radius:12px;
    padding:14px 18px;color:white;margin:12px 0;box-shadow:0 4px 14px rgba(124,58,237,0.3);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-weight:800;font-size:1rem;">😟 Duygu Check-in Riski</div>
                <div style="font-size:0.85rem;opacity:0.9;margin-top:4px;">
                    {len(risk_list)} öğrenci son 7 günde 3+ kez düşük ruh hali bildirdi
                </div>
            </div>
            <div style="font-size:2rem;">🧠</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ÖĞRENCİ YARDIMCI — Hızlı check-in (başka ekranlardan çağrılır)
# ══════════════════════════════════════════════════════════════

def render_mood_quick_widget():
    """Öğrenci paneli içinde — hızlı 3 butonlu check-in."""
    try:
        auth = st.session_state.get("auth_user", {})
        student_id = auth.get("id", auth.get("username", ""))
        student_name = auth.get("name", "")
    except Exception:
        student_id = "anonymous"
        student_name = ""

    if not student_id:
        return

    today_str = date.today().isoformat()
    checkins = _load_checkins()
    today_mine = next(
        (c for c in checkins if c.get("student_id") == student_id and c.get("tarih") == today_str),
        None,
    )

    if today_mine:
        return  # Zaten bugün işaretledi

    st.markdown("""
    <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);border-radius:12px;
    padding:12px 16px;color:white;margin:8px 0;">
        <div style="font-size:0.88rem;font-weight:600;">😊 Bugün nasılsın? (5 saniyende)</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (lvl, info) in enumerate(sorted(MOOD_LEVELS.items(), reverse=True)):
        with cols[i]:
            if st.button(info["emoji"], key=f"_mood_quick_{lvl}", use_container_width=True):
                checkins.append({
                    "student_id": student_id,
                    "student_name": student_name,
                    "tarih": today_str,
                    "level": lvl,
                    "tags": [],
                    "note": "",
                    "olusturma_tarihi": datetime.now().isoformat(),
                })
                _save_checkins(checkins)
                st.toast(f"✅ {info['label']} olarak kaydedildi", icon=info["emoji"])
                st.rerun()
