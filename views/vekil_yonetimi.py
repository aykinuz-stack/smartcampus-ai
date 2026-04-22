"""
Vekil Ogretmen Yonetimi
========================
Izinli ogretmenler icin vekil atama, bugunun vekilleri ve gecmis kayitlar.
"""

import json
import os
import uuid
from datetime import date, datetime, timedelta

import streamlit as st


# ── Veri Dosya Yollari ──────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "akademik")
VEKIL_PATH = os.path.join(DATA_DIR, "vekil_gorevler.json")
TEACHERS_PATH = os.path.join(DATA_DIR, "teachers.json")


# ── Yardimci Fonksiyonlar ──────────────────────────────────────────

def _load_json(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save_json(path: str, data: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_teachers() -> list[dict]:
    return _load_json(TEACHERS_PATH)


def _load_vekiller() -> list[dict]:
    return _load_json(VEKIL_PATH)


def _save_vekiller(data: list[dict]) -> None:
    _save_json(VEKIL_PATH, data)


def _ensure_sample_data() -> None:
    """Vekil gorev dosyasi bossa ornek veri olustur."""
    if os.path.exists(VEKIL_PATH):
        data = _load_json(VEKIL_PATH)
        if data:
            return

    teachers = _load_teachers()
    if len(teachers) < 2:
        return

    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    sample = [
        {
            "id": f"vkl_{uuid.uuid4().hex[:8]}",
            "izinli_ogretmen_id": teachers[0].get("id", ""),
            "izinli_ogretmen_adi": f"{teachers[0].get('ad', '')} {teachers[0].get('soyad', '')}".strip(),
            "vekil_ogretmen_id": teachers[1].get("id", ""),
            "vekil_ogretmen_adi": f"{teachers[1].get('ad', '')} {teachers[1].get('soyad', '')}".strip(),
            "tarih": today,
            "ders_saatleri": [1, 2, 3],
            "aciklama": "Saglik izni",
            "atayan": "Sistem",
            "olusturma_tarihi": datetime.now().isoformat(),
        },
        {
            "id": f"vkl_{uuid.uuid4().hex[:8]}",
            "izinli_ogretmen_id": teachers[2].get("id", "") if len(teachers) > 2 else teachers[0].get("id", ""),
            "izinli_ogretmen_adi": (
                f"{teachers[2].get('ad', '')} {teachers[2].get('soyad', '')}".strip()
                if len(teachers) > 2
                else f"{teachers[0].get('ad', '')} {teachers[0].get('soyad', '')}".strip()
            ),
            "vekil_ogretmen_id": teachers[1].get("id", ""),
            "vekil_ogretmen_adi": f"{teachers[1].get('ad', '')} {teachers[1].get('soyad', '')}".strip(),
            "tarih": yesterday,
            "ders_saatleri": [4, 5],
            "aciklama": "Seminer katilimi",
            "atayan": "Sistem",
            "olusturma_tarihi": (datetime.now() - timedelta(days=1)).isoformat(),
        },
    ]
    _save_vekiller(sample)


# ── CSS ─────────────────────────────────────────────────────────────

def _inject_css():
    st.markdown("""
    <style>
    .vekil-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        color: white;
    }
    .vekil-header h2 {
        color: white !important;
        margin: 0 0 4px 0;
        font-size: 1.4rem;
    }
    .vekil-header p {
        color: rgba(255,255,255,.75) !important;
        margin: 0;
        font-size: .85rem;
    }
    .vekil-card {
        background: rgba(30, 58, 95, 0.08);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .vekil-card-title {
        font-weight: 600;
        font-size: .95rem;
        color: #e2e8f0 !important;
    }
    .vekil-card-sub {
        font-size: .8rem;
        color: #94a3b8 !important;
    }
    .vekil-badge {
        display: inline-block;
        background: rgba(37, 99, 235, 0.15);
        color: #60a5fa !important;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: .72rem;
        font-weight: 600;
    }
    .vekil-stat {
        text-align: center;
        padding: 12px;
        background: rgba(37, 99, 235, 0.06);
        border-radius: 10px;
        border: 1px solid rgba(37, 99, 235, 0.1);
    }
    .vekil-stat-num {
        font-size: 1.6rem;
        font-weight: 700;
        color: #60a5fa !important;
    }
    .vekil-stat-label {
        font-size: .72rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: .05em;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Tab 1: Bugunun Vekilleri ────────────────────────────────────────

def _tab_bugun(vekiller: list[dict]):
    today = date.today().isoformat()
    bugun = [v for v in vekiller if v.get("tarih") == today]

    # Istatistikler
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="vekil-stat">
            <div class="vekil-stat-num">{len(bugun)}</div>
            <div class="vekil-stat-label">Bugun Vekil</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        toplam_saat = sum(len(v.get("ders_saatleri", [])) for v in bugun)
        st.markdown(f"""
        <div class="vekil-stat">
            <div class="vekil-stat-num">{toplam_saat}</div>
            <div class="vekil-stat-label">Toplam Ders Saati</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        izinli_set = {v.get("izinli_ogretmen_id") for v in bugun}
        st.markdown(f"""
        <div class="vekil-stat">
            <div class="vekil-stat-num">{len(izinli_set)}</div>
            <div class="vekil-stat-label">Izinli Ogretmen</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if not bugun:
        st.info("Bugun icin atanmis vekil ogretmen bulunmuyor.")
        return

    for v in bugun:
        saatler = ", ".join(str(s) for s in v.get("ders_saatleri", []))
        st.markdown(f"""
        <div class="vekil-card">
            <div class="vekil-card-title">
                {v.get('izinli_ogretmen_adi', '?')} yerine {v.get('vekil_ogretmen_adi', '?')}
            </div>
            <div class="vekil-card-sub">
                <span class="vekil-badge">{saatler}. ders saatleri</span>
                &nbsp;&middot;&nbsp; {v.get('aciklama', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Tab 2: Vekil Ata ───────────────────────────────────────────────

def _tab_vekil_ata(teachers: list[dict], vekiller: list[dict]):
    st.subheader("Yeni Vekil Atamasi")

    if len(teachers) < 2:
        st.warning("En az 2 ogretmen kayitli olmalidir.")
        return

    teacher_options = {
        f"{t.get('ad', '')} {t.get('soyad', '')} ({t.get('brans', '')})".strip(): t
        for t in teachers
        if t.get("durum", "aktif") != "pasif"
    }
    teacher_names = list(teacher_options.keys())

    col1, col2 = st.columns(2)
    with col1:
        izinli_sec = st.selectbox("Izinli Ogretmen", teacher_names, key="vekil_izinli")
    with col2:
        # Izinli secileni cikar
        vekil_names = [n for n in teacher_names if n != izinli_sec]
        vekil_sec = st.selectbox("Vekil Ogretmen", vekil_names, key="vekil_vekil")

    col3, col4 = st.columns(2)
    with col3:
        tarih = st.date_input("Tarih", value=date.today(), key="vekil_tarih")
    with col4:
        saatler = st.multiselect(
            "Ders Saatleri",
            options=list(range(1, 9)),
            default=[1, 2, 3],
            key="vekil_saatler",
        )

    aciklama = st.text_input("Aciklama (izin sebebi)", key="vekil_aciklama")

    if st.button("Vekil Ata", type="primary", use_container_width=True, key="vekil_ata_btn"):
        if not saatler:
            st.error("En az bir ders saati secmelisiniz.")
            return

        izinli_t = teacher_options[izinli_sec]
        vekil_t = teacher_options[vekil_sec]

        yeni = {
            "id": f"vkl_{uuid.uuid4().hex[:8]}",
            "izinli_ogretmen_id": izinli_t.get("id", ""),
            "izinli_ogretmen_adi": f"{izinli_t.get('ad', '')} {izinli_t.get('soyad', '')}".strip(),
            "vekil_ogretmen_id": vekil_t.get("id", ""),
            "vekil_ogretmen_adi": f"{vekil_t.get('ad', '')} {vekil_t.get('soyad', '')}".strip(),
            "tarih": tarih.isoformat(),
            "ders_saatleri": sorted(saatler),
            "aciklama": aciklama,
            "atayan": st.session_state.get("auth_user", {}).get("name", "Yonetici"),
            "olusturma_tarihi": datetime.now().isoformat(),
        }

        vekiller.append(yeni)
        _save_vekiller(vekiller)
        st.success(
            f"{izinli_t.get('ad', '')} {izinli_t.get('soyad', '')} yerine "
            f"{vekil_t.get('ad', '')} {vekil_t.get('soyad', '')} vekil atandi."
        )
        st.rerun()


# ── Tab 3: Gecmis ──────────────────────────────────────────────────

def _tab_gecmis(vekiller: list[dict]):
    st.subheader("Gecmis Vekil Atamalari")

    today = date.today().isoformat()
    gecmis = [v for v in vekiller if v.get("tarih", "") < today]
    gecmis.sort(key=lambda v: v.get("tarih", ""), reverse=True)

    if not gecmis:
        st.info("Gecmis vekil kaydi bulunmuyor.")
        return

    # Filtre
    col1, col2 = st.columns(2)
    with col1:
        tum_izinliler = sorted(set(v.get("izinli_ogretmen_adi", "") for v in gecmis))
        izinli_filtre = st.selectbox(
            "Izinli Ogretmen Filtre",
            ["Tumu"] + tum_izinliler,
            key="gecmis_izinli_filtre",
        )
    with col2:
        tum_vekiller = sorted(set(v.get("vekil_ogretmen_adi", "") for v in gecmis))
        vekil_filtre = st.selectbox(
            "Vekil Ogretmen Filtre",
            ["Tumu"] + tum_vekiller,
            key="gecmis_vekil_filtre",
        )

    if izinli_filtre != "Tumu":
        gecmis = [v for v in gecmis if v.get("izinli_ogretmen_adi") == izinli_filtre]
    if vekil_filtre != "Tumu":
        gecmis = [v for v in gecmis if v.get("vekil_ogretmen_adi") == vekil_filtre]

    for v in gecmis[:50]:
        saatler = ", ".join(str(s) for s in v.get("ders_saatleri", []))
        tarih_str = v.get("tarih", "")
        try:
            t = date.fromisoformat(tarih_str)
            tarih_gosterim = t.strftime("%d.%m.%Y")
        except (ValueError, TypeError):
            tarih_gosterim = tarih_str

        st.markdown(f"""
        <div class="vekil-card">
            <div class="vekil-card-title">
                {v.get('izinli_ogretmen_adi', '?')} yerine {v.get('vekil_ogretmen_adi', '?')}
            </div>
            <div class="vekil-card-sub">
                {tarih_gosterim} &nbsp;&middot;&nbsp;
                <span class="vekil-badge">{saatler}. ders</span>
                &nbsp;&middot;&nbsp; {v.get('aciklama', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.caption(f"Toplam {len(gecmis)} gecmis kayit gosteriliyor.")


# ── Ana Render ──────────────────────────────────────────────────────

def render_vekil_yonetimi():
    """Vekil Ogretmen Yonetimi ana fonksiyonu."""
    _inject_css()
    _ensure_sample_data()

    st.markdown("""
    <div class="vekil-header">
        <h2>Vekil Ogretmen Yonetimi</h2>
        <p>Izinli ogretmenler icin vekil atama ve takip sistemi</p>
    </div>
    """, unsafe_allow_html=True)

    teachers = _load_teachers()
    vekiller = _load_vekiller()

    tab1, tab2, tab3 = st.tabs([
        "Bugunun Vekilleri",
        "Vekil Ata",
        "Gecmis",
    ])

    with tab1:
        _tab_bugun(vekiller)
    with tab2:
        _tab_vekil_ata(teachers, vekiller)
    with tab3:
        _tab_gecmis(vekiller)
