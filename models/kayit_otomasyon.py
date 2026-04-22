"""
Kayit Modulu — Otomasyon Motoru
================================
Trigger -> Action workflow sistemi. Adayin durumuna gore otomatik
mesajlar/aksiyonlar gonderir.

8 hazir otomasyon:
1. Yeni aday geldi -> hosgeldin WhatsApp + 2 saat sonra randevu onerisi
2. Gorusme bitti -> tesekkur mesaji + brosur PDF
3. Fiyat 3 gun gecti -> hatirlatma + indirim teklifi
4. Ilk arama cevapsiz -> WhatsApp + aksamı SMS
5. Aday sogudu (isi dustu) -> mudur uyarisi
6. Sozlesme imzalandi -> hosgeldin paketi
7. Olumsuz isaretlendi -> 30 gun sonra geri donus
8. Dogum gunu -> kisisel kutlama mesaji
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, date, timedelta
from dataclasses import dataclass, asdict, field
from typing import Any

from utils.tenant import get_data_path


# ============================================================
# OTOMASYON TANIMLARI
# ============================================================

OTOMASYONLAR = [
    {
        "id": "yeni_aday_karsilama",
        "ad": "Yeni Aday Karsilama",
        "trigger": "yeni_aday",
        "icon": "👋",
        "renk": "#10B981",
        "aciklama": "Yeni aday eklenir eklenmez 5 dk icinde otomatik karsilama mesaji",
        "adimlar": [
            {"gecikme_dk": 5, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, {okul_adi} olarak ilginize tesekkur ederiz! "
                       "{ogrenci_adi} icin tum sorularinizi yanitlamak istiyoruz."},
            {"gecikme_dk": 120, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, sizinle bir randevu yapabilir miyiz? "
                       "Cocugunuzun gelisimi icin detayli sohbet edelim."},
            {"gecikme_dk": 1440, "kanal": "sms",
             "sablon": "{veli_adi} bey/hanim, sizin icin uygun bir gun belirleyelim. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "gorusme_sonrasi",
        "ad": "Gorusme Sonrasi Tesekkur",
        "trigger": "gorusme_tamamlandi",
        "icon": "🤝",
        "renk": "#6366F1",
        "aciklama": "Gorusme bitince 1 saat sonra AI'in yazdigi tesekkur mesaji + brosur",
        "adimlar": [
            {"gecikme_dk": 60, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, bugun bizi ziyaret ettiginiz icin cok tesekkur ederiz. "
                       "{ogrenci_adi} icin {okul_adi}'yi tercih edebilmeniz icin elimizden geleni yapacagiz."},
            {"gecikme_dk": 90, "kanal": "email",
             "sablon": "Sayin {veli_adi}, gorusme notlarimiza istinaden okul brosurumuzu ekte iletiyoruz. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "fiyat_3gun_hatirlatma",
        "ad": "Fiyat 3 Gun Hatirlatma",
        "trigger": "fiyat_verildi_3gun",
        "icon": "⏰",
        "renk": "#F59E0B",
        "aciklama": "Fiyat verildikten 3 gun sonra cevap gelmediyse nazik hatirlatma + indirim teklifi",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, gecen gun {ogrenci_adi} icin verdigimiz teklifi degerlendirme firsatiniz oldu mu? "
                       "Sizinle yeniden gorusup destek olmak isteriz."},
            {"gecikme_dk": 60, "kanal": "sms",
             "sablon": "{veli_adi} bey/hanim, ozel indirim firsatimiz icin bize ulasin. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "ilk_arama_cevapsiz",
        "ad": "Ilk Arama Cevapsiz",
        "trigger": "arama_cevapsiz",
        "icon": "📞",
        "renk": "#0EA5E9",
        "aciklama": "Ilk arama cevap vermediyse 2 saat sonra WhatsApp + aksam SMS",
        "adimlar": [
            {"gecikme_dk": 120, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, sizi aramistik ama ulasamadik. Size uygun bir saat bildirir misiniz? {okul_adi}"},
            {"gecikme_dk": 480, "kanal": "sms",
             "sablon": "{veli_adi} bey/hanim, {okul_adi}'den arama denedik. Geri donus icin: {okul_telefon}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "aday_soguma",
        "ad": "Aday Soguyor Uyarisi",
        "trigger": "isi_dustu",
        "icon": "❄️",
        "renk": "#94A3B8",
        "aciklama": "Adayin isi seviyesi dusunce mudure uyari + sicaklastirma araması planla",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "internal_alert",
             "sablon": "{ogrenci_adi} icin isi seviyesi dustu — sicaklastirma araması yapilmasi gerekiyor"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "sozlesme_imza_hosgeldin",
        "ad": "Sozlesme Hosgeldin Paketi",
        "trigger": "sozlesme_imzalandi",
        "icon": "🎉",
        "renk": "#10B981",
        "aciklama": "Sozlesme imzalanir imzalanmaz 5 dk icinde hosgeldin paketi + ders programi",
        "adimlar": [
            {"gecikme_dk": 5, "kanal": "whatsapp",
             "sablon": "🎉 Tebrikler {veli_adi}! {ogrenci_adi}'nin {okul_adi} ailesine katilmasindan mutluluk duyuyoruz. "
                       "Hosgeldin paketinizi en kisa surede tarafiniza ileteceğiz."},
            {"gecikme_dk": 60, "kanal": "email",
             "sablon": "Sayin {veli_adi}, ders programi, kitap listesi ve okul kurallarini ekte gonderiyoruz. Hosgeldiniz!"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "olumsuz_geri_donus",
        "ad": "Olumsuz Adaya 30 Gun Sonra Geri Donus",
        "trigger": "olumsuz_isaretlendi_30gun",
        "icon": "🔄",
        "renk": "#A78BFA",
        "aciklama": "Olumsuz isaretlenen aday icin 30 gun sonra yeni kampanya ile otomatik geri donus",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, gecen ay sizinle gorusmustuk. {ogrenci_adi} icin yeni firsatlarimiz var. "
                       "Bilgi almak ister misiniz? {okul_adi}"},
        ],
        "varsayilan_aktif": False,
    },
    {
        "id": "dogum_gunu",
        "ad": "Ogrenci Dogum Gunu Kutlama",
        "trigger": "dogum_gunu",
        "icon": "🎂",
        "renk": "#EC4899",
        "aciklama": "Kayitli adayin dogum gununde otomatik kisisel kutlama mesaji",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "🎂 {ogrenci_adi}'nin dogum gunu kutlu olsun! {okul_adi} ailesi olarak nice mutlu yillara dileriz."},
        ],
        "varsayilan_aktif": True,
    },
    # ═══════════════════════════════════════════════════════════
    # YENI OTOMASYONLAR — Pipeline Döngüsü Tam Kapsamı
    # ═══════════════════════════════════════════════════════════
    {
        "id": "fiyat_verildi_anlik",
        "ad": "Fiyat Verildi Anlik Teklif",
        "trigger": "fiyat_verildi",
        "icon": "💰",
        "renk": "#22c55e",
        "aciklama": "Fiyat kaydedilir kaydedilmez veliye profesyonel teklif mesaji + 5 gun zinciri",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, {ogrenci_adi} icin size ozel hazirladigimiz teklif hazir. "
                       "Detaylari size en kisa surede iletecegiz. Sorulariniz oldugunda cekinmeyin. {okul_adi}"},
            {"gecikme_dk": 1440, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, teklifimiz hakkinda sormak istediginiz bir sey var mi? "
                       "Size yardimci olmaktan memnuniyet duyariz."},
            {"gecikme_dk": 7200, "kanal": "whatsapp",
             "sablon": "Sayin {veli_adi}, {ogrenci_adi} icin ayirdigimiz kontenjan hizla doluyor. "
                       "Karar surecinde size nasil yardimci olabiliriz? {okul_adi}"},
            {"gecikme_dk": 10080, "kanal": "sms",
             "sablon": "{veli_adi} bey/hanim, mudurumuz sizinle bizzat gorusmek istiyor. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "randevu_onay_zinciri",
        "ad": "Randevu Onay + Yol Tarifi",
        "trigger": "randevu_alindi",
        "icon": "📅",
        "renk": "#6366f1",
        "aciklama": "Randevu alinir alinmaz onay mesaji + yol tarifi + park bilgisi",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "✅ Merhaba {veli_adi}, randevunuz kaydedildi. {ogrenci_adi} icin sizi bekliyoruz. "
                       "Adresimize ulasim bilgilerini ve park alanini size iletecegiz. {okul_adi}"},
            {"gecikme_dk": 5, "kanal": "whatsapp",
             "sablon": "📍 Adres: {okul_adres}\n📞 {okul_telefon}\n🚗 Park alani mevcut\n"
                       "Gorusmemizde cocuğunuzla ilgili detayli bir sohbet yapacagiz. Kolaylıklar dileriz!"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "randevu_reminder_yarin",
        "ad": "Randevu Yarin Hatirlatma",
        "trigger": "randevu_yarin",
        "icon": "⏰",
        "renk": "#f59e0b",
        "aciklama": "Randevuya 1 gun kala otomatik hatirlatma (cron tabanli)",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "⏰ Merhaba {veli_adi}, yarin {randevu_saati} saat icin {okul_adi} olarak "
                       "{ogrenci_adi} ile sizi bekliyoruz. Goruşmek uzere!"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "randevu_reminder_2saat",
        "ad": "Randevu 2 Saat Oncesi",
        "trigger": "randevu_2saat_oncesi",
        "icon": "🔔",
        "renk": "#f97316",
        "aciklama": "Randevu baslamadan 2 saat once son hatirlatma (cron tabanli)",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "🔔 Sayin {veli_adi}, {randevu_saati} randevumuza 2 saat kaldi. "
                       "Adres: {okul_adres}. Trafik durumunda yola cikmayi unutmayin. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "randevu_kacirildi",
        "ad": "Randevu Kacirildi Geri Donus",
        "trigger": "randevu_kacirildi",
        "icon": "🔄",
        "renk": "#94a3b8",
        "aciklama": "Veli randevuya gelmedi ise ayni gun icinde nazik geri donus",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "Merhaba {veli_adi}, bugun sizi gormek isterdik ancak randevumuzu gerceklestiremedik. "
                       "Sizin icin uygun baska bir zamana yeniden planlayalim mi? {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "test_sonucu_rapor",
        "ad": "Test Sonucu AI Rapor",
        "trigger": "test_sonucu_kaydedildi",
        "icon": "📊",
        "renk": "#8b5cf6",
        "aciklama": "Test sonucu kaydedilince otomatik AI analiz + veliye rapor PDF",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "📊 Merhaba {veli_adi}, {ogrenci_adi} icin uygulanan testin sonuclari hazir. "
                       "AI destekli ayrintili raporumuzu size iletiyoruz. Detaylarda gorusmek isteriz."},
            {"gecikme_dk": 30, "kanal": "email",
             "sablon": "Sayin {veli_adi}, {ogrenci_adi}'in test sonuc raporunu ekte iletiyoruz. "
                       "Guclu alanlari ve gelisim onerileri ile birlikte. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "ihtiyac_analizi_ozel_paket",
        "ad": "Ihtiyac Analizi Kisisel Paket",
        "trigger": "ihtiyac_analizi_tamamlandi",
        "icon": "🎯",
        "renk": "#ec4899",
        "aciklama": "Veli ihtiyaclarini soyledikten sonra AI ile ihtiyac bazli 'Size Uygun Paket' PDF",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "🎯 Sayin {veli_adi}, paylastiginiz ihtiyaclara gore {ogrenci_adi} icin "
                       "kisiye ozel cozum paketi hazirladik. Yakinda detaylari iletecegiz."},
            {"gecikme_dk": 60, "kanal": "email",
             "sablon": "Sayin {veli_adi}, sizin ve {ogrenci_adi} icin hazirladigimiz 'Size Uygun Paket' "
                       "raporunu ekte iletiyoruz. Her endise icin somut cevabimiz var. {okul_adi}"},
        ],
        "varsayilan_aktif": True,
    },
    {
        "id": "kesin_kayit_onboarding_14gun",
        "ad": "Kesin Kayit 14 Gun Onboarding",
        "trigger": "kesin_kayit_yapildi",
        "icon": "🎓",
        "renk": "#10b981",
        "aciklama": "Kesin kayit sonrasi 14 gun boyunca her gun 1 mikro dokunuş — cayma onler",
        "adimlar": [
            {"gecikme_dk": 0, "kanal": "whatsapp",
             "sablon": "🎉 Tebrikler {veli_adi}! {ogrenci_adi} artik {okul_adi} ailesinin uyesi. "
                       "Onumuzdeki 14 gun sizi aramizdaki yerinize aliyoruz. Hosgeldiniz!"},
            {"gecikme_dk": 1440, "kanal": "whatsapp",
             "sablon": "Gun 1: Mudurumuzden {ogrenci_adi}'ye ozel bir karsilama mektubu hazirladik."},
            {"gecikme_dk": 2880, "kanal": "whatsapp",
             "sablon": "Gun 2: Sinif ogretmeninden tanisma mesajini ekte iletiyoruz. {ogrenci_adi} tanismak icin sabirsiz!"},
            {"gecikme_dk": 4320, "kanal": "email",
             "sablon": "Gun 3: Ders programi, kitap listesi ve uniforma detaylarini size iletiyoruz. {okul_adi}"},
            {"gecikme_dk": 5760, "kanal": "whatsapp",
             "sablon": "Gun 4: {ogrenci_adi}'nin ilk hafta yapacagi 5 heyecan verici sey."},
            {"gecikme_dk": 7200, "kanal": "whatsapp",
             "sablon": "Gun 5: Kampus sanal tur linki + yemekhane hafta menusu hazir."},
            {"gecikme_dk": 8640, "kanal": "whatsapp",
             "sablon": "Gun 6: Mevcut veli WhatsApp grubuna davetinizi ekte gonderiyoruz."},
            {"gecikme_dk": 10080, "kanal": "whatsapp",
             "sablon": "Gun 7: Ilk hafta memnuniyet anketimizi paylasmak isteriz. Gorusuniz bizim icin degerli."},
            {"gecikme_dk": 14400, "kanal": "whatsapp",
             "sablon": "Gun 10: {ogrenci_adi}'nin ilk 10 gun ozeti + rehberlik randevu teklifi."},
            {"gecikme_dk": 20160, "kanal": "email",
             "sablon": "Gun 14: Ilk 2 hafta raporu + veli paylasimi. {okul_adi} olarak yaninizdayiz."},
        ],
        "varsayilan_aktif": True,
    },
]


# ============================================================
# OTOMASYON QUEUE (gonderim siralamasi)
# ============================================================

@dataclass
class OtomasyonGorev:
    """Otomasyon kuyrugundaki tek gorev."""
    id: str = field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    otomasyon_id: str = ""
    aday_id: str = ""
    trigger: str = ""
    kanal: str = "whatsapp"
    mesaj: str = ""
    planlanan_zaman: str = ""
    olusturma_zamani: str = field(default_factory=lambda: datetime.now().isoformat())
    durum: str = "bekliyor"  # bekliyor | gonderildi | basarisiz | iptal
    gonderim_zamani: str = ""
    hata: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "OtomasyonGorev":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class OtomasyonStore:
    """Otomasyon kurallari + gorev kuyrugu."""

    def __init__(self) -> None:
        self.base = get_data_path("kayit_modulu")
        os.makedirs(self.base, exist_ok=True)
        self.kurallar_file = os.path.join(self.base, "otomasyonlar.json")
        self.gorevler_file = os.path.join(self.base, "otomasyon_gorevleri.json")
        self.log_file = os.path.join(self.base, "otomasyon_log.json")

    def get_aktif_kurallar(self) -> dict[str, bool]:
        """Hangi otomasyonlar aktif? {id: bool}"""
        if os.path.exists(self.kurallar_file):
            try:
                with open(self.kurallar_file, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default
        return {o["id"]: o["varsayilan_aktif"] for o in OTOMASYONLAR}

    def save_aktif_kurallar(self, kurallar: dict[str, bool]) -> None:
        with open(self.kurallar_file, "w", encoding="utf-8") as f:
            json.dump(kurallar, f, ensure_ascii=False, indent=2)

    def load_gorevler(self) -> list[OtomasyonGorev]:
        if not os.path.exists(self.gorevler_file):
            return []
        try:
            with open(self.gorevler_file, encoding="utf-8") as f:
                data = json.load(f)
            return [OtomasyonGorev.from_dict(d) for d in data]
        except Exception:
            return []

    def save_gorevler(self, gorevler: list[OtomasyonGorev]) -> None:
        with open(self.gorevler_file, "w", encoding="utf-8") as f:
            json.dump([g.to_dict() for g in gorevler], f, ensure_ascii=False, indent=2)

    def add_gorev(self, gorev: OtomasyonGorev) -> None:
        gorevler = self.load_gorevler()
        gorevler.append(gorev)
        self.save_gorevler(gorevler)

    def log_event(self, otomasyon_id: str, aday_id: str, durum: str, mesaj: str = "") -> None:
        """Log dosyasina yaz."""
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, encoding="utf-8") as f:
                    logs = json.load(f)
            except Exception:
                pass
        logs.append({
            "tarih": datetime.now().isoformat(),
            "otomasyon_id": otomasyon_id,
            "aday_id": aday_id,
            "durum": durum,
            "mesaj": mesaj[:200],
        })
        # Son 1000 kayit
        logs = logs[-1000:]
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def get_istatistikler(self) -> dict:
        """Otomasyon istatistikleri."""
        gorevler = self.load_gorevler()
        toplam = len(gorevler)
        gonderildi = sum(1 for g in gorevler if g.durum == "gonderildi")
        bekliyor = sum(1 for g in gorevler if g.durum == "bekliyor")
        basarisiz = sum(1 for g in gorevler if g.durum == "basarisiz")
        return {
            "toplam": toplam,
            "gonderildi": gonderildi,
            "bekliyor": bekliyor,
            "basarisiz": basarisiz,
            "basari_orani": round(gonderildi / toplam * 100, 1) if toplam else 0,
        }


# ============================================================
# TRIGGER FONKSIYONLARI
# ============================================================

def trigger_yeni_aday(aday) -> int:
    """Yeni aday eklenince cagril. Return: planlanmis gorev sayisi."""
    return _create_tasks_for_trigger(aday, "yeni_aday")


def trigger_gorusme_tamamlandi(aday) -> int:
    return _create_tasks_for_trigger(aday, "gorusme_tamamlandi")


def trigger_sozlesme_imzalandi(aday) -> int:
    return _create_tasks_for_trigger(aday, "sozlesme_imzalandi")


def trigger_arama_cevapsiz(aday) -> int:
    return _create_tasks_for_trigger(aday, "arama_cevapsiz")


def trigger_isi_dustu(aday) -> int:
    return _create_tasks_for_trigger(aday, "isi_dustu")


# ─── YENI TRIGGER'LAR (Pipeline Kapsamı Tam) ───

def trigger_fiyat_verildi(aday) -> int:
    """Fiyat kaydedilir kaydedilmez anlik teklif zinciri baslatir."""
    return _create_tasks_for_trigger(aday, "fiyat_verildi")


def trigger_randevu_alindi(aday) -> int:
    """Randevu alindiginda onay + yol tarifi zinciri."""
    return _create_tasks_for_trigger(aday, "randevu_alindi")


def trigger_test_sonucu_kaydedildi(aday) -> int:
    """Test sonucu kaydedilince AI rapor tetikler."""
    return _create_tasks_for_trigger(aday, "test_sonucu_kaydedildi")


def trigger_ihtiyac_analizi_tamamlandi(aday) -> int:
    """Ihtiyac analizi dolunca kisisel AI paket uretilir."""
    return _create_tasks_for_trigger(aday, "ihtiyac_analizi_tamamlandi")


def trigger_kesin_kayit(aday) -> int:
    """Kesin kayit tamamlaninca 14 gun onboarding zinciri baslat."""
    return _create_tasks_for_trigger(aday, "kesin_kayit_yapildi")


def trigger_randevu_yarin(aday) -> int:
    """Randevu yarinda — hatirlatma."""
    return _create_tasks_for_trigger(aday, "randevu_yarin")


def trigger_randevu_2saat(aday) -> int:
    """Randevuya 2 saat kaldi — son hatirlatma."""
    return _create_tasks_for_trigger(aday, "randevu_2saat_oncesi")


def trigger_randevu_kacirildi(aday) -> int:
    """Veli randevuya gelmedi — geri donus planlanir."""
    return _create_tasks_for_trigger(aday, "randevu_kacirildi")


def trigger_olumsuz_30gun(aday) -> int:
    """Olumsuz olmus aday 30 gun gecti — geri donus kampanyasi."""
    return _create_tasks_for_trigger(aday, "olumsuz_isaretlendi_30gun")


def trigger_fiyat_3gun(aday) -> int:
    """Fiyat verildi ve 3 gun gecti — hatirlatma."""
    return _create_tasks_for_trigger(aday, "fiyat_verildi_3gun")


def trigger_dogum_gunu(aday) -> int:
    """Bugun dogum gunu — kutlama."""
    return _create_tasks_for_trigger(aday, "dogum_gunu")


def _create_tasks_for_trigger(aday, trigger_name: str) -> int:
    """Verilen trigger icin aktif tum otomasyonlardan gorevler olustur."""
    store = OtomasyonStore()
    aktif_kurallar = store.get_aktif_kurallar()

    a = aday if isinstance(aday, dict) else aday.to_dict()
    aday_id = a.get("id", "")
    veli_adi = a.get("veli_adi", "")
    ogrenci_adi = a.get("ogrenci_adi", "")
    randevu_tarihi = a.get("randevu_tarihi", "") or ""
    randevu_saati = a.get("randevu_saati", "") or ""

    okul_adi = "okulumuz"
    okul_telefon = "0212 ..."
    okul_adres = ""

    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili() or {}
        okul_adi = kp.get("okul_adi", kp.get("kurum_adi", kp.get("name", okul_adi))) or okul_adi
        okul_telefon = kp.get("telefon", kp.get("phone", okul_telefon)) or okul_telefon
        okul_adres = kp.get("adres", kp.get("address", "")) or ""
    except Exception:
        pass

    # Sablon format kwargs — herhangi bir alan eksikse KeyError atmasin
    format_kwargs = {
        "veli_adi": veli_adi or "Sayin Veli",
        "ogrenci_adi": ogrenci_adi or "ogrenciniz",
        "okul_adi": okul_adi,
        "okul_telefon": okul_telefon,
        "okul_adres": okul_adres or "Okul adresimiz",
        "randevu_tarihi": randevu_tarihi,
        "randevu_saati": randevu_saati,
    }

    sayac = 0
    for otom in OTOMASYONLAR:
        if otom["trigger"] != trigger_name:
            continue
        if not aktif_kurallar.get(otom["id"], otom["varsayilan_aktif"]):
            continue

        for adim in otom["adimlar"]:
            try:
                mesaj = adim["sablon"].format(**format_kwargs)
            except KeyError:
                # Eksik anahtar varsa sablon icin bos ekle
                mesaj = adim["sablon"]
            planlanan = (datetime.now() + timedelta(minutes=adim["gecikme_dk"])).isoformat()
            gorev = OtomasyonGorev(
                otomasyon_id=otom["id"],
                aday_id=aday_id,
                trigger=trigger_name,
                kanal=adim["kanal"],
                mesaj=mesaj,
                planlanan_zaman=planlanan,
            )
            store.add_gorev(gorev)
            sayac += 1

        store.log_event(otom["id"], aday_id, "queued",
                        f"{len(otom['adimlar'])} gorev planlandi")

    return sayac


# ============================================================
# KUYRUGU ISLE (cron-like)
# ============================================================

def gorevleri_isle(test_modu: bool = True) -> dict:
    """
    Kuyrugu kontrol et — vakti gelen gorevleri 'gonder'.

    test_modu=True: Gercek mesaj atmaz, sadece simule eder

    Returns: {islenen, basarili, basarisiz}
    """
    store = OtomasyonStore()
    gorevler = store.load_gorevler()
    now = datetime.now()

    islenen = 0
    basarili = 0
    basarisiz = 0

    for g in gorevler:
        if g.durum != "bekliyor":
            continue
        try:
            planlanan = datetime.fromisoformat(g.planlanan_zaman)
            if planlanan > now:
                continue  # zamani gelmedi
        except Exception:
            continue

        islenen += 1
        try:
            if test_modu:
                # Simulasyon
                g.durum = "gonderildi"
                g.gonderim_zamani = now.isoformat()
                basarili += 1
            else:
                # Gercek gonderim (entegrasyon yok — placeholder)
                # SMS icin: utils.bildirim_servisi.BildirimServisi kullan
                g.durum = "gonderildi"
                g.gonderim_zamani = now.isoformat()
                basarili += 1
            store.log_event(g.otomasyon_id, g.aday_id, "sent", g.mesaj[:100])
        except Exception as e:
            g.durum = "basarisiz"
            g.hata = str(e)[:200]
            basarisiz += 1
            store.log_event(g.otomasyon_id, g.aday_id, "failed", str(e))

    store.save_gorevler(gorevler)
    return {
        "islenen": islenen,
        "basarili": basarili,
        "basarisiz": basarisiz,
    }


# ============================================================
# CRON SCHEDULER — Zamana Bagli Otomasyonlar
# ============================================================
# Streamlit'te gercek cron yok — ana sayfa acilisinda "son calisma"
# kontrol edilir ve 4 saatten fazla gecmisse cron_tara tekrar calistirilir.

def _cron_meta_file() -> str:
    """Son cron calisma zamanini tutan dosya."""
    try:
        base = get_data_path("kayit_modulu")
    except Exception:
        base = os.path.join("data", "kayit_modulu")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "cron_meta.json")


def son_cron_zamani() -> datetime | None:
    """Son basarili cron calismasinin zamanini dondur."""
    p = _cron_meta_file()
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        s = data.get("son_calisma", "")
        if s:
            return datetime.fromisoformat(s)
    except Exception:
        pass
    return None


def _kaydet_cron_zamani(stat: dict):
    """Cron meta'yi guncelle."""
    p = _cron_meta_file()
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
    """Son calismadan saat_esigi saat gectiyse True."""
    son = son_cron_zamani()
    if son is None:
        return True
    return (datetime.now() - son).total_seconds() >= saat_esigi * 3600


