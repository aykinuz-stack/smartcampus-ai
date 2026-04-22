"""
SINAV OLUSTURUCU - MEB/OSYM UYUMLU
==================================
LGS, TYT, AYT formatinda profesyonel sinav olusturma modulu.
Gorsel sorular, AI destegi, PDF cikti.
"""

import streamlit as st
import random
import hashlib
import json
import io
import base64
from datetime import datetime
from typing import Optional
import os

from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("olcme_degerlendirme")
except Exception:
    pass

# ============================================================
# YAPILANDIRMA
# ============================================================

SINAV_TURLERI = {
    "LGS": {"ad": "Liselere Gecis Sınavı", "sinif": 8, "sik": 4, "gorsel_oran": 0.7},
    "TYT": {"ad": "Temel Yeterlilik Testi", "sinif": 12, "sik": 5, "gorsel_oran": 0.65},
    "AYT": {"ad": "Alan Yeterlilik Testi", "sinif": 12, "sik": 5, "gorsel_oran": 0.75},
    "Deneme": {"ad": "Okul Deneme Sınavı", "sinif": 0, "sik": 4, "gorsel_oran": 0.5},
}

DERSLER = {
    "Matematik": {"renk": "#3498db", "ikon": "📐"},
    "Turkce": {"renk": "#e74c3c", "ikon": "📖"},
    "Fen": {"renk": "#2ecc71", "ikon": "🔬"},
    "Sosyal": {"renk": "#f39c12", "ikon": "🌍"},
    "Ingilizce": {"renk": "#9b59b6", "ikon": "🇬🇧"},
}

# ============================================================
# SORU BANKASI - ZENGIN VE CESITLI
# ============================================================

