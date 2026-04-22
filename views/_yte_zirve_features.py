"""
Yonetim Tek Ekran — Zirve Ozellikleri
======================================
1. Okul Saglik Puani (School Health Index)
2. Yonetici Gunluk Ajanda + Yapiskan Notlar
3. Haftalik Karsilastirmali Trend
4. Sabah Brifing Ekrani
5. Hizli Islem Paneli (Quick Actions)
6. Haftalik Takvim Gorunumu
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from models.yonetim_ekran import (
    YTEDataStore, ModulOzetleyici, GunlukToplayici, GunlukIslemToplayici,
    RaporUreticisi, PlanlanmisGorev, GunlukRapor,
    MODUL_RENK, MODUL_IKON, _GUN_ADLARI,
    GOREV_DURUM_RENK, GOREV_DURUM_IKON,
)
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ============================================================
# 1. OKUL SAĞLIK PUANI (SCHOOL HEALTH INDEX)
# ============================================================

_SAGLIK_AGIRLIKLAR = {
    # (modul_adi, kpi_key, max_beklenti, agirlik, ters_mi)
    # ters_mi=True → dusuk deger iyi (ornegin devamsizlik)
    "Akademik Takip":       [("ogrenci_sayisi", 200, 8, False), ("not_kaydi", 500, 5, False),
                             ("devamsizlik", 200, 5, True), ("sinav_sayisi", 30, 4, False)],
    "Olcme Degerlendirme":  [("toplam_soru", 500, 5, False), ("aktif_sinav", 5, 4, False),
                             ("tamamlanan_sinav", 10, 4, False)],
    "Rehberlik":            [("toplam_vaka", 20, 3, False), ("gorusme_sayisi", 50, 4, False)],
    "Insan Kaynaklari":     [("aktif_personel", 50, 6, False), ("egitim", 10, 3, False)],
    "Butce Gelir Gider":    [("toplam_gelir", 1000000, 5, False), ("net", 0, 6, False)],
    "Okul Sagligi":         [("revir_ziyareti", 100, 3, True), ("kritik_stok", 5, 4, True)],
    "Destek Hizmetleri":    [("acik", 10, 4, True), ("tamamlanan", 50, 3, False)],
    "Sivil Savunma":        [("acik_risk", 5, 5, True), ("tatbikat_sayisi", 3, 3, False)],
    "Sosyal Etkinlik":      [("tamamlanan", 10, 3, False), ("aktif_kulup", 5, 3, False)],
    "Randevu ve Ziyaretci": [("tamamlanan", 30, 2, False)],
    "Toplanti ve Kurullar": [("yapilan", 10, 3, False)],
    "Kutuphane":            [("materyal_sayisi", 500, 2, False), ("geciken_iade", 10, 3, True)],
    "Veli Memnuniyet":      [("cevap", 100, 4, False)],
    "SWOT Analizi":         [("aksiyon", 10, 2, False)],
    "Halkla Iliskiler":     [("toplam_gorusme", 100, 3, False), ("sozlesme", 20, 4, False)],
    "Egitim Koclugu":       [("kocluk_ogrencisi", 20, 2, False), ("tamamlanan_hedef", 10, 3, False)],
}


def _hesapla_saglik_puani(kpis: dict) -> tuple[float, dict[str, float]]:
    """KPI dict'inden okul saglik puani (0-100) ve alt puanlari hesapla.
    Returns: (genel_puan, {modul: puan})
    """
    alt_puanlar: dict[str, float] = {}
    toplam_agirlik = 0
    agirlikli_toplam = 0.0

    for modul, metrikler in _SAGLIK_AGIRLIKLAR.items():
        modul_kpi = kpis.get(modul, {})
        if not modul_kpi:
            continue

        modul_puan_toplam = 0.0
        modul_agirlik_toplam = 0

        for kpi_key, max_val, agirlik, ters in metrikler:
            deger = modul_kpi.get(kpi_key, 0)
            if not isinstance(deger, (int, float)):
                continue

            if ters:
                # Dusuk deger iyi: 0 devamsizlik = 100, max devamsizlik = 0
                if max_val == 0:
                    puan = 100 if deger == 0 else 50
                else:
                    puan = max(0, min(100, 100 - (deger / max_val * 100)))
            else:
                # Yuksek deger iyi
                if kpi_key == "net":
                    # Butce dengesi: pozitif = iyi
                    puan = 100 if deger > 0 else max(0, 50 + deger / max(abs(deger) + 1, 1) * 50)
                elif max_val == 0:
                    puan = 100 if deger > 0 else 0
                else:
                    puan = min(100, deger / max_val * 100)

            modul_puan_toplam += puan * agirlik
            modul_agirlik_toplam += agirlik

        if modul_agirlik_toplam > 0:
            modul_puan = round(modul_puan_toplam / modul_agirlik_toplam, 1)
            alt_puanlar[modul] = modul_puan
            toplam_agirlik += modul_agirlik_toplam
            agirlikli_toplam += modul_puan * modul_agirlik_toplam

    genel = round(agirlikli_toplam / max(toplam_agirlik, 1), 1)
    return genel, alt_puanlar


def _saglik_renk(puan: float) -> tuple[str, str]:
    """Puana gore (renk, etiket) dondur."""
    if puan >= 85:
        return "#10b981", "Mukemmel"
    elif puan >= 70:
        return "#22c55e", "Iyi"
    elif puan >= 55:
        return "#f59e0b", "Orta"
    elif puan >= 40:
        return "#f97316", "Riskli"
    else:
        return "#ef4444", "Kritik"


def render_okul_saglik_puani():
    """Dashboard'a eklenen Okul Saglik Puani hero karti + alt puan detaylari."""
    # KPI'lari cache'den al veya yeniden hesapla
    _kpi_cache = "yte_modul_kpis"
    if _kpi_cache not in st.session_state:
        with st.spinner("Modül verileri yükleniyor..."):
            st.session_state[_kpi_cache] = ModulOzetleyici().tum_modul_kpi()
    kpis = st.session_state[_kpi_cache]

    genel_puan, alt_puanlar = _hesapla_saglik_puani(kpis)
    renk, etiket = _saglik_renk(genel_puan)

    # Kategori bazli ortalamalar
    akademik_moduls = ["Akademik Takip", "Olcme Degerlendirme", "Rehberlik", "Egitim Koclugu"]
    operasyon_moduls = ["Destek Hizmetleri", "Sivil Savunma", "Kutuphane", "Okul Sagligi"]
    kurum_moduls = ["Insan Kaynaklari", "Butce Gelir Gider", "Toplanti ve Kurullar", "Halkla Iliskiler"]
    sosyal_moduls = ["Sosyal Etkinlik", "Veli Memnuniyet", "Randevu ve Ziyaretci"]

    def _kat_ort(moduls):
        puanlar = [alt_puanlar[m] for m in moduls if m in alt_puanlar]
        return round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0

    ak_puan = _kat_ort(akademik_moduls)
    op_puan = _kat_ort(operasyon_moduls)
    kr_puan = _kat_ort(kurum_moduls)
    so_puan = _kat_ort(sosyal_moduls)

    # ── HERO KART ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
                border:2px solid {renk};border-radius:20px;padding:24px 32px;margin:0 0 18px 0;
                box-shadow:0 8px 32px {renk}30;position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,{renk},{renk},transparent);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <div style="font-size:10px;color:#94a3b8;letter-spacing:3px;text-transform:uppercase;
                            margin-bottom:4px;">SmartCampus AI</div>
                <div style="font-size:24px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;">Okul Saglik Puani</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px;">
                    {len(alt_puanlar)} modulden hesaplanan bilesik performans endeksi</div>
            </div>
            <div style="text-align:center;min-width:140px;">
                <div style="font-size:64px;font-weight:900;color:{renk};
                            font-family:Playfair Display,Georgia,serif;line-height:1;">{genel_puan}</div>
                <div style="background:{renk}20;color:{renk};padding:4px 16px;border-radius:8px;
                            font-size:11px;font-weight:800;letter-spacing:1px;margin-top:4px;">{etiket}</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px;
                    padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);">
            <div style="text-align:center;">
                <div style="font-size:22px;font-weight:800;color:{_saglik_renk(ak_puan)[0]};">{ak_puan}</div>
                <div style="font-size:9px;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;">Akademik</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:22px;font-weight:800;color:{_saglik_renk(op_puan)[0]};">{op_puan}</div>
                <div style="font-size:9px;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;">Operasyon</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:22px;font-weight:800;color:{_saglik_renk(kr_puan)[0]};">{kr_puan}</div>
                <div style="font-size:9px;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;">Kurumsal</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:22px;font-weight:800;color:{_saglik_renk(so_puan)[0]};">{so_puan}</div>
                <div style="font-size:9px;color:#94a3b8;letter-spacing:1.5px;text-transform:uppercase;">Sosyal</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── ALT PUAN DETAY (collapsible) ──
    with st.expander("Modül Bazlı Sağlık Puanları", expanded=False):
        sorted_puanlar = sorted(alt_puanlar.items(), key=lambda x: -x[1])
        for modul, puan in sorted_puanlar:
            m_renk, m_etiket = _saglik_renk(puan)
            ikon = MODUL_IKON.get(modul, "📋")
            bar_w = min(puan, 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="font-size:14px;min-width:22px;">{ikon}</span>
                <span style="min-width:160px;font-size:12px;color:#e2e8f0;font-weight:600;">{modul}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{m_renk},{m_renk}80);
                                border-radius:4px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:9px;color:#fff;font-weight:800;">{puan}</span>
                    </div>
                </div>
                <span style="min-width:60px;text-align:right;background:{m_renk}20;color:{m_renk};
                            padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">{m_etiket}</span>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 2. YÖNETİCİ GÜNLÜK AJANDA + YAPIŞKAN NOTLAR
# ============================================================

