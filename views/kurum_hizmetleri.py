"""
Kurum Hizmetleri Modülü
========================
Etkinlik & Duyurular, Yemek Menüsü, Servis Yönetimi, Veli Talep Yönetimi.
Akademik Takip modülünden bağımsız tek-ekran modülü olarak çalışır.
"""

from __future__ import annotations

import calendar
import json
import os
import uuid
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("kurum_hizmetleri")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("kurum_hizmetleri",
        "Nobet, ders programi, yemek, servis, veli talepleri, mesaj, kullanici yonetimi",
        [("9", "Sekme"), ("8", "Hizmet")])
except Exception:
    pass
from models.akademik_takip import (
    AkademikDataStore, get_akademik_store,
    VeliMesaj, MESAJ_KATEGORILERI,
)
from views.akademik_takip import (
    _render_nobet,
    _render_zaman_cizelgesi,
    _render_ders_programi,
    _styled_group_header,
)
from utils.tenant import get_data_path

# ==================== VERİ YOLU & SABITLER ====================

_HIZMET_DATA_DIR = get_data_path("akademik")

ETKINLIK_DOSYA = "etkinlik_duyurular.json"
YEMEK_MENU_DOSYA = "yemek_menusu.json"
SERVIS_DOSYA = "servis_bilgileri.json"
RANDEVU_DOSYA = "veli_randevular.json"
BELGE_TALEP_DOSYA = "veli_belge_talepleri.json"

MONTHS_TR = ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
             "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"]

ETKINLIK_TIPLERI = [
    ("duyuru",      "Duyuru"),
    ("etkinlik",    "Etkinlik"),
    ("toplanti",    "Toplantı"),
    ("tatil",       "Tatil"),
    ("toren",       "Tören"),
    ("sinav",       "Sınav"),
    ("kermes",      "Kermes"),
    ("mezuniyet",   "Mezuniyet"),
    ("seminer",     "Seminer"),
    ("panel",       "Panel"),
]

from models.servis_yonetimi import (
    SERVIS_DURUM_MAP, SOFOR_EHLIYET_SINIFLARI, SOFOR_DURUMLARI,
    ARAC_DURUMLARI, BAKIM_TIPLERI, OLAY_TIPLERI, OLAY_CIDDIYET,
    BINIS_DURUMLARI, ODEME_DURUMLARI, AYLAR_TR,
    Sofor, Hostes, Arac, ServisHatti, BinisKaydi, OlayKaydi,
    AracBakim, ServisUcret, TatilKaydi, get_servis_store,
)

BELGE_TURLERI_MAP = {
    "ogrenci_belgesi": "Öğrenci Belgesi",
    "transkript": "Not Durum Belgesi (Transkript)",
    "devamsizlik_belgesi": "Devamsızlık Belgesi",
    "nakil_belgesi": "Nakil Belgesi",
    "burs_belgesi": "Burs Belgesi",
    "kayit_belgesi": "Kayıt Belgesi",
    "askerlik_belgesi": "Askerlik Tecil Belgesi",
    "disiplin_belgesi": "Disiplin Durum Belgesi",
    "mezuniyet_belgesi": "Mezuniyet Belgesi",
}


# ==================== JSON YARDIMCILARI ====================

def _hizmet_json_path(filename: str) -> str:
    return os.path.join(_HIZMET_DATA_DIR, filename)


