"""
Gorsel Soru Ureticisi
=====================
Profesyonel deneme sinavlari icin gorsel sorular.
Geometri, Fizik, Kimya, Biyoloji, Cografya soru gorselleri.
"""

from __future__ import annotations

import io
import random
import math
import base64
from typing import Callable

# Matplotlib lazy import
def _get_plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    return plt


# ============================================================
# GEOMETRI GORSELLERI
# ============================================================

def create_triangle_question() -> dict:
    """Ucgen sorusu olustur."""
    plt = _get_plt()

    # Rastgele kenarlar
    a = random.randint(3, 8)
    b = random.randint(3, 8)
    c = random.randint(max(abs(a-b)+1, 3), min(a+b-1, 10))

    # Ucgen ciz
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

    # Koordinatlar (basit ucgen)
    points = [(0, 0), (a, 0), (a/2, b*0.8)]
    triangle = plt.Polygon(points, fill=False, edgecolor='#2E6F9E', linewidth=2)
    ax.add_patch(triangle)

    # Kenar uzunluklari
    ax.text(a/2, -0.3, f'{a} cm', ha='center', fontsize=10)
    ax.text(a + 0.2, b*0.4, f'{b} cm', ha='left', fontsize=10)
    ax.text(-0.2, b*0.4, f'{c} cm', ha='right', fontsize=10)

    ax.set_xlim(-1, a+2)
    ax.set_ylim(-1, b+1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Resmi byte'a cevir
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    # Cevre hesapla
    cevre = a + b + c

    return {
        "text": "Yukardaki ucgenin cevresi kac cm'dir?",
        "options": [f"{cevre-2} cm", f"{cevre} cm", f"{cevre+2} cm", f"{cevre+4} cm"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Geometri - Ucgen",
        "difficulty": "Orta",
    }


def create_rectangle_area_question() -> dict:
    """Dikdortgen alan sorusu."""
    plt = _get_plt()

    width = random.randint(4, 10)
    height = random.randint(3, 8)

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

    from matplotlib.patches import Rectangle
    rect = Rectangle((0.5, 0.5), width/2, height/2, fill=False, edgecolor='#2E6F9E', linewidth=2)
    ax.add_patch(rect)

    # Olculer
    ax.text(0.5 + width/4, 0.3, f'{width} cm', ha='center', fontsize=10)
    ax.text(0.5 + width/2 + 0.2, 0.5 + height/4, f'{height} cm', ha='left', fontsize=10)

    ax.set_xlim(0, width/2 + 2)
    ax.set_ylim(0, height/2 + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    area = width * height

    return {
        "text": "Sekildeki dikdortgenin alani kac cm²'dir?",
        "options": [f"{area-height} cm²", f"{area} cm²", f"{area+width} cm²", f"{area+height} cm²"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Geometri - Dikdortgen",
        "difficulty": "Kolay",
    }


def create_circle_question() -> dict:
    """Daire sorusu."""
    plt = _get_plt()

    radius = random.randint(3, 8)

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)

    from matplotlib.patches import Circle
    circle = Circle((2, 2), 1.5, fill=False, edgecolor='#2E6F9E', linewidth=2)
    ax.add_patch(circle)

    # Yaricap cizgisi
    ax.plot([2, 3.5], [2, 2], 'r-', linewidth=1.5)
    ax.text(2.75, 2.15, f'r = {radius} cm', ha='center', fontsize=10)

    # Merkez noktasi
    ax.plot(2, 2, 'ko', markersize=4)
    ax.text(2, 1.7, 'O', ha='center', fontsize=9)

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    cevre = 2 * radius  # pi katsayisi soru icinde

    return {
        "text": f"Yaricapi {radius} cm olan dairenin cevresi kac pi cm'dir?",
        "options": [f"{cevre-2}π cm", f"{cevre}π cm", f"{cevre+2}π cm", f"{cevre+4}π cm"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Geometri - Daire",
        "difficulty": "Orta",
    }


def create_angle_question() -> dict:
    """Aci sorusu."""
    plt = _get_plt()

    angle = random.choice([30, 45, 60, 90, 120, 135, 150])

    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

    # Aci ciz
    ax.plot([0, 3], [0, 0], 'b-', linewidth=2)

    rad = math.radians(angle)
    x2 = 3 * math.cos(rad)
    y2 = 3 * math.sin(rad)
    ax.plot([0, x2], [0, y2], 'b-', linewidth=2)

    # Aci yayı
    theta = [i * math.pi / 180 for i in range(0, angle + 1)]
    arc_x = [0.8 * math.cos(t) for t in theta]
    arc_y = [0.8 * math.sin(t) for t in theta]
    ax.plot(arc_x, arc_y, 'r-', linewidth=1.5)

    # Soru isareti
    mid_angle = math.radians(angle / 2)
    ax.text(1.2 * math.cos(mid_angle), 1.2 * math.sin(mid_angle), '?', fontsize=14, ha='center')

    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    return {
        "text": "Sekilde gosterilen acinin olcusu kac derecedir?",
        "options": [f"{angle-15}°", f"{angle}°", f"{angle+15}°", f"{angle+30}°"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Geometri - Acilar",
        "difficulty": "Kolay",
    }


# ============================================================
# FIZIK GORSELLERI
# ============================================================

def create_velocity_time_graph() -> dict:
    """Hiz-zaman grafigi sorusu."""
    plt = _get_plt()

    v0 = random.randint(0, 5)
    a = random.randint(2, 5)
    t_max = random.randint(4, 8)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    times = list(range(0, t_max + 1))
    velocities = [v0 + a * t for t in times]

    ax.plot(times, velocities, 'b-', linewidth=2, marker='o', markersize=4)
    ax.fill_between(times, velocities, alpha=0.3)

    ax.set_xlabel('Zaman (s)', fontsize=10)
    ax.set_ylabel('Hiz (m/s)', fontsize=10)
    ax.set_title('Hiz-Zaman Grafigi', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, t_max)
    ax.set_ylim(0, max(velocities) + 2)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    # Alinan yol = alan = (v0 + v_son) * t / 2
    v_son = v0 + a * t_max
    distance = (v0 + v_son) * t_max // 2

    return {
        "text": f"Grafige gore cismin {t_max} saniyede aldigi yol yaklasik kac metredir?",
        "options": [f"{distance-10} m", f"{distance} m", f"{distance+10} m", f"{distance+20} m"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Fizik",
        "topic": "Hareket - Hiz-Zaman Grafigi",
        "difficulty": "Orta",
    }


def create_force_diagram() -> dict:
    """Kuvvet diyagrami sorusu."""
    plt = _get_plt()

    f1 = random.randint(10, 30)
    f2 = random.randint(10, 30)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    # Cisim (kutu)
    from matplotlib.patches import Rectangle
    box = Rectangle((1.5, 1.5), 1, 1, fill=True, facecolor='#E8E8E8', edgecolor='black', linewidth=2)
    ax.add_patch(box)

    # F1 - sag yonlu
    ax.annotate('', xy=(3.5, 2), xytext=(2.5, 2),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(3.6, 2, f'F₁={f1}N', fontsize=10, va='center')

    # F2 - sol yonlu
    ax.annotate('', xy=(0.5, 2), xytext=(1.5, 2),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax.text(0.1, 2, f'F₂={f2}N', fontsize=10, va='center')

    ax.set_xlim(0, 4.5)
    ax.set_ylim(0.5, 3.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Kuvvet Diyagrami', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    net_force = abs(f1 - f2)
    direction = "sag" if f1 > f2 else "sol"

    return {
        "text": "Sekildeki cisme etki eden net kuvvet kac Newton'dur?",
        "options": [f"{net_force-5} N", f"{net_force} N", f"{net_force+5} N", f"{f1+f2} N"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Fizik",
        "topic": "Kuvvet ve Hareket",
        "difficulty": "Orta",
    }


def create_circuit_diagram() -> dict:
    """Basit elektrik devresi sorusu."""
    plt = _get_plt()

    voltage = random.choice([6, 9, 12, 24])
    resistance = random.choice([2, 3, 4, 6])

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    # Devre ciz (basitleştirilmis)
    # Pil
    ax.plot([0.5, 0.5], [1, 2], 'k-', linewidth=2)
    ax.plot([0.3, 0.7], [2, 2], 'k-', linewidth=3)
    ax.plot([0.4, 0.6], [2.2, 2.2], 'k-', linewidth=1)
    ax.text(0.5, 0.7, f'V={voltage}V', ha='center', fontsize=10)

    # Ustden kablo
    ax.plot([0.5, 3.5], [2.2, 2.2], 'k-', linewidth=2)

    # Direnc (zigzag)
    ax.plot([3.5, 3.5], [2.2, 1.8], 'k-', linewidth=2)
    zigzag_x = [3.5, 3.7, 3.3, 3.7, 3.3, 3.7, 3.3, 3.5]
    zigzag_y = [1.8, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.6]
    ax.plot(zigzag_x, zigzag_y, 'k-', linewidth=2)
    ax.text(4, 1.2, f'R={resistance}Ω', fontsize=10)

    # Alttan kablo
    ax.plot([3.5, 3.5], [0.6, 0.3], 'k-', linewidth=2)
    ax.plot([0.5, 3.5], [0.3, 0.3], 'k-', linewidth=2)
    ax.plot([0.5, 0.5], [0.3, 1], 'k-', linewidth=2)

    ax.set_xlim(0, 4.5)
    ax.set_ylim(0, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Elektrik Devresi', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    current = voltage // resistance

    return {
        "text": "Devredeki akim siddetini (I) bulunuz.",
        "options": [f"{current-1} A", f"{current} A", f"{current+1} A", f"{current+2} A"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Fizik",
        "topic": "Elektrik - Ohm Kanunu",
        "difficulty": "Orta",
    }


# ============================================================
# KIMYA GORSELLERI
# ============================================================

def create_atom_model() -> dict:
    """Atom modeli sorusu."""
    plt = _get_plt()

    proton = random.randint(6, 18)
    neutron = proton + random.randint(-1, 3)
    electron = proton

    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

    # Cekirdek
    from matplotlib.patches import Circle
    nucleus = Circle((2.5, 2.5), 0.5, fill=True, facecolor='#FFD700', edgecolor='black', linewidth=2)
    ax.add_patch(nucleus)
    ax.text(2.5, 2.5, f'{proton}p\n{neutron}n', ha='center', va='center', fontsize=8)

    # Elektron yörüngeleri
    for r, e_count in [(1.2, min(2, electron)), (1.8, min(8, max(0, electron-2)))]:
        orbit = Circle((2.5, 2.5), r, fill=False, edgecolor='gray', linewidth=1, linestyle='--')
        ax.add_patch(orbit)

        # Elektronlar
        for i in range(e_count):
            angle = 2 * math.pi * i / max(e_count, 1)
            ex = 2.5 + r * math.cos(angle)
            ey = 2.5 + r * math.sin(angle)
            e_circle = Circle((ex, ey), 0.1, fill=True, facecolor='blue')
            ax.add_patch(e_circle)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Atom Modeli', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    mass_number = proton + neutron

    return {
        "text": f"Sekildeki atomun kutle numarasi (A) kactir?",
        "options": [f"{mass_number-2}", f"{mass_number}", f"{mass_number+2}", f"{proton}"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Kimya",
        "topic": "Atom Yapisi",
        "difficulty": "Orta",
    }


def create_ph_scale() -> dict:
    """pH skalasi sorusu."""
    plt = _get_plt()

    fig, ax = plt.subplots(figsize=(6, 2), dpi=100)

    # pH skalasi
    colors = ['#FF0000', '#FF4500', '#FFA500', '#FFD700', '#FFFF00', '#ADFF2F',
              '#00FF00', '#00FA9A', '#00CED1', '#1E90FF', '#0000FF', '#4B0082', '#8B00FF', '#9400D3', '#800080']

    for i, color in enumerate(colors):
        from matplotlib.patches import Rectangle
        rect = Rectangle((i * 0.4, 0), 0.4, 1, facecolor=color)
        ax.add_patch(rect)
        ax.text(i * 0.4 + 0.2, -0.2, str(i), ha='center', fontsize=8)

    # Isaretler
    ax.text(1, 1.3, 'ASİT', ha='center', fontsize=9, fontweight='bold')
    ax.text(3.5, 1.3, 'NOTR', ha='center', fontsize=9, fontweight='bold')
    ax.text(5.5, 1.3, 'BAZ', ha='center', fontsize=9, fontweight='bold')

    # Soru isareti
    target_ph = random.choice([2, 3, 4, 10, 11, 12])
    ax.annotate('?', xy=(target_ph * 0.4 + 0.2, 0.5), fontsize=16, ha='center',
                xytext=(target_ph * 0.4 + 0.2, 1.8),
                arrowprops=dict(arrowstyle='->', color='black'))

    ax.set_xlim(-0.2, 6.2)
    ax.set_ylim(-0.5, 2.2)
    ax.axis('off')
    ax.set_title('pH Skalası', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    substance = "limon suyu" if target_ph < 7 else "sabun"
    prop = "asidik" if target_ph < 7 else "bazik"

    return {
        "text": f"pH degeri {target_ph} olan bir madde hangi ozelliktedir?",
        "options": ["Asidik", "Bazik", "Notr", "Amfoter"],
        "answer": "A" if target_ph < 7 else "B",
        "image_bytes": image_bytes,
        "subject": "Kimya",
        "topic": "Asit ve Bazlar",
        "difficulty": "Kolay",
    }


# ============================================================
# BIYOLOJI GORSELLERI
# ============================================================

def create_cell_diagram() -> dict:
    """Hucre diyagrami sorusu."""
    plt = _get_plt()

    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

    from matplotlib.patches import Circle, Ellipse

    # Hucre zari
    cell = Circle((2.5, 2.5), 2, fill=False, edgecolor='#2E6F9E', linewidth=3)
    ax.add_patch(cell)

    # Cekirdek
    nucleus = Circle((2.5, 2.5), 0.6, fill=True, facecolor='#8B4513', edgecolor='black', linewidth=2)
    ax.add_patch(nucleus)
    ax.text(2.5, 2.5, 'A', ha='center', va='center', fontsize=10, color='white', fontweight='bold')

    # Mitokondri
    mito = Ellipse((1.3, 3), 0.5, 0.25, angle=30, fill=True, facecolor='#FF6B6B', edgecolor='black')
    ax.add_patch(mito)
    ax.text(1.3, 3, 'B', ha='center', va='center', fontsize=8)

    # Ribozom
    for pos in [(3.2, 3.5), (3.5, 3.2), (3.7, 2.8)]:
        ribo = Circle(pos, 0.08, fill=True, facecolor='#4ECDC4')
        ax.add_patch(ribo)
    ax.text(3.8, 3.5, 'C', fontsize=8)

    # Golgi
    for i in range(3):
        golgi = Ellipse((1.5, 1.5 + i*0.15), 0.6, 0.1, fill=True, facecolor='#95E1D3', edgecolor='black')
        ax.add_patch(golgi)
    ax.text(1.5, 1.2, 'D', ha='center', fontsize=8)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Hayvan Hucresi', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    organelles = ["Cekirdek", "Mitokondri", "Ribozom", "Golgi"]
    question_target = random.choice(["A", "B"])
    correct = "Cekirdek" if question_target == "A" else "Mitokondri"

    return {
        "text": f"Sekilde '{question_target}' ile gosterilen organel hangisidir?",
        "options": ["Cekirdek", "Mitokondri", "Ribozom", "Golgi"],
        "answer": "A" if question_target == "A" else "B",
        "image_bytes": image_bytes,
        "subject": "Biyoloji",
        "topic": "Hucre Yapisi",
        "difficulty": "Kolay",
    }


def create_dna_structure() -> dict:
    """DNA yapisi sorusu."""
    plt = _get_plt()

    fig, ax = plt.subplots(figsize=(4, 5), dpi=100)

    # DNA sarmal
    t = [i * 0.1 for i in range(50)]
    x1 = [math.sin(ti * 2) + 2 for ti in t]
    x2 = [-math.sin(ti * 2) + 2 for ti in t]
    y = [ti for ti in t]

    ax.plot(x1, y, 'b-', linewidth=2, label='Seker-Fosfat')
    ax.plot(x2, y, 'b-', linewidth=2)

    # Baz ciftleri
    bases = ['A-T', 'G-C', 'T-A', 'C-G', 'A-T']
    for i, base in enumerate(bases):
        yi = i + 0.5
        xi1 = math.sin(yi * 2) + 2
        xi2 = -math.sin(yi * 2) + 2
        ax.plot([xi1, xi2], [yi, yi], 'r-', linewidth=1.5)
        ax.text(2, yi, base, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('DNA Yapisi', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    return {
        "text": "DNA'da Adenin (A) hangi baz ile eslesir?",
        "options": ["Guanin (G)", "Sitozin (C)", "Timin (T)", "Urasil (U)"],
        "answer": "C",
        "image_bytes": image_bytes,
        "subject": "Biyoloji",
        "topic": "DNA Yapisi",
        "difficulty": "Orta",
    }


# ============================================================
# COGRAFYA GORSELLERI
# ============================================================

def create_climate_graph() -> dict:
    """Iklim grafigi (sicaklik-yagis) sorusu."""
    plt = _get_plt()

    months = ['O', 'S', 'M', 'N', 'M', 'H', 'T', 'A', 'E', 'E', 'K', 'A']

    # Akdeniz iklimi benzeri
    temps = [10, 11, 14, 17, 22, 26, 29, 29, 25, 20, 15, 11]
    precip = [120, 100, 80, 50, 30, 10, 5, 10, 30, 70, 100, 130]

    fig, ax1 = plt.subplots(figsize=(6, 4), dpi=100)

    # Sicaklik cizgisi
    ax1.plot(months, temps, 'r-o', linewidth=2, label='Sicaklik (°C)')
    ax1.set_ylabel('Sicaklik (°C)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.set_ylim(0, 35)

    # Yagis cubuk grafigi
    ax2 = ax1.twinx()
    ax2.bar(months, precip, alpha=0.5, color='blue', label='Yagis (mm)')
    ax2.set_ylabel('Yagis (mm)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(0, 200)

    ax1.set_xlabel('Aylar')
    ax1.set_title('Iklim Grafigi', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    return {
        "text": "Grafikteki iklim tipi asagidakilerden hangisidir?",
        "options": ["Akdeniz Iklimi", "Karasal Iklim", "Ekvatoral Iklim", "Muson Iklimi"],
        "answer": "A",
        "image_bytes": image_bytes,
        "subject": "Cografya",
        "topic": "Iklim Tipleri",
        "difficulty": "Orta",
    }


def create_population_pyramid() -> dict:
    """Nufus piramidi sorusu."""
    plt = _get_plt()

    ages = ['0-14', '15-29', '30-44', '45-59', '60-74', '75+']

    # Genc nufus yapisi
    male = [-15, -20, -18, -12, -8, -4]
    female = [14, 19, 17, 11, 9, 5]

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    y_pos = range(len(ages))
    ax.barh(y_pos, male, color='#4A90D9', label='Erkek')
    ax.barh(y_pos, female, color='#E85D75', label='Ferkek')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(ages)
    ax.set_xlabel('Nufus (%)')
    ax.set_title('Nufus Piramidi', fontsize=11)
    ax.legend(loc='lower right')
    ax.axvline(0, color='black', linewidth=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    return {
        "text": "Bu nufus piramidi hangi ulke tipini gosterir?",
        "options": ["Gelismekte olan ulke", "Gelismis ulke", "Az gelismis ulke", "Duragan nufuslu ulke"],
        "answer": "A",
        "image_bytes": image_bytes,
        "subject": "Cografya",
        "topic": "Nufus",
        "difficulty": "Orta",
    }


# ============================================================
# MATEMATIK - FONKSIYON VE GRAFIK
# ============================================================

def create_function_graph() -> dict:
    """Fonksiyon grafigi sorusu."""
    plt = _get_plt()

    a = random.choice([1, 2, -1, -2])
    b = random.randint(-3, 3)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    x = [i * 0.5 for i in range(-8, 9)]
    y = [a * xi + b for xi in x]

    ax.plot(x, y, 'b-', linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'f(x) = {"" if a == 1 else ("-" if a == -1 else str(a))}x {("+" if b >= 0 else "") + str(b) if b != 0 else ""}', fontsize=11)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-6, 6)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    # x = 2 icin deger
    x_val = 2
    y_val = a * x_val + b

    return {
        "text": f"Grafikteki fonksiyon icin f({x_val}) degeri kactir?",
        "options": [f"{y_val-2}", f"{y_val}", f"{y_val+2}", f"{y_val+4}"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Fonksiyonlar",
        "difficulty": "Orta",
    }


def create_pie_chart_question() -> dict:
    """Pasta grafigi sorusu."""
    plt = _get_plt()

    labels = ['A', 'B', 'C', 'D']
    sizes = [random.randint(15, 35) for _ in range(3)]
    sizes.append(100 - sum(sizes))

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
                                       startangle=90, textprops={'fontsize': 10})

    ax.set_title('Ogrenci Ders Tercihleri', fontsize=11)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    total_students = random.choice([100, 200, 500])
    target_idx = random.randint(0, 3)
    target_label = labels[target_idx]
    target_count = sizes[target_idx] * total_students // 100

    return {
        "text": f"Toplam {total_students} ogrenci varsa, {target_label} secenegini tercih eden ogrenci sayisi kactir?",
        "options": [f"{target_count-10}", f"{target_count}", f"{target_count+10}", f"{target_count+20}"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Veri Analizi",
        "difficulty": "Kolay",
    }


def create_bar_chart_question() -> dict:
    """Cubuk grafik sorusu."""
    plt = _get_plt()

    categories = ['Pazartesi', 'Sali', 'Carsamba', 'Persembe', 'Cuma']
    values = [random.randint(20, 80) for _ in range(5)]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    bars = ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax.set_ylabel('Satis (adet)')
    ax.set_title('Haftalik Satis Grafigi', fontsize=11)

    # Deger etiketleri
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val),
                ha='center', va='bottom', fontsize=9)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    total = sum(values)
    max_day = categories[values.index(max(values))]

    return {
        "text": "Grafige gore haftalik toplam satis kac adettir?",
        "options": [f"{total-20}", f"{total}", f"{total+20}", f"{total+40}"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Veri Analizi",
        "difficulty": "Kolay",
    }


# ============================================================
# TABLO SORULARI
# ============================================================

def create_table_question() -> dict:
    """Tablo sorusu."""
    plt = _get_plt()

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.axis('off')

    # Tablo verisi
    data = [
        ['Urun', 'Fiyat (TL)', 'Adet'],
        ['Kalem', '5', '10'],
        ['Defter', '15', '5'],
        ['Silgi', '3', '20'],
    ]

    table = ax.table(cellText=data, loc='center', cellLoc='center',
                     colWidths=[0.3, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Baslik satiri renklendir
    for j in range(3):
        table[(0, j)].set_facecolor('#4ECDC4')
        table[(0, j)].set_text_props(fontweight='bold')

    ax.set_title('Urun Listesi', fontsize=11, pad=20)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    image_bytes = buf.read()

    # Toplam hesapla
    total = 5*10 + 15*5 + 3*20  # 50 + 75 + 60 = 185

    return {
        "text": "Tablodaki tum urunlerin toplam tutari kac TL'dir?",
        "options": ["175 TL", "185 TL", "195 TL", "205 TL"],
        "answer": "B",
        "image_bytes": image_bytes,
        "subject": "Matematik",
        "topic": "Problem Cozme",
        "difficulty": "Orta",
    }


# ============================================================
# ANA FONKSIYON - GORSEL SORU URETICI
# ============================================================

VISUAL_GENERATORS = {
    "Matematik": [
        create_triangle_question,
        create_rectangle_area_question,
        create_circle_question,
        create_angle_question,
        create_function_graph,
        create_pie_chart_question,
        create_bar_chart_question,
        create_table_question,
    ],
    "Fizik": [
        create_velocity_time_graph,
        create_force_diagram,
        create_circuit_diagram,
    ],
    "Kimya": [
        create_atom_model,
        create_ph_scale,
    ],
    "Biyoloji": [
        create_cell_diagram,
        create_dna_structure,
    ],
    "Cografya": [
        create_climate_graph,
        create_population_pyramid,
    ],
}


def generate_visual_question(subject: str) -> dict | None:
    """Belirtilen ders icin gorsel soru uret."""
    generators = VISUAL_GENERATORS.get(subject, [])
    if not generators:
        return None

    try:
        generator = random.choice(generators)
        return generator()
    except Exception as e:
        print(f"Gorsel soru uretim hatasi: {e}")
        return None


def get_available_visual_subjects() -> list[str]:
    """Gorsel soru uretebilen dersleri dondur."""
    return list(VISUAL_GENERATORS.keys())
