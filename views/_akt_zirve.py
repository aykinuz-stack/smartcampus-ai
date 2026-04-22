"""
Akademik Takvim — Zirve Ozellikleri
======================================
1. Birlesik Super Takvim (Unified Calendar Hub)
2. Akilli Takvim Planlama Asistani
3. Takvim Komuta Merkezi + Geri Sayim Paneli
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

_GUN_ADLARI = {0: "Pzt", 1: "Sal", 2: "Car", 3: "Per", 4: "Cum", 5: "Cmt", 6: "Paz"}
_AY_ADLARI = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
               7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}

_RESMI_TATILLER = {
    "01-01": "Yilbasi", "04-23": "23 Nisan", "05-01": "1 Mayis",
    "05-19": "19 Mayis", "07-15": "15 Temmuz", "08-30": "30 Agustos",
    "10-29": "29 Ekim", "11-10": "10 Kasim",
}

_KATMAN_RENK = {
    "akademik": {"renk": "#2563eb", "ikon": "📚", "label": "Akademik"},
    "sinav": {"renk": "#8b5cf6", "ikon": "📝", "label": "Sinav"},
    "toplanti": {"renk": "#059669", "ikon": "🤝", "label": "Toplanti"},
    "etkinlik": {"renk": "#ea580c", "ikon": "🎭", "label": "Etkinlik"},
    "randevu": {"renk": "#10b981", "ikon": "📅", "label": "Randevu"},
    "tatil": {"renk": "#f59e0b", "ikon": "🏖️", "label": "Tatil"},
    "izin": {"renk": "#94a3b8", "ikon": "👤", "label": "Izin"},
    "resmi": {"renk": "#dc2626", "ikon": "🇹🇷", "label": "Resmi Tatil"},
}


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


def _tum_modül_etkinlikleri(yil: int, ay: int) -> list[dict]:
    """Tum modullerden ay bazli etkinlikleri topla."""
    td = _td()
    etkinlikler = []
    ay_bas = f"{yil}-{ay:02d}-01"
    ay_bit = f"{yil}-{ay:02d}-31"

    # 1. Toplanti
    try:
        from models.toplanti_kurullar import ToplantiDataStore
        top = ToplantiDataStore(os.path.join(td, "toplanti"))
        for m in top.load_list("meetings") if hasattr(top, "load_list") else []:
            t = m.get("tarih", "")[:10]
            if ay_bas <= t <= ay_bit:
                etkinlikler.append({"tarih": t, "baslik": m.get("baslik", "Toplanti"),
                                     "katman": "toplanti", "saat": m.get("saat_baslangic", "")})
    except Exception:
        pass

    # 2. Sinav (Olcme)
    try:
        sinav_path = os.path.join("data", "olcme", "exams.json")
        for e in _lj(sinav_path):
            t = (e.get("start_date", "") or "")[:10]
            if ay_bas <= t <= ay_bit:
                etkinlikler.append({"tarih": t, "baslik": e.get("name", "Sinav"),
                                     "katman": "sinav", "saat": ""})
    except Exception:
        pass

    # 3. Sosyal Etkinlik
    try:
        from models.sosyal_etkinlik import SosyalEtkinlikDataStore
        se = SosyalEtkinlikDataStore(os.path.join(td, "sosyal_etkinlik"))
        for e in se.load_list("etkinlikler") if hasattr(se, "load_list") else []:
            t = (e.get("tarih_baslangic", "") or "")[:10]
            if ay_bas <= t <= ay_bit:
                etkinlikler.append({"tarih": t, "baslik": e.get("baslik", "Etkinlik"),
                                     "katman": "etkinlik", "saat": e.get("saat_baslangic", "")})
    except Exception:
        pass

    # 4. Randevu
    try:
        from models.randevu_ziyaretci import RZYDataStore
        rzy = RZYDataStore(os.path.join(td, "randevu"))
        for r in rzy.load_list("randevular") if hasattr(rzy, "load_list") else []:
            t = r.get("tarih", "")[:10]
            if ay_bas <= t <= ay_bit and r.get("durum") not in ("Iptal",):
                etkinlikler.append({"tarih": t, "baslik": f"Randevu: {r.get('ziyaretci_adi', '')}",
                                     "katman": "randevu", "saat": r.get("saat_baslangic", "")})
    except Exception:
        pass

    # 5. Personel izin
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        for iz in ik.load_list("izinler") if hasattr(ik, "load_list") else []:
            bas = iz.get("baslangic_tarihi", "")
            if bas and ay_bas <= bas[:10] <= ay_bit:
                etkinlikler.append({"tarih": bas[:10], "baslik": f"Izin: {iz.get('personel_adi', '')}",
                                     "katman": "izin", "saat": ""})
    except Exception:
        pass

    # 6. Resmi tatiller
    for mmdd, ad in _RESMI_TATILLER.items():
        t = f"{yil}-{mmdd}"
        if ay_bas <= t <= ay_bit:
            etkinlikler.append({"tarih": t, "baslik": ad, "katman": "resmi", "saat": ""})

    return sorted(etkinlikler, key=lambda x: x["tarih"])


# ============================================================
# 1. BİRLEŞİK SÜPER TAKVİM
# ============================================================

def render_super_takvim(events: list, yil: int, ay: int):
    """Tum modullerden birlestirilen super takvim."""
    styled_section("Birlesik Super Takvim", "#2563eb")
    styled_info_banner(
        "Akademik takvim + toplanti + sinav + etkinlik + randevu + izin + resmi tatil "
        "— hepsi tek takvimde, renk kodlu katmanlar.",
        banner_type="info", icon="🌐")

    # Katman filtreleri
    st.markdown("**Katman Filtreleri:**")
    aktif_katmanlar = []
    filter_cols = st.columns(4)
    for idx, (key, info) in enumerate(_KATMAN_RENK.items()):
        with filter_cols[idx % 4]:
            if st.checkbox(f"{info['ikon']} {info['label']}", value=True, key=f"stk_{key}"):
                aktif_katmanlar.append(key)

    # Akademik takvim etkinliklerini katmana donustur
    for e in events:
        tur = e.get("type", "").lower()
        if "sinav" in tur or "yazili" in tur:
            e["_katman"] = "sinav"
        elif "tatil" in tur:
            e["_katman"] = "tatil"
        else:
            e["_katman"] = "akademik"

    # Tum modüllerdne etkinlikleri topla
    modul_etkinlikler = _tum_modül_etkinlikleri(yil, ay)

    # Akademik takvim etkinliklerini ekle
    for e in events:
        t = e.get("date", e.get("tarih", ""))[:10]
        if t and f"{yil}-{ay:02d}" in t:
            modul_etkinlikler.append({
                "tarih": t, "baslik": e.get("title", e.get("baslik", "")),
                "katman": e.get("_katman", "akademik"), "saat": "",
            })

    # Filtrele
    filtered = [e for e in modul_etkinlikler if e.get("katman") in aktif_katmanlar]

    # Ozet
    katman_sayac = Counter(e["katman"] for e in filtered)
    stats = [(f"{_KATMAN_RENK[k]['ikon']} {_KATMAN_RENK[k]['label']}", str(s), _KATMAN_RENK[k]["renk"], _KATMAN_RENK[k]["ikon"])
              for k, s in katman_sayac.most_common()]
    if stats:
        styled_stat_row(stats[:6])

    # ── GÜNLÜK LİSTE ──
    styled_section(f"{_AY_ADLARI.get(ay, '')} {yil} — {len(filtered)} etkinlik")

    # Gune gore grupla
    gun_grp = {}
    for e in filtered:
        gun_grp.setdefault(e["tarih"], []).append(e)

    for gun_str in sorted(gun_grp.keys()):
        gun_etkinlikler = gun_grp[gun_str]
        try:
            dt = date.fromisoformat(gun_str)
            gun_adi = _GUN_ADLARI.get(dt.weekday(), "")
            is_bugun = dt == date.today()
        except Exception:
            gun_adi = ""
            is_bugun = False

        border = "2px solid #c9a84c" if is_bugun else "1px solid #1e293b"
        bg = "#1a1a2e" if is_bugun else "#0f172a"

        kartlar_html = ""
        for e in gun_etkinlikler:
            k_info = _KATMAN_RENK.get(e["katman"], {"renk": "#64748b", "ikon": "📋"})
            saat = e.get("saat", "")[:5] if e.get("saat") else ""
            kartlar_html += (
                f'<div style="display:flex;gap:6px;align-items:center;padding:2px 0;">'
                f'<span style="width:8px;height:8px;border-radius:50%;background:{k_info["renk"]};flex-shrink:0;"></span>'
                f'<span style="font-size:10px;color:{k_info["renk"]};font-weight:700;">{saat}</span>'
                f'<span style="font-size:10px;color:#e2e8f0;">{e["baslik"][:40]}</span></div>')

        st.markdown(f"""
        <div style="background:{bg};border:{border};border-radius:10px;
                    padding:10px 14px;margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-weight:700;color:{'#c9a84c' if is_bugun else '#e2e8f0'};font-size:13px;">
                    {'BUGUN ' if is_bugun else ''}{gun_str[8:10]}.{gun_str[5:7]} {gun_adi}</span>
                <span style="font-size:10px;color:#94a3b8;">{len(gun_etkinlikler)} etkinlik</span>
            </div>
            {kartlar_html}
        </div>""", unsafe_allow_html=True)

    if not filtered:
        styled_info_banner("Bu ayda secili katmanlarda etkinlik yok.", banner_type="info", icon="📅")

    # Renk aciklama
    legend_html = ""
    for key, info in _KATMAN_RENK.items():
        if key in aktif_katmanlar:
            legend_html += f'<span style="display:inline-flex;align-items:center;gap:4px;margin:2px 8px;font-size:9px;color:{info["renk"]};">{info["ikon"]} {info["label"]}</span>'
    st.markdown(f'<div style="margin-top:8px;">{legend_html}</div>', unsafe_allow_html=True)


# ============================================================
# 2. AI PLANLAMA ASİSTANI
# ============================================================

def render_ai_planlama(events: list):
    """Cakisma kontrolu + yogunluk dengesi + AI oneri."""
    styled_section("AI Takvim Planlama Asistani", "#7c3aed")
    styled_info_banner(
        "Sinav/etkinlik cakismalarini tespit edin. "
        "Yogunluk dengesini kontrol edin. AI ile optimal planlama.",
        banner_type="info", icon="🧠")

    if not events:
        styled_info_banner("Takvim verisi yok.", banner_type="warning", icon="📅")
        return

    # Cakisma kontrolu
    styled_section("Cakisma Kontrolu")
    gun_etkinlik = {}
    for e in events:
        t = e.get("date", e.get("tarih", ""))[:10]
        if t:
            gun_etkinlik.setdefault(t, []).append(e)

    cakismalar = []
    for gun, etks in gun_etkinlik.items():
        if len(etks) >= 3:
            tipler = [e.get("type", e.get("tur", "?")) for e in etks]
            cakismalar.append({"gun": gun, "sayi": len(etks), "tipler": tipler})

    if cakismalar:
        for c in sorted(cakismalar, key=lambda x: -x["sayi"]):
            st.markdown(f"""
            <div style="background:#431407;border:1px solid #f97316;border-radius:10px;
                        padding:10px 14px;margin-bottom:6px;">
                <span style="font-weight:700;color:#fdba74;">⚠️ {c['gun']} — {c['sayi']} etkinlik cakisiyor!</span>
                <div style="font-size:10px;color:#94a3b8;margin-top:2px;">{', '.join(c['tipler'][:5])}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("Cakisma yok — takvim dengeli!")

    # Aylik yogunluk analizi
    styled_section("Aylik Yogunluk Dagilimi")
    ay_sayac = Counter()
    for e in events:
        t = e.get("date", e.get("tarih", ""))
        if t and len(t) >= 7:
            ay_sayac[t[:7]] += 1

    if ay_sayac:
        en_yogun = max(ay_sayac.values())
        for ay_str, sayi in sorted(ay_sayac.items()):
            ay_no = int(ay_str[5:7]) if len(ay_str) >= 7 else 0
            ay_adi = _AY_ADLARI.get(ay_no, ay_str)
            renk = "#ef4444" if sayi > en_yogun * 0.8 else "#f59e0b" if sayi > en_yogun * 0.5 else "#10b981"
            bar_w = round(sayi / max(en_yogun, 1) * 100)

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="min-width:60px;font-size:11px;color:#e2e8f0;font-weight:600;">{ay_adi}</span>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
            </div>""", unsafe_allow_html=True)

    # AI planlama
    st.divider()
    if st.button("AI Planlama Onerisi", key="akt_ai_plan", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                yogunluk = ", ".join(f"{_AY_ADLARI.get(int(k[5:7]), k)}: {v}" for k, v in sorted(ay_sayac.items()))
                cak_ozet = f"{len(cakismalar)} gun cakisma" if cakismalar else "Cakisma yok"
                with st.spinner("AI takvim analiz ediyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul akademik takvim planlama uzmanisin. Yogunluk ve cakisma verilerine dayanarak oneriler sun: 1) Dengeli dagilim 2) Sinav zamanlama 3) Tatil planlamasi 4) Onerilen degisiklikler. Turkce."},
                            {"role": "user", "content": f"Toplam etkinlik: {len(events)}\nAylik dagılim: {yogunluk}\n{cak_ozet}"},
                        ],
                        max_tokens=400, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Planlama Onerisi</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 3. TAKVİM KOMUTA MERKEZİ + GERİ SAYIM
# ============================================================

_ONEMLI_TARIHLER = [
    {"ad": "LGS Sinavi", "tarih": "2026-06-14", "ikon": "📝"},
    {"ad": "Donem Sonu", "tarih": "2026-06-20", "ikon": "🏫"},
    {"ad": "Yariyil Tatili Bas", "tarih": "2026-01-23", "ikon": "🏖️"},
    {"ad": "Yariyil Tatili Bit", "tarih": "2026-02-03", "ikon": "📚"},
    {"ad": "23 Nisan", "tarih": "2026-04-23", "ikon": "🇹🇷"},
    {"ad": "19 Mayis", "tarih": "2026-05-19", "ikon": "🇹🇷"},
]


def render_takvim_komuta(events: list):
    """Yaklasan etkinlikler + geri sayim + haftalik ozet."""
    styled_section("Takvim Komuta Merkezi", "#f59e0b")
    styled_info_banner(
        "Yaklasan tum etkinlikler, geri sayim kartlari, "
        "bu hafta/bu ay ozeti — tek bakista.",
        banner_type="info", icon="🎛️")

    bugun = date.today()
    bugun_str = bugun.isoformat()

    # ── GERİ SAYIM KARTLARI ──
    styled_section("Onemli Tarihlere Geri Sayim")
    geri_cols = st.columns(3)
    for idx, ot in enumerate(_ONEMLI_TARIHLER):
        try:
            hedef = date.fromisoformat(ot["tarih"])
            kalan = (hedef - bugun).days
            if kalan < 0:
                continue
        except Exception:
            continue

        renk = "#ef4444" if kalan <= 7 else "#f59e0b" if kalan <= 30 else "#10b981"
        with geri_cols[idx % 3]:
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {renk};border-radius:14px;
                        padding:14px;text-align:center;margin-bottom:8px;">
                <div style="font-size:20px;">{ot['ikon']}</div>
                <div style="font-size:10px;color:#94a3b8;margin:3px 0;">{ot['ad']}</div>
                <div style="font-size:28px;font-weight:900;color:{renk};font-family:monospace;">{kalan}</div>
                <div style="font-size:9px;color:#64748b;">gun kaldi</div>
            </div>""", unsafe_allow_html=True)

    # ── BUGÜN + BU HAFTA ──
    styled_section("Bugun ve Bu Hafta")

    # Bugunun etkinlikleri
    bugun_etk = [e for e in events if (e.get("date", e.get("tarih", "")) or "")[:10] == bugun_str]

    # Bu haftanin etkinlikleri
    hafta_bas = bugun - timedelta(days=bugun.weekday())
    hafta_bit = hafta_bas + timedelta(days=6)
    hafta_etk = [e for e in events if hafta_bas.isoformat() <= (e.get("date", e.get("tarih", "")) or "")[:10] <= hafta_bit.isoformat()]

    # Bu ayin etkinlikleri
    ay_etk = [e for e in events if (e.get("date", e.get("tarih", "")) or "")[:7] == bugun_str[:7]]

    styled_stat_row([
        ("Bugun", str(len(bugun_etk)), "#2563eb", "📅"),
        ("Bu Hafta", str(len(hafta_etk)), "#7c3aed", "📊"),
        ("Bu Ay", str(len(ay_etk)), "#059669", "📆"),
        ("Toplam", str(len(events)), "#f59e0b", "📋"),
    ])

    # Bugunun etkinlikleri
    if bugun_etk:
        st.markdown("**Bugunun Etkinlikleri:**")
        for e in bugun_etk:
            baslik = e.get("title", e.get("baslik", "?"))
            tur = e.get("type", e.get("tur", ""))
            st.markdown(f"- 📌 **{baslik}** ({tur})")
    else:
        st.info("Bugun planli etkinlik yok.")

    # ── YAKLASAN 7 GÜN ──
    styled_section("Yaklasan 7 Gun")
    for i in range(7):
        gun = bugun + timedelta(days=i)
        gun_str = gun.isoformat()
        gun_adi = _GUN_ADLARI.get(gun.weekday(), "")
        gun_etk = [e for e in events if (e.get("date", e.get("tarih", "")) or "")[:10] == gun_str]
        is_bugun = i == 0

        if gun_etk:
            basliklar = ", ".join(e.get("title", e.get("baslik", "?"))[:30] for e in gun_etk[:3])
            renk = "#c9a84c" if is_bugun else "#3b82f6"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:4px 0;
                        {'border-left:3px solid #c9a84c;padding-left:10px;' if is_bugun else ''}">
                <span style="min-width:70px;font-size:11px;color:{renk};font-weight:{'800' if is_bugun else '600'};">
                    {'BUGUN' if is_bugun else f'{gun.day:02d}.{gun.month:02d} {gun_adi}'}</span>
                <span style="font-size:11px;color:#e2e8f0;">{basliklar}</span>
                <span style="font-size:9px;color:#94a3b8;margin-left:auto;">{len(gun_etk)}</span>
            </div>""", unsafe_allow_html=True)

    # ── BOŞ GÜN ANALİZİ ──
    styled_section("Bos Gun Analizi (Bu Ay)")
    import calendar
    ay_gun_sayisi = calendar.monthrange(bugun.year, bugun.month)[1]
    dolu_gunler = set((e.get("date", e.get("tarih", "")) or "")[:10] for e in ay_etk)
    bos_gunler = []
    for g in range(1, ay_gun_sayisi + 1):
        gun_t = f"{bugun.year}-{bugun.month:02d}-{g:02d}"
        try:
            dt = date.fromisoformat(gun_t)
            if dt.weekday() < 5 and gun_t not in dolu_gunler and dt >= bugun:
                bos_gunler.append(gun_t)
        except Exception:
            pass

    if bos_gunler:
        st.markdown(f"**{len(bos_gunler)} bos is gunu** (haftaici, etkinliksiz):")
        for bg in bos_gunler[:5]:
            try:
                dt = date.fromisoformat(bg)
                st.markdown(f"- {bg[8:]}.{bg[5:7]} {_GUN_ADLARI.get(dt.weekday(), '')}")
            except Exception:
                pass
        if len(bos_gunler) > 5:
            st.caption(f"... ve {len(bos_gunler) - 5} gun daha")
    else:
        st.success("Bu ayda bos gun yok — takvim dolu!")