def render_yonetici_ajanda(store: YTEDataStore):
    """Yonetici gunluk ajanda — yapiskan notlar + gorev ekleme + gunluk mood."""

    styled_section("Yonetici Ajandasi", "#7c3aed")

    bugun = date.today().isoformat()
    notlar = store.load_list("ajanda_notlari")

    # Bugunun notlarini filtrele
    bugun_notlar = [n for n in notlar if n.get("tarih") == bugun]
    tum_notlar = sorted(notlar, key=lambda n: n.get("tarih", ""), reverse=True)

    sub = st.tabs(["📝 Bugün", "📋 Geçmiş", "⭐ Günlük Değerlendirme"])

    # ═══ BUGÜN ═══
    with sub[0]:
        # Mevcut notlar
        if bugun_notlar:
            for n in bugun_notlar:
                tur = n.get("tur", "not")
                if tur == "gorev":
                    tamamlandi = n.get("tamamlandi", False)
                    renk = "#10b981" if tamamlandi else "#f59e0b"
                    ikon = "✅" if tamamlandi else "⬜"
                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                                border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;
                                display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-size:13px;color:#e2e8f0;">{ikon} {n.get('icerik', '')}</span>
                        <span style="font-size:10px;color:#64748b;">{n.get('saat', '')}</span>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#fef3c7,#fde68a);
                                border-radius:10px;padding:12px 16px;margin-bottom:6px;
                                box-shadow:2px 2px 8px rgba(0,0,0,0.1);transform:rotate(-0.3deg);">
                        <div style="font-size:13px;color:#78350f;font-weight:600;">{n.get('icerik', '')}</div>
                        <div style="font-size:9px;color:#92400e;margin-top:4px;text-align:right;">
                            {n.get('saat', '')} · {n.get('kategori', '')}</div>
                    </div>""", unsafe_allow_html=True)

        # Yeni not/gorev ekleme
        st.divider()
        col1, col2 = st.columns([3, 1])
        with col1:
            yeni_icerik = st.text_input("Not veya gorev yazin...", key="yte_ajanda_input",
                                         placeholder="Ornek: Veli toplantisi icin salon ayarla")
        with col2:
            yeni_tur = st.selectbox("Tur", ["not", "gorev"], key="yte_ajanda_tur",
                                     format_func=lambda x: "📝 Not" if x == "not" else "☑️ Gorev")

        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            kategori = st.selectbox("Kategori", ["Genel", "Toplanti", "Veli", "Personel", "Acil",
                                                    "Hatirlatma", "Fikir"], key="yte_ajanda_kat")
        with ac2:
            oncelik = st.selectbox("Oncelik", ["Normal", "Yuksek", "Dusuk"], key="yte_ajanda_onc")

        if st.button("Ekle", key="yte_ajanda_ekle", type="primary", use_container_width=True):
            if yeni_icerik.strip():
                yeni_not = {
                    "id": f"an_{uuid.uuid4().hex[:8]}",
                    "tarih": bugun,
                    "saat": datetime.now().strftime("%H:%M"),
                    "icerik": yeni_icerik.strip(),
                    "tur": yeni_tur,
                    "kategori": kategori,
                    "oncelik": oncelik,
                    "tamamlandi": False,
                }
                notlar.append(yeni_not)
                store.save_list("ajanda_notlari", notlar)
                st.success("Not eklendi!")
                st.rerun()

        # Gorev tamamlama
        bugun_gorevler = [n for n in bugun_notlar if n.get("tur") == "gorev" and not n.get("tamamlandi")]
        if bugun_gorevler:
            st.divider()
            st.caption("Gorevleri tamamla:")
            for g in bugun_gorevler:
                if st.checkbox(g.get("icerik", ""), key=f"yte_at_{g['id']}"):
                    for n in notlar:
                        if n.get("id") == g["id"]:
                            n["tamamlandi"] = True
                    store.save_list("ajanda_notlari", notlar)
                    st.rerun()

    # ═══ GEÇMİŞ ═══
    with sub[1]:
        styled_section("Gecmis Notlar")
        # Son 30 gunun notlari (tarihe gore gruplanmis)
        tarihler = sorted(set(n.get("tarih", "") for n in tum_notlar if n.get("tarih")), reverse=True)
        for tarih in tarihler[:30]:
            if tarih == bugun:
                continue  # bugun zaten baska sekmede
            gun_notlari = [n for n in tum_notlar if n.get("tarih") == tarih]
            try:
                dt = date.fromisoformat(tarih)
                gun_adi = _GUN_ADLARI.get(dt.weekday(), "")
                tarih_str = f"{dt.day:02d}.{dt.month:02d}.{dt.year} {gun_adi}"
            except ValueError:
                tarih_str = tarih

            with st.expander(f"📅 {tarih_str} ({len(gun_notlari)} not)", expanded=False):
                for n in gun_notlari:
                    tur_ikon = "📝" if n.get("tur") == "not" else ("✅" if n.get("tamamlandi") else "⬜")
                    st.markdown(f"- {tur_ikon} **{n.get('icerik', '')}** "
                                f"<span style='color:#94a3b8;font-size:11px;'>"
                                f"({n.get('kategori', '')} · {n.get('saat', '')})</span>",
                                unsafe_allow_html=True)

    # ═══ GÜNLÜK DEĞERLENDİRME ═══
    with sub[2]:
        styled_section("Gunluk Degerlendirme")
        styled_info_banner(
            "Gunun sonunda kisa bir degerlendirme yapin. Haftalik trendleri takip edin.",
            banner_type="info", icon="⭐")

        # Bugunun degerlendirmesi
        bugun_deger = next((n for n in bugun_notlar if n.get("tur") == "degerlendirme"), None)

        if bugun_deger:
            yildiz = bugun_deger.get("yildiz", 3)
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #334155;border-radius:14px;
                        padding:16px 20px;text-align:center;margin-bottom:12px;">
                <div style="font-size:32px;">{'⭐' * yildiz}{'☆' * (5 - yildiz)}</div>
                <div style="font-size:13px;color:#e2e8f0;margin-top:8px;font-style:italic;">
                    "{bugun_deger.get('icerik', '')}"</div>
            </div>""", unsafe_allow_html=True)
        else:
            yildiz = st.slider("Bugunu nasil degerlendiriyorsunuz?", 1, 5, 3, key="yte_mood")
            st.markdown(f"<div style='text-align:center;font-size:28px;'>{'⭐' * yildiz}{'☆' * (5 - yildiz)}</div>",
                        unsafe_allow_html=True)
            yorum = st.text_area("Kisa degerlendirme (istege bagli)", key="yte_mood_yorum",
                                  placeholder="Bugün verimli bir gündu...", height=80)
            if st.button("Kaydet", key="yte_mood_kaydet", type="primary"):
                deger_not = {
                    "id": f"dg_{uuid.uuid4().hex[:8]}",
                    "tarih": bugun,
                    "saat": datetime.now().strftime("%H:%M"),
                    "icerik": yorum.strip() or f"{yildiz}/5 yildiz",
                    "tur": "degerlendirme",
                    "yildiz": yildiz,
                    "kategori": "Degerlendirme",
                    "oncelik": "Normal",
                    "tamamlandi": False,
                }
                notlar.append(deger_not)
                store.save_list("ajanda_notlari", notlar)
                st.success("Degerlendirme kaydedildi!")
                st.rerun()

        # Haftalik mood trendi
        st.divider()
        styled_section("Son 14 Gun Mood Trendi")
        mood_data = []
        for i in range(13, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            deger = next((n for n in tum_notlar if n.get("tarih") == d and n.get("tur") == "degerlendirme"), None)
            mood_data.append((d[5:], deger.get("yildiz", 0) if deger else 0))

        mood_html = ""
        for tarih_kisa, yildiz_val in mood_data:
            bar_h = yildiz_val * 16 if yildiz_val > 0 else 2
            renk = "#10b981" if yildiz_val >= 4 else "#f59e0b" if yildiz_val >= 3 else "#ef4444" if yildiz_val > 0 else "#334155"
            mood_html += (
                f'<div style="display:flex;flex-direction:column;align-items:center;gap:2px;">'
                f'<div style="width:20px;height:{bar_h}px;background:{renk};border-radius:3px;"></div>'
                f'<span style="font-size:8px;color:#64748b;">{tarih_kisa}</span>'
                f'<span style="font-size:9px;color:{renk};font-weight:700;">'
                f'{"⭐" if yildiz_val > 0 else "—"}{yildiz_val if yildiz_val > 0 else ""}</span></div>')

        st.markdown(f"""
        <div style="display:flex;gap:6px;align-items:flex-end;justify-content:center;
                    background:#0f172a;border-radius:12px;padding:16px;margin:8px 0;
                    min-height:100px;">
            {mood_html}
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. HAFTALIK KARŞILAŞTIRMALI TREND
# ============================================================

def render_haftalik_trend(store: YTEDataStore):
    """Bu hafta vs gecen hafta karsilastirma + en iyi/en kotu modul."""

    styled_section("Haftalik Karsilastirma", "#2563eb")

    bugun = date.today()
    # Bu haftanin baslangici (Pazartesi)
    bu_hafta_bas = bugun - timedelta(days=bugun.weekday())
    gecen_hafta_bas = bu_hafta_bas - timedelta(days=7)
    gecen_hafta_bit = bu_hafta_bas - timedelta(days=1)

    # Bu hafta ve gecen haftanin raporlarini yukle
    raporlar = store.load_objects("raporlar")

    bu_hafta_rap = [r for r in raporlar if bu_hafta_bas.isoformat() <= r.tarih <= bugun.isoformat()]
    gecen_hafta_rap = [r for r in raporlar if gecen_hafta_bas.isoformat() <= r.tarih <= gecen_hafta_bit.isoformat()]

    # Metrikleri hesapla
    def _hafta_metrik(rap_list):
        if not rap_list:
            return {"planlanan": 0, "gerceklesen": 0, "iptal": 0, "oran": 0, "modul_islem": 0, "gun": 0}
        toplam_plan = sum(r.planlanan_sayi for r in rap_list)
        toplam_gercek = sum(r.gerceklesen_sayi for r in rap_list)
        toplam_iptal = sum(r.iptal_sayi for r in rap_list)
        ort_oran = round(sum(r.gerceklesme_orani for r in rap_list) / len(rap_list), 1)
        # Modul islem sayisi (raporlardan)
        toplam_islem = 0
        for r in rap_list:
            if r.modul_islemler:
                for items in r.modul_islemler.values():
                    if isinstance(items, list):
                        toplam_islem += sum(i.get("sayi", 0) for i in items)
        return {
            "planlanan": toplam_plan, "gerceklesen": toplam_gercek,
            "iptal": toplam_iptal, "oran": ort_oran,
            "modul_islem": toplam_islem, "gun": len(rap_list),
        }

    bu = _hafta_metrik(bu_hafta_rap)
    gecen = _hafta_metrik(gecen_hafta_rap)

    def _degisim(bu_val, gecen_val):
        if gecen_val == 0:
            return ("+∞" if bu_val > 0 else "—"), "#10b981"
        fark = round((bu_val - gecen_val) / gecen_val * 100, 1)
        renk = "#10b981" if fark >= 0 else "#ef4444"
        return (f"+{fark}%" if fark >= 0 else f"{fark}%"), renk

    d_plan, d_plan_r = _degisim(bu["planlanan"], gecen["planlanan"])
    d_gercek, d_gercek_r = _degisim(bu["gerceklesen"], gecen["gerceklesen"])
    d_oran, d_oran_r = _degisim(bu["oran"], gecen["oran"])
    d_islem, d_islem_r = _degisim(bu["modul_islem"], gecen["modul_islem"])

    # ── HERO KART ──
    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:20px 24px;margin:12px 0;">
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
            <div style="text-align:center;">
                <div style="font-size:10px;color:#64748b;letter-spacing:1px;text-transform:uppercase;">Planlanan</div>
                <div style="font-size:28px;font-weight:800;color:#3b82f6;">{bu['planlanan']}</div>
                <div style="font-size:10px;color:#64748b;">gecen: {gecen['planlanan']}</div>
                <div style="font-size:11px;font-weight:700;color:{d_plan_r};margin-top:2px;">{d_plan}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:10px;color:#64748b;letter-spacing:1px;text-transform:uppercase;">Gerceklesen</div>
                <div style="font-size:28px;font-weight:800;color:#10b981;">{bu['gerceklesen']}</div>
                <div style="font-size:10px;color:#64748b;">gecen: {gecen['gerceklesen']}</div>
                <div style="font-size:11px;font-weight:700;color:{d_gercek_r};margin-top:2px;">{d_gercek}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:10px;color:#64748b;letter-spacing:1px;text-transform:uppercase;">Ort. Oran</div>
                <div style="font-size:28px;font-weight:800;color:#f59e0b;">%{bu['oran']}</div>
                <div style="font-size:10px;color:#64748b;">gecen: %{gecen['oran']}</div>
                <div style="font-size:11px;font-weight:700;color:{d_oran_r};margin-top:2px;">{d_oran}</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:10px;color:#64748b;letter-spacing:1px;text-transform:uppercase;">Modul Islem</div>
                <div style="font-size:28px;font-weight:800;color:#7c3aed;">{bu['modul_islem']}</div>
                <div style="font-size:10px;color:#64748b;">gecen: {gecen['modul_islem']}</div>
                <div style="font-size:11px;font-weight:700;color:{d_islem_r};margin-top:2px;">{d_islem}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── MODÜL BAZLI HAFTALIK KARŞILAŞTIRMA ──
    # Bu hafta ve gecen haftanin modul_ozet verilerini topla
    bu_modul: dict[str, int] = {}
    gecen_modul: dict[str, int] = {}

    for r in bu_hafta_rap:
        for modul, ozet in (r.modul_ozet or {}).items():
            bu_modul[modul] = bu_modul.get(modul, 0) + ozet.get("planlanan", 0)
    for r in gecen_hafta_rap:
        for modul, ozet in (r.modul_ozet or {}).items():
            gecen_modul[modul] = gecen_modul.get(modul, 0) + ozet.get("planlanan", 0)

    tum_moduller = sorted(set(list(bu_modul.keys()) + list(gecen_modul.keys())))

    if tum_moduller:
        # En cok yukselen ve en cok dusen
        degisimler = []
        for m in tum_moduller:
            bu_val = bu_modul.get(m, 0)
            gecen_val = gecen_modul.get(m, 0)
            if gecen_val > 0:
                fark_pct = round((bu_val - gecen_val) / gecen_val * 100, 1)
            elif bu_val > 0:
                fark_pct = 100
            else:
                fark_pct = 0
            degisimler.append((m, bu_val, gecen_val, fark_pct))

        degisimler.sort(key=lambda x: -x[3])
        yukselenler = [d for d in degisimler if d[3] > 0][:3]
        dusenler = [d for d in degisimler if d[3] < 0][-3:]

        col1, col2 = st.columns(2)
        with col1:
            styled_section("Yukselen Moduller", "#10b981")
            if yukselenler:
                for m, bu_v, gc_v, fark in yukselenler:
                    ikon = MODUL_IKON.get(m, "📋")
                    st.markdown(f"""
                    <div style="background:#064e3b;border:1px solid #10b981;border-radius:10px;
                                padding:10px 14px;margin-bottom:6px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#e2e8f0;font-weight:600;">{ikon} {m}</span>
                            <span style="color:#10b981;font-weight:800;">▲ +{fark}%</span>
                        </div>
                        <div style="font-size:10px;color:#94a3b8;margin-top:3px;">
                            {gc_v} → {bu_v} gorev/islem</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Bu hafta yukselen modul yok.")

        with col2:
            styled_section("Dusen Moduller", "#ef4444")
            if dusenler:
                for m, bu_v, gc_v, fark in reversed(dusenler):
                    ikon = MODUL_IKON.get(m, "📋")
                    st.markdown(f"""
                    <div style="background:#450a0a;border:1px solid #ef4444;border-radius:10px;
                                padding:10px 14px;margin-bottom:6px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#e2e8f0;font-weight:600;">{ikon} {m}</span>
                            <span style="color:#ef4444;font-weight:800;">▼ {fark}%</span>
                        </div>
                        <div style="font-size:10px;color:#94a3b8;margin-top:3px;">
                            {gc_v} → {bu_v} gorev/islem</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Bu hafta dusen modul yok!")

    # ── 4 HAFTALIK SPARKLINE ──
    styled_section("4 Haftalik Trend")
    hafta_verileri = []
    for i in range(3, -1, -1):
        h_bas = bu_hafta_bas - timedelta(weeks=i)
        h_bit = h_bas + timedelta(days=6)
        h_rap = [r for r in raporlar if h_bas.isoformat() <= r.tarih <= h_bit.isoformat()]
        h_plan = sum(r.planlanan_sayi for r in h_rap)
        h_gercek = sum(r.gerceklesen_sayi for r in h_rap)
        h_oran = round(sum(r.gerceklesme_orani for r in h_rap) / max(len(h_rap), 1), 1) if h_rap else 0
        hafta_verileri.append({
            "label": f"{h_bas.day:02d}.{h_bas.month:02d}",
            "plan": h_plan, "gercek": h_gercek, "oran": h_oran, "gun": len(h_rap),
        })

    max_plan = max((h["plan"] for h in hafta_verileri), default=1) or 1
    spark_html = ""
    for i, h in enumerate(hafta_verileri):
        is_current = i == len(hafta_verileri) - 1
        bar_h = max(4, round(h["plan"] / max_plan * 60))
        bar_renk = "#c9a84c" if is_current else "#3b82f6"
        border = "border:2px solid #c9a84c;" if is_current else ""
        spark_html += (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;'
            f'background:#0f172a;border-radius:10px;padding:10px 14px;min-width:70px;{border}">'
            f'<div style="font-size:9px;color:#64748b;">Hafta {i+1}</div>'
            f'<div style="width:30px;height:{bar_h}px;background:{bar_renk};border-radius:4px;"></div>'
            f'<div style="font-size:14px;font-weight:800;color:#e2e8f0;">{h["plan"]}</div>'
            f'<div style="font-size:9px;color:#64748b;">%{h["oran"]}</div>'
            f'<div style="font-size:8px;color:#475569;">{h["label"]}</div></div>')

    st.markdown(f"""
    <div style="display:flex;gap:10px;justify-content:center;align-items:flex-end;margin:8px 0;">
        {spark_html}
    </div>""", unsafe_allow_html=True)

    if not bu_hafta_rap and not gecen_hafta_rap:
        styled_info_banner(
            "Haftalik karsilastirma icin en az 1 haftalik gun sonu raporu gereklidir. "
            "Gunluk Islemler > Gun Sonu sekmesinden rapor olusturun.",
            banner_type="warning", icon="⚠️")


# ============================================================
# 4. SABAH BRİFİNG EKRANI — "BUGÜN OKULDA NE VAR?"
# ============================================================

def _tenant_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _load_json_safe(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def render_sabah_brifing(store: YTEDataStore):
    """Sabah brifing — bugün okulda ne var, tek bakışta tüm resim."""
    bugun = date.today()
    bugun_str = bugun.isoformat()
    try:
        gun_adi = _GUN_ADLARI.get(bugun.weekday(), "")
        tarih_pretty = f"{bugun.day:02d}.{bugun.month:02d}.{bugun.year} {gun_adi}"
    except Exception:
        tarih_pretty = bugun_str

    td = _tenant_dir()

    # ── VERİ TOPLAMA (tüm modüllerden) ──
    # 1. Bugünün görevleri (GunlukToplayici)
    gt = GunlukToplayici(bugun_str)
    gorevler = gt.topla()
    modul_sayac = Counter(g.kaynak_modul for g in gorevler)
    toplanti_sayi = sum(1 for g in gorevler if g.kaynak_tipi in ("toplanti", "aksiyon"))
    sinav_sayi = sum(1 for g in gorevler if g.kaynak_tipi in ("sinav", "online_sinav"))
    etkinlik_sayi = sum(1 for g in gorevler if g.kaynak_tipi in ("etkinlik", "kulup_faaliyet"))
    randevu_sayi = sum(1 for g in gorevler if g.kaynak_tipi in ("randevu", "kayit_randevu", "veli_gorusme", "kayit_gorusme"))
    kritik_sayi = sum(1 for g in gorevler if g.oncelik in ("Kritik", "Yuksek"))

    # 2. İzinli personel
    izinli_personel = []
    try:
        from models.insan_kaynaklari import IKDataStore
        ik = IKDataStore(os.path.join(td, "ik"))
        for iz in ik.load_list("izinler"):
            bas = iz.get("baslangic_tarihi", "")
            bit = iz.get("bitis_tarihi", "") or bas
            if bas and bas <= bugun_str <= bit:
                izinli_personel.append(iz.get("personel_adi", "?"))
    except Exception:
        pass

    # 3. İzinli öğretmen
    izinli_ogretmen = []
    try:
        ak_dir = os.path.join("data", "akademik")
        try:
            from utils.tenant import get_data_path
            ak_dir = get_data_path("akademik")
        except Exception:
            pass
        ogr_izinler = _load_json_safe(os.path.join(ak_dir, "ogretmen_izin.json"))
        for oi in ogr_izinler:
            bas = oi.get("baslangic_tarihi", "")
            bit = oi.get("bitis_tarihi", "") or bas
            if bas and bas <= bugun_str <= bit and oi.get("durum") == "onaylandi":
                izinli_ogretmen.append(oi.get("ogretmen_adi", "?"))
    except Exception:
        pass

    # 4. Dünün devamsızlık
    dun = (bugun - timedelta(days=1)).isoformat()
    dun_devamsiz = 0
    try:
        ak_dir2 = os.path.join("data", "akademik")
        try:
            from utils.tenant import get_data_path
            ak_dir2 = get_data_path("akademik")
        except Exception:
            pass
        attendance = _load_json_safe(os.path.join(ak_dir2, "attendance.json"))
        dun_devamsiz = sum(1 for a in attendance if a.get("tarih", "") == dun)
    except Exception:
        pass

    # 5. Şikayet/Öneri (son 24 saat)
    sikayet_sayi = 0
    try:
        sikayetler = _load_json_safe(os.path.join(td, "kim01_sikayet_oneri.json"))
        yirmi_dort_saat = (bugun - timedelta(days=1)).isoformat()
        sikayet_sayi = sum(1 for s in sikayetler if (s.get("created_at", "") or "")[:10] >= yirmi_dort_saat)
    except Exception:
        pass

    # 6. Doğum günü
    dogum_gunu = []
    try:
        students = _load_json_safe(os.path.join(ak_dir if 'ak_dir' in dir() else "data/akademik", "students.json"))
        for s in students:
            dg = s.get("dogum_tarihi", "")
            if dg and len(dg) >= 10:
                try:
                    if dg[5:10] == bugun_str[5:10]:
                        dogum_gunu.append(f"{s.get('ad', '')} {s.get('soyad', '')} ({s.get('sinif', '')})")
                except Exception:
                    pass
    except Exception:
        pass

    # 7. Geciken iadeler
    geciken_iade = 0
    try:
        from models.kutuphane import KutuphaneDataStore
        kut = KutuphaneDataStore(os.path.join(td, "kutuphane"))
        odunc = kut.load_list("odunc_islemleri") if hasattr(kut, "load_list") else []
        geciken_iade = sum(1 for o in odunc if o.get("durum") == "Odunc" and (o.get("iade_tarihi", "") or "") < bugun_str)
    except Exception:
        pass

    # 8. Bugünkü nöbet
    nobet_sayi = 0
    nobet_isimler = []
    try:
        ak_dir3 = os.path.join("data", "akademik")
        try:
            from utils.tenant import get_data_path
            ak_dir3 = get_data_path("akademik")
        except Exception:
            pass
        nobet_kayitlar = _load_json_safe(os.path.join(ak_dir3, "nobet_kayitlar.json"))
        bugun_nobet = [n for n in nobet_kayitlar if n.get("tarih", "") == bugun_str]
        nobet_sayi = len(bugun_nobet)
        nobet_isimler = [n.get("ogretmen_adi", "?") for n in bugun_nobet[:4]]
    except Exception:
        pass

    # 9. Açık destek talebi
    destek_acik = 0
    try:
        from models.destek_hizmetleri import DestekDataStore
        dst = DestekDataStore(os.path.join(td, "destek"))
        tickets = dst.load_list("tickets") if hasattr(dst, "load_list") else []
        destek_acik = sum(1 for t in tickets if t.get("durum") not in ("Kapandi", "Tamamlandi"))
    except Exception:
        pass

    # 10. Bugünkü yemek menüsü
    bugun_menu = ""
    try:
        menuler = _load_json_safe(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
        if not menuler:
            menuler = _load_json_safe(os.path.join(ak_dir if 'ak_dir' in dir() else "data/akademik", "yemek_menusu.json"))
        menu_obj = next((m for m in menuler if m.get("tarih", "") == bugun_str), None)
        if menu_obj:
            bugun_menu = menu_obj.get("ogle", menu_obj.get("ana_yemek", menu_obj.get("menu", "")))
    except Exception:
        pass

    # 11. Kayıt pipeline — aktif aday
    kayit_aktif = 0
    kayit_bugun = 0
    try:
        from models.kayit_modulu import get_kayit_store
        k_store = get_kayit_store()
        k_adaylar = k_store.load_all()
        kayit_aktif = sum(1 for a in k_adaylar if a.aktif)
        kayit_bugun = sum(1 for a in k_adaylar if a.olusturma_tarihi[:10] == bugun_str)
    except Exception:
        pass

    # 12. Aktif öğrenci sayısı
    aktif_ogrenci = 0
    try:
        students_all = _load_json_safe(os.path.join(ak_dir if 'ak_dir' in dir() else "data/akademik", "students.json"))
        aktif_ogrenci = sum(1 for s in students_all if s.get("durum", "aktif") == "aktif")
    except Exception:
        pass

    # 13. Günün sözü
    _GUNUN_SOZLERI = [
        "Egitim, gelecege yapilan en buyuk yatirimdir. — Nelson Mandela",
        "Bir cocuga ogrettiginiz en onemli sey, merak etmeyi ogretmektir.",
        "Basari, hazirlik ile firsatin bulusmasidir.",
        "Her gun yeni bir baslangictir.",
        "Ogretmenlik, gelecegi sekillendiren en soylu meslektir.",
        "Kucuk adimlar, buyuk degisimler yaratir.",
        "Bilgi paylastikca coğalir.",
    ]
    gunun_sozu = _GUNUN_SOZLERI[bugun.toordinal() % len(_GUNUN_SOZLERI)]

    # 13b. Akademik Takvim — bugünün etkinlikleri
    takvim_etkinlikler = []
    try:
        from views.academic_calendar import load_calendar_data
        cal_data = load_calendar_data()
        cal_events = cal_data.get("events", [])
        for e in cal_events:
            e_tarih = (e.get("date", e.get("tarih", "")) or "")[:10]
            e_bitis = (e.get("end_date", e.get("bitis_tarihi", "")) or "")[:10]
            # Tek gunluk veya aralik icindeyse
            if e_tarih == bugun_str or (e_bitis and e_tarih <= bugun_str <= e_bitis):
                takvim_etkinlikler.append({
                    "baslik": e.get("title", e.get("baslik", "")),
                    "tur": e.get("type", e.get("tur", "")),
                    "kademe": e.get("kademe", ""),
                    "konum": e.get("location", e.get("konum", "")),
                })
    except Exception:
        pass

    # 14. Su anki ders saati
    aktif_ders = _aktif_ders_saati()
    ders_durumu = ""
    if bugun.weekday() >= 5:
        ders_durumu = "Hafta sonu"
    elif aktif_ders > 0:
        ders_durumu = f"{aktif_ders}. Ders devam ediyor"
    else:
        simdi_dk = _saat_to_dk(datetime.now().strftime("%H:%M"))
        if simdi_dk < _saat_to_dk("08:30"):
            ders_durumu = "Okul henuz acilmadi"
        elif simdi_dk > _saat_to_dk("15:40"):
            ders_durumu = "Dersler bitti"
        else:
            ders_durumu = "Teneffus / Ara"

    # 15. Dunun ozeti
    dun_str = (bugun - timedelta(days=1)).isoformat()
    dun_gorev_toplam = 0
    dun_gerceklesen = 0
    dun_en_aktif = ""
    try:
        dun_raporlar = store.find_by_field("raporlar", "tarih", dun_str) if hasattr(store, "find_by_field") else []
        if dun_raporlar:
            dun_rapor = dun_raporlar[-1] if isinstance(dun_raporlar[-1], dict) else dun_raporlar[-1].to_dict()
            dun_gorev_toplam = dun_rapor.get("planlanan_sayi", 0)
            dun_gerceklesen = dun_rapor.get("gerceklesen_sayi", 0)
            # En aktif modul
            modul_ozet = dun_rapor.get("modul_ozet", {})
            if modul_ozet:
                en_aktif_m = max(modul_ozet.items(), key=lambda x: x[1].get("planlanan", 0) if isinstance(x[1], dict) else 0)
                dun_en_aktif = en_aktif_m[0]
    except Exception:
        pass
    dun_oran = round(dun_gerceklesen / max(dun_gorev_toplam, 1) * 100) if dun_gorev_toplam > 0 else 0

    # 16. Yaklasan 3 gun
    yaklasan_gunler = []
    for i in range(1, 4):
        gun_tarih = bugun + timedelta(days=i)
        gun_str_y = gun_tarih.isoformat()
        gun_adi_y = _GUN_ADLARI.get(gun_tarih.weekday(), "")
        if gun_tarih.weekday() < 5:  # hafta ici
            gt_y = GunlukToplayici(gun_str_y)
            gorevler_y = gt_y.topla()
            yaklasan_gunler.append({
                "tarih": f"{gun_tarih.day:02d}.{gun_tarih.month:02d}",
                "gun": gun_adi_y,
                "sayi": len(gorevler_y),
                "kritik": sum(1 for g in gorevler_y if g.oncelik in ("Kritik", "Yuksek")),
            })
        else:
            yaklasan_gunler.append({"tarih": f"{gun_tarih.day:02d}.{gun_tarih.month:02d}", "gun": gun_adi_y, "sayi": 0, "kritik": 0})

    # ── BRİFİNG KARTI (küçük parçalara bölünmüş) ──
    # Hero üst bant
    aktif_modul = len(set(g.kaynak_modul for g in gorevler))
    st.markdown(f"""<div style="background:linear-gradient(135deg,#0B0F19 0%,#1a237e 100%);
        border:2px solid #c9a84c;border-radius:20px;padding:24px 28px;margin:0 0 14px 0;
        box-shadow:0 8px 32px rgba(201,168,76,0.2);position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;height:3px;
                background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <div>
            <div style="font-size:10px;color:#c9a84c;letter-spacing:3px;text-transform:uppercase;">Sabah Brifing</div>
            <div style="font-size:26px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">Bugün Okulda Ne Var?</div>
            <div style="font-size:12px;color:#e8d48b;margin-top:4px;">📅 {tarih_pretty} · {aktif_ogrenci} öğrenci · {aktif_modul} modül aktif</div>
        </div>
        <div style="text-align:center;background:rgba(201,168,76,0.12);border:1px solid #c9a84c;border-radius:14px;padding:12px 20px;">
            <div style="font-size:40px;font-weight:900;color:#c9a84c;line-height:1;">{len(gorevler)}</div>
            <div style="font-size:9px;color:#e8d48b;letter-spacing:1.5px;text-transform:uppercase;">Toplam İş</div>
        </div>
    </div>
    <div style="font-size:11px;color:#e8d48b;font-style:italic;opacity:0.7;text-align:center;
                padding-top:8px;border-top:1px solid rgba(201,168,76,0.15);">
        💡 {gunun_sozu}</div>
    <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
                background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
    </div>""", unsafe_allow_html=True)

    # 1. Satir: Ana sayaclar (Toplanti/Sinav/Etkinlik/Randevu)
    styled_stat_row([
        ("Toplantı", str(toplanti_sayi), "#3b82f6", "🤝"),
        ("Sınav", str(sinav_sayi), "#8b5cf6", "📝"),
        ("Etkinlik", str(etkinlik_sayi), "#ea580c", "🎭"),
        ("Randevu", str(randevu_sayi), "#10b981", "📅"),
    ])

    # 2. Satir: Personel + Ogrenci durumu
    styled_stat_row([
        ("İzinli Personel", str(len(izinli_personel)), "#f59e0b" if izinli_personel else "#10b981", "👥"),
        ("İzinli Öğretmen", str(len(izinli_ogretmen)), "#f59e0b" if izinli_ogretmen else "#10b981", "🏫"),
        ("Nöbetçi", str(nobet_sayi), "#0891b2", "🛡️"),
        ("Dün Devamsız", str(dun_devamsiz), "#ef4444" if dun_devamsiz > 10 else "#10b981", "📋"),
    ])

    # 3. Satir: Hizmetler + Operasyon
    styled_stat_row([
        ("Şikayet/Öneri", str(sikayet_sayi), "#ef4444" if sikayet_sayi > 3 else "#10b981", "📝"),
        ("Doğum Günü", str(len(dogum_gunu)), "#c9a84c" if dogum_gunu else "#64748b", "🎂"),
        ("Geciken İade", str(geciken_iade), "#ef4444" if geciken_iade > 5 else "#10b981", "📚"),
        ("Açık Destek", str(destek_acik), "#f97316" if destek_acik > 5 else "#10b981", "🔧"),
    ])

    # 4. Satir: Kayit + Pipeline
    styled_stat_row([
        ("Aktif Aday", str(kayit_aktif), "#7c3aed", "🎯"),
        ("Bugün Yeni Aday", str(kayit_bugun), "#2563eb", "➕"),
        ("Aktif Öğrenci", str(aktif_ogrenci), "#059669", "🎓"),
    ])

    # ── Nöbetçi isimleri ──
    # ── Akademik Takvim Etkinlikleri ──
    if takvim_etkinlikler:
        etk_html = ""
        for te in takvim_etkinlikler[:5]:
            etk_html += (f'<div style="display:flex;gap:6px;align-items:center;padding:2px 0;">'
                          f'<span style="width:6px;height:6px;border-radius:50%;background:#6366f1;flex-shrink:0;"></span>'
                          f'<span style="font-size:11px;color:#e2e8f0;font-weight:600;">{te["baslik"]}</span>'
                          f'<span style="font-size:9px;color:#94a3b8;">({te["tur"]})</span></div>')
        kalan_txt = f' <span style="font-size:9px;color:#64748b;">+{len(takvim_etkinlikler) - 5} daha</span>' if len(takvim_etkinlikler) > 5 else ""
        st.markdown(
            f'<div style="background:#6366f110;border:1px solid #6366f130;border-radius:10px;'
            f'padding:10px 14px;margin:4px 0;">'
            f'<div style="font-size:10px;color:#a5b4fc;font-weight:700;margin-bottom:4px;">'
            f'📅 Bugünün Akademik Takvim Etkinlikleri ({len(takvim_etkinlikler)})</div>'
            f'{etk_html}{kalan_txt}</div>', unsafe_allow_html=True)

    if nobet_isimler:
        st.markdown(
            f'<div style="background:#0c4a6e20;border:1px solid #0891b230;border-radius:10px;'
            f'padding:8px 14px;margin:4px 0;font-size:11px;color:#67e8f9;">'
            f'🛡️ Bugünkü Nöbetçiler: <b>{", ".join(nobet_isimler)}</b>'
            f'{"..." if nobet_sayi > 4 else ""}</div>', unsafe_allow_html=True)

    # ── Doğum günü isimleri ──
    if dogum_gunu:
        st.markdown(
            f'<div style="background:#c9a84c10;border:1px solid #c9a84c30;border-radius:10px;'
            f'padding:8px 14px;margin:4px 0;font-size:11px;color:#e8d48b;">'
            f'🎂 Doğum Günü: <b>{", ".join(dogum_gunu[:3])}</b>'
            f'{"..." if len(dogum_gunu) > 3 else ""} — Kutlama mesajı gönderin!</div>', unsafe_allow_html=True)

    # ── Bugünün menüsü ──
    if bugun_menu:
        st.markdown(
            f'<div style="background:#f59e0b10;border:1px solid #f59e0b30;border-radius:10px;'
            f'padding:8px 14px;margin:4px 0;font-size:11px;color:#fbbf24;">'
            f'🍽️ Bugünün Menüsü: <b>{bugun_menu[:80]}</b></div>', unsafe_allow_html=True)

    # ── İzinli isimleri ──
    if izinli_personel:
        st.markdown(
            f'<div style="background:#f59e0b10;border:1px solid #f59e0b30;border-radius:10px;'
            f'padding:8px 14px;margin:4px 0;font-size:11px;color:#fbbf24;">'
            f'👥 İzinli: <b>{", ".join(izinli_personel[:5])}</b>'
            f'{"..." if len(izinli_personel) > 5 else ""}</div>', unsafe_allow_html=True)

    # ── Kritik uyarı ──
    if kritik_sayi > 0:
        styled_info_banner(
            f"{kritik_sayi} kritik/yüksek öncelikli iş bugün yapılmalı!",
            banner_type="error", icon="🚨")

    # ── FİKİR 1: Şu anki ders durumu ──
    ders_renk = "#10b981" if aktif_ders > 0 else "#f59e0b" if ders_durumu == "Teneffus / Ara" else "#64748b"
    ders_ikon = "🟢" if aktif_ders > 0 else "🟡" if "Teneffus" in ders_durumu else "⚪"
    st.markdown(
        f'<div style="background:#0f172a;border:1px solid {ders_renk}30;border-left:4px solid {ders_renk};'
        f'border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:12px;color:#e2e8f0;font-weight:700;">'
        f'{ders_ikon} {ders_durumu}</span>'
        f'<span style="font-size:24px;font-weight:900;color:{ders_renk};font-family:monospace;">'
        f'{datetime.now().strftime("%H:%M")}</span></div></div>', unsafe_allow_html=True)

    # ── FİKİR 2: Dünün özeti ──
    if dun_gorev_toplam > 0:
        dun_renk = "#10b981" if dun_oran >= 70 else "#f59e0b" if dun_oran >= 40 else "#ef4444"
        st.markdown(
            f'<div style="background:#0f172a;border:1px solid {dun_renk}30;border-radius:10px;'
            f'padding:10px 14px;margin:6px 0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<div>'
            f'<span style="font-size:11px;color:#94a3b8;">Dünün Özeti:</span>'
            f'<span style="font-size:12px;color:#e2e8f0;font-weight:700;margin-left:6px;">'
            f'{dun_gerceklesen}/{dun_gorev_toplam} iş tamamlandı</span>'
            f'{f" · En aktif: {dun_en_aktif}" if dun_en_aktif else ""}'
            f'</div>'
            f'<span style="background:{dun_renk}20;color:{dun_renk};padding:3px 10px;border-radius:8px;'
            f'font-size:12px;font-weight:800;">%{dun_oran}</span></div></div>', unsafe_allow_html=True)

    # ── FİKİR 3: Yaklaşan 3 gün mini takvim ──
    if yaklasan_gunler:
        yaklasan_html = ""
        for yg in yaklasan_gunler:
            y_sayi = yg.get("sayi", 0)
            y_kritik = yg.get("kritik", 0)
            y_gun = yg.get("gun", "")
            y_tarih = yg.get("tarih", "")
            y_renk = "#ef4444" if y_kritik > 0 else "#3b82f6" if y_sayi > 0 else "#334155"
            kritik_txt = f" ({y_kritik} kritik)" if y_kritik > 0 else ""
            yaklasan_html += (
                f'<div style="flex:1;background:#0f172a;border:1px solid {y_renk}30;border-radius:10px;'
                f'padding:10px;text-align:center;">'
                f'<div style="font-size:10px;color:#94a3b8;">{y_gun}</div>'
                f'<div style="font-size:11px;color:#e2e8f0;font-weight:700;">{y_tarih}</div>'
                f'<div style="font-size:20px;font-weight:900;color:{y_renk};margin:4px 0;">{y_sayi}</div>'
                f'<div style="font-size:8px;color:#64748b;">is{kritik_txt}</div></div>')

        st.markdown(
            f'<div style="margin:6px 0;">'
            f'<div style="font-size:10px;color:#94a3b8;margin-bottom:4px;">📅 Yaklaşan 3 Gün</div>'
            f'<div style="display:flex;gap:8px;">{yaklasan_html}</div></div>', unsafe_allow_html=True)

    # ── Yıllık / Aylık Çalışma Planı PDF ──
    col_pdf1, col_pdf2 = st.columns(2)
    with col_pdf1:
        if st.button("📑 Aylık Plan PDF", key="sb_aylik_pdf", use_container_width=True):
            try:
                from views.academic_calendar import load_calendar_data
                from views._akt_yillik_plan import _generate_yillik_plan_pdf
                cal_data = load_calendar_data()
                cal_events = cal_data.get("events", [])
                b = bugun
                yb = b.year if b.month >= 9 else b.year - 1
                ey = f"{yb}-{yb + 1}"
                ey_bas = f"{yb}-09-01"
                ey_bit = f"{yb + 1}-08-31"
                yil_evts = [e for e in cal_events if ey_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= ey_bit]
                pdf = _generate_yillik_plan_pdf(yil_evts, ey, yb, yb + 1, cal_data.get("semesters", []), b.month)
                if pdf:
                    ay_adi_map = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran",
                                   7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}
                    st.download_button(f"📥 {ay_adi_map.get(b.month, '')} PDF Indir", pdf,
                                       file_name=f"aylik_plan_{ay_adi_map.get(b.month, '')}_{b.year}.pdf",
                                       mime="application/pdf", use_container_width=True, key="sb_aylik_dl")
            except Exception as _epdf:
                st.error(f"PDF hatasi: {_epdf}")

    with col_pdf2:
        if st.button("📑 Yıllık Plan PDF", key="sb_yillik_pdf", use_container_width=True):
            try:
                from views.academic_calendar import load_calendar_data
                from views._akt_yillik_plan import _generate_yillik_plan_pdf
                cal_data = load_calendar_data()
                cal_events = cal_data.get("events", [])
                b = bugun
                yb = b.year if b.month >= 9 else b.year - 1
                ey = f"{yb}-{yb + 1}"
                ey_bas = f"{yb}-09-01"
                ey_bit = f"{yb + 1}-08-31"
                yil_evts = [e for e in cal_events if ey_bas <= (e.get("date", e.get("tarih", "")) or "")[:10] <= ey_bit]
                pdf = _generate_yillik_plan_pdf(yil_evts, ey, yb, yb + 1, cal_data.get("semesters", []), None)
                if pdf:
                    st.download_button(f"📥 {ey} Yıllık PDF Indir", pdf,
                                       file_name=f"yillik_calisma_plani_{ey}.pdf",
                                       mime="application/pdf", use_container_width=True, key="sb_yillik_dl")
            except Exception as _epdf:
                st.error(f"PDF hatasi: {_epdf}")


# ============================================================
# 5. HIZLI İŞLEM PANELİ (QUICK ACTIONS)
# ============================================================

def render_quick_actions(store: YTEDataStore):
    """Yöneticinin en sık yaptığı işlemler — modül değiştirmeden tek tıkla."""

    styled_section("Hızlı İşlemler", "#c9a84c")

    # ── QUICK ACTION GRID ──
    actions = [
        ("📢", "Hızlı Duyuru", "duyuru", "#2563eb"),
        ("📅", "Toplantı Planla", "toplanti", "#7c3aed"),
        ("📄", "Günlük PDF", "pdf", "#059669"),
        ("📝", "Hızlı Not", "not", "#f59e0b"),
        ("📞", "Arama Notu", "arama", "#ea580c"),
        ("📊", "Anlık Rapor", "rapor", "#0891b2"),
        ("🚨", "Acil Duyuru", "acil", "#ef4444"),
        ("✅", "Görev Ekle", "gorev", "#10b981"),
    ]

    # Grid butonları
    cols = st.columns(4)
    for idx, (ikon, label, key, renk) in enumerate(actions):
        with cols[idx % 4]:
            if st.button(f"{ikon} {label}", key=f"qa_{key}", use_container_width=True):
                st.session_state["_qa_active"] = key if st.session_state.get("_qa_active") != key else None
                st.rerun()

    active = st.session_state.get("_qa_active")

    # ── AKTİF İŞLEM FORMLARI ──
    if active == "duyuru":
        with st.expander("📢 Hızlı Duyuru Gönder", expanded=True):
            duyuru_baslik = st.text_input("Başlık", key="qa_duyuru_baslik", placeholder="Duyuru başlığı...")
            duyuru_icerik = st.text_area("İçerik", key="qa_duyuru_icerik", height=100)
            duyuru_hedef = st.multiselect("Hedef Kitle",
                ["Tüm Personel", "Öğretmenler", "Veliler", "Öğrenciler", "İdare"], key="qa_duyuru_hedef")
            if st.button("Gönder", key="qa_duyuru_gonder", type="primary"):
                if duyuru_baslik:
                    td = _tenant_dir()
                    duyurular = _load_json_safe(os.path.join(td, "akademik", "duyurular.json"))
                    duyurular.append({
                        "id": f"dy_{uuid.uuid4().hex[:8]}",
                        "baslik": duyuru_baslik,
                        "icerik": duyuru_icerik,
                        "hedef": duyuru_hedef,
                        "gonderen": "Yönetim",
                        "tarih": date.today().isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    path = os.path.join(td, "akademik", "duyurular.json")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(duyurular, f, ensure_ascii=False, indent=2)
                    st.success(f"Duyuru gönderildi: {duyuru_baslik}")
                    st.session_state["_qa_active"] = None
                    st.rerun()

    elif active == "toplanti":
        with st.expander("📅 Hızlı Toplantı Planla", expanded=True):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                t_baslik = st.text_input("Toplantı Konusu", key="qa_top_baslik")
                t_tarih = st.date_input("Tarih", key="qa_top_tarih")
            with t_col2:
                t_saat = st.time_input("Saat", key="qa_top_saat")
                t_konum = st.text_input("Konum", key="qa_top_konum", placeholder="Toplantı salonu")
            if st.button("Planla", key="qa_top_kaydet", type="primary"):
                if t_baslik:
                    try:
                        from models.toplanti_kurullar import ToplantiDataStore
                        top_store = ToplantiDataStore(os.path.join(_tenant_dir(), "toplanti"))
                        top_store.add_item("meetings", {
                            "id": f"mtg_{uuid.uuid4().hex[:8]}",
                            "baslik": t_baslik,
                            "tarih": t_tarih.isoformat(),
                            "saat_baslangic": t_saat.strftime("%H:%M"),
                            "lokasyon": t_konum,
                            "durum": "TASLAK",
                            "organizator": "Yönetim",
                            "created_at": datetime.now().isoformat(),
                        })
                        st.success(f"Toplantı planlandı: {t_baslik} — {t_tarih}")
                        st.session_state["_qa_active"] = None
                    except Exception as e:
                        st.error(f"Hata: {e}")

    elif active == "pdf":
        with st.expander("📄 Günlük PDF İndir", expanded=True):
            bugun = date.today().isoformat()
            gt = GunlukToplayici(bugun)
            gorevler = gt.topla()
            if gorevler:
                rapor_engine = RaporUreticisi(store)
                pdf = rapor_engine.gun_basi_pdf_olustur(bugun, gorevler)
                if pdf:
                    st.download_button("📥 Gün Başı PDF İndir", pdf,
                                       file_name=f"gun_basi_{bugun}.pdf",
                                       mime="application/pdf", use_container_width=True)
            else:
                st.info("Bugün için görev bulunamadı.")

    elif active == "not":
        with st.expander("📝 Hızlı Not", expanded=True):
            not_icerik = st.text_area("Not yazın...", key="qa_not_icerik", height=80)
            if st.button("Kaydet", key="qa_not_kaydet", type="primary"):
                if not_icerik.strip():
                    notlar = store.load_list("ajanda_notlari")
                    notlar.append({
                        "id": f"an_{uuid.uuid4().hex[:8]}",
                        "tarih": date.today().isoformat(),
                        "saat": datetime.now().strftime("%H:%M"),
                        "icerik": not_icerik.strip(),
                        "tur": "not",
                        "kategori": "Hizli Not",
                        "oncelik": "Normal",
                        "tamamlandi": False,
                    })
                    store.save_list("ajanda_notlari", notlar)
                    st.success("Not kaydedildi!")
                    st.session_state["_qa_active"] = None
                    st.rerun()

    elif active == "arama":
        with st.expander("📞 Hızlı Arama Notu", expanded=True):
            ar_kisi = st.text_input("Kimi aradınız?", key="qa_ar_kisi")
            ar_sonuc = st.selectbox("Sonuç", ["Görüşme yapıldı", "Ulaşılamadı", "Mesaj bırakıldı",
                                                "Randevu alındı", "Bilgi verildi"], key="qa_ar_sonuc")
            ar_not = st.text_area("Not", key="qa_ar_not", height=60)
            if st.button("Kaydet", key="qa_ar_kaydet", type="primary"):
                if ar_kisi:
                    notlar = store.load_list("ajanda_notlari")
                    notlar.append({
                        "id": f"an_{uuid.uuid4().hex[:8]}",
                        "tarih": date.today().isoformat(),
                        "saat": datetime.now().strftime("%H:%M"),
                        "icerik": f"📞 {ar_kisi}: {ar_sonuc} — {ar_not}",
                        "tur": "not",
                        "kategori": "Arama",
                        "oncelik": "Normal",
                        "tamamlandi": False,
                    })
                    store.save_list("ajanda_notlari", notlar)
                    st.success(f"Arama notu kaydedildi: {ar_kisi}")
                    st.session_state["_qa_active"] = None
                    st.rerun()

    elif active == "rapor":
        with st.expander("📊 Anlık Rapor Oluştur", expanded=True):
            bugun = date.today().isoformat()
            gt = GunlukToplayici(bugun)
            gorevler = gt.topla()
            rapor_engine = RaporUreticisi(store)
            rapor = rapor_engine.gunluk_rapor_olustur(bugun, gorevler, "gun_sonu")
            store.upsert("raporlar", rapor)
            st.success(f"Rapor oluşturuldu! Görev: {rapor.planlanan_sayi} · Gerçekleşme: %{rapor.gerceklesme_orani}")
            pdf = rapor_engine.gun_sonu_pdf_olustur(rapor, gorevler)
            if pdf:
                st.download_button("📥 PDF İndir", pdf, file_name=f"rapor_{bugun}.pdf",
                                   mime="application/pdf", use_container_width=True)

    elif active == "acil":
        with st.expander("🚨 Acil Duyuru", expanded=True):
            acil_mesaj = st.text_area("Acil mesaj", key="qa_acil_mesaj", height=80,
                                       placeholder="Tüm personele gönderilecek acil duyuru...")
            if st.button("GÖNDER", key="qa_acil_gonder", type="primary"):
                if acil_mesaj:
                    td = _tenant_dir()
                    duyurular = _load_json_safe(os.path.join(td, "akademik", "duyurular.json"))
                    duyurular.append({
                        "id": f"dy_{uuid.uuid4().hex[:8]}",
                        "baslik": "🚨 ACİL DUYURU",
                        "icerik": acil_mesaj,
                        "hedef": ["Tüm Personel", "Öğretmenler", "İdare"],
                        "gonderen": "Yönetim (Acil)",
                        "tarih": date.today().isoformat(),
                        "created_at": datetime.now().isoformat(),
                        "oncelik": "Acil",
                    })
                    path = os.path.join(td, "akademik", "duyurular.json")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(duyurular, f, ensure_ascii=False, indent=2)
                    st.success("🚨 Acil duyuru gönderildi!")
                    st.session_state["_qa_active"] = None
                    st.rerun()

    elif active == "gorev":
        with st.expander("✅ Hızlı Görev Ekle", expanded=True):
            g_icerik = st.text_input("Görev", key="qa_gorev_icerik", placeholder="Yapılacak iş...")
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                g_oncelik = st.selectbox("Öncelik", ["Normal", "Yüksek", "Düşük"], key="qa_gorev_onc")
            with g_col2:
                g_kat = st.selectbox("Kategori", ["Genel", "Toplantı", "Veli", "Personel", "Acil"], key="qa_gorev_kat")
            if st.button("Ekle", key="qa_gorev_ekle", type="primary"):
                if g_icerik:
                    notlar = store.load_list("ajanda_notlari")
                    notlar.append({
                        "id": f"an_{uuid.uuid4().hex[:8]}",
                        "tarih": date.today().isoformat(),
                        "saat": datetime.now().strftime("%H:%M"),
                        "icerik": g_icerik.strip(),
                        "tur": "gorev",
                        "kategori": g_kat,
                        "oncelik": g_oncelik,
                        "tamamlandi": False,
                    })
                    store.save_list("ajanda_notlari", notlar)
                    st.success(f"Görev eklendi: {g_icerik}")
                    st.session_state["_qa_active"] = None
                    st.rerun()


# ============================================================
# 6. HAFTALIK TAKVİM GÖRÜNÜMÜ (TÜM MODÜLLER BİRLEŞİK)
# ============================================================

# Görev tipine göre renk
_TAKVIM_TIP_RENK = {
    "toplanti": ("#3b82f6", "🤝"),
    "aksiyon": ("#3b82f6", "🤝"),
    "sinav": ("#8b5cf6", "📝"),
    "online_sinav": ("#8b5cf6", "📝"),
    "etkinlik": ("#ea580c", "🎭"),
    "kulup_faaliyet": ("#ea580c", "🎭"),
    "randevu": ("#10b981", "📅"),
    "kayit_randevu": ("#10b981", "📅"),
    "veli_gorusme": ("#10b981", "📅"),
    "kayit_gorusme": ("#10b981", "📅"),
    "gorusme": ("#7c3aed", "🧠"),
    "aile_gorusme": ("#7c3aed", "🧠"),
    "nobet": ("#64748b", "🛡️"),
    "ogretmen_izin": ("#f59e0b", "🏖️"),
    "personel_izin": ("#f59e0b", "🏖️"),
    "mulakat": ("#0891b2", "👥"),
    "ilac": ("#dc2626", "💊"),
    "seminer": ("#059669", "🎓"),
    "tatbikat": ("#b91c1c", "🚒"),
    "kocluk_gorusme": ("#ea580c", "🏅"),
    "yd_sinav": ("#0369a1", "🌐"),
    "cefr_sinav": ("#6d28d9", "🎓"),
}


def render_haftalik_takvim(store: YTEDataStore):
    """Pazartesi-Cuma 5 sütunlu takvim — tüm modüllerden birleşik."""

    styled_section("Haftalık Takvim", "#2563eb")
    styled_info_banner(
        "Tüm modüllerden toplanan bu haftanın etkinlikleri. "
        "Toplantı, sınav, etkinlik, randevu — hepsi tek takvimde.",
        banner_type="info", icon="📅")

    bugun = date.today()

    # Hafta seçimi
    hafta_sec = st.radio("Hafta", ["Bu Hafta", "Gelecek Hafta", "Geçen Hafta"],
                          horizontal=True, key="yte_takvim_hafta")
    if hafta_sec == "Gelecek Hafta":
        hafta_bas = bugun - timedelta(days=bugun.weekday()) + timedelta(weeks=1)
    elif hafta_sec == "Geçen Hafta":
        hafta_bas = bugun - timedelta(days=bugun.weekday()) - timedelta(weeks=1)
    else:
        hafta_bas = bugun - timedelta(days=bugun.weekday())

    # 5 günün verilerini topla
    gun_verileri: list[tuple[date, str, list[PlanlanmisGorev]]] = []
    for i in range(5):
        gun = hafta_bas + timedelta(days=i)
        gun_str = gun.isoformat()
        gun_adi = _GUN_ADLARI.get(gun.weekday(), "")
        gt = GunlukToplayici(gun_str)
        gorevler = gt.topla()
        gun_verileri.append((gun, gun_adi, gorevler))

    # ── TAKVİM GRID ──
    cols = st.columns(5)
    for idx, (gun, gun_adi, gorevler) in enumerate(gun_verileri):
        gun_str = gun.isoformat()
        is_bugun = gun == bugun
        header_bg = "linear-gradient(135deg,#c9a84c,#e8d48b)" if is_bugun else "#1e293b"
        header_color = "#1a1a2e" if is_bugun else "#e2e8f0"
        border = "2px solid #c9a84c" if is_bugun else "1px solid #334155"

        with cols[idx]:
            # Gün başlığı
            st.markdown(f"""
            <div style="background:{header_bg};border-radius:10px 10px 0 0;padding:8px;text-align:center;
                        border:{border};border-bottom:none;">
                <div style="font-size:11px;font-weight:800;color:{header_color};">{gun_adi}</div>
                <div style="font-size:14px;font-weight:900;color:{header_color};">{gun.day}</div>
            </div>""", unsafe_allow_html=True)

            # Görev kartları
            if not gorevler:
                st.markdown(f"""
                <div style="background:#0f172a;border:{border};border-top:none;border-radius:0 0 10px 10px;
                            padding:12px 8px;text-align:center;min-height:80px;">
                    <span style="font-size:10px;color:#475569;">Etkinlik yok</span>
                </div>""", unsafe_allow_html=True)
            else:
                kartlar_html = ""
                for g in sorted(gorevler, key=lambda x: x.saat or "99:99")[:8]:
                    tip_info = _TAKVIM_TIP_RENK.get(g.kaynak_tipi, ("#64748b", "📋"))
                    renk = tip_info[0]
                    ikon = tip_info[1]
                    saat = g.saat[:5] if g.saat else ""
                    baslik_kisa = g.baslik[:25] + ("..." if len(g.baslik) > 25 else "")
                    kartlar_html += (
                        f'<div style="background:{renk}12;border-left:3px solid {renk};'
                        f'border-radius:0 6px 6px 0;padding:4px 6px;margin-bottom:3px;">'
                        f'<div style="font-size:8px;color:{renk};font-weight:700;">{saat} {ikon}</div>'
                        f'<div style="font-size:9px;color:#cbd5e1;line-height:1.2;">{baslik_kisa}</div>'
                        f'</div>')

                kalan = len(gorevler) - 8
                if kalan > 0:
                    kartlar_html += f'<div style="font-size:9px;color:#64748b;text-align:center;padding:2px;">+{kalan} daha</div>'

                st.markdown(f"""
                <div style="background:#0f172a;border:{border};border-top:none;border-radius:0 0 10px 10px;
                            padding:6px;min-height:80px;">
                    {kartlar_html}
                </div>""", unsafe_allow_html=True)

    # ── ÖZET STAT ──
    toplam_hafta = sum(len(g) for _, _, g in gun_verileri)
    en_yogun_gun = max(gun_verileri, key=lambda x: len(x[2]))
    tip_sayac = Counter()
    for _, _, gorevler in gun_verileri:
        for g in gorevler:
            tip_sayac[g.kaynak_tipi] += 1

    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;padding:12px 16px;margin-top:12px;">
        <div style="display:flex;justify-content:space-around;text-align:center;flex-wrap:wrap;gap:8px;">
            <div><div style="font-size:20px;font-weight:800;color:#3b82f6;">{toplam_hafta}</div>
                <div style="font-size:9px;color:#64748b;">Toplam İş</div></div>
            <div><div style="font-size:20px;font-weight:800;color:#c9a84c;">{en_yogun_gun[1]}</div>
                <div style="font-size:9px;color:#64748b;">En Yoğun Gün</div></div>
            <div><div style="font-size:20px;font-weight:800;color:#8b5cf6;">{len(tip_sayac)}</div>
                <div style="font-size:9px;color:#64748b;">Farklı Tip</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Renk kodu açıklama
    legend_html = ""
    for tip, (renk, ikon) in list(_TAKVIM_TIP_RENK.items())[:10]:
        legend_html += (f'<span style="background:{renk}15;color:{renk};padding:2px 8px;'
                        f'border-radius:4px;font-size:9px;font-weight:600;margin:2px;">'
                        f'{ikon} {tip.replace("_", " ").title()}</span>')
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:8px;">{legend_html}</div>',
                unsafe_allow_html=True)


# ============================================================
# 7. CANLI OKUL KONTROL MERKEZİ (LIVE CONTROL TOWER)
# ============================================================

_DERS_SAAT_ARALIĞI = {
    1: ("08:30", "09:10"), 2: ("09:20", "10:00"), 3: ("10:10", "10:50"),
    4: ("11:00", "11:40"), 5: ("11:50", "12:30"), 6: ("13:20", "14:00"),
    7: ("14:10", "14:50"), 8: ("15:00", "15:40"),
}


def _saat_to_dk(saat_str: str) -> int:
    """'HH:MM' -> dakika cinsinden."""
    try:
        h, m = saat_str.split(":")
        return int(h) * 60 + int(m)
    except Exception:
        return 0


def _aktif_ders_saati() -> int:
    """Su anki saat diliminde kacinci ders var (0=ders yok)."""
    simdi = _saat_to_dk(datetime.now().strftime("%H:%M"))
    for ders_no, (bas, bit) in _DERS_SAAT_ARALIĞI.items():
        if _saat_to_dk(bas) <= simdi <= _saat_to_dk(bit):
            return ders_no
    return 0


def render_canli_kontrol_merkezi(store: YTEDataStore):
    """Canli okul kontrol kulesi — su an okulda neler oluyor."""
    bugun = date.today()
    bugun_str = bugun.isoformat()
    simdi = datetime.now()
    saat_str = simdi.strftime("%H:%M")
    td = _tenant_dir()

    try:
        gun_adi = _GUN_ADLARI.get(bugun.weekday(), "")
    except Exception:
        gun_adi = ""

    styled_section("Canli Kontrol Merkezi", "#0ea5e9")

    # ── VERİ TOPLAMA ──

    # 1. Ders programi — bugünkü dersler
    bugun_gun_adi = gun_adi
    ak_dir = "data/akademik"
    try:
        from utils.tenant import get_data_path
        ak_dir = get_data_path("akademik")
    except Exception:
        pass

    schedule = _load_json_safe(os.path.join(ak_dir, "schedule.json"))
    bugun_dersler = [s for s in schedule if s.get("gun", "") == bugun_gun_adi]
    aktif_ders = _aktif_ders_saati()

    # Şu an devam eden dersler
    aktif_dersler = [s for s in bugun_dersler if s.get("ders_saati") == aktif_ders] if aktif_ders > 0 else []
    aktif_ogretmenler = set(s.get("ogretmen", "") for s in aktif_dersler if s.get("ogretmen"))
    aktif_siniflar = set(f"{s.get('sinif', '')}-{s.get('sube', '')}" for s in aktif_dersler)

    # Toplam bugünkü benzersiz öğretmenler
    bugun_ogretmenler = set(s.get("ogretmen", "") for s in bugun_dersler if s.get("ogretmen"))
    bos_ogretmenler = bugun_ogretmenler - aktif_ogretmenler if aktif_ders > 0 else set()

    # 2. Yoklama durumu
    attendance = _load_json_safe(os.path.join(ak_dir, "attendance.json"))
    bugun_devamsiz = [a for a in attendance if a.get("tarih", "") == bugun_str]
    devamsiz_ogrenci = len(set(a.get("student_id", "") for a in bugun_devamsiz))

    students = _load_json_safe(os.path.join(ak_dir, "students.json"))
    aktif_ogrenci = sum(1 for s in students if s.get("durum", "aktif") == "aktif")
    gelen_ogrenci = aktif_ogrenci - devamsiz_ogrenci
    doluluk_pct = round(gelen_ogrenci / max(aktif_ogrenci, 1) * 100, 1)

    # 3. Aktif sınavlar
    aktif_sinav = 0
    try:
        ol_exams = _load_json_safe(os.path.join("data", "olcme", "exams.json"))
        aktif_sinav = sum(1 for e in ol_exams if e.get("status") == "active"
                          and (e.get("start_date", "") or "")[:10] <= bugun_str <= (e.get("end_date", "") or bugun_str)[:10])
    except Exception:
        pass

    # 4. Ziyaretçi (bugün randevulu)
    ziyaretci_sayi = 0
    try:
        from models.randevu_ziyaretci import RZYDataStore
        rzy = RZYDataStore(os.path.join(td, "randevu"))
        rnd = rzy.load_list("randevular") if hasattr(rzy, "load_list") else []
        ziyaretci_sayi = sum(1 for r in rnd if r.get("tarih", "") == bugun_str
                             and r.get("durum") not in ("Iptal", "Gelmedi"))
    except Exception:
        pass

    # 5. Revir
    revir_basvuru = 0
    try:
        from models.okul_sagligi import SaglikDataStore
        sag = SaglikDataStore(os.path.join(td, "saglik"))
        ziyaretler = sag.load_list("revir_ziyaretleri") if hasattr(sag, "load_list") else []
        revir_basvuru = sum(1 for z in ziyaretler if (z.get("created_at", "") or "")[:10] == bugun_str)
    except Exception:
        pass

    # 6. Destek açık talep
    destek_acik = 0
    try:
        from models.destek_hizmetleri import DestekDataStore
        dst = DestekDataStore(os.path.join(td, "destek"))
        tickets = dst.load_list("tickets") if hasattr(dst, "load_list") else []
        destek_acik = sum(1 for t in tickets if t.get("durum") not in ("Kapandi", "Tamamlandi"))
    except Exception:
        pass

    # 7. Yemek menüsü
    yemek = ""
    try:
        menu = _load_json_safe(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
        bugun_menu = next((m for m in menu if m.get("tarih", "") == bugun_str), None)
        if bugun_menu:
            yemek = bugun_menu.get("menu", bugun_menu.get("ana_yemek", ""))
    except Exception:
        pass

    # ── KONTROL KULESİ RENDER ──
    # Durum ışığı helper
    def _isik(durum: str) -> str:
        renk = {"yesil": "#10b981", "sari": "#f59e0b", "kirmizi": "#ef4444", "mavi": "#3b82f6"}.get(durum, "#64748b")
        return f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{renk};box-shadow:0 0 6px {renk};"></span>'

    # Ders durumu
    if aktif_ders > 0:
        ders_durum = "yesil"
        ders_txt = f"{aktif_ders}. Ders Devam Ediyor"
        ders_detay = f"{len(aktif_dersler)} sinifta ders var · {len(aktif_ogretmenler)} ogretmen sinifta"
    elif bugun.weekday() >= 5:
        ders_durum = "mavi"
        ders_txt = "Hafta Sonu"
        ders_detay = "Okul kapali"
    else:
        simdi_dk = _saat_to_dk(saat_str)
        if simdi_dk < _saat_to_dk("08:30"):
            ders_durum = "sari"
            ders_txt = "Okul Henuz Acilmadi"
            ders_detay = "Ilk ders 08:30'da"
        elif simdi_dk > _saat_to_dk("15:40"):
            ders_durum = "mavi"
            ders_txt = "Dersler Bitti"
            ders_detay = "Gun sonu"
        else:
            ders_durum = "sari"
            ders_txt = "Teneffus / Ara"
            ders_detay = ""

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0c4a6e 0%,#075985 50%,#0369a1 100%);
                border:2px solid #0ea5e9;border-radius:20px;padding:24px 28px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(14,165,233,0.25);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,#0ea5e9,#38bdf8,#0ea5e9,transparent);"></div>

        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:10px;color:#7dd3fc;letter-spacing:3px;text-transform:uppercase;">
                    SmartCampus AI · Live</div>
                <div style="font-size:26px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;">Kontrol Merkezi</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:28px;font-weight:900;color:#38bdf8;font-family:monospace;">{saat_str}</div>
                <div style="font-size:10px;color:#7dd3fc;">{gun_adi} · {bugun.day:02d}.{bugun.month:02d}.{bugun.year}</div>
            </div>
        </div>

        <!-- ANA DURUM ŞERİDİ -->
        <div style="background:rgba(0,0,0,0.2);border-radius:14px;padding:14px 18px;margin-bottom:14px;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                {_isik(ders_durum)}
                <span style="font-size:16px;font-weight:800;color:#fff;">{ders_txt}</span>
                <span style="font-size:11px;color:#7dd3fc;">{ders_detay}</span>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
                <span style="background:rgba(16,185,129,0.15);color:#6ee7b7;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(aktif_siniflar)} sinif aktif</span>
                <span style="background:rgba(59,130,246,0.15);color:#93c5fd;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(aktif_ogretmenler)} ogretmen sinifta</span>
                <span style="background:rgba(249,115,22,0.15);color:#fdba74;padding:3px 10px;border-radius:6px;font-size:10px;font-weight:700;">
                    {len(bos_ogretmenler)} ogretmen bos</span>
            </div>
        </div>

        <!-- 8 GÖSTERGE GRİD -->
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('yesil' if doluluk_pct >= 90 else 'sari' if doluluk_pct >= 70 else 'kirmizi')}
                <div style="font-size:24px;font-weight:900;color:#fff;margin:4px 0;">{gelen_ogrenci}</div>
                <div style="font-size:9px;color:#7dd3fc;">Ogrenci Geldi</div>
                <div style="font-size:8px;color:#94a3b8;">%{doluluk_pct} doluluk</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('kirmizi' if devamsiz_ogrenci > 20 else 'sari' if devamsiz_ogrenci > 5 else 'yesil')}
                <div style="font-size:24px;font-weight:900;color:#fca5a5;margin:4px 0;">{devamsiz_ogrenci}</div>
                <div style="font-size:9px;color:#7dd3fc;">Devamsiz</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('sari' if aktif_sinav > 0 else 'mavi')}
                <div style="font-size:24px;font-weight:900;color:#c4b5fd;margin:4px 0;">{aktif_sinav}</div>
                <div style="font-size:9px;color:#7dd3fc;">Aktif Sinav</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('sari' if ziyaretci_sayi > 0 else 'yesil')}
                <div style="font-size:24px;font-weight:900;color:#6ee7b7;margin:4px 0;">{ziyaretci_sayi}</div>
                <div style="font-size:9px;color:#7dd3fc;">Ziyaretci</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('kirmizi' if revir_basvuru > 5 else 'sari' if revir_basvuru > 0 else 'yesil')}
                <div style="font-size:24px;font-weight:900;color:#fde68a;margin:4px 0;">{revir_basvuru}</div>
                <div style="font-size:9px;color:#7dd3fc;">Revir Basvuru</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                {_isik('kirmizi' if destek_acik > 10 else 'sari' if destek_acik > 3 else 'yesil')}
                <div style="font-size:24px;font-weight:900;color:#fdba74;margin:4px 0;">{destek_acik}</div>
                <div style="font-size:9px;color:#7dd3fc;">Acik Talep</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                <div style="font-size:14px;margin:4px 0;">🍽️</div>
                <div style="font-size:9px;color:#7dd3fc;">Yemekhane</div>
                <div style="font-size:8px;color:#94a3b8;">{yemek[:30] or 'Menu girilmedi'}</div>
            </div>
            <div style="background:rgba(0,0,0,0.15);border-radius:12px;padding:12px;text-align:center;">
                <div style="font-size:14px;margin:4px 0;">🏫</div>
                <div style="font-size:9px;color:#7dd3fc;">Bugun Ders</div>
                <div style="font-size:8px;color:#94a3b8;">{len(bugun_dersler)} slot</div>
            </div>
        </div>

        <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,transparent,#0ea5e9,#38bdf8,#0ea5e9,transparent);"></div>
    </div>""", unsafe_allow_html=True)

    # ── DERS ÇİZELGESİ MINI (bugünün dersleri saat bazlı) ──
    if bugun_dersler and bugun.weekday() < 5:
        with st.expander("Bugünkü Ders Çizelgesi", expanded=False):
            for saat_no in range(1, 9):
                saat_dersler = [s for s in bugun_dersler if s.get("ders_saati") == saat_no]
                is_aktif = saat_no == aktif_ders
                zaman = _DERS_SAAT_ARALIĞI.get(saat_no, ("", ""))
                border_stl = "border:2px solid #0ea5e9;" if is_aktif else ""
                bg = "#0c4a6e" if is_aktif else "#0f172a"
                sinif_list = ", ".join(f"{s.get('sinif', '')}-{s.get('sube', '')} ({s.get('ders', '')})" for s in saat_dersler[:6])
                kalan = len(saat_dersler) - 6
                st.markdown(f"""
                <div style="background:{bg};border:1px solid #1e293b;{border_stl}border-radius:8px;
                            padding:6px 12px;margin-bottom:4px;display:flex;align-items:center;gap:10px;">
                    <span style="min-width:70px;font-weight:700;color:{'#38bdf8' if is_aktif else '#94a3b8'};font-size:12px;">
                        {saat_no}. Ders</span>
                    <span style="font-size:10px;color:#64748b;min-width:90px;">{zaman[0]}-{zaman[1]}</span>
                    <span style="font-size:10px;font-weight:600;color:#e2e8f0;">{len(saat_dersler)} sinif</span>
                    <span style="font-size:9px;color:#94a3b8;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                        {sinif_list}{f' +{kalan}' if kalan > 0 else ''}</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# 8. AI ÇAPRAZ MODÜL STRATEJİK DANIŞMAN
# ============================================================

def render_ai_capraz_danisman(store: YTEDataStore):
    """AI ile tum 33 modülün verisini çapraz analiz et — insight'lar uret."""

    styled_section("AI Stratejik Danışman", "#7c3aed")
    styled_info_banner(
        "Tüm modüllerin verilerini çapraz analiz ederek hiç kimsenin fark edemeyeceği "
        "pattern'leri ortaya çıkarır. Modüller arası bağlantıları bulur.",
        banner_type="info", icon="🧠")

    # KPI'lari yukle
    _kpi_cache = "yte_modul_kpis"
    if _kpi_cache not in st.session_state:
        with st.spinner("Modül verileri yükleniyor..."):
            st.session_state[_kpi_cache] = ModulOzetleyici().tum_modul_kpi()
    kpis = st.session_state[_kpi_cache]

    # Saglik puani
    genel_puan, alt_puanlar = _hesapla_saglik_puani(kpis)

    # Bugünün verileri
    bugun = date.today().isoformat()
    gt = GunlukToplayici(bugun)
    gorevler = gt.topla()
    modul_sayac = Counter(g.kaynak_modul for g in gorevler)

    # Raporlar (son 7 gun)
    raporlar = store.load_objects("raporlar")
    son_7_gun = [r for r in raporlar if r.tarih >= (date.today() - timedelta(days=7)).isoformat()]
    ort_oran = round(sum(r.gerceklesme_orani for r in son_7_gun) / max(len(son_7_gun), 1), 1) if son_7_gun else 0

    # ── KURAL BAZLI INSIGHT MOTORU (AI olmadan da calısır) ──
    insights: list[dict] = []

    # 1. Dusuk performans modulleri
    for modul, puan in alt_puanlar.items():
        if puan < 40:
            insights.append({
                "seviye": "kritik", "ikon": "🔴",
                "baslik": f"{modul} kritik seviyede ({puan}/100)",
                "detay": f"Bu modülün sağlık puanı çok düşük. Acil müdahale gerekiyor.",
                "oneri": f"{modul} modülündeki açık işleri önceliklendirin ve bu hafta kapatın.",
            })
        elif puan < 55:
            insights.append({
                "seviye": "uyari", "ikon": "🟠",
                "baslik": f"{modul} riskli bölgede ({puan}/100)",
                "detay": f"Performans ortalamanın altında. Trend kötüye gidebilir.",
                "oneri": f"{modul} için haftalık hedefler belirleyin.",
            })

    # 2. Devamsızlık + Not korelasyonu
    ak_devamsiz = kpis.get("Akademik Takip", {}).get("devamsizlik", 0)
    ak_ogrenci = kpis.get("Akademik Takip", {}).get("ogrenci_sayisi", 0)
    if ak_devamsiz > 0 and ak_ogrenci > 0:
        devamsizlik_oran = round(ak_devamsiz / ak_ogrenci * 100, 1)
        if devamsizlik_oran > 15:
            insights.append({
                "seviye": "uyari", "ikon": "📊",
                "baslik": f"Devamsızlık oranı yüksek: %{devamsizlik_oran}",
                "detay": f"{ak_devamsiz} devamsızlık kaydı / {ak_ogrenci} öğrenci. Sektör ortalaması %8-10.",
                "oneri": "Devamsızlığı yüksek sınıfları belirleyip rehberlik görüşmesi planlayın.",
            })

    # 3. Rehberlik yükü
    reh_vaka = kpis.get("Rehberlik", {}).get("acik_vaka", 0)
    if reh_vaka > 15:
        insights.append({
            "seviye": "uyari", "ikon": "🧠",
            "baslik": f"Rehberlik açık vaka sayısı yüksek: {reh_vaka}",
            "detay": "Açık vaka yükü rehberlik ekibini zorlayabilir.",
            "oneri": "Vaka önceliklendirmesi yapın, gerekirse destek personeli görevlendirin.",
        })

    # 4. Bütçe dengesi
    butce = kpis.get("Butce Gelir Gider", {})
    net = butce.get("net", 0) if isinstance(butce.get("net", 0), (int, float)) else 0
    if net < 0:
        insights.append({
            "seviye": "kritik", "ikon": "💰",
            "baslik": f"Bütçe açığı: {abs(net):,.0f} TL",
            "detay": "Giderler geliri aşmış durumda.",
            "oneri": "Gider kalemlerini gözden geçirin, gereksiz harcamaları durdurun.",
        })

    # 5. Destek talep yükü
    destek = kpis.get("Destek Hizmetleri", {})
    destek_acik = destek.get("acik", 0) if isinstance(destek.get("acik", 0), int) else 0
    if destek_acik > 15:
        insights.append({
            "seviye": "uyari", "ikon": "🔧",
            "baslik": f"{destek_acik} açık destek talebi birikmiş",
            "detay": "Tamamlanmamış talepler birikmesi hizmet kalitesini düşürür.",
            "oneri": "Destek ekibine ek kaynak ayırın veya önceliklendirme yapın.",
        })

    # 6. Kayıt modülü
    hit = kpis.get("Halkla Iliskiler", {})
    sozlesme = hit.get("sozlesme", 0) if isinstance(hit.get("sozlesme", 0), int) else 0
    gorusme = hit.get("toplam_gorusme", 0) if isinstance(hit.get("toplam_gorusme", 0), int) else 0
    if gorusme > 20 and sozlesme < 3:
        donusum = round(sozlesme / max(gorusme, 1) * 100, 1)
        insights.append({
            "seviye": "uyari", "ikon": "🎯",
            "baslik": f"Kayıt dönüşüm oranı düşük: %{donusum}",
            "detay": f"{gorusme} görüşme yapılmış ama sadece {sozlesme} sözleşme.",
            "oneri": "Fiyat politikasını ve görüşme sürecini gözden geçirin.",
        })

    # 7. Genel gerceklesme
    if ort_oran > 0 and ort_oran < 60:
        insights.append({
            "seviye": "uyari", "ikon": "📈",
            "baslik": f"Son 7 gün gerçekleşme ortalaması düşük: %{ort_oran}",
            "detay": "Planlanan görevlerin yarıdan fazlası tamamlanamamış.",
            "oneri": "Gerçekçi olmayan planlamayı azaltın veya kaynak artırın.",
        })

    # 8. Boş modüller (veri yok)
    bos_modul = sum(1 for m in ["Egitim Koclugu", "AI Bireysel Egitim", "Kisisel Dil Gelisimi",
                                  "Yabanci Dil", "Sosyal Medya"] if not kpis.get(m))
    if bos_modul >= 3:
        insights.append({
            "seviye": "bilgi", "ikon": "💡",
            "baslik": f"{bos_modul} modülde hiç veri yok",
            "detay": "Kullanılmayan modüller potansiyel değer kaybı.",
            "oneri": "Eğitim Koçluğu ve AI Bireysel Eğitim modüllerini aktif kullanmaya başlayın.",
        })

    # Pozitif insight'lar
    for modul, puan in alt_puanlar.items():
        if puan >= 85:
            insights.append({
                "seviye": "basari", "ikon": "🌟",
                "baslik": f"{modul} mükemmel performans ({puan}/100)",
                "detay": "Bu modül hedeflerin üzerinde çalışıyor.",
                "oneri": "Bu başarıyı diğer modüllere örnek gösterin.",
            })

    # ── RENDER ──
    if not insights:
        st.success("Tebrikler! Şu an tüm modüller normal çalışıyor, kritik bulgu yok.")
        return

    # Ozet sayac
    kritik_c = sum(1 for i in insights if i["seviye"] == "kritik")
    uyari_c = sum(1 for i in insights if i["seviye"] == "uyari")
    bilgi_c = sum(1 for i in insights if i["seviye"] == "bilgi")
    basari_c = sum(1 for i in insights if i["seviye"] == "basari")

    styled_stat_row([
        ("Kritik", str(kritik_c), "#ef4444", "🔴"),
        ("Uyarı", str(uyari_c), "#f97316", "🟠"),
        ("Bilgi", str(bilgi_c), "#3b82f6", "💡"),
        ("Başarı", str(basari_c), "#10b981", "🌟"),
    ])

    # Insight kartlari
    seviye_renk = {"kritik": "#ef4444", "uyari": "#f97316", "bilgi": "#3b82f6", "basari": "#10b981"}
    seviye_bg = {"kritik": "#450a0a", "uyari": "#431407", "bilgi": "#0c1a3d", "basari": "#052e16"}

    for ins in sorted(insights, key=lambda x: {"kritik": 0, "uyari": 1, "bilgi": 2, "basari": 3}[x["seviye"]]):
        renk = seviye_renk.get(ins["seviye"], "#64748b")
        bg = seviye_bg.get(ins["seviye"], "#0f172a")
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <span style="font-size:18px;">{ins['ikon']}</span>
                <span style="font-weight:800;color:#fff;font-size:14px;">{ins['baslik']}</span>
            </div>
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">{ins['detay']}</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:8px 12px;">
                <span style="font-size:11px;color:{renk};font-weight:700;">💡 Öneri:</span>
                <span style="font-size:11px;color:#cbd5e1;"> {ins['oneri']}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── AI İLE DERİN ANALİZ (OpenAI) ──
    st.divider()
    if st.button("🧠 AI ile Derin Çapraz Analiz", key="yte_ai_capraz", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if not client:
                st.warning("OpenAI API anahtarı bulunamadı.")
            else:
                # Tüm verileri AI'a gönder
                veri_ozet = f"""Okul Sağlık Puanı: {genel_puan}/100
Modül Puanları: {', '.join(f'{m}:{p}' for m, p in sorted(alt_puanlar.items(), key=lambda x: x[1])[:10])}
Bugün Görev: {len(gorevler)} (moduller: {dict(modul_sayac.most_common(5))})
Son 7 Gün Ort. Gerçekleşme: %{ort_oran}
KPI Özet: {', '.join(f'{m}: {list(v.values())[:3]}' for m, v in list(kpis.items())[:8])}
Kural Bazlı Bulgular: {len(insights)} (kritik:{kritik_c}, uyari:{uyari_c})"""

                with st.spinner("AI çapraz analiz yapıyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul yönetim danışmanısın. Verilen verileri çapraz analiz et. Modüller arası bağlantıları bul. Kısa, somut, aksiyon odaklı Türkçe öneriler ver. Maddeler halinde yaz."},
                            {"role": "user", "content": f"Aşağıdaki okul verilerini çapraz analiz et ve stratejik öneriler sun:\n\n{veri_ozet}"},
                        ],
                        max_tokens=800, temperature=0.7,
                    )
                    ai_sonuc = resp.choices[0].message.content or ""

                if ai_sonuc:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                border-radius:14px;padding:18px 22px;margin-top:12px;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:8px;">
                            🧠 AI Çapraz Modül Analizi</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">
                            {ai_sonuc.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"AI analiz hatası: {e}")


# ============================================================
# 9. YÖNETİCİ KARŞILAŞTIRMA COCKPİT'İ (FLEXIBLE BI)
# ============================================================

def render_karsilastirma_cockpit(store: YTEDataStore):
    """İstediğin herhangi iki şeyi yan yana karşılaştır."""

    styled_section("Karşılaştırma Cockpit'i", "#f59e0b")
    styled_info_banner(
        "Dönem, sınıf, modül veya hafta bazlı esnek karşılaştırma. "
        "İstediğiniz iki şeyi seçin, sistem otomatik analiz eder.",
        banner_type="info", icon="⚖️")

    karsilastirma_turu = st.selectbox("Karşılaştırma Türü", [
        "📅 Dönem vs Dönem (Bu Ay vs Geçen Ay)",
        "📊 Hafta vs Hafta",
        "📋 Modül vs Modül",
        "🎓 Kademe vs Kademe",
    ], key="yte_kc_tur")

    # ── KPI'lari yukle ──
    _kpi_cache = "yte_modul_kpis"
    if _kpi_cache not in st.session_state:
        with st.spinner("Modül verileri yükleniyor..."):
            st.session_state[_kpi_cache] = ModulOzetleyici().tum_modul_kpi()
    kpis = st.session_state[_kpi_cache]

    raporlar = store.load_objects("raporlar")

    def _donem_metrik(raporlar_list):
        if not raporlar_list:
            return {"plan": 0, "gercek": 0, "iptal": 0, "oran": 0, "gun": 0}
        return {
            "plan": sum(r.planlanan_sayi for r in raporlar_list),
            "gercek": sum(r.gerceklesen_sayi for r in raporlar_list),
            "iptal": sum(r.iptal_sayi for r in raporlar_list),
            "oran": round(sum(r.gerceklesme_orani for r in raporlar_list) / len(raporlar_list), 1),
            "gun": len(raporlar_list),
        }

    # ═══ DÖNEM vs DÖNEM ═══
    if "Dönem" in karsilastirma_turu:
        bugun = date.today()
        bu_ay_bas = bugun.replace(day=1)
        gecen_ay_bit = bu_ay_bas - timedelta(days=1)
        gecen_ay_bas = gecen_ay_bit.replace(day=1)

        bu_ay_rap = [r for r in raporlar if bu_ay_bas.isoformat() <= r.tarih <= bugun.isoformat()]
        gecen_ay_rap = [r for r in raporlar if gecen_ay_bas.isoformat() <= r.tarih <= gecen_ay_bit.isoformat()]

        bu = _donem_metrik(bu_ay_rap)
        gecen = _donem_metrik(gecen_ay_rap)

        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">Bu Ay</div>', unsafe_allow_html=True)
            styled_stat_row([
                ("Planlanan", str(bu["plan"]), "#3b82f6", "📋"),
                ("Gerçekleşen", str(bu["gercek"]), "#10b981", "✅"),
                ("Ort. Oran", f"%{bu['oran']}", "#f59e0b", "📊"),
            ])
        with col2:
            st.markdown('<div style="text-align:center;font-size:32px;padding-top:30px;">⚖️</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">Geçen Ay</div>', unsafe_allow_html=True)
            styled_stat_row([
                ("Planlanan", str(gecen["plan"]), "#64748b", "📋"),
                ("Gerçekleşen", str(gecen["gercek"]), "#64748b", "✅"),
                ("Ort. Oran", f"%{gecen['oran']}", "#64748b", "📊"),
            ])

        # Fark analizi
        metrikler = [("Planlanan", bu["plan"], gecen["plan"]),
                     ("Gerçekleşen", bu["gercek"], gecen["gercek"]),
                     ("İptal", bu["iptal"], gecen["iptal"]),
                     ("Ort. Oran", bu["oran"], gecen["oran"])]

        styled_section("Fark Analizi")
        for label, bu_val, gc_val in metrikler:
            if gc_val == 0:
                fark_txt = "—"
                fark_renk = "#64748b"
            else:
                fark = round((bu_val - gc_val) / gc_val * 100, 1)
                fark_txt = f"+{fark}%" if fark >= 0 else f"{fark}%"
                fark_renk = "#10b981" if fark >= 0 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:6px 0;">
                <span style="min-width:100px;font-weight:600;color:#e2e8f0;font-size:13px;">{label}</span>
                <span style="min-width:60px;color:#3b82f6;font-weight:700;">{bu_val}</span>
                <span style="color:#64748b;">vs</span>
                <span style="min-width:60px;color:#94a3b8;font-weight:700;">{gc_val}</span>
                <span style="background:{fark_renk}20;color:{fark_renk};padding:3px 10px;border-radius:6px;
                            font-size:11px;font-weight:800;">{fark_txt}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ HAFTA vs HAFTA ═══
    elif "Hafta" in karsilastirma_turu:
        bugun = date.today()
        bu_hafta_bas = bugun - timedelta(days=bugun.weekday())
        hafta_secim = st.selectbox("Karşılaştırılacak hafta", [
            "Geçen Hafta", "2 Hafta Önce", "3 Hafta Önce", "4 Hafta Önce"
        ], key="yte_kc_hafta")
        hafta_offset = {"Geçen Hafta": 1, "2 Hafta Önce": 2, "3 Hafta Önce": 3, "4 Hafta Önce": 4}[hafta_secim]
        karsi_hafta_bas = bu_hafta_bas - timedelta(weeks=hafta_offset)
        karsi_hafta_bit = karsi_hafta_bas + timedelta(days=6)

        bu_rap = [r for r in raporlar if bu_hafta_bas.isoformat() <= r.tarih <= bugun.isoformat()]
        karsi_rap = [r for r in raporlar if karsi_hafta_bas.isoformat() <= r.tarih <= karsi_hafta_bit.isoformat()]

        bu = _donem_metrik(bu_rap)
        karsi = _donem_metrik(karsi_rap)

        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            st.markdown('<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">Bu Hafta</div>', unsafe_allow_html=True)
            styled_stat_row([("Plan", str(bu["plan"]), "#3b82f6", "📋"),
                             ("Gerçek", str(bu["gercek"]), "#10b981", "✅"),
                             ("Oran", f"%{bu['oran']}", "#f59e0b", "📊")])
        with col2:
            st.markdown('<div style="text-align:center;font-size:32px;padding-top:30px;">⚖️</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">{hafta_secim}</div>', unsafe_allow_html=True)
            styled_stat_row([("Plan", str(karsi["plan"]), "#64748b", "📋"),
                             ("Gerçek", str(karsi["gercek"]), "#64748b", "✅"),
                             ("Oran", f"%{karsi['oran']}", "#64748b", "📊")])

    # ═══ MODÜL vs MODÜL ═══
    elif "Modül" in karsilastirma_turu:
        modul_listesi = sorted(kpis.keys())
        col1, col2 = st.columns(2)
        with col1:
            m1 = st.selectbox("Modül A", modul_listesi, key="yte_kc_m1")
        with col2:
            m2 = st.selectbox("Modül B", [m for m in modul_listesi if m != m1] if modul_listesi else [], key="yte_kc_m2")

        if m1 and m2:
            kpi1 = kpis.get(m1, {})
            kpi2 = kpis.get(m2, {})
            p1 = alt_puanlar.get(m1, 0) if 'alt_puanlar' in dir() else 0
            p2 = alt_puanlar.get(m2, 0) if 'alt_puanlar' in dir() else 0
            _, alt_puanlar = _hesapla_saglik_puani(kpis)
            p1 = alt_puanlar.get(m1, 0)
            p2 = alt_puanlar.get(m2, 0)

            col1, col2, col3 = st.columns([1, 0.2, 1])
            with col1:
                ikon1 = MODUL_IKON.get(m1, "📋")
                st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">{ikon1} {m1}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;font-size:36px;font-weight:900;color:{_saglik_renk(p1)[0]};">{p1}</div>', unsafe_allow_html=True)
                for k, v in kpi1.items():
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:3px 0;"><span style="font-size:11px;color:#94a3b8;">{k.replace("_"," ").title()}</span><span style="font-size:12px;font-weight:700;color:#e2e8f0;">{v}</span></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="text-align:center;font-size:32px;padding-top:30px;">⚖️</div>', unsafe_allow_html=True)
            with col3:
                ikon2 = MODUL_IKON.get(m2, "📋")
                st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">{ikon2} {m2}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;font-size:36px;font-weight:900;color:{_saglik_renk(p2)[0]};">{p2}</div>', unsafe_allow_html=True)
                for k, v in kpi2.items():
                    st.markdown(f'<div style="display:flex;justify-content:space-between;padding:3px 0;"><span style="font-size:11px;color:#94a3b8;">{k.replace("_"," ").title()}</span><span style="font-size:12px;font-weight:700;color:#e2e8f0;">{v}</span></div>', unsafe_allow_html=True)

            # Kazanan
            kazanan = m1 if p1 > p2 else m2 if p2 > p1 else "Eşit"
            k_renk = "#10b981" if kazanan != "Eşit" else "#f59e0b"
            st.markdown(f"""
            <div style="background:{k_renk}15;border:1px solid {k_renk};border-radius:12px;
                        padding:12px;text-align:center;margin-top:12px;">
                <span style="font-size:14px;font-weight:800;color:{k_renk};">
                    🏆 {kazanan} {'daha iyi performans gösteriyor' if kazanan != 'Eşit' else '— her iki modül eşit'}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ KADEME vs KADEME ═══
    elif "Kademe" in karsilastirma_turu:
        kademeler = ["Anaokulu", "Ilkokul", "Ortaokul", "Lise"]
        col1, col2 = st.columns(2)
        with col1:
            k1 = st.selectbox("Kademe A", kademeler, key="yte_kc_k1")
        with col2:
            k2 = st.selectbox("Kademe B", [k for k in kademeler if k != k1], key="yte_kc_k2")

        # Kademe bazli verileri kayit modulunden cek
        try:
            from models.kayit_modulu import get_kayit_store
            kayit_store = get_kayit_store()
            adaylar = kayit_store.load_all()

            def _kademe_stat(kademe):
                k_adaylar = [a for a in adaylar if a.kademe == kademe]
                return {
                    "toplam": len(k_adaylar),
                    "aktif": sum(1 for a in k_adaylar if a.aktif),
                    "kesin": sum(1 for a in k_adaylar if a.asama == "kesin_kayit"),
                    "olumsuz": sum(1 for a in k_adaylar if a.asama == "olumsuz"),
                    "donusum": round(sum(1 for a in k_adaylar if a.asama == "kesin_kayit") / max(len(k_adaylar), 1) * 100, 1),
                }

            s1 = _kademe_stat(k1)
            s2 = _kademe_stat(k2)

            col1, col2, col3 = st.columns([1, 0.2, 1])
            with col1:
                st.markdown(f'<div style="text-align:center;font-weight:800;color:#3b82f6;font-size:16px;">🎓 {k1}</div>', unsafe_allow_html=True)
                styled_stat_row([("Aday", str(s1["toplam"]), "#3b82f6", "📋"),
                                 ("Kayıt", str(s1["kesin"]), "#10b981", "✅"),
                                 ("Dönüşüm", f"%{s1['donusum']}", "#f59e0b", "📊")])
            with col2:
                st.markdown('<div style="text-align:center;font-size:32px;padding-top:30px;">⚖️</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div style="text-align:center;font-weight:800;color:#f59e0b;font-size:16px;">🎓 {k2}</div>', unsafe_allow_html=True)
                styled_stat_row([("Aday", str(s2["toplam"]), "#64748b", "📋"),
                                 ("Kayıt", str(s2["kesin"]), "#64748b", "✅"),
                                 ("Dönüşüm", f"%{s2['donusum']}", "#64748b", "📊")])
        except Exception:
            st.info("Kayıt modülü verileri yüklenemedi.")
