"""
Kurumsal Organizasyon — MEGA Ozellikleri
=========================================
1. Paydas 360 CRM (Kisi bazli tum etkilesim haritasi)
2. Akilli Kurum Hafizasi (Knowledge Base + AI Search)
3. Stratejik OKR Takip Sistemi
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


def _ld(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. PAYDAŞ 360° CRM
# ============================================================

def _toplam_veli_listesi() -> list[dict]:
    """Tum velileri birlesik liste olarak topla."""
    veliler: dict[str, dict] = {}  # key: veli_adi (normalize)
    td = _td()
    ak = _ak_dir()

    # 1. Akademik ogrencilerden veli bilgisi
    students = _lj(os.path.join(ak, "students.json"))
    for s in students:
        veli = s.get("veli_ad", s.get("veli_adi", ""))
        if not veli:
            continue
        key = veli.strip().lower()
        if key not in veliler:
            veliler[key] = {
                "ad": veli.strip(), "telefon": s.get("veli_tel", s.get("veli_telefon", "")),
                "email": s.get("veli_email", s.get("veli_eposta", "")),
                "cocuklar": [], "tip": "veli",
            }
        veliler[key]["cocuklar"].append({
            "ad": f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
            "sinif": f"{s.get('sinif', '')}-{s.get('sube', '')}",
            "id": s.get("id", ""),
        })

    # 2. Kayit modulunden adaylar
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        for a in adaylar:
            veli = a.veli_adi
            if not veli:
                continue
            key = veli.strip().lower()
            if key not in veliler:
                veliler[key] = {
                    "ad": veli.strip(), "telefon": a.veli_telefon, "email": a.veli_email,
                    "cocuklar": [], "tip": "aday_veli",
                }
            # Aday bilgilerini ekle
            veliler[key].setdefault("kayit_adaylari", []).append({
                "ogrenci": a.ogrenci_adi, "asama": a.asama, "kademe": a.kademe,
                "arama": a.arama_sayisi, "gorusme": a.gorusme_sayisi, "id": a.id,
            })
    except Exception:
        pass

    return list(veliler.values())


def _kisi_etkilesimleri(kisi_adi: str) -> dict:
    """Bir kisi icin tum modullerdeki etkilesimleri topla."""
    td = _td()
    ak = _ak_dir()
    q = kisi_adi.strip().lower()
    sonuc: dict[str, list] = {}

    # 1. Randevular
    try:
        from models.randevu_ziyaretci import RZYDataStore
        rzy = RZYDataStore(os.path.join(td, "randevu"))
        for r in rzy.load_list("randevular") if hasattr(rzy, "load_list") else []:
            if q in (r.get("ziyaretci_adi", "") or "").lower():
                sonuc.setdefault("randevu", []).append({
                    "tarih": r.get("tarih", ""), "konu": r.get("konu", ""),
                    "durum": r.get("durum", ""), "tip": r.get("randevu_turu", ""),
                })
    except Exception:
        pass

    # 2. Sikayetler
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
    for s in sikayetler:
        if q in (s.get("bildiren", "") or "").lower() or q in (s.get("konu", "") or "").lower():
            sonuc.setdefault("sikayet", []).append({
                "tarih": (s.get("created_at", "") or "")[:10], "konu": s.get("konu", ""),
                "durum": s.get("durum", ""), "kategori": s.get("kategori", ""),
            })

    # 3. Rehberlik gorusmeleri
    try:
        from models.rehberlik import RehberlikDataStore
        reh = RehberlikDataStore(os.path.join(td, "rehberlik"))
        for g in reh.load_list("aile_gorusmeleri") if hasattr(reh, "load_list") else []:
            if q in (g.get("veli_adi", "") or "").lower():
                sonuc.setdefault("rehberlik", []).append({
                    "tarih": g.get("tarih", ""), "konu": g.get("gorusme_konusu", ""),
                    "gorusen": g.get("gorusen", ""),
                })
    except Exception:
        pass

    # 4. Memnuniyet anketi
    cevaplar = _lj(os.path.join(td, "veli_anket", "cevaplar.json"))
    for c in cevaplar:
        if q in (c.get("veli_adi", c.get("ad", "")) or "").lower():
            sonuc.setdefault("anket", []).append({
                "tarih": (c.get("created_at", "") or "")[:10],
                "puan": c.get("puan", 0), "kategori": c.get("kategori", ""),
            })

    # 5. Kayit gorusmeleri (HIT)
    gorusmeler = _lj(os.path.join(td, "pr01_gorusme_kayitlari.json"))
    for g in gorusmeler:
        if q in (g.get("Aday", "") or "").lower():
            sonuc.setdefault("kayit_gorusme", []).append({
                "tarih": g.get("Tarih", ""), "sonuc": g.get("Sonuc", ""),
                "kampanya": g.get("Kampanya", ""),
            })

    # 6. Toplanti katilimi
    try:
        from models.toplanti_kurullar import ToplantiDataStore
        top = ToplantiDataStore(os.path.join(td, "toplanti"))
        for p in top.load_list("participants") if hasattr(top, "load_list") else []:
            if q in (p.get("ad_soyad", p.get("name", "")) or "").lower():
                sonuc.setdefault("toplanti", []).append({
                    "toplanti_id": p.get("meeting_id", ""),
                    "katilim": p.get("katilim", ""),
                })
    except Exception:
        pass

    return sonuc


def _kisi_skor(etkilesimler: dict) -> int:
    """Etkilesim verisinden 0-100 ilişki skoru hesapla."""
    puan = 50  # baz puan
    puan += min(len(etkilesimler.get("randevu", [])) * 5, 15)
    puan += min(len(etkilesimler.get("rehberlik", [])) * 3, 10)
    puan += min(len(etkilesimler.get("toplanti", [])) * 4, 10)
    anketler = etkilesimler.get("anket", [])
    if anketler:
        ort = sum(a.get("puan", 3) for a in anketler) / len(anketler)
        puan += int((ort - 3) * 5)  # 3 baz, ustune +, altina -
    sikayet = len(etkilesimler.get("sikayet", []))
    puan -= min(sikayet * 5, 15)
    return max(0, min(100, puan))


def render_paydas_crm():
    """Paydas 360 CRM — kisi bazli tum etkilesim haritasi."""
    styled_section("Paydas 360 CRM", "#2563eb")
    styled_info_banner(
        "Her veli, ogretmen, personelin tum modullerdeki etkilesimleri tek ekranda. "
        "Isim arayın — tum gecmis 3 saniyede karsınızda.",
        banner_type="info", icon="👤")

    # Veli listesini yukle
    _cache = "kim_crm_veliler"
    if _cache not in st.session_state:
        with st.spinner("Paydas verileri yukleniyor..."):
            st.session_state[_cache] = _toplam_veli_listesi()
    veliler = st.session_state[_cache]

    if st.button("Verileri Yenile", key="crm_yenile"):
        st.session_state.pop(_cache, None)
        st.rerun()

    styled_stat_row([
        ("Toplam Paydas", str(len(veliler)), "#2563eb", "👤"),
        ("Veli", str(sum(1 for v in veliler if v.get("tip") == "veli")), "#10b981", "👪"),
        ("Aday Veli", str(sum(1 for v in veliler if v.get("tip") == "aday_veli")), "#f59e0b", "🎯"),
    ])

    # ── ARAMA ──
    arama = st.text_input("Kisi Ara (veli / ogretmen / personel)", key="crm_ara",
                           placeholder="Isim yazin...")

    if not arama or len(arama) < 2:
        st.caption("En az 2 karakter yazin.")
        return

    q = arama.strip().lower()
    eslesen = [v for v in veliler if q in v["ad"].lower()]

    if not eslesen:
        styled_info_banner(f'"{arama}" ile eslesen paydas bulunamadi.', banner_type="warning", icon="🔍")
        return

    st.caption(f"{len(eslesen)} sonuc bulundu")

    # ── KİŞİ KARTLARI ──
    for v in eslesen[:10]:
        etkilesimler = _kisi_etkilesimleri(v["ad"])
        skor = _kisi_skor(etkilesimler)
        skor_renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 45 else "#ef4444"

        toplam_etkilesim = sum(len(items) for items in etkilesimler.values())
        cocuklar = v.get("cocuklar", [])
        adaylar = v.get("kayit_adaylari", [])

        with st.expander(f"👤 {v['ad']} — Skor: {skor}/100 · {toplam_etkilesim} etkileşim", expanded=len(eslesen) == 1):
            # Hero kart
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {skor_renk}40;border-radius:16px;
                        padding:18px 22px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                    <div>
                        <div style="font-size:20px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                            {v['ad']}</div>
                        <div style="font-size:11px;color:#94a3b8;margin-top:4px;">
                            {v.get('telefon', '') or '—'} · {v.get('email', '') or '—'}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="font-size:36px;font-weight:900;color:{skor_renk};line-height:1;">{skor}</div>
                        <div style="font-size:9px;color:#94a3b8;letter-spacing:1px;">ILISKI SKORU</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Cocuklar
            if cocuklar:
                st.markdown("**Cocuklar:**")
                for c in cocuklar:
                    st.markdown(f"- {c['ad']} ({c['sinif']})")

            # Aday bilgileri
            if adaylar:
                st.markdown("**Kayit Adaylari:**")
                for a in adaylar:
                    st.markdown(f"- {a['ogrenci']} — {a['asama']} ({a['kademe']}) · {a['arama']}A / {a['gorusme']}G")

            # Etkilesim timeline
            timeline = []
            for r in etkilesimler.get("randevu", []):
                timeline.append({"tarih": r["tarih"], "tip": "📅 Randevu", "detay": f"{r['tip']}: {r['konu']}", "renk": "#10b981"})
            for s in etkilesimler.get("sikayet", []):
                timeline.append({"tarih": s["tarih"], "tip": "📝 Sikayet", "detay": f"{s['kategori']}: {s['konu']}", "renk": "#ef4444"})
            for r in etkilesimler.get("rehberlik", []):
                timeline.append({"tarih": r["tarih"], "tip": "🧠 Rehberlik", "detay": r["konu"], "renk": "#7c3aed"})
            for a in etkilesimler.get("anket", []):
                timeline.append({"tarih": a["tarih"], "tip": "📊 Anket", "detay": f"Puan: {a['puan']}/5 ({a['kategori']})", "renk": "#f59e0b"})
            for g in etkilesimler.get("kayit_gorusme", []):
                timeline.append({"tarih": g["tarih"], "tip": "📞 Kayit", "detay": f"{g['sonuc']} ({g['kampanya']})", "renk": "#0891b2"})

            timeline.sort(key=lambda x: x["tarih"], reverse=True)

            if timeline:
                st.markdown("**Etkilesim Gecmisi:**")
                for t in timeline[:15]:
                    st.markdown(f"""<div style="display:flex;gap:10px;align-items:flex-start;padding:4px 0;
                        border-left:3px solid {t['renk']};padding-left:12px;margin-bottom:4px;">
                        <span style="min-width:70px;font-size:10px;color:#64748b;">{t['tarih']}</span>
                        <span style="font-size:11px;font-weight:700;color:{t['renk']};">{t['tip']}</span>
                        <span style="font-size:11px;color:#94a3b8;">{t['detay']}</span>
                    </div>""", unsafe_allow_html=True)

            # Ozet stat
            st.markdown(f"""
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
                <span style="background:#10b98115;color:#10b981;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(etkilesimler.get('randevu', []))} randevu</span>
                <span style="background:#ef444415;color:#ef4444;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(etkilesimler.get('sikayet', []))} sikayet</span>
                <span style="background:#7c3aed15;color:#7c3aed;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(etkilesimler.get('rehberlik', []))} rehberlik</span>
                <span style="background:#f59e0b15;color:#f59e0b;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(etkilesimler.get('anket', []))} anket</span>
                <span style="background:#0891b215;color:#0891b2;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(etkilesimler.get('kayit_gorusme', []))} kayit</span>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 2. AKILLI KURUM HAFIZASI (KNOWLEDGE BASE + AI SEARCH)
