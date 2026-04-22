"""
Bütüncül Risk Paneli — UI Katmanı
==================================
20-boyutlu (10 akademik + 10 davranışsal) risk görünümü.

Özellikler:
  - 20 boyutlu radar (2 yarımküre)
  - Yetki-kilitli boyutlar (hassas olanlar rol bazlı gizli)
  - Müdahale protokolü motoru (otomatik üretim)
  - Açıklanabilir AI (her skor için neden + güven aralığı)
  - Yanlış pozitif geri bildirim formu
  - KVKK denetim log görünümü (yetkili kullanıcılar)
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from models.davranissal_risk import (
    BehavioralRiskEngine,
    InterventionProtocolEngine,
    DavranissalRiskStore,
    PermissionGuard,
    AuditLog,
    FalsePositiveFeedback,
    FalsePositiveFeedbackStore,
    BEHAVIORAL_DIMENSIONS,
    BEHAVIORAL_WEIGHTS,
    BEHAVIORAL_RISK_LEVELS,
    behavioral_risk_level,
)

# Akademik boyutlar icin (mevcut erken_uyari modeline referans)
try:
    from models.erken_uyari import (
        RISK_WEIGHTS as AKADEMIK_WEIGHTS,
        risk_level_for as akademik_risk_level_for,
    )
except Exception:
    AKADEMIK_WEIGHTS = {}
    akademik_risk_level_for = lambda s: {"label": "?", "color": "#999", "icon": "⬜"}

# Akademik boyutlarin insan okunur etiketleri
AKADEMIK_LABELS = {
    "grade": "Not Ortalaması",
    "attendance": "Devamsızlık",
    "exam": "Sınav",
    "homework": "Ödev",
    "outcome_debt": "Kazanım Borçları",
    "counseling": "Rehberlik",
    "health": "Sağlık",
    "trend": "Trend (Momentum)",
    "behavior": "Davranış Genel",
    "foreign_lang": "Yabancı Dil",
}


# ═══════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════

_CSS = """<style>
.btn-card {background: linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);
    border-radius: 14px; padding: 20px 24px; margin: 12px 0;
    border: 1px solid rgba(99,102,241,.2);}