SORU_BANKASI = {
    "Matematik": {
        "Kolay": [
            {
                "tip": "hesaplama",
                "sablon": "Bir bahcede {a} elma agaci ve {b} armut agaci vardir. Toplam kac agac vardir?",
                "cozum": lambda a, b: a + b,
                "celdirici": lambda ans: [ans - 1, ans, ans + 1, ans + 2],
                "dogru": 1,
            },
            {
                "tip": "hesaplama",
                "sablon": "Ali'nin {a} TL'si vardi. Annesi {b} TL daha verdi. Ali'nin simdi kac TL'si var?",
                "cozum": lambda a, b: a + b,
                "celdirici": lambda ans: [ans - 2, ans, ans + 3, ans - 1],
                "dogru": 1,
            },
            {
                "tip": "carpma",
                "sablon": "Bir kutuda {a} kalem var. {b} kutu kalem alinirsa toplam kac kalem olur?",
                "cozum": lambda a, b: a * b,
                "celdirici": lambda ans: [ans - a, ans, ans + a, a + b],
                "dogru": 1,
            },
        ],
        "Orta": [
            {
                "tip": "problem",
                "sablon": "Bir markette elmalar {a} TL/kg'dir. {b} kg elma alan bir musteri kasada {c} TL verirse, kac TL para ustu alir?",
                "hesapla": lambda: (random.randint(5, 15), random.randint(2, 5), 100),
                "cozum": lambda a, b, c: c - (a * b),
                "celdirici": lambda ans, a, b: [a * b, ans, ans + 5, c - a],
                "dogru": 1,
            },
            {
                "tip": "oran",
                "sablon": "Bir sinifta {a} ogrenci var. Öğrencilerin {b}/'u kiz ise kac erkek ogrenci vardir?",
                "hesapla": lambda: (random.choice([20, 24, 30, 36]), random.choice([2, 3])),
                "cozum": lambda a, b: a - (a // b),
                "dogru": 1,
            },
        ],
        "Zor": [
            {
                "tip": "denklem",
                "sablon": "x + {a} = {b} denkleminde x degeri kactir?",
                "hesapla": lambda: (random.randint(5, 15), random.randint(20, 40)),
                "cozum": lambda a, b: b - a,
                "dogru": 1,
            },
            {
                "tip": "geometri",
                "sablon": "Bir dikdortgenin kisa kenari {a} cm, uzun kenari {b} cm'dir. Dikdortgenin cevresi kac cm'dir?",
                "hesapla": lambda: (random.randint(3, 8), random.randint(10, 15)),
                "cozum": lambda a, b: 2 * (a + b),
                "dogru": 1,
            },
        ],
    },
    "Turkce": {
        "Kolay": [
            {
                "tip": "yazim",
                "metin": "Asagidaki cumlelerden hangisinde yazim yanlisi vardir?",
                "secenekler": ["Herkez toplantiya katildi.", "Herkes toplantiya katildi.", "Kimse gelmedi.", "Biri vardi."],
                "dogru": 0,
            },
            {
                "tip": "es_anlam",
                "metin": "'Guzel' kelimesinin es anlamlisi asagidakilerden hangisidir?",
                "secenekler": ["Cirkin", "Hos", "Kotu", "Fena"],
                "dogru": 1,
            },
        ],
        "Orta": [
            {
                "tip": "paragraf",
                "metin": """Kitap okumak, insanin dunya gorusunu genisletir. Farkli kulturleri, farkli dusunceleri taniriz.

Bu paragrafa gore kitap okumanin en onemli faydasi nedir?""",
                "secenekler": ["Eglence saglar", "Dunya gorusunu genisletir", "Para kazandirir", "Uyku getirir"],
                "dogru": 1,
            },
        ],
        "Zor": [
            {
                "tip": "anlam",
                "metin": "'Elden gelen bogaz', 'El elden ustundur' deyimlerindeki 'el' sozcuklerinin anlam iliskisi nedir?",
                "secenekler": ["Es anlamli", "Zit anlamli", "Es sesli (sesdas)", "Yakin anlamli"],
                "dogru": 2,
            },
        ],
    },
    "Fen": {
        "Kolay": [
            {
                "tip": "bilgi",
                "metin": "Asagidakilerden hangisi bir element degildir?",
                "secenekler": ["Demir (Fe)", "Su (H2O)", "Oksijen (O)", "Karbon (C)"],
                "dogru": 1,
            },
            {
                "tip": "bilgi",
                "metin": "Bitkilerin besin uretmek için kullandigi olay hangisidir?",
                "secenekler": ["Solunum", "Fotosentez", "Bosaltim", "Sindirim"],
                "dogru": 1,
            },
        ],
        "Orta": [
            {
                "tip": "hesaplama",
                "metin": "Bir cisim {v} m/s hizla {t} saniye hareket ederse aldigi yol kac metredir?",
                "hesapla": lambda: (random.randint(5, 20), random.randint(2, 10)),
                "cozum": lambda v, t: v * t,
                "dogru": 1,
            },
        ],
        "Zor": [
            {
                "tip": "analiz",
                "metin": "Bir devre elemani uzerinden 2A akim geciyor ve elemandaki gerilim 12V ise, elemanin direnci kac ohm'dur? (R=V/I)",
                "secenekler": ["4 ohm", "6 ohm", "24 ohm", "14 ohm"],
                "dogru": 1,
            },
        ],
    },
    "Sosyal": {
        "Kolay": [
            {
                "tip": "bilgi",
                "metin": "Turkiye Cumhuriyeti hangi yil ilan edilmistir?",
                "secenekler": ["1919", "1920", "1923", "1938"],
                "dogru": 2,
            },
        ],
        "Orta": [
            {
                "tip": "analiz",
                "metin": "Asagidakilerden hangisi Ataturk ilkelerinden biri degildir?",
                "secenekler": ["Cumhuriyetcilik", "Milliyetcilik", "Federalizm", "Laiklik"],
                "dogru": 2,
            },
        ],
        "Zor": [
            {
                "tip": "yorum",
                "metin": "'Yurtta sulh, cihanda sulh' sozunun anlami nedir?",
                "secenekler": [
                    "Savas her zaman gereklidir",
                    "Ulke icinde ve disinda baris onemlidir",
                    "Sadece ic baris yeterlidir",
                    "Dis politika onemsizdir"
                ],
                "dogru": 1,
            },
        ],
    },
    "Ingilizce": {
        "Kolay": [
            {
                "tip": "gramer",
                "metin": "She ___ to school every day.",
                "secenekler": ["go", "goes", "going", "gone"],
                "dogru": 1,
            },
        ],
        "Orta": [
            {
                "tip": "kelime",
                "metin": "What is the opposite of 'happy'?",
                "secenekler": ["Angry", "Sad", "Excited", "Tired"],
                "dogru": 1,
            },
        ],
        "Zor": [
            {
                "tip": "okuma",
                "metin": """John woke up late yesterday. He missed his bus and had to walk to school.

According to the text, why did John walk to school?""",
                "secenekler": [
                    "He likes walking",
                    "He missed the bus",
                    "The bus was broken",
                    "His mother told him"
                ],
                "dogru": 1,
            },
        ],
    },
}


# ============================================================
# GORSEL URETICI
# ============================================================

class GorselUretici:
    """Matplotlib ile gorsel soru olusturur."""

    @staticmethod
    def _get_plt():
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        return plt

    @staticmethod
    def grafik_soru() -> dict:
        """Cubuk grafik sorusu olustur."""
        plt = GorselUretici._get_plt()

        gunler = ['Pzt', 'Sal', 'Car', 'Per', 'Cum']
        satislar = [random.randint(20, 80) for _ in range(5)]

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        renkler = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        bars = ax.bar(gunler, satislar, color=renkler)

        for bar, val in zip(bars, satislar):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                   str(val), ha='center', fontsize=10)

        ax.set_ylabel('Satis Adedi')
        ax.set_title('Haftalık Satis Grafigi')
        ax.set_ylim(0, max(satislar) + 15)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)

        toplam = sum(satislar)
        maks_gun = gunler[satislar.index(max(satislar))]

        soru_tipi = random.choice(['toplam', 'maksimum', 'fark'])

        if soru_tipi == 'toplam':
            soru = "Grafige gore haftalik toplam satis kac adettir?"
            dogru = toplam
            secenekler = [toplam - 15, toplam, toplam + 10, toplam + 25]
        elif soru_tipi == 'maksimum':
            soru = "En cok satis hangi gun yapilmistir?"
            secenekler = gunler.copy()
            random.shuffle(secenekler)
            dogru_idx = secenekler.index(maks_gun)
            return {
                "metin": soru,
                "secenekler": secenekler,
                "dogru": dogru_idx,
                "gorsel": buf.getvalue(),
                "ders": "Matematik",
                "zorluk": "Orta",
            }
        else:
            fark = max(satislar) - min(satislar)
            soru = "En cok ve en az satis yapilan gunler arasindaki fark kac adettir?"
            dogru = fark
            secenekler = [fark - 5, fark, fark + 8, fark + 15]

        return {
            "metin": soru,
            "secenekler": [str(s) for s in secenekler],
            "dogru": 1,
            "gorsel": buf.getvalue(),
            "ders": "Matematik",
            "zorluk": "Orta",
        }

    @staticmethod
    def geometri_soru() -> dict:
        """Geometri sekil sorusu."""
        plt = GorselUretici._get_plt()

        sekil_tipi = random.choice(['ucgen', 'dikdortgen', 'kare', 'daire'])

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        if sekil_tipi == 'ucgen':
            a = random.randint(4, 10)
            b = random.randint(4, 10)
            c = random.randint(max(abs(a-b)+1, 4), min(a+b-1, 12))

            from matplotlib.patches import Polygon
            points = [(0, 0), (a, 0), (a/2, b*0.8)]
            triangle = Polygon(points, fill=False, edgecolor='#2980b9', linewidth=2)
            ax.add_patch(triangle)

            ax.text(a/2, -0.5, f'{a} cm', ha='center', fontsize=11)
            ax.text(a + 0.3, b*0.4, f'{b} cm', ha='left', fontsize=11)
            ax.text(-0.3, b*0.4, f'{c} cm', ha='right', fontsize=11)

            ax.set_xlim(-2, a+3)
            ax.set_ylim(-1.5, b+1)

            cevre = a + b + c
            soru = "Sekildeki ucgenin cevresi kac cm'dir?"
            secenekler = [cevre - 3, cevre, cevre + 2, cevre + 5]

        elif sekil_tipi == 'dikdortgen':
            uzun = random.randint(6, 12)
            kisa = random.randint(3, 6)

            from matplotlib.patches import Rectangle
            rect = Rectangle((1, 1), uzun/2, kisa/2, fill=False, edgecolor='#27ae60', linewidth=2)
            ax.add_patch(rect)

            ax.text(1 + uzun/4, 0.5, f'{uzun} cm', ha='center', fontsize=11)
            ax.text(1 + uzun/2 + 0.3, 1 + kisa/4, f'{kisa} cm', ha='left', fontsize=11)

            ax.set_xlim(0, uzun/2 + 3)
            ax.set_ylim(0, kisa/2 + 3)

            alan = uzun * kisa
            soru = "Sekildeki dikdortgenin alani kac cm²'dir?"
            secenekler = [alan - kisa, alan, alan + uzun, 2*(uzun+kisa)]

        elif sekil_tipi == 'kare':
            kenar = random.randint(4, 10)

            from matplotlib.patches import Rectangle
            rect = Rectangle((1, 1), kenar/2, kenar/2, fill=False, edgecolor='#8e44ad', linewidth=2)
            ax.add_patch(rect)

            ax.text(1 + kenar/4, 0.5, f'{kenar} cm', ha='center', fontsize=11)

            ax.set_xlim(0, kenar/2 + 3)
            ax.set_ylim(0, kenar/2 + 3)

            cevre = 4 * kenar
            soru = "Sekildeki karenin cevresi kac cm'dir?"
            secenekler = [cevre - 4, cevre, cevre + 4, kenar * kenar]

        else:  # daire
            yaricap = random.randint(3, 8)

            from matplotlib.patches import Circle
            circle = Circle((3, 3), yaricap/2, fill=False, edgecolor='#e74c3c', linewidth=2)
            ax.add_patch(circle)

            ax.plot([3, 3 + yaricap/2], [3, 3], 'k-', linewidth=1)
            ax.text(3 + yaricap/4, 3.3, f'r={yaricap} cm', fontsize=11)

            ax.set_xlim(0, 7)
            ax.set_ylim(0, 7)

            cap = 2 * yaricap
            soru = "Sekildeki dairenin capi kac cm'dir?"
            secenekler = [yaricap, cap, cap + 2, yaricap * 3]

        ax.set_aspect('equal')
        ax.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)

        return {
            "metin": soru,
            "secenekler": [str(s) for s in secenekler],
            "dogru": 1,
            "gorsel": buf.getvalue(),
            "ders": "Matematik",
            "zorluk": "Orta",
        }

    @staticmethod
    def tablo_soru() -> dict:
        """Tablo analiz sorusu."""
        plt = GorselUretici._get_plt()

        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.axis('off')

        tablo_tipi = random.choice(['not', 'satis', 'nufus'])

        if tablo_tipi == 'not':
            basliklar = ['Öğrenci', 'Matematik', 'Turkce', 'Fen']
            ogrenciler = ['Ali', 'Ayse', 'Mehmet', 'Zeynep']
            veriler = [[random.randint(60, 100) for _ in range(3)] for _ in range(4)]
            data = [[ogrenciler[i]] + [str(v) for v in veriler[i]] for i in range(4)]
            data.insert(0, basliklar)

            # En yuksek ortalama
            ortalamalar = [sum(v)/3 for v in veriler]
            en_yuksek = ogrenciler[ortalamalar.index(max(ortalamalar))]

            soru = "Tabloya gore en yuksek not ortalamasina sahip ogrenci kimdir?"
            secenekler = ogrenciler.copy()
            random.shuffle(secenekler)
            dogru_idx = secenekler.index(en_yuksek)

        elif tablo_tipi == 'satis':
            basliklar = ['Urun', 'Fiyat (TL)', 'Satis']
            urunler = ['Kalem', 'Defter', 'Silgi', 'Cetvel']
            fiyatlar = [5, 15, 3, 8]
            satislar = [random.randint(10, 50) for _ in range(4)]
            data = [[urunler[i], str(fiyatlar[i]), str(satislar[i])] for i in range(4)]
            data.insert(0, basliklar)

            toplam_gelir = sum(f * s for f, s in zip(fiyatlar, satislar))
            soru = "Tabloya gore toplam satis geliri kac TL'dir?"
            secenekler = [str(toplam_gelir - 50), str(toplam_gelir), str(toplam_gelir + 30), str(sum(satislar))]
            dogru_idx = 1

        else:
            basliklar = ['Sehir', 'Nufus (bin)', 'Alan (km²)']
            sehirler = ['Ankara', 'Izmir', 'Bursa', 'Antalya']
            nufuslar = [5700, 4400, 3100, 2500]
            alanlar = [25600, 12000, 10800, 20700]
            data = [[sehirler[i], str(nufuslar[i]), str(alanlar[i])] for i in range(4)]
            data.insert(0, basliklar)

            soru = "Tabloya gore en kalabalik sehir hangisidir?"
            secenekler = sehirler.copy()
            dogru_idx = 0

        table = ax.table(cellText=data, loc='center', cellLoc='center',
                        colWidths=[0.3] * len(data[0]))
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.8)

        for j in range(len(data[0])):
            table[(0, j)].set_facecolor('#3498db')
            table[(0, j)].set_text_props(color='white', fontweight='bold')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)

        return {
            "metin": soru,
            "secenekler": secenekler,
            "dogru": dogru_idx,
            "gorsel": buf.getvalue(),
            "ders": "Matematik",
            "zorluk": "Orta",
        }

    @staticmethod
    def fizik_grafik() -> dict:
        """Fizik hiz-zaman grafigi."""
        plt = GorselUretici._get_plt()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

        # Farkli hareket turleri
        hareket = random.choice(['sabit', 'ivmeli', 'duraklamali'])

        if hareket == 'sabit':
            t = list(range(0, 7))
            v = [20] * 7
            soru = "Grafikteki cismin 6 saniyede aldigi yol kac metredir?"
            cevap = 20 * 6  # 120
            secenekler = ['100 m', '120 m', '140 m', '20 m']
            dogru = 1

        elif hareket == 'ivmeli':
            t = list(range(0, 6))
            v = [0, 10, 20, 30, 40, 50]
            soru = "Grafikteki cismin ivmesi kac m/s²'dir?"
            cevap = 10
            secenekler = ['5 m/s²', '10 m/s²', '20 m/s²', '50 m/s²']
            dogru = 1

        else:
            t = list(range(0, 8))
            v = [0, 15, 30, 30, 30, 20, 10, 0]
            soru = "Cisim hangi zaman araliginda sabit hizla hareket etmistir?"
            secenekler = ['0-2 s', '2-4 s', '4-6 s', '6-7 s']
            dogru = 1

        ax.plot(t, v, 'b-o', linewidth=2, markersize=6)
        ax.fill_between(t, v, alpha=0.3)
        ax.set_xlabel('Zaman (s)', fontsize=11)
        ax.set_ylabel('Hiz (m/s)', fontsize=11)
        ax.set_title('Hiz-Zaman Grafigi')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max(t))
        ax.set_ylim(0, max(v) + 10)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)

        return {
            "metin": soru,
            "secenekler": secenekler,
            "dogru": dogru,
            "gorsel": buf.getvalue(),
            "ders": "Fen",
            "zorluk": "Orta",
        }

    @staticmethod
    def pasta_grafik() -> dict:
        """Pasta grafik sorusu."""
        plt = GorselUretici._get_plt()

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

        kategoriler = ['Matematik', 'Turkce', 'Fen', 'Sosyal']
        degerler = [random.randint(15, 35) for _ in range(4)]
        # Toplam 100 yap
        toplam = sum(degerler)
        degerler = [int(d * 100 / toplam) for d in degerler]
        degerler[-1] = 100 - sum(degerler[:-1])  # Yuvarlama duzeltme

        renkler = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        ax.pie(degerler, labels=kategoriler, colors=renkler, autopct='%1.0f%%',
               startangle=90, textprops={'fontsize': 10})
        ax.set_title('Öğrenci Ders Tercihleri')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)

        # Soru olustur
        hedef_idx = random.randint(0, 3)
        hedef_ders = kategoriler[hedef_idx]
        hedef_oran = degerler[hedef_idx]
        toplam_ogrenci = random.choice([100, 200, 500])
        ogrenci_sayisi = toplam_ogrenci * hedef_oran // 100

        soru = f"Toplam {toplam_ogrenci} ogrenci ankete katilmistir. {hedef_ders} dersini tercih eden kac ogrenci vardir?"
        secenekler = [str(ogrenci_sayisi - 10), str(ogrenci_sayisi), str(ogrenci_sayisi + 15), str(hedef_oran)]

        return {
            "metin": soru,
            "secenekler": secenekler,
            "dogru": 1,
            "gorsel": buf.getvalue(),
            "ders": "Matematik",
            "zorluk": "Kolay",
        }


