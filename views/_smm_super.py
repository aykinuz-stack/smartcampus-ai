"""
Sosyal Medya Yonetimi — Super Ozellikleri
===========================================
1. Kriz Yonetim Merkezi (Crisis War Room)
2. Veli Elci Programi (Brand Ambassador System)
3. Icerik DNA Analizi + Akilli Takvim Uretici
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
# 1. KRİZ YÖNETİM MERKEZİ (CRISIS WAR ROOM)
# ============================================================

_KRIZ_SEVIYELERI = {
    "yesil": {"label": "Normal", "renk": "#10b981", "ikon": "🟢", "esik": 0},
    "sari": {"label": "Dikkat", "renk": "#f59e0b", "ikon": "🟡", "esik": 15},
    "turuncu": {"label": "Uyari", "renk": "#f97316", "ikon": "🟠", "esik": 25},
    "kirmizi": {"label": "KRIZ", "renk": "#ef4444", "ikon": "🔴", "esik": 35},
}

_KRIZ_YANIT_SABLONLARI = {
    "servis": "Degerli velimiz, servis hizmetimizle ilgili yasadiginiz olumsuzluktan dolayi ozur dileriz. Konu ilgili birime iletilmistir ve en kisa surede cozume kavusturulacaktir.",
    "akademik": "Degerli velimiz, akademik kalitemizi surekli gelistirmek oncelikli hedefimizdir. Geri bildiriminiz icin tesekkur ederiz, ilgili ogretmenimiz sizinle iletisime gececektir.",
    "guvenlik": "Degerli velimiz, ogrencilerimizin guvenligi en onemli onceliğimizdir. Belirttiginiz konu hakkinda acil inceleme baslatilmistir.",
    "genel": "Degerli velimiz, geri bildiriminiz icin tesekkur ederiz. Konuyu en kisa surede degerlendirip sizinle paylasacagiz.",
    "yemek": "Degerli velimiz, yemek hizmetimiz konusundaki geri bildiriminizi dikkate aliyoruz. Mutfak ekibimizle gorusme planlanmistir.",
}


def render_kriz_yonetim():
    """Sosyal medya kriz yonetim merkezi."""
    styled_section("Kriz Yonetim Merkezi", "#ef4444")
    styled_info_banner(
        "Olumsuz yorumlardaki ani artislari otomatik algila. "
        "Hazir yanit sablonlari + eskalasyon zinciri + AI kriz cevap uretici.",
        banner_type="warning", icon="🚨")

    td = _td()

    # Inbox verisi yukle (sentiment analizi icin)
    inbox = _lj(os.path.join(td, "smm_inbox.json"))
    try:
        from models.sosyal_medya import get_smm_store
        store = get_smm_store()
        inbox = store.load_list("inbox") or inbox
    except Exception:
        pass

    alerts = _lj(os.path.join(td, "smm_alerts.json"))
    sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))

    # Sentiment analizi
    bugun = date.today().isoformat()
    son_24s = (date.today() - timedelta(days=1)).isoformat()
    son_7g = (date.today() - timedelta(days=7)).isoformat()

    bugun_mesajlar = [m for m in inbox if (m.get("created_at", m.get("tarih", "")) or "")[:10] >= son_24s]
    negatif_24s = sum(1 for m in bugun_mesajlar if m.get("sentiment", m.get("duygu", "")) in ("negatif", "negative", "olumsuz"))
    notr_24s = sum(1 for m in bugun_mesajlar if m.get("sentiment", m.get("duygu", "")) in ("notr", "neutral"))
    pozitif_24s = sum(1 for m in bugun_mesajlar if m.get("sentiment", m.get("duygu", "")) in ("pozitif", "positive", "olumlu"))
    toplam_24s = max(len(bugun_mesajlar), 1)
    negatif_oran = round(negatif_24s / toplam_24s * 100, 1)

    # Son 7 gun sikayet trendi
    son7_sikayet = sum(1 for s in sikayetler if (s.get("created_at", "") or "")[:10] >= son_7g)
    aktif_alarm = sum(1 for a in alerts if a.get("status") == "open" or a.get("aktif"))

    # Kriz seviyesi hesapla
    kriz_puan = negatif_oran + (aktif_alarm * 5) + (son7_sikayet * 2)
    if kriz_puan >= 35:
        seviye = _KRIZ_SEVIYELERI["kirmizi"]
    elif kriz_puan >= 25:
        seviye = _KRIZ_SEVIYELERI["turuncu"]
    elif kriz_puan >= 15:
        seviye = _KRIZ_SEVIYELERI["sari"]
    else:
        seviye = _KRIZ_SEVIYELERI["yesil"]

    # ── KRİZ HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,{'#7f1d1d' if kriz_puan >= 25 else '#1e293b'} 100%);
                border:2px solid {seviye['renk']};border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {seviye['renk']}30;text-align:center;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,{seviye['renk']},{seviye['renk']},transparent);"></div>
        <div style="font-size:10px;color:#94a3b8;letter-spacing:3px;text-transform:uppercase;">Kriz Seviyesi</div>
        <div style="font-size:72px;margin:8px 0;">{seviye['ikon']}</div>
        <div style="font-size:28px;font-weight:900;color:{seviye['renk']};
                    font-family:Playfair Display,Georgia,serif;">{seviye['label']}</div>
        <div style="font-size:12px;color:#94a3b8;margin-top:6px;">
            Puan: {kriz_puan:.0f} · Negatif oran: %{negatif_oran} · Aktif alarm: {aktif_alarm} · Sikayet (7g): {son7_sikayet}</div>

        <!-- TERMOMETRE -->
        <div style="margin:16px auto 0;max-width:350px;">
            <div style="display:flex;justify-content:space-between;font-size:8px;color:#64748b;margin-bottom:3px;">
                <span>0 Normal</span><span>15</span><span>25</span><span>35+ KRIZ</span></div>
            <div style="background:linear-gradient(90deg,#10b981,#f59e0b,#f97316,#ef4444);
                        border-radius:6px;height:12px;position:relative;">
                <div style="position:absolute;left:{min(kriz_puan, 50) / 50 * 100}%;top:-3px;transform:translateX(-50%);
                            width:4px;height:18px;background:#fff;border-radius:2px;
                            box-shadow:0 0 8px rgba(255,255,255,0.5);"></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── DURUM KARTLARI ──
    styled_stat_row([
        ("Son 24s Mesaj", str(len(bugun_mesajlar)), "#2563eb", "📬"),
        ("Negatif", str(negatif_24s), "#ef4444", "😡"),
        ("Notr", str(notr_24s), "#f59e0b", "😐"),
        ("Pozitif", str(pozitif_24s), "#10b981", "😊"),
        ("Aktif Alarm", str(aktif_alarm), "#dc2626", "🚨"),
    ])

    sub = st.tabs(["📋 Negatif Mesajlar", "💬 Hazir Yanitlar", "🤖 AI Kriz Yanit"])

    # ═══ NEGATİF MESAJLAR ═══
    with sub[0]:
        styled_section("Son 7 Gun Negatif Mesajlar")
        negatifler = [m for m in inbox
                       if (m.get("created_at", m.get("tarih", "")) or "")[:10] >= son_7g
                       and m.get("sentiment", m.get("duygu", "")) in ("negatif", "negative", "olumsuz")]

        if not negatifler:
            st.success("Son 7 gunde negatif mesaj yok!")
        else:
            for m in negatifler[:20]:
                tarih = (m.get("created_at", m.get("tarih", "")) or "")[:10]
                metin = m.get("metin", m.get("message", m.get("icerik", "")))[:200]
                platform = m.get("platform", "?")
                gonderen = m.get("gonderen", m.get("from", "Anonim"))
                st.markdown(f"""
                <div style="background:#450a0a;border:1px solid #ef4444;border-left:4px solid #ef4444;
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;font-size:10px;color:#fca5a5;margin-bottom:4px;">
                        <span>{gonderen} · {platform}</span><span>{tarih}</span></div>
                    <div style="font-size:12px;color:#fca5a5;">{metin}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ HAZIR YANITLAR ═══
    with sub[1]:
        styled_section("Kriz Yanit Sablonlari")
        for tur, sablon in _KRIZ_YANIT_SABLONLARI.items():
            with st.expander(f"📋 {tur.replace('_', ' ').title()}", expanded=False):
                st.text_area(f"Sablon — {tur}", value=sablon, height=80, key=f"kriz_sab_{tur}")
                st.caption("Kopyalayip sosyal medya yanitinizda kullanabilirsiniz.")

    # ═══ AI KRİZ YANIT ═══
    with sub[2]:
        styled_section("AI Kriz Yanit Uretici")
        kriz_metin = st.text_area("Kriz durumunu veya gelen mesaji yazin...", key="kriz_ai_metin", height=100,
                                    placeholder="Ornek: Veliler servislerin gecikmesinden sikayet ediyor...")
        kriz_platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "WhatsApp", "Genel"], key="kriz_ai_plat")

        if st.button("AI Yanit Uret", key="kriz_ai_btn", type="primary"):
            if kriz_metin:
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if client:
                        with st.spinner("AI profesyonel yanit uretiyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul sosyal medya kriz yonetim uzmanisin. Verilen olumsuz duruma/mesaja profesyonel, sakinlestirici, cozum odakli 3 farkli yanit uret: 1) Kisa (tweet/DM) 2) Orta (yorum yaniti) 3) Uzun (resmi aciklama). Turkce yaz. Platform: " + kriz_platform},
                                    {"role": "user", "content": kriz_metin},
                                ],
                                max_tokens=600, temperature=0.6,
                            )
                            ai = resp.choices[0].message.content or ""
                        if ai:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                        border-radius:14px;padding:16px 20px;">
                                <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Kriz Yanit Onerileri</div>
                                <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("OpenAI API anahtari bulunamadi.")
                except Exception as e:
                    st.error(f"Hata: {e}")


