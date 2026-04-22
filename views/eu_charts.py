# -*- coding: utf-8 -*-
"""
Erken Uyarı — Ultra Premium Grafik & Analiz Motoru
====================================================
Plotly 3D, pasta, sütun, çan eğrisi, radar, gauge + AI yorum.
"""
from __future__ import annotations

import math
import streamlit as st

# ═══════════════════════════════════════════════════════════════
# TEMA RENKLERI
# ═══════════════════════════════════════════════════════════════

_BG = "#0B0F19"
_CARD = "#131825"
_BORDER = "#1e293b"
_TEXT = "#e2e8f0"
_MUTED = "#64748b"
_ACCENT = "#6366f1"
_GREEN = "#22c55e"
_YELLOW = "#f59e0b"
_ORANGE = "#f97316"
_RED = "#ef4444"
_PURPLE = "#8b5cf6"
_BLUE = "#3b82f6"
_CYAN = "#06b6d4"
_PINK = "#ec4899"

_RISK_COLORS = {"LOW": _GREEN, "MEDIUM": _YELLOW, "HIGH": _ORANGE, "CRITICAL": _RED}
_COMP_COLORS = [_BLUE, _RED, _ORANGE, _YELLOW, _PURPLE, _CYAN, _GREEN, _PINK, "#f43f5e", "#6366f1"]

_PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=_TEXT, family="Inter, system-ui, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)


def _chart_key():
    if "_eu_ck" not in st.session_state:
        st.session_state["_eu_ck"] = 0
    st.session_state["_eu_ck"] += 1
    return f"eu_chart_{st.session_state['_eu_ck']}"


# ═══════════════════════════════════════════════════════════════
# 1. RISK DAĞILIMI — 3D Pasta Grafiği
# ═══════════════════════════════════════════════════════════════

def risk_distribution_3d_pie(low, med, high, crit):
    """Risk seviye dağılımı — 3D görünümlü pasta."""
    import plotly.graph_objects as go
    labels = ["Düşük", "Orta", "Yüksek", "Kritik"]
    values = [low, med, high, crit]
    colors = [_GREEN, _YELLOW, _ORANGE, _RED]

    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color=_BG, width=3)),
        textinfo="label+percent+value",
        textfont=dict(size=13, color="#fff"),
        pull=[0, 0, 0.05, 0.1],
    )])
    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="Risk Seviye Dağılımı", font=dict(size=16, color=_TEXT)),
        height=350,
        annotations=[dict(text=f"<b>{sum(values)}</b><br>Öğrenci", x=0.5, y=0.5,
                          font_size=16, font_color=_TEXT, showarrow=False)],
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 2. BİLEŞEN ORTALAMA — 3D Sütun Grafiği
# ═══════════════════════════════════════════════════════════════

def component_bar_3d(comp_avgs: dict):
    """Bileşen ortalamaları — 3D sütun."""
    import plotly.graph_objects as go
    labels = list(comp_avgs.keys())
    values = list(comp_avgs.values())
    colors = [_GREEN if v < 30 else _YELLOW if v < 55 else _ORANGE if v < 75 else _RED for v in values]

    fig = go.Figure(data=[go.Bar(
        x=labels, y=values,
        marker=dict(color=colors, line=dict(color="#fff", width=0.5),
                    pattern=dict(shape="/")),
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(color=_TEXT, size=11),
    )])
    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="Bileşen Risk Ortalamaları", font=dict(size=16, color=_TEXT)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#1e293b", range=[0, 100],
                   title="Risk Skoru"),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 3. ÇAN EĞRİSİ — Normal Dağılım
# ═══════════════════════════════════════════════════════════════

