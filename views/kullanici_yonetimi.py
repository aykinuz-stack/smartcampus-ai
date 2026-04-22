"""
Kullanıcı Yönetimi Modulu
=========================
IK entegreli kullanici olusturma, sifre yonetimi,
modul yetki atama ve kullanıcı işlemleri.
Sadece Yonetici rolundeki kullanicilar erisebilir.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any

import streamlit as st

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("kurum_hizmetleri")
except Exception:
    pass
from utils.auth import (
    AuthManager, get_all_users, add_user, delete_user,
    reset_password, toggle_user_active,
    generate_username, generate_password,
    update_user_modules, TUM_MODULLER, ROLES,
    MODUL_GRUPLARI, ROL_VARSAYILAN_MODULLER, get_role_default_modules,
)
from utils.shared_data import (
    get_ik_position_names,
    load_ik_active_employees,
    get_sinif_sube_listesi,
    get_student_display_options,
    load_shared_students,
)
from utils.report_utils import ReportStyler, get_institution_info
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome


# ============================================================
# YARDIMCI
# ============================================================

def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _get_current_user() -> dict:
    return AuthManager.get_current_user()


# ============================================================
# CSS STILLERI
# ============================================================

def _inject_ky_css():
    inject_common_css("ky")
    st.markdown("""
    <style>
    /* Rol radio butonlari okunabilirlik */
    div[data-testid="stRadio"] label {
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: #7c3aed !important;
        background: rgba(124, 58, 237, 0.15) !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
        border-color: #a78bfa !important;
        color: #fff !important;
    }
    div[data-testid="stRadio"] p {
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# YENI KULLANICI OLUSTURMA
# ============================================================

def _render_yeni_kullanici():
    """Rol bazli kullanici olusturma formu — Personel (IK), Ogrenci ve Veli destegi."""

    # ---- 1. Rol Secimi (en ustte) ----
    styled_section("Kullanıcı Türü Seçin", "#7c3aed")
    rol = st.radio("Rol", ROLES, horizontal=True, key="ky_rol_sec")

    st.markdown("")

    # Ortak degiskenler
    ad = ""
    soyad = ""
    cinsiyet = "Erkek"
    unvan = ""
    secili_emp: dict = {}
    secili_subeler: list[str] = []
    secili_ogrenci_id = ""
    secili_ogrenci_adi = ""
    secili_sinif = ""
    secili_sube = ""
    source_type = ""
    source_id = ""
    extra_fields: dict[str, Any] = {}

    # ================================================================
    # A) PERSONEL — Yonetici / Ogretmen / Calisan
    # ================================================================
    if rol in ("Yonetici", "Ogretmen", "Calisan"):
        styled_section("IK'dan Kişi Seç", "#2563eb")

        positions = get_ik_position_names()
        c1, c2 = st.columns(2)
        with c1:
            sec_pozisyon = st.selectbox(
                "Pozisyon Filtresi (Opsiyonel)",
                ["-- Tümü --"] + positions,
                key="ky_pozisyon",
            )

        employees = load_ik_active_employees()
        if sec_pozisyon != "-- Tümü --":
            employees = [e for e in employees if e.get("position_name") == sec_pozisyon]

        calisan_secenekleri: dict[str, dict] = {}
        for e in sorted(employees, key=lambda x: f"{x.get('ad', '')} {x.get('soyad', '')}"):
            tam_ad = f"{e.get('ad', '')} {e.get('soyad', '')}".strip()
            if not tam_ad:
                continue
            pos = e.get("position_name", "")
            label = f"{tam_ad} - {pos}" if pos else tam_ad
            calisan_secenekleri[label] = e

        with c2:
            secili_calisan_label = st.selectbox(
                "Çalışan Seç",
                ["-- Seçim yapın --"] + list(calisan_secenekleri.keys()),
                key="ky_calisan",
            )

        secili_emp = (
            calisan_secenekleri.get(secili_calisan_label, {})
            if secili_calisan_label != "-- Seçim yapın --"
            else {}
        )

        styled_section("Kullanıcı Bilgileri")
        k1, k2 = st.columns(2)
        with k1:
            ad = st.text_input("Ad", value=secili_emp.get("ad", ""), key="ky_ad")
        with k2:
            soyad = st.text_input("Soyad", value=secili_emp.get("soyad", ""), key="ky_soyad")

        # Unvan secimi
        unvan_secenekleri = [
            "Kurucu", "Kurucu Temsilcisi", "Genel Mudur",
            "Genel Mudur Yardimcisi", "Kampus Muduru", "Birim Muduru",
            "Birim Mudur Yardimcisi", "Öğretmen", "Halkla Iliskiler",
            "Idari Isler Muduru",
        ]
        k_u1, k_u2 = st.columns(2)
        with k_u1:
            emp_pos = secili_emp.get("position_name", "") if secili_emp else ""
            default_unvan_idx = 0
            secim_listesi = ["-- Seçin --"] + unvan_secenekleri + ["Yeni Ekle"]
            if emp_pos and emp_pos in unvan_secenekleri:
                default_unvan_idx = secim_listesi.index(emp_pos)
            unvan_sec = st.selectbox("Unvan / Pozisyon", secim_listesi,
                                     index=default_unvan_idx, key="ky_unvan")
        with k_u2:
            if unvan_sec == "Yeni Ekle":
                unvan = st.text_input("Yeni Unvan Girin", key="ky_yeni_unvan")
            elif unvan_sec != "-- Seçin --":
                unvan = unvan_sec
                st.text_input("Seçilen Unvan", value=unvan, disabled=True, key="ky_unvan_goster")
            else:
                unvan = emp_pos
                if unvan:
                    st.text_input("IK Pozisyonu", value=unvan, disabled=True, key="ky_unvan_ik")

        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadin"], key="ky_cinsiyet_p")

        if secili_emp:
            source_type = "ik_employee"
            source_id = secili_emp.get("id", "")
            extra_fields["position_name"] = secili_emp.get("position_name", "")

        # Ogretmen sinif/sube atamasi
        if rol == "Ogretmen":
            sinif_sube_data = get_sinif_sube_listesi()
            sinif_sube_listesi = sinif_sube_data.get("sinif_sube", [])
            styled_section("Sınıf / Şube Ataması", "#2563eb")
            st.caption("Öğretmenin sorumlu olduğu sınıf ve şubeleri seçin.")
            if sinif_sube_listesi:
                secili_subeler = st.multiselect(
                    "Sorumlu Sınıf/Şubeler", sinif_sube_listesi, key="ky_subeler")
            else:
                styled_info_banner(
                    "Henüz sınıf/şube verisi yok. İletişim > Sınıf Listeleri'nden öğrenci ekleyin.",
                    "warning")

    # ================================================================
    # B) OGRENCI — Sinif Listeleri'nden ogrenci sec
    # ================================================================
    elif rol == "Ogrenci":
        styled_section("Sınıf Listeleri'nden Öğrenci Seç", "#2563eb")
        styled_info_banner(
            "Öğrenci verileri Kurumsal Organizasyon > İletişim > Sınıf Listeleri'nden alınmaktadır.",
            "info", "📋")

        sinif_sube_data = get_sinif_sube_listesi()
        siniflar = sinif_sube_data.get("siniflar", [])
        sinif_sube_listesi = sinif_sube_data.get("sinif_sube", [])

        if not siniflar:
            styled_info_banner(
                "Henüz sınıf/şube verisi yok. Önce İletişim > Sınıf Listeleri'nden öğrenci ekleyin.",
                "warning")
            return

        o1, o2 = st.columns(2)
        with o1:
            secili_sinif = st.selectbox("Sınıf", ["-- Seçin --"] + siniflar, key="ky_ogr_sinif")
        with o2:
            uygun_subeler: list[str] = []
            if secili_sinif and secili_sinif != "-- Seçin --":
                uygun_subeler = sorted(set(
                    ss.split("/")[1] for ss in sinif_sube_listesi
                    if ss.startswith(f"{secili_sinif}/")
                ))
            secili_sube = st.selectbox("Şube", ["-- Seçin --"] + uygun_subeler, key="ky_ogr_sube")

        if secili_sinif != "-- Seçin --" and secili_sube != "-- Seçin --":
            ogr_opts = get_student_display_options(
                sinif_filter=secili_sinif, sube_filter=secili_sube, include_empty=True)
            secili_ogr_label = st.selectbox("Öğrenci Seç", list(ogr_opts.keys()), key="ky_ogr_sec")

            if secili_ogr_label and secili_ogr_label != "-- Secim yapin --":
                ogr = ogr_opts[secili_ogr_label]
                ad = ogr.get("ad", "")
                soyad = ogr.get("soyad", "")
                secili_ogrenci_id = ogr.get("id", "")
                secili_ogrenci_adi = f"{ad} {soyad}".strip()
                cinsiyet = ogr.get("cinsiyet", "Erkek")
                source_type = "student"
                source_id = secili_ogrenci_id

                # Ogrenci bilgi karti
                numara = ogr.get("numara", "-")
                st.markdown(
                    f'<div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;'
                    f'padding:14px 18px;margin:10px 0;">'
                    f'<b style="color:#1d4ed8;">Seçilen Öğrenci:</b> {secili_ogrenci_adi}<br>'
                    f'<span style="color:#475569;">Sınıf: {secili_sinif}/{secili_sube} · '
                    f'No: {numara}</span></div>',
                    unsafe_allow_html=True,
                )

        styled_section("Kullanıcı Bilgileri")
        k1, k2 = st.columns(2)
        with k1:
            ad = st.text_input("Ad", value=ad, key="ky_ogr_ad")
        with k2:
            soyad = st.text_input("Soyad", value=soyad, key="ky_ogr_soyad")
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadin"],
                                index=0 if cinsiyet == "Erkek" else 1,
                                key="ky_cinsiyet_o")

    # ================================================================
    # C) VELI — Sinif Listeleri'nden veli sec
    # ================================================================
    elif rol == "Veli":
        styled_section("Sınıf Listeleri'nden Veli Seç", "#ec4899")
        styled_info_banner(
            "Veli verileri Kurumsal Organizasyon > İletişim > Sınıf Listeleri'ndeki öğrenci kayıtlarından alınmaktadır.",
            "info", "👨‍👩‍👧")

        sinif_sube_data = get_sinif_sube_listesi()
        siniflar = sinif_sube_data.get("siniflar", [])
        sinif_sube_listesi = sinif_sube_data.get("sinif_sube", [])

        if not siniflar:
            styled_info_banner(
                "Henüz sınıf/şube verisi yok. Önce İletişim > Sınıf Listeleri'nden öğrenci ekleyin.",
                "warning")
            return

        v1, v2 = st.columns(2)
        with v1:
            secili_sinif = st.selectbox("Sınıf", ["-- Seçin --"] + siniflar, key="ky_veli_sinif")
        with v2:
            uygun_subeler_v: list[str] = []
            if secili_sinif and secili_sinif != "-- Seçin --":
                uygun_subeler_v = sorted(set(
                    ss.split("/")[1] for ss in sinif_sube_listesi
                    if ss.startswith(f"{secili_sinif}/")
                ))
            secili_sube = st.selectbox("Şube", ["-- Seçin --"] + uygun_subeler_v, key="ky_veli_sube")

        if secili_sinif != "-- Seçin --" and secili_sube != "-- Seçin --":
            ogr_opts = get_student_display_options(
                sinif_filter=secili_sinif, sube_filter=secili_sube, include_empty=True)
            secili_ogr_label = st.selectbox(
                "Öğrenci (Velisi olduğu)", list(ogr_opts.keys()), key="ky_veli_ogrenci")

            if secili_ogr_label and secili_ogr_label != "-- Secim yapin --":
                ogr = ogr_opts[secili_ogr_label]
                secili_ogrenci_id = ogr.get("id", "")
                ogr_ad = ogr.get("ad", "")
                ogr_soyad = ogr.get("soyad", "")
                secili_ogrenci_adi = f"{ogr_ad} {ogr_soyad}".strip()

                # Veli bilgilerini ogrenci kaydından al
                veli_adi = ogr.get("veli_adi", "")
                anne_adi = f'{ogr.get("anne_adi", "")} {ogr.get("anne_soyadi", "")}'.strip()
                baba_adi = f'{ogr.get("baba_adi", "")} {ogr.get("baba_soyadi", "")}'.strip()
                veli_tel = ogr.get("veli_telefon", "") or ogr.get("anne_telefon", "") or ogr.get("baba_telefon", "")

                # Veli secimi
                veli_secenekleri = ["-- Seçin --"]
                if veli_adi:
                    veli_secenekleri.append(f"Veli: {veli_adi}")
                if anne_adi:
                    veli_secenekleri.append(f"Anne: {anne_adi}")
                if baba_adi:
                    veli_secenekleri.append(f"Baba: {baba_adi}")
                veli_secenekleri.append("Manuel Giriş")

                secili_veli = st.selectbox("Veli Seç", veli_secenekleri, key="ky_veli_kisi")

                if secili_veli and secili_veli not in ("-- Seçin --", "Manuel Giriş"):
                    # "Anne: Ayse Yilmaz" -> "Ayse Yilmaz"
                    veli_tam = secili_veli.split(": ", 1)[1] if ": " in secili_veli else secili_veli
                    parts = veli_tam.rsplit(" ", 1)
                    ad = parts[0] if parts else veli_tam
                    soyad = parts[1] if len(parts) > 1 else ""
                    source_type = "veli"
                    source_id = secili_ogrenci_id

                    st.markdown(
                        f'<div style="background:#fdf2f8;border:1px solid #fbcfe8;border-radius:10px;'
                        f'padding:14px 18px;margin:10px 0;">'
                        f'<b style="color:#be185d;">Seçilen Veli:</b> {veli_tam}<br>'
                        f'<span style="color:#475569;">Öğrenci: {secili_ogrenci_adi} · '
                        f'Sınıf: {secili_sinif}/{secili_sube}'
                        f'{f" · Tel: {veli_tel}" if veli_tel else ""}</span></div>',
                        unsafe_allow_html=True,
                    )

        styled_section("Kullanıcı Bilgileri")
        k1, k2 = st.columns(2)
        with k1:
            ad = st.text_input("Ad", value=ad, key="ky_veli_ad")
        with k2:
            soyad = st.text_input("Soyad", value=soyad, key="ky_veli_soyad")
        cinsiyet = st.selectbox("Cinsiyet", ["Erkek", "Kadin"], key="ky_cinsiyet_v")

    # ================================================================
    # ORTAK: Modul yetkileri + Olustur butonu
    # ================================================================
    styled_section("Modül Yetkileri", "#10b981")
    st.caption("Boş bırakılırsa kullanıcı tüm modüllere erişebilir.")

    # Checkbox grid ile modul secimi
    _mod_cols = st.columns(3)
    secili_moduller: list[str] = []
    for i, mod in enumerate(TUM_MODULLER):
        with _mod_cols[i % 3]:
            if st.checkbox(mod, key=f"ky_mod_{i}", value=False):
                secili_moduller.append(mod)

    if ad and soyad:
        existing_usernames = {u["username"] for u in get_all_users()}
        oneri_username = generate_username(ad, soyad, existing_usernames)
        st.info(f"Önerilen kullanıcı adı: **{oneri_username}**")

    if st.button("Kullanıcı Oluştur", type="primary", use_container_width=True, key="ky_olustur"):
        if not ad or not soyad:
            st.error("Ad ve soyad gereklidir.")
            return

        existing_usernames = {u["username"] for u in get_all_users()}
        username = generate_username(ad, soyad, existing_usernames)
        password = generate_password()

        new_user: dict[str, Any] = {
            "username": username,
            "password_hash": hashlib.sha256(password.encode()).hexdigest(),
            "name": f"{ad} {soyad}",
            "role": rol,
            "cinsiyet": cinsiyet,
            "unvan": unvan,
            "is_active": True,
            "created_at": _now(),
        }

        if source_type:
            new_user["source_type"] = source_type
        if source_id:
            new_user["source_id"] = source_id
        for k, v in extra_fields.items():
            new_user[k] = v

        if secili_moduller:
            new_user["izinli_moduller"] = secili_moduller

        # Sinif/Sube bilgisi
        if rol == "Ogretmen" and secili_subeler:
            new_user["subeler"] = secili_subeler
        if secili_sinif and secili_sinif != "-- Seçin --":
            new_user["sinif"] = secili_sinif
        if secili_sube and secili_sube != "-- Seçin --":
            new_user["sube"] = secili_sube
        if secili_ogrenci_id:
            new_user["ogrenci_id"] = secili_ogrenci_id
            new_user["ogrenci_adi"] = secili_ogrenci_adi

        add_user(new_user)

        st.success("Kullanıcı başarıyla oluşturuldu!")

        # Bilgi karti
        sinif_bilgi = ""
        if secili_sinif and secili_sinif != "-- Seçin --":
            sinif_bilgi = f'<b>Sınıf/Şube:</b> {secili_sinif}/{secili_sube}<br>'
        ogr_bilgi = ""
        if secili_ogrenci_adi:
            lbl = "Bağlı Öğrenci" if rol == "Veli" else "Öğrenci"
            ogr_bilgi = f'<b>{lbl}:</b> {secili_ogrenci_adi}<br>'
        sube_bilgi = ""
        if secili_subeler:
            sube_bilgi = f'<b>Sorumlu Şubeler:</b> {", ".join(secili_subeler)}<br>'

        st.markdown(
            f'<div style="background:#f0fdf4;border:2px solid #10b981;border-radius:12px;'
            f'padding:16px;margin:10px 0;">'
            f'<div style="font-weight:700;color:#10b981;margin-bottom:8px;">Giriş Bilgileri</div>'
            f'<div style="font-size:15px;color:#94A3B8;">'
            f'<b>Kullanıcı Adı:</b> {username}<br>'
            f'<b>Şifre:</b> {password}<br>'
            f'<b>Rol:</b> {rol}<br>'
            f'{f"<b>Ünvan:</b> {unvan}<br>" if unvan else ""}'
            f'{sinif_bilgi}{ogr_bilgi}{sube_bilgi}'
            f'</div>'
            f'<div style="color:#ef4444;font-size:12px;margin-top:8px;">'
            f'Bu bilgileri kaydedin — şifre tekrar görüntülenemez!</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# KULLANICI LISTESI
# ============================================================

def _render_grup_yetkileri():
    """Rol bazlı toplu yetki yönetimi — Yönetici/Öğretmen/Veli/Öğrenci gruplarına toplu modül atama."""
    styled_section("Grup Bazlı Yetki Yönetimi")
    st.caption("Bir rol seçin → modül yetkilerini belirleyin → o roldeki TÜM kullanıcılara uygulayın.")

    users = get_all_users(tenant_scoped=True)
    rol_secimi = st.selectbox("Rol Seçin", ROLES, key="gy_rol_sec")

    # Bu roldeki kullanıcılar
    rol_users = [u for u in users if u.get("role") == rol_secimi]
    st.info(f"**{rol_secimi}** rolünde **{len(rol_users)}** kullanıcı var.")

    # Mevcut varsayılan modüller
    mevcut_mod = get_role_default_modules(rol_secimi)

    st.markdown("---")
    st.markdown("**Modül Yetkileri — Grup bazlı seçim:**")

    # Toplu seçim butonları
    _tc1, _tc2, _tc3 = st.columns(3)
    with _tc1:
        if st.button("✅ Tümünü Seç", key="gy_selall", use_container_width=True):
            for _i in range(len(TUM_MODULLER)):
                st.session_state[f"gy_mod_{_i}"] = True
            st.rerun()
    with _tc2:
        if st.button("❌ Tümünü Kaldır", key="gy_deselall", use_container_width=True):
            for _i in range(len(TUM_MODULLER)):
                st.session_state[f"gy_mod_{_i}"] = False
            st.rerun()
    with _tc3:
        if st.button("🔄 Mevcut Varsayılanı Yükle", key="gy_loaddef", use_container_width=True):
            for _i, _m in enumerate(TUM_MODULLER):
                st.session_state[f"gy_mod_{_i}"] = (_m in mevcut_mod if mevcut_mod else True)
            st.rerun()

    # Grup bazlı expander'lar
    secili_moduller: list[str] = []
    _idx = 0
    for _grp_ad, _grp_mods in MODUL_GRUPLARI.items():
        with st.expander(f"📁 {_grp_ad} ({len(_grp_mods)} modül)", expanded=False):
            _gc1, _gc2 = st.columns([0.5, 0.5])
            with _gc1:
                if st.button(f"✅ {_grp_ad} Tümü", key=f"gy_grpsel_{_grp_ad}", use_container_width=True):
                    for _gi in range(len(_grp_mods)):
                        st.session_state[f"gy_mod_{_idx + _gi}"] = True
                    st.rerun()
            with _gc2:
                if st.button(f"❌ {_grp_ad} Kaldır", key=f"gy_grpdes_{_grp_ad}", use_container_width=True):
                    for _gi in range(len(_grp_mods)):
                        st.session_state[f"gy_mod_{_idx + _gi}"] = False
                    st.rerun()

            _cols = st.columns(2)
            for _gi, _mod in enumerate(_grp_mods):
                _abs_i = _idx + _gi
                with _cols[_gi % 2]:
                    _def_val = st.session_state.get(
                        f"gy_mod_{_abs_i}",
                        _mod in mevcut_mod if mevcut_mod else True,
                    )
                    if st.checkbox(_mod, key=f"gy_mod_{_abs_i}", value=_def_val):
                        secili_moduller.append(_mod)
        _idx += len(_grp_mods)

    st.markdown("---")
    st.caption(f"Seçili: {len(secili_moduller)} modül | Boş = tüm modüllere erişim")

    _ac1, _ac2 = st.columns(2)
    with _ac1:
        if st.button(
            f"💾 {rol_secimi} Grubuna Uygula ({len(rol_users)} kullanıcı)",
            key="gy_uygula", type="primary", use_container_width=True,
        ):
            for u in rol_users:
                update_user_modules(u["username"], secili_moduller)
            ROL_VARSAYILAN_MODULLER[rol_secimi] = secili_moduller
            st.success(f"✅ {len(rol_users)} kullanıcının yetkileri güncellendi!")
            try:
                from utils.activity_log import log_activity
                log_activity("grup_yetki_guncelle",
                             detail=f"rol={rol_secimi}, kullanici={len(rol_users)}, modul={len(secili_moduller)}",
                             module="kullanici_yonetimi")
            except Exception:
                pass
            st.rerun()
    with _ac2:
        if st.button("🔍 Kullanıcıları Göster", key="gy_goster", use_container_width=True):
            for u in rol_users:
                _mods = u.get("izinli_moduller", [])
                _mod_txt = f"{len(_mods)} modül" if _mods else "Tüm modüller"
                st.caption(f"• {u.get('name', '')} (@{u['username']}) — {_mod_txt}")


# ============================================================
# KULLANICI LISTESİ
# ============================================================

def _render_kullanici_listesi():
    """Mevcut kullanicilari listele ve yonet."""
    styled_section("Kayıtli Kullanıcılar")

    users = get_all_users()

    aktif = sum(1 for u in users if u.get("is_active", True))
    pasif = len(users) - aktif
    rol_dagilimi: dict[str, int] = {}
    for u in users:
        r = u.get("role", "Diger")
        rol_dagilimi[r] = rol_dagilimi.get(r, 0) + 1

    styled_stat_row([
        ("Toplam", str(len(users)), "#7c3aed", "👥"),
        ("Aktif", str(aktif), "#10b981", "✅"),
        ("Pasif", str(pasif), "#ef4444", "⏸️"),
        ("Rol Cesidi", str(len(rol_dagilimi)), "#2563eb", "🎭"),
    ])

    f1, f2 = st.columns(2)
    with f1:
        rol_filtre = st.selectbox("Rol Filtresi", ["Tümü"] + list(ROLES), key="kl_rol")
    with f2:
        durum_filtre = st.selectbox("Durum", ["Tümü", "Aktif", "Pasif"], key="kl_durum")

    filtreli = users
    if rol_filtre != "Tümü":
        filtreli = [u for u in filtreli if u.get("role") == rol_filtre]
    if durum_filtre == "Aktif":
        filtreli = [u for u in filtreli if u.get("is_active", True)]
    elif durum_filtre == "Pasif":
        filtreli = [u for u in filtreli if not u.get("is_active", True)]

    st.caption(f"Gösterilen: {len(filtreli)} / {len(users)}")

    for u in filtreli:
        username = u["username"]
        name = u.get("name", "")
        role = u.get("role", "")
        unvan_goster = u.get("unvan", "") or u.get("position_name", "")
        is_active = u.get("is_active", True)
        moduller = u.get("izinli_moduller", [])

        durum_badge = (
            '<span style="background:#10b98120;color:#10b981;padding:2px 8px;'
            'border-radius:8px;font-size:11px;font-weight:600;">Aktif</span>'
            if is_active
            else '<span style="background:#ef444420;color:#ef4444;padding:2px 8px;'
            'border-radius:8px;font-size:11px;font-weight:600;">Pasif</span>'
        )

        unvan_badge = (
            f'<span style="background:#ea580c20;color:#ea580c;padding:2px 8px;'
            f'border-radius:8px;font-size:11px;font-weight:600;">{unvan_goster}</span>'
        ) if unvan_goster else ""

        # Sinif/Sube bilgisi
        user_subeler = u.get("subeler", [])
        user_sinif = u.get("sinif", "")
        user_sube_tek = u.get("sube", "")
        user_ogrenci = u.get("ogrenci_adi", "")

        sube_badge = ""
        if role == "Öğretmen" and user_subeler:
            sube_text = ", ".join(user_subeler[:4])
            if len(user_subeler) > 4:
                sube_text += f" +{len(user_subeler) - 4}"
            sube_badge = (
                f'<span style="background:#2563eb20;color:#2563eb;padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">'
                f'Şubeler: {sube_text}</span>'
            )
        elif role == "Veli" and user_sinif:
            veli_bilgi = f"{user_sinif}/{user_sube_tek}" if user_sube_tek else user_sinif
            if user_ogrenci:
                veli_bilgi += f" ({user_ogrenci})"
            sube_badge = (
                f'<span style="background:#2563eb20;color:#2563eb;padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">'
                f'{veli_bilgi}</span>'
            )

        modul_bilgi = ", ".join(moduller[:3]) if moduller else "Tüm moduller"
        if moduller and len(moduller) > 3:
            modul_bilgi += f" +{len(moduller) - 3}"

        _durum_icon = "🟢" if is_active else "🔴"
        _modul_say = f"{len(moduller)} modül" if moduller else "Tüm modüller"
        _exp_title = f"{_durum_icon} {name} (@{username}) — {role} — {_modul_say}"

        with st.expander(_exp_title, expanded=False):
            # Bilgi satırı
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;">'
                f'<span style="background:#7c3aed20;color:#7c3aed;padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">{role}</span>'
                f'{unvan_badge}{sube_badge}{durum_badge}'
                f'<span style="color:#94a3b8;font-size:11px;">Modüller: {modul_bilgi}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            bc1, bc2, bc3, bc4 = st.columns(4)
            with bc1:
                if st.button("🔑 Şifre Sıfırla", key=f"kl_reset_{username}", use_container_width=True):
                    new_pw = reset_password(username)
                    if new_pw:
                        st.success(f"Yeni şifre: **{new_pw}**")
                        st.caption("Bu şifreyi kaydedin!")
                    else:
                        st.error("Şifre sıfırlanamadı.")
            with bc2:
                btn_label = "🔴 Pasif Yap" if is_active else "🟢 Aktif Yap"
                if st.button(btn_label, key=f"kl_toggle_{username}", use_container_width=True):
                    new_status = toggle_user_active(username)
                    if new_status is not None:
                        st.success(f"Durum: {'Aktif' if new_status else 'Pasif'}")
                        st.rerun()
            with bc3:
                if st.button("🔐 Yetki Düzenle", key=f"kl_yetki_{username}", use_container_width=True):
                    st.session_state[f"kl_yetki_edit_{username}"] = True
            with bc4:
                if username not in ("admin", "superadmin"):
                    if st.button("🗑️ Sil", key=f"kl_sil_{username}", use_container_width=True):
                        delete_user(username)
                        st.success(f"{username} silindi!")
                        st.rerun()

        if st.session_state.get(f"kl_yetki_edit_{username}", False):
            with st.expander(f"🔐 {name} — Modül Yetkileri", expanded=True):
                # Hızlı şablon seçimi
                st.markdown(
                    '<div style="font-size:0.8rem;color:#94A3B8;margin-bottom:6px;">'
                    '⚡ Hızlı Şablon — Rol bazlı varsayılan yetkileri yükle:</div>',
                    unsafe_allow_html=True,
                )
                _tmpl_cols = st.columns(len(ROL_VARSAYILAN_MODULLER))
                for _ti, (_trol, _tmods) in enumerate(ROL_VARSAYILAN_MODULLER.items()):
                    with _tmpl_cols[_ti]:
                        _tlabel = f"Tümü" if not _tmods else f"{_trol} ({len(_tmods)})"
                        if st.button(_tlabel, key=f"kl_tmpl_{username}_{_trol}", use_container_width=True):
                            # Şablonu uygula
                            for _mi2, _mod2 in enumerate(TUM_MODULLER):
                                st.session_state[f"kl_mod_{username}_{_mi2}"] = (
                                    _mod2 in _tmods if _tmods else True
                                )
                            st.rerun()

                st.markdown("---")

                # Toplu seçim butonları
                _sel_c1, _sel_c2, _sel_c3 = st.columns(3)
                with _sel_c1:
                    if st.button("✅ Tümünü Seç", key=f"kl_selall_{username}", use_container_width=True):
                        for _mi2 in range(len(TUM_MODULLER)):
                            st.session_state[f"kl_mod_{username}_{_mi2}"] = True
                        st.rerun()
                with _sel_c2:
                    if st.button("❌ Tümünü Kaldır", key=f"kl_deselall_{username}", use_container_width=True):
                        for _mi2 in range(len(TUM_MODULLER)):
                            st.session_state[f"kl_mod_{username}_{_mi2}"] = False
                        st.rerun()
                with _sel_c3:
                    if st.button("🔄 Rol Varsayılanı", key=f"kl_roldef_{username}", use_container_width=True):
                        _def_mods = get_role_default_modules(role)
                        for _mi2, _mod2 in enumerate(TUM_MODULLER):
                            st.session_state[f"kl_mod_{username}_{_mi2}"] = (
                                _mod2 in _def_mods if _def_mods else True
                            )
                        st.rerun()

                # Grup bazlı checkbox'lar — her grup bir expander
                secili: list[str] = []
                _mod_idx = 0
                for _grp_ad, _grp_mods in MODUL_GRUPLARI.items():
                    with st.expander(f"📁 {_grp_ad} ({len(_grp_mods)} modül)", expanded=False):
                        # Grup toplu seçim
                        _gc1, _gc2 = st.columns([0.5, 0.5])
                        with _gc1:
                            if st.button(f"✅ {_grp_ad} Tümü", key=f"kl_grpsel_{username}_{_grp_ad}", use_container_width=True):
                                for _gi in range(len(_grp_mods)):
                                    st.session_state[f"kl_mod_{username}_{_mod_idx + _gi}"] = True
                                st.rerun()
                        with _gc2:
                            if st.button(f"❌ {_grp_ad} Kaldır", key=f"kl_grpdes_{username}_{_grp_ad}", use_container_width=True):
                                for _gi in range(len(_grp_mods)):
                                    st.session_state[f"kl_mod_{username}_{_mod_idx + _gi}"] = False
                                st.rerun()

                        _ed_cols = st.columns(2)
                        for _gi, _mod in enumerate(_grp_mods):
                            _abs_idx = _mod_idx + _gi
                            with _ed_cols[_gi % 2]:
                                _checked = st.session_state.get(
                                    f"kl_mod_{username}_{_abs_idx}",
                                    _mod in moduller,
                                )
                                if st.checkbox(_mod, key=f"kl_mod_{username}_{_abs_idx}", value=_checked):
                                    secili.append(_mod)
                    _mod_idx += len(_grp_mods)

                st.caption("Boş bırakırsanız tüm modüllere erişebilir.")

                # Kaydet / İptal
                yc1, yc2 = st.columns(2)
                with yc1:
                    if st.button("💾 Kaydet", key=f"kl_yetki_kaydet_{username}", type="primary", use_container_width=True):
                        update_user_modules(username, secili)
                        st.success("Yetkiler güncellendi!")
                        st.session_state[f"kl_yetki_edit_{username}"] = False
                        st.rerun()
                with yc2:
                    if st.button("İptal", key=f"kl_yetki_iptal_{username}", use_container_width=True):
                        st.session_state[f"kl_yetki_edit_{username}"] = False
                        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def _render_ky_dashboard():
    """Kullanıcı Yönetimi dashboard - ozet istatistikler ve grafikler."""
    users = get_all_users()
    total = len(users)
    aktif = sum(1 for u in users if u.get("is_active", True))
    pasif = total - aktif

    # Rol dagilimi
    role_dist: dict[str, int] = {}
    for u in users:
        r = u.get("role", "Diger")
        role_dist[r] = role_dist.get(r, 0) + 1

    yonetici_count = role_dist.get("Yonetici", 0)
    ogretmen_count = role_dist.get("Öğretmen", 0)
    veli_count = role_dist.get("Veli", 0)

    styled_section("Genel Bakis", "#7c3aed")
    styled_stat_row([
        ("Toplam Kullanıcı", str(total), "#7c3aed", "👥"),
        ("Aktif", str(aktif), "#10b981", "✅"),
        ("Pasif", str(pasif), "#ef4444", "⏸️"),
        ("Yonetici", str(yonetici_count), "#2563eb", "🛡️"),
        ("Öğretmen", str(ogretmen_count), "#f59e0b", "📚"),
        ("Veli", str(veli_count), "#ec4899", "👨‍👩‍👧"),
    ])

    col_left, col_right = st.columns(2)

    # Sol kolon: Rol Dagilimi donut chart
    with col_left:
        styled_section("Rol Dagilimi", "#2563eb")
        donut_colors = ["#7c3aed", "#2563eb", "#10b981", "#f59e0b", "#ef4444", "#ec4899"]
        donut_svg = ReportStyler.donut_chart_svg(
            data={k: float(v) for k, v in role_dist.items()},
            colors=donut_colors,
            size=155,
        )
        st.markdown(
            f'<div style="display:flex;justify-content:center;padding:10px 0;">'
            f'{donut_svg}</div>',
            unsafe_allow_html=True,
        )

    # Sag kolon: Son eklenen kullanicilar
    with col_right:
        styled_section("Son Eklenen Kullanıcılar", "#10b981")
        sorted_users = sorted(
            users,
            key=lambda u: u.get("created_at", ""),
            reverse=True,
        )
        recent = sorted_users[:8]

        if not recent:
            styled_info_banner("Henuz kullanici bulunmuyor.", "info", "📭")
        else:
            rows_html = ""
            for u in recent:
                name = u.get("name", u.get("username", "?"))
                role = u.get("role", "Diger")
                is_active = u.get("is_active", True)
                durum_badge = (
                    '<span style="background:#10b98120;color:#10b981;padding:2px 8px;'
                    'border-radius:8px;font-size:10px;font-weight:600;">Aktif</span>'
                    if is_active
                    else '<span style="background:#ef444420;color:#ef4444;padding:2px 8px;'
                    'border-radius:8px;font-size:10px;font-weight:600;">Pasif</span>'
                )
                role_badge = (
                    f'<span style="background:#7c3aed20;color:#7c3aed;padding:2px 8px;'
                    f'border-radius:8px;font-size:10px;font-weight:600;">{role}</span>'
                )
                created = u.get("created_at", "")[:10]
                rows_html += (
                    f'<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;'
                    f'border-bottom:1px solid #1A2035;">'
                    f'<span style="font-weight:600;color:#94A3B8;font-size:13px;min-width:120px;">'
                    f'{name}</span>'
                    f'{role_badge} {durum_badge}'
                    f'<span style="color:#94a3b8;font-size:11px;margin-left:auto;">{created}</span>'
                    f'</div>'
                )
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:6px 0;max-height:340px;overflow-y:auto;">{rows_html}</div>',
                unsafe_allow_html=True,
            )

    # Alt: Modul yetki ozeti
    styled_section("Modul Yetki Özeti", "#f59e0b")
    modul_atanmis = sum(1 for u in users if u.get("izinli_moduller"))
    modul_tum = total - modul_atanmis
    styled_info_banner(
        f"{modul_atanmis} kullaniciya ozel modul yetkisi atanmis, "
        f"{modul_tum} kullanici tum modullere erisebilir.",
        "info", "🔑",
    )


