"""
Ders Planı Copilot — AI Destekli Tam Ders Paketi Üreticisi
==============================================================
Öğretmen konuyu yazar, AI 5 saniyede:
  • Ders planı (giriş-geliştirme-sonuç)
  • 10 soruluk quiz
  • PowerPoint taslak
  • Öğrenci etkinliği
  • Video/link önerileri
üretir.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from io import BytesIO

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# VERİ STORE — Oluşturulan ders planları kaydı
# ══════════════════════════════════════════════════════════════

def _plan_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "ders_plani_copilot")
    except Exception:
        d = os.path.join("data", "ders_plani_copilot")
    os.makedirs(d, exist_ok=True)
    return d


def _load_plans() -> list[dict]:
    p = os.path.join(_plan_dir(), "plans.json")
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_plans(data: list[dict]) -> None:
    p = os.path.join(_plan_dir(), "plans.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data[-100:], f, ensure_ascii=False, indent=2)  # son 100 plan


# ══════════════════════════════════════════════════════════════
# SABİTLER — MEB Müfredat Bağlamı
# ══════════════════════════════════════════════════════════════

KADEMELER = {
    "ilkokul": ["1. Sınıf", "2. Sınıf", "3. Sınıf", "4. Sınıf"],
    "ortaokul": ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"],
    "lise": ["9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf"],
}

DERSLER = {
    "ilkokul": ["Türkçe", "Matematik", "Hayat Bilgisi", "Fen Bilimleri",
                "Sosyal Bilgiler", "İngilizce", "Görsel Sanatlar", "Müzik",
                "Beden Eğitimi", "Din Kültürü"],
    "ortaokul": ["Türkçe", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler",
                 "İngilizce", "T.C. İnkılap Tarihi", "Din Kültürü",
                 "Görsel Sanatlar", "Müzik", "Beden Eğitimi", "Teknoloji ve Tasarım",
                 "Bilişim Teknolojileri"],
    "lise": ["Türk Dili ve Edebiyatı", "Matematik", "Fizik", "Kimya", "Biyoloji",
             "Tarih", "Coğrafya", "Felsefe", "İngilizce", "Almanca",
             "Fransızca", "Din Kültürü", "Beden Eğitimi"],
}

SURE_SECENEKLERI = [40, 80, 120]  # Dakika

OGRETIM_YAKLASIMLARI = [
    "Etkileşimli (soru-cevap ağırlıklı)",
    "Keşfedici (öğrenci araştırması)",
    "Proje tabanlı",
    "İşbirlikçi (grup çalışması)",
    "Doğrudan öğretim (klasik)",
    "Oyunlaştırılmış",
    "Ters yüz sınıf (flipped)",
]


# ══════════════════════════════════════════════════════════════
# AI ÜRETİM FONKSİYONLARI
# ══════════════════════════════════════════════════════════════

def _get_ai_client():
    """OpenAI client."""
    try:
        from utils.smarti_helper import _get_client
        return _get_client()
    except Exception:
        return None


def generate_full_lesson_package(
    client,
    ders: str,
    sinif: str,
    konu: str,
    sure: int,
    yaklasim: str,
    kazanim: str = "",
) -> dict:
    """Tam ders paketi üret — 5 bileşen."""
    context = (
        f"Ders: {ders}\n"
        f"Sınıf: {sinif}\n"
        f"Konu: {konu}\n"
        f"Süre: {sure} dakika\n"
        f"Yaklaşım: {yaklasim}\n"
        f"Kazanım: {kazanim or 'Belirtilmedi'}\n"
    )

    if not client:
        # Fallback — AI olmadan şablon
        return {
            "ders_plani": f"# {konu}\n\n## Giriş (10 dk)\nKonuya giriş...\n\n## Geliştirme (25 dk)\n...\n\n## Sonuç (5 dk)\n...",
            "quiz": [{"soru": "Örnek soru 1", "cevaplar": ["A", "B", "C", "D"], "dogru": 0}],
            "etkinlik": "Öğrenci etkinlik önerisi.",
            "slayt_taslagi": "## Slayt 1: Giriş\n## Slayt 2: Konu\n## Slayt 3: Örnek",
            "kaynaklar": ["MEB müfredat belgesi", "Ders kitabı"],
            "ai_kullanildi": False,
        }

    result = {"ai_kullanildi": True}

    # 1. Ders Planı
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "Sen deneyimli bir MEB öğretmenisin. Detaylı, uygulanabilir ders planları hazırlıyorsun. "
                    "Türkçe yaz, Markdown kullan. Giriş (10dk) - Geliştirme - Sonuç (5dk) yapısında ol."
                )},
                {"role": "user", "content": f"{context}\n\nBu ders için detaylı ders planı hazırla (giriş, geliştirme, sonuç, materyaller, değerlendirme bölümleri olsun)."},
            ],
            max_tokens=1200, temperature=0.5,
        )
        result["ders_plani"] = resp.choices[0].message.content or ""
    except Exception as e:
        result["ders_plani"] = f"Ders planı oluşturulamadı: {e}"

    # 2. Quiz (10 soru)
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "Ölçme değerlendirme uzmanısın. Çoktan seçmeli sorular hazırla. "
                    "Yanıtı SADECE JSON formatında ver: "
                    '[{"soru": "...", "cevaplar": ["A", "B", "C", "D"], "dogru": 0, "aciklama": "..."}, ...]'
                )},
                {"role": "user", "content": f"{context}\n\n5 adet çoktan seçmeli soru hazırla. Zorluk kademeli (2 kolay, 2 orta, 1 zor)."},
            ],
            max_tokens=1000, temperature=0.5,
        )
        raw = resp.choices[0].message.content or "[]"
        import re
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            result["quiz"] = json.loads(match.group())
        else:
            result["quiz"] = []
    except Exception:
        result["quiz"] = []

    # 3. Öğrenci Etkinliği
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Yaratıcı bir öğretmensin. Öğrencilerin aktif katılımını sağlayan etkinlik öneriyorsun."},
                {"role": "user", "content": f"{context}\n\nBu konu için 1 yaratıcı sınıf içi öğrenci etkinliği öner. Süresi, malzemeleri, adımları belirt."},
            ],
            max_tokens=500, temperature=0.6,
        )
        result["etkinlik"] = resp.choices[0].message.content or ""
    except Exception as e:
        result["etkinlik"] = f"Etkinlik oluşturulamadı: {e}"

    # 4. Slayt Taslağı
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "PowerPoint slayt taslağı hazırlıyorsun. Her slayt için başlık + 3-4 madde. "
                    "Markdown formatı kullan: ## Slayt N: Başlık"
                )},
                {"role": "user", "content": f"{context}\n\n6-8 slaytlık sunum taslağı hazırla."},
            ],
            max_tokens=800, temperature=0.5,
        )
        result["slayt_taslagi"] = resp.choices[0].message.content or ""
    except Exception as e:
        result["slayt_taslagi"] = f"Slayt taslağı oluşturulamadı: {e}"

    # 5. Kaynak önerileri
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ders kaynak uzmanısın. Kaliteli Türkçe kaynaklar öneriyorsun."},
                {"role": "user", "content": f"{context}\n\nBu konu için 5 kaynak öner: YouTube videoları, MEB kitapları, web siteleri, interaktif araçlar."},
            ],
            max_tokens=500, temperature=0.5,
        )
        result["kaynaklar_text"] = resp.choices[0].message.content or ""
    except Exception as e:
        result["kaynaklar_text"] = f"Kaynak önerileri oluşturulamadı: {e}"

    return result


# ══════════════════════════════════════════════════════════════
# UI — Ana Panel
# ══════════════════════════════════════════════════════════════

def render_ders_plani_copilot():
    """Ders Planı Copilot ana paneli — AI Destek modülünden çağrılır."""
    styled_section("📚 Ders Planı Copilot — AI Tam Paket Üretici", "#4F46E5")

    styled_info_banner(
        "Konunuzu yazın, AI 5 bileşenli tam paketi üretir: Ders planı, quiz, etkinlik, slayt taslağı, kaynaklar.",
        "info", "🤖",
    )

    client = _get_ai_client()
    plans = _load_plans()

    # İstatistik
    styled_stat_row([
        ("Üretilen Plan", str(len(plans)), "#4F46E5", "📚"),
        ("Bu Ay", str(sum(1 for p in plans if p.get("olusturma_tarihi", "")[:7] == datetime.now().strftime("%Y-%m"))), "#059669", "📅"),
        ("Bu Hafta", str(sum(1 for p in plans if (datetime.now() - datetime.fromisoformat(p.get("olusturma_tarihi", datetime.now().isoformat()))).days < 7 if p.get("olusturma_tarihi"))), "#D97706", "🗓️"),
    ])

    # Ana form
    with st.form("ders_plani_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            kademe = st.selectbox(
                "Kademe", list(KADEMELER.keys()),
                format_func=lambda x: x.title(),
                key="_dpc_kademe_widget",
            )
            sinif = st.selectbox(
                "Sınıf", KADEMELER[kademe],
                key="_dpc_sinif_widget",
            )
            ders = st.selectbox(
                "Ders", DERSLER[kademe],
                key="_dpc_ders_widget",
            )
        with c2:
            konu = st.text_input(
                "Konu *",
                placeholder="Örn: Doğal sayılarda dört işlem, Atatürk'ün hayatı, Hücre zarı...",
                key="_dpc_konu_widget",
            )
            sure = st.selectbox(
                "Ders Süresi (dk)", SURE_SECENEKLERI,
                index=1,
                key="_dpc_sure_widget",
            )
            yaklasim = st.selectbox(
                "Öğretim Yaklaşımı", OGRETIM_YAKLASIMLARI,
                key="_dpc_yaklasim_widget",
            )

        kazanim = st.text_area(
            "Kazanım (opsiyonel — MEB müfredatından)",
            placeholder="Örn: M.3.1.1.1 Doğal sayıları okur ve yazar.",
            height=60,
            key="_dpc_kazanim_widget",
        )

        btn_col1, btn_col2 = st.columns([3, 1])
        with btn_col1:
            generate = st.form_submit_button(
                "🚀 Tam Paket Üret (Plan + Quiz + Etkinlik + Slayt + Kaynaklar)",
                type="primary", use_container_width=True,
            )
        with btn_col2:
            sadece_plan = st.form_submit_button(
                "📝 Sadece Plan",
                use_container_width=True,
            )

        if generate or sadece_plan:
            if not konu or len(konu.strip()) < 3:
                styled_info_banner("Lütfen konuyu yazın.", "warning")
                return

            with st.spinner("🤖 Smarti tam paketinizi hazırlıyor... (10-20 saniye sürebilir)"):
                package = generate_full_lesson_package(
                    client, ders, sinif, konu, sure, yaklasim, kazanim,
                )

            # Kaydet
            yeni_plan = {
                "id": f"DPC-{len(plans)+1:04d}",
                "ders": ders,
                "sinif": sinif,
                "konu": konu.strip(),
                "sure": sure,
                "yaklasim": yaklasim,
                "kazanim": kazanim.strip(),
                "paket": package,
                "olusturma_tarihi": datetime.now().isoformat(),
            }
            plans.append(yeni_plan)
            _save_plans(plans)

            st.success(f"✅ Paket hazır! ID: **{yeni_plan['id']}**")
            _render_package(package, compact=sadece_plan)

    # Geçmiş planlar
    if plans:
        with st.expander(f"📜 Önceki Planlar ({len(plans)})"):
            for p in reversed(plans[-10:]):
                pc1, pc2, pc3 = st.columns([3, 1, 1])
                with pc1:
                    st.markdown(f"**{p.get('id', '')}** — {p.get('ders', '')} / {p.get('sinif', '')} — {p.get('konu', '')[:50]}")
                with pc2:
                    st.caption(p.get("olusturma_tarihi", "")[:16])
                with pc3:
                    if st.button("📂 Aç", key=f"_dpc_open_{p.get('id')}"):
                        st.session_state["_dpc_aktif_plan"] = p.get("id")
                        st.rerun()

    # Aktif plan göster
    if "_dpc_aktif_plan" in st.session_state:
        aktif_id = st.session_state["_dpc_aktif_plan"]
        aktif_plan = next((p for p in plans if p.get("id") == aktif_id), None)
        if aktif_plan:
            st.divider()
            styled_section(f"📖 Plan: {aktif_plan.get('id')} — {aktif_plan.get('konu')}", "#4F46E5")
            _render_package(aktif_plan.get("paket", {}))
            if st.button("❌ Kapat", key="_dpc_close"):
                del st.session_state["_dpc_aktif_plan"]
                st.rerun()


def _render_package(package: dict, compact: bool = False):
    """Üretilen ders paketini göster."""
    if not package.get("ai_kullanildi", True):
        styled_info_banner(
            "⚠️ AI devre dışı (OpenAI API key yok) — şablon paket gösteriliyor.",
            "warning",
        )

    # Tab'lara ayır
    tab_labels = ["📝 Ders Planı"]
    if not compact:
        tab_labels += ["❓ Quiz", "🎯 Etkinlik", "📊 Slaytlar", "📚 Kaynaklar"]

    tabs = st.tabs(tab_labels)

    # 1. Ders Planı
    with tabs[0]:
        st.markdown(package.get("ders_plani", "Plan oluşturulamadı."))

        # İndirme butonu
        plan_bytes = package.get("ders_plani", "").encode("utf-8")
        st.download_button(
            "📥 Markdown İndir",
            data=plan_bytes,
            file_name=f"ders_plani_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            key=f"_dpc_dl_plan_{id(package)}",
        )

    if compact:
        return

    # 2. Quiz
    with tabs[1]:
        quiz = package.get("quiz", [])
        if not quiz:
            styled_info_banner("Quiz oluşturulamadı.", "warning")
        else:
            for i, q in enumerate(quiz, 1):
                st.markdown(f"**{i}. {q.get('soru', '')}**")
                cevaplar = q.get("cevaplar", [])
                dogru = q.get("dogru", 0)
                for j, c in enumerate(cevaplar):
                    harf = chr(65 + j)  # A, B, C, D
                    marker = "✅" if j == dogru else "•"
                    st.markdown(f"  {marker} **{harf})** {c}")
                if q.get("aciklama"):
                    st.caption(f"💡 {q['aciklama']}")
                st.markdown("---")

            # JSON indir (sınav modülüne import için)
            quiz_json = json.dumps(quiz, ensure_ascii=False, indent=2)
            st.download_button(
                "📥 Quiz JSON İndir (Ölçme modülüne import için)",
                data=quiz_json,
                file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                key=f"_dpc_dl_quiz_{id(package)}",
            )

    # 3. Etkinlik
    with tabs[2]:
        st.markdown(package.get("etkinlik", "Etkinlik oluşturulamadı."))

    # 4. Slaytlar
    with tabs[3]:
        st.markdown(package.get("slayt_taslagi", "Slayt taslağı oluşturulamadı."))
        st.caption("💡 Bu taslağı PowerPoint/Keynote/Google Slides'a kopyalayabilirsiniz.")

    # 5. Kaynaklar
    with tabs[4]:
        st.markdown(package.get("kaynaklar_text", package.get("kaynaklar", "Kaynak önerisi yok.")))
