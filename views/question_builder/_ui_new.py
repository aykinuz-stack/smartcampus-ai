"""
Soru Olusturma - Yeni Basit ve Calisan Arayuz
=============================================
Kullanici dostu, basit ve calisan soru olusturma modulu.
AI destekli (OpenAI + Anthropic) ve rule-based soru uretimi.
"""

from __future__ import annotations

import os
import random
import hashlib
import json
from datetime import datetime
import streamlit as st

# OpenAI icin
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Anthropic icin
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# PDF okuma icin
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

PDF_AVAILABLE = PYMUPDF_AVAILABLE or PDFPLUMBER_AVAILABLE


# ==================== AI YAPILANDIRMASI ====================

# Ders bazli konu havuzu (AI icin)
DERS_KONULARI = {
    "Matematik": {
        9: ["Kümeler", "Mantık", "Bağıntı ve Fonksiyon", "Sayılar", "Polinomlar", "Denklemler"],
        10: ["Fonksiyonlar", "Polinomlar", "2. Derece Denklemler", "Permütasyon", "Kombinasyon", "Olasılık"],
        11: ["Trigonometri", "Analitik Geometri", "Diziler", "Logaritma", "Limit"],
        12: ["Türev", "İntegral", "Limit ve Süreklilik", "Türev Uygulamaları"],
    },
    "Fizik": {
        9: ["Fizik Bilimine Giriş", "Madde ve Özellikleri", "Hareket ve Kuvvet", "Enerji"],
        10: ["Basınç", "Kaldırma Kuvveti", "Elektrik", "Manyetizma"],
        11: ["Kuvvet ve Hareket", "Elektrik ve Manyetizma", "Dalgalar", "Optik"],
        12: ["Çembersel Hareket", "Basit Harmonik Hareket", "Dalga Mekaniği", "Atom Fiziği", "Modern Fizik"],
    },
    "Kimya": {
        9: ["Kimya Bilimi", "Atom ve Periyodik Sistem", "Kimyasal Türler Arası Etkileşimler", "Maddenin Halleri"],
        10: ["Kimyasal Hesaplamalar", "Karışımlar", "Asitler ve Bazlar", "Kimya Her Yerde"],
        11: ["Modern Atom Teorisi", "Gazlar", "Sıvı Çözeltiler", "Kimyasal Tepkimeler"],
        12: ["Kimyasal Tepkimelerde Enerji", "Tepkime Hızları", "Kimyasal Denge", "Organik Kimya"],
    },
    "Biyoloji": {
        9: ["Canlıların Ortak Özellikleri", "Canlıların Temel Bileşenleri", "Hücre", "Canlılar Dünyası"],
        10: ["Hücre Bölünmeleri", "Kalıtım", "Ekosistem Ekolojisi", "Güncel Çevre Sorunları"],
        11: ["İnsan Fizyolojisi", "Komünite ve Popülasyon Ekolojisi"],
        12: ["Genden Proteine", "Canlılarda Enerji Dönüşümleri", "Bitki Biyolojisi"],
    },
    "Tarih": {
        9: ["Tarih Bilimi", "İlk Çağ Uygarlıkları", "Türklerin İslamiyeti Kabulü", "Türk-İslam Devletleri"],
        10: ["Beylikten Devlete", "Dünya Gücü Osmanlı", "Sultan ve Osmanlı Merkez Teşkilatı"],
        11: ["Değişen Dünya Dengeleri", "Uluslararası İlişkilerde Denge Stratejisi", "Devrimler Çağı"],
        12: ["XX. Yüzyıl Başlarında Osmanlı", "Milli Mücadele", "Atatürk İlke ve İnkılapları"],
    },
    "Cografya": {
        9: ["Doğa ve İnsan", "Dünya'nın Şekli ve Hareketleri", "Coğrafi Konum", "Harita Bilgisi"],
        10: ["Ekosistem", "Nüfus", "Göç", "Yerleşme", "Türkiye'nin Yer Şekilleri"],
        11: ["Doğal Sistemler", "Beşeri Sistemler", "Küresel Ortam", "Çevre ve Toplum"],
        12: ["Türkiye'nin Jeopolitik Konumu", "Ülkeler", "Türkiye'de Bölgeler"],
    },
    "Turkce": {
        9: ["Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam", "Ses Bilgisi", "Yazım Kuralları"],
        10: ["Anlam Bilgisi", "Söz Sanatları", "Paragraf", "Dil Bilgisi", "Noktalama"],
        11: ["Paragraf Çözümleme", "Anlatım Bozuklukları", "Sözcük Türleri"],
        12: ["Paragraf", "Anlam Bilgisi", "Dil Bilgisi", "Yazım ve Noktalama"],
    },
    "Ingilizce": {
        9: ["Greetings", "Daily Routines", "Movies", "Human Relations", "Helpful Tips"],
        10: ["School Life", "Plans", "Legendary Figures", "Traditions", "Travel"],
        11: ["Future Jobs", "Hobbies", "Hard Times", "What a Life", "Back to the Past"],
        12: ["Music", "Friendship", "Human Rights", "Coming Soon", "Psychology"],
    },
}

# ==================== GELISMIS AI PROMPT SISTEMI ====================

# ==================== SINAV TIPLERI (MEB/OSYM) ====================

SINAV_TIPLERI = {
    "LGS": {
        "name": "Liselere Geçiş Sınavı",
        "grade_range": [8],
        "description": "8. sınıf öğrencileri için merkezi sınav",
        "visual_ratio": 0.70,  # Soruların %70'i görsel içermeli
        "paragraph_required": True,  # Paragraf/bağlam zorunlu
        "question_style": """
LGS SORU FORMATI:
- Her soru mutlaka bir bağlam/senaryo ile başlamalı
- Günlük hayattan örnekler kullanılmalı
- Görsel (grafik, tablo, şekil) içermeli
- 4 şıklı çoktan seçmeli
- Analiz ve yorumlama becerisi ölçmeli
- Soru kökü net ve anlaşılır olmalı
        """,
        "subjects": ["Turkce", "Matematik", "Fen Bilimleri", "Sosyal Bilgiler", "Ingilizce", "Din Kulturu"],
    },
    "TYT": {
        "name": "Temel Yeterlilik Testi",
        "grade_range": [9, 10, 11, 12],
        "description": "Üniversite sınavı temel test",
        "visual_ratio": 0.65,
        "paragraph_required": True,
        "question_style": """
TYT SORU FORMATI:
- Temel düzey bilgi ve beceri ölçümü
- Paragraf/metin tabanlı sorular ağırlıklı
- Grafik ve tablo yorumlama soruları
- Güncel konularla bağlantılı
- 5 şıklı çoktan seçmeli
- Hızlı çözüm gerektiren sorular
        """,
        "subjects": ["Turkce", "Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya", "Felsefe"],
    },
    "AYT": {
        "name": "Alan Yeterlilik Testi",
        "grade_range": [11, 12],
        "description": "Üniversite sınavı alan testi",
        "visual_ratio": 0.75,
        "paragraph_required": True,
        "question_style": """
AYT SORU FORMATI:
- İleri düzey analiz ve sentez gerektiren sorular
- Karmaşık grafikler ve çoklu veri tabloları
- Çok adımlı problem çözme
- Alan bilgisini derinlemesine ölçen sorular
- 5 şıklı çoktan seçmeli
- Bağlam ve uygulama odaklı
        """,
        "subjects": ["Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya", "Felsefe", "Edebiyat"],
    },
    "Deneme": {
        "name": "Genel Deneme Sınavı",
        "grade_range": [5, 6, 7, 8, 9, 10, 11, 12],
        "description": "Okul içi deneme sınavı",
        "visual_ratio": 0.50,
        "paragraph_required": False,
        "question_style": """
DENEME SINAVI FORMATI:
- Konu tekrarı ve pekiştirme odaklı
- Görsel ve metin karışık sorular
- Farklı zorluk seviyelerinde sorular
- 4 veya 5 şıklı çoktan seçmeli
        """,
        "subjects": ["Matematik", "Turkce", "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya", "Felsefe", "Ingilizce"],
    },
}

# Ders bazli gorsel turleri - hangi derste hangi gorseller kullanilmali
DERS_GORSEL_TURLERI = {
    "Matematik": ["grafik", "tablo", "geometri_sekil", "koordinat_sistemi", "fonksiyon_grafigi"],
    "Fizik": ["hiz_zaman_grafigi", "kuvvet_diyagrami", "elektrik_devresi", "dalga_grafigi", "hareket_diyagrami"],
    "Kimya": ["atom_modeli", "periyodik_tablo", "ph_skalasi", "molekul_yapisi", "reaksiyon_semasi"],
    "Biyoloji": ["hucre_diyagrami", "dna_yapisi", "organ_sistemi", "beslenme_piramidi", "mitoz_safhalar"],
    "Cografya": ["iklim_grafigi", "nufus_piramidi", "harita", "besin_zinciri", "katman_kesiti"],
    "Tarih": ["kronoloji_serit", "harita", "tablo", "karsilastirma_tablosu"],
    "Turkce": ["paragraf", "tablo", "kavram_haritasi"],
}

# Bloom Taksonomisi Seviyeleri
BLOOM_LEVELS = {
    "hatirlama": {
        "description": "Bilgiyi hatırlama ve tanıma",
        "verbs": ["tanımla", "listele", "belirt", "hatırla", "seç", "eşleştir"],
        "question_stems": [
            "Aşağıdakilerden hangisi ... tanımıdır?",
            "... nedir?",
            "Aşağıdakilerden hangisi doğrudur?",
        ]
    },
    "anlama": {
        "description": "Kavramları açıklama ve yorumlama",
        "verbs": ["açıkla", "özetle", "yorumla", "karşılaştır", "sınıflandır"],
        "question_stems": [
            "Yukarıdaki metne göre ...",
            "Bu durumun nedeni nedir?",
            "Aşağıdakilerden hangisi ... ile açıklanabilir?",
        ]
    },
    "uygulama": {
        "description": "Bilgiyi yeni durumlarda kullanma",
        "verbs": ["uygula", "hesapla", "çöz", "göster", "kullan"],
        "question_stems": [
            "Verilen bilgilere göre ... değeri kaçtır?",
            "Bu formül kullanılarak ...",
            "Aşağıdaki problemde ...",
        ]
    },
    "analiz": {
        "description": "Parçalara ayırma ve ilişkileri inceleme",
        "verbs": ["analiz et", "karşılaştır", "ayırt et", "incele", "sorgula"],
        "question_stems": [
            "Tabloya göre aşağıdakilerden hangisi çıkarılabilir?",
            "Grafik incelendiğinde ...",
            "Bu durumların ortak özelliği nedir?",
        ]
    },
    "degerlendirme": {
        "description": "Yargılama ve eleştirme",
        "verbs": ["değerlendir", "eleştir", "savun", "destekle", "yargıla"],
        "question_stems": [
            "Aşağıdaki yorumlardan hangisi en doğrudur?",
            "Bu durumun en önemli sonucu hangisidir?",
            "Hangi yaklaşım en uygun olur?",
        ]
    },
    "sentez": {
        "description": "Yeni ürün oluşturma ve birleştirme",
        "verbs": ["tasarla", "oluştur", "planla", "geliştir", "birleştir"],
        "question_stems": [
            "Verilen koşullarda en uygun çözüm hangisidir?",
            "Bu bilgiler birleştirildiğinde ...",
            "Hangi sonuç ortaya çıkar?",
        ]
    }
}

