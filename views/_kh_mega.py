"""
Kurum Hizmetleri — MEGA Ozellikleri
=====================================
1. Akilli Tesis Yonetim Sistemi (Smart Facility Manager)
2. Veli Deneyim Platformu (Parent Experience Hub)
3. Acil Durum Yonetim Merkezi (Emergency Command Center)
"""
from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


# ============================================================
# 1. AKILLI TESİS YÖNETİM SİSTEMİ
# ============================================================

_VARSAYILAN_ALANLAR = [
    {"ad": "1. Kat Siniflar", "tip": "sinif", "kapasite": 30, "adet": 8},
    {"ad": "2. Kat Siniflar", "tip": "sinif", "kapasite": 30, "adet": 8},
    {"ad": "Fen Laboratuvari", "tip": "lab", "kapasite": 25, "adet": 2},
    {"ad": "Bilgisayar Lab", "tip": "lab", "kapasite": 30, "adet": 1},
    {"ad": "Spor Salonu", "tip": "spor", "kapasite": 100, "adet": 1},
    {"ad": "Yemekhane", "tip": "yemekhane", "kapasite": 200, "adet": 1},
    {"ad": "Kutuphane", "tip": "kutuphane", "kapasite": 50, "adet": 1},
    {"ad": "Ogretmenler Odasi", "tip": "idari", "kapasite": 40, "adet": 1},
    {"ad": "Toplanti Salonu", "tip": "idari", "kapasite": 30, "adet": 2},
    {"ad": "Bahce/Oyun Alani", "tip": "dis_alan", "kapasite": 200, "adet": 1},
    {"ad": "Otopark", "tip": "dis_alan", "kapasite": 50, "adet": 1},
    {"ad": "Tuvalet Blok A", "tip": "tuvalet", "kapasite": 0, "adet": 4},
    {"ad": "Tuvalet Blok B", "tip": "tuvalet", "kapasite": 0, "adet": 4},
]


def _tesis_path() -> str:
    return os.path.join(_td(), "kurum_hizmetleri", "tesis_yonetim.json")


def _enerji_path() -> str:
    return os.path.join(_td(), "kurum_hizmetleri", "enerji_tuketim.json")


def _temizlik_path() -> str:
    return os.path.join(_td(), "kurum_hizmetleri", "temizlik_kayitlari.json")


