"""Öğrenci Defteri — Kapsamlı akademik analiz, grafik ve AI tavsiyesi.

Analiz edilen veri kaynakları:
  ─── Akademik ──────────────────────────────────────────────────────
  • GradeRecord       not kayıtları (yazılı / sözlü / performans / proje)
  • AttendanceRecord  devamsızlık (özürlü / özürsüz / gün / saat)
  • KazanimBorc       kazanım borç bankası (aktif / kapatılan)
  • Odev / OdevTeslim ödev atamaları ve teslim durumları
  • ExamResult        ölçme-değerlendirme sınav sonuçları + kazanım breakdown
  • TelafiGorev       telafi görevleri (RED/YELLOW/GREEN/BLUE)
  • KazanimIsleme     sınıfta işlenen kazanımlar
  • KYT               günlük kazanım takip testleri ve başarı analizi
  • EtutKayit         etüt / destek dersi kayıtları
  ─── Sağlık & Rehberlik ────────────────────────────────────────────
  • RevirZiyareti     revir başvuruları, takip gereksinimi
  • RehberlikVaka     vaka kayıtları, öncelik ve risk seviyeleri
  • RehberlikGorusme  PDR görüşme geçmişi
"""

import datetime
import io
import os
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from models.akademik_takip import (
    AkademikDataStore,
    get_akademik_store,
    Student,
    BORC_NEDENI_LABELS,
)
from models.olcme_degerlendirme import DataStore as OlcmeDataStore
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("ogrenci_360")
except Exception:
    pass


# ── Stil yardımcıları ──────────────────────────────────────────────────────────

def _section(title: str, color: str = "#2563eb"):
    st.markdown(
        f"<div style='background:{color};color:#fff;padding:7px 16px;"
        f"border-radius:8px;margin:12px 0 8px 0;font-weight:700;"
        f"font-size:0.92rem;letter-spacing:.3px'>{title}</div>",
        unsafe_allow_html=True,
    )


def _info(text: str, kind: str = "info"):
    colors = {
        "info":    ("#eff6ff", "#2563eb", "#3b82f6"),
        "warning": ("#fffbeb", "#b45309", "#f59e0b"),
        "success": ("#f0fdf4", "#166534", "#22c55e"),
        "error":   ("#fef2f2", "#991b1b", "#ef4444"),
    }
    bg, fg, border = colors.get(kind, colors["info"])
    st.markdown(
        f"<div style='background:{bg};color:{fg};border-left:4px solid {border};"
        f"padding:10px 14px;border-radius:6px;margin:6px 0;font-size:0.87rem'>{text}</div>",
        unsafe_allow_html=True,
    )


def _risk_level(score: int):
    if score <= 25:
        return "🟢", "#22c55e", "Düşük Risk", "#f0fdf4", "#166534"
    elif score <= 55:
        return "🟡", "#f59e0b", "Orta Risk", "#fffbeb", "#b45309"
    elif score <= 75:
        return "🔴", "#ef4444", "Yüksek Risk", "#fef2f2", "#991b1b"
    else:
        return "⛔", "#7c3aed", "Kritik Risk", "#faf5ff", "#6d28d9"


# ── Yardımcı store erişimi ─────────────────────────────────────────────────────

def _saglik_store():
    try:
        from models.okul_sagligi import SaglikDataStore
        from utils.tenant import get_tenant_dir
        return SaglikDataStore(os.path.join(get_tenant_dir(), "saglik"))
    except Exception:
        return None


def _rehberlik_store():
    try:
        from models.rehberlik import RehberlikDataStore
        from utils.tenant import get_tenant_dir
        return RehberlikDataStore(os.path.join(get_tenant_dir(), "rehberlik"))
    except Exception:
        return None


def _get_akademik_yil() -> str:
    y = datetime.date.today().year
    m = datetime.date.today().month
    return f"{y}-{y+1}" if m >= 9 else f"{y-1}-{y}"


# ── Veri toplama ───────────────────────────────────────────────────────────────

def _collect_data(
    store: AkademikDataStore,
    od: OlcmeDataStore,
    student: Student,
    akademik_yil: str = "",
) -> dict:
    """Öğrenciye ait tüm analiz verisini toplar."""
    sid = student.id
    ay = akademik_yil or None

    # ── Akademik veriler ──
    grades      = store.get_grades(student_id=sid, akademik_yil=ay)
    attendance  = store.get_attendance(student_id=sid, akademik_yil=ay)
    dev_ozet    = store.get_attendance_summary(sid, ay)
    odevler     = store.get_odevler(sinif=student.sinif, sube=student.sube, akademik_yil=ay)
    teslimler   = store.get_odev_teslimleri(student_id=sid)
    teslim_ids  = {t.odev_id for t in teslimler if t.durum in ("teslim_edildi", "gecikti")}
    teslim_oran = round(len(teslim_ids) / len(odevler) * 100, 1) if odevler else 100.0

    borclar     = store.get_kazanim_borclari(student_id=sid, akademik_yil=ay)
    aktif_borc  = [b for b in borclar if b.durum == "borc_var"]

    exam_results = od.get_results(student_id=sid)
    try:
        telafi = od.get_telafi_tasks(student_id=sid)
    except Exception:
        telafi = []

    kazanim_isleme = store.get_kazanim_isleme(sinif=student.sinif, sube=student.sube, akademik_yil=ay)
    etut_kayitlari = store.get_etut_kayitlari(sinif=student.sinif, sube=student.sube, akademik_yil=ay)

    # KYT
    kyt_analiz: dict = {}
    kyt_cevaplar = []
    try:
        kyt_analiz = store.get_kyt_ogrenci_analizi(student_id=sid, akademik_yil=ay or _get_akademik_yil())
        kyt_cevaplar = store.get_kyt_cevaplar(student_id=sid)
    except Exception:
        kyt_analiz = {"toplam": 0, "dogru": 0, "yanlis": 0, "bos": 0, "basari_yuzde": 0}

    # ── Sağlık (revir) ──
    revir_ziyaretleri = []
    try:
        ss = _saglik_store()
        if ss:
            revir_ziyaretleri = ss.find_by_field("revir_ziyaretleri", "ogrenci_id", sid)
    except Exception:
        pass

    # ── Rehberlik ──
    rehberlik_vakalar   = []
    rehberlik_gorusmeler = []
    try:
        rs = _rehberlik_store()
        if rs:
            rehberlik_vakalar    = rs.find_by_field("vakalar",    "ogrenci_id", sid)
            rehberlik_gorusmeler = rs.find_by_field("gorusmeler", "ogrenci_id", sid)
    except Exception:
        pass

    return {
        "grades":               grades,
        "attendance":           attendance,
        "dev_ozet":             dev_ozet,
        "odevler":              odevler,
        "teslimler":            teslimler,
        "teslim_ids":           teslim_ids,
        "teslim_oran":          teslim_oran,
        "borclar":              borclar,
        "aktif_borc":           aktif_borc,
        "exam_results":         exam_results,
        "telafi":               telafi,
        "kazanim_isleme":       kazanim_isleme,
        "etut_kayitlari":       etut_kayitlari,
        "kyt_analiz":           kyt_analiz,
        "kyt_cevaplar":         kyt_cevaplar,
        "revir_ziyaretleri":    revir_ziyaretleri,
        "rehberlik_vakalar":    rehberlik_vakalar,
        "rehberlik_gorusmeler": rehberlik_gorusmeler,
    }


# ── Risk skoru hesaplama ───────────────────────────────────────────────────────

