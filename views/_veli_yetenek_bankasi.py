"""
Veli Yetenek Bankası — Okul-Veli Ortaklığı
================================================
Veliler mesleklerini/yeteneklerini paylaşır (doktor, avukat, mühendis vb.)
Okul misafir konuşmacı/kariyer günü/mentorluk için otomatik eşleştirir.
Velinin "değerli hissetme" duygusu + okulun zengin içerik kaynağı.
"""
from __future__ import annotations

import json
import os
from datetime import datetime

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# MESLEK KATEGORİLERİ
# ══════════════════════════════════════════════════════════════

MESLEK_KATEGORILERI = {
    "saglik": {
        "ad": "Sağlık", "ikon": "⚕️", "renk": "#059669",
        "meslekler": ["Doktor", "Hemşire", "Diyetisyen", "Psikolog", "Fizyoterapist",
                      "Eczacı", "Diş Hekimi", "Veteriner", "Sağlık Teknisyeni"],
    },
    "hukuk": {
        "ad": "Hukuk", "ikon": "⚖️", "renk": "#4F46E5",
        "meslekler": ["Avukat", "Hakim", "Savcı", "Noter", "Hukuk Müşaviri"],
    },
    "muhendislik": {
        "ad": "Mühendislik", "ikon": "⚙️", "renk": "#D97706",
        "meslekler": ["Bilgisayar Müh.", "İnşaat Müh.", "Makine Müh.", "Elektrik Müh.",
                      "Endüstri Müh.", "Kimya Müh.", "Ziraat Müh.", "Çevre Müh."],
    },
    "egitim": {
        "ad": "Eğitim & Akademi", "ikon": "🎓", "renk": "#7C3AED",
        "meslekler": ["Öğretmen", "Akademisyen", "Eğitim Danışmanı", "Kütüphaneci",
                      "Eğitim Koordinatörü"],
    },
    "is_finans": {
        "ad": "İş & Finans", "ikon": "💼", "renk": "#0284C7",
        "meslekler": ["Muhasebeci", "Mali Müşavir", "Bankacı", "Finans Uzmanı",
                      "İşletmeci", "Girişimci", "CEO/Yönetici", "Pazarlama Uzmanı"],
    },
    "sanat": {
        "ad": "Sanat & Tasarım", "ikon": "🎨", "renk": "#EC4899",
        "meslekler": ["Ressam", "Heykeltıraş", "Grafik Tasarımcı", "Fotoğrafçı",
                      "Müzisyen", "Yazar", "Film Yapımcısı", "Mimar", "İç Mimar"],
    },
    "spor": {
        "ad": "Spor & Sağlıklı Yaşam", "ikon": "⚽", "renk": "#DC2626",
        "meslekler": ["Antrenör", "Spor Eğitmeni", "Profesyonel Sporcu",
                      "Beslenme Uzmanı", "Yoga Eğitmeni"],
    },
    "teknoloji": {
        "ad": "Teknoloji & IT", "ikon": "💻", "renk": "#7C3AED",
        "meslekler": ["Yazılım Geliştirici", "Veri Analisti", "Siber Güvenlik Uzmanı",
                      "UX/UI Tasarımcı", "Proje Yöneticisi", "AI/ML Uzmanı",
                      "Network Uzmanı", "Dijital Pazarlama"],
    },
    "medya": {
        "ad": "Medya & İletişim", "ikon": "📰", "renk": "#EA580C",
        "meslekler": ["Gazeteci", "Yayıncı", "Redaktör", "PR Uzmanı",
                      "Sosyal Medya Uzmanı", "Haber Sunucusu"],
    },
    "esnaf": {
        "ad": "Esnaf & Zanaat", "ikon": "🔨", "renk": "#B45309",
        "meslekler": ["Marangoz", "Elektrikçi", "Tesisatçı", "Kuaför",
                      "Aşçı", "Terzi", "Ayakkabıcı", "Saatçi"],
    },
    "tarim": {
        "ad": "Tarım & Hayvancılık", "ikon": "🌾", "renk": "#059669",
        "meslekler": ["Çiftçi", "Bahçıvan", "Arıcı", "Hayvan Yetiştiricisi"],
    },
    "kamu": {
        "ad": "Kamu Hizmeti", "ikon": "🏛️", "renk": "#334155",
        "meslekler": ["Polis", "Asker", "İtfaiyeci", "Devlet Memuru", "Belediye Çalışanı"],
    },
    "diger": {
        "ad": "Diğer", "ikon": "📋", "renk": "#64748B",
        "meslekler": ["Diğer"],
    },
}

