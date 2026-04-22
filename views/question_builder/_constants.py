"""
Soru Olusturma - Sabitler
=========================
Soru bankasi ve sinav olusturma icin kullanilan sabitler.
"""

from __future__ import annotations

import os

from utils.tenant import get_data_path

# Tenant dizin koku
TENANT_ROOT = get_data_path("tenants")

# Varsayilan sinav turleri
DEFAULT_EXAM_TYPES = [
    "Deneme Sinavi",
    "TYT",
    "Okul Yazilisi",
    "Bursluluk Sinavi",
    "Seviye Tespit Sinavi",
]

# Varsayilan soru tipleri
DEFAULT_QUESTION_TYPES = [
    "Coktan Secmeli (ABCD)",
    "Coktan Secmeli (ABCDE)",
    "Dogru/Yanlis",
    "Bosluk Doldurma",
    "Acik Uclu",
    "Klasik",
    "Karisik",
]

# Varsayilan dersler
DEFAULT_SUBJECTS = [
    "Matematik",
    "Fizik",
    "Kimya",
    "Biyoloji",
    "Turk Dili ve Edebiyati",
    "Tarih",
    "Cografya",
    "Felsefe",
    "Ingilizce",
    "Din Kulturu",
    "Psikoloji",
    "Sosyoloji",
]

# Kapak uyarilari
DEFAULT_COVER_RULES = [
    "Cevap kagidi uzerindeki kodlamalari kursun kalemle yapiniz.",
    "Degistirmek istediginiz bir cevabi, yumusak silgiyle cevap kagidini orselemeden temizce siliniz ve yeni cevabinizi kodlayiniz.",
    "Kitapcik turunu cevap kagidinizdaki ilgili alana kodlayiniz.",
    "Soru kitapcigi uzerinde yapilip cevap kagidina isaretlenmeyen cevaplar degerlendirmeye alinmaz.",
    "Puanlama; her test icin yanlis cevap sayisinin ucte biri dogru cevap sayisindan cikarilarak yapilir.",
]

# Turkce karakter normalizasyon haritasi
TR_CHAR_MAP = {
    "ı": "i", "İ": "I",
    "ş": "s", "Ş": "S",
    "ğ": "g", "Ğ": "G",
    "ü": "u", "Ü": "U",
    "ö": "o", "Ö": "O",
    "ç": "c", "Ç": "C",
}

# Hariç tutulan dersler
EXCLUDED_SUBJECTS = [
    "rehberlik",
    "beden egitimi",
    "muzik",
    "gorsel sanatlar",
    "guzel sanatlar",
    "is",
    "bilgi islem",
    "egzersiz",
    "spor",
    "futbol",
    "voleybol",
    "basketbol",
    "satranc",
    "sosyal etkinlik",
    "kulup",
    "haftalik denetim",
    "okuma saati",
]