def cron_tara(adaylar: list | None = None, force: bool = False) -> dict:
    """
    Tum aday havuzunu tara ve zaman tabanli tetikleyicileri uygula.

    Triggers checked:
      1. fiyat_verildi_3gun  — fiyat verildi + 3 gun
      2. olumsuz_30gun       — olumsuz + 30 gun
      3. dogum_gunu          — bugun dogum gunu
      4. isi_dustu           — bir onceki taramaya gore isi dustuyse
      5. randevu_yarin       — randevu tarihi yarin
      6. randevu_2saat       — randevu saati 2 saat sonra
      7. randevu_kacirildi   — randevu saati gecti ve gorusme yapilmadi

    force=False ise ve son calismadan 4 saat gecmediyse atla.
    """
    if not force and not cron_gerekli_mi():
        son = son_cron_zamani()
        return {
            "atlandi": True,
            "neden": "4 saat gecmedi",
            "son_calisma": son.isoformat(timespec="seconds") if son else None,
        }

    # Adaylari yukle
    if adaylar is None:
        try:
            from models.kayit_modulu import get_kayit_store
            adaylar = get_kayit_store().load_all()
        except Exception:
            return {"atlandi": True, "neden": "aday yuklemesi hata"}

    bugun = date.today()
    now = datetime.now()

    sonuc = {
        "taranan": len(adaylar),
        "fiyat_3gun": 0,
        "olumsuz_30gun": 0,
        "dogum_gunu": 0,
        "isi_dustu": 0,
        "randevu_yarin": 0,
        "randevu_2saat": 0,
        "randevu_kacirildi": 0,
        "toplam_tetiklendi": 0,
        "atlandi": False,
    }

    # Onceki ısı kayıtlarını yukle (isi_dustu detector icin)
    onceki_isilar = _onceki_isi_yukle()
    yeni_isilar: dict[str, str] = {}

    for aday in adaylar:
        a = aday if isinstance(aday, dict) else aday.to_dict()
        aday_id = a.get("id", "")
        if not aday_id:
            continue
        asama = a.get("asama", "")

        # ─── 1. FIYAT 3 GUN ───
        if asama == "fiyat_verildi":
            try:
                son_islem = a.get("son_islem_tarihi", "")[:10]
                if son_islem:
                    gun_sayisi = (bugun - date.fromisoformat(son_islem)).days
                    if 3 <= gun_sayisi <= 4:  # 3-4 gun arasinda
                        # Ayni aday icin daha once tetiklenmedi mi?
                        if not _trigger_daha_once_yapildi(aday_id, "fiyat_verildi_3gun"):
                            trigger_fiyat_3gun(aday)
                            sonuc["fiyat_3gun"] += 1
                            sonuc["toplam_tetiklendi"] += 1
            except (ValueError, TypeError):
                pass

        # ─── 2. OLUMSUZ 30 GUN ───
        if asama == "olumsuz":
            try:
                kapanma = a.get("kapanma_tarihi", "")[:10]
                if kapanma:
                    gun_sayisi = (bugun - date.fromisoformat(kapanma)).days
                    if 30 <= gun_sayisi <= 31:
                        if not _trigger_daha_once_yapildi(aday_id, "olumsuz_isaretlendi_30gun"):
                            trigger_olumsuz_30gun(aday)
                            sonuc["olumsuz_30gun"] += 1
                            sonuc["toplam_tetiklendi"] += 1
            except (ValueError, TypeError):
                pass

        # ─── 3. DOGUM GUNU ───
        # Sadece kesin_kayit olmus veya aktif olanlar
        if asama in ("kesin_kayit", "aday", "arandi", "randevu", "gorusme",
                      "fiyat_verildi", "sozlesme"):
            dogum = a.get("ogrenci_dogum_tarihi", "") or ""
            if dogum and len(dogum) >= 10:
                try:
                    d = date.fromisoformat(dogum[:10])
                    if d.month == bugun.month and d.day == bugun.day:
                        # Her yil bir kere
                        yil_key = f"dogum_gunu_{bugun.year}"
                        if not _trigger_daha_once_yapildi(aday_id, yil_key):
                            trigger_dogum_gunu(aday)
                            _trigger_yapildi_kaydet(aday_id, yil_key)
                            sonuc["dogum_gunu"] += 1
                            sonuc["toplam_tetiklendi"] += 1
                except (ValueError, TypeError):
                    pass

        # ─── 4. ISI DUSTU ───
        if asama not in ("kesin_kayit", "olumsuz"):
            try:
                from models.kayit_takip_engine import hesapla_isi
                isi_sonuc = hesapla_isi(aday)
                yeni_seviye = isi_sonuc.get("isi", "BUZ") if isinstance(isi_sonuc, dict) else "BUZ"
                eski_seviye = onceki_isilar.get(aday_id, "")
                yeni_isilar[aday_id] = yeni_seviye

                seviye_sira = {"SICAK": 4, "ILIK": 3, "SOGUK": 2, "BUZ": 1}
                if (eski_seviye and yeni_seviye and
                    seviye_sira.get(yeni_seviye, 0) < seviye_sira.get(eski_seviye, 0)):
                    trigger_isi_dustu(aday)
                    sonuc["isi_dustu"] += 1
                    sonuc["toplam_tetiklendi"] += 1
            except Exception:
                pass

        # ─── 5, 6, 7. RANDEVU TETIKLEYICILERI ───
        if asama == "randevu":
            randevu_tarihi = a.get("randevu_tarihi", "") or ""
            randevu_saati = a.get("randevu_saati", "") or ""
            if randevu_tarihi and len(randevu_tarihi) >= 10:
                try:
                    rt_date = date.fromisoformat(randevu_tarihi[:10])
                    gun_fark = (rt_date - bugun).days

                    # 5. Randevu yarin
                    if gun_fark == 1:
                        if not _trigger_daha_once_yapildi(aday_id, "randevu_yarin"):
                            trigger_randevu_yarin(aday)
                            sonuc["randevu_yarin"] += 1
                            sonuc["toplam_tetiklendi"] += 1

                    # 6. Randevu 2 saat oncesi (bugun ve saat yakin)
                    if gun_fark == 0 and randevu_saati:
                        try:
                            hh, mm = randevu_saati.split(":")[:2]
                            rt_dt = datetime.combine(rt_date, datetime.min.time()).replace(
                                hour=int(hh), minute=int(mm)
                            )
                            delta_sn = (rt_dt - now).total_seconds()
                            # 1.5 saat - 2.5 saat arasi
                            if 5400 <= delta_sn <= 9000:
                                if not _trigger_daha_once_yapildi(aday_id, "randevu_2saat_oncesi"):
                                    trigger_randevu_2saat(aday)
                                    sonuc["randevu_2saat"] += 1
                                    sonuc["toplam_tetiklendi"] += 1
                            # 7. Randevu kacirildi (saati gecti, negatif)
                            if -3600 >= delta_sn >= -18000:  # 1-5 saat gecmis
                                if not _trigger_daha_once_yapildi(aday_id, "randevu_kacirildi"):
                                    trigger_randevu_kacirildi(aday)
                                    sonuc["randevu_kacirildi"] += 1
                                    sonuc["toplam_tetiklendi"] += 1
                        except (ValueError, IndexError):
                            pass
                except (ValueError, TypeError):
                    pass

    # Yeni isi seviyelerini kaydet (bir sonraki tarama icin)
    _onceki_isi_kaydet(yeni_isilar)

    # Cron zaman kaydi
    _kaydet_cron_zamani(sonuc)

    return sonuc