# ============================================================

def _kurum_bilgi_bankasi_topla() -> list[dict]:
    """Tum modullerden metin verilerini indeksle."""
    kayitlar: list[dict] = []
    td = _td()
    ak = _ak_dir()

    # 1. Toplanti kararlari
    try:
        from models.toplanti_kurullar import ToplantiDataStore
        top = ToplantiDataStore(os.path.join(td, "toplanti"))
        for d in top.load_list("decisions") if hasattr(top, "load_list") else []:
            kayitlar.append({
                "modul": "Toplanti", "tip": "Karar", "tarih": d.get("tarih", d.get("created_at", ""))[:10],
                "baslik": d.get("karar_metni", d.get("baslik", ""))[:200],
                "detay": d.get("aciklama", "")[:300],
                "id": d.get("id", ""),
            })
        for m in top.load_list("meetings") if hasattr(top, "load_list") else []:
            if m.get("tutanak"):
                kayitlar.append({
                    "modul": "Toplanti", "tip": "Tutanak", "tarih": m.get("tarih", "")[:10],
                    "baslik": m.get("baslik", "")[:200],
                    "detay": str(m.get("tutanak", ""))[:500],
                    "id": m.get("id", ""),
                })
    except Exception:
        pass

    # 2. Sikayet cozumleri
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
    for s in sikayetler:
        kayitlar.append({
            "modul": "Sikayet", "tip": s.get("tur", "Sikayet"), "tarih": (s.get("created_at", "") or "")[:10],
            "baslik": s.get("konu", "")[:200],
            "detay": f"{s.get('aciklama', '')} | Cozum: {s.get('cozum', s.get('sonuc', ''))}".strip()[:400],
            "id": s.get("id", ""),
        })

    # 3. SWOT aksiyonlari
    aksiyonlar = _lj(os.path.join(td, "swot", "aksiyonlar.json"))
    for a in aksiyonlar:
        kayitlar.append({
            "modul": "SWOT", "tip": "Aksiyon", "tarih": (a.get("created_at", "") or "")[:10],
            "baslik": a.get("baslik", "")[:200],
            "detay": a.get("aciklama", "")[:300],
            "id": a.get("id", ""),
        })

    # 4. SWOT maddeleri
    maddeler = _lj(os.path.join(td, "swot", "maddeler.json"))
    for m in maddeler:
        kayitlar.append({
            "modul": "SWOT", "tip": f"SWOT-{m.get('tur', '?')}", "tarih": (m.get("created_at", "") or "")[:10],
            "baslik": m.get("baslik", "")[:200],
            "detay": m.get("aciklama", "")[:300],
            "id": m.get("id", ""),
        })

    # 5. Duyurular
    duyurular = _lj(os.path.join(td, "akademik", "duyurular.json"))
    for d in duyurular:
        kayitlar.append({
            "modul": "Duyuru", "tip": "Duyuru", "tarih": d.get("tarih", (d.get("created_at", "") or "")[:10]),
            "baslik": d.get("baslik", d.get("title", ""))[:200],
            "detay": d.get("icerik", d.get("content", ""))[:400],
            "id": d.get("id", ""),
        })

    # 6. Etkinlik sonuclari
    etkinlikler = _lj(os.path.join(td, "sosyal_etkinlik", "etkinlikler.json"))
    for e in etkinlikler:
        kayitlar.append({
            "modul": "Etkinlik", "tip": e.get("kategori", "Etkinlik"), "tarih": e.get("tarih_baslangic", "")[:10],
            "baslik": e.get("baslik", "")[:200],
            "detay": e.get("aciklama", "")[:300],
            "id": e.get("id", ""),
        })

    # 7. Kampanya planlari
    kampanyalar = _lj(os.path.join(td, "pr01_kampanya_plani.json"))
    for k in kampanyalar:
        kayitlar.append({
            "modul": "Kampanya", "tip": "Plan", "tarih": k.get("tarih", (k.get("created_at", "") or "")[:10]),
            "baslik": k.get("baslik", k.get("kampanya_adi", ""))[:200],
            "detay": k.get("aciklama", k.get("strateji", ""))[:300],
            "id": k.get("id", ""),
        })

    return kayitlar


