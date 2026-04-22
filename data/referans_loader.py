# -*- coding: utf-8 -*-
"""
Universal Referans Veri Yukleyici
Tum siniflar ve dersler icin MEB onayli referans verilerini yukler.
1-12. sinif, tum dersler desteklenir.
"""
import logging
_logger = logging.getLogger("referans_loader")

# ═══════════════════════════════════════════════════════════════
# REFERANS HARITASI: (sinif, ders_anahtar) -> (modul, dict_adi, arama_fonksiyonu)
# ═══════════════════════════════════════════════════════════════

_REFERANS_MAP = {
    # 1. sinif
    (1, "turkce"):      ("data.turkce_1_referans", "TURKCE_1_REFERANS", "get_turkce1_reference"),
    (1, "matematik"):   ("data.matematik_1_referans", "MATEMATIK_1_REFERANS", "get_matematik1_reference"),
    (1, "hayat"):       ("data.hayat_bilgisi_1_referans", "HAYAT_BILGISI_1_REFERANS", "get_hayat_bilgisi1_reference"),
    # 2. sinif
    (2, "turkce"):      ("data.turkce_2_referans", "TURKCE_2_REFERANS", "get_turkce2_reference"),
    (2, "matematik"):   ("data.matematik_2_referans", "MATEMATIK_2_REFERANS", "get_matematik2_reference"),
    (2, "hayat"):       ("data.hayat_bilgisi_2_referans", "HAYAT_BILGISI_2_REFERANS", "get_hayat_bilgisi2_reference"),
    # 3. sinif
    (3, "turkce"):      ("data.turkce_3_referans", "TURKCE_3_REFERANS", "get_turkce3_reference"),
    (3, "matematik"):   ("data.matematik_3_referans", "MATEMATIK_3_REFERANS", "get_matematik3_reference"),
    (3, "fen"):         ("data.fen_3_referans", "FEN_3_REFERANS", "get_fen3_reference"),
    (3, "hayat"):       ("data.hayat_bilgisi_3_referans", "HAYAT_BILGISI_3_REFERANS", "get_hayat_bilgisi3_reference"),
    # 4. sinif
    (4, "turkce"):      ("data.turkce_4_referans", "TURKCE_4_REFERANS", "get_turkce4_reference"),
    (4, "matematik"):   ("data.matematik_4_referans", "MATEMATIK_4_REFERANS", "get_matematik4_reference"),
    (4, "fen"):         ("data.fen_4_referans", "FEN_4_REFERANS", "get_fen4_reference"),
    (4, "sosyal"):      ("data.sosyal_4_referans", "SOSYAL_4_REFERANS", "get_sosyal4_reference"),
    (4, "din"):         ("data.din_kulturu_4_referans", "DIN_KULTURU_4_REFERANS", "get_din_kulturu4_reference"),
    # 5. sinif
    (5, "turkce"):      ("data.turkce_5_referans", "TURKCE_5_REFERANS", "get_turkce5_reference"),
    (5, "matematik"):   ("data.matematik_5_referans", "MATEMATIK_5_REFERANS", "get_matematik5_reference"),
    (5, "fen"):         ("data.fen_5_referans", "FEN_5_REFERANS", "get_fen5_reference"),
    (5, "sosyal"):      ("data.sosyal_5_referans", "SOSYAL_5_REFERANS", "get_sosyal5_reference"),
    # 6. sinif
    (6, "turkce"):      ("data.turkce_6_referans", "TURKCE_6_REFERANS", "get_turkce6_reference"),
    (6, "matematik"):   ("data.matematik_6_referans", "MATEMATIK_6_REFERANS", "get_matematik6_reference"),
    (6, "fen"):         ("data.fen_6_referans", "FEN_6_REFERANS", "get_fen6_reference"),
    (6, "sosyal"):      ("data.sosyal_6_referans", "SOSYAL_6_REFERANS", "get_sosyal6_reference"),
    # 7. sinif
    (7, "turkce"):      ("data.turkce_7_referans", "TURKCE_7_REFERANS", "get_turkce7_reference"),
    (7, "matematik"):   ("data.matematik_7_referans", "MATEMATIK_7_REFERANS", "get_matematik7_reference"),
    (7, "fen"):         ("data.fen_7_referans", "FEN_7_REFERANS", "get_fen7_reference"),
    (7, "sosyal"):      ("data.sosyal_7_referans", "SOSYAL_7_REFERANS", "get_sosyal7_reference"),
    # 8. sinif
    (8, "turkce"):      ("data.turkce_8_referans", "TURKCE_8_REFERANS", "get_turkce8_reference"),
    (8, "matematik"):   ("data.matematik_8_referans", "MATEMATIK_8_REFERANS", "get_matematik8_reference"),
    (8, "fen"):         ("data.fen_8_referans", "FEN_8_REFERANS", "get_fen8_reference"),
    # 8. sinif inkilap ayri
    (8, "inkilap"):     ("data.inkilap_tarihi_8_referans", "INKILAP_REFERANS", None),
    # ═══════════════════════════════════════════════════════════════
    # 9. sinif (Lise)
    # ═══════════════════════════════════════════════════════════════
    (9, "matematik"):   ("data.matematik_9_referans", "MATEMATIK_9_REFERANS", "get_matematik9_reference"),
    (9, "fizik"):       ("data.fizik_9_referans", "FIZIK_9_REFERANS", "get_fizik9_reference"),
    (9, "kimya"):       ("data.kimya_9_referans", "KIMYA_9_REFERANS", "get_kimya9_reference"),
    (9, "biyoloji"):    ("data.biyoloji_9_referans", "BIYOLOJI_9_REFERANS", "get_biyoloji9_reference"),
    (9, "edebiyat"):    ("data.edebiyat_9_referans", "EDEBIYAT_9_REFERANS", "get_edebiyat9_reference"),
    (9, "tarih"):       ("data.tarih_9_referans", "TARIH_9_REFERANS", "get_tarih9_reference"),
    (9, "cografya"):    ("data.cografya_9_referans", "COGRAFYA_9_REFERANS", "get_cografya9_reference"),
    (9, "felsefe"):     ("data.felsefe_9_referans", "FELSEFE_9_REFERANS", "get_felsefe9_reference"),
    (9, "din"):         ("data.din_kulturu_9_referans", "DIN_KULTURU_9_REFERANS", "get_din_kulturu9_reference"),
    (9, "ingilizce"):   ("data.ingilizce_9_referans", "INGILIZCE_9_REFERANS", "get_ingilizce9_reference"),
    # ═══════════════════════════════════════════════════════════════
    # 10. sinif
    # ═══════════════════════════════════════════════════════════════
    (10, "matematik"):  ("data.matematik_10_referans", "MATEMATIK_10_REFERANS", "get_matematik10_reference"),
    (10, "fizik"):      ("data.fizik_10_referans", "FIZIK_10_REFERANS", "get_fizik10_reference"),
    (10, "kimya"):      ("data.kimya_10_referans", "KIMYA_10_REFERANS", "get_kimya10_reference"),
    (10, "biyoloji"):   ("data.biyoloji_10_referans", "BIYOLOJI_10_REFERANS", "get_biyoloji10_reference"),
    (10, "edebiyat"):   ("data.edebiyat_10_referans", "EDEBIYAT_10_REFERANS", "get_edebiyat10_reference"),
    (10, "tarih"):      ("data.tarih_10_referans", "TARIH_10_REFERANS", "get_tarih10_reference"),
    (10, "cografya"):   ("data.cografya_10_referans", "COGRAFYA_10_REFERANS", "get_cografya10_reference"),
    (10, "felsefe"):    ("data.felsefe_10_referans", "FELSEFE_10_REFERANS", "get_felsefe10_reference"),
    (10, "din"):        ("data.din_kulturu_10_referans", "DIN_KULTURU_10_REFERANS", "get_din_kulturu10_reference"),
    (10, "ingilizce"):  ("data.ingilizce_10_referans", "INGILIZCE_10_REFERANS", "get_ingilizce10_reference"),
    # ═══════════════════════════════════════════════════════════════
    # 11. sinif
    # ═══════════════════════════════════════════════════════════════
    (11, "matematik"):  ("data.matematik_11_referans", "MATEMATIK_11_REFERANS", "get_matematik11_reference"),
    (11, "fizik"):      ("data.fizik_11_referans", "FIZIK_11_REFERANS", "get_fizik11_reference"),
    (11, "kimya"):      ("data.kimya_11_referans", "KIMYA_11_REFERANS", "get_kimya11_reference"),
    (11, "biyoloji"):   ("data.biyoloji_11_referans", "BIYOLOJI_11_REFERANS", "get_biyoloji11_reference"),
    (11, "edebiyat"):   ("data.edebiyat_11_referans", "EDEBIYAT_11_REFERANS", "get_edebiyat11_reference"),
    (11, "tarih"):      ("data.tarih_11_referans", "TARIH_11_REFERANS", "get_tarih11_reference"),
    (11, "cografya"):   ("data.cografya_11_referans", "COGRAFYA_11_REFERANS", "get_cografya11_reference"),
    (11, "felsefe"):    ("data.felsefe_11_referans", "FELSEFE_11_REFERANS", "get_felsefe11_reference"),
    (11, "din"):        ("data.din_kulturu_11_referans", "DIN_KULTURU_11_REFERANS", "get_din_kulturu11_reference"),
    (11, "ingilizce"):  ("data.ingilizce_11_referans", "INGILIZCE_11_REFERANS", "get_ingilizce11_reference"),
    # ═══════════════════════════════════════════════════════════════
    # 12. sinif
    # ═══════════════════════════════════════════════════════════════
    (12, "matematik"):  ("data.matematik_12_referans", "MATEMATIK_12_REFERANS", "get_matematik12_reference"),
    (12, "fizik"):      ("data.fizik_12_referans", "FIZIK_12_REFERANS", "get_fizik12_reference"),
    (12, "kimya"):      ("data.kimya_12_referans", "KIMYA_12_REFERANS", "get_kimya12_reference"),
    (12, "biyoloji"):   ("data.biyoloji_12_referans", "BIYOLOJI_12_REFERANS", "get_biyoloji12_reference"),
    (12, "edebiyat"):   ("data.edebiyat_12_referans", "EDEBIYAT_12_REFERANS", "get_edebiyat12_reference"),
    (12, "tarih"):      ("data.tarih_12_referans", "TARIH_12_REFERANS", "get_tarih12_reference"),
    (12, "cografya"):   ("data.cografya_12_referans", "COGRAFYA_12_REFERANS", "get_cografya12_reference"),
    (12, "felsefe"):    ("data.felsefe_12_referans", "FELSEFE_12_REFERANS", "get_felsefe12_reference"),
    (12, "din"):        ("data.din_kulturu_12_referans", "DIN_KULTURU_12_REFERANS", "get_din_kulturu12_reference"),
    (12, "ingilizce"):  ("data.ingilizce_12_referans", "INGILIZCE_12_REFERANS", "get_ingilizce12_reference"),
}

