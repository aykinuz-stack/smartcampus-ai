"""QR Kod Handler — Kitaptan taranan QR kodları yazılıma yönlendirir.

URL format: /qr?sinif=5&ders=Matematik&unite=Kesirler&konu=Toplama&tip=quiz
tip: quiz, ders, video, telafi, veli, ogretmen
"""
import json
import os
import streamlit as st
from utils.ui_common import inject_common_css, styled_header


def render_qr_handler():
    """QR kod ile gelen kullanıcıyı rol bazlı yönlendirir."""
    inject_common_css()

    # URL parametreleri
    params = st.query_params
    sinif = params.get("sinif", "")
    ders = params.get("ders", "")
    unite = params.get("unite", "")
    konu = params.get("konu", "")
    tip = params.get("tip", "ders")

    auth_user = st.session_state.get("auth_user", {})
    role = auth_user.get("role", "").lower()
    name = auth_user.get("name", "Kullanici")

    styled_header("📱 Kitap → Yazılım Bağlantısı",
                   f"{sinif}. Sınıf {ders} — {konu or unite}")

    if not sinif or not ders:
        st.warning("Bu sayfaya kitaptaki QR kodu tarayarak ulaşabilirsiniz.")
        st.info("📖 Kitabınızdaki QR kodu telefonunuzla tarayın, ilgili dijital içerik otomatik açılacaktır.")
        return

    # ── Konu bilgisi göster ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
        f'padding:18px 24px;border-radius:14px;margin-bottom:16px">'
        f'<div style="font-size:1.2rem;font-weight:700">{sinif}. Sınıf {ders}</div>'
        f'<div style="font-size:.9rem;opacity:.8;margin-top:4px">'
        f'Ünite: {unite} | Konu: {konu}</div>'
        f'</div>', unsafe_allow_html=True,
    )

    # ── Kazanım bilgisi yükle ──
    kazanimlar = _load_kazanimlar(int(sinif) if sinif.isdigit() else 0, ders, unite, konu)
    soru_sayisi = _count_sorular(int(sinif) if sinif.isdigit() else 0, ders)

    # ── Rol bazlı içerik ──
    if role == "ogrenci":
        _ogrenci_view(sinif, ders, unite, konu, kazanimlar, soru_sayisi)
    elif role == "veli":
        _veli_view(sinif, ders, unite, konu, auth_user)
    elif role in ("ogretmen", "mudur", "yonetici", "superadmin"):
        _ogretmen_view(sinif, ders, unite, konu, kazanimlar, soru_sayisi)
    else:
        _genel_view(sinif, ders, unite, konu, kazanimlar)


def _ogrenci_view(sinif, ders, unite, konu, kazanimlar, soru_sayisi):
    """Öğrenci: Quiz çöz, video izle, etkinlik yap."""
    st.markdown("### 🎓 Öğrenci Paneli")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Kazanım", len(kazanimlar))
    with col2:
        st.metric("❓ Soru", soru_sayisi)
    with col3:
        st.metric("📊 Sınıf", f"{sinif}. Sınıf")

    # Kazanımlar
    if kazanimlar:
        with st.expander(f"🎯 Bu Konunun Kazanımları ({len(kazanimlar)})", expanded=False):
            for i, k in enumerate(kazanimlar, 1):
                outcomes = k.get("learning_outcomes", [])
                for o in outcomes[:3]:
                    st.markdown(f"- {o}")

    st.markdown("---")
    st.markdown("### 🚀 Ne yapmak istiyorsun?")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("❓ Quiz Çöz", use_container_width=True, type="primary"):
            st.session_state["_sidebar_secim"] = "AI Ogrenme Platformu"
            st.rerun()
        if st.button("🎮 Bilgi Yarışması", use_container_width=True):
            st.session_state["_sidebar_secim"] = "AI Ogrenme Platformu"
            st.rerun()
        if st.button("🏘️ Matematik Köyü", use_container_width=True):
            st.session_state["_sidebar_secim"] = "STEAM Merkezi"
            st.rerun()
    with c2:
        if st.button("📖 Konu Tekrarı", use_container_width=True):
            st.session_state["_sidebar_secim"] = "Akademik Takip"
            st.rerun()
        if st.button("🔄 Telafi Görevi", use_container_width=True):
            st.info(f"📚 Kitabınızdaki {sinif}. Sınıf {ders} - {konu} konusunu tekrar okuyun, sonra quiz çözün.")
        if st.button("🤖 Smarti'ye Sor", use_container_width=True):
            st.session_state["_sidebar_secim"] = "AI Ogrenme Platformu"
            st.rerun()