# Soru Format Turleri
SORU_FORMATLARI = {
    "klasik": {
        "description": "Doğrudan soru",
        "template": "Doğrudan ve net bir soru sor."
    },
    "paragraf": {
        "description": "Paragraf/metin tabanlı",
        "template": """3-5 cümlelik bir bağlam paragrafı yaz, ardından bu paragrafa dayalı soru sor.
Paragraf gerçekçi ve ilgi çekici olmalı.
Soru paragraftaki bilgiyi analiz etmeyi gerektirmeli."""
    },
    "senaryo": {
        "description": "Günlük hayat senaryosu",
        "template": """Günlük hayattan gerçekçi bir senaryo oluştur (alışveriş, yolculuk, spor, okul vb.)
Senaryoda isimler, yerler ve somut veriler kullan.
Öğrencinin bilgisini gerçek hayata uygulamasını iste."""
    },
    "tablo": {
        "description": "Tablo/veri analizi",
        "template": """Basit bir tablo veya veri seti oluştur (ASCII formatında).
Tablo 3-5 satır, 2-4 sütun olsun.
Öğrenciden tablodaki verileri yorumlamasını veya hesaplama yapmasını iste."""
    },
    "grafik_aciklama": {
        "description": "Grafik yorumlama",
        "template": """Bir grafik tanımla (örn: "Aşağıdaki çizgi grafik X'in Y'ye göre değişimini göstermektedir").
Grafiğin özelliklerini belirt (artış, azalış, sabit kalma noktaları).
Öğrenciden grafik yorumu iste."""
    },
    "karsilastirma": {
        "description": "Karşılaştırmalı analiz",
        "template": """İki veya daha fazla kavram/durum/veri ver.
Öğrenciden bunları karşılaştırmasını ve fark/benzerlik bulmasını iste."""
    }
}

# Celdirici Tasarim Kurallari
CELDIRICI_KURALLARI = {
    "matematik": [
        "İşlem hatası (toplama yerine çarpma vb.)",
        "İşaret hatası (pozitif/negatif karışıklığı)",
        "Birim dönüşüm hatası",
        "Formül karışıklığı",
        "Yarım hesaplama (işlemin yarısında bırakma)",
    ],
    "fen": [
        "Benzer kavram karışıklığı",
        "Birim hatası",
        "Ters orantı/doğru orantı karışıklığı",
        "Formül yanlışlığı",
        "Günlük hayat yanılgıları",
    ],
    "sosyal": [
        "Tarih/dönem karışıklığı",
        "Benzer isim/kavram karışıklığı",
        "Neden-sonuç ters çevirme",
        "Kısmen doğru bilgi",
        "Genelleme hatası",
    ],
    "dil": [
        "Yakın anlamlı kelime karışıklığı",
        "Dil bilgisi kuralı yanlışlığı",
        "Bağlam dışı kullanım",
        "Kısmen doğru cevap",
        "Yaygın yazım hatası",
    ]
}

# Ders -> Celdirici kategorisi esleme
DERS_CELDIRICI_MAP = {
    "Matematik": "matematik",
    "Fizik": "fen",
    "Kimya": "fen",
    "Biyoloji": "fen",
    "Tarih": "sosyal",
    "Cografya": "sosyal",
    "Felsefe": "sosyal",
    "Turkce": "dil",
    "Ingilizce": "dil",
}

# Ana prompt sablonu - OSYM/MEB kalitesinde
SORU_PROMPT_TEMPLATE = """Sen ÖSYM ve MEB'de görev yapmış, 20 yıllık deneyime sahip bir sınav sorusu yazarısın.
LGS, YKS, KPSS gibi ulusal sınavlarda yüzlerce soru hazırladın.

## GÖREV
{grade}. sınıf {subject} dersi için {difficulty} seviyede, {question_format} formatında profesyonel bir sınav sorusu hazırla.

## KONU
{topic}

## BİLİŞSEL SEVİYE (Bloom Taksonomisi)
{bloom_level}: {bloom_description}
Soru bu seviyeye uygun olmalı.

## SORU FORMATI KURALLARI
{format_rules}

## ZORLUK SEVİYESİ: {difficulty}
{difficulty_rules}

## ÇELDİRİCİ TASARIMI (ÇOK ÖNEMLİ!)
Şıklar şu özelliklere sahip olmalı:
- Her yanlış şık, öğrencilerin GERÇEKTEN yapabileceği bir hatayı temsil etmeli
- Rastgele değerler YASAK - her şık mantıklı bir yanılgıya dayanmalı
- Şıklar birbirine yakın uzunlukta olmalı
- Doğru cevap açıkça en doğru olmalı, ama çeldiriciler de makul görünmeli

Olası çeldirici hataları:
{celdirici_ornekleri}

## SORU KALİTESİ KRİTERLERİ
✓ Türkçe dil bilgisi kusursuz olmalı
✓ Soru kökü net ve tek anlama gelmeli
✓ Gereksiz bilgi veya uzatma olmamalı
✓ Görsele atıf varsa açık tanımlanmalı
✓ Sayısal sorularda birimler belirtilmeli
✓ Her şık dilbilgisi açısından soru köküyle uyumlu olmalı

## YASAK SORU TİPLERİ
✗ "Aşağıdakilerden hangisi yanlıştır?" (negatif soru) - çok sık kullanıldı
✗ Sadece ezbere dayanan, düşünme gerektirmeyen sorular
✗ Çok uzun ve karmaşık soru kökleri
✗ Şıklarda "hepsi/hiçbiri" seçenekleri

## ÇIKIŞ FORMATI
SADECE aşağıdaki JSON formatında cevap ver, başka hiçbir şey yazma:
{{"soru": "TAM SORU METNİ (paragraf/senaryo dahil)", "secenekler": ["A şıkkı tam metin", "B şıkkı tam metin", "C şıkkı tam metin", "D şıkkı tam metin"], "dogru_cevap": "A/B/C/D harfi", "konu": "{topic}", "aciklama": "Neden bu cevap doğru ve diğerleri neden yanlış - kısa açıklama", "bloom_seviyesi": "{bloom_level}", "celdirici_mantigi": "Her yanlış şık hangi hatayı temsil ediyor"}}
"""

# Zorluk kurallari - daha detayli
ZORLUK_KURALLARI_DETAYLI = {
    "Kolay": """
- Tek adımda çözülebilen soru
- Temel kavram veya formül bilgisi yeterli
- Net ve doğrudan soru kökü
- Çeldiriciler açıkça yanlış ama mantıklı
- Çözüm süresi: 30-60 saniye""",
    "Orta": """
- 2-3 adım gerektiren soru
- Kavramları birleştirme veya uygulama gerekli
- Biraz analiz veya yorumlama içermeli
- Çeldiriciler daha yakın ve dikkat gerektiren
- Çözüm süresi: 1-2 dakika""",
    "Zor": """
- 3+ adım veya çoklu kavram gerektiren soru
- Derin analiz, sentez veya değerlendirme gerekli
- Farklı bilgileri birleştirme zorunlu
- Çeldiriciler çok yakın, dikkatli okuma şart
- Transfer becerisi gerektirmeli
- Çözüm süresi: 2-4 dakika"""
}


def _get_api_key(provider: str = "openai") -> str | None:
    """API key al."""
    if provider == "openai":
        if st.session_state.get("qb_openai_key"):
            return st.session_state.qb_openai_key
        key = os.environ.get("OPENAI_API_KEY", "")
        if key and not key.startswith("sk-..."):
            return key
    elif provider == "anthropic":
        if st.session_state.get("qb_anthropic_key"):
            return st.session_state.qb_anthropic_key
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if key and not key.startswith("sk-ant-..."):
            return key
    return None


def _get_random_topic(subject: str, grade: int) -> str:
    """Ders ve sinif icin rastgele konu sec."""
    topics = DERS_KONULARI.get(subject, {}).get(grade, [])
    if not topics:
        # Varsayilan konular
        default_topics = {
            "Matematik": "Temel Matematik",
            "Fizik": "Temel Fizik",
            "Kimya": "Temel Kimya",
            "Biyoloji": "Temel Biyoloji",
            "Tarih": "Genel Tarih",
            "Cografya": "Genel Cografya",
            "Turkce": "Dil Bilgisi",
            "Ingilizce": "General English",
        }
        return default_topics.get(subject, "Genel")
    return random.choice(topics)


def _parse_ai_response(content: str) -> dict | None:
    """AI cevabini parse et."""
    try:
        # Markdown kod blogu temizle
        if "```" in content:
            parts = content.split("```")
            for part in parts:
                if part.strip().startswith("json"):
                    content = part.strip()[4:].strip()
                    break
                elif part.strip().startswith("{"):
                    content = part.strip()
                    break

        # JSON parse
        content = content.strip()
        if not content.startswith("{"):
            # JSON basini bul
            start = content.find("{")
            if start != -1:
                content = content[start:]

        data = json.loads(content)
        return data
    except json.JSONDecodeError:
        return None


def _get_bloom_level_for_difficulty(difficulty: str) -> str:
    """Zorluk seviyesine gore uygun Bloom seviyesi sec."""
    if difficulty == "Kolay":
        return random.choice(["hatirlama", "anlama"])
    elif difficulty == "Orta":
        return random.choice(["anlama", "uygulama", "analiz"])
    else:  # Zor
        return random.choice(["analiz", "degerlendirme", "sentez"])


def _get_question_format_for_difficulty(difficulty: str) -> str:
    """Zorluk seviyesine gore uygun soru formati sec."""
    if difficulty == "Kolay":
        return random.choice(["klasik", "klasik", "senaryo"])
    elif difficulty == "Orta":
        return random.choice(["paragraf", "senaryo", "tablo", "klasik"])
    else:  # Zor
        return random.choice(["paragraf", "tablo", "grafik_aciklama", "karsilastirma"])


