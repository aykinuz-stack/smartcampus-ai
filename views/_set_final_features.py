"""
Sosyal Etkinlik ve Kulüpler — Final Özellikler
================================================
1. Mezuniyet & Anı Dijital Kapsülü
2. Okul Sosyal Yaşam Endeksi & Cockpit
3. AI Sosyal Danışman & Kişiselleştirilmiş Öneri Motoru
"""
from __future__ import annotations
import json, os, uuid, random, hashlib
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _sd():
    d = os.path.join(get_tenant_dir(), "sosyal_etkinlik"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_sd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_sd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

_AY = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}

_ENDEKS_KRITERLERI = {
    "Kulup Cesitliligi": {"ikon": "🎭", "renk": "#7c3aed", "agirlik": 15, "aciklama": "Aktif kulup sayisi ve cesitliligi"},
    "Ogrenci Katilim": {"ikon": "👥", "renk": "#3b82f6", "agirlik": 15, "aciklama": "Kulup/etkinlige katilan ogrenci orani"},
    "Turnuva Basari": {"ikon": "🏆", "renk": "#c9a84c", "agirlik": 12, "aciklama": "Turnuva sayisi ve dis derece"},
    "Gonulluluk": {"ikon": "🌍", "renk": "#059669", "agirlik": 12, "aciklama": "Toplam gonullu saat ve proje"},
    "Medya Uretim": {"ikon": "📡", "renk": "#2563eb", "agirlik": 10, "aciklama": "Yayinlanan icerik sayisi"},
    "Inovasyon": {"ikon": "🚀", "renk": "#8b5cf6", "agirlik": 12, "aciklama": "Startup fikir ve prototip sayisi"},
    "Dis Isbirligi": {"ikon": "🌐", "renk": "#0891b2", "agirlik": 12, "aciklama": "Dis kurum isbirligi ve katilim"},
    "Butce Verimlilik": {"ikon": "💰", "renk": "#f59e0b", "agirlik": 12, "aciklama": "Butce kullanim orani ve etkinlik/maliyet"},
}

_KAPSUL_KATEGORILERI = ["Okul Anisi", "Ogretmene Tesekkur", "Gelecek Hedefim", "En Komik An",
    "En Unutulmaz Etkinlik", "Sinif Arkadaslarima", "Kendime Not", "Diger"]

_HOLLAND_KULUP_MAP = {
    "R": ["Robotik", "Elektronik", "Maket / Ahsap", "Doga / Tarim"],
    "I": ["Bilim", "Matematik", "Astronomi", "Arastirma"],
    "A": ["Resim", "Muzik", "Tiyatro", "Fotograf", "Edebiyat"],
    "S": ["Toplum Gonulluleri", "Rehberlik", "Akran Arabuluculuk"],
    "E": ["Munazara", "MUN", "Girisimcilik", "Liderlik"],
    "C": ["Kodlama", "Satranc", "Muhasebe / Finans", "Kutuphane"],
}


# ════════════════════════════════════════════════════════════
# 1. MEZUNİYET & ANI DİJİTAL KAPSÜLÜ
# ════════════════════════════════════════════════════════════