def _veli_view(sinif, ders, unite, konu, auth_user):
    """Veli: Çocuğun performansını gör."""
    st.markdown("### 👨‍👩‍👧 Veli Paneli")

    ogrenci_id = auth_user.get("ogrenci_id", "")
    ogrenci_adi = auth_user.get("ogrenci_adi", "Çocuğunuz")

    st.info(f"📊 **{ogrenci_adi}** — {sinif}. Sınıf {ders} konusundaki durum:")

    # Performans bilgisi
    grades = _load_grades(ogrenci_id, ders)
    attendance = _load_attendance(ogrenci_id)

    col1, col2, col3 = st.columns(3)
    with col1:
        avg = sum(g.get("puan", 0) for g in grades) / len(grades) if grades else 0
        st.metric("📊 Not Ortalaması", f"{avg:.1f}")
    with col2:
        st.metric("📝 Sınav Sayısı", len(grades))
    with col3:
        devamsiz = sum(1 for a in attendance if a.get("turu") in ("devamsiz", "ozursuz"))
        st.metric("❌ Devamsızlık", devamsiz)

    st.markdown("---")
    if st.button("📋 Tam Karne Görüntüle", use_container_width=True, type="primary"):
        st.session_state["_sidebar_secim"] = "Veli Paneli"
        st.rerun()
    if st.button("💬 Öğretmene Mesaj Gönder", use_container_width=True):
        st.session_state["_sidebar_secim"] = "Veli Paneli"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📖 Kitap Önerisi")
    st.success(f"📚 {sinif}. Sınıf {ders} kitabında **{konu or unite}** konusunu çocuğunuzla birlikte okuyabilirsiniz.")


def _ogretmen_view(sinif, ders, unite, konu, kazanimlar, soru_sayisi):
    """Öğretmen: Ders planı, sınav oluştur, yoklama."""
    st.markdown("### 👩‍🏫 Öğretmen Paneli")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Kazanım", len(kazanimlar))
    with col2:
        st.metric("❓ Soru Bankası", soru_sayisi)
    with col3:
        st.metric("📊 Sınıf", f"{sinif}. Sınıf")
    with col4:
        st.metric("📚 Ders", ders[:10])

    st.markdown("---")
    st.markdown("### 📋 Ne yapmak istiyorsun?")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📝 Bu Konudan Sınav Oluştur", use_container_width=True, type="primary"):
            st.session_state["_sidebar_secim"] = "Olcme ve Degerlendirme"
            st.rerun()
        if st.button("📖 Ders Defterine Kaydet", use_container_width=True):
            st.session_state["_sidebar_secim"] = "Akademik Takip"
            st.rerun()
        if st.button("✅ Yoklama Al", use_container_width=True):
            st.session_state["_sidebar_secim"] = "Akademik Takip"
            st.rerun()
    with c2:
        if st.button("📊 Sınıf Analizi Gör", use_container_width=True):
            st.session_state["_sidebar_secim"] = "Ogrenci Zeka Merkezi"
            st.rerun()
        if st.button("🎯 Kazanım Takibi", use_container_width=True):
            st.session_state["_sidebar_secim"] = "Akademik Takip"
            st.rerun()
        if st.button("🤖 AI ile Ders Planı", use_container_width=True):
            st.session_state["_sidebar_secim"] = "AI Ogrenme Platformu"
            st.rerun()

    # Kazanımlar listesi
    if kazanimlar:
        with st.expander(f"🎯 Kazanımlar ({len(kazanimlar)})", expanded=False):
            for k in kazanimlar:
                for o in k.get("learning_outcomes", [])[:3]:
                    st.markdown(f"- {o}")


def _genel_view(sinif, ders, unite, konu, kazanimlar):
    """Giriş yapılmamış kullanıcı."""
    st.warning("📱 Lütfen giriş yapın — rol bazlı içerik gösterilecektir.")
    st.info(f"Bu QR kod **{sinif}. Sınıf {ders} - {konu or unite}** konusuna aittir.")
    if kazanimlar:
        st.markdown(f"**{len(kazanimlar)} kazanım** bu konuyla ilişkilidir.")


# ── Veri yükleyiciler ──

def _load_kazanimlar(sinif, ders, unite="", konu=""):
    try:
        with open("data/olcme/annual_plans.json", "r", encoding="utf-8") as f:
            plans = json.load(f)
        filtered = [p for p in plans if p.get("grade") == sinif and p.get("subject") == ders]
        if unite:
            filtered = [p for p in filtered if unite.lower() in p.get("unit", "").lower()]
        if konu:
            filtered = [p for p in filtered if konu.lower() in p.get("topic", "").lower()]
        return filtered[:20]
    except Exception:
        return []


def _count_sorular(sinif, ders):
    try:
        with open("data/olcme/questions.json", "r", encoding="utf-8") as f:
            qs = json.load(f)
        return sum(1 for q in qs if q.get("sinif") == sinif and ders.lower() in (q.get("ders", "") or "").lower())
    except Exception:
        return 0


def _load_grades(student_id, ders):
    try:
        with open("data/akademik/grades.json", "r", encoding="utf-8") as f:
            grades = json.load(f)
        return [g for g in grades if g.get("student_id") == student_id
                and ders.lower() in (g.get("ders", "") or "").lower()][:10]
    except Exception:
        return []


def _load_attendance(student_id):
    try:
        with open("data/akademik/attendance.json", "r", encoding="utf-8") as f:
            att = json.load(f)
        return [a for a in att if a.get("student_id") == student_id]
    except Exception:
        return []