# ============================================================
# KY RAPORLAR
# ============================================================

def _render_ky_raporlar():
    """KY Raporlar - Kullanici yonetimi raporlari."""
    styled_section("KY Raporlar", "#7c3aed")

    users = get_all_users()
    total = len(users)
    active = sum(1 for u in users if u.get("active", True))

    # Role distribution
    role_dist = {}
    for u in users:
        r = u.get("role", "Diger")
        role_dist[r] = role_dist.get(r, 0) + 1

    # Date-based analysis
    import datetime as _dt
    bugun = _dt.date.today()
    bu_ay = sum(1 for u in users if u.get("created_at", "").startswith(bugun.strftime("%Y-%m")))

    # KPI
    styled_stat_row([
        ("Toplam Kullanıcı", total, "#7c3aed", "👥"),
        ("Aktif", active, "#10b981", "✅"),
        ("Pasif", total - active, "#ef4444", "🔒"),
        ("Bu Ay Eklenen", bu_ay, "#3b82f6", "📅"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Rol Dagilimi", "#7c3aed")
        if role_dist:
            st.markdown(ReportStyler.donut_chart_svg(role_dist, colors=["#7c3aed","#2563eb","#10b981","#f59e0b","#ef4444"]), unsafe_allow_html=True)

    with c2:
        styled_section("Modul Erisim Dagilimi", "#2563eb")
        modul_dist = {}
        for u in users:
            mods = u.get("izinli_moduller", [])
            if isinstance(mods, list):
                for m in mods:
                    modul_dist[m] = modul_dist.get(m, 0) + 1
        if modul_dist:
            top8 = dict(sorted(modul_dist.items(), key=lambda x: -x[1])[:8])
            for name, cnt in top8.items():
                st.markdown(ReportStyler.horizontal_bar_html({name[:20]: float(cnt)}, color="#2563eb"), unsafe_allow_html=True)
        else:
            st.info("Modul erisim verisi yok.")

    # AI Onerileri
    styled_section("AI Onerileri", "#8b5cf6")
    recommendations = []
    if total - active > total * 0.2:
        recommendations.append("Pasif kullanici orani yuksek (%{:.0f}). Hesaplari incelemeniz onerilir.".format((total-active)/max(total,1)*100))
    if role_dist.get("Yonetici", 0) > total * 0.3:
        recommendations.append("Yonetici orani yuksek. Yetki dagitimini gozden gecirin.")
    if not recommendations:
        recommendations.append("Kullanıcı dagilimi dengeli gorunuyor. Duzenli kontrol onerilir.")

    for i, rec in enumerate(recommendations):
        st.markdown(f'''<div style="background:linear-gradient(135deg,#f5f3ff,#ede9fe);
            border-radius:10px;padding:12px 16px;margin:6px 0;border-left:3px solid #8b5cf6;">
            <b>💡 Oneri {i+1}:</b> {rec}
        </div>''', unsafe_allow_html=True)

    # Kullanıcı Listesi Tablosu
    styled_section("Kullanıcı Detay Tablosu", "#0d9488")
    import pandas as _pd
    if users:
        rows = []
        for u in users:
            rows.append({
                "Ad": u.get("name", ""),
                "Kullanıcı Adi": u.get("username", ""),
                "Rol": u.get("role", ""),
                "Durum": "Aktif" if u.get("active", True) else "Pasif",
                "Oluşturma": u.get("created_at", "")[:10],
            })
        df = _pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ---- Performans Karsilastirma ----
    try:
        from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                         generate_module_pdf, render_pdf_download_button,
                                         render_report_kunye_html)
        from datetime import timedelta as _td_ky
        _now_ky = _dt.datetime.now()
        _cur_month_ky = _now_ky.strftime("%Y-%m")
        _prev_month_ky = (_now_ky.replace(day=1) - _td_ky(days=1)).strftime("%Y-%m")

        st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

        # Monthly login count (from last_login field)
        cur_login = sum(1 for u in users if str(u.get("last_login", "")).startswith(_cur_month_ky))
        prev_login = sum(1 for u in users if str(u.get("last_login", "")).startswith(_prev_month_ky))

        # Monthly new user count
        cur_new = sum(1 for u in users if str(u.get("created_at", "")).startswith(_cur_month_ky))
        prev_new = sum(1 for u in users if str(u.get("created_at", "")).startswith(_prev_month_ky))

        ky_comparisons = [
            {"label": "Giriş Yapan Kullanıcı", "current": cur_login, "previous": prev_login},
            {"label": "Yeni Kullanıcı", "current": cur_new, "previous": prev_new},
        ]
        st.markdown(period_comparison_row_html(ky_comparisons), unsafe_allow_html=True)

        # ---- Enhanced AI Onerileri ----
        ky_insights = []
        inactive_pct = ((total - active) / max(total, 1)) * 100
        if inactive_pct > 30:
            ky_insights.append({
                "icon": "🔒", "title": "Yuksek Pasif Kullanıcı Orani",
                "text": f"Kullanıcılarin %{inactive_pct:.0f}'i pasif durumda. Hesap temizligi veya yeniden aktivasyon sureci baslatilmali.",
                "color": "#ef4444"
            })
        elif inactive_pct > 15:
            ky_insights.append({
                "icon": "⚠️", "title": "Pasif Kullanıcı Uyarisi",
                "text": f"Pasif kullanici orani %{inactive_pct:.0f}. 90 gunden fazla inaktif hesaplari inceleyin.",
                "color": "#f59e0b"
            })

        # Role balance check
        admin_count = role_dist.get("Yonetici", 0)
        if admin_count > total * 0.25 and total > 4:
            ky_insights.append({
                "icon": "👑", "title": "Yetki Dağıtım Dengesizligi",
                "text": f"{admin_count} yonetici hesabi mevcut (toplam kullanicinin %{admin_count/max(total,1)*100:.0f}'i). Minimum yetki ilkesine uygun olarak rolleri gozden gecirin.",
                "color": "#8b5cf6"
            })

        # Module access diversity
        modul_per_user = []
        for u in users:
            mods = u.get("izinli_moduller", [])
            if isinstance(mods, list):
                modul_per_user.append(len(mods))
        avg_modul = sum(modul_per_user) / max(len(modul_per_user), 1)
        if avg_modul < 2 and total > 2:
            ky_insights.append({
                "icon": "📦", "title": "Sinirli Modul Erisimi",
                "text": f"Kullanıcı basina ortalama {avg_modul:.1f} modul erisimi var. Ihtiyaca gore erisim yetkilendirmelerini genisletin.",
                "color": "#2563eb"
            })

        ky_insights.append({
            "icon": "🔐", "title": "Guvenlik Onerisi",
            "text": "Duzensiz giris yapan kullanicilarin sifre politikalarini ve iki faktorlu dogrulamayi kontrol edin.",
            "color": "#0d9488"
        })

        if not ky_insights:
            ky_insights.append({
                "icon": "✅", "title": "Sistem Sagligi Iyi",
                "text": "Kullanıcı dagilimi ve yetki yapisi dengeli gorunuyor. Periyodik kontrollere devam edin.",
                "color": "#10b981"
            })

        st.markdown(ai_recommendations_html(ky_insights), unsafe_allow_html=True)

        # ---- Kurumsal Kunye ----
        st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

        # ---- PDF Export ----
        st.markdown(ReportStyler.section_divider_html("PDF Rapor", "#1e40af"), unsafe_allow_html=True)
        if st.button("📥 KY Raporu (PDF)", key="ky_pdf_btn", use_container_width=True):
            ky_pdf_sections = [
                {
                    "title": "Kullanıcı Yönetimi Özet",
                    "metrics": [
                        ("Toplam", total, "#7c3aed"),
                        ("Aktif", active, "#10b981"),
                        ("Pasif", total - active, "#ef4444"),
                        ("Bu Ay", bu_ay, "#3b82f6"),
                    ],
                    "text": f"Toplam {total} kullanici, {active} aktif, {total-active} pasif.",
                },
                {
                    "title": "Rol Dagilimi",
                    "donut_data": {k: float(v) for k, v in role_dist.items()} if role_dist else {},
                    "donut_title": "Rol Dagilimi",
                },
            ]
            if users:
                ky_pdf_sections.append({
                    "title": "Kullanıcı Listesi",
                    "table": df,
                    "table_color": "#7c3aed",
                })
            ky_pdf_bytes = generate_module_pdf("KY Raporu", ky_pdf_sections)
            render_pdf_download_button(ky_pdf_bytes, "ky_raporu.pdf", "KY Raporu", "ky_dl")
    except Exception as _ky_err:
        st.caption(f"Rapor bilesenleri yuklenemedi: {_ky_err}")


# ============================================================
# ANA GIRIS NOKTASI
# ============================================================

def render_kullanici_yonetimi():
    """Kullanıcı Yönetimi modulu ana giris noktasi."""
    _inject_ky_css()

    user = _get_current_user()
    role = user.get("role", "")

    if role != "Yonetici":
        styled_info_banner(
            "Bu modüle sadece Yönetici rolündeki kullanıcılar erişebilir.",
            "error", "🔒",
        )
        return

    styled_header("Kullanıcı Yönetimi", "Şifre oluşturma, yetki atama ve kullanıcı işlemleri", icon="👥")

    render_smarti_welcome("kullanici_yonetimi")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("kullanici_yonetimi_egitim_yili")

    tabs = st.tabs(["📊 Dashboard", "➕ Yeni Kullanıcı", "👥 Kullanıcı Listesi", "🔐 Grup Yetkileri", "📈 KY Raporlar", "🤖 Smarti"])

    with tabs[0]:
        _render_ky_dashboard()
    with tabs[1]:
        _render_yeni_kullanici()
    with tabs[2]:
        _render_kullanici_listesi()
    with tabs[3]:
        _render_grup_yetkileri()
    with tabs[4]:
        _render_ky_raporlar()
    with tabs[5]:
        def _ky_smarti_context() -> str:
            try:
                all_users = get_all_users()
                total = len(all_users)
                role_dist = {}
                for u in all_users:
                    r = u.get("role", "Bilinmiyor")
                    role_dist[r] = role_dist.get(r, 0) + 1
                role_str = ", ".join(f"{k}: {v}" for k, v in role_dist.items())
                return f"Toplam kullanici: {total}. Rol dagilimi: {role_str}."
            except Exception:
                return "Kullanıcı verisi yuklenemedi."
        render_smarti_chat("kullanici_yonetimi", _ky_smarti_context)