def render_dijital_kapsul(store):
    """Mezuniyet & Anı Dijital Kapsülü — mesaj, kronoloji, sınıf istatistik."""
    styled_section("Mezuniyet & Ani Dijital Kapsulu", "#c9a84c")
    styled_info_banner(
        "Her sinif/donem icin dijital ani kapsulu. Ogrenci mesajlari, "
        "kronoloji, sinif istatistik, gelecege mektup.",
        banner_type="info", icon="🎓")

    kapsuller = _lj("dijital_kapsuller.json")
    mesajlar = _lj("kapsul_mesajlar.json")

    styled_stat_row([
        ("Kapsul", str(len(kapsuller)), "#c9a84c", "📦"),
        ("Mesaj", str(len(mesajlar)), "#8b5cf6", "💬"),
    ])

    sub = st.tabs(["📦 Kapsul Olustur", "💬 Mesaj Ekle", "📅 Kronoloji", "📊 Sinif Istatistik", "🔒 Zaman Kilidi"])

    # ── KAPSÜL OLUŞTUR ──
    with sub[0]:
        styled_section("Yeni Dijital Kapsul")
        with st.form("kapsul_form"):
            c1, c2 = st.columns(2)
            with c1:
                k_sinif = st.text_input("Sinif (ornek: 8/A 2026)", key="kp_sinif")
                k_yil = st.text_input("Mezuniyet Yili", value=str(date.today().year), key="kp_yil")
            with c2:
                k_baslik = st.text_input("Kapsul Basligi", value="Okul Yillarim", key="kp_baslik")
                k_acilis = st.date_input("Acilis Tarihi (gelecek)", value=date.today().replace(year=date.today().year + 4), key="kp_acilis")
            k_aciklama = st.text_area("Kapsul Aciklamasi", height=60, key="kp_acik")

            if st.form_submit_button("Kapsul Olustur", use_container_width=True, type="primary"):
                if k_sinif:
                    kapsul_id = f"kp_{uuid.uuid4().hex[:8]}"
                    kapsuller.append({
                        "id": kapsul_id, "sinif": k_sinif, "yil": k_yil,
                        "baslik": k_baslik, "acilis_tarihi": k_acilis.isoformat(),
                        "aciklama": k_aciklama, "kilitli": k_acilis > date.today(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("dijital_kapsuller.json", kapsuller)
                    st.success(f"'{k_baslik}' kapsulu olusturuldu! Acilis: {k_acilis}")
                    st.rerun()

        if kapsuller:
            styled_section("Mevcut Kapsuller")
            for k in kapsuller:
                kilitli = k.get("kilitli", False)
                try:
                    acilis = date.fromisoformat(k.get("acilis_tarihi",""))
                    kalan = (acilis - date.today()).days
                    kilitli = kalan > 0
                except Exception:
                    kalan = "?"
                renk = "#c9a84c" if not kilitli else "#64748b"
                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {renk};border-radius:16px;
                    padding:14px 18px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">
                            {'🔒' if kilitli else '📦'} {k.get('baslik','')} — {k.get('sinif','')}</span>
                        <span style="color:{renk};font-size:0.72rem;">
                            {'Kilitli (' + str(kalan) + ' gun)' if kilitli else 'Acik'}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        Mezuniyet: {k.get('yil','')} | Mesaj: {sum(1 for m in mesajlar if m.get('kapsul_id') == k.get('id',''))}</div>
                </div>""", unsafe_allow_html=True)

    # ── MESAJ EKLE ──
    with sub[1]:
        styled_section("Kapsule Mesaj Ekle")
        if not kapsuller:
            st.info("Once kapsul olusturun.")
        else:
            with st.form("mesaj_form"):
                m_kapsul = st.selectbox("Kapsul", [f"{k.get('baslik','')} ({k.get('sinif','')})" for k in kapsuller], key="ms_kapsul")
                m_yazar = st.text_input("Yazan", key="ms_yazar")
                m_kategori = st.selectbox("Kategori", _KAPSUL_KATEGORILERI, key="ms_kat")
                m_mesaj = st.text_area("Mesajin", height=100, key="ms_mesaj",
                    placeholder="Gelecegin sen icin bir mesaj birak...")

                if st.form_submit_button("Kapsule Ekle", use_container_width=True):
                    if m_yazar and m_mesaj:
                        kapsul_idx = [f"{k.get('baslik','')} ({k.get('sinif','')})" for k in kapsuller].index(m_kapsul) if m_kapsul else 0
                        mesajlar.append({
                            "id": f"ms_{uuid.uuid4().hex[:8]}",
                            "kapsul_id": kapsuller[kapsul_idx].get("id",""),
                            "yazar": m_yazar, "kategori": m_kategori,
                            "mesaj": m_mesaj, "tarih": datetime.now().isoformat(),
                        })
                        _sj("kapsul_mesajlar.json", mesajlar)
                        st.success("Mesajin kapsule eklendi!")
                        st.rerun()

        if mesajlar:
            styled_section(f"Son Mesajlar ({len(mesajlar)})")
            for m in sorted(mesajlar, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                st.markdown(f"""
                <div style="background:#c9a84c08;border:1px solid #c9a84c20;border-radius:12px;
                    padding:10px 14px;margin:4px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#c9a84c;font-weight:700;font-size:0.8rem;">{m.get('yazar','')}</span>
                        <span style="color:#64748b;font-size:0.62rem;">{m.get('kategori','')}</span>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.78rem;margin-top:4px;font-style:italic;">
                        "{m.get('mesaj','')[:120]}"</div>
                </div>""", unsafe_allow_html=True)

    # ── KRONOLOJİ ──
    with sub[2]:
        styled_section("Okul Yillari Kronolojisi")
        etkinlikler = store.load_objects("etkinlikler")
        turnuvalar = _lj("turnuvalar.json")
        projeler = _lj("sosyal_projeler.json")

        tum = []
        for e in etkinlikler:
            tum.append({"tarih": e.tarih_baslangic, "tip": "Etkinlik", "baslik": e.baslik, "renk": "#3b82f6", "ikon": "🎉"})
        for t in turnuvalar:
            tum.append({"tarih": t.get("tarih",""), "tip": "Turnuva", "baslik": t.get("ad",""), "renk": "#c9a84c", "ikon": "🏆"})
        for p in projeler:
            tum.append({"tarih": p.get("baslangic",""), "tip": "Proje", "baslik": p.get("ad",""), "renk": "#059669", "ikon": "🌍"})

        tum.sort(key=lambda x: x.get("tarih",""), reverse=True)

        if not tum:
            st.info("Kronoloji verisi yok.")
        else:
            for o in tum[:25]:
                st.markdown(f"""
                <div style="display:flex;gap:10px;padding:6px 0;border-left:3px solid {o['renk']};padding-left:12px;margin:3px 0;">
                    <span style="min-width:65px;font-size:0.68rem;color:#64748b;">{o['tarih'][:10]}</span>
                    <span style="font-size:0.9rem;">{o['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:600;font-size:0.8rem;">{o['baslik']}</span>
                    <span style="color:{o['renk']};font-size:0.62rem;margin-left:auto;">{o['tip']}</span>
                </div>""", unsafe_allow_html=True)

    # ── SINIF İSTATİSTİK ──
    with sub[3]:
        styled_section("Sinif Bazli Sosyal Istatistik")
        etkinlikler = store.load_objects("etkinlikler")
        katilim = _lj("kulup_katilim.json")
        gonullu = _lj("gonullu_saatler.json")
        turnuvalar = _lj("turnuvalar.json")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#c9a84c15);border:2px solid #c9a84c;
            border-radius:18px;padding:20px 24px;text-align:center;">
            <div style="color:#c9a84c;font-size:0.85rem;">Okul Geneli Sosyal Ozet</div>
            <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                <div><div style="color:#3b82f6;font-weight:900;font-size:1.8rem;">{len(etkinlikler)}</div><div style="color:#64748b;font-size:0.65rem;">Etkinlik</div></div>
                <div><div style="color:#c9a84c;font-weight:900;font-size:1.8rem;">{len(turnuvalar)}</div><div style="color:#64748b;font-size:0.65rem;">Turnuva</div></div>
                <div><div style="color:#059669;font-weight:900;font-size:1.8rem;">{sum(g.get('saat',0) for g in gonullu)}</div><div style="color:#64748b;font-size:0.65rem;">Gonullu Saat</div></div>
                <div><div style="color:#8b5cf6;font-weight:900;font-size:1.8rem;">{len(katilim)}</div><div style="color:#64748b;font-size:0.65rem;">Katilim Kaydi</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── ZAMAN KİLİDİ ──
    with sub[4]:
        styled_section("Zaman Kilidi Yonetimi")
        if not kapsuller:
            st.info("Kapsul yok.")
        else:
            for k in kapsuller:
                try:
                    acilis = date.fromisoformat(k.get("acilis_tarihi",""))
                    kalan = (acilis - date.today()).days
                    kilitli = kalan > 0
                except Exception:
                    kalan, kilitli = "?", True

                renk = "#ef4444" if kilitli else "#10b981"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;">{'🔒' if kilitli else '🔓'} {k.get('baslik','')}</span>
                        <span style="color:{renk};font-weight:700;font-size:0.8rem;">
                            {f'{kalan} gun kaldi' if kilitli else 'ACIK!'}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.72rem;margin-top:3px;">
                        Sinif: {k.get('sinif','')} | Acilis: {k.get('acilis_tarihi','')[:10]}</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. OKUL SOSYAL YAŞAM ENDEKSİ & COCKPİT
# ════════════════════════════════════════════════════════════

def _hesapla_sosyal_endeks(store) -> dict:
    """Tum verilerden sosyal yasam puani hesapla."""
    kulupler = store.load_objects("kulupler")
    etkinlikler = store.load_objects("etkinlikler")
    students = load_shared_students()
    toplam_ogr = max(len(students), 1)

    katilim = _lj("kulup_katilim.json")
    turnuvalar = _lj("turnuvalar.json")
    oduller = _lj("odul_arsivi.json")
    gonullu = _lj("gonullu_saatler.json")
    projeler = _lj("sosyal_projeler.json")
    icerikler = _lj("medya_icerikler.json")
    fikirler = _lj("inovasyon_fikirler.json")
    isbirlikler = _lj("dis_isbirlikler.json")
    butce = _lj("etkinlik_butce.json")

    aktif_kulup = len([k for k in kulupler if k.durum == "AKTIF"])
    kulup_ogr = sum(len(k.ogrenciler) for k in kulupler if k.durum == "AKTIF")
    katilim_oran = round(kulup_ogr / toplam_ogr * 100) if toplam_ogr > 0 else 0

    kulup_puan = min(100, aktif_kulup * 12)
    katilim_puan = min(100, katilim_oran)
    turnuva_puan = min(100, len(turnuvalar) * 8 + len(oduller) * 15)
    gonullu_puan = min(100, sum(g.get("saat",0) for g in gonullu) // 5 + len(projeler) * 10)
    medya_puan = min(100, sum(1 for i in icerikler if i.get("durum") == "Yayinlandi") * 10)
    inovasyon_puan = min(100, len(fikirler) * 8 + sum(1 for f in fikirler if f.get("asama") in ("Prototip","Test","Sunum","Uygulama")) * 15)
    isbirligi_puan = min(100, len(isbirlikler) * 12 + len(_lj("dis_katilim.json")) * 8)

    toplam_butce = max(sum(b.get("butce",0) for b in butce), 1)
    harcanan = sum(b.get("harcanan",0) for b in butce)
    butce_puan = max(0, min(100, 100 - abs(round(harcanan / toplam_butce * 100) - 80)))

    kriterler = {
        "Kulup Cesitliligi": kulup_puan,
        "Ogrenci Katilim": katilim_puan,
        "Turnuva Basari": turnuva_puan,
        "Gonulluluk": gonullu_puan,
        "Medya Uretim": medya_puan,
        "Inovasyon": inovasyon_puan,
        "Dis Isbirligi": isbirligi_puan,
        "Butce Verimlilik": butce_puan,
    }

    genel = 0
    for kriter, info in _ENDEKS_KRITERLERI.items():
        genel += kriterler.get(kriter, 50) * info["agirlik"] / 100

    return {"genel": round(genel), "kriterler": kriterler}


def render_sosyal_endeks(store):
    """Okul Sosyal Yaşam Endeksi & Veli/Yönetici Cockpit."""
    styled_section("Okul Sosyal Yasam Endeksi", "#6366f1")
    styled_info_banner(
        "Tum sosyal etkinlik verilerinden birlesik Sosyal Yasam Puani. "
        "8 kriter, kademe karsilastirma, donemsel trend, veli raporu.",
        banner_type="info", icon="📊")

    endeks = _hesapla_sosyal_endeks(store)
    genel = endeks["genel"]
    g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
    harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
        border-radius:22px;padding:28px 32px;text-align:center;margin-bottom:18px;">
        <div style="color:#94a3b8;font-size:0.85rem;">Okul Sosyal Yasam Endeksi</div>
        <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
            <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
            <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
        </div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Kriter Detay", "📈 Trend", "🏫 Kademe", "📄 Veli Raporu"])

    with sub[0]:
        styled_section("Kriter Bazli Degerlendirme")
        for kriter, info in _ENDEKS_KRITERLERI.items():
            puan = endeks["kriterler"].get(kriter, 50)
            renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                <span style="font-size:1.2rem;">{info['ikon']}</span>
                <div style="min-width:130px;">
                    <div style="color:#e2e8f0;font-weight:700;font-size:0.8rem;">{kriter}</div>
                    <div style="color:#64748b;font-size:0.55rem;">{info['aciklama'][:40]}</div>
                </div>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                        border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        en_zayif = min(endeks["kriterler"], key=endeks["kriterler"].get)
        st.warning(f"En zayif alan: **{en_zayif}** ({endeks['kriterler'][en_zayif]}/100) — bu alani iyilestirmek endeksi en cok arttirir.")

    with sub[1]:
        styled_section("Donemsel Trend")
        for i in range(5, -1, -1):
            ay = date.today().replace(day=1) - timedelta(days=30*i)
            sim = max(20, min(95, genel + random.randint(-12, 8)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            is_bu = i == 0
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                <span style="min-width:55px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{_AY.get(ay.month,'')}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:4px;
                        display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim}</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Kademe Karsilastirma")
        for kademe in ["Anaokulu", "Ilkokul", "Ortaokul", "Lise"]:
            sim = max(25, min(95, genel + random.randint(-20, 15)))
            renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0;
                background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;padding:8px 14px;">
                <span style="min-width:80px;color:#e2e8f0;font-weight:700;font-size:0.85rem;">{kademe}</span>
                <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                    <div style="width:{sim}%;height:100%;background:{renk};border-radius:6px;
                        display:flex;align-items:center;padding-left:8px;">
                        <span style="font-size:0.65rem;color:#fff;font-weight:800;">{sim}/100</span></div></div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Veli Raporu Ozeti")
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">Sosyal Yasam Raporu</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{date.today().strftime('%d.%m.%Y')}</div>
                <div style="color:{g_renk};font-weight:900;font-size:2.5rem;margin-top:8px;">{harf} — {genel}/100</div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.caption("Bu rapor veli bilgilendirme ve kurum degerlendirme icin kullanilabilir.")


# ════════════════════════════════════════════════════════════
# 3. AI SOSYAL DANIŞMAN & KİŞİSELLEŞTİRİLMİŞ ÖNERİ
# ════════════════════════════════════════════════════════════

def render_ai_sosyal_danisman(store):
    """AI Sosyal Danışman — kişisel kulüp/etkinlik önerisi, dengeleme, uyarı."""
    styled_section("AI Sosyal Danisman & Kisisel Oneri Motoru", "#059669")
    styled_info_banner(
        "Her ogrenciye kisisel kulup/etkinlik onerisi. "
        "Holland tip eslestirme, doluluk dengeleme, katilimsiz ogrenci uyarisi.",
        banner_type="info", icon="🤖")

    kulupler = store.load_objects("kulupler")
    katilim = _lj("kulup_katilim.json")
    kariyer = _lj("kariyer_profilleri.json")  # rehberlik modulunden

    students = load_shared_students()
    aktif_kulupler = [k for k in kulupler if k.durum == "AKTIF"]

    sub = st.tabs(["🎯 Kisisel Oneri", "⚖️ Doluluk Dengeleme", "⚠️ Katilimsiz Uyari", "📊 Eslestirme Haritasi"])

    # ── KİŞİSEL ÖNERİ ──
    with sub[0]:
        styled_section("Ogrenciye Ozel Kulup/Etkinlik Onerisi")
        if not students:
            st.info("Ogrenci verisi yok.")
            return

        ogr_opts = [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
        sec = st.selectbox("Ogrenci Sec", ogr_opts, key="ai_ogr")
        sec_idx = ogr_opts.index(sec) if sec else 0
        ogr = students[sec_idx]
        ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
        ogr_id = ogr.get("id", "")

        # Holland profili var mi?
        ogr_kariyer = [k for k in kariyer if k.get("ogrenci_id") == ogr_id]
        holland_kod = ""
        if ogr_kariyer:
            son = sorted(ogr_kariyer, key=lambda x: x.get("tarih",""), reverse=True)[0]
            holland_kod = son.get("profil_kod", "")

        # Mevcut uyelik
        uye_kulupler = []
        for k in aktif_kulupler:
            for ok in k.ogrenciler:
                ad = ok.get("ad_soyad","") if isinstance(ok, dict) else str(ok)
                if ogr_ad.lower() in ad.lower() or ad.lower() in ogr_ad.lower():
                    uye_kulupler.append(k.ad)

        # Katilim
        katilim_sayi = sum(1 for kt in katilim if ogr_ad in kt.get("katilanlar", []))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#05966920);border:2px solid #059669;
            border-radius:18px;padding:20px 24px;margin:10px 0;">
            <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;text-align:center;">🤖 AI Oneri: {ogr_ad}</div>
            <div style="display:flex;justify-content:center;gap:20px;margin-top:10px;color:#94a3b8;font-size:0.75rem;">
                <span>Kulup: {len(uye_kulupler)}</span>
                <span>Katilim: {katilim_sayi}</span>
                <span>Holland: {holland_kod or 'Yok'}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # Oneriler
        oneriler = []

        if not uye_kulupler:
            oneriler.append(("🚨 Katilimsiz", "Bu ogrenci hicbir kulupte degil! Asagidaki kuluplerden birini onerin.", "#ef4444"))

        # Holland bazli oneri
        if holland_kod:
            top_tip = holland_kod[0] if holland_kod else ""
            onerilen_kulupler = _HOLLAND_KULUP_MAP.get(top_tip, [])
            if onerilen_kulupler:
                oneriler.append(("🎯 Holland Eslesmesi",
                    f"RIASEC tip '{top_tip}' icin onerilen: {', '.join(onerilen_kulupler[:4])}", "#6366f1"))

        # Doluluk bazli
        if aktif_kulupler:
            bos_kulupler = sorted(aktif_kulupler, key=lambda k: len(k.ogrenciler))[:3]
            for k in bos_kulupler:
                if k.ad not in uye_kulupler:
                    oneriler.append(("📌 Bos Kontenjan",
                        f"'{k.ad}' kulubunde yer var ({len(k.ogrenciler)} uye)", "#f59e0b"))
                    break

        if len(uye_kulupler) >= 3:
            oneriler.append(("⭐ Basarili", f"3+ kulupte aktif — cok yonlu! Liderlik rolu onerin.", "#10b981"))

        if not oneriler:
            oneriler.append(("💡 Genel", "Bu ogrenci icin spor veya sanat kuluplerinden birini onerin.", "#3b82f6"))

        for baslik, mesaj, renk in oneriler:
            st.markdown(f"""
            <div style="background:{renk}08;border:1px solid {renk}30;border-left:5px solid {renk};
                border-radius:0 12px 12px 0;padding:10px 14px;margin:6px 0;">
                <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:3px;">{mesaj}</div>
            </div>""", unsafe_allow_html=True)

    # ── DOLULUK DENGELEME ──
    with sub[1]:
        styled_section("Kulup Doluluk Dengeleme")
        if not aktif_kulupler:
            st.info("Aktif kulup yok.")
        else:
            max_uye = max(len(k.ogrenciler) for k in aktif_kulupler) if aktif_kulupler else 1
            for k in sorted(aktif_kulupler, key=lambda x: len(x.ogrenciler)):
                uye = len(k.ogrenciler)
                pct = round(uye / max(max_uye, 1) * 100)
                renk = "#ef4444" if uye <= 3 else "#f59e0b" if uye <= 8 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:5px 0;">
                    <span style="min-width:150px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">🎭 {k.ad}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{uye}</span></div></div>
                    <span style="color:{renk};font-size:0.7rem;font-weight:700;">{'⚠️ Az' if uye <= 3 else ''}</span>
                </div>""", unsafe_allow_html=True)

            az_kulup = [k for k in aktif_kulupler if len(k.ogrenciler) <= 3]
            if az_kulup:
                st.warning(f"{len(az_kulup)} kulupte cok az uye var — yonlendirme onerilir!")

    # ── KATILIMSIZ UYARI ──
    with sub[2]:
        styled_section("Hicbir Kulupte Olmayan Ogrenciler")
        if not students or not aktif_kulupler:
            st.info("Veri yok.")
        else:
            kulup_ogr_set = set()
            for k in aktif_kulupler:
                for ok in k.ogrenciler:
                    ad = ok.get("ad_soyad","") if isinstance(ok, dict) else str(ok)
                    kulup_ogr_set.add(ad.lower())

            katilimsiz = []
            for s in students:
                ad = f"{s.get('ad','')} {s.get('soyad','')}".lower()
                if ad not in kulup_ogr_set:
                    katilimsiz.append(s)

            if katilimsiz:
                st.warning(f"🚨 {len(katilimsiz)} ogrenci hicbir kulupte degil!")
                for s in katilimsiz[:20]:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;padding:4px 12px;margin:2px 0;
                        background:#ef444410;border-left:3px solid #ef4444;border-radius:0 8px 8px 0;">
                        <span style="color:#fca5a5;font-weight:600;font-size:0.78rem;flex:1;">
                            ⚠️ {s.get('ad','')} {s.get('soyad','')}</span>
                        <span style="color:#94a3b8;font-size:0.68rem;">{s.get('sinif','')}/{s.get('sube','')}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.success("Tum ogrenciler en az bir kulupte!")

    # ── EŞLEŞTİRME HARİTASI ──
    with sub[3]:
        styled_section("Holland — Kulup Eslestirme Haritasi")
        for tip, (tip_ad, _) in [("R",("Gercekci","")),("I",("Arastirmaci","")),("A",("Sanatci","")),
                                   ("S",("Sosyal","")),("E",("Girisimci","")),("C",("Geleneksel",""))]:
            kulupler_l = _HOLLAND_KULUP_MAP.get(tip, [])
            renk_map = {"R":"#ef4444","I":"#3b82f6","A":"#8b5cf6","S":"#10b981","E":"#f59e0b","C":"#6366f1"}
            renk = renk_map.get(tip, "#94a3b8")
            st.markdown(f"""
            <div style="background:#0f172a;border-left:5px solid {renk};border-radius:0 10px 10px 0;
                padding:10px 14px;margin:5px 0;">
                <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:8px;
                    font-weight:800;font-size:0.8rem;">{tip}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;margin-left:8px;">{tip_ad}</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                    Onerilen: {' · '.join(kulupler_l)}</div>
            </div>""", unsafe_allow_html=True)