def render_tesis_yonetim():
    """Akilli tesis yonetim — alan + temizlik + enerji."""
    styled_section("Akilli Tesis Yonetim", "#059669")
    styled_info_banner(
        "Okulun fiziksel altyapisini dijitallestirin. "
        "Alan envanteri + temizlik takibi + enerji tuketim analizi.",
        banner_type="info", icon="🏗️")

    tesis = _lj(_tesis_path())
    if not tesis:
        tesis = _VARSAYILAN_ALANLAR

    temizlik = _lj(_temizlik_path())
    enerji = _lj(_enerji_path())

    toplam_alan = sum(a.get("adet", 1) for a in tesis)
    bugun = date.today().isoformat()

    # Temizlik durumu
    bugun_temizlik = [t for t in temizlik if t.get("tarih", "") == bugun]
    temizlenen = len(set(t.get("alan", "") for t in bugun_temizlik))

    styled_stat_row([
        ("Toplam Alan", str(toplam_alan), "#059669", "🏗️"),
        ("Bugun Temizlenen", str(temizlenen), "#10b981", "🧹"),
        ("Enerji Kaydi", str(len(enerji)), "#f59e0b", "⚡"),
    ])

    sub = st.tabs(["🏗️ Alan Envanteri", "🧹 Temizlik Takibi", "⚡ Enerji Tuketim"])

    # ═══ ALAN ENVANTERİ ═══
    with sub[0]:
        styled_section("Okul Alan Envanteri")
        tip_renk = {"sinif": "#2563eb", "lab": "#7c3aed", "spor": "#ea580c", "yemekhane": "#f59e0b",
                      "kutuphane": "#0891b2", "idari": "#64748b", "dis_alan": "#10b981", "tuvalet": "#94a3b8"}
        tip_ikon = {"sinif": "🏫", "lab": "🔬", "spor": "🏋️", "yemekhane": "🍽️",
                      "kutuphane": "📚", "idari": "🏛️", "dis_alan": "🌳", "tuvalet": "🚻"}

        for a in tesis:
            tip = a.get("tip", "diger")
            renk = tip_renk.get(tip, "#64748b")
            ikon = tip_ikon.get(tip, "📋")
            # Son temizlik
            son_tem = next((t for t in sorted(temizlik, key=lambda x: x.get("tarih", ""), reverse=True)
                             if t.get("alan", "") == a["ad"]), None)
            son_tem_txt = son_tem.get("tarih", "Hic") if son_tem else "Hic"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:14px;">{ikon}</span>
                        <span style="font-weight:700;color:#e2e8f0;font-size:13px;margin-left:6px;">{a['ad']}</span>
                        <span style="color:#94a3b8;font-size:10px;margin-left:8px;">x{a.get('adet', 1)}</span>
                    </div>
                    <div style="display:flex;gap:8px;font-size:10px;">
                        <span style="color:#94a3b8;">Kapasite: {a.get('kapasite', '-')}</span>
                        <span style="color:#64748b;">Son temizlik: {son_tem_txt}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ TEMİZLİK TAKİBİ ═══
    with sub[1]:
        styled_section("Temizlik Kaydi Gir")
        with st.form("temizlik_form"):
            tc1, tc2 = st.columns(2)
            with tc1:
                t_alan = st.selectbox("Alan", [a["ad"] for a in tesis], key="tem_alan")
                t_personel = st.text_input("Temizlik Personeli", key="tem_per")
            with tc2:
                t_tarih = st.date_input("Tarih", value=date.today(), key="tem_tarih")
                t_durum = st.selectbox("Durum", ["Tamamlandi", "Kismi", "Yapilmadi"], key="tem_durum")
            t_not = st.text_input("Not", key="tem_not", placeholder="Ek bilgi...")

            if st.form_submit_button("Kaydet", type="primary"):
                temizlik.append({
                    "id": f"tem_{uuid.uuid4().hex[:8]}",
                    "alan": t_alan, "personel": t_personel,
                    "tarih": t_tarih.isoformat(), "durum": t_durum, "not": t_not,
                    "created_at": datetime.now().isoformat(),
                })
                _sj(_temizlik_path(), temizlik)
                st.success(f"Temizlik kaydi eklendi: {t_alan}")
                st.rerun()

        # Son kayitlar
        styled_section("Son Temizlik Kayitlari")
        for t in sorted(temizlik, key=lambda x: x.get("tarih", ""), reverse=True)[:15]:
            d_renk = "#10b981" if t.get("durum") == "Tamamlandi" else "#f59e0b" if t.get("durum") == "Kismi" else "#ef4444"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
                <span style="min-width:70px;font-size:10px;color:#94a3b8;">{t.get('tarih', '')}</span>
                <span style="flex:1;font-size:11px;color:#e2e8f0;">{t.get('alan', '')}</span>
                <span style="font-size:10px;color:#94a3b8;">{t.get('personel', '-')}</span>
                <span style="background:{d_renk}20;color:{d_renk};padding:2px 6px;border-radius:4px;
                            font-size:9px;font-weight:700;">{t.get('durum', '')}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ ENERJİ TÜKETİM ═══
    with sub[2]:
        styled_section("Enerji & Su Tuketim Takibi")

        with st.form("enerji_form"):
            ec1, ec2, ec3, ec4 = st.columns(4)
            with ec1:
                e_ay = st.selectbox("Ay", list(range(1, 13)),
                                     format_func=lambda x: ["Oca", "Sub", "Mar", "Nis", "May", "Haz",
                                                              "Tem", "Agu", "Eyl", "Eki", "Kas", "Ara"][x-1],
                                     index=date.today().month - 1, key="enerji_ay")
            with ec2:
                e_elektrik = st.number_input("Elektrik (kWh)", 0, 100000, 0, key="enerji_e")
            with ec3:
                e_su = st.number_input("Su (m3)", 0, 10000, 0, key="enerji_s")
            with ec4:
                e_dogalgaz = st.number_input("Dogalgaz (m3)", 0, 50000, 0, key="enerji_d")

            if st.form_submit_button("Kaydet", type="primary"):
                enerji.append({
                    "ay": e_ay, "yil": date.today().year,
                    "elektrik": e_elektrik, "su": e_su, "dogalgaz": e_dogalgaz,
                    "created_at": datetime.now().isoformat(),
                })
                _sj(_enerji_path(), enerji)
                st.success("Enerji tuketim kaydedildi!")
                st.rerun()

        # Trend
        if enerji:
            styled_section("12 Aylik Enerji Trendi")
            ay_adlari = ["Oca", "Sub", "Mar", "Nis", "May", "Haz", "Tem", "Agu", "Eyl", "Eki", "Kas", "Ara"]
            for e in sorted(enerji, key=lambda x: (x.get("yil", 0), x.get("ay", 0)), reverse=True)[:12]:
                ay_adi = ay_adlari[e.get("ay", 1) - 1]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:3px 0;">
                    <span style="min-width:50px;font-size:11px;color:#e2e8f0;font-weight:600;">{ay_adi} {e.get('yil', '')}</span>
                    <span style="font-size:10px;color:#f59e0b;">⚡{e.get('elektrik', 0):,} kWh</span>
                    <span style="font-size:10px;color:#3b82f6;">💧{e.get('su', 0):,} m3</span>
                    <span style="font-size:10px;color:#ef4444;">🔥{e.get('dogalgaz', 0):,} m3</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# 2. VELİ DENEYİM PLATFORMU
