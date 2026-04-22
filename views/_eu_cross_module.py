"""
Erken Uyari - Cross-Module Super Features
==========================================
1. Mezun Basari Haritasi & Etki Puani
2. Moduller Arasi Cross-Alert & Kurumsal Saglik Skoru
3. AI Kariyer Pusula (mezun veri madenciligi)
"""
from __future__ import annotations

import streamlit as st
from datetime import datetime, date
from collections import Counter
import json, os

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ── Yardımcı: JSON yükleyici ──
def _load_json_safe(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _get_tenant_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. MEZUN BAŞARI HARİTASI & ETKİ PUANI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_basari_haritasi(store, loader):
    styled_section("🗺️ Mezun Başarı Haritası & Etki Puanı", "#2563eb")
    styled_info_banner(
        "Mezun verilerinden oluşturulan başarı haritası — kurumun etkisini somut verilerle ölçer.",
        "info", "🗺️",
    )

    # ── Mezun verisi yükle ──
    td = _get_tenant_dir()
    alumni_path = os.path.join(td, "mezunlar.json")
    alumni_list = _load_json_safe(alumni_path)

    # CSV import'tan da yükle
    import_path = os.path.join(
        ".streamlit", "MEZ-01_TamPaket",
        "MEZ-01_TamPaket_Import_UAT_Checklist_FINAL_v2",
        "02_Import", "MEZ-01_IMPORT_Ornek_Mezunlar.csv",
    )
    csv_alumni = []
    if os.path.exists(import_path):
        try:
            import pandas as pd
            df = pd.read_csv(import_path, encoding="utf-8-sig")
            csv_alumni = df.to_dict("records")
        except Exception:
            pass

    all_alumni = alumni_list + csv_alumni
    if not all_alumni:
        styled_info_banner("Mezun verisi bulunamadı. Mezunlar ve Kariyer modülünden kayıt ekleyin.", "warning")
        return

    # ── Etkinlik/mentorluk/bağış verisi ──
    events = _load_json_safe(os.path.join(td, "mezun_etkinlikleri.json"))
    mentors = _load_json_safe(os.path.join(td, "mezun_mentorluk.json"))
    bagislar = _load_json_safe(os.path.join(td, "mezun_bagis_sponsorluk.json"))
    tavsiyeler = _load_json_safe(os.path.join(td, "mezun_tavsiye_adaylari.json"))

    # ── Etki Puanı hesapla ──
    def _etki_puani(mezun_id: str) -> dict:
        m_events = sum(1 for e in events if mezun_id in str(e.get("sorumlu", "")) or mezun_id in str(e.get("kaynak_mezun", "")))
        m_mentor = sum(1 for m in mentors if m.get("mentor_id") == mezun_id)
        m_bagis = sum(float(b.get("tutar", 0)) for b in bagislar if b.get("mezun_id") == mezun_id)
        m_tavsiye = sum(1 for t in tavsiyeler if t.get("tavsiye_eden_id") == mezun_id)
        puan = (m_events * 10) + (m_mentor * 25) + (min(m_bagis / 1000, 30)) + (m_tavsiye * 15)
        return {
            "etkinlik": m_events, "mentorluk": m_mentor,
            "bagis": m_bagis, "tavsiye": m_tavsiye,
            "puan": round(min(puan, 100), 1),
        }

    # ── KPI Kartları ──
    uni_set = set()
    sektor_set = set()
    sehir_set = set()
    for a in all_alumni:
        u = str(a.get("Universite", "")).strip()
        if u and u != "nan":
            uni_set.add(u)
        s = str(a.get("Sektor", "")).strip()
        if s and s != "nan":
            sektor_set.add(s)
        c = str(a.get("Sehir", "")).strip()
        if c and c != "nan":
            sehir_set.add(c)

    styled_stat_row([
        ("Toplam Mezun", len(all_alumni), "#2563eb", "🎓"),
        ("Farklı Üniversite", len(uni_set), "#8b5cf6", "🏫"),
        ("Farklı Sektör", len(sektor_set), "#10b981", "🏢"),
        ("Farklı Şehir", len(sehir_set), "#f59e0b", "🌍"),
    ])

    # ── Sektör Dağılımı ──
    col1, col2 = st.columns(2)
    with col1:
        styled_section("Sektör Dağılımı", "#10b981")
        sektor_counter = Counter(
            str(a.get("Sektor", "Bilinmiyor")).strip()
            for a in all_alumni if str(a.get("Sektor", "")).strip() and str(a.get("Sektor", "")).strip() != "nan"
        )
        if sektor_counter:
            for sektor, cnt in sektor_counter.most_common(10):
                pct = cnt / len(all_alumni) * 100
                color = "#10b981"
                st.markdown(f"""
                <div style="margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                        <span style="color:#e0e0e0;">{sektor}</span>
                        <span style="color:{color};font-weight:700;">{cnt} (%{pct:.0f})</span>
                    </div>
                    <div style="background:#1a2035;border-radius:4px;height:8px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    with col2:
        styled_section("Şehir Dağılımı", "#f59e0b")
        sehir_counter = Counter(
            str(a.get("Sehir", "Bilinmiyor")).strip()
            for a in all_alumni if str(a.get("Sehir", "")).strip() and str(a.get("Sehir", "")).strip() != "nan"
        )
        if sehir_counter:
            for sehir, cnt in sehir_counter.most_common(10):
                pct = cnt / len(all_alumni) * 100
                color = "#f59e0b"
                st.markdown(f"""
                <div style="margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                        <span style="color:#e0e0e0;">{sehir}</span>
                        <span style="color:{color};font-weight:700;">{cnt} (%{pct:.0f})</span>
                    </div>
                    <div style="background:#1a2035;border-radius:4px;height:8px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Top Etki Puanı ──
    styled_section("Etki Puanı Sıralaması", "#8b5cf6")
    etki_list = []
    for a in all_alumni:
        mid = str(a.get("MezunID", "")).strip()
        ad = str(a.get("Ad", "")).strip()
        soyad = str(a.get("Soyad", "")).strip()
        if not mid or not ad:
            continue
        ep = _etki_puani(mid)
        etki_list.append({"id": mid, "ad": f"{ad} {soyad}", "uni": str(a.get("Universite", "-")), "sektor": str(a.get("Sektor", "-")), **ep})

    etki_list.sort(key=lambda x: -x["puan"])
    for i, e in enumerate(etki_list[:10], 1):
        puan = e["puan"]
        renk = "#10b981" if puan >= 50 else ("#f59e0b" if puan >= 20 else "#64748b")
        st.markdown(f"""
        <div style="background:#111827;border-radius:10px;padding:10px 16px;margin-bottom:6px;
        display:flex;justify-content:space-between;align-items:center;border-left:4px solid {renk};">
            <div>
                <strong style="color:#e0e0e0;">#{i} {e['ad']}</strong>
                <span style="color:#888;font-size:0.78rem;margin-left:8px;">{e['uni']} | {e['sektor']}</span>
            </div>
            <div style="text-align:right;">
                <span style="color:{renk};font-weight:800;font-size:1.2rem;">{puan}</span>
                <div style="color:#888;font-size:0.7rem;">Etkinlik:{e['etkinlik']} Mentor:{e['mentorluk']} Tavsiye:{e['tavsiye']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Kurumsal Etki Skoru ──
    ort_puan = sum(e["puan"] for e in etki_list) / max(1, len(etki_list))
    renk = "#10b981" if ort_puan >= 30 else ("#f59e0b" if ort_puan >= 15 else "#ef4444")
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0B0F19,#162033);border-radius:16px;padding:24px;
    text-align:center;margin-top:16px;border:1px solid {renk}40;">
        <div style="color:#888;font-size:0.9rem;">Kurumsal Mezun Etki Skoru</div>
        <div style="font-size:3rem;font-weight:900;color:{renk};">{ort_puan:.1f}/100</div>
        <div style="color:#94a3b8;font-size:0.8rem;">{len(all_alumni)} mezun | {len(etki_list)} puanlanan</div>
    </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. MODÜLLER ARASI CROSS-ALERT & KURUMSAL SAĞLIK SKORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_cross_alert(store, loader):
    styled_section("🏥 Modüller Arası Cross-Alert & Kurumsal Sağlık Skoru", "#ef4444")
    styled_info_banner(
        "SSG, Akademik Takip, Mezunlar ve Erken Uyarı modüllerini birleştiren çapraz uyarı sistemi.",
        "info", "🏥",
    )

    # ── Veri toplama ──
    td = _get_tenant_dir()

    # SSG verileri
    ssg_base = os.path.join(td, "ssg")
    ssg_olaylar = _load_json_safe(os.path.join(ssg_base, "olay_kayitlari.json"))
    ssg_riskler = _load_json_safe(os.path.join(ssg_base, "risk_kayitlari.json"))
    ssg_tatbikatlar = _load_json_safe(os.path.join(ssg_base, "tatbikat_kayitlari.json"))
    ssg_denetimler = _load_json_safe(os.path.join(ssg_base, "denetim_kayitlari.json"))

    # Akademik verileri
    ak_base = os.path.join(td, "akademik") if os.path.isdir(os.path.join(td, "akademik")) else os.path.join("data", "akademik")
    ak_devamsizlik = _load_json_safe(os.path.join(ak_base, "attendance.json"))
    ak_notlar = _load_json_safe(os.path.join(ak_base, "grades.json"))

    # Erken uyarı risk verileri
    eu_base = os.path.join(td, "erken_uyari") if os.path.isdir(os.path.join(td, "erken_uyari")) else os.path.join("data", "erken_uyari")
    eu_risks = _load_json_safe(os.path.join(eu_base, "risk_records.json"))
    eu_alerts = _load_json_safe(os.path.join(eu_base, "alerts.json"))

    # Mezun verileri
    mezun_stajlar = _load_json_safe(os.path.join(td, "mezun_staj_is.json"))
    mezun_etkinlikler = _load_json_safe(os.path.join(td, "mezun_etkinlikleri.json"))

    # ── Alt Skor Hesaplama (her biri 0-100) ──
    # 1) Güvenlik Skoru (SSG)
    acik_olay = sum(1 for o in ssg_olaylar if o.get("durum") in ("Acik", "Açık", "Inceleniyor"))
    kritik_risk = sum(1 for r in ssg_riskler if r.get("seviye") in ("kritik", "yuksek") and r.get("durum") != "Kapandi")
    tamamlanan_tat = sum(1 for t in ssg_tatbikatlar if t.get("durum") == "Tamamlandı")
    guvenlik_skor = max(0, 100 - (acik_olay * 15) - (kritik_risk * 10) + (tamamlanan_tat * 5))
    guvenlik_skor = min(100, guvenlik_skor)

    # 2) Akademik Sağlık Skoru
    yuksek_devamsiz = sum(1 for d in ak_devamsizlik if str(d.get("turu", "")).lower() in ("ozursuz", "özürsüz"))
    toplam_not = len(ak_notlar)
    dusuk_not = sum(1 for n in ak_notlar if float(n.get("puan", n.get("not_degeri", 100))) < 50)
    akademik_skor = max(0, 100 - (yuksek_devamsiz * 2) - (dusuk_not * 3 if toplam_not > 0 else 0))
    akademik_skor = min(100, akademik_skor)

    # 3) Erken Uyarı Skoru
    kritik_ogrenci = sum(1 for r in eu_risks if r.get("risk_level") in ("CRITICAL", "HIGH"))
    acik_alert = sum(1 for a in eu_alerts if not a.get("is_resolved"))
    eu_skor = max(0, 100 - (kritik_ogrenci * 5) - (acik_alert * 3))
    eu_skor = min(100, eu_skor)

    # 4) Mezun Etkinlik Skoru
    aktif_staj = sum(1 for s in mezun_stajlar if s.get("durum") in ("Aktif", "Açık"))
    mezun_skor = min(100, 40 + (aktif_staj * 10) + (len(mezun_etkinlikler) * 8))

    # ── Genel Kurumsal Sağlık Skoru ──
    genel_skor = int((guvenlik_skor * 0.30) + (akademik_skor * 0.35) + (eu_skor * 0.25) + (mezun_skor * 0.10))
    genel_renk = "#10b981" if genel_skor >= 70 else ("#f59e0b" if genel_skor >= 40 else "#ef4444")
    genel_label = "SAĞLIKLI" if genel_skor >= 70 else ("DİKKAT" if genel_skor >= 40 else "KRİTİK")

    # ── Ana Skor Göstergesi ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0B0F19,#162033);border-radius:20px;padding:28px;
    text-align:center;margin-bottom:20px;border:2px solid {genel_renk}40;">
        <div style="color:#888;font-size:1rem;font-weight:600;">KURUMSAL SAĞLIK SKORU</div>
        <div style="font-size:4rem;font-weight:900;color:{genel_renk};margin:8px 0;">{genel_skor}/100</div>
        <div style="display:inline-block;background:{genel_renk}20;color:{genel_renk};padding:6px 20px;
        border-radius:20px;font-weight:700;font-size:0.95rem;">{genel_label}</div>
    </div>""", unsafe_allow_html=True)

    # ── Bileşen Skorları ──
    styled_stat_row([
        ("Güvenlik (SSG)", f"{guvenlik_skor}", "#ef4444", "🛡️"),
        ("Akademik", f"{akademik_skor}", "#2563eb", "📚"),
        ("Erken Uyarı", f"{eu_skor}", "#f59e0b", "🧠"),
        ("Mezun Etkinlik", f"{mezun_skor}", "#8b5cf6", "🎓"),
    ])

    # ── Bileşen Progress Barları ──
    bilesenler = [
        ("Güvenlik (SSG) — %30 ağırlık", guvenlik_skor, "#ef4444"),
        ("Akademik Sağlık — %35 ağırlık", akademik_skor, "#2563eb"),
        ("Erken Uyarı — %25 ağırlık", eu_skor, "#f59e0b"),
        ("Mezun Ekosistemi — %10 ağırlık", mezun_skor, "#8b5cf6"),
    ]
    for baslik, skor, renk in bilesenler:
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                <span style="color:#e0e0e0;font-weight:600;font-size:0.85rem;">{baslik}</span>
                <span style="color:{renk};font-weight:700;">{skor}/100</span>
            </div>
            <div style="background:#1a2035;border-radius:6px;height:14px;overflow:hidden;">
                <div style="width:{skor}%;height:100%;background:{renk};border-radius:6px;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Cross-Alert Tablosu ──
    styled_section("Çapraz Uyarılar", "#f97316")
    cross_alerts = []

    # SSG → Akademik uyarılar
    if acik_olay > 0:
        cross_alerts.append({
            "icon": "🚨", "kaynak": "SSG → Akademik",
            "mesaj": f"{acik_olay} açık güvenlik olayı var — öğrenci güvenliği takibi yapılmalı",
            "seviye": "Yüksek", "renk": "#ef4444",
        })
    if kritik_risk > 0:
        cross_alerts.append({
            "icon": "⚠️", "kaynak": "SSG → Yönetim",
            "mesaj": f"{kritik_risk} kritik/yüksek risk kalemi açık — acil aksiyon gerekli",
            "seviye": "Kritik", "renk": "#ef4444",
        })

    # Akademik → Rehberlik uyarılar
    if yuksek_devamsiz > 10:
        cross_alerts.append({
            "icon": "📉", "kaynak": "Akademik → Rehberlik",
            "mesaj": f"{yuksek_devamsiz} özürsüz devamsızlık kaydı — rehberlik görüşmesi planlanmalı",
            "seviye": "Orta", "renk": "#f59e0b",
        })

    # Erken Uyarı → Veli uyarılar
    if kritik_ogrenci > 0:
        cross_alerts.append({
            "icon": "🧠", "kaynak": "Erken Uyarı → Veli İletişim",
            "mesaj": f"{kritik_ogrenci} öğrenci kritik/yüksek risk seviyesinde — veli bilgilendirmesi yapılmalı",
            "seviye": "Yüksek", "renk": "#f97316",
        })

    # Mezun → Akademik fırsatlar
    if aktif_staj > 0:
        cross_alerts.append({
            "icon": "💼", "kaynak": "Mezun → Akademik",
            "mesaj": f"{aktif_staj} aktif staj/iş ilanı mevcut — ilgili sınıflara duyurulmalı",
            "seviye": "Bilgi", "renk": "#10b981",
        })

    if not cross_alerts:
        cross_alerts.append({
            "icon": "✅", "kaynak": "Sistem",
            "mesaj": "Tüm modüller sağlıklı — çapraz uyarı bulunmuyor",
            "seviye": "Normal", "renk": "#10b981",
        })

    for alert in cross_alerts:
        st.markdown(f"""
        <div style="background:#111827;border-radius:10px;padding:12px 16px;margin-bottom:6px;
        border-left:4px solid {alert['renk']};display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.4rem;">{alert['icon']}</span>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;">
                    <strong style="color:#e0e0e0;font-size:0.9rem;">{alert['kaynak']}</strong>
                    <span style="background:{alert['renk']}20;color:{alert['renk']};padding:2px 10px;
                    border-radius:10px;font-size:0.75rem;font-weight:600;">{alert['seviye']}</span>
                </div>
                <div style="color:#94a3b8;font-size:0.82rem;margin-top:3px;">{alert['mesaj']}</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. AI KARİYER PUSULA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_kariyer_pusula(store, loader):
    styled_section("🧭 AI Kariyer Pusula — Mezun Veri Madenciliği", "#0d9488")
    styled_info_banner(
        "Mezun kariyer yollarını analiz ederek mevcut öğrencilere veri odaklı yönlendirme sunar.",
        "info", "🧭",
    )

    # ── Mezun verisi yükle ──
    td = _get_tenant_dir()
    alumni_path = os.path.join(td, "mezunlar.json")
    alumni_list = _load_json_safe(alumni_path)

    import_path = os.path.join(
        ".streamlit", "MEZ-01_TamPaket",
        "MEZ-01_TamPaket_Import_UAT_Checklist_FINAL_v2",
        "02_Import", "MEZ-01_IMPORT_Ornek_Mezunlar.csv",
    )
    if os.path.exists(import_path):
        try:
            import pandas as pd
            df = pd.read_csv(import_path, encoding="utf-8-sig")
            alumni_list = alumni_list + df.to_dict("records")
        except Exception:
            pass

    if not alumni_list:
        styled_info_banner("Kariyer pusula için mezun verisi gereklidir.", "warning")
        return

    # ── Kariyer Yolu Analizi ──
    styled_section("Bölüm → Sektör Kariyer Yolları", "#2563eb")

    bolum_sektor: dict[str, Counter] = {}
    bolum_uni: dict[str, Counter] = {}
    for a in alumni_list:
        bolum = str(a.get("Bolum", "")).strip()
        sektor = str(a.get("Sektor", "")).strip()
        uni = str(a.get("Universite", "")).strip()
        if not bolum or bolum == "nan":
            continue
        if bolum not in bolum_sektor:
            bolum_sektor[bolum] = Counter()
            bolum_uni[bolum] = Counter()
        if sektor and sektor != "nan":
            bolum_sektor[bolum][sektor] += 1
        if uni and uni != "nan":
            bolum_uni[bolum][uni] += 1

    if bolum_sektor:
        for bolum in sorted(bolum_sektor.keys()):
            sektor_c = bolum_sektor[bolum]
            uni_c = bolum_uni.get(bolum, Counter())
            toplam = sum(sektor_c.values())
            if toplam < 1:
                continue

            with st.expander(f"📚 {bolum} ({toplam} mezun)"):
                st.markdown("**Sektör Dağılımı:**")
                for sektor, cnt in sektor_c.most_common(5):
                    pct = cnt / toplam * 100
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                        <div style="flex:1;background:#1a2035;border-radius:4px;height:8px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#0d9488;border-radius:4px;"></div>
                        </div>
                        <span style="color:#e0e0e0;font-size:0.82rem;min-width:200px;">{sektor} — {cnt} (%{pct:.0f})</span>
                    </div>""", unsafe_allow_html=True)

                if uni_c:
                    st.markdown("**Tercih Edilen Üniversiteler:**")
                    for uni, cnt in uni_c.most_common(3):
                        st.markdown(f"  🏫 {uni} ({cnt} mezun)")
    else:
        styled_info_banner("Bölüm verisi bulunamadı.", "info")

    # ── Öğrenci Profil Eşleştirme ──
    styled_section("Öğrenci-Mezun Profil Eşleştirme", "#8b5cf6")
    st.markdown("Mevcut öğrenci bilgileriyle en yakın mezun profillerini eşleştirin:")

    students = loader.load_students() if hasattr(loader, "load_students") else []
    if students:
        student_names = [f"{s.get('ad', '')} {s.get('soyad', '')} ({s.get('sinif', '')}/{s.get('sube', '')})" for s in students]
        selected_student = st.selectbox("Öğrenci Seçin", student_names, key="kp_student")
        if selected_student:
            idx = student_names.index(selected_student)
            stu = students[idx]
            stu_sinif = int(stu.get("sinif", 0))

            # En yakın mezuniyet yılı / kademe eşleşmesi
            kademe = "Lise" if stu_sinif >= 9 else ("Ortaokul" if stu_sinif >= 5 else "İlkokul")
            matching_alumni = [
                a for a in alumni_list
                if str(a.get("Kademe", "")).strip() == kademe
                and str(a.get("Universite", "")).strip() not in ("", "nan")
            ]

            if matching_alumni:
                st.markdown(f"**{kademe}** kademesinden **{len(matching_alumni)}** üniversite mezunu bulundu:")

                # Üniversite-Sektör dağılımı
                uni_counter = Counter(str(a.get("Universite", "")).strip() for a in matching_alumni if str(a.get("Universite", "")).strip() != "nan")
                sektor_counter = Counter(str(a.get("Sektor", "")).strip() for a in matching_alumni if str(a.get("Sektor", "")).strip() not in ("", "nan"))

                mc1, mc2 = st.columns(2)
                with mc1:
                    st.markdown("**En Çok Tercih Edilen Üniversiteler:**")
                    for uni, cnt in uni_counter.most_common(5):
                        pct = cnt / len(matching_alumni) * 100
                        st.markdown(f"  🏫 {uni} — **%{pct:.0f}** ({cnt} mezun)")

                with mc2:
                    st.markdown("**Çalışılan Sektörler:**")
                    for sektor, cnt in sektor_counter.most_common(5):
                        pct = cnt / len(matching_alumni) * 100
                        st.markdown(f"  🏢 {sektor} — **%{pct:.0f}** ({cnt} mezun)")

                # Rol model önerisi
                styled_section("Rol Model Önerileri", "#f59e0b")
                mentors_data = _load_json_safe(os.path.join(td, "mezun_mentorluk.json"))
                aktif_mentorlar = {m.get("mentor_id") for m in mentors_data if m.get("durum") == "Aktif"}

                for a in matching_alumni[:5]:
                    mid = str(a.get("MezunID", ""))
                    ad = str(a.get("Ad", ""))
                    soyad = str(a.get("Soyad", ""))
                    uni = str(a.get("Universite", "-"))
                    sektor = str(a.get("Sektor", "-"))
                    unvan = str(a.get("Unvan", "-"))
                    mentor_badge = "🟢 Aktif Mentor" if mid in aktif_mentorlar else ""

                    st.markdown(f"""
                    <div style="background:#111827;border-radius:10px;padding:10px 16px;margin-bottom:6px;
                    display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;">{ad} {soyad}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{uni} → {sektor}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="color:#0d9488;font-size:0.82rem;">{unvan}</span>
                            {f'<span style="color:#10b981;font-size:0.72rem;margin-left:6px;">{mentor_badge}</span>' if mentor_badge else ''}
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                styled_info_banner("Bu kademe için üniversite mezunu bulunamadı.", "info")
    else:
        styled_info_banner("Öğrenci verisi bulunamadı.", "info")

    # ── AI Kariyer Insight ──
    styled_section("AI Kariyer İçgörüleri", "#ec4899")
    insights = []

    # En popüler yollar
    all_sektorler = Counter(
        str(a.get("Sektor", "")).strip()
        for a in alumni_list if str(a.get("Sektor", "")).strip() not in ("", "nan")
    )
    if all_sektorler:
        top = all_sektorler.most_common(1)[0]
        insights.append(f"En popüler sektör: **{top[0]}** — mezunların %{top[1]/len(alumni_list)*100:.0f}'ı bu alanda çalışıyor.")

    all_uni = Counter(
        str(a.get("Universite", "")).strip()
        for a in alumni_list if str(a.get("Universite", "")).strip() not in ("", "nan")
    )
    if all_uni:
        top_uni = all_uni.most_common(1)[0]
        insights.append(f"En tercih edilen üniversite: **{top_uni[0]}** — {top_uni[1]} mezun.")

    if len(alumni_list) > 10:
        uni_rate = sum(1 for a in alumni_list if str(a.get("Universite", "")).strip() not in ("", "nan")) / len(alumni_list) * 100
        insights.append(f"Üniversiteye yerleşme oranı: **%{uni_rate:.0f}**")

    mentors_data = _load_json_safe(os.path.join(td, "mezun_mentorluk.json"))
    if len(mentors_data) > 0:
        insights.append(f"Aktif mentorluk programı: **{len(mentors_data)}** eşleşme kayıtlı.")

    if not insights:
        insights.append("Daha fazla mezun verisi eklendikçe içgörüler zenginleşecektir.")

    for ins in insights:
        st.markdown(f"""
        <div style="background:rgba(236,72,153,0.06);border-left:3px solid #ec4899;border-radius:0 8px 8px 0;
        padding:8px 14px;margin-bottom:6px;font-size:0.88rem;color:#e0e0e0;">
            💡 {ins}
        </div>""", unsafe_allow_html=True)