KATKI_TURLERI = [
    "🎤 Misafir Konuşmacı (bir ders için)",
    "🌟 Kariyer Günü Sunumu",
    "🔬 Uygulamalı Atölye",
    "👥 Panel Konuşmacısı",
    "🎯 Mentorluk (öğrenciye birebir)",
    "🏢 İş Yeri Gezisi (öğrencilere)",
    "📝 Proje Danışmanlığı",
    "💼 Staj Fırsatı",
    "🎓 Üniversite/Meslek Paylaşımı",
]


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _vyb_path() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "veli_yetenek_bankasi")
    except Exception:
        d = os.path.join("data", "veli_yetenek_bankasi")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "yetenekler.json")


def _load_yetenekler() -> list[dict]:
    p = _vyb_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_yetenekler(data: list[dict]) -> None:
    with open(_vyb_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _davet_path() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "veli_yetenek_bankasi")
    except Exception:
        d = os.path.join("data", "veli_yetenek_bankasi")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "davetler.json")


def _load_davetler() -> list[dict]:
    p = _davet_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_davetler(data: list[dict]) -> None:
    with open(_davet_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# VELİ KAYIT PANELİ — Veli kendi yeteneğini paylaşır
# ══════════════════════════════════════════════════════════════

def render_veli_kayit_panel():
    """Veli kendi yeteneklerini paylaşır."""
    styled_section("🛠️ Veli Yetenek Bankası — Kaydım", "#0284C7")

    styled_info_banner(
        "Mesleğinizi veya yeteneğinizi paylaşarak okulunuza katkıda bulunun. "
        "Kariyer günlerinde misafir konuşmacı, atölye çalışmaları, mentorluk fırsatları için otomatik eşleştirme yapılır.",
        "info", "💼",
    )

    yetenekler = _load_yetenekler()

    # Mevcut kayıt var mı (email veya telefonla eşleştir)
    try:
        auth = st.session_state.get("auth_user", {})
        veli_email = auth.get("email", "")
        veli_ad = auth.get("name", "")
    except Exception:
        veli_email, veli_ad = "", ""

    mevcut = next((y for y in yetenekler if y.get("email") == veli_email and veli_email), None)

    if mevcut:
        st.success(f"✅ Kaydınız var — Son güncelleme: {mevcut.get('guncelleme_tarihi', '')[:16]}")

    # Kayıt formu
    with st.form("vyb_kayit_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            ad_soyad = st.text_input(
                "Ad Soyad *",
                value=mevcut.get("ad_soyad", veli_ad) if mevcut else veli_ad,
                key="_vyb_ad_widget",
            )
            telefon = st.text_input(
                "Telefon",
                value=mevcut.get("telefon", "") if mevcut else "",
                key="_vyb_tel_widget",
            )
            email = st.text_input(
                "E-posta",
                value=mevcut.get("email", veli_email) if mevcut else veli_email,
                key="_vyb_email_widget",
            )

        with c2:
            kategori = st.selectbox(
                "Meslek Kategorisi *",
                list(MESLEK_KATEGORILERI.keys()),
                format_func=lambda x: f"{MESLEK_KATEGORILERI[x]['ikon']} {MESLEK_KATEGORILERI[x]['ad']}",
                index=list(MESLEK_KATEGORILERI.keys()).index(mevcut.get("kategori", "diger"))
                      if mevcut and mevcut.get("kategori") in MESLEK_KATEGORILERI else 0,
                key="_vyb_kategori_widget",
            )
            meslekler = MESLEK_KATEGORILERI[kategori]["meslekler"]
            meslek = st.selectbox(
                "Meslek *",
                meslekler,
                index=meslekler.index(mevcut.get("meslek", meslekler[0]))
                      if mevcut and mevcut.get("meslek") in meslekler else 0,
                key="_vyb_meslek_widget",
            )
            deneyim_yil = st.number_input(
                "Deneyim (yıl)",
                min_value=0, max_value=60,
                value=mevcut.get("deneyim_yil", 5) if mevcut else 5,
                key="_vyb_deneyim_widget",
            )

        # Öğrenci bilgisi
        ogrenci_bilgisi = st.text_input(
            "Velisi olduğunuz öğrenci (ad + sınıf)",
            value=mevcut.get("ogrenci_bilgisi", "") if mevcut else "",
            placeholder="Örn: Ali Yılmaz — 9-A",
            key="_vyb_ogrenci_widget",
        )

        # Uzmanlık alanları
        uzmanlik = st.text_area(
            "Uzmanlık Alanlarınız / Detay",
            value=mevcut.get("uzmanlik", "") if mevcut else "",
            placeholder="Örn: Kalp cerrahisi, çocuk hastalıkları, kurumsal finans, gömülü sistemler vs.",
            height=60,
            key="_vyb_uzmanlik_widget",
        )

        # Katkı türü
        katki_turleri = st.multiselect(
            "Hangi tür katkıda bulunabilirsiniz?",
            KATKI_TURLERI,
            default=mevcut.get("katki_turleri", []) if mevcut else [],
            key="_vyb_katki_widget",
        )

        # Uygunluk
        uc1, uc2 = st.columns(2)
        with uc1:
            hafta_ici = st.checkbox(
                "Hafta içi (mesai saati dışı) uygun",
                value=mevcut.get("hafta_ici", True) if mevcut else True,
                key="_vyb_hafta_ici_widget",
            )
        with uc2:
            hafta_sonu = st.checkbox(
                "Hafta sonu uygun",
                value=mevcut.get("hafta_sonu", True) if mevcut else True,
                key="_vyb_hafta_sonu_widget",
            )

        notlar = st.text_input(
            "Ek Notlar (opsiyonel)",
            value=mevcut.get("notlar", "") if mevcut else "",
            placeholder="Özel bir konu, tercih vb.",
            key="_vyb_notlar_widget",
        )

        gonder = st.form_submit_button(
            "💾 Kaydet / Güncelle" if mevcut else "🚀 Yetenek Bankasına Katıl",
            type="primary", use_container_width=True,
        )

        if gonder:
            if not ad_soyad.strip():
                styled_info_banner("Ad Soyad zorunludur.", "warning")
                return
            if not katki_turleri:
                styled_info_banner("En az 1 katkı türü seçin.", "warning")
                return

            kayit = {
                "ad_soyad": ad_soyad.strip(),
                "telefon": telefon.strip(),
                "email": email.strip().lower(),
                "kategori": kategori,
                "meslek": meslek,
                "deneyim_yil": deneyim_yil,
                "uzmanlik": uzmanlik.strip(),
                "katki_turleri": katki_turleri,
                "hafta_ici": hafta_ici,
                "hafta_sonu": hafta_sonu,
                "notlar": notlar.strip(),
                "ogrenci_bilgisi": ogrenci_bilgisi.strip(),
                "aktif": True,
                "guncelleme_tarihi": datetime.now().isoformat(),
            }

            if mevcut:
                # Güncelle
                idx = next((i for i, y in enumerate(yetenekler) if y is mevcut), None)
                if idx is not None:
                    kayit["id"] = mevcut.get("id", f"VYB-{idx+1:04d}")
                    kayit["olusturma_tarihi"] = mevcut.get("olusturma_tarihi", datetime.now().isoformat())
                    yetenekler[idx] = kayit
            else:
                kayit["id"] = f"VYB-{len(yetenekler)+1:04d}"
                kayit["olusturma_tarihi"] = datetime.now().isoformat()
                yetenekler.append(kayit)

            _save_yetenekler(yetenekler)
            st.balloons()
            st.success(f"✅ Kaydınız alındı! ID: {kayit['id']}")
            st.rerun()


# ══════════════════════════════════════════════════════════════
# OKUL YÖNETİMİ PANELİ — Yetenekleri filtrele + davet gönder
# ══════════════════════════════════════════════════════════════

def render_okul_yonetim_panel():
    """Okul yöneticileri için — yetenek havuzu + davet sistemi."""
    styled_section("📚 Yetenek Havuzu (Yönetim)", "#4F46E5")

    yetenekler = _load_yetenekler()
    davetler = _load_davetler()

    # İstatistik
    toplam = len(yetenekler)
    aktif = sum(1 for y in yetenekler if y.get("aktif", True))
    kategori_sayi = len(set(y.get("kategori", "") for y in yetenekler))

    styled_stat_row([
        ("Toplam Veli", str(toplam), "#4F46E5", "👥"),
        ("Aktif", str(aktif), "#059669", "✅"),
        ("Farklı Kategori", str(kategori_sayi), "#D97706", "🏷️"),
        ("Davet", str(len(davetler)), "#EC4899", "📧"),
    ])

    if toplam == 0:
        styled_info_banner(
            "Henüz veli kaydı yok. Velilere duyurarak katılım çağrısı yapın.",
            "info",
        )
        return

    # Filtreler
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_kategori = st.selectbox(
            "Kategori",
            ["Tümü"] + list(MESLEK_KATEGORILERI.keys()),
            format_func=lambda x: "Tümü" if x == "Tümü" else f"{MESLEK_KATEGORILERI[x]['ikon']} {MESLEK_KATEGORILERI[x]['ad']}",
            key="_vyb_f_kategori",
        )
    with fc2:
        f_katki = st.selectbox(
            "Katkı Türü",
            ["Tümü"] + KATKI_TURLERI,
            key="_vyb_f_katki",
        )
    with fc3:
        f_arama = st.text_input("Arama (ad, meslek, uzmanlık)", key="_vyb_f_arama")

    # Filtrele
    filtered = yetenekler
    if f_kategori != "Tümü":
        filtered = [y for y in filtered if y.get("kategori") == f_kategori]
    if f_katki != "Tümü":
        filtered = [y for y in filtered if f_katki in y.get("katki_turleri", [])]
    if f_arama:
        q = f_arama.lower()
        filtered = [y for y in filtered if
                    q in y.get("ad_soyad", "").lower() or
                    q in y.get("meslek", "").lower() or
                    q in y.get("uzmanlik", "").lower()]

    st.markdown(f"**{len(filtered)} veli listeleniyor**")

    for yt in filtered:
        kat_info = MESLEK_KATEGORILERI.get(yt.get("kategori", "diger"), MESLEK_KATEGORILERI["diger"])
        aktif_badge = "🟢" if yt.get("aktif", True) else "⚫"

        with st.expander(
            f"{aktif_badge} {kat_info['ikon']} {yt.get('ad_soyad', '')} — {yt.get('meslek', '')} ({yt.get('deneyim_yil', 0)} yıl)"
        ):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**Meslek:** {yt.get('meslek', '')} — **Deneyim:** {yt.get('deneyim_yil', 0)} yıl")
                if yt.get("uzmanlik"):
                    st.markdown(f"**Uzmanlık:** {yt['uzmanlik']}")
                if yt.get("ogrenci_bilgisi"):
                    st.markdown(f"**Öğrencisi:** {yt['ogrenci_bilgisi']}")
                if yt.get("notlar"):
                    st.caption(f"📝 {yt['notlar']}")

            with c2:
                st.markdown(f"**📞** {yt.get('telefon', '—')}")
                st.markdown(f"**📧** {yt.get('email', '—')}")
                uygunluk = []
                if yt.get("hafta_ici"):
                    uygunluk.append("Hafta içi")
                if yt.get("hafta_sonu"):
                    uygunluk.append("Hafta sonu")
                st.caption(f"🗓️ {', '.join(uygunluk) if uygunluk else 'Uygunluk belirtilmedi'}")

            st.markdown("**Katkı Türleri:**")
            for kt in yt.get("katki_turleri", []):
                st.markdown(f"  • {kt}")

            # Davet gönder
            st.divider()
            with st.form(f"davet_form_{yt['id']}"):
                dc1, dc2 = st.columns(2)
                with dc1:
                    davet_tur = st.selectbox(
                        "Davet Türü",
                        yt.get("katki_turleri", KATKI_TURLERI),
                        key=f"_dvt_tur_{yt['id']}",
                    )
                with dc2:
                    davet_tarih = st.date_input(
                        "Tarih",
                        key=f"_dvt_tarih_{yt['id']}",
                    )

                davet_konu = st.text_input(
                    "Konu",
                    placeholder="Örn: 11. sınıflara kariyer sunumu",
                    key=f"_dvt_konu_{yt['id']}",
                )

                davet_mesaj = st.text_area(
                    "Mesaj (AI yardımcı olabilir)",
                    placeholder="Sayın veli, X konusunda tecrübenizden yararlanmak isteriz...",
                    height=80,
                    key=f"_dvt_mesaj_{yt['id']}",
                )

                if st.form_submit_button(f"📧 Davet Gönder", type="primary"):
                    if not davet_konu or not davet_mesaj:
                        styled_info_banner("Konu ve mesaj zorunludur.", "warning")
                    else:
                        davetler.append({
                            "id": f"DVT-{len(davetler)+1:04d}",
                            "veli_id": yt["id"],
                            "veli_ad": yt["ad_soyad"],
                            "veli_email": yt.get("email", ""),
                            "davet_tur": davet_tur,
                            "konu": davet_konu,
                            "mesaj": davet_mesaj,
                            "tarih": davet_tarih.isoformat(),
                            "durum": "Gönderildi",
                            "olusturma_tarihi": datetime.now().isoformat(),
                        })
                        _save_davetler(davetler)
                        st.success(f"✅ Davet kaydedildi ve e-posta gönderilecek: {yt.get('email', '—')}")
                        st.rerun()


# ══════════════════════════════════════════════════════════════
# DAVETLER PANELİ
# ══════════════════════════════════════════════════════════════

def render_davetler_panel():
    """Gönderilen davetlerin takibi."""
    styled_section("📧 Davetler & Geri Dönüşler", "#EC4899")

    davetler = _load_davetler()
    if not davetler:
        styled_info_banner("Henüz davet gönderilmedi.", "info")
        return

    # İstatistik
    gonderildi = sum(1 for d in davetler if d.get("durum") == "Gönderildi")
    kabul = sum(1 for d in davetler if d.get("durum") == "Kabul")
    red = sum(1 for d in davetler if d.get("durum") == "Red")
    tamamlandi = sum(1 for d in davetler if d.get("durum") == "Tamamlandı")

    styled_stat_row([
        ("Toplam", str(len(davetler)), "#64748B", "📧"),
        ("Gönderildi", str(gonderildi), "#0284C7", "📨"),
        ("Kabul", str(kabul), "#059669", "✅"),
        ("Tamamlandı", str(tamamlandi), "#4F46E5", "🎉"),
    ])

    for dvt in reversed(davetler):
        durum = dvt.get("durum", "Gönderildi")
        durum_renk = {"Gönderildi": "#0284C7", "Kabul": "#059669",
                       "Red": "#DC2626", "Tamamlandı": "#4F46E5"}.get(durum, "#64748B")
        with st.expander(f"📧 {dvt.get('id')} — {dvt.get('veli_ad')} ({durum})"):
            st.markdown(f"**Konu:** {dvt.get('konu', '')}")
            st.markdown(f"**Tarih:** {dvt.get('tarih', '')}")
            st.markdown(f"**Tür:** {dvt.get('davet_tur', '')}")
            st.caption(f"📧 {dvt.get('veli_email', '—')}")
            st.markdown(f"**Mesaj:**")
            st.markdown(f"> {dvt.get('mesaj', '')[:300]}")

            # Durum güncelleme
            yeni_durum = st.selectbox(
                "Durum",
                ["Gönderildi", "Kabul", "Red", "Tamamlandı"],
                index=["Gönderildi", "Kabul", "Red", "Tamamlandı"].index(durum),
                key=f"_dvt_durum_{dvt['id']}",
            )
            if yeni_durum != durum:
                dvt["durum"] = yeni_durum
                dvt["guncelleme_tarihi"] = datetime.now().isoformat()
                _save_davetler(davetler)
                st.success("Güncellendi.")
                st.rerun()


# ══════════════════════════════════════════════════════════════
# ANA PANEL
# ══════════════════════════════════════════════════════════════

def render_veli_yetenek_bankasi():
    """Ana panel — tab ile veli/yönetim ayrımı."""
    styled_section("💼 Veli Yetenek Bankası", "#4F46E5")

    styled_info_banner(
        "Okul-Veli Ortaklığı — Velilerin mesleki deneyimlerini okulun içerik zenginliğine dönüştürür. "
        "Kariyer günleri, atölyeler, mentorluk fırsatları.",
        "info", "💼",
    )

    tabs = st.tabs([
        "👤 Ben Kayıt Olmak İstiyorum (Veli)",
        "📚 Yetenek Havuzu (Yönetim)",
        "📧 Davetler",
    ])

    with tabs[0]:
        render_veli_kayit_panel()

    with tabs[1]:
        try:
            auth = st.session_state.get("auth_user", {})
            rol = auth.get("role", "").lower()
            yetkili = any(r in rol for r in ["mudur", "müdür", "yonetici", "kurucu", "admin", "koordinator"])
        except Exception:
            yetkili = True  # Dev

        if yetkili:
            render_okul_yonetim_panel()
        else:
            styled_info_banner("Bu panele sadece okul yönetimi erişebilir.", "warning", "🔒")

    with tabs[2]:
        render_davetler_panel()
