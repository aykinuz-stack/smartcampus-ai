"""
Akademik Takip — Veli Bildirim Otomasyon Motoru
=================================================
Akademik takip modulu icin proaktif veli iletisim sistemi.

Mevcut yapida AttendanceRecord modelinde 'veli_bildirim' alani var ama
gonderilmiyor. Bu modul tetikleyici + kuyruk + cron sistemini ekler.

Tetikleyiciler:
1. devamsizlik_kaydedildi  -> aninda WhatsApp + SMS bildirim
2. not_kaydedildi          -> 30dk gecikmeyle ozet bildirim
3. odev_son_tarihi_yakin   -> 1 gun once veliye hatirlatma
4. risk_seviyesi_yukseldi  -> aninda mudur + veli uyari
5. haftalik_ozet           -> her cuma 17:00 cron ile veliye haftalik rapor

Akis:
- Tetikleyici cagrisi → kuyruga gorev eklenir → planli zamanda gonderilir
- Tum gorevler veli_bildirim_log.json'a yazilir
- Cron her sayfa acilisinda (4 saatte 1) tarar, vakti gelmis gorevleri "gonderir"
"""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, date, timedelta
from typing import Any


# ============================================================
# SABLONLAR
# ============================================================

VELI_MESAJ_SABLONLARI = {
    "devamsizlik_anlik": (
        "Sayin {veli_adi}, {ogrenci_adi} bugun {tarih} tarihinde "
        "{ders_adi} dersinde devamsizlik yapmistir. Mazeret bildirmek "
        "icin lutfen okul ile iletisime gecin. {okul_adi}"
    ),
    "devamsizlik_tam_gun": (
        "Sayin {veli_adi}, {ogrenci_adi} bugun ({tarih}) okula gelmemistir. "
        "Saglik veya mazeret durumunda lutfen {telefon} numarasi ile bilgi verin. "
        "{okul_adi}"
    ),
    "not_bilgilendirme": (
        "Sayin {veli_adi}, {ogrenci_adi} icin yeni not girisi yapildi:\n"
        "Ders: {ders_adi}\n"
        "Sinav: {sinav_turu}\n"
        "Puan: {puan}/100\n"
        "Tarih: {tarih}\n\n"
        "Detaylar icin veli portalindan giris yapin. {okul_adi}"
    ),
    "odev_hatirlatma": (
        "Sayin {veli_adi}, {ogrenci_adi}'in {ders_adi} dersinden "
        "{odev_adi} adli odevin son teslim tarihi yarin ({tarih}). "
        "Lutfen ogrencinizin tamamladigindan emin olun. {okul_adi}"
    ),
    "risk_uyari": (
        "🚨 Sayin {veli_adi}, {ogrenci_adi} icin akademik risk uyarisi:\n"
        "Risk seviyesi: {risk_seviye}\n"
        "Faktorler: {faktorler}\n\n"
        "Acil veli gorusmesi onerilir. Lutfen {telefon} ile iletisime gecin. {okul_adi}"
    ),
    "haftalik_ozet": (
        "Sayin {veli_adi}, {ogrenci_adi}'in bu haftaki ozet raporu:\n\n"
        "📚 Yeni Notlar: {not_sayisi}\n"
        "✅ Devamsizlik: {devamsizlik}\n"
        "📝 Tamamlanan Odev: {odev_tamamlanan}\n"
        "⚠️ Bekleyen Odev: {odev_bekleyen}\n\n"
        "{ai_yorum}\n\n"
        "Detayli rapor icin veli portalimizi ziyaret edin. {okul_adi}"
    ),
    "kazanim_ilerlemesi": (
        "Sayin {veli_adi}, {ogrenci_adi}'in bu hafta {ders_adi} dersinde "
        "{kazanim_sayisi} yeni konu islendi. Konular: {kazanim_listesi}. "
        "Detaylar veli portalinda. {okul_adi}"
    ),
}

