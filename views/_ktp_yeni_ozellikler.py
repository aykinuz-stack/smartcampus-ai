"""
Kütüphane — Yeni Özellikler
=============================
1. Okuma Kulübü & Kitap Öneri Motoru
2. Akıllı Envanter & Kayıp-Hasar Takip
3. Otomatik Hatırlatma & Gecikme Yönetim
"""
from __future__ import annotations
import json, os, uuid
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _kd():
    d = os.path.join(get_tenant_dir(), "kutuphane"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_kd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_kd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_KITAP_TURLERI = ["Roman", "Hikaye", "Siir", "Bilim", "Tarih", "Biyografi", "Macera",
    "Bilim Kurgu", "Fantastik", "Polisiye", "Cocuk", "Genclik", "Klasik", "Diger"]

_HASAR_TURLERI = ["Kapak Hasari", "Sayfa Yirtigi", "Su Hasari", "Yipranma", "Kayip Sayfa",
    "Karalama / Cizme", "Cilt Ayrılmasi", "Tam Kayip", "Diger"]
_HASAR_SEVIYELERI = ["Hafif", "Orta", "Agir", "Kullanim Disi"]
_HASAR_RENK = {"Hafif": "#f59e0b", "Orta": "#ef4444", "Agir": "#dc2626", "Kullanim Disi": "#64748b"}

_MATERYAL_YASAM = ["Yeni", "Aktif", "Yipranmis", "Tamir Gerekli", "Ayiklanmis"]
_YASAM_RENK = {"Yeni": "#10b981", "Aktif": "#3b82f6", "Yipranmis": "#f59e0b", "Tamir Gerekli": "#ef4444", "Ayiklanmis": "#64748b"}

_SURE_POLITIKA = {"Ogrenci": 15, "Ogretmen": 30, "Personel": 21, "Diger": 14}


# ════════════════════════════════════════════════════════════
# 1. OKUMA KULÜBÜ & KİTAP ÖNERİ MOTORU
# ════════════════════════════════════════════════════════════

def render_okuma_kulubu(store):
    """Okuma Kulübü — kitap önerisi, okuma hedefi, yorum/puanlama."""
    styled_section("Okuma Kulubu & Kitap Oneri Motoru", "#7c3aed")
    styled_info_banner(
        "Ogrenci bazli kitap onerisi, okuma hedefi belirleme, "
        "kitap yorum/puanlama, sinif okuma listesi.",
        banner_type="info", icon="📖")

    yorumlar = _lj("kitap_yorumlari.json")
    hedefler = _lj("okuma_hedefleri.json")
    okuma_listeleri = _lj("okuma_listeleri.json")

    # Odunc gecmisinden okunan kitap sayisi
    islemler = []
    try:
        islemler = store.load_objects("odunc_islemleri")
    except Exception: pass
    iade_edilen = [i for i in islemler if getattr(i, 'durum', '') == "Iade"]

    styled_stat_row([
        ("Okunan Kitap", str(len(iade_edilen)), "#7c3aed", "📚"),
        ("Yorum", str(len(yorumlar)), "#3b82f6", "💬"),
        ("Okuma Hedefi", str(len(hedefler)), "#10b981", "🎯"),
        ("Okuma Listesi", str(len(okuma_listeleri)), "#f59e0b", "📋"),
    ])

    sub = st.tabs(["💬 Kitap Yorum", "🎯 Okuma Hedefi", "📋 Okuma Listesi", "🤖 Kitap Oneri", "🏆 Siralama"])

    # ── KİTAP YORUM ──
    with sub[0]:
        styled_section("Kitap Yorum & Puanlama")
        with st.form("yorum_form"):
            c1, c2 = st.columns(2)
            with c1:
                y_kitap = st.text_input("Kitap Adi", key="ky_kitap")
                y_yazar = st.text_input("Yazar", key="ky_yazar")
                y_tur = st.selectbox("Tur", _KITAP_TURLERI, key="ky_tur")
            with c2:
                y_okuyucu = st.text_input("Okuyucu Adi", key="ky_okuyucu")
                y_puan = st.select_slider("Puan", options=[1,2,3,4,5], value=4, key="ky_puan")
                y_tarih = st.date_input("Bitirme Tarihi", key="ky_tarih")
            y_yorum = st.text_area("Yorum", height=60, key="ky_yorum",
                placeholder="Bu kitap hakkinda ne dusunuyorsun?")

            if st.form_submit_button("Yorum Ekle", use_container_width=True):
                if y_kitap and y_okuyucu:
                    yorumlar.append({
                        "id": f"ky_{uuid.uuid4().hex[:8]}",
                        "kitap": y_kitap, "yazar": y_yazar, "tur": y_tur,
                        "okuyucu": y_okuyucu, "puan": y_puan,
                        "yorum": y_yorum, "tarih": y_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("kitap_yorumlari.json", yorumlar)
                    st.success(f"{'⭐'*y_puan} {y_kitap} — yorum eklendi!")
                    st.rerun()

        if yorumlar:
            styled_section("Son Yorumlar")
            for y in sorted(yorumlar, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                yildiz = "⭐" * y.get("puan", 0)
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #7c3aed;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">📚 {y.get('kitap','')}</span>
                        <span style="font-size:0.75rem;">{yildiz}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;">{y.get('yazar','')} | {y.get('tur','')} | {y.get('okuyucu','')}</div>
                    <div style="color:#64748b;font-size:0.72rem;font-style:italic;margin-top:3px;">"{y.get('yorum','')[:100]}"</div>
                </div>""", unsafe_allow_html=True)

    # ── OKUMA HEDEFİ ──
    with sub[1]:
        styled_section("Okuma Hedefi Belirle & Takip")
        with st.form("hedef_form"):
            c1, c2 = st.columns(2)
            with c1:
                h_okuyucu = st.text_input("Ogrenci Adi", key="oh_ogr")
                h_hedef = st.number_input("Aylik Hedef (kitap)", min_value=1, max_value=20, value=2, key="oh_hedef")
            with c2:
                h_ay = st.selectbox("Ay", list(range(1, 13)),
                    format_func=lambda x: {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}[x],
                    index=date.today().month - 1, key="oh_ay")
                h_okunan = st.number_input("Okunan Kitap", min_value=0, value=0, key="oh_okunan")

            if st.form_submit_button("Hedef Kaydet", use_container_width=True):
                if h_okuyucu:
                    hedefler.append({
                        "okuyucu": h_okuyucu, "hedef": h_hedef,
                        "okunan": h_okunan, "ay": h_ay,
                        "yil": date.today().year,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("okuma_hedefleri.json", hedefler)
                    ilerleme = round(h_okunan / max(h_hedef, 1) * 100)
                    st.success(f"{h_okuyucu}: {h_okunan}/{h_hedef} kitap (%{ilerleme})")
                    st.rerun()

        if hedefler:
            styled_section("Hedef Takibi")
            for h in sorted(hedefler, key=lambda x: x.get("created_at",""), reverse=True)[:10]:
                ilerleme = round(h.get("okunan",0) / max(h.get("hedef",1), 1) * 100)
                renk = "#10b981" if ilerleme >= 100 else "#f59e0b" if ilerleme >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:120px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{h.get('okuyucu','')}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{min(ilerleme,100)}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{h.get('okunan',0)}/{h.get('hedef',0)}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── OKUMA LİSTESİ ──
    with sub[2]:
        styled_section("Sinif Okuma Listesi Olustur")
        with st.form("liste_form"):
            c1, c2 = st.columns(2)
            with c1:
                l_sinif = st.text_input("Sinif/Sube", placeholder="7/A", key="ol_sinif")
                l_olusturan = st.text_input("Olusturan (Ogretmen)", key="ol_ogr")
            with c2:
                l_donem = st.selectbox("Donem", ["1. Donem", "2. Donem", "Yaz Tatili"], key="ol_donem")
            l_kitaplar = st.text_area("Kitap Listesi (her satira bir)", height=100, key="ol_kitaplar",
                placeholder="Kucuk Prens - Saint-Exupery\nSefiller - Victor Hugo\n...")

            if st.form_submit_button("Liste Kaydet", use_container_width=True):
                if l_sinif and l_kitaplar:
                    kitap_list = [k.strip() for k in l_kitaplar.split("\n") if k.strip()]
                    okuma_listeleri.append({
                        "id": f"ol_{uuid.uuid4().hex[:8]}",
                        "sinif": l_sinif, "olusturan": l_olusturan,
                        "donem": l_donem, "kitaplar": kitap_list,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("okuma_listeleri.json", okuma_listeleri)
                    st.success(f"{l_sinif} icin {len(kitap_list)} kitaplik liste olusturuldu!")
                    st.rerun()

        if okuma_listeleri:
            for ol in okuma_listeleri:
                with st.expander(f"📋 {ol.get('sinif','')} — {ol.get('donem','')} ({len(ol.get('kitaplar',[]))} kitap)"):
                    for idx, k in enumerate(ol.get("kitaplar", []), 1):
                        st.markdown(f"  {idx}. 📚 {k}")

    # ── KİTAP ÖNERİ ──
    with sub[3]:
        styled_section("Kisisel Kitap Onerisi")
        if not yorumlar:
            st.info("Oneri icin kitap yorum verisi gerekli. Once yorum ekleyin.")
        else:
            okuyucu_opts = list(set(y.get("okuyucu","") for y in yorumlar))
            sec = st.selectbox("Okuyucu Sec", okuyucu_opts, key="ko_sec")

            ogr_yorumlar = [y for y in yorumlar if y.get("okuyucu") == sec]
            if ogr_yorumlar:
                # En sevdigi turler
                tur_puan = defaultdict(list)
                for y in ogr_yorumlar:
                    tur_puan[y.get("tur","")].append(y.get("puan", 3))

                sirali = sorted(tur_puan.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
                en_sevilen = sirali[0][0] if sirali else "Diger"

                st.markdown(f"**{sec}** — {len(ogr_yorumlar)} kitap okumus, en sevdigi tur: **{en_sevilen}**")

                # Ayni turde yuksek puanli kitaplar (baskalarinin okudugu)
                oneriler = [y for y in yorumlar if y.get("tur") == en_sevilen
                            and y.get("puan", 0) >= 4 and y.get("okuyucu") != sec]

                if oneriler:
                    styled_section(f"'{en_sevilen}' Turunde Oneriler")
                    seen = set()
                    for o in sorted(oneriler, key=lambda x: x.get("puan",0), reverse=True):
                        if o.get("kitap") not in seen:
                            seen.add(o.get("kitap"))
                            st.markdown(f"""
                            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                                background:#7c3aed10;border:1px solid #7c3aed30;border-radius:10px;">
                                <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">📚 {o.get('kitap','')}</span>
                                <span style="color:#94a3b8;font-size:0.68rem;">{o.get('yazar','')}</span>
                                <span style="font-size:0.72rem;">{'⭐'*o.get('puan',0)}</span>
                            </div>""", unsafe_allow_html=True)
                            if len(seen) >= 5:
                                break
                else:
                    st.info(f"'{en_sevilen}' turunde baska yorum yok — daha fazla yorum eklendikce oneriler zenginlesir.")

    # ── SIRALAMA ──
    with sub[4]:
        styled_section("En Cok Okunan & En Yuksek Puanli")
        if yorumlar:
            # En cok yorumlanan
            kitap_say = Counter(y.get("kitap","") for y in yorumlar)
            styled_section("En Cok Okunan")
            for sira, (kitap, sayi) in enumerate(kitap_say.most_common(10), 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #7c3aed;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{kitap}</span>
                    <span style="color:#7c3aed;font-weight:700;">{sayi} okuma</span>
                </div>""", unsafe_allow_html=True)

            # En yuksek puanli
            styled_section("En Yuksek Puanli")
            kitap_puan = defaultdict(list)
            for y in yorumlar:
                kitap_puan[y.get("kitap","")].append(y.get("puan", 0))
            sirali_puan = sorted(kitap_puan.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
            for sira, (kitap, puanlar) in enumerate(sirali_puan[:10], 1):
                ort = round(sum(puanlar) / len(puanlar), 1)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #c9a84c;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{kitap}</span>
                    <span style="color:#c9a84c;font-weight:700;">{ort}/5 ({'⭐'*round(ort)})</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Yorum verisi yok.")


# ════════════════════════════════════════════════════════════
# 2. AKILLI ENVANTER & KAYIP-HASAR TAKİP
# ════════════════════════════════════════════════════════════

def render_envanter_takip(store):
    """Akıllı Envanter — kayıp/hasar kayıt, yaşam döngüsü, raf haritası, sipariş."""
    styled_section("Akilli Envanter & Kayip-Hasar Takip", "#2563eb")
    styled_info_banner(
        "Yillik envanter sayim, kayip/hasarli materyal kayit, "
        "materyal yasam dongusu, raf haritasi, siparis onerisi.",
        banner_type="info", icon="🔄")

    hasar_kayitlari = _lj("hasar_kayitlari.json")
    sayim_kayitlari = _lj("envanter_sayim.json")

    materyaller = []
    try:
        materyaller = store.load_objects("materyaller")
    except Exception: pass

    # KPI
    toplam = len(materyaller)
    aktif = sum(1 for m in materyaller if getattr(m, 'durum', '') == "Aktif")
    hasarli = len(hasar_kayitlari)
    kayip = sum(1 for h in hasar_kayitlari if h.get("tur") == "Tam Kayip")

    styled_stat_row([
        ("Toplam Materyal", str(toplam), "#2563eb", "📚"),
        ("Aktif", str(aktif), "#10b981", "✅"),
        ("Hasar Kaydi", str(hasarli), "#f59e0b", "⚠️"),
        ("Kayip", str(kayip), "#ef4444", "❌"),
    ])

    sub = st.tabs(["🔍 Hasar/Kayip Kaydet", "📋 Hasar Listesi", "📦 Envanter Sayim", "🗺️ Raf Haritasi", "🛒 Siparis Oneri"])

    # ── HASAR/KAYIP KAYDET ──
    with sub[0]:
        styled_section("Hasar / Kayip Kaydi")
        with st.form("hasar_form"):
            c1, c2 = st.columns(2)
            with c1:
                if materyaller:
                    mat_opts = [f"{getattr(m,'baslik','')} ({getattr(m,'materyal_kodu','')})" for m in materyaller]
                    h_mat = st.selectbox("Materyal", mat_opts, key="hs_mat")
                else:
                    h_mat = st.text_input("Materyal", key="hs_mat")
                h_tur = st.selectbox("Hasar Turu", _HASAR_TURLERI, key="hs_tur")
            with c2:
                h_seviye = st.selectbox("Seviye", _HASAR_SEVIYELERI, key="hs_sev")
                h_tarih = st.date_input("Tespit Tarihi", key="hs_tarih")
            h_aciklama = st.text_area("Aciklama", height=60, key="hs_acik")

            if st.form_submit_button("Kaydet", use_container_width=True):
                hasar_kayitlari.append({
                    "id": f"hs_{uuid.uuid4().hex[:8]}",
                    "materyal": h_mat if isinstance(h_mat, str) else str(h_mat),
                    "tur": h_tur, "seviye": h_seviye,
                    "aciklama": h_aciklama, "tarih": h_tarih.isoformat(),
                    "created_at": datetime.now().isoformat(),
                })
                _sj("hasar_kayitlari.json", hasar_kayitlari)
                st.success("Hasar/kayip kaydedildi!")
                st.rerun()

    # ── HASAR LİSTESİ ──
    with sub[1]:
        styled_section("Hasar & Kayip Kayitlari")
        if not hasar_kayitlari:
            st.success("Hasar/kayip kaydi yok.")
        else:
            for h in sorted(hasar_kayitlari, key=lambda x: x.get("tarih",""), reverse=True):
                renk = _HASAR_RENK.get(h.get("seviye",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:8px 14px;margin:4px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">{h.get('materyal','')[:40]}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.65rem;font-weight:700;">{h.get('seviye','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:2px;">{h.get('tur','')} — {h.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    # ── ENVANTER SAYIM ──
    with sub[2]:
        styled_section("Envanter Sayim Kaydi")
        with st.form("sayim_form"):
            s_tarih = st.date_input("Sayim Tarihi", key="sy_tarih")
            s_sayan = st.text_input("Sayan Kisi", key="sy_sayan")
            s_beklenen = st.number_input("Beklenen Adet", min_value=0, value=toplam, key="sy_bek")
            s_bulunan = st.number_input("Bulunan Adet", min_value=0, value=toplam, key="sy_bul")
            s_not = st.text_area("Sayim Notu", height=40, key="sy_not")

            if st.form_submit_button("Sayim Kaydet", use_container_width=True):
                fark = s_bulunan - s_beklenen
                sayim_kayitlari.append({
                    "tarih": s_tarih.isoformat(), "sayan": s_sayan,
                    "beklenen": s_beklenen, "bulunan": s_bulunan,
                    "fark": fark, "not": s_not,
                    "created_at": datetime.now().isoformat(),
                })
                _sj("envanter_sayim.json", sayim_kayitlari)
                renk = "#10b981" if fark == 0 else "#ef4444"
                st.success(f"Sayim tamamlandi! Fark: {fark}")

        if sayim_kayitlari:
            styled_section("Sayim Gecmisi")
            for s in sorted(sayim_kayitlari, key=lambda x: x.get("tarih",""), reverse=True)[:5]:
                fark = s.get("fark", 0)
                renk = "#10b981" if fark == 0 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-size:0.78rem;flex:1;">{s.get('tarih','')[:10]} — {s.get('sayan','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">Beklenen: {s.get('beklenen',0)}</span>
                    <span style="color:{renk};font-weight:700;font-size:0.72rem;">Bulunan: {s.get('bulunan',0)} (fark: {fark})</span>
                </div>""", unsafe_allow_html=True)

    # ── RAF HARİTASI ──
    with sub[3]:
        styled_section("Raf Doluluk Haritasi")
        if not materyaller:
            st.info("Materyal verisi yok.")
        else:
            raf_grp = Counter()
            for m in materyaller:
                raf = getattr(m, 'raf_no', '') or "Belirsiz"
                if getattr(m, 'durum', '') == "Aktif":
                    raf_grp[raf] += 1

            if raf_grp:
                max_val = max(raf_grp.values())
                for raf in sorted(raf_grp.keys()):
                    sayi = raf_grp[raf]
                    pct = round(sayi / max(max_val, 1) * 100)
                    renk = "#ef4444" if sayi <= 3 else "#f59e0b" if sayi <= 8 else "#10b981"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:70px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">📚 {raf}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Raf verisi yok.")

    # ── SİPARİŞ ÖNERİ ──
    with sub[4]:
        styled_section("Otomatik Siparis Onerisi")
        if not materyaller:
            st.info("Materyal verisi yok.")
        else:
            # Az kalan kategoriler
            kat_say = Counter()
            for m in materyaller:
                if getattr(m, 'durum', '') == "Aktif":
                    kat_say[getattr(m, 'kategori', 'Diger')] += 1

            az_kalan = [(kat, sayi) for kat, sayi in kat_say.items() if sayi <= 5]
            if az_kalan:
                st.warning(f"{len(az_kalan)} kategoride stok dusuk!")
                for kat, sayi in sorted(az_kalan, key=lambda x: x[1]):
                    renk = "#ef4444" if sayi <= 2 else "#f59e0b"
                    st.markdown(f"""
                    <div style="background:{renk}10;border:1px solid {renk}30;border-left:4px solid {renk};
                        border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                        <span style="color:{renk};font-weight:800;">⚠️ {kat}</span>
                        <span style="color:#e2e8f0;font-size:0.78rem;margin-left:8px;">Sadece {sayi} materyal — yenileme onerilir</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Tum kategorilerde yeterli stok mevcut.")


# ════════════════════════════════════════════════════════════
# 3. OTOMATİK HATIRLATMA & GECİKME YÖNETİM
# ════════════════════════════════════════════════════════════

def render_gecikme_yonetim(store):
    """Otomatik Hatırlatma & Gecikme Yönetim — hatırlatma, ceza, rezervasyon, politika."""
    styled_section("Otomatik Hatirlatma & Gecikme Yonetim", "#ef4444")
    styled_info_banner(
        "Iade tarihi yaklasanlara hatirlatma, gecikme ceza puani, "
        "rezervasyon sistemi, veliye bildirim, sure politikasi.",
        banner_type="warning", icon="⏰")

    hatirlatmalar = _lj("kutuphane_hatirlatma.json")
    rezervasyonlar = _lj("kutuphane_rezervasyon.json")

    islemler = []
    try:
        islemler = store.load_objects("odunc_islemleri")
    except Exception: pass

    bugun = date.today()

    # Geciken ve yaklasan
    geciken = []
    yaklasan = []
    for isl in islemler:
        if getattr(isl, 'durum', '') != "Odunc":
            continue
        iade_str = getattr(isl, 'iade_tarihi', '')
        if not iade_str:
            continue
        try:
            iade = date.fromisoformat(iade_str[:10])
        except Exception:
            continue
        kalan = (iade - bugun).days
        entry = {
            "materyal": getattr(isl, 'materyal_adi', ''),
            "kisi": getattr(isl, 'odunc_alan_adi', ''),
            "iade_tarihi": iade_str[:10],
            "kalan": kalan,
        }
        if kalan < 0:
            geciken.append(entry)
        elif kalan <= 3:
            yaklasan.append(entry)

    styled_stat_row([
        ("Geciken", str(len(geciken)), "#ef4444", "🔴"),
        ("3 Gun Icinde", str(len(yaklasan)), "#f59e0b", "🟡"),
        ("Hatirlatma", str(len(hatirlatmalar)), "#3b82f6", "📨"),
        ("Rezervasyon", str(len(rezervasyonlar)), "#8b5cf6", "📌"),
    ])

    sub = st.tabs(["🔴 Geciken", "🟡 Yaklasan", "📌 Rezervasyon", "📨 Hatirlatma", "⚙️ Sure Politikasi"])

    # ── GECİKEN ──
    with sub[0]:
        styled_section("Geciken Materyaller")
        if not geciken:
            st.success("Geciken materyal yok!")
        else:
            for g in sorted(geciken, key=lambda x: x["kalan"]):
                gun = abs(g["kalan"])
                renk = "#dc2626" if gun >= 7 else "#ef4444"
                st.markdown(f"""
                <div style="background:#ef444410;border:1px solid #ef444430;border-left:5px solid {renk};
                    border-radius:0 12px 12px 0;padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#fca5a5;font-weight:700;font-size:0.85rem;">📚 {g['materyal']}</span>
                        <span style="color:{renk};font-weight:800;font-size:0.8rem;">{gun} gun gecikme!</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        {g['kisi']} | Iade: {g['iade_tarihi']}</div>
                </div>""", unsafe_allow_html=True)

    # ── YAKLAŞAN ──
    with sub[1]:
        styled_section("Iade Tarihi Yaklasan (3 Gun)")
        if not yaklasan:
            st.success("Yaklasan iade yok.")
        else:
            for y in sorted(yaklasan, key=lambda x: x["kalan"]):
                renk = "#ef4444" if y["kalan"] <= 1 else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#f59e0b10;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">📚 {y['materyal']}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{y['kisi']}</span>
                    <span style="color:{renk};font-weight:700;font-size:0.72rem;">{y['kalan']} gun kaldi</span>
                </div>""", unsafe_allow_html=True)

    # ── REZERVASYON ──
    with sub[2]:
        styled_section("Kitap Rezervasyon Sistemi")
        with st.form("rez_form"):
            c1, c2 = st.columns(2)
            with c1:
                r_kitap = st.text_input("Kitap Adi", key="rz_kitap")
                r_kisi = st.text_input("Rezerve Eden", key="rz_kisi")
            with c2:
                r_tarih = st.date_input("Talep Tarihi", key="rz_tarih")

            if st.form_submit_button("Rezerve Et", use_container_width=True):
                if r_kitap and r_kisi:
                    rezervasyonlar.append({
                        "id": f"rz_{uuid.uuid4().hex[:8]}",
                        "kitap": r_kitap, "kisi": r_kisi,
                        "tarih": r_tarih.isoformat(), "durum": "Bekliyor",
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("kutuphane_rezervasyon.json", rezervasyonlar)
                    st.success(f"'{r_kitap}' icin rezervasyon olusturuldu!")
                    st.rerun()

        if rezervasyonlar:
            styled_section("Aktif Rezervasyonlar")
            for r in sorted(rezervasyonlar, key=lambda x: x.get("tarih",""), reverse=True):
                d_renk = "#3b82f6" if r.get("durum") == "Bekliyor" else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid {d_renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.78rem;flex:1;">📌 {r.get('kitap','')}</span>
                    <span style="color:#94a3b8;font-size:0.68rem;">{r.get('kisi','')}</span>
                    <span style="color:{d_renk};font-size:0.65rem;font-weight:700;">{r.get('durum','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── HATIRLATMA ──
    with sub[3]:
        styled_section("Hatirlatma Gecmisi & Yeni Gonder")
        if geciken or yaklasan:
            if st.button("Tum Gecikenler Icin Hatirlatma Olustur", use_container_width=True, type="primary"):
                yeni = 0
                for g in geciken + yaklasan:
                    hatirlatmalar.append({
                        "kisi": g["kisi"], "materyal": g["materyal"],
                        "iade_tarihi": g["iade_tarihi"],
                        "tip": "Gecikme" if g["kalan"] < 0 else "Yaklasan",
                        "tarih": datetime.now().isoformat(),
                    })
                    yeni += 1
                _sj("kutuphane_hatirlatma.json", hatirlatmalar)
                st.success(f"{yeni} hatirlatma olusturuldu!")
                st.rerun()

        if hatirlatmalar:
            styled_section(f"Gonderilen Hatirlatmalar ({len(hatirlatmalar)})")
            for h in sorted(hatirlatmalar, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                tip_renk = "#ef4444" if h.get("tip") == "Gecikme" else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;padding:4px 10px;margin:2px 0;
                    background:#0f172a;border-left:2px solid {tip_renk};border-radius:0 6px 6px 0;">
                    <span style="color:{tip_renk};font-size:0.65rem;font-weight:700;min-width:60px;">{h.get('tip','')}</span>
                    <span style="color:#e2e8f0;font-size:0.72rem;flex:1;">{h.get('kisi','')} — {h.get('materyal','')[:25]}</span>
                    <span style="color:#64748b;font-size:0.6rem;">{h.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── SÜRE POLİTİKASI ──
    with sub[4]:
        styled_section("Odunc Sure Politikasi")
        for tip, gun in _SURE_POLITIKA.items():
            renk = "#3b82f6" if gun <= 15 else "#10b981" if gun <= 21 else "#f59e0b"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;margin:5px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;min-width:100px;">👤 {tip}</span>
                <span style="color:{renk};font-weight:800;font-size:1.1rem;">{gun} gun</span>
            </div>""", unsafe_allow_html=True)

        st.caption("Sure politikasi degisikligi icin Ayarlar sekmesini kullanin.")
