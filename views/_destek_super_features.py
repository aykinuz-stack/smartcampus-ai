"""
Destek Hizmetleri - SÜPER Özellikler
1. AI Kök Neden Analizi & Tekrar Eden Arıza Motoru
2. Mobil Saha Ekibi & Görev Takip Merkezi
3. Otomatik Eskalasyon & İş Akışı Motoru
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter


# ── Ortak stil ──
def _styled_header(title, icon="🧠"):
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
    return os.path.join("data", "destek", filename)

def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def _get_attr(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)

def _parse_date(val):
    if isinstance(val, datetime):
        return val
    val_str = str(val)
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(val_str[:len(fmt.replace('%', 'X'))], fmt)
        except (ValueError, IndexError):
            continue
    return datetime.now()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. AI KÖK NEDEN ANALİZİ & TEKRAR EDEN ARIZA MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_kok_neden(store):
    _styled_header("AI Kok Neden Analizi & Tekrar Eden Ariza Motoru", "🧠")

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    cozum_path = _get_data_path(store, "kok_neden_cozumler.json")
    cozumler = _load_json(cozum_path)

    # Tekrar eden arıza tespiti
    tekrar_grup = {}
    for t in tickets:
        lokasyon = _get_attr(t, "lokasyon") or _get_attr(t, "konum") or _get_attr(t, "bina") or ""
        alan = _get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or ""
        anahtar = f"{lokasyon}|{alan}".strip("|")
        if anahtar:
            if anahtar not in tekrar_grup:
                tekrar_grup[anahtar] = []
            tekrar_grup[anahtar].append(t)

    tekrar_eden = {k: v for k, v in tekrar_grup.items() if len(v) >= 2}
    toplam_tekrar = sum(len(v) for v in tekrar_eden.values())

    _styled_stat_row([
        ("Toplam Talep", len(tickets)),
        ("Tekrar Kume Sayisi", len(tekrar_eden)),
        ("Tekrar Eden Talep", toplam_tekrar),
        ("Tekrar Orani", f"%{int(toplam_tekrar / max(1, len(tickets)) * 100)}"),
        ("Kalici Cozum", len(cozumler)),
    ])

    sub = st.tabs(["🔍 Tekrar Tespiti", "🌳 Kok Neden Agaci", "📊 Kume Analizi", "💡 AI Oneri", "✅ Kalici Cozum Takip", "📈 Tekrar Trendi"])

    # ── Tekrar Tespiti ──
    with sub[0]:
        _styled_section("🔍 Tekrar Eden Ariza Kumeleri", "#e94560")

        if tekrar_eden:
            _styled_info_banner(f"{len(tekrar_eden)} kume tespit edildi — ayni lokasyon+alan kombinasyonunda 2+ talep.")

            siralama = sorted(tekrar_eden.items(), key=lambda x: -len(x[1]))
            for anahtar, tlist in siralama[:15]:
                sayi = len(tlist)
                renk = "#e94560" if sayi >= 5 else ("#ffd166" if sayi >= 3 else "#00b4d8")
                seviye = "KRITIK" if sayi >= 5 else ("YUKSEK" if sayi >= 3 else "ORTA")
                parcalar = anahtar.split("|")
                lokasyon = parcalar[0] if parcalar else "?"
                alan = parcalar[1] if len(parcalar) > 1 else ""

                st.markdown(f"""
                <div style="background:{renk}10;border-left:4px solid {renk};padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:{renk};">{lokasyon}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{alan}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px;">
                            <span style="color:{renk};font-weight:700;font-size:1.2rem;">{sayi}x</span>
                            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:600;">{seviye}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            kritik_sayi = len([k for k, v in tekrar_eden.items() if len(v) >= 5])
            if kritik_sayi > 0:
                st.error(f"🚨 {kritik_sayi} kume KRITIK seviyede (5+ tekrar) — kok neden analizi sart!")
        else:
            _styled_info_banner("Tekrar eden ariza kumesi bulunamadi. ✅")

    # ── Kök Neden Ağacı ──
    with sub[1]:
        _styled_section("🌳 Kok Neden Agaci Olusturucu", "#8338ec")

        _styled_info_banner("Bir problemi katmanlara ayirarak kok nedene inin. 5 Neden (5 Why) yontemi.")

        kok_path = _get_data_path(store, "kok_neden_agaclari.json")
        agaclar = _load_json(kok_path)

        with st.form("kok_neden_form"):
            kn_problem = st.text_input("Problem / Ariza Tanimi", key="kn_problem")
            st.markdown("**5 Neden Analizi**")
            kn1 = st.text_input("1. Neden? (Neden bu sorun olustu?)", key="kn_1")
            kn2 = st.text_input("2. Neden? (Neden #1 oldu?)", key="kn_2")
            kn3 = st.text_input("3. Neden? (Neden #2 oldu?)", key="kn_3")
            kn4 = st.text_input("4. Neden? (Neden #3 oldu?)", key="kn_4")
            kn5 = st.text_input("5. Neden? (KOK NEDEN)", key="kn_5")
            kn_cozum = st.text_area("Onerilen Kalici Cozum", height=68, key="kn_cozum")

            if st.form_submit_button("🌳 Analiz Kaydet", use_container_width=True):
                if kn_problem:
                    agaclar.append({
                        "id": f"kn_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "problem": kn_problem,
                        "nedenler": [kn1, kn2, kn3, kn4, kn5],
                        "kok_neden": kn5,
                        "cozum": kn_cozum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(kok_path, agaclar)
                    st.success("Kok neden analizi kaydedildi!")
                    st.rerun()

        if agaclar:
            _styled_section("Kayitli Analizler", "#06d6a0")
            for a in reversed(agaclar[-10:]):
                with st.expander(f"🌳 {a.get('problem','?')[:50]}"):
                    nedenler = a.get("nedenler", [])
                    for i, n in enumerate(nedenler):
                        if n:
                            girinti = "  " * i
                            renk = ["#00b4d8", "#ffd166", "#8338ec", "#ff6b6b", "#e94560"][i]
                            st.markdown(f"""
                            <div style="margin-left:{i*20}px;background:{renk}10;border-left:3px solid {renk};padding:6px 12px;border-radius:0 6px 6px 0;margin-bottom:4px;">
                                <span style="color:{renk};font-weight:600;">Neden {i+1}:</span>
                                <span style="color:#e0e0e0;margin-left:6px;">{n}</span>
                            </div>""", unsafe_allow_html=True)
                    if a.get("cozum"):
                        st.success(f"💡 Onerilen Cozum: {a['cozum']}")

    # ── Küme Analizi ──
    with sub[2]:
        _styled_section("📊 Detayli Kume Analizi", "#00b4d8")

        if tekrar_eden:
            secilen = st.selectbox("Kume Secin", [f"{k} ({len(v)}x)" for k, v in sorted(tekrar_eden.items(), key=lambda x: -len(x[1]))], key="kume_sec")
            secilen_key = secilen.split(" (")[0] if secilen else ""
            kume_tickets = tekrar_eden.get(secilen_key, [])

            if kume_tickets:
                st.markdown(f"**{len(kume_tickets)} talep bu kumede**")

                # Zaman dağılımı
                tarihler = []
                for t in kume_tickets:
                    tarih = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih")
                    if tarih:
                        tarihler.append(str(tarih)[:10])

                if tarihler:
                    st.markdown("**Zaman Dagilimi:**")
                    for trh in sorted(tarihler):
                        st.caption(f"📅 {trh}")

                # Öncelik dağılımı
                oncelik_sayim = Counter(_get_attr(t, "oncelik") or "normal" for t in kume_tickets)
                st.markdown("**Oncelik Dagilimi:**")
                for onc, sayi in oncelik_sayim.items():
                    renk = {"acil": "#e94560", "yuksek": "#ff6b6b", "normal": "#ffd166", "dusuk": "#06d6a0"}.get(onc, "#888")
                    st.markdown(f"<span style='color:{renk};font-weight:600;'>{onc}: {sayi}</span>", unsafe_allow_html=True)

                # Tekrar skoru
                tekrar_skor = min(100, len(kume_tickets) * 15)
                renk = "#e94560" if tekrar_skor >= 60 else ("#ffd166" if tekrar_skor >= 30 else "#06d6a0")
                st.markdown(f"""
                <div style="background:#0f3460;border-radius:10px;padding:14px;text-align:center;margin-top:10px;">
                    <div style="color:#888;">Tekrar Skoru</div>
                    <div style="font-size:2rem;font-weight:800;color:{renk};">{tekrar_skor}/100</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Kume analizi icin tekrar eden ariza gerekiyor.")

    # ── AI Öneri ──
    with sub[3]:
        _styled_section("💡 AI Kok Neden & Cozum Onerileri", "#ffd166")

        _styled_info_banner("AI, tekrar eden ariza kaliplarini analiz ederek kok neden ve kalici cozum onerir.")

        if tekrar_eden:
            st.markdown("**En Kritik Kumeler Icin AI Onerileri:**")
            oneriler_db = {
                "elektrik": ("Elektrik Altyapi Yenileme", "Tekrarlayan elektrik arizalari eski kablo/pano altyapisina isaret ediyor. Bina elektrik tesisat revizyonu planlayin."),
                "tesisat": ("Tesisat Modernizasyonu", "Su/kalorifer tesisatinda tekrar eden sorunlar boru yaslanmasini gosteriyor. Koruyucu bakim plani olusturun."),
                "klima": ("HVAC Preventif Bakim", "Klima/iklimlendirme arizalari periyodik filtre ve gaz kontrolu ile %70 azaltilabilir."),
                "temizlik": ("Temizlik Protokolu Guncelleme", "Tekrar eden temizlik sikayet kumeleri personel rotasyonu veya malzeme degisikligi gerektirebilir."),
                "bilisim": ("IT Altyapi Denetimi", "Ag/bilgisayar sorunlari switch/router yaslanmasina veya bant genisligi yetersizligine isaret edebilir."),
            }

            for anahtar, tlist in sorted(tekrar_eden.items(), key=lambda x: -len(x[1]))[:5]:
                anahtar_lower = anahtar.lower()
                bulunan = None
                for key, (baslik, aciklama) in oneriler_db.items():
                    if key in anahtar_lower:
                        bulunan = (baslik, aciklama)
                        break
                if not bulunan:
                    bulunan = ("Detayli Inceleme Gerekli", f"{anahtar} kumesinde {len(tlist)} tekrar tespit edildi. 5 Neden analizi uygulayin ve kok nedeni belirleyin.")

                renk = "#e94560" if len(tlist) >= 5 else "#ffd166"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <strong style="color:{renk};">{bulunan[0]}</strong>
                        <span style="color:#888;font-size:0.8rem;">{anahtar[:30]} ({len(tlist)}x)</span>
                    </div>
                    <p style="color:#aaa;font-size:0.88rem;margin:0;">{bulunan[1]}</p>
                </div>""", unsafe_allow_html=True)
        else:
            oneriler = [
                ("Proaktif Izleme", "Ariza olmadan once erken uyari sistemi kurun — IoT sensor verileri ve periyodik denetim sonuclari.", "#06d6a0"),
                ("Koruyucu Bakim", "Reaktif (ariza olduktan sonra) yerine preventif (onceden planlanan) bakim stratejisine gecin.", "#00b4d8"),
                ("Veri Toplama", "Her talebe lokasyon, ekipman ve ariza turu bilgisi ekleyin — AI daha iyi analiz yapabilir.", "#ffd166"),
            ]
            for baslik, aciklama, renk in oneriler:
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;border-left:3px solid {renk};">
                    <strong style="color:{renk};">{baslik}</strong>
                    <p style="color:#aaa;font-size:0.85rem;margin:4px 0 0 0;">{aciklama}</p>
                </div>""", unsafe_allow_html=True)

    # ── Kalıcı Çözüm Takip ──
    with sub[4]:
        _styled_section("✅ Kalici Cozum Planlama & Takip", "#06d6a0")

        with st.form("cozum_form"):
            cc1, cc2 = st.columns(2)
            with cc1:
                c_problem = st.text_input("Problem / Ariza Kumesi", key="cozum_problem")
                c_kok_neden = st.text_input("Tespit Edilen Kok Neden", key="cozum_kok")
                c_cozum = st.text_area("Kalici Cozum Plani", height=68, key="cozum_plan")
            with cc2:
                c_sorumlu = st.text_input("Sorumlu", key="cozum_sorumlu")
                c_bitis = st.date_input("Hedef Tarih", value=datetime.now().date() + timedelta(days=30), key="cozum_bitis")
                c_oncelik = st.selectbox("Oncelik", ["Kritik", "Yuksek", "Normal", "Dusuk"], key="cozum_oncelik")

            if st.form_submit_button("✅ Cozum Plani Olustur", use_container_width=True):
                if c_problem and c_cozum:
                    cozumler.append({
                        "id": f"czm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "problem": c_problem,
                        "kok_neden": c_kok_neden,
                        "cozum": c_cozum,
                        "sorumlu": c_sorumlu,
                        "hedef_tarih": str(c_bitis),
                        "oncelik": c_oncelik,
                        "durum": "planli",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(cozum_path, cozumler)
                    st.success("Kalici cozum plani olusturuldu!")
                    st.rerun()

        if cozumler:
            for idx, c in enumerate(reversed(cozumler[-12:])):
                durum = c.get("durum", "planli")
                durum_ikon = {"planli": "📋", "devam": "🔄", "tamamlandi": "✅", "iptal": "❌"}.get(durum, "⚪")
                onc_renk = {"Kritik": "#e94560", "Yuksek": "#ff6b6b", "Normal": "#ffd166", "Dusuk": "#06d6a0"}.get(c.get("oncelik", ""), "#888")

                with st.expander(f"{durum_ikon} {c.get('problem','?')[:40]} — {c.get('oncelik','')}"):
                    st.write(f"**Kok Neden:** {c.get('kok_neden','')}")
                    st.write(f"**Cozum:** {c.get('cozum','')}")
                    st.write(f"**Sorumlu:** {c.get('sorumlu','')} | **Hedef:** {c.get('hedef_tarih','')}")
                    yeni_durum = st.selectbox("Durum", ["planli", "devam", "tamamlandi", "iptal"], index=["planli", "devam", "tamamlandi", "iptal"].index(durum), key=f"czm_durum_{idx}")
                    if st.button("Guncelle", key=f"czm_btn_{idx}"):
                        c["durum"] = yeni_durum
                        _save_json(cozum_path, cozumler)
                        st.rerun()

    # ── Tekrar Trendi ──
    with sub[5]:
        _styled_section("📈 Tekrar Eden Ariza Trend Analizi", "#8338ec")

        if tickets:
            aylik_tekrar = {}
            for anahtar, tlist in tekrar_eden.items():
                for t in tlist:
                    tarih = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""
                    ay = str(tarih)[:7]
                    if ay and len(ay) >= 7:
                        aylik_tekrar[ay] = aylik_tekrar.get(ay, 0) + 1

            if aylik_tekrar:
                max_val = max(aylik_tekrar.values())
                st.markdown("**Aylik Tekrar Eden Ariza Sayisi**")
                for ay in sorted(aylik_tekrar.keys()):
                    val = aylik_tekrar[ay]
                    bar_w = int(val / max_val * 100)
                    renk = "#e94560" if val > 10 else ("#ffd166" if val > 5 else "#06d6a0")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <span style="width:80px;color:#888;">{ay}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                        <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{val}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Aylik tekrar trendi icin yeterli veri yok.")

            # Genel tekrar skoru
            genel_tekrar_oran = int(toplam_tekrar / max(1, len(tickets)) * 100)
            renk = "#e94560" if genel_tekrar_oran >= 30 else ("#ffd166" if genel_tekrar_oran >= 15 else "#06d6a0")
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Genel Tekrar Orani</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">%{genel_tekrar_oran}</div>
                <div style="color:#aaa;font-size:0.85rem;">Dusuk oran = iyi performans</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Trend analizi icin talep verisi gerekiyor.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. MOBİL SAHA EKİBİ & GÖREV TAKİP MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_saha_ekibi(store):
    _styled_header("Mobil Saha Ekibi & Gorev Takip Merkezi", "📱")

    teknisyen_path = _get_data_path(store, "saha_teknisyenler.json")
    teknisyenler = _load_json(teknisyen_path)

    gorev_path = _get_data_path(store, "saha_gorevler.json")
    gorevler = _load_json(gorev_path)

    aktif_gorev = [g for g in gorevler if g.get("durum") in ("atandi", "yolda", "basladı")]
    tamamlanan = [g for g in gorevler if g.get("durum") == "tamamlandi"]

    _styled_stat_row([
        ("Teknisyen Sayisi", len(teknisyenler)),
        ("Toplam Gorev", len(gorevler)),
        ("Aktif Gorev", len(aktif_gorev)),
        ("Tamamlanan", len(tamamlanan)),
        ("Tamamlama Orani", f"%{int(len(tamamlanan) / max(1, len(gorevler)) * 100)}"),
    ])

    sub = st.tabs(["👷 Teknisyen Yonetimi", "📋 Gorev Atama", "📊 Performans Karnesi", "⚖️ Is Yuku Dengesi", "📅 Gorev Takvimi", "📸 Tamamlama Onay"])

    # ── Teknisyen Yönetimi ──
    with sub[0]:
        _styled_section("👷 Saha Teknisyen Kadrosu", "#0f3460")

        with st.form("teknisyen_form"):
            tc1, tc2 = st.columns(2)
            with tc1:
                t_ad = st.text_input("Ad Soyad", key="saha_tek_ad")
                t_uzmanlik = st.selectbox("Uzmanlik", ["Elektrik", "Tesisat", "Mekanik", "Bilisim", "Boyama", "Marangoz", "Genel"], key="saha_tek_uzm")
            with tc2:
                t_telefon = st.text_input("Telefon", key="saha_tek_tel")
                t_vardiya = st.selectbox("Vardiya", ["Sabah (08-16)", "Aksam (16-00)", "Gece (00-08)", "Tam Gun"], key="saha_tek_var")

            if st.form_submit_button("👷 Teknisyen Ekle", use_container_width=True):
                if t_ad:
                    teknisyenler.append({
                        "id": f"tek_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": t_ad,
                        "uzmanlik": t_uzmanlik,
                        "telefon": t_telefon,
                        "vardiya": t_vardiya,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(teknisyen_path, teknisyenler)
                    st.success(f"{t_ad} eklendi!")
                    st.rerun()

        if teknisyenler:
            for tk in teknisyenler:
                atanmis = len([g for g in gorevler if g.get("teknisyen") == tk.get("ad") and g.get("durum") in ("atandi", "yolda", "basladi")])
                durum_renk = "#06d6a0" if atanmis < 3 else ("#ffd166" if atanmis < 5 else "#e94560")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{tk.get('ad','?')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{tk.get('uzmanlik','')} | {tk.get('vardiya','')}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="background:{durum_renk}20;color:{durum_renk};padding:3px 10px;border-radius:8px;font-weight:700;">{atanmis} aktif is</span>
                        <span style="color:#888;font-size:0.78rem;">📞 {tk.get('telefon','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Görev Atama ──
    with sub[1]:
        _styled_section("📋 Yeni Gorev Olustur & Ata", "#e94560")

        teknisyen_isimleri = [t.get("ad", "?") for t in teknisyenler]

        with st.form("gorev_form"):
            gc1, gc2 = st.columns(2)
            with gc1:
                g_baslik = st.text_input("Gorev Basligi", key="saha_g_baslik")
                g_lokasyon = st.text_input("Lokasyon", key="saha_g_lok")
                g_oncelik = st.selectbox("Oncelik", ["Acil", "Yuksek", "Normal", "Dusuk"], key="saha_g_onc")
            with gc2:
                g_teknisyen = st.selectbox("Atanacak Teknisyen", ["Sec..."] + teknisyen_isimleri, key="saha_g_tek")
                g_tahmini = st.number_input("Tahmini Sure (dk)", min_value=5, value=60, step=15, key="saha_g_sure")
                g_tarih = st.date_input("Planlanan Tarih", value=datetime.now().date(), key="saha_g_tarih")
            g_aciklama = st.text_area("Aciklama", height=60, key="saha_g_acik")

            if st.form_submit_button("📋 Gorev Ata", use_container_width=True):
                if g_baslik and g_teknisyen != "Sec...":
                    gorevler.append({
                        "id": f"grv_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": g_baslik,
                        "lokasyon": g_lokasyon,
                        "oncelik": g_oncelik,
                        "teknisyen": g_teknisyen,
                        "tahmini_sure": g_tahmini,
                        "planlanan_tarih": str(g_tarih),
                        "aciklama": g_aciklama,
                        "durum": "atandi",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(gorev_path, gorevler)
                    st.success(f"Gorev {g_teknisyen} kisisine atandi!")
                    st.rerun()

        if gorevler:
            _styled_section("Aktif Gorevler", "#ffd166")
            for idx, g in enumerate(reversed([g for g in gorevler if g.get("durum") != "tamamlandi"][:15])):
                durum_ikon = {"atandi": "📌", "yolda": "🚗", "basladi": "🔧", "tamamlandi": "✅"}.get(g.get("durum", ""), "⚪")
                onc_renk = {"Acil": "#e94560", "Yuksek": "#ff6b6b", "Normal": "#ffd166", "Dusuk": "#06d6a0"}.get(g.get("oncelik", ""), "#888")

                with st.expander(f"{durum_ikon} {g.get('baslik','?')} — {g.get('teknisyen','')}"):
                    ec1, ec2, ec3 = st.columns(3)
                    ec1.write(f"**Lokasyon:** {g.get('lokasyon','')}")
                    ec2.write(f"**Tahmini:** {g.get('tahmini_sure','')} dk")
                    ec3.markdown(f"**Oncelik:** <span style='color:{onc_renk}'>{g.get('oncelik','')}</span>", unsafe_allow_html=True)

                    yeni_durum = st.selectbox("Durum", ["atandi", "yolda", "basladi", "tamamlandi"], index=["atandi", "yolda", "basladi", "tamamlandi"].index(g.get("durum", "atandi")), key=f"saha_durum_{idx}")
                    if st.button("Guncelle", key=f"saha_btn_{idx}"):
                        g["durum"] = yeni_durum
                        if yeni_durum == "tamamlandi":
                            g["tamamlanma"] = datetime.now().isoformat()
                        _save_json(gorev_path, gorevler)
                        st.rerun()

    # ── Performans Karnesi ──
    with sub[2]:
        _styled_section("📊 Teknisyen Performans Karnesi", "#06d6a0")

        if teknisyenler and gorevler:
            for tk in teknisyenler:
                ad = tk.get("ad", "?")
                kisi_gorevler = [g for g in gorevler if g.get("teknisyen") == ad]
                toplam = len(kisi_gorevler)
                biten = len([g for g in kisi_gorevler if g.get("durum") == "tamamlandi"])
                aktif = len([g for g in kisi_gorevler if g.get("durum") in ("atandi", "yolda", "basladi")])
                tamamlama_oran = int(biten / max(1, toplam) * 100)
                renk = "#06d6a0" if tamamlama_oran >= 80 else ("#ffd166" if tamamlama_oran >= 50 else "#e94560")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;font-size:1.05rem;">{ad}</strong>
                            <div style="color:#888;font-size:0.8rem;">{tk.get('uzmanlik','')} | Toplam: {toplam} | Aktif: {aktif} | Biten: {biten}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.5rem;font-weight:800;color:{renk};">%{tamamlama_oran}</div>
                        </div>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;margin-top:8px;">
                        <div style="width:{tamamlama_oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Performans karnesi icin teknisyen ve gorev verisi gerekiyor.")

    # ── İş Yükü Dengesi ──
    with sub[3]:
        _styled_section("⚖️ Is Yuku Dengesi & Optimizasyon", "#ffd166")

        if teknisyenler:
            yukler = []
            for tk in teknisyenler:
                ad = tk.get("ad", "?")
                aktif = len([g for g in gorevler if g.get("teknisyen") == ad and g.get("durum") in ("atandi", "yolda", "basladi")])
                toplam_dk = sum(g.get("tahmini_sure", 60) for g in gorevler if g.get("teknisyen") == ad and g.get("durum") in ("atandi", "yolda", "basladi"))
                yukler.append({"ad": ad, "aktif": aktif, "dakika": toplam_dk, "uzmanlik": tk.get("uzmanlik", "")})

            max_yuk = max(y["aktif"] for y in yukler) if yukler else 1
            ort_yuk = sum(y["aktif"] for y in yukler) / max(1, len(yukler))

            for y in sorted(yukler, key=lambda x: -x["aktif"]):
                bar_w = int(y["aktif"] / max(1, max_yuk) * 100)
                renk = "#e94560" if y["aktif"] > ort_yuk * 1.5 else ("#ffd166" if y["aktif"] > ort_yuk else "#06d6a0")
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="color:#e0e0e0;font-weight:600;">{y['ad']} <span style="color:#888;font-size:0.78rem;">({y['uzmanlik']})</span></span>
                        <span style="color:{renk};font-weight:700;">{y['aktif']} gorev ({y['dakika']} dk)</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Denge skoru
            if len(yukler) >= 2:
                degerler = [y["aktif"] for y in yukler]
                ortalama = sum(degerler) / len(degerler)
                sapma = (sum((d - ortalama) ** 2 for d in degerler) / len(degerler)) ** 0.5
                denge_skor = max(0, 100 - int(sapma * 20))
                renk = "#06d6a0" if denge_skor >= 70 else ("#ffd166" if denge_skor >= 40 else "#e94560")
                st.markdown(f"""
                <div style="background:#0f3460;border-radius:10px;padding:14px;text-align:center;margin-top:10px;">
                    <div style="color:#888;">Is Yuku Denge Skoru</div>
                    <div style="font-size:2rem;font-weight:800;color:{renk};">{denge_skor}/100</div>
                </div>""", unsafe_allow_html=True)

    # ── Görev Takvimi ──
    with sub[4]:
        _styled_section("📅 Gunluk / Haftalik Gorev Takvimi", "#00b4d8")

        if gorevler:
            bugun = datetime.now().date()
            gunluk = [g for g in gorevler if g.get("planlanan_tarih") == str(bugun)]
            haftalik = [g for g in gorevler if g.get("planlanan_tarih", "") >= str(bugun) and g.get("planlanan_tarih", "") <= str(bugun + timedelta(days=7))]

            st.markdown(f"**Bugun ({bugun}) — {len(gunluk)} gorev**")
            if gunluk:
                for g in gunluk:
                    durum_ikon = {"atandi": "📌", "yolda": "🚗", "basladi": "🔧", "tamamlandi": "✅"}.get(g.get("durum", ""), "⚪")
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:8px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;">
                        <span>{durum_ikon} <strong style="color:#e0e0e0;">{g.get('baslik','?')}</strong> — {g.get('teknisyen','')}</span>
                        <span style="color:#888;font-size:0.8rem;">{g.get('lokasyon','')} | {g.get('tahmini_sure','')} dk</span>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Bugun icin planlanmis gorev yok.")

            _styled_section(f"Bu Hafta ({len(haftalik)} gorev)", "#8338ec")
            tarih_grup = {}
            for g in haftalik:
                t = g.get("planlanan_tarih", "?")
                if t not in tarih_grup:
                    tarih_grup[t] = []
                tarih_grup[t].append(g)

            for tarih in sorted(tarih_grup.keys()):
                glist = tarih_grup[tarih]
                st.markdown(f"**📅 {tarih}** ({len(glist)} gorev)")
                for g in glist:
                    st.caption(f"  → {g.get('baslik','')} | {g.get('teknisyen','')} | {g.get('lokasyon','')}")
        else:
            _styled_info_banner("Takvim icin gorev olusturun.")

    # ── Tamamlama Onay ──
    with sub[5]:
        _styled_section("📸 Gorev Tamamlama & Onay", "#06d6a0")

        onay_path = _get_data_path(store, "gorev_onaylari.json")
        onaylar = _load_json(onay_path)

        tamamlananlar = [g for g in gorevler if g.get("durum") == "tamamlandi"]
        if tamamlananlar:
            for idx, g in enumerate(reversed(tamamlananlar[-10:])):
                onaylandi = any(o.get("gorev_id") == g.get("id") for o in onaylar)
                ikon = "✅" if onaylandi else "⏳"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{g.get('baslik','?')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{g.get('teknisyen','')}</span>
                    </div>
                    <span style="color:#888;font-size:0.78rem;">{g.get('tamamlanma','')[:10] if g.get('tamamlanma') else ''}</span>
                </div>""", unsafe_allow_html=True)

                if not onaylandi:
                    oc1, oc2 = st.columns(2)
                    with oc1:
                        o_not = st.text_input("Onay Notu", key=f"onay_not_{idx}")
                    with oc2:
                        o_puan = st.slider("Kalite Puani (1-5)", 1, 5, 4, key=f"onay_puan_{idx}")
                    if st.button("Onayla", key=f"onay_btn_{idx}"):
                        onaylar.append({
                            "gorev_id": g.get("id"),
                            "not": o_not,
                            "puan": o_puan,
                            "tarih": datetime.now().isoformat(),
                        })
                        _save_json(onay_path, onaylar)
                        st.success("Gorev onaylandi!")
                        st.rerun()
        else:
            _styled_info_banner("Tamamlanmis gorev bulunmuyor.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. OTOMATİK ESKALASYON & İŞ AKIŞI MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_eskalasyon_motoru(store):
    _styled_header("Otomatik Eskalasyon & Is Akisi Motoru", "🔄")

    kural_path = _get_data_path(store, "eskalasyon_kurallari.json")
    kurallar = _load_json(kural_path)

    log_path = _get_data_path(store, "eskalasyon_log.json")
    loglar = _load_json(log_path)

    akis_path = _get_data_path(store, "is_akislari.json")
    akislar = _load_json(akis_path)

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    _styled_stat_row([
        ("Eskalasyon Kurali", len(kurallar)),
        ("Eskalasyon Sayisi", len(loglar)),
        ("Is Akisi", len(akislar)),
        ("Aktif Talep", len(tickets)),
    ])

    sub = st.tabs(["📋 Eskalasyon Kurallari", "🔗 Eskalasyon Zinciri", "🔄 Is Akisi Tasarla", "📊 Eskalasyon Log", "🤖 Otomatik Atama", "📈 Analitik"])

    # ── Eskalasyon Kuralları ──
    with sub[0]:
        _styled_section("📋 Eskalasyon Kural Tanimlama", "#e94560")

        _styled_info_banner("Kurallar tetiklendiginde talep otomatik olarak bir ust kademeye eskalasyon edilir.")

        with st.form("eskalasyon_kural_form"):
            kc1, kc2 = st.columns(2)
            with kc1:
                k_ad = st.text_input("Kural Adi", key="esk_ad")
                k_tetikleyici = st.selectbox("Tetikleyici", [
                    "Sure Asimi (saat)",
                    "Tekrar Sayisi",
                    "Oncelik Degisimi",
                    "SLA Ihlali",
                    "Musteri Sikayeti",
                    "Teknisyen Mevcut Degil",
                ], key="esk_tetik")
                k_deger = st.number_input("Esik Deger", min_value=1, value=24, key="esk_deger")
            with kc2:
                k_hedef = st.text_input("Eskalasyon Hedefi (kisi/birim)", key="esk_hedef")
                k_aksiyon = st.selectbox("Aksiyon", ["Ust Kademeye Yonlendir", "Yonetici Bilgilendir", "Acil Ekip Cagir", "Oncelik Yukselt", "Dis Firma Cagir"], key="esk_aksiyon")
                k_kademe = st.selectbox("Kademe", ["Kademe 1", "Kademe 2", "Kademe 3", "Yonetici"], key="esk_kademe")

            if st.form_submit_button("📋 Kural Ekle", use_container_width=True):
                if k_ad:
                    kurallar.append({
                        "id": f"esk_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": k_ad,
                        "tetikleyici": k_tetikleyici,
                        "esik": k_deger,
                        "hedef": k_hedef,
                        "aksiyon": k_aksiyon,
                        "kademe": k_kademe,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(kural_path, kurallar)
                    st.success(f"Eskalasyon kurali '{k_ad}' eklendi!")
                    st.rerun()

        if kurallar:
            _styled_section("Tanimli Kurallar", "#0f3460")
            for idx, k in enumerate(kurallar):
                durum = "🟢" if k.get("aktif") else "🔴"
                kademe_renk = {"Kademe 1": "#06d6a0", "Kademe 2": "#ffd166", "Kademe 3": "#ff6b6b", "Yonetici": "#e94560"}.get(k.get("kademe", ""), "#888")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span>{durum}</span>
                            <strong style="color:#e0e0e0;margin-left:6px;">{k.get('ad','?')}</strong>
                        </div>
                        <span style="background:{kademe_renk}20;color:{kademe_renk};padding:3px 10px;border-radius:8px;font-size:0.8rem;">{k.get('kademe','')}</span>
                    </div>
                    <div style="color:#888;font-size:0.82rem;margin-top:4px;">
                        Tetik: {k.get('tetikleyici','')} >= {k.get('esik','')} | Aksiyon: {k.get('aksiyon','')} | Hedef: {k.get('hedef','')}
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Eskalasyon Zinciri ──
    with sub[1]:
        _styled_section("🔗 Eskalasyon Zinciri Gorsellestirme", "#8338ec")

        _styled_info_banner("Bir talebin eskalasyon surecinde hangi kademelerden gectigini gorsellestirir.")

        # Kademe yapısı
        kademeler = [
            {"ad": "Kademe 1 — Teknisyen", "sure": "0-4 saat", "ikon": "👷", "renk": "#06d6a0"},
            {"ad": "Kademe 2 — Takım Lideri", "sure": "4-24 saat", "ikon": "👨‍💼", "renk": "#ffd166"},
            {"ad": "Kademe 3 — Birim Muduru", "sure": "24-48 saat", "ikon": "🏢", "renk": "#ff6b6b"},
            {"ad": "Yonetici — Genel Mudur", "sure": "48+ saat", "ikon": "🎯", "renk": "#e94560"},
        ]

        for i, kad in enumerate(kademeler):
            st.markdown(f"""
            <div style="display:flex;gap:14px;margin-bottom:0;">
                <div style="display:flex;flex-direction:column;align-items:center;min-width:40px;">
                    <div style="font-size:1.5rem;">{kad['ikon']}</div>
                    {'<div style="width:3px;height:30px;background:' + kad['renk'] + '40;"></div>' if i < len(kademeler)-1 else ''}
                </div>
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;flex:1;margin-bottom:8px;border-left:4px solid {kad['renk']};">
                    <strong style="color:{kad['renk']};">{kad['ad']}</strong>
                    <div style="color:#888;font-size:0.82rem;">Mudahale suresi: {kad['sure']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Manuel eskalasyon
        _styled_section("Manuel Eskalasyon", "#ffd166")
        with st.form("manuel_esk_form"):
            me1, me2 = st.columns(2)
            with me1:
                m_talep = st.text_input("Talep No / Baslik", key="man_esk_talep")
                m_neden = st.selectbox("Eskalasyon Nedeni", ["Sure Asimi", "Musteri Sikayeti", "Teknik Yetersizlik", "Kaynak Eksikligi", "Diger"], key="man_esk_neden")
            with me2:
                m_kademe = st.selectbox("Hedef Kademe", ["Kademe 2", "Kademe 3", "Yonetici"], key="man_esk_kademe")
                m_not = st.text_input("Not", key="man_esk_not")

            if st.form_submit_button("🔗 Eskale Et", use_container_width=True):
                if m_talep:
                    loglar.append({
                        "id": f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "talep": m_talep,
                        "neden": m_neden,
                        "kademe": m_kademe,
                        "not": m_not,
                        "tip": "manuel",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(log_path, loglar)
                    st.success(f"Talep {m_kademe} kademesine eskale edildi!")
                    st.rerun()

    # ── İş Akışı Tasarla ──
    with sub[2]:
        _styled_section("🔄 Is Akisi Sablonu Tasarla", "#06d6a0")

        with st.form("akis_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                a_ad = st.text_input("Akis Adi", key="akis_ad")
                a_tetik = st.selectbox("Tetikleyici Olay", ["Yeni Talep Acildi", "Oncelik Degisti", "SLA Yaklasti", "Talep Kapandi", "Atama Degisti"], key="akis_tetik")
            with ac2:
                a_adim1 = st.text_input("Adim 1", key="akis_adim1")
                a_adim2 = st.text_input("Adim 2", key="akis_adim2")
                a_adim3 = st.text_input("Adim 3 (opsiyonel)", key="akis_adim3")

            if st.form_submit_button("🔄 Akis Olustur", use_container_width=True):
                if a_ad:
                    adimlar = [a for a in [a_adim1, a_adim2, a_adim3] if a]
                    akislar.append({
                        "id": f"ais_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": a_ad,
                        "tetik": a_tetik,
                        "adimlar": adimlar,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(akis_path, akislar)
                    st.success(f"Is akisi '{a_ad}' olusturuldu!")
                    st.rerun()

        if akislar:
            for a in akislar:
                durum = "🟢" if a.get("aktif") else "🔴"
                with st.expander(f"{durum} {a.get('ad','?')} — Tetik: {a.get('tetik','')}"):
                    for i, adim in enumerate(a.get("adimlar", [])):
                        st.markdown(f"""
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                            <span style="background:#0f3460;color:#00b4d8;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;">{i+1}</span>
                            <span style="color:#e0e0e0;">{adim}</span>
                        </div>""", unsafe_allow_html=True)

    # ── Eskalasyon Log ──
    with sub[3]:
        _styled_section("📊 Eskalasyon Gecmisi & Log", "#ffd166")

        if loglar:
            for log in reversed(loglar[-15:]):
                tip_ikon = "🤖" if log.get("tip") == "otomatik" else "👤"
                kademe_renk = {"Kademe 2": "#ffd166", "Kademe 3": "#ff6b6b", "Yonetici": "#e94560"}.get(log.get("kademe", ""), "#888")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span>{tip_ikon}</span>
                            <strong style="color:#e0e0e0;margin-left:6px;">{log.get('talep','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">Neden: {log.get('neden','')}</span>
                        </div>
                        <div>
                            <span style="background:{kademe_renk}20;color:{kademe_renk};padding:2px 8px;border-radius:6px;font-size:0.78rem;">{log.get('kademe','')}</span>
                            <span style="color:#888;font-size:0.75rem;margin-left:6px;">{log.get('tarih','')[:16]}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henuz eskalasyon kaydi bulunmuyor.")

    # ── Otomatik Atama ──
    with sub[4]:
        _styled_section("🤖 Otomatik Atama Kurallari", "#00b4d8")

        atama_path = _get_data_path(store, "otomatik_atama.json")
        atamalar = _load_json(atama_path)

        with st.form("atama_kural_form"):
            ata1, ata2 = st.columns(2)
            with ata1:
                at_kosul = st.selectbox("Kosul", ["Hizmet Alani", "Oncelik", "Lokasyon", "Ariza Turu"], key="atama_kosul")
                at_deger = st.text_input("Kosul Degeri (ornek: Elektrik)", key="atama_deger")
            with ata2:
                at_hedef = st.text_input("Otomatik Atanacak Kisi/Ekip", key="atama_hedef")
                at_kademe = st.selectbox("Kademe", ["Kademe 1", "Kademe 2", "Kademe 3"], key="atama_kademe")

            if st.form_submit_button("🤖 Atama Kurali Ekle", use_container_width=True):
                if at_deger and at_hedef:
                    atamalar.append({
                        "id": f"ata_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "kosul": at_kosul,
                        "deger": at_deger,
                        "hedef": at_hedef,
                        "kademe": at_kademe,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(atama_path, atamalar)
                    st.success("Otomatik atama kurali eklendi!")
                    st.rerun()

        if atamalar:
            for a in atamalar:
                durum = "🟢" if a.get("aktif") else "🔴"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                    <span>{durum} <strong style="color:#e0e0e0;">{a.get('kosul','')}: {a.get('deger','')}</strong> → {a.get('hedef','')}</span>
                    <span style="color:#888;font-size:0.8rem;">{a.get('kademe','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Analitik ──
    with sub[5]:
        _styled_section("📈 Eskalasyon Analitikleri", "#8338ec")

        if loglar:
            # Neden dağılımı
            neden_sayim = Counter(l.get("neden", "Diger") for l in loglar)
            st.markdown("**Eskalasyon Neden Dagilimi**")
            max_val = max(neden_sayim.values()) if neden_sayim.values() else 1
            for neden, sayi in sorted(neden_sayim.items(), key=lambda x: -x[1]):
                bar_w = int(sayi / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:160px;color:#e0e0e0;font-size:0.88rem;">{neden}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#8338ec;border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:#8338ec;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            # Kademe dağılımı
            kademe_sayim = Counter(l.get("kademe", "?") for l in loglar)
            _styled_section("Kademe Dagilimi", "#e94560")
            for kademe, sayi in sorted(kademe_sayim.items()):
                renk = {"Kademe 2": "#ffd166", "Kademe 3": "#ff6b6b", "Yonetici": "#e94560"}.get(kademe, "#888")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                    <span style="color:{renk};font-weight:600;">{kademe}</span>
                    <span style="color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            # Eskalasyon oranı
            esk_oran = int(len(loglar) / max(1, len(tickets)) * 100)
            renk = "#e94560" if esk_oran > 30 else ("#ffd166" if esk_oran > 15 else "#06d6a0")
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Eskalasyon Orani</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">%{esk_oran}</div>
                <div style="color:#aaa;font-size:0.85rem;">Dusuk oran = iyi ilk cozum performansi</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Analitik icin eskalasyon verisi gerekiyor.")
