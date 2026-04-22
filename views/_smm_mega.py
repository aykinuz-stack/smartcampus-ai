"""
Sosyal Medya Yonetimi — MEGA Ozellikleri
==========================================
1. Sosyal Dinleme Radari (Social Listening Engine)
2. Sosyal Medya Otopilot (Auto-Publish Scheduler)
3. Sosyal Medya ROI Zekasi (Cross-Module Impact Tracker)
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
# 1. SOSYAL DİNLEME RADARI
# ============================================================

_KONU_ANAHTAR = {
    "servis": ["servis", "otobus", "ring", "gecikme", "ulasim", "sofor"],
    "yemek": ["yemek", "kantin", "yemekhane", "menu", "aclik"],
    "akademik": ["ders", "sinav", "not", "ogretmen", "basari", "odev", "proje"],
    "ucret": ["ucret", "fiyat", "para", "taksit", "odeme", "pahali", "indirim"],
    "guvenlik": ["guvenlik", "kamera", "kapı", "kaza", "zarar", "siddet"],
    "temizlik": ["temizlik", "hijyen", "tuvalet", "kirli"],
    "iletisim": ["aranmıyor", "cevap", "donmuyorlar", "iletisim", "telefon"],
}


def _kategorize_metin(metin: str) -> str:
    """Metinden konu kategorisi cikar."""
    m = metin.lower()
    for kategori, kelimeler in _KONU_ANAHTAR.items():
        if any(k in m for k in kelimeler):
            return kategori
    return "genel"


def _toplam_dinleme_verisi() -> list[dict]:
    """Tum modullerden metin verileri topla."""
    td = _td()
    ak = _ak_dir()
    kayitlar = []

    # 1. Inbox mesajlari
    inbox = _lj(os.path.join(td, "smm_inbox.json"))
    try:
        from models.sosyal_medya import get_smm_store
        inbox = get_smm_store().load_list("inbox") or inbox
    except Exception:
        pass
    for m in inbox:
        metin = m.get("metin", m.get("message", m.get("icerik", ""))) or ""
        kayitlar.append({
            "kaynak": "Sosyal Medya", "metin": metin, "duygu": m.get("sentiment", m.get("duygu", "notr")),
            "tarih": (m.get("created_at", m.get("tarih", "")) or "")[:10],
            "konu": _kategorize_metin(metin),
        })

    # 2. Sikayetler
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
    for s in sikayetler:
        metin = f"{s.get('konu', '')} {s.get('aciklama', '')}"
        kayitlar.append({
            "kaynak": "Sikayet", "metin": metin, "duygu": "negatif",
            "tarih": (s.get("created_at", "") or "")[:10],
            "konu": s.get("kategori", _kategorize_metin(metin)),
        })

    # 3. Veli anket yorumlari
    yorumlar = _lj(os.path.join(td, "veli_anket", "yorumlar.json"))
    for y in yorumlar:
        metin = y.get("yorum", y.get("metin", "")) or ""
        kayitlar.append({
            "kaynak": "Anket", "metin": metin, "duygu": "notr",
            "tarih": (y.get("created_at", "") or "")[:10],
            "konu": _kategorize_metin(metin),
        })

    # 4. Kayit gorusme notlari
    gorusmeler = _lj(os.path.join(td, "pr01_gorusme_kayitlari.json"))
    for g in gorusmeler:
        metin = g.get("Not", g.get("not", "")) or ""
        if metin:
            kayitlar.append({
                "kaynak": "Kayit", "metin": metin, "duygu": "notr",
                "tarih": g.get("Tarih", "")[:10] if g.get("Tarih") else "",
                "konu": _kategorize_metin(metin),
            })

    return [k for k in kayitlar if k["metin"].strip()]


def render_sosyal_dinleme():
    """Sosyal dinleme radari — tum platformlarda ne konusuluyor."""
    styled_section("Sosyal Dinleme Radari", "#0ea5e9")
    styled_info_banner(
        "Okulunuz hakkinda tum kanallarda ne konusuluyor? "
        "Mesajlar, sikayetler, anket yorumlari, kayit notlari — hepsi analiz edilir.",
        banner_type="info", icon="📡")

    _cache = "smm_dinleme_data"
    if _cache not in st.session_state:
        with st.spinner("Dinleme verileri toplanıyor..."):
            st.session_state[_cache] = _toplam_dinleme_verisi()
    kayitlar = st.session_state[_cache]

    if st.button("Verileri Yenile", key="dinleme_yenile"):
        st.session_state.pop(_cache, None)
        st.rerun()

    son_7g = (date.today() - timedelta(days=7)).isoformat()
    son_30g = (date.today() - timedelta(days=30)).isoformat()
    son7 = [k for k in kayitlar if k["tarih"] >= son_7g]
    son30 = [k for k in kayitlar if k["tarih"] >= son_30g]

    # Duygu dagilimi
    duygu_sayac = Counter(k["duygu"] for k in son30)
    negatif = sum(1 for k in son30 if k["duygu"] in ("negatif", "negative", "olumsuz"))
    pozitif = sum(1 for k in son30 if k["duygu"] in ("pozitif", "positive", "olumlu"))
    notr = len(son30) - negatif - pozitif

    styled_stat_row([
        ("Toplam Kayit", str(len(kayitlar)), "#0ea5e9", "📡"),
        ("Son 7 Gun", str(len(son7)), "#2563eb", "📊"),
        ("Pozitif", str(pozitif), "#10b981", "😊"),
        ("Notr", str(notr), "#f59e0b", "😐"),
        ("Negatif", str(negatif), "#ef4444", "😡"),
    ])

    sub = st.tabs(["📊 Konu Analizi", "☁️ Kelime Bulutu", "📈 Trend", "🤖 AI Ozet"])

    # ═══ KONU ANALİZİ ═══
    with sub[0]:
        styled_section("Konu Dagilimi (Son 30 Gun)")
        konu_sayac = Counter(k["konu"] for k in son30)
        if konu_sayac:
            en_cok = konu_sayac.most_common(1)[0][1]
            _konu_renk = {"servis": "#ef4444", "yemek": "#f59e0b", "akademik": "#2563eb",
                           "ucret": "#7c3aed", "guvenlik": "#dc2626", "temizlik": "#0891b2",
                           "iletisim": "#6366f1", "genel": "#94a3b8"}
            for konu, sayi in konu_sayac.most_common():
                renk = _konu_renk.get(konu, "#64748b")
                bar_w = round(sayi / max(en_cok, 1) * 100)
                # Bu konudaki negatif oran
                konu_neg = sum(1 for k in son30 if k["konu"] == konu and k["duygu"] in ("negatif", "negative", "olumsuz"))
                neg_pct = round(konu_neg / max(sayi, 1) * 100)
                alarm = " 🚨" if neg_pct > 40 else ""
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="min-width:80px;font-size:12px;color:#e2e8f0;font-weight:700;">
                        {konu.title()}{alarm}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:22px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:10px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                    <span style="min-width:50px;font-size:10px;color:{'#ef4444' if neg_pct > 30 else '#94a3b8'};">
                        %{neg_pct} neg</span>
                </div>""", unsafe_allow_html=True)

    # ═══ KELİME BULUTU ═══
    with sub[1]:
        styled_section("En Cok Gecen Kelimeler")
        tum_metin = " ".join(k["metin"] for k in son30)
        kelimeler = [w.strip().lower() for w in tum_metin.split() if len(w.strip()) > 3]
        # Stop words
        stop = {"olan", "icin", "bile", "daha", "cok", "gibi", "ama", "fakat", "veya", "ile",
                "bu", "bir", "ve", "da", "de", "mi", "mu", "ben", "biz", "siz", "var", "yok",
                "kadar", "sonra", "once", "nasil", "neden", "nerede", "zaman"}
        kelimeler = [w for w in kelimeler if w not in stop]
        kelime_sayac = Counter(kelimeler)

        if kelime_sayac:
            en_cok_k = kelime_sayac.most_common(1)[0][1]
            cloud_html = ""
            for kelime, sayi in kelime_sayac.most_common(30):
                size = max(10, min(36, round(sayi / max(en_cok_k, 1) * 36)))
                renk = "#ef4444" if kelime in sum(_KONU_ANAHTAR.values(), []) else "#6366f1"
                cloud_html += f'<span style="font-size:{size}px;color:{renk};font-weight:700;margin:4px 8px;display:inline-block;">{kelime}</span>'
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;
                        padding:20px;text-align:center;line-height:2.2;">
                {cloud_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Yeterli metin verisi yok.")

    # ═══ TREND ═══
    with sub[2]:
        styled_section("Haftalik Duygu Trendi")
        for i in range(3, -1, -1):
            hafta_bas = (date.today() - timedelta(weeks=i, days=date.today().weekday())).isoformat()
            hafta_bit = (date.today() - timedelta(weeks=i, days=date.today().weekday() - 6)).isoformat()
            hafta_kayit = [k for k in kayitlar if hafta_bas <= k["tarih"] <= hafta_bit]
            h_neg = sum(1 for k in hafta_kayit if k["duygu"] in ("negatif", "negative", "olumsuz"))
            h_poz = sum(1 for k in hafta_kayit if k["duygu"] in ("pozitif", "positive", "olumlu"))
            h_top = max(len(hafta_kayit), 1)
            neg_pct = round(h_neg / h_top * 100)
            poz_pct = round(h_poz / h_top * 100)
            is_current = i == 0
            border = "border:2px solid #0ea5e9;" if is_current else ""

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;{border}border-radius:10px;
                        padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:12px;">
                        {'Bu Hafta' if is_current else f'{4-i} Hafta Once'}</span>
                    <span style="font-size:10px;color:#94a3b8;">{len(hafta_kayit)} kayit</span>
                </div>
                <div style="display:flex;gap:4px;height:12px;">
                    <div style="width:{poz_pct}%;background:#10b981;border-radius:3px;"></div>
                    <div style="width:{100 - poz_pct - neg_pct}%;background:#f59e0b;border-radius:3px;"></div>
                    <div style="width:{neg_pct}%;background:#ef4444;border-radius:3px;"></div>
                </div>
                <div style="display:flex;gap:12px;font-size:9px;color:#64748b;margin-top:3px;">
                    <span>Pozitif: %{poz_pct}</span><span>Notr: %{100-poz_pct-neg_pct}</span><span>Negatif: %{neg_pct}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ AI ÖZET ═══
    with sub[3]:
        styled_section("AI Haftalik Dinleme Ozeti")
        if st.button("AI Ozet Olustur", key="dinleme_ai", type="primary"):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    konu_ozet = ", ".join(f"{k}: {s}" for k, s in Counter(k["konu"] for k in son7).most_common())
                    duygu_ozet = f"Pozitif: {sum(1 for k in son7 if k['duygu'] in ('pozitif','positive','olumlu'))}, Negatif: {sum(1 for k in son7 if k['duygu'] in ('negatif','negative','olumsuz'))}, Notr: {len(son7) - sum(1 for k in son7 if k['duygu'] in ('pozitif','positive','olumlu','negatif','negative','olumsuz'))}"
                    ornekler = "\n".join(f"- [{k['kaynak']}] {k['metin'][:100]}" for k in son7[:10])

                    with st.spinner("AI analiz ediyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul iletisim uzmanisin. Verilen sosyal dinleme verilerini analiz et. Haftalik ozet rapor hazirla: 1) Genel durum 2) One cikan konular 3) Riskler 4) Oneriler. Turkce, kisa."},
                                {"role": "user", "content": f"Son 7 gun: {len(son7)} kayit\nKonular: {konu_ozet}\nDuygu: {duygu_ozet}\nOrnekler:\n{ornekler}"},
                            ],
                            max_tokens=500, temperature=0.7,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#0c4a6e,#075985);border:1px solid #0ea5e9;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#7dd3fc;font-weight:700;margin-bottom:6px;">AI Haftalik Dinleme Raporu</div>
                            <div style="font-size:12px;color:#e0f2fe;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API anahtari bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")


