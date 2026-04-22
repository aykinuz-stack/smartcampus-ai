"""
Sosyal Medya Yonetimi — Zirve Ozellikleri
===========================================
1. Sosyal Medya Komuta Merkezi (Social Command Center)
2. Okul Icerik Fabrikasi (AI Content Factory)
3. Kampanya Performans & ROI Takip Sistemi
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


def _store():
    try:
        from models.sosyal_medya import get_smm_store
        return get_smm_store()
    except Exception:
        return None


_PLATFORM_INFO = {
    "instagram": {"ikon": "📸", "renk": "#E4405F", "label": "Instagram"},
    "facebook": {"ikon": "📘", "renk": "#1877F2", "label": "Facebook"},
    "tiktok": {"ikon": "🎵", "renk": "#000000", "label": "TikTok"},
    "youtube": {"ikon": "🎬", "renk": "#FF0000", "label": "YouTube"},
    "linkedin": {"ikon": "💼", "renk": "#0A66C2", "label": "LinkedIn"},
    "x_twitter": {"ikon": "🐦", "renk": "#1DA1F2", "label": "X/Twitter"},
    "whatsapp_business": {"ikon": "💬", "renk": "#25D366", "label": "WhatsApp"},
    "email": {"ikon": "📧", "renk": "#4285F4", "label": "E-posta"},
}


# ============================================================
# 1. SOSYAL MEDYA KOMUTA MERKEZİ
# ============================================================

def render_komuta_merkezi():
    """Tum platformlarin canli durumu tek ekranda."""
    styled_section("Sosyal Medya Komuta Merkezi", "#E4405F")

    store = _store()
    td = _td()
    bugun = date.today().isoformat()

    # Veri yukle
    posts = _lj(os.path.join(td, "smm_posts.json"))
    accounts = _lj(os.path.join(td, "smm_accounts.json"))
    inbox = _lj(os.path.join(td, "smm_inbox.json"))
    alerts = _lj(os.path.join(td, "smm_alerts.json"))

    if store:
        try:
            posts = store.load_list("posts") or posts
            accounts = store.load_list("accounts") or accounts
            inbox = store.load_list("inbox") or inbox
            alerts = store.load_list("alerts") or alerts
        except Exception:
            pass

    # Istatistikler
    toplam_post = len(posts)
    yayinlanan = sum(1 for p in posts if p.get("status") == "PUBLISHED")
    taslak = sum(1 for p in posts if p.get("status") in ("DRAFT", "READY_TO_PUBLISH"))
    planli = sum(1 for p in posts if p.get("status") == "SCHEDULED")
    onay_bekleyen = sum(1 for p in posts if p.get("status") in ("SUBMITTED", "IN_REVIEW"))
    bugun_post = sum(1 for p in posts if (p.get("planlanan_tarih", "") or "")[:10] == bugun)
    cevapsiz_inbox = sum(1 for m in inbox if not m.get("cevaplandi") and not m.get("replied"))
    aktif_alarm = sum(1 for a in alerts if a.get("status") == "open" or a.get("aktif"))

    # Son 7 gun yayinlanan
    yedi_gun = (date.today() - timedelta(days=7)).isoformat()
    son7_yayin = sum(1 for p in posts if p.get("status") == "PUBLISHED"
                     and (p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "")[:10] >= yedi_gun)

    # Platform bazli post dagilimi
    platform_sayac = Counter(p.get("platform", "bilinmiyor") for p in posts if p.get("status") == "PUBLISHED")

    # ── KOMUTA HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#3b0764 50%,#581c87 100%);
                border:2px solid #a855f7;border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(168,85,247,0.25);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#E4405F,#1877F2,#25D366,#FF0000,#E4405F);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:10px;color:#c4b5fd;letter-spacing:3px;text-transform:uppercase;">
                    SmartCampus AI</div>
                <div style="font-size:28px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;">Social Command Center</div>
            </div>
            <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:14px;padding:12px 20px;">
                <div style="font-size:36px;font-weight:900;color:#a855f7;line-height:1;">{toplam_post}</div>
                <div style="font-size:9px;color:#c4b5fd;">Toplam Post</div>
            </div>
        </div>

        <!-- ANA SAYAÇLAR -->
        <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-bottom:14px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#10b981;">{yayinlanan}</div>
                <div style="font-size:8px;color:#c4b5fd;">Yayinlanan</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#f59e0b;">{planli + taslak}</div>
                <div style="font-size:8px;color:#c4b5fd;">Taslak/Planli</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#3b82f6;">{bugun_post}</div>
                <div style="font-size:8px;color:#c4b5fd;">Bugun Plan</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#8b5cf6;">{onay_bekleyen}</div>
                <div style="font-size:8px;color:#c4b5fd;">Onay Bekl.</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#ef4444' if cevapsiz_inbox > 5 else '#f59e0b' if cevapsiz_inbox > 0 else '#10b981'};">{cevapsiz_inbox}</div>
                <div style="font-size:8px;color:#c4b5fd;">Cevapsiz DM</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#ef4444' if aktif_alarm > 0 else '#10b981'};">{aktif_alarm}</div>
                <div style="font-size:8px;color:#c4b5fd;">Aktif Alarm</div></div>
        </div>

        <!-- PLATFORM SAĞLIK KARTLARI -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
    """, unsafe_allow_html=True)

    platform_html = ""
    for p_key, p_info in list(_PLATFORM_INFO.items())[:8]:
        p_posts = sum(1 for p in posts if p.get("platform") == p_key and p.get("status") == "PUBLISHED")
        # Son post tarihi
        p_tarihler = [p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "" for p in posts
                       if p.get("platform") == p_key and p.get("status") == "PUBLISHED"]
        son_post = max(p_tarihler)[:10] if p_tarihler else "Yok"
        # Hesap durumu
        hesap = next((a for a in accounts if a.get("platform") == p_key), None)
        bagli = hesap and hesap.get("status") == "connected"
        durum_renk = "#10b981" if bagli else "#64748b"
        durum_txt = "Bagli" if bagli else "Bagli Degil"

        # Sessizlik
        gun_sessiz = 999
        if p_tarihler and max(p_tarihler):
            try:
                gun_sessiz = (date.today() - date.fromisoformat(max(p_tarihler)[:10])).days
            except Exception:
                pass
        isik = "#10b981" if gun_sessiz <= 2 else "#f59e0b" if gun_sessiz <= 7 else "#ef4444"

        platform_html += f"""
            <div style="background:rgba(0,0,0,0.15);border:1px solid {p_info['renk']}40;border-radius:10px;
                        padding:10px;text-align:center;">
                <div style="font-size:16px;">{p_info['ikon']}</div>
                <div style="font-size:10px;font-weight:700;color:{p_info['renk']};margin:2px 0;">{p_info['label']}</div>
                <div style="font-size:14px;font-weight:800;color:#fff;">{p_posts}</div>
                <div style="font-size:8px;color:#94a3b8;">post</div>
                <div style="display:inline-block;width:6px;height:6px;border-radius:50%;background:{isik};margin-top:4px;"></div>
                <div style="font-size:7px;color:#64748b;">{gun_sessiz}g once</div>
            </div>"""

    st.markdown(f"""{platform_html}
        </div>
    </div>""", unsafe_allow_html=True)

    # ── BUGÜNÜN İÇERİK PLANI ──
    styled_section("Bugunun Icerik Plani")
    bugun_planli = [p for p in posts if (p.get("planlanan_tarih", "") or "")[:10] == bugun
                     and p.get("status") not in ("PUBLISHED",)]
    if bugun_planli:
        for p in bugun_planli:
            p_info = _PLATFORM_INFO.get(p.get("platform", ""), {"ikon": "📋", "renk": "#64748b", "label": "?"})
            saat = (p.get("planlanan_tarih", "") or "")[11:16] or "--:--"
            metin = (p.get("metin", p.get("caption", "")) or "")[:80]
            durum = p.get("status", "?")
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {p_info['renk']}30;border-left:4px solid {p_info['renk']};
                        border-radius:0 10px 10px 0;padding:8px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:12px;color:#e2e8f0;font-weight:600;">
                        {p_info['ikon']} {saat} — {metin}</span>
                    <span style="background:{p_info['renk']}20;color:{p_info['renk']};padding:2px 8px;
                                border-radius:6px;font-size:9px;font-weight:700;">{durum}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        styled_info_banner("Bugun icin planlanmis post yok.", banner_type="info", icon="📅")

    # ── SON 7 GÜN TREND ──
    styled_section(f"Son 7 Gun: {son7_yayin} yayin")
    for i in range(6, -1, -1):
        gun = (date.today() - timedelta(days=i)).isoformat()
        gun_kisa = gun[5:]
        gun_sayi = sum(1 for p in posts if p.get("status") == "PUBLISHED"
                        and (p.get("yayin_tarihi", p.get("planlanan_tarih", "")) or "")[:10] == gun)
        bar_w = min(gun_sayi * 20, 100)
        is_bugun = i == 0
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
            <span style="min-width:50px;font-size:10px;color:{'#a855f7' if is_bugun else '#94a3b8'};
                        font-weight:{'800' if is_bugun else '400'};">{gun_kisa}</span>
            <div style="flex:1;background:#1e293b;border-radius:3px;height:12px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{'#a855f7' if is_bugun else '#6366f1'};border-radius:3px;"></div>
            </div>
            <span style="font-size:11px;font-weight:700;color:#e2e8f0;min-width:20px;">{gun_sayi}</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. OKUL İÇERİK FABRİKASI (AI CONTENT FACTORY)