def bell_curve(scores: list[float], title="Risk Puanı Dağılımı"):
    """Çan eğrisi — risk puanlarının normal dağılım analizi."""
    import plotly.graph_objects as go

    if len(scores) < 3:
        return

    mean = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mean) ** 2 for s in scores) / len(scores))
    if std == 0:
        std = 1

    # Histogram
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=scores, nbinsx=20,
        marker=dict(color=_ACCENT, line=dict(color="#818cf8", width=1)),
        opacity=0.7, name="Dağılım",
    ))

    # Normal curve overlay
    x_range = [max(0, mean - 3.5 * std + i * (7 * std / 100)) for i in range(101)]
    y_normal = [len(scores) * (7 * std / 20) * (1 / (std * math.sqrt(2 * math.pi))) *
                math.exp(-0.5 * ((x - mean) / std) ** 2) for x in x_range]
    fig.add_trace(go.Scatter(
        x=x_range, y=y_normal, mode="lines",
        line=dict(color=_CYAN, width=3), name="Çan Eğrisi",
    ))

    # Mean line
    fig.add_vline(x=mean, line_dash="dash", line_color=_YELLOW, line_width=2,
                  annotation_text=f"Ort: {mean:.1f}", annotation_position="top")

    # Risk zone backgrounds
    fig.add_vrect(x0=0, x1=29, fillcolor=_GREEN, opacity=0.08, layer="below", line_width=0)
    fig.add_vrect(x0=30, x1=54, fillcolor=_YELLOW, opacity=0.08, layer="below", line_width=0)
    fig.add_vrect(x0=55, x1=74, fillcolor=_ORANGE, opacity=0.08, layer="below", line_width=0)
    fig.add_vrect(x0=75, x1=100, fillcolor=_RED, opacity=0.08, layer="below", line_width=0)

    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text=title, font=dict(size=16, color=_TEXT)),
        xaxis=dict(title="Risk Skoru", range=[0, 100], showgrid=True, gridcolor="#1e293b"),
        yaxis=dict(title="Öğrenci Sayısı", showgrid=True, gridcolor="#1e293b"),
        height=380, barmode="overlay", showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())

    # İstatistik özet
    median = sorted(scores)[len(scores) // 2]
    skew = sum(((s - mean) / std) ** 3 for s in scores) / len(scores) if std > 0 else 0
    st.markdown(f"""<div style="display:flex;gap:12px;justify-content:center;margin:8px 0;">
    <span style="background:{_CARD};border:1px solid {_BORDER};border-radius:8px;padding:6px 14px;font-size:.78rem;">
    <span style="color:{_MUTED};">Ort:</span> <b style="color:{_TEXT};">{mean:.1f}</b></span>
    <span style="background:{_CARD};border:1px solid {_BORDER};border-radius:8px;padding:6px 14px;font-size:.78rem;">
    <span style="color:{_MUTED};">Medyan:</span> <b style="color:{_TEXT};">{median:.1f}</b></span>
    <span style="background:{_CARD};border:1px solid {_BORDER};border-radius:8px;padding:6px 14px;font-size:.78rem;">
    <span style="color:{_MUTED};">Std:</span> <b style="color:{_TEXT};">{std:.1f}</b></span>
    <span style="background:{_CARD};border:1px solid {_BORDER};border-radius:8px;padding:6px 14px;font-size:.78rem;">
    <span style="color:{_MUTED};">Çarpıklık:</span> <b style="color:{_TEXT};">{skew:.2f}</b></span>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 4. RADAR GRAFİĞİ — Öğrenci Bileşen Profili
# ═══════════════════════════════════════════════════════════════

def student_radar(components: dict, student_name: str = ""):
    """10 bileşenli radar grafik — öğrenci risk profili."""
    import plotly.graph_objects as go

    labels = list(components.keys())
    values = list(components.values())
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed, theta=labels_closed,
        fill="toself",
        fillcolor=f"rgba(99,102,241,0.15)",
        line=dict(color=_ACCENT, width=2),
        marker=dict(size=6, color=[_GREEN if v < 30 else _YELLOW if v < 55 else _ORANGE if v < 75 else _RED for v in values] + [_GREEN]),
        name=student_name or "Risk Profili",
    ))

    fig.update_layout(
        **_PLOTLY_LAYOUT,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True,
                            tickfont=dict(size=9, color=_MUTED), gridcolor="#1e293b"),
            angularaxis=dict(tickfont=dict(size=10, color=_TEXT), gridcolor="#1e293b"),
        ),
        title=dict(text=f"Risk Profili{(' — ' + student_name) if student_name else ''}",
                   font=dict(size=16, color=_TEXT)),
        height=420, showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 5. GAUGE — Risk Skoru Göstergesi
# ═══════════════════════════════════════════════════════════════

def risk_gauge(score: float, title="Risk Skoru"):
    """Profesyonel gauge gösterge — 0-100 arası risk skoru."""
    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title=dict(text=title, font=dict(size=16, color=_TEXT)),
        number=dict(font=dict(size=36, color=_TEXT)),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=2, tickcolor=_MUTED,
                      tickfont=dict(size=10, color=_MUTED)),
            bar=dict(color=_ACCENT, thickness=0.3),
            bgcolor=_CARD,
            borderwidth=2, bordercolor=_BORDER,
            steps=[
                dict(range=[0, 29], color="rgba(34,197,94,0.2)"),
                dict(range=[30, 54], color="rgba(245,158,11,0.2)"),
                dict(range=[55, 74], color="rgba(249,115,22,0.2)"),
                dict(range=[75, 100], color="rgba(239,68,68,0.2)"),
            ],
            threshold=dict(line=dict(color=_RED, width=3), thickness=0.8, value=75),
        ),
    ))
    fig.update_layout(
        **_PLOTLY_LAYOUT,
        height=280,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 6. SINIF KARŞILAŞTIRMA — Grouped Bar
# ═══════════════════════════════════════════════════════════════

def class_comparison_bar(class_data: dict):
    """Sınıf bazlı risk karşılaştırma — grouped bar."""
    import plotly.graph_objects as go

    classes = list(class_data.keys())
    avgs = [sum(v) / len(v) for v in class_data.values()]
    counts = [len(v) for v in class_data.values()]
    colors = [_GREEN if a < 30 else _YELLOW if a < 55 else _ORANGE if a < 75 else _RED for a in avgs]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=classes, y=avgs, name="Risk Ort.",
        marker=dict(color=colors, line=dict(color="#fff", width=0.5)),
        text=[f"{a:.1f}" for a in avgs], textposition="outside",
        textfont=dict(size=10, color=_TEXT),
    ))

    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="Sınıf Bazlı Risk Karşılaştırma", font=dict(size=16, color=_TEXT)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#1e293b", range=[0, max(avgs) * 1.3 if avgs else 100],
                   title="Risk Skoru"),
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 7. TREND CHART — Zaman Serisi
# ═══════════════════════════════════════════════════════════════

def risk_trend_line(dates: list[str], scores: list[float], student_name: str = ""):
    """Risk trendi — zaman serisi çizgi grafik."""
    import plotly.graph_objects as go

    fig = go.Figure()
    colors = [_GREEN if s < 30 else _YELLOW if s < 55 else _ORANGE if s < 75 else _RED for s in scores]

    fig.add_trace(go.Scatter(
        x=dates, y=scores, mode="lines+markers",
        line=dict(color=_ACCENT, width=3),
        marker=dict(size=8, color=colors, line=dict(color="#fff", width=1)),
        fill="tozeroy", fillcolor="rgba(99,102,241,0.08)",
        name="Risk Skoru",
    ))

    # Risk zone lines
    for threshold, color, label in [(29, _GREEN, "Düşük"), (54, _YELLOW, "Orta"), (74, _ORANGE, "Yüksek")]:
        fig.add_hline(y=threshold, line_dash="dot", line_color=color, opacity=0.4,
                      annotation_text=label, annotation_position="right")

    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text=f"Risk Trendi{(' — ' + student_name) if student_name else ''}",
                   font=dict(size=16, color=_TEXT)),
        xaxis=dict(showgrid=True, gridcolor="#1e293b"),
        yaxis=dict(showgrid=True, gridcolor="#1e293b", range=[0, 100], title="Risk"),
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 8. DÖNEM KARŞILAŞTIRMA — Waterfall / Butterfly
# ═══════════════════════════════════════════════════════════════

def period_comparison_butterfly(comp_labels: dict, first_avgs: dict, last_avgs: dict):
    """Dönem karşılaştırma — butterfly chart."""
    import plotly.graph_objects as go

    labels = list(comp_labels.values())
    keys = list(comp_labels.keys())
    first_vals = [first_avgs.get(k, 0) for k in keys]
    last_vals = [last_avgs.get(k, 0) for k in keys]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=[-v for v in first_vals], orientation="h",
        name="İlk Dönem", marker=dict(color=_BLUE, opacity=0.7),
        text=[f"{v:.1f}" for v in first_vals], textposition="inside",
    ))
    fig.add_trace(go.Bar(
        y=labels, x=last_vals, orientation="h",
        name="Son Dönem", marker=dict(color=_PURPLE, opacity=0.7),
        text=[f"{v:.1f}" for v in last_vals], textposition="inside",
    ))

    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="Dönem Karşılaştırma (Bileşen Bazlı)", font=dict(size=16, color=_TEXT)),
        barmode="overlay",
        xaxis=dict(showgrid=True, gridcolor="#1e293b", zeroline=True, zerolinecolor=_MUTED,
                   title="← İlk Dönem | Son Dönem →"),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 9. 3D SURFACE — Risk Isı Haritası
# ═══════════════════════════════════════════════════════════════

def heatmap_3d_surface(class_names: list, comp_names: list, z_data: list[list[float]]):
    """3D surface plot — sınıf × bileşen risk ısı haritası."""
    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Surface(
        z=z_data,
        x=list(range(len(comp_names))),
        y=list(range(len(class_names))),
        colorscale=[[0, _GREEN], [0.3, _YELLOW], [0.55, _ORANGE], [0.75, _RED], [1, "#7f1d1d"]],
        showscale=True,
        colorbar=dict(title="Risk", tickfont=dict(color=_TEXT)),
    )])
    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="3D Risk Isı Haritası", font=dict(size=16, color=_TEXT)),
        scene=dict(
            xaxis=dict(title="Bileşen", ticktext=comp_names, tickvals=list(range(len(comp_names))),
                       backgroundcolor=_BG, gridcolor="#1e293b", tickfont=dict(size=8)),
            yaxis=dict(title="Sınıf", ticktext=class_names, tickvals=list(range(len(class_names))),
                       backgroundcolor=_BG, gridcolor="#1e293b", tickfont=dict(size=9)),
            zaxis=dict(title="Risk", range=[0, 100], backgroundcolor=_BG, gridcolor="#1e293b"),
            bgcolor=_BG,
        ),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 10. SUNBURST — Hiyerarşik Risk Dağılımı
# ═══════════════════════════════════════════════════════════════

def risk_sunburst(risks: list[dict]):
    """Sunburst — Okul > Sınıf > Öğrenci hiyerarşik risk."""
    import plotly.graph_objects as go

    ids, labels, parents, values, colors = [], [], [], [], []

    # Root
    ids.append("Okul")
    labels.append("Okul")
    parents.append("")
    values.append(0)
    colors.append(_ACCENT)

    # Sınıf grupları
    class_map: dict[str, list] = {}
    for r in risks:
        k = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
        class_map.setdefault(k, []).append(r)

    for cls, students in class_map.items():
        avg = sum(s.get("risk_score", 0) for s in students) / len(students)
        clr = _GREEN if avg < 30 else _YELLOW if avg < 55 else _ORANGE if avg < 75 else _RED
        ids.append(cls)
        labels.append(cls)
        parents.append("Okul")
        values.append(round(avg))
        colors.append(clr)

        for s in students[:10]:  # max 10 per class for readability
            sid = s.get("student_id", "?")
            sc = s.get("risk_score", 0)
            s_clr = _GREEN if sc < 30 else _YELLOW if sc < 55 else _ORANGE if sc < 75 else _RED
            ids.append(f"{cls}_{sid}")
            labels.append(s.get("student_name", "?")[:15])
            parents.append(cls)
            values.append(round(sc))
            colors.append(s_clr)

    fig = go.Figure(go.Sunburst(
        ids=ids, labels=labels, parents=parents, values=values,
        marker=dict(colors=colors, line=dict(width=1, color=_BG)),
        branchvalues="total",
        textfont=dict(size=10),
    ))
    fig.update_layout(
        **_PLOTLY_LAYOUT,
        title=dict(text="Hiyerarşik Risk Dağılımı (Okul → Sınıf → Öğrenci)",
                   font=dict(size=16, color=_TEXT)),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True, key=_chart_key())


# ═══════════════════════════════════════════════════════════════
# 11. PREMIUM STAT CARD
# ═══════════════════════════════════════════════════════════════

def premium_stat_card(label: str, value: str, delta: str = "", color: str = _ACCENT,
                      icon: str = "", subtitle: str = ""):
    """Ultra premium tek stat kartı."""
    delta_html = ""
    if delta:
        d_clr = _GREEN if delta.startswith("-") or delta.startswith("↓") else _RED if delta.startswith("+") or delta.startswith("↑") else _YELLOW
        delta_html = f'<div style="color:{d_clr};font-size:.75rem;font-weight:600;margin-top:2px;">{delta}</div>'

    return f"""<div style="background:linear-gradient(135deg,{_CARD},{_BG});border-radius:14px;
    padding:16px;border:1px solid {color}25;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-10px;right:-10px;font-size:3rem;opacity:.06;color:{color};">{icon}</div>
    <div style="color:{_MUTED};font-size:.72rem;text-transform:uppercase;letter-spacing:.5px;">{label}</div>
    <div style="font-size:1.6rem;font-weight:800;color:{color};margin:4px 0;">{value}</div>
    {delta_html}
    {f'<div style="color:{_MUTED};font-size:.68rem;">{subtitle}</div>' if subtitle else ''}
    </div>"""