# ============================================================
# 2. SOSYAL MEDYA OTOPİLOT
# ============================================================

def _otopilot_path() -> str:
    return os.path.join(_td(), "smm_otopilot.json")


def render_otopilot():
    """Otomatik yayin zamanlama — set it and forget it."""
    styled_section("Sosyal Medya Otopilot", "#7c3aed")
    styled_info_banner(
        "Onayli postlari otopilot kuyruğuna alin. Tarih+saat geldiginde "
        "otomatik durum degisimi: SCHEDULED → PUBLISHED.",
        banner_type="info", icon="🤖")

    td = _td()
    posts = _lj(os.path.join(td, "smm_posts.json"))
    try:
        from models.sosyal_medya import get_smm_store
        store = get_smm_store()
        posts = store.load_list("posts") or posts
    except Exception:
        store = None

    # Otopilot ayarlari
    otopilot = _lj(_otopilot_path())
    otopilot_aktif = any(o.get("aktif") for o in otopilot) if otopilot else False

    # Zamanlanmis postlar
    bugun = date.today().isoformat()
    simdi = datetime.now().strftime("%H:%M")
    zamanlanmis = [p for p in posts if p.get("status") in ("SCHEDULED", "READY_TO_PUBLISH", "APPROVED")
                    and p.get("planlanan_tarih")]

    # Yaklasan (onumuzdeki 7 gun)
    yedi_gun = (date.today() + timedelta(days=7)).isoformat()
    yaklasan = [p for p in zamanlanmis if bugun <= (p.get("planlanan_tarih", "") or "")[:10] <= yedi_gun]
    yaklasan.sort(key=lambda p: p.get("planlanan_tarih", ""))

    # Gecmis (bugun oncesi ama hala scheduled)
    geciken = [p for p in zamanlanmis if (p.get("planlanan_tarih", "") or "")[:10] < bugun]

    _PI = {
        "instagram": {"ikon": "📸", "renk": "#E4405F"}, "facebook": {"ikon": "📘", "renk": "#1877F2"},
        "tiktok": {"ikon": "🎵", "renk": "#000"}, "youtube": {"ikon": "🎬", "renk": "#FF0000"},
        "linkedin": {"ikon": "💼", "renk": "#0A66C2"}, "x_twitter": {"ikon": "🐦", "renk": "#1DA1F2"},
    }

    styled_stat_row([
        ("Kuyrukta", str(len(zamanlanmis)), "#7c3aed", "📋"),
        ("Bu Hafta", str(len(yaklasan)), "#2563eb", "📅"),
        ("Geciken", str(len(geciken)), "#ef4444", "⚠️"),
        ("Otopilot", "AKTIF" if otopilot_aktif else "PASIF", "#10b981" if otopilot_aktif else "#64748b", "🤖"),
    ])

    # ── OTOPILOT TOGGLE ──
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Otopilot AKTIF" if not otopilot_aktif else "Otopilot KAPAT", key="oto_toggle",
                       type="primary" if not otopilot_aktif else "secondary", use_container_width=True):
            _sj(_otopilot_path(), [{"aktif": not otopilot_aktif, "updated": datetime.now().isoformat()}])
            st.rerun()

    # ── GECİKEN POSTLAR ──
    if geciken:
        styled_section(f"Geciken Postlar ({len(geciken)})", "#ef4444")
        for p in geciken[:10]:
            pi = _PI.get(p.get("platform", ""), {"ikon": "📋", "renk": "#64748b"})
            metin = (p.get("metin", p.get("caption", "")) or "")[:60]
            tarih = (p.get("planlanan_tarih", "") or "")[:16]
            st.markdown(f"""
            <div style="background:#450a0a;border:1px solid #ef4444;border-left:4px solid #ef4444;
                        border-radius:0 10px 10px 0;padding:8px 12px;margin-bottom:4px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:11px;color:#fca5a5;">{pi['ikon']} {tarih} — {metin}</span>
                    <span style="background:#ef4444;color:#fff;padding:2px 8px;border-radius:6px;
                                font-size:9px;font-weight:700;">GECIKTI</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── YAKLASAN 7 GÜN TAKVİMİ ──
    styled_section("Onumuzdeki 7 Gun Yayin Plani")
    if not yaklasan:
        styled_info_banner("Onumuzdeki 7 gunde zamanlanmis post yok.", banner_type="info", icon="📅")
    else:
        for p in yaklasan:
            pi = _PI.get(p.get("platform", ""), {"ikon": "📋", "renk": "#64748b"})
            metin = (p.get("metin", p.get("caption", "")) or "")[:80]
            tarih = (p.get("planlanan_tarih", "") or "")[:16]
            tarih_obj = tarih[:10]
            saat = tarih[11:16] if len(tarih) > 15 else "--:--"

            # Countdown
            try:
                plan_dt = datetime.fromisoformat(tarih[:19]) if len(tarih) >= 19 else datetime.fromisoformat(tarih[:10])
                kalan = plan_dt - datetime.now()
                if kalan.total_seconds() > 0:
                    saat_kalan = int(kalan.total_seconds() // 3600)
                    dk_kalan = int((kalan.total_seconds() % 3600) // 60)
                    countdown = f"{saat_kalan}s {dk_kalan}dk"
                else:
                    countdown = "SIMDI"
            except Exception:
                countdown = "?"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {pi['renk']}30;border-left:4px solid {pi['renk']};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:12px;font-weight:700;color:#e2e8f0;">{pi['ikon']} {saat} · {tarih_obj}</span>
                        <span style="color:#94a3b8;font-size:11px;margin-left:8px;">{metin}</span>
                    </div>
                    <span style="background:#7c3aed20;color:#7c3aed;padding:3px 10px;border-radius:6px;
                                font-size:10px;font-weight:700;">{countdown}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── EN İYİ SAAT ÖNERİLERİ ──
    styled_section("Platform Bazli En Iyi Yayin Saati")
    _ideal_saatler = {
        "instagram": ("18:00-20:00", "Aksam yorgunlugu — scroll zamani"),
        "facebook": ("12:00-14:00", "Ogle arasi — haber okuma"),
        "tiktok": ("19:00-22:00", "Aksam eglence zamani"),
        "youtube": ("14:00-17:00", "Ogleden sonra — video izleme"),
        "linkedin": ("08:00-10:00", "Is baslangici — profesyonel icerik"),
    }
    for plat, (saat, neden) in _ideal_saatler.items():
        pi = _PI.get(plat, {"ikon": "📋", "renk": "#64748b"})
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
            <span style="font-size:14px;">{pi['ikon']}</span>
            <span style="min-width:80px;font-size:12px;color:#e2e8f0;font-weight:600;">{plat.title()}</span>
            <span style="background:{pi['renk']}20;color:{pi['renk']};padding:2px 10px;border-radius:6px;
                        font-size:11px;font-weight:700;">{saat}</span>
            <span style="font-size:10px;color:#64748b;">{neden}</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. SOSYAL MEDYA ROI ZEKASI (CROSS-MODULE IMPACT)
# ============================================================

def render_etki_analizi():
    """Sosyal medya aktivitesinin diger metriklere etkisi."""
    styled_section("Sosyal Medya Etki Analizi", "#f59e0b")
    styled_info_banner(
        "Sosyal medya aktivitesinin kayit, memnuniyet ve itibar uzerindeki etkisini olcun. "
        "Moduller arasi korelasyon + haftalik etki skoru.",
        banner_type="info", icon="🧩")

    td = _td()
    ak = _ak_dir()

    # Veri yukle
    posts = _lj(os.path.join(td, "smm_posts.json"))
    try:
        from models.sosyal_medya import get_smm_store
        posts = get_smm_store().load_list("posts") or posts
    except Exception:
        pass
    yayinlanan = [p for p in posts if p.get("status") == "PUBLISHED"]

    # Kayit verisi
    kayit_toplam, kayit_kesin, kayit_referans = 0, 0, 0
    try:
        from models.kayit_modulu import get_kayit_store
        adaylar = get_kayit_store().load_all()
        kayit_toplam = len(adaylar)
        kayit_kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
        kayit_referans = sum(1 for a in adaylar if a.referans_veli)
    except Exception:
        pass

    # Memnuniyet
    cevaplar = _lj(os.path.join(td, "veli_anket", "cevaplar.json"))
    memnuniyet = round(sum(c.get("puan", 0) for c in cevaplar) / max(len(cevaplar), 1), 1) if cevaplar else 0

    # Sikayet
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))

    # Haftalik post sayilari (son 8 hafta)
    haftalik_post = []
    haftalik_kayit = []
    for i in range(7, -1, -1):
        h_bas = date.today() - timedelta(weeks=i, days=date.today().weekday())
        h_bit = h_bas + timedelta(days=6)
        h_post = sum(1 for p in yayinlanan
                      if h_bas.isoformat() <= (p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "")[:10] <= h_bit.isoformat())
        h_kayit = sum(1 for a in (adaylar if 'adaylar' in dir() else [])
                       if h_bas.isoformat() <= a.olusturma_tarihi[:10] <= h_bit.isoformat())
        haftalik_post.append(h_post)
        haftalik_kayit.append(h_kayit)

    # Etki skoru hesapla (basit korelasyon)
    # Post artisi + kayit artisi = pozitif etki
    if len(haftalik_post) >= 2 and sum(haftalik_post) > 0:
        son_post = haftalik_post[-1]
        ort_post = sum(haftalik_post[:-1]) / max(len(haftalik_post) - 1, 1)
        son_kayit = haftalik_kayit[-1]
        ort_kayit = sum(haftalik_kayit[:-1]) / max(len(haftalik_kayit) - 1, 1)
        post_degisim = (son_post - ort_post) / max(ort_post, 1)
        kayit_degisim = (son_kayit - ort_kayit) / max(ort_kayit, 1)
        etki_skor = round(50 + (post_degisim * 15) + (kayit_degisim * 20) + (memnuniyet * 3), 1)
        etki_skor = max(0, min(100, etki_skor))
    else:
        etki_skor = 50

    e_renk = "#10b981" if etki_skor >= 65 else "#f59e0b" if etki_skor >= 40 else "#ef4444"

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 100%);
                border:2px solid {e_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {e_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">
            Sosyal Medya Etki Skoru</div>
        <div style="font-size:64px;font-weight:900;color:{e_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{etki_skor}</div>
        <div style="font-size:12px;color:#fde68a;">
            {len(yayinlanan)} yayin · {kayit_toplam} aday · {memnuniyet}/5 memnuniyet</div>
    </div>""", unsafe_allow_html=True)

    # ── KORELASYON KARTLARI ──
    styled_section("Moduller Arasi Etki Haritasi")

    korelasyonlar = [
        {"kaynak": "Post Sayisi", "hedef": "Kayit Adayi", "kaynak_val": len(yayinlanan),
         "hedef_val": kayit_toplam, "yorum": "Daha fazla post = daha fazla aday?",
         "renk": "#2563eb"},
        {"kaynak": "Kampanya Post", "hedef": "UTM Aday",
         "kaynak_val": sum(1 for p in yayinlanan if p.get("kampanya")),
         "hedef_val": sum(1 for a in (adaylar if 'adaylar' in dir() else []) if a.utm_campaign),
         "yorum": "Kampanya postlari aday getiriyor mu?", "renk": "#f59e0b"},
        {"kaynak": "Negatif Yorum", "hedef": "Memnuniyet",
         "kaynak_val": sum(1 for m in _lj(os.path.join(td, "smm_inbox.json"))
                           if m.get("sentiment") in ("negatif", "negative")),
         "hedef_val": f"{memnuniyet}/5", "yorum": "Negatif artinca memnuniyet duser mu?",
         "renk": "#ef4444"},
        {"kaynak": "Referans Post", "hedef": "Referans Aday",
         "kaynak_val": sum(1 for p in yayinlanan if "referans" in (p.get("metin", "") or "").lower()),
         "hedef_val": kayit_referans, "yorum": "Referans icerigi referans adayi artirir mi?",
         "renk": "#7c3aed"},
    ]

    for kor in korelasyonlar:
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {kor['renk']}30;border-left:4px solid {kor['renk']};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-weight:700;color:#e2e8f0;font-size:13px;">
                        {kor['kaynak']} → {kor['hedef']}</span>
                    <div style="font-size:10px;color:#64748b;margin-top:2px;">{kor['yorum']}</div>
                </div>
                <div style="display:flex;gap:12px;align-items:center;">
                    <div style="text-align:center;">
                        <div style="font-size:18px;font-weight:800;color:{kor['renk']};">{kor['kaynak_val']}</div>
                        <div style="font-size:8px;color:#64748b;">Kaynak</div></div>
                    <div style="font-size:16px;color:#64748b;">→</div>
                    <div style="text-align:center;">
                        <div style="font-size:18px;font-weight:800;color:#10b981;">{kor['hedef_val']}</div>
                        <div style="font-size:8px;color:#64748b;">Hedef</div></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── 8 HAFTALIK TREND ──
    styled_section("8 Haftalik Post vs Kayit Trendi")
    max_val = max(max(haftalik_post, default=1), max(haftalik_kayit, default=1), 1)
    for i in range(8):
        hafta_label = f"{'Bu Hafta' if i == 7 else f'{8-i} H. Once'}"
        p_val = haftalik_post[i]
        k_val = haftalik_kayit[i]
        p_w = round(p_val / max_val * 100)
        k_w = round(k_val / max_val * 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
            <span style="min-width:70px;font-size:10px;color:{'#fbbf24' if i == 7 else '#94a3b8'};
                        font-weight:{'800' if i == 7 else '400'};">{hafta_label}</span>
            <div style="flex:1;display:flex;gap:3px;">
                <div style="flex:1;background:#1e293b;border-radius:3px;height:10px;overflow:hidden;">
                    <div style="width:{p_w}%;height:100%;background:#6366f1;border-radius:3px;"></div></div>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:10px;overflow:hidden;">
                    <div style="width:{k_w}%;height:100%;background:#10b981;border-radius:3px;"></div></div>
            </div>
            <span style="min-width:40px;font-size:9px;color:#6366f1;">{p_val}P</span>
            <span style="min-width:40px;font-size:9px;color:#10b981;">{k_val}A</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:12px;font-size:9px;color:#64748b;margin-top:4px;">
        <span>🟣 Post Sayisi</span><span>🟢 Yeni Aday</span>
    </div>""", unsafe_allow_html=True)

    # ── AI INSIGHT ──
    st.divider()
    if st.button("AI Etki Analizi", key="etki_ai", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = (f"Yayinlanan: {len(yayinlanan)}, Kayit Aday: {kayit_toplam}, Kesin: {kayit_kesin}, "
                        f"Referans: {kayit_referans}, Memnuniyet: {memnuniyet}/5, Sikayet: {len(sikayetler)}, "
                        f"Etki Skor: {etki_skor}/100, Haftalik Post: {haftalik_post}, Haftalik Aday: {haftalik_kayit}")
                with st.spinner("AI analiz ediyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul sosyal medya ROI analistisin. Verilen verileri analiz et. Sosyal medyanin okula etkisini degerlendir. Somut oneriler sun. Turkce."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Etki Degerlendirmesi</div>
                        <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API anahtari bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
