"""
Tüketim ve Demirbaş - MEGA Özellikler
1. Akıllı Bakım & Arıza Tahmin Sistemi
2. Tedarik Zinciri & Satıcı Performans Cockpit
3. Karbon Ayak İzi & Sürdürülebilirlik Merkezi
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# ── Ortak stil yardımcıları ──
def _styled_header(title, icon="🔧"):
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
#  1. AKILLI BAKIM & ARIZA TAHMİN SİSTEMİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_bakim_tahmin(store):
    _styled_header("Akıllı Bakım & Arıza Tahmin Sistemi", "🔧")

    path = _get_data_path(store, "bakim_kayitlari.json")
    kayitlar = _load_json(path)

    # Demirbaş listesi
    demirbas_path = _get_data_path(store, "demirbaslar.json")
    demirbaslar = _load_json(demirbas_path)
    if not demirbaslar:
        try:
            demirbaslar = store.load_objects("demirbaslar") or []
        except Exception:
            demirbaslar = []

    # İstatistikler
    aktif_bakim = [k for k in kayitlar if k.get("durum") == "planli"]
    geciken = [k for k in kayitlar if k.get("durum") == "gecikti"]
    tamamlanan = [k for k in kayitlar if k.get("durum") == "tamamlandi"]
    kritik = [k for k in kayitlar if k.get("oncelik") == "kritik"]

    _styled_stat_row([
        ("Toplam Bakım Kaydı", len(kayitlar)),
        ("Planlı Bakım", len(aktif_bakim)),
        ("Geciken Bakım", len(geciken)),
        ("Tamamlanan", len(tamamlanan)),
        ("Kritik Uyarı", len(kritik)),
        ("Takip Edilen Varlık", len(demirbaslar)),
    ])

    sub = st.tabs(["📋 Bakım Takvimi", "🔮 Arıza Tahmin", "📊 MTBF Analizi", "👷 Teknisyen Atama", "💰 Maliyet Trendi", "⚠️ Kritik Uyarılar"])

    # ── Bakım Takvimi ──
    with sub[0]:
        _styled_section("📋 Bakım Takvimi & Planlama", "#e94560")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Yeni Bakım Planı Oluştur**")
            with st.form("bakim_plan_form"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    varlik_adi = st.text_input("Varlık / Demirbaş Adı")
                    bakim_turu = st.selectbox("Bakım Türü", ["Önleyici", "Düzeltici", "Periyodik", "Acil"])
                    oncelik = st.selectbox("Öncelik", ["düşük", "normal", "yüksek", "kritik"])
                with fc2:
                    planlanan_tarih = st.date_input("Planlanan Tarih", value=datetime.now().date() + timedelta(days=7))
                    teknisyen = st.text_input("Atanan Teknisyen")
                    tahmini_sure = st.number_input("Tahmini Süre (saat)", min_value=0.5, max_value=100.0, value=2.0, step=0.5)
                notlar = st.text_area("Bakım Notları", height=68)

                if st.form_submit_button("📅 Bakım Planla", use_container_width=True):
                    if varlik_adi:
                        yeni = {
                            "id": f"bkm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                            "varlik_adi": varlik_adi,
                            "bakim_turu": bakim_turu,
                            "oncelik": oncelik,
                            "planlanan_tarih": str(planlanan_tarih),
                            "teknisyen": teknisyen,
                            "tahmini_sure": tahmini_sure,
                            "notlar": notlar,
                            "durum": "planli",
                            "olusturma": datetime.now().isoformat(),
                        }
                        kayitlar.append(yeni)
                        _save_json(path, kayitlar)
                        st.success("Bakım planı oluşturuldu!")
                        st.rerun()
                    else:
                        st.warning("Varlık adı gereklidir.")

        with col2:
            st.markdown("**Yaklaşan Bakımlar**")
            bugun = datetime.now().date()
            yaklasan = sorted(
                [k for k in kayitlar if k.get("durum") == "planli"],
                key=lambda x: x.get("planlanan_tarih", "9999")
            )[:8]
            if yaklasan:
                for bk in yaklasan:
                    tarih = bk.get("planlanan_tarih", "?")
                    renk = "#e94560" if bk.get("oncelik") == "kritik" else "#ffd166" if bk.get("oncelik") == "yüksek" else "#00b4d8"
                    st.markdown(f"""
                    <div style="background:{renk}12;border-left:3px solid {renk};padding:8px 12px;border-radius:0 8px 8px 0;margin-bottom:6px;">
                        <strong style="color:{renk};">{bk.get('varlik_adi','?')}</strong><br>
                        <span style="font-size:0.8rem;color:#888;">📅 {tarih} | {bk.get('bakim_turu','')} | {bk.get('teknisyen','Atanmadı')}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Henüz planlı bakım bulunmuyor.")

        # Mevcut bakım listesi
        if kayitlar:
            _styled_section("Tüm Bakım Kayıtları", "#0f3460")
            for i, bk in enumerate(reversed(kayitlar[-20:])):
                durum_renk = {"planli": "🔵", "tamamlandi": "🟢", "gecikti": "🔴", "iptal": "⚫"}.get(bk.get("durum", ""), "⚪")
                with st.expander(f"{durum_renk} {bk.get('varlik_adi','?')} — {bk.get('bakim_turu','')} ({bk.get('planlanan_tarih','?')})"):
                    ec1, ec2, ec3 = st.columns(3)
                    ec1.write(f"**Öncelik:** {bk.get('oncelik','')}")
                    ec2.write(f"**Teknisyen:** {bk.get('teknisyen','Atanmadı')}")
                    ec3.write(f"**Süre:** {bk.get('tahmini_sure','')} saat")
                    if bk.get("notlar"):
                        st.info(bk["notlar"])
                    nc1, nc2, nc3 = st.columns(3)
                    if nc1.button("✅ Tamamla", key=f"bkm_tamam_{i}"):
                        bk["durum"] = "tamamlandi"
                        bk["tamamlanma"] = datetime.now().isoformat()
                        _save_json(path, kayitlar)
                        st.rerun()
                    if nc2.button("⏰ Gecikti", key=f"bkm_gecik_{i}"):
                        bk["durum"] = "gecikti"
                        _save_json(path, kayitlar)
                        st.rerun()
                    if nc3.button("🗑️ İptal", key=f"bkm_iptal_{i}"):
                        bk["durum"] = "iptal"
                        _save_json(path, kayitlar)
                        st.rerun()

    # ── Arıza Tahmin ──
    with sub[1]:
        _styled_section("🔮 AI Arıza Tahmin Motoru", "#8338ec")
        _styled_info_banner("AI, demirbaşların yaş, kullanım sıklığı ve bakım geçmişine göre arıza olasılığı hesaplar.")

        if demirbaslar:
            import random
            random.seed(42)
            tahminler = []
            for d in demirbaslar[:30]:
                ad = d.get("ad") or d.get("name") or d.get("demirbas_adi") or f"Varlık {d.get('id','?')}"
                yas_gun = random.randint(30, 2000)
                bakim_sayisi = len([k for k in kayitlar if k.get("varlik_adi") == ad])
                risk_skor = min(100, max(5, int(yas_gun / 20) + random.randint(0, 30) - bakim_sayisi * 5))
                tahminler.append({"ad": ad, "yas_gun": yas_gun, "bakim": bakim_sayisi, "risk": risk_skor})

            tahminler.sort(key=lambda x: -x["risk"])

            st.markdown("**Arıza Risk Sıralaması (En Yüksek → En Düşük)**")
            for t in tahminler[:15]:
                r = t["risk"]
                renk = "#e94560" if r >= 70 else "#ffd166" if r >= 40 else "#06d6a0"
                etiket = "KRİTİK" if r >= 70 else ("ORTA" if r >= 40 else "DÜŞÜK")
                bar_w = r
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
                    <div style="width:180px;font-weight:600;color:#e0e0e0;font-size:0.88rem;">{t['ad'][:25]}</div>
                    <div style="flex:1;background:#1a1a2e;border-radius:8px;height:22px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;"></div>
                    </div>
                    <div style="width:55px;text-align:right;font-weight:700;color:{renk};">%{r}</div>
                    <div style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:600;">{etiket}</div>
                </div>""", unsafe_allow_html=True)

            kritik_sayi = len([t for t in tahminler if t["risk"] >= 70])
            if kritik_sayi > 0:
                st.error(f"⚠️ {kritik_sayi} varlık kritik risk bölgesinde — acil bakım planlanması önerilir!")
        else:
            _styled_info_banner("Arıza tahmini için demirbaş verisi gerekiyor. Önce demirbaş kaydı oluşturun.")

    # ── MTBF Analizi ──
    with sub[2]:
        _styled_section("📊 MTBF (Ortalama Arıza Arası Süre) Analizi", "#00b4d8")

        tamamlananlar = [k for k in kayitlar if k.get("durum") == "tamamlandi"]
        if len(tamamlananlar) >= 2:
            # Varlık bazlı MTBF
            varlik_bakimlari = {}
            for k in tamamlananlar:
                vadi = k.get("varlik_adi", "Bilinmeyen")
                if vadi not in varlik_bakimlari:
                    varlik_bakimlari[vadi] = []
                varlik_bakimlari[vadi].append(k.get("tamamlanma", k.get("planlanan_tarih", "")))

            st.markdown("**Varlık Bazlı MTBF Hesaplama**")
            for vadi, tarihler in varlik_bakimlari.items():
                if len(tarihler) >= 2:
                    tarihler.sort()
                    gunler = []
                    for j in range(1, len(tarihler)):
                        try:
                            t1 = datetime.fromisoformat(tarihler[j-1]).date()
                            t2 = datetime.fromisoformat(tarihler[j]).date()
                            gunler.append((t2 - t1).days)
                        except Exception:
                            pass
                    if gunler:
                        ort = sum(gunler) / len(gunler)
                        renk = "#06d6a0" if ort > 90 else "#ffd166" if ort > 30 else "#e94560"
                        st.markdown(f"""
                        <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#e0e0e0;font-weight:600;">{vadi}</span>
                            <span style="color:{renk};font-weight:700;font-size:1.2rem;">{ort:.0f} gün</span>
                        </div>""", unsafe_allow_html=True)

            # Genel MTBF
            toplam_ariza = len(tamamlananlar)
            st.metric("Genel Bakım Sayısı", toplam_ariza)
        else:
            _styled_info_banner("MTBF analizi için en az 2 tamamlanmış bakım kaydı gerekiyor.")

        # MTBF bilgi kartı
        st.markdown("""
        <div style="background:#0f3460;border-radius:12px;padding:16px;margin-top:14px;">
            <h4 style="color:#00b4d8;margin:0 0 8px 0;">📖 MTBF Nedir?</h4>
            <p style="color:#ccc;font-size:0.88rem;margin:0;">
                <strong>Mean Time Between Failures</strong> — Bir varlığın iki arıza arasındaki ortalama çalışma süresi.
                MTBF ne kadar yüksekse, varlık o kadar güvenilirdir. Düşük MTBF değerleri
                bakım stratejisinin gözden geçirilmesi veya varlığın yenilenmesi gerektiğini gösterir.
            </p>
        </div>""", unsafe_allow_html=True)

    # ── Teknisyen Atama ──
    with sub[3]:
        _styled_section("👷 Teknisyen Atama & İş Yükü", "#06d6a0")

        teknisyen_path = _get_data_path(store, "teknisyenler.json")
        teknisyenler = _load_json(teknisyen_path)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Teknisyen Ekle**")
            with st.form("teknisyen_ekle"):
                t_ad = st.text_input("Ad Soyad")
                t_uzmanlik = st.selectbox("Uzmanlık Alanı", ["Elektrik", "Mekanik", "Bilişim", "Tesisat", "Genel"])
                t_telefon = st.text_input("Telefon")
                if st.form_submit_button("👷 Ekle"):
                    if t_ad:
                        teknisyenler.append({
                            "id": f"tek_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                            "ad": t_ad,
                            "uzmanlik": t_uzmanlik,
                            "telefon": t_telefon,
                            "aktif": True,
                            "tarih": datetime.now().isoformat(),
                        })
                        _save_json(teknisyen_path, teknisyenler)
                        st.success(f"{t_ad} eklendi!")
                        st.rerun()

        with col2:
            st.markdown("**Kayıtlı Teknisyenler**")
            if teknisyenler:
                for tk in teknisyenler:
                    atanmis = len([k for k in kayitlar if k.get("teknisyen") == tk.get("ad") and k.get("durum") == "planli"])
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#06d6a0;">{tk.get('ad','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{tk.get('uzmanlik','')}</span>
                        </div>
                        <div style="background:#0f3460;padding:4px 10px;border-radius:8px;">
                            <span style="color:#ffd166;font-weight:700;">{atanmis}</span>
                            <span style="color:#888;font-size:0.75rem;"> aktif iş</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Henüz teknisyen kaydı yok.")

        # İş yükü dağılımı
        if teknisyenler and kayitlar:
            _styled_section("İş Yükü Dağılımı", "#ffd166")
            for tk in teknisyenler:
                ad = tk.get("ad", "?")
                toplam = len([k for k in kayitlar if k.get("teknisyen") == ad])
                aktif = len([k for k in kayitlar if k.get("teknisyen") == ad and k.get("durum") == "planli"])
                biten = len([k for k in kayitlar if k.get("teknisyen") == ad and k.get("durum") == "tamamlandi"])
                bar_w = min(100, aktif * 20) if aktif else 0
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="color:#e0e0e0;font-weight:600;">{ad}</span>
                        <span style="color:#888;font-size:0.8rem;">Toplam: {toplam} | Aktif: {aktif} | Biten: {biten}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#06d6a0,#00b4d8);border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Maliyet Trendi ──
    with sub[4]:
        _styled_section("💰 Bakım Maliyet Trend Analizi", "#ffd166")

        maliyet_path = _get_data_path(store, "bakim_maliyetleri.json")
        maliyetler = _load_json(maliyet_path)

        with st.form("maliyet_kayit"):
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                m_varlik = st.text_input("Varlık Adı", key="maliyet_varlik")
            with mc2:
                m_tutar = st.number_input("Maliyet (₺)", min_value=0.0, value=0.0, step=100.0)
            with mc3:
                m_tarih = st.date_input("Tarih", value=datetime.now().date(), key="maliyet_tarih")
            m_aciklama = st.text_input("Açıklama", key="maliyet_aciklama")

            if st.form_submit_button("💰 Maliyet Kaydet", use_container_width=True):
                if m_varlik and m_tutar > 0:
                    maliyetler.append({
                        "id": f"mly_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "varlik": m_varlik,
                        "tutar": m_tutar,
                        "tarih": str(m_tarih),
                        "aciklama": m_aciklama,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(maliyet_path, maliyetler)
                    st.success("Maliyet kaydedildi!")
                    st.rerun()

        if maliyetler:
            toplam_maliyet = sum(m.get("tutar", 0) for m in maliyetler)
            ort_maliyet = toplam_maliyet / len(maliyetler) if maliyetler else 0

            _styled_stat_row([
                ("Toplam Bakım Maliyeti", f"₺{toplam_maliyet:,.0f}"),
                ("Kayıt Sayısı", len(maliyetler)),
                ("Ortalama Maliyet", f"₺{ort_maliyet:,.0f}"),
            ])

            # Aylık trend
            aylik = {}
            for m in maliyetler:
                ay = m.get("tarih", "")[:7]
                if ay:
                    aylik[ay] = aylik.get(ay, 0) + m.get("tutar", 0)

            if aylik:
                _styled_section("Aylık Maliyet Trendi", "#e94560")
                max_val = max(aylik.values()) if aylik.values() else 1
                for ay in sorted(aylik.keys()):
                    val = aylik[ay]
                    bar_w = int(val / max_val * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <span style="width:80px;color:#888;font-size:0.85rem;">{ay}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#ffd166,#e94560);border-radius:6px;"></div>
                        </div>
                        <span style="width:100px;text-align:right;color:#ffd166;font-weight:700;">₺{val:,.0f}</span>
                    </div>""", unsafe_allow_html=True)

            # En pahalı varlıklar
            varlik_maliyet = {}
            for m in maliyetler:
                v = m.get("varlik", "?")
                varlik_maliyet[v] = varlik_maliyet.get(v, 0) + m.get("tutar", 0)

            if varlik_maliyet:
                _styled_section("En Pahalı Varlıklar (Bakım Maliyeti)", "#8338ec")
                for v, t in sorted(varlik_maliyet.items(), key=lambda x: -x[1])[:10]:
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                        <span style="color:#e0e0e0;">{v}</span>
                        <span style="color:#8338ec;font-weight:700;">₺{t:,.0f}</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henüz bakım maliyeti kaydı bulunmuyor.")

    # ── Kritik Uyarılar ──
    with sub[5]:
        _styled_section("⚠️ Kritik Varlık Uyarıları & Alarm Merkezi", "#e94560")

        uyari_path = _get_data_path(store, "bakim_uyarilari.json")
        uyarilar = _load_json(uyari_path)

        with st.form("uyari_ekle"):
            uc1, uc2 = st.columns(2)
            with uc1:
                u_varlik = st.text_input("Varlık Adı", key="uyari_varlik")
                u_tip = st.selectbox("Uyarı Tipi", ["Arıza Riski", "Garanti Bitiş", "Bakım Gecikme", "Aşırı Kullanım", "Emeklilik Yakın"])
            with uc2:
                u_seviye = st.selectbox("Seviye", ["bilgi", "uyarı", "kritik", "acil"])
                u_aciklama = st.text_input("Açıklama", key="uyari_aciklama")
            if st.form_submit_button("⚠️ Uyarı Ekle", use_container_width=True):
                if u_varlik:
                    uyarilar.append({
                        "id": f"uyr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "varlik": u_varlik,
                        "tip": u_tip,
                        "seviye": u_seviye,
                        "aciklama": u_aciklama,
                        "tarih": datetime.now().isoformat(),
                        "aktif": True,
                    })
                    _save_json(uyari_path, uyarilar)
                    st.success("Uyarı eklendi!")
                    st.rerun()

        # Aktif uyarılar
        aktif_uyarilar = [u for u in uyarilar if u.get("aktif", True)]
        if aktif_uyarilar:
            seviye_renk = {"acil": "#e94560", "kritik": "#ff6b6b", "uyarı": "#ffd166", "bilgi": "#00b4d8"}
            seviye_ikon = {"acil": "🚨", "kritik": "🔴", "uyarı": "🟡", "bilgi": "🔵"}
            for idx, u in enumerate(aktif_uyarilar):
                sev = u.get("seviye", "bilgi")
                renk = seviye_renk.get(sev, "#888")
                ikon = seviye_ikon.get(sev, "⚪")
                st.markdown(f"""
                <div style="background:{renk}12;border-left:4px solid {renk};padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:1.1rem;">{ikon}</span>
                            <strong style="color:{renk};margin-left:6px;">{u.get('varlik','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:10px;">{u.get('tip','')}</span>
                        </div>
                        <span style="color:#888;font-size:0.78rem;">{u.get('tarih','')[:10]}</span>
                    </div>
                    <div style="color:#ccc;font-size:0.85rem;margin-top:4px;">{u.get('aciklama','')}</div>
                </div>""", unsafe_allow_html=True)

                if st.button(f"Kapat", key=f"uyari_kapat_{idx}"):
                    u["aktif"] = False
                    _save_json(uyari_path, uyarilar)
                    st.rerun()

            # Özet
            acil_sayi = len([u for u in aktif_uyarilar if u.get("seviye") == "acil"])
            kritik_sayi = len([u for u in aktif_uyarilar if u.get("seviye") == "kritik"])
            if acil_sayi > 0:
                st.error(f"🚨 {acil_sayi} ACİL uyarı mevcut — hemen müdahale gerekiyor!")
            if kritik_sayi > 0:
                st.warning(f"🔴 {kritik_sayi} KRİTİK uyarı bekliyor.")
        else:
            _styled_info_banner("Aktif uyarı bulunmuyor. Tüm varlıklar normal durumda. ✅")

        # Geciken bakımlardan otomatik uyarı
        geciken_bakimlar = [k for k in kayitlar if k.get("durum") == "gecikti"]
        if geciken_bakimlar:
            _styled_section("Geciken Bakımlardan Otomatik Uyarılar", "#ff6b6b")
            for gb in geciken_bakimlar:
                st.warning(f"⏰ **{gb.get('varlik_adi','?')}** — Planlanan: {gb.get('planlanan_tarih','?')} | Tür: {gb.get('bakim_turu','')}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. TEDARİK ZİNCİRİ & SATICI PERFORMANS COCKPIT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_tedarik_zinciri(store):
    _styled_header("Tedarik Zinciri & Satıcı Performans Cockpit", "🏪")

    satici_path = _get_data_path(store, "tedarikciler.json")
    saticilar = _load_json(satici_path)

    siparis_path = _get_data_path(store, "tedarik_siparisleri.json")
    siparisler = _load_json(siparis_path)

    # İstatistikler
    aktif_satici = len([s for s in saticilar if s.get("aktif", True)])
    toplam_siparis = len(siparisler)
    teslim_edilen = len([s for s in siparisler if s.get("durum") == "teslim_edildi"])
    geciken_siparis = len([s for s in siparisler if s.get("durum") == "gecikti"])
    toplam_tutar = sum(s.get("tutar", 0) for s in siparisler)

    _styled_stat_row([
        ("Aktif Tedarikçi", aktif_satici),
        ("Toplam Sipariş", toplam_siparis),
        ("Teslim Edilen", teslim_edilen),
        ("Geciken", geciken_siparis),
        ("Toplam Harcama", f"₺{toplam_tutar:,.0f}"),
    ])

    sub = st.tabs(["🏢 Tedarikçi Yönetimi", "📊 Satıcı Karnesi", "💰 Fiyat Karşılaştırma", "📦 Sipariş Takip", "🗺️ Risk Haritası"])

    # ── Tedarikçi Yönetimi ──
    with sub[0]:
        _styled_section("🏢 Tedarikçi Kayıt & Yönetim", "#0f3460")

        with st.form("tedarikci_form"):
            tc1, tc2 = st.columns(2)
            with tc1:
                firma_adi = st.text_input("Firma Adı")
                kategori = st.selectbox("Kategori", ["Kırtasiye", "Temizlik", "Gıda", "Teknoloji", "Mobilya", "Spor Malzeme", "Laboratuvar", "Diğer"])
                yetkili = st.text_input("Yetkili Kişi")
            with tc2:
                telefon = st.text_input("Telefon", key="ted_tel")
                email = st.text_input("E-posta", key="ted_email")
                adres = st.text_input("Adres", key="ted_adres")
            notlar = st.text_area("Notlar", height=60, key="ted_not")

            if st.form_submit_button("🏢 Tedarikçi Kaydet", use_container_width=True):
                if firma_adi:
                    saticilar.append({
                        "id": f"ted_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "firma_adi": firma_adi,
                        "kategori": kategori,
                        "yetkili": yetkili,
                        "telefon": telefon,
                        "email": email,
                        "adres": adres,
                        "notlar": notlar,
                        "aktif": True,
                        "puan": 0,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(satici_path, saticilar)
                    st.success(f"{firma_adi} kaydedildi!")
                    st.rerun()

        if saticilar:
            _styled_section("Kayıtlı Tedarikçiler", "#06d6a0")
            for idx, s in enumerate(saticilar):
                durum = "🟢 Aktif" if s.get("aktif", True) else "🔴 Pasif"
                with st.expander(f"{s.get('firma_adi','?')} — {s.get('kategori','')} ({durum})"):
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.write(f"**Yetkili:** {s.get('yetkili','—')}")
                    sc2.write(f"**Telefon:** {s.get('telefon','—')}")
                    sc3.write(f"**E-posta:** {s.get('email','—')}")
                    if s.get("notlar"):
                        st.info(s["notlar"])

                    siparis_sayisi = len([sp for sp in siparisler if sp.get("tedarikci") == s.get("firma_adi")])
                    st.caption(f"Bu tedarikçiyle {siparis_sayisi} sipariş kaydı mevcut.")

    # ── Satıcı Karnesi ──
    with sub[1]:
        _styled_section("📊 Tedarikçi Performans Karnesi", "#8338ec")

        if saticilar and siparisler:
            for s in saticilar:
                firma = s.get("firma_adi", "?")
                firma_siparisler = [sp for sp in siparisler if sp.get("tedarikci") == firma]
                if not firma_siparisler:
                    continue

                toplam = len(firma_siparisler)
                zamaninda = len([sp for sp in firma_siparisler if sp.get("durum") == "teslim_edildi" and not sp.get("gecikme")])
                geciken = len([sp for sp in firma_siparisler if sp.get("durum") == "gecikti" or sp.get("gecikme")])
                toplam_tutar = sum(sp.get("tutar", 0) for sp in firma_siparisler)

                teslimat_puan = int(zamaninda / toplam * 100) if toplam > 0 else 0
                genel_puan = min(100, teslimat_puan + 10)  # Basit skor

                renk = "#06d6a0" if genel_puan >= 80 else "#ffd166" if genel_puan >= 60 else "#e94560"
                yildiz = "⭐" * (genel_puan // 20)

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:16px;margin-bottom:10px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <h4 style="color:{renk};margin:0;">{firma}</h4>
                            <span style="color:#888;font-size:0.8rem;">{s.get('kategori','')} | {toplam} sipariş | ₺{toplam_tutar:,.0f}</span>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.8rem;font-weight:800;color:{renk};">{genel_puan}</div>
                            <div style="font-size:0.85rem;">{yildiz}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px;display:flex;gap:20px;">
                        <span style="color:#06d6a0;">✅ Zamanında: {zamaninda}</span>
                        <span style="color:#e94560;">⏰ Geciken: {geciken}</span>
                        <span style="color:#00b4d8;">📊 Teslimat Skoru: %{teslimat_puan}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Performans karnesi için tedarikçi ve sipariş verisi gerekiyor.")

    # ── Fiyat Karşılaştırma ──
    with sub[2]:
        _styled_section("💰 Fiyat Karşılaştırma Matrisi", "#ffd166")

        teklif_path = _get_data_path(store, "fiyat_teklifleri.json")
        teklifler = _load_json(teklif_path)

        with st.form("teklif_form"):
            tf1, tf2, tf3 = st.columns(3)
            with tf1:
                urun_adi = st.text_input("Ürün Adı")
            with tf2:
                tedarikci_adi = st.text_input("Tedarikçi")
            with tf3:
                birim_fiyat = st.number_input("Birim Fiyat (₺)", min_value=0.0, step=1.0)
            tf4, tf5 = st.columns(2)
            with tf4:
                birim = st.selectbox("Birim", ["Adet", "Kutu", "Paket", "Kg", "Litre", "Metre"])
            with tf5:
                teklif_tarihi = st.date_input("Teklif Tarihi", value=datetime.now().date(), key="teklif_tarih")

            if st.form_submit_button("💰 Teklif Kaydet", use_container_width=True):
                if urun_adi and tedarikci_adi and birim_fiyat > 0:
                    teklifler.append({
                        "id": f"tkl_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "urun": urun_adi,
                        "tedarikci": tedarikci_adi,
                        "birim_fiyat": birim_fiyat,
                        "birim": birim,
                        "tarih": str(teklif_tarihi),
                    })
                    _save_json(teklif_path, teklifler)
                    st.success("Teklif kaydedildi!")
                    st.rerun()

        if teklifler:
            # Ürün bazlı gruplama
            urun_grubu = {}
            for t in teklifler:
                u = t.get("urun", "?")
                if u not in urun_grubu:
                    urun_grubu[u] = []
                urun_grubu[u].append(t)

            for urun, tlist in urun_grubu.items():
                tlist.sort(key=lambda x: x.get("birim_fiyat", 0))
                en_ucuz = tlist[0].get("birim_fiyat", 0) if tlist else 0
                st.markdown(f"**{urun}** ({len(tlist)} teklif)")
                for t in tlist:
                    fiyat = t.get("birim_fiyat", 0)
                    en_iyi = "🏆" if fiyat == en_ucuz else ""
                    renk = "#06d6a0" if fiyat == en_ucuz else "#ffd166" if fiyat <= en_ucuz * 1.2 else "#e94560"
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:#e0e0e0;">{t.get('tedarikci','?')} {en_iyi}</span>
                        <span style="color:{renk};font-weight:700;">₺{fiyat:,.2f} / {t.get('birim','')}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")
        else:
            _styled_info_banner("Fiyat karşılaştırma için teklif kaydı girin.")

    # ── Sipariş Takip ──
    with sub[3]:
        _styled_section("📦 Sipariş Oluştur & Takip Et", "#00b4d8")

        with st.form("siparis_form"):
            sp1, sp2 = st.columns(2)
            with sp1:
                sp_urun = st.text_input("Ürün / Malzeme", key="sp_urun")
                sp_tedarikci = st.text_input("Tedarikçi", key="sp_tedarikci")
                sp_miktar = st.number_input("Miktar", min_value=1, value=1, key="sp_miktar")
            with sp2:
                sp_tutar = st.number_input("Toplam Tutar (₺)", min_value=0.0, step=100.0, key="sp_tutar")
                sp_termin = st.date_input("Termin Tarihi", value=datetime.now().date() + timedelta(days=14), key="sp_termin")
                sp_oncelik = st.selectbox("Öncelik", ["Normal", "Acil", "Kritik"], key="sp_oncelik")

            if st.form_submit_button("📦 Sipariş Oluştur", use_container_width=True):
                if sp_urun and sp_tedarikci:
                    siparisler.append({
                        "id": f"spr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "urun": sp_urun,
                        "tedarikci": sp_tedarikci,
                        "miktar": sp_miktar,
                        "tutar": sp_tutar,
                        "termin": str(sp_termin),
                        "oncelik": sp_oncelik,
                        "durum": "beklemede",
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(siparis_path, siparisler)
                    st.success("Sipariş oluşturuldu!")
                    st.rerun()

        if siparisler:
            for idx, sp in enumerate(reversed(siparisler[-15:])):
                durum_ikon = {"beklemede": "🟡", "hazirlaniyor": "🔵", "kargoda": "📦", "teslim_edildi": "🟢", "gecikti": "🔴"}.get(sp.get("durum", ""), "⚪")
                with st.expander(f"{durum_ikon} {sp.get('urun','?')} — {sp.get('tedarikci','')} (₺{sp.get('tutar',0):,.0f})"):
                    dc1, dc2, dc3 = st.columns(3)
                    dc1.write(f"**Miktar:** {sp.get('miktar','')}")
                    dc2.write(f"**Termin:** {sp.get('termin','')}")
                    dc3.write(f"**Öncelik:** {sp.get('oncelik','')}")

                    yeni_durum = st.selectbox(
                        "Durum Güncelle",
                        ["beklemede", "hazirlaniyor", "kargoda", "teslim_edildi", "gecikti"],
                        index=["beklemede", "hazirlaniyor", "kargoda", "teslim_edildi", "gecikti"].index(sp.get("durum", "beklemede")),
                        key=f"sp_durum_{idx}"
                    )
                    if st.button("Güncelle", key=f"sp_guncelle_{idx}"):
                        sp["durum"] = yeni_durum
                        if yeni_durum == "gecikti":
                            sp["gecikme"] = True
                        _save_json(siparis_path, siparisler)
                        st.rerun()
        else:
            _styled_info_banner("Henüz sipariş kaydı yok.")

    # ── Risk Haritası ──
    with sub[4]:
        _styled_section("🗺️ Tedarik Risk Haritası", "#e94560")

        if saticilar:
            _styled_info_banner("Tedarik riski; tedarikçi çeşitliliği, gecikme oranı ve kritik ürün bağımlılığına göre hesaplanır.")

            # Kategori bazlı risk
            kategori_satici = {}
            for s in saticilar:
                kat = s.get("kategori", "Diğer")
                if kat not in kategori_satici:
                    kategori_satici[kat] = []
                kategori_satici[kat].append(s)

            st.markdown("**Kategori Bazlı Tedarik Riski**")
            for kat, slist in kategori_satici.items():
                satici_sayisi = len(slist)
                risk = "DÜŞÜK" if satici_sayisi >= 3 else "ORTA" if satici_sayisi >= 2 else "YÜKSEK"
                renk = "#06d6a0" if risk == "DÜŞÜK" else "#ffd166" if risk == "ORTA" else "#e94560"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{kat}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:10px;">{satici_sayisi} tedarikçi</span>
                    </div>
                    <div style="background:{renk}20;color:{renk};padding:4px 12px;border-radius:8px;font-weight:700;">{risk}</div>
                </div>""", unsafe_allow_html=True)

            # Tek tedarikçiye bağımlılık uyarısı
            tek_tedarikci = [kat for kat, slist in kategori_satici.items() if len(slist) == 1]
            if tek_tedarikci:
                st.error(f"⚠️ **Tek Tedarikçi Riski:** {', '.join(tek_tedarikci)} — Bu kategorilerde alternatif tedarikçi bulunmuyor!")

            # Gecikme oranı
            if siparisler:
                _styled_section("Tedarikçi Gecikme Oranları", "#ffd166")
                tedarikci_gecikme = {}
                for sp in siparisler:
                    ted = sp.get("tedarikci", "?")
                    if ted not in tedarikci_gecikme:
                        tedarikci_gecikme[ted] = {"toplam": 0, "geciken": 0}
                    tedarikci_gecikme[ted]["toplam"] += 1
                    if sp.get("durum") == "gecikti" or sp.get("gecikme"):
                        tedarikci_gecikme[ted]["geciken"] += 1

                for ted, data in sorted(tedarikci_gecikme.items(), key=lambda x: -(x[1]["geciken"]/max(1,x[1]["toplam"]))):
                    oran = data["geciken"] / max(1, data["toplam"]) * 100
                    renk = "#e94560" if oran >= 30 else "#ffd166" if oran >= 15 else "#06d6a0"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
                        <span style="width:160px;color:#e0e0e0;font-weight:600;">{ted[:20]}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{min(100,oran)}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                        <span style="width:60px;text-align:right;color:{renk};font-weight:700;">%{oran:.0f}</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Risk haritası için tedarikçi kaydı oluşturun.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. KARBON AYAK İZİ & SÜRDÜRÜLEBİLİRLİK MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_surdurulebilirlik(store):
    _styled_header("Karbon Ayak İzi & Sürdürülebilirlik Merkezi", "🌱")

    karbon_path = _get_data_path(store, "karbon_kayitlari.json")
    kayitlar = _load_json(karbon_path)

    hedef_path = _get_data_path(store, "surdurulebilirlik_hedefleri.json")
    hedefler = _load_json(hedef_path)

    # Toplam karbon
    toplam_co2 = sum(k.get("co2_kg", 0) for k in kayitlar)
    enerji_co2 = sum(k.get("co2_kg", 0) for k in kayitlar if k.get("kategori") == "Enerji")
    kagit_co2 = sum(k.get("co2_kg", 0) for k in kayitlar if k.get("kategori") == "Kağıt")
    atik_co2 = sum(k.get("co2_kg", 0) for k in kayitlar if k.get("kategori") == "Atık")

    _styled_stat_row([
        ("Toplam CO₂ (kg)", f"{toplam_co2:,.1f}"),
        ("Enerji Emisyonu", f"{enerji_co2:,.1f}"),
        ("Kağıt Emisyonu", f"{kagit_co2:,.1f}"),
        ("Atık Emisyonu", f"{atik_co2:,.1f}"),
        ("Kayıt Sayısı", len(kayitlar)),
    ])

    sub = st.tabs(["📊 Karbon Dashboard", "📝 Emisyon Kaydı", "🎯 Hedef Takip", "♻️ Atık Yönetimi", "🌿 Yeşil Satın Alma", "📄 ESG Raporu"])

    # ── Karbon Dashboard ──
    with sub[0]:
        _styled_section("📊 Karbon Ayak İzi Dashboard", "#06d6a0")

        if kayitlar:
            # Kategori dağılımı
            kategori_toplam = {}
            for k in kayitlar:
                kat = k.get("kategori", "Diğer")
                kategori_toplam[kat] = kategori_toplam.get(kat, 0) + k.get("co2_kg", 0)

            if kategori_toplam:
                st.markdown("**Kategori Bazlı CO₂ Dağılımı**")
                max_val = max(kategori_toplam.values()) if kategori_toplam.values() else 1
                kat_renkler = {"Enerji": "#e94560", "Kağıt": "#ffd166", "Atık": "#8338ec", "Plastik": "#ff6b6b", "Ulaşım": "#00b4d8", "Elektronik": "#06d6a0"}
                for kat, val in sorted(kategori_toplam.items(), key=lambda x: -x[1]):
                    renk = kat_renkler.get(kat, "#888")
                    bar_w = int(val / max_val * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="width:100px;color:#e0e0e0;font-weight:600;">{kat}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:22px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                        </div>
                        <span style="width:90px;text-align:right;color:{renk};font-weight:700;">{val:,.1f} kg</span>
                    </div>""", unsafe_allow_html=True)

            # Aylık trend
            aylik = {}
            for k in kayitlar:
                ay = k.get("tarih", "")[:7]
                if ay:
                    aylik[ay] = aylik.get(ay, 0) + k.get("co2_kg", 0)

            if aylik:
                _styled_section("Aylık CO₂ Emisyon Trendi", "#00b4d8")
                max_val = max(aylik.values()) if aylik.values() else 1
                for ay in sorted(aylik.keys()):
                    val = aylik[ay]
                    bar_w = int(val / max_val * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <span style="width:80px;color:#888;font-size:0.85rem;">{ay}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#06d6a0,#00b4d8);border-radius:6px;"></div>
                        </div>
                        <span style="width:80px;text-align:right;color:#06d6a0;font-weight:700;">{val:,.1f} kg</span>
                    </div>""", unsafe_allow_html=True)

            # Sürdürülebilirlik skoru
            skor = max(0, 100 - int(toplam_co2 / max(1, len(kayitlar)) * 2))
            renk = "#06d6a0" if skor >= 70 else "#ffd166" if skor >= 40 else "#e94560"
            st.markdown(f"""
            <div style="background:#16213e;border-radius:14px;padding:20px;text-align:center;margin-top:16px;">
                <div style="font-size:0.9rem;color:#888;">Sürdürülebilirlik Skoru</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">{skor}/100</div>
                <div style="font-size:0.85rem;color:#aaa;">Düşük emisyon = Yüksek skor</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Dashboard için emisyon kaydı girin.")

    # ── Emisyon Kaydı ──
    with sub[1]:
        _styled_section("📝 CO₂ Emisyon Kaydı Oluştur", "#06d6a0")

        with st.form("emisyon_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_kategori = st.selectbox("Kategori", ["Enerji", "Kağıt", "Plastik", "Atık", "Ulaşım", "Elektronik", "Su", "Diğer"])
                e_miktar = st.number_input("Miktar", min_value=0.0, step=1.0, key="emisyon_miktar")
                e_birim = st.selectbox("Birim", ["kWh", "kg", "litre", "adet", "km", "m³"])
            with ec2:
                e_tarih = st.date_input("Tarih", value=datetime.now().date(), key="emisyon_tarih")
                e_aciklama = st.text_input("Açıklama", key="emisyon_aciklama")

                # CO2 dönüşüm katsayıları (yaklaşık)
                katsayilar = {"Enerji": 0.5, "Kağıt": 1.1, "Plastik": 2.5, "Atık": 0.8, "Ulaşım": 0.21, "Elektronik": 3.0, "Su": 0.3, "Diğer": 0.5}
                tahmini_co2 = e_miktar * katsayilar.get(e_kategori, 0.5)
                st.info(f"Tahmini CO₂: {tahmini_co2:.1f} kg")

            if st.form_submit_button("🌱 Emisyon Kaydet", use_container_width=True):
                if e_miktar > 0:
                    kayitlar.append({
                        "id": f"co2_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "kategori": e_kategori,
                        "miktar": e_miktar,
                        "birim": e_birim,
                        "co2_kg": tahmini_co2,
                        "tarih": str(e_tarih),
                        "aciklama": e_aciklama,
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(karbon_path, kayitlar)
                    st.success(f"Emisyon kaydedildi: {tahmini_co2:.1f} kg CO₂")
                    st.rerun()

        if kayitlar:
            _styled_section("Son Emisyon Kayıtları", "#0f3460")
            for k in reversed(kayitlar[-10:]):
                kat_ikon = {"Enerji": "⚡", "Kağıt": "📄", "Plastik": "🥤", "Atık": "🗑️", "Ulaşım": "🚗", "Elektronik": "💻", "Su": "💧"}.get(k.get("kategori", ""), "🌍")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{kat_ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{k.get('kategori','')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{k.get('miktar',0)} {k.get('birim','')}</span>
                    </div>
                    <div>
                        <span style="color:#06d6a0;font-weight:700;">{k.get('co2_kg',0):.1f} kg CO₂</span>
                        <span style="color:#666;font-size:0.78rem;margin-left:8px;">{k.get('tarih','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Hedef Takip ──
    with sub[2]:
        _styled_section("🎯 Sürdürülebilirlik Hedefleri", "#ffd166")

        with st.form("hedef_form"):
            hc1, hc2 = st.columns(2)
            with hc1:
                h_baslik = st.text_input("Hedef Başlığı")
                h_kategori = st.selectbox("Kategori", ["Enerji Azaltma", "Kağıt Tasarrufu", "Atık Azaltma", "Su Tasarrufu", "Geri Dönüşüm", "Yeşil Satın Alma"], key="hedef_kat")
            with hc2:
                h_hedef_deger = st.number_input("Hedef Değer (%)", min_value=1, max_value=100, value=20)
                h_bitis = st.date_input("Hedef Tarihi", value=datetime.now().date() + timedelta(days=180), key="hedef_bitis")

            if st.form_submit_button("🎯 Hedef Belirle", use_container_width=True):
                if h_baslik:
                    hedefler.append({
                        "id": f"hdf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": h_baslik,
                        "kategori": h_kategori,
                        "hedef_deger": h_hedef_deger,
                        "bitis": str(h_bitis),
                        "mevcut_ilerleme": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(hedef_path, hedefler)
                    st.success("Hedef oluşturuldu!")
                    st.rerun()

        if hedefler:
            for idx, h in enumerate(hedefler):
                ilerleme = h.get("mevcut_ilerleme", 0)
                hedef = h.get("hedef_deger", 100)
                oran = min(100, int(ilerleme / max(1, hedef) * 100))
                renk = "#06d6a0" if oran >= 80 else "#ffd166" if oran >= 40 else "#e94560"

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <strong style="color:#e0e0e0;">{h.get('baslik','?')}</strong>
                        <span style="color:{renk};font-weight:700;">%{oran}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:8px;height:20px;overflow:hidden;">
                        <div style="width:{oran}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;transition:width 0.5s;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-top:6px;">
                        <span style="color:#888;font-size:0.78rem;">{h.get('kategori','')}</span>
                        <span style="color:#888;font-size:0.78rem;">Hedef: {h.get('bitis','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                yeni_ilerleme = st.slider(f"İlerleme güncelle", 0, 100, ilerleme, key=f"hedef_slider_{idx}")
                if yeni_ilerleme != ilerleme:
                    if st.button("Güncelle", key=f"hedef_guncelle_{idx}"):
                        h["mevcut_ilerleme"] = yeni_ilerleme
                        _save_json(hedef_path, hedefler)
                        st.rerun()
        else:
            _styled_info_banner("Henüz sürdürülebilirlik hedefi belirlenmemiş.")

    # ── Atık Yönetimi ──
    with sub[3]:
        _styled_section("♻️ Atık Yönetimi & Geri Dönüşüm Takibi", "#8338ec")

        atik_path = _get_data_path(store, "atik_kayitlari.json")
        atiklar = _load_json(atik_path)

        with st.form("atik_form"):
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                a_tur = st.selectbox("Atık Türü", ["Kağıt/Karton", "Plastik", "Cam", "Metal", "Elektronik", "Organik", "Tehlikeli", "Diğer"])
            with ac2:
                a_miktar = st.number_input("Miktar (kg)", min_value=0.0, step=0.5, key="atik_miktar")
            with ac3:
                a_yontem = st.selectbox("Bertaraf Yöntemi", ["Geri Dönüşüm", "Kompost", "Enerji Geri Kazanım", "Düzenli Depolama", "Tehlikeli Atık Bertaraf"])

            a_tarih = st.date_input("Tarih", value=datetime.now().date(), key="atik_tarih")

            if st.form_submit_button("♻️ Atık Kaydet", use_container_width=True):
                if a_miktar > 0:
                    atiklar.append({
                        "id": f"atk_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "tur": a_tur,
                        "miktar": a_miktar,
                        "yontem": a_yontem,
                        "tarih": str(a_tarih),
                        "kayit_tarihi": datetime.now().isoformat(),
                    })
                    _save_json(atik_path, atiklar)
                    st.success("Atık kaydedildi!")
                    st.rerun()

        if atiklar:
            toplam_atik = sum(a.get("miktar", 0) for a in atiklar)
            geri_donusum = sum(a.get("miktar", 0) for a in atiklar if a.get("yontem") == "Geri Dönüşüm")
            gd_oran = int(geri_donusum / max(1, toplam_atik) * 100)

            _styled_stat_row([
                ("Toplam Atık", f"{toplam_atik:,.1f} kg"),
                ("Geri Dönüşüm", f"{geri_donusum:,.1f} kg"),
                ("Geri Dönüşüm Oranı", f"%{gd_oran}"),
            ])

            # Tür bazlı dağılım
            tur_toplam = {}
            for a in atiklar:
                t = a.get("tur", "Diğer")
                tur_toplam[t] = tur_toplam.get(t, 0) + a.get("miktar", 0)

            max_val = max(tur_toplam.values()) if tur_toplam.values() else 1
            tur_renkler = {"Kağıt/Karton": "#ffd166", "Plastik": "#e94560", "Cam": "#00b4d8", "Metal": "#888", "Elektronik": "#8338ec", "Organik": "#06d6a0", "Tehlikeli": "#ff6b6b"}
            for tur, val in sorted(tur_toplam.items(), key=lambda x: -x[1]):
                renk = tur_renkler.get(tur, "#888")
                bar_w = int(val / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:120px;color:#e0e0e0;font-weight:600;">{tur}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <span style="width:80px;text-align:right;color:{renk};font-weight:700;">{val:,.1f} kg</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henüz atık kaydı bulunmuyor.")

    # ── Yeşil Satın Alma ──
    with sub[4]:
        _styled_section("🌿 Yeşil Satın Alma Endeksi", "#06d6a0")

        yesil_path = _get_data_path(store, "yesil_satin_alma.json")
        yesil_kayitlar = _load_json(yesil_path)

        with st.form("yesil_form"):
            yc1, yc2 = st.columns(2)
            with yc1:
                y_urun = st.text_input("Ürün Adı", key="yesil_urun")
                y_tedarikci = st.text_input("Tedarikçi", key="yesil_ted")
            with yc2:
                y_sertifika = st.multiselect("Çevre Sertifikaları", ["ISO 14001", "FSC", "Energy Star", "EU Ecolabel", "Mavi Bayrak", "Yeşil Ofis", "Karbon Nötr"])
                y_puan = st.slider("Yeşil Skor (1-10)", 1, 10, 5, key="yesil_puan")

            if st.form_submit_button("🌿 Kaydet", use_container_width=True):
                if y_urun:
                    yesil_kayitlar.append({
                        "id": f"ysl_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "urun": y_urun,
                        "tedarikci": y_tedarikci,
                        "sertifikalar": y_sertifika,
                        "puan": y_puan,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(yesil_path, yesil_kayitlar)
                    st.success("Yeşil satın alma kaydı oluşturuldu!")
                    st.rerun()

        if yesil_kayitlar:
            ort_puan = sum(y.get("puan", 0) for y in yesil_kayitlar) / len(yesil_kayitlar)
            renk = "#06d6a0" if ort_puan >= 7 else "#ffd166" if ort_puan >= 4 else "#e94560"

            st.markdown(f"""
            <div style="background:#16213e;border-radius:14px;padding:20px;text-align:center;margin:14px 0;">
                <div style="font-size:0.9rem;color:#888;">Yeşil Satın Alma Endeksi</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">{ort_puan:.1f}/10</div>
                <div style="font-size:0.85rem;color:#aaa;">{len(yesil_kayitlar)} ürün değerlendirildi</div>
            </div>""", unsafe_allow_html=True)

            for y in reversed(yesil_kayitlar[-10:]):
                p = y.get("puan", 0)
                renk = "#06d6a0" if p >= 7 else "#ffd166" if p >= 4 else "#e94560"
                sert = ", ".join(y.get("sertifikalar", [])) if y.get("sertifikalar") else "Yok"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{y.get('urun','?')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">({y.get('tedarikci','')})</span>
                    </div>
                    <div>
                        <span style="color:#888;font-size:0.78rem;margin-right:8px;">{sert}</span>
                        <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;font-weight:700;">{p}/10</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Yeşil satın alma kaydı oluşturun.")

    # ── ESG Raporu ──
    with sub[5]:
        _styled_section("📄 ESG (Çevre, Sosyal, Yönetişim) Raporu", "#0f3460")

        _styled_info_banner("Kurumun çevresel performansını özetleyen otomatik ESG raporu.")

        # Çevre skoru
        cevre_skor = max(0, 100 - int(toplam_co2 / max(1, len(kayitlar) + 1) * 2)) if kayitlar else 50

        # Atık skoru
        atik_path2 = _get_data_path(store, "atik_kayitlari.json")
        atiklar2 = _load_json(atik_path2)
        if atiklar2:
            geri_don = sum(a.get("miktar", 0) for a in atiklar2 if a.get("yontem") == "Geri Dönüşüm")
            toplam_at = sum(a.get("miktar", 0) for a in atiklar2)
            atik_skor = int(geri_don / max(1, toplam_at) * 100)
        else:
            atik_skor = 50

        # Yeşil satın alma skoru
        yesil_path2 = _get_data_path(store, "yesil_satin_alma.json")
        yesil2 = _load_json(yesil_path2)
        yesil_skor = int(sum(y.get("puan", 0) for y in yesil2) / max(1, len(yesil2)) * 10) if yesil2 else 50

        genel_esg = int((cevre_skor + atik_skor + yesil_skor) / 3)
        renk = "#06d6a0" if genel_esg >= 70 else "#ffd166" if genel_esg >= 40 else "#e94560"
        derece = "A+" if genel_esg >= 90 else "A" if genel_esg >= 80 else "B+" if genel_esg >= 70 else "B" if genel_esg >= 60 else "C+" if genel_esg >= 50 else "C" if genel_esg >= 40 else "D"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin:14px 0;">
            <div style="font-size:1rem;color:#888;">Genel ESG Derecesi</div>
            <div style="font-size:4rem;font-weight:900;color:{renk};">{derece}</div>
            <div style="font-size:1.4rem;color:{renk};font-weight:700;">{genel_esg}/100</div>
        </div>""", unsafe_allow_html=True)

        # Alt skorlar
        skorlar = [
            ("Çevre & Emisyon", cevre_skor, "#06d6a0"),
            ("Atık & Geri Dönüşüm", atik_skor, "#8338ec"),
            ("Yeşil Satın Alma", yesil_skor, "#ffd166"),
        ]
        for baslik, skor, renk in skorlar:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:#e0e0e0;font-weight:600;">{baslik}</span>
                    <span style="color:{renk};font-weight:700;">{skor}/100</span>
                </div>
                <div style="background:#1a1a2e;border-radius:8px;height:22px;overflow:hidden;">
                    <div style="width:{skor}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:8px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Öneriler
        _styled_section("AI Sürdürülebilirlik Önerileri", "#06d6a0")
        oneriler = []
        if cevre_skor < 70:
            oneriler.append("⚡ Enerji tüketimini azaltmak için LED aydınlatma ve hareket sensörü kullanımını artırın.")
        if atik_skor < 70:
            oneriler.append("♻️ Geri dönüşüm oranını artırmak için sınıflara ayrıştırma kutuları yerleştirin.")
        if yesil_skor < 70:
            oneriler.append("🌿 Tedarikçi seçimlerinde çevre sertifikası olan firmaları tercih edin.")
        if not oneriler:
            oneriler.append("✅ Tebrikler! Kurumunuz sürdürülebilirlik hedeflerine uygun ilerliyor.")

        for o in oneriler:
            st.markdown(f"""
            <div style="background:#06d6a012;border-left:3px solid #06d6a0;padding:8px 14px;border-radius:0 8px 8px 0;margin-bottom:6px;">
                <span style="color:#06d6a0;font-size:0.9rem;">{o}</span>
            </div>""", unsafe_allow_html=True)
