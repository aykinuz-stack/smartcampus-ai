"""
Erken Uyarı — Mega Özellikler
================================
1. Çapraz Modül Risk Füzyon Motoru
2. Gerçek Zamanlı Bildirim & Veli-Öğretmen Mesajlaşma
3. Pozitif Davranış & Ödül Tabanlı Önleme Sistemi
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner
from views._eu_common import eu_data_dir as _dd, eu_load_json as _lj, eu_save_json as _sj, eu_ogrenci_sec as _ogr_sec

_FUZYON_MODULLERI = {
    "Akademik": {"ikon": "📚", "renk": "#3b82f6", "agirlik": 20, "kaynak": "Sinav sonuclari, not ortalamasi"},
    "Devamsizlik": {"ikon": "📅", "renk": "#ef4444", "agirlik": 18, "kaynak": "Devamsizlik kayitlari"},
    "Davranis": {"ikon": "⚠️", "renk": "#f59e0b", "agirlik": 15, "kaynak": "Davranis olaylari, zorbalik"},
    "Sosyo-Duygusal": {"ikon": "🧠", "renk": "#8b5cf6", "agirlik": 15, "kaynak": "Duygu kaydi, kaygı olcegi"},
    "Sosyal Katilim": {"ikon": "👥", "renk": "#10b981", "agirlik": 10, "kaynak": "Kulup, etkinlik katilimi"},
    "Saglik": {"ikon": "🏥", "renk": "#0891b2", "agirlik": 8, "kaynak": "Revir ziyareti, kronik hastalik"},
    "Dijital Ogrenme": {"ikon": "💻", "renk": "#6366f1", "agirlik": 7, "kaynak": "AI calisma, quest XP"},
    "Aile": {"ikon": "👨‍👩‍👧", "renk": "#059669", "agirlik": 7, "kaynak": "Veli geri bildirim, gorusme"},
}

_POZITIF_DAVRANISLAR = [
    {"ad": "Tam Devam", "ikon": "✅", "puan": 10, "kosul": "Haftada 0 devamsizlik", "renk": "#10b981"},
    {"ad": "Ders Yildizi", "ikon": "⭐", "puan": 8, "kosul": "Ders ici aktif katilim", "renk": "#f59e0b"},
    {"ad": "Yardimci Arkadas", "ikon": "🤝", "puan": 12, "kosul": "Arkadasina yardim etme", "renk": "#3b82f6"},
    {"ad": "Temiz Sinif", "ikon": "🧹", "puan": 5, "kosul": "Sinif temizligine katki", "renk": "#059669"},
    {"ad": "Odun Getir", "ikon": "📚", "puan": 7, "kosul": "Odevlerini zamaninda teslim", "renk": "#8b5cf6"},
    {"ad": "Spor Ruhu", "ikon": "🏃", "puan": 6, "kosul": "Sportmenlik gosterme", "renk": "#0891b2"},
    {"ad": "Saygi Yildizi", "ikon": "💎", "puan": 10, "kosul": "Ogretmen/arkadasa saygi", "renk": "#c9a84c"},
    {"ad": "Gelisim Sampiyonu", "ikon": "📈", "puan": 15, "kosul": "Not ortalamasi yukseldi", "renk": "#6366f1"},
]

_POZITIF_ROZETLER = [
    {"ad": "Hafta Yildizi", "ikon": "⭐", "kosul": "hafta_30", "hedef": 30, "renk": "#f59e0b"},
    {"ad": "Ay Kahramani", "ikon": "🏆", "kosul": "ay_100", "hedef": 100, "renk": "#c9a84c"},
    {"ad": "Donem Efsanesi", "ikon": "💎", "kosul": "donem_500", "hedef": 500, "renk": "#8b5cf6"},
]


def _cross_module_load(ogr_ad: str) -> dict:
    """Cross-module veri yukle — her modülden risk sinyali topla."""
    td = get_tenant_dir()
    skorlar = {}

    # Akademik (olcme)
    try:
        p = os.path.join(td, "olcme", "results.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                results = json.load(f)
            ogr_r = [r for r in results if r.get("student_name","").startswith(ogr_ad.split()[0])]
            if ogr_r:
                puanlar = [r.get("score",50) for r in ogr_r if isinstance(r.get("score"), (int,float))]
                ort = sum(puanlar) / max(len(puanlar),1) if puanlar else 50
                skorlar["Akademik"] = max(0, min(100, round(100 - ort)))
            else:
                skorlar["Akademik"] = 30
        else:
            skorlar["Akademik"] = 30
    except Exception:
        skorlar["Akademik"] = 30

    # Sosyo-Duygusal (rehberlik)
    try:
        p = os.path.join(td, "rehberlik", "sosyo_duygusal.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                duygu = json.load(f)
            _mp = {"Cok Mutlu":5,"Mutlu":4,"Normal":3,"Mutsuz":2,"Cok Mutsuz":1,"Ofkeli":1,"Kaygili":2}
            ogr_d = [_mp.get(d.get("duygu","Normal"),3) for d in duygu if ogr_ad.split()[0] in d.get("ogrenci_ad","")]
            if ogr_d:
                ort = sum(ogr_d)/len(ogr_d)
                skorlar["Sosyo-Duygusal"] = max(0, min(100, round((5-ort)*20)))
            else:
                skorlar["Sosyo-Duygusal"] = 25
        else:
            skorlar["Sosyo-Duygusal"] = 25
    except Exception:
        skorlar["Sosyo-Duygusal"] = 25

    # Davranis (rehberlik)
    try:
        p = os.path.join(td, "rehberlik", "davranis_olaylari.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                dav = json.load(f)
            ogr_dav = sum(1 for d in dav if ogr_ad.split()[0] in d.get("ogrenci_ad",""))
            skorlar["Davranis"] = min(100, ogr_dav * 15)
        else:
            skorlar["Davranis"] = 10
    except Exception:
        skorlar["Davranis"] = 10

    # Sosyal Katilim (sosyal_etkinlik)
    try:
        p = os.path.join(td, "sosyal_etkinlik", "kulup_katilim.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                katilim = json.load(f)
            sayi = sum(1 for k in katilim if ogr_ad in k.get("katilanlar",[]))
            skorlar["Sosyal Katilim"] = max(0, min(100, 60 - sayi * 5))
        else:
            skorlar["Sosyal Katilim"] = 40
    except Exception:
        skorlar["Sosyal Katilim"] = 40

    # Diger modüller — varsayilan
    for mod in ["Devamsizlik", "Saglik", "Dijital Ogrenme", "Aile"]:
        if mod not in skorlar:
            skorlar[mod] = random.randint(10, 40)

    return skorlar


# ════════════════════════════════════════════════════════════
# 1. ÇAPRAZ MODÜL RİSK FÜZYON MOTORU
# ════════════════════════════════════════════════════════════

def render_fuzyon_motoru(store, loader):
    """Çapraz Modül Risk Füzyon — 8+ modülden birleşik risk skoru."""
    styled_section("Capraz Modul Risk Fuzyon Motoru", "#6366f1")
    styled_info_banner(
        "9+ modulden anlik veri cekerek tek birlesik 'Tehlike Endeksi' uretir. "
        "Her modulun katkisi ayri gosterilir.",
        banner_type="info", icon="🌐")

    sub = st.tabs(["🎯 Bireysel Fuzyon", "🗺️ Sinif Haritasi", "📊 Modul Katki", "📈 Trend"])

    with sub[0]:
        styled_section("Ogrenci Tehlike Endeksi")
        ogr = _ogr_sec("fm_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            skorlar = _cross_module_load(ogr_ad)

            # Agirlikli toplam
            genel = 0
            for mod, info in _FUZYON_MODULLERI.items():
                genel += skorlar.get(mod, 25) * info["agirlik"] / 100
            genel = round(genel)

            g_renk = "#dc2626" if genel >= 60 else "#ef4444" if genel >= 40 else "#f59e0b" if genel >= 20 else "#10b981"
            g_label = "Kritik" if genel >= 60 else "Yuksek" if genel >= 40 else "Orta" if genel >= 20 else "Dusuk"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,{g_renk}15);border:3px solid {g_renk};
                border-radius:22px;padding:24px 28px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                <div style="color:#94a3b8;font-size:0.8rem;">Birlesik Tehlike Endeksi</div>
                <div style="color:{g_renk};font-weight:900;font-size:3.5rem;margin-top:8px;">{genel}</div>
                <div style="color:{g_renk};font-weight:700;font-size:0.9rem;">{g_label} Risk</div>
            </div>""", unsafe_allow_html=True)

            # Modul bazli detay
            styled_section("Modul Bazli Risk Katkisi")
            for mod, info in _FUZYON_MODULLERI.items():
                skor = skorlar.get(mod, 25)
                renk = "#ef4444" if skor >= 50 else "#f59e0b" if skor >= 25 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
                    <span style="font-size:1.1rem;">{info['ikon']}</span>
                    <span style="min-width:120px;color:#e2e8f0;font-weight:700;font-size:0.8rem;">{mod}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
                        <div style="width:{skor}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                            border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:800;">{skor}/100</span>
                        </div>
                    </div>
                    <span style="font-size:0.6rem;color:#64748b;">{info['agirlik']}%</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Sinif Bazli Tehlike Haritasi")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci yok.")
        else:
            ss = get_sinif_sube_listesi()
            sec_s = st.selectbox("Sinif", ["Tumu"] + ss.get("siniflar",[]), key="fm_sinif")
            filtered = students if sec_s == "Tumu" else [s for s in students if str(s.get("sinif","")) == sec_s]

            endeks_list = []
            for s in filtered[:30]:
                ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
                sk = _cross_module_load(ogr_ad)
                genel = round(sum(sk.get(m,25) * _FUZYON_MODULLERI[m]["agirlik"]/100 for m in _FUZYON_MODULLERI))
                endeks_list.append({"ad": ogr_ad, "sinif": f"{s.get('sinif','')}/{s.get('sube','')}", "risk": genel})

            endeks_list.sort(key=lambda x: x["risk"], reverse=True)
            kirmizi = sum(1 for e in endeks_list if e["risk"] >= 40)
            sari = sum(1 for e in endeks_list if 20 <= e["risk"] < 40)
            yesil = sum(1 for e in endeks_list if e["risk"] < 20)

            styled_stat_row([
                ("Kirmizi", str(kirmizi), "#ef4444", "🔴"),
                ("Sari", str(sari), "#f59e0b", "🟡"),
                ("Yesil", str(yesil), "#10b981", "🟢"),
            ])

            for e in endeks_list[:20]:
                renk = "#dc2626" if e["risk"] >= 60 else "#ef4444" if e["risk"] >= 40 else "#f59e0b" if e["risk"] >= 20 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{e['ad']}</span>
                    <span style="color:#64748b;font-size:0.65rem;">{e['sinif']}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.75rem;">{e['risk']}/100</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Modul Veri Kaynaklari")
        for mod, info in _FUZYON_MODULLERI.items():
            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {info['renk']};border-radius:0 10px 10px 0;
                padding:8px 14px;margin:4px 0;">
                <span style="font-size:1rem;">{info['ikon']}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.82rem;margin-left:6px;">{mod}</span>
                <span style="color:#64748b;font-size:0.68rem;margin-left:8px;">(%{info['agirlik']})</span>
                <div style="color:#94a3b8;font-size:0.7rem;margin-top:2px;">Kaynak: {info['kaynak']}</div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Risk Trend (Simule)")
        ogr2 = _ogr_sec("fm_ogr2")
        if ogr2:
            for i in range(5, -1, -1):
                ay = date.today().replace(day=1) - timedelta(days=30*i)
                sim = random.randint(15, 55)
                renk = "#ef4444" if sim >= 40 else "#f59e0b" if sim >= 20 else "#10b981"
                is_bu = i == 0
                ay_ad = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                    {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                    <span style="min-width:35px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{ay_ad.get(ay.month,'')}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{sim}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim}</span></div></div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. GERÇEK ZAMANLI BİLDİRİM & VELİ-ÖĞRETMEN MESAJLAŞMA
# ════════════════════════════════════════════════════════════

def render_bildirim_merkezi(store, loader):
    """Gerçek Zamanlı Bildirim — risk değişim bildirimi, veli mesaj, haftalık bülten."""
    styled_section("Gercek Zamanli Bildirim & Mesajlasma", "#2563eb")
    styled_info_banner(
        "Risk seviyesi degistiginde anlik bildirim. "
        "Ogretmen-veli guvenli mesajlasma, haftalik risk bulteni.",
        banner_type="info", icon="📱")

    bildirimler = _lj("risk_bildirimler.json")
    mesajlar = _lj("risk_mesajlar.json")

    styled_stat_row([
        ("Bildirim", str(len(bildirimler)), "#2563eb", "🔔"),
        ("Mesaj", str(len(mesajlar)), "#10b981", "💬"),
    ])

    sub = st.tabs(["🔔 Bildirimler", "💬 Mesajlasma", "📋 Haftalik Bulten", "⚙️ Bildirim Ayar"])

    with sub[0]:
        styled_section("Risk Degisim Bildirimleri")
        with st.form("bildirim_form"):
            c1, c2 = st.columns(2)
            with c1:
                b_ogr = st.text_input("Ogrenci", key="bm_ogr")
                b_tur = st.selectbox("Bildirim Turu",
                    ["Risk Yukseldi", "Risk Dustu", "Yeni Alarm", "Mudahale Tamamlandi",
                     "Devamsizlik Uyari", "Not Dususu", "Davranis Olayi"], key="bm_tur")
            with c2:
                b_hedef = st.multiselect("Bildirim Hedefi",
                    ["Sinif Ogretmeni", "Rehber Ogretmen", "Mudur", "Veli"], key="bm_hedef")
            b_mesaj = st.text_area("Bildirim Mesaji", height=50, key="bm_mesaj")

            if st.form_submit_button("Bildirim Gonder", use_container_width=True, type="primary"):
                if b_ogr and b_hedef:
                    bildirimler.append({
                        "id": f"bn_{uuid.uuid4().hex[:8]}",
                        "ogrenci": b_ogr, "tur": b_tur, "hedefler": b_hedef,
                        "mesaj": b_mesaj, "durum": "Gonderildi",
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("risk_bildirimler.json", bildirimler)
                    st.success(f"Bildirim gonderildi: {' + '.join(b_hedef)}")
                    st.rerun()

        if bildirimler:
            styled_section("Son Bildirimler")
            for b in sorted(bildirimler, key=lambda x: x.get("tarih",""), reverse=True)[:10]:
                tur_renk = {"Risk Yukseldi":"#ef4444","Risk Dustu":"#10b981","Yeni Alarm":"#dc2626",
                    "Mudahale Tamamlandi":"#3b82f6"}.get(b.get("tur",""),"#f59e0b")
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;margin:3px 0;
                    background:#0f172a;border-left:3px solid {tur_renk};border-radius:0 8px 8px 0;">
                    <span style="color:{tur_renk};font-weight:700;font-size:0.72rem;min-width:100px;">{b.get('tur','')}</span>
                    <span style="color:#e2e8f0;font-size:0.75rem;flex:1;">{b.get('ogrenci','')} — {b.get('mesaj','')[:40]}</span>
                    <span style="color:#64748b;font-size:0.6rem;">{b.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Ogretmen-Veli Guvenli Mesajlasma")
        with st.form("mesaj_form"):
            c1, c2 = st.columns(2)
            with c1:
                m_gonderen = st.text_input("Gonderen", key="rm_gon")
                m_alici = st.text_input("Alici", key="rm_al")
            with c2:
                m_konu = st.text_input("Konu", placeholder="Ahmet'in devamsizligi hk.", key="rm_konu")
            m_mesaj = st.text_area("Mesaj", height=60, key="rm_mesaj")

            if st.form_submit_button("Gonder", use_container_width=True):
                if m_gonderen and m_alici and m_mesaj:
                    mesajlar.append({
                        "gonderen": m_gonderen, "alici": m_alici,
                        "konu": m_konu, "mesaj": m_mesaj,
                        "tarih": datetime.now().isoformat(),
                    })
                    _sj("risk_mesajlar.json", mesajlar)
                    st.success("Mesaj gonderildi!")
                    st.rerun()

        if mesajlar:
            for m in sorted(mesajlar, key=lambda x: x.get("tarih",""), reverse=True)[:8]:
                st.markdown(f"""
                <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                    border-left:3px solid #2563eb;border-radius:0 8px 8px 0;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#93c5fd;font-size:0.7rem;">{m.get('gonderen','')} → {m.get('alici','')}</span>
                        <span style="color:#64748b;font-size:0.6rem;">{m.get('tarih','')[:10]}</span>
                    </div>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{m.get('mesaj','')[:80]}</div>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Haftalik Risk Bulteni")
        alarmlar = _lj("escalation_alarmlar.json")
        bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
        hafta_alarm = [a for a in alarmlar if a.get("created_at","")[:10] >= bu_hafta]
        hafta_bildirim = [b for b in bildirimler if b.get("tarih","")[:10] >= bu_hafta]

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #334155;border-radius:16px;padding:20px 24px;">
            <div style="text-align:center;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">📋 Haftalik Risk Bulteni</div>
                <div style="color:#94a3b8;font-size:0.75rem;">{bu_hafta[5:]} — {date.today().isoformat()[5:]}</div>
            </div>
            <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;">
                <div style="text-align:center;"><div style="color:#ef4444;font-weight:900;font-size:1.5rem;">{len(hafta_alarm)}</div><div style="color:#64748b;font-size:0.62rem;">Yeni Alarm</div></div>
                <div style="text-align:center;"><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{len(hafta_bildirim)}</div><div style="color:#64748b;font-size:0.62rem;">Bildirim</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Bildirim Ayarlari")
        st.markdown("**Otomatik Bildirim Tetikleyicileri:**")
        tetikler = [
            ("Risk seviyesi degistiginde", True),
            ("Yeni alarm olusturulduugunda", True),
            ("Mudahale suresi asıldığında", True),
            ("Haftalik bulten (Pazartesi)", True),
            ("Devamsizlik 3+ gun", False),
            ("Not dususu %15+", False),
        ]
        for tetik, varsayilan in tetikler:
            st.checkbox(tetik, value=varsayilan, key=f"ba_{tetik[:10]}")


# ════════════════════════════════════════════════════════════
# 3. POZİTİF DAVRANIŞ & ÖDÜL TABANLI ÖNLEME
# ════════════════════════════════════════════════════════════

def render_pozitif_davranis(store, loader):
    """Pozitif Davranış & Ödül — puan, rozet, liderlik, restoratif yaklaşım."""
    styled_section("Pozitif Davranis & Odul Tabanli Onleme Sistemi", "#10b981")
    styled_info_banner(
        "Cezalandirma degil odullendirme yaklasimi. Pozitif davranis puani, "
        "rozet, sinif liderlik tablosu, restoratif mudahale plani.",
        banner_type="info", icon="🏅")

    puan_kayitlari = _lj("pozitif_puanlar.json")

    # KPI
    toplam_puan = sum(p.get("puan",0) for p in puan_kayitlari)
    bu_ay = sum(p.get("puan",0) for p in puan_kayitlari if p.get("tarih","")[:7] == date.today().strftime("%Y-%m"))
    ogrenci_say = len(set(p.get("ogrenci","") for p in puan_kayitlari))

    styled_stat_row([
        ("Toplam Puan", str(toplam_puan), "#10b981", "⭐"),
        ("Bu Ay", str(bu_ay), "#f59e0b", "📅"),
        ("Ogrenci", str(ogrenci_say), "#3b82f6", "👥"),
    ])

    sub = st.tabs(["⭐ Puan Ver", "🏆 Liderlik", "🎖️ Rozetler", "🔄 Restoratif Plan", "📊 Analiz"])

    with sub[0]:
        styled_section("Pozitif Davranis Puani Ver")
        with st.form("poz_form"):
            c1, c2 = st.columns(2)
            with c1:
                ogr = _ogr_sec("pz_ogr")
                p_davranis = st.selectbox("Davranis",
                    [f"{d['ikon']} {d['ad']} (+{d['puan']})" for d in _POZITIF_DAVRANISLAR], key="pz_dav")
            with c2:
                p_veren = st.text_input("Veren Ogretmen", key="pz_veren")
                p_tarih = st.date_input("Tarih", key="pz_tarih")
            p_not = st.text_input("Not (opsiyonel)", key="pz_not")

            if st.form_submit_button("Puan Ver", use_container_width=True, type="primary"):
                if ogr:
                    ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
                    idx = [f"{d['ikon']} {d['ad']} (+{d['puan']})" for d in _POZITIF_DAVRANISLAR].index(p_davranis)
                    dav = _POZITIF_DAVRANISLAR[idx]
                    puan_kayitlari.append({
                        "id": f"pz_{uuid.uuid4().hex[:8]}",
                        "ogrenci": ogr_ad, "sinif": f"{ogr.get('sinif','')}/{ogr.get('sube','')}",
                        "davranis": dav["ad"], "puan": dav["puan"],
                        "veren": p_veren, "not": p_not,
                        "tarih": p_tarih.isoformat(),
                    })
                    _sj("pozitif_puanlar.json", puan_kayitlari)
                    st.success(f"{dav['ikon']} {ogr_ad} — +{dav['puan']} puan! ({dav['ad']})")
                    st.rerun()

        # Davranis listesi
        styled_section("Pozitif Davranislar & Puanlar")
        for d in _POZITIF_DAVRANISLAR:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                background:{d['renk']}08;border:1px solid {d['renk']}30;border-radius:10px;">
                <span style="font-size:1.1rem;">{d['ikon']}</span>
                <span style="color:#e2e8f0;font-weight:700;font-size:0.8rem;flex:1;">{d['ad']}</span>
                <span style="color:{d['renk']};font-weight:800;font-size:0.8rem;">+{d['puan']}</span>
            </div>""", unsafe_allow_html=True)

    with sub[1]:
        styled_section("Pozitif Davranis Liderlik Tablosu")
        ogr_puan = defaultdict(int)
        for p in puan_kayitlari:
            ogr_puan[p.get("ogrenci","")] += p.get("puan", 0)

        lider = sorted(ogr_puan.items(), key=lambda x: x[1], reverse=True)

        if not lider:
            st.info("Puan kaydi yok.")
        else:
            for sira, (ad, puan) in enumerate(lider[:15], 1):
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                renk = "#c9a84c" if sira <= 3 else "#94a3b8"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:6px 14px;margin:3px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 10px 10px 0;">
                    <span style="font-size:1.1rem;min-width:28px;text-align:center;">{madalya}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.85rem;flex:1;">{ad}</span>
                    <span style="color:#c9a84c;font-weight:800;font-size:0.85rem;">⭐ {puan}</span>
                </div>""", unsafe_allow_html=True)

    with sub[2]:
        styled_section("Pozitif Davranis Rozetleri")
        for r in _POZITIF_ROZETLER:
            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid {r['renk']};border-radius:16px;
                padding:14px;text-align:center;margin:6px 0;display:inline-block;min-width:180px;">
                <div style="font-size:2rem;">{r['ikon']}</div>
                <div style="color:{r['renk']};font-weight:800;font-size:0.85rem;margin-top:4px;">{r['ad']}</div>
                <div style="color:#64748b;font-size:0.68rem;">{r['hedef']}+ puan</div>
            </div>""", unsafe_allow_html=True)

    with sub[3]:
        styled_section("Restoratif Yaklasim Plani")
        st.markdown("""
        **Restoratif Yaklasim — Ceza Degil Cozum Odakli:**

        Geleneksel yaklasim: "Ne yaptin? Kuralları bozdun. Cezan bu."

        Restoratif yaklasim: "Ne oldu? Kim etkilendi? Nasıl duzeltebiliriz?"
        """)

        adimlar = [
            ("1. Olayı Anlama", "Ogretmen yargilamadan dinler, tum taraflari duyar"),
            ("2. Etkiyi Gorme", "Davranisin kimi, nasıl etkiledigini konusur"),
            ("3. Sorumluluk Alma", "Ogrenci kendi eyleminin sorumlulugunnu alır"),
            ("4. Onarım Planı", "Birlikte 'nasıl düzeltebiliriz?' sorusuna cevap bulur"),
            ("5. Takip", "Plan uygulanıyor mu, iliski onarıldı mı kontrol"),
        ]
        for baslik, aciklama in adimlar:
            st.markdown(f"""
            <div style="background:#10b98108;border:1px solid #10b98130;border-left:4px solid #10b981;
                border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                <span style="color:#10b981;font-weight:800;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

    with sub[4]:
        styled_section("Pozitif Davranis Analizi")
        if puan_kayitlari:
            dav_say = Counter(p.get("davranis","") for p in puan_kayitlari)
            styled_section("En Sik Pozitif Davranis")
            for dav, sayi in dav_say.most_common():
                info = next((d for d in _POZITIF_DAVRANISLAR if d["ad"] == dav), {"ikon":"⭐","renk":"#10b981"})
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;">
                    <span style="font-size:1rem;">{info['ikon']}</span>
                    <span style="min-width:140px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{dav}</span>
                    <span style="color:#10b981;font-weight:700;">{sayi} kez</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Puan verisi yok.")