.btn-card h3 {margin:0 0 6px 0; color:#e0e7ff; font-size:1.1rem;}
.btn-card .sub {color:#a5b4fc; font-size:.85rem; margin-bottom:10px;}
.btn-hemikuzey {background: linear-gradient(135deg,#0f172a,#134e4a);
    border-radius:12px; padding:16px; border:1px solid rgba(20,184,166,.3);}
.btn-hemikuzey .title {color:#5eead4; font-size:.85rem; font-weight:700; text-transform:uppercase;}
.btn-hemikuzey .score {color:#2dd4bf; font-size:2rem; font-weight:800; margin:6px 0;}
.btn-hemicenup {background: linear-gradient(135deg,#0f172a,#7f1d1d);
    border-radius:12px; padding:16px; border:1px solid rgba(239,68,68,.4);}
.btn-hemicenup .title {color:#fca5a5; font-size:.85rem; font-weight:700; text-transform:uppercase;}
.btn-hemicenup .score {color:#ef4444; font-size:2rem; font-weight:800; margin:6px 0;}
.btn-birlesik {background: linear-gradient(135deg,#3b0764,#1e1b4b);
    border-radius:12px; padding:18px; border:2px solid #8b5cf6;}
.btn-birlesik .title {color:#c4b5fd; font-size:.88rem; font-weight:700; text-transform:uppercase;}
.btn-birlesik .score {color:#a78bfa; font-size:2.5rem; font-weight:800; margin:8px 0;}
.btn-protokol {background: rgba(239,68,68,.08); border-left:4px solid #ef4444;
    border-radius:8px; padding:14px 18px; margin:10px 0;}
.btn-protokol.urgency-acil_24h {border-left-color:#ef4444; background:rgba(239,68,68,.12);}
.btn-protokol.urgency-72h {border-left-color:#f97316; background:rgba(249,115,22,.08);}
.btn-protokol.urgency-hafta {border-left-color:#eab308; background:rgba(234,179,8,.08);}
.btn-protokol h4 {margin:0 0 6px 0; color:#fca5a5;}
.btn-protokol .desc {color:#cbd5e1; font-size:.88rem; line-height:1.5;}
.btn-step {background:rgba(99,102,241,.06); border-radius:6px;
    padding:10px 14px; margin:6px 0; border-left:3px solid #6366f1;}
.btn-step .order {color:#818cf8; font-weight:700; font-size:.8rem;}
.btn-step .action {color:#e2e8f0; font-size:.9rem; margin:4px 0;}
.btn-step .meta {color:#94a3b8; font-size:.75rem;}
.btn-kilit {background: rgba(148,163,184,.1); border:1px dashed #64748b;
    border-radius:8px; padding:14px; color:#94a3b8; text-align:center;
    font-style:italic;}
.btn-reason {background: rgba(34,197,94,.05); border-left:3px solid #22c55e;
    border-radius:6px; padding:8px 12px; margin:6px 0; font-size:.82rem; color:#86efac;}
.btn-confidence {display:inline-block; padding:2px 8px; border-radius:6px;
    font-size:.75rem; font-weight:600; margin-left:8px;}
.btn-confidence.high {background:rgba(34,197,94,.15); color:#22c55e;}
.btn-confidence.med {background:rgba(234,179,8,.15); color:#eab308;}
.btn-confidence.low {background:rgba(239,68,68,.15); color:#ef4444;}
.btn-legal {background: rgba(251,191,36,.08); border:1px solid #eab308;
    border-radius:8px; padding:12px; margin:10px 0; color:#fde68a; font-size:.82rem;}
.btn-legal b {color:#fbbf24;}
.btn-audit-row {background: rgba(30,41,59,.5); border-radius:6px;
    padding:8px 12px; margin:3px 0; display:flex; gap:12px; font-size:.78rem;}
.btn-audit-row .time {color:#64748b; min-width:140px;}
.btn-audit-row .user {color:#a78bfa; min-width:100px;}
.btn-audit-row .action {color:#34d399; min-width:80px;}
.btn-audit-row .target {color:#94a3b8;}
</style>"""


# ═══════════════════════════════════════════════════════════════════════
# 20 BOYUTLU RADAR CIZIMI
# ═══════════════════════════════════════════════════════════════════════

def render_20_boyutlu_radar(akademik_scores: dict, davranissal_scores: dict,
                            visible_dimensions: list[str] = None):
    """
    20 boyutlu radar grafigi — 2 yarimkure (akademik sol, davranissal sag).
    visible_dimensions: yetki kilidinden dolayi gizlenecek boyutlar filtrelenir.
    """
    if visible_dimensions is None:
        visible_dimensions = list(BEHAVIORAL_DIMENSIONS.keys())

    # Akademik (sol yarım)
    ak_labels = [AKADEMIK_LABELS.get(k, k) for k in AKADEMIK_WEIGHTS.keys()]
    ak_values = [akademik_scores.get(k, 0) for k in AKADEMIK_WEIGHTS.keys()]

    # Davranissal (sag yarim) — sadece gorulebilir olanlar
    dvr_labels = []
    dvr_values = []
    for k, info in BEHAVIORAL_DIMENSIONS.items():
        if k in visible_dimensions:
            dvr_labels.append(f"{info['icon']} {info['label']}")
            dvr_values.append(davranissal_scores.get(k, 0))
        else:
            dvr_labels.append(f"🔒 (Kilitli)")
            dvr_values.append(0)

    # Birleştir
    all_labels = ak_labels + dvr_labels
    all_values = ak_values + dvr_values
    # Kapalı radar icin ilk elemani sona ekle
    all_labels_closed = all_labels + [all_labels[0]]
    all_values_closed = all_values + [all_values[0]]

    fig = go.Figure()

    # Akademik (mavi-yesil)
    fig.add_trace(go.Scatterpolar(
        r=ak_values + [ak_values[0]],
        theta=ak_labels + [ak_labels[0]],
        fill="toself",
        fillcolor="rgba(34, 197, 94, 0.15)",
        line=dict(color="#22c55e", width=2),
        name="Akademik Risk",
    ))

    # Davranissal (kirmizi-turuncu)
    fig.add_trace(go.Scatterpolar(
        r=dvr_values + [dvr_values[0]],
        theta=dvr_labels + [dvr_labels[0]],
        fill="toself",
        fillcolor="rgba(239, 68, 68, 0.15)",
        line=dict(color="#ef4444", width=2),
        name="Davranışsal Risk",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#94a3b8")),
            angularaxis=dict(tickfont=dict(color="#e2e8f0", size=10)),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5,
                   font=dict(color="#e2e8f0")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=550,
        margin=dict(t=30, b=60, l=60, r=60),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════
# BOYUT KARTLARI (Davranissal 10 boyut — açıklanabilirlik ile)
# ═══════════════════════════════════════════════════════════════════════

def render_dimension_card(dim_key: str, score: float, reason: str,
                         confidence: float, role: str, student_id: str):
    """Tek bir davranissal boyut karti — gerekce + guven + kilit kontrollu."""
    info = BEHAVIORAL_DIMENSIONS[dim_key]
    can_see = PermissionGuard.can_see_dimension(dim_key, role)

    if not can_see:
        st.markdown(f"""
        <div class="btn-kilit">
            🔒 <b>{info['icon']} {info['label']}</b><br>
            Bu boyut rolunuz icin gizlidir.
        </div>
        """, unsafe_allow_html=True)
        return

    # Log: hassas boyut goruntulendi
    if info.get("yetki_kilit", False):
        AuditLog.log(
            action="gor", target_type="davranissal_boyut",
            target_id=student_id, target_dimension=dim_key,
            notes=f"Skor={score:.0f} Confidence={confidence:.0f}",
        )

    # Guven kategorisi
    if confidence >= 80:
        conf_cls = "high"
    elif confidence >= 60:
        conf_cls = "med"
    else:
        conf_cls = "low"

    # Severity color
    severity_colors = {
        "dusuk": "#22c55e", "orta": "#eab308",
        "yuksek": "#f97316", "kritik": "#ef4444",
    }
    sev_color = severity_colors.get(info.get("ciddiyet", "orta"), "#eab308")

    st.markdown(f"""
    <div class="btn-card" style="border-left:4px solid {sev_color};">
        <h3>{info['icon']} {info['label']}
            <span style="float:right; font-weight:800; color:{sev_color};">{score:.0f}/100</span>
        </h3>
        <div class="sub">
            {info['aciklama']}
            <span class="btn-confidence {conf_cls}">Güven: %{confidence:.0f}</span>
        </div>
        <div class="btn-reason">
            <b>🔍 Neden:</b> {reason}
        </div>
        <div style="font-size:.72rem; color:#64748b; margin-top:6px;">
            Kaynak: {info['kaynak']} | Ciddiyet: {info.get('ciddiyet','orta').upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# MÜDAHALE PROTOKOL GORUNUMU
# ═══════════════════════════════════════════════════════════════════════

def render_protocol(protocol: dict, store: DavranissalRiskStore):
    """Tek bir mudahale protokolunu goster — onay/iptal/tamamla seçenekli."""
    urgency = protocol.get("urgency", "normal")
    urgency_labels = {
        "acil_24h": "⚠️ ACİL 24 SAAT",
        "72h": "📍 72 Saat İçinde",
        "hafta": "📅 Bu Hafta",
        "izleme": "👁️ İzleme",
    }
    urgency_label = urgency_labels.get(urgency, urgency.upper())

    status = protocol.get("status", "onerildi")
    status_labels = {
        "onerildi": "🔷 Önerildi",
        "onaylandi": "✅ Onaylandı",
        "uygulanyor": "⏳ Uygulanıyor",
        "tamamlandi": "✔️ Tamamlandı",
        "iptal": "❌ İptal",
    }

    st.markdown(f"""
    <div class="btn-protokol urgency-{urgency}">
        <h4>{protocol.get('title','')}
            <span style="float:right; font-size:.75rem;">{urgency_label}</span>
        </h4>
        <div class="desc">{protocol.get('description','')}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption(f"Durum: {status_labels.get(status, status)}")
    with col2:
        required = ", ".join(protocol.get("required_roles", []))
        st.caption(f"👥 Rol: {required[:40]}")
    with col3:
        ext = ", ".join(protocol.get("external_parties", [])) or "-"
        st.caption(f"🏥 Dış: {ext[:30]}")

    # Yasal zorunluluk
    if protocol.get("legal_notification_required", False):
        st.markdown(f"""
        <div class="btn-legal">
            <b>⚖️ YASAL BİLDİRİM ZORUNLU:</b><br>
            {protocol.get('legal_notes','5395 SK / ilgili mevzuat')}
        </div>
        """, unsafe_allow_html=True)

    # Adım adım plan
    with st.expander(f"📋 Adımlar ({len(protocol.get('steps', []))} adet)", expanded=False):
        for step in protocol.get("steps", []):
            dead_h = step.get("deadline_hours", 168)
            dead_label = f"{dead_h}h" if dead_h < 24 else f"{dead_h//24}gün"
            st.markdown(f"""
            <div class="btn-step">
                <div class="order">ADIM {step.get('order')}</div>
                <div class="action">{step.get('action','')}</div>
                <div class="meta">Sorumlu: {step.get('responsible','?')} | Son tarih: {dead_label} | Durum: {step.get('status','bekliyor')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Aksiyon butonlari (sadece yetkili)
    role = PermissionGuard.get_user_role()
    if role in ("superadmin", "yonetici", "calisan", "mudur", "mudur_yardimcisi", "psikolog", "rehber"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if status == "onerildi":
                if st.button("✅ Onayla", key=f"app_{protocol.get('id')}"):
                    protocol["status"] = "onaylandi"
                    protocol["approved_at"] = datetime.now().isoformat()
                    # Kaydet
                    import dataclasses
                    from models.davranissal_risk import InterventionProtocol
                    # Dict'ten dataclass olustur (approx)
                    st.success("Protokol onaylandi.")
                    AuditLog.log("onayla", "protokol", protocol.get("id", ""))
        with c2:
            if status in ("onaylandi", "onerildi"):
                if st.button("⏳ Başlat", key=f"start_{protocol.get('id')}"):
                    protocol["status"] = "uygulanyor"
                    AuditLog.log("basla", "protokol", protocol.get("id", ""))
                    st.info("Uygulama basladi.")
        with c3:
            if status == "uygulanyor":
                if st.button("✔️ Tamamla", key=f"comp_{protocol.get('id')}"):
                    protocol["status"] = "tamamlandi"
                    protocol["completed_at"] = datetime.now().isoformat()
                    AuditLog.log("tamamla", "protokol", protocol.get("id", ""))
                    st.success("Tamamlandi.")
        with c4:
            if status not in ("tamamlandi", "iptal"):
                if st.button("❌ İptal", key=f"iptal_{protocol.get('id')}"):
                    protocol["status"] = "iptal"
                    AuditLog.log("iptal", "protokol", protocol.get("id", ""))
                    st.warning("İptal edildi.")


# ═══════════════════════════════════════════════════════════════════════
# YANLIS POZITIF GERI BILDIRIM FORMU
# ═══════════════════════════════════════════════════════════════════════

def render_false_positive_form(risk_record: dict):
    """Rehber 'bu skor yanlis' diyebilir — model ogrenir."""
    st.markdown("### 🎯 Yanlış Pozitif Geri Bildirim")
    st.caption(
        "AI modelinin herhangi bir boyutta yanliş skor ürettiğini düşünüyorsanız "
        "aşağıdaki formu doldurun. Model bu geri bildirimlerle kalibre edilir."
    )

    # Sadece belirli roller
    role = PermissionGuard.get_user_role()
    if role not in ("superadmin", "yonetici", "calisan", "mudur", "rehber", "psikolog", "mudur_yardimcisi"):
        st.info("Geri bildirim için yetkiniz yok.")
        return

    # Boyut sec
    visible = PermissionGuard.filter_dimensions()
    if not visible:
        return
    dim_options = {f"{BEHAVIORAL_DIMENSIONS[k]['icon']} {BEHAVIORAL_DIMENSIONS[k]['label']}": k
                   for k in visible}

    with st.form(f"fp_form_{risk_record.get('id','')}"):
        dim_label = st.selectbox("Yanlış skor hangi boyutta?", list(dim_options.keys()))
        dim_key = dim_options[dim_label]

        reported = risk_record.get(dim_key, 0)
        st.caption(f"AI'nin verdiği skor: **{reported:.0f}/100**")
        correct = st.slider("Sizce doğru skor nedir?", 0, 100,
                          value=int(max(0, reported - 30)))
        reason = st.text_area(
            "Neden yanlıştı? (Kısa açıklama)",
            placeholder="Örn: 'Disiplin olayı gösteriyor ama aslında tatbikatta rol oyunuydu.'",
            height=80,
        )

        submit = st.form_submit_button("📤 Geri Bildirim Gönder", type="primary")
        if submit:
            if not reason.strip():
                st.error("Neden alani zorunludur.")
                return
            feedback = FalsePositiveFeedback(
                risk_record_id=risk_record.get("id", ""),
                student_id=risk_record.get("student_id", ""),
                dimension=dim_key,
                reported_score=reported,
                correct_score=correct,
                reporter_role=role,
                reason=reason.strip(),
            )
            FalsePositiveFeedbackStore.add(feedback)
            AuditLog.log("geri_bildirim", "risk_record",
                        risk_record.get("id", ""), target_dimension=dim_key,
                        notes=f"Reported={reported:.0f} Correct={correct}")
            st.success("✅ Geri bildirim kaydedildi. Model bir sonraki çalışmada kalibre edilecek.")


# ═══════════════════════════════════════════════════════════════════════
# DENETIM LOGU GORUNUMU (KVKK zorunluluğu)
# ═══════════════════════════════════════════════════════════════════════

def render_audit_log():
    """Son 30 gunun KVKK denetim log kayitlari."""
    role = PermissionGuard.get_user_role()
    if role not in ("superadmin", "yonetici", "mudur", "mudur_yardimcisi", "psikolog"):
        st.warning("🔒 Denetim logu yalnızca yönetici, müdür veya psikolog tarafından görülebilir.")
        return

    st.markdown("### 📜 KVKK Denetim Logu — Son 30 Gün")
    st.caption(
        "Hassas davranışsal risk verilerinin erişim kayıtları. "
        "KVKK md. 12 gereği 2 yıl saklanır."
    )

    entries = AuditLog.load_recent(days=30)
    if not entries:
        st.info("Son 30 günde kayıt yok.")
        return

    # Filtre
    c1, c2, c3 = st.columns(3)
    with c1:
        action_filter = st.selectbox(
            "Eylem", ["Hepsi"] + list(set(e.get("action", "") for e in entries)),
            key="audit_action")
    with c2:
        role_filter = st.selectbox(
            "Rol", ["Hepsi"] + list(set(e.get("user_role", "") for e in entries)),
            key="audit_role")
    with c3:
        limit = st.number_input("Göster", 10, 500, 100, key="audit_limit")

    filtered = entries
    if action_filter != "Hepsi":
        filtered = [e for e in filtered if e.get("action") == action_filter]
    if role_filter != "Hepsi":
        filtered = [e for e in filtered if e.get("user_role") == role_filter]
    filtered = sorted(filtered, key=lambda e: e.get("timestamp", ""), reverse=True)[:limit]

    st.caption(f"Toplam {len(filtered)} kayıt")
    for e in filtered:
        time_str = e.get("timestamp", "")[:19].replace("T", " ")
        st.markdown(f"""
        <div class="btn-audit-row">
            <span class="time">{time_str}</span>
            <span class="user">{e.get('user_role','?')} / {e.get('user_id','?')[:10]}</span>
            <span class="action">{e.get('action','?')}</span>
            <span class="target">{e.get('target_type','?')} · {e.get('target_id','?')[:12]} · {e.get('target_dimension','') or '-'}</span>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# FALSE POSITIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════

def render_fp_summary():
    """Model kalibrasyonu icin yanlis pozitif ozeti."""
    st.markdown("### 📊 Model Kalibrasyon Raporu")
    st.caption(
        "Hangi boyutlarda AI yanlış skor uretmeye meyilli? "
        "Sık yanlış raporlanan boyutlar model kalibrasyonunda düşürülür."
    )

    summary = FalsePositiveFeedbackStore.summary_by_dimension()
    if not summary:
        st.info("Henüz geri bildirim yok — model yeni başlıyor.")
        return

    df = pd.DataFrame([
        {
            "Boyut": BEHAVIORAL_DIMENSIONS.get(k, {}).get("label", k),
            "İkon": BEHAVIORAL_DIMENSIONS.get(k, {}).get("icon", "⬜"),
            "Yanlış Rapor": v,
        }
        for k, v in summary.items()
    ]).sort_values("Yanlış Rapor", ascending=False)

    # Grafik
    fig = go.Figure(go.Bar(
        x=df["Yanlış Rapor"],
        y=df["İkon"] + " " + df["Boyut"],
        orientation="h",
        marker=dict(color="#ef4444"),
    ))
    fig.update_layout(
        height=400, margin=dict(l=10, r=10, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Yanlış Rapor Sayısı", gridcolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b"),
        font=dict(color="#e2e8f0"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════
# ANA PANEL
# ═══════════════════════════════════════════════════════════════════════

def render_butuncul_panel(store=None, loader=None):
    """Bütüncül Risk Paneli — ana giriş noktası.

    Args:
        store: Mevcut ErkenUyariStore (akademik risk kayıtları için)
        loader: CrossModuleLoader
    """
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown("## 🛡️ Bütüncül Risk Paneli — 20 Boyut")
    st.caption(
        "**Etik çerçeve:** 'Suç riski' değil 'davranışsal risk göstergesi'. "
        "AI sadece UYARI verir — KARAR her zaman insanindir. "
        "Hassas boyutlar yetki-kilitlidir (KVKK md. 6, 5395 SK)."
    )

    role = PermissionGuard.get_user_role()
    st.caption(f"🔑 Mevcut rol: **{role.upper()}**")

    dvr_store = DavranissalRiskStore()

    # ── TÜM BÖLÜMLER TEK SAYFADA — EXPANDER AKIŞI ───────────────
    # Varsayilan: Kategori Bazli Otomatik Liste acik, digerleri kapali.
    # Kullanici istedigi bolumu acip kapatabilir.

    # 1. Kategori Bazli Otomatik Liste (ANA GORUNUM — acik baslar)
    with st.expander("📊 KATEGORİ BAZLI OTOMATİK LİSTE  —  Akademik + Davranışsal Segment",
                     expanded=True):
        _tab_category_segments(store, loader, dvr_store, role)

    # 2. Ogrenci Analizi (ikinci sirada, default kapali)
    with st.expander("🎯 ÖĞRENCİ ANALİZİ  —  Tek öğrenci 20 boyutlu radar + protokol",
                     expanded=False):
        _tab_student_analysis(store, loader, dvr_store, role)

    # 3. Mudahale Protokolleri
    with st.expander("📋 MÜDAHALE PROTOKOLLERİ  —  Aktif protokoller, onay ve takip",
                     expanded=False):
        _tab_protocols(dvr_store, role)

    # 4. Risk Listesi (tablo)
    with st.expander("🔥 RİSK LİSTESİ  —  Tüm öğrenciler tablo + kritik uyarı",
                     expanded=False):
        _tab_risk_list(store, dvr_store, role)

    # 5. Model Kalibrasyon
    with st.expander("📊 MODEL KALİBRASYON  —  Yanlış pozitif geri bildirim özeti",
                     expanded=False):
        render_fp_summary()

    # 6. Denetim Logu
    with st.expander("📜 KVKK DENETİM LOGU  —  Son 30 gün hassas veri erişim kayıtları",
                     expanded=False):
        render_audit_log()

    # 7. Batch Hesapla
    with st.expander("⚙️ TOPLU HESAPLAMA  —  Tüm öğrenciler için davranışsal risk üret",
                     expanded=False):
        _tab_batch_calculate(store, loader, dvr_store, role)


def _tab_student_analysis(store, loader, dvr_store, role):
    """Ogrenci sec -> 20 boyutlu radar + 10 davranissal kart + protokoller."""
    # Öğrenci listesi yükle
    try:
        students = loader.load_students() if loader else []
    except Exception:
        students = []

    if not students:
        st.warning("Öğrenci verisi yüklenemedi. 'Hesapla (Batch)' sekmesinden veri üret.")
        return

    # Veli/ogrenci icin sadece kendini/kendi cocugunu goruntule
    if role in ("veli", "ogrenci"):
        try:
            own_id = st.session_state.get("student_id", "")
            children = st.session_state.get("children_ids", [])
            allowed = [own_id] + children
            students = [s for s in students if s.get("id") in allowed]
        except Exception:
            students = []
        if not students:
            st.info("Gösterilecek öğrenci yok.")
            return

    # Ogrenci sec
    opt_map = {f"{s.get('ad_soyad', s.get('ad', ''))} ({s.get('sinif','')}{s.get('sube','')})": s
               for s in students}
    sel_label = st.selectbox("👤 Öğrenci seçin", list(opt_map.keys()), key="btn_std")
    if not sel_label:
        return
    student = opt_map[sel_label]
    student_id = student.get("id", "")

    if not PermissionGuard.can_see_student(student_id, role):
        st.error("🔒 Bu öğrenciyi görme yetkiniz yok.")
        return

    # Davranissal risk hesapla
    engine = BehavioralRiskEngine()
    # Akademik skoru mevcut storedan alamaya calis
    akademik_score = 0.0
    akademik_boyutlar = {}
    try:
        if store:
            # Varsayılan — en son RiskRecord'u bul
            all_records = []
            try:
                all_records = store.load_risk_records() if hasattr(store, "load_risk_records") else []
            except Exception:
                pass
            for r in all_records:
                if r.get("student_id") == student_id:
                    akademik_score = r.get("risk_score", 0)
                    for k in AKADEMIK_WEIGHTS.keys():
                        akademik_boyutlar[k] = r.get(f"{k}_risk", 0)
                    break
    except Exception:
        pass

    # Davranissal hesaplama
    dvr_record = engine.calculate(
        student_id=student_id,
        student_name=student.get("ad_soyad", student.get("ad", "")),
        akademik_skor=akademik_score,
        sinif=int(student.get("sinif", 0) or 0),
        sube=student.get("sube", ""),
    )
    dvr_store.save_record(dvr_record)

    # Log
    AuditLog.log("gor", "risk_record", dvr_record.id,
                notes=f"Student={student_id}")

    # Ust ozet — 3 kutu
    col1, col2, col3 = st.columns(3)
    with col1:
        ak_level = akademik_risk_level_for(akademik_score)
        st.markdown(f"""
        <div class="btn-hemikuzey">
            <div class="title">🎓 AKADEMIK RISK</div>
            <div class="score">{akademik_score:.0f}<small style="font-size:.6em;">/100</small></div>
            <div style="color:#94a3b8;">{ak_level['icon']} {ak_level['label']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        dvr_level = behavioral_risk_level(dvr_record.behavioral_risk_score)
        st.markdown(f"""
        <div class="btn-hemicenup">
            <div class="title">🧠 DAVRANIŞSAL RISK</div>
            <div class="score">{dvr_record.behavioral_risk_score:.0f}<small style="font-size:.6em;">/100</small></div>
            <div style="color:#94a3b8;">{dvr_level['icon']} {dvr_level['label']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Birlesik skor (ortalama)
        combined = (akademik_score + dvr_record.behavioral_risk_score) / 2
        if combined >= 75:
            comb_label = "🔴 Kritik Birleşik Risk"
        elif combined >= 55:
            comb_label = "🟠 Yüksek"
        elif combined >= 30:
            comb_label = "🟡 Orta"
        else:
            comb_label = "🟢 Düşük"
        st.markdown(f"""
        <div class="btn-birlesik">
            <div class="title">🌐 BİRLEŞİK SKOR</div>
            <div class="score">{combined:.0f}<small style="font-size:.6em;">/100</small></div>
            <div style="color:#c4b5fd;">{comb_label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 20 boyutlu radar
    st.markdown("### 📡 20 Boyutlu Risk Radarı")
    visible_dims = PermissionGuard.filter_dimensions(role)

    davranissal_scores_dict = {
        k: getattr(dvr_record, k, 0) for k in BEHAVIORAL_DIMENSIONS.keys()
    }
    render_20_boyutlu_radar(akademik_boyutlar, davranissal_scores_dict, visible_dims)

    # Davranissal boyut kartlari
    st.markdown("### 🧠 Davranışsal Boyut Detayları")
    for dim_key in BEHAVIORAL_DIMENSIONS.keys():
        score = getattr(dvr_record, dim_key, 0)
        reason = dvr_record.dimension_reasons.get(dim_key, "")
        confidence = dvr_record.confidence.get(dim_key, 50)
        render_dimension_card(dim_key, score, reason, confidence, role, student_id)

    # Protokoller (otomatik uret)
    st.markdown("---")
    st.markdown("### 📋 Önerilen Müdahale Protokolleri")
    proto_engine = InterventionProtocolEngine()
    protocols = proto_engine.generate(dvr_record)

    if not protocols:
        st.success("✅ Bu öğrenci için herhangi bir müdahale protokolü tetiklenmedi.")
    else:
        st.info(f"{len(protocols)} protokol öneri olarak üretildi. Onay ve uygulama insan yetkilinin kararındadır.")
        for proto in protocols:
            # Kaydet
            dvr_store.save_protocol(proto)
            import dataclasses
            render_protocol(dataclasses.asdict(proto), dvr_store)

    # False positive feedback formu
    if role in ("superadmin", "yonetici", "calisan", "mudur", "rehber",
                "psikolog", "mudur_yardimcisi"):
        st.markdown("---")
        import dataclasses
        render_false_positive_form(dataclasses.asdict(dvr_record))


def _tab_category_segments(store, loader, dvr_store, role):
    """Kategori Bazli Otomatik Risk Gruplari.

    Her kategori icin:
      - Toplam riskli ogrenci sayisi
      - En riskli 10 ogrenci listesi
      - Tek tikla toplu protokol baslatma
      - Kategori bazli trend
    """
    if role not in ("superadmin", "yonetici", "calisan", "mudur", "mudur_yardimcisi", "psikolog", "rehber"):
        st.warning("🔒 Yalnızca yetkili roller kategori bazlı riski görebilir.")
        return

    st.markdown("## 📊 Kategori Bazlı Otomatik Riskli Öğrenciler")
    st.caption(
        "Sistem her davranışsal boyut için öğrencileri otomatik gruplar. "
        "Kategorinin sağındaki **Toplu Protokol Başlat** butonu ile listedeki tüm öğrenciler için aynı anda müdahale akışı başlatılır."
    )

    records = dvr_store.load_records()
    if not records:
        st.info("⚠️ Hesaplanmış kayıt yok. Once '⚙️ Hesapla (Batch)' sekmesinden tum ogrenciler icin hesaplama yap.")
        return

    # En son hesaplamalar (unique student_id)
    latest = {}
    for r in records:
        sid = r.get("student_id", "")
        if sid not in latest or r.get("calculated_at", "") > latest[sid].get("calculated_at", ""):
            latest[sid] = r
    all_records = list(latest.values())

    # Kategori gruplari — her davranissal boyut + akademik ayri
    # Esik degerleri: 45+ WATCH, 60+ HIGH, 70+ CRITICAL
    CATEGORIES = [
        {
            "key": "akademik",
            "icon": "🎓",
            "label": "Akademik Risk",
            "description": "Notlar, devamsızlık, ödev, kazanım borçları",
            "field": None,  # Akademik skor (baska kaynak)
            "protocol_type": "akademik_kritik",
            "threshold": 55,
            "color": "#22c55e",
            "yetki_kilit": False,
        },
        {
            "key": "zorbalik_pattern",
            "icon": "⚠️",
            "label": "Zorbalık / Akran İlişkileri",
            "description": "Fail veya mağdur rolünde zorbalık kayıtları",
            "field": "zorbalik_pattern",
            "protocol_type": "zorbalik_kronik",
            "threshold": 45,
            "color": "#f97316",
            "yetki_kilit": True,
        },
        {
            "key": "duygusal_kizilbayrak",
            "icon": "💔",
            "label": "Duygusal Sorunlar",
            "description": "Negatif mood, depresyon/anksiyete belirtileri",
            "field": "duygusal_kizilbayrak",
            "protocol_type": "duygusal_yuksek",
            "threshold": 45,
            "color": "#a855f7",
            "yetki_kilit": True,
        },
        {
            "key": "kendine_zarar_intihar",
            "icon": "🚨",
            "label": "Kendine Zarar / İntihar Riski",
            "description": "ACİL — rehberlik risk + revir şüpheli + ihbar",
            "field": "kendine_zarar_intihar",
            "protocol_type": "intihar_acil",
            "threshold": 40,  # daha düşük eşik (hassas)
            "color": "#dc2626",
            "yetki_kilit": True,
        },
        {
            "key": "madde_kullanim_supheli",
            "icon": "🚬",
            "label": "Madde Kullanım Şüphesi",
            "description": "Rehberlik + revir + ihbar sinyalleri",
            "field": "madde_kullanim_supheli",
            "protocol_type": "madde_supheli",
            "threshold": 45,
            "color": "#ef4444",
            "yetki_kilit": True,
        },
        {
            "key": "disiplin_sikligi",
            "icon": "📋",
            "label": "Disiplin / Davranış Olayları",
            "description": "Son 90 günde disiplin olayı sıklığı",
            "field": "disiplin_sikligi",
            "protocol_type": None,  # protokol otomatik değil
            "threshold": 40,
            "color": "#f59e0b",
            "yetki_kilit": False,
        },
        {
            "key": "kronik_devamsizlik",
            "icon": "📅",
            "label": "Kronik Devamsızlık",
            "description": "Seçici ders kaçma ve kronik devamsızlık",
            "field": "kronik_devamsizlik",
            "protocol_type": "devamsizlik_kronik",
            "threshold": 45,
            "color": "#0ea5e9",
            "yetki_kilit": False,
        },
        {
            "key": "sosyal_izolasyon",
            "icon": "🫂",
            "label": "Sosyal İzolasyon",
            "description": "Kulüp üyeliği yok, etkinlik katılımı yok",
            "field": "sosyal_izolasyon",
            "protocol_type": None,
            "threshold": 50,
            "color": "#64748b",
            "yetki_kilit": False,
        },
        {
            "key": "aile_risk",
            "icon": "🏠",
            "label": "Aile Risk Faktörleri",
            "description": "Şiddet, bölünme, kayıp, ekonomik kriz",
            "field": "aile_risk",
            "protocol_type": "aile_yuksek",
            "threshold": 45,
            "color": "#be185d",
            "yetki_kilit": True,
        },
        {
            "key": "sosyoekonomik_stres",
            "icon": "💰",
            "label": "Sosyo-Ekonomik Stres",
            "description": "Bursluluk değişimi, ödeme gecikme, veli sessiz",
            "field": "sosyoekonomik_stres",
            "protocol_type": None,
            "threshold": 40,
            "color": "#14b8a6",
            "yetki_kilit": True,
        },
    ]

    # Üst özet metrikler
    toplam_risk = sum(1 for r in all_records
                     if r.get("behavioral_risk_score", 0) >= 45)
    kritik_risk = sum(1 for r in all_records
                     if r.get("behavioral_risk_score", 0) >= 70)
    acil_kategori = sum(1 for r in all_records
                       if r.get("kendine_zarar_intihar", 0) >= 40
                       or r.get("madde_kullanim_supheli", 0) >= 45)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Hesaplanan", len(all_records))
    with c2:
        st.metric("🟠 Risk Altında", toplam_risk)
    with c3:
        st.metric("🔴 Kritik Düzey", kritik_risk)
    with c4:
        st.metric("🆘 Acil Kategori", acil_kategori, help="İntihar / madde kategorisinde en az 1 öğrenci")

    st.markdown("---")

    # Her kategori icin genisleyebilir bolum
    for cat in CATEGORIES:
        # Yetki kilit kontrol
        if cat["yetki_kilit"] and not PermissionGuard.can_see_dimension(cat["key"], role):
            # Yetki yoksa kategoriyi tamamen gizle
            continue

        # Bu kategoride riskli ogrencileri bul
        threshold = cat["threshold"]
        if cat["key"] == "akademik":
            # Akademik skor mevcut erken uyari systeminden geliyor — simdilik
            # davranissal store'dan alamayiz. Ileride Loader'dan cekilir.
            # Gecici: mevcut RiskRecord'lardan (varsa) al
            try:
                ak_records = []
                if store and hasattr(store, "load_risk_records"):
                    ak_records = store.load_risk_records()
                elif store and hasattr(store, "get_latest_risks"):
                    ak_records = store.get_latest_risks()
                if ak_records:
                    riskli = [r for r in ak_records if r.get("risk_score", 0) >= threshold]
                    riskli.sort(key=lambda r: r.get("risk_score", 0), reverse=True)
                else:
                    riskli = []
            except Exception:
                riskli = []
        else:
            riskli = [r for r in all_records if r.get(cat["field"], 0) >= threshold]
            riskli.sort(key=lambda r: r.get(cat["field"], 0), reverse=True)

        # Kategori karti
        seviye_sayilari = _count_by_level(riskli, cat["field"] or "risk_score", threshold)
        ust_satir = st.columns([3, 1, 1, 1, 1])
        with ust_satir[0]:
            st.markdown(
                f"### {cat['icon']} {cat['label']} "
                f"<span style='color:{cat['color']}; font-size:0.75em; font-weight:600;'>"
                f"({len(riskli)} öğrenci)</span>",
                unsafe_allow_html=True,
            )
            st.caption(cat["description"])
        with ust_satir[1]:
            st.metric("🟡 İzlenen", seviye_sayilari.get("watch", 0))
        with ust_satir[2]:
            st.metric("🟠 Yüksek", seviye_sayilari.get("high", 0))
        with ust_satir[3]:
            st.metric("🔴 Kritik", seviye_sayilari.get("critical", 0))
        with ust_satir[4]:
            st.metric("🆘 ACİL", seviye_sayilari.get("emergency", 0))

        # Ogrenci listesi
        if not riskli:
            st.success(f"✅ Bu kategoride risk altında öğrenci yok.")
            st.markdown("---")
            continue

        # Top 10 goster, tamami expander'da
        with st.expander(f"👁️ Tüm {len(riskli)} öğrenciyi gör", expanded=len(riskli) <= 10):
            # Tablo
            display_records = riskli[:50]
            field = cat["field"] or "risk_score"
            table_data = []
            for r in display_records:
                skor = r.get(field, 0)
                if skor >= 90:
                    seviye = "🆘 ACİL"
                elif skor >= 70:
                    seviye = "🔴 Kritik"
                elif skor >= 55:
                    seviye = "🟠 Yüksek"
                elif skor >= 45:
                    seviye = "🟡 İzlenen"
                else:
                    seviye = "🟢 Normal"
                table_data.append({
                    "Ad Soyad": r.get("student_name", ""),
                    "Sınıf/Şube": f"{r.get('sinif','')}{r.get('sube','')}",
                    f"Skor ({cat['label']})": round(skor, 0),
                    "Seviye": seviye,
                    "Birleşik Risk": round(r.get("behavioral_risk_score", 0), 0),
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True,
                        hide_index=True, height=min(400, 60 + len(display_records) * 35))

        # Top 3 kartlari (kritik olanlar) - hizli gorunum
        kritik_top3 = [r for r in riskli if r.get(cat["field"] or "risk_score", 0) >= 70][:3]
        if kritik_top3:
            st.markdown(f"**🚨 Bu Kategoride En Kritik 3 Öğrenci:**")
            cols = st.columns(3)
            for i, r in enumerate(kritik_top3):
                with cols[i]:
                    skor = r.get(cat["field"] or "risk_score", 0)
                    st.markdown(f"""
                    <div style="background:rgba(239,68,68,.08); border-left:3px solid {cat['color']};
                                border-radius:6px; padding:10px; min-height:80px;">
                        <div style="color:#cbd5e1; font-weight:700;">{r.get('student_name','')}</div>
                        <div style="color:#94a3b8; font-size:.8rem;">
                            {r.get('sinif','')}{r.get('sube','')} · Skor {skor:.0f}
                        </div>
                        <div style="color:{cat['color']}; font-weight:600; font-size:.85rem;">
                            {r.get('dimension_reasons',{}).get(cat['field']or'', '')[:60]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Toplu protokol butonu
        if cat["protocol_type"] and len(riskli) > 0:
            col_btn1, col_btn2 = st.columns([2, 1])
            with col_btn1:
                st.caption(
                    f"⚡ **{len(riskli)} öğrenci** için tek tıkla '{cat['protocol_type']}' protokolü başlatabilirsin. "
                    "Her öğrenci için ayrı protokol kaydı oluşur, onay insan yetkilidir."
                )
            with col_btn2:
                if st.button(f"🚀 Toplu Protokol Başlat ({len(riskli)})",
                           key=f"bulk_proto_{cat['key']}",
                           type="primary", use_container_width=True):
                    _trigger_bulk_protocols(riskli, cat, dvr_store)

        st.markdown("---")


def _count_by_level(records: list, field: str, threshold: float) -> dict:
    """Bir kategorideki ogrencileri seviyelere gore say."""
    counts = {"watch": 0, "high": 0, "critical": 0, "emergency": 0}
    for r in records:
        s = r.get(field, 0)
        if s >= 90:
            counts["emergency"] += 1
        elif s >= 70:
            counts["critical"] += 1
        elif s >= 55:
            counts["high"] += 1
        elif s >= threshold:
            counts["watch"] += 1
    return counts


def _trigger_bulk_protocols(records: list, category: dict, dvr_store):
    """Bir kategorideki tum ogrenciler icin toplu protokol tetikler."""
    from models.davranissal_risk import (
        InterventionProtocolEngine, InterventionProtocol, BehavioralRiskRecord
    )
    engine = InterventionProtocolEngine()
    tpl = engine.TEMPLATES.get(category["protocol_type"])
    if not tpl:
        st.error(f"Protokol şablonu bulunamadı: {category['protocol_type']}")
        return

    count = 0
    for r in records:
        proto = InterventionProtocol(
            student_id=r.get("student_id", ""),
            risk_record_id=r.get("id", ""),
            protocol_type=category["protocol_type"],
            urgency=tpl["urgency"],
            title=tpl["title"],
            description=tpl["description"],
            required_roles=list(tpl["required_roles"]),
            external_parties=list(tpl.get("external_parties", [])),
            steps=[dict(s, status="bekliyor") for s in tpl["steps"]],
            legal_notification_required=tpl["legal_notification_required"],
            legal_notes=tpl.get("legal_notes", ""),
        )
        dvr_store.save_protocol(proto)
        AuditLog.log(
            action="toplu_protokol",
            target_type="protokol",
            target_id=proto.id,
            target_dimension=category["key"],
            notes=f"Toplu baslatildi student={r.get('student_id')}",
        )
        count += 1

    st.success(
        f"✅ {count} öğrenci için '{tpl['title']}' protokolü oluşturuldu. "
        "Müdahale Protokolleri sekmesinden incele ve onayla."
    )


def _tab_protocols(dvr_store, role):
    """Tüm aktif mudahale protokolleri."""
    if role not in ("superadmin", "yonetici", "ogretmen", "calisan",
                    "mudur", "mudur_yardimcisi", "psikolog", "rehber", "sinif_ogretmeni"):
        st.warning("🔒 Bu bölüm yalnızca yetkili roller tarafından görülebilir.")
        return

    protocols = dvr_store.load_protocols()
    if not protocols:
        st.info("Aktif protokol yok. 'Öğrenci Analizi' sekmesinden bir öğrenci için protokol üretebilirsin.")
        return

    # Filtre
    c1, c2, c3 = st.columns(3)
    with c1:
        urgency_f = st.selectbox("Aciliyet",
            ["Hepsi", "acil_24h", "72h", "hafta", "izleme"], key="proto_urg")
    with c2:
        status_f = st.selectbox("Durum",
            ["Hepsi", "onerildi", "onaylandi", "uygulanyor", "tamamlandi", "iptal"],
            key="proto_stat")
    with c3:
        type_f = st.selectbox("Tür",
            ["Hepsi"] + list(set(p.get("protocol_type", "") for p in protocols)),
            key="proto_type")

    filtered = protocols
    if urgency_f != "Hepsi":
        filtered = [p for p in filtered if p.get("urgency") == urgency_f]
    if status_f != "Hepsi":
        filtered = [p for p in filtered if p.get("status") == status_f]
    if type_f != "Hepsi":
        filtered = [p for p in filtered if p.get("protocol_type") == type_f]

    # Siralama — aciliyete gore
    urgency_order = {"acil_24h": 0, "72h": 1, "hafta": 2, "izleme": 3, "normal": 4}
    filtered.sort(key=lambda p: urgency_order.get(p.get("urgency"), 5))

    st.caption(f"Toplam {len(filtered)} protokol")
    for proto in filtered:
        render_protocol(proto, dvr_store)


def _tab_risk_list(store, dvr_store, role):
    """Tum ogrencilerin davranissal risk siralamasi."""
    if role not in ("superadmin", "yonetici", "calisan", "mudur", "mudur_yardimcisi", "psikolog", "rehber"):
        st.warning("🔒 Yalnızca yetkili roller görebilir.")
        return

    records = dvr_store.load_records()
    if not records:
        st.info("Henüz hesaplanmış kayıt yok. 'Hesapla (Batch)' sekmesinden üret.")
        return

    # Son hesaplamalar
    latest = {}
    for r in records:
        sid = r.get("student_id", "")
        if sid not in latest or r.get("calculated_at", "") > latest[sid].get("calculated_at", ""):
            latest[sid] = r

    all_records = list(latest.values())
    # Yuksek skordan sirala
    all_records.sort(key=lambda r: r.get("behavioral_risk_score", 0), reverse=True)

    df = pd.DataFrame([{
        "Ad Soyad": r.get("student_name", ""),
        "Sınıf/Şube": f"{r.get('sinif','')}{r.get('sube','')}",
        "Davranışsal Skor": round(r.get("behavioral_risk_score", 0), 1),
        "Seviye": BEHAVIORAL_RISK_LEVELS.get(
            r.get("behavioral_risk_level", "LOW"), {}).get("label", "?"),
        "İntihar": round(r.get("kendine_zarar_intihar", 0), 0),
        "Madde": round(r.get("madde_kullanim_supheli", 0), 0),
        "Zorbalık": round(r.get("zorbalik_pattern", 0), 0),
        "Duygusal": round(r.get("duygusal_kizilbayrak", 0), 0),
        "Aile": round(r.get("aile_risk", 0), 0),
    } for r in all_records])

    st.dataframe(df, use_container_width=True, hide_index=True, height=500)

    # Critical + Emergency hızlı liste
    critical = [r for r in all_records if r.get("behavioral_risk_score", 0) >= 70]
    if critical:
        st.markdown(f"### 🚨 Kritik ve ACİL — {len(critical)} öğrenci")
        for r in critical[:10]:
            st.error(
                f"**{r.get('student_name')}** ({r.get('sinif','')}{r.get('sube','')}) — "
                f"Skor: {r.get('behavioral_risk_score'):.0f} | "
                f"Seviye: {BEHAVIORAL_RISK_LEVELS.get(r.get('behavioral_risk_level','LOW'),{}).get('label','?')}"
            )


def _tab_batch_calculate(store, loader, dvr_store, role):
    """Toplu hesaplama — tum ogrenciler icin."""
    if role not in ("superadmin", "yonetici", "calisan", "mudur", "mudur_yardimcisi", "psikolog", "rehber"):
        st.warning("🔒 Yalnızca yetkili roller çalıştırabilir.")
        return

    st.markdown("### ⚙️ Toplu Hesaplama")
    st.caption(
        "Tüm öğrenciler için davranışsal risk hesaplar. "
        "Akademik risk skorları da mevcut Erken Uyarı motorundan çekilir."
    )

    if st.button("🚀 Tüm Öğrenciler için Hesapla", type="primary"):
        try:
            students = loader.load_students() if loader else []
        except Exception:
            students = []
        if not students:
            st.error("Öğrenci verisi yüklenemedi.")
            return

        engine = BehavioralRiskEngine()
        records = engine.calculate_all(students)
        dvr_store.save_records(records)
        AuditLog.log("batch_hesapla", "davranissal_risk", "",
                    notes=f"Toplam {len(records)} ogrenci")
        st.success(f"✅ {len(records)} öğrenci için davranışsal risk hesaplandı.")

        # Özet
        levels_count = {}
        for r in records:
            lvl = r.behavioral_risk_level
            levels_count[lvl] = levels_count.get(lvl, 0) + 1
        cols = st.columns(len(BEHAVIORAL_RISK_LEVELS))
        for i, (k, v) in enumerate(BEHAVIORAL_RISK_LEVELS.items()):
            with cols[i]:
                count = levels_count.get(k, 0)
                st.metric(f"{v['icon']} {v['label']}", count)


# Public API
__all__ = [
    "render_butuncul_panel",
    "render_20_boyutlu_radar",
    "render_dimension_card",
    "render_protocol",
    "render_false_positive_form",
    "render_audit_log",
    "render_fp_summary",
]
