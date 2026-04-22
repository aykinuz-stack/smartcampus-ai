"""
Akademik Takvim Modülü
======================
Eğitim yılı takvimi: sınavlar, tatiller, bayramlar, etkinlikler, geziler vb.
Aylık görünüm, 1 Eylül – 31 Ağustos akademik yıl döngüsü.
Güncel tarih ve yıldan otomatik hesaplama.
"""

from __future__ import annotations

import calendar
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("akademik_takip")
except Exception:
    pass
from utils.tenant import get_data_path

# ── VERİ YOLU ────────────────────────────────────────────────────────────────
_DATA_DIR = get_data_path("akademik")
_TAKVIM_DOSYA = os.path.join(_DATA_DIR, "akademik_takvim.json")

# ── SABİTLER ─────────────────────────────────────────────────────────────────
AYLAR_TR = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
]
GUNLER_TR_KISA = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

# Akademik yıl ay sırası: Eylül(9) → Ağustos(8) = index 0 → 11
AY_SIRASI = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
AY_SIRASI_ETIKET = [
    "Eylül", "Ekim", "Kasım", "Aralık",
    "Ocak", "Şubat", "Mart", "Nisan",
    "Mayıs", "Haziran", "Temmuz", "Ağustos",
]

ETKINLIK_TURLERI = [
    ("sinav",        "📝 Sınav",               "#ef4444"),
    ("someter",      "🏫 Sömestr / Yarıyıl",   "#3b82f6"),
    ("ara_tatil",    "🌴 Ara Tatil",            "#10b981"),
    ("bayram_milli", "🇹🇷 Milli Bayram",         "#dc2626"),
    ("bayram_dini",  "🕌 Dini Bayram",           "#059669"),
    ("etkinlik",     "🎉 Etkinlik / Kermes",    "#8b5cf6"),
    ("toplanti",     "📋 Toplantı",             "#f59e0b"),
    ("gezi",         "🚌 Gezi / Kültür Gezisi", "#3b82f6"),
    ("odev",         "📚 Ödev / Proje",         "#f97316"),
    ("diger",        "📌 Diğer",               "#6b7280"),
]
TUR_MAP = {k: (label, renk) for k, label, renk in ETKINLIK_TURLERI}


# ── VERİ MODELİ ──────────────────────────────────────────────────────────────
@dataclass
class TakvimEtkinlik:
    id: str = field(default_factory=lambda: f"te_{uuid.uuid4().hex[:8]}")
    baslik: str = ""
    tur: str = "etkinlik"
    tarih_baslangic: str = field(default_factory=lambda: date.today().isoformat())
    tarih_bitis: str = ""      # boşsa → tek gün (== tarih_baslangic)
    saat: str = ""
    aciklama: str = ""
    renk: str = "#8b5cf6"
    hedef: str = "tumu"        # "tumu" | "5/A" | "7/B" vb.
    akademik_yil: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TakvimEtkinlik":
        valid = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**valid)