# ============================================================

_ICERIK_KAYNAKLARI = [
    {"id": "etkinlik", "ikon": "🎭", "label": "Etkinlikler", "renk": "#ea580c",
     "aciklama": "Tamamlanan/yaklasan etkinliklerden post onerisi"},
    {"id": "basari", "ikon": "🏆", "label": "Akademik Basari", "renk": "#f59e0b",
     "aciklama": "Ogrenci/okul basarilarindan kutlama postu"},
    {"id": "kayit", "ikon": "🎯", "label": "Kayit Kampanya", "renk": "#2563eb",
     "aciklama": "Kontenjan/kayit durumundan FOMO icerigi"},
    {"id": "dogum_gunu", "ikon": "🎂", "label": "Dogum Gunu", "renk": "#ec4899",
     "aciklama": "Ogrenci/personel dogum gunu kutlamasi"},
    {"id": "bayram", "ikon": "🇹🇷", "label": "Bayram/Ozel Gun", "renk": "#dc2626",
     "aciklama": "Milli bayram ve ozel gun kutlamasi"},
    {"id": "swot", "ikon": "📊", "label": "Kurumsal Gelisim", "renk": "#7c3aed",
     "aciklama": "SWOT basarilarindan kurumsal gelisim postu"},
]


def render_icerik_fabrikasi():
    """AI ile modullerden otomatik icerik uretimi."""
    styled_section("Icerik Fabrikasi", "#6366f1")
    styled_info_banner(
        "Okulun tum modullerinden otomatik icerik fikirleri + AI ile hazir postlar. "
        "Secin, duzenlein, 1 tikla taslaga ekleyin.",
        banner_type="info", icon="🏭")

    td = _td()

    # ── İÇERİK KAYNAK SEÇİMİ ──
    styled_section("Icerik Kaynagi Secin")
    cols = st.columns(3)
    for idx, kaynak in enumerate(_ICERIK_KAYNAKLARI):
        with cols[idx % 3]:
            if st.button(f"{kaynak['ikon']} {kaynak['label']}", key=f"cf_{kaynak['id']}",
                          use_container_width=True):
                st.session_state["_cf_active"] = kaynak["id"]
                st.rerun()

    active = st.session_state.get("_cf_active")
    if not active:
        st.caption("Bir icerik kaynagi secin.")
        return

    kaynak_info = next((k for k in _ICERIK_KAYNAKLARI if k["id"] == active), None)
    if not kaynak_info:
        return

    st.divider()
    styled_section(f"{kaynak_info['ikon']} {kaynak_info['label']} — Icerik Uretici")

    # ── KAYNAK BAZLI VERİ + İÇERİK ──
    icerik_fikirleri = []

    if active == "etkinlik":
        etkinlikler = _lj(os.path.join(td, "sosyal_etkinlik", "etkinlikler.json"))
        for e in etkinlikler[-10:]:
            baslik = e.get("baslik", "")
            tarih = e.get("tarih_baslangic", "")[:10]
            icerik_fikirleri.append({
                "baslik": f"Etkinlik: {baslik}",
                "oneri": f"Okulumuzdaki '{baslik}' etkinligi basariyla gerceklesti! ({tarih})",
                "hashtag": "#okul #etkinlik #egitim",
                "platform": "instagram",
            })

    elif active == "kayit":
        try:
            from models.kayit_modulu import get_kayit_store
            adaylar = get_kayit_store().load_all()
            kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
            aktif = sum(1 for a in adaylar if a.aktif)
            icerik_fikirleri.append({
                "baslik": "Kontenjan Durumu",
                "oneri": f"Kayitlar devam ediyor! Simdiiye kadar {kesin} ailemize katildi. Sinirli kontenjan — yerinizi ayirtin!",
                "hashtag": "#kayit #kontenjan #ozelokul",
                "platform": "instagram",
            })
            icerik_fikirleri.append({
                "baslik": "FOMO Icerigi",
                "oneri": f"Kontenjanlarimiz hizla doluyor. {aktif} aile su an kayit surecinde. Son {max(0, 200 - kesin)} kontenjan!",
                "hashtag": "#sonkontenjan #kayit2026 #egitim",
                "platform": "facebook",
            })
        except Exception:
            pass

    elif active == "dogum_gunu":
        try:
            students = _lj(os.path.join(td if 'ak_dir' not in dir() else td, "..", "..", "akademik", "students.json"))
            if not students:
                try:
                    from utils.tenant import get_data_path
                    students = _lj(os.path.join(get_data_path("akademik"), "students.json"))
                except Exception:
                    pass
            bugun = date.today()
            for s in students:
                dg = s.get("dogum_tarihi", "")
                if dg and len(dg) >= 10 and dg[5:10] == bugun.isoformat()[5:10]:
                    ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                    icerik_fikirleri.append({
                        "baslik": f"Dogum Gunu: {ad}",
                        "oneri": f"Ogrencimiz {ad}'in dogum gununu kutluyoruz! Mutlu yillar!",
                        "hashtag": "#dogumgunu #ogrencimiz #kutlu",
                        "platform": "instagram",
                    })
        except Exception:
            pass

    elif active == "bayram":
        # Statik ozel gun onerileri
        ay_gun = date.today().strftime("%m-%d")
        ozel_gunler = {
            "01-01": "Yeni Yil", "03-08": "Dunya Kadinlar Gunu", "03-18": "Canakkale Zaferi",
            "04-23": "23 Nisan", "05-01": "1 Mayis", "05-19": "19 Mayis",
            "06-15": "Babalar Gunu", "08-30": "30 Agustos", "10-29": "29 Ekim",
            "11-10": "10 Kasim", "11-24": "Ogretmenler Gunu",
        }
        for gun_key, gun_adi in ozel_gunler.items():
            icerik_fikirleri.append({
                "baslik": gun_adi,
                "oneri": f"{gun_adi} kutlu olsun! Tum ogrencilerimize ve ailelerimize sevgilerimizle.",
                "hashtag": f"#{gun_adi.replace(' ', '').lower()} #kutlama",
                "platform": "instagram",
            })

    elif active == "basari":
        icerik_fikirleri.append({
            "baslik": "Genel Basari Postu",
            "oneri": "Ogrencilerimiz bu donem de buyuk basarilara imza atti! Tebrikler!",
            "hashtag": "#basari #gurur #egitim",
            "platform": "instagram",
        })

    elif active == "swot":
        aksiyonlar = _lj(os.path.join(td, "swot", "aksiyonlar.json"))
        tamamlanan = [a for a in aksiyonlar if a.get("durum") == "Tamamlandi"]
        if tamamlanan:
            for a in tamamlanan[-3:]:
                icerik_fikirleri.append({
                    "baslik": f"Kurumsal Gelisim: {a.get('baslik', '')}",
                    "oneri": f"Surekli gelisim yolculugumuz devam ediyor. '{a.get('baslik', '')}' aksiyonumuzu basariyla tamamladik!",
                    "hashtag": "#kurumsal #gelisim #kalite",
                    "platform": "linkedin",
                })

    # ── İÇERİK FİKİRLERİ KARTLARI ──
    if not icerik_fikirleri:
        styled_info_banner(f"'{kaynak_info['label']}' kaynagindan icerik bulunamadi.", banner_type="warning", icon="📭")
    else:
        st.caption(f"{len(icerik_fikirleri)} icerik onerisi bulundu")
        for i, fikir in enumerate(icerik_fikirleri[:10]):
            p_info = _PLATFORM_INFO.get(fikir.get("platform", "instagram"), {"ikon": "📋", "renk": "#64748b"})

            with st.expander(f"{kaynak_info['ikon']} {fikir['baslik']}", expanded=i == 0):
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {kaynak_info['renk']}30;border-radius:12px;
                            padding:14px 18px;margin-bottom:8px;">
                    <div style="font-size:13px;color:#e2e8f0;line-height:1.6;margin-bottom:8px;">
                        {fikir['oneri']}</div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <span style="background:{p_info['renk']}20;color:{p_info['renk']};padding:2px 8px;
                                    border-radius:6px;font-size:10px;font-weight:700;">
                            {p_info['ikon']} {fikir.get('platform', 'instagram')}</span>
                        <span style="background:#7c3aed20;color:#7c3aed;padding:2px 8px;
                                    border-radius:6px;font-size:10px;">{fikir['hashtag']}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                # AI ile zenginlestirme
                if st.button(f"AI ile 3 Caption Uret", key=f"cf_ai_{active}_{i}", type="primary"):
                    try:
                        from utils.smarti_helper import _get_client
                        client = _get_client()
                        if client:
                            with st.spinner("AI caption uretiyor..."):
                                resp = client.chat.completions.create(
                                    model="gpt-4o-mini",
                                    messages=[
                                        {"role": "system", "content": "Sen bir okul sosyal medya yoneticisisin. Verilen icerik fikrinden 3 farkli caption uret. Her biri farkli tonda: 1) Resmi 2) Samimi 3) Heyecanli. Her caption altina 5 hashtag ekle. Turkce yaz."},
                                        {"role": "user", "content": f"Icerik: {fikir['oneri']}\nPlatform: {fikir.get('platform', 'instagram')}"},
                                    ],
                                    max_tokens=500, temperature=0.8,
                                )
                                ai_captions = resp.choices[0].message.content or ""
                            if ai_captions:
                                st.markdown(f"""
                                <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                            border-radius:12px;padding:14px 18px;">
                                    <div style="font-size:11px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Caption Onerileri</div>
                                    <div style="font-size:12px;color:#e0e7ff;line-height:1.7;">{ai_captions.replace(chr(10), '<br>')}</div>
                                </div>""", unsafe_allow_html=True)
                        else:
                            st.warning("OpenAI API anahtari bulunamadi.")
                    except Exception as e:
                        st.error(f"AI hatasi: {e}")


