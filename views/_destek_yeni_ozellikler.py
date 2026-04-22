"""
Destek Hizmetleri - Yeni Özellikler
1. SLA Performans Cockpit & Analitik
2. Bina & Tesis Haritası (Lokasyon Bazlı Yönetim)
3. Memnuniyet & Kalite Endeksi
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import Counter


# ── Ortak stil yardımcıları ──
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  1. SLA PERFORMANS COCKPİT & ANALİTİK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_sla_cockpit(store):
    _styled_header("SLA Performans Cockpit & Analitik", "📊")

    # Ticket verilerini yükle
    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    # SLA ayarlarını yükle
    try:
        sla_ayarlar = store.load_list("sla_ayarlar") or []
    except Exception:
        sla_ayarlar = []

    # Metrikleri hesapla
    toplam = len(tickets)
    kapali = [t for t in tickets if _get_attr(t, "durum") in ("kapali", "cozuldu", "closed", "resolved")]
    acik = [t for t in tickets if _get_attr(t, "durum") in ("acik", "open", "beklemede", "islemde", "atandi")]
    geciken_list = []
    cozum_sureleri = []

    bugun = datetime.now()
    for t in tickets:
        # Gecikme kontrolü
        olusturma = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih")
        kapanma = _get_attr(t, "kapanma_tarihi") or _get_attr(t, "closed_at")

        if olusturma:
            try:
                olusturma_dt = _parse_date(olusturma)
                if kapanma:
                    kapanma_dt = _parse_date(kapanma)
                    fark = (kapanma_dt - olusturma_dt).total_seconds() / 3600
                    cozum_sureleri.append(fark)
                else:
                    gecen = (bugun - olusturma_dt).total_seconds() / 3600
                    if gecen > 48:
                        geciken_list.append(t)
            except Exception:
                pass

    ort_cozum = sum(cozum_sureleri) / len(cozum_sureleri) if cozum_sureleri else 0
    sla_uyum = int(len(kapali) / max(1, toplam) * 100)

    _styled_stat_row([
        ("Toplam Talep", toplam),
        ("Acik Talep", len(acik)),
        ("Kapali Talep", len(kapali)),
        ("Geciken Talep", len(geciken_list)),
        ("Ort. Cozum (saat)", f"{ort_cozum:.1f}"),
        ("SLA Uyum", f"%{sla_uyum}"),
    ])

    sub = st.tabs(["📊 Canli Metrikler", "🏢 Departman Karnesi", "📈 Trend Analizi", "⏰ Geciken Talepler", "🎯 SLA Hedef Takip", "🔔 Alarm Sistemi"])

    # ── Canlı Metrikler ──
    with sub[0]:
        _styled_section("📊 Canli SLA Metrikleri", "#00b4d8")

        # Durum dağılımı
        durum_sayim = Counter(_get_attr(t, "durum") or "belirsiz" for t in tickets)
        if durum_sayim:
            st.markdown("**Talep Durum Dagilimi**")
            durum_renkler = {"acik": "#e94560", "open": "#e94560", "beklemede": "#ffd166", "islemde": "#00b4d8", "atandi": "#8338ec", "kapali": "#06d6a0", "closed": "#06d6a0", "cozuldu": "#06d6a0", "resolved": "#06d6a0"}
            max_val = max(durum_sayim.values()) if durum_sayim.values() else 1
            for durum, sayi in sorted(durum_sayim.items(), key=lambda x: -x[1]):
                renk = durum_renkler.get(durum, "#888")
                bar_w = int(sayi / max_val * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:120px;color:#e0e0e0;font-weight:600;text-transform:capitalize;">{durum}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

        # Öncelik dağılımı
        oncelik_sayim = Counter(_get_attr(t, "oncelik") or _get_attr(t, "priority") or "normal" for t in tickets)
        if oncelik_sayim:
            _styled_section("Oncelik Dagilimi", "#ffd166")
            oncelik_renkler = {"acil": "#e94560", "critical": "#e94560", "yuksek": "#ff6b6b", "high": "#ff6b6b", "normal": "#ffd166", "dusuk": "#06d6a0", "low": "#06d6a0"}
            for oncelik, sayi in sorted(oncelik_sayim.items(), key=lambda x: -x[1]):
                renk = oncelik_renkler.get(oncelik, "#888")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:8px 14px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;">
                    <span style="color:{renk};font-weight:600;text-transform:capitalize;">{oncelik}</span>
                    <span style="color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

        # Çözüm süresi dağılımı
        if cozum_sureleri:
            _styled_section("Cozum Suresi Dagilimi", "#8338ec")
            hizli = len([s for s in cozum_sureleri if s <= 4])
            orta = len([s for s in cozum_sureleri if 4 < s <= 24])
            yavas = len([s for s in cozum_sureleri if 24 < s <= 72])
            cok_yavas = len([s for s in cozum_sureleri if s > 72])

            for etiket, sayi, renk in [("0-4 saat (Hizli)", hizli, "#06d6a0"), ("4-24 saat (Normal)", orta, "#ffd166"), ("1-3 gun (Yavas)", yavas, "#ff6b6b"), ("3+ gun (Kritik)", cok_yavas, "#e94560")]:
                bar_w = int(sayi / max(1, len(cozum_sureleri)) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:160px;color:#e0e0e0;font-size:0.88rem;">{etiket}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)

    # ── Departman Karnesi ──
    with sub[1]:
        _styled_section("🏢 Departman / Hizmet Alani Performans Karnesi", "#0f3460")

        alan_sayim = Counter(_get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or "Diger" for t in tickets)
        if alan_sayim:
            for alan, sayi in sorted(alan_sayim.items(), key=lambda x: -x[1]):
                alan_tickets = [t for t in tickets if (_get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or "Diger") == alan]
                alan_kapali = [t for t in alan_tickets if _get_attr(t, "durum") in ("kapali", "cozuldu", "closed", "resolved")]
                alan_acik = len(alan_tickets) - len(alan_kapali)
                cozum_oran = int(len(alan_kapali) / max(1, len(alan_tickets)) * 100)
                renk = "#06d6a0" if cozum_oran >= 80 else ("#ffd166" if cozum_oran >= 50 else "#e94560")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:10px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <h4 style="color:#e0e0e0;margin:0;">{alan}</h4>
                            <span style="color:#888;font-size:0.8rem;">Toplam: {sayi} | Acik: {alan_acik} | Kapali: {len(alan_kapali)}</span>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.6rem;font-weight:800;color:{renk};">%{cozum_oran}</div>
                            <div style="color:#888;font-size:0.75rem;">Cozum Orani</div>
                        </div>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;margin-top:8px;">
                        <div style="width:{cozum_oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Departman karnesi icin talep verisi gerekiyor.")

    # ── Trend Analizi ──
    with sub[2]:
        _styled_section("📈 Aylik Talep Trend Analizi", "#8338ec")

        if tickets:
            aylik = {}
            for t in tickets:
                tarih = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""
                ay = str(tarih)[:7]
                if ay and len(ay) >= 7:
                    aylik[ay] = aylik.get(ay, 0) + 1

            if aylik:
                max_val = max(aylik.values())
                for ay in sorted(aylik.keys()):
                    val = aylik[ay]
                    bar_w = int(val / max_val * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <span style="width:80px;color:#888;font-size:0.85rem;">{ay}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#8338ec,#00b4d8);border-radius:6px;"></div>
                        </div>
                        <span style="width:40px;text-align:right;color:#8338ec;font-weight:700;">{val}</span>
                    </div>""", unsafe_allow_html=True)

                # Trend yönü
                aylar = sorted(aylik.keys())
                if len(aylar) >= 2:
                    son = aylik[aylar[-1]]
                    onceki = aylik[aylar[-2]]
                    degisim = son - onceki
                    yon = "yukseldi" if degisim > 0 else ("dususte" if degisim < 0 else "ayni")
                    renk = "#e94560" if degisim > 0 else "#06d6a0"
                    st.markdown(f"""
                    <div style="background:#0f3460;border-radius:10px;padding:14px;text-align:center;margin-top:10px;">
                        <span style="color:#888;">Son ay degisim: </span>
                        <span style="color:{renk};font-weight:700;font-size:1.2rem;">{degisim:+d} talep ({yon})</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Trend analizi icin talep verisi gerekiyor.")

    # ── Geciken Talepler ──
    with sub[3]:
        _styled_section("⏰ Geciken & Kritik Talepler", "#e94560")

        if geciken_list:
            st.error(f"🚨 {len(geciken_list)} talep 48+ saattir acik!")
            for idx, t in enumerate(geciken_list[:20]):
                olusturma = _get_attr(t, "olusturma_tarihi") or _get_attr(t, "created_at") or _get_attr(t, "tarih") or ""
                baslik = _get_attr(t, "baslik") or _get_attr(t, "konu") or _get_attr(t, "title") or "Baslik yok"
                oncelik = _get_attr(t, "oncelik") or _get_attr(t, "priority") or "normal"
                alan = _get_attr(t, "hizmet_alani") or _get_attr(t, "alan") or ""

                try:
                    olusturma_dt = _parse_date(olusturma)
                    gecen_saat = (bugun - olusturma_dt).total_seconds() / 3600
                except Exception:
                    gecen_saat = 0

                renk = "#e94560" if gecen_saat > 168 else ("#ff6b6b" if gecen_saat > 72 else "#ffd166")
                st.markdown(f"""
                <div style="background:{renk}12;border-left:4px solid {renk};padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:{renk};">{baslik[:50]}</strong>
                            <div style="color:#888;font-size:0.8rem;margin-top:2px;">{alan} | Oncelik: {oncelik}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="color:{renk};font-weight:700;font-size:1.1rem;">{gecen_saat:.0f} saat</div>
                            <div style="color:#888;font-size:0.75rem;">bekliyor</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Geciken talep bulunmuyor. Tum talepler SLA icerisinde. ✅")

    # ── SLA Hedef Takip ──
    with sub[4]:
        _styled_section("🎯 SLA Hedef & Performans Takibi", "#06d6a0")

        sla_hedef_path = _get_data_path(store, "sla_hedefler.json")
        hedefler = _load_json(sla_hedef_path)

        with st.form("sla_hedef_form"):
            hc1, hc2, hc3 = st.columns(3)
            with hc1:
                h_metrik = st.selectbox("Metrik", ["Cozum Suresi (saat)", "Ilk Yanit (saat)", "SLA Uyum (%)", "Memnuniyet (%)"], key="sla_metrik")
            with hc2:
                h_hedef = st.number_input("Hedef Deger", min_value=0.0, value=24.0, step=1.0, key="sla_hedef_val")
            with hc3:
                h_alan = st.text_input("Hizmet Alani (bos = genel)", key="sla_alan")

            if st.form_submit_button("🎯 Hedef Belirle", use_container_width=True):
                hedefler.append({
                    "id": f"slah_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "metrik": h_metrik,
                    "hedef": h_hedef,
                    "alan": h_alan or "Genel",
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(sla_hedef_path, hedefler)
                st.success("SLA hedefi belirlendi!")
                st.rerun()

        if hedefler:
            for h in hedefler:
                metrik = h.get("metrik", "")
                hedef_val = h.get("hedef", 0)

                # Mevcut performansı hesapla
                if "Cozum" in metrik:
                    mevcut = ort_cozum
                elif "Uyum" in metrik:
                    mevcut = sla_uyum
                else:
                    mevcut = 0

                if "%" in metrik:
                    oran = min(100, int(mevcut / max(1, hedef_val) * 100))
                    basarili = mevcut >= hedef_val
                else:
                    oran = min(100, int((1 - mevcut / max(1, hedef_val)) * 100)) if mevcut <= hedef_val else 0
                    basarili = mevcut <= hedef_val

                renk = "#06d6a0" if basarili else "#e94560"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                        <div>
                            <strong style="color:#e0e0e0;">{metrik}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">({h.get('alan','')})</span>
                        </div>
                        <span style="color:{renk};font-weight:700;">{'✅ Basarili' if basarili else '❌ Hedef altinda'}</span>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:16px;overflow:hidden;">
                        <div style="width:{oran}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-top:4px;">
                        <span style="color:#888;font-size:0.78rem;">Mevcut: {mevcut:.1f}</span>
                        <span style="color:#888;font-size:0.78rem;">Hedef: {hedef_val}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Alarm Sistemi ──
    with sub[5]:
        _styled_section("🔔 SLA Alarm & Bildirim Sistemi", "#ff6b6b")

        alarm_path = _get_data_path(store, "sla_alarmlar.json")
        alarmlar = _load_json(alarm_path)

        with st.form("sla_alarm_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                a_kosul = st.selectbox("Alarm Kosulu", [
                    "Talep 24 saat acik kaldı",
                    "Talep 48 saat acik kaldı",
                    "Acil talep 4 saat icinde cevaplanmadı",
                    "SLA uyum %80 altına dustu",
                    "Gunluk yeni talep 10+ oldu",
                ], key="alarm_kosul")
            with ac2:
                a_bildirim = st.selectbox("Bildirim Turu", ["Ekran Uyarisi", "E-posta", "SMS", "Tumu"], key="alarm_bildirim")

            if st.form_submit_button("🔔 Alarm Ekle", use_container_width=True):
                alarmlar.append({
                    "id": f"alr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "kosul": a_kosul,
                    "bildirim": a_bildirim,
                    "aktif": True,
                    "tarih": datetime.now().isoformat(),
                })
                _save_json(alarm_path, alarmlar)
                st.success("Alarm kuruldu!")
                st.rerun()

        if alarmlar:
            for idx, a in enumerate(alarmlar):
                durum = "🟢 Aktif" if a.get("aktif") else "⚫ Pasif"
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{a.get('kosul','')}</strong>
                        <span style="color:#888;font-size:0.8rem;margin-left:8px;">({a.get('bildirim','')})</span>
                    </div>
                    <span style="color:#888;font-size:0.82rem;">{durum}</span>
                </div>""", unsafe_allow_html=True)
                if a.get("aktif"):
                    if st.button("Kapat", key=f"alarm_kapat_{idx}"):
                        a["aktif"] = False
                        _save_json(alarm_path, alarmlar)
                        st.rerun()

        # Otomatik alarm kontrolü
        otomatik_uyarilar = []
        if len(geciken_list) > 0:
            otomatik_uyarilar.append(f"⏰ {len(geciken_list)} talep 48+ saattir acik")
        if sla_uyum < 80:
            otomatik_uyarilar.append(f"📉 SLA uyum orani %{sla_uyum} — hedefin altinda")
        if len(acik) > 20:
            otomatik_uyarilar.append(f"📊 {len(acik)} acik talep birikti")

        if otomatik_uyarilar:
            _styled_section("Otomatik Uyarilar", "#e94560")
            for u in otomatik_uyarilar:
                st.warning(u)
        else:
            _styled_info_banner("Tum metrikler normal. Otomatik uyari yok. ✅")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  2. BİNA & TESİS HARİTASI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_tesis_haritasi(store):
    _styled_header("Bina & Tesis Haritasi — Lokasyon Bazli Yonetim", "🗺️")

    lokasyon_path = _get_data_path(store, "lokasyonlar.json")
    lokasyonlar = _load_json(lokasyon_path)

    # Ticket verilerini yükle
    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    # Bakım verilerini yükle
    try:
        bakimlar = store.load_list("bakim_kayitlari") or []
    except Exception:
        bakimlar = []

    _styled_stat_row([
        ("Kayitli Lokasyon", len(lokasyonlar)),
        ("Toplam Talep", len(tickets)),
        ("Bakim Kaydi", len(bakimlar)),
    ])

    sub = st.tabs(["🏢 Lokasyon Yonetimi", "🔥 Yogunluk Haritasi", "💰 Maliyet Analizi", "📊 Risk Skoru", "📦 Ekipman Envanteri"])

    # ── Lokasyon Yönetimi ──
    with sub[0]:
        _styled_section("🏢 Bina / Kat / Oda Tanimlama", "#0f3460")

        with st.form("lokasyon_form"):
            lc1, lc2, lc3 = st.columns(3)
            with lc1:
                l_bina = st.text_input("Bina Adi", key="lok_bina")
            with lc2:
                l_kat = st.text_input("Kat", key="lok_kat")
            with lc3:
                l_oda = st.text_input("Oda / Alan", key="lok_oda")
            lc4, lc5 = st.columns(2)
            with lc4:
                l_tur = st.selectbox("Alan Turu", ["Sinif", "Laboratuvar", "Ofis", "Toplanti Odasi", "Koridor", "Tuvalet", "Kantin", "Kutuphane", "Spor Salonu", "Bahce", "Otopark", "Depo", "Teknik", "Diger"], key="lok_tur")
            with lc5:
                l_kapasite = st.number_input("Kapasite", min_value=0, value=30, key="lok_kapasite")

            if st.form_submit_button("🏢 Lokasyon Ekle", use_container_width=True):
                if l_bina:
                    lokasyonlar.append({
                        "id": f"lok_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "bina": l_bina,
                        "kat": l_kat,
                        "oda": l_oda,
                        "tur": l_tur,
                        "kapasite": l_kapasite,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(lokasyon_path, lokasyonlar)
                    st.success(f"{l_bina} / {l_kat} / {l_oda} eklendi!")
                    st.rerun()

        if lokasyonlar:
            _styled_section("Kayitli Lokasyonlar", "#06d6a0")
            # Bina bazlı grupla
            bina_grup = {}
            for l in lokasyonlar:
                b = l.get("bina", "?")
                if b not in bina_grup:
                    bina_grup[b] = []
                bina_grup[b].append(l)

            for bina, locs in bina_grup.items():
                with st.expander(f"🏢 {bina} ({len(locs)} alan)"):
                    for l in locs:
                        st.markdown(f"""
                        <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;">
                            <span style="color:#e0e0e0;">{l.get('kat','')}/{l.get('oda','')} — {l.get('tur','')}</span>
                            <span style="color:#888;font-size:0.8rem;">Kapasite: {l.get('kapasite','')}</span>
                        </div>""", unsafe_allow_html=True)

    # ── Yoğunluk Haritası ──
    with sub[1]:
        _styled_section("🔥 Talep & Ariza Yogunluk Haritasi", "#e94560")

        if tickets:
            # Lokasyon bazlı talep sayısı
            lok_talep = {}
            for t in tickets:
                lok = _get_attr(t, "lokasyon") or _get_attr(t, "konum") or _get_attr(t, "bina") or "Belirtilmemis"
                lok_talep[lok] = lok_talep.get(lok, 0) + 1

            if lok_talep:
                st.markdown("**En Cok Talep Alan Lokasyonlar**")
                max_val = max(lok_talep.values())
                for lok, sayi in sorted(lok_talep.items(), key=lambda x: -x[1])[:15]:
                    oran = sayi / max_val
                    renk = "#e94560" if oran > 0.7 else ("#ffd166" if oran > 0.4 else "#06d6a0")
                    bar_w = int(oran * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="width:180px;color:#e0e0e0;font-weight:600;font-size:0.88rem;">{lok[:25]}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:22px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                        </div>
                        <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                    </div>""", unsafe_allow_html=True)

                # Top 3 alarm
                top3 = sorted(lok_talep.items(), key=lambda x: -x[1])[:3]
                if top3[0][1] > 5:
                    st.error(f"🔥 En yogun: {top3[0][0]} ({top3[0][1]} talep) — detayli inceleme onerilir!")
        else:
            _styled_info_banner("Yogunluk haritasi icin talep verisi gerekiyor.")

    # ── Maliyet Analizi ──
    with sub[2]:
        _styled_section("💰 Lokasyon Bazli Maliyet Analizi", "#ffd166")

        maliyet_path = _get_data_path(store, "lokasyon_maliyetleri.json")
        maliyetler = _load_json(maliyet_path)

        with st.form("lok_maliyet_form"):
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                m_lokasyon = st.text_input("Lokasyon", key="lok_mal_lok")
            with mc2:
                m_tutar = st.number_input("Maliyet (TL)", min_value=0.0, step=100.0, key="lok_mal_tutar")
            with mc3:
                m_tur = st.selectbox("Tur", ["Bakim", "Onarim", "Yenileme", "Temizlik", "Diger"], key="lok_mal_tur")

            if st.form_submit_button("💰 Kaydet", use_container_width=True):
                if m_lokasyon and m_tutar > 0:
                    maliyetler.append({
                        "lokasyon": m_lokasyon,
                        "tutar": m_tutar,
                        "tur": m_tur,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(maliyet_path, maliyetler)
                    st.success("Maliyet kaydedildi!")
                    st.rerun()

        if maliyetler:
            lok_maliyet = {}
            for m in maliyetler:
                l = m.get("lokasyon", "?")
                lok_maliyet[l] = lok_maliyet.get(l, 0) + m.get("tutar", 0)

            toplam = sum(lok_maliyet.values())
            _styled_stat_row([("Toplam Maliyet", f"TL{toplam:,.0f}"), ("Lokasyon Sayisi", len(lok_maliyet))])

            for lok, tutar in sorted(lok_maliyet.items(), key=lambda x: -x[1]):
                st.markdown(f"""
                <div style="background:#16213e;border-radius:8px;padding:10px 14px;margin-bottom:5px;display:flex;justify-content:space-between;">
                    <span style="color:#e0e0e0;font-weight:600;">{lok}</span>
                    <span style="color:#ffd166;font-weight:700;">TL{tutar:,.0f}</span>
                </div>""", unsafe_allow_html=True)

    # ── Risk Skoru ──
    with sub[3]:
        _styled_section("📊 Lokasyon Risk Skoru", "#8338ec")

        if lokasyonlar and tickets:
            _styled_info_banner("Risk skoru; talep yogunlugu, tekrar eden arizalar ve bakim durumuna gore hesaplanir.")

            risk_list = []
            for l in lokasyonlar:
                ad = f"{l.get('bina','')}/{l.get('kat','')}/{l.get('oda','')}"
                talep_sayi = len([t for t in tickets if ad.lower() in str(_get_attr(t, "lokasyon") or _get_attr(t, "konum") or "").lower()])
                bakim_sayi = len([b for b in bakimlar if ad.lower() in str(_get_attr(b, "lokasyon") or _get_attr(b, "konum") or "").lower()])
                risk = min(100, talep_sayi * 15 + max(0, 30 - bakim_sayi * 10))
                risk_list.append({"ad": ad, "talep": talep_sayi, "bakim": bakim_sayi, "risk": risk})

            risk_list.sort(key=lambda x: -x["risk"])

            for r in risk_list:
                skor = r["risk"]
                renk = "#e94560" if skor >= 70 else ("#ffd166" if skor >= 40 else "#06d6a0")
                durum = "YUKSEK RISK" if skor >= 70 else ("ORTA" if skor >= 40 else "DUSUK")

                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="color:#e0e0e0;">{r['ad']}</strong>
                        <span style="color:#888;font-size:0.78rem;margin-left:8px;">Talep: {r['talep']} | Bakim: {r['bakim']}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="background:#1a1a2e;border-radius:6px;width:80px;height:14px;overflow:hidden;">
                            <div style="width:{skor}%;height:100%;background:{renk};border-radius:6px;"></div>
                        </div>
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;font-size:0.78rem;font-weight:600;">{durum}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Risk skoru icin lokasyon ve talep verisi gerekiyor.")

    # ── Ekipman Envanteri ──
    with sub[4]:
        _styled_section("📦 Oda Bazli Ekipman Envanteri", "#06d6a0")

        envanter_path = _get_data_path(store, "lokasyon_envanter.json")
        envanter = _load_json(envanter_path)

        with st.form("envanter_form"):
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                e_lokasyon = st.text_input("Lokasyon (Bina/Kat/Oda)", key="env_lok")
            with ec2:
                e_ekipman = st.text_input("Ekipman Adi", key="env_ekip")
            with ec3:
                e_adet = st.number_input("Adet", min_value=1, value=1, key="env_adet")
            e_durum = st.selectbox("Durum", ["Calisiyor", "Arizali", "Bakimda", "Yeni"], key="env_durum")

            if st.form_submit_button("📦 Envanter Ekle", use_container_width=True):
                if e_lokasyon and e_ekipman:
                    envanter.append({
                        "id": f"env_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "lokasyon": e_lokasyon,
                        "ekipman": e_ekipman,
                        "adet": e_adet,
                        "durum": e_durum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(envanter_path, envanter)
                    st.success("Envanter eklendi!")
                    st.rerun()

        if envanter:
            # Lokasyon bazlı grupla
            lok_grup = {}
            for e in envanter:
                l = e.get("lokasyon", "?")
                if l not in lok_grup:
                    lok_grup[l] = []
                lok_grup[l].append(e)

            for lok, items in lok_grup.items():
                with st.expander(f"📍 {lok} ({len(items)} ekipman)"):
                    for item in items:
                        durum_renk = {"Calisiyor": "#06d6a0", "Arizali": "#e94560", "Bakimda": "#ffd166", "Yeni": "#00b4d8"}.get(item.get("durum", ""), "#888")
                        st.markdown(f"""
                        <div style="background:#1a1a2e;border-radius:8px;padding:8px 12px;margin-bottom:3px;display:flex;justify-content:space-between;">
                            <span style="color:#e0e0e0;">{item.get('ekipman','')} x{item.get('adet','')}</span>
                            <span style="color:{durum_renk};font-size:0.82rem;font-weight:600;">{item.get('durum','')}</span>
                        </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Envanter kaydi olusturun.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  3. MEMNUNİYET & KALİTE ENDEKSİ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_memnuniyet_endeksi(store):
    _styled_header("Memnuniyet & Kalite Endeksi", "🏆")

    anket_path = _get_data_path(store, "memnuniyet_anketleri.json")
    anketler = _load_json(anket_path)

    # Ticket verilerini yükle
    try:
        tickets = store.load_list("tickets") or []
    except Exception:
        tickets = []

    # İstatistikler
    toplam_anket = len(anketler)
    ort_puan = sum(a.get("puan", 0) for a in anketler) / max(1, toplam_anket)
    memnun = len([a for a in anketler if a.get("puan", 0) >= 4])
    memnuniyet_oran = int(memnun / max(1, toplam_anket) * 100)

    _styled_stat_row([
        ("Toplam Degerlendirme", toplam_anket),
        ("Ort. Puan", f"{ort_puan:.1f}/5"),
        ("Memnuniyet Orani", f"%{memnuniyet_oran}"),
        ("Memnun (4-5)", memnun),
        ("Memnun Degil (1-3)", toplam_anket - memnun),
    ])

    sub = st.tabs(["📊 Memnuniyet Dashboard", "📝 Anket Gir", "👤 Birim Karnesi", "🏢 Firma Karnesi", "📈 Kalite Trendi", "🤖 AI İyilestirme"])

    # ── Memnuniyet Dashboard ──
    with sub[0]:
        _styled_section("📊 Memnuniyet Genel Bakis", "#06d6a0")

        if anketler:
            # Genel skor
            renk = "#06d6a0" if ort_puan >= 4 else ("#ffd166" if ort_puan >= 3 else "#e94560")
            yildiz = "⭐" * int(ort_puan)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:16px;padding:24px;text-align:center;margin-bottom:16px;">
                <div style="font-size:0.9rem;color:#888;">Genel Memnuniyet Skoru</div>
                <div style="font-size:3.5rem;font-weight:900;color:{renk};">{ort_puan:.1f}</div>
                <div style="font-size:1.5rem;">{yildiz}</div>
                <div style="color:#aaa;font-size:0.85rem;margin-top:4px;">{toplam_anket} degerlendirme</div>
            </div>""", unsafe_allow_html=True)

            # Puan dağılımı
            puan_dagilim = Counter(a.get("puan", 0) for a in anketler)
            _styled_section("Puan Dagilimi", "#ffd166")
            puan_etiketler = {5: "Cok Memnun", 4: "Memnun", 3: "Orta", 2: "Memnun Degil", 1: "Cok Kotu"}
            puan_renkler = {5: "#06d6a0", 4: "#00b4d8", 3: "#ffd166", 2: "#ff6b6b", 1: "#e94560"}
            max_puan = max(puan_dagilim.values()) if puan_dagilim else 1

            for p in range(5, 0, -1):
                sayi = puan_dagilim.get(p, 0)
                bar_w = int(sayi / max_puan * 100) if sayi else 0
                renk = puan_renkler.get(p, "#888")
                etiket = puan_etiketler.get(p, "?")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                    <span style="width:30px;color:{renk};font-weight:700;font-size:1.1rem;">{p}⭐</span>
                    <span style="width:100px;color:#888;font-size:0.85rem;">{etiket}</span>
                    <div style="flex:1;background:#1a1a2e;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                    <span style="width:40px;text-align:right;color:{renk};font-weight:700;">{sayi}</span>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Dashboard icin memnuniyet degerlendirmesi girin.")

    # ── Anket Gir ──
    with sub[1]:
        _styled_section("📝 Memnuniyet Anketi / Degerlendirme", "#8338ec")

        with st.form("memnuniyet_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                a_talep = st.text_input("Ilgili Talep No / Baslik", key="memn_talep")
                a_degerlendiren = st.text_input("Degerlendiren Kisi", key="memn_kisi")
                a_birim = st.text_input("Hizmet Birimi / Departman", key="memn_birim")
            with ac2:
                a_puan = st.slider("Genel Memnuniyet (1-5)", 1, 5, 4, key="memn_puan")
                a_hiz_puan = st.slider("Cozum Hizi (1-5)", 1, 5, 3, key="memn_hiz")
                a_iletisim_puan = st.slider("Iletisim Kalitesi (1-5)", 1, 5, 4, key="memn_iletisim")
            a_yorum = st.text_area("Yorum / Oneri", height=68, key="memn_yorum")

            if st.form_submit_button("📝 Degerlendirmeyi Kaydet", use_container_width=True):
                if a_degerlendiren:
                    anketler.append({
                        "id": f"mmn_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "talep": a_talep,
                        "degerlendiren": a_degerlendiren,
                        "birim": a_birim,
                        "puan": a_puan,
                        "hiz_puan": a_hiz_puan,
                        "iletisim_puan": a_iletisim_puan,
                        "yorum": a_yorum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(anket_path, anketler)
                    st.success("Degerlendirme kaydedildi!")
                    st.rerun()

        # Son değerlendirmeler
        if anketler:
            _styled_section("Son Degerlendirmeler", "#0f3460")
            for a in reversed(anketler[-8:]):
                p = a.get("puan", 0)
                renk = "#06d6a0" if p >= 4 else ("#ffd166" if p >= 3 else "#e94560")
                st.markdown(f"""
                <div style="background:#16213e;border-radius:10px;padding:10px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#e0e0e0;">{a.get('degerlendiren','?')}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{a.get('birim','')}</span>
                        </div>
                        <div>
                            <span style="color:{renk};font-weight:700;font-size:1.2rem;">{'⭐' * p}</span>
                            <span style="color:#888;font-size:0.78rem;margin-left:8px;">{a.get('tarih','')[:10]}</span>
                        </div>
                    </div>
                    {f'<div style="color:#aaa;font-size:0.85rem;margin-top:4px;">{a.get("yorum","")}</div>' if a.get("yorum") else ''}
                </div>""", unsafe_allow_html=True)

    # ── Birim Karnesi ──
    with sub[2]:
        _styled_section("👤 Birim / Departman Memnuniyet Karnesi", "#00b4d8")

        if anketler:
            birim_puan = {}
            for a in anketler:
                b = a.get("birim", "Genel")
                if b not in birim_puan:
                    birim_puan[b] = []
                birim_puan[b].append(a.get("puan", 0))

            for birim, puanlar in sorted(birim_puan.items(), key=lambda x: -sum(x[1])/len(x[1])):
                ort = sum(puanlar) / len(puanlar)
                renk = "#06d6a0" if ort >= 4 else ("#ffd166" if ort >= 3 else "#e94560")
                bar_w = int(ort / 5 * 100)

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                        <div>
                            <strong style="color:#e0e0e0;font-size:1.05rem;">{birim}</strong>
                            <span style="color:#888;font-size:0.8rem;margin-left:8px;">{len(puanlar)} degerlendirme</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.4rem;font-weight:800;color:{renk};">{ort:.1f}</span>
                            <span style="color:#888;font-size:0.8rem;">/5</span>
                        </div>
                    </div>
                    <div style="background:#1a1a2e;border-radius:6px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:6px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Birim karnesi icin degerlendirme verisi gerekiyor.")

    # ── Firma Karnesi ──
    with sub[3]:
        _styled_section("🏢 Dis Firma / Tedarikci Memnuniyet Karnesi", "#ffd166")

        firma_anket_path = _get_data_path(store, "firma_memnuniyet.json")
        firma_anketler = _load_json(firma_anket_path)

        with st.form("firma_memn_form"):
            fc1, fc2 = st.columns(2)
            with fc1:
                f_firma = st.text_input("Firma Adi", key="firma_memn_ad")
                f_hizmet = st.text_input("Hizmet Turu", key="firma_memn_hizmet")
            with fc2:
                f_puan = st.slider("Genel Puan (1-5)", 1, 5, 3, key="firma_memn_puan")
                f_zamaninda = st.selectbox("Zamaninda Teslim", ["Evet", "Hayir", "Kismen"], key="firma_memn_zaman")
            f_yorum = st.text_input("Yorum", key="firma_memn_yorum")

            if st.form_submit_button("🏢 Firma Degerlendirmesi Kaydet", use_container_width=True):
                if f_firma:
                    firma_anketler.append({
                        "id": f"fmm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "firma": f_firma,
                        "hizmet": f_hizmet,
                        "puan": f_puan,
                        "zamaninda": f_zamaninda,
                        "yorum": f_yorum,
                        "tarih": datetime.now().isoformat(),
                    })
                    _save_json(firma_anket_path, firma_anketler)
                    st.success("Firma degerlendirmesi kaydedildi!")
                    st.rerun()

        if firma_anketler:
            firma_puan = {}
            for f in firma_anketler:
                ad = f.get("firma", "?")
                if ad not in firma_puan:
                    firma_puan[ad] = {"puanlar": [], "zamaninda": 0, "toplam": 0}
                firma_puan[ad]["puanlar"].append(f.get("puan", 0))
                firma_puan[ad]["toplam"] += 1
                if f.get("zamaninda") == "Evet":
                    firma_puan[ad]["zamaninda"] += 1

            for firma, data in sorted(firma_puan.items(), key=lambda x: -sum(x[1]["puanlar"])/len(x[1]["puanlar"])):
                ort = sum(data["puanlar"]) / len(data["puanlar"])
                zaman_oran = int(data["zamaninda"] / max(1, data["toplam"]) * 100)
                renk = "#06d6a0" if ort >= 4 else ("#ffd166" if ort >= 3 else "#e94560")
                yildiz = "⭐" * int(ort)

                st.markdown(f"""
                <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <strong style="color:#ffd166;font-size:1.05rem;">{firma}</strong>
                            <div style="color:#888;font-size:0.8rem;">{data['toplam']} degerlendirme | Zamaninda: %{zaman_oran}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.3rem;font-weight:800;color:{renk};">{ort:.1f}/5</div>
                            <div>{yildiz}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── Kalite Trendi ──
    with sub[4]:
        _styled_section("📈 Aylik Memnuniyet & Kalite Trendi", "#8338ec")

        if anketler:
            aylik = {}
            for a in anketler:
                ay = a.get("tarih", "")[:7]
                if ay:
                    if ay not in aylik:
                        aylik[ay] = []
                    aylik[ay].append(a.get("puan", 0))

            if aylik:
                st.markdown("**Aylik Ortalama Memnuniyet Puani**")
                for ay in sorted(aylik.keys()):
                    puanlar = aylik[ay]
                    ort = sum(puanlar) / len(puanlar)
                    bar_w = int(ort / 5 * 100)
                    renk = "#06d6a0" if ort >= 4 else ("#ffd166" if ort >= 3 else "#e94560")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
                        <span style="width:80px;color:#888;font-size:0.85rem;">{ay}</span>
                        <div style="flex:1;background:#1a1a2e;border-radius:6px;height:20px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}88);border-radius:6px;"></div>
                        </div>
                        <span style="width:50px;text-align:right;color:{renk};font-weight:700;">{ort:.1f}/5</span>
                        <span style="width:30px;color:#888;font-size:0.78rem;">({len(puanlar)})</span>
                    </div>""", unsafe_allow_html=True)

                # Trend yönü
                aylar_sorted = sorted(aylik.keys())
                if len(aylar_sorted) >= 2:
                    son_ort = sum(aylik[aylar_sorted[-1]]) / len(aylik[aylar_sorted[-1]])
                    onceki_ort = sum(aylik[aylar_sorted[-2]]) / len(aylik[aylar_sorted[-2]])
                    degisim = son_ort - onceki_ort
                    yon_renk = "#06d6a0" if degisim > 0 else "#e94560"
                    yon_text = "yukseldi" if degisim > 0 else "dustu"
                    st.markdown(f"""
                    <div style="background:#0f3460;border-radius:10px;padding:14px;text-align:center;margin-top:10px;">
                        <span style="color:#888;">Trend: </span>
                        <span style="color:{yon_renk};font-weight:700;font-size:1.2rem;">{degisim:+.1f} puan ({yon_text})</span>
                    </div>""", unsafe_allow_html=True)
        else:
            _styled_info_banner("Trend analizi icin degerlendirme verisi gerekiyor.")

    # ── AI İyileştirme ──
    with sub[5]:
        _styled_section("🤖 AI Iyilestirme Onerileri", "#00b4d8")

        _styled_info_banner("AI, memnuniyet verilerine dayanarak iyilestirme onerileri sunar.")

        oneriler = []

        if ort_puan < 3.5:
            oneriler.append(("Acil: Hizmet Kalitesi", "Genel memnuniyet dusukte. Personel egitimi ve surec iyilestirmesi onerilir.", "#e94560"))
        if anketler:
            dusuk_hiz = [a for a in anketler if a.get("hiz_puan", 5) <= 2]
            if len(dusuk_hiz) > len(anketler) * 0.3:
                oneriler.append(("Cozum Hizi Dusuk", "Cozum suresi memnuniyeti etkiliyor. Kaynak artirimi veya otomasyon onerilir.", "#ffd166"))
            dusuk_iletisim = [a for a in anketler if a.get("iletisim_puan", 5) <= 2]
            if len(dusuk_iletisim) > len(anketler) * 0.3:
                oneriler.append(("Iletisim Eksikligi", "Kullanicilara duzenli geri bildirim saglanmali. Otomatik bildirim sistemi kurulmali.", "#8338ec"))

        if not oneriler:
            oneriler = [
                ("Proaktif Iletisim", "Talep durumu hakkinda otomatik bilgilendirme gonderimi memnuniyeti %15 artirir.", "#06d6a0"),
                ("Ilk Yanit Suresi", "Ilk 1 saat icinde yanit veren ekipler %25 daha yuksek puan aliyor.", "#00b4d8"),
                ("Kapanma Anketi", "Her kapanan talep sonrasi otomatik anket gonderimi veri kalitesini arttirir.", "#ffd166"),
                ("Tekrar Eden Sorunlar", "En sik tekrar eden ariza turlerini belirleyip kok neden analizi yapin.", "#8338ec"),
                ("Personel Taninirlik", "Teknisyen/gorevli isim ve iletisim bilgisini paylasmak guven arttirir.", "#ff6b6b"),
            ]

        for baslik, aciklama, renk in oneriler:
            st.markdown(f"""
            <div style="background:#16213e;border-radius:12px;padding:14px 18px;margin-bottom:8px;border-left:4px solid {renk};">
                <h4 style="color:{renk};margin:0 0 6px 0;">{baslik}</h4>
                <p style="color:#aaa;font-size:0.88rem;margin:0;">{aciklama}</p>
            </div>""", unsafe_allow_html=True)

        # Genel kalite endeksi
        if anketler:
            genel_hiz = sum(a.get("hiz_puan", 3) for a in anketler) / len(anketler)
            genel_iletisim = sum(a.get("iletisim_puan", 3) for a in anketler) / len(anketler)
            kalite_endeks = int((ort_puan + genel_hiz + genel_iletisim) / 3 / 5 * 100)
            renk = "#06d6a0" if kalite_endeks >= 70 else ("#ffd166" if kalite_endeks >= 50 else "#e94560")

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f3460,#16213e);border-radius:14px;padding:20px;text-align:center;margin-top:14px;">
                <div style="color:#888;">Genel Hizmet Kalite Endeksi</div>
                <div style="font-size:3rem;font-weight:800;color:{renk};">{kalite_endeks}/100</div>
                <div style="color:#aaa;font-size:0.85rem;">Memnuniyet + Hiz + Iletisim ortalaması</div>
            </div>""", unsafe_allow_html=True)


# ── Yardımcı fonksiyonlar ──
def _get_attr(obj, key):
    """Dict veya dataclass'tan attribute okur."""
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)

def _parse_date(val):
    """Tarih string'ini datetime'a cevirir."""
    if isinstance(val, datetime):
        return val
    val_str = str(val)
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(val_str[:len(fmt.replace('%', 'X'))], fmt)
        except (ValueError, IndexError):
            continue
    return datetime.now()
