"""
Kayit Modulu — ULTRA MEGA Final Ozellikleri
=============================================
1. Kayit Savas Odasi (War Room Dashboard)
2. Aday Yolculuk Haritasi + Tikanma Dedektoru
3. AI Tahmin Motoru + Gelir Projeksiyon Paneli
"""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from models.kayit_modulu import (
    KayitAday, KayitDataStore,
    PIPELINE_ASAMALARI, PIPELINE_INFO, KADEME_SECENEKLERI,
)
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _son_temas_gun(a: KayitAday) -> int:
    tarihler = []
    for ar in a.aramalar:
        t = ar.get("tarih", "")
        if t:
            tarihler.append(t[:10])
    for gr in a.gorusmeler:
        t = gr.get("tarih", "")
        if t:
            tarihler.append(t[:10])
    if a.son_islem_tarihi:
        tarihler.append(a.son_islem_tarihi[:10])
    if not tarihler:
        return 999
    try:
        return (date.today() - date.fromisoformat(max(tarihler))).days
    except Exception:
        return 999


def _asama_suresi(a: KayitAday, asama: str) -> int | None:
    """Adayin belirli asamada kac gun kaldigi."""
    tarihler = []
    if asama in ("aday", "arandi"):
        for ar in a.aramalar:
            t = ar.get("tarih", "")
            if t:
                tarihler.append(t[:10])
    elif asama in ("randevu", "gorusme"):
        for gr in a.gorusmeler:
            t = gr.get("tarih", "")
            if t:
                tarihler.append(t[:10])
    elif asama == "fiyat_verildi":
        if a.fiyat_bilgi and a.fiyat_bilgi.get("tarih"):
            tarihler.append(a.fiyat_bilgi["tarih"][:10])
    elif asama == "sozlesme":
        if a.sozlesme_bilgi and a.sozlesme_bilgi.get("sozlesme_tarihi"):
            tarihler.append(a.sozlesme_bilgi["sozlesme_tarihi"][:10])
    if not tarihler:
        return None
    try:
        ilk = date.fromisoformat(min(tarihler))
        son = date.fromisoformat(max(tarihler))
        return max((son - ilk).days, 1)
    except Exception:
        return None


# ============================================================
# 1. KAYIT SAVAŞ ODASI (WAR ROOM)
# ============================================================