def _load_hizmet_json(filename: str) -> list[dict]:
    path = _hizmet_json_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_hizmet_json(filename: str, data: list[dict]) -> None:
    os.makedirs(_HIZMET_DATA_DIR, exist_ok=True)
    with open(_hizmet_json_path(filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==================== STİL YARDIMCILARI ====================

def _inject_css():
    inject_common_css("kh")
    st.markdown("""
    <style>
    .kh-metric-card {
        background: linear-gradient(135deg, #111827 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== 1) ETKİNLİK & DUYURU YÖNETİMİ ====================

def _render_admin_etkinlik_duyuru(store: AkademikDataStore):
    """Duyuru/etkinlik CRUD yonetimi."""
    styled_section("Etkinlik & Duyuru Yönetimi", "#3b82f6")

    duyurular = _load_hizmet_json(ETKINLIK_DOSYA)

    today = date.today()
    aktif = [d for d in duyurular
             if not d.get("bitis_tarihi") or d.get("bitis_tarihi", "") >= today.isoformat()]
    tip_sayac = {}
    for d in duyurular:
        t = d.get("tip", "duyuru")
        tip_sayac[t] = tip_sayac.get(t, 0) + 1

    stat_items = [
        ("Toplam", str(len(duyurular)), "#3b82f6", "📋"),
        ("Aktif", str(len(aktif)), "#22c55e", "✅"),
        ("Duyuru", str(tip_sayac.get("duyuru", 0)), "#f59e0b", "📢"),
        ("Etkinlik", str(tip_sayac.get("etkinlik", 0)), "#8b5cf6", "🎉"),
    ]
    cols = st.columns(len(stat_items))
    for i, (label, val, color, icon) in enumerate(stat_items):
        with cols[i]:
            st.metric(f"{icon} {label}", val)

    with st.expander("Yeni Duyuru / Etkinlik Ekle", expanded=False):
        with st.form("kh_etkinlik_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                baslik = st.text_input("Başlık *", key="kh_ae_baslik")
                tip_secenekler = [t[0] for t in ETKINLIK_TIPLERI] + ["diger"]
                tip_fmt = dict(ETKINLIK_TIPLERI)
                tip_fmt["diger"] = "➕ Diğer (özel gir)"
                tip = st.selectbox("Tip", tip_secenekler,
                                   format_func=lambda x: tip_fmt.get(x, x),
                                   key="kh_ae_tip")
                ozel_tip = st.text_input(
                    "Özel Tip Adı",
                    placeholder="Ör: Açık Kapı, Yarışma...",
                    key="kh_ae_ozel_tip",
                    disabled=(tip != "diger"),
                )
                tarih = st.date_input("Tarih", value=today, key="kh_ae_tarih")
            with fc2:
                yer = st.text_input("Yer (opsiyonel)", key="kh_ae_yer")
                saat = st.text_input("Saat (opsiyonel, orn: 10:00)", key="kh_ae_saat")
                bitis_tarihi = st.date_input("Bitis Tarihi (opsiyonel)",
                                              value=today + timedelta(days=30),
                                              key="kh_ae_bitis")

            icerik = st.text_area("İçerik *", key="kh_ae_icerik")

            # Hedef Sınıf/Şube — mevcut öğrencilerden otomatik üret
            _all_stu = store.get_students()
            def _safe_sinif_sort(x):
                parts = x.split("/")
                try:
                    return (0, int(parts[0]), parts[1] if len(parts) > 1 else "")
                except (ValueError, IndexError):
                    return (1, 0, x)
            _sinif_sube_set = sorted(
                set(f"{s.sinif}/{s.sube}" for s in _all_stu if s.sinif and s.sube),
                key=_safe_sinif_sort
            ) if _all_stu else []
            _hedef_secenekler = ["Tümü (Okul Geneli)"] + _sinif_sube_set
            hedef_sec = st.multiselect(
                "Hedef Sınıf / Şube",
                _hedef_secenekler,
                default=["Tümü (Okul Geneli)"],
                key="kh_ae_hedef",
                help="'Tümü (Okul Geneli)' seçilirse ya da boş bırakılırsa tüm okula gönderilir.",
            )
            onemli = st.checkbox("Onemli / Sabit Duyuru", key="kh_ae_onemli")

            if st.form_submit_button("Kaydet", type="primary"):
                gercek_tip = ozel_tip.strip() if tip == "diger" else tip
                if not baslik or not icerik:
                    st.error("Başlık ve icerik alanlari zorunludur.")
                elif tip == "diger" and not ozel_tip.strip():
                    st.error("Özel tip adı boş bırakılamaz.")
                else:
                    if not hedef_sec or "Tümü (Okul Geneli)" in hedef_sec:
                        hedef_list = ["tumu"]
                    else:
                        hedef_list = list(hedef_sec)  # ["5/A", "6/B", ...]

                    yeni = {
                        "id": str(uuid.uuid4())[:8],
                        "baslik": baslik,
                        "tip": gercek_tip,
                        "tarih": tarih.isoformat(),
                        "bitis_tarihi": bitis_tarihi.isoformat(),
                        "yer": yer,
                        "saat": saat,
                        "icerik": icerik,
                        "hedef_siniflar": hedef_list,
                        "onemli": onemli,
                        "olusturma_tarihi": datetime.now().isoformat(),
                    }
                    duyurular.append(yeni)
                    _save_hizmet_json(ETKINLIK_DOSYA, duyurular)
                    st.success(f"'{baslik}' basariyla eklendi!")
                    st.rerun()

    styled_section("Mevcut Duyurular", "#6366f1")

    if not duyurular:
        styled_info_banner("Henuz duyuru/etkinlik eklenmemiş.", "info")
        return

    for d in sorted(duyurular, key=lambda x: x.get("tarih", ""), reverse=True):
        tip = d.get("tip", "duyuru")
        tip_icon = {
            "duyuru": "📢", "etkinlik": "🎉", "toplanti": "📋", "tatil": "🏖️",
            "toren": "🎖️", "sinav": "📝", "kermes": "🎪", "mezuniyet": "🎓",
            "seminer": "🎤", "panel": "🗣️",
        }.get(tip, "📌")
        hedef = d.get("hedef_siniflar", ["tumu"])
        if not hedef or hedef == ["tumu"] or "tumu" in [str(h).lower() for h in hedef]:
            hedef_str = "Tümü (Okul Geneli)"
        else:
            hedef_str = ", ".join(str(h) for h in hedef)

        with st.expander(f"{tip_icon} {d.get('baslik', '-')} | {d.get('tarih', '-')} | Hedef: {hedef_str}"):
            st.markdown(f"**İçerik:** {d.get('icerik', '-')}")
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.caption(f"Yer: {d.get('yer', '-')} | Saat: {d.get('saat', '-')}")
            with mc2:
                st.caption(f"Bitis: {d.get('bitis_tarihi', '-')} | Onemli: {'Evet' if d.get('onemli') else 'Hayir'}")
            with mc3:
                if st.button("Sil", key=f"kh_del_etkinlik_{d.get('id', '')}",
                             type="secondary"):
                    duyurular.remove(d)
                    _save_hizmet_json(ETKINLIK_DOSYA, duyurular)
                    st.success("Silindi!")
                    st.rerun()


# ==================== 2) YEMEK MENÜSÜ YÖNETİMİ ====================

def _normalize_menu_kayit(m: dict) -> dict:
    """Eski (ogun+yemekler) veya yeni (kahvalti/ogle/ikindi) formati normalize eder."""
    if "kahvalti" in m or "ogle_yemegi" in m or "ikindi_ara_ogun" in m:
        return m
    ogun = m.get("ogun", "Ogle Yemegi")
    yemekler = m.get("yemekler", [])
    result = {
        "id": m.get("id", str(uuid.uuid4())[:8]),
        "tarih": m.get("tarih", ""),
        "kahvalti": [],
        "ogle_yemegi": [],
        "ikindi_ara_ogun": [],
        "notlar": m.get("notlar", ""),
        "guncelleme": m.get("guncelleme", ""),
    }
    if "Kahvalti" in ogun or "Sabah" in ogun:
        result["kahvalti"] = yemekler
    elif "Ikindi" in ogun or "ikindi" in ogun:
        result["ikindi_ara_ogun"] = yemekler
    else:
        result["ogle_yemegi"] = yemekler
    return result


def _render_admin_yemek_menusu():
    """Aylik yemek menusu giris ve yonetimi — Kahvaltı / Öğle / İkindi."""
    styled_section("Yemek Menüsü Yönetimi", "#f59e0b")

    menuler_raw = _load_hizmet_json(YEMEK_MENU_DOSYA)
    menuler_map: dict[str, dict] = {}
    for m in menuler_raw:
        nm = _normalize_menu_kayit(m)
        menuler_map[nm["tarih"]] = nm

    today = date.today()
    ay_key = f"{today.year}-{today.month:02d}"
    bu_ay_count = sum(1 for t in menuler_map if t.startswith(ay_key))

    styled_stat_row([
        ("Toplam Kayıt", str(len(menuler_map)), "#f59e0b", ""),
        (f"{MONTHS_TR[today.month-1]} Girilen", str(bu_ay_count), "#ea580c", ""),
        ("Bugün", "✅ Var" if today.isoformat() in menuler_map else "❌ Yok", "#10b981", ""),
    ])

    tab_gunluk, tab_excel, tab_takvim = st.tabs([
        "📅 Günlük Menü Ekle", "📊 Excel Yükle", "📆 Aylık Takvim"
    ])

    # ─────────── TAB 1: GÜNLÜK MENÜ EKLE ───────────
    with tab_gunluk:
        styled_section("Günlük Menü Girişi", "#f59e0b")
        styled_info_banner(
            "Kahvaltı, Öğle Yemeği ve İkindi Ara Öğün bilgilerini ayrı ayrı girin. "
            "Her satıra bir yiyecek/içecek yazın.",
            banner_type="info"
        )
        with st.form("kh_yemek_form", clear_on_submit=True):
            ym_tarih = st.date_input("Tarih", value=today, key="kh_ym_tarih")
            mevcut = menuler_map.get(ym_tarih.isoformat() if hasattr(ym_tarih, 'isoformat') else str(ym_tarih), {})

            yf1, yf2, yf3 = st.columns(3)
            with yf1:
                st.markdown("☕ **Kahvaltı**")
                kahvalti_text = st.text_area(
                    "Kahvaltı",
                    value="\n".join(mevcut.get("kahvalti", [])),
                    height=120,
                    placeholder="Çay\nPeynir\nZeytin\nDomates\nSalatalık\nEkmek",
                    key="kh_ym_kahvalti",
                    label_visibility="collapsed",
                )
            with yf2:
                st.markdown("🍽️ **Öğle Yemeği**")
                ogle_text = st.text_area(
                    "Öğle Yemeği",
                    value="\n".join(mevcut.get("ogle_yemegi", [])),
                    height=120,
                    placeholder="Mercimek Çorbası\nKuru Fasulye\nPirinç Pilavı\nAyran\nMeyve",
                    key="kh_ym_ogle",
                    label_visibility="collapsed",
                )
            with yf3:
                st.markdown("🍎 **İkindi Ara Öğün**")
                ikindi_text = st.text_area(
                    "İkindi Ara Öğün",
                    value="\n".join(mevcut.get("ikindi_ara_ogun", [])),
                    height=120,
                    placeholder="Meyve\nSüt\nBisküvi",
                    key="kh_ym_ikindi",
                    label_visibility="collapsed",
                )
            notlar = st.text_input(
                "Notlar (opsiyonel)",
                value=mevcut.get("notlar", ""),
                key="kh_ym_notlar"
            )
            if st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True):
                kahvalti = [y.strip() for y in kahvalti_text.strip().split("\n") if y.strip()]
                ogle = [y.strip() for y in ogle_text.strip().split("\n") if y.strip()]
                ikindi = [y.strip() for y in ikindi_text.strip().split("\n") if y.strip()]
                if not any([kahvalti, ogle, ikindi]):
                    st.error("En az bir öğün için yemek giriniz.")
                else:
                    tarih_str = ym_tarih.isoformat()
                    kayit = {
                        "id": mevcut.get("id", str(uuid.uuid4())[:8]),
                        "tarih": tarih_str,
                        "kahvalti": kahvalti,
                        "ogle_yemegi": ogle,
                        "ikindi_ara_ogun": ikindi,
                        "notlar": notlar.strip(),
                        "guncelleme": datetime.now().isoformat(),
                    }
                    menuler_map[tarih_str] = kayit
                    _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                    st.success(f"✅ {tarih_str} menüsü kaydedildi!")
                    st.rerun()

        yakin = sorted(
            [(t, m) for t, m in menuler_map.items()
             if t >= (today - timedelta(days=3)).isoformat()],
            key=lambda x: x[0]
        )[:7]
        if yakin:
            st.markdown("---")
            styled_section("Son Girişler", "#ea580c")
            for t_str, m in yakin:
                is_t = t_str == today.isoformat()
                kh = ", ".join(m.get("kahvalti", [])) or "–"
                og = ", ".join(m.get("ogle_yemegi", [])) or "–"
                ik = ", ".join(m.get("ikindi_ara_ogun", [])) or "–"
                with st.expander(f"{'📌 ' if is_t else ''}{t_str}  {'(Bugün)' if is_t else ''}",
                    expanded=is_t
                ):
                    st.markdown(f"☕ **Kahvaltı:** {kh}")
                    st.markdown(f"🍽️ **Öğle:** {og}")
                    st.markdown(f"🍎 **İkindi:** {ik}")
                    if m.get("notlar"):
                        st.caption(f"💡 {m['notlar']}")
                    if st.button("🗑️ Sil", key=f"kh_ym_del_{t_str}", type="secondary"):
                        menuler_map.pop(t_str, None)
                        _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                        st.rerun()

    # ─────────── TAB 2: EXCEL YÜKLE ───────────
    with tab_excel:
        styled_section("Excel ile Aylık Menü Yükle", "#0284c7")
        styled_info_banner(
            "Excel dosyanızın sütunları: A=Tarih (YYYY-AA-GG veya GG.AA.YYYY) | "
            "B=Kahvaltı | C=Öğle Yemeği | D=İkindi Ara Öğün  "
            "Her hücreye yiyecekleri satır satır veya virgülle ayırarak yazabilirsiniz.",
            banner_type="info"
        )

        st.markdown("**📥 Örnek şablon:**")
        ornek_satir = (
            "Tarih\tKahvaltı\tÖğle Yemeği\tİkindi Ara Öğün\n"
            "2026-03-03\tÇay\nPeynir\nZeytin\tMercimek Çorbası\nKuru Fasulye\nPilav\nAyran\tMeyve\nSüt\n"
            "2026-03-04\tSüt\nKakao\nEkmek\tDomates Çorbası\nSpagetti\nSalata\tBisküvi\nMeyve Suyu"
        )
        st.download_button(
            "📥 Örnek Excel Şablonu İndir (TSV)",
            data=ornek_satir.encode("utf-8-sig"),
            file_name="yemek_menusu_sablon.tsv",
            mime="text/tab-separated-values",
        )

        yukle_dosya = st.file_uploader(
            "Excel Dosyası Seç (.xlsx, .xls, .csv)",
            type=["xlsx", "xls", "csv"],
            key="kh_ym_excel_yukle"
        )
        if yukle_dosya:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(yukle_dosya, allowed_types=["xlsx", "xls", "csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                yukle_dosya = None
        if yukle_dosya:
            try:
                if yukle_dosya.name.endswith(".csv"):
                    df = pd.read_csv(yukle_dosya, dtype=str)
                else:
                    df = pd.read_excel(yukle_dosya, dtype=str)

                df.columns = [str(c).strip() for c in df.columns]
                st.dataframe(df.head(10), use_container_width=True)

                tum_sutunlar = list(df.columns)
                em1, em2, em3, em4 = st.columns(4)
                with em1:
                    col_tarih = st.selectbox("Tarih Sütunu", tum_sutunlar, key="kh_ym_col_tarih")
                with em2:
                    col_kahvalti = st.selectbox(
                        "Kahvaltı Sütunu", ["(yok)"] + tum_sutunlar, key="kh_ym_col_kah")
                with em3:
                    col_ogle = st.selectbox(
                        "Öğle Yemeği Sütunu", ["(yok)"] + tum_sutunlar, key="kh_ym_col_ogle")
                with em4:
                    col_ikindi = st.selectbox(
                        "İkindi Sütunu", ["(yok)"] + tum_sutunlar, key="kh_ym_col_ikindi")

                if st.button("📥 İçe Aktar", type="primary", key="kh_ym_import_btn",
                              use_container_width=True):
                    eklenen = 0
                    hatalar = []

                    def _parse_ogun_hucre(val) -> list[str]:
                        if not val or str(val).strip() in ("nan", "None", ""):
                            return []
                        return [x.strip() for x in
                                str(val).replace("\n", ",").split(",") if x.strip()]

                    for _, row in df.iterrows():
                        raw_tarih = str(row.get(col_tarih, "")).strip()
                        if not raw_tarih or raw_tarih in ("nan", "None"):
                            continue
                        tarih_str = None
                        for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
                            try:
                                from datetime import datetime as _dt2
                                tarih_str = _dt2.strptime(raw_tarih, fmt).strftime("%Y-%m-%d")
                                break
                            except ValueError:
                                continue
                        if not tarih_str:
                            hatalar.append(f"Tarih okunamadı: {raw_tarih}")
                            continue

                        kah = _parse_ogun_hucre(row.get(col_kahvalti) if col_kahvalti != "(yok)" else None)
                        og  = _parse_ogun_hucre(row.get(col_ogle) if col_ogle != "(yok)" else None)
                        ik  = _parse_ogun_hucre(row.get(col_ikindi) if col_ikindi != "(yok)" else None)

                        if not any([kah, og, ik]):
                            continue

                        mevcut_k = menuler_map.get(tarih_str, {})
                        kayit = {
                            "id": mevcut_k.get("id", str(uuid.uuid4())[:8]),
                            "tarih": tarih_str,
                            "kahvalti": kah or mevcut_k.get("kahvalti", []),
                            "ogle_yemegi": og or mevcut_k.get("ogle_yemegi", []),
                            "ikindi_ara_ogun": ik or mevcut_k.get("ikindi_ara_ogun", []),
                            "notlar": mevcut_k.get("notlar", ""),
                            "guncelleme": datetime.now().isoformat(),
                        }
                        menuler_map[tarih_str] = kayit
                        eklenen += 1

                    _save_hizmet_json(YEMEK_MENU_DOSYA, list(menuler_map.values()))
                    st.success(f"✅ {eklenen} günlük menü içe aktarıldı!")
                    if hatalar:
                        st.warning("Bazı satırlar atlandı:\n" + "\n".join(hatalar[:5]))
                    st.rerun()

            except Exception as ex:
                st.error(f"Dosya okunamadı: {ex}")

    # ─────────── TAB 3: AYLIK TAKVİM ───────────
    with tab_takvim:
        styled_section("Aylık Menü Takvimi", "#ea580c")
        tk1, tk2 = st.columns(2)
        with tk1:
            goster_ay = st.selectbox("Ay", list(range(1, 13)),
                                      index=today.month - 1,
                                      format_func=lambda x: MONTHS_TR[x - 1],
                                      key="kh_ym_goster_ay")
        with tk2:
            goster_yil = st.selectbox("Yil", [today.year - 1, today.year, today.year + 1],
                                       index=1, key="kh_ym_goster_yil")

        ay_k = f"{goster_yil}-{goster_ay:02d}"
        ay_m = {t: m for t, m in menuler_map.items() if t.startswith(ay_k)}

        if not ay_m:
            styled_info_banner(
                f"{MONTHS_TR[goster_ay - 1]} {goster_yil} için menü kaydı yok.", "info")
        else:
            gunler_tr = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
            cal = calendar.monthcalendar(goster_yil, goster_ay)
            hdr = st.columns(7)
            for i, g in enumerate(gunler_tr):
                with hdr[i]:
                    st.markdown(
                        f"<div style='text-align:center;font-weight:700;"
                        f"color:#6b7280;font-size:0.8rem;'>{g}</div>",
                        unsafe_allow_html=True)
            for week in cal:
                cols = st.columns(7)
                for i, day in enumerate(week):
                    with cols[i]:
                        if day == 0:
                            st.markdown("")
                            continue
                        ts = f"{goster_yil}-{goster_ay:02d}-{day:02d}"
                        m = ay_m.get(ts)
                        is_today = ts == today.isoformat()
                        bg = "#fef3c7" if m else "#111827"
                        if is_today:
                            bg = "#dbeafe"
                        border = "2px solid #3b82f6" if is_today else "1px solid #e5e7eb"
                        if m:
                            og_items = m.get("ogle_yemegi", [])[:3]
                            og_html = "<br>".join(f"• {y}" for y in og_items)
                            kah_count = len(m.get("kahvalti", []))
                            ik_count  = len(m.get("ikindi_ara_ogun", []))
                            badges = ""
                            if kah_count:
                                badges += f'<span style="color:#92400e;font-size:0.6rem;">☕{kah_count}</span> '
                            if ik_count:
                                badges += f'<span style="color:#166534;font-size:0.6rem;">🍎{ik_count}</span>'
                            st.markdown(
                                f'<div style="background:{bg};border:{border};border-radius:8px;'
                                f'padding:0.3rem;min-height:80px;font-size:0.65rem;margin-bottom:0.2rem;">'
                                f'<strong style="color:#94A3B8;">{day}</strong> {badges}<br>'
                                f'<span style="color:#94A3B8;">{og_html}</span>'
                                f'</div>',
                                unsafe_allow_html=True)
                        else:
                            st.markdown(
                                f'<div style="background:{bg};border:{border};border-radius:8px;'
                                f'padding:0.3rem;min-height:80px;font-size:0.65rem;margin-bottom:0.2rem;">'
                                f'<strong style="color:#9ca3af;">{day}</strong>'
                                f'</div>',
                                unsafe_allow_html=True)


# ==================== 3) SERVİS YÖNETİMİ ====================

def _generate_servis_pdf(servisler: list[dict], kurum_adi: str) -> bytes:
    """Tum servis hatlarinin PDF listesini olustur."""
    try:
        from utils.report_utils import ReportPDFGenerator
        pdf = ReportPDFGenerator("Servis Guzergah Listesi", f"{kurum_adi}")
        pdf.add_header(kurum_adi)
        pdf.add_section("Servis Hatlari Ozet")
        import pandas as _pd
        ozet = []
        for s in servisler:
            ogr = max(len(s.get("ogrenci_ids", [])), len(s.get("ogrenci_adlari", [])))
            kap = s.get("kapasite", 0) or 30
            ozet.append({
                "Hat": s.get("hat_adi", "-"),
                "Plaka": s.get("plaka", "-"),
                "Sofor": s.get("sofor_adi", "-"),
                "Telefon": s.get("sofor_tel", "-"),
                "Sabah": s.get("sabah_saat", "-"),
                "Aksam": s.get("aksam_saat", "-"),
                "Ogrenci": f"{ogr}/{kap}",
            })
        if ozet:
            pdf.add_table(_pd.DataFrame(ozet))

        for s in servisler:
            pdf.add_section(f"{s.get('hat_adi', '-')} ({s.get('plaka', '-')})")
            info = (
                f"Sofor: {s.get('sofor_adi', '-')} | Tel: {s.get('sofor_tel', '-')} | "
                f"Hostes: {s.get('hostes_adi', '-') or 'Yok'}\n"
                f"Sabah: {s.get('sabah_saat', '-')} | Aksam: {s.get('aksam_saat', '-')} | "
                f"Kapasite: {s.get('kapasite', '-')}"
            )
            pdf.add_text(info)

            duraklar = s.get("duraklar", [])
            if duraklar:
                durak_rows = [{"Sira": i + 1, "Durak": d.get("ad", "-"), "Saat": d.get("saat", "-")}
                              for i, d in enumerate(duraklar)]
                pdf.add_table(_pd.DataFrame(durak_rows))

            ogrenciler = s.get("ogrenci_adlari", [])
            if ogrenciler:
                pdf.add_text(f"Kayitli Ogrenciler ({len(ogrenciler)}): {', '.join(ogrenciler)}")

        return pdf.generate()
    except Exception:
        return b""


def _ogr_sayisi(s: dict) -> int:
    """Servis hattindaki ogrenci sayisi - FIX: cift sayim hatasi giderildi."""
    return max(len(s.get("ogrenci_ids", [])), len(s.get("ogrenci_adlari", [])))


def _parse_saat(saat_str: str) -> tuple[int, int]:
    """'07:30' -> (7, 30) seklinde parse eder."""
    try:
        parts = saat_str.strip().split(":")
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return 0, 0


def _saat_to_minutes(saat_str: str) -> int:
    """'07:30' -> 450 dakika."""
    h, m = _parse_saat(saat_str)
    return h * 60 + m


GUN_ADLARI_TR = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
GUN_KISA_TR = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]


def _render_admin_servis(store: AkademikDataStore):
    """Servis guzergah, sofor, arac, yoklama, ucret ve raporlama yonetimi."""
    styled_section("Servis / Ulasim Yönetimi", "#10b981")

    sstore = get_servis_store()
    servisler = _load_hizmet_json(SERVIS_DOSYA)

    # ── Özet Metrikler (FIX #1: cift sayim) ──
    toplam_ogrenci = sum(_ogr_sayisi(s) for s in servisler)
    toplam_kapasite = sum(s.get("kapasite", 0) or 30 for s in servisler)
    soforler = sstore.get_soforler(sadece_aktif=True)
    araclar = sstore.get_araclar(sadece_aktif=True)
    dolu_hat = sum(1 for s in servisler if _ogr_sayisi(s) >= (s.get("kapasite", 0) or 30))

    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    with mc1:
        st.metric("Servis Hatti", str(len(servisler)))
    with mc2:
        st.metric("Kayitli Ogrenci", f"{toplam_ogrenci}/{toplam_kapasite}")
    with mc3:
        st.metric("Aktif Sofor", str(len(soforler)))
    with mc4:
        st.metric("Aktif Arac", str(len(araclar)))
    with mc5:
        st.metric("Dolu Hat", str(dolu_hat), delta="Kapasite dolu" if dolu_hat > 0 else None,
                  delta_color="inverse" if dolu_hat > 0 else "off")

    # ── Alt Sekmeler (8 ana sekme) ──
    sv_t1, sv_t2, sv_t3, sv_t4, sv_t5, sv_t6, sv_t7, sv_t8 = st.tabs([
        "  🚌 Hat Yönetimi  ",
        "  🚗 Filo & Personel  ",
        "  ✅ Yoklama  ",
        "  📡 Canli Durum  ",
        "  ⚠️ Olay Kaydi  ",
        "  💰 Ucret Takibi  ",
        "  📊 Raporlar  ",
        "  📱 Veli & PDF  ",
    ])

    # ══════════════════════════════════════════════════
    # SEKME 1 — Hat Yönetimi (mevcut + iyilestirilmis)
    # ══════════════════════════════════════════════════
    with sv_t1:
        # --- Toplu import (#14) ---
        with st.expander("📥 Toplu Ogrenci Atama (Excel/CSV)", expanded=False):
            st.caption("Excel veya CSV dosyasi ile ogrencileri toplu olarak hatlara atayabilirsiniz.")
            st.info("**Format:** Sutunlar: `ogrenci_id`, `hat_adi` veya `hat_id`")
            uploaded = st.file_uploader("Dosya Yukle", type=["csv", "xlsx"], key="kh_sv_toplu_upload")
            if uploaded:
                try:
                    if uploaded.name.endswith(".csv"):
                        df_upload = pd.read_csv(uploaded)
                    else:
                        df_upload = pd.read_excel(uploaded)
                    st.dataframe(df_upload.head(10), use_container_width=True, hide_index=True)

                    if st.button("Toplu Atama Uygula", type="primary", key="kh_sv_toplu_btn"):
                        atanan = 0
                        students = store.get_students()
                        stu_map = {s.id: s.tam_ad for s in students}
                        for _, row in df_upload.iterrows():
                            ogr_id = str(row.get("ogrenci_id", "")).strip()
                            hat_ref = str(row.get("hat_adi", row.get("hat_id", ""))).strip()
                            if not ogr_id or not hat_ref:
                                continue
                            for s in servisler:
                                if s.get("hat_adi") == hat_ref or s.get("id") == hat_ref:
                                    if ogr_id not in s.get("ogrenci_ids", []):
                                        s.setdefault("ogrenci_ids", []).append(ogr_id)
                                        ad = stu_map.get(ogr_id, ogr_id)
                                        s.setdefault("ogrenci_adlari", []).append(ad)
                                        atanan += 1
                                    break
                        _save_hizmet_json(SERVIS_DOSYA, servisler)
                        st.success(f"{atanan} ogrenci atandi!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Dosya okunamadi: {e}")

        # --- Yeni hat ekleme ---
        with st.expander("➕ Yeni Servis Hatti Ekle", expanded=False):
            with st.form("kh_servis_form", clear_on_submit=True):
                sf1, sf2 = st.columns(2)
                with sf1:
                    hat_adi = st.text_input("Hat Adi *", placeholder="Orn: Kadikoy - Okul", key="kh_sv_hat")
                    # Arac secimi (havuzdan)
                    arac_opts = {a.id: f"{a.plaka} ({a.marka} {a.model})" for a in araclar}
                    arac_opts["manual"] = "Elle Gir"
                    sec_arac = st.selectbox("Arac *", list(arac_opts.keys()),
                                            format_func=lambda x: arac_opts.get(x, x), key="kh_sv_arac")
                    manual_plaka = ""
                    if sec_arac == "manual":
                        manual_plaka = st.text_input("Plaka *", key="kh_sv_plaka")
                    # Sofor secimi (havuzdan)
                    sofor_opts = {s.id: f"{s.ad} ({s.telefon})" for s in soforler}
                    sofor_opts["manual"] = "Elle Gir"
                    sec_sofor = st.selectbox("Sofor *", list(sofor_opts.keys()),
                                              format_func=lambda x: sofor_opts.get(x, x), key="kh_sv_sofor_sel")
                    manual_sofor = ""
                    manual_sofor_tel = ""
                    if sec_sofor == "manual":
                        manual_sofor = st.text_input("Sofor Adi *", key="kh_sv_sofor")
                        manual_sofor_tel = st.text_input("Sofor Telefon", key="kh_sv_sofor_tel")
                with sf2:
                    # Hostes secimi
                    hostesler = sstore.get_hostesler(sadece_aktif=True)
                    hostes_opts = {h.id: f"{h.ad} ({h.telefon})" for h in hostesler}
                    hostes_opts["yok"] = "Hostes Yok"
                    hostes_opts["manual"] = "Elle Gir"
                    sec_hostes = st.selectbox("Hostes", list(hostes_opts.keys()),
                                              format_func=lambda x: hostes_opts.get(x, x), key="kh_sv_hostes_sel")
                    manual_hostes = ""
                    if sec_hostes == "manual":
                        manual_hostes = st.text_input("Hostes Adi", key="kh_sv_hostes")
                    sabah_saat = st.text_input("Sabah Alinma Saati", placeholder="07:30", key="kh_sv_sabah")
                    aksam_saat = st.text_input("Aksam Birakma Saati", placeholder="16:30", key="kh_sv_aksam")
                    kapasite = st.number_input("Kapasite", min_value=1, value=30, key="kh_sv_kapasite")
                    # Calisma gunleri (#7)
                    calisma_gun = st.multiselect(
                        "Calisma Gunleri", list(range(7)),
                        default=[0, 1, 2, 3, 4],
                        format_func=lambda x: GUN_ADLARI_TR[x],
                        key="kh_sv_gunler",
                    )

                st.markdown("**Duraklar** (her satira: durak_adi, saat, enlem, boylam)")
                durak_text = st.text_area("Duraklar", height=100,
                                           placeholder="Kadikoy Meydan, 07:30, 40.99, 29.02\nOkul, 08:15",
                                           key="kh_sv_duraklar")

                students = store.get_students()
                student_opts = {s.id: f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in students}
                secili_ogrenciler = st.multiselect("Ogrenciler", list(student_opts.keys()),
                                                   format_func=lambda x: student_opts.get(x, x),
                                                   key="kh_sv_ogrenciler")

                if st.form_submit_button("Kaydet", type="primary"):
                    # Plaka resolve
                    if sec_arac == "manual":
                        plaka_val = manual_plaka
                        arac_id_val = ""
                        kap_val = kapasite
                    else:
                        arac_obj = sstore.get_by_id("araclar", sec_arac)
                        plaka_val = arac_obj.plaka if arac_obj else ""
                        arac_id_val = sec_arac
                        kap_val = arac_obj.kapasite if arac_obj else kapasite
                    # Sofor resolve
                    if sec_sofor == "manual":
                        sofor_adi_val = manual_sofor
                        sofor_tel_val = manual_sofor_tel
                        sofor_id_val = ""
                    else:
                        sof_obj = sstore.get_by_id("soforler", sec_sofor)
                        sofor_adi_val = sof_obj.ad if sof_obj else ""
                        sofor_tel_val = sof_obj.telefon if sof_obj else ""
                        sofor_id_val = sec_sofor
                    # Hostes resolve
                    if sec_hostes == "yok":
                        hostes_adi_val, hostes_id_val = "", ""
                    elif sec_hostes == "manual":
                        hostes_adi_val, hostes_id_val = manual_hostes, ""
                    else:
                        hos_obj = sstore.get_by_id("hostesler", sec_hostes)
                        hostes_adi_val = hos_obj.ad if hos_obj else ""
                        hostes_id_val = sec_hostes

                    if not hat_adi or (not plaka_val and sec_arac == "manual"):
                        st.error("Hat adi ve plaka zorunludur.")
                    else:
                        duraklar = []
                        for line in durak_text.strip().split("\n"):
                            if not line.strip():
                                continue
                            parts = [p.strip() for p in line.split(",")]
                            d = {"ad": parts[0], "saat": parts[1] if len(parts) > 1 else ""}
                            if len(parts) > 2:
                                try:
                                    d["lat"] = float(parts[2])
                                except ValueError:
                                    d["lat"] = 0.0
                            if len(parts) > 3:
                                try:
                                    d["lon"] = float(parts[3])
                                except ValueError:
                                    d["lon"] = 0.0
                            duraklar.append(d)

                        ogrenci_adlari = []
                        for sid in secili_ogrenciler:
                            for s in students:
                                if s.id == sid:
                                    ogrenci_adlari.append(s.tam_ad)
                                    break

                        yeni = {
                            "id": str(uuid.uuid4())[:8],
                            "hat_adi": hat_adi,
                            "arac_id": arac_id_val,
                            "plaka": plaka_val,
                            "sofor_id": sofor_id_val,
                            "sofor_adi": sofor_adi_val,
                            "sofor_tel": sofor_tel_val,
                            "hostes_id": hostes_id_val,
                            "hostes_adi": hostes_adi_val,
                            "sabah_saat": sabah_saat,
                            "aksam_saat": aksam_saat,
                            "kapasite": kap_val,
                            "duraklar": duraklar,
                            "ogrenci_ids": secili_ogrenciler,
                            "ogrenci_adlari": ogrenci_adlari,
                            "calisma_gunleri": calisma_gun,
                            "durum": "garajda",
                        }
                        servisler.append(yeni)
                        _save_hizmet_json(SERVIS_DOSYA, servisler)
                        st.success(f"'{hat_adi}' hatti eklendi!")
                        st.rerun()

        # ── Arama / Filtre ──
        if servisler:
            fi1, fi2 = st.columns([2, 1])
            with fi1:
                arama = st.text_input("🔍 Hat Ara", placeholder="Hat adi, plaka veya sofor...",
                                      key="kh_sv_arama")
            with fi2:
                filtre_durum = st.selectbox("Doluluk Filtre", ["Tumu", "Bos Kontenjan Var", "Dolu"],
                                            key="kh_sv_filtre_doluluk")

            filtered_servisler = servisler
            if arama:
                q = arama.lower()
                filtered_servisler = [s for s in filtered_servisler
                                      if q in s.get("hat_adi", "").lower()
                                      or q in s.get("plaka", "").lower()
                                      or q in s.get("sofor_adi", "").lower()]
            if filtre_durum == "Bos Kontenjan Var":
                filtered_servisler = [s for s in filtered_servisler
                                      if _ogr_sayisi(s) < (s.get("kapasite", 0) or 30)]
            elif filtre_durum == "Dolu":
                filtered_servisler = [s for s in filtered_servisler
                                      if _ogr_sayisi(s) >= (s.get("kapasite", 0) or 30)]

            st.caption(f"{len(filtered_servisler)} hat listeleniyor")
        else:
            filtered_servisler = []

        if not filtered_servisler:
            styled_info_banner("Servis hatti bulunamadi.", "info")
        else:
            for s in filtered_servisler:
                s_id = s.get("id", "")
                ogr_sayi = _ogr_sayisi(s)
                kap = s.get("kapasite", 0) or 30
                doluluk = ogr_sayi / kap if kap > 0 else 0
                doluluk_pct = min(doluluk * 100, 100)
                doluluk_renk = "#10b981" if doluluk < 0.7 else ("#f59e0b" if doluluk < 1.0 else "#ef4444")
                doluluk_text = "DOLU" if doluluk >= 1.0 else f"%{doluluk_pct:.0f}"

                durum_key = s.get("durum", "garajda")
                durum_label, durum_renk = SERVIS_DURUM_MAP.get(durum_key, ("", "#64748b"))

                # Calisma gunu bilgisi (#7)
                c_gunler = s.get("calisma_gunleri", [0, 1, 2, 3, 4])
                gun_str = ", ".join(GUN_KISA_TR[g] for g in sorted(c_gunler) if g < 7)

                with st.expander(f"🚌 {s.get('hat_adi', '-')} | {s.get('plaka', '-')} | {durum_label} | {ogr_sayi}/{kap} ogrenci"):

                    # Doluluk bar
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                        <div style="flex:1;background:#e2e8f0;border-radius:6px;height:10px;overflow:hidden">
                            <div style="width:{doluluk_pct:.0f}%;height:100%;background:{doluluk_renk};
                            border-radius:6px;transition:width 0.3s"></div>
                        </div>
                        <span style="font-size:12px;font-weight:700;color:{doluluk_renk}">{doluluk_text}</span>
                    </div>""", unsafe_allow_html=True)

                    dc1, dc2 = st.columns(2)
                    with dc1:
                        st.markdown(f"""
                        - **Plaka:** {s.get('plaka', '-')}
                        - **Sofor:** {s.get('sofor_adi', '-')} ({s.get('sofor_tel', '-')})
                        - **Hostes:** {s.get('hostes_adi', '-') or 'Yok'}
                        """)
                    with dc2:
                        st.markdown(f"""
                        - **Sabah:** {s.get('sabah_saat', '-')}
                        - **Aksam:** {s.get('aksam_saat', '-')}
                        - **Kapasite:** {ogr_sayi}/{kap}
                        - **Gunler:** {gun_str}
                        """)

                    # Guzergah + Harita (#6)
                    duraklar = s.get("duraklar", [])
                    if duraklar:
                        st.caption("Guzergah:")
                        for idx, d in enumerate(duraklar):
                            icon = "🏠" if idx == 0 else ("🏫" if idx == len(duraklar) - 1 else "📍")
                            coord_str = ""
                            if d.get("lat") and d.get("lon"):
                                coord_str = f" ({d['lat']:.4f}, {d['lon']:.4f})"
                            st.write(f"{icon} {d.get('ad', '-')} — {d.get('saat', '-')}{coord_str}")

                        # Harita gosterimi (#6)
                        harita_duraklar = [d for d in duraklar if d.get("lat") and d.get("lon")]
                        if harita_duraklar:
                            try:
                                map_data = pd.DataFrame([
                                    {"lat": d["lat"], "lon": d["lon"]} for d in harita_duraklar
                                ])
                                st.map(map_data, zoom=12)
                            except Exception:
                                pass

                    # Ogrenci listesi + cikarma
                    ogrenci_ids = s.get("ogrenci_ids", [])
                    ogrenci_adlari = s.get("ogrenci_adlari", [])
                    if ogrenci_adlari:
                        st.caption(f"Kayitli Ogrenciler ({len(ogrenci_adlari)}):")
                        cikarilacak = []
                        for oi, ad in enumerate(ogrenci_adlari):
                            oc1, oc2 = st.columns([4, 1])
                            with oc1:
                                st.write(f"👤 {ad}")
                            with oc2:
                                if st.button("✖", key=f"kh_sv_cikar_{s_id}_{oi}",
                                             help=f"{ad} cikart"):
                                    cikarilacak.append(oi)
                        if cikarilacak:
                            for ci in sorted(cikarilacak, reverse=True):
                                if ci < len(ogrenci_adlari):
                                    ogrenci_adlari.pop(ci)
                                if ci < len(ogrenci_ids):
                                    ogrenci_ids.pop(ci)
                            s["ogrenci_adlari"] = ogrenci_adlari
                            s["ogrenci_ids"] = ogrenci_ids
                            _save_hizmet_json(SERVIS_DOSYA, servisler)
                            st.success("Ogrenci cikarildi!")
                            st.rerun()

                    # Islem butonlari
                    st.divider()

                    # Duzenleme modu
                    edit_key = f"_kh_sv_edit_{s_id}"
                    if st.session_state.get(edit_key, False):
                        st.markdown("**✏️ Hat Bilgilerini Duzenle**")
                        with st.form(f"kh_servis_edit_form_{s_id}"):
                            ef1, ef2 = st.columns(2)
                            with ef1:
                                e_hat = st.text_input("Hat Adi", value=s.get("hat_adi", ""),
                                                      key=f"kh_e_hat_{s_id}")
                                e_plaka = st.text_input("Plaka", value=s.get("plaka", ""),
                                                        key=f"kh_e_plaka_{s_id}")
                                e_sofor = st.text_input("Sofor Adi", value=s.get("sofor_adi", ""),
                                                        key=f"kh_e_sofor_{s_id}")
                                e_tel = st.text_input("Sofor Tel", value=s.get("sofor_tel", ""),
                                                      key=f"kh_e_tel_{s_id}")
                            with ef2:
                                e_hostes = st.text_input("Hostes", value=s.get("hostes_adi", ""),
                                                         key=f"kh_e_hostes_{s_id}")
                                e_sabah = st.text_input("Sabah Saati", value=s.get("sabah_saat", ""),
                                                        key=f"kh_e_sabah_{s_id}")
                                e_aksam = st.text_input("Aksam Saati", value=s.get("aksam_saat", ""),
                                                        key=f"kh_e_aksam_{s_id}")
                                e_kap = st.number_input("Kapasite", min_value=1,
                                                        value=s.get("kapasite", 30) or 30,
                                                        key=f"kh_e_kap_{s_id}")
                            # Calisma gunleri duzenleme (#7)
                            e_gunler = st.multiselect(
                                "Calisma Gunleri", list(range(7)),
                                default=s.get("calisma_gunleri", [0, 1, 2, 3, 4]),
                                format_func=lambda x: GUN_ADLARI_TR[x],
                                key=f"kh_e_gunler_{s_id}",
                            )
                            durak_str = "\n".join(
                                f"{d.get('ad', '')}, {d.get('saat', '')}"
                                + (f", {d.get('lat', '')}, {d.get('lon', '')}" if d.get('lat') else "")
                                for d in s.get("duraklar", [])
                            )
                            e_durak = st.text_area("Duraklar (ad, saat, enlem, boylam)", value=durak_str,
                                                    key=f"kh_e_durak_{s_id}")
                            eb1, eb2 = st.columns(2)
                            with eb1:
                                kaydet = st.form_submit_button("Kaydet", type="primary")
                            with eb2:
                                iptal = st.form_submit_button("Iptal")

                            if kaydet:
                                s["hat_adi"] = e_hat
                                s["plaka"] = e_plaka
                                s["sofor_adi"] = e_sofor
                                s["sofor_tel"] = e_tel
                                s["hostes_adi"] = e_hostes
                                s["sabah_saat"] = e_sabah
                                s["aksam_saat"] = e_aksam
                                s["kapasite"] = e_kap
                                s["calisma_gunleri"] = e_gunler
                                new_duraklar = []
                                for line in e_durak.strip().split("\n"):
                                    if not line.strip():
                                        continue
                                    parts = [p.strip() for p in line.split(",")]
                                    nd = {"ad": parts[0], "saat": parts[1] if len(parts) > 1 else ""}
                                    if len(parts) > 2:
                                        try:
                                            nd["lat"] = float(parts[2])
                                        except ValueError:
                                            pass
                                    if len(parts) > 3:
                                        try:
                                            nd["lon"] = float(parts[3])
                                        except ValueError:
                                            pass
                                    new_duraklar.append(nd)
                                s["duraklar"] = new_duraklar
                                _save_hizmet_json(SERVIS_DOSYA, servisler)
                                st.session_state[edit_key] = False
                                st.success("Hat bilgileri guncellendi!")
                                st.rerun()
                            if iptal:
                                st.session_state[edit_key] = False
                                st.rerun()
                    else:
                        # Ogrenci ekleme + butonlar
                        with st.form(f"kh_servis_ogr_form_{s_id}"):
                            students = store.get_students()
                            mevcut_ids = set(s.get("ogrenci_ids", []))
                            yeni_adaylar = {st_obj.id: f"{st_obj.tam_ad} ({st_obj.sinif}/{st_obj.sube})"
                                            for st_obj in students if st_obj.id not in mevcut_ids}
                            ek_ogrenciler = st.multiselect(
                                "Ogrenci Ekle", list(yeni_adaylar.keys()),
                                format_func=lambda x: yeni_adaylar.get(x, x),
                                key=f"kh_sv_ekle_{s_id}",
                            )
                            bb1, bb2, bb3 = st.columns(3)
                            with bb1:
                                ekle_btn = st.form_submit_button("Ogrenci Ekle", type="primary")
                            with bb2:
                                duzenle_btn = st.form_submit_button("✏️ Duzenle")
                            with bb3:
                                sil_btn = st.form_submit_button("🗑️ Hatti Sil")

                            if ekle_btn and ek_ogrenciler:
                                for sid in ek_ogrenciler:
                                    s.setdefault("ogrenci_ids", []).append(sid)
                                    for st_obj in students:
                                        if st_obj.id == sid:
                                            s.setdefault("ogrenci_adlari", []).append(st_obj.tam_ad)
                                            break
                                _save_hizmet_json(SERVIS_DOSYA, servisler)
                                st.success(f"{len(ek_ogrenciler)} ogrenci eklendi!")
                                st.rerun()

                            if duzenle_btn:
                                st.session_state[edit_key] = True
                                st.rerun()

                            # FIX #3: Silme onay mekanizmasi
                            if sil_btn:
                                st.session_state[f"_kh_sv_sil_onay_{s_id}"] = True
                                st.rerun()

                    # Silme onay dialogu (FIX #3)
                    sil_onay_key = f"_kh_sv_sil_onay_{s_id}"
                    if st.session_state.get(sil_onay_key, False):
                        st.warning(f"**'{s.get('hat_adi', '-')}' hattini silmek istediginize emin misiniz?** "
                                   f"Bu islem geri alinamaz. Hatta kayitli {_ogr_sayisi(s)} ogrenci bulunmaktadir.")
                        onay1, onay2 = st.columns(2)
                        with onay1:
                            if st.button("Evet, Sil", type="primary", key=f"kh_sv_sil_evet_{s_id}"):
                                servisler = [x for x in servisler if x.get("id") != s_id]
                                _save_hizmet_json(SERVIS_DOSYA, servisler)
                                st.session_state[sil_onay_key] = False
                                st.success("Servis hatti silindi!")
                                st.rerun()
                        with onay2:
                            if st.button("Vazgec", key=f"kh_sv_sil_hayir_{s_id}"):
                                st.session_state[sil_onay_key] = False
                                st.rerun()

    # ══════════════════════════════════════════════════
    # SEKME 2 — Filo & Personel (#9, #10)
    # ══════════════════════════════════════════════════
    with sv_t2:
        filo_t1, filo_t2, filo_t3, filo_t4 = st.tabs([
            "  👨‍✈️ Soforler  ", "  👩‍💼 Hostesler  ", "  🚗 Araclar  ", "  🔧 Bakim Takibi  "
        ])

        # ── Sofor Havuzu (#9) ──
        with filo_t1:
            styled_section("Sofor Havuzu", "#3b82f6")
            tum_soforler = sstore.get_soforler()

            sm1, sm2, sm3 = st.columns(3)
            with sm1:
                st.metric("Toplam Sofor", str(len(tum_soforler)))
            with sm2:
                st.metric("Aktif", str(sum(1 for s in tum_soforler if s.durum == "aktif")))
            with sm3:
                # Ehliyet uyarisi
                eh_uyari = sum(1 for s in tum_soforler
                               if s.ehliyet_bitis and s.ehliyet_bitis <= (date.today() + timedelta(days=30)).isoformat())
                st.metric("Ehliyet Uyari (30 gun)", str(eh_uyari),
                          delta="Dikkat!" if eh_uyari > 0 else None, delta_color="inverse")

            with st.expander("➕ Yeni Sofor Ekle", expanded=False):
                with st.form("kh_sofor_form", clear_on_submit=True):
                    sfc1, sfc2 = st.columns(2)
                    with sfc1:
                        sf_ad = st.text_input("Ad Soyad *", key="kh_sof_ad")
                        sf_tel = st.text_input("Telefon", key="kh_sof_tel")
                        sf_ehliyet = st.selectbox("Ehliyet Sinifi", SOFOR_EHLIYET_SINIFLARI,
                                                   index=2, key="kh_sof_ehliyet")
                    with sfc2:
                        sf_ehliyet_no = st.text_input("Ehliyet No", key="kh_sof_ehliyet_no")
                        sf_ehliyet_bitis = st.date_input("Ehliyet Bitis", key="kh_sof_ehliyet_bitis")
                        sf_src = st.checkbox("SRC Belgesi Var", key="kh_sof_src")
                        sf_src_bitis = st.date_input("SRC Bitis", key="kh_sof_src_bitis") if sf_src else None
                    sf_notlar = st.text_area("Notlar", key="kh_sof_notlar", height=68)
                    if st.form_submit_button("Kaydet", type="primary"):
                        if not sf_ad:
                            st.error("Ad soyad zorunludur.")
                        else:
                            yeni_sof = Sofor(
                                ad=sf_ad, telefon=sf_tel, ehliyet_sinif=sf_ehliyet,
                                ehliyet_no=sf_ehliyet_no,
                                ehliyet_bitis=str(sf_ehliyet_bitis),
                                src_belgesi=sf_src,
                                src_bitis=str(sf_src_bitis) if sf_src_bitis else "",
                                notlar=sf_notlar,
                            )
                            sstore.add_object("soforler", yeni_sof)
                            st.success(f"Sofor '{sf_ad}' eklendi!")
                            st.rerun()

            if not tum_soforler:
                styled_info_banner("Henuz sofor kaydi yok.", "info")
            else:
                for sof in tum_soforler:
                    durum_renk = "#10b981" if sof.durum == "aktif" else ("#f59e0b" if sof.durum == "izinli" else "#94a3b8")
                    eh_uyari_str = ""
                    if sof.ehliyet_bitis:
                        try:
                            kalan = (date.fromisoformat(sof.ehliyet_bitis) - date.today()).days
                            if kalan < 0:
                                eh_uyari_str = " ⛔ Suresi Dolmus"
                            elif kalan <= 30:
                                eh_uyari_str = f" ⚠️ {kalan} gun kaldi"
                        except ValueError:
                            pass

                    with st.expander(f"👨‍✈️ {sof.ad} | {sof.ehliyet_sinif} | {sof.durum.title()}{eh_uyari_str}"):
                        st.markdown(f"""
                        - **Telefon:** {sof.telefon or '-'}
                        - **Ehliyet:** {sof.ehliyet_sinif} | No: {sof.ehliyet_no or '-'} | Bitis: {sof.ehliyet_bitis or '-'}
                        - **SRC:** {'Var' if sof.src_belgesi else 'Yok'}{f' (Bitis: {sof.src_bitis})' if sof.src_bitis else ''}
                        - **Notlar:** {sof.notlar or '-'}
                        """)
                        scol1, scol2, scol3 = st.columns(3)
                        with scol1:
                            yeni_d = st.selectbox("Durum", SOFOR_DURUMLARI,
                                                   index=SOFOR_DURUMLARI.index(sof.durum) if sof.durum in SOFOR_DURUMLARI else 0,
                                                   key=f"kh_sof_d_{sof.id}")
                            if st.button("Durum Guncelle", key=f"kh_sof_d_btn_{sof.id}"):
                                sstore.update_object("soforler", sof.id, {"durum": yeni_d})
                                st.success("Durum guncellendi!")
                                st.rerun()
                        with scol3:
                            if st.button("🗑️ Sil", key=f"kh_sof_sil_{sof.id}"):
                                sstore.delete_object("soforler", sof.id)
                                st.success("Sofor silindi!")
                                st.rerun()

        # ── Hostes Havuzu (#9) ──
        with filo_t2:
            styled_section("Hostes Havuzu", "#8b5cf6")
            tum_hostesler = sstore.get_hostesler()

            with st.expander("➕ Yeni Hostes Ekle", expanded=False):
                with st.form("kh_hostes_form", clear_on_submit=True):
                    hf1, hf2 = st.columns(2)
                    with hf1:
                        h_ad = st.text_input("Ad Soyad *", key="kh_hos_ad")
                    with hf2:
                        h_tel = st.text_input("Telefon", key="kh_hos_tel")
                    h_notlar = st.text_area("Notlar", key="kh_hos_notlar", height=68)
                    if st.form_submit_button("Kaydet", type="primary"):
                        if not h_ad:
                            st.error("Ad soyad zorunludur.")
                        else:
                            yeni_hos = Hostes(ad=h_ad, telefon=h_tel, notlar=h_notlar)
                            sstore.add_object("hostesler", yeni_hos)
                            st.success(f"Hostes '{h_ad}' eklendi!")
                            st.rerun()

            if not tum_hostesler:
                styled_info_banner("Henuz hostes kaydi yok.", "info")
            else:
                for hos in tum_hostesler:
                    with st.expander(f"👩‍💼 {hos.ad} | {hos.durum.title()}"):
                        st.markdown(f"- **Telefon:** {hos.telefon or '-'}\n- **Notlar:** {hos.notlar or '-'}")
                        hcol1, hcol2 = st.columns(2)
                        with hcol1:
                            h_yeni_d = st.selectbox("Durum", ["aktif", "izinli", "pasif"],
                                                     index=["aktif", "izinli", "pasif"].index(hos.durum) if hos.durum in ["aktif", "izinli", "pasif"] else 0,
                                                     key=f"kh_hos_d_{hos.id}")
                            if st.button("Guncelle", key=f"kh_hos_d_btn_{hos.id}"):
                                sstore.update_object("hostesler", hos.id, {"durum": h_yeni_d})
                                st.rerun()
                        with hcol2:
                            if st.button("🗑️ Sil", key=f"kh_hos_sil_{hos.id}"):
                                sstore.delete_object("hostesler", hos.id)
                                st.rerun()

        # ── Arac Yonetimi (#10) ──
        with filo_t3:
            styled_section("Arac Filomuz", "#10b981")
            tum_araclar = sstore.get_araclar()

            am1, am2, am3 = st.columns(3)
            with am1:
                st.metric("Toplam Arac", str(len(tum_araclar)))
            with am2:
                st.metric("Aktif", str(sum(1 for a in tum_araclar if a.durum == "aktif")))
            with am3:
                muayene_uyari = sum(1 for a in tum_araclar
                                     if a.muayene_bitis and a.muayene_bitis <= (date.today() + timedelta(days=30)).isoformat())
                st.metric("Muayene Uyari (30 gun)", str(muayene_uyari),
                          delta="Dikkat!" if muayene_uyari > 0 else None, delta_color="inverse")

            with st.expander("➕ Yeni Arac Ekle", expanded=False):
                with st.form("kh_arac_form", clear_on_submit=True):
                    ac1, ac2 = st.columns(2)
                    with ac1:
                        a_plaka = st.text_input("Plaka *", key="kh_ara_plaka")
                        a_marka = st.text_input("Marka", key="kh_ara_marka")
                        a_model = st.text_input("Model", key="kh_ara_model")
                        a_yil = st.number_input("Yil", min_value=2000, max_value=2030, value=2020, key="kh_ara_yil")
                    with ac2:
                        a_kap = st.number_input("Kapasite", min_value=1, value=30, key="kh_ara_kap")
                        a_muayene = st.date_input("Muayene Bitis", key="kh_ara_muayene")
                        a_sigorta = st.date_input("Sigorta Bitis", key="kh_ara_sigorta")
                        a_kasko = st.date_input("Kasko Bitis", key="kh_ara_kasko")
                    a_km = st.number_input("Kilometre", min_value=0, value=0, key="kh_ara_km")
                    if st.form_submit_button("Kaydet", type="primary"):
                        if not a_plaka:
                            st.error("Plaka zorunludur.")
                        else:
                            yeni_arac = Arac(
                                plaka=a_plaka, marka=a_marka, model=a_model, yil=a_yil,
                                kapasite=a_kap, muayene_bitis=str(a_muayene),
                                sigorta_bitis=str(a_sigorta), kasko_bitis=str(a_kasko), km=a_km,
                            )
                            sstore.add_object("araclar", yeni_arac)
                            st.success(f"Arac '{a_plaka}' eklendi!")
                            st.rerun()

            if not tum_araclar:
                styled_info_banner("Henuz arac kaydi yok.", "info")
            else:
                for arac in tum_araclar:
                    durum_emoji = {"aktif": "🟢", "bakimda": "🟡", "arizali": "🔴", "pasif": "⚪"}.get(arac.durum, "⚪")
                    uyari_str = ""
                    if arac.muayene_gecikme is not None and arac.muayene_gecikme > 0:
                        uyari_str += " ⛔ Muayene gecikti"
                    elif arac.muayene_gecikme is not None and arac.muayene_gecikme > -30:
                        uyari_str += f" ⚠️ Muayene {abs(arac.muayene_gecikme)} gun"
                    if arac.sigorta_gecikme is not None and arac.sigorta_gecikme > 0:
                        uyari_str += " ⛔ Sigorta gecikti"

                    with st.expander(f"{durum_emoji} {arac.plaka} | {arac.marka} {arac.model} | {arac.kapasite} kisi{uyari_str}"):
                        st.markdown(f"""
                        - **Plaka:** {arac.plaka} | **Yil:** {arac.yil} | **KM:** {arac.km:,}
                        - **Muayene Bitis:** {arac.muayene_bitis or '-'} | **Sigorta:** {arac.sigorta_bitis or '-'} | **Kasko:** {arac.kasko_bitis or '-'}
                        - **Son Bakim:** {arac.son_bakim_tarih or '-'} | **Sonraki Bakim:** {arac.sonraki_bakim_tarih or '-'}
                        """)
                        arcol1, arcol2 = st.columns(2)
                        with arcol1:
                            a_yeni_d = st.selectbox("Durum", ARAC_DURUMLARI,
                                                     index=ARAC_DURUMLARI.index(arac.durum) if arac.durum in ARAC_DURUMLARI else 0,
                                                     key=f"kh_ara_d_{arac.id}")
                            if st.button("Guncelle", key=f"kh_ara_d_btn_{arac.id}"):
                                sstore.update_object("araclar", arac.id, {"durum": a_yeni_d})
                                st.rerun()
                        with arcol2:
                            if st.button("🗑️ Sil", key=f"kh_ara_sil_{arac.id}"):
                                sstore.delete_object("araclar", arac.id)
                                st.rerun()

        # ── Bakim Takibi (#10) ──
        with filo_t4:
            styled_section("Arac Bakim Takibi", "#f59e0b")
            tum_bakimlar = sstore.get_bakimlar()

            with st.expander("➕ Yeni Bakim Kaydi", expanded=False):
                with st.form("kh_bakim_form", clear_on_submit=True):
                    bk1, bk2 = st.columns(2)
                    with bk1:
                        bk_arac_opts = {a.id: a.plaka for a in tum_araclar}
                        if bk_arac_opts:
                            bk_arac = st.selectbox("Arac", list(bk_arac_opts.keys()),
                                                    format_func=lambda x: bk_arac_opts.get(x, x), key="kh_bkm_arac")
                        else:
                            bk_arac = ""
                            st.info("Once arac ekleyin.")
                        bk_tarih = st.date_input("Tarih", key="kh_bkm_tarih")
                        bk_tip = st.selectbox("Bakim Tipi", BAKIM_TIPLERI, key="kh_bkm_tip")
                    with bk2:
                        bk_maliyet = st.number_input("Maliyet (TL)", min_value=0.0, step=100.0, key="kh_bkm_maliyet")
                        bk_km = st.number_input("KM", min_value=0, key="kh_bkm_km")
                        bk_sonraki = st.date_input("Sonraki Bakim Tarihi", key="kh_bkm_sonraki")
                    bk_aciklama = st.text_area("Aciklama", key="kh_bkm_aciklama", height=68)
                    bk_yapan = st.text_input("Yapan Firma/Kisi", key="kh_bkm_yapan")
                    if st.form_submit_button("Kaydet", type="primary"):
                        if bk_arac:
                            plaka_str = bk_arac_opts.get(bk_arac, "")
                            yeni_bkm = AracBakim(
                                arac_id=bk_arac, arac_plaka=plaka_str,
                                tarih=str(bk_tarih), tip=bk_tip,
                                aciklama=bk_aciklama, maliyet=bk_maliyet,
                                km=bk_km, sonraki_tarih=str(bk_sonraki), yapan=bk_yapan,
                            )
                            sstore.add_object("bakimlar", yeni_bkm)
                            # Arac bilgilerini guncelle
                            sstore.update_object("araclar", bk_arac, {
                                "son_bakim_tarih": str(bk_tarih),
                                "sonraki_bakim_tarih": str(bk_sonraki),
                                "km": bk_km,
                            })
                            st.success("Bakim kaydi eklendi!")
                            st.rerun()

            if not tum_bakimlar:
                styled_info_banner("Henuz bakim kaydi yok.", "info")
            else:
                rows = []
                for bkm in sorted(tum_bakimlar, key=lambda x: x.tarih, reverse=True):
                    rows.append({
                        "Tarih": bkm.tarih,
                        "Arac": bkm.arac_plaka,
                        "Tip": bkm.tip.title(),
                        "Aciklama": bkm.aciklama[:40],
                        "Maliyet": f"{bkm.maliyet:,.0f} TL",
                        "KM": f"{bkm.km:,}",
                        "Yapan": bkm.yapan,
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════
    # SEKME 3 — Yoklama / Binis Takibi (#4)
    # ══════════════════════════════════════════════════
    with sv_t3:
        styled_section("Servis Yoklama / Binis Takibi", "#10b981")

        if not servisler:
            styled_info_banner("Yoklama icin en az bir servis hatti gerekli.", "info")
        else:
            yc1, yc2, yc3 = st.columns(3)
            with yc1:
                yoklama_hat = st.selectbox("Hat Sec", [s.get("hat_adi", "-") for s in servisler],
                                            key="kh_yoklama_hat")
            with yc2:
                yoklama_tarih = st.date_input("Tarih", value=date.today(), key="kh_yoklama_tarih")
            with yc3:
                yoklama_yon = st.selectbox("Yon", ["sabah", "aksam"], key="kh_yoklama_yon",
                                            format_func=lambda x: "Sabah" if x == "sabah" else "Aksam")

            sec_hat_obj = next((s for s in servisler if s.get("hat_adi") == yoklama_hat), None)
            if sec_hat_obj:
                hat_id = sec_hat_obj.get("id", "")
                ogrenci_adlari = sec_hat_obj.get("ogrenci_adlari", [])
                ogrenci_ids = sec_hat_obj.get("ogrenci_ids", [])

                # Mevcut kayitlari yukle
                mevcut_binis = sstore.get_binis_by_tarih(str(yoklama_tarih), hat_id)
                mevcut_map = {}
                for b in mevcut_binis:
                    if b.yon == yoklama_yon:
                        mevcut_map[b.ogrenci_id] = b.durum

                # Tatil kontrolu (#7)
                if sstore.tarih_tatil_mi(str(yoklama_tarih)):
                    styled_info_banner("Bu tarih tatil olarak isaretlenmis — servis calismamaktadir.", "warning")
                elif yoklama_tarih.weekday() not in sec_hat_obj.get("calisma_gunleri", [0, 1, 2, 3, 4]):
                    styled_info_banner(f"Bu hat {GUN_ADLARI_TR[yoklama_tarih.weekday()]} gunu calismamaktadir.", "warning")

                if not ogrenci_adlari:
                    styled_info_banner("Bu hatta kayitli ogrenci yok.", "info")
                else:
                    st.caption(f"{len(ogrenci_adlari)} ogrenci | {len(mevcut_map)} kayit mevcut")

                    with st.form(f"kh_yoklama_form_{hat_id}_{yoklama_tarih}_{yoklama_yon}"):
                        yoklama_verileri = {}
                        for oi in range(len(ogrenci_adlari)):
                            ad = ogrenci_adlari[oi] if oi < len(ogrenci_adlari) else "-"
                            oid = ogrenci_ids[oi] if oi < len(ogrenci_ids) else ""
                            mevcut_d = mevcut_map.get(oid, "bindi")
                            yc1, yc2 = st.columns([3, 2])
                            with yc1:
                                st.write(f"👤 {ad}")
                            with yc2:
                                yoklama_verileri[oid] = st.selectbox(
                                    "Durum", BINIS_DURUMLARI,
                                    index=BINIS_DURUMLARI.index(mevcut_d) if mevcut_d in BINIS_DURUMLARI else 0,
                                    key=f"kh_yk_{hat_id}_{oi}_{yoklama_tarih}_{yoklama_yon}",
                                    label_visibility="collapsed",
                                )

                        if st.form_submit_button("Yoklamayi Kaydet", type="primary"):
                            # Mevcut kayitlari temizle
                            mevcut_tum = sstore.load_list("binis")
                            mevcut_tum = [b for b in mevcut_tum
                                          if not (b.get("hat_id") == hat_id
                                                  and b.get("tarih") == str(yoklama_tarih)
                                                  and b.get("yon") == yoklama_yon)]
                            # Yeni kayitlar ekle
                            simdi = datetime.now().strftime("%H:%M")
                            for oid, durum in yoklama_verileri.items():
                                ad = ""
                                for oi2, oid2 in enumerate(ogrenci_ids):
                                    if oid2 == oid and oi2 < len(ogrenci_adlari):
                                        ad = ogrenci_adlari[oi2]
                                        break
                                kayit = BinisKaydi(
                                    hat_id=hat_id, ogrenci_id=oid, ogrenci_adi=ad,
                                    tarih=str(yoklama_tarih), yon=yoklama_yon,
                                    durum=durum, saat=simdi,
                                )
                                mevcut_tum.append(kayit.to_dict())
                            sstore.save_list("binis", mevcut_tum)
                            st.success(f"{len(yoklama_verileri)} ogrenci yoklamasi kaydedildi!")
                            st.rerun()

                    # Ozet
                    if mevcut_map:
                        bindi_c = sum(1 for d in mevcut_map.values() if d == "bindi")
                        gelmedi_c = sum(1 for d in mevcut_map.values() if d == "gelmedi")
                        oc1, oc2, oc3 = st.columns(3)
                        with oc1:
                            st.metric("Bindi", str(bindi_c))
                        with oc2:
                            st.metric("Gelmedi", str(gelmedi_c))
                        with oc3:
                            oran = bindi_c / len(mevcut_map) * 100 if mevcut_map else 0
                            st.metric("Devam Orani", f"%{oran:.0f}")

    # ══════════════════════════════════════════════════
    # SEKME 4 — Canli Durum (#13 iyilestirilmis)
    # ══════════════════════════════════════════════════
    with sv_t4:
        styled_section("Canli Servis Durum Takibi", "#3b82f6")

        # Tatil / takvim bilgisi (#7)
        bugun_str = date.today().isoformat()
        if sstore.tarih_tatil_mi(bugun_str):
            styled_info_banner("Bugun tatil — servisler calismamaktadir.", "warning")

        # Tatil yonetimi (#7)
        with st.expander("📅 Tatil Gunleri Yonetimi", expanded=False):
            tatiller = sstore.get_tatiller()
            with st.form("kh_tatil_form", clear_on_submit=True):
                tc1, tc2 = st.columns(2)
                with tc1:
                    tat_tarih = st.date_input("Tatil Tarihi", key="kh_tat_tarih")
                with tc2:
                    tat_aciklama = st.text_input("Aciklama", placeholder="Orn: 29 Ekim Cumhuriyet Bayrami",
                                                  key="kh_tat_aciklama")
                if st.form_submit_button("Tatil Ekle"):
                    yeni_tat = TatilKaydi(tarih=str(tat_tarih), aciklama=tat_aciklama)
                    sstore.add_object("tatiller", yeni_tat)
                    st.success("Tatil gunu eklendi!")
                    st.rerun()
            if tatiller:
                for tat in sorted(tatiller, key=lambda x: x.tarih):
                    tc1, tc2 = st.columns([4, 1])
                    with tc1:
                        st.write(f"📅 {tat.tarih} — {tat.aciklama}")
                    with tc2:
                        if st.button("✖", key=f"kh_tat_sil_{tat.id}"):
                            sstore.delete_object("tatiller", tat.id)
                            st.rerun()

        if not servisler:
            styled_info_banner("Servis hatti tanimlanmamis.", "info")
        else:
            st.caption("Her servisin guncel durumunu buradan guncelleyebilir ve takip edebilirsiniz.")

            # Durum ozet kartlari
            durum_sayac = {}
            for s in servisler:
                dk = s.get("durum", "garajda")
                durum_sayac[dk] = durum_sayac.get(dk, 0) + 1

            durum_cols = st.columns(len(SERVIS_DURUM_MAP))
            for i, (dk, (dl, dr)) in enumerate(SERVIS_DURUM_MAP.items()):
                with durum_cols[i]:
                    cnt = durum_sayac.get(dk, 0)
                    st.markdown(f"""<div style="text-align:center;padding:8px;background:{dr}15;
                        border:1px solid {dr}40;border-radius:10px">
                        <div style="font-size:18px;font-weight:800;color:{dr}">{cnt}</div>
                        <div style="font-size:9px;color:{dr}">{dl}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("---")

            for s in servisler:
                s_id = s.get("id", "")
                durum_key = s.get("durum", "garajda")
                durum_label, durum_renk = SERVIS_DURUM_MAP.get(durum_key, ("?", "#64748b"))
                ogr_sayi = _ogr_sayisi(s)

                # Bugun calisiyor mu? (#7)
                c_gunler = s.get("calisma_gunleri", [0, 1, 2, 3, 4])
                bugun_calisiyor = date.today().weekday() in c_gunler and not sstore.tarih_tatil_mi(bugun_str)
                if not bugun_calisiyor:
                    durum_label = "📅 Bugun Kapalı"
                    durum_renk = "#94a3b8"

                st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:12px 16px;
                    margin:6px 0;background:linear-gradient(135deg,{durum_renk}08,{durum_renk}15);
                    border:1px solid {durum_renk}30;border-radius:12px">
                    <div style="font-size:24px">🚌</div>
                    <div style="flex:1">
                        <div style="font-weight:700;color:#94A3B8;font-size:14px">{s.get('hat_adi', '-')}</div>
                        <div style="font-size:11px;color:#64748b">{s.get('plaka', '-')} | Sofor: {s.get('sofor_adi', '-')} | {ogr_sayi} ogrenci</div>
                    </div>
                    <div style="text-align:center">
                        <div style="background:{durum_renk};color:#fff;padding:4px 12px;
                        border-radius:16px;font-size:11px;font-weight:700">{durum_label}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                if bugun_calisiyor:
                    durum_secenekler = list(SERVIS_DURUM_MAP.keys())
                    mevcut_idx = durum_secenekler.index(durum_key) if durum_key in durum_secenekler else 0

                    dc1, dc2, dc3 = st.columns([2, 1, 1])
                    with dc1:
                        yeni_durum = st.selectbox(
                            "Durum Guncelle", durum_secenekler,
                            index=mevcut_idx,
                            format_func=lambda x: SERVIS_DURUM_MAP.get(x, ("?", ""))[0],
                            key=f"kh_sv_durum_{s_id}",
                            label_visibility="collapsed",
                        )
                    with dc2:
                        if st.button("Guncelle", key=f"kh_sv_durum_btn_{s_id}",
                                     use_container_width=True):
                            s["durum"] = yeni_durum
                            s["durum_zaman"] = datetime.now().strftime("%H:%M")
                            _save_hizmet_json(SERVIS_DOSYA, servisler)
                            st.success(f"{s.get('hat_adi', '')} durumu guncellendi!")
                            st.rerun()
                    with dc3:
                        son_guncelleme = s.get("durum_zaman", "")
                        if son_guncelleme:
                            st.caption(f"Son: {son_guncelleme}")

                # Guzergah ilerleme (#13 — saat bazli gercek hesaplama)
                duraklar = s.get("duraklar", [])
                if duraklar and durum_key in ("yolda_sabah", "duraga_vardi", "yolda_aksam"):
                    simdi_dk = datetime.now().hour * 60 + datetime.now().minute
                    progress_html = '<div style="display:flex;align-items:center;gap:4px;margin:4px 0 10px">'
                    for di, d in enumerate(duraklar):
                        durak_dk = _saat_to_minutes(d.get("saat", ""))
                        is_active = durak_dk <= simdi_dk if durak_dk > 0 else (di == 0)
                        clr = durum_renk if is_active else "#e2e8f0"
                        txt_clr = "#fff" if is_active else "#94a3b8"
                        progress_html += f'''<div style="flex:1;text-align:center;padding:4px;
                            background:{clr};color:{txt_clr};border-radius:6px;font-size:9px;
                            font-weight:{'700' if is_active else '400'}">{d.get("ad","")[:12]}</div>'''
                        if di < len(duraklar) - 1:
                            progress_html += f'<div style="color:{clr};font-size:10px">→</div>'
                    progress_html += '</div>'
                    st.markdown(progress_html, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    # SEKME 5 — Olay Kaydi (#5)
    # ══════════════════════════════════════════════════
    with sv_t5:
        styled_section("Olay / Gecikme Kayitlari", "#ef4444")

        olaylar = sstore.get_olaylar()

        om1, om2, om3, om4 = st.columns(4)
        with om1:
            st.metric("Toplam Olay", str(len(olaylar)))
        with om2:
            acik = sum(1 for o in olaylar if o.durum == "acik")
            st.metric("Acik", str(acik))
        with om3:
            gecikme_c = sum(1 for o in olaylar if o.tip == "gecikme")
            st.metric("Gecikme", str(gecikme_c))
        with om4:
            ort_sure = sum(o.sure_dk for o in olaylar if o.sure_dk > 0)
            ort_sure = ort_sure / len([o for o in olaylar if o.sure_dk > 0]) if any(o.sure_dk > 0 for o in olaylar) else 0
            st.metric("Ort. Sure (dk)", f"{ort_sure:.0f}")

        with st.expander("➕ Yeni Olay Kaydi", expanded=False):
            with st.form("kh_olay_form", clear_on_submit=True):
                oc1, oc2 = st.columns(2)
                with oc1:
                    o_hat_opts = {s.get("id", ""): s.get("hat_adi", "-") for s in servisler}
                    o_hat = st.selectbox("Hat", list(o_hat_opts.keys()),
                                          format_func=lambda x: o_hat_opts.get(x, x), key="kh_olay_hat")
                    o_tip = st.selectbox("Olay Tipi", OLAY_TIPLERI, key="kh_olay_tip",
                                          format_func=lambda x: x.replace("_", " ").title())
                    o_ciddiyet = st.selectbox("Ciddiyet", OLAY_CIDDIYET, key="kh_olay_ciddiyet",
                                              format_func=lambda x: x.title())
                with oc2:
                    o_tarih = st.date_input("Tarih", value=date.today(), key="kh_olay_tarih")
                    o_saat = st.text_input("Saat", value=datetime.now().strftime("%H:%M"), key="kh_olay_saat")
                    o_sure = st.number_input("Sure (dk)", min_value=0, value=0, key="kh_olay_sure")
                o_aciklama = st.text_area("Aciklama *", key="kh_olay_aciklama", height=68)
                o_veli_bildirim = st.checkbox("Velilere bildirim gonderilsin mi? (#8)", key="kh_olay_veli")
                if st.form_submit_button("Kaydet", type="primary"):
                    if not o_aciklama:
                        st.error("Aciklama zorunludur.")
                    else:
                        hat_adi_val = o_hat_opts.get(o_hat, "")
                        yeni_olay = OlayKaydi(
                            hat_id=o_hat, hat_adi=hat_adi_val,
                            tarih=str(o_tarih), saat=o_saat,
                            tip=o_tip, ciddiyet=o_ciddiyet,
                            aciklama=o_aciklama, sure_dk=o_sure,
                            veli_bildirim=o_veli_bildirim,
                        )
                        sstore.add_object("olaylar", yeni_olay)

                        # Veli bildirim entegrasyonu (#8)
                        if o_veli_bildirim:
                            try:
                                hat_obj = next((s for s in servisler if s.get("id") == o_hat), None)
                                if hat_obj:
                                    ogr_ids_bildirim = hat_obj.get("ogrenci_ids", [])
                                    ak_store = get_akademik_store()
                                    for ogr_id in ogr_ids_bildirim:
                                        mesaj = VeliMesaj(
                                            sender_type="yonetici",
                                            sender_name="Servis Yonetimi",
                                            receiver_type="veli",
                                            student_id=ogr_id,
                                            konu=f"Servis Olayi: {o_tip.replace('_', ' ').title()}",
                                            icerik=(
                                                f"Sayin Velimiz, {hat_adi_val} hattinda "
                                                f"{o_tip.replace('_', ' ')} yasanmistir. "
                                                f"{o_aciklama}"
                                                f"{f' (Tahmini sure: {o_sure} dk)' if o_sure else ''}"
                                            ),
                                            kategori="duyuru",
                                        )
                                        ak_store.save_veli_mesaj(mesaj)
                            except Exception:
                                pass

                        st.success("Olay kaydi olusturuldu!")
                        st.rerun()

        # Olay listesi
        if not olaylar:
            styled_info_banner("Henuz olay kaydi yok.", "info")
        else:
            # Filtre
            ofc1, ofc2 = st.columns(2)
            with ofc1:
                o_filtre_tip = st.selectbox("Tip Filtre", ["Tumu"] + OLAY_TIPLERI, key="kh_olay_filtre_tip")
            with ofc2:
                o_filtre_durum = st.selectbox("Durum Filtre", ["Tumu", "acik", "cozuldu"], key="kh_olay_filtre_durum")

            filtreli = olaylar
            if o_filtre_tip != "Tumu":
                filtreli = [o for o in filtreli if o.tip == o_filtre_tip]
            if o_filtre_durum != "Tumu":
                filtreli = [o for o in filtreli if o.durum == o_filtre_durum]

            for olay in sorted(filtreli, key=lambda x: (x.tarih, x.saat), reverse=True):
                ciddiyet_renk = {"dusuk": "#10b981", "orta": "#f59e0b", "yuksek": "#ef4444", "kritik": "#dc2626"}.get(olay.ciddiyet, "#64748b")
                durum_badge = "🟢 Cozuldu" if olay.durum == "cozuldu" else "🔴 Acik"
                with st.expander(f"{olay.tarih} {olay.saat} | {olay.hat_adi} | {olay.tip.title()} | {durum_badge}"):
                    st.markdown(f"""
                    - **Ciddiyet:** <span style="color:{ciddiyet_renk};font-weight:700">{olay.ciddiyet.title()}</span>
                    - **Sure:** {olay.sure_dk} dk
                    - **Aciklama:** {olay.aciklama}
                    - **Cozum:** {olay.cozum or 'Henuz cozulmedi'}
                    - **Veli Bildirim:** {'Gonderildi' if olay.veli_bildirim else 'Hayir'}
                    """, unsafe_allow_html=True)
                    if olay.durum == "acik":
                        with st.form(f"kh_olay_cozum_{olay.id}"):
                            cozum_text = st.text_area("Cozum Aciklamasi", key=f"kh_olay_czm_{olay.id}")
                            if st.form_submit_button("Cozuldu Olarak Isaretle"):
                                sstore.update_object("olaylar", olay.id, {
                                    "durum": "cozuldu", "cozum": cozum_text
                                })
                                st.success("Olay cozuldu olarak isaretlendi!")
                                st.rerun()

    # ══════════════════════════════════════════════════
    # SEKME 6 — Ucret Takibi (#11)
    # ══════════════════════════════════════════════════
    with sv_t6:
        styled_section("Servis Ucret Takibi", "#8b5cf6")

        ucretler = sstore.get_ucretler()
        ucret_ozet = sstore.ucret_ozet()

        um1, um2, um3, um4 = st.columns(4)
        with um1:
            st.metric("Kayitli Ogrenci", str(ucret_ozet["ogrenci_sayisi"]))
        with um2:
            st.metric("Toplam Odenen", f"{ucret_ozet['toplam_odenen']:,.0f} TL")
        with um3:
            st.metric("Toplam Borc", f"{ucret_ozet['toplam_borc']:,.0f} TL")
        with um4:
            st.metric("Tahsilat Orani", f"%{ucret_ozet['tahsilat_orani']:.0f}")

        with st.expander("➕ Yeni Ucret Kaydi", expanded=False):
            with st.form("kh_ucret_form", clear_on_submit=True):
                uf1, uf2 = st.columns(2)
                with uf1:
                    u_hat_opts = {s.get("id", ""): s.get("hat_adi", "-") for s in servisler}
                    u_hat = st.selectbox("Hat", list(u_hat_opts.keys()),
                                          format_func=lambda x: u_hat_opts.get(x, x), key="kh_ucr_hat")
                    # Secilen hattaki ogrenciler
                    u_hat_obj = next((s for s in servisler if s.get("id") == u_hat), None)
                    if u_hat_obj:
                        u_ogr_opts = {}
                        for oi, oid in enumerate(u_hat_obj.get("ogrenci_ids", [])):
                            ad = u_hat_obj["ogrenci_adlari"][oi] if oi < len(u_hat_obj.get("ogrenci_adlari", [])) else oid
                            u_ogr_opts[oid] = ad
                        u_ogr = st.selectbox("Ogrenci", list(u_ogr_opts.keys()),
                                              format_func=lambda x: u_ogr_opts.get(x, x), key="kh_ucr_ogr")
                    else:
                        u_ogr = ""
                        st.info("Hatta ogrenci yok.")
                with uf2:
                    u_donem = st.text_input("Donem", value="2025-2026", key="kh_ucr_donem")
                    u_aylik = st.number_input("Aylik Ucret (TL)", min_value=0.0, step=100.0, key="kh_ucr_aylik")
                    u_ay_secim = st.multiselect("Odemeler Olusturulacak Aylar", AYLAR_TR,
                                                 default=["Eylul", "Ekim", "Kasim", "Aralik",
                                                          "Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran"],
                                                 key="kh_ucr_aylar")
                if st.form_submit_button("Kaydet", type="primary"):
                    if u_ogr and u_aylik > 0:
                        ogr_adi = u_ogr_opts.get(u_ogr, u_ogr) if u_hat_obj else u_ogr
                        odemeler = [{"ay": ay, "tutar": u_aylik, "durum": "beklemede", "tarih": ""} for ay in u_ay_secim]
                        yeni_ucret = ServisUcret(
                            ogrenci_id=u_ogr, ogrenci_adi=ogr_adi,
                            hat_id=u_hat, hat_adi=u_hat_opts.get(u_hat, ""),
                            donem=u_donem, aylik_ucret=u_aylik, odemeler=odemeler,
                        )
                        sstore.add_object("ucretler", yeni_ucret)
                        st.success("Ucret kaydi olusturuldu!")
                        st.rerun()

        if not ucretler:
            styled_info_banner("Henuz ucret kaydi yok.", "info")
        else:
            # Filtre
            ucr_filtre = st.selectbox("Hat Filtre", ["Tumu"] + [s.get("hat_adi", "") for s in servisler],
                                       key="kh_ucr_filtre")
            filtreli_ucr = ucretler
            if ucr_filtre != "Tumu":
                filtreli_ucr = [u for u in ucretler if u.hat_adi == ucr_filtre]

            for ucr in filtreli_ucr:
                odenen = ucr.toplam_odenen
                borc = ucr.toplam_borclu
                toplam = odenen + borc
                oran = (odenen / toplam * 100) if toplam > 0 else 0
                oran_renk = "#10b981" if oran >= 80 else ("#f59e0b" if oran >= 50 else "#ef4444")

                with st.expander(f"👤 {ucr.ogrenci_adi} | {ucr.hat_adi} | %{oran:.0f} odendi"):
                    st.markdown(f"**Donem:** {ucr.donem} | **Aylik:** {ucr.aylik_ucret:,.0f} TL | "
                                f"**Odenen:** {odenen:,.0f} TL | **Kalan:** {borc:,.0f} TL")

                    # Aylık odeme durumu
                    for oi, odeme in enumerate(ucr.odemeler):
                        ay = odeme.get("ay", "")
                        durum = odeme.get("durum", "beklemede")
                        durum_emoji = {"odendi": "✅", "beklemede": "⏳", "gecikti": "🔴", "muaf": "🔵"}.get(durum, "⏳")
                        pcol1, pcol2, pcol3 = st.columns([2, 2, 1])
                        with pcol1:
                            st.write(f"{durum_emoji} {ay}: {odeme.get('tutar', 0):,.0f} TL")
                        with pcol2:
                            yeni_odeme_d = st.selectbox(
                                "Durum", ODEME_DURUMLARI,
                                index=ODEME_DURUMLARI.index(durum) if durum in ODEME_DURUMLARI else 0,
                                key=f"kh_ucr_od_{ucr.id}_{oi}",
                                label_visibility="collapsed",
                            )
                        with pcol3:
                            if st.button("Guncelle", key=f"kh_ucr_od_btn_{ucr.id}_{oi}"):
                                tum_ucretler = sstore.load_list("ucretler")
                                for u_item in tum_ucretler:
                                    if u_item.get("id") == ucr.id:
                                        if oi < len(u_item.get("odemeler", [])):
                                            u_item["odemeler"][oi]["durum"] = yeni_odeme_d
                                            if yeni_odeme_d == "odendi":
                                                u_item["odemeler"][oi]["tarih"] = date.today().isoformat()
                                sstore.save_list("ucretler", tum_ucretler)
                                st.rerun()

    # ══════════════════════════════════════════════════
    # SEKME 7 — Raporlar (#12)
    # ══════════════════════════════════════════════════
    with sv_t7:
        styled_section("Servis Raporlari", "#6366f1")

        rap_t1, rap_t2, rap_t3, rap_t4 = st.tabs([
            "  📊 Doluluk  ", "  ✅ Devam  ", "  ⚠️ Olaylar  ", "  💰 Tahsilat  "
        ])

        # --- Doluluk Raporu ---
        with rap_t1:
            if not servisler:
                styled_info_banner("Rapor icin servis hatti gerekli.", "info")
            else:
                rows = []
                for s in servisler:
                    ogr = _ogr_sayisi(s)
                    kap = s.get("kapasite", 0) or 30
                    oran = ogr / kap * 100 if kap > 0 else 0
                    rows.append({
                        "Hat": s.get("hat_adi", "-"),
                        "Plaka": s.get("plaka", "-"),
                        "Ogrenci": ogr,
                        "Kapasite": kap,
                        "Doluluk (%)": round(oran, 1),
                        "Bos Kontenjan": max(kap - ogr, 0),
                    })
                df_dol = pd.DataFrame(rows)
                st.dataframe(df_dol, use_container_width=True, hide_index=True)

                # Doluluk grafigi
                try:
                    import plotly.express as px
                    fig = px.bar(df_dol, x="Hat", y="Doluluk (%)",
                                 color="Doluluk (%)",
                                 color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"],
                                 range_color=[0, 100])
                    fig.update_layout(height=300, margin=dict(t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                except ImportError:
                    st.bar_chart(df_dol.set_index("Hat")["Doluluk (%)"])

        # --- Devam/Yoklama Raporu ---
        with rap_t2:
            rc1, rc2 = st.columns(2)
            with rc1:
                rap_baslangic = st.date_input("Baslangic", value=date.today() - timedelta(days=30),
                                               key="kh_rap_baslangic")
            with rc2:
                rap_bitis = st.date_input("Bitis", value=date.today(), key="kh_rap_bitis")

            devam_rows = []
            for s in servisler:
                hat_id = s.get("id", "")
                istat = sstore.hat_binis_istatistik(hat_id, str(rap_baslangic), str(rap_bitis))
                devam_rows.append({
                    "Hat": s.get("hat_adi", "-"),
                    "Toplam Kayit": istat["toplam_kayit"],
                    "Bindi": istat["bindi"],
                    "Gelmedi": istat["gelmedi"],
                    "Devam Orani (%)": round(istat["devam_orani"], 1),
                })
            if devam_rows:
                st.dataframe(pd.DataFrame(devam_rows), use_container_width=True, hide_index=True)
            else:
                styled_info_banner("Yoklama verisi bulunamadi.", "info")

        # --- Olay Raporu ---
        with rap_t3:
            olaylar_tum = sstore.get_olaylar()
            if not olaylar_tum:
                styled_info_banner("Olay kaydi yok.", "info")
            else:
                olay_rows = []
                for o in sorted(olaylar_tum, key=lambda x: x.tarih, reverse=True)[:50]:
                    olay_rows.append({
                        "Tarih": o.tarih,
                        "Hat": o.hat_adi,
                        "Tip": o.tip.title(),
                        "Ciddiyet": o.ciddiyet.title(),
                        "Sure (dk)": o.sure_dk,
                        "Durum": o.durum.title(),
                    })
                st.dataframe(pd.DataFrame(olay_rows), use_container_width=True, hide_index=True)

                # Tip dagilimi
                tip_sayac = {}
                for o in olaylar_tum:
                    tip_sayac[o.tip] = tip_sayac.get(o.tip, 0) + 1
                if tip_sayac:
                    try:
                        import plotly.express as px
                        fig = px.pie(names=list(tip_sayac.keys()), values=list(tip_sayac.values()),
                                     title="Olay Tipi Dagilimi")
                        fig.update_layout(height=300, margin=dict(t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                    except ImportError:
                        st.bar_chart(pd.Series(tip_sayac))

        # --- Tahsilat Raporu ---
        with rap_t4:
            ucretler_tum = sstore.get_ucretler()
            if not ucretler_tum:
                styled_info_banner("Ucret kaydi yok.", "info")
            else:
                tah_rows = []
                for u in ucretler_tum:
                    tah_rows.append({
                        "Ogrenci": u.ogrenci_adi,
                        "Hat": u.hat_adi,
                        "Donem": u.donem,
                        "Aylik": f"{u.aylik_ucret:,.0f}",
                        "Odenen": f"{u.toplam_odenen:,.0f}",
                        "Kalan Borc": f"{u.toplam_borclu:,.0f}",
                        "Tahsilat %": f"{(u.toplam_odenen / (u.toplam_odenen + u.toplam_borclu) * 100) if (u.toplam_odenen + u.toplam_borclu) > 0 else 0:.0f}",
                    })
                st.dataframe(pd.DataFrame(tah_rows), use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════
    # SEKME 8 — Veli & PDF (mevcut + iyilestirilmis)
    # ══════════════════════════════════════════════════
    with sv_t8:
        vp_t1, vp_t2 = st.tabs(["  📋 PDF Listesi  ", "  📱 Veli Bilgilendirme  "])

        with vp_t1:
            styled_section("Servis Listesi PDF", "#8b5cf6")
            if not servisler:
                styled_info_banner("PDF olusturmak icin en az bir servis hatti ekleyin.", "info")
            else:
                from utils.shared_data import load_kurum_profili
                kp = load_kurum_profili()
                k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

                st.info(f"**{len(servisler)}** servis hatti ve **{toplam_ogrenci}** ogrenci iceren "
                        f"kurumsal PDF raporu olusturun.")

                pdf_bytes = _generate_servis_pdf(servisler, k_adi)
                if pdf_bytes:
                    st.download_button(
                        "📄 Servis Listesi PDF Indir",
                        data=pdf_bytes,
                        file_name=f"Servis_Listesi_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="kh_sv_pdf_dl",
                        use_container_width=True,
                    )
                else:
                    st.warning("PDF olusturulamadi. ReportLab kurulu oldugundan emin olun.")

                # Hat bazli ozet tablosu
                rows = []
                for s in servisler:
                    ogr = _ogr_sayisi(s)
                    kap = s.get("kapasite", 0) or 30
                    rows.append({
                        "Hat": s.get("hat_adi", "-"),
                        "Plaka": s.get("plaka", "-"),
                        "Sofor": s.get("sofor_adi", "-"),
                        "Sabah": s.get("sabah_saat", "-"),
                        "Aksam": s.get("aksam_saat", "-"),
                        "Ogrenci": ogr,
                        "Kapasite": kap,
                        "Doluluk": f"%{ogr / kap * 100:.0f}" if kap else "-",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with vp_t2:
            styled_section("Veli Bilgilendirme Metni", "#f59e0b")
            if not servisler:
                styled_info_banner("Hat bulunamadi.", "info")
            else:
                sec_hat = st.selectbox("Hat Sec", [s.get("hat_adi", "-") for s in servisler],
                                       key="kh_sv_veli_hat")
                sec_servis = next((s for s in servisler if s.get("hat_adi") == sec_hat), None)

                if sec_servis:
                    ogr_sayi = _ogr_sayisi(sec_servis)
                    duraklar = sec_servis.get("duraklar", [])
                    durak_str = " → ".join(d.get("ad", "") for d in duraklar) if duraklar else "Belirtilmemis"
                    durak_detail = "\n".join(
                        f"  * {d.get('ad', '-')}: {d.get('saat', '-')}" for d in duraklar
                    ) if duraklar else ""

                    veli_metin = (
                        f"Sayin Velimiz,\n\n"
                        f"Ogrencimizin servisi hakkinda bilgilendirme:\n\n"
                        f"Hat: {sec_servis.get('hat_adi', '-')}\n"
                        f"Plaka: {sec_servis.get('plaka', '-')}\n"
                        f"Sofor: {sec_servis.get('sofor_adi', '-')}\n"
                        f"Sofor Telefon: {sec_servis.get('sofor_tel', '-')}\n"
                        f"Hostes: {sec_servis.get('hostes_adi', '-') or 'Bulunmamaktadir'}\n\n"
                        f"Sabah Alinma Saati: {sec_servis.get('sabah_saat', '-')}\n"
                        f"Aksam Birakma Saati: {sec_servis.get('aksam_saat', '-')}\n\n"
                        f"Guzergah: {durak_str}\n"
                        f"{durak_detail}\n\n"
                        f"Serviste {ogr_sayi} ogrenci bulunmaktadir.\n\n"
                        f"Herhangi bir sorunuz icin okul idaresi ile iletisime gecebilirsiniz.\n\n"
                        f"Saygilarimizla."
                    )

                    st.text_area("Veli Bilgilendirme Metni", value=veli_metin, height=350,
                                 key="kh_sv_veli_metin")
                    vc1, vc2 = st.columns(2)
                    with vc1:
                        st.download_button(
                            "📄 Metin Olarak Indir",
                            data=veli_metin.encode("utf-8"),
                            file_name=f"Servis_Bilgi_{sec_hat.replace(' ', '_')}.txt",
                            mime="text/plain",
                            key="kh_sv_veli_txt",
                            use_container_width=True,
                        )
                    with vc2:
                        if st.button("📋 Panoya Kopyala", key="kh_sv_veli_copy",
                                     use_container_width=True):
                            st.code(veli_metin, language=None)
                            st.success("Metin yukarida goruntulendi — kopyalayabilirsiniz.")


# ==================== 4) VELİ TALEP YÖNETİMİ (RANDEVU + BELGE) ====================

def _render_admin_veli_talepler(store: AkademikDataStore):
    """Veli randevu ve belge taleplerini yonetme ekrani."""
    vt1, vt2 = st.tabs(["  📅 Randevu Talepleri  ", "  📄 Belge Talepleri  "])

    with vt1:
        _render_admin_randevu_talepler(store)
    with vt2:
        _render_admin_belge_talepler()


def _render_admin_randevu_talepler(store: AkademikDataStore):
    """Velilerin gonderdigi randevu taleplerini yonet."""
    styled_section("Veli Randevu Talepleri", "#8b5cf6")

    randevular = _load_hizmet_json(RANDEVU_DOSYA)

    if not randevular:
        styled_info_banner("Henuz randevu talebi bulunmuyor.", "info")
        return

    bekleyen = [r for r in randevular if r.get("durum") == "beklemede"]
    onaylanan = [r for r in randevular if r.get("durum") == "onaylandi"]
    reddedilen = [r for r in randevular if r.get("durum") == "reddedildi"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam", str(len(randevular)))
    with c2:
        st.metric("Bekleyen", str(len(bekleyen)))
    with c3:
        st.metric("Onaylanan", str(len(onaylanan)))
    with c4:
        st.metric("Reddedilen", str(len(reddedilen)))

    if bekleyen:
        styled_section("Bekleyen Talepler", "#f59e0b")
        for r in sorted(bekleyen, key=lambda x: x.get("tarih", ""), reverse=True):
            with st.expander(f"⏳ {r.get('veli_adi', '-')} → {r.get('ogretmen_adi', '-')} | "
                f"{r.get('tarih', '-')} {r.get('saat', '-')}"
            ):
                st.markdown(f"""
                - **Veli:** {r.get('veli_adi', '-')}
                - **Öğrenci:** {r.get('ogrenci_adi', '-')}
                - **Öğretmen:** {r.get('ogretmen_adi', '-')}
                - **Tarih/Saat:** {r.get('tarih', '-')} / {r.get('saat', '-')}
                - **Konu:** {r.get('konu', '-')}
                """)
                ac1, ac2 = st.columns(2)
                with ac1:
                    if st.button("Onayla", key=f"kh_rv_onayla_{r.get('id', '')}",
                                 type="primary", use_container_width=True):
                        r["durum"] = "onaylandi"
                        r["islem_tarihi"] = datetime.now().isoformat()
                        _save_hizmet_json(RANDEVU_DOSYA, randevular)
                        st.success("Randevu onaylandi!")
                        st.rerun()
                with ac2:
                    if st.button("Reddet", key=f"kh_rv_reddet_{r.get('id', '')}",
                                 type="secondary", use_container_width=True):
                        r["durum"] = "reddedildi"
                        r["islem_tarihi"] = datetime.now().isoformat()
                        _save_hizmet_json(RANDEVU_DOSYA, randevular)
                        st.warning("Randevu reddedildi.")
                        st.rerun()

    styled_section("Tüm Randevular", "#6366f1")
    if randevular:
        rows = []
        for r in sorted(randevular, key=lambda x: x.get("tarih", ""), reverse=True):
            durum = r.get("durum", "beklemede")
            durum_icon = {"beklemede": "⏳", "onaylandi": "✅", "reddedildi": "❌"}.get(durum, "❓")
            rows.append({
                "Durum": f"{durum_icon} {durum.capitalize()}",
                "Veli": r.get("veli_adi", "-"),
                "Öğrenci": r.get("ogrenci_adi", "-"),
                "Öğretmen": r.get("ogretmen_adi", "-"),
                "Tarih": r.get("tarih", "-"),
                "Saat": r.get("saat", "-"),
                "Konu": r.get("konu", "-"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_admin_belge_talepler():
    """Veli belge taleplerini yonet (durum guncelleme)."""
    styled_section("Veli Belge Talepleri", "#0ea5e9")

    talepler = _load_hizmet_json(BELGE_TALEP_DOSYA)

    if not talepler:
        styled_info_banner("Henuz belge talebi bulunmuyor.", "info")
        return

    bekleyen = [t for t in talepler if t.get("durum") == "beklemede"]
    hazirlanan = [t for t in talepler if t.get("durum") == "hazirlaniyor"]
    tamamlanan = [t for t in talepler if t.get("durum") == "tamamlandı"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam", str(len(talepler)))
    with c2:
        st.metric("Bekleyen", str(len(bekleyen)))
    with c3:
        st.metric("Hazirlaniyor", str(len(hazirlanan)))
    with c4:
        st.metric("Tamamlandı", str(len(tamamlanan)))

    islem_bekleyen = [t for t in talepler if t.get("durum") != "tamamlandı"]
    if islem_bekleyen:
        styled_section("İşlem Bekleyen Talepler", "#f59e0b")
        for t in sorted(islem_bekleyen, key=lambda x: x.get("talep_tarihi", ""), reverse=True):
            durum = t.get("durum", "beklemede")
            durum_icon = {"beklemede": "⏳", "hazirlaniyor": "🔄", "tamamlandı": "✅"}.get(durum, "❓")
            belge_adi = BELGE_TURLERI_MAP.get(t.get("belge_turu", ""), t.get("belge_turu", "-"))

            with st.expander(f"{durum_icon} {t.get('veli_adi', '-')} | {belge_adi} | "
                f"{t.get('talep_tarihi', '-')}"
            ):
                st.markdown(f"""
                - **Veli:** {t.get('veli_adi', '-')}
                - **Öğrenci:** {t.get('ogrenci_adi', '-')}
                - **Belge:** {belge_adi}
                - **Talep Tarihi:** {t.get('talep_tarihi', '-')}
                - **Aciklama:** {t.get('aciklama', '-')}
                - **Mevcut Durum:** {durum.capitalize()}
                """)

                yeni_durum = st.selectbox(
                    "Durumu Güncelle",
                    ["beklemede", "hazirlaniyor", "tamamlandı"],
                    index=["beklemede", "hazirlaniyor", "tamamlandı"].index(durum),
                    format_func=lambda x: {"beklemede": "Beklemede", "hazirlaniyor": "Hazirlaniyor",
                                           "tamamlandı": "Tamamlandı"}.get(x, x),
                    key=f"kh_bt_durum_{t.get('id', '')}",
                )
                if st.button("Güncelle", key=f"kh_bt_guncelle_{t.get('id', '')}",
                             type="primary"):
                    t["durum"] = yeni_durum
                    t["islem_tarihi"] = datetime.now().isoformat()
                    _save_hizmet_json(BELGE_TALEP_DOSYA, talepler)
                    st.success(f"Durum '{yeni_durum}' olarak güncellendi!")
                    st.rerun()

    styled_section("Tüm Belge Talepleri", "#0891b2")
    rows = []
    for t in sorted(talepler, key=lambda x: x.get("talep_tarihi", ""), reverse=True):
        durum = t.get("durum", "beklemede")
        durum_icon = {"beklemede": "⏳", "hazirlaniyor": "🔄", "tamamlandı": "✅"}.get(durum, "❓")
        rows.append({
            "Durum": f"{durum_icon} {durum.capitalize()}",
            "Veli": t.get("veli_adi", "-"),
            "Öğrenci": t.get("ogrenci_adi", "-"),
            "Belge": BELGE_TURLERI_MAP.get(t.get("belge_turu", ""), t.get("belge_turu", "-")),
            "Talep": t.get("talep_tarihi", "-"),
            "İşlem": t.get("islem_tarihi", "-"),
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ==================== MESAJ SİSTEMİ ====================

def _get_user_display_name(user: dict) -> str:
    """Auth kullanıcısından görünen ad döner; yoksa boş string."""
    name = (user.get("name") or "").strip()
    if name:
        return name
    ad = (user.get("ad") or user.get("first_name") or "").strip()
    soyad = (user.get("soyad") or user.get("last_name") or "").strip()
    return f"{ad} {soyad}".strip()


def _mesaj_puan_badge(m, durum: str) -> str:
    if durum == "yeni":
        return ('<span style="background:#fef2f2;color:#ef4444;padding:2px 8px;'
                'border-radius:6px;font-size:10px;font-weight:700;">Yeni</span>')
    return ('<span style="background:#ecfdf5;color:#10b981;padding:2px 8px;'
            'border-radius:6px;font-size:10px;">Okundu</span>')


def _resolve_ik_receiver_id(emp: dict) -> str:
    """IK çalışanı için mesaj alıcı ID'sini bul.

    Sıralama: auth email eşleşmesi → auth ad-soyad eşleşmesi → emp.id
    Bu sayede employee kendi auth username'iyle girip mesajını görebilir.
    """
    emp_email = (emp.get("email") or "").strip().lower()
    emp_ad = f"{emp.get('ad', '')} {emp.get('soyad', '')}".strip().lower()
    try:
        from utils.auth import get_all_users
        for u in get_all_users():
            if emp_email and (u.get("email") or "").strip().lower() == emp_email:
                return u["username"]
            if emp_ad and (u.get("name") or "").strip().lower() == emp_ad:
                return u["username"]
    except Exception:
        pass
    return emp.get("id", emp_ad)


def _resolve_veli_auth_username(veli_adi: str) -> str | None:
    """Veli adından auth sistemindeki username'i bul.

    Mantık: auth kullanıcıları içinde role==Veli olanların name alanını
    veli_adi ile karşılaştır (kısmi eşleşme). Bulunursa username döndür.
    """
    if not veli_adi:
        return None
    name_lower = veli_adi.strip().lower()
    try:
        from utils.auth import get_all_users
        for u in get_all_users():
            if u.get("role") == "Veli":
                u_name = (u.get("name") or "").strip().lower()
                if u_name and (u_name in name_lower or name_lower in u_name):
                    return u["username"]
    except Exception:
        pass
    return None


def _resolve_ogrenci_auth_username(ogrenci_ad: str, ogrenci_no: str = "") -> str | None:
    """Öğrenci adından/numarasından auth sistemindeki username'i bul."""
    if not ogrenci_ad and not ogrenci_no:
        return None
    ad_lower = ogrenci_ad.strip().lower()
    try:
        from utils.auth import get_all_users
        for u in get_all_users():
            if u.get("role") == "Öğrenci":
                # Numara eşleşmesi daha güvenilir
                if ogrenci_no and str(u.get("student_id") or u.get("numara") or "") == str(ogrenci_no):
                    return u["username"]
                # Ad-soyad eşleşmesi
                u_name = (u.get("name") or "").strip().lower()
                if u_name and ad_lower and (u_name in ad_lower or ad_lower in u_name):
                    return u["username"]
    except Exception:
        pass
    return None


def _lookup_kisi_detay(user_id: str, user_tip: str, store: AkademikDataStore) -> dict:
    """Kullanıcı ID ve tipine göre ad, soyad, branş/pozisyon döndür.

    Dönen dict: {ad, soyad, ad_soyad, brans}
    """
    ad = soyad = brans = ""

    # 1. Öğretmen
    try:
        for t in store.get_teachers():
            if t.id == user_id or getattr(t, "username", "") == user_id:
                ad = getattr(t, "ad", "")
                soyad = getattr(t, "soyad", "")
                brans = getattr(t, "brans", "")
                return {"ad": ad, "soyad": soyad,
                        "ad_soyad": f"{ad} {soyad}".strip(), "brans": brans}
    except Exception:
        pass

    # 2. IK çalışanı
    try:
        from utils.shared_data import load_ik_active_employees
        for e in load_ik_active_employees():
            if e.get("id") == user_id or e.get("username") == user_id:
                tam = e.get("name") or f"{e.get('ad','')} {e.get('soyad','')}".strip()
                parts = tam.split(" ", 1)
                ad = parts[0]
                soyad = parts[1] if len(parts) > 1 else ""
                brans = e.get("pozisyon") or e.get("brans") or e.get("departman") or ""
                return {"ad": ad, "soyad": soyad,
                        "ad_soyad": tam, "brans": brans}
    except Exception:
        pass

    # 3. Öğrenci (ad/soyad/sınıf)
    try:
        for s in store.get_students():
            if s.id == user_id:
                ad = getattr(s, "ad", "")
                soyad = getattr(s, "soyad", "")
                brans = f"{s.sinif}/{s.sube}"
                return {"ad": ad, "soyad": soyad,
                        "ad_soyad": f"{ad} {soyad}".strip(), "brans": brans}
    except Exception:
        pass

    # 4. Auth kullanıcısı (ad en azından ad_soyad olarak)
    try:
        from utils.auth import get_all_users
        for u in get_all_users():
            if u.get("username") == user_id:
                tam = u.get("name", user_id)
                parts = tam.split(" ", 1)
                ad = parts[0]
                soyad = parts[1] if len(parts) > 1 else ""
                brans = u.get("role", "")
                return {"ad": ad, "soyad": soyad,
                        "ad_soyad": tam, "brans": brans}
    except Exception:
        pass

    return {"ad": user_id, "soyad": "", "ad_soyad": user_id, "brans": ""}


def _render_goruldu_raporu(raw_item: dict, store: AkademikDataStore):
    """Tek mesaj için görüldü/görülmedi raporu tablosu."""
    is_grup = raw_item.get("is_group_message", False)
    kat_map = dict(MESAJ_KATEGORILERI)

    # ── Mesaj özet bilgisi ──────────────────────────────────────────
    konu = raw_item.get("konu", "-")
    tarih = (raw_item.get("created_at", "")[:16] or "-").replace("T", " ")
    kat_label = kat_map.get(raw_item.get("kategori", ""), raw_item.get("kategori", "-"))
    icerik = raw_item.get("icerik", "")
    st.markdown(
        f'<div style="background:#111827;border-radius:8px;padding:10px 14px;margin-bottom:10px;'
        f'border-left:3px solid #6366f1;">'
        f'<span style="font-size:11px;color:#64748b;">Konu: </span>'
        f'<b style="font-size:12px;">{konu}</b>&nbsp;&nbsp;'
        f'<span style="font-size:10px;color:#94a3b8;">{kat_label} · {tarih}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if icerik:
        with st.expander("Mesaj İçeriği", expanded=False):
            st.write(icerik)

    # ── Alıcı listesi ve okundu durumu ─────────────────────────────
    if is_grup:
        recipient_details = raw_item.get("recipient_details", [])  # [{id, ad, tip}]
        okundu_by = set(raw_item.get("okundu_by", []))
        goruldu_list = []
        for r in recipient_details:
            rid = r.get("id", "")
            detay = _lookup_kisi_detay(rid, r.get("tip", ""), store)
            goruldu = rid in okundu_by
            goruldu_list.append({
                "id": rid,
                "ad": detay["ad"],
                "soyad": detay["soyad"],
                "ad_soyad": detay["ad_soyad"] or r.get("ad", rid),
                "brans": detay["brans"],
                "goruldu": goruldu,
            })
    else:
        rid = raw_item.get("receiver_id", "")
        detay = _lookup_kisi_detay(rid, raw_item.get("receiver_type", ""), store)
        goruldu_list = [{
            "id": rid,
            "ad": detay["ad"],
            "soyad": detay["soyad"],
            "ad_soyad": detay["ad_soyad"] or raw_item.get("receiver_name", rid),
            "brans": detay["brans"],
            "goruldu": bool(raw_item.get("okundu", False)),
        }]

    goruldu_say = sum(1 for r in goruldu_list if r["goruldu"])
    gorulmedi_say = len(goruldu_list) - goruldu_say

    # Özet sayaçlar
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.metric("👥 Toplam Alıcı", len(goruldu_list))
    with rc2:
        st.metric("✅ Gördü", goruldu_say)
    with rc3:
        st.metric("⏳ Görülmedi", gorulmedi_say)

    # Filtre: hepsini / sadece görenler / sadece görmeyenler
    rf = st.radio(
        "Göster:", ["Tümü", "✅ Gördü", "⏳ Görülmedi"],
        horizontal=True,
        key=f"rpr_f_{raw_item.get('id','')}",
    )
    if rf == "✅ Gördü":
        goruldu_list = [r for r in goruldu_list if r["goruldu"]]
    elif rf == "⏳ Görülmedi":
        goruldu_list = [r for r in goruldu_list if not r["goruldu"]]

    if not goruldu_list:
        styled_info_banner("Bu filtrede sonuç yok.", "info")
        return

    # Tablo
    rows_html = ""
    for r in goruldu_list:
        durum_badge = (
            '<span style="background:#ecfdf5;color:#10b981;padding:2px 8px;'
            'border-radius:5px;font-size:10px;font-weight:600;">✅ Gördü</span>'
            if r["goruldu"] else
            '<span style="background:#fef3c7;color:#92400e;padding:2px 8px;'
            'border-radius:5px;font-size:10px;">⏳ Görülmedi</span>'
        )
        rows_html += (
            f'<tr style="border-bottom:1px solid #1A2035;">'
            f'<td style="padding:7px 8px;font-size:11px;font-weight:600;">{r["ad"]}</td>'
            f'<td style="padding:7px 8px;font-size:11px;">{r["soyad"]}</td>'
            f'<td style="padding:7px 8px;font-size:11px;color:#475569;">{r["brans"] or "—"}</td>'
            f'<td style="padding:7px 8px;">{durum_badge}</td>'
            f'</tr>'
        )
    st.markdown(
        '<div style="overflow-x:auto;margin-top:8px">'
        '<table style="width:100%;border-collapse:collapse;">'
        '<thead><tr style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);">'
        '<th style="padding:7px 8px;text-align:left;color:#5b21b6;font-size:10px;">Ad</th>'
        '<th style="padding:7px 8px;text-align:left;color:#5b21b6;font-size:10px;">Soyad</th>'
        '<th style="padding:7px 8px;text-align:left;color:#5b21b6;font-size:10px;">Branş / Pozisyon</th>'
        '<th style="padding:7px 8px;text-align:left;color:#5b21b6;font-size:10px;">Durum</th>'
        f'</tr></thead><tbody>{rows_html}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def _render_kh_gelen(store: AkademikDataStore, user: dict, username: str):
    styled_section("Gelen Mesajlar", "#2563eb")

    gelen = store.get_panel_gelen_kutusu(username)
    okunmamis = sum(1 for m in gelen if not m.okundu)

    styled_stat_row([
        ("Toplam", str(len(gelen)), "#2563eb", "📨"),
        ("Okunmamış", str(okunmamis), "#ef4444", "🔴"),
        ("Okunmuş", str(len(gelen) - okunmamis), "#10b981", "✅"),
    ])

    if not gelen:
        styled_info_banner("Gelen kutunuz boş. Henüz mesaj almadınız.", "info")
        return

    # Filtreler
    fc1, fc2 = st.columns(2)
    with fc1:
        f_okunma = st.selectbox("Durum", ["Tümü", "Okunmamış", "Okunmuş"], key="kh_gm_f_okunma")
    with fc2:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in MESAJ_KATEGORILERI], key="kh_gm_f_kat")

    filtered = list(gelen)
    if f_okunma == "Okunmamış":
        filtered = [m for m in filtered if not m.okundu]
    elif f_okunma == "Okunmuş":
        filtered = [m for m in filtered if m.okundu]
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == f_kat), "")
        filtered = [m for m in filtered if m.kategori == kat_key]

    st.caption(f"{len(filtered)} mesaj listeleniyor")

    rows_html = ""
    for m in filtered[:100]:
        okundu_badge = _mesaj_puan_badge(m, "yeni" if not m.okundu else "okunan")
        kat_label = dict(MESAJ_KATEGORILERI).get(m.kategori, m.kategori)
        tarih = m.created_at[:16].replace("T", " ") if m.created_at else "-"
        konu = m.konu[:50] if m.konu else "-"
        font_w = "700" if not m.okundu else "400"
        bg = "#eff6ff" if not m.okundu else "#fff"
        grup_badge = ""
        if m.is_group_message:
            grup_badge = ' <span style="background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:4px;font-size:9px;">Grup</span>'
        rows_html += (
            f'<tr style="border-bottom:1px solid #1A2035;background:{bg};">'
            f'<td style="padding:8px 6px;font-size:11px;font-weight:{font_w};">{m.sender_name}{grup_badge}</td>'
            f'<td style="padding:8px 6px;font-size:11px;font-weight:{font_w};">{konu}</td>'
            f'<td style="padding:8px 6px;font-size:11px;">{kat_label}</td>'
            f'<td style="padding:8px 6px;font-size:11px;color:#64748b;">{tarih}</td>'
            f'<td style="padding:8px 6px;">{okundu_badge}</td>'
            f'</tr>'
        )

    if rows_html:
        st.markdown(
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:12px;">'
            f'<thead><tr style="background:linear-gradient(135deg,#eff6ff,#dbeafe);">'
            f'<th style="padding:8px 6px;text-align:left;color:#1e40af;font-size:10px;">Gönderen</th>'
            f'<th style="padding:8px 6px;text-align:left;color:#1e40af;font-size:10px;">Konu</th>'
            f'<th style="padding:8px 6px;text-align:left;color:#1e40af;font-size:10px;">Kategori</th>'
            f'<th style="padding:8px 6px;text-align:left;color:#1e40af;font-size:10px;">Tarih</th>'
            f'<th style="padding:8px 6px;text-align:left;color:#1e40af;font-size:10px;">Durum</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table></div>',
            unsafe_allow_html=True,
        )

    # Detay + Yanıtla
    st.divider()
    styled_section("Mesaj Detay & Yanıtla", "#0d9488")
    secenekler = {}
    for m in filtered:
        lbl = f"{'🔴 ' if not m.okundu else ''}{m.sender_name} | {m.konu[:40]} | {m.created_at[:16]}"
        secenekler[lbl] = m.id

    sec = st.selectbox("Mesaj Seçin", [""] + list(secenekler.keys()), key="kh_gm_detay_sec")
    if not (sec and sec in secenekler):
        return

    msg_id = secenekler[sec]
    msg = next((m for m in filtered if m.id == msg_id), None)
    if not msg:
        return

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Gönderen:** {msg.sender_name} ({msg.sender_type.title()})")
        st.markdown(f"**Konu:** {msg.konu}")
        st.markdown(f"**Kategori:** {dict(MESAJ_KATEGORILERI).get(msg.kategori, msg.kategori)}")
    with c2:
        st.markdown(f"**Tarih:** {msg.created_at[:16].replace('T', ' ')}")
        st.markdown(f"**Durum:** {'Okundu' if msg.okundu else 'Okunmamış'}")
        if msg.is_group_message:
            st.markdown(f"**Grup:** {msg.group_target}")

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#111827,#1A2035);border-radius:12px;'
        f'padding:16px 20px;margin:12px 0;font-size:13px;color:#94A3B8;'
        f'border-left:4px solid #2563eb;line-height:1.7;">{msg.icerik}</div>',
        unsafe_allow_html=True,
    )

    bc1, bc2 = st.columns(2)
    with bc1:
        if not msg.okundu:
            if st.button("✅ Okundu İşaretle", key="kh_gm_okundu_btn", type="primary", use_container_width=True):
                if msg.is_group_message:
                    store.mark_grup_mesaj_okundu(msg.id, username)
                else:
                    store.mark_mesaj_okundu(msg.id)
                st.success("Mesaj okundu olarak işaretlendi!")
                st.rerun()
        else:
            st.markdown('<div style="background:#ecfdf5;border-radius:8px;padding:8px 12px;'
                        'text-align:center;color:#059669;font-size:12px;font-weight:600;">✅ Okundu</div>',
                        unsafe_allow_html=True)
    with bc2:
        if st.button("↩️ Yanıtla", key="kh_gm_yanitla_btn", use_container_width=True):
            st.session_state["kh_yanitla_id"] = msg.id
            st.session_state["kh_yanitla_kisi"] = msg.sender_id
            st.session_state["kh_yanitla_ad"] = msg.sender_name
            st.session_state["kh_yanitla_tip"] = msg.sender_type
            st.session_state["kh_yanitla_konu"] = f"Re: {msg.konu}"
            st.session_state["kh_yanitla_conv"] = msg.conversation_id or msg.id
            st.rerun()

    # Yanıtla formu
    if st.session_state.get("kh_yanitla_id") == msg.id:
        st.divider()
        styled_section("Yanıt Yaz", "#6366f1")

        # Gönderen adı doğrulaması
        user_display = _get_user_display_name(user)
        if user_display:
            st.markdown(
                f'<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;'
                f'padding:8px 12px;font-size:0.88rem;color:#065f46;margin-bottom:8px">'
                f'✅ <b>Yanıtlayan:</b> {user_display} <span style="opacity:.7;font-size:.78rem">'
                f'(oturumdan otomatik alındı)</span></div>',
                unsafe_allow_html=True,
            )
            gonderen_adi_yanit = user_display
        else:
            gonderen_adi_yanit = st.text_input(
                "Adınız Soyadınız *(zorunlu)*",
                key="kh_yanit_gonderen_adi",
                placeholder="Ad ve soyadınızı giriniz",
            )
            if not gonderen_adi_yanit.strip():
                st.warning("⚠️ Yanıt göndermek için adınızı ve soyadınızı girmelisiniz.")

        yanit_icerik = st.text_area(
            "Yanıtınız *",
            key="kh_yanit_icerik",
            height=120,
            placeholder="Yanıtınızı yazın...",
        )

        if st.button("📤 Yanıtı Gönder", key="kh_yanit_gonder", type="primary", use_container_width=False):
            errors = []
            if not (gonderen_adi_yanit or user_display).strip():
                errors.append("Gönderen adı soyadı zorunludur.")
            if not yanit_icerik.strip():
                errors.append("Yanıt içeriği boş olamaz.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                yanit = VeliMesaj(
                    sender_type=user.get("role", "calisan").lower(),
                    sender_id=username,
                    sender_name=gonderen_adi_yanit.strip(),
                    receiver_type=st.session_state["kh_yanitla_tip"],
                    receiver_id=st.session_state["kh_yanitla_kisi"],
                    receiver_name=st.session_state["kh_yanitla_ad"],
                    konu=st.session_state["kh_yanitla_konu"],
                    icerik=yanit_icerik.strip(),
                    kategori=msg.kategori,
                    parent_message_id=msg.id,
                    conversation_id=st.session_state["kh_yanitla_conv"],
                )
                store.save_veli_mesaj(yanit)
                try:
                    from utils.messaging import send_panel_mesaj_bildirimi
                    send_panel_mesaj_bildirimi(
                        receiver_id=yanit.receiver_id,
                        receiver_type=yanit.receiver_type,
                        receiver_name=yanit.receiver_name,
                        sender_name=yanit.sender_name,
                        konu=yanit.konu,
                        icerik=yanit.icerik,
                    )
                except Exception:
                    pass
                for k in ["kh_yanitla_id", "kh_yanitla_kisi", "kh_yanitla_ad",
                           "kh_yanitla_tip", "kh_yanitla_konu", "kh_yanitla_conv"]:
                    st.session_state.pop(k, None)
                st.toast("✅ Yanıt gönderildi!", icon="✅")
                st.rerun()


def _render_kh_giden(store: AkademikDataStore, user: dict, username: str):
    styled_section("Giden Mesajlar", "#8b5cf6")

    # Ham JSON'dan gönderilen tüm mesajları al (okundu_by bilgisi için)
    all_data = store._load(store.veli_mesajlar_file)
    raw_giden = [item for item in all_data if item.get("sender_id") == username]
    raw_giden.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    # Model nesneleri (stat için)
    giden = [VeliMesaj.from_dict(item) for item in raw_giden]

    toplam = len(giden)
    # Grup mesajlarda "okundu" = en az 1 kişi okudu
    okunan = 0
    for item in raw_giden:
        if item.get("is_group_message"):
            if item.get("okundu_by"):
                okunan += 1
        elif item.get("okundu"):
            okunan += 1

    styled_stat_row([
        ("Toplam Giden", str(toplam), "#8b5cf6", "📤"),
        ("En Az 1 Kişi Okudu", str(okunan), "#10b981", "👁️"),
        ("Hiç Açılmadı", str(toplam - okunan), "#f59e0b", "⏳"),
    ])

    if not giden:
        styled_info_banner("Henüz mesaj göndermediniz. 'Yeni Mesaj' sekmesinden gönderin.", "info")
        return

    # Filtreler
    fc1, fc2 = st.columns(2)
    with fc1:
        f_kat = st.selectbox("Kategori", ["Tümü"] + [k[1] for k in MESAJ_KATEGORILERI],
                             key="kh_gdm_f_kat")
    with fc2:
        f_tip = st.selectbox("Mesaj Tipi", ["Tümü", "Birebir", "Grup"], key="kh_gdm_f_tip")

    filtered_raw = list(raw_giden)
    if f_kat != "Tümü":
        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == f_kat), "")
        filtered_raw = [x for x in filtered_raw if x.get("kategori") == kat_key]
    if f_tip == "Birebir":
        filtered_raw = [x for x in filtered_raw if not x.get("is_group_message")]
    elif f_tip == "Grup":
        filtered_raw = [x for x in filtered_raw if x.get("is_group_message")]

    st.caption(f"{len(filtered_raw)} mesaj listeleniyor")
    st.write("")

    kat_map = dict(MESAJ_KATEGORILERI)
    for item in filtered_raw[:100]:
        is_grup = item.get("is_group_message", False)
        konu = item.get("konu", "(Konu yok)")
        tarih = (item.get("created_at", "")[:16] or "-").replace("T", " ")
        kat_label = kat_map.get(item.get("kategori", ""), "-")

        if is_grup:
            alici_str = f"👥 Grup — {item.get('group_target', '')}"
            okundu_by = item.get("okundu_by", [])
            rcpt_count = len(item.get("group_recipients", []))
            durum_str = f"✅ {len(okundu_by)}/{rcpt_count} gördü"
        else:
            alici_str = f"👤 {item.get('receiver_name', '-')}"
            durum_str = "✅ Gördü" if item.get("okundu") else "⏳ Görülmedi"

        baslik = f"📤 {konu[:45]}  |  {alici_str}  |  {durum_str}  |  {tarih}"

        with st.expander(baslik, expanded=False):
            st.caption(f"Kategori: {kat_label}")
            st.markdown("**Görüldü Raporu**")
            _render_goruldu_raporu(item, store)