# ============================================================
# SORU URETICI
# ============================================================

class SoruUretici:
    """Soru bankasi ve gorsellerden soru uretir."""

    def __init__(self, sinav_turu: str = "Deneme"):
        self.sinav_turu = sinav_turu
        self.config = SINAV_TURLERI.get(sinav_turu, SINAV_TURLERI["Deneme"])
        self.kullanilan_sorular: set = set()

    def soru_uret(self, ders: str, zorluk: str = "Orta") -> dict:
        """Bir soru uret."""
        gorsel_orani = self.config["gorsel_oran"]

        # Gorsel soru mu?
        if random.random() < gorsel_orani:
            gorsel_soru = self._gorsel_soru_uret(ders, zorluk)
            if gorsel_soru:
                return gorsel_soru

        # Metin soru
        return self._metin_soru_uret(ders, zorluk)

    def _gorsel_soru_uret(self, ders: str, zorluk: str) -> Optional[dict]:
        """Gorsel soru uret."""
        try:
            if ders == "Matematik":
                secim = random.choice(['grafik', 'geometri', 'tablo', 'pasta'])
                if secim == 'grafik':
                    return GorselUretici.grafik_soru()
                elif secim == 'geometri':
                    return GorselUretici.geometri_soru()
                elif secim == 'tablo':
                    return GorselUretici.tablo_soru()
                else:
                    return GorselUretici.pasta_grafik()
            elif ders == "Fen":
                return GorselUretici.fizik_grafik()
            else:
                # Diger dersler için tablo kullan
                soru = GorselUretici.tablo_soru()
                soru["ders"] = ders
                return soru
        except Exception as e:
            print(f"Gorsel soru hatasi: {e}")
            return None

    def _metin_soru_uret(self, ders: str, zorluk: str) -> dict:
        """Metin tabanli soru uret."""
        ders_sorulari = SORU_BANKASI.get(ders, SORU_BANKASI["Matematik"])
        zorluk_sorulari = ders_sorulari.get(zorluk, ders_sorulari.get("Orta", []))

        if not zorluk_sorulari:
            zorluk_sorulari = list(ders_sorulari.values())[0]

        sablon = random.choice(zorluk_sorulari)

        # Soru tipine gore islem
        if "sablon" in sablon:
            # Dinamik soru
            if "hesapla" in sablon:
                params = sablon["hesapla"]()
                if isinstance(params, tuple):
                    metin = sablon["sablon"].format(*params) if len(params) <= 2 else sablon["sablon"]
                    cevap = sablon["cozum"](*params)
                else:
                    a, b = random.randint(5, 20), random.randint(3, 15)
                    metin = sablon["sablon"].format(a=a, b=b)
                    cevap = sablon["cozum"](a, b)
            else:
                a = random.randint(5, 20)
                b = random.randint(3, 15)
                metin = sablon["sablon"].format(a=a, b=b)
                cevap = sablon["cozum"](a, b)

            # Celdirici olustur
            if "celdirici" in sablon:
                try:
                    secenekler = sablon["celdirici"](cevap)
                except Exception:
                    secenekler = [cevap - 2, cevap, cevap + 3, cevap + 5]
            else:
                secenekler = [cevap - 2, cevap, cevap + 3, cevap + 5]

            secenekler = [str(s) for s in secenekler]
            dogru = sablon.get("dogru", 1)

        else:
            # Statik soru
            metin = sablon["metin"]
            secenekler = sablon["secenekler"]
            dogru = sablon["dogru"]

        return {
            "metin": metin,
            "secenekler": secenekler,
            "dogru": dogru,
            "ders": ders,
            "zorluk": zorluk,
        }