def render_savas_odasi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Kayit operasyonunun canli komuta merkezi."""
    styled_section("Kayit Savas Odasi", "#dc2626")

    bugun = date.today()
    bugun_str = bugun.isoformat()
    aktifler = [a for a in adaylar if a.aktif]

    # Bugunku aktiviteler
    bugun_arama = 0
    bugun_gorusme = 0
    for a in adaylar:
        for ar in a.aramalar:
            if (ar.get("tarih", "") or "")[:10] == bugun_str:
                bugun_arama += 1
        for gr in a.gorusmeler:
            if (gr.get("tarih", "") or "")[:10] == bugun_str:
                bugun_gorusme += 1

    bugun_yeni = sum(1 for a in adaylar if a.olusturma_tarihi[:10] == bugun_str)
    bugun_kayit = sum(1 for a in adaylar if a.kapanma_tarihi and a.kapanma_tarihi[:10] == bugun_str and a.asama == "kesin_kayit")

    fiyat_adaylar = [a for a in aktifler if a.asama == "fiyat_verildi"]
    sozlesme_adaylar = [a for a in aktifler if a.asama == "sozlesme"]
    kritik = [a for a in fiyat_adaylar + sozlesme_adaylar if _son_temas_gun(a) >= 2]

    bugun_aranacak = [a for a in aktifler
                       if a.sonraki_takip and a.sonraki_takip[:10] <= bugun_str
                       and a.asama in ("aday", "arandi")]
    bugun_randevu = [a for a in aktifler if a.randevu_tarihi and a.randevu_tarihi[:10] == bugun_str]

    # Pipeline funnel sayilari
    pipeline = Counter(a.asama for a in adaylar)
    kesin = pipeline.get("kesin_kayit", 0)
    toplam = len(adaylar)
    donusum = round(kesin / max(toplam, 1) * 100, 1)

    # ── WAR ROOM HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#450a0a 0%,#7f1d1d 50%,#991b1b 100%);
                border:2px solid #ef4444;border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(239,68,68,0.3);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,#ef4444,#fca5a5,#ef4444,transparent);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:10px;color:#fca5a5;letter-spacing:3px;text-transform:uppercase;">
                    SmartCampus AI</div>
                <div style="font-size:28px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;">Kayit Savas Odasi</div>
                <div style="font-size:11px;color:#fca5a5;margin-top:4px;">
                    {bugun.strftime('%d.%m.%Y')} · Canli Komuta Merkezi</div>
            </div>
            <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:16px;padding:14px 24px;">
                <div style="font-size:42px;font-weight:900;color:#fbbf24;line-height:1;">{len(aktifler)}</div>
                <div style="font-size:9px;color:#fca5a5;letter-spacing:1.5px;">AKTIF ADAY</div>
            </div>
        </div>

        <!-- BUGUNUN RAKAMLARI -->
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:14px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:24px;font-weight:900;color:#fbbf24;">{bugun_arama}</div>
                <div style="font-size:8px;color:#fca5a5;">Bugun Arama</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:24px;font-weight:900;color:#a78bfa;">{bugun_gorusme}</div>
                <div style="font-size:8px;color:#fca5a5;">Bugun Gorusme</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:24px;font-weight:900;color:#34d399;">{bugun_yeni}</div>
                <div style="font-size:8px;color:#fca5a5;">Yeni Aday</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:24px;font-weight:900;color:#38bdf8;">{bugun_kayit}</div>
                <div style="font-size:8px;color:#fca5a5;">Bugun Kayit</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:10px;text-align:center;">
                <div style="font-size:24px;font-weight:900;color:#ef4444;">{len(kritik)}</div>
                <div style="font-size:8px;color:#fca5a5;">Acil Mudahale</div></div>
        </div>

        <!-- DONUSUM FUNNEL -->
        <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:10px 14px;">
            <div style="font-size:9px;color:#fca5a5;letter-spacing:1px;margin-bottom:6px;">PIPELINE FUNNEL</div>
            <div style="display:flex;gap:4px;align-items:center;">
    """, unsafe_allow_html=True)

    # Funnel bars
    funnel_html = ""
    max_sayi = max(pipeline.values()) if pipeline else 1
    for asama in PIPELINE_ASAMALARI + ["olumsuz"]:
        sayi = pipeline.get(asama, 0)
        info = PIPELINE_INFO.get(asama, {})
        bar_h = max(4, round(sayi / max_sayi * 40))
        funnel_html += (
            f'<div style="flex:1;text-align:center;">'
            f'<div style="font-size:14px;font-weight:800;color:#fff;">{sayi}</div>'
            f'<div style="height:{bar_h}px;background:{info.get("color", "#64748b")};border-radius:3px;margin:2px 0;"></div>'
            f'<div style="font-size:7px;color:#94a3b8;">{info.get("emoji", "")} {info.get("label", asama)[:8]}</div></div>')

    st.markdown(f"""{funnel_html}
            </div>
            <div style="text-align:right;font-size:10px;color:#fbbf24;font-weight:700;margin-top:4px;">
                Donusum: %{donusum}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── ACİL MÜDAHALE KUYRUGU ──
    col1, col2 = st.columns(2)

    with col1:
        styled_section("Acil Mudahale (Kapanisa Yakin)", "#ef4444")
        if kritik:
            for a in sorted(kritik, key=lambda x: -_son_temas_gun(x))[:8]:
                gun = _son_temas_gun(a)
                info = a.pipeline_info
                st.markdown(f"""
                <div style="background:#450a0a;border:1px solid #ef4444;border-left:4px solid {info['color']};
                            border-radius:0 10px 10px 0;padding:8px 12px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#fca5a5;font-size:12px;">{a.veli_adi}</span>
                        <span style="background:#ef4444;color:#fff;padding:2px 8px;border-radius:6px;font-size:9px;font-weight:700;">{gun}g sessiz</span>
                    </div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:2px;">
                        {a.ogrenci_adi} · {info['emoji']} {info['label']} · {a.arama_sayisi}A/{a.gorusme_sayisi}G</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Acil mudahale gereken aday yok!")

    with col2:
        styled_section("Bugun Yapilacaklar", "#f59e0b")
        # Aranacaklar
        if bugun_aranacak:
            st.markdown(f"**Aranacak: {len(bugun_aranacak)}**")
            for a in bugun_aranacak[:5]:
                st.markdown(f"<div style='font-size:11px;color:#fbbf24;padding:2px 0;'>📞 {a.veli_adi} — {a.ogrenci_adi} ({a.kademe})</div>", unsafe_allow_html=True)
            if len(bugun_aranacak) > 5:
                st.caption(f"+{len(bugun_aranacak) - 5} daha")

        # Randevular
        if bugun_randevu:
            st.markdown(f"**Randevu: {len(bugun_randevu)}**")
            for a in bugun_randevu[:5]:
                st.markdown(f"<div style='font-size:11px;color:#38bdf8;padding:2px 0;'>📅 {a.veli_adi} — {a.randevu_saati or '--:--'}</div>", unsafe_allow_html=True)

        if not bugun_aranacak and not bugun_randevu:
            st.info("Bugunku is listesi bos.")

    # ── KOORDİNATÖR PERFORMANSI ──
    styled_section("Koordinator Performansi (Bugun)")
    yapan_kisi_sayac = Counter()
    for a in adaylar:
        for ar in a.aramalar:
            if (ar.get("tarih", "") or "")[:10] == bugun_str:
                yapan = ar.get("yapan_kisi", "Belirtilmedi")
                yapan_kisi_sayac[yapan] += 1
        for gr in a.gorusmeler:
            if (gr.get("tarih", "") or "")[:10] == bugun_str:
                yapan = gr.get("yapan_kisi", "Belirtilmedi")
                yapan_kisi_sayac[yapan] += 1

    if yapan_kisi_sayac:
        en_cok = yapan_kisi_sayac.most_common(1)[0][1]
        for kisi, sayi in yapan_kisi_sayac.most_common(10):
            bar_w = round(sayi / max(en_cok, 1) * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{kisi}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#ef4444;border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:9px;color:#fff;font-weight:700;">{sayi} islem</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.caption("Bugun henuz islem yapilmamis.")


# ============================================================
# 2. ADAY YOLCULUK HARİTASI + TIKANMA DEDEKTÖRÜ
# ============================================================

_ASAMA_SIRASI = ["aday", "arandi", "randevu", "gorusme", "fiyat_verildi", "sozlesme", "kesin_kayit"]


def _aday_yolculuk(a: KayitAday) -> list[dict]:
    """Bir adayin yolculuk adimlari."""
    adimlar = []
    # Kayit
    adimlar.append({"asama": "aday", "tarih": a.olusturma_tarihi[:10], "not": f"Kanal: {a.kanal or '-'}"})
    # Aramalar
    for ar in a.aramalar:
        adimlar.append({"asama": "arandi", "tarih": (ar.get("tarih", "") or "")[:10],
                         "not": ar.get("sonuc", "")})
    # Gorusmeler
    for gr in a.gorusmeler:
        adimlar.append({"asama": "gorusme", "tarih": (gr.get("tarih", "") or "")[:10],
                         "not": gr.get("sonuc", "")})
    # Fiyat
    if a.fiyat_bilgi and a.fiyat_bilgi.get("tarih"):
        fiyat = a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0))
        adimlar.append({"asama": "fiyat_verildi", "tarih": a.fiyat_bilgi["tarih"][:10],
                         "not": f"{fiyat:,.0f} TL" if fiyat else ""})
    # Sozlesme
    if a.sozlesme_bilgi and a.sozlesme_bilgi.get("sozlesme_tarihi"):
        adimlar.append({"asama": "sozlesme", "tarih": a.sozlesme_bilgi["sozlesme_tarihi"][:10],
                         "not": a.sozlesme_bilgi.get("kayit_sonucu", "")})
    # Kesin kayit
    if a.asama == "kesin_kayit" and a.kapanma_tarihi:
        adimlar.append({"asama": "kesin_kayit", "tarih": a.kapanma_tarihi[:10], "not": "Kesin Kayit"})

    adimlar.sort(key=lambda x: x["tarih"])
    return adimlar