# Ders adi -> anahtar esleme
_DERS_ANAHTAR_MAP = {
    "turkce": "turkce", "türkçe": "turkce",
    "matematik": "matematik", "mat": "matematik",
    "fen": "fen", "fen bilimleri": "fen", "fen bilgisi": "fen",
    "sosyal": "sosyal", "sosyal bilgiler": "sosyal",
    "hayat": "hayat", "hayat bilgisi": "hayat",
    "din": "din", "din kültürü": "din", "din kulturu": "din",
    "din kültürü ve ahlak bilgisi": "din",
    "inkilap": "inkilap", "inkılap": "inkilap", "inkılâp": "inkilap",
    "t.c. inkılap": "inkilap", "inkılap tarihi": "inkilap",
    "t.c. inkılap tarihi": "inkilap",
    # Lise dersleri
    "fizik": "fizik", "physics": "fizik",
    "kimya": "kimya", "chemistry": "kimya",
    "biyoloji": "biyoloji", "biology": "biyoloji", "bio": "biyoloji",
    "edebiyat": "edebiyat", "türk edebiyatı": "edebiyat", "turk edebiyati": "edebiyat",
    "türk dili ve edebiyatı": "edebiyat", "dil ve anlatım": "edebiyat",
    "tarih": "tarih", "history": "tarih", "t.c. inkılap tarihi ve atatürkçülük": "tarih",
    "coğrafya": "cografya", "cografya": "cografya", "geography": "cografya",
    "felsefe": "felsefe", "philosophy": "felsefe", "mantık": "felsefe",
    "ingilizce": "ingilizce", "İngilizce": "ingilizce", "english": "ingilizce",
    "yabancı dil": "ingilizce", "yabanci dil": "ingilizce",
}