def render_kurum_hafizasi():
    """Kurum hafizasi — tum modullerin metin verileri + AI arama."""
    styled_section("Kurum Hafizasi", "#7c3aed")
    styled_info_banner(
        "Tum toplanti kararlari, sikayet cozumleri, SWOT aksiyonlari, duyurular, etkinlik sonuclari "
        "— hepsi indekslenmiş. Dogal dilde arayin.",
        banner_type="info", icon="🧠")

    _cache = "kim_hafiza_db"
    if _cache not in st.session_state:
        with st.spinner("Kurum hafizasi yukleniyor..."):
            st.session_state[_cache] = _kurum_bilgi_bankasi_topla()
    kayitlar = st.session_state[_cache]

    if st.button("Verileri Yenile", key="hf_yenile"):
        st.session_state.pop(_cache, None)
        st.rerun()

    modul_sayac = Counter(k["modul"] for k in kayitlar)
    styled_stat_row([
        ("Toplam Kayit", str(len(kayitlar)), "#7c3aed", "📚"),
        ("Modul Sayisi", str(len(modul_sayac)), "#2563eb", "📦"),
        ("Karar", str(sum(1 for k in kayitlar if k["tip"] == "Karar")), "#10b981", "📋"),
        ("Sikayet", str(sum(1 for k in kayitlar if k["modul"] == "Sikayet")), "#ef4444", "📝"),
    ])

    sub = st.tabs(["🔍 Arama", "🤖 AI Soru-Cevap", "📋 Tum Kayitlar"])

    # ═══ ARAMA ═══
    with sub[0]:
        sorgu = st.text_input("Kurum hafizasinda ara...", key="hf_sorgu",
                               placeholder="Ornek: servis sikayeti, matematik basarisi, yangin tatbikati...")

        if sorgu and len(sorgu) >= 2:
            q = sorgu.strip().lower()
            sonuclar = [k for k in kayitlar
                        if q in (k.get("baslik", "") or "").lower()
                        or q in (k.get("detay", "") or "").lower()
                        or q in (k.get("modul", "") or "").lower()
                        or q in (k.get("tip", "") or "").lower()]

            st.caption(f"{len(sonuclar)} sonuc bulundu")

            _modul_renk = {
                "Toplanti": "#059669", "Sikayet": "#ef4444", "SWOT": "#7c3aed",
                "Duyuru": "#2563eb", "Etkinlik": "#ea580c", "Kampanya": "#f59e0b",
            }

            for k in sonuclar[:20]:
                renk = _modul_renk.get(k["modul"], "#64748b")
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                            border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <div style="display:flex;gap:6px;align-items:center;">
                            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                                        font-size:10px;font-weight:700;">{k['modul']}</span>
                            <span style="font-size:10px;color:#64748b;">{k['tip']}</span>
                        </div>
                        <span style="font-size:10px;color:#64748b;">{k['tarih']}</span>
                    </div>
                    <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
                        {k['baslik'][:120]}</div>
                    <div style="font-size:11px;color:#94a3b8;">{k['detay'][:200]}</div>
                </div>""", unsafe_allow_html=True)

            if not sonuclar:
                styled_info_banner(f'"{sorgu}" ile eslesen kayit bulunamadi.', banner_type="warning", icon="🔍")

    # ═══ AI SORU-CEVAP ═══
    with sub[1]:
        styled_section("AI ile Kurum Hafizasi Sorgula")
        ai_soru = st.text_area("Sorunuzu yazin...", key="hf_ai_soru", height=80,
                                placeholder="Ornek: Gecen yil servis sikayetlerine ne cevap verdik?")

        if st.button("AI'ya Sor", key="hf_ai_btn", type="primary"):
            if ai_soru:
                # Ilgili kayitlari bul (keyword match)
                q = ai_soru.strip().lower()
                ilgili = [k for k in kayitlar
                          if any(w in (k.get("baslik", "") + " " + k.get("detay", "")).lower()
                                 for w in q.split() if len(w) > 2)][:15]

                baglamlar = "\n".join(
                    f"[{k['modul']}/{k['tip']}] {k['tarih']}: {k['baslik']} — {k['detay'][:150]}"
                    for k in ilgili)

                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if not client:
                        st.warning("OpenAI API anahtari bulunamadi.")
                    else:
                        with st.spinner("AI dusunuyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul kurumsal hafiza asistanisin. Verilen kurumsal kayitlara dayanarak soruyu Turkce cevapla. Kaynak goster."},
                                    {"role": "user", "content": f"Soru: {ai_soru}\n\nKurumsal Kayitlar:\n{baglamlar or 'Ilgili kayit bulunamadi.'}"},
                                ],
                                max_tokens=600, temperature=0.5,
                            )
                            cevap = resp.choices[0].message.content or ""

                        if cevap:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                        border-radius:14px;padding:18px 22px;margin-top:12px;">
                                <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:8px;">
                                    🧠 AI Cevabi ({len(ilgili)} kayit taranarak)</div>
                                <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">
                                    {cevap.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI hatasi: {e}")

    # ═══ TUM KAYITLAR ═══
    with sub[2]:
        styled_section("Tum Kurumsal Kayitlar")
        modul_fil = st.selectbox("Modul", ["Tumu"] + sorted(modul_sayac.keys()), key="hf_modul_fil")

        filtered = kayitlar
        if modul_fil != "Tumu":
            filtered = [k for k in filtered if k["modul"] == modul_fil]

        st.caption(f"{len(filtered)} kayit")

        rows = ""
        for k in sorted(filtered, key=lambda x: x["tarih"], reverse=True)[:50]:
            rows += f"""<tr>
                <td style="padding:5px 8px;font-size:11px;color:#64748b;">{k['tarih']}</td>
                <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{k['modul']}</td>
                <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{k['tip']}</td>
                <td style="padding:5px 8px;font-size:11px;color:#e2e8f0;font-weight:600;">{k['baslik'][:80]}</td>
            </tr>"""
        if rows:
            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:#1e293b;">
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Tarih</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Modul</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Tip</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Baslik</th>
            </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)


# ============================================================
# 3. STRATEJİK OKR TAKİP SİSTEMİ
# ============================================================

def _okr_path() -> str:
    return os.path.join(_td(), "yte", "okr_hedefler.json")


def _load_okrs() -> list[dict]:
    return _lj(_okr_path())


def _save_okrs(okrs: list[dict]):
    path = _okr_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(okrs, f, ensure_ascii=False, indent=2)


# Otomatik KR kaynaklari
_OTO_KR_KAYNAKLARI = {
    "not_ortalamasi": {
        "label": "Not Ortalamasi",
        "fn": lambda: _hesapla_not_ort(),
    },
    "devamsizlik_orani": {
        "label": "Devamsizlik Orani %",
        "fn": lambda: _hesapla_devamsizlik_oran(),
    },
    "memnuniyet_puani": {
        "label": "Veli Memnuniyet Puani (1-5)",
        "fn": lambda: _hesapla_memnuniyet(),
    },
    "sikayet_cozum_suresi": {
        "label": "Ort. Sikayet Cozum Suresi (gun)",
        "fn": lambda: _hesapla_sikayet_sure(),
    },
    "kayit_donusum": {
        "label": "Kayit Donusum Orani %",
        "fn": lambda: _hesapla_kayit_donusum(),
    },
    "personel_doluluk": {
        "label": "Personel Doluluk %",
        "fn": lambda: _hesapla_personel_doluluk(),
    },
}


def _hesapla_not_ort():
    notlar = _lj(os.path.join(_ak_dir(), "grades.json"))
    puanlar = [n.get("puan", 0) for n in notlar if isinstance(n.get("puan"), (int, float))]
    return round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0


def _hesapla_devamsizlik_oran():
    devamsiz = len(_lj(os.path.join(_ak_dir(), "attendance.json")))
    ogrenci = len(_lj(os.path.join(_ak_dir(), "students.json")))
    return round(devamsiz / max(ogrenci, 1) * 100, 1) if ogrenci else 0


def _hesapla_memnuniyet():
    cevaplar = _lj(os.path.join(_td(), "veli_anket", "cevaplar.json"))
    puanlar = [c.get("puan", 0) for c in cevaplar if isinstance(c.get("puan"), (int, float))]
    return round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0


def _hesapla_sikayet_sure():
    sikayetler = _lj(os.path.join(_td(), "kim01_sikayet_oneri.json"))
    sureler = []
    for s in sikayetler:
        if s.get("durum") == "cozumlendi" and s.get("created_at") and s.get("cozum_tarihi"):
            try:
                bas = datetime.fromisoformat(s["created_at"][:19])
                bit = datetime.fromisoformat(s["cozum_tarihi"][:19])
                sureler.append((bit - bas).days)
            except Exception:
                pass
    return round(sum(sureler) / max(len(sureler), 1), 1) if sureler else 0


def _hesapla_kayit_donusum():
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
        return round(kesin / max(len(adaylar), 1) * 100, 1) if adaylar else 0
    except Exception:
        return 0


def _hesapla_personel_doluluk():
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(_td(), "ik"))
        emp = ik.load_list("employees") if hasattr(ik, "load_list") else []
        aktif = sum(1 for e in emp if e.get("status") == "Aktif")
        pos = ik.load_list("positions") if hasattr(ik, "load_list") else []
        return round(aktif / max(len(pos), 1) * 100, 1) if pos else 0
    except Exception:
        return 0


def render_okr_takip():
    """Stratejik OKR Takip — hedef belirleme + otomatik ilerleme."""
    styled_section("OKR Takip Sistemi", "#f59e0b")
    styled_info_banner(
        "Kurumsal hedefleri OKR formatinda belirleyin. "
        "Anahtar sonuclar modullerden otomatik cekilir veya manuel girilir.",
        banner_type="info", icon="🎯")

    okrs = _load_okrs()

    sub = st.tabs(["📊 Dashboard", "➕ Yeni OKR", "📋 OKR Listesi"])

    # ═══ DASHBOARD ═══
    with sub[0]:
        if not okrs:
            styled_info_banner("Henuz OKR tanimlanmamis. 'Yeni OKR' sekmesinden ekleyin.", banner_type="info", icon="🎯")
        else:
            toplam_kr = sum(len(o.get("key_results", [])) for o in okrs)
            ort_ilerleme = round(sum(o.get("ilerleme", 0) for o in okrs) / max(len(okrs), 1), 1)
            tamamlanan = sum(1 for o in okrs if o.get("ilerleme", 0) >= 100)

            styled_stat_row([
                ("Toplam Hedef", str(len(okrs)), "#f59e0b", "🎯"),
                ("Key Result", str(toplam_kr), "#2563eb", "📋"),
                ("Ort. Ilerleme", f"%{ort_ilerleme}", "#7c3aed", "📊"),
                ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
            ])

            # OKR kartlari
            for o in okrs:
                krs = o.get("key_results", [])
                # Her KR icin otomatik guncelle
                for kr in krs:
                    if kr.get("oto_kaynak") and kr["oto_kaynak"] in _OTO_KR_KAYNAKLARI:
                        try:
                            kr["gercek"] = _OTO_KR_KAYNAKLARI[kr["oto_kaynak"]]["fn"]()
                        except Exception:
                            pass

                # OKR ilerleme hesapla
                kr_ilerlemeler = []
                for kr in krs:
                    hedef = kr.get("hedef", 100)
                    gercek = kr.get("gercek", 0)
                    if kr.get("ters", False):
                        ilerleme = max(0, min(100, 100 - (gercek / max(hedef, 1) * 100))) if hedef else 100
                    else:
                        ilerleme = min(100, gercek / max(hedef, 1) * 100) if hedef else 0
                    kr_ilerlemeler.append(ilerleme)
                    kr["ilerleme"] = round(ilerleme, 1)

                okr_ilerleme = round(sum(kr_ilerlemeler) / max(len(kr_ilerlemeler), 1), 1) if kr_ilerlemeler else 0
                o["ilerleme"] = okr_ilerleme
                renk = "#10b981" if okr_ilerleme >= 70 else "#f59e0b" if okr_ilerleme >= 40 else "#ef4444"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                            border-radius:0 16px 16px 0;padding:16px 20px;margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                        <div>
                            <div style="font-size:15px;font-weight:800;color:#fff;">{o.get('baslik', '')}</div>
                            <div style="font-size:10px;color:#94a3b8;">{o.get('donem', '')} · {o.get('sorumlu', '')}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="font-size:28px;font-weight:900;color:{renk};">%{okr_ilerleme}</div>
                        </div>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;margin-bottom:10px;">
                        <div style="width:{min(okr_ilerleme, 100)}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

                # KR detaylari
                for kr in krs:
                    kr_renk = "#10b981" if kr.get("ilerleme", 0) >= 70 else "#f59e0b" if kr.get("ilerleme", 0) >= 40 else "#ef4444"
                    oto_badge = '<span style="background:#0891b215;color:#0891b2;padding:1px 6px;border-radius:4px;font-size:8px;">OTO</span>' if kr.get("oto_kaynak") else ''
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:4px 0 4px 24px;">
                        <span style="font-size:11px;color:#94a3b8;flex:1;">{kr.get('ad', '')}</span>
                        {oto_badge}
                        <span style="font-size:11px;color:#64748b;">{kr.get('gercek', 0)}/{kr.get('hedef', 0)}</span>
                        <span style="background:{kr_renk}20;color:{kr_renk};padding:1px 8px;border-radius:4px;
                                    font-size:10px;font-weight:700;">%{kr.get('ilerleme', 0)}</span>
                    </div>""", unsafe_allow_html=True)

            # Kaydet (otomatik KR guncelleme)
            _save_okrs(okrs)

    # ═══ YENİ OKR ═══
    with sub[1]:
        styled_section("Yeni OKR Olustur")

        with st.form("okr_yeni_form"):
            baslik = st.text_input("Hedef (Objective)", placeholder="Ornek: Veli Memnuniyetini %90'a Cikarmak")
            fc1, fc2 = st.columns(2)
            with fc1:
                donem = st.selectbox("Donem", ["2025-2026 Q1", "2025-2026 Q2", "2025-2026 Q3", "2025-2026 Q4",
                                                 "2025-2026 Yillik"], key="okr_donem")
            with fc2:
                sorumlu = st.text_input("Sorumlu", placeholder="Mudur / Departman")

            st.markdown("**Key Results (Anahtar Sonuclar):**")
            kr_list = []
            for i in range(1, 5):
                kr_col1, kr_col2, kr_col3, kr_col4 = st.columns([3, 1, 1, 1])
                with kr_col1:
                    kr_ad = st.text_input(f"KR{i} Ad", key=f"okr_kr{i}_ad", placeholder=f"Anahtar Sonuc {i}")
                with kr_col2:
                    kr_hedef = st.number_input(f"Hedef", key=f"okr_kr{i}_hedef", min_value=0, value=100)
                with kr_col3:
                    kr_oto = st.selectbox(f"Kaynak", ["Manuel"] + list(_OTO_KR_KAYNAKLARI.keys()),
                                           key=f"okr_kr{i}_oto",
                                           format_func=lambda x: _OTO_KR_KAYNAKLARI[x]["label"] if x in _OTO_KR_KAYNAKLARI else "Manuel")
                with kr_col4:
                    kr_ters = st.checkbox("Ters", key=f"okr_kr{i}_ters", help="Dusuk deger iyi (devamsizlik gibi)")
                if kr_ad:
                    kr_list.append({
                        "ad": kr_ad, "hedef": kr_hedef, "gercek": 0,
                        "oto_kaynak": kr_oto if kr_oto != "Manuel" else "",
                        "ters": kr_ters,
                    })

            if st.form_submit_button("OKR Olustur", type="primary"):
                if baslik and kr_list:
                    yeni = {
                        "id": f"okr_{uuid.uuid4().hex[:8]}",
                        "baslik": baslik,
                        "donem": donem,
                        "sorumlu": sorumlu,
                        "key_results": kr_list,
                        "ilerleme": 0,
                        "created_at": datetime.now().isoformat(),
                    }
                    okrs.append(yeni)
                    _save_okrs(okrs)
                    st.success(f"OKR olusturuldu: {baslik} ({len(kr_list)} KR)")
                    st.rerun()
                else:
                    st.warning("Baslik ve en az 1 Key Result gerekli.")

    # ═══ OKR LİSTESİ (Düzenle/Sil) ═══
    with sub[2]:
        styled_section("Tum OKR'ler")
        if not okrs:
            st.info("Henuz OKR yok.")
        else:
            for oidx, o in enumerate(okrs):
                with st.expander(f"🎯 {o['baslik']} — %{o.get('ilerleme', 0)} ({o.get('donem', '')})", expanded=False):
                    # Manuel KR guncelleme
                    for kidx, kr in enumerate(o.get("key_results", [])):
                        if not kr.get("oto_kaynak"):
                            yeni_gercek = st.number_input(
                                f"{kr['ad']} (hedef: {kr['hedef']})",
                                min_value=0, value=int(kr.get("gercek", 0)),
                                key=f"okr_g_{oidx}_{kidx}")
                            kr["gercek"] = yeni_gercek

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Guncelle", key=f"okr_upd_{oidx}", type="primary"):
                            _save_okrs(okrs)
                            st.success("OKR guncellendi!")
                            st.rerun()
                    with c2:
                        if st.button("Sil", key=f"okr_del_{oidx}"):
                            okrs.pop(oidx)
                            _save_okrs(okrs)
                            st.success("OKR silindi.")
                            st.rerun()