def render_yolculuk_haritasi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Aday yolculuk haritasi + pipeline tikanma analizi."""
    styled_section("Aday Yolculuk Haritasi", "#6366f1")
    styled_info_banner(
        "Her adayin kayit surecini gorsel zaman cizelgesinde gor. "
        "Pipeline darbogazlarini otomatik tespit et.",
        banner_type="info", icon="🗺️")

    sub = st.tabs(["🗺️ Bireysel Yolculuk", "🔍 Tikanma Analizi"])

    # ═══ BİREYSEL YOLCULUK ═══
    with sub[0]:
        aday_labels = [f"{a.veli_adi} — {a.ogrenci_adi} ({a.pipeline_info['label']})" for a in adaylar[:200]]
        secili = st.selectbox("Aday Secin", [""] + aday_labels, key="yh_aday")

        if secili:
            idx = aday_labels.index(secili)
            a = adaylar[idx]
            adimlar = _aday_yolculuk(a)

            # Toplam sure
            if len(adimlar) >= 2:
                try:
                    ilk = date.fromisoformat(adimlar[0]["tarih"])
                    son = date.fromisoformat(adimlar[-1]["tarih"])
                    toplam_gun = (son - ilk).days
                except Exception:
                    toplam_gun = 0
            else:
                toplam_gun = 0

            # Per-stage durations via _asama_suresi
            asama_gun_map = {}
            for _as in ["aday", "arandi", "gorusme", "fiyat_verildi", "sozlesme"]:
                s_gun = _asama_suresi(a, _as)
                if s_gun is not None:
                    asama_gun_map[_as] = s_gun

            info = a.pipeline_info
            asama_badges = "".join(
                f'<span style="background:#1e293b;color:#94a3b8;padding:2px 6px;border-radius:4px;'
                f'font-size:9px;margin-left:4px;">{k}:{v}g</span>'
                for k, v in asama_gun_map.items()
            )
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {info['color']}40;border-radius:16px;
                        padding:16px 20px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:800;color:#fff;font-size:16px;">{a.veli_adi}</span>
                        <span style="color:#94a3b8;font-size:12px;margin-left:8px;">— {a.ogrenci_adi}</span>
                    </div>
                    <div style="display:flex;gap:8px;">
                        <span style="background:{info['color']};color:#fff;padding:3px 12px;border-radius:8px;
                                    font-size:11px;font-weight:700;">{info['emoji']} {info['label']}</span>
                        <span style="background:#1e293b;color:#e2e8f0;padding:3px 12px;border-radius:8px;
                                    font-size:11px;font-weight:700;">{toplam_gun} gun surec</span>
                    </div>
                </div>
                <div style="margin-top:6px;">{asama_badges}</div>
            </div>""", unsafe_allow_html=True)

            # Timeline
            for i, adim in enumerate(adimlar):
                a_info = PIPELINE_INFO.get(adim["asama"], {"color": "#64748b", "emoji": "", "label": adim["asama"]})
                # Bekleme suresi
                bekleme = ""
                if i > 0:
                    try:
                        onceki = date.fromisoformat(adimlar[i-1]["tarih"])
                        simdi = date.fromisoformat(adim["tarih"])
                        gun_fark = (simdi - onceki).days
                        bekleme_renk = "#ef4444" if gun_fark > 7 else "#f59e0b" if gun_fark > 3 else "#10b981"
                        bekleme = f'<span style="background:{bekleme_renk}20;color:{bekleme_renk};padding:1px 6px;border-radius:4px;font-size:9px;font-weight:700;margin-left:8px;">{gun_fark}g bekleme</span>'
                    except Exception:
                        pass

                st.markdown(f"""
                <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:2px;">
                    <div style="display:flex;flex-direction:column;align-items:center;min-width:30px;">
                        <div style="width:12px;height:12px;border-radius:50%;background:{a_info['color']};
                                    border:2px solid {a_info['color']};"></div>
                        {'<div style="width:2px;height:24px;background:#334155;"></div>' if i < len(adimlar) - 1 else ''}
                    </div>
                    <div style="flex:1;padding-bottom:8px;">
                        <div style="display:flex;align-items:center;gap:6px;">
                            <span style="font-size:11px;font-weight:700;color:{a_info['color']};">{a_info['emoji']} {a_info['label']}</span>
                            <span style="font-size:10px;color:#64748b;">{adim['tarih']}</span>
                            {bekleme}
                        </div>
                        <div style="font-size:10px;color:#94a3b8;margin-top:2px;">{adim['not']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ═══ TIKANMA ANALİZİ ═══
    with sub[1]:
        styled_section("Pipeline Tikanma Analizi")
        styled_info_banner(
            "Her asamada ortalama bekleme suresi + darbogazlar. "
            "Sektör ortalamasıyla karşılaştırma.",
            banner_type="info", icon="🔍")

        # Her asamada ortalama sure hesapla
        asama_sureleri: dict[str, list[int]] = {a: [] for a in _ASAMA_SIRASI}

        for aday in adaylar:
            yolculuk = _aday_yolculuk(aday)
            onceki_tarih = None
            for adim in yolculuk:
                if onceki_tarih and adim["tarih"]:
                    try:
                        fark = (date.fromisoformat(adim["tarih"]) - date.fromisoformat(onceki_tarih)).days
                        if fark >= 0:
                            asama_sureleri.setdefault(adim["asama"], []).append(fark)
                    except Exception:
                        pass
                onceki_tarih = adim["tarih"]

        # Sektör ortalamalari (benchmark)
        sektor_ort = {"aday": 0, "arandi": 2, "randevu": 3, "gorusme": 5,
                       "fiyat_verildi": 5, "sozlesme": 7, "kesin_kayit": 3}

        styled_section("Asama Bazli Bekleme Suresi")
        for asama in _ASAMA_SIRASI:
            sureler = asama_sureleri.get(asama, [])
            info = PIPELINE_INFO.get(asama, {"label": asama, "color": "#64748b", "emoji": ""})
            ort = round(sum(sureler) / max(len(sureler), 1), 1) if sureler else 0
            sektor = sektor_ort.get(asama, 5)

            fark = ort - sektor
            fark_renk = "#ef4444" if fark > 3 else "#f59e0b" if fark > 0 else "#10b981"
            fark_txt = f"+{fark:.0f}g yavas" if fark > 0 else f"{fark:.0f}g hizli" if fark < 0 else "esit"

            bar_max = max(ort, sektor, 1)
            ort_w = round(ort / bar_max * 100)
            sek_w = round(sektor / bar_max * 100)

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-left:4px solid {info['color']};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{info['emoji']} {info['label']}</span>
                    <div style="display:flex;gap:8px;align-items:center;">
                        <span style="font-size:11px;color:#94a3b8;">Ort: <b>{ort}g</b></span>
                        <span style="font-size:11px;color:#64748b;">Sektor: {sektor}g</span>
                        <span style="background:{fark_renk}20;color:{fark_renk};padding:2px 8px;border-radius:4px;
                                    font-size:9px;font-weight:700;">{fark_txt}</span>
                    </div>
                </div>
                <div style="display:flex;gap:4px;">
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:8px;overflow:hidden;">
                        <div style="width:{ort_w}%;height:100%;background:{info['color']};border-radius:3px;"></div></div>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:8px;overflow:hidden;">
                        <div style="width:{sek_w}%;height:100%;background:#475569;border-radius:3px;"></div></div>
                </div>
                <div style="display:flex;gap:8px;margin-top:3px;font-size:8px;color:#64748b;">
                    <span>Biz ({len(sureler)} aday)</span><span>Sektor ort.</span></div>
            </div>""", unsafe_allow_html=True)

        # En buyuk darboğaz
        darbogazlar = []
        for asama in _ASAMA_SIRASI:
            sureler = asama_sureleri.get(asama, [])
            if sureler:
                ort = sum(sureler) / len(sureler)
                sektor = sektor_ort.get(asama, 5)
                if ort > sektor + 2:
                    darbogazlar.append((asama, ort, sektor))

        if darbogazlar:
            darbogazlar.sort(key=lambda x: -(x[1] - x[2]))
            styled_section("Tespit Edilen Darbogazlar")
            for asama, ort, sektor in darbogazlar[:3]:
                info = PIPELINE_INFO.get(asama, {"label": asama, "emoji": ""})
                st.error(f"**{info['emoji']} {info['label']}** — Ort: {ort:.1f} gun vs Sektor: {sektor} gun "
                         f"(+{ort - sektor:.0f} gun gecikme)")


