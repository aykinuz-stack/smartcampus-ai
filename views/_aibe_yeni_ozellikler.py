"""
AI Bireysel Eğitim — Yeni Özellikler
======================================
1. Kişisel Öğrenme Yol Haritası & Adaptif Plan
2. Akıllı Çalışma Koçu & Tekrar Motoru
3. Bireysel Gelişim Analitik & Veli/Öğretmen Raporu
"""
from __future__ import annotations
import json, os, uuid, math
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

_DERSLER = ["Matematik", "Turkce", "Fen Bilimleri", "Sosyal Bilgiler", "Ingilizce",
            "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya"]

_DERS_KONULARI = {
    "Matematik": ["Cebir", "Geometri", "Olasilik", "Istatistik", "Sayilar", "Fonksiyonlar", "Denklemler", "Ucgenler"],
    "Turkce": ["Dil Bilgisi", "Paragraf", "Anlama", "Yazma", "Sozcuk", "Ses Bilgisi"],
    "Fen Bilimleri": ["Fizik", "Kimya", "Biyoloji", "Yer Bilimi"],
    "Sosyal Bilgiler": ["Tarih", "Cografya", "Vatandaslik", "Ekonomi"],
    "Ingilizce": ["Grammar", "Vocabulary", "Reading", "Listening", "Writing"],
    "Fizik": ["Mekanik", "Elektrik", "Optik", "Dalgalar", "Termodinamik"],
    "Kimya": ["Atom", "Baglar", "Reaksiyonlar", "Asit-Baz", "Organik"],
    "Biyoloji": ["Hucre", "Genetik", "Ekoloji", "Sistem", "Evrim"],
}

_MASTERY = {(0,30):("Baslangic","#ef4444","🔴"), (30,60):("Gelisen","#f59e0b","🟡"),
            (60,80):("Yetkin","#3b82f6","🔵"), (80,101):("Uzman","#10b981","🟢")}

_BLOOM = ["Hatirlama", "Anlama", "Uygulama", "Analiz", "Degerlendirme", "Yaratma"]

_TEKRAR_ARALIKLARI = [1, 3, 7, 14, 30]  # gun

_POMODORO_SURELER = {"Kisa (15dk)": 15, "Standart (25dk)": 25, "Uzun (45dk)": 45}

_MOTIVASYON_MESAJLARI = [
    "Her gun bir adim daha yakinsin!", "Basari kucuk adimlarin toplami.",
    "Bugunku calisman yarinin basarisi.", "Zor konular seni guclendirir!",
    "Dunden daha iyisin, yarini daha da iyi olacak.", "Odaklan ve devam et!",
    "Hata yapmak ogrenmek demek.", "Sen basarabilirsin!",
    "Her usta bir zamanlar cirakti.", "Konsantrasyon surecin guclu!",
]

def _mastery_label(p):
    for (lo,hi),(ad,renk,ikon) in _MASTERY.items():
        if lo <= p < hi: return ad, renk, ikon
    return "?","#94a3b8","⚪"

def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None


# ════════════════════════════════════════════════════════════
# 1. KİŞİSEL ÖĞRENME YOL HARİTASI & ADAPTİF PLAN
# ════════════════════════════════════════════════════════════