# ── VERİ YÖNETİMİ ────────────────────────────────────────────────────────────
def _load_etkinlikler() -> list:
    os.makedirs(_DATA_DIR, exist_ok=True)
    if not os.path.exists(_TAKVIM_DOSYA):
        return []
    try:
        with open(_TAKVIM_DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_all(data: list):
    os.makedirs(_DATA_DIR, exist_ok=True)
    with open(_TAKVIM_DOSYA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _upsert_etkinlik(etkinlik: TakvimEtkinlik):
    data = _load_etkinlikler()
    for i, item in enumerate(data):
        if item.get("id") == etkinlik.id:
            data[i] = etkinlik.to_dict()
            _save_all(data)
            return
    data.append(etkinlik.to_dict())
    _save_all(data)


def _delete_etkinlik(etkinlik_id: str):
    data = _load_etkinlikler()
    data = [d for d in data if d.get("id") != etkinlik_id]
    _save_all(data)


# ── AKADEMİK YIL YARDIMCILARI ────────────────────────────────────────────────
def _aktif_akademik_yil(bugun: date | None = None) -> str:
    """Bugünün tarihine göre akademik yılı hesapla (1 Eyl → 31 Ağu)."""
    if bugun is None:
        bugun = date.today()
    if bugun.month >= 9:
        return f"{bugun.year}-{bugun.year + 1}"
    return f"{bugun.year - 1}-{bugun.year}"


def _akademik_yil_listesi(n_onceki: int = 2, n_sonraki: int = 2) -> list:
    aktif = _aktif_akademik_yil()
    y1 = int(aktif.split("-")[0])
    return [f"{y1 + d}-{y1 + d + 1}" for d in range(-n_onceki, n_sonraki + 1)]


def _ay_yil_for(akademik_yil: str, ay_no: int) -> tuple:
    """Verilen akademik yıl + ay numarası → (takvim_yıl, ay_no)."""
    y1, y2 = akademik_yil.split("-")
    yil = int(y1) if ay_no >= 9 else int(y2)
    return yil, ay_no


# ── ETKİNLİK FİLTRELEME ──────────────────────────────────────────────────────
def _etkinlik_gunler(e: dict) -> set:
    """Etkinliğin kapsadığı tüm günleri {date} seti olarak döndür."""
    gunler = set()
    try:
        bas = date.fromisoformat(e["tarih_baslangic"])
        bit_str = e.get("tarih_bitis", "")
        bit = date.fromisoformat(bit_str) if bit_str else bas
        cur = bas
        while cur <= bit:
            gunler.add(cur)
            cur += timedelta(days=1)
    except Exception:
        pass
    return gunler


def _etkinlikler_bu_ay(etkinlikler: list, yil: int, ay: int) -> list:
    """Bu ayda başlayan, biten veya yayılan etkinlikleri döndür."""
    ay_bas = date(yil, ay, 1)
    last_day = calendar.monthrange(yil, ay)[1]
    ay_bit = date(yil, ay, last_day)
    result = []
    for e in etkinlikler:
        try:
            e_bas = date.fromisoformat(e["tarih_baslangic"])
            bit_str = e.get("tarih_bitis", "")
            e_bit = date.fromisoformat(bit_str) if bit_str else e_bas
            if e_bas <= ay_bit and e_bit >= ay_bas:
                result.append(e)
        except Exception:
            pass
    return sorted(result, key=lambda x: x.get("tarih_baslangic", ""))


# ── MİLLİ TATİLLER OTO YÜKLE ─────────────────────────────────────────────────
def _milli_tatilleri_olustur(akademik_yil: str) -> list:
    """Türkiye sabit milli tatillerini döndür (dini bayramlar manuel girilmeli)."""
    y1 = int(akademik_yil.split("-")[0])
    y2 = int(akademik_yil.split("-")[1])
    now_str = datetime.now().isoformat()

    def _t(baslik, ay, gun, tur="bayram_milli", bit_ay=None, bit_gun=None):
        yil_ = y1 if ay >= 9 else y2
        bas = f"{yil_:04d}-{ay:02d}-{gun:02d}"
        bit = f"{yil_:04d}-{bit_ay:02d}-{bit_gun:02d}" if bit_ay else ""
        renk = TUR_MAP[tur][1]
        return {
            "id": f"te_milli_{yil_}{ay:02d}{gun:02d}_{uuid.uuid4().hex[:4]}",
            "baslik": baslik, "tur": tur,
            "tarih_baslangic": bas, "tarih_bitis": bit,
            "saat": "", "aciklama": "Otomatik yüklendi",
            "renk": renk, "hedef": "tumu",
            "akademik_yil": akademik_yil,
            "created_at": now_str, "updated_at": now_str,
        }

    return [
        _t("Cumhuriyet Bayramı", 10, 29, y1 if False else "bayram_milli"),
        _t("Yılbaşı", 1, 1, "diger"),
        _t("Ulusal Egemenlik ve Çocuk Bayramı", 4, 23, "bayram_milli"),
        _t("İşçi ve Dayanışma Bayramı", 5, 1, "diger"),
        _t("Atatürk'ü Anma, Gençlik ve Spor Bayramı", 5, 19, "bayram_milli"),
        _t("15 Temmuz Demokrasi ve Millî Birlik Günü", 7, 15, "bayram_milli"),
        _t("Zafer Bayramı", 8, 30, "bayram_milli"),
    ]


# ── CSS ───────────────────────────────────────────────────────────────────────
def _inject_css():
    if st.session_state.get("_atk_css_done"):
        return
    st.session_state["_atk_css_done"] = True
    inject_common_css("atk")
    st.markdown("""<style>
/* ══ Akademik Takvim ══════════════════════════════════════ */
.atk-wrap {
    overflow-x: auto;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    background: white;
}
.atk-table {
    width: 100%;
    border-collapse: collapse;
    min-width: 560px;
}
.atk-table thead tr th {
    background: linear-gradient(135deg, #111827 0%, #1A2035 50%, #e2e8f0 100%);
    color: #94A3B8;
    text-align: center;
    padding: 11px 4px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #6366f1;
}
.atk-table thead tr th.pazar-th {
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
    color: #4338ca;
}
.atk-table td {
    vertical-align: top;
    border: 1px solid #e8edf3;
    padding: 6px 5px 4px 5px;
    height: 92px;
    min-width: 14.28%;
    background: #fff;
}
.atk-table td.bos-gun { background: #111827; }
.atk-table td.bugun-gun {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 2px solid #3b82f6 !important;
}
.atk-table td.pazar-gun { background: #fafafa; }
.atk-gun-no {
    font-size: 0.8rem;
    font-weight: 700;
    color: #475569;
    display: block;
    margin-bottom: 3px;
    line-height: 1;
}
.atk-gun-no.bugun-circle {
    background: #2563eb;
    color: white;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
}
.atk-chip {
    display: block;
    font-size: 0.62rem;
    font-weight: 600;
    padding: 2px 4px;
    border-radius: 4px;
    margin: 1px 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
    color: white;
    line-height: 1.35;
}
.atk-more {
    font-size: 0.58rem;
    color: #94a3b8;
    font-style: italic;
    margin-top: 1px;
}
.atk-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 10px;
    padding: 10px 0 4px 0;
}
.atk-legend-item {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    color: white;
}
.atk-ay-nav {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
    margin: 6px 0 10px 0;
}
.atk-ay-chip {
    padding: 5px 11px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 600;
    cursor: default;
}
.atk-event-card {
    border-radius: 0 8px 8px 0;
    padding: 8px 10px;
    margin: 5px 0;
}
</style>""", unsafe_allow_html=True)


# ── STİL YARDIMCILARI ────────────────────────────────────────────────────────


# ── TAKVIM HTML ───────────────────────────────────────────────────────────────
def _render_ay_takvimi(yil: int, ay: int, etkinlikler: list, bugun: date):
    """Verilen ay için HTML takvim tablosu oluştur ve göster."""
    # Gün → etkinlik listesi haritası
    gun_map: dict[date, list] = {}
    for e in etkinlikler:
        for g in _etkinlik_gunler(e):
            if g.year == yil and g.month == ay:
                gun_map.setdefault(g, []).append(e)

    # Takvim matrisi (Pazartesi başlangıç)
    calendar.setfirstweekday(calendar.MONDAY)
    cal = calendar.monthcalendar(yil, ay)

    # Başlık satırı
    th_cells = ""
    for i, g in enumerate(GUNLER_TR_KISA):
        cls = ' class="pazar-th"' if i == 6 else ""
        th_cells += f"<th{cls}>{g}</th>"

    # Hücre satırları
    rows = ""
    for hafta in cal:
        td_cells = ""
        for col_i, gun_no in enumerate(hafta):
            if gun_no == 0:
                td_cells += '<td class="bos-gun"></td>'
                continue

            gun = date(yil, ay, gun_no)
            is_bugun = gun == bugun
            is_pazar = col_i == 6
            td_cls = "bugun-gun" if is_bugun else ("pazar-gun" if is_pazar else "")
            no_cls = "bugun-circle" if is_bugun else ""

            chips = ""
            gune_ait = gun_map.get(gun, [])
            MAX_CHIP = 2
            for e in gune_ait[:MAX_CHIP]:
                renk = e.get("renk", "#6b7280")
                baslik = e.get("baslik", "")[:16]
                title = e.get("baslik", "").replace('"', "&quot;")
                chips += f'<span class="atk-chip" style="background:{renk}" title="{title}">{baslik}</span>'
            if len(gune_ait) > MAX_CHIP:
                chips += f'<span class="atk-more">+{len(gune_ait) - MAX_CHIP} daha</span>'

            td_cells += (
                f'<td class="{td_cls}">'
                f'<span class="atk-gun-no {no_cls}">{gun_no}</span>'
                f"{chips}</td>"
            )
        rows += f"<tr>{td_cells}</tr>"

    html = (
        '<div class="atk-wrap">'
        '<table class="atk-table">'
        f"<thead><tr>{th_cells}</tr></thead>"
        f"<tbody>{rows}</tbody>"
        "</table></div>"
    )
    st.markdown(html, unsafe_allow_html=True)

    # Legend
    legend = '<div class="atk-legend">'
    for k, label, renk in ETKINLIK_TURLERI:
        legend += f'<span class="atk-legend-item" style="background:{renk}">{label}</span>'
    legend += "</div>"
    st.markdown(legend, unsafe_allow_html=True)


# ── ETKİNLİK FORMU ───────────────────────────────────────────────────────────
def _render_etkinlik_formu(
    akademik_yil: str,
    etkinlik: dict | None = None,
    form_key: str = "ekle",
):
    """Etkinlik ekle (etkinlik=None) veya güncelle (etkinlik=dict)."""
    is_edit = etkinlik is not None
    p = f"atk_f_{form_key}"
    bugun = date.today()

    with st.form(f"{p}_form", clear_on_submit=not is_edit):
        c1, c2 = st.columns(2)
        with c1:
            baslik = st.text_input(
                "Başlık *",
                value=etkinlik.get("baslik", "") if is_edit else "",
                key=f"{p}_baslik",
            )
            tur_keys = [k for k, _, _ in ETKINLIK_TURLERI]
            default_tur = etkinlik.get("tur", "etkinlik") if is_edit else "etkinlik"
            tur_idx = tur_keys.index(default_tur) if default_tur in tur_keys else 6
            tur = st.selectbox(
                "Tür",
                tur_keys,
                index=tur_idx,
                format_func=lambda x: TUR_MAP[x][0],
                key=f"{p}_tur",
            )
        with c2:
            try:
                bas_def = (
                    date.fromisoformat(etkinlik["tarih_baslangic"]) if is_edit else bugun
                )
            except Exception:
                bas_def = bugun
            tarih_bas = st.date_input(
                "Başlangıç Tarihi *", value=bas_def, key=f"{p}_bas"
            )
            try:
                bit_str = etkinlik.get("tarih_bitis", "") if is_edit else ""
                bit_def = date.fromisoformat(bit_str) if bit_str else bas_def
            except Exception:
                bit_def = bas_def
            tarih_bit = st.date_input(
                "Bitiş Tarihi (tek gün = başlangıçla aynı)",
                value=bit_def,
                key=f"{p}_bit",
            )

        c3, c4 = st.columns(2)
        with c3:
            saat = st.text_input(
                "Saat (ör: 09:00)",
                value=etkinlik.get("saat", "") if is_edit else "",
                key=f"{p}_saat",
            )
        with c4:
            hedef = st.text_input(
                "Hedef (tumu / 5/A)",
                value=etkinlik.get("hedef", "tumu") if is_edit else "tumu",
                key=f"{p}_hedef",
                help="Tüm okul için 'tumu', belirli sınıf için '5/A' yazın.",
            )

        aciklama = st.text_area(
            "Açıklama (opsiyonel)",
            value=etkinlik.get("aciklama", "") if is_edit else "",
            key=f"{p}_aciklama",
        )

        submitted = st.form_submit_button(
            "Güncelle" if is_edit else "Kaydet",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not baslik.strip():
                st.error("Başlık zorunludur.")
                return False
            if tarih_bit < tarih_bas:
                st.error("Bitiş tarihi başlangıçtan önce olamaz.")
                return False

            renk = TUR_MAP.get(tur, ("", "#6b7280"))[1]
            bit_iso = (
                "" if tarih_bit == tarih_bas else tarih_bit.isoformat()
            )
            now_str = datetime.now().isoformat()

            if is_edit:
                e = TakvimEtkinlik.from_dict(etkinlik)
                e.baslik = baslik.strip()
                e.tur = tur
                e.tarih_baslangic = tarih_bas.isoformat()
                e.tarih_bitis = bit_iso
                e.saat = saat.strip()
                e.aciklama = aciklama.strip()
                e.renk = renk
                e.hedef = hedef.strip() or "tumu"
                e.updated_at = now_str
            else:
                e = TakvimEtkinlik(
                    baslik=baslik.strip(),
                    tur=tur,
                    tarih_baslangic=tarih_bas.isoformat(),
                    tarih_bitis=bit_iso,
                    saat=saat.strip(),
                    aciklama=aciklama.strip(),
                    renk=renk,
                    hedef=hedef.strip() or "tumu",
                    akademik_yil=akademik_yil,
                    created_at=now_str,
                    updated_at=now_str,
                )

            _upsert_etkinlik(e)
            islem = "güncellendi" if is_edit else "kaydedildi"
            st.success(f"✅ '{e.baslik}' {islem}.")
            st.rerun()

    return False


# ── ANA RENDER ────────────────────────────────────────────────────────────────
def render_akademik_takvim():
    # DEPRECATED: This is the legacy entry point. The new version is academic_calendar.py.
    # Kept for backward compatibility.
    _inject_css()

    bugun = date.today()
    aktif_yil = _aktif_akademik_yil(bugun)

    # ── Başlık ────────────────────────────────────────────────────────────────
    styled_header(
        "Akademik Takvim",
        subtitle=f"Eğitim Yılı Takvimi — Bugün: {bugun.strftime('%d %B %Y')}",
        icon="📅",
    )

    # ── Kontrol satırı: Yıl | Ay gezinme | Butonlar ──────────────────────────
    col_yil, col_prev, col_ay_lbl, col_next, col_ekle = st.columns([3, 1, 4, 1, 3])

    with col_yil:
        yil_listesi = _akademik_yil_listesi()
        aktif_idx = yil_listesi.index(aktif_yil) if aktif_yil in yil_listesi else 2
        secilen_yil = st.selectbox(
            "Akademik Yıl",
            yil_listesi,
            index=aktif_idx,
            key="atk_akademik_yil",
            label_visibility="visible",
        )

    # Aktif ay index'ini session_state'te tut
    if "atk_ay_idx" not in st.session_state:
        # Bugünün ayına karşılık gelen AY_SIRASI index'ini bul
        try:
            st.session_state["atk_ay_idx"] = AY_SIRASI.index(bugun.month)
        except ValueError:
            st.session_state["atk_ay_idx"] = 0

    with col_prev:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("◀", key="atk_prev", use_container_width=True):
            st.session_state["atk_ay_idx"] = (st.session_state["atk_ay_idx"] - 1) % 12
            st.rerun()

    with col_ay_lbl:
        ay_idx = st.session_state["atk_ay_idx"]
        yil_no, ay_no = _ay_yil_for(secilen_yil, AY_SIRASI[ay_idx])
        st.markdown(
            f"<div style='text-align:center;font-size:1.2rem;font-weight:800;"
            f"color:#94A3B8;padding-top:28px'>"
            f"{AYLAR_TR[ay_no]} {yil_no}</div>",
            unsafe_allow_html=True,
        )

    with col_next:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("▶", key="atk_next", use_container_width=True):
            st.session_state["atk_ay_idx"] = (st.session_state["atk_ay_idx"] + 1) % 12
            st.rerun()

    with col_ekle:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("➕ Ekle", key="atk_ekle_btn", use_container_width=True, type="primary"):
                st.session_state["atk_form_ac"] = not st.session_state.get("atk_form_ac", False)
        with bc2:
            if st.button("🇹🇷 Tatil Yükle", key="atk_milli_btn", use_container_width=True):
                st.session_state["atk_milli_confirm"] = True

    # ── Milli Tatil Yükleme Onayı ─────────────────────────────────────────────
    if st.session_state.get("atk_milli_confirm"):
        st.warning(
            f"⚠️ {secilen_yil} yılı için Türkiye sabit milli tatilleri eklenecek. "
            "Dini bayramlar tarihleri değiştiğinden manuel girilmelidir."
        )
        oc1, oc2 = st.columns(2)
        with oc1:
            if st.button("✅ Evet, Yükle", key="atk_milli_evet", type="primary"):
                tatiller = _milli_tatilleri_olustur(secilen_yil)
                for t in tatiller:
                    _upsert_etkinlik(TakvimEtkinlik.from_dict(t))
                st.session_state["atk_milli_confirm"] = False
                st.success(f"{len(tatiller)} milli tatil yüklendi.")
                st.rerun()
        with oc2:
            if st.button("İptal", key="atk_milli_iptal"):
                st.session_state["atk_milli_confirm"] = False
                st.rerun()

    # ── Veri ──────────────────────────────────────────────────────────────────
    tum_data = _load_etkinlikler()
    yil_data = [d for d in tum_data if d.get("akademik_yil") == secilen_yil]

    # ── İstatistikler ─────────────────────────────────────────────────────────
    bugun_str = bugun.isoformat()
    bugun_etk = [
        d for d in yil_data
        if d.get("tarih_baslangic", "") <= bugun_str <= (d.get("tarih_bitis") or d.get("tarih_baslangic", ""))
    ]
    yaklasan = [d for d in yil_data if d.get("tarih_baslangic", "") > bugun_str]
    ay_etk = _etkinlikler_bu_ay(yil_data, yil_no, ay_no)

    styled_stat_row([
        ("Toplam Etkinlik", str(len(yil_data)), "#3b82f6", "📅"),
        ("Bu Ay", str(len(ay_etk)), "#8b5cf6", "📆"),
        ("Bugün", str(len(bugun_etk)), "#ef4444", "🔴"),
        ("Yaklaşan", str(len(yaklasan)), "#10b981", "⏰"),
    ])
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Ay navigasyon chip'leri (görsel, tıklanamaz) ──────────────────────────
    chips_html = '<div class="atk-ay-nav">'
    for i, ay_n in enumerate(AY_SIRASI):
        yn, _ = _ay_yil_for(secilen_yil, ay_n)
        is_sel = i == st.session_state["atk_ay_idx"]
        is_bugun_ay = ay_n == bugun.month and yn == bugun.year
        has_event = any(
            d.get("tarih_baslangic", "").startswith(f"{yn:04d}-{ay_n:02d}")
            for d in yil_data
        )
        if is_sel:
            bg, color, brd = "#2563eb", "white", "none"
        elif is_bugun_ay:
            bg, color, brd = "#dbeafe", "#1d4ed8", "2px solid #3b82f6"
        else:
            bg, color, brd = "#1A2035", "#475569", "none"

        dot = " •" if has_event and not is_sel else ""
        chips_html += (
            f'<span class="atk-ay-chip" '
            f'style="background:{bg};color:{color};border:{brd}">'
            f"{AYLAR_TR[ay_n]}{dot}</span>"
        )
    chips_html += "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

    # ── Yeni Etkinlik Formu ───────────────────────────────────────────────────
    if st.session_state.get("atk_form_ac"):
        styled_section("➕ Yeni Etkinlik / Tatil / Bayram / Gezi Ekle", "#10b981")
        _render_etkinlik_formu(secilen_yil, form_key="yeni")
        if st.button("✖ Formu Kapat", key="atk_form_kapat"):
            st.session_state["atk_form_ac"] = False
            st.rerun()
        st.markdown("---")

    # ── Takvim + Ay Listesi ───────────────────────────────────────────────────
    col_cal, col_list = st.columns([7, 3], gap="medium")

    with col_cal:
        styled_section(f"📅 {AYLAR_TR[ay_no]} {yil_no} Takvimi", "#2563eb")
        _render_ay_takvimi(yil_no, ay_no, yil_data, bugun)

    with col_list:
        styled_section(f"📋 {AYLAR_TR[ay_no]} Etkinlikleri", "#6366f1")
        if not ay_etk:
            styled_info_banner(f"{AYLAR_TR[ay_no]} için etkinlik eklenmemiş.", "info")
        else:
            for e in ay_etk:
                eid = e.get("id", "")
                renk = e.get("renk", "#6b7280")
                tur_label = TUR_MAP.get(e.get("tur", ""), ("📌 Diğer", "#6b7280"))[0]
                bas = e.get("tarih_baslangic", "")
                bit = e.get("tarih_bitis", "")
                tarih_txt = bas if (not bit or bit == bas) else f"{bas} → {bit}"
                saat_txt = f" 🕐 {e['saat']}" if e.get("saat") else ""
                aciklama_kisa = e.get("aciklama", "")[:55]
                aciklama_html = (
                    f"<div style='font-size:0.7rem;color:#94a3b8;margin-top:3px'>"
                    f"{aciklama_kisa}{'…' if len(e.get('aciklama','')) > 55 else ''}</div>"
                    if e.get("aciklama")
                    else ""
                )

                st.markdown(
                    f'<div class="atk-event-card" style="border-left:4px solid {renk};background:{renk}14;">'
                    f"<div style='font-size:0.72rem;font-weight:700;color:{renk}'>{tur_label}</div>"
                    f"<div style='font-size:0.84rem;font-weight:600;color:#94A3B8;margin:2px 0'>{e.get('baslik','')}</div>"
                    f"<div style='font-size:0.71rem;color:#64748b'>📅 {tarih_txt}{saat_txt}</div>"
                    f"{aciklama_html}</div>",
                    unsafe_allow_html=True,
                )

                ec1, ec2 = st.columns(2)
                with ec1:
                    if st.button(
                        "✏️ Düzenle", key=f"atk_edit_{eid}",
                        use_container_width=True
                    ):
                        st.session_state[f"atk_edit_{eid}"] = not st.session_state.get(f"atk_edit_{eid}", False)
                with ec2:
                    if st.button(
                        "🗑️ Sil", key=f"atk_del_{eid}",
                        use_container_width=True
                    ):
                        _delete_etkinlik(eid)
                        st.rerun()

                if st.session_state.get(f"atk_edit_{eid}"):
                    with st.expander(f"Düzenle: {e.get('baslik','')}", expanded=True):
                        _render_etkinlik_formu(
                            secilen_yil, etkinlik=e, form_key=f"edit_{eid}"
                        )
                        if st.button("✖ İptal", key=f"atk_edit_cancel_{eid}"):
                            st.session_state[f"atk_edit_{eid}"] = False
                            st.rerun()

    # ── Tüm Etkinlikler (Yıllık Liste) ───────────────────────────────────────
    st.markdown("---")
    with st.expander(f"📋 {secilen_yil} — Tüm Etkinlikler ({len(yil_data)} kayıt)", expanded=False
    ):
        if not yil_data:
            styled_info_banner(
                "Bu akademik yıl için henüz etkinlik eklenmemiş.", "info"
            )
        else:
            sıralı = sorted(yil_data, key=lambda x: x.get("tarih_baslangic", ""))

            # Ay bazlı grupla
            ay_grup: dict[str, list] = {}
            for e in sıralı:
                bas_str = e.get("tarih_baslangic", "")
                try:
                    bas_d = date.fromisoformat(bas_str)
                    ay_key = f"{bas_d.year}-{bas_d.month:02d}"
                    ay_label = f"{AYLAR_TR[bas_d.month]} {bas_d.year}"
                except Exception:
                    ay_key = "bilinmiyor"
                    ay_label = "Bilinmiyor"
                ay_grup.setdefault((ay_key, ay_label), []).append(e)

            for (ay_key, ay_label), events in sorted(ay_grup.items(), key=lambda x: x[0][0]):
                st.markdown(
                    f"<div style='font-size:0.85rem;font-weight:700;color:#2563eb;"
                    f"border-bottom:2px solid #dbeafe;padding:6px 0 4px 0;margin:10px 0 4px 0'>"
                    f"📆 {ay_label}</div>",
                    unsafe_allow_html=True,
                )
                for e in events:
                    eid = e.get("id", "")
                    renk = e.get("renk", "#6b7280")
                    tur_label = TUR_MAP.get(e.get("tur", ""), ("📌", "#6b7280"))[0]
                    bas = e.get("tarih_baslangic", "")
                    bit = e.get("tarih_bitis", "")
                    tarih_txt = bas if (not bit or bit == bas) else f"{bas} → {bit}"

                    dc1, dc2, dc3 = st.columns([6, 1, 1])
                    with dc1:
                        st.markdown(
                            f"<div style='display:flex;align-items:center;gap:8px;"
                            f"padding:6px 0;border-bottom:1px solid #1A2035'>"
                            f"<span style='background:{renk};color:white;font-size:0.65rem;"
                            f"font-weight:700;padding:2px 7px;border-radius:10px;white-space:nowrap'>{tur_label}</span>"
                            f"<span style='font-weight:600;font-size:0.83rem;color:#94A3B8;flex:1'>{e.get('baslik','')}</span>"
                            f"<span style='font-size:0.73rem;color:#94a3b8;white-space:nowrap'>📅 {tarih_txt}</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    with dc2:
                        if st.button("✏️", key=f"atk_all_edit_{eid}", use_container_width=True):
                            st.session_state[f"atk_all_edit_{eid}"] = not st.session_state.get(f"atk_all_edit_{eid}", False)
                    with dc3:
                        if st.button("🗑️", key=f"atk_all_del_{eid}", use_container_width=True):
                            _delete_etkinlik(eid)
                            st.rerun()

                    if st.session_state.get(f"atk_all_edit_{eid}"):
                        with st.expander(f"Düzenle: {e.get('baslik','')}", expanded=True):
                            _render_etkinlik_formu(
                                secilen_yil, etkinlik=e, form_key=f"all_edit_{eid}"
                            )
                            if st.button("✖ İptal", key=f"atk_all_cancel_{eid}"):
                                st.session_state[f"atk_all_edit_{eid}"] = False
                                st.rerun()


# Legacy alias — replaced by academic_calendar.render_academic_calendar
_LEGACY = [render_akademik_takvim]