# ============================================================
# 3. AI TAHMİN MOTORU + GELİR PROJEKSİYON
# ============================================================

def render_ai_tahmin(store: KayitDataStore, adaylar: list[KayitAday]):
    """AI tahmin motoru — gelecek 30/60/90 gun kayit + gelir projeksiyonu."""
    styled_section("AI Tahmin & Gelir Projeksiyon", "#f59e0b")
    styled_info_banner(
        "Mevcut pipeline verisine dayanarak gelecek 30/60/90 gun icin kayit tahmini, "
        "gelir projeksiyonu ve kayip onleme skoru.",
        banner_type="info", icon="🔮")

    aktifler = [a for a in adaylar if a.aktif]
    kesin_kayitlar = [a for a in adaylar if a.asama == "kesin_kayit"]

    # Tarihsel donusum oranlari
    toplam = len(adaylar)
    kesin = len(kesin_kayitlar)
    olumsuz = sum(1 for a in adaylar if a.asama == "olumsuz")
    tarihsel_donusum = round(kesin / max(toplam, 1) * 100, 1)

    # Asama bazli donusum tahminleri
    asama_donusum = {
        "aday": 0.15, "arandi": 0.25, "randevu": 0.45, "gorusme": 0.55,
        "fiyat_verildi": 0.70, "sozlesme": 0.90,
    }

    # Ortalama ucret
    fiyatlar = [float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
                for a in adaylar if a.fiyat_bilgi and float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0) > 0]
    ort_ucret = round(sum(fiyatlar) / max(len(fiyatlar), 1)) if fiyatlar else 50000

    # ── TAHMİN HESAPLAMA ──
    tahmini_kayit = 0
    iyimser = 0
    kotumser = 0
    kademe_tahmin = Counter()
    aday_risk = []

    for a in aktifler:
        oran = asama_donusum.get(a.asama, 0.1)
        gun = _son_temas_gun(a)
        # Sessizlik cezasi
        if gun > 14:
            oran *= 0.3
        elif gun > 7:
            oran *= 0.5
        elif gun > 3:
            oran *= 0.8

        tahmini_kayit += oran
        iyimser += min(oran * 1.3, 1.0)
        kotumser += max(oran * 0.6, 0)
        kademe_tahmin[a.kademe or "Belirtilmedi"] += oran

        # Kayip riski
        kayip_risk = round((1 - oran) * 100, 1)
        if kayip_risk >= 60:
            potansiyel = float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
            aday_risk.append({"aday": a, "risk": kayip_risk, "potansiyel": potansiyel or ort_ucret})

    tahmini_kayit = round(tahmini_kayit)
    iyimser = round(iyimser)
    kotumser = round(kotumser)

    # Gelir projeksiyonu
    tahmini_gelir = tahmini_kayit * ort_ucret
    iyimser_gelir = iyimser * ort_ucret
    kotumser_gelir = kotumser * ort_ucret

    # Kurtarilabilir gelir
    aday_risk.sort(key=lambda x: -x["risk"])
    kurtarilabilir = sum(r["potansiyel"] for r in aday_risk[:20])

    # ── HERO KART ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 50%,#a16207 100%);
                border:2px solid #fbbf24;border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(251,191,36,0.25);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,#fbbf24,#fde68a,#fbbf24,transparent);"></div>
        <div style="text-align:center;margin-bottom:16px;">
            <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">
                AI Kayit Tahmini</div>
            <div style="font-size:56px;font-weight:900;color:#fbbf24;
                        font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">+{tahmini_kayit}</div>
            <div style="font-size:12px;color:#fde68a;">
                Tahmini ek kesin kayit (mevcut pipeline'dan)</div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;text-align:center;">
                <div style="font-size:10px;color:#94a3b8;">Iyimser</div>
                <div style="font-size:24px;font-weight:900;color:#10b981;">{iyimser}</div>
                <div style="font-size:9px;color:#64748b;">{iyimser_gelir:,.0f} TL</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;text-align:center;border:1px solid #fbbf24;">
                <div style="font-size:10px;color:#fbbf24;">Gercekci</div>
                <div style="font-size:24px;font-weight:900;color:#fbbf24;">{tahmini_kayit}</div>
                <div style="font-size:9px;color:#fde68a;">{tahmini_gelir:,.0f} TL</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:12px;padding:12px;text-align:center;">
                <div style="font-size:10px;color:#94a3b8;">Kotumser</div>
                <div style="font-size:24px;font-weight:900;color:#ef4444;">{kotumser}</div>
                <div style="font-size:9px;color:#64748b;">{kotumser_gelir:,.0f} TL</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── DETAY SEKMELER ──
    t_sub = st.tabs(["📊 Kademe Tahmin", "💰 Gelir Projeksiyon", "🚨 Kayip Onleme"])

    # Kademe bazli
    with t_sub[0]:
        styled_section("Kademe Bazli Kayit Tahmini")
        for kademe in KADEME_SECENEKLERI:
            tahmin = round(kademe_tahmin.get(kademe, 0))
            aktif_k = sum(1 for a in aktifler if a.kademe == kademe)
            if aktif_k == 0 and tahmin == 0:
                continue
            bar_w = min(100, round(tahmin / max(tahmini_kayit, 1) * 100))
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="min-width:80px;font-weight:700;color:#e2e8f0;font-size:12px;">{kademe}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:20px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#fbbf24;border-radius:4px;
                                display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:10px;color:#1a1a2e;font-weight:700;">+{tahmin}</span>
                    </div>
                </div>
                <span style="font-size:10px;color:#94a3b8;min-width:60px;">{aktif_k} aktif</span>
            </div>""", unsafe_allow_html=True)

    # Gelir projeksiyon
    with t_sub[1]:
        styled_section("Gelir Projeksiyon Tablosu")
        mevcut_gelir = len(kesin_kayitlar) * ort_ucret

        for donem, carpan in [("30 Gun", 0.5), ("60 Gun", 0.8), ("90 Gun", 1.0)]:
            d_kayit = round(tahmini_kayit * carpan)
            d_gelir = d_kayit * ort_ucret
            toplam = mevcut_gelir + d_gelir
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                        padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{donem}</span>
                <div style="display:flex;gap:16px;font-size:11px;">
                    <span style="color:#94a3b8;">+{d_kayit} kayit</span>
                    <span style="color:#fbbf24;font-weight:700;">+{d_gelir:,.0f} TL</span>
                    <span style="color:#10b981;font-weight:700;">Toplam: {toplam:,.0f} TL</span>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #fbbf24;border-radius:12px;padding:14px;
                    text-align:center;margin-top:12px;">
            <div style="font-size:10px;color:#94a3b8;">Ortalama Ucret Baz: {ort_ucret:,.0f} TL ({len(fiyatlar)} fiyat verisi)</div>
            <div style="font-size:10px;color:#64748b;margin-top:4px;">Tarihsel Donusum: %{tarihsel_donusum} · Mevcut Kayit: {kesin} · Aktif Pipeline: {len(aktifler)}</div>
        </div>""", unsafe_allow_html=True)

    # Kayip onleme
    with t_sub[2]:
        styled_section("Yuksek Kayip Riskli Adaylar")
        if not aday_risk:
            st.success("Yuksek kayip riski tasiyan aday yok!")
        else:
            toplam_risk_gelir = sum(r["potansiyel"] for r in aday_risk)
            st.markdown(f"""
            <div style="background:#7f1d1d;border:1px solid #ef4444;border-radius:12px;
                        padding:14px;text-align:center;margin-bottom:12px;">
                <div style="font-size:10px;color:#fca5a5;letter-spacing:1px;">KURTARILABILIR GELIR</div>
                <div style="font-size:32px;font-weight:900;color:#fbbf24;">{toplam_risk_gelir:,.0f} TL</div>
                <div style="font-size:10px;color:#fca5a5;">{len(aday_risk)} aday kayip riski tasiyor</div>
            </div>""", unsafe_allow_html=True)

            for r in aday_risk[:15]:
                a = r["aday"]
                info = a.pipeline_info
                gun = _son_temas_gun(a)
                risk_renk = "#ef4444" if r["risk"] >= 80 else "#f97316" if r["risk"] >= 60 else "#f59e0b"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {risk_renk}30;border-left:4px solid {risk_renk};
                            border-radius:0 10px 10px 0;padding:8px 12px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{a.veli_adi}</span>
                            <span style="color:#94a3b8;font-size:10px;margin-left:6px;">— {a.ogrenci_adi}</span>
                        </div>
                        <div style="display:flex;gap:6px;">
                            <span style="background:{risk_renk}20;color:{risk_renk};padding:2px 8px;border-radius:6px;
                                        font-size:10px;font-weight:700;">%{r['risk']} risk</span>
                            <span style="color:#fbbf24;font-size:10px;font-weight:700;">{r['potansiyel']:,.0f} TL</span>
                        </div>
                    </div>
                    <div style="font-size:10px;color:#64748b;margin-top:2px;">
                        {info['emoji']} {info['label']} · {gun}g sessiz · {a.arama_sayisi}A/{a.gorusme_sayisi}G</div>
                </div>""", unsafe_allow_html=True)
