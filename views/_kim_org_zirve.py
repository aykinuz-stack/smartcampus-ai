"""
Kurumsal Org — Organizasyon Sekmesi Zirve Ozellikleri
======================================================
1. Interaktif Org Semasi + Bos Pozisyon Radari
2. Yedekleme Plani (Succession Planning)
3. Organizasyon Zaman Makinesi (Versiyonlama + Karsilastirma)
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


_KAT_RENK = {
    "yonetim_kurulu": "#1a237e", "ust_yonetim": "#0d47a1",
    "okul_yoneticileri": "#1b5e20", "akademik": "#bf360c",
    "idari": "#4a148c", "destek": "#37474f",
    "ogretim": "#006064", "diger": "#616161",
}

_KAT_LABEL = {
    "yonetim_kurulu": "Yonetim Kurulu", "ust_yonetim": "Ust Yonetim",
    "okul_yoneticileri": "Okul Yoneticileri", "akademik": "Akademik Liderlik",
    "idari": "Idari Birimler", "destek": "Destek Hizmetleri",
    "ogretim": "Ogretim Kadrosu", "diger": "Diger",
}


# ============================================================
# 1. İNTERAKTİF ORG ŞEMASI + BOŞ POZİSYON RADARI
# ============================================================

def render_interaktif_sema(positions: list[dict]):
    """Interaktif org semasi — departman gruplama + bos pozisyon vurgulama."""
    styled_section("Interaktif Organizasyon Semasi", "#2563eb")

    if not positions:
        styled_info_banner("Pozisyon verisi bulunamadi. Pozisyon Yonetimi sekmesinden ekleyin.",
                            banner_type="warning", icon="⚠️")
        return

    # Istatistikler
    toplam = len(positions)
    dolu = sum(1 for p in positions if p.get("person_name", "").strip())
    bos = toplam - dolu
    doluluk = round(dolu / max(toplam, 1) * 100, 1)
    d_renk = "#10b981" if doluluk >= 90 else "#f59e0b" if doluluk >= 70 else "#ef4444"

    styled_stat_row([
        ("Toplam Pozisyon", str(toplam), "#2563eb", "📋"),
        ("Dolu", str(dolu), "#10b981", "✅"),
        ("Bos", str(bos), "#ef4444", "⬜"),
        ("Doluluk", f"%{doluluk}", d_renk, "📊"),
    ])

    # ── DOLULUK GAUGE ──
    st.markdown(f"""
    <div style="background:#0f172a;border:2px solid {d_renk};border-radius:16px;
                padding:20px;text-align:center;margin:12px 0;">
        <div style="font-size:48px;font-weight:900;color:{d_renk};
                    font-family:Playfair Display,Georgia,serif;">%{doluluk}</div>
        <div style="font-size:11px;color:#94a3b8;">Pozisyon Doluluk Orani · {dolu}/{toplam}</div>
        <div style="margin:12px auto 0;max-width:300px;">
            <div style="background:#1e293b;border-radius:6px;height:12px;overflow:hidden;">
                <div style="width:{doluluk}%;height:100%;background:{d_renk};border-radius:6px;"></div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── BOŞ POZİSYON ALARM ──
    bos_pozisyonlar = [p for p in positions if not p.get("person_name", "").strip()]
    if bos_pozisyonlar:
        styled_section(f"Bos Pozisyonlar ({len(bos_pozisyonlar)})", "#ef4444")
        for p in bos_pozisyonlar:
            kat = p.get("category", "diger")
            renk = _KAT_RENK.get(kat, "#616161")
            kat_label = _KAT_LABEL.get(kat, kat)
            parent = next((pp for pp in positions if pp.get("id") == p.get("parent_id")), None)
            parent_txt = parent.get("title", "") if parent else "Kok"

            # Bos sure tahmini (created_at varsa)
            created = p.get("created_at", "")
            bos_gun = ""
            if created:
                try:
                    bos_gun = f" · {(date.today() - date.fromisoformat(created[:10])).days} gundur bos"
                except Exception:
                    pass

            st.markdown(f"""
            <div style="background:#450a0a;border:2px dashed #ef4444;border-left:5px solid {renk};
                        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:800;color:#fca5a5;font-size:14px;">{p.get('title', '?')}</span>
                        <span style="color:#94a3b8;font-size:11px;margin-left:8px;">← {parent_txt}</span>
                    </div>
                    <span style="background:{renk}30;color:{renk};padding:2px 10px;border-radius:6px;
                                font-size:10px;font-weight:700;">{kat_label}</span>
                </div>
                <div style="font-size:10px;color:#fca5a5;margin-top:4px;">
                    ⬜ BU POZISYON BOS{bos_gun} · Departman: {p.get('department', '-')}</div>
            </div>""", unsafe_allow_html=True)

    # ── DEPARTMAN BAZLI GRUPLAMA ──
    styled_section("Departman Bazli Organizasyon")

    # Kategori bazli gruplama
    kat_gruplari: dict[str, list] = {}
    for p in positions:
        kat = p.get("category", "diger")
        kat_gruplari.setdefault(kat, []).append(p)

    kat_sira = ["yonetim_kurulu", "ust_yonetim", "okul_yoneticileri", "akademik", "idari", "destek", "ogretim", "diger"]

    for kat in kat_sira:
        poz_list = kat_gruplari.get(kat, [])
        if not poz_list:
            continue
        renk = _KAT_RENK.get(kat, "#616161")
        label = _KAT_LABEL.get(kat, kat)
        dolu_k = sum(1 for p in poz_list if p.get("person_name", "").strip())

        with st.expander(f"{label} ({dolu_k}/{len(poz_list)} dolu)", expanded=False):
            cols = st.columns(3)
            for idx, p in enumerate(sorted(poz_list, key=lambda x: x.get("order", 0))):
                is_bos = not p.get("person_name", "").strip()
                border = "2px dashed #ef4444" if is_bos else f"1px solid {renk}40"
                bg = "#450a0a08" if is_bos else "#0f172a"
                kisi = p.get("person_name", "") or "BOŞ"
                kisi_renk = "#ef4444" if is_bos else "#e2e8f0"

                # Alt pozisyonlar
                children = [c for c in positions if c.get("parent_id") == p.get("id")]
                child_txt = f"{len(children)} alt pozisyon" if children else ""

                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="background:{bg};border:{border};border-radius:12px;
                                padding:10px 14px;margin-bottom:8px;min-height:80px;">
                        <div style="font-size:12px;font-weight:800;color:{renk};">{p.get('title', '?')}</div>
                        <div style="font-size:14px;font-weight:700;color:{kisi_renk};margin:4px 0;">
                            {'⬜ ' if is_bos else '👤 '}{kisi}</div>
                        <div style="font-size:9px;color:#64748b;">
                            {p.get('department', '-')}{(' · ' + child_txt) if child_txt else ''}</div>
                    </div>""", unsafe_allow_html=True)


# ============================================================
# 2. YEDEKLEME PLANI (SUCCESSION PLANNING)
# ============================================================

def _yedekleme_path() -> str:
    return os.path.join(_td(), "yte", "yedekleme_plani.json")


def _load_yedekleme() -> list[dict]:
    return _lj(_yedekleme_path())


def _save_yedekleme(data: list[dict]):
    _sj(_yedekleme_path(), data)


def render_yedekleme_plani(positions: list[dict]):
    """Kritik pozisyonlar icin yedekleme plani."""
    styled_section("Yedekleme Plani (Succession Planning)", "#dc2626")
    styled_info_banner(
        "Kritik pozisyonlar icin 1. ve 2. yedek atayin. "
        "Yedek kisinin hazirlik puanini otomatik hesaplayin.",
        banner_type="warning", icon="🛡️")

    if not positions:
        styled_info_banner("Pozisyon verisi yok.", banner_type="warning", icon="⚠️")
        return

    yedekler = _load_yedekleme()
    yedek_map = {y["pozisyon_id"]: y for y in yedekler}

    # Kritik pozisyonlar (ust yonetim + okul yoneticileri + akademik liderlik)
    kritik_katlar = {"yonetim_kurulu", "ust_yonetim", "okul_yoneticileri", "akademik"}
    kritik_poz = [p for p in positions if p.get("category") in kritik_katlar and p.get("person_name", "").strip()]
    diger_poz = [p for p in positions if p not in kritik_poz and p.get("person_name", "").strip()]

    yedekli = sum(1 for p in kritik_poz if p.get("id") in yedek_map)
    yedeksiz = len(kritik_poz) - yedekli

    styled_stat_row([
        ("Kritik Pozisyon", str(len(kritik_poz)), "#dc2626", "🛡️"),
        ("Yedekli", str(yedekli), "#10b981", "✅"),
        ("Yedeksiz", str(yedeksiz), "#ef4444", "⚠️"),
        ("Risk", f"%{round(yedeksiz / max(len(kritik_poz), 1) * 100)}", "#f59e0b", "📊"),
    ])

    sub = st.tabs(["📊 Durum", "➕ Yedek Ata"])

    # ═══ DURUM ═══
    with sub[0]:
        styled_section("Kritik Pozisyon Yedekleme Durumu")

        for p in kritik_poz:
            pid = p.get("id", "")
            kat = p.get("category", "diger")
            renk = _KAT_RENK.get(kat, "#616161")
            ydek = yedek_map.get(pid)

            if ydek:
                y1 = ydek.get("yedek_1_ad", "—")
                y1_hazir = ydek.get("yedek_1_hazirlik", 0)
                y2 = ydek.get("yedek_2_ad", "—")
                y2_hazir = ydek.get("yedek_2_hazirlik", 0)
                durum_renk = "#10b981"
                durum_txt = "Yedekli"
            else:
                y1, y1_hazir, y2, y2_hazir = "—", 0, "—", 0
                durum_renk = "#ef4444"
                durum_txt = "YEDEKSIZ"

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {renk}40;border-left:5px solid {renk};
                        border-radius:0 14px 14px 0;padding:14px 18px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div>
                        <span style="font-weight:800;color:#e2e8f0;font-size:14px;">{p.get('title', '')}</span>
                        <span style="color:#94a3b8;font-size:11px;margin-left:8px;">({p.get('person_name', '')})</span>
                    </div>
                    <span style="background:{durum_renk}20;color:{durum_renk};padding:3px 12px;border-radius:8px;
                                font-size:11px;font-weight:700;">{durum_txt}</span>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 12px;">
                        <div style="font-size:9px;color:#64748b;">1. Yedek</div>
                        <div style="font-size:13px;font-weight:700;color:#e2e8f0;">{y1}</div>
                        <div style="font-size:10px;color:{'#10b981' if y1_hazir >= 70 else '#f59e0b' if y1_hazir >= 40 else '#ef4444'};">
                            Hazirlik: %{y1_hazir}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 12px;">
                        <div style="font-size:9px;color:#64748b;">2. Yedek</div>
                        <div style="font-size:13px;font-weight:700;color:#e2e8f0;">{y2}</div>
                        <div style="font-size:10px;color:{'#10b981' if y2_hazir >= 70 else '#f59e0b' if y2_hazir >= 40 else '#ef4444'};">
                            Hazirlik: %{y2_hazir}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Yedeksiz alarm
        yedeksiz_list = [p for p in kritik_poz if p.get("id") not in yedek_map]
        if yedeksiz_list:
            styled_section("YEDEKSIZ Kritik Pozisyonlar", "#ef4444")
            for p in yedeksiz_list:
                st.error(f"🚨 **{p.get('title', '')}** ({p.get('person_name', '')}) — yedek atanmamis!")

    # ═══ YEDEK ATA ═══
    with sub[1]:
        styled_section("Yedek Atama")
        if not kritik_poz:
            styled_info_banner("Kritik pozisyon yok.", banner_type="info", icon="✅")
        else:
            poz_labels = [f"{p.get('title', '')} — {p.get('person_name', '')}" for p in kritik_poz]
            secili_poz = st.selectbox("Pozisyon", poz_labels, key="yd_poz")

            if secili_poz:
                poz = kritik_poz[poz_labels.index(secili_poz)]
                pid = poz.get("id", "")

                # Yedek aday listesi (diger personel)
                personel_listesi = [p.get("person_name", "") for p in positions
                                     if p.get("person_name", "").strip() and p.get("id") != pid]

                with st.form("yedek_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        y1_ad = st.selectbox("1. Yedek", [""] + personel_listesi, key="yd_y1")
                        y1_hazir = st.slider("Hazirlik %", 0, 100, 50, key="yd_y1h")
                    with col2:
                        y2_ad = st.selectbox("2. Yedek", [""] + personel_listesi, key="yd_y2")
                        y2_hazir = st.slider("Hazirlik %", 0, 100, 30, key="yd_y2h")

                    notlar = st.text_area("Notlar", height=60, key="yd_not")

                    if st.form_submit_button("Kaydet", type="primary"):
                        yeni = {
                            "pozisyon_id": pid,
                            "pozisyon_adi": poz.get("title", ""),
                            "mevcut_kisi": poz.get("person_name", ""),
                            "yedek_1_ad": y1_ad, "yedek_1_hazirlik": y1_hazir,
                            "yedek_2_ad": y2_ad, "yedek_2_hazirlik": y2_hazir,
                            "notlar": notlar,
                            "updated_at": datetime.now().isoformat(),
                        }
                        # Guncelle veya ekle
                        mevcut = [y for y in yedekler if y.get("pozisyon_id") != pid]
                        mevcut.append(yeni)
                        _save_yedekleme(mevcut)
                        st.success(f"Yedekleme plani kaydedildi: {poz.get('title', '')}")
                        st.rerun()


# ============================================================
# 3. ORGANİZASYON ZAMAN MAKİNESİ
# ============================================================

def _snapshot_path() -> str:
    return os.path.join(_td(), "yte", "org_snapshots.json")


def _load_snapshots() -> list[dict]:
    return _lj(_snapshot_path())


def _save_snapshots(data: list[dict]):
    _sj(_snapshot_path(), data)


def render_zaman_makinesi(positions: list[dict]):
    """Org semasi versiyonlama + karsilastirma."""
    styled_section("Organizasyon Zaman Makinesi", "#6366f1")
    styled_info_banner(
        "Org semanizin anlık goruntusunu kaydedin. Herhangi iki tarihi karsilastirin. "
        "Eklenen, cikan, degisen pozisyonlari otomatik tespit edin.",
        banner_type="info", icon="⏰")

    snapshots = _load_snapshots()

    styled_stat_row([
        ("Kayitli Snapshot", str(len(snapshots)), "#6366f1", "📸"),
        ("Mevcut Pozisyon", str(len(positions)), "#2563eb", "📋"),
    ])

    sub = st.tabs(["📸 Snapshot Al", "⚖️ Karsilastir", "📜 Gecmis"])

    # ═══ SNAPSHOT AL ═══
    with sub[0]:
        styled_section("Anlık Goruntu Kaydet")
        st.markdown(f"**Mevcut durum:** {len(positions)} pozisyon · "
                     f"{sum(1 for p in positions if p.get('person_name', '').strip())} dolu")

        etiket = st.text_input("Snapshot Etiketi", key="zm_etiket",
                                placeholder="Ornek: 2026 Nisan — yeni kadro",
                                value=f"Snapshot {date.today().isoformat()}")

        if st.button("Snapshot Kaydet", key="zm_kaydet", type="primary", use_container_width=True):
            yeni = {
                "id": f"snap_{uuid.uuid4().hex[:8]}",
                "tarih": date.today().isoformat(),
                "etiket": etiket,
                "pozisyon_sayisi": len(positions),
                "dolu": sum(1 for p in positions if p.get("person_name", "").strip()),
                "pozisyonlar": [dict(p) for p in positions],  # derin kopya
                "created_at": datetime.now().isoformat(),
            }
            snapshots.append(yeni)
            _save_snapshots(snapshots)
            st.success(f"Snapshot kaydedildi: {etiket}")
            st.rerun()

    # ═══ KARŞILAŞTIR ═══
    with sub[1]:
        styled_section("Iki Donemi Karsilastir")

        if len(snapshots) < 1:
            styled_info_banner("Karsilastirma icin en az 1 snapshot + mevcut durum gerekli.",
                                banner_type="info", icon="📸")
        else:
            snap_labels = [f"{s['etiket']} ({s['tarih']} · {s['pozisyon_sayisi']} poz)" for s in snapshots]

            col1, col2 = st.columns(2)
            with col1:
                sol_sec = st.selectbox("Eski Donem", snap_labels, key="zm_sol")
            with col2:
                sag_sec = st.selectbox("Yeni Donem", ["Mevcut Durum"] + snap_labels, key="zm_sag")

            # Verileri al
            sol_snap = snapshots[snap_labels.index(sol_sec)]
            sol_poz = sol_snap.get("pozisyonlar", [])

            if sag_sec == "Mevcut Durum":
                sag_poz = positions
                sag_label = "Mevcut"
            else:
                sag_snap = snapshots[snap_labels.index(sag_sec)]
                sag_poz = sag_snap.get("pozisyonlar", [])
                sag_label = sag_snap.get("etiket", "?")

            if st.button("Karsilastir", key="zm_cmp_btn", type="primary"):
                sol_ids = {p.get("id"): p for p in sol_poz}
                sag_ids = {p.get("id"): p for p in sag_poz}

                eklenen = [sag_ids[pid] for pid in sag_ids if pid not in sol_ids]
                cikan = [sol_ids[pid] for pid in sol_ids if pid not in sag_ids]
                degisen = []
                for pid in sol_ids:
                    if pid in sag_ids:
                        sol_p = sol_ids[pid]
                        sag_p = sag_ids[pid]
                        farklar = []
                        for key in ("title", "person_name", "category", "department", "parent_id"):
                            if sol_p.get(key) != sag_p.get(key):
                                farklar.append(f"{key}: {sol_p.get(key, '-')} → {sag_p.get(key, '-')}")
                        if farklar:
                            degisen.append({"poz": sag_p, "farklar": farklar})

                # Ozet
                styled_stat_row([
                    ("Eski Pozisyon", str(len(sol_poz)), "#64748b", "📋"),
                    ("Yeni Pozisyon", str(len(sag_poz)), "#2563eb", "📋"),
                    ("Eklenen", str(len(eklenen)), "#10b981", "➕"),
                    ("Cikan", str(len(cikan)), "#ef4444", "➖"),
                    ("Degisen", str(len(degisen)), "#f59e0b", "🔄"),
                ])

                # Eklenen
                if eklenen:
                    styled_section(f"Eklenen Pozisyonlar ({len(eklenen)})", "#10b981")
                    for p in eklenen:
                        st.markdown(f"""
                        <div style="background:#052e16;border:1px solid #10b981;border-radius:8px;
                                    padding:8px 12px;margin-bottom:4px;">
                            <span style="color:#6ee7b7;font-weight:700;">➕ {p.get('title', '')}</span>
                            <span style="color:#94a3b8;font-size:11px;margin-left:8px;">
                                {p.get('person_name', '') or 'Bos'} · {_KAT_LABEL.get(p.get('category', ''), '')}</span>
                        </div>""", unsafe_allow_html=True)

                # Cikan
                if cikan:
                    styled_section(f"Cikan Pozisyonlar ({len(cikan)})", "#ef4444")
                    for p in cikan:
                        st.markdown(f"""
                        <div style="background:#450a0a;border:1px solid #ef4444;border-radius:8px;
                                    padding:8px 12px;margin-bottom:4px;">
                            <span style="color:#fca5a5;font-weight:700;">➖ {p.get('title', '')}</span>
                            <span style="color:#94a3b8;font-size:11px;margin-left:8px;">
                                {p.get('person_name', '') or 'Bos'}</span>
                        </div>""", unsafe_allow_html=True)

                # Degisen
                if degisen:
                    styled_section(f"Degisen Pozisyonlar ({len(degisen)})", "#f59e0b")
                    for d in degisen:
                        p = d["poz"]
                        fark_txt = " · ".join(d["farklar"][:3])
                        st.markdown(f"""
                        <div style="background:#78350f20;border:1px solid #f59e0b;border-radius:8px;
                                    padding:8px 12px;margin-bottom:4px;">
                            <span style="color:#fbbf24;font-weight:700;">🔄 {p.get('title', '')}</span>
                            <div style="font-size:10px;color:#94a3b8;margin-top:2px;">{fark_txt}</div>
                        </div>""", unsafe_allow_html=True)

                if not eklenen and not cikan and not degisen:
                    st.success("Iki donem arasinda hicbir fark yok!")

    # ═══ GEÇMİŞ ═══
    with sub[2]:
        styled_section("Kayitli Snapshot'lar")
        if not snapshots:
            styled_info_banner("Henuz snapshot alinmamis.", banner_type="info", icon="📸")
        else:
            for s in sorted(snapshots, key=lambda x: x.get("tarih", ""), reverse=True):
                dolu = s.get("dolu", 0)
                toplam = s.get("pozisyon_sayisi", 0)
                doluluk = round(dolu / max(toplam, 1) * 100)
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #6366f130;border-radius:10px;
                            padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:700;color:#e2e8f0;font-size:13px;">📸 {s.get('etiket', '')}</span>
                        <span style="color:#94a3b8;font-size:11px;margin-left:8px;">{s.get('tarih', '')}</span>
                    </div>
                    <div style="display:flex;gap:8px;font-size:11px;">
                        <span style="color:#2563eb;">{toplam} poz</span>
                        <span style="color:#10b981;">{dolu} dolu</span>
                        <span style="color:#f59e0b;">%{doluluk}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Sil
            sil_sec = st.selectbox("Snapshot Sil", [""] + [s["etiket"] for s in snapshots], key="zm_sil")
            if sil_sec and st.button("Sil", key="zm_sil_btn"):
                snapshots = [s for s in snapshots if s["etiket"] != sil_sec]
                _save_snapshots(snapshots)
                st.success(f"Silindi: {sil_sec}")
                st.rerun()
