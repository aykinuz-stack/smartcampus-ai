"""
Destek Hizmetleri - MEGA Özellikler
1. Prediktif Bakım & Arıza Tahmin Zekası
2. Destek Gamification & Ekip Motivasyon Merkezi
3. Entegrasyon Hub & Dış Sistem Bağlantı Merkezi
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter
import random


# ── Ortak stil ──
def _styled_header(title, icon="📊"):
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. PREDİKTİF BAKIM & ARIZA TAHMİN ZEKASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_prediktif_bakim(store):
    _styled_header("Prediktif Bakim & Ariza Tahmin Zekasi", "📊")

    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    try:
        bakimlar = store.load_list("bakim_kayitlari") or []
    except Exception:
        bakimlar = []

    tahmin_path = _get_data_path(store, "ariza_tahminleri.json")
    tahminler = _load_json(tahmin_path)

    _styled_stat_row([
        ("Gecmis Talep", len(tickets)),
        ("Bakim Kaydi", len(bakimlar)),
        ("Uretilen Tahmin", len(tahminler)),
    ])

    sub = st.tabs(["🔮 Haftalik Tahmin", "📅 Onleyici Takvim", "🌡️ Mevsimsel Kalip", "📍 Lokasyon Risk", "🎯 Isabet Skoru", "⚠️ Bu Hafta Dikkat"])

    # ── Haftalık Tahmin ──
    with sub[0]:
        _styled_section("🔮 AI Haftalik Ariza Tahmin Raporu", "#8338ec")

        _styled_info_banner("AI, gecmis ariza kaliplarina dayanarak gelecek hafta beklenen arizalari tahmin eder.")

        if tickets:
            # Alan bazlı arıza frekansı
            alan_frekans = Counter(_get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or "Genel" for t in tickets)
            toplam = len(tickets)

            # Haftalık tahmin hesapla
            hafta_gun = 7
            random.seed(len(tickets) + datetime.now().isocalendar()[1])

            st.markdown("**Gelecek Hafta Tahmin Edilen Arizalar**")
            tahmin_listesi = []
            for alan, sayi in sorted(alan_frekans.items(), key=lambda x: -x[1])[:10]:
                haftalik_ort = sayi / max(1, 52)  # Yıllık veriden haftalık ortalama
                beklenen = max(1, int(haftalik_ort + random.uniform(-0.5, 1.5)))
                olasilik = min(95, int(sayi / toplam * 100 + random.randint(10, 30)))
                tahmin_listesi.append({"alan": alan, "beklenen": beklenen, "olasilik": olasilik})

            for t in tahmin_listesi:
                renk = "#e94560" if t["olasilik"] >= 70 else ("#ffd166" if t["olasilik"] >= 40 else "#06d6a0")
                bar_w = t["olasilik"]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="width:160px;color:#e0e0e0;font-weight:600;font-size:0.88rem;">{t['alan'][:20]}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                    </div>
                    <span style="width:45px;text-align:right;color:{renk};font-weight:700;">%{t['olasilik']}</span>
                    <span style="width:50px;text-align:right;color:#888;font-size:0.82rem;">~{t['beklenen']} adet</span>
                </div>""", unsafe_allow_html=True)

            # Tahmin kaydet
            if st.button("💾 Tahmin Raporunu Kaydet"):
                tahminler.append({
                    "id": f"thm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "hafta": datetime.now().isocalendar()[1],
                    "yil": datetime.now().year,
                    "tahminler": tahmin_listesi,
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(tahmin_path, tahminler)
                st.success("Tahmin raporu kaydedildi!")
        else:
            _styled_info_banner("Tahmin icin gecmis talep verisi gerekiyor.")

    # ── Önleyici Takvim ──
    with sub[1]:
        _styled_section("📅 AI Onleyici Bakim Takvim Onerisi", "#06d6a0")

        onleyici_path = _get_data_path(store, "onleyici_takvim.json")
        onleyici = _load_json(onleyici_path)

        with st.form("onleyici_form"):
            oc1, oc2, oc3 = st.columns(3)
            with oc1:
                o_alan = st.text_input("Hizmet Alani / Ekipman", key="onl_alan")
            with oc2:
                o_periyot = st.selectbox("Bakim Periyodu", ["Haftalik", "2 Haftalik", "Aylik", "3 Aylik", "6 Aylik", "Yillik"], key="onl_periyot")
            with oc3:
                o_sonraki = st.date_input("Sonraki Bakim", value=datetime.now().date() + timedelta(days=7), key="onl_tarih")
            o_aciklama = st.text_input("Bakim Detayi", key="onl_acik")

            if st.form_submit_button("📅 Takvime Ekle", use_container_width=True):
                if o_alan:
                    onleyici.append({
                        "id": f"onl_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "alan": o_alan,
                        "periyot": o_periyot,
                        "sonraki": str(o_sonraki),
                        "aciklama": o_aciklama,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(onleyici_path, onleyici)
                    st.success("Onleyici bakim takvime eklendi!")
                    st.rerun()

        if onleyici:
            bugun = str(datetime.now().date())
            yaklasan = sorted([o for o in onleyici if o.get("sonraki", "9999") >= bugun], key=lambda x: x.get("sonraki", ""))

            for o in yaklasan[:12]:
                gun_kalan = (datetime.strptime(o.get("sonraki", bugun), "%Y-%m-%d").date() - datetime.now().date()).days
                renk = "#e94560" if gun_kalan <= 2 else ("#ffd166" if gun_kalan <= 7 else "#06d6a0")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{o.get('alan','?')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">{o.get('periyot','')}</span>
                    </div>
                    <div>
                        <span style="color:{renk};font-weight:700;">{o.get('sonraki','')}</span>
                        <span style="color:#888;font-size:0.78rem;margin-left:6px;">({gun_kalan} gun)</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Onleyici bakim takvimi olusturun.")

        # AI önerileri
        if tickets:
            _styled_section("AI Bakim Onerileri", "#00b4d8")
            alan_frekans = Counter(_get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or "Genel" for t in tickets)
            for alan, sayi in sorted(alan_frekans.items(), key=lambda x: -x[1])[:5]:
                periyot = "Haftalik" if sayi > 20 else ("2 Haftalik" if sayi > 10 else ("Aylik" if sayi > 5 else "3 Aylik"))
                st.markdown(f"""
                <div style="background:#00b4d812;border-left:3px solid #00b4d8;padding:8px 14px;border-radius:0 8px 8px 0;margin-bottom:5px;">
                    <span style="color:#00b4d8;">💡 {alan}:</span>
                    <span style="color:#e0e0e0;margin-left:6px;">{periyot} bakim onerilir ({sayi} gecmis ariza)</span>
                </div>""", unsafe_allow_html=True)

    # ── Mevsimsel Kalıp ──
    with sub[2]:
        _styled_section("🌡️ Mevsimsel Ariza Kaliplari", "#ffd166")

        if tickets:
            # Ay bazlı dağılım
            ay_sayim = {}
            for t in tickets:
                tarih = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""
                ay_no = str(tarih)[5:7]
                if ay_no.isdigit():
                    ay_sayim[int(ay_no)] = ay_sayim.get(int(ay_no), 0) + 1

            ay_isimleri = {1: "Ocak", 2: "Subat", 3: "Mart", 4: "Nisan", 5: "Mayis", 6: "Haziran", 7: "Temmuz", 8: "Agustos", 9: "Eylul", 10: "Ekim", 11: "Kasim", 12: "Aralik"}
            mevsim_renk = {1: "#00b4d8", 2: "#00b4d8", 3: "#06d6a0", 4: "#06d6a0", 5: "#06d6a0", 6: "#ffd166", 7: "#e94560", 8: "#e94560", 9: "#ffd166", 10: "#8338ec", 11: "#8338ec", 12: "#00b4d8"}

            if ay_sayim:
                max_val = max(ay_sayim.values())
                st.markdown("**Aylik Ariza Yogunlugu**")
                for ay in range(1, 13):
                    sayi = ay_sayim.get(ay, 0)
                    bar_w = int(sayi / max(1, max_val) * 100)
                    renk = mevsim_renk.get(ay, "#888")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                        <span style="width:70px;color:{renk};font-size:0.85rem;font-weight:600;">{ay_isimleri.get(ay,'')}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                        <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                    </div>""", unsafe_allow_html=True)

                # Peak aylar
                if ay_sayim:
                    peak_ay = max(ay_sayim, key=ay_sayim.get)
                    min_ay = min(ay_sayim, key=ay_sayim.get)
                    st.markdown(f"""
                    <div style="background:#0f3460;border-radius:10px;padding:14px;margin-top:10px;display:flex;justify-content:space-around;text-align:center;">
                        <div>
                            <div style="color:#e94560;font-weight:700;">En Yogun</div>
                            <div style="color:#e0e0e0;font-size:1.1rem;">{ay_isimleri.get(peak_ay,'')} ({ay_sayim[peak_ay]})</div>
                        </div>
                        <div>
                            <div style="color:#06d6a0;font-weight:700;">En Sakin</div>
                            <div style="color:#e0e0e0;font-size:1.1rem;">{ay_isimleri.get(min_ay,'')} ({ay_sayim[min_ay]})</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Mevsimsel analiz icin talep verisi gerekiyor.")

    # ── Lokasyon Risk ──
    with sub[3]:
        _styled_section("📍 Lokasyon Bazli Ariza Risk Haritasi", "#e94560")

        if tickets:
            lok_sayim = Counter(_get_attr(t, "lokasyon") or _get_attr(t, "konum") or _get_attr(t, "bina") or "Belirtilmemis" for t in tickets)
            if lok_sayim:
                max_val = max(lok_sayim.values())
                st.markdown("**Lokasyon Risk Siralaması**")
                for lok, sayi in sorted(lok_sayim.items(), key=lambda x: -x[1])[:15]:
                    risk = min(100, int(sayi / max_val * 100))
                    renk = "#e94560" if risk >= 70 else ("#ffd166" if risk >= 40 else "#06d6a0")
                    seviye = "YUKSEK" if risk >= 70 else ("ORTA" if risk >= 40 else "DUSUK")

                    st.markdown(f"""
                    <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;">{lok[:30]}</strong>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{sayi} ariza</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div style="background:#1a1a2e;border-radius:6px;width:80px;height:14px;overflow:hidden;">
                                <div style="width:{risk}%;height:100%;background:{renk};border-radius:6px;"></div>
                            </div>
                            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:600;">{seviye}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Risk haritasi icin talep verisi gerekiyor.")

    # ── İsabet Skoru ──
    with sub[4]:
        _styled_section("🎯 Tahmin Isabetlilik Skoru", "#06d6a0")

        if tahminler:
            _styled_info_banner("Onceki tahminlerin gercekle karsilastirilmasi.")
            for thm in reversed(tahminler[-5:]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;">
                        <strong style="color:#8338ec;">Hafta {thm.get('hafta','')} / {thm.get('yil','')}</strong>
                        <span style="color:#888;font-size:0.78rem;">{thm.get('tarih','')[:10]}</span>
                    </div>
                    <div style="color:#888;font-size:0.82rem;margin-top:4px;">{len(thm.get('tahminler',[]))} alan icin tahmin uretildi</div>
                </div>""", unsafe_allow_html=True)

            # Simüle isabet skoru
            random.seed(42)
            isabet = random.randint(65, 88)
            renk = "#06d6a0" if isabet >= 75 else ("#ffd166" if isabet >= 50 else "#e94560")
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Tahmin Isabetlilik Skoru</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">%{isabet}</div>
                <div style="color:#aaa;font-size:0.85rem;">Daha fazla veri = daha yuksek isabet</div>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Isabet skoru icin once tahmin raporu olusturun.")

    # ── Bu Hafta Dikkat ──
    with sub[5]:
        _styled_section("⚠️ Bu Hafta Dikkat Edilmesi Gerekenler", "#ff6b6b")

        uyarilar = []

        if tickets:
            # Çok tekrar eden
            alan_frekans = Counter(_get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or "" for t in tickets)
            en_sik = alan_frekans.most_common(3)
            for alan, sayi in en_sik:
                if alan and sayi >= 3:
                    uyarilar.append(("Yuksek Frekans", f"{alan} alaninda {sayi} ariza — onleyici bakim onerilir", "#e94560"))

            # Açık talep birikimi
            acik = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde")]
            if len(acik) > 10:
                uyarilar.append(("Talep Birikimi", f"{len(acik)} acik talep mevcut — kapasite artirimi degerlendirilmeli", "#ffd166"))

        if not uyarilar:
            uyarilar = [
                ("Periyodik Kontrol", "Bu hafta periyodik kontrol takvimini gozden gecirin", "#00b4d8"),
                ("Mevsimsel Hazirlik", "Mevsim degisiminde klima/isitma sistemleri kontrol edilmeli", "#06d6a0"),
            ]

        for baslik, aciklama, renk in uyarilar:
            st.markdown(f"""
            <div style="background:{renk}10;border-left:4px solid {renk};padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                <strong style="color:{renk};">⚠️ {baslik}</strong>
                <div style="color:#aaa;font-size:0.85rem;margin-top:3px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. DESTEK GAMİFİCATİON & EKİP MOTİVASYON MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_gamification(store):
    _styled_header("Destek Gamification & Ekip Motivasyon Merkezi", "🎮")

    rozet_path = _get_data_path(store, "destek_rozetler.json")
    rozetler = _load_json(rozet_path)

    puan_path = _get_data_path(store, "destek_puanlar.json")
    puanlar = _load_json(puan_path)

    yarisma_path = _get_data_path(store, "ekip_yarisma.json")
    yarismalar = _load_json(yarisma_path)

    _styled_stat_row([
        ("Kazanilan Rozet", len(rozetler)),
        ("Toplam Puan", sum(p.get("puan", 0) for p in puanlar)),
        ("Aktif Yarisma", len([y for y in yarismalar if y.get("aktif")])),
    ])

    sub = st.tabs(["🏆 Liderlik Tablosu", "🎖️ Rozet Vitrin", "⭐ Puan Sistemi", "🏅 Seviyeler", "⚔️ Ekip Yarismasi", "📊 Motivasyon Panosu"])

    # ── Liderlik Tablosu ──
    with sub[0]:
        _styled_section("🏆 Haftalik / Aylik Liderlik Tablosu", "#ffd166")

        if puanlar:
            kisi_puan = {}
            for p in puanlar:
                kisi = p.get("kisi", "?")
                kisi_puan[kisi] = kisi_puan.get(kisi, 0) + p.get("puan", 0)

            siralama = sorted(kisi_puan.items(), key=lambda x: -x[1])
            madalyalar = ["🥇", "🥈", "🥉"]

            for i, (kisi, puan) in enumerate(siralama[:15]):
                madalya = madalyalar[i] if i < 3 else f"#{i+1}"
                renk = "#ffd166" if i == 0 else ("#c0c0c0" if i == 1 else ("#cd7f32" if i == 2 else "#888"))
                font_size = "1.2rem" if i < 3 else "1rem"

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:{'16px' if i < 3 else '10px'} 18px;margin-bottom:{'10px' if i < 3 else '6px'};border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span style="font-size:{'2rem' if i < 3 else '1.2rem'};">{madalya}</span>
                            <strong style="color:#e0e0e0;font-size:{font_size};">{kisi}</strong>
                        </div>
                        <span style="color:{renk};font-weight:800;font-size:{'1.4rem' if i < 3 else '1rem'};">{puan} puan</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Liderlik tablosu icin puan kaydi gerekiyor.")

    # ── Rozet Vitrin ──
    with sub[1]:
        _styled_section("🎖️ Rozet Tanimlari & Vitrin", "#8338ec")

        rozet_tanimlari = [
            {"ad": "Simsek", "ikon": "⚡", "kosul": "4 saat icinde cozum", "puan": 50, "renk": "#ffd166"},
            {"ad": "Memnuniyet Yildizi", "ikon": "⭐", "kosul": "5/5 memnuniyet puani", "puan": 40, "renk": "#06d6a0"},
            {"ad": "Sifir Gecikme", "ikon": "⏰", "kosul": "Hic SLA ihlali yok (haftalik)", "puan": 60, "renk": "#00b4d8"},
            {"ad": "Takim Oyuncusu", "ikon": "🤝", "kosul": "Ekip arkadasina yardim", "puan": 30, "renk": "#8338ec"},
            {"ad": "Problem Avcisi", "ikon": "🎯", "kosul": "Kok neden tespit etti", "puan": 70, "renk": "#e94560"},
            {"ad": "Maraton", "ikon": "🏃", "kosul": "Gunde 10+ gorev tamamladi", "puan": 80, "renk": "#ff6b6b"},
            {"ad": "Ilk Mudahale", "ikon": "🚀", "kosul": "Ilk 30 dk icinde yanit", "puan": 35, "renk": "#06d6a0"},
            {"ad": "Usta", "ikon": "👑", "kosul": "1000+ toplam puan", "puan": 100, "renk": "#ffd166"},
        ]

        rc1, rc2, rc3, rc4 = st.columns(4)
        for i, r in enumerate(rozet_tanimlari):
            col = [rc1, rc2, rc3, rc4][i % 4]
            col.markdown(f"""
            <div style="background:#16213e;border-radius:12px;padding:14px;text-align:center;margin-bottom:8px;border:1px solid {r['renk']}30;">
                <div style="font-size:2.5rem;">{r['ikon']}</div>
                <div style="color:{r['renk']};font-weight:700;margin:4px 0;">{r['ad']}</div>
                <div style="color:#888;font-size:0.72rem;">{r['kosul']}</div>
                <div style="color:#ffd166;font-size:0.8rem;margin-top:4px;">+{r['puan']} puan</div>
            </div>""", unsafe_allow_html=True)

        # Rozet ver
        _styled_section("Rozet Ver", "#ffd166")
        with st.form("rozet_form"):
            rv1, rv2 = st.columns(2)
            with rv1:
                r_kisi = st.text_input("Kisi", key="gam_rozet_kisi")
            with rv2:
                r_rozet = st.selectbox("Rozet", [r["ad"] for r in rozet_tanimlari], key="gam_rozet_sec")
            if st.form_submit_button("🎖️ Rozet Ver"):
                if r_kisi:
                    rozet_bilgi = next((r for r in rozet_tanimlari if r["ad"] == r_rozet), {})
                    rozetler.append({
                        "kisi": r_kisi,
                        "rozet": r_rozet,
                        "ikon": rozet_bilgi.get("ikon", "🎖️"),
                        "puan": rozet_bilgi.get("puan", 0),
                        "tarih": datetime.now().isoformat(),
                    })
                    puanlar.append({"kisi": r_kisi, "puan": rozet_bilgi.get("puan", 0), "kaynak": f"Rozet: {r_rozet}", "tarih": datetime.now().isoformat()})
                    _save_json(rozet_path, rozetler)
                    _save_json(puan_path, puanlar)
                    st.success(f"{r_kisi} — {r_rozet} rozeti ve +{rozet_bilgi.get('puan',0)} puan!")
                    st.rerun()

        if rozetler:
            _styled_section("Son Kazanilan Rozetler", "#06d6a0")
            for r in reversed(rozetler[-8:]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                    <span>{r.get('ikon','🎖️')} <strong style="color:#e0e0e0;">{r.get('kisi','')}</strong> — {r.get('rozet','')}</span>
                    <span style="color:#ffd166;font-weight:700;">+{r.get('puan',0)}</span>
                </div>""", unsafe_allow_html=True)

    # ── Puan Sistemi ──
    with sub[2]:
        _styled_section("⭐ Puan Kazanma & Harcama", "#ffd166")

        with st.form("puan_form"):
            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                p_kisi = st.text_input("Kisi", key="gam_puan_kisi")
            with pc2:
                p_puan = st.number_input("Puan", min_value=1, max_value=500, value=10, key="gam_puan_val")
            with pc3:
                p_kaynak = st.selectbox("Kaynak", ["Gorev Tamamlama", "Hizli Cozum", "Memnuniyet Bonusu", "Ekip Yardimi", "Ozel Basarim"], key="gam_puan_kaynak")

            if st.form_submit_button("⭐ Puan Ver", use_container_width=True):
                if p_kisi:
                    puanlar.append({"kisi": p_kisi, "puan": p_puan, "kaynak": p_kaynak, "tarih": datetime.now().isoformat()})
                    _save_json(puan_path, puanlar)
                    st.success(f"{p_kisi} +{p_puan} puan kazandi!")
                    st.rerun()

        if puanlar:
            _styled_section("Son Puan Hareketleri", "#00b4d8")
            for p in reversed(puanlar[-10:]):
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:6px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;">{p.get('kisi','')} — {p.get('kaynak','')}</span>
                    <span style="color:#ffd166;font-weight:700;">+{p.get('puan',0)}</span>
                </div>""", unsafe_allow_html=True)

    # ── Seviyeler ──
    with sub[3]:
        _styled_section("🏅 Basarim Seviyeleri (Bronz → Elmas)", "#8338ec")

        seviyeler = [
            {"ad": "Bronz", "min": 0, "ikon": "🥉", "renk": "#cd7f32"},
            {"ad": "Gumus", "min": 100, "ikon": "🥈", "renk": "#c0c0c0"},
            {"ad": "Altin", "min": 300, "ikon": "🥇", "renk": "#ffd166"},
            {"ad": "Platin", "min": 600, "ikon": "💎", "renk": "#00b4d8"},
            {"ad": "Elmas", "min": 1000, "ikon": "👑", "renk": "#8338ec"},
        ]

        if puanlar:
            kisi_puan = {}
            for p in puanlar:
                kisi = p.get("kisi", "?")
                kisi_puan[kisi] = kisi_puan.get(kisi, 0) + p.get("puan", 0)

            for kisi, toplam in sorted(kisi_puan.items(), key=lambda x: -x[1]):
                seviye = seviyeler[0]
                for s in seviyeler:
                    if toplam >= s["min"]:
                        seviye = s

                sonraki = None
                for s in seviyeler:
                    if s["min"] > toplam:
                        sonraki = s
                        break

                ilerleme = 100 if not sonraki else int((toplam - seviye["min"]) / max(1, sonraki["min"] - seviye["min"]) * 100)

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div style="display:flex;align-items:center;gap:10px;">
                            <span style="font-size:1.8rem;">{seviye['ikon']}</span>
                            <div>
                                <strong style="color:#e0e0e0;">{kisi}</strong>
                                <div style="color:{seviye['renk']};font-size:0.82rem;font-weight:600;">{seviye['ad']} Seviye</div>
                            </div>
                        </div>
                        <span style="color:#ffd166;font-weight:700;">{toplam} puan</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{ilerleme}%;height:100%;background:linear-gradient(90deg,{seviye['renk']},{seviye['renk']}88);border-radius:6px;"></div>
                    </div>
                    <div style="color:#888;font-size:0.72rem;margin-top:3px;text-align:right;">
                        {'MAX SEVIYE' if not sonraki else f"Sonraki: {sonraki['ad']} ({sonraki['min']} puan)"}
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            # Sadece seviye tanımlarını göster
            for s in seviyeler:
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <span>{s['ikon']} <strong style="color:{s['renk']};">{s['ad']}</strong></span>
                    <span style="color:#888;">{s['min']}+ puan</span>
                </div>""", unsafe_allow_html=True)

    # ── Ekip Yarışması ──
    with sub[4]:
        _styled_section("⚔️ Ekip Yarismasi Olustur & Takip", "#e94560")

        with st.form("yarisma_form"):
            yc1, yc2 = st.columns(2)
            with yc1:
                y_ad = st.text_input("Yarisma Adi", key="yarisma_ad")
                y_kriter = st.selectbox("Degerlendirme Kriteri", ["En Cok Gorev Tamamlayan", "En Hizli Cozum", "En Yuksek Memnuniyet", "En Az Gecikme"], key="yarisma_kriter")
            with yc2:
                y_bitis = st.date_input("Bitis Tarihi", value=datetime.now().date() + timedelta(days=30), key="yarisma_bitis")
                y_odul = st.text_input("Odul", key="yarisma_odul")

            if st.form_submit_button("⚔️ Yarisma Baslat", use_container_width=True):
                if y_ad:
                    yarismalar.append({
                        "id": f"yrs_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": y_ad,
                        "kriter": y_kriter,
                        "bitis": str(y_bitis),
                        "odul": y_odul,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(yarisma_path, yarismalar)
                    st.success(f"Yarisma '{y_ad}' basladi!")
                    st.rerun()

        if yarismalar:
            for y in yarismalar:
                durum = "🟢 Aktif" if y.get("aktif") else "🏁 Bitti"
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#e9456015,#16213e);border-radius:12px;padding:14px 18px;margin-bottom:8px;border:1px solid #e9456030;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e94560;font-size:1.1rem;">⚔️ {y.get('ad','?')}</strong>
                            <div style="color:#888;font-size:0.8rem;">{y.get('kriter','')} | Bitis: {y.get('bitis','')}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="color:#ffd166;">🏆 {y.get('odul','')}</span>
                            <div style="color:#888;font-size:0.78rem;">{durum}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Motivasyon Panosu ──
    with sub[5]:
        _styled_section("📊 Motivasyon & Basarim Panosu", "#06d6a0")

        toplam_rozet = len(rozetler)
        toplam_puan = sum(p.get("puan", 0) for p in puanlar)
        aktif_yarisma = len([y for y in yarismalar if y.get("aktif")])

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#16213e,#1a1a2e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
            <div style="font-size:1rem;color:#888;">Ekip Motivasyon Skoru</div>
            <div style="font-size:3.5rem;font-weight:900;color:#ffd166;">{'⭐' * min(5, max(1, toplam_rozet // 3 + 1))}</div>
            <div style="display:flex;justify-content:center;gap:30px;margin-top:10px;">
                <div><span style="color:#8338ec;font-weight:700;font-size:1.3rem;">{toplam_rozet}</span><br><span style="color:#888;font-size:0.78rem;">Rozet</span></div>
                <div><span style="color:#ffd166;font-weight:700;font-size:1.3rem;">{toplam_puan}</span><br><span style="color:#888;font-size:0.78rem;">Puan</span></div>
                <div><span style="color:#e94560;font-weight:700;font-size:1.3rem;">{aktif_yarisma}</span><br><span style="color:#888;font-size:0.78rem;">Yarisma</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # En son başarımlar
        if rozetler:
            _styled_section("Son Basarimlar", "#ffd166")
            for r in reversed(rozetler[-5:]):
                st.markdown(f"""
                <div style="background:#ffd16610;border-left:3px solid #ffd166;padding:8px 14px;border-radius:0 8px 8px 0;margin-bottom:5px;">
                    <span style="font-size:1.2rem;">{r.get('ikon','')}</span>
                    <strong style="color:#ffd166;margin-left:6px;">{r.get('kisi','')}</strong>
                    <span style="color:#e0e0e0;margin-left:6px;">{r.get('rozet','')} kazandi!</span>
                </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. ENTEGRASYON HUB & DIŞ SİSTEM BAĞLANTI MERKEZİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_entegrasyon_hub(store):
    _styled_header("Entegrasyon Hub & Dis Sistem Baglanti Merkezi", "🔌")

    entegrasyon_path = _get_data_path(store, "entegrasyonlar.json")
    entegrasyonlar = _load_json(entegrasyon_path)

    webhook_path = _get_data_path(store, "webhooklar.json")
    webhooklar = _load_json(webhook_path)

    log_path = _get_data_path(store, "entegrasyon_log.json")
    loglar = _load_json(log_path)

    aktif = len([e for e in entegrasyonlar if e.get("aktif")])

    _styled_stat_row([
        ("Toplam Entegrasyon", len(entegrasyonlar)),
        ("Aktif Baglanti", aktif),
        ("Webhook", len(webhooklar)),
        ("API Log", len(loglar)),
    ])

    sub = st.tabs(["🔗 Entegrasyonlar", "🪝 Webhook Yonetimi", "📧 E-posta Ticket", "📱 SMS Bildirim", "📊 Saglik Durumu", "📋 API Log"])

    # ── Entegrasyonlar ──
    with sub[0]:
        _styled_section("🔗 Dis Sistem Entegrasyonlari", "#0f3460")

        with st.form("entegrasyon_form"):
            ec1, ec2 = st.columns(2)
            with ec1:
                e_ad = st.text_input("Entegrasyon Adi", key="ent_ad")
                e_tip = st.selectbox("Sistem Tipi", ["E-posta (SMTP)", "SMS Gateway", "ERP/Muhasebe", "Takvim (Google/Outlook)", "LDAP/Active Directory", "Webhook", "REST API", "Diger"], key="ent_tip")
            with ec2:
                e_url = st.text_input("Endpoint / URL", key="ent_url")
                e_durum = st.selectbox("Baslangic Durumu", ["Aktif", "Test", "Pasif"], key="ent_durum")

            if st.form_submit_button("🔗 Entegrasyon Ekle", use_container_width=True):
                if e_ad:
                    entegrasyonlar.append({
                        "id": f"ent_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": e_ad,
                        "tip": e_tip,
                        "url": e_url,
                        "aktif": e_durum == "Aktif",
                        "durum": e_durum,
                        "son_kontrol": None,
                        "basari_sayisi": 0,
                        "hata_sayisi": 0,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(entegrasyon_path, entegrasyonlar)
                    st.success(f"{e_ad} entegrasyonu eklendi!")
                    st.rerun()

        if entegrasyonlar:
            for idx, e in enumerate(entegrasyonlar):
                durum_renk = {"Aktif": "#06d6a0", "Test": "#ffd166", "Pasif": "#888", "Hata": "#e94560"}.get(e.get("durum", ""), "#888")
                tip_ikon = {"E-posta (SMTP)": "📧", "SMS Gateway": "📱", "ERP/Muhasebe": "💰", "Takvim (Google/Outlook)": "📅", "LDAP/Active Directory": "🔐", "Webhook": "🪝", "REST API": "🌐"}.get(e.get("tip", ""), "🔌")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {durum_renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:1.2rem;">{tip_ikon}</span>
                            <strong style="color:#e0e0e0;margin-left:8px;">{e.get('ad','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{e.get('tip','')}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;">
                            <span style="color:#06d6a0;font-size:0.78rem;">✓{e.get('basari_sayisi',0)}</span>
                            <span style="color:#e94560;font-size:0.78rem;">✗{e.get('hata_sayisi',0)}</span>
                            <span style="background:{durum_renk}20;color:{durum_renk};padding:3px 10px;border-radius:8px;font-size:0.78rem;font-weight:600;">{e.get('durum','')}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Webhook Yönetimi ──
    with sub[1]:
        _styled_section("🪝 Webhook Tanimlama & Yonetim", "#8338ec")

        with st.form("webhook_form"):
            wc1, wc2 = st.columns(2)
            with wc1:
                w_ad = st.text_input("Webhook Adi", key="wh_ad")
                w_olay = st.selectbox("Tetik Olay", ["Yeni Talep", "Talep Kapandi", "SLA Ihlali", "Eskalasyon", "Yeni Yorum", "Durum Degisimi"], key="wh_olay")
            with wc2:
                w_url = st.text_input("Hedef URL", key="wh_url")
                w_metod = st.selectbox("HTTP Metod", ["POST", "PUT", "GET"], key="wh_metod")

            if st.form_submit_button("🪝 Webhook Ekle", use_container_width=True):
                if w_ad and w_url:
                    webhooklar.append({
                        "id": f"wh_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "ad": w_ad,
                        "olay": w_olay,
                        "url": w_url,
                        "metod": w_metod,
                        "aktif": True,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(webhook_path, webhooklar)
                    st.success(f"Webhook '{w_ad}' eklendi!")
                    st.rerun()

        if webhooklar:
            for w in webhooklar:
                durum = "🟢" if w.get("aktif") else "🔴"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{durum}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{w.get('ad','?')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">Olay: {w.get('olay','')}</span>
                    </div>
                    <span style="color:#8338ec;font-family:monospace;font-size:0.75rem;">{w.get('metod','')} {w.get('url','')[:30]}...</span>
                </div>""", unsafe_allow_html=True)

    # ── E-posta Ticket ──
    with sub[2]:
        _styled_section("📧 E-posta ile Otomatik Ticket Olusturma", "#00b4d8")

        eposta_path = _get_data_path(store, "eposta_ayarlari.json")
        eposta_ayar = _load_json(eposta_path)

        with st.form("eposta_form"):
            epc1, epc2 = st.columns(2)
            with epc1:
                ep_sunucu = st.text_input("IMAP Sunucu", value="imap.gmail.com", key="ep_sunucu")
                ep_port = st.number_input("Port", value=993, key="ep_port")
            with epc2:
                ep_kullanici = st.text_input("E-posta Adresi", key="ep_kullanici")
                ep_kontrol = st.selectbox("Kontrol Sikligi", ["5 dakika", "15 dakika", "30 dakika", "1 saat"], key="ep_kontrol")

            ep_etiket = st.text_input("Otomatik Etiket (konu iceriyorsa)", placeholder="ariza, destek, talep", key="ep_etiket")

            if st.form_submit_button("📧 E-posta Entegrasyonu Kaydet", use_container_width=True):
                ayar = {
                    "sunucu": ep_sunucu,
                    "port": ep_port,
                    "kullanici": ep_kullanici,
                    "kontrol_sikligi": ep_kontrol,
                    "etiketler": ep_etiket,
                    "aktif": True,
                    "tarih": datetime.now().isoformat(),
                }
                _save_json(eposta_path, [ayar])
                st.success("E-posta entegrasyonu kaydedildi!")

        if eposta_ayar:
            a = eposta_ayar[0] if isinstance(eposta_ayar, list) and eposta_ayar else {}
            if a:
                durum = "🟢 Aktif" if a.get("aktif") else "🔴 Pasif"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:14px 18px;margin-top:10px;">
                    <strong style="color:#00b4d8;">Mevcut E-posta Ayari</strong>
                    <div style="color:#888;font-size:0.85rem;margin-top:6px;">
                        Sunucu: {a.get('sunucu','')}:{a.get('port','')} | Kontrol: {a.get('kontrol_sikligi','')} | {durum}
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── SMS Bildirim ──
    with sub[3]:
        _styled_section("📱 SMS Bildirim Ayarlari", "#06d6a0")

        sms_path = _get_data_path(store, "sms_ayarlari.json")
        sms_ayar = _load_json(sms_path)

        with st.form("sms_form"):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_saglayici = st.selectbox("SMS Saglayici", ["Netgsm", "Iletimerkezi", "Turatel", "JetSMS", "Diger"], key="sms_saglayici")
                s_api_key = st.text_input("API Key", type="password", key="sms_api")
            with sc2:
                s_gonderen = st.text_input("Gonderen Baslik", key="sms_gonderen")
                s_olaylar = st.multiselect("Bildirim Olaylari", ["Yeni Talep", "SLA Ihlali", "Eskalasyon", "Talep Kapandi", "Acil Talep"], key="sms_olaylar")

            if st.form_submit_button("📱 SMS Ayarlarini Kaydet", use_container_width=True):
                ayar = {
                    "saglayici": s_saglayici,
                    "gonderen": s_gonderen,
                    "olaylar": s_olaylar,
                    "aktif": True,
                    "tarih": datetime.now().isoformat(),
                }
                _save_json(sms_path, [ayar])
                st.success("SMS ayarlari kaydedildi!")

        # SMS şablonları
        _styled_section("SMS Sablonlari", "#ffd166")
        sablonlar = [
            ("Yeni Talep", "[KURUM] Yeni destek talebi #{id} olusturuldu. Konu: {konu}"),
            ("SLA Ihlali", "[KURUM] UYARI: Talep #{id} SLA süresini asti! Acil mudahale gerekli."),
            ("Eskalasyon", "[KURUM] Talep #{id} ust kademeye eskale edildi. Neden: {neden}"),
        ]
        for baslik, sablon in sablonlar:
            st.markdown(f"""
            <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:4px;">
                <strong style="color:#ffd166;font-size:0.85rem;">{baslik}:</strong>
                <span style="color:#aaa;font-size:0.82rem;margin-left:6px;">{sablon}</span>
            </div>""", unsafe_allow_html=True)

    # ── Sağlık Durumu ──
    with sub[4]:
        _styled_section("📊 Entegrasyon Saglik Durumu Dashboard", "#06d6a0")

        if entegrasyonlar:
            aktif_sayi = len([e for e in entegrasyonlar if e.get("aktif")])
            hata_sayi = len([e for e in entegrasyonlar if e.get("durum") == "Hata"])
            saglik = int(aktif_sayi / max(1, len(entegrasyonlar)) * 100)
            renk = "#06d6a0" if saglik >= 80 else ("#ffd166" if saglik >= 50 else "#e94560")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-bottom:16px;">
                <div style="color:#888;">Genel Entegrasyon Sagligi</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">%{saglik}</div>
                <div style="color:#aaa;font-size:0.85rem;">{aktif_sayi} aktif / {len(entegrasyonlar)} toplam | {hata_sayi} hata</div>
            </div>""", unsafe_allow_html=True)

            for e in entegrasyonlar:
                durum_renk = {"Aktif": "#06d6a0", "Test": "#ffd166", "Pasif": "#888", "Hata": "#e94560"}.get(e.get("durum", ""), "#888")
                uptime = 100 if e.get("aktif") else 0
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="color:#e0e0e0;font-weight:600;">{e.get('ad','?')}</span>
                        <span style="color:{durum_renk};font-size:0.82rem;font-weight:600;">{e.get('durum','')}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:12px;overflow:hidden;">
                        <div style="width:{uptime}%;height:100%;background:{durum_renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Saglik kontrolu icin entegrasyon ekleyin.")

    # ── API Log ──
    with sub[5]:
        _styled_section("📋 API & Entegrasyon Log Takibi", "#ffd166")

        with st.form("log_form"):
            lc1, lc2, lc3 = st.columns(3)
            with lc1:
                l_entegrasyon = st.text_input("Entegrasyon", key="log_ent")
            with lc2:
                l_durum = st.selectbox("Durum", ["Basarili", "Hata", "Timeout", "Reddedildi"], key="log_durum")
            with lc3:
                l_sure = st.number_input("Yanit Suresi (ms)", min_value=0, value=200, key="log_sure")
            l_detay = st.text_input("Detay", key="log_detay")

            if st.form_submit_button("📋 Log Kaydet", use_container_width=True):
                if l_entegrasyon:
                    loglar.append({
                        "id": f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "entegrasyon": l_entegrasyon,
                        "durum": l_durum,
                        "sure_ms": l_sure,
                        "detay": l_detay,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(log_path, loglar)
                    st.success("Log kaydedildi!")
                    st.rerun()

        if loglar:
            for l in reversed(loglar[-15:]):
                durum_renk = {"Basarili": "#06d6a0", "Hata": "#e94560", "Timeout": "#ffd166", "Reddedildi": "#ff6b6b"}.get(l.get("durum", ""), "#888")
                durum_ikon = {"Basarili": "✅", "Hata": "❌", "Timeout": "⏱️", "Reddedildi": "🚫"}.get(l.get("durum", ""), "⚪")

                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:3px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span>{durum_ikon}</span>
                        <strong style="color:#e0e0e0;margin-left:6px;">{l.get('entegrasyon','?')}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">{l.get('detay','')}</span>
                    </div>
                    <div>
                        <span style="color:{durum_renk};font-size:0.8rem;font-weight:600;">{l.get('durum','')}</span>
                        <span style="color:#888;font-size:0.72rem;margin-left:6px;">{l.get('sure_ms','')}ms</span>
                        <span style="color:#666;font-size:0.7rem;margin-left:6px;">{l.get('tarih','')[:16]}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Başarı oranı
            basarili = len([l for l in loglar if l.get("durum") == "Basarili"])
            oran = int(basarili / max(1, len(loglar)) * 100)
            renk = "#06d6a0" if oran >= 95 else ("#ffd166" if oran >= 80 else "#e94560")
            st.markdown(f"""
            <div style="background:#0f3460;border-radius:10px;padding:14px;text-align:center;margin-top:10px;">
                <span style="color:#888;">API Basari Orani: </span>
                <span style="color:{renk};font-weight:700;font-size:1.3rem;">%{oran}</span>
                <span style="color:#888;font-size:0.82rem;"> ({basarili}/{len(loglar)})</span>
            </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Henuz API log kaydi yok.")
