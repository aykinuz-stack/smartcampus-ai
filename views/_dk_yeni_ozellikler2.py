"""Dijital Kutuphane - 10 Yeni Ozellik (Part 2: 6-10)"""
import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime, date


# ============================================================
# 6. DIJITAL DERGI KOSESI
# ============================================================
def render_dijital_dergi():
    """SmartCampus e-Dergi - Aylik Dijital Dergi Sistemi"""

    ISSUES = [
        {
            "month": "Eylul 2025", "sayi": 1, "tema": "Okula Donus",
            "kapak_emoji": "\U0001f392", "kapak_renk": "#2563eb",
            "editorial": "Yeni egitim ogretim yilina merhaba! Bu sayimizda beynimizin ogrenme mekanizmalarindan yapay zekanin egitimdeki rolune, sonbahar gocunden dunya edebiyatina kadar genis bir yelpazede sizlerle bulusuyoruz. Keyifli okumalar!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Beynimiz Nasil Ogrenir?",
                    "content": [
                        "Insan beyni yaklasik 86 milyar norondan olusur ve bu noronlar arasindaki sinaptik baglantilar ogrenmenin temelini olusturur. Noroplastisite adi verilen bu ozellik sayesinde beyin, yeni deneyimlerle surekli yeniden sekillenir. Her yeni bilgi ogrendigimizde noronlar arasinda yeni baglantilar kurulur veya mevcut baglantilar guclenir.",
                        "Hafiza olusumu uc temel asamadan gecer: kodlama, depolama ve geri cagirma. Kisa sureli hafiza yaklasik 20-30 saniye bilgi tutabilirken, tekrar ve anlam yukleme ile bilgiler uzun sureli hafizaya aktarilir. Uyku sirasinda beyin, gun icerisinde ogrenilenlerini konsolide ederek kalici hafizaya deger.",
                        "Etkili calisma teknikleri arasinda aralikli tekrar (spaced repetition), aktif geri cagirma (active recall) ve interleaving (konular arasi gecis) one cikar. Arastirmalar, bir konuyu tek seferde uzun sure calismak yerine, aralikli kisa seanslar halinde calismanin ogrenmeyi yuzde 50'ye kadar artirabildigini gostermektedir.",
                        "Norobilimdeki son gelismeler, egzersizin beyinde BDNF (Brain-Derived Neurotrophic Factor) salgilanmasini artirarak ogrenme kapasitesini yukselttigini ortaya koymustur. Gunluk 30 dakikalik aerobik egzersiz, hipokampusteki noron uretimini hizlandirarak hafiza performansini iyilestirir."
                    ],
                    "quiz": [
                        {"q": "Beynin yeni deneyimlerle yeniden sekillenmesine ne ad verilir?", "opts": ["Noroplastisite", "Noroloji", "Sinaptogenez", "Miyelinizasyon"], "answer": 0},
                        {"q": "Aralikli tekrar teknigi ogrenmeyi yaklasik ne kadar artirabilir?", "opts": ["%10", "%25", "%50", "%75"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Yapay Zeka ve Egitimin Gelecegi",
                    "content": [
                        "Yapay zeka destekli egitim sistemleri, her ogrencinin ogrenme hizina ve stiline uyum saglayabilen kisisellestirilmis ogrenme deneyimleri sunmaktadir. AI tutorlar, ogrencilerin guclu ve zayif yonlerini analiz ederek bireysel ogrenme planlari olusturabilir.",
                        "Adaptif ogrenme platformlari, ogrencinin performansina gore zorluk seviyesini otomatik ayarlar. Bir ogrenci bir konuda zorlandiginda sistem ek aciklamalar ve pratik sorular sunarken, konuyu kavrayan ogrencilere daha ileri seviye icerikler onerır.",
                        "Dogal dil isleme teknolojileri sayesinde AI sistemleri artik ogrencilerin acik uclu yanitlarini degerlendirebilir, yazim hatalarini duzeltebilir ve hatta yaratici yazma konusunda geri bildirim verebilir. Bu teknoloji ogretmenlerin is yukunu azaltirken ogrencilere aninda geri donus saglar.",
                        "Gelecegin siniflarinda AI, ogretmenin yerini almak yerine onu destekleyen bir asistan rolu ustlenecektir. Ogretmenler rutın degerlendirme islerinden kurtularak ogrencilerle bire bir ilgilenmeye, motivasyon saglamaya ve kritik dusunme becerilerini gelistirmeye daha fazla zaman ayirabilecektir."
                    ],
                    "quiz": [
                        {"q": "Adaptif ogrenme platformlari neye gore zorluk seviyesini ayarlar?", "opts": ["Ogrenci yasina", "Ogrenci performansina", "Sinif ortalamasina", "Ogretmen tercihine"], "answer": 1},
                        {"q": "Gelecekte AI'nin egitimdeki rolu ne olacaktir?", "opts": ["Ogretmenlerin yerini almak", "Ogretmeni destekleyen asistan", "Sadece sinav yapmak", "Sadece odev kontrol etmek"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Sonbahar Gocu - Kuslar Nereye Gidiyor?",
                    "content": [
                        "Her sonbahar, dunyada yaklasik 50 milyar kus goc yolculuguna cikar. Bu inanilmaz yolculuklar sirasinda bazi turler 10.000 kilometreden fazla mesafe kat eder. Kuzey Kutbu sumru kusu, her yil Kuzey Kutbu'ndan Guney Kutbu'na ve geri donerek yaklasik 70.000 km yol alan sampiyondur.",
                        "Kuslarin navigasyon yetenekleri bilim insanlarini hala sasirtmaktadir. Gocmen kuslar yonlerini bulmak icin Dunya'nin manyetik alanini, gunes ve yildizlarin konumunu ve hatta koku duyularini kullanir. Gagalarindaki manyetit kristalleri bir tur dahili pusula gorevi gorur.",
                        "Turkiye, Avrupa ile Afrika arasindaki en onemli goc yollarindan birinin uzerinde yer alir. Istanbul Bogazı, her sonbahar binlerce yirtici kusun gecis noktasidir. Leylekler, kartaIlar ve atmacalar termal hava akimlariyi kullanarak minimum enerjiyle bu yolculugu tamamlar.",
                        "Iklim degisikligi goc paternlerini degistirmektedir. Bazi turler daha erken goc ederken, bazilari kis mevsimini daha kuzeyde gecirmeye baslamistir. Bu degisimler ekosistemdeki besin zincirleri ve tozlasma surecleri uzerinde onemli etkilere sahiptir."
                    ],
                    "quiz": [
                        {"q": "Hangi kus turu yillik en uzun goc mesafesini kat eder?", "opts": ["Leylek", "Kuzey Kutbu sumru kusu", "Kaz", "Flamingo"], "answer": 1},
                        {"q": "Kuslar yonlerini bulmak icin asagidakilerden hangisini kullanMAZ?", "opts": ["Manyetik alan", "Yildiz konumlari", "Sicaklik farklari", "Koku duyusu"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Dunyanin En Eski Universiteleri",
                    "content": [
                        "Dunyanin en eski surekli faaliyet gosteren universitesi, 859 yilinda Fas'in Fez sehrinde kurulan El-Karaviyyin Universitesi'dir. Fatima el-Fihri tarafindan kurulan bu universite, UNESCO tarafindan da taninmaktadir. Matematikten astronomiye kadar pek cok alanda egitim verilmistir.",
                        "Avrupa'nin en eski universitesi 1088 yilinda kurulan Bologna Universitesi'dir. Hukuk egitimi ile un kazanan bu kurum, modern universite kavraminin temellerini atmistir. Oxford Universitesi ise 1096'dan beri egitim vermekte olup, Ingilizce konusulan dunyanin en eski universitesidir.",
                        "El-Ezher Universitesi 970 yilinda Kahire'de kurulmus ve Islam dunyasinin en prestijli egitim kurumlarindan biri olmustur. Orta Cag'da bu universiteler, bilginin korunmasi ve aktarilmasinda kritik bir rol oynamislardir. Antik Yunan eserlerinin Arapca'ya cevirisi buralarda gerceklestirilmistir.",
                        "Bu eski universiteler modern yuksekogretimin temel taslarini olusturmustur. Diploma sistemi, fakulte yapisi, akademik ozgurluk ve arastirma gelenegı gibi kavramlarin kokleri bu kurumlara dayanir."
                    ],
                    "quiz": [
                        {"q": "Dunyanin en eski surekli faaliyet gosteren universitesi hangisidir?", "opts": ["Oxford", "Bologna", "El-Karaviyyin", "El-Ezher"], "answer": 2},
                        {"q": "Bologna Universitesi hangi alanda un kazanmistir?", "opts": ["Tip", "Hukuk", "Matematik", "Felsefe"], "answer": 1}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dunya Cocuk Edebiyatinin Donum Noktalari",
                    "content": [
                        "Cocuk edebiyatinin tarihi, 1658'de Jan Amos Comenius'un yazdigi 'Orbis Pictus' adli resimli ansiklopediye kadar uzanir. Bu eser, cocuklar icin ozel olarak tasarlanmis ilk kitap kabul edilir. Ancak cocuk edebiyatinin altın cagi 19. yuzyilda baslamistir.",
                        "Lewis Carroll'in 1865'te yazdigi 'Alice Harikalar Diyarinda' cocuk edebiyatinda bir devrim yaratti. Ilk kez bir cocuk kitabi salt egitim amaci gutmeden, hayal gucu ve eglenceyi on plana cıkardi. Hans Christian Andersen'in masallari da ayni donemde dunya edebiyatina damgasini vurdu.",
                        "20. yuzyilda Antoine de Saint-Exupery'nin 'Kucuk Prens'i (1943), J.R.R. Tolkien'in 'Hobbit'i (1937) ve Astrid Lindgren'in 'Pippi Uzuncorap'i (1945) cocuk edebiyatina yeni boyutlar kazandirdi. Bu eserler hem cocuklara hem yetiskinlere hitap eden evrensel temalar isledi.",
                        "Turk cocuk edebiyati da zengin bir gelenlege sahiptir. Tevfik Fikret'in 'Sis' ve 'Haluk'un Defteri' eserleri, Eflatun Cem Guney'in derlediği masallar ve Muzaffer Izgü'nun kitaplari Turk cocuklarinin edebiyat dunyasina acilan kapilarini olusturmustur."
                    ],
                    "quiz": [
                        {"q": "'Orbis Pictus' eseri hangi yilda yazilmistir?", "opts": ["1658", "1765", "1865", "1543"], "answer": 0},
                        {"q": "'Alice Harikalar Diyarinda' hangi yazar tarafindan yazilmistir?", "opts": ["Hans C. Andersen", "Lewis Carroll", "J.R.R. Tolkien", "A. de Saint-Exupery"], "answer": 1}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Yeni Sezon Basliyor - Olimpiyat Sporlari Rehberi",
                    "content": [
                        "Modern Olimpiyat Oyunlari 1896 yilinda Atina'da basladi ve bugün 200'den fazla ulkeden 10.000'i askin sporcuyu bir araya getirmektedir. Yaz Olimpiyatlari'nda 32 farkli spor dalinda yarisma yapilir. Her dort yilda bir duzenlenen bu organizasyon, dunyanin en buyuk spor etkinligidir.",
                        "Atletizm, yuzme ve jimnastik Olimpiyatlarin en cok takip edilen brans laridir. Usain Bolt'un 100 metredeki 9.58 saniyelik dunya rekoru, Michael Phelps'in 23 altin madalyasi gibi basarilar spor tarihine altin harflerle yazilmistir.",
                        "Son yillarda Olimpiyat programina kaykay, sorf, spor tirmanisi ve breakdans gibi yeni dallar eklenmistir. Bu degisim, genc nesillerin ilgisini cekmek ve Olimpiyat ruhunu canli tutmak amaciyla yapilmistir.",
                        "Turkiye, Olimpiyat tarihinde gures, halter ve tekvando dallarinda buyuk basarilar elde etmistir. Naim Suleymanoglu, Halil Mutlu ve Servet Tazegul gibi sporcular ulkemizi Olimpiyat sampiyonluguna tasimistir."
                    ],
                    "quiz": [
                        {"q": "Modern Olimpiyat Oyunlari ilk olarak hangi sehirde duzenlenmistir?", "opts": ["Paris", "Londra", "Atina", "Roma"], "answer": 2},
                        {"q": "Michael Phelps kac Olimpiyat altin madalyasi kazanmistir?", "opts": ["18", "21", "23", "28"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Ekim 2025", "sayi": 2, "tema": "Bilim ve Kesif",
            "kapak_emoji": "\U0001f9ea", "kapak_renk": "#7c3aed",
            "editorial": "Ekim sayimizda bilimin ve kesfin izinde yola cikiyoruz. Nobel Odullerinden uzayin derinliklerine, piramitlerin gizeminden futbolun tarihine uzanan bir yolculuga hazir olun!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Nobel Odulleri 2025 - Kim, Neden Kazandi?",
                    "content": [
                        "Nobel Odulleri, Isvecli mucit Alfred Nobel'in vasiyetiyle 1901'den beri her yil insanliga en buyuk katkiyi yapan kisilere verilmektedir. Fizik, kimya, fizyoloji veya tip, edebiyat, baris ve ekonomi dallarinda verilen oduller, bilim dunyasinin en prestijli onurlandirmasidir.",
                        "Nobel Fizik Odulu genellikle evrenin temel yasalarini anlamaya yonelik calismalara verilir. Kuantum fiziği, parcacik fizigi ve astrofizik alanlari son yillarda one cikan konular olmustur. 2022'de kuantum dolaniklık uzerine calismalara verilen odul buyuk yanki uyandirmistir.",
                        "Nobel Tip Odulu, insan sagligina dogrudan etki eden kesiflerı odullendirir. mRNA asi teknolojisi, gen duzenleme (CRISPR) ve bagisiklik sistemi uzerine calismalar son yillarin one cikan konularıdır. Bu kesifler milyonlarca insanin hayatini kurtarma potansiyeline sahiptir.",
                        "Turkiye'den Prof. Dr. Aziz Sancar, 2015 yilinda DNA onarim mekanizmalari uzerine calismalariyla Nobel Kimya Odulu'nu kazanmistir. Bu basari, Turk bilim insanlarinin dunya sahnesindeki yeteneklerini bir kez daha kanitlamistir."
                    ],
                    "quiz": [
                        {"q": "Nobel Odulleri ilk olarak hangi yil verilmeye baslanmistir?", "opts": ["1895", "1901", "1910", "1920"], "answer": 1},
                        {"q": "Aziz Sancar hangi alanda Nobel Odulu almistir?", "opts": ["Fizik", "Tip", "Kimya", "Baris"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Uzay Teleskoplari - James Webb'in Kesifleri",
                    "content": [
                        "James Webb Uzay Teleskobu (JWST), 2021 yilinda firlatilan ve 10 milyar dolar maliyetle insa edilen insanligin en gelismis uzay gozlemevıdir. Hubble'in halefi olarak tasarlanan JWST, kizilotesi dalga boyunda calisarak evrenin en derin koselerini goruntuleyebilir.",
                        "JWST'nin 6.5 metrelik altin kapli aynasi, Hubble'inkinden 6 kat daha genis yuzey alanina sahiptir. Teleskop, Dunya'dan 1.5 milyon km uzaktaki L2 Lagrange noktasinda konumlanmis olup, gunes isigındn korunmak icin tenis kortu buyuklugunde bir gunes kalkani kullanir.",
                        "Teleskobun ilk goruntulerı bilim dunyasini heyecanlandirmistir. Ilk galaksilerin olusumunu, yildiz dogum bulutsuIarinin ic yapisini ve otegezegenlerın atmosfer bileşimini inceleyebilmektedir. TRAPPIST-1 sistemindeki kayalik gezegenlerin atmosferinde su buhari izleri tespit edilmistir.",
                        "JWST, Buyuk Patlama'dan sadece birkaç yuz milyon yil sonra olusan galaksileri goruntulemeyi basarmistir. Bu kesifler, evrenin ilk donemlerine dair bilgilerimizi kokten degistirmekte ve kozmoloji teorilerinin yeniden gozden gecirilmesini gerektirmektedir."
                    ],
                    "quiz": [
                        {"q": "James Webb Uzay Teleskobu hangi dalga boyunda calisir?", "opts": ["Morötesi", "Kizilotesi", "X-isini", "Radyo dalgasi"], "answer": 1},
                        {"q": "JWST'nin aynasi kac metre capindadir?", "opts": ["2.4 m", "4.0 m", "6.5 m", "10.0 m"], "answer": 2}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Sonbahar Ormanlari ve Yaprak Dokme Bilimi",
                    "content": [
                        "Sonbaharda yapraklarin renk degistirmesi, dogadaki en gorkemli gorunumlerden birini olusturur. Bu degisim aslinda bir kimyasal surecin sonucudur. Gun isiginin kisalmesiyla birlikte yapraklardaki klorofil parcalanmaya baslar ve alttaki sari, turuncu pigmentler (karotenoidler) ortaya cikar.",
                        "Kirmizi ve mor renkler ise antosiyanin adli pigmentlerden gelir. Bu pigmentler sonbaharda yapraklarda yeni uretilir. Bilim insanlari antosiyaninlerin yapraklari gunes hasarindan koruyarak agacin son dakikaya kadar besin maddelerini geri cekebilmesini sagladigini dusunmektedir.",
                        "Yaprak dokme (abscission) sureci, agaclarin kis hazirlıginın kritik bir parcasidir. Agaclar, yaprak sapinin tabaninda ozel bir ayrilma tabakasi olusturur. Bu tabaka yaprak ile dal arasindaki su ve besin akisini keser, yaprak sonunda duser.",
                        "Dokulen yapraklar orman tabaninda ayrisarak zengin humus tabakasini olusturur. Bu dogal geri donusum sureci, toprak verimliligi icin hayati onem tasir. Bir hektar yaprakli orman yilda yaklasik 5-8 ton yaprak dokuntisi uretir."
                    ],
                    "quiz": [
                        {"q": "Sonbaharda yapraklardaki sari renk hangi pigmentten gelir?", "opts": ["Klorofil", "Antosiyanin", "Karotenoid", "Melanin"], "answer": 2},
                        {"q": "Yaprak dokme surecine ne ad verilir?", "opts": ["Fotosentez", "Transpirasyon", "Abscission", "Osmoz"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Antik Misir'in Gizemli Piramitleri",
                    "content": [
                        "Giza Piramitleri yaklasik 4.500 yil once insa edilmis olup, Antik Dunyanin Yedi Harikasi'ndan gunumuze ulasan tek yapidir. Buyuk Piramit (Keops), 146 metre yuksekliginde ve yaklasik 2.3 milyon tas bloktan olusur. Her blok ortalama 2.5 ton agirligindadir.",
                        "Piramitlerin nasil insa edildigi hala tartisma konusudur. En yaygin teori, rampa sistemi kullanildigini one surer. Isçilerin carklar, kizaklar ve su ile islatiImiş kum uzerinde taslari kaydirdiği dusunulmektedir. Yaklasik 20-30 yil suren bir insaat sureci on binlerce iscinin koordineli calismasini gerektirmistir.",
                        "Piramitler sadece mezar yapilari degil, ayni zamanda astronomik gozlemevleri olarak da islevseldi. Buyuk Piramit'in kenarları neredeyse mukemmel bir sekilde kuzey-guney ve dogu-bati yonlerine hizalanmistir. Icindeki dar kanallar belirli yildizlara isaret eder.",
                        "Modern teknoloji piramitlerin gizemlerini aydinlatmaya devam etmektedir. Muon tomografisi ile 2017'de Buyuk Piramit'in icerisinde daha once bilinmeyen buyuk bir bosluk kesfedilmistir. Bu kesif, piramitlerin hala sirlariyla dolu oldugunu gostermektedir."
                    ],
                    "quiz": [
                        {"q": "Buyuk Piramit yaklasik kac tas bloktan olusur?", "opts": ["500 bin", "1 milyon", "2.3 milyon", "5 milyon"], "answer": 2},
                        {"q": "2017'de piramit icerisinde ne kesfedilmistir?", "opts": ["Yeni bir oda", "Hazine", "Bilinmeyen bosluk", "Giris tuneli"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dunya Muzik Tarihi - Klasikten Moderne",
                    "content": [
                        "Muzik, insanlik tarihinin en eski sanat formlarindan biridir. 40.000 yil oncesine ait kemik flutler, muzigın Paleolitik Cag'a kadar uzandigini gosterir. Antik Yunan'da muzik matematik ve felsefe ile ic ice bir disiplindi; Pisagor, muzik aralikIarinin matematiksel oranlarini kesfetmistir.",
                        "Klasik muzik donemi 1750-1820 yillari arasinda doruguna ulasti. Mozart, Beethoven ve Haydn bu donemin dev isimleridir. Beethoven'in 9. Senfonisi, isitme kaybina ragmen besteledigi bir basyapittir ve bugun Avrupa Birligi marsi olarak da kullanilmaktadir.",
                        "20. yuzyil muzik tarihinde buyuk bir devrim donemidir. Caz, blues, rock and roll, pop ve hip-hop gibi turler birbirini izleyerek ortaya cikmistir. Elvis Presley, Beatles, Michael Jackson ve daha niceleri muzik tarihinin akisini degistirmistir.",
                        "Dijital cag muzik uretim ve tuketim bicimlerini kokten degistirmistir. Streaming platformlari sayesinde dunyadakı tum muziğe aninda erisim mumkun hale gelmistir. Yapay zeka ile muzik besteleyen algoritmalar da artik gerceklige donusmustur."
                    ],
                    "quiz": [
                        {"q": "Bilinen en eski muzik aletleri ne kadar eskidir?", "opts": ["5.000 yil", "15.000 yil", "40.000 yil", "100.000 yil"], "answer": 2},
                        {"q": "Beethoven'in 9. Senfonisi bugun hangi amacla da kullanilir?", "opts": ["ABD marsi", "BM marsi", "AB marsi", "Olimpiyat marsi"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Futbolun Tarihi - Ilk Mactan Dunya Kupasina",
                    "content": [
                        "Modern futbolun kurallari 1863 yilinda Ingiltere'de kurulan Football Association tarafindan belirlenmistir. Ancak top oynama geleneği cok daha eskidir; Cin'de MO 2. yuzyilda oynanan 'cuju', bilinen en eski futbol benzeri oyundur.",
                        "Ilk resmi uluslararasi futbol maci 1872'de Ingiltere ile Iskocya arasinda oynandi ve 0-0 bitti. FIFA 1904'te Paris'te kuruldu ve ilk Dunya Kupasi 1930'da Uruguay'da duzenlendi. Ev sahibi Uruguay sampiyonlugu kazandi.",
                        "Pele, Maradona, Cruyff, Zidane, Messi ve Ronaldo gibi isimler futbol tarihinin en buyuk oyunculari arasinda yer alir. Pele uç Dunya Kupasi kazanan tek futbolcudur. Maradona'nin 1986 Dunya Kupasi'ndaki 'Tanri'nin Eli' golu tarihın en tartismali anlarindan biridir.",
                        "Turkiye, 2002 Dunya Kupasi'nda ucunculuk elde ederek futbol tarihindeki en buyuk basarisini yakalamiştir. Hakan Sukur'un Guney Kore'ye karsi 11. saniyede attigi gol, Dunya Kupasi tarihinin en erken golu olarak kayitlara gecmistir."
                    ],
                    "quiz": [
                        {"q": "Ilk FIFA Dunya Kupasi hangi yil duzenlenmistir?", "opts": ["1920", "1926", "1930", "1934"], "answer": 2},
                        {"q": "Hakan Sukur'un Dunya Kupasi'ndaki rekor golu kacinci saniyede atilmistir?", "opts": ["8", "11", "15", "22"], "answer": 1}
                    ]
                }
            ]
        },
        {
            "month": "Kasim 2025", "sayi": 3, "tema": "Teknoloji Cagi",
            "kapak_emoji": "\U0001f916", "kapak_renk": "#059669",
            "editorial": "Kasim sayimizda teknolojinin dunumuzu ve gelecegimizi nasil seklillendirdigini kesfediyoruz. Robotlardan siber guvenlige, volkanlardan e-spora kadar heyecan verici konularla karsinızdayız!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Robotik ve Otomasyon - Gelecegin Fabrikalari",
                    "content": [
                        "Endustriyel robotlar 1961'de General Motors fabrikasinda kullanilmaya baslanmistir. Bugün dunya genelinde 3 milyondan fazla endustriyel robot faaliyet gostermektedir. Japonya, Guney Kore ve Almanya robot yogunlugu en yüksek ulkeler arasindadir.",
                        "Modern fabrikalar 'akilli uretim' konseptiyle calisir. IoT sensorleri, yapay zeka ve robotlar bir arada calısarak uretim sureclerini optimize eder. Isbirlıkci robotlar (cobot'lar) insanlarla ayni ortamda guvenli sekilde calisabilir.",
                        "Robotik cerrahi, tip alaninda devrim yaratmistir. Da Vinci cerrahi robotu, cerrahlarin milimetre hassasiyetinde ameliyat yapmasini saglar. Nanobotlar ise gelecekte kan dolasimina girip hastalikli hucreleri hedefleyebilecektir.",
                        "Insansi robotlar (humanoid) gunluk hayata girmeye baslamıstir. Boston Dynamics'in Atlas robotu arka takla atabilirken, Tesla'nin Optimus robotu basit ev islerini yapmayi hedeflemektedir. 2030'a kadar insansi robotlarin yasli bakimi ve egitimde kullanilmasi beklenmektedir."
                    ],
                    "quiz": [
                        {"q": "Ilk endustriyel robot hangi yil kullanilmaya baslanmistir?", "opts": ["1945", "1961", "1975", "1990"], "answer": 1},
                        {"q": "Insanlarla ayni ortamda calisan robotlara ne ad verilir?", "opts": ["Android", "Cobot", "Humanoid", "Cyborg"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Siber Guvenlik - Internette Guvenli Kalma",
                    "content": [
                        "Siber saldirilar her yil artmakta olup, 2024'te dunya genelinde siber suc maliyetinin 10.5 trilyon dolari asmasi beklenmektedir. Phishing (oltalama), ransomware (fidye yazilimi) ve DDoS saldirilari en yaygin siber tehditler arasindadir.",
                        "Guclu sifre kullanimi siber guvenligin temelidir. Bir sifrenin en az 12 karakter uzunlugunda olmasi, buyuk-kucuk harf, rakam ve ozel karakter icermesi onerilir. Iki faktorlu kimlik dogrulama (2FA) hesap guvenligini onemli olcude arttirir.",
                        "Sosyal muhendislik saldirilari, teknolojiden cok insan psikolojisini hedef alir. Dolandiricilar, guven olusturarak kisisel bilgileri ele gecirmeye calisir. E-posta, telefon veya sosyal medya üzerinden gelen supheli mesajlara karsi dikkatli olunmalidir.",
                        "VPN (Sanal Ozel Ag) kullanimi, özellikle acik Wi-Fi aglarinda internet trafiginizi sifrelemenize yardimci olur. Yazilimlari guncel tutmak, guveniIir antiviurs programlari kullanmak ve duzenli yedekleme yapmak temel guvenlik onlemleridir."
                    ],
                    "quiz": [
                        {"q": "Asagidakilerden hangisi bir siber saldiri turu degildir?", "opts": ["Phishing", "Ransomware", "Firewall", "DDoS"], "answer": 2},
                        {"q": "Guclu bir sifre en az kac karakter olmalidir?", "opts": ["6", "8", "10", "12"], "answer": 3}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Volkanlar - Yeryzunun Atesli Nefesi",
                    "content": [
                        "Dunya uzerinde yaklasik 1.500 aktif volkan bulunmaktadir. Bu volkanlarin cogu 'Ates Cemberi' olarak bilinen Pasifik Okyanusu cevresi boyunca siralannistir. Her yil yaklasik 50-70 volkan patlama gerceklestirir.",
                        "Volkanlar, Dunya'nin ic yapisini anlamamiza yardimci olur. Magma, yeryuzunun mantodan gelen erimis kayalardan olusur. Lav olarak yuzeye ciktiginda sicakligi 700-1200 derece Celsius arasinda degisir. Volkanik kayaclar jeolojik tarihin onemli kayitlarini icerir.",
                        "1883 Krakatoa patlamasi tarihın en siddetli volkanik olaylarindan biridir. Patlama sesi 5.000 km uzaktan duyulmus, tsunami dalgalari 36.000 kisibin olmune yol acmistir. Atmosfere yayilan kul, dunya genelinde sicakliklari 1.2 derece dusurmustur.",
                        "Turkiye volkanik acisindan zengin bir ulkedir. Agri Dagi (5.137 m) ulkenin en yuksek noktasi ve bir volkanik dagdir. Kapadokya'nin peri bacalari da volkanik tuflerden olusmustur. Nemrut Dagi ve Erciyes Dagi diger onemli volkanik yapilardir."
                    ],
                    "quiz": [
                        {"q": "Dunya uzerinde yaklasik kac aktif volkan vardir?", "opts": ["500", "1.500", "5.000", "10.000"], "answer": 1},
                        {"q": "Krakatoa patlamasi hangi yil gerceklesmistir?", "opts": ["1815", "1883", "1902", "1980"], "answer": 1}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Sanayi Devrimi'nin Dunyayi Degistirisi",
                    "content": [
                        "Sanayi Devrimi 18. yuzyilin ortalarinda Ingiltere'de baslamis ve dunya tarihinin en buyuk donusum noktalarindan biri olmustur. James Watt'in 1769'da gelistirdigi buhar makinesi bu devrimin simgesidir. El emegi yerini makine uretimine birakmistir.",
                        "Tekstil sanayi, sanayilesmenin ilk buyuk alaniydi. Ucan mekik, iplik makinesi ve dokuma tezgahi gibi icatlar uretimi katlayarak artirdi. Fabrika sistemi ortaya cikti ve insanlar kirsal alanlardan sehirlere goc etmeye basladı.",
                        "Demir yolu aglarinin genislemesi ulasim ve ticaret devrimini tetikledi. 1830'da Liverpool-Manchester arasinda acılan demiryolu hatti, yolcu tasimacılıgında yeni bir cag baslatti. Sanayi Devrimi isgücü, toplumsal yapilar ve cevre uzerinde derin etkiler birakti.",
                        "Ikinci Sanayi Devrimi (1870-1914) elektrik, petrol ve celigi on plana cikararak imalat sureclerini tekrar donusturdu. Henry Ford'un 1913'te gelistirdigi montaj hatti sistemi, seri uretimin onunu acarak urunleri herkes icin erisilibilir kildi."
                    ],
                    "quiz": [
                        {"q": "Sanayi Devrimi hangi ulkede baslamistir?", "opts": ["Fransa", "Almanya", "Ingiltere", "ABD"], "answer": 2},
                        {"q": "James Watt buhar makinesini hangi yil gelistirmistir?", "opts": ["1712", "1769", "1800", "1830"], "answer": 1}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dijital Sanat ve NFT'ler",
                    "content": [
                        "Dijital sanat, bilgisayar teknolojisi kullanilarak uretilen sanat eserlerini kapsar. 1960'larda bilgisayar grafikleriyle basalyan bu alan, bugün yapay zeka ile uretilen sanattan sanal gerceklik enstalasyonlarina kadar genis bir yelpazeyi kapsamaktadir.",
                        "NFT (Non-Fungible Token - Degistirilemez Jeton), dijital eserlerin benzersiz sahipligini blokzincir teknolojisi ile kanitlayan bir sistemdir. 2021'de dijital sanatci Beeple'in 'Everydays' adli eseri 69.3 milyon dolara satilarak dijital sanat tarihinde bir donum noktasi olmustur.",
                        "Dijital sanat aracları demokratiklesmeyi hizlandirmistir. Procreate, Adobe Creative Suite ve ucretsiz acik kaynakli yazılımlar sayesinde herkes dijital sanat uretebilir hale gelmistir. Sosyal medya platformlari sanatlilara kuresel bir vitrin sunmaktadir.",
                        "Yapay zeka ile sanat uretimi etik tartismalara da yol acmistir. DALL-E, Midjourney gibi araclarin orijinal sanatcilarin eserlerinden ogrenıp yeni gorutuler uretmesi telif haklari konusunda soru isaretleri dogurmustur."
                    ],
                    "quiz": [
                        {"q": "Beeple'in rekor kiran dijital eseri kac milyon dolara satilmistir?", "opts": ["10.5", "35.2", "69.3", "91.8"], "answer": 2},
                        {"q": "NFT hangi teknolojiyi kullanir?", "opts": ["Bulut bilisim", "Blokzincir", "Yapay zeka", "IoT"], "answer": 1}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "E-Spor - Yeni Nesil Rekabet",
                    "content": [
                        "E-spor (elektronik spor), video oyunlarında profesyonel duzeyde yarismayi ifade eder. Kuresel e-spor geliri 2024'te 1.8 milyar dolari asmistir. League of Legends, Dota 2, CS2 ve Valorant en populer e-spor oyunlari arasindadir.",
                        "Profesyonel e-spor oyunculari gunluk 8-12 saat antrenman yapar. Refleks hizi, stratejik dusunme, takim koordinasyonu ve stres yonetimi kritik becerilerdir. Cogu profesyonel oyuncunun kariyeri 18-28 yas arasinda zirvesine ulasir.",
                        "E-spor turnuvalari artik stadyumlarda duzenlenmekte ve milonlarca kisi tarafından online izlenmektedir. The International (Dota 2) turnuvasinin odul havuzu 40 milyon dolari asmistir. Asya ulkeleri, ozellikle Guney Kore, e-sporda lider konumdadir.",
                        "Turkiye'de e-spor hizla buyumektedir. Turk takimlari uluslararasi turnuvalarda basarili sonuclar elde etmektedir. E-spor, bazı ulkelerde lise ve universite ders programlarina dahil edilmeye baslanmistir."
                    ],
                    "quiz": [
                        {"q": "Kuresel e-spor geliri 2024'te ne kadardir?", "opts": ["500 milyon $", "1.8 milyar $", "5 milyar $", "10 milyar $"], "answer": 1},
                        {"q": "The International turnuvasi hangi oyun icin duzenlenir?", "opts": ["CS2", "League of Legends", "Dota 2", "Valorant"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Aralik 2025", "sayi": 4, "tema": "Kis ve Kutlamalar",
            "kapak_emoji": "\u2744\ufe0f", "kapak_renk": "#0891b2",
            "editorial": "Aralik sayimizda kisin bugusuyle bilim ve kulturu bir araya getiriyoruz. Kar tanelerinin matematiginden yilbasi geleneklerinin tarihine, bir kış masali sizi bekliyor!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Kar Tanelerinin Matematigi - Fraktal Geometri",
                    "content": [
                        "Her kar tanesi benzersizdir, ancak hepsi alti kollu (heksagonal) simetriye sahiptir. Bu simetri, su molekullerinin kristal yapisından kaynaklanir. Su molekulleri 120 derecelik acilarla birbirine baglanir ve bu alti kollu yapilari olusturur.",
                        "Kar taneleri fraktal geometrinin dogadaki en guzel orneklerinden biridir. Fraktallar, buyutulduğunde kendine benzer paternler gosteren geometrik sekillerdir. Bir kar tanesinin kolu buyutulduğunde, ana kolun minyatur kopyalarini gormek mumkundur.",
                        "Wilson Bentley, 1885'te ilk kar tanesi fotografini cekmis ve yasamı boyunca 5.000'den fazla kar tanesini fotogroflamistir. Her bir tanenin farkli olmasi, olusum sirasindaki sicaklik ve nem kosullarinin surekli degismesinden kaynaklanir.",
                        "Koch kar tanesi, matematiksel bir fraktal ornegu olup sonsuz cevre uzunluguna sahipken sonlu bir alani kaplar. Bu paradoks, fraktal geometrinin kurucusu Benoit Mandelbrot'un calismalariyla matematiğe yeni bir boyut kazandirmistir."
                    ],
                    "quiz": [
                        {"q": "Kar taneleri kac kollu simetriye sahiptir?", "opts": ["4", "5", "6", "8"], "answer": 2},
                        {"q": "Ilk kar tanesi fotografini kim cekmistir?", "opts": ["Mandelbrot", "Wilson Bentley", "Koch", "Euler"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "2025'in En Iyi Buluslari",
                    "content": [
                        "2025 yili teknolojik inovasyon acisindan cok verimli gecmistir. Yapay zeka asistanlari artik dogal konusma dilini anlayarak karmasik gorevleri yerine getirebilmektedir. Multimodal AI modelleri metin, goruntu ve sesi bir arada isleyebilir hale gelmistir.",
                        "Kati hal pilleri, elektrikli arac endustrisinde devrim yaratma potansiyeline sahiptir. Geleneksel lityum-iyon pillere kiyasla daha yuksek enerji yogunlugu, daha hizli sarj suresi ve daha uzun omur sunarlar. Toyota ve Samsung bu alanda onemli ilerlemeler kaydetmistir.",
                        "Noralink benzeri beyin-bilgisayar arayuzleri (BCI) ilk klinik denemelerde umut verici sonuclar gostermistir. Felcli hastalar dusunce guculeriyle bilgisayar imleciini kontrol edebilmistir. Bu teknoloji norolojik hastaliklarin tedavisinde yeni ufuklar acmaktadir.",
                        "CRISPR gen duzenleme teknolojisi ilk kez orak hucre anemisi tedavisinde FDA onayi almistir. Casgevy adi verilen bu tedavi, hastalarin kendi hücrelerini genetik olarak duzelterek kalici bir cozum sunmaktadir."
                    ],
                    "quiz": [
                        {"q": "Kati hal piller hangi avantaji sunmaz?", "opts": ["Yuksek enerji yogunlugu", "Hizli sarj", "Daha ucuz uretim", "Uzun omur"], "answer": 2},
                        {"q": "CRISPR hangi hastalik icin ilk FDA onayini almistir?", "opts": ["Kanser", "Diyabet", "Orak hucre anemisi", "Alzheimer"], "answer": 2}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Kis Uykusu - Hayvanlar Nasil Hayatta Kalir?",
                    "content": [
                        "Kis uykusu (hibernasyon), bazi hayvanlarin soguk ve besin kıt donemlerini atlatmak icin metabolizmalarini yavaslatma stratejisidir. Hibernasyon sirasinda vucut sicakligi, kalp atisi ve solunum hizi dramatik sekilde duser.",
                        "Ayilar kis uykusunun en bilinen ornekleridir, ancak gercek hibernasyona girmezler. Ayilarin vucut sicakligi sadece birkaç derece duser ve kolayca uyanabilirler. Gercek hibernatörler arasinda yer sincaplari, yarasalar ve kirpiler vardir; bunlarin vucut sicakligi 0 dereceye kadar dusebilir.",
                        "Bazi hayvanlar alternatif hayatta kalma stratejileri kullanir. Aliskan kurbagasi vucut sularinin yuzde 65'inin donmasina dayanabilir; ozel antifrız proteinleri hücrelerinin zarar gormesini engeller. Arktik yer sincaplari vucut sicakligini eksi 3 dereceye kadar dusurur.",
                        "Goc, bir diger hayatta kalma stratejisidir. Kisın dondurucu soguklarin olmadigi bölgelere goc eden hayvanlar arasinda kelebekler (Monarch kelebeği 4.800 km goc eder), balinalar ve tabii ki kuslar bulunur."
                    ],
                    "quiz": [
                        {"q": "Asagidakilerden hangisi gercek hibernasyona girer?", "opts": ["Ayi", "Yer sincabi", "Kurt", "Geyik"], "answer": 1},
                        {"q": "Aliskan kurbagasi vucut suyunun yuzde kacinin donmasina dayanabilir?", "opts": ["%20", "%35", "%50", "%65"], "answer": 3}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Yilbasi Geleneklerinin Tarihi",
                    "content": [
                        "Yeni yil kutlamalari insanlik tarihinin en eski geleneklerinden biridir. Babilliler MO 2000 yilinda yeni yili Mart ayinda kutlardi. Julius Caesar MO 46'da Julian takvimini olusturarak 1 Ocak'i yilin ilk gunu olarak belirledi.",
                        "Noel agaci geleneği 16. yuzyil Almanya'sinda baslamistir. Martin Luther'in cocuklarina yildizli gokyuzunu anlatmak icin bir agaci mumlarla susledigi rivayet edilir. Gelenek 19. yuzyilda Kraliçe Victoria ile birlikte Ingiltere'ye ve oradan tum dunyaya yayilmistir.",
                        "Noel Baba figuru, 4. yuzyilda yasamis Myra piskoposu Aziz Nikolaus'a dayanir. Yoksullara gizlice hediye dagitmasıyla tanınan Nikolaus, zamánla farkli kulturlerde farkli isimler almistir: Santa Claus, Pere Noel, Babbo Natale gibi.",
                        "Turkiye'de yilbasi kutlamalari Cumhuriyet donemiyle birlikte yayginlasmistir. Noel Baba'nin memleketi olan Demre (Myra) Antalya'da bulunur. Her yil aralik ayinda Demre'de Aziz Nikolaus anma torenlerı duzenlenir."
                    ],
                    "quiz": [
                        {"q": "1 Ocak'i yilin ilk gunu olarak kim belirlenmistir?", "opts": ["Augustus", "Julius Caesar", "Nero", "Platon"], "answer": 1},
                        {"q": "Noel Baba figuru hangi tarihi kisiye dayanir?", "opts": ["Aziz Patrick", "Aziz George", "Aziz Nikolaus", "Aziz Francis"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dunya Sinemasindan 10 Unutulmaz Film",
                    "content": [
                        "Sinema 1895'te Lumiere kardeslerın Paris'teki ilk gosterimile basladi. Charlie Chaplin sessiz sinema doneminin en buyuk yildizi oldu. 1927'de 'The Jazz Singer' ile sesli sinema donemi açıldi ve Hollywood altin çagina girdi.",
                        "Orson Welles'in 'Citizen Kane' (1941) filmi sinema tarihinin en etkili filmi kabul edilir. Alfred Hitchcock gerilim turunu zirveye tasirken, Akira Kurosawa'nin 'Yedi Samuray'i (1954) dunya sinemasinin basyapitlari arasinda yer aldi.",
                        "Steven Spielberg, Francis Ford Coppola ve Martin Scorsese 1970'lerde modern Hollywood'u sekillendirdi. 'Baba' (The Godfather), 'Cennet'in Çocuklari' (Children of Heaven) ve 'Hayat Guzeldir' (La Vita e Bella) farklı kulturlerden evrensel hikayeler anlatir.",
                        "Turk sinemasi da dunya sahnesinde onemli bir yere sahiptir. Nuri Bilge Ceylan'in 'Kis Uykusu' 2014'te Cannes'da Altin Palmiye kazanmistir. Yilmaz Guney'in 'Yol' filmi 1982'de ayni odulu almistir."
                    ],
                    "quiz": [
                        {"q": "Sinema tarihinin en etkili filmi hangisi kabul edilir?", "opts": ["Casablanca", "Citizen Kane", "The Godfather", "2001: A Space Odyssey"], "answer": 1},
                        {"q": "Nuri Bilge Ceylan hangi filmle Altin Palmiye kazanmistir?", "opts": ["Uzak", "Uc Maymun", "Kis Uykusu", "Ahlat Agaci"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Kis Sporlari - Kayaktan Buz Hokeysine",
                    "content": [
                        "Kis sporlari, Kuzey Avrupa ve Iskandinavya'da binlerce yillik bir gecmise sahiptir. Norveç'te bulunan 4.500 yillik kaya resimleri, kayagin en eski kanıtlarıdır. Modern kis sporlari 19. yuzyilda organize yarismalara donusmustur.",
                        "Kis Olimpiyatlari ilk kez 1924'te Fransa'nin Chamonix kasabasinda duzenlenmistir. Bugun 15 spor dalinda yarisma yapilir: kayak, biatlon, buz pateni, buz hokeyi, curling, kizak ve daha fazlasi. Norveç, tarihte en cok kis olimpiyat madalyasi kazanan ulkedir.",
                        "Artistik buz pateni, estetik ve atletizmin birlestigi bir spor dalidir. Uçlu aksel (triple axel) atlayisi, havada 3.5 tur donmeyi gerektirir. Japon patenci Yuzuru Hanyu bu sporu sanata donusturen isimlerden biridir.",
                        "Turkiye'de kis sporlari ozellikle Dogu Anadolu ve Karadeniz bolgelerinde populerdir. Palandoken, Uludag, Kartalkaya ve Sarikamis onemli kayak merkezleridir. Turkiye Kis Olimpiyatlari'nda 2022'de ilk madalyasina cok yaklasmiştir."
                    ],
                    "quiz": [
                        {"q": "Ilk Kis Olimpiyatlari hangi yil ve nerede duzenlenmistir?", "opts": ["1920 Oslo", "1924 Chamonix", "1928 St. Moritz", "1932 Lake Placid"], "answer": 1},
                        {"q": "Tarihte en cok kis olimpiyat madalyasi kazanan ulke hangisidir?", "opts": ["Kanada", "Rusya", "Norvec", "ABD"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Ocak 2026", "sayi": 5, "tema": "Yeni Baslangiclar",
            "kapak_emoji": "\U0001f31f", "kapak_renk": "#dc2626",
            "editorial": "Yeni yila yeni baslangiclarla giriyoruz! Ocak sayimizda insan genomu projesinden kuantum bilgisayarlara, iklim degisikliginden Turk edebiyatina heyecan verici konular sizi bekliyor.",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Insan Genomu Projesi ve Gen Tedavisi",
                    "content": [
                        "Insan Genomu Projesi (HGP), 1990-2003 yillari arasinda yurutulen ve insan DNA'sindaki yaklasik 3 milyar baz ciftinin haritasini cikaran devasa bir bilimsel girisimdir. 13 yil suren ve 2.7 milyar dolara mal olan proje, biyoloji tarihinin en buyuk basarilarindan biridir.",
                        "Insan genomu yaklasik 20.000-25.000 gen icerir, bu sayi baslangicta tahmin edilen 100.000'den cok daha azdir. Genomumuzun yuzde 99.9'u tum insanlarda ortaktir; bireysel farklılıklar sadece yuzde 0.1'lik dilimden kaynaklanir.",
                        "Gen tedavisi, hatali genlerin duzeltilmesi veya degistirilmesiyle hastaliklarin tedavi edilmesini amaclar. CRISPR-Cas9 teknolojisi, DNA'yi hassas bir sekilde kesip düzenlemeyi mumkun kilmistir. Bu teknoloji 2020 Nobel Kimya Odulu'ne layik gorulmustur.",
                        "Gen tedavisi simdiden bazi nadir hastaliklarda basari gostermektedir. Spinal muskuler atrofi (SMA) tedavisinde kullanilan Zolgensma, dünyanın en pahali ilaci olup tek doz 2.1 milyon dolardır. Gelecekte kanser, Alzheimer ve kalp hastalıklarina yonelik gen tedavileri beklenmektedir."
                    ],
                    "quiz": [
                        {"q": "Insan genomu yaklasik kac gen icerir?", "opts": ["5.000", "20.000-25.000", "100.000", "1 milyon"], "answer": 1},
                        {"q": "CRISPR-Cas9 teknolojisi hangi yil Nobel Odulu almistir?", "opts": ["2015", "2018", "2020", "2022"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Kuantum Bilgisayarlar - Hesaplamanin Gelecegi",
                    "content": [
                        "Kuantum bilgisayarlar, klasik bilgisayarlarin 0 ve 1 bitleri yerine kubit (quantum bit) kullanir. Kubitler superpozisyon ilkesi sayesinde ayni anda hem 0 hem 1 olabilir. Bu ozellik, belirli problemlerde inanilmaz hesaplama gucu saglar.",
                        "Google'in Sycamore islemcisi, 2019'da 'kuantum ustunlugu' olarak adlandirilan bir dönüm noktasına ulasti. Klasik bir superilgisayarin 10.000 yilda yapacagi bir hesaplamayi 200 saniyede gerceklestirdigini iddia etti. IBM bu iddaya itiraz etse de, gelisme buyuk yanki uyandirdi.",
                        "Kuantum bilgisayarlar ozellikle kriptografi, ilac gelistirme, malzeme bilimi ve optimizasyon problemlerinde devrim yaratma potansiyeline sahiptir. Molekuler simulasyonlar sayesinde yeni ilaclarin kesfı hizlanabilir.",
                        "Kuantum bilgisayarlarin en buyuk sorunu 'dekoherans'tir; kubitler cevresel etkilere son derece duyarlidir ve bilgiyi korumalari zordur. Bu nedenle kuantum bilgisayarlar sifira yakin sicakliklarda (-273 derece) calistirilir. Tam hata duzeltmeli buyuk olcekli kuantum bilgisayarlar henuz gelistirme asamasindadir."
                    ],
                    "quiz": [
                        {"q": "Kuantum bilgisayarlarin temel bilgi birimi nedir?", "opts": ["Bit", "Byte", "Kubit", "Piksel"], "answer": 2},
                        {"q": "Kuantum bilgisayarlar neden cok dusuk sicakliklarda calistirilir?", "opts": ["Hiz icin", "Enerji tasarrufu", "Dekoherans onleme", "Maliyet azaltma"], "answer": 2}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Kutuplar Eriyor mu? - Iklim Degisikligi Verileri",
                    "content": [
                        "Kuzey Kutbu'ndaki deniz buzu, son 40 yilda yaklasik yuzde 40 azalmistir. Yaz aylarinda minimum buz kaplamasi her on yilda yuzde 13 oraninda kuculmoktedir. NASA uydu verileri bu egiIimin hizlandigini gostermektedir.",
                        "Antarktika ve Gronland buz tabakalari kara üzerindeki devasa buz kutleleridir. Gronland buz tabakasi tamamen erirse, kuresel deniz seviyesi yaklasik 7 metre yukselir. Antarktika'daki buzun tamami erirse bu rakam 58 metreye cikar.",
                        "Iklim degisikligi sadece kutuplari degil, tum dunya ekosistemlerini etkiler. Mercan resifleri agarmakta, buzullar kuculmokte, deniz seviyesi yukselmektedir. Son 100 yilda kuresel ortalama sicaklik yaklasik 1.1 derece artmistir.",
                        "Paris Iklim Anlasmasi (2015), kuresel isinmayi 1.5 dereceyle sinirlamayı hedefler. Yenilenebilir enerji kaynaklarina gecis, karbon emisyonlarinin azaltilmasi ve orman alanlarının korunmasi bu hedefe ulasmak icin kritik oneme sahiptir."
                    ],
                    "quiz": [
                        {"q": "Kuzey Kutbu deniz buzu son 40 yilda yaklasik yuzde kac azalmistir?", "opts": ["%10", "%25", "%40", "%60"], "answer": 2},
                        {"q": "Paris Iklim Anlasmasi kuresel isinmayi kac dereceyle sinirlamayi hedefler?", "opts": ["0.5°C", "1.0°C", "1.5°C", "2.5°C"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Turk Cumhuriyeti'nin Ilk Yillari (1923-1930)",
                    "content": [
                        "29 Ekim 1923'te ilan edilen Turkiye Cumhuriyeti, Osmanli Imparatorlugu'nun kuluundan dogmus modern bir ulus devlettir. Mustafa Kemal Ataturk, cumhuriyetin kurucusu ve ilk cumhurbaskani olarak kapsamli reformlar baslatmistir.",
                        "Harf Devrimi (1928), Arap alfabesinden Latin alfabesine gecisi sagladi. Ataturk bizzat halka yeni harfleri ogretmek icin 'Millet Mektepleri' açtirdi. Bu devrim okuma yazma oranini onemli olcude artirmistir.",
                        "1924'te halifelik kaldirildi, 1926'da yeni Medeni Kanun kabul edildi. Kadin haklari alaninda buyuk adimlar atildi; 1930'da belediye secimlerinde ve 1934'te genel secımlerde kadinlara oy hakki taninmistir. Bu hak birçok Avrupa ulkesinden daha erken verilmistir.",
                        "Ekonomik alanda da onemli adimlar atilmistir. 1927'de Tesvik-i Sanayi Kanunu cikarilarak ulusal sanayinin gelistirilmesi hedeflenmistir. Sumerbank ve Etibank gibi devlet kuruluslari ekonomik kalkinmanin motorlari olmustur."
                    ],
                    "quiz": [
                        {"q": "Harf Devrimi hangi yil gerceklestirilmistir?", "opts": ["1924", "1926", "1928", "1930"], "answer": 2},
                        {"q": "Turkiye'de kadinlara genel secimlerde oy hakki hangi yil taninmistir?", "opts": ["1928", "1930", "1934", "1946"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Turk Edebiyatinin 10 Basyapiti",
                    "content": [
                        "Turk edebiyati, Orta Asya'daki Orhun Yazitlari'ndan (8. yuzyil) gunumuze zengin bir gelenek tasir. Yunus Emre, Mevlana ve Fuzuli gibi divan sairleri Turk edebiyatinin temel taslarini olusturmustur.",
                        "Tanzimat donemiyle birlikte Bati etkili edebi turler Turk edebiyatina girmistir. Namik Kemal'in 'Intibah'i ilk Turk romani kabul edilir. Halide Edib Adivar'in 'Atesten Gomlek'i Kurtulus Savasi'nin en etkileyici anlatılarından biridir.",
                        "Cumhuriyet donemi Turk edebiyati, Yasar Kemal'in 'Ince Memed'i, Orhan Pamuk'un 'Benim Adim Kirmizi'si ve Oguz Atay'in 'Tutunamayanlar'i gibi dunya capinda tanınan eserler uretmistir. Orhan Pamuk 2006'da Nobel Edebiyat Odulu'nu kazanmistir.",
                        "Siirde Nazim Hikmet, Orhan Veli Kanik ve Cemal Sureya gibi isimler farkli akimlarla Turk siirini zenginlestirmistir. Nazim Hikmet'in 'Memleketimden Insan Manzaralari' destani, dünya edebiyatinin onemi eserlerinden biri kabul edilir."
                    ],
                    "quiz": [
                        {"q": "Turk edebiyatinin bilinen en eski yazili kaynaklari nedir?", "opts": ["Divan-i Lugat", "Orhun Yazitlari", "Kutadgu Bilig", "Dede Korkut"], "answer": 1},
                        {"q": "Orhan Pamuk Nobel Edebiyat Odulu'nu hangi yil almistir?", "opts": ["2002", "2004", "2006", "2008"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Saglikli Yasam Icin 10 Egzersiz",
                    "content": [
                        "Dunya Saglik Orgutu, yetiskinlerin haftada en az 150 dakika orta yoğunlukta veya 75 dakika yuksek yogunlukta fiziksel aktivite yapmasini onerir. Duzenli egzersiz kalp hastaligi, diyabet ve depresyon riskini onemli olcude azaltir.",
                        "Yuruyus, herkesin kolayca yapabilecegi en etkili egzersizdir. Gunluk 30 dakikalik tempolu yuruyus kardiyovaskuler sagligı iyilestirir. Yuzme tum vucut kaslarini çalıştıran, eklemlere az yuk bindiren mukemmel bir egzersizdir.",
                        "Plank, squat ve lunges gibi vucut agirligiyla yapilan egzersizler kas gucunu artirır. Yoga ve pilates esneklik, denge ve zihinsel rahatlama saglar. HIIT (Yuksek Yogunluklu Aralikli Antrenman) kisa surede yuksek kalori yakimi sunar.",
                        "Cocuklar ve gencler icin gunluk en az 60 dakika fiziksel aktivite onerilir. Takim sporlari hem fiziksel gelisim hem sosyal beceriler kazandirır. Egzersiz oncesi isinma ve sonrasi soguma hareketleri sakatlık riskini azaltir."
                    ],
                    "quiz": [
                        {"q": "DSO haftada en az kac dakika orta yogunlukta egzersiz onerir?", "opts": ["60", "90", "120", "150"], "answer": 3},
                        {"q": "HIIT neyin kisaltmasidir?", "opts": ["Heavy Impact Interval Training", "High Intensity Interval Training", "Heart Improvement Indoor Training", "Hic biri"], "answer": 1}
                    ]
                }
            ]
        },
        {
            "month": "Subat 2026", "sayi": 6, "tema": "Sevgi ve Dostluk",
            "kapak_emoji": "\u2764\ufe0f", "kapak_renk": "#e11d48",
            "editorial": "Subat'in sevgi dolu atmosferinde bilim, doga ve kulturun dostluk yonlerini kesfediyoruz. Sevgi hormonundan balinalarIn sarkilarina, baris anlasmalarndan spordaki dostluk hikayelerine!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Oksitosin - Sevgi Hormonu'nun Bilimi",
                    "content": [
                        "Oksitosin, beynin hipotalamus bolgesinde uretilen ve 'sevgi hormonu' veya 'baglanma hormonu' olarak bilinen bir noropeptittir. Fiziksel temas, sarilma ve goz kontagi sirasinda salgilanir. Anne-bebek bagi olusumunda kritik bir rol oynar.",
                        "Arastirmalar oksitosin seviyesinin yukseldiğinde guven duygusunun arttigini gostermistir. Bir deneyde burundan oksitosin spreyi verilen katilimcilar, diger insanlara daha fazla guven gostermistir. Bu hormon sosyal baglarun ve empati kurmanin biyolojik temelidir.",
                        "Oksitosin sadece insanlarda degil, diger memelilerde de baglanma davranislarini duzenler. Preri tarla fareleri, yuksek oksitosin seviyelerine sahip olup tek esli yasarlar. Evci hayvanlarimizla etkilesim sirasinda da hem bizim hem hayvanlarin oksitosin seviyeleri yukselir.",
                        "Son arastirmalar oksitosinin otizm spektrum bozuklugunun tedavisinde potansiyel faydalar sunabilecegini gostermektedir. Ancak hormonun etkileri karmasiktir; bazi durumlarda grup ici kayirmaciligi artirabilecegi de gozlenmistir."
                    ],
                    "quiz": [
                        {"q": "Oksitosin beynin hangi bolgesinde uretilir?", "opts": ["Hipokampus", "Amigdala", "Hipotalamus", "Serebellum"], "answer": 2},
                        {"q": "Asagidaki hayvanlardan hangisi yuksek oksitosin seviyeleri ile bilinir?", "opts": ["Kedi", "Preri tarla faresi", "Iguana", "Baykus"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Sosyal Medya Algoritmalari Nasil Calisir?",
                    "content": [
                        "Sosyal medya platformlari, kullanicilara gosterilecek icerigi belirlemek icin karmasik algoritmalar kullanir. Bu algoritmalar kullanicinin gecmis etkilesimleri, begeni ve yorum paternleri, takip ettigi hesaplar ve harcadigi zamana gore kisisellestirilmis bir akis olusturur.",
                        "Instagram, TikTok ve YouTube gibi platformlarin oneri algoritmalari 'isbirlıkcı filtreleme' yontemini kullanir. Benzer ilgi alanliarina sahip kullanicilarin begendigi icerikleri birbirlerine onerir. Bu sistem bazen 'filtre baloncugu' adi verilen dusunce yankilarina yol acabilir.",
                        "Dikkat ekonomisi kavrami, sosyal medya platformlarinin temel is modelini tanimlar. Kullanicilarin platformda gecirdigi her dakika, reklam geliri uretir. Bu nedenle algoritmalar, dikkat cekici ve duygusal tepki uyandiran icerikleri on plana cikarir.",
                        "Dijital okur-yazarlik, algoritmalarin etkilerini anlamak icin kritik oneme sahiptir. Bilgi kaynaklarinı sorgulamak, farkli bakis acilarini aramak ve ekran süresini bilinçli yonetmek saglikli bir dijital yasam icin gereklidir."
                    ],
                    "quiz": [
                        {"q": "Sosyal medya algoritmalarinin ana amaci nedir?", "opts": ["Egitim", "Kullaniciyi platformda tutma", "Haber verme", "Arkadas edinme"], "answer": 1},
                        {"q": "'Filtre baloncugu' ne anlama gelir?", "opts": ["Spam filtreleme", "Sadece benzer icerikleri gorme", "Reklam engelleme", "Gizlilik ayarlari"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Hayvanlar Arasi Iletisim - Balinalarin Sarkilari",
                    "content": [
                        "Kambur balinalar, hayvanlar aleminin en karmasik vokal iletisimlerinden birini gerceklestirir. Erkek balinaların sarkilari 30 dakikayi aşabılır ve yüzlerce kilometre uzaktan duyulabilir. Her populasyon kendine ozgu bir sarkiya sahiptir ve bu sarkilar yillar icinde degisir.",
                        "Yunuslar ekolokasyon (yanki ile konum belirleme) kullanarak avlanir ve iletisim kurar. Her yunusun kendine ozgu bir 'isim isligi' vardir ve birbirlerini bu isliklerle cagirır. Arastirmacilar yunuslarin basit bir 'dil' kullandığına dair kanitlar bulmaktadir.",
                        "Fillerin iletisimi de son derece karmasiktir. Infrasound adi verilen cok alcak frekanstaki sesler, 10 km uzaktan algilanabilir. Filler ayrica vucut dili, dokunma ve kimyasal sinyaller kullanır. Olmus akrabalarina yas tuttiklari gozlenmistir.",
                        "Arıların 'dans dili' Karl von Frisch tarafindan cozulmüs ve ona 1973 Nobel Odulu kazandirmistir. Iscı arılar, besin kaynaginın yonunu ve uzakligini '8 dansi' ile kovan arkadaslarina bildirir. Bu dans, hayvanlar alemindeki en hassas iletisim sistemlerinden biridir."
                    ],
                    "quiz": [
                        {"q": "Kambur balina sarkilari ne kadar uzaktan duyulabilir?", "opts": ["1 km", "10 km", "Yuzlerce km", "Binlerce km"], "answer": 2},
                        {"q": "Ari dans dilini cozen bilim insani kimdir?", "opts": ["Darwin", "Karl von Frisch", "Jane Goodall", "Konrad Lorenz"], "answer": 1}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Dunya Baris Anlasmalari Tarihi",
                    "content": [
                        "Westfalya Barisi (1648), modern uluslararası iliskilerin baslangici kabul edilir. Otuz Yil Savalarini sona erdiren bu anlasma, ulus-devlet kavraminın temelini atmis ve devletlerin egemenlik haklarini tanimiştir.",
                        "Viyana Kongresi (1815), Napoleon Savaselarindan sonra Avrupa'da yeni bir guc dengesi kurmaya calismistir. Kısa sureli bir baris donemi saglasa da, 19. yuzyilın milliyetcilik akimlari bu dengeyi bozmustur.",
                        "Birinci Dunya Savasi'ni sona erdiren Versay Antlasmasi (1919) kaybeden taraflara agir kosullar dayatti. Bu kosullarin Almanya'da yarattigi hosnutsuzluk, İkinci Dunya Savasi'nin nedenlerinden biri olmustur. Savasin ardindan Milletler Cemiyeti kurulmustur.",
                        "Ikinci Dunya Savasi'ndan sonra kurulan Birlesmis Milletler (1945) ve Avrupa Birligi projesi, kalici baris icin en kapsamli girisimlerdir. AB, asirlar boyunca savasmis Avrupa ulkelerini ekonomik ve siyasi birlik icerisinde bir araya getirerek 2012'de Nobel Baris Odulu'nu almistir."
                    ],
                    "quiz": [
                        {"q": "Modern uluslararasi iliskilerin baslangici kabul edilen anlasma hangisidir?", "opts": ["Versay", "Westfalya", "Viyana", "Lozan"], "answer": 1},
                        {"q": "Avrupa Birligi Nobel Baris Odulu'nu hangi yil almistir?", "opts": ["2000", "2006", "2012", "2018"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Ask Edebiyatta - Romeo ve Juliet'ten Leyla ve Mecnun'a",
                    "content": [
                        "Ask, dunya edebiyatinin en evrensel ve kalici temasidir. Shakespeare'in 'Romeo ve Juliet'i (1597), trajik askin en bilinen anlatisidir. Iki dusman ailenin cocuklarinin yasak aski, dort yuzyildir sahnelenmeye devam etmektedir.",
                        "Dogu edebiyatinda Fuzuli'nin 'Leyla ve Mecnun'u (16. yuzyil), platonik askin en derin anlatımlarından biridir. Mecnun'un Leyla aski uzerinden ilahi aska yolculugu, tasavvuf gelenegiinin en guzel orneklerinden birini olusturur.",
                        "Jane Austen'in 'Gurur ve Onyargi'si (1813), toplumsal sinıf farkliliklari ve bireysel gurur arasinda sekillenen bir ask hikayesi anlatir. Emily Bronte'nin 'Ugultulu Tepeler'i ise tutku ve intikamla bezenmis karanlik bir ask destanidir.",
                        "Modern edebiyatta Gabriel Garcia Marquez'in 'Kolera Gunlerinde Ask'i, elli yillik bir bekleyisin hikayesini anlatir. Turk edebiyatinda ise Cemal Sureya'nin ask siirleri ve Orhan Pamuk'un 'Masumiyet Muzesi' askin farkli yuzlerini kesfeder."
                    ],
                    "quiz": [
                        {"q": "'Romeo ve Juliet' hangi yil yazilmistir?", "opts": ["1497", "1597", "1697", "1797"], "answer": 1},
                        {"q": "'Leyla ve Mecnun'un yazari kimdir?", "opts": ["Yunus Emre", "Nedim", "Fuzuli", "Baki"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Takim Ruhu - Sporda Dostluk Oykuleri",
                    "content": [
                        "Spor tarihı, rekabetin otesinde insanlik ve dostluk ornekleriyle doludur. 1936 Berlin Olimpiyatları'nda Alman atlet Luz Long, rakibi Jesse Owens'a yardim ederek onun altin madalya kazanmasina katki saglamistir. Bu jest, Nazi ideolojisine karsi insanlık mesaji olmustur.",
                        "2016 Rio Olimpiyatı'nda 5.000 metre yarisinda Yeni Zelandali Nikki Hamblin ve Amerikali Abbey D'Agostino carpısarak dustu. Iki atlet birbirine yardim ederek yarisi birlikte tamamladi. Bu goruntu olimpiyat ruhunun en guzel ornegi olarak hafizalara kazindi.",
                        "Futbolda 1914 Noel Ateskes'i, Birinci Dunya Savasi sirasinda Ingiliz ve Alman askerlerin cepheIer arasında futbol oynamasiyla tarihe gecmistir. Bu spontan baris anı, sporun insanlari birlestirici gucunu gostermektedir.",
                        "Turkiye'de Galatasaray ve Fenerbahce arasindaki Dunya Barisi icin Dostluk Maci geleneği, rekabetin dostluga donusebilecegini gosterir. Spor, farkli kulturlerin, dillerin ve inancların bir araya geldigi evrensel bir barış dilidir."
                    ],
                    "quiz": [
                        {"q": "1936 Olimpiyatlari'nda Jesse Owens'a yardim eden Alman atlet kimdir?", "opts": ["Max Schmeling", "Luz Long", "Rudolf Harbig", "Carl Diem"], "answer": 1},
                        {"q": "1914 Noel Ateskesi sirasinda askerler hangi sporu oynamistir?", "opts": ["Kriket", "Rugby", "Futbol", "Beyzbol"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Mart 2026", "sayi": 7, "tema": "Bahar Geliyor",
            "kapak_emoji": "\U0001f338", "kapak_renk": "#16a34a",
            "editorial": "Baharın gelisiyle dogada ve kulturdeki yenilenmeyi kutluyoruz! Fotosentezden elektrikli araclara, Canakkale'den bisiklet kulturune kadar renkli bir sayi sizi bekliyor.",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Fotosentez - Bitkilerin Gunes Fabrikasi",
                    "content": [
                        "Fotosentez, bitkilerin gunes isigini kullanarak karbondioksit ve suyu glukoz ve oksijene donusturdugu yasamin temel surecidir. Bu islem yapraklardaki kloroplast organellerinde gerceklesir. Klorofil pigmenti isigı emerek enerji donusumunu baslatir.",
                        "Fotosentez iki asamadan olusur: isik reaksiyonlari ve Calvin dongusu. Isik reaksiyonlarinda su parcalanarak oksijen serbest kalir ve enerji taşıyıcıları (ATP ve NADPH) uretilir. Calvin dongusunde bu enerji kullanılarak CO2, seeker molekullerine donusturulur.",
                        "Dunyadaki tum oksijen uretiminin yaklasik yuzde 50-80'i okyanuslardaki fitoplankton tarafindan gerceklestirilir. Bir hektar yetiskin orman yılda yaklasik 10 ton oksijen uretir. Fotosentez olmadan Dunya'daki yasam mümkün olmazdi.",
                        "Bilim insanları yapay fotosentez uzerinde calismaktadir. Gunes isigini kullanarak suyu hidrojen ve oksijene ayiran sistemler gelistirilmektedir. Bu teknoloji basarili olursa, temiz enerji uretiminde devrim yaratabilir."
                    ],
                    "quiz": [
                        {"q": "Fotosentez yapraklardaki hangi organelde gerceklesir?", "opts": ["Mitokondri", "Kloroplast", "Ribosom", "Cekirdek"], "answer": 1},
                        {"q": "Dunya oksijen uretiminin buyuk kismi nereden gelir?", "opts": ["Yagmur ormanlari", "Okyanuslardaki fitoplankton", "Cicekli bitkiler", "Mantarlar"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Elektrikli Araclar ve Surdurulebilir Ulasim",
                    "content": [
                        "Elektrikli araclar (EV), fosil yakitlara bagimliligi azaltmanin en umut verici yollarindan biridir. 2024 yilinda dunya genelinde 40 milyondan fazla elektrikli arac trafiğe cikmistir. Cin, Avrupa ve ABD en buyuk EV pazarlarıdır.",
                        "Modern elektrikli araclarin menzili 400-600 km'ye ulasmistir. Tesla, BYD, Volkswagen ve Hyundai oncu markalardır. Sarj altyapisi hizla genislemekte olup, hizli sarj istasyonlari 30 dakikada yuzde 80 sarj imkani sunmaktadir.",
                        "Elektrikli araclar egzoz emisyonu uretmez, ancak cevresel etkileri enerji kaynagina baglıdır. Yenilenebilir enerjiyle sarj edilen bir EV, yasamdongusu boyunca benzinli araca gore yuzde 70 daha az karbon ayak izi birakir.",
                        "Turkiye'nin yerli elektrikli otomobili TOGG, 2023'te yollara cikmistir. Surucusuz araclar, paylasimli mobilite ve elektrikli toplu tasimayla birlikte gelecegIn ulasim sistemi tamamen degisecektir."
                    ],
                    "quiz": [
                        {"q": "2024'te dunya genelinde yaklasik kac elektrikli arac vardir?", "opts": ["10 milyon", "20 milyon", "40 milyon", "100 milyon"], "answer": 2},
                        {"q": "Turkiye'nin yerli elektrikli otomobili hangisidir?", "opts": ["TOGG", "TOFAS", "Anadol", "Devrim"], "answer": 0}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Bahar Uyanisi - Tohumdan Cicege",
                    "content": [
                        "Bahar geldiginde sicaklik ve gun isigi suresinin artmasi bitkilerde uyanma sinyallerini tetikler. Tohumlar cimlenmeye, agaclar tomurcuklanmaya baslar. Bu surecte bitkiler, kis boyunca depoladiklari enerjiyi kullanir.",
                        "Ciçeklenme sureci, bitkinin ureme dogusudendir. Cicek yapraklari (petaller), boceekleri cekmek icin parlak renkler ve kokular uretir. Tozlasma, cicektozu (polen) tanesinin bir cicekten digerine tasınmasiyla gerceklesir. Ruzgar, bocekler, kuslar ve yarasalar bu islemde aracilik eder.",
                        "Ilkbahar alerjileri, havadaki polen yogunlugunun artmasiyla ortaya cikar. Cimen, agac ve yabanotu polenleri en yaygin alerjenlerdir. Iklim degisikligi nedeniyle polen sezonu son 30 yilda ortalama 20 gun uzamistir.",
                        "Turkiye, yaklasik 12.000 bitki turuyle Avrupa'nin en zengin florasina sahip ulkelerinden biridir. Bunlarln 3.000'den fazlasi endemiktir, yani sadece Turkiye'de bulunur. Ozellikle Dogu Anadolu ve Akdeniz Bolgesi bitki cesitliligi acisindan cok zengindir."
                    ],
                    "quiz": [
                        {"q": "Turkiye'de yaklasik kac bitki turu bulunur?", "opts": ["3.000", "7.000", "12.000", "20.000"], "answer": 2},
                        {"q": "Iklim degisikligi nedeniyle polen sezonu ne kadar uzamistir?", "opts": ["5 gun", "10 gun", "20 gun", "40 gun"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Canakkale Savasi'nin Oykusu",
                    "content": [
                        "Canakkale Savasi (1915-1916), Birinci Dunya Savasi'nin en kanlı ve stratejik acisindan en onemli cephelerinden biridir. Itilaf Devletleri, Istanbul'u ele gecirmek ve Rusya'ya deniz yolu acmak amaciyla Canakkale Bogazi'na saldirmistir.",
                        "18 Mart 1915'te Itilaf donanmasi Canakkale Bogazi'ni gecmeye calışmis, ancak Turk mayinlari ve topculari tarafindan agir kayiplar verilmistir. Uc savas gemisi batmiş, uc tanesi de agir hasar almistir. Bu basarisizlık uzerine kara harekati planlanmistir.",
                        "25 Nisan 1915'te Gelibolu Yarimadasi'na yapilan cikarma, Turk kuvvetlerinin kahramanca dirençiyle karsilasmistir. Yarbay Mustafa Kemal, Conkbayiri ve Anafartalar'daki basarili savunmasıyla savasi degistirmis ve ulusal bir kahraman olmustur.",
                        "Canakkale Savasi'nda her iki taraftan toplam yaklasik 500.000 asker hayatini kaybetmis veya yaralanmistir. Bu savas, Turk ulusal bilincinin olusumunda donum noktasi olmus ve Kurtulus Savasi'nin liderini ortaya cikarmistir. 'Canakkale gecilmez' sozu ulusun sembol cumlelerinden biri olmustur."
                    ],
                    "quiz": [
                        {"q": "Canakkale Deniz Savasi hangi tarihte gerceklesmistir?", "opts": ["25 Nisan 1915", "18 Mart 1915", "19 Mayis 1915", "30 Agustos 1915"], "answer": 1},
                        {"q": "Canakkale'de Turk savunmasina liderlik eden komutan kimdir?", "opts": ["Enver Pasa", "Fevzi Cakmak", "Mustafa Kemal", "Kazim Karabekir"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dunya Tiyatro Tarihi",
                    "content": [
                        "Tiyatronun kokleri Antik Yunan'a, MO 6. yuzyila dayanir. Dionysos onuruna duzenlenen festivallerde ortaya cikan tragedya ve komedya turleri, Batı tiyatrosunun temelini olusturmustur. Aiskhylos, Sofokles ve Euripides tragedyanin uc buyuk ustasıdır.",
                        "Shakespeare donemi (16-17. yuzyil), tiyatro tarihinin altin cagidir. Globe Tiyatrosu'nda sahnelenen 'Hamlet', 'Macbeth' ve 'Bir Yaz Gecesi Ruya'si gibi oyunlar bugun hala dunyanin dort bir yaninda oynanmaktadir.",
                        "Turk tiyatrosu, geleneksel Karagoz-Hacivat golge oyunundan, Orta Oyunu'ndan ve meddah geleneklerinden beslenir. Cumhuriyet donemiyle birlikte Bati tiyatrosu etkisinde modern Turk tiyatrosu olusmustur. Muhsin Ertugrul bu donusumun oncusudur.",
                        "Cagdas tiyatro, geleneksel sahne sinirlarini zorlayan deneysel formlara evrilmistir. Immersif tiyatro, sokak tiyatrosu ve dijital performanslar tiyatronun sinirlarini genisletmektedir. Tiyatro, binlerce yildir insanlık deneyimini yansitan canli bir sanat formu olmaya devam etmektedir."
                    ],
                    "quiz": [
                        {"q": "Antik Yunan'da tragedyanin uc buyuk ustasi arasinda hangisi yer almaz?", "opts": ["Aiskhylos", "Aristofanes", "Sofokles", "Euripides"], "answer": 1},
                        {"q": "Turk tiyatrosunun modernlesme oncusu kimdir?", "opts": ["Haldun Taner", "Muhsin Ertugrul", "Aziz Nesin", "Orhan Asena"], "answer": 1}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Bisiklet Kulturu ve Saglik",
                    "content": [
                        "Bisiklet, 1817'de Karl Drais'in icad ettigi 'draisin' ile baslamistir. Pedallar 1860'larda eklenmis, modern bisiklet formu 1885'te 'guvenlik bisikleti' ile olusmustur. Bugün dunya genelinde 1 milyardan fazla bisiklet kullanilmaktadir.",
                        "Duzenli bisiklet surmek kardiyovaskuler sagligi guclendirir, kalori yakar ve kas gucu artırır. Haftada 30 dakikalik bisiklet kullanimi, kalp hastalıgi riskini yuzde 50 oraninda azaltir. Ayrica zihinsel saglık uzerinde de olumlu etkileri kanitlanmistir.",
                        "Hollanda ve Danimarka dünyanin en bisiklet dostu ulkeleridir. Kopenhag'da iş gidis-gelislerinin yuzde 50'si bisikletle yapilir. Bu ulkelerde bisiklet yollari, park sistemleri ve trafik duzenlemeleri bisikletlileri oncelikli kılar.",
                        "Turkiye'de bisiklet kulturu hizla buyumektedir. Buyuk sehirlerde bisiklet yollari genisletilmekte, paylasimli bisiklet sistemleri yaygınlasmaktadır. Tour de France gibi profesyonel yarislarin yani sira, rekreasyonel bisiklet turizmi de populerlik kazanmaktadir."
                    ],
                    "quiz": [
                        {"q": "Modern bisikletin atasi 'draisin' hangi yil icad edilmistir?", "opts": ["1790", "1817", "1860", "1885"], "answer": 1},
                        {"q": "Kopenhag'da is gidis-gelislerinin yuzde kaci bisikletle yapilir?", "opts": ["%20", "%30", "%40", "%50"], "answer": 3}
                    ]
                }
            ]
        },
        {
            "month": "Nisan 2026", "sayi": 8, "tema": "Dunya Gunu",
            "kapak_emoji": "\U0001f30d", "kapak_renk": "#15803d",
            "editorial": "22 Nisan Dunya Gunu'ne ozel bu sayimizda gezegenimizi ve onu koruma yollarini inceliyoruz. Karbon ayak izinden derin deniz yaratiklarina, cevre hareketinden doga sporlarindan keyifli bir icerik sizi bekliyor!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Karbon Ayak Izi ve Surdurulebilirlik",
                    "content": [
                        "Karbon ayak izi, bir bireyin, kurulusun veya urünun sera gazi emisyonlarinin toplam olcusudur. Ortalama bir Turk vatandasinin yillik karbon ayak izi yaklasik 5 ton CO2 esdeğeridir. Kuresel ortalama 4.7 ton iken, ABD'de bu rakam 15 tonu asar.",
                        "Bireysel karbon ayak izinin en buyuk kaynaklari ulasim, konut enerjisi ve beslenme alanlarindadir. Bir saatlik ucak yolculugu kisı basina yaklasik 250 kg CO2 uretir. Et tuketimi, ozellikle sigir eti, bitkisel beslenmeye gore 10-50 kat daha fazla sera gazi emisyonuna neden olur.",
                        "Surdurulebilirlik, gelecek nesillerin ihtiyaclarini karsilama kapasitesini tehlikeye atmadan bugunun ihtiyaclarini karsilamaktir. Dongusel ekonomi, atiklari minimuma indirerek kaynaklari tekrar tekrar kullanmayi hedefler.",
                        "Bireysel olarak karbon ayak izinizi azaltmak icin toplu taşıma kullanabilir, enerji verimli ev aletleri tercih edebilir, yerel ve mevsimsel gidalar tuketebilir ve gereksiz tuketimden kacinabilirsiniz. Kucuk degisiklikler buyuk etkiler yaratabilir."
                    ],
                    "quiz": [
                        {"q": "Ortalama bir Turk vatandasinin yillik karbon ayak izi yaklasik ne kadardir?", "opts": ["2 ton", "5 ton", "10 ton", "15 ton"], "answer": 1},
                        {"q": "Asagidakilerden hangisi en fazla sera gazi emisyonuna neden olur?", "opts": ["Tavuk eti", "Balik", "Sigir eti", "Mercimek"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Yenilenebilir Enerji - Gunes, Ruzgar, Dalga",
                    "content": [
                        "Yenilenebilir enerji kaynaklari 2023'te kuresel elektrik uretiminin yuzde 30'unu karsılamistir. Gunes enerjisi maliyeti son 10 yilda yuzde 90 dusmus ve en ucuz enerji kaynagi haline gelmistir. Cin, dunya gunes paneli uretiminin yuzde 80'inden fazlasını karsilamaktadir.",
                        "Ruzgar enerjisi, ozellikle acik deniz rüzgar santralleri ile buyuk potansiyel tasimnaktadir. Bir modern ruzgar turbini 5-15 MW guc uretebilir, bu da binlerce evi besleyecek kapasitedir. Danimarka elektriginin yuzde 50'sinden fazlasını ruzgardan elde eder.",
                        "Dalga ve gelgit enerjisi henuz gelisme asamasindadir ancak buyuk potansiyele sahiptir. Okyanus dalgalari surekli ve öngörülebilir bir enerji kaynagidir. Iskoçya ve Portekiz bu alanda oncu ulkelerdir.",
                        "Turkiye, gunes enerjisi potansiyeli acisindan Avrupa'nin en avantajli ulkelerinden biridir. Güneydogu Anadolu Bolgesi yilda ortalama 2.900 saat gunes ışığı alır. Turkiye'nin kurulu ruzgar enerji kapasitesi 12 GW'i asmistir."
                    ],
                    "quiz": [
                        {"q": "Gunes enerjisi maliyeti son 10 yilda yuzde kac dusmustur?", "opts": ["%50", "%70", "%90", "%95"], "answer": 2},
                        {"q": "Danimarka elektriginin yuzde kacini ruzgardan elde eder?", "opts": ["%20", "%35", "%50+", "%75"], "answer": 2}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Okyanuslarin Gizemi - Derin Deniz Yaratiklari",
                    "content": [
                        "Okyanuslarin yuzde 80'den fazlasi henuz kesfedilmemistir. Derin deniz, 200 metreden daha derindeki bolgeleri kapsar ve Dunya yuzeyinin yuzde 65'inden fazlasini olusturur. Bu karanlik dunyada benzersiz yasam formları bulunmaktadir.",
                        "Biyoluminesans, derin deniz canlilarinin en dikkat cekici ozelligidir. Balon baligi, vampir kalamar ve derin deniz yildiz baligi gibi turler kendi isklarini uretebilir. Bu isik avlanma, savunma ve eslesme icin kullanilir.",
                        "Mariana Cukuru, okyanusların en derin noktasi olup 10.994 metre derinlige ulasmaktadir. Bu asiri basinca ragmen, 2019'da Victor Vescovo'nun dalisiyla cukurun dibinde bile yasam kesfedilmistir. Asiri basinca, soguga ve karanliga uyum saglamis organizmalar bilim insanlarini sasirtmaktadir.",
                        "Derin deniz hidrotermal bacalari, gunes isigi olmadan yasam destekleyen ozel ekosistemlerdir. Kemosentez yapan bakteriler bu ekosistemlerin temelini olusturur. Bu kesif, uzaydaki okyanus dunya larında (Europa, Enceladus) yasam arayisina ilham vermistir."
                    ],
                    "quiz": [
                        {"q": "Okyanuslarin yuzde kaci henuz kesfedilmemistir?", "opts": ["%30", "%50", "%65", "%80+"], "answer": 3},
                        {"q": "Mariana Cukuru kac metre derinliktedir?", "opts": ["5.000 m", "7.500 m", "10.994 m", "15.000 m"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Cevre Hareketinin Tarihi",
                    "content": [
                        "Modern cevre hareketi, Rachel Carson'in 1962'de yayimladigi 'Sessiz Bahar' (Silent Spring) kitabiyla baslamistir. Kitap, pestisitlerin dogaya verdigi zarari belgeleyerek kamU bilincini uyandirmistir. DDT'nin yasaklanmasi bu kitabin dogrudan etkilerinden biridir.",
                        "22 Nisan 1970'te ilk Dunya Gunu kutlamasi ABD'de 20 milyon insanin katilimiyla gerceklesmistir. Bu hareket, ABD Cevre Koruma Ajansi'nin (EPA) kurulmasina ve Temiz Hava Kanunu'nun cikarilmasina yol acmistir.",
                        "1987'de yayimlanan Brundtland Raporu 'surdurulebilir kalkinma' kavramını dünyaya tanitmistir. 1992 Rio Dunya Zirvesi, iklim degisikligi ve biyocesitlilik konularinda uluslararasi isbirliginin temellerini atmistir.",
                        "2018'de Greta Thunberg'in baslattigi 'Gelecek icin Cuma' (Fridays for Future) hareketi, genc nesillerin cevre mucadelesindeki rolunu on plana cikmistir. 2015 Paris Iklim Anlasmasi ile 196 ulke karbon emisyonlarini azaltma taahhudunde bulunmustur."
                    ],
                    "quiz": [
                        {"q": "'Sessiz Bahar' kitabinin yazari kimdir?", "opts": ["Al Gore", "Rachel Carson", "Jane Goodall", "David Attenborough"], "answer": 1},
                        {"q": "Ilk Dunya Gunu hangi yil kutlanmistir?", "opts": ["1962", "1970", "1987", "1992"], "answer": 1}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Doga Fotografciligi Sanati",
                    "content": [
                        "Doga fotografciligi, vahsi yasami ve dogal peyzajlari belgeleyerek hem sanat hem bilim icin degerli bir araçtir. National Geographic dergisi 1888'den bu yana dunyanin en etkileyici doga fotograflarini yayimlamaktadir.",
                        "Basarili bir doga fotografcisi icin sabir, teknik bilgi ve doga anlayisi gerekir. Isik, kompozisyon ve zamanlama kiritik oneme sahiptir. Altin saatler (gun dogumu ve gun batimi) en dramatik isik kosullarini sunar.",
                        "Dijital teknoloji doga fotografciligini donusturmustur. Drone fotografciligi yukaridan benzersiz perspektifler sunarken, kamera tuzaklari vahsi hayvanlari rahatsiz etmeden goruntulemeye olanak tanir. Zaman atlamali (time-lapse) teknik dogadaki yavas değisimleri gorunur kılar.",
                        "Turkiye, doga fotografcilari icin cennet gibi bir ulkedir. Kapadokya'nin peribacalari, Pamukkale'nin travertenleri, Kackar Daglari'nin yaylalari ve Bolu'nun ormanlari doga fotografcılıgı için essis mekanlar sunar."
                    ],
                    "quiz": [
                        {"q": "Doga fotografciligi icin en ideal isik kosullari ne zaman olusur?", "opts": ["Oglen", "Gece", "Altin saatler (gun dogumu/batimi)", "Bulutlu hava"], "answer": 2},
                        {"q": "National Geographic dergisi hangi yildan bu yana yayindadir?", "opts": ["1860", "1888", "1920", "1950"], "answer": 1}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Doga Sporlari - Dagcilik, Sorf, Kano",
                    "content": [
                        "Dagcilik, insanlik tarihinin en eski macera sporlarilarından biridir. Dunyanin en yuksek noktasi Everest (8.849 m) ilk kez 1953'te Edmund Hillary ve Tenzing Norgay tarafindan tirmanilmistir. Bugüne kadar 6.000'den fazla kisi zirveye ulasmistir.",
                        "Sorf, Polinezya kulturunde binlerce yillik bir gecmise sahiptir. Hawaii'de dogmus olan modern sorf, 1960'lardan itibaren kuresel bir fenomene donusmustur. 2020 Tokyo Olimpiyatlari'nda ilk kez olimpik bir spor olarak kabul edilmistir.",
                        "Kano ve kayak sporlari hem rekreasyonel hem yarismaci duzeyde yapilmaktadir. Beyaz su raftingi, adrenalin arayanlar icin populerken, deniz kayagi sakin sularda doga kesfine olanak tanir. Turkiye'nin Koprulu Kanyon, Zamanti ve Coruh Vadisi rafting icin ideal noktalardir.",
                        "Doga sporlari yapilirken cevre bilincı ve guvenlik kurallarına uyulmalıdır. Iz birakmama (Leave No Trace) ilkeleri, doganin korunmasini saglar. Uygun ekipman, egitim ve deneyimli rehberlerle bu sporlar guvenle yapilabilir."
                    ],
                    "quiz": [
                        {"q": "Everest ilk kez hangi yil tirmanilmistir?", "opts": ["1924", "1938", "1953", "1965"], "answer": 2},
                        {"q": "Sorf hangi olimpiyatta ilk kez yer almistir?", "opts": ["2012 Londra", "2016 Rio", "2020 Tokyo", "2024 Paris"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Mayis 2026", "sayi": 9, "tema": "Genclik ve Gelecek",
            "kapak_emoji": "\U0001f680", "kapak_renk": "#ea580c",
            "editorial": "19 Mayis Genclik ve Spor Bayrami'na ozel bu sayimizda gelecege yonelik heyecan verici konulari ele alıyoruz. Mars'tan 3D baskiya, arilardan genc girisimcilere ilham verici bir sayi!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Mars'a Yolculuk - Kizil Gezegen Kolonisi",
                    "content": [
                        "Mars, Dunya'ya en cok benzeyen gezegen olup insanligin uzay kolonizasyonu icin en guclu adaydir. Bir gunu 24 saat 37 dakikadir, mevsimleri vardir ve kutuplarinda su buzunun bulundugu dogrulanmistir. NASA'nın Perseverance robotu 2021'den beri Mars yuzeyinde arastirma yapmaktadir.",
                        "Dunya'dan Mars'a yolculuk mevcut teknolojiyle yaklasik 7-9 ay surmektedir. SpaceX'in Starship roketi, 100 yolcu tasiyabilen ve yeniden kullanilabilir bir uzay araci olarak tasarlanmistir. Elon Musk, 2030'lara kadar insanli Mars misyonu hedeflemektedir.",
                        "Mars'ta yasam icin kritik zorluklar vardir: ince atmosfer (yuzde 95 CO2), dusuk sicakliklar (ortalama -60°C), yuksek radyasyon ve dusuk yercekimi (Dunya'nin yuzde 38'i). Habitat tasarimlari bu kosullara dayanikli olmak zorundadir.",
                        "Terraforming (gezegen donustürme), Mars'i uzun vadede yasilanabilir kilma vizyonudur. Sera gazlari salarak atmosferi kalinlastirma, kutup buzlarini eritme ve bitki yetistirme gibi adimlar oneriImektedir. Ancak bu surecin yuzlerce yil alabileceği tahmin edilmektedir."
                    ],
                    "quiz": [
                        {"q": "Mars'taki bir gun yaklasik ne kadar surer?", "opts": ["20 saat", "24 saat 37 dk", "28 saat", "36 saat"], "answer": 1},
                        {"q": "Mars'in yercekimi Dunya'nin yuzde kacidir?", "opts": ["%17", "%38", "%50", "%75"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "3D Baski ile Gelecegi Insa Etmek",
                    "content": [
                        "3D baski (katmanli imalat), dijital modelden fiziksel nesneler ureten bir teknolojidir. 1980'lerde gelistirilen bu teknoloji, bugün plastikten metale, betondan biyolojik dokuya kadar pek cok malzemeyle calismaktadir.",
                        "Tip alanında 3D baski hayat kurtarmaktadir. Kisisellestirilmis protezler, implantlar ve cerrahi modeller rutın olarak uretilmektedir. Biyobaski (bioprinting) teknolojisiyle canli dokular uretilmekte, gelecekte organ nakli ihtiyacını ortadan kaldirmasi beklenmektedir.",
                        "Insaat sektorunde 3D baski ile evler insa edilmektedir. ICON sirketi, 24 saat icinde yasilanabilir bir ev basabilmektedir. Bu teknoloji ozellikle afet sonrasi konut ihtiyacı ve uygun fiyatli konut problemine cozum sunma potansiyeline sahiptir.",
                        "Uzay arastirmalarinda 3D baski kritik bir rol oynamaktadir. Uluslararasi Uzay Istasyonu'nda yedek parca basılabilmektedir. Mars kolonisi senaryolarin da habitatların yerli malzemelerle 3D basilmasi planlanmaktadir."
                    ],
                    "quiz": [
                        {"q": "3D baski teknolojisi ilk olarak hangi onyilda gelistirilmistir?", "opts": ["1960'lar", "1970'ler", "1980'ler", "1990'lar"], "answer": 2},
                        {"q": "ICON sirketi 3D baski ile ne kadar surede ev insa edebilir?", "opts": ["6 saat", "24 saat", "1 hafta", "1 ay"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Arilarin Super Gucu - Polinasyon",
                    "content": [
                        "Arilar, dunyadaki gida uretiminin yaklasik ucte birinden sorumludur. Tozlasma (polinasyon) bitkilerin ureyebilmesi icin hayati onem tasir. Bir bal arisi kolonisi günde 300 milyon cicegi ziyaret edebilir.",
                        "Bal arilari mükemmel matematikciilerdır. Peteklerini altigen (heksagonal) sekilde insa ederler; bu sekil, en az malzemeyle en fazla depolama alanı saglayan geometrik formudur. Her arinin kovanadaki rolu (kralice, isci, erkek) kesin olarak belirlidir.",
                        "Koloni Cokme Bozuklugu (CCD), 2006'dan beri ari popuelasyonlarini ciddi sekilde tehdit etmektedir. Pestisitler, habitat kaybi, parazitler (Varroa akari) ve iklim degisikligi bu sorunun ana nedenleri arasindadir. ABD'de ari kolonilerinin yuzde 40'i her yil kaybedilmektedir.",
                        "Arilarin korunmasi icin herkes katkida bulunabilir. Bahcenizde yerli cicek turlerl dikmek, pestiit kullaninmni azaltmak ve arı dostu alanlar olusturmak onemli adimlardir. Albert Einstein'a atfedilen 'Arilar yok olursa insanlık 4 yil icinde yok olur' sozu, onların kritik rolunu vurgular."
                    ],
                    "quiz": [
                        {"q": "Arilar dunyadaki gida uretiminin yaklasik ne kadarindan sorumludur?", "opts": ["1/10", "1/5", "1/3", "1/2"], "answer": 2},
                        {"q": "Koloni Cokme Bozuklugu (CCD) hangi yildan beri ciddi bir sorundur?", "opts": ["1990", "2000", "2006", "2015"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Genclik Hareketleri Dunyayi Nasil Degistirdi?",
                    "content": [
                        "Genclik hareketleri tarih boyunca toplumsal degisimin itici gucu olmustur. 1960'larin ogrenci hareketleri ABD, Fransa ve dunyanin pek cok ulkesinde sivil haklar, savaş karsıtligi ve toplumsal esitlik taleplerini gundeme getirmistir.",
                        "1968 Parıs ogrenci olaylari, Fransa'da genel grev ve siyasi krize yol acmistir. ABD'de Martin Luther King Jr. ve ogrenci aktivistler sivil haklar mucadelesinde belirleyici roller oynamistir. Bu hareketler, dunya genelinde demokratiklesme sureclerini hizlandirmistir.",
                        "Teknoloji, genc aktivizmi donusturmustur. Arap Bahari (2011) sirasinida sosyal medya, genclerin orgutlenmesinde kritik bir arac olmustur. Hong Kong semsiye hareketi (2014) ve iklim grevleri dijital aktivizmin gücünü gostermistir.",
                        "Turkiye'de 19 Mayis 1919, gencliğin ulusal mucadeledeki rolunun simgesidir. Mustafa Kemal'in Samsun'a cikisiyla baslayan surecte gencler, Kurtulus Savasi'nin ve Cumhuriyet'in kurulusunun oncu kuvvetlerinden olmustur."
                    ],
                    "quiz": [
                        {"q": "1968 ogrenci olaylari hangi sehirde buyuk etkiye yol acmistir?", "opts": ["Londra", "Berlin", "Paris", "Roma"], "answer": 2},
                        {"q": "19 Mayis 1919'da Mustafa Kemal hangi sehre cikmistir?", "opts": ["Istanbul", "Ankara", "Samsun", "Erzurum"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Genc Girisimciler - Ilham Veren Hikayeler",
                    "content": [
                        "Mark Zuckerberg, Facebook'u 19 yasinda Harvard yurt odasında kurmustur. Steve Jobs, Apple'i 21 yasinda garajindan baslatmistir. Bu hikayeler, yasin basarı icin engel olmadigini gostermektedir.",
                        "Malala Yousafzai, 15 yasinda Taliban'in saldirısına ugradiktan sonra kizlarin egitim hakki icin kuresel bir sembol olmus ve 17 yasinda Nobel Baris Odulu'nu almistir. Greta Thunberg ise 15 yasinda baslattigi iklim greviyle dunyanin gundemini degistirmistir.",
                        "Turkiye'de genc girisimcilik ekosistemi hizla büyümektedir. Peak Games, Trendyol ve Dream Games gibi genc kurucularin basardigi sirketler milyar dolar degerleme yakalamnistir. Universite ogrencileri teknoloji yarismalarinda dunya capında basarilar elde etmektedir.",
                        "Basarili girisimcilerin ortak ozellikleri problem cözme yeteneği, azim, ogrenmeye aciklik ve risk alabilme cesaretidir. Basarisizlik korkusu en buyuk engellerden biridir, ancak cogu basarili girisimci birden fazla basarisizlik deneyiminden gecmistir."
                    ],
                    "quiz": [
                        {"q": "Mark Zuckerberg Facebook'u kac yasinda kurmustur?", "opts": ["17", "19", "21", "23"], "answer": 1},
                        {"q": "Malala Yousafzai kac yasinda Nobel Odulu almistir?", "opts": ["15", "16", "17", "18"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "19 Mayis - Genclik ve Spor Bayrami",
                    "content": [
                        "19 Mayis Ataturk'u Anma, Genclik ve Spor Bayrami, 1919'da Mustafa Kemal'in Samsun'a cikisiyla baslayan ulusal mucadelenin anisinma kutlanir. Ataturk bu tarihi Turk gencligine armagam etmistir.",
                        "Bayram kapsaminda ulke genelinde spor yarismalari, genclik senlikleri ve stadyum gosterileri duzenlenir. Okullarda ozel programlar yapilir, ogrenciler atletizm, jimnastik ve takim sporlarinda yeteneklerini sergiler.",
                        "Ataturk'un 'Turkiye Cumhuriyeti'nin temeli kulturdu' sozu, gencligin egitim ve spor yoluyla gelisiminin onemine isaret eder. Sporun sadece fiziksel degil, zihinsel ve karakter gelisimi acisindan da onemi vurgulanmistir.",
                        "Bugün Turkiye'de 15 milyondan fazla genc nufus bulunmaktadir. Gencler, bilim, teknoloji, sanat ve spor alanlarinda uluslararasi arenada ulkemizi basariyla temsil etmektedir. 19 Mayis, bu potansiyelin kutulandigi ozel bir gundur."
                    ],
                    "quiz": [
                        {"q": "19 Mayis 1919'da hangi olay gerceklesmistir?", "opts": ["TBMM'nin acilisi", "Cumhuriyet'in ilani", "Mustafa Kemal'in Samsun'a cikisi", "Lozan Barisi"], "answer": 2},
                        {"q": "Ataturk 19 Mayis'i kime armagan etmistir?", "opts": ["Turk ordusuna", "Turk gencligine", "Turk kadinina", "Turk milletine"], "answer": 1}
                    ]
                }
            ]
        },
        {
            "month": "Haziran 2026", "sayi": 10, "tema": "Yaz Tatili",
            "kapak_emoji": "\u2600\ufe0f", "kapak_renk": "#f59e0b",
            "editorial": "Yaz tatili basliyor! Bu sayimizda gunes sisteminden deniz kaplumbagalarina, antik olimpiyatlardan yuzme tekniklerine kadar yaza ozel konularla karsinızdayız. Keyifli bir yaz gecirmenizi diliyoruz!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Gunes Sistemi Rehberi - 8 Gezegen",
                    "content": [
                        "Gunes Sistemi, yaklasik 4.6 milyar yil once bir gaz ve toz bulutunun cökmesiyle olusmustur. Merkur, Venus, Dunya ve Mars kayalik (yersel) gezegenler olarak siniflandirilirken; Jupiter, Saturn, Uranus ve Nephin gaz/buz devleridir.",
                        "Jupiter, Gunes Sistemi'nin en buyuk gezegenidir; capi Dunya'nin 11 katindan fazladir ve 79'dan fazla uydusu vardir. Buyuk Kirmizi Leke, 350 yildir suregelen ve Dunya'dan buyuk bir firtinaidr. Saturn'un halkalari buz parcaciklari ve kaya parcacilarindan olusur.",
                        "Dunya, bilinen tek yasilanabilir gezegendir. 'Goldilocks bolgesi' adi verilen yasilanabilir kusakia konumlanmistir; Gunes'e ne çok yakin ne cok uzaktir, bu da suyun sivi halde kalmasına izin verir. Atmosferimiz ve manyetik alanımiz bizi uzay radyasyonundan korur.",
                        "Pluton, 2006'da Uluslararasi Astronomi Birligi (IAU) tarafindan cuce gezegen olarak yeniden siniflandirilmistir. New Horizons sondasi 2015'te Pluton'un yakindan göruntülerini cekmis ve yuzeyinde azot buzulları ve dag siralari kesfetmistir."
                    ],
                    "quiz": [
                        {"q": "Gunes Sistemi yaklasik kac yil once olusmustur?", "opts": ["1 milyar", "2.5 milyar", "4.6 milyar", "10 milyar"], "answer": 2},
                        {"q": "Pluton hangi yil cuce gezegen olarak siniflandirilmistir?", "opts": ["2000", "2003", "2006", "2010"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Yaz Icin En Iyi Egitici Uygulamalar",
                    "content": [
                        "Dijital ogrenme platformlari yaz tatilinde oğrencilerin bilgilerini taze tutmasi icin mukemmel araclardir. Khan Academy, tum sinif seviyelerinde ucretsiz matematik, fen ve programlama dersleri sunar. Duolingo ile yaz boyunca yeni bir dil ogrenilebilir.",
                        "Kodlama egitimi icin Scratch (baslangic) ve Code.org (orta seviye) platformlari gencler arasinda populerdir. Python ogrenmek isteyen ogrenciler Codecademy ve freeCodeCamp gibi interaktif platformlari kullanabilir.",
                        "Bilim meraklilari icin NASA'nin uygulamalari, Star Walk (yildiz haritasi) ve iNaturalist (dogadaki turleri tanimlama) harika seceneklerdir. Podcast dinleme aliskanligi edinmek de yaz icin tavsiye edilir; TED Talks, bilimsel konularda kisa ve ilham verici sunumlar sunar.",
                        "Ekran suresi yonetimi yaz tatilinde de önemlidir. Dijital ogrenmenin yaninda kitap okuma, doga gezileri ve fiziksel aktiviteler dengelenmelidir. Pomodoro teknigi (25 dk calisma + 5 dk mola) etkili bir zaman yonetim araci olarak kullanilabilir."
                    ],
                    "quiz": [
                        {"q": "Khan Academy hangi turde egitim icerikleri sunar?", "opts": ["Sadece matematik", "Sadece dil", "Cok alanli ucretsiz egitim", "Sadece kodlama"], "answer": 2},
                        {"q": "Pomodoro tekniginde calisma suresi ne kadardir?", "opts": ["15 dakika", "25 dakika", "45 dakika", "60 dakika"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Deniz Kaplumbagalari ve Yuvalama Sezonu",
                    "content": [
                        "Deniz kaplumbagalari 100 milyon yildan fazla suredir okyanuslarda yasamakta olup dinozorlardan daha eski canlılardir. Dunya'da 7 deniz kaplumbagasi turu bulunur ve hepsi tehdit altindadir. Yesil kaplumbaga ve caretta caretta en bilinen turlerdir.",
                        "Her yaz, disi kaplumbagalar dogdukları sahillere geri donerek yumurtalarini birakir. Bir yuva 50-200 yumurta icerir ve kum sicakligi yavruların cinsiyetini belirler: yüksek sicaklik disi, dusuk sicaklik erkek bireyler uretir. Yavrular 45-70 gun sonra yumurtadan cikar.",
                        "Turkiye, Akdeniz'deki en onemli deniz kaplumbagasi yuvalama alanlarina ev sahipligi yapar. Dalyan (Iztuzu), Belek, Anamur ve Mersin sahilleri koruma altindaki yuvalama bolgelerdir. DEKAMER (Deniz Kaplumbagalari Arastirma, Kurtarma ve Rehabilitasyon Merkezi) bu cabalarin oncusudur.",
                        "Isik kirliligi, plastik atiklar, habitat kaybi ve iklim degisikligi deniz kaplumbagalarinin en buyuk tehditleridir. Sahillerdeki yapay isiklar yavruların denizi bulmalarini engeller. Plastik torbalar deniz anasina benzedigi icin kaplumbagalar tarafindan yutulabilir."
                    ],
                    "quiz": [
                        {"q": "Deniz kaplumbagalari yaklasik ne kadar suredir yasamaktadir?", "opts": ["1 milyon yil", "10 milyon yil", "50 milyon yil", "100+ milyon yil"], "answer": 3},
                        {"q": "Yumurtadan cikan yavruların cinsiyetini ne belirler?", "opts": ["Genetik", "Kum sicakligi", "Ay fazlari", "Deniz suyu tuzu"], "answer": 1}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Antik Olimpiyatlar'dan Modern Oyunlara",
                    "content": [
                        "Antik Olimpiyat Oyunlari MO 776'da Yunanistan'in Olympia sehrinida baslamistir. Her dort yilda bir duzenlenen yarismalarda atletizm, gures, boks ve araba yarislari yapilirdi. Oyunlar sirasinda Yunan sehir devletleri arasinda savaslara ara verilirdi (Kutsal Baris).",
                        "Antik Olimpiyatlar MS 393'te Roma Imparatoru Theodosius tarafindan pagan bir festival olarak gorulerek yasaklanmistir. Yaklasik 1.500 yil sonra, Pierre de Coubertin'in cabalariyla 1896'da Atina'da modern Olimpiyat Oyunlari yeniden baslatılmistir.",
                        "Kadinlar ilk kez 1900 Paris Olimpiyatlari'nda yarismistir. O zamanki 22 spor dalinin sadece ikisine (tenis ve golf) katilabilmislerdir. Bugün kadinlar tum dallarda yarisabilmekte ve sporcu sayisi neredeyse erkeklerle esitlenmistir.",
                        "Olimpiyat mesalesi geleneği 1936 Berlin Oyunlari'nda baslatilmistir. Bes halka amblemi bes kitayi temsil eder ve Pierre de Coubertin tarafindan 1913'te tasarlanmistir. 'Daha hizli, daha yuksek, daha guclu' mottosu 2021'de 'birlikte' kelimesi eklenerek guncellenmistir."
                    ],
                    "quiz": [
                        {"q": "Antik Olimpiyat Oyunlari hangi yil baslamistir?", "opts": ["MO 1000", "MO 776", "MO 500", "MO 200"], "answer": 1},
                        {"q": "Kadinlar ilk kez hangi Olimpiyatlarda yarismistir?", "opts": ["1896 Atina", "1900 Paris", "1908 Londra", "1920 Antwerp"], "answer": 1}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Yaz Okuma Listesi - 10 Kitap Onerisi",
                    "content": [
                        "Yaz tatili, okuma aliskanligi edinmek veya guclendirimek icin ideal bir donemdir. Antoine de Saint-Exupery'nin 'Kucuk Prens'i her yasta okunabilecek evrensel bir basayapittir. George Orwell'in '1984'u, dijital cagda her zamankinden daha gunceldir.",
                        "Bilim kurgu sevenler icin Isaac Asimov'un 'Vakif' serisi ve Frank Herbert'in 'Kumul'u (Dune) mutlaka okunmasi gereken eserlerdir. Macera arayanlar icin Jules Verne'in 'Denizler Altında 20.000 Fersah'i ve Daniel Defoe'nun 'Robinson Crusoe'su klasikler arasındadir.",
                        "Turk edebiyatından Yasar Kemal'in 'Ince Memed'i Anadolu'nun destansi anlatımıyla buyuler. Sabahattin Ali'nin 'Kuyucakli Yusuf'u ve 'Madonna Bir Kurk Manto' eserleri derin insan hikayeleri sunar. Resat Nuri Guntekin'in 'Calikusu' ise Anadolu'nun ve bir ogretmenin hikayesini anlatır.",
                        "Iyi bir okuma aliskanligi icin gunluk en az 20 dakika okuma hedefi konulabilir. Bir okuma gunlugu tutmak, okunan kitaplar hakkinda notlar almak ve kitap kulupleri kurmak okuma deneyimini zenginlestirir."
                    ],
                    "quiz": [
                        {"q": "'Kucuk Prens' hangi yazar tarafindan yazilmistir?", "opts": ["Victor Hugo", "Saint-Exupery", "Jules Verne", "Albert Camus"], "answer": 1},
                        {"q": "'Calikusu' hangi Turk yazarinın eseridir?", "opts": ["Yasar Kemal", "Orhan Pamuk", "Resat Nuri Guntekin", "Halide Edib Adivar"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Yuzme Bilim ve Teknigi",
                    "content": [
                        "Yuzme, tum vucut kaslarini calistiran ve eklemlere en az yuk bindiren sporlardan biridir. Bir saatlik yuzme 400-700 kalori yakabilir. Suyun kaldirrma kuvveti sayesinde sakatlık riski diger sporlara gore cok dusuktur.",
                        "Dort temel yuzme stili vardir: serbest stil (krawl), sirtüstü, kurbagalama ve kelebek. Serbest stil en hizli yuzme stiliyken, kelebek en zor teknik olarak kabul edilir. Her stilin kendine ozgu kolcek ve ayak vurusu teknigi vardir.",
                        "Michael Phelps, 28 olimpiyat madalyasiyla (23 altin) tarihinin en basarili olimpik sporcusudur. Phelps'in 2.01 m boyunda oldugune ragmen ayak numarasi 47'dir ve kol acikligi boyundan 10 cm uzundur; bu fiziksel ozellikler ona suda avantaj saglamistir.",
                        "Turkiye'nin uc tarafinin denizlerle cevrili olmasi yüzme sporu icin dogal bir avantajdir. Derya Buyukuncu Türk yüzme tarihinin onculerinden olup, cocuklara yuzme ogretim programlarI ulke genelinde yayginlasmaktadir."
                    ],
                    "quiz": [
                        {"q": "En hizli yuzme stili hangisidir?", "opts": ["Kurbagalama", "Serbest stil", "Kelebek", "Sirtüstü"], "answer": 1},
                        {"q": "Michael Phelps toplam kac olimpiyat madalyasi kazanmistir?", "opts": ["22", "25", "28", "30"], "answer": 2}
                    ]
                }
            ]
        },
        {
            "month": "Temmuz 2026", "sayi": 11, "tema": "Kesif Zamani",
            "kapak_emoji": "\U0001f9ed", "kapak_renk": "#7c2d12",
            "editorial": "Temmuz sayimizda keşfin heyecanini yasiyoruz! Galaksilerden Amazon ormanlarına, buyuk kasiflerden su sporlarına, macera dolu bir yaz sayisi sizlerle!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "Derin Uzay - Galaksiler ve Nebulalar",
                    "content": [
                        "Gozlemlenebilir evrende yaklasik 2 trilyon galaksi bulundugu tahmin edilmektedir. Samanyolu galaksimiz 100-400 milyar yildiz icerir ve yaklasik 100.000 isik yili capindadir. Gunes, merkeze 26.000 isik yili uzakliktaki bir spiral kolda yer alir.",
                        "Nebulalar (bulutsu), uzaydaki gaz ve toz bulutlaridir. Yildiz dogum nebulalari (Kartal Nebulasi gibi) yeni yildizlarin olustuğu bolgelerdir. Gezegen nebulalari ise olmeye yüz tutmus yildizlarin dis katmanlarini uzaya savurmasiyla olusur.",
                        "Andromeda galaksisi, Samanyolu'na en yakin buyuk galaksi olup 2.5 milyon isik yili uzakliktadir. Iki galaksi saniyede 110 km hizla birbirine yaklasmanktadir ve yaklasik 4.5 milyar yıl sonra birlesecektir. Bu cakisma gorkemli yeni bir galaksi olusturacaktir.",
                        "Kara madde ve kara enerji, evrenin yuzde 95'ini olusturmasina ragmen doğrudan gozlenememektedir. Kara madde yerçekim etkisi ile varlıgini belli ederken, kara enerji evrenin genislemesini hızlandiran gizemli kuvvettir. Bunları anlamak modern fizigin en buyuk sorusudur."
                    ],
                    "quiz": [
                        {"q": "Gozlenebilir evrende yaklasik kac galaksi oldugu tahmin edilir?", "opts": ["100 milyar", "500 milyar", "2 trilyon", "10 trilyon"], "answer": 2},
                        {"q": "Andromeda galaksisi Samanyolu'na ne kadar uzaktadir?", "opts": ["100.000 isik yili", "1 milyon isik yili", "2.5 milyon isik yili", "10 milyon isik yili"], "answer": 2}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Dronelar - Havadan Kesif Teknolojisi",
                    "content": [
                        "Dronelar (insansiz hava araclari), askeri amaclı kullanımdan ticari ve bireysel kullanıma hizla evrilmistir. 2024'te kuresel drone pazari 40 milyar dolari asmistir. Tarim, haritalama, kargo teslimatı ve acil yardim alanlarinda yaygin kullanilmaktadir.",
                        "Tarimda dronelar, genis arazilerin havadan taranmasi, hastalikli bitkilerin tespit edilmesi ve hassas ilaclama yapmak icin kullanilmaktadir. Bir drone, bir gundelik iscinin bir haftada yapacagi ilaclama isini birkaç saatte tamamlayabilir.",
                        "Kargo teslimati alaninda Amazon Prime Air ve Wing (Google) gibi projeler, dronelarla paket teslimatini gerceklestirmektedir. Saglik alaninda, Rwanda'da Zipline sirketi kan ve ilac teslimatını uzak koylere dronelarla yapmaktadir.",
                        "Turkiye, drone teknolojisinde dunya liderleri arasindadir. Bayraktar TB2 ve Akıncı TİHA'lar savunma sanayisinde buyuk basari elde etmistir. Sivil drone kullanimi icin SHGM (Sivil Havacilik Genel Mudurlugu) tarafindan belirlenen kurallara uyulmasi gerekmektedir."
                    ],
                    "quiz": [
                        {"q": "2024'te kuresel drone pazari ne kadardir?", "opts": ["10 milyar $", "25 milyar $", "40 milyar $", "80 milyar $"], "answer": 2},
                        {"q": "Zipline sirketi dronelarla hangi ulkede saglik malzemesi tasımaktadir?", "opts": ["Kenya", "Rwanda", "Gana", "Nijerya"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Amazon Yagmur Ormanlari - Dunya'nin Cigerleri",
                    "content": [
                        "Amazon yagmur ormani, 5.5 milyon km2'lik alaniyla dunyanin en buyuk tropik ormanidir. 9 ulkeye yayilmis olup Brezilya toprakılarinin yuzde 60'ini kaplar. Dunya oksijen uretiminin yaklasik yuzde 6-9'unu saglar ve kuresel iklim duzenlemesinde kritik rol oynar.",
                        "Amazon, biyolojik çesitlilik acisindan dunya sampiyonudur. 80.000 bitki turu, 2.5 milyon bocek turu, 2.000 kus turu ve 400'den fazla memeli turu burada yasar. Her yil yeni turler kesfedilmeye devam etmektedir.",
                        "Orman tahribati Amazon'un en buyuk tehditidir. Tarim alanı açma, hayvancılık, madencilik ve yasadisi agac kesimi her yil binlerce km2 ormanin kaybedilmesine neden olmaktadir. 2004-2012 arasinda ormansizlasma orani yuzde 80 azaltilmis, ancak son yillarda yeniden artmistir.",
                        "Amazon nehri, dunyanın en buyuk nehridir (hacim olarak). Saniyede 209.000 m3 su tasir, bu Dunya'daki tum nehirlerin toplam debisinin yuzde 20'sidir. Nehirde 3.000'den fazla balik turu yasar; bunlardan biri olan arapaima 3 metreye ulasabilen dev bir tatli su baligidir."
                    ],
                    "quiz": [
                        {"q": "Amazon yagmur ormani kac milyon km2'lik bir alani kaplar?", "opts": ["2.5", "4.0", "5.5", "8.0"], "answer": 2},
                        {"q": "Amazon nehri tum nehirlerin toplam debisinin yuzde kacini olusturur?", "opts": ["%5", "%10", "%20", "%30"], "answer": 2}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Buyuk Kasifler - Marco Polo'dan Amundsen'e",
                    "content": [
                        "Marco Polo (1254-1324), Venedik'ten Cin'e uzanan yolculuguyla Avrupalilarin Asya hakkindaki bilgisini kokten degistirmistir. 24 yil suren seyahatini anlatan 'Il Milione' (Dunyanin Tasvirı) kitabi, keşif çağinin ilham kaynaklarından olmustur.",
                        "Kristof Kolomb, 1492'de Hindistan'a giden bir bati yolu araırken Amerika kitasına ulasmiştir. Vasco da Gama 1498'de Ümit Burnu'nu dolasarak Hindistan'a deniz yolunu acmistir. Ferdinand Magellan'in filosu 1522'de dunyanin cevresini dolasan ilk sefer olmustur.",
                        "Piri Reis (1465-1554), Osmanlı denizcisi ve kartografi olarak dunya haritacılık tarihinin en onemli isimlerinden biridir. 1513 tarihli duınya haritasi, Amerika kıtalarının ayrintılı betimlemesiyle Avrupali haritalara kıyasla buyuk bir başaridır.",
                        "Roald Amundsen, 1911'de Guney Kutbu'na ulasan ilk insan olmustur. Ernest Shackleton'in Endurance seferi (1914-1917) ise tarihin en dramatik hayatta kalma hikayelerinden biridir. Keşif ruhu bugun uzay arastirmalarıyla devam etmektedir."
                    ],
                    "quiz": [
                        {"q": "Marco Polo'nun seyahati yaklasik kac yil surmustur?", "opts": ["5", "12", "24", "30"], "answer": 2},
                        {"q": "Piri Reis'in unlu dunya haritasi hangi yil cizilmistir?", "opts": ["1453", "1492", "1513", "1570"], "answer": 2}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Dunya Mutfaklari Turu",
                    "content": [
                        "Yemek kulturu, bir toplumun tarihini, cografyasini ve degerlerini yansitan en temel unsurlardan biridir. UNESCO, gastronomiyi somut olmayan kulturel miras kapsaminda degerlendirir. Turk mutfagi, Fransiz ve Cin mutfagiyla birlikte dunyanin en zengin uc mutfagindan biri kabul edilir.",
                        "Italyan mutfagi basitlik ve kaliteli malzeme uzerine kuruludur. Pizza, pasta ve risotto dunyanin en populer yemekleri arasindadir. Japon mutfagi ise dengeye ve estetige onem verir; sushi ve ramen kuresel fenomenler haline gelmistir.",
                        "Turk mutfagi, Orta Asya, Anadolu ve Osmanli geleneklerinin bileşimidir. Kebap cesitleri, meze kulturu, zeytinyagli yemekler ve baklava gibi tatlilar dunya capında taninir. Her bolgenin kendine ozgu yemek gelenekleri vardir: Gaziantep baklava ve lahmacun, Trabzon kuymak ve hamsi, Adana kebap.",
                        "Yemek bilimi (gastronomi) son yillarda büyük gelisme gostermistir. Molekuler gastronomi, kimya ve fiziği mutfaga tasıyarak yemek hazirlama tekniklerini yeniden tanimlamistir. Ferré Adria ve Heston Blumenthal bu akimin onculeridır."
                    ],
                    "quiz": [
                        {"q": "Dunyanin en zengin uc mutfagi arasinda hangisi yer almaz?", "opts": ["Turk", "Cin", "Hint", "Fransiz"], "answer": 2},
                        {"q": "Molekuler gastronomi hangi bilim dallarini mutfaga tasir?", "opts": ["Biyoloji ve tip", "Kimya ve fizik", "Matematik ve istatistik", "Psikoloji ve sosyoloji"], "answer": 1}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Su Sporlari - Yelken, Kurek, Dalis",
                    "content": [
                        "Su sporlari, insanligin suyla olan kadim iliskisini yansitur. Yelken, ruzgarin gucunu kullanarak suyu keşfetmenin en eski yollarindan biridir. America's Cup (1851'den beri) dunyanin en eski uluslararası spor yarismasidir.",
                        "Kurek, Olimpiyat programindaki en eski sporlardan biri olup 1896'da programa alınmistir (ama kotu hava nedeniyle 1900'da ilk kez yapilmistir). Oxford-Cambridge kurek yarisi 1829'dan beri devam eden geleneksel bir rekabettir.",
                        "Tupled dalis (scuba diving), Jacques Cousteau ve Emile Gagnan'in 1943'te gelistirdigi aqualung ile popularlesmiştir. Bugün dunyadamn 30 milyondan fazla sertifikali dalgic vardir. Turkiye'nin Ege ve Akdeniz kiyilari dalis icin dunyanin en guzel noktarindan bazılarini sunar.",
                        "Turkiye'de su sporlari özellikle Ege ve Akdeniz kiyilarında populerdir. Bodrum, Fethiye ve Kas ruzgar sorfu, yelken ve dalis icin uluslararasi standartlarda tesislere sahiptir. Turkiye Yelken Federasyonu olimpik basarilar hedeflemektedir."
                    ],
                    "quiz": [
                        {"q": "America's Cup hangi yildan beri duzenlennoktedir?", "opts": ["1800", "1851", "1896", "1920"], "answer": 1},
                        {"q": "Aqualung'u kim gelistirmistir?", "opts": ["Hans Hass", "Jacques Cousteau", "Sylvia Earle", "Robert Ballard"], "answer": 1}
                    ]
                }
            ]
        },
        {
            "month": "Agustos 2026", "sayi": 12, "tema": "Yil Sonu Ozel",
            "kapak_emoji": "\U0001f3c6", "kapak_renk": "#b91c1c",
            "editorial": "Egitim ogretim yilinin son sayisina ulastik! Bu ozel sayimizda yilin bilimsel kesiflerinden gelecegin teknolojilerine, nesli tukenen turlerden yilin spor olaylarina kadar genis bir ozetle vedalasiyoruz. Gelecek yil gorusmek uzere!",
            "articles": [
                {
                    "cat": "Bilim", "icon": "\U0001f52c",
                    "title": "2026'nin En Buyuk Bilimsel Kesifleri",
                    "content": [
                        "Bilim dunyasi her yil heyecan verici kesfilerle dolup tasar. Genom duzenlemeden yapay zeka araştırmalarına, uzay kesfinden malzeme bilimine kadar pek cok alanda çığır acan calismalar yapilmaktadir.",
                        "Norobılim alanında beyin-bilgisayar arayuzleri onemli ilerlemeler kaydetmistir. Felcli hastalarin sadece dusunce guculeriyle yazı yazabilmesi, robotik kolları kontrol edebilmesi artik bir gerceklik haline gelmistir.",
                        "Iklim biliminde yapay zekanin kullanımı hava tahminlerını devrimsel olcude iyilestirmistir. Google DeepMind'in GraphCast modeli, geleneksel hava tahmin modellerini dogruluk acisindan gercek zamanda geride birakmistir.",
                        "Fuzyın enerjisinde de umut verici gelismeler yasanmaktadir. Ulusal Ateslleme Tesisi (NIF) 2022'deki basarısının ardindan, net enerji kazanci elde etme calismalarina devam etmektedir. Fuzyın gerceklesirse sınırsız ve temiz enerji mumkun olacaktir."
                    ],
                    "quiz": [
                        {"q": "Google DeepMind'in hava tahmin modeli hangisidir?", "opts": ["AlphaFold", "GraphCast", "Gemini", "WaveNet"], "answer": 1},
                        {"q": "Fuzyon enerjisi gerceklesirse ne saglanacaktir?", "opts": ["Ucuz petrol", "Sinırsız temiz enerji", "Hizli internet", "Uzay yolculugu"], "answer": 1}
                    ]
                },
                {
                    "cat": "Teknoloji", "icon": "\U0001f4bb",
                    "title": "Gelecegin Teknolojileri - 2030 Tahminleri",
                    "content": [
                        "2030 yilina kadar yapay genel zeka (AGI) konusunda onemli ilerlemeler beklenmektedir. Mevcut AI sistemleri dar alanlarda insan performansini asarken, genel amaçlı zeka henuz ufukta belirsizdir. Ancak multimodal AI modelleri hizla gelismektedir.",
                        "6G teknolojisinin 2030'larda kullanima girmesi beklenmektedir. 5G'den 100 kat daha hizli olan 6G, holografik iletisimi, uzaktan cerrahiyi ve tam immersif sanal gercekligi mumkun kilacaktir.",
                        "Uzay turizmi ve ticari uzay istasyonlari 2030'a kadar gerceklik olacaktir. SpaceX, Blue Origin ve Virgin Galactic sivil uzay yolcularini tasimaya baslamistir. Ay'a donülmesi ve kalici Ay ussu kurulması planlanmaktadir.",
                        "Biyoteknoloji ve nanoteknoloji birlesiminden ortaya cikan yenilikler saglik sektorunu donusturecektir. Kisiye ozel kanser asilari, nanobotlarla hedefli ilac tedavisi ve 3D basılmis organlar 2030'larin tip dunyanının parcasi olacaktir."
                    ],
                    "quiz": [
                        {"q": "6G teknolojisinin 5G'den kac kat daha hizli olmasi beklenmektedir?", "opts": ["10 kat", "50 kat", "100 kat", "1000 kat"], "answer": 2},
                        {"q": "Asagidakilerden hangisi 2030 icin beklenen bir gelisme degildir?", "opts": ["Ticari uzay istasyonlari", "Isik hizinda seyahat", "Kisiye ozel kanser asilari", "Holografik iletisim"], "answer": 1}
                    ]
                },
                {
                    "cat": "Doga", "icon": "\U0001f33f",
                    "title": "Nesli Tukenen Turler ve Koruma Calismalari",
                    "content": [
                        "Bilim insanlari, Dunya'nin altinci buyuk tukenis olayini yasadigini uyarmaktadır. Tür kayip hizi, dogal arka plan hizinin 100-1000 katına ulasmıstir. IUCN Kirmizi Listesi'nde 42.000'den fazla tur nesli tukenmekte olarak siniflandirilmistir.",
                        "Buyuk memeliler en cok tehdit altinda olan gruplar arasindadir. Sumatra gergedani 80'den az bireyle, Amur leopari 100'den az bireyle hayatta kalma mucadelesi vermektedir. Deniz samuru, beyaz gergedan ve dag gorili de kritik tehlike altindadir.",
                        "Koruma calismalari bazi turlerde basari gostermistir. Dev panda'nin durumu 'tehlike altinda'dan 'savunmasız'a iyilesmistir. Amerikan kel kartali, DDT yasakının ardindan populasyonunu toparlamiştir. Turkiye'deki Anadolu leopari ve kelaynak kusu icin de koruma projeleri yurütülmektedir.",
                        "Bireylerin de katkida bulunması mumkundur. Yerel doga koruma organizasyonlarına destek olmak, surdurulebilir urunler tercih etmek, plastik tuketimini azaltmak ve doga farkindaligini artirmak her bireyin yapabilecegi onemli adimlardir."
                    ],
                    "quiz": [
                        {"q": "IUCN Kirmizi Listesi'nde kac turden fazla tur tehdit altindadir?", "opts": ["10.000", "25.000", "42.000", "100.000"], "answer": 2},
                        {"q": "Hangi turun koruma durumu iyilesmistir?", "opts": ["Sumatra gergedani", "Dev panda", "Amur leopari", "Dag gorili"], "answer": 1}
                    ]
                },
                {
                    "cat": "Tarih", "icon": "\U0001f3db\ufe0f",
                    "title": "Cumhuriyet Tarihi'nden 10 Donum Noktasi",
                    "content": [
                        "Turkiye Cumhuriyeti'nin 100 yillik tarihi, ulkeyi ve toplumu dönüstüren sayisiz onemli olayla doludur. 29 Ekim 1923'te cumhuriyetin ilani, 3 Mart 1924'te hilafetin kaldirilmasi ve 1928 Harf Devrimi ilk yillarin kritik adımlarıdır.",
                        "1934'te soyadi kanunu ve kadinlara secme-secilme hakki taninmistir. 1950'de cok partili sisteme gecis ve demokratik secimlerle iktidar degisimi gerceklesmiştir. Bu geçis, Turkiye'nin demokratik olgunlasmasinda onemli bir kilometre tasidir.",
                        "1960, 1971 ve 1980 askeri mudahaleleri siyasi tarihte derin izler birakmistir. 1982 Anayasasi bugünkü siyasi sistemin temelini olusturmustur. 1999'da Turkiye AB adayligi almis ve reform sureci hizlanmistir.",
                        "21. yuzyilda Turkiye, ekonomik buyumeden altyapi yatirimlarına, savunma sanayisinden uzay programina kadar pek cok alanda onemli gelismeler kaydetmistir. Cumhuriyetin ikinci yuzyilina giren Turkiye, geçmişinin dersleriyle gelecegini sekillendirmektedir."
                    ],
                    "quiz": [
                        {"q": "Turkiye'de cok partili sisteme hangi yil gecilmistir?", "opts": ["1938", "1945", "1950", "1960"], "answer": 2},
                        {"q": "Turkiye AB adayligini hangi yil almistir?", "opts": ["1996", "1999", "2002", "2005"], "answer": 1}
                    ]
                },
                {
                    "cat": "Kultur", "icon": "\U0001f3ad",
                    "title": "Yilin En Iyi Kitaplari - Okuyucu Oylamasi",
                    "content": [
                        "Kitap dunyasi her yil yuzlerce dikkate deger eser uretir. Edebiyat odulleri arasinda Nobel, Booker, Pulitzer ve Turkiye'de Orhan Kemal Roman Armağanı en prestijli olanlardir. Bu oduller okuyuculara kaliteli eserleri kesfetrmenin yolunu acar.",
                        "Roman, siir, deneme ve biyografi farkli okuyucu tercihlerine hitap eden turlerdir. Son yillarda grafik roman ve sesli kitap formatlari da populerlik kazanmistir. Audible ve Storytel gibi platformlar sesli kitap pazarını hızla buyutmuştur.",
                        "Turkiye'de kitap okuma alıskanlığı gelismeye devam etmektedir. Yillik kisi basi kitap okuma sayisi artmakta, ozellikle genc nesil arasinda okuma kulturu guclenmektedir. Kitap fuarlari ve edebiyat festivalleri okuyucu-yazar bulusmalarını kolaylasiirmaktadir.",
                        "Okuma, sadece bilgi edinme degil, ayni zamanda empati gelistirme, elestırel dusunme ve yaraticilik becerilerini guclendiren bir aktivitedir. Arastirmalar düzenli kitap okuyan bireylerin daha yüksek akademik basari gosterdiklerini ve daha guclu sosyal becerilere sahip olduklarını ortaya koymaktadir."
                    ],
                    "quiz": [
                        {"q": "Asagidakilerden hangisi bir edebiyat odulu degildir?", "opts": ["Booker", "Pulitzer", "Grammy", "Nobel"], "answer": 2},
                        {"q": "Duzenli kitap okuma hangi beceriyi gelistirmez?", "opts": ["Empati", "Elestırel dusunme", "Fiziksel dayaniklilik", "Yaraticilik"], "answer": 2}
                    ]
                },
                {
                    "cat": "Spor", "icon": "\u26bd",
                    "title": "Yilin Spor Olaylari Ozeti",
                    "content": [
                        "Spor dunyasi her yil unutulmaz anlar ve basarilarla dolar. Futbol, basketbol, tenis, atletizm ve yuzme gibi branslarda dunya sampiyonalari ve liga yarismaları milyarlarca izleyiciye ulasir.",
                        "Olimpiyat Oyunlari, dort yilda bir dunyanin en buyuk spor bulusmasını sunar. Yuz binlerce sporcu bu sahneye cikabilmek icin yillarini harcar. Bir olimpiyat madalyasi, bir sporcunun kariyerindeki en büyuk basari olarak kabul edilir.",
                        "Turkiye'de futbol en populer spor olmaya devam etmektedir. Super Lig takimlarımız Avrupa kupalarinda yansimasalarını surdurmektedir. Voleybol, ozellikle kadin voleybolunda Turkiye dunya capinda basarılar elde etmektedir. Eczacibasi ve VakifBank dunya sampiyonalarina damga vurmaktadir.",
                        "Bireysel sporlarda Turkiye gures, halter, tekvando, atletizm ve okculuk dallarinda uluslararasi arenada onemli basarilar elde etmektedir. Mete Gazoz'un 2020 Tokyo Olimpiyatlari'nda altin madalya kazanması okçulukta tarihi bir an olmuştur."
                    ],
                    "quiz": [
                        {"q": "Mete Gazoz hangi dalda olimpiyat altin madalyasi kazanmistir?", "opts": ["Gures", "Tekvando", "Okculuk", "Halter"], "answer": 2},
                        {"q": "Turkiye'de en populer spor dalı hangisidir?", "opts": ["Basketbol", "Voleybol", "Futbol", "Tenis"], "answer": 2}
                    ]
                }
            ]
        }
    ]

    # --- CSS ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');

    .dergi-banner {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #7c3aed 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .dergi-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
        animation: dergi-shimmer 4s infinite;
    }
    @keyframes dergi-shimmer {
        0%, 100% { transform: translateX(-30%) translateY(-30%); }
        50% { transform: translateX(30%) translateY(30%); }
    }
    .dergi-banner h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        margin: 0 0 4px 0;
        position: relative;
        z-index: 2;
    }
    .dergi-banner p {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        margin: 0;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }

    .sayi-card {
        background: white;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e5e7eb;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .sayi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .sayi-card.active {
        border-color: #2563eb;
        box-shadow: 0 4px 15px rgba(37,99,235,0.25);
    }
    .sayi-card .emoji {
        font-size: 2rem;
        margin-bottom: 6px;
    }
    .sayi-card .sayi-no {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        color: #374151;
    }
    .sayi-card .sayi-ay {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #6b7280;
    }

    .kapak-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 32px;
        margin: 20px 0;
        border-left: 5px solid;
    }
    .kapak-section h2 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        margin: 0 0 8px 0;
    }
    .kapak-section .tema {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 16px;
    }
    .kapak-section .editorial {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        color: #475569;
        font-style: italic;
        border-left: 3px solid #94a3b8;
        padding-left: 16px;
    }

    .makale-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }
    .makale-header .cat-badge {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        color: white;
    }
    .makale-icerik p {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.8;
        color: #334155;
        margin-bottom: 12px;
        text-align: justify;
    }
    .quiz-section {
        background: #f0f9ff;
        border-radius: 10px;
        padding: 16px;
        margin-top: 12px;
        border: 1px solid #bae6fd;
    }
    .quiz-section h4 {
        font-family: 'Inter', sans-serif;
        color: #0369a1;
        margin: 0 0 8px 0;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Banner ---
    now = datetime.now()
    st.markdown(f"""
    <div class="dergi-banner">
        <h1>\U0001f4d6 SmartCampus e-Dergi</h1>
        <p>Aylik Dijital Egitim Dergisi \u2022 {now.strftime('%B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Issue selector ---
    if "dergi_sayi" not in st.session_state:
        # Auto-select current month
        month_map = {9:0, 10:1, 11:2, 12:3, 1:4, 2:5, 3:6, 4:7, 5:8, 6:9, 7:10, 8:11}
        st.session_state.dergi_sayi = month_map.get(now.month, 0)

    st.markdown("### \U0001f4da Sayi Secin")
    cols = st.columns(6)
    for i, issue in enumerate(ISSUES):
        with cols[i % 6]:
            active = "active" if i == st.session_state.dergi_sayi else ""
            if st.button(
                f"{issue['kapak_emoji']} Sayi {issue['sayi']}\n{issue['month']}",
                key=f"dergi_sayi_{i}",
                use_container_width=True
            ):
                st.session_state.dergi_sayi = i
                st.rerun()

    # --- Selected Issue ---
    issue = ISSUES[st.session_state.dergi_sayi]

    st.markdown(f"""
    <div class="kapak-section" style="border-left-color: {issue['kapak_renk']};">
        <h2>{issue['kapak_emoji']} Sayi {issue['sayi']} \u2014 {issue['month']}</h2>
        <div class="tema">\U0001f3af Tema: {issue['tema']}</div>
        <div class="editorial">\u270d\ufe0f {issue['editorial']}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Articles ---
    CAT_COLORS = {
        "Bilim": "#dc2626",
        "Teknoloji": "#2563eb",
        "Doga": "#16a34a",
        "Tarih": "#d97706",
        "Kultur": "#9333ea",
        "Spor": "#0891b2"
    }

    st.markdown("---")
    st.markdown("### \U0001f4f0 Makaleler")

    for idx, article in enumerate(issue["articles"]):
        cat_color = CAT_COLORS.get(article["cat"], "#6b7280")
        with st.expander(f"{article['icon']} {article['title']}  \u2014  {article['cat']}", expanded=(idx == 0)):
            # Category badge
            st.markdown(f"""
            <div class="makale-header">
                <span class="cat-badge" style="background-color: {cat_color};">{article['icon']} {article['cat']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Content paragraphs
            content_html = ""
            for para in article["content"]:
                content_html += f"<p>{para}</p>"
            st.markdown(f'<div class="makale-icerik">{content_html}</div>', unsafe_allow_html=True)

            # Quiz
            if article.get("quiz"):
                st.markdown(f"""
                <div class="quiz-section">
                    <h4>\U0001f9e0 Bilgini Test Et!</h4>
                </div>
                """, unsafe_allow_html=True)

                for qi, q in enumerate(article["quiz"]):
                    quiz_key = f"dergi_q_{issue['sayi']}_{idx}_{qi}"
                    answer = st.radio(
                        q["q"],
                        q["opts"],
                        key=quiz_key,
                        index=None
                    )
                    if answer is not None:
                        selected_idx = q["opts"].index(answer)
                        if selected_idx == q["answer"]:
                            st.success(f"\u2705 Dogru! '{answer}' dogru cevap.")
                        else:
                            st.error(f"\u274c Yanlis. Dogru cevap: {q['opts'][q['answer']]}")

    # --- Footer ---
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 16px; color: #94a3b8; font-family: 'Inter', sans-serif; font-size: 0.85rem;">
        \U0001f4d6 SmartCampus e-Dergi \u2022 Sayi {issue['sayi']} \u2022 {issue['month']} \u2022 {issue['tema']}<br>
        \u00a9 2025-2026 SmartCampus Egitim Platformu
    </div>
    """, unsafe_allow_html=True)



# ============================================================
# 7. HIKAYE YAZMA ATOLYESI
# ============================================================
def render_hikaye_yazma_atolyesi():
    """Hikaye Yazma Atolyesi - Creative writing workshop"""

    OPENING_SENTENCES = {
        "Macera": [
            "Harita, sandığın dibinde yıllardır bekliyor olmalıydı; kenarları sararmış, üzerindeki mürekkeple çizilmiş yollar neredeyse silinmişti.",
            "Geminin dümenini kırdığımda, ufukta beliren ada hiçbir deniz haritasında yoktu.",
            "Dağın zirvesine ulaştığımda, aşağıda uzanan vadi haritadakinden tamamen farklıydı.",
            "Pusulam çıldırmış gibi dönmeye başladığında, ormanın derinliklerinde kaybolduğumu anladım.",
            "Mağaranın girişindeki yazıt, bin yıldır kimsenin buraya adım atmadığını söylüyordu.",
            "Köprü çöktüğünde, geri dönüş yolu kapanmış ve önümde sadece bilinmeyen uzanıyordu.",
            "Eski haritadaki X işareti, tam da ayaklarımın altındaki toprak parçasını gösteriyordu.",
            "Fırtına dindiğinde, kendimi tanımadığım bir kıyıda, cebimde sadece bir pusulayla buldum.",
            "Şelale'nin arkasına ilk adımı attığımda, karşıma çıkan manzara nefesimi kesti.",
            "Dedelerden kalma anahtarın hangi kapıyı açtığını keşfettiğimde, macera gerçek anlamda başladı."
        ],
        "Bilim Kurgu": [
            "Uzay gemisinin alarmları çalmaya başladığında, kaptan ekranındaki verilerine inanamadı: bilinmeyen bir sinyal.",
            "Zaman makinesi ilk kez çalıştırıldığında, laboratuvarın duvarları titremeye başladı.",
            "Yapay zekanın ilk bağımsız kararı, yaratıcısını şaşkınlığa uğrattı.",
            "Mars kolonisinin kubbesi altında doğan ilk çocuk, dünyanın sadece fotoğraflarda gördüğü bir yerdi.",
            "Işık hızını aşan gemimiz, evrenin kenarına ulaştığında karşılaştığımız şey tüm teorileri çürüttü.",
            "Robot, aynaya baktığında ilk kez 'Ben kimim?' diye sordu.",
            "Teleportasyon kabininden çıktığımda, her şey aynıydı ama bir şeyler farklı hissettiriyordu.",
            "Gezegenler arası elçi gemisi, dünya yörüngesine girdiğinde tüm iletişim kanalları sessizliğe büründü.",
            "Hologram şehirde yaşayan son insan, gerçek bir ağacı ilk kez gördüğünde gözyaşlarını tutamadı.",
            "Kuantum bilgisayarın verdiği cevap tek bir cümleydi: 'Yalnız değilsiniz.'"
        ],
        "Fantastik": [
            "Kitabın sayfaları kendi kendine çevrilmeye başladığında, harfler sayfadan yükselip havada dans etti.",
            "Ejderha yavrusu, ocağın külleri arasından gözlerini açtığında, tüm köy uyuyordu.",
            "Sihirli değneğim ilk kez parladığında, etrafımdaki tüm çiçekler maviye döndü.",
            "Ayna, benim yansımam yerine başka birinin yüzünü gösterdiğinde, nefesim kesildi.",
            "Ormanın derinlerindeki ağaçlar fısıldamaya başladığında, onların dilini anlayabildiğimi fark ettim.",
            "Bulutların üzerindeki şehre ulaşmanın tek yolu, ışıktan örülmüş merdivendi.",
            "Gecenin en karanlık saatinde, gölgem benden ayrılıp kendi yoluna gitti.",
            "Taç, başıma dokunduğu anda tüm hayvanların düşüncelerini duyabildim.",
            "Eski büyücünün not defterini açtığımda, sayfalar arasından gerçek bir kelebek uçtu.",
            "Ay tutulduğu gece, nehirdeki balıklar şarkı söylemeye başladı."
        ],
        "Gizem": [
            "Masanın üzerindeki mektup, on yıl önce kaybolmuş birinden geliyordu.",
            "Kütüphanenin en tozlu rafındaki kitabın arasından düşen fotoğraf, her şeyi değiştirdi.",
            "Saatin her gece tam üçte durması, bir tesadüf olamazdı.",
            "Eski evin bodrum katından gelen sesler, herkesin görmezden geldiği bir sırrın habercisiydi.",
            "Anahtar, kilide mükemmel uyuyordu, ama bu kapının arkasında ne olduğunu kimse bilmiyordu.",
            "Dedektifin masasına bırakılan not kısa ve özdü: 'Müzeye bu gece gel. Yalnız.'",
            "Kasabaya yeni taşınan ailenin evi, tam da otuz yıl önce gizemli şekilde boşaltılan evdi.",
            "Tren istasyonunun kayıp eşya bürosunda unutulan bavul, beklenenin çok ötesinde şeyler saklıyordu.",
            "Fotoğraftaki yüz tanıdıktı, ama fotoğraf 1920'lere aitti.",
            "Her şey, parkta bulduğum o eski cep saatiyle başladı."
        ],
        "Komedi": [
            "Kedim klavyenin üzerine yürüdüğünde, kazara yazdığı e-posta okul müdürüne gitmişti.",
            "Görünmezlik iksirini içtiğimde harika hissettim, ta ki kıyafetlerimin görünmez olmadığını fark edene kadar.",
            "Büyükanneme robot süpürge aldığım gün, evin düzeni bir daha asla eskisi gibi olmadı.",
            "Okul müsameresinde sahneye çıktığımda, kostümümün ters olduğunu fark etmem tam beş dakika sürdü.",
            "Dilek balığı yakaladığımda üç dilek hakkım vardı, ama balık benden daha zeki çıktı.",
            "Uzaylılar dünyaya indiğinde, ilk istedikleri şey pizza oldu.",
            "Dedemin icatları genellikle işe yaramazdı, ama bu sefer gerçekten uçan bir bisiklet yapmıştı.",
            "Konuşan papağanı eve getirdiğimiz günden beri, ailemizin sırları kalmadı.",
            "Yeni taşındığımız evin hayaleti, bizden çok o korkmuştu.",
            "Matematik sınavında hesap makinem isyan edip kendi cevaplarını yazmaya başladığında, öğretmenin yüzü görülmeye değerdi."
        ]
    }

    WRITING_TIPS = [
        "🖊️ **Güçlü bir açılış yapın** — İlk cümle okuyucuyu yakalamalı. Bir soru, şaşırtıcı bir olay veya ilginç bir betimlemeyle başlayın.",
        "👁️ **Gösterin, anlatmayın** — 'Korkmuştu' yerine 'Elleri titriyordu, kalbi göğsünden fırlayacakmış gibi atıyordu' yazın.",
        "🗣️ **Diyalog kullanın** — Karakterleri konuştırarak hikayeye canlılık katın. Her karakter farklı konuşmalı.",
        "🎭 **Çatışma yaratın** — Her iyi hikayenin bir sorunu ve çözümü vardır. Karakterinizin önüne engeller koyun.",
        "🌍 **Duyuları kullanın** — Sadece görüntü değil; ses, koku, tat ve dokunma ile ortamı canlandırın.",
        "⏰ **Gerilim oluşturun** — Okuyucuyu merakta bırakan sahneler ekleyin. Her şeyi hemen açıklamayın.",
        "💬 **İç monolog ekleyin** — Karakterin düşüncelerini paylaşarak okuyucunun empati kurmasını sağlayın.",
        "📐 **Yapı kullanın** — Giriş, gelişme, doruk nokta ve çözüm yapısını takip edin.",
        "✏️ **İlk taslak mükemmel olmak zorunda değil** — Önce yazın, sonra düzenleyin. Mükemmeliyetçilik yaratıcılığı engeller.",
        "📖 **Çok okuyun** — İyi yazarlar iyi okuyuculardır. Farklı türlerde okumak yazım becerinizi geliştirir."
    ]

    st.markdown("""
    <style>
        .story-header { background:linear-gradient(135deg,#0a0a14,#1a1a3e); padding:25px; border-radius:12px;
            border:1px solid #c9a030; text-align:center; margin-bottom:20px; }
        .story-header h2 { color:#c9a030; margin:0; font-size:26px; }
        .story-header p { color:#888; margin:5px 0 0 0; }
        .story-stat { background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; text-align:center; }
        .story-stat h3 { color:#c9a030; font-size:24px; margin:0; }
        .story-stat p { color:#888; font-size:13px; margin:4px 0 0 0; }
        .saved-story { background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; margin-bottom:10px; }
        .saved-story h4 { color:#c9a030; margin:0 0 5px 0; }
        .saved-story .meta { color:#666; font-size:12px; }
        .tip-card { background:#12121e; border-left:3px solid #c9a030; padding:12px 15px; margin-bottom:8px;
            border-radius:0 8px 8px 0; font-size:14px; color:#ccc; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="story-header"><h2>✍️ Hikâye Yazma Atölyesi</h2><p>Hayal gücünü serbest bırak, kendi hikayeni yaz!</p></div>', unsafe_allow_html=True)

    if "stories" not in st.session_state:
        st.session_state.stories = []

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("### 💡 Yazma İpuçları")
        for tip in WRITING_TIPS:
            st.markdown(f'<div class="tip-card">{tip}</div>', unsafe_allow_html=True)

    with col_main:
        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("📚 Tür", list(OPENING_SENTENCES.keys()))
            title = st.text_input("📝 Başlık", placeholder="Hikayene bir isim ver...")
        with col2:
            character = st.text_input("👤 Ana Karakter Adı", placeholder="Karakterinin adı...")
            setting = st.selectbox("🌍 Mekan", ["Orman", "Uzay", "Denizaltı", "Antik Şehir", "Gelecek Dünya"])

        col_starter, _ = st.columns([1, 2])
        with col_starter:
            if st.button("🎲 Hikaye Başlatıcı", use_container_width=True):
                import random
                sentences = OPENING_SENTENCES.get(genre, OPENING_SENTENCES["Macera"])
                opener = random.choice(sentences)
                if character:
                    opener = opener.replace("kendimi", f"{character} kendini").replace("benim", f"{character}'in")
                st.session_state["story_opener"] = opener

        default_text = st.session_state.get("story_opener", "")
        story_text = st.text_area(
            "📖 Hikayeni Yaz",
            value=default_text,
            height=350,
            placeholder="Hikayene burada başla... Yukarıdaki 'Hikaye Başlatıcı' butonuna basarak ilham alabilirsin!"
        )

        word_count = len(story_text.split()) if story_text.strip() else 0
        char_count = len(story_text)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="story-stat"><h3>{word_count}</h3><p>Kelime</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="story-stat"><h3>{char_count}</h3><p>Karakter</p></div>', unsafe_allow_html=True)
        with c3:
            paragraphs = len([p for p in story_text.split("\n") if p.strip()]) if story_text.strip() else 0
            st.markdown(f'<div class="story-stat"><h3>{paragraphs}</h3><p>Paragraf</p></div>', unsafe_allow_html=True)
        with c4:
            read_time = max(1, word_count // 200)
            st.markdown(f'<div class="story-stat"><h3>{read_time}</h3><p>dk Okuma</p></div>', unsafe_allow_html=True)

        if st.button("💾 Hikayeyi Kaydet", type="primary", use_container_width=True):
            if story_text.strip() and title.strip():
                st.session_state.stories.append({
                    "title": title,
                    "genre": genre,
                    "character": character,
                    "setting": setting,
                    "text": story_text,
                    "words": word_count,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M")
                })
                st.success(f"'{title}' hikayesi kaydedildi!")
                st.session_state["story_opener"] = ""
            else:
                st.warning("Lütfen başlık ve hikaye metnini doldurun.")

        if st.session_state.stories:
            st.markdown("---")
            st.markdown("### 📚 Önceki Hikayelerim")
            for i, s in enumerate(reversed(st.session_state.stories)):
                st.markdown(f"""
                <div class="saved-story">
                    <h4>{s['genre']} | {s['title']}</h4>
                    <div class="meta">👤 {s.get('character','—')} | 🌍 {s.get('setting','—')} | 📝 {s['words']} kelime | 📅 {s['date']}</div>
                    <p style="color:#aaa;font-size:13px;margin-top:8px;">{s['text'][:200]}{'...' if len(s['text'])>200 else ''}</p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# 8. EDEBIYAT HARITASI
# ============================================================
def render_edebiyat_haritasi():
    """Edebiyat Haritasi - Interactive literary world map"""

    REGIONS = {
        "Rusya": {
            "pos": "grid-column:5/7;grid-row:1/3", "color": "#e74c3c",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [
                    {"name": "Lev Tolstoy", "work": "Savaş ve Barış", "year": 1869, "bio": "Rus edebiyatının dev ismi. Savaş ve Barış, Napolyon savaşları döneminde beş aristokrat ailenin hikayesini anlatır."},
                    {"name": "Fyodor Dostoyevski", "work": "Suç ve Ceza", "year": 1866, "bio": "Psikolojik romanın öncüsü. İnsan ruhunun en karanlık köşelerini eşsiz bir derinlikle işlemiştir."},
                    {"name": "Anton Çehov", "work": "Vişne Bahçesi", "year": 1904, "bio": "Modern kısa öykünün babası. Tiyatro eserleri dünya sahnesinde hâlâ sahnelenmektedir."}
                ],
                "20.yy": [
                    {"name": "Mihail Bulgakov", "work": "Usta ve Margarita", "year": 1967, "bio": "Sovyet döneminin en özgün yazarı. Eserleri sansüre rağmen ölümsüzleşmiştir."}
                ],
                "Modern": []
            }
        },
        "Fransa": {
            "pos": "grid-column:3/5;grid-row:2/4", "color": "#3498db",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [
                    {"name": "Victor Hugo", "work": "Sefiller", "year": 1862, "bio": "Fransız romantizminin en büyük ismi. Sefiller, toplumsal adaletsizliği işleyen bir başyapıttır."},
                    {"name": "Alexandre Dumas", "work": "Üç Silahşörler", "year": 1844, "bio": "Tarihi macera romanının ustası. Eserleri dünya genelinde milyonlarca okura ulaşmıştır."},
                    {"name": "Gustave Flaubert", "work": "Madame Bovary", "year": 1857, "bio": "Modern romanın öncüsü. Gerçekçi edebiyatın temel taşlarından biridir."}
                ],
                "20.yy": [
                    {"name": "Albert Camus", "work": "Yabancı", "year": 1942, "bio": "Varoluşçu edebiyatın öncüsü, Nobel ödüllü yazar. Absürt felsefenin temsilcisidir."},
                    {"name": "Antoine de Saint-Exupéry", "work": "Küçük Prens", "year": 1943, "bio": "Küçük Prens, dünya edebiyatının en çok okunan kitaplarından biridir."}
                ],
                "Modern": []
            }
        },
        "İngiltere": {
            "pos": "grid-column:2/4;grid-row:1/3", "color": "#2ecc71",
            "authors": {
                "Antik": [],
                "Ortaçağ": [
                    {"name": "Geoffrey Chaucer", "work": "Canterbury Hikayeleri", "year": 1400, "bio": "İngiliz edebiyatının babası. Canterbury Hikayeleri, ortaçağ İngiltere'sinin panoramasıdır."}
                ],
                "19.yy": [
                    {"name": "Charles Dickens", "work": "İki Şehrin Hikayesi", "year": 1859, "bio": "Viktorya dönemi İngiltere'sinin toplumsal sorunlarını ustalıkla işlemiştir."},
                    {"name": "Jane Austen", "work": "Gurur ve Önyargı", "year": 1813, "bio": "İngiliz edebiyatının en sevilen yazarlarından. Toplumsal eleştiriyi zarif bir ironiyle sunar."}
                ],
                "20.yy": [
                    {"name": "George Orwell", "work": "1984", "year": 1949, "bio": "Distopya edebiyatının en etkili eseri. Totaliter rejimlerin eleştirisi olan 1984 hâlâ güncelliğini korur."},
                    {"name": "J.R.R. Tolkien", "work": "Yüzüklerin Efendisi", "year": 1954, "bio": "Modern fantastik edebiyatın kurucusu. Orta Dünya evreni nesiller boyu okuyucuları büyülemiştir."}
                ],
                "Modern": [
                    {"name": "J.K. Rowling", "work": "Harry Potter", "year": 1997, "bio": "Harry Potter serisi, dünya genelinde 500 milyondan fazla kopya satmıştır."}
                ]
            }
        },
        "Amerika": {
            "pos": "grid-column:1/3;grid-row:3/5", "color": "#9b59b6",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [
                    {"name": "Mark Twain", "work": "Tom Sawyer'ın Maceraları", "year": 1876, "bio": "Amerikan edebiyatının en önemli isimlerinden. Mizah ve toplumsal eleştiriyi birleştirmiştir."},
                    {"name": "Edgar Allan Poe", "work": "Kuzgun", "year": 1845, "bio": "Korku ve gerilim türünün öncüsü. Modern dedektif hikayesinin de yaratıcısıdır."}
                ],
                "20.yy": [
                    {"name": "Ernest Hemingway", "work": "Yaşlı Adam ve Deniz", "year": 1952, "bio": "Nobel ödüllü yazar. Yalın ve güçlü üslubuyla 20. yüzyıl edebiyatını şekillendirmiştir."},
                    {"name": "F. Scott Fitzgerald", "work": "Muhteşem Gatsby", "year": 1925, "bio": "Amerikan Rüyası'nın eleştirisi olan Gatsby, Caz Çağı'nın aynasıdır."}
                ],
                "Modern": [
                    {"name": "Toni Morrison", "work": "Sevilen", "year": 1987, "bio": "Nobel ödüllü Afro-Amerikan yazar. Köleliğin mirası üzerine güçlü eserler vermiştir."}
                ]
            }
        },
        "Almanya": {
            "pos": "grid-column:4/6;grid-row:2/4", "color": "#f39c12",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [
                    {"name": "Johann W. von Goethe", "work": "Faust", "year": 1808, "bio": "Alman edebiyatının en büyük ismi. Faust, insanın bilgi ve güç arayışının destanıdır."},
                    {"name": "Friedrich Schiller", "work": "Wilhelm Tell", "year": 1804, "bio": "Alman romantizminin öncüsü. Özgürlük temalı eserleri Avrupa'yı etkilemiştir."},
                    {"name": "Grimm Kardeşler", "work": "Grimm Masalları", "year": 1812, "bio": "Hansel ve Gretel, Kül Kedisi gibi masalları derleyerek dünya kültürüne kazandırmışlardır."}
                ],
                "20.yy": [
                    {"name": "Franz Kafka", "work": "Dönüşüm", "year": 1915, "bio": "Modern edebiyatın en etkili isimlerinden. Absürt ve varoluşsal temaları işlemiştir."},
                    {"name": "Thomas Mann", "work": "Buddenbrook Ailesi", "year": 1901, "bio": "Nobel ödüllü yazar. Burjuva toplumunun çöküşünü anlatan büyük romanlarıyla tanınır."}
                ],
                "Modern": []
            }
        },
        "Türkiye": {
            "pos": "grid-column:5/7;grid-row:3/5", "color": "#c9a030",
            "authors": {
                "Antik": [],
                "Ortaçağ": [
                    {"name": "Mevlana", "work": "Mesnevi", "year": 1273, "bio": "Sufi edebiyatının en büyük ismi. Mesnevi, evrensel sevgi ve hoşgörü mesajlarıyla doludur."},
                    {"name": "Yunus Emre", "work": "Divan", "year": 1321, "bio": "Türk tasavvuf edebiyatının öncüsü. Sade Türkçesiyle halkın dilinden konuşmuştur."}
                ],
                "19.yy": [
                    {"name": "Namık Kemal", "work": "İntibah", "year": 1876, "bio": "Tanzimat edebiyatının öncüsü. Vatan ve özgürlük kavramlarını edebiyata taşımıştır."}
                ],
                "20.yy": [
                    {"name": "Yaşar Kemal", "work": "İnce Memed", "year": 1955, "bio": "Anadolu'nun destansı anlatıcısı. İnce Memed dünya genelinde 40'tan fazla dile çevrilmiştir."},
                    {"name": "Orhan Pamuk", "work": "Benim Adım Kırmızı", "year": 1998, "bio": "Nobel ödüllü yazar. Doğu-Batı sentezini eserlerinde ustalıkla işlemiştir."}
                ],
                "Modern": [
                    {"name": "Elif Şafak", "work": "Aşk", "year": 2009, "bio": "Dünya çapında tanınan çağdaş Türk yazar. Eserleri 50'den fazla dile çevrilmiştir."}
                ]
            }
        },
        "Japonya": {
            "pos": "grid-column:7/9;grid-row:2/4", "color": "#e91e63",
            "authors": {
                "Antik": [],
                "Ortaçağ": [
                    {"name": "Murasaki Shikibu", "work": "Genji'nin Hikayesi", "year": 1010, "bio": "Dünyanın ilk romanı olarak kabul edilen eserin yazarı. Japon saray yaşamını anlatır."}
                ],
                "19.yy": [],
                "20.yy": [
                    {"name": "Yasunari Kawabata", "work": "Kar Ülkesi", "year": 1948, "bio": "Japonya'nın ilk Nobel ödüllü yazarı. Doğa ve insan ilişkisini şiirsel bir dille anlatır."},
                    {"name": "Haruki Murakami", "work": "Kafka Sahilde", "year": 2002, "bio": "Çağdaş Japon edebiyatının dünyaca ünlü ismi. Gerçeküstü anlatım tarzıyla tanınır."}
                ],
                "Modern": []
            }
        },
        "İtalya": {
            "pos": "grid-column:3/5;grid-row:4/6", "color": "#1abc9c",
            "authors": {
                "Antik": [],
                "Ortaçağ": [
                    {"name": "Dante Alighieri", "work": "İlahi Komedya", "year": 1320, "bio": "İtalyan edebiyatının babası. İlahi Komedya, dünya edebiyatının en büyük şiirsel eserlerinden biridir."},
                    {"name": "Giovanni Boccaccio", "work": "Decameron", "year": 1353, "bio": "Rönesans edebiyatının öncüsü. Decameron, yüz hikayeden oluşan bir başyapıttır."}
                ],
                "19.yy": [],
                "20.yy": [
                    {"name": "Italo Calvino", "work": "Görünmez Kentler", "year": 1972, "bio": "Postmodern İtalyan edebiyatının ustası. Hayal gücü ve felsefeyi birleştiren eserleriyle tanınır."}
                ],
                "Modern": [
                    {"name": "Umberto Eco", "work": "Gülün Adı", "year": 1980, "bio": "Göstergebilim profesörü ve yazar. Gülün Adı, ortaçağ manastırında geçen felsefi bir gerilimdir."}
                ]
            }
        },
        "İspanya": {
            "pos": "grid-column:1/3;grid-row:5/7", "color": "#e67e22",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [
                    {"name": "Miguel de Cervantes", "work": "Don Kişot", "year": 1605, "bio": "Modern romanın kurucusu. Don Kişot, dünya edebiyatının en etkili eserlerinden biridir."}
                ],
                "20.yy": [
                    {"name": "Federico García Lorca", "work": "Kanlı Düğün", "year": 1932, "bio": "İspanyol edebiyatının en önemli şair ve oyun yazarlarından biridir."}
                ],
                "Modern": [
                    {"name": "Carlos Ruiz Zafón", "work": "Rüzgarın Gölgesi", "year": 2001, "bio": "Modern İspanyol edebiyatının en çok okunan yazarı. Barcelona'yı eserlerinin merkezi yapmıştır."}
                ]
            }
        },
        "Latin Amerika": {
            "pos": "grid-column:1/3;grid-row:7/9", "color": "#16a085",
            "authors": {
                "Antik": [],
                "Ortaçağ": [],
                "19.yy": [],
                "20.yy": [
                    {"name": "Gabriel García Márquez", "work": "Yüzyıllık Yalnızlık", "year": 1967, "bio": "Büyülü gerçekçiliğin ustası, Nobel ödüllü Kolombiyalı yazar. Latin Amerika edebiyatını dünyaya tanıtmıştır."},
                    {"name": "Jorge Luis Borges", "work": "Ficciones", "year": 1944, "bio": "Arjantinli yazar. Kısa öyküleri, labirent ve sonsuzluk temaları ile edebiyat tarihini etkilemiştir."},
                    {"name": "Pablo Neruda", "work": "Yirmi Aşk Şiiri", "year": 1924, "bio": "Nobel ödüllü Şilili şair. 20. yüzyılın en etkili şairlerinden biri kabul edilir."}
                ],
                "Modern": [
                    {"name": "Isabel Allende", "work": "Ruhlar Evi", "year": 1982, "bio": "Şilili yazar. Büyülü gerçekçilik geleneğini sürdüren en önemli çağdaş isimlerden biridir."}
                ]
            }
        },
        "Antik Yunan": {
            "pos": "grid-column:5/7;grid-row:5/7", "color": "#8e44ad",
            "authors": {
                "Antik": [
                    {"name": "Homeros", "work": "İlyada", "year": -750, "bio": "Batı edebiyatının kurucusu. İlyada ve Odysseia, tüm zamanların en etkili destanlarıdır."},
                    {"name": "Sofokles", "work": "Kral Oidipus", "year": -429, "bio": "Antik Yunan tragedyasının ustası. Kral Oidipus, dramatik ironinin en mükemmel örneğidir."},
                    {"name": "Platon", "work": "Devlet", "year": -375, "bio": "Filozof ve yazar. Diyalog formundaki eserleri hem felsefe hem edebiyat şaheserleridir."}
                ],
                "Ortaçağ": [],
                "19.yy": [],
                "20.yy": [
                    {"name": "Nikos Kazancakis", "work": "Zorba", "year": 1946, "bio": "Modern Yunan edebiyatının en önemli ismi. Zorba, yaşam sevgisinin destanıdır."}
                ],
                "Modern": []
            }
        },
        "Orta Doğu": {
            "pos": "grid-column:7/9;grid-row:4/6", "color": "#d35400",
            "authors": {
                "Antik": [],
                "Ortaçağ": [
                    {"name": "Ömer Hayyam", "work": "Rubailer", "year": 1120, "bio": "İranlı şair, matematikçi ve astronom. Rubaileri dünya edebiyatının en çok okunan şiirlerindendir."},
                    {"name": "Hafız", "work": "Divan", "year": 1370, "bio": "İran şiirinin en büyük ustası. Gazelleri yüzyıllardır okunmakta ve yorumlanmaktadır."},
                    {"name": "Binbir Gece Masalları", "work": "Binbir Gece", "year": 1400, "bio": "Doğu edebiyatının en ünlü derlemesi. Şehrazat'ın hikaye anlatma sanatı evrenseldir."}
                ],
                "19.yy": [],
                "20.yy": [
                    {"name": "Necip Mahfuz", "work": "Kahire Üçlemesi", "year": 1957, "bio": "Arap edebiyatının ilk Nobel ödüllü yazarı. Mısır toplumunu romanlarında ustalıkla yansıtmıştır."}
                ],
                "Modern": []
            }
        }
    }

    regions_json = json.dumps(REGIONS, ensure_ascii=False)
    periods = ["Tümü", "Antik", "Ortaçağ", "19.yy", "20.yy", "Modern"]

    html = f"""
    <div id="lit-map">
        <style>
            #lit-map * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',sans-serif; }}
            #lit-map {{ background:#0a0a14; color:#e0e0e0; padding:20px; min-height:600px; }}
            .lm-header {{ text-align:center; padding:20px 0; border-bottom:2px solid #c9a030; margin-bottom:20px; }}
            .lm-header h1 {{ color:#c9a030; font-size:26px; }}
            .lm-filters {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:20px; }}
            .lm-fbtn {{ padding:6px 16px; border-radius:18px; border:1px solid #333; background:#111; color:#aaa; cursor:pointer; font-size:13px; transition:all .3s; }}
            .lm-fbtn:hover {{ border-color:#c9a030; color:#c9a030; }}
            .lm-fbtn.active {{ background:linear-gradient(135deg,#c9a030,#e8c547); color:#0a0a14; border-color:#c9a030; font-weight:600; }}
            .lm-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }}
            .lm-region {{ background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; cursor:pointer; transition:all .3s; text-align:center; min-height:80px; display:flex; flex-direction:column; justify-content:center; }}
            .lm-region:hover {{ border-color:#c9a030; transform:translateY(-2px); box-shadow:0 4px 15px rgba(201,160,48,.15); }}
            .lm-region.active {{ border-color:#c9a030; background:#1a1a2e; box-shadow:0 0 20px rgba(201,160,48,.2); }}
            .lm-region h3 {{ font-size:15px; margin-bottom:4px; }}
            .lm-region .count {{ font-size:11px; color:#888; }}
            .lm-detail {{ display:none; background:#12121e; border:1px solid #c9a030; border-radius:12px; padding:25px; }}
            .lm-detail.show {{ display:block; }}
            .lm-detail h2 {{ color:#c9a030; font-size:22px; margin-bottom:15px; }}
            .author-card {{ background:#0d0d1a; border:1px solid #222; border-radius:10px; padding:15px; margin-bottom:12px; cursor:pointer; transition:all .3s; }}
            .author-card:hover {{ border-color:#c9a030; }}
            .author-card h4 {{ color:#e0e0e0; font-size:15px; }}
            .author-card .work {{ color:#c9a030; font-size:13px; margin:4px 0; }}
            .author-card .year {{ color:#888; font-size:12px; }}
            .author-card .bio {{ display:none; color:#aaa; font-size:13px; line-height:1.6; margin-top:10px; padding-top:10px; border-top:1px solid #222; }}
            .author-card.expanded .bio {{ display:block; }}
            .no-authors {{ color:#666; font-style:italic; text-align:center; padding:20px; }}
            .back-btn {{ background:none; border:1px solid #c9a030; color:#c9a030; padding:6px 14px; border-radius:8px; cursor:pointer; margin-bottom:15px; font-size:13px; }}
            .back-btn:hover {{ background:#c9a030; color:#0a0a14; }}
        </style>
        <div class="lm-header">
            <h1>🗺️ Edebiyat Haritası</h1>
            <p style="color:#888;margin-top:6px;">Dünya edebiyatını keşfet — bölgelere tıklayarak yazarları gör</p>
        </div>
        <div class="lm-filters" id="lmFilters"></div>
        <div class="lm-grid" id="lmGrid"></div>
        <div class="lm-detail" id="lmDetail"></div>
    </div>
    <script>
    (function(){{
        const R = {regions_json};
        const periods = {json.dumps(periods)};
        let activePeriod = 'Tümü';

        function countAuthors(region, period) {{
            const data = R[region].authors;
            if (period === 'Tümü') return Object.values(data).flat().length;
            return (data[period] || []).length;
        }}

        function buildFilters() {{
            let h = '';
            periods.forEach(p => {{
                h += `<div class="lm-fbtn ${{p===activePeriod?'active':''}}" data-p="${{p}}" onclick="window._lmPeriod(this.dataset.p)">${{p}}</div>`;
            }});
            document.getElementById('lmFilters').innerHTML = h;
        }}

        function buildGrid() {{
            let h = '';
            Object.keys(R).forEach(name => {{
                const cnt = countAuthors(name, activePeriod);
                const c = R[name].color;
                h += `<div class="lm-region" data-name="${{name}}" onclick="window._lmOpen(this.dataset.name)" style="border-left:3px solid ${{c}}">` +
                    `<h3 style="color:${{c}}">${{name}}</h3>` +
                    `<div class="count">${{cnt}} yazar</div></div>`;
            }});
            document.getElementById('lmGrid').innerHTML = h;
            document.getElementById('lmDetail').classList.remove('show');
            document.getElementById('lmGrid').style.display = 'grid';
        }}

        window._lmPeriod = function(p) {{
            activePeriod = p;
            buildFilters();
            buildGrid();
        }};

        window._lmOpen = function(name) {{
            const r = R[name];
            const detail = document.getElementById('lmDetail');
            document.getElementById('lmGrid').style.display = 'none';

            let authors = [];
            if (activePeriod === 'Tümü') {{
                Object.entries(r.authors).forEach(([period, list]) => {{
                    list.forEach(a => authors.push({{...a, period}}));
                }});
            }} else {{
                (r.authors[activePeriod] || []).forEach(a => authors.push({{...a, period: activePeriod}}));
            }}

            let h = '<button class="back-btn" onclick="window._lmBack()">&larr; Haritaya Dön</button>';
            h += '<h2 style="color:'+r.color+'">'+name+'</h2>';
            if (authors.length === 0) {{
                h += '<div class="no-authors">Bu dönemde kayıtlı yazar bulunmamaktadır.</div>';
            }} else {{
                authors.forEach((a, i) => {{
                    const yr = a.year < 0 ? 'M.Ö. ' + Math.abs(a.year) : a.year;
                    h += '<div class="author-card" data-toggle="1">' +
                        '<h4>📖 ' + a.name + '</h4>' +
                        '<div class="work">' + a.work + ' (' + yr + ')</div>' +
                        '<div class="year">Dönem: ' + a.period + '</div>' +
                        '<div class="bio">' + a.bio + '</div></div>';
                }});
            }}
            detail.innerHTML = h;
            detail.classList.add('show');
        }};

        window._lmBack = function() {{
            document.getElementById('lmDetail').classList.remove('show');
            document.getElementById('lmGrid').style.display = 'grid';
        }};

        // Delegated click for author cards
        document.addEventListener('click', function(e) {{
            var card = e.target.closest('[data-toggle]');
            if (card) {{
                if (card.classList.contains('expanded')) {{
                    card.classList.remove('expanded');
                }} else {{
                    card.classList.add('expanded');
                }}
            }}
        }});

        buildFilters();
        buildGrid();
    }})();
    </script>
    """
    components.html(html, height=700, scrolling=True)


# ============================================================
# 9. KELIME HAZINESI TAKIBI
# ============================================================
def render_kelime_hazinesi():
    """Kelime Hazinesi Takibi - Vocabulary tracking with flashcards"""

    WORDS = {
        "Edebiyat": [
            {"word": "Alegori", "def": "Soyut kavramların somut imgeler aracılığıyla anlatılması", "ex": "Hayvan Çiftliği, toplumsal düzeni anlatan bir alegoridir.", "diff": 4},
            {"word": "Metafor", "def": "Bir kavramı başka bir kavramla benzetme yapmadan anlatma", "ex": "Hayat bir yolculuktur.", "diff": 2},
            {"word": "İroni", "def": "Söylenen ile kastedilen arasındaki zıtlık", "ex": "Ne güzel hava, dedi sağanak yağmurda.", "diff": 2},
            {"word": "Destan", "def": "Kahramanlık olaylarını anlatan uzun manzum eser", "ex": "İlyada, Batı edebiyatının en eski destanıdır.", "diff": 1},
            {"word": "Lirik", "def": "Duygu ve coşkuları dile getiren şiir türü", "ex": "Yunus Emre'nin şiirleri lirik şiirin en güzel örnekleridir.", "diff": 3},
            {"word": "Satirik", "def": "Toplumsal aksaklıkları alaycı bir dille eleştiren", "ex": "Molière'in komedileri satirik eserlerdir.", "diff": 3},
            {"word": "Pastoral", "def": "Kır ve çoban yaşamını idealize eden edebiyat türü", "ex": "Vergilius'un Bukolikalar'ı pastoral şiirin klasiğidir.", "diff": 4},
            {"word": "Epilog", "def": "Bir eserin sonunda yer alan kapanış bölümü", "ex": "Romanın epilogu, karakterlerin yıllar sonraki halini anlatıyordu.", "diff": 2},
            {"word": "Protagonisit", "def": "Bir eserin ana karakteri, baş kahraman", "ex": "Don Kişot, romanın protagonistidir.", "diff": 3},
            {"word": "Antagonist", "def": "Ana karaktere karşı çıkan, engelleyen karakter", "ex": "Kötü büyücü, masalın antagonistidir.", "diff": 3},
            {"word": "Monolog", "def": "Tek kişinin uzun konuşması, iç konuşma", "ex": "Hamlet'in 'Olmak ya da olmamak' monologu ünlüdür.", "diff": 2},
            {"word": "Katarsis", "def": "Sanat eserinin izleyicide yarattığı arınma duygusu", "ex": "Tragedya izleyicilerde katarsis yaratır.", "diff": 5},
            {"word": "Aforizma", "def": "Kısa ve özlü düşünce sözü", "ex": "Biliyorum ki hiçbir şey bilmiyorum, bir aforizmadır.", "diff": 4},
            {"word": "Fabl", "def": "Hayvanların konuşturulduğu öğretici kısa hikaye", "ex": "La Fontaine'in fablları dünyaca ünlüdür.", "diff": 1},
            {"word": "Peripeti", "def": "Olayların beklenmedik şekilde tersine dönmesi", "ex": "Kral Oidipus'taki peripeti, tragedyanın doruk noktasıdır.", "diff": 5},
            {"word": "Arkaizm", "def": "Eski ve artık kullanılmayan sözcüklerin kullanımı", "ex": "Divan şiirinde pek çok arkaizm bulunur.", "diff": 4},
            {"word": "Klişe", "def": "Çok kullanılmaktan etkisini yitirmiş ifade", "ex": "Bembeyaz kar örtüsü bir klişe ifadedir.", "diff": 1},
            {"word": "Parodi", "def": "Bir eseri taklit ederek alay eden yapıt", "ex": "Don Kişot, şövalye romanlarının bir parodisidir.", "diff": 3},
            {"word": "Leitmotif", "def": "Bir eserde tekrar eden ana tema veya motif", "ex": "Yalnızlık, Murakami romanlarının leitmotifidir.", "diff": 5},
            {"word": "Anlatıcı", "def": "Bir eserde olayları aktaran ses veya bakış açısı", "ex": "Roman birinci tekil kişi anlatıcıyla yazılmıştır.", "diff": 1}
        ],
        "Bilim": [
            {"word": "Hipotez", "def": "Bilimsel araştırmada sınanmak üzere öne sürülen geçici açıklama", "ex": "Araştırmacı, deneyden önce hipotezini belirledi.", "diff": 2},
            {"word": "Paradigma", "def": "Bir dönemin genel kabul görmüş bilimsel çerçevesi", "ex": "Einstein, fizikte bir paradigma değişimi yarattı.", "diff": 4},
            {"word": "Entropi", "def": "Bir sistemdeki düzensizlik ölçüsü", "ex": "Evrenin entropisi sürekli artmaktadır.", "diff": 5},
            {"word": "Sentez", "def": "Farklı öğeleri birleştirerek yeni bir bütün oluşturma", "ex": "Kimyada sentez, yeni bileşikler üretmek demektir.", "diff": 2},
            {"word": "Empiri", "def": "Deneyime ve gözleme dayalı bilgi", "ex": "Bilim, empirik verilere dayanır.", "diff": 3},
            {"word": "Teorem", "def": "Matematiksel olarak kanıtlanmış önerme", "ex": "Pisagor teoremi en bilinen matematiksel teoremdir.", "diff": 2},
            {"word": "Mutasyon", "def": "DNA dizisindeki kalıtsal değişim", "ex": "Evrim, mutasyonlar aracılığıyla gerçekleşir.", "diff": 3},
            {"word": "Fotosentez", "def": "Bitkilerin ışık enerjisiyle besin üretmesi", "ex": "Fotosentez, dünya üzerindeki yaşamın temelidir.", "diff": 1},
            {"word": "Katalizör", "def": "Kimyasal tepkimeyi hızlandıran ama değişmeden kalan madde", "ex": "Enzimler, biyolojik katalizörlerdir.", "diff": 3},
            {"word": "Osmoz", "def": "Suyun yarı geçirgen zardan geçişi", "ex": "Hücrelerdeki su dengesi osmozla sağlanır.", "diff": 3},
            {"word": "Ekosistem", "def": "Canlılar ve çevreleri arasındaki etkileşim sistemi", "ex": "Bir göl, kendi başına bir ekosistemdir.", "diff": 1},
            {"word": "Genom", "def": "Bir organizmanın tüm genetik bilgisi", "ex": "İnsan genomu 3 milyar baz çiftinden oluşur.", "diff": 3},
            {"word": "İzotop", "def": "Aynı elementin farklı nötron sayılı atomları", "ex": "Karbon-14, arkeolojik yaş tayininde kullanılan bir izotoptur.", "diff": 4},
            {"word": "Plazma", "def": "Maddenin iyonlaşmış dördüncü hali", "ex": "Güneş, plazma halindeki maddeden oluşur.", "diff": 3},
            {"word": "Simbiyoz", "def": "İki farklı türün karşılıklı yarar sağlayarak birlikte yaşaması", "ex": "Mercan ve alg arasındaki ilişki simbiyoza örnektir.", "diff": 4},
            {"word": "Tez", "def": "Kanıtlanmak üzere öne sürülen bilimsel iddia", "ex": "Doktora tezinde yeni bir teori öne sürdü.", "diff": 2},
            {"word": "Atom", "def": "Maddenin kimyasal yollarla bölünemeyen en küçük birimi", "ex": "Her element farklı sayıda proton içeren atomlardan oluşur.", "diff": 1},
            {"word": "Galaksi", "def": "Milyarlarca yıldız, gaz ve tozdan oluşan büyük gök cismi sistemi", "ex": "Samanyolu galaksisinde 200-400 milyar yıldız bulunur.", "diff": 2},
            {"word": "Biyosfer", "def": "Dünya üzerinde canlıların yaşadığı tüm alanlar", "ex": "Biyosfer, atmosfer, hidrosfer ve litosfer arasında yer alır.", "diff": 3},
            {"word": "Nebula", "def": "Yıldızlararası gaz ve toz bulutu", "ex": "Yeni yıldızlar nebulalar içinde doğar.", "diff": 4}
        ],
        "Felsefe": [
            {"word": "Epistemoloji", "def": "Bilginin doğası, kapsamı ve sınırlarını inceleyen felsefe dalı", "ex": "Epistemoloji, 'Bilgi nedir?' sorusunu araştırır.", "diff": 5},
            {"word": "Ontoloji", "def": "Varlığın doğasını ve yapısını inceleyen felsefe dalı", "ex": "Ontoloji, var olan şeylerin temel kategorilerini sorgular.", "diff": 5},
            {"word": "Etik", "def": "Ahlaki değerleri ve doğru-yanlış kavramlarını inceleyen dal", "ex": "Tıp etiği, sağlık alanındaki ahlaki soruları ele alır.", "diff": 2},
            {"word": "Determinizm", "def": "Her olayın önceki nedenler tarafından belirlendiği görüş", "ex": "Determinizme göre özgür irade bir yanılsamadır.", "diff": 4},
            {"word": "Nihilizm", "def": "Hayatın anlamsız olduğunu savunan felsefi görüş", "ex": "Nietzsche, nihilizmi aşmanın yollarını araştırdı.", "diff": 4},
            {"word": "Pragmatizm", "def": "Düşüncelerin değerini pratik sonuçlarıyla ölçen felsefe", "ex": "Pragmatizm, 'İşe yarıyorsa doğrudur' der.", "diff": 3},
            {"word": "Diyalektik", "def": "Tez-antitez-sentez yoluyla gerçeğe ulaşma yöntemi", "ex": "Hegel'in diyalektiği, çelişkilerden ilerleme yaratır.", "diff": 5},
            {"word": "Hedonizm", "def": "Hazzı en yüksek değer olarak gören yaşam felsefesi", "ex": "Epikuros, ölçülü bir hedonizm önermiştir.", "diff": 3},
            {"word": "Stoacılık", "def": "Erdemi ve iç huzuru öne çıkaran antik felsefe okulu", "ex": "Marcus Aurelius, stoacı felsefenin en ünlü temsilcisidir.", "diff": 3},
            {"word": "Ampirizm", "def": "Tüm bilginin deneyimden geldiğini savunan görüş", "ex": "John Locke, ampirizmin öncüsüdür.", "diff": 4},
            {"word": "Rasyonalizm", "def": "Bilginin kaynağının akıl olduğunu savunan görüş", "ex": "Descartes, 'Düşünüyorum, o halde varım' ile rasyonalizmi temellendirdi.", "diff": 3},
            {"word": "Estetik", "def": "Güzellik ve sanat felsefesi", "ex": "Estetik, 'Güzel nedir?' sorusunu inceler.", "diff": 2},
            {"word": "Metafizik", "def": "Varlığın temel doğasını inceleyen felsefe dalı", "ex": "Metafizik, fiziksel dünyanın ötesindeki gerçekliği sorgular.", "diff": 4},
            {"word": "Ütopya", "def": "İdeal ve mükemmel toplum tasarımı", "ex": "Thomas More'un Ütopya'sı, ideal devleti betimler.", "diff": 2},
            {"word": "Distopya", "def": "Korku verici karanlık gelecek toplumu", "ex": "1984, en bilinen distopya romanıdır.", "diff": 2},
            {"word": "Sofizm", "def": "Mantıksal görünen ama geçersiz olan aldatıcı argüman", "ex": "Bu akıl yürütme bir sofizmdir, mantıksal hata içerir.", "diff": 4},
            {"word": "Dogma", "def": "Sorgulanmadan kabul edilen kesin inanç veya ilke", "ex": "Bilim, dogmaları sorgulamakla ilerler.", "diff": 2},
            {"word": "Paradoks", "def": "Çelişkili görünen ama derin anlam taşıyan ifade", "ex": "Zenon'un paradoksları binlerce yıldır tartışılır.", "diff": 3},
            {"word": "Apriori", "def": "Deneyimden bağımsız, akılla bilinen bilgi", "ex": "Matematik gerçekleri apriori bilgidir.", "diff": 5},
            {"word": "Hermeneutik", "def": "Metin ve anlam yorumlama bilimi", "ex": "Hermeneutik, kutsal metinlerin yorumlanmasından doğmuştur.", "diff": 5}
        ],
        "Günlük": [
            {"word": "Empati", "def": "Başkasının duygularını anlama ve paylaşma yeteneği", "ex": "İyi bir dinleyici empati kurabilir.", "diff": 1},
            {"word": "Motivasyon", "def": "İnsanı harekete geçiren iç güdü veya neden", "ex": "Başarı için güçlü bir motivasyon gerekir.", "diff": 1},
            {"word": "Karizmatik", "def": "Etkileyici kişiliğe sahip, çekici", "ex": "Karizmatik liderler insanları kolayca etkiler.", "diff": 2},
            {"word": "Nostalji", "def": "Geçmişe duyulan özlem ve hasret", "ex": "Eski fotoğraflara bakmak nostalji uyandırır.", "diff": 1},
            {"word": "Optimist", "def": "Olayları olumlu yönden gören, iyimser", "ex": "Optimist insanlar zorluklarda bile umut görür.", "diff": 1},
            {"word": "Pesimist", "def": "Olayları olumsuz yönden gören, kötümser", "ex": "Pesimist bakış açısı çözüm üretmeyi zorlaştırır.", "diff": 1},
            {"word": "Spontan", "def": "Doğal, plansız, içten gelen", "ex": "Spontan bir kararla yolculuğa çıktık.", "diff": 2},
            {"word": "Tolerans", "def": "Farklı görüşlere hoşgörü gösterme", "ex": "Toplumsal barış için tolerans şarttır.", "diff": 1},
            {"word": "Vizyon", "def": "Geleceğe yönelik uzun vadeli bakış ve hedef", "ex": "Büyük liderler güçlü bir vizyona sahiptir.", "diff": 2},
            {"word": "Kaos", "def": "Tam bir düzensizlik ve karışıklık durumu", "ex": "Depremden sonra şehirde kaos hakimdi.", "diff": 1},
            {"word": "Egoist", "def": "Yalnızca kendi çıkarını düşünen, bencil", "ex": "Egoist tutumlar takım çalışmasını bozar.", "diff": 1},
            {"word": "Altruist", "def": "Başkalarının iyiliğini kendi çıkarının üstünde tutan", "ex": "Gönüllü çalışanlar altruist davranışa örnektir.", "diff": 3},
            {"word": "Pragmatik", "def": "Pratik ve sonuç odaklı düşünen", "ex": "Pragmatik bir yaklaşımla sorunu hızla çözdük.", "diff": 3},
            {"word": "Ambivalans", "def": "Aynı anda çelişkili duygular hissetme", "ex": "Mezuniyet, hem sevinç hem hüzün — bir ambivalanstı.", "diff": 4},
            {"word": "Retrospektif", "def": "Geriye dönük değerlendirme", "ex": "Retrospektif bakışla hatalarımdan çok şey öğrendim.", "diff": 4},
            {"word": "Sinerji", "def": "Birlikte çalışmanın tek tek çalışmadan fazla sonuç vermesi", "ex": "İki ekibin işbirliği güçlü bir sinerji yarattı.", "diff": 3},
            {"word": "Dilemma", "def": "İki zor seçenek arasında kalma durumu", "ex": "Ahlaki dilemmalar kolay çözülemez.", "diff": 2},
            {"word": "Stereotip", "def": "Bir gruba atfedilen basmakalıp yargı", "ex": "Stereotipler, önyargıların temelini oluşturur.", "diff": 2},
            {"word": "Empowerment", "def": "Güçlendirme, yetkilendirme", "ex": "Kadın empowerment'ı toplumsal kalkınmanın anahtarıdır.", "diff": 3},
            {"word": "Resilience", "def": "Zorluklara karşı dayanıklılık, psikolojik esneklik", "ex": "Resilience, başarılı insanların ortak özelliğidir.", "diff": 4}
        ],
        "Akademik": [
            {"word": "Analiz", "def": "Bir konuyu parçalarına ayırarak inceleme", "ex": "Araştırma verilerinin analizi bir hafta sürdü.", "diff": 1},
            {"word": "Metodoloji", "def": "Araştırmada kullanılan yöntemler bütünü", "ex": "Tez çalışmasında nitel metodoloji tercih edildi.", "diff": 3},
            {"word": "Referans", "def": "Kaynak gösterme, atıfta bulunma", "ex": "Akademik yazılarda referans vermek zorunludur.", "diff": 1},
            {"word": "Korelasyon", "def": "İki değişken arasındaki istatistiksel ilişki", "ex": "Eğitim ve gelir arasında pozitif korelasyon vardır.", "diff": 4},
            {"word": "Literatür", "def": "Belirli bir konudaki yazılı kaynakların tamamı", "ex": "Literatür taraması, araştırmanın ilk adımıdır.", "diff": 2},
            {"word": "Argüman", "def": "Bir iddiayı desteklemek için sunulan gerekçe", "ex": "Güçlü argümanlar kanıtlarla desteklenmelidir.", "diff": 2},
            {"word": "Soyutlama", "def": "Genel özellikleri çıkararak basitleştirme", "ex": "Soyutlama, karmaşık problemleri anlamayı kolaylaştırır.", "diff": 3},
            {"word": "Emprik", "def": "Gözlem ve deneye dayalı", "ex": "Emprik araştırmalar bilimsel ilerlemenin temelidir.", "diff": 3},
            {"word": "Semantik", "def": "Anlam bilimi, dilde anlam ile ilgilenen alan", "ex": "Semantik analiz, metnin derinlemesine anlaşılmasını sağlar.", "diff": 4},
            {"word": "Paradigma", "def": "Bir alanın temel varsayımlar ve yöntemler çerçevesi", "ex": "Dijitalleşme, eğitimde bir paradigma değişimi yaratmıştır.", "diff": 4},
            {"word": "Retrospektif", "def": "Geçmişe yönelik, geriye dönük inceleme", "ex": "Retrospektif çalışmada hasta kayıtları incelendi.", "diff": 4},
            {"word": "Prospektif", "def": "İleriye yönelik, gelecek odaklı araştırma", "ex": "Prospektif kohort çalışması 10 yıl sürecek.", "diff": 5},
            {"word": "Disiplinlerarası", "def": "Birden fazla bilim dalını kapsayan", "ex": "Yapay zeka, disiplinlerarası bir alandır.", "diff": 2},
            {"word": "Objektif", "def": "Kişisel yargılardan bağımsız, nesnel", "ex": "Bilimsel araştırma objektif olmalıdır.", "diff": 1},
            {"word": "Sübjektif", "def": "Kişisel görüş ve duygulara dayalı, öznel", "ex": "Sanat eleştirisi büyük ölçüde sübjektiftir.", "diff": 1},
            {"word": "Kantitatif", "def": "Sayısal verilerle çalışan nicel araştırma", "ex": "Anket, kantitatif araştırma yöntemidir.", "diff": 3},
            {"word": "Kalitatif", "def": "Derinlemesine anlama odaklı nitel araştırma", "ex": "Mülakat, kalitatif araştırma tekniğidir.", "diff": 3},
            {"word": "Abstrakt", "def": "Soyut, somut olmayan; araştırma özeti", "ex": "Makalenin abstraktı araştırmanın özetini sunar.", "diff": 2},
            {"word": "İnterdisipliner", "def": "Farklı bilim dallarını bir araya getiren", "ex": "Biyoinformatik, interdisipliner bir alandır.", "diff": 4},
            {"word": "Validasyon", "def": "Geçerlilik kontrolü, doğrulama", "ex": "Ölçeğin validasyonu uzman görüşleriyle yapıldı.", "diff": 4}
        ]
    }

    words_json = json.dumps(WORDS, ensure_ascii=False)
    cats = list(WORDS.keys())

    html = f"""
    <div id="vocab-app">
        <style>
            #vocab-app * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI',sans-serif; }}
            #vocab-app {{ background:#0a0a14; color:#e0e0e0; padding:20px; min-height:700px; }}
            .va-header {{ text-align:center; padding:20px 0; border-bottom:2px solid #c9a030; margin-bottom:20px; }}
            .va-header h1 {{ color:#c9a030; font-size:26px; }}
            .va-tabs {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:20px; }}
            .va-tab {{ padding:8px 18px; border-radius:20px; border:1px solid #333; background:#111; color:#aaa; cursor:pointer; font-size:13px; transition:all .3s; }}
            .va-tab:hover {{ border-color:#c9a030; color:#c9a030; }}
            .va-tab.active {{ background:linear-gradient(135deg,#c9a030,#e8c547); color:#0a0a14; border-color:#c9a030; font-weight:600; }}
            .va-cats {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; margin-bottom:20px; }}
            .va-cat {{ padding:6px 14px; border-radius:15px; border:1px solid #333; background:#12121e; color:#aaa; cursor:pointer; font-size:12px; }}
            .va-cat:hover {{ border-color:#c9a030; }}
            .va-cat.active {{ border-color:#c9a030; color:#c9a030; }}
            .va-section {{ display:none; }}
            .va-section.show {{ display:block; }}
            /* Level Test */
            .test-word {{ background:#12121e; border:1px solid #222; border-radius:10px; padding:12px 18px; margin:6px 0; display:flex; justify-content:space-between; align-items:center; }}
            .test-word span {{ font-size:16px; font-weight:500; }}
            .test-btns button {{ padding:5px 14px; border-radius:6px; border:1px solid #333; margin-left:6px; cursor:pointer; font-size:12px; background:#111; color:#aaa; }}
            .test-btns button:hover {{ border-color:#c9a030; color:#c9a030; }}
            .test-btns button.yes {{ background:#1a3a1a; border-color:#27ae60; color:#2ecc71; }}
            .test-btns button.no {{ background:#3a1a1a; border-color:#e74c3c; color:#e74c3c; }}
            .level-result {{ text-align:center; padding:30px; background:#12121e; border:1px solid #c9a030; border-radius:12px; margin:20px 0; }}
            .level-result h2 {{ color:#c9a030; font-size:40px; }}
            /* Flashcard */
            .flashcard {{ background:#12121e; border:1px solid #c9a030; border-radius:14px; width:100%; max-width:500px; margin:0 auto 20px; min-height:250px; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:30px; cursor:pointer; transition:all .3s; text-align:center; }}
            .flashcard:hover {{ box-shadow:0 0 25px rgba(201,160,48,.2); }}
            .flashcard h3 {{ color:#c9a030; font-size:28px; margin-bottom:10px; }}
            .flashcard .fc-def {{ color:#ccc; font-size:16px; line-height:1.6; display:none; }}
            .flashcard .fc-ex {{ color:#888; font-size:14px; font-style:italic; margin-top:10px; display:none; }}
            .flashcard.flipped .fc-def, .flashcard.flipped .fc-ex {{ display:block; }}
            .flashcard .fc-hint {{ color:#666; font-size:12px; margin-top:15px; }}
            .flashcard.flipped .fc-hint {{ display:none; }}
            .fc-nav {{ display:flex; gap:10px; justify-content:center; margin:15px 0; }}
            .fc-nav button {{ padding:8px 20px; border-radius:8px; border:1px solid #333; background:#111; color:#aaa; cursor:pointer; font-size:13px; }}
            .fc-nav button:hover {{ border-color:#c9a030; color:#c9a030; }}
            .fc-progress {{ text-align:center; color:#888; font-size:13px; margin-bottom:10px; }}
            /* Word List */
            .word-item {{ background:#12121e; border:1px solid #222; border-radius:10px; padding:14px 18px; margin:8px 0; cursor:pointer; transition:all .3s; }}
            .word-item:hover {{ border-color:#c9a030; }}
            .word-item h4 {{ color:#c9a030; font-size:16px; display:flex; justify-content:space-between; align-items:center; }}
            .word-item .wi-diff {{ font-size:11px; color:#888; }}
            .word-item .wi-body {{ display:none; margin-top:10px; padding-top:10px; border-top:1px solid #222; }}
            .word-item.open .wi-body {{ display:block; }}
            .wi-def {{ color:#ccc; font-size:14px; }}
            .wi-ex {{ color:#888; font-size:13px; font-style:italic; margin-top:6px; }}
            .diff-stars {{ color:#c9a030; }}
            .stats-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; margin:20px 0; }}
            .stat-card {{ background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; text-align:center; }}
            .stat-card h3 {{ color:#c9a030; font-size:24px; }}
            .stat-card p {{ color:#888; font-size:12px; margin-top:4px; }}
            .sr-schedule {{ background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; margin:10px 0; }}
            .sr-bar {{ height:8px; background:#222; border-radius:4px; margin-top:6px; overflow:hidden; }}
            .sr-fill {{ height:100%; background:linear-gradient(90deg,#c9a030,#e8c547); border-radius:4px; }}
        </style>
        <div class="va-header">
            <h1>📚 Kelime Hazinesi Takibi</h1>
            <p style="color:#888;margin-top:6px;">Seviye testi, flashcard ve aralıklı tekrar</p>
        </div>
        <div class="va-tabs">
            <div class="va-tab active" onclick="window._vaTab('test')">📊 Seviye Testi</div>
            <div class="va-tab" onclick="window._vaTab('flash')">🃏 Flashcard</div>
            <div class="va-tab" onclick="window._vaTab('list')">📖 Kelime Listesi</div>
            <div class="va-tab" onclick="window._vaTab('stats')">📈 İstatistikler</div>
        </div>
        <div class="va-cats" id="vaCats"></div>
        <div id="vaTest" class="va-section show"></div>
        <div id="vaFlash" class="va-section"></div>
        <div id="vaList" class="va-section"></div>
        <div id="vaStats" class="va-section"></div>
    </div>
    <script>
    (function(){{
        const W = {words_json};
        const cats = {json.dumps(cats)};
        let activeCat = cats[0];
        let activeTab = 'test';
        let testAnswers = {{}};
        let testDone = false;
        let fcIndex = 0;
        let learned = JSON.parse(localStorage.getItem('va_learned') || '{{}}');

        function renderCats() {{
            let h = '';
            cats.forEach(c => {{
                h += `<div class="va-cat ${{c===activeCat?'active':''}}" data-cat="${{c}}" onclick="window._vaCat(this.dataset.cat)">${{c}} (${{W[c].length}})</div>`;
            }});
            document.getElementById('vaCats').innerHTML = h;
        }}

        window._vaTab = function(tab) {{
            activeTab = tab;
            document.querySelectorAll('.va-tab').forEach((t,i) => t.classList.toggle('active', ['test','flash','list','stats'][i]===tab));
            document.querySelectorAll('.va-section').forEach(s => s.classList.remove('show'));
            var tabMap = {{}}; tabMap.test='vaTest'; tabMap.flash='vaFlash'; tabMap.list='vaList'; tabMap.stats='vaStats';
            document.getElementById(tabMap[tab]).classList.add('show');
            render();
        }};

        window._vaCat = function(c) {{ activeCat = c; fcIndex = 0; testDone = false; testAnswers = {{}}; renderCats(); render(); }};

        function render() {{
            if (activeTab==='test') renderTest();
            else if (activeTab==='flash') renderFlash();
            else if (activeTab==='list') renderList();
            else renderStats();
        }}

        function renderTest() {{
            const words = W[activeCat];
            const testWords = words.filter((_,i) => i < 10);
            if (testDone) {{
                const known = Object.values(testAnswers).filter(v=>v).length;
                const total = testWords.length;
                const pct = known / total;
                let level = 'A1';
                if (pct >= 0.9) level = 'C2';
                else if (pct >= 0.8) level = 'C1';
                else if (pct >= 0.6) level = 'B2';
                else if (pct >= 0.4) level = 'B1';
                else if (pct >= 0.2) level = 'A2';
                const el = document.getElementById('vaTest');
                el.innerHTML = '<div class="level-result"><p style="color:#888;margin-bottom:10px;">Tahmini Kelime Seviyeniz</p>' +
                    '<h2>' + level + '</h2><p style="color:#aaa;margin-top:10px;">' + known + '/' + total + ' kelimeyi biliyorsunuz</p>' +
                    '<button style="margin-top:15px;padding:8px 20px;border-radius:8px;border:1px solid #c9a030;background:none;color:#c9a030;cursor:pointer" ' +
                    'onclick="window._vaRetest()">Tekrar Test</button></div>';
                return;
            }}
            let h = '<p style="color:#aaa;text-align:center;margin-bottom:15px;">Aşağıdaki kelimeleri biliyor musunuz?</p>';
            testWords.forEach((w, i) => {{
                const ans = testAnswers[i];
                h += '<div class="test-word"><span>' + w.word + '</span><div class="test-btns">' +
                    '<button class="'+(ans===true?'yes':'')+'" onclick="window._vaTestAns('+i+',true)">Biliyorum</button>' +
                    '<button class="'+(ans===false?'no':'')+'" onclick="window._vaTestAns('+i+',false)">Bilmiyorum</button></div></div>';
            }});
            h += '<div style="text-align:center;margin-top:15px;"><button style="padding:10px 30px;border-radius:8px;border:none;background:linear-gradient(135deg,#c9a030,#e8c547);color:#0a0a14;font-weight:600;cursor:pointer;font-size:15px" onclick="window._vaFinishTest()">Sonucu Gör</button></div>';
            document.getElementById('vaTest').innerHTML = h;
        }}

        window._vaTestAns = function(i, val) {{ testAnswers[i] = val; renderTest(); }};
        window._vaFinishTest = function() {{ testDone = true; renderTest(); }};
        window._vaRetest = function() {{ testDone = false; testAnswers = {{}}; renderTest(); }};

        function renderFlash() {{
            const words = W[activeCat];
            const w = words[fcIndex];
            const stars = '★'.repeat(w.diff) + '☆'.repeat(5 - w.diff);
            let h = '<div class="fc-progress">' + (fcIndex+1) + ' / ' + words.length + '</div>';
            h += '<div class="flashcard" data-toggle="1">';
            h += '<h3>' + w.word + '</h3>';
            h += '<div class="diff-stars">' + stars + '</div>';
            h += '<div class="fc-def">' + w.def + '</div>';
            h += '<div class="fc-ex">"' + w.ex + '"</div>';
            h += '<div class="fc-hint">Kartı çevirmek için tıklayın</div>';
            h += '</div>';
            h += '<div class="fc-nav">';
            h += '<button onclick="window._vaFcPrev()">◀ Önceki</button>';
            const lk = activeCat + '_' + fcIndex;
            const isLearned = learned[lk];
            h += '<button onclick="window._vaFcLearn('+fcIndex+')" style="'+(isLearned?'background:#1a3a1a;border-color:#27ae60;color:#2ecc71':'')+'">✓ '+(isLearned?'Öğrenildi':'Öğrendim')+'</button>';
            h += '<button onclick="window._vaFcNext()">Sonraki ▶</button>';
            h += '</div>';
            document.getElementById('vaFlash').innerHTML = h;
        }}

        window._vaFcPrev = function() {{ const words = W[activeCat]; fcIndex = (fcIndex - 1 + words.length) % words.length; renderFlash(); }};
        window._vaFcNext = function() {{ const words = W[activeCat]; fcIndex = (fcIndex + 1) % words.length; renderFlash(); }};
        window._vaFcLearn = function(i) {{
            const lk = activeCat + '_' + i;
            learned[lk] = !learned[lk];
            localStorage.setItem('va_learned', JSON.stringify(learned));
            renderFlash();
        }};

        function renderList() {{
            const words = W[activeCat];
            let h = '';
            words.forEach((w, i) => {{
                const stars = '★'.repeat(w.diff) + '☆'.repeat(5 - w.diff);
                const lk = activeCat + '_' + i;
                const badge = learned[lk] ? ' <span style="color:#2ecc71;font-size:11px;">✓ Öğrenildi</span>' : '';
                h += '<div class="word-item" data-toggle="1">';
                h += '<h4>' + w.word + badge + ' <span class="wi-diff"><span class="diff-stars">' + stars + '</span></span></h4>';
                h += '<div class="wi-body"><div class="wi-def">' + w.def + '</div><div class="wi-ex">"' + w.ex + '"</div></div></div>';
            }});
            document.getElementById('vaList').innerHTML = h;
        }}

        function renderStats() {{
            let totalWords = 0, totalLearned = 0;
            const catStats = {{}};
            cats.forEach(c => {{
                const cnt = W[c].length;
                let ln = 0;
                for (let i = 0; i < cnt; i++) {{ if (learned[c + '_' + i]) ln++; }}
                totalWords += cnt;
                totalLearned += ln;
                catStats[c] = {{ total: cnt, learned: ln }};
            }});
            let h = '<div class="stats-grid">';
            h += '<div class="stat-card"><h3>' + totalWords + '</h3><p>Toplam Kelime</p></div>';
            h += '<div class="stat-card"><h3>' + totalLearned + '</h3><p>Öğrenilen</p></div>';
            h += '<div class="stat-card"><h3>' + (totalWords - totalLearned) + '</h3><p>Kalan</p></div>';
            h += '<div class="stat-card"><h3>' + (totalWords > 0 ? Math.round(totalLearned/totalWords*100) : 0) + '%</h3><p>İlerleme</p></div>';
            h += '</div>';
            h += '<h3 style="color:#c9a030;margin:20px 0 10px;">📅 Aralıklı Tekrar Programı</h3>';
            cats.forEach(c => {{
                const s = catStats[c];
                const pct = s.total > 0 ? Math.round(s.learned / s.total * 100) : 0;
                h += '<div class="sr-schedule"><div style="display:flex;justify-content:space-between"><span>' + c + '</span><span style="color:#c9a030">' + s.learned + '/' + s.total + '</span></div>';
                h += '<div class="sr-bar"><div class="sr-fill" style="width:'+pct+'%"></div></div></div>';
            }});
            document.getElementById('vaStats').innerHTML = h;
        }}

        // Delegated toggle for flashcard and word items
        document.addEventListener('click', function(e) {{
            var el = e.target.closest('[data-toggle]');
            if (el) {{
                if (el.classList.contains('flipped')) el.classList.remove('flipped');
                else if (el.classList.contains('open')) el.classList.remove('open');
                else if (el.classList.contains('flashcard')) el.classList.add('flipped');
                else if (el.classList.contains('word-item')) el.classList.add('open');
            }}
        }});

        renderCats();
        render();
    }})();
    </script>
    """
    components.html(html, height=750, scrolling=True)


# ============================================================
# 10. CANLI OKUMA SAATI
# ============================================================
def render_canli_okuma_saati():
    """Canli Okuma Saati - Reading session planner and tracker"""

    BOOKS = [
        "Küçük Prens — Antoine de Saint-Exupéry",
        "Sefiller — Victor Hugo",
        "Suç ve Ceza — Fyodor Dostoyevski",
        "1984 — George Orwell",
        "Yüzüklerin Efendisi — J.R.R. Tolkien",
        "Harry Potter ve Felsefe Taşı — J.K. Rowling",
        "İnce Memed — Yaşar Kemal",
        "Benim Adım Kırmızı — Orhan Pamuk",
        "Don Kişot — Miguel de Cervantes",
        "Muhteşem Gatsby — F. Scott Fitzgerald",
        "Simyacı — Paulo Coelho",
        "Hayvan Çiftliği — George Orwell",
        "Yabancı — Albert Camus",
        "Dönüşüm — Franz Kafka",
        "Uçurtma Avcısı — Khaled Hosseini",
        "Tutunamayanlar — Oğuz Atay",
        "Saatleri Ayarlama Enstitüsü — Ahmet Hamdi Tanpınar",
        "Kürk Mantolu Madonna — Sabahattin Ali",
        "Çalıkuşu — Reşat Nuri Güntekin",
        "Aşk — Elif Şafak"
    ]

    st.markdown("""
    <style>
        .ok-header { background:linear-gradient(135deg,#0a0a14,#1a1a3e); padding:25px; border-radius:12px;
            border:1px solid #c9a030; text-align:center; margin-bottom:20px; }
        .ok-header h2 { color:#c9a030; margin:0; font-size:26px; }
        .ok-header p { color:#888; margin:5px 0 0 0; }
        .ok-stat { background:#12121e; border:1px solid #222; border-radius:10px; padding:15px; text-align:center; }
        .ok-stat h3 { color:#c9a030; font-size:24px; margin:0; }
        .ok-stat p { color:#888; font-size:12px; margin:4px 0 0 0; }
        .ok-session-card { background:#12121e; border:1px solid #222; border-radius:10px; padding:14px 18px; margin-bottom:8px; }
        .ok-session-card h4 { color:#c9a030; margin:0 0 4px 0; font-size:14px; }
        .ok-session-card .meta { color:#666; font-size:12px; }
        .ok-question { background:#12121e; border-left:3px solid #c9a030; border-radius:0 8px 8px 0;
            padding:12px 15px; margin-bottom:8px; }
        .ok-question label { color:#c9a030; font-weight:600; font-size:14px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ok-header"><h2>📖 Canlı Okuma Saati</h2><p>Planlı okuma seansları ile okuma alışkanlığını geliştir</p></div>', unsafe_allow_html=True)

    if "reading_sessions" not in st.session_state:
        st.session_state.reading_sessions = []

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 📚 Okuma Seansı Oluştur")

        book = st.selectbox("📖 Kitap Seç", BOOKS)
        c1, c2, c3 = st.columns(3)
        with c1:
            start_page = st.number_input("Başlangıç Sayfası", min_value=1, value=1, step=1)
        with c2:
            end_page = st.number_input("Bitiş Sayfası", min_value=1, value=20, step=1)
        with c3:
            reading_time = st.slider("Okuma Süresi (dk)", 15, 120, 30, 5)

        st.markdown("### ⏱️ Zamanlayıcı")

        timer_html = f"""
        <div id="timer-app">
            <style>
                #timer-app {{ font-family:'Segoe UI',sans-serif; text-align:center; padding:20px; background:#12121e; border-radius:12px; border:1px solid #222; }}
                .timer-display {{ font-size:56px; font-weight:300; color:#c9a030; letter-spacing:4px; margin:15px 0; font-variant-numeric:tabular-nums; }}
                .timer-label {{ color:#888; font-size:13px; margin-bottom:10px; }}
                .timer-btns {{ display:flex; gap:10px; justify-content:center; margin-top:15px; }}
                .timer-btns button {{ padding:10px 24px; border-radius:8px; border:none; cursor:pointer; font-size:14px; font-weight:600; transition:all .3s; }}
                .btn-start {{ background:linear-gradient(135deg,#27ae60,#2ecc71); color:#fff; }}
                .btn-pause {{ background:linear-gradient(135deg,#f39c12,#e67e22); color:#fff; }}
                .btn-reset {{ background:none; border:1px solid #666 !important; color:#888; }}
                .btn-reset:hover {{ border-color:#c9a030 !important; color:#c9a030; }}
                .timer-bar {{ height:6px; background:#222; border-radius:3px; margin-top:15px; overflow:hidden; }}
                .timer-fill {{ height:100%; background:linear-gradient(90deg,#c9a030,#e8c547); border-radius:3px; transition:width 1s linear; }}
            </style>
            <div class="timer-label">Kalan Süre</div>
            <div class="timer-display" id="timerDisp">
                {reading_time:02d}:00
            </div>
            <div class="timer-bar"><div class="timer-fill" id="timerFill" style="width:100%"></div></div>
            <div class="timer-btns">
                <button class="btn-start" id="btnStart" onclick="window._tStart()">▶ Başlat</button>
                <button class="btn-pause" id="btnPause" onclick="window._tPause()" style="display:none">⏸ Duraklat</button>
                <button class="btn-reset" onclick="window._tReset()">↺ Sıfırla</button>
            </div>
        </div>
        <script>
        (function(){{
            let total = {reading_time} * 60;
            let remaining = total;
            let interval = null;
            let running = false;

            function fmt(s) {{
                const m = Math.floor(s/60);
                const sec = s % 60;
                return String(m).padStart(2,'0') + ':' + String(sec).padStart(2,'0');
            }}

            function updateUI() {{
                document.getElementById('timerDisp').textContent = fmt(remaining);
                const pct = (remaining / total) * 100;
                document.getElementById('timerFill').style.width = pct + '%';
            }}

            window._tStart = function() {{
                if (running) return;
                running = true;
                document.getElementById('btnStart').style.display = 'none';
                document.getElementById('btnPause').style.display = 'inline-block';
                interval = setInterval(function() {{
                    if (remaining > 0) {{
                        remaining--;
                        updateUI();
                    }} else {{
                        clearInterval(interval);
                        running = false;
                        document.getElementById('timerDisp').textContent = '00:00';
                        document.getElementById('timerDisp').style.color = '#2ecc71';
                        document.getElementById('btnStart').style.display = 'inline-block';
                        document.getElementById('btnPause').style.display = 'none';
                    }}
                }}, 1000);
            }};

            window._tPause = function() {{
                clearInterval(interval);
                running = false;
                document.getElementById('btnStart').style.display = 'inline-block';
                document.getElementById('btnPause').style.display = 'none';
            }};

            window._tReset = function() {{
                clearInterval(interval);
                running = false;
                remaining = total;
                updateUI();
                document.getElementById('timerDisp').style.color = '#c9a030';
                document.getElementById('btnStart').style.display = 'inline-block';
                document.getElementById('btnPause').style.display = 'none';
            }};
        }})();
        </script>
        """
        components.html(timer_html, height=220)

        st.markdown("### 📝 Okuma Sırasında — Notlar")
        notes = st.text_area("Notlarınızı buraya yazın...", height=120, placeholder="Bu bölümde dikkatinizi çeken noktaları, karakterleri veya alıntıları not edin...")

        st.markdown("### ❓ Anlama Soruları")
        st.markdown('<div class="ok-question"><label>1. Bu bölümde en önemli olay neydi?</label></div>', unsafe_allow_html=True)
        q1 = st.text_input("Cevap 1", label_visibility="collapsed", placeholder="Bu bölümde en önemli olay neydi?")
        st.markdown('<div class="ok-question"><label>2. Hangi karakter sizi etkiledi?</label></div>', unsafe_allow_html=True)
        q2 = st.text_input("Cevap 2", label_visibility="collapsed", placeholder="Hangi karakter sizi etkiledi ve neden?")
        st.markdown('<div class="ok-question"><label>3. Bu bölümü tek cümleyle özetleyin.</label></div>', unsafe_allow_html=True)
        q3 = st.text_input("Cevap 3", label_visibility="collapsed", placeholder="Bu bölümü tek cümleyle özetleyin.")

        if st.button("💾 Okuma Seansını Kaydet", type="primary", use_container_width=True):
            if end_page > start_page:
                session = {
                    "book": book,
                    "start_page": start_page,
                    "end_page": end_page,
                    "pages_read": end_page - start_page,
                    "duration": reading_time,
                    "notes": notes,
                    "q1": q1, "q2": q2, "q3": q3,
                    "date": datetime.now().strftime("%d.%m.%Y %H:%M")
                }
                st.session_state.reading_sessions.append(session)
                st.success(f"Okuma seansı kaydedildi! {end_page - start_page} sayfa okundu.")
            else:
                st.warning("Bitiş sayfası başlangıç sayfasından büyük olmalı.")

    with col_right:
        st.markdown("### 📊 Okuma İstatistikleri")
        sessions = st.session_state.reading_sessions
        total_sessions = len(sessions)
        total_pages = sum(s["pages_read"] for s in sessions)
        total_minutes = sum(s["duration"] for s in sessions)
        avg_speed = round(total_pages / max(total_minutes, 1) * 60, 1) if sessions else 0

        st.markdown(f'<div class="ok-stat"><h3>{total_sessions}</h3><p>Toplam Seans</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ok-stat"><h3>{total_pages}</h3><p>Toplam Sayfa</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ok-stat"><h3>{total_minutes}</h3><p>Toplam Dakika</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ok-stat"><h3>{avg_speed}</h3><p>Sayfa/Saat</p></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📜 Seans Geçmişi")

        if sessions:
            for s in reversed(sessions):
                st.markdown(f"""
                <div class="ok-session-card">
                    <h4>📖 {s['book']}</h4>
                    <div class="meta">📅 {s['date']} | 📄 s.{s['start_page']}-{s['end_page']} ({s['pages_read']} sayfa) | ⏱️ {s['duration']} dk</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Henüz okuma seansı yok. İlk seansını oluştur!")
