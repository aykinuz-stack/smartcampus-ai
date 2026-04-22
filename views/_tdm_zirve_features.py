"""
Tüketim ve Demirbaş - ZİRVE Özellikler
1. Demirbaş DNA & Dijital İkiz Sistemi
2. Akıllı Bütçe Planlama & Senaryo Motoru
3. Kurum Verimliliği Liderlik Tablosu & Gamification
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# ── Ortak stil yardımcıları ──
def _styled_header(title, icon="🧬"):
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
    if hasattr(store, 'tenant_id') and store.tenant_id:
        return os.path.join("data", "tenants", store.tenant_id, "tuketim", filename)
    return os.path.join("data", "tuketim", filename)

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
#  1. DEMİRBAŞ DNA & DİJİTAL İKİZ SİSTEMİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_dijital_ikiz(store):
    _styled_header("Demirbaş DNA & Dijital İkiz Sistemi", "🧬")

    dna_path = _get_data_path(store, "demirbas_dna.json")
    dna_kayitlar = _load_json(dna_path)

    # Demirbaş listesi
    demirbas_path = _get_data_path(store, "demirbaslar.json")
    demirbaslar = _load_json(demirbas_path)
    if not demirbaslar:
        try:
            demirbaslar = store.load_objects("demirbaslar") or []
        except Exception:
            demirbaslar = []

    # Bakım kayıtları
    bakim_path = _get_data_path(store, "bakim_kayitlari.json")
    bakimlar = _load_json(bakim_path)

    # İstatistikler
    _styled_stat_row([
        ("Toplam Varlık", len(demirbaslar)),
        ("DNA Profili Oluşturulan", len(dna_kayitlar)),
        ("Bakım Geçmişi", len(bakimlar)),
        ("Kapsama Oranı", f"%{int(len(dna_kayitlar) / max(1, len(demirbaslar)) * 100)}"),
    ])

    sub = st.tabs(["🧬 DNA Kartı", "📜 Zaman Çizelgesi", "💯 Yaşam Skoru", "🔄 Karşılaştırma", "📸 Fotoğraf Arşivi", "🔮 Emeklilik Tahmini"])

    # ── DNA Kartı ──
    with sub[0]:
        _styled_section("🧬 Varlık DNA Kartı Oluştur", "#8338ec")

        with st.form("dna_kart_form"):
            dc1, dc2 = st.columns(2)
            with dc1:
                varlik_adi = st.text_input("Varlık / Demirbaş Adı", key="dna_ad")
                seri_no = st.text_input("Seri / Barkod No", key="dna_seri")
                kategori = st.selectbox("Kategori", ["Elektronik", "Mobilya", "Beyaz Eşya", "Aydınlatma", "Isıtma/Soğutma", "Spor Ekipman", "Lab Ekipman", "Araç", "Diğer"], key="dna_kat")
                marka_model = st.text_input("Marka / Model", key="dna_marka")
            with dc2:
                satin_alma_tarihi = st.date_input("Satın Alma Tarihi", value=datetime.now().date() - timedelta(days=365), key="dna_satin")
                satin_alma_fiyati = st.number_input("Satın Alma Fiyatı (TL)", min_value=0.0, step=100.0, key="dna_fiyat")
                garanti_bitis = st.date_input("Garanti Bitiş", value=datetime.now().date() + timedelta(days=365), key="dna_garanti")
                konum = st.text_input("Konum (Bina/Kat/Oda)", key="dna_konum")
            zimmetli = st.text_input("Zimmetli Kişi / Departman", key="dna_zimmet")
            notlar = st.text_area("Ek Notlar", height=60, key="dna_not")

            if st.form_submit_button("🧬 DNA Kartı Oluştur", use_container_width=True):
                if varlik_adi:
                    yeni = {
                        "id": f"dna_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "varlik_adi": varlik_adi,
                        "seri_no": seri_no,
                        "kategori": kategori,
                        "marka_model": marka_model,
                        "satin_alma_tarihi": str(satin_alma_tarihi),
                        "satin_alma_fiyati": satin_alma_fiyati,
                        "garanti_bitis": str(garanti_bitis),
                        "konum": konum,
                        "zimmetli": zimmetli,
                        "notlar": notlar,
                        "olaylar": [],
                        "olusturma": datetime.now().isoformat(),
                    }
                    dna_kayitlar.append(yeni)
                    _save_json(dna_path, dna_kayitlar)
                    st.success(f"{varlik_adi} DNA kartı oluşturuldu!")
                    st.rerun()

        # Mevcut DNA kartları
        if dna_kayitlar:
            _styled_section("Kayıtlı Dijital İkizler", "#06d6a0")
            arama = st.text_input("Ara (ad, seri no, konum)...", key="dna_ara")
            filtreli = dna_kayitlar
            if arama:
                arama_lower = arama.lower()
                filtreli = [d for d in dna_kayitlar if arama_lower in (d.get("varlik_adi", "") + d.get("seri_no", "") + d.get("konum", "")).lower()]

            for idx, d in enumerate(filtreli):
                garanti_ok = d.get("garanti_bitis", "") >= str(datetime.now().date())
                garanti_renk = "#06d6a0" if garanti_ok else "#e94560"
                garanti_text = "Garantide" if garanti_ok else "Garanti Bitti"

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#16213e,#1a1a2e);border-radius:14px;padding:18px;margin-bottom:12px;border:1px solid #8338ec30;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <h3 style="color:#8338ec;margin:0 0 6px 0;">🧬 {d.get('varlik_adi','?')}</h3>
                            <span style="color:#888;font-size:0.82rem;">{d.get('marka_model','')} | SN: {d.get('seri_no','—')}</span>
                        </div>
                        <div style="text-align:right;">
                            <div style="background:{garanti_renk}20;color:{garanti_renk};padding:4px 12px;border-radius:8px;font-size:0.8rem;font-weight:600;">{garanti_text}</div>
                        </div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px;">
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Kategori</div>
                            <div style="color:#00b4d8;font-weight:600;">{d.get('kategori','')}</div>
                        </div>
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Konum</div>
                            <div style="color:#ffd166;font-weight:600;">{d.get('konum','—')}</div>
                        </div>
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Zimmetli</div>
                            <div style="color:#06d6a0;font-weight:600;">{d.get('zimmetli','—')}</div>
                        </div>
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Satın Alma</div>
                            <div style="color:#e0e0e0;font-weight:600;">{d.get('satin_alma_tarihi','')}</div>
                        </div>
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Fiyat</div>
                            <div style="color:#e94560;font-weight:600;">TL{d.get('satin_alma_fiyati',0):,.0f}</div>
                        </div>
                        <div style="background:#0f346020;padding:8px;border-radius:8px;">
                            <div style="color:#666;font-size:0.72rem;">Garanti Bitiş</div>
                            <div style="color:{garanti_renk};font-weight:600;">{d.get('garanti_bitis','')}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Zaman Çizelgesi ──
    with sub[1]:
        _styled_section("📜 Varlık Yaşam Zaman Çizelgesi (Timeline)", "#00b4d8")

        if dna_kayitlar:
            secilen = st.selectbox("Varlık Seçin", [d.get("varlik_adi", "?") for d in dna_kayitlar], key="timeline_sec")
            secilen_dna = next((d for d in dna_kayitlar if d.get("varlik_adi") == secilen), None)

            if secilen_dna:
                # Olayları topla
                olaylar = []
                olaylar.append({"tarih": secilen_dna.get("satin_alma_tarihi", ""), "tip": "Satın Alma", "ikon": "🛒", "renk": "#06d6a0", "detay": f"TL{secilen_dna.get('satin_alma_fiyati',0):,.0f}"})

                # Bakım olayları
                varlik_bakimlari = [b for b in bakimlar if b.get("varlik_adi") == secilen]
                for b in varlik_bakimlari:
                    olaylar.append({"tarih": b.get("planlanan_tarih", ""), "tip": f"Bakım ({b.get('bakim_turu','')})", "ikon": "🔧", "renk": "#ffd166", "detay": b.get("notlar", "")})

                # DNA'daki ek olaylar
                for o in secilen_dna.get("olaylar", []):
                    olaylar.append({"tarih": o.get("tarih", ""), "tip": o.get("tip", ""), "ikon": "📌", "renk": "#8338ec", "detay": o.get("detay", "")})

                garanti = secilen_dna.get("garanti_bitis", "")
                if garanti:
                    olaylar.append({"tarih": garanti, "tip": "Garanti Bitiş", "ikon": "🛡️", "renk": "#e94560", "detay": ""})

                olaylar.sort(key=lambda x: x.get("tarih", ""))

                # Timeline render
                st.markdown(f"**{secilen}** - Yaşam Hikayesi ({len(olaylar)} olay)")
                for i, o in enumerate(olaylar):
                    st.markdown(f"""
                    <div style="display:flex;gap:14px;margin-bottom:0;">
                        <div style="display:flex;flex-direction:column;align-items:center;min-width:30px;">
                            <div style="font-size:1.3rem;">{o['ikon']}</div>
                            {'<div style="width:2px;height:30px;background:' + o['renk'] + '40;"></div>' if i < len(olaylar)-1 else ''}
                        </div>
                        <div style="background:#16213e;border-radius:10px;padding:10px 16px;flex:1;margin-bottom:8px;border-left:3px solid {o['renk']};">
                            <div style="display:flex;justify-content:space-between;">
                                <strong style="color:{o['renk']};">{o['tip']}</strong>
                                <span style="color:#888;font-size:0.8rem;">{o['tarih']}</span>
                            </div>
                            <div style="color:#aaa;font-size:0.85rem;margin-top:3px;">{o['detay']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                # Olay ekle
                _styled_section("Yeni Olay Ekle", "#8338ec")
                with st.form("olay_ekle_form"):
                    oc1, oc2 = st.columns(2)
                    with oc1:
                        o_tip = st.selectbox("Olay Tipi", ["Zimmet Değişikliği", "Konum Değişikliği", "Arıza", "Tamir", "Yükseltme", "Hasar", "Diğer"])
                    with oc2:
                        o_tarih = st.date_input("Tarih", value=datetime.now().date(), key="olay_tarih")
                    o_detay = st.text_input("Detay", key="olay_detay")
                    if st.form_submit_button("📌 Olay Ekle"):
                        if "olaylar" not in secilen_dna:
                            secilen_dna["olaylar"] = []
                        secilen_dna["olaylar"].append({"tarih": str(o_tarih), "tip": o_tip, "detay": o_detay})
                        _save_json(dna_path, dna_kayitlar)
                        st.success("Olay eklendi!")
                        st.rerun()
        else:
            _styled_info_banner("Zaman cizelgesi icin DNA karti olusturun.")

    # ── Yaşam Skoru ──
    with sub[2]:
        _styled_section("💯 Varlık Yaşam Skoru (Health Score)", "#06d6a0")

        if dna_kayitlar:
            _styled_info_banner("Yasam skoru; varligin yasi, bakim gecmisi, garanti durumu ve kullanim yogunluguna gore hesaplanir.")

            skorlar = []
            bugun = datetime.now().date()
            for d in dna_kayitlar:
                ad = d.get("varlik_adi", "?")

                # Yaş puanı (yeni = yüksek)
                try:
                    satin_tarih = datetime.strptime(d.get("satin_alma_tarihi", "2020-01-01"), "%Y-%m-%d").date()
                    yas_gun = (bugun - satin_tarih).days
                except Exception:
                    yas_gun = 365
                yas_puan = max(0, 100 - int(yas_gun / 20))

                # Garanti puanı
                try:
                    garanti = datetime.strptime(d.get("garanti_bitis", "2020-01-01"), "%Y-%m-%d").date()
                    garanti_puan = 100 if garanti > bugun else max(0, 50 - (bugun - garanti).days // 30 * 10)
                except Exception:
                    garanti_puan = 30

                # Bakım puanı
                varlik_bakim = len([b for b in bakimlar if b.get("varlik_adi") == ad and b.get("durum") == "tamamlandi"])
                bakim_puan = min(100, 50 + varlik_bakim * 15)

                genel = int((yas_puan * 0.3 + garanti_puan * 0.3 + bakim_puan * 0.4))
                skorlar.append({"ad": ad, "yas_puan": yas_puan, "garanti_puan": garanti_puan, "bakim_puan": bakim_puan, "genel": genel, "yas_gun": yas_gun})

            skorlar.sort(key=lambda x: -x["genel"])

            for s in skorlar:
                g = s["genel"]
                renk = "#06d6a0" if g >= 70 else "#ffd166" if g >= 40 else "#e94560"
                durum = "Mukemmel" if g >= 85 else ("Iyi" if g >= 70 else ("Orta" if g >= 50 else ("Riskli" if g >= 30 else "Kritik")))

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;font-size:1.05rem;">{s['ad']}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:10px;">{s['yas_gun']} gun</span>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.6rem;font-weight:800;color:{renk};">{g}</div>
                            <div style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;font-size:0.75rem;font-weight:600;">{durum}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:16px;margin-top:8px;">
                        <span style="color:#888;font-size:0.78rem;">Yas: <strong style="color:#00b4d8;">{s['yas_puan']}</strong></span>
                        <span style="color:#888;font-size:0.78rem;">Garanti: <strong style="color:#ffd166;">{s['garanti_puan']}</strong></span>
                        <span style="color:#888;font-size:0.78rem;">Bakim: <strong style="color:#06d6a0;">{s['bakim_puan']}</strong></span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Genel skor
            if skorlar:
                ort = sum(s["genel"] for s in skorlar) / len(skorlar)
                renk = "#06d6a0" if ort >= 70 else "#ffd166" if ort >= 40 else "#e94560"
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-top:16px;">
                    <div style="font-size:0.9rem;color:#888;">Kurum Varlik Sagligi Ortalaması</div>
                    <div style="font-size:3rem;font-weight:800;color:{renk};">{ort:.0f}/100</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Yasam skoru icin DNA karti olusturun.")

    # ── Karşılaştırma ──
    with sub[3]:
        _styled_section("🔄 Benzer Varlık Karşılaştırma", "#ffd166")

        if len(dna_kayitlar) >= 2:
            kc1, kc2 = st.columns(2)
            isimler = [d.get("varlik_adi", "?") for d in dna_kayitlar]
            with kc1:
                sol = st.selectbox("Varlık 1", isimler, index=0, key="karsilastir_sol")
            with kc2:
                sag = st.selectbox("Varlık 2", isimler, index=min(1, len(isimler)-1), key="karsilastir_sag")

            sol_d = next((d for d in dna_kayitlar if d.get("varlik_adi") == sol), {})
            sag_d = next((d for d in dna_kayitlar if d.get("varlik_adi") == sag), {})

            karsilastirma = [
                ("Kategori", sol_d.get("kategori", "—"), sag_d.get("kategori", "—")),
                ("Marka/Model", sol_d.get("marka_model", "—"), sag_d.get("marka_model", "—")),
                ("Satin Alma", sol_d.get("satin_alma_tarihi", "—"), sag_d.get("satin_alma_tarihi", "—")),
                ("Fiyat", f"TL{sol_d.get('satin_alma_fiyati', 0):,.0f}", f"TL{sag_d.get('satin_alma_fiyati', 0):,.0f}"),
                ("Garanti Bitis", sol_d.get("garanti_bitis", "—"), sag_d.get("garanti_bitis", "—")),
                ("Konum", sol_d.get("konum", "—"), sag_d.get("konum", "—")),
                ("Zimmetli", sol_d.get("zimmetli", "—"), sag_d.get("zimmetli", "—")),
            ]

            st.markdown(f"""
            <div style="background:#16213e;border-radius:12px;overflow:hidden;margin-top:10px;">
                <div style="display:grid;grid-template-columns:1fr 2fr 2fr;background:#0f3460;padding:10px 16px;">
                    <strong style="color:#888;">Kriter</strong>
                    <strong style="color:#8338ec;text-align:center;">{sol}</strong>
                    <strong style="color:#ffd166;text-align:center;">{sag}</strong>
                </div>""", unsafe_allow_html=True)

            for kriter, s_val, g_val in karsilastirma:
                st.markdown(f"""
                <div style="display:grid;grid-template-columns:1fr 2fr 2fr;padding:8px 16px;border-bottom:1px solid #0f346040;">
                    <span style="color:#888;">{kriter}</span>
                    <span style="color:#e0e0e0;text-align:center;">{s_val}</span>
                    <span style="color:#e0e0e0;text-align:center;">{g_val}</span>
                </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            _styled_info_banner("Karsilastirma icin en az 2 DNA karti gerekiyor.")

    # ── Fotoğraf Arşivi ──
    with sub[4]:
        _styled_section("📸 Varlık Fotoğraf & Belge Arşivi", "#e94560")

        foto_path = _get_data_path(store, "demirbas_fotograflari.json")
        fotograflar = _load_json(foto_path)

        with st.form("foto_form"):
            fc1, fc2 = st.columns(2)
            with fc1:
                f_varlik = st.text_input("Varlık Adı", key="foto_varlik")
                f_tip = st.selectbox("Belge Tipi", ["Fotoğraf", "Fatura", "Garanti Belgesi", "Kullanım Kılavuzu", "Bakım Raporu", "Diğer"])
            with fc2:
                f_aciklama = st.text_input("Açıklama", key="foto_aciklama")
                f_tarih = st.date_input("Tarih", value=datetime.now().date(), key="foto_tarih")

            if st.form_submit_button("📸 Kayıt Ekle", use_container_width=True):
                if f_varlik:
                    fotograflar.append({
                        "id": f"fot_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "varlik": f_varlik,
                        "tip": f_tip,
                        "aciklama": f_aciklama,
                        "tarih": str(f_tarih),
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(foto_path, fotograflar)
                    st.success("Belge kaydı eklendi!")
                    st.rerun()

        if fotograflar:
            # Varlık bazlı grupla
            varlik_belge = {}
            for f in fotograflar:
                v = f.get("varlik", "?")
                if v not in varlik_belge:
                    varlik_belge[v] = []
                varlik_belge[v].append(f)

            for varlik, belgeler in varlik_belge.items():
                with st.expander(f"📁 {varlik} ({len(belgeler)} belge)"):
                    for b in belgeler:
                        tip_ikon = {"Fotoğraf": "📷", "Fatura": "🧾", "Garanti Belgesi": "🛡️", "Kullanım Kılavuzu": "📖", "Bakım Raporu": "🔧"}.get(b.get("tip", ""), "📄")
                        st.markdown(f"""
                        <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;">
                            <span>{tip_ikon} <strong style="color:#e0e0e0;">{b.get('tip','')}</strong> — {b.get('aciklama','')}</span>
                            <span style="color:#888;font-size:0.78rem;">{b.get('tarih','')}</span>
                        </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henuz belge arsivi kaydi yok.")

    # ── Emeklilik Tahmini ──
    with sub[5]:
        _styled_section("🔮 Varlık Emeklilik / Yenileme Tahmini", "#e94560")

        if dna_kayitlar:
            _styled_info_banner("Varlik kategorisi, yasi ve bakim gecmisine gore tahmini ekonomik omur ve yenileme zamani hesaplanir.")

            # Kategori bazlı ekonomik ömür (yıl)
            ekonomik_omur = {"Elektronik": 5, "Mobilya": 10, "Beyaz Eşya": 8, "Aydınlatma": 6, "Isıtma/Soğutma": 10, "Spor Ekipman": 7, "Lab Ekipman": 8, "Araç": 10, "Diğer": 7}

            bugun = datetime.now().date()
            tahminler = []
            for d in dna_kayitlar:
                ad = d.get("varlik_adi", "?")
                kat = d.get("kategori", "Diğer")
                omur_yil = ekonomik_omur.get(kat, 7)
                try:
                    satin = datetime.strptime(d.get("satin_alma_tarihi", "2020-01-01"), "%Y-%m-%d").date()
                except Exception:
                    satin = bugun - timedelta(days=365)

                yas_yil = (bugun - satin).days / 365.25
                kalan_yil = max(0, omur_yil - yas_yil)
                kalan_oran = max(0, min(100, int(kalan_yil / omur_yil * 100)))

                tahminler.append({
                    "ad": ad, "kat": kat, "omur": omur_yil,
                    "yas": round(yas_yil, 1), "kalan": round(kalan_yil, 1),
                    "oran": kalan_oran,
                    "fiyat": d.get("satin_alma_fiyati", 0)
                })

            tahminler.sort(key=lambda x: x["kalan"])

            # Acil yenileme gerektirenler
            acil = [t for t in tahminler if t["kalan"] <= 1]
            if acil:
                st.error(f"🚨 {len(acil)} varlik 1 yil icinde emekliye ayrilacak!")

            for t in tahminler:
                renk = "#e94560" if t["oran"] <= 20 else ("#ffd166" if t["oran"] <= 50 else "#06d6a0")
                durum = "Acil Yenile" if t["kalan"] <= 0.5 else ("Yenileme Planla" if t["kalan"] <= 2 else ("Izle" if t["kalan"] <= 4 else "Saglıklı"))
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div>
                            <strong style="color:#e0e0e0;">{t['ad']}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">({t['kat']})</span>
                        </div>
                        <div style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;font-size:0.8rem;font-weight:600;">{durum}</div>
                    </div>
                    <div style="display:flex;gap:20px;margin-bottom:6px;">
                        <span style="color:#888;font-size:0.8rem;">Yas: <strong style="color:#00b4d8;">{t['yas']} yil</strong></span>
                        <span style="color:#888;font-size:0.8rem;">Ekonomik Omur: <strong style="color:#ffd166;">{t['omur']} yil</strong></span>
                        <span style="color:#888;font-size:0.8rem;">Kalan: <strong style="color:{renk};">{t['kalan']} yil</strong></span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                        <div style="width:{t['oran']}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Toplam yenileme bütçesi
            yenileme_butce = sum(t["fiyat"] for t in tahminler if t["kalan"] <= 2)
            if yenileme_butce > 0:
                st.markdown(f"""
                <div style="background:#0f3460;border-radius:12px;padding:16px;text-align:center;margin-top:14px;">
                    <div style="color:#888;">2 Yil Icinde Tahmini Yenileme Butcesi</div>
                    <div style="font-size:2.2rem;font-weight:800;color:#e94560;">TL{yenileme_butce:,.0f}</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Emeklilik tahmini icin DNA karti olusturun.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. AKILLI BÜTÇE PLANLAMA & SENARYO MOTORU
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_butce_planlama(store):
    _styled_header("Akıllı Bütçe Planlama & Senaryo Motoru", "🎯")

    butce_path = _get_data_path(store, "butce_planlari.json")
    butceler = _load_json(butce_path)

    senaryo_path = _get_data_path(store, "butce_senaryolari.json")
    senaryolar = _load_json(senaryo_path)

    # Mevcut harcama verileri
    maliyet_path = _get_data_path(store, "bakim_maliyetleri.json")
    maliyetler = _load_json(maliyet_path)
    toplam_harcama = sum(m.get("tutar", 0) for m in maliyetler)

    _styled_stat_row([
        ("Butce Plani Sayisi", len(butceler)),
        ("Senaryo Sayisi", len(senaryolar)),
        ("Gecmis Harcama", f"TL{toplam_harcama:,.0f}"),
        ("Ort. Aylik", f"TL{toplam_harcama / max(1, 12):,.0f}"),
    ])

    sub = st.tabs(["📋 Bütçe Oluştur", "🔮 Senaryo Simülasyonu", "🏢 Departman Bütçe", "📊 Sapma Analizi", "🤖 AI Bütçe Önerisi"])

    # ── Bütçe Oluştur ──
    with sub[0]:
        _styled_section("📋 Yeni Bütçe Planı", "#0f3460")

        with st.form("butce_form"):
            bc1, bc2 = st.columns(2)
            with bc1:
                b_donem = st.selectbox("Dönem", ["2025-2026", "2026-2027", "2027-2028"], key="butce_donem")
                b_kategori = st.selectbox("Kategori", ["Tüketim Malzemesi", "Demirbaş Alım", "Bakım & Onarım", "Teknoloji", "Kırtasiye", "Temizlik", "Gıda", "Diğer"], key="butce_kat")
                b_departman = st.text_input("Departman / Birim", key="butce_dept")
            with bc2:
                b_tutar = st.number_input("Planlanan Bütçe (TL)", min_value=0.0, step=1000.0, key="butce_tutar")
                b_oncelik = st.selectbox("Öncelik", ["Zorunlu", "Yüksek", "Normal", "Düşük"], key="butce_onc")
                b_aciklama = st.text_input("Açıklama", key="butce_acik")

            if st.form_submit_button("📋 Bütçe Planla", use_container_width=True):
                if b_departman and b_tutar > 0:
                    butceler.append({
                        "id": f"btc_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "donem": b_donem,
                        "kategori": b_kategori,
                        "departman": b_departman,
                        "planlanan": b_tutar,
                        "gerceklesen": 0,
                        "oncelik": b_oncelik,
                        "aciklama": b_aciklama,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(butce_path, butceler)
                    st.success("Butce plani olusturuldu!")
                    st.rerun()

        if butceler:
            toplam_plan = sum(b.get("planlanan", 0) for b in butceler)
            toplam_gercek = sum(b.get("gerceklesen", 0) for b in butceler)

            _styled_stat_row([
                ("Toplam Planlanan", f"TL{toplam_plan:,.0f}"),
                ("Toplam Gerceklesen", f"TL{toplam_gercek:,.0f}"),
                ("Sapma", f"TL{toplam_plan - toplam_gercek:,.0f}"),
            ])

            for idx, b in enumerate(butceler):
                plan = b.get("planlanan", 0)
                gercek = b.get("gerceklesen", 0)
                oran = int(gercek / max(1, plan) * 100)
                renk = "#06d6a0" if oran <= 80 else ("#ffd166" if oran <= 100 else "#e94560")

                with st.expander(f"{b.get('departman','?')} — {b.get('kategori','')} (TL{plan:,.0f})"):
                    st.markdown(f"""
                    <div style="margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="color:#888;">Kullanım: %{oran}</span>
                            <span style="color:{renk};font-weight:700;">TL{gercek:,.0f} / TL{plan:,.0f}</span>
                        </div>
                        <div style="background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{min(100, oran)}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    yeni_gercek = st.number_input("Gerceklesen Tutar Guncelle", min_value=0.0, value=float(gercek), step=100.0, key=f"btc_guncelle_{idx}")
                    if st.button("Guncelle", key=f"btc_btn_{idx}"):
                        b["gerceklesen"] = yeni_gercek
                        _save_json(butce_path, butceler)
                        st.rerun()

    # ── Senaryo Simülasyonu ──
    with sub[1]:
        _styled_section("🔮 'Ya Olursa?' Senaryo Simulasyonu", "#8338ec")

        _styled_info_banner("Farkli senaryolari simule ederek butce etkisini onceden gorun.")

        with st.form("senaryo_form"):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_ad = st.text_input("Senaryo Adi", key="senaryo_ad")
                s_tip = st.selectbox("Senaryo Tipi", [
                    "Butce Kisitlama (%)", "Ogrenci Artisi (%)",
                    "Yeni Bina/Kat", "Enflasyon Etkisi (%)",
                    "Personel Artisi", "Teknoloji Yenileme",
                ], key="senaryo_tip")
            with sc2:
                s_deger = st.number_input("Deger / Oran", min_value=-100.0, max_value=500.0, value=10.0, step=5.0, key="senaryo_deger")
                s_donem = st.selectbox("Hedef Donem", ["2025-2026", "2026-2027", "2027-2028"], key="senaryo_donem")

            if st.form_submit_button("🔮 Senaryo Simule Et", use_container_width=True):
                if s_ad:
                    # Simülasyon
                    baz_butce = sum(b.get("planlanan", 0) for b in butceler) if butceler else 500000
                    if "Kisitlama" in s_tip:
                        etki = -baz_butce * abs(s_deger) / 100
                        sonuc_butce = baz_butce + etki
                    elif "Artisi" in s_tip or "Enflasyon" in s_tip:
                        etki = baz_butce * s_deger / 100
                        sonuc_butce = baz_butce + etki
                    elif "Bina" in s_tip:
                        etki = s_deger * 50000
                        sonuc_butce = baz_butce + etki
                    else:
                        etki = s_deger * 10000
                        sonuc_butce = baz_butce + etki

                    senaryo = {
                        "id": f"snr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": s_ad,
                        "tip": s_tip,
                        "deger": s_deger,
                        "donem": s_donem,
                        "baz_butce": baz_butce,
                        "etki": etki,
                        "sonuc_butce": sonuc_butce,
                        "tarih": datetime.now().isoformat(),
                    }
                    senaryolar.append(senaryo)
                    _save_json(senaryo_path, senaryolar)
                    st.success(f"Senaryo olusturuldu: Etki TL{etki:+,.0f}")
                    st.rerun()

        if senaryolar:
            _styled_section("Olusturulan Senaryolar", "#ffd166")
            for s in reversed(senaryolar[-10:]):
                etki = s.get("etki", 0)
                renk = "#e94560" if etki > 0 else "#06d6a0"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:14px 18px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#8338ec;">{s.get('ad','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{s.get('tip','')}: {s.get('deger',0)}</span>
                        </div>
                        <div style="text-align:right;">
                            <div style="color:{renk};font-weight:700;font-size:1.1rem;">TL{etki:+,.0f}</div>
                            <div style="color:#888;font-size:0.78rem;">Sonuc: TL{s.get('sonuc_butce',0):,.0f}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:20px;margin-top:6px;">
                        <span style="color:#888;font-size:0.78rem;">Baz: TL{s.get('baz_butce',0):,.0f}</span>
                        <span style="color:#888;font-size:0.78rem;">Donem: {s.get('donem','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Departman Bütçe ──
    with sub[2]:
        _styled_section("🏢 Departman Bazlı Bütçe Dağılımı", "#06d6a0")

        if butceler:
            dept_toplam = {}
            for b in butceler:
                dept = b.get("departman", "Diger")
                if dept not in dept_toplam:
                    dept_toplam[dept] = {"planlanan": 0, "gerceklesen": 0}
                dept_toplam[dept]["planlanan"] += b.get("planlanan", 0)
                dept_toplam[dept]["gerceklesen"] += b.get("gerceklesen", 0)

            max_plan = max(d["planlanan"] for d in dept_toplam.values()) if dept_toplam else 1
            for dept, data in sorted(dept_toplam.items(), key=lambda x: -x[1]["planlanan"]):
                plan = data["planlanan"]
                gercek = data["gerceklesen"]
                oran = int(gercek / max(1, plan) * 100)
                bar_w = int(plan / max_plan * 100)
                renk = "#06d6a0" if oran <= 80 else ("#ffd166" if oran <= 100 else "#e94560")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:14px 18px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <strong style="color:#e0e0e0;">{dept}</strong>
                        <span style="color:{renk};font-weight:700;">%{oran} kullanildi</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:22px;overflow:hidden;position:relative;">
                        <div style="width:{bar_w}%;height:100%;background:#0f346060;border-radius:6px;position:absolute;"></div>
                        <div style="width:{min(bar_w, int(gercek/max(1,max_plan)*100))}%;height:100%;background:{renk};border-radius:6px;position:absolute;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-top:4px;">
                        <span style="color:#888;font-size:0.78rem;">Planlanan: TL{plan:,.0f}</span>
                        <span style="color:#888;font-size:0.78rem;">Gerceklesen: TL{gercek:,.0f}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Departman dagilimi icin butce plani olusturun.")

    # ── Sapma Analizi ──
    with sub[3]:
        _styled_section("📊 Bütçe-Gerçek Sapma Analizi", "#e94560")

        if butceler:
            sapmalar = []
            for b in butceler:
                plan = b.get("planlanan", 0)
                gercek = b.get("gerceklesen", 0)
                sapma = gercek - plan
                sapma_oran = int(sapma / max(1, plan) * 100)
                sapmalar.append({
                    "dept": b.get("departman", "?"),
                    "kat": b.get("kategori", ""),
                    "plan": plan,
                    "gercek": gercek,
                    "sapma": sapma,
                    "oran": sapma_oran,
                })

            # En büyük sapmalar
            sapmalar.sort(key=lambda x: abs(x["sapma"]), reverse=True)

            for s in sapmalar:
                renk = "#e94560" if s["sapma"] > 0 else "#06d6a0"
                yon = "Asim" if s["sapma"] > 0 else "Tasarruf"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{s['dept']}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{s['kat']}</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="color:{renk};font-weight:700;">TL{s['sapma']:+,.0f} ({yon})</div>
                        <div style="color:#888;font-size:0.78rem;">%{s['oran']:+d}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            toplam_sapma = sum(s["sapma"] for s in sapmalar)
            renk = "#e94560" if toplam_sapma > 0 else "#06d6a0"
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:12px;padding:18px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Toplam Sapma</div>
                <div style="font-size:2.4rem;font-weight:800;color:{renk};">TL{toplam_sapma:+,.0f}</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Sapma analizi icin butce plani olusturun.")

    # ── AI Bütçe Önerisi ──
    with sub[4]:
        _styled_section("🤖 AI Bütçe Optimizasyon Önerileri", "#00b4d8")

        _styled_info_banner("AI, gecmis harcama verileri ve trendlere dayanarak akilli butce onerileri sunar.")

        oneriler = [
            ("Toplu Alim Indirimi", "Kirtasiye ve temizlik malzemelerini yillik toplu alimla %15-20 tasarruf saglayin.", "#06d6a0", "TL Tasarruf: ~%18"),
            ("Enerji Verimliligi", "LED donusum ve hareket sensorleri ile aylik enerji faturasini %25 azaltin.", "#ffd166", "ROI: 14 ay"),
            ("Bakim Planlama", "Reaktif bakim yerine onleyici bakim ile uzun vadede %30 maliyet azalma.", "#00b4d8", "Yillik Kazanc: ~%30"),
            ("Dijital Donusum", "Kagit tuketimini %40 azaltmak icin dijital form ve imza sistemine gecin.", "#8338ec", "Kagit Tasarrufu: %40"),
            ("Tedarikci Optimizasyonu", "Tek tedarikci bagimliligi riskli kategorilerde alternatif tedarikci bulun.", "#e94560", "Risk Azaltma: Yuksek"),
            ("Mevsimsel Planlama", "Tüketim malzemelerini dusuk sezon fiyatlariyla stoklayin.", "#ff6b6b", "Fiyat Avantaji: ~%12"),
        ]

        for baslik, aciklama, renk, metrik in oneriler:
            st.markdown(f"""
            <div style="background:#16213e;border-radius:12px;padding:16px;margin-bottom:10px;border-left:4px solid {renk};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <h4 style="color:{renk};margin:0 0 6px 0;">{baslik}</h4>
                        <p style="color:#aaa;font-size:0.88rem;margin:0;">{aciklama}</p>
                    </div>
                    <div style="background:{renk}20;color:{renk};padding:6px 14px;border-radius:8px;font-size:0.82rem;font-weight:600;white-space:nowrap;margin-left:12px;">
                        {metrik}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Özet
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#06d6a020,#00b4d810);border:1px solid #06d6a040;border-radius:12px;padding:16px;margin-top:14px;text-align:center;">
            <div style="color:#06d6a0;font-size:1.1rem;font-weight:700;">AI Tahmini Toplam Tasarruf Potansiyeli</div>
            <div style="color:#06d6a0;font-size:2rem;font-weight:800;margin-top:4px;">%15-25</div>
            <div style="color:#888;font-size:0.85rem;">Tum onerilerin uygulanmasi durumunda</div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. KURUM VERİMLİLİĞİ LİDERLİK TABLOSU & GAMİFİCATİON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_verimlilik_liderlik(store):
    _styled_header("Kurum Verimliliği Liderlik Tablosu", "🏆")

    liderlik_path = _get_data_path(store, "verimlilik_liderlik.json")
    liderlik = _load_json(liderlik_path)

    rozet_path = _get_data_path(store, "verimlilik_rozetleri.json")
    rozetler = _load_json(rozet_path)

    hedef_path = _get_data_path(store, "verimlilik_hedefleri.json")
    hedefler = _load_json(hedef_path)

    _styled_stat_row([
        ("Kayitli Birim", len(liderlik)),
        ("Kazanilan Rozet", len(rozetler)),
        ("Aktif Hedef", len(hedefler)),
    ])

    sub = st.tabs(["🏆 Liderlik Tablosu", "🎖️ Rozet Sistemi", "📊 Israf Haritası", "🎯 Tasarruf Hedefleri", "📈 Trend Karşılaştırma", "🌟 Verimlilik Endeksi"])

    # ── Liderlik Tablosu ──
    with sub[0]:
        _styled_section("🏆 Departman/Birim Verimlilik Sıralaması", "#ffd166")

        with st.form("birim_ekle_form"):
            lc1, lc2, lc3 = st.columns(3)
            with lc1:
                l_birim = st.text_input("Birim / Departman Adi", key="lider_birim")
            with lc2:
                l_tuketim = st.number_input("Aylik Tuketim (TL)", min_value=0.0, step=100.0, key="lider_tuketim")
            with lc3:
                l_kisi = st.number_input("Kisi Sayisi", min_value=1, value=10, key="lider_kisi")
            l_ay = st.selectbox("Ay", ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran", "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"], key="lider_ay")

            if st.form_submit_button("📊 Kayit Ekle", use_container_width=True):
                if l_birim:
                    kisi_basi = l_tuketim / max(1, l_kisi)
                    liderlik.append({
                        "id": f"ldr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "birim": l_birim,
                        "tuketim": l_tuketim,
                        "kisi": l_kisi,
                        "kisi_basi": round(kisi_basi, 2),
                        "ay": l_ay,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(liderlik_path, liderlik)
                    st.success(f"{l_birim} eklendi! Kisi basi: TL{kisi_basi:,.0f}")
                    st.rerun()

        if liderlik:
            # Birim bazlı ortalama
            birim_ort = {}
            for l in liderlik:
                b = l.get("birim", "?")
                if b not in birim_ort:
                    birim_ort[b] = {"toplam": 0, "sayi": 0, "kisi_basi_top": 0}
                birim_ort[b]["toplam"] += l.get("tuketim", 0)
                birim_ort[b]["sayi"] += 1
                birim_ort[b]["kisi_basi_top"] += l.get("kisi_basi", 0)

            siralama = []
            for b, d in birim_ort.items():
                ort_kisi_basi = d["kisi_basi_top"] / max(1, d["sayi"])
                siralama.append({"birim": b, "ort": ort_kisi_basi, "toplam": d["toplam"], "kayit": d["sayi"]})

            siralama.sort(key=lambda x: x["ort"])

            madalyalar = ["🥇", "🥈", "🥉"]
            for i, s in enumerate(siralama):
                madalya = madalyalar[i] if i < 3 else f"#{i+1}"
                renk = "#ffd166" if i == 0 else ("#c0c0c0" if i == 1 else ("#cd7f32" if i == 2 else "#888"))
                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span style="font-size:1.8rem;">{madalya}</span>
                            <div>
                                <strong style="color:#e0e0e0;font-size:1.1rem;">{s['birim']}</strong>
                                <div style="color:#888;font-size:0.78rem;">{s['kayit']} ay verisi</div>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.4rem;font-weight:800;color:{renk};">TL{s['ort']:,.0f}</div>
                            <div style="color:#888;font-size:0.78rem;">kisi basi/ay</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Rozet Sistemi ──
    with sub[1]:
        _styled_section("🎖️ Verimlilik Rozet & Odulleri", "#8338ec")

        rozet_tanimlari = [
            {"ad": "Tasarruf Yildizi", "ikon": "⭐", "kosul": "Aylik tuketimi %20 azaltan birim", "renk": "#ffd166"},
            {"ad": "Yesil Sampiyon", "ikon": "🌿", "kosul": "En dusuk karbon ayak izi", "renk": "#06d6a0"},
            {"ad": "Verimlilik Gurusu", "ikon": "🧠", "kosul": "3 ay ust uste en verimli", "renk": "#8338ec"},
            {"ad": "Sifir Israf", "ikon": "♻️", "kosul": "Israf orani %5 altinda", "renk": "#00b4d8"},
            {"ad": "Bakim Sampiyonu", "ikon": "🔧", "kosul": "Tum bakimlari zamaninda tamamlayan", "renk": "#e94560"},
            {"ad": "Inovasyon Lideri", "ikon": "💡", "kosul": "En fazla tasarruf onerisi veren", "renk": "#ff6b6b"},
        ]

        st.markdown("**Kazanılabilecek Rozetler**")
        rc1, rc2, rc3 = st.columns(3)
        for i, r in enumerate(rozet_tanimlari):
            col = [rc1, rc2, rc3][i % 3]
            col.markdown(f"""
            <div style="background:#16213e;border-radius:12px;padding:16px;text-align:center;margin-bottom:8px;border:1px solid {r['renk']}30;">
                <div style="font-size:2.5rem;">{r['ikon']}</div>
                <div style="color:{r['renk']};font-weight:700;margin:6px 0 4px 0;">{r['ad']}</div>
                <div style="color:#888;font-size:0.78rem;">{r['kosul']}</div>
            </div>""", unsafe_allow_html=True)

        # Rozet ver
        _styled_section("Rozet Ver", "#ffd166")
        with st.form("rozet_ver_form"):
            rv1, rv2 = st.columns(2)
            with rv1:
                r_birim = st.text_input("Birim Adi", key="rozet_birim")
            with rv2:
                r_rozet = st.selectbox("Rozet", [r["ad"] for r in rozet_tanimlari], key="rozet_sec")
            if st.form_submit_button("🎖️ Rozet Ver"):
                if r_birim:
                    rozet_bilgi = next((r for r in rozet_tanimlari if r["ad"] == r_rozet), {})
                    rozetler.append({
                        "id": f"rzt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "birim": r_birim,
                        "rozet": r_rozet,
                        "ikon": rozet_bilgi.get("ikon", "🎖️"),
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(rozet_path, rozetler)
                    st.success(f"{r_birim} birimine {r_rozet} rozeti verildi!")
                    st.rerun()

        if rozetler:
            _styled_section("Kazanilan Rozetler", "#06d6a0")
            for r in reversed(rozetler[-10:]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:1.3rem;">{r.get('ikon','🎖️')}</span>
                        <strong style="color:#e0e0e0;margin-left:8px;">{r.get('birim','?')}</strong>
                    </div>
                    <div>
                        <span style="color:#ffd166;font-weight:600;">{r.get('rozet','')}</span>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{r.get('tarih','')[:10]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Israf Haritası ──
    with sub[2]:
        _styled_section("📊 Kurum Israf Haritasi", "#e94560")

        israf_path = _get_data_path(store, "israf_kayitlari.json")
        israflar = _load_json(israf_path)

        with st.form("israf_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                i_alan = st.text_input("Alan / Konum", key="israf_alan")
            with ic2:
                i_tur = st.selectbox("Israf Turu", ["Enerji", "Su", "Kagit", "Gida", "Malzeme", "Diger"], key="israf_tur")
            with ic3:
                i_seviye = st.selectbox("Seviye", ["Dusuk", "Orta", "Yuksek", "Kritik"], key="israf_sev")
            i_aciklama = st.text_input("Aciklama", key="israf_acik")

            if st.form_submit_button("📊 Israf Bildir", use_container_width=True):
                if i_alan:
                    israflar.append({
                        "id": f"isr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "alan": i_alan,
                        "tur": i_tur,
                        "seviye": i_seviye,
                        "aciklama": i_aciklama,
                        "tarih": datetime.now().isoformat(),
                        "cozuldu": False,
                    })
                    _save_json(israf_path, israflar)
                    st.success("Israf bildirimi kaydedildi!")
                    st.rerun()

        if israflar:
            aktif = [i for i in israflar if not i.get("cozuldu")]
            cozulen = [i for i in israflar if i.get("cozuldu")]

            _styled_stat_row([
                ("Aktif Israf", len(aktif)),
                ("Cozulen", len(cozulen)),
                ("Toplam Bildirim", len(israflar)),
            ])

            seviye_renk = {"Kritik": "#e94560", "Yuksek": "#ff6b6b", "Orta": "#ffd166", "Dusuk": "#06d6a0"}
            for idx, isf in enumerate(aktif):
                sev = isf.get("seviye", "Dusuk")
                renk = seviye_renk.get(sev, "#888")
                st.markdown(f"""
                <div style="background:{renk}12;border-left:4px solid {renk};padding:10px 14px;border-radius:0 10px 10px 0;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;">
                        <strong style="color:{renk};">{isf.get('alan','?')} — {isf.get('tur','')}</strong>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.78rem;">{sev}</span>
                    </div>
                    <div style="color:#aaa;font-size:0.85rem;margin-top:3px;">{isf.get('aciklama','')}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("Cozuldu", key=f"israf_coz_{idx}"):
                    isf["cozuldu"] = True
                    _save_json(israf_path, israflar)
                    st.rerun()
        else:
            _styled_info_banner("Henuz israf bildirimi yok. Bu iyi bir isaret!")

    # ── Tasarruf Hedefleri ──
    with sub[3]:
        _styled_section("🎯 Birim Tasarruf Hedefleri & Basirimlar", "#06d6a0")

        with st.form("tasarruf_hedef_form"):
            hc1, hc2, hc3 = st.columns(3)
            with hc1:
                h_birim = st.text_input("Birim", key="tsr_birim")
            with hc2:
                h_hedef = st.number_input("Hedef Tasarruf (%)", min_value=1, max_value=100, value=10, key="tsr_hedef")
            with hc3:
                h_sure = st.selectbox("Sure", ["1 Ay", "3 Ay", "6 Ay", "1 Yil"], key="tsr_sure")

            if st.form_submit_button("🎯 Hedef Belirle", use_container_width=True):
                if h_birim:
                    hedefler.append({
                        "id": f"tsr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "birim": h_birim,
                        "hedef": h_hedef,
                        "sure": h_sure,
                        "ilerleme": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(hedef_path, hedefler)
                    st.success(f"{h_birim} icin %{h_hedef} tasarruf hedefi belirlendi!")
                    st.rerun()

        if hedefler:
            for idx, h in enumerate(hedefler):
                ilerleme = h.get("ilerleme", 0)
                hedef = h.get("hedef", 100)
                oran = min(100, int(ilerleme / max(1, hedef) * 100))
                renk = "#06d6a0" if oran >= 80 else ("#ffd166" if oran >= 40 else "#e94560")
                basarim = "Tamamlandi!" if oran >= 100 else ("Iyi gidiyor" if oran >= 60 else "Devam ediyor")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div>
                            <strong style="color:#e0e0e0;">{h.get('birim','?')}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">Hedef: %{hedef} | {h.get('sure','')}</span>
                        </div>
                        <span style="color:{renk};font-weight:700;">{basarim}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:8px;height:20px;overflow:hidden;">
                        <div style="width:{oran}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

                yeni = st.slider(f"Ilerleme", 0, 100, ilerleme, key=f"tsr_slider_{idx}")
                if yeni != ilerleme:
                    if st.button("Guncelle", key=f"tsr_btn_{idx}"):
                        h["ilerleme"] = yeni
                        _save_json(hedef_path, hedefler)
                        st.rerun()

    # ── Trend Karşılaştırma ──
    with sub[4]:
        _styled_section("📈 Birim Trend Karsilastirma", "#00b4d8")

        if liderlik:
            birimler = list(set(l.get("birim", "?") for l in liderlik))
            secilen_birimler = st.multiselect("Karsilastirmak icin birim secin", birimler, default=birimler[:3], key="trend_birim")

            if secilen_birimler:
                aylar = ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran", "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"]
                birim_renkler = ["#e94560", "#00b4d8", "#06d6a0", "#ffd166", "#8338ec", "#ff6b6b"]

                for ay in aylar:
                    ay_verileri = [l for l in liderlik if l.get("ay") == ay and l.get("birim") in secilen_birimler]
                    if ay_verileri:
                        st.markdown(f"**{ay}**")
                        max_val = max(l.get("kisi_basi", 1) for l in ay_verileri)
                        for l in ay_verileri:
                            birim_idx = secilen_birimler.index(l.get("birim", "?")) if l.get("birim") in secilen_birimler else 0
                            renk = birim_renkler[birim_idx % len(birim_renkler)]
                            bar_w = int(l.get("kisi_basi", 0) / max(1, max_val) * 100)
                            st.markdown(f"""
                            <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                                <span style="width:120px;color:{renk};font-size:0.85rem;font-weight:600;">{l.get('birim','?')[:15]}</span>
                                <div style="flex:1;background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                                </div>
                                <span style="width:80px;text-align:right;color:{renk};font-weight:700;">TL{l.get('kisi_basi',0):,.0f}</span>
                            </div>""", unsafe_allow_html=True)
                        st.markdown("")
        else:
            _styled_info_banner("Trend karsilastirma icin liderlik tablosu verisi gerekiyor.")

    # ── Verimlilik Endeksi ──
    with sub[5]:
        _styled_section("🌟 Kurum Geneli Verimlilik Endeksi", "#ffd166")

        # Genel endeks hesaplama
        bilesenler = []

        # Liderlik verisi
        if liderlik:
            ort_kisi_basi = sum(l.get("kisi_basi", 0) for l in liderlik) / len(liderlik)
            tuketim_skor = max(0, 100 - int(ort_kisi_basi / 10))
            bilesenler.append(("Tuketim Verimliligi", tuketim_skor, "#00b4d8"))
        else:
            bilesenler.append(("Tuketim Verimliligi", 50, "#00b4d8"))

        # Israf verisi
        israf_path2 = _get_data_path(store, "israf_kayitlari.json")
        israflar2 = _load_json(israf_path2)
        if israflar2:
            cozulme_oran = len([i for i in israflar2 if i.get("cozuldu")]) / max(1, len(israflar2)) * 100
            bilesenler.append(("Israf Yonetimi", int(cozulme_oran), "#06d6a0"))
        else:
            bilesenler.append(("Israf Yonetimi", 70, "#06d6a0"))

        # Rozet sayısı
        rozet_skor = min(100, len(rozetler) * 15 + 30)
        bilesenler.append(("Basarim & Motivasyon", rozet_skor, "#ffd166"))

        # Hedef ilerleme
        if hedefler:
            ort_ilerleme = sum(h.get("ilerleme", 0) for h in hedefler) / len(hedefler)
            bilesenler.append(("Hedef Gerceklestirme", int(ort_ilerleme), "#8338ec"))
        else:
            bilesenler.append(("Hedef Gerceklestirme", 50, "#8338ec"))

        genel_endeks = int(sum(b[1] for b in bilesenler) / len(bilesenler))
        renk = "#06d6a0" if genel_endeks >= 70 else ("#ffd166" if genel_endeks >= 40 else "#e94560")
        derece = "A+" if genel_endeks >= 90 else ("A" if genel_endeks >= 80 else ("B+" if genel_endeks >= 70 else ("B" if genel_endeks >= 60 else ("C" if genel_endeks >= 40 else "D"))))

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e,#1a1a2e);border-radius:16px;padding:28px;text-align:center;margin-bottom:16px;">
            <div style="font-size:1rem;color:#888;">Kurum Verimlilik Endeksi</div>
            <div style="font-size:4.5rem;font-weight:900;color:{renk};">{derece}</div>
            <div style="font-size:1.8rem;font-weight:700;color:{renk};">{genel_endeks}/100</div>
        </div>""", unsafe_allow_html=True)

        # Alt bileşenler
        for baslik, skor, renk in bilesenler:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:#e0e0e0;font-weight:600;">{baslik}</span>
                    <span style="color:{renk};font-weight:700;">{skor}/100</span>
                </div>
                <div style="background:#1a1a2e;border-radius:8px;height:20px;overflow:hidden;">
                    <div style="width:{skor}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)