def _calc_risk(data: dict) -> dict:
    """
    Akademik + sağlık + rehberlik verilerini birleştirerek 0-100 risk skoru üretir.
    Düşük skor = iyi durum.
    """
    score = 0
    breakdown = {}

    # ── 1. Not ortalaması (max +40) ──
    puan_list = [g.puan for g in data["grades"] if g.puan and g.puan > 0]
    not_ort = round(sum(puan_list) / len(puan_list), 1) if puan_list else 0
    not_risk = (40 if not_ort < 50 else 20 if not_ort < 70 else 8 if not_ort < 85 else 0) if not_ort else 0
    score += not_risk
    breakdown["not_ort"] = {"deger": f"{not_ort}/100", "risk": not_risk, "etiket": "Not Ortalaması",
                             "aciklama": "Tüm ders notlarının ağırlıksız ortalaması"}

    # ── 2. Devamsızlık (max +30) ──
    dev_ozet   = data["dev_ozet"]
    toplam_dev = dev_ozet.get("toplam", 0)
    ozursuz    = dev_ozet.get("ozursuz", 0)
    dev_risk   = min(int(toplam_dev * 1.5) + int(ozursuz * 1.0), 30)
    score += dev_risk
    breakdown["devamsizlik"] = {
        "deger": f"{toplam_dev} gün ({ozursuz} özürsüz)", "risk": dev_risk,
        "etiket": "Devamsızlık", "aciklama": "Toplam devamsızlık; özürsüz devamsızlık ekstra ağırlıklı"}

    # ── 3. Ödev teslim oranı (max +20) ──
    teslim_oran = data["teslim_oran"]
    odev_risk   = min(int((100 - teslim_oran) * 0.20), 20)
    score += odev_risk
    breakdown["odev"] = {
        "deger": f"%{teslim_oran}", "risk": odev_risk,
        "etiket": "Ödev Teslim", "aciklama": "Atanan ödevlerin teslim yüzdesi"}

    # ── 4. Kazanım borcu (max +20) ──
    aktif_borc = len(data["aktif_borc"])
    borc_risk  = min(aktif_borc * 2, 20)
    score += borc_risk
    breakdown["borc"] = {
        "deger": f"{aktif_borc} kazanım", "risk": borc_risk,
        "etiket": "Kazanım Borcu", "aciklama": "Devamsızlık veya ödev eksikliğinden doğan aktif borçlar"}

    # ── 5. Sınav (ölçme-değerlendirme) ortalaması (max +10) ──
    # ÖD modülü kullanılmadıysa (sınav yoksa) bu bileşen risk haritasına dahil edilmez
    sinav_puanlar = [r.score for r in data["exam_results"] if r.score and r.score > 0]
    sinav_ort     = round(sum(sinav_puanlar) / len(sinav_puanlar), 1) if sinav_puanlar else 0
    od_kullaniliyor = len(data["exam_results"]) > 0
    if od_kullaniliyor:
        sinav_risk = 10 if sinav_ort < 50 else 5 if sinav_ort < 70 else 0
        score += sinav_risk
        breakdown["sinav"] = {
            "deger": f"{sinav_ort}/100", "risk": sinav_risk,
            "etiket": "Sınav Ortalaması", "aciklama": "Ölçme-değerlendirme modülündeki sınav puanları"}
    else:
        sinav_risk = 0

    # ── 6. KYT (günlük kazanım testi) başarısı (max +10) ──
    kyt_analiz  = data["kyt_analiz"]
    kyt_basari  = kyt_analiz.get("basari_yuzde", 0) if kyt_analiz.get("toplam", 0) > 0 else -1
    kyt_risk    = (0 if kyt_basari < 0 else 10 if kyt_basari < 50 else 5 if kyt_basari < 70 else 0)
    score += kyt_risk
    kyt_deger = f"%{kyt_basari}" if kyt_basari >= 0 else "Veri yok"
    breakdown["kyt"] = {
        "deger": kyt_deger, "risk": kyt_risk,
        "etiket": "KYT Başarısı", "aciklama": "Günlük kazanım takip testi doğruluk oranı"}

    # ── 7. Telafi görevleri (max +10) ──
    # ÖD modülü kullanılmadıysa telafi görevi de oluşmaz → risk haritasına dahil edilmez
    telafi_bekl = [t for t in data["telafi"] if getattr(t, "status", "") != "tamamlandi"]
    red_count   = sum(1 for t in telafi_bekl if getattr(t, "color_band", "") == "RED")
    if od_kullaniliyor:
        telafi_risk = min(red_count * 3 + len(telafi_bekl), 10)
        score += telafi_risk
        breakdown["telafi"] = {
            "deger": f"{len(telafi_bekl)} bekliyor ({red_count} RED)",
            "risk": telafi_risk, "etiket": "Telafi Görevleri",
            "aciklama": "Tamamlanmamış telafi görevleri; RED bant daha yüksek risk"}
    else:
        telafi_risk = 0

    # ── 8. Revir ziyaretleri (max +10) ──
    revir        = data["revir_ziyaretleri"]
    takip_sayisi = sum(1 for z in revir if getattr(z, "takip_gerekiyor", False))
    revir_risk   = min(takip_sayisi * 3 + (len(revir) // 3), 10)
    score += revir_risk
    breakdown["revir"] = {
        "deger": f"{len(revir)} ziyaret ({takip_sayisi} takipli)",
        "risk": revir_risk, "etiket": "Revir Ziyaretleri",
        "aciklama": "Revir başvuruları; takip gerektiren vakalar daha yüksek ağırlıklı"}

    # ── 9. Rehberlik vakaları (max +15) ──
    vakalar      = data["rehberlik_vakalar"]
    acik_vakalar = [v for v in vakalar if getattr(v, "durum", "") in ("ACIK", "TAKIPTE")]
    yuksek_risk_vaka = sum(
        1 for v in vakalar
        if getattr(v, "risk_seviyesi", "") in ("YUKSEK", "KRITIK", "ACIL")
        or getattr(v, "oncelik", "") in ("ACIL", "YUKSEK")
    )
    rehber_risk  = min(len(acik_vakalar) * 4 + yuksek_risk_vaka * 5, 15)
    score += rehber_risk
    breakdown["rehberlik"] = {
        "deger": f"{len(vakalar)} vaka ({len(acik_vakalar)} açık, {yuksek_risk_vaka} yüksek risk)",
        "risk": rehber_risk, "etiket": "Rehberlik Vakaları",
        "aciklama": "PDR vaka kayıtları; açık ve yüksek öncelikli vakalar risk faktörü"}

    # ── 10. Etüt katılımı — koruyucu faktör (max -5) ──
    etut = data["etut_kayitlari"]
    etut_bonus = min(len(etut) // 3, 5)  # Etüt risk azaltır
    score = max(0, score - etut_bonus)
    breakdown["etut"] = {
        "deger": f"{len(etut)} kayıt (−{etut_bonus} risk)",
        "risk": -etut_bonus, "etiket": "Etüt Katılımı",
        "aciklama": "Etüt/destek derslerine katılım akademik riski azaltır"}

    score = min(score, 100)
    return {
        "score": score,
        "breakdown": breakdown,
        "not_ort": not_ort,
        "sinav_ort": sinav_ort,
        "kyt_basari": kyt_basari,
    }


# ── Tab 1: Genel Özet ──────────────────────────────────────────────────────────

def _tab_genel_ozet(student: Student, data: dict, risk: dict):
    ikon, renk, etiket, bg, fg = _risk_level(risk["score"])

    # Risk kartı
    st.markdown(
        f"<div style='background:{bg};border:2px solid {renk};border-radius:14px;"
        f"padding:18px 24px;margin-bottom:18px;display:flex;align-items:center;gap:18px'>"
        f"<div style='font-size:3rem'>{ikon}</div>"
        f"<div>"
        f"<div style='color:{fg};font-size:1.3rem;font-weight:800'>{etiket}</div>"
        f"<div style='color:{fg};font-size:0.87rem;margin-top:2px'>"
        f"Akademik Risk Skoru: <b>{risk['score']}/100</b> "
        f"— 10 farklı veri kaynağı analiz edildi</div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # Stat kartları (2 satır × 4)
    dev_ozet    = data["dev_ozet"]
    aktif_borc  = len(data["aktif_borc"])
    teslim_oran = data["teslim_oran"]
    kyt_analiz  = data["kyt_analiz"]
    kyt_b       = kyt_analiz.get("basari_yuzde", 0) if kyt_analiz.get("toplam", 0) > 0 else None
    revir_cnt   = len(data["revir_ziyaretleri"])
    vaka_acik   = sum(1 for v in data["rehberlik_vakalar"] if getattr(v, "durum", "") in ("ACIK", "TAKIPTE"))
    etut_cnt    = len(data["etut_kayitlari"])
    telafi_bekl = sum(1 for t in data["telafi"] if getattr(t, "status", "") != "tamamlandi")

    def _kart(ic, lbl, val, c):
        return (
            f"<div style='background:linear-gradient(135deg,#ffffff,#111827);"
            f"border:1.5px solid #e2e8f0;border-radius:14px;"
            f"padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06);"
            f"transition:transform 0.15s'>"
            f"<div style='font-size:1.6rem'>{ic}</div>"
            f"<div style='color:#64748b;font-size:0.7rem;margin:5px 0;font-weight:600;"
            f"letter-spacing:0.3px;text-transform:uppercase'>{lbl}</div>"
            f"<div style='color:{c};font-size:1.3rem;font-weight:800'>{val}</div>"
            f"</div>"
        )

    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)

    r1c1.markdown(_kart("📊", "Not Ort.", f"{risk['not_ort']}",
                         "#22c55e" if risk["not_ort"] >= 70 else "#f59e0b" if risk["not_ort"] >= 50 else "#ef4444"),
                  unsafe_allow_html=True)
    r1c2.markdown(_kart("📅", "Devamsızlık", f"{dev_ozet.get('toplam', 0)} gün",
                         "#ef4444" if dev_ozet.get("toplam", 0) > 10 else "#22c55e"),
                  unsafe_allow_html=True)
    r1c3.markdown(_kart("📚", "Ödev Teslim", f"%{teslim_oran}",
                         "#22c55e" if teslim_oran >= 80 else "#f59e0b" if teslim_oran >= 60 else "#ef4444"),
                  unsafe_allow_html=True)
    r1c4.markdown(_kart("🎯", "Kazanım Borcu", f"{aktif_borc} aktif",
                         "#22c55e" if aktif_borc == 0 else "#f59e0b" if aktif_borc <= 3 else "#ef4444"),
                  unsafe_allow_html=True)

    kyt_val = f"%{kyt_b}" if kyt_b is not None else "—"
    kyt_clr = "#22c55e" if (kyt_b or 0) >= 70 else "#f59e0b" if (kyt_b or 0) >= 50 else "#ef4444"
    r2c1.markdown(_kart("🧪", "KYT Başarısı", kyt_val, kyt_clr if kyt_b is not None else "#94a3b8"),
                  unsafe_allow_html=True)
    r2c2.markdown(_kart("🏥", "Revir", f"{revir_cnt} ziyaret",
                         "#f59e0b" if revir_cnt > 3 else "#22c55e"),
                  unsafe_allow_html=True)
    r2c3.markdown(_kart("🧠", "Rehberlik", f"{vaka_acik} açık vaka",
                         "#ef4444" if vaka_acik > 0 else "#22c55e"),
                  unsafe_allow_html=True)
    r2c4.markdown(_kart("📖", "Etüt", f"{etut_cnt} kayıt",
                         "#22c55e" if etut_cnt > 0 else "#94a3b8"),
                  unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk bileşenleri tablosu — premium
    st.markdown(
        "<div style='background:linear-gradient(135deg,#1A2035,#e2e8f0);border-radius:12px;"
        "padding:12px 16px;margin-bottom:12px;border:1.5px solid #cbd5e1'>"
        "<div style='font-weight:700;color:#334155;font-size:0.92rem'>"
        "📋 Risk Bileşeni Detayı (10 Kaynak)</div></div>",
        unsafe_allow_html=True,
    )
    bd = risk["breakdown"]
    for key, v in bd.items():
        r = v["risk"]
        if r < 0:
            durum, dc, dbg = "✅ Koruyucu", "#22c55e", "#f0fdf4"
        elif r == 0:
            durum, dc, dbg = "✅ İyi", "#22c55e", "#f0fdf4"
        elif r <= 5:
            durum, dc, dbg = "🟡 Hafif", "#f59e0b", "#fffbeb"
        elif r <= 10:
            durum, dc, dbg = "🔴 Dikkat", "#ef4444", "#fef2f2"
        else:
            durum, dc, dbg = "⛔ Kritik", "#7c3aed", "#faf5ff"
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;padding:10px 14px;"
            f"background:{dbg};border-left:4px solid {dc};border-radius:0 10px 10px 0;"
            f"margin:4px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04)'>"
            f"<div style='flex:3;font-weight:600;font-size:0.85rem;color:#94A3B8'>{v['etiket']}</div>"
            f"<div style='flex:2.5;font-size:0.82rem;color:#475569'>{v['deger']}</div>"
            f"<div style='flex:1;text-align:center'>"
            f"<span style='background:{dc}22;color:{dc};padding:2px 8px;border-radius:8px;"
            f"font-size:0.72rem;font-weight:700'>{r}</span></div>"
            f"<div style='flex:1.5;text-align:right'>"
            f"<span style='color:{dc};font-weight:600;font-size:0.82rem'>{durum}</span></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Kritik uyarılar
    toplam_dev = dev_ozet.get("toplam", 0)
    if toplam_dev >= 20:
        _info(f"⛔ Toplam <b>{toplam_dev}</b> gün devamsızlık — yasal sınır aşıldı. Veli ile acil görüşme gerekli.", "error")
    elif toplam_dev >= 10:
        _info(f"⚠️ Toplam <b>{toplam_dev}</b> gün devamsızlık — izleme altına alınmalı.", "warning")

    acik_vakalar = [v for v in data["rehberlik_vakalar"] if getattr(v, "durum", "") in ("ACIK", "TAKIPTE")]
    for v in acik_vakalar:
        oncelik = getattr(v, "oncelik", "") or ""
        baslik  = getattr(v, "vaka_basligi", "Rehberlik vakası") or "Rehberlik vakası"
        if oncelik in ("ACIL", "YUKSEK"):
            _info(f"⛔ Açık rehberlik vakası: <b>{baslik}</b> [{oncelik}]", "error")
        else:
            _info(f"🧠 Açık rehberlik vakası: <b>{baslik}</b>", "warning")

    if telafi_bekl > 0:
        _info(f"📌 <b>{telafi_bekl}</b> tamamlanmamış telafi görevi var.", "warning")


# ── Tab 2: Grafikler ───────────────────────────────────────────────────────────

def _tab_grafikler(student: Student, data: dict, risk: dict):
    grades       = data["grades"]
    attendance   = data["attendance"]
    exam_results = data["exam_results"]
    odevler      = data["odevler"]
    teslimler    = data["teslimler"]
    kyt_analiz   = data["kyt_analiz"]

    # — Radar: genel performans —
    _section("Akademik Performans Radarı", "#94A3B8")
    not_ort    = risk["not_ort"]
    sinav_ort  = risk["sinav_ort"]
    kyt_b      = kyt_analiz.get("basari_yuzde", 0) if kyt_analiz.get("toplam", 0) > 0 else 0
    devam_skor = max(0, 100 - data["dev_ozet"].get("toplam", 0) * 2)
    odev_skor  = data["teslim_oran"]
    borc_skor  = max(0, 100 - len(data["aktif_borc"]) * 10)
    revir_skor = max(0, 100 - len(data["revir_ziyaretleri"]) * 8)
    rehber_skor = max(0, 100 - sum(
        1 for v in data["rehberlik_vakalar"] if getattr(v, "durum", "") in ("ACIK", "TAKIPTE")
    ) * 20)

    categories = ["Not Ort.", "Sınav", "KYT", "Devam", "Ödev", "Kazanım", "Sağlık", "Rehberlik"]
    values     = [not_ort, sinav_ort, kyt_b, devam_skor, odev_skor, borc_skor, revir_skor, rehber_skor]
    fig_radar = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(37,99,235,0.15)",
        line=dict(color="#2563eb", width=2),
        marker=dict(size=6),
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                   tickfont=dict(size=9), gridcolor="#e5e7eb"),
                   angularaxis=dict(tickfont=dict(size=10))),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=10, r=10), height=320,
        showlegend=False,
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="dft_radar",
                    config=SC_CHART_CFG)

    col_a, col_b = st.columns(2)

    with col_a:
        # — Not bar grafiği —
        _section("Ders Bazlı Not Ort.", "#2563eb")
        if grades:
            ders_nots: dict[str, list] = defaultdict(list)
            for g in grades:
                if g.puan and g.puan > 0:
                    ders_nots[g.ders].append(g.puan)
            if ders_nots:
                df_nots = pd.DataFrame([
                    {"Ders": d, "Ort.": round(sum(v)/len(v), 1)}
                    for d, v in ders_nots.items()
                ]).sort_values("Ort.", ascending=True)
                clrs = ["#22c55e" if x >= 70 else "#f59e0b" if x >= 50 else "#ef4444"
                        for x in df_nots["Ort."]]
                fig2 = go.Figure(go.Bar(
                    y=df_nots["Ders"], x=df_nots["Ort."], orientation="h",
                    marker_color=clrs, text=df_nots["Ort."].astype(str), textposition="outside",
                ))
                fig2.add_vline(x=70, line_dash="dot", line_color="#22c55e")
                sc_bar(fig2, height=max(200, len(df_nots) * 34), horizontal=True)
                fig2.update_layout(xaxis=dict(range=[0, 115]))
                st.plotly_chart(fig2, use_container_width=True, key="dft_ders_bar",
                                config=SC_CHART_CFG)
        else:
            _info("Not kaydı yok.", "info")

    with col_b:
        # — Devamsızlık aylık trendi —
        _section("Aylık Devamsızlık", "#ef4444")
        if attendance:
            ay_say: dict[str, int] = defaultdict(int)
            for a in attendance:
                try:
                    ay_say[a.tarih[:7]] += 1
                except Exception:
                    pass
            if ay_say:
                df_dev = pd.DataFrame(sorted(ay_say.items()), columns=["Ay", "Gün"])
                fig3 = go.Figure(go.Bar(
                    x=df_dev["Ay"], y=df_dev["Gün"],
                    marker_color=["#ef4444" if v > 3 else "#f59e0b" if v > 1 else "#22c55e"
                                  for v in df_dev["Gün"]],
                    text=df_dev["Gün"].astype(str), textposition="outside",
                ))
                sc_bar(fig3, height=260)
                fig3.update_layout(xaxis=dict(tickangle=-30))
                st.plotly_chart(fig3, use_container_width=True, key="dft_dev_bar",
                                config=SC_CHART_CFG)
        else:
            _info("Devamsızlık kaydı yok — devam durumu iyi.", "success")

    col_c, col_d = st.columns(2)

    with col_c:
        # — Sınav trendi —
        _section("Sınav Skoru Trendi", "#7c3aed")
        if exam_results:
            df_ex = pd.DataFrame([
                {"Tarih": (r.graded_at or "")[:10], "Puan": r.score}
                for r in sorted(exam_results, key=lambda x: x.graded_at or "")
                if r.score and r.score > 0
            ])
            if not df_ex.empty:
                fig4 = go.Figure(go.Scatter(
                    x=df_ex["Tarih"], y=df_ex["Puan"],
                    mode="lines+markers+text",
                    line=dict(color="#7c3aed", width=2), marker=dict(size=7),
                    text=df_ex["Puan"].round(1).astype(str), textposition="top center",
                    fill="tozeroy", fillcolor="rgba(124,58,237,0.07)",
                ))
                fig4.add_hline(y=50, line_dash="dot", line_color="#ef4444")
                fig4.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=10, l=10, r=10), height=260,
                    yaxis=dict(range=[0, 110], gridcolor="#1A2035", tickfont_size=9),
                    xaxis=dict(tickangle=-30, tickfont_size=9),
                )
                st.plotly_chart(fig4, use_container_width=True, key="dft_sinav_trend",
                                config=SC_CHART_CFG)
        else:
            _info("Sınav kaydı yok.", "info")

    with col_d:
        # — KYT başarı trendi —
        _section("KYT Günlük Başarı", "#0891b2")
        kyt_cevaplar = data.get("kyt_cevaplar", [])
        if kyt_cevaplar:
            gun_say: dict[str, list] = defaultdict(list)
            for c in kyt_cevaplar:
                tarih = getattr(c, "tarih", "") or ""
                if tarih:
                    gun_say[tarih].append(1 if getattr(c, "dogru_mu", False) else 0)
            if gun_say:
                df_kyt = pd.DataFrame(
                    sorted([
                        {"Tarih": t, "Başarı %": round(sum(v)/len(v)*100, 1)}
                        for t, v in gun_say.items()
                    ], key=lambda x: x["Tarih"])
                )
                fig5 = go.Figure(go.Scatter(
                    x=df_kyt["Tarih"], y=df_kyt["Başarı %"],
                    mode="lines+markers",
                    line=dict(color="#0891b2", width=2), marker=dict(size=6),
                    fill="tozeroy", fillcolor="rgba(8,145,178,0.08)",
                ))
                fig5.add_hline(y=70, line_dash="dot", line_color="#22c55e")
                fig5.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=10, l=10, r=10), height=260,
                    yaxis=dict(range=[0, 110], gridcolor="#1A2035", tickfont_size=9),
                    xaxis=dict(tickangle=-30, tickfont_size=9),
                )
                st.plotly_chart(fig5, use_container_width=True, key="dft_kyt_trend",
                                config=SC_CHART_CFG)
        else:
            _info("KYT cevap kaydı yok.", "info")

    # — Revir ziyaret kategorileri —
    revir = data["revir_ziyaretleri"]
    if revir:
        _section("Revir Ziyaret Kategorileri", "#ef4444")
        kat_say: dict[str, int] = defaultdict(int)
        for z in revir:
            kat = getattr(z, "sikayet_kategorisi", "Belirtilmedi") or "Belirtilmedi"
            kat_say[kat] += 1
        if kat_say:
            _labels = list(kat_say.keys())
            _values = list(kat_say.values())
            _n = len(_labels)
            fig6 = go.Figure(go.Pie(
                labels=_labels, values=_values,
                marker=dict(colors=SC_COLORS[:_n], line=dict(color="#fff", width=2)),
                hole=0.55,
            ))
            sc_pie(fig6)
            st.plotly_chart(fig6, use_container_width=True, key="dft_revir_pie",
                            config=SC_CHART_CFG)