# Cron meta dosyasi
def _meta_path() -> str:
    try:
        from utils.tenant import get_data_path
        base = get_data_path("akademik")
    except Exception:
        base = os.path.join("data", "akademik")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "veli_bildirim_meta.json")


def _kuyruk_path() -> str:
    try:
        from utils.tenant import get_data_path
        base = get_data_path("akademik")
    except Exception:
        base = os.path.join("data", "akademik")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "veli_bildirim_kuyruk.json")


def _log_path() -> str:
    try:
        from utils.tenant import get_data_path
        base = get_data_path("akademik")
    except Exception:
        base = os.path.join("data", "akademik")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "veli_bildirim_log.json")


# ============================================================
# VERI MODELI — KuyrukGorev
# ============================================================

@dataclass
class VeliBildirimGorev:
    """Kuyruktaki veli bildirim gorevi."""
    id: str = field(default_factory=lambda: f"vb_{uuid.uuid4().hex[:10]}")
    tip: str = ""                 # devamsizlik / not / odev / risk / haftalik / kazanim
    ogrenci_id: str = ""
    veli_adi: str = ""
    veli_telefon: str = ""
    ogrenci_adi: str = ""
    sinif: str = ""
    konu: str = ""                # konu basligi
    mesaj: str = ""               # tam mesaj metni
    kanal: str = "whatsapp"        # whatsapp / sms / email
    olusturma_zamani: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    planlanan_zaman: str = ""      # ISO — bu zaman gelince gonderilir
    durum: str = "bekliyor"        # bekliyor / gonderildi / basarisiz / iptal
    gonderim_zamani: str = ""
    hata: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "VeliBildirimGorev":
        valid = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in d.items() if k in valid})


# ============================================================
# KUYRUK YONETIMI
# ============================================================

def _kuyrugu_yukle() -> list[VeliBildirimGorev]:
    p = _kuyruk_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return [VeliBildirimGorev.from_dict(d) for d in json.load(f) if isinstance(d, dict)]
    except (json.JSONDecodeError, OSError):
        return []


def _kuyrugu_kaydet(gorevler: list[VeliBildirimGorev]):
    with open(_kuyruk_path(), "w", encoding="utf-8") as f:
        json.dump([g.to_dict() for g in gorevler], f, ensure_ascii=False, indent=2)


def _gorev_ekle(gorev: VeliBildirimGorev):
    gorevler = _kuyrugu_yukle()
    gorevler.append(gorev)
    _kuyrugu_kaydet(gorevler)