def _trigger_daha_once_yapildi(aday_id: str, trigger_key: str) -> bool:
    """Bu aday icin bu trigger bir kere calismis mi? Log'tan bakar."""
    try:
        store = OtomasyonStore()
        if not os.path.exists(store.log_file):
            return False
        with open(store.log_file, encoding="utf-8") as f:
            logs = json.load(f)
        for log in logs:
            if (log.get("aday_id") == aday_id and
                trigger_key in log.get("otomasyon_id", "") and
                log.get("durum") == "queued"):
                return True
    except Exception:
        pass
    return False


def _trigger_yapildi_kaydet(aday_id: str, trigger_key: str):
    """Manuel trigger log'u (ornek: dogum gunu)."""
    try:
        store = OtomasyonStore()
        store.log_event(trigger_key, aday_id, "queued", "cron_tara manual")
    except Exception:
        pass


def _onceki_isi_yukle() -> dict:
    """Bir onceki cron taramasindaki isi seviyelerini yukle."""
    try:
        base = get_data_path("kayit_modulu")
        p = os.path.join(base, "cron_isi_snapshot.json")
    except Exception:
        p = os.path.join("data", "kayit_modulu", "cron_isi_snapshot.json")
    if not os.path.exists(p):
        return {}
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _onceki_isi_kaydet(isilar: dict):
    """Isi seviyelerini bir sonraki tarama icin kaydet."""
    try:
        base = get_data_path("kayit_modulu")
    except Exception:
        base = os.path.join("data", "kayit_modulu")
    os.makedirs(base, exist_ok=True)
    p = os.path.join(base, "cron_isi_snapshot.json")
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(isilar, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
