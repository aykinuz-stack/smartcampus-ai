"""
AI Bireysel Eğitim — Zirve Özellikler
=======================================
1. AI Kişisel Öğretmen & Sokratik Diyalog Motoru
2. Akıllı Ödev & Proje Takip Asistanı
3. Dijital İkiz & Öğrenme Simülasyonu
"""
from __future__ import annotations
import json, os, uuid, random, math
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "ai_bireysel"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

_DERSLER = ["Matematik", "Turkce", "Fen Bilimleri", "Sosyal Bilgiler", "Ingilizce",
            "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya"]

_SOKRATIK_SABLONLAR = {
    "anlama_kontrol": [
        "Bu konuyu kendi cumlelerinle ozetleyebilir misin?",
        "Neden bu sonuca ulastigini aciklayabilir misin?",
        "Bu bilgiyi gunluk hayattan bir ornekle iliskilendirebilir misin?",
    ],
    "derinlestirme": [
        "Peki ya tersini dusunursek ne olur?",
        "Bu kural her zaman gecerli mi? Bir istisna dusunebilir misin?",
        "Bu kavram ile {ilgili_konu} arasinda nasil bir baglanti kurarsın?",
    ],
    "zorluk_artir": [
        "Harika! Simdi bir adim daha ileri gidelim...",
        "Bunu cok iyi anlamışsın. Peki bu durumda ne olur?",
        "Mukemmel! Simdi daha zor bir soru: ...",
    ],
    "zorluk_dusur": [
        "Sorun degil, birlikte adim adim ilerleyelim.",
        "Konuyu en basindan alalim. Once su temel kavrama bakalim...",
        "Basit bir ornekle baslayalim...",
    ],
}

_ODEV_ZORLUK = {"Kolay": 1, "Orta": 2, "Zor": 3, "Challenge": 4}
_ODEV_TIPLERI = ["Soru Cozme", "Arastirma", "Ozet Yazma", "Proje", "Sunum Hazirlama",
    "Deney Raporu", "Kitap Okuma", "Video Izleme & Analiz", "Flash Kart Olusturma", "Quiz Hazirlama"]
_ODEV_DURUMLARI = ["Atandi", "Baslandi", "Teslim Edildi", "Degerlendirildi", "Gecikti"]
_ODEV_DURUM_RENK = {"Atandi": "#3b82f6", "Baslandi": "#f59e0b", "Teslim Edildi": "#10b981",
    "Degerlendirildi": "#8b5cf6", "Gecikti": "#ef4444"}

_PROJE_ASAMALARI = ["Konu Belirleme", "Arastirma", "Taslak", "Gelistirme", "Sunum", "Degerlendirme"]


# ════════════════════════════════════════════════════════════
# 1. AI KİŞİSEL ÖĞRETMEN & SOKRATİK DİYALOG
# ════════════════════════════════════════════════════════════

