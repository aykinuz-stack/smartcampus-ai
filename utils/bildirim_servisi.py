"""
Bildirim Servisi (SMS & Email)
==============================
SmartCampus AI icin merkezi bildirim gonderim altyapisi.
SMS ve Email icin provider soyutlama katmani ile calisir.
Tum gonderimler data/bildirim/gonderim_log.json dosyasina kaydedilir.

Desteklenen Providerlar:
  - SMS:   NetGSMProvider, TwilioProvider (stub)
  - Email: SMTPProvider (stub)

Konfigürasyon: Ortam degiskenleri (environment variables) ile yapilir.
"""

import json
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

# ===================== KONFIGÜRASYON =====================

SMS_PROVIDER = os.environ.get("SMS_PROVIDER", "netgsm")  # netgsm | twilio
SMS_API_KEY = os.environ.get("SMS_API_KEY", "")
SMS_API_SECRET = os.environ.get("SMS_API_SECRET", "")
SMS_SENDER_ID = os.environ.get("SMS_SENDER_ID", "SMARTCAMPUS")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "SmartCampus AI")
SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", "")

LOG_FILE = os.path.join("data", "bildirim", "gonderim_log.json")

# ===================== SMS SABLONLARI =====================

SMS_SABLONLAR: dict[str, str] = {
    "devamsizlik": (
        "Sayin Veli, ogrencisiniz {ogrenci_adi} {tarih} tarihinde "
        "{ders} dersine katilmamistir. Bilginize."
    ),
    "not_bildirimi": (
        "Sayin Veli, ogrencisiniz {ogrenci_adi} {ders} dersinden "
        "{puan} puan almistir."
    ),
    "odeme_hatirlatma": (
        "Sayin Veli, {ogrenci_adi} icin {taksit_no}. taksit ({tutar} TL) "
        "odeme vade tarihi: {vade}. Lutfen zamaninda odeme yapiniz."
    ),
    "duyuru": (
        "[SmartCampus] {baslik}: {mesaj}"
    ),
    "sinav_hatirlatma": (
        "Sayin Veli, ogrencisiniz {ogrenci_adi} icin {tarih} tarihinde "
        "{ders} sinavi yapilacaktir. Bilginize."
    ),
    "toplanti_davet": (
        "Sayin {alici_adi}, {tarih} tarihinde {saat}'da {konu} konulu "
        "toplantiya katiliminiz beklenmektedir."
    ),
    "sifre_sifirlama": (
        "[SmartCampus] Yeni sifreniz: {yeni_sifre} — Ilk giriste "
        "degistirmeniz gerekmektedir."
    ),
    "hosgeldiniz": (
        "SmartCampus AI'ya hosgeldiniz! Kullanici adiniz: {username}. "
        "Ilk giris sifreniz SMS olarak gonderildi."
    ),
}

# ===================== EMAIL SABLONLARI =====================

EMAIL_SABLONLAR: dict[str, str] = {
    "devamsizlik": (
        "<h2>Devamsizlik Bildirimi</h2>"
        "<p>Sayin Veli,</p>"
        "<p>Ogrencisiniz <strong>{ogrenci_adi}</strong>, "
        "<strong>{tarih}</strong> tarihinde <strong>{ders}</strong> "
        "dersine katilmamistir.</p>"
        "<p>Bilginize sunariz.</p>"
        "<hr><small>SmartCampus AI - Akademik Yonetim Platformu</small>"
    ),
    "not_bildirimi": (
        "<h2>Not Bildirimi</h2>"
        "<p>Sayin Veli,</p>"
        "<p>Ogrencisiniz <strong>{ogrenci_adi}</strong>, "
        "<strong>{ders}</strong> dersinden <strong>{puan}</strong> "
        "puan almistir.</p>"
        "<hr><small>SmartCampus AI - Akademik Yonetim Platformu</small>"
    ),
    "odeme_hatirlatma": (
        "<h2>Odeme Hatirlatma</h2>"
        "<p>Sayin Veli,</p>"
        "<p><strong>{ogrenci_adi}</strong> icin <strong>{taksit_no}. taksit</strong> "
        "({tutar} TL) odeme vade tarihi: <strong>{vade}</strong>.</p>"
        "<p>Lutfen zamaninda odeme yapiniz.</p>"
        "<hr><small>SmartCampus AI - Akademik Yonetim Platformu</small>"
    ),
    "duyuru": (
        "<h2>{baslik}</h2>"
        "<p>{mesaj}</p>"
        "<hr><small>SmartCampus AI - Akademik Yonetim Platformu</small>"
    ),
    "haftalik_rapor": (
        "<h2>Haftalik Ogrenci Raporu</h2>"
        "<p>Sayin Veli,</p>"
        "<p>Ogrencisiniz <strong>{ogrenci_adi}</strong> icin "
        "haftalik performans raporu:</p>"
        "<ul>"
        "<li>Devamsizlik: {devamsizlik_gun} gun</li>"
        "<li>Not Ortalamasi: {ortalama}</li>"
        "<li>Odev Tamamlama: %{odev_oran}</li>"
        "</ul>"
        "<hr><small>SmartCampus AI - Akademik Yonetim Platformu</small>"
    ),
}