def _normalize_turkish(text: str) -> str:
    """Turkce ozel karakterleri ASCII karsiliklarina cevirir."""
    _tr_map = str.maketrans("çğıöşüÇĞİÖŞÜâîûêÂÎÛÊ", "cgiosuCGIOSUaiueAIUE")
    return text.translate(_tr_map)


def _detect_sinif(seviye: str) -> int | None:
    """Seviye stringinden sinif numarasini cikarir."""
    if not seviye:
        return None
    s = seviye.lower().strip()
    # "5. sinif", "5.sinif", "sinif 5", "5" gibi formatlar
    import re
    m = re.search(r'(\d+)', s)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 12:
            return n
    return None


def _detect_ders_anahtar(ders: str) -> str | None:
    """Ders adini standart anahtara cevirir."""
    if not ders:
        return None
    d = ders.lower().strip()
    # Dogrudan esleme
    if d in _DERS_ANAHTAR_MAP:
        return _DERS_ANAHTAR_MAP[d]
    # Icinde gecen esleme
    for key, val in _DERS_ANAHTAR_MAP.items():
        if key in d:
            return val
    return None


def load_referans(ders: str, seviye: str, konu: str) -> tuple[str, bool]:
    """
    Verilen ders, seviye ve konu icin referans icerik yukler.

    Returns:
        (referans_text, is_verified) tuple
        referans_text: Referans icerik string (bos ise referans bulunamadi)
        is_verified: Referans verisi bulundu mu?
    """
    sinif = _detect_sinif(seviye)
    ders_key = _detect_ders_anahtar(ders)

    if not sinif or not ders_key:
        return "", False

    # Inkilap icin ozel handler (mevcut sistem korunuyor)
    if ders_key == "inkilap":
        return "", False  # Inkilap kendi ozel handler'ini kullaniyor

    map_key = (sinif, ders_key)
    if map_key not in _REFERANS_MAP:
        return "", False

    modul_adi, dict_adi, search_func_name = _REFERANS_MAP[map_key]

    try:
        import importlib
        mod = importlib.import_module(modul_adi)
        ref_dict = getattr(mod, dict_adi)
        search_func = getattr(mod, search_func_name) if search_func_name else None

        results = []

        # 1. Konu ile arama yap (farkli fonksiyon imzalarini destekle)
        if search_func and konu:
            try:
                matches = search_func(konu)
                if matches:
                    first = matches[0] if isinstance(matches, list) else matches
                    # Format 1: [(score, key, val), ...] — standart
                    if isinstance(first, (list, tuple)) and len(first) == 3:
                        for score, key, val in matches[:3]:
                            if isinstance(val, dict) and 'baslik' in val:
                                results.append(f"### {key}: {val['baslik']}\n{val['icerik']}")
                    # Format 2: dict dogrudan dondu (tek sonuc)
                    elif isinstance(first, dict) and 'baslik' in first:
                        results.append(f"### {konu}: {first['baslik']}\n{first['icerik']}")
            except (TypeError, ValueError):
                pass

        # 1b. Eger fonksiyon sonuc vermediyse, dict uzerinde fuzzy arama yap
        if not results and konu and ref_dict:
            import difflib
            _konu_lower = konu.lower()
            _konu_ascii = _normalize_turkish(_konu_lower)
            _scored = []
            for key, val in ref_dict.items():
                _searchable = f"{val.get('baslik','')} {val.get('unite','')} {val.get('icerik','')[:1500]}".lower()
                _searchable_ascii = _normalize_turkish(_searchable)
                _ratio = max(
                    difflib.SequenceMatcher(None, _konu_lower, _searchable).ratio(),
                    difflib.SequenceMatcher(None, _konu_ascii, _searchable_ascii).ratio()
                )
                _word_match = any(
                    w in _searchable or w in _searchable_ascii
                    for w in (_konu_lower.split() + _konu_ascii.split()) if len(w) > 3
                )
                if _ratio > 0.15 or _word_match:
                    _scored.append((_ratio + (0.3 if _word_match else 0), key, val))
            _scored.sort(key=lambda x: x[0], reverse=True)
            for _, key, val in _scored[:3]:
                results.append(f"### {key}: {val['baslik']}\n{val['icerik']}")

        # 2. Eger sonuc yoksa tum icerigi ver (kucuk dict'ler icin)
        if not results and len(ref_dict) <= 5:
            for key, val in ref_dict.items():
                results.append(f"### {key}: {val['baslik']}\n{val['icerik']}")

        if results:
            ref_text = "\n\n".join(results)
            # Max 8000 karakter (token limitini asmamak icin)
            if len(ref_text) > 8000:
                ref_text = ref_text[:8000] + "\n... (referans kisaltildi)"
            return ref_text, True

    except Exception as e:
        _logger.warning(f"Referans yuklenemedi ({modul_adi}): {e}")

    return "", False


def get_verified_ders_name(ders: str, seviye: str) -> str | None:
    """Referans verisi olan ders icin gorunen adi dondurur."""
    sinif = _detect_sinif(seviye)
    ders_key = _detect_ders_anahtar(ders)
    if not sinif or not ders_key:
        return None
    if (sinif, ders_key) in _REFERANS_MAP:
        _names = {
            "turkce": "Türkçe", "matematik": "Matematik",
            "fen": "Fen Bilimleri", "sosyal": "Sosyal Bilgiler",
            "hayat": "Hayat Bilgisi", "din": "Din Kültürü",
            "inkilap": "İnkılap Tarihi",
            "fizik": "Fizik", "kimya": "Kimya", "biyoloji": "Biyoloji",
            "edebiyat": "Türk Dili ve Edebiyatı", "tarih": "Tarih",
            "cografya": "Coğrafya", "felsefe": "Felsefe",
            "ingilizce": "İngilizce",
        }
        return f"{sinif}. Sınıf {_names.get(ders_key, ders_key.title())}"
    return None


def get_all_supported() -> list[tuple[int, str]]:
    """Desteklenen tum (sinif, ders) ciftlerini listeler."""
    return list(_REFERANS_MAP.keys())
