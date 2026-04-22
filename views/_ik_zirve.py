"""
Insan Kaynaklari — Zirve Ozellikleri
======================================
1. Personel Yetenek Haritasi + Gelisim Radari (Skill Matrix)
2. 360 Derece Geri Bildirim Sistemi
3. IK Komuta Merkezi + Prediktif Analitik
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# 1. YETENEK HARİTASI + GELİŞİM RADARI
# ============================================================

_YETKINLIKLER = {
    "teknik": {"label": "Teknik / Alan Bilgisi", "ikon": "🔧", "renk": "#2563eb",
               "alt": ["Mufredat Hakimiyeti", "Teknoloji Kullanimi", "Materyal Hazirlama", "Olcme Yontemleri"]},
    "pedagojik": {"label": "Pedagojik Yetkinlik", "ikon": "📚", "renk": "#7c3aed",
                  "alt": ["Sinif Yonetimi", "Ogrenme Farklilastirma", "Motivasyon", "Geri Bildirim"]},
    "sosyal": {"label": "Sosyal / Iletisim", "ikon": "🤝", "renk": "#10b981",
               "alt": ["Veli Iletisimi", "Takim Calismasi", "Empati", "Cozum Odaklilik"]},
    "liderlik": {"label": "Liderlik / Yonetim", "ikon": "🏅", "renk": "#f59e0b",
                 "alt": ["Mentorluk", "Proje Yonetimi", "Karar Verme", "Vizyoner Dusunme"]},
    "dijital": {"label": "Dijital Yetkinlik", "ikon": "💻", "renk": "#0891b2",
                "alt": ["Dijital Arac Kullanimi", "Online Ders", "Veri Analizi", "Icerik Uretimi"]},
    "kisisel": {"label": "Kisisel Gelisim", "ikon": "🌱", "renk": "#059669",
                "alt": ["Zaman Yonetimi", "Stres Yonetimi", "Ogrenme Istegi", "Esneklik"]},
}


def _yetenek_path() -> str:
    return os.path.join(_td(), "ik", "yetenek_haritasi.json")


def _load_yetenekler() -> list[dict]:
    return _lj(_yetenek_path())


def _save_yetenekler(data: list[dict]):
    _sj(_yetenek_path(), data)


def render_yetenek_haritasi(store):
    """Personel yetenek haritasi — skill matrix + radar chart."""
    styled_section("Yetenek Haritasi", "#2563eb")
    styled_info_banner(
        "Her personelin 6 ana yetkinlik alanindaki seviyesini izleyin. "
        "Departman bazli bosluklari tespit edin, hedefli egitim planlayin.",
        banner_type="info", icon="🧩")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    yetenekler = _load_yetenekler()

    # Personel → yetenek map
    yetenek_map = {y["employee_id"]: y for y in yetenekler}

    styled_stat_row([
        ("Aktif Personel", str(len(aktif)), "#2563eb", "👥"),
        ("Degerlendirilen", str(len(yetenekler)), "#10b981", "✅"),
        ("Degerlendirilmeyen", str(len(aktif) - len(yetenekler)), "#f59e0b", "⚠️"),
    ])

    sub = st.tabs(["🧩 Bireysel Profil", "📊 Departman Analizi", "➕ Degerlendirme Gir"])

    # ═══ BİREYSEL PROFİL ═══
    with sub[0]:
        styled_section("Personel Yetkinlik Profili")
        if not yetenekler:
            styled_info_banner("Henuz yetkinlik degerlendirmesi girilmemis. 'Degerlendirme Gir' sekmesinden baslatin.", banner_type="info", icon="📝")
        else:
            p_labels = []
            for y in yetenekler:
                emp = next((e for e in aktif if e.get("id") == y.get("employee_id")), None)
                if emp:
                    p_labels.append(f"{emp.get('name', '')} {emp.get('surname', '')} — {emp.get('position', '')}")
                else:
                    p_labels.append(y.get("employee_id", "?"))

            secili = st.selectbox("Personel Secin", [""] + p_labels, key="yt_sec")
            if secili and secili in p_labels:
                idx = p_labels.index(secili)
                y = yetenekler[idx]
                puanlar = y.get("puanlar", {})

                # Radar chart (HTML/SVG)
                genel_ort = round(sum(puanlar.get(k, 0) for k in _YETKINLIKLER) / max(len(_YETKINLIKLER), 1), 1)
                g_renk = "#10b981" if genel_ort >= 4 else "#f59e0b" if genel_ort >= 3 else "#ef4444"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {g_renk}40;border-radius:16px;
                            padding:18px 22px;text-align:center;margin-bottom:14px;">
                    <div style="font-size:48px;font-weight:900;color:{g_renk};
                                font-family:Playfair Display,Georgia,serif;">{genel_ort}</div>
                    <div style="font-size:10px;color:#94a3b8;letter-spacing:1.5px;">GENEL YETKINLIK ORTALAMASI (1-5)</div>
                </div>""", unsafe_allow_html=True)

                # Yetkinlik barlari
                for yk_key, yk_info in _YETKINLIKLER.items():
                    puan = puanlar.get(yk_key, 0)
                    bar_w = round(puan / 5 * 100)
                    p_renk = "#10b981" if puan >= 4 else "#f59e0b" if puan >= 3 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                        <span style="font-size:16px;min-width:24px;">{yk_info['ikon']}</span>
                        <span style="min-width:160px;font-size:12px;color:#e2e8f0;font-weight:600;">{yk_info['label']}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:20px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{yk_info['renk']},{yk_info['renk']}80);
                                        border-radius:4px;display:flex;align-items:center;padding-left:8px;">
                                <span style="font-size:10px;color:#fff;font-weight:800;">{puan}/5</span></div></div>
                    </div>""", unsafe_allow_html=True)

                # Alt yetkinlik detay
                with st.expander("Alt Yetkinlik Detaylari", expanded=False):
                    alt_puanlar = y.get("alt_puanlar", {})
                    for yk_key, yk_info in _YETKINLIKLER.items():
                        st.markdown(f"**{yk_info['ikon']} {yk_info['label']}:**")
                        for alt in yk_info["alt"]:
                            alt_puan = alt_puanlar.get(f"{yk_key}_{alt}", 0)
                            st.markdown(f"- {alt}: {'⭐' * alt_puan}{'☆' * (5 - alt_puan)} ({alt_puan}/5)")

    # ═══ DEPARTMAN ANALİZİ ═══
    with sub[1]:
        styled_section("Departman Yetkinlik Analizi")
        if not yetenekler:
            styled_info_banner("Henuz veri yok.", banner_type="info", icon="📊")
        else:
            # Departman/brans bazli gruplama
            dept_yetkinlik: dict[str, dict[str, list]] = {}
            for y in yetenekler:
                emp = next((e for e in aktif if e.get("id") == y.get("employee_id")), None)
                dept = emp.get("branch", emp.get("department", "Genel")) if emp else "Genel"
                if dept not in dept_yetkinlik:
                    dept_yetkinlik[dept] = {k: [] for k in _YETKINLIKLER}
                for yk_key in _YETKINLIKLER:
                    puan = y.get("puanlar", {}).get(yk_key, 0)
                    if puan > 0:
                        dept_yetkinlik[dept][yk_key].append(puan)

            for dept, yetkinlikler_d in sorted(dept_yetkinlik.items()):
                st.markdown(f"##### {dept}")
                for yk_key, yk_info in _YETKINLIKLER.items():
                    puanlar_l = yetkinlikler_d.get(yk_key, [])
                    ort = round(sum(puanlar_l) / max(len(puanlar_l), 1), 1) if puanlar_l else 0
                    bar_w = round(ort / 5 * 100)
                    renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                        <span style="min-width:140px;font-size:10px;color:#94a3b8;">{yk_info['ikon']} {yk_info['label']}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                        display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:8px;color:#fff;font-weight:700;">{ort}</span></div></div>
                        <span style="font-size:9px;color:#64748b;min-width:40px;">{len(puanlar_l)} kisi</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")

    # ═══ DEĞERLENDİRME GİR ═══
    with sub[2]:
        styled_section("Yeni Yetkinlik Degerlendirmesi")
        if not aktif:
            styled_info_banner("Aktif calisan bulunamadi.", banner_type="warning", icon="⚠️")
        else:
            emp_labels = [f"{e.get('name', '')} {e.get('surname', '')} — {e.get('position', '')}" for e in aktif]
            secili_emp = st.selectbox("Personel", emp_labels, key="yt_yeni_emp")

            if secili_emp:
                emp_idx = emp_labels.index(secili_emp)
                emp = aktif[emp_idx]

                with st.form("yetenek_form"):
                    puanlar = {}
                    alt_puanlar = {}

                    for yk_key, yk_info in _YETKINLIKLER.items():
                        st.markdown(f"**{yk_info['ikon']} {yk_info['label']}**")
                        cols = st.columns(len(yk_info["alt"]))
                        alt_toplam = 0
                        for i, alt in enumerate(yk_info["alt"]):
                            with cols[i]:
                                val = st.slider(alt, 1, 5, 3, key=f"yt_{yk_key}_{i}")
                                alt_puanlar[f"{yk_key}_{alt}"] = val
                                alt_toplam += val
                        puanlar[yk_key] = round(alt_toplam / len(yk_info["alt"]), 1)

                    degerlendiren = st.text_input("Degerlendiren", placeholder="Ad Soyad")
                    notlar = st.text_area("Notlar (istege bagli)", height=60)

                    if st.form_submit_button("Kaydet", type="primary"):
                        yeni = {
                            "id": f"yt_{uuid.uuid4().hex[:8]}",
                            "employee_id": emp.get("id", ""),
                            "puanlar": puanlar,
                            "alt_puanlar": alt_puanlar,
                            "degerlendiren": degerlendiren,
                            "notlar": notlar,
                            "tarih": date.today().isoformat(),
                            "created_at": datetime.now().isoformat(),
                        }
                        # Mevcut varsa guncelle
                        mevcut = [y for y in yetenekler if y.get("employee_id") != emp.get("id")]
                        mevcut.append(yeni)
                        _save_yetenekler(mevcut)
                        st.success(f"Yetkinlik degerlendirmesi kaydedildi: {secili_emp}")
                        st.rerun()


# ============================================================
# 2. 360° GERİ BİLDİRİM SİSTEMİ
# ============================================================

_360_KAYNAKLAR = {
    "yonetici": {"label": "Ust Yonetici", "ikon": "👔", "renk": "#2563eb"},
    "meslektas": {"label": "Meslektas", "ikon": "🤝", "renk": "#7c3aed"},
    "veli": {"label": "Veli", "ikon": "👪", "renk": "#f59e0b"},
    "oz": {"label": "Oz Degerlendirme", "ikon": "🪞", "renk": "#0891b2"},
}

_360_KRITERLER = [
    "Alan Bilgisi", "Sinif Yonetimi", "Iletisim", "Takım Calismasi",
    "Motivasyon", "Mesleki Gelisim",
]


def _fb360_path() -> str:
    return os.path.join(_td(), "ik", "feedback_360.json")


def _load_fb360() -> list[dict]:
    return _lj(_fb360_path())


def _save_fb360(data: list[dict]):
    _sj(_fb360_path(), data)


def render_360_feedback(store):
    """360 derece geri bildirim sistemi."""
    styled_section("360 Geri Bildirim", "#7c3aed")
    styled_info_banner(
        "4 farkli kaynaktan anonim geri bildirim: Yonetici, meslektas, veli, oz degerlendirme. "
        "Kor noktaları tespit edin, gercek resmi gorun.",
        banner_type="info", icon="🔄")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    feedbackler = _load_fb360()

    # Personel bazli gruplama
    emp_fb: dict[str, list[dict]] = {}
    for fb in feedbackler:
        eid = fb.get("employee_id", "")
        emp_fb.setdefault(eid, []).append(fb)

    styled_stat_row([
        ("Aktif Personel", str(len(aktif)), "#7c3aed", "👥"),
        ("Toplam Feedback", str(len(feedbackler)), "#10b981", "📋"),
        ("Degerlendirilen", str(len(emp_fb)), "#2563eb", "✅"),
    ])

    sub = st.tabs(["📊 Sonuclar", "➕ Feedback Gir", "🔍 Gap Analizi"])

    # ═══ SONUÇLAR ═══
    with sub[0]:
        styled_section("360 Feedback Sonuclari")
        if not emp_fb:
            styled_info_banner("Henuz feedback girilmemis.", banner_type="info", icon="📝")
        else:
            for eid, fbs in emp_fb.items():
                emp = next((e for e in aktif if e.get("id") == eid), None)
                emp_ad = f"{emp.get('name', '')} {emp.get('surname', '')}" if emp else eid

                with st.expander(f"👤 {emp_ad} ({len(fbs)} feedback)", expanded=False):
                    # Kaynak bazli ortalamalar
                    for kaynak_key, kaynak_info in _360_KAYNAKLAR.items():
                        k_fbs = [fb for fb in fbs if fb.get("kaynak") == kaynak_key]
                        if not k_fbs:
                            continue
                        # Ortalama puan
                        tum_puanlar = []
                        for fb in k_fbs:
                            for kriter in _360_KRITERLER:
                                p = fb.get("puanlar", {}).get(kriter, 0)
                                if p > 0:
                                    tum_puanlar.append(p)
                        ort = round(sum(tum_puanlar) / max(len(tum_puanlar), 1), 1)
                        bar_w = round(ort / 5 * 100)
                        renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"

                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                            <span style="font-size:14px;">{kaynak_info['ikon']}</span>
                            <span style="min-width:120px;font-size:11px;color:#e2e8f0;font-weight:600;">{kaynak_info['label']}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                                <div style="width:{bar_w}%;height:100%;background:{kaynak_info['renk']};border-radius:4px;
                                            display:flex;align-items:center;padding-left:6px;">
                                    <span style="font-size:9px;color:#fff;font-weight:700;">{ort}/5</span></div></div>
                            <span style="font-size:9px;color:#64748b;">{len(k_fbs)} fb</span>
                        </div>""", unsafe_allow_html=True)

    # ═══ FEEDBACK GİR ═══
    with sub[1]:
        styled_section("Yeni 360 Feedback")
        if not aktif:
            styled_info_banner("Aktif calisan yok.", banner_type="warning", icon="⚠️")
        else:
            emp_labels = [f"{e.get('name', '')} {e.get('surname', '')}" for e in aktif]
            secili_emp = st.selectbox("Degerlendirilen Personel", emp_labels, key="fb_emp")
            kaynak = st.selectbox("Kaynak", list(_360_KAYNAKLAR.keys()),
                                   format_func=lambda x: f"{_360_KAYNAKLAR[x]['ikon']} {_360_KAYNAKLAR[x]['label']}",
                                   key="fb_kaynak")

            with st.form("fb360_form"):
                puanlar = {}
                cols = st.columns(3)
                for i, kriter in enumerate(_360_KRITERLER):
                    with cols[i % 3]:
                        puanlar[kriter] = st.slider(kriter, 1, 5, 3, key=f"fb_{kriter}")

                yorum = st.text_area("Yorum (anonim)", height=60, placeholder="Guclu yonleri ve gelisim alanlari...")

                if st.form_submit_button("Gonder (Anonim)", type="primary"):
                    emp_idx = emp_labels.index(secili_emp)
                    emp = aktif[emp_idx]
                    yeni = {
                        "id": f"fb_{uuid.uuid4().hex[:8]}",
                        "employee_id": emp.get("id", ""),
                        "kaynak": kaynak,
                        "puanlar": puanlar,
                        "yorum": yorum,
                        "donem": f"{date.today().year}-{1 if date.today().month <= 6 else 2}. Donem",
                        "tarih": date.today().isoformat(),
                    }
                    feedbackler.append(yeni)
                    _save_fb360(feedbackler)
                    st.success("Feedback anonim olarak kaydedildi!")
                    st.rerun()

    # ═══ GAP ANALİZİ ═══
    with sub[2]:
        styled_section("Oz Degerlendirme vs Diger — Kor Nokta Tespiti")
        if not emp_fb:
            styled_info_banner("Gap analizi icin feedback gerekli.", banner_type="info", icon="🔍")
        else:
            for eid, fbs in emp_fb.items():
                emp = next((e for e in aktif if e.get("id") == eid), None)
                if not emp:
                    continue
                emp_ad = f"{emp.get('name', '')} {emp.get('surname', '')}"

                oz_fbs = [fb for fb in fbs if fb.get("kaynak") == "oz"]
                diger_fbs = [fb for fb in fbs if fb.get("kaynak") != "oz"]

                if not oz_fbs or not diger_fbs:
                    continue

                # Kriter bazli gap
                gaps = []
                for kriter in _360_KRITERLER:
                    oz_ort = sum(fb.get("puanlar", {}).get(kriter, 0) for fb in oz_fbs) / max(len(oz_fbs), 1)
                    diger_ort = sum(fb.get("puanlar", {}).get(kriter, 0) for fb in diger_fbs) / max(len(diger_fbs), 1)
                    gap = round(oz_ort - diger_ort, 1)
                    gaps.append({"kriter": kriter, "oz": round(oz_ort, 1), "diger": round(diger_ort, 1), "gap": gap})

                kor_noktalar = [g for g in gaps if g["gap"] > 1]  # Kendini 1+ puan yuksek goruyor
                if kor_noktalar:
                    st.markdown(f"**{emp_ad}** — {len(kor_noktalar)} kor nokta")
                    for g in kor_noktalar:
                        st.markdown(f"""
                        <div style="background:#7f1d1d;border:1px solid #ef4444;border-radius:8px;
                                    padding:6px 12px;margin-bottom:4px;font-size:11px;">
                            <span style="color:#fca5a5;font-weight:700;">{g['kriter']}</span>:
                            Oz: {g['oz']}/5 vs Diger: {g['diger']}/5
                            <span style="color:#ef4444;font-weight:800;"> (gap: +{g['gap']})</span>
                        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. İK KOMUTA MERKEZİ + PREDİKTİF ANALİTİK
# ============================================================

def render_ik_komuta(store):
    """IK canli durum paneli + gelecege yonelik tahminler."""
    styled_section("IK Komuta Merkezi", "#0d9488")

    td = _td()
    bugun = date.today()
    bugun_str = bugun.isoformat()

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    izinler = store.load_list("izinler") if hasattr(store, "load_list") else []
    performans = store.load_list("performance_reviews") if hasattr(store, "load_list") else []
    disiplin = store.load_list("disiplin") if hasattr(store, "load_list") else []
    interviews = store.load_list("interviews") if hasattr(store, "load_list") else []
    candidates = store.load_list("candidates") if hasattr(store, "load_list") else []
    egitimler = store.load_list("egitimler") if hasattr(store, "load_list") else []
    bordro = store.load_list("maas_bordro") if hasattr(store, "load_list") else []
    positions = store.load_list("positions") if hasattr(store, "load_list") else []

    # Bugun izinli
    bugun_izinli = []
    for iz in izinler:
        bas = iz.get("baslangic_tarihi", "")
        bit = iz.get("bitis_tarihi", "") or bas
        if bas and bas <= bugun_str <= bit:
            bugun_izinli.append(iz.get("personel_adi", "?"))

    # Acik pozisyon
    dolu_poz = set(e.get("position", "") for e in aktif)
    acik_poz = [p for p in positions if p.get("title", "") not in dolu_poz]

    # Yaklasan izin bitis (7 gun)
    yedi_gun = (bugun + timedelta(days=7)).isoformat()
    yaklasan_izin = [iz for iz in izinler if iz.get("bitis_tarihi", "") and bugun_str <= iz["bitis_tarihi"] <= yedi_gun]

    # Dogum gunu (bu hafta)
    dogum_gunu = []
    for e in aktif:
        dg = e.get("birth_date", e.get("dogum_tarihi", ""))
        if dg and len(dg) >= 10:
            try:
                if abs(int(dg[5:7]) - bugun.month) <= 0 and abs(int(dg[8:10]) - bugun.day) <= 7:
                    dogum_gunu.append(f"{e.get('name', '')} {e.get('surname', '')}")
            except Exception:
                pass

    # ── KOMUTA HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#042f2e 0%,#134e4a 50%,#0d9488 100%);
                border:2px solid #14b8a6;border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(20,184,166,0.25);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,#14b8a6,#5eead4,#14b8a6,transparent);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:10px;color:#5eead4;letter-spacing:3px;text-transform:uppercase;">
                    SmartCampus AI</div>
                <div style="font-size:28px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;">IK Komuta Merkezi</div>
            </div>
            <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:14px;padding:12px 20px;">
                <div style="font-size:36px;font-weight:900;color:#5eead4;line-height:1;">{len(aktif)}</div>
                <div style="font-size:9px;color:#99f6e4;">Aktif Personel</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#f59e0b;">{len(bugun_izinli)}</div>
                <div style="font-size:8px;color:#99f6e4;">Bugun Izinli</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#ef4444;">{len(acik_poz)}</div>
                <div style="font-size:8px;color:#99f6e4;">Acik Pozisyon</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#3b82f6;">{len(interviews)}</div>
                <div style="font-size:8px;color:#99f6e4;">Mulakat</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#7c3aed;">{len(performans)}</div>
                <div style="font-size:8px;color:#99f6e4;">Performans</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#ec4899;">{len(dogum_gunu)}</div>
                <div style="font-size:8px;color:#99f6e4;">Dogum Gunu</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── İzinli personel ──
    if bugun_izinli:
        styled_section(f"Bugun Izinli ({len(bugun_izinli)})")
        for isim in bugun_izinli[:10]:
            st.markdown(f"- 🏖️ {isim}")

    sub = st.tabs(["📊 Canli Durum", "🔮 Tahminler", "💰 Maliyet Projeksiyon"])

    # ═══ CANLI DURUM ═══
    with sub[0]:
        # Departman bazli dagılım
        styled_section("Departman Dagilimi")
        dept_sayac = Counter(e.get("branch", e.get("department", "Genel")) for e in aktif)
        if dept_sayac:
            en_cok = dept_sayac.most_common(1)[0][1]
            for dept, sayi in dept_sayac.most_common():
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="min-width:120px;font-size:11px;color:#e2e8f0;font-weight:600;">{dept}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#0d9488;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

    # ═══ TAHMİNLER ═══
    with sub[1]:
        styled_section("Prediktif IK Analitik")

        # Turnover risk
        styled_section("Ayrilma Riski Tahmini", "#ef4444")
        riskli_personel = []
        for e in aktif:
            eid = e.get("id", "")
            risk = 0
            # Cok izin = risk
            e_izin = sum(1 for iz in izinler if iz.get("employee_id", iz.get("personel_id", "")) == eid)
            risk += min(e_izin * 5, 20)
            # Disiplin = risk
            e_disiplin = sum(1 for d in disiplin if d.get("employee_id", "") == eid)
            risk += min(e_disiplin * 15, 30)
            # Dusuk performans = risk
            e_perf = [p for p in performans if p.get("employee_id", "") == eid]
            if e_perf:
                son_puan = e_perf[-1].get("puan", e_perf[-1].get("genel_puan", 50))
                if isinstance(son_puan, (int, float)) and son_puan < 50:
                    risk += 25
            # Egitim eksikliği = risk
            e_egitim = sum(1 for eg in egitimler if eg.get("employee_id", "") == eid)
            if e_egitim == 0:
                risk += 10

            risk = min(risk, 100)
            if risk >= 30:
                riskli_personel.append({
                    "ad": f"{e.get('name', '')} {e.get('surname', '')}",
                    "pozisyon": e.get("position", ""),
                    "risk": risk,
                    "izin": e_izin, "disiplin": e_disiplin,
                })

        riskli_personel.sort(key=lambda x: -x["risk"])

        if riskli_personel:
            for rp in riskli_personel[:10]:
                r_renk = "#ef4444" if rp["risk"] >= 60 else "#f97316" if rp["risk"] >= 40 else "#f59e0b"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {r_renk}30;border-left:4px solid {r_renk};
                            border-radius:0 10px 10px 0;padding:8px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{rp['ad']}</span>
                        <span style="background:{r_renk}20;color:{r_renk};padding:2px 10px;border-radius:6px;
                                    font-size:10px;font-weight:700;">%{rp['risk']} risk</span>
                    </div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:2px;">
                        {rp['pozisyon']} · Izin: {rp['izin']} · Disiplin: {rp['disiplin']}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Yuksek ayrilma riski olan personel yok!")

        # Kadro planlama
        styled_section("Kadro Planlama Tahmini")
        try:
            from utils.tenant import get_data_path
            ak_dir = get_data_path("akademik")
        except Exception:
            ak_dir = "data/akademik"
        ogrenciler = _lj(os.path.join(ak_dir, "students.json"))
        aktif_ogr = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")
        ogretmen_sayisi = sum(1 for e in aktif if e.get("branch") or e.get("brans"))
        oran = round(aktif_ogr / max(ogretmen_sayisi, 1), 1)

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #0d9488;border-radius:12px;padding:14px 18px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                <div><div style="font-size:24px;font-weight:800;color:#5eead4;">{aktif_ogr}</div>
                    <div style="font-size:9px;color:#94a3b8;">Ogrenci</div></div>
                <div><div style="font-size:24px;font-weight:800;color:#0d9488;">{ogretmen_sayisi}</div>
                    <div style="font-size:9px;color:#94a3b8;">Ogretmen</div></div>
                <div><div style="font-size:24px;font-weight:800;color:{'#ef4444' if oran > 20 else '#f59e0b' if oran > 15 else '#10b981'};">{oran}</div>
                    <div style="font-size:9px;color:#94a3b8;">Ogr/Ogt Orani</div></div>
            </div>
            <div style="font-size:10px;color:#64748b;text-align:center;margin-top:8px;">
                Ideal oran: 12-15 · {'Ek ogretmen gerekli!' if oran > 18 else 'Oran normal.' if oran <= 15 else 'Sinirda.'}</div>
        </div>""", unsafe_allow_html=True)

    # ═══ MALİYET PROJEKSİYON ═══
    with sub[2]:
        styled_section("12 Aylik Personel Maliyet Projeksiyonu")
        if bordro:
            aylik_maliyet = sum(b.get("net_maas", b.get("brut_maas", 0)) for b in bordro
                                 if isinstance(b.get("net_maas", b.get("brut_maas")), (int, float)))
            if aylik_maliyet == 0:
                aylik_maliyet = len(aktif) * 25000  # Tahmini

            for ay in range(1, 13):
                carpan = 1.0
                if ay in (1, 7):  # Ocak/Temmuz zam
                    carpan = 1.25
                elif ay == 12:  # Aralik ikramiye
                    carpan = 2.0
                projeksiyon = round(aylik_maliyet * carpan)
                bar_w = round(projeksiyon / (aylik_maliyet * 2.5) * 100)
                renk = "#ef4444" if carpan > 1.5 else "#f59e0b" if carpan > 1 else "#0d9488"

                from models.yonetim_ekran import _GUN_ADLARI
                ay_adlari = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
                              7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="min-width:60px;font-size:10px;color:#e2e8f0;font-weight:600;">{ay_adlari[ay]}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:16px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:8px;color:#fff;font-weight:700;">{projeksiyon:,.0f} TL</span></div></div>
                </div>""", unsafe_allow_html=True)

            yillik = round(aylik_maliyet * 13.5)  # 12 ay + zam + ikramiye tahmini
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #0d9488;border-radius:12px;padding:14px;
                        text-align:center;margin-top:12px;">
                <div style="font-size:10px;color:#94a3b8;">Tahmini Yillik Personel Maliyeti</div>
                <div style="font-size:28px;font-weight:900;color:#5eead4;">{yillik:,.0f} TL</div>
                <div style="font-size:9px;color:#64748b;">{len(aktif)} personel · Aylik baz: {aylik_maliyet:,.0f} TL</div>
            </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bordro verisi bulunamadi. Maas & Bordro sekmesinden giris yapin.", banner_type="warning", icon="💰")
