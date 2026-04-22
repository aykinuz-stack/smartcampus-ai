"""
Insan Kaynaklari — ULTRA MEGA Ozellikleri
===========================================
1. Personel Kariyer Yol Haritasi + AI Mentorluk
2. Canli Performans Duvari (Gamification Leaderboard)
3. IK Stratejik Simulasyon Odasi (HR War Game)
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
# 1. KARİYER YOL HARİTASI + AI MENTORLUK
# ============================================================

_KARIYER_AGACI = {
    "Ogretmen": ["Bolum Baskani", "Koordinator"],
    "Bolum Baskani": ["Mudur Yardimcisi", "Koordinator"],
    "Koordinator": ["Mudur Yardimcisi"],
    "Mudur Yardimcisi": ["Mudur"],
    "Mudur": [],
    "Uzman": ["Koordinator", "Mudur Yardimcisi"],
    "Stajyer": ["Ogretmen"],
    "Asistan": ["Ogretmen", "Uzman"],
}

_TERFI_GEREKSINIMLERI = {
    "Bolum Baskani": {"liderlik": 4, "teknik": 4, "pedagojik": 4, "min_deneyim": 5},
    "Koordinator": {"liderlik": 4, "sosyal": 4, "dijital": 3, "min_deneyim": 4},
    "Mudur Yardimcisi": {"liderlik": 5, "sosyal": 5, "kisisel": 4, "min_deneyim": 8},
    "Mudur": {"liderlik": 5, "sosyal": 5, "kisisel": 5, "teknik": 4, "min_deneyim": 12},
}


def render_kariyer_yol(store):
    """Kariyer yol haritasi + AI mentorluk motoru."""
    styled_section("Kariyer Yol Haritasi", "#6d28d9")
    styled_info_banner(
        "Her personelin gelecek kariyer yolunu planlayin. "
        "Gerekli yetkinlikler + eksikler + AI gelisim plani + mentor eslestirme.",
        banner_type="info", icon="🗺️")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    yetenekler = _lj(os.path.join(_td(), "ik", "yetenek_haritasi.json"))
    yt_map = {y["employee_id"]: y.get("puanlar", {}) for y in yetenekler}

    if not aktif:
        styled_info_banner("Aktif calisan yok.", banner_type="warning", icon="⚠️")
        return

    sub = st.tabs(["🗺️ Kariyer Plani", "🤝 Mentor Eslestirme", "🤖 AI Gelisim"])

    # ═══ KARİYER PLANI ═══
    with sub[0]:
        emp_labels = [f"{e.get('name', '')} {e.get('surname', '')} — {e.get('position', '')}" for e in aktif]
        secili = st.selectbox("Personel Secin", [""] + emp_labels, key="ky_sec")

        if secili:
            idx = emp_labels.index(secili)
            emp = aktif[idx]
            mevcut_poz = emp.get("position", "Ogretmen")
            eid = emp.get("id", "")
            puanlar = yt_map.get(eid, {})

            # Olasi terfi yollari
            yollar = _KARIYER_AGACI.get(mevcut_poz, _KARIYER_AGACI.get("Ogretmen", []))

            # Mevcut pozisyon karti
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #6d28d9;border-radius:16px;
                        padding:18px;text-align:center;margin-bottom:14px;">
                <div style="font-size:10px;color:#a78bfa;letter-spacing:2px;">MEVCUT POZISYON</div>
                <div style="font-size:24px;font-weight:900;color:#fff;margin:6px 0;">{mevcut_poz}</div>
                <div style="font-size:11px;color:#94a3b8;">{emp.get('name', '')} {emp.get('surname', '')}</div>
            </div>""", unsafe_allow_html=True)

            if not yollar:
                st.success("Bu pozisyon en ust seviyededir!")
            else:
                styled_section("Olasi Kariyer Yollari")
                for hedef_poz in yollar:
                    gereksinimler = _TERFI_GEREKSINIMLERI.get(hedef_poz, {})
                    min_den = gereksinimler.pop("min_deneyim", 0) if "min_deneyim" in gereksinimler else 0

                    # Eksik yetkinlikler
                    eksikler = []
                    tamam = []
                    for yk_key, gerekli in gereksinimler.items():
                        mevcut = puanlar.get(yk_key, 0)
                        if mevcut < gerekli:
                            eksikler.append({"alan": yk_key, "mevcut": mevcut, "gerekli": gerekli})
                        else:
                            tamam.append({"alan": yk_key, "mevcut": mevcut, "gerekli": gerekli})

                    hazirlik = round(len(tamam) / max(len(tamam) + len(eksikler), 1) * 100)
                    h_renk = "#10b981" if hazirlik >= 80 else "#f59e0b" if hazirlik >= 50 else "#ef4444"

                    eksik_html = ""
                    for e in eksikler:
                        eksik_html += (f'<span style="background:#ef444420;color:#ef4444;padding:2px 8px;'
                                       f'border-radius:4px;font-size:9px;font-weight:700;margin:2px;">'
                                       f'{e["alan"]}: {e["mevcut"]}→{e["gerekli"]}</span>')
                    tamam_html = ""
                    for t in tamam:
                        tamam_html += (f'<span style="background:#10b98120;color:#10b981;padding:2px 8px;'
                                       f'border-radius:4px;font-size:9px;font-weight:700;margin:2px;">'
                                       f'{t["alan"]}: {t["mevcut"]} ✓</span>')

                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid {h_renk}40;border-left:5px solid {h_renk};
                                border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <div>
                                <span style="font-size:16px;font-weight:800;color:#fff;">→ {hedef_poz}</span>
                                <span style="font-size:10px;color:#94a3b8;margin-left:8px;">Min {min_den} yil deneyim</span>
                            </div>
                            <span style="background:{h_renk}20;color:{h_renk};padding:4px 14px;border-radius:8px;
                                        font-size:12px;font-weight:800;">%{hazirlik} Hazir</span>
                        </div>
                        <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;margin-bottom:8px;">
                            <div style="width:{hazirlik}%;height:100%;background:{h_renk};border-radius:4px;"></div>
                        </div>
                        <div style="margin-bottom:4px;">
                            <span style="font-size:9px;color:#64748b;">Tamamlanan:</span> {tamam_html or '<span style="font-size:9px;color:#64748b;">—</span>'}
                        </div>
                        <div>
                            <span style="font-size:9px;color:#64748b;">Eksik:</span> {eksik_html or '<span style="font-size:9px;color:#10b981;font-size:9px;">Yok ✓</span>'}
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ═══ MENTOR EŞLEŞTİRME ═══
    with sub[1]:
        styled_section("Otomatik Mentor Eslestirme")
        styled_info_banner(
            "Yuksek yetkinlikli personeli dusuk yetkinlikli personelle eslestirir.",
            banner_type="info", icon="🤝")

        if not yetenekler or len(yetenekler) < 2:
            styled_info_banner("Eslestirme icin en az 2 yetkinlik degerlendirmesi gerekli.", banner_type="warning", icon="📊")
        else:
            # En yuksek ve en dusuk yetkinlikli
            skor_list = []
            for y in yetenekler:
                puanlar_d = y.get("puanlar", {})
                ort = sum(puanlar_d.values()) / max(len(puanlar_d), 1) if puanlar_d else 0
                emp = next((e for e in aktif if e.get("id") == y.get("employee_id")), None)
                if emp:
                    skor_list.append({"emp": emp, "ort": round(ort, 1), "puanlar": puanlar_d})

            skor_list.sort(key=lambda x: -x["ort"])
            mentorlar = skor_list[:max(len(skor_list) // 3, 1)]
            mentiler = skor_list[-max(len(skor_list) // 3, 1):]

            for mi, menti in enumerate(mentiler):
                mentor = mentorlar[mi % len(mentorlar)]
                m_ad = f"{mentor['emp'].get('name', '')} {mentor['emp'].get('surname', '')}"
                t_ad = f"{menti['emp'].get('name', '')} {menti['emp'].get('surname', '')}"

                # En buyuk gap
                gaps = []
                for k in menti["puanlar"]:
                    m_val = mentor["puanlar"].get(k, 0)
                    t_val = menti["puanlar"].get(k, 0)
                    if m_val > t_val + 1:
                        gaps.append(f"{k}(+{round(m_val - t_val, 1)})")

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #6d28d930;border-radius:12px;
                            padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:14px;">
                    <div style="text-align:center;min-width:100px;">
                        <div style="font-size:12px;font-weight:700;color:#10b981;">{m_ad}</div>
                        <div style="font-size:9px;color:#64748b;">Mentor ({mentor['ort']})</div>
                    </div>
                    <div style="font-size:20px;color:#6d28d9;">→</div>
                    <div style="text-align:center;min-width:100px;">
                        <div style="font-size:12px;font-weight:700;color:#f59e0b;">{t_ad}</div>
                        <div style="font-size:9px;color:#64748b;">Menti ({menti['ort']})</div>
                    </div>
                    <div style="flex:1;font-size:9px;color:#94a3b8;">
                        Odak: {', '.join(gaps[:3]) or 'Genel gelisim'}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ AI GELİŞİM PLANI ═══
    with sub[2]:
        styled_section("AI Kisisel Gelisim Plani")
        if not aktif:
            return
        emp_labels2 = [f"{e.get('name', '')} {e.get('surname', '')}" for e in aktif]
        secili2 = st.selectbox("Personel", emp_labels2, key="ky_ai_sec")

        if st.button("AI Gelisim Plani Olustur", key="ky_ai_btn", type="primary"):
            emp = aktif[emp_labels2.index(secili2)]
            eid = emp.get("id", "")
            puanlar = yt_map.get(eid, {})
            poz = emp.get("position", "")
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    veri = f"Personel: {secili2}, Pozisyon: {poz}, Yetkinlikler: {puanlar or 'Degerlendirme yok'}"
                    with st.spinner("AI gelisim plani hazirlaniyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul IK gelisim uzmanisin. Personelin yetkinlik verilerine gore 3 aylik kisisel gelisim plani olustur: 1) Guclu yonler 2) Gelisim alanlari 3) Haftalik micro-hedefler 4) Onerilen egitimler 5) Kariyer hedefi. Turkce."},
                                {"role": "user", "content": veri},
                            ],
                            max_tokens=600, temperature=0.7,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#3b0764,#6d28d9);border:1px solid #a78bfa;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Kisisel Gelisim Plani</div>
                            <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")


# ============================================================
# 2. CANLI PERFORMANS DUVARI (GAMIFICATION)
# ============================================================

_PUAN_KAYNAKLARI = {
    "not_girisi": {"puan": 2, "label": "Not Girisi", "ikon": "📝"},
    "sinav": {"puan": 10, "label": "Sinav Hazirladi", "ikon": "📋"},
    "kazanim": {"puan": 3, "label": "Kazanim Isledi", "ikon": "🎯"},
    "toplanti": {"puan": 5, "label": "Toplanti Katildi", "ikon": "🤝"},
    "nobet": {"puan": 5, "label": "Nobet Tuttu", "ikon": "🛡️"},
    "egitim": {"puan": 15, "label": "Egitime Katildi", "ikon": "🎓"},
    "etkinlik": {"puan": 20, "label": "Etkinlik Duzenledi", "ikon": "🎭"},
    "gorusme": {"puan": 8, "label": "Veli Gorusmesi", "ikon": "👪"},
    "gecikme": {"puan": -5, "label": "Gecikme/Devamsizlik", "ikon": "⏰"},
    "disiplin": {"puan": -20, "label": "Disiplin Kaydi", "ikon": "⚠️"},
}

_ROZETLER = [
    {"id": "not_100", "ad": "100 Not Ustasi", "ikon": "🏆", "kosul": "not_girisi >= 100"},
    {"id": "etkinlik_10", "ad": "Etkinlik Yildizi", "ikon": "🎭", "kosul": "etkinlik >= 10"},
    {"id": "sifir_gecikme", "ad": "Dakik Profesyonel", "ikon": "🎯", "kosul": "gecikme == 0"},
    {"id": "egitim_5", "ad": "Ogrenme Tutkunu", "ikon": "📚", "kosul": "egitim >= 5"},
    {"id": "toplanti_20", "ad": "Takim Oyuncusu", "ikon": "🤝", "kosul": "toplanti >= 20"},
]


def _hesapla_personel_puanlari(aktif: list, store) -> list[dict]:
    """Her personel icin tum modullerden puan hesapla."""
    td = _td()
    ak = _ak_dir()

    notlar = _lj(os.path.join(ak, "grades.json"))
    kazanim = _lj(os.path.join(ak, "kazanim_isleme.json"))
    nobet = _lj(os.path.join(ak, "nobet_kayitlar.json"))
    schedule = _lj(os.path.join(ak, "schedule.json"))

    izinler = store.load_list("izinler") if hasattr(store, "load_list") else []
    disiplin = store.load_list("disiplin") if hasattr(store, "load_list") else []
    egitimler = store.load_list("egitimler") if hasattr(store, "load_list") else []
    perf = store.load_list("performance_reviews") if hasattr(store, "load_list") else []

    try:
        from models.toplanti_kurullar import ToplantiDataStore
        top = ToplantiDataStore(os.path.join(td, "toplanti"))
        katilimcilar = top.load_list("participants") if hasattr(top, "load_list") else []
    except Exception:
        katilimcilar = []

    sonuclar = []
    for emp in aktif:
        ad = f"{emp.get('name', '')} {emp.get('surname', '')}".strip().lower()
        eid = emp.get("id", "")

        sayaclar = {
            "not_girisi": sum(1 for n in notlar if ad in (n.get("ogretmen_adi", "") or "").lower()),
            "kazanim": sum(1 for k in kazanim if ad in (k.get("ogretmen_adi", "") or "").lower()),
            "nobet": sum(1 for n in nobet if ad in (n.get("ogretmen_adi", "") or "").lower()),
            "toplanti": sum(1 for p in katilimcilar if ad in (p.get("ad_soyad", p.get("name", "")) or "").lower()),
            "egitim": sum(1 for e in egitimler if e.get("employee_id") == eid),
            "gecikme": sum(1 for iz in izinler if (iz.get("employee_id", iz.get("personel_id", "")) == eid)),
            "disiplin": sum(1 for d in disiplin if d.get("employee_id") == eid),
            "sinav": 0,
            "etkinlik": 0,
            "gorusme": 0,
        }

        toplam = 0
        for key, sayi in sayaclar.items():
            pk = _PUAN_KAYNAKLARI.get(key, {}).get("puan", 0)
            toplam += sayi * pk

        # Rozetler
        rozetler = []
        for r in _ROZETLER:
            try:
                if eval(r["kosul"], {"__builtins__": {}}, sayaclar):
                    rozetler.append(r)
            except Exception:
                pass

        sonuclar.append({
            "emp": emp, "puan": max(toplam, 0), "sayaclar": sayaclar, "rozetler": rozetler,
        })

    sonuclar.sort(key=lambda x: -x["puan"])
    return sonuclar


def render_performans_duvari(store):
    """Canli performans duvari — gamification leaderboard."""
    styled_section("Performans Duvari", "#f59e0b")
    styled_info_banner(
        "Tum modullerdeki katkilara dayali canli siralama. "
        "Puan + rozet + Ayin Personeli otomatik secim.",
        banner_type="info", icon="🏆")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]

    if not aktif:
        styled_info_banner("Aktif calisan yok.", banner_type="warning", icon="⚠️")
        return

    _cache = "ik_perf_duvar"
    if _cache not in st.session_state:
        with st.spinner("Performans puanlari hesaplaniyor..."):
            st.session_state[_cache] = _hesapla_personel_puanlari(aktif, store)
    sonuclar = st.session_state[_cache]

    if st.button("Verileri Yenile", key="pd_yenile"):
        st.session_state.pop(_cache, None)
        st.rerun()

    # Ayin personeli
    if sonuclar:
        ayin = sonuclar[0]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#78350f,#92400e);border:3px solid #fbbf24;
                    border-radius:20px;padding:20px;text-align:center;margin-bottom:16px;
                    box-shadow:0 8px 32px rgba(251,191,36,0.3);">
            <div style="font-size:40px;">👑</div>
            <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">Ayin Personeli</div>
            <div style="font-size:24px;font-weight:900;color:#fbbf24;margin:6px 0;">
                {ayin['emp'].get('name', '')} {ayin['emp'].get('surname', '')}</div>
            <div style="font-size:12px;color:#fde68a;">{ayin['emp'].get('position', '')} · {ayin['puan']} puan</div>
            <div style="margin-top:6px;">{''.join(r['ikon'] for r in ayin['rozetler'][:5])}</div>
        </div>""", unsafe_allow_html=True)

    # Leaderboard
    styled_section("Siralama")
    en_yuksek = sonuclar[0]["puan"] if sonuclar else 1
    for sira, s in enumerate(sonuclar[:20], 1):
        madalya = {1: "🥇", 2: "🥈", 3: "🥉"}.get(sira, f"#{sira}")
        bar_w = round(s["puan"] / max(en_yuksek, 1) * 100)
        renk = "#fbbf24" if sira <= 3 else "#6366f1"
        rozet_html = " ".join(r["ikon"] for r in s["rozetler"][:3])

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {renk}30;border-radius:12px;
                    padding:10px 16px;margin-bottom:6px;display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;min-width:32px;text-align:center;">{madalya}</span>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:13px;">
                        {s['emp'].get('name', '')} {s['emp'].get('surname', '')}</span>
                    <div style="display:flex;gap:4px;align-items:center;">
                        <span style="font-size:12px;">{rozet_html}</span>
                        <span style="font-size:18px;font-weight:900;color:{renk};">{s['puan']}</span>
                    </div>
                </div>
                <div style="font-size:9px;color:#64748b;margin-top:2px;">
                    {s['emp'].get('position', '')} · Not:{s['sayaclar']['not_girisi']} Kaz:{s['sayaclar']['kazanim']} Top:{s['sayaclar']['toplanti']}</div>
                <div style="margin-top:4px;background:#1e293b;border-radius:3px;height:4px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;"></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Puan kaynaklari aciklama
    with st.expander("Puan Kaynaklari", expanded=False):
        for key, info in _PUAN_KAYNAKLARI.items():
            renk = "#10b981" if info["puan"] > 0 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
                <span style="font-size:14px;">{info['ikon']}</span>
                <span style="flex:1;font-size:11px;color:#e2e8f0;">{info['label']}</span>
                <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
                            font-size:11px;font-weight:800;">{'+'if info['puan']>0 else ''}{info['puan']}/islem</span>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 3. İK STRATEJİK SİMÜLASYON ODASI
# ============================================================

def render_hr_simulasyon(store):
    """IK stratejik simulasyon — Ya ... olursa?"""
    styled_section("IK Stratejik Simulasyon", "#dc2626")
    styled_info_banner(
        "IK kararlarinin etkisini simule edin. "
        "Personel ayrilmasi, maas artisi, yeni sube — hepsinin sonucunu gorun.",
        banner_type="warning", icon="🎮")

    employees = store.load_list("employees") if hasattr(store, "load_list") else []
    aktif = [e for e in employees if e.get("status") == "Aktif"]
    bordro = store.load_list("maas_bordro") if hasattr(store, "load_list") else []
    positions = store.load_list("positions") if hasattr(store, "load_list") else []

    aktif_sayi = len(aktif)
    # Ortalama maas tahmini
    maas_list = [b.get("net_maas", b.get("brut_maas", 0)) for b in bordro
                  if isinstance(b.get("net_maas", b.get("brut_maas")), (int, float)) and b.get("net_maas", b.get("brut_maas", 0)) > 0]
    ort_maas = round(sum(maas_list) / max(len(maas_list), 1)) if maas_list else 25000
    aylik_toplam = ort_maas * aktif_sayi

    # Ogrenci/ogretmen orani
    ogrenciler = _lj(os.path.join(_ak_dir(), "students.json"))
    aktif_ogr = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")
    ogretmen_sayi = sum(1 for e in aktif if e.get("branch") or e.get("brans"))
    oran = round(aktif_ogr / max(ogretmen_sayi, 1), 1)

    senaryo = st.selectbox("Senaryo Secin", [
        "👥 Personel Ayrilmasi",
        "💰 Maas Artisi",
        "🏫 Yeni Sube / Kadro Genisletme",
        "🎓 Egitim Butcesi Artisi",
        "🔮 Serbest Senaryo (AI)",
    ], key="hrs_sec")

    st.divider()

    # ═══ PERSONEL AYRILMASI ═══
    if "Ayrilma" in senaryo:
        styled_section("Personel Ayrilma Simulasyonu")
        ayrilan = st.slider("Kac personel ayrilirsa?", 1, min(20, aktif_sayi), 3, key="hrs_ayr")

        # Departman bazli etki
        dept_sayac = Counter(e.get("branch", e.get("department", "Genel")) for e in aktif)
        en_kalabalik = dept_sayac.most_common(1)[0] if dept_sayac else ("?", 0)

        maliyet_tasarrufu = ayrilan * ort_maas * 12
        yeni_ise_alim_maliyeti = ayrilan * ort_maas * 3  # 3 aylik maas = ise alim maliyeti
        yeni_oran = round(aktif_ogr / max(ogretmen_sayi - ayrilan, 1), 1)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #3b82f6;border-radius:14px;padding:16px;text-align:center;">
                <div style="font-size:10px;color:#64748b;">MEVCUT</div>
                <div style="font-size:28px;font-weight:900;color:#3b82f6;">{aktif_sayi}</div>
                <div style="font-size:10px;color:#94a3b8;">personel · oran: {oran}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            yeni_renk = "#ef4444" if yeni_oran > 20 else "#f59e0b"
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {yeni_renk};border-radius:14px;padding:16px;text-align:center;">
                <div style="font-size:10px;color:#64748b;">SONRA</div>
                <div style="font-size:28px;font-weight:900;color:{yeni_renk};">{aktif_sayi - ayrilan}</div>
                <div style="font-size:10px;color:#94a3b8;">personel · oran: {yeni_oran}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#1e293b;border-radius:12px;padding:14px;margin-top:12px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                <div><div style="font-size:10px;color:#64748b;">Maas Tasarrufu (Yillik)</div>
                    <div style="font-size:18px;font-weight:800;color:#10b981;">{maliyet_tasarrufu:,.0f} TL</div></div>
                <div><div style="font-size:10px;color:#64748b;">Ise Alim Maliyeti</div>
                    <div style="font-size:18px;font-weight:800;color:#ef4444;">{yeni_ise_alim_maliyeti:,.0f} TL</div></div>
                <div><div style="font-size:10px;color:#64748b;">Ogr/Ogt Orani</div>
                    <div style="font-size:18px;font-weight:800;color:{yeni_renk};">{yeni_oran}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if yeni_oran > 18:
            st.error(f"⚠️ Oran {yeni_oran} — ek ogretmen gerekli! {ayrilan} kisi ayrilirsa ders aksayabilir.")

    # ═══ MAAŞ ARTIŞI ═══
    elif "Maas" in senaryo:
        styled_section("Maas Artis Simulasyonu")
        artis = st.slider("Maas Artis Orani (%)", 0, 50, 15, 5, key="hrs_maas")

        yeni_aylik = round(aylik_toplam * (1 + artis / 100))
        yillik_fark = (yeni_aylik - aylik_toplam) * 12

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:14px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                <div><div style="font-size:10px;color:#64748b;">Mevcut Aylik</div>
                    <div style="font-size:18px;font-weight:800;color:#3b82f6;">{aylik_toplam:,.0f} TL</div></div>
                <div><div style="font-size:10px;color:#64748b;">Yeni Aylik (+%{artis})</div>
                    <div style="font-size:18px;font-weight:800;color:#f59e0b;">{yeni_aylik:,.0f} TL</div></div>
                <div><div style="font-size:10px;color:#64748b;">Yillik Ek Maliyet</div>
                    <div style="font-size:18px;font-weight:800;color:#ef4444;">{yillik_fark:,.0f} TL</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Mutluluk tahmini
        mutluluk_artis = min(artis * 0.8, 25)
        st.markdown(f"""
        <div style="background:#052e16;border:1px solid #10b981;border-radius:10px;padding:10px 14px;margin-top:8px;">
            <span style="font-size:12px;color:#6ee7b7;">Tahmini Mutluluk Artisi: <b>+%{mutluluk_artis:.0f}</b> · Turnover Riski: <b>-%{min(artis * 1.5, 40):.0f}</b></span>
        </div>""", unsafe_allow_html=True)

    # ═══ YENİ ŞUBE ═══
    elif "Sube" in senaryo:
        styled_section("Yeni Sube / Kadro Genisletme")
        ek_ogrenci = st.slider("Beklenen Ek Ogrenci", 0, 300, 100, 10, key="hrs_sube")

        gerekli_ogretmen = round(ek_ogrenci / max(oran, 12))
        gerekli_diger = round(gerekli_ogretmen * 0.3)  # Idari personel
        toplam_gerekli = gerekli_ogretmen + gerekli_diger
        ek_maliyet = toplam_gerekli * ort_maas * 12

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #0891b2;border-radius:12px;padding:14px;">
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center;">
                <div><div style="font-size:10px;color:#64748b;">Ek Ogrenci</div>
                    <div style="font-size:22px;font-weight:800;color:#0891b2;">{ek_ogrenci}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Gerekli Ogretmen</div>
                    <div style="font-size:22px;font-weight:800;color:#2563eb;">{gerekli_ogretmen}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Idari Personel</div>
                    <div style="font-size:22px;font-weight:800;color:#7c3aed;">{gerekli_diger}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Yillik Maliyet</div>
                    <div style="font-size:22px;font-weight:800;color:#ef4444;">{ek_maliyet:,.0f} TL</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ═══ EĞİTİM BÜTÇESİ ═══
    elif "Egitim" in senaryo:
        styled_section("Egitim Butcesi Artis Simulasyonu")
        carpan = st.slider("Butce Carpani", 1.0, 5.0, 2.0, 0.5, key="hrs_egitim")
        mevcut_egitim = len(store.load_list("egitimler") if hasattr(store, "load_list") else [])
        tahmini_yeni = round(mevcut_egitim * carpan)

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #059669;border-radius:12px;padding:14px;">
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
                <div><div style="font-size:10px;color:#64748b;">Mevcut Egitim</div>
                    <div style="font-size:22px;font-weight:800;color:#059669;">{mevcut_egitim}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Tahmini (x{carpan})</div>
                    <div style="font-size:22px;font-weight:800;color:#10b981;">{tahmini_yeni}</div></div>
                <div><div style="font-size:10px;color:#64748b;">Yetkinlik Artisi</div>
                    <div style="font-size:22px;font-weight:800;color:#f59e0b;">+%{round((carpan - 1) * 15)}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ═══ SERBEST SENARYO (AI) ═══
    elif "Serbest" in senaryo:
        styled_section("AI Serbest Senaryo")
        soru = st.text_area("Senaryonuzu yazin...", key="hrs_ai_soru", height=100,
                             placeholder="Ornek: Tum ogretmenlere haftada 1 gun evden calisma versek ne olur?")
        if st.button("Simule Et", key="hrs_ai_btn", type="primary"):
            if soru:
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if client:
                        veri = (f"Aktif: {aktif_sayi}, Ogretmen: {ogretmen_sayi}, Ogrenci: {aktif_ogr}, "
                                f"Oran: {oran}, Ort Maas: {ort_maas:,.0f} TL, Pozisyon: {len(positions)}")
                        with st.spinner("AI simule ediyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul IK stratejik danisman. Verilen IK verilerine dayanarak senaryo analizi yap. Olasi sonuclari, riskleri, maliyetleri ve onerileri Turkce maddeler halinde sun."},
                                    {"role": "user", "content": f"Senaryo: {soru}\n\nOkul IK Verileri: {veri}"},
                                ],
                                max_tokens=600, temperature=0.7,
                            )
                            ai = resp.choices[0].message.content or ""
                        if ai:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border:1px solid #ef4444;
                                        border-radius:14px;padding:16px 20px;">
                                <div style="font-size:12px;color:#fca5a5;font-weight:700;margin-bottom:6px;">AI Senaryo Analizi</div>
                                <div style="font-size:12px;color:#fecaca;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("OpenAI API bulunamadi.")
                except Exception as e:
                    st.error(f"Hata: {e}")
