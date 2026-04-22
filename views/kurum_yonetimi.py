"""
Kurum Yonetimi Modulu — SuperAdmin Paneli
==========================================
Coklu kurum (multi-tenant) yonetimi.
Sadece SuperAdmin rolu erisebilir.
"""

import hashlib
import streamlit as st

from utils.auth import AuthManager, SUPER_ADMIN_ROLE, get_all_users, add_user, \
    delete_user, generate_password, _load_users, _save_users
from utils.tenant import (
    list_tenant_configs, create_tenant, get_tenant_config,
    save_tenant_config, tenant_key, TENANT_ROOT,
)


def _inject_css():
    st.markdown("""
    <style>
    .tenant-card {
        background: linear-gradient(135deg, rgba(14,165,233,.08), rgba(14,165,233,.02));
        border: 1px solid rgba(14,165,233,.15);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
    }
    .tenant-card h3 {
        margin: 0 0 8px 0;
        color: #e2e8f0;
        font-size: 1.1rem;
    }
    .tenant-stat {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(14,165,233,.1);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: .78rem;
        color: #94a3b8;
        margin-right: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_kurum_yonetimi():
    """SuperAdmin icin kurum yonetim paneli."""
    # Yetki kontrolu
    auth_user = AuthManager.get_current_user()
    if auth_user.get("role") != SUPER_ADMIN_ROLE:
        st.error("Bu sayfaya erisim yetkiniz yok. Sadece Süper Yönetici erisebilir.")
        return

    _inject_css()

    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">'
        '<span style="font-size:28px;">🏢</span>'
        '<div>'
        '<div style="font-size:1.4rem;font-weight:800;color:#e2e8f0;">Kurum Yönetimi</div>'
        '<div style="font-size:.8rem;color:#94a3b8;">Multi-Tenant Merkezi Yönetim Paneli</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["📋 Kurumlar", "➕ Yeni Kurum", "👤 Kurum Yöneticileri", "⚙️ Ayarlar"])

    with tabs[0]:
        _render_kurumlar_listesi()

    with tabs[1]:
        _render_yeni_kurum()

    with tabs[2]:
        _render_kurum_yoneticileri()

    with tabs[3]:
        _render_genel_ayarlar()


def _render_kurumlar_listesi():
    """Mevcut kurumlari listele."""
    configs = list_tenant_configs()
    all_users = get_all_users(tenant_scoped=False)

    if not configs:
        st.info("Henuz kayitli kurum yok.")
        return

    st.markdown(f"**Toplam {len(configs)} kurum kayitli**")

    for cfg in configs:
        t_key = cfg.get("key", "")
        t_name = cfg.get("name", t_key)
        aktif = cfg.get("aktif", True)

        # Bu kuruma ait kullanici sayisi
        user_count = sum(1 for u in all_users if u.get("tenant_id") == t_key)
        yonetici_count = sum(1 for u in all_users
                            if u.get("tenant_id") == t_key and u.get("role") == "Yonetici")

        status_color = "#22c55e" if aktif else "#ef4444"
        status_text = "Aktif" if aktif else "Pasif"

        st.markdown(
            f'<div class="tenant-card">'
            f'<h3>🏫 {t_name}</h3>'
            f'<div>'
            f'<span class="tenant-stat">🔑 {t_key}</span>'
            f'<span class="tenant-stat">👥 {user_count} kullanici</span>'
            f'<span class="tenant-stat">👔 {yonetici_count} yonetici</span>'
            f'<span class="tenant-stat" style="color:{status_color};">'
            f'● {status_text}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button(f"Duzenle", key=f"edit_{t_key}", use_container_width=True):
                st.session_state["_edit_tenant"] = t_key
        with col2:
            new_aktif = not aktif
            label = "Aktif Yap" if not aktif else "Pasif Yap"
            if st.button(label, key=f"toggle_{t_key}", use_container_width=True):
                cfg["aktif"] = new_aktif
                save_tenant_config(cfg, t_key)
                st.rerun()
        with col3:
            if st.button("Gecis Yap", key=f"switch_{t_key}", use_container_width=True,
                         type="primary"):
                st.session_state["tenant_id"] = t_key
                st.session_state["tenant_name"] = t_name
                st.success(f"'{t_name}' kurumuna gecis yapildi.")
                st.rerun()

    # Duzenle formu
    edit_key = st.session_state.get("_edit_tenant")
    if edit_key:
        st.divider()
        st.subheader(f"Kurum Düzenleme: {edit_key}")
        cfg = get_tenant_config(edit_key)
        if cfg:
            new_name = st.text_input("Kurum Adi", value=cfg.get("name", ""),
                                     key="edit_tenant_name")
            new_tema = st.selectbox("Renk Tema", ["blue", "green", "purple", "red"],
                                   index=0, key="edit_tenant_tema")
            c1, c2 = st.columns(2)
            with c1:
                new_smtp_host = st.text_input("SMTP Host", value=cfg.get("smtp_host", ""),
                                              key="edit_smtp_host")
                new_smtp_user = st.text_input("SMTP User", value=cfg.get("smtp_user", ""),
                                              key="edit_smtp_user")
            with c2:
                new_smtp_port = st.text_input("SMTP Port", value=cfg.get("smtp_port", ""),
                                              key="edit_smtp_port")
                new_smtp_pass = st.text_input("SMTP Pass", type="password",
                                              value=cfg.get("smtp_pass", ""),
                                              key="edit_smtp_pass")
            new_mail_from = st.text_input("Mail From", value=cfg.get("mail_from", ""),
                                          key="edit_mail_from")

            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("Kaydet", key="save_tenant_edit", type="primary"):
                    cfg["name"] = new_name
                    cfg["renk_tema"] = new_tema
                    cfg["smtp_host"] = new_smtp_host
                    cfg["smtp_port"] = new_smtp_port
                    cfg["smtp_user"] = new_smtp_user
                    cfg["smtp_pass"] = new_smtp_pass
                    cfg["mail_from"] = new_mail_from
                    save_tenant_config(cfg, edit_key)
                    st.session_state.pop("_edit_tenant", None)
                    st.success("Kurum bilgileri guncellendi.")
                    st.rerun()
            with bc2:
                if st.button("Iptal", key="cancel_tenant_edit"):
                    st.session_state.pop("_edit_tenant", None)
                    st.rerun()


def _render_yeni_kurum():
    """Yeni kurum olusturma formu."""
    st.subheader("Yeni Kurum Ekle")

    with st.form("new_tenant_form"):
        kurum_adi = st.text_input("Kurum Adi *", placeholder="Ornek: ABC Koleji")

        smtp_host = st.text_input("SMTP Host", placeholder="smtp.gmail.com")

        smtp_port = st.text_input("SMTP Port", placeholder="465")

        smtp_user = st.text_input("SMTP Kullanici")

        smtp_pass = st.text_input("SMTP Sifre", type="password")

        mail_from = st.text_input("Mail From")


        st.divider()
        st.markdown("**Kurum Yoneticisi Hesabi**")
        admin_username = st.text_input("Yonetici Kullanici Adi *", placeholder="admin")

        admin_name = st.text_input("Yonetici Ad Soyad *", placeholder="Kurum Yoneticisi")

        admin_password = st.text_input("Yonetici Sifresi *", type="password",
                                       placeholder="Minimum 6 karakter")

        submitted = st.form_submit_button("Kurum Olustur", type="primary")

        if submitted:
            if not kurum_adi:
                st.error("Kurum adi zorunludur.")
            elif not admin_username or not admin_password:
                st.error("Yonetici hesabi bilgileri zorunludur.")
            elif len(admin_password) < 6:
                st.error("Sifre en az 6 karakter olmalidir.")
            else:
                # Kurum olustur
                t_key = create_tenant(kurum_adi)

                # Config guncelle
                cfg = get_tenant_config(t_key)
                cfg["smtp_host"] = smtp_host
                cfg["smtp_port"] = smtp_port
                cfg["smtp_user"] = smtp_user
                cfg["smtp_pass"] = smtp_pass
                cfg["mail_from"] = mail_from
                from datetime import datetime
                cfg["created_at"] = datetime.now().isoformat()
                save_tenant_config(cfg, t_key)

                # Kurum yoneticisi olustur
                admin_user = {
                    "username": admin_username,
                    "password_hash": hashlib.sha256(admin_password.encode()).hexdigest(),
                    "name": admin_name or "Yonetici",
                    "role": "Yonetici",
                    "tenant_id": t_key,
                    "is_active": True,
                }

                # Kullanici adi benzersizlik kontrolu
                all_users = get_all_users(tenant_scoped=False)
                existing = {u["username"] for u in all_users}
                if admin_username in existing:
                    st.error(f"'{admin_username}' kullanici adi zaten mevcut.")
                else:
                    add_user(admin_user)
                    st.success(f"'{kurum_adi}' kurumu basariyla olusturuldu! "
                               f"Yonetici: {admin_username}")
                    st.rerun()


def _render_kurum_yoneticileri():
    """Kurum bazli yonetici listesi."""
    configs = list_tenant_configs()
    all_users = get_all_users(tenant_scoped=False)

    for cfg in configs:
        t_key = cfg.get("key", "")
        t_name = cfg.get("name", t_key)

        # Bu kurumun kullanicilari
        tenant_users = [u for u in all_users if u.get("tenant_id") == t_key]
        yoneticiler = [u for u in tenant_users if u.get("role") == "Yonetici"]
        ogretmenler = [u for u in tenant_users if u.get("role") == "Ogretmen"]
        diger = [u for u in tenant_users
                 if u.get("role") not in ("Yonetici", "Ogretmen", "SuperAdmin")]

        with st.expander(f"🏫 {t_name} — {len(tenant_users)} kullanici", expanded=False):
            st.markdown(f"**Yoneticiler ({len(yoneticiler)}):**")
            for u in yoneticiler:
                aktif = "✅" if u.get("is_active", True) else "❌"
                st.markdown(f"- {aktif} `{u['username']}` — {u.get('name', '')}")

            st.markdown(f"**Ogretmenler ({len(ogretmenler)}):**")
            for u in ogretmenler:
                aktif = "✅" if u.get("is_active", True) else "❌"
                st.markdown(f"- {aktif} `{u['username']}` — {u.get('name', '')}")

            st.markdown(f"**Diger ({len(diger)}):**")
            st.caption(f"{len(diger)} ogrenci/veli/calisan")

            # Hizli yonetici ekleme
            st.divider()
            st.markdown("**Hizli Yonetici Ekle:**")
            c1, c2 = st.columns(2)
            with c1:
                new_admin_user = st.text_input("Kullanici Adi",
                                               key=f"new_admin_{t_key}")
                new_admin_name = st.text_input("Ad Soyad",
                                               key=f"new_admin_name_{t_key}")
            with c2:
                new_admin_pw = st.text_input("Sifre", type="password",
                                             key=f"new_admin_pw_{t_key}")
            if st.button("Ekle", key=f"add_admin_{t_key}"):
                if new_admin_user and new_admin_pw:
                    existing = {u["username"] for u in all_users}
                    if new_admin_user in existing:
                        st.error("Bu kullanici adi zaten mevcut.")
                    else:
                        add_user({
                            "username": new_admin_user,
                            "password_hash": hashlib.sha256(
                                new_admin_pw.encode()).hexdigest(),
                            "name": new_admin_name or new_admin_user,
                            "role": "Yonetici",
                            "tenant_id": t_key,
                            "is_active": True,
                        })
                        st.success(f"Yonetici '{new_admin_user}' eklendi.")
                        st.rerun()
                else:
                    st.warning("Kullanici adi ve sifre zorunludur.")


def _render_genel_ayarlar():
    """Genel sistem ayarlari."""
    st.subheader("Sistem Ayarlari")

    st.info("SuperAdmin olarak tum kurumlari yonetebilir, "
            "kurumlararasi gecis yapabilir ve merkezi ayarlari duzenleyebilirsiniz.")

    # Istatistikler
    configs = list_tenant_configs()
    all_users = get_all_users(tenant_scoped=False)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Kurum", len(configs))
    with c2:
        aktif = sum(1 for c in configs if c.get("aktif", True))
        st.metric("Aktif Kurum", aktif)
    with c3:
        st.metric("Toplam Kullanici", len(all_users))
    with c4:
        sa_count = sum(1 for u in all_users if u.get("role") == SUPER_ADMIN_ROLE)
        st.metric("Super Admin", sa_count)

    st.divider()
    st.markdown("**Kurum Bazli Kullanici Dagilimi:**")
    for cfg in configs:
        t_key = cfg.get("key", "")
        t_name = cfg.get("name", t_key)
        count = sum(1 for u in all_users if u.get("tenant_id") == t_key)
        st.markdown(f"- 🏫 **{t_name}**: {count} kullanici")