# ── Tab 3: Kazanım & Ödev ─────────────────────────────────────────────────────

def _tab_kazanim_odev(student: Student, data: dict):
    aktif_borc  = data["aktif_borc"]
    kapali_borc = [b for b in data["borclar"] if b.durum == "kapandi"]
    odevler     = data["odevler"]
    teslimler   = data["teslimler"]
    etut        = data["etut_kayitlari"]

    # — Kazanım borç özeti —
    _section(f"Kazanım Borç Bankası — {len(aktif_borc)} aktif", "#7c3aed")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Borç", len(data["borclar"]))
    c2.metric("Aktif", len(aktif_borc))
    c3.metric("Kapatılan", len(kapali_borc))
    c4.metric("Borçlu Ders", len({b.ders for b in aktif_borc}))

    if aktif_borc:
        ders_borc: dict[str, int] = defaultdict(int)
        for b in aktif_borc:
            ders_borc[b.ders] += 1
        df_b = pd.DataFrame(sorted(ders_borc.items(), key=lambda x: -x[1]),
                            columns=["Ders", "Borç"])
        fig = go.Figure(go.Bar(
            x=df_b["Borç"], y=df_b["Ders"], orientation="h",
            marker_color=SC_COLORS[0],
            text=df_b["Borç"].astype(str), textposition="outside",
        ))
        sc_bar(fig, height=max(160, len(df_b) * 36), horizontal=True)
        st.plotly_chart(fig, use_container_width=True, key="dft_borc_bar2",
                        config=SC_CHART_CFG)

        with st.expander("📋 Aktif Borç Listesi", expanded=False):
            for b in aktif_borc[:30]:
                neden = BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)
                st.markdown(
                    f"<div style='background:#faf5ff;border-left:3px solid #7c3aed;"
                    f"padding:7px 12px;border-radius:5px;margin:3px 0;font-size:0.82rem'>"
                    f"<b>{b.ders}</b> — {b.kazanim_metni or b.kazanim_kodu} "
                    f"<span style='color:#7c3aed;font-size:0.74rem'>({neden})</span></div>",
                    unsafe_allow_html=True,
                )
    else:
        _info("Aktif kazanım borcu bulunmuyor 🎉", "success")

    # — KYT özeti —
    kyt_analiz = data["kyt_analiz"]
    if kyt_analiz.get("toplam", 0) > 0:
        _section("KYT Performans Özeti", "#0891b2")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Toplam Soru", kyt_analiz.get("toplam", 0))
        k2.metric("Doğru", kyt_analiz.get("dogru", 0))
        k3.metric("Yanlış", kyt_analiz.get("yanlis", 0))
        k4.metric("Başarı %", f"%{kyt_analiz.get('basari_yuzde', 0)}")

    # — Ödev teslim —
    _section(f"Ödev Teslim Durumu — {len(odevler)} ödev", "#f59e0b")
    if odevler:
        teslim_map = {t.odev_id: t for t in teslimler}
        DURUM_RENK = {
            "teslim_edildi": "#22c55e", "gecikti": "#f59e0b",
            "teslim_edilmedi": "#ef4444", "bekliyor": "#94a3b8", "muaf": "#0891b2",
        }
        DURUM_L = {
            "teslim_edildi": "✅ Teslim", "gecikti": "⏰ Geç",
            "teslim_edilmedi": "❌ Teslim Edilmedi", "bekliyor": "⏳ Bekliyor", "muaf": "🔵 Muaf",
        }
        for odev in sorted(odevler, key=lambda x: x.son_teslim_tarihi or "", reverse=True)[:25]:
            teslim = teslim_map.get(odev.id)
            durum  = teslim.durum if teslim else "bekliyor"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"background:#fffbeb;border-left:3px solid {DURUM_RENK.get(durum,'#94a3b8')};"
                f"padding:6px 12px;border-radius:5px;margin:3px 0;font-size:0.82rem'>"
                f"<span><b>{odev.ders}</b> — {odev.baslik} "
                f"<span style='color:#94a3b8;font-size:0.73rem'>({odev.son_teslim_tarihi or '–'})</span></span>"
                f"<span style='color:{DURUM_RENK.get(durum, '#94a3b8')};font-weight:700'>"
                f"{DURUM_L.get(durum, durum)}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        _info("Bu sınıf/şube için ödev kaydı bulunamadı.", "info")

    # — Etüt / destek dersleri —
    if etut:
        _section(f"Etüt & Destek Dersleri — {len(etut)} kayıt", "#059669")
        TUR_L = {"etut": "📖 Etüt", "destek_dersi": "🎓 Destek", "telafi": "🔄 Telafi"}
        for e in sorted(etut, key=lambda x: x.tarih, reverse=True)[:10]:
            tur_l = TUR_L.get(e.tur, e.tur)
            st.markdown(
                f"<div style='background:#f0fdf4;border-left:3px solid #22c55e;"
                f"padding:6px 12px;border-radius:5px;margin:3px 0;font-size:0.82rem'>"
                f"{tur_l} <b>{e.ders}</b> — {e.konu or '–'} "
                f"<span style='color:#94a3b8;font-size:0.73rem'>({e.tarih})</span></div>",
                unsafe_allow_html=True,
            )