def _render_kh_yeni_mesaj(store: AkademikDataStore, user: dict, username: str):
    styled_section("Yeni Mesaj Oluştur", "#10b981")

    user_display = _get_user_display_name(user)

    # Gönderen adı bloğu
    if user_display:
        st.markdown(
            f'<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;'
            f'padding:10px 14px;margin-bottom:12px;font-size:0.9rem;color:#065f46">'
            f'✅ <b>Gönderen:</b> {user_display}'
            f'<span style="opacity:.65;font-size:.78rem;margin-left:8px">'
            f'(oturumdan otomatik alındı)</span></div>',
            unsafe_allow_html=True,
        )
        gonderen_adi = user_display
    else:
        st.markdown(
            '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;'
            'padding:10px 14px;margin-bottom:12px;font-size:0.88rem;color:#7f1d1d">'
            '⚠️ Hesabınızda ad/soyad bilgisi bulunamadı. '
            'Mesaj göndermek için adınızı ve soyadınızı girmeniz zorunludur.</div>',
            unsafe_allow_html=True,
        )
        gonderen_adi = st.text_input(
            "Adınız Soyadınız *(zorunlu)*",
            key="kh_ym_gonderen_adi",
            placeholder="Ad ve soyadınızı eksiksiz giriniz",
        )

    styled_info_banner(
        "Kurum içi kullanıcılara birebir veya grup mesaj gönderin. "
        "Mesajlar alıcının Gelen Mesaj kutusuna anında düşer.",
        "info",
    )

    mesaj_tipi = st.radio("Mesaj Tipi", ["Birebir", "Grup"], horizontal=True, key="kh_ym_tipi")

    alici_secenekleri: dict[str, str] = {}

    if mesaj_tipi == "Birebir":
        alici_turu = st.radio(
            "Alıcı Türü", ["Personel (İK)", "Öğrenci", "Veli"],
            horizontal=True, key="kh_ym_alici_turu",
        )

        if alici_turu == "Personel (İK)":
            try:
                from utils.shared_data import load_ik_active_employees
                employees = load_ik_active_employees()
                for e in sorted(employees, key=lambda x: f"{x.get('ad','')} {x.get('soyad','')}"):
                    ad = f"{e.get('ad','')} {e.get('soyad','')}".strip()
                    if not ad:
                        continue
                    pos = e.get("position_name", "")
                    brans = e.get("brans", "")
                    suffix = " | ".join(filter(None, [pos, brans]))
                    label = f"{ad} — {suffix}" if suffix else ad
                    # Auth username eşleşmesiyle doğru receiver_id bul
                    alici_secenekleri[label] = _resolve_ik_receiver_id(e)
            except Exception:
                pass

        elif alici_turu == "Öğrenci":
            try:
                from utils.shared_data import load_shared_students
                studs = load_shared_students()
                for s in sorted(studs, key=lambda x: (str(x.get("sinif","")), x.get("sube",""), x.get("soyad",""))):
                    ad = f"{s.get('ad','')} {s.get('soyad','')}".strip()
                    if not ad:
                        continue
                    label = f"{ad} — {s.get('sinif','')}/{s.get('sube','')}"
                    # Auth username ile eşleştir — öğrencinin panelde mesajı görebilmesi için
                    ogrenci_no = str(s.get("numara") or s.get("ogrenci_no") or "")
                    resolved = _resolve_ogrenci_auth_username(ad, ogrenci_no)
                    alici_secenekleri[label] = resolved if resolved else s.get("id", ad)
            except Exception:
                pass

        else:  # Veli
            try:
                from utils.shared_data import load_shared_students
                studs = load_shared_students()
                seen_veli = set()  # Aynı veliyi birden fazla kez eklememek için
                for s in sorted(studs, key=lambda x: (str(x.get("sinif","")), x.get("sube",""), x.get("soyad",""))):
                    veli_ad = s.get("veli_adi", "")
                    if not veli_ad:
                        veli_ad = f"{s.get('anne_adi','')} {s.get('anne_soyadi','')}".strip()
                    if not veli_ad:
                        veli_ad = f"{s.get('baba_adi','')} {s.get('baba_soyadi','')}".strip()
                    if not veli_ad:
                        continue
                    ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}".strip()
                    label = f"{veli_ad} (Velisi: {ogr_ad} — {s.get('sinif','')}/{s.get('sube','')})"
                    # Auth username ile eşleştir — velinin panelde mesajı görebilmesi için
                    resolved = _resolve_veli_auth_username(veli_ad)
                    receiver_val = resolved if resolved else veli_ad
                    if label not in alici_secenekleri:
                        alici_secenekleri[label] = receiver_val
            except Exception:
                pass

        alici_label = st.selectbox("Alıcı *", [""] + list(alici_secenekleri.keys()), key="kh_ym_alici")

    else:  # Grup
        # Kaydedilmiş özel gruplar
        ozel_gruplar = _load_mesaj_gruplari()
        grup_secenekleri = [
            ("tum_ogretmenler",  "Tüm Öğretmenler"),
            ("tum_veliler",      "Tüm Veliler"),
            ("tum_yoneticiler",  "Tüm Yöneticiler"),
            ("tum_ik_calisanlar","Tüm IK Çalışanları"),
            ("tum_calisanlar",   "Tüm Çalışanlar (Auth)"),
            ("tum_kullanicilar", "Tüm Kullanıcılar"),
        ]
        # Özel grupları ekle
        for g in ozel_gruplar:
            grup_secenekleri.append((f"ozel_{g['id']}", f"📋 {g['name']} ({len(g.get('members',[]))} üye)"))

        grup_label = st.selectbox("Grup *", [g[1] for g in grup_secenekleri], key="kh_ym_grup")
        grup_key = next((g[0] for g in grup_secenekleri if g[1] == grup_label), "tum_kullanicilar")

        # ── Dinamik filtreler ─────────────────────────────────────
        if grup_key == "tum_veliler":
            st.caption("🎯 Velileri daraltmak için filtre uygulayın (tümü için boş bırakın)")
            try:
                studs = store.get_students()
                siniflar = sorted({str(s.sinif) for s in studs if s.sinif})
                subeler = sorted({s.sube for s in studs if s.sube})
            except Exception:
                siniflar, subeler = [], []
            vf1, vf2, vf3 = st.columns(3)
            with vf1:
                st.selectbox(
                    "Kademe", ["Tümü", "İlkokul (1-4)", "Ortaokul (5-8)", "Lise (9-12)"],
                    key="kh_ym_veli_kademe",
                )
            with vf2:
                st.selectbox("Sınıf", ["Tümü"] + siniflar, key="kh_ym_veli_sinif")
            with vf3:
                st.selectbox("Şube", ["Tümü"] + subeler, key="kh_ym_veli_sube")

        elif grup_key == "tum_ik_calisanlar":
            st.caption("🎯 Çalışanları daraltmak için görev türü filtreleyin")
            try:
                from utils.shared_data import load_ik_active_employees
                ik_emp = load_ik_active_employees()
                role_labels = {
                    "TEACHER": "Öğretmen",
                    "MANAGEMENT": "Yönetim",
                    "ADMIN": "Yönetici",
                    "SUPPORT": "Destek Personeli",
                }
                role_scopes = sorted({(e.get("role_scope") or "Diğer") for e in ik_emp})
                role_secenek = ["Tümü"] + [
                    f"{role_labels.get(r, r)} ({r})" for r in role_scopes
                ]
            except Exception:
                role_secenek = ["Tümü"]
            st.selectbox("Görev Türü", role_secenek, key="kh_ym_ik_role")

    # Mesaj formu
    with st.form("kh_ym_form"):
        konu = st.text_input("Konu *", key="kh_ym_konu")
        kategori_label = st.selectbox("Kategori", [k[1] for k in MESAJ_KATEGORILERI], key="kh_ym_kat")
        icerik = st.text_area(
            "Mesaj İçeriği *", height=140, key="kh_ym_icerik",
            placeholder="Mesajınızı buraya yazın...",
        )
        submitted = st.form_submit_button("📤 Gönder", type="primary", use_container_width=True)

    if submitted:
        errors = []
        if not gonderen_adi.strip():
            errors.append("⚠️ Gönderen adı soyadı zorunludur — sisteme kendi adınızla giriş yapın ya da alanı doldurun.")
        if not konu.strip():
            errors.append("Konu alanı zorunludur.")
        if not icerik.strip():
            errors.append("Mesaj içeriği boş olamaz.")
        if errors:
            for e in errors:
                st.error(e)
            return

        kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == kategori_label), "genel")
        user_role = user.get("role", "calisan").lower()

        if mesaj_tipi == "Birebir":
            if not alici_label or alici_label not in alici_secenekleri:
                st.error("Alıcı seçmelisiniz.")
                return
            alici_id = alici_secenekleri[alici_label]
            alici_ad = alici_label.split(" — ")[0].split(" (")[0].strip()
            alici_turu_map = {"Personel (İK)": "personel", "Öğrenci": "ogrenci", "Veli": "veli"}
            alici_role = alici_turu_map.get(alici_turu, "personel")

            mesaj = VeliMesaj(
                sender_type=user_role,
                sender_id=username,
                sender_name=gonderen_adi.strip(),
                receiver_type=alici_role,
                receiver_id=alici_id,
                receiver_name=alici_ad,
                konu=konu.strip(),
                icerik=icerik.strip(),
                kategori=kat_key,
            )
            mesaj.conversation_id = mesaj.id
            store.save_veli_mesaj(mesaj)
            try:
                from utils.messaging import send_panel_mesaj_bildirimi
                send_panel_mesaj_bildirimi(
                    receiver_id=mesaj.receiver_id,
                    receiver_type=mesaj.receiver_type,
                    receiver_name=mesaj.receiver_name,
                    sender_name=mesaj.sender_name,
                    konu=mesaj.konu,
                    icerik=mesaj.icerik,
                )
            except Exception:
                pass
            st.toast(f"✅ Mesaj '{alici_ad}' adlı kişiye gönderildi!", icon="✅")
            st.rerun()
        else:
            try:
                recipients = []

                if grup_key == "tum_veliler":
                    # Filtreli veli alıcıları
                    kademe_f = st.session_state.get("kh_ym_veli_kademe", "Tümü")
                    sinif_f = st.session_state.get("kh_ym_veli_sinif", "Tümü")
                    sube_f = st.session_state.get("kh_ym_veli_sube", "Tümü")
                    recipients = _resolve_veli_recipients_by_filter(store, kademe_f, sinif_f, sube_f)
                    if not recipients:
                        # Fallback: auth'taki tüm veliler
                        from utils.auth import get_all_users
                        tum = get_all_users()
                        recipients = [
                            {"id": u["username"], "ad": u["name"], "tip": "veli"}
                            for u in tum
                            if u.get("role") == "Veli"
                            and u.get("username") != username
                            and u.get("active", True)
                        ]

                elif grup_key == "tum_ik_calisanlar":
                    # Filtrelenmiş IK çalışanları
                    ik_role_f = st.session_state.get("kh_ym_ik_role", "Tümü")
                    from utils.shared_data import load_ik_active_employees
                    ik_emp = load_ik_active_employees()
                    if ik_role_f != "Tümü":
                        # "Öğretmen (TEACHER)" formatından kodu çıkar
                        ik_role_kod = ik_role_f.split("(")[-1].rstrip(")").strip() if "(" in ik_role_f else ik_role_f
                        ik_emp = [e for e in ik_emp if (e.get("role_scope") or "") == ik_role_kod]
                    for e in ik_emp:
                        rid = _resolve_ik_receiver_id(e)
                        if rid == username:
                            continue
                        ad_soyad = f"{e.get('ad','')} {e.get('soyad','')}".strip()
                        recipients.append({"id": rid, "ad": ad_soyad, "tip": "personel"})

                elif grup_key.startswith("ozel_"):
                    # Özel kayıtlı grup
                    grp_id = grup_key[5:]  # "ozel_" prefix'ini çıkar
                    ozel_g = next((g for g in _load_mesaj_gruplari() if g["id"] == grp_id), None)
                    if ozel_g:
                        recipients = [
                            m for m in ozel_g.get("members", [])
                            if m.get("id") != username
                        ]

                else:
                    from utils.auth import get_all_users
                    tum = get_all_users()
                    role_map = {
                        "tum_ogretmenler": "Ogretmen",
                        "tum_yoneticiler": "Yonetici",
                        "tum_calisanlar": "Calisan",
                    }
                    hedef_role = role_map.get(grup_key)
                    if hedef_role:
                        recipients = [
                            {"id": u["username"], "ad": u["name"], "tip": u["role"]}
                            for u in tum
                            if u.get("role") == hedef_role
                            and u.get("username") != username
                            and u.get("active", True)
                        ]
                    else:
                        recipients = [
                            {"id": u["username"], "ad": u["name"], "tip": u["role"]}
                            for u in tum
                            if u.get("username") != username and u.get("active", True)
                        ]

                if not recipients:
                    st.warning("Seçilen grupta alıcı bulunamadı.")
                    return

                store.send_grup_mesaj(
                    sender_type=user_role,
                    sender_id=username,
                    sender_name=gonderen_adi.strip(),
                    group_target=grup_key,
                    recipients=recipients,
                    konu=konu.strip(),
                    icerik=icerik.strip(),
                    kategori=kat_key,
                )
                try:
                    from utils.messaging import send_grup_mesaj_bildirimleri
                    send_grup_mesaj_bildirimleri(
                        recipients=recipients,
                        sender_name=gonderen_adi.strip(),
                        konu=konu.strip(),
                        icerik=icerik.strip(),
                    )
                except Exception:
                    pass
                st.toast(f"✅ Grup mesajı {len(recipients)} kişiye gönderildi!", icon="✅")
                st.rerun()
            except Exception as ex:
                st.error(f"Grup mesajı gönderilemedi: {ex}")


