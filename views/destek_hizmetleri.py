"""
DES-01 Destek Hizmetleri Takip Modulu - Streamlit UI
=====================================================
Dashboard, talepler, periyodik isler, denetimler, PBK,
tedarikciler, raporlar ve ayarlar.
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta
from collections import Counter

import streamlit as st
from utils.ui_kit import confirm_action
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info, CHART_PALETTE
from models.destek_hizmetleri import (
    DestekDataStore,
    HizmetAlani, AltKategori, SLAAyar, Tedarikci, Ticket,
    GorevSablonu, PeriyodikGorev, DenetimFormu, DenetimMaddesi,
    Denetim, BakimKalemi, BakimKaydi, DestekAyar, FirmaHavuzu,
    SLACalculator, DenetimScorer, PeriyodikGorevPlanner, BakimPlanner,
    TICKET_STATUSES, TICKET_PRIORITIES, DENETIM_SONUCLARI,
    DENETIM_DURUMLARI, BAKIM_DURUMLARI, BAKIM_SONUCLARI,
    YURUTUCU_TIPLERI, PERIYOT_TIPLERI, GOREV_DURUMLARI,
    KADEME_SECENEKLERI, BULGU_SEVIYELERI, BULGU_DURUMLARI,
    NEXT_STATUS_MAP, BAKIM_SONUC_SECENEKLERI, FIRMA_SEKTORLER,
)
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("destek_hizmetleri")
except Exception:
    pass


# ============================================================
# STORE INIT
# ============================================================

def _get_destek_store() -> DestekDataStore:
    base = os.path.join(get_tenant_dir(), "destek")
    store = DestekDataStore(base)
    _pop_key = "des01_defaults_populated"
    if _pop_key not in st.session_state:
        store.auto_populate_defaults()
        st.session_state[_pop_key] = True
    return store


# ============================================================
# CSS & STYLED HELPERS
# ============================================================

def _inject_des_css():
    inject_common_css("des")
    st.markdown("""
    <style>
    :root {
        --des-primary: #2563eb;
        --des-primary-dark: #1e40af;
        --des-primary-light: #60a5fa;
        --des-success: #10b981;
        --des-warning: #f59e0b;
        --des-danger: #ef4444;
        --des-purple: #8b5cf6;
        --des-teal: #0d9488;
        --des-dark: #0B0F19;
    }
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: linear-gradient(180deg, #0B0F19 0%, #131825 100%);
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #2563eb;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
    }
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
    hr { border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #cbd5e1 50%, transparent 100%) !important; }
    </style>
    """, unsafe_allow_html=True)


def _sla_badge_html(ticket: dict) -> str:
    remaining = SLACalculator.get_remaining_minutes(ticket)
    if remaining is None:
        return "<span style='color:#64748b'>-</span>"
    if remaining < 0:
        return "<span style='background:#fef2f2;color:#dc2626;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:700'>SLA IHLAL</span>"
    hours = remaining // 60
    if hours < 4:
        return f"<span style='background:#fffbeb;color:#d97706;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:600'>{hours}s {remaining % 60}dk</span>"
    return f"<span style='background:#f0fdf4;color:#059669;padding:2px 8px;border-radius:6px;font-size:0.75rem;font-weight:600'>{hours}s</span>"


def _priority_color(oncelik: str) -> str:
    return {"Kritik": "#ef4444", "Yuksek": "#f59e0b", "Normal": "#2563eb", "Dusuk": "#64748b"}.get(oncelik, "#64748b")


def _status_color(durum: str) -> str:
    return {
        "Açık": "#ef4444", "Atandi": "#f59e0b", "Kabul Edildi": "#8b5cf6",
        "İşlemde": "#2563eb", "Parca Bekleniyor": "#d97706",
        "Tamamlandı": "#10b981", "Kontrol": "#0d9488", "Kapandi": "#64748b",
    }.get(durum, "#64748b")


def _alan_adi_map(store: DestekDataStore) -> dict[str, str]:
    return {ha.alan_kodu: ha.alan_adi for ha in store.load_objects("hizmet_alanlari")}


# ============================================================
# TAB 1: DASHBOARD
# ============================================================

def _render_dashboard(store: DestekDataStore):
    tickets = store.load_list("tickets")
    gorevler = store.load_list("periyodik_gorevler")
    today_str = date.today().isoformat()

    acik = [t for t in tickets if t.get("durum") not in ("Kapandi", "Tamamlandı", "Kontrol")]
    sla_risk = [t for t in acik if SLACalculator.check_sla_violation(t)]
    kritik = [t for t in acik if t.get("oncelik") == "Kritik"]
    bugun_gorev = [g for g in gorevler if g.get("plan_tarihi") == today_str and g.get("durum") != "Tamamlandı"]

    styled_stat_row([
        ("Açık Talepler", len(acik), "#ef4444", "\U0001f4dd"),
        ("SLA Risk", len(sla_risk), "#f59e0b", "\u26a0\ufe0f"),
        ("Kritik Olaylar", len(kritik), "#8b5cf6", "\U0001f6a8"),
        ("Bugün Periyodik", len(bugun_gorev), "#2563eb", "\U0001f504"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    alan_map = _alan_adi_map(store)

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Açık Talepler", "#ef4444")
        if acik:
            rows = []
            for t in sorted(acik, key=lambda x: x.get("created_at", ""), reverse=True)[:10]:
                rows.append({
                    "No": t.get("ticket_no", ""),
                    "Alan": alan_map.get(t.get("hizmet_alani_kodu", ""), t.get("hizmet_alani_kodu", "")),
                    "Öncelik": t.get("oncelik", ""),
                    "Durum": t.get("durum", ""),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Açık talep bulunmuyor.", "success")

    with c2:
        styled_section("SLA Risk Listesi", "#f59e0b")
        if sla_risk:
            rows = []
            for t in sla_risk[:10]:
                rows.append({
                    "No": t.get("ticket_no", ""),
                    "Alan": alan_map.get(t.get("hizmet_alani_kodu", ""), ""),
                    "Öncelik": t.get("oncelik", ""),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("SLA riski olan talep yok.", "success")

    st.divider()
    styled_section("Bugünün Periyodik Görevleri", "#2563eb")
    if bugun_gorev:
        sab_map = {s.id: s.sablon_adi for s in store.load_objects("gorev_sablonlari")}
        rows = []
        for g in bugun_gorev:
            rows.append({
                "Görev": sab_map.get(g.get("sablon_id", ""), "Bilinmeyen"),
                "Sorumlu": g.get("sorumlu_kisi", ""),
                "Durum": g.get("durum", ""),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner("Bugüne ait periyodik gorev yok.", "info")

    # Hizmet Alani Dagilimi - Sunburst + Bar (Excel stili)
    if tickets:
        st.divider()
        styled_section("Hizmet Alani / Alt Kategori Dagilimi", "#0d9488")
        alan_counts = Counter(t.get("hizmet_alani_kodu", "DIG") for t in tickets)
        chart_data = {alan_map.get(k, k): v for k, v in alan_counts.most_common(8)}

        # Alt kategori verisi hazirla (sunburst dis halka)
        alt_kat_map = {ak.alt_kategori_kodu: ak.alt_kategori_adi for ak in store.load_objects("alt_kategoriler")}
        alan_sub: dict[str, list[tuple[str, float]]] = {}
        for alan_kodu, _ in alan_counts.most_common(8):
            alan_adi = alan_map.get(alan_kodu, alan_kodu)
            alt_cnt = Counter(
                alt_kat_map.get(t.get("alt_kategori_kodu", ""), t.get("alt_kategori_kodu", "Diğer"))
                for t in tickets if t.get("hizmet_alani_kodu") == alan_kodu
            )
            alan_sub[alan_adi] = [(k, v) for k, v in alt_cnt.most_common()]

        if chart_data:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    ReportStyler.sunburst_chart_svg(chart_data, alan_sub, size=300,
                                                     title="Hizmet Alani / Alt Kategori"),
                    unsafe_allow_html=True)
            with c2:
                st.markdown(ReportStyler.horizontal_bar_html(chart_data, "#4472C4", max_width_px=300), unsafe_allow_html=True)

        # Oncelik dagilimi donut
        onc_counts = Counter(t.get("oncelik", "Normal") for t in tickets)
        durum_counts = Counter(t.get("durum", "Açık") for t in tickets)
        if onc_counts:
            c3, c4 = st.columns(2)
            with c3:
                styled_section("Öncelik Dagilimi", "#ED7D31")
                st.markdown(ReportStyler.donut_chart_svg(
                    dict(onc_counts.most_common()),
                    colors=["#ED7D31", "#FFC000", "#4472C4", "#A5A5A5"], size=155),
                    unsafe_allow_html=True)
            with c4:
                styled_section("Durum Dagilimi", "#4472C4")
                st.markdown(ReportStyler.horizontal_bar_html(
                    dict(durum_counts.most_common()), "#4472C4", max_width_px=300),
                    unsafe_allow_html=True)


# ============================================================
# TAB 2: TALEPLER
# ============================================================

def _render_talepler(store: DestekDataStore):
    sub = st.tabs(["➕ Talep Aç", "📋 Talepler Listesi", "🔍 Talep Detay"])

    with sub[0]:
        _render_talep_ac(store)
    with sub[1]:
        _render_talep_listesi(store)
    with sub[2]:
        _render_talep_detay(store)


def _render_talep_ac(store: DestekDataStore):
    styled_section("Yeni Talep Oluştur", "#2563eb")
    alanlar = [ha for ha in store.load_objects("hizmet_alanlari") if ha.aktif_durumu == "Evet"]
    if not alanlar:
        styled_info_banner("Hizmet alanı tanımlanmamış. Ayarlar sekmesinden ekleyin.", "warning")
        return

    alan_options = {ha.alan_adi: ha.alan_kodu for ha in alanlar}
    alan_map_rev = {ha.alan_kodu: ha for ha in alanlar}

    c1, c2 = st.columns(2)
    with c1:
        sel_alan_adi = st.selectbox("Hizmet Alani *", list(alan_options.keys()), key="des_talep_alan")
        sel_alan_kodu = alan_options.get(sel_alan_adi, "")

        alt_kats = [ak for ak in store.load_objects("alt_kategoriler")
                    if ak.alan_kodu == sel_alan_kodu and ak.aktif_mi]
        if alt_kats:
            alt_kat_options = {ak.alt_kategori_adi: ak.alt_kategori_kodu for ak in alt_kats}
            sel_alt = st.selectbox("Alt Kategori *", list(alt_kat_options.keys()), key="des_talep_altkat")
            sel_alt_kodu = alt_kat_options.get(sel_alt, "")
        else:
            sel_alt_kodu = ""
            st.info("Bu alan için alt kategori tanımlanmamış.")

        lokasyon = st.text_input("Lokasyon *", placeholder="Ornek: A Blok, 2. Kat, Oda 204", key="des_talep_lok")
    with c2:
        kademe = st.selectbox("Kademe *", KADEME_SECENEKLERI, key="des_talep_kademe")
        oncelik = st.selectbox("Öncelik *", TICKET_PRIORITIES, index=2, key="des_talep_oncelik")
        ist_c1, ist_c2 = st.columns(2)
        with ist_c1:
            istenen_tarih = st.date_input("Istenen Tarih (opsiyonel)", value=None, key="des_talep_ist_tarih")
        with ist_c2:
            istenen_saat = st.time_input("Istenen Saat", value=None, key="des_talep_ist_saat")
        if istenen_tarih and istenen_saat:
            istenen = datetime.combine(istenen_tarih, istenen_saat).isoformat()
        elif istenen_tarih:
            istenen = istenen_tarih.isoformat()
        else:
            istenen = ""

    c3, c4 = st.columns(2)
    with c3:
        talep_eden = st.text_input("Talep Eden *", placeholder="Adi Soyadi / Birimi", key="des_talep_eden")
    with c4:
        atanan_kisi = st.text_input("Yapacak Kisi (opsiyonel)", placeholder="Atanan personel / firma", key="des_talep_atanan")

    aciklama = st.text_area("Açıklama *", height=100, key="des_talep_aciklama")

    if st.button("Talep Oluştur", type="primary", key="des_talep_btn"):
        if not lokasyon.strip() or not aciklama.strip() or not talep_eden.strip():
            st.error("Lokasyon, talep eden ve aciklama zorunludur.")
            return

        sla_list = store.load_list("sla_ayarlar")
        now_str = datetime.now().isoformat()
        sla_targets = SLACalculator.calculate_sla_targets(sla_list, oncelik, now_str)

        ha_obj = alan_map_rev.get(sel_alan_kodu)
        ticket = Ticket(
            ticket_no=store.next_ticket_no(),
            hizmet_alani_kodu=sel_alan_kodu,
            alt_kategori_kodu=sel_alt_kodu,
            lokasyon=lokasyon.strip(),
            kademe=kademe,
            oncelik=oncelik,
            aciklama=aciklama.strip(),
            istenen_tarih_saat=istenen,
            talep_eden=talep_eden.strip(),
            atanan_kisi=atanan_kisi.strip(),
            sorumlu_rol=ha_obj.varsayilan_sorumlu_rol if ha_obj else "",
            sla_hedef_mudahale=sla_targets.get("sla_hedef_mudahale", ""),
            sla_hedef_cozum=sla_targets.get("sla_hedef_cozum", ""),
        )
        store.upsert("tickets", ticket)
        st.success(f"Talep oluşturuldu: {ticket.ticket_no}")
        st.rerun()


def _render_talep_listesi(store: DestekDataStore):
    styled_section("Talepler Listesi", "#1e40af")
    tickets_raw = store.load_list("tickets")
    if not tickets_raw:
        styled_info_banner("Henuz talep olusturulmamis.", "info")
        return

    alan_map = _alan_adi_map(store)
    alt_kat_map = {ak.alt_kategori_kodu: ak.alt_kategori_adi for ak in store.load_objects("alt_kategoriler")}

    # --- Filtreler ---
    c1, c2, c3 = st.columns(3)
    with c1:
        f_durum = st.selectbox("Durum Filtre", ["Tümü"] + TICKET_STATUSES, key="des_tl_durum")
    with c2:
        f_oncelik = st.selectbox("Öncelik Filtre", ["Tümü"] + TICKET_PRIORITIES, key="des_tl_oncelik")
    with c3:
        f_alan = st.selectbox("Hizmet Alani", ["Tümü"] + list(alan_map.values()), key="des_tl_alan")

    alan_kodu_rev = {v: k for k, v in alan_map.items()}
    filtered = tickets_raw
    if f_durum != "Tümü":
        filtered = [t for t in filtered if t.get("durum") == f_durum]
    if f_oncelik != "Tümü":
        filtered = [t for t in filtered if t.get("oncelik") == f_oncelik]
    if f_alan != "Tümü":
        ak = alan_kodu_rev.get(f_alan, "")
        filtered = [t for t in filtered if t.get("hizmet_alani_kodu") == ak]

    filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    if not filtered:
        styled_info_banner("Filtreye uygun talep bulunamadı.", "info")
        return

    styled_info_banner(f"Toplam {len(filtered)} talep listeleniyor. Tikla -> ac -> islem yap.", "info")

    # --- Tiklanabilir talep listesi ---
    for idx, t in enumerate(filtered):
        t_no = t.get("ticket_no", "")
        t_durum = t.get("durum", "")
        t_oncelik = t.get("oncelik", "")
        t_alan = alan_map.get(t.get("hizmet_alani_kodu", ""), t.get("hizmet_alani_kodu", ""))
        t_talep_eden = t.get("talep_eden", "") or "-"
        t_atanan = t.get("atanan_kisi", "") or "-"
        t_tarih = t.get("created_at", "")[:10]

        durum_icon = {"Açık": "\U0001f534", "Atandi": "\U0001f7e0", "Kabul Edildi": "\U0001f7e3",
                      "İşlemde": "\U0001f535", "Parca Bekleniyor": "\U0001f7e1",
                      "Tamamlandı": "\U0001f7e2", "Kontrol": "\U0001f50d", "Kapandi": "\u2b1c"}.get(t_durum, "\u2b1c")
        onc_icon = {"Kritik": "\U0001f525", "Yuksek": "\u26a0\ufe0f", "Normal": "\U0001f7e6", "Dusuk": "\u2b1c"}.get(t_oncelik, "")

        header = f"{durum_icon} **{t_no}** | {t_alan} | {onc_icon} {t_oncelik} | {t_durum} | Talep: {t_talep_eden} | Yapacak: {t_atanan} | {t_tarih}"

        with st.expander(header, expanded=False):
            _render_talep_inline(store, t, idx, alan_map, alt_kat_map)


def _render_talep_inline(store: DestekDataStore, t: dict, idx: int, alan_map: dict, alt_kat_map: dict):
    """Expander icinde tiklanarak acilan talep detay + islem ekrani."""
    t_id = t.get("id", "")
    ticket = store.get_by_id("tickets", t_id)
    if not ticket:
        st.error("Talep bulunamadı.")
        return

    # --- Bilgi karti ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"**No:** {ticket.ticket_no}")
        st.markdown(f"**Hizmet Alani:** {alan_map.get(ticket.hizmet_alani_kodu, ticket.hizmet_alani_kodu)}")
        st.markdown(f"**Alt Kategori:** {alt_kat_map.get(ticket.alt_kategori_kodu, ticket.alt_kategori_kodu)}")
        st.markdown(f"**Kademe:** {ticket.kademe}")
    with c2:
        p_color = _priority_color(ticket.oncelik)
        st.markdown(f'**Öncelik:** <span style="color:{p_color};font-weight:700;">{ticket.oncelik}</span>', unsafe_allow_html=True)
        st.markdown(f"**Durum:** {ticket.durum}")
        st.markdown(f"**Lokasyon:** {ticket.lokasyon}")
        st.markdown(f"**Tarih:** {ticket.created_at[:10]}")
        if ticket.istenen_tarih_saat:
            st.markdown(f"**Istenen:** {ticket.istenen_tarih_saat[:16]}")
    with c3:
        st.markdown(f"**Talep Eden:** {ticket.talep_eden or '-'}")
        st.markdown(f"**Yapacak Kisi:** {ticket.atanan_kisi or '-'}")
        sla_html = _sla_badge_html(ticket.to_dict())
        st.markdown(f"**SLA:** {sla_html}", unsafe_allow_html=True)

    st.markdown(f"**Açıklama:** {ticket.aciklama}")

    # --- Islem yapan kisi ---
    st.divider()
    styled_section("İşlem Yap", "#8b5cf6")

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        islem_adi = st.text_input("İşlemi Yapan Adi Soyadi *", key=f"des_tli_ad_{idx}")
    with ic2:
        islem_gorevi = st.text_input("Görevi", placeholder="Teknisyen, Temizlik Sorumlusu...", key=f"des_tli_gorev_{idx}")
    with ic3:
        islem_yapacak = st.text_input("Yapacak Kisi (guncelle)", value=ticket.atanan_kisi, key=f"des_tli_yapacak_{idx}")

    # --- Hizli durum butonlari ---
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        btn_bitti = st.button("\u2705 Bitirildi", key=f"des_tli_bitti_{idx}", use_container_width=True)
    with bc2:
        btn_devam = st.button("\U0001f504 Devam Ediyor", key=f"des_tli_devam_{idx}", use_container_width=True)
    with bc3:
        btn_sorun = st.button("\u26a0\ufe0f Sorun Var", key=f"des_tli_sorun_{idx}", use_container_width=True)
    with bc4:
        btn_kontrol = st.button("\U0001f50d Kontrole Gonder", key=f"des_tli_kontrol_{idx}", use_container_width=True)

    # --- Not alani ---
    not_text = st.text_area("Not / Açıklama", height=68, key=f"des_tli_not_{idx}",
                            placeholder="Yapilan islem, sorun detayi, bilgi notu...")

    # --- Islem kaydet ---
    hedef_durum = None
    if btn_bitti:
        hedef_durum = "Tamamlandı"
    elif btn_devam:
        hedef_durum = "İşlemde"
    elif btn_sorun:
        hedef_durum = "Parca Bekleniyor"
    elif btn_kontrol:
        hedef_durum = "Kontrol"

    if hedef_durum:
        if not islem_adi.strip():
            st.error("İşlemi yapan kisi adi zorunludur.")
            return

        ticket.durum = hedef_durum
        ticket.atanan_kisi = islem_yapacak.strip() if islem_yapacak.strip() else ticket.atanan_kisi
        ticket.updated_at = datetime.now().isoformat()
        if hedef_durum == "Tamamlandı":
            ticket.kapanis_tarihi = datetime.now().isoformat()

        not_kayit = f"[{hedef_durum}] {islem_adi.strip()}"
        if islem_gorevi.strip():
            not_kayit += f" ({islem_gorevi.strip()})"
        if not_text.strip():
            not_kayit += f" - {not_text.strip()}"

        ticket.notlar.append({
            "tarih": datetime.now().isoformat(),
            "yazan": islem_adi.strip(),
            "gorev": islem_gorevi.strip(),
            "not": not_kayit,
        })
        store.upsert("tickets", ticket)
        st.success(f"Talep {ticket.ticket_no} -> {hedef_durum} olarak güncellendi.")
        st.rerun()

    # --- Sadece not ekle butonu ---
    if st.button("Sadece Not Ekle", key=f"des_tli_notbtn_{idx}"):
        if not islem_adi.strip():
            st.error("Not ekleyen kisi adi zorunludur.")
            return
        if not not_text.strip():
            st.error("Not alani bos olamaz.")
            return
        not_kayit = f"{islem_adi.strip()}"
        if islem_gorevi.strip():
            not_kayit += f" ({islem_gorevi.strip()})"
        not_kayit += f" - {not_text.strip()}"
        ticket.notlar.append({
            "tarih": datetime.now().isoformat(),
            "yazan": islem_adi.strip(),
            "gorev": islem_gorevi.strip(),
            "not": not_kayit,
        })
        ticket.updated_at = datetime.now().isoformat()
        store.upsert("tickets", ticket)
        st.success("Not eklendi.")
        st.rerun()

    # --- Notlar gecmisi ---
    if ticket.notlar:
        st.divider()
        styled_section("Notlar Geçmişi", "#0d9488")
        for n in reversed(ticket.notlar):
            tarih = n.get("tarih", "")[:16].replace("T", " ")
            yazan = n.get("yazan", "")
            gorev = n.get("gorev", "")
            not_metni = n.get("not", "")
            yazan_str = f"**{yazan}**" if yazan else ""
            if gorev:
                yazan_str += f" _{gorev}_"
            st.markdown(f"{tarih} | {yazan_str}: {not_metni}")


def _render_talep_detay(store: DestekDataStore):
    styled_section("Talep Detay (Arama)", "#0d9488")
    tickets = store.load_objects("tickets")
    if not tickets:
        styled_info_banner("Henuz talep yok.", "info")
        return

    alan_map = _alan_adi_map(store)
    alt_kat_map = {ak.alt_kategori_kodu: ak.alt_kategori_adi for ak in store.load_objects("alt_kategoriler")}

    ticket_options = {f"{t.ticket_no} - {t.durum} - {t.talep_eden or ''}": t.id for t in tickets}
    sel = st.selectbox("Talep Sec / Ara", list(ticket_options.keys()), key="des_td_sel")
    sel_id = ticket_options.get(sel, "")
    ticket = store.get_by_id("tickets", sel_id)
    if not ticket:
        return

    # Inline detay olarak goster (ayni format)
    t_dict = ticket.to_dict()
    _render_talep_inline(store, t_dict, 9999, alan_map, alt_kat_map)


# ============================================================
# TAB 3: PERIYODIK ISLER
# ============================================================

def _render_periyodik_isler(store: DestekDataStore):
    sub = st.tabs(["📋 Görev Şablonları", "📅 Görev Planları"])

    with sub[0]:
        _render_gorev_sablonlari(store)
    with sub[1]:
        _render_gorev_planlari(store)


def _render_gorev_sablonlari(store: DestekDataStore):
    styled_section("Görev Şablonları", "#2563eb")
    sablonlar = store.load_objects("gorev_sablonlari")

    if sablonlar:
        rows = []
        for s in sablonlar:
            rows.append({
                "Sablon Adi": s.sablon_adi,
                "Alan": s.hizmet_alani_kodu,
                "Periyot": s.periyot,
                "Sorumlu": s.sorumlu_kisi_rol,
                "Madde Sayısı": len(s.checklist_maddeleri),
                "Aktif": "Evet" if s.aktif_mi else "Hayir",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    styled_section("Yeni Sablon Ekle", "#10b981")
    alan_map = _alan_adi_map(store)

    c1, c2 = st.columns(2)
    with c1:
        sablon_adi = st.text_input("Sablon Adi *", key="des_gs_adi")
        alan_sec = st.selectbox("Hizmet Alani", list(alan_map.values()), key="des_gs_alan")
    with c2:
        periyot = st.selectbox("Periyot", PERIYOT_TIPLERI, key="des_gs_periyot")
        sorumlu = st.text_input("Sorumlu Kisi/Rol", key="des_gs_sorumlu")

    madde_text = st.text_area("Checklist Maddeleri (her satir bir madde)", height=100, key="des_gs_maddeler")

    if st.button("Sablon Kaydet", type="primary", key="des_gs_btn"):
        if not sablon_adi.strip():
            st.error("Sablon adi zorunludur.")
            return
        alan_kodu_rev = {v: k for k, v in alan_map.items()}
        maddeler = [m.strip() for m in madde_text.split("\n") if m.strip()]
        sablon = GorevSablonu(
            sablon_adi=sablon_adi.strip(),
            hizmet_alani_kodu=alan_kodu_rev.get(alan_sec, ""),
            periyot=periyot,
            sorumlu_kisi_rol=sorumlu.strip(),
            checklist_maddeleri=maddeler,
        )
        store.upsert("gorev_sablonlari", sablon)
        st.success(f"Sablon kaydedildi: {sablon_adi}")
        st.rerun()


def _render_gorev_planlari(store: DestekDataStore):
    styled_section("Görev Planları", "#8b5cf6")

    c1, c2 = st.columns([2, 1])
    with c1:
        target = st.date_input("Tarih", value=date.today(), key="des_gp_tarih")
    with c2:
        if st.button("Görev Uret", type="primary", key="des_gp_btn"):
            count = PeriyodikGorevPlanner.generate_for_date(store, target)
            if count > 0:
                st.success(f"{count} gorev uretildi.")
            else:
                st.info("Uretilecek yeni gorev yok.")
            st.rerun()

    gorevler = store.load_objects("periyodik_gorevler")
    sab_map = {s.id: s.sablon_adi for s in store.load_objects("gorev_sablonlari")}

    date_gorevler = [g for g in gorevler if g.plan_tarihi == target.isoformat()]

    if date_gorevler:
        for g in date_gorevler:
            sablon_adi = sab_map.get(g.sablon_id, "Bilinmeyen")
            durum_icon = {"Bekliyor": "\u23f3", "Devam": "\U0001f504", "Tamamlandı": "\u2705"}.get(g.durum, "")
            with st.expander(f"{durum_icon} {sablon_adi} - {g.durum}"):
                if g.checklist_durum:
                    changed = False
                    for madde, done in g.checklist_durum.items():
                        new_val = st.checkbox(madde, value=done, key=f"des_gp_cl_{g.id}_{madde}")
                        if new_val != done:
                            g.checklist_durum[madde] = new_val
                            changed = True
                    if changed:
                        all_done = all(g.checklist_durum.values())
                        if all_done:
                            g.durum = "Tamamlandı"
                            g.yapildi_tarihi = datetime.now().isoformat()
                        elif any(g.checklist_durum.values()):
                            g.durum = "Devam"
                        store.upsert("periyodik_gorevler", g)
                else:
                    st.info("Checklist maddesi yok.")

                if g.durum != "Tamamlandı":
                    if st.button("Tamamla", key=f"des_gp_done_{g.id}"):
                        g.durum = "Tamamlandı"
                        g.yapildi_tarihi = datetime.now().isoformat()
                        for k in g.checklist_durum:
                            g.checklist_durum[k] = True
                        store.upsert("periyodik_gorevler", g)
                        st.rerun()
    else:
        styled_info_banner("Bu tarih için gorev bulunamadı.", "info")


# ============================================================
# TAB 4: DENETIMLER
# ============================================================

def _render_denetimler(store: DestekDataStore):
    formlar = store.load_objects("denetim_formlari")
    if not formlar:
        styled_info_banner("Denetim formu tanımlanmamış.", "warning")
        return

    form_tabs = st.tabs([f.form_adi for f in formlar])
    for i, form in enumerate(formlar):
        with form_tabs[i]:
            _render_denetim_formu(store, form)


def _render_denetim_formu(store: DestekDataStore, form: DenetimFormu):
    denetimler = store.find_by_field("denetimler", "form_kodu", form.form_kodu)

    # Denetim Listesi
    styled_section(f"Denetimler - {form.form_kodu}", "#1e40af")
    if denetimler:
        rows = []
        for d in denetimler:
            rows.append({
                "No": d.denetim_no,
                "Donem": f"{d.donem_ay}/{d.donem_yil}",
                "Skor": f"{d.yuzde_skor:.0f}%",
                "Sonuc": d.genel_sonuc,
                "Durum": d.durum,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Yeni Denetim
    st.divider()
    styled_section("Yeni Denetim", "#10b981")
    c1, c2, c3 = st.columns(3)
    with c1:
        donem_ay = st.number_input("Donem Ay", min_value=1, max_value=12, value=date.today().month, key=f"des_den_ay_{form.form_kodu}")
    with c2:
        donem_yil = st.number_input("Donem Yil", min_value=2024, max_value=2030, value=date.today().year, key=f"des_den_yil_{form.form_kodu}")
    with c3:
        kampus = st.text_input("Kampus/Lokasyon", key=f"des_den_kamp_{form.form_kodu}")

    denetci = st.text_input("Denetci Adi", key=f"des_den_denetci_{form.form_kodu}")

    if st.button("Denetim Oluştur", type="primary", key=f"des_den_btn_{form.form_kodu}"):
        den = Denetim(
            denetim_no=store.next_denetim_no(form.form_kodu),
            form_kodu=form.form_kodu,
            donem_ay=int(donem_ay),
            donem_yil=int(donem_yil),
            kampus_lokasyon=kampus.strip(),
            denetci_adi=denetci.strip(),
        )
        store.upsert("denetimler", den)
        st.success(f"Denetim oluşturuldu: {den.denetim_no}")
        st.rerun()

    # Puanlama
    if denetimler:
        st.divider()
        styled_section("Puanlama", "#8b5cf6")
        _PUAN_ACIKLAMA = {1: "Olumsuz", 2: "Orta", 3: "Iyi"}
        _PUAN_RENK = {1: "#ef4444", 2: "#f59e0b", 3: "#10b981"}
        st.markdown("""<div style="display:flex;gap:16px;margin-bottom:12px;padding:10px 16px;
        background:linear-gradient(135deg,#111827,#0B0F19);border-radius:10px;border:1px solid #e2e8f0">
        <span style="font-weight:700;color:#94A3B8">Puanlama Olcegi:</span>
        <span style="color:#ef4444;font-weight:600">1 = Olumsuz</span>
        <span style="color:#f59e0b;font-weight:600">2 = Orta</span>
        <span style="color:#10b981;font-weight:600">3 = Iyi</span>
        </div>""", unsafe_allow_html=True)

        den_options = {d.denetim_no: d.id for d in denetimler if d.durum in ("Taslak", "Dolduruldu")}
        if den_options:
            sel_den_no = st.selectbox("Denetim Sec", list(den_options.keys()), key=f"des_den_sel_{form.form_kodu}")
            sel_den = store.get_by_id("denetimler", den_options[sel_den_no])
            if sel_den:
                maddeler = [m for m in store.load_objects("denetim_maddeleri")
                            if m.form_kodu == form.form_kodu and m.aktif_mi]
                maddeler.sort(key=lambda m: (m.bolum_no, m.madde_no))

                current_bolum = ""
                for m in maddeler:
                    if m.bolum_adi != current_bolum:
                        current_bolum = m.bolum_adi
                        st.markdown(f"""<div style="background:linear-gradient(135deg,#1e40af,#2563eb);
                        color:#fff;padding:8px 14px;border-radius:8px;margin:16px 0 8px 0;
                        font-weight:700;font-size:0.95rem">{m.bolum_no}. {m.bolum_adi}</div>""",
                                    unsafe_allow_html=True)

                    kritik_badge = (' <span style="background:#ef4444;color:#fff;padding:1px 8px;'
                                    'border-radius:6px;font-size:0.7rem;font-weight:700">KRITIK</span>') if m.kritik_mi else ""

                    current_val = sel_den.puanlar.get(m.id, 1)
                    try:
                        current_val = int(current_val)
                        if current_val not in (1, 2, 3):
                            current_val = 1
                    except (ValueError, TypeError):
                        current_val = 1

                    st.markdown(f"""<div style="padding:4px 0;font-size:0.88rem">
                    <b>{m.madde_no}.</b> {m.madde_metni}{kritik_badge}</div>""", unsafe_allow_html=True)

                    puan = st.radio(
                        f"Puan - Madde {m.madde_no}",
                        options=[1, 2, 3],
                        index=current_val - 1,
                        format_func=lambda x: f"{x} - {_PUAN_ACIKLAMA[x]}",
                        horizontal=True,
                        key=f"des_den_p_{form.form_kodu}_{m.id}",
                        label_visibility="collapsed",
                    )
                    sel_den.puanlar[m.id] = puan

                    # Puan gosterge cubuğu
                    renk = _PUAN_RENK[puan]
                    genislik = puan / 3 * 100
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
                    <div style="flex:1;background:#e2e8f0;border-radius:4px;height:8px;overflow:hidden">
                    <div style="width:{genislik:.0f}%;height:100%;background:{renk};border-radius:4px;
                    transition:width 0.3s"></div></div>
                    <span style="font-size:0.78rem;font-weight:700;color:{renk}">{_PUAN_ACIKLAMA[puan]}</span>
                    </div>""", unsafe_allow_html=True)

                # Toplam ozet
                toplam_puan = sum(sel_den.puanlar.get(m.id, 1) for m in maddeler)
                max_puan = len(maddeler) * 3
                yuzde = round(toplam_puan / max_puan * 100, 0) if max_puan > 0 else 0
                st.divider()
                styled_stat_row([
                    ("Toplam Puan", f"{toplam_puan}/{max_puan}", "#2563eb", "\U0001f4ca"),
                    ("Yuzde", f"%{yuzde:.0f}", "#8b5cf6", "\U0001f4af"),
                    ("Olumsuz", sum(1 for m in maddeler if sel_den.puanlar.get(m.id, 1) == 1), "#ef4444", "\U0001f534"),
                    ("Iyi", sum(1 for m in maddeler if sel_den.puanlar.get(m.id, 1) == 3), "#10b981", "\U0001f7e2"),
                ])

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Puanlari Kaydet ve Hesapla", type="primary", key=f"des_den_calc_{form.form_kodu}"):
                        ayarlar = store.load_list("destek_ayarlar")
                        sel_den = DenetimScorer.calculate_score(sel_den, maddeler, ayarlar)
                        sel_den.durum = "Dolduruldu"
                        store.upsert("denetimler", sel_den)
                        st.success(f"Skor: {sel_den.yuzde_skor:.0f}% - {sel_den.genel_sonuc}")
                        st.rerun()
                with c2:
                    if sel_den.durum == "Dolduruldu":
                        if st.button("Onaya Gonder", key=f"des_den_onay_{form.form_kodu}"):
                            sel_den.durum = "Onaya Gonderildi"
                            store.upsert("denetimler", sel_den)
                            st.success("Onaya gonderildi.")
                            st.rerun()

        # Onay bekleyenler
        onay_list = [d for d in denetimler if d.durum == "Onaya Gonderildi"]
        if onay_list:
            st.divider()
            styled_section("Onay Bekleyenler", "#f59e0b")
            for d in onay_list:
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"**{d.denetim_no}** - Skor: {d.yuzde_skor:.0f}% ({d.genel_sonuc})")
                with c2:
                    if st.button("Onayla", key=f"des_den_approve_{d.id}"):
                        d.durum = "Onaylandi"
                        store.upsert("denetimler", d)
                        st.rerun()
                with c3:
                    if st.button("Arsivle", key=f"des_den_arsiv_{d.id}"):
                        d.durum = "Arsiv"
                        store.upsert("denetimler", d)
                        st.rerun()

    # PDF Export
    onaylanan = [d for d in denetimler if d.durum in ("Onaylandi", "Arsiv")]
    if onaylanan:
        st.divider()
        styled_section("PDF Rapor", "#0d9488")
        den_pdf_sel = st.selectbox("Rapor için Denetim Sec",
                                    [d.denetim_no for d in onaylanan],
                                    key=f"des_den_pdf_{form.form_kodu}")
        den_pdf = next((d for d in onaylanan if d.denetim_no == den_pdf_sel), None)
        if den_pdf and st.button("PDF Oluştur", key=f"des_den_pdfbtn_{form.form_kodu}"):
            pdf = _generate_denetim_pdf(store, den_pdf)
            if pdf:
                st.download_button("PDF İndir", data=pdf,
                                   file_name=f"Denetim_{den_pdf.denetim_no}.pdf",
                                   mime="application/pdf",
                                   key=f"des_den_dl_{form.form_kodu}")


def _generate_denetim_pdf(store: DestekDataStore, den: Denetim) -> bytes | None:
    try:
        info = get_institution_info()
        form = store.get_by_field("denetim_formlari", "form_kodu", den.form_kodu)
        form_adi = form.form_adi if form else den.form_kodu

        gen = ReportPDFGenerator(f"Denetim Raporu - {form_adi}",
                                 f"Dönem: {den.donem_ay}/{den.donem_yil}")
        gen.add_header(kurum_adi=info.get("name", ""))
        gen.add_section("Denetim Bilgileri")
        gen.add_text(f"Denetim No: {den.denetim_no}")
        gen.add_text(f"Kampüs: {den.kampus_lokasyon}")
        gen.add_text(f"Denetçi: {den.denetci_adi}")
        gen.add_text(f"Genel Sonuç: {den.genel_sonuc} ({den.yuzde_skor:.0f}/100)")

        maddeler = [m for m in store.load_objects("denetim_maddeleri")
                    if m.form_kodu == den.form_kodu and m.aktif_mi]
        maddeler.sort(key=lambda m: (m.bolum_no, m.madde_no))

        bolum_scores: dict[str, list] = {}
        for m in maddeler:
            if m.bolum_adi not in bolum_scores:
                bolum_scores[m.bolum_adi] = []
            puan = den.puanlar.get(m.id, 0)
            bolum_scores[m.bolum_adi].append(float(puan))

        chart_data = {}
        for bolum, puanlar in bolum_scores.items():
            total = sum(puanlar)
            max_p = len(puanlar) * 2
            chart_data[bolum] = round(total / max_p * 100 if max_p > 0 else 0, 0)

        gen.add_section("Bölüm Skorları")
        gen.add_bar_chart(chart_data, "Bölüm Bazlı Skor (%)", "#4472C4")

        return gen.generate()
    except Exception:
        return None


# ============================================================
# TAB 5: PERIYODIK BAKIM (PBK)
# ============================================================

def _render_pbk(store: DestekDataStore):
    sub = st.tabs(["📊 Bakım Durumu", "📦 Bakım Envanteri", "📅 Bakım Planı", "📝 Bakım Kayıt"])

    with sub[0]:
        _render_bakim_durumu(store)
    with sub[1]:
        _render_bakim_envanter(store)
    with sub[2]:
        _render_bakim_plani(store)
    with sub[3]:
        _render_bakim_kayit(store)


# ---------- BAKIM DURUMU (Dashboard) ----------

def _render_bakim_durumu(store: DestekDataStore):
    styled_section("Bakım Durum Paneli", "#2563eb")
    today = date.today()
    today_str = today.isoformat()
    yaklasan_sinir = (today + timedelta(days=5)).isoformat()

    kayitlar_raw = store.load_list("bakim_kayitlari")
    kalem_map = {k.kalem_kodu: k for k in store.load_objects("bakim_kalemleri")}

    bekleyen = [k for k in kayitlar_raw if k.get("durum") in ("Planlandi", "Devam")]
    geciken = [k for k in bekleyen if k.get("plan_tarihi", "") < today_str]
    bugunun = [k for k in bekleyen if k.get("plan_tarihi", "") == today_str]
    yaklasan = [k for k in bekleyen if today_str < k.get("plan_tarihi", "") <= yaklasan_sinir]
    tamamlanan = [k for k in kayitlar_raw if k.get("durum") == "Tamamlandı"]
    toplam = len(kayitlar_raw)

    styled_stat_row([
        ("Geciken", len(geciken), "#ef4444", "\U0001f6a8"),
        ("Bugün", len(bugunun), "#f59e0b", "\U0001f4c5"),
        ("Yaklasan (5 gun)", len(yaklasan), "#2563eb", "\u23f3"),
        ("Tamamlanan", len(tamamlanan), "#10b981", "\u2705"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    def _bakim_tablo(title, items, color, icon):
        styled_section(f"{icon} {title} ({len(items)})", color)
        if not items:
            styled_info_banner(f"{title} bulunmuyor.", "success")
            return
        rows = []
        for k in sorted(items, key=lambda x: x.get("plan_tarihi", "")):
            kalem = kalem_map.get(k.get("kalem_kodu", ""))
            rows.append({
                "Kalem Kodu": k.get("kalem_kodu", ""),
                "Kalem Adi": kalem.kalem_adi if kalem else "",
                "Kategori": kalem.kategori if kalem else "",
                "Periyot": kalem.periyot if kalem else "",
                "Plan Tarihi": k.get("plan_tarihi", ""),
                "Sorumlu": k.get("bakim_sorumlusu", ""),
                "Firma": k.get("firma_adi", ""),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    _bakim_tablo("Geciken Bakımlar", geciken, "#ef4444", "\U0001f6a8")
    _bakim_tablo("Bugünkü Bakımlar", bugunun, "#f59e0b", "\U0001f4c5")
    _bakim_tablo("Yaklaşan Bakımlar (5 Gün İçinde)", yaklasan, "#2563eb", "\u23f3")

    # Grafik: Sunburst (Kategori/Periyot) + Bar + Donut (Excel stili)
    st.divider()
    styled_section("Bakım Özet Grafikleri", "#0d9488")

    # Kategori bazli sunburst: ic halka=kategori, dis halka=periyot
    kat_counts: dict[str, float] = {}
    kat_sub: dict[str, list[tuple[str, float]]] = {}
    for k in kayitlar_raw:
        kalem = kalem_map.get(k.get("kalem_kodu", ""))
        kat = kalem.kategori if kalem else "Diğer"
        per = kalem.periyot if kalem else "Diğer"
        kat_counts[kat] = kat_counts.get(kat, 0) + 1
        kat_sub.setdefault(kat, {})
        kat_sub[kat][per] = kat_sub[kat].get(per, 0) + 1
    kat_sub_list = {k: [(p, c) for p, c in v.items()] for k, v in kat_sub.items()}

    c1, c2 = st.columns(2)
    with c1:
        if kat_counts:
            st.markdown(
                ReportStyler.sunburst_chart_svg(kat_counts, kat_sub_list, size=300,
                                                 title="Kategori / Periyot Dagilimi"),
                unsafe_allow_html=True)
    with c2:
        durum_data = {
            "Planlanan": len(bekleyen) - len(geciken),
            "Tamamlanan": len(tamamlanan),
            "Geciken": len(geciken),
        }
        st.markdown(ReportStyler.donut_chart_svg(durum_data,
                    colors=["#4472C4", "#10b981", "#ED7D31"], size=155), unsafe_allow_html=True)
        if kat_counts:
            st.markdown(ReportStyler.horizontal_bar_html(kat_counts, "#4472C4", max_width_px=300), unsafe_allow_html=True)

    # PDF Rapor
    st.divider()
    if st.button("Bakım Durum PDF Rapor", type="primary", key="des_pbk_dash_pdf"):
        pdf = _generate_bakim_durum_pdf(store, geciken, bugunun, yaklasan, tamamlanan, kalem_map, toplam)
        if pdf:
            st.download_button("PDF İndir", data=pdf, file_name=f"PBK_Durum_Rapor_{today}.pdf",
                               mime="application/pdf", key="des_pbk_dash_dl")


def _generate_bakim_durum_pdf(store, geciken, bugunun, yaklasan, tamamlanan, kalem_map, toplam):
    try:
        info = get_institution_info()
        gen = ReportPDFGenerator("Periyodik Bakım (PBK) Durum Raporu",
                                  f"Rapor Tarihi: {date.today().strftime('%d.%m.%Y')}")
        gen.add_header(kurum_adi=info.get("name", ""))

        gen.add_section("Temel Göstergeler")
        gen.add_metrics([
            ("Geciken", len(geciken), "#ef4444"),
            ("Bugün", len(bugunun), "#f59e0b"),
            ("Yaklaşan", len(yaklasan), "#2563eb"),
            ("Tamamlanan", len(tamamlanan), "#10b981"),
        ])
        gen.add_spacer(0.4)

        # Durum grafiği
        durum_data = {"Planlanan": toplam - len(tamamlanan) - len(geciken),
                      "Tamamlanan": len(tamamlanan), "Geciken": len(geciken)}
        gen.add_section("Bakım Durum Dağılımı")
        gen.add_donut_chart(durum_data, "Planlanan / Yapılan / Geciken", ["#4472C4", "#10b981", "#ED7D31"])

        # Geciken tablo
        if geciken:
            gen.add_section("Geciken Bakımlar")
            rows = []
            for k in geciken:
                kalem = kalem_map.get(k.get("kalem_kodu", ""))
                rows.append({"Kod": k.get("kalem_kodu", ""), "Kalem": kalem.kalem_adi if kalem else "",
                             "Plan Tarihi": k.get("plan_tarihi", ""), "Sorumlu": k.get("bakim_sorumlusu", "")})
            gen.add_table(pd.DataFrame(rows))

        # Yaklasan tablo
        if yaklasan:
            gen.add_section("Yaklaşan Bakımlar (5 Gün)")
            rows = []
            for k in yaklasan:
                kalem = kalem_map.get(k.get("kalem_kodu", ""))
                rows.append({"Kod": k.get("kalem_kodu", ""), "Kalem": kalem.kalem_adi if kalem else "",
                             "Plan Tarihi": k.get("plan_tarihi", ""), "Sorumlu": k.get("bakim_sorumlusu", "")})
            gen.add_table(pd.DataFrame(rows))

        return gen.generate()
    except Exception:
        return None


# ---------- BAKIM ENVANTERI ----------

def _render_bakim_envanter(store: DestekDataStore):
    styled_section("Periyodik Bakım Envanteri (PBK)", "#2563eb")
    kalemler = store.load_objects("bakim_kalemleri")

    if kalemler:
        kategoriler = sorted(set(k.kategori for k in kalemler))
        for kat in kategoriler:
            with st.expander(f"{kat} ({sum(1 for k in kalemler if k.kategori == kat and k.aktif_mi)} aktif)"):
                kat_kalemler = [k for k in kalemler if k.kategori == kat]
                rows = []
                for k in kat_kalemler:
                    rows.append({
                        "Kod": k.kalem_kodu,
                        "Kalem": k.kalem_adi,
                        "Periyot": k.periyot,
                        "İlk Bakım": k.ilk_bakim_tarihi or "-",
                        "Sorumlu": k.bakim_sorumlusu or "-",
                        "Yürütucu": k.varsayilan_yurutucu_tipi,
                        "Kanit": "Evet" if k.kanit_zorunlu_mu else "Hayir",
                        "Aktif": "Evet" if k.aktif_mi else "Hayir",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner("Bakım kalemi tanımlanmamış.", "warning")

    # --- Yeni Bakım Kalemi Ekle ---
    st.divider()
    styled_section("Yeni Bakım Kalemi Ekle", "#10b981")

    mevcut_kodlar = {k.kalem_kodu for k in kalemler} if kalemler else set()
    mevcut_kategoriler = sorted(set(k.kategori for k in kalemler)) if kalemler else []

    c1, c2 = st.columns(2)
    with c1:
        yeni_kod = st.text_input("Kalem Kodu *", placeholder="PBK-026", key="des_pbk_yeni_kod")
        yeni_adi = st.text_input("Kalem Adi *", placeholder="Ornek: Jenerator bakim", key="des_pbk_yeni_adi")
        if mevcut_kategoriler:
            kat_sec = st.selectbox("Kategori (mevcut)", ["-- Yeni Kategori --"] + mevcut_kategoriler, key="des_pbk_yeni_kat_sec")
        else:
            kat_sec = "-- Yeni Kategori --"
        if kat_sec == "-- Yeni Kategori --":
            yeni_kategori = st.text_input("Yeni Kategori Adi *", placeholder="Ornek: Jenerator", key="des_pbk_yeni_kat")
        else:
            yeni_kategori = kat_sec
        yeni_sorumlu = st.text_input("Bakım Sorumlusu", placeholder="Okul bakım sorumlusu", key="des_pbk_yeni_sorumlu")
    with c2:
        yeni_periyot = st.selectbox("Periyot", PERIYOT_TIPLERI, index=2, key="des_pbk_yeni_periyot")
        yeni_ilk_tarih = st.date_input("İlk Bakım Tarihi *", value=date.today(), key="des_pbk_yeni_ilk")
        yeni_yurutucu = st.selectbox("Yürütucu Tipi", YURUTUCU_TIPLERI, key="des_pbk_yeni_yur")
        yeni_kanit = st.checkbox("Kanit Eki Zorunlu", key="des_pbk_yeni_kanit")
        yeni_aktif = st.checkbox("Aktif", value=True, key="des_pbk_yeni_aktif")

    if st.button("Bakım Kalemi Ekle", type="primary", key="des_pbk_yeni_btn"):
        if not yeni_kod.strip() or not yeni_adi.strip() or not yeni_kategori.strip():
            st.error("Kalem kodu, adi ve kategori zorunludur.")
        elif yeni_kod.strip().upper() in mevcut_kodlar:
            st.error(f"'{yeni_kod.strip().upper()}' kodu zaten mevcut.")
        else:
            kalem = BakimKalemi(
                kalem_kodu=yeni_kod.strip().upper(),
                kalem_adi=yeni_adi.strip(),
                kategori=yeni_kategori.strip(),
                periyot=yeni_periyot,
                ilk_bakim_tarihi=yeni_ilk_tarih.isoformat() if yeni_ilk_tarih else "",
                varsayilan_yurutucu_tipi=yeni_yurutucu,
                bakim_sorumlusu=yeni_sorumlu.strip(),
                kanit_zorunlu_mu=yeni_kanit,
                aktif_mi=yeni_aktif,
            )
            store.upsert("bakim_kalemleri", kalem)
            st.success(f"Bakım kalemi eklendi: {kalem.kalem_kodu} - {kalem.kalem_adi}")
            st.rerun()


# ---------- BAKIM PLANI ----------

def _render_bakim_plani(store: DestekDataStore):
    styled_section("Bakım Planı Oluştur", "#10b981")

    styled_info_banner("Kalem envanterindeki 'İlk Bakım Tarihi' ve 'Periyot' bilgilerine gore otomatik plan uretir.", "info")

    plan_sec = st.radio("Plan Uretme Yontemi", ["Otomatik (İlk tarihten itibaren)", "Aylık (Klasik)"],
                        horizontal=True, key="des_pbk_plan_yontem")

    if plan_sec == "Otomatik (İlk tarihten itibaren)":
        c1, c2 = st.columns(2)
        with c1:
            bitis = st.date_input("Plan Bitis Tarihi", value=date(date.today().year, 12, 31), key="des_pbk_plan_bitis")
        with c2:
            if st.button("Otomatik Plan Uret", type="primary", key="des_pbk_plan_oto_btn"):
                count = BakimPlanner.generate_all_from_start(store, bitis.isoformat())
                if count > 0:
                    st.success(f"{count} bakım kaydı oluşturuldu.")
                else:
                    st.info("Uretilecek yeni kayıt yok. Kalemler zaten planli veya 'İlk Bakım Tarihi' girilmemiş.")
                st.rerun()
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            ay = st.number_input("Ay", min_value=1, max_value=12, value=date.today().month, key="des_pbk_ay")
        with c2:
            yil = st.number_input("Yil", min_value=2024, max_value=2030, value=date.today().year, key="des_pbk_yil")
        with c3:
            if st.button("Aylık Plan Uret", type="primary", key="des_pbk_btn"):
                count = BakimPlanner.generate_monthly(store, int(yil), int(ay))
                if count > 0:
                    st.success(f"{count} bakım kaydı oluşturuldu.")
                else:
                    st.info("Bu donem için tum kayitlar zaten mevcut.")
                st.rerun()

    # Mevcut kayitlari goster
    st.divider()
    styled_section("Planlanan Bakımlar", "#2563eb")
    kayitlar = store.load_list("bakim_kayitlari")
    kalem_map = {k.kalem_kodu: k for k in store.load_objects("bakim_kalemleri")}

    if kayitlar:
        rows = []
        for k in sorted(kayitlar, key=lambda x: x.get("plan_tarihi", "")):
            kalem = kalem_map.get(k.get("kalem_kodu", ""))
            rows.append({
                "Kalem Kodu": k.get("kalem_kodu", ""),
                "Kalem Adi": kalem.kalem_adi if kalem else "",
                "Periyot": kalem.periyot if kalem else "",
                "Plan Tarihi": k.get("plan_tarihi", ""),
                "Durum": k.get("durum", ""),
                "Sonuc": k.get("sonuc", "-"),
                "Sorumlu": k.get("bakim_sorumlusu", ""),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        tamamlanan = sum(1 for k in kayitlar if k.get("durum") == "Tamamlandı")
        toplam = len(kayitlar)
        geciken = sum(1 for k in kayitlar if k.get("durum") in ("Planlandi", "Devam") and k.get("plan_tarihi", "") < date.today().isoformat())
        styled_stat_row([
            ("Toplam", toplam, "#2563eb", "\U0001f4cb"),
            ("Tamamlanan", tamamlanan, "#10b981", "\u2705"),
            ("Geciken", geciken, "#ef4444", "\U0001f6a8"),
            ("Uyum", f"%{round(tamamlanan / toplam * 100) if toplam else 0}", "#0d9488", "\U0001f4ca"),
        ])
    else:
        styled_info_banner("Henuz bakim plani olusturulmamis.", "info")


# ---------- BAKIM KAYIT ----------

def _render_bakim_kayit(store: DestekDataStore):
    styled_section("Bakım Kayıt İşlemleri", "#8b5cf6")
    kayitlar = store.load_objects("bakim_kayitlari")
    bekleyen = [k for k in kayitlar if k.durum in ("Planlandi", "Devam")]

    if not bekleyen:
        styled_info_banner("Güncellenmesi gereken bakım kaydı yok.", "success")
        return

    kalem_map = {k.kalem_kodu: k for k in store.load_objects("bakim_kalemleri")}

    # Siralama: geciken ilk, sonra yakin tarih
    today_str = date.today().isoformat()
    bekleyen.sort(key=lambda k: (0 if k.plan_tarihi < today_str else 1, k.plan_tarihi))

    styled_info_banner(f"{len(bekleyen)} bekleyen bakım kaydı var. Tikla -> islem yap.", "info")

    for idx, kayit in enumerate(bekleyen):
        kalem = kalem_map.get(kayit.kalem_kodu)
        kalem_adi = kalem.kalem_adi if kalem else kayit.kalem_kodu
        kat = kalem.kategori if kalem else ""

        gecikme = kayit.plan_tarihi < today_str
        icon = "\U0001f6a8" if gecikme else ("\U0001f4c5" if kayit.plan_tarihi == today_str else "\u23f3")
        gecikme_label = " **GECIKEN**" if gecikme else (" **BUGUN**" if kayit.plan_tarihi == today_str else "")

        header = f"{icon} {kayit.kalem_kodu} - {kalem_adi} | {kayit.plan_tarihi} | {kat}{gecikme_label}"

        with st.expander(header, expanded=gecikme):
            # Bilgi karti
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                st.markdown(f"**Kalem:** {kalem_adi}")
                st.markdown(f"**Kategori:** {kat}")
                st.markdown(f"**Periyot:** {kalem.periyot if kalem else '-'}")
            with ic2:
                st.markdown(f"**Plan Tarihi:** {kayit.plan_tarihi}")
                st.markdown(f"**Durum:** {kayit.durum}")
                st.markdown(f"**Yürütucu:** {kayit.yurutucu_tipi}")
            with ic3:
                st.markdown(f"**Sorumlu:** {kayit.bakim_sorumlusu or '-'}")
                st.markdown(f"**Görevli:** {kayit.gorevli_adi or '-'}")
                st.markdown(f"**Firma:** {kayit.firma_adi or '-'}")

            st.divider()

            # Islem formu
            fc1, fc2 = st.columns(2)
            with fc1:
                bk_sorumlu = st.text_input("Okul Bakım Sorumlusu *", value=kayit.bakim_sorumlusu,
                                            key=f"des_bk_sorm_{idx}")
                bk_firma = st.text_input("Bakımı Yapan Firma", value=kayit.firma_adi,
                                          key=f"des_bk_firma_{idx}")
                bk_yetkili = st.text_input("Firma Yetkili Kisi", value=kayit.firma_yetkili,
                                            key=f"des_bk_yetk_{idx}")
            with fc2:
                bk_gorevli = st.text_input("Bakımı Yapan Görevli", value=kayit.gorevli_adi,
                                            key=f"des_bk_gorv_{idx}")
                bk_sonuc = st.selectbox("Sonuc *", BAKIM_SONUC_SECENEKLERI, key=f"des_bk_sonuc_{idx}")
                bk_detay = st.text_input("Sonuc Detay", placeholder="Ek aciklama...",
                                          key=f"des_bk_detay_{idx}")

            bk_not = st.text_area("Not / Açıklama", height=68, placeholder="Yapilan islem detayi, bulunan sorunlar...",
                                   key=f"des_bk_not_{idx}")

            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("Kaydet", type="primary", key=f"des_bk_save_{idx}", use_container_width=True):
                    if not bk_sorumlu.strip():
                        st.error("Bakım sorumlusu zorunludur.")
                    else:
                        kayit.bakim_sorumlusu = bk_sorumlu.strip()
                        kayit.firma_adi = bk_firma.strip()
                        kayit.firma_yetkili = bk_yetkili.strip()
                        kayit.gorevli_adi = bk_gorevli.strip()
                        kayit.sonuc = bk_sonuc
                        kayit.sonuc_detay = bk_detay.strip()
                        kayit.durum = "Tamamlandı"
                        kayit.yapildi_tarihi = datetime.now().isoformat()
                        kayit.updated_at = datetime.now().isoformat()

                        # Not ekle
                        not_kayit = f"[{bk_sonuc}] {bk_sorumlu.strip()}"
                        if bk_firma.strip():
                            not_kayit += f" / Firma: {bk_firma.strip()}"
                        if bk_not.strip():
                            not_kayit += f" - {bk_not.strip()}"
                        if not isinstance(kayit.notlar, list):
                            kayit.notlar = []
                        kayit.notlar.append({
                            "tarih": datetime.now().isoformat(),
                            "yazan": bk_sorumlu.strip(),
                            "not": not_kayit,
                        })

                        # Yeni ariza -> ticket
                        if bk_sonuc == "Yeni Ariza Bulundu":
                            kalem_adi_t = kalem.kalem_adi if kalem else kayit.kalem_kodu
                            ticket = Ticket(
                                ticket_no=store.next_ticket_no(),
                                hizmet_alani_kodu="TEK",
                                aciklama=f"PBK Ariza: {kalem_adi_t} - {kayit.plan_tarihi}. {bk_detay.strip()}",
                                oncelik="Yuksek",
                                lokasyon="PBK",
                                talep_eden=bk_sorumlu.strip(),
                            )
                            store.upsert("tickets", ticket)
                            kayit.ticket_id = ticket.id
                            st.warning(f"Ariza talebi oluşturuldu: {ticket.ticket_no}")

                        store.upsert("bakim_kayitlari", kayit)
                        st.success(f"Bakım kaydı güncellendi: {kayit.kalem_kodu}")
                        st.rerun()

            with bc2:
                if st.button("Sadece Not Ekle", key=f"des_bk_notonly_{idx}", use_container_width=True):
                    if not bk_sorumlu.strip() or not bk_not.strip():
                        st.error("Sorumlu ve not alani zorunludur.")
                    else:
                        if not isinstance(kayit.notlar, list):
                            kayit.notlar = []
                        kayit.notlar.append({
                            "tarih": datetime.now().isoformat(),
                            "yazan": bk_sorumlu.strip(),
                            "not": bk_not.strip(),
                        })
                        kayit.updated_at = datetime.now().isoformat()
                        store.upsert("bakim_kayitlari", kayit)
                        st.success("Not eklendi.")
                        st.rerun()

            # Notlar gecmisi
            if isinstance(kayit.notlar, list) and kayit.notlar:
                st.divider()
                styled_section("Notlar Geçmişi", "#0d9488")
                for n in reversed(kayit.notlar):
                    tarih = n.get("tarih", "")[:16].replace("T", " ") if isinstance(n, dict) else ""
                    yazan = n.get("yazan", "") if isinstance(n, dict) else ""
                    not_m = n.get("not", "") if isinstance(n, dict) else str(n)
                    st.markdown(f"{tarih} | **{yazan}**: {not_m}")


# ============================================================
# TAB 6: FIRMA HAVUZU
# ============================================================

def _render_firma_havuzu(store: DestekDataStore):
    styled_section("Firma Havuzu", "#7c3aed")

    firmalar = store.load_objects("firma_havuzu")

    # --- Sektor Dagilimi Grafigi (Sunburst + Bar, Excel stili) ---
    if firmalar:
        aktif_firmalar = [f for f in firmalar if f.aktif_mi]
        sektor_cnt: dict[str, float] = {}
        sektor_puan: dict[str, list[tuple[str, float]]] = {}
        for f in aktif_firmalar:
            sek = f.sektor or "Diğer"
            sektor_cnt[sek] = sektor_cnt.get(sek, 0) + 1
            # Dis halka: firma adlari
            sektor_puan.setdefault(sek, [])
            sektor_puan[sek].append((f.firma_adi, 1))

        styled_stat_row([
            ("Toplam Firma", len(firmalar), "#7c3aed", "\U0001f3e2"),
            ("Aktif", len(aktif_firmalar), "#10b981", "\U0001f7e2"),
            ("Pasif", len(firmalar) - len(aktif_firmalar), "#ef4444", "\U0001f534"),
            ("Sektor Sayısı", len(sektor_cnt), "#4472C4", "\U0001f4ca"),
        ])

        if sektor_cnt:
            gc1, gc2 = st.columns(2)
            with gc1:
                st.markdown(
                    ReportStyler.sunburst_chart_svg(sektor_cnt, sektor_puan, size=320,
                                                     title="Sektor / Firma Dagilimi"),
                    unsafe_allow_html=True)
            with gc2:
                st.markdown(ReportStyler.horizontal_bar_html(
                    dict(sorted(sektor_cnt.items(), key=lambda x: x[1], reverse=True)),
                    "#4472C4", max_width_px=350), unsafe_allow_html=True)
        st.divider()

    # --- Arama & Filtreleme ---
    st.markdown("""<div style="background:linear-gradient(135deg,#f5f0ff,#ede5ff);
        border-radius:10px;padding:14px 18px;margin-bottom:12px;
        border-left:4px solid #7c3aed;">
        <b style="color:#4c1d95;">Firma Ara & Filtrele</b></div>""", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 1.5, 1])
    with fc1:
        arama = st.text_input("Firma / Yetkili / Telefon Ara",
                              placeholder="Firma adi, yetkili kisi, telefon...",
                              key="fhav_ara")
    with fc2:
        sektor_list = ["Tümü"] + FIRMA_SEKTORLER
        sektor_filtre = st.selectbox("Sektor Filtre", sektor_list, key="fhav_sektor_f")
    with fc3:
        durum_filtre = st.selectbox("Durum", ["Tümü", "Aktif", "Pasif"], key="fhav_durum_f")

    # Filtreleme uygula
    filtered = firmalar
    if arama.strip():
        q = arama.strip().lower()
        filtered = [f for f in filtered
                    if q in f.firma_adi.lower()
                    or q in f.yetkili_kisi.lower()
                    or q in f.telefon.lower()
                    or q in f.email.lower()
                    or q in f.sektor.lower()
                    or q in f.adres.lower()]
    if sektor_filtre != "Tümü":
        filtered = [f for f in filtered if f.sektor == sektor_filtre]
    if durum_filtre == "Aktif":
        filtered = [f for f in filtered if f.aktif_mi]
    elif durum_filtre == "Pasif":
        filtered = [f for f in filtered if not f.aktif_mi]

    st.caption(f"Toplam {len(filtered)} / {len(firmalar)} firma listeleniyor")

    # --- Firma Kartlari ---
    if filtered:
        # Sektor bazli gruplama
        sektor_grp: dict[str, list] = {}
        for f in filtered:
            sek = f.sektor or "Diğer"
            sektor_grp.setdefault(sek, []).append(f)

        for sek_adi, sek_firmalar in sorted(sektor_grp.items()):
            st.markdown(f"""<div style="background:linear-gradient(135deg,#7c3aed,#5b21b6);
                color:white;border-radius:8px;padding:8px 14px;margin:10px 0 6px 0;
                font-weight:600;">{sek_adi} ({len(sek_firmalar)} firma)</div>""",
                unsafe_allow_html=True)

            for f in sek_firmalar:
                durum_badge = "🟢 Aktif" if f.aktif_mi else "🔴 Pasif"
                puan_str = ("⭐" * f.puan) if f.puan else "Puanlanmadi"
                with st.expander(f"**{f.firma_adi}**  |  {durum_badge}  |  {puan_str}", expanded=False):
                    # Bilgi karti
                    ic1, ic2, ic3 = st.columns(3)
                    with ic1:
                        st.markdown(f"**Yetkili:** {f.yetkili_kisi or '-'}")
                        st.markdown(f"**Telefon:** {f.telefon or '-'}")
                        st.markdown(f"**Email:** {f.email or '-'}")
                    with ic2:
                        st.markdown(f"**Adres:** {f.adres or '-'}")
                        st.markdown(f"**Web:** {f.web_sitesi or '-'}")
                        st.markdown(f"**Hizmet Alanlari:** {f.hizmet_alanlari or '-'}")
                    with ic3:
                        st.markdown(f"**Vergi Dairesi:** {f.vergi_dairesi or '-'}")
                        st.markdown(f"**Vergi No:** {f.vergi_no or '-'}")
                        st.markdown(f"**Notlar:** {f.notlar or '-'}")

                    # Duzenleme
                    st.markdown("---")
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        yf = st.text_input("Firma Adi", value=f.firma_adi, key=f"fhav_f_{f.id}")
                        ys = st.selectbox("Sektor", FIRMA_SEKTORLER,
                                          index=FIRMA_SEKTORLER.index(f.sektor) if f.sektor in FIRMA_SEKTORLER else len(FIRMA_SEKTORLER) - 1,
                                          key=f"fhav_s_{f.id}")
                        yy = st.text_input("Yetkili Kisi", value=f.yetkili_kisi, key=f"fhav_y_{f.id}")
                        yt = st.text_input("Telefon", value=f.telefon, key=f"fhav_t_{f.id}")
                        ye = st.text_input("Email", value=f.email, key=f"fhav_e_{f.id}")
                    with ec2:
                        ya = st.text_area("Adres", value=f.adres, key=f"fhav_a_{f.id}", height=68)
                        yw = st.text_input("Web Sitesi", value=f.web_sitesi, key=f"fhav_w_{f.id}")
                        yvd = st.text_input("Vergi Dairesi", value=f.vergi_dairesi, key=f"fhav_vd_{f.id}")
                        yvn = st.text_input("Vergi No", value=f.vergi_no, key=f"fhav_vn_{f.id}")
                        yha = st.text_input("Hizmet Alanlari", value=f.hizmet_alanlari, key=f"fhav_ha_{f.id}")

                    ec3, ec4 = st.columns(2)
                    with ec3:
                        yn = st.text_area("Notlar", value=f.notlar, key=f"fhav_n_{f.id}", height=68)
                    with ec4:
                        yp = st.slider("Puan (1-5)", 0, 5, value=f.puan, key=f"fhav_p_{f.id}")
                        yak = st.checkbox("Aktif", value=f.aktif_mi, key=f"fhav_ak_{f.id}")

                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("Güncelle", type="primary", key=f"fhav_up_{f.id}"):
                            f.firma_adi = yf.strip()
                            f.sektor = ys
                            f.yetkili_kisi = yy.strip()
                            f.telefon = yt.strip()
                            f.email = ye.strip()
                            f.adres = ya.strip()
                            f.web_sitesi = yw.strip()
                            f.vergi_dairesi = yvd.strip()
                            f.vergi_no = yvn.strip()
                            f.hizmet_alanlari = yha.strip()
                            f.notlar = yn.strip()
                            f.puan = yp
                            f.aktif_mi = yak
                            f.updated_at = datetime.now().isoformat()
                            store.upsert("firma_havuzu", f)
                            st.success("Firma güncellendi.")
                            st.rerun()
                    with bc2:
                        if confirm_action("Sil", "Bu firmayı havuzdan silmek istediğinize emin misiniz?", key=f"fhav_del_{f.id}"):
                            store.delete_by_id("firma_havuzu", f.id)
                            st.success(f"{f.firma_adi} silindi.")
                            st.rerun()
    elif firmalar:
        st.info("Filtreye uygun firma bulunamadı.")
    else:
        st.info("Henuz firma eklenmedi. Asagidaki formdan yeni firma ekleyebilirsiniz.")

    # --- Yeni Firma Ekle ---
    st.divider()
    styled_section("Yeni Firma Ekle", "#10b981")

    nc1, nc2 = st.columns(2)
    with nc1:
        n_firma = st.text_input("Firma Adi *", key="fhav_new_firma")
        n_sektor = st.selectbox("Sektor *", FIRMA_SEKTORLER, key="fhav_new_sektor")
        n_yetkili = st.text_input("Yetkili Kisi", key="fhav_new_yetkili")
        n_tel = st.text_input("Telefon", key="fhav_new_tel")
        n_email = st.text_input("Email", key="fhav_new_email")
    with nc2:
        n_adres = st.text_area("Adres", key="fhav_new_adres", height=68)
        n_web = st.text_input("Web Sitesi", key="fhav_new_web")
        n_vd = st.text_input("Vergi Dairesi", key="fhav_new_vd")
        n_vn = st.text_input("Vergi No", key="fhav_new_vn")
        n_ha = st.text_input("Hizmet Alanlari (virgul ile)", key="fhav_new_ha")

    nc3, nc4 = st.columns(2)
    with nc3:
        n_not = st.text_area("Notlar", key="fhav_new_not", height=68)
    with nc4:
        n_puan = st.slider("Puan (1-5)", 0, 5, value=0, key="fhav_new_puan")

    if st.button("Firma Kaydet", type="primary", key="fhav_new_btn"):
        if not n_firma.strip():
            st.error("Firma adi zorunludur.")
            return
        if not n_sektor:
            st.error("Sektor secimi zorunludur.")
            return
        yeni = FirmaHavuzu(
            firma_adi=n_firma.strip(),
            sektor=n_sektor,
            yetkili_kisi=n_yetkili.strip(),
            telefon=n_tel.strip(),
            email=n_email.strip(),
            adres=n_adres.strip(),
            web_sitesi=n_web.strip(),
            vergi_dairesi=n_vd.strip(),
            vergi_no=n_vn.strip(),
            hizmet_alanlari=n_ha.strip(),
            notlar=n_not.strip(),
            puan=n_puan,
        )
        store.upsert("firma_havuzu", yeni)
        st.success(f"Firma kaydedildi: {n_firma}")
        st.rerun()