def _log_yaz(gorev: VeliBildirimGorev, durum: str):
    """Log dosyasina yaz (son 1000 kayit)."""
    p = _log_path()
    logs = []
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            pass
    logs.append({
        "tarih": datetime.now().isoformat(timespec="seconds"),
        "id": gorev.id,
        "tip": gorev.tip,
        "ogrenci": gorev.ogrenci_adi,
        "veli": gorev.veli_adi,
        "kanal": gorev.kanal,
        "durum": durum,
        "konu": gorev.konu,
    })
    logs = logs[-1000:]
    with open(p, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# ============================================================
# OKUL VERISINI HAZIRLAMA
# ============================================================

def _okul_bilgisi() -> dict:
    """Kurum profilinden okul ad+telefon cek."""
    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili() or {}
        return {
            "okul_adi": kp.get("kurum_adi") or kp.get("okul_adi") or kp.get("name") or "Okulumuz",
            "telefon": kp.get("telefon") or kp.get("phone") or "0212 ...",
        }
    except Exception:
        return {"okul_adi": "Okulumuz", "telefon": "0212 ..."}


def _safe_get(obj, key: str, default=None):
    """Hem dataclass hem dict'ten guvenli okuma."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    val = getattr(obj, key, default)
    return val if val is not None else default


def _ogrenci_veli_bilgisi(store, ogrenci_id: str) -> dict | None:
    """Bir ogrencinin veli bilgisini cek."""
    try:
        students = store.get_students() or []
        for s in students:
            sid = _safe_get(s, "id", "")
            if sid == ogrenci_id:
                # Ad birlestirme
                ad = _safe_get(s, "ad", "")
                soyad = _safe_get(s, "soyad", "")
                ad_soyad = _safe_get(s, "ad_soyad", "") or f"{ad} {soyad}".strip() or "Ogrenci"

                # Veli adi — once veli_adi, sonra anne_adi, sonra baba_adi
                veli_adi = (
                    _safe_get(s, "veli_adi", "")
                    or (f"{_safe_get(s, 'anne_adi', '')} {_safe_get(s, 'anne_soyadi', '')}".strip())
                    or (f"{_safe_get(s, 'baba_adi', '')} {_safe_get(s, 'baba_soyadi', '')}".strip())
                    or "Sayin Veli"
                ).strip()

                # Veli telefon
                veli_telefon = (
                    _safe_get(s, "veli_telefon", "")
                    or _safe_get(s, "anne_telefon", "")
                    or _safe_get(s, "baba_telefon", "")
                    or ""
                )

                # Sinif
                sinif_str = (
                    _safe_get(s, "sinif", "")
                    or f"{_safe_get(s, 'sinif_no', '')}/{_safe_get(s, 'sube', '')}".strip("/")
                    or ""
                )

                return {
                    "ogrenci_adi": ad_soyad,
                    "veli_adi": veli_adi if veli_adi.strip() else "Sayin Veli",
                    "veli_telefon": veli_telefon,
                    "sinif": sinif_str,
                }
    except Exception:
        pass
    return None


# ============================================================
# TETIKLEYICILER
# ============================================================

def trigger_devamsizlik(store, ogrenci_id: str, ders_adi: str = "",
                         tarih: str = "", anlik: bool = True) -> bool:
    """Devamsizlik kaydedildiginde cagrilir. Anlik veli WhatsApp."""
    veli_bilgi = _ogrenci_veli_bilgisi(store, ogrenci_id)
    if not veli_bilgi:
        return False

    okul = _okul_bilgisi()
    sablon_key = "devamsizlik_anlik" if ders_adi else "devamsizlik_tam_gun"
    sablon = VELI_MESAJ_SABLONLARI[sablon_key]

    mesaj = sablon.format(
        veli_adi=veli_bilgi["veli_adi"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        ders_adi=ders_adi or "-",
        tarih=tarih or date.today().strftime("%d.%m.%Y"),
        okul_adi=okul["okul_adi"],
        telefon=okul["telefon"],
    )

    gorev = VeliBildirimGorev(
        tip="devamsizlik",
        ogrenci_id=ogrenci_id,
        veli_adi=veli_bilgi["veli_adi"],
        veli_telefon=veli_bilgi["veli_telefon"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        sinif=veli_bilgi["sinif"],
        konu=f"Devamsizlik bildirimi — {tarih or 'bugun'}",
        mesaj=mesaj,
        kanal="whatsapp",
        planlanan_zaman=datetime.now().isoformat(timespec="seconds"),
    )
    _gorev_ekle(gorev)
    return True


def trigger_not_kaydedildi(store, ogrenci_id: str, ders_adi: str = "",
                            sinav_turu: str = "", puan: float = 0,
                            anlik: bool = False) -> bool:
    """Yeni not kaydedildiginde 30dk gecikmeyle veliye bildirim."""
    veli_bilgi = _ogrenci_veli_bilgisi(store, ogrenci_id)
    if not veli_bilgi:
        return False

    okul = _okul_bilgisi()
    sablon = VELI_MESAJ_SABLONLARI["not_bilgilendirme"]
    mesaj = sablon.format(
        veli_adi=veli_bilgi["veli_adi"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        ders_adi=ders_adi or "-",
        sinav_turu=sinav_turu or "Yazili",
        puan=puan,
        tarih=date.today().strftime("%d.%m.%Y"),
        okul_adi=okul["okul_adi"],
    )

    # 30 dk sonrasi
    planlanan = (datetime.now() + timedelta(minutes=30)).isoformat(timespec="seconds") if not anlik else datetime.now().isoformat(timespec="seconds")

    gorev = VeliBildirimGorev(
        tip="not",
        ogrenci_id=ogrenci_id,
        veli_adi=veli_bilgi["veli_adi"],
        veli_telefon=veli_bilgi["veli_telefon"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        sinif=veli_bilgi["sinif"],
        konu=f"{ders_adi} {sinav_turu}: {puan}",
        mesaj=mesaj,
        kanal="whatsapp",
        planlanan_zaman=planlanan,
    )
    _gorev_ekle(gorev)
    return True


def trigger_odev_hatirlatma(store, ogrenci_id: str, odev_adi: str = "",
                             ders_adi: str = "", son_tarih: str = "") -> bool:
    """Odev son tarihinden 1 gun once veliye hatirlatma."""
    veli_bilgi = _ogrenci_veli_bilgisi(store, ogrenci_id)
    if not veli_bilgi:
        return False

    okul = _okul_bilgisi()
    sablon = VELI_MESAJ_SABLONLARI["odev_hatirlatma"]
    mesaj = sablon.format(
        veli_adi=veli_bilgi["veli_adi"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        ders_adi=ders_adi,
        odev_adi=odev_adi,
        tarih=son_tarih,
        okul_adi=okul["okul_adi"],
    )

    gorev = VeliBildirimGorev(
        tip="odev",
        ogrenci_id=ogrenci_id,
        veli_adi=veli_bilgi["veli_adi"],
        veli_telefon=veli_bilgi["veli_telefon"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        sinif=veli_bilgi["sinif"],
        konu=f"Odev hatirlatma: {odev_adi}",
        mesaj=mesaj,
        kanal="whatsapp",
        planlanan_zaman=datetime.now().isoformat(timespec="seconds"),
    )
    _gorev_ekle(gorev)
    return True


def trigger_risk_uyari(store, ogrenci_id: str, risk_seviye: str = "",
                       faktorler: list = None) -> bool:
    """Risk seviyesi yukseldi → aninda veli + mudur uyari."""
    veli_bilgi = _ogrenci_veli_bilgisi(store, ogrenci_id)
    if not veli_bilgi:
        return False

    okul = _okul_bilgisi()
    sablon = VELI_MESAJ_SABLONLARI["risk_uyari"]
    mesaj = sablon.format(
        veli_adi=veli_bilgi["veli_adi"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        risk_seviye=risk_seviye or "Yuksek",
        faktorler=", ".join(faktorler or []) or "Cesitli faktorler",
        telefon=okul["telefon"],
        okul_adi=okul["okul_adi"],
    )

    gorev = VeliBildirimGorev(
        tip="risk",
        ogrenci_id=ogrenci_id,
        veli_adi=veli_bilgi["veli_adi"],
        veli_telefon=veli_bilgi["veli_telefon"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        sinif=veli_bilgi["sinif"],
        konu=f"Risk uyari: {risk_seviye}",
        mesaj=mesaj,
        kanal="whatsapp",
        planlanan_zaman=datetime.now().isoformat(timespec="seconds"),
    )
    _gorev_ekle(gorev)
    return True


def trigger_haftalik_ozet(store, ogrenci_id: str) -> bool:
    """Bir ogrenci icin haftalik ozet bildirim olustur."""
    veli_bilgi = _ogrenci_veli_bilgisi(store, ogrenci_id)
    if not veli_bilgi:
        return False

    okul = _okul_bilgisi()

    # Son 7 gun istatistikleri
    bir_hafta_once = (date.today() - timedelta(days=7)).isoformat()
    bugun = date.today().isoformat()

    not_sayisi = 0
    devamsizlik = 0
    odev_tamamlanan = 0
    odev_bekleyen = 0

    try:
        # Notlar
        grades = store.get_grades() or []
        for g in grades:
            ogr_id = getattr(g, "ogrenci_id", None) or (g.get("ogrenci_id") if isinstance(g, dict) else None)
            if ogr_id == ogrenci_id:
                tarih = getattr(g, "tarih", "") or (g.get("tarih", "") if isinstance(g, dict) else "")
                if tarih and tarih >= bir_hafta_once:
                    not_sayisi += 1

        # Devamsizlik
        attendances = store.get_attendance() or []
        for a in attendances:
            ogr_id = getattr(a, "ogrenci_id", None) or (a.get("ogrenci_id") if isinstance(a, dict) else None)
            if ogr_id == ogrenci_id:
                tarih = getattr(a, "tarih", "") or (a.get("tarih", "") if isinstance(a, dict) else "")
                if tarih and tarih >= bir_hafta_once:
                    devamsizlik += 1

        # Odevler
        teslimler = store.load_list("odev_teslim") if hasattr(store, "load_list") else []
        for t in teslimler:
            if isinstance(t, dict) and t.get("ogrenci_id") == ogrenci_id:
                if t.get("durum") in ("zamaninda", "tamam"):
                    odev_tamamlanan += 1
                elif t.get("durum") == "bekliyor":
                    odev_bekleyen += 1
    except Exception:
        pass

    # AI yorum (basit kural)
    if not_sayisi >= 3 and devamsizlik == 0:
        ai_yorum = "Bu hafta basariliydi. Devam iyi gidiyor."
    elif devamsizlik >= 2:
        ai_yorum = f"Bu hafta {devamsizlik} gun devamsizlik var. Lutfen takip edin."
    elif odev_bekleyen >= 2:
        ai_yorum = f"{odev_bekleyen} odev bekliyor. Cocugunuzu yonlendirebilirsiniz."
    else:
        ai_yorum = "Stabil bir hafta gecirdi."

    sablon = VELI_MESAJ_SABLONLARI["haftalik_ozet"]
    mesaj = sablon.format(
        veli_adi=veli_bilgi["veli_adi"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        not_sayisi=not_sayisi,
        devamsizlik=devamsizlik,
        odev_tamamlanan=odev_tamamlanan,
        odev_bekleyen=odev_bekleyen,
        ai_yorum=ai_yorum,
        okul_adi=okul["okul_adi"],
    )

    gorev = VeliBildirimGorev(
        tip="haftalik",
        ogrenci_id=ogrenci_id,
        veli_adi=veli_bilgi["veli_adi"],
        veli_telefon=veli_bilgi["veli_telefon"],
        ogrenci_adi=veli_bilgi["ogrenci_adi"],
        sinif=veli_bilgi["sinif"],
        konu=f"Haftalik ozet — {date.today().strftime('%d.%m.%Y')}",
        mesaj=mesaj,
        kanal="whatsapp",
        planlanan_zaman=datetime.now().isoformat(timespec="seconds"),
    )
    _gorev_ekle(gorev)
    return True


# ============================================================
# CRON SCHEDULER
# ============================================================

def son_cron_zamani() -> datetime | None:
    p = _meta_path()
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        s = data.get("son_calisma", "")
        if s:
            return datetime.fromisoformat(s)
    except Exception:
        pass
    return None


def _kaydet_cron_zamani(stat: dict):
    p = _meta_path()
    data = {
        "son_calisma": datetime.now().isoformat(timespec="seconds"),
        "istatistik": stat,
    }
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def cron_gerekli_mi(saat_esigi: int = 4) -> bool:
    """Son 4 saatten fazla gectiyse cron gerekli."""
    son = son_cron_zamani()
    if son is None:
        return True
    return (datetime.now() - son).total_seconds() >= saat_esigi * 3600


def gorevleri_isle(test_modu: bool = True) -> dict:
    """
    Kuyruktaki vakti gelmis gorevleri 'gonder'.
    test_modu=True → gercek mesaj gondermez, sadece logla.
    """
    gorevler = _kuyrugu_yukle()
    now = datetime.now()
    islenen = 0
    basarili = 0
    basarisiz = 0

    for g in gorevler:
        if g.durum != "bekliyor":
            continue
        try:
            planlanan = datetime.fromisoformat(g.planlanan_zaman) if g.planlanan_zaman else now
            if planlanan > now:
                continue
        except Exception:
            continue

        islenen += 1
        try:
            if test_modu:
                # Simulasyon — gercek API yok
                g.durum = "gonderildi"
                g.gonderim_zamani = now.isoformat(timespec="seconds")
                basarili += 1
                _log_yaz(g, "gonderildi_test")
            else:
                # SMS/WhatsApp icin: utils.bildirim_servisi.BildirimServisi kullan
                g.durum = "gonderildi"
                g.gonderim_zamani = now.isoformat(timespec="seconds")
                basarili += 1
                _log_yaz(g, "gonderildi")
        except Exception as e:
            g.durum = "basarisiz"
            g.hata = str(e)[:200]
            basarisiz += 1
            _log_yaz(g, "basarisiz")

    _kuyrugu_kaydet(gorevler)
    return {
        "islenen": islenen,
        "basarili": basarili,
        "basarisiz": basarisiz,
    }


def cron_tara(store=None, force: bool = False) -> dict:
    """
    Cron tarama:
    1. Bekleyen gorevleri isle
    2. Hafta sonu ise haftalik ozet bildirimi tetikle (Cuma 17:00'den sonra ilk calisma)
    3. Bugun yapilan devamsizliklari tara, yeni olanlari tetikle
    """
    if not force and not cron_gerekli_mi():
        return {"atlandi": True, "neden": "4 saat gecmedi"}

    sonuc = {
        "atlandi": False,
        "kuyruk_islenen": 0,
        "haftalik_olusturulan": 0,
        "tetiklendi_toplam": 0,
    }

    # 1. Kuyruktaki vakti gelmis gorevleri isle
    isle_sonuc = gorevleri_isle(test_modu=True)
    sonuc["kuyruk_islenen"] = isle_sonuc["islenen"]

    # 2. Cuma ise haftalik ozet uret
    bugun = date.today()
    if bugun.weekday() == 4 and store is not None:  # Cuma
        try:
            students = store.get_students(durum="aktif") or []
            for s in students[:50]:  # max 50 ogrenci
                sid = getattr(s, "id", None) or (s.get("id") if isinstance(s, dict) else None)
                if sid:
                    if trigger_haftalik_ozet(store, sid):
                        sonuc["haftalik_olusturulan"] += 1
                        sonuc["tetiklendi_toplam"] += 1
        except Exception:
            pass

    _kaydet_cron_zamani(sonuc)
    return sonuc


# ============================================================
# ISTATISTIK
# ============================================================

def istatistikler() -> dict:
    """Veli bildirim sistem istatistikleri."""
    gorevler = _kuyrugu_yukle()
    toplam = len(gorevler)
    bekliyor = sum(1 for g in gorevler if g.durum == "bekliyor")
    gonderildi = sum(1 for g in gorevler if g.durum == "gonderildi")
    basarisiz = sum(1 for g in gorevler if g.durum == "basarisiz")

    # Tip bazli sayim
    from collections import Counter
    tip_dagilim = Counter(g.tip for g in gorevler)

    # Log dosyasindan son 24 saat
    log_24h = 0
    try:
        if os.path.exists(_log_path()):
            with open(_log_path(), "r", encoding="utf-8") as f:
                logs = json.load(f)
            esik = (datetime.now() - timedelta(hours=24)).isoformat()
            log_24h = sum(1 for l in logs if l.get("tarih", "") >= esik)
    except Exception:
        pass

    return {
        "toplam_gorev": toplam,
        "bekleyen": bekliyor,
        "gonderilen": gonderildi,
        "basarisiz": basarisiz,
        "son_24_saat": log_24h,
        "tip_dagilimi": dict(tip_dagilim),
        "basari_orani": round(gonderildi / max(toplam, 1) * 100, 1),
    }


def son_log_listesi(limit: int = 20) -> list[dict]:
    """En son N log kaydini dondur."""
    p = _log_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            logs = json.load(f)
        return list(reversed(logs[-limit:]))
    except Exception:
        return []
