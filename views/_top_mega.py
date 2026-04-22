"""
Toplanti & Kurullar — MEGA Ozellikleri
========================================
1. Toplanti Komuta Merkezi (Meeting Control Tower)
2. AI Toplanti Hazirlik Asistani (Pre-Meeting Intelligence)
3. Kurul Performans & Uyum Radari
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

_GUN_ADLARI = {0: "Pzt", 1: "Sal", 2: "Car", 3: "Per", 4: "Cum", 5: "Cmt", 6: "Paz"}

# MEB zorunlu kurul sikliklari (yillik minimum)
_MEB_ZORUNLU = {
    "Ogretmenler Kurulu": {"min_yillik": 4, "aciklama": "Yilda en az 4 kez (donem basi/sonu)"},
    "Zumre Toplantisi": {"min_yillik": 8, "aciklama": "Ayda 1 kez zorunlu"},
    "Sinif Ogretmenler Kurulu": {"min_yillik": 4, "aciklama": "Donemde 2 kez"},
    "Okul Gelisim Yonetim Ekibi": {"min_yillik": 4, "aciklama": "Yilda 4 kez zorunlu"},
    "Disiplin Kurulu": {"min_yillik": 0, "aciklama": "Gerektiginde toplanir"},
    "Rehberlik Komisyonu": {"min_yillik": 4, "aciklama": "Donemde 2 kez"},
    "Veli Toplantisi": {"min_yillik": 4, "aciklama": "Donemde 2 kez zorunlu"},
    "Okuloncesi Kurul": {"min_yillik": 4, "aciklama": "Donemde 2 kez"},
}


# ============================================================
# 1. TOPLANTI KOMUTA MERKEZİ
# ============================================================

def render_toplanti_komuta(store):
    """Canli toplanti kontrol paneli."""
    styled_section("Toplanti Komuta Merkezi", "#6366f1")

    bugun = date.today()
    bugun_str = bugun.isoformat()
    simdi = datetime.now()
    saat_str = simdi.strftime("%H:%M")

    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []
    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    kurullar = store.load_list("kurullar") if hasattr(store, "load_list") else []

    # Bugunku toplantılar
    bugun_mtg = [m for m in meetings if m.get("tarih", "")[:10] == bugun_str]
    bu_hafta_bas = bugun - timedelta(days=bugun.weekday())
    bu_hafta_bit = bu_hafta_bas + timedelta(days=6)
    hafta_mtg = [m for m in meetings if bu_hafta_bas.isoformat() <= m.get("tarih", "")[:10] <= bu_hafta_bit.isoformat()]

    # Acik kararlar
    acik_aksiyon = sum(1 for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR"))
    geciken = sum(1 for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")
                   and g.get("hedef_tarih", "") and g["hedef_tarih"] < bugun_str)

    # Devam eden (saat bazli)
    devam_eden = []
    for m in bugun_mtg:
        bas = m.get("saat_baslangic", "")
        bit = m.get("saat_bitis", "")
        if bas and bas <= saat_str and (not bit or bit >= saat_str):
            devam_eden.append(m)

    styled_stat_row([
        ("Bugun Toplanti", str(len(bugun_mtg)), "#6366f1", "📅"),
        ("Bu Hafta", str(len(hafta_mtg)), "#2563eb", "📊"),
        ("Devam Eden", str(len(devam_eden)), "#10b981", "🟢"),
        ("Acik Aksiyon", str(acik_aksiyon), "#f59e0b", "🎯"),
        ("Geciken", str(geciken), "#ef4444", "🚨"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                border:2px solid #6366f1;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(99,102,241,0.25);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-size:10px;color:#a5b4fc;letter-spacing:3px;text-transform:uppercase;">Toplanti Komuta</div>
                <div style="font-size:26px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                    {bugun.strftime('%d.%m.%Y')} · {_GUN_ADLARI.get(bugun.weekday(), '')}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:28px;font-weight:900;color:#a5b4fc;font-family:monospace;">{saat_str}</div>
                <div style="font-size:10px;color:#818cf8;">
                    {'🟢 Toplanti devam ediyor' if devam_eden else '⚪ Aktif toplanti yok'}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── BUGÜNÜN TİMELINE ──
    styled_section("Bugunun Toplantilari")
    if not bugun_mtg:
        st.info("Bugun planli toplanti yok.")
    else:
        for m in sorted(bugun_mtg, key=lambda x: x.get("saat_baslangic", "")):
            bas = m.get("saat_baslangic", "--:--")
            bit = m.get("saat_bitis", "--:--")
            is_devam = m in devam_eden
            durum = m.get("durum", "TASLAK")
            d_renk = "#10b981" if is_devam else {"YAPILDI": "#10b981", "TUTANAK_TAMAM": "#10b981", "TASLAK": "#3b82f6"}.get(durum, "#64748b")
            border = "2px solid #10b981" if is_devam else f"1px solid {d_renk}30"

            # Countdown
            countdown = ""
            if not is_devam and bas > saat_str:
                try:
                    plan_dt = datetime.strptime(f"{bugun_str} {bas}", "%Y-%m-%d %H:%M")
                    kalan = plan_dt - simdi
                    if kalan.total_seconds() > 0:
                        countdown = f"{int(kalan.total_seconds() // 3600)}s {int((kalan.total_seconds() % 3600) // 60)}dk"
                except Exception:
                    pass

            m_karar = sum(1 for d in decisions if d.get("meeting_id") == m.get("id"))

            st.markdown(f"""
            <div style="background:#0f172a;border:{border};border-left:5px solid {d_renk};
                        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:800;color:#e2e8f0;font-size:14px;">
                            {'🟢 ' if is_devam else ''}{m.get('baslik', '?')}</span>
                        <div style="font-size:10px;color:#94a3b8;margin-top:2px;">
                            {bas}-{bit} · {m.get('lokasyon', '-')} · {m.get('organizator', '-')}</div>
                    </div>
                    <div style="display:flex;gap:6px;align-items:center;">
                        {f'<span style="background:#10b98120;color:#10b981;padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">DEVAM EDIYOR</span>' if is_devam else ''}
                        {f'<span style="background:#3b82f620;color:#3b82f6;padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">{countdown}</span>' if countdown else ''}
                        <span style="font-size:10px;color:#2563eb;">{m_karar} karar</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── KURUL SON TOPLANMA ──
    styled_section("Kurul Son Toplanma Durumu")
    for k in kurullar[:10]:
        k_ad = k.get("ad", k.get("baslik", "?"))
        # Son toplanti
        k_mtg = [m for m in meetings if k_ad.lower() in (m.get("baslik", "") or "").lower()
                  and m.get("durum") in ("YAPILDI", "TUTANAK_TAMAM", "ONAYLANDI")]
        if k_mtg:
            son = max(k_mtg, key=lambda x: x.get("tarih", ""))
            son_tarih = son.get("tarih", "")[:10]
            try:
                gun_gecti = (bugun - date.fromisoformat(son_tarih)).days
            except Exception:
                gun_gecti = 999
        else:
            son_tarih = "Hic toplanmadi"
            gun_gecti = 999

        renk = "#ef4444" if gun_gecti > 60 else "#f59e0b" if gun_gecti > 30 else "#10b981"
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
            <span style="flex:1;font-size:12px;color:#e2e8f0;font-weight:600;">{k_ad}</span>
            <span style="font-size:10px;color:#94a3b8;">{son_tarih}</span>
            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                        font-size:10px;font-weight:700;">{gun_gecti}g once</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. AI HAZIRLIK ASİSTANI