# ============================================================
# 3. KAMPANYA PERFORMANS & ROI TAKİP
# ============================================================

def _kampanya_roi_path() -> str:
    return os.path.join(_td(), "smm_kampanya_roi.json")


def _load_kampanya_roi() -> list[dict]:
    return _lj(_kampanya_roi_path())


def _save_kampanya_roi(data: list[dict]):
    path = _kampanya_roi_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def render_kampanya_roi():
    """Kampanya bazli performans ve ROI takibi."""
    styled_section("Kampanya ROI Takip", "#f59e0b")
    styled_info_banner(
        "Her sosyal medya kampanyasinin gercek etkisini olcun. "
        "Post performansi + kayit donusum + maliyet/etkislesim orani.",
        banner_type="info", icon="💎")

    td = _td()
    kampanyalar = _load_kampanya_roi()

    # Post verisi
    posts = _lj(os.path.join(td, "smm_posts.json"))
    store = _store()
    if store:
        try:
            posts = store.load_list("posts") or posts
        except Exception:
            pass

    sub = st.tabs(["📊 Dashboard", "➕ Yeni Kampanya", "📋 Kampanya Listesi"])

    # ═══ DASHBOARD ═══
    with sub[0]:
        if not kampanyalar:
            styled_info_banner("Henuz kampanya tanimlanmamis. 'Yeni Kampanya' sekmesinden ekleyin.",
                                banner_type="info", icon="📋")
        else:
            toplam_butce = sum(k.get("butce", 0) for k in kampanyalar)
            toplam_post = sum(k.get("post_sayisi", 0) for k in kampanyalar)

            styled_stat_row([
                ("Toplam Kampanya", str(len(kampanyalar)), "#f59e0b", "📣"),
                ("Toplam Butce", f"{toplam_butce:,.0f} TL", "#ef4444", "💰"),
                ("Toplam Post", str(toplam_post), "#2563eb", "📝"),
            ])

            # Kampanya kartlari
            for k in kampanyalar:
                renk = "#10b981" if k.get("durum") == "aktif" else "#64748b"
                post_count = sum(1 for p in posts if k.get("etiket") and k["etiket"] in (p.get("kampanya", "") or ""))

                # Kayit entegrasyonu
                kayit_aday = 0
                try:
                    from models.kayit_modulu import get_kayit_store
                    adaylar = get_kayit_store().load_all()
                    kayit_aday = sum(1 for a in adaylar if k.get("etiket") and k["etiket"] in (a.utm_campaign or ""))
                except Exception:
                    pass

                butce = k.get("butce", 0)
                cpi = round(butce / max(post_count, 1)) if butce else 0

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}40;border-left:5px solid {renk};
                            border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <div>
                            <div style="font-size:15px;font-weight:800;color:#fff;">{k.get('ad', '')}</div>
                            <div style="font-size:10px;color:#94a3b8;">{k.get('baslangic', '')} — {k.get('bitis', '')} · Etiket: {k.get('etiket', '-')}</div>
                        </div>
                        <span style="background:{renk};color:#fff;padding:3px 12px;border-radius:8px;
                                    font-size:10px;font-weight:700;">{k.get('durum', 'aktif').upper()}</span>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:#2563eb;">{post_count}</div>
                            <div style="font-size:8px;color:#94a3b8;">Post</div></div>
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:#f59e0b;">{butce:,.0f} TL</div>
                            <div style="font-size:8px;color:#94a3b8;">Butce</div></div>
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:#10b981;">{kayit_aday}</div>
                            <div style="font-size:8px;color:#94a3b8;">Kayit Adayi</div></div>
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:#7c3aed;">{cpi:,.0f} TL</div>
                            <div style="font-size:8px;color:#94a3b8;">Maliyet/Post</div></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ═══ YENİ KAMPANYA ═══
    with sub[1]:
        styled_section("Yeni Kampanya Tanimla")
        with st.form("roi_yeni"):
            c1, c2 = st.columns(2)
            with c1:
                ad = st.text_input("Kampanya Adi", placeholder="Erken Kayit 2026")
                baslangic = st.date_input("Baslangic", key="roi_bas")
                hedef_platform = st.multiselect("Hedef Platform",
                    ["instagram", "facebook", "tiktok", "youtube", "linkedin"], key="roi_plat")
            with c2:
                etiket = st.text_input("Kampanya Etiketi", placeholder="erken_kayit_2026")
                bitis = st.date_input("Bitis", key="roi_bit")
                butce = st.number_input("Butce (TL)", min_value=0, value=0, key="roi_butce")

            hedef = st.text_input("Hedef", placeholder="50 kayit adayi, 10.000 erisim")

            if st.form_submit_button("Kampanya Olustur", type="primary"):
                if ad and etiket:
                    yeni = {
                        "id": f"kmp_{uuid.uuid4().hex[:8]}",
                        "ad": ad, "etiket": etiket,
                        "baslangic": baslangic.isoformat(), "bitis": bitis.isoformat(),
                        "platformlar": hedef_platform, "butce": butce, "hedef": hedef,
                        "durum": "aktif", "post_sayisi": 0,
                        "created_at": datetime.now().isoformat(),
                    }
                    kampanyalar.append(yeni)
                    _save_kampanya_roi(kampanyalar)
                    st.success(f"Kampanya olusturuldu: {ad}")
                    st.rerun()

    # ═══ KAMPANYA LİSTESİ ═══
    with sub[2]:
        styled_section("Tum Kampanyalar")
        if not kampanyalar:
            st.info("Henuz kampanya yok.")
        else:
            rows = ""
            for k in sorted(kampanyalar, key=lambda x: x.get("created_at", ""), reverse=True):
                d_renk = "#10b981" if k.get("durum") == "aktif" else "#64748b"
                rows += f"""<tr>
                    <td style="padding:5px 8px;font-size:11px;color:#e2e8f0;font-weight:600;">{k.get('ad', '')}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{k.get('etiket', '')}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{k.get('baslangic', '')[:10]}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{k.get('bitis', '')[:10]}</td>
                    <td style="padding:5px 8px;font-size:11px;color:#f59e0b;">{k.get('butce', 0):,.0f} TL</td>
                    <td style="padding:5px 8px;"><span style="background:{d_renk}20;color:{d_renk};
                        padding:2px 8px;border-radius:6px;font-size:9px;font-weight:700;">{k.get('durum', '')}</span></td>
                </tr>"""
            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:#1e293b;">
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Ad</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Etiket</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Baslangic</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Bitis</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Butce</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Durum</th>
            </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

            # Sil
            sil_sec = st.selectbox("Kampanya Sil", [""] + [k["ad"] for k in kampanyalar], key="roi_sil_sec")
            if sil_sec and st.button("Sil", key="roi_sil_btn"):
                kampanyalar = [k for k in kampanyalar if k["ad"] != sil_sec]
                _save_kampanya_roi(kampanyalar)
                st.success(f"{sil_sec} silindi.")
                st.rerun()
