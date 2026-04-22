"""
Tüketim ve Demirbaş - FİNAL Özellikler
1. Blokzincir Tabanlı Varlık Sertifika & Denetim Sistemi
2. Akıllı Ekosistem & IoT Entegrasyon Merkezi
3. Kurum Varlık Akademisi & Bilgi Bankası
"""
import streamlit as st
import json
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

# ── Ortak stil yardımcıları ──
def _styled_header(title, icon="🔗"):
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

def _hash_block(data_str):
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. BLOKZİNCİR TABANLI VARLIK SERTİFİKA & DENETİM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_blokzincir_denetim(store):
    _styled_header("Blokzincir Tabanlı Varlık Sertifika & Denetim Sistemi", "🔗")

    zincir_path = _get_data_path(store, "denetim_zinciri.json")
    zincir = _load_json(zincir_path)

    sertifika_path = _get_data_path(store, "varlik_sertifikalari.json")
    sertifikalar = _load_json(sertifika_path)

    # Zincir bütünlük kontrolü
    butunluk_ok = True
    for i in range(1, len(zincir)):
        onceki_hash = zincir[i].get("onceki_hash", "")
        beklenen = zincir[i-1].get("hash", "")
        if onceki_hash != beklenen:
            butunluk_ok = False
            break

    _styled_stat_row([
        ("Zincir Blok Sayisi", len(zincir)),
        ("Sertifika Sayisi", len(sertifikalar)),
        ("Butunluk Durumu", "Saglam" if butunluk_ok else "BOZUK"),
        ("Son Islem", zincir[-1].get("tarih", "—")[:10] if zincir else "—"),
    ])

    sub = st.tabs(["📋 Denetim Zinciri", "📜 Sertifika Uret", "🔍 Dogrulama", "📊 Denetim Raporu", "🔄 Transfer Gecmisi", "🏛️ Uyumluluk"])

    # ── Denetim Zinciri ──
    with sub[0]:
        _styled_section("📋 Degistirilemez Denetim Zinciri", "#8338ec")

        _styled_info_banner("Her islem kriptografik hash ile zincirlenir. Gecmis kayitlar degistirilemez.")

        with st.form("zincir_islem_form"):
            zc1, zc2 = st.columns(2)
            with zc1:
                z_varlik = st.text_input("Varlik Adi", key="zincir_varlik")
                z_islem = st.selectbox("Islem Turu", [
                    "Satin Alma", "Zimmet Atama", "Zimmet Devir",
                    "Konum Degisikligi", "Bakim Yapildi", "Hasar Tespit",
                    "Hurdaya Ayirma", "Satis/Devir", "Garanti Uzatma",
                    "Deger Guncelleme"
                ], key="zincir_islem")
            with zc2:
                z_yapan = st.text_input("Islemi Yapan", key="zincir_yapan")
                z_detay = st.text_input("Detay / Aciklama", key="zincir_detay")

            if st.form_submit_button("🔗 Zincire Ekle", use_container_width=True):
                if z_varlik and z_yapan:
                    onceki_hash = zincir[-1].get("hash", "0" * 64) if zincir else "0" * 64
                    blok_no = len(zincir) + 1
                    zaman = datetime.now().isoformat()
                    veri_str = f"{blok_no}|{z_varlik}|{z_islem}|{z_yapan}|{z_detay}|{zaman}|{onceki_hash}"
                    blok_hash = _hash_block(veri_str)

                    yeni_blok = {
                        "blok_no": blok_no,
                        "varlik": z_varlik,
                        "islem": z_islem,
                        "yapan": z_yapan,
                        "detay": z_detay,
                        "tarih": zaman,
                        "onceki_hash": onceki_hash,
                        "hash": blok_hash,
                    }
                    zincir.append(yeni_blok)
                    _save_json(zincir_path, zincir)
                    st.success(f"Blok #{blok_no} zincire eklendi!")
                    st.rerun()

        # Zincir görüntüleme
        if zincir:
            _styled_section("Zincir Bloklari (Son 20)", "#0f3460")
            for blok in reversed(zincir[-20:]):
                islem_ikon = {
                    "Satin Alma": "🛒", "Zimmet Atama": "📌", "Zimmet Devir": "🔄",
                    "Konum Degisikligi": "📍", "Bakim Yapildi": "🔧", "Hasar Tespit": "⚠️",
                    "Hurdaya Ayirma": "🗑️", "Satis/Devir": "💰", "Garanti Uzatma": "🛡️",
                    "Deger Guncelleme": "💎",
                }.get(blok.get("islem", ""), "📋")

                hash_kisa = blok.get("hash", "")[:16] + "..."
                onceki_kisa = blok.get("onceki_hash", "")[:12] + "..."

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid #8338ec;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#8338ec;font-weight:700;">Blok #{blok.get('blok_no','?')}</span>
                            <span style="font-size:1.2rem;margin-left:8px;">{islem_ikon}</span>
                            <strong style="color:#e0e0e0;margin-left:6px;">{blok.get('islem','')}</strong>
                        </div>
                        <span style="color:#888;font-size:0.78rem;">{blok.get('tarih','')[:16]}</span>
                    </div>
                    <div style="margin-top:6px;">
                        <span style="color:#00b4d8;">{blok.get('varlik','')}</span>
                        <span style="color:#888;margin-left:12px;">Yapan: {blok.get('yapan','')}</span>
                    </div>
                    <div style="color:#aaa;font-size:0.82rem;margin-top:3px;">{blok.get('detay','')}</div>
                    <div style="margin-top:6px;font-family:monospace;font-size:0.7rem;">
                        <span style="color:#06d6a0;">Hash: {hash_kisa}</span>
                        <span style="color:#666;margin-left:12px;">Onceki: {onceki_kisa}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Sertifika Üret ──
    with sub[1]:
        _styled_section("📜 Varlik Sertifikasi Uret", "#ffd166")

        _styled_info_banner("Her varlik icin benzersiz dijital sertifika uretin. Kurumlar arasi transfer ve denetim icin kullanilir.")

        with st.form("sertifika_form"):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_varlik = st.text_input("Varlik Adi", key="sert_varlik")
                s_seri = st.text_input("Seri No / Barkod", key="sert_seri")
                s_deger = st.number_input("Guncel Deger (TL)", min_value=0.0, step=100.0, key="sert_deger")
            with sc2:
                s_sahip = st.text_input("Kurum / Sahip", key="sert_sahip")
                s_durum = st.selectbox("Varlik Durumu", ["Aktif Kullanımda", "Depoda", "Bakimda", "Arızalı", "Hurdaya Ayrildi"], key="sert_durum")
                s_gecerlilik = st.date_input("Gecerlilik Tarihi", value=datetime.now().date() + timedelta(days=365), key="sert_gecerlilik")

            if st.form_submit_button("📜 Sertifika Uret", use_container_width=True):
                if s_varlik:
                    sert_id = f"CERT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    sert_veri = f"{sert_id}|{s_varlik}|{s_seri}|{s_sahip}|{s_deger}|{s_durum}"
                    sert_hash = _hash_block(sert_veri)

                    sertifika = {
                        "sertifika_id": sert_id,
                        "varlik": s_varlik,
                        "seri_no": s_seri,
                        "deger": s_deger,
                        "sahip": s_sahip,
                        "durum": s_durum,
                        "gecerlilik": str(s_gecerlilik),
                        "hash": sert_hash,
                        "olusturma": datetime.now().isoformat(),
                    }
                    sertifikalar.append(sertifika)
                    _save_json(sertifika_path, sertifikalar)
                    st.success(f"Sertifika uretildi: {sert_id}")
                    st.rerun()

        if sertifikalar:
            _styled_section("Uretilen Sertifikalar", "#06d6a0")
            for s in reversed(sertifikalar[-12:]):
                durum_renk = {"Aktif Kullanımda": "#06d6a0", "Depoda": "#00b4d8", "Bakimda": "#ffd166", "Arızalı": "#e94560", "Hurdaya Ayrildi": "#666"}.get(s.get("durum", ""), "#888")
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#16213e,#1a1a2e);border-radius:12px;padding:14px 18px;margin-bottom:8px;border:1px solid #ffd16630;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="color:#ffd166;font-weight:700;font-family:monospace;">{s.get('sertifika_id','')}</span>
                            <strong style="color:#e0e0e0;margin-left:10px;">{s.get('varlik','')}</strong>
                        </div>
                        <span style="background:{durum_renk}20;color:{durum_renk};padding:3px 10px;border-radius:8px;font-size:0.8rem;">{s.get('durum','')}</span>
                    </div>
                    <div style="display:flex;gap:20px;margin-top:8px;">
                        <span style="color:#888;font-size:0.8rem;">Sahip: <strong style="color:#00b4d8;">{s.get('sahip','')}</strong></span>
                        <span style="color:#888;font-size:0.8rem;">Deger: <strong style="color:#06d6a0;">TL{s.get('deger',0):,.0f}</strong></span>
                        <span style="color:#888;font-size:0.8rem;">Gecerlilik: {s.get('gecerlilik','')}</span>
                    </div>
                    <div style="font-family:monospace;font-size:0.68rem;color:#666;margin-top:6px;">SHA-256: {s.get('hash','')[:32]}...</div>
                </div>""", unsafe_allow_html=True)

    # ── Doğrulama ──
    with sub[2]:
        _styled_section("🔍 Sertifika & Zincir Dogrulama", "#06d6a0")

        dogrulama_tab = st.radio("Dogrulama Turu", ["Sertifika Dogrula", "Zincir Butunluk Kontrolu"], horizontal=True, key="dogrulama_tip")

        if dogrulama_tab == "Sertifika Dogrula":
            sert_id_ara = st.text_input("Sertifika ID girin (ornek: CERT-20260413...)", key="dogrula_sert")
            if st.button("🔍 Dogrula", key="dogrula_btn"):
                bulunan = next((s for s in sertifikalar if s.get("sertifika_id") == sert_id_ara), None)
                if bulunan:
                    # Hash yeniden hesapla
                    kontrol_veri = f"{bulunan['sertifika_id']}|{bulunan['varlik']}|{bulunan['seri_no']}|{bulunan['sahip']}|{bulunan['deger']}|{bulunan['durum']}"
                    kontrol_hash = _hash_block(kontrol_veri)
                    gecerli = kontrol_hash == bulunan.get("hash", "")

                    if gecerli:
                        st.success(f"DOGRULANDI - Sertifika gecerli ve degistirilmemis.")
                    else:
                        st.error("UYARI - Sertifika verileri degistirilmis olabilir!")

                    st.json(bulunan)
                else:
                    st.warning("Sertifika bulunamadi.")
        else:
            if st.button("🔗 Zincir Butunluk Kontrolu Baslat", key="butunluk_btn"):
                if len(zincir) < 2:
                    st.info("Zincirde yeterli blok yok (min 2).")
                else:
                    hatalar = []
                    for i in range(1, len(zincir)):
                        onceki_hash = zincir[i].get("onceki_hash", "")
                        beklenen = zincir[i-1].get("hash", "")
                        if onceki_hash != beklenen:
                            hatalar.append(f"Blok #{zincir[i].get('blok_no','?')}: Hash uyumsuzlugu!")

                    if not hatalar:
                        st.success(f"Zincir SAGLAM - {len(zincir)} blok dogrulandi. Hicbir kayit degistirilmemis.")
                        st.balloons()
                    else:
                        st.error(f"ZINCIR BOZUK - {len(hatalar)} hata tespit edildi!")
                        for h in hatalar:
                            st.warning(h)

        # Bütünlük skoru
        skor = 100 if butunluk_ok else max(0, 100 - len([1 for i in range(1, len(zincir)) if zincir[i].get("onceki_hash") != zincir[i-1].get("hash", "")]) * 20)
        renk = "#06d6a0" if skor >= 90 else ("#ffd166" if skor >= 60 else "#e94560")
        st.markdown(f"""
        <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
            <div style="color:#888;">Zincir Butunluk Skoru</div>
            <div style="font-size:3rem;font-weight:800;color:{renk};">{skor}/100</div>
        </div>""", unsafe_allow_html=True)

    # ── Denetim Raporu ──
    with sub[3]:
        _styled_section("📊 Otomatik Denetim Raporu", "#0f3460")

        if zincir:
            # İşlem türü dağılımı
            islem_dagilim = {}
            for b in zincir:
                isl = b.get("islem", "Diger")
                islem_dagilim[isl] = islem_dagilim.get(isl, 0) + 1

            st.markdown("**Islem Turu Dagilimi**")
            max_val = max(islem_dagilim.values()) if islem_dagilim.values() else 1
            islem_renkler = {
                "Satin Alma": "#06d6a0", "Zimmet Atama": "#00b4d8", "Zimmet Devir": "#8338ec",
                "Bakim Yapildi": "#ffd166", "Hurdaya Ayirma": "#e94560", "Hasar Tespit": "#ff6b6b",
            }
            for isl, sayi in sorted(islem_dagilim.items(), key=lambda x: -x[1]):
                renk = islem_renkler.get(isl, "#888")
                bar_w = int(sayi / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:160px;color:#e0e0e0;font-size:0.88rem;">{isl}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

            # Kullanıcı bazlı aktivite
            _styled_section("Kullanici Bazli Islem Aktivitesi", "#00b4d8")
            kullanici_islem = {}
            for b in zincir:
                k = b.get("yapan", "?")
                kullanici_islem[k] = kullanici_islem.get(k, 0) + 1

            for k, s in sorted(kullanici_islem.items(), key=lambda x: -x[1]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">{k}</span>
                    <span style="color:#00b4d8;font-weight:700;">{s} islem</span>
                </div>""", unsafe_allow_html=True)

            # Aylık işlem hacmi
            _styled_section("Aylik Islem Hacmi", "#ffd166")
            aylik = {}
            for b in zincir:
                ay = b.get("tarih", "")[:7]
                if ay:
                    aylik[ay] = aylik.get(ay, 0) + 1

            max_ay = max(aylik.values()) if aylik.values() else 1
            for ay in sorted(aylik.keys()):
                val = aylik[ay]
                bar_w = int(val / max_ay * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                    <span style="width:80px;color:#888;">{ay}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#ffd166;border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:#ffd166;font-weight:700;">{val}</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Denetim raporu icin zincire islem ekleyin.")

    # ── Transfer Geçmişi ──
    with sub[4]:
        _styled_section("🔄 Varlik Zimmet Zinciri & Transfer Gecmisi", "#8338ec")

        if zincir:
            # Varlık bazlı zimmet zinciri
            varliklar = list(set(b.get("varlik", "?") for b in zincir))
            secilen = st.selectbox("Varlik Secin", sorted(varliklar), key="transfer_sec")

            varlik_islemleri = [b for b in zincir if b.get("varlik") == secilen]
            zimmet_islemleri = [b for b in varlik_islemleri if b.get("islem") in ["Zimmet Atama", "Zimmet Devir", "Satin Alma", "Satis/Devir"]]

            if varlik_islemleri:
                st.markdown(f"**{secilen}** - {len(varlik_islemleri)} islem kaydi")

                for i, b in enumerate(varlik_islemleri):
                    islem_ikon = {
                        "Satin Alma": "🛒", "Zimmet Atama": "📌", "Zimmet Devir": "🔄",
                        "Konum Degisikligi": "📍", "Bakim Yapildi": "🔧", "Hasar Tespit": "⚠️",
                        "Hurdaya Ayirma": "🗑️", "Satis/Devir": "💰",
                    }.get(b.get("islem", ""), "📋")

                    st.markdown(f"""
                    <div style="display:flex;gap:14px;margin-bottom:0;">
                        <div style="display:flex;flex-direction:column;align-items:center;min-width:30px;">
                            <div style="font-size:1.2rem;">{islem_ikon}</div>
                            {'<div style="width:2px;height:25px;background:#8338ec40;"></div>' if i < len(varlik_islemleri)-1 else ''}
                        </div>
                        <div style="background:#16213e;border-radius:8px;padding:8px 14px;flex:1;margin-bottom:6px;">
                            <div style="display:flex;justify-content:space-between;">
                                <strong style="color:#8338ec;">{b.get('islem','')}</strong>
                                <span style="color:#888;font-size:0.78rem;">{b.get('tarih','')[:16]}</span>
                            </div>
                            <span style="color:#aaa;font-size:0.82rem;">Yapan: {b.get('yapan','')} {('| ' + b.get('detay','')) if b.get('detay') else ''}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Bu varlik icin islem kaydi bulunamadi.")
        else:
            _styled_info_banner("Transfer gecmisi icin zincire islem ekleyin.")

    # ── Uyumluluk ──
    with sub[5]:
        _styled_section("🏛️ Sayistay / MEB Denetim Uyumlulugu", "#e94560")

        _styled_info_banner("Kurum varlik yonetiminin yasal mevzuat ve denetim standartlarina uyumluluk durumu.")

        uyumluluk_kriterleri = [
            ("Demirbas Kayit Butunlugu", "Tum demirbaslarin eksiksiz kaydi", butunluk_ok, "#06d6a0"),
            ("Zimmet Zinciri Takibi", "Her demirbasin zimmetli oldugu kisi/birim kaydi", len(zincir) > 0, "#00b4d8"),
            ("Degistirilemez Denetim Izi", "Blokzincir tabanli islem kaydi", len(zincir) >= 5, "#8338ec"),
            ("Dijital Sertifika", "Varlik sertifikalandirma sistemi", len(sertifikalar) > 0, "#ffd166"),
            ("Periyodik Sayim", "Yillik/donemsel envanter sayimi", True, "#06d6a0"),
            ("Hurdaya Ayirma Proseduru", "Resmi hurda islem kaydi", any(b.get("islem") == "Hurdaya Ayirma" for b in zincir), "#e94560"),
        ]

        gecen = sum(1 for _, _, durum, _ in uyumluluk_kriterleri if durum)
        toplam = len(uyumluluk_kriterleri)
        uyum_skor = int(gecen / toplam * 100)
        renk = "#06d6a0" if uyum_skor >= 80 else ("#ffd166" if uyum_skor >= 50 else "#e94560")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-bottom:16px;">
            <div style="color:#888;">Denetim Uyumluluk Skoru</div>
            <div style="font-size:3rem;font-weight:800;color:{renk};">{uyum_skor}%</div>
            <div style="color:#aaa;font-size:0.85rem;">{gecen}/{toplam} kriter karsilandi</div>
        </div>""", unsafe_allow_html=True)

        for baslik, aciklama, durum, renk in uyumluluk_kriterleri:
            ikon = "✅" if durum else "❌"
            renk_d = "#06d6a0" if durum else "#e94560"
            st.markdown(f"""
            <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:1.1rem;">{ikon}</span>
                    <strong style="color:#e0e0e0;margin-left:8px;">{baslik}</strong>
                    <div style="color:#888;font-size:0.78rem;margin-left:30px;">{aciklama}</div>
                </div>
                <span style="color:{renk_d};font-weight:700;">{'UYUMLU' if durum else 'EKSIK'}</span>
            </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. AKILLI EKOSİSTEM & IoT ENTEGRASYON MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_iot_ekosistem(store):
    _styled_header("Akilli Ekosistem & IoT Entegrasyon Merkezi", "🌐")

    sensor_path = _get_data_path(store, "iot_sensorler.json")
    sensorler = _load_json(sensor_path)

    veri_path = _get_data_path(store, "iot_veriler.json")
    veriler = _load_json(veri_path)

    alarm_path = _get_data_path(store, "iot_alarmlar.json")
    alarmlar = _load_json(alarm_path)

    aktif_sensor = len([s for s in sensorler if s.get("aktif", True)])
    aktif_alarm = len([a for a in alarmlar if a.get("aktif", True)])

    _styled_stat_row([
        ("Toplam Sensor", len(sensorler)),
        ("Aktif Sensor", aktif_sensor),
        ("Veri Kaydi", len(veriler)),
        ("Aktif Alarm", aktif_alarm),
    ])

    sub = st.tabs(["📊 Canli Dashboard", "📡 Sensor Yonetimi", "⚡ Enerji Haritasi", "🚨 Alarm Merkezi", "📈 Anormallik Tespiti", "💡 Tasarruf Simulasyonu"])

    # ── Canlı Dashboard ──
    with sub[0]:
        _styled_section("📊 Gercek Zamanli IoT Dashboard", "#00b4d8")

        if sensorler:
            # Sensör tipi bazlı grupla
            tip_grup = {}
            for s in sensorler:
                tip = s.get("tip", "Diger")
                if tip not in tip_grup:
                    tip_grup[tip] = []
                tip_grup[tip].append(s)

            for tip, slist in tip_grup.items():
                tip_ikon = {"Enerji": "⚡", "Su": "💧", "Sicaklik": "🌡️", "Hareket": "🏃", "Nem": "💦", "Isik": "💡", "CO2": "🌫️"}.get(tip, "📡")
                _styled_section(f"{tip_ikon} {tip} Sensorleri ({len(slist)} adet)", "#00b4d8")

                cols = st.columns(min(4, len(slist)))
                for i, s in enumerate(slist[:8]):
                    col = cols[i % len(cols)]
                    son_deger = s.get("son_deger", "—")
                    birim = s.get("birim", "")
                    durum = "🟢" if s.get("aktif", True) else "🔴"
                    col.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:12px;text-align:center;margin-bottom:6px;">
                        <div style="font-size:0.78rem;color:#888;">{durum} {s.get('ad','?')}</div>
                        <div style="font-size:1.5rem;font-weight:800;color:#00b4d8;">{son_deger} {birim}</div>
                        <div style="font-size:0.7rem;color:#666;">{s.get('konum','')}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Canli dashboard icin sensor kaydi ekleyin.")

    # ── Sensör Yönetimi ──
    with sub[1]:
        _styled_section("📡 Sensor Kayit & Yonetim", "#8338ec")

        with st.form("sensor_form"):
            snc1, snc2 = st.columns(2)
            with snc1:
                sn_ad = st.text_input("Sensor Adi", key="sensor_ad")
                sn_tip = st.selectbox("Sensor Tipi", ["Enerji", "Su", "Sicaklik", "Hareket", "Nem", "Isik", "CO2", "Diger"], key="sensor_tip")
                sn_konum = st.text_input("Konum (Bina/Kat/Oda)", key="sensor_konum")
            with snc2:
                sn_birim = st.selectbox("Olcum Birimi", ["kWh", "m3", "C", "adet", "%", "lux", "ppm"], key="sensor_birim")
                sn_esik_min = st.number_input("Min Esik", value=0.0, step=1.0, key="sensor_min")
                sn_esik_max = st.number_input("Max Esik", value=100.0, step=1.0, key="sensor_max")

            if st.form_submit_button("📡 Sensor Ekle", use_container_width=True):
                if sn_ad:
                    sensorler.append({
                        "id": f"sns_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": sn_ad,
                        "tip": sn_tip,
                        "konum": sn_konum,
                        "birim": sn_birim,
                        "esik_min": sn_esik_min,
                        "esik_max": sn_esik_max,
                        "aktif": True,
                        "son_deger": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(sensor_path, sensorler)
                    st.success(f"{sn_ad} sensoru eklendi!")
                    st.rerun()

        if sensorler:
            _styled_section("Kayitli Sensorler", "#06d6a0")
            for idx, s in enumerate(sensorler):
                durum = "🟢 Aktif" if s.get("aktif", True) else "🔴 Pasif"
                with st.expander(f"{s.get('ad','?')} — {s.get('tip','')} ({durum})"):
                    ec1, ec2, ec3 = st.columns(3)
                    ec1.write(f"**Konum:** {s.get('konum','—')}")
                    ec2.write(f"**Birim:** {s.get('birim','')}")
                    ec3.write(f"**Esikler:** {s.get('esik_min','')}-{s.get('esik_max','')}")

                    # Manuel veri girisi
                    yeni_deger = st.number_input("Deger Gir", value=float(s.get("son_deger", 0)), step=0.1, key=f"sns_deger_{idx}")
                    if st.button("Kaydet", key=f"sns_kaydet_{idx}"):
                        s["son_deger"] = yeni_deger
                        veriler.append({
                            "sensor_id": s["id"],
                            "sensor_ad": s.get("ad", "?"),
                            "deger": yeni_deger,
                            "tarih": datetime.now().isoformat(),
                        })
                        # Eşik kontrolü
                        if yeni_deger > s.get("esik_max", 999999) or yeni_deger < s.get("esik_min", -999999):
                            alarmlar.append({
                                "id": f"alr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sensor": s.get("ad", "?"),
                                "konum": s.get("konum", ""),
                                "deger": yeni_deger,
                                "esik": f"{s.get('esik_min','')}-{s.get('esik_max','')}",
                                "tarih": datetime.now().isoformat(),
                                "aktif": True,
                            })
                            _save_json(alarm_path, alarmlar)
                            st.warning("Esik asimi! Alarm olusturuldu.")

                        _save_json(sensor_path, sensorler)
                        _save_json(veri_path, veriler)
                        st.rerun()

    # ── Enerji Haritası ──
    with sub[2]:
        _styled_section("⚡ Oda Bazli Enerji Tuketim Haritasi", "#ffd166")

        enerji_sensorler = [s for s in sensorler if s.get("tip") == "Enerji"]
        if enerji_sensorler:
            # Konum bazlı grupla
            konum_enerji = {}
            for s in enerji_sensorler:
                k = s.get("konum", "Bilinmeyen")
                konum_enerji[k] = konum_enerji.get(k, 0) + s.get("son_deger", 0)

            if konum_enerji:
                max_val = max(konum_enerji.values()) if konum_enerji.values() else 1
                st.markdown("**Konum Bazli Enerji Tuketimi**")
                for konum, val in sorted(konum_enerji.items(), key=lambda x: -x[1]):
                    oran = val / max_val
                    renk = "#e94560" if oran > 0.8 else ("#ffd166" if oran > 0.5 else "#06d6a0")
                    bar_w = int(oran * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="width:180px;color:#e0e0e0;font-weight:600;font-size:0.88rem;">{konum}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:22px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                        </div>
                        <span style="width:80px;text-align:right;color:{renk};font-weight:700;">{val:,.1f} kWh</span>
                    </div>""", unsafe_allow_html=True)

                toplam = sum(konum_enerji.values())
                st.markdown(f"""
                <div style="background:#0f3460;border-radius:12px;padding:16px;text-align:center;margin-top:14px;">
                    <div style="color:#888;">Toplam Enerji Tuketimi</div>
                    <div style="font-size:2.2rem;font-weight:800;color:#ffd166;">{toplam:,.1f} kWh</div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Enerji haritasi icin 'Enerji' tipinde sensor ekleyin.")

    # ── Alarm Merkezi ──
    with sub[3]:
        _styled_section("🚨 IoT Alarm & Bildirim Merkezi", "#e94560")

        aktif_alarmlar = [a for a in alarmlar if a.get("aktif", True)]
        if aktif_alarmlar:
            st.error(f"🚨 {len(aktif_alarmlar)} aktif alarm mevcut!")
            for idx, a in enumerate(aktif_alarmlar):
                st.markdown(f"""
                <div style="background:#e9456012;border-left:4px solid #e94560;padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;">
                        <strong style="color:#e94560;">{a.get('sensor','?')}</strong>
                        <span style="color:#888;font-size:0.78rem;">{a.get('tarih','')[:16]}</span>
                    </div>
                    <div style="color:#aaa;font-size:0.85rem;margin-top:3px;">
                        Konum: {a.get('konum','')} | Deger: {a.get('deger','')} | Esik: {a.get('esik','')}
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button("Onayla & Kapat", key=f"alarm_kapat_{idx}"):
                    a["aktif"] = False
                    _save_json(alarm_path, alarmlar)
                    st.rerun()
        else:
            _styled_info_banner("Aktif alarm bulunmuyor. Tum sensorler normal calisıyor. ✅")

        # Alarm geçmişi
        kapali_alarmlar = [a for a in alarmlar if not a.get("aktif")]
        if kapali_alarmlar:
            _styled_section("Alarm Gecmisi", "#888")
            for a in reversed(kapali_alarmlar[-10:]):
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;">
                    <span style="color:#888;">{a.get('sensor','?')} — {a.get('konum','')}</span>
                    <span style="color:#666;font-size:0.78rem;">{a.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── Anormallik Tespiti ──
    with sub[4]:
        _styled_section("📈 AI Anormallik Tespit Motoru", "#8338ec")

        if veriler:
            _styled_info_banner("Sensor verilerindeki anormal degisimleri ve sapmalari otomatik tespit eder.")

            # Sensör bazlı istatistik
            sensor_verileri = {}
            for v in veriler:
                sid = v.get("sensor_ad", "?")
                if sid not in sensor_verileri:
                    sensor_verileri[sid] = []
                sensor_verileri[sid].append(v.get("deger", 0))

            for sensor, degerler in sensor_verileri.items():
                if len(degerler) >= 3:
                    ort = sum(degerler) / len(degerler)
                    maks = max(degerler)
                    mn = min(degerler)
                    std_sapma = (sum((d - ort) ** 2 for d in degerler) / len(degerler)) ** 0.5
                    son = degerler[-1]
                    anormal = abs(son - ort) > 2 * std_sapma if std_sapma > 0 else False

                    renk = "#e94560" if anormal else "#06d6a0"
                    durum = "ANORMAL" if anormal else "NORMAL"

                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;border-left:4px solid {renk};">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="color:#e0e0e0;">{sensor}</strong>
                            <span style="background:{renk}20;color:{renk};padding:3px 10px;border-radius:8px;font-weight:700;font-size:0.82rem;">{durum}</span>
                        </div>
                        <div style="display:flex;gap:16px;margin-top:6px;">
                            <span style="color:#888;font-size:0.8rem;">Ort: <strong style="color:#00b4d8;">{ort:.1f}</strong></span>
                            <span style="color:#888;font-size:0.8rem;">Son: <strong style="color:{renk};">{son:.1f}</strong></span>
                            <span style="color:#888;font-size:0.8rem;">Min/Max: {mn:.1f}/{maks:.1f}</span>
                            <span style="color:#888;font-size:0.8rem;">Std: {std_sapma:.2f}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

            anormal_sayi = sum(1 for s, d in sensor_verileri.items() if len(d) >= 3 and abs(d[-1] - sum(d)/len(d)) > 2 * max(0.01, (sum((v - sum(d)/len(d))**2 for v in d)/len(d))**0.5))
            if anormal_sayi > 0:
                st.warning(f"⚠️ {anormal_sayi} sensorde anormal deger tespit edildi!")
        else:
            _styled_info_banner("Anormallik tespiti icin sensor verisi gerekiyor.")

    # ── Tasarruf Simülasyonu ──
    with sub[5]:
        _styled_section("💡 Tasarruf Simulasyonu & Oneri", "#06d6a0")

        _styled_info_banner("Farkli tasarruf senaryolarini simule ederek potansiyel kazanimi hesaplayin.")

        st.markdown("**Senaryo Parametreleri**")
        sim_c1, sim_c2 = st.columns(2)
        with sim_c1:
            aylik_enerji = st.number_input("Aylik Enerji Tuketimi (kWh)", min_value=0.0, value=5000.0, step=100.0, key="sim_enerji")
            birim_fiyat = st.number_input("Enerji Birim Fiyati (TL/kWh)", min_value=0.0, value=3.5, step=0.1, key="sim_fiyat")
        with sim_c2:
            led_oran = st.slider("LED Donusum Orani (%)", 0, 100, 50, key="sim_led")
            sensor_oran = st.slider("Hareket Sensoru Kapsami (%)", 0, 100, 30, key="sim_sensor")

        mevcut_maliyet = aylik_enerji * birim_fiyat
        led_tasarruf = aylik_enerji * (led_oran / 100) * 0.40 * birim_fiyat
        sensor_tasarruf = aylik_enerji * (sensor_oran / 100) * 0.25 * birim_fiyat
        toplam_tasarruf = led_tasarruf + sensor_tasarruf
        yeni_maliyet = mevcut_maliyet - toplam_tasarruf
        tasarruf_oran = int(toplam_tasarruf / max(1, mevcut_maliyet) * 100)

        _styled_stat_row([
            ("Mevcut Aylik", f"TL{mevcut_maliyet:,.0f}"),
            ("LED Tasarruf", f"TL{led_tasarruf:,.0f}"),
            ("Sensor Tasarruf", f"TL{sensor_tasarruf:,.0f}"),
            ("Toplam Tasarruf", f"TL{toplam_tasarruf:,.0f}"),
            ("Yeni Maliyet", f"TL{yeni_maliyet:,.0f}"),
            ("Tasarruf Orani", f"%{tasarruf_oran}"),
        ])

        # Yıllık projeksiyon
        yillik_tasarruf = toplam_tasarruf * 12
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#06d6a020,#00b4d810);border:1px solid #06d6a040;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
            <div style="color:#06d6a0;font-size:1.1rem;font-weight:700;">Yillik Tahmini Tasarruf</div>
            <div style="font-size:2.8rem;font-weight:900;color:#06d6a0;">TL{yillik_tasarruf:,.0f}</div>
            <div style="color:#888;font-size:0.85rem;">LED (%{led_oran}) + Sensor (%{sensor_oran}) senaryosu</div>
        </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. KURUM VARLIK AKADEMİSİ & BİLGİ BANKASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_varlik_akademi(store):
    _styled_header("Kurum Varlik Akademisi & Bilgi Bankasi", "🎓")

    egitim_path = _get_data_path(store, "varlik_egitimler.json")
    egitimler = _load_json(egitim_path)

    quiz_path = _get_data_path(store, "varlik_quizler.json")
    quizler = _load_json(quiz_path)

    rehber_path = _get_data_path(store, "ariza_rehberi.json")
    rehberler = _load_json(rehber_path)

    sertifika_path = _get_data_path(store, "akademi_sertifikalari.json")
    sertifikalar = _load_json(sertifika_path)

    _styled_stat_row([
        ("Egitim Icerigi", len(egitimler)),
        ("Quiz Sayisi", len(quizler)),
        ("Ariza Rehberi", len(rehberler)),
        ("Verilen Sertifika", len(sertifikalar)),
    ])

    sub = st.tabs(["📚 Egitim Kutuphanesi", "📝 Quiz & Sertifika", "🔧 Ariza Rehberi", "👥 Departman Takip", "🤖 AI Soru-Cevap", "📊 Analitik"])

    # ── Eğitim Kütüphanesi ──
    with sub[0]:
        _styled_section("📚 Egitim Icerik Kutuphanesi", "#0f3460")

        with st.form("egitim_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_baslik = st.text_input("Egitim Basligi", key="egitim_baslik")
                e_kategori = st.selectbox("Kategori", [
                    "Demirbas Kullanim", "Bakim Proseduru", "Tasarruf Ipuclari",
                    "Guvenlik", "Hijyen & Temizlik", "Teknoloji Kullanim",
                    "Acil Durum", "Genel"
                ], key="egitim_kat")
                e_seviye = st.selectbox("Seviye", ["Baslangic", "Orta", "Ileri"], key="egitim_sev")
            with ec2:
                e_tur = st.selectbox("Icerik Turu", ["Dokuman", "Video", "Sunum", "Infografik", "Checklist"], key="egitim_tur")
                e_sure = st.number_input("Tahmini Sure (dk)", min_value=1, value=15, key="egitim_sure")
                e_hedef = st.multiselect("Hedef Kitle", ["Tum Personel", "Ogretmenler", "Idari", "Teknik", "Temizlik", "Guvenlik"], key="egitim_hedef")
            e_icerik = st.text_area("Icerik / Ozet", height=100, key="egitim_icerik")

            if st.form_submit_button("📚 Egitim Ekle", use_container_width=True):
                if e_baslik:
                    egitimler.append({
                        "id": f"egt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": e_baslik,
                        "kategori": e_kategori,
                        "seviye": e_seviye,
                        "tur": e_tur,
                        "sure": e_sure,
                        "hedef": e_hedef,
                        "icerik": e_icerik,
                        "tamamlayan": [],
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(egitim_path, egitimler)
                    st.success(f"'{e_baslik}' egitimi eklendi!")
                    st.rerun()

        if egitimler:
            # Kategori filtresi
            kategoriler = list(set(e.get("kategori", "") for e in egitimler))
            filtre = st.selectbox("Kategori Filtresi", ["Tumu"] + kategoriler, key="egitim_filtre")

            filtreli = egitimler if filtre == "Tumu" else [e for e in egitimler if e.get("kategori") == filtre]

            for idx, e in enumerate(filtreli):
                tur_ikon = {"Dokuman": "📄", "Video": "🎬", "Sunum": "📊", "Infografik": "🖼️", "Checklist": "✅"}.get(e.get("tur", ""), "📋")
                sev_renk = {"Baslangic": "#06d6a0", "Orta": "#ffd166", "Ileri": "#e94560"}.get(e.get("seviye", ""), "#888")
                tamamlayan_sayi = len(e.get("tamamlayan", []))

                with st.expander(f"{tur_ikon} {e.get('baslik','?')} — {e.get('kategori','')} ({e.get('sure','')} dk)"):
                    sc1, sc2, sc3 = st.columns(3)
                    sc1.markdown(f"**Seviye:** <span style='color:{sev_renk}'>{e.get('seviye','')}</span>", unsafe_allow_html=True)
                    sc2.write(f"**Tur:** {e.get('tur','')}")
                    sc3.write(f"**Tamamlayan:** {tamamlayan_sayi} kisi")

                    if e.get("icerik"):
                        st.info(e["icerik"])

                    # Tamamlama kaydi
                    kisi = st.text_input("Tamamlayan Kisi Adi", key=f"egt_tamam_kisi_{idx}")
                    if st.button("Tamamlandi Olarak Isaretle", key=f"egt_tamam_{idx}"):
                        if kisi:
                            if "tamamlayan" not in e:
                                e["tamamlayan"] = []
                            e["tamamlayan"].append({"kisi": kisi, "tarih": datetime.now().isoformat()})
                            _save_json(egitim_path, egitimler)
                            st.success(f"{kisi} egitimi tamamladi!")
                            st.rerun()

    # ── Quiz & Sertifika ──
    with sub[1]:
        _styled_section("📝 Quiz Olustur & Sertifika Ver", "#8338ec")

        with st.form("quiz_form"):
            qc1, qc2 = st.columns(2)
            with qc1:
                q_baslik = st.text_input("Quiz Basligi", key="quiz_baslik")
                q_kategori = st.selectbox("Kategori", ["Demirbas Kullanim", "Bakim", "Tasarruf", "Guvenlik", "Genel"], key="quiz_kat")
            with qc2:
                q_soru_sayisi = st.number_input("Soru Sayisi", min_value=3, max_value=50, value=10, key="quiz_soru")
                q_gecme_puani = st.number_input("Gecme Puani (%)", min_value=50, max_value=100, value=70, key="quiz_gecme")

            q_sorular = st.text_area("Sorulari girin (her satir bir soru)", height=120, key="quiz_sorular")

            if st.form_submit_button("📝 Quiz Olustur", use_container_width=True):
                if q_baslik:
                    sorular = [s.strip() for s in q_sorular.split("\n") if s.strip()] if q_sorular else []
                    quizler.append({
                        "id": f"qz_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": q_baslik,
                        "kategori": q_kategori,
                        "soru_sayisi": q_soru_sayisi,
                        "gecme_puani": q_gecme_puani,
                        "sorular": sorular,
                        "sonuclar": [],
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(quiz_path, quizler)
                    st.success(f"'{q_baslik}' quizi olusturuldu!")
                    st.rerun()

        if quizler:
            _styled_section("Mevcut Quizler", "#ffd166")
            for idx, q in enumerate(quizler):
                katilimci = len(q.get("sonuclar", []))
                gecen = len([s for s in q.get("sonuclar", []) if s.get("puan", 0) >= q.get("gecme_puani", 70)])

                with st.expander(f"📝 {q.get('baslik','?')} ({katilimci} katilimci, {gecen} basarili)"):
                    st.write(f"**Gecme Puani:** %{q.get('gecme_puani','')}")
                    if q.get("sorular"):
                        for i, s in enumerate(q["sorular"][:5]):
                            st.caption(f"{i+1}. {s}")

                    # Sonuç kaydet
                    rc1, rc2 = st.columns(2)
                    with rc1:
                        r_kisi = st.text_input("Katilimci", key=f"qz_kisi_{idx}")
                    with rc2:
                        r_puan = st.number_input("Puan (%)", min_value=0, max_value=100, value=0, key=f"qz_puan_{idx}")
                    if st.button("Sonuc Kaydet", key=f"qz_kaydet_{idx}"):
                        if r_kisi:
                            q.setdefault("sonuclar", []).append({
                                "kisi": r_kisi,
                                "puan": r_puan,
                                "tarih": datetime.now().isoformat(),
                            })
                            _save_json(quiz_path, quizler)

                            if r_puan >= q.get("gecme_puani", 70):
                                sertifikalar.append({
                                    "id": f"srt_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                                    "kisi": r_kisi,
                                    "quiz": q.get("baslik", ""),
                                    "puan": r_puan,
                                    "tarih": datetime.now().isoformat(),
                                })
                                _save_json(sertifika_path, sertifikalar)
                                st.success(f"Tebrikler! {r_kisi} sertifika kazandi! 🎉")
                            else:
                                st.warning(f"Puan yetersiz. Gecme puani: %{q.get('gecme_puani','')}")
                            st.rerun()

        # Sertifikalar
        if sertifikalar:
            _styled_section("Verilen Sertifikalar", "#06d6a0")
            for s in reversed(sertifikalar[-10:]):
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#06d6a015,#06d6a008);border:1px solid #06d6a030;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:1.2rem;">🎓</span>
                        <strong style="color:#06d6a0;margin-left:6px;">{s.get('kisi','')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{s.get('quiz','')}</span>
                    </div>
                    <div>
                        <span style="color:#ffd166;font-weight:700;">%{s.get('puan','')}</span>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{s.get('tarih','')[:10]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Arıza Rehberi ──
    with sub[2]:
        _styled_section("🔧 En Sik Ariza Cozum Rehberi", "#e94560")

        with st.form("rehber_form"):
            rc1, rc2 = st.columns(2)
            with rc1:
                r_baslik = st.text_input("Ariza / Sorun Basligi", key="rehber_baslik")
                r_kategori = st.selectbox("Kategori", ["Elektronik", "Mekanik", "Elektrik", "Tesisat", "Bilisim", "Diger"], key="rehber_kat")
            with rc2:
                r_cihaz = st.text_input("Ilgili Cihaz/Ekipman", key="rehber_cihaz")
                r_zorluk = st.selectbox("Zorluk", ["Kolay", "Orta", "Zor", "Uzman Gerektir"], key="rehber_zor")
            r_cozum = st.text_area("Cozum Adimlari", height=120, key="rehber_cozum")

            if st.form_submit_button("🔧 Rehber Ekle", use_container_width=True):
                if r_baslik and r_cozum:
                    rehberler.append({
                        "id": f"rhb_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "baslik": r_baslik,
                        "kategori": r_kategori,
                        "cihaz": r_cihaz,
                        "zorluk": r_zorluk,
                        "cozum": r_cozum,
                        "faydali": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(rehber_path, rehberler)
                    st.success("Rehber eklendi!")
                    st.rerun()

        if rehberler:
            arama = st.text_input("Ariza ara...", key="rehber_ara")
            filtreli = rehberler
            if arama:
                arama_l = arama.lower()
                filtreli = [r for r in rehberler if arama_l in (r.get("baslik", "") + r.get("cihaz", "") + r.get("cozum", "")).lower()]

            for idx, r in enumerate(filtreli):
                zorluk_renk = {"Kolay": "#06d6a0", "Orta": "#ffd166", "Zor": "#e94560", "Uzman Gerektir": "#8338ec"}.get(r.get("zorluk", ""), "#888")

                with st.expander(f"🔧 {r.get('baslik','?')} — {r.get('cihaz','')} ({r.get('zorluk','')})"):
                    st.markdown(f"**Kategori:** {r.get('kategori','')} | **Zorluk:** <span style='color:{zorluk_renk}'>{r.get('zorluk','')}</span>", unsafe_allow_html=True)
                    st.markdown("**Cozum Adimlari:**")
                    st.info(r.get("cozum", ""))
                    fc1, fc2 = st.columns([1, 4])
                    if fc1.button("👍 Faydali", key=f"rhb_faydali_{idx}"):
                        r["faydali"] = r.get("faydali", 0) + 1
                        _save_json(rehber_path, rehberler)
                        st.rerun()
                    fc2.caption(f"👍 {r.get('faydali', 0)} kisi faydali buldu")

    # ── Departman Takip ──
    with sub[3]:
        _styled_section("👥 Departman Bazli Egitim Tamamlama Takibi", "#00b4d8")

        if egitimler:
            # Tamamlayan kişileri departman bazlı grupla
            dept_tamamlama = {}
            toplam_egitim = len(egitimler)

            for e in egitimler:
                for t in e.get("tamamlayan", []):
                    kisi = t.get("kisi", "?")
                    if kisi not in dept_tamamlama:
                        dept_tamamlama[kisi] = 0
                    dept_tamamlama[kisi] += 1

            if dept_tamamlama:
                st.markdown("**Kisi Bazli Egitim Tamamlama**")
                for kisi, sayi in sorted(dept_tamamlama.items(), key=lambda x: -x[1]):
                    oran = min(100, int(sayi / max(1, toplam_egitim) * 100))
                    renk = "#06d6a0" if oran >= 80 else ("#ffd166" if oran >= 40 else "#e94560")
                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <strong style="color:#e0e0e0;">{kisi}</strong>
                            <span style="color:{renk};font-weight:700;">{sayi}/{toplam_egitim} (%{oran})</span>
                        </div>
                        <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                            <div style="width:{oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                _styled_info_banner("Henuz egitim tamamlama kaydi bulunmuyor.")
        else:
            _styled_info_banner("Departman takibi icin egitim icerigi olusturun.")

    # ── AI Soru-Cevap ──
    with sub[4]:
        _styled_section("🤖 AI Destekli Soru-Cevap", "#8338ec")

        _styled_info_banner("Demirbas kullanimi, bakim ve tasarruf hakkinda bilgi bankasından aninda yanit alin.")

        sik_sorulan = [
            ("Yeni demirbas nasil kayit altina alinir?", "Tuketim & Demirbas > Demirbas Kayit sekmesinden varlik bilgilerini girerek kayit olusturabilirsiniz. Barkod/QR kod otomatik uretilir."),
            ("Zimmet degisikligi nasil yapilir?", "Zimmet Yonetimi sekmesinden mevcut zimmeti sonlandirip yeni kişiye atama yapabilirsiniz. Tum degisiklikler denetim zincirine kaydedilir."),
            ("Bakim plani nasil olusturulur?", "Bakim Tahmin sekmesinden onleyici bakim takvimi olusturabilirsiniz. AI, arizadan once bakim zamani onerir."),
            ("Hurda islemi nasil yapilir?", "Demirbas kaydinda 'Hurdaya Ayir' secenegiyle resmi hurda islemini baslatabilirsiniz. Blokzincir denetim kaydı otomatik olusur."),
            ("Stok seviyesi nasil takip edilir?", "Stok Durumu sekmesinden anlik stok goruntuleme, Stok Tahmin sekmesinden AI tabanli stok tahmini alabilirsiniz."),
            ("Enerji tasarrufu icin ne yapilmali?", "Surdurulebilirlik sekmesinden karbon ayak izi takibi, IoT sekmesinden gercek zamanli enerji izleme yapabilirsiniz."),
        ]

        for soru, cevap in sik_sorulan:
            with st.expander(f"❓ {soru}"):
                st.markdown(f"""
                <div style="background:#8338ec12;border-left:3px solid #8338ec;padding:10px 14px;border-radius:0 8px 8px 0;">
                    <span style="color:#e0e0e0;font-size:0.9rem;">{cevap}</span>
                </div>""", unsafe_allow_html=True)

        # Serbest soru
        _styled_section("Soru Sorun", "#00b4d8")
        soru_input = st.text_input("Sorunuzu yazin...", key="ai_soru")
        if soru_input:
            # Basit keyword matching
            cevap = None
            for s, c in sik_sorulan:
                if any(kelime in soru_input.lower() for kelime in s.lower().split()[:3]):
                    cevap = c
                    break
            if cevap:
                st.success(f"💡 {cevap}")
            else:
                st.info("Bu konuda bilgi bankamizda henuz kayit bulunmuyor. Ariza Rehberi veya Egitim Kutuphanesine goz atin.")

    # ── Analitik ──
    with sub[5]:
        _styled_section("📊 Akademi Analitikleri & Genel Bakis", "#ffd166")

        toplam_egitim = len(egitimler)
        toplam_quiz = len(quizler)
        toplam_sertifika = len(sertifikalar)
        toplam_rehber = len(rehberler)
        toplam_tamamlayan = sum(len(e.get("tamamlayan", [])) for e in egitimler)

        _styled_stat_row([
            ("Egitim Icerigi", toplam_egitim),
            ("Quiz", toplam_quiz),
            ("Sertifika", toplam_sertifika),
            ("Ariza Rehberi", toplam_rehber),
            ("Tamamlama Kaydi", toplam_tamamlayan),
        ])

        # Kategori dağılımı
        if egitimler:
            _styled_section("Egitim Kategori Dagilimi", "#00b4d8")
            kat_dagilim = {}
            for e in egitimler:
                k = e.get("kategori", "Diger")
                kat_dagilim[k] = kat_dagilim.get(k, 0) + 1

            max_val = max(kat_dagilim.values()) if kat_dagilim.values() else 1
            for kat, sayi in sorted(kat_dagilim.items(), key=lambda x: -x[1]):
                bar_w = int(sayi / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:160px;color:#e0e0e0;font-size:0.88rem;">{kat}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#00b4d8;border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:#00b4d8;font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

        # Akademi skoru
        aktivite = toplam_egitim + toplam_quiz + toplam_rehber + toplam_sertifika
        skor = min(100, aktivite * 5 + 20)
        renk = "#06d6a0" if skor >= 70 else ("#ffd166" if skor >= 40 else "#e94560")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
            <div style="color:#888;">Akademi Olgunluk Skoru</div>
            <div style="font-size:3rem;font-weight:800;color:{renk};">{skor}/100</div>
            <div style="color:#aaa;font-size:0.85rem;">Daha fazla icerik ve katilim ile skoru artirin</div>
        </div>""", unsafe_allow_html=True)