# ============================================================
# TAB 7: TEDARIKCILER
# ============================================================

def _render_tedarikciler(store: DestekDataStore):
    styled_section("Tedarikci Yönetimi", "#8b5cf6")
    tedarikciler = store.load_objects("tedarikciler")
    alan_map = _alan_adi_map(store)

    # --- Hizmet Alani Dagilim Grafigi (Sunburst stili) ---
    if tedarikciler:
        aktif_tdr = [t for t in tedarikciler if t.aktif_mi]
        alan_cnt: dict[str, float] = {}
        alan_firma: dict[str, list[tuple[str, float]]] = {}
        for t in aktif_tdr:
            a_adi = alan_map.get(t.alan_kodu, t.alan_kodu or "Diğer")
            alan_cnt[a_adi] = alan_cnt.get(a_adi, 0) + 1
            alan_firma.setdefault(a_adi, [])
            alan_firma[a_adi].append((t.firma_adi, 1))

        if alan_cnt:
            tc1, tc2 = st.columns(2)
            with tc1:
                st.markdown(
                    ReportStyler.sunburst_chart_svg(alan_cnt, alan_firma, size=280,
                                                     title="Hizmet Alani / Tedarikci"),
                    unsafe_allow_html=True)
            with tc2:
                st.markdown(ReportStyler.horizontal_bar_html(
                    dict(sorted(alan_cnt.items(), key=lambda x: x[1], reverse=True)),
                    "#4472C4", max_width_px=300), unsafe_allow_html=True)
        st.divider()

    # --- Arama ve Filtreleme ---
    st.markdown("""<div style="background:linear-gradient(135deg,#f0f4ff,#e8ecff);
        border-radius:10px;padding:14px 18px;margin-bottom:12px;
        border-left:4px solid #8b5cf6;">
        <b style="color:#4c1d95;">Tedarikci Ara & Filtrele</b></div>""", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([2, 1.5, 1])
    with fc1:
        arama = st.text_input("Firma / Yetkili Ara", placeholder="Firma adi veya yetkili kisi...", key="des_tdr_ara")
    with fc2:
        alan_sec_list = ["Tümü"] + list(alan_map.values())
        alan_filtre = st.selectbox("Hizmet Alani Filtre", alan_sec_list, key="des_tdr_alan_f")
    with fc3:
        aktif_filtre = st.selectbox("Durum", ["Tümü", "Aktif", "Pasif"], key="des_tdr_aktif_f")

    # Filtreleme uygula
    filtered = tedarikciler
    if arama.strip():
        q = arama.strip().lower()
        filtered = [t for t in filtered if q in t.firma_adi.lower() or q in t.yetkili_kisi.lower()
                     or q in t.telefon.lower() or q in t.email.lower()]
    if alan_filtre != "Tümü":
        alan_kodu_rev = {v: k for k, v in alan_map.items()}
        sec_kod = alan_kodu_rev.get(alan_filtre, "")
        filtered = [t for t in filtered if t.alan_kodu == sec_kod]
    if aktif_filtre == "Aktif":
        filtered = [t for t in filtered if t.aktif_mi]
    elif aktif_filtre == "Pasif":
        filtered = [t for t in filtered if not t.aktif_mi]

    # Sonuc bilgisi
    st.caption(f"Toplam {len(filtered)} / {len(tedarikciler)} tedarikci listeleniyor")

    if filtered:
        # Interaktif tedarikci kartlari
        for t in filtered:
            alan_adi = alan_map.get(t.alan_kodu, t.alan_kodu)
            durum_badge = ("🟢 Aktif" if t.aktif_mi else "🔴 Pasif")
            with st.expander(f"**{t.firma_adi}**  |  {alan_adi}  |  {durum_badge}", expanded=False):
                ic1, ic2, ic3 = st.columns(3)
                with ic1:
                    st.markdown(f"**Yetkili:** {t.yetkili_kisi or '-'}")
                    st.markdown(f"**Telefon:** {t.telefon or '-'}")
                with ic2:
                    st.markdown(f"**Email:** {t.email or '-'}")
                    st.markdown(f"**Notlar:** {t.notlar or '-'}")
                with ic3:
                    st.markdown(f"**Sozlesme Başlangıç:** {t.sozlesme_baslangic or '-'}")
                    st.markdown(f"**Sozlesme Bitis:** {t.sozlesme_bitis or '-'}")

                # Duzenleme formu
                st.markdown("---")
                ec1, ec2 = st.columns(2)
                with ec1:
                    yeni_firma = st.text_input("Firma Adi", value=t.firma_adi, key=f"tdr_ed_f_{t.id}")
                    yeni_alan = st.selectbox("Hizmet Alani", list(alan_map.values()),
                                            index=list(alan_map.values()).index(alan_adi) if alan_adi in alan_map.values() else 0,
                                            key=f"tdr_ed_a_{t.id}")
                    yeni_yetkili = st.text_input("Yetkili Kisi", value=t.yetkili_kisi, key=f"tdr_ed_y_{t.id}")
                    yeni_tel = st.text_input("Telefon", value=t.telefon, key=f"tdr_ed_t_{t.id}")
                with ec2:
                    yeni_email = st.text_input("Email", value=t.email, key=f"tdr_ed_e_{t.id}")
                    yeni_not = st.text_input("Notlar", value=t.notlar, key=f"tdr_ed_n_{t.id}")
                    yeni_sb = st.text_input("Sozlesme Başlangıç (YYYY-MM-DD)", value=t.sozlesme_baslangic, key=f"tdr_ed_sb_{t.id}")
                    yeni_se = st.text_input("Sozlesme Bitis (YYYY-MM-DD)", value=t.sozlesme_bitis, key=f"tdr_ed_se_{t.id}")

                yeni_aktif = st.checkbox("Aktif", value=t.aktif_mi, key=f"tdr_ed_ak_{t.id}")

                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("Güncelle", type="primary", key=f"tdr_up_{t.id}"):
                        alan_kodu_rev2 = {v: k for k, v in alan_map.items()}
                        t.firma_adi = yeni_firma.strip()
                        t.alan_kodu = alan_kodu_rev2.get(yeni_alan, t.alan_kodu)
                        t.yetkili_kisi = yeni_yetkili.strip()
                        t.telefon = yeni_tel.strip()
                        t.email = yeni_email.strip()
                        t.notlar = yeni_not.strip()
                        t.sozlesme_baslangic = yeni_sb.strip()
                        t.sozlesme_bitis = yeni_se.strip()
                        t.aktif_mi = yeni_aktif
                        t.updated_at = datetime.now().isoformat()
                        store.upsert("tedarikciler", t)
                        st.success("Tedarikci güncellendi.")
                        st.rerun()
                with bc2:
                    if confirm_action("Sil", "Bu tedarikçiyi silmek istediğinize emin misiniz?", key=f"tdr_del_{t.id}"):
                        store.delete_by_id("tedarikciler", t.id)
                        st.success(f"{t.firma_adi} silindi.")
                        st.rerun()
    elif tedarikciler:
        st.info("Filtreye uygun tedarikci bulunamadı.")
    else:
        st.info("Henuz tedarikci eklenmedi.")

    st.divider()
    styled_section("Yeni Tedarikci Ekle", "#10b981")

    c1, c2 = st.columns(2)
    with c1:
        firma_adi = st.text_input("Firma Adi *", key="des_tdr_firma")
        alan_sec = st.selectbox("Hizmet Alani", list(alan_map.values()), key="des_tdr_alan")
        yetkili = st.text_input("Yetkili Kisi", key="des_tdr_yetkili")
    with c2:
        telefon = st.text_input("Telefon", key="des_tdr_tel")
        email = st.text_input("Email", key="des_tdr_email")
        notlar = st.text_input("Notlar", key="des_tdr_not")

    nc1, nc2 = st.columns(2)
    with nc1:
        sozlesme_bas = st.text_input("Sozlesme Başlangıç (YYYY-MM-DD)", key="des_tdr_sb")
    with nc2:
        sozlesme_bit = st.text_input("Sozlesme Bitis (YYYY-MM-DD)", key="des_tdr_se")

    if st.button("Tedarikci Kaydet", type="primary", key="des_tdr_btn"):
        if not firma_adi.strip():
            st.error("Firma adi zorunludur.")
            return
        alan_kodu_rev = {v: k for k, v in alan_map.items()}
        tdr = Tedarikci(
            firma_adi=firma_adi.strip(),
            alan_kodu=alan_kodu_rev.get(alan_sec, ""),
            yetkili_kisi=yetkili.strip(),
            telefon=telefon.strip(),
            email=email.strip(),
            notlar=notlar.strip(),
            sozlesme_baslangic=sozlesme_bas.strip(),
            sozlesme_bitis=sozlesme_bit.strip(),
        )
        store.upsert("tedarikciler", tdr)
        st.success(f"Tedarikci kaydedildi: {firma_adi}")
        st.rerun()


# ============================================================
# TAB 7: RAPORLAR  (Excel sunburst stili + filtreleme + PDF)
# ============================================================

_DONEM_SECENEKLERI = ["Günlük", "Haftalık", "Aylık", "Yıllık", "Özel Aralik"]


def _period_date_range(donem: str, ref_date: date, custom_start: date | None = None,
                       custom_end: date | None = None) -> tuple[date, date]:
    """Secilen doneme gore baslangic-bitis tarih araligi dondurur."""
    if donem == "Günlük":
        return ref_date, ref_date
    if donem == "Haftalık":
        start = ref_date - timedelta(days=ref_date.weekday())
        return start, start + timedelta(days=6)
    if donem == "Aylık":
        start = ref_date.replace(day=1)
        next_m = (start.month % 12) + 1
        next_y = start.year + (1 if next_m == 1 else 0)
        end = date(next_y, next_m, 1) - timedelta(days=1)
        return start, end
    if donem == "Yıllık":
        return date(ref_date.year, 1, 1), date(ref_date.year, 12, 31)
    # Ozel
    if custom_start and custom_end:
        return custom_start, custom_end
    return date(ref_date.year, 1, 1), ref_date


def _filter_by_date(items: list[dict], start: date, end: date, date_field: str = "created_at") -> list[dict]:
    """Tarih alanina gore filtrele."""
    s_str = start.isoformat()
    e_str = end.isoformat()
    result = []
    for item in items:
        d = item.get(date_field, "")[:10]
        if d and s_str <= d <= e_str:
            result.append(item)
    return result


def _render_donem_filtre(key_prefix: str) -> tuple[date, date]:
    """Donem secici widget'larini cizer, (start, end) dondurur."""
    c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 1])
    with c1:
        donem = st.selectbox("Donem", _DONEM_SECENEKLERI, index=2, key=f"{key_prefix}_donem")
    with c2:
        ref = st.date_input("Referans Tarih", value=date.today(), key=f"{key_prefix}_ref")
    custom_s, custom_e = None, None
    if donem == "Özel Aralik":
        with c3:
            custom_s = st.date_input("Başlangıç", value=date.today().replace(day=1), key=f"{key_prefix}_cs")
        with c4:
            custom_e = st.date_input("Bitis", value=date.today(), key=f"{key_prefix}_ce")
    start, end = _period_date_range(donem, ref, custom_s, custom_e)
    styled_info_banner(f"Rapor Donemi: {start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}", "info", "\U0001f4c5")
    return start, end