# ===================== LOG YONETIMI =====================

def _ensure_log_dir() -> None:
    """Log dizinini olustur."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _log_gonderim(kayit: dict[str, Any]) -> None:
    """Gonderim kaydini log dosyasina ekle."""
    _ensure_log_dir()
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logs = []
    logs.append(kayit)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def get_gonderim_log(limit: int = 100) -> list[dict]:
    """Son N gonderim kaydini dondur."""
    _ensure_log_dir()
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    return logs[-limit:]


# ===================== PROVIDER SOYUTLAMA =====================

class SMSProvider(ABC):
    """SMS provider soyut sinifi. Tum SMS providerlari bunu miras alir."""

    @abstractmethod
    def send(self, telefon: str, mesaj: str) -> dict[str, Any]:
        """
        Tek SMS gonder.
        Returns: {"success": bool, "message_id": str, "error": str|None}
        """
        ...

    @abstractmethod
    def send_bulk(self, alicilar: list[str], mesaj: str) -> list[dict[str, Any]]:
        """
        Toplu SMS gonder.
        Returns: list of {"telefon": str, "success": bool, ...}
        """
        ...


class NetGSMProvider(SMSProvider):
    """
    NetGSM SMS provider stub.
    Gercek entegrasyon icin https://www.netgsm.com.tr/dokuman/ adresine bakiniz.
    API_KEY ve API_SECRET ortam degiskenlerinden alinir.
    """

    def __init__(self):
        self.api_key = SMS_API_KEY
        self.api_secret = SMS_API_SECRET
        self.sender_id = SMS_SENDER_ID

    def send(self, telefon: str, mesaj: str) -> dict[str, Any]:
        """
        NetGSM API uzerinden SMS gonder.
        STUB: Gercek HTTP istegi yapilmiyor, basarili sonuc simule ediliyor.
        Uretim ortaminda requests ile NetGSM XML/REST API'sine istek atilmalidir.
        """
        if not self.api_key:
            return {
                "success": False,
                "message_id": None,
                "error": "SMS_API_KEY ortam degiskeni ayarlanmamis.",
                "provider": "netgsm",
            }

        # --- STUB: Gercek API cagrisi burada yapilir ---
        # import requests
        # response = requests.post("https://api.netgsm.com.tr/sms/send/get/", ...)
        # --- STUB SONU ---

        message_id = f"netgsm_{uuid.uuid4().hex[:12]}"
        return {
            "success": True,
            "message_id": message_id,
            "error": None,
            "provider": "netgsm",
            "telefon": telefon,
            "stub": True,
        }

    def send_bulk(self, alicilar: list[str], mesaj: str) -> list[dict[str, Any]]:
        """Toplu SMS gonder (her alici icin ayri istek)."""
        results = []
        for tel in alicilar:
            results.append(self.send(tel, mesaj))
        return results


class TwilioProvider(SMSProvider):
    """
    Twilio SMS provider stub.
    Gercek entegrasyon icin https://www.twilio.com/docs/sms adresine bakiniz.
    """

    def __init__(self):
        self.account_sid = SMS_API_KEY
        self.auth_token = SMS_API_SECRET
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", "")

    def send(self, telefon: str, mesaj: str) -> dict[str, Any]:
        if not self.account_sid:
            return {
                "success": False,
                "message_id": None,
                "error": "SMS_API_KEY (Twilio Account SID) ortam degiskeni ayarlanmamis.",
                "provider": "twilio",
            }

        # --- STUB: Gercek Twilio API cagrisi burada yapilir ---
        # from twilio.rest import Client
        # client = Client(self.account_sid, self.auth_token)
        # message = client.messages.create(to=telefon, from_=self.from_number, body=mesaj)
        # --- STUB SONU ---

        message_id = f"twilio_{uuid.uuid4().hex[:12]}"
        return {
            "success": True,
            "message_id": message_id,
            "error": None,
            "provider": "twilio",
            "telefon": telefon,
            "stub": True,
        }

    def send_bulk(self, alicilar: list[str], mesaj: str) -> list[dict[str, Any]]:
        results = []
        for tel in alicilar:
            results.append(self.send(tel, mesaj))
        return results


class EmailProvider(ABC):
    """Email provider soyut sinifi."""

    @abstractmethod
    def send(self, to_email: str, konu: str, icerik: str) -> dict[str, Any]:
        """
        Tek email gonder.
        Returns: {"success": bool, "message_id": str, "error": str|None}
        """
        ...

    @abstractmethod
    def send_bulk(self, alicilar: list[str], konu: str, icerik: str) -> list[dict[str, Any]]:
        """Toplu email gonder."""
        ...


class SMTPProvider(EmailProvider):
    """
    SMTP tabanli email provider stub.
    Gercek gonderim icin smtplib kullanilir.
    """

    def __init__(self):
        self.host = SMTP_HOST
        self.port = SMTP_PORT
        self.user = SMTP_USER
        self.password = SMTP_PASSWORD
        self.from_name = SMTP_FROM_NAME
        self.from_email = SMTP_FROM_EMAIL

    def send(self, to_email: str, konu: str, icerik: str) -> dict[str, Any]:
        if not self.user or not self.password:
            return {
                "success": False,
                "message_id": None,
                "error": "SMTP_USER veya SMTP_PASSWORD ortam degiskeni ayarlanmamis.",
                "provider": "smtp",
            }

        # --- STUB: Gercek SMTP gonderimi burada yapilir ---
        # import smtplib
        # from email.mime.multipart import MIMEMultipart
        # from email.mime.text import MIMEText
        #
        # msg = MIMEMultipart("alternative")
        # msg["Subject"] = konu
        # msg["From"] = f"{self.from_name} <{self.from_email}>"
        # msg["To"] = to_email
        # msg.attach(MIMEText(icerik, "html", "utf-8"))
        #
        # with smtplib.SMTP(self.host, self.port) as server:
        #     server.starttls()
        #     server.login(self.user, self.password)
        #     server.sendmail(self.from_email, to_email, msg.as_string())
        # --- STUB SONU ---

        message_id = f"smtp_{uuid.uuid4().hex[:12]}"
        return {
            "success": True,
            "message_id": message_id,
            "error": None,
            "provider": "smtp",
            "to_email": to_email,
            "stub": True,
        }

    def send_bulk(self, alicilar: list[str], konu: str, icerik: str) -> list[dict[str, Any]]:
        results = []
        for email_addr in alicilar:
            results.append(self.send(email_addr, konu, icerik))
        return results


# ===================== PROVIDER FABRIKASI =====================

def _get_sms_provider() -> SMSProvider:
    """Konfigurasyona gore uygun SMS provider dondur."""
    if SMS_PROVIDER == "twilio":
        return TwilioProvider()
    return NetGSMProvider()  # varsayilan


def _get_email_provider() -> EmailProvider:
    """Email provider dondur (su an sadece SMTP)."""
    return SMTPProvider()


# ===================== YARDIMCI: OGRENCI/VELI BILGISI =====================

def _get_student_info(student_id: str) -> dict[str, Any] | None:
    """Ogrenci bilgilerini AkademikDataStore'dan cek."""
    try:
        from models.akademik_takip import AkademikDataStore
        store = AkademikDataStore()
        students = store.get_students()
        for s in students:
            if s.id == student_id:
                return {
                    "id": s.id,
                    "ad": f"{s.ad} {s.soyad}",
                    "sinif": s.sinif,
                    "sube": s.sube,
                    "veli_adi": getattr(s, "veli_adi", ""),
                    "veli_telefon": getattr(s, "veli_telefon", ""),
                    "veli_email": getattr(s, "veli_email", ""),
                }
    except Exception:
        pass
    return None


