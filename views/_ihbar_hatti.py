"""
Anonim İhbar Hattı — Öğrenci Güvenliği için Gizli Bildirim Sistemi
===================================================================
Öğrenciler, veliler, personel için %100 anonim bildirim kanalı.
Akran zorbalığı, uyuşturucu, intihar riski, şiddet — hayat kurtarır.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime
from typing import Callable

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# KATEGORİLER & SEVİYELER
# ══════════════════════════════════════════════════════════════

IHBAR_KATEGORILERI = {
    "akran_zorbaligi": {
        "ad": "Akran Zorbalığı / Şiddet",
        "ikon": "⚠️",
        "renk": "#DC2626",
        "seviye": "Yüksek",
        "alt_kategoriler": [
            "Fiziksel şiddet", "Sözel taciz", "Sosyal dışlama",
            "Siber zorbalık", "Tehdit",
        ],
    },
    "intihar_riski": {
        "ad": "İntihar / Kendine Zarar Riski",
        "ikon": "🆘",
        "renk": "#991B1B",
        "seviye": "Kritik",
        "alt_kategoriler": [
            "Kendine zarar verme işaretleri",
            "İntihardan bahsetme",
            "Umutsuzluk ifadeleri",
            "Sosyal izolasyon",
        ],
    },
    "madde_kullanim": {
        "ad": "Madde Kullanımı",
        "ikon": "💊",
        "renk": "#7C2D12",
        "seviye": "Kritik",
        "alt_kategoriler": [
            "Uyuşturucu şüphesi", "Alkol kullanımı",
            "Sigara", "Reçetesiz ilaç", "Vape/elektronik sigara",
        ],
    },
    "cinsel_taciz": {
        "ad": "Cinsel Taciz / İstismar",
        "ikon": "🚨",
        "renk": "#831843",
        "seviye": "Kritik",
        "alt_kategoriler": [
            "Öğrenci-öğrenci arası",
            "Yetişkin tarafından şüphe",
            "Uygunsuz mesaj/görüntü",
            "Diğer",
        ],
    },
    "aile_ici_siddet": {
        "ad": "Aile İçi Şiddet / İhmal",
        "ikon": "🏠",
        "renk": "#9A3412",
        "seviye": "Kritik",
        "alt_kategoriler": [
            "Fiziksel şiddet işareti", "Duygusal şiddet",
            "İhmal (yiyecek, hijyen)", "Evden kaçma sinyali",
        ],
    },
    "akademik_kopya": {
        "ad": "Akademik Sahtekarlık",
        "ikon": "📝",
        "renk": "#D97706",
        "seviye": "Orta",
        "alt_kategoriler": [
            "Kopya", "Sahte belge", "Toplu kopya", "Başkasının ödevi",
        ],
    },
    "personel_sikayet": {
        "ad": "Personel Şikayeti",
        "ikon": "👤",
        "renk": "#D97706",
        "seviye": "Yüksek",
        "alt_kategoriler": [
            "Uygunsuz davranış", "Ayrımcılık",
            "Mesleki yetersizlik", "Adaletsizlik",
        ],
    },
    "diger": {
        "ad": "Diğer",
        "ikon": "📋",
        "renk": "#64748B",
        "seviye": "Orta",
        "alt_kategoriler": ["Diğer güvenlik konusu"],
    },
}

IHBAR_DURUMLARI = ["Yeni", "İnceleniyor", "Müdahale Edildi", "Çözüldü", "Asılsız"]


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _ihbar_path() -> str:
    """Anonim ihbar veri dosyası (tenant-aware)."""
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "ihbar_hatti")
    except Exception:
        d = os.path.join("data", "ihbar_hatti")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "ihbarlar.json")


def _load_ihbarlar() -> list[dict]:
    p = _ihbar_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_ihbarlar(data: list[dict]) -> None:
    with open(_ihbar_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _gen_anonim_id() -> str:
    """Sadece rastgele ID — hiç kişisel bilgi yok."""
    return f"IHB-{uuid.uuid4().hex[:10].upper()}"


def _hash_content(content: str) -> str:
    """Tekrar eden ihbarı tespit için içerik hash'i."""
    return hashlib.sha256(content.lower().strip().encode("utf-8")).hexdigest()[:12]