# ── Tab 4: Sınav & Sağlık & Rehberlik ────────────────────────────────────────

def _tab_sinav_saglik(student: Student, data: dict):
    grades       = data["grades"]
    exam_results = data["exam_results"]
    telafi       = data["telafi"]
    revir        = data["revir_ziyaretleri"]
    vakalar      = data["rehberlik_vakalar"]
    gorusmeler   = data["rehberlik_gorusmeler"]

    # — Yazılı notlar —
    _section("Okul Yazılı ve Performans Notları", "#2563eb")
    yazili = [g for g in grades if g.not_turu in ("yazili", "performans", "proje")]
    if yazili:
        for g in sorted(yazili, key=lambda x: (x.ders, x.not_sirasi)):
            renk = "#22c55e" if g.puan >= 70 else "#f59e0b" if g.puan >= 50 else "#ef4444"
            TUR_L = {"yazili": "Yazılı", "performans": "Performans", "proje": "Proje",
                     "sozlu": "Sözlü", "ders_ici": "Ders İçi"}
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;align-items:center;"
                f"background:#111827;border-left:4px solid {renk};"
                f"padding:8px 14px;border-radius:6px;margin:3px 0;font-size:0.84rem'>"
                f"<span><b>{g.ders}</b> — {g.donem}, {TUR_L.get(g.not_turu, g.not_turu)} #{g.not_sirasi}</span>"
                f"<span style='color:{renk};font-size:1.1rem;font-weight:800'>{g.puan}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        _info("Yazılı/performans notu bulunmuyor.", "info")

    # — ÖD sınav sonuçları —
    _section("Ölçme & Değerlendirme Sınav Sonuçları", "#7c3aed")
    if exam_results:
        for r in sorted(exam_results, key=lambda x: x.graded_at or "", reverse=True)[:15]:
            puan = round(r.score or 0, 1)
            net  = round(r.net_score or 0, 1)
            renk = "#22c55e" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
            with st.expander(f"📝 {(r.graded_at or '')[:10]} — Puan: **{puan}** | Net: {net}", expanded=False
            ):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Doğru", r.correct_count or 0)
                c2.metric("Yanlış", r.wrong_count or 0)
                c3.metric("Boş", r.empty_count or 0)
                c4.metric("Puan", puan)
                ob = r.outcome_breakdown or {}
                if ob:
                    rows = []
                    for oid, v in ob.items():
                        total = v.get("total", 1)
                        correct = v.get("correct", 0)
                        rows.append({"Kazanım": oid[:40], "Doğru": correct,
                                     "Toplam": total, "Başarı %": round(correct/total*100, 1) if total else 0})
                    if rows:
                        st.dataframe(pd.DataFrame(rows).sort_values("Başarı %"),
                                     use_container_width=True, hide_index=True)
    else:
        _info("ÖD sınav kaydı bulunamadı.", "info")

    # — Telafi görevleri —
    _section("Telafi Görevleri", "#ef4444")
    RENK_MAP = {
        "RED":    ("#fef2f2", "#ef4444", "🔴"),
        "YELLOW": ("#fffbeb", "#f59e0b", "🟡"),
        "GREEN":  ("#f0fdf4", "#22c55e", "🟢"),
        "BLUE":   ("#eff6ff", "#3b82f6", "🔵"),
    }
    if telafi:
        for t in telafi[:20]:
            bg_t, fg_t, ic_t = RENK_MAP.get(getattr(t, "color_band", "RED"), ("#fef2f2", "#ef4444", "🔴"))
            durum_t = getattr(t, "status", "atandi")
            durum_ic = "✅" if durum_t == "tamamlandi" else "⏳"
            st.markdown(
                f"<div style='background:{bg_t};border-left:4px solid {fg_t};"
                f"padding:7px 14px;border-radius:6px;margin:3px 0;font-size:0.83rem'>"
                f"{ic_t} <b>{getattr(t,'outcome_text','') or 'Telafi Görevi'}</b> "
                f"— {getattr(t,'assignment_type','')} "
                f"<span style='color:{fg_t}'>{durum_ic} {durum_t}</span></div>",
                unsafe_allow_html=True,
            )
    else:
        _info("Telafi görevi kaydı bulunmuyor.", "success")

    # — Revir ziyaretleri —
    _section(f"Revir Ziyaretleri — {len(revir)} kayıt", "#ef4444")
    if revir:
        for z in sorted(revir, key=lambda x: getattr(x, "basvuru_tarihi", "") or "", reverse=True)[:10]:
            tarih    = getattr(z, "basvuru_tarihi", "") or "–"
            sikayet  = getattr(z, "sikayet", "–") or "–"
            kat      = getattr(z, "sikayet_kategorisi", "–") or "–"
            mudahale = getattr(z, "mudahale", "–") or "–"
            takip    = getattr(z, "takip_gerekiyor", False)
            sonuc    = getattr(z, "sonuc", "–") or "–"
            renk     = "#ef4444" if takip else "#22c55e"
            st.markdown(
                f"<div style='background:#fff;border-left:4px solid {renk};"
                f"border:1px solid #e2e8f0;border-left-width:4px;"
                f"padding:8px 14px;border-radius:7px;margin:4px 0;font-size:0.83rem'>"
                f"<b>{tarih}</b> — {sikayet} [{kat}] | Müdahale: {mudahale} | "
                f"{'⚠️ Takip Gerekiyor' if takip else '✅ Kapandı'} | {sonuc}"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        _info("Revir ziyaret kaydı bulunmuyor.", "info")

    # — Rehberlik vakaları —
    _section(f"Rehberlik Vakaları — {len(vakalar)} kayıt", "#8b5cf6")
    if vakalar:
        for v in vakalar[:10]:
            durum    = getattr(v, "durum", "ACIK") or "ACIK"
            oncelik  = getattr(v, "oncelik", "NORMAL") or "NORMAL"
            risk_sev = getattr(v, "risk_seviyesi", "DUSUK") or "DUSUK"
            baslik   = getattr(v, "vaka_basligi", "–") or "–"
            konular  = ", ".join(getattr(v, "ilgili_konular", []) or []) or "–"
            d_renk   = {"ACIK": "#ef4444", "TAKIPTE": "#f59e0b",
                        "BEKLEMEDE": "#94a3b8", "KAPANDI": "#22c55e"}.get(durum, "#64748b")
            st.markdown(
                f"<div style='background:#faf5ff;border-left:4px solid {d_renk};"
                f"padding:8px 14px;border-radius:7px;margin:4px 0;font-size:0.83rem'>"
                f"<b>{baslik}</b> — Durum: <span style='color:{d_renk}'>{durum}</span> | "
                f"Öncelik: {oncelik} | Risk: {risk_sev} | Konular: {konular}"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        _info("Rehberlik vaka kaydı bulunmuyor.", "info")

    # — Rehberlik görüşmeleri —
    if gorusmeler:
        _section(f"PDR Görüşme Geçmişi — {len(gorusmeler)} görüşme", "#8b5cf6")
        for g in sorted(gorusmeler,
                        key=lambda x: getattr(x, "gorusme_tarihi", "") or "", reverse=True)[:8]:
            tarih  = getattr(g, "gorusme_tarihi", "–") or "–"
            konu   = getattr(g, "konu", "–") or "–"
            sonuc  = getattr(g, "sonuc", "–") or "–"
            rehber = getattr(g, "rehber_adi", "–") or "–"
            st.markdown(
                f"<div style='background:#ede9fe;border-left:3px solid #8b5cf6;"
                f"padding:7px 12px;border-radius:5px;margin:3px 0;font-size:0.82rem'>"
                f"<b>{tarih}</b> — {konu} | Rehber: {rehber} | Sonuç: {sonuc}"
                f"</div>",
                unsafe_allow_html=True,
            )


# ── Tab 5: AI Analizi ─────────────────────────────────────────────────────────

def _tab_ai_analizi(student: Student, data: dict, risk: dict):
    _section("🤖 AI Akademik & Gelişim Analizi", "#94A3B8")
    _info(
        "Yapay zeka <b>10 farklı veri kaynağını</b> (notlar, devamsızlık, KYT, ödevler, "
        "sınavlar, kazanım borçları, telafi görevleri, revir, rehberlik vakaları, etüt) "
        "birleştirerek kişiselleştirilmiş analiz ve eylem planı üretir.",
        "info",
    )

    cache_key = f"dft_ai_{student.id}_{risk['score']}"
    if cache_key in st.session_state:
        st.markdown(st.session_state[cache_key])
        if st.button("🔄 Yeniden Analiz Et", key="dft_ai_yenile"):
            del st.session_state[cache_key]
            st.rerun()
        return

    if st.button("🤖 AI Analizi Başlat", type="primary", key="dft_ai_basla",
                 use_container_width=True):
        with st.spinner("10 veri kaynağı analiz ediliyor, kişiselleştirilmiş değerlendirme hazırlanıyor..."):
            analiz = _run_ai_analysis(student, data, risk)
        st.session_state[cache_key] = analiz
        st.markdown(analiz)
        st.rerun()


def _run_ai_analysis(student: Student, data: dict, risk: dict) -> str:
    """GPT-4o-mini ile 10 veri kaynağını kapsayan kapsamlı öğrenci analizi."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return (
            "⚠️ **AI analizi kullanılamıyor.** OpenAI API anahtarı yapılandırılmamış.\n\n"
            "Ayarlar > API Yapılandırması bölümünden OPENAI_API_KEY giriniz."
        )

    dev_ozet = data["dev_ozet"]

    # Not ortalamaları ders bazlı
    ders_nots: dict[str, list] = defaultdict(list)
    for g in data["grades"]:
        if g.puan and g.puan > 0:
            ders_nots[g.ders].append(g.puan)
    ders_ozet = "\n".join(
        f"  • {d}: ort. {round(sum(v)/len(v),1)} ({len(v)} kayıt)"
        for d, v in sorted(ders_nots.items(), key=lambda x: sum(x[1])/len(x[1]))
    ) or "  (kayıt yok)"

    # Ödev durumu
    odev_bekleme = [o for o in data["odevler"]
                    if o.id not in data["teslim_ids"]]
    odev_gecikti = [t for t in data["teslimler"] if t.durum == "gecikti"]

    # Borçlar
    borc_ozet = "\n".join(
        f"  • {b.ders}: {b.kazanim_metni or b.kazanim_kodu} "
        f"({BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni)})"
        for b in data["aktif_borc"][:8]
    ) or "  (aktif borç yok)"

    # Sınav ortalamaları
    sinav_puan = [r.score for r in data["exam_results"] if r.score and r.score > 0]
    sinav_ort  = round(sum(sinav_puan)/len(sinav_puan), 1) if sinav_puan else 0

    # KYT
    kyt = data["kyt_analiz"]
    kyt_str = (f"Toplam {kyt.get('toplam',0)} soru, %{kyt.get('basari_yuzde',0)} başarı"
               if kyt.get("toplam", 0) > 0 else "Veri yok")

    # Telafi
    telafi_bekl = [t for t in data["telafi"] if getattr(t, "status", "") != "tamamlandi"]
    red_telafi  = [t for t in telafi_bekl if getattr(t, "color_band", "") == "RED"]

    # Revir
    revir        = data["revir_ziyaretleri"]
    takip_revir  = [z for z in revir if getattr(z, "takip_gerekiyor", False)]
    revir_kat    = list({(getattr(z, "sikayet_kategorisi", "") or "Diğer") for z in revir})[:5]

    # Rehberlik
    vakalar     = data["rehberlik_vakalar"]
    acik_vaka   = [v for v in vakalar if getattr(v, "durum", "") in ("ACIK", "TAKIPTE")]
    yuksek_vaka = [v for v in vakalar if getattr(v, "oncelik", "") in ("ACIL", "YUKSEK")]
    vaka_konular = list({konu for v in vakalar for konu in (getattr(v, "ilgili_konular", []) or [])})[:5]

    # Etüt
    etut_cnt = len(data["etut_kayitlari"])

    prompt = f"""Sen deneyimli bir Türk eğitim danışmanısın. Aşağıdaki öğrencinin 10 farklı akademik ve gelişimsel veri kaynağını analiz ederek kapsamlı bir değerlendirme yaz.

ÖĞRENCİ: {student.tam_ad} | {student.sinif}. Sınıf / {student.sube} Şubesi
AKADEMİK RİSK SKORU: {risk["score"]}/100 (0=mükemmel, 100=kritik)

━━━ DERS NOTLARI ━━━
{ders_ozet}

━━━ DEVAMSIZLIK ━━━
Toplam: {dev_ozet.get("toplam", 0)} gün | Özürlü: {dev_ozet.get("ozurlu", 0)} | Özürsüz: {dev_ozet.get("ozursuz", 0)}

━━━ ÖDEV DURUMU ━━━
Teslim Oranı: %{data["teslim_oran"]} | Teslim Edilmeyen: {len(odev_bekleme)} | Geç Teslim: {len(odev_gecikti)}

━━━ KAZANIM BORÇLARI ━━━
Aktif Borç: {len(data["aktif_borc"])} kazanım
{borc_ozet}

━━━ SINAV PERFORMANSI ━━━
ÖD Sınav Ortalaması: {sinav_ort} | Sınav Sayısı: {len(sinav_puan)}
Okul Yazılı Ortalaması: {risk["not_ort"]}

━━━ KYT (GÜNLÜK KAZANIM TESTİ) ━━━
{kyt_str}

━━━ TELAFİ GÖREVLERİ ━━━
Bekleyen: {len(telafi_bekl)} | RED (kritik): {len(red_telafi)} | Tamamlanan: {len(data["telafi"]) - len(telafi_bekl)}

━━━ REVİR ZİYARETLERİ ━━━
Toplam: {len(revir)} ziyaret | Takip Gerektiren: {len(takip_revir)}
Yaygın Şikayet Kategorileri: {", ".join(revir_kat) or "–"}

━━━ REHBERLİK VAKALARI ━━━
Toplam Vaka: {len(vakalar)} | Açık: {len(acik_vaka)} | Yüksek Öncelikli: {len(yuksek_vaka)}
Konu Alanları: {", ".join(vaka_konular) or "–"}
Görüşme Geçmişi: {len(data["rehberlik_gorusmeler"])} görüşme

━━━ ETÜT / DESTEK ━━━
Etüt Katılımı: {etut_cnt} kayıt {"(olumlu gösterge)" if etut_cnt > 0 else "(etüt katılımı yok)"}

━━━ ANALİZ TALEP EDİLEN BAŞLIKLAR ━━━

Lütfen şu başlıkları içeren kapsamlı bir Türkçe analiz yaz:

## 📊 Bütünsel Akademik Değerlendirme
(Tüm veri kaynaklarını sentezleyerek genel durumu 3-4 cümleyle özetle)

## ✅ Güçlü Yönler ve Olumlu Göstergeler
(Madde madde, somut veriye dayalı)

## ⚠️ Risk Alanları ve Endişe Verici Göstergeler
(Madde madde, akademik + sağlık + rehberlik boyutlarını kapsayan)

## 🎯 Öncelikli Eylem Planı — Bu Hafta İçin 5 Adım
(Uygulanabilir, somut, ölçülebilir)

## 👨‍👩‍👧 Veli İçin Tavsiyeler
(Evde yapılabilecekler, iletişim önerileri, dikkat edilmesi gerekenler)

## 🏫 Okul İçin Öneriler
(Öğretmen, rehber öğretmen ve idare için öncelikli aksiyonlar)

## 📅 Bu Dönem Hedefleri
(3 ölçülebilir hedef — not, devam, gelişim boyutlarında)
"""

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen deneyimli bir Türk eğitim danışmanısın. "
                        "Öğrenci verilerini bütünsel bir perspektifle analiz edersin: "
                        "akademik başarı, devam durumu, psikolojik gelişim ve sağlık verileri. "
                        "Markdown formatında, samimi, yapıcı ve uygulanabilir tavsiyeler üretirsin."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2500,
            temperature=0.7,
        )
        return resp.choices[0].message.content or "AI yanıt üretemedi."
    except Exception as e:
        return f"⚠️ AI analizi sırasında hata oluştu: {e}"


# ── PDF Export ────────────────────────────────────────────────────────────────

def _parse_ai_for_pdf(ai_text: str) -> list[tuple[str, str]]:
    """Markdown AI metnini (başlık, gövde) çiftlerine böler."""
    import re
    sections = []
    current_header = ""
    current_body_lines = []

    for line in ai_text.splitlines():
        if line.startswith("## "):
            if current_header or current_body_lines:
                body = "\n".join(current_body_lines).strip()
                sections.append((current_header, body))
            # Markdown temizle: ##, **, *, ─ karakterleri
            current_header = re.sub(r"[*_`#─━]", "", line).strip()
            current_body_lines = []
        else:
            # Satır içi markdown temizle
            clean = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            clean = re.sub(r"\*(.*?)\*", r"\1", clean)
            clean = re.sub(r"`(.*?)`", r"\1", clean)
            clean = re.sub(r"^[─━]+$", "", clean)
            current_body_lines.append(clean)

    if current_header or current_body_lines:
        body = "\n".join(current_body_lines).strip()
        sections.append((current_header, body))

    return sections


def _generate_defter_pdf(student: Student, data: dict, risk: dict,
                          ai_analiz: str = "") -> bytes:
    """Öğrenci Defteri verilerinden ReportPDFGenerator ile PDF oluşturur."""
    try:
        from utils.report_utils import ReportPDFGenerator, get_institution_info
        kurum = get_institution_info()
        today = datetime.date.today().strftime("%d.%m.%Y")

        pdf = ReportPDFGenerator(
            title=f"Öğrenci Defteri — {student.tam_ad}",
            subtitle=f"{student.sinif}. Sinif / {student.sube} Subesi | {today}",
            orientation="portrait",
        )

        # Kapak başlığı
        pdf.add_header(
            kurum_adi=kurum.get("name", "SmartCampusAI"),
            logo_path=kurum.get("logo_path", ""),
        )

        # ── Akademik Risk Özeti ──
        ikon, renk, etiket, _, _ = _risk_level(risk["score"])
        pdf.add_section("Akademik Risk Ozeti", color="#94A3B8")
        dev_ozet   = data["dev_ozet"]
        aktif_borc = len(data["aktif_borc"])
        pdf.add_metrics([
            ("Risk Skoru",    f"{risk['score']}/100 — {etiket}",  renk),
            ("Not Ortalamasi", str(risk["not_ort"]),
             "#22c55e" if risk["not_ort"] >= 70 else "#f59e0b" if risk["not_ort"] >= 50 else "#ef4444"),
            ("Devamsizlik",   f"{dev_ozet.get('toplam', 0)} gun ({dev_ozet.get('ozursuz', 0)} ozursuz)",
             "#ef4444" if dev_ozet.get("toplam", 0) > 10 else "#22c55e"),
            ("Odev Teslim",   f"%{data['teslim_oran']}",
             "#22c55e" if data["teslim_oran"] >= 80 else "#f59e0b" if data["teslim_oran"] >= 60 else "#ef4444"),
            ("Kazanim Borcu", f"{aktif_borc} aktif kazanim",
             "#22c55e" if aktif_borc == 0 else "#f59e0b" if aktif_borc <= 3 else "#ef4444"),
            ("Sinav Ort.",    str(risk["sinav_ort"]),
             "#22c55e" if risk["sinav_ort"] >= 70 else "#f59e0b" if risk["sinav_ort"] >= 50 else "#ef4444"),
        ])
        pdf.add_spacer(0.3)

        # ── Risk bileşenleri tablosu ──
        pdf.add_section("Risk Bileseni Detayi (10 Kaynak)", color="#64748b")
        bd = risk["breakdown"]
        risk_rows = []
        for v in bd.values():
            r = v["risk"]
            if r < 0:
                durum = "Koruyucu"
            elif r == 0:
                durum = "Iyi"
            elif r <= 5:
                durum = "Hafif"
            elif r <= 10:
                durum = "Dikkat"
            else:
                durum = "Kritik"
            risk_rows.append({
                "Bileseni":  v["etiket"],
                "Deger":     v["deger"],
                "Risk Puan": str(r),
                "Durum":     durum,
            })
        if risk_rows:
            pdf.add_table(pd.DataFrame(risk_rows), header_color="#64748b")
        pdf.add_spacer(0.3)

        # ── Ders bazlı not ortalamaları ──
        grades = data["grades"]
        if grades:
            pdf.add_section("Ders Bazli Not Ortalamalari", color="#2563eb")
            ders_nots: dict[str, list] = defaultdict(list)
            for g in grades:
                if g.puan and g.puan > 0:
                    ders_nots[g.ders].append(g.puan)
            if ders_nots:
                not_rows = [
                    {"Ders": d, "Ortalama": f"{round(sum(v)/len(v), 1)}", "Not Sayisi": str(len(v))}
                    for d, v in sorted(ders_nots.items(), key=lambda x: -sum(x[1])/len(x[1]))
                ]
                pdf.add_table(pd.DataFrame(not_rows), header_color="#2563eb")
            pdf.add_spacer(0.3)

        # ── Yazılı notlar detayı ──
        yazili = [g for g in grades if g.not_turu in ("yazili", "performans", "proje")]
        if yazili:
            pdf.add_section("Yazili ve Performans Notlari", color="#2563eb")
            TUR_L = {"yazili": "Yazili", "performans": "Performans", "proje": "Proje",
                     "sozlu": "Sozlu", "ders_ici": "Ders Ici"}
            yazili_rows = [
                {
                    "Ders":   g.ders,
                    "Donem":  g.donem,
                    "Tur":    TUR_L.get(g.not_turu, g.not_turu),
                    "No":     str(g.not_sirasi),
                    "Puan":   str(g.puan),
                }
                for g in sorted(yazili, key=lambda x: (x.ders, x.not_sirasi))
            ]
            pdf.add_table(pd.DataFrame(yazili_rows), header_color="#2563eb")
            pdf.add_spacer(0.3)

        # ── Devamsızlık özeti ──
        attendance = data["attendance"]
        if attendance:
            pdf.add_section("Devamsizlik Kayitlari", color="#ef4444")
            dev_ozet_data = data["dev_ozet"]
            pdf.add_metrics([
                ("Toplam",    f"{dev_ozet_data.get('toplam', 0)} gun",   "#ef4444"),
                ("Ozurlu",    f"{dev_ozet_data.get('ozurlu', 0)} gun",   "#f59e0b"),
                ("Ozursuz",   f"{dev_ozet_data.get('ozursuz', 0)} gun",  "#ef4444"),
            ])
            pdf.add_spacer(0.3)

        # ── Kazanım borçları ──
        aktif_borc_list = data["aktif_borc"]
        if aktif_borc_list:
            pdf.add_section(f"Aktif Kazanim Borclari ({len(aktif_borc_list)})", color="#7c3aed")
            borc_rows = [
                {
                    "Ders":    b.ders,
                    "Kazanim": (b.kazanim_metni or b.kazanim_kodu or "")[:50],
                    "Neden":   BORC_NEDENI_LABELS.get(b.borc_nedeni, b.borc_nedeni),
                    "Tarih":   b.kazanim_isleme_tarihi or "",
                }
                for b in aktif_borc_list[:20]
            ]
            pdf.add_table(pd.DataFrame(borc_rows), header_color="#7c3aed")
            pdf.add_spacer(0.3)

        # ── Ödev teslim durumu ──
        odevler  = data["odevler"]
        teslimler = data["teslimler"]
        if odevler:
            pdf.add_section(f"Odev Teslim Durumu ({len(odevler)} odev)", color="#f59e0b")
            teslim_map = {t.odev_id: t for t in teslimler}
            DURUM_L = {
                "teslim_edildi": "Teslim", "gecikti": "Gec Teslim",
                "teslim_edilmedi": "Teslim Edilmedi", "bekliyor": "Bekliyor", "muaf": "Muaf",
            }
            odev_rows = [
                {
                    "Ders":    o.ders,
                    "Baslik":  (o.baslik or "")[:40],
                    "Son Teslim": o.son_teslim_tarihi or "–",
                    "Durum":   DURUM_L.get(
                        (teslim_map.get(o.id).durum if teslim_map.get(o.id) else "bekliyor"),
                        "Bekliyor"
                    ),
                }
                for o in sorted(odevler, key=lambda x: x.son_teslim_tarihi or "", reverse=True)[:20]
            ]
            pdf.add_table(pd.DataFrame(odev_rows), header_color="#f59e0b")
            pdf.add_spacer(0.3)

        # ── Telafi görevleri ──
        telafi = data["telafi"]
        if telafi:
            pdf.add_section("Telafi Gorevleri", color="#ef4444")
            RENK_M = {"RED": "Kritik", "YELLOW": "Orta", "GREEN": "Iyi", "BLUE": "Ileri"}
            tel_rows = [
                {
                    "Gorev":  (getattr(t, "outcome_text", "") or "Telafi")[:45],
                    "Bant":   RENK_M.get(getattr(t, "color_band", "RED"), "–"),
                    "Tur":    getattr(t, "assignment_type", "–"),
                    "Durum":  getattr(t, "status", "atandi"),
                }
                for t in telafi[:15]
            ]
            pdf.add_table(pd.DataFrame(tel_rows), header_color="#ef4444")
            pdf.add_spacer(0.3)

        # ── Sınav sonuçları ──
        exam_results = data["exam_results"]
        if exam_results:
            pdf.add_section("OD Sinav Sonuclari", color="#7c3aed")
            sinav_rows = [
                {
                    "Tarih": (r.graded_at or "")[:10],
                    "Puan":  str(round(r.score or 0, 1)),
                    "Net":   str(round(r.net_score or 0, 1)),
                    "Dogru": str(r.correct_count or 0),
                    "Yanlis": str(r.wrong_count or 0),
                    "Bos":   str(r.empty_count or 0),
                }
                for r in sorted(exam_results, key=lambda x: x.graded_at or "", reverse=True)[:15]
            ]
            pdf.add_table(pd.DataFrame(sinav_rows), header_color="#7c3aed")
            pdf.add_spacer(0.3)

        # ── Revir ziyaretleri ──
        revir = data["revir_ziyaretleri"]
        if revir:
            pdf.add_section(f"Revir Ziyaretleri ({len(revir)})", color="#ef4444")
            rev_rows = [
                {
                    "Tarih":   getattr(z, "basvuru_tarihi", "–") or "–",
                    "Sikayet": (getattr(z, "sikayet", "–") or "–")[:35],
                    "Kategori": getattr(z, "sikayet_kategorisi", "–") or "–",
                    "Takip":   "Evet" if getattr(z, "takip_gerekiyor", False) else "Hayir",
                }
                for z in revir[:10]
            ]
            pdf.add_table(pd.DataFrame(rev_rows), header_color="#ef4444")
            pdf.add_spacer(0.3)

        # ── Rehberlik ──
        vakalar = data["rehberlik_vakalar"]
        if vakalar:
            pdf.add_section(f"Rehberlik Vakalari ({len(vakalar)})", color="#8b5cf6")
            vak_rows = [
                {
                    "Baslik":  (getattr(v, "vaka_basligi", "–") or "–")[:40],
                    "Durum":   getattr(v, "durum", "–") or "–",
                    "Oncelik": getattr(v, "oncelik", "–") or "–",
                    "Risk":    getattr(v, "risk_seviyesi", "–") or "–",
                }
                for v in vakalar[:10]
            ]
            pdf.add_table(pd.DataFrame(vak_rows), header_color="#8b5cf6")
            pdf.add_spacer(0.3)

        # ── AI Analizi ──
        if ai_analiz and not ai_analiz.startswith("⚠️"):
            pdf.add_section("AI Akademik & Gelisim Analizi", color="#94A3B8")
            pdf.add_text(
                "Bu bolum yapay zeka tarafindan 10 farkli veri kaynagi "
                "analiz edilerek olusturulmustur. Bilgilendirme amaclidir."
            )
            pdf.add_spacer(0.2)
            parsed = _parse_ai_for_pdf(ai_analiz)
            for header, body in parsed:
                if header:
                    pdf.add_section(header, color="#2563eb")
                if body:
                    # Uzun satırları böl — her paragraf ayrı add_text
                    for para in body.split("\n\n"):
                        para = para.strip()
                        if para:
                            pdf.add_text(para)
                            pdf.add_spacer(0.15)

        return pdf.generate()

    except Exception as e:
        # Hata durumunda boş bytes dön (buton disabled olmayacak)
        import traceback
        return b""


# ── Ana giriş noktaları ────────────────────────────────────────────────────────

def render_ogrenci_defteri_tab(
    store: AkademikDataStore,
    od: OlcmeDataStore,
    student: Student,
    rol: str = "veli",
    akademik_yil: str = "",
):
    """Öğrenci Defteri — veli, öğrenci ve admin için ortak görünüm."""
    inject_common_css("odf")
    if student is None:
        st.warning("Öğrenci bilgisi bulunamadı.")
        return

    # Kurum bilgisi
    try:
        from utils.shared_data import load_kurum_profili
        _kurum = load_kurum_profili()
        _kurum_adi = _kurum.get("kurum_adi", "Smart Campus") if _kurum else "Smart Campus"
    except Exception:
        _kurum_adi = "Smart Campus"

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#0c2461 0%,#1e3a8a 30%,#2563eb 60%,#3b82f6 100%);"
        f"color:#fff;padding:22px 26px;border-radius:16px;margin-bottom:18px;"
        f"position:relative;overflow:hidden;"
        f"box-shadow:0 4px 20px rgba(37,99,235,0.25)'>"
        f"<div style='position:absolute;top:-25px;right:-25px;width:110px;height:110px;"
        f"background:rgba(255,255,255,0.05);border-radius:50%'></div>"
        f"<div style='position:absolute;bottom:-15px;left:-15px;width:70px;height:70px;"
        f"background:rgba(255,255,255,0.03);border-radius:50%'></div>"
        f"<div style='font-size:0.68rem;letter-spacing:2px;text-transform:uppercase;"
        f"opacity:0.6;margin-bottom:3px'>{_kurum_adi}</div>"
        f"<div style='font-size:1.3rem;font-weight:800;letter-spacing:0.3px'>📓 Öğrenci Defteri</div>"
        f"<div style='font-size:0.85rem;opacity:.85;margin-top:6px'>"
        f"{student.tam_ad} · {student.sinif}/{student.sube}</div>"
        f"<div style='font-size:0.75rem;opacity:0.6;margin-top:4px;border-top:1px solid rgba(255,255,255,0.15);"
        f"padding-top:6px'>Not, devamsızlık, KYT, ödev, sınav, kazanım, revir ve rehberlik — "
        f"10 veri kaynağının bütünsel analizi</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.spinner("10 veri kaynağı yükleniyor..."):
        data = _collect_data(store, od, student, akademik_yil)
        risk = _calc_risk(data)

    # PDF indirme butonu (başlığın hemen altında, sağ tarafta)
    pdf_col, _ = st.columns([1, 4])
    with pdf_col:
        today_str = datetime.date.today().strftime("%Y%m%d")
        safe_ad = (student.tam_ad or "ogrenci").replace(" ", "_")
        # Önbelleklenmiş AI analizini al (varsa)
        cache_key = f"dft_ai_{student.id}_{risk['score']}"
        ai_analiz_text = st.session_state.get(cache_key, "")
        pdf_bytes = _generate_defter_pdf(student, data, risk, ai_analiz=ai_analiz_text)
        btn_label = "📥 PDF İndir (AI dahil)" if ai_analiz_text else "📥 PDF İndir"
        if pdf_bytes:
            st.download_button(
                label=btn_label,
                data=pdf_bytes,
                file_name=f"ogrenci_defteri_{safe_ad}_{today_str}.pdf",
                mime="application/pdf",
                key=f"dft_pdf_{student.id}",
                use_container_width=True,
            )

    tab_ozet, tab_grafik, tab_kazanim, tab_sinav, tab_ai = st.tabs([
        "  📊 Genel Özet  ",
        "  📈 Grafikler  ",
        "  🎯 Kazanım & Ödev  ",
        "  📝 Sınav, Sağlık & Rehberlik  ",
        "  🤖 AI Analizi  ",
    ])

    with tab_ozet:
        _tab_genel_ozet(student, data, risk)
    with tab_grafik:
        _tab_grafikler(student, data, risk)
    with tab_kazanim:
        _tab_kazanim_odev(student, data)
    with tab_sinav:
        _tab_sinav_saglik(student, data)
    with tab_ai:
        _tab_ai_analizi(student, data, risk)


def render_ogrenci_defteri_admin(selected_egitim_yili: str = ""):
    """Admin modülü için Öğrenci Defteri — filtreli görünüm."""
    store = get_akademik_store()
    od    = OlcmeDataStore()

    st.markdown(
        "<div style='background:#1A2035;border-radius:10px;padding:12px 18px;"
        "margin-bottom:14px;font-size:0.88rem'>"
        "<b>🔍 Öğrenci Seçimi</b> — Sınıf ve şubeyi seçin, ardından öğrenciyi belirleyin.</div>",
        unsafe_allow_html=True,
    )
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sinif_sec = st.selectbox("Sınıf", list(range(1, 13)), index=4, key="dft_adm_sinif")
    with fc2:
        sube_sec = st.selectbox("Şube", ["A", "B", "C", "D", "E", "F"], key="dft_adm_sube")
    with fc3:
        students = store.get_students(sinif=sinif_sec, sube=sube_sec)
        if not students:
            st.info("Bu sınıf/şubede öğrenci kaydı bulunamadı.")
            return
        ogrenci_sec = st.selectbox(
            "Öğrenci",
            options=[s.id for s in students],
            format_func=lambda sid: next(
                (f"{s.tam_ad} (No:{s.numara})" for s in students if s.id == sid), sid
            ),
            key="dft_adm_ogrenci",
        )

    student = next((s for s in students if s.id == ogrenci_sec), None)
    if not student:
        st.warning("Öğrenci seçilmedi.")
        return

    render_ogrenci_defteri_tab(store, od, student, rol="admin",
                               akademik_yil=selected_egitim_yili)