# ===================== ANA SERVIS =====================

class BildirimServisi:
    """
    Merkezi bildirim servisi.
    SMS ve Email gonderimini tek bir arayuz uzerinden yonetir.
    Tum gonderimler otomatik olarak loglanir.
    """

    def __init__(self):
        self.sms_provider: SMSProvider = _get_sms_provider()
        self.email_provider: EmailProvider = _get_email_provider()

    # ─────────────── TEK SMS ───────────────

    def sms_gonder(self, telefon: str, mesaj: str, sablon: str | None = None) -> dict[str, Any]:
        """
        Tek SMS gonder.

        Args:
            telefon: Alici telefon numarasi (ornek: 05551234567)
            mesaj: Gonderilecek mesaj metni
            sablon: Kullanilan sablon adi (log icin)

        Returns:
            {"success": bool, "message_id": str|None, "error": str|None, ...}
        """
        result = self.sms_provider.send(telefon, mesaj)

        _log_gonderim({
            "id": uuid.uuid4().hex,
            "tip": "sms",
            "tarih": datetime.now().isoformat(),
            "alici": telefon,
            "sablon": sablon,
            "mesaj": mesaj[:200],  # log icin kisalt
            "basarili": result.get("success", False),
            "message_id": result.get("message_id"),
            "hata": result.get("error"),
            "provider": result.get("provider"),
        })

        return result

    # ─────────────── TEK EMAIL ───────────────

    def email_gonder(
        self, email: str, konu: str, icerik: str, sablon: str | None = None
    ) -> dict[str, Any]:
        """
        Tek email gonder.

        Args:
            email: Alici email adresi
            konu: Email konusu
            icerik: Email icerigi (HTML destekli)
            sablon: Kullanilan sablon adi (log icin)

        Returns:
            {"success": bool, "message_id": str|None, "error": str|None, ...}
        """
        result = self.email_provider.send(email, konu, icerik)

        _log_gonderim({
            "id": uuid.uuid4().hex,
            "tip": "email",
            "tarih": datetime.now().isoformat(),
            "alici": email,
            "konu": konu,
            "sablon": sablon,
            "basarili": result.get("success", False),
            "message_id": result.get("message_id"),
            "hata": result.get("error"),
            "provider": result.get("provider"),
        })

        return result

    # ─────────────── TOPLU SMS ───────────────

    def toplu_sms(
        self, alicilar: list[dict[str, str]], mesaj_sablonu: str
    ) -> list[dict[str, Any]]:
        """
        Toplu SMS gonder.

        Args:
            alicilar: [{"telefon": "0555...", "ad": "Ahmet", ...}, ...]
            mesaj_sablonu: SMS_SABLONLAR key'i veya direkt sablon string

        Returns:
            list of gonderim sonuclari
        """
        sablon = SMS_SABLONLAR.get(mesaj_sablonu, mesaj_sablonu)
        results = []
        for alici in alicilar:
            telefon = alici.get("telefon", "")
            if not telefon:
                results.append({"success": False, "error": "Telefon numarasi eksik", "alici": alici})
                continue
            try:
                mesaj = sablon.format(**alici)
            except KeyError:
                mesaj = sablon
            result = self.sms_gonder(telefon, mesaj, sablon=mesaj_sablonu)
            results.append(result)
        return results

    # ─────────────── TOPLU EMAIL ───────────────

    def toplu_email(
        self, alicilar: list[dict[str, str]], konu: str, sablon: str
    ) -> list[dict[str, Any]]:
        """
        Toplu email gonder.

        Args:
            alicilar: [{"email": "x@y.com", "ad": "Ahmet", ...}, ...]
            konu: Email konu satiri
            sablon: EMAIL_SABLONLAR key'i veya direkt HTML sablon

        Returns:
            list of gonderim sonuclari
        """
        icerik_sablonu = EMAIL_SABLONLAR.get(sablon, sablon)
        results = []
        for alici in alicilar:
            email_addr = alici.get("email", "")
            if not email_addr:
                results.append({"success": False, "error": "Email adresi eksik", "alici": alici})
                continue
            try:
                icerik = icerik_sablonu.format(**alici)
            except KeyError:
                icerik = icerik_sablonu
            result = self.email_gonder(email_addr, konu, icerik, sablon=sablon)
            results.append(result)
        return results

    # ─────────────── DEVAMSIZLIK BILDIRIMI ───────────────

    def devamsizlik_bildirimi(
        self, student_id: str, tarih: str, ders: str
    ) -> dict[str, Any]:
        """
        Devamsizlik yapan ogrencinin velisine otomatik SMS gonder.

        Args:
            student_id: Ogrenci ID'si
            tarih: Devamsizlik tarihi (ornek: 2026-04-21)
            ders: Ders adi

        Returns:
            {"success": bool, "sms": dict|None, "email": dict|None, "error": str|None}
        """
        ogrenci = _get_student_info(student_id)
        if not ogrenci:
            return {"success": False, "sms": None, "email": None, "error": "Ogrenci bulunamadi"}

        veri = {
            "ogrenci_adi": ogrenci["ad"],
            "tarih": tarih,
            "ders": ders,
        }

        sms_result = None
        email_result = None

        # SMS gonder
        veli_tel = ogrenci.get("veli_telefon", "")
        if veli_tel:
            mesaj = SMS_SABLONLAR["devamsizlik"].format(**veri)
            sms_result = self.sms_gonder(veli_tel, mesaj, sablon="devamsizlik")

        # Email gonder
        veli_email = ogrenci.get("veli_email", "")
        if veli_email:
            icerik = EMAIL_SABLONLAR["devamsizlik"].format(**veri)
            email_result = self.email_gonder(
                veli_email, f"Devamsizlik Bildirimi - {ogrenci['ad']}", icerik, sablon="devamsizlik"
            )

        success = bool(
            (sms_result and sms_result.get("success"))
            or (email_result and email_result.get("success"))
        )

        return {
            "success": success,
            "sms": sms_result,
            "email": email_result,
            "error": None if success else "Veli iletisim bilgisi eksik veya gonderim basarisiz",
        }

    # ─────────────── NOT BILDIRIMI ───────────────

    def not_bildirimi(
        self, student_id: str, ders: str, puan: float
    ) -> dict[str, Any]:
        """
        Not girildiginde veliye otomatik SMS gonder.

        Args:
            student_id: Ogrenci ID'si
            ders: Ders adi
            puan: Alinan puan

        Returns:
            {"success": bool, "sms": dict|None, "email": dict|None, "error": str|None}
        """
        ogrenci = _get_student_info(student_id)
        if not ogrenci:
            return {"success": False, "sms": None, "email": None, "error": "Ogrenci bulunamadi"}

        veri = {
            "ogrenci_adi": ogrenci["ad"],
            "ders": ders,
            "puan": str(puan),
        }

        sms_result = None
        email_result = None

        veli_tel = ogrenci.get("veli_telefon", "")
        if veli_tel:
            mesaj = SMS_SABLONLAR["not_bildirimi"].format(**veri)
            sms_result = self.sms_gonder(veli_tel, mesaj, sablon="not_bildirimi")

        veli_email = ogrenci.get("veli_email", "")
        if veli_email:
            icerik = EMAIL_SABLONLAR["not_bildirimi"].format(**veri)
            email_result = self.email_gonder(
                veli_email, f"Not Bildirimi - {ogrenci['ad']} - {ders}", icerik, sablon="not_bildirimi"
            )

        success = bool(
            (sms_result and sms_result.get("success"))
            or (email_result and email_result.get("success"))
        )

        return {
            "success": success,
            "sms": sms_result,
            "email": email_result,
            "error": None if success else "Veli iletisim bilgisi eksik veya gonderim basarisiz",
        }

    # ─────────────── ODEME HATIRLATMA ───────────────

    def odeme_hatirlatma(
        self, student_id: str, taksit_no: int, tutar: float, vade: str
    ) -> dict[str, Any]:
        """
        Odeme hatirlatma SMS'i gonder.

        Args:
            student_id: Ogrenci ID'si
            taksit_no: Taksit numarasi
            tutar: Taksit tutari (TL)
            vade: Vade tarihi (ornek: 2026-05-01)

        Returns:
            {"success": bool, "sms": dict|None, "email": dict|None, "error": str|None}
        """
        ogrenci = _get_student_info(student_id)
        if not ogrenci:
            return {"success": False, "sms": None, "email": None, "error": "Ogrenci bulunamadi"}

        veri = {
            "ogrenci_adi": ogrenci["ad"],
            "taksit_no": str(taksit_no),
            "tutar": f"{tutar:,.2f}",
            "vade": vade,
        }

        sms_result = None
        email_result = None

        veli_tel = ogrenci.get("veli_telefon", "")
        if veli_tel:
            mesaj = SMS_SABLONLAR["odeme_hatirlatma"].format(**veri)
            sms_result = self.sms_gonder(veli_tel, mesaj, sablon="odeme_hatirlatma")

        veli_email = ogrenci.get("veli_email", "")
        if veli_email:
            icerik = EMAIL_SABLONLAR["odeme_hatirlatma"].format(**veri)
            email_result = self.email_gonder(
                veli_email, f"Odeme Hatirlatma - {ogrenci['ad']}", icerik, sablon="odeme_hatirlatma"
            )

        success = bool(
            (sms_result and sms_result.get("success"))
            or (email_result and email_result.get("success"))
        )

        return {
            "success": success,
            "sms": sms_result,
            "email": email_result,
            "error": None if success else "Veli iletisim bilgisi eksik veya gonderim basarisiz",
        }

    # ─────────────── DUYURU YAYINLA ───────────────

    def duyuru_yayinla(
        self, baslik: str, mesaj: str, hedef_rol: str = "hepsi"
    ) -> dict[str, Any]:
        """
        Tum kullanicilara veya belirli bir role duyuru yayinla.

        Args:
            baslik: Duyuru basligi
            mesaj: Duyuru icerigi
            hedef_rol: "hepsi" | "Veli" | "Ogretmen" | "Ogrenci" | ...

        Returns:
            {"success": bool, "sms_count": int, "email_count": int,
             "sms_basarili": int, "email_basarili": int}
        """
        # Kullanicilari yukle
        try:
            from utils.auth import _load_users
            users = _load_users()
        except Exception:
            users = []

        # Hedef filtreleme
        if hedef_rol and hedef_rol != "hepsi":
            users = [u for u in users if u.get("role") == hedef_rol]

        sms_count = 0
        sms_basarili = 0
        email_count = 0
        email_basarili = 0

        sms_mesaj = SMS_SABLONLAR["duyuru"].format(baslik=baslik, mesaj=mesaj[:120])
        email_icerik = EMAIL_SABLONLAR["duyuru"].format(baslik=baslik, mesaj=mesaj)

        for user in users:
            # SMS (telefon bilgisi varsa)
            telefon = user.get("telefon", "")
            if telefon:
                sms_count += 1
                r = self.sms_gonder(telefon, sms_mesaj, sablon="duyuru")
                if r.get("success"):
                    sms_basarili += 1

            # Email
            email_addr = user.get("email", "")
            if email_addr:
                email_count += 1
                r = self.email_gonder(email_addr, f"[SmartCampus] {baslik}", email_icerik, sablon="duyuru")
                if r.get("success"):
                    email_basarili += 1

        return {
            "success": True,
            "sms_count": sms_count,
            "sms_basarili": sms_basarili,
            "email_count": email_count,
            "email_basarili": email_basarili,
        }


# ===================== KOLAY ERISIM (Singleton) =====================

_servis_instance: BildirimServisi | None = None


def get_bildirim_servisi() -> BildirimServisi:
    """Singleton BildirimServisi instance'i dondur."""
    global _servis_instance
    if _servis_instance is None:
        _servis_instance = BildirimServisi()
    return _servis_instance