def _render_raporlar(store: DestekDataStore):
    sub = st.tabs(["📊 Genel Özet", "🎫 Talep Raporlari", "📋 Denetim Raporlari", "🔧 PBK Raporlari"])

    with sub[0]:
        _render_rapor_genel(store)
    with sub[1]:
        _render_rapor_talep(store)
    with sub[2]:
        _render_rapor_denetim(store)
    with sub[3]:
        _render_rapor_pbk(store)

    # ================================================================
    # PERFORMANS KARSILASTIRMA + AI ONERILERI + KUNYE + PDF
    # ================================================================
    from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                     generate_module_pdf, render_pdf_download_button,
                                     render_report_kunye_html, ReportStyler as _RS)

    st.markdown(_RS.section_divider_html("Donemsel Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

    from datetime import datetime as _dt, timedelta as _td
    _now = _dt.now()
    _cur_month = _now.strftime("%Y-%m")
    _prev_month = (_now.replace(day=1) - _td(days=1)).strftime("%Y-%m")

    try:
        _dh_tickets_raw = store.load_list("tickets")
        _dh_denetim_raw = store.load_list("denetimler")
        _dh_bakim_raw = store.load_list("bakim_kayitlari")
        _dh_periyodik_raw = store.load_list("periyodik_gorevler")
    except Exception:
        _dh_tickets_raw, _dh_denetim_raw, _dh_bakim_raw, _dh_periyodik_raw = [], [], [], []

    def _dh_count_by_month(records, month_str, date_fields=("created_at", "tarih", "plan_tarihi", "yapildi_tarihi")):
        c = 0
        for r in records:
            for df in date_fields:
                val = r.get(df, "")
                if val and val[:7] == month_str:
                    c += 1
                    break
        return c

    _dh_tickets_cur = _dh_count_by_month(_dh_tickets_raw, _cur_month)
    _dh_tickets_prev = _dh_count_by_month(_dh_tickets_raw, _prev_month)
    _dh_kapali_cur = sum(1 for t in _dh_tickets_raw if t.get("durum") == "Kapandi" and t.get("kapanis_tarihi", "")[:7] == _cur_month)
    _dh_kapali_prev = sum(1 for t in _dh_tickets_raw if t.get("durum") == "Kapandi" and t.get("kapanis_tarihi", "")[:7] == _prev_month)

    _dh_comparisons = [
        {"label": "Yeni Talepler", "current": _dh_tickets_cur, "previous": _dh_tickets_prev},
        {"label": "Cozulen Talepler", "current": _dh_kapali_cur, "previous": _dh_kapali_prev},
        {"label": "Denetimler", "current": _dh_count_by_month(_dh_denetim_raw, _cur_month), "previous": _dh_count_by_month(_dh_denetim_raw, _prev_month)},
        {"label": "Bakım Kayıtları", "current": _dh_count_by_month(_dh_bakim_raw, _cur_month), "previous": _dh_count_by_month(_dh_bakim_raw, _prev_month)},
    ]
    st.markdown(period_comparison_row_html(_dh_comparisons), unsafe_allow_html=True)

    # ---- AI Onerileri ----
    _dh_insights = []

    _toplam_ticket = len(_dh_tickets_raw)
    _acik_ticket = sum(1 for t in _dh_tickets_raw if t.get("durum") not in ("Kapandi",))
    _kapali_ticket = sum(1 for t in _dh_tickets_raw if t.get("durum") == "Kapandi")
    _sla_ihlal = sum(1 for t in _dh_tickets_raw if t.get("sla_ihlal") in (True, "true", "True"))
    _cozum_orani = round((_kapali_ticket / _toplam_ticket) * 100, 1) if _toplam_ticket > 0 else 0
    _sla_uyum = round((1 - _sla_ihlal / _toplam_ticket) * 100, 1) if _toplam_ticket > 0 else 100

    # Tekrarlayan sorunlari tespit et
    _kategori_cnt: dict[str, int] = {}
    for t in _dh_tickets_raw:
        k = t.get("hizmet_alani_kodu", "Diğer")
        _kategori_cnt[k] = _kategori_cnt.get(k, 0) + 1
    _en_cok_kategori = max(_kategori_cnt.items(), key=lambda x: x[1]) if _kategori_cnt else ("", 0)

    _geciken_periyodik = sum(1 for g in _dh_periyodik_raw if g.get("durum") in ("Gecikti", "gecikti", "Beklemede"))

    if _acik_ticket > 10:
        _dh_insights.append({
            "icon": "\u26a0\ufe0f", "title": "Yuksek Açık Talep Sayısı",
            "text": f"{_acik_ticket} talep hala acik durumda. Öncelik siralamasinin gozden gecirilmesi ve ek kaynak tahsisi degerlendirilmelidir.",
            "color": "#ef4444"
        })

    if _sla_ihlal > 3:
        _dh_insights.append({
            "icon": "\u23f0", "title": "SLA Ihlalleri",
            "text": f"{_sla_ihlal} talepte SLA ihlali tespit edildi (SLA Uyum: %{_sla_uyum:.0f}). Mudahale ve cozum surelerinin iyilestirilmesi için surec analizi onerilir.",
            "color": "#f59e0b"
        })

    if _en_cok_kategori[1] > 5:
        _dh_insights.append({
            "icon": "\U0001f504", "title": "Tekrarlayan Sorun Alani",
            "text": f"'{_en_cok_kategori[0]}' alaninda {_en_cok_kategori[1]} talep birikti. Kok neden analizi yapilarak kalici cozum uretilmesi onerilir.",
            "color": "#ea580c"
        })

    if _geciken_periyodik > 0:
        _dh_insights.append({
            "icon": "\U0001f527", "title": "Geciken Periyodik Görevler",
            "text": f"{_geciken_periyodik} periyodik bakım/gorev gecikme durumunda. Bakım takviminin guncellenmesi ve sorumlu atamasinin kontrol edilmesi onerilir.",
            "color": "#8b5cf6"
        })

    _dh_insights.append({
        "icon": "\U0001f4a1", "title": "Genel Oneri",
        "text": f"Toplam {_toplam_ticket} talep, Cozum Orani: %{_cozum_orani:.0f}, SLA Uyum: %{_sla_uyum:.0f}. Duzenli performans raporlamasi ve tedarikci degerlendirmesi surdurul melidir.",
        "color": "#2563eb"
    })

    _dh_insights.append({
        "icon": "\U0001f4c5", "title": "Bakım Planlama",
        "text": "Onleyici bakım takviminin olusturulmasi ve periyodik denetimlerin zamaninda yapilmasi ekipman omrunu uzatir ve maliyet tasarrufu saglar.",
        "color": "#0d9488"
    })

    st.markdown(ai_recommendations_html(_dh_insights), unsafe_allow_html=True)

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(_RS.section_divider_html("Destek Hizmetleri PDF Raporu", "#1e40af"), unsafe_allow_html=True)
    if st.button("\U0001f4e5 Destek Hizmetleri Raporu Oluştur (PDF)", key="dh_full_pdf_btn", use_container_width=True):
        try:
            _sections = [
                {
                    "title": "Destek Hizmetleri Genel İstatistikler",
                    "metrics": [
                        ("Toplam Talep", _toplam_ticket, "#2563eb"),
                        ("Açık", _acik_ticket, "#ef4444"),
                        ("Kapali", _kapali_ticket, "#10b981"),
                        ("SLA Ihlal", _sla_ihlal, "#f59e0b"),
                    ],
                    "text": f"Cozum Orani: %{_cozum_orani:.0f} | SLA Uyum: %{_sla_uyum:.0f} | Geciken Periyodik: {_geciken_periyodik}",
                },
                {
                    "title": "Donemsel Karsilastirma",
                    "text": " | ".join([f"{c['label']}: {c['current']} (onceki: {c['previous']})" for c in _dh_comparisons]),
                },
            ]
            _pdf_bytes = generate_module_pdf("Destek Hizmetleri Raporu", _sections)
            render_pdf_download_button(_pdf_bytes, "destek_hizmetleri_raporu.pdf", "Destek Hizmetleri Raporu Indir", "dh_full_dl")
        except Exception as _e:
            st.error(f"PDF olusturulurken hata: {_e}")


# ---------- GENEL OZET ----------

def _render_rapor_genel(store: DestekDataStore):
    styled_section("Genel Özet Raporu", "#2563eb")
    start, end = _render_donem_filtre("des_rg")

    all_tickets = store.load_list("tickets")
    tickets = _filter_by_date(all_tickets, start, end)

    if not tickets:
        styled_info_banner("Secilen donemde talep bulunamadı.", "info")
        return

    toplam = len(tickets)
    acik = sum(1 for t in tickets if t.get("durum") not in ("Kapandi",))
    kapali = sum(1 for t in tickets if t.get("durum") == "Kapandi")
    sla_ihlal = sum(1 for t in tickets if SLACalculator.check_sla_violation(t))
    sla_uyum = round((1 - sla_ihlal / toplam) * 100, 0) if toplam > 0 else 100

    styled_stat_row([
        ("Toplam Talep", toplam, "#2563eb", "\U0001f4dd"),
        ("Açık", acik, "#ef4444", "\U0001f534"),
        ("Kapali", kapali, "#10b981", "\U0001f7e2"),
        ("SLA Uyum", f"%{sla_uyum:.0f}", "#0d9488", "\U0001f4ca"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    alan_map = _alan_adi_map(store)

    # ---- Sunburst: Hizmet Alani -> Alt Kategori ----
    styled_section("Hizmet Alani ve Alt Kategori Dagilimi (Sunburst)", "#4472C4")
    alan_counts: dict[str, float] = {}
    alan_sub: dict[str, list[tuple[str, float]]] = {}
    alt_kat_map = {ak.alt_kategori_kodu: ak.alt_kategori_adi for ak in store.load_objects("alt_kategoriler")}

    for t in tickets:
        ak = t.get("hizmet_alani_kodu", "DIG")
        alan_adi = alan_map.get(ak, ak)
        alan_counts[alan_adi] = alan_counts.get(alan_adi, 0) + 1
        sub_key = t.get("alt_kategori_kodu", "")
        sub_adi = alt_kat_map.get(sub_key, sub_key or "Diğer")
        alan_sub.setdefault(alan_adi, [])
        found = False
        for i, (s_adi, s_val) in enumerate(alan_sub[alan_adi]):
            if s_adi == sub_adi:
                alan_sub[alan_adi][i] = (s_adi, s_val + 1)
                found = True
                break
        if not found:
            alan_sub[alan_adi].append((sub_adi, 1))

    st.markdown(
        ReportStyler.sunburst_chart_svg(alan_counts, alan_sub, size=380,
                                         title="Hizmet Alani / Alt Kategori"),
        unsafe_allow_html=True,
    )

    # ---- Yan yana: Oncelik bar + SLA donut ----
    c1, c2 = st.columns(2)
    with c1:
        styled_section("Öncelik Dagilimi", "#ED7D31")
        onc_counts = Counter(t.get("oncelik", "Normal") for t in tickets)
        if onc_counts:
            st.markdown(ReportStyler.horizontal_bar_html(dict(onc_counts.most_common()), "#ED7D31", max_width_px=300), unsafe_allow_html=True)
    with c2:
        styled_section("SLA Uyum Orani", "#0d9488")
        sla_data = {"SLA Uyumlu": toplam - sla_ihlal, "SLA Ihlal": sla_ihlal}
        st.markdown(ReportStyler.donut_chart_svg(sla_data, colors=["#4472C4", "#ED7D31"], size=155), unsafe_allow_html=True)

    # ---- Veri Tablosu ----
    styled_section("Talep Detay Tablosu", "#94A3B8")
    rows = []
    for t in sorted(tickets, key=lambda x: x.get("created_at", ""), reverse=True)[:50]:
        rows.append({
            "No": t.get("ticket_no", ""),
            "Hizmet Alani": alan_map.get(t.get("hizmet_alani_kodu", ""), ""),
            "Öncelik": t.get("oncelik", ""),
            "Durum": t.get("durum", ""),
            "Lokasyon": t.get("lokasyon", ""),
            "Tarih": t.get("created_at", "")[:10],
        })
    if rows:
        df = pd.DataFrame(rows)
        st.markdown(ReportStyler.colored_table_html(df, "#2563eb"), unsafe_allow_html=True)

    # ---- Ozet satir ----
    st.divider()
    styled_section("Özet Tablo", "#64748b")
    ozet_rows = []
    for alan_adi, cnt in sorted(alan_counts.items(), key=lambda x: x[1], reverse=True):
        ozet_rows.append({
            "Hizmet Alani": alan_adi,
            "Talep Sayısı": int(cnt),
            "Oran": f"%{cnt / toplam * 100:.1f}",
        })
    if ozet_rows:
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(ozet_rows), "#4472C4"), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.divider()
    if st.button("PDF Rapor Oluştur", type="primary", key="des_rg_pdf"):
        pdf = _generate_ozet_pdf(store, tickets, alan_map, alan_counts, start, end)
        if pdf:
            st.download_button("PDF İndir", data=pdf, file_name=f"Destek_Özet_{start}_{end}.pdf",
                               mime="application/pdf", key="des_rg_dl")


def _generate_ozet_pdf(store: DestekDataStore, tickets: list[dict], alan_map: dict,
                       alan_counts: dict, start: date, end: date) -> bytes | None:
    try:
        info = get_institution_info()
        gen = ReportPDFGenerator("Destek Hizmetleri Genel Özet Raporu",
                                  f"Dönem: {start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}")
        gen.add_header(kurum_adi=info.get("name", ""))

        toplam = len(tickets)
        acik = sum(1 for t in tickets if t.get("durum") not in ("Kapandi",))
        kapali = toplam - acik
        sla_ihlal = sum(1 for t in tickets if SLACalculator.check_sla_violation(t))
        sla_uyum = round((1 - sla_ihlal / toplam) * 100, 0) if toplam > 0 else 100

        gen.add_section("Temel Göstergeler (KPI)")
        gen.add_metrics([
            ("Toplam Talep", toplam, "#2563eb"),
            ("Açık", acik, "#ef4444"),
            ("Kapalı", kapali, "#10b981"),
            ("SLA Uyum %", f"{sla_uyum:.0f}", "#0d9488"),
        ])
        gen.add_spacer(0.4)

        # Hizmet alanı bar chart
        chart_data = {k: v for k, v in sorted(alan_counts.items(), key=lambda x: x[1], reverse=True)[:10]}
        gen.add_section("Hizmet Alanı Dağılımı")
        gen.add_bar_chart(chart_data, "Hizmet Alanı Bazında Talep Sayısı", "#4472C4")

        # Öncelik donut
        onc_counts = Counter(t.get("oncelik", "Normal") for t in tickets)
        gen.add_section("Öncelik Dağılımı")
        gen.add_donut_chart(dict(onc_counts.most_common()), "Öncelik Bazında Dağılım")

        # SLA donut
        gen.add_section("SLA Uyum Oranı")
        gen.add_donut_chart({"SLA Uyumlu": toplam - sla_ihlal, "SLA İhlal": sla_ihlal},
                            "SLA Uyum", ["#4472C4", "#ED7D31"])

        # Detay tablosu
        gen.add_section("Talep Detay Tablosu")
        rows = []
        for t in sorted(tickets, key=lambda x: x.get("created_at", ""), reverse=True)[:30]:
            rows.append({
                "No": t.get("ticket_no", ""),
                "Alan": alan_map.get(t.get("hizmet_alani_kodu", ""), ""),
                "Öncelik": t.get("oncelik", ""),
                "Durum": t.get("durum", ""),
                "Tarih": t.get("created_at", "")[:10],
            })
        if rows:
            gen.add_table(pd.DataFrame(rows))

        return gen.generate()
    except Exception:
        return None


# ---------- TALEP RAPORLARI ----------

def _render_rapor_talep(store: DestekDataStore):
    styled_section("Talep Raporlari", "#1e40af")
    start, end = _render_donem_filtre("des_rt")

    all_tickets = store.load_list("tickets")
    tickets = _filter_by_date(all_tickets, start, end)

    if not tickets:
        styled_info_banner("Secilen donemde talep verisi yok.", "info")
        return

    toplam = len(tickets)
    sla_ihlal = sum(1 for t in tickets if SLACalculator.check_sla_violation(t))

    styled_stat_row([
        ("Toplam", toplam, "#2563eb", "\U0001f4dd"),
        ("SLA Ihlal", sla_ihlal, "#ef4444", "\u26a0\ufe0f"),
        ("SLA Uyum", f"%{round((1 - sla_ihlal / toplam) * 100) if toplam else 100}", "#10b981", "\U0001f4ca"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    alan_map = _alan_adi_map(store)

    # ---- Durum Dagilimi (bar) ----
    c1, c2 = st.columns(2)
    with c1:
        styled_section("Durum Dagilimi", "#4472C4")
        durum_counts = Counter(t.get("durum", "") for t in tickets)
        st.markdown(ReportStyler.horizontal_bar_html(dict(durum_counts.most_common()), "#4472C4", max_width_px=350), unsafe_allow_html=True)
    with c2:
        styled_section("Öncelik Dagilimi", "#ED7D31")
        onc_counts = Counter(t.get("oncelik", "Normal") for t in tickets)
        st.markdown(ReportStyler.donut_chart_svg(dict(onc_counts.most_common()),
                                                  colors=["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000"], size=155),
                    unsafe_allow_html=True)

    # ---- Hizmet Alani sunburst + bar chart (Excel stili) ----
    styled_section("Hizmet Alani / Alt Kategori Dagilimi", "#2563eb")
    alan_counts = Counter(t.get("hizmet_alani_kodu", "DIG") for t in tickets)
    chart_data = {alan_map.get(k, k): v for k, v in alan_counts.most_common(10)}

    alt_kat_map = {ak.alt_kategori_kodu: ak.alt_kategori_adi for ak in store.load_objects("alt_kategoriler")}
    alan_sub_rt: dict[str, list[tuple[str, float]]] = {}
    for ak_kodu, _ in alan_counts.most_common(10):
        a_adi = alan_map.get(ak_kodu, ak_kodu)
        sub_cnt = Counter(
            alt_kat_map.get(t.get("alt_kategori_kodu", ""), t.get("alt_kategori_kodu", "Diğer"))
            for t in tickets if t.get("hizmet_alani_kodu") == ak_kodu
        )
        alan_sub_rt[a_adi] = [(k, v) for k, v in sub_cnt.most_common()]

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown(
            ReportStyler.sunburst_chart_svg(chart_data, alan_sub_rt, size=320,
                                             title="Hizmet Alani / Alt Kategori"),
            unsafe_allow_html=True)
    with rc2:
        st.markdown(ReportStyler.horizontal_bar_html(chart_data, "#4472C4", max_width_px=400), unsafe_allow_html=True)

    # ---- Cozum suresi analizi ----
    styled_section("Cozum Suresi Analizi", "#0d9488")
    kapanan = [t for t in tickets if t.get("durum") == "Kapandi" and t.get("kapanis_tarihi")]
    if kapanan:
        sureler = []
        for t in kapanan:
            try:
                acilis = datetime.fromisoformat(t["created_at"])
                kapanis = datetime.fromisoformat(t["kapanis_tarihi"])
                saat = (kapanis - acilis).total_seconds() / 3600
                sureler.append({"No": t.get("ticket_no", ""), "Alan": alan_map.get(t.get("hizmet_alani_kodu", ""), ""),
                                "Öncelik": t.get("oncelik", ""), "Cozum Suresi (saat)": f"{saat:.1f}"})
            except (ValueError, KeyError):
                continue
        if sureler:
            st.markdown(ReportStyler.colored_table_html(pd.DataFrame(sureler), "#0d9488", "Cozum Suresi (saat)"), unsafe_allow_html=True)
            ort_saat = sum(float(s["Cozum Suresi (saat)"]) for s in sureler) / len(sureler)
            styled_info_banner(f"Ortalama Cozum Suresi: {ort_saat:.1f} saat ({ort_saat / 24:.1f} gun)", "info", "\u23f1\ufe0f")
    else:
        styled_info_banner("Bu donemde kapanan talep yok.", "info")

    # ---- SLA Uyum Trendi (gunluk) ----
    styled_section("SLA Durumu Tablosu", "#8b5cf6")
    sla_rows = []
    for t in tickets:
        remaining = SLACalculator.get_remaining_minutes(t)
        sla_str = "-"
        if remaining is not None:
            if remaining < 0:
                sla_str = "IHLAL"
            else:
                sla_str = f"{remaining // 60}s {remaining % 60}dk"
        sla_rows.append({
            "No": t.get("ticket_no", ""),
            "Öncelik": t.get("oncelik", ""),
            "Durum": t.get("durum", ""),
            "SLA Kalan": sla_str,
        })
    if sla_rows:
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(sla_rows[:30]), "#8b5cf6"), unsafe_allow_html=True)

    # ---- PDF ----
    st.divider()
    if st.button("Talep Raporu PDF", type="primary", key="des_rt_pdf"):
        pdf = _generate_talep_rapor_pdf(store, tickets, alan_map, start, end)
        if pdf:
            st.download_button("PDF İndir", data=pdf, file_name=f"Destek_Talep_Rapor_{start}_{end}.pdf",
                               mime="application/pdf", key="des_rt_dl")


def _generate_talep_rapor_pdf(store: DestekDataStore, tickets: list, alan_map: dict,
                               start: date, end: date) -> bytes | None:
    try:
        info = get_institution_info()
        gen = ReportPDFGenerator("Destek Hizmetleri Talep Raporu",
                                  f"Dönem: {start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}")
        gen.add_header(kurum_adi=info.get("name", ""))

        toplam = len(tickets)
        sla_ihlal = sum(1 for t in tickets if SLACalculator.check_sla_violation(t))

        gen.add_section("Temel Göstergeler")
        gen.add_metrics([
            ("Toplam", toplam, "#2563eb"),
            ("SLA İhlal", sla_ihlal, "#ef4444"),
            ("Uyum %", f"{round((1 - sla_ihlal / toplam) * 100) if toplam else 100}", "#10b981"),
        ])
        gen.add_spacer(0.4)

        # Durum dağılımı
        durum_counts = Counter(t.get("durum", "") for t in tickets)
        gen.add_section("Durum Dağılımı")
        gen.add_bar_chart(dict(durum_counts.most_common()), "Durum Bazında Talep", "#4472C4")

        # Hizmet alanı
        alan_counts = Counter(t.get("hizmet_alani_kodu", "DIG") for t in tickets)
        chart_data = {alan_map.get(k, k): v for k, v in alan_counts.most_common(10)}
        gen.add_section("Hizmet Alanı Dağılımı")
        gen.add_bar_chart(chart_data, "Hizmet Alanı Bazında Talep", "#4472C4")

        # Öncelik donut
        onc_counts = Counter(t.get("oncelik", "Normal") for t in tickets)
        gen.add_section("Öncelik Dağılımı")
        gen.add_donut_chart(dict(onc_counts.most_common()), "Öncelik Dağılımı")

        # Detay tablo
        gen.add_section("Talep Listesi")
        rows = []
        for t in sorted(tickets, key=lambda x: x.get("created_at", ""), reverse=True)[:40]:
            rows.append({
                "No": t.get("ticket_no", ""),
                "Alan": alan_map.get(t.get("hizmet_alani_kodu", ""), ""),
                "Öncelik": t.get("oncelik", ""),
                "Durum": t.get("durum", ""),
                "Tarih": t.get("created_at", "")[:10],
            })
        if rows:
            gen.add_table(pd.DataFrame(rows))

        return gen.generate()
    except Exception:
        return None


# ---------- DENETIM RAPORLARI ----------

def _render_rapor_denetim(store: DestekDataStore):
    styled_section("Denetim Raporlari", "#8b5cf6")
    start, end = _render_donem_filtre("des_rd")

    denetimler = store.load_objects("denetimler")
    if not denetimler:
        styled_info_banner("Denetim verisi yok.", "info")
        return

    # Tarih filtresi
    filtered = []
    for d in denetimler:
        d_date = d.created_at[:10] if hasattr(d, "created_at") and d.created_at else ""
        if d_date and start.isoformat() <= d_date <= end.isoformat():
            filtered.append(d)
    if not filtered:
        filtered = denetimler  # fallback tum veriye

    onaylanan = [d for d in filtered if d.durum in ("Onaylandi", "Arsiv")]
    if not onaylanan:
        styled_info_banner("Secilen donemde onaylanmis denetim yok. Tüm denetimler gosteriliyor.", "warning")
        onaylanan = [d for d in denetimler if d.durum in ("Onaylandi", "Arsiv")]
        if not onaylanan:
            styled_info_banner("Onaylanmis denetim bulunmuyor.", "info")
            return

    toplam_den = len(onaylanan)
    ort_skor = sum(d.yuzde_skor for d in onaylanan) / toplam_den if toplam_den else 0
    basarili = sum(1 for d in onaylanan if d.genel_sonuc == "Başarılı")
    basarisiz = sum(1 for d in onaylanan if d.genel_sonuc == "Başarısız")

    styled_stat_row([
        ("Toplam Denetim", toplam_den, "#8b5cf6", "\U0001f50d"),
        ("Ort. Skor", f"%{ort_skor:.0f}", "#2563eb", "\U0001f4ca"),
        ("Başarılı", basarili, "#10b981", "\u2705"),
        ("Başarısız", basarisiz, "#ef4444", "\u274c"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Sunburst: Form -> Sonuc (Excel stili) + Skor bar ----
    form_map = {f.form_kodu: f.form_adi for f in store.load_objects("denetim_formlari")}
    form_scores: dict[str, list] = {}
    form_cnt: dict[str, float] = {}
    form_sonuc: dict[str, list[tuple[str, float]]] = {}
    for d in onaylanan:
        fn = form_map.get(d.form_kodu, d.form_kodu)
        form_scores.setdefault(fn, []).append(d.yuzde_skor)
        form_cnt[fn] = form_cnt.get(fn, 0) + 1
        form_sonuc.setdefault(fn, {})
        form_sonuc[fn][d.genel_sonuc] = form_sonuc[fn].get(d.genel_sonuc, 0) + 1
    form_sonuc_list = {k: [(s, c) for s, c in v.items()] for k, v in form_sonuc.items()}

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Form / Sonuc Dagilimi (Sunburst)", "#4472C4")
        if form_cnt:
            st.markdown(
                ReportStyler.sunburst_chart_svg(form_cnt, form_sonuc_list, size=300,
                                                 title="Form / Sonuc"),
                unsafe_allow_html=True)
    with c2:
        styled_section("Form Bazinda Ortalama Skor", "#4472C4")
        chart_data = {k: round(sum(v) / len(v), 1) for k, v in form_scores.items()}
        st.markdown(ReportStyler.horizontal_bar_html(chart_data, "#4472C4", max_width_px=350, max_val=100), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        styled_section("Sonuc Dagilimi", "#ED7D31")
        sonuc_counts = Counter(d.genel_sonuc for d in onaylanan)
        st.markdown(ReportStyler.donut_chart_svg(dict(sonuc_counts),
                                                  colors=["#10b981", "#FFC000", "#ef4444"], size=145),
                    unsafe_allow_html=True)

    # ---- Denetim detay tablosu ----
    styled_section("Denetim Detay Tablosu", "#94A3B8")
    rows = []
    for d in sorted(onaylanan, key=lambda x: x.created_at, reverse=True):
        rows.append({
            "No": d.denetim_no,
            "Form": form_map.get(d.form_kodu, d.form_kodu),
            "Donem": f"{d.donem_ay}/{d.donem_yil}",
            "Skor (%)": f"{d.yuzde_skor:.0f}",
            "Sonuc": d.genel_sonuc,
            "Denetci": d.denetci_adi,
            "Kritik Bulgu": "Evet" if d.kritik_bulgu_var else "Hayir",
        })
    if rows:
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(rows), "#8b5cf6", "Skor (%)"), unsafe_allow_html=True)

    # ---- PDF ----
    st.divider()
    if st.button("Denetim Raporu PDF", type="primary", key="des_rd_pdf"):
        pdf = _generate_denetim_rapor_pdf(store, onaylanan, form_map, start, end)
        if pdf:
            st.download_button("PDF İndir", data=pdf, file_name=f"Destek_Denetim_Rapor_{start}_{end}.pdf",
                               mime="application/pdf", key="des_rd_dl")


def _generate_denetim_rapor_pdf(store: DestekDataStore, onaylanan: list, form_map: dict,
                                 start: date, end: date) -> bytes | None:
    try:
        info = get_institution_info()
        gen = ReportPDFGenerator("Destek Hizmetleri Denetim Raporu",
                                  f"Dönem: {start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}")
        gen.add_header(kurum_adi=info.get("name", ""))

        toplam_den = len(onaylanan)
        ort_skor = sum(d.yuzde_skor for d in onaylanan) / toplam_den if toplam_den else 0

        gen.add_section("Temel Göstergeler")
        gen.add_metrics([
            ("Toplam", toplam_den, "#8b5cf6"),
            ("Ort. Skor %", f"{ort_skor:.0f}", "#2563eb"),
            ("Başarılı", sum(1 for d in onaylanan if d.genel_sonuc == "Başarılı"), "#10b981"),
            ("Başarısız", sum(1 for d in onaylanan if d.genel_sonuc == "Başarısız"), "#ef4444"),
        ])
        gen.add_spacer(0.4)

        # Form bazında skor
        form_scores: dict[str, list] = {}
        for d in onaylanan:
            form_scores.setdefault(form_map.get(d.form_kodu, d.form_kodu), []).append(d.yuzde_skor)
        chart_data = {k: round(sum(v) / len(v), 1) for k, v in form_scores.items()}
        gen.add_section("Form Bazında Ortalama Skor")
        gen.add_bar_chart(chart_data, "Form Bazında Skor (%)", "#4472C4")

        # Sonuç dağılımı
        sonuc_counts = Counter(d.genel_sonuc for d in onaylanan)
        gen.add_section("Sonuç Dağılımı")
        gen.add_donut_chart(dict(sonuc_counts), "Denetim Sonuçları")

        # Detay tablo
        gen.add_section("Denetim Detay Tablosu")
        rows = []
        for d in sorted(onaylanan, key=lambda x: x.created_at, reverse=True):
            rows.append({
                "No": d.denetim_no,
                "Form": form_map.get(d.form_kodu, d.form_kodu),
                "Dönem": f"{d.donem_ay}/{d.donem_yil}",
                "Skor": f"{d.yuzde_skor:.0f}%",
                "Sonuç": d.genel_sonuc,
            })
        if rows:
            gen.add_table(pd.DataFrame(rows))

        return gen.generate()
    except Exception:
        return None


# ---------- PBK RAPORLARI ----------

def _render_rapor_pbk(store: DestekDataStore):
    styled_section("PBK Raporlari", "#0d9488")
    start, end = _render_donem_filtre("des_rp")

    all_kayitlar = store.load_list("bakim_kayitlari")
    kayitlar = _filter_by_date(all_kayitlar, start, end, "plan_tarihi")
    if not kayitlar:
        kayitlar = all_kayitlar  # fallback

    if not kayitlar:
        styled_info_banner("Bakım kaydı yok.", "info")
        return

    toplam = len(kayitlar)
    tamamlanan = sum(1 for k in kayitlar if k.get("durum") == "Tamamlandı")
    uygunsuz = sum(1 for k in kayitlar if k.get("durum") == "Uygunsuz")
    bekleyen = toplam - tamamlanan - uygunsuz
    uyum_orani = round(tamamlanan / toplam * 100, 0) if toplam > 0 else 0

    styled_stat_row([
        ("Toplam", toplam, "#2563eb", "\U0001f527"),
        ("Tamamlanan", tamamlanan, "#10b981", "\u2705"),
        ("Bekleyen", bekleyen, "#f59e0b", "\u23f3"),
        ("Uygunsuz", uygunsuz, "#ef4444", "\u274c"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Sunburst: Kategori -> Durum (Excel stili) ----
    kalem_map = {k.kalem_kodu: k for k in store.load_objects("bakim_kalemleri")}
    kat_counts: dict[str, float] = {}
    kat_durum: dict[str, dict[str, float]] = {}
    for k in kayitlar:
        kalem = kalem_map.get(k.get("kalem_kodu", ""))
        kat = kalem.kategori if kalem else "Diğer"
        dur = k.get("durum", "Planlandi")
        kat_counts[kat] = kat_counts.get(kat, 0) + 1
        kat_durum.setdefault(kat, {})
        kat_durum[kat][dur] = kat_durum[kat].get(dur, 0) + 1
    kat_durum_list = {k: [(d, c) for d, c in v.items()] for k, v in kat_durum.items()}

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Kategori / Durum Dagilimi (Sunburst)", "#4472C4")
        if kat_counts:
            st.markdown(
                ReportStyler.sunburst_chart_svg(kat_counts, kat_durum_list, size=300,
                                                 title="Kategori / Durum"),
                unsafe_allow_html=True)
    with c2:
        styled_section("Uyum Orani", "#4472C4")
        uyum_data = {"Tamamlandı": tamamlanan, "Bekleyen": bekleyen, "Uygunsuz": uygunsuz}
        st.markdown(ReportStyler.donut_chart_svg(uyum_data,
                                                  colors=["#4472C4", "#FFC000", "#ED7D31"], size=155),
                    unsafe_allow_html=True)
        if kat_counts:
            st.markdown(ReportStyler.horizontal_bar_html(kat_counts, "#4472C4", max_width_px=300), unsafe_allow_html=True)

    # ---- Sonuc Dagilimi ----
    styled_section("Sonuc Dagilimi", "#8b5cf6")
    sonuc_counts = Counter(k.get("sonuc", "-") for k in kayitlar if k.get("sonuc"))
    if sonuc_counts:
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(ReportStyler.donut_chart_svg(dict(sonuc_counts),
                                                      colors=["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#10b981"], size=155),
                        unsafe_allow_html=True)
        with sc2:
            st.markdown(ReportStyler.horizontal_bar_html(dict(sonuc_counts), "#ED7D31", max_width_px=300), unsafe_allow_html=True)

    # ---- Detay Tablosu ----
    styled_section("Bakım Detay Tablosu", "#94A3B8")
    rows = []
    for k in kayitlar:
        kalem = kalem_map.get(k.get("kalem_kodu", ""))
        rows.append({
            "Kalem Kodu": k.get("kalem_kodu", ""),
            "Kalem Adi": kalem.kalem_adi if kalem else "",
            "Kategori": kalem.kategori if kalem else "",
            "Durum": k.get("durum", ""),
            "Sonuc": k.get("sonuc", "-"),
            "Plan Tarihi": k.get("plan_tarihi", ""),
            "Yapildi": k.get("yapildi_tarihi", "-")[:10] if k.get("yapildi_tarihi") else "-",
        })
    if rows:
        st.markdown(ReportStyler.colored_table_html(pd.DataFrame(rows), "#0d9488"), unsafe_allow_html=True)

    # Uyum ozetini banner olarak goster
    styled_info_banner(f"Genel Uyum Orani: %{uyum_orani:.0f} ({tamamlanan}/{toplam})", "success" if uyum_orani >= 80 else "warning")

    # ---- PDF ----
    st.divider()
    if st.button("PBK Raporu PDF", type="primary", key="des_rp_pdf"):
        pdf = _generate_pbk_rapor_pdf(store, kayitlar, kalem_map, start, end)
        if pdf:
            st.download_button("PDF İndir", data=pdf, file_name=f"Destek_PBK_Rapor_{start}_{end}.pdf",
                               mime="application/pdf", key="des_rp_dl")


def _generate_pbk_rapor_pdf(store: DestekDataStore, kayitlar: list, kalem_map: dict,
                              start: date, end: date) -> bytes | None:
    try:
        info = get_institution_info()
        gen = ReportPDFGenerator("Periyodik Bakım (PBK) Raporu",
                                  f"Dönem: {start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}")
        gen.add_header(kurum_adi=info.get("name", ""))

        toplam = len(kayitlar)
        tamamlanan = sum(1 for k in kayitlar if k.get("durum") == "Tamamlandı")
        uygunsuz = sum(1 for k in kayitlar if k.get("durum") == "Uygunsuz")

        gen.add_section("Temel Göstergeler")
        gen.add_metrics([
            ("Toplam", toplam, "#2563eb"),
            ("Tamamlanan", tamamlanan, "#10b981"),
            ("Uygunsuz", uygunsuz, "#ef4444"),
            ("Uyum %", f"{round(tamamlanan / toplam * 100) if toplam else 0}", "#0d9488"),
        ])
        gen.add_spacer(0.4)

        # Uyum donut
        gen.add_section("Uyum Oranı")
        gen.add_donut_chart({"Tamamlandı": tamamlanan, "Bekleyen": toplam - tamamlanan - uygunsuz, "Uygunsuz": uygunsuz},
                            "Bakım Uyum Durumu", ["#4472C4", "#FFC000", "#ED7D31"])

        # Kategori bazında bar
        kat_counts: dict[str, float] = {}
        for k in kayitlar:
            kalem = kalem_map.get(k.get("kalem_kodu", ""))
            kat = kalem.kategori if kalem else "Diğer"
            kat_counts[kat] = kat_counts.get(kat, 0) + 1
        if kat_counts:
            gen.add_section("Kategori Bazında Bakım")
            gen.add_bar_chart(kat_counts, "Kategori Bazında Bakım Sayısı", "#4472C4")

        # Detay tablo
        gen.add_section("Bakım Detay Tablosu")
        rows = []
        for k in kayitlar:
            kalem = kalem_map.get(k.get("kalem_kodu", ""))
            rows.append({
                "Kod": k.get("kalem_kodu", ""),
                "Kalem": kalem.kalem_adi if kalem else "",
                "Durum": k.get("durum", ""),
                "Sonuç": k.get("sonuc", "-"),
                "Tarih": k.get("plan_tarihi", ""),
            })
        if rows:
            gen.add_table(pd.DataFrame(rows))

        return gen.generate()
    except Exception:
        return None


# ============================================================
# TAB 8: AYARLAR
# ============================================================

def _render_ayarlar(store: DestekDataStore):
    sub = st.tabs([
        "🏢 Hizmet Alanlari", "📂 Alt Kategoriler", "⏱️ SLA Ayarlari",
        "📋 Denetim Formlari", "🔧 PBK Kalemleri", "⚙️ Genel Ayarlar",
    ])

    with sub[0]:
        _render_ayar_hizmet_alanlari(store)
    with sub[1]:
        _render_ayar_alt_kategoriler(store)
    with sub[2]:
        _render_ayar_sla(store)
    with sub[3]:
        _render_ayar_denetim(store)
    with sub[4]:
        _render_ayar_pbk(store)
    with sub[5]:
        _render_ayar_genel(store)


def _render_ayar_hizmet_alanlari(store: DestekDataStore):
    styled_section("Hizmet Alanlari", "#2563eb")
    alanlar = store.load_objects("hizmet_alanlari")
    if alanlar:
        rows = []
        for ha in alanlar:
            rows.append({
                "Kod": ha.alan_kodu,
                "Alan Adi": ha.alan_adi,
                "Aktif": ha.aktif_durumu,
                "Sorumlu Rol": ha.varsayilan_sorumlu_rol,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    styled_section("Yeni Hizmet Alani", "#10b981")
    c1, c2, c3 = st.columns(3)
    with c1:
        kod = st.text_input("Kod (3 harf)", key="des_ay_ha_kod")
    with c2:
        adi = st.text_input("Alan Adi", key="des_ay_ha_adi")
    with c3:
        rol = st.text_input("Varsayilan Sorumlu Rol", key="des_ay_ha_rol")

    if st.button("Hizmet Alani Ekle", key="des_ay_ha_btn"):
        if kod.strip() and adi.strip():
            ha = HizmetAlani(alan_kodu=kod.strip().upper(), alan_adi=adi.strip(),
                             varsayilan_sorumlu_rol=rol.strip())
            store.upsert("hizmet_alanlari", ha)
            st.success(f"Hizmet alani eklendi: {kod}")
            st.rerun()


def _render_ayar_alt_kategoriler(store: DestekDataStore):
    styled_section("Alt Kategoriler", "#8b5cf6")
    alan_map = _alan_adi_map(store)
    filtre = st.selectbox("Hizmet Alani Filtre", ["Tümü"] + list(alan_map.values()), key="des_ay_ak_filtre")
    alan_kodu_rev = {v: k for k, v in alan_map.items()}

    alt_kats = store.load_objects("alt_kategoriler")
    if filtre != "Tümü":
        ak = alan_kodu_rev.get(filtre, "")
        alt_kats = [a for a in alt_kats if a.alan_kodu == ak]

    if alt_kats:
        rows = []
        for a in alt_kats:
            rows.append({
                "Alan": a.alan_kodu,
                "Kod": a.alt_kategori_kodu,
                "Adi": a.alt_kategori_adi,
                "Aktif": "Evet" if a.aktif_mi else "Hayir",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    styled_section("Yeni Alt Kategori", "#10b981")
    c1, c2, c3 = st.columns(3)
    with c1:
        alan_sec = st.selectbox("Hizmet Alani", list(alan_map.values()), key="des_ay_ak_alan")
    with c2:
        ak_kod = st.text_input("Kod (TEM-08 gibi)", key="des_ay_ak_kod")
    with c3:
        ak_adi = st.text_input("Alt Kategori Adi", key="des_ay_ak_adi")

    if st.button("Alt Kategori Ekle", key="des_ay_ak_btn"):
        if ak_kod.strip() and ak_adi.strip():
            ak = AltKategori(
                alan_kodu=alan_kodu_rev.get(alan_sec, ""),
                alt_kategori_kodu=ak_kod.strip().upper(),
                alt_kategori_adi=ak_adi.strip(),
            )
            store.upsert("alt_kategoriler", ak)
            st.success(f"Alt kategori eklendi: {ak_kod}")
            st.rerun()


def _render_ayar_sla(store: DestekDataStore):
    styled_section("SLA Ayarlari", "#f59e0b")
    sla_list = store.load_objects("sla_ayarlar")

    if sla_list:
        rows = []
        for s in sla_list:
            mudahale_saat = s.hedef_mudahale_dk / 60
            cozum_saat = s.hedef_cozum_dk / 60
            rows.append({
                "Öncelik": s.oncelik,
                "Mudahale": f"{mudahale_saat:.0f} saat" if mudahale_saat >= 1 else f"{s.hedef_mudahale_dk} dk",
                "Cozum": f"{cozum_saat:.0f} saat" if cozum_saat >= 1 else f"{s.hedef_cozum_dk} dk",
                "Eskalasyon": f"{s.eskalasyon_dk / 60:.0f} saat",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_ayar_denetim(store: DestekDataStore):
    styled_section("Denetim Formlari ve Maddeleri", "#0d9488")
    formlar = store.load_objects("denetim_formlari")

    if formlar:
        for form in formlar:
            with st.expander(f"{form.form_kodu} - {form.form_adi}"):
                st.markdown(f"**Periyot:** {form.periyot} | **Olceg:** {form.puanlama_olcegi}")
                maddeler = [m for m in store.load_objects("denetim_maddeleri")
                            if m.form_kodu == form.form_kodu]
                maddeler.sort(key=lambda m: (m.bolum_no, m.madde_no))
                if maddeler:
                    rows = []
                    for m in maddeler:
                        rows.append({
                            "Bolum": f"{m.bolum_no}. {m.bolum_adi}",
                            "No": m.madde_no,
                            "Madde": m.madde_metni,
                            "Kritik": "EVET" if m.kritik_mi else "",
                            "Aktif": "Evet" if m.aktif_mi else "Hayir",
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_ayar_pbk(store: DestekDataStore):
    styled_section("PBK Bakım Kalemleri", "#2563eb")
    kalemler = store.load_objects("bakim_kalemleri")

    if kalemler:
        rows = []
        for k in kalemler:
            rows.append({
                "Kod": k.kalem_kodu,
                "Kalem": k.kalem_adi,
                "Kategori": k.kategori,
                "Periyot": k.periyot,
                "Yürütucu": k.varsayilan_yurutucu_tipi,
                "Kanit": "Evet" if k.kanit_zorunlu_mu else "Hayir",
                "Aktif": "Evet" if k.aktif_mi else "Hayir",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_ayar_genel(store: DestekDataStore):
    styled_section("Genel Ayarlar", "#64748b")
    ayarlar = store.load_objects("destek_ayarlar")

    if ayarlar:
        for a in ayarlar:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{a.ayar_kodu}**: {a.aciklama}")
            with c2:
                new_val = st.text_input("Deger", value=a.deger, key=f"des_ay_g_{a.ayar_kodu}")
                if new_val != a.deger:
                    a.deger = new_val
                    store.upsert("destek_ayarlar", a)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def render_destek_hizmetleri():
    """DES-01 Destek Hizmetleri Takip modulu giris noktasi."""
    _inject_des_css()
    styled_header(
        "Destek Hizmetleri Takip",
        "DES-01 Talep, Denetim ve Bakım Yönetim Sistemi",
        "\U0001f6e0"
    )

    render_smarti_welcome("destek_hizmetleri")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("destek_hizmetleri_egitim_yili")

    # -- Tab Gruplama (25 tab -> 4 grup) --
    _GRP_33990 = {
        "📋 Grup A": [("📊 Dashboard", 0), ("🎫 Talepler", 1), ("🔄 Periyodik İşler", 2), ("📋 Denetimler", 3), ("🔧 Bakım Yönetimi", 4), ("🏢 Firma Havuzu", 5), ("📦 Tedarikçiler", 6)],
        "📊 Grup B": [("📈 Raporlar", 7), ("📊 SLA Cockpit", 8), ("🗺️ Tesis Haritası", 9), ("🏆 Memnuniyet", 10), ("🧠 Kök Neden", 11), ("📱 Saha Ekibi", 12), ("🔄 Eskalasyon", 13)],
        "🔧 Grup C": [("📊 Prediktif Bakım", 14), ("🎮 Gamification", 15), ("🔌 Entegrasyon Hub", 16), ("🧬 Destek DNA", 17), ("🎯 Kaynak Planlama", 18), ("📡 Komuta Merkezi", 19), ("📋 Denetim Uyum", 20)],
        "📈 Grup D": [("🌍 Benchmark", 21), ("🤖 AI Operasyon", 22), ("⚙️ Ayarlar", 23), ("🤖 Smarti", 24)],
    }
    _sg_33990 = st.radio("", list(_GRP_33990.keys()), horizontal=True, label_visibility="collapsed", key="rg_33990")
    _gt_33990 = _GRP_33990[_sg_33990]
    _aktif_idx_33990 = set(t[1] for t in _gt_33990)
    _tab_names_33990 = [t[0] for t in _gt_33990]
    tabs = st.tabs(_tab_names_33990)
    _tab_real_33990 = {idx: t for idx, t in zip((t[1] for t in _gt_33990), tabs)}

    store = _get_destek_store()

    if 0 in _aktif_idx_33990:
      with _tab_real_33990[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_33990:
      with _tab_real_33990[1]:
        _render_talepler(store)
    if 2 in _aktif_idx_33990:
      with _tab_real_33990[2]:
        _render_periyodik_isler(store)
    if 3 in _aktif_idx_33990:
      with _tab_real_33990[3]:
        _render_denetimler(store)
    if 4 in _aktif_idx_33990:
      with _tab_real_33990[4]:
        _render_pbk(store)
    if 5 in _aktif_idx_33990:
      with _tab_real_33990[5]:
        _render_firma_havuzu(store)
    if 6 in _aktif_idx_33990:
      with _tab_real_33990[6]:
        _render_tedarikciler(store)
    if 7 in _aktif_idx_33990:
      with _tab_real_33990[7]:
        _render_raporlar(store)
    if 8 in _aktif_idx_33990:
      with _tab_real_33990[8]:
        try:
            from views._destek_yeni_ozellikler import render_sla_cockpit
            render_sla_cockpit(store)
        except Exception as _e:
            st.error(f"SLA Cockpit yuklenemedi: {_e}")
    if 9 in _aktif_idx_33990:
      with _tab_real_33990[9]:
        try:
            from views._destek_yeni_ozellikler import render_tesis_haritasi
            render_tesis_haritasi(store)
        except Exception as _e:
            st.error(f"Tesis Haritasi yuklenemedi: {_e}")
    if 10 in _aktif_idx_33990:
      with _tab_real_33990[10]:
        try:
            from views._destek_yeni_ozellikler import render_memnuniyet_endeksi
            render_memnuniyet_endeksi(store)
        except Exception as _e:
            st.error(f"Memnuniyet Endeksi yuklenemedi: {_e}")
    if 11 in _aktif_idx_33990:
      with _tab_real_33990[11]:
        try:
            from views._destek_super_features import render_kok_neden
            render_kok_neden(store)
        except Exception as _e:
            st.error(f"Kok Neden yuklenemedi: {_e}")
    if 12 in _aktif_idx_33990:
      with _tab_real_33990[12]:
        try:
            from views._destek_super_features import render_saha_ekibi
            render_saha_ekibi(store)
        except Exception as _e:
            st.error(f"Saha Ekibi yuklenemedi: {_e}")
    if 13 in _aktif_idx_33990:
      with _tab_real_33990[13]:
        try:
            from views._destek_super_features import render_eskalasyon_motoru
            render_eskalasyon_motoru(store)
        except Exception as _e:
            st.error(f"Eskalasyon Motoru yuklenemedi: {_e}")
    if 14 in _aktif_idx_33990:
      with _tab_real_33990[14]:
        try:
            from views._destek_mega_features import render_prediktif_bakim
            render_prediktif_bakim(store)
        except Exception as _e:
            st.error(f"Prediktif Bakim yuklenemedi: {_e}")
    if 15 in _aktif_idx_33990:
      with _tab_real_33990[15]:
        try:
            from views._destek_mega_features import render_gamification
            render_gamification(store)
        except Exception as _e:
            st.error(f"Gamification yuklenemedi: {_e}")
    if 16 in _aktif_idx_33990:
      with _tab_real_33990[16]:
        try:
            from views._destek_mega_features import render_entegrasyon_hub
            render_entegrasyon_hub(store)
        except Exception as _e:
            st.error(f"Entegrasyon Hub yuklenemedi: {_e}")
    if 17 in _aktif_idx_33990:
      with _tab_real_33990[17]:
        try:
            from views._destek_zirve_features import render_destek_dna
            render_destek_dna(store)
        except Exception as _e:
            st.error(f"Destek DNA yuklenemedi: {_e}")
    if 18 in _aktif_idx_33990:
      with _tab_real_33990[18]:
        try:
            from views._destek_zirve_features import render_kaynak_planlama
            render_kaynak_planlama(store)
        except Exception as _e:
            st.error(f"Kaynak Planlama yuklenemedi: {_e}")
    if 19 in _aktif_idx_33990:
      with _tab_real_33990[19]:
        try:
            from views._destek_zirve_features import render_komuta_merkezi
            render_komuta_merkezi(store)
        except Exception as _e:
            st.error(f"Komuta Merkezi yuklenemedi: {_e}")
    if 20 in _aktif_idx_33990:
      with _tab_real_33990[20]:
        try:
            from views._destek_final_features import render_denetim_uyumluluk
            render_denetim_uyumluluk(store)
        except Exception as _e:
            st.error(f"Denetim Uyumluluk yuklenemedi: {_e}")
    if 21 in _aktif_idx_33990:
      with _tab_real_33990[21]:
        try:
            from views._destek_final_features import render_benchmark_merkezi
            render_benchmark_merkezi(store)
        except Exception as _e:
            st.error(f"Benchmark Merkezi yuklenemedi: {_e}")
    if 22 in _aktif_idx_33990:
      with _tab_real_33990[22]:
        try:
            from views._destek_final_features import render_ai_operasyon
            render_ai_operasyon(store)
        except Exception as _e:
            st.error(f"AI Operasyon yuklenemedi: {_e}")
    if 23 in _aktif_idx_33990:
      with _tab_real_33990[23]:
        _render_ayarlar(store)
    if 24 in _aktif_idx_33990:
      with _tab_real_33990[24]:
        def _des_smarti_context():
            try:
                t = len(store.load_list("tickets"))
                g = len(store.load_list("periyodik_gorevler"))
                d = len(store.load_list("denetimler"))
                b = len(store.load_list("bakim_kayitlari"))
                return f"Toplam talep: {t}, Periyodik gorev: {g}, Denetim: {d}, Bakım kaydı: {b}"
            except Exception:
                return ""
        render_smarti_chat("destek_hizmetleri", data_context_fn=_des_smarti_context)