# ===================== MESAJ GRUPLARI =====================

_MESAJ_GRUPLARI_DOSYA = get_data_path("akademik", "mesaj_gruplari.json")


def _load_mesaj_gruplari() -> list[dict]:
    try:
        if os.path.exists(_MESAJ_GRUPLARI_DOSYA):
            with open(_MESAJ_GRUPLARI_DOSYA, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save_mesaj_gruplari(gruplar: list[dict]) -> bool:
    try:
        os.makedirs(os.path.dirname(_MESAJ_GRUPLARI_DOSYA), exist_ok=True)
        with open(_MESAJ_GRUPLARI_DOSYA, "w", encoding="utf-8") as f:
            json.dump(gruplar, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def _resolve_veli_recipients_by_filter(
    store: AkademikDataStore,
    kademe: str,
    sinif: str,
    sube: str,
) -> list[dict]:
    """Kademe/sınıf/şube filtresine göre veli alıcı listesi çöz.

    Veli auth username'i, öğrenci kaydındaki veli_adi ile auth.name eşleşmesiyle bulunur.
    """
    try:
        students = store.get_students()

        # Kademe filtresi
        _KADEME_MAP = {
            "İlkokul (1-4)":  [1, 2, 3, 4],
            "Ortaokul (5-8)": [5, 6, 7, 8],
            "Lise (9-12)":    [9, 10, 11, 12],
        }
        if kademe != "Tümü" and kademe in _KADEME_MAP:
            sinif_aralik = _KADEME_MAP[kademe]
            students = [s for s in students if s.sinif in sinif_aralik]

        # Sınıf filtresi
        if sinif != "Tümü":
            try:
                sinif_int = int(sinif)
                students = [s for s in students if s.sinif == sinif_int]
            except ValueError:
                pass

        # Şube filtresi
        if sube != "Tümü":
            students = [s for s in students if (s.sube or "").upper() == sube.upper()]

        if not students:
            return []

        # Veli adları
        veli_adi_set: set[str] = set()
        for s in students:
            for field in ["veli_adi", "anne_adi", "baba_adi"]:
                v = (getattr(s, field, None) or "").strip()
                if v:
                    veli_adi_set.add(v.lower())

        # Auth kullanıcılarından Veli rolündekileri eşleştir
        try:
            from utils.auth import get_all_users
            auth_users = get_all_users()
        except Exception:
            auth_users = []

        recipients: list[dict] = []
        seen_ids: set[str] = set()
        for u in auth_users:
            if u.get("role") != "Veli" or not u.get("active", True):
                continue
            name = (u.get("name") or "").strip().lower()
            if name in veli_adi_set:
                uid = u["username"]
                if uid not in seen_ids:
                    seen_ids.add(uid)
                    recipients.append({"id": uid, "ad": u.get("name", ""), "tip": "veli"})

        # Eşleşmeyen ama filtreye giren öğrencilerin veli adlarını fallback olarak ekle
        if not recipients:
            for s in students:
                v_adi = (getattr(s, "veli_adi", "") or "").strip()
                if v_adi and v_adi not in seen_ids:
                    seen_ids.add(v_adi)
                    recipients.append({"id": s.id, "ad": v_adi, "tip": "veli"})

        return recipients
    except Exception:
        return []


def _render_mesaj_gruplari_kh(store: AkademikDataStore, current_username: str):
    """Mesaj Grupları — kalıcı grup oluşturma ve yönetimi."""
    styled_section("Mesaj Grupları", "#7c3aed")
    styled_info_banner(
        "Sık kullandığınız alıcı gruplarını kaydedin. Kaydedilen gruplar 'Yeni Mesaj' "
        "formunda doğrudan seçilebilir.",
        "info",
    )

    gruplar = _load_mesaj_gruplari()
    benim_gruplar = [g for g in gruplar if g.get("creator_id") == current_username]
    diger_gruplar = [g for g in gruplar if g.get("creator_id") != current_username]

    mg_t1, mg_t2 = st.tabs(["  📋 Gruplarım  ", "  ➕ Yeni Grup Oluştur  "])

    # ── Tab 1: Gruplarım ─────────────────────────────────────────
    with mg_t1:
        styled_section("Oluşturduğum Gruplar", "#7c3aed")
        if not benim_gruplar:
            styled_info_banner("Henüz grup oluşturmadınız.", "info")
        else:
            for g in benim_gruplar:
                uye_say = len(g.get("members", []))
                tarih = (g.get("created_at", "")[:10] or "-")
                with st.expander(f"👥 {g['name']}  ·  {uye_say} üye  ·  {tarih}", expanded=False
                ):
                    if g.get("description"):
                        st.caption(g["description"])
                    # Üye listesi
                    members = g.get("members", [])
                    if members:
                        rows = ""
                        for m in members:
                            tip_label = {"veli": "Veli", "personel": "Personel",
                                         "ogrenci": "Öğrenci"}.get(m.get("tip", ""), m.get("tip", ""))
                            rows += (
                                f'<tr><td style="padding:4px 8px;font-size:11px;">{m.get("ad","")}</td>'
                                f'<td style="padding:4px 8px;font-size:11px;color:#64748b;">{tip_label}</td></tr>'
                            )
                        st.markdown(
                            '<table style="width:100%;border-collapse:collapse;">'
                            '<thead><tr style="background:#f5f3ff;">'
                            '<th style="padding:4px 8px;font-size:10px;color:#5b21b6;text-align:left;">Ad Soyad</th>'
                            '<th style="padding:4px 8px;font-size:10px;color:#5b21b6;text-align:left;">Tür</th>'
                            f'</tr></thead><tbody>{rows}</tbody></table>',
                            unsafe_allow_html=True,
                        )
                    dc1, dc2 = st.columns(2)
                    with dc1:
                        if st.button("🗑️ Grubu Sil", key=f"mg_sil_{g['id']}", type="secondary"):
                            st.session_state[f"mg_sil_onay_{g['id']}"] = True
                    if st.session_state.get(f"mg_sil_onay_{g['id']}"):
                        st.warning(f"'{g['name']}' grubunu silmek istediğinize emin misiniz?")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✅ Evet, Sil", key=f"mg_sil_evet_{g['id']}", type="primary"):
                                yeni = [x for x in gruplar if x["id"] != g["id"]]
                                _save_mesaj_gruplari(yeni)
                                st.session_state.pop(f"mg_sil_onay_{g['id']}", None)
                                st.success(f"'{g['name']}' grubu silindi.")
                                st.rerun()
                        with c2:
                            if st.button("✖ İptal", key=f"mg_sil_iptal_{g['id']}"):
                                st.session_state.pop(f"mg_sil_onay_{g['id']}", None)
                                st.rerun()

        if diger_gruplar:
            st.write("")
            styled_section("Diğer Kullanıcıların Grupları", "#94a3b8")
            for g in diger_gruplar:
                uye_say = len(g.get("members", []))
                st.caption(f"👥 **{g['name']}** ({uye_say} üye) — Oluşturan: {g.get('creator_id', '-')}")

    # ── Tab 2: Yeni Grup Oluştur ─────────────────────────────────
    with mg_t2:
        styled_section("Yeni Grup Oluştur", "#10b981")

        with st.form("mg_yeni_form"):
            mg_ad = st.text_input("Grup Adı *", placeholder="Ör: 7A Velileri, Matematik Bölümü...")
            mg_desc = st.text_input("Açıklama", placeholder="İsteğe bağlı kısa açıklama")
            mg_kaynak = st.radio(
                "Üye Kaynağı", ["Veli (Sınıf/Şube)", "IK Çalışanı", "Manuel Giriş"],
                horizontal=True, key="mg_kaynak",
            )

            # Veli kaynağı filtreleri
            mg_veli_kademe = mg_veli_sinif = mg_veli_sube = ""
            mg_ik_role = ""
            mg_manuel_ids = ""

            if mg_kaynak == "Veli (Sınıf/Şube)":
                try:
                    studs = store.get_students()
                    siniflar = sorted({str(s.sinif) for s in studs if s.sinif})
                    subeler = sorted({s.sube for s in studs if s.sube})
                except Exception:
                    siniflar, subeler = [], []

                vk1, vk2, vk3 = st.columns(3)
                with vk1:
                    mg_veli_kademe = st.selectbox(
                        "Kademe", ["Tümü", "İlkokul (1-4)", "Ortaokul (5-8)", "Lise (9-12)"],
                        key="mg_veli_kademe",
                    )
                with vk2:
                    mg_veli_sinif = st.selectbox("Sınıf", ["Tümü"] + siniflar, key="mg_veli_sinif")
                with vk3:
                    mg_veli_sube = st.selectbox("Şube", ["Tümü"] + subeler, key="mg_veli_sube")

            elif mg_kaynak == "IK Çalışanı":
                try:
                    from utils.shared_data import load_ik_active_employees
                    ik_emp = load_ik_active_employees()
                    role_scopes = sorted({(e.get("role_scope") or "Diğer") for e in ik_emp})
                except Exception:
                    role_scopes = []
                mg_ik_role = st.selectbox(
                    "Görev Türü", ["Tümü"] + role_scopes, key="mg_ik_role",
                )
                st.caption("'Tümü' seçilirse tüm aktif çalışanlar gruba eklenir.")

            else:  # Manuel Giriş
                mg_manuel_ids = st.text_area(
                    "Auth Kullanıcı Adları (virgülle ayırın)",
                    placeholder="admin, ogretmen1, veli_ahmet...",
                    height=80,
                    key="mg_manuel_ids",
                )

            mg_kaydet = st.form_submit_button("💾 Grubu Oluştur", type="primary", use_container_width=True)

        if mg_kaydet:
            if not mg_ad.strip():
                st.error("Grup adı zorunludur.")
            else:
                # Üyeleri çöz
                members: list[dict] = []

                if mg_kaynak == "Veli (Sınıf/Şube)":
                    kademe_v = st.session_state.get("mg_veli_kademe", "Tümü")
                    sinif_v = st.session_state.get("mg_veli_sinif", "Tümü")
                    sube_v = st.session_state.get("mg_veli_sube", "Tümü")
                    members = _resolve_veli_recipients_by_filter(store, kademe_v, sinif_v, sube_v)

                elif mg_kaynak == "IK Çalışanı":
                    try:
                        from utils.shared_data import load_ik_active_employees
                        ik_emp = load_ik_active_employees()
                        role_f = st.session_state.get("mg_ik_role", "Tümü")
                        if role_f != "Tümü":
                            ik_emp = [e for e in ik_emp if (e.get("role_scope") or "Diğer") == role_f]
                        for e in ik_emp:
                            rid = _resolve_ik_receiver_id(e)
                            ad = f"{e.get('ad','')} {e.get('soyad','')}".strip()
                            members.append({"id": rid, "ad": ad, "tip": "personel"})
                    except Exception:
                        pass

                else:  # Manuel
                    raw_ids = st.session_state.get("mg_manuel_ids", "")
                    try:
                        from utils.auth import get_all_users
                        auth_all = {u["username"]: u for u in get_all_users()}
                    except Exception:
                        auth_all = {}
                    for uid in [x.strip() for x in raw_ids.split(",") if x.strip()]:
                        u = auth_all.get(uid)
                        ad = u.get("name", uid) if u else uid
                        members.append({"id": uid, "ad": ad, "tip": "kullanici"})

                if not members:
                    st.warning("Belirtilen kriterlere göre üye bulunamadı.")
                else:
                    yeni_grup = {
                        "id": f"grp_{uuid.uuid4().hex[:8]}",
                        "name": mg_ad.strip(),
                        "description": mg_desc.strip(),
                        "creator_id": current_username,
                        "members": members,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                    }
                    gruplar_guncel = _load_mesaj_gruplari()
                    gruplar_guncel.append(yeni_grup)
                    if _save_mesaj_gruplari(gruplar_guncel):
                        st.success(
                            f"✅ '{yeni_grup['name']}' grubu {len(members)} üyeyle oluşturuldu!"
                        )
                        st.rerun()
                    else:
                        st.error("Grup kaydedilemedi.")


def _render_bildirim_ayarlari_kh():
    """Bildirim Ayarları — E-posta ve SMS bildirim yapılandırması."""
    from utils.messaging import (
        load_bildirim_ayarlari, save_bildirim_ayarlari,
        smtp_configured, sms_configured, send_panel_mesaj_bildirimi,
    )

    ayarlar = load_bildirim_ayarlari()

    styled_section("Bildirim Altyapısı Durumu", "#0f766e")

    # Durum kartları
    smtp_ok = smtp_configured()
    sms_ok = sms_configured()
    styled_stat_row([
        ("E-posta (SMTP)", "✅ Yapılandırıldı" if smtp_ok else "❌ Ayarlanmamış",
         "#10b981" if smtp_ok else "#ef4444", "📧"),
        ("SMS Sağlayıcı", "✅ Yapılandırıldı" if sms_ok else "❌ Ayarlanmamış",
         "#10b981" if sms_ok else "#ef4444", "📱"),
    ])

    if not smtp_ok:
        styled_info_banner(
            "E-posta bildirimi için .streamlit/secrets.toml dosyasına "
            "SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM anahtarlarını ekleyin.",
            "warning",
        )
    if not sms_ok:
        styled_info_banner(
            "SMS bildirimi için secrets.toml dosyasına SMS_PROVIDER ve ilgili API "
            "anahtarlarını ekleyin (NETGSM_USERCODE/NETGSM_PASSWORD vb.).",
            "info",
        )

    st.write("")
    styled_section("Bildirim Tercihleri", "#2563eb")

    with st.form("bildirim_ayarlar_form"):
        email_aktif = st.toggle(
            "📧 E-posta Bildirimi Aktif",
            value=ayarlar.get("email_aktif", True),
            disabled=not smtp_ok,
            help="Yeni mesaj gelince alıcıya otomatik e-posta gönder",
        )
        sms_aktif = st.toggle(
            "📱 SMS Bildirimi Aktif",
            value=ayarlar.get("sms_aktif", False),
            disabled=not sms_ok,
            help="Yeni mesaj gelince alıcıya otomatik SMS gönder",
        )
        imza = st.text_input(
            "E-posta Gönderen İmzası",
            value=ayarlar.get("email_gonderen_imza", "SmartCampus AI Mesaj Sistemi"),
            help="E-posta altbilgisinde gösterilecek kurum adı / imza",
        )
        kaydet_btn = st.form_submit_button("💾 Ayarları Kaydet", type="primary")

    if kaydet_btn:
        yeni_ayarlar = {
            **ayarlar,
            "email_aktif": email_aktif,
            "sms_aktif": sms_aktif,
            "email_gonderen_imza": imza.strip(),
        }
        if save_bildirim_ayarlari(yeni_ayarlar):
            st.success("✅ Bildirim ayarları kaydedildi!")
            st.rerun()
        else:
            st.error("Ayarlar kaydedilemedi.")

    # NetGSM kontör sorgulama
    try:
        provider = st.secrets.get("SMS_PROVIDER", "").lower()
    except Exception:
        provider = ""
    if provider == "netgsm" and sms_ok:
        st.write("")
        styled_section("NetGSM Bakiye & Kontör", "#0ea5e9")
        nc1, nc2 = st.columns([3, 2])
        with nc1:
            if st.button("🔄 Bakiye Sorgula", key="netgsm_balance_btn"):
                from utils.messaging import query_netgsm_balance
                with st.spinner("NetGSM sorgulanıyor..."):
                    sonuc = query_netgsm_balance()
                if sonuc["ok"]:
                    cols_b = st.columns(3)
                    with cols_b[0]:
                        st.metric("💰 TL Kredi", sonuc["kredi"] or "—")
                    with cols_b[1]:
                        st.metric("📱 Kontör", sonuc["kontor"] or "—")
                    with cols_b[2]:
                        st.metric("📅 Geçerlilik", sonuc["gecerlilik"] or "—")
                    if sonuc.get("paket"):
                        st.caption(f"Paket: {sonuc['paket']}")
                    with st.expander("Ham API yanıtı"):
                        st.code(sonuc["raw"])
                else:
                    st.error(f"NetGSM sorgu hatası: {sonuc['hata']}")
        with nc2:
            styled_info_banner(
                "📦 <b>Kontör Yükleme</b><br>"
                "NetGSM SMS kredi/paket yüklemesi API üzerinden yapılamaz.<br>"
                "Yükleme için: <b>netgsm.com.tr → Müşteri Girişi → Kredi Yükle</b>",
                "info",
            )

    # Test gönder bölümü
    if smtp_ok or sms_ok:
        st.write("")
        styled_section("Test Bildirimi Gönder", "#7c3aed")
        with st.form("bildirim_test_form"):
            test_email = st.text_input(
                "Test E-posta Adresi",
                placeholder="ornek@okul.k12.tr",
                help="SMTP ile test mesajı göndermek için",
            )
            test_gonder = st.form_submit_button("📤 Test Gönder", type="secondary")

        if test_gonder:
            if not test_email.strip():
                st.error("Test e-posta adresi zorunludur.")
            elif smtp_ok:
                send_panel_mesaj_bildirimi(
                    receiver_id="__test__",
                    receiver_type="test",
                    receiver_name="Test Alıcısı",
                    sender_name="SmartCampus AI",
                    konu="Test Bildirimi",
                    icerik="Bu bir test mesajıdır. Bildirim sistemi çalışıyor.",
                    force_email=test_email.strip(),
                    asenkron=False,
                )
                st.success(f"✅ Test e-postası '{test_email.strip()}' adresine gönderildi!")
            else:
                st.warning("SMTP yapılandırılmamış, test gönderilemedi.")


def _render_calisanlar_listesi_kh(store: AkademikDataStore, current_username: str):
    """IK aktif çalışanlar listesi — bilgi tablosu + hızlı mesaj gönder."""
    from utils.shared_data import load_ik_active_employees
    styled_section("IK Aktif Çalışanlar", "#0369a1")

    try:
        employees = load_ik_active_employees()
    except Exception:
        employees = []

    if not employees:
        styled_info_banner("IK modülünde aktif çalışan kaydı bulunamadı.", "warning")
        return

    # Filtreler
    f1, f2, f3 = st.columns(3)
    with f1:
        role_scopes = sorted({e.get("role_scope", "—") or "—" for e in employees})
        f_role = st.selectbox("Görev Türü", ["Tümü"] + role_scopes, key="kh_emp_role")
    with f2:
        positions = sorted({e.get("position_name", "—") or "—" for e in employees})
        f_pos = st.selectbox("Pozisyon", ["Tümü"] + positions, key="kh_emp_pos")
    with f3:
        f_ara = st.text_input("Ad / Soyad Ara", key="kh_emp_ara", placeholder="Arama...")

    filtered = list(employees)
    if f_role != "Tümü":
        filtered = [e for e in filtered if (e.get("role_scope") or "—") == f_role]
    if f_pos != "Tümü":
        filtered = [e for e in filtered if (e.get("position_name") or "—") == f_pos]
    if f_ara.strip():
        ara = f_ara.strip().lower()
        filtered = [e for e in filtered
                    if ara in f"{e.get('ad','')} {e.get('soyad','')}".lower()]

    styled_stat_row([
        ("Toplam Aktif Çalışan", str(len(employees)), "#0369a1", "👥"),
        ("Filtrelenen", str(len(filtered)), "#7c3aed", "🔍"),
    ])

    st.write("")
    st.caption(f"{len(filtered)} çalışan listeleniyor")

    # Mesaj gönder session state
    if "kh_emp_mesaj_alici" not in st.session_state:
        st.session_state["kh_emp_mesaj_alici"] = None

    # Tablo başlığı
    header_cols = st.columns([2, 2, 2, 2, 1])
    headers = ["Ad", "Soyad", "Pozisyon / Branş", "E-posta", ""]
    for hc, ht in zip(header_cols, headers):
        hc.markdown(
            f'<div style="font-size:10px;font-weight:700;color:#0369a1;'
            f'padding:4px 0;border-bottom:2px solid #bae6fd;">{ht}</div>',
            unsafe_allow_html=True,
        )

    for i, e in enumerate(filtered[:150]):
        ad = e.get("ad", "")
        soyad = e.get("soyad", "")
        pos = e.get("position_name", "—") or "—"
        brans = e.get("brans", "")
        pos_brans = f"{pos} / {brans}" if brans else pos
        email = e.get("email", "—") or "—"

        row_cols = st.columns([2, 2, 2, 2, 1])
        row_cols[0].write(ad)
        row_cols[1].write(soyad)
        row_cols[2].write(pos_brans)
        row_cols[3].write(email)
        if row_cols[4].button("✉️", key=f"kh_emp_msg_{i}_{e.get('id','')}",
                               help=f"{ad} {soyad}'a mesaj gönder"):
            rid = _resolve_ik_receiver_id(e)
            st.session_state["kh_emp_mesaj_alici"] = {
                "id": rid,
                "ad_soyad": f"{ad} {soyad}".strip(),
                "pos": pos,
            }
            st.rerun()

    # Hızlı mesaj formu (alıcı seçildiyse göster)
    alici_info = st.session_state.get("kh_emp_mesaj_alici")
    if alici_info:
        st.write("")
        styled_section(f"Mesaj Gönder — {alici_info['ad_soyad']} ({alici_info['pos']})", "#10b981")
        with st.form("kh_emp_hizli_mesaj_form"):
            hizli_konu = st.text_input("Konu *", key="kh_emp_hm_konu")
            hizli_kat = st.selectbox("Kategori", [k[1] for k in MESAJ_KATEGORILERI],
                                      key="kh_emp_hm_kat")
            hizli_icerik = st.text_area("Mesaj İçeriği *", height=120, key="kh_emp_hm_icerik")
            hm_gonder = st.form_submit_button("📤 Gönder", type="primary")
            hm_iptal = st.form_submit_button("✖ İptal", type="secondary")

        if hm_iptal:
            st.session_state["kh_emp_mesaj_alici"] = None
            st.rerun()

        if hm_gonder:
            if not hizli_konu.strip() or not hizli_icerik.strip():
                st.error("Konu ve mesaj içeriği zorunludur.")
            else:
                from utils.auth import AuthManager
                cur_user = AuthManager.get_current_user()
                gonderen_adi = _get_user_display_name(cur_user) or cur_user.get("username", "")
                kat_key = next((k[0] for k in MESAJ_KATEGORILERI if k[1] == hizli_kat), "genel")
                mesaj = VeliMesaj(
                    sender_type=cur_user.get("role", "calisan").lower(),
                    sender_id=current_username,
                    sender_name=gonderen_adi,
                    receiver_type="personel",
                    receiver_id=alici_info["id"],
                    receiver_name=alici_info["ad_soyad"],
                    konu=hizli_konu.strip(),
                    icerik=hizli_icerik.strip(),
                    kategori=kat_key,
                )
                mesaj.conversation_id = mesaj.id
                store.save_veli_mesaj(mesaj)
                try:
                    from utils.messaging import send_panel_mesaj_bildirimi
                    send_panel_mesaj_bildirimi(
                        receiver_id=mesaj.receiver_id,
                        receiver_type=mesaj.receiver_type,
                        receiver_name=mesaj.receiver_name,
                        sender_name=mesaj.sender_name,
                        konu=mesaj.konu,
                        icerik=mesaj.icerik,
                    )
                except Exception:
                    pass
                st.session_state["kh_emp_mesaj_alici"] = None
                st.toast(f"✅ Mesaj '{alici_info['ad_soyad']}' adlı kişiye gönderildi!", icon="✅")
                st.rerun()


def _render_mesaj_sistemi_kh(store: AkademikDataStore):
    """Kurum Hizmetleri — Mesaj Sistemi ana fonksiyonu."""
    from utils.auth import AuthManager

    user = AuthManager.get_current_user()
    username = user.get("username", "")

    styled_section("Kurum İçi Mesaj Sistemi", "#2563eb")
    styled_info_banner(
        "Tüm kurum içi mesajlaşma burada yönetilir. Gelen/giden mesajlarınızı görüntüleyin, "
        "yanıtlayın veya yeni mesaj oluşturun. Mesaj gönderirken adınız ve soyadınız zorunludur.",
        "info",
    )

    # Özet stat
    gelen = store.get_panel_gelen_kutusu(username)
    giden = store.get_veli_giden_kutusu(username)
    okunmamis = sum(1 for m in gelen if not m.okundu)

    styled_stat_row([
        ("Gelen", str(len(gelen)), "#2563eb", "📨"),
        ("Okunmamış", str(okunmamis), "#ef4444", "🔴"),
        ("Giden", str(len(giden)), "#8b5cf6", "📤"),
    ])
    st.write("")

    t_gelen, t_giden, t_yeni, t_calisanlar, t_gruplar, t_bildirim = st.tabs([
        "  📥 Gelen Mesajlar  ",
        "  📤 Giden Mesajlar  ",
        "  ✉️ Yeni Mesaj  ",
        "  👥 Çalışan Listesi  ",
        "  📋 Mesaj Grupları  ",
        "  ⚙️ Bildirim Ayarları  ",
    ])

    with t_gelen:
        _render_kh_gelen(store, user, username)
    with t_giden:
        _render_kh_giden(store, user, username)
    with t_yeni:
        _render_kh_yeni_mesaj(store, user, username)
    with t_calisanlar:
        _render_calisanlar_listesi_kh(store, username)
    with t_gruplar:
        _render_mesaj_gruplari_kh(store, username)
    with t_bildirim:
        _render_bildirim_ayarlari_kh()


# ==================== ANA RENDER ====================

def render_kurum_hizmetleri():
    """Kurum Hizmetleri - tek ekran modülü ana fonksiyonu."""
    _inject_css()
    styled_header(
        "Kurum Hizmetleri",
        "Nöbet | Zaman Çizelgesi | Ders Programı | Etkinlik | Yemek | Servis | Veli Talepleri | Mesaj | Kullanıcı Yönetimi",
        icon="🏛️"
    )

    store = get_akademik_store()

    # -- Tab Gruplama (19 tab -> 3 grup) --
    _GRP_TABS = {
        "📋 Grup A": [("  🛡️ Nöbet Yönetimi  ", 0), ("  ⏰ Zaman Çizelgesi  ", 1), ("  📚 Ders & Program  ", 2), ("  📢 Etkinlik & Duyurular  ", 3), ("  🍽️ Yemek Menüsü  ", 4), ("  🚌 Servis Yönetimi  ", 5), ("  📋 Veli Talepleri  ", 6)],
        "📊 Grup B": [("  💬 Mesaj Sistemi  ", 7), ("  ⚙️ Kullanıcı Yönetimi  ", 8), ("  🤖 AI Menü  ", 9), ("  🎛️ Komuta Merkezi  ", 10), ("  🛡️ Servis Güvenlik  ", 11), ("  🏗️ Tesis Yönetim  ", 12), ("  👪 Veli Portal  ", 13)],
        "🔧 Grup C": [("  🚨 Acil Durum  ", 14), ("  🧠 Operasyon AI  ", 15), ("  🪪 Dijital Pasaport  ", 16), ("  💎 Maliyet Optim  ", 17), ("  🤖 Smarti  ", 18)],
    }
    _sg_grp_64203 = st.radio("", list(_GRP_TABS.keys()), horizontal=True, label_visibility="collapsed", key="rg_grp_64203")
    _gt_grp_64203 = _GRP_TABS[_sg_grp_64203]
    _tn_grp_64203 = [t[0] for t in _gt_grp_64203]
    _ti_grp_64203 = [t[1] for t in _gt_grp_64203]
    _tabs_grp_64203 = st.tabs(_tn_grp_64203)
    _tmap_grp_64203 = {i: t for i, t in zip(_ti_grp_64203, _tabs_grp_64203)}
    kh_nobet = _tmap_grp_64203.get(0)
    kh_zaman = _tmap_grp_64203.get(1)
    kh_ders = _tmap_grp_64203.get(2)
    kh_t1 = _tmap_grp_64203.get(3)
    kh_t2 = _tmap_grp_64203.get(4)
    kh_t3 = _tmap_grp_64203.get(5)
    kh_t4 = _tmap_grp_64203.get(6)
    kh_t5 = _tmap_grp_64203.get(7)
    kh_kullanici = _tmap_grp_64203.get(8)
    kh_ai_menu = _tmap_grp_64203.get(9)
    kh_komuta = _tmap_grp_64203.get(10)
    kh_servis_g = _tmap_grp_64203.get(11)
    kh_tesis = _tmap_grp_64203.get(12)
    kh_veli_p = _tmap_grp_64203.get(13)
    kh_acil = _tmap_grp_64203.get(14)
    kh_ops_ai = _tmap_grp_64203.get(15)
    kh_pasaport = _tmap_grp_64203.get(16)
    kh_maliyet = _tmap_grp_64203.get(17)
    kh_smarti = _tmap_grp_64203.get(18)

    if kh_nobet is not None:
      with kh_nobet:
        try:
            _styled_group_header(
                "Nöbet Yönetimi",
                "Öğretmen nöbet planlama, takip ve raporlama",
                color="#b45309"
            )
            _render_nobet(store)
        except Exception as _e:
            import traceback; st.error(f"Nöbet hatası: {_e}"); st.code(traceback.format_exc())

    if kh_zaman is not None:
      with kh_zaman:
        try:
            _styled_group_header(
                "Zaman Çizelgesi",
                "Günlük ders, teneffüs ve etüt zaman dilimleri",
                color="#0891b2"
            )
            _render_zaman_cizelgesi(store)
        except Exception as _e:
            import traceback; st.error(f"Zaman Çizelgesi hatası: {_e}"); st.code(traceback.format_exc())

    if kh_ders is not None:
      with kh_ders:
        try:
            _styled_group_header(
                "Ders Programı",
                "Otomatik ders dağıtımı, öğretmen görevlendirme ve program raporları",
                color="#0d9488"
            )
            _render_ders_programi(store)
        except Exception as _e:
            import traceback; st.error(f"Ders Programı hatası: {_e}"); st.code(traceback.format_exc())

    if kh_t1 is not None:
      with kh_t1:
        _render_admin_etkinlik_duyuru(store)
    if kh_t2 is not None:
      with kh_t2:
        _render_admin_yemek_menusu()
    if kh_t3 is not None:
      with kh_t3:
        _render_admin_servis(store)
    if kh_t4 is not None:
      with kh_t4:
        _render_admin_veli_talepler(store)
    if kh_t5 is not None:
      with kh_t5:
        _render_mesaj_sistemi_kh(store)

    if kh_kullanici is not None:
      with kh_kullanici:
        try:
            from views.kullanici_yonetimi import render_kullanici_yonetimi
            render_kullanici_yonetimi()
        except Exception as _eku:
            import traceback; st.error(f"Kullanıcı Yönetimi hatası: {_eku}"); st.code(traceback.format_exc())

    # ZIRVE: AI Menu Planlama
    if kh_ai_menu is not None:
      with kh_ai_menu:
        try:
            from views._kh_zirve import render_ai_menu_planlama
            render_ai_menu_planlama()
        except Exception as _e:
            st.error(f"AI Menu Planlama yuklenemedi: {_e}")

    # ZIRVE: Komuta Merkezi
    if kh_komuta is not None:
      with kh_komuta:
        try:
            from views._kh_zirve import render_hizmet_komuta
            render_hizmet_komuta()
        except Exception as _e:
            st.error(f"Komuta Merkezi yuklenemedi: {_e}")

    # ZIRVE: Servis Guvenlik
    if kh_servis_g is not None:
      with kh_servis_g:
        try:
            from views._kh_zirve import render_servis_guvenlik
            render_servis_guvenlik()
        except Exception as _e:
            st.error(f"Servis Guvenlik yuklenemedi: {_e}")

    # MEGA: Tesis Yonetim
    if kh_tesis is not None:
      with kh_tesis:
        try:
            from views._kh_mega import render_tesis_yonetim
            render_tesis_yonetim()
        except Exception as _e:
            st.error(f"Tesis Yonetim yuklenemedi: {_e}")

    # MEGA: Veli Deneyim Platformu
    if kh_veli_p is not None:
      with kh_veli_p:
        try:
            from views._kh_mega import render_veli_portal
            render_veli_portal()
        except Exception as _e:
            st.error(f"Veli Portal yuklenemedi: {_e}")

    # MEGA: Acil Durum Merkezi
    if kh_acil is not None:
      with kh_acil:
        try:
            from views._kh_mega import render_acil_durum
            render_acil_durum()
        except Exception as _e:
            st.error(f"Acil Durum yuklenemedi: {_e}")

    # ULTRA MEGA: Operasyon AI
    if kh_ops_ai is not None:
      with kh_ops_ai:
        try:
            from views._kh_ultra import render_operasyon_ai
            render_operasyon_ai()
        except Exception as _e:
            st.error(f"Operasyon AI yuklenemedi: {_e}")

    # ULTRA MEGA: Dijital Pasaport
    if kh_pasaport is not None:
      with kh_pasaport:
        try:
            from views._kh_ultra import render_dijital_pasaport
            render_dijital_pasaport()
        except Exception as _e:
            st.error(f"Dijital Pasaport yuklenemedi: {_e}")

    # ULTRA MEGA: Maliyet Optimizasyon
    if kh_maliyet is not None:
      with kh_maliyet:
        try:
            from views._kh_ultra import render_maliyet_optimizasyon
            render_maliyet_optimizasyon()
        except Exception as _e:
            st.error(f"Maliyet Optimizasyon yuklenemedi: {_e}")

    if kh_smarti is not None:
      with kh_smarti:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="kurum_hizmetleri")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_kurum_hizmetleri")
            if st.button("Gönder", key="smarti_send_kurum_hizmetleri"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. kurum_hizmetleri modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")
