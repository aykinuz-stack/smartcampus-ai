"""
Kampüs Wiki — Okul Bilgi Bankası
=====================================
Crowd-sourced bilgi havuzu: "Matematik zümresinin soru formatı nedir?",
"Servis kuralları", "Kayıp eşya süreci" — herkes yazar/düzenler, öğretmen onaylar.
Yeni gelen personel ve veliler için ilaç.
"""
from __future__ import annotations

import json
import os
from datetime import datetime

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# KATEGORİLER
# ══════════════════════════════════════════════════════════════

WIKI_KATEGORILERI = {
    "yeni_personel": {"ad": "Yeni Personel", "ikon": "👋", "renk": "#4F46E5"},
    "akademik":      {"ad": "Akademik", "ikon": "🎓", "renk": "#2563EB"},
    "veli":          {"ad": "Veli Rehberi", "ikon": "👨‍👩‍👧", "renk": "#EC4899"},
    "ogrenci":       {"ad": "Öğrenci Rehberi", "ikon": "🎒", "renk": "#7C3AED"},
    "operasyon":     {"ad": "Operasyon", "ikon": "⚙️", "renk": "#64748B"},
    "guvenlik":      {"ad": "Güvenlik", "ikon": "🛡️", "renk": "#DC2626"},
    "saglik":        {"ad": "Sağlık", "ikon": "🏥", "renk": "#059669"},
    "servis":        {"ad": "Servis/Ulaşım", "ikon": "🚌", "renk": "#D97706"},
    "yemekhane":     {"ad": "Yemekhane", "ikon": "🍽️", "renk": "#EA580C"},
    "etkinlik":      {"ad": "Etkinlik", "ikon": "🎉", "renk": "#DB2777"},
    "teknoloji":     {"ad": "Teknoloji/IT", "ikon": "💻", "renk": "#7C3AED"},
    "sss":           {"ad": "Sıkça Sorulan", "ikon": "❓", "renk": "#0891B2"},
}

# Onay durumları
ONAY_DURUMLARI = ["Taslak", "İncelemede", "Onaylandı", "Reddedildi"]


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _wiki_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "kampus_wiki")
    except Exception:
        d = os.path.join("data", "kampus_wiki")
    os.makedirs(d, exist_ok=True)
    return d


def _wiki_path() -> str:
    return os.path.join(_wiki_dir(), "makaleler.json")