# ============================================================
# 2. VELİ ELÇİ PROGRAMI (BRAND AMBASSADOR)
# ============================================================

def _elci_path() -> str:
    return os.path.join(_td(), "smm_veli_elciler.json")


def _load_elciler() -> list[dict]:
    return _lj(_elci_path())


def _save_elciler(data: list[dict]):
    _sj(_elci_path(), data)


_AKSIYON_PUANLARI = {
    "begeni": {"puan": 2, "label": "Post Begendi", "ikon": "👍"},
    "yorum": {"puan": 5, "label": "Post Yorumu", "ikon": "💬"},
    "paylasim": {"puan": 10, "label": "Post Paylasti", "ikon": "🔄"},
    "kendi_post": {"puan": 20, "label": "Kendi Postu", "ikon": "📸"},
    "referans": {"puan": 30, "label": "Referans Getirdi", "ikon": "🔗"},
    "google_yorum": {"puan": 25, "label": "Google Yorum", "ikon": "⭐"},
}

_ODUL_KATMANLARI = [
    {"esik": 50, "ad": "Bronz Elci", "ikon": "🥉", "renk": "#cd7f32", "odul": "Dijital Tesekkur Karti"},
    {"esik": 100, "ad": "Gumus Elci", "ikon": "🥈", "renk": "#C0C0C0", "odul": "%5 Indirim Kuponu"},
    {"esik": 200, "ad": "Altin Elci", "ikon": "🥇", "renk": "#FFD700", "odul": "VIP Etkinlik Daveti"},
    {"esik": 500, "ad": "Platin Elci", "ikon": "💎", "renk": "#E5E4E2", "odul": "Yillik Odul Toreninde Takdir"},
]


