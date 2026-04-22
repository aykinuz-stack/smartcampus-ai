#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartCampusAI — Kullanma Kilavuzu — Modul Verileri
40 modulun detayli kilavuz verisi.

Veri sekli:
{
    section_no, grup, ad, icon, accent, yeni,
    amac (str), kim [(role, desc)], ana_ozellikler [str],
    sekmeler [(name, purpose, [usage_step])],
    is_akisi [str], ipuclari [str], sss [(s, c)]
}
"""
from reportlab.lib.colors import HexColor

# Renk paleti (generate_manual.py ile ayni)
TEAL = HexColor("#0891B2")
EMERALD = HexColor("#059669")
PURPLE = HexColor("#7C3AED")
CORAL = HexColor("#F43F5E")
BLUE = HexColor("#2563EB")
AMBER = HexColor("#D97706")
INDIGO = HexColor("#4F46E5")
ROSE = HexColor("#E11D48")
LIME = HexColor("#65A30D")
SKY = HexColor("#0284C7")
FUCHSIA = HexColor("#C026D3")
CYAN = HexColor("#06B6D4")
ORANGE = HexColor("#EA580C")
SLATE = HexColor("#475569")
VIOLET = HexColor("#8B5CF6")
PINK = HexColor("#EC4899")
GOLD = HexColor("#C5962E")

# ═══════════════════════════════════════════════════════════
# 40 MODUL
# ═══════════════════════════════════════════════════════════

MODULLER = [
    # ──────────────────── GENEL (2) ────────────────────
    {
        "section_no": 1, "grup": "GENEL", "ad": "Ana Sayfa", "icon": "🏠",
        "accent": INDIGO, "yeni": False,
        "amac": (
            "Ana Sayfa, SmartCampus AI'ya girdiginde karsilastigin ilk ekrandir. 40+ modulun tamamina "
            "tek tiklama ile erismeni saglayan kart tabanli navigasyon merkezidir. Uzerinde hizli "
            "arama, role gore filtreleme ve sik kullanilan modullere kisayol sunar."
        ),
        "kim": [
            ("Tum Kullanicilar", "Sisteme giren herkes ilk olarak Ana Sayfa'yi gorur."),
            ("Yoneticiler", "Gun icinde hangi modulde ne yapilacaksa buradan dagilir."),
            ("Ogretmenler", "Yoklama, not girisi ve ders defteri icin hizli erisim kartlarini kullanir."),
        ],
        "ana_ozellikler": [
            "Rol bazli modul kartlari — sadece yetkili olunan modulleri gosterir",
            "Modul kartlarinda rapid-search (anlik arama) — isim yazmaya baslar baslamaz filtreler",
            "Son ziyaret edilen moduller ve favoriler",
            "Duyuru ve ozel gun bilgileri ust bantta",
            "Smarti AI asistani sag-alt kosede her an ulasilabilir",
        ],
        "sekmeler": [
            ("Modul Kartlari", "40+ modul 5 grupta (GENEL/KURUM/AKADEMIK/OPERASYON/SISTEM) dinamik kart olarak.",
                ["Kart uzerine tikla module gir", "Karta hover et ozet tooltip gor"]),
            ("Arama Cubugu", "Modul veya ozellik ismi yazarak an be an filtreleme.",
                ["Modul ismi yaz", "ARAMA ENTER'a bas veya kart sec"]),
            ("Favoriler", "En sik kullandigin 6 modulu sabitleyebilirsin.",
                ["Kart sag-ust kosesindeki yildiza tikla", "Favoriler bolumunde sirala"]),
            ("Duyuru Bandi", "Okul-geneli duyurular ve sistem bildirimleri ust bantta kayar.",
                ["Bildirime tikla detay ac", "X ile dismiss et (sadece bu oturum)"]),
            ("Smarti Widget", "Sag-alt kosede her sayfada erisilebilen AI asistan widget'i.",
                ["Sohbet baslat", "Ses butonuna bas konus"]),
        ],
        "is_akisi": [
            "Giris yap — Ana Sayfa otomatik acilir.",
            "Rolune gore modulleri incele; sol ustteki arama cubuguna ihtiyacin olan modulun ismini yaz.",
            "Kart uzerine tikla — ilgili modul acilir.",
            "Modulden cikmak icin ust sol SmartCampus logosuna tikla, Ana Sayfa'ya don.",
            "Smarti widget ile anlik soru sor — 'Bu hafta yapilacak sinavlar neler?' gibi.",
        ],
        "ipuclari": [
            "En sik kullandigin 6 modulu Favoriler'e al — her oturum acilista kisayol olarak yukaridadir.",
            "Smarti'ye dogal dilde komut verebilirsin: 'Kayit modulunu ac' → otomatik yonlendirir.",
            "Bildirimleri kacirmamak icin ust banti gun ici tekrar kontrol et.",
            "★ OGRENCI ROLUYLE GIRDI ISEN: Ogrenci Panel'in ust bolumunde '😊 Bugunkü Ruh Halin' acilir kutucugu goreceksin — gunluk 5 saniyede mood check-in. Bu veri gizli, sadece rehbere gider ve Erken Uyari motoru'nun duygusal boyutunu besler.",
        ],
        "sss": [
            ("Modul kartim yok?", "Yoneticinden rol izni istemen gerekiyor. Her rol sadece yetkili oldugu modulleri gorur."),
            ("Arama calismiyor?", "Turkce karakter kontrol et. 'ogrenci' ile 'oğrenci' ikisi de calisir."),
        ],
    },
    {
        "section_no": 2, "grup": "GENEL", "ad": "Yonetim Tek Ekran", "icon": "📊",
        "accent": SKY, "yeni": False,
        "amac": (
            "Yonetim Tek Ekran, okul yoneticisinin gun baslangicinda 5 dakikada tum okulun nabzini "
            "kontrol ettigi merkez dashboard'dir. 18 modulden otomatik veri toplar, KPI'lari gorsel "
            "olarak sunar, Smarti AI ile sozel raporlama yapar ve gunluk planlama araclarini icerir."
        ),
        "kim": [
            ("Okul Muduru", "Gun basi ve son 5 dakikada okulun tum metriklerini kontrol eder."),
            ("Mudur Yardimcilari", "Sorumlu olduklari alan icin KPI ve uyari takibi yapar."),
            ("Egitim Koordinatoru", "Akademik performans, rehberlik ve sinav metriklerini izler."),
        ],
        "ana_ozellikler": [
            "18 modulden otomatik cross-module veri toplama",
            "Rol-adapte KPI kartlari — yonetici rolune gore degisir",
            "Bugun ne var? — dinamik ders programi + etkinlik + randevu ozeti",
            "Smarti AI asistani ile sozel rapor: 'Bu haftaki ogrenci devamsizligi nasil?'",
            "Kampus Wiki entegrasyonu ile dahili bilgi tabanina erisim",
            "Tek tikla rapor uretimi (Excel/PDF)",
        ],
        "sekmeler": [
            ("Dashboard", "Okul geneli KPI'lar: ogrenci/ogretmen sayisi, devamsizlik, basari ortalamasi, mali durum, kayit dönüsüm.",
                ["Ust karttlardan birine tikla detay gor", "Zaman filtresi: bugun/hafta/ay secimi"]),
            ("Gunluk Planlama ve Isler", "Yoneticinin bugun ne yapacaginin otomatik listesi: toplantilar, denetimler, imzalar.",
                ["Gorevi tamamlayinca onay kutusunu isaretle", "Yeni gorev ekle: '+' butonu"]),
            ("Modul Islemler", "Her modulun bekleyen islemleri (onay bekleyen izinler, fatura, talep vs).",
                ["Modul kartindan tikla ilgili moduldeki detayi ac", "Hizli aksiyon: onayla/reddet butonlari"]),
            ("Rapor Olustur", "Otomatik rapor sablonlari: haftalik, aylik, donemlik, ozel tarih.",
                ["Sablon sec", "Tarih araligi belirle", "PDF/Excel olarak indir"]),
            ("Smarti Chat", "Yoneticiye ozel AI asistan — 'Hangi ogrenciler risk altinda?', 'Butce durumu?' gibi sorular.",
                ["Soru yaz veya ses butonuna bas", "AI yanit + grafik uretir"]),
        ],
        "is_akisi": [
            "Sabah 08:00 — Yonetim Tek Ekran'i ac, Dashboard KPI'larini incele.",
            "Gunluk Planlama ve Isler sekmesinden bugunun gorevlerini oku.",
            "Modul Islemler'de bekleyen onaylari birer birer islet.",
            "Smarti'ye sor: 'Bugun dikkat etmem gereken bir sey var mi?'",
            "Aksam: Rapor Olustur ile gun ozeti PDF'i uret, arsivle.",
        ],
        "ipuclari": [
            "Smarti'ye dogal dilde karsilastirmali sorular sor: 'Bu ay geçen aya göre devamsizlik nasil?'",
            "Dashboard uzerindeki her sayi tiklanabilir — ilgili ekrana direct goturur.",
            "Favori KPI kartlarini kisisellestir: sag-ust '...' menusu ile sirala.",
        ],
        "sss": [
            ("Veriler neden eski?", "Her modul kendi guncelleme dongusunde veri gonderir. Dashboard'i F5 ile yenile."),
            ("Smarti yanlis cevap veriyor?", "Smarti chat gecmisini temizle ve sorunu yeniden sor. OpenAI key'in aktif oldugundan emin ol."),
        ],
    },

    # ──────────────────── KURUM (9) ────────────────────
    {
        "section_no": 3, "grup": "KURUM", "ad": "Kurumsal Organizasyon ve Iletisim", "icon": "🏢",
        "accent": BLUE, "yeni": False,
        "amac": (
            "Kurumsal Organizasyon modulu, okulun hiyerarsik yapisi, pozisyon tanimlari, organizasyon "
            "semasi, kurum profili ve halkla iliskiler yonetiminin kalbi. Hem hukuki belgeler (vergi no, "
            "tuzuk) hem de iletisim bilgileri buradan yonetilir. Pozisyon tanimlari tum diger modulleri "
            "(IK, Randevu, Toplanti) besler."
        ),
        "kim": [
            ("Kurucu/Mudur", "Kurum profilini ve hiyerarsi yapisini tanimlar."),
            ("Mudur Yardimcilari", "Pozisyonlar icin yetki/sorumluluk tanimlar."),
            ("Halkla Iliskiler Sorumlusu", "Veli memnuniyet anketleri ve PR kampanyalarini yonetir."),
        ],
        "ana_ozellikler": [
            "Kurum profili CRUD — ad, vergi no, adres, iletisim, logo, mutluluk hedefleri",
            "Pozisyon CRUD — unvan, sorumluluk, raporlanacak pozisyon",
            "Otomatik organizasyon semasi (Graphviz ile gorsel hiyerarsi)",
            "SWOT analizi modulu — gucler/zayifliklar/firsatlar/tehditler",
            "Veli Memnuniyet Anketi — 5-boyutlu anket + trend grafigi",
            "Halkla Iliskiler — PR kampanyalari, basin bulteni, kurumsal iletisim",
            "Veli Yetenek Bankasi (v2 ★) — 13 meslek kategorisi, veli ag haritasi",
        ],
        "sekmeler": [
            ("Kurum Profili", "Kurumun temel bilgileri (ad, vergi, adres, iletisim, logo, kurulusu yilı).",
                ["Dolusmamis alanlari doldur", "Logo yukle (512×512 PNG onerilir)", "Kaydet"]),
            ("Pozisyon Yonetimi", "Kurumdaki tum pozisyonlar CRUD (hatirla: IK ve diger moduller buradan besleniyor).",
                ["Yeni pozisyon ekle: '+' butonu", "Unvan, gorev, raporlanan pozisyonu gir", "Hiyerarsi sırasını ayarla"]),
            ("Organizasyon Semasi", "Pozisyon verilerinden otomatik Graphviz tabanli hiyerarsik sema.",
                ["Sema ile aci kontrolu yap", "PNG/PDF olarak indir", "Okul panosuna as"]),
            ("SWOT Analizi", "4 kadran: Gucler, Zayifliklar, Firsatlar, Tehditler. Yonetim kurulu calismasi icin ideal.",
                ["Her kadrana 5-7 madde ekle", "Oncelik skoru ver (1-10)", "PDF olarak indir"]),
            ("Veli Memnuniyet", "5-boyutlu anket sablonu (Egitim, Iletisim, Hizmet, Temizlik, Guvenlik).",
                ["Anket olustur ve link paylas (QR)", "Cevaplari bekleyip trend grafigine bak"]),
            ("Halkla Iliskiler", "PR kampanyalari, basin bulteni, medya iletisim listesi.",
                ["Kampanya sablonu sec", "Mesajlama yap", "Basariyi olc (ulasilan/geri donus)"]),
            ("Veli Yetenek Bankasi ★", "13 meslek kategorisinde veli ag haritasi — egitimsel isbirligi icin.",
                ["Velilerin mesleklerini etiketle", "Kategoriye gore filtrele", "Isbirligi teklifi gonder"]),
        ],
        "is_akisi": [
            "Kurulus surecinde: Kurum Profili'ni en bastan doldur (logo + vergi + adres).",
            "Pozisyonlari hiyerarsik olarak ekle (once Mudur, sonra Yardimcilar, sonra diger).",
            "Organizasyon Semasi'nda sonucu gor; hatayi pozisyon editoruyle duzelt.",
            "Yilda 1 kez SWOT analizi yap — yonetim kurulu ile.",
            "Donemde 2 kere Veli Memnuniyet anketi cikar, sonuclara gore PR aksiyonlari al.",
        ],
        "ipuclari": [
            "Pozisyon ekle-sil islemi IK'daki calisan atamalarini etkiler — dikkatli ol.",
            "Veli Memnuniyet anketi gonderirken QR + SMS kombinasyonu en yuksek cevap oranini verir.",
            "SWOT'u her yil gunlemekle yetinme — kurumsal hafiza icin yillari karsilastir.",
        ],
        "sss": [
            ("Pozisyonu sildim ama hala goruntuleniyor?", "Cache yuzunden olabilir — F5 ile yenile. Kalirsa IK'da atanan calisan var demektir."),
            ("Org semasi yuklenmiyor?", "Graphviz kurulumu gerekli: `pip install graphviz` ve sistem paketi yukle."),
        ],
    },
    {
        "section_no": 4, "grup": "KURUM", "ad": "Kayit Modulu", "icon": "🎯",
        "accent": AMBER, "yeni": False,
        "amac": (
            "Kayit Modulu, aday ogrenciyi 'ilk telefon'dan 'sozlesme imzasina' kadar 7 asamali pipeline ile "
            "takip eden, sifir kayip anlayisiyla kurulmus bir aday yonetim sistemidir. AI lead scoring, "
            "12 ay kampanya takvimi, personel performans karnesi ve detayli donusum raporlari icerir."
        ),
        "kim": [
            ("Kayit Sorumlusu", "Gunluk aday girislerini, aramalari ve gorusmeleri yonetir."),
            ("Mudur Yardimcisi (Kayit)", "Donusum oranlarini ve kampanya etkinligini olcer."),
            ("Rehber Ogretmen", "Aday gorusmelerine katilir, profil degerlendirir."),
        ],
        "ana_ozellikler": [
            "7 asamali pipeline: Aday → Arandi → Randevu → Gorusme → Fiyat Teklifi → Sozlesme → Kayit",
            "AI Lead Scoring — her aday icin %0-100 kayit olasiligi + neden + oneri",
            "12 aylik data arama kampanyasi (her ay KPI hedefi)",
            "Personel performans karnesi (kim kac arama, gorusme, kayit?)",
            "Referans ve bursluluk takip sistemi",
            "Sicak/Ilik/Soguk siniflandirma ve otomatik follow-up planlama",
            "Kayit Diamond Kilavuzu — PDF olarak detayli surec rehberi",
        ],
        "sekmeler": [
            ("Dashboard", "Pipeline ozeti: asama sayilari, bu ay dönüşüm, hedef/gercek farki, en aktif kaynak.",
                ["KPI kartina tikla asama listesine git", "Tarih filtresi: bu ay/cyrek/yil"]),
            ("Aday Yonetimi", "Tum adaylari listele, ara, filtrele; yeni aday ekle veya Excel import.",
                ["'+ Yeni Aday' ile elle ekle", "Import ile Excel yukle", "Sagdan asamaya gec"]),
            ("Pipeline Asama", "7 asamali Kanban goruntusunde aday hareketleri (surukle-birak).",
                ["Adayi surukleyerek sonraki asamaya tasi", "Renkli renk banti: sicak/ilik/soguk"]),
            ("AI Lead Scoring", "Her aday icin AI skor + oneri. Yuksek skorlular once gorusulur.",
                ["AI skoru tikla neden ve aksiyon oner", "Skorlara gore sirala/filtrele"]),
            ("12 Ay Kampanya", "Her ay icin arama hedefi, teklif hazirlama, referans kampanyasi.",
                ["Ay sec kampanya dashboard'una git", "Hedef/gercek/oran gor"]),
            ("Personel Performans", "Kayit personelinin performans karnesi: arama/gorusme/kayit, donusum orani.",
                ["Personel sec detay kart ac", "Karsilastirmali tablo PDF indir"]),
            ("Referans & Bursluluk", "Mevcut velilerden referans, sosyoekonomik bursluluk basvurulari.",
                ["Referans formu linkini gonder", "Bursluluk basvurularini degerlendir"]),
            ("Raporlar", "Donusum analizleri, ay/yil bazli raporlar, AI trend uretimi.",
                ["Rapor sablonu sec", "Tarih + sube filtresi", "PDF/Excel indir"]),
        ],
        "is_akisi": [
            "Aday telefondan arayinca — Aday Yonetimi'ne '+ Yeni Aday' ile kaydet.",
            "Pipeline'da 'Arandi' asamasina tasi, AI skora bak (yuksekse hemen randevu).",
            "Gorusme sonrasi asamayi 'Gorusme' → 'Fiyat Teklifi' olarak ilerlet.",
            "12 Ay Kampanya'dan o ay icin sicak aday listesini cikar, haftalik follow-up.",
            "Ay sonu: Personel Performans ve Raporlar ile donusum oranlarini olc.",
        ],
        "ipuclari": [
            "Aday kaydi ekle + ilk konusma notunu hemen gir — AI scoring dogru islemek icin bagimli.",
            "Sicak adaylari 48 saat icinde geri ara; soguyanlari yeniden aktiflestirmek 3 kat daha zor.",
            "Bursluluk basvurularini mutlaka Rehberlik ile koordine et — birlikte cikan sonuclar daha iyi.",
        ],
        "sss": [
            ("AI Lead Scoring yanlis gorunuyor?", "Aday profilinde veri eksik olabilir (telefon, email, onceki okul). Bos alanlari doldur, skor guncellenir."),
            ("Excel import basarisiz?", "Sablon dosyayi indir: Aday Yonetimi > Import > Sablon Indir. Kolon adlari birebir olmali."),
            ("Pipeline'da asama yanlis goruntuleniyor?", "Aday kartinin sag-ust menusunden 'Manuel Asama Degistir' ile duzelt."),
        ],
    },
    {
        "section_no": 5, "grup": "KURUM", "ad": "Sosyal Medya Yonetimi", "icon": "📱",
        "accent": PINK, "yeni": False,
        "amac": (
            "Sosyal Medya Yonetimi, 5 platformu (Instagram, Facebook, LinkedIn, TikTok, YouTube) tek "
            "arayuzde toplar. Icerik takvimi, onay akisi, direkt/planlanmis yayin, analytics, rakip "
            "izleme, akilli saat onerisi ve hashtag takvimi ile profesyonel kurumsal medya yonetimi sunar."
        ),
        "kim": [
            ("Sosyal Medya Sorumlusu", "Gunluk icerik planlar, yayinlar, etkilesimleri takip eder."),
            ("Grafiker/Tasarimci", "Icerik goruntusunu hazirlayip editore yukler."),
            ("Mudur", "Onay sureclerinde onay/ret karari verir."),
        ],
        "ana_ozellikler": [
            "5 platform (IG, FB, LinkedIn, TikTok, YT) tek panelden yonetim",
            "Icerik takvimi — aylik/haftalik gorunum, surukle-birak planlama",
            "Onay akisi — 'Taslak → Onaya Gonderildi → Yayinlandi'",
            "Analytics — reach/engagement/follower buyume, platform kiyaslama",
            "Gelen kutusu — tum mesajlar ve yorumlar tek panelde",
            "Akilli Saatler Onerisi — takipciler en aktif oldugu saat dilimleri",
            "Hashtag Takvimi — gune ozel hashtag onerileri",
            "Rakip Izleme — rakip okullarin paylasim ve etkilesim analizi",
        ],
        "sekmeler": [
            ("Dashboard", "5 platformun toplu ozeti: follower, engagement, bu hafta reach.",
                ["Kartlara tikla detay analytics", "Tarih filtresi: 7 gun / 30 gun / 90 gun"]),
            ("Hesap Yonetimi", "5 platform hesabini ayri ayri bagla, token yonetimi, yetki ayari.",
                ["Platform sec '+Hesap Ekle'", "OAuth ile baglan", "Aktif/pasif durumu"]),
            ("Icerik Olusturma", "Zengin editor: gorsel + metin + hashtag + emoji + mention.",
                ["Platform sec", "Icerigi hazirla", "Onaya gonder veya direkt planla"]),
            ("Takvim Goruntus", "Aylik/haftalik calendar, surukle-birak ile plan degistirme.",
                ["Ay sec", "Icerik kartini tut surukle", "Zamanlanmis yayin olustur"]),
            ("Onay Akisi", "Taslak icerikler onay bekliyor; yonetici onaylar veya duzeltme ister.",
                ["Icerik kartina tikla detay", "Onayla / Reddet / Duzeltme Iste"]),
            ("Analytics", "Reach, engagement, follower buyume grafikleri; platform karsilastirma.",
                ["Platform ve tarih filtresi", "Export PDF/Excel"]),
            ("Gelen Kutusu", "Tum mesajlar ve yorumlar. Hizli cevap ve etiketleme.",
                ["Mesaj sec", "Hizli cevap sablonu sec veya yaz", "Etiket ekle"]),
            ("Akilli Saat Onerisi", "AI takipci davranisini analiz ederek en iyi yayin saatlerini onerir.",
                ["Platform sec", "Grafikte hotspot'lara bak", "Yayini o saate planla"]),
            ("Hashtag Takvimi", "Gune ozel hashtag onerileri (ozel gunler, trending vb).",
                ["Gun sec", "Hashtag'lari kopyala", "Icerige yapistir"]),
            ("Rakip Izleme", "Rakip okullarin public yayinlari, etkilesim analizi.",
                ["Rakip hesap ekle", "Etkilesim kiyaslamasina bak"]),
        ],
        "is_akisi": [
            "Her pazartesi: haftalik icerik planini Icerik Olusturma'da hazirla (5-7 post).",
            "Akilli Saat Onerisi ile yayin saatlerini belirle.",
            "Takvim Goruntus'de surukle-birak ile saatlere yerlestir.",
            "Onay Akisi'na gonder; mudur onaylayinca otomatik yayinlanir.",
            "Gun icinde Gelen Kutusu'nu kontrol et — tum platformlarin mesajlari tek yerde.",
            "Cuma ogleden sonra Analytics'ten haftalik rapor cikar.",
        ],
        "ipuclari": [
            "Hashtag sayisi: IG 8-12, TikTok 3-5, LinkedIn 3. Platform bazli optimize et.",
            "Rakip Izleme'de en iyi etkilesim alan posta bak — format/saat/hashtag/uzunluk kopyalanabilir.",
            "Akilli Saat onerisi ilk 2 hafta ogrenme asamasidir; veri biriktikce dogruluk artar.",
        ],
        "sss": [
            ("Instagram bagli degil?", "Hesap Yonetimi > OAuth yenile. Facebook Business Manager uzerinden Instagram Business Account gerekli."),
            ("Otomatik yayinlanmiyor?", "Onay akisini kontrol et — onay bekliyor olabilir. Ya da token suresi bitmis olabilir."),
        ],
    },
    {
        "section_no": 6, "grup": "KURUM", "ad": "Insan Kaynaklari Yonetimi", "icon": "👥",
        "accent": PURPLE, "yeni": False,
        "amac": (
            "Insan Kaynaklari modulu, ise alimdan ise cikisa (onboarding → offboarding) kadar tum "
            "calisan yasam dongusunu yonetir. AI destekli mulakat sistemi, ozluk dosyasi, izin "
            "yonetimi, performans degerlendirme, bordro hazirligi, egitim planlama ve disiplin "
            "islemleri tek panelden yurutulur."
        ),
        "kim": [
            ("IK Sorumlusu", "Ise alim, ozluk, izin, bordro islemlerini yurutur."),
            ("Mudur", "Performans degerlendirme ve nihai onaylari verir."),
            ("Calisan", "Kendi izin talebini, ozluk bilgisini, egitim katilimini takip eder."),
        ],
        "ana_ozellikler": [
            "Aday havuzu + AI mulakat soru seti + degerlendirme",
            "Kapsamli ozluk dosyasi (kisisel, egitim, deneyim, belgeler)",
            "Cevrimici izin basvurusu ve onay akisi",
            "360° performans degerlendirme (kendi+yonetici+akran+ast)",
            "Aylik bordro hazirlama + puantaj entegrasyonu",
            "Egitim planlama — zorunlu/onerilen egitimler, sertifika takibi",
            "Offboarding surecleri (KVKK uyumlu veri arsivleme)",
            "Is Yuku Dengeleyici ★ — 10 yuk tipi, burnout/ideal/dusuk durumu",
        ],
        "sekmeler": [
            ("Dashboard", "Calisan sayisi, acik pozisyon, izin durumu, aylik bordro ozeti.",
                ["Kartlara tikla detay", "Bu ay/yil filtresi"]),
            ("Aday Havuzu", "Acik pozisyonlara basvuran tum adaylar, CV, referans.",
                ["Pozisyon sec aday listesi gor", "CV indir", "Mulakata cagir"]),
            ("AI Mulakat", "Pozisyona gore AI'nin onerdigi sorular + degerlendirme sablonlari.",
                ["Pozisyon secildiginde AI soru seti gelir", "Her soru icin 1-5 puan", "Genel not ve oneri"]),
            ("Personel Kayit (Ozluk)", "Tum calisan verileri: kisisel, egitim, deneyim, belgeler, fotograf.",
                ["Calisan ekle", "Sekmelerden ilgili alani doldur", "Belgeleri yukle (PDF/JPG)"]),
            ("Performans Degerlendirme", "360° degerlendirme — 4 kaynaktan geri bildirim.",
                ["Donem sec", "Calisan sec", "4 kaynak degerlendirmesini topla"]),
            ("Izin Yonetimi", "Yillik/ücretsiz/sağlık izinleri — basvuru ve onay akisi.",
                ["Basvuru al", "Takvimde catisma kontrolu", "Onay veya reddet"]),
            ("Egitim Planlama", "Zorunlu/onerilen egitimler + sertifika takvimi.",
                ["Egitim olustur", "Katilimci sec", "Sertifikayi yukle/takip et"]),
            ("Bordro", "Aylik bordro hesaplama, kesinti ve primler, brut/net.",
                ["Ay sec", "Puantajdan veri cek", "Bordro olustur PDF uret"]),
            ("Offboarding", "Isten cikis sureci: belge teslimi, KVKK uyumlu veri arsivleme.",
                ["Checklist ile adimlari takip", "Belgeleri arsive al", "KVKK onayi"]),
            ("Disiplin Islemleri", "Uyari, kinama vb disiplin islemleri; hukuki uyumlu kayit.",
                ["Olay tarihi + acikilama", "Islem turu sec", "Ilgili belgeleri ekle"]),
            ("Is Yuku Dengeleyici ★", "10 yuk tipi (ders, nobet, sinav, idari vb) bazli analiz.",
                ["Calisan sec", "Son 30 gun yukunu gor", "Ideal/burnout durumuna bak"]),
        ],
        "is_akisi": [
            "Acik pozisyon duyurusu — Aday Havuzu'nda pozisyon olustur, kriterleri gir.",
            "Basvurular geldikce AI Mulakat ile sorulari hazirla, mulakat yap, puan gir.",
            "Secilen adayi 'Personel Kayit'a ekle — ozluk dosyasi olustur.",
            "Her ay bordro hazirla, Egitim Planlama ile zorunlu egitimleri planla.",
            "6 ayda bir Performans Degerlendirme yap, sonuclara gore gelisim plani.",
            "Isten cikis olacaksa Offboarding checklist'ini takip et.",
        ],
        "ipuclari": [
            "AI Mulakat soru setlerini pozisyona gore kisisellestir — her seferinde iyilesir.",
            "Is Yuku Dengeleyici'de burnout uyarisi alan personele muhakkak 1:1 gorusme planla.",
            "Disiplin islemlerinde tum belgelerin PDF'lerini ekle — ileride hukuki zemin icin kritik.",
        ],
        "sss": [
            ("Izin onay akisi calismiyor?", "Onay hiyerarsisini Kurumsal Organizasyon > Pozisyon Yonetimi'nde tanimla."),
            ("Bordro puantaji eksik?", "Akademik Takip > Yoklama ile senkronizasyon aktif olmali."),
        ],
    },
    {
        "section_no": 7, "grup": "KURUM", "ad": "Butce Gelir Gider", "icon": "💰",
        "accent": EMERALD, "yeni": False,
        "amac": (
            "Butce Gelir Gider modulu, okulun tum mali suregini tek panelden yonetir. Yillik butce "
            "planlama, aylik gelir/gider takibi, tahminsel-gerceklesen karsilastirmasi, mali analiz, "
            "donemsel raporlar ve AI destekli finansal tavsiye sunar."
        ),
        "kim": [
            ("Mali Isler Sorumlusu", "Gunluk kayit, aylik rapor, yillik butce."),
            ("Mudur/Kurucu", "Butce onayi, yatirim karari."),
            ("Muhasebe Bolumu", "Defter tutulan kayitlari sisteme yansitir."),
        ],
        "ana_ozellikler": [
            "Yillik butce planlama (20+ kategori)",
            "Gunluk gelir/gider kaydi",
            "Tahminsel vs Gerceklesen karsilastirma (her kategori)",
            "Aylik ve donemlik mali raporlar",
            "Nakit akis projeksiyonu (AI)",
            "Butce sapma uyarilari (%10 ustunde otomatik bildirim)",
            "Vergi ve kesinti takibi",
        ],
        "sekmeler": [
            ("Dashboard", "Bu ay gelir/gider, net durum, butce kullanimi, en yuksek kategori.",
                ["Tarih filtresi: ay/cyrek/yil", "Kartlara tikla detay rapor"]),
            ("Butce Planlama", "Yillik butce kategorileri + hedef tutar + aylik dagilim.",
                ["Kategori ekle (Personel/Kira/Elektrik vs)", "Yillik hedef + aylik yuzde"]),
            ("Gelir Kaydi", "Tum gelirler (kayit ucreti, bagis, kira, hibeler vs).",
                ["Yeni kayit: kategori + tutar + tarih + aciklama", "Makbuz ekle"]),
            ("Gider Kaydi", "Tum giderler (maas, fatura, temizlik, yiyecek vs).",
                ["Yeni kayit + makbuz/fatura PDF", "Tekrarli ise 'aylik' isaretle"]),
            ("Tahmin vs Gerceklesen", "Her kategori icin butce hedefi ile gercek durumu karsilastir.",
                ["Ay sec", "Sapma % renkli gor (yesil/turuncu/kirmizi)"]),
            ("Aylik Rapor", "Otomatik aylik rapor: gelir/gider ayrimi, kar-zarar, onemli kalemler.",
                ["Ay sec", "PDF olarak indir", "Yonetim kuruluna gonder"]),
            ("Mali Analiz", "Trend, sezonluk dalgalanma, likidite orani.",
                ["Trend grafigini incele", "Projeksiyon 3-6 ay", "Oneri oku"]),
            ("Raporlar & Export", "Farkli sablonlar: VUK uyumlu, yonetim kurulu, SMMM icin.",
                ["Sablon sec", "Tarih araligi belirle", "Excel/PDF indir"]),
        ],
        "is_akisi": [
            "Yil basi: Butce Planlama'da yillik butce olustur, kategorileri ve tutarlari gir.",
            "Gun icinde: gelir/gider olduguca ilgili sekmede hemen kaydet (makbuz ile).",
            "Ay sonu: Tahmin vs Gerceklesen'e bak, sapmalari analiz et.",
            "Aylik Rapor uret, mudure sun.",
            "3 ayda bir Mali Analiz ile buyuk resmi gor; AI projeksiyonunu dikkate al.",
        ],
        "ipuclari": [
            "Tekrarli giderleri 'aylik' isaretleyerek otomatik kopyala — her ay tekrar girmek zorunda kalma.",
            "Sapma %10'u asinca otomatik uyari al — bildirim ayarlarini aktif et.",
            "Sene sonu vergi icin tum makbuzlari PDF olarak yuklemek kritik.",
        ],
        "sss": [
            ("Butce ustu harcama uyarisi gelmiyor?", "Ayarlar > Bildirimler'de esiklerin aktif oldugundan emin ol."),
            ("Aylik rapor bos?", "Gelir/gider kaydi eksik olabilir. Dashboard'dan toplam kalem sayisini kontrol et."),
        ],
    },
    {
        "section_no": 8, "grup": "KURUM", "ad": "Randevu ve Ziyaretci", "icon": "📅",
        "accent": CYAN, "yeni": False,
        "amac": (
            "Randevu ve Ziyaretci modulu, okula gelecek ziyaretcilerin online randevu alimi, QR kod "
            "tabanli giris/cikis takibi, ziyaretci rehberi, gorusulecek unvan + kisi atamasi ve "
            "raporlamasini tek panelden yonetir. AR Kampus Haritasi ile ziyaretci yonlendirme de dahildir."
        ),
        "kim": [
            ("Guvenlik/Giris Sorumlusu", "Ziyaretci giris/cikis islemlerini gerceklestirir."),
            ("Sekreter", "Randevulari planlayip katilimci atar."),
            ("Ziyaretci/Veli", "Online randevu alir, QR kod ile giris yapar."),
        ],
        "ana_ozellikler": [
            "Online randevu alimi (veli/ziyaretci self-service)",
            "QR kod ile giris/cikis (dokunmasiz)",
            "Ziyaretci rehberi — 'Ben kimim?' cevaplayan AI panel",
            "Gorusulecek Unvan ve Kisi atamasi (IK ile entegre)",
            "Ziyaretci turleri (Veli, Tedarikci, Mufettis, Aday Veli)",
            "AR Kampus Haritasi ★ — 15 lokasyon SVG harita, QR ile aktive",
            "Detayli raporlama ve trend analizi",
        ],
        "sekmeler": [
            ("Dashboard", "Bugunun randevulari, haftanin zirvesi, ziyaretci tipi dagilimi.",
                ["Kart uzerine tikla detay", "Tarih filtresi"]),
            ("Randevu Yonetimi", "Randevu CRUD + QR kod uretimi + email/SMS bildirimi.",
                ["'+ Randevu' ile yeni olustur", "QR kod kendi kendine olusur", "Bildirim ayarla"]),
            ("Ziyaretci Giris/Cikis", "QR tarama ile hizli giris + manuel kayit + fotograf.",
                ["QR okut veya manuel kayit", "Ziyaretci kart yazdir"]),
            ("Ziyaretci Rehberi", "Ziyaretci gorusulecek kisiye nasil ulasir rehberi.",
                ["Lokasyon sec", "Harita gor"]),
            ("Raporlar", "Ziyaretci sayisi, ortalama sure, en sik gelen ziyaretci tipi.",
                ["Tarih araligi sec", "PDF/Excel indir"]),
            ("Ayarlar", "Ziyaretci turleri CRUD + bildirim sablonlari + gorusulecek unvanlar.",
                ["Yeni tur ekle (Veli/Tedarikci vs)", "Email sablonu duzenle"]),
            ("AR Kampus Haritasi ★", "15 lokasyon SVG harita + QR ile mobil AR navigasyon.",
                ["Harita gor", "Ziyaretciye link/QR gonder"]),
        ],
        "is_akisi": [
            "Randevu alim: Ziyaretci website'ten link uzerinden online randevu alir VEYA sekreter manuel olusturur.",
            "Email/SMS ile QR kod gonderilir.",
            "Ziyaretci gun icinde gelince QR'i okutur, fotograf cekilir (opsiyonel), ziyaretci karti cikar.",
            "Gorusulen kisi SMS/notification alir.",
            "Cikis QR tarama ile otomatik, ziyaretci suresi kaydedilir.",
            "Hafta sonu raporlar incelenir.",
        ],
        "ipuclari": [
            "Veli toplantilarini toplu randevu seklinde olustur — 1 tikla tum velilere gonder.",
            "AR Kampus Haritasi'ni ziyaretciye onceden paylas; okul icinde kaybolma sorunu cozulur.",
            "Gorusulecek Kisi listesi otomatik IK'dan gelir — IK'da aktif kalmayan calisani buradan da secemezsin.",
        ],
        "sss": [
            ("QR okumadi, ne yapmali?", "Manuel kayit sekmesinde TC ve ziyaretci turu gir — ayni sureci takip eder."),
            ("Ziyaretci rehberi yuklenmedi?", "Cache sorunu olabilir. F5 ile yenile, veya tarayici cache'ini temizle."),
        ],
    },
    {
        "section_no": 9, "grup": "KURUM", "ad": "Toplanti ve Kurullar", "icon": "🤝",
        "accent": VIOLET, "yeni": False,
        "amac": (
            "Toplanti ve Kurullar modulu, 5 farkli kurul tipini (Ogretmenler Kurulu, Zumre, Okul Meclisi, "
            "Ogrenci Meclisi, Okul Gelisim Kurulu) yonetir. Toplanti planlama, gundem hazirlama, "
            "tutanak kaydi, karar ve aksiyon takibi, AI ozet ve katilimci bildirimleri icerir."
        ),
        "kim": [
            ("Mudur", "Ogretmenler Kurulu ve Okul Gelisim Kurulu'nu yonetir."),
            ("Zumre Baskani", "Zumre toplantilarini planlar, gundem hazirlar."),
            ("Ogrenci Meclisi Baskani", "Ogrenci meclis toplantilarini organize eder."),
        ],
        "ana_ozellikler": [
            "5 kurul tipi (Ogretmenler/Zumre/Okul Meclisi/Ogrenci Meclisi/Okul Gelisim)",
            "Toplanti planlama (tarih, saat, yer, Zoom/Meet linki)",
            "Gundem maddesi ekleme ve onem siralamasi",
            "Katilimci yonetimi + otomatik davetli listesi",
            "Canli tutanak kaydi + sonradan duzenleme",
            "Karar ve aksiyon atama + takip (Due date + sorumlu)",
            "AI ozet — uzun tutanaklardan 1 paragraf ozet",
            "PDF tutanak export (kurumsal sablon)",
        ],
        "sekmeler": [
            ("Dashboard", "Yaklasilan toplanti, bekleyen karar, aksiyon takibi.",
                ["Kartlara tikla detay", "Takvim goruntusunde yaklasilan"]),
            ("Kurul Yonetimi", "5 kurul tipi + her kurul icin uyeler + yetki.",
                ["Kurul sec", "Uye ekle/cikar", "Baskani tayin et"]),
            ("Toplanti Planlama", "Tarih/saat/yer + Zoom linki + katilimci davet.",
                ["Kurul sec", "Tarih + saat", "Yer + online link", "Davet gonder"]),
            ("Gundem Hazirlama", "Madde madde gundem + onem sirasi + sunum PDF.",
                ["Madde ekle", "Suruklerek sirala", "PDF hazirla"]),
            ("Katilimci Yonetimi", "Davetli liste + RSVP + katilim takibi (yuz yuze/online).",
                ["Davetli ekle", "RSVP durumu", "Katilimi isaretle"]),
            ("Karar & Aksiyon", "Alinan kararlar + aksiyon + due date + sorumlu kisi.",
                ["Karar ekle", "Aksiyon baslat (sorumlu + son tarih)", "Durum guncelle"]),
            ("Tutanak Olustur", "Canli tutanak kaydi; kararlari + aksiyonlari otomatik birlestirir.",
                ["Toplanti acilinca 'Kayit Baslat'", "Not al", "Karari isaretle", "PDF olarak indir"]),
            ("AI Ozet", "Uzun tutanaklardan 1 paragraf ozet + Smarti AI ile konu bazinda sorgulama.",
                ["Tutanak sec", "AI ozet iste", "Soruyla detaya in"]),
        ],
        "is_akisi": [
            "Toplantidan 1 hafta once: Toplanti Planlama'dan tarih + yer + katilimcilari ekle.",
            "Gundem Hazirlama'da maddeleri madde madde gir, onem sirala.",
            "Davet + hatirlatici email/notification otomatik gonderilir.",
            "Toplanti anında: Tutanak Olustur 'Kayit Baslat' ile anlik not al.",
            "Kararlari ve aksiyonlari isaretle — sorumlu ve son tarih ata.",
            "Toplanti sonu: PDF tutanak ve AI ozet otomatik hazirlanir.",
            "Haftalik: Karar & Aksiyon'da vadeleri takip et; gecikenler kirmizi isaretlenir.",
        ],
        "ipuclari": [
            "Gundem PDF'ini toplantidan 24 saat once katilimcilara gonder — hazirlikli gelirler.",
            "AI ozet 15 dakikalik tutanaktan sonra en dogru sonucu verir — daha kisasi yetersiz olabilir.",
            "Aksiyon atarken 'sorumlu + son tarih' kombinasyonu olmazsa takip etkisiz kalir.",
        ],
        "sss": [
            ("Tutanak kayboldu?", "Otomatik kaydetme her 60 saniyede. Tutanaklar > Arsiv'de son versiyon var."),
            ("Zoom linki calismiyor?", "Toplanti Planlama > link alanini yeniden yapistir — Zoom tokens suresi bitmis olabilir."),
        ],
    },
    {
        "section_no": 10, "grup": "KURUM", "ad": "Kurum Hizmetleri", "icon": "🏛️",
        "accent": SLATE, "yeni": False,
        "amac": (
            "Kurum Hizmetleri modulu, gunluk kurumsal operasyonu yoneten yardimci hizmetleri toplar: "
            "etkinlik ve duyurular, haftalik yemek menusu, servis/rota yonetimi, veli talep formlari, "
            "mesajlasma, nobet ve ders programi ozetleri. Akademik Takip'ten bagimsiz hizli erisim saglar."
        ),
        "kim": [
            ("Sekreter", "Duyuru ve yemek menusu gunceller."),
            ("Servis Sorumlusu", "Arac, sofor ve rota atamalari yapar."),
            ("Veli", "Talep formu gonderir (belge, donem sonu rapor)."),
        ],
        "ana_ozellikler": [
            "Etkinlik ve duyuru paneli (veli/ogrenciye gorunur)",
            "Haftalik yemek menusu (fotograf + besin degeri)",
            "Servis arac/sofor/rota CRUD + ogrenci atamasi",
            "Veli talep formlari (belge, rapor, gorusme)",
            "Dahili mesajlasma (okul ici)",
            "Nobet yonetimi (AT'den entegre)",
            "Zaman cizelgesi (AT'den entegre)",
            "Ders programi (AT'den entegre)",
        ],
        "sekmeler": [
            ("Etkinlik & Duyurular", "Okul geneli duyurular (veli/ogrenciye gorunur).",
                ["Yeni duyuru ekle", "Hedef kitle sec (tum/sinif/sube)", "Yayinla"]),
            ("Yemek Menu", "Haftalik menu + besin degeri + alerjen uyarisi.",
                ["Haftayi sec", "Gun gun menu gir", "Fotograf ekle", "Yayinla"]),
            ("Servis Yonetimi", "Servis arac/sofor CRUD + rota + ogrenci atamasi.",
                ["Arac ekle (plaka, kapasite)", "Sofor ekle", "Rota ciz", "Ogrenci ata"]),
            ("Veli Talepleri", "Veli talep formlari — belge, donem rapor, gorusme.",
                ["Talep listesi gor", "Durum guncelle (islem/sonuc)", "Cevap gonder"]),
            ("Mesajlasma", "Okul ici yazisma paneli (ogretmen<>veli, vb).",
                ["Sohbet ac", "Mesaj yaz ve gonder"]),
            ("Nobet Yonetimi (AT)", "Akademik Takip'ten gelen nobet programi ozeti.",
                ["Bu hafta nobetci listesi", "Degisim talebi"]),
            ("Zaman Cizelgesi (AT)", "Gunluk/haftalik zaman dilimleri ozet.", []),
            ("Ders Programi (AT)", "Sinif/sube bazli ders programi ozet.", []),
        ],
        "is_akisi": [
            "Haftalik: Yemek Menu'yu Pazartesi oncesi haftayi doldur — veli/ogrenciye otomatik yayinlanir.",
            "Duyuru oldugunda Etkinlik & Duyurular'dan hedefle birlikte yayin yap.",
            "Servis degisiklikleri Servis Yonetimi'nden yapilir — ogrenci ataması ile.",
            "Veli Talepleri sekmesinde gelen talepleri zamaninda yanitla (SLA 24 saat).",
            "Mesajlasma ile ogretmen ve veliler arasinda asenkron iletisim kur.",
        ],
        "ipuclari": [
            "Yemek menu fotograflari besin degerleri ile beraber gorunde veliler cok daha olumlu algilar.",
            "Duyuru hedefini 'Tum Okul' yerine sinif/sube sec — hedefsiz duyuru ilgi kaybeder.",
            "Servis rotasini haftada 1 gunceller gibi gorun — sabit kalsa bile ilgilisin izlemini yarat.",
        ],
        "sss": [
            ("Veli talepleri gelmiyor?", "Veli Paneli'nde form linki aktif mi kontrol et. Bildirim izinleri acilmali."),
            ("Servis rotasi haritada goruntulenmiyor?", "Google Maps API key ayarlanmis olmali (Ayarlar > Integrations)."),
        ],
    },
    {
        "section_no": 11, "grup": "KURUM", "ad": "Veli Gunluk Kapsul", "icon": "📦",
        "accent": INDIGO, "yeni": True,
        "amac": (
            "Veli Gunluk Kapsul (v2.0 ★) her aksam 18:00'de AI'nin veliye gonderdigi 2-3 dakikalik "
            "gunluk ozettir. 'Bugun cocugum ne yapti?' sorusuna tek kapsulde cevap verir: akademik, "
            "sosyal-duygusal, etkinlikler, yarin hazirligi ve gunun ozel ani. WhatsApp, SMS ve "
            "uygulama ici kanallarla calisir."
        ),
        "kim": [
            ("Veli", "Her aksam cocugunun gunluk ozetini tek kapsulde okur."),
            ("Ogretmen", "Gun icinde ozel bir an varsa kapsule not ekler."),
            ("Sistem", "Diger modullerden veriyi otomatik toplar, AI ile ozetler."),
        ],
        "ana_ozellikler": [
            "Her aksam 18:00'de otomatik AI ozet uretimi",
            "6 bolum: Akademik, Sosyal-Duygusal, Etkinlik, Yarin, Ozel An, Mood",
            "3 kanal: Uygulama ici, WhatsApp, SMS",
            "Gunluk ozet + aylik trend grafigi",
            "Veli yorum ve aciklama iste butonu",
            "Ses ve fotograf ekleme (opsiyonel)",
        ],
        "sekmeler": [
            ("Bugunun Ozeti", "Bugun ogluna/kizina ait AI tarafindan hazirlanmis 6 bolumlu kapsul.",
                ["Kapsulu oku", "Ses ile dinle", "Yorum ekle / aciklama iste"]),
            ("Gecmis Kapsuller", "Son 30/60/90 gun tum kapsuller.",
                ["Tarih sec", "Kapsulu goruntule"]),
            ("Aylik Ozet", "Akademik + sosyal-duygusal trend + hafta hafta grafikler.",
                ["Ay sec", "Trend grafigi", "PDF indir"]),
            ("Bildirim Ayarlari", "Kanal sec (WhatsApp/SMS/Uygulama), zaman, dil.",
                ["Kanal aktif et", "Saat ayarla (16:00-19:00 arasi)"]),
        ],
        "is_akisi": [
            "Ogretmen gun icinde ilgili moduller uzerinden veri girer (not, yoklama, etkinlik, mood).",
            "17:30: Sistem tum verileri toplar.",
            "18:00: AI kapsul uretir ve veliye secilen kanaldan gonderilir.",
            "Veli kapsulu acar, icindekileri okur.",
            "Veli yorum yazar veya 'Aciklama iste' ile ogretmene soru sorar.",
        ],
        "ipuclari": [
            "Ogretmenin kisisel bir not eklemesi kapsulu duygusal baga donusturur — her hafta en az 1 ekle.",
            "WhatsApp kanali en yuksek acilim oranina sahip — SMS'e tercih et.",
            "Aylik Ozet'te trend grafigini veli toplantisinda gosterebilirsin.",
        ],
        "sss": [
            ("Kapsul gelmedi?", "Bildirim ayarlarini kontrol et. Ya da WhatsApp Business API key suresi bitmis olabilir."),
            ("AI yanlis ozet cikarmis?", "'Duzelt' butonuna bas, yeniden olusturma tetikleyebilirsin. AI zaman icinde ogrenir."),
        ],
    },
]

# Not: 40 modulden 11 tanesini icerdik (GENEL 2 + KURUM 9). Devami alt bolumde.
# Butunluk icin asagida AKADEMIK (17), OPERASYON (4), SISTEM (1) modulleri devam eder.

MODULLER.extend([
    # ──────────────────── AKADEMIK (17) ────────────────────
    {
        "section_no": 12, "grup": "AKADEMIK", "ad": "Ogrenci 360", "icon": "📊",
        "accent": ROSE, "yeni": False,
        "amac": (
            "Ogrenci 360, bir ogrencinin A'dan Z'ye tum verilerini tek ekranda toplar. 12 farkli modulden "
            "43+ veri kaynagi otomatik birlestirilir (notlar, yoklama, sinav, rehberlik, saglik, "
            "kocluk, kutuphane, yabanci dil, sosyal etkinlik, gamification, servis). AI 360° mega raporla "
            "guclu/zayif yonler tespiti ve resmi belge formati uretir."
        ),
        "kim": [
            ("Rehber Ogretmen", "Gorusme oncesi ogrencinin tam profiline bakar."),
            ("Sinif Ogretmeni/Danismani", "Veli toplantisinda kapsamli profil sunmak icin kullanir."),
            ("Mudur/Mudur Yardimcisi", "Riskli ogrenciler icin detayli inceleme."),
            ("Veli (yetkili)", "Cocugunun tum akademik/sosyal-duygusal resmine bakar."),
        ],
        "ana_ozellikler": [
            "43+ veri kaynagi 12 modulden otomatik",
            "20 gorsel seksiyon (akademik, devamsizlik, YD, odev, saglik, kocluk vs)",
            "AI 360° mega rapor (guclu/zayif/oneri)",
            "Trend analizi (yil bazli + donum noktalari)",
            "Veli ve ogretmen gorunumleri ayri",
            "PDF export (resmi format)",
        ],
        "sekmeler": [
            ("Genel Bakis", "Ogrencinin 1 sayfalik dashboard'i: 20 seksiyonun ozet kartlari.",
                ["Ogrenci ara ve sec", "Kart uzerine tikla detay seksiyonuna git"]),
            ("Akademik Performans", "Notlar, sinav sonuclari, ders bazli ortalamalar, trend.",
                ["Donem sec", "Ders sec", "Trend grafigini incele"]),
            ("Devamsizlik & Yoklama", "Gunluk/aylik devamsizlik, geç kalma, izin dagilimi.",
                ["Tarih araligi", "Sebep analizini gor"]),
            ("Yabanci Dil (CEFR)", "Seviye (Pre-A1-B2) + speaking + reading + writing kirmisi.",
                ["Beceri sec", "Deneme sinavlarinda ilerleme"]),
            ("Rehberlik Gecmisi", "Tum gorusme notlari, vaka kayitlari, test sonuclari.",
                ["Gorusme sec detay", "Gizlilik kontrollu — sadece yetkilliler"]),
            ("Saglik Kayitlari", "Revir ziyaretleri, ilac, kaza, alerji, surekli rahatsizlik.",
                ["Tarih filtresi", "Kategori sec"]),
            ("Kocluk Gecmisi", "Koc gorusmeleri, SMART hedefler, motivasyon skoru.",
                ["Koc sec", "Hedef listesi", "Motivasyon egrisi"]),
            ("Sosyal Etkinlik & Kulup", "Uye oldugu kulupler, katildiği etkinlikler, rozet.",
                ["Kulup sec", "Etkinlik listesi"]),
            ("Kutuphane & Servis", "Odunc kitap gecmisi, gecikmeler, servis kaydi.",
                []),
            ("AI 360° Mega Rapor", "Tum seksiyonlari tarayip AI ile guclu/zayif yon + 5 oneri.",
                ["Rapor olustur", "PDF indir"]),
            ("Trend Analizi", "Yil bazli karsilastirma + donum noktasi tespiti.",
                ["Yil sec", "Donum noktasi bolgesine bak"]),
        ],
        "is_akisi": [
            "Ogrenci ara ve sec (isim/no).",
            "Genel Bakis'ta 20 seksiyonun dashboard'ina bak; dikkat cekici kirmizi bolge varsa tikla.",
            "Rehberlik Gecmisi ve Saglik Kayitlari'ni kronolojik incele.",
            "AI 360° Mega Rapor'u calistir; cikan oneriler + guclu/zayif yonlere bak.",
            "Trend Analizi ile donum noktalari kontrol et — akademik dusus bir olaya denk gelmis olabilir.",
            "Rapor PDF olarak indir; veli toplantisinda kullan veya arsivle.",
        ],
        "ipuclari": [
            "Veli toplantisi ONCESI Ogrenci 360'i mutlaka ac — 'onceki veli toplantisindaki gibi daglinik olmayacak'.",
            "AI mega rapor her seferinde guncel veri uzerinden uretilir — eski rapor cachelenmez.",
            "Rehberlik gecmisi sadece yetkili kullaniciya gorunur — veli icin bu sekme otomatik gizlenir.",
            "★ ERKEN UYARI BUTUNCUL RISK SKORLARI BURADA DA GORUNUR: Ogrenci secildiginde 20 boyutlu radar (akademik sol + davranissal sag) otomatik gelir. Yetkili role gore hassas boyutlar maskelenir.",
            "★ Bu modul PASIF — veri URETMEZ sadece okur ve birlestirir. Profilde gorunen her veri baska bir moduldeki form aracılıgıyla girilmistir. Eksik gorunen alan ilgili moduldaki form girisinin yapilmadigi anlamina gelir.",
        ],
        "sss": [
            ("Bazi bolumler bos?", "Ilgili modul o ogrenci icin veri tutmamis olabilir (ornek: sporcu degilse Kocluk bos)."),
            ("Mega rapor cok uzun surdu?", "12 modulden veri cekiyor — normal cevrimde 15-30 saniye. Bekle."),
            ("Butuncul Risk skorunu nereden okur?",
             "Erken Uyari Sistemi > Butuncul Risk 20-Boyut > Toplu Hesaplama ile uretilen 'risk_records.json' dosyasindan. Hesaplama yapilmamisssa profilde skor gorunmez."),
        ],
    },
    {
        "section_no": 13, "grup": "AKADEMIK", "ad": "Okul Oncesi - Ilkokul", "icon": "🎨",
        "accent": PINK, "yeni": False,
        "amac": (
            "Okul Oncesi - Ilkokul modulu, anasinifi (4-5 yas + hazirlik) ve ilkokul (1-4) kademeleri "
            "icin ozellestirilmis arac kitidir. Gunluk bulten, gelisim takibi (milestone), haftalik "
            "veli raporu, erken uyari, portfolyo (gelisim dosyasi), davranis DNA analizi ve ebeveyn "
            "okulu gibi 15+ sekme ile erken cocukluk egitiminin butunsel yonetimini saglar."
        ),
        "kim": [
            ("Okul Oncesi Ogretmeni", "Gunluk bulten, gelisim takibi, veli raporlari."),
            ("Ilkokul Ogretmeni", "Hizli erisim paneli, davranis DNA, sinif asistani."),
            ("Veli", "Haftalik rapor + gelisim dosyasi + mutluluk indeksine bakar."),
        ],
        "ana_ozellikler": [
            "Okul oncesi gunluk bulten ve takvim",
            "Gelisim milestone takibi (motor, dil, sosyal, bilissel)",
            "Haftalik otomatik veli raporu (fotograf + etkinlik + gelisim notu)",
            "Davranis DNA — davranis paternleri analizi",
            "Erken uyari — gelisim geriligi tespiti",
            "Portfolyo (gelisim dosyasi) — yildan yila arsivlenen",
            "Ebeveyn okulu — veliye yonelik egitim iceriklleri",
            "Mutluluk Indeksi — gunluk duygu takibi",
            "Sinif Karmasi — heterojen grup olusturma araci",
        ],
        "sekmeler": [
            ("Okul Oncesi Panel", "4-5 yas + hazirlik sinifi gunluk bulten, duyuru, takvim.",
                ["Sinif sec", "Bulten olustur (fotograf + yazi)", "Veliye yayinla"]),
            ("Ilkokul Panel", "1-4 sinif icin hizli erisim (yoklama, not, etkinlik).",
                []),
            ("Gelisim Takip", "Motor/Dil/Sosyal/Bilissel alanlarda milestone takibi.",
                ["Ogrenci sec", "Milestone isaretle (var/yok/gelisiyor)", "Uyari al"]),
            ("Haftalik Rapor", "Haftanin sonu veliye gonderilen otomatik rapor.",
                ["Haftayi sec", "Fotograf ve etkinlikleri ekle", "AI ozet uret", "Gonder"]),
            ("Erken Uyari", "Gelisim geriligi, davranis sorunlari tespiti.",
                ["Ogrenci sec", "Uyari seviyesi (dusuk/orta/yuksek)"]),
            ("Portfolyo (Gelisim Dosyasi)", "Yillari arsivlenen gelisim dosyasi (resim, yazim, video).",
                ["Icerik ekle (resim/video)", "Kategori: sanat/dil/matematik vs"]),
            ("Aktivite Planlama", "Gunluk/haftalik etkinlik plani (oyun, bilim, sanat).",
                ["Haftayi sec", "Gun gun etkinlik olustur"]),
            ("Veli-Ogretmen Koprusu", "Iki yonlu hizli mesajlasma + onemli paylasimlar.",
                ["Veli sec", "Mesaj yaz", "Fotograf ekle"]),
            ("Davranis DNA", "AI cocugun davranis paternlerini analiz eder + oneri.",
                ["Ogrenci sec", "Gun bazli davranis", "AI pattern + oneri"]),
            ("Sinif Asistani", "Ogretmenin gunluk is akisini kolaylastiran AI assistant.",
                []),
            ("Ebeveyn Okulu", "Veliye yonelik egitim iceriklleri (uyku, beslenme, oyun).",
                ["Konu sec", "Veliye link gonder"]),
            ("Sinif Karmasi", "Heterojen grup olusturma: cesitlilik icin AI eslesme.",
                ["Kriter sec", "AI gruplama onerisi"]),
            ("Mutluluk Indeksi", "Gunluk duygu check-in (emoji bazli).",
                ["Gunluk cocuklara sor", "Sinif ortalamasina bak"]),
            ("Hazirlik Egitimi", "Ilkokula hazirlik modulu (5-6 yas).",
                []),
            ("Smarti (Egitmen)", "Erken cocukluk ozel AI asistani.",
                ["Soru yaz", "Cevap al"]),
        ],
        "is_akisi": [
            "Sabah: Gunluk bulten olustur (foto + aktivite), veliye gonder.",
            "Haftalik: Gelisim Takibi'nde her cocuk icin milestone guncelle.",
            "Cuma aksam: Haftalik Rapor otomatik uretildigini kontrol et, kisisel not ekle, gonder.",
            "Ayda 2 kez: Mutluluk Indeksi gun bazli analiz.",
            "Ayda 1 kez: Portfolyo'ya yeni icerik (resim, ses kaydi, fotograf) ekle.",
            "Ihtiyac durumunda: Davranis DNA ile pattern incele — sorun varsa rehberliğe yonlendir.",
        ],
        "ipuclari": [
            "Haftalik rapordaki 'ozel an' bolumu veliye en cok duygusal baglanti saglayan kisimdir — ihmal etme.",
            "Portfolyo yildan yila aktarilir — ilkokul mezuniyetinde veliye PDF olarak verebilirsin.",
            "Davranis DNA'nin 30 gunluk pattern icin minimum veri gerekir — hemen yorumda bulunma.",
        ],
        "sss": [
            ("Haftalik rapor gonderilmedi?", "Email/WhatsApp ayarlarindan provider'in aktifligini kontrol et."),
            ("Portfolyo fotograf yuklenmiyor?", "Dosya boyutu 5 MB'i geciyor olabilir. 2048x2048'e ufalt."),
        ],
    },
    {
        "section_no": 14, "grup": "AKADEMIK", "ad": "Akademik Takip", "icon": "📚",
        "accent": EMERALD, "yeni": False,
        "amac": (
            "Akademik Takip, okulun akademik omurgasidir. 14+ sekme ile ogrenci/ogretmen yonetimi, "
            "ders programi, yoklama, not girisi, odev, kazanim takibi, ders defteri, nobet, izin, "
            "online ders, sertifika ve ayrica v2.0 ile gelen Ogrenci Kimlik (Dijital Pasaport + Basari "
            "Duvari + Karsilastirmali Ilerleme) ve Akilli Yoklama ozelliklerini icerir."
        ),
        "kim": [
            ("Sinif Ogretmeni", "Yoklama, not, ders defteri, kazanim takibi."),
            ("Brans Ogretmeni", "Kendi ders programi + not girisi + odev."),
            ("Mudur Yardimcisi", "Ogrenci/ogretmen yonetimi + programlar + raporlar."),
        ],
        "ana_ozellikler": [
            "14+ ana sekme",
            "Ogrenci ve ogretmen CRUD",
            "Haftalik ders programi (surukle-birak)",
            "Gunluk yoklama (Akilli Yoklama ★ ile 5 yontem)",
            "Not girisi (yazili/sozlu/proje)",
            "Odev atama ve takip",
            "Kazanim takibi (islendi/islenmedi/kismen)",
            "Ders defteri + online ders entegrasyonu",
            "Nobet ve izin yonetimi",
            "Sertifika talebi ve arsiv",
            "Ogrenci Kimlik ★: Dijital Pasaport + Basari Duvari + Karsilastirmali Karne",
        ],
        "sekmeler": [
            ("Dashboard", "Akademik ozet: ogrenci sayisi, bu hafta sinav, devamsizlik yuzde.",
                []),
            ("Ogrenci Yonetimi", "Tum ogrenciler CRUD + Excel import + ozluk bilgisi.",
                ["'+ Ogrenci' ile ekle", "Excel import", "Duzenle/Sil"]),
            ("Ogretmen Yonetimi", "Ogretmen CRUD + brans + haftalik yuk.",
                []),
            ("Ders Programi", "Haftalik program (surukle-birak) + catisma kontrolu.",
                ["Gun + saat sec", "Ogretmen+sinif+ders sec", "Catisma uyarisi kontrol"]),
            ("Yoklama & Devamsizlik", "Gunluk yoklama + Akilli Yoklama ★ (5 yontem).",
                ["Sinif sec", "Yontem sec: hizli/tek tek/QR/yuz/sesli", "Kaydet"]),
            ("Not Girisi", "Yazili/sozlu/proje notlari + kazanim eslestirme.",
                ["Ders + sinav sec", "Ogrencilere not gir", "Kaydet"]),
            ("Odev Yonetimi", "Odev atama + teslim tarihi + online teslim + puanlama.",
                ["Odev olustur (dosya/link/video)", "Sinif sec", "Son teslim tarihi", "Yayinla"]),
            ("Kazanim Takibi", "MEB kazanimlari islendi/islenmedi/kismen isaretleme.",
                ["Ders + unite sec", "Kazanim tek tek isaretle", "Yillik plan ile esitlenir"]),
            ("Ders Defteri", "Gunluk ders islenen konu + ozel not + online ders linki.",
                ["Gun + ders sec", "Islenen konu yaz", "Ozel not + online link"]),
            ("Nobet Yonetimi", "Haftalik nobet programi + degisim talebi.",
                ["Nobetci ata", "Degisim talebi al"]),
            ("Izin Islemleri", "Ogretmen izin talep + onay akisi.",
                []),
            ("Online Ders", "Zoom/Meet/Teams entegrasyonu + katilim takibi.",
                ["Ders ekle + link", "Katilimci sayisi otomatik"]),
            ("Sertifika", "Ogrenci sertifika talebi + imza + QR dogrulama.",
                ["Tur sec (basari/katilim)", "Ogrenciler sec", "Olustur PDF"]),
            ("Ogrenci Kimlik ★", "3 alt-sekme: Dijital Pasaport / Basari Duvari / Karsilastirmali Ilerleme.",
                ["Ogrenci sec", "Sekmeyi gez", "PDF export"]),
            ("Raporlar", "Sinif/ogrenci/ogretmen bazli + devamsizlik + akademik trend.",
                ["Sablon sec", "Filtre uygula", "PDF/Excel indir"]),
        ],
        "is_akisi": [
            "Yil basi: Ogrenci ve Ogretmen yonetiminde listeleri olustur veya import et.",
            "Eylul: Ders Programi'ni haftalik gorunumde olustur.",
            "Her gun: Yoklama al (Akilli Yoklama ile hizli), Ders Defteri'ne isledigin konuyu yaz.",
            "Haftalik: Odev ver/teslim al.",
            "Donem icinde: Not Girisi ile sinav notlarini + kazanim takibini yap.",
            "Ayda 1 kez: Ogrenci Kimlik ile ogrenci profilleri gun.",
            "Yil sonu: Sertifika talebi ve rapor cikisi.",
        ],
        "ipuclari": [
            "Akilli Yoklama'da QR yontemi ogrenciler cep telefonuyla saniyeler icinde yoklama yapiyor.",
            "Kazanim Takibi'ni her ders sonunda doldur — haftalik birikmis yazim 2 kat daha zor.",
            "Ogrenci Kimlik'teki Dijital Pasaport velilerle en hizli etkilesimli iletisim araci.",
            "★ BU MODUL ERKEN UYARI SISTEMI'NIN 2 DAVRANISSAL BOYUTUNU BESLER:",
            "◆ YOKLAMA (ATTENDANCE.JSON): Her gun sistematik yoklama tutmak Butuncul Risk motoru'nun 'kronik_devamsizlik' boyutunu hesaplar. Motor son 60 gun ozursuz devamsizlik oranina bakar + SECICI DERS KACMA paternini analiz eder (belirli bir dersten tekrarli kacma -> kirmizi bayrak). %10 ustu = YUKSEK, %20 ustu = KRITIK.",
            "◆ MUDAHALE KAYITLARI: 'mudahale_turu' + tarih + aciklama alanlari 'disiplin_sikligi' boyutunu besler. Son 90 gunde 3+ mudahale -> KRITIK. Rehberlige yonlendirme, uyari, aile gorusmesi gibi turler dogru kaydedilmeli.",
            "• Tam dogruluk icin yoklamayi gun sonunda degil DERS-DERS gir (sekme bazli analiz icin).",
        ],
        "sss": [
            ("Ogrenci Excel import basarisiz?", "Sablon dosyayi indir (TC, ad, soyad, sinif, sube kolonlari zorunlu)."),
            ("Akilli Yoklama yuz tanima calismiyor?", "Kamera izni verilmis mi? Isik yeterli mi?"),
            ("Yoklama girmedigim gun Butuncul Risk motorunu etkiler mi?",
             "Evet — eksik yoklama 'bilmiyorum' olarak kalir, motor veri eksikligi halinde dusuk guven (confidence 40-70) ile calisir. Her gun tutmak dogru skor icin sart."),
            ("Disiplin kaydi nasil tutulur?",
             "Akademik Takip > ilgili alt sekmeden 'Yeni Mudahale' ile tarih + tur (bireysel_gorusme / yazili_uyari / aile_gorusmesi / yonlendirme) + aciklama gir."),
        ],
    },
    {
        "section_no": 15, "grup": "AKADEMIK", "ad": "Akademik Takvim", "icon": "📅",
        "accent": AMBER, "yeni": True,
        "amac": (
            "Akademik Takvim (v2.0 ★) MEB egitim takvimi, sinav programi, kulup etkinlikleri, veli "
            "toplantilari ve ozel gunleri tek takvim arayuzunde toplar. 365 gun gorunumu, ICS export "
            "ile Google/Apple/Outlook senkronu, otomatik hatirlatma ve donemsel karsilastirma sunar."
        ),
        "kim": [
            ("Mudur Yardimcisi (Akademik)", "Yillik takvimi olusturur, sinavlari planlar."),
            ("Kulup Sorumlusu", "Kulup etkinliklerini takvime ekler."),
            ("Ogretmen/Veli/Ogrenci", "Takvimi gorur, ICS ile kisisel takvimine senkron eder."),
        ],
        "ana_ozellikler": [
            "Yillik akademik takvim (MEB uyumlu)",
            "Tatil, ozel gun, resmi tatil otomatik",
            "Sinav programi (yazili + deneme + TYT/AYT/LGS)",
            "Kulup etkinlikleri + veli toplantilari",
            "Filtreleme (sinif/sube/ders/ogretmen)",
            "ICS export (Google/Apple/Outlook)",
            "Otomatik hatirlatma (1 gun once / 1 saat once)",
            "Donemsel karsilastirma (geçen donemle)",
        ],
        "sekmeler": [
            ("Dashboard", "Bugun + bu hafta ozet, yaklasilan etkinlik.",
                []),
            ("Takvim Goruntus", "Ay/hafta/gun gorunumleri — renkli kategori.",
                ["Goruntu sec (ay/hafta/gun)", "Etkinlik uzerine tikla"]),
            ("Liste Goruntus", "Kronolojik liste — arama ve filtreleme destekli.",
                ["Tarih araligi", "Kategori filtresi"]),
            ("Etkinlik Ekle", "Yeni etkinlik olustur: kategori/tarih/katilimci/aciklama.",
                ["Kategori sec (Sinav/Toplanti/Tatil vs)", "Tarih+saat", "Hedef kitle sec"]),
            ("Donem Yonetimi", "Yillari donem donem tanimla (1. Donem, Ara Tatil, 2. Donem).",
                ["Donem ekle", "Tarih araligi", "MEB takvimle ayarla"]),
            ("Tatil Planla", "Resmi + ozel tatilleri tanimla.",
                []),
            ("Sinav Tarihleri", "Yazili/deneme/MEB sinavlari + hazirlik programi.",
                ["Sinav tipi sec", "Tarih + sinif + ders", "Hatirlatma ayarla"]),
            ("MEB Sinavlari", "LGS/TYT/AYT/YDT resmi sinavlar — MEB tarihinden otomatik.",
                []),
            ("Durum Karsilastirmasi", "Bu donem vs geçen donem etkinlik yogunlugu.",
                ["Donem sec", "Kategori sec"]),
            ("Raporlar", "Etkinlik yogunlugu, kategori dagilimi.",
                []),
            ("Paylas (QR/Link)", "Takvimi veliye QR veya link ile paylas + ICS indirme.",
                ["Link/QR olustur", "ICS export indir"]),
        ],
        "is_akisi": [
            "Agustos: Donem Yonetimi'nde yeni yil donem yapisini olustur.",
            "Eylul: Tatil Planla'da resmi + ozel tatilleri gir.",
            "Ekim: Sinav Tarihleri'nde tum yil yazili/deneme sinavlarini belirle.",
            "Yil boyu: Etkinlik Ekle'de kulup/toplanti/gezi ekle.",
            "Haftalik: Dashboard'da yaklasilanleri gozden gecir.",
            "Donem sonu: Durum Karsilastirmasi ile geçen donem kiyas.",
        ],
        "ipuclari": [
            "ICS export linkini tum velilere gonder — herkes takvimine ekler, hatirlatma otomatik.",
            "Sinav tarihini 2 hafta onceden girmek ogretmen hazirligi icin cok etkili.",
            "Kategorilere renk atamak gorsel okunurlugu cok arttirir.",
        ],
        "sss": [
            ("Google Calendar'a senkron olmadi?", "ICS linkini tekrar indir, Google Calendar 'Takvim ekle > URL' ile link yapistir."),
            ("Etkinlik catisma uyarisi gelmedi?", "Ayarlar > Bildirimler'de 'Cakisma Kontrolu' aktif olmali."),
        ],
    },
    {
        "section_no": 16, "grup": "AKADEMIK", "ad": "Olcme ve Degerlendirme", "icon": "📝",
        "accent": PURPLE, "yeni": False,
        "amac": (
            "Olcme ve Degerlendirme modulu, kazanim bankasi, soru havuzu (7 soru tipi), blueprint "
            "tabanli sinav uretme, AI ile soru uretimi, IRT/CAT psikometrik analiz, QR ile ogrenci "
            "girisi, proctoring, MEB/OSYM sinav motoru (LGS/TYT/AYT) ve otomatik puanlama ile "
            "uluslararasi duzey olcme-degerlendirme platformudur."
        ),
        "kim": [
            ("Ogretmen", "Soru bankasi, sinav olusturma, ogrenci sinavi."),
            ("Zumre Baskani", "Ortak sinavlar, kazanim takibi, blueprint."),
            ("Egitim Koordinatoru", "IRT analiz, soru kalite, benchmark."),
        ],
        "ana_ozellikler": [
            "Kazanim bankasi (MEB + ozel)",
            "7 soru tipi: MCQ, D/Y, bosluk, eslestirme, siralama, cloze, matematik ifadesi",
            "Blueprint (sinav sablonu) ile otomatik sinav uretimi",
            "AI ile soru uretimi (OpenAI GPT-4o-mini)",
            "IRT psikometrik analiz (1-PL/2-PL/3-PL)",
            "CAT (Computerized Adaptive Testing)",
            "MEB/OSYM sinav motoru (LGS/TYT/AYT/YDT)",
            "OSYM tarzi PDF (cift sutun, profesyonel kapak, optik form)",
            "QR ile ogrenci girisi + proctoring (browser lockdown, webcam)",
            "Telafi sistemi (renk bandi: red/yellow/green/blue)",
            "Stok kontrol + otomatik soru doldurma",
            "QTI 2.1 import/export (Moodle/Canvas uyumlu)",
            "LTI 1.3 entegrasyon",
        ],
        "sekmeler": [
            ("Dashboard", "Soru bankasi sayisi, bu hafta yazili, ortalama zorluk.",
                []),
            ("Kazanim Yonetimi", "MEB kazanimlari import + ozel kazanim ekleme.",
                ["Sinif+ders+unite sec", "Import (6839 MEB kazanim hazir)"]),
            ("Soru Bankasi", "7 soru tipi + zorluk + bloom + rubrik + celdirici analizi.",
                ["Kategori sec (Kazanim/Disardan)", "Soru olustur veya AI ile uret"]),
            ("AI Soru Uretimi", "5 adimli wizard: kazanim/sinif/ders/soru sayisi/zorluk/tip.",
                ["Wizard'a gir", "Parametreleri sec", "AI uret", "Incele/duzenle", "Bankaya ekle"]),
            ("Blueprint", "Sinav sablonu: kac soru, hangi kazanim, zorluk dagilimi.",
                ["Blueprint olustur", "Sinav ureticisine baglama"]),
            ("Sinav Olustur", "Blueprint + soru havuzundan otomatik sinav uretimi.",
                ["Blueprint sec", "Sinav adi + sure + negatif puan", "Uret", "PDF/Online"]),
            ("MEB Sinav Motoru", "LGS/TYT/AYT/YDT ozel bolum yapisi ve puanlama.",
                ["Sinav turu sec", "Blueprint", "OSYM tarzi PDF uret"]),
            ("Online Sinav & QR", "Ogrenci QR ile giris, browser lockdown, otomatik puanlama.",
                ["Sinav sec", "QR kod yazdir", "Oturumu baslatin"]),
            ("Proctoring", "Webcam + tab kontrol + heartbeat + risk skoru.",
                []),
            ("Otomatik Puanlama", "Sinav sonuclari + negatif puanlama + IRT/CAT analiz.",
                []),
            ("Telafi Sistemi", "Red(0-49): hemen quiz+48h quiz; Yellow: pekistirme; Green: haftalik tekrar; Blue: zor set.",
                []),
            ("IRT Psikometrik", "1-PL Rasch / 2-PL / 3-PL parametreler + Fisher info.",
                ["Sinav sec", "Model sec", "Parametre tahminle"]),
            ("CAT Adaptif Test", "Fisher bilgi + MLE + SE ile adaptif.",
                []),
            ("Stok Kontrol", "Soru stogu rapor + otomatik AI ile doldurma.",
                []),
            ("Rubric Yonetimi", "Kriter + seviye tabanli rubrik olusturma (acik ucu sorular icin).",
                []),
            ("QTI Import/Export", "Moodle/Canvas/Blackboard uyumlu XML.",
                []),
            ("Raporlar", "Sinav sonuclari, siralama, zorluk analizi, benchmark.",
                []),
        ],
        "is_akisi": [
            "Ilk kurulumda: Kazanim Yonetimi'nden MEB kazanimlarini import et.",
            "Soru Bankasi'na soru ekle (elle veya AI ile).",
            "Blueprint olustur: sinavin yapisini tanimla (zorluk + kazanim dagilimi).",
            "Sinav Olustur: blueprint'ten otomatik sinav uret.",
            "Online/PDF yolu sec: QR ile online veya OSYM tarzi PDF.",
            "Ogrenciler sinavi cozer, Otomatik Puanlama yapilir.",
            "IRT ile soru kalitesini analiz et, zayif soruyu bankaya geri cikar.",
            "Telafi sistemi otomatik devreye girer (renk bandi).",
        ],
        "ipuclari": [
            "AI ile soru uretirken 'kazanim + zorluk + Bloom' uclusunu dogru sec — iyi kalite soru bir denemede cikar.",
            "Blueprint'te zorluk dagilimi (%20 kolay / %60 orta / %20 zor) klasik ama etkili.",
            "OSYM tarzi PDF profesyonel gorunum saglar, veliyi etkiler.",
        ],
        "sss": [
            ("AI soru uretimi basarisiz?", "OpenAI API key ayarlanmis mi (Ayarlar > Integrations)? Kota bitmis olabilir."),
            ("QR ile ogrenci giremiyor?", "Ogrenci TC no sistemde kayitli mi? Browser eski surum olabilir."),
        ],
    },
    {
        "section_no": 17, "grup": "AKADEMIK", "ad": "Rehberlik", "icon": "🧠",
        "accent": ROSE, "yeni": False,
        "amac": (
            "Rehberlik modulu, psikolojik danismanlik ve rehberlik hizmetlerinin tam kapsamli "
            "yonetimidir. 41 sekme ile gorusme kaydi, vaka takibi, aile gorusmesi, yonlendirme, BEP "
            "(Bireysellestirilmis Egitim Programi), 36 MEB formu, 20+ psikolojik test, risk "
            "degerlendirmesi, Mood Check-in ★ ve Ihbar Hatti ★ entegrasyonu icerir."
        ),
        "kim": [
            ("Rehber Ogretmen/Psikolojik Danisman", "Tum sekmelerin ana kullanicisi."),
            ("Okul Muduru", "Ozet raporlar ve vaka istatistikleri."),
            ("Sinif Ogretmeni/Danismani", "Kendi sinifindaki ogrenci rehberlik durumuna bakar."),
        ],
        "ana_ozellikler": [
            "41 sekme (en genis modul)",
            "Gorusme kaydi (bireysel/grup)",
            "Vaka takibi (acik/devam eden/cozulmus)",
            "Aile gorusmesi + veli kaydi",
            "Yonlendirme islemleri (RAM, hastane, uzman)",
            "BEP (Bireysellestirilmis Egitim Programi) kaydi",
            "36 MEB formu (e-Rehberlik uyumlu)",
            "20+ psikolojik test (IQ, kisilik, ilgi vs)",
            "Risk degerlendirme matrisleri",
            "Ihbar Hatti ★ (anonim, 8 kategori)",
            "Mood Check-in ★ rehber paneli",
            "Kriz mudahale planlari",
        ],
        "sekmeler": [
            ("Dashboard", "Acik vaka, bu hafta gorusme, risk dagilimi.", []),
            ("Gorusme Kaydi", "Bireysel/grup gorusme notlari + ses kaydi + PDF.",
                ["Ogrenci sec", "Gorusme turu", "Not yaz / ses kaydet", "Kaydet"]),
            ("Vaka Takibi", "Vaka CRUD + durum (acik/devam/cozuldu).", []),
            ("Aile Gorusmeleri", "Veli ile yapilan gorusmeler + aile dinamigi.", []),
            ("Yonlendirme Islemleri", "RAM / hastane / ozel uzmana yonlendirme.", []),
            ("BEP", "Bireysellestirilmis Egitim Programi olusturma + takip.", []),
            ("Psikolojik Testler", "20+ test: IQ, kisilik, ilgi, yetenek vs.",
                ["Test sec", "Ogrenci sec", "Uygula", "Puanla", "Yorumla"]),
            ("Test Degerlendirme", "Testlerin puanlamasi ve yorumlanmasi.", []),
            ("Risk Degerlendirmesi", "Intihar/madde/zorbalik/istismar risk matrisleri.", []),
            ("Rehberlik Plani", "Yillik/donemlik rehberlik calisma plani.", []),
            ("Ihbar Hatti ★", "Anonim ihbar — 8 kategori (zorbalik, intihar, madde, taciz vs).",
                ["Ihbar incele", "Kategori sec", "Aksiyon al"]),
            ("Mood Check-in Rehber Paneli ★", "Tum ogrencilerin gunluk mood verileri + trend.",
                ["Ogrenci/sinif sec", "Son 30 gun mood", "Riskli goruntu"]),
            ("Kriz Mudahale", "Kriz durumlari (olum, travma) acil plani.", []),
            ("MEB Formlari (36)", "e-Rehberlik uyumlu 36 form.",
                ["Form sec", "Ogrenci sec", "Doldur", "PDF ciktisi"]),
            ("Raporlar", "Vaka/test/risk bazli raporlar.", []),
        ],
        "is_akisi": [
            "Ogretmen ogrenciyi rehberlige yonlendirir (referral).",
            "Rehber ogrenci ile Gorusme Kaydi yapar (not + ses).",
            "Ihtiyac halinde Psikolojik Test uygular, Vaka aclir.",
            "Vaka karmasikligina gore BEP olusturur veya disa Yonlendirme yapar.",
            "Aile Gorusmesi yapar, Mood Check-in panelinden takip eder.",
            "Risk varsa Risk Degerlendirme ve Kriz Mudahale'yi baslatir.",
            "Vaka cozulmus: Durumu 'cozuldu' olarak isaretler, izleme suresi baslar.",
        ],
        "ipuclari": [
            "Gorusme kaydinda ses kaydi cok yardimci ama KVKK onayi sart — veli/ogrenci imzali sablon kullan.",
            "Mood Check-in panelinde 7+ gun usust agir duygular varsa 1:1 gorusme planla.",
            "Ihbar Hatti'ni her donem basinda tum ogrencilere tanit — varligini bilmedikleri kanal kullanilmaz.",
            "★ BU MODUL ERKEN UYARI SISTEMI'NIN 5 DAVRANISSAL BOYUTUNU BESLER:",
            "◆ VAKA TAKIBI: 'Konu' alanini DOGRU sec — motor bu alana bakarak riski siniflar. Akran Zorbaligi / Aile Sorunlari / Sinav Kaygisi / Motivasyon Dusuklugu / Sosyal Uyum / Okula Devamsizlik / Ders Basarisizligi / Dikkat Eksikligi dogru konulardir. Konu yanlissa motor farkli boyuta sinyal verir.",
            "◆ GORUSME KAYDI: Notlara yazilan kelimeler Butuncul Risk motoruna keyword-sinyal olur. 'Zorbalik', 'siddet', 'intihar', 'kendine zarar', 'madde', 'sigara', 'alkol', 'umutsuz', 'ailede kavga' kelimelerini NET olarak kullan — dolayli ifadeler yakalanmaz.",
            "◆ AILE BILGI FORMU: 'aile_durumu' (birlikte/ayri/vefat) + 'ozel_durum' serbest metin. Ozel durumda 'siddet', 'istismar', 'ihmal', 'ekonomik kriz', 'ebeveyn kaybi', 'bosanma' anahtar kelimelerini acik yaz — aile_risk boyutu dogru skorlanir.",
            "◆ RISK DEGERLENDIRME: Intihar / Kendine Zarar risk degerlendirmesi acinca motor 'kendine_zarar_intihar' boyutunda 60+ skor uretir, otomatik Acil 24h Protokolu tetiklenir (yetkili mudur+psikolog'e).",
            "◆ IHBAR INCELEME: Gelen ihbarlar Bu sekmeden islenir. Motor ihbar kategorilerini (zorbalik, intihar, madde, aile ici siddet) okul-geneli trend olarak raporlar.",
        ],
        "sss": [
            ("Psikolojik test sonucu abartili mi?", "Test 'degerlendirme' sekmesinde uzmanin yorumu esastir; ham puan tek basina yetmez."),
            ("Ihbar anonim mi gerçekten?", "Evet — IP/kullanici bilgisi sadece hukuki zorunluluk halinde acilir."),
            ("Vaka acinca Erken Uyari anlik guncellenir mi?",
             "Hayir. Motor Batch calisir — EU > Butuncul Risk 20-Boyut > Toplu Hesaplama sekmesinden tetiklenir. Gunluk otomatik tetiklenmesini planlamak mumkun (scheduler)."),
            ("Gorusme notuna yazdigim kelime motoru etkiler mi?",
             "EVET. Motor keyword tarama yapar: 'zorbalik', 'intihar', 'madde' vb. kelimeler ilgili davranis boyutunu tetikler. Hassas konular icin NET dil kullan."),
        ],
    },
    {
        "section_no": 18, "grup": "AKADEMIK", "ad": "Okul Sagligi Takip", "icon": "🏥",
        "accent": CORAL, "yeni": False,
        "amac": (
            "Okul Sagligi Takip modulu, okul revirinin tam kapsamli yonetimidir. Ogrenci saglik karti, "
            "revir ziyaret kaydi, ilac uygulama takibi, kaza/olay kaydi, saglik envanteri, ilk yardim "
            "dolaplari, seminer ve egitim programlari ile KVKK uyumlu erisim logu icerir."
        ),
        "kim": [
            ("Okul Hemsiresi/Sagilk Gorevlisi", "Gunluk revir islemleri, ilac, kaza kaydi."),
            ("Mudur Yardimcisi", "Kaza raporu, aylik istatistik."),
            ("Sinif Ogretmeni/Veli", "Kendi ogrencisinin saglik gecmisine bakar."),
        ],
        "ana_ozellikler": [
            "Ogrenci saglik karti (alerji, kronik hastalik, asi takvimi)",
            "Gunluk revir ziyaret kaydi",
            "Ilac uygulama takibi (doktor reseteli)",
            "Kaza/olay kaydi (adli vaka olma ihtimaline karsi)",
            "Saglik envanteri (malzeme, ilac stogu)",
            "Ilk yardim dolaplari (lokasyon bazli)",
            "Seminer ve egitim programlari",
            "KVKK erisim logu (kim ne zaman baktı)",
        ],
        "sekmeler": [
            ("Dashboard", "Bugunku revir, acil durumlar, malzeme uyari.", []),
            ("Ogrenci Saglik Karti", "Her ogrenci icin detayli saglik kaydi.",
                ["Ogrenci sec", "Alerji/ilac/kronik hastalik gir", "Kaydet"]),
            ("Revir Ziyareti", "Gunluk revir girisi (neden/isiklem/sonuc).",
                ["Ogrenci sec (ara)", "Neden + islem", "Kaydet + veliye bilgi ver"]),
            ("Ilac Uygulama", "Doktor reseteli ilaclar, zamanlama, veli izni.",
                ["Ilac ekle", "Doz+zaman", "Her uygulamayi isaretle"]),
            ("Kaza/Olay Kaydi", "Kaza, yaralanma, adli olay kaydi — fotograf+aciklama.",
                ["Olay ekle", "Detayli aciklama", "Fotograf yukle", "Mudure bildir"]),
            ("Saglik Envanter", "Malzeme ve ilac stogu + uyari.",
                []),
            ("Ilk Yardim Dolabi", "Dolabin lokasyonu + icerigi + son kontrol tarihi.", []),
            ("Seminer & Egitim", "Ogrenci/veli/ogretmen icin saglik egitimi.",
                ["Egitim olustur", "Katilimci sec", "Arsivle"]),
            ("KVKK Erisim Logu", "Saglik verisine kim ne zaman baktı kaydi.",
                []),
            ("Raporlar", "Aylik istatistik, en sik nedenler, demografik.", []),
        ],
        "is_akisi": [
            "Yil basi: Ogrenci Saglik Karti'nda tum ogrencilerin bilgilerini topla (veliden form).",
            "Gun icinde: Revir Ziyareti kaydi her ogrenci girisinde.",
            "Ilac gerekirse: Ilac Uygulama'da zamanlama ve doz isaretleme.",
            "Kaza olursa: Kaza/Olay Kaydi hemen olustur, fotograf ekle, mudure bildir.",
            "Haftalik: Saglik Envanter kontrol — eksik ise satin alma talebi.",
            "Ayda 1: Seminer olustur (ornek 'Adolesan Saglik', '1. Yardim').",
        ],
        "ipuclari": [
            "Alerji bilgisini veli formunda zorunlu alan yap — hayati onem tasir.",
            "Kaza kaydinda fotograf KVKK uygunlugunu kontrol et (yuz goruntu koruma).",
            "Ilk yardim dolabi kontrol tarihi 3 ayda bir yenile — son kontrol tarihi 90 gun gecince otomatik uyari.",
            "★ BU MODUL ERKEN UYARI 'KENDINE ZARAR/INTIHAR' VE 'MADDE' BOYUTLARINI BESLER:",
            "◆ REVIR ZIYARETI: Her ziyarette 'supheli_yaralanma' CHECKBOX'INI DOGRU KULLAN. Bu tek checkbox Butuncul Risk motoru'nun KENDINE_ZARAR boyutunu dogrudan besler. Supheli bir kesik, tekrar eden yara, aciklama tutmayan bir durum varsa MUTLAKA isaretle. Sadece mudur + psikolog + rehber gorur (yetki kilidi).",
            "◆ 'MADDE_SUPHELI' BAYRAGI: Koku, tavir, supheli materyal varsa revir kaydinda bu bayragi isaretle. MADDE boyutu dogru skorlanir. 5395 SK md.6 — supheli durumda bildirim zorunlu olabilir.",
            "◆ TEKRARLAYAN REVIR: Son 60 gunde 5+ revir ziyareti de kirmizi bayrak. Sistem otomatik yakalar — gereksiz gozlem yapma, dogru girdiginde yeter.",
            "• KVKK Logu'nu periyodik kontrol et — hassas saglik verisine kim baktigi 2 yil saklanir.",
        ],
        "sss": [
            ("Saglik verisi kim gorur?", "Sadece rol = saglik/rehber/mudur yardimcisi. KVKK Logu ile izleme yapilir."),
            ("Veli saglik karti dolduracak?", "Online form linkini gonder, veli doldursun — otomatik sisteme dusmesini sagla."),
            ("'Supheli yaralanma' isaretlersem ne olur?",
             "Butuncul Risk motoru bunu kendine_zarar_intihar boyutuna +2 bayrak olarak sayar. 60 gun icinde tekrar ederse skor 60+ olur, ACIL 24h PROTOKOLU otomatik oneri olarak cikar (psikolog + mudur'e)."),
        ],
    },
    {
        "section_no": 19, "grup": "AKADEMIK", "ad": "Sosyal Etkinlik ve Kulupler", "icon": "🎭",
        "accent": FUCHSIA, "yeni": False,
        "amac": (
            "Sosyal Etkinlik ve Kulupler modulu, okulun sosyal hayatinin kalbidir. 20 sekme ile 10+ "
            "kulup yonetimi, etkinlik takibi, turnuva/yarisma, galeri/arsiv, AI planlama, gamification, "
            "sosyal sorumluluk projeleri ve dijital kapsul (yil sonu anilisi) icerir."
        ),
        "kim": [
            ("Kulup Sorumlusu Ogretmen", "Kulubunun tum faaliyetlerini yonetir."),
            ("Sosyal Etkinlik Koordinatoru", "Tum okul etkinliklerini planlar."),
            ("Ogrenci", "Kulup uyeligi, etkinlik kaydı, portfolyo."),
        ],
        "ana_ozellikler": [
            "10+ kulup CRUD + uye yonetimi",
            "Etkinlik takvimi ve planlama",
            "Turnuva/yarisma yonetimi (puan tablosu)",
            "Galeri ve dijital arsiv",
            "AI destekli etkinlik planlama",
            "Sosyal portfolyo (ogrenci bazli)",
            "Gamification (rozet, XP, lig)",
            "Sosyal sorumluluk proje takibi",
            "Dijital kapsul (yil sonu anilari paketi)",
            "Dis isbirligi (diger okullar/STK)",
            "Medya merkezi (video/foto/metin)",
        ],
        "sekmeler": [
            ("Dashboard", "Aktif kulup, bu hafta etkinlik, katilimci yogunlugu.", []),
            ("Kulupler", "Kulup CRUD + uye yonetimi + performans.",
                ["Kulup olustur", "Uyelik kriteri", "Baskani tayin et"]),
            ("Sosyal Etkinlikler", "Tum etkinlik listesi + takvim.",
                ["Etkinlik olustur", "Kulup sec", "Katilimci listesi"]),
            ("Kulup Performans", "Kulup bazli katilim, etkinlik sayisi, memnuniyet.", []),
            ("Etkinlik Takvimi", "Yillik etkinlik planiyla takvim gorunumu.", []),
            ("Sosyal Portfolyo", "Her ogrencinin sosyal aktivite dosyasi.", []),
            ("Turnuva & Yarisma", "Turnuva CRUD + fikstür + puan tablosu.",
                ["Turnuva olustur", "Takimlar ekle", "Fikstur uret"]),
            ("Galeri & Arsiv", "Etkinlik fotograf/video arsivi.", []),
            ("AI Planlama", "AI etkinlik onerileri (mevsim, bayram, tema bazli).",
                ["Tema sec", "AI oneri al", "Etkinlige cevir"]),
            ("Gamifiye", "Rozet/XP/lig sistemleri (ogrenci motivasyonu).", []),
            ("Sosyal Sorumluluk", "Proje bazli takip (cevre, yardimlasma, farkindalik).", []),
            ("Otomasyon", "Tekrarli etkinlikler icin sablonlar + otomatik olustur.", []),
            ("Medya Merkezi", "Video/foto/metin icerik uretimi + sosyal medya entegrasyonu.", []),
            ("Dis Isbirligi", "Diger okul/STK ile ortak proje yonetimi.", []),
            ("Inovasyon", "Ogrenci inovasyon projeleri (Tubitak/proje pazari).", []),
            ("Dijital Kapsul", "Yil sonu anilari paketi (PDF/video).", []),
            ("Sosyal Endeks", "Ogrencinin sosyal katilim endeksi (0-100).", []),
            ("AI Danisma", "AI'dan etkinlik tema danismanligi.", []),
            ("Smarti", "Bu modul icin AI asistan.", []),
        ],
        "is_akisi": [
            "Yil basi: Kulupler'de yeni yil kuluplerini acip uyelik alma donemi acki.",
            "Eylul: Ogrenciler uyelik basvurusu yapar, sorumlu ogretmen kabul eder.",
            "Aylik: Etkinlik Takvimi'nden aylik etkinlikleri planlar + AI Planlama'dan oneri al.",
            "Etkinlik sonrasi: Galeri'ye foto/video ekle, Sosyal Portfolyo'yu guncelle.",
            "Donem sonu: Turnuva/yarisma duzenle (ornek 'Kulupler Arasi Matematik Turnuvasi').",
            "Yil sonu: Dijital Kapsul uret, velilere gonder (PDF + video).",
        ],
        "ipuclari": [
            "AI Planlama tema olarak 'Dunya Cevre Gunu' verince icerige hazir etkinlik sablonu cikarir.",
            "Sosyal Endeks'i yil sonu karnede kisminda sergileyerek ogrenciyi motive edebilirsin.",
            "Dijital Kapsul'u veliye yil sonu etkinligi gibi duzenle — dokunakli an.",
            "★ BU MODUL ERKEN UYARI 'SOSYAL_IZOLASYON' BOYUTUNU BESLER:",
            "◆ KULUP UYELIK LISTESI: Her kulupte 'Ogrenciler' sekmesine uye ogrenci ekle (ad_soyad + sinif). Butuncul Risk motoru her ogrencinin KAC KULUPTE uye oldugunu sayar. 0 kulup = 60 puan izolasyon. 2+ kulup = 0 puan.",
            "◆ ETKINLIK KATILIMCI LISTESI: Etkinlik olustururken 'Katilimcilar' ve 'Gorevliler' listelerine OGRENCI kategorisiyle ekle. Motor son 90 gun icindeki etkinlik katilimlarini sayar.",
            "◆ BOS KULUP/ETKINLIK LISTESI TEHLIKELI: Kulup acilmis ama ogrenci atanmamis -> herkes izole skoru alir. Yil basinda 'Uyelik Alma Donemi' ile bu liste mutlaka doldurulmali.",
            "• Sosyal Endeks de ayni veriden beslenir — kulup+etkinlik cogaldıkca endeks yukselir.",
        ],
        "sss": [
            ("Kulup secme donemi ne zaman?", "Ayarlar'dan tanimli. Varsayilan Eylul 1-15 arasi — yoneticiniz kontrol etmeli."),
            ("Ogrenci birden fazla kulupte olabilir mi?", "Evet, ayarlarda 'max 3 kulup' gibi sinir koyabilirsiniz."),
            ("Kulup uyeligi girmedim, ogrenciler 'izole' mi gozukecek?",
             "Evet — Butuncul Risk motoru boş uyelik listesini sosyal izolasyon isareti sayar. Yil basinda uyeleri mutlaka gir. Sadece AKTIF kuluplerdeki uyeler sayilir (durum=AKTIF)."),
        ],
    },
    {
        "section_no": 20, "grup": "AKADEMIK", "ad": "Kutuphane", "icon": "📖",
        "accent": BLUE, "yeni": False,
        "amac": (
            "Kutuphane modulu, fiziksel kutuphane materyallerinin kaydi, odunc/iade islemleri, gecikme "
            "ve ceza hesaplamasi, populer kitaplarin analizi ve okuma trendlerinin izlenmesini saglar. "
            "Okumayi tesvik eden gamification unsurlari da icerir."
        ),
        "kim": [
            ("Kutuphaneci", "Materyal kaydi, odunc-iade."),
            ("Sinif Ogretmeni", "Sinif odunc raporu + en cok okuyan ogrenci."),
            ("Ogrenci", "Ara, odunc al, okuma profilini gor."),
        ],
        "ana_ozellikler": [
            "Materyal CRUD (kitap, dergi, DVD)",
            "ISBN tarayici (barkod) ile hizli kayit",
            "Odunc/iade islemi (barcode/QR)",
            "Gecikme takibi + ceza hesabi",
            "Populer kitap analizi",
            "Ogrenci okuma profili + gamification",
            "Kayip/hasar kayit",
        ],
        "sekmeler": [
            ("Dashboard", "Toplam materyal, bugun odunc, gecikme sayisi.", []),
            ("Materyal Kaydi", "ISBN ile hizli kayit veya manuel.",
                ["ISBN gir veya tara", "Otomatik bilgi geldiginde kaydet"]),
            ("Odunc Islemleri", "Ogrenci + kitap ile odunc alma.",
                ["Ogrenci no gir/tara", "Kitap ISBN tara", "Tarih otomatik", "Kaydet"]),
            ("Iade Islemleri", "Kitap iade + gecikme kontrolu.", []),
            ("Gecikmeler & Cezalar", "Gecikmis ogrenci listesi + otomatik ceza hesabi.", []),
            ("Populer Kitaplar", "En cok odunc alinan kitap ve kategori.", []),
            ("Ogrenci Profil", "Her ogrencinin okuma gecmisi + rozet.", []),
            ("Kayip & Hasar", "Kaybolmus/hasarli materyal kaydi + bedel.", []),
            ("Raporlar", "Donemlik okuma trend + kategori analizi.", []),
        ],
        "is_akisi": [
            "Yeni kitap alinca: Materyal Kaydi'nda ISBN tara, bilgileri kontrol et, kaydet.",
            "Ogrenci gelince: Odunc Islemleri sekmesinde iki tarama (ogrenci + kitap).",
            "Iade: Iade Islemleri'nde barkodu tara, gecikme varsa ceza otomatik hesaplanir.",
            "Haftalik: Gecikmeler listesini kontrol et, ogrencilere SMS/veliye bildirim gonder.",
            "Donem sonu: Populer Kitaplar ve Raporlar ile okuma trendlerini analiz et.",
        ],
        "ipuclari": [
            "Barkod tarayicisi yatirimla 3 kat hizli kayit olur — fiziksel cihazi aktarma.",
            "Ogrenci rozet sistemini duyur — 'Yilin Okumaz' ogrenci odulu motivasyon yaratir.",
            "Kayip kitap bedel SMS ile veliye tek tikla bildirilir.",
        ],
        "sss": [
            ("ISBN taranamadi?", "Sorunlu barkod el ile gir — bazi eski kitaplarda ISBN yok (yayin oncesi)."),
            ("Ceza tutarlari yanlis?", "Ayarlar > Ceza Hesaplama'da gunluk tutari kontrol et."),
        ],
    },
    {
        "section_no": 21, "grup": "AKADEMIK", "ad": "Dijital Kutuphane", "icon": "📱",
        "accent": CYAN, "yeni": False,
        "amac": (
            "Dijital Kutuphane modulu, kademe bazli (Okul Oncesi/Ilkokul/Ortaokul/Lise) dijital "
            "egitim kaynaklarini tek arayuzde toplar. YouTube kanallari, e-ogrenme platformlari, "
            "interaktif araclar, canli ders sistemleri, e-kitaplik ve AI ders asistani icerir. "
            "Premium UI ile zengin deneyim."
        ),
        "kim": [
            ("Ogretmen", "Dersine kaynak arar, sinifa paylasir."),
            ("Ogrenci", "Kendi kademesine uygun kaynaga ulasir."),
            ("Veli", "Cocuguna destek kaynagi bulur."),
        ],
        "ana_ozellikler": [
            "Kademe bazli (4 kademe) filtreleme",
            "10+ kategori (Matematik, Fen, Turkce, Ingilizce, Tarih vs)",
            "YouTube kanal kataloglu",
            "E-ogrenme platform entegrasyonlu (Khan, Edpuzzle vs)",
            "Interaktif laboratuvar (PhET, simulation)",
            "Canli ders sistemleri (Zoom/Meet/Teams)",
            "E-kitaplik (reader UI)",
            "AI ders asistani (ChatGPT entegrasyonu)",
            "Ogrenci seviye testi (CEFR/yetkinlik)",
            "Raporlar (hangi kaynak ne kadar kullanildi)",
        ],
        "sekmeler": [
            ("Dashboard", "Kaynak sayisi, bu hafta izlenme, populer kategoriler.", []),
            ("Kademe Secimi", "Okul Oncesi / Ilkokul / Ortaokul / Lise ayrim.",
                ["Kademeyi tikla", "Ilgili kaynaklar filtrelenir"]),
            ("Kategori Filtresi", "Ders bazli filtreleme (Matematik, Fen, Dil vs).", []),
            ("YouTube Kanallari", "Se sili (ogretmen onayli) YouTube kanal listesi.",
                ["Kanal sec", "Video listesi", "Derste paylas"]),
            ("E-Ogrenme Platform", "Khan, Edpuzzle, Quizizz vs link.", []),
            ("Interaktif Araclar", "PhET, GeoGebra, Desmos — simulasyon/oyun.", []),
            ("Canli Ders", "Zoom/Meet/Teams link uretimi + katilim listesi.", []),
            ("E-Kitaplik", "Okunabilir PDF/EPUB reader.", []),
            ("AI Ders Asistani", "ChatGPT destekli ders konusu asistani.",
                ["Konu sec", "Soru yaz", "Cevap + detay"]),
            ("Seviye Testi", "CEFR veya yetkinlik testi ile ogrenciye uygun kaynak.",
                ["Test sec", "Uygula", "Sonuca gore kaynak oner"]),
            ("Raporlar", "Hangi kaynak ne kadar kullanildi, derse etkisi.", []),
        ],
        "is_akisi": [
            "Ogretmen: ders oncesi Kategori + Kademe sec, kaynak tara.",
            "YouTube/Interaktif/E-Kitap kaynagi sec, derse entegre et.",
            "Canli ders yapiliyorsa Canli Ders sekmesinden link uret.",
            "Ogrenci: Kendi kademesinde ders konusu ara; AI Ders Asistani ile detay al.",
            "Periyodik: Raporlar'da hangi kaynagin ne kadar kullanildigini gor.",
        ],
        "ipuclari": [
            "AI Ders Asistani'na 'Bu konuyu yedinci siniftaki bir ogrenciye nasil anlatirdin?' diye sorabilirsin.",
            "Interaktif Araclar (PhET) fen derslerinde unutulmaz deneyim yaratir.",
            "Seviye Testi sonucu kisisellestirilmis kaynak listesi olusturur — AI onerisi secilebilir.",
        ],
        "sss": [
            ("AI cevap vermedi?", "OpenAI API key dolu mu? Ayarlar > Integrations kontrol et."),
            ("Video izlenmiyor?", "YouTube'a okul agindan izin verilmis mi? Ag yoneticisi ile kontrol et."),
        ],
    },
    {
        "section_no": 22, "grup": "AKADEMIK", "ad": "AI Bireysel Egitim", "icon": "🎓",
        "accent": PURPLE, "yeni": False,
        "amac": (
            "AI Bireysel Egitim modulu, her ogrenciye kisisellestirilmis AI ders asistani, yol "
            "haritasi, calisma kocu, gelisim analitigi, sinav hazirligi, ogrenme stili analizi (VARK), "
            "quest sistemi (gamification), Sokratik AI ogretmen, odev asistani, dijital ikiz ve veli "
            "paneli sunar. 13 alt-modul ile uc uclu bireysellestirme."
        ),
        "kim": [
            ("Ogrenci", "Kendi ogrenme hizinda ilerler, AI destegi alir."),
            ("Ogretmen", "Ogrencinin AI uzerinden ilerlemesini takip eder."),
            ("Veli", "Cocugunun AI kullanim gelisimine bakar."),
        ],
        "ana_ozellikler": [
            "13 alt modul",
            "Kisisellestirilmis AI ders asistani",
            "Yol haritasi (ogrenme patikasi)",
            "Calisma kocu (zaman yonetimi)",
            "VARK ogrenme stili analizi",
            "Quest sistemi (gamification)",
            "Sokratik AI ogretmen",
            "Odev asistani",
            "Dijital Ikiz (cocugun dijital muadili)",
            "Sinav hazirlik (AYT/TYT/LGS)",
            "Veli paneli + AI Cockpit",
        ],
        "sekmeler": [
            ("AI Ders Asistani", "Her konuda kisisellestirilmis aciklama + ornek.",
                ["Konu yaz", "Seviye sec", "AI detaylaandir", "Ornek ver"]),
            ("Yol Haritasi", "Ogrenmek istedigi konu icin adim adim patika.",
                ["Hedef sec", "AI haritasi uret", "Ilerlemeyi isaretle"]),
            ("Calisma Kocu", "Gunluk calisma plani + pomodoro + zaman yonetimi.",
                []),
            ("Gelisim Analitik", "VARK testi + ogrenme hizi + eksik alan tespiti.", []),
            ("Sinav Hazirligi", "AYT/TYT/LGS deneme + AI feedback.", []),
            ("Ogrenme Stili (VARK)", "Visual/Auditory/Read/Kinesthetic analiz.", []),
            ("Quest Sistemi", "Oyunlastirilmis gorevler + rozet + XP.", []),
            ("Sokratik AI Ogretmen", "Cevap vermez, sorular sorarak ogretir.", []),
            ("Odev Asistani", "Odev cozumunde AI destek (cozumu yapmaz, yol gosterir).", []),
            ("Dijital Ikiz", "AI ogrenmeni ve performansini simule eder.", []),
            ("Veli Panel", "Veli kendi cocugunun AI kullanimini gorur.", []),
            ("AI Cockpit", "Yonetici/ogretmen — tum ogrencilerin AI kullanim ozeti.", []),
            ("Ekosistem", "Icerikler, kaynaklar, AI dersler.", []),
        ],
        "is_akisi": [
            "Ilk giris: Ogrenme Stili (VARK) testini coz — AI kisisellestirme bunun uzerine kurulur.",
            "Yol Haritasi'nda hedef belirle (ornek: 'TYT Matematik Limit konusunda B+').",
            "Gunluk: Calisma Kocu'ndan plani al, konulari tamamla.",
            "AI Ders Asistani'ni istediginde cagir — kisisel ogretmen gibi.",
            "Quest'leri yap, rozet topla.",
            "Haftalik: Gelisim Analitik'te ilerlemeye bak.",
        ],
        "ipuclari": [
            "Sokratik AI Ogretmen ile calistiginda cevabi kendi bul — daha kalici ogrenirsin.",
            "VARK testini donemde 1 kez tekrarla — stilin degisebilir.",
            "Dijital Ikiz sana 'eger su konuyu daha iyi calisirsan su kadar artis beklenir' oneri verir.",
        ],
        "sss": [
            ("AI cevap yavas?", "OpenAI servisi yuklu. Gece saatlerinde daha hizli."),
            ("Quest rozeti gelmedi?", "Odullendirme gun sonu toplu calistirilir."),
        ],
    },
    {
        "section_no": 23, "grup": "AKADEMIK", "ad": "Yabanci Dil", "icon": "🌍",
        "accent": INDIGO, "yeni": False,
        "amac": (
            "Yabanci Dil modulu, CEFR-uyumlu kurumsal dil ogretim platformudur. Pre-A1'den B2'ye "
            "mufredat, interaktif aktiviteler, quiz/sinav, odev, dinleme/konusma, grup calismalari, "
            "projeler, e-kitaplik ve Smarti AI language tutor ile butunsel dil ogretimi saglar."
        ),
        "kim": [
            ("Yabanci Dil Ogretmeni", "Ders programi, materyal, quiz, sinav."),
            ("Ogrenci", "Ders takip, odev, pratik."),
            ("Koordinator", "CEFR seviyelerini + zumre calismalarini yonetir."),
        ],
        "ana_ozellikler": [
            "CEFR uyumlu (Pre-A1 - B2)",
            "79 ozellik",
            "Interaktif aktiviteler (listening/speaking/reading/writing)",
            "Quiz + sinav + online cozme",
            "Odev atama + teslim + puanlama",
            "Dinleme/konusma (mikrofon)",
            "Grup calismasi araclari",
            "Proje takibi",
            "E-kitaplik (CEFR seviyesine gore)",
            "Smarti dil tutor AI",
        ],
        "sekmeler": [
            ("Dashboard", "Sinif ozeti, CEFR dagilimi, bu hafta sinav.", []),
            ("Sinif Secimi", "Sinif/sube bazli is parcasi.", []),
            ("Ders Programi", "Haftalik mufredat plani.", []),
            ("Mufredat (CEFR)", "Pre-A1'den B2'ye seviye bazli unite.", []),
            ("Ders Materyalleri", "PDF/sunum/video dagitimi.", []),
            ("Odev Yonetimi", "Atama + teslim + puanlama.", []),
            ("Quiz & Test", "Hizli quiz + formal test.", []),
            ("Sinav (Mock/Final)", "Mock sinav + final sinav.", []),
            ("Dinleme & Konusma", "Ses kaydi + AI degerlendirme.", []),
            ("Grup Calismalari", "Grup projeleri + online isbirligi.", []),
            ("Projeler", "Uzun donemli proje takibi.", []),
            ("E-Kitaplik", "CEFR'a gore kitap onerileri.", []),
            ("Raporlar", "Ilerleme + yetenek bazli degerlendirme.", []),
            ("Smarti (Tutor)", "AI dil tutor asistani.", []),
        ],
        "is_akisi": [
            "Yil basi: Ogrencilerin CEFR seviyesi belirle (diagnostic test).",
            "Haftalik: Ders Programi'nda mufredat plani takip et.",
            "Her hafta: Odev ver + quiz uygula.",
            "Aylik: Mock sinav cik, sonuclara gore mufredat uyarla.",
            "Yil sonu: Final sinav + CEFR raporu.",
        ],
        "ipuclari": [
            "Dinleme & Konusma modulunde AI telaffuz analizi ogrencinin kendi kendine calismasini saglar.",
            "Grup Calismalari'nda 3-4 kisiyi farkli seviyelerde karisik sec — yuksek seviye dusugu ceker.",
            "E-Kitaplik'te CEFR seviyesine uygun kitap onerisi — okumayi tesvik eder.",
        ],
        "sss": [
            ("Ses kaydi gonderemiyorum?", "Mikrofon izni ver — tarayici ayarlari kontrol et."),
            ("CEFR seviyesi nasil hesaplaniyor?", "Diagnostic test sonucu + donemlik sinav ortalamasi."),
        ],
    },
    {
        "section_no": 24, "grup": "AKADEMIK", "ad": "Kisisel Dil Gelisimi", "icon": "🎓",
        "accent": TEAL, "yeni": False,
        "amac": (
            "Kisisel Dil Gelisimi modulu, 10 alt modulluk dil ogrenme hub'i: Fono Ingilizce (104 ders), "
            "Fono Almanca/Fransizca/Italyanca/Ispanyolca, KDG Premium Ingilizce ve Almanca, Pratik Dil "
            "(5 dil hub), Dil Treni (10 dilli flashcard + tren gorseli). Toplam 520+ ders."
        ),
        "kim": [
            ("Ogrenci", "Kendi hizinda dil ogrenir."),
            ("Veli", "Cocugunun hangi dili ne kadar ilerledigini gorur."),
            ("Dil Koordinatoru", "Hangi modulun hangi ogrenciye dusecegini planlar."),
        ],
        "ana_ozellikler": [
            "10 alt modul (dil)",
            "520+ ders (toplam)",
            "CEFR seviyeli",
            "104 Ingilizce ders (Fono)",
            "10 dil flashcard (Dil Treni)",
            "Pratik Dil — 5 dil hub",
            "Telaffuz + dinleme + yazma",
            "Seviye testi",
        ],
        "sekmeler": [
            ("Fono Ingilizce", "104 ders, A1-B1.", []),
            ("Fono Almanca", "", []),
            ("Fono Fransizca", "", []),
            ("Fono Italyanca", "", []),
            ("Fono Ispanyolca", "", []),
            ("KDG Ingilizce (Premium)", "CEFR Premium.", []),
            ("KDG Almanca (Premium)", "", []),
            ("Pratik Dil", "5 dil hub.", []),
            ("Dil Treni", "10 dilli flashcard + tren.", []),
            ("Smarti + Ayarlar", "", []),
        ],
        "is_akisi": [
            "Dil sec (menu).",
            "Seviye testi yap (varsa).",
            "Ders yolunda ilerle (her ders ~15 dk).",
            "Alistirmalari tamamla.",
            "Haftalik quiz ile pekistir.",
            "Aylik seviye sinavi.",
        ],
        "ipuclari": [
            "Dil Treni'nin '10 dil' modunda haftada 2 yeni kelime prensibiyle hifiza baglanti kurabiliyor.",
            "Pratik Dil hub 5 dilde ozet konusma sablonlari — tatillerde cok pratik.",
            "Fono 104 ders plani CEFR'a birebir uyumlu; okul mufredatina entegre et.",
        ],
        "sss": [
            ("Hangi dilden baslayayim?", "Okul mufredatinda varsa onden, yoksa ilgi alanina gore — Ispanyolca en populer."),
        ],
    },
    {
        "section_no": 25, "grup": "AKADEMIK", "ad": "Erken Uyari Sistemi", "icon": "⚠️",
        "accent": ORANGE, "yeni": False,
        "amac": (
            "Erken Uyari Sistemi, 9 modulden 43 veri kaynagi toplayan, 10-boyutlu AI risk skoru uretip "
            "riskli ogrencileri proaktif olarak tespit eden akilli erken uyari motorudur. v2.1 ile "
            "eklenen BUTUNCUL RISK 20-BOYUT motoru akademik + davranissal riskleri birlestirir: "
            "zorbalik, intihar, madde, aile, duygusal, disiplin, sosyal izolasyon kategorilerinde "
            "otomatik riskli ogrenci listeleri, mudahale protokolu motoru, yetki-kilitli hassas "
            "boyutlar, aciklanabilir AI ve KVKK denetim logu ile tam MEB/5395 SK/AI Act uyumlu."
        ),
        "kim": [
            ("Mudur / Mudur Yardimcisi", "Tum 20 boyutu gorur. Kategori bazli listeye bakar. Toplu mudahale protokolu baslatir."),
            ("Rehber Ogretmen / Psikolog", "Hassas boyutlari (intihar, madde, aile) gorur. Mudahale protokolunu uygular."),
            ("Sinif Ogretmeni / Brans", "Kendi sinifindaki ogrencilerin AKADEMIK + davranissal (hassaslar haric) skorunu gorur."),
            ("Koc", "Atanan ogrencilerin akademik + davranis profilini inceler, mudahale planlar."),
            ("Veli (sadece kendi cocugu)", "Gizli/hassas boyutlar gizli; akademik + genel ozet gorunur."),
        ],
        "ana_ozellikler": [
            "9 modulden cross-modul veri (43 kaynak)",
            "10 boyutlu akademik risk skoru (klasik)",
            "10 boyutlu DAVRANISSAL risk skoru ★ (v2.1 — zorbalik, intihar, madde, aile, duygusal, disiplin, izolasyon, sosyoekonomik, devamsizlik, akademik-davranis celiski)",
            "KATEGORI BAZLI OTOMATIK LISTE ★ (10 kategori, otomatik riskli ogrenci gruplama)",
            "20 boyutlu butuncul radar (akademik sol + davranissal sag)",
            "Mudahale protokolu motoru (7 onceden tanimli protokol, 5395 SK uyumlu)",
            "Yetki-kilitli hassas boyutlar (KVKK md. 6)",
            "Aciklanabilir AI (her skor icin neden + guven araligi)",
            "Yanlis pozitif feedback (model kalibrasyonu)",
            "KVKK denetim logu (2 yil retention)",
            "Ogrenci 360 profil cross-module",
            "Basari Haritasi ★, Cross-Alert ★, Kariyer Pusula ★",
        ],
        "sekmeler": [
            ("Dashboard", "Risk dagilimi (dusuk/orta/yuksek/kritik) ve trend.", []),
            ("Ogrenci 360 Profil", "Riskli ogrencinin tam profili — cross-module.", []),
            ("Erken Uyari Listesi", "Riskli ogrencilerin siralanmis listesi.", []),
            ("Risk Detay ve Analiz", "Ogrenci sec, 10-boyutlu radara bak.", []),
            ("Sinif Karsilastirmasi", "Sinif bazli risk dagilimi kiyaslama.", []),
            ("Heatmap / Radarlar / Trend", "Gorsel analiz paketi.", []),
            ("Mudahale Plani", "AI oneriler + mudahale adimlari.", []),
            ("Zorbalik Tespit / Davranis Tarama", "Ozel davranis analizleri.", []),
            ("Risk Fuzyon / Risk DNA", "Cok kaynakli risk birlestirme.", []),
            ("Bildirim Merkezi / Komuta Merkezi", "Uyari yonetimi.", []),
            ("Basari Haritasi ★ / Cross-Alert ★ / Kariyer Pusula ★ (v2.0)",
             "Ileri analiz sekmeleri.", []),
            ("Butuncul Risk 20-Boyut ★ (v2.1)",
             "20 BOYUTLU AKADEMIK + DAVRANISSAL BIRLESIK RISK PANELI. 7 alt bolum tek sayfada:",
             [
                 "Kategori Bazli Otomatik Liste — 10 kategori, otomatik riskli ogrenciler",
                 "Ogrenci Analizi — tek ogrenci 20 boyut radar + protokol",
                 "Mudahale Protokolleri — aktif protokoller, onay ve takip",
                 "Risk Listesi — tum ogrenciler tablo + kritik uyari",
                 "Model Kalibrasyon — yanlis pozitif geri bildirim ozeti",
                 "KVKK Denetim Logu — son 30 gun hassas veri erisim",
                 "Toplu Hesaplama — tum ogrenciler icin batch risk uret",
             ]),
        ],
        "is_akisi": [
            "ILK KURULUMDA: Butuncul Risk 20-Boyut > Toplu Hesaplama > '🚀 Tum Ogrenciler icin Hesapla' butonuna bas. 204 ogrenci icin motor 15-30 saniyede tamamlanir.",
            "Sabah (gunluk): Dashboard'da risk dagilimini incele. Kritik renk varsa detaya in.",
            "Butuncul Risk 20-Boyut > Kategori Bazli Otomatik Liste: her kategoride riskli ogrencileri gor (Zorbalik, Intihar, Madde, Duygusal, Aile, Disiplin, Izolasyon, Sosyoekonomik, Devamsizlik).",
            "Kritik ogrenci icin: Ogrenci Analizi'nde 20 boyutlu radar + her boyut icin NEDEN + GUVEN araligina bak.",
            "Otomatik uretilen Mudahale Protokolu listesinden ONAYLA / BASLAT / IPTAL et (insan karar verir, AI karar vermez).",
            "Haftalik: Trend Grafikleri'nde mudahalenin etkisine bak. Risk dustu mu?",
            "KATEGORI BAZLI TOPLU AKSIYON: Butuncul Risk > Kategori > 'Toplu Protokol Baslat' butonu ile tum riskliler icin tek tikla plan acilir.",
        ],
        "ipuclari": [
            "MOTORUN CALISMASI ICIN SART OLAN VERI GIRISI (KIM NE GIRER?):",
            "• SINIF OGRETMENI: Akademik Takip > Yoklama (gunluk) + Mudahale Kayitlari (gozlem). → devamsizlik + disiplin boyutlari beslenir.",
            "• REHBER/PSIKOLOG: Rehberlik > Vaka Kaydi (konu dogru sec: Akran Zorbaligi / Aile sorunlari / Kaygi / vb) + Gorusme Kaydi (notlara anahtar kelime). → zorbalik, aile, duygusal, intihar, madde boyutlari beslenir.",
            "• REHBER: Aile Bilgi Formu doldur (aile_durumu, ozel_durum) → aile_risk + sosyoekonomik boyutlari beslenir.",
            "• HEMSIRE: Okul Sagligi > Revir Ziyareti kaydet + 'supheli_yaralanma' checkbox'ini dogru kullan → kendine_zarar boyutu beslenir.",
            "• OGRENCI: Ogrenci Paneli > ust bolumde '😊 Bugunkü Ruh Halin' — gunluk check-in. → duygusal boyut beslenir.",
            "• SOSYAL ETKINLIK SORUMLUSU: Kulup uyelik + etkinlik katilimci listelerini doldur → sosyal_izolasyon boyutu beslenir.",
            "• SSG: Ihbar Hatti paneli — poster/QR ile ogrenciye duyur, anonim ihbar kategori sayilari motor'a sinyal olur.",
            "Risk skoru 70+ (Kritik) ogrenciler icin 48 saat icinde mudahale plani baslat.",
            "Intihar/Madde/Aile gibi hassas boyutlar SADECE mudur/yardimci/psikolog/rehber rolunde gorunur (KVKK md.6 + 5395 SK).",
            "AI skoru yanlis goruyorsan 'Yanlis Pozitif Geri Bildirim' ile isaretle — model kalibre edilir.",
            "Her skor tiklanabilir: NEDEN + GUVEN YUZDESI + KAYNAK dosyalar gosterilir (aciklanabilir AI zorunlulugu).",
        ],
        "sss": [
            ("Motor calismadi, skorlar 0 geldi?",
             "Veri girisi eksik. Su 4 dosyadan biri doluysa motor o boyutu hesaplar: attendance.json (yoklama), vaka_kayitlari.json (rehberlik), aile_bilgi_formlari.json (aile formu), revir_ziyaretleri.json (saglik). Digerlerinin de doldurulmasi icin ilgili modulleri aktif kullan."),
            ("Hassas bolumleri goremiyorum?",
             "Rolun izin vermiyor. Intihar, madde, aile gibi bolumler sadece SuperAdmin / Yonetici / Mudur / Mudur Yardimcisi / Psikolog / Rehber / Calisan rolunde gorunur. Sinif Ogretmeni + Ogretmen bu bolumleri goremez (yetki kilidi)."),
            ("Toplu protokol baslatinca ne olur?",
             "Her ogrenci icin ayri protokol kaydi olusur, durumlari 'onerildi' olur. YETKILI bu protokolleri ONAYLA / BASLAT / TAMAMLA / IPTAL edebilir. Otomatik aksiyon tetiklenmez — insan karari her zaman sart (AI Act zorunlulugu)."),
            ("Kategorilerde hep '0 ogrenci' goruyorum?",
             "Ilk defa kullanyorsan Toplu Hesaplama sekmesinden batch calistirmayi unutmus olabilirsin. Oraya git ve '🚀 Tum Ogrenciler icin Hesapla' butonuna bas."),
            ("Yanlis pozitif feedback ne ise yarar?",
             "Rehber/Psikolog 'Bu skor yanlis' diyip dogru degeri girince motor bir sonraki calismada ilgili boyutu kalibre eder. Mod sahte pozitif (false positive) istatistigi 'Model Kalibrasyon' bolumunde gorunur."),
        ],
    },
    {
        "section_no": 26, "grup": "AKADEMIK", "ad": "Egitim Koclugu", "icon": "🏅",
        "accent": GOLD, "yeni": False,
        "amac": (
            "Egitim Koclugu modulu, 1:1 bireysel kocluk platformudur. SMART hedef belirleme, haftalik "
            "plan, gorusme kaydi, motivasyon takibi, deneme sinavi analizi, zaman yonetimi, veli "
            "raporlari ve Smarti coaching bot ile ogrencinin donusumsel gelisimini yonetir."
        ),
        "kim": [
            ("Egitim Kocu (ogretmen/uzman)", "Atanan ogrencilerin kocluk surecini yurutur."),
            ("Ogrenci", "Hedef koyar, takip eder, gorusme yapar."),
            ("Veli", "Cocugunun koclukta gelisimini izler."),
        ],
        "ana_ozellikler": [
            "Ogrenci-koc atama",
            "1:1 gorusme kaydi (ses/metin)",
            "SMART hedef belirleme",
            "Haftalik plan",
            "Motivasyon egrisi",
            "Odev izlemesi (kocluk disi)",
            "Deneme sinavi analizi (TYT/AYT/LGS)",
            "Zaman yonetimi (calendar)",
            "Canli ders entegrasyonu",
            "Soru kutusu (asenkron)",
            "Veli rapor + geri bildirim",
            "Ilerleme grafikleri",
            "Smarti coaching bot",
        ],
        "sekmeler": [
            ("Dashboard", "Kocluk alti ogrenci sayisi, haftalik durum.", []),
            ("Ogrenciler (Atama)", "Ogrenci-koc atama yonetimi.", []),
            ("Gorusmeler", "1:1 gorusme kaydi — ses + not.", []),
            ("SMART Hedef", "Spesifik/Olculebilir/Ulasilabilir/Relevant/Zamanli hedef.", []),
            ("Haftalik Plan", "Haftanin gunluk task listesi.", []),
            ("Motivasyon Takibi", "Motivasyon egrisi + trend.", []),
            ("Odev Izleme", "Kocluk disi odev takibi.", []),
            ("Deneme Analizi", "TYT/AYT/LGS deneme sonuc + trend.", []),
            ("Zaman Yonetimi", "Calendar ile ders/gorusme/sinav.", []),
            ("Canli Ders", "Online ders linki + katilim.", []),
            ("Soru Kutusu", "Asenkron ogrenci sorulari.", []),
            ("Veli Rapor", "Aylik veli raporlari.", []),
            ("Ilerleme Grafikleri", "Net/puan/hedef trend.", []),
            ("Smarti Coaching Bot", "Koc ve ogrenci AI destegi.", []),
        ],
        "is_akisi": [
            "Koc atama: Dashboard > Ogrenciler > Atama.",
            "Ilk gorusme: Ogrenci tanima + needs assessment (60 dk).",
            "SMART Hedef olustur (ornek: '6 hafta sonunda TYT mat neti 15'ten 22'ye cikmak').",
            "Haftalik Plan olustur (her gunu detaylandir).",
            "Haftalik gorusme: Gorusmeler'de kaydet, Motivasyon isaretle.",
            "Deneme sonrasi Deneme Analizi'nde konu bazli net + dusum/yukselis.",
            "Aylik: Veli Raporu otomatik olustur, veliye gonder.",
            "Yil sonu: Ilerleme Grafikleri ile donusumu goster.",
        ],
        "ipuclari": [
            "SMART hedeflerde 'Spesifik' ve 'Zamanli' kisimlari cok onemli — 'iyi olsun' degil '15 puan artsin' yaz.",
            "Motivasyon 3 hafta ust uste dusukse mutlaka velisi ile ortak gorusme yap.",
            "Smarti Coaching Bot kocun yerine gecmez — arasinda farkli bir agenda ile calisir.",
        ],
        "sss": [
            ("Koc atayabilmem icin ne lazim?", "Personel Kayit'ta 'Koc' rolu tanimlanmali."),
            ("Deneme analizi yanlis?", "Deneme sonuclarini Olcme modulunden cekiyor — oradan senkronlastir."),
        ],
    },
    {
        "section_no": 27, "grup": "AKADEMIK", "ad": "AI Treni (Bilgi Treni)", "icon": "🚂",
        "accent": LIME, "yeni": False,
        "amac": (
            "AI Treni (Bilgi Treni) modulu, her sinif (1-12) icin ayri bir vagon, her vagonda 10 "
            "kompartiman (Konu Anlatimi, Kultur&Sanat, Bilim, Edebiyat, Quiz, Oyun, Matematik "
            "Atolyesi, Yabanci Dil, Deney Lab, Genel Kultur) ile ogrenmeyi eglenceli ve sisteme "
            "yapilandirilmis hale getiren gamified egitim ekosistemidir."
        ),
        "kim": [
            ("Ogrenci", "Kendi siniifinin vagonuna biner, kompartimanlara gider."),
            ("Ogretmen", "Dersine Konu Anlatimi kompartimanindan destek alir."),
            ("Veli", "Cocugunun hangi vagonu, hangi kompartimanda vakit gecirdigini gorur."),
        ],
        "ana_ozellikler": [
            "12 vagon (1-12. sinif)",
            "10 kompartiman (her vagon)",
            "Konu Anlatimi (MEB uyumlu)",
            "Kultur & Sanat bolumleri",
            "Bilim & Teknik",
            "Edebiyat",
            "Bilgi Yarismasi (quiz)",
            "Oyunlar (Memory, Stroop, Math Races, Riddle)",
            "Matematik Atolyesi (Math Games)",
            "Yabanci Dil (Vocabulary, Pronunciation)",
            "Deney Lab (video + simulasyon)",
            "Genel Kultur",
            "Rozet ve skor sistemi",
        ],
        "sekmeler": [
            ("Vagon Secimi", "1-12 sinif icinden secim.",
                ["Sinif sec", "Vagona bin"]),
            ("Konu Anlatimi", "MEB uyumlu konu anlatimi.", []),
            ("Kultur & Sanat", "Muze, tarih, sanat icerigi.", []),
            ("Bilim & Teknik", "Populer bilim iceriklleri.", []),
            ("Edebiyat", "Yazar-eser-tema analizleri.", []),
            ("Bilgi Yarismasi", "Quiz oyunlari.", []),
            ("Oyunlar", "Memory, Riddle, Stroop, Math Races.", []),
            ("Matematik Atolyesi", "Math Games.", []),
            ("Yabanci Dil", "Vocabulary + Pronunciation.", []),
            ("Deney Lab", "Video + simulasyon.", []),
            ("Genel Kultur", "", []),
            ("Rozetler & Skorlar", "Kazanilan rozet + siralama.", []),
        ],
        "is_akisi": [
            "Ogrenci sinifini sec > vagonuna bin.",
            "Kompartiman sec (ornek Deney Lab).",
            "Icerik izle/oyun oyna/quiz coz.",
            "Rozet kazan.",
            "Diger kompartimanlara gec.",
            "Hafta sonu siralama bakimi.",
        ],
        "ipuclari": [
            "Ogrenci motivasyonunu yuksek tutmak icin haftalik rozet hedefi tanimla.",
            "Deney Lab'i fen dersi ile entegre et — ogretmen oneri ver.",
            "Yarisma modundaki 'Sinif karsi Sinif' turnuvalar cok tutulur.",
        ],
        "sss": [
            ("Vagon secimi nerede?", "AI Treni modulune girdiginde ilk ekran vagon secimi."),
            ("Deney Lab yavas acildi?", "Interaktif simulasyon agir — tarayicini guncelle."),
        ],
    },
    {
        "section_no": 28, "grup": "AKADEMIK", "ad": "STEAM Merkezi", "icon": "🔬",
        "accent": FUCHSIA, "yeni": True,
        "amac": (
            "STEAM Merkezi (v2.0 ★) ekosistemi — 100 proje, 5 disiplin (Bilim, Teknoloji, Muhendislik, "
            "Sanat, Matematik), Robotik, Kodlama, 3D modelleme, Maker atolyesi, yarismalar ve turnuvalar "
            "ile 21. yuzyil yeteneklerinin kurumsallasmasini saglayan disiplinler arasi proje platformu."
        ),
        "kim": [
            ("STEAM Koordinatoru", "Projeler + mentorluk + yarisma."),
            ("Ogretmen (Fen/Mat/Tekno)", "Proje onerir, mentorluk yapar."),
            ("Ogrenci", "Proje sec, gerceklestir, yarismaya katil."),
        ],
        "ana_ozellikler": [
            "100 proje katalogu",
            "5 disiplin (Bilim/Tekno/Muh/Sanat/Mat)",
            "Skill Tree (yetkinlikler)",
            "Live Lab (canli deney)",
            "Rozet sistemi",
            "Proje yonetimi",
            "Muhendislik gorevleri",
            "Yarismalar ve turnuvalar",
            "Profil (basarilar)",
            "Mentor paneli",
            "Kaynak kutuphane",
        ],
        "sekmeler": [
            ("Panel (Dashboard)", "Proje sayisi, aktif ogrenci, yarismalar.", []),
            ("Showcase", "En iyi projeler.", []),
            ("Skill Tree", "Yetkinlik agaci.", []),
            ("Live Lab", "Canli deney odasi.", []),
            ("Rozetler", "Kazanilan rozet.", []),
            ("Proje Yonetimi", "Proje CRUD + atama.", []),
            ("Muhendislik Gorevleri", "Problem cozme challenge.", []),
            ("Yarismalar & Turnuvalar", "TUBITAK + diger yarismalar.", []),
            ("Profil", "Basarilar + portfolio.", []),
            ("Matematik", "Matematik ekrani.", []),
            ("Bilisim", "Kodlama.", []),
            ("Sanat", "3D/Design.", []),
            ("Mentor Paneli", "Mentor atama + takip.", []),
            ("Kaynak Kutuphane", "STEM kaynaklari.", []),
            ("Raporlar", "Proje tamamlanma + yetkinlik.", []),
        ],
        "is_akisi": [
            "Ogrenci Panel'den proje kataloguna bakar.",
            "Ilgi + yetkinligine gore proje sec.",
            "Mentor ata (sorumlu ogretmen).",
            "Proje Yonetimi'nde asamalari yonet.",
            "Tamamlandiginda Showcase'e ekle.",
            "Yarismaya katil.",
        ],
        "ipuclari": [
            "Skill Tree her yil guncellenmeli — yeni teknolojiler (AI, Web3) ekle.",
            "Showcase'e giren proje kendi dalinda yarismaya gitmeye adaydir.",
            "Live Lab'da fizik derslerinde gercek zamanli deney cok etkili.",
        ],
        "sss": [
            ("Proje tamamlanmadi, notum ne olacak?", "Proje Yonetimi'nde durum degistir — koordinator karar verir."),
        ],
    },

    # ──────────────────── OPERASYON (4) ────────────────────
    {
        "section_no": 29, "grup": "OPERASYON", "ad": "Tuketim ve Demirbas", "icon": "🗄️",
        "accent": SLATE, "yeni": False,
        "amac": (
            "Tuketim ve Demirbas modulu, okulun tum fiziksel kaynak yonetimidir: gunluk tuketim kaydi "
            "(kirtasiye, yiyecek, temizlik), stok takibi, demirbas kaydi (bilgisayar, masa, projeksiyon), "
            "zimmet yonetimi, AI reorder tavsiyesi, satin alma talepleri, fiyat teklifi karsilastirma, "
            "siparis takibi ve tedarikci yonetimi icerir."
        ),
        "kim": [
            ("Idari Isler Sorumlusu", "Gunluk tuketim + stok + satin alma."),
            ("Muhasebe", "Satin alma onay + fatura."),
            ("Zimmet Alici (Calisanlar)", "Kendisine zimmetli demirbaslar."),
        ],
        "ana_ozellikler": [
            "Gunluk tuketim kaydi (20+ kategori)",
            "Stok goruntuleme + min stok uyari",
            "Demirbas kaydi (barkod/QR)",
            "Zimmet atamasi (kim kullaniyor)",
            "AI reorder tavsiyesi (hangi urun ne zaman siparisli)",
            "Satin alma talepleri (workflow)",
            "Fiyat teklifi karsilastirma",
            "Siparis takip (suresi, kargo)",
            "Tedarikci yonetimi",
        ],
        "sekmeler": [
            ("Dashboard", "Min stok uyarisi, bu ay harcama, bekleyen siparis.", []),
            ("Tuketim Kaydi", "Gunluk tuketim girisi.",
                ["Kategori sec", "Miktar + tarih", "Kaydet"]),
            ("Stok Goruntu", "Tum stok listesi + filtreleme.", []),
            ("Demirbas Kaydi", "Demirbas CRUD + barkod.", []),
            ("Zimmet Yonetimi", "Kim kullaniyor + tarih.",
                ["Calisan sec", "Demirbas sec", "Zimmet ver/al"]),
            ("AI Tavsiye", "Reorder onerisi (stok + trend).", []),
            ("Satin Alma Talepleri", "Talep CRUD + onay.", []),
            ("Fiyat Teklifleri", "Tedarikcilerden teklif karsilastirma.", []),
            ("Siparis Takip", "Siparis durumu + kargo.", []),
            ("Tedarikci Yonetimi", "Tedarikci CRUD + performans.", []),
            ("Raporlar", "Donemlik tuketim + demirbas envanter.", []),
        ],
        "is_akisi": [
            "Gun icinde: Tuketim Kaydi'nda her kullanimi kaydet (kirtasiye, yiyecek).",
            "Haftalik: Stok Goruntu'de eksilenleri gor; AI Tavsiye'den reorder onerisi al.",
            "Satin Alma Talepleri'nde onaya gonder.",
            "Fiyat Teklifleri'nde 3 tedarikciden teklif iste.",
            "Onay sonrasi Siparis Takip'e gec.",
            "Gelen demirbas: Demirbas Kaydi + Zimmet Yonetimi.",
        ],
        "ipuclari": [
            "AI Tavsiye her hafta calissin — 2 hafta once siparisi vermek yok-olma sorununu onler.",
            "Demirbaslarin barkodu fiziksel etiket + dijital kayit olmali — denetim kolaylasir.",
            "Tedarikci performansini 3 ayda bir gozlemle — gec teslimat veya kalite sorunu olaninstri.",
        ],
        "sss": [
            ("Stok yanlis gorunuyor?", "Son tuketim kaydi eksik olabilir — gun sonunda tekrar yapma aliskanligi edin."),
            ("Zimmet iade islem yok?", "Zimmet Yonetimi'nde demirbas sec, 'Iade Al' butonu."),
        ],
    },
    {
        "section_no": 30, "grup": "OPERASYON", "ad": "Destek Hizmetleri Takip", "icon": "🔧",
        "accent": AMBER, "yeni": False,
        "amac": (
            "Destek Hizmetleri Takip modulu, okuldaki tum hizmet taleplerini (ticket) yonetir: ariza "
            "bildirimi, bakim talebi, temizlik istegi, teknik destek. SLA takibi, periyodik gorev "
            "planlamasi, denetim formlari ve bakim kayitlari ile is surecleri akisini kontrol altinda "
            "tutar."
        ),
        "kim": [
            ("Idari Isler Sorumlusu", "Ticket atama + SLA takibi."),
            ("Teknik Ekip", "Kendine atanan ticket'lari islet."),
            ("Ogretmen/Calisan", "Talep acar, takip eder."),
        ],
        "ana_ozellikler": [
            "Ticket CRUD + oncelik (Kritik/Yuksek/Normal/Dusuk)",
            "Durum takibi (Acik/Devam/Cozuldu)",
            "SLA kontrol (zamanindalik)",
            "Periyodik gorevler (aylik bakim)",
            "Denetim formu",
            "Bakim kaydi",
            "Raporlar (verimlilik)",
            "Tedarikci yonetimi",
        ],
        "sekmeler": [
            ("Dashboard", "Acik ticket, SLA ihlal, cozum suresi.", []),
            ("Talepler (Tickets)", "Tum ticket CRUD.",
                ["Talep ac (kategori + oncelik + aciklama)", "Ata (ekip)", "Durum guncelle"]),
            ("Durum Takip", "Kanban goruntusunde Acik/Devam/Cozuldu.", []),
            ("SLA Kontrol", "Her ticket'in hedef suresi vs gercek suresi.", []),
            ("Periyodik Gorevler", "Aylik/Uc Aylik bakim planlari.", []),
            ("Denetim Formu", "Temizlik/guvenlik denetimi.", []),
            ("Bakim Kaydi", "Yapilmis bakim gecmisi.", []),
            ("Tedarikci Yonetimi", "Dis servis saglayicilari.", []),
            ("Raporlar", "Verimlilik + SLA analiz.", []),
            ("Ayarlar", "Kategori + oncelik + SLA esik degerleri.", []),
        ],
        "is_akisi": [
            "Talep alinca: Talepler'de ticket ac (kategori + oncelik + aciklama).",
            "Ekip ata; teknik ekip ticket'i alir.",
            "Islem bittiginde durum 'Cozuldu' isaretle.",
            "SLA Kontrol'de ihlal var mi gor.",
            "Aylik: Periyodik Gorevler calisir (otomatik bakim).",
            "Denetim Formu'nu periyodik kontrol et.",
            "Raporlar'dan verimlilik olc.",
        ],
        "ipuclari": [
            "Kritik ticket icin 4 saat SLA — onemli esik.",
            "Periyodik bakim ihmal edilince acil ticket sayisi yukselir. Plan iyi takip et.",
            "Tedarikci performansini 3 ayda bir gozlemle; zayif olanini degistir.",
        ],
        "sss": [
            ("SLA ihlal oldu, ne yapmali?", "Raporlar'da nedenini analiz et — ekip yogunlugu, tedarikci gecikmesi vs."),
        ],
    },
    {
        "section_no": 31, "grup": "OPERASYON", "ad": "Sivil Savunma ve IS Guvenligi", "icon": "⛑️",
        "accent": CORAL, "yeni": False,
        "amac": (
            "Sivil Savunma ve IS Guvenligi modulu, 3 bolumu tek panelden yonetir: Sivil Savunma "
            "(yangin/deprem tatbikati), ISG (is saglik + guvenlik, risk matrisi), Okul/Ogrenci "
            "Guvenligi (zorbalik, bagimsiz ihbar). Tatbikat planlama, risk yonetimi, denetim kaydi, "
            "olay kaydi, eylem plani ve v2.0 Egitim Akademisi + ISG Olcum + Zorbalik Onleme ★ icerir."
        ),
        "kim": [
            ("Sivil Savunma Amiri", "Tatbikat + risk + egitim."),
            ("IS Guvenligi Uzmani", "ISG modulu + denetim + olay."),
            ("Mudur Yardimcisi (Guvenlik)", "Ogrenci guvenligi + zorbalik."),
        ],
        "ana_ozellikler": [
            "3 bolum (Sivil Savunma / ISG / Ogrenci Guvenlik)",
            "Checklist yonetimi",
            "Tatbikat planlama + degerlendirme",
            "Risk yonetimi + matris",
            "Denetim kaydi",
            "Olay kaydi (kaza, zorbalik)",
            "Eylem plani + takip",
            "Sorumlular yonetimi",
            "Egitim Akademisi ★ (v2)",
            "ISG Olcum ★ (v2 — gurultu, isik, hava)",
            "Zorbalik Onleme ★ (v2 — Ihbar Hatti entegrasyonlu)",
        ],
        "sekmeler": [
            ("Dashboard", "Aktif risk, yakin tatbikat, acik olay.", []),
            ("Checklist Yonetimi", "Guvenlik + saglik checklist.", []),
            ("Tatbikat Planlama", "Yangin + deprem + sizdirma tatbikatlari.", []),
            ("Tatbikat Degerlendirme", "Tatbikat sonrasi puanlama + rapor.", []),
            ("Risk Yonetimi", "Risk envanteri (5x5 matris).", []),
            ("Risk Matrisi", "Olasilik x siddet gorseli.", []),
            ("Denetim Kaydi", "Periyodik denetim sonuclari.", []),
            ("Olay Kaydi", "Kaza/yaralanma/zorbalik kaydi.", []),
            ("Eylem Plani", "Olay sonrasi aksiyon + sorumlu + tarih.", []),
            ("Egitim Akademisi ★", "Calisan + ogrenci guvenlik egitimleri.", []),
            ("ISG Olcum ★", "Gurultu, isik, hava kalite olcumu.", []),
            ("Zorbalik Onleme ★", "Bagimsiz ihbar hatti entegrasyonlu.", []),
            ("Sorumlular Yonetimi", "Bolum bazli sorumlu ata.", []),
            ("Raporlar", "Tatbikat + risk + olay raporlari.", []),
        ],
        "is_akisi": [
            "Yil basi: Risk envanteri olustur (ornek 'yangin', 'deprem', 'su baskini', 'siber').",
            "Risk Matrisi'nde olasilik + siddet isaretle.",
            "Tatbikat Planlama'da aylik/ucer aylik tatbikat ata.",
            "Tatbikat gunu: Tatbikati yap, Degerlendirme'de puan ver.",
            "Periyodik: Denetim Kaydi + Egitim Akademisi ★.",
            "Olay cikarsa: Olay Kaydi + Eylem Plani hemen olustur.",
        ],
        "ipuclari": [
            "Yangin tatbikati yilda 2 kez zorunlu — Tatbikat Planlama'da otomatik olarak hatirlatma ayarla.",
            "Zorbalik Onleme ★ Ihbar Hatti'na entegre — ihbar gelen olay otomatik olay kaydi olur.",
            "ISG Olcum ★ sonuclari yonetmeliklerde belirli esikleri asarsa otomatik uyari gonderir.",
            "★ IHBAR HATTI ERKEN UYARI SISTEMINE DOLAYLI VERI AKTARIR:",
            "◆ IHBAR HATTI 8 KATEGORI: akran_zorbaligi, intihar_riski, madde_kullanim, cinsel_taciz, aile_ici_siddet, akademik_kopya, personel_sikayet, diger. Her kategorinin KOLEKTIF sayisi Butuncul Risk motoru'nda okul-geneli trend olarak gorunur.",
            "◆ ANONIMLIK KORUNUR: Ihbar eden ve ihbar konusu kisinin kimligi motor'a aktarilmaz (etik + KVKK). Motor sadece 'bu okulda madde ihbarlari arttigini gosteren trend' gibi kolektif sinyal verir.",
            "◆ IHBAR PANELI DUYURU SART: Poster + QR kod + sinif duyurulariyla ogrenciye tanit. Varligini bilinmeyen kanal kullanilmaz. SSG > Zorbalik Onleme veya Rehberlik > Kriz Mudahale sekmesinden erisim sagla.",
            "◆ IHBAR INCELEME REHBERDE: Gelen ihbarlar Rehberlik'te ILGILI yetkili tarafindan incelenir + durum (Yeni/Inceleniyor/Mudahale Edildi/Cozuldu) guncellenir.",
        ],
        "sss": [
            ("Tatbikat katilim zorunlu mu?", "Evet, resmi yonetmelikte sart. Yoklama tuttugundan emin ol."),
            ("Ihbar Hatti Erken Uyari motoruna ne veriyor?",
             "Kolektif trend: 'Bu donem akran_zorbaligi kategorisinde 12 ihbar -> okul genelinde zorbalik risk artmis olabilir' gibi. Bireysel ogrenciye sinyal YAPILMAZ (anonim tasarim)."),
        ],
    },
    {
        "section_no": 32, "grup": "OPERASYON", "ad": "Mezunlar ve Kariyer Yonetimi", "icon": "🎓",
        "accent": GOLD, "yeni": False,
        "amac": (
            "Mezunlar ve Kariyer Yonetimi modulu, mezun veritabanini canli tutar, hedef kampanyalari "
            "(etkinlik, reunion), mentorluk eslesmeleri, is/staj havuzu, anket/feedback, bagis ve "
            "sponsorluk, referans adaylari ve uzun vadeli alumni iletisimini yonetir."
        ),
        "kim": [
            ("Alumni Sorumlusu", "Iletisim kampanyalari, mentorluk, etkinlik."),
            ("Mudur", "Bagis + sponsorluk."),
            ("Mezun", "Kendisi profilini gunceller, etkinliklere katilir."),
        ],
        "ana_ozellikler": [
            "Mezun veritabani (her yildan)",
            "Hedef gruplar (5 yil, 10 yil mezunu vs)",
            "Iletisim kampanyalari (email/SMS)",
            "Mentorluk (mezun <> ogrenci)",
            "Etkinlik duzenleme (reunion, konferans)",
            "Is & Staj havuzu (mezun tarafindan acilan)",
            "Anket & Feedback (yaptigi mesleklere gore)",
            "Bagis ve sponsorluk takibi",
            "Tavsiye adaylari (mezun tanidigi)",
        ],
        "sekmeler": [
            ("Dashboard", "Mezun sayisi, bu ay etkinlik, aktif kampanya.", []),
            ("Mezun Veritabani", "Tum mezunlar + filtre + ara.", []),
            ("Hedef Gruplar", "Kampanya icin hedef grup olustur.", []),
            ("Iletisim Kampanyalari", "Email/SMS toplu gonderim.", []),
            ("Mentorluk", "Mezun-ogrenci eslesme.", []),
            ("Etkinlik Duzenle", "Reunion, kariyer gunu vs.", []),
            ("Is & Staj", "Mezunlarin actigi pozisyonlar.", []),
            ("Anket & Feedback", "Mesleklere dair yillik anket.", []),
            ("Bagis & Sponsorluk", "Bagis takibi + sponsorluk teklifi.", []),
            ("Tavsiye Adaylari", "Mezunun tanidigi potansiyel kayit adaylari.", []),
            ("Raporlar", "Mezun istihdam + bagis raporu.", []),
            ("Ayarlar & Sablonlar", "Email sablonlari, kampanya sablonlari.", []),
        ],
        "is_akisi": [
            "Mezuniyet sonrasi: Ogrenciyi Mezun Veritabani'na aktar.",
            "Yilda 1 kez: Mezun profil guncelleme anketi gonder.",
            "Aylik: Ilgili hedef gruba kampanya (ornek '5 yil mezunlari icin reunion').",
            "Mentorluk'te lise son ogrencilerini mezunlara ile eslestir.",
            "Is & Staj havuzundan fakulteye giden ogrencilere staj/is onerisi.",
            "Yil sonu: Bagis & Sponsorluk raporu.",
        ],
        "ipuclari": [
            "Mezunlarla ilisiyi kes KOPMA — yilda en az 2 kez temas (mezun gunu + kariyer gunu).",
            "Mentorluk eslesmesi mezunu geri okulla buluşturur — uzun vadede bagis potansiyeli artar.",
            "Bagis kampanyalari somut bir hedef (ornek 'laboratuvar') belirtince cevap orani %3 kat daha yuksek.",
        ],
        "sss": [
            ("Mezun iletisim bilgisi eski?", "Yillik profil guncelleme anketi gonder."),
        ],
    },

    # ──────────────────── SISTEM (1) ────────────────────
    {
        "section_no": 33, "grup": "SISTEM", "ad": "AI Destek (Smarti AI)", "icon": "🤖",
        "accent": INDIGO, "yeni": False,
        "amac": (
            "AI Destek modulu, SmartCampus'un merkez beyni ve 26 Smarti AI asistaninin kalbidir. "
            "18 modulden veri toplayan yonetici dashboard, AI analiz, sesli/yazili Smarti chatbot, yol "
            "haritasi, sistem saglik durumu ve v2.0 ile gelen Ders Plani Copilot ★ + 23 tab aracini icerir."
        ),
        "kim": [
            ("Mudur/Mudur Yardimcisi", "Yonetici dashboard + AI analiz."),
            ("Ogretmen", "Ders Plani Copilot + Smarti asistan."),
            ("Veli/Ogrenci", "Smarti chat + ses asistani."),
        ],
        "ana_ozellikler": [
            "Yonetici Dashboard (18 modulden agregre)",
            "AI Analiz Raporlari",
            "Yol Haritasi (sistem onerisi)",
            "Smarti Chatbot (yazili)",
            "Sesli Asistan (audio record + TTS)",
            "Genel istatistikler",
            "Sistem Saglik (API logs, cache)",
            "26 Smarti AI asistani",
            "23+ tab araci (Hafiza, Bildirim, Rapor, Veli, Gorev, Analiz, Toplanti, Ses, Transkript, Koc, Gorsel, Bench, Kriz, Gunluk, Duygu, Takvim, Kampus, Tahmin, Agent, Dokuman, Ceviri, Ogretmen, Entegrasyon)",
            "Ders Plani Copilot ★ (v2)",
            "Mood Widget ★",
            "Ogretmen Dashboard + Ogrenci Dashboard ayri gorunum",
        ],
        "sekmeler": [
            ("Yonetici Dashboard", "18 modulden veri + KPI + uyari.",
                ["KPI kartlari incele", "Modul bazli drill-down"]),
            ("AI Analiz Raporlari", "Otomatik uretilen analiz raporlari.", []),
            ("Yol Haritasi", "Sistem onerileri (iyilesme noktalari).", []),
            ("Smarti Chatbot", "Yazili AI asistan.",
                ["Soru yaz", "Cevap al"]),
            ("Sesli Asistan", "Mikrofonla konus + TTS ile dinle.",
                ["Mikrofona bas", "Soru sor", "Sesli cevap"]),
            ("23+ Tab Araci", "Her biri ayri bir Smarti asistani (Hafiza, Bildirim, Rapor vs).",
                ["Arac sec", "Ilgili islemi calistir"]),
            ("Ders Plani Copilot ★", "Ogretmen icin AI ders plani uretici (plan+quiz+etkinlik+slayt+kaynaklar).",
                ["Konu + sinif", "AI uret", "PDF indir / OD'ye aktar"]),
            ("Ogretmen Dashboard", "Ogretmene ozel gorunum (AI onerileri ders).", []),
            ("Ogrenci Dashboard", "Ogrenciye ozel gorunum (bugun ne yapacagim AI).", []),
            ("Genel Istatistikler", "AI kullanim, sorgu sayisi, model performans.", []),
            ("Sistem Saglik", "API logs, cache, yedekleme durumu.", []),
            ("Ayarlar", "OpenAI key, model secimi, TTS, dil.", []),
        ],
        "is_akisi": [
            "Mudur sabah: Yonetici Dashboard > 18 modulden agregre KPI'lar.",
            "AI Analiz Raporlari'nda gunluk rapor oku.",
            "Smarti'ye dogal dilde soru: 'Bu hafta risk altindaki ogrenciler?'",
            "Ogretmen: Ders Plani Copilot ile yarinki dersini 2 dakikada hazirla.",
            "23+ Tab Araci'ndan ilgili olani sec (ornek: 'Toplanti' tutanak ozeti isterken).",
            "Sistem Saglik'i haftalik kontrol et.",
        ],
        "ipuclari": [
            "Smarti'ya daha fazla baglam verirsen daha iyi cevap alirsin — 'Bu ogrencinin matematik dersinde...' gibi.",
            "Ders Plani Copilot ★ ciktisini OD'ye aktarabilirsin — soru ureterek dersi tam sabotla.",
            "OpenAI kota takibini Ayarlar'dan dikkatle yap — musrif kullanim fatura sismesine yol acar.",
        ],
        "sss": [
            ("Smarti yavas cevap veriyor?", "OpenAI API servisi yogun. Gece saatlerinde daha hizli."),
            ("Sesli Asistan mikrofonum ac diyor?", "Tarayici ayarlarinda mikrofon izni ver."),
            ("Ders Plani Copilot yanlis mufredat kullaniyor?", "Sinif + ders + unite parametrelerini tam gir — MEB kazanimi otomatik gelir."),
        ],
    },

    # ══════════════════════════════════════════════════════════════
    # YENI MODULLER (2026-04 eklenen)
    # ══════════════════════════════════════════════════════════════

    {
        "section_no": 34, "grup": "KURUM YONETIMI", "ad": "Odeme Takip", "icon": "💳",
        "accent": HexColor("#F59E0B"), "yeni": True,
        "amac": "Kolej ucret yonetim sistemi. Ogrenci bazli taksit planlari, odeme kayitlari, geciken odeme takibi, veli borc durumu, makbuz uretimi. Kurum gelirlerinin tamamini yonetir.",
        "kim": [("Yonetici", "Taksit plani olusturur, odeme alir, rapor cikarir."), ("Muhasebe", "Gunluk odeme girisi ve geciken takibi."), ("Veli", "Mobil'den borc durumunu goruntuler.")],
        "ana_ozellikler": [
            "Otomatik taksit plani olusturma (10 taksit, ay bazli vade)",
            "Indirim yonetimi (kardes indirimi, basari bursu, tam burs)",
            "Geciken odeme takibi + otomatik uyari",
            "Ucret kalemleri CRUD (ogretim, yemek, servis, kiyafet, etkinlik)",
            "Sinif bazli tahsilat raporu + CSV export",
            "Veli borc durumu (mobil API)",
        ],
        "sekmeler": [
            ("Dashboard", "Toplam borc, odenen, kalan, tahsilat orani metrikleri. Aylik tahsilat grafigi.", []),
            ("Taksit Planlari", "Ogrenci bazli taksit listesi. Her taksit icin odeme alma formu (tutar, yontem, aciklama).", []),
            ("Ucret Kalemleri", "Donem bazli ucret tanimlari. Ogretim, yemek, servis, kiyafet, etkinlik kategorileri.", []),
            ("Yeni Plan Olustur", "Ogrenci sec, donem/tutar/taksit/indirim gir, otomatik vade hesapla.", []),
            ("Odeme Gecmisi", "Tarih ve ogrenci filtreli gecmis kayitlar. CSV export.", []),
            ("Raporlar", "Sinif bazli tahsilat ozeti, geciken odemeler listesi, indirim raporu.", []),
        ],
        "is_akisi": [
            "1. Ucret kalemleri tanimla (yil basinda bir kez)",
            "2. Ogrencilere taksit plani olustur (kayit sirasinda)",
            "3. Aylık odemeler gelince 'Odeme Al' ile kaydet",
            "4. Geciken odemeleri raporla, veli bilgilendir",
            "5. Donem sonu tahsilat raporu cikart",
        ],
        "ipuclari": [
            "Kardes indirimi otomatik hesaplanir — indirim_orani alanina % gir.",
            "Geciken odemeler kirmizi renkle isretlenir — Dashboard'dan hemen gor.",
            "Mobil'den veliler kendi borc durumlarini gorebilir.",
        ],
        "sss": [
            ("Taksit plani nasil degistirilir?", "Taksit Planlari sekmesinden ogrenciyi bul, plani duzenle."),
            ("Odeme iadesi nasil yapilir?", "Odeme Gecmisi'nden ilgili kaydi bul, iptal butonuna bas."),
        ],
    },

    {
        "section_no": 35, "grup": "GENEL", "ad": "Analitik Dashboard", "icon": "📈",
        "accent": HexColor("#3B82F6"), "yeni": True,
        "amac": "Okul geneli analitik dashboard. Ogrenci performansi, devamsizlik analizi, ogretmen metrikleri, sinif karsilastirmasi. Plotly grafikleri ile goruntuler.",
        "kim": [("Yonetici", "Okul geneli performans analizi."), ("Mudur", "Donem sonu karsilastirma."), ("Koordinator", "Sinif bazli takip.")],
        "ana_ozellikler": [
            "Genel bakis (ogrenci/ogretmen/sinif sayilari, cinsiyet dagilimi)",
            "Akademik performans (sinif ortalamasi, top 10, ders bazli)",
            "Devamsizlik analizi (sinif/gun/ay bazli trend)",
            "Ogretmen performans metrikleri",
            "Iki sinif yan yana karsilastirma",
        ],
        "sekmeler": [
            ("Genel Bakis", "4 metrik karti + cinsiyet pie chart + sinif dagilimi bar chart.", []),
            ("Akademik Performans", "Sinif ortalamasi, top 10 ogrenci, ders bazli karsilastirma.", []),
            ("Devamsizlik Analizi", "Aylik trend, gun bazli pattern (hangi gun en cok devamsizlik).", []),
            ("Ogretmen Performans", "Brans dagilimi, sinif basina ogretmen, ogrenci basari ortalamasi.", []),
            ("Karsilastirma", "Iki sinif sec — yan yana ortalama, devamsizlik, ders bazli grafik.", []),
        ],
        "is_akisi": ["1. Donem sonunda Analitik Dashboard'u ac", "2. Sinif karsilastirmasi yap", "3. Raporlari indir"],
        "ipuclari": ["Plotly grafikleri interaktiftir — ustune gel, detay gor.", "Karsilastirma sekmesinde ayni sinifin iki donemini de karsilastirabilirsin."],
        "sss": [("Grafik gorunmuyor?", "Plotly paketi yuklu olmalidir: pip install plotly")],
    },

    {
        "section_no": 36, "grup": "ILETISIM & RANDEVU", "ad": "Veli-Ogretmen Gorusme", "icon": "👨‍👩‍👦",
        "accent": HexColor("#8B5CF6"), "yeni": True,
        "amac": "Veli-ogretmen gorusme randevu sistemi. Slot bazli randevu, cakisma kontrolu, gorusme notlari, puanlama.",
        "kim": [("Veli", "Gorusme talebi olusturur."), ("Ogretmen", "Onaylar, gorusme notu yazar."), ("Yonetici", "Tum gorusmeleri izler.")],
        "ana_ozellikler": ["Haftalik gorusme takvimi", "Cakisma kontrolu", "Gorusme sonrasi puanlama (1-5)", "Konu bazli istatistik"],
        "sekmeler": [
            ("Gorusme Takvimi", "Bu haftanin gorusmeleri, durum badge'leri.", []),
            ("Yeni Talep", "Ogretmen/tarih/saat/konu secimi, cakisma kontrolu.", []),
            ("Gecmis", "Tamamlanan gorusmeler, notlar, puanlama.", []),
            ("Istatistik", "Toplam gorusme, konu dagilimi pie chart, trend.", []),
        ],
        "is_akisi": ["1. Veli gorusme talebi olusturur", "2. Ogretmen onaylar", "3. Gorusme yapilir, not yazilir", "4. Veli puanlar"],
        "ipuclari": ["Ayni saat+ogretmen icin cakisma otomatik engellenir."],
        "sss": [("Gorusme iptal nasil yapilir?", "Takvim'den ilgili gorusmeyi bul, iptal butonuna tikla.")],
    },

    {
        "section_no": 37, "grup": "AKADEMIK", "ad": "Sertifika Uretici", "icon": "🏆",
        "accent": HexColor("#C5962E"), "yeni": True,
        "amac": "Sertifika ve belge uretim sistemi. 7 sablon, HTML onizleme, ReportLab PDF, toplu uretim + ZIP.",
        "kim": [("Yonetici", "Toplu sertifika uretir."), ("Ogretmen", "Ogrenci bazli belge olusturur."), ("Koordinator", "Donem sonu basari belgeleri.")],
        "ana_ozellikler": ["7 sertifika sablonu", "HTML onizleme", "ReportLab PDF", "Toplu uretim + ZIP", "Sertifika arsivi"],
        "sekmeler": [
            ("Sertifika Olustur", "Sablon sec, ogrenci sec, onizle, PDF uret.", []),
            ("Toplu Sertifika", "Sinif sec, tum ogrencilere batch uret, ZIP indir.", []),
            ("Arsiv", "Gecmis sertifikalar, filtre, yeniden indirme.", []),
        ],
        "is_akisi": ["1. Sablon sec (Basari/Katilim/Takdir/...)", "2. Ogrenci sec", "3. Onizle, PDF uret", "4. Indir veya yazdir"],
        "ipuclari": ["Toplu sertifika ile tum sinifa tek tikla uret."],
        "sss": [("PDF bozuk gorunuyor?", "ReportLab yuklu olmalidir: pip install reportlab")],
    },

    {
        "section_no": 38, "grup": "OKUL YASAMI", "ad": "Servis GPS Takip", "icon": "🚌",
        "accent": HexColor("#0EA5E9"), "yeni": True,
        "amac": "Okul servisi takip sistemi. Canli harita, guzergah CRUD, ogrenci atama, doluluk raporu.",
        "kim": [("Yonetici", "Guzergah ve atama yonetimi."), ("Veli", "Mobil'den servis durumunu gorur."), ("Servis Sorumlusu", "Canli takip ve raporlama.")],
        "ana_ozellikler": ["Canli konum haritasi (st.map)", "Guzergah CRUD", "Ogrenci-servis atama", "Doluluk raporu"],
        "sekmeler": [
            ("Canli Takip", "Harita + servis kartlari + durum badge.", []),
            ("Guzergah Yonetimi", "Ekle/duzenle/sil (plaka, sofor, kapasite).", []),
            ("Ogrenci Atama", "Servise ogrenci ata/cikar.", []),
            ("Raporlar", "Doluluk orani + performans.", []),
        ],
        "is_akisi": ["1. Guzergahlari tanimla", "2. Ogrencileri ata", "3. Canli takip ile izle"],
        "ipuclari": ["Doluluk %90 ustu olunca uyari verir."],
        "sss": [("GPS gercek mi?", "Simule edilmis koordinatlar. Gercek GPS icin 3. parti entegrasyon gerekir.")],
    },

    {
        "section_no": 39, "grup": "OKUL YASAMI", "ad": "Kutuphane Barkod", "icon": "📚",
        "accent": HexColor("#059669"), "yeni": True,
        "amac": "Kutuphane barkod/kitap yonetim sistemi. Arama, odunc, iade, envanter, barkod uretici.",
        "kim": [("Kutuphane Sorumlusu", "Odunc/iade/envanter yonetimi."), ("Ogretmen", "Kitap onerisi ve takip."), ("Ogrenci", "Kitap arama ve odunc.")],
        "ana_ozellikler": ["Kitap arama (baslik/yazar/ISBN)", "Odunc verme + iade", "Gecikme ucreti (2 TL/gun)", "Barkod etiketi uretici"],
        "sekmeler": [
            ("Kitap Arama", "Baslik/yazar/ISBN/kategori ile ara.", []),
            ("Odunc Ver", "Kitap + ogrenci sec, tarih belirle.", []),
            ("Iade Al", "Odunc listesi, iade butonu, gecikme hesabi.", []),
            ("Envanter", "Toplam/odunc/mevcut + kategori grafigi.", []),
            ("Barkod Uretici", "Secilen kitaplara barkod etiketi.", []),
        ],
        "is_akisi": ["1. Kitap kaydet", "2. Odunc ver", "3. Iade al", "4. Gecikmeleri takip et"],
        "ipuclari": ["20 ornek kitap otomatik yuklenir."],
        "sss": [("Barkod okuyucu lazim mi?", "Hayir, ISBN elle girilebilir. Barkod okuyucu opsiyoneldir.")],
    },

    {
        "section_no": 40, "grup": "OKUL YASAMI", "ad": "Yemek Tercihi ve Alerji", "icon": "🍽️",
        "accent": HexColor("#EF4444"), "yeni": True,
        "amac": "Ogrenci yemek tercihi ve alerji takip sistemi. 5 diyet turu, 11 alerjen, haftalik menu planlama, cakisma kontrolu.",
        "kim": [("Yonetici", "Alerji raporlari ve menu onayı."), ("Yemekhane", "Menu planlama, cakisma kontrolu."), ("Veli", "Tercih ve alerji bildirimi.")],
        "ana_ozellikler": ["5 diyet turu", "11 alerjen takibi", "Haftalik menu editoru", "Alerji cakisma kontrolu", "Kritik alerji uyari"],
        "sekmeler": [
            ("Tercihler", "Ogrenci listesi + diyet/alerji formu.", []),
            ("Alerji Raporu", "Alerjen bazli sayilar, kritik uyarilar, CSV export.", []),
            ("Menu Planlama", "5 gun x 4 ogel, alerji cakisma kontrolu.", []),
            ("Istatistik", "Diyet dagilimi + alerji grafikleri.", []),
        ],
        "is_akisi": ["1. Ogrenci alerjilerini kaydet", "2. Haftalik menu planla", "3. Cakisma kontrolu yap", "4. Alerji raporunu paylas"],
        "ipuclari": ["Fistik ve kabuklu deniz urunleri 'kritik' olarak isaretlenir — kirmizi uyari karti cikar."],
        "sss": [("Yeni alerjen eklenebilir mi?", "Evet, tercih formundaki 'Diger' alanina yaz.")],
    },
])
