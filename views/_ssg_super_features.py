"""
Sivil Savunma, ISG ve Okul Güvenliği - SÜPER Özellikler
1. Güvenlik Eğitim Akademisi & Sertifikasyon
2. ISG Ölçüm & Çevresel İzleme Merkezi
3. Zorbalık & Şiddet Önleme Komuta Merkezi
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter


# ── Ortak stil ──
def _styled_header(title, icon="🎓"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:18px 24px;border-radius:14px;margin-bottom:18px;">
        <h2 style="color:#e94560;margin:0;font-size:1.5rem;">{icon} {title}</h2>
    </div>""", unsafe_allow_html=True)

def _styled_section(title, color="#e94560"):
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,{color}22,transparent);border-left:4px solid {color};padding:10px 16px;border-radius:0 10px 10px 0;margin:14px 0 10px 0;">
        <strong style="color:{color};font-size:1.05rem;">{title}</strong>
    </div>""", unsafe_allow_html=True)

def _styled_stat_row(stats):
    cols = st.columns(len(stats))
    colors = ["#e94560", "#0f3460", "#00b4d8", "#06d6a0", "#ffd166", "#8338ec", "#ff6b6b"]
    for i, (label, value) in enumerate(stats):
        c = colors[i % len(colors)]
        cols[i].markdown(f"""
        <div style="background:linear-gradient(135deg,{c}18,{c}08);border:1px solid {c}40;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-size:1.6rem;font-weight:800;color:{c};">{value}</div>
            <div style="font-size:0.78rem;color:#888;margin-top:2px;">{label}</div>
        </div>""", unsafe_allow_html=True)

def _styled_info_banner(text, color="#00b4d8"):
    st.markdown(f"""
    <div style="background:{color}12;border:1px solid {color}40;border-radius:10px;padding:12px 16px;margin:10px 0;">
        <span style="color:{color};font-size:0.92rem;">{text}</span>
    </div>""", unsafe_allow_html=True)

def _get_data_path(store, filename):
    if hasattr(store, 'base_dir'):
        return os.path.join(store.base_dir, filename)
    return os.path.join("data", "ssg", filename)

def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. GÜVENLİK EĞİTİM AKADEMİSİ & SERTİFİKASYON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_egitim_akademisi(store):
    _styled_header("Guvenlik Egitim Akademisi & Sertifikasyon", "🎓")

    egitim_path = _get_data_path(store, "guvenlik_egitimleri.json")
    egitimler = _load_json(egitim_path)

    quiz_path = _get_data_path(store, "guvenlik_quizler.json")
    quizler = _load_json(quiz_path)

    sertifika_path = _get_data_path(store, "guvenlik_sertifikalari.json")
    sertifikalar = _load_json(sertifika_path)

    takvim_path = _get_data_path(store, "egitim_takvimi.json")
    takvim = _load_json(takvim_path)

    _styled_stat_row([
        ("Egitim Modulu", len(egitimler)),
        ("Quiz", len(quizler)),
        ("Sertifika", len(sertifikalar)),
        ("Takvim Kaydi", len(takvim)),
    ])

    sub = st.tabs(["📚 Egitim Modulleri", "📝 Quiz & Sinav", "🎖️ Sertifika", "📅 Yillik Takvim", "👥 Katilim Takip", "📊 Analitik"])

    # ── Eğitim Modülleri ──
    with sub[0]:
        _styled_section("📚 Guvenlik Egitim Modulleri", "#0f3460")

        with st.form("egitim_modul_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_baslik = st.text_input("Egitim Basligi", key="ge_baslik")
                e_kategori = st.selectbox("Kategori", [
                    "Deprem Egitimi", "Yangin Egitimi", "Ilk Yardim",
                    "ISG Temel", "Kimyasal Guvenlik", "Elektrik Guvenligi",
                    "Yuksekte Calisma", "Tahliye Proseduru", "Trafik Guvenligi",
                    "Siber Guvenlik", "Cocuk Koruma", "Genel"
                ], key="ge_kat")
                e_hedef = st.multiselect("Hedef Kitle", ["Tum Personel", "Ogretmenler", "Idari", "Teknik", "Ogrenciler", "Veliler"], key="ge_hedef")
            with ec2:
                e_sure = st.number_input("Sure (dk)", min_value=5, value=45, key="ge_sure")
                e_zorunlu = st.checkbox("Zorunlu Egitim", value=True, key="ge_zorunlu")
                e_periyot = st.selectbox("Tekrar Periyodu", ["Tek Seferlik", "3 Ayda Bir", "6 Ayda Bir", "Yilda Bir"], key="ge_periyot")
            e_icerik = st.text_area("Icerik Ozeti", height=68, key="ge_icerik")

            if st.form_submit_button("📚 Egitim Modulu Ekle", use_container_width=True):
                if e_baslik:
                    egitimler.append({
                        "id": f"ge_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": e_baslik,
                        "kategori": e_kategori,
                        "hedef": e_hedef,
                        "sure": e_sure,
                        "zorunlu": e_zorunlu,
                        "periyot": e_periyot,
                        "icerik": e_icerik,
                        "katilimcilar": [],
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(egitim_path, egitimler)
                    st.success(f"'{e_baslik}' egitim modulu eklendi!")
                    st.rerun()

        if egitimler:
            for e in egitimler:
                zorunlu_badge = "🔴 Zorunlu" if e.get("zorunlu") else "🔵 Istege Bagli"
                katilimci = len(e.get("katilimcilar", []))
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{e.get('baslik','')}</strong>
                        <div style="color:#888;font-size:0.78rem;">{e.get('kategori','')} | {e.get('sure','')} dk | {e.get('periyot','')}</div>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.78rem;">{zorunlu_badge}</span>
                        <div style="color:#00b4d8;font-size:0.78rem;">{katilimci} katilimci</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Quiz & Sınav ──
    with sub[1]:
        _styled_section("📝 Guvenlik Quiz & Sinav Olustur", "#8338ec")

        with st.form("quiz_form"):
            qc1, qc2 = st.columns(2)
            with qc1:
                q_baslik = st.text_input("Quiz Adi", key="gq_baslik")
                q_egitim = st.selectbox("Ilgili Egitim", ["Genel"] + [e.get("baslik", "") for e in egitimler], key="gq_egitim")
            with qc2:
                q_soru = st.number_input("Soru Sayisi", min_value=3, value=10, key="gq_soru")
                q_gecme = st.number_input("Gecme Puani (%)", min_value=50, max_value=100, value=70, key="gq_gecme")
            q_sorular = st.text_area("Sorulari girin (her satir bir soru)", height=100, key="gq_sorular")

            if st.form_submit_button("📝 Quiz Olustur", use_container_width=True):
                if q_baslik:
                    soru_list = [s.strip() for s in q_sorular.split("\n") if s.strip()] if q_sorular else []
                    quizler.append({
                        "id": f"gq_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": q_baslik,
                        "egitim": q_egitim,
                        "soru_sayisi": q_soru,
                        "gecme_puani": q_gecme,
                        "sorular": soru_list,
                        "sonuclar": [],
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(quiz_path, quizler)
                    st.success(f"Quiz '{q_baslik}' olusturuldu!")
                    st.rerun()

        if quizler:
            for idx, q in enumerate(quizler):
                katilimci = len(q.get("sonuclar", []))
                gecen = len([s for s in q.get("sonuclar", []) if s.get("puan", 0) >= q.get("gecme_puani", 70)])
                with st.expander(f"📝 {q.get('baslik','')} ({katilimci} katilimci, {gecen} basarili)"):
                    rc1, rc2 = st.columns(2)
                    with rc1:
                        r_kisi = st.text_input("Katilimci", key=f"gq_kisi_{idx}")
                    with rc2:
                        r_puan = st.number_input("Puan (%)", min_value=0, max_value=100, value=0, key=f"gq_puan_{idx}")
                    if st.button("Sonuc Kaydet", key=f"gq_btn_{idx}"):
                        if r_kisi:
                            q.setdefault("sonuclar", []).append({"kisi": r_kisi, "puan": r_puan, "tarih": datetime.now().isoformat()})
                            _save_json(quiz_path, quizler)
                            if r_puan >= q.get("gecme_puani", 70):
                                sertifikalar.append({
                                    "id": f"gsrt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                    "kisi": r_kisi,
                                    "egitim": q.get("egitim", ""),
                                    "quiz": q.get("baslik", ""),
                                    "puan": r_puan,
                                    "tarih": datetime.now().isoformat(),
                                })
                                _save_json(sertifika_path, sertifikalar)
                                st.success(f"{r_kisi} sertifika kazandi! 🎉")
                            else:
                                st.warning(f"Gecme puani: %{q.get('gecme_puani','')}")
                            st.rerun()

    # ── Sertifika ──
    with sub[2]:
        _styled_section("🎖️ Kazanilan Sertifikalar", "#06d6a0")

        if sertifikalar:
            for s in reversed(sertifikalar[-12:]):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#06d6a010,#16213e);border:1px solid #06d6a030;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:1.2rem;">🎖️</span>
                        <strong style="color:#06d6a0;margin-left:6px;">{s.get('kisi','')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{s.get('egitim','')} — {s.get('quiz','')}</span>
                    </div>
                    <div>
                        <span style="color:#ffd166;font-weight:700;">%{s.get('puan','')}</span>
                        <span style="color:#888;font-size:0.75rem;margin-left:8px;">{s.get('tarih','')[:10]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henuz sertifika verilmedi. Quiz tamamlandiginda otomatik olusur.")

    # ── Yıllık Takvim ──
    with sub[3]:
        _styled_section("📅 Yillik Zorunlu Egitim Takvimi", "#ffd166")

        with st.form("takvim_form"):
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                t_egitim = st.selectbox("Egitim", [e.get("baslik", "") for e in egitimler] if egitimler else ["Egitim ekleyin"], key="tk_egitim")
            with tc2:
                t_tarih = st.date_input("Planlanan Tarih", value=datetime.now().date() + timedelta(days=30), key="tk_tarih")
            with tc3:
                t_hedef_kitle = st.text_input("Hedef Kitle", key="tk_hedef")

            if st.form_submit_button("📅 Takvime Ekle", use_container_width=True):
                takvim.append({
                    "egitim": t_egitim,
                    "tarih": str(t_tarih),
                    "hedef_kitle": t_hedef_kitle,
                    "durum": "planli",
                    "kayit_tarihi": datetime.now().isoformat(),
                })
                _save_json(takvim_path, takvim)
                st.success("Egitim takvime eklendi!")
                st.rerun()

        if takvim:
            bugun = str(datetime.now().date())
            for t in sorted(takvim, key=lambda x: x.get("tarih", "")):
                gecmis = t.get("tarih", "9999") < bugun
                renk = "#888" if gecmis else ("#ffd166" if t.get("durum") == "planli" else "#06d6a0")
                ikon = "✅" if t.get("durum") == "tamamlandi" else ("⏰" if not gecmis else "⚠️")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span>{ikon} <strong style="color:#e0e0e0;">{t.get('egitim','')}</strong> <span style="color:#888;font-size:0.78rem;">({t.get('hedef_kitle','')})</span></span>
                    <span style="color:{renk};font-weight:600;">{t.get('tarih','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Katılım Takip ──
    with sub[4]:
        _styled_section("👥 Egitim Katilim Takibi", "#00b4d8")

        if egitimler:
            secilen = st.selectbox("Egitim Secin", [e.get("baslik", "") for e in egitimler], key="kt_sec")
            secilen_egitim = next((e for e in egitimler if e.get("baslik") == secilen), None)

            if secilen_egitim:
                katilimcilar = secilen_egitim.get("katilimcilar", [])
                st.markdown(f"**{len(katilimcilar)} katilimci kayitli**")

                yeni_kisi = st.text_input("Katilimci Ekle", key="kt_kisi")
                if st.button("Ekle", key="kt_btn"):
                    if yeni_kisi:
                        secilen_egitim.setdefault("katilimcilar", []).append({"kisi": yeni_kisi, "tarih": datetime.now().isoformat()})
                        _save_json(egitim_path, egitimler)
                        st.success(f"{yeni_kisi} katilimci olarak eklendi!")
                        st.rerun()

                for k in katilimcilar:
                    st.markdown(f"""
                    <div style="background:#1a1a2e;border-radius:6px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                        <span style="color:#e0e0e0;">👤 {k.get('kisi','')}</span>
                        <span style="color:#888;font-size:0.75rem;">{k.get('tarih','')[:10]}</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Katilim takibi icin egitim modulu olusturun.")

    # ── Analitik ──
    with sub[5]:
        _styled_section("📊 Egitim Analitikleri", "#8338ec")

        _styled_stat_row([
            ("Egitim Modulu", len(egitimler)),
            ("Toplam Sertifika", len(sertifikalar)),
            ("Quiz Sayisi", len(quizler)),
            ("Toplam Katilim", sum(len(e.get("katilimcilar", [])) for e in egitimler)),
        ])

        if egitimler:
            _styled_section("Kategori Dagilimi", "#ffd166")
            kat_sayim = Counter(e.get("kategori", "Genel") for e in egitimler)
            for kat, sayi in sorted(kat_sayim.items(), key=lambda x: -x[1]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">{kat}</span>
                    <span style="color:#ffd166;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

        # Akademi skoru
        aktivite = len(egitimler) + len(sertifikalar) + len(quizler)
        skor = min(100, aktivite * 5 + 20)
        renk = "#06d6a0" if skor >= 70 else ("#ffd166" if skor >= 40 else "#e94560")
        st.markdown(f"""
        <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
            <div style="color:#888;">Egitim Akademisi Olgunluk Skoru</div>
            <div style="font-size:3rem;font-weight:800;color:{renk};">{skor}/100</div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. ISG ÖLÇÜM & ÇEVRESEL İZLEME MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_isg_olcum(store):
    _styled_header("ISG Olcum & Cevresel Izleme Merkezi", "🔬")

    olcum_path = _get_data_path(store, "isg_olcumler.json")
    olcumler = _load_json(olcum_path)

    limit_path = _get_data_path(store, "isg_limitler.json")
    limitler = _load_json(limit_path)

    _styled_stat_row([
        ("Olcum Kaydi", len(olcumler)),
        ("Limit Tanimi", len(limitler)),
        ("Asim Tespit", len([o for o in olcumler if o.get("asim")])),
    ])

    sub = st.tabs(["📊 Olcum Kayit", "📏 Limit Tanimlari", "🚨 Asim Alarmlari", "🗺️ Ortam Risk Haritasi", "📅 Olcum Takvimi", "📈 Uyumluluk"])

    # ── Ölçüm Kayıt ──
    with sub[0]:
        _styled_section("📊 ISG Olcum Kaydi Olustur", "#00b4d8")

        with st.form("olcum_form"):
            oc1, oc2 = st.columns(2)
            with oc1:
                o_tur = st.selectbox("Olcum Turu", [
                    "Gurultu (dB)", "Aydinlatma (lux)", "Sicaklik (C)",
                    "Nem (%)", "CO2 (ppm)", "Toz (mg/m3)",
                    "Kimyasal Maruz Kalma", "Titresim", "Radyasyon"
                ], key="isg_tur")
                o_deger = st.number_input("Olcum Degeri", min_value=0.0, step=0.1, key="isg_deger")
            with oc2:
                o_konum = st.text_input("Konum (Bina/Oda)", key="isg_konum")
                o_tarih = st.date_input("Tarih", value=datetime.now().date(), key="isg_tarih")
            o_olcen = st.text_input("Olcumu Yapan", key="isg_olcen")

            if st.form_submit_button("📊 Olcum Kaydet", use_container_width=True):
                if o_konum:
                    # Limit kontrolü
                    asim = False
                    ilgili_limit = next((l for l in limitler if l.get("tur") == o_tur), None)
                    if ilgili_limit:
                        max_val = ilgili_limit.get("max_deger", 9999)
                        if o_deger > max_val:
                            asim = True

                    olcumler.append({
                        "id": f"isgm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "tur": o_tur,
                        "deger": o_deger,
                        "konum": o_konum,
                        "tarih": str(o_tarih),
                        "olcen": o_olcen,
                        "asim": asim,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(olcum_path, olcumler)
                    if asim:
                        st.error(f"🚨 LIMIT ASIMI! {o_tur}: {o_deger} (Max: {ilgili_limit.get('max_deger','')})")
                    else:
                        st.success("Olcum kaydedildi!")
                    st.rerun()

        if olcumler:
            _styled_section("Son Olcumler", "#06d6a0")
            for o in reversed(olcumler[-12:]):
                asim = o.get("asim", False)
                renk = "#e94560" if asim else "#06d6a0"
                ikon = "🚨" if asim else "✅"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{o.get('tur','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{o.get('konum','')}</span>
                    </div>
                    <div>
                        <span style="color:{renk};font-weight:700;">{o.get('deger','')}</span>
                        <span style="color:#888;font-size:0.75rem;margin-left:8px;">{o.get('tarih','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Limit Tanımları ──
    with sub[1]:
        _styled_section("📏 Yasal Limit Tanimlari", "#ffd166")

        with st.form("limit_form"):
            lc1, lc2, lc3 = st.columns(3)
            with lc1:
                l_tur = st.selectbox("Olcum Turu", [
                    "Gurultu (dB)", "Aydinlatma (lux)", "Sicaklik (C)",
                    "Nem (%)", "CO2 (ppm)", "Toz (mg/m3)"
                ], key="lmt_tur")
            with lc2:
                l_min = st.number_input("Min Deger", value=0.0, key="lmt_min")
            with lc3:
                l_max = st.number_input("Max Deger", value=85.0, key="lmt_max")
            l_mevzuat = st.text_input("Yasal Dayanak", key="lmt_mevzuat")

            if st.form_submit_button("📏 Limit Tanimla", use_container_width=True):
                limitler.append({
                    "tur": l_tur,
                    "min_deger": l_min,
                    "max_deger": l_max,
                    "mevzuat": l_mevzuat,
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(limit_path, limitler)
                st.success("Limit tanimi eklendi!")
                st.rerun()

        if limitler:
            for l in limitler:
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;font-weight:600;">{l.get('tur','')}</span>
                    <span style="color:#ffd166;">Min: {l.get('min_deger','')} | Max: {l.get('max_deger','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Aşım Alarmları ──
    with sub[2]:
        _styled_section("🚨 Limit Asim Alarmlari", "#e94560")

        asimlar = [o for o in olcumler if o.get("asim")]
        if asimlar:
            st.error(f"🚨 {len(asimlar)} limit asimi tespit edildi!")
            for a in reversed(asimlar[-10:]):
                st.markdown(f"""
                <div style="background:#e9456012;border-left:4px solid #e94560;padding:10px 14px;border-radius:0 10px 10px 0;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;">
                        <strong style="color:#e94560;">{a.get('tur','')}</strong>
                        <span style="color:#888;font-size:0.78rem;">{a.get('tarih','')}</span>
                    </div>
                    <div style="color:#aaa;font-size:0.85rem;">Deger: {a.get('deger','')} | Konum: {a.get('konum','')}</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Limit asimi bulunmuyor. Tum olcumler normal. ✅")

    # ── Ortam Risk Haritası ──
    with sub[3]:
        _styled_section("🗺️ Konum Bazli Ortam Risk Haritasi", "#8338ec")

        if olcumler:
            konum_risk = {}
            for o in olcumler:
                k = o.get("konum", "?")
                if k not in konum_risk:
                    konum_risk[k] = {"toplam": 0, "asim": 0}
                konum_risk[k]["toplam"] += 1
                if o.get("asim"):
                    konum_risk[k]["asim"] += 1

            for konum, data in sorted(konum_risk.items(), key=lambda x: -x[1]["asim"]):
                asim_oran = int(data["asim"] / max(1, data["toplam"]) * 100)
                renk = "#e94560" if asim_oran >= 30 else ("#ffd166" if asim_oran >= 10 else "#06d6a0")
                seviye = "YUKSEK RISK" if asim_oran >= 30 else ("ORTA" if asim_oran >= 10 else "DUSUK")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{konum}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{data['toplam']} olcum, {data['asim']} asim</span>
                    </div>
                    <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:6px;font-weight:600;font-size:0.82rem;">{seviye}</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Ortam risk haritasi icin olcum verisi gerekiyor.")

    # ── Ölçüm Takvimi ──
    with sub[4]:
        _styled_section("📅 Periyodik Olcum Takvimi", "#06d6a0")

        olcum_takvim_path = _get_data_path(store, "olcum_takvimi.json")
        olcum_takvim = _load_json(olcum_takvim_path)

        with st.form("olcum_takvim_form"):
            otc1, otc2, otc3 = st.columns(3)
            with otc1:
                ot_tur = st.selectbox("Olcum Turu", ["Gurultu", "Aydinlatma", "Sicaklik", "Hava Kalitesi", "Toz", "Genel"], key="ot_tur")
            with otc2:
                ot_periyot = st.selectbox("Periyot", ["Aylik", "3 Aylik", "6 Aylik", "Yillik"], key="ot_per")
            with otc3:
                ot_sonraki = st.date_input("Sonraki Olcum", value=datetime.now().date() + timedelta(days=30), key="ot_tarih")

            if st.form_submit_button("📅 Takvime Ekle", use_container_width=True):
                olcum_takvim.append({"tur": ot_tur, "periyot": ot_periyot, "sonraki": str(ot_sonraki), "tarih": datetime.now().isoformat()})
                _save_json(olcum_takvim_path, olcum_takvim)
                st.success("Olcum takvime eklendi!")
                st.rerun()

        if olcum_takvim:
            bugun = str(datetime.now().date())
            for ot in sorted(olcum_takvim, key=lambda x: x.get("sonraki", "")):
                gecmis = ot.get("sonraki", "9999") < bugun
                renk = "#e94560" if gecmis else "#06d6a0"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">{ot.get('tur','')} ({ot.get('periyot','')})</span>
                    <span style="color:{renk};font-weight:600;">{ot.get('sonraki','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Uyumluluk ──
    with sub[5]:
        _styled_section("📈 Yasal Uyumluluk Durumu", "#06d6a0")

        toplam = len(olcumler)
        asim_sayi = len([o for o in olcumler if o.get("asim")])
        uyum_oran = int((toplam - asim_sayi) / max(1, toplam) * 100) if toplam else 100
        renk = "#06d6a0" if uyum_oran >= 90 else ("#ffd166" if uyum_oran >= 70 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;">
            <div style="color:#888;">ISG Yasal Uyumluluk Orani</div>
            <div style="font-size:3.5rem;font-weight:900;color:{renk};">%{uyum_oran}</div>
            <div style="color:#aaa;font-size:0.85rem;">{toplam} olcum, {asim_sayi} asim</div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. ZORBALIK & ŞİDDET ÖNLEME KOMUTA MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_zorbalik_onleme(store):
    _styled_header("Zorbalik & Siddet Onleme Komuta Merkezi", "🛡️")

    ihbar_path = _get_data_path(store, "zorbalik_ihbarlari.json")
    ihbarlar = _load_json(ihbar_path)

    mudahale_path = _get_data_path(store, "mudahale_kayitlari.json")
    mudahaleler = _load_json(mudahale_path)

    aktif = [i for i in ihbarlar if i.get("durum") in ("acik", "inceleniyor")]
    cozulen = [i for i in ihbarlar if i.get("durum") == "cozuldu"]

    _styled_stat_row([
        ("Toplam Ihbar", len(ihbarlar)),
        ("Aktif Inceleme", len(aktif)),
        ("Cozulen", len(cozulen)),
        ("Mudahale Kaydi", len(mudahaleler)),
    ])

    sub = st.tabs(["📢 Anonim Ihbar", "📋 Olay Takip", "🔄 Mudahale Protokolu", "📊 Tekrar Analizi", "🏫 Guvenli Okul Endeksi", "👨‍👩‍👧 Veli & Psikolog"])

    # ── Anonim İhbar ──
    with sub[0]:
        _styled_section("📢 Anonim Ihbar Hatti", "#e94560")

        _styled_info_banner("Ihbar verenin kimligi gizli tutulur. Sadece yetkililer gorebilir.")

        with st.form("ihbar_form"):
            ic1, ic2 = st.columns(2)
            with ic1:
                i_tur = st.selectbox("Ihbar Turu", [
                    "Fiziksel Zorbalik", "Sozel Zorbalik", "Siber Zorbalik",
                    "Dislanma/Izolasyon", "Cinsel Taciz/Istismar",
                    "Madde Kullanimi", "Silah/Kesici Alet", "Genel Siddet", "Diger"
                ], key="zih_tur")
                i_ciddiyet = st.selectbox("Ciddiyet", ["Dusuk", "Orta", "Yuksek", "Acil"], key="zih_cid")
            with ic2:
                i_konum = st.text_input("Olay Yeri / Sinif", key="zih_konum")
                i_tarih = st.date_input("Olay Tarihi", value=datetime.now().date(), key="zih_tarih")
            i_aciklama = st.text_area("Olay Aciklamasi", height=80, key="zih_acik")
            i_anonim = st.checkbox("Anonim olarak bildir", value=True, key="zih_anonim")
            if not i_anonim:
                i_bildiren = st.text_input("Bildiren Kisi (opsiyonel)", key="zih_bildiren")
            else:
                i_bildiren = "Anonim"

            if st.form_submit_button("📢 Ihbar Gonder", use_container_width=True):
                if i_aciklama:
                    ihbarlar.append({
                        "id": f"zih_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "tur": i_tur,
                        "ciddiyet": i_ciddiyet,
                        "konum": i_konum,
                        "tarih": str(i_tarih),
                        "aciklama": i_aciklama,
                        "bildiren": i_bildiren,
                        "durum": "acik",
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(ihbar_path, ihbarlar)
                    st.success("Ihbar kaydedildi. Yetkililer bilgilendirilecek.")
                    st.rerun()

    # ── Olay Takip ──
    with sub[1]:
        _styled_section("📋 Ihbar & Olay Takip Listesi", "#8338ec")

        if ihbarlar:
            durum_filtre = st.selectbox("Durum Filtresi", ["Tumu", "acik", "inceleniyor", "cozuldu", "kapali"], key="zih_filtre")
            filtreli = ihbarlar if durum_filtre == "Tumu" else [i for i in ihbarlar if i.get("durum") == durum_filtre]

            for idx, ih in enumerate(reversed(filtreli[:15])):
                durum = ih.get("durum", "acik")
                cid = ih.get("ciddiyet", "Orta")
                durum_ikon = {"acik": "🔴", "inceleniyor": "🟡", "cozuldu": "🟢", "kapali": "⚫"}.get(durum, "⚪")
                cid_renk = {"Dusuk": "#06d6a0", "Orta": "#ffd166", "Yuksek": "#ff6b6b", "Acil": "#e94560"}.get(cid, "#888")

                with st.expander(f"{durum_ikon} {ih.get('tur','?')} — {ih.get('konum','')} ({cid})"):
                    st.write(f"**Aciklama:** {ih.get('aciklama','')}")
                    st.write(f"**Tarih:** {ih.get('tarih','')} | **Bildiren:** {ih.get('bildiren','Anonim')}")

                    yeni_durum = st.selectbox("Durum", ["acik", "inceleniyor", "cozuldu", "kapali"], index=["acik", "inceleniyor", "cozuldu", "kapali"].index(durum), key=f"zih_d_{idx}")
                    if st.button("Guncelle", key=f"zih_btn_{idx}"):
                        ih["durum"] = yeni_durum
                        _save_json(ihbar_path, ihbarlar)
                        st.rerun()
        else:
            _styled_info_banner("Henuz ihbar kaydi yok.")

    # ── Müdahale Protokolü ──
    with sub[2]:
        _styled_section("🔄 Mudahale Protokolu & Kayit", "#06d6a0")

        with st.form("mudahale_form"):
            mc1, mc2 = st.columns(2)
            with mc1:
                m_ihbar = st.text_input("Ilgili Ihbar No / Olay", key="mud_ihbar")
                m_mudahale = st.selectbox("Mudahale Turu", [
                    "Gorusme (Ogrenci)", "Gorusme (Veli)", "Disiplin Islemi",
                    "Psikolog Yonlendirme", "Arabuluculuk", "Sinif Degisikligi",
                    "Guvenlik Onlemi", "Yasal Islem Bildirimi", "Izleme"
                ], key="mud_tur")
            with mc2:
                m_yapan = st.text_input("Mudahale Eden", key="mud_yapan")
                m_sonuc = st.selectbox("Sonuc", ["Devam Ediyor", "Basarili", "Kismi Basarili", "Yetersiz"], key="mud_sonuc")
            m_not = st.text_area("Notlar", height=60, key="mud_not")

            if st.form_submit_button("🔄 Mudahale Kaydet", use_container_width=True):
                if m_ihbar:
                    mudahaleler.append({
                        "id": f"mud_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ihbar": m_ihbar,
                        "mudahale": m_mudahale,
                        "yapan": m_yapan,
                        "sonuc": m_sonuc,
                        "notlar": m_not,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(mudahale_path, mudahaleler)
                    st.success("Mudahale kaydedildi!")
                    st.rerun()

        if mudahaleler:
            for m in reversed(mudahaleler[-10:]):
                sonuc_renk = {"Basarili": "#06d6a0", "Kismi Basarili": "#ffd166", "Yetersiz": "#e94560", "Devam Ediyor": "#00b4d8"}.get(m.get("sonuc", ""), "#888")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{m.get('mudahale','')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">Ihbar: {m.get('ihbar','')} | {m.get('yapan','')}</span>
                    </div>
                    <span style="color:{sonuc_renk};font-weight:600;font-size:0.82rem;">{m.get('sonuc','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Tekrar Analizi ──
    with sub[3]:
        _styled_section("📊 Tekrar Eden Olay & Konum Analizi", "#ffd166")

        if ihbarlar:
            # Tür bazlı
            tur_sayim = Counter(i.get("tur", "?") for i in ihbarlar)
            st.markdown("**Olay Turu Dagilimi**")
            max_val = max(tur_sayim.values()) if tur_sayim.values() else 1
            for tur, sayi in sorted(tur_sayim.items(), key=lambda x: -x[1]):
                bar_w = int(sayi / max_val * 100)
                renk = "#e94560" if sayi >= 5 else ("#ffd166" if sayi >= 3 else "#06d6a0")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:180px;color:#e0e0e0;font-size:0.85rem;">{tur}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <span style="width:30px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            # Konum bazlı
            konum_sayim = Counter(i.get("konum", "?") for i in ihbarlar)
            _styled_section("Konum Bazli Yogunluk", "#8338ec")
            for konum, sayi in sorted(konum_sayim.items(), key=lambda x: -x[1])[:8]:
                renk = "#e94560" if sayi >= 3 else "#ffd166"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">📍 {konum}</span>
                    <span style="color:{renk};font-weight:700;">{sayi} olay</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Tekrar analizi icin ihbar verisi gerekiyor.")

    # ── Güvenli Okul Endeksi ──
    with sub[4]:
        _styled_section("🏫 Guvenli Okul Endeksi", "#06d6a0")

        toplam_ihbar = len(ihbarlar)
        cozulen_sayi = len(cozulen)
        cozum_oran = int(cozulen_sayi / max(1, toplam_ihbar) * 100) if toplam_ihbar else 100
        acil_sayi = len([i for i in ihbarlar if i.get("ciddiyet") == "Acil"])

        guvenlik_skor = max(0, 100 - toplam_ihbar * 3 - acil_sayi * 10 + cozulen_sayi * 5)
        guvenlik_skor = min(100, max(0, guvenlik_skor))
        renk = "#06d6a0" if guvenlik_skor >= 70 else ("#ffd166" if guvenlik_skor >= 40 else "#e94560")
        derece = "A" if guvenlik_skor >= 85 else ("B" if guvenlik_skor >= 70 else ("C" if guvenlik_skor >= 50 else "D"))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:0.9rem;color:#888;">Guvenli Okul Endeksi</div>
            <div style="font-size:4rem;font-weight:900;color:{renk};">{derece}</div>
            <div style="font-size:1.4rem;color:{renk};">{guvenlik_skor}/100</div>
        </div>""", unsafe_allow_html=True)

        bilesenler = [
            ("Ihbar Yogunlugu", max(0, 100 - toplam_ihbar * 5), "#00b4d8"),
            ("Cozum Orani", cozum_oran, "#06d6a0"),
            ("Mudahale Etkisi", min(100, len(mudahaleler) * 15 + 30), "#ffd166"),
        ]
        for baslik, skor, renk in bilesenler:
            st.markdown(f"""
            <div style="margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                    <span style="color:#e0e0e0;font-weight:600;">{baslik}</span>
                    <span style="color:{renk};font-weight:700;">{min(100, max(0, skor))}/100</span>
                </div>
                <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                    <div style="width:{min(100, max(0, skor))}%;height:100%;background:{renk};border-radius:6px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── Veli & Psikolog ──
    with sub[5]:
        _styled_section("👨‍👩‍👧 Veli Bilgilendirme & Psikolog Yonlendirme", "#8338ec")

        yonlendirme_path = _get_data_path(store, "psikolog_yonlendirme.json")
        yonlendirmeler = _load_json(yonlendirme_path)

        with st.form("yonlendirme_form"):
            yc1, yc2 = st.columns(2)
            with yc1:
                y_ogrenci = st.text_input("Ogrenci Adi", key="psy_ogr")
                y_neden = st.selectbox("Yonlendirme Nedeni", [
                    "Zorbalik Magduru", "Zorbalik Faili", "Sosyal Izolasyon",
                    "Agresif Davranis", "Kaygi/Depresyon Belirtisi",
                    "Travma Sonrasi", "Aile Ici Sorun", "Genel Destek"
                ], key="psy_neden")
            with yc2:
                y_psikolog = st.text_input("Yonlendirilen Psikolog", key="psy_psi")
                y_veli_bilgi = st.checkbox("Veli Bilgilendirildi", value=False, key="psy_veli")
            y_not = st.text_input("Not", key="psy_not")

            if st.form_submit_button("👨‍⚕️ Yonlendirme Olustur", use_container_width=True):
                if y_ogrenci:
                    yonlendirmeler.append({
                        "id": f"psy_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ogrenci": y_ogrenci,
                        "neden": y_neden,
                        "psikolog": y_psikolog,
                        "veli_bilgi": y_veli_bilgi,
                        "notlar": y_not,
                        "durum": "aktif",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(yonlendirme_path, yonlendirmeler)
                    st.success(f"{y_ogrenci} psikolog yonlendirmesi olusturuldu!")
                    st.rerun()

        if yonlendirmeler:
            for y in reversed(yonlendirmeler[-10:]):
                veli = "✅ Bilgilendirildi" if y.get("veli_bilgi") else "⏳ Bilgilendirilmedi"
                veli_renk = "#06d6a0" if y.get("veli_bilgi") else "#ffd166"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;">👤 {y.get('ogrenci','')}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{y.get('neden','')}</span>
                        </div>
                        <span style="color:{veli_renk};font-size:0.8rem;">{veli}</span>
                    </div>
                    <div style="color:#888;font-size:0.78rem;margin-top:3px;">Psikolog: {y.get('psikolog','')} | {y.get('tarih','')[:10]}</div>
                </div>""", unsafe_allow_html=True)
