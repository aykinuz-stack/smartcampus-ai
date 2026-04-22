"""
Rehberlik Modülü — Yeni Özellikler
====================================
1. Sosyo-Duygusal Takip Paneli
2. Akran Arabuluculuk & Çatışma Çözümü
3. Kariyer Rehberliği & Meslek Keşfi
4. Kriz Müdahale Protokolü
5. Öğrenci Gelişim Dosyası (Kümülatif Kayıt)
6. Veli Psiko-eğitim & Seminer Takip
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import datetime, date, timedelta

import streamlit as st

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi, get_student_display_options
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ════════════════════════════════════════════════════════════
# ORTAK YARDIMCILAR
# ════════════════════════════════════════════════════════════

def _rhb_data_dir() -> str:
    d = os.path.join(get_tenant_dir(), "rehberlik")
    os.makedirs(d, exist_ok=True)
    return d


def _load_json(name: str) -> list:
    p = os.path.join(_rhb_data_dir(), name)
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_json(name: str, data: list) -> None:
    p = os.path.join(_rhb_data_dir(), name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ogrenci_sec(key: str) -> dict | None:
    students = load_shared_students()
    if not students:
        st.warning("Henuz ogrenci kaydi yok.")
        return None
    opts = ["-- Secin --"] + [
        f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}"
        for s in students
    ]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None


_MOOD_EMOJIS = {"Cok Mutlu": "😄", "Mutlu": "🙂", "Normal": "😐", "Mutsuz": "😟", "Cok Mutsuz": "😢", "Ofkeli": "😠", "Kaygili": "😰"}
_MOOD_RENK = {"Cok Mutlu": "#10b981", "Mutlu": "#34d399", "Normal": "#f59e0b", "Mutsuz": "#f97316", "Cok Mutsuz": "#ef4444", "Ofkeli": "#dc2626", "Kaygili": "#8b5cf6"}
_MOOD_PUAN = {"Cok Mutlu": 5, "Mutlu": 4, "Normal": 3, "Mutsuz": 2, "Cok Mutsuz": 1, "Ofkeli": 1, "Kaygili": 2}

_DAVRANIS_TURLERI = [
    "Olumlu Davranış", "Uyumsuz Davranış", "Agresif Davranış", "İçe Kapanma",
    "Sosyal Beceri Gelişimi", "Akademik Motivasyon Düşüşü", "Akran İlişkisi Sorunu",
    "Dikkat Eksikliği", "Aile Kaynaklı Sorun", "Diğer"
]

_CATISMA_TURLERI = [
    "Sözel Çatışma", "Fiziksel Çatışma", "Sosyal Dışlama / Mobbing",
    "Dijital Zorbalık", "Eşya Anlaşmazlığı", "Dedikodu / İftira",
    "Grup İçi Çatışma", "Öğretmen-Öğrenci Anlaşmazlığı", "Diğer"
]

_CATISMA_DURUMLARI = ["Açık", "Arabuluculuk Başladı", "Çözüldü", "İzleniyor", "Tırmanma Riski"]
_CATISMA_DURUM_RENK = {"Açık": "#ef4444", "Arabuluculuk Başladı": "#f59e0b", "Çözüldü": "#10b981", "İzleniyor": "#3b82f6", "Tırmanma Riski": "#dc2626"}

_HOLLAND_TIPLERI = {
    "R": ("Gerçekçi (Realistic)", "Ellerini kullanan, pratik, doğa/mekanik seven", "#ef4444"),
    "I": ("Araştırmacı (Investigative)", "Meraklı, analitik, bilimsel düşünen", "#3b82f6"),
    "A": ("Sanatçı (Artistic)", "Yaratıcı, bağımsız, estetik duyarlılığı yüksek", "#8b5cf6"),
    "S": ("Sosyal (Social)", "Yardımsever, iletişimi güçlü, insanlarla çalışan", "#10b981"),
    "E": ("Girişimci (Enterprising)", "Lider, ikna edici, risk alabilen", "#f59e0b"),
    "C": ("Geleneksel (Conventional)", "Düzenli, detaycı, kurallara uyumlu", "#6366f1"),
}

_HOLLAND_SORULARI = [
    ("Makineleri tamir etmek veya kurcalamak", "R"),
    ("Bilimsel makaleler okumak", "I"),
    ("Resim veya müzikle uğraşmak", "A"),
    ("İnsanlara yardım etmek, gönüllü çalışmak", "S"),
    ("Bir ekip veya proje yönetmek", "E"),
    ("Verileri düzenlemek, tablolar oluşturmak", "C"),
    ("Doğada yürüyüş, kampçılık, tarım işleri", "R"),
    ("Matematik veya fen problemleri çözmek", "I"),
    ("Şiir/hikaye yazmak veya tiyatro oynamak", "A"),
    ("Bir arkadaşının derdini dinlemek", "S"),
    ("Bir iş kurmak veya satış yapmak", "E"),
    ("Dosyaları sınıflandırmak, arşiv düzenlemek", "C"),
    ("Elektronik devreler veya robotlarla çalışmak", "R"),
    ("Laboratuvarda deney yapmak", "I"),
    ("Tasarım veya fotoğrafçılık", "A"),
    ("Öğretmenlik veya koçluk yapmak", "S"),
    ("Bir topluluk önünde konuşmak", "E"),
    ("Muhasebe veya envanter tutmak", "C"),
]

_MESLEK_HARITASI = {
    "R": ["Mühendislik", "Teknisyenlik", "Pilotluk", "Mimarlık", "Veterinerlik", "Çiftçilik", "Ormancılık"],
    "I": ["Doktorluk", "Araştırmacı", "Biyolog", "Kimyager", "Eczacı", "Veri Bilimci", "Arkeolog"],
    "A": ["Grafik Tasarımcı", "Müzisyen", "Yazar", "Fotoğrafçı", "Moda Tasarımcı", "Aktör", "İç Mimar"],
    "S": ["Öğretmen", "Psikolog", "Sosyal Hizmet", "Hemşire", "Diyetisyen", "Rehber", "İnsan Kaynakları"],
    "E": ["Avukat", "Pazarlamacı", "Girişimci", "Politikacı", "Emlakçı", "Finans Yöneticisi", "CEO"],
    "C": ["Muhasebeci", "Bankacı", "Kütüphaneci", "Sekreter", "İstatistikçi", "Lojistikçi", "Arşivci"],
}


# ════════════════════════════════════════════════════════════
# 1. SOSYO-DUYGUSAL TAKİP PANELİ
# ════════════════════════════════════════════════════════════

def render_sosyo_duygusal_takip():
    """Sosyo-Duygusal Takip Paneli — mood tracking, davranış kayıt, trend analizi."""
    styled_section("Sosyo-Duygusal Takip Paneli", "#8b5cf6")
    styled_info_banner(
        "Ogrencilerin duygu durumu, davranis degisimleri ve sosyal becerilerini "
        "zaman icinde izleyin. Erken mudahale tetikleyicileri otomatik calisir.",
        banner_type="info", icon="🧠")

    kayitlar = _load_json("sosyo_duygusal.json")
    davranis_kayitlari = _load_json("davranis_olaylari.json")

    # KPI
    bugun = date.today().isoformat()
    bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    bugun_kayit = sum(1 for k in kayitlar if k.get("tarih", "")[:10] == bugun)
    hafta_kayit = sum(1 for k in kayitlar if k.get("tarih", "")[:10] >= bu_hafta)
    riskli = sum(1 for k in kayitlar if _MOOD_PUAN.get(k.get("duygu", "Normal"), 3) <= 2
                 and k.get("tarih", "")[:10] >= bu_hafta)
    davranis_hafta = sum(1 for d in davranis_kayitlari if d.get("tarih", "")[:10] >= bu_hafta)

    styled_stat_row([
        ("Bugun", str(bugun_kayit), "#8b5cf6", "📅"),
        ("Bu Hafta", str(hafta_kayit), "#3b82f6", "📊"),
        ("Riskli Ogrenci", str(riskli), "#ef4444", "🚨"),
        ("Davranis Olayi", str(davranis_hafta), "#f59e0b", "⚠️"),
        ("Toplam Kayit", str(len(kayitlar)), "#10b981", "📋"),
    ])

    sub = st.tabs(["😊 Duygu Kaydi", "⚠️ Davranis Olayi", "📈 Trend Analizi", "🚨 Erken Uyari"])

    # ── TAB 1: DUYGU KAYDI ──
    with sub[0]:
        styled_section("Duygu Durumu Kaydi")

        with st.form("sdt_duygu_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogrenci_sec("sdt_ogr")
                duygu = st.selectbox("Duygu Durumu", list(_MOOD_EMOJIS.keys()), key="sdt_duygu")
            with c2:
                tarih = st.date_input("Tarih", value=date.today(), key="sdt_tarih")
                ortam = st.selectbox("Gozlem Ortami",
                    ["Sinif Ici", "Teneffus", "Yemekhane", "Spor Aktivitesi", "Bireysel Gorusme", "Diger"],
                    key="sdt_ortam")
            notlar = st.text_area("Gozlem Notlari", height=80, key="sdt_not")
            tetikleyici = st.text_input("Tetikleyici Olay (varsa)", key="sdt_tetik")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if ogr:
                    kayit = {
                        "id": f"sdt_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "duygu": duygu,
                        "puan": _MOOD_PUAN.get(duygu, 3),
                        "ortam": ortam,
                        "notlar": notlar,
                        "tetikleyici": tetikleyici,
                        "tarih": tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    kayitlar.append(kayit)
                    _save_json("sosyo_duygusal.json", kayitlar)
                    st.success(f"{_MOOD_EMOJIS.get(duygu, '')} {ogr.get('ad','')} icin duygu kaydi eklendi!")
                    st.rerun()

        # Son kayitlar
        if kayitlar:
            styled_section("Son Kayitlar")
            for k in sorted(kayitlar, key=lambda x: x.get("tarih", ""), reverse=True)[:15]:
                emoji = _MOOD_EMOJIS.get(k.get("duygu", ""), "")
                renk = _MOOD_RENK.get(k.get("duygu", ""), "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;margin:4px 0;
                    background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.5rem;">{emoji}</span>
                    <div style="flex:1;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{k.get('ogrenci_ad','')}</span>
                        <span style="color:#94a3b8;font-size:0.75rem;margin-left:8px;">{k.get('sinif','')}/{k.get('sube','')}</span>
                        <span style="color:{renk};font-size:0.75rem;margin-left:8px;font-weight:600;">{k.get('duygu','')}</span>
                    </div>
                    <span style="color:#64748b;font-size:0.7rem;">{k.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── TAB 2: DAVRANIS OLAYI ──
    with sub[1]:
        styled_section("Davranis Olayi Kaydi")

        with st.form("sdt_davranis_form"):
            c1, c2 = st.columns(2)
            with c1:
                d_ogr = _ogrenci_sec("sdt_d_ogr")
                d_tur = st.selectbox("Davranis Turu", _DAVRANIS_TURLERI, key="sdt_d_tur")
            with c2:
                d_tarih = st.date_input("Tarih", value=date.today(), key="sdt_d_tarih")
                d_siddet = st.select_slider("Siddet", options=["Hafif", "Orta", "Ciddi", "Kritik"], key="sdt_d_sid")
            d_aciklama = st.text_area("Olay Aciklamasi", height=80, key="sdt_d_acik")
            d_mudahale = st.text_area("Yapilan Mudahale", height=60, key="sdt_d_mud")

            if st.form_submit_button("Davranis Kaydet", use_container_width=True):
                if d_ogr:
                    dk = {
                        "id": f"dav_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": d_ogr.get("id", ""),
                        "ogrenci_ad": f"{d_ogr.get('ad','')} {d_ogr.get('soyad','')}",
                        "sinif": d_ogr.get("sinif", ""),
                        "sube": d_ogr.get("sube", ""),
                        "tur": d_tur,
                        "siddet": d_siddet,
                        "aciklama": d_aciklama,
                        "mudahale": d_mudahale,
                        "tarih": d_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    davranis_kayitlari.append(dk)
                    _save_json("davranis_olaylari.json", davranis_kayitlari)
                    st.success(f"{d_ogr.get('ad','')} icin davranis olayi kaydedildi!")
                    st.rerun()

        if davranis_kayitlari:
            styled_section("Son Davranis Olaylari")
            sid_renk = {"Hafif": "#10b981", "Orta": "#f59e0b", "Ciddi": "#ef4444", "Kritik": "#dc2626"}
            for d in sorted(davranis_kayitlari, key=lambda x: x.get("tarih", ""), reverse=True)[:10]:
                r = sid_renk.get(d.get("siddet", ""), "#94a3b8")
                st.markdown(f"""
                <div style="padding:8px 12px;margin:4px 0;background:#0f172a;border-left:4px solid {r};border-radius:0 8px 8px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{d.get('ogrenci_ad','')}</span>
                        <span style="background:{r}20;color:{r};padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:700;">{d.get('siddet','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:2px;">{d.get('tur','')} — {d.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

    # ── TAB 3: TREND ANALİZİ ──
    with sub[2]:
        styled_section("Duygu Durumu Trend Analizi")
        if not kayitlar:
            st.info("Henuz kayit yok. Duygu kaydi ekleyin.")
        else:
            # Haftalik ortalama
            hafta_grp = {}
            for k in kayitlar:
                t = k.get("tarih", "")[:10]
                try:
                    dt = date.fromisoformat(t)
                    hafta = dt - timedelta(days=dt.weekday())
                    hafta_key = hafta.isoformat()
                except Exception:
                    continue
                hafta_grp.setdefault(hafta_key, []).append(_MOOD_PUAN.get(k.get("duygu", "Normal"), 3))

            if hafta_grp:
                styled_section("Haftalik Duygu Ortalamalari")
                for h in sorted(hafta_grp.keys())[-8:]:
                    puanlar = hafta_grp[h]
                    ort = round(sum(puanlar) / len(puanlar), 1)
                    bar_w = round(ort / 5 * 100)
                    renk = "#10b981" if ort >= 3.5 else "#f59e0b" if ort >= 2.5 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:80px;font-size:0.7rem;color:#94a3b8;">{h[5:]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.6rem;color:#fff;font-weight:700;">{ort}</span>
                            </div>
                        </div>
                        <span style="font-size:0.7rem;color:#64748b;">{len(puanlar)} kayit</span>
                    </div>""", unsafe_allow_html=True)

            # Duygu dagilimi
            styled_section("Duygu Dagilimi")
            duygu_say = Counter(k.get("duygu", "Normal") for k in kayitlar)
            toplam = max(len(kayitlar), 1)
            for duygu, sayi in duygu_say.most_common():
                pct = round(sayi / toplam * 100)
                renk = _MOOD_RENK.get(duygu, "#94a3b8")
                emoji = _MOOD_EMOJIS.get(duygu, "")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                    <span style="min-width:25px;font-size:1.1rem;">{emoji}</span>
                    <span style="min-width:90px;font-size:0.75rem;color:#e2e8f0;font-weight:600;">{duygu}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <span style="font-size:0.7rem;color:#64748b;">{sayi} (%{pct})</span>
                </div>""", unsafe_allow_html=True)

    # ── TAB 4: ERKEN UYARI ──
    with sub[3]:
        styled_section("Erken Uyari Sistemi", "#ef4444")
        styled_info_banner(
            "Son 2 haftada duygu puani dusuk (<=2) olan veya 2+ davranis olayi yasayan ogrenciler otomatik listelenir.",
            banner_type="warning", icon="🚨")

        iki_hafta = (date.today() - timedelta(days=14)).isoformat()
        # Riskli ogrencileri bul
        ogr_puanlar = {}
        for k in kayitlar:
            if k.get("tarih", "")[:10] >= iki_hafta:
                oid = k.get("ogrenci_id", "")
                ogr_puanlar.setdefault(oid, {"ad": k.get("ogrenci_ad", ""), "sinif": k.get("sinif", ""),
                                              "sube": k.get("sube", ""), "puanlar": [], "kayitlar": []})
                ogr_puanlar[oid]["puanlar"].append(_MOOD_PUAN.get(k.get("duygu", "Normal"), 3))
                ogr_puanlar[oid]["kayitlar"].append(k)

        ogr_davranis = {}
        for d in davranis_kayitlari:
            if d.get("tarih", "")[:10] >= iki_hafta:
                oid = d.get("ogrenci_id", "")
                ogr_davranis.setdefault(oid, []).append(d)

        riskli_list = []
        for oid, data in ogr_puanlar.items():
            ort = sum(data["puanlar"]) / max(len(data["puanlar"]), 1)
            dav_count = len(ogr_davranis.get(oid, []))
            risk_skoru = 0
            if ort <= 2:
                risk_skoru += 3
            elif ort <= 2.5:
                risk_skoru += 2
            risk_skoru += min(dav_count, 3)
            if risk_skoru >= 2:
                riskli_list.append({**data, "ort": round(ort, 1), "dav": dav_count, "risk": risk_skoru, "oid": oid})

        riskli_list.sort(key=lambda x: x["risk"], reverse=True)

        if not riskli_list:
            st.success("Su anda erken uyari gerektiren ogrenci yok.")
        else:
            st.warning(f"{len(riskli_list)} ogrenci erken uyari listesinde!")
            for r in riskli_list:
                risk_renk = "#dc2626" if r["risk"] >= 4 else "#ef4444" if r["risk"] >= 3 else "#f59e0b"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {risk_renk}30;border-left:5px solid {risk_renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">🚨 {r['ad']}</span>
                            <span style="color:#64748b;font-size:0.75rem;margin-left:8px;">{r['sinif']}/{r['sube']}</span>
                        </div>
                        <span style="background:{risk_renk}20;color:{risk_renk};padding:3px 10px;border-radius:8px;
                            font-size:0.7rem;font-weight:800;">Risk: {r['risk']}/6</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">
                        Duygu Ort: <b style="color:{risk_renk}">{r['ort']}/5</b> | Davranis Olayi: <b>{r['dav']}</b> (son 2 hafta)
                    </div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. AKRAN ARABULUCULUK & ÇATIŞMA ÇÖZÜMÜ
# ════════════════════════════════════════════════════════════

def render_akran_arabuluculuk():
    """Akran Arabuluculuk & Çatışma Çözümü — kayıt, süreç takip, raporlama."""
    styled_section("Akran Arabuluculuk & Catisma Cozumu", "#f59e0b")
    styled_info_banner(
        "Ogrenciler arasi catismalarin kayit altina alindigi, arabuluculuk surecinin "
        "takip edildigi ve MEB Akran Arabuluculuk Programi dokumantasyonunun otomatik olustugu sistem.",
        banner_type="info", icon="🤝")

    catismalar = _load_json("catisma_kayitlari.json")

    # KPI
    acik = sum(1 for c in catismalar if c.get("durum") in ("Açık", "Arabuluculuk Başladı", "Tırmanma Riski"))
    cozuldu = sum(1 for c in catismalar if c.get("durum") == "Çözüldü")
    izleniyor = sum(1 for c in catismalar if c.get("durum") == "İzleniyor")
    cozum_orani = round(cozuldu / max(len(catismalar), 1) * 100)

    styled_stat_row([
        ("Toplam Vaka", str(len(catismalar)), "#f59e0b", "📋"),
        ("Acik", str(acik), "#ef4444", "🔴"),
        ("Cozuldu", str(cozuldu), "#10b981", "✅"),
        ("Izleniyor", str(izleniyor), "#3b82f6", "👁️"),
        ("Cozum Orani", f"%{cozum_orani}", "#10b981" if cozum_orani >= 70 else "#f59e0b", "📊"),
    ])

    sub = st.tabs(["➕ Yeni Kayit", "📋 Vaka Listesi", "🔄 Durum Guncelle", "📊 Rapor"])

    # ── YENİ KAYIT ──
    with sub[0]:
        styled_section("Yeni Catisma Kaydi")
        with st.form("arb_yeni_form"):
            c1, c2 = st.columns(2)
            with c1:
                taraf1 = _ogrenci_sec("arb_taraf1")
                tur = st.selectbox("Catisma Turu", _CATISMA_TURLERI, key="arb_tur")
                tarih = st.date_input("Olay Tarihi", value=date.today(), key="arb_tarih")
            with c2:
                taraf2 = _ogrenci_sec("arb_taraf2")
                konum = st.text_input("Olay Yeri", placeholder="Sinif, koridor, bahce...", key="arb_konum")
                taniklar = st.text_input("Taniklar (opsiyonel)", key="arb_tanik")

            olay_ozet = st.text_area("Olay Ozeti", height=80, key="arb_ozet")
            arabulucu = st.text_input("Arabulucu (varsa)", key="arb_arabulucu")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if taraf1 and taraf2:
                    kayit = {
                        "id": f"cat_{uuid.uuid4().hex[:8]}",
                        "taraf1_id": taraf1.get("id", ""),
                        "taraf1_ad": f"{taraf1.get('ad','')} {taraf1.get('soyad','')}",
                        "taraf2_id": taraf2.get("id", ""),
                        "taraf2_ad": f"{taraf2.get('ad','')} {taraf2.get('soyad','')}",
                        "tur": tur,
                        "konum": konum,
                        "taniklar": taniklar,
                        "olay_ozet": olay_ozet,
                        "arabulucu": arabulucu,
                        "durum": "Açık",
                        "gorusmeler": [],
                        "tarih": tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    catismalar.append(kayit)
                    _save_json("catisma_kayitlari.json", catismalar)
                    st.success("Catisma kaydi olusturuldu!")
                    st.rerun()

    # ── VAKA LİSTESİ ──
    with sub[1]:
        styled_section("Catisma Vakalari")
        if not catismalar:
            st.info("Henuz catisma kaydi yok.")
        else:
            for c in sorted(catismalar, key=lambda x: x.get("tarih", ""), reverse=True):
                d_renk = _CATISMA_DURUM_RENK.get(c.get("durum", ""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {d_renk}30;border-left:4px solid {d_renk};
                    border-radius:0 10px 10px 0;padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">
                            {c.get('taraf1_ad','')} ↔ {c.get('taraf2_ad','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{c.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">
                        {c.get('tur','')} — {c.get('tarih','')[:10]} — Arabulucu: {c.get('arabulucu','Atanmadi')}
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── DURUM GÜNCELLE ──
    with sub[2]:
        styled_section("Durum Guncelle")
        if not catismalar:
            st.info("Guncellenecek vaka yok.")
        else:
            acik_vakalar = [c for c in catismalar if c.get("durum") != "Çözüldü"]
            if not acik_vakalar:
                st.success("Tum vakalar cozulmus!")
            else:
                for c in acik_vakalar:
                    cid = c.get("id", "")
                    with st.expander(f"🔄 {c.get('taraf1_ad','')} ↔ {c.get('taraf2_ad','')} ({c.get('durum','')})"):
                        yeni_durum = st.selectbox("Yeni Durum", _CATISMA_DURUMLARI,
                            index=_CATISMA_DURUMLARI.index(c.get("durum", "Açık")) if c.get("durum") in _CATISMA_DURUMLARI else 0,
                            key=f"arb_d_{cid}")
                        gorusme_notu = st.text_area("Gorusme Notu", key=f"arb_n_{cid}", height=60)

                        if st.button("Guncelle", key=f"arb_g_{cid}"):
                            c["durum"] = yeni_durum
                            if gorusme_notu:
                                c.setdefault("gorusmeler", []).append({
                                    "tarih": datetime.now().isoformat(),
                                    "not": gorusme_notu,
                                    "durum": yeni_durum,
                                })
                            _save_json("catisma_kayitlari.json", catismalar)
                            st.success("Durum guncellendi!")
                            st.rerun()

    # ── RAPOR ──
    with sub[3]:
        styled_section("Catisma Istatistikleri")
        if catismalar:
            tur_say = Counter(c.get("tur", "Diger") for c in catismalar)
            styled_section("Catisma Turu Dagilimi")
            en_cok = tur_say.most_common(1)[0][1] if tur_say else 1
            for tur, sayi in tur_say.most_common():
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                    <span style="min-width:150px;font-size:0.75rem;color:#e2e8f0;font-weight:600;">{tur}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#f59e0b;border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            styled_section("Durum Dagilimi")
            durum_say = Counter(c.get("durum", "Acik") for c in catismalar)
            for durum, sayi in durum_say.most_common():
                renk = _CATISMA_DURUM_RENK.get(durum, "#94a3b8")
                st.markdown(f"""
                <div style="display:inline-block;background:{renk}15;color:{renk};padding:6px 16px;
                    border-radius:10px;border:1px solid {renk}30;margin:3px;font-size:0.8rem;font-weight:700;">
                    {durum}: {sayi}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Henuz veri yok.")


# ════════════════════════════════════════════════════════════
# 3. KARİYER REHBERLİĞİ & MESLEK KEŞFİ
# ════════════════════════════════════════════════════════════

def render_kariyer_rehberligi():
    """Kariyer Rehberliği & Meslek Keşfi — Holland testi, RIASEC profili, meslek eşleştirme."""
    styled_section("Kariyer Rehberligi & Meslek Kesfi", "#6366f1")
    styled_info_banner(
        "Holland tipi ilgi envanteri, RIASEC profili, meslek esleştirme. "
        "Ortaokul/lise ogrencileri icin kariyer yol haritasi.",
        banner_type="info", icon="🎯")

    kariyer_kayitlari = _load_json("kariyer_profilleri.json")

    styled_stat_row([
        ("Profil Sayisi", str(len(kariyer_kayitlari)), "#6366f1", "👤"),
        ("Bu Ay", str(sum(1 for k in kariyer_kayitlari if k.get("tarih","")[:7] == date.today().strftime("%Y-%m"))), "#3b82f6", "📅"),
    ])

    sub = st.tabs(["🧪 Holland Testi", "👤 Profil Goruntule", "🗺️ Meslek Haritasi", "📊 Sinif Analizi"])

    # ── HOLLAND TESTİ ──
    with sub[0]:
        styled_section("Holland Ilgi Envanteri (RIASEC)")
        st.caption("18 soru — her soru icin 'Beni tanimliyor' veya 'Beni tanimlamiyor' secin.")

        ogr = _ogrenci_sec("kr_ogr")
        if ogr:
            with st.form("kr_holland_form"):
                cevaplar = {}
                for i, (soru, tip) in enumerate(_HOLLAND_SORULARI):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{i+1}.** {soru}")
                    with col2:
                        cevaplar[i] = st.checkbox("Evet", key=f"kr_h_{i}")

                if st.form_submit_button("Sonuclari Hesapla", use_container_width=True):
                    # Puanlama
                    skorlar = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
                    for i, (soru, tip) in enumerate(_HOLLAND_SORULARI):
                        if cevaplar.get(i, False):
                            skorlar[tip] += 1

                    # RIASEC sirala
                    sirali = sorted(skorlar.items(), key=lambda x: x[1], reverse=True)
                    profil_kod = "".join(t for t, _ in sirali[:3])

                    # Kaydet
                    kayit = {
                        "id": f"kr_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "sinif": ogr.get("sinif", ""),
                        "sube": ogr.get("sube", ""),
                        "skorlar": skorlar,
                        "profil_kod": profil_kod,
                        "tarih": date.today().isoformat(),
                    }
                    kariyer_kayitlari.append(kayit)
                    _save_json("kariyer_profilleri.json", kariyer_kayitlari)

                    st.success(f"RIASEC Profil Kodu: **{profil_kod}**")

                    # Sonuc goster
                    for tip, skor in sirali:
                        ad, aciklama, renk = _HOLLAND_TIPLERI[tip]
                        bar_w = round(skor / 3 * 100)
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                            <span style="background:{renk};color:#fff;padding:4px 10px;border-radius:8px;
                                font-weight:800;font-size:0.8rem;min-width:30px;text-align:center;">{tip}</span>
                            <span style="min-width:120px;font-size:0.75rem;color:#e2e8f0;font-weight:600;">{ad.split('(')[0].strip()}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                                <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                                    <span style="font-size:0.6rem;color:#fff;font-weight:700;">{skor}/3</span>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)

                    # Meslek onerileri
                    st.markdown("---")
                    styled_section("Onerilen Meslekler")
                    top3 = [t for t, _ in sirali[:3]]
                    for tip in top3:
                        ad, _, renk = _HOLLAND_TIPLERI[tip]
                        meslekler = _MESLEK_HARITASI.get(tip, [])
                        st.markdown(f"""
                        <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                            border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;">
                            <span style="color:{renk};font-weight:800;font-size:0.85rem;">{ad}</span>
                            <div style="color:#94a3b8;font-size:0.75rem;margin-top:4px;">
                                {' · '.join(meslekler)}</div>
                        </div>""", unsafe_allow_html=True)

    # ── PROFİL GÖRÜNTÜLE ──
    with sub[1]:
        styled_section("Ogrenci Kariyer Profilleri")
        if not kariyer_kayitlari:
            st.info("Henuz profil yok. Holland Testi ile baslatin.")
        else:
            for k in sorted(kariyer_kayitlari, key=lambda x: x.get("tarih", ""), reverse=True)[:20]:
                skorlar = k.get("skorlar", {})
                top_tip = max(skorlar, key=skorlar.get) if skorlar else "?"
                _, _, renk = _HOLLAND_TIPLERI.get(top_tip, ("?", "?", "#94a3b8"))
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;margin:4px 0;
                    background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="background:{renk};color:#fff;padding:4px 12px;border-radius:8px;
                        font-weight:800;font-size:0.85rem;">{k.get('profil_kod','?')}</span>
                    <div style="flex:1;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{k.get('ogrenci_ad','')}</span>
                        <span style="color:#64748b;font-size:0.7rem;margin-left:8px;">{k.get('sinif','')}/{k.get('sube','')}</span>
                    </div>
                    <span style="color:#64748b;font-size:0.7rem;">{k.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── MESLEK HARİTASI ──
    with sub[2]:
        styled_section("RIASEC Meslek Haritasi")
        for tip, (ad, aciklama, renk) in _HOLLAND_TIPLERI.items():
            meslekler = _MESLEK_HARITASI.get(tip, [])
            with st.expander(f"{tip} — {ad}"):
                st.markdown(f"*{aciklama}*")
                for m in meslekler:
                    st.markdown(f"- 💼 {m}")

    # ── SINIF ANALİZİ ──
    with sub[3]:
        styled_section("Sinif Bazli RIASEC Dagilimi")
        if not kariyer_kayitlari:
            st.info("Yeterli veri yok.")
        else:
            sinif_grp = {}
            for k in kariyer_kayitlari:
                key = f"{k.get('sinif','')}/{k.get('sube','')}"
                sinif_grp.setdefault(key, []).append(k)

            for sinif_key in sorted(sinif_grp.keys()):
                kayitlar_s = sinif_grp[sinif_key]
                styled_section(f"{sinif_key} ({len(kayitlar_s)} ogrenci)")
                tip_say = Counter()
                for k in kayitlar_s:
                    skorlar = k.get("skorlar", {})
                    if skorlar:
                        top = max(skorlar, key=skorlar.get)
                        tip_say[top] += 1

                for tip, sayi in tip_say.most_common():
                    ad, _, renk = _HOLLAND_TIPLERI.get(tip, ("?", "?", "#94a3b8"))
                    pct = round(sayi / max(len(kayitlar_s), 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:8px;
                            font-weight:800;font-size:0.75rem;min-width:25px;text-align:center;">{tip}</span>
                        <span style="min-width:100px;font-size:0.75rem;color:#e2e8f0;">{ad.split('(')[0].strip()}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;"></div>
                        </div>
                        <span style="font-size:0.7rem;color:#64748b;">{sayi} (%{pct})</span>
                    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 4. KRİZ MÜDAHALE PROTOKOLÜ
# ════════════════════════════════════════════════════════════

_KRIZ_TURLERI = [
    "İntihar Riski / Girişimi",
    "İstismar Şüphesi (Fiziksel/Cinsel/Duygusal)",
    "Madde Kullanımı",
    "Öğrenci Kayıp / Kaçırma",
    "Şiddet / Silahlı Tehdit",
    "Doğal Afet",
    "Ölüm / Yas (Öğrenci/Personel/Yakın)",
    "Toplumsal Olay / Travma",
    "Dijital Zorbalık (Ciddi)",
    "Kendine Zarar Verme",
    "Aile İçi Şiddet Bildirimi",
    "Diğer Acil Durum",
]

_KRIZ_SEVIYELERI = {
    "Seviye 1 — Düşük": ("#f59e0b", "Gozlem altinda, yakin takip yeterli"),
    "Seviye 2 — Orta": ("#f97316", "Bireysel mudahale gerekli, aile bilgilendirilmeli"),
    "Seviye 3 — Yüksek": ("#ef4444", "Kurum ici kriz ekibi devrede, RAM bilgilendirilmeli"),
    "Seviye 4 — Kritik": ("#dc2626", "Acil resmi bildirim: 112 / Savcılık / İl MEM"),
}

_BILDIRIM_ZINCIRI = {
    "Seviye 1 — Düşük": ["Sınıf Öğretmeni", "Rehber Öğretmen", "Müdür Yardımcısı"],
    "Seviye 2 — Orta": ["Rehber Öğretmen", "Müdür Yardımcısı", "Veli", "Okul Müdürü"],
    "Seviye 3 — Yüksek": ["Okul Müdürü", "RAM", "Veli", "İlçe MEM"],
    "Seviye 4 — Kritik": ["112 Acil", "Savcılık", "İl MEM", "Okul Müdürü", "RAM", "Veli"],
}

_PROTOKOL_ADIMLARI = {
    "İntihar Riski / Girişimi": [
        "Ogrenciyi yalniz birakmayın — guvenli ortamda tutun",
        "Okul mudurunu hemen bilgilendirin",
        "112'yi arayin (girişim varsa)",
        "Veliyi arayarak bilgilendirin",
        "RAM'a yazılı bildirim yapın",
        "Kriz mudahale formu doldurun",
        "Takip gorusmesi planlayin (24 saat icinde)",
    ],
    "İstismar Şüphesi (Fiziksel/Cinsel/Duygusal)": [
        "Ogrenciyle guvenli ortamda gorusun — sorgulama yapmayin",
        "Gozlemlerinizi yazili kayit altina alin",
        "Okul mudurunu bilgilendirin",
        "ALO 183 Sosyal Destek Hattini arayin",
        "Savciliga suc duyurusunda bulunun (zorunlu bildirim)",
        "Ogrencinin guvenligini saglayin",
        "RAM ile koordine olun",
    ],
    "Madde Kullanımı": [
        "Ogrenciyi sakin bir ortama alin",
        "Saglik durumunu kontrol edin — 112 gerekiyorsa arayin",
        "Okul mudurunu bilgilendirin",
        "Veliyi bilgilendirin",
        "RAM'a yonlendirme yapin",
        "Ogrenci icin destek plani olusturun",
    ],
}


def render_kriz_mudahale():
    """Kriz Müdahale Protokolü — acil durum yönetimi, bildirim zinciri, müdahale kaydı."""
    styled_section("Kriz Mudahale Protokolu", "#dc2626")
    styled_info_banner(
        "Acil durumlarda MEB kriz mudahale adimlarini otomatik baslatin. "
        "Bildirim zinciri, dakika bazli mudahale kaydi, yasal bildirim takibi.",
        banner_type="warning", icon="🚨")

    krizler = _load_json("kriz_kayitlari.json")

    # KPI
    aktif = sum(1 for k in krizler if k.get("durum") != "Kapandi")
    bu_ay = sum(1 for k in krizler if k.get("tarih", "")[:7] == date.today().strftime("%Y-%m"))
    kritik = sum(1 for k in krizler if "Seviye 4" in k.get("seviye", "") or "Seviye 3" in k.get("seviye", ""))

    styled_stat_row([
        ("Toplam", str(len(krizler)), "#dc2626", "📋"),
        ("Aktif", str(aktif), "#ef4444", "🔴"),
        ("Bu Ay", str(bu_ay), "#f59e0b", "📅"),
        ("Kritik/Yuksek", str(kritik), "#dc2626", "🚨"),
    ])

    sub = st.tabs(["🚨 Yeni Kriz", "📋 Aktif Krizler", "📝 Mudahale Kaydi", "📊 Protokol Rehberi"])

    # ── YENİ KRİZ ──
    with sub[0]:
        styled_section("Yeni Kriz Bildirimi", "#dc2626")
        st.markdown("""
        <div style="background:#dc262615;border:2px solid #dc2626;border-radius:12px;padding:14px 18px;margin-bottom:12px;">
            <span style="color:#fca5a5;font-weight:800;font-size:0.9rem;">
            ⚠️ UYARI: Bu ekran acil durum protokolunu baslatir. Bildirim zinciri otomatik olusturulur.</span>
        </div>""", unsafe_allow_html=True)

        with st.form("kriz_yeni_form"):
            c1, c2 = st.columns(2)
            with c1:
                k_ogr = _ogrenci_sec("kriz_ogr")
                k_tur = st.selectbox("Kriz Turu", _KRIZ_TURLERI, key="kriz_tur")
                k_tarih = st.date_input("Olay Tarihi", value=date.today(), key="kriz_tarih")
            with c2:
                k_seviye = st.selectbox("Kriz Seviyesi", list(_KRIZ_SEVIYELERI.keys()), key="kriz_seviye")
                k_konum = st.text_input("Olay Yeri", key="kriz_konum")
                k_saat = st.time_input("Olay Saati", key="kriz_saat")

            k_aciklama = st.text_area("Olay Aciklamasi", height=100, key="kriz_acik",
                placeholder="Olaya iliskin ilk gozlemler, ogrencinin durumu, taniklar...")
            k_ilk_mud = st.text_area("Yapilan Ilk Mudahale", height=60, key="kriz_ilk",
                placeholder="Olay aninda alinan ilk onlemler...")

            if st.form_submit_button("🚨 KRİZ PROTOKOLÜNÜ BAŞLAT", use_container_width=True, type="primary"):
                if k_ogr:
                    bildirim = _BILDIRIM_ZINCIRI.get(k_seviye, [])
                    kriz = {
                        "id": f"krz_{uuid.uuid4().hex[:8]}",
                        "ogrenci_id": k_ogr.get("id", ""),
                        "ogrenci_ad": f"{k_ogr.get('ad','')} {k_ogr.get('soyad','')}",
                        "sinif": k_ogr.get("sinif", ""),
                        "sube": k_ogr.get("sube", ""),
                        "tur": k_tur,
                        "seviye": k_seviye,
                        "konum": k_konum,
                        "saat": str(k_saat),
                        "aciklama": k_aciklama,
                        "ilk_mudahale": k_ilk_mud,
                        "bildirim_zinciri": bildirim,
                        "bildirim_durumu": {b: "Bekliyor" for b in bildirim},
                        "mudahale_kayitlari": [{
                            "dakika": 0,
                            "eylem": "Kriz protokolu baslatildi",
                            "yapan": "Rehber Ogretmen",
                            "zaman": datetime.now().isoformat(),
                        }],
                        "durum": "Aktif",
                        "tarih": k_tarih.isoformat(),
                        "created_at": datetime.now().isoformat(),
                    }
                    krizler.append(kriz)
                    _save_json("kriz_kayitlari.json", krizler)
                    st.success("Kriz protokolu baslatildi!")
                    st.warning(f"Bildirim Zinciri: {' → '.join(bildirim)}")
                    st.rerun()

    # ── AKTİF KRİZLER ──
    with sub[1]:
        styled_section("Aktif Krizler")
        aktif_list = [k for k in krizler if k.get("durum") != "Kapandi"]
        if not aktif_list:
            st.success("Aktif kriz bulunmuyor.")
        else:
            for k in sorted(aktif_list, key=lambda x: x.get("created_at", ""), reverse=True):
                sev_renk, _ = _KRIZ_SEVIYELERI.get(k.get("seviye", ""), ("#94a3b8", ""))
                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {sev_renk};border-left:6px solid {sev_renk};
                    border-radius:0 12px 12px 0;padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#fca5a5;font-weight:900;font-size:1rem;">🚨 {k.get('ogrenci_ad','')}</span>
                            <span style="color:#64748b;font-size:0.75rem;margin-left:8px;">{k.get('sinif','')}/{k.get('sube','')}</span>
                        </div>
                        <span style="background:{sev_renk}25;color:{sev_renk};padding:4px 12px;border-radius:8px;
                            font-size:0.75rem;font-weight:800;">{k.get('seviye','')}</span>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.85rem;margin-top:6px;font-weight:600;">{k.get('tur','')}</div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">
                        {k.get('tarih','')[:10]} {k.get('saat','')} — {k.get('konum','')}
                    </div>
                    <div style="color:#64748b;font-size:0.7rem;margin-top:6px;">
                        Bildirim: {' → '.join(k.get('bildirim_zinciri',[]))}
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:2px;">
                        Mudahale: {len(k.get('mudahale_kayitlari',[]))} kayit
                    </div>
                </div>""", unsafe_allow_html=True)

                # Bildirim durumu + kapat butonu
                with st.expander(f"Detay: {k.get('id','')}", expanded=False):
                    # Bildirim zinciri durumu
                    st.markdown("**Bildirim Zinciri:**")
                    bd = k.get("bildirim_durumu", {})
                    for birim, durum in bd.items():
                        renk = "#10b981" if durum == "Bildirildi" else "#f59e0b" if durum == "Bekliyor" else "#94a3b8"
                        emoji = "✅" if durum == "Bildirildi" else "⏳"
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"{emoji} **{birim}** — {durum}")
                        with c2:
                            if durum != "Bildirildi":
                                if st.button("Bildirildi", key=f"bd_{k['id']}_{birim}"):
                                    k["bildirim_durumu"][birim] = "Bildirildi"
                                    _save_json("kriz_kayitlari.json", krizler)
                                    st.rerun()

                    # Mudahale kaydi ekle
                    st.markdown("---")
                    mud_not = st.text_input("Yeni mudahale notu", key=f"mud_{k['id']}")
                    mc1, mc2 = st.columns(2)
                    with mc1:
                        if st.button("Mudahale Ekle", key=f"me_{k['id']}"):
                            if mud_not:
                                k.setdefault("mudahale_kayitlari", []).append({
                                    "dakika": len(k.get("mudahale_kayitlari", [])),
                                    "eylem": mud_not,
                                    "yapan": "Rehber Ogretmen",
                                    "zaman": datetime.now().isoformat(),
                                })
                                _save_json("kriz_kayitlari.json", krizler)
                                st.rerun()
                    with mc2:
                        if st.button("Krizi Kapat", key=f"kk_{k['id']}", type="primary"):
                            k["durum"] = "Kapandi"
                            k["kapanma_tarihi"] = datetime.now().isoformat()
                            _save_json("kriz_kayitlari.json", krizler)
                            st.success("Kriz kapatildi.")
                            st.rerun()

    # ── MÜDAHALE KAYDI ──
    with sub[2]:
        styled_section("Mudahale Zaman Cizelgesi")
        if not krizler:
            st.info("Henuz kriz kaydi yok.")
        else:
            for k in sorted(krizler, key=lambda x: x.get("created_at", ""), reverse=True)[:5]:
                sev_renk, _ = _KRIZ_SEVIYELERI.get(k.get("seviye", ""), ("#94a3b8", ""))
                st.markdown(f"**{k.get('ogrenci_ad','')}** — {k.get('tur','')} ({k.get('durum','')})")
                for m in k.get("mudahale_kayitlari", []):
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;padding:6px 0;border-left:3px solid {sev_renk};padding-left:12px;margin:3px 0;">
                        <span style="background:{sev_renk}20;color:{sev_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.65rem;font-weight:800;min-width:40px;text-align:center;">+{m.get('dakika',0)}dk</span>
                        <span style="color:#e2e8f0;font-size:0.8rem;">{m.get('eylem','')}</span>
                        <span style="color:#64748b;font-size:0.65rem;margin-left:auto;">{m.get('zaman','')[:16]}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")

    # ── PROTOKOL REHBERİ ──
    with sub[3]:
        styled_section("Kriz Turu Bazli Mudahale Protokolleri")
        for kriz_turu, adimlar in _PROTOKOL_ADIMLARI.items():
            with st.expander(f"📋 {kriz_turu}"):
                for i, adim in enumerate(adimlar, 1):
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;align-items:flex-start;padding:6px 0;">
                        <span style="background:#dc2626;color:#fff;min-width:24px;height:24px;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.7rem;">{i}</span>
                        <span style="color:#e2e8f0;font-size:0.85rem;">{adim}</span>
                    </div>""", unsafe_allow_html=True)

        styled_section("Kriz Seviyesi Rehberi")
        for seviye, (renk, aciklama) in _KRIZ_SEVIYELERI.items():
            bildirim = _BILDIRIM_ZINCIRI.get(seviye, [])
            st.markdown(f"""
            <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 10px 10px 0;
                padding:10px 14px;margin:6px 0;">
                <span style="color:{renk};font-weight:800;font-size:0.85rem;">{seviye}</span>
                <div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">{aciklama}</div>
                <div style="color:#64748b;font-size:0.7rem;margin-top:4px;">
                    Bildirim: {' → '.join(bildirim)}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 5. ÖĞRENCİ GELİŞİM DOSYASI (KÜMÜLATİF KAYIT)
# ════════════════════════════════════════════════════════════

def render_ogrenci_gelisim_dosyasi():
    """Tüm modüllerden toplanan verilerin tek öğrenci bazında birleştirildiği dijital dosya."""
    styled_section("Ogrenci Gelisim Dosyasi", "#2563eb")
    styled_info_banner(
        "Gorusme, vaka, BEP, test, sosyo-duygusal, kariyer, kriz — "
        "tum rehberlik verilerinin tek ogrenci bazinda birlestirildigi kumülatif kayit.",
        banner_type="info", icon="📁")

    ogr = _ogrenci_sec("gd_ogr")
    if not ogr:
        return

    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
    ogr_id = ogr.get("id", "")
    sinif = ogr.get("sinif", "")
    sube = ogr.get("sube", "")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:16px 20px;border-radius:14px;margin-bottom:14px;">
        <div style="color:#fff;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
        <div style="color:#93c5fd;font-size:0.8rem;">{sinif}. Sinif / {sube} Subesi</div>
    </div>""", unsafe_allow_html=True)

    # Veri toplama
    gorusmeler = [g for g in _load_json("gorusme_kayitlari.json") if g.get("ogrenci_id") == ogr_id]
    vakalar = [v for v in _load_json("vaka_kayitlari.json") if v.get("ogrenci_id") == ogr_id]
    bep = [b for b in _load_json("bep_kayitlari.json") if b.get("ogrenci_id") == ogr_id]
    testler = [t for t in _load_json("test_sonuclari.json") if t.get("ogrenci_id") == ogr_id]
    duygusal = [d for d in _load_json("sosyo_duygusal.json") if d.get("ogrenci_id") == ogr_id]
    davranis = [d for d in _load_json("davranis_olaylari.json") if d.get("ogrenci_id") == ogr_id]
    kariyer = [k for k in _load_json("kariyer_profilleri.json") if k.get("ogrenci_id") == ogr_id]
    krizler_ogr = [k for k in _load_json("kriz_kayitlari.json") if k.get("ogrenci_id") == ogr_id]
    catismalar_ogr = [c for c in _load_json("catisma_kayitlari.json")
                      if c.get("taraf1_id") == ogr_id or c.get("taraf2_id") == ogr_id]

    # Ozet KPI
    styled_stat_row([
        ("Gorusme", str(len(gorusmeler)), "#3b82f6", "💬"),
        ("Vaka", str(len(vakalar)), "#f59e0b", "📁"),
        ("BEP", str(len(bep)), "#8b5cf6", "🎓"),
        ("Test", str(len(testler)), "#10b981", "🧪"),
        ("Duygusal", str(len(duygusal)), "#6366f1", "🧠"),
        ("Davranis", str(len(davranis)), "#ef4444", "⚠️"),
        ("Kriz", str(len(krizler_ogr)), "#dc2626", "🚨"),
    ])

    sub = st.tabs(["📅 Zaman Cizelgesi", "📊 Genel Ozet", "🧠 Sosyo-Duygusal", "🎯 Kariyer"])

    # ── ZAMAN ÇİZELGESİ ──
    with sub[0]:
        styled_section("Kronolojik Gelisim Cizelgesi")
        tum_olaylar = []
        for g in gorusmeler:
            tum_olaylar.append({"tarih": g.get("tarih", ""), "tip": "Gorusme", "renk": "#3b82f6",
                "ikon": "💬", "baslik": g.get("konu", "Gorusme"), "detay": g.get("notlar", "")[:80]})
        for v in vakalar:
            tum_olaylar.append({"tarih": v.get("tarih", ""), "tip": "Vaka", "renk": "#f59e0b",
                "ikon": "📁", "baslik": v.get("baslik", "Vaka"), "detay": v.get("aciklama", "")[:80]})
        for b in bep:
            tum_olaylar.append({"tarih": b.get("tarih", ""), "tip": "BEP", "renk": "#8b5cf6",
                "ikon": "🎓", "baslik": f"BEP: {b.get('durum','')}", "detay": b.get("hedef", "")[:80]})
        for d in duygusal:
            tum_olaylar.append({"tarih": d.get("tarih", ""), "tip": "Duygu", "renk": _MOOD_RENK.get(d.get("duygu",""), "#94a3b8"),
                "ikon": _MOOD_EMOJIS.get(d.get("duygu",""), ""), "baslik": d.get("duygu", ""),
                "detay": d.get("notlar", "")[:80]})
        for dv in davranis:
            tum_olaylar.append({"tarih": dv.get("tarih", ""), "tip": "Davranis", "renk": "#ef4444",
                "ikon": "⚠️", "baslik": dv.get("tur", "Davranis"), "detay": dv.get("aciklama", "")[:80]})
        for kr in krizler_ogr:
            tum_olaylar.append({"tarih": kr.get("tarih", ""), "tip": "Kriz", "renk": "#dc2626",
                "ikon": "🚨", "baslik": kr.get("tur", "Kriz"), "detay": kr.get("aciklama", "")[:80]})
        for c in catismalar_ogr:
            tum_olaylar.append({"tarih": c.get("tarih", ""), "tip": "Catisma", "renk": "#f97316",
                "ikon": "🤝", "baslik": f"Catisma: {c.get('tur','')}", "detay": c.get("olay_ozet", "")[:80]})

        tum_olaylar.sort(key=lambda x: x.get("tarih", ""), reverse=True)

        if not tum_olaylar:
            st.info(f"{ogr_ad} icin henuz kayit yok.")
        else:
            for o in tum_olaylar[:30]:
                st.markdown(f"""
                <div style="display:flex;gap:12px;padding:8px 0;border-left:3px solid {o['renk']};padding-left:14px;margin:4px 0;">
                    <div style="min-width:70px;">
                        <div style="font-size:0.7rem;color:#64748b;">{o['tarih'][:10]}</div>
                        <div style="background:{o['renk']}20;color:{o['renk']};padding:2px 8px;border-radius:6px;
                            font-size:0.6rem;font-weight:700;margin-top:2px;text-align:center;">{o['tip']}</div>
                    </div>
                    <div style="flex:1;">
                        <span style="font-size:1rem;margin-right:6px;">{o['ikon']}</span>
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{o['baslik']}</span>
                        <div style="color:#94a3b8;font-size:0.72rem;margin-top:2px;">{o['detay']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── GENEL ÖZET ──
    with sub[1]:
        styled_section(f"{ogr_ad} — Genel Degerlendirme")
        toplam_olay = len(tum_olaylar)
        if toplam_olay == 0:
            st.info("Yeterli veri yok.")
        else:
            tip_say = Counter(o["tip"] for o in tum_olaylar)
            for tip, sayi in tip_say.most_common():
                renk_map = {"Gorusme": "#3b82f6", "Vaka": "#f59e0b", "BEP": "#8b5cf6",
                    "Duygu": "#6366f1", "Davranis": "#ef4444", "Kriz": "#dc2626", "Catisma": "#f97316"}
                r = renk_map.get(tip, "#94a3b8")
                pct = round(sayi / toplam_olay * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:80px;font-size:0.75rem;color:#e2e8f0;font-weight:600;">{tip}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{r};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── SOSYO-DUYGUSAL ÖZET ──
    with sub[2]:
        styled_section(f"{ogr_ad} — Duygu Gecmisi")
        if not duygusal:
            st.info("Duygu kaydi yok.")
        else:
            for d in sorted(duygusal, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                emoji = _MOOD_EMOJIS.get(d.get("duygu",""), "")
                renk = _MOOD_RENK.get(d.get("duygu",""), "#94a3b8")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="font-size:1.2rem;">{emoji}</span>
                    <span style="color:{renk};font-weight:700;font-size:0.8rem;min-width:80px;">{d.get('duygu','')}</span>
                    <span style="color:#94a3b8;font-size:0.72rem;">{d.get('ortam','')}</span>
                    <span style="color:#64748b;font-size:0.68rem;margin-left:auto;">{d.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── KARİYER PROFİL ──
    with sub[3]:
        styled_section(f"{ogr_ad} — Kariyer Profili")
        if not kariyer:
            st.info("Kariyer profili yok. Holland Testi uygulatin.")
        else:
            son = sorted(kariyer, key=lambda x: x.get("tarih",""), reverse=True)[0]
            profil = son.get("profil_kod", "?")
            skorlar = son.get("skorlar", {})
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#4c1d95,#6366f1);padding:16px 20px;border-radius:14px;
                text-align:center;margin-bottom:12px;">
                <div style="color:#e0e7ff;font-size:0.8rem;">RIASEC Profil Kodu</div>
                <div style="color:#fff;font-weight:900;font-size:2rem;letter-spacing:8px;">{profil}</div>
            </div>""", unsafe_allow_html=True)
            for tip, skor in sorted(skorlar.items(), key=lambda x: x[1], reverse=True):
                ad, _, renk = _HOLLAND_TIPLERI.get(tip, ("?", "?", "#94a3b8"))
                bar_w = round(skor / 3 * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                    <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:8px;
                        font-weight:800;font-size:0.75rem;">{tip}</span>
                    <span style="min-width:100px;font-size:0.72rem;color:#e2e8f0;">{ad.split('(')[0].strip()}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <span style="font-size:0.68rem;color:#64748b;">{skor}/3</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 6. VELİ PSİKO-EĞİTİM & SEMİNER TAKİP
# ════════════════════════════════════════════════════════════

_SEMINER_KONULARI = [
    "Sınav Kaygısı ile Başa Çıkma",
    "Ekran Süresi ve Dijital Bağımlılık",
    "Öfke Kontrolü ve İletişim",
    "Ergenlik Dönemi Rehberliği",
    "Akran Zorbalığı ve Korunma",
    "Motivasyon ve Çalışma Alışkanlıkları",
    "Okul Uyumu ve Sosyal Beceriler",
    "Aile İçi İletişim",
    "Özel Eğitim ve BEP Bilgilendirme",
    "Kariyer Planlama ve Meslek Seçimi",
    "Madde Kullanımı Farkındalığı",
    "İnternet Güvenliği",
    "Beslenme ve Uyku Düzeni",
    "Öz Bakım ve Hijyen",
    "Diğer",
]


def render_veli_psiko_egitim():
    """Veli Psiko-eğitim & Seminer Takip — planlama, yoklama, anket, sertifika."""
    styled_section("Veli Psiko-egitim & Seminer Takip", "#059669")
    styled_info_banner(
        "Veli seminerleri planlama, katilim yoklamasi, geri bildirim anketi, "
        "katilim sertifikasi. MEB Veli Egitim Programi dokumantasyonu otomatik olusur.",
        banner_type="info", icon="👨‍👩‍👧")

    seminerler = _load_json("veli_seminerler.json")
    katilimlar = _load_json("veli_seminer_katilim.json")
    geri_bildirimler = _load_json("veli_seminer_feedback.json")

    # KPI
    toplam = len(seminerler)
    tamamlanan = sum(1 for s in seminerler if s.get("durum") == "Tamamlandi")
    toplam_katilim = sum(len(k.get("katilimcilar", [])) for k in katilimlar)
    ort_memnuniyet = 0
    if geri_bildirimler:
        puanlar = [g.get("puan", 0) for g in geri_bildirimler if g.get("puan")]
        ort_memnuniyet = round(sum(puanlar) / max(len(puanlar), 1), 1)

    styled_stat_row([
        ("Toplam Seminer", str(toplam), "#059669", "📅"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
        ("Toplam Katilim", str(toplam_katilim), "#3b82f6", "👥"),
        ("Memnuniyet", f"{ort_memnuniyet}/5", "#f59e0b" if ort_memnuniyet < 4 else "#10b981", "⭐"),
    ])

    sub = st.tabs(["➕ Yeni Seminer", "📋 Seminer Listesi", "✅ Yoklama", "📊 Geri Bildirim", "🏆 Sertifika"])

    # ── YENİ SEMİNER ──
    with sub[0]:
        styled_section("Yeni Seminer Planla")
        with st.form("vpe_yeni_form"):
            c1, c2 = st.columns(2)
            with c1:
                s_konu = st.selectbox("Konu", _SEMINER_KONULARI, key="vpe_konu")
                s_tarih = st.date_input("Tarih", key="vpe_tarih")
                s_saat = st.time_input("Saat", key="vpe_saat")
            with c2:
                s_konusmaci = st.text_input("Konusmaci", key="vpe_konusmaci")
                s_sure = st.number_input("Sure (dk)", min_value=15, max_value=180, value=60, key="vpe_sure")
                s_hedef = st.multiselect("Hedef Kitle",
                    ["Tum Veliler", "Anaokulu Velileri", "Ilkokul Velileri", "Ortaokul Velileri", "Lise Velileri"],
                    default=["Tum Veliler"], key="vpe_hedef")
            s_konum = st.text_input("Konum", placeholder="Konferans salonu, online link...", key="vpe_konum")
            s_aciklama = st.text_area("Aciklama / Icerik Ozeti", height=80, key="vpe_acik")

            if st.form_submit_button("Semineri Planla", use_container_width=True):
                seminer = {
                    "id": f"sem_{uuid.uuid4().hex[:8]}",
                    "konu": s_konu,
                    "tarih": s_tarih.isoformat(),
                    "saat": str(s_saat),
                    "konusmaci": s_konusmaci,
                    "sure_dk": s_sure,
                    "hedef_kitle": s_hedef,
                    "konum": s_konum,
                    "aciklama": s_aciklama,
                    "durum": "Planlandi",
                    "created_at": datetime.now().isoformat(),
                }
                seminerler.append(seminer)
                _save_json("veli_seminerler.json", seminerler)
                st.success(f"'{s_konu}' semineri planlandi!")
                st.rerun()

    # ── SEMİNER LİSTESİ ──
    with sub[1]:
        styled_section("Seminer Takvimi")
        if not seminerler:
            st.info("Henuz seminer planlanmamis.")
        else:
            for s in sorted(seminerler, key=lambda x: x.get("tarih", ""), reverse=True):
                d_renk = "#10b981" if s.get("durum") == "Tamamlandi" else "#3b82f6" if s.get("durum") == "Planlandi" else "#f59e0b"
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {d_renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{s.get('konu','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{s.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">
                        {s.get('tarih','')[:10]} {s.get('saat','')} — {s.get('konusmaci','')} — {s.get('sure_dk',60)} dk
                    </div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {s.get('id','')}", expanded=False):
                    if s.get("durum") != "Tamamlandi":
                        if st.button("Tamamlandi Isaretle", key=f"vpe_t_{s['id']}"):
                            s["durum"] = "Tamamlandi"
                            _save_json("veli_seminerler.json", seminerler)
                            st.rerun()

    # ── YOKLAMA ──
    with sub[2]:
        styled_section("Katilim Yoklamasi")
        tamamlanan_sem = [s for s in seminerler if s.get("durum") == "Tamamlandi"]
        if not tamamlanan_sem:
            st.info("Tamamlanmis seminer yok.")
        else:
            sec_sem = st.selectbox("Seminer Sec",
                [f"{s.get('konu','')} ({s.get('tarih','')[:10]})" for s in tamamlanan_sem],
                key="vpe_yok_sec")
            sec_idx = [f"{s.get('konu','')} ({s.get('tarih','')[:10]})" for s in tamamlanan_sem].index(sec_sem) if sec_sem else 0
            sem = tamamlanan_sem[sec_idx]

            # Mevcut katilim
            mevcut = next((k for k in katilimlar if k.get("seminer_id") == sem["id"]), None)
            if mevcut:
                st.success(f"Kayitli katilimci: {len(mevcut.get('katilimcilar', []))}")

            with st.form(f"vpe_yok_form_{sem['id']}"):
                veli_list = st.text_area("Katilimci Listesi (her satira bir isim)", height=120,
                    key=f"vpe_yok_list_{sem['id']}")
                if st.form_submit_button("Yoklamayi Kaydet", use_container_width=True):
                    isimler = [i.strip() for i in veli_list.split("\n") if i.strip()]
                    if isimler:
                        if mevcut:
                            mevcut["katilimcilar"] = isimler
                        else:
                            katilimlar.append({
                                "seminer_id": sem["id"],
                                "konu": sem.get("konu", ""),
                                "tarih": sem.get("tarih", ""),
                                "katilimcilar": isimler,
                            })
                        _save_json("veli_seminer_katilim.json", katilimlar)
                        st.success(f"{len(isimler)} katilimci kaydedildi!")

    # ── GERİ BİLDİRİM ──
    with sub[3]:
        styled_section("Veli Geri Bildirim Anketi")
        tamamlanan_sem2 = [s for s in seminerler if s.get("durum") == "Tamamlandi"]
        if not tamamlanan_sem2:
            st.info("Tamamlanmis seminer yok.")
        else:
            sec2 = st.selectbox("Seminer",
                [f"{s.get('konu','')} ({s.get('tarih','')[:10]})" for s in tamamlanan_sem2],
                key="vpe_fb_sec")

            with st.form("vpe_fb_form"):
                fb_veli = st.text_input("Veli Adi", key="vpe_fb_veli")
                fb_puan = st.select_slider("Genel Memnuniyet", options=[1,2,3,4,5], value=4, key="vpe_fb_puan")
                fb_yorum = st.text_area("Yorumunuz", height=60, key="vpe_fb_yorum")
                fb_oneri = st.text_input("Gelecek seminer onerisi", key="vpe_fb_oneri")

                if st.form_submit_button("Gonderim", use_container_width=True):
                    if fb_veli:
                        geri_bildirimler.append({
                            "seminer": sec2,
                            "veli": fb_veli,
                            "puan": fb_puan,
                            "yorum": fb_yorum,
                            "oneri": fb_oneri,
                            "tarih": datetime.now().isoformat(),
                        })
                        _save_json("veli_seminer_feedback.json", geri_bildirimler)
                        st.success("Geri bildiriminiz kaydedildi!")

            # Mevcut feedback
            if geri_bildirimler:
                styled_section("Geri Bildirimler")
                for g in sorted(geri_bildirimler, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                    yildiz = "⭐" * g.get("puan", 0)
                    st.markdown(f"""
                    <div style="padding:8px 12px;margin:4px 0;background:#0f172a;border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:#e2e8f0;font-weight:600;font-size:0.8rem;">{g.get('veli','')}</span>
                            <span style="font-size:0.75rem;">{yildiz}</span>
                        </div>
                        <div style="color:#94a3b8;font-size:0.72rem;">{g.get('seminer','')}</div>
                        <div style="color:#64748b;font-size:0.72rem;margin-top:2px;">{g.get('yorum','')}</div>
                    </div>""", unsafe_allow_html=True)

    # ── SERTİFİKA ──
    with sub[4]:
        styled_section("Katilim Sertifikasi")
        katilimli_sem = [k for k in katilimlar if k.get("katilimcilar")]
        if not katilimli_sem:
            st.info("Katilim kaydi olan seminer yok.")
        else:
            sec3 = st.selectbox("Seminer",
                [f"{k.get('konu','')} ({k.get('tarih','')[:10]}) — {len(k.get('katilimcilar',[]))} kisi" for k in katilimli_sem],
                key="vpe_sert_sec")
            sec3_idx = [f"{k.get('konu','')} ({k.get('tarih','')[:10]}) — {len(k.get('katilimcilar',[]))} kisi" for k in katilimli_sem].index(sec3) if sec3 else 0
            sem_kat = katilimli_sem[sec3_idx]

            st.markdown(f"**{len(sem_kat.get('katilimcilar',[]))} katilimci** icin sertifika:")
            for idx, kisi in enumerate(sem_kat.get("katilimcilar", [])):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:2px 0;
                    background:#05966915;border:1px solid #05966930;border-radius:8px;">
                    <span style="color:#10b981;font-weight:700;font-size:0.8rem;">{idx+1}.</span>
                    <span style="color:#e2e8f0;font-size:0.8rem;">{kisi}</span>
                    <span style="color:#059669;font-size:0.7rem;margin-left:auto;">🏆 Sertifika Hazir</span>
                </div>""", unsafe_allow_html=True)

            st.caption("Sertifika PDF indirme icin 'Sertifikalar' modulunu kullanabilirsiniz.")


# ════════════════════════════════════════════════════════════
# 7. AI ERKEN UYARI & RİSK TAHMİN MOTORU
# ════════════════════════════════════════════════════════════

_RISK_KATEGORILERI = {
    "Akademik": {"renk": "#3b82f6", "ikon": "📚", "kaynaklar": ["not_dusus", "devamsizlik", "odev_eksik"]},
    "Sosyal": {"renk": "#10b981", "ikon": "👥", "kaynaklar": ["catisma", "akran_sorun", "yalnizlik"]},
    "Duygusal": {"renk": "#8b5cf6", "ikon": "🧠", "kaynaklar": ["duygu_dusuk", "kaygi", "motivasyon"]},
    "Davranissal": {"renk": "#f59e0b", "ikon": "⚠️", "kaynaklar": ["davranis_olay", "kural_ihlal", "agresyon"]},
    "Aile": {"renk": "#ef4444", "ikon": "👨‍👩‍👧", "kaynaklar": ["aile_sorun", "ihmal", "siddete_maruz"]},
}

_MUDAHALE_ONERILERI = {
    "Akademik": [
        "Bireysel akademik destek plani olustur",
        "Etut / telafi dersi planla",
        "Ogretmen ile koordinasyon toplantisi",
        "Ogrenci motivasyon gorusmesi",
    ],
    "Sosyal": [
        "Sosyal beceri grubu calismasina dahil et",
        "Akran arabuluculuk programi baslat",
        "Sinif ici gozlem yap",
        "Empati gelistirme etkinlikleri",
    ],
    "Duygusal": [
        "Bireysel gorusme serisi planla",
        "Dijital terapi araclarini ata",
        "Nefes/gevserme egzersizleri oner",
        "Gerekirse RAM'a yonlendir",
    ],
    "Davranissal": [
        "Davranis sozlesmesi olustur",
        "Aile bilgilendirme gorusmesi",
        "Okul kurallarini gozden gecir",
        "Odul/motive sistemi kur",
    ],
    "Aile": [
        "Aile gorusmesi planla (acil)",
        "Sosyal hizmet yonlendirmesi",
        "Gizlilik kapsaminda mudur bilgilendir",
        "Gerekirse yasal bildirim",
    ],
}


def _hesapla_risk_skoru(ogr_id: str) -> dict:
    """Ogrenci icin 5 kategoride risk skoru hesapla (0-100)."""
    duygusal = _load_json("sosyo_duygusal.json")
    davranis = _load_json("davranis_olaylari.json")
    catismalar = _load_json("catisma_kayitlari.json")
    krizler = _load_json("kriz_kayitlari.json")
    kariyer = _load_json("kariyer_profilleri.json")

    iki_hafta = (date.today() - timedelta(days=14)).isoformat()
    bir_ay = (date.today() - timedelta(days=30)).isoformat()

    # Duygusal veriler
    ogr_duygu = [d for d in duygusal if d.get("ogrenci_id") == ogr_id and d.get("tarih", "")[:10] >= iki_hafta]
    duygu_puanlar = [_MOOD_PUAN.get(d.get("duygu", "Normal"), 3) for d in ogr_duygu]
    duygu_ort = sum(duygu_puanlar) / max(len(duygu_puanlar), 1) if duygu_puanlar else 3.0

    # Davranis
    ogr_davranis = [d for d in davranis if d.get("ogrenci_id") == ogr_id and d.get("tarih", "")[:10] >= bir_ay]
    ciddi_dav = sum(1 for d in ogr_davranis if d.get("siddet") in ("Ciddi", "Kritik"))

    # Catisma
    ogr_catisma = [c for c in catismalar
                   if (c.get("taraf1_id") == ogr_id or c.get("taraf2_id") == ogr_id)
                   and c.get("tarih", "")[:10] >= bir_ay]
    acik_catisma = sum(1 for c in ogr_catisma if c.get("durum") in ("Açık", "Tırmanma Riski"))

    # Kriz gecmisi
    ogr_kriz = [k for k in krizler if k.get("ogrenci_id") == ogr_id]
    son_kriz = any(k.get("tarih", "")[:10] >= bir_ay for k in ogr_kriz)

    # Risk skorlari (0-100)
    akademik = min(100, max(0, round((5 - duygu_ort) * 15 + len(ogr_davranis) * 5)))
    sosyal = min(100, max(0, round(len(ogr_catisma) * 20 + acik_catisma * 15)))
    duygusal_skor = min(100, max(0, round((5 - duygu_ort) * 20 + len(ogr_duygu) * 2)))
    davranissal = min(100, max(0, round(len(ogr_davranis) * 12 + ciddi_dav * 20)))
    aile = min(100, max(0, round(30 if son_kriz else 0 + ciddi_dav * 8)))

    genel = round((akademik + sosyal + duygusal_skor + davranissal + aile) / 5)

    return {
        "Akademik": akademik,
        "Sosyal": sosyal,
        "Duygusal": duygusal_skor,
        "Davranissal": davranissal,
        "Aile": aile,
        "Genel": genel,
        "duygu_ort": round(duygu_ort, 1),
        "davranis_sayi": len(ogr_davranis),
        "catisma_sayi": len(ogr_catisma),
        "kriz_gecmis": len(ogr_kriz),
    }


def render_ai_risk_tahmin():
    """AI Erken Uyarı & Risk Tahmin Motoru — 5 kategoride risk profili, radar grafik, müdahale önerisi."""
    styled_section("AI Erken Uyari & Risk Tahmin Motoru", "#dc2626")
    styled_info_banner(
        "Tum modullerden veri toplayarak ogrenci bazli 5 kategoride risk skoru hesaplar. "
        "Otomatik mudahale onerisi + haftalik risk bulteni.",
        banner_type="warning", icon="🤖")

    sub = st.tabs(["🎯 Ogrenci Risk Profili", "📊 Sinif Risk Haritasi", "📋 Haftalik Bulten", "⚙️ Motor Detaylari"])

    # ── ÖĞRENCI RİSK PROFİLİ ──
    with sub[0]:
        styled_section("Bireysel Risk Analizi")
        ogr = _ogrenci_sec("risk_ogr")
        if ogr:
            ogr_id = ogr.get("id", "")
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            skorlar = _hesapla_risk_skoru(ogr_id)
            genel = skorlar["Genel"]
            genel_renk = "#dc2626" if genel >= 60 else "#ef4444" if genel >= 40 else "#f59e0b" if genel >= 20 else "#10b981"
            risk_label = "Kritik" if genel >= 60 else "Yuksek" if genel >= 40 else "Orta" if genel >= 20 else "Dusuk"

            # Hero kart
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a0a0a,{genel_renk}30);border:2px solid {genel_renk};
                border-radius:16px;padding:20px 24px;margin-bottom:16px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                        <div style="color:#94a3b8;font-size:0.8rem;">{ogr.get('sinif','')}/{ogr.get('sube','')}</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:{genel_renk};font-weight:900;font-size:2.5rem;">{genel}</div>
                        <div style="color:{genel_renk};font-weight:700;font-size:0.8rem;">{risk_label} Risk</div>
                    </div>
                </div>
                <div style="color:#64748b;font-size:0.7rem;margin-top:8px;">
                    Duygu Ort: {skorlar['duygu_ort']}/5 | Davranis: {skorlar['davranis_sayi']} olay |
                    Catisma: {skorlar['catisma_sayi']} | Kriz Gecmis: {skorlar['kriz_gecmis']}
                </div>
            </div>""", unsafe_allow_html=True)

            # 5 kategori radar (bar ile)
            styled_section("Kategori Bazli Risk Profili")
            for kat, info in _RISK_KATEGORILERI.items():
                skor = skorlar.get(kat, 0)
                renk = "#dc2626" if skor >= 60 else "#ef4444" if skor >= 40 else "#f59e0b" if skor >= 20 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.1rem;">{info['ikon']}</span>
                    <span style="min-width:90px;font-size:0.8rem;color:#e2e8f0;font-weight:700;">{kat}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{skor}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                            border-radius:6px;display:flex;align-items:center;padding-left:8px;
                            transition:width 0.5s;">
                            <span style="font-size:0.7rem;color:#fff;font-weight:800;">{skor}/100</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Mudahale onerileri
            yuksek_kat = [k for k, v in skorlar.items() if k in _RISK_KATEGORILERI and v >= 30]
            if yuksek_kat:
                styled_section("Onerilen Mudahaleler", "#f59e0b")
                for kat in yuksek_kat:
                    oneriler = _MUDAHALE_ONERILERI.get(kat, [])
                    renk = _RISK_KATEGORILERI[kat]["renk"]
                    st.markdown(f"**{_RISK_KATEGORILERI[kat]['ikon']} {kat}** (Risk: {skorlar[kat]})")
                    for o in oneriler:
                        st.markdown(f"""
                        <div style="display:flex;gap:8px;padding:4px 0;padding-left:12px;border-left:2px solid {renk};">
                            <span style="color:#10b981;">▸</span>
                            <span style="color:#e2e8f0;font-size:0.8rem;">{o}</span>
                        </div>""", unsafe_allow_html=True)
            else:
                st.success("Bu ogrenci icin acil mudahale onerilmemiyor.")

    # ── SINIF RİSK HARİTASI ──
    with sub[1]:
        styled_section("Sinif Bazli Risk Haritasi")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci verisi yok.")
        else:
            ss = get_sinif_sube_listesi()
            siniflar = ["Tümü"] + ss.get("siniflar", [])
            sec_sinif = st.selectbox("Sinif Filtre", siniflar, key="risk_sinif_f")

            filtered = students
            if sec_sinif != "Tümü":
                filtered = [s for s in students if str(s.get("sinif", "")) == sec_sinif]

            if not filtered:
                st.info("Filtraye uyan ogrenci yok.")
            else:
                risk_list = []
                for s in filtered[:50]:  # performans icin 50 ile sinirla
                    sid = s.get("id", "")
                    skorlar = _hesapla_risk_skoru(sid)
                    risk_list.append({
                        "ad": f"{s.get('ad','')} {s.get('soyad','')}",
                        "sinif": s.get("sinif", ""),
                        "sube": s.get("sube", ""),
                        "genel": skorlar["Genel"],
                        "skorlar": skorlar,
                    })

                risk_list.sort(key=lambda x: x["genel"], reverse=True)

                # Ozet
                yuksek_risk = sum(1 for r in risk_list if r["genel"] >= 40)
                orta_risk = sum(1 for r in risk_list if 20 <= r["genel"] < 40)
                dusuk_risk = sum(1 for r in risk_list if r["genel"] < 20)

                styled_stat_row([
                    ("Toplam", str(len(risk_list)), "#3b82f6", "👥"),
                    ("Yuksek Risk", str(yuksek_risk), "#dc2626", "🔴"),
                    ("Orta Risk", str(orta_risk), "#f59e0b", "🟡"),
                    ("Dusuk Risk", str(dusuk_risk), "#10b981", "🟢"),
                ])

                for r in risk_list:
                    g = r["genel"]
                    renk = "#dc2626" if g >= 60 else "#ef4444" if g >= 40 else "#f59e0b" if g >= 20 else "#10b981"
                    label = "KRİTİK" if g >= 60 else "YÜKSEK" if g >= 40 else "ORTA" if g >= 20 else "DÜŞÜK"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:6px 12px;margin:3px 0;
                        background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;min-width:150px;">{r['ad']}</span>
                        <span style="color:#64748b;font-size:0.7rem;min-width:40px;">{r['sinif']}/{r['sube']}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{g}%;height:100%;background:{renk};border-radius:4px;"></div>
                        </div>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:0.65rem;font-weight:800;min-width:50px;text-align:center;">{g} {label}</span>
                    </div>""", unsafe_allow_html=True)

    # ── HAFTALIK BÜLTEN ──
    with sub[2]:
        styled_section("Haftalik Risk Bulteni")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci verisi yok.")
        else:
            all_risks = []
            for s in students[:100]:
                sk = _hesapla_risk_skoru(s.get("id", ""))
                if sk["Genel"] >= 20:
                    all_risks.append({
                        "ad": f"{s.get('ad','')} {s.get('soyad','')}",
                        "sinif": f"{s.get('sinif','')}/{s.get('sube','')}",
                        "genel": sk["Genel"],
                        "en_yuksek": max([(k, v) for k, v in sk.items()
                            if k in _RISK_KATEGORILERI], key=lambda x: x[1], default=("?", 0)),
                    })

            all_risks.sort(key=lambda x: x["genel"], reverse=True)
            tarih_str = date.today().strftime("%d.%m.%Y")
            hafta_bas = (date.today() - timedelta(days=date.today().weekday())).strftime("%d.%m")
            hafta_bit = (date.today() - timedelta(days=date.today().weekday()) + timedelta(days=4)).strftime("%d.%m.%Y")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e293b,#334155);padding:16px 20px;border-radius:14px;
                border:1px solid #475569;margin-bottom:14px;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">📋 Haftalik Risk Bulteni</div>
                <div style="color:#94a3b8;font-size:0.8rem;">{hafta_bas} — {hafta_bit}</div>
                <div style="color:#64748b;font-size:0.75rem;margin-top:4px;">
                    Takip gerektiren: <b style="color:#ef4444;">{len(all_risks)}</b> ogrenci</div>
            </div>""", unsafe_allow_html=True)

            if not all_risks:
                st.success("Bu hafta risk tespit edilen ogrenci yok!")
            else:
                for r in all_risks[:15]:
                    en_kat, en_skor = r["en_yuksek"]
                    renk = _RISK_KATEGORILERI.get(en_kat, {}).get("renk", "#94a3b8")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;
                        background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;min-width:140px;">{r['ad']}</span>
                        <span style="color:#64748b;font-size:0.7rem;min-width:35px;">{r['sinif']}</span>
                        <span style="background:{renk}20;color:{renk};padding:2px 6px;border-radius:4px;
                            font-size:0.65rem;font-weight:700;">{en_kat}: {en_skor}</span>
                        <span style="color:#94a3b8;font-size:0.7rem;margin-left:auto;">Genel: {r['genel']}</span>
                    </div>""", unsafe_allow_html=True)

    # ── MOTOR DETAYLARI ──
    with sub[3]:
        styled_section("Risk Hesaplama Motoru Detaylari")
        for kat, info in _RISK_KATEGORILERI.items():
            with st.expander(f"{info['ikon']} {kat} Riski — Nasil Hesaplaniyor?"):
                st.markdown(f"**Renk:** {info['renk']}")
                st.markdown("**Veri Kaynaklari:**")
                for k in info["kaynaklar"]:
                    st.markdown(f"- {k}")
                st.markdown("**Onerilen Mudahaleler:**")
                for o in _MUDAHALE_ONERILERI.get(kat, []):
                    st.markdown(f"- {o}")


# ════════════════════════════════════════════════════════════
# 8. DİJİTAL TERAPİ ODASI & PSİKOLOJİK DESTEK ARAÇLARI
# ════════════════════════════════════════════════════════════

_NEFES_EGZERSIZLERI = [
    {"ad": "4-7-8 Tekniği", "nefes_al": 4, "tut": 7, "ver": 8, "tekrar": 4,
     "aciklama": "Sakinlesme ve uyku oncesi. 4 sn nefes al, 7 sn tut, 8 sn ver."},
    {"ad": "Kare Nefes", "nefes_al": 4, "tut": 4, "ver": 4, "tekrar": 6,
     "aciklama": "Stres aninda. 4 sn al, 4 sn tut, 4 sn ver, 4 sn bekle."},
    {"ad": "Derin Karin Nefesi", "nefes_al": 5, "tut": 2, "ver": 6, "tekrar": 8,
     "aciklama": "Karindan derin nefes. 5 sn al, 2 sn tut, 6 sn yavasca ver."},
]

_POZITIF_KARTLAR = [
    "Ben degerliyim ve sevilmeye layigim.",
    "Hatalar ogrenmek icin bir firsattir.",
    "Bugün kucuk adimlarla buyuk ilerleme yapabilirim.",
    "Duygularimi hissetmek normaldir ve guvenlidir.",
    "Yardim istemek guc gosterisidir.",
    "Her gun yeni bir baslangictir.",
    "Kendi hizimda ilerlemek yeterlidir.",
    "Zor zamanlari atlatabilirim, daha once de basardim.",
    "Beni seven ve destekleyen insanlar var.",
    "Mukemmel olmak zorunda degilim, iyi olmak yeterli.",
    "Nefes aldigim surece umut var.",
    "Kendime nazik davranmayi hak ediyorum.",
]

_KAYGI_SORULARI = [
    "Son bir haftada ne kadar endiseliydiniz?",
    "Rahatlamakta zorlandınız mı?",
    "Kolayca sinirlendiniz mi?",
    "Kotu bir sey olacaginden korktunuz mu?",
    "Konsantre olmakta zorlandınız mı?",
    "Uyumakta güçlük cektiniz mi?",
    "Kalp carpintisi veya terleme yasadiniz mi?",
]


def render_dijital_terapi_odasi():
    """Dijital Terapi Odası — nefes egzersizi, kaygı ölçeği, duygu günlüğü, pozitif kartlar."""
    styled_section("Dijital Terapi Odasi", "#7c3aed")
    styled_info_banner(
        "Ogrencinin kendi basina kullanabilecegi interaktif psikolojik destek araclari. "
        "Rehber ogretmen arac atayabilir ve kullanim istatistiklerini takip edebilir.",
        banner_type="info", icon="🧘")

    kullanim = _load_json("terapi_kullanim.json")

    sub = st.tabs(["🌬️ Nefes Egzersizi", "📊 Kaygi Olcegi", "🌡️ Ofke Termometresi",
                    "📓 Duygu Gunlugu", "💎 Pozitif Kartlar", "📈 Kullanim Raporu"])

    # ── NEFES EGZERSİZİ ──
    with sub[0]:
        styled_section("Nefes Egzersizleri", "#7c3aed")
        for eg in _NEFES_EGZERSIZLERI:
            with st.expander(f"🌬️ {eg['ad']}", expanded=False):
                st.markdown(f"*{eg['aciklama']}*")
                toplam = (eg["nefes_al"] + eg["tut"] + eg["ver"]) * eg["tekrar"]
                st.markdown(f"**Toplam sure:** ~{toplam} saniye ({eg['tekrar']} tekrar)")

                # Gorsel animasyon
                adimlar = []
                for t in range(eg["tekrar"]):
                    adimlar.append(f"**{t+1}. Tekrar:** 🫁 {eg['nefes_al']}sn nefes al → ⏸️ {eg['tut']}sn tut → 💨 {eg['ver']}sn ver")
                for a in adimlar:
                    st.markdown(a)

                ogr = _ogrenci_sec(f"nef_ogr_{eg['ad']}")
                if ogr and st.button(f"Tamamlandi", key=f"nef_done_{eg['ad']}"):
                    kullanim.append({
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "arac": "Nefes Egzersizi",
                        "detay": eg["ad"],
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json("terapi_kullanim.json", kullanim)
                    st.success("Egzersiz kaydedildi!")

    # ── KAYGI ÖLÇEĞİ ──
    with sub[1]:
        styled_section("Anlik Kaygi Olcegi (GAD-7 Benzeri)")
        ogr = _ogrenci_sec("kaygi_ogr")
        if ogr:
            with st.form("kaygi_form"):
                puanlar = []
                for i, soru in enumerate(_KAYGI_SORULARI):
                    p = st.select_slider(soru,
                        options=["Hic (0)", "Bazen (1)", "Sik (2)", "Her zaman (3)"],
                        key=f"kaygi_{i}")
                    puan_map = {"Hic (0)": 0, "Bazen (1)": 1, "Sik (2)": 2, "Her zaman (3)": 3}
                    puanlar.append(puan_map.get(p, 0))

                if st.form_submit_button("Sonucu Hesapla", use_container_width=True):
                    toplam = sum(puanlar)
                    if toplam <= 4:
                        seviye, renk = "Minimal Kaygi", "#10b981"
                    elif toplam <= 9:
                        seviye, renk = "Hafif Kaygi", "#f59e0b"
                    elif toplam <= 14:
                        seviye, renk = "Orta Kaygi", "#ef4444"
                    else:
                        seviye, renk = "Ciddi Kaygi", "#dc2626"

                    st.markdown(f"""
                    <div style="background:{renk}15;border:2px solid {renk};border-radius:14px;
                        padding:16px 20px;text-align:center;margin:10px 0;">
                        <div style="color:{renk};font-weight:900;font-size:2rem;">{toplam}/21</div>
                        <div style="color:{renk};font-weight:700;font-size:1rem;">{seviye}</div>
                    </div>""", unsafe_allow_html=True)

                    kullanim.append({
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "arac": "Kaygi Olcegi",
                        "detay": f"Puan: {toplam}/21 — {seviye}",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json("terapi_kullanim.json", kullanim)

    # ── ÖFKE TERMOMETRESİ ──
    with sub[2]:
        styled_section("Ofke Termometresi")
        ogr = _ogrenci_sec("ofke_ogr")
        if ogr:
            ofke = st.slider("Ofke seviyenizi secin (0=sakin, 10=patlama noktasi)",
                min_value=0, max_value=10, value=3, key="ofke_slider")
            renk = "#10b981" if ofke <= 3 else "#f59e0b" if ofke <= 6 else "#ef4444" if ofke <= 8 else "#dc2626"
            emoji = "😌" if ofke <= 3 else "😐" if ofke <= 5 else "😤" if ofke <= 7 else "🤬"
            oneri = ("Harika, sakin durumdasiniz." if ofke <= 3
                else "Hafif gerginlik. Derin nefes alin." if ofke <= 5
                else "Ofke yukseliyor. 10'dan geriye sayin, ortamdan uzaklasin." if ofke <= 7
                else "Dikkat! Su icin, yuruyuse cikin. Gerekirse rehber ogretmenle konusun.")

            st.markdown(f"""
            <div style="text-align:center;padding:20px;background:#0f172a;border-radius:16px;
                border:2px solid {renk};margin:10px 0;">
                <div style="font-size:4rem;">{emoji}</div>
                <div style="color:{renk};font-weight:900;font-size:2rem;">{ofke}/10</div>
                <div style="color:#e2e8f0;font-size:0.85rem;margin-top:8px;">{oneri}</div>
            </div>""", unsafe_allow_html=True)

            if st.button("Kaydet", key="ofke_kaydet"):
                kullanim.append({
                    "ogrenci_id": ogr.get("id", ""),
                    "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                    "arac": "Ofke Termometresi",
                    "detay": f"Seviye: {ofke}/10",
                    "tarih": datetime.now().isoformat(),
                })
                _save_json("terapi_kullanim.json", kullanim)
                st.success("Kaydedildi!")

    # ── DUYGU GÜNLÜĞÜ ──
    with sub[3]:
        styled_section("Duygu Gunlugu")
        ogr = _ogrenci_sec("gunluk_ogr")
        if ogr:
            with st.form("gunluk_form"):
                duygu = st.selectbox("Bugun nasil hissediyorsun?", list(_MOOD_EMOJIS.keys()), key="gn_duygu")
                neden = st.text_area("Ne oldu? (opsiyonel)", height=60, key="gn_neden")
                minnettarlik = st.text_input("Bugun minnettar oldugum bir sey:", key="gn_minnet")

                if st.form_submit_button("Gunluge Ekle", use_container_width=True):
                    kullanim.append({
                        "ogrenci_id": ogr.get("id", ""),
                        "ogrenci_ad": f"{ogr.get('ad','')} {ogr.get('soyad','')}",
                        "arac": "Duygu Gunlugu",
                        "detay": f"{_MOOD_EMOJIS.get(duygu,'')} {duygu} — {neden[:50]}",
                        "minnettarlik": minnettarlik,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json("terapi_kullanim.json", kullanim)
                    st.success("Gunluge eklendi!")

    # ── POZİTİF KARTLAR ──
    with sub[4]:
        styled_section("Pozitif Dusunce Kartlari")
        import random
        st.caption("Her tiklayista yeni bir kart!")
        if st.button("Yeni Kart Goster", key="pozitif_btn", use_container_width=True):
            kart = random.choice(_POZITIF_KARTLAR)
            renk = random.choice(["#7c3aed", "#3b82f6", "#10b981", "#f59e0b", "#6366f1", "#059669"])
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{renk}20,{renk}05);border:2px solid {renk};
                border-radius:20px;padding:30px 24px;text-align:center;margin:16px 0;">
                <div style="font-size:2rem;margin-bottom:10px;">💎</div>
                <div style="color:#e2e8f0;font-weight:700;font-size:1.1rem;line-height:1.6;">{kart}</div>
            </div>""", unsafe_allow_html=True)

        styled_section("Tum Kartlar")
        cols = st.columns(2)
        for i, kart in enumerate(_POZITIF_KARTLAR):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #334155;border-radius:10px;
                    padding:10px 14px;margin:4px 0;font-size:0.8rem;color:#94a3b8;">
                    💎 {kart}</div>""", unsafe_allow_html=True)

    # ── KULLANIM RAPORU ──
    with sub[5]:
        styled_section("Arac Kullanim Istatistikleri")
        if not kullanim:
            st.info("Henuz kullanim kaydi yok.")
        else:
            arac_say = Counter(k.get("arac", "?") for k in kullanim)
            toplam_k = len(kullanim)
            styled_stat_row([
                ("Toplam Kullanim", str(toplam_k), "#7c3aed", "📊"),
                ("Farkli Arac", str(len(arac_say)), "#3b82f6", "🧰"),
            ])
            for arac, sayi in arac_say.most_common():
                pct = round(sayi / toplam_k * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:130px;font-size:0.8rem;color:#e2e8f0;font-weight:600;">{arac}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#7c3aed;border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Son kullanimlar
            styled_section("Son Kullanimlar")
            for k in sorted(kullanim, key=lambda x: x.get("tarih",""), reverse=True)[:15]:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 10px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #7c3aed;border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.75rem;min-width:120px;">{k.get('ogrenci_ad','')}</span>
                    <span style="color:#7c3aed;font-size:0.7rem;font-weight:700;">{k.get('arac','')}</span>
                    <span style="color:#64748b;font-size:0.65rem;margin-left:auto;">{k.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 9. AKILLI GRUP ÇALIŞMASI & PSİKO-EĞİTİM GRUBU PLANLAYICI
# ════════════════════════════════════════════════════════════

_HAZIR_PROGRAMLAR = [
    {
        "ad": "Ofke Yonetimi Grubu",
        "oturum": 8,
        "hedef": "Ofke tetikleyicilerini tanimlama, sakinlesme teknikleri, empatik iletisim",
        "ikon": "😤",
        "renk": "#ef4444",
        "planlar": [
            "1. Tanis ve Kural Belirleme",
            "2. Ofkeyi Tanimlama — Bedensel & Duygusal Isaretler",
            "3. Ofke Tetikleyicileri Haritasi",
            "4. Sakinlesme Teknikleri (Nefes, Saymaca)",
            "5. Ben Dili ile Iletisim",
            "6. Empati Gelistirme Canlandirma",
            "7. Problem Cozme Basamaklari",
            "8. Degerlendirme ve Kapanis",
        ],
    },
    {
        "ad": "Sinav Kaygisi Grubu",
        "oturum": 6,
        "hedef": "Sinav kaygisini azaltma, calisma stratejileri, motivasyon",
        "ikon": "😰",
        "renk": "#f59e0b",
        "planlar": [
            "1. Kaygiyi Tanimlama — Normal vs Asiri",
            "2. Bilissel Yapilandirma (Olumsuz Dusunceleri Sorgulama)",
            "3. Gevserme ve Nefes Teknikleri",
            "4. Etkili Calisma Stratejileri",
            "5. Sinav Gunu Plani & Zaman Yonetimi",
            "6. Degerlendirme ve Kapanis",
        ],
    },
    {
        "ad": "Sosyal Beceri Grubu",
        "oturum": 10,
        "hedef": "Iletisim, is birligi, empati, catisma cozumu becerileri",
        "ikon": "🤝",
        "renk": "#10b981",
        "planlar": [
            "1. Tanis ve Grup Kurallari",
            "2. Dinleme Becerileri",
            "3. Kendini Ifade Etme",
            "4. Empati ve Perspektif Alma",
            "5. Is Birligi ve Takim Calismasi",
            "6. Hayir Deme ve Sinir Koyma",
            "7. Catisma Cozme Yollari",
            "8. Akran Baskisina Direnme",
            "9. Dijital Iletisim Etigi",
            "10. Degerlendirme ve Kapanis",
        ],
    },
    {
        "ad": "Ozguven Gelistirme Grubu",
        "oturum": 6,
        "hedef": "Olumlu benlik algisi, guclu yanlari kesfetme, hedef koyma",
        "ikon": "💪",
        "renk": "#6366f1",
        "planlar": [
            "1. Ben Kimim? — Kendini Tanima",
            "2. Guclu Yanlarim ve Basarilarim",
            "3. Olumsuz Ic Sesi Donusturme",
            "4. Hedef Koyma ve Kucuk Zaferler",
            "5. Basarisizlikla Bas Etme",
            "6. Degerlendirme ve Kapanis",
        ],
    },
]


def render_grup_calismasi():
    """Akıllı Grup Çalışması & Psiko-eğitim Grubu Planlayıcı."""
    styled_section("Akilli Grup Calismasi & Psiko-egitim Planlayici", "#059669")
    styled_info_banner(
        "Benzer sorunlari olan ogrencileri otomatik eslestir, hazir programlardan sec, "
        "oturum bazli takip yap. MEB Psiko-egitim Grup Calismasi formu otomatik olusur.",
        banner_type="info", icon="👥")

    gruplar = _load_json("psiko_gruplar.json")
    oturumlar = _load_json("psiko_oturumlar.json")

    # KPI
    aktif_grup = sum(1 for g in gruplar if g.get("durum") == "Aktif")
    toplam_oturum = len(oturumlar)
    toplam_katilimci = sum(len(g.get("uyeler", [])) for g in gruplar)

    styled_stat_row([
        ("Aktif Grup", str(aktif_grup), "#059669", "👥"),
        ("Toplam Oturum", str(toplam_oturum), "#3b82f6", "📅"),
        ("Katilimci", str(toplam_katilimci), "#8b5cf6", "🎓"),
        ("Program", str(len(_HAZIR_PROGRAMLAR)), "#f59e0b", "📋"),
    ])

    sub = st.tabs(["📋 Hazir Programlar", "➕ Yeni Grup", "👥 Aktif Gruplar", "📅 Oturum Takip", "📊 Ilerleme"])

    # ── HAZIR PROGRAMLAR ──
    with sub[0]:
        styled_section("Hazir Psiko-egitim Programlari")
        for prog in _HAZIR_PROGRAMLAR:
            with st.expander(f"{prog['ikon']} {prog['ad']} ({prog['oturum']} oturum)"):
                st.markdown(f"**Hedef:** {prog['hedef']}")
                st.markdown("**Oturum Plani:**")
                for p in prog["planlar"]:
                    st.markdown(f"""
                    <div style="display:flex;gap:8px;padding:4px 0;padding-left:10px;border-left:2px solid {prog['renk']};">
                        <span style="color:{prog['renk']};font-weight:700;">▸</span>
                        <span style="color:#e2e8f0;font-size:0.82rem;">{p}</span>
                    </div>""", unsafe_allow_html=True)

    # ── YENİ GRUP ──
    with sub[1]:
        styled_section("Yeni Grup Olustur")
        with st.form("grup_yeni_form"):
            c1, c2 = st.columns(2)
            with c1:
                g_program = st.selectbox("Program",
                    [f"{p['ikon']} {p['ad']}" for p in _HAZIR_PROGRAMLAR], key="grp_prog")
                g_ad = st.text_input("Grup Adi", placeholder="ornek: 8-A Ofke Yonetimi", key="grp_ad")
                g_lider = st.text_input("Grup Lideri (Rehber Ogretmen)", key="grp_lider")
            with c2:
                g_baslangic = st.date_input("Baslangic", key="grp_bas")
                g_gun = st.selectbox("Oturum Gunu", ["Pazartesi","Sali","Carsamba","Persembe","Cuma"], key="grp_gun")
                g_saat = st.time_input("Oturum Saati", key="grp_saat")

            st.markdown("**Uye Ekle (her satira bir ogrenci adi):**")
            g_uyeler = st.text_area("Uyeler", height=80, key="grp_uyeler")

            if st.form_submit_button("Grubu Olustur", use_container_width=True):
                if g_ad:
                    prog_idx = [f"{p['ikon']} {p['ad']}" for p in _HAZIR_PROGRAMLAR].index(g_program) if g_program else 0
                    secilen = _HAZIR_PROGRAMLAR[prog_idx]
                    uyeler = [u.strip() for u in g_uyeler.split("\n") if u.strip()]
                    grup = {
                        "id": f"grp_{uuid.uuid4().hex[:8]}",
                        "ad": g_ad,
                        "program": secilen["ad"],
                        "program_ikon": secilen["ikon"],
                        "oturum_sayisi": secilen["oturum"],
                        "planlar": secilen["planlar"],
                        "lider": g_lider,
                        "baslangic": g_baslangic.isoformat(),
                        "gun": g_gun,
                        "saat": str(g_saat),
                        "uyeler": uyeler,
                        "tamamlanan_oturum": 0,
                        "durum": "Aktif",
                        "created_at": datetime.now().isoformat(),
                    }
                    gruplar.append(grup)
                    _save_json("psiko_gruplar.json", gruplar)
                    st.success(f"'{g_ad}' grubu {len(uyeler)} uye ile olusturuldu!")
                    st.rerun()

    # ── AKTİF GRUPLAR ──
    with sub[2]:
        styled_section("Aktif Gruplar")
        if not gruplar:
            st.info("Henuz grup olusturulmamis.")
        else:
            for g in gruplar:
                ilerleme = round(g.get("tamamlanan_oturum", 0) / max(g.get("oturum_sayisi", 1), 1) * 100)
                d_renk = "#10b981" if g.get("durum") == "Aktif" else "#64748b"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {d_renk}30;border-left:5px solid {d_renk};
                    border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">
                            {g.get('program_ikon','')} {g.get('ad','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.7rem;font-weight:700;">{g.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.75rem;margin-top:3px;">
                        {g.get('program','')} | {g.get('gun','')} {g.get('saat','')} | {len(g.get('uyeler',[]))} uye
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:10px;margin-top:8px;overflow:hidden;">
                        <div style="width:{ilerleme}%;height:100%;background:#10b981;border-radius:4px;"></div>
                    </div>
                    <div style="color:#64748b;font-size:0.65rem;margin-top:2px;">
                        {g.get('tamamlanan_oturum',0)}/{g.get('oturum_sayisi',0)} oturum (%{ilerleme})</div>
                </div>""", unsafe_allow_html=True)

    # ── OTURUM TAKİP ──
    with sub[3]:
        styled_section("Oturum Kaydi")
        aktif_grp = [g for g in gruplar if g.get("durum") == "Aktif"]
        if not aktif_grp:
            st.info("Aktif grup yok.")
        else:
            sec_grp = st.selectbox("Grup Sec",
                [f"{g.get('program_ikon','')} {g.get('ad','')}" for g in aktif_grp], key="ot_grp")
            sec_idx = [f"{g.get('program_ikon','')} {g.get('ad','')}" for g in aktif_grp].index(sec_grp) if sec_grp else 0
            grp = aktif_grp[sec_idx]

            siradaki = grp.get("tamamlanan_oturum", 0) + 1
            planlar = grp.get("planlar", [])
            if siradaki <= len(planlar):
                st.info(f"Siradaki oturum: **{planlar[siradaki - 1]}**")

            with st.form(f"oturum_form_{grp['id']}"):
                ot_tarih = st.date_input("Oturum Tarihi", key=f"ot_t_{grp['id']}")
                ot_katilim = st.multiselect("Katilimcilar", grp.get("uyeler", []),
                    default=grp.get("uyeler", []), key=f"ot_k_{grp['id']}")
                ot_notlar = st.text_area("Oturum Notlari", height=80, key=f"ot_n_{grp['id']}")
                ot_gozlem = st.text_area("Grup Dinamigi Gozlemleri", height=60, key=f"ot_g_{grp['id']}")

                if st.form_submit_button("Oturumu Kaydet", use_container_width=True):
                    oturum = {
                        "grup_id": grp["id"],
                        "grup_ad": grp.get("ad", ""),
                        "oturum_no": siradaki,
                        "tarih": ot_tarih.isoformat(),
                        "katilimcilar": ot_katilim,
                        "devamsiz": [u for u in grp.get("uyeler", []) if u not in ot_katilim],
                        "notlar": ot_notlar,
                        "gozlem": ot_gozlem,
                        "created_at": datetime.now().isoformat(),
                    }
                    oturumlar.append(oturum)
                    _save_json("psiko_oturumlar.json", oturumlar)
                    grp["tamamlanan_oturum"] = siradaki
                    if siradaki >= grp.get("oturum_sayisi", 0):
                        grp["durum"] = "Tamamlandi"
                    _save_json("psiko_gruplar.json", gruplar)
                    st.success(f"Oturum {siradaki} kaydedildi!")
                    st.rerun()

    # ── İLERLEME ──
    with sub[4]:
        styled_section("Grup Ilerleme Raporu")
        if not gruplar:
            st.info("Henuz grup yok.")
        else:
            for g in gruplar:
                ilerleme = round(g.get("tamamlanan_oturum", 0) / max(g.get("oturum_sayisi", 1), 1) * 100)
                renk = "#10b981" if ilerleme >= 75 else "#f59e0b" if ilerleme >= 40 else "#3b82f6"
                grp_oturumlar = [o for o in oturumlar if o.get("grup_id") == g["id"]]
                ort_katilim = 0
                if grp_oturumlar:
                    ort_katilim = round(sum(len(o.get("katilimcilar", [])) for o in grp_oturumlar)
                                        / len(grp_oturumlar), 1)

                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{g.get('program_ikon','')} {g.get('ad','')}</span>
                    <div style="display:flex;gap:14px;color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                        <span>Ilerleme: <b style="color:{renk};">%{ilerleme}</b></span>
                        <span>Oturum: {g.get('tamamlanan_oturum',0)}/{g.get('oturum_sayisi',0)}</span>
                        <span>Ort. Katilim: {ort_katilim}</span>
                        <span>Uye: {len(g.get('uyeler',[]))}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