def _load_makaleler() -> list[dict]:
    p = _wiki_path()
    if not os.path.exists(p):
        # İlk kez — örnek makaleleri ekle
        makaleler = _ornek_makaleler()
        _save_makaleler(makaleler)
        return makaleler
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_makaleler(data: list[dict]) -> None:
    with open(_wiki_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ornek_makaleler() -> list[dict]:
    """İlk açılışta örnek içerikle başlat."""
    now = datetime.now().isoformat()
    return [
        {
            "id": "WIKI-0001",
            "kategori": "yeni_personel",
            "baslik": "İlk Gün Kontrol Listesi",
            "icerik": (
                "## Yeni Personel İlk Gün\n\n"
                "- 🎫 Personel kartını İK'dan al\n"
                "- 💻 Bilgisayar ve e-posta hesabı talep et (IT Destek)\n"
                "- 🗺️ Kampüs turuna katıl\n"
                "- 📋 Görev tanımını zümre başkanından öğren\n"
                "- 🔑 Odalarını kapı kodu ve kilit bilgisi al\n"
                "- ☕ Çay/kahve servisi ve yemekhane saatlerini öğren\n\n"
                "İletişim: ik@okul.edu.tr"
            ),
            "yazar": "İK Müdürü",
            "onay_durumu": "Onaylandı",
            "olusturma_tarihi": now,
            "guncelleme_tarihi": now,
            "begen_sayisi": 12,
            "goruntulenme": 145,
            "etiketler": ["onboarding", "yeni", "ilk-gün"],
        },
        {
            "id": "WIKI-0002",
            "kategori": "servis",
            "baslik": "Servis Kullanım Kuralları",
            "icerik": (
                "## Servis Kullanım Kuralları\n\n"
                "### Genel Kurallar\n"
                "- Servis saatleri 07:30 — 08:15 arası\n"
                "- Okula gelmeden önce veli bilgilendirmesi yapılır\n"
                "- Duraklarda en az 5 dakika önce hazır olunmalıdır\n\n"
                "### Servis Şoförü İletişim\n"
                "- Şoför Ali Bey: 0555-111-2222\n"
                "- Servis Sorumlusu: 0555-333-4444\n\n"
                "### Arıza/Sorun\n"
                "Servis arıza durumunda okul müdüriyetine bildirim yapılır."
            ),
            "yazar": "İdare",
            "onay_durumu": "Onaylandı",
            "olusturma_tarihi": now,
            "guncelleme_tarihi": now,
            "begen_sayisi": 8,
            "goruntulenme": 234,
            "etiketler": ["servis", "ulaşım", "kural"],
        },
        {
            "id": "WIKI-0003",
            "kategori": "sss",
            "baslik": "Sık Sorulan Sorular",
            "icerik": (
                "## Sık Sorulan Sorular\n\n"
                "### Q: Okul saatleri nedir?\n"
                "**A:** 08:30 — 15:45\n\n"
                "### Q: Revir saatleri?\n"
                "**A:** 09:00 — 14:00 her gün\n\n"
                "### Q: Öğle yemeği nerede?\n"
                "**A:** 2. katta yemekhane, 12:00-13:00 arası\n\n"
                "### Q: Veli görüşme günleri?\n"
                "**A:** Her Perşembe 14:00-16:00\n\n"
                "### Q: Karne dağıtımı ne zaman?\n"
                "**A:** Dönem sonu, 2. hafta Perşembe"
            ),
            "yazar": "Okul Yönetimi",
            "onay_durumu": "Onaylandı",
            "olusturma_tarihi": now,
            "guncelleme_tarihi": now,
            "begen_sayisi": 25,
            "goruntulenme": 523,
            "etiketler": ["sss", "bilgi", "saat"],
        },
    ]


# ══════════════════════════════════════════════════════════════
# ANA PANEL
# ══════════════════════════════════════════════════════════════

def render_kampus_wiki():
    """Kampüs Wiki ana paneli."""
    styled_section("📚 Kampüs Wiki", "#4F46E5")

    styled_info_banner(
        "Okulun bilgi havuzu — herkes katkıda bulunur, yönetim onaylar. "
        "Yeni personel, veli ve öğrenci için rehber.",
        "info", "📚",
    )

    makaleler = _load_makaleler()
    onayli_makaleler = [m for m in makaleler if m.get("onay_durumu") == "Onaylandı"]

    # İstatistik
    toplam = len(makaleler)
    onayli = len(onayli_makaleler)
    taslak = sum(1 for m in makaleler if m.get("onay_durumu") == "Taslak")
    incele = sum(1 for m in makaleler if m.get("onay_durumu") == "İncelemede")
    toplam_goruntulenme = sum(m.get("goruntulenme", 0) for m in makaleler)

    styled_stat_row([
        ("Toplam Makale", str(toplam), "#4F46E5", "📚"),
        ("Onaylı", str(onayli), "#059669", "✅"),
        ("İncelemede", str(incele), "#D97706", "⏳"),
        ("Görüntülenme", str(toplam_goruntulenme), "#EC4899", "👁️"),
    ])

    tabs = st.tabs(["🔍 Gözat", "➕ Yeni Makale", "✅ Onay Paneli", "📊 İstatistik"])

    # ── Tab 1: Gözat ──
    with tabs[0]:
        # Arama
        arama = st.text_input(
            "🔍 Ara (başlık, içerik, etiket)",
            key="_wiki_arama_widget",
            placeholder="Örn: servis, yemekhane, karne",
        )

        # Kategori filtresi
        kategori_options = ["Tümü"] + list(WIKI_KATEGORILERI.keys())
        sel_kategori = st.selectbox(
            "Kategori",
            kategori_options,
            format_func=lambda x: "🌍 Tümü" if x == "Tümü" else f"{WIKI_KATEGORILERI[x]['ikon']} {WIKI_KATEGORILERI[x]['ad']}",
            key="_wiki_kategori_widget",
        )

        # Filtrele
        filtered = onayli_makaleler
        if sel_kategori != "Tümü":
            filtered = [m for m in filtered if m.get("kategori") == sel_kategori]
        if arama:
            q = arama.lower()
            filtered = [m for m in filtered if
                        q in m.get("baslik", "").lower() or
                        q in m.get("icerik", "").lower() or
                        any(q in t.lower() for t in m.get("etiketler", []))]

        # Sırala (beğeni + görüntülenme)
        filtered.sort(key=lambda x: -(x.get("begen_sayisi", 0) * 3 + x.get("goruntulenme", 0)))

        if not filtered:
            styled_info_banner("Arama kriterine uyan makale bulunamadı.", "info")
        else:
            st.markdown(f"**{len(filtered)} makale bulundu**")

            # Kategorize göster
            for mak in filtered:
                kat = WIKI_KATEGORILERI.get(mak.get("kategori", "sss"), WIKI_KATEGORILERI["sss"])
                begen = mak.get("begen_sayisi", 0)
                gor = mak.get("goruntulenme", 0)

                with st.expander(f"{kat['ikon']} **{mak.get('baslik', '')}** — {kat['ad']} · ❤️ {begen} · 👁️ {gor}"):
                    # Görüntülenme say
                    mak["goruntulenme"] = gor + 1
                    _save_makaleler(makaleler)

                    # İçerik
                    st.markdown(mak.get("icerik", ""))

                    # Meta
                    st.caption(f"✍️ {mak.get('yazar', '—')} · 📅 {mak.get('guncelleme_tarihi', '')[:10]}")

                    # Etiketler
                    if mak.get("etiketler"):
                        tag_html = " ".join(
                            f'<span style="background:{kat["renk"]}20;border:1px solid {kat["renk"]}40;border-radius:12px;padding:2px 10px;margin:2px;font-size:0.75rem;color:{kat["renk"]};">#{t}</span>'
                            for t in mak["etiketler"]
                        )
                        st.markdown(tag_html, unsafe_allow_html=True)

                    # Beğeni butonu
                    btn_c1, btn_c2 = st.columns(2)
                    with btn_c1:
                        if st.button(f"❤️ Beğen ({begen})", key=f"_wiki_begen_{mak['id']}"):
                            mak["begen_sayisi"] = begen + 1
                            _save_makaleler(makaleler)
                            st.rerun()
                    with btn_c2:
                        if st.button(f"✏️ Düzelt/Öner", key=f"_wiki_duzelt_{mak['id']}"):
                            st.session_state["_wiki_edit_id"] = mak["id"]
                            st.rerun()

    # ── Tab 2: Yeni Makale ──
    with tabs[1]:
        st.markdown("### ➕ Yeni Makale / Düzenleme Önerisi")

        # Düzenleme modu kontrol
        edit_id = st.session_state.get("_wiki_edit_id")
        edit_mak = next((m for m in makaleler if m.get("id") == edit_id), None) if edit_id else None

        if edit_mak:
            st.info(f"✏️ Düzenleniyor: **{edit_mak.get('baslik', '')}**")
            if st.button("❌ İptal", key="_wiki_edit_iptal"):
                del st.session_state["_wiki_edit_id"]
                st.rerun()

        try:
            auth = st.session_state.get("auth_user", {})
            yazar_ad = auth.get("name", "Anonim")
        except Exception:
            yazar_ad = "Anonim"

        with st.form("wiki_form", clear_on_submit=not edit_mak):
            c1, c2 = st.columns(2)
            with c1:
                mak_kategori = st.selectbox(
                    "Kategori *",
                    list(WIKI_KATEGORILERI.keys()),
                    index=list(WIKI_KATEGORILERI.keys()).index(edit_mak.get("kategori", "sss"))
                          if edit_mak and edit_mak.get("kategori") in WIKI_KATEGORILERI else 11,
                    format_func=lambda x: f"{WIKI_KATEGORILERI[x]['ikon']} {WIKI_KATEGORILERI[x]['ad']}",
                    key="_wiki_form_kat_widget",
                )
            with c2:
                mak_baslik = st.text_input(
                    "Başlık *",
                    value=edit_mak.get("baslik", "") if edit_mak else "",
                    key="_wiki_form_baslik_widget",
                )

            mak_icerik = st.text_area(
                "İçerik (Markdown destekler) *",
                value=edit_mak.get("icerik", "") if edit_mak else "",
                height=300,
                placeholder="## Başlık\n\n**Kalın yazı** veya `kod`\n\n- Madde 1\n- Madde 2\n\n### Alt başlık",
                key="_wiki_form_icerik_widget",
            )

            mak_etiketler = st.text_input(
                "Etiketler (virgülle)",
                value=", ".join(edit_mak.get("etiketler", [])) if edit_mak else "",
                placeholder="servis, kural, saat",
                key="_wiki_form_etiket_widget",
            )

            submit = st.form_submit_button(
                "💾 Güncelle" if edit_mak else "📝 Taslak Olarak Gönder",
                type="primary",
            )

            if submit:
                if not mak_baslik.strip() or not mak_icerik.strip():
                    styled_info_banner("Başlık ve içerik zorunlu.", "warning")
                else:
                    etiketler = [t.strip().lower() for t in mak_etiketler.split(",") if t.strip()]
                    now = datetime.now().isoformat()

                    if edit_mak:
                        # Güncelleme
                        idx = next((i for i, m in enumerate(makaleler) if m.get("id") == edit_id), None)
                        if idx is not None:
                            makaleler[idx].update({
                                "kategori": mak_kategori,
                                "baslik": mak_baslik.strip(),
                                "icerik": mak_icerik.strip(),
                                "etiketler": etiketler,
                                "onay_durumu": "İncelemede",  # Düzenleme yeniden onay gerektirir
                                "guncelleme_tarihi": now,
                                "guncelleyen": yazar_ad,
                            })
                            _save_makaleler(makaleler)
                            del st.session_state["_wiki_edit_id"]
                            st.success("✅ Düzenleme kaydedildi, onay bekliyor.")
                            st.rerun()
                    else:
                        # Yeni
                        yeni = {
                            "id": f"WIKI-{len(makaleler)+1:04d}",
                            "kategori": mak_kategori,
                            "baslik": mak_baslik.strip(),
                            "icerik": mak_icerik.strip(),
                            "etiketler": etiketler,
                            "yazar": yazar_ad,
                            "onay_durumu": "Taslak",
                            "olusturma_tarihi": now,
                            "guncelleme_tarihi": now,
                            "begen_sayisi": 0,
                            "goruntulenme": 0,
                        }
                        makaleler.append(yeni)
                        _save_makaleler(makaleler)
                        st.success(f"✅ Taslak kaydedildi. İnceleme için **İncelemede** moduna çevirin.")
                        st.balloons()
                        st.rerun()

    # ── Tab 3: Onay Paneli ──
    with tabs[2]:
        try:
            auth = st.session_state.get("auth_user", {})
            rol = auth.get("role", "").lower()
            yetkili = any(r in rol for r in ["mudur", "müdür", "yonetici", "kurucu", "admin", "koordinator"])
        except Exception:
            yetkili = True  # Dev

        if not yetkili:
            styled_info_banner("Bu panele sadece yönetim erişebilir.", "warning", "🔒")
        else:
            st.markdown("### ✅ Onay Bekleyen Makaleler")

            bekliyor = [m for m in makaleler if m.get("onay_durumu") in ("Taslak", "İncelemede")]
            if not bekliyor:
                styled_info_banner("Onay bekleyen makale yok.", "success")
            else:
                for mak in bekliyor:
                    kat = WIKI_KATEGORILERI.get(mak.get("kategori", "sss"), WIKI_KATEGORILERI["sss"])
                    durum_renk = "#D97706" if mak.get("onay_durumu") == "İncelemede" else "#64748B"

                    with st.expander(f"{kat['ikon']} {mak['baslik']} — {mak['yazar']} [{mak['onay_durumu']}]"):
                        st.markdown(mak["icerik"][:500] + ("..." if len(mak["icerik"]) > 500 else ""))

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("✅ Onayla", key=f"_wiki_onay_{mak['id']}", type="primary"):
                                idx = next((i for i, m in enumerate(makaleler) if m.get("id") == mak["id"]), None)
                                if idx is not None:
                                    makaleler[idx]["onay_durumu"] = "Onaylandı"
                                    _save_makaleler(makaleler)
                                    st.rerun()
                        with col2:
                            if st.button("⏳ İncele", key=f"_wiki_incele_{mak['id']}"):
                                idx = next((i for i, m in enumerate(makaleler) if m.get("id") == mak["id"]), None)
                                if idx is not None:
                                    makaleler[idx]["onay_durumu"] = "İncelemede"
                                    _save_makaleler(makaleler)
                                    st.rerun()
                        with col3:
                            if st.button("❌ Reddet", key=f"_wiki_red_{mak['id']}"):
                                idx = next((i for i, m in enumerate(makaleler) if m.get("id") == mak["id"]), None)
                                if idx is not None:
                                    makaleler[idx]["onay_durumu"] = "Reddedildi"
                                    _save_makaleler(makaleler)
                                    st.rerun()

    # ── Tab 4: İstatistik ──
    with tabs[3]:
        # Kategori dağılımı
        from collections import Counter
        kat_counts = Counter(m.get("kategori", "sss") for m in onayli_makaleler)

        st.markdown("### 📊 Kategori Dağılımı")
        for kat, sayi in kat_counts.most_common():
            info = WIKI_KATEGORILERI.get(kat, {"ad": kat, "ikon": "•", "renk": "#64748B"})
            pct = sayi / max(len(onayli_makaleler), 1) * 100
            st.markdown(f"""
            <div style="margin:6px 0;">
                <div style="display:flex;justify-content:space-between;font-size:0.88rem;margin-bottom:3px;">
                    <span>{info['ikon']} {info['ad']}</span>
                    <span style="color:{info['renk']};font-weight:700;">{sayi} (%{pct:.0f})</span>
                </div>
                <div style="background:#18181B;border-radius:6px;height:10px;">
                    <div style="width:{pct}%;height:100%;background:{info['renk']};border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # En popüler makaleler
        st.markdown("### 🏆 En Popüler Makaleler")
        top_makaleler = sorted(onayli_makaleler, key=lambda x: -(x.get("goruntulenme", 0)))[:10]
        for i, m in enumerate(top_makaleler, 1):
            st.markdown(f"**{i}.** {m.get('baslik')} — 👁️ {m.get('goruntulenme', 0)} · ❤️ {m.get('begen_sayisi', 0)}")

        # Aktif yazarlar
        st.markdown("### ✍️ Aktif Yazarlar")
        yazar_counts = Counter(m.get("yazar", "Anonim") for m in makaleler)
        for yazar, sayi in yazar_counts.most_common(5):
            st.markdown(f"• **{yazar}** — {sayi} makale")