def render_yol_haritasi():
    """Kişisel Öğrenme Yol Haritası — güçlü/zayıf tespit, adaptif plan, mastery haritası."""
    styled_section("Kisisel Ogrenme Yol Haritasi & Adaptif Plan", "#6366f1")
    styled_info_banner(
        "Ders bazli guclu/zayif konulari tespit edip kisisel calisma plani olusturur. "
        "Haftalik adaptif plan — quiz sonuclarina gore otomatik guncellenir.",
        banner_type="info", icon="🗺️")

    planlar = _lj("ogrenme_planlari.json")
    konu_puanlari = _lj("konu_puanlari.json")

    styled_stat_row([
        ("Plan", str(len(planlar)), "#6366f1", "📋"),
        ("Konu Kaydi", str(len(konu_puanlari)), "#3b82f6", "📊"),
    ])

    sub = st.tabs(["🎯 Konu Degerlendirme", "🗺️ Mastery Haritasi", "📋 Haftalik Plan", "📈 Ilerleme"])

    # ── KONU DEĞERLENDİRME ──
    with sub[0]:
        styled_section("Konu Bazli Seviye Degerlendirmesi")
        ogr = _ogr_sec("yh_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            with st.form("konu_form"):
                k_ders = st.selectbox("Ders", _DERSLER, key="yh_ders")
                konular = _DERS_KONULARI.get(k_ders, ["Genel"])

                puanlar = {}
                st.markdown(f"**{k_ders} — Konu Seviyeleri (0-100):**")
                cols = st.columns(2)
                for i, konu in enumerate(konular):
                    with cols[i % 2]:
                        puanlar[konu] = st.slider(konu, 0, 100, 50, key=f"yh_k_{konu}")

                if st.form_submit_button("Kaydet & Plan Olustur", use_container_width=True, type="primary"):
                    # Konu puanlarini kaydet
                    for konu, puan in puanlar.items():
                        konu_puanlari.append({
                            "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                            "ders": k_ders, "konu": konu, "puan": puan,
                            "tarih": date.today().isoformat(),
                        })
                    _sj("konu_puanlari.json", konu_puanlari)

                    # Zayif konulardan plan olustur
                    zayiflar = [(k, p) for k, p in puanlar.items() if p < 70]
                    zayiflar.sort(key=lambda x: x[1])

                    aktiviteler = []
                    gun_idx = 0
                    gunler = ["Pzt","Sal","Car","Per","Cum"]
                    for konu, puan in zayiflar:
                        if puan < 40:
                            akts = ["Konu Tekrari (Video)", "Temel Sorular (10)", "Flash Kart"]
                        elif puan < 60:
                            akts = ["Ozet Tekrari", "Orta Sorular (8)", "Quiz"]
                        else:
                            akts = ["Pekistirme Sorulari (5)", "Uygulama Quiz"]

                        for akt in akts:
                            aktiviteler.append({
                                "gun": gunler[gun_idx % 5], "ders": k_ders,
                                "konu": konu, "aktivite": akt,
                                "sure_dk": 20, "tamamlandi": False,
                            })
                            gun_idx += 1

                    plan = {
                        "id": f"pl_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "ogrenci_id": ogr.get("id",""),
                        "ders": k_ders, "aktiviteler": aktiviteler,
                        "hafta": date.today().isocalendar()[1],
                        "durum": "Aktif", "tarih": date.today().isoformat(),
                    }
                    planlar.append(plan)
                    _sj("ogrenme_planlari.json", planlar)
                    st.success(f"{len(zayiflar)} zayif konu icin {len(aktiviteler)} aktiviteli plan olusturuldu!")
                    st.rerun()

    # ── MASTERY HARİTASI ──
    with sub[1]:
        styled_section("Konu Mastery Haritasi")
        ogr2 = _ogr_sec("yh_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            ogr_kp = [k for k in konu_puanlari if k.get("ogrenci") == ogr_ad2]

            if not ogr_kp:
                st.info(f"{ogr_ad2} icin konu degerlendirmesi yok.")
            else:
                # Ders bazli grupla
                ders_grp = defaultdict(dict)
                for k in ogr_kp:
                    ders_grp[k.get("ders","?")][k.get("konu","")] = k.get("puan", 0)

                for ders, konular in ders_grp.items():
                    ort = round(sum(konular.values()) / max(len(konular), 1))
                    d_label, d_renk, d_ikon = _mastery_label(ort)

                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid {d_renk}30;border-left:5px solid {d_renk};
                        border-radius:0 14px 14px 0;padding:12px 16px;margin:8px 0;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">📚 {ders}</span>
                            <span style="background:{d_renk}20;color:{d_renk};padding:3px 10px;border-radius:8px;
                                font-size:0.72rem;font-weight:800;">{d_ikon} {d_label} ({ort}%)</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    for konu, puan in sorted(konular.items(), key=lambda x: x[1]):
                        k_label, k_renk, _ = _mastery_label(puan)
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin:3px 0;padding-left:20px;">
                            <span style="min-width:120px;color:#e2e8f0;font-size:0.78rem;font-weight:600;">{konu}</span>
                            <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                                <div style="width:{puan}%;height:100%;background:{k_renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                                    <span style="font-size:0.55rem;color:#fff;font-weight:700;">{puan}%</span>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)

    # ── HAFTALIK PLAN ──
    with sub[2]:
        styled_section("Aktif Calisma Planlari")
        aktif = [p for p in planlar if p.get("durum") == "Aktif"]
        if not aktif:
            st.info("Aktif plan yok. 'Konu Degerlendirme' sekmesinden plan olusturun.")
        else:
            for plan in aktif:
                akt = plan.get("aktiviteler", [])
                tamamlanan = sum(1 for a in akt if a.get("tamamlandi"))
                toplam = max(len(akt), 1)
                ilerleme = round(tamamlanan / toplam * 100)
                renk = "#10b981" if ilerleme >= 70 else "#f59e0b" if ilerleme >= 40 else "#3b82f6"

                st.markdown(f"""
                <div style="background:#0f172a;border:2px solid {renk};border-radius:16px;
                    padding:14px 18px;margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#e2e8f0;font-weight:800;font-size:0.9rem;">
                            🗺️ {plan.get('ogrenci','')} — {plan.get('ders','')}</span>
                        <span style="color:{renk};font-weight:800;">{ilerleme}%</span>
                    </div>
                    <div style="background:#1e293b;border-radius:4px;height:10px;margin:8px 0;overflow:hidden;">
                        <div style="width:{ilerleme}%;height:100%;background:{renk};border-radius:4px;"></div>
                    </div>
                    <div style="color:#64748b;font-size:0.68rem;">{tamamlanan}/{toplam} aktivite</div>
                </div>""", unsafe_allow_html=True)

                with st.expander(f"Detay: {plan.get('id','')}", expanded=False):
                    gun_grp = defaultdict(list)
                    for a in akt:
                        gun_grp[a.get("gun","?")].append(a)
                    for gun in ["Pzt","Sal","Car","Per","Cum"]:
                        gun_akt = gun_grp.get(gun, [])
                        if gun_akt:
                            st.markdown(f"**{gun}:**")
                            for a in gun_akt:
                                done = "✅" if a.get("tamamlandi") else "⬜"
                                st.markdown(f"  {done} {a.get('konu','')} — {a.get('aktivite','')}")

                    if st.button("Plani Tamamla", key=f"pl_d_{plan['id']}"):
                        plan["durum"] = "Tamamlandi"
                        _sj("ogrenme_planlari.json", planlar)
                        st.rerun()

    # ── İLERLEME ──
    with sub[3]:
        styled_section("Ilerleme Takibi")
        tamamlanan_plan = [p for p in planlar if p.get("durum") == "Tamamlandi"]
        if tamamlanan_plan:
            ogr_say = Counter(p.get("ogrenci","") for p in tamamlanan_plan)
            for ad, sayi in ogr_say.most_common(10):
                st.markdown(f"- **{ad}**: {sayi} plan tamamladi")
        else:
            st.info("Tamamlanan plan yok.")


# ════════════════════════════════════════════════════════════
# 2. AKILLI ÇALIŞMA KOÇU & TEKRAR MOTORU
# ════════════════════════════════════════════════════════════

def render_calisma_kocu():
    """Akıllı Çalışma Koçu — pomodoro, spaced repetition, flash kart, streak."""
    styled_section("Akilli Calisma Kocu & Tekrar Motoru", "#059669")
    styled_info_banner(
        "Pomodoro odak zamanlayici, aralikli tekrar takvimi, flash kart, "
        "gunluk calisma streak takibi, motivasyon mesajlari.",
        banner_type="info", icon="⏰")

    calisma_log = _lj("calisma_log.json")
    flash_kartlar = _lj("flash_kartlar.json")
    tekrar_takvim = _lj("tekrar_takvim.json")

    # KPI
    bugun = date.today().isoformat()
    bugun_dk = sum(c.get("sure_dk", 0) for c in calisma_log if c.get("tarih","")[:10] == bugun)
    bu_hafta_bas = (date.today() - timedelta(days=date.today().weekday())).isoformat()
    hafta_dk = sum(c.get("sure_dk", 0) for c in calisma_log if c.get("tarih","")[:10] >= bu_hafta_bas)

    # Streak hesapla
    streak = 0
    gun = date.today()
    while True:
        gun_str = gun.isoformat()
        if any(c.get("tarih","")[:10] == gun_str for c in calisma_log):
            streak += 1
            gun -= timedelta(days=1)
        else:
            break

    styled_stat_row([
        ("Bugun", f"{bugun_dk} dk", "#059669", "📅"),
        ("Bu Hafta", f"{hafta_dk} dk", "#3b82f6", "📊"),
        ("Streak", f"{streak} gun 🔥", "#ef4444" if streak >= 7 else "#f59e0b", "🔥"),
        ("Flash Kart", str(len(flash_kartlar)), "#8b5cf6", "🃏"),
    ])

    # Motivasyon
    import random
    if streak > 0:
        mesaj = random.choice(_MOTIVASYON_MESAJLARI)
        st.markdown(f"""
        <div style="background:#05966915;border:1px solid #05966930;border-radius:12px;
            padding:10px 16px;text-align:center;margin-bottom:12px;">
            <span style="color:#10b981;font-weight:700;font-size:0.85rem;">💪 {mesaj}</span>
        </div>""", unsafe_allow_html=True)

    sub = st.tabs(["🍅 Pomodoro", "🃏 Flash Kart", "🔄 Tekrar Takvim", "📊 Calisma Analiz", "📝 Log Kaydet"])

    # ── POMODORO ──
    with sub[0]:
        styled_section("Pomodoro Odak Zamanlayici")
        st.caption("Bir sure secin ve calismayi baslatin. Bitirince kaydet.")

        p_ders = st.selectbox("Ders", _DERSLER, key="pm_ders")
        p_konu = st.text_input("Konu", key="pm_konu")
        p_sure = st.selectbox("Sure", list(_POMODORO_SURELER.keys()), key="pm_sure")
        sure_dk = _POMODORO_SURELER[p_sure]

        st.markdown(f"""
        <div style="background:#0f172a;border:3px solid #059669;border-radius:50%;
            width:150px;height:150px;display:flex;align-items:center;justify-content:center;
            margin:20px auto;">
            <div style="text-align:center;">
                <div style="color:#10b981;font-weight:900;font-size:2.5rem;">{sure_dk}</div>
                <div style="color:#64748b;font-size:0.7rem;">dakika</div>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("Calisma Tamamlandi — Kaydet", use_container_width=True, type="primary"):
            calisma_log.append({
                "ogrenci": st.session_state.get("_pm_ogr", ""),
                "ders": p_ders, "konu": p_konu,
                "sure_dk": sure_dk, "tip": "Pomodoro",
                "tarih": datetime.now().isoformat(),
            })
            _sj("calisma_log.json", calisma_log)
            st.success(f"🍅 {sure_dk} dk {p_ders} calismasi kaydedildi!")
            st.rerun()

    # ── FLASH KART ──
    with sub[1]:
        styled_section("Flash Kart Sistemi")

        # Kart ekle
        with st.form("fk_form"):
            c1, c2 = st.columns(2)
            with c1:
                fk_on = st.text_input("On Yuz (Soru/Terim)", key="fk_on")
                fk_ders = st.selectbox("Ders", _DERSLER, key="fk_ders")
            with c2:
                fk_arka = st.text_input("Arka Yuz (Cevap/Tanim)", key="fk_arka")

            if st.form_submit_button("Kart Ekle", use_container_width=True):
                if fk_on and fk_arka:
                    flash_kartlar.append({
                        "id": f"fk_{uuid.uuid4().hex[:8]}",
                        "on": fk_on, "arka": fk_arka, "ders": fk_ders,
                        "tekrar_no": 0,
                        "sonraki_tekrar": date.today().isoformat(),
                        "created_at": datetime.now().isoformat(),
                    })
                    _sj("flash_kartlar.json", flash_kartlar)
                    st.success("Kart eklendi!")
                    st.rerun()

        # Bugunun kartlari
        bugun_kartlar = [k for k in flash_kartlar if k.get("sonraki_tekrar","") <= bugun]
        if bugun_kartlar:
            styled_section(f"Bugunku Tekrar ({len(bugun_kartlar)} kart)")
            for kart in bugun_kartlar[:5]:
                with st.expander(f"🃏 {kart.get('on','')[:40]}"):
                    st.markdown(f"**Cevap:** {kart.get('arka','')}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Bildim ✅", key=f"fk_b_{kart['id']}"):
                            idx = min(kart.get("tekrar_no", 0), len(_TEKRAR_ARALIKLARI) - 1)
                            sonraki = date.today() + timedelta(days=_TEKRAR_ARALIKLARI[idx])
                            kart["tekrar_no"] = kart.get("tekrar_no", 0) + 1
                            kart["sonraki_tekrar"] = sonraki.isoformat()
                            _sj("flash_kartlar.json", flash_kartlar)
                            st.rerun()
                    with c2:
                        if st.button("Bilemedim 🔄", key=f"fk_m_{kart['id']}"):
                            kart["tekrar_no"] = 0
                            kart["sonraki_tekrar"] = (date.today() + timedelta(days=1)).isoformat()
                            _sj("flash_kartlar.json", flash_kartlar)
                            st.rerun()
        else:
            st.success("Bugunku tekrarlar tamamlandi!")

    # ── TEKRAR TAKVİM ──
    with sub[2]:
        styled_section("Aralikli Tekrar Takvimi")
        if not flash_kartlar:
            st.info("Flash kart yok.")
        else:
            # Gelecek 7 gun
            for i in range(7):
                gun = date.today() + timedelta(days=i)
                gun_str = gun.isoformat()
                gun_kartlar = [k for k in flash_kartlar if k.get("sonraki_tekrar","") == gun_str]
                is_bugun = i == 0
                renk = "#ef4444" if len(gun_kartlar) > 5 else "#f59e0b" if gun_kartlar else "#10b981"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid {renk};border-radius:0 8px 8px 0;
                    {'border:1px solid #c9a84c;' if is_bugun else ''}">
                    <span style="min-width:70px;color:{'#c9a84c' if is_bugun else '#e2e8f0'};
                        font-weight:{'800' if is_bugun else '600'};font-size:0.78rem;">
                        {'📌 Bugun' if is_bugun else gun_str[5:]}</span>
                    <span style="color:{renk};font-weight:700;font-size:0.78rem;">{len(gun_kartlar)} kart</span>
                </div>""", unsafe_allow_html=True)

    # ── ÇALIŞMA ANALİZ ──
    with sub[3]:
        styled_section("Calisma Aliskanligi Analizi")
        if not calisma_log:
            st.info("Calisma verisi yok.")
        else:
            # Ders dagilimi
            ders_dk = defaultdict(int)
            for c in calisma_log:
                ders_dk[c.get("ders","?")] += c.get("sure_dk", 0)

            styled_section("Ders Bazli Calisma Suresi")
            max_dk = max(ders_dk.values()) if ders_dk else 1
            for ders, dk in sorted(ders_dk.items(), key=lambda x: x[1], reverse=True):
                pct = round(dk / max(max_dk, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:#059669;border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{dk} dk</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Haftalik trend
            styled_section("Haftalik Calisma Trendi")
            hafta_grp = Counter()
            for c in calisma_log:
                tarih = c.get("tarih","")[:10]
                try:
                    dt = date.fromisoformat(tarih)
                    hb = dt - timedelta(days=dt.weekday())
                    hafta_grp[hb.isoformat()] += c.get("sure_dk", 0)
                except Exception: pass

            if hafta_grp:
                max_h = max(hafta_grp.values())
                for h in sorted(hafta_grp.keys())[-6:]:
                    dk = hafta_grp[h]
                    pct = round(dk / max(max_h, 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:70px;font-size:0.7rem;color:#94a3b8;">{h[5:]}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#3b82f6;border-radius:4px;"></div>
                        </div>
                        <span style="font-size:0.65rem;color:#64748b;">{dk} dk</span>
                    </div>""", unsafe_allow_html=True)

    # ── LOG KAYDET ──
    with sub[4]:
        styled_section("Manuel Calisma Kaydi")
        with st.form("log_form"):
            c1, c2 = st.columns(2)
            with c1:
                lg_ogr = st.text_input("Ogrenci", key="lg_ogr")
                lg_ders = st.selectbox("Ders", _DERSLER, key="lg_ders")
            with c2:
                lg_sure = st.number_input("Sure (dk)", min_value=5, value=30, key="lg_sure")
                lg_tip = st.selectbox("Tip", ["Konu Calismasi", "Soru Cozme", "Video Izleme",
                    "Flash Kart", "Quiz", "Pomodoro", "Diger"], key="lg_tip")
            lg_konu = st.text_input("Konu", key="lg_konu")

            if st.form_submit_button("Kaydet", use_container_width=True):
                if lg_ogr:
                    calisma_log.append({
                        "ogrenci": lg_ogr, "ders": lg_ders,
                        "konu": lg_konu, "sure_dk": lg_sure, "tip": lg_tip,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("calisma_log.json", calisma_log)
                    st.success(f"{lg_ogr}: {lg_sure} dk {lg_ders}")
                    st.rerun()


# ════════════════════════════════════════════════════════════
# 3. BİREYSEL GELİŞİM ANALİTİK & VELİ/ÖĞRETMEN RAPORU
# ════════════════════════════════════════════════════════════

def render_gelisim_analitik():
    """Bireysel Gelişim Analitik — öğrenci analiz, veli raporu, öğretmen özeti."""
    styled_section("Bireysel Gelisim Analitik & Veli/Ogretmen Raporu", "#8b5cf6")
    styled_info_banner(
        "Tum AI etkilesimlerinden ogrenci bazli ogrenme analitikleri. "
        "Ders ilerleme grafigi, haftalik aktivite, veli/ogretmen raporu.",
        banner_type="info", icon="📊")

    calisma_log = _lj("calisma_log.json")
    konu_puanlari = _lj("konu_puanlari.json")
    planlar = _lj("ogrenme_planlari.json")

    sub = st.tabs(["👤 Ogrenci Analiz", "📈 Ders Ilerleme", "📨 Veli Raporu", "👨‍🏫 Ogretmen Ozeti"])

    # ── ÖĞRENCİ ANALİZ ──
    with sub[0]:
        styled_section("Bireysel Ogrenme Analizi")
        ogr = _ogr_sec("ga_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"

            ogr_cal = [c for c in calisma_log if c.get("ogrenci") == ogr_ad]
            ogr_kp = [k for k in konu_puanlari if k.get("ogrenci") == ogr_ad]
            ogr_plan = [p for p in planlar if p.get("ogrenci") == ogr_ad]

            toplam_dk = sum(c.get("sure_dk", 0) for c in ogr_cal)
            ders_say = len(set(c.get("ders","") for c in ogr_cal))
            plan_tamamlanan = sum(1 for p in ogr_plan if p.get("durum") == "Tamamlandi")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,#8b5cf630);border:2px solid #8b5cf6;
                border-radius:18px;padding:20px 24px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                    <div><div style="color:#8b5cf6;font-weight:900;font-size:1.8rem;">{toplam_dk}</div><div style="color:#64748b;font-size:0.65rem;">dakika</div></div>
                    <div><div style="color:#3b82f6;font-weight:900;font-size:1.8rem;">{ders_say}</div><div style="color:#64748b;font-size:0.65rem;">ders</div></div>
                    <div><div style="color:#10b981;font-weight:900;font-size:1.8rem;">{plan_tamamlanan}</div><div style="color:#64748b;font-size:0.65rem;">plan</div></div>
                    <div><div style="color:#f59e0b;font-weight:900;font-size:1.8rem;">{len(ogr_cal)}</div><div style="color:#64748b;font-size:0.65rem;">oturum</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Ders bazli calisma
            if ogr_cal:
                styled_section("Ders Bazli Calisma")
                ders_dk = defaultdict(int)
                for c in ogr_cal:
                    ders_dk[c.get("ders","")] += c.get("sure_dk", 0)
                for ders, dk in sorted(ders_dk.items(), key=lambda x: x[1], reverse=True):
                    pct = round(dk / max(toplam_dk, 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                        <span style="min-width:120px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{ders}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#8b5cf6;border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                                <span style="font-size:0.55rem;color:#fff;font-weight:700;">{dk} dk</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    # ── DERS İLERLEME ──
    with sub[1]:
        styled_section("Ders Ilerleme Grafigi")
        if not konu_puanlari:
            st.info("Konu puani verisi yok.")
        else:
            ders_ort = defaultdict(list)
            for k in konu_puanlari:
                ders_ort[k.get("ders","?")].append(k.get("puan", 0))

            for ders, puanlar in sorted(ders_ort.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
                ort = round(sum(puanlar) / max(len(puanlar), 1))
                _, d_renk, _ = _mastery_label(ort)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{ders}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{ort}%;height:100%;background:{d_renk};border-radius:6px;
                            display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{ort}%</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{len(puanlar)} konu</span>
                </div>""", unsafe_allow_html=True)

    # ── VELİ RAPORU ──
    with sub[2]:
        styled_section("Haftalik Veli Raporu")
        ogr2 = _ogr_sec("ga_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
            hafta_cal = [c for c in calisma_log if c.get("ogrenci") == ogr_ad2 and c.get("tarih","")[:10] >= bu_hafta]
            toplam_dk = sum(c.get("sure_dk", 0) for c in hafta_cal)
            ders_dk = defaultdict(int)
            for c in hafta_cal:
                ders_dk[c.get("ders","")] += c.get("sure_dk", 0)

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #8b5cf6;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">📨 Haftalik Veli Raporu</div>
                    <div style="color:#c4b5fd;font-size:0.8rem;">{ogr_ad2}</div>
                    <div style="color:#94a3b8;font-size:0.72rem;">{bu_hafta[5:]} — {date.today().isoformat()[5:]}</div>
                </div>
                <div style="text-align:center;margin-top:10px;">
                    <div style="color:#8b5cf6;font-weight:900;font-size:2rem;">{toplam_dk} dk</div>
                    <div style="color:#64748b;font-size:0.72rem;">toplam calisma suresi</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if ders_dk:
                styled_section("Ders Dagilimi")
                for ders, dk in sorted(ders_dk.items(), key=lambda x: x[1], reverse=True):
                    st.markdown(f"- 📚 **{ders}**: {dk} dakika")
            else:
                st.info("Bu hafta calisma kaydi yok.")

            st.caption("Bu rapor veliye otomatik gonderilebilir.")

    # ── ÖĞRETMEN ÖZETİ ──
    with sub[3]:
        styled_section("Sinif Bazli AI Kullanim Ozeti (Ogretmen)")
        if not calisma_log:
            st.info("Calisma verisi yok.")
        else:
            ogr_dk = defaultdict(int)
            for c in calisma_log:
                ogr_dk[c.get("ogrenci","")] += c.get("sure_dk", 0)

            styled_section("En Aktif Ogrenciler")
            for sira, (ogr, dk) in enumerate(sorted(ogr_dk.items(), key=lambda x: x[1], reverse=True)[:10], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;">
                    <span style="font-size:1rem;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;flex:1;">{ogr}</span>
                    <span style="color:#8b5cf6;font-weight:800;">{dk} dk</span>
                </div>""", unsafe_allow_html=True)

            # Ders bazli genel
            styled_section("Ders Bazli Toplam")
            ders_toplam = defaultdict(int)
            for c in calisma_log:
                ders_toplam[c.get("ders","")] += c.get("sure_dk", 0)
            for ders, dk in sorted(ders_toplam.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"- **{ders}**: {dk} dk ({sum(1 for c in calisma_log if c.get('ders') == ders)} oturum)")
