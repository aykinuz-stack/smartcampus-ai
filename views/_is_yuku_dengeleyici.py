"""
Öğretmen İş Yükü Dengeleyici
====================================
AI haftalık analiz — her öğretmen için ders, toplantı, nöbet, ödev kontrol yükünü hesaplar.
Burnout önler, eşitsizlik tespit eder, öneri verir.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# YÜK TİPLERİ & AĞIRLIKLARI (saat bazlı)
# ══════════════════════════════════════════════════════════════

YUK_TIPLERI = {
    "ders_saati":      {"ad": "Ders Saati", "birim_yuk": 1.0, "ikon": "📚"},
    "odev_kontrol":    {"ad": "Ödev Kontrol", "birim_yuk": 0.3, "ikon": "📝"},  # saat başına
    "sinav_hazirla":   {"ad": "Sınav Hazırlama", "birim_yuk": 2.0, "ikon": "📋"},
    "sinav_okuma":     {"ad": "Sınav Okuma", "birim_yuk": 0.15, "ikon": "✅"},  # kağıt başına
    "toplanti":        {"ad": "Toplantı", "birim_yuk": 1.0, "ikon": "🤝"},
    "nobet":           {"ad": "Nöbet", "birim_yuk": 0.5, "ikon": "🛡️"},
    "veli_gorusme":    {"ad": "Veli Görüşmesi", "birim_yuk": 0.5, "ikon": "👨‍👩‍👧"},
    "etut":            {"ad": "Etüt", "birim_yuk": 1.0, "ikon": "📖"},
    "rehberlik":       {"ad": "Rehberlik Desteği", "birim_yuk": 0.3, "ikon": "🧠"},
    "idari":           {"ad": "İdari İşler", "birim_yuk": 0.3, "ikon": "📋"},
}

# Eşikler
HAFTALIK_IDEAL_SAAT = 40  # Haftalık ideal toplam yük
HAFTALIK_DIKKAT_SAAT = 50  # Bu üstü dikkat
HAFTALIK_BURNOUT_SAAT = 60  # Bu üstü burnout riski


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _yuk_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "is_yuku")
    except Exception:
        d = os.path.join("data", "is_yuku")
    os.makedirs(d, exist_ok=True)
    return d


def _yuk_path() -> str:
    return os.path.join(_yuk_dir(), "yukler.json")


def _load_yukler() -> list[dict]:
    p = _yuk_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_yukler(data: list[dict]) -> None:
    with open(_yuk_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# ÖĞRETMEN YÜKÜ HESAPLAMA
# ══════════════════════════════════════════════════════════════

def calculate_teacher_load(teacher_id: str, hafta_baslangic: date = None) -> dict:
    """Bir öğretmenin haftalık yükünü hesapla — akademik sistemden çek."""
    if hafta_baslangic is None:
        bugun = date.today()
        hafta_baslangic = bugun - timedelta(days=bugun.weekday())

    hafta_bitis = hafta_baslangic + timedelta(days=6)

    yuk = {
        "teacher_id": teacher_id,
        "hafta_baslangic": hafta_baslangic.isoformat(),
        "hafta_bitis": hafta_bitis.isoformat(),
        "kalemler": {},
        "toplam_saat": 0.0,
    }

    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()

        # Ders programı
        try:
            schedules = ak.get_schedules() if hasattr(ak, 'get_schedules') else []
            ders_saat = sum(1 for s in schedules if str(
                s.teacher_id if hasattr(s, 'teacher_id') else s.get('teacher_id', '')
            ) == str(teacher_id))
            yuk["kalemler"]["ders_saati"] = ders_saat * YUK_TIPLERI["ders_saati"]["birim_yuk"]
        except Exception:
            yuk["kalemler"]["ders_saati"] = 0

        # Ödev sayısı (oluşturulan)
        try:
            odevler = ak.get_odevler() if hasattr(ak, 'get_odevler') else []
            odev_count = sum(1 for o in odevler if str(
                o.teacher_id if hasattr(o, 'teacher_id') else o.get('teacher_id', '')
            ) == str(teacher_id))
            yuk["kalemler"]["odev_kontrol"] = odev_count * YUK_TIPLERI["odev_kontrol"]["birim_yuk"]
        except Exception:
            yuk["kalemler"]["odev_kontrol"] = 0
    except Exception:
        pass

    # Manuel kayıtlı yükler
    yukler = _load_yukler()
    manuel = [y for y in yukler if y.get("teacher_id") == str(teacher_id)
              and y.get("hafta_baslangic") == hafta_baslangic.isoformat()]

    for m in manuel:
        for k, v in m.get("kalemler", {}).items():
            yuk["kalemler"][k] = yuk["kalemler"].get(k, 0) + v

    # Toplam
    yuk["toplam_saat"] = round(sum(yuk["kalemler"].values()), 1)

    # Durum
    if yuk["toplam_saat"] >= HAFTALIK_BURNOUT_SAAT:
        yuk["durum"] = "burnout_riski"
        yuk["durum_renk"] = "#DC2626"
        yuk["durum_ikon"] = "🔥"
    elif yuk["toplam_saat"] >= HAFTALIK_DIKKAT_SAAT:
        yuk["durum"] = "dikkat"
        yuk["durum_renk"] = "#D97706"
        yuk["durum_ikon"] = "⚠️"
    elif yuk["toplam_saat"] >= HAFTALIK_IDEAL_SAAT * 0.7:
        yuk["durum"] = "ideal"
        yuk["durum_renk"] = "#059669"
        yuk["durum_ikon"] = "✅"
    else:
        yuk["durum"] = "dusuk"
        yuk["durum_renk"] = "#0284C7"
        yuk["durum_ikon"] = "💤"

    return yuk


# ══════════════════════════════════════════════════════════════
# AI ÖNERİ ÜRETİCİ
# ══════════════════════════════════════════════════════════════

def generate_yuk_dengeleme_onerisi(all_loads: list[dict]) -> list[dict]:
    """Tüm öğretmen yüklerinden denge önerileri üret."""
    oneriler = []

    # Yüksek yük olanlar
    burnout = [y for y in all_loads if y.get("durum") == "burnout_riski"]
    dikkat = [y for y in all_loads if y.get("durum") == "dikkat"]
    dusuk = [y for y in all_loads if y.get("durum") == "dusuk"]

    if burnout:
        for y in burnout:
            oneriler.append({
                "seviye": "Kritik",
                "renk": "#DC2626",
                "ikon": "🔥",
                "mesaj": f"**{y.get('teacher_name', y.get('teacher_id'))}** öğretmeni **{y['toplam_saat']:.0f} saatlik** haftalık yük taşıyor. Burnout riski! Acil görev dağılımı yapılmalı.",
                "aksiyon": "Görev devri, bazı ödev kontrollerini erteleme, nöbet değişimi önerilir.",
            })

    if dikkat:
        for y in dikkat:
            oneriler.append({
                "seviye": "Uyarı",
                "renk": "#D97706",
                "ikon": "⚠️",
                "mesaj": f"**{y.get('teacher_name', y.get('teacher_id'))}** öğretmeninin yükü **{y['toplam_saat']:.0f} saat**. Takip edilmeli.",
                "aksiyon": "Yeni görev verilmemeli, mevcut yük gözden geçirilmeli.",
            })

    # Eşitsizlik varsa
    if burnout and dusuk:
        for yuksek in burnout:
            for alcak in dusuk[:1]:  # ilk düşük
                oneriler.append({
                    "seviye": "Öneri",
                    "renk": "#0284C7",
                    "ikon": "💡",
                    "mesaj": f"**{yuksek.get('teacher_name', yuksek.get('teacher_id'))}** → **{alcak.get('teacher_name', alcak.get('teacher_id'))}** görev transferi değerlendirilmeli.",
                    "aksiyon": "Ödev kontrol veya nöbet görevi transferi.",
                })

    # Genel durum
    avg = sum(y["toplam_saat"] for y in all_loads) / max(len(all_loads), 1)
    if avg < HAFTALIK_IDEAL_SAAT * 0.7:
        oneriler.append({
            "seviye": "Bilgi",
            "renk": "#059669",
            "ikon": "✅",
            "mesaj": f"Okulun ortalama haftalık yükü **{avg:.0f} saat**. Sağlıklı seviyede.",
            "aksiyon": "Mevcut dengeyi koruyun.",
        })

    return oneriler


# ══════════════════════════════════════════════════════════════
# UI — Ana Panel
# ══════════════════════════════════════════════════════════════

def render_is_yuku_dengeleyici():
    """İş Yükü Dengeleyici ana paneli."""
    styled_section("⚖️ Öğretmen İş Yükü Dengeleyici", "#4F46E5")

    styled_info_banner(
        "Her öğretmen için haftalık toplam yük (ders + ödev + sınav + nöbet + toplantı). "
        "Burnout önleme, eşitsizlik tespiti, otomatik öneri.",
        "info", "⚖️",
    )

    # Öğretmen listesi
    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        teachers = ak.get_teachers() if hasattr(ak, 'get_teachers') else []
    except Exception:
        teachers = []

    if not teachers:
        styled_info_banner("Öğretmen verisi yok. Önce akademik kadroyu doldurun.", "warning")
        return

    # Hafta seçimi
    bugun = date.today()
    hafta_baslangic = bugun - timedelta(days=bugun.weekday())

    hc1, hc2 = st.columns([1, 3])
    with hc1:
        sel_hafta = st.date_input(
            "Hafta Başı",
            value=hafta_baslangic,
            key="_iyd_hafta_widget",
        )

    # Tüm öğretmenlerin yükünü hesapla
    all_loads = []
    for t in teachers:
        tid = t.id if hasattr(t, 'id') else t.get('id', '')
        tad = t.tam_ad if hasattr(t, 'tam_ad') else t.get('tam_ad', f"Öğretmen {tid}")
        load = calculate_teacher_load(str(tid), sel_hafta)
        load["teacher_name"] = tad
        load["branch"] = getattr(t, 'brans', t.get('brans', '—') if isinstance(t, dict) else '—')
        all_loads.append(load)

    # İstatistik
    burnout_sayi = sum(1 for y in all_loads if y.get("durum") == "burnout_riski")
    dikkat_sayi = sum(1 for y in all_loads if y.get("durum") == "dikkat")
    ideal_sayi = sum(1 for y in all_loads if y.get("durum") == "ideal")
    dusuk_sayi = sum(1 for y in all_loads if y.get("durum") == "dusuk")
    avg_yuk = round(sum(y["toplam_saat"] for y in all_loads) / max(len(all_loads), 1), 1)

    styled_stat_row([
        ("Toplam Öğretmen", str(len(teachers)), "#4F46E5", "👥"),
        ("🔥 Burnout Riski", str(burnout_sayi), "#DC2626", "🔥"),
        ("⚠️ Dikkat", str(dikkat_sayi), "#D97706", "⚠️"),
        ("✅ İdeal", str(ideal_sayi), "#059669", "✅"),
        ("📉 Ortalama (saat)", str(avg_yuk), "#0284C7", "📉"),
    ])

    tabs = st.tabs(["📊 Öğretmen Listesi", "🧠 AI Denge Önerileri", "➕ Manuel Yük Ekle"])

    # Tab 1: Öğretmen listesi
    with tabs[0]:
        # Sırala (en yüksek yük önce)
        all_loads.sort(key=lambda x: -x["toplam_saat"])

        for yuk in all_loads:
            durum_renk = yuk["durum_renk"]
            durum_ikon = yuk["durum_ikon"]
            saat = yuk["toplam_saat"]

            # Görsel bar
            bar_width = min(100, saat / HAFTALIK_BURNOUT_SAAT * 100)

            with st.expander(
                f"{durum_ikon} **{yuk['teacher_name']}** ({yuk.get('branch', '—')}) — **{saat} saat** [{yuk['durum']}]"
            ):
                # Progress bar
                st.markdown(f"""
                <div style="margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:4px;">
                        <span style="color:#94A3B8;">Haftalık Toplam Yük</span>
                        <span style="color:{durum_renk};font-weight:700;">{saat} / {HAFTALIK_BURNOUT_SAAT} saat</span>
                    </div>
                    <div style="background:#18181B;border-radius:8px;height:12px;overflow:hidden;">
                        <div style="width:{bar_width}%;height:100%;background:{durum_renk};border-radius:8px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Kalem detayları
                st.markdown("**📋 Yük Kalemleri:**")
                for tip_kod, saat_val in yuk["kalemler"].items():
                    if saat_val > 0:
                        tip_info = YUK_TIPLERI.get(tip_kod, {"ad": tip_kod, "ikon": "•"})
                        st.markdown(f"• {tip_info['ikon']} **{tip_info['ad']}**: {saat_val:.1f} saat")

                # Eşikler
                st.caption(f"📊 İdeal: ≤{HAFTALIK_IDEAL_SAAT}s | Dikkat: {HAFTALIK_IDEAL_SAAT}-{HAFTALIK_DIKKAT_SAAT}s | Burnout: >{HAFTALIK_BURNOUT_SAAT}s")

    # Tab 2: AI Öneriler
    with tabs[1]:
        oneriler = generate_yuk_dengeleme_onerisi(all_loads)
        if not oneriler:
            styled_info_banner("Şu anda öneri yok. Tüm öğretmenler dengeli çalışıyor.", "success")
        else:
            for o in oneriler:
                st.markdown(f"""
                <div style="background:{o['renk']}15;border-left:4px solid {o['renk']};
                border-radius:0 12px 12px 0;padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <span style="font-size:1.2rem;">{o['ikon']} <strong style="color:{o['renk']};">{o['seviye']}</strong></span>
                    </div>
                    <div style="color:#E4E4E7;font-size:0.9rem;line-height:1.6;">
                        {o['mesaj']}
                    </div>
                    <div style="color:#94A3B8;font-size:0.82rem;margin-top:6px;padding-top:6px;border-top:1px solid {o['renk']}20;">
                        💡 <strong>Aksiyon:</strong> {o['aksiyon']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 3: Manuel yük ekle
    with tabs[2]:
        st.markdown("**Otomatik sisteme giremeyen yükleri manuel ekleyin:**")

        with st.form("manuel_yuk_form"):
            teacher_names = [f"{t.tam_ad if hasattr(t, 'tam_ad') else t.get('tam_ad', '')}" for t in teachers]
            sel_idx = st.selectbox("Öğretmen", range(len(teachers)),
                                    format_func=lambda i: teacher_names[i], key="_iyd_t_widget")
            sel_teacher = teachers[sel_idx]
            sel_tid = str(sel_teacher.id if hasattr(sel_teacher, 'id') else sel_teacher.get('id', ''))

            manuel_kalemler = {}
            for kod, info in YUK_TIPLERI.items():
                manuel_kalemler[kod] = st.number_input(
                    f"{info['ikon']} {info['ad']} (saat)",
                    min_value=0.0, max_value=80.0, value=0.0, step=0.5,
                    key=f"_iyd_yuk_{kod}_widget",
                )

            if st.form_submit_button("💾 Kaydet", type="primary"):
                yukler = _load_yukler()
                yukler.append({
                    "teacher_id": sel_tid,
                    "teacher_name": teacher_names[sel_idx],
                    "hafta_baslangic": sel_hafta.isoformat(),
                    "kalemler": {k: v for k, v in manuel_kalemler.items() if v > 0},
                    "olusturma_tarihi": datetime.now().isoformat(),
                })
                _save_yukler(yukler)
                st.success(f"✅ {teacher_names[sel_idx]} için manuel yük eklendi.")
                st.rerun()