def _elci_katman(puan: int) -> dict:
    katman = {"ad": "Aday", "ikon": "🌱", "renk": "#94a3b8", "odul": ""}
    for k in _ODUL_KATMANLARI:
        if puan >= k["esik"]:
            katman = k
    return katman


def render_veli_elci():
    """Veli elci programi — gamification ile organik buyume."""
    styled_section("Veli Elci Programi", "#f59e0b")
    styled_info_banner(
        "Memnun velileri gonullu marka elcisine donusturun. "
        "Puanlama + odul katmanlari + liderlik tablosu.",
        banner_type="info", icon="🌟")

    elciler = _load_elciler()

    toplam_puan = sum(e.get("puan", 0) for e in elciler)
    aktif = sum(1 for e in elciler if e.get("puan", 0) > 0)

    styled_stat_row([
        ("Toplam Elci", str(len(elciler)), "#f59e0b", "🌟"),
        ("Aktif Elci", str(aktif), "#10b981", "✅"),
        ("Toplam Puan", str(toplam_puan), "#7c3aed", "⭐"),
    ])

    sub = st.tabs(["🏆 Liderlik Tablosu", "➕ Elci / Puan Ekle", "🎁 Odul Katmanlari"])

    # ═══ LİDERLİK TABLOSU ═══
    with sub[0]:
        styled_section("Elci Sampiyonlari")
        if not elciler:
            styled_info_banner("Henuz elci yok. 'Elci Ekle' sekmesinden baslatin.", banner_type="info", icon="🌟")
        else:
            sirali = sorted(elciler, key=lambda e: -e.get("puan", 0))
            for sira, e in enumerate(sirali[:20], 1):
                puan = e.get("puan", 0)
                katman = _elci_katman(puan)
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                en_yuksek = max(el.get("puan", 0) for el in sirali) or 1
                bar_w = round(puan / en_yuksek * 100)

                aksiyonlar = e.get("aksiyonlar", [])
                son_aksiyon = aksiyonlar[-1] if aksiyonlar else {}
                son_txt = f"{son_aksiyon.get('tip', '')} ({son_aksiyon.get('tarih', '')[:10]})" if son_aksiyon else "—"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {katman['renk']}40;border-radius:12px;
                            padding:12px 16px;margin-bottom:6px;display:flex;align-items:center;gap:14px;">
                    <div style="font-size:22px;min-width:36px;text-align:center;">{madalya}</div>
                    <div style="flex:1;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{e.get('ad', '')}</span>
                            <div style="display:flex;gap:6px;align-items:center;">
                                <span style="font-size:12px;">{katman['ikon']}</span>
                                <span style="background:{katman['renk']}20;color:{katman['renk']};padding:2px 8px;
                                            border-radius:6px;font-size:10px;font-weight:700;">{katman['ad']}</span>
                            </div>
                        </div>
                        <div style="display:flex;gap:12px;font-size:10px;color:#94a3b8;margin-top:2px;">
                            <span>Puan: <b style="color:#fbbf24;">{puan}</b></span>
                            <span>Aksiyon: {len(aksiyonlar)}</span>
                            <span>Son: {son_txt}</span>
                        </div>
                        <div style="margin-top:4px;background:#1e293b;border-radius:3px;height:4px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{katman['renk']};border-radius:3px;"></div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ═══ ELÇİ / PUAN EKLE ═══
    with sub[1]:
        styled_section("Elci Kayit / Puan Ekle")

        mode = st.radio("Islem", ["Yeni Elci Ekle", "Mevcut Elciye Puan Ekle"], horizontal=True, key="elci_mode")

        if mode == "Yeni Elci Ekle":
            with st.form("elci_yeni"):
                ad = st.text_input("Veli Adi Soyadi")
                telefon = st.text_input("Telefon (istege bagli)")
                ogrenci = st.text_input("Ogrenci Adi")
                if st.form_submit_button("Elci Ekle", type="primary"):
                    if ad:
                        yeni = {
                            "id": f"elci_{uuid.uuid4().hex[:8]}",
                            "ad": ad.strip(), "telefon": telefon, "ogrenci": ogrenci,
                            "puan": 0, "aksiyonlar": [],
                            "created_at": datetime.now().isoformat(),
                        }
                        elciler.append(yeni)
                        _save_elciler(elciler)
                        st.success(f"Elci eklendi: {ad}")
                        st.rerun()
        else:
            if not elciler:
                st.info("Henuz elci yok.")
            else:
                secili = st.selectbox("Elci Secin", [e["ad"] for e in elciler], key="elci_sec")
                aksiyon = st.selectbox("Aksiyon Turu",
                    list(_AKSIYON_PUANLARI.keys()),
                    format_func=lambda x: f"{_AKSIYON_PUANLARI[x]['ikon']} {_AKSIYON_PUANLARI[x]['label']} (+{_AKSIYON_PUANLARI[x]['puan']}p)",
                    key="elci_aksiyon")
                not_txt = st.text_input("Not (istege bagli)", key="elci_not")

                if st.button("Puan Ekle", key="elci_puan_btn", type="primary"):
                    for e in elciler:
                        if e["ad"] == secili:
                            puan_info = _AKSIYON_PUANLARI[aksiyon]
                            e["puan"] = e.get("puan", 0) + puan_info["puan"]
                            e.setdefault("aksiyonlar", []).append({
                                "tip": aksiyon, "puan": puan_info["puan"],
                                "not": not_txt, "tarih": datetime.now().isoformat(),
                            })
                            _save_elciler(elciler)
                            st.success(f"+{puan_info['puan']} puan eklendi! Toplam: {e['puan']}")
                            st.rerun()

    # ═══ ÖDÜL KATMANLARI ═══
    with sub[2]:
        styled_section("Odul Katmanlari")
        for k in _ODUL_KATMANLARI:
            elci_sayisi = sum(1 for e in elciler if e.get("puan", 0) >= k["esik"])
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {k['renk']}40;border-left:5px solid {k['renk']};
                        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:18px;">{k['ikon']}</span>
                        <span style="font-weight:800;color:{k['renk']};font-size:14px;margin-left:8px;">{k['ad']}</span>
                        <span style="color:#94a3b8;font-size:11px;margin-left:8px;">({k['esik']}+ puan)</span>
                    </div>
                    <span style="background:{k['renk']}20;color:{k['renk']};padding:3px 10px;border-radius:6px;
                                font-size:11px;font-weight:700;">{elci_sayisi} elci</span>
                </div>
                <div style="font-size:11px;color:#64748b;margin-top:4px;">Odul: {k['odul']}</div>
            </div>""", unsafe_allow_html=True)

        # Aksiyon puanlari tablosu
        styled_section("Aksiyon Puanlari")
        for key, info in _AKSIYON_PUANLARI.items():
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                <span style="font-size:16px;min-width:24px;">{info['ikon']}</span>
                <span style="flex:1;font-size:12px;color:#e2e8f0;">{info['label']}</span>
                <span style="background:#fbbf2420;color:#fbbf24;padding:2px 10px;border-radius:6px;
                            font-size:12px;font-weight:800;">+{info['puan']}</span>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 3. İÇERİK DNA ANALİZİ + AKILLI TAKVİM ÜRETİCİ
# ============================================================

_GUNLER = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
_SAAT_DILIMLERI = ["07:00-09:00", "09:00-12:00", "12:00-14:00", "14:00-17:00", "17:00-19:00", "19:00-22:00"]


def render_icerik_dna():
    """Gecmis postlarin DNA analizi + otomatik takvim uretici."""
    styled_section("Icerik DNA Analizi", "#6366f1")
    styled_info_banner(
        "Gecmis postlarinizi analiz ederek basarili icerigin DNA'sini cikarir. "
        "Sonuclara dayanarak otomatik haftalik/aylik takvim olusturur.",
        banner_type="info", icon="🧬")

    td = _td()
    posts = _lj(os.path.join(td, "smm_posts.json"))
    try:
        from models.sosyal_medya import get_smm_store
        store = get_smm_store()
        posts = store.load_list("posts") or posts
    except Exception:
        pass

    yayinlanan = [p for p in posts if p.get("status") == "PUBLISHED"]

    sub = st.tabs(["🧬 DNA Analizi", "📅 Akilli Takvim Uretici"])

    # ═══ DNA ANALİZİ ═══
    with sub[0]:
        if not yayinlanan:
            styled_info_banner("DNA analizi icin en az 1 yayinlanmis post gerekli.", banner_type="warning", icon="📊")
        else:
            styled_stat_row([
                ("Toplam Yayinlanan", str(len(yayinlanan)), "#6366f1", "📊"),
            ])

            # 1. En iyi gun
            styled_section("En Iyi Yayin Gunu")
            gun_sayac = Counter()
            for p in yayinlanan:
                tarih = p.get("yayin_tarihi", p.get("planlanan_tarih", ""))
                if tarih and len(tarih) >= 10:
                    try:
                        dt = date.fromisoformat(tarih[:10])
                        gun_sayac[_GUNLER[dt.weekday()]] += 1
                    except Exception:
                        pass

            if gun_sayac:
                en_iyi_gun = gun_sayac.most_common(1)[0]
                en_cok = en_iyi_gun[1]
                for gun in _GUNLER:
                    sayi = gun_sayac.get(gun, 0)
                    bar_w = round(sayi / max(en_cok, 1) * 100)
                    is_best = gun == en_iyi_gun[0]
                    renk = "#fbbf24" if is_best else "#6366f1"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                        <span style="min-width:80px;font-size:11px;color:{'#fbbf24' if is_best else '#94a3b8'};
                                    font-weight:{'800' if is_best else '400'};">{'⭐ ' if is_best else ''}{gun}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                        display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                    </div>""", unsafe_allow_html=True)

            # 2. En iyi platform
            styled_section("En Iyi Platform")
            platform_sayac = Counter(p.get("platform", "?") for p in yayinlanan)
            if platform_sayac:
                en_iyi_plat = platform_sayac.most_common(1)[0]
                for plat, sayi in platform_sayac.most_common():
                    is_best = plat == en_iyi_plat[0]
                    bar_w = round(sayi / max(en_iyi_plat[1], 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                        <span style="min-width:100px;font-size:11px;color:{'#fbbf24' if is_best else '#94a3b8'};
                                    font-weight:{'800' if is_best else '400'};">{'⭐ ' if is_best else ''}{plat}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:#6366f1;border-radius:3px;
                                        display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                    </div>""", unsafe_allow_html=True)

            # 3. En cok kullanilan hashtag
            styled_section("En Basarili Hashtag'ler")
            hashtag_sayac = Counter()
            for p in yayinlanan:
                tags = p.get("hashtagler", p.get("hashtags", []))
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split("#") if t.strip()]
                elif isinstance(tags, list):
                    pass
                else:
                    tags = []
                for t in tags:
                    hashtag_sayac[t] += 1

            if hashtag_sayac:
                for tag, sayi in hashtag_sayac.most_common(10):
                    st.markdown(f"- **#{tag}** — {sayi} kez kullanildi")
            else:
                st.caption("Hashtag verisi bulunamadi.")

            # 4. Post sikligi
            styled_section("Optimal Post Sikligi")
            if len(yayinlanan) >= 2:
                tarihler = sorted(set(
                    (p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "")[:10]
                    for p in yayinlanan if p.get("yayin_tarihi") or p.get("planlanan_tarih")
                ))
                if len(tarihler) >= 2:
                    try:
                        ilk = date.fromisoformat(tarihler[0])
                        son = date.fromisoformat(tarihler[-1])
                        gun_farki = max((son - ilk).days, 1)
                        haftalik = round(len(yayinlanan) / (gun_farki / 7), 1)
                        st.markdown(f"""
                        <div style="background:#0f172a;border:1px solid #6366f1;border-radius:12px;
                                    padding:14px;text-align:center;">
                            <div style="font-size:36px;font-weight:900;color:#6366f1;">{haftalik}</div>
                            <div style="font-size:11px;color:#94a3b8;">post / hafta (mevcut ortalama)</div>
                            <div style="font-size:10px;color:#64748b;margin-top:4px;">
                                {len(yayinlanan)} post · {gun_farki} gun · Oneri: Haftada {max(3, round(haftalik * 1.2))} post</div>
                        </div>""", unsafe_allow_html=True)
                    except Exception:
                        pass

            # 5. DNA Ozet
            styled_section("DNA Ozet Karti")
            en_iyi_g = gun_sayac.most_common(1)[0][0] if gun_sayac else "?"
            en_iyi_p = platform_sayac.most_common(1)[0][0] if platform_sayac else "?"
            en_iyi_h = hashtag_sayac.most_common(1)[0][0] if hashtag_sayac else "?"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:2px solid #7c3aed;
                        border-radius:16px;padding:18px 22px;">
                <div style="font-size:13px;color:#c4b5fd;font-weight:700;margin-bottom:10px;">Icerik DNA'niz</div>
                <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;font-size:12px;color:#e0e7ff;">
                    <div>En iyi gun: <b style="color:#fbbf24;">{en_iyi_g}</b></div>
                    <div>En iyi platform: <b style="color:#fbbf24;">{en_iyi_p}</b></div>
                    <div>Top hashtag: <b style="color:#fbbf24;">#{en_iyi_h}</b></div>
                    <div>Toplam post: <b style="color:#fbbf24;">{len(yayinlanan)}</b></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ AKILLI TAKVİM ÜRETİCİ ═══
    with sub[1]:
        styled_section("AI Akilli Takvim Uretici")
        styled_info_banner(
            "DNA sonuclarina dayanarak otomatik haftalik/aylik icerik takvimi olusturur.",
            banner_type="info", icon="📅")

        hafta_sayisi = st.selectbox("Kac haftalik plan?", [1, 2, 4], index=0, key="dna_hafta")
        post_adet = st.slider("Haftalik post sayisi", 2, 10, 5, key="dna_post_adet")

        if st.button("Takvim Olustur", key="dna_takvim_btn", type="primary", use_container_width=True):
            # DNA'dan en iyi parametreleri al
            gun_sira = [g for g, _ in (Counter(
                _GUNLER[date.fromisoformat((p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "0001-01-01")[:10]).weekday()]
                for p in yayinlanan if (p.get("yayin_tarihi") or p.get("planlanan_tarih", ""))[:4] != "0001"
            ).most_common())] if yayinlanan else _GUNLER[:5]

            if not gun_sira:
                gun_sira = _GUNLER[:5]

            platform_sira = [p for p, _ in Counter(p.get("platform", "instagram") for p in yayinlanan).most_common()] if yayinlanan else ["instagram"]

            konular = ["Akademik basari", "Etkinlik/kulup", "Gunluk yasam", "Motivasyon",
                        "Ogretmen tanitim", "Kayit kampanya", "Veli referans", "Bilgilendirme"]

            # Takvim uret
            plan = []
            bugun = date.today()
            hafta_bas = bugun - timedelta(days=bugun.weekday())  # Pazartesi

            for h in range(hafta_sayisi):
                for post_idx in range(post_adet):
                    gun_idx = post_idx % len(gun_sira)
                    gun_str = gun_sira[gun_idx]
                    gun_no = _GUNLER.index(gun_str)
                    post_tarih = hafta_bas + timedelta(weeks=h, days=gun_no)
                    saat = ["09:00", "12:00", "17:00", "19:00", "20:00"][post_idx % 5]
                    platform = platform_sira[post_idx % len(platform_sira)]
                    konu = konular[post_idx % len(konular)]

                    plan.append({
                        "tarih": post_tarih.isoformat(),
                        "gun": gun_str, "saat": saat,
                        "platform": platform, "konu": konu,
                    })

            # Goster
            styled_section(f"{hafta_sayisi} Haftalik Plan ({len(plan)} post)")
            for h in range(hafta_sayisi):
                hafta_plan = [p for p in plan if (date.fromisoformat(p["tarih"]) - hafta_bas).days // 7 == h]
                with st.expander(f"Hafta {h + 1} ({len(hafta_plan)} post)", expanded=h == 0):
                    for p in hafta_plan:
                        p_renk = {"instagram": "#E4405F", "facebook": "#1877F2", "tiktok": "#000",
                                   "youtube": "#FF0000", "linkedin": "#0A66C2"}.get(p["platform"], "#64748b")
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:10px;padding:4px 0;
                                    border-bottom:1px solid #1e293b;">
                            <span style="min-width:70px;font-size:10px;color:#94a3b8;">{p['tarih'][5:]}</span>
                            <span style="min-width:60px;font-size:10px;color:#e2e8f0;font-weight:600;">{p['gun'][:3]}</span>
                            <span style="min-width:40px;font-size:10px;color:#64748b;">{p['saat']}</span>
                            <span style="background:{p_renk}20;color:{p_renk};padding:1px 8px;
                                        border-radius:4px;font-size:9px;font-weight:700;">{p['platform']}</span>
                            <span style="font-size:11px;color:#e2e8f0;flex:1;">{p['konu']}</span>
                        </div>""", unsafe_allow_html=True)