def _build_advanced_prompt(
    subject: str,
    difficulty: str,
    grade: int,
    topic: str,
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> str:
    """MEB/OSYM formatinda gelismis AI promptu olustur."""
    # Sinav tipi bilgileri
    sinav_config = SINAV_TIPLERI.get(sinav_tipi, SINAV_TIPLERI["Deneme"])

    # Otomatik secimler - sinav tipine gore
    if not bloom_level:
        bloom_level = _get_bloom_level_for_difficulty(difficulty)
    if not question_format:
        # LGS/TYT/AYT icin paragraf zorunlu
        if sinav_config.get("paragraph_required", False):
            question_format = random.choice(["paragraf", "senaryo", "tablo"])
        else:
            question_format = _get_question_format_for_difficulty(difficulty)

    # Bloom bilgileri
    bloom_info = BLOOM_LEVELS.get(bloom_level, BLOOM_LEVELS["uygulama"])
    bloom_description = bloom_info["description"]

    # Format kurallari
    format_info = SORU_FORMATLARI.get(question_format, SORU_FORMATLARI["klasik"])
    format_rules = format_info["template"]

    # Celdirici ornekleri
    celdirici_kategori = DERS_CELDIRICI_MAP.get(subject, "fen")
    celdirici_list = CELDIRICI_KURALLARI.get(celdirici_kategori, CELDIRICI_KURALLARI["fen"])
    celdirici_ornekleri = "\n".join(f"- {c}" for c in celdirici_list)

    # Zorluk kurallari
    difficulty_rules = ZORLUK_KURALLARI_DETAYLI.get(difficulty, ZORLUK_KURALLARI_DETAYLI["Orta"])

    return SORU_PROMPT_TEMPLATE.format(
        subject=subject,
        grade=grade,
        difficulty=difficulty,
        topic=topic,
        question_format=format_info["description"],
        bloom_level=bloom_level,
        bloom_description=bloom_description,
        format_rules=format_rules,
        difficulty_rules=difficulty_rules,
        celdirici_ornekleri=celdirici_ornekleri
    )


def _generate_ai_question_openai(
    subject: str,
    difficulty: str,
    grade: int,
    topic: str | None = None,
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> dict | None:
    """MEB/OSYM formatinda OpenAI ile profesyonel kalitede soru uret."""
    api_key = _get_api_key("openai")
    if not api_key or not OPENAI_AVAILABLE:
        return None

    try:
        client = OpenAI(api_key=api_key)

        if not topic:
            topic = _get_random_topic(subject, grade)

        # Sinav tipine gore prompt olustur
        prompt = _build_advanced_prompt(
            subject=subject,
            difficulty=difficulty,
            grade=grade,
            topic=topic,
            question_format=question_format,
            bloom_level=bloom_level,
            sinav_tipi=sinav_tipi
        )

        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

        # Sinav tipine ozel sistem mesaji
        sinav_config = SINAV_TIPLERI.get(sinav_tipi, SINAV_TIPLERI["Deneme"])
        system_message = f"""Sen ÖSYM ve MEB'de çalışmış deneyimli bir {sinav_tipi} sınav sorusu yazarısın.
{sinav_config['name']} için yüzlerce soru hazırladın.
{sinav_config.get('question_style', '')}

MUTLAKA:
- Soru görsel/grafik/tablo gerektiriyorsa, bunu soru metninde açıkça belirt
- Her soru bağlam/senaryo ile başlamalı
- Çeldiriciler gerçek öğrenci hatalarını yansıtmalı
- SADECE istenen JSON formatında cevap ver."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=1500,
        )

        content = response.choices[0].message.content.strip()
        data = _parse_ai_response(content)

        if not data or "soru" not in data:
            return None

        return {
            "text": data["soru"],
            "options": data.get("secenekler", ["A", "B", "C", "D"]),
            "answer": data.get("dogru_cevap", "A"),
            "subject": subject,
            "difficulty": difficulty,
            "topic": data.get("konu", topic),
            "explanation": data.get("aciklama", ""),
            "bloom_level": data.get("bloom_seviyesi", bloom_level),
            "celdirici_mantigi": data.get("celdirici_mantigi", ""),
            "source": "ai-openai-pro",
        }
    except Exception as e:
        st.warning(f"OpenAI hatasi: {str(e)[:100]}")
        return None


def _generate_ai_question_anthropic(
    subject: str,
    difficulty: str,
    grade: int,
    topic: str | None = None,
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> dict | None:
    """MEB/OSYM formatinda Anthropic Claude ile profesyonel kalitede soru uret."""
    api_key = _get_api_key("anthropic")
    if not api_key or not ANTHROPIC_AVAILABLE:
        return None

    try:
        client = anthropic.Anthropic(api_key=api_key)

        if not topic:
            topic = _get_random_topic(subject, grade)

        # Sinav tipine gore prompt olustur
        prompt = _build_advanced_prompt(
            subject=subject,
            difficulty=difficulty,
            grade=grade,
            topic=topic,
            question_format=question_format,
            bloom_level=bloom_level,
            sinav_tipi=sinav_tipi
        )

        # Sinav tipine ozel sistem mesaji
        sinav_config = SINAV_TIPLERI.get(sinav_tipi, SINAV_TIPLERI["Deneme"])
        system_message = f"""Sen ÖSYM ve MEB'de çalışmış deneyimli bir {sinav_tipi} sınav sorusu yazarısın.
{sinav_config['name']} için yüzlerce soru hazırladın.
{sinav_config.get('question_style', '')}

MUTLAKA:
- Soru görsel/grafik/tablo gerektiriyorsa, bunu soru metninde açıkça belirt
- Her soru bağlam/senaryo ile başlamalı
- Çeldiriciler gerçek öğrenci hatalarını yansıtmalı
- SADECE istenen JSON formatında cevap ver."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system_message,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.content[0].text.strip()
        data = _parse_ai_response(content)

        if not data or "soru" not in data:
            return None

        return {
            "text": data["soru"],
            "options": data.get("secenekler", ["A", "B", "C", "D"]),
            "answer": data.get("dogru_cevap", "A"),
            "subject": subject,
            "difficulty": difficulty,
            "topic": data.get("konu", topic),
            "explanation": data.get("aciklama", ""),
            "bloom_level": data.get("bloom_seviyesi", bloom_level),
            "celdirici_mantigi": data.get("celdirici_mantigi", ""),
            "source": "ai-anthropic-pro",
        }
    except Exception as e:
        st.warning(f"Anthropic hatasi: {str(e)[:100]}")
        return None


def _generate_ai_question(
    subject: str,
    difficulty: str,
    grade: int,
    provider: str = "auto",
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> dict | None:
    """MEB/OSYM formatinda AI ile profesyonel kalitede soru uret."""
    if provider == "auto":
        # Once OpenAI dene
        if _get_api_key("openai") and OPENAI_AVAILABLE:
            result = _generate_ai_question_openai(
                subject, difficulty, grade,
                question_format=question_format,
                bloom_level=bloom_level,
                sinav_tipi=sinav_tipi
            )
            if result:
                return result
        # Sonra Anthropic dene
        if _get_api_key("anthropic") and ANTHROPIC_AVAILABLE:
            result = _generate_ai_question_anthropic(
                subject, difficulty, grade,
                question_format=question_format,
                bloom_level=bloom_level,
                sinav_tipi=sinav_tipi
            )
            if result:
                return result
    elif provider == "openai":
        return _generate_ai_question_openai(
            subject, difficulty, grade,
            question_format=question_format,
            bloom_level=bloom_level,
            sinav_tipi=sinav_tipi
        )
    elif provider == "anthropic":
        return _generate_ai_question_anthropic(
            subject, difficulty, grade,
            question_format=question_format,
            bloom_level=bloom_level,
            sinav_tipi=sinav_tipi
        )

    return None


def get_ai_status() -> dict:
    """AI durumunu kontrol et."""
    return {
        "openai_available": OPENAI_AVAILABLE,
        "openai_key": bool(_get_api_key("openai")),
        "anthropic_available": ANTHROPIC_AVAILABLE,
        "anthropic_key": bool(_get_api_key("anthropic")),
        "any_ai_ready": (OPENAI_AVAILABLE and bool(_get_api_key("openai"))) or
                        (ANTHROPIC_AVAILABLE and bool(_get_api_key("anthropic"))),
    }


# Sabitler
SINIF_SEVIYELERI = {
    "Ilkokul": [1, 2, 3, 4],
    "Ortaokul": [5, 6, 7, 8],
    "Lise": [9, 10, 11, 12],
}

DERSLER = {
    "Sayisal": ["Matematik", "Fizik", "Kimya", "Biyoloji"],
    "Sozel": ["Turkce", "Tarih", "Cografya", "Felsefe"],
    "Dil": ["Ingilizce", "Almanca"],
    "Diger": ["Din Kulturu", "Beden Egitimi"],
}

TUM_DERSLER = ["Matematik", "Turkce", "Fizik", "Kimya", "Biyoloji", "Tarih", "Cografya", "Felsefe", "Ingilizce"]

SORU_TIPLERI = ["Coktan Secmeli (4 Sik)", "Coktan Secmeli (5 Sik)", "Dogru/Yanlis", "Bosluk Doldurma"]

ZORLUK_SEVIYELERI = ["Kolay", "Orta", "Zor", "Karisik"]


def _init_state(reset: bool = False):
    """Session state'i baslat.

    Args:
        reset: True ise mevcut sinav ve import verilerini temizle
    """
    # Modul giris kontrolu - farkli sayfadan gelindiyse temizle
    current_page = "question_builder"
    last_page = st.session_state.get("_last_visited_page", "")

    if last_page != current_page:
        # Farkli sayfadan gelindi - gecici verileri temizle
        reset = True

    st.session_state["_last_visited_page"] = current_page

    defaults = {
        "qb_kademe": "Lise",
        "qb_sinif": 9,
        "qb_sube": "A",
        "qb_secili_dersler": [],
        "qb_ders_soru_sayilari": {},
        "qb_soru_tipi": "Coktan Secmeli (4 Sik)",
        "qb_zorluk": "Karisik",
        "qb_sure": 40,
        "qb_sinav_adi": "",
        "qb_olusturulan_sinav": None,
        "qb_use_ai": False,
        "qb_openai_key": "",
        "qb_anthropic_key": "",
        "qb_ai_provider": "auto",
        "qb_use_visuals": True,
        "qb_imported_questions": None,  # PDF'den yuklenen sorular
        # Gelismis kalite ayarlari
        "qb_question_format": "otomatik",  # otomatik/klasik/paragraf/senaryo/tablo/grafik_aciklama/karsilastirma
        "qb_bloom_level": "otomatik",  # otomatik/hatirlama/anlama/uygulama/analiz/degerlendirme/sentez
        # Sinav tipi (MEB/OSYM uyumlu)
        "qb_sinav_tipi": "Deneme",  # LGS/TYT/AYT/Deneme
    }

    # Reset modunda gecici verileri sifirla
    if reset:
        st.session_state["qb_olusturulan_sinav"] = None
        st.session_state["qb_imported_questions"] = None
        st.session_state["qb_secili_dersler"] = []
        st.session_state["qb_ders_soru_sayilari"] = {}
        st.session_state["qb_sinav_adi"] = ""

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _generate_math_question(difficulty: str) -> dict:
    """Matematik sorusu uret."""
    rng = random.Random()

    if difficulty == "Kolay":
        a, b = rng.randint(1, 10), rng.randint(1, 10)
        answer = a + b
        question = f"{a} + {b} = ?"
        options = [str(answer - 1), str(answer), str(answer + 1), str(answer + 2)]
        correct = "B"
    elif difficulty == "Zor":
        a = rng.randint(2, 5)
        b = rng.randint(1, 10)
        x = rng.randint(1, 5)
        answer = a * x + b
        question = f"f(x) = {a}x + {b} fonksiyonunda x = {x} icin f(x) degeri kactir?"
        options = [str(answer - 2), str(answer - 1), str(answer), str(answer + 1)]
        correct = "C"
    else:  # Orta
        a, b = rng.randint(5, 15), rng.randint(2, 8)
        answer = a * b
        question = f"{a} x {b} = ?"
        options = [str(answer - b), str(answer), str(answer + b), str(answer + 2*b)]
        correct = "B"

    return {
        "text": question,
        "options": options,
        "answer": correct,
        "subject": "Matematik",
        "difficulty": difficulty,
    }


def _generate_turkish_question(difficulty: str) -> dict:
    """Turkce sorusu uret."""
    questions = [
        {
            "text": "Asagidaki cumlelerden hangisinde yazim yanlisi vardir?",
            "options": ["Herkez geldi.", "Herkes gelmis.", "Kimse yok.", "Biri var."],
            "answer": "A",
        },
        {
            "text": "'Kitap okumak faydalidir' cumlesinin ogeleri hangi sirada verilmistir?",
            "options": ["Ozne-Yuklem", "Nesne-Yuklem", "Ozne-Nesne-Yuklem", "Dolayli Tumle\u00e7-Yuklem"],
            "answer": "A",
        },
        {
            "text": "Asagidakilerden hangisi sifat degildir?",
            "options": ["guzel", "hizli", "kosmak", "buyuk"],
            "answer": "C",
        },
        {
            "text": "'Ormanda yuruyus yaptik' cumlesinde kac kelime vardir?",
            "options": ["2", "3", "4", "5"],
            "answer": "B",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Turkce"
    q["difficulty"] = difficulty
    return q


def _generate_physics_question(difficulty: str) -> dict:
    """Fizik sorusu uret."""
    rng = random.Random()

    v = rng.randint(3, 10)
    t = rng.randint(2, 8)
    s = v * t

    questions = [
        {
            "text": f"Bir cisim {v} m/s hizla {t} saniye hareket ederse aldigi yol kac metredir?",
            "options": [str(s - v), str(s), str(s + v), str(s + t)],
            "answer": "B",
        },
        {
            "text": f"Kutlesi {v} kg olan cisme {t} m/s^2 ivme uygulanirsa kuvvet kac Newton olur?",
            "options": [str(v*t - t), str(v*t), str(v*t + v), str(v*t + t)],
            "answer": "B",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Fizik"
    q["difficulty"] = difficulty
    return q


def _generate_chemistry_question(difficulty: str) -> dict:
    """Kimya sorusu uret."""
    questions = [
        {
            "text": "Asagidakilerden hangisi element degildir?",
            "options": ["Su (H2O)", "Demir (Fe)", "Oksijen (O)", "Karbon (C)"],
            "answer": "A",
        },
        {
            "text": "Periyodik tabloda atomlar neye gore siralanir?",
            "options": ["Atom numarasina", "Kutleye", "Hacme", "Renge"],
            "answer": "A",
        },
        {
            "text": "Asit ve baz tepkimesine ne ad verilir?",
            "options": ["Notrallesme", "Yanma", "Oksidasyon", "Indirgeme"],
            "answer": "A",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Kimya"
    q["difficulty"] = difficulty
    return q


def _generate_biology_question(difficulty: str) -> dict:
    """Biyoloji sorusu uret."""
    questions = [
        {
            "text": "Hucrenin enerji uretimiinden sorumlu organeli hangisidir?",
            "options": ["Mitokondri", "Ribozom", "Golgi", "Cekirdek"],
            "answer": "A",
        },
        {
            "text": "DNA'nin yapitasi olan molekul hangisidir?",
            "options": ["Nokleotit", "Amino asit", "Glikoz", "Yag asidi"],
            "answer": "A",
        },
        {
            "text": "Fotosentez hangi organelde gerceklesir?",
            "options": ["Kloroplast", "Mitokondri", "Ribozom", "Lizozom"],
            "answer": "A",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Biyoloji"
    q["difficulty"] = difficulty
    return q


def _generate_history_question(difficulty: str) -> dict:
    """Tarih sorusu uret."""
    questions = [
        {
            "text": "Turkiye Cumhuriyeti hangi yil ilan edilmistir?",
            "options": ["1920", "1921", "1922", "1923"],
            "answer": "D",
        },
        {
            "text": "Kurtulus Savasi hangi antlasma ile sona ermistir?",
            "options": ["Sevr", "Mondros", "Lozan", "Ankara"],
            "answer": "C",
        },
        {
            "text": "Ilk Turk devleti hangisidir?",
            "options": ["Hunlar", "Gokturkler", "Uygurlar", "Selcuklular"],
            "answer": "A",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Tarih"
    q["difficulty"] = difficulty
    return q


def _generate_geography_question(difficulty: str) -> dict:
    """Cografya sorusu uret."""
    questions = [
        {
            "text": "Turkiye'nin en buyuk golu hangisidir?",
            "options": ["Van Golu", "Tuz Golu", "Beysehir Golu", "Egirdir Golu"],
            "answer": "A",
        },
        {
            "text": "Asagidakilerden hangisi bir iklim unsurudur?",
            "options": ["Sicaklik", "Enlem", "Yukselti", "Denize uzaklik"],
            "answer": "A",
        },
        {
            "text": "Dunya'nin en buyuk okyanusu hangisidir?",
            "options": ["Pasifik", "Atlantik", "Hint", "Arktik"],
            "answer": "A",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Cografya"
    q["difficulty"] = difficulty
    return q


def _generate_philosophy_question(difficulty: str) -> dict:
    """Felsefe sorusu uret."""
    questions = [
        {
            "text": "Felsefenin temel sorularindan biri olan 'Varlik nedir?' sorusu hangi alan ile ilgilidir?",
            "options": ["Ontoloji", "Epistemoloji", "Etik", "Estetik"],
            "answer": "A",
        },
        {
            "text": "'Dusunuyorum, o halde varim' sozunu soyleyen filozof kimdir?",
            "options": ["Descartes", "Platon", "Aristoteles", "Sokrates"],
            "answer": "A",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Felsefe"
    q["difficulty"] = difficulty
    return q


def _generate_english_question(difficulty: str) -> dict:
    """Ingilizce sorusu uret."""
    questions = [
        {
            "text": "Choose the correct form: She ___ to school every day.",
            "options": ["go", "goes", "going", "gone"],
            "answer": "B",
        },
        {
            "text": "What is the past tense of 'eat'?",
            "options": ["eated", "ate", "eaten", "eating"],
            "answer": "B",
        },
        {
            "text": "Which word is a noun?",
            "options": ["quickly", "beautiful", "happiness", "run"],
            "answer": "C",
        },
    ]
    q = random.choice(questions)
    q["subject"] = "Ingilizce"
    q["difficulty"] = difficulty
    return q


def _generate_question(
    subject: str,
    difficulty: str,
    use_ai: bool = False,
    grade: int = 9,
    use_visuals: bool = True,
    ai_provider: str = "auto",
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> dict:
    """MEB/OSYM formatinda profesyonel kalitede soru uret.

    Args:
        subject: Ders adi
        difficulty: Zorluk seviyesi (Kolay/Orta/Zor/Karisik)
        use_ai: AI kullanimi
        grade: Sinif seviyesi
        use_visuals: Gorsel soru kullanimi
        ai_provider: AI saglayici (auto/openai/anthropic)
        question_format: Soru formati (klasik/paragraf/senaryo/tablo/grafik_aciklama/karsilastirma)
        bloom_level: Bloom taksonomisi seviyesi
        sinav_tipi: Sinav tipi (LGS/TYT/AYT/Deneme)
    """
    if difficulty == "Karisik":
        difficulty = random.choice(["Kolay", "Orta", "Zor"])

    # Sinav tipine gore gorsel orani al
    sinav_config = SINAV_TIPLERI.get(sinav_tipi, SINAV_TIPLERI["Deneme"])
    visual_ratio = sinav_config.get("visual_ratio", 0.50)
    paragraph_required = sinav_config.get("paragraph_required", False)

    # Gorsel soru uretici import
    visual_available = False
    try:
        from ._visual_questions import generate_visual_question, get_available_visual_subjects
        visual_available = subject in get_available_visual_subjects()
    except Exception:
        pass

    # ========== MEB/OSYM UYUMLU SORU URETIM STRATEJISI ==========

    # STRATEJI 1: Sinav tipine gore gorsel soru (LGS/TYT/AYT icin yuksek oran)
    # Gercek sinavlarda gosel oran %60-75 arasi
    if use_visuals and visual_available and random.random() < visual_ratio:
        try:
            visual_q = generate_visual_question(subject)
            if visual_q:
                visual_q["difficulty"] = difficulty
                visual_q["source"] = f"visual-{sinav_tipi.lower()}"
                visual_q["sinav_tipi"] = sinav_tipi
                return visual_q
        except Exception:
            pass

    # STRATEJI 2: AI + Gorsel hibrit (sinav tipine gore)
    if use_ai:
        # Paragraf zorunluysa (LGS/TYT/AYT) ve format belirtilmemisse, paragraf sec
        if paragraph_required and not question_format:
            question_format = random.choice(["paragraf", "senaryo", "tablo"])

        # Format gorselse yuksek ihtimalle gorsel soru uret
        visual_formats = ["tablo", "grafik_aciklama", "karsilastirma"]
        if question_format in visual_formats and visual_available and random.random() < visual_ratio:
            try:
                visual_q = generate_visual_question(subject)
                if visual_q:
                    visual_q["difficulty"] = difficulty
                    visual_q["source"] = f"visual-ai-{sinav_tipi.lower()}"
                    visual_q["sinav_tipi"] = sinav_tipi
                    return visual_q
            except Exception:
                pass

        # AI sorusu uret (sinav tipine ozel prompt ile)
        ai_question = _generate_ai_question(
            subject=subject,
            difficulty=difficulty,
            grade=grade,
            provider=ai_provider,
            question_format=question_format,
            bloom_level=bloom_level,
            sinav_tipi=sinav_tipi
        )
        if ai_question:
            ai_question["sinav_tipi"] = sinav_tipi

            # STRATEJI 3: AI sorularina tamamlayici gorsel ekleme
            # Sinav tipine gore gorsel ekleme orani
            if use_visuals and visual_available:
                # LGS/TYT/AYT icin her AI sorusuna gorsel eklemeye calis
                add_visual_chance = visual_ratio if sinav_tipi in ["LGS", "TYT", "AYT"] else 0.3
                if question_format in visual_formats or random.random() < add_visual_chance:
                    try:
                        # Ilgili gorsel uret ve ekle
                        supplementary_visual = _create_supplementary_visual(subject, question_format, ai_question)
                        if supplementary_visual:
                            ai_question["image_bytes"] = supplementary_visual
                            ai_question["source"] = ai_question.get("source", "ai") + "-with-visual"
                    except Exception:
                        pass
            return ai_question

    # Zengin soru sablonlarindan al
    try:
        from ._question_templates import get_question_from_template
        template_q = get_question_from_template(subject, difficulty)
        if template_q:
            return template_q
    except Exception:
        pass

    # Legacy fallback (sadece template bulunamazsa)
    generators = {
        "Matematik": _generate_math_question,
        "Turkce": _generate_turkish_question,
        "Fizik": _generate_physics_question,
        "Kimya": _generate_chemistry_question,
        "Biyoloji": _generate_biology_question,
        "Tarih": _generate_history_question,
        "Cografya": _generate_geography_question,
        "Felsefe": _generate_philosophy_question,
        "Ingilizce": _generate_english_question,
    }

    generator = generators.get(subject, _generate_math_question)
    return generator(difficulty)


# ==================== AI SORU GORSELLERI ====================

def _create_supplementary_visual(subject: str, question_format: str, ai_question: dict) -> bytes | None:
    """AI sorusuna tamamlayici gorsel olustur.

    Args:
        subject: Ders adi
        question_format: Soru formati (tablo/grafik_aciklama/karsilastirma)
        ai_question: AI'nin olusturdugu soru

    Returns:
        Gorsel bytes veya None
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import io

        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']

        if question_format == "tablo":
            return _create_table_visual(ai_question, plt)
        elif question_format == "grafik_aciklama":
            return _create_graph_visual(subject, ai_question, plt)
        elif question_format == "karsilastirma":
            return _create_comparison_visual(ai_question, plt)

    except Exception as e:
        print(f"Gorsel olusturma hatasi: {e}")
        return None

    return None


def _create_table_visual(ai_question: dict, plt) -> bytes | None:
    """AI sorusu icin tablo gorseli olustur."""
    import io
    import re

    question_text = ai_question.get("text", "")

    # Soru metninden tablo verisi cikarma (basit regex)
    # Ornek: "Asagidaki tabloda X ve Y verilmistir..."
    # Bu durumda ornek veri ile tablo olustur

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
    ax.axis('off')

    # Ornek tablo verisi (soru baglamina gore)
    if "ogrenci" in question_text.lower() or "sinif" in question_text.lower():
        data = [
            ['Ogrenci', 'Mat', 'Fen', 'Turkce'],
            ['Ali', '85', '90', '78'],
            ['Ayse', '92', '88', '95'],
            ['Mehmet', '78', '82', '80'],
            ['Zeynep', '95', '91', '88'],
        ]
    elif "urun" in question_text.lower() or "fiyat" in question_text.lower():
        data = [
            ['Urun', 'Fiyat (TL)', 'Stok'],
            ['Kalem', '5', '120'],
            ['Defter', '15', '80'],
            ['Silgi', '3', '200'],
            ['Cetvel', '8', '50'],
        ]
    elif "gun" in question_text.lower() or "hafta" in question_text.lower():
        data = [
            ['Gun', 'Sicaklik', 'Nem (%)'],
            ['Pazartesi', '22°C', '65'],
            ['Sali', '25°C', '58'],
            ['Carsamba', '28°C', '45'],
            ['Persembe', '24°C', '70'],
        ]
    else:
        data = [
            ['Kategori', 'Deger A', 'Deger B'],
            ['X', '45', '52'],
            ['Y', '38', '41'],
            ['Z', '67', '73'],
            ['W', '29', '35'],
        ]

    table = ax.table(cellText=data, loc='center', cellLoc='center',
                     colWidths=[0.25] * len(data[0]))
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Baslik satiri renklendir
    for j in range(len(data[0])):
        table[(0, j)].set_facecolor('#4ECDC4')
        table[(0, j)].set_text_props(fontweight='bold', color='white')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def _create_graph_visual(subject: str, ai_question: dict, plt) -> bytes | None:
    """AI sorusu icin grafik gorseli olustur."""
    import io
    import random

    question_text = ai_question.get("text", "")

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    # Ders ve soru baglamina gore grafik tipi sec
    if subject == "Matematik":
        # Fonksiyon grafigi
        x = [i * 0.5 for i in range(-6, 7)]
        a = random.choice([1, 2, -1])
        b = random.choice([-2, -1, 0, 1, 2])
        y = [a * xi + b for xi in x]

        ax.plot(x, y, 'b-', linewidth=2, label=f'f(x)')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Fonksiyon Grafigi', fontsize=11)

    elif subject == "Fizik":
        # Hiz-zaman grafigi
        t = list(range(0, 8))
        v = [0, 10, 20, 20, 20, 15, 10, 0]

        ax.plot(t, v, 'r-o', linewidth=2, markersize=6)
        ax.fill_between(t, v, alpha=0.3, color='red')
        ax.set_xlabel('Zaman (s)')
        ax.set_ylabel('Hiz (m/s)')
        ax.set_title('Hiz-Zaman Grafigi', fontsize=11)
        ax.grid(True, alpha=0.3)

    elif subject == "Cografya":
        # Iklim grafigi
        months = ['O', 'S', 'M', 'N', 'M', 'H', 'T', 'A', 'E', 'E', 'K', 'A']
        temps = [5, 7, 12, 17, 22, 27, 30, 29, 24, 18, 12, 7]
        precip = [80, 70, 60, 45, 25, 10, 5, 8, 20, 45, 70, 90]

        ax2 = ax.twinx()
        ax.plot(months, temps, 'r-o', linewidth=2, label='Sicaklik')
        ax2.bar(months, precip, alpha=0.5, color='blue', label='Yagis')
        ax.set_ylabel('Sicaklik (°C)', color='red')
        ax2.set_ylabel('Yagis (mm)', color='blue')
        ax.set_title('Iklim Grafigi', fontsize=11)

    else:
        # Genel cubuk grafik
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [random.randint(20, 80) for _ in range(5)]

        bars = ax.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        ax.set_ylabel('Deger')
        ax.set_title('Veri Grafigi', fontsize=11)

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val),
                    ha='center', va='bottom', fontsize=9)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def _create_comparison_visual(ai_question: dict, plt) -> bytes | None:
    """AI sorusu icin karsilastirma gorseli olustur."""
    import io
    import random

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

    categories = ['Ozellik 1', 'Ozellik 2', 'Ozellik 3', 'Ozellik 4']
    group_a = [random.randint(30, 90) for _ in range(4)]
    group_b = [random.randint(30, 90) for _ in range(4)]

    x = range(len(categories))
    width = 0.35

    bars1 = ax.bar([xi - width/2 for xi in x], group_a, width, label='Grup A', color='#4ECDC4')
    bars2 = ax.bar([xi + width/2 for xi in x], group_b, width, label='Grup B', color='#FF6B6B')

    ax.set_ylabel('Deger')
    ax.set_title('Karsilastirma Grafigi', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Deger etiketleri
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{int(bar.get_height())}',
                ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{int(bar.get_height())}',
                ha='center', va='bottom', fontsize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ==================== PDF SORU IMPORT ====================

def _extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """PDF'den metin cikar."""
    text = ""

    if PYMUPDF_AVAILABLE:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n\n"
            doc.close()
            return text.strip()
        except Exception as e:
            st.warning(f"PyMuPDF ile okuma hatasi: {e}")

    if PDFPLUMBER_AVAILABLE:
        try:
            import io
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            return text.strip()
        except Exception as e:
            st.warning(f"pdfplumber ile okuma hatasi: {e}")

    return text


def _parse_questions_from_text(text: str, use_ai: bool = False) -> list[dict]:
    """Metinden sorulari ayikla."""
    import re

    questions = []

    # Ortak soru desenleri
    patterns = [
        # "1. Soru metni" veya "1) Soru metni"
        r'(?:^|\n)\s*(\d+)\s*[.\)]\s*(.+?)(?=\n\s*(?:A\)|A\.|a\)|[Aa][\.\)]))',
        # Sadece numarali satirlar
        r'(?:^|\n)\s*(?:Soru\s*)?(\d+)\s*[:\.\)]\s*(.+?)(?=\n\s*\d+\s*[:\.\)]|\Z)',
    ]

    # Sik desenleri
    option_pattern = r'\s*([A-Ea-e])\s*[.\)]\s*(.+?)(?=\s*[A-Ea-e]\s*[.\)]|\n\s*(?:Cevap|Dogru|Yanit)|$)'

    # Basit regex ile soru ayirma
    # Soru numaralari ile ayir: 1. 2. 3. veya 1) 2) 3)
    question_blocks = re.split(r'\n(?=\s*\d+\s*[\.\)])', text)

    for block in question_blocks:
        block = block.strip()
        if not block or len(block) < 20:
            continue

        # Soru numarasi ve metni ayir
        match = re.match(r'^\s*(\d+)\s*[\.\)]\s*(.+)', block, re.DOTALL)
        if not match:
            continue

        q_num = match.group(1)
        q_content = match.group(2).strip()

        # Siklari bul
        options = []
        option_matches = re.findall(r'([A-Ea-e])\s*[\.\)]\s*([^\n]+)', q_content)

        if option_matches:
            for opt_letter, opt_text in option_matches:
                options.append(opt_text.strip())

            # Soru metnini siklar baslamadan once kes
            first_option_match = re.search(r'[A-Ea-e]\s*[\.\)]', q_content)
            if first_option_match:
                q_text = q_content[:first_option_match.start()].strip()
            else:
                q_text = q_content
        else:
            q_text = q_content
            options = []

        # Cevap anahtarini bul (varsa)
        answer = ""
        answer_match = re.search(r'(?:Cevap|Dogru\s*Cevap|Yanit)\s*[:\s]*([A-Ea-e])', q_content, re.IGNORECASE)
        if answer_match:
            answer = answer_match.group(1).upper()

        if q_text and len(q_text) > 10:
            questions.append({
                "number": int(q_num),
                "text": q_text,
                "options": options[:5] if options else ["", "", "", ""],  # Max 5 sik
                "answer": answer or "A",
                "subject": "Genel",
                "difficulty": "Orta",
                "source": "pdf-import",
            })

    # AI ile daha iyi ayristirma (opsiyonel)
    if use_ai and not questions and len(text) > 100:
        ai_questions = _parse_questions_with_ai(text)
        if ai_questions:
            return ai_questions

    return questions


def _parse_questions_with_ai(text: str) -> list[dict]:
    """AI kullanarak metinden soru ayikla."""
    api_key = _get_api_key("openai")
    if not api_key or not OPENAI_AVAILABLE:
        return []

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""Asagidaki metinden sinav sorularini ayikla ve JSON formatinda dondur.
Her soru icin:
- number: Soru numarasi
- text: Soru metni
- options: Siklar listesi (A, B, C, D seklinde)
- answer: Dogru cevap harfi (A/B/C/D)

METIN:
{text[:4000]}

SADECE JSON array formatinda cevap ver, baska bir sey yazma:
[{{"number": 1, "text": "...", "options": ["...", "...", "...", "..."], "answer": "A"}}, ...]
"""

        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Sen bir PDF soru ayristirma uzmanisin. Sadece JSON formatinda cevap ver."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        content = response.choices[0].message.content.strip()

        # JSON parse
        if "```" in content:
            parts = content.split("```")
            for part in parts:
                if part.strip().startswith("json"):
                    content = part.strip()[4:].strip()
                    break
                elif part.strip().startswith("["):
                    content = part.strip()
                    break

        data = json.loads(content)

        questions = []
        for item in data:
            questions.append({
                "number": item.get("number", len(questions) + 1),
                "text": item.get("text", ""),
                "options": item.get("options", ["", "", "", ""]),
                "answer": item.get("answer", "A"),
                "subject": "Genel",
                "difficulty": "Orta",
                "source": "pdf-import-ai",
            })

        return questions

    except Exception as e:
        st.warning(f"AI soru ayristirma hatasi: {e}")
        return []


def _normalize_question_text(text: str) -> str:
    """Soru metnini karsilastirma icin normalize et."""
    # Kucuk harf, bosluk temizleme, noktalama kaldirma
    import re
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Coklu bosluklari tekil yap
    text = re.sub(r'[.,;:!?()"\'\-]', '', text)  # Noktalama kaldir
    return text


def _generate_exam(
    sinav_adi: str,
    sinif: int,
    sube: str,
    ders_sayilari: dict,
    zorluk: str,
    sure: int,
    use_ai: bool = False,
    use_visuals: bool = True,
    ai_provider: str = "auto",
    question_format: str | None = None,
    bloom_level: str | None = None,
    sinav_tipi: str = "Deneme"
) -> dict:
    """MEB/OSYM formatinda profesyonel kalitede sinav olustur.

    Args:
        sinav_adi: Sinav adi
        sinif: Sinif seviyesi
        sube: Sube
        ders_sayilari: Ders bazli soru sayilari
        zorluk: Zorluk seviyesi
        sure: Sinav suresi
        use_ai: AI kullanimi
        use_visuals: Gorsel soru kullanimi
        ai_provider: AI saglayici
        question_format: Soru formati (None=otomatik)
        bloom_level: Bloom seviyesi (None=otomatik)
        sinav_tipi: Sinav tipi (LGS/TYT/AYT/Deneme)
    """
    questions = []
    question_number = 1
    used_questions: set[str] = set()  # Kullanilan soru metinleri (normalize edilmis)
    MAX_RETRIES = 10  # Ayni soru gelirse max deneme sayisi

    for ders, sayi in ders_sayilari.items():
        if sayi <= 0:
            continue

        ders_retries = 0  # Bu ders icin toplam deneme
        generated_for_ders = 0  # Bu ders icin uretilen soru sayisi

        while generated_for_ders < sayi and ders_retries < sayi * MAX_RETRIES:
            q = _generate_question(
                subject=ders,
                difficulty=zorluk,
                use_ai=use_ai,
                grade=sinif,
                use_visuals=use_visuals,
                ai_provider=ai_provider,
                question_format=question_format,
                bloom_level=bloom_level,
                sinav_tipi=sinav_tipi
            )

            # Soru metnini normalize et
            q_text_normalized = _normalize_question_text(q.get("text", ""))

            # Bos veya cok kisa soru kontrolu
            if len(q_text_normalized) < 5:
                ders_retries += 1
                continue

            # Tekrar kontrolu
            if q_text_normalized in used_questions:
                ders_retries += 1
                continue

            # Benzersiz soru bulundu
            used_questions.add(q_text_normalized)
            q["number"] = question_number
            q["grade"] = sinif
            questions.append(q)
            question_number += 1
            generated_for_ders += 1

        # Eger yeterli benzersiz soru uretilemezse uyari ver
        if generated_for_ders < sayi:
            st.warning(f"{ders} icin {sayi} soru istendi, {generated_for_ders} benzersiz soru bulundu.")

    # Sorulari karistir
    random.shuffle(questions)

    # Numaralari yeniden ata
    for i, q in enumerate(questions, 1):
        q["number"] = i

    exam_code = hashlib.md5(f"{sinav_adi}{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper()

    return {
        "name": sinav_adi or f"Sinav {sinif}-{sube}",
        "exam_code": exam_code,
        "grade": sinif,
        "section": sube,
        "duration": sure,
        "questions": questions,
        "total_questions": len(questions),
        "created_at": datetime.now().isoformat(),
        "scoring_system": 100,
        "point_per_question": round(100 / max(len(questions), 1), 2),
    }


def render_question_builder_new() -> None:
    """Yeni basit ve calisan soru olusturma arayuzu."""

    _init_state()

    # Baslik
    st.title("Soru Olusturma")
    st.markdown("---")

    # ========== ADIM 1: SINAV TIPI VE SINIF SECIMI ==========
    st.subheader("1. Sinav Tipi ve Sinif Bilgileri")

    # Sinav tipi secimi - EN ONEMLI AYAR
    st.markdown("##### Sinav Formatı (MEB/ÖSYM Uyumlu)")
    sinav_tipi_options = {
        "LGS - Liselere Geçiş Sınavı": "LGS",
        "TYT - Temel Yeterlilik Testi": "TYT",
        "AYT - Alan Yeterlilik Testi": "AYT",
        "Deneme - Genel Deneme Sınavı": "Deneme",
    }
    current_sinav_tipi = st.session_state.get("qb_sinav_tipi", "Deneme")
    current_idx = list(sinav_tipi_options.values()).index(current_sinav_tipi) if current_sinav_tipi in sinav_tipi_options.values() else 3

    sinav_tipi_display = st.selectbox(
        "Sınav Tipi",
        list(sinav_tipi_options.keys()),
        index=current_idx,
        key="sinav_tipi_select",
        help="Seçilen sınav tipine göre sorular MEB/ÖSYM formatında üretilir"
    )
    sinav_tipi = sinav_tipi_options[sinav_tipi_display]
    st.session_state.qb_sinav_tipi = sinav_tipi

    # Sinav tipi bilgisi
    sinav_config = SINAV_TIPLERI.get(sinav_tipi, {})
    visual_ratio = int(sinav_config.get("visual_ratio", 0.5) * 100)
    st.info(f"**{sinav_config.get('name', sinav_tipi)}**: {sinav_config.get('description', '')} | Görsel oran: %{visual_ratio}")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        kademe = st.selectbox(
            "Kademe",
            list(SINIF_SEVIYELERI.keys()),
            index=list(SINIF_SEVIYELERI.keys()).index(st.session_state.qb_kademe),
            key="kademe_select"
        )
        st.session_state.qb_kademe = kademe

    with col2:
        siniflar = SINIF_SEVIYELERI[kademe]
        default_idx = siniflar.index(st.session_state.qb_sinif) if st.session_state.qb_sinif in siniflar else 0
        sinif = st.selectbox(
            "Sinif",
            siniflar,
            index=default_idx,
            key="sinif_select"
        )
        st.session_state.qb_sinif = sinif

    with col3:
        sube = st.selectbox(
            "Sube",
            ["A", "B", "C", "D", "E"],
            index=["A", "B", "C", "D", "E"].index(st.session_state.qb_sube),
            key="sube_select"
        )
        st.session_state.qb_sube = sube

    st.markdown("---")

    # ========== ADIM 2: DERS SECIMI ==========
    st.subheader("2. Ders ve Soru Sayisi")

    # Hizli secim butonlari
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Sayisal Sec", use_container_width=True):
            st.session_state.qb_secili_dersler = DERSLER["Sayisal"].copy()
            st.rerun()
    with col2:
        if st.button("Sozel Sec", use_container_width=True):
            st.session_state.qb_secili_dersler = DERSLER["Sozel"].copy()
            st.rerun()
    with col3:
        if st.button("Tumu Sec", use_container_width=True):
            st.session_state.qb_secili_dersler = TUM_DERSLER.copy()
            st.rerun()
    with col4:
        if st.button("Temizle", use_container_width=True):
            st.session_state.qb_secili_dersler = []
            st.session_state.qb_ders_soru_sayilari = {}
            st.rerun()

    st.write("")

    # Ders secimi
    secili_dersler = st.multiselect(
        "Dersler",
        TUM_DERSLER,
        default=st.session_state.qb_secili_dersler,
        key="ders_multi"
    )
    st.session_state.qb_secili_dersler = secili_dersler

    # Soru sayilari
    if secili_dersler:
        st.write("**Her ders icin soru sayisi:**")

        # Toplu atama - daha belirgin
        st.markdown("##### Toplu Soru Sayisi Atama")
        col_toplu1, col_toplu2, col_toplu3 = st.columns([2, 1, 2])
        with col_toplu1:
            toplu_sayi = st.number_input(
                "Soru sayisi",
                min_value=0,
                max_value=50,
                value=5,
                key="toplu_sayi",
                help="Bu sayiyi tum secili derslere uygulayabilirsiniz"
            )
        with col_toplu2:
            st.write("")  # Bosluk
            st.write("")  # Hizalama icin
            if st.button("Tum Derslere Uygula", key="toplu_uygula", type="primary", use_container_width=True):
                for ders in secili_dersler:
                    st.session_state.qb_ders_soru_sayilari[ders] = toplu_sayi
                st.rerun()
        with col_toplu3:
            st.write("")
            st.write("")
            if st.button("Sifirla", key="sifirla_btn", use_container_width=True):
                for ders in secili_dersler:
                    st.session_state.qb_ders_soru_sayilari[ders] = 0
                st.rerun()

        st.markdown("---")
        st.markdown("##### Ders Bazli Ayarlama")

        # Ders bazli soru sayilari
        cols = st.columns(min(len(secili_dersler), 4))
        for i, ders in enumerate(secili_dersler):
            with cols[i % 4]:
                mevcut = st.session_state.qb_ders_soru_sayilari.get(ders, 5)
                sayi = st.number_input(
                    ders,
                    min_value=0,
                    max_value=50,
                    value=mevcut,
                    key=f"sayi_{ders}"
                )
                st.session_state.qb_ders_soru_sayilari[ders] = sayi

        # Toplam
        st.write("")
        toplam = sum(st.session_state.qb_ders_soru_sayilari.get(d, 0) for d in secili_dersler)
        if toplam > 0:
            col_ozet1, col_ozet2 = st.columns(2)
            with col_ozet1:
                st.success(f"**Toplam: {toplam} soru**")
            with col_ozet2:
                st.info(f"**{len(secili_dersler)} ders secili**")
        else:
            st.warning("Lutfen en az bir ders icin soru sayisi girin!")
    else:
        st.info("Yukaridan ders secin.")

    st.markdown("---")

    # ========== ADIM 3: SINAV AYARLARI ==========
    st.subheader("3. Sinav Ayarlari")

    col1, col2, col3 = st.columns(3)

    with col1:
        soru_tipi = st.selectbox(
            "Soru Tipi",
            SORU_TIPLERI,
            index=0,
            key="soru_tipi_select"
        )
        st.session_state.qb_soru_tipi = soru_tipi

    with col2:
        zorluk = st.selectbox(
            "Zorluk",
            ZORLUK_SEVIYELERI,
            index=ZORLUK_SEVIYELERI.index(st.session_state.qb_zorluk),
            key="zorluk_select"
        )
        st.session_state.qb_zorluk = zorluk

    with col3:
        sure = st.number_input(
            "Sure (dk)",
            min_value=5,
            max_value=180,
            value=st.session_state.qb_sure,
            step=5,
            key="sure_input"
        )
        st.session_state.qb_sure = sure

    sinav_adi = st.text_input(
        "Sinav Adi (istege bagli)",
        value=st.session_state.qb_sinav_adi,
        placeholder=f"Ornek: {sinif}. Sinif 1. Donem 2. Yazili",
        key="sinav_adi_input"
    )
    st.session_state.qb_sinav_adi = sinav_adi

    # AI Ayarlari
    with st.expander("AI Destekli Soru Uretimi", expanded=False):
        st.markdown("##### Yapay Zeka ile Kaliteli Sorular")

        # AI durumunu kontrol et
        ai_status = get_ai_status()

        # API Key giris alanlari
        col_ai1, col_ai2 = st.columns(2)

        with col_ai1:
            st.markdown("**OpenAI (GPT)**")
            if ai_status["openai_key"]:
                st.success("API Key tanimli", icon="✅")
            else:
                if not OPENAI_AVAILABLE:
                    st.error("openai paketi yuklu degil")
                else:
                    new_openai_key = st.text_input(
                        "OpenAI API Key",
                        type="password",
                        placeholder="sk-...",
                        key="openai_key_input",
                        label_visibility="collapsed"
                    )
                    if new_openai_key and new_openai_key.startswith("sk-"):
                        st.session_state.qb_openai_key = new_openai_key
                        st.success("Kaydedildi!")
                        st.rerun()

        with col_ai2:
            st.markdown("**Anthropic (Claude)**")
            if ai_status["anthropic_key"]:
                st.success("API Key tanimli", icon="✅")
            else:
                if not ANTHROPIC_AVAILABLE:
                    st.warning("anthropic paketi yuklu degil")
                else:
                    new_anthropic_key = st.text_input(
                        "Anthropic API Key",
                        type="password",
                        placeholder="sk-ant-...",
                        key="anthropic_key_input",
                        label_visibility="collapsed"
                    )
                    if new_anthropic_key and "ant" in new_anthropic_key:
                        st.session_state.qb_anthropic_key = new_anthropic_key
                        st.success("Kaydedildi!")
                        st.rerun()

        st.markdown("---")

        # AI aktiflestime
        use_ai = st.checkbox(
            "AI ile soru uret (mufredata uygun, kaliteli sorular)",
            value=st.session_state.qb_use_ai,
            disabled=not ai_status["any_ai_ready"],
            key="use_ai_check"
        )
        st.session_state.qb_use_ai = use_ai

        if use_ai and ai_status["any_ai_ready"]:
            # Provider secimi
            providers = []
            if ai_status["openai_key"] and OPENAI_AVAILABLE:
                providers.append("OpenAI (GPT)")
            if ai_status["anthropic_key"] and ANTHROPIC_AVAILABLE:
                providers.append("Anthropic (Claude)")
            providers.append("Otomatik (Ilk Uygun)")

            provider_choice = st.radio(
                "AI Saglayici",
                providers,
                index=len(providers) - 1,
                horizontal=True,
                key="ai_provider_radio"
            )

            # Provider mapping
            if "OpenAI" in provider_choice:
                st.session_state.qb_ai_provider = "openai"
            elif "Anthropic" in provider_choice:
                st.session_state.qb_ai_provider = "anthropic"
            else:
                st.session_state.qb_ai_provider = "auto"

            st.markdown("---")
            st.markdown("##### Profesyonel Soru Kalitesi Ayarlari")
            st.caption("OSYM/MEB standartlarinda soru uretimi icin gelismis ayarlar")

            col_q1, col_q2 = st.columns(2)

            with col_q1:
                # Soru formati secimi
                format_options = {
                    "Otomatik (Onerilen)": "otomatik",
                    "Klasik (Dogrudan soru)": "klasik",
                    "Paragraf Tabanli": "paragraf",
                    "Senaryo/Problem": "senaryo",
                    "Tablo/Veri Analizi": "tablo",
                    "Grafik Yorumlama": "grafik_aciklama",
                    "Karsilastirmali": "karsilastirma",
                }
                format_choice = st.selectbox(
                    "Soru Formati",
                    list(format_options.keys()),
                    index=0,
                    key="qb_format_select",
                    help="Sorularin sunulus bicimini belirler"
                )
                st.session_state.qb_question_format = format_options[format_choice]

            with col_q2:
                # Bloom taksonomisi secimi
                bloom_options = {
                    "Otomatik (Zorluga Gore)": "otomatik",
                    "Hatirlama (Temel)": "hatirlama",
                    "Anlama (Kavrama)": "anlama",
                    "Uygulama (Problem Cozme)": "uygulama",
                    "Analiz (Inceleme)": "analiz",
                    "Degerlendirme (Yargilama)": "degerlendirme",
                    "Sentez (Olusturma)": "sentez",
                }
                bloom_choice = st.selectbox(
                    "Bilissel Seviye (Bloom)",
                    list(bloom_options.keys()),
                    index=0,
                    key="qb_bloom_select",
                    help="Sorularin olctugu dusunme becerisi seviyesi"
                )
                st.session_state.qb_bloom_level = bloom_options[bloom_choice]

            # Secime gore bilgi
            if st.session_state.qb_question_format != "otomatik":
                format_desc = SORU_FORMATLARI.get(st.session_state.qb_question_format, {}).get("description", "")
                st.caption(f"Secilen format: {format_desc}")

            st.success("AI Pro aktif: OSYM/MEB kalitesinde, celdirici tasarimli, bilissel seviyeye uygun sorular uretilecek.")

        elif not ai_status["any_ai_ready"]:
            st.warning("AI kullanmak icin en az bir API key girmeniz gerekiyor.")

    # Gorsel Soru Ayarlari
    with st.expander("Gorsel Sorular (Grafik, Sekil, Diyagram)", expanded=True):
        use_visuals = st.checkbox(
            "Gorsel sorular uret (geometri sekilleri, grafikler, diyagramlar)",
            value=st.session_state.qb_use_visuals,
            key="use_visuals_check"
        )
        st.session_state.qb_use_visuals = use_visuals

        if use_visuals:
            st.success("Gorsel sorular aktif: Matematik, Fizik, Kimya, Biyoloji ve Cografya derslerinde sekilli sorular olusturulacak.")
            st.caption("Icerilen gorsel turler: Ucgen, Dikdortgen, Daire, Fonksiyon Grafigi, Hiz-Zaman Grafigi, Kuvvet Diyagrami, Elektrik Devresi, Atom Modeli, pH Skalasi, Hucre Diyagrami, DNA Yapisi, Iklim Grafigi, Nufus Piramidi")

    st.markdown("---")

    # ========== ADIM 4: OLUSTUR ==========
    st.subheader("4. Sinav Olustur")

    # Validasyon
    can_generate = True
    errors = []

    if not secili_dersler:
        errors.append("Ders secilmedi")
        can_generate = False

    toplam = sum(st.session_state.qb_ders_soru_sayilari.get(d, 0) for d in secili_dersler)
    if toplam == 0:
        errors.append("Soru sayisi 0")
        can_generate = False

    if errors:
        for err in errors:
            st.error(f"Eksik: {err}")

    # Ozet
    if can_generate:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sinif", f"{sinif}/{sube}")
        with col2:
            st.metric("Toplam Soru", toplam)
        with col3:
            st.metric("Sure", f"{sure} dk")
        with col4:
            st.metric("Zorluk", zorluk)

    st.write("")

    # Olustur butonu
    if st.button("SINAV OLUSTUR", type="primary", use_container_width=True, disabled=not can_generate):
        with st.spinner("Sinav olusturuluyor..."):
            # Soru sayilarini filtrele
            ders_sayilari = {d: st.session_state.qb_ders_soru_sayilari.get(d, 0) for d in secili_dersler}

            # Sinav olustur - MEB/OSYM formatinda kalite ayarlariyla
            q_format = st.session_state.get("qb_question_format", "otomatik")
            b_level = st.session_state.get("qb_bloom_level", "otomatik")
            s_tipi = st.session_state.get("qb_sinav_tipi", "Deneme")

            exam = _generate_exam(
                sinav_adi=sinav_adi,
                sinif=sinif,
                sube=sube,
                ders_sayilari=ders_sayilari,
                zorluk=zorluk,
                sure=sure,
                use_ai=st.session_state.qb_use_ai,
                use_visuals=st.session_state.qb_use_visuals,
                ai_provider=st.session_state.get("qb_ai_provider", "auto"),
                question_format=None if q_format == "otomatik" else q_format,
                bloom_level=None if b_level == "otomatik" else b_level,
                sinav_tipi=s_tipi
            )

            st.session_state.qb_olusturulan_sinav = exam
            st.success(f"Sinav basariyla olusturuldu! ({exam['total_questions']} soru)")

    st.markdown("---")

    # ========== SONUC ==========
    if st.session_state.qb_olusturulan_sinav:
        exam = st.session_state.qb_olusturulan_sinav

        st.subheader("Olusturulan Sinav")

        # Bilgiler
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Sinav Adi:** {exam['name']}")
            st.write(f"**Kod:** {exam['exam_code']}")
        with col2:
            st.write(f"**Sinif:** {exam['grade']}/{exam['section']}")
            st.write(f"**Sure:** {exam['duration']} dakika")
        with col3:
            st.write(f"**Soru Sayisi:** {exam['total_questions']}")
            st.write(f"**Soru Basi Puan:** {exam['point_per_question']}")

        st.write("")

        # Sorulari goster
        if st.checkbox("Sorulari Goster", key="show_questions"):
            for q in exam["questions"]:
                # Gorsel soru varsa etiketle
                has_visual = q.get("image_bytes") is not None
                visual_tag = " [GORSEL]" if has_visual else ""

                with st.expander(f"Soru {q['number']} - {q['subject']} ({q['difficulty']}){visual_tag}"):
                    # Gorsel varsa goster
                    if has_visual:
                        try:
                            st.image(q["image_bytes"], use_container_width=True)
                        except Exception:
                            st.warning("Gorsel yuklenemedi")

                    st.write(f"**{q['text']}**")
                    st.write("")
                    for i, opt in enumerate(q["options"]):
                        letter = chr(65 + i)  # A, B, C, D
                        if letter == q["answer"]:
                            st.success(f"**{letter}) {opt}**")
                        else:
                            st.write(f"{letter}) {opt}")

        st.write("")

        # Indirme secenekleri
        exam_text = _generate_exam_text(exam)
        answer_key = _generate_answer_key(exam)

        # PDF icin exam'i hazirla
        pdf_exam = _prepare_exam_for_pdf(exam)
        pdf_bytes = None
        try:
            from views.question_builder_module import build_exam_pdf
            pdf_bytes = build_exam_pdf(pdf_exam)
        except Exception:
            pass

        st.markdown("#### Indirme Secenekleri")

        # Gorsel soru sayisini goster
        visual_count = sum(1 for q in exam["questions"] if q.get("image_bytes"))
        if visual_count > 0:
            st.info(f"Bu sinavda {visual_count} gorsel soru var. PDF formatinda indirildiginde sekiller gorunur olacak.")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if pdf_bytes:
                st.download_button(
                    "PDF Indir (Gorselli)",
                    data=pdf_bytes,
                    file_name=f"{exam['name'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            else:
                st.button("PDF (Kullanilamiyor)", disabled=True, use_container_width=True)
        with col2:
            st.download_button(
                "TXT Indir",
                data=exam_text,
                file_name=f"{exam['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col3:
            st.download_button(
                "Cevap Anahtari",
                data=answer_key,
                file_name=f"{exam['name'].replace(' ', '_')}_cevap.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col4:
            if st.button("Yeni Sinav", use_container_width=True):
                st.session_state.qb_olusturulan_sinav = None
                st.rerun()

    # ========== PDF'DEN SORU YUKLE ==========
    st.markdown("---")
    with st.expander("PDF'den Soru Yukle (Metin Tabanli)", expanded=False):
        _render_pdf_import_section()


def _render_pdf_import_section():
    """PDF'den soru yukleme bolumu."""
    st.markdown("##### Disaridan PDF Yukleyerek Soru Aktar")
    st.caption("PDF dosyasindaki sorulari otomatik olarak ayirir ve bagimsiz sorular haline getirir.")

    # PDF kutuphanesi kontrolu
    if not PDF_AVAILABLE:
        st.error("PDF okuma icin PyMuPDF veya pdfplumber kutuphanesi gerekli.")
        st.code("pip install PyMuPDF pdfplumber", language="bash")
        return

    # PDF yukle
    uploaded_pdf = st.file_uploader(
        "PDF Dosyasi Yukle",
        type=["pdf"],
        key="qb_pdf_import_file",
        help="Soru iceren PDF dosyasini yukleyin"
    )

    if uploaded_pdf is not None:
        from utils.security import validate_upload
        _ok, _msg = validate_upload(uploaded_pdf, allowed_types=["pdf"], max_mb=100)
        if not _ok:
            st.error(f"⚠️ {_msg}")
            uploaded_pdf = None

    if uploaded_pdf is None:
        st.info("Soru iceren bir PDF dosyasi yukleyin. Sorular otomatik olarak ayristirilacak.")
        return

    # Ayarlar
    col1, col2, col3 = st.columns(3)
    with col1:
        import_subject = st.selectbox(
            "Ders",
            TUM_DERSLER,
            key="qb_pdf_import_subject"
        )
    with col2:
        import_difficulty = st.selectbox(
            "Zorluk",
            ["Kolay", "Orta", "Zor"],
            index=1,
            key="qb_pdf_import_difficulty"
        )
    with col3:
        use_ai_parse = st.checkbox(
            "AI ile Ayristir",
            value=False,
            key="qb_pdf_import_use_ai",
            help="AI kullanarak daha iyi soru ayristirma (API key gerekli)"
        )

    # PDF'i isle butonu
    if st.button("PDF'i Isele ve Sorulari Ayir", type="primary", key="qb_pdf_import_process"):
        with st.spinner("PDF isleniyor..."):
            # Metni cikar
            pdf_bytes = uploaded_pdf.read()
            text = _extract_text_from_pdf(pdf_bytes)

            if not text:
                st.error("PDF'den metin cikaralamadi. PDF'in metin katmani oldugundan emin olun.")
                return

            # Sorulari ayikla
            questions = _parse_questions_from_text(text, use_ai=use_ai_parse)

            if not questions:
                st.warning("PDF'den soru ayiklanamadi. Farkli bir format deneyin veya AI kullanin.")
                # Ham metni goster
                with st.expander("Ham PDF Metni"):
                    st.text_area("Cikartilan metin", text[:5000], height=300)
                return

            # Sorulari session state'e kaydet
            for q in questions:
                q["subject"] = import_subject
                q["difficulty"] = import_difficulty

            st.session_state.qb_imported_questions = questions
            st.success(f"{len(questions)} soru basariyla ayiklandi!")

    # Ayiklanan sorulari goster ve duzenle
    if st.session_state.get("qb_imported_questions"):
        questions = st.session_state.qb_imported_questions

        st.markdown("##### Ayiklanan Sorular")
        st.info(f"Toplam {len(questions)} soru bulundu. Duzenleyip sinava ekleyebilirsiniz.")

        # Secim icin checkbox'lar
        selected_indices = []

        for i, q in enumerate(questions):
            with st.expander(f"Soru {q['number']}: {q['text'][:50]}...", expanded=False):
                # Soru metni duzenleme
                new_text = st.text_area(
                    "Soru Metni",
                    value=q["text"],
                    key=f"qb_pdf_q_text_{i}",
                    height=100
                )
                q["text"] = new_text

                # Siklar
                st.write("**Siklar:**")
                for j, opt in enumerate(q.get("options", [])[:4]):
                    letter = chr(65 + j)
                    new_opt = st.text_input(
                        f"{letter})",
                        value=opt,
                        key=f"qb_pdf_q_opt_{i}_{j}"
                    )
                    if j < len(q["options"]):
                        q["options"][j] = new_opt

                # Dogru cevap
                current_answer = q.get("answer", "A")
                answer_idx = ord(current_answer.upper()) - 65 if current_answer else 0
                answer_idx = min(answer_idx, 3)
                new_answer = st.selectbox(
                    "Dogru Cevap",
                    ["A", "B", "C", "D"],
                    index=answer_idx,
                    key=f"qb_pdf_q_answer_{i}"
                )
                q["answer"] = new_answer

                # Sec/kaldir
                selected = st.checkbox("Bu soruyu ekle", value=True, key=f"qb_pdf_q_select_{i}")
                if selected:
                    selected_indices.append(i)

        # Secilen sorulari sinava ekle veya bankaya kaydet
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Secilen Soru", len(selected_indices))

        with col2:
            if st.button("Sinava Ekle", type="primary", key="qb_pdf_add_to_exam"):
                if not selected_indices:
                    st.warning("Lutfen en az bir soru secin.")
                else:
                    # Mevcut sinava ekle veya yeni sinav olustur
                    selected_questions = [questions[i].copy() for i in selected_indices]

                    if st.session_state.get("qb_olusturulan_sinav"):
                        # Mevcut sinava ekle
                        exam = st.session_state.qb_olusturulan_sinav
                        start_num = len(exam["questions"]) + 1
                        for idx, q in enumerate(selected_questions):
                            q["number"] = start_num + idx
                            q["grade"] = exam.get("grade", 9)
                            exam["questions"].append(q)
                        exam["total_questions"] = len(exam["questions"])
                        exam["point_per_question"] = round(100 / max(len(exam["questions"]), 1), 2)
                        st.success(f"{len(selected_questions)} soru mevcut sinava eklendi!")
                    else:
                        # Yeni sinav olustur
                        exam = {
                            "name": f"PDF Import - {uploaded_pdf.name}",
                            "exam_code": hashlib.md5(f"pdf_{datetime.now().isoformat()}".encode()).hexdigest()[:8].upper(),
                            "grade": st.session_state.get("qb_sinif", 9),
                            "section": st.session_state.get("qb_sube", "A"),
                            "duration": st.session_state.get("qb_sure", 40),
                            "questions": [],
                            "total_questions": 0,
                            "created_at": datetime.now().isoformat(),
                            "scoring_system": 100,
                            "point_per_question": 0,
                        }
                        for idx, q in enumerate(selected_questions):
                            q["number"] = idx + 1
                            q["grade"] = exam["grade"]
                            exam["questions"].append(q)
                        exam["total_questions"] = len(exam["questions"])
                        exam["point_per_question"] = round(100 / max(len(exam["questions"]), 1), 2)
                        st.session_state.qb_olusturulan_sinav = exam
                        st.success(f"{len(selected_questions)} soruyla yeni sinav olusturuldu!")

                    # Import listesini temizle
                    st.session_state.qb_imported_questions = None
                    st.rerun()

        with col3:
            if st.button("Bankaya Kaydet", key="qb_pdf_save_to_bank", help="Secilen sorulari kalici soru bankasina kaydet"):
                if not selected_indices:
                    st.warning("Lutfen en az bir soru secin.")
                else:
                    selected_questions = [questions[i].copy() for i in selected_indices]
                    try:
                        # Soru bankasi fonksiyonlarini import et
                        from views.question_builder import add_to_question_bank

                        # Sorulari banka formatina cevir
                        bank_questions = []
                        for q in selected_questions:
                            bank_q = {
                                "id": hashlib.md5(f"{q['text']}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
                                "text": q["text"],
                                "options": q.get("options", []),
                                "answer": q.get("answer", "A"),
                                "subject": q.get("subject", "Genel"),
                                "difficulty": q.get("difficulty", "Orta"),
                                "grade": st.session_state.get("qb_sinif", 9),
                                "question_type": "Coktan Secmeli (ABCD)",
                                "source": "pdf-import",
                                "created_at": datetime.now().isoformat(),
                            }
                            bank_questions.append(bank_q)

                        # Bankaya ekle
                        add_to_question_bank(bank_questions)
                        st.success(f"{len(bank_questions)} soru kalici olarak soru bankasina kaydedildi!")

                        # Import listesini temizle
                        st.session_state.qb_imported_questions = None
                        st.rerun()

                    except Exception as e:
                        st.error(f"Soru bankasina kaydetme hatasi: {e}")

        with col4:
            if st.button("Temizle", key="qb_pdf_clear"):
                st.session_state.qb_imported_questions = None
                st.rerun()


def _prepare_exam_for_pdf(exam: dict) -> dict:
    """Sinav verisini PDF modulu icin hazirla."""
    # Sorulari PDF formatina cevir
    pdf_questions = []
    for q in exam["questions"]:
        pdf_q = {
            "number": q.get("number", 1),
            "text": q.get("text", ""),
            "question_type": "Coktan Secmeli (ABCD)",
            "options": q.get("options", []),
            "answer": q.get("answer", "A"),
            "subject": q.get("subject", "Matematik"),
            "difficulty": q.get("difficulty", "Orta"),
            "topic": q.get("topic", ""),
        }
        # Gorsel varsa ekle
        if q.get("image_bytes"):
            pdf_q["image_bytes"] = q["image_bytes"]
        pdf_questions.append(pdf_q)

    # Ders dagilimini hesapla
    subject_counts = {}
    for q in pdf_questions:
        subject = q.get("subject", "Matematik")
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    return {
        "exam_name": exam.get("name", "Sinav"),
        "exam_code": exam.get("exam_code", ""),
        "exam_type": "Deneme Sinavi",
        "grade": exam.get("grade", 9),
        "section": exam.get("section", "A"),
        "duration": exam.get("duration", 60),
        "questions": pdf_questions,
        "subject_counts": subject_counts,
        "booklet_type": "A",
        "school_name": st.session_state.get("school_name", "Okul"),
        "brand_primary": st.session_state.get("brand_primary", "#0F4C81"),
        "brand_secondary": st.session_state.get("brand_secondary", "#F2A900"),
        "include_topic_distribution": False,
        "cover_instructions": [
            "Bu test, Coktan Secmeli ve Dogru/Yanlis sorulardan olusmaktadir.",
            "Cevaplarınızı, cevap kağıdının ilgili bölümüne isaretleyiniz.",
            "Her soru esit puana sahiptir.",
            "Sinav suresi bitince kalemlerinizi birakiniz.",
        ],
    }


def _generate_exam_text(exam: dict) -> str:
    """Sinavi text formatinda olustur."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"SINAV: {exam['name']}")
    lines.append(f"Sinif: {exam['grade']}/{exam['section']}  |  Sure: {exam['duration']} dk  |  Kod: {exam['exam_code']}")
    lines.append("=" * 60)
    lines.append("")

    for q in exam["questions"]:
        visual_tag = " [GORSEL SORU]" if q.get("image_bytes") else ""
        lines.append(f"SORU {q['number']}: ({q['subject']}){visual_tag}")
        if q.get("image_bytes"):
            lines.append("[Bu soruda bir gorsel/sekil vardir - PDF ciktida gorunecektir]")
        lines.append(q["text"])
        lines.append("")
        for i, opt in enumerate(q["options"]):
            letter = chr(65 + i)
            lines.append(f"   {letter}) {opt}")
        lines.append("")
        lines.append("-" * 40)
        lines.append("")

    return "\n".join(lines)


def _generate_answer_key(exam: dict) -> str:
    """Cevap anahtari olustur."""
    lines = []
    lines.append("=" * 40)
    lines.append(f"CEVAP ANAHTARI: {exam['name']}")
    lines.append(f"Kod: {exam['exam_code']}")
    lines.append("=" * 40)
    lines.append("")

    for q in exam["questions"]:
        lines.append(f"Soru {q['number']}: {q['answer']}")

    lines.append("")
    lines.append("-" * 40)
    lines.append(f"Toplam: {exam['total_questions']} soru")
    lines.append(f"Soru basi puan: {exam['point_per_question']}")

    return "\n".join(lines)