# ============================================================

def render_veli_portal():
    """Veli self-servis portal — tek noktadan tum hizmetler."""
    styled_section("Veli Deneyim Platformu", "#7c3aed")
    styled_info_banner(
        "Velinin okulla tum etkilesimi tek portalda. "
        "Randevu, belge, menu, servis, mesaj, not, duyuru — hepsi burada.",
        banner_type="info", icon="👪")

    ak = _ak_dir()
    td = _td()

    # Veri topla
    randevular = _lj(os.path.join(ak, "veli_randevular.json"))
    belge_talep = _lj(os.path.join(ak, "veli_belge_talepleri.json"))
    mesajlar = _lj(os.path.join(ak, "veli_mesajlar.json"))
    duyurular = _lj(os.path.join(ak, "duyurular.json"))
    if not duyurular:
        duyurular = _lj(os.path.join(td, "akademik", "duyurular.json"))
    menuler = _lj(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
    if not menuler:
        menuler = _lj(os.path.join(ak, "yemek_menusu.json"))
    anketler = _lj(os.path.join(td, "veli_anket", "cevaplar.json"))

    bekleyen_rnd = sum(1 for r in randevular if r.get("durum") in ("Beklemede", "beklemede"))
    bekleyen_blg = sum(1 for b in belge_talep if b.get("durum") in ("Beklemede", "beklemede"))
    cevapsiz_msj = sum(1 for m in mesajlar if not m.get("cevaplandi") and m.get("yon", m.get("direction", "")) == "gelen")

    styled_stat_row([
        ("Randevu Talep", str(len(randevular)), "#7c3aed", "📅"),
        ("Belge Talep", str(len(belge_talep)), "#2563eb", "📄"),
        ("Mesaj", str(len(mesajlar)), "#059669", "💬"),
        ("Bekleyen Rnd", str(bekleyen_rnd), "#f59e0b", "⏳"),
        ("Cevapsiz Msj", str(cevapsiz_msj), "#ef4444", "📬"),
    ])

    sub = st.tabs(["📊 Ozet", "📅 Randevular", "📄 Belge Talepler", "📢 Duyurular", "🍽️ Menu"])

    # ═══ ÖZET ═══
    with sub[0]:
        styled_section("Veli Hizmet Ozeti")

        hizmetler = [
            {"ad": "Randevu Sistemi", "ikon": "📅", "sayi": len(randevular), "bekleyen": bekleyen_rnd, "renk": "#7c3aed"},
            {"ad": "Belge Talep", "ikon": "📄", "sayi": len(belge_talep), "bekleyen": bekleyen_blg, "renk": "#2563eb"},
            {"ad": "Mesaj Sistemi", "ikon": "💬", "sayi": len(mesajlar), "bekleyen": cevapsiz_msj, "renk": "#059669"},
            {"ad": "Duyurular", "ikon": "📢", "sayi": len(duyurular), "bekleyen": 0, "renk": "#f59e0b"},
            {"ad": "Memnuniyet Anketi", "ikon": "⭐", "sayi": len(anketler), "bekleyen": 0, "renk": "#ec4899"},
        ]

        for h in hizmetler:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {h['renk']}30;border-left:4px solid {h['renk']};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:13px;font-weight:700;color:#e2e8f0;">{h['ikon']} {h['ad']}</span>
                    <div style="display:flex;gap:10px;font-size:11px;">
                        <span style="color:{h['renk']};">{h['sayi']} toplam</span>
                        {f'<span style="color:#ef4444;font-weight:700;">{h["bekleyen"]} bekleyen</span>' if h['bekleyen'] > 0 else ''}
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Cozum suresi
        cozulen_rnd = [r for r in randevular if r.get("durum") == "Tamamlandi"]
        cozulen_blg = [b for b in belge_talep if b.get("durum") == "Tamamlandi"]
        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #7c3aed;border-radius:14px;padding:14px;
                    text-align:center;margin-top:12px;">
            <div style="font-size:10px;color:#94a3b8;">Hizmet Performansi</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;">
                <div><div style="font-size:22px;font-weight:800;color:#10b981;">{len(cozulen_rnd)}</div>
                    <div style="font-size:9px;color:#94a3b8;">Tamamlanan Rnd</div></div>
                <div><div style="font-size:22px;font-weight:800;color:#2563eb;">{len(cozulen_blg)}</div>
                    <div style="font-size:9px;color:#94a3b8;">Tamamlanan Belge</div></div>
                <div><div style="font-size:22px;font-weight:800;color:#f59e0b;">{len(duyurular)}</div>
                    <div style="font-size:9px;color:#94a3b8;">Duyuru</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ═══ RANDEVULAR ═══
    with sub[1]:
        styled_section("Veli Randevu Talepleri")
        for r in sorted(randevular, key=lambda x: x.get("tarih", x.get("created_at", "")), reverse=True)[:20]:
            durum = r.get("durum", "?")
            d_renk = {"Tamamlandi": "#10b981", "Beklemede": "#f59e0b", "Iptal": "#94a3b8", "Onaylandi": "#3b82f6"}.get(durum, "#64748b")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #1e293b;">
                <span style="min-width:70px;font-size:10px;color:#94a3b8;">{r.get('tarih', r.get('created_at', ''))[:10]}</span>
                <span style="flex:1;font-size:11px;color:#e2e8f0;">{r.get('veli_adi', r.get('ad', '-'))}</span>
                <span style="font-size:10px;color:#94a3b8;">{r.get('konu', '-')[:30]}</span>
                <span style="background:{d_renk}20;color:{d_renk};padding:2px 6px;border-radius:4px;
                            font-size:9px;font-weight:700;">{durum}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ BELGE TALEPLER ═══
    with sub[2]:
        styled_section("Belge Talepleri")
        for b in sorted(belge_talep, key=lambda x: x.get("created_at", ""), reverse=True)[:20]:
            durum = b.get("durum", "?")
            d_renk = {"Tamamlandi": "#10b981", "Beklemede": "#f59e0b"}.get(durum, "#64748b")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #1e293b;">
                <span style="min-width:70px;font-size:10px;color:#94a3b8;">{(b.get('created_at', '') or '')[:10]}</span>
                <span style="flex:1;font-size:11px;color:#e2e8f0;">{b.get('veli_adi', b.get('ad', '-'))}</span>
                <span style="font-size:10px;color:#94a3b8;">{b.get('belge_turu', '-')}</span>
                <span style="background:{d_renk}20;color:{d_renk};padding:2px 6px;border-radius:4px;
                            font-size:9px;font-weight:700;">{durum}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ DUYURULAR ═══
    with sub[3]:
        styled_section("Son Duyurular")
        for d in sorted(duyurular, key=lambda x: x.get("tarih", x.get("created_at", "")), reverse=True)[:10]:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #f59e0b30;border-left:3px solid #f59e0b;
                        border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:4px;">
                <span style="font-size:10px;color:#f59e0b;font-weight:700;">{(d.get('tarih', d.get('created_at', '')) or '')[:10]}</span>
                <span style="font-size:12px;color:#e2e8f0;font-weight:600;margin-left:8px;">{d.get('baslik', d.get('title', ''))[:60]}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ MENÜ ═══
    with sub[4]:
        styled_section("Bu Haftanin Menusu")
        bugun = date.today()
        for i in range(5):
            gun = bugun - timedelta(days=bugun.weekday()) + timedelta(days=i)
            gun_str = gun.isoformat()
            gun_menu = next((m for m in menuler if m.get("tarih", "") == gun_str), None)
            gun_adi = ["Pzt", "Sal", "Car", "Per", "Cum"][i]
            is_bugun = gun == bugun

            if gun_menu:
                ogle = gun_menu.get("ogle", gun_menu.get("ana_yemek", gun_menu.get("menu", "-")))[:50]
            else:
                ogle = "Menu girilmedi"

            border = "2px solid #f59e0b" if is_bugun else "1px solid #1e293b"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #1e293b;">
                <span style="min-width:30px;font-size:11px;color:{'#f59e0b' if is_bugun else '#94a3b8'};
                            font-weight:{'800' if is_bugun else '400'};">{'> ' if is_bugun else ''}{gun_adi}</span>
                <span style="font-size:11px;color:#e2e8f0;">{ogle}</span>
            </div>""", unsafe_allow_html=True)


# ============================================================
# 3. ACİL DURUM YÖNETİM MERKEZİ
# ============================================================

_ACIL_PROTOKOLLER = {
    "yangin": {"label": "Yangin", "ikon": "🔥", "renk": "#ef4444",
               "adimlar": ["Alarm aktive et", "Tahliye baslat", "Itfaiye ara (110)", "Toplanma noktasina yonlendir",
                            "Ogrenci sayimi yap", "Veli bildirim gonder", "Olay raporu yaz"]},
    "deprem": {"label": "Deprem", "ikon": "🌍", "renk": "#f59e0b",
               "adimlar": ["Cap-Kapan-Tutun komutu ver", "Sarsinti durmasini bekle", "Tahliye baslat",
                            "Bina hasar kontrolu", "Ogrenci sayimi", "AFAD bildir (122)", "Veli bildirim"]},
    "saglik": {"label": "Saglik Acil", "ikon": "🏥", "renk": "#dc2626",
               "adimlar": ["Revir aktive et", "Ilk yardim uygula", "Ambulans ara (112)",
                            "Veli bildir", "Olay raporu", "Sigorta bildirimi"]},
    "guvenlik": {"label": "Guvenlik Tehdidi", "ikon": "🔒", "renk": "#7c3aed",
                 "adimlar": ["Lockdown komutu ver", "Kapilari kilitle", "Polis ara (155)",
                              "Ogrencileri sinifta tut", "Veli bildirim (tehlike gecinceye kadar bekleme)",
                              "Emniyet ile koordinasyon"]},
    "afet": {"label": "Dogal Afet", "ikon": "⛈️", "renk": "#0891b2",
             "adimlar": ["Erken kapatma karari", "Servisleri aktive et", "Veli bildirim",
                          "Ogrenci teslim listesi", "Bina guvenligi kontrol"]},
}


def _acil_log_path() -> str:
    return os.path.join(_td(), "kurum_hizmetleri", "acil_durum_log.json")


def render_acil_durum():
    """Acil durum yonetim merkezi."""
    styled_section("Acil Durum Yonetim Merkezi", "#dc2626")
    styled_info_banner(
        "Yangin, deprem, saglik acil, guvenlik tehdidi — "
        "her senaryo icin adim adim dijital protokol + iletisim agaci.",
        banner_type="warning", icon="🚨")

    acil_log = _lj(_acil_log_path())

    styled_stat_row([
        ("Protokol Sayisi", str(len(_ACIL_PROTOKOLLER)), "#dc2626", "📋"),
        ("Gecmis Olay", str(len(acil_log)), "#f59e0b", "📜"),
    ])

    sub = st.tabs(["📋 Protokoller", "🚨 Acil Baslat", "📜 Olay Gecmisi", "📞 Iletisim Agaci"])

    # ═══ PROTOKOLLER ═══
    with sub[0]:
        styled_section("Acil Durum Protokolleri")
        for key, prot in _ACIL_PROTOKOLLER.items():
            with st.expander(f"{prot['ikon']} {prot['label']} Protokolu ({len(prot['adimlar'])} adim)", expanded=False):
                for i, adim in enumerate(prot["adimlar"], 1):
                    st.markdown(f"""
                    <div style="display:flex;gap:10px;align-items:center;padding:4px 0;">
                        <div style="width:24px;height:24px;border-radius:50%;background:{prot['renk']};
                                    display:flex;align-items:center;justify-content:center;
                                    font-size:10px;color:#fff;font-weight:800;flex-shrink:0;">{i}</div>
                        <span style="font-size:12px;color:#e2e8f0;">{adim}</span>
                    </div>""", unsafe_allow_html=True)

    # ═══ ACİL BAŞLAT ═══
    with sub[1]:
        styled_section("Acil Durum Baslat", "#ef4444")
        st.markdown("""
        <div style="background:#7f1d1d;border:2px solid #ef4444;border-radius:14px;
                    padding:16px;text-align:center;margin-bottom:12px;">
            <div style="font-size:14px;font-weight:800;color:#fca5a5;">
                Bu bolum gercek acil durumlarda kullanilir. Tatbikat icin SSG modulunu kullanin.</div>
        </div>""", unsafe_allow_html=True)

        acil_tur = st.selectbox("Acil Durum Turu",
            list(_ACIL_PROTOKOLLER.keys()),
            format_func=lambda x: f"{_ACIL_PROTOKOLLER[x]['ikon']} {_ACIL_PROTOKOLLER[x]['label']}",
            key="acil_tur")
        acil_aciklama = st.text_area("Durum Aciklamasi", key="acil_aciklama", height=80)

        if st.button("ACIL DURUM BASLAT", key="acil_btn", type="primary", use_container_width=True):
            if acil_aciklama:
                prot = _ACIL_PROTOKOLLER[acil_tur]
                log = {
                    "id": f"acil_{uuid.uuid4().hex[:8]}",
                    "tur": acil_tur, "aciklama": acil_aciklama,
                    "tarih": date.today().isoformat(),
                    "saat": datetime.now().strftime("%H:%M"),
                    "durum": "aktif",
                    "adimlar": [{"adim": a, "tamamlandi": False} for a in prot["adimlar"]],
                    "created_at": datetime.now().isoformat(),
                }
                acil_log.append(log)
                _sj(_acil_log_path(), acil_log)
                st.error(f"🚨 ACIL DURUM BASLATILDI: {prot['label']}")

                # Protokol adimlarini goster
                for i, adim in enumerate(prot["adimlar"], 1):
                    st.markdown(f"**{i}.** {adim}")
                st.rerun()

    # ═══ OLAY GEÇMİŞİ ═══
    with sub[2]:
        styled_section("Gecmis Acil Durumlar")
        if not acil_log:
            st.success("Gecmis acil durum kaydi yok.")
        else:
            for log in sorted(acil_log, key=lambda x: x.get("created_at", ""), reverse=True):
                prot = _ACIL_PROTOKOLLER.get(log.get("tur", ""), {"label": "?", "ikon": "?", "renk": "#64748b"})
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {prot['renk']}30;border-left:4px solid {prot['renk']};
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{prot['ikon']} {prot['label']}</span>
                        <span style="font-size:10px;color:#94a3b8;">{log.get('tarih', '')} {log.get('saat', '')}</span>
                    </div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:3px;">{log.get('aciklama', '')[:100]}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ İLETİŞİM AĞACI ═══
    with sub[3]:
        styled_section("Acil Durum Iletisim Agaci")
        iletisim = [
            {"rol": "Okul Muduru", "ikon": "👔", "seviye": 1, "renk": "#dc2626"},
            {"rol": "Mudur Yardimcisi", "ikon": "👤", "seviye": 2, "renk": "#f97316"},
            {"rol": "Guvenlik Sorumlusu", "ikon": "🛡️", "seviye": 2, "renk": "#f97316"},
            {"rol": "Ogretmenler (Nobetci)", "ikon": "👨‍🏫", "seviye": 3, "renk": "#f59e0b"},
            {"rol": "Revir Hemiresi", "ikon": "🏥", "seviye": 3, "renk": "#f59e0b"},
            {"rol": "Servis Koordinatoru", "ikon": "🚌", "seviye": 3, "renk": "#f59e0b"},
            {"rol": "Tum Ogretmenler", "ikon": "👥", "seviye": 4, "renk": "#3b82f6"},
            {"rol": "Veliler (Toplu SMS)", "ikon": "👪", "seviye": 4, "renk": "#3b82f6"},
        ]

        st.markdown("""
        <div style="background:#0f172a;border:1px solid #dc2626;border-radius:14px;padding:16px;margin-bottom:12px;">
            <div style="font-size:11px;color:#fca5a5;font-weight:700;margin-bottom:8px;">Bildirim Sirasi (Ust → Alt)</div>
        """, unsafe_allow_html=True)

        for il in iletisim:
            indent = (il["seviye"] - 1) * 30
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:4px 0;margin-left:{indent}px;">
                <span style="font-size:14px;">{il['ikon']}</span>
                <span style="font-size:12px;font-weight:600;color:{il['renk']};">{il['rol']}</span>
                <span style="font-size:9px;color:#64748b;">Seviye {il['seviye']}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Acil numaralar
        styled_section("Acil Numaralar")
        numaralar = [("Itfaiye", "110", "🔥"), ("Ambulans", "112", "🏥"),
                      ("Polis", "155", "🚔"), ("AFAD", "122", "🌍"),
                      ("Dogalgaz Acil", "187", "🔥"), ("Elektrik Ariza", "186", "⚡")]
        for ad, no, ikon in numaralar:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                <span style="font-size:16px;">{ikon}</span>
                <span style="font-size:13px;color:#e2e8f0;font-weight:700;">{ad}</span>
                <span style="font-size:16px;font-weight:900;color:#ef4444;font-family:monospace;">{no}</span>
            </div>""", unsafe_allow_html=True)