# ============================================================
# SINAV MOTORU
# ============================================================

class SinavMotoru:
    """Sinav olusturma ve yonetim."""

    def __init__(self, sinav_turu: str = "Deneme"):
        self.sinav_turu = sinav_turu
        self.uretici = SoruUretici(sinav_turu)

    def sinav_olustur(
        self,
        sinav_adi: str,
        ders_sayilari: dict,
        zorluk: str = "Orta",
        sinif: int = 9,
        sube: str = "A"
    ) -> dict:
        """Sinav olustur."""
        sorular = []
        soru_no = 1

        for ders, sayi in ders_sayilari.items():
            for _ in range(sayi):
                # Zorluk dagilimi
                if zorluk == "Karisik":
                    secilen_zorluk = random.choice(["Kolay", "Orta", "Zor"])
                else:
                    secilen_zorluk = zorluk

                soru = self.uretici.soru_uret(ders, secilen_zorluk)
                soru["numara"] = soru_no
                sorular.append(soru)
                soru_no += 1

        # Sorulari karistir
        random.shuffle(sorular)
        for i, s in enumerate(sorular, 1):
            s["numara"] = i

        # Sinav kodu
        kod = hashlib.md5(f"{sinav_adi}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()

        return {
            "kod": kod,
            "ad": sinav_adi,
            "tur": self.sinav_turu,
            "sinif": sinif,
            "sube": sube,
            "tarih": datetime.now().strftime("%d.%m.%Y"),
            "sorular": sorular,
            "toplam_soru": len(sorular),
            "ders_dagilimi": ders_sayilari,
        }


# ============================================================
# STREAMLIT ARAYUZU
# ============================================================

def render_sinav_olusturucu():
    """Ana arayuz."""
    inject_common_css("so")
    styled_header("Sinav Olusturucu", "MEB/OSYM formatinda profesyonel sinav hazirlama", icon="📝")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("sinav_olusturucu_egitim_yili")

    # Session state
    if "sinav_sonuc" not in st.session_state:
        st.session_state.sinav_sonuc = None

    # ===== 1. SINAV TURU =====
    st.markdown("### 1️⃣ Sınav Türü")

    col1, col2 = st.columns([2, 3])

    with col1:
        sinav_turu = st.selectbox(
            "Sınav Formatı",
            list(SINAV_TURLERI.keys()),
            format_func=lambda x: f"{x} - {SINAV_TURLERI[x]['ad']}"
        )

    with col2:
        config = SINAV_TURLERI[sinav_turu]
        gorsel_oran = int(config["gorsel_oran"] * 100)
        st.info(f"**{config['ad']}** | Görsel oran: %{gorsel_oran} | {config['sik']} şıklı sorular")

    # ===== 2. SINIF BILGILERI =====
    st.markdown("### 2️⃣ Sınıf Bilgileri")

    col1, col2, col3 = st.columns(3)

    with col1:
        sinif = st.selectbox("Sınıf", list(range(5, 13)), index=4)

    with col2:
        sube = st.selectbox("Şube", ["A", "B", "C", "D", "E"])

    with col3:
        sinav_adi = st.text_input("Sınav Adı", f"{sinav_turu} Deneme - {datetime.now().strftime('%d.%m.%Y')}")


    # ===== 3. DERS VE SORU SAYILARI =====
    st.markdown("### 3️⃣ Ders ve Soru Sayıları")

    # Hizli secim
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📐 Sayısal", use_container_width=True):

            st.session_state.secili_dersler = ["Matematik", "Fen"]
    with col2:
        if st.button("📖 Sözel", use_container_width=True):

            st.session_state.secili_dersler = ["Turkce", "Sosyal"]
    with col3:
        if st.button("🌐 Tümü", use_container_width=True):

            st.session_state.secili_dersler = list(DERSLER.keys())

    secili_dersler = st.multiselect(
        "Dersler",
        list(DERSLER.keys()),
        default=st.session_state.get("secili_dersler", ["Matematik", "Turkce"])
    )
    st.session_state.secili_dersler = secili_dersler

    # Soru sayilari
    ders_sayilari = {}
    if secili_dersler:
        st.markdown("**Soru Sayıları:**")
        cols = st.columns(min(len(secili_dersler), 5))
        for i, ders in enumerate(secili_dersler):
            with cols[i % 5]:
                info = DERSLER[ders]
                ders_sayilari[ders] = st.number_input(
                    f"{info['ikon']} {ders}",
                    min_value=0,
                    max_value=30,
                    value=5,
                    key=f"sayi_{ders}"
                )

    # Zorluk
    col1, col2 = st.columns(2)
    with col1:
        zorluk = st.select_slider(
            "Zorluk Seviyesi",
            options=["Kolay", "Orta", "Zor", "Karisik"],
            value="Orta"
        )
    with col2:
        toplam = sum(ders_sayilari.values())
        st.metric("Toplam Soru", toplam)

    # ===== 4. OLUSTUR =====
    st.markdown("### 4️⃣ Sınavı Oluştur")

    if st.button("🚀 **SINAV OLUŞTUR**", type="primary", use_container_width=True, disabled=toplam == 0):

        with st.spinner("Sınav hazırlanıyor..."):
            motor = SinavMotoru(sinav_turu)
            sinav = motor.sinav_olustur(
                sinav_adi=sinav_adi,
                ders_sayilari=ders_sayilari,
                zorluk=zorluk,
                sinif=sinif,
                sube=sube
            )
            st.session_state.sinav_sonuc = sinav
        st.success(f"✅ Sınav oluşturuldu! Kod: **{sinav['kod']}** | {sinav['toplam_soru']} soru")
        st.rerun()

    # ===== SONUC =====
    if st.session_state.sinav_sonuc:
        sinav = st.session_state.sinav_sonuc

        st.markdown("---")
        st.markdown(f"### 📋 {sinav['ad']}")
        st.caption(f"Kod: {sinav['kod']} | {sinav['sinif']}/{sinav['sube']} | {sinav['tarih']}")

        # Istatistikler
        gorsel_sayisi = sum(1 for s in sinav["sorular"] if s.get("gorsel"))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Toplam", sinav["toplam_soru"])
        col2.metric("Görsel", gorsel_sayisi)
        col3.metric("Metin", sinav["toplam_soru"] - gorsel_sayisi)
        col4.metric("Tür", sinav["tur"])

        # Sorular
        st.markdown("#### Sorular")

        for soru in sinav["sorular"]:
            gorsel_etiket = " 📊" if soru.get("gorsel") else ""
            with st.expander(f"Soru {soru['numara']} - {soru['ders']} ({soru['zorluk']}){gorsel_etiket}"):

                # Gorsel varsa goster
                if soru.get("gorsel"):
                    st.image(soru["gorsel"], use_container_width=True)

                st.markdown(f"**{soru['metin']}**")
                st.markdown("")

                for i, secenek in enumerate(soru["secenekler"]):
                    harf = chr(65 + i)
                    if i == soru["dogru"]:
                        st.markdown(f"**{harf})** {secenek} ✓")
                    else:
                        st.markdown(f"{harf}) {secenek}")

        # Indirme
        st.markdown("---")
        st.markdown("#### 📥 İndir")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # PDF Soru - Cevapsiz
            pdf_soru = _sinav_pdf_olustur(sinav, cevap_goster=False)
            st.download_button(
                "📕 PDF Soru",
                pdf_soru,
                file_name=f"{sinav['kod']}_soru.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:
            # PDF Cevap Anahtarli
            pdf_cevap = _sinav_pdf_olustur(sinav, cevap_goster=True)
            st.download_button(
                "📗 PDF Cevaplı",
                pdf_cevap,
                file_name=f"{sinav['kod']}_cevapli.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col3:
            # TXT indir
            txt_icerik = _sinav_txt_olustur(sinav)
            st.download_button(
                "📄 TXT",
                txt_icerik,
                file_name=f"{sinav['kod']}_sinav.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col4:
            if st.button("🗑️ Temizle", use_container_width=True):

                st.session_state.sinav_sonuc = None
                st.rerun()


def _sinav_pdf_olustur(sinav: dict, cevap_goster: bool = False) -> bytes:
    """Sinavi PDF formatinda olustur."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        # reportlab yoksa basit PDF olustur
        return _sinav_pdf_basit(sinav, cevap_goster)

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                           leftMargin=2*cm, rightMargin=2*cm)

    styles = getSampleStyleSheet()

    # Ozel stiller
    styles.add(ParagraphStyle(
        name='Başlık',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName=font_bold
    ))

    styles.add(ParagraphStyle(
        name='AltBaşlık',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.grey,
        fontName=font_name
    ))

    styles.add(ParagraphStyle(
        name='SoruNo',
        fontSize=11,
        leading=14,
        fontName=font_bold,
        spaceBefore=15,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='SoruMetin',
        fontSize=10,
        leading=14,
        spaceAfter=8,
        fontName=font_name
    ))

    styles.add(ParagraphStyle(
        name='Secenek',
        fontSize=10,
        leading=13,
        leftIndent=20,
        fontName=font_name
    ))

    elements = []

    # Baslik
    elements.append(Paragraph(sinav['ad'], styles['Başlık']))
    elements.append(Paragraph(
        f"Kod: {sinav['kod']} | Sınıf: {sinav['sinif']}/{sinav['sube']} | Tarih: {sinav['tarih']} | Toplam: {sinav['toplam_soru']} Soru",
        styles['AltBaşlık']
    ))
    elements.append(Spacer(1, 0.5*cm))

    # Ders dagilimi tablosu
    ders_data = [['Ders', 'Soru Sayısı']]
    for ders, sayi in sinav['ders_dagilimi'].items():
        if sayi > 0:
            ders_data.append([ders, str(sayi)])

    if len(ders_data) > 1:
        ders_table = Table(ders_data, colWidths=[8*cm, 4*cm])
        ders_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), font_bold),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(ders_table)
        elements.append(Spacer(1, 1*cm))

    # Sorular
    for soru in sinav['sorular']:
        # Soru numarasi ve ders
        elements.append(Paragraph(
            f"<b>Soru {soru['numara']}</b> ({soru['ders']} - {soru['zorluk']})",
            styles['SoruNo']
        ))

        # Gorsel varsa ekle
        if soru.get('gorsel'):
            try:
                img_buffer = io.BytesIO(soru['gorsel'])
                img = Image(img_buffer, width=12*cm, height=8*cm)
                img.hAlign = 'CENTER'
                elements.append(img)
                elements.append(Spacer(1, 0.3*cm))
            except Exception:
                elements.append(Paragraph("[Görsel yüklenemedi]", styles['SoruMetin']))

        # Soru metni
        elements.append(Paragraph(soru['metin'], styles['SoruMetin']))

        # Secenekler
        for i, secenek in enumerate(soru['secenekler']):
            harf = chr(65 + i)
            if cevap_goster and i == soru['dogru']:
                elements.append(Paragraph(f"<b>{harf})</b> {secenek} ✓", styles['Secenek']))
            else:
                elements.append(Paragraph(f"{harf}) {secenek}", styles['Secenek']))

        elements.append(Spacer(1, 0.3*cm))

    # Cevap anahtari sayfasi
    if not cevap_goster:
        elements.append(PageBreak())
        elements.append(Paragraph("CEVAP ANAHTARI", styles['Başlık']))
        elements.append(Spacer(1, 0.5*cm))

        # Cevaplar tablosu
        cevap_data = []
        row = []
        for i, soru in enumerate(sinav['sorular']):
            dogru_harf = chr(65 + soru['dogru'])
            row.append(f"{soru['numara']}. {dogru_harf}")
            if len(row) == 5:
                cevap_data.append(row)
                row = []
        if row:
            while len(row) < 5:
                row.append('')
            cevap_data.append(row)

        if cevap_data:
            cevap_table = Table(cevap_data, colWidths=[3*cm]*5)
            cevap_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(cevap_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def _sinav_pdf_basit(sinav: dict, cevap_goster: bool = False) -> bytes:
    """reportlab olmadan basit PDF olustur (FPDF ile)."""
    try:
        from fpdf import FPDF
    except ImportError:
        # FPDF de yoksa TXT dondur
        return _sinav_txt_olustur(sinav).encode('utf-8')

    pdf = FPDF()

    # DejaVuSans font ekle (Turkce karakter destegi)
    _fpdf_font = "Helvetica"
    try:
        deja_path = os.path.join("assets", "DejaVuSans.ttf")
        deja_bold_path = os.path.join("assets", "DejaVuSans-Bold.ttf")
        if os.path.exists(deja_path):
            pdf.add_font("DejaVu", "", deja_path)
            if os.path.exists(deja_bold_path):
                pdf.add_font("DejaVu", "B", deja_bold_path)
            _fpdf_font = "DejaVu"
    except Exception:
        _fpdf_font = "Helvetica"

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Baslik
    pdf.set_font(_fpdf_font, 'B', 16)
    pdf.cell(0, 10, sinav['ad'], ln=True, align='C')

    pdf.set_font(_fpdf_font, '', 10)
    pdf.cell(0, 8, f"Kod: {sinav['kod']} | Sınıf: {sinav['sinif']}/{sinav['sube']} | Tarih: {sinav['tarih']}", ln=True, align='C')
    pdf.ln(10)

    # Sorular
    for soru in sinav['sorular']:
        pdf.set_font(_fpdf_font, 'B', 11)
        pdf.cell(0, 8, f"Soru {soru['numara']} ({soru['ders']})", ln=True)

        if soru.get('gorsel'):
            try:
                img_buffer = io.BytesIO(soru['gorsel'])
                pdf.image(img_buffer, x=30, w=150)
                pdf.ln(5)
            except Exception:
                pdf.set_font(_fpdf_font, '', 9)
                pdf.cell(0, 6, "[Gorsel]", ln=True)

        pdf.set_font(_fpdf_font, '', 10)
        pdf.multi_cell(0, 6, soru['metin'])
        pdf.ln(3)

        for i, secenek in enumerate(soru['secenekler']):
            harf = chr(65 + i)
            if cevap_goster and i == soru['dogru']:
                pdf.set_font(_fpdf_font, 'B', 10)
                pdf.cell(0, 6, f"  {harf}) {secenek} *", ln=True)
            else:
                pdf.set_font(_fpdf_font, '', 10)
                pdf.cell(0, 6, f"  {harf}) {secenek}", ln=True)

        pdf.ln(5)

    # Cevap anahtari
    if not cevap_goster:
        pdf.add_page()
        pdf.set_font(_fpdf_font, 'B', 14)
        pdf.cell(0, 10, "CEVAP ANAHTARI", ln=True, align='C')
        pdf.ln(5)

        pdf.set_font(_fpdf_font, '', 11)
        cevaplar = []
        for soru in sinav['sorular']:
            dogru_harf = chr(65 + soru['dogru'])
            cevaplar.append(f"{soru['numara']}. {dogru_harf}")

        # 5'li gruplar halinde yaz
        for i in range(0, len(cevaplar), 5):
            satir = "   ".join(cevaplar[i:i+5])
            pdf.cell(0, 8, satir, ln=True, align='C')

    return bytes(pdf.output())


def _sinav_txt_olustur(sinav: dict) -> str:
    """Sinavi TXT formatina cevir."""
    lines = [
        f"{'='*60}",
        f"{sinav['ad']}",
        f"{'='*60}",
        f"Kod: {sinav['kod']}",
        f"Sınıf: {sinav['sinif']}/{sinav['sube']}",
        f"Tarih: {sinav['tarih']}",
        f"Toplam Soru: {sinav['toplam_soru']}",
        f"{'='*60}",
        ""
    ]

    for soru in sinav["sorular"]:
        gorsel_notu = " [GÖRSEL SORU]" if soru.get("gorsel") else ""
        lines.append(f"SORU {soru['numara']}: ({soru['ders']}){gorsel_notu}")
        if soru.get("gorsel"):
            lines.append("[Bu soruda görsel/grafik bulunmaktadır]")
        lines.append(soru["metin"])
        lines.append("")

        for i, secenek in enumerate(soru["secenekler"]):
            harf = chr(65 + i)
            lines.append(f"   {harf}) {secenek}")

        lines.append("")
        lines.append("-" * 40)
        lines.append("")

    # Cevap anahtari
    lines.append("")
    lines.append("CEVAP ANAHTARI")
    lines.append("-" * 20)

    for soru in sinav["sorular"]:
        dogru_harf = chr(65 + soru["dogru"])
        lines.append(f"{soru['numara']}. {dogru_harf}")

    return "\n".join(lines)


# Ana cagri
if __name__ == "__main__":
    render_sinav_olusturucu()