# ══════════════════════════════════════════════════════════════
# GÖNDERİM (Herkes erişebilir — öğrenci, veli, personel)
# ══════════════════════════════════════════════════════════════

def render_ihbar_gonder_panel():
    """Anonim ihbar gönderim formu."""
    styled_section("🤫 Anonim İhbar Hattı", "#DC2626")

    styled_info_banner(
        "Bu form **tamamen anonimdir**. Adınız, IP adresiniz, kullanıcı bilginiz kaydedilmez. "
        "Sadece rehber ve okul yönetimi görebilir. Acil durumlarda 183'ü arayın.",
        "info", "🔒",
    )

    # Sıcak hat uyarısı
    st.markdown("""
    <div style="background:#991B1B20;border:2px solid #991B1B;border-radius:12px;
    padding:14px 18px;margin:12px 0;">
        <div style="color:#FCA5A5;font-weight:700;margin-bottom:6px;">🆘 Acil Durum?</div>
        <div style="color:#FAFAFA;font-size:0.88rem;line-height:1.6;">
            • Hayati tehlike: <strong>112</strong><br/>
            • ALO 183 Çocuk Danışma: <strong>183</strong><br/>
            • İntihar önleme hattı: <strong>182</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Form
    with st.form("anonim_ihbar_form", clear_on_submit=True):
        ic1, ic2 = st.columns(2)

        with ic1:
            kategori = st.selectbox(
                "Konu Kategorisi",
                list(IHBAR_KATEGORILERI.keys()),
                format_func=lambda x: f"{IHBAR_KATEGORILERI[x]['ikon']} {IHBAR_KATEGORILERI[x]['ad']}",
                key="_ih_kategori_widget",
            )
            alt_kategoriler = IHBAR_KATEGORILERI[kategori]["alt_kategoriler"]
            alt_kategori = st.selectbox(
                "Alt Kategori",
                alt_kategoriler,
                key="_ih_alt_kategori_widget",
            )

        with ic2:
            # Opsiyonel: olay yeri ve zaman
            nerede = st.text_input(
                "Nerede oldu? (opsiyonel)",
                placeholder="Örn: Koridor, tuvalet, dışarıda...",
                key="_ih_nerede_widget",
            )
            ne_zaman = st.text_input(
                "Ne zaman oldu? (opsiyonel)",
                placeholder="Örn: Bugün öğlen, geçen hafta...",
                key="_ih_ne_zaman_widget",
            )

        aciklama = st.text_area(
            "Ne olduğunu anlatın (ayrıntılı ama **isim vermeden**):",
            placeholder="Gördüğünüz/yaşadığınız durumu olabildiğince detaylı anlatın. "
                        "İsim yerine 'bir öğrenci', 'bir öğretmen' gibi ifadeler kullanın. "
                        "Yer, zaman, kişi sayısı önemlidir.",
            height=140,
            key="_ih_aciklama_widget",
        )

        # Kendimle ilgili mi, başkasıyla mı
        kim_icin = st.radio(
            "Bu ihbar kiminle ilgili?",
            ["Kendim hakkında", "Arkadaşım/tanıdığım hakkında", "Tanık olduğum bir olay"],
            horizontal=True,
            key="_ih_kim_widget",
        )

        # Geri dönüş isteği
        geri_donus = st.checkbox(
            "Konuyla ilgili bilgilendirilmek istiyorum (takip kodu oluşturulur — anonim kalır)",
            key="_ih_geri_widget",
        )

        col_submit, col_acil = st.columns([3, 1])
        with col_submit:
            gonder = st.form_submit_button(
                "🔒 Anonim Gönder",
                type="primary",
                use_container_width=True,
            )
        with col_acil:
            acil_mi = st.form_submit_button(
                "🆘 ACİL",
                use_container_width=True,
            )

        if gonder or acil_mi:
            if not aciklama or len(aciklama.strip()) < 20:
                styled_info_banner(
                    "Lütfen en az 20 karakter detay yazın. Anonim kalsanız bile, durumu anlamamız için bilgi gerekli.",
                    "warning",
                )
                return

            kat_info = IHBAR_KATEGORILERI[kategori]
            seviye = "Kritik" if acil_mi else kat_info["seviye"]

            ihbarlar = _load_ihbarlar()
            content_hash = _hash_content(aciklama)

            # Aynı ihbar tekrar ediyor mu (spam önleme)
            existing = next((i for i in ihbarlar if i.get("hash") == content_hash
                             and i.get("durum") not in ("Çözüldü", "Asılsız")), None)
            if existing:
                styled_info_banner(
                    f"Bu konu daha önce bildirilmiş ve incelenmekte. Takip ID: **{existing.get('anonim_id')}**",
                    "info",
                )
                return

            anonim_id = _gen_anonim_id()
            yeni_ihbar = {
                "anonim_id": anonim_id,
                "hash": content_hash,
                "kategori": kategori,
                "kategori_ad": kat_info["ad"],
                "alt_kategori": alt_kategori,
                "seviye": seviye,
                "aciklama": aciklama.strip(),
                "nerede": nerede.strip(),
                "ne_zaman": ne_zaman.strip(),
                "kim_icin": kim_icin,
                "geri_donus_istiyor": geri_donus,
                "durum": "Yeni",
                "olusturma_tarihi": datetime.now().isoformat(),
                "guncelleme_tarihi": datetime.now().isoformat(),
                "rehber_notlari": [],
                "aksiyon_gecmisi": [],
                "takip_kodu": hashlib.sha256(f"{anonim_id}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper() if geri_donus else "",
            }
            ihbarlar.append(yeni_ihbar)
            _save_ihbarlar(ihbarlar)

            # Başarı mesajı
            st.balloons()
            styled_info_banner(
                f"✅ İhbarınız güvenli bir şekilde iletildi. **Anonim ID: {anonim_id}**. "
                f"{'Takip kodunuz: **' + yeni_ihbar['takip_kodu'] + '**' if geri_donus else ''} "
                f"Rehber ekibi en kısa sürede değerlendirecek.",
                "success",
            )

    # Takip Kodu ile Sorgula
    with st.expander("🔍 Daha Önce Bildirdiğim İhbarı Sorgula"):
        takip_kodu = st.text_input("Takip Kodu", key="_ih_takip_sorgu_widget",
                                    placeholder="Örn: A1B2C3D4").upper().strip()
        if takip_kodu:
            ihbarlar = _load_ihbarlar()
            bulunan = next((i for i in ihbarlar if i.get("takip_kodu") == takip_kodu), None)
            if bulunan:
                st.markdown(f"**Durum:** {bulunan.get('durum', 'Yeni')}")
                st.markdown(f"**Son Güncelleme:** {bulunan.get('guncelleme_tarihi', '')[:16]}")
                if bulunan.get("geri_donus_mesaji"):
                    st.markdown(f"**Rehber Mesajı:** {bulunan['geri_donus_mesaji']}")
            else:
                styled_info_banner("Takip kodu bulunamadı.", "warning")


# ══════════════════════════════════════════════════════════════
# İNCELEME (Sadece Rehber / Müdür Erişimi)
# ══════════════════════════════════════════════════════════════

def _kullanici_yetkili_mi() -> bool:
    """Sadece rehber/müdür/kurucu görebilir."""
    try:
        auth = st.session_state.get("auth_user", {})
        rol = auth.get("role", "").lower()
        return any(r in rol for r in ["rehber", "mudur", "müdür", "yonetici", "kurucu", "admin"])
    except Exception:
        return False


def render_ihbar_inceleme_panel():
    """Rehber/müdür için ihbar inceleme paneli."""
    styled_section("🔐 Anonim İhbar İnceleme (Yetkili Personel)", "#991B1B")

    if not _kullanici_yetkili_mi():
        styled_info_banner(
            "Bu panele sadece Rehberlik, Müdür Yardımcısı, Müdür ve Kurucu erişebilir.",
            "warning", "🔒",
        )
        return

    ihbarlar = _load_ihbarlar()

    # İstatistik
    toplam = len(ihbarlar)
    yeni = sum(1 for i in ihbarlar if i.get("durum") == "Yeni")
    kritik = sum(1 for i in ihbarlar if i.get("seviye") == "Kritik" and i.get("durum") not in ("Çözüldü", "Asılsız"))
    cozuldu = sum(1 for i in ihbarlar if i.get("durum") == "Çözüldü")

    styled_stat_row([
        ("Toplam", str(toplam), "#64748B", "📋"),
        ("Yeni", str(yeni), "#DC2626", "🆕"),
        ("Kritik Açık", str(kritik), "#991B1B", "🚨"),
        ("Çözüldü", str(cozuldu), "#059669", "✅"),
    ])

    # Filtreler
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_durum = st.selectbox("Durum", ["Tümü"] + IHBAR_DURUMLARI, key="_ih_f_durum")
    with fc2:
        f_kategori = st.selectbox(
            "Kategori",
            ["Tümü"] + list(IHBAR_KATEGORILERI.keys()),
            format_func=lambda x: "Tümü" if x == "Tümü" else f"{IHBAR_KATEGORILERI[x]['ikon']} {IHBAR_KATEGORILERI[x]['ad']}",
            key="_ih_f_kategori",
        )
    with fc3:
        f_seviye = st.selectbox("Seviye", ["Tümü", "Kritik", "Yüksek", "Orta"], key="_ih_f_seviye")

    # Filtrele
    filtered = ihbarlar
    if f_durum != "Tümü":
        filtered = [i for i in filtered if i.get("durum") == f_durum]
    if f_kategori != "Tümü":
        filtered = [i for i in filtered if i.get("kategori") == f_kategori]
    if f_seviye != "Tümü":
        filtered = [i for i in filtered if i.get("seviye") == f_seviye]

    # Sırala (kritik ve yeni önce)
    seviye_oncelik = {"Kritik": 0, "Yüksek": 1, "Orta": 2}
    filtered.sort(
        key=lambda x: (
            seviye_oncelik.get(x.get("seviye", "Orta"), 3),
            0 if x.get("durum") == "Yeni" else 1,
            x.get("olusturma_tarihi", ""),
        ),
        reverse=False,
    )

    if not filtered:
        styled_info_banner("Filtreye uyan ihbar bulunamadı.", "info")
        return

    # Liste
    for ihbar in filtered:
        kat = IHBAR_KATEGORILERI.get(ihbar.get("kategori", "diger"), IHBAR_KATEGORILERI["diger"])
        seviye = ihbar.get("seviye", "Orta")
        durum = ihbar.get("durum", "Yeni")

        seviye_renk = {"Kritik": "#991B1B", "Yüksek": "#DC2626", "Orta": "#D97706"}.get(seviye, "#64748B")
        durum_renk = {"Yeni": "#DC2626", "İnceleniyor": "#D97706", "Müdahale Edildi": "#0284C7",
                       "Çözüldü": "#059669", "Asılsız": "#64748B"}.get(durum, "#64748B")

        with st.expander(
            f"{kat['ikon']} [{seviye}] {kat['ad']} — {ihbar.get('anonim_id', '')} ({durum})",
            expanded=(durum == "Yeni" and seviye == "Kritik"),
        ):
            tarih = ihbar.get("olusturma_tarihi", "")[:16].replace("T", " ")
            st.markdown(f"""
            <div style="background:{seviye_renk}15;border-left:4px solid {seviye_renk};
            border-radius:8px;padding:10px 14px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:700;color:{seviye_renk};">Seviye: {seviye}</span>
                    <span style="font-size:0.82rem;color:#94A3B8;">{tarih}</span>
                </div>
                <div style="color:#E4E4E7;margin-top:4px;font-size:0.9rem;">
                    <strong>Alt Kategori:</strong> {ihbar.get('alt_kategori', '')}<br/>
                    <strong>Kim için:</strong> {ihbar.get('kim_icin', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**📝 Açıklama:**")
            st.markdown(f"> {ihbar.get('aciklama', '')}")

            if ihbar.get("nerede"):
                st.markdown(f"**📍 Nerede:** {ihbar['nerede']}")
            if ihbar.get("ne_zaman"):
                st.markdown(f"**🕒 Ne zaman:** {ihbar['ne_zaman']}")

            # Durum güncelleme
            st.divider()
            uc1, uc2 = st.columns(2)
            with uc1:
                yeni_durum = st.selectbox(
                    "Durum Değiştir",
                    IHBAR_DURUMLARI,
                    index=IHBAR_DURUMLARI.index(durum) if durum in IHBAR_DURUMLARI else 0,
                    key=f"_ih_durum_{ihbar['anonim_id']}",
                )
            with uc2:
                yeni_not = st.text_input(
                    "İşlem Notu (dahili)",
                    key=f"_ih_not_{ihbar['anonim_id']}",
                    placeholder="Ne yapıldı? Kimle görüşüldü?",
                )

            geri_donus_msg = ""
            if ihbar.get("geri_donus_istiyor"):
                geri_donus_msg = st.text_area(
                    f"İhbar eden için mesaj (takip kodu: {ihbar.get('takip_kodu', '—')})",
                    value=ihbar.get("geri_donus_mesaji", ""),
                    key=f"_ih_geri_donus_{ihbar['anonim_id']}",
                    height=60,
                )

            uc3, uc4 = st.columns(2)
            with uc3:
                if st.button("💾 Güncelle", key=f"_ih_kaydet_{ihbar['anonim_id']}", type="primary"):
                    # İhbarı bul ve güncelle
                    idx = next((i for i, x in enumerate(ihbarlar) if x["anonim_id"] == ihbar["anonim_id"]), None)
                    if idx is not None:
                        ihbarlar[idx]["durum"] = yeni_durum
                        ihbarlar[idx]["guncelleme_tarihi"] = datetime.now().isoformat()
                        if yeni_not:
                            ihbarlar[idx].setdefault("rehber_notlari", []).append({
                                "not": yeni_not,
                                "tarih": datetime.now().isoformat(),
                            })
                        if geri_donus_msg:
                            ihbarlar[idx]["geri_donus_mesaji"] = geri_donus_msg
                        ihbarlar[idx].setdefault("aksiyon_gecmisi", []).append({
                            "durum": yeni_durum, "tarih": datetime.now().isoformat(),
                        })
                        _save_ihbarlar(ihbarlar)
                        st.success("Güncellendi.")
                        st.rerun()
            with uc4:
                if ihbar.get("aksiyon_gecmisi"):
                    st.caption(f"📜 {len(ihbar['aksiyon_gecmisi'])} önceki işlem kaydı")

            # Önceki notlar
            if ihbar.get("rehber_notlari"):
                with st.expander("📜 Önceki Notlar"):
                    for n in ihbar["rehber_notlari"]:
                        st.markdown(f"• *{n.get('tarih', '')[:16]}*: {n.get('not', '')}")


# ══════════════════════════════════════════════════════════════
# DASHBOARD WIDGET (Kritik uyarılar için)
# ══════════════════════════════════════════════════════════════

def render_ihbar_uyari_badge():
    """Dashboard'lara eklenebilecek kritik ihbar uyarı badge'i."""
    if not _kullanici_yetkili_mi():
        return

    ihbarlar = _load_ihbarlar()
    kritik_acik = sum(1 for i in ihbarlar
                       if i.get("seviye") == "Kritik" and i.get("durum") not in ("Çözüldü", "Asılsız"))
    yeni = sum(1 for i in ihbarlar if i.get("durum") == "Yeni")

    if kritik_acik == 0 and yeni == 0:
        return

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#991B1B,#7F1D1D);border:2px solid #DC2626;
    border-radius:12px;padding:14px 18px;margin:12px 0;color:#FAFAFA;
    box-shadow:0 4px 14px rgba(153,27,27,0.4);">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div style="font-weight:800;font-size:1.05rem;">🚨 Anonim İhbar Uyarısı</div>
                <div style="font-size:0.85rem;opacity:0.9;margin-top:4px;">
                    {kritik_acik} kritik ihbar aktif | {yeni} yeni ihbar değerlendirme bekliyor
                </div>
            </div>
            <div style="font-size:2rem;">⚠️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