# ============================================================

def render_ai_hazirlik(store):
    """Toplantiya girmeden AI brifing dosyasi."""
    styled_section("AI Toplanti Hazirlik Asistani", "#059669")
    styled_info_banner(
        "Toplanti secin — AI otomatik brifing hazilar: "
        "tamamlanmamis aksiyonlar, gundem onerisi, katilim gecmisi, ilgili veriler.",
        banner_type="info", icon="📋")

    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []
    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    participants = store.load_list("participants") if hasattr(store, "load_list") else []
    agenda = store.load_list("agenda_items") if hasattr(store, "load_list") else []

    bugun = date.today().isoformat()
    gelecek = [m for m in meetings if m.get("tarih", "") >= bugun and m.get("durum") not in ("IPTAL", "YAPILDI", "TUTANAK_TAMAM", "ONAYLANDI")]

    if not gelecek and not meetings:
        styled_info_banner("Toplanti kaydi bulunamadi.", banner_type="warning", icon="📅")
        return

    # Secim (gelecek + son yapilanlar)
    secenekler = gelecek + sorted([m for m in meetings if m.get("durum") in ("YAPILDI", "TUTANAK_TAMAM")],
                                     key=lambda x: x.get("tarih", ""), reverse=True)[:5]
    mtg_labels = [f"{m.get('baslik', '?')} ({m.get('tarih', '')[:10]})" for m in secenekler]
    secili = st.selectbox("Toplanti Secin", [""] + mtg_labels, key="aih_sec")

    if not secili:
        return

    mtg = secenekler[mtg_labels.index(secili)]
    mid = mtg.get("id", "")

    # Veri topla
    mtg_gorevler = [g for g in gorevler if g.get("meeting_id") == mid]
    mtg_kararlar = [d for d in decisions if d.get("meeting_id") == mid]
    mtg_katilimci = [p for p in participants if p.get("meeting_id") == mid]
    mtg_gundem = [a for a in agenda if a.get("meeting_id") == mid]
    acik_aksiyon = [g for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")]

    # ── BRİFİNG KARTI ──
    st.markdown(f"""
    <div style="background:#0f172a;border:2px solid #059669;border-radius:16px;padding:18px 22px;margin:12px 0;">
        <div style="font-size:16px;font-weight:900;color:#6ee7b7;margin-bottom:8px;">
            Hazirlik Brifing — {mtg.get('baslik', '')}</div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:11px;color:#94a3b8;">
            <div>Tarih: <b style="color:#e2e8f0;">{mtg.get('tarih', '')[:10]}</b></div>
            <div>Saat: <b style="color:#e2e8f0;">{mtg.get('saat_baslangic', '')} - {mtg.get('saat_bitis', '')}</b></div>
            <div>Lokasyon: <b style="color:#e2e8f0;">{mtg.get('lokasyon', '-')}</b></div>
            <div>Organizator: <b style="color:#e2e8f0;">{mtg.get('organizator', '-')}</b></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Tamamlanmamis aksiyonlar
    if acik_aksiyon:
        styled_section(f"Tamamlanmamis Aksiyonlar ({len(acik_aksiyon)})", "#ef4444")
        for g in acik_aksiyon[:10]:
            gecikme = ""
            if g.get("hedef_tarih", "") and g["hedef_tarih"] < bugun:
                gecikme = " GECIKTI"
            st.markdown(f"- **{g.get('gorev_tanimi', g.get('baslik', '?'))[:60]}** → {g.get('sorumlu', '-')}{gecikme}")

    # Gundem maddeleri
    if mtg_gundem:
        styled_section(f"Gundem Maddeleri ({len(mtg_gundem)})")
        for a in sorted(mtg_gundem, key=lambda x: x.get("sira", 0)):
            st.markdown(f"- {a.get('baslik', '?')} ({a.get('tip', '-')})")

    # Katilimci listesi
    if mtg_katilimci:
        styled_section(f"Katilimcilar ({len(mtg_katilimci)})")
        for p in mtg_katilimci:
            durum = p.get("katilim_durumu", "DAVETLI")
            d_ikon = {"KATILDI": "✅", "KATILMADI": "❌", "MAZERET": "🟡"}.get(durum, "⬜")
            st.markdown(f"- {d_ikon} {p.get('ad_soyad', p.get('name', '?'))} ({p.get('gorev', '-')})")

    # AI brifing
    st.divider()
    if st.button("AI Brifing Olustur", key="aih_ai_btn", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                aksiyon_ozet = "\n".join(f"- {g.get('gorev_tanimi', '')[:60]} → {g.get('sorumlu', '')} [{g.get('durum', '')}]" for g in acik_aksiyon[:10])
                gundem_ozet = "\n".join(f"- {a.get('baslik', '')}" for a in mtg_gundem[:10])
                veri = (f"Toplanti: {mtg.get('baslik', '')}\nTarih: {mtg.get('tarih', '')}\n"
                        f"Gundem:\n{gundem_ozet or 'Gundem girilmemis'}\n"
                        f"Acik Aksiyonlar:\n{aksiyon_ozet or 'Acik aksiyon yok'}\n"
                        f"Katilimci: {len(mtg_katilimci)}")
                with st.spinner("AI brifing hazirlıyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul toplanti danismanisin. Verilen toplanti verileriyle kisa brifing hazirla: 1) Toplanti ozeti 2) Dikkat edilecekler 3) Gundem onerisi 4) Tahmini sure. Turkce."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #059669;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#6ee7b7;font-weight:700;margin-bottom:6px;">AI Toplanti Brifing</div>
                        <div style="font-size:12px;color:#d1fae5;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 3. KURUL PERFORMANS & UYUM RADARI
# ============================================================

def render_kurul_uyum(store):
    """MEB zorunlu kurul takibi + performans scorecard."""
    styled_section("Kurul Uyum Radari", "#dc2626")
    styled_info_banner(
        "MEB'in zorunlu kurul toplanti sikliklarini otomatik kontrol edin. "
        "Eksik toplantilari tespit edin, yasal uyumu saglayin.",
        banner_type="warning", icon="🛡️")

    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []
    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    kurullar = store.load_list("kurullar") if hasattr(store, "load_list") else []
    participants = store.load_list("participants") if hasattr(store, "load_list") else []

    yapilan = [m for m in meetings if m.get("durum") in ("YAPILDI", "TUTANAK_TAMAM", "ONAYLANDI")]

    # Bu egitim yili (Eylul-Agustos)
    bugun = date.today()
    if bugun.month >= 9:
        yil_bas = date(bugun.year, 9, 1)
    else:
        yil_bas = date(bugun.year - 1, 9, 1)
    yil_bas_str = yil_bas.isoformat()

    # Kurul bazli uyum kontrolu
    uyum_sonuclari = []
    for kurul_adi, kural in _MEB_ZORUNLU.items():
        min_yillik = kural["min_yillik"]
        # Bu yil yapilan
        yapilan_sayi = sum(1 for m in yapilan
                            if kurul_adi.lower() in (m.get("baslik", "") or "").lower()
                            and m.get("tarih", "") >= yil_bas_str)

        eksik = max(0, min_yillik - yapilan_sayi)
        uyumlu = yapilan_sayi >= min_yillik if min_yillik > 0 else True

        # Son toplanti
        kurul_mtg = [m for m in yapilan if kurul_adi.lower() in (m.get("baslik", "") or "").lower()]
        son_tarih = max((m.get("tarih", "")[:10] for m in kurul_mtg), default="Hic") if kurul_mtg else "Hic"

        uyum_sonuclari.append({
            "kurul": kurul_adi, "min": min_yillik, "yapilan": yapilan_sayi,
            "eksik": eksik, "uyumlu": uyumlu, "son_tarih": son_tarih,
            "aciklama": kural["aciklama"],
        })

    # Ozet
    uyumlu_sayi = sum(1 for u in uyum_sonuclari if u["uyumlu"])
    uyumsuz_sayi = sum(1 for u in uyum_sonuclari if not u["uyumlu"] and u["min"] > 0)
    genel_uyum = round(uyumlu_sayi / max(len(uyum_sonuclari), 1) * 100)
    u_renk = "#10b981" if genel_uyum >= 80 else "#f59e0b" if genel_uyum >= 50 else "#ef4444"

    styled_stat_row([
        ("Izlenen Kurul", str(len(uyum_sonuclari)), "#dc2626", "🛡️"),
        ("Uyumlu", str(uyumlu_sayi), "#10b981", "✅"),
        ("Uyumsuz", str(uyumsuz_sayi), "#ef4444", "🚨"),
        ("Genel Uyum", f"%{genel_uyum}", u_renk, "📊"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#450a0a 0%,#7f1d1d 100%);
                border:2px solid {u_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {u_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fca5a5;letter-spacing:3px;text-transform:uppercase;">MEB Kurul Uyum Orani</div>
        <div style="font-size:56px;font-weight:900;color:{u_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">%{genel_uyum}</div>
        <div style="font-size:12px;color:#fca5a5;">{uyumlu_sayi}/{len(uyum_sonuclari)} kurul uyumlu · {yil_bas.year}-{yil_bas.year + 1} Egitim Yili</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Uyum Tablosu", "🏆 Kurul Scorecard"])

    # ═══ UYUM TABLOSU ═══
    with sub[0]:
        styled_section("Kurul Bazli Uyum Durumu")
        for u in uyum_sonuclari:
            if u["min"] == 0:
                continue  # Zorunlu degil
            renk = "#10b981" if u["uyumlu"] else "#ef4444"
            durum_txt = "UYUMLU" if u["uyumlu"] else f"EKSIK ({u['eksik']} toplanti)"
            bar_w = min(100, round(u["yapilan"] / max(u["min"], 1) * 100))

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                        border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <div>
                        <span style="font-weight:800;color:#e2e8f0;font-size:14px;">{u['kurul']}</span>
                        <div style="font-size:10px;color:#94a3b8;margin-top:2px;">{u['aciklama']}</div>
                    </div>
                    <span style="background:{renk}20;color:{renk};padding:4px 14px;border-radius:8px;
                                font-size:11px;font-weight:800;">{durum_txt}</span>
                </div>
                <div style="display:flex;gap:16px;font-size:11px;color:#94a3b8;margin-bottom:6px;">
                    <span>Zorunlu: <b style="color:#e2e8f0;">{u['min']}/yil</b></span>
                    <span>Yapilan: <b style="color:{renk};">{u['yapilan']}</b></span>
                    <span>Son: <b style="color:#e2e8f0;">{u['son_tarih']}</b></span>
                </div>
                <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ KURUL SCORECARD ═══
    with sub[1]:
        styled_section("Kurul Performans Scorecard")
        for k in kurullar[:15]:
            k_ad = k.get("ad", k.get("baslik", "?"))
            k_mtg = [m for m in yapilan if k_ad.lower() in (m.get("baslik", "") or "").lower()]
            k_karar = sum(1 for d in decisions if d.get("meeting_id") in [m.get("id") for m in k_mtg])
            k_aksiyon = sum(1 for g in gorevler if g.get("meeting_id") in [m.get("id") for m in k_mtg])
            k_tamam = sum(1 for g in gorevler if g.get("meeting_id") in [m.get("id") for m in k_mtg]
                           and g.get("durum") == "TAMAMLANDI")
            tamam_oran = round(k_tamam / max(k_aksiyon, 1) * 100)

            # Katilim
            k_kat = [p for p in participants if p.get("meeting_id") in [m.get("id") for m in k_mtg]]
            katilan = sum(1 for p in k_kat if p.get("katilim_durumu") == "KATILDI")
            kat_oran = round(katilan / max(len(k_kat), 1) * 100) if k_kat else 0

            skor = round((tamam_oran * 0.4 + kat_oran * 0.3 + min(len(k_mtg) * 10, 30)) * 1)
            skor = min(skor, 100)
            s_renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 45 else "#ef4444"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {s_renk}30;border-radius:12px;
                        padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{k_ad}</span>
                    <span style="font-size:20px;font-weight:900;color:{s_renk};">{skor}</span>
                </div>
                <div style="display:flex;gap:12px;font-size:10px;color:#94a3b8;">
                    <span>Toplanti: {len(k_mtg)}</span>
                    <span>Karar: {k_karar}</span>
                    <span>Aksiyon: {k_aksiyon} ({k_tamam} tamam)</span>
                    <span>Katilim: %{kat_oran}</span>
                </div>
            </div>""", unsafe_allow_html=True)
