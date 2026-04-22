"""
Servis GPS Takip Modulu - Streamlit UI
=======================================
Okul servisi canli takip, guzergah yonetimi, ogrenci atama ve raporlar.
"""

import streamlit as st
import json
import random
import uuid
import pandas as pd
from pathlib import Path
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Veri Yardimcilari
# ---------------------------------------------------------------------------

SERVIS_PATH = "data/akademik/servis_bilgileri.json"
STUDENTS_PATH = "data/akademik/students.json"


def _load(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _gen_id(prefix="srv"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def _load_students():
    return _load(STUDENTS_PATH)


def _student_name(sid, students):
    for s in students:
        if s.get("id") == sid:
            return f"{s['ad']} {s['soyad']} ({s.get('sinif', '?')}{s.get('sube', '')})"
    return sid


# ---------------------------------------------------------------------------
# GPS Simuelasyon
# ---------------------------------------------------------------------------

ISTANBUL_CENTER = (41.0082, 28.9784)

def _random_istanbul_coords(n=1):
    """Istanbul icinde rastgele GPS koordinatlari uret."""
    coords = []
    for _ in range(n):
        lat = ISTANBUL_CENTER[0] + random.uniform(-0.08, 0.08)
        lon = ISTANBUL_CENTER[1] + random.uniform(-0.15, 0.15)
        coords.append({"lat": lat, "lon": lon})
    return coords


def _simulate_bus_status():
    """Rastgele servis durumu belirle."""
    r = random.random()
    if r < 0.5:
        return "yolda"
    elif r < 0.8:
        return "bekleniyor"
    else:
        return "tamamlandi"


DURUM_COLORS = {
    "yolda": "green",
    "bekleniyor": "orange",
    "tamamlandi": "grey",
    "aktif": "green",
}

DURUM_EMOJI = {
    "yolda": "🟢",
    "bekleniyor": "🟠",
    "tamamlandi": "⚫",
}

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def _inject_css():
    st.markdown("""
    <style>
    .servis-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 5px solid #1a73e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .servis-card h4 { margin: 0 0 8px 0; color: #1a237e; }
    .servis-card p { margin: 2px 0; font-size: 14px; }
    .badge-yolda { background: #28a745; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
    .badge-bekleniyor { background: #fd7e14; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
    .badge-tamamlandi { background: #6c757d; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
    .badge-aktif { background: #28a745; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
    .stat-box {
        background: linear-gradient(135deg, #1a237e 0%, #1565c0 100%);
        color: white; border-radius: 12px; padding: 18px; text-align: center;
    }
    .stat-box .val { font-size: 28px; font-weight: 700; }
    .stat-box .lbl { font-size: 13px; opacity: .85; }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# TAB 1: Canli Takip
# ---------------------------------------------------------------------------

def _tab_canli_takip():
    st.subheader("Canli Servis Takip")
    routes = _load(SERVIS_PATH)
    students = _load_students()

    if not routes:
        st.info("Henuz servis guzergahi tanimlanmamis.")
        return

    # Ozet metrikler
    toplam_kapasite = sum(r.get("kapasite", 0) for r in routes)
    toplam_ogrenci = sum(r.get("ogrenci_sayisi", 0) for r in routes)
    cols = st.columns(4)
    with cols[0]:
        st.metric("Toplam Servis", len(routes))
    with cols[1]:
        st.metric("Toplam Ogrenci", toplam_ogrenci)
    with cols[2]:
        st.metric("Toplam Kapasite", toplam_kapasite)
    with cols[3]:
        doluluk = round(toplam_ogrenci / toplam_kapasite * 100, 1) if toplam_kapasite else 0
        st.metric("Ortalama Doluluk", f"%{doluluk}")

    st.divider()

    # Harita - tum servislerin simule konumlari
    all_coords = []
    bus_positions = {}
    for r in routes:
        coord = _random_istanbul_coords(1)[0]
        all_coords.append(coord)
        bus_positions[r["id"]] = coord

    map_df = pd.DataFrame(all_coords)
    st.map(map_df, zoom=10)

    st.caption(f"Son guncelleme: {datetime.now().strftime('%H:%M:%S')} (simuelasyon)")

    st.divider()

    # Servis kartlari
    for i in range(0, len(routes), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(routes):
                break
            r = routes[idx]
            sim_durum = _simulate_bus_status()
            kapasite = r.get("kapasite", 1)
            ogr_say = r.get("ogrenci_sayisi", 0)
            doluluk_pct = min(ogr_say / kapasite, 1.0) if kapasite else 0

            with col:
                st.markdown(f"""
                <div class="servis-card">
                    <h4>{r.get('plaka', '---')} - {r.get('guzergah', '---')}</h4>
                    <p><b>Sofor:</b> {r.get('sofor', '-')} | <b>Hostes:</b> {r.get('hostes', '-')}</p>
                    <p><b>Kalkis:</b> {r.get('kalkis_saati', '-')} | <b>Varis:</b> {r.get('varis_saati', '-')}</p>
                    <p><b>Durum:</b> <span class="badge-{sim_durum}">{sim_durum.upper()}</span></p>
                    <p><b>Konum:</b> {bus_positions[r['id']]['lat']:.4f}, {bus_positions[r['id']]['lon']:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(doluluk_pct, text=f"Doluluk: {ogr_say}/{kapasite}")


# ---------------------------------------------------------------------------
# TAB 2: Guzergah Yonetimi
# ---------------------------------------------------------------------------

def _tab_guzergah_yonetimi():
    st.subheader("Guzergah Yonetimi")
    routes = _load(SERVIS_PATH)

    # Mevcut guzergahlar listesi
    if routes:
        df_data = []
        for r in routes:
            df_data.append({
                "Plaka": r.get("plaka", ""),
                "Guzergah": r.get("guzergah", ""),
                "Sofor": r.get("sofor", ""),
                "Hostes": r.get("hostes", ""),
                "Kapasite": r.get("kapasite", 0),
                "Ogrenci": r.get("ogrenci_sayisi", 0),
                "Kalkis": r.get("kalkis_saati", ""),
                "Varis": r.get("varis_saati", ""),
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("Henuz guzergah tanimlanmamis.")

    st.divider()

    # Ekleme / Duzenleme
    col_mode, _ = st.columns([1, 2])
    with col_mode:
        mode = st.radio("Islem", ["Yeni Ekle", "Duzenle", "Sil"], horizontal=True, key="guz_mode")

    if mode == "Yeni Ekle":
        with st.form("add_route_form", clear_on_submit=True):
            st.markdown("**Yeni Guzergah Ekle**")
            c1, c2 = st.columns(2)
            with c1:
                plaka = st.text_input("Plaka", placeholder="34 XX 000")
                guzergah = st.text_input("Guzergah Adi", placeholder="Kadikoy - Atasehir")
                sofor = st.text_input("Sofor")
                hostes = st.text_input("Hostes")
            with c2:
                kapasite = st.number_input("Kapasite", min_value=1, max_value=60, value=30)
                kalkis = st.time_input("Kalkis Saati")
                varis = st.time_input("Varis Saati")
                donus = st.time_input("Donus Saati")

            if st.form_submit_button("Kaydet", type="primary"):
                if not plaka or not guzergah:
                    st.error("Plaka ve guzergah alanlari zorunludur.")
                else:
                    new_route = {
                        "id": _gen_id(),
                        "guzergah": guzergah,
                        "plaka": plaka,
                        "sofor": sofor,
                        "hostes": hostes,
                        "kapasite": kapasite,
                        "ogrenci_sayisi": 0,
                        "ogrenci_idleri": [],
                        "kalkis_saati": kalkis.strftime("%H:%M"),
                        "varis_saati": varis.strftime("%H:%M"),
                        "donus_saati": donus.strftime("%H:%M"),
                        "durum": "aktif",
                    }
                    routes.append(new_route)
                    _save(SERVIS_PATH, routes)
                    st.success(f"Guzergah '{guzergah}' eklendi.")
                    st.rerun()

    elif mode == "Duzenle" and routes:
        labels = [f"{r['plaka']} - {r['guzergah']}" for r in routes]
        sel = st.selectbox("Guzergah Sec", labels, key="edit_route_sel")
        idx = labels.index(sel)
        r = routes[idx]

        with st.form("edit_route_form"):
            st.markdown(f"**Duzenle: {r['plaka']}**")
            c1, c2 = st.columns(2)
            with c1:
                plaka = st.text_input("Plaka", value=r.get("plaka", ""))
                guzergah = st.text_input("Guzergah", value=r.get("guzergah", ""))
                sofor = st.text_input("Sofor", value=r.get("sofor", ""))
                hostes = st.text_input("Hostes", value=r.get("hostes", ""))
            with c2:
                kapasite = st.number_input("Kapasite", min_value=1, max_value=60, value=r.get("kapasite", 30))
                kalkis = st.text_input("Kalkis Saati", value=r.get("kalkis_saati", "07:30"))
                varis = st.text_input("Varis Saati", value=r.get("varis_saati", "08:15"))
                donus = st.text_input("Donus Saati", value=r.get("donus_saati", "16:00"))

            if st.form_submit_button("Guncelle", type="primary"):
                routes[idx].update({
                    "plaka": plaka,
                    "guzergah": guzergah,
                    "sofor": sofor,
                    "hostes": hostes,
                    "kapasite": kapasite,
                    "kalkis_saati": kalkis,
                    "varis_saati": varis,
                    "donus_saati": donus,
                })
                _save(SERVIS_PATH, routes)
                st.success("Guzergah guncellendi.")
                st.rerun()

    elif mode == "Sil" and routes:
        labels = [f"{r['plaka']} - {r['guzergah']}" for r in routes]
        sel = st.selectbox("Silinecek Guzergah", labels, key="del_route_sel")
        idx = labels.index(sel)
        if st.button("Sil", type="primary"):
            removed = routes.pop(idx)
            _save(SERVIS_PATH, routes)
            st.success(f"'{removed['guzergah']}' silindi.")
            st.rerun()


# ---------------------------------------------------------------------------
# TAB 3: Ogrenci Atama
# ---------------------------------------------------------------------------

def _tab_ogrenci_atama():
    st.subheader("Ogrenci - Servis Atama")
    routes = _load(SERVIS_PATH)
    students = _load_students()

    if not routes:
        st.warning("Once guzergah tanimlayin.")
        return

    labels = [f"{r['plaka']} - {r['guzergah']}" for r in routes]
    sel = st.selectbox("Guzergah Sec", labels, key="atama_route_sel")
    idx = labels.index(sel)
    route = routes[idx]

    assigned_ids = route.get("ogrenci_idleri", [])

    col_assigned, col_available = st.columns(2)

    with col_assigned:
        st.markdown(f"**Atanmis Ogrenciler ({len(assigned_ids)})**")
        remove_ids = []
        if assigned_ids:
            for sid in assigned_ids:
                name = _student_name(sid, students)
                checked = st.checkbox(name, value=True, key=f"rm_{route['id']}_{sid}")
                if not checked:
                    remove_ids.append(sid)
        else:
            st.info("Bu guzergaha atanmis ogrenci yok.")

    with col_available:
        st.markdown("**Mevcut Ogrenciler (Atanmamis)**")
        all_assigned = set()
        for r in routes:
            all_assigned.update(r.get("ogrenci_idleri", []))

        available = [s for s in students if s["id"] not in all_assigned]
        add_ids = []
        if available:
            for s in available[:30]:  # ilk 30 goster
                name = f"{s['ad']} {s['soyad']} ({s.get('sinif', '?')}{s.get('sube', '')})"
                checked = st.checkbox(name, value=False, key=f"add_{route['id']}_{s['id']}")
                if checked:
                    add_ids.append(s["id"])
            if len(available) > 30:
                st.caption(f"... ve {len(available) - 30} ogrenci daha")
        else:
            st.info("Tum ogrenciler bir guzergaha atanmis.")

    st.divider()

    if st.button("Degisiklikleri Kaydet", type="primary", key="save_atama"):
        new_assigned = [sid for sid in assigned_ids if sid not in remove_ids]
        new_assigned.extend(add_ids)
        routes[idx]["ogrenci_idleri"] = new_assigned
        routes[idx]["ogrenci_sayisi"] = len(new_assigned)
        _save(SERVIS_PATH, routes)
        st.success(f"Guzergah guncellendi. {len(remove_ids)} cikarildi, {len(add_ids)} eklendi.")
        st.rerun()


# ---------------------------------------------------------------------------
# TAB 4: Raporlar
# ---------------------------------------------------------------------------

def _tab_raporlar():
    st.subheader("Servis Raporlari")
    routes = _load(SERVIS_PATH)

    if not routes:
        st.info("Rapor icin guzergah verisi bulunamadi.")
        return

    # Doluluk istatistikleri
    st.markdown("#### Doluluk Oranlari")
    doluluk_data = []
    for r in routes:
        kap = r.get("kapasite", 1)
        ogr = r.get("ogrenci_sayisi", 0)
        oran = round(ogr / kap * 100, 1) if kap else 0
        doluluk_data.append({
            "Guzergah": r.get("guzergah", ""),
            "Plaka": r.get("plaka", ""),
            "Ogrenci": ogr,
            "Kapasite": kap,
            "Doluluk (%)": oran,
        })

    df_doluluk = pd.DataFrame(doluluk_data)
    st.dataframe(df_doluluk, use_container_width=True, hide_index=True)

    # Bar chart - ogrenci sayisi per route
    st.markdown("#### Guzergah Bazinda Ogrenci Sayisi")
    chart_df = pd.DataFrame({
        "Guzergah": [r.get("guzergah", "") for r in routes],
        "Ogrenci Sayisi": [r.get("ogrenci_sayisi", 0) for r in routes],
    })
    st.bar_chart(chart_df.set_index("Guzergah"))

    # Doluluk bar chart
    st.markdown("#### Doluluk Orani (%)")
    doluluk_chart = pd.DataFrame({
        "Guzergah": [d["Guzergah"] for d in doluluk_data],
        "Doluluk (%)": [d["Doluluk (%)"] for d in doluluk_data],
    })
    st.bar_chart(doluluk_chart.set_index("Guzergah"))

    st.divider()

    # Zamaninda varis performansi (mock)
    st.markdown("#### Zamaninda Varis Performansi (Simuelasyon)")
    perf_data = []
    for r in routes:
        on_time = random.randint(70, 100)
        perf_data.append({
            "Guzergah": r.get("guzergah", ""),
            "Plaka": r.get("plaka", ""),
            "Zamaninda (%)": on_time,
            "Gecikme (dk ort)": random.randint(0, 8) if on_time < 90 else 0,
        })
    df_perf = pd.DataFrame(perf_data)
    st.dataframe(df_perf, use_container_width=True, hide_index=True)

    # Ozet metrikler
    st.divider()
    st.markdown("#### Genel Ozet")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Guzergah", len(routes))
    with c2:
        st.metric("Toplam Ogrenci", sum(r.get("ogrenci_sayisi", 0) for r in routes))
    with c3:
        avg_doluluk = sum(d["Doluluk (%)"] for d in doluluk_data) / len(doluluk_data) if doluluk_data else 0
        st.metric("Ort. Doluluk", f"%{avg_doluluk:.1f}")
    with c4:
        avg_perf = sum(d["Zamaninda (%)"] for d in perf_data) / len(perf_data) if perf_data else 0
        st.metric("Ort. Zamaninda Varis", f"%{avg_perf:.0f}")


# ---------------------------------------------------------------------------
# ANA FONKSIYON
# ---------------------------------------------------------------------------

def render_servis_gps_takip():
    """Servis GPS Takip ana giris noktasi."""
    _inject_css()
    st.title("Servis GPS Takip Sistemi")
    st.caption("Okul servisi canli takip, guzergah yonetimi ve raporlama")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Canli Takip",
        "Guzergah Yonetimi",
        "Ogrenci Atama",
        "Raporlar",
    ])

    with tab1:
        _tab_canli_takip()
    with tab2:
        _tab_guzergah_yonetimi()
    with tab3:
        _tab_ogrenci_atama()
    with tab4:
        _tab_raporlar()


if __name__ == "__main__":
    render_servis_gps_takip()
