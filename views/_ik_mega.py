"""
Insan Kaynaklari — MEGA Ozellikleri
=====================================
1. Personel Dijital Ikiz (Employee Digital Twin)
2. Akilli Ise Alim Asistani (AI Recruitment Engine)
3. Personel Mutluluk Barometresi (Happiness Index)
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


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. PERSONEL DİJİTAL İKİZ
# ============================================================

def _personel_capraz_veri(emp: dict, store) -> dict:
    """Bir personel icin tum modullerden capraz veri topla."""
    td = _td()
    ak = _ak_dir()
    eid = emp.get("id", "")
    ad = f"{emp.get('name', '')} {emp.get('surname', '')}".strip().lower()
    veri = {"ik": {}, "akademik": {}, "toplanti": {}, "nobet": {}, "yetenek": {}, "fb360": {}}

    # IK verileri
    izinler = store.load_list("izinler") if hasattr(store, "load_list") else []
    perf = store.load_list("performance_reviews") if hasattr(store, "load_list") else []
    disiplin = store.load_list("disiplin") if hasattr(store, "load_list") else []
    egitim = store.load_list("egitimler") if hasattr(store, "load_list") else []
    bordro = store.load_list("maas_bordro") if hasattr(store, "load_list") else []

    veri["ik"] = {
        "izin": sum(1 for iz in izinler if iz.get("employee_id", iz.get("personel_id", "")) == eid
                     or ad in (iz.get("personel_adi", "") or "").lower()),
        "performans": [p for p in perf if p.get("employee_id") == eid],
        "disiplin": sum(1 for d in disiplin if d.get("employee_id") == eid),
        "egitim": sum(1 for e in egitim if e.get("employee_id") == eid),
        "bordro": sum(1 for b in bordro if b.get("employee_id") == eid),
    }

    # Akademik — not girisi, kazanim
    notlar = _lj(os.path.join(ak, "grades.json"))
    veri["akademik"]["not_girisi"] = sum(1 for n in notlar if ad in (n.get("ogretmen_adi", "") or "").lower())

    kazanim = _lj(os.path.join(ak, "kazanim_isleme.json"))
    veri["akademik"]["kazanim"] = sum(1 for k in kazanim if ad in (k.get("ogretmen_adi", "") or "").lower())

    # Ders programi
    schedule = _lj(os.path.join(ak, "schedule.json"))
    veri["akademik"]["ders_sayi"] = sum(1 for s in schedule if ad in (s.get("ogretmen", "") or "").lower())

    # Toplanti katilimi
    try:
        from models.toplanti_kurullar import ToplantiDataStore
        top = ToplantiDataStore(os.path.join(td, "toplanti"))
        katilimcilar = top.load_list("participants") if hasattr(top, "load_list") else []
        veri["toplanti"]["katilim"] = sum(1 for p in katilimcilar
                                           if ad in (p.get("ad_soyad", p.get("name", "")) or "").lower())
    except Exception:
        veri["toplanti"]["katilim"] = 0

    # Nobet
    nobet = _lj(os.path.join(ak, "nobet_kayitlar.json"))
    veri["nobet"]["toplam"] = sum(1 for n in nobet if ad in (n.get("ogretmen_adi", "") or "").lower())

    # Yetenek haritasi
    yetenekler = _lj(os.path.join(td, "ik", "yetenek_haritasi.json"))
    yt = next((y for y in yetenekler if y.get("employee_id") == eid), None)
    if yt:
        puanlar = yt.get("puanlar", {})
        veri["yetenek"] = {"ort": round(sum(puanlar.values()) / max(len(puanlar), 1), 1), "detay": puanlar}

    # 360 feedback
    fb360 = _lj(os.path.join(td, "ik", "feedback_360.json"))
    e_fb = [fb for fb in fb360 if fb.get("employee_id") == eid]
    if e_fb:
        tum_p = []
        for fb in e_fb:
            tum_p.extend(fb.get("puanlar", {}).values())
        veri["fb360"] = {"ort": round(sum(tum_p) / max(len(tum_p), 1), 1), "sayi": len(e_fb)}

    return veri


def _bilesik_skor(emp: dict, veri: dict) -> float:
    """12 modülden bileşik performans skoru (0-100)."""
    puan = 50  # baz
    # IK
    perf_list = veri["ik"].get("performans", [])
    if perf_list:
        son = perf_list[-1]
        p = son.get("puan", son.get("genel_puan", 50))
        if isinstance(p, (int, float)):
            puan += (p - 50) * 0.3
    puan -= min(veri["ik"].get("disiplin", 0) * 5, 15)
    puan += min(veri["ik"].get("egitim", 0) * 3, 12)
    # Akademik
    puan += min(veri["akademik"].get("not_girisi", 0) * 0.05, 8)
    puan += min(veri["akademik"].get("kazanim", 0) * 0.1, 8)
    puan += min(veri["akademik"].get("ders_sayi", 0) * 0.3, 6)
    # Toplanti
    puan += min(veri["toplanti"].get("katilim", 0) * 1, 5)
    # Yetenek
    yt_ort = veri.get("yetenek", {}).get("ort", 0)
    if yt_ort > 0:
        puan += (yt_ort - 3) * 4
    # 360
    fb_ort = veri.get("fb360", {}).get("ort", 0)
    if fb_ort > 0:
        puan += (fb_ort - 3) * 3
    return max(0, min(100, round(puan, 1)))


def render_dijital_ikiz(store):
    """Personel dijital ikiz — tum modullerden capraz profil."""
    styled_section("Personel Dijital Ikiz", "#6366f1")
    styled_info_banner(
        "Her personelin tum modullerdeki verileri tek ekranda. "
        "IK + Akademik + Toplanti + Nobet + Yetenek + 360 = Bilesik Skor.",
        banner_type="info", icon="👤")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]

    if not aktif:
        styled_info_banner("Aktif calisan bulunamadi.", banner_type="warning", icon="⚠️")
        return

    emp_labels = [f"{e.get('name', '')} {e.get('surname', '')} — {e.get('position', '')}" for e in aktif]
    secili = st.selectbox("Personel Secin", [""] + emp_labels, key="dikiz_sec")

    if not secili:
        return

    idx = emp_labels.index(secili)
    emp = aktif[idx]

    with st.spinner("Dijital ikiz yukleniyor..."):
        veri = _personel_capraz_veri(emp, store)
        skor = _bilesik_skor(emp, veri)

    s_renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 50 else "#ef4444"

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                border:2px solid {s_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {s_renk}30;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
            <div>
                <div style="font-size:24px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                    {emp.get('name', '')} {emp.get('surname', '')}</div>
                <div style="font-size:12px;color:#a5b4fc;margin-top:4px;">
                    {emp.get('position', '')} · {emp.get('branch', emp.get('department', ''))} · {emp.get('employee_code', '')}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:52px;font-weight:900;color:{s_renk};line-height:1;">{skor}</div>
                <div style="font-size:9px;color:#a5b4fc;letter-spacing:1.5px;">BILESIK SKOR</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── MODÜL KARTLARI ──
    col1, col2 = st.columns(2)

    with col1:
        # IK
        ik = veri["ik"]
        son_perf = ik["performans"][-1].get("puan", ik["performans"][-1].get("genel_puan", "-")) if ik["performans"] else "-"
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #6366f130;border-left:4px solid #6366f1;
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="font-weight:700;color:#a5b4fc;font-size:13px;margin-bottom:6px;">👥 IK Verileri</div>
            <div style="font-size:11px;color:#94a3b8;line-height:1.8;">
                Izin: <b style="color:#e2e8f0;">{ik['izin']}</b> ·
                Performans: <b style="color:#e2e8f0;">{son_perf}</b> ·
                Disiplin: <b style="color:{'#ef4444' if ik['disiplin'] > 0 else '#10b981'};">{ik['disiplin']}</b> ·
                Egitim: <b style="color:#e2e8f0;">{ik['egitim']}</b> ·
                Bordro: <b style="color:#e2e8f0;">{ik['bordro']}</b></div>
        </div>""", unsafe_allow_html=True)

        # Akademik
        ak = veri["akademik"]
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #2563eb30;border-left:4px solid #2563eb;
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="font-weight:700;color:#93c5fd;font-size:13px;margin-bottom:6px;">📚 Akademik Katki</div>
            <div style="font-size:11px;color:#94a3b8;line-height:1.8;">
                Not Girisi: <b style="color:#e2e8f0;">{ak['not_girisi']}</b> ·
                Kazanim: <b style="color:#e2e8f0;">{ak['kazanim']}</b> ·
                Haftalik Ders: <b style="color:#e2e8f0;">{ak['ders_sayi']}</b></div>
        </div>""", unsafe_allow_html=True)

        # Toplanti + Nobet
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #05966930;border-left:4px solid #059669;
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="font-weight:700;color:#6ee7b7;font-size:13px;margin-bottom:6px;">🤝 Katilim</div>
            <div style="font-size:11px;color:#94a3b8;line-height:1.8;">
                Toplanti: <b style="color:#e2e8f0;">{veri['toplanti']['katilim']}</b> ·
                Nobet: <b style="color:#e2e8f0;">{veri['nobet']['toplam']}</b></div>
        </div>""", unsafe_allow_html=True)

    with col2:
        # Yetenek
        yt = veri.get("yetenek", {})
        yt_ort = yt.get("ort", 0)
        yt_renk = "#10b981" if yt_ort >= 4 else "#f59e0b" if yt_ort >= 3 else "#ef4444" if yt_ort > 0 else "#64748b"
        detay_html = ""
        for k, v in yt.get("detay", {}).items():
            detay_html += f"<span style='margin-right:8px;'>{k}: <b>{v}</b></span>"
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {yt_renk}30;border-left:4px solid {yt_renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="font-weight:700;color:#fbbf24;font-size:13px;margin-bottom:6px;">🧩 Yetenek Haritasi</div>
            <div style="font-size:18px;font-weight:800;color:{yt_renk};">{yt_ort}/5</div>
            <div style="font-size:9px;color:#94a3b8;margin-top:4px;">{detay_html or 'Degerlendirme yok'}</div>
        </div>""", unsafe_allow_html=True)

        # 360 feedback
        fb = veri.get("fb360", {})
        fb_ort = fb.get("ort", 0)
        fb_renk = "#10b981" if fb_ort >= 4 else "#f59e0b" if fb_ort >= 3 else "#ef4444" if fb_ort > 0 else "#64748b"
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {fb_renk}30;border-left:4px solid #7c3aed;
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="font-weight:700;color:#c4b5fd;font-size:13px;margin-bottom:6px;">🔄 360 Feedback</div>
            <div style="font-size:18px;font-weight:800;color:{fb_renk};">{fb_ort}/5</div>
            <div style="font-size:9px;color:#94a3b8;">{fb.get('sayi', 0)} feedback</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. AKILLI İŞE ALIM ASİSTANI
# ============================================================

def render_ai_ise_alim(store):
    """AI ile aday esletirme + mulakat stratejisi."""
    styled_section("AI Ise Alim Asistani", "#f59e0b")
    styled_info_banner(
        "Acik pozisyon profilini tanimla, AI en uygun adaylari skor ile sıralar. "
        "Kisiye ozel mulakat sorulari olusturur.",
        banner_type="info", icon="🤖")

    positions = store.load_list("positions") if hasattr(store, "load_list") else []
    candidates = store.load_list("candidates") if hasattr(store, "load_list") else []
    employees = store.load_list("employees") if hasattr(store, "load_list") else []

    # Dolu pozisyonlar
    dolu = set(e.get("position", "") for e in employees if e.get("status") == "Aktif")
    acik_poz = [p for p in positions if p.get("title", "") not in dolu]

    styled_stat_row([
        ("Acik Pozisyon", str(len(acik_poz)), "#f59e0b", "📋"),
        ("Aday Havuzu", str(len(candidates)), "#2563eb", "👤"),
        ("Aktif Personel", str(sum(1 for e in employees if e.get("status") == "Aktif")), "#10b981", "👥"),
    ])

    sub = st.tabs(["🎯 Aday Esletirme", "🎤 Mulakat Stratejisi", "📊 Karsilastirma"])

    # ═══ ADAY EŞLEŞTİRME ═══
    with sub[0]:
        styled_section("Pozisyon - Aday Esletirme")

        if not acik_poz:
            styled_info_banner("Acik pozisyon yok.", banner_type="info", icon="✅")
        elif not candidates:
            styled_info_banner("Aday havuzu bos.", banner_type="warning", icon="📋")
        else:
            poz_labels = [f"{p.get('title', '')} — {p.get('department', '')}" for p in acik_poz]
            secili_poz = st.selectbox("Acik Pozisyon Secin", poz_labels, key="aia_poz")

            if secili_poz:
                poz = acik_poz[poz_labels.index(secili_poz)]

                # Basit esletme skoru
                skorlu_adaylar = []
                for c in candidates:
                    skor = 50
                    # Deneyim
                    if c.get("deneyim_yili") and isinstance(c.get("deneyim_yili"), (int, float)):
                        skor += min(c["deneyim_yili"] * 3, 15)
                    # Brans eslesmesi
                    if poz.get("department") and c.get("brans"):
                        if poz["department"].lower() in c["brans"].lower() or c["brans"].lower() in poz["department"].lower():
                            skor += 20
                    # Egitim seviyesi
                    if c.get("egitim_seviyesi") in ("Yuksek Lisans", "Doktora"):
                        skor += 10
                    elif c.get("egitim_seviyesi") == "Lisans":
                        skor += 5
                    # Mulakat puani
                    interviews = store.load_list("interview_scores") if hasattr(store, "load_list") else []
                    c_scores = [s for s in interviews if s.get("candidate_id") == c.get("id")]
                    if c_scores:
                        ort_s = sum(s.get("puan", s.get("toplam_puan", 50)) for s in c_scores
                                     if isinstance(s.get("puan", s.get("toplam_puan")), (int, float))) / max(len(c_scores), 1)
                        skor += min((ort_s - 50) * 0.3, 15)

                    skor = max(0, min(100, round(skor)))
                    skorlu_adaylar.append({"aday": c, "skor": skor})

                skorlu_adaylar.sort(key=lambda x: -x["skor"])

                st.markdown(f"##### En Uygun Adaylar — {poz.get('title', '')}")
                for i, sa in enumerate(skorlu_adaylar[:10], 1):
                    c = sa["aday"]
                    skor = sa["skor"]
                    s_renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 50 else "#ef4444"
                    madalya = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"#{i}")

                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid {s_renk}30;border-radius:12px;
                                padding:10px 16px;margin-bottom:6px;display:flex;align-items:center;gap:14px;">
                        <span style="font-size:20px;min-width:32px;">{madalya}</span>
                        <div style="flex:1;">
                            <div style="font-weight:700;color:#e2e8f0;font-size:13px;">
                                {c.get('tam_ad', f"{c.get('ad', '')} {c.get('soyad', '')}")}</div>
                            <div style="font-size:10px;color:#94a3b8;">
                                {c.get('brans', '-')} · {c.get('deneyim_yili', '-')} yil · {c.get('egitim_seviyesi', '-')}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-size:22px;font-weight:900;color:{s_renk};">{skor}</div>
                            <div style="font-size:8px;color:#94a3b8;">UYUM</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ═══ MÜLAKAT STRATEJİSİ ═══
    with sub[1]:
        styled_section("AI Mulakat Soru Uretici")
        if not candidates:
            styled_info_banner("Aday yok.", banner_type="info", icon="📋")
        else:
            c_labels = [c.get("tam_ad", f"{c.get('ad', '')} {c.get('soyad', '')}") for c in candidates]
            secili_c = st.selectbox("Aday Secin", c_labels, key="aia_mulakat_c")
            pozisyon_txt = st.text_input("Pozisyon", placeholder="Matematik Ogretmeni", key="aia_mulakat_poz")

            if st.button("AI Mulakat Sorulari Uret", key="aia_mulakat_btn", type="primary"):
                if secili_c and pozisyon_txt:
                    c = candidates[c_labels.index(secili_c)]
                    try:
                        from utils.smarti_helper import _get_client
                        client = _get_client()
                        if client:
                            profil = f"Aday: {secili_c}, Brans: {c.get('brans', '-')}, Deneyim: {c.get('deneyim_yili', '-')} yil, Egitim: {c.get('egitim_seviyesi', '-')}"
                            with st.spinner("AI mulakat stratejisi olusturuyor..."):
                                resp = client.chat.completions.create(
                                    model="gpt-4o-mini",
                                    messages=[
                                        {"role": "system", "content": "Sen bir okul IK uzmanisin. Adayin profiline gore kisiye ozel 8 mulakat sorusu uret. Her soru icin: soru + neden sorulmali + ideal cevap ipucu. Turkce."},
                                        {"role": "user", "content": f"Pozisyon: {pozisyon_txt}\n{profil}"},
                                    ],
                                    max_tokens=600, temperature=0.7,
                                )
                                ai = resp.choices[0].message.content or ""
                            if ai:
                                st.markdown(f"""
                                <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                            border-radius:14px;padding:16px 20px;">
                                    <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Mulakat Sorulari</div>
                                    <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                                </div>""", unsafe_allow_html=True)
                        else:
                            st.warning("OpenAI API anahtari bulunamadi.")
                    except Exception as e:
                        st.error(f"Hata: {e}")

    # ═══ KARŞILAŞTIRMA ═══
    with sub[2]:
        styled_section("Aday Karsilastirma")
        if len(candidates) < 2:
            styled_info_banner("Karsilastirma icin en az 2 aday gerekli.", banner_type="info", icon="📊")
        else:
            c_labels = [c.get("tam_ad", f"{c.get('ad', '')} {c.get('soyad', '')}") for c in candidates]
            col1, col2 = st.columns(2)
            with col1:
                a1 = st.selectbox("Aday A", c_labels, key="aia_cmp_a")
            with col2:
                a2 = st.selectbox("Aday B", [l for l in c_labels if l != a1] if c_labels else [], key="aia_cmp_b")

            if a1 and a2:
                c1 = candidates[c_labels.index(a1)]
                c2 = candidates[c_labels.index(a2)]

                metrikler = [
                    ("Brans", c1.get("brans", "-"), c2.get("brans", "-")),
                    ("Deneyim", f"{c1.get('deneyim_yili', '-')} yil", f"{c2.get('deneyim_yili', '-')} yil"),
                    ("Egitim", c1.get("egitim_seviyesi", "-"), c2.get("egitim_seviyesi", "-")),
                    ("Durum", c1.get("status", "-"), c2.get("status", "-")),
                ]

                col1, col2, col3 = st.columns([1, 0.2, 1])
                with col1:
                    st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">{a1}</div>', unsafe_allow_html=True)
                    for label, v1, _ in metrikler:
                        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:3px 0;"><span style="font-size:11px;color:#94a3b8;">{label}</span><span style="font-size:12px;font-weight:700;color:#e2e8f0;">{v1}</span></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div style="text-align:center;font-size:28px;padding-top:30px;">vs</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">{a2}</div>', unsafe_allow_html=True)
                    for label, _, v2 in metrikler:
                        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:3px 0;"><span style="font-size:11px;color:#94a3b8;">{label}</span><span style="font-size:12px;font-weight:700;color:#e2e8f0;">{v2}</span></div>', unsafe_allow_html=True)


# ============================================================
# 3. PERSONEL MUTLULUK BAROMETRESİ
# ============================================================

_PULSE_SORULARI = [
    {"id": "is_yuku", "soru": "Is yukunuzu nasil buluyorsunuz?", "ikon": "📋"},
    {"id": "yonetim", "soru": "Yonetiminizden memnun musunuz?", "ikon": "👔"},
    {"id": "deger", "soru": "Kendinizi degerli hissediyor musunuz?", "ikon": "💎"},
    {"id": "denge", "soru": "Is-yasam dengeniz nasil?", "ikon": "⚖️"},
    {"id": "gelecek", "soru": "Bu okulda geleceginizi goruyor musunuz?", "ikon": "🔮"},
]


def _mutluluk_path() -> str:
    return os.path.join(_td(), "ik", "mutluluk_anket.json")


def _load_mutluluk() -> list[dict]:
    return _lj(_mutluluk_path())


def _save_mutluluk(data: list[dict]):
    _sj(_mutluluk_path(), data)


def _veri_bazli_mutluluk(store) -> dict[str, float]:
    """Otomatik endeks (veri bazli)."""
    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    izinler = store.load_list("izinler") if hasattr(store, "load_list") else []
    perf = store.load_list("performance_reviews") if hasattr(store, "load_list") else []
    disiplin = store.load_list("disiplin") if hasattr(store, "load_list") else []
    egitim = store.load_list("egitimler") if hasattr(store, "load_list") else []

    n = max(len(aktif), 1)
    # Izin dengesi (cok az veya cok fazla = kotu)
    izin_kisi = len(set(iz.get("employee_id", iz.get("personel_id", "")) for iz in izinler))
    izin_oran = izin_kisi / n
    izin_puan = 80 if 0.3 <= izin_oran <= 0.7 else 60 if izin_oran < 0.3 else 50

    # Performans trendi
    perf_puanlar = [p.get("puan", p.get("genel_puan", 50)) for p in perf if isinstance(p.get("puan", p.get("genel_puan")), (int, float))]
    perf_puan = round(sum(perf_puanlar) / max(len(perf_puanlar), 1)) if perf_puanlar else 50

    # Disiplin orani
    disiplin_puan = max(0, 100 - len(disiplin) * 10)

    # Egitim katilimi
    egitim_puan = min(len(egitim) * 10, 100)

    return {
        "izin_dengesi": izin_puan,
        "performans": min(perf_puan, 100),
        "disiplin": disiplin_puan,
        "egitim": egitim_puan,
    }


def render_mutluluk_barometresi(store):
    """Personel mutluluk endeksi — veri + anket bazli."""
    styled_section("Mutluluk Barometresi", "#ec4899")
    styled_info_banner(
        "Personel mutlulugunu hem veriye hem anonim ankete dayanarak olcun. "
        "Mutsuz personel ayrilmadan once mudahale edin.",
        banner_type="info", icon="😊")

    anketler = _load_mutluluk()
    veri_skor = _veri_bazli_mutluluk(store)

    # Veri bazli genel
    veri_ort = round(sum(veri_skor.values()) / max(len(veri_skor), 1), 1)

    # Anket bazli genel
    if anketler:
        tum_puanlar = []
        for a in anketler:
            for s in _PULSE_SORULARI:
                p = a.get("cevaplar", {}).get(s["id"], 0)
                if p > 0:
                    tum_puanlar.append(p)
        anket_ort = round(sum(tum_puanlar) / max(len(tum_puanlar), 1) / 5 * 100, 1) if tum_puanlar else 0
    else:
        anket_ort = 0

    # Bilesik
    genel = round((veri_ort * 0.4 + anket_ort * 0.6) if anket_ort > 0 else veri_ort, 1)
    g_renk = "#10b981" if genel >= 70 else "#f59e0b" if genel >= 50 else "#ef4444"

    # ── HERO TERMOMETRE ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#831843 0%,#9d174d 100%);
                border:2px solid {g_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {g_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fda4af;letter-spacing:3px;text-transform:uppercase;">Personel Mutluluk Endeksi</div>
        <div style="font-size:64px;font-weight:900;color:{g_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{genel}</div>
        <div style="font-size:12px;color:#fda4af;">
            Veri bazli: {veri_ort} · Anket bazli: {anket_ort if anket_ort > 0 else 'Henuz yok'} · {len(anketler)} anket</div>
        <div style="margin:16px auto 0;max-width:300px;">
            <div style="background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);
                        border-radius:6px;height:12px;position:relative;">
                <div style="position:absolute;left:{min(genel, 100)}%;top:-3px;transform:translateX(-50%);
                            width:4px;height:18px;background:#fff;border-radius:2px;box-shadow:0 0 8px #fff;"></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Veri bazli alt puanlar
    styled_section("Veri Bazli Gostergeler")
    _veri_labels = {"izin_dengesi": ("Izin Dengesi", "🏖️"), "performans": ("Performans Trendi", "⭐"),
                     "disiplin": ("Disiplin Sagligi", "📝"), "egitim": ("Egitim Katilimi", "🎓")}
    for key, val in veri_skor.items():
        label, ikon = _veri_labels.get(key, (key, "📋"))
        renk = "#10b981" if val >= 70 else "#f59e0b" if val >= 50 else "#ef4444"
        bar_w = min(val, 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:14px;">{ikon}</span>
            <span style="min-width:130px;font-size:12px;color:#e2e8f0;font-weight:600;">{label}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                    <span style="font-size:9px;color:#fff;font-weight:700;">{val}</span></div></div>
        </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📝 Pulse Anket", "📊 Anket Sonuclari"])

    # ═══ PULSE ANKET ═══
    with sub[0]:
        styled_section("Anonim Pulse Anket (Aylik)")
        with st.form("mutluluk_form"):
            st.caption("Yanitlariniz tamamen anonimdir.")
            cevaplar = {}
            for s in _PULSE_SORULARI:
                cevaplar[s["id"]] = st.slider(f"{s['ikon']} {s['soru']}", 1, 5, 3, key=f"mut_{s['id']}")

            serbest = st.text_area("Ek yorum (istege bagli, anonim)", height=60, key="mut_yorum")

            if st.form_submit_button("Gonder (Anonim)", type="primary"):
                yeni = {
                    "id": f"ma_{uuid.uuid4().hex[:8]}",
                    "cevaplar": cevaplar,
                    "yorum": serbest,
                    "tarih": date.today().isoformat(),
                    "ay": date.today().strftime("%Y-%m"),
                }
                anketler.append(yeni)
                _save_mutluluk(anketler)
                st.success("Anket anonim olarak kaydedildi!")
                st.rerun()

    # ═══ ANKET SONUÇLARI ═══
    with sub[1]:
        styled_section("Pulse Anket Sonuclari")
        if not anketler:
            styled_info_banner("Henuz anket yaniti yok.", banner_type="info", icon="📊")
        else:
            # Soru bazli ortalama
            for s in _PULSE_SORULARI:
                puanlar = [a.get("cevaplar", {}).get(s["id"], 0) for a in anketler if a.get("cevaplar", {}).get(s["id"], 0) > 0]
                ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0
                bar_w = round(ort / 5 * 100)
                renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <span style="font-size:14px;">{s['ikon']}</span>
                    <span style="min-width:200px;font-size:11px;color:#e2e8f0;">{s['soru']}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{ort}/5</span></div></div>
                </div>""", unsafe_allow_html=True)

            # Serbest yorumlar
            yorumlar = [a.get("yorum", "") for a in anketler if a.get("yorum", "").strip()]
            if yorumlar:
                styled_section("Anonim Yorumlar")
                for y in yorumlar[-10:]:
                    st.markdown(f"""
                    <div style="background:#0f172a;border-left:3px solid #ec4899;border-radius:0 8px 8px 0;
                                padding:8px 12px;margin-bottom:4px;font-size:11px;color:#fda4af;font-style:italic;">
                        "{y}"</div>""", unsafe_allow_html=True)
