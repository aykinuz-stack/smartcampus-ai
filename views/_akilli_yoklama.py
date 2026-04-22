"""
Akıllı Yoklama — Çoklu Yöntem Yoklama Sistemi
====================================================
Yüz tanıma (gelecek), QR kod, tek tıkla toplu, ses komutlu yoklama.
Her öğretmen günde 10 dk kazanır.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _yoklama_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "akilli_yoklama")
    except Exception:
        d = os.path.join("data", "akilli_yoklama")
    os.makedirs(d, exist_ok=True)
    return d


def _yoklama_path() -> str:
    return os.path.join(_yoklama_dir(), "yoklamalar.json")


def _load_yoklamalar() -> list[dict]:
    p = _yoklama_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_yoklamalar(data: list[dict]) -> None:
    with open(_yoklama_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# YOKLAMA YÖNTEMLERİ
# ══════════════════════════════════════════════════════════════

YOKLAMA_YONTEMLERI = {
    "hizli_toplu":  {"ad": "⚡ Hızlı Toplu (tek tık)", "sure_sn": 5, "hassasiyet": "yuksek"},
    "tek_tek":      {"ad": "👆 Tek Tek Öğrenci", "sure_sn": 60, "hassasiyet": "tam"},
    "qr_kod":       {"ad": "📱 QR Kod (öğrenci tarar)", "sure_sn": 30, "hassasiyet": "tam"},
    "yuz_tanima":   {"ad": "📸 Yüz Tanıma (Beta)", "sure_sn": 15, "hassasiyet": "cok_yuksek"},
    "sesli_komut":  {"ad": "🎙️ Sesli Komut (Öğretmen okur)", "sure_sn": 90, "hassasiyet": "tam"},
}


# ══════════════════════════════════════════════════════════════
# 1. HIZLI TOPLU YOKLAMA — Tek Tık
# ══════════════════════════════════════════════════════════════

def render_hizli_toplu_yoklama(students: list, ders: str, ders_saati: int):
    """Tüm öğrenciler varsayılan OLANDA — tek tıkla eksikleri işaretle."""
    st.markdown("**⚡ Hızlı Toplu Yoklama** — Tüm öğrenciler **VAR** varsayılır. Eksikleri işaretle.")

    # State init
    session_key = f"_ayk_hizli_{ders}_{ders_saati}_{date.today().isoformat()}"
    if session_key not in st.session_state:
        st.session_state[session_key] = {
            "yok": set(),  # eksik öğrenciler
            "ozurlu": set(),
            "gec": set(),
        }

    state = st.session_state[session_key]

    # Toplu aksiyon
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Hepsi Var (sıfırla)", key=f"_ayk_hepsi_var_{session_key}"):
            state["yok"] = set()
            state["ozurlu"] = set()
            state["gec"] = set()
            st.rerun()
    with c2:
        st.markdown(f"**📊 Yok:** {len(state['yok'])} | **⏰ Geç:** {len(state['gec'])} | **🤒 Özürlü:** {len(state['ozurlu'])}")
    with c3:
        var_sayi = len(students) - len(state["yok"]) - len(state["ozurlu"])
        st.markdown(f"**✅ Var:** {var_sayi}/{len(students)}")

    st.divider()

    # Öğrenci grid — 3 sütunlu
    cols_per_row = 3
    for row_start in range(0, len(students), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for col, stu in zip(row_cols, students[row_start:row_start + cols_per_row]):
            with col:
                sid = str(stu.id)
                is_yok = sid in state["yok"]
                is_gec = sid in state["gec"]
                is_oz = sid in state["ozurlu"]

                if is_yok:
                    badge, renk = "❌ YOK", "#DC2626"
                elif is_oz:
                    badge, renk = "🤒 ÖZÜR", "#D97706"
                elif is_gec:
                    badge, renk = "⏰ GEÇ", "#0284C7"
                else:
                    badge, renk = "✅ VAR", "#059669"

                st.markdown(f"""
                <div style="background:{renk}15;border:1px solid {renk}40;border-radius:8px;
                padding:8px 12px;margin:3px 0;">
                    <div style="color:{renk};font-weight:700;font-size:0.72rem;">{badge}</div>
                    <div style="color:#FAFAFA;font-size:0.88rem;font-weight:600;">{stu.tam_ad[:24]}</div>
                    <div style="color:#94A3B8;font-size:0.72rem;">No: {getattr(stu, 'numara', '—')}</div>
                </div>
                """, unsafe_allow_html=True)

                bc1, bc2, bc3 = st.columns(3)
                with bc1:
                    if st.button("❌", key=f"_ayk_yok_{session_key}_{sid}", help="Yok (özürsüz)"):
                        if sid in state["yok"]:
                            state["yok"].discard(sid)
                        else:
                            state["yok"].add(sid)
                            state["ozurlu"].discard(sid)
                            state["gec"].discard(sid)
                        st.rerun()
                with bc2:
                    if st.button("🤒", key=f"_ayk_oz_{session_key}_{sid}", help="Özürlü"):
                        if sid in state["ozurlu"]:
                            state["ozurlu"].discard(sid)
                        else:
                            state["ozurlu"].add(sid)
                            state["yok"].discard(sid)
                            state["gec"].discard(sid)
                        st.rerun()
                with bc3:
                    if st.button("⏰", key=f"_ayk_gec_{session_key}_{sid}", help="Geç kaldı"):
                        if sid in state["gec"]:
                            state["gec"].discard(sid)
                        else:
                            state["gec"].add(sid)
                        st.rerun()

    # Kaydet
    st.divider()
    if st.button("💾 Yoklamayı Kaydet", type="primary", use_container_width=True, key=f"_ayk_kaydet_{session_key}"):
        yoklama_kayitlari = _load_yoklamalar()
        tarih_str = date.today().isoformat()
        yeni_kayit = {
            "id": f"AYK-{len(yoklama_kayitlari)+1:06d}",
            "tarih": tarih_str,
            "ders": ders,
            "ders_saati": ders_saati,
            "yontem": "hizli_toplu",
            "toplam_ogrenci": len(students),
            "var": len(students) - len(state["yok"]) - len(state["ozurlu"]),
            "yok": list(state["yok"]),
            "ozurlu": list(state["ozurlu"]),
            "gec": list(state["gec"]),
            "olusturma_tarihi": datetime.now().isoformat(),
        }
        yoklama_kayitlari.append(yeni_kayit)
        _save_yoklamalar(yoklama_kayitlari)

        # Akademik Takip'e de yaz
        try:
            from models.akademik_takip import AkademikDataStore
            ak = AkademikDataStore()
            for sid in state["yok"]:
                try:
                    ak.add_attendance(student_id=sid, ders=ders, ders_saati=ders_saati,
                                      tarih=tarih_str, turu="ozursuz")
                except Exception:
                    pass
            for sid in state["ozurlu"]:
                try:
                    ak.add_attendance(student_id=sid, ders=ders, ders_saati=ders_saati,
                                      tarih=tarih_str, turu="ozurlu")
                except Exception:
                    pass
        except Exception:
            pass

        st.success(f"✅ Yoklama kaydedildi! {yeni_kayit['var']}/{len(students)} öğrenci var.")
        st.balloons()
        # State temizle
        del st.session_state[session_key]
        st.rerun()


# ══════════════════════════════════════════════════════════════
# 2. QR KOD YOKLAMA — Öğrenci tarar
# ══════════════════════════════════════════════════════════════

def render_qr_yoklama(students: list, ders: str, ders_saati: int):
    """QR kod ile öğrenci self-check yoklama."""
    st.markdown("**📱 QR Kod Yoklama** — Öğrenciler tabletteki QR'ı telefonlarıyla tarar.")

    # QR kod üret
    session_key = f"_ayk_qr_{ders}_{ders_saati}_{date.today().isoformat()}"
    if session_key not in st.session_state:
        # QR için unique kod
        import uuid
        qr_kod = f"YK-{uuid.uuid4().hex[:12].upper()}"
        st.session_state[session_key] = {
            "qr_kod": qr_kod,
            "taranlar": set(),
            "baslangic": datetime.now().isoformat(),
        }

    state = st.session_state[session_key]

    # QR kodu göster
    qr_data = f"SCAI-YOKLAMA:{state['qr_kod']}:{ders}:{ders_saati}:{date.today().isoformat()}"
    try:
        import qrcode
        from io import BytesIO
        import base64
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#FFFFFF", back_color="#09090B")
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        qr_html = f'<img src="data:image/png;base64,{b64}" style="width:300px;height:300px;border-radius:12px;" />'
    except ImportError:
        qr_html = (f'<div style="width:300px;height:300px;background:#09090B;color:#FAFAFA;'
                   f'border-radius:12px;display:flex;align-items:center;justify-content:center;'
                   f'font-family:monospace;padding:20px;text-align:center;">QR: {state["qr_kod"]}<br/><br/>'
                   f'qrcode kütüphanesi yüklü değil</div>')

    cc1, cc2 = st.columns([1, 1])
    with cc1:
        st.markdown(f"""
        <div style="text-align:center;background:#18181B;border-radius:16px;padding:20px;">
            {qr_html}
            <div style="margin-top:12px;color:#FAFAFA;font-weight:700;font-size:1.1rem;">
                📱 Tarayın
            </div>
            <div style="color:#94A3B8;font-size:0.82rem;margin-top:4px;">
                Kod: <code>{state['qr_kod']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cc2:
        st.markdown(f"**📊 Durum:** {len(state['taranlar'])}/{len(students)} öğrenci tarandı")

        # Manuel check-in (test için)
        st.caption("Test için manuel:")
        sim_student = st.selectbox(
            "Simülasyon: Öğrenci seçin",
            [""] + [s.tam_ad for s in students],
            key=f"_ayk_qr_sim_{session_key}",
        )
        if sim_student and st.button("📱 Tara (simülasyon)", key=f"_ayk_qr_sim_btn_{session_key}"):
            stu = next((s for s in students if s.tam_ad == sim_student), None)
            if stu:
                state["taranlar"].add(str(stu.id))
                st.success(f"✅ {sim_student} tarandı.")
                st.rerun()

    # Tarayan öğrencileri listele
    if state["taranlar"]:
        st.markdown("**✅ Tarayan Öğrenciler:**")
        for sid in state["taranlar"]:
            stu = next((s for s in students if str(s.id) == sid), None)
            if stu:
                st.markdown(f"• ✅ {stu.tam_ad}")

    # Eksik
    eksik = [s for s in students if str(s.id) not in state["taranlar"]]
    if eksik:
        st.markdown(f"**❌ Henüz Taramayan ({len(eksik)}):**")
        for s in eksik[:10]:
            st.markdown(f"• ❌ {s.tam_ad}")

    # Kaydet
    if st.button("💾 Yoklamayı Kapat ve Kaydet", type="primary", use_container_width=True, key=f"_ayk_qr_save_{session_key}"):
        yoklama_kayitlari = _load_yoklamalar()
        yeni_kayit = {
            "id": f"AYK-{len(yoklama_kayitlari)+1:06d}",
            "tarih": date.today().isoformat(),
            "ders": ders,
            "ders_saati": ders_saati,
            "yontem": "qr_kod",
            "qr_kod": state["qr_kod"],
            "toplam_ogrenci": len(students),
            "var": len(state["taranlar"]),
            "taranlar": list(state["taranlar"]),
            "eksik": [str(s.id) for s in students if str(s.id) not in state["taranlar"]],
            "baslangic": state["baslangic"],
            "bitis": datetime.now().isoformat(),
        }
        yoklama_kayitlari.append(yeni_kayit)
        _save_yoklamalar(yoklama_kayitlari)
        st.success(f"✅ QR Yoklama kaydedildi! {len(state['taranlar'])}/{len(students)} tarandı.")
        del st.session_state[session_key]
        st.rerun()


# ══════════════════════════════════════════════════════════════
# 3. YÜZ TANIMA (BETA) — Kamera yakalama
# ══════════════════════════════════════════════════════════════

def render_yuz_tanima_yoklama(students: list, ders: str, ders_saati: int):
    """Kamera ile yüz tanıma yoklama (beta)."""
    st.markdown("**📸 Yüz Tanıma Yoklama (Beta)** — Tablet kamerasını sınıfa tutun.")

    styled_info_banner(
        "Yüz tanıma özelliği **KVKK uyumluluğu** gerektirir. Bu özelliğin kullanımı için "
        "okul yönetimi ve veli onayı şarttır. Şu an simülasyon modundadır.",
        "warning", "⚠️",
    )

    # Kamera girişi
    img_file = st.camera_input("📸 Sınıf fotoğrafı çek", key=f"_ayk_cam_{ders}_{ders_saati}")

    if img_file:
        st.image(img_file, caption="Çekilen fotoğraf", width=400)

        if st.button("🔍 Öğrencileri Tanı (AI)", type="primary", key=f"_ayk_tani_{ders}_{ders_saati}"):
            with st.spinner("🤖 Yüzler tanınıyor..."):
                # Simülasyon — gerçek yüz tanıma için AWS Rekognition, Azure Face, OpenAI vision vs. kullanılabilir
                import random
                tanınan = random.sample(students, k=min(len(students) - 2, len(students)))
                st.success(f"✅ {len(tanınan)}/{len(students)} öğrenci tanındı (simülasyon)")

                for stu in tanınan:
                    st.markdown(f"• 📸 {stu.tam_ad} — ✅ Tanındı (güven: {random.randint(85, 99)}%)")

                eksik = [s for s in students if s not in tanınan]
                if eksik:
                    st.markdown("**❓ Tanınmayan / Yok:**")
                    for s in eksik:
                        st.markdown(f"• ❓ {s.tam_ad}")

                # Kaydet
                yoklama_kayitlari = _load_yoklamalar()
                yoklama_kayitlari.append({
                    "id": f"AYK-{len(yoklama_kayitlari)+1:06d}",
                    "tarih": date.today().isoformat(),
                    "ders": ders,
                    "ders_saati": ders_saati,
                    "yontem": "yuz_tanima",
                    "toplam_ogrenci": len(students),
                    "var": len(tanınan),
                    "taninan": [str(s.id) for s in tanınan],
                    "eksik": [str(s.id) for s in eksik],
                    "olusturma_tarihi": datetime.now().isoformat(),
                    "simülasyon": True,
                })
                _save_yoklamalar(yoklama_kayitlari)


# ══════════════════════════════════════════════════════════════
# 4. SESLİ KOMUT YOKLAMA — Öğretmen okur
# ══════════════════════════════════════════════════════════════

def render_sesli_yoklama(students: list, ders: str, ders_saati: int):
    """Öğretmen isim okur, öğrenci 'buradayım' der."""
    st.markdown("**🎙️ Sesli Komut Yoklama** — Öğrenciyi seç, sesli 'Buradayım' de.")

    styled_info_banner(
        "Mikrofonu açın, öğrencinin sesiyle 'Buradayım' ifadesini kontrol edin. "
        "(Şimdilik manuel onay modunda.)",
        "info",
    )

    session_key = f"_ayk_sesli_{ders}_{ders_saati}_{date.today().isoformat()}"
    if session_key not in st.session_state:
        st.session_state[session_key] = {"mevcut": set(), "sira": 0}

    state = st.session_state[session_key]

    # Sıradaki öğrenci
    sorted_students = sorted(students, key=lambda s: getattr(s, "numara", 0) or 0)

    if state["sira"] >= len(sorted_students):
        st.success(f"✅ Tüm öğrenciler okundu! {len(state['mevcut'])}/{len(students)} var.")
        if st.button("💾 Kaydet", type="primary", key=f"_ayk_sesli_save_{session_key}"):
            yoklama_kayitlari = _load_yoklamalar()
            yoklama_kayitlari.append({
                "id": f"AYK-{len(yoklama_kayitlari)+1:06d}",
                "tarih": date.today().isoformat(),
                "ders": ders,
                "ders_saati": ders_saati,
                "yontem": "sesli_komut",
                "toplam_ogrenci": len(students),
                "var": len(state["mevcut"]),
                "mevcut": list(state["mevcut"]),
                "olusturma_tarihi": datetime.now().isoformat(),
            })
            _save_yoklamalar(yoklama_kayitlari)
            del st.session_state[session_key]
            st.rerun()
        return

    mevcut_ogr = sorted_students[state["sira"]]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);border-radius:16px;
    padding:24px;text-align:center;color:white;margin:16px 0;">
        <div style="font-size:0.82rem;opacity:0.9;letter-spacing:2px;">
            {state['sira']+1} / {len(sorted_students)}
        </div>
        <div style="font-size:2rem;font-weight:900;margin:8px 0;">
            {mevcut_ogr.tam_ad}
        </div>
        <div style="font-size:0.88rem;opacity:0.9;">
            No: {getattr(mevcut_ogr, 'numara', '—')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🎙️ Öğrenciyi çağırın:**")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✅ Buradayım", type="primary", use_container_width=True,
                     key=f"_ayk_ses_var_{session_key}"):
            state["mevcut"].add(str(mevcut_ogr.id))
            state["sira"] += 1
            st.rerun()
    with c2:
        if st.button("❌ Yok", use_container_width=True,
                     key=f"_ayk_ses_yok_{session_key}"):
            state["sira"] += 1
            st.rerun()
    with c3:
        if st.button("⏭️ Atla", use_container_width=True,
                     key=f"_ayk_ses_atla_{session_key}"):
            state["sira"] += 1
            st.rerun()