def render_sokratik_ogretmen():
    """AI Kişisel Öğretmen — Sokratik diyalog, seviye adaptasyon, profil hafıza."""
    styled_section("AI Kisisel Ogretmen & Sokratik Diyalog", "#6366f1")
    styled_info_banner(
        "Direkt cevap vermez, sorularla dusundurur. Seviyeye gore adapte olur. "
        "Ogrenci profilini hatirlar, gecmis konulardan devam eder.",
        banner_type="info", icon="🧠")

    diyaloglar = _lj("sokratik_diyaloglar.json")
    ogr_profil = _lj("ai_ogretmen_profil.json")

    styled_stat_row([
        ("Diyalog", str(len(diyaloglar)), "#6366f1", "💬"),
        ("Profil", str(len(ogr_profil)), "#10b981", "👤"),
    ])

    sub = st.tabs(["💬 Sokratik Sohbet", "👤 Ogrenci Hafiza", "📊 Etkilesim Analizi", "⚙️ AI Ayarlari"])

    # ── SOKRATİK SOHBET ──
    with sub[0]:
        styled_section("Sokratik Diyalog Baslat")
        ogr = _ogr_sec("sk_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            with st.form("sokratik_form"):
                c1, c2 = st.columns(2)
                with c1:
                    s_ders = st.selectbox("Ders", _DERSLER, key="sk_ders")
                    s_konu = st.text_input("Konu", key="sk_konu")
                with c2:
                    s_seviye = st.select_slider("Baslangic Seviyesi",
                        options=["Cok Kolay", "Kolay", "Orta", "Zor", "Cok Zor"], value="Orta", key="sk_sev")
                    s_mod = st.selectbox("Diyalog Modu",
                        ["Anlama Kontrol", "Derinlestirme", "Problem Cozme", "Tartisma"], key="sk_mod")

                s_soru = st.text_area("Sorun / Konun", height=80, key="sk_soru",
                    placeholder="Neyi ogrenmek istiyorsun? Nerede takildin?")

                if st.form_submit_button("AI Ogretmenle Konuş", use_container_width=True, type="primary"):
                    if s_konu and s_soru:
                        # Sokratik yanit sec
                        if s_mod == "Anlama Kontrol":
                            sablonlar = _SOKRATIK_SABLONLAR["anlama_kontrol"]
                        elif s_mod == "Derinlestirme":
                            sablonlar = _SOKRATIK_SABLONLAR["derinlestirme"]
                        else:
                            sablonlar = _SOKRATIK_SABLONLAR["anlama_kontrol"] + _SOKRATIK_SABLONLAR["derinlestirme"]

                        yanit = random.choice(sablonlar)

                        # Seviyeye gore adapte
                        if s_seviye in ("Cok Kolay", "Kolay"):
                            adapte = random.choice(_SOKRATIK_SABLONLAR["zorluk_dusur"])
                            yanit = f"{adapte}\n\n{yanit}"
                        elif s_seviye in ("Zor", "Cok Zor"):
                            adapte = random.choice(_SOKRATIK_SABLONLAR["zorluk_artir"])
                            yanit = f"{adapte}\n\n{yanit}"

                        diyalog = {
                            "id": f"sk_{uuid.uuid4().hex[:8]}",
                            "ogrenci": ogr_ad, "ders": s_ders, "konu": s_konu,
                            "soru": s_soru, "yanit": yanit,
                            "seviye": s_seviye, "mod": s_mod,
                            "tarih": datetime.now().isoformat(),
                        }
                        diyaloglar.append(diyalog)
                        _sj("sokratik_diyaloglar.json", diyaloglar)

                        # Profil guncelle
                        mevcut = next((p for p in ogr_profil if p.get("ogrenci") == ogr_ad), None)
                        if mevcut:
                            mevcut.setdefault("konular", []).append(s_konu)
                            mevcut["son_etkilesim"] = datetime.now().isoformat()
                            mevcut["etkilesim_sayisi"] = mevcut.get("etkilesim_sayisi", 0) + 1
                        else:
                            ogr_profil.append({
                                "ogrenci": ogr_ad, "konular": [s_konu],
                                "son_etkilesim": datetime.now().isoformat(),
                                "etkilesim_sayisi": 1, "tercih_seviye": s_seviye,
                            })
                        _sj("ai_ogretmen_profil.json", ogr_profil)

                        # Diyalogu goster
                        st.markdown(f"""
                        <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:16px 20px;margin:10px 0;">
                            <div style="color:#94a3b8;font-size:0.72rem;">🧑‍🎓 {ogr_ad} — {s_ders} / {s_konu}</div>
                            <div style="color:#e2e8f0;font-size:0.85rem;margin-top:6px;padding:10px;
                                background:#1e293b;border-radius:10px;border-left:3px solid #3b82f6;">
                                {s_soru}</div>
                            <div style="color:#6ee7b7;font-size:0.85rem;margin-top:10px;padding:10px;
                                background:#05966910;border-radius:10px;border-left:3px solid #10b981;">
                                🧠 {yanit}</div>
                        </div>""", unsafe_allow_html=True)

            # Son diyaloglar
            ogr_diyalog = [d for d in diyaloglar if d.get("ogrenci") == ogr_ad]
            if ogr_diyalog:
                styled_section(f"Gecmis Diyaloglar ({len(ogr_diyalog)})")
                for d in sorted(ogr_diyalog, key=lambda x: x.get("tarih",""), reverse=True)[:5]:
                    st.markdown(f"""
                    <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                        border-left:3px solid #6366f1;border-radius:0 8px 8px 0;">
                        <span style="color:#94a3b8;font-size:0.68rem;">{d.get('ders','')} / {d.get('konu','')} — {d.get('tarih','')[:10]}</span>
                        <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{d.get('soru','')[:60]}...</div>
                    </div>""", unsafe_allow_html=True)

    # ── ÖĞRENCİ HAFIZA ──
    with sub[1]:
        styled_section("AI Ogretmen Hafizasi — Ogrenci Profilleri")
        if not ogr_profil:
            st.info("Henuz profil yok.")
        else:
            for p in sorted(ogr_profil, key=lambda x: x.get("etkilesim_sayisi",0), reverse=True):
                konular = p.get("konular", [])
                son_3 = konular[-3:] if len(konular) >= 3 else konular
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">🧠 {p.get('ogrenci','')}</span>
                        <span style="color:#6366f1;font-size:0.7rem;font-weight:700;">{p.get('etkilesim_sayisi',0)} etkilesim</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        Son konular: {', '.join(son_3)} | Tercih: {p.get('tercih_seviye','Orta')}</div>
                </div>""", unsafe_allow_html=True)

    # ── ETKİLEŞİM ANALİZİ ──
    with sub[2]:
        styled_section("AI Ogretmen Etkilesim Analizi")
        if not diyaloglar:
            st.info("Diyalog verisi yok.")
        else:
            ders_say = Counter(d.get("ders","") for d in diyaloglar)
            styled_section("Ders Bazli Diyalog")
            for ders, sayi in ders_say.most_common():
                pct = round(sayi / max(len(diyaloglar), 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:120px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#6366f1;border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.55rem;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            mod_say = Counter(d.get("mod","") for d in diyaloglar)
            styled_section("Diyalog Modu Dagilimi")
            for mod, sayi in mod_say.most_common():
                st.markdown(f"  - **{mod}**: {sayi} diyalog")

    # ── AI AYARLARI ──
    with sub[3]:
        styled_section("AI Ogretmen Ayarlari")
        st.markdown("**Sokratik Diyalog Sablonlari:**")
        for kategori, sablonlar in _SOKRATIK_SABLONLAR.items():
            with st.expander(f"📋 {kategori.replace('_',' ').title()} ({len(sablonlar)} sablon)"):
                for s in sablonlar:
                    st.markdown(f"  - 💬 {s}")


# ════════════════════════════════════════════════════════════
# 2. AKILLI ÖDEV & PROJE TAKİP ASİSTANI
# ════════════════════════════════════════════════════════════

def render_odev_asistani():
    """Akıllı Ödev & Proje Takip — AI ödev üretimi, seviye ayarı, proje takip."""
    styled_section("Akilli Odev & Proje Takip Asistani", "#059669")
    styled_info_banner(
        "AI'nin ders bazli kisisellestirmis odev uretter. Seviyeye gore zorluk, "
        "proje bazli uzun vadeli gorev takibi, teslim durumu.",
        banner_type="info", icon="📋")

    odevler = _lj("ai_odevler.json")
    projeler = _lj("ai_projeler.json")

    # KPI
    aktif = sum(1 for o in odevler if o.get("durum") in ("Atandi", "Baslandi"))
    teslim = sum(1 for o in odevler if o.get("durum") == "Teslim Edildi")
    geciken = sum(1 for o in odevler if o.get("durum") == "Gecikti")

    styled_stat_row([
        ("Aktif Odev", str(aktif), "#059669", "📋"),
        ("Teslim", str(teslim), "#10b981", "✅"),
        ("Geciken", str(geciken), "#ef4444", "⏰"),
        ("Proje", str(len(projeler)), "#8b5cf6", "🔨"),
    ])

    sub = st.tabs(["➕ Odev Ata", "📋 Odev Takip", "🔨 Proje Yonetimi", "📊 Performans", "🤖 AI Odev Uret"])

    # ── ÖDEV ATA ──
    with sub[0]:
        styled_section("Yeni Odev Ata")
        with st.form("odev_form"):
            c1, c2 = st.columns(2)
            with c1:
                o_ogr = st.text_input("Ogrenci", key="od_ogr")
                o_ders = st.selectbox("Ders", _DERSLER, key="od_ders")
                o_tip = st.selectbox("Odev Tipi", _ODEV_TIPLERI, key="od_tip")
            with c2:
                o_konu = st.text_input("Konu", key="od_konu")
                o_zorluk = st.selectbox("Zorluk", list(_ODEV_ZORLUK.keys()), key="od_zorluk")
                o_termin = st.date_input("Teslim Tarihi", value=date.today() + timedelta(days=7), key="od_termin")
            o_aciklama = st.text_area("Odev Aciklamasi", height=60, key="od_acik")

            if st.form_submit_button("Odev Ata", use_container_width=True, type="primary"):
                if o_ogr and o_konu:
                    odevler.append({
                        "id": f"od_{uuid.uuid4().hex[:8]}",
                        "ogrenci": o_ogr, "ders": o_ders, "tip": o_tip,
                        "konu": o_konu, "zorluk": o_zorluk,
                        "aciklama": o_aciklama, "termin": o_termin.isoformat(),
                        "durum": "Atandi", "puan": None,
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("ai_odevler.json", odevler)
                    st.success(f"{o_ogr}: {o_ders} — {o_konu} odevi atandi!")
                    st.rerun()

    # ── ÖDEV TAKİP ──
    with sub[1]:
        styled_section("Odev Durumu Takip")
        if not odevler:
            st.info("Odev yok.")
        else:
            # Gecikme kontrolu
            bugun = date.today().isoformat()
            for o in odevler:
                if o.get("durum") in ("Atandi", "Baslandi") and o.get("termin","") < bugun:
                    o["durum"] = "Gecikti"
            _sj("ai_odevler.json", odevler)

            for o in sorted(odevler, key=lambda x: x.get("termin",""), reverse=True)[:15]:
                d_renk = _ODEV_DURUM_RENK.get(o.get("durum",""), "#94a3b8")
                st.markdown(f"""
                <div style="background:#0f172a;border-left:4px solid {d_renk};border-radius:0 10px 10px 0;
                    padding:10px 14px;margin:5px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;">{o.get('ogrenci','')} — {o.get('ders','')}</span>
                        <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                            font-size:0.68rem;font-weight:700;">{o.get('durum','')}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:0.7rem;margin-top:3px;">
                        {o.get('tip','')} | {o.get('konu','')} | Zorluk: {o.get('zorluk','')} | Termin: {o.get('termin','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Islem: {o.get('id','')}", expanded=False):
                    yeni_durum = st.selectbox("Durum", _ODEV_DURUMLARI,
                        index=_ODEV_DURUMLARI.index(o.get("durum","Atandi")) if o.get("durum") in _ODEV_DURUMLARI else 0,
                        key=f"od_d_{o['id']}")
                    o_puan = st.number_input("Puan (0-100)", min_value=0, max_value=100,
                        value=o.get("puan") or 0, key=f"od_p_{o['id']}")
                    if st.button("Guncelle", key=f"od_g_{o['id']}"):
                        o["durum"] = yeni_durum
                        o["puan"] = o_puan if o_puan > 0 else None
                        _sj("ai_odevler.json", odevler)
                        st.rerun()

    # ── PROJE YÖNETİMİ ──
    with sub[2]:
        styled_section("Proje Bazli Gorev Takibi")
        with st.form("proje_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_ad = st.text_input("Proje Adi", key="pj_ad")
                p_ogr = st.text_input("Ogrenci / Takim", key="pj_ogr")
                p_ders = st.selectbox("Ders", _DERSLER, key="pj_ders")
            with c2:
                p_bas = st.date_input("Baslangic", key="pj_bas")
                p_bit = st.date_input("Bitis", key="pj_bit")
            p_aciklama = st.text_area("Proje Aciklamasi", height=50, key="pj_acik")

            if st.form_submit_button("Proje Olustur", use_container_width=True):
                if p_ad:
                    projeler.append({
                        "id": f"pj_{uuid.uuid4().hex[:8]}",
                        "ad": p_ad, "ogrenci": p_ogr, "ders": p_ders,
                        "baslangic": p_bas.isoformat(), "bitis": p_bit.isoformat(),
                        "aciklama": p_aciklama, "asama": "Konu Belirleme",
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("ai_projeler.json", projeler)
                    st.success(f"'{p_ad}' projesi olusturuldu!")
                    st.rerun()

        if projeler:
            for p in projeler:
                asama_idx = _PROJE_ASAMALARI.index(p.get("asama","Konu Belirleme")) if p.get("asama") in _PROJE_ASAMALARI else 0
                ilerleme = round((asama_idx + 1) / len(_PROJE_ASAMALARI) * 100)
                renk = "#10b981" if ilerleme >= 80 else "#f59e0b" if ilerleme >= 40 else "#3b82f6"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">🔨 {p.get('ad','')}</span>
                        <span style="color:{renk};font-weight:700;font-size:0.78rem;">{p.get('asama','')} ({ilerleme}%)</span>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:8px;margin-top:6px;overflow:hidden;">
                        <div style="width:{ilerleme}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <div style="color:#64748b;font-size:0.68rem;margin-top:4px;">
                        {p.get('ogrenci','')} | {p.get('ders','')} | {p.get('baslangic','')[:10]} → {p.get('bitis','')[:10]}</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Asama Guncelle: {p.get('id','')}", expanded=False):
                    yeni = st.selectbox("Asama", _PROJE_ASAMALARI,
                        index=asama_idx, key=f"pj_a_{p['id']}")
                    if st.button("Guncelle", key=f"pj_g_{p['id']}"):
                        p["asama"] = yeni
                        _sj("ai_projeler.json", projeler)
                        st.rerun()

    # ── PERFORMANS ──
    with sub[3]:
        styled_section("Odev Performans Analizi")
        if odevler:
            degerlendirilmis = [o for o in odevler if o.get("puan") is not None]
            if degerlendirilmis:
                ort_puan = round(sum(o["puan"] for o in degerlendirilmis) / len(degerlendirilmis), 1)
                teslim_oran = round(sum(1 for o in odevler if o.get("durum") in ("Teslim Edildi","Degerlendirildi")) / max(len(odevler),1) * 100)

                styled_stat_row([
                    ("Ort Puan", f"{ort_puan}/100", "#10b981" if ort_puan >= 70 else "#f59e0b", "📊"),
                    ("Teslim Orani", f"%{teslim_oran}", "#10b981" if teslim_oran >= 80 else "#f59e0b", "✅"),
                ])

                # Ders bazli
                ders_puan = defaultdict(list)
                for o in degerlendirilmis:
                    ders_puan[o.get("ders","")].append(o["puan"])
                for ders, puanlar in sorted(ders_puan.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
                    ort = round(sum(puanlar) / len(puanlar))
                    renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:120px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{ders}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{ort}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{ort}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Degerlendirilmis odev yok.")
        else:
            st.info("Odev verisi yok.")

    # ── AI ÖDEV ÜRET ──
    with sub[4]:
        styled_section("AI ile Kisisellestirmis Odev Uret")
        ogr = _ogr_sec("od_ai_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            ai_ders = st.selectbox("Ders", _DERSLER, key="od_ai_ders")
            ai_konu = st.text_input("Konu", key="od_ai_konu")

            # Ogrenci seviyesini tahmin et
            ogr_odevler = [o for o in odevler if o.get("ogrenci") == ogr_ad and o.get("puan") is not None]
            ort = round(sum(o["puan"] for o in ogr_odevler) / max(len(ogr_odevler), 1)) if ogr_odevler else 50
            seviye = "Kolay" if ort < 40 else "Orta" if ort < 65 else "Zor" if ort < 85 else "Challenge"

            st.info(f"AI Tahmin: {ogr_ad} icin onerilen zorluk: **{seviye}** (ort puan: {ort})")

            if st.button("AI Odev Uret", use_container_width=True, type="primary") and ai_konu:
                # Seviyeye gore odev tipi sec
                if seviye == "Kolay":
                    tip = random.choice(["Soru Cozme", "Ozet Yazma", "Video Izleme & Analiz"])
                    aciklama = f"{ai_konu} konusunu tekrar et. Temel kavramlari ozetle. 5 kolay soru coz."
                elif seviye == "Orta":
                    tip = random.choice(["Soru Cozme", "Arastirma", "Flash Kart Olusturma"])
                    aciklama = f"{ai_konu} konusunda 10 orta zorluk soru coz. Onemli formulleri flash karta yaz."
                elif seviye == "Zor":
                    tip = random.choice(["Soru Cozme", "Proje", "Quiz Hazirlama"])
                    aciklama = f"{ai_konu} konusunda 8 zor soru + 2 yorum sorusu coz. Konu haritasi cikar."
                else:
                    tip = random.choice(["Proje", "Sunum Hazirlama", "Deney Raporu"])
                    aciklama = f"{ai_konu} konusunda arastirma projesi hazirla. Farkli kaynaklardan karsilastirmali analiz yap."

                odevler.append({
                    "id": f"od_{uuid.uuid4().hex[:8]}",
                    "ogrenci": ogr_ad, "ders": ai_ders, "tip": tip,
                    "konu": ai_konu, "zorluk": seviye,
                    "aciklama": aciklama,
                    "termin": (date.today() + timedelta(days=7)).isoformat(),
                    "durum": "Atandi", "puan": None, "ai_uretim": True,
                    "created_at": datetime.now().isoformat(),
                })
                _sj("ai_odevler.json", odevler)
                st.success(f"AI Odev: {tip} — {seviye} zorluk — {ai_konu}")
                st.markdown(f"**Odev:** {aciklama}")
                st.rerun()


# ════════════════════════════════════════════════════════════
# 3. DİJİTAL İKİZ & ÖĞRENME SİMÜLASYONU
# ════════════════════════════════════════════════════════════

def render_dijital_ikiz():
    """Dijital İkiz — what-if simülasyon, performans projeksiyon, strateji karşılaştırma."""
    styled_section("Dijital Ikiz & Ogrenme Simulasyonu", "#8b5cf6")
    styled_info_banner(
        "Ogrencinin tum verilerinden 'dijital ikiz' olusturur. "
        "What-if senaryolari, gelecek 30 gun projeksiyon, strateji simulasyonu.",
        banner_type="info", icon="🔮")

    calisma_log = _lj("calisma_log.json")
    konu_puanlari = _lj("konu_puanlari.json")
    deneme_sonuclari = _lj("deneme_sonuclari.json")
    quest_log = _lj("quest_log.json")

    sub = st.tabs(["🧬 Dijital Ikiz Profil", "🔮 What-If Senaryo", "📈 30 Gun Projeksiyon", "⚖️ Strateji Karsilastir"])

    # ── DİJİTAL İKİZ PROFİL ──
    with sub[0]:
        styled_section("Dijital Ikiz Olustur")
        ogr = _ogr_sec("di_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            ogr_cal = [c for c in calisma_log if c.get("ogrenci") == ogr_ad]
            ogr_kp = [k for k in konu_puanlari if k.get("ogrenci") == ogr_ad]
            ogr_dn = [d for d in deneme_sonuclari if d.get("ogrenci") == ogr_ad]
            ogr_qst = [q for q in quest_log if q.get("ogrenci") == ogr_ad]

            toplam_dk = sum(c.get("sure_dk", 0) for c in ogr_cal)
            gunluk_ort = round(toplam_dk / max(len(set(c.get("tarih","")[:10] for c in ogr_cal)), 1))
            ders_say = len(set(c.get("ders","") for c in ogr_cal))
            son_deneme = sorted(ogr_dn, key=lambda x: x.get("tarih",""), reverse=True)[0] if ogr_dn else None
            quest_xp = sum(q.get("xp", 0) for q in ogr_qst)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#8b5cf630);border:2px solid #8b5cf6;
                border-radius:20px;padding:24px 28px;margin:10px 0;">
                <div style="text-align:center;">
                    <div style="font-size:2.5rem;">🧬</div>
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;margin-top:4px;">{ogr_ad}</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">Dijital Ikiz Profili</div>
                </div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="color:#8b5cf6;font-weight:900;font-size:1.5rem;">{toplam_dk}</div>
                        <div style="color:#64748b;font-size:0.62rem;">toplam dk</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{gunluk_ort}</div>
                        <div style="color:#64748b;font-size:0.62rem;">gunluk ort dk</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#10b981;font-weight:900;font-size:1.5rem;">{ders_say}</div>
                        <div style="color:#64748b;font-size:0.62rem;">ders</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#f59e0b;font-weight:900;font-size:1.5rem;">{son_deneme.get('toplam_net','?') if son_deneme else '?'}</div>
                        <div style="color:#64748b;font-size:0.62rem;">son net</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#c9a84c;font-weight:900;font-size:1.5rem;">{quest_xp}</div>
                        <div style="color:#64748b;font-size:0.62rem;">XP</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── WHAT-IF SENARYO ──
    with sub[1]:
        styled_section("What-If Senaryo Motoru")
        ogr2 = _ogr_sec("di_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_dn2 = sorted([d for d in deneme_sonuclari if d.get("ogrenci") == ogr_ad2],
                             key=lambda x: x.get("tarih",""), reverse=True)
            ogr_cal2 = [c for c in calisma_log if c.get("ogrenci") == ogr_ad2]

            mevcut_net = ogr_dn2[0].get("toplam_net", 0) if ogr_dn2 else 30
            mevcut_dk = sum(c.get("sure_dk", 0) for c in ogr_cal2)
            gunluk = round(mevcut_dk / max(len(set(c.get("tarih","")[:10] for c in ogr_cal2)), 1)) if ogr_cal2 else 30

            st.markdown(f"**{ogr_ad2}** — Mevcut: {mevcut_net} net, gunluk {gunluk} dk calisma")

            ek_saat = st.slider("Gunluk ek calisma suresi (dk)", 0, 120, 30, step=15, key="di_ek")
            ek_hafta = st.slider("Kac hafta devam edecek?", 1, 16, 8, key="di_hafta")

            if st.button("Simule Et", use_container_width=True, type="primary"):
                # Basit model: her 60dk ek calisma = ~0.5 net artis/hafta
                haftalik_artis = round(ek_saat / 60 * 0.5, 1)
                toplam_artis = round(haftalik_artis * ek_hafta, 1)
                tahmin_net = round(mevcut_net + toplam_artis, 1)

                # Puan tahmini (LGS icin basit)
                mevcut_puan = round(mevcut_net * 5.5)
                tahmin_puan = round(tahmin_net * 5.5)

                renk_m = "#ef4444" if mevcut_puan < 300 else "#f59e0b" if mevcut_puan < 400 else "#10b981"
                renk_t = "#ef4444" if tahmin_puan < 300 else "#f59e0b" if tahmin_puan < 400 else "#10b981"

                st.markdown(f"""
                <div style="display:flex;gap:16px;margin:14px 0;">
                    <div style="flex:1;background:#0f172a;border:2px solid {renk_m};border-radius:16px;padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">Mevcut Tempo</div>
                        <div style="color:{renk_m};font-weight:900;font-size:2rem;">{mevcut_net} net</div>
                        <div style="color:#64748b;font-size:0.7rem;">~{mevcut_puan} puan | {gunluk} dk/gun</div>
                    </div>
                    <div style="display:flex;align-items:center;color:#94a3b8;font-size:1.5rem;">→</div>
                    <div style="flex:1;background:#0f172a;border:2px solid {renk_t};border-radius:16px;padding:16px;text-align:center;">
                        <div style="color:#94a3b8;font-size:0.75rem;">+{ek_saat} dk/gun, {ek_hafta} hafta</div>
                        <div style="color:{renk_t};font-weight:900;font-size:2rem;">{tahmin_net} net</div>
                        <div style="color:#64748b;font-size:0.7rem;">~{tahmin_puan} puan | +{toplam_artis} net artis</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                st.info(f"Haftalik artis: +{haftalik_artis} net | {ek_hafta} haftada toplam: +{toplam_artis} net")

    # ── 30 GÜN PROJEKSİYON ──
    with sub[2]:
        styled_section("Gelecek 30 Gun Performans Projeksiyonu")
        ogr3 = _ogr_sec("di_ogr3")
        if ogr3:
            ogr_ad3 = f"{ogr3.get('ad','')} {ogr3.get('soyad','')}"
            ogr_cal3 = [c for c in calisma_log if c.get("ogrenci") == ogr_ad3]

            if not ogr_cal3:
                st.info("Calisma verisi yok — projeksiyon icin en az 1 hafta veri gerekli.")
            else:
                gunluk_dk = sum(c.get("sure_dk", 0) for c in ogr_cal3)
                gun_say = max(len(set(c.get("tarih","")[:10] for c in ogr_cal3)), 1)
                ort_dk = round(gunluk_dk / gun_say)

                st.markdown(f"**{ogr_ad3}** — Ortalama: {ort_dk} dk/gun")

                for gun in range(0, 31, 5):
                    toplam_tahmini = ort_dk * gun
                    konu_tahmini = toplam_tahmini // 45  # her 45dk = 1 konu
                    renk = "#10b981" if konu_tahmini >= 20 else "#f59e0b" if konu_tahmini >= 10 else "#3b82f6"
                    tarih = (date.today() + timedelta(days=gun)).strftime("%d.%m")

                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:50px;color:#94a3b8;font-size:0.72rem;">+{gun} gun</span>
                        <span style="min-width:45px;color:#64748b;font-size:0.68rem;">{tarih}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{min(konu_tahmini * 3, 100)}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{konu_tahmini} konu</span>
                            </div>
                        </div>
                        <span style="color:#64748b;font-size:0.62rem;">{toplam_tahmini} dk</span>
                    </div>""", unsafe_allow_html=True)

    # ── STRATEJİ KARŞILAŞTIR ──
    with sub[3]:
        styled_section("Calisma Stratejisi Karsilastirma")
        stratejiler = [
            ("Yogun Calisma", "Gunluk 3 saat, haftada 6 gun", 180, 6, "#ef4444"),
            ("Dengeli Plan", "Gunluk 1.5 saat, haftada 5 gun", 90, 5, "#f59e0b"),
            ("Hafif Tempo", "Gunluk 45 dk, haftada 5 gun", 45, 5, "#10b981"),
            ("Sprint Modu", "Gunluk 2 saat, haftada 7 gun (sinav oncesi)", 120, 7, "#8b5cf6"),
        ]

        for ad, aciklama, dk, gun, renk in stratejiler:
            haftalik = dk * gun
            aylik = haftalik * 4
            net_artis = round(haftalik / 60 * 0.5, 1)  # haftalik

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {renk};
                border-radius:0 14px 14px 0;padding:12px 16px;margin:6px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;">{ad}</span>
                        <div style="color:#94a3b8;font-size:0.7rem;">{aciklama}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:{renk};font-weight:900;font-size:1.2rem;">+{net_artis}/hafta</div>
                        <div style="color:#64748b;font-size:0.62rem;">{haftalik} dk/hafta | {aylik} dk/ay</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
