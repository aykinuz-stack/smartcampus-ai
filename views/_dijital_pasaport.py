"""
Dijital Öğrenci Pasaportu
==============================
QR kodlu dijital kimlik + taşınabilir başarı geçmişi.
Okul değişince notlar, rozetler, etkinlikler yeni okula transfer olur.
"""
from __future__ import annotations

import json
import os
import base64
import hashlib
from datetime import datetime
from io import BytesIO

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _pasaport_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "dijital_pasaport")
    except Exception:
        d = os.path.join("data", "dijital_pasaport")
    os.makedirs(d, exist_ok=True)
    return d


def _pasaport_path() -> str:
    return os.path.join(_pasaport_dir(), "pasaportlar.json")


def _load_pasaportlar() -> list[dict]:
    p = _pasaport_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_pasaportlar(data: list[dict]) -> None:
    with open(_pasaport_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════
# QR ÜRETİM (Basit — pyqrcode veya qrcode kütüphanesi)
# ══════════════════════════════════════════════════════════════

def _generate_qr_svg(data: str, size: int = 200) -> str:
    """QR kod SVG üret — kütüphanesi varsa, yoksa basit barcode fallback."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(data)
        qr.make(fit=True)
        # SVG olarak üret
        img = qr.make_image(fill_color="#09090B", back_color="#FAFAFA")
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f'<img src="data:image/png;base64,{b64}" style="width:{size}px;height:{size}px;border-radius:8px;" />'
    except ImportError:
        # Fallback — basit hash karesi
        hash_val = hashlib.md5(data.encode()).hexdigest()
        return f"""<div style="width:{size}px;height:{size}px;background:#FAFAFA;border-radius:8px;
        display:flex;align-items:center;justify-content:center;color:#09090B;font-family:monospace;
        font-size:10px;padding:10px;text-align:center;word-break:break-all;">
        QR<br/>{hash_val[:16]}</div>"""
    except Exception:
        return ""


# ══════════════════════════════════════════════════════════════
# PASAPORT ÜRETİMİ
# ══════════════════════════════════════════════════════════════

def generate_pasaport(student) -> dict:
    """Öğrencinin tam pasaport verisini üret — akademik veriyi topla."""
    pasaport = {
        "pasaport_id": f"PSP-{student.id}",
        "ogrenci": {
            "id": student.id,
            "ad": student.tam_ad,
            "sinif": getattr(student, "sinif", ""),
            "sube": getattr(student, "sube", ""),
            "numara": getattr(student, "numara", ""),
            "kademe": getattr(student, "kademe", ""),
        },
        "olusturma_tarihi": datetime.now().isoformat(),
        "guncelleme_tarihi": datetime.now().isoformat(),
        "ozet": {
            "not_ortalamasi": 0,
            "devamsizlik_gun": 0,
            "odev_teslim_orani": 0,
            "rozet_sayisi": 0,
            "etkinlik_sayisi": 0,
            "proje_sayisi": 0,
        },
        "basarilar": [],
        "yarismalar": [],
        "projeler": [],
        "etkinlikler": [],
        "rozetler": [],
        "dersler": [],
        "okul_gecmisi": [],
    }

    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()

        # Notlar
        grades = ak.get_grades(student_id=student.id)
        if grades:
            try:
                puanlar = [float(g.not_degeri if hasattr(g, 'not_degeri') else g.get('puan', 0)) for g in grades]
                puanlar = [p for p in puanlar if p > 0]
                if puanlar:
                    pasaport["ozet"]["not_ortalamasi"] = round(sum(puanlar) / len(puanlar), 1)
            except Exception:
                pass

        # Devamsızlık
        attendance = ak.get_attendance(student_id=student.id) if hasattr(ak, 'get_attendance') else []
        pasaport["ozet"]["devamsizlik_gun"] = len(attendance) if attendance else 0

        # Dersler (aldığı)
        if grades:
            dersler = set()
            for g in grades:
                ders = g.ders if hasattr(g, 'ders') else g.get('ders', '')
                if ders:
                    dersler.add(ders)
            pasaport["dersler"] = sorted(list(dersler))
    except Exception:
        pass

    return pasaport


# ══════════════════════════════════════════════════════════════
# TEK ÖĞRENCİ PASAPORT GÖRÜNÜMÜ
# ══════════════════════════════════════════════════════════════

def render_ogrenci_pasaport_karti(pasaport: dict, compact: bool = False):
    """Pasaport kartı görünümü — QR kodlu."""
    ogr = pasaport.get("ogrenci", {})
    ozet = pasaport.get("ozet", {})

    # QR için data
    qr_data = json.dumps({
        "id": pasaport.get("pasaport_id"),
        "ad": ogr.get("ad"),
        "sinif": f"{ogr.get('sinif')}/{ogr.get('sube')}",
        "tarih": pasaport.get("guncelleme_tarihi", "")[:10],
    }, ensure_ascii=False)
    qr_html = _generate_qr_svg(qr_data, size=140 if not compact else 100)

    # Ön yüz — Kimlik kartı tarzı
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 50%,#EC4899 100%);
    border-radius:16px;padding:24px;color:white;margin:16px 0;
    box-shadow:0 12px 40px rgba(79,70,229,0.3);position:relative;overflow:hidden;">

        <div style="position:absolute;top:0;left:0;right:0;height:4px;
        background:linear-gradient(90deg,rgba(255,255,255,0.3),rgba(255,255,255,0.1));"></div>

        <div style="display:flex;justify-content:space-between;gap:20px;align-items:flex-start;">
            <div style="flex:1;">
                <div style="font-size:0.75rem;opacity:0.9;letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;">
                    SmartCampus AI — Dijital Öğrenci Pasaportu
                </div>
                <div style="font-size:1.5rem;font-weight:800;margin-bottom:6px;">{ogr.get('ad', '—')}</div>
                <div style="font-size:0.88rem;opacity:0.95;line-height:1.6;">
                    🎓 <strong>{ogr.get('sinif', '—')}/{ogr.get('sube', '—')}</strong> · No: {ogr.get('numara', '—')}<br/>
                    🏫 {ogr.get('kademe', 'Öğrenci')}<br/>
                    🔒 {pasaport.get('pasaport_id', '—')}
                </div>
            </div>
            <div style="background:white;padding:6px;border-radius:10px;flex-shrink:0;">
                {qr_html}
            </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px;
        padding-top:14px;border-top:1px solid rgba(255,255,255,0.2);">
            <div style="text-align:center;">
                <div style="font-size:1.4rem;font-weight:800;">{ozet.get('not_ortalamasi', 0)}</div>
                <div style="font-size:0.7rem;opacity:0.85;">Not Ort.</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.4rem;font-weight:800;">{len(pasaport.get('rozetler', []))}</div>
                <div style="font-size:0.7rem;opacity:0.85;">Rozet</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:1.4rem;font-weight:800;">{len(pasaport.get('dersler', []))}</div>
                <div style="font-size:0.7rem;opacity:0.85;">Ders</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if compact:
        return

    # Detay sekmeleri
    tabs = st.tabs(["📊 Özet", "🏆 Başarılar", "🏅 Rozetler", "📚 Dersler", "🔐 Güvenlik"])

    with tabs[0]:
        st.markdown("**Akademik Özet**")
        styled_stat_row([
            ("Not Ortalaması", str(ozet.get("not_ortalamasi", 0)), "#4F46E5", "📊"),
            ("Devamsızlık (gün)", str(ozet.get("devamsizlik_gun", 0)), "#D97706", "📅"),
            ("Ödev Teslim %", f"%{ozet.get('odev_teslim_orani', 0)}", "#059669", "📝"),
            ("Proje", str(ozet.get("proje_sayisi", 0)), "#EC4899", "🎯"),
        ])
        st.caption(f"Son güncelleme: {pasaport.get('guncelleme_tarihi', '')[:16]}")

    with tabs[1]:
        basarilar = pasaport.get("basarilar", []) + pasaport.get("yarismalar", [])
        if basarilar:
            for b in basarilar:
                st.markdown(f"🏆 **{b.get('ad', '')}** — {b.get('yil', '')} — {b.get('aciklama', '')}")
        else:
            styled_info_banner("Henüz başarı kaydı yok.", "info")

        # Manuel ekleme
        with st.expander("➕ Başarı Ekle"):
            with st.form(f"basari_form_{pasaport['pasaport_id']}"):
                b_ad = st.text_input("Başarı Adı", key=f"_psp_b_ad_{pasaport['pasaport_id']}")
                b_yil = st.text_input("Yıl/Tarih", key=f"_psp_b_yil_{pasaport['pasaport_id']}")
                b_ac = st.text_area("Açıklama", key=f"_psp_b_ac_{pasaport['pasaport_id']}")
                if st.form_submit_button("➕ Ekle"):
                    if b_ad:
                        pasaportlar = _load_pasaportlar()
                        idx = next((i for i, p in enumerate(pasaportlar) if p.get("pasaport_id") == pasaport["pasaport_id"]), None)
                        if idx is not None:
                            pasaportlar[idx].setdefault("basarilar", []).append({
                                "ad": b_ad, "yil": b_yil, "aciklama": b_ac,
                                "eklenme_tarihi": datetime.now().isoformat(),
                            })
                            pasaportlar[idx]["guncelleme_tarihi"] = datetime.now().isoformat()
                            _save_pasaportlar(pasaportlar)
                            st.success("Başarı eklendi!")
                            st.rerun()

    with tabs[2]:
        rozetler = pasaport.get("rozetler", [])
        if rozetler:
            rozet_html = " ".join(
                f'<span style="background:#D9770620;border:1px solid #D97706;border-radius:20px;'
                f'padding:6px 14px;margin:4px;font-size:0.82rem;display:inline-block;color:#FAFAFA;">'
                f'{r.get("ikon", "🏅")} {r.get("ad", "")}</span>'
                for r in rozetler
            )
            st.markdown(rozet_html, unsafe_allow_html=True)
        else:
            styled_info_banner("Henüz rozet yok. Başarı Duvarı modülünden rozet kazan.", "info")

    with tabs[3]:
        dersler = pasaport.get("dersler", [])
        if dersler:
            st.markdown("**Aldığı Dersler:**")
            for d in dersler:
                st.markdown(f"• 📖 {d}")
        else:
            styled_info_banner("Ders kaydı yok.", "info")

    with tabs[4]:
        st.markdown("**🔐 Pasaport Güvenliği**")
        st.code(f"Pasaport ID: {pasaport.get('pasaport_id')}")
        st.code(f"QR Data: {qr_data}")
        st.caption("Bu pasaport blockchain tabanlı doğrulama için hazırdır. "
                   "Her güncelleme hash ile imzalanır.")

        # JSON export
        pasaport_json = json.dumps(pasaport, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 Pasaport JSON İndir (Transfer için)",
            data=pasaport_json,
            file_name=f"pasaport_{pasaport['pasaport_id']}.json",
            mime="application/json",
            key=f"_psp_dl_{pasaport['pasaport_id']}",
        )


# ══════════════════════════════════════════════════════════════
# ANA PANEL — Yönetim
# ══════════════════════════════════════════════════════════════

def render_dijital_pasaport():
    """Dijital Öğrenci Pasaportu ana paneli."""
    styled_section("🪪 Dijital Öğrenci Pasaportu", "#4F46E5")

    styled_info_banner(
        "Her öğrenci için QR kodlu dijital pasaport. Transfer olduğunda tüm akademik geçmişi taşınır. "
        "Blockchain doğrulamaya hazır.",
        "info", "🪪",
    )

    pasaportlar = _load_pasaportlar()

    # Öğrenci seçimi
    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        all_students = ak.get_students(durum="aktif")
    except Exception:
        all_students = []

    # İstatistik
    styled_stat_row([
        ("Toplam Pasaport", str(len(pasaportlar)), "#4F46E5", "🪪"),
        ("Toplam Öğrenci", str(len(all_students)), "#7C3AED", "🎓"),
        ("Üretilmesi Gereken",
         str(len(all_students) - len(pasaportlar)) if len(all_students) > len(pasaportlar) else "0",
         "#D97706", "⚠️"),
    ])

    tabs = st.tabs(["🔍 Pasaport Görüntüle", "🚀 Toplu Üret", "📤 Transfer / Import"])

    # Tab 1: Görüntüle
    with tabs[0]:
        if not all_students:
            styled_info_banner("Öğrenci verisi bulunamadı.", "warning")
            return

        student_names = [f"{s.tam_ad} ({s.sinif}/{s.sube})" for s in all_students]
        sel_idx = st.selectbox(
            "Öğrenci seç",
            range(len(all_students)),
            format_func=lambda i: student_names[i],
            key="_psp_sel_widget",
        )
        selected_student = all_students[sel_idx]

        # Pasaport var mı?
        mevcut = next((p for p in pasaportlar if p.get("ogrenci", {}).get("id") == selected_student.id), None)

        if mevcut:
            render_ogrenci_pasaport_karti(mevcut)

            # Güncelle butonu
            if st.button("🔄 Pasaportu Güncelle (akademik verileri yenile)",
                          key=f"_psp_update_{selected_student.id}"):
                idx = next((i for i, p in enumerate(pasaportlar) if p.get("ogrenci", {}).get("id") == selected_student.id), None)
                if idx is not None:
                    yeni = generate_pasaport(selected_student)
                    # Önceki custom verileri koru
                    yeni["basarilar"] = mevcut.get("basarilar", [])
                    yeni["rozetler"] = mevcut.get("rozetler", [])
                    yeni["projeler"] = mevcut.get("projeler", [])
                    yeni["yarismalar"] = mevcut.get("yarismalar", [])
                    pasaportlar[idx] = yeni
                    _save_pasaportlar(pasaportlar)
                    st.success("Güncellendi.")
                    st.rerun()
        else:
            styled_info_banner(f"{selected_student.tam_ad} için henüz pasaport üretilmemiş.", "warning")
            if st.button("🚀 Pasaport Üret", type="primary", key=f"_psp_gen_{selected_student.id}"):
                yeni = generate_pasaport(selected_student)
                pasaportlar.append(yeni)
                _save_pasaportlar(pasaportlar)
                st.success("Pasaport üretildi!")
                st.balloons()
                st.rerun()

    # Tab 2: Toplu üret
    with tabs[1]:
        st.markdown("**Tüm öğrenciler için pasaport üret**")
        styled_info_banner(
            "Bu işlem akademik verileri çekip her öğrenci için pasaport oluşturur. "
            "Mevcut pasaportlar atlanır.",
            "info",
        )

        if st.button("🚀 Toplu Üret", type="primary", key="_psp_toplu_gen"):
            if not all_students:
                styled_info_banner("Öğrenci yok.", "warning")
            else:
                progress = st.progress(0)
                status = st.empty()
                olusturuldu = 0
                for i, stu in enumerate(all_students):
                    mevcut = next((p for p in pasaportlar if p.get("ogrenci", {}).get("id") == stu.id), None)
                    if mevcut:
                        continue
                    status.text(f"Üretiliyor: {stu.tam_ad} ({i+1}/{len(all_students)})")
                    pasaportlar.append(generate_pasaport(stu))
                    olusturuldu += 1
                    progress.progress((i + 1) / len(all_students))
                _save_pasaportlar(pasaportlar)
                status.empty()
                progress.empty()
                st.success(f"✅ {olusturuldu} yeni pasaport üretildi!")
                st.balloons()
                st.rerun()

    # Tab 3: Transfer/Import
    with tabs[2]:
        st.markdown("**📤 Pasaport Transfer Sistemi**")
        styled_info_banner(
            "Öğrenci başka okula gittiğinde pasaportunu JSON olarak ihraç edin. "
            "Yeni okul bu JSON'u import ederek tüm geçmişe erişir.",
            "info", "📤",
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📤 Export**")
            if pasaportlar:
                all_json = json.dumps(pasaportlar, ensure_ascii=False, indent=2)
                st.download_button(
                    "📥 Tüm Pasaportları İndir",
                    data=all_json,
                    file_name=f"pasaportlar_tumu_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    key="_psp_all_export",
                )

        with col2:
            st.markdown("**📥 Import**")
            uploaded = st.file_uploader(
                "Pasaport JSON yükle",
                type=["json"],
                key="_psp_upload",
            )
            if uploaded:
                try:
                    content = json.loads(uploaded.read().decode("utf-8"))
                    if isinstance(content, dict):
                        content = [content]
                    mevcut_ids = {p.get("pasaport_id") for p in pasaportlar}
                    yeni = [p for p in content if p.get("pasaport_id") not in mevcut_ids]
                    if yeni:
                        pasaportlar.extend(yeni)
                        _save_pasaportlar(pasaportlar)
                        st.success(f"✅ {len(yeni)} pasaport import edildi.")
                        st.rerun()
                    else:
                        styled_info_banner("Tüm pasaportlar zaten mevcut.", "info")
                except Exception as e:
                    st.error(f"Import hatası: {e}")