# ══════════════════════════════════════════════════════════════
# ANA PANEL
# ══════════════════════════════════════════════════════════════

def render_akilli_yoklama():
    """Akıllı Yoklama ana paneli."""
    styled_section("📸 Akıllı Yoklama", "#4F46E5")

    styled_info_banner(
        "5 farklı yoklama yöntemi: **Hızlı Toplu** (5sn), **QR Kod**, **Yüz Tanıma** (beta), "
        "**Sesli Komut**, **Tek Tek**. Günde 10+ dakika tasarruf.",
        "info", "📸",
    )

    # Sınıf ve ders seçimi
    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        all_students = ak.get_students(durum="aktif")
    except Exception:
        all_students = []

    if not all_students:
        styled_info_banner("Öğrenci verisi yok.", "warning")
        return

    # Sınıf filtresi
    siniflar = sorted(set(f"{s.sinif}/{s.sube}" for s in all_students if s.sube))

    c1, c2, c3 = st.columns(3)
    with c1:
        sel_sinif = st.selectbox("Sınıf/Şube", siniflar, key="_ayk_sinif_widget")
    with c2:
        ders = st.text_input("Ders", value="Matematik", key="_ayk_ders_widget")
    with c3:
        ders_saati = st.selectbox("Ders Saati", [1, 2, 3, 4, 5, 6, 7, 8], key="_ayk_saat_widget")

    # Filtrele
    sinif, sube = sel_sinif.split("/")
    filtered = [s for s in all_students if s.sinif == int(sinif) and s.sube == sube]

    if not filtered:
        styled_info_banner(f"{sel_sinif} sınıfında öğrenci yok.", "info")
        return

    # İstatistik
    yoklamalar = _load_yoklamalar()
    bugun_yoklama = [y for y in yoklamalar if y.get("tarih") == date.today().isoformat()]

    styled_stat_row([
        ("Sınıftaki Öğrenci", str(len(filtered)), "#4F46E5", "🎓"),
        ("Bugün Yoklama", str(len(bugun_yoklama)), "#059669", "📅"),
        ("Toplam Kayıt", str(len(yoklamalar)), "#D97706", "📊"),
    ])

    # Yöntem seçimi
    st.divider()
    st.markdown("**📋 Yoklama Yöntemi Seçin:**")

    method_tabs = st.tabs([info["ad"] for info in YOKLAMA_YONTEMLERI.values()])

    with method_tabs[0]:  # Hızlı Toplu
        render_hizli_toplu_yoklama(filtered, ders, ders_saati)

    with method_tabs[1]:  # Tek Tek
        st.info("Geleneksel tek tek yoklama — Akademik Takip > Yoklama sekmesinden yapılabilir.")

    with method_tabs[2]:  # QR Kod
        render_qr_yoklama(filtered, ders, ders_saati)

    with method_tabs[3]:  # Yüz Tanıma
        render_yuz_tanima_yoklama(filtered, ders, ders_saati)

    with method_tabs[4]:  # Sesli Komut
        render_sesli_yoklama(filtered, ders, ders_saati)

    # Bugün kayıtları
    st.divider()
    if bugun_yoklama:
        styled_section("📊 Bugünkü Yoklamalar", "#64748B")
        for y in bugun_yoklama[-5:]:
            ortalama = (y.get("var", 0) / max(y.get("toplam_ogrenci", 1), 1)) * 100
            yontem = YOKLAMA_YONTEMLERI.get(y.get("yontem", "?"), {}).get("ad", y.get("yontem"))
            st.markdown(f"""
            • **{y.get('ders')}** — {y.get('ders_saati')}. saat — {yontem}
              — **{y.get('var', 0)}/{y.get('toplam_ogrenci', 0)}** öğrenci (%{ortalama:.0f})
            """)
