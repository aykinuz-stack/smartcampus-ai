"""Bilgi Yarışması — Premium HTML5 Quiz Oyunu, 3 seviye (İlkokul/Ortaokul/Lise), geniş soru bankası."""

import json as _json
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("default")
except Exception:
    pass

# ══════════════════════════════════════════════════════════════════════════════
# SEVİYE BAZLI SORU BANKALARI
# ══════════════════════════════════════════════════════════════════════════════

def _get_by_questions(level: str) -> str:
    """Seviyeye göre JavaScript soru bankası döndürür."""
    if level == "ilkokul":
        return _BY_QUESTIONS_ILKOKUL
    elif level == "ortaokul":
        return _BY_QUESTIONS_ORTAOKUL
    else:
        return _BY_QUESTIONS_LISE

_BY_QUESTIONS_ILKOKUL = r"""
{k:"Tarih",s:"Türkiye Cumhuriyeti ne zaman kuruldu?",o:["1920","1922","1923","1925"],d:2,a:"29 Ekim 1923'te ilan edildi."},
{k:"Tarih",s:"Cumhuriyetimizin kurucusu kimdir?",o:["İsmet İnönü","Atatürk","Fevzi Çakmak","Kazım Karabekir"],d:1,a:"Mustafa Kemal Atatürk kurucumuzdur."},
{k:"Tarih",s:"23 Nisan hangi bayramdır?",o:["Zafer","Cumhuriyet","Egemenlik ve Çocuk","Gençlik"],d:2,a:"Ulusal Egemenlik ve Çocuk Bayramı."},
{k:"Tarih",s:"29 Ekim hangi bayramdır?",o:["Zafer","Cumhuriyet","Çocuk","Gençlik"],d:1,a:"Cumhuriyet Bayramı'dır."},
{k:"Tarih",s:"30 Ağustos hangi bayramdır?",o:["Zafer","Cumhuriyet","Çocuk","Gençlik"],d:0,a:"Zafer Bayramı, 1922 Büyük Taarruz."},
{k:"Tarih",s:"19 Mayıs hangi bayramdır?",o:["Zafer","Cumhuriyet","Çocuk","Gençlik ve Spor"],d:3,a:"Atatürk 1919'da Samsun'a çıktı."},
{k:"Tarih",s:"İstanbul'un fethi hangi yılda oldu?",o:["1071","1299","1453","1923"],d:2,a:"1453'te Fatih Sultan Mehmet fethetti."},
{k:"Tarih",s:"Osmanlı Devleti'ni kim kurdu?",o:["Fatih","Osman Bey","Kanuni","Yavuz"],d:1,a:"Osman Bey 1299'da kurdu."},
{k:"Tarih",s:"Atatürk nerede doğdu?",o:["Ankara","İstanbul","Selanik","İzmir"],d:2,a:"1881'de Selanik'te doğdu."},
{k:"Tarih",s:"TBMM ilk ne zaman açıldı?",o:["23 Nisan 1920","29 Ekim 1923","19 Mayıs 1919","30 Ağustos 1922"],d:0,a:"23 Nisan 1920'de Ankara'da açıldı."},
{k:"Tarih",s:"Piramitler hangi ülkededir?",o:["Irak","İran","Mısır","Suriye"],d:2,a:"Piramitler Mısır'dadır."},
{k:"Tarih",s:"İlk yazıyı kim buldu?",o:["Mısırlılar","Sümerler","Romalılar","Yunanlılar"],d:1,a:"Sümerler MÖ 3500'de çivi yazısını buldu."},
{k:"Tarih",s:"Malazgirt Savaşı hangi yıl yapıldı?",o:["1071","1176","1243","1453"],d:0,a:"1071'de Anadolu'nun kapıları açıldı."},
{k:"Tarih",s:"Çanakkale Savaşı ne zaman oldu?",o:["1912","1914","1915","1918"],d:2,a:"Çanakkale Savaşı 1915'te yapıldı."},
{k:"Tarih",s:"Hangi medeniyet piramitleri inşa etti?",o:["Romalılar","Yunanlılar","Mısırlılar","Fenikeliler"],d:2,a:"Antik Mısırlılar inşa etti."},
{k:"Tarih",s:"Atatürk'ün soyadı ne zaman verildi?",o:["1920","1923","1934","1938"],d:2,a:"1934 Soyadı Kanunu ile verildi."},
{k:"Tarih",s:"Ankara ne zaman başkent oldu?",o:["1920","1923","1925","1930"],d:1,a:"13 Ekim 1923'te başkent ilan edildi."},
{k:"Tarih",s:"Türk bayrağındaki ay-yıldız neyi temsil eder?",o:["Güneş","Bağımsızlık","Ay ve yıldız","Deniz"],d:2,a:"Bayraktaki semboller ay ve yıldızdır."},
{k:"Tarih",s:"Cumhuriyet öncesi devletin adı neydi?",o:["Selçuklu","Osmanlı","Bizans","Roma"],d:1,a:"Osmanlı İmparatorluğu'ydu."},
{k:"Tarih",s:"Atatürk'ün ilk askeri başarısı nerede oldu?",o:["İstanbul","Çanakkale","Sakarya","Ankara"],d:1,a:"Çanakkale'de büyük başarı kazandı."},
{k:"Tarih",s:"İstiklal Marşı'nı kim yazdı?",o:["Atatürk","Mehmet Akif Ersoy","Nazım Hikmet","Yahya Kemal"],d:1,a:"Mehmet Akif Ersoy yazmıştır."},
{k:"Tarih",s:"İstiklal Marşı ne zaman kabul edildi?",o:["1920","1921","1923","1930"],d:1,a:"12 Mart 1921'de kabul edildi."},
{k:"Tarih",s:"Harf inkılabı ne zaman yapıldı?",o:["1923","1925","1928","1934"],d:2,a:"1928'de Latin harflerine geçildi."},
{k:"Tarih",s:"İlk Türk devleti hangisidir?",o:["Osmanlı","Selçuklu","Göktürk","Hun"],d:3,a:"Büyük Hun İmparatorluğu ilk Türk devletidir."},
{k:"Tarih",s:"Mete Han hangi devletin hükümdarıdır?",o:["Osmanlı","Selçuklu","Göktürk","Hun"],d:3,a:"Mete Han Büyük Hun İmparatorluğu hükümdarıdır."},
{k:"Tarih",s:"Kurtuluş Savaşı hangi yıllar arasında oldu?",o:["1914-1918","1919-1922","1923-1930","1912-1913"],d:1,a:"Kurtuluş Savaşı 1919-1922 arasında oldu."},
{k:"Tarih",s:"İlk Türk kadın pilotu kimdir?",o:["Halide Edib","Sabiha Gökçen","Safiye Ayla","Afet İnan"],d:1,a:"Sabiha Gökçen dünyanın ilk kadın savaş pilotudur."},
{k:"Tarih",s:"10 Kasım neyi anlatır?",o:["Bayram","Atatürk'ün ölüm yıldönümü","Zafer","Cumhuriyet"],d:1,a:"Atatürk 10 Kasım 1938'de vefat etti."},
{k:"Tarih",s:"Hangisi Atatürk'ün ilkelerinden biridir?",o:["Monarşi","Cumhuriyetçilik","Krallık","Sultanlık"],d:1,a:"Cumhuriyetçilik 6 ilkeden biridir."},
{k:"Tarih",s:"Troya Savaşı hangi ülkede geçer?",o:["Yunanistan","Mısır","Türkiye (Çanakkale)","İtalya"],d:2,a:"Troya, Çanakkale'dedir."},
{k:"Tarih",s:"İlk olimpiyatlar nerede yapıldı?",o:["Roma","Atina","Paris","Londra"],d:1,a:"Antik Yunanistan'da, Atina yakınlarında."},
{k:"Tarih",s:"Leonardo da Vinci hangi çağda yaşadı?",o:["Antik Çağ","Orta Çağ","Rönesans","Modern"],d:2,a:"Rönesans döneminin ünlü dahisidir."},
{k:"Tarih",s:"Kristof Kolomb neyi keşfetti?",o:["Avustralya","Amerika","Hindistan","Afrika"],d:1,a:"1492'de Amerika kıtasını keşfetti."},
{k:"Tarih",s:"Tekerlek ilk nerede icat edildi?",o:["Mısır","Mezopotamya","Çin","Roma"],d:1,a:"Mezopotamya'da (Sümerler) icat edildi."},
{k:"Tarih",s:"Matbaayı kim icat etti?",o:["Edison","Gutenberg","Bell","Newton"],d:1,a:"Johannes Gutenberg 1440'ta icat etti."},
{k:"Tarih",s:"Osmanlı'nın en uzun süre tahtta kalan padişahı kimdir?",o:["Fatih","Kanuni","II. Abdülhamid","Yavuz"],d:1,a:"Kanuni Sultan Süleyman 46 yıl hüküm sürdü."},
{k:"Tarih",s:"Mısır'ın ünlü kraliçesi kimdir?",o:["Victoria","Kleopatra","Elizabeth","Diana"],d:1,a:"Kleopatra Antik Mısır'ın son kraliçesidir."},
{k:"Tarih",s:"İpek Yolu neyi bağlar?",o:["Afrika-Avrupa","Asya-Avrupa","Amerika-Avrupa","Asya-Afrika"],d:1,a:"Asya'yı Avrupa'ya bağlayan ticaret yoluydu."},
{k:"Tarih",s:"Nasrettin Hoca nerelidir?",o:["Konya","Eskişehir","Akşehir","İstanbul"],d:2,a:"Akşehir'de yaşamıştır."},
{k:"Tarih",s:"Hacı Bayram Veli hangi şehirde yaşadı?",o:["İstanbul","Konya","Ankara","Bursa"],d:2,a:"Ankara'da yaşamış bir İslam alimidir."},
{k:"Tarih",s:"Yunus Emre ne ile ünlüdür?",o:["Savaş","Şiir","Resim","Mimari"],d:1,a:"Türk edebiyatının büyük şairidir."},
{k:"Tarih",s:"Kağıdı hangi medeniyet icat etti?",o:["Mısırlılar","Romalılar","Çinliler","Yunanlılar"],d:2,a:"Çinliler MÖ 105'te kağıdı icat etti."},
{k:"Tarih",s:"Barut nerede icat edildi?",o:["Mısır","Roma","Çin","Hindistan"],d:2,a:"Barut Çin'de icat edilmiştir."},
{k:"Tarih",s:"Pusula nerede icat edildi?",o:["Avrupa","Çin","Afrika","Amerika"],d:1,a:"Pusula Çin'de icat edilmiştir."},
{k:"Tarih",s:"Truva Atı hangi savaşta kullanıldı?",o:["Çanakkale","Troya","Malazgirt","Sakarya"],d:1,a:"Troya Savaşı'nda hile olarak kullanıldı."},
{k:"Tarih",s:"Dünyanın ilk haritasını kim çizdi?",o:["Piri Reis","Ptolemy","Kopernik","Kolomb"],d:0,a:"Piri Reis 1513'te ünlü haritasını çizdi."},
{k:"Tarih",s:"Selçuklu Devleti nerede kuruldu?",o:["İstanbul","İran","Anadolu","Mısır"],d:1,a:"1037'de İran'da kuruldu."},
{k:"Tarih",s:"Evliya Çelebi ne ile ünlüdür?",o:["Savaş","Seyahat","Resim","Müzik"],d:1,a:"Seyahatname adlı eserle ünlü gezgindir."},
{k:"Tarih",s:"İstanbul'un eski adı nedir?",o:["Ankara","Roma","Konstantinopolis","Atina"],d:2,a:"Bizans döneminde Konstantinopolis adıyla bilinirdi."},
{k:"Coğrafya",s:"Türkiye'nin başkenti neresidir?",o:["İstanbul","Ankara","İzmir","Bursa"],d:1,a:"Ankara 1923'ten beri başkenttir."},
{k:"Coğrafya",s:"Dünya'da kaç kıta vardır?",o:["5","6","7","8"],d:2,a:"7 kıta vardır."},
{k:"Coğrafya",s:"En büyük kıta hangisidir?",o:["Afrika","Avrupa","Asya","K.Amerika"],d:2,a:"Asya en büyük kıtadır."},
{k:"Coğrafya",s:"En küçük kıta hangisidir?",o:["Antarktika","Okyanusya","Avrupa","G.Amerika"],d:1,a:"Okyanusya en küçük kıtadır."},
{k:"Coğrafya",s:"Dünya'nın en büyük okyanusu hangisidir?",o:["Atlas","Hint","Arktik","Pasifik"],d:3,a:"Pasifik en büyük okyanustur."},
{k:"Coğrafya",s:"Türkiye kaç coğrafi bölgeye ayrılır?",o:["5","6","7","8"],d:2,a:"7 coğrafi bölge vardır."},
{k:"Coğrafya",s:"Türkiye'nin en büyük gölü hangisidir?",o:["Tuz Gölü","Beyşehir","Van Gölü","Burdur"],d:2,a:"Van Gölü en büyük göldür."},
{k:"Coğrafya",s:"Türkiye'nin en uzun nehri hangisidir?",o:["Sakarya","Fırat","Kızılırmak","Dicle"],d:2,a:"Kızılırmak 1355 km ile en uzundur."},
{k:"Coğrafya",s:"Türkiye'nin en yüksek dağı hangisidir?",o:["Erciyes","Uludağ","Ağrı Dağı","Kaçkar"],d:2,a:"Ağrı Dağı 5137 m ile en yüksektir."},
{k:"Coğrafya",s:"Dünya'nın en uzun nehri hangisidir?",o:["Amazon","Nil","Mississippi","Tuna"],d:1,a:"Nil yaklaşık 6650 km'dir."},
{k:"Coğrafya",s:"Dünya'nın en yüksek dağı hangisidir?",o:["K2","Ağrı","Everest","Kilimanjaro"],d:2,a:"Everest 8849 m'dir."},
{k:"Coğrafya",s:"Sahara Çölü hangi kıtadadır?",o:["Asya","Avrupa","Afrika","Amerika"],d:2,a:"Sahara Afrika'dadır."},
{k:"Coğrafya",s:"Himalaya Dağları hangi kıtadadır?",o:["Avrupa","Afrika","Asya","Amerika"],d:2,a:"Himalayalar Asya'dadır."},
{k:"Coğrafya",s:"Amazon Ormanları hangi kıtadadır?",o:["Afrika","Asya","Avrupa","G.Amerika"],d:3,a:"Amazon G.Amerika'dadır."},
{k:"Coğrafya",s:"Ekvator çizgisi neyi ikiye böler?",o:["Doğu-Batı","Kuzey-Güney","Deniz-Kara","Gece-Gündüz"],d:1,a:"Dünyayı kuzey-güney yarımküreye böler."},
{k:"Coğrafya",s:"Kutup yıldızı hangi yönü gösterir?",o:["Güney","Doğu","Batı","Kuzey"],d:3,a:"Kuzey yönünü gösterir."},
{k:"Coğrafya",s:"İstanbul Boğazı hangi denizleri birleştirir?",o:["Ege-Marmara","Karadeniz-Marmara","Akdeniz-Ege","Karadeniz-Ege"],d:1,a:"Karadeniz ile Marmara'yı birleştirir."},
{k:"Coğrafya",s:"Antarktika nasıl bir yerdir?",o:["Çok sıcak","Çok soğuk","Ilıman","Tropikal"],d:1,a:"Dünyanın en soğuk kıtasıdır."},
{k:"Coğrafya",s:"Tuna Nehri hangi kıtadadır?",o:["Asya","Avrupa","Afrika","Amerika"],d:1,a:"Avrupa'nın ikinci en uzun nehridir."},
{k:"Coğrafya",s:"Kilimanjaro Dağı hangi kıtadadır?",o:["Asya","Avrupa","G.Amerika","Afrika"],d:3,a:"Afrika'nın en yüksek dağıdır."},
{k:"Coğrafya",s:"Mississippi Nehri hangi ülkededir?",o:["Kanada","Brezilya","ABD","Meksika"],d:2,a:"ABD'nin en uzun nehridir."},
{k:"Coğrafya",s:"Tuz Gölü hangi bölgededir?",o:["Ege","Karadeniz","İç Anadolu","Akdeniz"],d:2,a:"İç Anadolu Bölgesi'ndedir."},
{k:"Coğrafya",s:"Karadeniz Bölgesi neyle ünlüdür?",o:["Turunçgil","Çay ve fındık","Pamuk","Zeytin"],d:1,a:"Çay ve fındık üretimiyle ünlüdür."},
{k:"Coğrafya",s:"Akdeniz Bölgesi neyle ünlüdür?",o:["Çay","Fındık","Turunçgiller","Buğday"],d:2,a:"Turunçgil üretimiyle ünlüdür."},
{k:"Coğrafya",s:"Kapadokya neyle ünlüdür?",o:["Deniz","Peri bacaları","Orman","Göl"],d:1,a:"Peri bacaları ve balon turlarıyla ünlüdür."},
{k:"Coğrafya",s:"Ege Denizi hangi iki ülke arasındadır?",o:["Türkiye-İtalya","Türkiye-Yunanistan","Türkiye-Mısır","İtalya-Yunanistan"],d:1,a:"Türkiye ve Yunanistan arasındadır."},
{k:"Coğrafya",s:"Karadeniz hangi denize bağlanır?",o:["Ege","Akdeniz","Marmara","Kızıldeniz"],d:2,a:"İstanbul Boğazı ile Marmara'ya bağlanır."},
{k:"Coğrafya",s:"Büyük Set Resifi hangi ülkededir?",o:["Brezilya","Meksika","Avustralya","Japonya"],d:2,a:"Avustralya kıyısındadır."},
{k:"Coğrafya",s:"And Dağları hangi kıtadadır?",o:["Avrupa","Asya","G.Amerika","Afrika"],d:2,a:"Güney Amerika boyunca uzanır."},
{k:"Coğrafya",s:"Alpler hangi kıtadadır?",o:["Asya","Avrupa","Afrika","Amerika"],d:1,a:"Avrupa'nın en büyük dağ silsilesidir."},
{k:"Coğrafya",s:"Amazon Nehri hangi kıtadadır?",o:["Afrika","Asya","Avrupa","G.Amerika"],d:3,a:"Güney Amerika'nın en büyük nehridir."},
{k:"Coğrafya",s:"Hangisi Türkiye'nin komşusu değildir?",o:["Yunanistan","Bulgaristan","Mısır","Gürcistan"],d:2,a:"Mısır komşu değildir."},
{k:"Coğrafya",s:"Pamukkale hangi ildedir?",o:["Muğla","Antalya","Denizli","Aydın"],d:2,a:"Denizli'dedir."},
{k:"Coğrafya",s:"Uludağ hangi şehirdedir?",o:["İstanbul","Ankara","Bursa","Eskişehir"],d:2,a:"Bursa'dadır, kayak merkezidir."},
{k:"Coğrafya",s:"Efes Antik Kenti hangi ildedir?",o:["İzmir","Aydın","Muğla","Denizli"],d:0,a:"İzmir Selçuk'tadır."},
{k:"Coğrafya",s:"Göbeklitepe hangi ildedir?",o:["Diyarbakır","Şanlıurfa","Mardin","Gaziantep"],d:1,a:"Şanlıurfa'dadır, 12.000 yıllık!"},
{k:"Coğrafya",s:"Mardin hangi bölgededir?",o:["Ege","İç Anadolu","Güneydoğu Anadolu","Karadeniz"],d:2,a:"Güneydoğu Anadolu'dadır."},
{k:"Coğrafya",s:"Rize neyle ünlüdür?",o:["Zeytin","Çay","Pamuk","Buğday"],d:1,a:"Türkiye'nin çay başkentidir."},
{k:"Coğrafya",s:"Türkiye hangi kıtalarda yer alır?",o:["Avrupa","Asya","Avrupa ve Asya","Afrika"],d:2,a:"Hem Avrupa hem Asya kıtasındadır."},
{k:"Coğrafya",s:"Dünya'nın en derin gölü hangisidir?",o:["Hazar","Victoria","Baykal","Van"],d:2,a:"Baykal Gölü Rusya'dadır."},
{k:"Coğrafya",s:"Hangi ülke çizme şeklindedir?",o:["Fransa","İspanya","İtalya","Yunanistan"],d:2,a:"İtalya haritada çizmeye benzer."},
{k:"Bilim",s:"Suyun kimyasal formülü nedir?",o:["CO2","H2O","O2","NaCl"],d:1,a:"Su H2O'dur."},
{k:"Bilim",s:"Güneş bir yıldız mıdır?",o:["Evet","Hayır","Gezegen","Uydu"],d:0,a:"Güneş en yakın yıldızımızdır."},
{k:"Bilim",s:"Dünya'nın uydusu hangisidir?",o:["Güneş","Mars","Ay","Venüs"],d:2,a:"Ay Dünya'nın tek doğal uydusudur."},
{k:"Bilim",s:"Hangi gezegen Kızıl Gezegen olarak bilinir?",o:["Venüs","Jüpiter","Mars","Satürn"],d:2,a:"Mars yüzeyindeki demir oksit nedeniyle kızıldır."},
{k:"Bilim",s:"Bitkiler oksijeni nasıl üretir?",o:["Köklerle","Fotosentez ile","Tohumla","Yaprak dökerek"],d:1,a:"Fotosentez yaparak oksijen üretir."},
{k:"Bilim",s:"Gökyüzü neden mavidir?",o:["Su yansıması","Işığın saçılması","Boyalı","Hayal"],d:1,a:"Güneş ışığı atmosferde saçılır."},
{k:"Bilim",s:"Termometre ne ölçer?",o:["Ağırlık","Uzunluk","Sıcaklık","Hız"],d:2,a:"Sıcaklığı ölçer."},
{k:"Bilim",s:"Maddenin üç hali nedir?",o:["Sıcak-soğuk-ılık","Katı-sıvı-gaz","Büyük-küçük-orta","Hafif-ağır-orta"],d:1,a:"Katı, sıvı ve gaz."},
{k:"Bilim",s:"Dinozorlar ne zaman yaşadı?",o:["100 yıl önce","1000 yıl önce","Milyon yıllar önce","10 yıl önce"],d:2,a:"65 milyon yıl önce yok oldu."},
{k:"Bilim",s:"Kalp ne işe yarar?",o:["Yemek sindirir","Kan pompalar","Nefes aldırır","Düşündürür"],d:1,a:"Kanı vücuda pompalar."},
{k:"Bilim",s:"Kaç duyu organımız vardır?",o:["3","4","5","6"],d:2,a:"Görme, işitme, dokunma, tat, koku."},
{k:"Bilim",s:"Beyin ne işe yarar?",o:["Kan pompalar","Düşünmemizi sağlar","Yemek sindirir","Nefes alır"],d:1,a:"Düşünce ve kontrol merkezidir."},
{k:"Bilim",s:"Yerçekimini kim keşfetti?",o:["Einstein","Newton","Galileo","Edison"],d:1,a:"Isaac Newton keşfetti."},
{k:"Bilim",s:"İlk ampulü kim icat etti?",o:["Newton","Einstein","Edison","Bell"],d:2,a:"Thomas Edison icat etti."},
{k:"Bilim",s:"Telefonu kim icat etti?",o:["Edison","Bell","Tesla","Marconi"],d:1,a:"Alexander Graham Bell icat etti."},
{k:"Bilim",s:"Dünya Güneş'in etrafında kaç günde döner?",o:["30","180","365","730"],d:2,a:"Yaklaşık 365 gün, yani 1 yıl."},
{k:"Bilim",s:"Yağmur nasıl oluşur?",o:["Deniz taşar","Bulutlarda su yoğuşur","Gökyüzü ağlar","Rüzgar eser"],d:1,a:"Su buharı yoğuşarak oluşur."},
{k:"Bilim",s:"Hangisi yenilenebilir enerji kaynağıdır?",o:["Kömür","Petrol","Güneş","Doğalgaz"],d:2,a:"Güneş enerjisi tükenmez."},
{k:"Bilim",s:"Ses hangi ortamda iletilmez?",o:["Havada","Suda","Boşlukta","Demirde"],d:2,a:"Ses vakumda iletilemez."},
{k:"Bilim",s:"Mıknatıs hangi maddeleri çeker?",o:["Tahta","Plastik","Demir","Cam"],d:2,a:"Demir ve çelik gibi metalleri çeker."},
{k:"Bilim",s:"Hangisi Güneş Sistemi'nde gezegen değildir?",o:["Mars","Venüs","Ay","Satürn"],d:2,a:"Ay gezegen değil, uydudur."},
{k:"Bilim",s:"Dünya'nın şekli neye benzer?",o:["Düz","Küre","Küp","Silindir"],d:1,a:"Kutuplardan basık bir küre."},
{k:"Bilim",s:"Havada en çok bulunan gaz hangisidir?",o:["Oksijen","Karbondioksit","Azot","Hidrojen"],d:2,a:"Havanın %78'i azottur."},
{k:"Bilim",s:"Buz neyin katı halidir?",o:["Hava","Su","Toprak","Ateş"],d:1,a:"Buz suyun katı halidir."},
{k:"Bilim",s:"Buhar neyin gaz halidir?",o:["Hava","Su","Toprak","Ateş"],d:1,a:"Buhar suyun gaz halidir."},
{k:"Bilim",s:"Ay ışığını nereden alır?",o:["Kendi üretir","Güneş'ten yansıtır","Yıldızlardan","Dünya'dan"],d:1,a:"Güneş ışığını yansıtır."},
{k:"Bilim",s:"Hangisi fosil yakıttır?",o:["Güneş","Rüzgar","Petrol","Su"],d:2,a:"Petrol fosil yakıttır."},
{k:"Bilim",s:"Yıldırım nasıl oluşur?",o:["Güneşten","Rüzgardan","Elektrik boşalmasından","Yağmurdan"],d:2,a:"Bulutlardaki elektrik boşalmasıdır."},
{k:"Bilim",s:"Göçmen kuşlar neden göç eder?",o:["Canları sıkılır","Soğuktan kaçar","Eğlence","Alışkanlık"],d:1,a:"Soğuk iklimden sıcak bölgelere göç eder."},
{k:"Bilim",s:"Kış uykusuna yatan hayvan hangisidir?",o:["Kedi","Tavşan","Ayı","Tavuk"],d:2,a:"Ayılar kış uykusuna yatar."},
{k:"Bilim",s:"Ağaçların en önemli görevi nedir?",o:["Gölge","Oksijen üretmek","Meyve","Odun"],d:1,a:"Fotosentez yaparak oksijen üretirler."},
{k:"Bilim",s:"Hangisi doğal afet değildir?",o:["Deprem","Sel","Gece","Tsunami"],d:2,a:"Gece doğal olay ama afet değildir."},
{k:"Bilim",s:"Güneş Sistemi'nin en büyük gezegeni hangisidir?",o:["Mars","Dünya","Jüpiter","Satürn"],d:2,a:"Jüpiter en büyük gezegendir."},
{k:"Bilim",s:"Hangisi gezegenin halkalarıyla ünlüdür?",o:["Mars","Venüs","Jüpiter","Satürn"],d:3,a:"Satürn halkalarıyla ünlüdür."},
{k:"Bilim",s:"Işık hızı yaklaşık kaç km/s'dir?",o:["100.000","200.000","300.000","400.000"],d:2,a:"Yaklaşık 300.000 km/s'dir."},
{k:"Doğa",s:"Hangi hayvan miyav der?",o:["Köpek","Kedi","Kuş","Tavşan"],d:1,a:"Kediler miyavlar!"},
{k:"Doğa",s:"Arı ne üretir?",o:["Süt","Yumurta","Bal","Peynir"],d:2,a:"Arılar bal üretir."},
{k:"Doğa",s:"Hangisi memeli değildir?",o:["Kedi","Köpek","Yılan","At"],d:2,a:"Yılan sürüngendir."},
{k:"Doğa",s:"Kurbağa yavrusuna ne denir?",o:["Civciv","İribaş","Tırtıl","Larva"],d:1,a:"İribaş denir."},
{k:"Doğa",s:"Tırtıl büyüyünce ne olur?",o:["Arı","Kelebek","Örümcek","Karınca"],d:1,a:"Koza örer ve kelebek olur."},
{k:"Doğa",s:"En hızlı kara hayvanı hangisidir?",o:["Aslan","Çita","At","Tavşan"],d:1,a:"Çita 120 km/h hıza ulaşır."},
{k:"Doğa",s:"Penguen uçabilir mi?",o:["Evet","Hayır","Bazen","Kışın"],d:1,a:"Uçamaz ama çok iyi yüzer."},
{k:"Doğa",s:"Hangisi böcek değildir?",o:["Karınca","Arı","Örümcek","Uğur böceği"],d:2,a:"Örümcek eklembacaklıdır."},
{k:"Doğa",s:"Develerin hörgücünde ne vardır?",o:["Su","Yağ","Hava","Kan"],d:1,a:"Yağ depolanır, su değil!"},
{k:"Doğa",s:"Hangisi gece aktif hayvandır?",o:["Tavuk","Baykuş","Serçe","Güvercin"],d:1,a:"Baykuş gece avcısıdır."},
{k:"Doğa",s:"Zürafanın boynu neden uzundur?",o:["Koşmak","Yüksek yapraklara ulaşmak","Güzellik","Savaş"],d:1,a:"Yüksek ağaçların yapraklarını yemek için."},
{k:"Doğa",s:"Balıklar nasıl nefes alır?",o:["Burunla","Solungaçla","Ağızla","Deriyle"],d:1,a:"Solungaçlarıyla nefes alır."},
{k:"Doğa",s:"Hangisi otçuldur?",o:["Aslan","Kartal","İnek","Köpekbalığı"],d:2,a:"İnek otçuldur."},
{k:"Doğa",s:"Hangisi etçildir?",o:["Tavşan","Koyun","Keçi","Aslan"],d:3,a:"Aslan etçildir."},
{k:"Doğa",s:"Hangisi kuş değildir?",o:["Kartal","Serçe","Yarasa","Papağan"],d:2,a:"Yarasa bir memelidir."},
{k:"Doğa",s:"Hangisi suda yaşar?",o:["Kartal","Kedi","Yunus","Aslan"],d:2,a:"Yunuslar denizde yaşar."},
{k:"Doğa",s:"Bukalemun ne yapabilir?",o:["Uçabilir","Renk değiştirebilir","Konuşabilir","Ateş püskürür"],d:1,a:"Renk değiştirebilir."},
{k:"Doğa",s:"Ahtapotun kaç kolu vardır?",o:["4","6","8","10"],d:2,a:"8 kolu vardır."},
{k:"Doğa",s:"Hangisi çölde yaşar?",o:["Penguen","Kutup ayısı","Deve","Yunus"],d:2,a:"Develer çöle uyum sağlamıştır."},
{k:"Doğa",s:"Hangisi yaprak dökmeyen ağaçtır?",o:["Meşe","Kavak","Çam","Kayın"],d:2,a:"Çam her dem yeşildir."},
{k:"Doğa",s:"Arılar çiçeklerden ne toplar?",o:["Yaprak","Toprak","Nektar","Su"],d:2,a:"Nektar toplayarak bal üretir."},
{k:"Doğa",s:"Hangisi göçmen kuştur?",o:["Serçe","Güvercin","Leylek","Karga"],d:2,a:"Leylekler kışın Afrika'ya göç eder."},
{k:"Doğa",s:"En büyük kuş hangisidir?",o:["Kartal","Devekuşu","Penguen","Albatros"],d:1,a:"Devekuşu dünyanın en büyük kuşudur."},
{k:"Doğa",s:"Hangisi en hızlı kuştur?",o:["Kartal","Şahin","Güvercin","Papağan"],d:1,a:"Şahin dalışta 320 km/h'e ulaşır."},
{k:"Doğa",s:"Hangi hayvanın boynuzları her yıl yenilenir?",o:["İnek","Geyik","Keçi","Koç"],d:1,a:"Geyiklerin boynuzları yenilenir."},
{k:"Doğa",s:"Fil kaç yıl yaşar?",o:["20","40","60-70","100"],d:2,a:"Filler 60-70 yıl yaşayabilir."},
{k:"Doğa",s:"Kanguru yavrusunu nerede taşır?",o:["Sırtında","Kesesinde","Ağzında","Kuyruğunda"],d:1,a:"Kangurular yavruyu karnındaki kesede taşır."},
{k:"Doğa",s:"Hangisi denizde yaşayan memeli değildir?",o:["Yunus","Balina","Fok","Köpekbalığı"],d:3,a:"Köpekbalığı bir balıktır, memeli değil."},
{k:"Doğa",s:"Kaplumbağa nereye yumurta bırakır?",o:["Suya","Kumsal","Ağaca","Taşa"],d:1,a:"Deniz kaplumbağaları kumsala yumurtlar."},
{k:"Doğa",s:"Papağan ne yapabilir?",o:["Uçamaz","Konuşabilir (taklit)","Yüzebilir","Kazabilir"],d:1,a:"Papağanlar insan sesini taklit edebilir."},
{k:"Doğa",s:"Hangisi hem karada hem suda yaşar?",o:["Kedi","Kurbağa","Güvercin","Aslan"],d:1,a:"Kurbağalar amfibidir."},
{k:"Doğa",s:"İpek böceği ne üretir?",o:["Bal","İpek","Süt","Yün"],d:1,a:"İpek böceği iplik üretir."},
{k:"Doğa",s:"Sincap kışa nasıl hazırlanır?",o:["Göç eder","Yiyecek depolar","Uyumaz","Hiç hazırlanmaz"],d:1,a:"Fındık ve ceviz gibi yiyecekleri depolar."},
{k:"Doğa",s:"Dünyanın en büyük hayvanı hangisidir?",o:["Fil","Zürafa","Mavi balina","Gergedan"],d:2,a:"Mavi balina 30 metreye ulaşabilir."},
{k:"Doğa",s:"Hangisi uçabilen tek memeli hayvandır?",o:["Sincap","Yarasa","Penguen","Uçan balık"],d:1,a:"Yarasa uçabilen tek memelidir."},
{k:"Başkentler",s:"Fransa'nın başkenti neresidir?",o:["Lyon","Marsilya","Paris","Nice"],d:2,a:"Paris başkenttir."},
{k:"Başkentler",s:"İngiltere'nin başkenti neresidir?",o:["Manchester","Liverpool","Londra","Birmingham"],d:2,a:"Londra başkenttir."},
{k:"Başkentler",s:"Almanya'nın başkenti neresidir?",o:["Münih","Berlin","Hamburg","Frankfurt"],d:1,a:"Berlin başkenttir."},
{k:"Başkentler",s:"İtalya'nın başkenti neresidir?",o:["Milano","Venedik","Roma","Napoli"],d:2,a:"Roma başkenttir."},
{k:"Başkentler",s:"Japonya'nın başkenti neresidir?",o:["Osaka","Kyoto","Tokyo","Nagoya"],d:2,a:"Tokyo başkenttir."},
{k:"Başkentler",s:"Rusya'nın başkenti neresidir?",o:["Petersburg","Moskova","Kiev","Minsk"],d:1,a:"Moskova başkenttir."},
{k:"Başkentler",s:"Mısır'ın başkenti neresidir?",o:["İskenderiye","Kahire","Luksor","Asuan"],d:1,a:"Kahire başkenttir."},
{k:"Başkentler",s:"ABD'nin başkenti neresidir?",o:["New York","Los Angeles","Washington","Chicago"],d:2,a:"Washington D.C. başkenttir."},
{k:"Başkentler",s:"Çin'in başkenti neresidir?",o:["Şanghay","Hong Kong","Pekin","Guangzhou"],d:2,a:"Pekin başkenttir."},
{k:"Başkentler",s:"Hindistan'ın başkenti neresidir?",o:["Mumbai","Kalküta","Yeni Delhi","Bangalore"],d:2,a:"Yeni Delhi başkenttir."},
{k:"Başkentler",s:"Kanada'nın başkenti neresidir?",o:["Toronto","Vancouver","Ottawa","Montreal"],d:2,a:"Ottawa başkenttir."},
{k:"Başkentler",s:"Avustralya'nın başkenti neresidir?",o:["Sidney","Melbourne","Canberra","Brisbane"],d:2,a:"Canberra başkenttir, Sidney değil!"},
{k:"Başkentler",s:"İspanya'nın başkenti neresidir?",o:["Barselona","Madrid","Sevilla","Valencia"],d:1,a:"Madrid başkenttir."},
{k:"Başkentler",s:"Yunanistan'ın başkenti neresidir?",o:["Selanik","Atina","Girit","Rodos"],d:1,a:"Atina başkenttir."},
{k:"Başkentler",s:"Güney Kore'nin başkenti neresidir?",o:["Tokyo","Pekin","Seul","Taipei"],d:2,a:"Seul başkenttir."},
{k:"Başkentler",s:"Meksika'nın başkenti neresidir?",o:["Havana","Meksiko","Cancun","Guadalajara"],d:1,a:"Meksiko başkenttir."},
{k:"Başkentler",s:"Brezilya'nın başkenti neresidir?",o:["Rio de Janeiro","Sao Paulo","Brasilia","Salvador"],d:2,a:"Brasilia başkenttir."},
{k:"Başkentler",s:"Arjantin'in başkenti neresidir?",o:["Santiago","Lima","Buenos Aires","Montevideo"],d:2,a:"Buenos Aires başkenttir."},
{k:"Başkentler",s:"İsveç'in başkenti neresidir?",o:["Stockholm","Oslo","Helsinki","Kopenhag"],d:0,a:"Stockholm başkenttir."},
{k:"Başkentler",s:"Norveç'in başkenti neresidir?",o:["Stockholm","Helsinki","Kopenhag","Oslo"],d:3,a:"Oslo başkenttir."},
{k:"Başkentler",s:"Finlandiya'nın başkenti neresidir?",o:["Oslo","Stockholm","Helsinki","Tallinn"],d:2,a:"Helsinki başkenttir."},
{k:"Başkentler",s:"Danimarka'nın başkenti neresidir?",o:["Oslo","Helsinki","Stockholm","Kopenhag"],d:3,a:"Kopenhag başkenttir."},
{k:"Başkentler",s:"Avusturya'nın başkenti neresidir?",o:["Münih","Viyana","Prag","Budapeşte"],d:1,a:"Viyana başkenttir."},
{k:"Başkentler",s:"İsviçre'nin başkenti neresidir?",o:["Zürih","Cenevre","Bern","Basel"],d:2,a:"Bern başkenttir."},
{k:"Başkentler",s:"Portekiz'in başkenti neresidir?",o:["Madrid","Lizbon","Porto","Sevilla"],d:1,a:"Lizbon başkenttir."},
{k:"Başkentler",s:"Polonya'nın başkenti neresidir?",o:["Prag","Varşova","Budapeşte","Bükreş"],d:1,a:"Varşova başkenttir."},
{k:"Başkentler",s:"Macaristan'ın başkenti neresidir?",o:["Viyana","Prag","Bükreş","Budapeşte"],d:3,a:"Budapeşte başkenttir."},
{k:"Başkentler",s:"Romanya'nın başkenti neresidir?",o:["Budapeşte","Sofya","Bükreş","Belgrad"],d:2,a:"Bükreş başkenttir."},
{k:"Başkentler",s:"Bulgaristan'ın başkenti neresidir?",o:["Bükreş","Belgrad","Sofya","Atina"],d:2,a:"Sofya başkenttir."},
{k:"Başkentler",s:"İran'ın başkenti neresidir?",o:["Bağdat","Tahran","Şam","Kabil"],d:1,a:"Tahran başkenttir."},
{k:"Başkentler",s:"Irak'ın başkenti neresidir?",o:["Tahran","Şam","Bağdat","Amman"],d:2,a:"Bağdat başkenttir."},
{k:"Başkentler",s:"Küba'nın başkenti neresidir?",o:["Havana","Santiago","Meksiko","San Juan"],d:0,a:"Havana başkenttir."},
{k:"Başkentler",s:"Vietnam'ın başkenti neresidir?",o:["Bangkok","Hanoi","Ho Chi Minh","Cakarta"],d:1,a:"Hanoi başkenttir."},
{k:"Başkentler",s:"Tayland'ın başkenti neresidir?",o:["Hanoi","Bangkok","Manila","Singapur"],d:1,a:"Bangkok başkenttir."},
{k:"Başkentler",s:"Kenya'nın başkenti neresidir?",o:["Lagos","Nairobi","Kampala","Addis Ababa"],d:1,a:"Nairobi başkenttir."},
{k:"Başkentler",s:"Peru'nun başkenti neresidir?",o:["Bogota","Lima","Quito","Santiago"],d:1,a:"Lima başkenttir."},
{k:"Başkentler",s:"Şili'nin başkenti neresidir?",o:["Buenos Aires","Lima","Montevideo","Santiago"],d:3,a:"Santiago başkenttir."},
{k:"Başkentler",s:"Kolombiya'nın başkenti neresidir?",o:["Lima","Bogota","Quito","Caracas"],d:1,a:"Bogota başkenttir."},
{k:"Başkentler",s:"Nijerya'nın başkenti neresidir?",o:["Lagos","Abuja","Accra","Nairobi"],d:1,a:"Abuja başkenttir, Lagos değil!"},
{k:"Başkentler",s:"Etiyopya'nın başkenti neresidir?",o:["Mogadişu","Nairobi","Addis Ababa","Hartum"],d:2,a:"Addis Ababa başkenttir."},
{k:"Başkentler",s:"Endonezya'nın başkenti neresidir?",o:["Manila","Bangkok","Cakarta","Singapur"],d:2,a:"Cakarta başkenttir."},
{k:"Deyimler",s:"'Gözden düşmek' ne demektir?",o:["Göz ağrısı","Değerini kaybetmek","Düşmek","Görmemek"],d:1,a:"İtibar kaybetmek."},
{k:"Deyimler",s:"'Ağzı açık kalmak' ne demektir?",o:["Ağız ağrısı","Çok şaşırmak","Konuşamamak","Ağız açmak"],d:1,a:"Çok şaşırmak, hayret etmek."},
{k:"Deyimler",s:"'Kulak misafiri olmak' ne demektir?",o:["Kulak ağrısı","İstemeden duymak","Misafir olmak","Kulak çekmek"],d:1,a:"Başkalarının konuşmasını istemeden duymak."},
{k:"Deyimler",s:"'Dili tutulmak' ne demektir?",o:["Dil ağrısı","Konuşamamak","Dil yemek","Yalan söylemek"],d:1,a:"Şaşkınlıktan konuşamamak."},
{k:"Deyimler",s:"'Başı derde girmek' ne demektir?",o:["Baş ağrısı","Sıkıntıya düşmek","Düşmek","Baş eğmek"],d:1,a:"Zor duruma düşmek."},
{k:"Deyimler",s:"'El ele vermek' ne demektir?",o:["Tokalaşmak","Birlikte çalışmak","El sallamak","El çırpmak"],d:1,a:"Dayanışma içinde hareket etmek."},
{k:"Deyimler",s:"'Göze girmek' ne demektir?",o:["Göze kaçmak","Beğenilmek","Göz ağrısı","Görmek"],d:1,a:"Birinin takdirini kazanmak."},
{k:"Deyimler",s:"'Kulak kabartmak' ne demektir?",o:["Kulak büyütmek","Dikkatle dinlemek","Kulak çekmek","Duymamak"],d:1,a:"Dikkatini vererek dinlemek."},
{k:"Deyimler",s:"'Yüzü gülmek' ne demektir?",o:["Gülmek","Mutlu olmak","Yüz yıkamak","Gülmemek"],d:1,a:"Sevinçli, mutlu olmak."},
{k:"Deyimler",s:"'Burun kıvırmak' ne demektir?",o:["Hapşırmak","Beğenmemek","Burun silmek","Koku almak"],d:1,a:"Küçümseyip beğenmemek."},
{k:"Deyimler",s:"'Ağzı kulaklarına varmak' ne demektir?",o:["Konuşmak","Çok sevinmek","Kulak ağrısı","Gülmek"],d:1,a:"Çok mutlu olmak."},
{k:"Deyimler",s:"'Göz yummak' ne demektir?",o:["Uyumak","Görmezden gelmek","Göz kırpmak","Bakmamak"],d:1,a:"Kusuru görmezden gelmek."},
{k:"Deyimler",s:"'Dil dökmek' ne demektir?",o:["Dil çıkarmak","İkna etmeye çalışmak","Dil yemek","Susmak"],d:1,a:"Güzel sözlerle ikna etmeye çalışmak."},
{k:"Deyimler",s:"'Ayak diremek' ne demektir?",o:["Koşmak","İnat etmek","Ayak ağrısı","Durmak"],d:1,a:"Fikrini değiştirmemekte ısrar etmek."},
{k:"Deyimler",s:"'Parmak ısırmak' ne demektir?",o:["Parmak ağrısı","Çok şaşırmak","Parmak kesmek","Isırmak"],d:1,a:"Hayret etmek, çok şaşırmak."},
{k:"Deyimler",s:"'Çam devirmek' ne demektir?",o:["Ağaç kesmek","Gaf yapmak","Çam dikmek","Orman gezmek"],d:1,a:"Yersiz söz söylemek."},
{k:"Deyimler",s:"'Etekleri zil çalmak' ne demektir?",o:["Zil çalmak","Çok sevinmek","Etek giymek","Dans etmek"],d:1,a:"Çok mutlu olmak, sevinçten uçmak."},
{k:"Deyimler",s:"'İpe un sermek' ne demektir?",o:["Un dökmek","Oyalayıp işten kaçmak","İp germek","Un elemek"],d:1,a:"Bahane uydurup işten kaçınmak."},
{k:"Deyimler",s:"'Taşı gediğine koymak' ne demektir?",o:["Taş atmak","Yerinde söz söylemek","Taş kırmak","Duvar örmek"],d:1,a:"En uygun cevabı vermek."},
{k:"Deyimler",s:"'Kafa tutmak' ne demektir?",o:["Kafa vurmak","Karşı gelmek","Kafa ağrısı","Düşünmek"],d:1,a:"Meydan okumak, karşı gelmek."},
{k:"Deyimler",s:"'Yüz bulmak' ne demektir?",o:["Yüz yıkamak","Cesaret kazanıp küstahlaşmak","Güzel olmak","Yüz ağrısı"],d:1,a:"Hoşgörüden yararlanıp küstahça davranmak."},
{k:"Deyimler",s:"'Göz açıp kapayıncaya kadar' ne demektir?",o:["Uyumak","Çok kısa sürede","Göz kırpmak","Uzun sürede"],d:1,a:"Çok çabuk, bir an içinde."},
{k:"Deyimler",s:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",o:["Ateş yak","Her söylentinin sebebi var","Duman çıkar","Ateş sön"],d:1,a:"Her dedikodunun arkasında gerçeklik payı var."},
{k:"Deyimler",s:"'Tüylerini diken diken etmek' ne demektir?",o:["Üşümek","Çok korkmak veya heyecanlanmak","Tüy dökmek","Soğuk almak"],d:1,a:"Korku veya heyecandan tüylerin ürpermesi."},
{k:"Deyimler",s:"'Saman altından su yürütmek' ne demektir?",o:["Su taşımak","Gizlice iş çevirmek","Saman taşımak","Su dökmek"],d:1,a:"Gizlice ve sinsi planlar yapmak."},
{k:"Atasözleri",s:"'Damlaya damlaya göl olur' ne demektir?",o:["Göl oluşur","Küçük birikimler büyük sonuç verir","Su akar","Damla düşer"],d:1,a:"Az az biriktirerek büyük sonuç."},
{k:"Atasözleri",s:"'Ağaç yaşken eğilir' ne demektir?",o:["Ağaç kes","Eğitim küçükken verilmeli","Ağaç dik","Yaşlan"],d:1,a:"İnsan küçükken eğitilmeli."},
{k:"Atasözleri",s:"'Bir elin nesi var iki elin sesi var' ne demektir?",o:["El çırp","Birlikte güçlüyüz","El tut","Tek kal"],d:1,a:"Birlik ve dayanışma önemli."},
{k:"Atasözleri",s:"'Dost kara günde belli olur' ne demektir?",o:["Dost edin","Gerçek dost zor günde yanındadır","Kara gün gel","Dost ara"],d:1,a:"Gerçek dostluk zor zamanlarda ortaya çıkar."},
{k:"Atasözleri",s:"'Gülme komşuna gelir başına' ne demektir?",o:["Gül","Başkasının derdiyle dalga geçme","Komşuya git","Gülme"],d:1,a:"Başkasına gülenin başına aynısı gelebilir."},
{k:"Atasözleri",s:"'Sakla samanı gelir zamanı' ne demektir?",o:["Saman topla","İhtiyatlı ol, saklanan işe yarar","Zaman geç","Saklan"],d:1,a:"Biriktirilen bir gün işe yarar."},
{k:"Atasözleri",s:"'Acele işe şeytan karışır' ne demektir?",o:["Şeytan gelir","Aceleyle yapılan iş hatalı olur","Hızlı ol","İş yap"],d:1,a:"Aceleye getirilen işler yanlış olur."},
{k:"Atasözleri",s:"'Ayağını yorganına göre uzat' ne demektir?",o:["Uyu","İmkanına göre harca","Yorgan al","Ayak uzat"],d:1,a:"Gelirine göre harcama yap."},
{k:"Atasözleri",s:"'İşleyen demir ışıldar' ne demektir?",o:["Demir parla","Çalışan gelişir","Demir ısıt","Işık yak"],d:1,a:"Sürekli çalışan parlak kalır."},
{k:"Atasözleri",s:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",o:["Yılan tut","Güzel konuşma her kapıyı açar","Dil çıkar","Yılan besle"],d:1,a:"Nazik sözlerle her şey başarılır."},
{k:"Atasözleri",s:"'Nerde birlik orda dirlik' ne demektir?",o:["Birlik kur","Birlik olan yerde huzur olur","Dirlik bul","Bir ol"],d:1,a:"Birlikte olan toplumda huzur olur."},
{k:"Atasözleri",s:"'Yuvarlanan taş yosun tutmaz' ne demektir?",o:["Taş at","Sürekli yer değiştiren birikim yapamaz","Taş topla","Yosun bul"],d:1,a:"İstikrarsız kişi bir yere varamaz."},
{k:"Atasözleri",s:"'Bugünün işini yarına bırakma' ne demektir?",o:["Yarın gel","İşini zamanında yap","Bugün çalış","Yarın bak"],d:1,a:"İşleri ertelemeden bitir."},
{k:"Atasözleri",s:"'Bal tutan parmağını yalar' ne demektir?",o:["Bal ye","İşin başındaki çıkar sağlar","Parmak yala","Bal tut"],d:1,a:"İşi yöneten kendi payını alır."},
{k:"Atasözleri",s:"'El elden üstündür' ne demektir?",o:["El tut","Her zaman daha iyisi vardır","El sık","Üstün ol"],d:1,a:"Ne kadar iyi olursan ol, daha iyisi var."},
{k:"Atasözleri",s:"'Görünen köy kılavuz istemez' ne demektir?",o:["Köy gez","Belli olan açıklamaya gerek yok","Köy kur","Kılavuz bul"],d:1,a:"Açıkça görünen şey açıklama gerektirmez."},
{k:"Atasözleri",s:"'Mum dibine ışık vermez' ne demektir?",o:["Mum yak","Kişi yakınlarına fayda sağlayamaz","Mum sön","Işık aç"],d:1,a:"İnsan en yakınlarına bazen faydası olamaz."},
{k:"Atasözleri",s:"'Düşenin dostu olmaz' ne demektir?",o:["Düşme","Zor durumda kalana kimse yardım etmez","Dost bul","Kalk"],d:1,a:"Zorluk yaşayan kişiyi herkes terk eder."},
{k:"Atasözleri",s:"'Her yokuşun bir inişi vardır' ne demektir?",o:["Yokuş çık","Zor günler geçici, iyiye döner","İniş in","Yol yürü"],d:1,a:"Zorluklar sonsuza kadar sürmez."},
{k:"Atasözleri",s:"'Komşu komşunun külüne muhtaçtır' ne demektir?",o:["Kül ver","İnsanlar birbirine ihtiyaç duyar","Komşu ziyaret et","Kül at"],d:1,a:"Herkesin birbirine ihtiyacı var."},
{k:"Atasözleri",s:"'Dimyat'a pirince giderken bulgurdan olmak' ne demektir?",o:["Pirinç al","Elindekini de kaybetmek","Bulgur ye","Yola çık"],d:1,a:"Daha iyisini ararken mevcut olanı kaybetmek."},
{k:"Atasözleri",s:"'Çalma kapıyı çalarlar kapını' ne demektir?",o:["Kapı çal","Kötülük yaparsan karşılığını görürsün","Kapı aç","Çal"],d:1,a:"Yapılan kötülük geri döner."},
{k:"Atasözleri",s:"'Aç tavuk kendini buğday ambarında sanır' ne demektir?",o:["Tavuk besle","Muhtaç kişi küçük şeyi büyük sanır","Buğday topla","Ambar aç"],d:1,a:"İhtiyaç sahibi küçük şeyleri büyütür."},
{k:"Atasözleri",s:"'Her kuşun eti yenmez' ne demektir?",o:["Kuş avla","Her kişi ile uğraşılmaz","Kuş besle","Et ye"],d:1,a:"Bazı insanlarla uğraşmak doğru değildir."},
{k:"Atasözleri",s:"'Lafla peynir gemisi yürümez' ne demektir?",o:["Peynir ye","Sadece konuşmakla iş olmaz","Gemi sür","Laf at"],d:1,a:"İş yapmak için eylem gerekir."},
{k:"Matematik",s:"5+3 kaç eder?",o:["6","7","8","9"],d:2,a:"5+3=8"},
{k:"Matematik",s:"10-4 kaç eder?",o:["5","6","7","8"],d:1,a:"10-4=6"},
{k:"Matematik",s:"3x4 kaç eder?",o:["7","10","12","15"],d:2,a:"3x4=12"},
{k:"Matematik",s:"20÷5 kaç eder?",o:["3","4","5","6"],d:1,a:"20÷5=4"},
{k:"Matematik",s:"Bir düzinede kaç tane vardır?",o:["6","10","12","24"],d:2,a:"Bir düzine 12'dir."},
{k:"Matematik",s:"Üçgenin kaç kenarı vardır?",o:["2","3","4","5"],d:1,a:"3 kenarı vardır."},
{k:"Matematik",s:"Karenin kaç kenarı vardır?",o:["3","4","5","6"],d:1,a:"4 eşit kenarı vardır."},
{k:"Matematik",s:"1 saatte kaç dakika vardır?",o:["30","45","60","100"],d:2,a:"60 dakika."},
{k:"Matematik",s:"1 dakikada kaç saniye vardır?",o:["30","45","60","100"],d:2,a:"60 saniye."},
{k:"Matematik",s:"Yarım kilo kaç gramdır?",o:["100","250","500","1000"],d:2,a:"500 gram."},
{k:"Matematik",s:"100'ün yarısı kaçtır?",o:["25","40","50","75"],d:2,a:"50'dir."},
{k:"Matematik",s:"Bir yüzyıl kaç yıldır?",o:["10","50","100","1000"],d:2,a:"100 yıl."},
{k:"Matematik",s:"Hangisi çift sayıdır?",o:["3","5","8","11"],d:2,a:"8 çift sayıdır."},
{k:"Matematik",s:"Hangisi tek sayıdır?",o:["4","6","7","10"],d:2,a:"7 tek sayıdır."},
{k:"Matematik",s:"1 km kaç metredir?",o:["10","100","1000","10000"],d:2,a:"1000 metre."},
{k:"Matematik",s:"7x7 kaç eder?",o:["42","49","56","64"],d:1,a:"7x7=49"},
{k:"Matematik",s:"8x5 kaç eder?",o:["35","40","45","50"],d:1,a:"8x5=40"},
{k:"Matematik",s:"Dairenin çevresi neyle hesaplanır?",o:["a+b","2πr","a×b","πr²"],d:1,a:"Çevre = 2πr formülüyle."},
{k:"Matematik",s:"Dikdörtgenin alanı nasıl bulunur?",o:["a+b","a×b","2(a+b)","a²"],d:1,a:"Uzunluk × genişlik."},
{k:"Matematik",s:"1 litre kaç mililitredir?",o:["10","100","1000","10000"],d:2,a:"1000 mililitre."},
{k:"Matematik",s:"Bir çeyrek saat kaç dakikadır?",o:["10","15","20","25"],d:1,a:"15 dakika."},
{k:"Matematik",s:"0,5 kaça eşittir?",o:["Yarım","Çeyrek","Bir","İki"],d:0,a:"0,5 = yarım."},
{k:"Matematik",s:"25+25 kaç eder?",o:["40","45","50","55"],d:2,a:"25+25=50"},
{k:"Matematik",s:"Bir yılda kaç hafta vardır?",o:["48","50","52","54"],d:2,a:"52 hafta."},
{k:"Matematik",s:"6x6 kaç eder?",o:["30","32","34","36"],d:3,a:"6x6=36"},
{k:"Spor",s:"Futbolda bir takımda kaç kişi oynar?",o:["7","9","11","13"],d:2,a:"11 kişi sahada olur."},
{k:"Spor",s:"Voleybolda bir takımda kaç kişi oynar?",o:["5","6","7","8"],d:1,a:"6 kişi sahada olur."},
{k:"Spor",s:"Basketbolda bir takımda kaç kişi oynar?",o:["4","5","6","7"],d:1,a:"5 kişi sahada olur."},
{k:"Spor",s:"Olimpiyat halkaları kaç tanedir?",o:["3","4","5","6"],d:2,a:"5 halka 5 kıtayı temsil eder."},
{k:"Spor",s:"FIFA Dünya Kupası kaç yılda bir yapılır?",o:["2","3","4","5"],d:2,a:"4 yılda bir."},
{k:"Spor",s:"Tenis topuna ne ile vurulur?",o:["Sopayla","Raketle","Elle","Ayakla"],d:1,a:"Raket kullanılır."},
{k:"Spor",s:"Yüzmede kaç stil vardır?",o:["2","3","4","5"],d:2,a:"Serbest, sırt, kurbağa, kelebek: 4 stil."},
{k:"Spor",s:"Hangisi kış sporudur?",o:["Futbol","Yüzme","Kayak","Tenis"],d:2,a:"Kayak kış sporudur."},
{k:"Spor",s:"Maratonda kaç km koşulur?",o:["10","21","42","50"],d:2,a:"42.195 km."},
{k:"Spor",s:"Hangisi su sporudur?",o:["Atletizm","Su topu","Güreş","Boks"],d:1,a:"Su topu havuzda oynanır."},
{k:"Spor",s:"Hangisi raket sporudur?",o:["Futbol","Basketbol","Badminton","Yüzme"],d:2,a:"Badminton raket sporudur."},
{k:"Spor",s:"Olimpiyatlar kaç yılda bir yapılır?",o:["2","3","4","5"],d:2,a:"4 yılda bir."},
{k:"Spor",s:"Hangisi takım sporu değildir?",o:["Futbol","Voleybol","Tenis","Basketbol"],d:2,a:"Tenis bireysel oynanabilir."},
{k:"Spor",s:"Futbolda sarı kart ne anlama gelir?",o:["Atılma","Uyarı","Gol","Penaltı"],d:1,a:"Sarı kart uyarıdır."},
{k:"Spor",s:"Futbolda kırmızı kart ne anlama gelir?",o:["Uyarı","Oyundan atılma","Gol","Serbest vuruş"],d:1,a:"Kırmızı kart oyundan atılmadır."},
{k:"Spor",s:"Basketbolda 3 sayı çizgisi ne işe yarar?",o:["Faul çizgisi","Uzaktan atınca 3 puan","Başlangıç","Bitiş"],d:1,a:"Çizginin arkasından atılan 3 puan eder."},
{k:"Spor",s:"Hangisi bir atletizm dalıdır?",o:["Futbol","100 metre koşu","Basketbol","Voleybol"],d:1,a:"100 metre koşu atletizm dalıdır."},
{k:"Spor",s:"Jimnastik hangi tür spordur?",o:["Takım","Bireysel","Su","Kış"],d:1,a:"Jimnastik bireysel spordur."},
{k:"Spor",s:"Buz pateni hangi yüzeyde yapılır?",o:["Toprak","Çim","Buz","Kum"],d:2,a:"Buz üzerinde yapılır."},
{k:"Spor",s:"Hangisi dövüş sporudur?",o:["Tenis","Judo","Yüzme","Bisiklet"],d:1,a:"Judo bir dövüş sporudur."},
{k:"Spor",s:"Bisiklet yarışında Tour de France nerede yapılır?",o:["İspanya","İtalya","Almanya","Fransa"],d:3,a:"Fransa'da yapılır."},
{k:"Spor",s:"Kriket en çok hangi ülkede oynanır?",o:["ABD","Brezilya","Hindistan","Almanya"],d:2,a:"Hindistan kriketin kalesidir."},
{k:"Spor",s:"Beyzbol hangi ülkenin ulusal sporudur?",o:["İngiltere","ABD","Japonya","Kanada"],d:1,a:"ABD'nin ulusal sporlarından biridir."},
{k:"Spor",s:"Golf topuna ne ile vurulur?",o:["Raket","Sopa","El","Ayak"],d:1,a:"Golf sopası (club) ile vurulur."},
{k:"Spor",s:"Hangisi bir engelli koşu dalıdır?",o:["Maraton","110 metre engelli","Yüzme","Atlama"],d:1,a:"110 metre engelli atletizm dalıdır."},
{k:"Türkiye",s:"Türk bayrağında hangi renkler vardır?",o:["Mavi-beyaz","Kırmızı-beyaz","Yeşil-beyaz","Sarı-kırmızı"],d:1,a:"Kırmızı zemin, beyaz ay-yıldız."},
{k:"Türkiye",s:"Türkiye'nin en kalabalık şehri hangisidir?",o:["Ankara","İzmir","İstanbul","Bursa"],d:2,a:"İstanbul ~16 milyon nüfus."},
{k:"Türkiye",s:"Türkiye'nin para birimi nedir?",o:["Dolar","Euro","Türk Lirası","Sterlin"],d:2,a:"Türk Lirası (TL)."},
{k:"Türkiye",s:"Sümela Manastırı hangi ildedir?",o:["Trabzon","Rize","Artvin","Giresun"],d:0,a:"Trabzon Maçka'dadır."},
{k:"Türkiye",s:"Aspendos Tiyatrosu hangi ildedir?",o:["İzmir","Muğla","Antalya","Mersin"],d:2,a:"Antalya'dadır."},
{k:"Türkiye",s:"Türkiye'nin en doğusundaki il hangisidir?",o:["Van","Hakkari","Iğdır","Ağrı"],d:2,a:"Iğdır en doğudadır."},
{k:"Türkiye",s:"Türkiye'nin en güneydeki ili hangisidir?",o:["Antalya","Mersin","Hatay","Adana"],d:2,a:"Hatay en güneydedir."},
{k:"Türkiye",s:"Türkiye'de en çok konuşulan dil hangisidir?",o:["Arapça","İngilizce","Türkçe","Farsça"],d:2,a:"Türkçe resmi dildir."},
{k:"Türkiye",s:"Hangisi bir Türk halk çalgısıdır?",o:["Piyano","Bağlama","Gitar","Keman"],d:1,a:"Bağlama (saz) halk müziği çalgısıdır."},
{k:"Türkiye",s:"Türkiye'nin en batısındaki il hangisidir?",o:["İzmir","Çanakkale","Edirne","Muğla"],d:2,a:"Edirne en batıdadır."},
{k:"Türkiye",s:"Türkiye'nin en kuzeyindeki il hangisidir?",o:["Trabzon","Sinop","Artvin","Rize"],d:1,a:"Sinop en kuzeydedir."},
{k:"Türkiye",s:"Mevlana hangi şehirde yaşadı?",o:["İstanbul","Ankara","Konya","Bursa"],d:2,a:"Konya'da yaşadı."},
{k:"Türkiye",s:"Türkiye'nin en büyük adası hangisidir?",o:["Bozcaada","Gökçeada","Büyükada","Kıbrıs"],d:1,a:"Gökçeada en büyük Türk adasıdır."},
{k:"Türkiye",s:"Nemrut Dağı hangi ildedir?",o:["Malatya","Adıyaman","Elazığ","Diyarbakır"],d:1,a:"Adıyaman'dadır."},
{k:"Türkiye",s:"Türkiye'nin en uzun sahili hangi denize aittir?",o:["Karadeniz","Ege","Akdeniz","Marmara"],d:2,a:"Akdeniz kıyıları en uzundur."},
{k:"Türkiye",s:"Aşık Veysel hangi sanat dalında ünlüdür?",o:["Resim","Müzik","Heykel","Mimari"],d:1,a:"Türk halk müziği ozanıdır."},
{k:"Türkiye",s:"Türkiye'de en çok yetişen tarım ürünü hangisidir?",o:["Muz","Buğday","Pirinç","Pamuk"],d:1,a:"Buğday en çok yetişen üründür."},
{k:"Türkiye",s:"Atatürk Barajı hangi nehir üzerindedir?",o:["Kızılırmak","Fırat","Dicle","Sakarya"],d:1,a:"Fırat Nehri üzerindedir."},
{k:"Türkiye",s:"Çay en çok hangi bölgede yetişir?",o:["Ege","Akdeniz","Doğu Karadeniz","İç Anadolu"],d:2,a:"Doğu Karadeniz'de (Rize)."},
{k:"Türkiye",s:"Antep fıstığı hangi ilin simgesidir?",o:["Adana","Gaziantep","Malatya","Şanlıurfa"],d:1,a:"Gaziantep'in simgesidir."},
{k:"Türkiye",s:"Kayısı hangi ilin simgesidir?",o:["Gaziantep","Malatya","Mersin","Adana"],d:1,a:"Malatya kayısıyla ünlüdür."},
{k:"Türkiye",s:"İstanbul'da hangi iki kıta birleşir?",o:["Avrupa-Afrika","Asya-Afrika","Avrupa-Asya","Amerika-Asya"],d:2,a:"İstanbul Avrupa ve Asya'yı birleştirir."},
{k:"Türkiye",s:"Türkiye'nin en yüksek barajı hangisidir?",o:["Keban","Atatürk","Artvin Yusufeli","Ilısu"],d:2,a:"Artvin Yusufeli Barajı en yüksektir."},
{k:"Türkiye",s:"Türkiye'nin telefon kodu kaçtır?",o:["+1","+44","+49","+90"],d:3,a:"+90 Türkiye'nin telefon kodudur."},
{k:"Türkiye",s:"Zeytinyağı en çok hangi bölgede üretilir?",o:["Karadeniz","Ege","İç Anadolu","Doğu Anadolu"],d:1,a:"Ege Bölgesi'nde üretilir."},
{k:"Doğa",s:"Kurbağalar hangi hayvan sınıfına aittir?",o:["Memeliler","Sürüngenler","İki yaşamlılar","Balıklar"],d:2,a:"Kurbağalar hem karada hem suda yaşayan iki yaşamlılardır."}
{k:"Doğa",s:"Hangi hayvan yumurtlayarak çoğalır?",o:["Kedi","Köpek","Tavuk","İnek"],d:2,a:"Tavuklar yumurtlayarak çoğalan kuşlardır."}
{k:"Doğa",s:"Bitkiler havadan hangi gazı alır?",o:["Oksijen","Azot","Karbondioksit","Helyum"],d:2,a:"Bitkiler fotosentez için havadan karbondioksit alır."}
{k:"Doğa",s:"Hangi mevsimde ağaçlar yapraklarını döker?",o:["İlkbahar","Yaz","Sonbahar","Kış"],d:2,a:"Sonbaharda yaprak döken ağaçlar yapraklarını bırakır."}
{k:"Doğa",s:"Arılar ne üretir?",o:["Süt","Yumurta","Bal","İpek"],d:2,a:"Arılar çiçeklerden topladıkları nektarla bal üretir."}
{k:"Doğa",s:"Hangi hayvan gece aktiftir?",o:["Tavuk","Baykuş","Serçe","Güvercin"],d:1,a:"Baykuşlar gece aktif olan kuşlardır."}
{k:"Doğa",s:"Balıklar nasıl nefes alır?",o:["Burunla","Ağızla","Solungaçla","Deriyle"],d:2,a:"Balıklar sudaki oksijeni solungaçlarıyla alır."}
{k:"Doğa",s:"Hangi böcek ışık üretir?",o:["Arı","Ateş böceği","Karınca","Uğur böceği"],d:1,a:"Ateş böcekleri biolüminesans ile ışık üretir."}
{k:"Doğa",s:"En büyük kara hayvanı hangisidir?",o:["Gergedan","Zürafa","Fil","Su aygırı"],d:2,a:"Afrika fili karada yaşayan en büyük hayvandır."}
{k:"Doğa",s:"Hangi hayvan kabuğunu sırtında taşır?",o:["Kirpi","Kaplumbağa","Kertenkele","Yılan"],d:1,a:"Kaplumbağalar kabuklarını sırtlarında taşır."}
{k:"Doğa",s:"Hangi kuş uçamaz?",o:["Kartal","Deve kuşu","Şahin","Papağan"],d:1,a:"Deve kuşu uçamayan en büyük kuştur."}
{k:"Doğa",s:"Tırtıl büyüyünce ne olur?",o:["Böcek","Kelebek","Arı","Sinek"],d:1,a:"Tırtıllar başkalaşım geçirerek kelebeğe dönüşür."}
{k:"Doğa",s:"Hangi hayvanın boynuzu vardır?",o:["Kedi","Tavşan","Geyik","Tilki"],d:2,a:"Geyikler boynuzlu hayvanlardır."}
{k:"Doğa",s:"Karada ve suda yaşayan hayvanlara ne denir?",o:["Memeliler","Amfibiler","Sürüngenler","Kuşlar"],d:1,a:"Amfibiler hem karada hem suda yaşar."}
{k:"Doğa",s:"Hangi hayvan bal yapar?",o:["Karınca","Arı","Kelebek","Sinek"],d:1,a:"Bal arıları çiçek nektarından bal üretir."}
{k:"Bilim",s:"Suyun donma noktası kaç derecedir?",o:["10","0","-10","5"],d:1,a:"Saf su 0 derecede donar."}
{k:"Bilim",s:"Hangi gezegen Güneşe en yakındır?",o:["Venüs","Merkür","Mars","Dünya"],d:1,a:"Merkür Güneşe en yakın gezegendir."}
{k:"Bilim",s:"Gökkuşağında kaç renk vardır?",o:["5","6","7","8"],d:2,a:"Gökkuşağında 7 renk bulunur."}
{k:"Bilim",s:"Hangi organ kanı pompalar?",o:["Beyin","Kalp","Böbrek","Akciğer"],d:1,a:"Kalp kanı vücuda pompalayan organdır."}
{k:"Bilim",s:"Bitkilerin yeşil olmasını sağlayan madde nedir?",o:["Vitamin","Protein","Klorofil","Mineral"],d:2,a:"Klorofil bitkilere yeşil rengini verir."}
{k:"Bilim",s:"Ay Dünya nın nesidir?",o:["Gezegeni","Yıldızı","Uydusu","Güneşi"],d:2,a:"Ay Dünya nın doğal uydusudur."}
{k:"Bilim",s:"Ses hangi ortamda yayılamaz?",o:["Suda","Havada","Demirde","Boşlukta"],d:3,a:"Ses boşlukta yayılamaz."}
{k:"Bilim",s:"Hangi vitamin güneşten alınır?",o:["A vitamini","B vitamini","C vitamini","D vitamini"],d:3,a:"D vitamini güneş ışığı ile sentezlenir."}
{k:"Bilim",s:"Dünya nın şekli neye benzer?",o:["Küp","Küre","Silindir","Dikdörtgen"],d:1,a:"Dünya kutuplardan basık küre şeklindedir."}
{k:"Bilim",s:"Termometre ne ölçer?",o:["Ağırlık","Uzunluk","Sıcaklık","Hız"],d:2,a:"Termometre sıcaklık ölçen alettir."}
{k:"Bilim",s:"Dünya kendi etrafında kaç saatte döner?",o:["12 saat","24 saat","36 saat","48 saat"],d:1,a:"Dünya kendi ekseni etrafında 24 saatte döner."}
{k:"Bilim",s:"Mıknatıs hangi metali çeker?",o:["Altın","Bakır","Demir","Alüminyum"],d:2,a:"Mıknatıs demir ve çelik gibi metalleri çeker."}
{k:"Bilim",s:"Bulutlar neden oluşur?",o:["Tozdan","Su buharından","Dumandan","Rüzgardan"],d:1,a:"Bulutlar su buharının yoğunlaşmasıyla oluşur."}
{k:"Bilim",s:"Güneş sistemimizdeki en büyük gezegen hangisidir?",o:["Satürn","Jüpiter","Uranüs","Neptün"],d:1,a:"Jüpiter güneş sisteminin en büyük gezegenidir."}
{k:"Bilim",s:"Işık mı ses mi daha hızlıdır?",o:["Ses","Eşit hız","Işık","Ortama bağlı"],d:2,a:"Işık sesten çok daha hızlıdır."}
{k:"Coğrafya",s:"Türkiye nin en büyük gölü hangisidir?",o:["Tuz Gölü","Van Gölü","Beyşehir Gölü","Burdur Gölü"],d:1,a:"Van Gölü Türkiye nin en büyük gölüdür."}
{k:"Coğrafya",s:"Hangi kıtada penguen yaşar?",o:["Avrupa","Asya","Antarktika","Afrika"],d:2,a:"Penguenler çoğunlukla Antarktikada yaşar."}
{k:"Coğrafya",s:"Dünyanın en büyük okyanusu hangisidir?",o:["Atlas","Hint","Büyük Okyanus","Kuzey Buz"],d:2,a:"Büyük Okyanus dünyanın en büyük okyanusudur."}
{k:"Coğrafya",s:"Nil Nehri hangi kıtadadır?",o:["Asya","Avrupa","Afrika","Amerika"],d:2,a:"Nil Nehri Afrika kıtasındadır."}
{k:"Coğrafya",s:"Türkiye kaç coğrafi bölgeye ayrılır?",o:["5","6","7","8"],d:2,a:"Türkiye 7 coğrafi bölgeye ayrılmıştır."}
{k:"Coğrafya",s:"Everest Dağı hangi kıtadadır?",o:["Avrupa","Afrika","Asya","Amerika"],d:2,a:"Everest Dağı Asya kıtasında Nepal-Çin sınırındadır."}
{k:"Coğrafya",s:"Hangi deniz Türkiye nin kuzeyindedir?",o:["Akdeniz","Ege","Karadeniz","Marmara"],d:2,a:"Karadeniz Türkiye nin kuzey kıyısında yer alır."}
{k:"Coğrafya",s:"Amazon Ormanları hangi kıtadadır?",o:["Afrika","Asya","Güney Amerika","Avustralya"],d:2,a:"Amazon yağmur ormanları Güney Amerikadadır."}
{k:"Coğrafya",s:"Dünyanın en küçük kıtası hangisidir?",o:["Avrupa","Antarktika","Avustralya","Afrika"],d:2,a:"Avustralya dünyanın en küçük kıtasıdır."}
{k:"Başkentler",s:"Japonya nın başkenti neresidir?",o:["Osaka","Tokyo","Kyoto","Hiroshima"],d:1,a:"Tokyo Japonya nın başkentidir."}
{k:"Başkentler",s:"Brezilya nın başkenti neresidir?",o:["Rio de Janeiro","Sao Paulo","Brasilia","Salvador"],d:2,a:"Brasilia Brezilya nın başkentidir."}
{k:"Başkentler",s:"Avustralya nın başkenti neresidir?",o:["Sydney","Melbourne","Canberra","Brisbane"],d:2,a:"Canberra Avustralya nın başkentidir."}
{k:"Başkentler",s:"Kanada nın başkenti neresidir?",o:["Toronto","Vancouver","Montreal","Ottawa"],d:3,a:"Ottawa Kanada nın başkentidir."}
{k:"Başkentler",s:"Hindistan ın başkenti neresidir?",o:["Mumbai","Yeni Delhi","Kalküta","Bangalore"],d:1,a:"Yeni Delhi Hindistan ın başkentidir."}
{k:"Başkentler",s:"Güney Kore nin başkenti neresidir?",o:["Busan","Seul","Incheon","Daegu"],d:1,a:"Seul Güney Kore nin başkentidir."}
{k:"Başkentler",s:"Norveç in başkenti neresidir?",o:["Stockholm","Helsinki","Oslo","Kopenhag"],d:2,a:"Oslo Norveç in başkentidir."}
{k:"Başkentler",s:"Arjantin in başkenti neresidir?",o:["Santiago","Lima","Buenos Aires","Bogota"],d:2,a:"Buenos Aires Arjantin in başkentidir."}
{k:"Başkentler",s:"Tayland ın başkenti neresidir?",o:["Hanoi","Bangkok","Jakarta","Manila"],d:1,a:"Bangkok Tayland ın başkentidir."}
{k:"Türkiye",s:"Türkiye nin en yüksek dağı hangisidir?",o:["Uludağ","Erciyes","Ağrı Dağı","Süphan Dağı"],d:2,a:"Ağrı Dağı 5137 m ile Türkiye nin en yüksek dağıdır."}
{k:"Türkiye",s:"Kapadokya hangi şehirdedir?",o:["Konya","Nevşehir","Kayseri","Aksaray"],d:1,a:"Kapadokya bölgesi ağırlıklı olarak Nevşehir ilindedir."}
{k:"Türkiye",s:"Türk bayrağında hangi simgeler vardır?",o:["Güneş ve yıldız","Ay ve yıldız","Yıldız ve çizgi","Hilal ve güneş"],d:1,a:"Türk bayrağında kırmızı zemin üzerinde beyaz ay ve yıldız bulunur."}
{k:"Türkiye",s:"Pamukkale hangi ilde bulunur?",o:["Muğla","Denizli","Aydın","Antalya"],d:1,a:"Pamukkale travertenleri Denizli ilinde yer alır."}
{k:"Türkiye",s:"Türkiye nin en uzun nehri hangisidir?",o:["Sakarya","Fırat","Kızılırmak","Dicle"],d:2,a:"Kızılırmak 1355 km ile Türkiye nin en uzun nehridir."}
{k:"Türkiye",s:"Efes Antik Kenti hangi ilde bulunur?",o:["İzmir","Aydın","Muğla","Antalya"],d:0,a:"Efes Antik Kenti İzmir in Selçuk ilçesindedir."}
{k:"Türkiye",s:"Sümela Manastırı hangi ildedir?",o:["Artvin","Rize","Trabzon","Giresun"],d:2,a:"Sümela Manastırı Trabzon un Maçka ilçesindedir."}
{k:"Türkiye",s:"Türkiye nin en büyük adası hangisidir?",o:["Bozcaada","Gökçeada","Büyükada","Akdamar"],d:1,a:"Gökçeada Türkiye nin en büyük adasıdır."}
{k:"Türkiye",s:"Nemrut Dağı hangi ildedir?",o:["Malatya","Adıyaman","Elazığ","Diyarbakır"],d:1,a:"Nemrut Dağı ve dev heykelleri Adıyaman ilindedir."}
{k:"Türkiye",s:"Aspendos Antik Tiyatrosu hangi ildedir?",o:["Mersin","Antalya","İzmir","Muğla"],d:1,a:"Aspendos Antalya nın Serik ilçesindedir."}
{k:"Türkiye",s:"Mardin hangi bölgemizdedir?",o:["Akdeniz","Güneydoğu Anadolu","Doğu Anadolu","İç Anadolu"],d:1,a:"Mardin Güneydoğu Anadolu Bölgesindedir."}
{k:"Türkiye",s:"Gelibolu Yarımadası hangi ildedir?",o:["Tekirdağ","Edirne","Çanakkale","Balıkesir"],d:2,a:"Gelibolu Yarımadası Çanakkale ilinde yer alır."}
{k:"Türkiye",s:"Göbeklitepe hangi ilde bulunur?",o:["Mardin","Diyarbakır","Şanlıurfa","Gaziantep"],d:2,a:"Göbeklitepe dünyanın en eski tapınağı olarak Şanlıurfadadır."}
{k:"Türkiye",s:"Türkiye nin en kalabalık şehri hangisidir?",o:["Ankara","İzmir","İstanbul","Bursa"],d:2,a:"İstanbul 15 milyonu aşan nüfusuyla en kalabalık şehirdir."}
{k:"Türkiye",s:"Hattuşaş Antik Kenti hangi ildedir?",o:["Çorum","Yozgat","Amasya","Tokat"],d:0,a:"Hitit başkenti Hattuşaş Çorum un Boğazkale ilçesindedir."}
{k:"Türkiye",s:"Safranbolu hangi ile bağlıdır?",o:["Kastamonu","Bartın","Karabük","Çankırı"],d:2,a:"Safranbolu Karabük iline bağlı tarihi ilçedir."}
{k:"Türkiye",s:"Türkiye nin kaç ili vardır?",o:["79","80","81","82"],d:2,a:"Türkiye 81 ilden oluşmaktadır."}
{k:"Türkiye",s:"Çanakkale Boğazı hangi denizleri birleştirir?",o:["Karadeniz-Akdeniz","Ege-Marmara","Marmara-Karadeniz","Akdeniz-Ege"],d:1,a:"Çanakkale Boğazı Ege Denizi ile Marmara Denizini birleştirir."}
{k:"Türkiye",s:"Anadolu nun en eski uygarlığı hangisidir?",o:["Romalılar","Hititler","Osmanlılar","Selçuklular"],d:1,a:"Hititler Anadolu nun en eski büyük uygarlıklarından biridir."}
{k:"Spor",s:"Futbolda bir takımda kaç oyuncu sahada bulunur?",o:["9","10","11","12"],d:2,a:"Futbolda her takımdan 11 oyuncu sahada bulunur."}
{k:"Spor",s:"Olimpiyat Oyunları kaç yılda bir yapılır?",o:["2 yıl","3 yıl","4 yıl","5 yıl"],d:2,a:"Yaz Olimpiyatları 4 yılda bir düzenlenir."}
{k:"Spor",s:"Basketbolda bir takımda kaç oyuncu sahadadır?",o:["4","5","6","7"],d:1,a:"Basketbolda her takımdan 5 oyuncu sahada bulunur."}
{k:"Spor",s:"Voleybolda bir takımda kaç oyuncu sahadadır?",o:["5","6","7","8"],d:1,a:"Voleybolda her takımdan 6 oyuncu sahada bulunur."}
{k:"Spor",s:"Hangi spor dalında raket kullanılır?",o:["Futbol","Basketbol","Tenis","Yüzme"],d:2,a:"Teniste raket ile top vurulur."}
{k:"Spor",s:"FIFA Dünya Kupası kaç yılda bir yapılır?",o:["2 yıl","3 yıl","4 yıl","5 yıl"],d:2,a:"FIFA Dünya Kupası 4 yılda bir düzenlenir."}
{k:"Spor",s:"Yüzmede hangi stil en hızlıdır?",o:["Kurbağalama","Sırtüstü","Kelebek","Serbest stil"],d:3,a:"Serbest stil en hızlı yüzme stilidir."}
{k:"Spor",s:"Maraton kaç kilometredir?",o:["21 km","30 km","42 km","50 km"],d:2,a:"Maraton 42.195 km uzunluğunda bir koşu yarışıdır."}
{k:"Spor",s:"Türkiye nin milli sporu hangisidir?",o:["Futbol","Güreş","Okçuluk","Cirit"],d:1,a:"Yağlı güreş Türkiye nin geleneksel milli sporudur."}
{k:"Spor",s:"Olimpiyat halkalarında kaç halka vardır?",o:["3","4","5","6"],d:2,a:"Olimpiyat sembolünde 5 kıtayı temsil eden 5 halka bulunur."}
{k:"Spor",s:"Kırkpınar güreşleri nerede yapılır?",o:["İstanbul","Edirne","Bursa","Antalya"],d:1,a:"Kırkpınar yağlı güreşleri her yıl Edirne de düzenlenir."}
{k:"Spor",s:"Hangi spor dalında file kullanılır?",o:["Futbol","Voleybol","Güreş","Atletizm"],d:1,a:"Voleybol sahanın ortasında file ile oynanır."}
{k:"Spor",s:"Atletizmde 100 metre koşusu ne tür bir yarıştır?",o:["Uzun mesafe","Orta mesafe","Sprint","Dayanıklılık"],d:2,a:"100 metre sprint kısa mesafe yarışıdır."}
{k:"Spor",s:"Buz hokeyi hangi yüzeyde oynanır?",o:["Çim","Toprak","Buz","Ahşap"],d:2,a:"Buz hokeyi buz üzerinde oynanan bir spordur."}
{k:"Spor",s:"Jimnastikte yer hareketleri hangi alanda yapılır?",o:["Ring","Minder","Havuz","Pist"],d:1,a:"Jimnastikte yer hareketleri minder üzerinde yapılır."}
{k:"Spor",s:"Kayak sporu hangi mevsimde yapılır?",o:["İlkbahar","Yaz","Sonbahar","Kış"],d:3,a:"Kayak kış mevsiminde karlı dağlarda yapılan bir spordur."}
{k:"Spor",s:"Masa tenisinde kullanılan alete ne denir?",o:["Raket","Sopa","Tokmak","Kürek"],d:0,a:"Masa tenisinde raket kullanılır."}
{k:"Spor",s:"Golf topunu koymaya çalıştığımız çukura ne denir?",o:["Gol","Basket","Delik","Kale"],d:2,a:"Golfte top deliğe sokulur."}
{k:"Spor",s:"Okçulukta hedefe ne denir?",o:["Kale","Pota","Nişangah","Hedef tahtası"],d:3,a:"Okçulukta okların atıldığı dairesel hedefe hedef tahtası denir."}
{k:"Spor",s:"Dalış sporunda ayağa ne takılır?",o:["Çorap","Palet","Bot","Kanat"],d:1,a:"Dalış sporunda ayağa palet takılır."}
{k:"Spor",s:"Hangi spor aletinde ip kullanılır?",o:["İp atlama","Gülle atma","Disk atma","Cirit atma"],d:0,a:"İp atlama sporunda ip kullanılır."}
{k:"Matematik",s:"12 + 15 kaç eder?",o:["25","26","27","28"],d:2,a:"12 + 15 = 27 dir."}
{k:"Matematik",s:"Bir düzinede kaç tane vardır?",o:["6","10","12","24"],d:2,a:"Bir düzine 12 adettir."}
{k:"Matematik",s:"Üçgenin kaç kenarı vardır?",o:["2","3","4","5"],d:1,a:"Üçgenin 3 kenarı vardır."}
{k:"Matematik",s:"50 nin yarısı kaçtır?",o:["20","25","30","35"],d:1,a:"50 nin yarısı 25 tir."}
{k:"Matematik",s:"6 x 7 kaç eder?",o:["36","42","48","54"],d:1,a:"6 x 7 = 42 dir."}
{k:"Matematik",s:"Bir karede kaç köşe vardır?",o:["2","3","4","5"],d:2,a:"Karenin 4 köşesi vardır."}
{k:"Matematik",s:"100 - 37 kaç eder?",o:["57","63","67","73"],d:1,a:"100 - 37 = 63 tür."}
{k:"Matematik",s:"8 x 8 kaç eder?",o:["56","62","64","72"],d:2,a:"8 x 8 = 64 tür."}
{k:"Matematik",s:"Bir saat kaç dakikadır?",o:["30","45","60","90"],d:2,a:"Bir saat 60 dakikadır."}
{k:"Matematik",s:"1 kilometre kaç metredir?",o:["100","500","1000","10000"],d:2,a:"1 kilometre 1000 metredir."}
{k:"Matematik",s:"Çift sayılar hangileridir?",o:["1 3 5","2 4 6","1 2 3","3 6 9"],d:1,a:"2 4 6 gibi 2 ye tam bölünen sayılar çift sayılardır."}
{k:"Matematik",s:"Bir yılda kaç hafta vardır?",o:["48","50","52","54"],d:2,a:"Bir yılda 52 hafta vardır."}
{k:"Matematik",s:"Üçgenin iç açıları toplamı kaç derecedir?",o:["90","120","180","360"],d:2,a:"Üçgenin iç açıları toplamı 180 derecedir."}
{k:"Matematik",s:"Bir dakika kaç saniyedir?",o:["30","45","60","100"],d:2,a:"Bir dakika 60 saniyedir."}
{k:"Matematik",s:"9 x 9 kaç eder?",o:["72","81","90","99"],d:1,a:"9 x 9 = 81 dir."}
{k:"Matematik",s:"Bir dikdörtgenin kaç kenarı vardır?",o:["3","4","5","6"],d:1,a:"Dikdörtgenin 4 kenarı vardır."}
{k:"Matematik",s:"25 x 4 kaç eder?",o:["80","90","100","120"],d:2,a:"25 x 4 = 100 dür."}
{k:"Matematik",s:"1 ton kaç kilogramdır?",o:["100","500","1000","10000"],d:2,a:"1 ton 1000 kilogramdır."}
{k:"Matematik",s:"1 litre kaç mililitredir?",o:["10","100","1000","10000"],d:2,a:"1 litre 1000 mililitredir."}
{k:"Matematik",s:"Sıfır tek mi çift mi sayıdır?",o:["Tek","Çift","Hiçbiri","İkisi de"],d:1,a:"Sıfır çift sayıdır çünkü 2 ye tam bölünür."}
{k:"Matematik",s:"Beşgenin kaç kenarı vardır?",o:["4","5","6","7"],d:1,a:"Beşgenin 5 kenarı vardır."}
{k:"Matematik",s:"7 x 6 kaç eder?",o:["36","42","48","54"],d:1,a:"7 x 6 = 42 dir."}
{k:"Matematik",s:"Pi sayısının yaklaşık değeri kaçtır?",o:["2.14","3.14","4.14","5.14"],d:1,a:"Pi sayısı yaklaşık 3.14 tür."}
{k:"Matematik",s:"144 ün karekökü kaçtır?",o:["10","11","12","13"],d:2,a:"12 x 12 = 144 karekökü 12 dir."}
{k:"Matematik",s:"Çemberin çevresi neyle hesaplanır?",o:["a x b","2 pi r","pi r kare","a kare + b kare"],d:1,a:"Çemberin çevresi 2 pi r formülüyle bulunur."}
{k:"Deyimler",s:"Göz boyamak ne anlama gelir?",o:["Güzel görmek","Aldatmak","Boyamak","Bakmak"],d:1,a:"Göz boyamak gerçeği gizleyerek iyi göstermeye çalışmak demektir."}
{k:"Deyimler",s:"Kulak misafiri olmak ne demektir?",o:["Kulağı ağrımak","Gizlice dinlemek","İyi duymak","Yardım etmek"],d:1,a:"Kulak misafiri olmak istemeden başkalarının konuşmasını duymaktır."}
{k:"Deyimler",s:"Baş tacı etmek ne anlama gelir?",o:["Taç giydirmek","Çok değer vermek","Kızmak","Başa geçmek"],d:1,a:"Bir kişiye çok değer vermek saygı göstermek demektir."}
{k:"Deyimler",s:"Dört gözle beklemek ne demektir?",o:["Gözlük takmak","Sabırsızca beklemek","Uzun süre bakmak","Görmemek"],d:1,a:"Bir şeyi sabırsızlıkla ve heyecanla beklemektir."}
{k:"Deyimler",s:"Ağzı açık kalmak ne anlama gelir?",o:["Konuşamamak","Çok şaşırmak","Uykusu gelmek","Acıkmak"],d:1,a:"Bir şeye çok şaşırmak hayrete düşmek demektir."}
{k:"Deyimler",s:"İğne ile kuyu kazmak ne demektir?",o:["Su aramak","Çok zor bir işi sabırla yapmak","Kuyu kazmak","Terzilik yapmak"],d:1,a:"Çok zor ve uzun sürecek bir işi sabırla yapmak demektir."}
{k:"Deyimler",s:"El üstünde tutmak ne anlama gelir?",o:["Taşımak","Çok değer vermek","İtmek","Uzaklaştırmak"],d:1,a:"Bir kişiye çok değer verip onu önemli kılmak demektir."}
{k:"Deyimler",s:"Gözden düşmek ne demektir?",o:["Düşmek","İtibar kaybetmek","Görmemek","Bayılmak"],d:1,a:"Birinin gözünde değerini ve itibarını kaybetmek demektir."}
{k:"Deyimler",s:"Burnundan kıl aldırmamak ne demektir?",o:["Temiz olmak","Çok sinirli ve geçimsiz olmak","Hasta olmak","Mutlu olmak"],d:1,a:"Çok huysuz ve geçimsiz olmak kimsenin lafını dinlememek demektir."}
{k:"Deyimler",s:"Yüzü gülmek ne anlama gelir?",o:["Gülmek","Mutlu ve sevinçli olmak","Şaka yapmak","Komik olmak"],d:1,a:"Mutlu ve memnun olduğu yüzünden belli olmak demektir."}
{k:"Deyimler",s:"Kol kanat germek ne demektir?",o:["Uçmak","Korumak ve yardım etmek","Kolları açmak","Dans etmek"],d:1,a:"Birini korumak ona sahip çıkmak ve yardım etmek demektir."}
{k:"Deyimler",s:"Devede kulak kalmak ne demektir?",o:["Deveye binmek","Çok az ve yetersiz kalmak","Kulak ağrısı","Hayvanları sevmek"],d:1,a:"Yapılanın çok az ve yetersiz kalması demektir."}
{k:"Deyimler",s:"Yüreği ağzına gelmek ne demektir?",o:["Hasta olmak","Çok korkmak","Yemek yemek","Sevinmek"],d:1,a:"Çok korkmak heyecandan yüreğinin yerinden çıkacakmış gibi hissetmek demektir."}
{k:"Deyimler",s:"Dil dökmek ne anlama gelir?",o:["Konuşmak","Birini ikna etmek için çok konuşmak","Yemek pişirmek","Şarkı söylemek"],d:1,a:"Birini ikna etmek veya kandırmak için çok ve etkili konuşmak demektir."}
{k:"Deyimler",s:"Tüyleri diken diken olmak ne demektir?",o:["Üşümek","Çok etkilenmek veya korkmak","Terleme","Uyumak"],d:1,a:"Korku heyecan veya hayretten çok etkilenmek demektir."}
{k:"Deyimler",s:"Parmak ısırmak ne demektir?",o:["Parmağını yemek","Çok şaşırmak veya pişman olmak","Acıkmak","Düşünmek"],d:1,a:"Çok şaşırmak veya pişmanlık duymak demektir."}
{k:"Deyimler",s:"Gözü kara olmak ne anlama gelir?",o:["Görmemek","Hiçbir şeyden korkmamak","Kör olmak","Ağlamak"],d:1,a:"Sonuçlarını düşünmeden cesurca davranmak demektir."}
{k:"Deyimler",s:"Etekleri zil çalmak ne demektir?",o:["Müzik yapmak","Çok sevinmek","Dans etmek","Etek giymek"],d:1,a:"Çok sevinmek mutluluktan uçmak demektir."}
{k:"Deyimler",s:"Çam devirmek ne anlama gelir?",o:["Ağaç kesmek","Büyük bir hata yapmak","Ormanda gezmek","Yardım etmek"],d:1,a:"Toplum içinde büyük bir gaf yapmak demektir."}
{k:"Deyimler",s:"Kaşla göz arasında ne demektir?",o:["Yüze bakmak","Çok kısa sürede fark ettirmeden","Makyaj yapmak","Gülümsemek"],d:1,a:"Çok kısa bir sürede kimse fark etmeden bir işi yapmak demektir."}
{k:"Deyimler",s:"Kılı kırk yarmak ne anlama gelir?",o:["Berber olmak","Çok titiz ve detaycı olmak","Saç kesmek","Temizlik yapmak"],d:1,a:"Bir işi son derece titiz ve özenli şekilde yapmak demektir."}
{k:"Deyimler",s:"Saman altından su yürütmek ne demektir?",o:["Çiftçilik","Gizlice iş çevirmek","Su taşımak","Tarla sulamak"],d:1,a:"Gizli gizli kimseye belli etmeden işler çevirmek demektir."}
{k:"Deyimler",s:"Taşı sıksa suyunu çıkarır ne anlama gelir?",o:["Güçlü olmak","Çok cimri olmak","Taş kırmak","Su bulmak"],d:1,a:"Çok cimri olan parasını hiç harcamayan kişi için kullanılır."}
{k:"Deyimler",s:"Pişmiş aşa su katmak ne demektir?",o:["Yemek yapmak","Olmuş işi bozmaya çalışmak","Su içmek","Yardım etmek"],d:1,a:"Olmuş bitmiş bir işi bozmaya çalışmak demektir."}
{k:"Deyimler",s:"Abayı yakmak ne demektir?",o:["Ateş yakmak","Birine aşık olmak","Ütü yapmak","Kızmak"],d:1,a:"Birine çok aşık olmak tutkuyla bağlanmak demektir."}
{k:"Atasözleri",s:"Damlaya damlaya göl olur ne anlatır?",o:["Su birikir","Azla yetinmek lazım","Küçük birikimler büyük sonuç verir","Göl oluşumu"],d:2,a:"Küçük küçük biriktirilen şeyler zamanla büyük sonuçlar doğurur."}
{k:"Atasözleri",s:"Sakla samanı gelir zamanı ne demektir?",o:["Saman topla","Her şeyin lazım olacağı gün gelir","Hayvanlara yem ver","Temizlik yap"],d:1,a:"Bugün gereksiz gibi görünen şeylerin bir gün lazım olacağını anlatır."}
{k:"Atasözleri",s:"Ağaç yaşken eğilir ne anlatır?",o:["Ağaçlar eğilir","İnsan küçükken eğitilir","Ağaç kesmek","Rüzgar eser"],d:1,a:"Eğitim küçük yaşta verilmelidir."}
{k:"Atasözleri",s:"Bir elin nesi var iki elin sesi var ne demektir?",o:["Müzik yapmak","Birlik güç demektir","El çırpmak","Parmak saymak"],d:1,a:"İş birliği yaparak daha güçlü sonuçlar elde edilir."}
{k:"Atasözleri",s:"Yuvarlanan taş yosun tutmaz ne anlatır?",o:["Taşlar yuvarlanır","Sürekli yer değiştiren tutunmaz","Doğa güzeldir","Taş toplama"],d:1,a:"Sürekli iş veya yer değiştiren kişi bir yerde tutunamaz."}
{k:"Atasözleri",s:"Gülme komşuna gelir başına ne demektir?",o:["Komşuyla gülmek","Başkasına gülme sana da gelebilir","Eğlenmek","Şaka yapmak"],d:1,a:"Başkalarının kötü durumuna gülme aynı şey sana da olabilir."}
{k:"Atasözleri",s:"Acele işe şeytan karışır ne anlatır?",o:["Şeytan kötüdür","Acele edilen iş hatalı olur","Hızlı koşmak","İşe gitmek"],d:1,a:"Acele yapılan işlerde hata yapılma olasılığı yüksektir."}
{k:"Atasözleri",s:"Komşu komşunun külüne muhtaçtır ne demektir?",o:["Kül toplamak","İnsanlar birbirine ihtiyaç duyar","Ateş yakmak","Temizlik yapmak"],d:1,a:"İnsanlar en küçük şeyde bile birbirine muhtaç olabilir."}
{k:"Atasözleri",s:"Ak akçe kara gün içindir ne demektir?",o:["Para biriktirmek","Zor günler için tasarruf et","Siyah beyaz","Harcamak"],d:1,a:"Zor zamanlar için önceden tasarruf yapılmalıdır."}
{k:"Atasözleri",s:"İşleyen demir ışıldar ne anlatır?",o:["Demir parlar","Çalışan insan gelişir","Metal işleme","Fabrika"],d:1,a:"Sürekli çalışan emek veren kişi gelişir ve başarılı olur."}
{k:"Atasözleri",s:"Bakarsan bağ olur bakmazsan dağ olur ne demektir?",o:["Bahçe işleri","İlgilenirsen güzel ilgilenmezsen bozulur","Dağa çıkmak","Üzüm toplamak"],d:1,a:"Bir işle ilgilenirsen verimli olur ihmal edersen bozulur."}
{k:"Atasözleri",s:"Ayağını yorganına göre uzat ne anlatır?",o:["Uyumak","Harcamayı gelirine göre yap","Yorgan almak","Uzanmak"],d:1,a:"İmkanların ölçüsünde harcama yap."}
{k:"Atasözleri",s:"Dost kara günde belli olur ne demektir?",o:["Kara günler kötüdür","Gerçek dost zor zamanda yanında olur","Arkadaş edinmek","Gece gezmek"],d:1,a:"Gerçek dostluk zor zamanlarda belli olur."}
{k:"Atasözleri",s:"Bal tutan parmağını yalar ne anlatır?",o:["Bal yemek","İşin başındaki kişi fayda sağlar","Temizlik","Parmak saymak"],d:1,a:"Değerli bir işin başında olan kişi bundan pay çıkarır."}
{k:"Atasözleri",s:"Atı alan Üsküdarı geçti ne demektir?",o:["At yarışı","Fırsatı kaçırmak","Üsküdara gitmek","Ata binmek"],d:1,a:"Fırsat kaçmıştır artık yapılacak bir şey kalmamıştır."}
{k:"Atasözleri",s:"Her yokuşun bir inişi vardır ne anlatır?",o:["Dağ tırmanışı","Zor günlerin ardından iyi günler gelir","Yol yapmak","Araba sürmek"],d:1,a:"Zorluklar sonsuza dek sürmez her sıkıntının bir sonu vardır."}
{k:"Atasözleri",s:"Mum dibine ışık vermez ne demektir?",o:["Mum söner","Yakındakilere faydası olmaz","Karanlık olur","Mum yakmak"],d:1,a:"Kişi en yakınındakilere yardım edemeyebilir."}
{k:"Atasözleri",s:"Sütten ağzı yanan yoğurdu üfleyerek yer ne anlatır?",o:["Yoğurt yemek","Kötü tecrübe yaşayan aşırı tedbirli olur","Süt içmek","Yemek yapmak"],d:1,a:"Daha önce kötü deneyim yaşayan kişi aşırı temkinli davranır."}
{k:"Atasözleri",s:"Tatlı dil yılanı deliğinden çıkarır ne anlatır?",o:["Yılan avlamak","Güzel konuşma her kapıyı açar","Şeker yemek","Delik kazmak"],d:1,a:"Güzel ve nazik konuşmayla en zor insanlar bile ikna edilebilir."}
{k:"Atasözleri",s:"Bugünün işini yarına bırakma ne demektir?",o:["Yarın tatil","İşlerini zamanında yap","Uyumak lazım","Erken kalkmak"],d:1,a:"İşleri ertelemeden zamanında bitirmek gerekir."}
{k:"Atasözleri",s:"El elden üstündür ne anlatır?",o:["El sıkmak","Her zaman daha iyisi vardır","Yardım etmek","Parmak saymak"],d:1,a:"Ne kadar iyi olursan ol senden daha iyisi mutlaka vardır."}
{k:"Atasözleri",s:"Körle yatan şaşı kalkar ne demektir?",o:["Uyumak","Kötü arkadaş kötü alışkanlık verir","Doktor olmak","Yardım etmek"],d:1,a:"Kötü çevreyle vakit geçiren kişi onlardan olumsuz etkilenir."}
{k:"Atasözleri",s:"Yazın başı pişenin kışın aşı pişer ne anlatır?",o:["Yemek pişirmek","Önceden hazırlık yapan sonra rahat eder","Mevsimler","Güneşte kalmak"],d:1,a:"Zamanında çalışıp hazırlık yapan kişi sonra sıkıntı çekmez."}
{k:"Atasözleri",s:"Minareyi çalan kılıfını hazırlar ne demektir?",o:["Minare yapmak","Büyük iş yapan önceden tedbir alır","Kılıf dikmek","Cami inşaatı"],d:1,a:"Büyük bir iş yapmaya kalkan kişi sonucuna da hazırlıklı olmalıdır."}
{k:"Atasözleri",s:"Bana dokunmayan yılan bin yaşasın ne anlatır?",o:["Yılanları sevmek","Bencilce düşünmek","Hayvanları korumak","Doğa sevgisi"],d:1,a:"Kendi başına gelmediği sürece başkalarının sorunuyla ilgilenmemek."}
{k:"Tarih",s:"Cumhuriyet ne zaman ilan edildi?",o:["1920","1921","1923","1924"],d:2,a:"Türkiye Cumhuriyeti 29 Ekim 1923 te ilan edilmiştir."}
{k:"Spor",s:"Hangi spor dalinda top kullanilmaz?",o:["Futbol","Basketbol","Yuzme","Voleybol"],d:2,a:"Yuzme sporunda top kullanilmaz."}
{k:"Spor",s:"Hentbolda bir takimda kac oyuncu sahadadır?",o:["5","6","7","8"],d:2,a:"Hentbolda her takımdan 7 oyuncu sahada bulunur."}
{k:"Spor",s:"Bisiklet yarisi hangi spor dalina girer?",o:["Atletizm","Cimnastik","Bisiklet","Yuzme"],d:2,a:"Bisiklet yarisi bisiklet sporu dalindadir."}
{k:"Spor",s:"Hangi spor dalinda buz uzerinde kayilir?",o:["Kayak","Buz pateni","Snowboard","Curling"],d:1,a:"Buz pateni buz uzerinde kayilarak yapilan bir spordur."}
{k:"Türkiye",s:"Truva Antik Kenti hangi ildedir?",o:["Balikesir","Canakkale","Bursa","Tekirdag"],d:1,a:"Truva Antik Kenti Canakkale ilinde yer alir."}
{k:"Türkiye",s:"Uzungol hangi ildedir?",o:["Rize","Artvin","Trabzon","Giresun"],d:2,a:"Uzungol Trabzon ilinin Caykara ilcesindedir."}
{k:"Türkiye",s:"Turkiye de en cok uretilen tarim urunu hangisidir?",o:["Bugday","Misir","Pamuk","Findik"],d:0,a:"Bugday Turkiye de en cok uretilen tarim urunlerinden biridir."}
{k:"Türkiye",s:"Anıtkabir hangi ildedir?",o:["Istanbul","Ankara","Izmir","Bursa"],d:1,a:"Ataturk un mozolesi Anitkabir Ankara dadır."}
{k:"Türkiye",s:"Turkiye nin en batisindaki il hangisidir?",o:["Izmir","Canakkale","Edirne","Mugla"],d:2,a:"Edirne Turkiye nin en batisindaki ildir."}
{k:"Türkiye",s:"Karain Magarasi hangi ildedir?",o:["Burdur","Isparta","Antalya","Mersin"],d:2,a:"Karain Magarasi Antalya dadır ve Anadolunun en eski yerlesimlerinden biridir."}
"""

_BY_QUESTIONS_ORTAOKUL = r"""
{k:"Tarih",s:"Malazgirt Muharebesi hangi yılda yapıldı?",o:["1054","1071","1176","1243"],d:1,a:"Malazgirt Muharebesi 1071 yılında Selçuklular ile Bizans arasında yapıldı."}
{k:"Tarih",s:"İstanbul hangi yılda fethedildi?",o:["1389","1402","1453","1517"],d:2,a:"İstanbul 1453 yılında Fatih Sultan Mehmet tarafından fethedildi."}
{k:"Tarih",s:"Osmanlı Devleti hangi yılda kuruldu?",o:["1243","1299","1326","1354"],d:1,a:"Osmanlı Devleti 1299 yılında kurulmuştur."}
{k:"Tarih",s:"Kurtuluş Savaşı hangi yıllar arasında yapıldı?",o:["1914-1918","1919-1922","1923-1925","1912-1913"],d:1,a:"Kurtuluş Savaşı 1919-1922 yılları arasında yapılmıştır."}
{k:"Tarih",s:"TBMM hangi yılda açıldı?",o:["1919","1920","1921","1923"],d:1,a:"TBMM 23 Nisan 1920 de Ankara da açılmıştır."}
{k:"Tarih",s:"Çanakkale Savaşı hangi yılda yapıldı?",o:["1912","1914","1915","1916"],d:2,a:"Çanakkale Savaşı 1915 yılında yapılmıştır."}
{k:"Tarih",s:"Birinci Dünya Savaşı kaç yılında başladı?",o:["1912","1914","1916","1918"],d:1,a:"Birinci Dünya Savaşı 1914 yılında başlamıştır."}
{k:"Tarih",s:"Halifelik hangi yılda kaldırıldı?",o:["1922","1923","1924","1925"],d:2,a:"Halifelik 3 Mart 1924 te kaldırılmıştır."}
{k:"Tarih",s:"Ankara Muharebesi hangi yılda yapıldı?",o:["1399","1402","1413","1421"],d:1,a:"Ankara Muharebesi 1402 de Timur ile Yıldırım Bayezid arasında yapıldı."}
{k:"Tarih",s:"Fatih Sultan Mehmet kaç yaşında tahta çıktı?",o:["12","15","19","21"],d:2,a:"Fatih Sultan Mehmet 19 yaşında tahta çıkmıştır."}
{k:"Tarih",s:"Sakarya Meydan Muharebesi hangi yılda yapıldı?",o:["1920","1921","1922","1923"],d:1,a:"Sakarya Meydan Muharebesi 1921 yılında yapılmıştır."}
{k:"Tarih",s:"Büyük Taarruz hangi yılda başladı?",o:["1920","1921","1922","1923"],d:2,a:"Büyük Taarruz 26 Ağustos 1922 de başlamıştır."}
{k:"Tarih",s:"Mudanya Ateşkes Antlaşması hangi yılda imzalandı?",o:["1920","1921","1922","1923"],d:2,a:"Mudanya Ateşkes Antlaşması 11 Ekim 1922 de imzalanmıştır."}
{k:"Tarih",s:"Lozan Antlaşması hangi yılda imzalandı?",o:["1921","1922","1923","1924"],d:2,a:"Lozan Antlaşması 24 Temmuz 1923 te imzalanmıştır."}
{k:"Tarih",s:"Sanayi Devrimi ilk hangi ülkede başladı?",o:["Fransa","Almanya","İngiltere","ABD"],d:2,a:"Sanayi Devrimi 18. yüzyılda İngiltere de başlamıştır."}
{k:"Tarih",s:"Fransız İhtilali hangi yılda oldu?",o:["1776","1789","1815","1830"],d:1,a:"Fransız İhtilali 1789 yılında gerçekleşmiştir."}
{k:"Tarih",s:"Kanuni Sultan Süleyman dönemi hangi yüzyıldadır?",o:["14. yy","15. yy","16. yy","17. yy"],d:2,a:"Kanuni Sultan Süleyman 16. yüzyılda hüküm sürmüştür."}
{k:"Tarih",s:"Selçuklu Devleti hangi savaşla Anadoluya girdi?",o:["Kosova","Malazgirt","Dandanakan","Miryokefalon"],d:1,a:"1071 Malazgirt Savaşı ile Anadolunun kapıları Türklere açılmıştır."}
{k:"Tarih",s:"İlk Türk devleti hangisidir?",o:["Selçuklu","Osmanlı","Göktürk","Uygur"],d:2,a:"Bilinen ilk Türk devleti Göktürk Devleti dir."}
{k:"Tarih",s:"İpek Yolu hangi kıtaları birleştiriyordu?",o:["Avrupa-Afrika","Asya-Avrupa","Amerika-Avrupa","Afrika-Asya"],d:1,a:"İpek Yolu Asya ile Avrupa arasında ticaret yoluydu."}
{k:"Tarih",s:"Tanzimat Fermanı hangi yılda ilan edildi?",o:["1826","1839","1856","1876"],d:1,a:"Tanzimat Fermanı 1839 yılında ilan edilmiştir."}
{k:"Tarih",s:"Mısır piramitlerini hangi uygarlık inşa etti?",o:["Romalılar","Yunanlılar","Mısırlılar","Persler"],d:2,a:"Mısır piramitleri Eski Mısır uygarlığı tarafından inşa edilmiştir."}
{k:"Tarih",s:"Kavimler Göçü ne zaman yaşandı?",o:["275","375","475","575"],d:1,a:"Kavimler Göçü 375 yılında Hunların batıya göçüyle başlamıştır."}
{k:"Tarih",s:"Roma İmparatorluğu hangi yılda ikiye ayrıldı?",o:["295","395","476","527"],d:1,a:"Roma İmparatorluğu 395 yılında Doğu ve Batı olarak ikiye ayrılmıştır."}
{k:"Tarih",s:"Atatürk hangi şehirde doğdu?",o:["İstanbul","Ankara","Selanik","İzmir"],d:2,a:"Mustafa Kemal Atatürk 1881 de Selanik te doğmuştur."}
{k:"Tarih",s:"İzmir hangi tarihte düşman işgalinden kurtuldu?",o:["9 Eylül 1922","30 Ağustos 1922","29 Ekim 1923","23 Nisan 1920"],d:0,a:"İzmir 9 Eylül 1922 de düşman işgalinden kurtulmuştur."}
{k:"Tarih",s:"Miryokefalon Muharebesi hangi yılda yapıldı?",o:["1071","1176","1243","1299"],d:1,a:"Miryokefalon Muharebesi 1176 yılında Türkiye Selçukluları ile Bizans arasında yapıldı."}
{k:"Tarih",s:"Kösedağ Muharebesi hangi yılda yapıldı?",o:["1176","1230","1243","1299"],d:2,a:"Kösedağ Muharebesi 1243 yılında Moğollar ile Selçuklular arasında yapıldı."}
{k:"Tarih",s:"Medeni Kanun hangi yılda kabul edildi?",o:["1924","1925","1926","1928"],d:2,a:"Türk Medeni Kanunu 1926 yılında kabul edilmiştir."}
{k:"Tarih",s:"Harf İnkılabı hangi yılda yapıldı?",o:["1924","1926","1928","1930"],d:2,a:"Latin harflerine geçiş 1928 yılında gerçekleşmiştir."}
{k:"Tarih",s:"Osmanlı Devleti hangi yılda sona erdi?",o:["1918","1920","1922","1924"],d:2,a:"Osmanlı saltanatı 1 Kasım 1922 de kaldırılmıştır."}
{k:"Tarih",s:"Soğuk Savaş hangi yıllar arasında yaşandı?",o:["1939-1945","1945-1991","1950-1980","1960-2000"],d:1,a:"Soğuk Savaş 1945-1991 yılları arasında ABD ve SSCB arasında yaşanmıştır."}
{k:"Tarih",s:"İkinci Dünya Savaşı kaç yılında bitti?",o:["1943","1944","1945","1946"],d:2,a:"İkinci Dünya Savaşı 1945 yılında sona ermiştir."}
{k:"Tarih",s:"Preveze Deniz Muharebesi hangi yılda yapıldı?",o:["1522","1538","1571","1580"],d:1,a:"Preveze Deniz Muharebesi 1538 yılında Barbaros Hayrettin Paşa komutasında kazanıldı."}
{k:"Tarih",s:"Orhun Yazıtları hangi Türk devletine aittir?",o:["Hunlar","Göktürkler","Uygurlar","Selçuklular"],d:1,a:"Orhun Yazıtları Göktürk Devletine ait en eski Türkçe metinlerdir."}
{k:"Tarih",s:"Viyana Kuşatması hangi yılda yapıldı?",o:["1526","1529","1571","1683"],d:3,a:"İkinci Viyana Kuşatması 1683 yılında yapılmıştır."}
{k:"Tarih",s:"Mohaç Muharebesi hangi yılda yapıldı?",o:["1517","1522","1526","1538"],d:2,a:"Mohaç Muharebesi 1526 yılında Osmanlı ile Macaristan arasında yapıldı."}
{k:"Tarih",s:"Meşrutiyet ilk hangi yılda ilan edildi?",o:["1856","1876","1908","1918"],d:1,a:"Birinci Meşrutiyet 1876 yılında ilan edilmiştir."}
{k:"Tarih",s:"İstiklal Marşı hangi yılda kabul edildi?",o:["1920","1921","1922","1923"],d:1,a:"İstiklal Marşı 12 Mart 1921 de kabul edilmiştir."}
{k:"Tarih",s:"Türk kadınlarına seçme seçilme hakkı hangi yılda verildi?",o:["1930","1934","1935","1938"],d:1,a:"Türk kadınlarına seçme ve seçilme hakkı 1934 yılında verilmiştir."}
{k:"Tarih",s:"Atatürk hangi yılda vefat etti?",o:["1935","1936","1937","1938"],d:3,a:"Atatürk 10 Kasım 1938 de vefat etmiştir."}
{k:"Tarih",s:"İlk olimpiyat oyunları nerede yapıldı?",o:["Roma","Atina","İskenderiye","Sparta"],d:1,a:"İlk antik olimpiyat oyunları Yunanistan da yapılmıştır."}
{k:"Tarih",s:"Amerika kıtasını keşfeden denizci kimdir?",o:["Vasco da Gama","Magellan","Kristof Kolomb","Marco Polo"],d:2,a:"Kristof Kolomb 1492 de Amerika kıtasına ulaşmıştır."}
{k:"Tarih",s:"İstanbul Boğazı ilk kez hangi köprüyle bağlandı?",o:["Fatih Sultan Mehmet","Boğaziçi","Yavuz Sultan Selim","Marmaray"],d:1,a:"Boğaziçi Köprüsü 1973 te açılarak İstanbul un iki yakasını bağlamıştır."}
{k:"Tarih",s:"Dünya tarihinde matbaayı kim buldu?",o:["Edison","Newton","Gutenberg","Da Vinci"],d:2,a:"Modern matbaayı Johannes Gutenberg 15. yüzyılda icat etmiştir."}
{k:"Tarih",s:"Amasya Genelgesi hangi yılda yayınlandı?",o:["1919","1920","1921","1922"],d:0,a:"Amasya Genelgesi 22 Haziran 1919 da yayınlanmıştır."}
{k:"Tarih",s:"Erzurum Kongresi hangi yılda yapıldı?",o:["1918","1919","1920","1921"],d:1,a:"Erzurum Kongresi 23 Temmuz-7 Ağustos 1919 tarihleri arasında yapıldı."}
{k:"Tarih",s:"Sivas Kongresi hangi yılda yapıldı?",o:["1918","1919","1920","1921"],d:1,a:"Sivas Kongresi 4-11 Eylül 1919 tarihleri arasında yapıldı."}
{k:"Tarih",s:"Mondros Ateşkes Antlaşması hangi yılda imzalandı?",o:["1916","1917","1918","1919"],d:2,a:"Mondros Ateşkes Antlaşması 30 Ekim 1918 de imzalanmıştır."}
{k:"Tarih",s:"Sevr Antlaşması hangi yılda imzalandı?",o:["1919","1920","1921","1922"],d:1,a:"Sevr Antlaşması 10 Ağustos 1920 de imzalanmış ancak uygulanmamıştır."}
{k:"Coğrafya",s:"Türkiye nin en uzun nehri hangisidir?",o:["Fırat","Kızılırmak","Dicle","Sakarya"],d:1,a:"Kızılırmak 1355 km ile Türkiye nin en uzun nehridir."}
{k:"Coğrafya",s:"Dünyanın en uzun nehri hangisidir?",o:["Amazon","Nil","Mississippi","Yangtze"],d:1,a:"Nil Nehri yaklaşık 6650 km ile dünyanın en uzun nehridir."}
{k:"Coğrafya",s:"Türkiye hangi iki kıtada yer alır?",o:["Avrupa-Afrika","Asya-Afrika","Avrupa-Asya","Asya-Amerika"],d:2,a:"Türkiye hem Avrupa hem Asya kıtasında yer alır."}
{k:"Coğrafya",s:"Dünyanın en yüksek dağı hangisidir?",o:["K2","Kangchenjunga","Everest","Lhotse"],d:2,a:"Everest Dağı 8848 m ile dünyanın en yüksek dağıdır."}
{k:"Coğrafya",s:"Karadeniz ile Akdeniz hangi boğazlarla bağlanır?",o:["Cebelitarık","Hürmüz","İstanbul-Çanakkale","Malakka"],d:2,a:"İstanbul ve Çanakkale Boğazları Karadeniz ile Akdeniz i Marmara üzerinden bağlar."}
{k:"Coğrafya",s:"Ekvator çizgisi neyi ikiye böler?",o:["Kıtaları","Dünyayı kuzey-güney","Okyanusları","Atmosferi"],d:1,a:"Ekvator dünyayı kuzey ve güney yarımküre olarak ikiye böler."}
{k:"Coğrafya",s:"Hangi ülke hem Avrupa hem Asya da yer alır?",o:["Mısır","Yunanistan","Türkiye","İran"],d:2,a:"Türkiye coğrafi olarak hem Avrupa hem Asya kıtasında yer alır."}
{k:"Coğrafya",s:"Sahra Çölü hangi kıtadadır?",o:["Asya","Avrupa","Afrika","Avustralya"],d:2,a:"Sahra Çölü Afrika kıtasının kuzeyinde yer alır."}
{k:"Coğrafya",s:"Dünyanın en büyük adasını hangi ülke yönetir?",o:["ABD","Kanada","Danimarka","İngiltere"],d:2,a:"Grönland dünyanın en büyük adasıdır ve Danimarka ya bağlıdır."}
{k:"Coğrafya",s:"Akdeniz Bölgesinin en önemli tarım ürünü hangisidir?",o:["Çay","Fındık","Narenciye","Buğday"],d:2,a:"Akdeniz Bölgesinde narenciye (turunçgiller) en önemli tarım ürünüdür."}
{k:"Coğrafya",s:"Karadeniz Bölgesinin en önemli tarım ürünü hangisidir?",o:["Pamuk","Çay ve fındık","Zeytin","Üzüm"],d:1,a:"Karadeniz Bölgesinde çay ve fındık en önemli tarım ürünleridir."}
{k:"Coğrafya",s:"İç Anadolu Bölgesinin iklimi nasıldır?",o:["Ilıman","Karasal","Tropikal","Akdeniz"],d:1,a:"İç Anadolu Bölgesinde karasal iklim hakimdir."}
{k:"Coğrafya",s:"Güneydoğu Anadolu nun en önemli barajı hangisidir?",o:["Keban","Atatürk Barajı","Hirfanlı","Oymapınar"],d:1,a:"Atatürk Barajı Güneydoğu Anadolu Projesinin en büyük barajıdır."}
{k:"Coğrafya",s:"Himalaya Dağları hangi iki ülke arasındadır?",o:["Çin-Japonya","Nepal-Hindistan","Çin-Rusya","Pakistan-İran"],d:1,a:"Himalayalar Nepal ve Hindistan arasında (Çin ile de sınır) yer alır."}
{k:"Coğrafya",s:"Marmara Denizi hangi boğazlarla açık denize bağlanır?",o:["Süveyş-Panama","İstanbul-Çanakkale","Hürmüz-Malakka","Cebelitarık-Bab"],d:1,a:"Marmara Denizi İstanbul ve Çanakkale boğazlarıyla bağlanır."}
{k:"Coğrafya",s:"Tuz Gölü hangi bölgemizdedir?",o:["Marmara","Akdeniz","İç Anadolu","Ege"],d:2,a:"Tuz Gölü İç Anadolu Bölgesinde yer alır."}
{k:"Coğrafya",s:"Doğu Anadolu Bölgesinin en belirgin özelliği nedir?",o:["Denize kıyısı var","Yüksek ve sert iklim","Ilıman hava","Tropikal ormanlar"],d:1,a:"Doğu Anadolu Bölgesi yüksek rakımlı ve sert karasal iklime sahiptir."}
{k:"Coğrafya",s:"Panama Kanalı hangi iki okyanusu birleştirir?",o:["Atlas-Hint","Büyük Okyanus-Atlas","Hint-Büyük Okyanus","Atlas-Kuzey Buz"],d:1,a:"Panama Kanalı Büyük Okyanus ile Atlas Okyanusunu birleştirir."}
{k:"Coğrafya",s:"Süveyş Kanalı hangi iki denizi birleştirir?",o:["Akdeniz-Kızıldeniz","Karadeniz-Akdeniz","Hazar-Karadeniz","Atlas-Hint"],d:0,a:"Süveyş Kanalı Akdeniz ile Kızıldenizi birleştirir."}
{k:"Coğrafya",s:"Dünyada en çok nüfusa sahip ülke hangisidir?",o:["ABD","Hindistan","Çin","Brezilya"],d:1,a:"Hindistan dünyanın en kalabalık ülkesidir."}
{k:"Coğrafya",s:"Güneş en son hangi yönde batar?",o:["Doğu","Batı","Kuzey","Güney"],d:1,a:"Güneş batıda batar."}
{k:"Coğrafya",s:"Yüzölçümü en büyük ülke hangisidir?",o:["Kanada","ABD","Çin","Rusya"],d:3,a:"Rusya dünyanın yüzölçümü en büyük ülkesidir."}
{k:"Coğrafya",s:"Sıcak ve soğuk su akıntılarının karşılaştığı yerde ne oluşur?",o:["Deprem","Volkan","Balıkçılık alanı","Çöl"],d:2,a:"Sıcak ve soğuk su akıntılarının buluşma noktaları zengin balıkçılık alanlarıdır."}
{k:"Coğrafya",s:"Ege Bölgesinde kıyılar neden girintili çıkıntılıdır?",o:["Rüzgardan","Dağların denize dik uzanması","Depremden","Volkanlardan"],d:1,a:"Ege de dağlar denize dik uzandığından kıyılar girintili çıkıntılıdır."}
{k:"Coğrafya",s:"Volkanik göl nasıl oluşur?",o:["Nehir birikimiyle","Krater çukurunda su birikmesiyle","Buzul erozyonuyla","Heyelanla"],d:1,a:"Volkan krateri veya kalderası içinde su birikmesiyle volkanik göl oluşur."}
{k:"Coğrafya",s:"Türkiye nin en güneydeki ili hangisidir?",o:["Antalya","Mersin","Hatay","Şanlıurfa"],d:2,a:"Hatay Türkiye nin en güneydeki ilidir."}
{k:"Coğrafya",s:"Meriç Nehri hangi ülkelerin sınırını oluşturur?",o:["Türkiye-Suriye","Türkiye-Irak","Türkiye-Yunanistan","Türkiye-İran"],d:2,a:"Meriç Nehri Türkiye ile Yunanistan arasında doğal sınır oluşturur."}
{k:"Coğrafya",s:"Rüzgar erozyonu en çok hangi bölgede görülür?",o:["Karadeniz","Akdeniz","İç Anadolu","Marmara"],d:2,a:"İç Anadolu da bitki örtüsünün az olması nedeniyle rüzgar erozyonu fazladır."}
{k:"Coğrafya",s:"Karstik arazi nerelerde görülür?",o:["Volkanik bölge","Kireçtaşı bölge","Granit bölge","Kumtaşı bölge"],d:1,a:"Karstik arazi kireçtaşının erimesiyle oluşan bölgelerde görülür."}
{k:"Coğrafya",s:"Deprem kuşağı Türkiye nin hangi bölgesinde en aktiftir?",o:["Karadeniz","Güneydoğu","Kuzey Anadolu Fay Hattı","Doğu Anadolu"],d:2,a:"Kuzey Anadolu Fay Hattı Türkiye nin en aktif deprem kuşağıdır."}
{k:"Bilim",s:"Periyodik tabloda kaç element vardır?",o:["92","108","118","126"],d:2,a:"Periyodik tabloda şu an 118 element bulunmaktadır."}
{k:"Bilim",s:"Fotosentez sırasında bitkiler ne üretir?",o:["Karbondioksit","Oksijen","Azot","Helyum"],d:1,a:"Bitkiler fotosentez sırasında oksijen üretir."}
{k:"Bilim",s:"DNA nın açılımı nedir?",o:["Direkt Nükleer Asit","Deoksiribo Nükleik Asit","Düzenli Nöral Ağ","Doğal Nitrat Asit"],d:1,a:"DNA Deoksiribonükleik Asit anlamına gelir."}
{k:"Bilim",s:"İnsan vücudunda kaç kemik vardır?",o:["186","206","226","256"],d:1,a:"Yetişkin insan vücudunda 206 kemik bulunur."}
{k:"Bilim",s:"Ses boşlukta yayılabilir mi?",o:["Evet","Hayır","Bazen","Sıcakta evet"],d:1,a:"Ses maddesel ortam gerektirir, boşlukta yayılamaz."}
{k:"Bilim",s:"Güneş hangi tür yıldızdır?",o:["Kırmızı cüce","Sarı cüce","Mavi dev","Beyaz cüce"],d:1,a:"Güneş bir sarı cüce yıldızdır."}
{k:"Bilim",s:"Atomun çekirdeğinde ne bulunur?",o:["Elektron","Proton ve nötron","Sadece proton","Foton"],d:1,a:"Atom çekirdeğinde proton ve nötron bulunur."}
{k:"Bilim",s:"Hangi element sembolü Fe dir?",o:["Flor","Fosfor","Demir","Fermiyum"],d:2,a:"Fe demir elementinin sembolüdür (Latince Ferrum)."}
{k:"Bilim",s:"Suyun kaynama noktası kaç derecedir?",o:["80","90","100","120"],d:2,a:"Saf su deniz seviyesinde 100 derecede kaynar."}
{k:"Bilim",s:"Hangi gezegen halkaları ile ünlüdür?",o:["Jüpiter","Mars","Satürn","Uranüs"],d:2,a:"Satürn belirgin halka sistemiyle ünlüdür."}
{k:"Bilim",s:"Yer kabuğunda en çok bulunan element hangisidir?",o:["Demir","Silisyum","Oksijen","Alüminyum"],d:2,a:"Oksijen yer kabuğunda en çok bulunan elementtir."}
{k:"Bilim",s:"Işık hızı yaklaşık kaç km/s dir?",o:["100000","200000","300000","400000"],d:2,a:"Işık hızı yaklaşık 300000 km/s dir."}
{k:"Bilim",s:"İnsan beyninin ağırlığı yaklaşık kaç gramdır?",o:["800","1000","1400","2000"],d:2,a:"Yetişkin insan beyni yaklaşık 1400 gram ağırlığındadır."}
{k:"Bilim",s:"PH değeri 7 olan çözelti nasıldır?",o:["Asidik","Bazik","Nötr","Tuzlu"],d:2,a:"PH 7 nötr çözeltiyi ifade eder."}
{k:"Bilim",s:"Dünya Güneşin etrafını kaç günde dolanır?",o:["300","325","365","400"],d:2,a:"Dünya Güneşin etrafını yaklaşık 365 günde dolanır."}
{k:"Bilim",s:"Newton un birinci hareket yasası neyi tanımlar?",o:["Kuvvet","Eylemsizlik","İvme","Enerji"],d:1,a:"Newton un birinci yasası eylemsizlik yasasıdır."}
{k:"Bilim",s:"Elektrik akımının birimi nedir?",o:["Volt","Watt","Amper","Ohm"],d:2,a:"Elektrik akımının birimi amperdir."}
{k:"Bilim",s:"Hangi vitamin eksikliği gece körlüğüne yol açar?",o:["B vitamini","C vitamini","A vitamini","D vitamini"],d:2,a:"A vitamini eksikliği gece körlüğüne neden olabilir."}
{k:"Bilim",s:"Kırmızı kan hücreleri ne taşır?",o:["Su","Oksijen","Vitamin","Protein"],d:1,a:"Kırmızı kan hücreleri hemoglobin ile oksijen taşır."}
{k:"Bilim",s:"Ses dalgaları hangi tür dalgadır?",o:["Enine","Boyuna","Elektromanyetik","Işık"],d:1,a:"Ses dalgaları boyuna (longitudinal) dalgalardır."}
{k:"Bilim",s:"Doğal uydu olan tek gezegenimiz hangisidir?",o:["Mars","Dünya","Venüs","Merkür"],d:1,a:"Dünya nın tek doğal uydusu Ay dır."}
{k:"Bilim",s:"Karbondioksit gazının formülü nedir?",o:["CO","CO2","C2O","C2O2"],d:1,a:"Karbondioksitin kimyasal formülü CO2 dir."}
{k:"Bilim",s:"Elektrik direncinin birimi nedir?",o:["Amper","Volt","Ohm","Watt"],d:2,a:"Elektrik direncinin birimi ohm dur."}
{k:"Bilim",s:"Ağır cisimlerin düşme hızı hafiflerden farklı mıdır?",o:["Evet ağırlar hızlı","Hayır aynı hızda","Hafifler hızlı","Ortama bağlı"],d:1,a:"Hava direnci ihmal edildiğinde tüm cisimler aynı hızda düşer."}
{k:"Bilim",s:"Mars gezegeninin rengi nedir?",o:["Mavi","Yeşil","Kırmızı","Sarı"],d:2,a:"Mars yüzeyindeki demir oksit nedeniyle kırmızımsı görünür."}
{k:"Bilim",s:"Hangi bilim insanı görelilik kuramını ortaya attı?",o:["Newton","Galileo","Einstein","Hawking"],d:2,a:"Albert Einstein görelilik kuramını ortaya atmıştır."}
{k:"Bilim",s:"İnsan vücudunda en büyük organ hangisidir?",o:["Karaciğer","Kalp","Deri","Beyin"],d:2,a:"Deri insan vücudunun en büyük organıdır."}
{k:"Bilim",s:"Güneş enerjisini hangi süreçle üretir?",o:["Fisyon","Füzyon","Yanma","Kimyasal tepkime"],d:1,a:"Güneş nükleer füzyon ile enerji üretir."}
{k:"Bilim",s:"Oksijen atomunun atom numarası kaçtır?",o:["6","8","10","12"],d:1,a:"Oksijenin atom numarası 8 dir."}
{k:"Bilim",s:"Hangi cihaz sıcaklığı ölçer?",o:["Barometre","Termometre","Higrometre","Voltmetre"],d:1,a:"Termometre sıcaklık ölçen cihazdır."}
{k:"Doğa",s:"Fotosentez için gerekli üç temel madde nedir?",o:["Su toprak hava","Güneş su CO2","Oksijen su toprak","Rüzgar su güneş"],d:1,a:"Fotosentez için güneş ışığı su ve karbondioksit gereklidir."}
{k:"Doğa",s:"Dünyanın en büyük yağmur ormanı hangisidir?",o:["Kongo","Amazon","Borneo","Daintree"],d:1,a:"Amazon yağmur ormanları dünyanın en büyük yağmur ormanıdır."}
{k:"Doğa",s:"Hangi hayvan en hızlı koşar?",o:["Aslan","Çita","At","Geyik"],d:1,a:"Çita saatte 120 km hıza ulaşabilen en hızlı kara hayvanıdır."}
{k:"Doğa",s:"Ekosistem nedir?",o:["Sadece bitkiler","Canlılar ve çevreleri arası ilişki","Sadece hayvanlar","Hava durumu"],d:1,a:"Ekosistem canlılar ve cansız çevreleri arasındaki etkileşim sistemidir."}
{k:"Doğa",s:"Hangi gaz sera etkisine en çok katkıda bulunur?",o:["Oksijen","Azot","Karbondioksit","Helyum"],d:2,a:"Karbondioksit sera etkisine en çok katkıda bulunan gazlardan biridir."}
{k:"Doğa",s:"Suda yaşayan memelilere ne denir?",o:["Balıklar","Amfibiler","Deniz memelileri","Sürüngenler"],d:2,a:"Yunus balina gibi suda yaşayan memelilere deniz memelileri denir."}
{k:"Doğa",s:"Hangi hayvan ultrason kullanarak yön bulur?",o:["Kartal","Yarasa","Güvercin","Baykuş"],d:1,a:"Yarasalar ekolokasyon ile ultrason kullanarak yön bulur."}
{k:"Doğa",s:"Besin zincirinde üretici canlılar kimlerdir?",o:["Hayvanlar","Mantarlar","Bitkiler","Bakteriler"],d:2,a:"Bitkiler fotosentez yaparak besin zincirinin üretici canlılarıdır."}
{k:"Doğa",s:"Karbon döngüsü nedir?",o:["Karbonun atmosfer toprak ve canlılar arasında dolaşması","Karbonun yok olması","Sadece yanma","Sadece solunum"],d:0,a:"Karbon döngüsü karbonun atmosfer biyosfer ve litosfer arasında dolaşmasıdır."}
{k:"Doğa",s:"Ozon tabakası ne işe yarar?",o:["Yağmur yağdırır","Zararlı UV ışınlarını süzer","Sıcaklığı artırır","Rüzgar oluşturur"],d:1,a:"Ozon tabakası güneşten gelen zararlı UV ışınlarını süzer."}
{k:"Doğa",s:"Göç eden kuşlar neden göç eder?",o:["Can sıkıntısı","Besin ve iklim koşulları","Merak","Egzersiz"],d:1,a:"Kuşlar besin bulmak ve uygun iklim koşulları için göç eder."}
{k:"Doğa",s:"Hangi hayvan en uzun ömre sahiptir?",o:["Fil","Kaplumbağa","Kartal","Timsah"],d:1,a:"Bazı kaplumbağa türleri 200 yıldan fazla yaşayabilir."}
{k:"Doğa",s:"Toprak erozyonunu en çok ne önler?",o:["Beton","Bitki örtüsü","Kum","Taşlar"],d:1,a:"Bitki örtüsü kökleriyle toprağı tutarak erozyonu önler."}
{k:"Doğa",s:"Dünyanın en büyük canlısı hangisidir?",o:["Fil","Köpek balığı","Mavi balina","Zürafa"],d:2,a:"Mavi balina yaklaşık 30 metre uzunluğuyla en büyük canlıdır."}
{k:"Doğa",s:"Kamuflaj yapan hayvan hangisidir?",o:["Aslan","Bukalemun","Tavşan","Leylek"],d:1,a:"Bukalemun rengini değiştirerek kamuflaj yapar."}
{k:"Doğa",s:"Hangi hayvan kış uykusuna yatar?",o:["Tavşan","Ayı","Geyik","Kartal"],d:1,a:"Ayılar kış aylarında kış uykusuna (hibernasyon) yatar."}
{k:"Doğa",s:"Yenilenebilir enerji kaynağı hangisidir?",o:["Kömür","Petrol","Güneş","Doğalgaz"],d:2,a:"Güneş enerjisi yenilenebilir bir enerji kaynağıdır."}
{k:"Doğa",s:"Deniz yıldızının kaç kolu vardır?",o:["3","4","5","6"],d:2,a:"Deniz yıldızlarının genellikle 5 kolu vardır."}
{k:"Doğa",s:"Hangi böcek en güçlü böcektir?",o:["Karınca","Bok böceği","Arı","Çekirge"],d:1,a:"Bok böceği kendi ağırlığının 1000 katını çekebilir."}
{k:"Doğa",s:"Biyolojik çeşitlilik ne demektir?",o:["Tek tür bitki","Canlı tür zenginliği","Sadece orman","Deniz canlıları"],d:1,a:"Biyolojik çeşitlilik bir bölgedeki canlı tür zenginliğidir."}
{k:"Doğa",s:"Su döngüsünün aşamaları nelerdir?",o:["Sadece yağış","Buharlaşma yoğunlaşma yağış","Sadece buharlaşma","Sadece donma"],d:1,a:"Su döngüsü buharlaşma yoğunlaşma ve yağış aşamalarından oluşur."}
{k:"Doğa",s:"Hangi ağaç yapraklarını kışın dökmez?",o:["Meşe","Kayın","Çam","Akasya"],d:2,a:"Çam ağacı her dem yeşil iğne yapraklı bir ağaçtır."}
{k:"Doğa",s:"Nesli tükenmekte olan hayvanlara ne denir?",o:["Evcil","Yabani","Tehlike altındaki türler","Göçmen"],d:2,a:"Nesli tükenme tehlikesinde olan canlılara tehlike altındaki türler denir."}
{k:"Doğa",s:"Hangi kuş geriye doğru uçabilir?",o:["Serçe","Kartal","Sinek kuşu","Papağan"],d:2,a:"Sinek kuşu geriye doğru uçabilen tek kuş türüdür."}
{k:"Doğa",s:"Mercan resifleri hangi sularda oluşur?",o:["Soğuk ve derin","Sıcak ve sığ","Tatlı su","Buz altı"],d:1,a:"Mercan resifleri sıcak ve sığ tropikal sularda oluşur."}
{k:"Doğa",s:"Ahtapotun kaç kolu vardır?",o:["6","8","10","12"],d:1,a:"Ahtapotların 8 kolu bulunur."}
{k:"Doğa",s:"Atmosferde en çok bulunan gaz hangisidir?",o:["Oksijen","Karbondioksit","Azot","Helyum"],d:2,a:"Atmosferin yaklaşık yüzde 78 i azot gazından oluşur."}
{k:"Doğa",s:"Hangi hayvan sütüyle yavrularını besler?",o:["Timsah","Yunus","Kertenkele","Kurbağa"],d:1,a:"Yunus bir memeli olduğu için yavrularını sütle besler."}
{k:"Doğa",s:"Ağaçların yaşı nasıl hesaplanır?",o:["Boyuna bakılır","Halka sayılır","Yaprak sayılır","Kök ölçülür"],d:1,a:"Ağaçların yaşı gövde kesitindeki yıllık halkalar sayılarak hesaplanır."}
{k:"Doğa",s:"Küresel ısınmanın en büyük nedeni nedir?",o:["Volkanlar","Sera gazı emisyonları","Güneş patlamaları","Depremler"],d:1,a:"İnsan kaynaklı sera gazı emisyonları küresel ısınmanın en büyük nedenidir."}
{k:"Başkentler",s:"İspanya nın başkenti neresidir?",o:["Barselona","Madrid","Sevilla","Valencia"],d:1,a:"Madrid İspanya nın başkentidir."}
{k:"Başkentler",s:"Çin in başkenti neresidir?",o:["Şanghay","Hong Kong","Pekin","Guangzhou"],d:2,a:"Pekin Çin in başkentidir."}
{k:"Başkentler",s:"Meksika nın başkenti neresidir?",o:["Cancun","Guadalajara","Mexico City","Monterrey"],d:2,a:"Mexico City Meksika nın başkentidir."}
{k:"Başkentler",s:"İsviçre nin başkenti neresidir?",o:["Zürih","Cenevre","Bern","Basel"],d:2,a:"Bern İsviçre nin başkentidir."}
{k:"Başkentler",s:"Mısır ın başkenti neresidir?",o:["İskenderiye","Kahire","Luxor","Aswan"],d:1,a:"Kahire Mısır ın başkentidir."}
{k:"Başkentler",s:"Yeni Zelanda nın başkenti neresidir?",o:["Auckland","Wellington","Christchurch","Hamilton"],d:1,a:"Wellington Yeni Zelanda nın başkentidir."}
{k:"Başkentler",s:"Polonya nın başkenti neresidir?",o:["Krakow","Varşova","Gdansk","Poznan"],d:1,a:"Varşova Polonya nın başkentidir."}
{k:"Başkentler",s:"Portekiz in başkenti neresidir?",o:["Porto","Lizbon","Faro","Coimbra"],d:1,a:"Lizbon Portekiz in başkentidir."}
{k:"Başkentler",s:"Küba nın başkenti neresidir?",o:["Santiago","Havana","Trinidad","Varadero"],d:1,a:"Havana Küba nın başkentidir."}
{k:"Başkentler",s:"Kenya nın başkenti neresidir?",o:["Nairobi","Mombasa","Kisumu","Nakuru"],d:0,a:"Nairobi Kenya nın başkentidir."}
{k:"Başkentler",s:"Peru nun başkenti neresidir?",o:["Cusco","Lima","Arequipa","Trujillo"],d:1,a:"Lima Peru nun başkentidir."}
{k:"Başkentler",s:"Yunanistan ın başkenti neresidir?",o:["Selanik","Atina","Girit","Rodos"],d:1,a:"Atina Yunanistan ın başkentidir."}
{k:"Başkentler",s:"Macaristan ın başkenti neresidir?",o:["Prag","Viyana","Budapeşte","Bratislava"],d:2,a:"Budapeşte Macaristan ın başkentidir."}
{k:"Başkentler",s:"Çek Cumhuriyeti nin başkenti neresidir?",o:["Budapeşte","Viyana","Prag","Bratislava"],d:2,a:"Prag Çek Cumhuriyeti nin başkentidir."}
{k:"Başkentler",s:"İsveç in başkenti neresidir?",o:["Oslo","Stockholm","Helsinki","Kopenhag"],d:1,a:"Stockholm İsveç in başkentidir."}
{k:"Başkentler",s:"Finlandiya nın başkenti neresidir?",o:["Oslo","Stockholm","Helsinki","Tallinn"],d:2,a:"Helsinki Finlandiya nın başkentidir."}
{k:"Başkentler",s:"Danimarka nın başkenti neresidir?",o:["Oslo","Stockholm","Helsinki","Kopenhag"],d:3,a:"Kopenhag Danimarka nın başkentidir."}
{k:"Başkentler",s:"Avusturya nın başkenti neresidir?",o:["Salzburg","Viyana","Graz","Innsbruck"],d:1,a:"Viyana Avusturya nın başkentidir."}
{k:"Başkentler",s:"Romanya nın başkenti neresidir?",o:["Sofya","Bükreş","Belgrat","Tiran"],d:1,a:"Bükreş Romanya nın başkentidir."}
{k:"Başkentler",s:"Gürcistan ın başkenti neresidir?",o:["Bakü","Erivan","Tiflis","Batum"],d:2,a:"Tiflis Gürcistan ın başkentidir."}
{k:"Başkentler",s:"Azerbaycan ın başkenti neresidir?",o:["Bakü","Tiflis","Erivan","Tahran"],d:0,a:"Bakü Azerbaycan ın başkentidir."}
{k:"Başkentler",s:"Kolombiya nın başkenti neresidir?",o:["Medellin","Bogota","Cali","Cartagena"],d:1,a:"Bogota Kolombiya nın başkentidir."}
{k:"Başkentler",s:"Nijerya nın başkenti neresidir?",o:["Lagos","Abuja","Kano","Ibadan"],d:1,a:"Abuja Nijerya nın başkentidir."}
{k:"Başkentler",s:"Ukrayna nın başkenti neresidir?",o:["Odessa","Kiev","Lviv","Harkov"],d:1,a:"Kiev Ukrayna nın başkentidir."}
{k:"Başkentler",s:"Irak ın başkenti neresidir?",o:["Basra","Erbil","Bağdat","Musul"],d:2,a:"Bağdat Irak ın başkentidir."}
{k:"Başkentler",s:"İran ın başkenti neresidir?",o:["İsfahan","Tahran","Şiraz","Tebriz"],d:1,a:"Tahran İran ın başkentidir."}
{k:"Başkentler",s:"Endonezya nın başkenti neresidir?",o:["Bali","Surabaya","Jakarta","Medan"],d:2,a:"Jakarta Endonezya nın başkentidir."}
{k:"Başkentler",s:"Filipinler in başkenti neresidir?",o:["Manila","Cebu","Davao","Quezon"],d:0,a:"Manila Filipinler in başkentidir."}
{k:"Başkentler",s:"Vietnam ın başkenti neresidir?",o:["Ho Chi Minh","Hanoi","Da Nang","Hue"],d:1,a:"Hanoi Vietnam ın başkentidir."}
{k:"Başkentler",s:"Pakistan ın başkenti neresidir?",o:["Karaçi","Lahor","İslamabad","Peşaver"],d:2,a:"İslamabad Pakistan ın başkentidir."}
{k:"Türkiye",s:"Türkiye nin en uzun nehri hangisidir?",o:["Fırat","Kızılırmak","Dicle","Sakarya"],d:1,a:"Kızılırmak 1355 km ile en uzun nehirdir."}
{k:"Türkiye",s:"Kapadokya hangi ilde yer alır?",o:["Kayseri","Nevşehir","Aksaray","Konya"],d:1,a:"Kapadokya ağırlıklı olarak Nevşehir ilindedir."}
{k:"Türkiye",s:"Peri Bacaları hangi bölgede bulunur?",o:["Ege","Akdeniz","İç Anadolu","Karadeniz"],d:2,a:"Peri Bacaları Kapadokya İç Anadolu Bölgesinde bulunur."}
{k:"Türkiye",s:"Türkiye nin en derin gölü hangisidir?",o:["Tuz Gölü","Van Gölü","Tortum Gölü","Hazar Gölü"],d:3,a:"Hazar Gölü 200 m derinliğiyle Türkiye nin en derin gölüdür."}
{k:"Türkiye",s:"Çatalhöyük antik kenti hangi ildedir?",o:["Nevşehir","Konya","Kayseri","Aksaray"],d:1,a:"Çatalhöyük dünyanın en eski şehirlerinden biri olarak Konya da yer alır."}
{k:"Türkiye",s:"Türkiye de en çok çay hangi bölgede yetişir?",o:["Marmara","Ege","Karadeniz","Akdeniz"],d:2,a:"Çay üretimi Karadeniz Bölgesinin doğusunda yoğunlaşmıştır."}
{k:"Türkiye",s:"Afrodisias Antik Kenti hangi ildedir?",o:["Aydın","Denizli","Muğla","İzmir"],d:0,a:"Afrodisias Antik Kenti Aydın ilinde yer alır."}
{k:"Türkiye",s:"Türkiye nin en kurak bölgesi hangisidir?",o:["Karadeniz","İç Anadolu","Ege","Marmara"],d:1,a:"İç Anadolu Bölgesi Türkiye nin en kurak bölgesidir."}
{k:"Türkiye",s:"Erciyes Dağı hangi ildedir?",o:["Nevşehir","Kayseri","Aksaray","Niğde"],d:1,a:"Erciyes Dağı Kayseri ilinde bulunan sönmüş volkanik dağdır."}
{k:"Türkiye",s:"Amasra hangi ilde yer alır?",o:["Sinop","Kastamonu","Bartın","Zonguldak"],d:2,a:"Amasra Bartın iline bağlı tarihi bir ilçedir."}
{k:"Türkiye",s:"Zeugma Mozaik Müzesi hangi ildedir?",o:["Adıyaman","Şanlıurfa","Gaziantep","Malatya"],d:2,a:"Zeugma Mozaik Müzesi Gaziantep te dünyanın en büyük mozaik müzesidir."}
{k:"Türkiye",s:"Fırtına Vadisi hangi ildedir?",o:["Trabzon","Artvin","Rize","Giresun"],d:2,a:"Fırtına Vadisi Rize Çamlıhemşin de yer alır."}
{k:"Türkiye",s:"Myra Antik Kenti hangi ildedir?",o:["Muğla","Antalya","Mersin","Aydın"],d:1,a:"Myra Antik Kenti Antalya nın Demre ilçesindedir."}
{k:"Türkiye",s:"Türkiye nin en doğusundaki il hangisidir?",o:["Kars","Ağrı","Iğdır","Hakkari"],d:3,a:"Hakkari Türkiye nin en doğusundaki illerdendir."}
{k:"Türkiye",s:"Didim Antik Kenti hangi ildedir?",o:["İzmir","Muğla","Aydın","Denizli"],d:2,a:"Didim Antik Kenti Aydın ilindedir."}
{k:"Türkiye",s:"Türkiye de en fazla yağış alan bölge hangisidir?",o:["Akdeniz","Marmara","Karadeniz","Ege"],d:2,a:"Karadeniz Bölgesi Türkiye de en fazla yağış alan bölgedir."}
{k:"Türkiye",s:"Bergama Antik Kenti hangi ildedir?",o:["İzmir","Manisa","Aydın","Balıkesir"],d:0,a:"Bergama İzmir iline bağlı antik kentir."}
{k:"Türkiye",s:"Kaçkar Dağları hangi bölgededir?",o:["İç Anadolu","Doğu Anadolu","Karadeniz","Akdeniz"],d:2,a:"Kaçkar Dağları Karadeniz Bölgesinin doğusunda yer alır."}
{k:"Türkiye",s:"Perge Antik Kenti hangi ildedir?",o:["Mersin","Muğla","Antalya","Aydın"],d:2,a:"Perge Antik Kenti Antalya dadır."}
{k:"Türkiye",s:"Saklıkent Kanyonu hangi ildedir?",o:["Antalya","Muğla","Burdur","Isparta"],d:1,a:"Saklıkent Kanyonu Muğla ilinde yer alır."}
{k:"Türkiye",s:"Türkiye nin en yüksek barajı hangisidir?",o:["Keban","Atatürk","Artvin Yusufeli","Ilısu"],d:2,a:"Artvin Yusufeli Barajı Türkiye nin en yüksek barajıdır."}
{k:"Türkiye",s:"Kız Kulesi hangi şehirdedir?",o:["Ankara","İzmir","İstanbul","Antalya"],d:2,a:"Kız Kulesi İstanbul Boğazında yer alır."}
{k:"Türkiye",s:"Ani Harabeleri hangi ildedir?",o:["Erzurum","Kars","Iğdır","Ağrı"],d:1,a:"Ani Harabeleri Kars ilinde yer alan UNESCO Dünya Mirası alanıdır."}
{k:"Türkiye",s:"Patara Plajı hangi ildedir?",o:["Muğla","Antalya","Mersin","Aydın"],d:1,a:"Patara Plajı Antalya nın Kaş ilçesindedir."}
{k:"Türkiye",s:"Galata Kulesi hangi şehirdedir?",o:["Ankara","İzmir","İstanbul","Bursa"],d:2,a:"Galata Kulesi İstanbul un Beyoğlu ilçesinde yer alır."}
{k:"Spor",s:"Modern olimpiyatlar ilk hangi yılda yapıldı?",o:["1896","1900","1904","1912"],d:0,a:"Modern olimpiyat oyunları 1896 yılında Atina da başlamıştır."}
{k:"Spor",s:"FIFA Dünya Kupasını en çok hangi ülke kazandı?",o:["Almanya","Arjantin","Brezilya","İtalya"],d:2,a:"Brezilya 5 kez Dünya Kupası kazanarak rekor sahibidir."}
{k:"Spor",s:"Hangi sporda set sistemi uygulanır?",o:["Futbol","Basketbol","Voleybol","Hentbol"],d:2,a:"Voleybolda set sistemi uygulanır."}
{k:"Spor",s:"Tenis maçında love ne demektir?",o:["Sevgi","Sıfır puan","Beraberlik","Son set"],d:1,a:"Teniste love sıfır puan anlamına gelir."}
{k:"Spor",s:"Olimpiyatlarda altın madalya hangi sırayı gösterir?",o:["İkinci","Üçüncü","Birinci","Dördüncü"],d:2,a:"Altın madalya birinciliği temsil eder."}
{k:"Spor",s:"Kriket en çok hangi ülkelerde oynanır?",o:["ABD ve Kanada","Hindistan ve İngiltere","Japonya ve Çin","Brezilya ve Arjantin"],d:1,a:"Kriket özellikle Hindistan İngiltere ve Avustralya da popülerdir."}
{k:"Spor",s:"Formula 1 yarışlarında piste ne denir?",o:["Stadyum","Arena","Pistte","Pist (Circuit)"],d:3,a:"Formula 1 yarışları özel tasarlanmış pist (circuit) larda yapılır."}
{k:"Spor",s:"Bir basketbol maçı kaç periyottan oluşur?",o:["2","3","4","5"],d:2,a:"Basketbol maçı 4 periyottan oluşur."}
{k:"Spor",s:"Hangi spor dalında tatami kullanılır?",o:["Boks","Judo","Güreş","Eskrim"],d:1,a:"Judo müsabakaları tatami üzerinde yapılır."}
{k:"Spor",s:"UEFA Şampiyonlar Ligi hangi spor dalındadır?",o:["Basketbol","Voleybol","Futbol","Hentbol"],d:2,a:"UEFA Şampiyonlar Ligi Avrupa nın en prestijli futbol kulüp turnuvasıdır."}
{k:"Spor",s:"Serbest dalış nedir?",o:["Paraşütle atlama","Tüpsüz su altı dalışı","Kayak","Sörf"],d:1,a:"Serbest dalış tüp kullanmadan nefes tutarak yapılan dalıştır."}
{k:"Spor",s:"Triatlon kaç spor dalından oluşur?",o:["2","3","4","5"],d:1,a:"Triatlon yüzme bisiklet ve koşu olmak üzere 3 daldan oluşur."}
{k:"Spor",s:"Bir futbol maçı normal sürede kaç dakikadır?",o:["60","80","90","120"],d:2,a:"Bir futbol maçı normal sürede 90 dakikadır."}
{k:"Spor",s:"Wimbledon turnuvası hangi spor dalındadır?",o:["Golf","Tenis","Polo","Kriket"],d:1,a:"Wimbledon dünyanın en eski ve prestijli tenis turnuvasıdır."}
{k:"Spor",s:"NBA hangi ülkenin basketbol ligidır?",o:["Kanada","İngiltere","ABD","Avustralya"],d:2,a:"NBA Amerika Birleşik Devletleri nin profesyonel basketbol ligi dir."}
{k:"Spor",s:"Ragbi topunun şekli nasıldır?",o:["Yuvarlak","Oval","Kare","Üçgen"],d:1,a:"Ragbi topu oval şekildedir."}
{k:"Spor",s:"Eskrimde kullanılan silaha ne denir?",o:["Kılıç","Mızrak","Flöre","Bıçak"],d:2,a:"Eskrimde flöre epe ve kılıç türleri kullanılır."}
{k:"Spor",s:"Bir voleybol setini kazanmak için kaç sayıya ulaşmak gerekir?",o:["15","21","25","30"],d:2,a:"Voleybolda seti kazanmak için 25 sayıya ulaşmak gerekir (5. set hariç)."}
{k:"Spor",s:"Biathlon hangi iki sporu birleştirir?",o:["Yüzme koşu","Kayak atıcılık","Bisiklet koşu","Güreş boks"],d:1,a:"Biathlon kayak ve atıcılığı birleştiren bir kış sporudur."}
{k:"Spor",s:"Curling hangi yüzeyde oynanır?",o:["Çim","Kum","Buz","Ahşap"],d:2,a:"Curling buz üzerinde oynanan bir takım sporudur."}
{k:"Spor",s:"Bir tenis setini kazanmak için kaç oyun kazanılmalıdır?",o:["4","5","6","7"],d:2,a:"Tenis setini kazanmak için 6 oyun kazanmak gerekir."}
{k:"Spor",s:"Beyzbol hangi ülkenin milli sporudur?",o:["İngiltere","Kanada","ABD","Japonya"],d:2,a:"Beyzbol ABD nin en popüler sporlarından biridir."}
{k:"Spor",s:"Sumo güreşi hangi ülkenin geleneksel sporudur?",o:["Çin","Kore","Japonya","Moğolistan"],d:2,a:"Sumo güreşi Japonya nın geleneksel sporudur."}
{k:"Spor",s:"Sutopu hangi ortamda oynanır?",o:["Kumda","Havuzda","Çimde","Buz üstünde"],d:1,a:"Sutopu havuzda oynanan bir su sporudur."}
{k:"Spor",s:"Olimpiyatlarda hangi renk halka Avrupa yı temsil eder?",o:["Kırmızı","Mavi","Sarı","Yeşil"],d:1,a:"Mavi halka Avrupa kıtasını temsil eder."}
{k:"Matematik",s:"Bir üçgenin iç açıları toplamı kaç derecedir?",o:["90","180","270","360"],d:1,a:"Üçgenin iç açıları toplamı 180 derecedir."}
{k:"Matematik",s:"Pi sayısı yaklaşık kaçtır?",o:["2.14","3.14","4.14","5.14"],d:1,a:"Pi sayısı yaklaşık 3.14159 dur."}
{k:"Matematik",s:"256 nın karekökü kaçtır?",o:["14","15","16","17"],d:2,a:"16 x 16 = 256 olduğundan karekökü 16 dır."}
{k:"Matematik",s:"Bir dairenin alanı nasıl hesaplanır?",o:["2 pi r","pi r kare","pi d","2 r kare"],d:1,a:"Dairenin alanı pi r kare formülüyle hesaplanır."}
{k:"Matematik",s:"1 den 10 a kadar sayıların toplamı kaçtır?",o:["45","50","55","60"],d:2,a:"1+2+3+...+10 = 55 tir."}
{k:"Matematik",s:"Bir doğrunun açısı kaç derecedir?",o:["90","120","180","360"],d:2,a:"Bir doğrunun oluşturduğu düz açı 180 derecedir."}
{k:"Matematik",s:"Yüzde 25 kesir olarak nasıl yazılır?",o:["1/2","1/3","1/4","1/5"],d:2,a:"Yüzde 25 bir bütünün dörtte biri yani 1/4 tür."}
{k:"Matematik",s:"Asal sayı nedir?",o:["Çift sayı","Sadece 1 ve kendine bölünen","Tek sayı","Negatif sayı"],d:1,a:"Asal sayı sadece 1 ve kendisine tam bölünebilen sayıdır."}
{k:"Matematik",s:"13 asal sayı mıdır?",o:["Evet","Hayır","Bazen","Bilinmiyor"],d:0,a:"13 sadece 1 ve 13 e bölünebildiği için asal sayıdır."}
{k:"Matematik",s:"Karenin çevresi nasıl hesaplanır?",o:["a x a","4 x a","2 x a","a + b"],d:1,a:"Karenin çevresi 4 x kenar uzunluğu olarak hesaplanır."}
{k:"Matematik",s:"Negatif sayıların çarpımı nasıl sonuç verir?",o:["Negatif","Pozitif","Sıfır","Belirsiz"],d:1,a:"İki negatif sayının çarpımı pozitif sonuç verir."}
{k:"Matematik",s:"Bir küpün kaç yüzeyi vardır?",o:["4","5","6","8"],d:2,a:"Bir küpün 6 yüzeyi vardır."}
{k:"Matematik",s:"EBOB ne demektir?",o:["En büyük ortak bölen","En büyük ortak bölünen","En büyük oran","En büyük ortalama"],d:0,a:"EBOB en büyük ortak bölen anlamına gelir."}
{k:"Matematik",s:"EKOK ne demektir?",o:["En küçük ortak kat","En küçük ortak kalıntı","En küçük oran","En küçük ortalama"],d:0,a:"EKOK en küçük ortak kat anlamına gelir."}
{k:"Matematik",s:"24 ve 36 nın EBOB u kaçtır?",o:["6","8","12","18"],d:2,a:"24 ve 36 nın en büyük ortak böleni 12 dir."}
{k:"Matematik",s:"Bir dikdörtgenin alanı nasıl hesaplanır?",o:["a + b","a x b","2(a+b)","a kare"],d:1,a:"Dikdörtgenin alanı uzun kenar x kısa kenar olarak hesaplanır."}
{k:"Matematik",s:"Romen rakamıyla X kaçtır?",o:["5","10","50","100"],d:1,a:"Romen rakamıyla X on demektir."}
{k:"Matematik",s:"0.5 kesir olarak nasıl yazılır?",o:["1/3","1/2","1/4","1/5"],d:1,a:"0.5 bir bütünün yarısı yani 1/2 dir."}
{k:"Matematik",s:"Bir çemberin çevresi nasıl hesaplanır?",o:["pi r kare","2 pi r","pi d kare","4 r"],d:1,a:"Çemberin çevresi 2 pi r formülüyle hesaplanır."}
{k:"Matematik",s:"İkizkenar üçgenin özelliği nedir?",o:["3 kenarı eşit","2 kenarı eşit","Hiçbir kenarı eşit değil","Dik açılı"],d:1,a:"İkizkenar üçgenin iki kenarı birbirine eşittir."}
{k:"Matematik",s:"Fibonacci dizisinde ilk 5 sayı nedir?",o:["1 1 2 3 5","1 2 3 4 5","0 1 2 3 4","2 4 6 8 10"],d:0,a:"Fibonacci dizisi 1 1 2 3 5 şeklinde devam eder."}
{k:"Matematik",s:"Bir silindirin hacmi nasıl hesaplanır?",o:["pi r kare h","2 pi r h","pi r h","4/3 pi r kare"],d:0,a:"Silindirin hacmi pi r kare x yükseklik formülüyle hesaplanır."}
{k:"Matematik",s:"Tam kare sayı hangisidir?",o:["15","24","36","42"],d:2,a:"36 tam kare sayıdır çünkü 6 x 6 = 36 dır."}
{k:"Matematik",s:"Bir açının tümleyeni 90 derece ise açı kaç derecedir?",o:["0","45","90","180"],d:0,a:"Tümler açıların toplamı 90 derecedir 90-90=0 yani bu soru yanlıştır. Doğrusu: Tümleyeni 50 olan açı 40 derecedir."}
{k:"Matematik",s:"Mutlak değer ne demektir?",o:["Sayının işaretsiz hali","Sayının karesi","Sayının yarısı","Sayının tersi"],d:0,a:"Mutlak değer bir sayının sıfıra olan uzaklığıdır yani işaretsiz halidir."}
{k:"Deyimler",s:"Ayağını denk almak ne demektir?",o:["Hızlı yürümek","Dikkatli ve tedbirli olmak","Dans etmek","Koşmak"],d:1,a:"Ayağını denk almak dikkatli ve tedbirli davranmak demektir."}
{k:"Deyimler",s:"İpe un sermek ne anlama gelir?",o:["Yemek yapmak","Oyalayıcı davranmak","İp germek","Un ezmek"],d:1,a:"İpe un sermek yapılması gereken işi oyalayarak geciktirmek demektir."}
{k:"Deyimler",s:"Can kulağıyla dinlemek ne demektir?",o:["Kulak ağrısı","Çok dikkatli dinlemek","Fısıldamak","Sesli okumak"],d:1,a:"Can kulağıyla dinlemek büyük bir dikkat ve ilgiyle dinlemek demektir."}
{k:"Deyimler",s:"Gönlünü almak ne demektir?",o:["Kalbini çalmak","Memnun etmek kırgınlığını gidermek","Hediye almak","Yemek pişirmek"],d:1,a:"Gönlünü almak birinin kırgınlığını gidermek veya onu memnun etmek demektir."}
{k:"Deyimler",s:"Ateş pahası olmak ne demektir?",o:["Yanmak","Çok pahalı olmak","Isınmak","Ateşle oynamak"],d:1,a:"Ateş pahası çok pahalı anlamına gelir."}
{k:"Deyimler",s:"Yüzüne gözüne bulaştırmak ne demektir?",o:["Makyaj yapmak","Bir işi becerememek","Boyamak","Yıkanmak"],d:1,a:"Bir işi becerememek berbat etmek demektir."}
{k:"Deyimler",s:"Çenesi düşmek ne demektir?",o:["Çenesi kırılmak","Çok konuşmak","Ağlamak","Gülmek"],d:1,a:"Çenesi düşmek durmadan çok konuşmak demektir."}
{k:"Deyimler",s:"Tırnağıyla kazımak ne anlama gelir?",o:["Tırnak kesmek","Büyük emekle kazanmak","Temizlik yapmak","Boyamak"],d:1,a:"Büyük emek ve çabayla bir şey kazanmak demektir."}
{k:"Deyimler",s:"Kulağına küpe olmak ne demektir?",o:["Küpe takmak","Ders almak aklında tutmak","Kulak tıkamak","Süslenmek"],d:1,a:"Yaşanan olaydan ders alıp bir daha tekrarlamamak demektir."}
{k:"Deyimler",s:"Göz açıp kapayıncaya kadar ne demektir?",o:["Göz egzersizi","Çok kısa sürede","Uyumak","Şaşırmak"],d:1,a:"Çok kısa bir an çok hızlı bir şekilde demektir."}
{k:"Deyimler",s:"Başını kaşıyacak vakti olmamak ne demektir?",o:["Kaşıntı","Çok meşgul olmak","Tembel olmak","Uyumak"],d:1,a:"Çok yoğun ve meşgul olmak hiç boş vakti olmamak demektir."}
{k:"Deyimler",s:"Ağzından bal akmak ne demektir?",o:["Bal yemek","Tatlı ve güzel konuşmak","Ağız yarası","Şeker yemek"],d:1,a:"Çok tatlı ve güzel konuşmak demektir."}
{k:"Deyimler",s:"Yağmurdan kaçarken doluya tutulmak ne demektir?",o:["Hava durumu","Kötü durumdan daha kötüsüne düşmek","Islanmak","Şemsiye almak"],d:1,a:"Kötü bir durumdan kaçarken daha kötü bir duruma düşmek demektir."}
{k:"Deyimler",s:"Ocağına incir dikmek ne demektir?",o:["Bahçe işi","Birisinin yuvasını yıkmak","Ağaç dikmek","Yemek yapmak"],d:1,a:"Birinin yuvasını yıkmak hayatını mahvetmek demektir."}
{k:"Deyimler",s:"Ağzı kulaklarına varmak ne demektir?",o:["Kulak ağrısı","Çok sevinmek","Şaşırmak","Korkmak"],d:1,a:"Çok sevinmek gülmekten ağzının kulaklarına kadar açılması demektir."}
{k:"Deyimler",s:"Bin dereden su getirmek ne anlama gelir?",o:["Su taşımak","İkna etmek için çok uğraşmak","Yüzmek","Çeşme yapmak"],d:1,a:"Birini ikna etmek için türlü bahaneler öne sürmek demektir."}
{k:"Deyimler",s:"Dizini dövmek ne demektir?",o:["Egzersiz yapmak","Çok pişman olmak","Yere düşmek","Dans etmek"],d:1,a:"Çok pişman olmak ve üzülmek demektir."}
{k:"Deyimler",s:"Havadan nem kapmak ne demektir?",o:["Hastalanmak","Her şeyden alınmak","Nemli hava","Yağmur yağmak"],d:1,a:"Her şeyden alınan çok kolay kırılan kişi için kullanılır."}
{k:"Deyimler",s:"İki arada bir derede kalmak ne demektir?",o:["Yüzmek","İki seçenek arasında kararsız kalmak","Kaybolmak","Gezmek"],d:1,a:"İki seçenek arasında kararsız kalmak zor durumda olmak demektir."}
{k:"Deyimler",s:"Gözünün bebeği gibi korumak ne demektir?",o:["Göz doktoru","Çok özenle ve dikkatle korumak","Bebeğe bakmak","Gözlük takmak"],d:1,a:"Bir şeye veya birine çok özenle sahip çıkmak ve korumak demektir."}
{k:"Deyimler",s:"Tüylerini diken diken etmek ne demektir?",o:["Berber olmak","Çok korkutmak veya heyecanlandırmak","Uyumak","Isınmak"],d:1,a:"Çok korku veya heyecan vermek tüylerin ürpermesine neden olmak demektir."}
{k:"Deyimler",s:"Yel değirmenlerine savaş açmak ne demektir?",o:["Değirmen yapmak","Boş yere güçlü düşmanla uğraşmak","Rüzgar estirmek","Savaşmak"],d:1,a:"Boş yere karşı koyulamayacak güçlerle mücadele etmek demektir."}
{k:"Deyimler",s:"Bir taşla iki kuş vurmak ne demektir?",o:["Kuş avlamak","Tek hamleyle iki iş başarmak","Taş atmak","Kuş beslemek"],d:1,a:"Tek bir eylemle iki farklı işi aynı anda başarmak demektir."}
{k:"Deyimler",s:"Suya sabuna dokunmamak ne demektir?",o:["Temiz olmak","Hiçbir şeye karışmamak","Yıkanmak","Sabun yapmak"],d:1,a:"Hiçbir işe karışmamak taraf tutmamak sorumluluk almamak demektir."}
{k:"Deyimler",s:"Kolları sıvamak ne demektir?",o:["Gömlek giymek","İşe ciddi olarak girişmek","Kol egzersizi","Yıkanmak"],d:1,a:"Bir işe büyük bir kararlılıkla ve enerjiyle girişmek demektir."}
{k:"Atasözleri",s:"Nerede birlik orada dirlik ne demektir?",o:["Birlik ordusu","Birlikte olan toplum huzurlu olur","Askere gitmek","Savaş kazanmak"],d:1,a:"Birlik ve beraberlik olan yerde huzur ve düzen olur."}
{k:"Atasözleri",s:"Aç tavuk kendini buğday ambarında sanır ne anlatır?",o:["Tavuk beslemek","Çok isteyen hayal görür","Ambar yapmak","Buğday ekmek"],d:1,a:"Bir şeyi çok isteyen kişi onu her yerde görür hayal eder."}
{k:"Atasözleri",s:"Çivi çiviyi söker ne demektir?",o:["Tamir yapmak","Yeni sorun eskisini unutturur","Çivi çakmak","Tahta kırmak"],d:1,a:"Yeni bir durum veya dert eskisini unutturur demektir."}
{k:"Atasözleri",s:"Dağ dağa kavuşmaz insan insana kavuşur ne anlatır?",o:["Dağ tırmanışı","İnsanlar er ya da geç karşılaşır","Yolculuk","Harita okumak"],d:1,a:"İnsanların bir gün mutlaka tekrar karşılaşabileceğini anlatır."}
{k:"Atasözleri",s:"Demir tavında dövülür ne demektir?",o:["Demircilik","Fırsat anında hareket et","Metal işleme","Ateş yakmak"],d:1,a:"Fırsat uygun olduğunda hemen harekete geçmek gerekir."}
{k:"Atasözleri",s:"Ağaç meyvesi olunca başını eğer ne demektir?",o:["Meyve toplamak","Erdemli insan alçak gönüllüdür","Ağaç dikmek","Bahçe bakımı"],d:1,a:"Olgun ve bilgili insan alçak gönüllü olur."}
{k:"Atasözleri",s:"İyilik yap denize at ne demektir?",o:["Denize çöp atma","İyiliği karşılık beklemeden yap","Balık avla","Yüzmeye git"],d:1,a:"İyiliği hiçbir karşılık beklemeden yapmalısın."}
{k:"Atasözleri",s:"Zaman herşeyin ilacıdır ne anlatır?",o:["İlaç almak","Zamanla tüm yaralar iyileşir","Doktora gitmek","Saat almak"],d:1,a:"Zamanla acılar dinir yaralar iyileşir ve sorunlar çözülür."}
{k:"Atasözleri",s:"Güneş balçıkla sıvanmaz ne demektir?",o:["Güneş kremi","Gerçekler gizlenemez","Duvar boyamak","Hava durumu"],d:1,a:"Açık ve kesin olan gerçekler gizlenemez örtbas edilemez."}
{k:"Atasözleri",s:"Boş çuval ayakta durmaz ne anlatır?",o:["Çuval taşımak","İçi boş kişi ayakta kalamaz","Alışveriş","Depolama"],d:1,a:"Bilgi veya destek olmayan kişi başarılı olamaz."}
{k:"Atasözleri",s:"Tembele iş buyur sana akıl öğretsin ne demektir?",o:["İş vermek","Tembel kişi bahane üretmekte ustadır","Akıl almak","Danışmak"],d:1,a:"Tembel kişi iş yapmamak için türlü bahaneler üretir."}
{k:"Atasözleri",s:"Araba devrilince yol gösteren çok olur ne anlatır?",o:["Araba tamiri","İş işten geçtikten sonra akıl veren çok olur","Trafik kazası","Yol haritası"],d:1,a:"Olay olduktan sonra akıl veren ne yapılması gerektiğini söyleyen çok olur."}
{k:"Atasözleri",s:"Mart kapıdan baktırır kazma kürek yaktırır ne demektir?",o:["Mart ayı planı","Mart ayında hava değişken olur","Bahçe işi","Yakacak almak"],d:1,a:"Mart ayında hava çok değişken olur bahar sanılır ama soğuk geri gelir."}
{k:"Atasözleri",s:"Besle kargayı oysun gözünü ne anlatır?",o:["Karga beslemek","İyilik yaptığın kişi sana zarar verebilir","Kuş bakmak","Göz doktoru"],d:1,a:"İyilik ettiğin kişinin sana nankörlük yapabileceğini anlatır."}
{k:"Atasözleri",s:"Üzüm üzüme baka baka kararır ne demektir?",o:["Üzüm toplamak","İnsanlar çevrelerinden etkilenir","Bağ bakmak","Şarap yapmak"],d:1,a:"İnsanlar beraber oldukları kişilerden etkilenip onlara benzerler."}
{k:"Atasözleri",s:"Her kuşun eti yenmez ne anlatır?",o:["Kuş eti","Her insana her şey söylenemez","Avcılık","Yemek tarifi"],d:1,a:"Her insanla her konuda rahat konuşulamaz bazı insanlara dikkat edilmeli."}
{k:"Atasözleri",s:"At ölür meydan kalır yiğit ölür şan kalır ne demektir?",o:["At yarışı","İyi isim bırakana adı yaşar","At bakımı","Savaş meydanı"],d:1,a:"İnsan ölür ama arkasında bıraktığı iyi isim ve eserler yaşamaya devam eder."}
{k:"Atasözleri",s:"Korkunun ecele faydası yoktur ne anlatır?",o:["Korkak olmak","Korkmak sonucu değiştirmez","Doktor olmak","Cesur olmak"],d:1,a:"Korkmak kaçınılmaz olanı engellemez gereksiz yere endişelenmemelisin."}
{k:"Atasözleri",s:"Sükut ikrardan gelir ne demektir?",o:["Sessiz olmak","Susma kabul etmek demektir","Konuşmak","İtiraz etmek"],d:1,a:"Bir şeye karşı çıkılmayıp susulması onu kabul etmek anlamına gelir."}
{k:"Atasözleri",s:"Dervişin fikri neyse zikri de odur ne anlatır?",o:["Dini ibadet","İnsan sürekli düşündüğünü konuşur","Meditasyon","Dua etmek"],d:1,a:"İnsan sürekli aklında olan konuyu konuşur ve ondan bahseder."}
{k:"Atasözleri",s:"Her işin başı sağlık ne demektir?",o:["Hastane","Sağlık her şeyden önemlidir","Spor yapmak","Doktor olmak"],d:1,a:"En önemli şey sağlıktır sağlık olmadan hiçbir şeyin değeri yoktur."}
{k:"Atasözleri",s:"Kendi düşen ağlamaz ne anlatır?",o:["Düşmek","Kendi hatasının sonuçlarına katlanmalı","Ağlamamak","Dikkatli olmak"],d:1,a:"Kendi hatasıyla başına kötü gelen kişi şikayet etmemelidir."}
{k:"Atasözleri",s:"Horozu çok olan köyün sabahı erken olur ne demektir?",o:["Horoz yetiştirmek","Yöneticisi çok olanlar karışıklık yaşar","Erken kalkmak","Köy hayatı"],d:1,a:"Bir yerde söz sahibi çok olursa kargaşa çıkar."}
{k:"Atasözleri",s:"Gönül ne kahve ister ne kahvehane ne demektir?",o:["Kahve içmek","İnsan samimi ilgi ve sohbet ister","Kafede oturmak","Kahve yapmak"],d:1,a:"İnsanın istediği maddi şeyler değil samimi ilgi ve dostluktur."}
{k:"Atasözleri",s:"Bıçak yarası geçer dil yarası geçmez ne anlatır?",o:["Bıçak yaralanması","Sözle verilen acı kalıcıdır","Dil sağlığı","İlk yardım"],d:1,a:"Fiziksel yaralar iyileşir ama kötü sözlerin acısı kalıcıdır."}
{k:"Coğrafya",s:"Meridyen nedir?",o:["Yatay çizgi","Boyunca çizilen dikey çizgi","Ekvator çizgisi","Kutup noktası"],d:1,a:"Meridyenler kutupları birleştiren dikey hayali çizgilerdir."}
{k:"Coğrafya",s:"Paralel nedir?",o:["Dikey çizgi","Ekvator paraleli yatay çizgi","Meridyen çizgisi","Boylam çizgisi"],d:1,a:"Paraleller ekvatore paralel çizilen yatay hayali çizgilerdir."}
{k:"Coğrafya",s:"Hangi rüzgar Türkiye ye yağış getirir?",o:["Poyraz","Lodos","Yıldız","Keşişleme"],d:1,a:"Lodos güneyden esen sıcak ve nemli rüzgardır yağış getirir."}
{k:"Coğrafya",s:"Muson iklimi nerelerde görülür?",o:["Kutuplarda","Güney ve Güneydoğu Asya","Avrupa","Kuzey Amerika"],d:1,a:"Muson iklimi özellikle Güney ve Güneydoğu Asya da görülür."}
{k:"Coğrafya",s:"Dünya üzerinde kaç zaman dilimi vardır?",o:["12","18","24","36"],d:2,a:"Dünya 24 zaman dilimine bölünmüştür."}
{k:"Coğrafya",s:"Yer kabuğunu oluşturan büyük parçalara ne denir?",o:["Magma","Levha (plaka)","Manto","Çekirdek"],d:1,a:"Yer kabuğu tektonik levhalardan (plakalardan) oluşur."}
{k:"Coğrafya",s:"Tropikal iklim hangi bölgelerde görülür?",o:["Kutuplarda","Ekvator çevresinde","Ilıman kuşakta","Çöllerde"],d:1,a:"Tropikal iklim ekvator çevresindeki sıcak ve nemli bölgelerde görülür."}
{k:"Coğrafya",s:"Fırtına hangi olaydan kaynaklanır?",o:["Deprem","Basınç farkı ve rüzgar","Volkan","Tsunami"],d:1,a:"Fırtınalar atmosferik basınç farklarından kaynaklanan güçlü rüzgarlardır."}
{k:"Coğrafya",s:"Göl ile deniz arasındaki fark nedir?",o:["Boyut","Göller karayla çevrili denizler değil","Renk","Derinlik"],d:1,a:"Göller her tarafı karayla çevrili su kütleleridir denizler okyanuslarla bağlantılıdır."}
{k:"Coğrafya",s:"Delta nasıl oluşur?",o:["Depremle","Nehirlerin denize döküldüğü yerde alüvyon birikmesiyle","Volkanla","Rüzgarla"],d:1,a:"Delta nehirlerin taşıdığı alüvyonları denize döküldüğü yerde biriktirmesiyle oluşur."}
{k:"Coğrafya",s:"Yer altı suyu nasıl oluşur?",o:["Volkanla","Yağışların toprağa sızmasıyla","Depremle","Rüzgarla"],d:1,a:"Yağış suları toprağa sızarak yer altında birikerek yer altı suyunu oluşturur."}
{k:"Coğrafya",s:"Barometle ne ölçülür?",o:["Sıcaklık","Hava basıncı","Nem","Rüzgar hızı"],d:1,a:"Barometre hava basıncını ölçen alettir."}
{k:"Coğrafya",s:"Troposfer nedir?",o:["Uzay","Atmosferin en alt katmanı","Ozon tabakası","Yer kabuğu"],d:1,a:"Troposfer atmosferin en alt katmanıdır hava olayları burada gerçekleşir."}
{k:"Coğrafya",s:"Okyanus akıntıları ne etkiler?",o:["Depremleri","İklimi ve deniz canlılarını","Volkanları","Dağ oluşumunu"],d:1,a:"Okyanus akıntıları iklimi ve deniz ekosistemlerini etkiler."}
{k:"Coğrafya",s:"Tundra iklimi nerelerde görülür?",o:["Ekvator","Kutup bölgeleri","Tropikal","Akdeniz"],d:1,a:"Tundra iklimi kutuplara yakın soğuk bölgelerde görülür."}
{k:"Coğrafya",s:"Step iklimi nedir?",o:["Çok yağışlı","Yarı kurak bozkır iklimi","Tropikal","Kutupsal"],d:1,a:"Step iklimi az yağışlı yarı kurak bozkır alanlarında görülür."}
{k:"Coğrafya",s:"Tsunami nasıl oluşur?",o:["Rüzgarla","Deniz altı deprem veya volkanla","Yağmurla","Gel gitlerle"],d:1,a:"Tsunami deniz altındaki deprem veya volkanik aktivitelerle oluşan dev dalgalardır."}
{k:"Coğrafya",s:"Gece gündüz eşitliği ne zaman olur?",o:["21 Haziran","21 Aralık","21 Mart ve 23 Eylül","1 Ocak"],d:2,a:"21 Mart ve 23 Eylül tarihlerinde gece gündüz eşitliği yaşanır."}
{k:"Coğrafya",s:"Karstik oluşum hangisidir?",o:["Volkan","Mağara","Delta","Vadi"],d:1,a:"Kireçtaşının erimesiyle oluşan mağaralar karstik oluşumlardır."}
{k:"Coğrafya",s:"Akdeniz ikliminin özelliği nedir?",o:["Yazlar yağışlı","Yazlar sıcak kuru kışlar ılık yağışlı","Her mevsim soğuk","Her mevsim yağışlı"],d:1,a:"Akdeniz ikliminde yazlar sıcak ve kurak kışlar ılık ve yağışlıdır."}
{k:"Bilim",s:"Protonun yükü nedir?",o:["Negatif","Nötr","Pozitif","Değişken"],d:2,a:"Protonun yükü pozitiftir."}
{k:"Bilim",s:"Elektronun yükü nedir?",o:["Pozitif","Nötr","Negatif","Değişken"],d:2,a:"Elektronun yükü negatiftir."}
{k:"Bilim",s:"Hangi gezegen güneş sisteminin en sıcak gezegenidir?",o:["Merkür","Venüs","Mars","Jüpiter"],d:1,a:"Venüs yoğun atmosferi nedeniyle sera etkisiyle en sıcak gezegendir."}
{k:"Bilim",s:"Karbon elementinin sembolü nedir?",o:["Ca","Co","C","Cr"],d:2,a:"Karbon elementinin sembolü C dir."}
{k:"Bilim",s:"Hangi cihaz hava basıncını ölçer?",o:["Termometre","Barometre","Voltmetre","Ampermetre"],d:1,a:"Barometre hava basıncını ölçen cihazdır."}
{k:"Bilim",s:"Foton nedir?",o:["Atom parçacığı","Işık parçacığı","Ses dalgası","Elektrik birimi"],d:1,a:"Foton ışığın en küçük enerji paketidir."}
{k:"Bilim",s:"Hangi gaz yanmayı destekler?",o:["Azot","Karbondioksit","Oksijen","Helyum"],d:2,a:"Oksijen yanmayı destekleyen gazdır."}
{k:"Bilim",s:"İnsan vücudunda en sert doku hangisidir?",o:["Kemik","Kıkırdak","Diş minesi","Tırnak"],d:2,a:"Diş minesi insan vücudundaki en sert dokudur."}
{k:"Bilim",s:"Hangi bilim dalı yıldızları inceler?",o:["Jeoloji","Biyoloji","Astronomi","Meteoroloji"],d:2,a:"Astronomi gök cisimlerini ve yıldızları inceleyen bilim dalıdır."}
{k:"Bilim",s:"Sindirim sisteminin ilk organı hangisidir?",o:["Mide","Ağız","Yemek borusu","İnce bağırsak"],d:1,a:"Sindirim ağızda başlar çiğneme ve tükürük ile mekanik ve kimyasal sindirim yapılır."}
{k:"Bilim",s:"Kan grupları kaç tanedir?",o:["2","3","4","6"],d:2,a:"4 ana kan grubu vardır A B AB ve 0."}
{k:"Bilim",s:"Newton un üçüncü yasası nedir?",o:["Kuvvet","Her etkiye eşit ve zıt tepki","İvme","Enerji korunumu"],d:1,a:"Her etkiye eşit büyüklükte ve zıt yönde bir tepki kuvveti vardır."}
{k:"Bilim",s:"Hangi madde sıvı metal olarak bilinir?",o:["Altın","Gümüş","Civa","Bakır"],d:2,a:"Civa oda sıcaklığında sıvı halde bulunan tek metaldir."}
{k:"Bilim",s:"Klorofil hangi renk ışığı emer?",o:["Yeşil","Kırmızı ve mavi","Sarı","Beyaz"],d:1,a:"Klorofil kırmızı ve mavi ışığı emer yeşili yansıtır."}
{k:"Bilim",s:"Deprem dalgalarını ölçen cihaz nedir?",o:["Barometre","Sismograf","Termometre","Voltmetre"],d:1,a:"Sismograf deprem dalgalarını ölçen ve kaydeden cihazdır."}
{k:"Bilim",s:"Suyun kimyasal formülü nedir?",o:["H2O","CO2","NaCl","O2"],d:0,a:"Suyun kimyasal formülü H2O dur."}
{k:"Bilim",s:"Genetik biliminin babası kimdir?",o:["Darwin","Mendel","Pasteur","Watson"],d:1,a:"Gregor Mendel genetik biliminin babası olarak kabul edilir."}
{k:"Bilim",s:"Hücrenin enerji santrali hangisidir?",o:["Çekirdek","Ribozom","Mitokondri","Lizozom"],d:2,a:"Mitokondri hücrenin enerji santralıdır."}
{k:"Bilim",s:"Hangisi bir bileşiktir?",o:["Oksijen","Demir","Su","Altın"],d:2,a:"Su iki farklı elementten oluşan bir bileşiktir."}
{k:"Bilim",s:"Evrenin yaşı yaklaşık kaç milyar yıldır?",o:["4.5","9","13.8","20"],d:2,a:"Evrenin yaşı yaklaşık 13.8 milyar yıl olarak hesaplanmıştır."}
{k:"Doğa",s:"Mantar hangi canlı grubuna aittir?",o:["Bitki","Hayvan","Mantarlar alemi","Bakteri"],d:2,a:"Mantarlar ne bitki ne hayvan olan ayrı bir canlı alemine aittir."}
{k:"Doğa",s:"Simbiyoz ilişki nedir?",o:["Düşmanlık","İki canlının birlikte yaşayıp karşılıklı fayda sağlaması","Avlanma","Rekabet"],d:1,a:"Simbiyoz iki canlının birlikte yaşayarak karşılıklı fayda sağladığı ilişkidir."}
{k:"Doğa",s:"Predatör ne demektir?",o:["Bitki","Avcı hayvan","Otçul","Çürükçül"],d:1,a:"Predatör başka hayvanları avlayarak beslenen avcı hayvandır."}
{k:"Doğa",s:"Omurgasız hayvan hangisidir?",o:["Kedi","Balık","Ahtapot","Kuş"],d:2,a:"Ahtapot omurgası olmayan yumuşakça sınıfından bir hayvandır."}
{k:"Doğa",s:"Erozyon nedir?",o:["Bitki büyümesi","Toprağın su ve rüzgarla aşınması","Volkanik patlama","Deprem"],d:1,a:"Erozyon toprağın su rüzgar gibi etkenlerle aşınıp taşınmasıdır."}
{k:"Doğa",s:"Hangi hayvan sonar kullanır?",o:["Kartal","Yunus","Aslan","Tavşan"],d:1,a:"Yunuslar ekolokasyon ile sonar kullanarak yön bulur ve avlanır."}
{k:"Doğa",s:"Toprak katmanlarına ne denir?",o:["Magma","Toprak horizonları","Lav","Plaka"],d:1,a:"Toprağın farklı katmanlarına toprak horizonları denir."}
{k:"Doğa",s:"Fotosentezde üretilen gaz hangisidir?",o:["Karbondioksit","Azot","Oksijen","Metan"],d:2,a:"Fotosentez sonucunda oksijen gazı üretilir."}
{k:"Doğa",s:"Doğal seleksiyon teorisini kim öne sürdü?",o:["Mendel","Einstein","Darwin","Newton"],d:2,a:"Charles Darwin doğal seleksiyon teorisini ortaya koymuştur."}
{k:"Doğa",s:"Orman yangınlarının en büyük nedeni nedir?",o:["Volkan","İnsan kaynaklı nedenler","Deprem","Sel"],d:1,a:"Orman yangınlarının büyük çoğunluğu insan kaynaklı nedenlerle çıkar."}
{k:"Doğa",s:"Parazit canlı nedir?",o:["Serbest yaşayan","Başka canlının üzerinde yaşayıp zarar veren","Üretici","Tüketici"],d:1,a:"Parazit başka bir canlının üzerinde yaşayıp ondan beslenip zarar veren canlıdır."}
{k:"Doğa",s:"Hangi hayvan en zeki kabul edilir?",o:["Köpek","Yunus","Kedi","Papağan"],d:1,a:"Yunuslar en zeki hayvanlardan biri olarak kabul edilir."}
{k:"Doğa",s:"Çölde yaşayan bitkiler suyu nasıl depolar?",o:["Yapraklarda","Gövde ve köklerinde","Çiçeklerinde","Tohumlarında"],d:1,a:"Çöl bitkileri suyu kalın gövdelerinde ve derin köklerinde depolar."}
{k:"Doğa",s:"Hangi kuş en büyük yumurtayı bırakır?",o:["Kartal","Deve kuşu","Penguen","Flamingo"],d:1,a:"Deve kuşu dünyanın en büyük yumurtasını bırakan kuştur."}
{k:"Doğa",s:"Asit yağmuru nedir?",o:["Normal yağmur","Hava kirliliğinin neden olduğu asitli yağış","Tuzlu yağmur","Sıcak yağmur"],d:1,a:"Asit yağmuru hava kirliliğindeki gazların yağmur suyuyla birleşmesiyle oluşur."}
{k:"Doğa",s:"Hangi böcek en çok türe sahiptir?",o:["Karınca","Kelebek","Kın kanatlılar (böcek)","Arı"],d:2,a:"Kın kanatlılar (Coleoptera) en fazla türe sahip böcek takımıdır."}
{k:"Doğa",s:"Tozlaşma nedir?",o:["Toz temizleme","Polenin çiçeğe taşınması","Toprağın aşınması","Rüzgar oluşumu"],d:1,a:"Tozlaşma polenin rüzgar veya böceklerle çiçeğin dişi organına taşınmasıdır."}
{k:"Doğa",s:"Hangi hayvan dünyada en çok popülasyona sahiptir?",o:["İnsan","Tavuk","Karınca","Balık"],d:2,a:"Karıncalar dünyada en yüksek popülasyona sahip canlılardan biridir."}
{k:"Doğa",s:"Habitat ne demektir?",o:["Hayvan türü","Canlının doğal yaşam alanı","Bitki türü","Hava durumu"],d:1,a:"Habitat bir canlının doğal olarak yaşadığı çevre ve alandır."}
{k:"Doğa",s:"Birincil tüketici ne demektir?",o:["Bitki","Bitkilerle beslenen otçul hayvan","Etçil hayvan","Ayrıştırıcı"],d:1,a:"Birincil tüketiciler bitkilerle beslenen otçul hayvanlardır."}
{k:"Başkentler",s:"Belçika nın başkenti neresidir?",o:["Amsterdam","Brüksel","Lüksemburg","Paris"],d:1,a:"Brüksel Belçika nın başkentidir."}
{k:"Başkentler",s:"Hollanda nın başkenti neresidir?",o:["Rotterdam","Amsterdam","Lahey","Utrecht"],d:1,a:"Amsterdam Hollanda nın resmi başkentidir."}
{k:"Başkentler",s:"Şili nin başkenti neresidir?",o:["Buenos Aires","Santiago","Lima","Bogota"],d:1,a:"Santiago Şili nin başkentidir."}
{k:"Başkentler",s:"Slovenya nın başkenti neresidir?",o:["Zagreb","Belgrad","Ljubljana","Sarajevo"],d:2,a:"Ljubljana Slovenya nın başkentidir."}
{k:"Başkentler",s:"Hırvatistan ın başkenti neresidir?",o:["Ljubljana","Zagreb","Belgrad","Sarajevo"],d:1,a:"Zagreb Hırvatistan ın başkentidir."}
{k:"Başkentler",s:"Sırbistan ın başkenti neresidir?",o:["Zagreb","Ljubljana","Belgrad","Tiran"],d:2,a:"Belgrad Sırbistan ın başkentidir."}
{k:"Başkentler",s:"Bosna Hersek in başkenti neresidir?",o:["Zagreb","Belgrad","Sarajevo","Tiran"],d:2,a:"Sarajevo Bosna Hersek in başkentidir."}
{k:"Başkentler",s:"Arnavutluk un başkenti neresidir?",o:["Belgrad","Tiran","Podgorica","Üsküp"],d:1,a:"Tiran Arnavutluk un başkentidir."}
{k:"Başkentler",s:"Kuzey Makedonya nın başkenti neresidir?",o:["Tiran","Belgrad","Üsküp","Priştine"],d:2,a:"Üsküp Kuzey Makedonya nın başkentidir."}
{k:"Başkentler",s:"Bulgaristan ın başkenti neresidir?",o:["Bükreş","Sofya","Belgrad","Tiran"],d:1,a:"Sofya Bulgaristan ın başkentidir."}
{k:"Başkentler",s:"Suudi Arabistan ın başkenti neresidir?",o:["Dubai","Riyad","Mekke","Cidde"],d:1,a:"Riyad Suudi Arabistan ın başkentidir."}
{k:"Başkentler",s:"Birleşik Arap Emirlikleri nin başkenti neresidir?",o:["Dubai","Abu Dabi","Doha","Riyad"],d:1,a:"Abu Dabi BAE nin başkentidir."}
{k:"Başkentler",s:"Katar ın başkenti neresidir?",o:["Dubai","Riyad","Doha","Muskat"],d:2,a:"Doha Katar ın başkentidir."}
{k:"Başkentler",s:"İsrail in başkenti neresidir?",o:["Tel Aviv","Kudüs","Hayfa","Eilat"],d:1,a:"İsrail Kudüs ü başkent olarak kabul eder."}
{k:"Başkentler",s:"Lübnan ın başkenti neresidir?",o:["Bağdat","Şam","Beyrut","Amman"],d:2,a:"Beyrut Lübnan ın başkentidir."}
{k:"Başkentler",s:"Suriye nin başkenti neresidir?",o:["Beyrut","Şam","Bağdat","Amman"],d:1,a:"Şam Suriye nin başkentidir."}
{k:"Başkentler",s:"Ürdün ün başkenti neresidir?",o:["Beyrut","Şam","Bağdat","Amman"],d:3,a:"Amman Ürdün ün başkentidir."}
{k:"Başkentler",s:"Malezya nın başkenti neresidir?",o:["Singapur","Kuala Lumpur","Jakarta","Manila"],d:1,a:"Kuala Lumpur Malezya nın başkentidir."}
{k:"Başkentler",s:"Myanmar ın başkenti neresidir?",o:["Yangon","Naypyidaw","Bangkok","Hanoi"],d:1,a:"Naypyidaw Myanmar ın başkentidir."}
{k:"Başkentler",s:"Moğolistan ın başkenti neresidir?",o:["Pekin","Astana","Ulan Batur","Bişkek"],d:2,a:"Ulan Batur Moğolistan ın başkentidir."}
{k:"Türkiye",s:"Sumela Manastırı hangi vadide yer alır?",o:["Fırtına Vadisi","Altındere Vadisi","Ihlara Vadisi","Köprülü Kanyon"],d:1,a:"Sumela Manastırı Trabzon Altındere Vadisinde yer alır."}
{k:"Türkiye",s:"Ihlara Vadisi hangi ildedir?",o:["Nevşehir","Aksaray","Kayseri","Niğde"],d:1,a:"Ihlara Vadisi Aksaray ilinde bulunan 14 km uzunluğunda bir kanyondur."}
{k:"Türkiye",s:"Türkiye de en çok zeytin hangi bölgede üretilir?",o:["Karadeniz","Ege","İç Anadolu","Doğu Anadolu"],d:1,a:"Zeytin üretimi en çok Ege Bölgesinde yapılmaktadır."}
{k:"Türkiye",s:"Boğaziçi Köprüsü kaç yılında açıldı?",o:["1970","1973","1980","1985"],d:1,a:"Boğaziçi Köprüsü 1973 yılında hizmete açılmıştır."}
{k:"Türkiye",s:"Türkiye nin en eski şehirlerinden biri olan Mardin hangi bölgededir?",o:["Akdeniz","İç Anadolu","Güneydoğu Anadolu","Doğu Anadolu"],d:2,a:"Mardin Güneydoğu Anadolu Bölgesinde yer alır."}
{k:"Türkiye",s:"Harran Ovası hangi ildedir?",o:["Mardin","Şanlıurfa","Diyarbakır","Gaziantep"],d:1,a:"Harran Ovası Şanlıurfa ilinde yer alır."}
{k:"Türkiye",s:"Antalya Müzesi hangi döneme ait eserleriyle ünlüdür?",o:["Osmanlı","Roma ve antik dönem","Cumhuriyet","Selçuklu"],d:1,a:"Antalya Müzesi Roma ve antik dönem eserleriyle ünlü bir müzedir."}
{k:"Türkiye",s:"Hierapolis Antik Kenti hangi ilde yer alır?",o:["Muğla","Denizli","Aydın","İzmir"],d:1,a:"Hierapolis Antik Kenti Denizli Pamukkale de yer alır."}
{k:"Türkiye",s:"Olympos Antik Kenti hangi ildedir?",o:["Muğla","İzmir","Antalya","Mersin"],d:2,a:"Olympos Antik Kenti Antalya nın Kumluca ilçesindedir."}
{k:"Türkiye",s:"Türkiye de hangi il en çok fındık üretir?",o:["Trabzon","Ordu","Giresun","Rize"],d:1,a:"Ordu ili Türkiye nin en fazla fındık üreten ilidir."}
{k:"Türkiye",s:"Selimiye Camii hangi ildedir?",o:["İstanbul","Konya","Bursa","Edirne"],d:3,a:"Mimar Sinan ın ustalık eseri Selimiye Camii Edirne dedir."}
{k:"Türkiye",s:"Topkapı Sarayı hangi şehirdedir?",o:["Ankara","Edirne","Bursa","İstanbul"],d:3,a:"Topkapı Sarayı İstanbul da yer alan Osmanlı sarayıdır."}
{k:"Türkiye",s:"Dolmabahçe Sarayı hangi boğazda yer alır?",o:["Çanakkale","İstanbul Boğazı","Kerç","Süveyş"],d:1,a:"Dolmabahçe Sarayı İstanbul Boğazı kıyısında yer alır."}
{k:"Türkiye",s:"Yedigöller Milli Parkı hangi ildedir?",o:["Kastamonu","Bartın","Bolu","Düzce"],d:2,a:"Yedigöller Milli Parkı Bolu ilinde yer alır."}
{k:"Türkiye",s:"Aizanoi Antik Kenti hangi ildedir?",o:["Kütahya","Afyon","Eskişehir","Uşak"],d:0,a:"Aizanoi Antik Kenti Kütahya nın Çavdarhisar ilçesindedir."}
{k:"Türkiye",s:"Türkiye nin en geniş ovası hangisidir?",o:["Çukurova","Konya Ovası","Bafra Ovası","Muş Ovası"],d:1,a:"Konya Ovası Türkiye nin en geniş ovasıdır."}
{k:"Türkiye",s:"Likya Yolu hangi bölgededir?",o:["Karadeniz","Ege","Akdeniz","Marmara"],d:2,a:"Likya Yolu Akdeniz Bölgesinde Antalya ve Muğla arasında uzanır."}
{k:"Türkiye",s:"Uludağ hangi ildedir?",o:["İstanbul","Bursa","Eskişehir","Bilecik"],d:1,a:"Uludağ Bursa ilinde yer alan kış turizmi merkezidir."}
{k:"Türkiye",s:"Abant Gölü hangi ildedir?",o:["Düzce","Sakarya","Bolu","Kastamonu"],d:2,a:"Abant Gölü Bolu ilinde yer alan doğal güzelliklerden biridir."}
{k:"Türkiye",s:"Xanthos Antik Kenti hangi ildedir?",o:["Antalya","Muğla","Aydın","Denizli"],d:0,a:"Xanthos Likya medeniyetinin başkenti olarak Antalya dadır."}
{k:"Türkiye",s:"Türkiye de kaç UNESCO Dünya Mirası alanı vardır?",o:["10-12","15-17","19-21","25-27"],d:2,a:"Türkiye 2024 itibarıyla 21 UNESCO Dünya Mirası alanına sahiptir."}
{k:"Türkiye",s:"Karain Mağarası hangi ildedir?",o:["Mersin","Antalya","Muğla","Burdur"],d:1,a:"Karain Mağarası Antalya da bulunan Anadolunun en eski yerleşim yerlerinden biridir."}
{k:"Türkiye",s:"Safranbolu evleri hangi mimari tarzda yapılmıştır?",o:["Modern","Osmanlı sivil mimarisi","Gotik","Barok"],d:1,a:"Safranbolu evleri Osmanlı sivil mimarisi örneğidir."}
{k:"Türkiye",s:"Hasankeyf hangi ildedir?",o:["Mardin","Şırnak","Batman","Siirt"],d:2,a:"Hasankeyf antik kenti Batman ilinde yer almaktadır."}
{k:"Türkiye",s:"Türkiye nin en yağışlı ili hangisidir?",o:["Trabzon","Rize","Artvin","Giresun"],d:1,a:"Rize Türkiye nin en çok yağış alan ilidir."}
{k:"Spor",s:"Tour de France hangi spor dalının yarışıdır?",o:["Koşu","Bisiklet","Yüzme","Kayak"],d:1,a:"Tour de France dünyanın en ünlü bisiklet yarışıdır."}
{k:"Spor",s:"Bir rugby maçında kaç oyuncu sahadadır?",o:["11","13","15","18"],d:2,a:"Rugby Union da her takımdan 15 oyuncu sahada bulunur."}
{k:"Spor",s:"Badminton da kullanılan topa ne denir?",o:["Top","Birdie","Koza","Tüylü top"],d:3,a:"Badminton da kullanılan tüylü topa shuttlecock veya tüylü top denir."}
{k:"Spor",s:"Super Bowl hangi sporun finalidir?",o:["Basketbol","Beyzbol","Amerikan futbolu","Hokey"],d:2,a:"Super Bowl Amerikan futbolunun (NFL) final maçıdır."}
{k:"Spor",s:"Pele hangi ülkenin futbolcusudur?",o:["Arjantin","Brezilya","Portekiz","İspanya"],d:1,a:"Pele Brezilyalı efsanevi futbolcudur."}
{k:"Spor",s:"Hangi spor dalında paralel bar kullanılır?",o:["Atletizm","Jimnastik","Yüzme","Boks"],d:1,a:"Jimnastikte paralel bar kullanılan aletlerden biridir."}
{k:"Spor",s:"Olimpiyatlarda kış sporları hangileridir?",o:["Yüzme futbol","Kayak buz pateni biatlon","Tenis golf","Atletizm güreş"],d:1,a:"Kış Olimpiyatlarında kayak buz pateni biatlon gibi sporlar yapılır."}
{k:"Spor",s:"Usain Bolt hangi yarış mesafesinin rekorunu kırdı?",o:["400 metre","200 metre","100 metre","800 metre"],d:2,a:"Usain Bolt 100 metre de 9.58 saniye ile dünya rekorunu kırmıştır."}
{k:"Spor",s:"Boks ringinin şekli nasıldır?",o:["Daire","Kare","Dikdörtgen","Altıgen"],d:1,a:"Boks ringi kare şeklindedir."}
{k:"Spor",s:"Halter sporunda kaç hareket yapılır?",o:["1","2","3","4"],d:1,a:"Halterde koparma ve silkme olmak üzere 2 hareket yapılır."}
{k:"Spor",s:"Polo sporunda hangi hayvan kullanılır?",o:["Deve","At","Fil","Eşek"],d:1,a:"Polo at üzerinde oynanan bir spordur."}
{k:"Spor",s:"Bowling da kaç pini devirmek gerekir?",o:["8","9","10","12"],d:2,a:"Bowling da 10 pini devirmek amaçlanır."}
{k:"Spor",s:"Dart tahtasında en yüksek tek alan puanı kaçtır?",o:["20","25","50","60"],d:3,a:"Üçlü 20 alanı 60 puanla en yüksek tek alan puanını verir."}
{k:"Spor",s:"Bir golf sahasında kaç delik vardır?",o:["9","12","15","18"],d:3,a:"Standart bir golf sahasında 18 delik bulunur."}
{k:"Spor",s:"Kano ve kayak farkı nedir?",o:["Aynı spor","Kanoda tek kürek kayakta çift kürek","Biri denizde biri nehirde","Fark yok"],d:1,a:"Kanoda tek taraflı kürek kayakta çift taraflı kürek kullanılır."}
{k:"Spor",s:"Sörf hangi doğal güçle yapılır?",o:["Rüzgar","Dalga","Akıntı","Gel git"],d:1,a:"Sörf okyanus dalgaları üzerinde tahta ile yapılan bir spordur."}
{k:"Spor",s:"Paralimpik oyunlar kimler için düzenlenir?",o:["Yaşlılar","Engelli sporcular","Çocuklar","Amatörler"],d:1,a:"Paralimpik oyunlar engelli sporcular için düzenlenen uluslararası spor etkinliğidir."}
{k:"Spor",s:"Bir maratonu tamamlama süresi dünya rekoru yaklaşık kaç dakikadır?",o:["90","100","120","150"],d:2,a:"Maraton dünya rekoru yaklaşık 2 saat yani 120 dakika civarındadır."}
{k:"Spor",s:"Wushu hangi ülkenin geleneksel spor dalıdır?",o:["Japonya","Kore","Çin","Tayland"],d:2,a:"Wushu Çin in geleneksel dövüş sanatı ve sporudur."}
{k:"Spor",s:"Taekwondo hangi ülkenin dövüş sanatıdır?",o:["Japonya","Çin","Kore","Tayland"],d:2,a:"Taekwondo Güney Kore kökenli bir dövüş sanatıdır."}
{k:"Spor",s:"Karate hangi ülkede ortaya çıkmıştır?",o:["Çin","Kore","Japonya","Vietnam"],d:2,a:"Karate Japonya da özellikle Okinawa adasında ortaya çıkmıştır."}
{k:"Spor",s:"Muay Thai hangi ülkenin dövüş sanatıdır?",o:["Japonya","Çin","Vietnam","Tayland"],d:3,a:"Muay Thai Tayland ın geleneksel dövüş sanatıdır."}
{k:"Spor",s:"Hentbol maçı kaç dakikadır?",o:["40","50","60","70"],d:2,a:"Hentbol maçı 2x30 toplam 60 dakikadır."}
{k:"Spor",s:"Masa tenisi maçında bir seti kazanmak için kaç sayıya ulaşılmalıdır?",o:["9","11","15","21"],d:1,a:"Masa tenisinde seti kazanmak için 11 sayıya ulaşmak gerekir."}
{k:"Spor",s:"Sutopu maçı kaç periyottan oluşur?",o:["2","3","4","5"],d:2,a:"Sutopu maçı 4 periyottan oluşur."}
{k:"Matematik",s:"Bir prizmada kaç adet taban yüzeyi vardır?",o:["1","2","3","4"],d:1,a:"Prizmada 2 taban yüzeyi bulunur."}
{k:"Matematik",s:"Kesir türünde payda sıfır olabilir mi?",o:["Evet","Hayır","Bazen","Pozitifse evet"],d:1,a:"Payda hiçbir zaman sıfır olamaz tanımsız olur."}
{k:"Matematik",s:"1000 in yüzde 15 i kaçtır?",o:["100","150","200","250"],d:1,a:"1000 x 0.15 = 150 dir."}
{k:"Matematik",s:"Paralel kenarın alanı nasıl hesaplanır?",o:["a x b","taban x yükseklik","2(a+b)","pi r kare"],d:1,a:"Paralelkenarın alanı taban x yükseklik formülüyle hesaplanır."}
{k:"Matematik",s:"Yamuk nedir?",o:["4 kenarı eşit","Sadece bir çift kenarı paralel dörtgen","Tüm kenarları paralel","Üçgen"],d:1,a:"Yamuk sadece bir çift kenarı paralel olan dörtgendir."}
{k:"Matematik",s:"Ondalık sayı 0.75 kesir olarak nasıl yazılır?",o:["1/2","3/4","2/3","4/5"],d:1,a:"0.75 kesir olarak 3/4 tür."}
{k:"Matematik",s:"Bir çemberin yarıçapı 5 ise çevresi yaklaşık kaçtır?",o:["25","31.4","50","15.7"],d:1,a:"Çevre = 2 x pi x r = 2 x 3.14 x 5 = 31.4 tür."}
{k:"Matematik",s:"Kareköklerin hangi özelliği vardır?",o:["Negatif olamaz","Her zaman tam sayı","Sıfırdan küçük","Paydası sıfır"],d:0,a:"Reel sayılarda karekök negatif olamaz sonuç sıfır veya pozitiftir."}
{k:"Matematik",s:"Romen rakamıyla L kaçtır?",o:["10","50","100","500"],d:1,a:"Romen rakamıyla L 50 demektir."}
{k:"Matematik",s:"Romen rakamıyla C kaçtır?",o:["10","50","100","500"],d:2,a:"Romen rakamıyla C 100 demektir."}
{k:"Matematik",s:"Bir doğru parçasının kaç uç noktası vardır?",o:["0","1","2","Sonsuz"],d:2,a:"Doğru parçasının 2 uç noktası vardır."}
{k:"Matematik",s:"İki doğru birbirine dik ise aralarındaki açı kaç derecedir?",o:["45","60","90","180"],d:2,a:"Birbirine dik iki doğru arasında 90 derecelik açı vardır."}
{k:"Matematik",s:"Eşkenar üçgenin açıları kaçar derecedir?",o:["45","60","90","120"],d:1,a:"Eşkenar üçgenin her açısı 60 derecedir."}
{k:"Matematik",s:"Karenin köşegen sayısı kaçtır?",o:["1","2","4","6"],d:1,a:"Karenin 2 köşegeni vardır."}
{k:"Matematik",s:"Altıgenin kaç köşegeni vardır?",o:["6","9","12","15"],d:1,a:"Düzgün altıgenin 9 köşegeni vardır."}
{k:"Matematik",s:"Bir sayının negatif kuvveti ne anlama gelir?",o:["Sıfır olur","O sayının tersinin pozitif kuvveti","Tanımsız","Negatif sayı"],d:1,a:"Negatif kuvvet sayının tersinin pozitif kuvveti anlamına gelir."}
{k:"Matematik",s:"Ortalama nasıl hesaplanır?",o:["Toplam x sayı","Toplam / sayı adet","En büyük - en küçük","Ortanca değer"],d:1,a:"Ortalama tüm değerlerin toplamının değer sayısına bölünmesiyle bulunur."}
{k:"Matematik",s:"2 üzeri 10 kaç eder?",o:["512","1000","1024","2048"],d:2,a:"2 üzeri 10 = 1024 tür."}
{k:"Matematik",s:"Faktöriyel işareti nedir?",o:["#","!","@","&"],d:1,a:"Faktöriyel ünlem işareti ! ile gösterilir."}
{k:"Matematik",s:"5 faktöriyel kaçtır?",o:["60","100","120","150"],d:2,a:"5! = 5x4x3x2x1 = 120 dir."}
{k:"Matematik",s:"Koordinat düzleminde orijin noktası neresidir?",o:["(1,1)","(0,0)","(1,0)","(0,1)"],d:1,a:"Orijin noktası koordinat düzleminin merkezi olan (0,0) noktasıdır."}
{k:"Matematik",s:"Bir dik üçgende en uzun kenara ne denir?",o:["Kenar","Taban","Hipotenüs","Yükseklik"],d:2,a:"Dik üçgenin en uzun kenarına hipotenüs denir."}
{k:"Matematik",s:"Pisagor teoremi nedir?",o:["a+b=c","a kare + b kare = c kare","a x b = c","2a + 2b = c"],d:1,a:"Pisagor teoremine göre dik üçgende a kare + b kare = hipotenüs kare dir."}
{k:"Matematik",s:"Doğal sayılar sıfırdan başlar mı?",o:["Evet","Hayır","Bazen","Sadece pozitifler"],d:0,a:"Doğal sayılar 0 dan başlar: 0 1 2 3 4..."}
{k:"Matematik",s:"Rasyonel sayı nedir?",o:["Pi sayısı","Kesir olarak yazılabilen sayı","Kök 2","Sonsuz"],d:1,a:"Rasyonel sayılar a/b şeklinde yazılabilen sayılardır (b sıfırdan farklı)."}
{k:"Deyimler",s:"Son sözü söylemek ne demektir?",o:["Konuşmayı bitirmek","Kesin kararı vermek","Sessiz kalmak","Özür dilemek"],d:1,a:"Son sözü söylemek bir konuda kesin ve nihai kararı vermek demektir."}
{k:"Deyimler",s:"Çıkmaza girmek ne demektir?",o:["Dar yolda kalmak","Çözümsüz bir duruma düşmek","Kaybolmak","Yürümek"],d:1,a:"Bir sorunun çözümsüz hale gelmesi demektir."}
{k:"Deyimler",s:"Eli uzun olmak ne demektir?",o:["Uzun kolları olmak","Hırsızlık yapma eğiliminde olmak","Yardımsever olmak","Uzağa ulaşmak"],d:1,a:"Başkalarının eşyalarına el uzatmak hırsızlık eğilimi göstermek demektir."}
{k:"Deyimler",s:"Kalbi kırılmak ne anlama gelir?",o:["Kalp krizi","Çok üzülmek hayal kırıklığına uğramak","Korkuya kapılmak","Sevinmek"],d:1,a:"Birine kırgın olmak çok üzülmek demektir."}
{k:"Deyimler",s:"Pabucunu dama atmak ne demektir?",o:["Temizlik yapmak","Birinin yerini almak onu geçmek","Ayakkabı almak","Dans etmek"],d:1,a:"Birinin işinde kendinden üstün olmak onu geçmek demektir."}
{k:"Deyimler",s:"Dümeni kırmak ne demektir?",o:["Gemi sürmek","Yolunu değiştirmek planını bozmak","Dümeni tamir etmek","Yüzmek"],d:1,a:"Planını veya yönünü ani olarak değiştirmek demektir."}
{k:"Deyimler",s:"Maşa gibi kullanmak ne demektir?",o:["Yemek yapmak","Birini kendi çıkarı için alet etmek","Ateş yakmak","Temizlik yapmak"],d:1,a:"Birini kendi işlerini yaptırmak için alet olarak kullanmak demektir."}
{k:"Deyimler",s:"Yüzünü ekşitmek ne demektir?",o:["Limon yemek","Hoşnutsuzluğunu yüz ifadesiyle göstermek","Ağlamak","Gülmek"],d:1,a:"Memnuniyetsizliğini yüz ifadesiyle belli etmek demektir."}
{k:"Deyimler",s:"Gemi azıya almak ne demektir?",o:["Gemi kullanmak","Kontrol dışına çıkmak başına buyruk olmak","Yemek yemek","Denize açılmak"],d:1,a:"Kontrolden çıkmak kimsenin sözünü dinlememek demektir."}
{k:"Deyimler",s:"Yüzüne gülmek ne demektir?",o:["Mutlu olmak","İki yüzlü davranmak","Komik bulmak","Sevinmek"],d:1,a:"Yüzüne gülerken arkadan kötü konuşmak iki yüzlülük demektir."}
{k:"Deyimler",s:"Ağzını aramak ne demektir?",o:["Dişçiye gitmek","Birinden üstü kapalı bilgi almaya çalışmak","Yemek aramak","Konuşmak"],d:1,a:"Dolaylı sorularla birinden gizlice bilgi almaya çalışmak demektir."}
{k:"Deyimler",s:"Taban tabana zıt olmak ne demektir?",o:["Ayakkabı giymek","Tamamen birbirine aykırı olmak","Yürümek","Aynı olmak"],d:1,a:"İki şeyin birbirine tamamen zıt ve uyumsuz olması demektir."}
{k:"Deyimler",s:"Gözü yüksekte olmak ne demektir?",o:["Yüksekten korkmak","Hep daha iyisini istemek","Gözlük takmak","Uzağı görmek"],d:1,a:"Her zaman daha iyisini daha yükseğini istemek demektir."}
{k:"Deyimler",s:"İpin ucunu kaçırmak ne demektir?",o:["İp koparmak","Kontrolü kaybetmek","İp atlamak","Düğüm atmak"],d:1,a:"Bir işin veya durumun kontrolünü kaybetmek demektir."}
{k:"Deyimler",s:"Can havliyle ne demektir?",o:["Sakin olmak","Büyük korku veya panikle","Mutlulukla","Heyecanla"],d:1,a:"Ölüm korkusuyla büyük bir panikle hareket etmek demektir."}
{k:"Deyimler",s:"Balık kavağa çıkınca ne demektir?",o:["Balık tutmak","Olmayacak bir zaman asla","Ağaç tırmanmak","Çok beklemek"],d:1,a:"Asla gerçekleşmeyecek bir zaman dilimini ifade eder."}
{k:"Deyimler",s:"Daldan dala konmak ne demektir?",o:["Kuş olmak","Sürekli konu değiştirmek","Ağaçlara tırmanmak","Gezmek"],d:1,a:"Konuşurken sürekli konu değiştirmek bir konuda karar kılamamak demektir."}
{k:"Deyimler",s:"Elinin hamuru ile erkek işine karışmak ne anlama gelir?",o:["Yemek yapmak","Bilmediği işe karışmak","Hamur yoğurmak","Yardım etmek"],d:1,a:"Bilmediği bir konuya karışmak yetkinliği olmayan işlere burnunu sokmak demektir."}
{k:"Deyimler",s:"Çorap söküğü gibi gitmek ne demektir?",o:["Çorap yırtılmak","Bir şeyin peş peşe devam etmesi","Alışveriş yapmak","Koşmak"],d:1,a:"Bir işin veya olayın zincirleme şekilde birbirini izlemesi demektir."}
{k:"Deyimler",s:"Pabuç bırakmamak ne demektir?",o:["Ayakkabı almak","Boyun eğmemek teslim olmamak","Koşmak","Kaçmak"],d:1,a:"Hiçbir zorluk karşısında boyun eğmemek teslim olmamak demektir."}
{k:"Deyimler",s:"Sinek avlamak ne demektir?",o:["Böcek yakalamak","Boş oturmak işsiz olmak","Temizlik yapmak","Spor yapmak"],d:1,a:"Hiçbir iş yapmadan boş oturmak demektir."}
{k:"Deyimler",s:"Göz yummak ne demektir?",o:["Uyumak","Bir hatayı görmezden gelmek","Göz kapamak","Karanlık"],d:1,a:"Bir hatayı veya yanlışı bilerek görmezden gelmek demektir."}
{k:"Deyimler",s:"Burun kıvırmak ne demektir?",o:["Hapşırmak","Beğenmemek küçümsemek","Koku almak","Aksırmak"],d:1,a:"Bir şeyi beğenmeyip küçümsemek demektir."}
{k:"Deyimler",s:"Yelkenleri suya indirmek ne demektir?",o:["Denize açılmak","Pes etmek boyun eğmek","Yüzmek","Gemi yapmak"],d:1,a:"Pes etmek karşısındakinin gücünü kabul edip boyun eğmek demektir."}
{k:"Deyimler",s:"Ağzına bir parmak bal çalmak ne demektir?",o:["Bal yemek","Küçük bir iyilikle birini oyalamak","Tatlı yapmak","Diş fırçalamak"],d:1,a:"Küçük bir iyilik veya söz vererek birini geçici olarak memnun etmek ve oyalamak demektir."}
{k:"Atasözleri",s:"Bir mum diğer mumu tutuşturmakla ışığından kaybetmez ne anlatır?",o:["Mum yakmak","Paylaşmak seni eksiltmez","Yangın söndürmek","Aydınlatma"],d:1,a:"Bilgini veya iyiliğini paylaşmak seni eksiltmez aksine çoğaltır."}
{k:"Atasözleri",s:"İnsan yedisinde ne ise yetmişinde de odur ne demektir?",o:["Yaşlanmak","Karakter küçük yaşta oluşur","Sağlık","Spor yapmak"],d:1,a:"İnsanın temel karakteri küçük yaşta şekillenir ve ömür boyu değişmez."}
{k:"Atasözleri",s:"Çalma kapıyı çalarlar kapını ne anlatır?",o:["Kapı çalmak","Kötülük yapana kötülük yapılır","Zil çalmak","Hırsızlık"],d:1,a:"Başkasına kötülük yapan kişi bir gün aynı kötülükle karşılaşır."}
{k:"Atasözleri",s:"Dost acı söyler ne demektir?",o:["Kötü konuşmak","Gerçek dost doğruyu söyler","Tartışmak","Kavga etmek"],d:1,a:"Gerçek dost hoşuna gitmese bile doğruyu söyler."}
{k:"Atasözleri",s:"Su uyur düşman uyumaz ne anlatır?",o:["Uykusuzluk","Düşmanına karşı her zaman uyanık ol","Su kaynatmak","Gece nöbeti"],d:1,a:"Düşmanın her zaman tetikte olduğunu sende uyanık olmalısın."}
{k:"Atasözleri",s:"Ağlamayan çocuğa meme vermezler ne demektir?",o:["Bebek bakımı","İstediğini söylemezsen alamazsın","Ağlamak","Doktor olmak"],d:1,a:"İhtiyacını ve istediğini dile getirmezsen kimse yardım etmez."}
{k:"Atasözleri",s:"Aşağı tükürsem sakal yukarı tükürsem bıyık ne anlatır?",o:["Temizlik","İki seçenek de kötü çıkmaz durum","Berber olmak","Tıraş olmak"],d:1,a:"Her iki seçeneğin de kötü olduğu çıkmaz durumu ifade eder."}
{k:"Atasözleri",s:"Dikensiz gül olmaz ne demektir?",o:["Gül yetiştirmek","Her güzel şeyin bir zorluğu vardır","Bahçe bakmak","Çiçek almak"],d:1,a:"Her güzel şeyin yanında bir zorluk veya sıkıntı da vardır."}
{k:"Atasözleri",s:"Gün doğmadan neler doğar ne anlatır?",o:["Sabah erken kalkmak","Beklenmedik olaylar olabilir","Doğum","Güneşi izlemek"],d:1,a:"Her an beklenmedik olumlu veya olumsuz gelişmeler olabilir."}
{k:"Atasözleri",s:"Hamama giren terler ne demektir?",o:["Temizlik","İşe girişen zorluğuna katlanır","Saunaya gitmek","Spor yapmak"],d:1,a:"Bir işe girişen kişi o işin zorluklarına da katlanmalıdır."}
{k:"Atasözleri",s:"Kaz gelecek yerden tavuk esirgenmez ne anlatır?",o:["Tavuk beslemek","Büyük kazanç için küçük harcama yapılır","Kaz avlamak","Market alışverişi"],d:1,a:"Büyük kazanç elde etmek için küçük fedakarlıklar yapmak gerekir."}
{k:"Atasözleri",s:"Sel gider kum kalır ne demektir?",o:["Sel felaketi","Geçici olaylar gider kalıcı sonuçlar kalır","Kum oyunu","Çöl oluşumu"],d:1,a:"Olaylar geçicidir ama bıraktığı izler ve sonuçlar kalıcıdır."}
{k:"Atasözleri",s:"Yalancının mumu yatsıya kadar yanar ne anlatır?",o:["Mum yakmak","Yalan er geç ortaya çıkar","Gece lambaları","Elektrik kesintisi"],d:1,a:"Yalancı bir süre idare edebilir ama sonunda yalanı ortaya çıkar."}
{k:"Atasözleri",s:"Ateş düştüğü yeri yakar ne demektir?",o:["Yangın söndürmek","Felaket en çok yaşayanı etkiler","Ateş yakmak","Soba kurmak"],d:1,a:"Bir felaket veya sıkıntı en çok onu yaşayan kişiyi etkiler."}
{k:"Atasözleri",s:"Dolu küpten ses çıkmaz ne anlatır?",o:["Küp doldurmak","Bilgili ve olgun insan sessizdir","Müzik yapmak","Depolama"],d:1,a:"Gerçekten bilgili ve olgun insan gereksiz gürültü yapmaz."}
{k:"Atasözleri",s:"Herkesin bir bildiği vardır ne demektir?",o:["Herkes bilgili","Her insanın farklı bilgi ve tecrübesi vardır","Okula gitmek","Ders çalışmak"],d:1,a:"Her insanın kendine göre bir bilgisi ve tecrübesi vardır küçümsenmemeli."}
{k:"Atasözleri",s:"Kervan yolda düzülür ne anlatır?",o:["Kervan sürmek","İşler yapılırken düzene girer","Yol yapmak","Seyahat etmek"],d:1,a:"Bir işe başlanıp yolda sorunlar çözülerek düzene sokulur."}
{k:"Atasözleri",s:"Meyve veren ağaç taşlanır ne demektir?",o:["Meyve toplamak","Başarılı insan kıskançlık ve saldırıya uğrar","Taş atmak","Ağaç dikmek"],d:1,a:"Başarılı ve üretken insanlar her zaman eleştiri ve kıskançlığa hedef olur."}
{k:"Atasözleri",s:"Gülü seven dikenine katlanır ne anlatır?",o:["Gül yetiştirmek","Sevdiğinin zorluklarına katlanırsın","Çiçek almak","Bahçe işi"],d:1,a:"Bir şeyi veya birini gerçekten seviyorsan zorluklarına da katlanmalısın."}
{k:"Atasözleri",s:"Taşıma suyla değirmen dönmez ne demektir?",o:["Su taşımak","Dışarıdan destekle sürdürülen iş kalıcı olmaz","Değirmen yapmak","Su bulmak"],d:1,a:"Kendi kaynağı olmayan dışarıdan destekle sürdürülen iş kalıcı olmaz."}
{k:"Atasözleri",s:"Kardeş kardeşi bıçaklar sofrada barışır ne anlatır?",o:["Kavga etmek","Aile bağları güçlüdür küslük sürmez","Yemek yemek","Bıçak kullanmak"],d:1,a:"Aile içi küsler uzun sürmez çünkü aile bağları güçlüdür."}
{k:"Atasözleri",s:"Aç ayı oynamaz ne demektir?",o:["Hayvanat bahçesi","Karşılığı olmayan iş için kimse çaba göstermez","Ayı beslemek","Sirk gösterisi"],d:1,a:"Karşılığını görmeden kimse emek harcamak istemez."}
{k:"Atasözleri",s:"Lafla peynir gemisi yürümez ne anlatır?",o:["Gemi kullanmak","Sadece konuşmayla iş olmaz eylem lazım","Peynir yapmak","Denizcilik"],d:1,a:"Sadece konuşarak iş yapılmaz harekete geçmek gerekir."}
{k:"Atasözleri",s:"Yarım doktor candan yarım hoca dinden eder ne demektir?",o:["Doktor olmak","Yarım bilgi tehlikelidir","Okula gitmek","Ders çalışmak"],d:1,a:"Eksik ve yarım bilgi tam bilmemekten daha tehlikelidir."}
{k:"Atasözleri",s:"Davulun sesi uzaktan hoş gelir ne anlatır?",o:["Müzik dinlemek","Uzaktan güzel görünen şey yakından öyle olmayabilir","Davul çalmak","Konser"],d:1,a:"Uzaktan güzel ve çekici görünen her şey yakınından bakıldığında öyle olmayabilir."}
"""

_BY_QUESTIONS_LISE = r"""
{k:"Tarih",s:"Vestfalya Barışı hangi yılda imzalandı?",o:["1618","1648","1713","1789"],d:1,a:"Vestfalya Barışı 1648 de imzalanmış ve modern devletler sistemini kurmuştur."}
{k:"Tarih",s:"Rönesans hangi ülkede başlamıştır?",o:["Fransa","İngiltere","İtalya","Almanya"],d:2,a:"Rönesans 14. yüzyılda İtalya da başlamıştır."}
{k:"Tarih",s:"Magna Carta hangi yılda imzalanmıştır?",o:["1066","1215","1453","1789"],d:1,a:"Magna Carta 1215 yılında İngiltere de imzalanmıştır."}
{k:"Tarih",s:"Amerikan Bağımsızlık Bildirgesi hangi yıl ilan edildi?",o:["1763","1776","1789","1812"],d:1,a:"Amerikan Bağımsızlık Bildirgesi 4 Temmuz 1776 da ilan edilmiştir."}
{k:"Tarih",s:"Bolşevik Devrimi hangi yılda gerçekleşti?",o:["1905","1914","1917","1922"],d:2,a:"Bolşevik Devrimi Ekim 1917 de Rusya da gerçekleşmiştir."}
{k:"Tarih",s:"Birleşmiş Milletler hangi yılda kuruldu?",o:["1919","1939","1945","1950"],d:2,a:"Birleşmiş Milletler 1945 yılında kurulmuştur."}
{k:"Tarih",s:"NATO hangi yılda kuruldu?",o:["1945","1947","1949","1955"],d:2,a:"NATO (Kuzey Atlantik Antlaşması Örgütü) 1949 yılında kurulmuştur."}
{k:"Tarih",s:"Berlin Duvarı hangi yılda yıkıldı?",o:["1985","1987","1989","1991"],d:2,a:"Berlin Duvarı 9 Kasım 1989 da yıkılmıştır."}
{k:"Tarih",s:"Osmanlı Devletinde ilk anayasa hangi dönemde hazırlandı?",o:["Tanzimat","I. Meşrutiyet","II. Meşrutiyet","Cumhuriyet"],d:1,a:"İlk anayasa Kanun-i Esasi 1876 I. Meşrutiyet döneminde hazırlanmıştır."}
{k:"Tarih",s:"Türkiye hangi yılda NATO ya katıldı?",o:["1949","1950","1952","1955"],d:2,a:"Türkiye 1952 yılında NATO ya katılmıştır."}
{k:"Tarih",s:"Lale Devri hangi yüzyılda yaşanmıştır?",o:["16. yy","17. yy","18. yy","19. yy"],d:2,a:"Lale Devri 18. yüzyılda 1718-1730 yılları arasında yaşanmıştır."}
{k:"Tarih",s:"Yavuz Sultan Selim hangi savaşla Mısırı fethetti?",o:["Çaldıran","Ridaniye","Preveze","Mohaç"],d:1,a:"Yavuz Sultan Selim 1517 Ridaniye Savaşı ile Mısırı fethetti."}
{k:"Tarih",s:"İttihat ve Terakki Cemiyeti hangi olayla iktidara geldi?",o:["31 Mart","II. Meşrutiyet","Balkan Savaşları","I. Dünya Savaşı"],d:1,a:"İttihat ve Terakki 1908 II. Meşrutiyet ilanıyla iktidara gelmiştir."}
{k:"Tarih",s:"Waterloo Savaşı kim yenilmiştir?",o:["İngiltere","Prusya","Napolyon","Rusya"],d:2,a:"Napolyon 1815 Waterloo Savaşında yenilerek sürgüne gönderilmiştir."}
{k:"Tarih",s:"Endüstri Devriminde buhar makinesini kim geliştirdi?",o:["Edison","Newton","James Watt","Tesla"],d:2,a:"James Watt buhar makinesini geliştirerek Endüstri Devrimine katkı sağlamıştır."}
{k:"Tarih",s:"Düyun-u Umumiye ne demektir?",o:["Meclis","Borç idaresi","Ordu","Mahkeme"],d:1,a:"Düyun-u Umumiye Osmanlı dış borçlarını yönetmek için kurulan idaredir."}
{k:"Tarih",s:"Mudros Ateşkesinden sonra hangi antlaşma dayatıldı?",o:["Lozan","Sevr","Ankara","Kars"],d:1,a:"Sevr Antlaşması Osmanlıya dayatılmış ancak TBMM kabul etmemiştir."}
{k:"Tarih",s:"Tekalif-i Milliye emirleri ne amaçla çıkarıldı?",o:["Eğitim","Savaş ihtiyaçlarını karşılamak","Ticaret","Tarım"],d:1,a:"Tekalif-i Milliye emirleri Kurtuluş Savaşı için kaynak toplamak amacıyla çıkarılmıştır."}
{k:"Tarih",s:"Avrupa Birliği hangi antlaşmayla kuruldu?",o:["Roma","Paris","Maastricht","Lizbon"],d:2,a:"Avrupa Birliği 1992 Maastricht Antlaşması ile kurulmuştur."}
{k:"Tarih",s:"Osmanlıda devşirme sistemi nedir?",o:["Vergi sistemi","Hristiyan çocukların askere alınması","Ticaret sistemi","Eğitim sistemi"],d:1,a:"Devşirme sistemi Hristiyan ailelerden çocuk alınarak Osmanlı ordusuna kazandırılmasıdır."}
{k:"Tarih",s:"Marshall Planı hangi ülke tarafından uygulandı?",o:["SSCB","İngiltere","ABD","Fransa"],d:2,a:"Marshall Planı II. Dünya Savaşı sonrası Avrupa yı yeniden inşa etmek için ABD tarafından uygulandı."}
{k:"Tarih",s:"Piri Reis Haritası hangi yüzyılda çizildi?",o:["14. yy","15. yy","16. yy","17. yy"],d:2,a:"Piri Reis Haritası 1513 yılında 16. yüzyılda çizilmiştir."}
{k:"Tarih",s:"Kurtuluş Savaşının ilk askeri zafer hangisidir?",o:["Sakarya","İnönü","Dumlupınar","Başkomutanlık"],d:1,a:"I. İnönü Muharebesi (1921) Kurtuluş Savaşının ilk askeri zaferidir."}
{k:"Tarih",s:"Atatürk ilkelerinden hangisi ekonomi politikasını belirler?",o:["Halkçılık","Devletçilik","Laiklik","Milliyetçilik"],d:1,a:"Devletçilik ilkesi ekonomi politikasını belirler."}
{k:"Tarih",s:"Tanzimat Fermanının en önemli yeniliği nedir?",o:["Matbaa","Can ve mal güvenliği","Meclis","Cumhuriyet"],d:1,a:"Tanzimat Fermanı ile tüm vatandaşlara can ve mal güvencesi sağlanmıştır."}
{k:"Tarih",s:"Türk Tarih Kurumu hangi yılda kuruldu?",o:["1928","1931","1934","1938"],d:1,a:"Türk Tarih Kurumu 1931 yılında kurulmuştur."}
{k:"Tarih",s:"Türk Dil Kurumu hangi yılda kuruldu?",o:["1928","1930","1932","1935"],d:2,a:"Türk Dil Kurumu 1932 yılında kurulmuştur."}
{k:"Tarih",s:"Kabotaj Kanunu hangi yılda kabul edildi?",o:["1924","1926","1928","1930"],d:1,a:"Kabotaj Kanunu 1 Temmuz 1926 da kabul edilerek deniz ticareti Türklere verilmiştir."}
{k:"Tarih",s:"Soğuk Savaşta Varşova Paktı hangi yılda kuruldu?",o:["1949","1951","1955","1961"],d:2,a:"Varşova Paktı 1955 yılında SSCB liderliğinde kurulmuştur."}
{k:"Tarih",s:"Kıbrıs Barış Harekatı hangi yılda yapıldı?",o:["1960","1964","1974","1983"],d:2,a:"Kıbrıs Barış Harekatı 20 Temmuz 1974 te gerçekleştirilmiştir."}
{k:"Tarih",s:"Osmanlıda Islahat Fermanı hangi yılda ilan edildi?",o:["1839","1856","1876","1908"],d:1,a:"Islahat Fermanı 1856 yılında ilan edilmiştir."}
{k:"Tarih",s:"Hz. Muhammed hangi yılda Hicret etmiştir?",o:["610","622","630","632"],d:1,a:"Hicret 622 yılında Mekke den Medine ye göçtür."}
{k:"Tarih",s:"Haçlı Seferleri kaç yüzyıl sürmüştür?",o:["1","2","3","4"],d:1,a:"Haçlı Seferleri 11.-13. yüzyıllar arasında yaklaşık 2 yüzyıl sürmüştür."}
{k:"Tarih",s:"Matbaayı Osmanlıya kim getirmiştir?",o:["Mimar Sinan","İbrahim Müteferrika","Evliya Çelebi","Katip Çelebi"],d:1,a:"İbrahim Müteferrika 1727 de Osmanlıda ilk matbaayı kurmuştur."}
{k:"Tarih",s:"30 Yıl Savaşları hangi kıtada yaşanmıştır?",o:["Asya","Afrika","Avrupa","Amerika"],d:2,a:"30 Yıl Savaşları 1618-1648 arasında Avrupa da yaşanmıştır."}
{k:"Tarih",s:"Sanayi Devrimi ile ortaya çıkan sınıf hangisidir?",o:["Aristokrasi","Burjuvazi ve işçi sınıfı","Ruhban sınıfı","Köylü sınıfı"],d:1,a:"Sanayi Devrimi ile burjuvazi güçlenmiş ve işçi sınıfı ortaya çıkmıştır."}
{k:"Tarih",s:"Truman Doktrini hangi yılda ilan edildi?",o:["1945","1947","1949","1950"],d:1,a:"Truman Doktrini 1947 de komünizme karşı ABD nin yardım politikasıdır."}
{k:"Tarih",s:"İnsan Hakları Evrensel Beyannamesi hangi yılda kabul edildi?",o:["1945","1948","1950","1960"],d:1,a:"İnsan Hakları Evrensel Beyannamesi 10 Aralık 1948 de BM tarafından kabul edilmiştir."}
{k:"Tarih",s:"Türkiye de çok partili hayata ne zaman geçildi?",o:["1923","1930","1946","1950"],d:2,a:"Türkiye de çok partili hayata fiilen 1946 yılında geçilmiştir."}
{k:"Tarih",s:"Demokrat Parti hangi yılda iktidara geldi?",o:["1946","1948","1950","1952"],d:2,a:"Demokrat Parti 14 Mayıs 1950 seçimleriyle iktidara gelmiştir."}
{k:"Tarih",s:"Çaldıran Savaşı hangi yılda yapıldı?",o:["1453","1514","1526","1538"],d:1,a:"Çaldıran Savaşı 1514 yılında Osmanlı ile Safeviler arasında yapılmıştır."}
{k:"Tarih",s:"Avrupa Konseyi hangi yılda kuruldu?",o:["1945","1947","1949","1951"],d:2,a:"Avrupa Konseyi 1949 yılında kurulmuş, Türkiye kurucu üyedir."}
{k:"Tarih",s:"Balkan Savaşları hangi yıllar arasında yapıldı?",o:["1908-1910","1912-1913","1914-1918","1919-1922"],d:1,a:"Balkan Savaşları 1912-1913 yılları arasında yapılmıştır."}
{k:"Tarih",s:"Osmanlı padişahlarından hangisi en uzun süre tahtta kalmıştır?",o:["Fatih","Yavuz","Kanuni","II. Abdülhamid"],d:2,a:"Kanuni Sultan Süleyman 46 yıl ile en uzun süre tahtta kalan padişahtır."}
{k:"Coğrafya",s:"Tektonik plaka hareketleri ne oluşturur?",o:["Rüzgar","Deprem ve volkan","Yağmur","Gel-git"],d:1,a:"Tektonik plaka hareketleri deprem volkanik aktivite ve dağ oluşumuna neden olur."}
{k:"Coğrafya",s:"Coriolis etkisi nedir?",o:["Depremlerin sebebi","Dünya dönüşünün rüzgar ve akıntıları saptırması","Volkanik etki","Gel-git olayı"],d:1,a:"Coriolis etkisi Dünya nın dönüşünden kaynaklanan rüzgar ve akıntıların sapmasıdır."}
{k:"Coğrafya",s:"Fay hattı nedir?",o:["Dağ zirvesi","Yer kabuğundaki kırık hattı","Nehir yatağı","Okyanus dibi"],d:1,a:"Fay hattı yer kabuğundaki tektonik plakaların birleştiği kırık hattıdır."}
{k:"Coğrafya",s:"El Nino etkisi nedir?",o:["Deprem","Pasifik de deniz suyu sıcaklık artışı","Volkanik patlama","Tsunami"],d:1,a:"El Nino Pasifik Okyanusundaki anormal deniz suyu ısınmasıdır."}
{k:"Coğrafya",s:"Orojenez ne demektir?",o:["Deprem oluşumu","Dağ oluşumu","Kıta kayması","Volkanik patlama"],d:1,a:"Orojenez tektonik kuvvetlerle dağ oluşumu sürecidir."}
{k:"Coğrafya",s:"Karst topoğrafyası hangi kayaçta gelişir?",o:["Granit","Bazalt","Kireçtaşı","Kumtaşı"],d:2,a:"Karst topoğrafyası kireçtaşının çözünmesiyle gelişir."}
{k:"Coğrafya",s:"Rift vadisi nasıl oluşur?",o:["Aşınmayla","Tektonik plakaların birbirinden uzaklaşmasıyla","Volkanla","Buzul erozyonuyla"],d:1,a:"Rift vadisi tektonik plakaların birbirinden uzaklaşmasıyla oluşur."}
{k:"Coğrafya",s:"Dünya nın en derin noktası neresidir?",o:["Grand Kanyon","Mariana Çukuru","Baykal Gölü","Kola Kuyusu"],d:1,a:"Mariana Çukuru yaklaşık 11000 m ile dünyanın en derin noktasıdır."}
{k:"Coğrafya",s:"Jet akımı nedir?",o:["Uçak rotası","Atmosferin üst katmanlarındaki hızlı hava akımı","Okyanus akıntısı","Volkanik gaz"],d:1,a:"Jet akımı troposferin üst kısmında esen çok hızlı hava akımıdır."}
{k:"Coğrafya",s:"Monoson ikliminin en belirgin özelliği nedir?",o:["Sürekli kurak","Mevsimsel rüzgar değişimi ve yoğun yağış","Soğuk kış","Ilıman yaz"],d:1,a:"Muson ikliminde mevsimsel rüzgar değişimi ve yoğun yağış dönemleri karakteristiktir."}
{k:"Coğrafya",s:"GAP hangi nehirler üzerinde kurulmuştur?",o:["Kızılırmak-Sakarya","Fırat-Dicle","Seyhan-Ceyhan","Meriç-Ergene"],d:1,a:"GAP (Güneydoğu Anadolu Projesi) Fırat ve Dicle nehirleri üzerine kurulmuştur."}
{k:"Coğrafya",s:"Moren ne demektir?",o:["Volkanik kayaç","Buzulun taşıdığı malzeme birikintisi","Kum tepesi","Akarsu yatağı"],d:1,a:"Moren buzulların taşıyıp biriktirdiği kaya ve toprak yığınıdır."}
{k:"Coğrafya",s:"İzostazi kavramı neyi açıklar?",o:["Hava basıncı","Yer kabuğunun denge durumu","Okyanus akıntıları","Rüzgar oluşumu"],d:1,a:"İzostazi yer kabuğunun manto üzerinde denge durumunda bulunmasıdır."}
{k:"Coğrafya",s:"Meridyen boylam farkı neyi etkiler?",o:["Mevsimler","Saat farkı","Yağış","Sıcaklık"],d:1,a:"Meridyenler arası 15 derecelik fark 1 saatlik saat farkına karşılık gelir."}
{k:"Coğrafya",s:"Türkiye de en çok deprem yaşanan fay hangisidir?",o:["Doğu Anadolu","Kuzey Anadolu","Batı Anadolu","Güneydoğu"],d:1,a:"Kuzey Anadolu Fay Hattı Türkiye nin en aktif ve tehlikeli fay hattıdır."}
{k:"Coğrafya",s:"Taiga biyomu nerelerde bulunur?",o:["Tropiklerde","Kuzeyde iğne yapraklı orman kuşağı","Çöllerde","Kutuplarda"],d:1,a:"Taiga kuzeyin soğuk bölgelerinde bulunan iğne yapraklı orman biyomudur."}
{k:"Coğrafya",s:"Çöl ortamında hangi fiziksel ayrışma daha yaygındır?",o:["Kimyasal","Biyolojik","Termal (sıcaklık farkı)","Buzul"],d:2,a:"Çöllerde gece-gündüz sıcaklık farkı nedeniyle termal ayrışma yaygındır."}
{k:"Coğrafya",s:"Heyelan en çok hangi koşullarda oluşur?",o:["Kurak arazide","Eğimli arazide yoğun yağış sonrası","Düz ovada","Çöl ortamında"],d:1,a:"Heyelan genellikle eğimli arazilerde yoğun yağış sonrası toprak kaymasıyla oluşur."}
{k:"Coğrafya",s:"Stratosferde bulunan koruyucu tabaka hangisidir?",o:["Troposfer","Ozon tabakası","Mezosfer","Termosfer"],d:1,a:"Ozon tabakası stratosferde bulunur ve zararlı UV ışınlarını süzer."}
{k:"Coğrafya",s:"Batı Karadeniz in en önemli ekonomik faaliyeti nedir?",o:["Tarım","Madencilik","Turizm","Hayvancılık"],d:1,a:"Batı Karadeniz de Zonguldak bölgesinde taşkömürü madenciliği önemli ekonomik faaliyettir."}
{k:"Coğrafya",s:"Tünel vadisi nasıl oluşur?",o:["Volkanla","Akarsu erozyonuyla","Rüzgarla","Buzulla"],d:1,a:"Tünel vadisi genellikle akarsuyun kayalık arazi içinden geçmesiyle oluşur."}
{k:"Coğrafya",s:"Epirojenez ne demektir?",o:["Dağ oluşumu","Kıta oluşumu (yükselme-alçalma)","Deprem","Volkan"],d:1,a:"Epirojenez geniş alanları etkileyen yavaş yükselme ve alçalma hareketleridir."}
{k:"Coğrafya",s:"Litosfer nedir?",o:["Atmosferin alt katmanı","Yer kabuğu ve üst manto","Okyanus tabanı","Volkanik bölge"],d:1,a:"Litosfer yer kabuğu ve üst mantonun katı kısmından oluşan katmandır."}
{k:"Coğrafya",s:"Enlem sıcaklığı nasıl etkiler?",o:["Etkilemez","Enlem arttıkça sıcaklık azalır","Enlem arttıkça sıcaklık artar","Sadece yağışı etkiler"],d:1,a:"Ekvatorda en yüksek sıcaklık vardır kutuplara gidildikçe sıcaklık azalır."}
{k:"Coğrafya",s:"Konveksiyonel yağış nasıl oluşur?",o:["Dağa çarparak","Cephe ile","Yüzeyin ısınmasıyla havanın yükselmesi","Rüzgarla"],d:2,a:"Konveksiyonel yağış yüzeyin aşırı ısınmasıyla havanın yükselmesi sonucu oluşur."}
{k:"Coğrafya",s:"Astenosfer nedir?",o:["Atmosfer katmanı","Mantonun akışkan üst kısmı","Yer çekirdeği","Okyanus tabanı"],d:1,a:"Astenosfer mantonun yarı akışkan kısmıdır litosfer plakaları üzerinde hareket eder."}
{k:"Bilim",s:"Avogadro sayısı yaklaşık kaçtır?",o:["3.14 x 10^8","6.02 x 10^23","9.81","1.6 x 10^-19"],d:1,a:"Avogadro sayısı yaklaşık 6.02 x 10^23 tür ve 1 moldeki tanecik sayısını ifade eder."}
{k:"Bilim",s:"Heisenberg belirsizlik ilkesi neyi ifade eder?",o:["Enerji korunumu","Konum ve momentum aynı anda kesin ölçülemez","Işık hızı sabittir","Kütle enerji eşdeğerliği"],d:1,a:"Heisenberg ilkesi bir parçacığın konumu ve momentumunun aynı anda kesin ölçülemeyeceğini belirtir."}
{k:"Bilim",s:"RNA nın DNA dan farkı nedir?",o:["Çift sarmal","Tek sarmallı ve riboz şekeri içerir","Daha büyük","Proteindir"],d:1,a:"RNA tek sarmallı yapıdadır ve deoksiriboz yerine riboz şekeri içerir."}
{k:"Bilim",s:"Entropi ne demektir?",o:["Enerji birimi","Düzensizlik ölçüsü","Basınç birimi","Kuvvet türü"],d:1,a:"Entropi termodinamikte düzensizliğin ölçüsüdür."}
{k:"Bilim",s:"Kara delik nedir?",o:["Uzay boşluğu","Çekim kuvveti ışığın bile kaçamadığı bölge","Yıldız patlaması","Gezegen"],d:1,a:"Kara delik çekim kuvveti o kadar güçlü olan bölgedir ki ışık bile kaçamaz."}
{k:"Bilim",s:"Ohm kanunu nedir?",o:["F=ma","V=IR","E=mc2","PV=nRT"],d:1,a:"Ohm kanunu gerilim = akım x direnç yani V=IR formülüyle ifade edilir."}
{k:"Bilim",s:"Kromozom sayısı insanda kaçtır?",o:["23","44","46","48"],d:2,a:"İnsanda 46 kromozom (23 çift) bulunur."}
{k:"Bilim",s:"Periyodik tabloda soy gazlar hangi gruptadır?",o:["1. grup","7. grup","8A grubu","Geçiş metalleri"],d:2,a:"Soy gazlar periyodik tablonun 8A (18.) grubundadır."}
{k:"Bilim",s:"Fotoelektrik olay nedir?",o:["Fotoğrafçılık","Işığın metalden elektron koparması","Elektrik üretimi","Lens oluşumu"],d:1,a:"Fotoelektrik olay ışığın metal yüzeye çarparak elektron koparmasıdır."}
{k:"Bilim",s:"Mitoz bölünme sonucunda kaç hücre oluşur?",o:["1","2","4","8"],d:1,a:"Mitoz bölünme sonucunda genetik olarak özdeş 2 hücre oluşur."}
{k:"Bilim",s:"Mayoz bölünme sonucunda kaç hücre oluşur?",o:["1","2","4","8"],d:2,a:"Mayoz bölünme sonucunda 4 haploid hücre oluşur."}
{k:"Bilim",s:"Standart basınç kaç atmosferdir?",o:["0.5","1","2","10"],d:1,a:"Standart basınç 1 atmosfer yani 101325 Pascal dir."}
{k:"Bilim",s:"Doppler etkisi neyi açıklar?",o:["Işık hızı","Ses kaynağı hareket edince frekans değişimi","Çekim kuvveti","Manyetik alan"],d:1,a:"Doppler etkisi ses veya ışık kaynağı hareket ederken gözlemciye göre frekans değişimini açıklar."}
{k:"Bilim",s:"Elektromanyetik spektrumda en kısa dalga boylu ışın hangisidir?",o:["Radyo dalgası","Kızılötesi","Mor ötesi","Gama ışını"],d:3,a:"Gama ışınları elektromanyetik spektrumda en kısa dalga boyuna sahiptir."}
{k:"Bilim",s:"Mendel in birinci yasası nedir?",o:["Bağımsız dağılım","Ayrışma (segregasyon)","Dominant gen","Mutasyon"],d:1,a:"Mendel in birinci yasası alellerin gamet oluşumunda birbirinden ayrılmasıdır."}
{k:"Bilim",s:"Joule neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:2,a:"Joule SI birim sisteminde enerjinin birimidir."}
{k:"Bilim",s:"Watt neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:1,a:"Watt güç (birim zamanda yapılan iş) birimidir."}
{k:"Bilim",s:"Pascal neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:3,a:"Pascal basınç birimidir."}
{k:"Bilim",s:"Katalizör ne yapar?",o:["Tepkimeyi durdurur","Tepkime hızını değiştirir kendisi değişmez","Tepkimeye katılır","Ürün oluşturur"],d:1,a:"Katalizör kimyasal tepkime hızını değiştirir ancak kendisi tepkimede tüketilmez."}
{k:"Bilim",s:"Hubble Yasası neyi ifade eder?",o:["Gezegenler","Evrenin genişlediğini","Atom yapısı","Genetik"],d:1,a:"Hubble Yasası galaksilerin bizden uzaklaştığını yani evrenin genişlediğini gösterir."}
{k:"Bilim",s:"Nötron yıldızı nasıl oluşur?",o:["Güneşten","Büyük yıldızın çökmesiyle","Gezegenlerden","Kara delikten"],d:1,a:"Nötron yıldızı süpernova patlamasından sonra büyük bir yıldızın çekirdeğinin çökmesiyle oluşur."}
{k:"Bilim",s:"Enzimler ne tür moleküllerdir?",o:["Karbonhidrat","Lipid","Protein","Nükleik asit"],d:2,a:"Enzimler biyolojik katalizör görevi gören protein molekülleridir."}
{k:"Bilim",s:"Endotermik tepkime ne demektir?",o:["Isı veren","Isı alan","Nötr","Gaz çıkaran"],d:1,a:"Endotermik tepkime çevreden ısı alan tepkimedir."}
{k:"Bilim",s:"Ekzotermik tepkime ne demektir?",o:["Isı alan","Isı veren","Nötr","Gaz alan"],d:1,a:"Ekzotermik tepkime çevreye ısı veren tepkimedir."}
{k:"Bilim",s:"Kuantum fiziğinin kurucusu kimdir?",o:["Newton","Einstein","Planck","Bohr"],d:2,a:"Max Planck kuantum fiziğinin kurucusu olarak kabul edilir."}
{k:"Bilim",s:"CRISPR teknolojisi ne amaçla kullanılır?",o:["Teleskop","Gen düzenleme","Nükleer enerji","İlaç üretimi"],d:1,a:"CRISPR DNA düzenleme teknolojisidir gen terapisi ve araştırmada kullanılır."}
{k:"Tarih",s:"Müdafaa-i Hukuk Cemiyetleri ne amaçla kuruldu?",o:["Ticaret","İşgallere karşı direniş","Eğitim","Tarım"],d:1,a:"Müdafaa-i Hukuk Cemiyetleri işgallere karşı halkın haklarını savunmak için kurulmuştur."}
{k:"Tarih",s:"Misak-ı Milli hangi yılda kabul edildi?",o:["1918","1919","1920","1921"],d:2,a:"Misak-ı Milli 28 Ocak 1920 de son Osmanlı Meclisinde kabul edilmiştir."}
{k:"Tarih",s:"Takrir-i Sükun Kanunu ne amaçla çıkarıldı?",o:["Ekonomi","İç güvenlik ve muhalefeti bastırma","Eğitim","Sağlık"],d:1,a:"Takrir-i Sükun Kanunu 1925 te Şeyh Said isyanı sonrası çıkarılmıştır."}
{k:"Tarih",s:"Osmanlıda Divan-ı Hümayun ne işe yarardı?",o:["Askeri karargah","Devlet yönetim kurulu","Mahkeme","Ticaret odası"],d:1,a:"Divan-ı Hümayun Osmanlı Devletinin en yüksek yönetim organıydı."}
{k:"Tarih",s:"Coğrafi Keşifler hangi yüzyılda yoğunlaştı?",o:["13. yy","14. yy","15. yy","17. yy"],d:2,a:"Coğrafi Keşifler 15. ve 16. yüzyıllarda yoğunlaşmıştır."}
{k:"Tarih",s:"Osmanlıda Tımar sistemi neyi ifade eder?",o:["Ticaret","Toprak yönetim sistemi","Eğitim","Denizcilik"],d:1,a:"Tımar sistemi devlete ait toprakların sipahilere verildiği askeri-tarımsal düzendir."}
{k:"Coğrafya",s:"Türkiye nin en büyük ovası hangisidir?",o:["Çukurova","Konya Ovası","Bafra Ovası","Muş Ovası"],d:1,a:"Konya Ovası Türkiye nin en geniş ovasıdır."}
{k:"Coğrafya",s:"Plato ile ova arasındaki fark nedir?",o:["Boyut","Plato yüksekte düz alan ova alçakta","Renk","İklim"],d:1,a:"Plato yüksek ve düz araziyken ova alçak ve düz alanları ifade eder."}
{k:"Coğrafya",s:"Sübtropikal iklim kuşağı nerelerde görülür?",o:["Kutuplar","Ekvator","Dönenceler civarı","Kuzey Kutup Dairesi"],d:2,a:"Sübtropikal iklim tropikal kuşak ile ılıman kuşak arasında dönenceler civarında görülür."}
{k:"Coğrafya",s:"Karstik göl nasıl oluşur?",o:["Volkanla","Kireçtaşının erimesiyle oluşan çukurda","Buzulla","Heyelanla"],d:1,a:"Karstik göl kireçtaşının erimesiyle oluşan çukurlarda su birikmesiyle meydana gelir."}
{k:"Coğrafya",s:"Set gölü nasıl oluşur?",o:["Depremle","Heyelan veya lav akıntısıyla nehrin önünün kapanması","Rüzgarla","Buzulla"],d:1,a:"Set gölü heyelan lav akıntısı veya birikinti ile nehir yatağının önünün kapanmasıyla oluşur."}
{k:"Coğrafya",s:"Türkiye de Akdeniz iklimi nerelerde görülür?",o:["Karadeniz kıyıları","Akdeniz ve Ege kıyıları","İç Anadolu","Doğu Anadolu"],d:1,a:"Akdeniz iklimi Akdeniz ve Ege kıyılarında görülür."}
{k:"Coğrafya",s:"Tuzluluk oranı en yüksek deniz hangisidir?",o:["Akdeniz","Karadeniz","Lut Gölü (Ölü Deniz)","Kızıldeniz"],d:2,a:"Ölü Deniz (Lut Gölü) dünyanın tuzluluk oranı en yüksek su kütlesidir."}
{k:"Coğrafya",s:"Delta ovaları hangi özelliğe sahiptir?",o:["Kurak","Alüvyon bakımından zengin verimli","Dağlık","Volkanik"],d:1,a:"Delta ovaları nehirlerin alüvyon biriktirmesiyle oluşan çok verimli alanlardır."}
{k:"Coğrafya",s:"Türkiye de en önemli krom yatakları nerededir?",o:["Batı Anadolu","Güneydoğu ve İç Anadolu","Karadeniz","Ege"],d:1,a:"Krom yatakları Elazığ Eskişehir ve Güneydoğu Anadolu da yoğunlaşmıştır."}
{k:"Coğrafya",s:"Dünyanın en yağışlı yeri neresidir?",o:["Amazon","Cherrapunji Hindistan","Kongo","Borneo"],d:1,a:"Hindistan daki Cherrapunji (Mawsynram) dünyanın en yağışlı yeri olarak bilinir."}
{k:"Coğrafya",s:"Graben nedir?",o:["Dağ","Fay hatları arasında çökmüş alan","Volkan","Plato"],d:1,a:"Graben iki fay hattı arasında çökmüş tektonik çukurluktur."}
{k:"Coğrafya",s:"Horst nedir?",o:["Çukur","Fay hatları arasında yükselmiş alan","Göl","Ova"],d:1,a:"Horst iki fay hattı arasında yükselmiş bloktur."}
{k:"Coğrafya",s:"Bor madeni en çok hangi ülkede bulunur?",o:["ABD","Rusya","Türkiye","Çin"],d:2,a:"Türkiye dünya bor rezervlerinin yaklaşık yüzde 73 üne sahiptir."}
{k:"Coğrafya",s:"Maki bitki örtüsü nerelerde görülür?",o:["Kurak bölgeler","Akdeniz iklim kuşağı","Tropikal bölge","Kutuplar"],d:1,a:"Maki Akdeniz ikliminin hüküm sürdüğü yerlerde görülen bodur ağaç ve çalılıklardır."}
{k:"Coğrafya",s:"Türkiye nin en uzun sınırı hangi ülkeyledir?",o:["Irak","İran","Suriye","Bulgaristan"],d:2,a:"Türkiye nin en uzun kara sınırı Suriye iledir."}
{k:"Coğrafya",s:"Beşeri coğrafya neyi inceler?",o:["Fiziki arazi","İnsan ve mekan ilişkisi","Hava durumu","Kayaçlar"],d:1,a:"Beşeri coğrafya insanların mekanla ilişkisini nüfus yerleşme ekonomi gibi konuları inceler."}
{k:"Coğrafya",s:"Sıcak çöl ikliminin en belirgin özelliği nedir?",o:["Çok yağışlı","Gece-gündüz sıcaklık farkı çok yüksek","Ilıman","Nemli"],d:1,a:"Sıcak çöllerde gece-gündüz sıcaklık farkı 40-50 dereceyi bulabilir."}
{k:"Coğrafya",s:"Dalmaçya tipi kıyı nasıl oluşur?",o:["Akarsu erozyonuyla","Dağların kıyıya paralel uzanıp vadilerin deniz suyu altında kalmasıyla","Volkanla","Buzulla"],d:1,a:"Dalmaçya tipi kıyı dağların kıyıya paralel uzandığı ve vadilerin suyla dolduğu kıyılardır."}
{k:"Coğrafya",s:"Ria tipi kıyı nasıl oluşur?",o:["Volkanla","Akarsu vadilerinin deniz suyu altında kalmasıyla","Rüzgarla","Buzulla"],d:1,a:"Ria tipi kıyı akarsu vadilerinin deniz seviyesi yükselmesiyle suyla dolmasıyla oluşur."}
{k:"Coğrafya",s:"Fjord tipi kıyı nasıl oluşur?",o:["Volkanla","Buzul vadilerinin suyla dolmasıyla","Rüzgarla","Akarsuyla"],d:1,a:"Fjord tipi kıyılar buzul vadilerinin deniz suyu ile dolmasıyla oluşan derin girintilerdir."}
{k:"Coğrafya",s:"Skyer (şist) hangi kayaç türüne aittir?",o:["Magmatik","Tortul","Başkalaşım (metamorfik)","Volkanik"],d:2,a:"Şist başkalaşım (metamorfik) kayaçlardandır."}
{k:"Coğrafya",s:"Türkiye de jeotermal enerji potansiyeli en yüksek bölge hangisidir?",o:["Karadeniz","Ege","İç Anadolu","Doğu Anadolu"],d:1,a:"Ege Bölgesi fay hatları nedeniyle Türkiye nin en yüksek jeotermal enerji potansiyeline sahiptir."}
{k:"Bilim",s:"Termodinamiğin ikinci yasası neyi belirtir?",o:["Enerji korunur","Entropi sürekli artar","Sıcaklık sabit kalır","Basınç azalır"],d:1,a:"Termodinamiğin ikinci yasası kapalı bir sistemde entropinin sürekli arttığını belirtir."}
{k:"Bilim",s:"Genelleştirilmiş görelilik kuramı neyi açıklar?",o:["Atomlar","Kütlenin uzay-zamanı bükmesi ve kütleçekim","Işık hızı","Elektrik"],d:1,a:"Einstein in genel görelilik kuramı kütleçekimi uzay-zamanın bükülmesi olarak açıklar."}
{k:"Bilim",s:"Higgs bozonu niçin önemlidir?",o:["Enerji üretimi","Parçacıklara kütle kazandıran mekanizma","Işık hızı","Nükleer enerji"],d:1,a:"Higgs bozonu parçacıklara kütlelerini kazandıran Higgs alanıyla ilişkili parçacıktır."}
{k:"Bilim",s:"Karanlık madde ne demektir?",o:["Siyah delik","Gözlemlenemeyen ama çekim etkisi olan madde","Kara enerji","Nötron"],d:1,a:"Karanlık madde gözlemlenemeyen ancak kütleçekim etkisiyle varlığı bilinen maddedir."}
{k:"Bilim",s:"Genetik mühendisliği ne amaçla kullanılır?",o:["Araba üretimi","Canlıların genlerini değiştirme","Maden arama","Havayolu"],d:1,a:"Genetik mühendisliği canlıların DNA sını değiştirmek için kullanılır."}
{k:"Bilim",s:"Redoks tepkimesi nedir?",o:["Asit-baz","Elektron alışverişi tepkimesi","Nükleer","Fisyon"],d:1,a:"Redoks tepkimesi elektron alışverişinin (yükseltgenme-indirgenme) olduğu tepkimedir."}
{k:"Bilim",s:"Hücre zarı hangi moleküllerden oluşur?",o:["Karbonhidrat","Fosfolipid çift tabaka","Sadece protein","Nükleik asit"],d:1,a:"Hücre zarı fosfolipid çift tabakasından ve proteinlerden oluşur."}
{k:"Bilim",s:"Kuvantum dolanıklık nedir?",o:["Elektrik","İki parçacığın birbirine bağlı kuantum durumu","Çekim kuvveti","Manyetik alan"],d:1,a:"Kuantum dolanıklık iki parçacığın mesafeden bağımsız olarak birbirine bağlı davranmasıdır."}
{k:"Bilim",s:"Proton kütle birimi olarak kaç amu dur?",o:["0.5","1","2","4"],d:1,a:"Protonun kütlesi yaklaşık 1 atom kütle birimi (amu) dir."}
{k:"Bilim",s:"Standart Modelde kaç temel kuvvet vardır?",o:["2","3","4","5"],d:2,a:"Standart Modelde 4 temel kuvvet vardır: kütle çekim elektromanyetik güçlü ve zayıf nükleer."}
{k:"Bilim",s:"Antibiyotikler neye karşı etkilidir?",o:["Virüslere","Bakterilere","Mantarlara","Parazitlere"],d:1,a:"Antibiyotikler bakterilere karşı etkili ilaçlardır virüslere karşı etkisizdir."}
{k:"Bilim",s:"İzotop ne demektir?",o:["Farklı element","Aynı elementin farklı nötron sayılı türleri","Bileşik","Alaşım"],d:1,a:"İzotoplar aynı elementin farklı nötron sayısına sahip türleridir."}
{k:"Bilim",s:"Schrodinger denklemi neyi tanımlar?",o:["Çekim kuvveti","Kuantum mekaniğinde dalga fonksiyonu","Işık hızı","Ses dalgası"],d:1,a:"Schrodinger denklemi kuantum mekaniğinde parçacığın dalga fonksiyonunu tanımlar."}
{k:"Bilim",s:"Fotosentezde ışık tepkimeleri nerede gerçekleşir?",o:["Mitokondri","Tilakoid zarında","Hücre çekirdeğinde","Ribozomda"],d:1,a:"Fotosentezin ışık tepkimeleri kloroplastın tilakoid zarında gerçekleşir."}
{k:"Bilim",s:"Krebs döngüsü nerede gerçekleşir?",o:["Sitoplazma","Hücre zarı","Mitokondri matriks","Çekirdek"],d:2,a:"Krebs döngüsü mitokondrinin matriksinde gerçekleşen metabolik döngüdür."}
{k:"Bilim",s:"Nötrinonun özelliği nedir?",o:["Ağır parçacık","Çok küçük kütleli zayıf etkileşimli parçacık","Protondan büyük","Yüklü parçacık"],d:1,a:"Nötrino çok küçük kütleli nötr ve maddeyle çok zayıf etkileşen parçacıktır."}
{k:"Bilim",s:"Manyetik rezonans görüntüleme (MR) hangi prensiple çalışır?",o:["X ışını","Manyetik alan ve radyo dalgası","Ultrason","Lazer"],d:1,a:"MR güçlü manyetik alan ve radyo dalgaları kullanarak vücuttaki hidrojen atomlarını görüntüler."}
{k:"Bilim",s:"Plazma ne tür bir maddedir?",o:["Katı","Sıvı","Gaz","Maddenin dördüncü hali"],d:3,a:"Plazma iyonize gaz olarak bilinen maddenin dördüncü halidir."}
{k:"Bilim",s:"Supernova nedir?",o:["Yeni gezegen","Büyük bir yıldızın patlayarak parlaması","Kara delik","Kuasar"],d:1,a:"Supernova büyük bir yıldızın ömrünün sonunda patlayarak muazzam parlaklıkla parlamasıdır."}
{k:"Bilim",s:"Elektroliz ne demektir?",o:["Isıyla ayrışma","Elektrik akımıyla bileşikleri ayrıştırma","Nükleer parçalanma","Yanma"],d:1,a:"Elektroliz elektrik akımı kullanarak bileşikleri bileşenlerine ayırma işlemidir."}
{k:"Bilim",s:"Allotropi ne demektir?",o:["Farklı element","Aynı elementin farklı fiziksel yapıları","İzotop","Bileşik"],d:1,a:"Allotropi aynı elementin farklı fiziksel yapılarda bulunmasıdır (elmas ve grafit gibi)."}
{k:"Bilim",s:"Le Chatelier prensibi neyi ifade eder?",o:["Enerji korunumu","Denge sistemi değişikliğe karşı tepki verir","Kütle korunumu","Entropi artışı"],d:1,a:"Le Chatelier prensibi dengedeki bir sisteme dışarıdan etki yapıldığında sistemin bu etkiyi azaltacak yönde tepki verdiğini belirtir."}
{k:"Bilim",s:"pH skalasında 1 ne anlama gelir?",o:["Nötr","Güçlü asit","Güçlü baz","Saf su"],d:1,a:"pH 1 çok güçlü asidik çözeltiyi ifade eder."}
{k:"Bilim",s:"Süperiletkenlik ne demektir?",o:["Normal iletim","Sıfır direnç ile elektrik iletimi","Yüksek direnç","Isı iletimi"],d:1,a:"Süperiletkenlik belirli sıcaklıkların altında bir malzemenin sıfır elektrik direnci göstermesidir."}
{k:"Doğa",s:"Biyom nedir?",o:["Tek tür","Benzer iklim ve bitki örtüsüne sahip geniş ekosistem","Hayvan grubu","Toprak türü"],d:1,a:"Biyom benzer iklim koşullarına ve bitki örtüsüne sahip büyük ekolojik bölgedir."}
{k:"Doğa",s:"Tropik yağmur ormanlarının en önemli özelliği nedir?",o:["Düşük nem","Yüksek biyolojik çeşitlilik","Soğuk iklim","Az yağış"],d:1,a:"Tropik yağmur ormanları dünyanın en yüksek biyolojik çeşitliliğine sahip biyomlardır."}
{k:"Doğa",s:"Ötrofikasyon ne demektir?",o:["Oksijen artışı","Göl ve nehirlerde aşırı besin maddesi birikimi","Kuraklık","Erozyon"],d:1,a:"Ötrofikasyon su kütlelerinde aşırı besin maddesi birikimi sonucu alg patlaması ve oksijen azalmasıdır."}
{k:"Doğa",s:"Endemik tür ne demektir?",o:["Yaygın tür","Sadece belirli bir bölgede yaşayan tür","Göçmen tür","Nesli tükenmiş tür"],d:1,a:"Endemik tür yalnızca belirli bir coğrafi bölgede doğal olarak yaşayan türdür."}
{k:"Doğa",s:"Karbon ayak izi ne demektir?",o:["Ayak izi","Bireyin veya kuruluşun ürettiği sera gazı miktarı","Karbon elementi","Toprak izi"],d:1,a:"Karbon ayak izi bir faaliyetin doğrudan ve dolaylı olarak ürettiği sera gazı miktarıdır."}
{k:"Doğa",s:"Biyoçeşitlilik kaybının en büyük nedeni nedir?",o:["Doğal afetler","Habitat tahribatı","Volkanlar","Depremler"],d:1,a:"Habitat tahribatı ve parçalanması biyoçeşitlilik kaybının en büyük nedenidir."}
{k:"Doğa",s:"Kırmızı Liste ne demektir?",o:["Alışveriş listesi","IUCN nesli tehlike altındaki türler listesi","Yasaklı maddeler","Tehlikeli bölgeler"],d:1,a:"IUCN Kırmızı Liste nesli tehlike altındaki türlerin uluslararası sınıflandırma listesidir."}
{k:"Doğa",s:"İstilacı tür ne demektir?",o:["Yerli tür","Yabancı ortamda hızla yayılıp zarar veren tür","Göçmen tür","Endemik tür"],d:1,a:"İstilacı tür doğal ortamının dışına yayılarak ekosisteme zarar veren türdür."}
{k:"Doğa",s:"Permakültür ne demektir?",o:["Gübreleme","Doğaya uyumlu sürdürülebilir tarım sistemi","Endüstriyel tarım","Monokültür"],d:1,a:"Permakültür doğal ekosistemleri taklit eden sürdürülebilir tarım ve yaşam tasarım sistemidir."}
{k:"Doğa",s:"Okyanusların asitlenmesi neyin sonucudur?",o:["Volkanik aktivite","CO2 emiliminin artması","Rüzgar","Gel-git"],d:1,a:"Okyanuslar atmosferden artan CO2 yi emerek asitlenir ve mercan resifleri tehlikeye girer."}
{k:"Doğa",s:"Azot döngüsünde azot fiksasyonu ne demektir?",o:["Azotun yok olması","Atmosferik azotun biyolojik kullanılabilir forma dönüşmesi","Azot gazı üretimi","Amonyak yıkımı"],d:1,a:"Azot fiksasyonu atmosferdeki N2 nin bitkilerin kullanabileceği forma dönüştürülmesidir."}
{k:"Doğa",s:"Mercan ağarması neden olur?",o:["Soğuk su","Deniz suyunun ısınmasıyla simbiyotik alglerin kaybı","Kirlilik","Tuzluluk"],d:1,a:"Mercan ağarması su sıcaklığının artmasıyla mercanların simbiyotik alglerini kaybetmesidir."}
{k:"Doğa",s:"Suksesyon ne demektir?",o:["Ölüm","Bir ekosistemde zamanla tür kompozisyonunun değişmesi","Göç","Avcılık"],d:1,a:"Suksesyon bir ekosistemin zamanla tür kompozisyonu ve yapısının değişim sürecidir."}
{k:"Doğa",s:"Ticari avcılığın en büyük kurbanı hangi hayvan grubudur?",o:["Kuşlar","Deniz memelileri ve balıklar","Sürüngenler","Böcekler"],d:1,a:"Ticari avcılık özellikle deniz memelileri ve balıkları tehdit etmektedir."}
{k:"Doğa",s:"Yenilenebilir enerji kaynakları hangileridir?",o:["Kömür petrol","Güneş rüzgar hidroelektrik","Doğalgaz","Uranyum"],d:1,a:"Güneş rüzgar ve hidroelektrik yenilenebilir enerji kaynaklarıdır."}
{k:"Doğa",s:"Ozon deliğinin en büyük nedeni nedir?",o:["CO2","CFC gazları","Metan","Su buharı"],d:1,a:"Kloroflorokarbon (CFC) gazları ozon tabakasının incelmesinin en büyük nedenidir."}
{k:"Doğa",s:"Mangrove ormanları neden önemlidir?",o:["Kereste","Kıyı koruma ve biyoçeşitlilik","Süs bitkisi","Yakacak"],d:1,a:"Mangrove ormanları kıyıları fırtınadan korur ve zengin biyoçeşitliliğe ev sahipliği yapar."}
{k:"Doğa",s:"Toprak kirliliğinin en büyük nedeni nedir?",o:["Rüzgar","Tarım kimyasalları ve sanayi atıkları","Yağmur","Güneş"],d:1,a:"Pestisit gübre ve endüstriyel atıklar toprak kirliliğinin en büyük nedenleridir."}
{k:"Doğa",s:"Su ayak izi ne demektir?",o:["Ayak yıkama","Bir ürünün üretimi için harcanan toplam su","Yağmur ölçümü","Nehir akışı"],d:1,a:"Su ayak izi bir ürün veya hizmetin üretimi için doğrudan ve dolaylı kullanılan toplam su miktarıdır."}
{k:"Doğa",s:"Ekolojik niş ne demektir?",o:["Yuva","Bir türün ekosistemdeki rolü ve yaşam tarzı","Göç yolu","Bölge sınırı"],d:1,a:"Ekolojik niş bir türün ekosistemi içindeki rolü beslenme tarzı ve yaşam koşullarını tanımlar."}
{k:"Doğa",s:"Biyokütle enerjisi nedir?",o:["Nükleer","Organik maddelerden elde edilen enerji","Fosil yakıt","Jeotermal"],d:1,a:"Biyokütle enerjisi bitki ve hayvan kaynaklı organik maddelerden elde edilen enerjidir."}
{k:"Doğa",s:"Yer altı sularının kirlenmesi neye yol açar?",o:["Deprem","İçme suyu kıtlığı ve toprak kirliliği","Volkan","Sel"],d:1,a:"Yer altı sularının kirlenmesi içme suyu kaynaklarını ve tarım alanlarını tehdit eder."}
{k:"Doğa",s:"Paris İklim Anlaşması ne amaçlar?",o:["Ticaret","Küresel sıcaklık artışını 1.5 derece ile sınırlama","Savaş","Eğitim"],d:1,a:"Paris Anlaşması küresel sıcaklık artışını sanayi öncesine göre 1.5 derece ile sınırlamayı hedefler."}
{k:"Doğa",s:"Sürdürülebilir kalkınma ne demektir?",o:["Hızlı büyüme","Bugünün ihtiyaçlarını gelecek nesilleri tehlikeye atmadan karşılama","Sanayi devrimi","Doğal kaynak tüketimi"],d:1,a:"Sürdürülebilir kalkınma gelecek nesillerin ihtiyaçlarını karşılayabilme kapasitesini tehlikeye atmadan bugünün ihtiyaçlarını karşılamaktır."}
{k:"Doğa",s:"Atık su arıtma tesisleri ne yapar?",o:["Su üretir","Kirli suyu temizleyerek doğaya güvenle geri verir","Su depolar","Su ısıtır"],d:1,a:"Atık su arıtma tesisleri evsel ve endüstriyel atık suları arıtarak çevreye zarar vermeden doğaya geri kazandırır."}
{k:"Doğa",s:"Gen bankası ne amaçla kurulur?",o:["Para saklamak","Bitki ve hayvan genetik materyalini korumak","İlaç üretmek","Gıda depolamak"],d:1,a:"Gen bankaları bitki tohumları ve hayvan genetik materyallerini gelecek nesiller için korumak amacıyla kurulur."}
{k:"Doğa",s:"Ekosistem hizmetleri ne demektir?",o:["İnternet","Doğanın insanlara sağladığı faydalar","Bankacılık","Telekomünikasyon"],d:1,a:"Ekosistem hizmetleri tozlaşma su arıtma karbon tutma gibi doğanın insanlara sağladığı faydalardır."}
{k:"Doğa",s:"Biyolojik göstergeler ne işe yarar?",o:["Termometre","Çevre kalitesini ölçmek için belirli canlı türleri","Pusula","Harita"],d:1,a:"Biyolojik göstergeler çevre kalitesinin değerlendirilmesinde kullanılan belirli canlı türleridir."}
{k:"Doğa",s:"Sera etkisi olmasa Dünya ortalama sıcaklığı kaç olurdu?",o:["-18 derece","0 derece","15 derece","25 derece"],d:0,a:"Sera etkisi olmasa Dünya nın ortalama sıcaklığı yaklaşık -18 derece olurdu."}
{k:"Doğa",s:"Karbon nötr ne demektir?",o:["Karbon yok","Üretilen karbonun eşit miktarda dengelenmesi","Karbon elementinin nötr olması","Karbon kırılması"],d:1,a:"Karbon nötr atmosfere salınan karbonun eşit miktarda azaltılması veya dengelenmesidir."}
{k:"Başkentler",s:"Kazakistan ın başkenti neresidir?",o:["Almatı","Astana","Bişkek","Taşkent"],d:1,a:"Astana Kazakistan ın başkentidir."}
{k:"Başkentler",s:"Özbekistan ın başkenti neresidir?",o:["Bişkek","Astana","Taşkent","Dışanbe"],d:2,a:"Taşkent Özbekistan ın başkentidir."}
{k:"Başkentler",s:"Türkmenistan ın başkenti neresidir?",o:["Aşkabat","Taşkent","Bişkek","Dışanbe"],d:0,a:"Aşkabat Türkmenistan ın başkentidir."}
{k:"Başkentler",s:"Kırgızistan ın başkenti neresidir?",o:["Taşkent","Astana","Bişkek","Aşkabat"],d:2,a:"Bişkek Kırgızistan ın başkentidir."}
{k:"Başkentler",s:"Tacikistan ın başkenti neresidir?",o:["Taşkent","Bişkek","Astana","Dışanbe"],d:3,a:"Dışanbe Tacikistan ın başkentidir."}
{k:"Başkentler",s:"Ermenistan ın başkenti neresidir?",o:["Tiflis","Bakü","Erivan","Tahran"],d:2,a:"Erivan Ermenistan ın başkentidir."}
{k:"Başkentler",s:"Sri Lanka nın başkenti neresidir?",o:["Kolombo","Sri Jayewardenepura Kotte","Kandy","Galle"],d:1,a:"Sri Lanka nın resmi başkenti Sri Jayewardenepura Kotte dir."}
{k:"Başkentler",s:"Nepal in başkenti neresidir?",o:["Katmandu","Dakka","Thimphu","Colombo"],d:0,a:"Katmandu Nepal in başkentidir."}
{k:"Başkentler",s:"Bhutan ın başkenti neresidir?",o:["Katmandu","Thimphu","Dakka","Yangon"],d:1,a:"Thimphu Bhutan ın başkentidir."}
{k:"Başkentler",s:"Bangladeş in başkenti neresidir?",o:["Kalküta","Mumbai","Dakka","Chittagong"],d:2,a:"Dakka Bangladeş in başkentidir."}
{k:"Başkentler",s:"Kamboçya nın başkenti neresidir?",o:["Vientiane","Phnom Penh","Hanoi","Jakarta"],d:1,a:"Phnom Penh Kamboçya nın başkentidir."}
{k:"Başkentler",s:"Laos un başkenti neresidir?",o:["Phnom Penh","Vientiane","Bangkok","Hanoi"],d:1,a:"Vientiane Laos un başkentidir."}
{k:"Başkentler",s:"Etiyopya nın başkenti neresidir?",o:["Nairobi","Addis Ababa","Mogadişu","Kampala"],d:1,a:"Addis Ababa Etiyopya nın başkentidir."}
{k:"Başkentler",s:"Gana nın başkenti neresidir?",o:["Lagos","Accra","Dakar","Abidjan"],d:1,a:"Accra Gana nın başkentidir."}
{k:"Başkentler",s:"Senegal in başkenti neresidir?",o:["Accra","Bamako","Dakar","Conakry"],d:2,a:"Dakar Senegal in başkentidir."}
{k:"Başkentler",s:"Libya nın başkenti neresidir?",o:["Tunus","Trablus","Kahire","Cezayir"],d:1,a:"Trablus Libya nın başkentidir."}
{k:"Başkentler",s:"Cezayir in başkenti neresidir?",o:["Tunus","Rabat","Trablus","Cezayir"],d:3,a:"Cezayir şehri Cezayir in başkentidir."}
{k:"Başkentler",s:"Fas ın başkenti neresidir?",o:["Kazablanka","Marakeş","Rabat","Fes"],d:2,a:"Rabat Fas ın başkentidir."}
{k:"Başkentler",s:"Tunus un başkenti neresidir?",o:["Tunus","Trablus","Kahire","Rabat"],d:0,a:"Tunus şehri Tunus un başkentidir."}
{k:"Başkentler",s:"Tanzanya nın başkenti neresidir?",o:["Nairobi","Dar es Salaam","Dodoma","Kampala"],d:2,a:"Dodoma Tanzanya nın resmi başkentidir."}
{k:"Başkentler",s:"Uganda nın başkenti neresidir?",o:["Nairobi","Kampala","Kigali","Bujumbura"],d:1,a:"Kampala Uganda nın başkentidir."}
{k:"Başkentler",s:"Küba nın eski adı ile bilinen başkenti neresidir?",o:["Havana","Santiago","Trinidad","Varadero"],d:0,a:"Havana Küba nın başkentidir."}
{k:"Başkentler",s:"Paraguay ın başkenti neresidir?",o:["Montevideo","Buenos Aires","Asuncion","La Paz"],d:2,a:"Asuncion Paraguay ın başkentidir."}
{k:"Başkentler",s:"Uruguay ın başkenti neresidir?",o:["Asuncion","Montevideo","Buenos Aires","Brasilia"],d:1,a:"Montevideo Uruguay ın başkentidir."}
{k:"Başkentler",s:"Bolivya nın anayasal başkenti neresidir?",o:["La Paz","Sucre","Santa Cruz","Cochabamba"],d:1,a:"Sucre Bolivya nın anayasal başkenti La Paz ise yönetim başkentidir."}
{k:"Başkentler",s:"Ekvador ın başkenti neresidir?",o:["Lima","Quito","Bogota","Guayaquil"],d:1,a:"Quito Ekvador ın başkentidir."}
{k:"Başkentler",s:"Venezuela nın başkenti neresidir?",o:["Bogota","Caracas","Lima","Quito"],d:1,a:"Caracas Venezuela nın başkentidir."}
{k:"Başkentler",s:"Panama nın başkenti neresidir?",o:["San Jose","Panama City","Managua","Tegucigalpa"],d:1,a:"Panama City Panama nın başkentidir."}
{k:"Başkentler",s:"Kosta Rika nın başkenti neresidir?",o:["Panama City","San Jose","Managua","Guatemala City"],d:1,a:"San Jose Kosta Rika nın başkentidir."}
{k:"Başkentler",s:"İzlanda nın başkenti neresidir?",o:["Oslo","Reykjavik","Helsinki","Kopenhag"],d:1,a:"Reykjavik İzlanda nın başkentidir."}
{k:"Başkentler",s:"Malta nın başkenti neresidir?",o:["Valletta","Napoli","Atina","Nicosia"],d:0,a:"Valletta Malta nın başkentidir."}
{k:"Başkentler",s:"KKTC nin başkenti neresidir?",o:["Limasol","Girne","Lefkoşa","Magusa"],d:2,a:"Lefkoşa KKTC nin başkentidir."}
{k:"Başkentler",s:"Kosova nın başkenti neresidir?",o:["Belgrad","Tiran","Priştine","Üsküp"],d:2,a:"Priştine Kosova nın başkentidir."}
{k:"Başkentler",s:"Karadağ ın başkenti neresidir?",o:["Belgrad","Podgorica","Tiran","Sarajevo"],d:1,a:"Podgorica Karadağ ın başkentidir."}
{k:"Başkentler",s:"Lüksemburg un başkenti neresidir?",o:["Brüksel","Lüksemburg","Amsterdam","Bern"],d:1,a:"Lüksemburg şehri Lüksemburg un başkentidir."}
{k:"Başkentler",s:"Liechtenstein in başkenti neresidir?",o:["Bern","Vaduz","Zürih","Cenevre"],d:1,a:"Vaduz Liechtenstein in başkentidir."}
{k:"Başkentler",s:"Andorra nın başkenti neresidir?",o:["Andorra la Vella","Madrid","Lizbon","Toulouse"],d:0,a:"Andorra la Vella Andorra nın başkentidir."}
{k:"Başkentler",s:"San Marino nun başkenti neresidir?",o:["Roma","San Marino","Vatikan","Napoli"],d:1,a:"San Marino şehri San Marino nun başkentidir."}
{k:"Başkentler",s:"Monako nın başkenti neresidir?",o:["Nice","Monako","Marsilya","Cannes"],d:1,a:"Monako şehir-devleti olarak başkenti kendisidir."}
{k:"Başkentler",s:"Fiji nin başkenti neresidir?",o:["Suva","Nadi","Port Moresby","Honiara"],d:0,a:"Suva Fiji nin başkentidir."}
{k:"Türkiye",s:"Türkiye GDP ye göre dünyanın kaçıncı büyük ekonomisidir?",o:["10-15","15-20","20-25","25-30"],d:1,a:"Türkiye GDP ye göre dünyanın yaklaşık 17-19. büyük ekonomisidir."}
{k:"Türkiye",s:"Bosphorus kelimesi ne anlama gelir?",o:["Dar geçit","İnek geçidi","Deniz yolu","Köprü"],d:1,a:"Bosphorus Yunanca inek geçidi anlamına gelir."}
{k:"Türkiye",s:"Türkiye nin ilk nükleer santralı nerede inşa edilmektedir?",o:["Sinop","Mersin Akkuyu","İstanbul","Edirne"],d:1,a:"Akkuyu Nükleer Santrali Mersin de inşa edilmektedir."}
{k:"Türkiye",s:"Mimar Sinan ın kalfalık eseri hangisidir?",o:["Selimiye","Süleymaniye","Şehzadebaşı","Sultanahmet"],d:1,a:"Süleymaniye Camii Mimar Sinan ın kalfalık eseridir."}
{k:"Türkiye",s:"Mimar Sinan ın çıraklık eseri hangisidir?",o:["Selimiye","Süleymaniye","Şehzadebaşı","Sultanahmet"],d:2,a:"Şehzadebaşı Camii Mimar Sinan ın çıraklık eseridir."}
{k:"Türkiye",s:"Türkiye de UNESCO listesindeki ilk alan hangisidir?",o:["Pamukkale","İstanbul Tarihi Alanları","Göreme","Divriği"],d:3,a:"Divriği Ulu Camii ve Darüşşifası 1985 te UNESCO listesine alınan ilk Türk eseridir."}
{k:"Türkiye",s:"Marmaray hangi yılda hizmete açıldı?",o:["2010","2013","2016","2019"],d:1,a:"Marmaray 29 Ekim 2013 te hizmete açılmıştır."}
{k:"Türkiye",s:"Yavuz Sultan Selim Köprüsü hangi yılda açıldı?",o:["2014","2016","2018","2020"],d:1,a:"Yavuz Sultan Selim Köprüsü 2016 yılında açılmıştır."}
{k:"Türkiye",s:"Türkiye de en çok ihracat yapılan sektör hangisidir?",o:["Tarım","Otomotiv","Tekstil","Madencilik"],d:1,a:"Otomotiv sektörü Türkiye nin en büyük ihracat kalemidir."}
{k:"Türkiye",s:"Çatalhöyük kaç yıl öncesine tarihlenir?",o:["3000","5000","7000","9000"],d:3,a:"Çatalhöyük yaklaşık 9000 yıl öncesine tarihlenen dünyanın en eski yerleşim yerlerinden biridir."}
{k:"Türkiye",s:"Türkiye nin en uzun tüneli hangisidir?",o:["Marmaray","Ovit","İlgaz","Avrasya"],d:1,a:"Ovit Tüneli 14.3 km ile Türkiye nin en uzun karayolu tünelidir."}
{k:"Türkiye",s:"İstanbul Havalimanı hangi yılda tam kapasiteyle açıldı?",o:["2017","2018","2019","2020"],d:2,a:"İstanbul Havalimanı 2019 yılında tam kapasiteyle hizmete açılmıştır."}
{k:"Türkiye",s:"Van Gölü neden tuzlu ve sodalıdır?",o:["Denizle bağlantılı","Volkanik kayaçlardan çözünen mineraller","İnsan kirliliği","Rüzgar"],d:1,a:"Van Gölü çevresindeki volkanik kayaçlardan çözünen mineraller nedeniyle tuzlu ve sodalıdır."}
{k:"Türkiye",s:"Efes teki Artemis Tapınağı dünyanın yedi harikasından biri midir?",o:["Evet","Hayır","Belirsiz","Tartışmalı"],d:0,a:"Artemis Tapınağı Antik Dünyanın Yedi Harikasından biridir."}
{k:"Türkiye",s:"Osmanlı döneminde İstanbul a ne ad verilirdi?",o:["Byzantium","Konstantinopolis","Dersaadet","Hepsi"],d:3,a:"İstanbul tarih boyunca Byzantium Konstantinopolis ve Dersaadet gibi isimlerle anılmıştır."}
{k:"Türkiye",s:"Türkiye nin en büyük suni gölü hangisidir?",o:["Keban","Atatürk Baraj Gölü","Hirfanlı","Karakaya"],d:1,a:"Atatürk Baraj Gölü Türkiye nin en büyük yapay gölüdür."}
{k:"Türkiye",s:"Anadolu Medeniyetleri Müzesi hangi ildedir?",o:["İstanbul","Ankara","İzmir","Antalya"],d:1,a:"Anadolu Medeniyetleri Müzesi Ankara dadır."}
{k:"Türkiye",s:"Türkiye de ilk demir yolu hattı nerede yapıldı?",o:["İstanbul","İzmir-Aydın","Ankara","Adana"],d:1,a:"Türkiye nin ilk demir yolu hattı 1856 da İzmir-Aydın arasında yapılmıştır."}
{k:"Türkiye",s:"Türkiye de zeytinyağı üretiminde birinci il hangisidir?",o:["İzmir","Aydın","Balıkesir","Muğla"],d:2,a:"Balıkesir Türkiye de zeytinyağı üretiminde en önde gelen illerdendir."}
{k:"Türkiye",s:"Türkiye nin en büyük limanı hangisidir?",o:["İzmir","Mersin","İstanbul Ambarlı","Antalya"],d:2,a:"İstanbul Ambarlı Limanı Türkiye nin en büyük konteyner limanıdır."}
{k:"Türkiye",s:"Diyarbakır Surları hangi döneme aittir?",o:["Osmanlı","Roma","Selçuklu","Cumhuriyet"],d:1,a:"Diyarbakır Surları Roma dönemine ait olup UNESCO Dünya Mirası listesindedir."}
{k:"Türkiye",s:"Kapadokya da peribacaları hangi kayaçtan oluşmuştur?",o:["Granit","Mermer","Tüf","Bazalt"],d:2,a:"Peribacaları volkanik tüf kayacının aşınmasıyla oluşmuştur."}
{k:"Türkiye",s:"Türkiye nin en büyük ticaret ortağı hangi ülkedir?",o:["ABD","Rusya","Almanya","Çin"],d:2,a:"Almanya Türkiye nin en büyük ticaret ortaklarından biridir."}
{k:"Türkiye",s:"Türkiye de kaç tane UNESCO Dünya Mirası alanı vardır?",o:["10","15","21","30"],d:2,a:"Türkiye 2024 itibarıyla 21 UNESCO Dünya Mirası alanına sahiptir."}
{k:"Türkiye",s:"Avrasya Tüneli hangi boğazın altından geçer?",o:["Çanakkale","İstanbul","Kerç","Süveyş"],d:1,a:"Avrasya Tüneli İstanbul Boğazı nın altından geçen karayolu tünelidir."}
{k:"Türkiye",s:"Troya Savaşı efsanesi hangi ilde geçer?",o:["İzmir","Çanakkale","Balıkesir","Bursa"],d:1,a:"Troya antik kenti ve savaş efsanesi Çanakkale ilinde geçmektedir."}
{k:"Spor",s:"Olimpiyatlarda en çok altın madalya kazanan sporcu kimdir?",o:["Usain Bolt","Michael Phelps","Carl Lewis","Jesse Owens"],d:1,a:"Michael Phelps 23 altın madalya ile olimpiyat tarihinin en başarılı sporcusudur."}
{k:"Spor",s:"FIFA Dünya Kupası ilk kez hangi ülkede düzenlendi?",o:["Brezilya","İtalya","Uruguay","İngiltere"],d:2,a:"İlk FIFA Dünya Kupası 1930 da Uruguay da düzenlenmiştir."}
{k:"Spor",s:"Olimpiyat ateşi ilk kez nerede yakıldı?",o:["Atina 1896","Amsterdam 1928","Berlin 1936","Londra 1948"],d:1,a:"Olimpiyat ateşi ilk kez 1928 Amsterdam Olimpiyatlarında yakılmıştır."}
{k:"Spor",s:"Roger Federer hangi spor dalında ünlüdür?",o:["Golf","Tenis","Badminton","Masa tenisi"],d:1,a:"Roger Federer tenis tarihinin en büyük oyuncularından biridir."}
{k:"Spor",s:"Decathlon kaç branştan oluşur?",o:["5","8","10","12"],d:2,a:"Decathlon (onlu yarışma) 10 atletizm branşından oluşur."}
{k:"Spor",s:"Yelken sporunda kullanılan teknelere ne denir?",o:["Gemi","Kayık","Yat","Tekne sınıflarına göre değişir"],d:3,a:"Yelken sporunda tekne sınıflarına göre Laser Finn Optimist gibi farklı isimler kullanılır."}
{k:"Spor",s:"Grand Slam tenis turnuvalarından biri değil hangisi?",o:["Wimbledon","Roland Garros","US Open","Miami Open"],d:3,a:"Miami Open Grand Slam turnuvası değildir. Grand Slamler: Avustralya Roland Garros Wimbledon US Open."}
{k:"Spor",s:"Beşiktaş JK hangi yılda kurulmuştur?",o:["1899","1903","1905","1907"],d:1,a:"Beşiktaş JK 1903 yılında kurulmuştur."}
{k:"Spor",s:"Galatasaray SK hangi yılda kurulmuştur?",o:["1899","1903","1905","1907"],d:2,a:"Galatasaray SK 1905 yılında kurulmuştur."}
{k:"Spor",s:"Fenerbahçe SK hangi yılda kurulmuştur?",o:["1899","1903","1905","1907"],d:3,a:"Fenerbahçe SK 1907 yılında kurulmuştur."}
{k:"Spor",s:"E-spor hangi tür yarışmadır?",o:["Atletizm","Elektronik oyun yarışması","Masa oyunu","Kart oyunu"],d:1,a:"E-spor profesyonel elektronik oyun yarışmalarıdır."}
{k:"Spor",s:"Bir kriket maçında wicket ne demektir?",o:["Top","Kaleci","Üç tahta çubuk ve üzerindeki çıtalar","Saha"],d:2,a:"Wicket kriket te korucunun arkasındaki üç tahta çubuk ve üzerindeki çıtalardır."}
{k:"Spor",s:"Ironman yarışı hangi sporlardan oluşur?",o:["Koşu bisiklet","Yüzme bisiklet koşu","Kayak atış","Yüzme güreş"],d:1,a:"Ironman 3.8 km yüzme 180 km bisiklet ve 42.2 km koşudan oluşan ultra triatlon yarışıdır."}
{k:"Spor",s:"Doping nedir?",o:["Spor malzemesi","Performans artırıcı yasaklı madde kullanımı","Antrenman yöntemi","Beslenme planı"],d:1,a:"Doping sporcuların performanslarını artırmak için yasaklı madde kullanmasıdır."}
{k:"Spor",s:"VAR sistemi ne işe yarar?",o:["Skor takibi","Video ile hakem kararlarının incelenmesi","Bilet satışı","Antrenman planı"],d:1,a:"VAR Video Yardımcı Hakem sistemi tartışmalı pozisyonların video ile incelenmesidir."}
{k:"Spor",s:"Türkiye hangi yılda Avrupa Şampiyonası üçüncüsü oldu?",o:["2000","2002","2008","2012"],d:2,a:"Türkiye 2008 Avrupa Şampiyonasında yarı finale çıkarak üçüncü olmuştur."}
{k:"Spor",s:"2002 Dünya Kupasında Türkiye kaçıncı oldu?",o:["Birinci","İkinci","Üçüncü","Dördüncü"],d:2,a:"Türkiye 2002 Dünya Kupasında üçüncülük kazanmıştır."}
{k:"Spor",s:"Naim Süleymanoğlu hangi spor dalında olimpiyat şampiyonu oldu?",o:["Güreş","Halter","Boks","Judo"],d:1,a:"Naim Süleymanoğlu halter dalında 3 kez olimpiyat şampiyonu olmuştur."}
{k:"Spor",s:"Olimpiyatlarda hangi spor dalı ilk kez 2020 Tokyo da yer aldı?",o:["Karate","Kriket","Rugby","Golf"],d:0,a:"Karate ilk kez 2020 Tokyo Olimpiyatlarında yer almıştır."}
{k:"Spor",s:"ATP ve WTA hangi sporun organizasyonlarıdır?",o:["Futbol","Tenis","Basketbol","Voleybol"],d:1,a:"ATP (erkekler) ve WTA (kadınlar) profesyonel tenisin ana organizasyonlarıdır."}
{k:"Spor",s:"Biatlon hangi iki sporu birleştirir?",o:["Yüzme koşu","Kros kayak ve atıcılık","Bisiklet koşu","Güreş boks"],d:1,a:"Biatlon kros kayak ve tüfekle atıcılığı birleştiren kış sporudur."}
{k:"Spor",s:"Bir boks maçında raunt kaç dakikadır?",o:["2","3","4","5"],d:1,a:"Profesyonel boksta her raunt 3 dakikadır."}
{k:"Spor",s:"Dünya Atletizm Şampiyonası ilk kez nerede yapıldı?",o:["Atina","Helsinki","Berlin","Tokyo"],d:1,a:"İlk Dünya Atletizm Şampiyonası 1983 te Helsinki de yapılmıştır."}
{k:"Spor",s:"Kendo hangi ülkenin dövüş sanatıdır?",o:["Çin","Kore","Japonya","Vietnam"],d:2,a:"Kendo Japonya nın geleneksel kılıç sanatıdır."}
{k:"Spor",s:"Polo maçında kaç chukker oynanır?",o:["2","4","6","8"],d:2,a:"Polo maçında genellikle 6 chukker oynanır her biri 7 dakikadır."}
{k:"Matematik",s:"Logaritma ne demektir?",o:["Çarpma işlemi","Üs alma işleminin tersi","Bölme işlemi","Toplama işlemi"],d:1,a:"Logaritma üs alma işleminin tersidir log_b(x)=y demek b^y=x demektir."}
{k:"Matematik",s:"sin 30 derece kaçtır?",o:["0","0.5","0.707","1"],d:1,a:"sin 30 derece = 0.5 tir."}
{k:"Matematik",s:"cos 60 derece kaçtır?",o:["0","0.5","0.707","1"],d:1,a:"cos 60 derece = 0.5 tir."}
{k:"Matematik",s:"tan 45 derece kaçtır?",o:["0","0.5","1","Tanımsız"],d:2,a:"tan 45 derece = 1 dir."}
{k:"Matematik",s:"e sayısı yaklaşık kaçtır?",o:["1.414","2.718","3.14","1.618"],d:1,a:"Euler sayısı e yaklaşık 2.718 dir."}
{k:"Matematik",s:"Altın oran yaklaşık kaçtır?",o:["1.414","2.718","3.14","1.618"],d:3,a:"Altın oran (phi) yaklaşık 1.618 dir."}
{k:"Matematik",s:"Türev neyi ifade eder?",o:["Alan","Bir fonksiyonun anlık değişim hızı","Toplam","Ortalama"],d:1,a:"Türev bir fonksiyonun belirli bir noktadaki anlık değişim hızını ifade eder."}
{k:"Matematik",s:"İntegral neyi hesaplar?",o:["Eğim","Bir eğri altında kalan alan","Hız","Açı"],d:1,a:"Belirli integral bir eğri altında kalan alanı hesaplar."}
{k:"Matematik",s:"Permütasyon ile kombinasyon arasındaki fark nedir?",o:["Fark yok","Permütasyonda sıra önemli kombinasyonda değil","Aynı formül","Biri toplama biri çarpma"],d:1,a:"Permütasyonda sıra önemlidir kombinasyonda sıra önemsizdir."}
{k:"Matematik",s:"Bir kürenin hacmi nasıl hesaplanır?",o:["pi r kare","4/3 pi r kup","2 pi r","pi r kare h"],d:1,a:"Kürenin hacmi 4/3 x pi x r kup formülüyle hesaplanır."}
{k:"Matematik",s:"Bir matrisin determinantı sıfır ise ne anlama gelir?",o:["Tersi var","Tersi yoktur (tekil matris)","Birim matris","Simetrik"],d:1,a:"Determinantı sıfır olan matris tekil matristir ve tersi yoktur."}
{k:"Matematik",s:"Kompleks sayıda i neyi ifade eder?",o:["1","0","-1 in karekökü","Pi"],d:2,a:"i sanal birimdir ve -1 in karekökü olarak tanımlanır."}
{k:"Matematik",s:"Olasılıkta bağımsız olay ne demektir?",o:["Birbirini etkileyen","Birinin sonucu diğerini etkilemeyen","Aynı anda olan","Sıralı"],d:1,a:"Bağımsız olaylarda birinin sonucu diğerinin olasılığını etkilemez."}
{k:"Matematik",s:"Normal dağılımda ortalamadan 1 standart sapma içinde verinin yüzdesi kaçtır?",o:["50%","68%","95%","99%"],d:1,a:"Normal dağılımda verinin yaklaşık yüzde 68 i ortalamadan 1 standart sapma içindedir."}
{k:"Matematik",s:"Polinom nedir?",o:["Tek terimli","Değişkenlerin kuvvetlerinden oluşan cebirsel ifade","Kesir","Logaritma"],d:1,a:"Polinom değişkenlerin negatif olmayan tam sayı kuvvetleri ve katsayılardan oluşan ifadedir."}
{k:"Matematik",s:"Limit kavramı neyi ifade eder?",o:["Son nokta","Fonksiyonun bir noktaya yaklaşırken aldığı değer","İlk nokta","Orta nokta"],d:1,a:"Limit bir fonksiyonun bağımsız değişkeni belirli bir değere yaklaşırken aldığı değeri ifade eder."}
{k:"Matematik",s:"Pisagor üçlüsü hangisidir?",o:["2 3 4","3 4 5","4 5 6","5 6 7"],d:1,a:"3 4 5 bir Pisagor üçlüsüdür çünkü 9+16=25 dir."}
{k:"Matematik",s:"10 faktöriyel (10!) yaklaşık kaçtır?",o:["100000","362880","3628800","1000000"],d:2,a:"10! = 10x9x8x7x6x5x4x3x2x1 = 3628800 dür."}
{k:"Matematik",s:"Geometrik dizi nedir?",o:["Sabit fark","Her terim öncekinin sabit katı","Rastgele","Fibonacci"],d:1,a:"Geometrik dizide her terim bir önceki terimin sabit bir sayıyla çarpılmasıyla elde edilir."}
{k:"Matematik",s:"Aritmetik dizi nedir?",o:["Sabit oran","Her terim öncekine sabit sayı eklenmesi","Rastgele","Üstel"],d:1,a:"Aritmetik dizide ardışık terimler arasındaki fark sabittir."}
{k:"Matematik",s:"Euler formülü e^(i*pi) + 1 kaça eşittir?",o:["1","0","-1","Pi"],d:1,a:"Euler formülüne göre e^(i*pi) + 1 = 0 dır."}
{k:"Matematik",s:"İrrasyonel sayı nedir?",o:["Tam sayı","Kesir olarak yazılamayan sayı","Negatif sayı","Çift sayı"],d:1,a:"İrrasyonel sayılar kesir olarak yazılamayan sayılardır (pi kök 2 gibi)."}
{k:"Matematik",s:"Vektör ile skaler arasındaki fark nedir?",o:["Fark yok","Vektör büyüklük ve yön skaler sadece büyüklük","Biri sayı biri harf","Biri pozitif biri negatif"],d:1,a:"Vektör hem büyüklük hem yön içerirken skaler sadece büyüklük ifade eder."}
{k:"Matematik",s:"Sinüs teoremi ne ifade eder?",o:["a/sinA = b/sinB = c/sinC","a^2=b^2+c^2","sin^2+cos^2=1","tan=sin/cos"],d:0,a:"Sinüs teoremi üçgenin kenarlarının karşı açılarının sinüsleriyle orantılı olduğunu gösterir."}
{k:"Matematik",s:"Kosinüs teoremi ne ifade eder?",o:["Sinüs kuralı","a^2 = b^2 + c^2 - 2bc cosA","tan kuralı","Alan formülü"],d:1,a:"Kosinüs teoremi herhangi bir üçgende kenarlar ve açılar arasındaki ilişkiyi verir."}
{k:"Deyimler",s:"Araba devrilince yol gösteren çok olur ne demektir?",o:["Trafik kuralı","İş işten geçtikten sonra akıl veren çok olur","Araba tamiri","Yol yapımı"],d:1,a:"Olay olduktan sonra akıl verip ne yapılması gerektiğini söyleyen çok olur."}
{k:"Deyimler",s:"Ayıkla pirincin taşını ne demektir?",o:["Pirinç temizlemek","Çok zor ve karmaşık bir durumu ifade eder","Yemek pişirmek","Tarla işi"],d:1,a:"İçinden çıkılması çok zor karmaşık bir durumu ifade eder."}
{k:"Deyimler",s:"Balık baştan kokar ne demektir?",o:["Balık pişirmek","Bozukluk yöneticiden başlar","Denize gitmek","Balık avlamak"],d:1,a:"Bir toplulukta bozukluk ve sorunlar önce yöneticiden başlar."}
{k:"Deyimler",s:"Dolap çevirmek ne demektir?",o:["Çamaşır yıkamak","Gizli entrikalar yapmak","Dans etmek","Mobilya taşımak"],d:1,a:"Gizlice hile ve entrika yapmak demektir."}
{k:"Deyimler",s:"Feleğin çemberinden geçmek ne demektir?",o:["Jimnastik","Çok sıkıntı ve zorluk çekmek","Sirk gösterisi","Halka geçirmek"],d:1,a:"Çok acı ve zorluk çekerek deneyim kazanmak demektir."}
{k:"Deyimler",s:"Hamam böceği gibi her yere girmek ne demektir?",o:["Temizlik","Her işe burnunu sokmak","Böcek ilaçlama","Seyahat"],d:1,a:"Her yere sokulup her işe burnunu sokan kişi için kullanılır."}
{k:"Deyimler",s:"İt ürür kervan yürür ne demektir?",o:["Hayvan bakımı","Kararlı olan eleştirilere aldırmaz","Seyahat","Avcılık"],d:1,a:"Amacına kararlı olan kişi boş eleştirilere aldırmaz yoluna devam eder."}
{k:"Deyimler",s:"Karınca kararınca ne demektir?",o:["Karınca bilgisi","Gücü ve imkanı ölçüsünde","Küçük iş","Böcek bilimi"],d:1,a:"Kendi gücü ve imkanı ölçüsünde elinden geldiğince demektir."}
{k:"Deyimler",s:"Kırk yılda bir ne demektir?",o:["40 yıl","Çok nadiren","Her gün","Bazen"],d:1,a:"Çok seyrek çok nadiren olan şeyler için kullanılır."}
{k:"Deyimler",s:"Mangalda kül bırakmamak ne demektir?",o:["Mangal yakmak","Çok kurnaz ve sinsi olmak","Temizlik","Yemek pişirmek"],d:1,a:"Çok kurnaz ve sinsi olmak hiçbir iz bırakmamak demektir."}
{k:"Deyimler",s:"Nalıncı keseri gibi kendine yontmak ne demektir?",o:["Marangozluk","Her şeyi kendi çıkarına göre yapmak","Ağaç işi","Taş yontmak"],d:1,a:"Her şeyi kendi çıkarına uygun hale getirmek demektir."}
{k:"Deyimler",s:"Öğretmene küsmekle cahil kalınır ne demektir?",o:["Okula gitmek","Kırgınlıkla kendine zarar verirsin","Öğretmenlik","Sınav"],d:1,a:"Sana faydası olan kişiye küsmek sadece sana zarar verir."}
{k:"Deyimler",s:"Söz gümüşse sükut altındır ne demektir?",o:["Metal fiyatları","Bazen susmak konuşmaktan değerlidir","Altın almak","Gümüş satmak"],d:1,a:"Bazen konuşmak yerine susmak daha değerli ve akıllıcadır."}
{k:"Deyimler",s:"Taş yerinde ağırdır ne demektir?",o:["Taş taşımak","İnsan kendi yerinde değerlidir","Ağırlık ölçmek","Dağ tırmanmak"],d:1,a:"İnsan kendi bulunduğu yerde kendi konumunda değerlidir."}
{k:"Deyimler",s:"Üzüm yemek ne anlama gelir (deyim olarak)?",o:["Meyve yemek","Asıl amacı bilmeden taklit etmek","Bağ bakmak","Şarap yapmak"],d:1,a:"Asıl amacı anlamadan sadece sonucuyla ilgilenmek (bağcıyı dövmek değil üzüm yemek)."}
{k:"Deyimler",s:"Yel kayadan ne koparır ne demektir?",o:["Rüzgar","Güçlü kişi küçük saldırıdan etkilenmez","Dağ tırmanma","Hava durumu"],d:1,a:"Güçlü ve dayanıklı kişi küçük saldırı ve eleştirilerden etkilenmez."}
{k:"Deyimler",s:"Zaman herşeyin ilacıdır ne demektir?",o:["İlaç almak","Zamanla acılar diner sorunlar çözülür","Saat almak","Doktor olmak"],d:1,a:"Zamanla acılar azalır yaralar iyileşir sorunlar çözüme kavuşur."}
{k:"Deyimler",s:"Aba altından sopa göstermek ne demektir?",o:["Kıyafet","Gizlice tehdit etmek","Spor yapmak","Hediye vermek"],d:1,a:"Belli etmeden üstü kapalı bir şekilde tehdit etmek demektir."}
{k:"Deyimler",s:"Dikine gitmek ne demektir?",o:["Yokuş çıkmak","İnatla kendi bildiğini yapmak","Yüzmek","Koşmak"],d:1,a:"Hiç kimsenin sözünü dinlemeyip inatla kendi bildiğini yapmak demektir."}
{k:"Deyimler",s:"Çıban başı olmak ne demektir?",o:["Hastalanmak","Sorunların kaynağı olmak","Doktor olmak","İlaç almak"],d:1,a:"Sorunların ve kötülüklerin asıl kaynağı ve sebebi olmak demektir."}
{k:"Deyimler",s:"Kaşık düşmanı ne demektir?",o:["Kaşık toplayan","Yemek konusunda seçici olan","Yemek yemek","Bulaşık yıkamak"],d:1,a:"Yemek seçen yemek konusunda çok titiz olan kişi için kullanılır."}
{k:"Deyimler",s:"Çuvaldızı kendine iğneyi başkasına batırmak ne demektir?",o:["Terzilik","Önce kendini eleştir sonra başkasını","Dikiş dikmek","İğne toplamak"],d:1,a:"Eleştiriye önce kendinden başlamak daha sonra başkalarını eleştirmek gerektiğini anlatır."}
{k:"Deyimler",s:"Kesenin ağzını açmak ne demektir?",o:["Çanta açmak","Para harcamaya başlamak","Alışveriş","Cüzdan almak"],d:1,a:"Cömertçe para harcamaya başlamak demektir."}
{k:"Deyimler",s:"Devlet kuşu konmak ne demektir?",o:["Kuş bakmak","Büyük bir şansa erişmek","Avcılık","Parkta gezmek"],d:1,a:"Büyük bir talih ve şansa erişmek beklenmedik bir fırsat yakalamak demektir."}
{k:"Deyimler",s:"Üç aşağı beş yukarı ne demektir?",o:["Matematik","Aşağı yukarı yaklaşık","Merdiven çıkmak","Asansör"],d:1,a:"Tam olarak olmasa da yaklaşık olarak aşağı yukarı demektir."}
{k:"Atasözleri",s:"Bilgi güçtür kimin sözüdür?",o:["Aristoteles","Francis Bacon","Newton","Platon"],d:1,a:"Bilgi güçtür sözü Francis Bacon a atfedilir."}
{k:"Atasözleri",s:"Her şeyin başı sağlık ne anlatır?",o:["Hastane","Sağlık tüm değerlerin temelidir","Spor","Doktor"],d:1,a:"Sağlık olmadan hiçbir şeyin değeri yoktur en önemli şey sağlıktır."}
{k:"Atasözleri",s:"Korkak bezirgan ne kar ne zarar eder ne demektir?",o:["Ticaret","Risk almayan kazanamaz","Korkmak","Kaçmak"],d:1,a:"Risk almayan kişi ne kazanır ne kaybeder yani hiçbir ilerleme kaydedemez."}
{k:"Atasözleri",s:"Dimyata pirince giderken evdeki bulgurdan olmak ne anlatır?",o:["Pirinç almak","Daha fazlasını isterken elindekini de kaybetmek","Yemek pişirmek","Seyahat"],d:1,a:"Daha fazlasını elde etmeye çalışırken elindekini de kaybetmeyi anlatır."}
{k:"Atasözleri",s:"Havlamak ile ısırmak bir değildir ne demektir?",o:["Köpek eğitimi","Tehdit eden her zaman yapamaz","Hayvan bakımı","Veteriner"],d:1,a:"Tehdit eden lafla söyleyen her zaman eyleme geçemez."}
{k:"Atasözleri",s:"İki cambaz bir ipte oynamaz ne anlatır?",o:["Sirk","İki rakip aynı yerde barınamaz","Jimnastik","Akrobasi"],d:1,a:"Aynı alanda iki güçlü rakip bir arada barınamaz."}
{k:"Atasözleri",s:"Kendi göbeğini kendin kes ne demektir?",o:["Doktorluk","Sorunlarını kendin çöz başkasını bekleme","Ameliyat","İlk yardım"],d:1,a:"Kendi sorunlarını kendin çöz başkalarından yardım bekleme."}
{k:"Atasözleri",s:"Mum yanmasa ışık vermez ne anlatır?",o:["Mum yakmak","Emek vermeden sonuç alınamaz","Karanlık","Elektrik"],d:1,a:"Bir şey elde etmek için emek fedakarlık ve çaba gerekir."}
{k:"Atasözleri",s:"Ne ekersen onu biçersin ne demektir?",o:["Tarım","Yaptıklarının sonuçlarıyla karşılaşırsın","Hasat","Ekim"],d:1,a:"İyi veya kötü ne yaparsan sonucuyla kendin karşılaşırsın."}
{k:"Atasözleri",s:"Otuz bir günde kırk haramileri ne anlatır?",o:["Masal","Her gün yeni bir sorunla karşılaşmak","Sayı saymak","Hırsızlık"],d:1,a:"Sürekli olarak yeni sorunlar ve sıkıntılarla karşılaşmak demektir."}
{k:"Atasözleri",s:"Parayı veren düdüğü çalar ne demektir?",o:["Müzik","Gücü ve parası olan istediğini yaptırır","Düdük almak","Konser"],d:1,a:"Para ve güç sahibi olan istediğini yaptırabilir karar verici odur."}
{k:"Atasözleri",s:"Sürüden ayrılan koyunu kurt kapar ne anlatır?",o:["Hayvancılık","Topluluktan ayrılan tehlikeye düşer","Çoban olmak","Kurt avı"],d:1,a:"Topluluktan ayrılıp yalnız kalan kişi tehlikelere karşı savunmasız kalır."}
{k:"Atasözleri",s:"Terzi kendi söküğünü dikemez ne demektir?",o:["Terzilik","Uzman bile kendi sorununu çözemeyebilir","Dikiş dikmek","Kumaş kesmek"],d:1,a:"Bir konuda uzman olan kişi bile kendi sorunlarını çözmekte zorlanabilir."}
{k:"Atasözleri",s:"Ucuz etin yahnisi yavan olur ne anlatır?",o:["Yemek tarifi","Kalitesiz malzeme kalitesiz sonuç verir","Et almak","Aşçılık"],d:1,a:"Düşük kaliteli malzeme veya ucuz iş kalitesiz sonuç doğurur."}
{k:"Atasözleri",s:"Vakit nakittir ne demektir?",o:["Saat almak","Zaman çok değerlidir boşa harcanmamalı","Para saymak","Banka"],d:1,a:"Zaman para kadar değerlidir verimli kullanılmalıdır."}
{k:"Atasözleri",s:"Yılan hikayesi ne demektir?",o:["Hayvan bilimi","Bir türlü bitmeyen iş veya anlatım","Masal okumak","Yılan avlamak"],d:1,a:"Bir türlü bitmeyen sonu gelmeyen uzun ve sıkıcı iş veya anlatım demektir."}
{k:"Atasözleri",s:"Zorla güzellik olmaz ne anlatır?",o:["Güzellik bakımı","İsteksiz yapılan iş iyi sonuç vermez","Makyaj","Estetik"],d:1,a:"Gönüllü olmayan zorla yaptırılan hiçbir iş güzel ve kaliteli olmaz."}
{k:"Atasözleri",s:"Alet işler el övünür ne demektir?",o:["Alet satmak","İyi araç gereç başarıyı artırır","Tamir","Fabrika"],d:1,a:"Doğru aletlerle çalışan kişi daha iyi sonuç alır."}
{k:"Atasözleri",s:"Cahile söz anlatmak deveye hendek atlatmaktan zordur ne anlatır?",o:["Deve bakımı","Bilgisiz kişiye bir şey anlatmak çok zordur","Hendek kazmak","Hayvanat bahçesi"],d:1,a:"Bilgisiz ve inatçı bir kişiye bir şeyi anlatmak veya kabul ettirmek çok zordur."}
{k:"Atasözleri",s:"Deli ile damda oturma ya o seni iter ya sen onu ne demektir?",o:["İnşaat","Akılsız kişiyle iş yapmak tehlikelidir","Çatı tamiri","Yükseklik korkusu"],d:1,a:"Aklı başında olmayan kişiyle iş birliği yapmak tehlikelidir eninde sonunda sorun çıkar."}
{k:"Atasözleri",s:"Elinin hamuruyla erkek işine karışma ne anlatır?",o:["Yemek yapmak","Bilmediğin işe karışma","Hamur yoğurmak","Fırın"],d:1,a:"Bilmediğin ve uzmanlığın olmayan işlere karışma demektir."}
{k:"Atasözleri",s:"Güvenme varlığa düşersin darlığa ne demektir?",o:["Zenginlik","Sahip olduklarına güvenip savurganlık yapma","Banka","Yatırım"],d:1,a:"Elindeki varlığa güvenip savurganlık yaparsan bir gün darlığa düşebilirsin."}
{k:"Atasözleri",s:"Her gece karanlık olmaz ne anlatır?",o:["Astronomi","Kötü günler sona erer","Gece lambası","Uyumak"],d:1,a:"Her zorluk geçicidir kötü günlerin ardından iyi günler gelir."}
{k:"Atasözleri",s:"İnsanı tanımak kolay anlamak zordur ne demektir?",o:["Psikoloji","İnsanı dışından görmek kolay içini anlamak zordur","Fotoğrafçılık","Resim"],d:1,a:"İnsanın dış görünüşünü bilmek kolaydır ama gerçek karakterini anlamak çok zordur."}
{k:"Atasözleri",s:"Kadıya mülk (ev) geçmez ne anlatır?",o:["Gayrimenkul","Geçici görevdekine sürekli mal verilmez","Kadı olmak","Ev almak"],d:1,a:"Geçici bir görevde bulunan kişiye kalıcı bir mülk verilmez."}

{k:"Coğrafya",s:"Bermuda Şeytan Üçgeni hangi okyanustadır?",o:["Hint Okyanusu","Pasifik","Atlantik","Arktik"],d:2,a:"Bermuda Üçgeni Kuzey Atlantik'tedir."}
{k:"Coğrafya",s:"Dünyanın en büyük mercan resifi hangisidir?",o:["Kızıldeniz Resifi","Büyük Set Resifi","Belize Resifi","Raja Ampat"],d:1,a:"Büyük Set Resifi Avustralya kıyılarındadır."}

{k:"Başkentler",s:"Gürcistan'ın başkenti neresidir?",o:["Batum","Tiflis","Kutaisi","Suhumi"],d:1,a:"Gürcistan'ın başkenti Tiflis'tir."}
{k:"Başkentler",s:"Hırvatistan'ın başkenti neresidir?",o:["Split","Dubrovnik","Zagreb","Rijeka"],d:2,a:"Hırvatistan'ın başkenti Zagreb'dir."}
{k:"Başkentler",s:"Sırbistan'ın başkenti neresidir?",o:["Novi Sad","Belgrad","Niş","Kragujevac"],d:1,a:"Sırbistan'ın başkenti Belgrad'dır."}
{k:"Başkentler",s:"Slovenya'nın başkenti neresidir?",o:["Maribor","Koper","Ljubljana","Celje"],d:2,a:"Slovenya'nın başkenti Ljubljana'dır."}
{k:"Başkentler",s:"Letonya'ın başkenti neresidir?",o:["Daugavpils","Riga","Liepaja","Jurmala"],d:1,a:"Letonya'nın başkenti Riga'dır."}
{k:"Başkentler",s:"Litvanya'nın başkenti neresidir?",o:["Kaunas","Klaipeda","Vilnius","Şiauliai"],d:2,a:"Litvanya'nın başkenti Vilnius'tur."}
{k:"Başkentler",s:"Estonya'nın başkenti neresidir?",o:["Tartu","Tallinn","Narva","Pärnu"],d:1,a:"Estonya'nın başkenti Tallinn'dir."}
{k:"Başkentler",s:"Moldova'nın başkenti neresidir?",o:["Tiraspol","Bălți","Kişinev","Cahul"],d:2,a:"Moldova'nın başkenti Kişinev'dir."}
{k:"Başkentler",s:"Kuzey Makedonya'nın başkenti neresidir?",o:["Bitola","Üsküp","Ohrid","Kumanovo"],d:1,a:"Kuzey Makedonya'nın başkenti Üsküp'tür."}
{k:"Başkentler",s:"Karadağ'ın başkenti neresidir?",o:["Podgorica","Nikşiç","Kotor","Budva"],d:0,a:"Karadağ'ın başkenti Podgorica'dır."}

{k:"Doğa",s:"Fotosentez sırasında bitkiler hangi gazı açığa çıkarır?",o:["Karbondioksit","Azot","Oksijen","Hidrojen"],d:2,a:"Fotosentezde bitkiler oksijen üretir."}
{k:"Doğa",s:"Hangi hayvan en uzun göç yolculuğu yapar?",o:["Kuzey Kırlangıcı","Kutup Sumru","Balina","Kelebek"],d:1,a:"Kutup sumru yılda ~70.000 km göç eder."}
{k:"Doğa",s:"Mantarlar hangi aleme aittir?",o:["Bitkiler","Hayvanlar","Fungi","Protista"],d:2,a:"Mantarlar Fungi (Mantarlar) alemine aittir."}
{k:"Doğa",s:"En hızlı büyüyen bitki hangisidir?",o:["Bambu","Söğüt","Kavak","Çam"],d:0,a:"Bambu günde 91 cm'ye kadar büyüyebilir."}
{k:"Doğa",s:"Hangi organ insan vücudunun en büyük organıdır?",o:["Karaciğer","Beyin","Deri","Akciğer"],d:2,a:"Deri insan vücudunun en büyük organıdır."}
{k:"Doğa",s:"Bir arı kovanında kraliçe arı kaç yıl yaşar?",o:["1 yıl","2-3 yıl","5-7 yıl","10 yıl"],d:2,a:"Kraliçe arı ortalama 5-7 yıl yaşar."}
{k:"Doğa",s:"DNA'nın açılımı nedir?",o:["Deoksiribonükleik Asit","Diribonükleik Asit","Dinükleotid Amino","Deoksi Nükleik Amino"],d:0,a:"DNA Deoksiribonükleik Asit anlamına gelir."}
{k:"Doğa",s:"Hangi element insan vücudunda en çok bulunur?",o:["Karbon","Hidrojen","Oksijen","Azot"],d:2,a:"İnsan vücudunun %65'i oksijenden oluşur."}
{k:"Doğa",s:"Ekosistemde ayrıştırıcıların görevi nedir?",o:["Enerji üretmek","Ölü maddeleri parçalamak","Avlanmak","Fotosentez yapmak"],d:1,a:"Ayrıştırıcılar ölü organik maddeleri parçalar."}
{k:"Doğa",s:"Hangi biyom dünya yüzeyinin en geniş alanını kaplar?",o:["Çöl","Tropikal Orman","Tayga","Savan"],d:2,a:"Tayga (kuzey iğne yapraklı orman) en geniş biyomdur."}
{k:"Doğa",s:"Plazmodik bölünme hangi canlılarda görülür?",o:["Bakterilerde","Bitkilerde","Cıvık mantarlarda","Hayvanlarda"],d:2,a:"Plazmodik bölünme cıvık mantarlarda görülür."}
{k:"Doğa",s:"Kaç tür kan grubu vardır?",o:["3","4","6","8"],d:3,a:"ABO (4 ana grup) ve Rh (+/-) ile birlikte 8 kan grubu vardır."}
{k:"Doğa",s:"Endemik tür ne demektir?",o:["Nesli tükenen tür","Sadece belirli bölgede yaşayan","Göçmen tür","Evcilleştirilmiş tür"],d:1,a:"Endemik tür yalnızca belirli bir coğrafi bölgede yaşar."}
{k:"Doğa",s:"İnsan genomunda yaklaşık kaç gen bulunur?",o:["5.000","20.000","100.000","1.000.000"],d:1,a:"İnsan genomunda yaklaşık 20.000-25.000 gen vardır."}
{k:"Doğa",s:"Hangi vitamin eksikliği raşitizme neden olur?",o:["A vitamini","B vitamini","C vitamini","D vitamini"],d:3,a:"D vitamini eksikliği kemik yumuşaması (raşitizm) yapar."}
{k:"Doğa",s:"Klorofil hangi renk ışığı en çok emer?",o:["Yeşil","Kırmızı ve Mavi","Sarı","Turuncu"],d:1,a:"Klorofil kırmızı ve mavi dalga boylarını emer, yeşili yansıtır."}
{k:"Doğa",s:"Ozon tabakası atmosferin hangi katmanındadır?",o:["Troposfer","Stratosfer","Mezosfer","Termosfer"],d:1,a:"Ozon tabakası stratosfer katmanındadır."}
{k:"Doğa",s:"Simbiyoz ilişki türlerinden hangisi her iki canlıya da yarar sağlar?",o:["Parazitizm","Kommensalizm","Mutualizm","Predatörlük"],d:2,a:"Mutualizm her iki canlının da fayda gördüğü ilişkidir."}
{k:"Doğa",s:"Kromozom sayısı insanda kaçtır?",o:["23","44","46","48"],d:2,a:"İnsanda 46 kromozom (23 çift) bulunur."}
{k:"Doğa",s:"Hangi canlı grubu hem karada hem suda yaşar?",o:["Sürüngenler","Amfibiler","Memeliler","Balıklar"],d:1,a:"Amfibiler (kurbağalar vb.) hem karada hem suda yaşar."}

{k:"Türkiye",s:"Türkiye'nin en uzun nehri hangisidir?",o:["Fırat","Kızılırmak","Sakarya","Dicle"],d:1,a:"Kızılırmak 1355 km ile Türkiye'nin en uzun nehridir."}
{k:"Türkiye",s:"Kapadokya hangi ildedir?",o:["Kayseri","Nevşehir","Aksaray","Niğde"],d:1,a:"Kapadokya'nın merkezi Nevşehir'dedir."}
{k:"Türkiye",s:"Türkiye'nin en yüksek gölü hangisidir?",o:["Van Gölü","Çıldır Gölü","Balık Gölü","Süphan Gölü"],d:2,a:"Balık Gölü (Ağrı) ~2241 m ile en yüksek göldür."}
{k:"Türkiye",s:"Anadolu'da kurulan ilk Türk beyliği hangisidir?",o:["Danişmentliler","Saltuklar","Mengücekliler","Artuklular"],d:1,a:"Saltuklular Anadolu'daki ilk Türk beyliklerinden kabul edilir."}
{k:"Türkiye",s:"Efes Antik Kenti hangi ildedir?",o:["Muğla","Aydın","İzmir","Denizli"],d:2,a:"Efes Antik Kenti İzmir Selçuk ilçesindedir."}
{k:"Türkiye",s:"Türkiye'nin en büyük adası hangisidir?",o:["Bozcaada","Gökçeada","Büyükada","Akdamar"],d:1,a:"Gökçeada (Çanakkale) Türkiye'nin en büyük adasıdır."}
{k:"Türkiye",s:"Sümela Manastırı hangi ildedir?",o:["Rize","Artvin","Trabzon","Giresun"],d:2,a:"Sümela Manastırı Trabzon Maçka ilçesindedir."}
{k:"Türkiye",s:"Türkiye Cumhuriyeti'nin ilk anayasası hangi yıl kabul edildi?",o:["1921","1923","1924","1926"],d:2,a:"İlk kapsamlı anayasa 1924 Teşkilât-ı Esasiye Kanunu'dur."}
{k:"Türkiye",s:"Hatay hangi yıl Türkiye'ye katıldı?",o:["1936","1938","1939","1940"],d:2,a:"Hatay 1939'da Türkiye'ye katılmıştır."}
{k:"Türkiye",s:"Aspendos Antik Tiyatrosu hangi ildedir?",o:["Mersin","Antalya","Adana","Burdur"],d:1,a:"Aspendos Antalya Serik ilçesindedir."}
{k:"Türkiye",s:"Türkiye'nin ilk kadın pilotu kimdir?",o:["Sabiha Gökçen","Bedriye Tahir","Yıldız Uçansu","Leman Bozkurt"],d:0,a:"Sabiha Gökçen dünyanın ilk kadın savaş pilotudur."}
{k:"Türkiye",s:"İstanbul Boğazı hangi iki denizi birleştirir?",o:["Akdeniz-Ege","Karadeniz-Marmara","Marmara-Ege","Karadeniz-Akdeniz"],d:1,a:"İstanbul Boğazı Karadeniz ile Marmara Denizi'ni birleştirir."}
{k:"Türkiye",s:"Göbeklitepe hangi ildedir?",o:["Diyarbakır","Şanlıurfa","Mardin","Gaziantep"],d:1,a:"Göbeklitepe Şanlıurfa'dadır ve dünyanın en eski tapınağıdır."}
{k:"Türkiye",s:"Türkiye'nin en uzun tüneli hangisidir?",o:["Bolu Tüneli","Ovit Tüneli","Zigana Tüneli","Ilgaz Tüneli"],d:1,a:"Ovit Tüneli 14.3 km ile Türkiye'nin en uzun karayolu tünelidir."}
{k:"Türkiye",s:"Zeugma Mozaik Müzesi hangi ildedir?",o:["Adıyaman","Gaziantep","Şanlıurfa","Malatya"],d:1,a:"Zeugma Mozaik Müzesi Gaziantep'tedir."}
{k:"Türkiye",s:"Safranbolu hangi ilin ilçesidir?",o:["Çankırı","Kastamonu","Karabük","Bartın"],d:2,a:"Safranbolu Karabük iline bağlı UNESCO Dünya Mirasıdır."}
{k:"Türkiye",s:"Türkiye'nin en kalabalık ikinci şehri hangisidir?",o:["İzmir","Ankara","Bursa","Antalya"],d:1,a:"Ankara nüfus olarak Türkiye'nin ikinci büyük şehridir."}
{k:"Türkiye",s:"Nemrut Dağı hangi ildedir?",o:["Bitlis","Adıyaman","Malatya","Elazığ"],d:1,a:"Nemrut Dağı (Kommagene) Adıyaman'dadır."}
{k:"Türkiye",s:"Türkiye'nin en derin gölü hangisidir?",o:["Van Gölü","Tortum Gölü","Hazar Gölü","Çıldır Gölü"],d:2,a:"Hazar Gölü (Elazığ) ~216 m derinlikle en derin göldür."}
{k:"Türkiye",s:"Ani Harabeleri hangi ildedir?",o:["Ağrı","Kars","Iğdır","Erzurum"],d:1,a:"Ani Harabeleri Kars'ta yer alır, UNESCO Dünya Mirasıdır."}
{k:"Türkiye",s:"Çanakkale Savaşı hangi yıl başladı?",o:["1914","1915","1916","1917"],d:1,a:"Çanakkale Savaşı 1915'te başlamıştır."}
{k:"Türkiye",s:"Pamukkale travertenleri hangi ildedir?",o:["Aydın","Burdur","Denizli","Muğla"],d:2,a:"Pamukkale Denizli'dedir, UNESCO Dünya Mirasıdır."}
{k:"Türkiye",s:"Türkiye'nin ilk cumhurbaşkanı kimdir?",o:["İsmet İnönü","Mustafa Kemal Atatürk","Celal Bayar","Fevzi Çakmak"],d:1,a:"Mustafa Kemal Atatürk Türkiye'nin ilk cumhurbaşkanıdır."}
{k:"Türkiye",s:"Mardin'in mimari özelliği nedir?",o:["Ahşap evler","Taş evler ve medreseler","Kerpiç yapılar","Betonarme binalar"],d:1,a:"Mardin taş mimarisi ve medreseleriyle ünlüdür."}

{k:"Spor",s:"FIFA Dünya Kupası ilk kez hangi yıl düzenlendi?",o:["1926","1930","1934","1938"],d:1,a:"İlk Dünya Kupası 1930'da Uruguay'da yapıldı."}
{k:"Spor",s:"Olimpiyat halkaları kaç tanedir?",o:["4","5","6","7"],d:1,a:"5 halka 5 kıtayı temsil eder."}
{k:"Spor",s:"Wimbledon turnuvası hangi spor dalındadır?",o:["Golf","Tenis","Kriket","Badminton"],d:1,a:"Wimbledon dünyanın en prestijli tenis turnuvasıdır."}
{k:"Spor",s:"NBA hangi ülkenin basketbol liginin kısaltmasıdır?",o:["Kanada","İngiltere","ABD","Avustralya"],d:2,a:"NBA (National Basketball Association) ABD liginin kısaltmasıdır."}
{k:"Spor",s:"Bir maraton kaç kilometredir?",o:["40 km","42.195 km","45 km","50 km"],d:1,a:"Maraton mesafesi 42.195 km'dir."}
{k:"Spor",s:"Formula 1'de en çok şampiyonluk kazanan pilot kimdir?",o:["Ayrton Senna","Michael Schumacher","Lewis Hamilton","Sebastian Vettel"],d:2,a:"Lewis Hamilton 7 şampiyonlukla rekor sahibidir (Schumacher ile birlikte)."}
{k:"Spor",s:"Voleybolda bir takım kaç kişiden oluşur?",o:["5","6","7","8"],d:1,a:"Voleybolda sahada 6 oyuncu bulunur."}
{k:"Spor",s:"Bir buz hokeyi maçı kaç periyottan oluşur?",o:["2","3","4","5"],d:1,a:"Buz hokeyi 3 periyottan oluşur."}
{k:"Spor",s:"Hangi ülke en çok olimpiyat altın madalyası kazanmıştır?",o:["Çin","Rusya","ABD","İngiltere"],d:2,a:"ABD tarihte en çok olimpiyat altın madalyası kazanan ülkedir."}
{k:"Spor",s:"Bir kriket maçında bir takım kaç oyuncudan oluşur?",o:["9","10","11","12"],d:2,a:"Krikette bir takım 11 oyuncudan oluşur."}
{k:"Spor",s:"Tour de France hangi spor dalında düzenlenir?",o:["Koşu","Bisiklet","Yüzme","Triatlon"],d:1,a:"Tour de France dünyanın en ünlü bisiklet yarışıdır."}
{k:"Spor",s:"Bir rugby takımı kaç kişidir?",o:["11","13","15","17"],d:2,a:"Rugby Union'da bir takım 15 kişidir."}
{k:"Spor",s:"Usain Bolt 100 metreyi kaç saniyede koşmuştur?",o:["9.38","9.58","9.72","9.84"],d:1,a:"Usain Bolt 100 metre dünya rekoru 9.58 saniyedir."}
{k:"Spor",s:"Bir golf sahasında kaç delik bulunur?",o:["9","12","16","18"],d:3,a:"Standart bir golf sahasında 18 delik bulunur."}
{k:"Spor",s:"Beyzbolda atıcıya ne denir?",o:["Pitcher","Catcher","Batter","Shortstop"],d:0,a:"Beyzbolda top atan oyuncuya Pitcher denir."}
{k:"Spor",s:"Türkiye'nin ilk olimpiyat altın madalyası hangi spor dalındandır?",o:["Halter","Güreş","Atletizm","Boks"],d:1,a:"Türkiye'nin ilk altın madalyası 1936'da güreştedir."}
{k:"Spor",s:"Super Bowl hangi sporun şampiyonluk maçıdır?",o:["Beyzbol","Basketbol","Amerikan Futbolu","Buz Hokeyi"],d:2,a:"Super Bowl NFL (Amerikan Futbolu) şampiyonluk maçıdır."}
{k:"Spor",s:"Bir polo maçında bir takım kaç biniciden oluşur?",o:["2","3","4","5"],d:2,a:"Poloda her takım 4 biniciden oluşur."}
{k:"Spor",s:"2024 Yaz Olimpiyatları hangi şehirde yapıldı?",o:["Tokyo","Los Angeles","Paris","Londra"],d:2,a:"2024 Yaz Olimpiyatları Paris'te düzenlendi."}
{k:"Spor",s:"Bir tenis setinde kaç game kazanmak gerekir?",o:["4","5","6","7"],d:2,a:"Normal sette 6 game kazanmak gerekir (tie-break hariç)."}
{k:"Spor",s:"Fenerbahçe hangi yıl kurulmuştur?",o:["1903","1905","1907","1909"],d:2,a:"Fenerbahçe 1907'de kurulmuştur."}
{k:"Spor",s:"Galatasaray hangi yıl UEFA Kupası'nı kazandı?",o:["1998","1999","2000","2001"],d:2,a:"Galatasaray 2000 yılında UEFA Kupası'nı kazandı."}
{k:"Spor",s:"Dünya Kupası'nı en çok kazanan ülke hangisidir?",o:["Almanya","Arjantin","İtalya","Brezilya"],d:3,a:"Brezilya 5 kez Dünya Kupası kazanmıştır."}
{k:"Spor",s:"Bir hentbol maçı kaç dakikadır?",o:["40","50","60","70"],d:2,a:"Hentbol maçı 2x30=60 dakikadır."}
{k:"Spor",s:"Bir yüzme olimpik havuzu kaç metredir?",o:["25 m","33 m","50 m","100 m"],d:2,a:"Olimpik yüzme havuzu 50 metre uzunluğundadır."}

{k:"Matematik",s:"Pi sayısının ilk 5 basamağı nedir?",o:["3.14159","3.14169","3.15159","3.14259"],d:0,a:"Pi sayısı 3.14159265... şeklinde devam eder."}
{k:"Matematik",s:"Bir üçgenin iç açıları toplamı kaç derecedir?",o:["90°","180°","270°","360°"],d:1,a:"Üçgenin iç açıları toplamı 180 derecedir."}
{k:"Matematik",s:"Fibonacci dizisinde 1, 1, 2, 3'ten sonra gelen sayı nedir?",o:["4","5","6","7"],d:1,a:"Fibonacci dizisinde 2+3=5'tir."}
{k:"Matematik",s:"Bir küpün kaç yüzü vardır?",o:["4","5","6","8"],d:2,a:"Bir küpün 6 yüzü vardır."}
{k:"Matematik",s:"0! (sıfır faktöriyel) kaçtır?",o:["0","1","Tanımsız","Sonsuz"],d:1,a:"0! = 1 olarak tanımlanır."}
{k:"Matematik",s:"Bir çemberin çevresi hangi formülle hesaplanır?",o:["πr²","2πr","πd²","r²"],d:1,a:"Çemberin çevresi 2πr formülüyle hesaplanır."}
{k:"Matematik",s:"Karekök 144 kaçtır?",o:["11","12","13","14"],d:1,a:"√144 = 12'dir."}
{k:"Matematik",s:"Bir doğal sayının karesinin birler basamağı 2 olabilir mi?",o:["Evet","Hayır","Bazen","Sadece çift sayılarda"],d:1,a:"Hiçbir tam karenin birler basamağı 2 olamaz."}
{k:"Matematik",s:"log₁₀(1000) kaçtır?",o:["2","3","4","10"],d:1,a:"10³=1000 olduğundan log₁₀(1000)=3'tür."}
{k:"Matematik",s:"Bir altıgenin iç açıları toplamı kaç derecedir?",o:["540°","630°","720°","810°"],d:2,a:"Altıgenin iç açıları toplamı (6-2)×180=720 derecedir."}
{k:"Matematik",s:"İki paralel doğruyu bir kesenle kestiğimizde oluşan yöndeş açılar nasıldır?",o:["Tamamlayıcı","Bütünler","Eşit","Ters"],d:2,a:"Yöndeş açılar birbirine eşittir."}
{k:"Matematik",s:"Asal sayıların en küçüğü hangisidir?",o:["0","1","2","3"],d:2,a:"2 en küçük asal sayıdır."}
{k:"Matematik",s:"Bir silindirin hacmi hangi formülle bulunur?",o:["πr²h","2πrh","4/3πr³","πr²"],d:0,a:"Silindir hacmi V=πr²h formülüyle hesaplanır."}
{k:"Matematik",s:"Euler sabiti (e) yaklaşık olarak kaçtır?",o:["1.618","2.718","3.141","4.236"],d:1,a:"Euler sabiti e ≈ 2.71828'dir."}
{k:"Matematik",s:"Bir dik üçgende hipotenüs nasıl bulunur?",o:["a+b","a×b","√(a²+b²)","a²+b²"],d:2,a:"Pisagor teoremine göre hipotenüs = √(a²+b²)"},
{k:"Matematik",s:"sin 30° kaçtır?",o:["0","1/2","√2/2","√3/2"],d:1,a:"sin 30° = 1/2'dir."}
{k:"Matematik",s:"Bir matrisin determinantı 0 ise ne olur?",o:["Tersi vardır","Tersi yoktur","Birim matristir","Simetrik matristir"],d:1,a:"Determinantı 0 olan matrisin tersi yoktur (tekil matris)."}
{k:"Matematik",s:"İki kümenin kesişimi ne anlama gelir?",o:["Tüm elemanlar","Ortak elemanlar","Fark elemanları","Boş küme"],d:1,a:"Kesişim iki kümenin ortak elemanlarının kümesidir."}
{k:"Matematik",s:"Bir fonksiyonun türevi neyi verir?",o:["Alan","Eğim","Hacim","Uzunluk"],d:1,a:"Türev fonksiyonun o noktadaki eğimini verir."}
{k:"Matematik",s:"Bir olayın olasılığı en fazla kaç olabilir?",o:["0.5","0.99","1","Sonsuz"],d:2,a:"Olasılık değerleri 0 ile 1 arasındadır, en fazla 1 olabilir."}
{k:"Matematik",s:"∫(2x)dx integrali nedir?",o:["x²","x²+C","2x²","2x²+C"],d:1,a:"∫2x dx = x² + C'dir."}
{k:"Matematik",s:"Bir çokgenin köşegen sayısı formülü nedir?",o:["n(n-1)/2","n(n-3)/2","n(n-2)/2","n²/2"],d:1,a:"Köşegen sayısı n(n-3)/2 formülüyle hesaplanır."}
{k:"Matematik",s:"i² (sanal birim karesi) kaçtır?",o:["1","-1","i","0"],d:1,a:"Sanal birim i'nin karesi -1'dir: i²=-1."}
{k:"Matematik",s:"Bir kümede 5 eleman varsa, alt küme sayısı kaçtır?",o:["10","16","25","32"],d:3,a:"Alt küme sayısı 2⁵=32'dir."}
{k:"Matematik",s:"Aritmetik dizide ortak fark sabit ise dizi nasıl adlandırılır?",o:["Geometrik","Harmonik","Aritmetik","Fibonacci"],d:2,a:"Ardışık terimler arası farkı sabit olan dizi aritmetik dizidir."}

{k:"Deyimler",s:"'Ayağını denk almak' ne demektir?",o:["Hızlı koşmak","Dikkatli davranmak","Yürümeye başlamak","Engel olmak"],d:1,a:"Ayağını denk almak: dikkatli ve tedbirli davranmak."}
{k:"Deyimler",s:"'Kılı kırk yarmak' ne anlama gelir?",o:["Saç kesmek","Titiz davranmak","Sinirli olmak","Zorluk çekmek"],d:1,a:"Kılı kırk yarmak: çok titiz ve ayrıntıcı davranmak."}
{k:"Deyimler",s:"'Taşı gediğine koymak' ne demektir?",o:["İnşaat yapmak","Yerinde söz söylemek","Taş toplamak","Duvar örmek"],d:1,a:"Taşı gediğine koymak: yerinde ve uygun söz söylemek."}
{k:"Deyimler",s:"'Çam devirmek' ne anlama gelir?",o:["Ağaç kesmek","Büyük gaf yapmak","Güçlü olmak","Başarılı olmak"],d:1,a:"Çam devirmek: istemeden büyük bir pot kırmak, gaf yapmak."}
{k:"Deyimler",s:"'Pabucu dama atılmak' ne demektir?",o:["Pabuç kaybetmek","Önemini kaybetmek","Yükseğe çıkmak","Hediye almak"],d:1,a:"Pabucu dama atılmak: değerini, önemini yitirmek."}
{k:"Deyimler",s:"'Çenesi düşük' ne anlama gelir?",o:["Çenesi ağrıyan","Çok konuşan","Sessiz olan","Dişçiye giden"],d:1,a:"Çenesi düşük: çok ve gereksiz konuşan kişi."}
{k:"Deyimler",s:"'Araba devrilince yol gösteren çok olur' ne demektir?",o:["Trafik kuralı","İş işten geçince akıl veren çoğalır","Araba tamiri","Yardımseverlik"],d:1,a:"İş işten geçtikten sonra akıl veren, eleştiren çok olur."}
{k:"Deyimler",s:"'Balık kavağa çıkınca' ne anlama gelir?",o:["İmkânsız bir durum","Balık avı","Ağaç tırmanma","Doğa olayı"],d:0,a:"Olmayacak, imkânsız bir durumu ifade eder."}
{k:"Deyimler",s:"'Kendi göbeğini kendi kesmek' ne demektir?",o:["Doğum yapmak","Kendi sorununu kendi çözmek","Diyet yapmak","Ameliyat olmak"],d:1,a:"Kendi sorunlarını başkasına muhtaç olmadan çözmek."}
{k:"Deyimler",s:"'Saman altından su yürütmek' ne anlama gelir?",o:["Çiftçilik","Gizlice iş çevirmek","Sulama yapmak","Temizlik yapmak"],d:1,a:"Gizliden gizliye, kimseye belli etmeden iş çevirmek."}
{k:"Deyimler",s:"'Yüzüne gözüne bulaştırmak' ne demektir?",o:["Makyaj yapmak","Bir işi becerememek","Yemek dökmek","Boyama yapmak"],d:1,a:"Yapılan işi becerememek, berbat etmek."}
{k:"Deyimler",s:"'Devede kulak' ne anlama gelir?",o:["Büyük kulak","Çok az, önemsiz","Deve bakımı","Hayvan hastalığı"],d:1,a:"Devede kulak: büyük bir şeye oranla çok az olan."}
{k:"Deyimler",s:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",o:["Yangın uyarısı","Her söylentinin bir gerçeklik payı var","Duman zararlıdır","Ateş söndürme"],d:1,a:"Her dedikodunun, söylentinin bir dayanağı vardır."}
{k:"Deyimler",s:"'Bin dereden su getirmek' ne anlama gelir?",o:["Susuzluk","Bir şeyi yapmamak için bahaneler uydurmak","Su taşımak","Çok çalışmak"],d:1,a:"Bir işten kaçmak için çeşitli bahaneler öne sürmek."}
{k:"Deyimler",s:"'Kulağı kirişte olmak' ne demektir?",o:["Kulağı ağrımak","Dikkatle dinlemek, tetikte olmak","Müzik dinlemek","Kulak tıkanması"],d:1,a:"Her an olan biteni dikkatle dinlemek, tetikte olmak."}
{k:"Deyimler",s:"'El elden üstündür' ne anlama gelir?",o:["Alkış","Her zaman daha iyisi vardır","El sıkışma","Güreş terimi"],d:1,a:"Ne kadar başarılı olursan ol, senden daha iyisi mutlaka vardır."}
{k:"Deyimler",s:"'Dağ fare doğurdu' ne demektir?",o:["Doğa olayı","Büyük beklentiden küçük sonuç çıkması","Hayvan doğumu","Dağcılık"],d:1,a:"Büyük hazırlık ve beklentinin ardından önemsiz bir sonuç çıkması."}
{k:"Deyimler",s:"'Çıkmadık candan umut kesilmez' ne anlama gelir?",o:["Tıp terimi","Yaşadığı sürece umut vardır","Ölüm haberi","Hastane kuralı"],d:1,a:"İnsan hayatta olduğu sürece her zaman umut vardır."}
{k:"Deyimler",s:"'Kaşla göz arasında' ne demektir?",o:["Makyaj","Çok kısa sürede, hemen","Göz hastalığı","Yüz ifadesi"],d:1,a:"Çok kısa bir süre içinde, kimse farkına varmadan."}
{k:"Deyimler",s:"'Baklayı ağzından çıkarmak' ne anlama gelir?",o:["Yemek yemek","Gizli tuttuğu şeyi söylemek","Dişçiye gitmek","Nefes egzersizi"],d:1,a:"Sakladığı sırrı, gizlediği şeyi açığa vurmak."}
{k:"Deyimler",s:"'Dikme çınarı gölgesinde oturmak' ne anlama gelir?",o:["Bahçecilik","Başkasının emeğinden yararlanmak","Park gezisi","Ağaç dikmek"],d:1,a:"Başkasının kurduğu düzenin, emeğin nimetlerinden faydalanmak."}
{k:"Deyimler",s:"'Gemisini yürüten kaptandır' ne demektir?",o:["Denizcilik kuralı","Herkes kendi çıkarına bakar","Kaptan eğitimi","Gemi yarışı"],d:1,a:"Herkes kendi işini becermeye, çıkarını korumaya bakar."}
{k:"Deyimler",s:"'İğneyi kendine çuvaldızı başkasına batır' ne anlama gelir?",o:["Terzilik","Önce kendini eleştir","İğne yapımı","Dikiş kursu"],d:1,a:"Başkasını eleştirmeden önce kendine bak."}
{k:"Deyimler",s:"'Su uyur düşman uyumaz' ne demektir?",o:["Su tasarrufu","Düşman her zaman tetikte olabilir","Uyku düzeni","Nehir akışı"],d:1,a:"Her şey sakin görünse de düşman her zaman hazırdır."}
{k:"Deyimler",s:"'Yangından mal kaçırır gibi' ne demektir?",o:["İtfaiyecilik","Çok acele ve telaşla","Hırsızlık","Taşınma"],d:1,a:"Son derece aceleyle, büyük telaş içinde bir işi yapmak."}

{k:"Atasözleri",s:"'Ak akçe kara gün içindir' ne anlama gelir?",o:["Renk bilgisi","Zor günler için para biriktirmek","Banka reklamı","Madeni para"],d:1,a:"İleride karşılaşılabilecek sıkıntılar için önceden para biriktirmek."}
{k:"Atasözleri",s:"'Ağaç yaşken eğilir' ne demektir?",o:["Bahçecilik","Eğitim küçük yaşta başlamalı","Ağaç budama","Orman bakımı"],d:1,a:"İnsan küçük yaşta eğitilir, büyüyünce alışkanlık değiştirmek zordur."}
{k:"Atasözleri",s:"'Her yokuşun bir inişi vardır' ne anlama gelir?",o:["Yol yapımı","Her zorluğun ardından kolaylık gelir","Dağcılık","Trafik kuralı"],d:1,a:"Sıkıntılı dönemler sonunda sona erer."}
{k:"Atasözleri",s:"'Sakla samanı gelir zamanı' ne demektir?",o:["Çiftçilik","Her şeyin lazım olacağı bir gün gelir","Saman satışı","Depolama"],d:1,a:"İşe yaramaz görünen şey ileride gerekebilir."}
{k:"Atasözleri",s:"'Damlaya damlaya göl olur' ne anlama gelir?",o:["Su döngüsü","Küçük birikimler büyük sonuçlar doğurur","Göl oluşumu","Yağmur yağışı"],d:1,a:"Küçük birikimlerin zamanla büyük kazanımlara dönüşeceğini anlatır."}
{k:"Atasözleri",s:"'Balık baştan kokar' ne demektir?",o:["Yemek tarifi","Bozukluk yöneticiden başlar","Balıkçılık","Mutfak hijyeni"],d:1,a:"Bir topluluktaki sorun, yöneticilerden kaynaklanır."}
{k:"Atasözleri",s:"'Komşu komşunun külüne muhtaçtır' ne anlama gelir?",o:["Kül temizliği","İnsanlar birbirine ihtiyaç duyar","Komşu kavgası","Kül kullanımı"],d:1,a:"Herkes bir gün komşusuna muhtaç olabilir."}
{k:"Atasözleri",s:"'Gülme komşuna gelir başına' ne demektir?",o:["Komedi","Başkasının başına gelene gülme, sana da gelebilir","Espri yapma","Güldürü programı"],d:1,a:"Başkasının başına gelene gülme, aynısı sana da gelebilir."}
{k:"Atasözleri",s:"'Yuvarlanan taş yosun tutmaz' ne anlama gelir?",o:["Jeoloji","Sürekli yer değiştiren birikim yapamaz","Taş bilimi","Yosun türleri"],d:1,a:"Bir yerde durmayan, sürekli iş/yer değiştiren kişi bir şey elde edemez."}
{k:"Atasözleri",s:"'Dost acı söyler' ne demektir?",o:["Dost kavgası","Gerçek dost doğruyu söyler","Acı biber","İlaç"],d:1,a:"Gerçek dost hoşa gitmese de doğruyu söyler."}
{k:"Atasözleri",s:"'Güvenme varlığa düşersin darlığa' ne anlama gelir?",o:["Finansal tavsiye","Zenginliğe güvenme, bir gün yoksul kalabilirsin","Banka iflası","Sigorta reklamı"],d:1,a:"Sahip olduğun varlığa güvenme, her an kaybedebilirsin."}
{k:"Atasözleri",s:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",o:["Yılan avcılığı","Güzel sözle her kapı açılır","Hayvan bakımı","Dil bilgisi"],d:1,a:"Güzel ve tatlı konuşmayla en zor işler bile başarılır."}
{k:"Atasözleri",s:"'Mum dibine ışık vermez' ne anlama gelir?",o:["Fizik kanunu","Kişi yakınlarına fayda sağlayamaz","Mum üretimi","Aydınlatma"],d:1,a:"Başkalarına yardım eden kişi bazen yakınlarına faydası olmaz."}
{k:"Atasözleri",s:"'Üzüm üzüme baka baka kararır' ne anlama gelir?",o:["Tarım bilgisi","İnsanlar çevresinden etkilenir","Üzüm hasadı","Bağcılık"],d:1,a:"İnsanlar birbirinden etkilenir, çevre kişiyi şekillendirir."}
{k:"Atasözleri",s:"'El eli yıkar el de yüzü' ne demektir?",o:["Hijyen kuralı","İnsanlar birbirine yardım edince herkes kazanır","El yıkama","Temizlik"],d:1,a:"Karşılıklı yardımlaşma herkese fayda sağlar."}
{k:"Atasözleri",s:"'İşleyen demir pas tutmaz' ne anlama gelir?",o:["Metal bilimi","Çalışan kişi her zaman dinç ve sağlıklı kalır","Demir bakımı","Fabrika kuralı"],d:1,a:"Sürekli çalışan, hareket eden kişi sağlığını ve zindeliğini korur."}
{k:"Atasözleri",s:"'Bugünün işini yarına bırakma' ne demektir?",o:["Takvim kullanımı","İşleri erteleme, zamanında yap","Planlama aracı","Ajanda"],d:1,a:"Yapılması gereken işi ertelemeden hemen yapmalısın."}
{k:"Atasözleri",s:"'Keskin sirke küpüne zarar' ne anlama gelir?",o:["Sirke üretimi","Aşırı sert/kızgın olan kendine zarar verir","Küp bakımı","Yemek tarifi"],d:1,a:"Çok sert, öfkeli davranan kişi en çok kendine zarar verir."}
{k:"Atasözleri",s:"'Aç ayı oynamaz' ne demektir?",o:["Hayvan bakımı","Karşılığını almadan kimse iş yapmaz","Sirk gösterisi","Ayı besleme"],d:1,a:"Karşılığını görmeyen kişi o iş için çaba göstermez."}
{k:"Atasözleri",s:"'Her kuşun eti yenmez' ne anlama gelir?",o:["Yemek kültürü","Her kişiye her şey söylenemez/yapılamaz","Kuş türleri","Avcılık"],d:1,a:"Bazı insanlarla uğraşmamak gerekir, herkes aynı muameleyi kaldırmaz."}
{k:"Atasözleri",s:"'Atı alan Üsküdar'ı geçti' ne demektir?",o:["At yarışı","İş işten geçti, fırsat kaçırıldı","Üsküdar tarihi","Ulaşım"],d:1,a:"Artık çok geç, yapılacak bir şey kalmadı."}
{k:"Atasözleri",s:"'Gönül ne kahve ister ne kahvehane' ne anlama gelir?",o:["Kahve kültürü","Önemli olan maddi şeyler değil samimiyettir","Kahvehane tarihi","İçecek tercihi"],d:1,a:"Önemli olan ikram değil, samimiyet ve dostluktur."}
{k:"Atasözleri",s:"'İki cambaz bir ipte oynamaz' ne demektir?",o:["Sirk gösterisi","İki rakip aynı yerde barınamaz","Cambaz eğitimi","İp yapımı"],d:1,a:"İki güçlü rakip aynı ortamda geçinemez."}
{k:"Atasözleri",s:"'Tencere yuvarlanmış kapağını bulmuş' ne anlama gelir?",o:["Mutfak eşyası","Birbirine denk kişiler bir araya gelmiş","Tencere üretimi","Yemek pişirme"],d:1,a:"Birbirine benzeyen, denk olan kişiler bir araya gelmiştir."}
{k:"Atasözleri",s:"'Körle yatan şaşı kalkar' ne demektir?",o:["Göz hastalığı","Kötü çevreyle takılan zarar görür","Uyku düzeni","Oftalmoloji"],d:1,a:"Kötü alışkanlıkları olan insanlarla vakit geçiren onlardan etkilenir."}
"""


def _build_bilgi_yarismasi_html(level: str = "ilkokul") -> str:
    """Bilgi Yarışması — 3 seviye, 20 soru/tur, zamanlı, kategori rozetli, premium tasarım."""
    questions_js = _get_by_questions(level)
    level_labels = {"ilkokul": "İlkokul", "ortaokul": "Ortaokul", "lise": "Lise"}
    level_label = level_labels.get(level, "İlkokul")
    html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body,html{width:100%;height:100%;overflow-y:auto;overflow-x:hidden;
  background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);font-family:'Segoe UI',sans-serif}
.by-wrap{max-width:600px;margin:0 auto;padding:10px 12px}
.by-header{text-align:center;padding:16px 0 8px}
.by-title{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#ffd700,#ffaa00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:none}
.by-badge{display:inline-block;background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;
  font-size:.7rem;padding:2px 10px;border-radius:20px;margin-left:8px;font-weight:600;
  vertical-align:middle}
.by-subtitle{font-size:.82rem;color:#94a3b8;margin-top:4px}
.by-stats{display:flex;justify-content:center;gap:16px;margin:10px 0}
.by-stat{background:rgba(255,255,255,.08);border-radius:10px;padding:8px 16px;text-align:center;
  border:1px solid rgba(255,255,255,.1);min-width:80px}
.by-stat-val{font-size:1.2rem;font-weight:700;color:#ffd700}
.by-stat-lbl{font-size:.68rem;color:#94a3b8;margin-top:2px}
.by-progress{margin:10px 0;display:flex;align-items:center;gap:8px}
.by-pbar{flex:1;height:8px;background:rgba(255,255,255,.1);border-radius:4px;overflow:hidden}
.by-pfill{height:100%;border-radius:4px;transition:width .4s;
  background:linear-gradient(90deg,#ffd700,#ff6b35)}
.by-ptxt{font-size:.78rem;color:#94a3b8;min-width:50px;text-align:right}
.by-timer{text-align:center;margin:6px 0}
.by-timer-bar{width:100%;height:6px;background:rgba(255,255,255,.1);border-radius:3px;overflow:hidden}
.by-timer-fill{height:100%;border-radius:3px;transition:width .3s linear;
  background:linear-gradient(90deg,#22c55e,#fbbf24,#ef4444)}
.by-timer-txt{font-size:.75rem;color:#94a3b8;margin-top:3px}
.by-cat{display:inline-block;padding:3px 12px;border-radius:15px;font-size:.72rem;font-weight:600;
  margin-bottom:8px}
.by-qcard{background:rgba(255,255,255,.06);border-radius:16px;padding:20px;margin:10px 0;
  border:1px solid rgba(255,255,255,.1);backdrop-filter:blur(10px)}
.by-qtext{font-size:1.05rem;color:#e2e8f0;font-weight:600;line-height:1.5;margin-bottom:14px}
.by-qnum{font-size:.72rem;color:#64748b;margin-bottom:6px}
.by-opts{display:flex;flex-direction:column;gap:8px}
.by-opt{display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:12px;
  cursor:pointer;transition:all .25s;border:2px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);color:#cbd5e1;font-size:.92rem;font-weight:500}
.by-opt:hover{border-color:rgba(99,102,241,.5);background:rgba(99,102,241,.1);transform:translateX(4px)}
.by-opt.selected{border-color:#6366f1;background:rgba(99,102,241,.2);color:#fff}
.by-opt.correct{border-color:#22c55e;background:rgba(34,197,94,.2);color:#22c55e;font-weight:700}
.by-opt.wrong{border-color:#ef4444;background:rgba(239,68,68,.2);color:#ef4444}
.by-opt.dimmed{opacity:.4;pointer-events:none}
.by-opt-letter{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-weight:700;font-size:.82rem;flex-shrink:0;
  background:rgba(255,255,255,.1);color:#94a3b8}
.by-opt.selected .by-opt-letter{background:#6366f1;color:#fff}
.by-opt.correct .by-opt-letter{background:#22c55e;color:#fff}
.by-opt.wrong .by-opt-letter{background:#ef4444;color:#fff}
.by-explain{margin-top:10px;padding:12px 16px;border-radius:10px;font-size:.85rem;line-height:1.5;
  background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#86efac;display:none}
.by-explain.show{display:block}
.by-explain.wrong-exp{background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.3);color:#fca5a5}
.by-btn{display:block;width:100%;padding:14px;border:none;border-radius:12px;font-size:1rem;
  font-weight:700;cursor:pointer;margin-top:12px;transition:all .3s;letter-spacing:.5px}
.by-btn-primary{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff}
.by-btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(99,102,241,.4)}
.by-btn-gold{background:linear-gradient(135deg,#ffd700,#f59e0b);color:#1a1a2e}
.by-btn-gold:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(255,215,0,.4)}
.by-result{text-align:center;padding:30px 20px}
.by-result-icon{font-size:3.5rem;margin-bottom:10px}
.by-result-score{font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,#ffd700,#ff6b35);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.by-result-txt{font-size:1rem;color:#94a3b8;margin:8px 0}
.by-result-detail{display:flex;justify-content:center;gap:20px;margin:16px 0}
.by-rd{text-align:center}
.by-rd-val{font-size:1.3rem;font-weight:700}
.by-rd-lbl{font-size:.7rem;color:#64748b;margin-top:2px}
.by-start{text-align:center;padding:40px 20px}
.by-start-icon{font-size:4rem;margin-bottom:12px}
.by-start-title{font-size:1.8rem;font-weight:800;color:#ffd700;margin-bottom:8px}
.by-start-desc{font-size:.92rem;color:#94a3b8;line-height:1.6;margin-bottom:20px}
.by-start-features{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-bottom:20px}
.by-feat{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:8px;
  padding:6px 12px;font-size:.78rem;color:#cbd5e1}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.by-anim{animation:fadeIn .4s ease-out}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.by-pulse{animation:pulse .6s ease-in-out}
@keyframes confetti{0%{transform:translateY(0) rotate(0)}100%{transform:translateY(400px) rotate(720deg);opacity:0}}
.confetti-piece{position:fixed;width:8px;height:8px;top:-10px;z-index:999;border-radius:2px;
  animation:confetti 2.5s ease-in forwards}
</style></head><body>
<div class="by-wrap" id="app"></div>
<script>
var LEVEL="__LEVEL__";
var QUESTIONS_PER_ROUND=20;
var TIME_PER_QUESTION=30;
var LETTERS=["A","B","C","D"];
var CAT_COLORS={
  "Tarih":["#f59e0b","#78350f"],"Coğrafya":["#22c55e","#064e3b"],
  "Bilim":["#3b82f6","#1e3a5f"],"Edebiyat":["#a855f7","#3b0764"],
  "Spor":["#ef4444","#450a0a"],"Türkiye":["#e11d48","#4c0519"],
  "Müzik":["#ec4899","#500724"],"Sanat":["#8b5cf6","#2e1065"],
  "Matematik":["#06b6d4","#083344"],"Doğa":["#10b981","#022c22"],
  "Genel":["#64748b","#94A3B8"],"Deyimler":["#f97316","#431407"],
  "Atasözleri":["#eab308","#422006"],"Başkentler":["#14b8a6","#042f2e"]
};

var allQ=__QUESTIONS_JSON__;
var PPQ=5; /* her soru 5 puan, 20 soru = 100 puan */
var pool=[],cur=null,qIdx=0,score=0,answered=false,selIdx=-1,timer=0,timerInterval=null;
var state="start",results=[];
var LS_KEY="by_high_"+LEVEL;
function getHigh(){try{return parseInt(localStorage.getItem(LS_KEY))||0;}catch(e){return 0;}}
function setHigh(v){try{localStorage.setItem(LS_KEY,v);}catch(e){}}

function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}

function startGame(){
  /* Kategorilere eşit dağılım: her kategoriden eşit soru seç */
  var cats={};
  for(var i=0;i<allQ.length;i++){
    var c=allQ[i].k;
    if(!cats[c])cats[c]=[];
    cats[c].push(allQ[i]);
  }
  var catKeys=Object.keys(cats);
  for(var i=0;i<catKeys.length;i++)cats[catKeys[i]]=shuffle(cats[catKeys[i]]);
  var perCat=Math.floor(QUESTIONS_PER_ROUND/catKeys.length);
  var extra=QUESTIONS_PER_ROUND-(perCat*catKeys.length);
  pool=[];
  for(var i=0;i<catKeys.length;i++){
    var take=perCat+(i<extra?1:0);
    var arr=cats[catKeys[i]];
    for(var j=0;j<Math.min(take,arr.length);j++)pool.push(arr[j]);
  }
  /* Eksik kaldıysa rastgele tamamla */
  if(pool.length<QUESTIONS_PER_ROUND){
    var rest=shuffle(allQ.filter(function(q){return pool.indexOf(q)===-1;}));
    while(pool.length<QUESTIONS_PER_ROUND&&rest.length>0)pool.push(rest.shift());
  }
  pool=shuffle(pool);
  qIdx=0;score=0;results=[];state="playing";answered=false;selIdx=-1;
  renderQuestion();
}

function startTimer(){
  clearInterval(timerInterval);
  timer=TIME_PER_QUESTION;
  timerInterval=setInterval(function(){
    timer--;
    updateTimer();
    if(timer<=0){clearInterval(timerInterval);timeUp();}
  },1000);
}

function timeUp(){
  answered=true;selIdx=-1;
  results.push({q:cur,sel:-1,correct:false});
  renderQuestion();
}

function updateTimer(){
  var fill=document.getElementById("timerFill");
  var txt=document.getElementById("timerTxt");
  if(fill)fill.style.width=(timer/TIME_PER_QUESTION*100)+"%";
  if(txt)txt.textContent=timer+" sn";
  if(fill){
    if(timer<=5)fill.style.background="linear-gradient(90deg,#ef4444,#dc2626)";
    else if(timer<=10)fill.style.background="linear-gradient(90deg,#fbbf24,#f59e0b)";
    else fill.style.background="linear-gradient(90deg,#22c55e,#16a34a)";
  }
}

function selectAnswer(idx){
  if(answered)return;
  answered=true;
  clearInterval(timerInterval);
  selIdx=idx;
  var isCorrect=idx===cur.d;
  if(isCorrect)score++;
  results.push({q:cur,sel:idx,correct:isCorrect});
  if(isCorrect)playCorrect();else playWrong();
  renderQuestion();
}

function nextQuestion(){
  qIdx++;
  if(qIdx>=pool.length){state="result";renderResult();return;}
  answered=false;selIdx=-1;
  renderQuestion();
}

function renderQuestion(){
  cur=pool[qIdx];
  var app=document.getElementById("app");
  var catColor=CAT_COLORS[cur.k]||CAT_COLORS["Genel"];
  var pct=((qIdx+(answered?1:0))/pool.length*100);

  var h='<div class="by-anim">';
  h+='<div class="by-header"><span class="by-title">Bilgi Yarışması</span>';
  h+='<span class="by-badge">'+LEVEL+'</span></div>';
  var pts=score*PPQ;
  var hi=getHigh();
  h+='<div class="by-stats">';
  h+='<div class="by-stat"><div class="by-stat-val" style="color:#ffd700">'+pts+'</div><div class="by-stat-lbl">Puan</div></div>';
  h+='<div class="by-stat"><div class="by-stat-val" style="color:#22c55e">'+score+'</div><div class="by-stat-lbl">Doğru</div></div>';
  h+='<div class="by-stat"><div class="by-stat-val" style="color:#ef4444">'+(results.filter(function(r){return !r.correct}).length)+'</div><div class="by-stat-lbl">Yanlış</div></div>';
  h+='<div class="by-stat"><div class="by-stat-val" style="color:#a78bfa">'+hi+'</div><div class="by-stat-lbl">Rekor</div></div>';
  h+='</div>';
  h+='<div class="by-progress"><div class="by-pbar"><div class="by-pfill" style="width:'+pct+'%"></div></div>';
  h+='<div class="by-ptxt">'+(qIdx+(answered?1:0))+'/'+pool.length+'</div></div>';

  if(!answered){
    h+='<div class="by-timer"><div class="by-timer-bar"><div class="by-timer-fill" id="timerFill" style="width:100%"></div></div>';
    h+='<div class="by-timer-txt" id="timerTxt">'+TIME_PER_QUESTION+' sn</div></div>';
  }

  h+='<div class="by-qcard">';
  h+='<div class="by-cat" style="background:'+catColor[1]+';color:'+catColor[0]+'">'+cur.k+'</div>';
  h+='<div class="by-qnum">Soru '+(qIdx+1)+' / '+pool.length+'</div>';
  h+='<div class="by-qtext">'+cur.s+'</div>';
  h+='<div class="by-opts">';

  for(var i=0;i<cur.o.length;i++){
    var cls="by-opt";
    if(answered){
      if(i===cur.d)cls+=" correct";
      else if(i===selIdx&&i!==cur.d)cls+=" wrong";
      else cls+=" dimmed";
    }else if(i===selIdx){cls+=" selected";}
    h+='<div class="'+cls+'" '+(answered?'':'onclick="selectAnswer('+i+')"')+'>';
    h+='<span class="by-opt-letter">'+LETTERS[i]+'</span>';
    h+='<span>'+cur.o[i]+'</span></div>';
  }
  h+='</div>';

  if(answered){
    var isC=selIdx===cur.d;
    var expCls=isC?"by-explain show":"by-explain show wrong-exp";
    var icon=selIdx===-1?"⏱️ Süre doldu! ":(isC?"✅ Doğru! ":"❌ Yanlış! ");
    h+='<div class="'+expCls+'">'+icon+(cur.a||"")+'</div>';
    h+='<button class="by-btn by-btn-primary" onclick="nextQuestion()">'+(qIdx+1>=pool.length?"Sonuçları Gör ➜":"Sonraki Soru ➜")+'</button>';
  }
  h+='</div></div>';
  app.innerHTML=h;

  if(!answered)startTimer();
}

function renderResult(){
  var app=document.getElementById("app");
  var pts=score*PPQ;
  var wrong=pool.length-score;
  var hi=getHigh();
  var isNewRecord=pts>hi;
  var isTied=pts===hi&&pts>0;
  if(isNewRecord){setHigh(pts);hi=pts;}
  var icon=pts>=90?"🏆":pts>=70?"🎉":pts>=50?"👍":"💪";
  var msg=pts>=90?"Muhteşem! Bilgi şampiyonu!":pts>=70?"Harika! Çok başarılı!":pts>=50?"İyi! Biraz daha çalışarak zirveye çıkabilirsin!":"Pes etme! Her yarışma yeni bir fırsat!";

  if(pts>=70||isNewRecord)spawnConfetti();

  var h='<div class="by-anim"><div class="by-header"><span class="by-title">Bilgi Yarışması</span>';
  h+='<span class="by-badge">'+LEVEL+'</span></div>';
  h+='<div class="by-result">';
  h+='<div class="by-result-icon by-pulse">'+icon+'</div>';
  h+='<div class="by-result-score">'+pts+' Puan</div>';
  h+='<div class="by-result-txt">'+msg+'</div>';

  if(isNewRecord){
    h+='<div style="margin:10px 0;padding:10px 20px;border-radius:12px;background:linear-gradient(135deg,rgba(255,215,0,.2),rgba(255,107,53,.2));border:2px solid #ffd700;display:inline-block">';
    h+='<div style="font-size:1.1rem;font-weight:800;color:#ffd700">🎊 YENİ REKOR! 🎊</div>';
    h+='<div style="font-size:.82rem;color:#fbbf24;margin-top:2px">Önceki rekor: '+(hi===pts?0:hi)+' → Yeni: '+pts+'</div></div>';
  }else if(isTied){
    h+='<div style="margin:10px 0;padding:10px 20px;border-radius:12px;background:rgba(168,85,247,.15);border:2px solid #a855f7;display:inline-block">';
    h+='<div style="font-size:1rem;font-weight:700;color:#a855f7">⚡ REKOR EŞİTLENDİ!</div>';
    h+='<div style="font-size:.82rem;color:#c084fc;margin-top:2px">Rekor puanın: '+hi+'</div></div>';
  }

  h+='<div class="by-result-detail">';
  h+='<div class="by-rd"><div class="by-rd-val" style="color:#ffd700">'+pts+'</div><div class="by-rd-lbl">Puan</div></div>';
  h+='<div class="by-rd"><div class="by-rd-val" style="color:#22c55e">'+score+'</div><div class="by-rd-lbl">Doğru</div></div>';
  h+='<div class="by-rd"><div class="by-rd-val" style="color:#ef4444">'+wrong+'</div><div class="by-rd-lbl">Yanlış</div></div>';
  h+='<div class="by-rd"><div class="by-rd-val" style="color:#a78bfa">'+hi+'</div><div class="by-rd-lbl">Rekor</div></div>';
  h+='</div>';
  h+='<button class="by-btn by-btn-gold" onclick="startGame()" style="max-width:300px;margin:16px auto">🔄 Tekrar Oyna</button>';
  h+='</div>';

  // Yanlış cevaplanan soruları göster
  var wrongs=results.filter(function(r){return !r.correct;});
  if(wrongs.length>0){
    h+='<div class="by-qcard" style="margin-top:16px"><div class="by-qtext" style="font-size:.95rem;color:#fbbf24;margin-bottom:12px">📋 Yanlış Cevaplanan Sorular ('+wrongs.length+')</div>';
    for(var i=0;i<wrongs.length;i++){
      var r=wrongs[i];
      var catColor=CAT_COLORS[r.q.k]||CAT_COLORS["Genel"];
      h+='<div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06)">';
      h+='<span class="by-cat" style="background:'+catColor[1]+';color:'+catColor[0]+';font-size:.65rem;padding:2px 8px">'+r.q.k+'</span>';
      h+='<div style="color:#e2e8f0;font-size:.85rem;margin:4px 0">'+r.q.s+'</div>';
      if(r.sel>=0)h+='<div style="color:#ef4444;font-size:.78rem">Senin cevabın: '+r.q.o[r.sel]+'</div>';
      else h+='<div style="color:#f59e0b;font-size:.78rem">⏱️ Süre doldu</div>';
      h+='<div style="color:#22c55e;font-size:.78rem">Doğru cevap: '+r.q.o[r.q.d]+'</div>';
      h+='</div>';
    }
    h+='</div>';
  }
  h+='</div>';
  app.innerHTML=h;
}

function renderStart(){
  var app=document.getElementById("app");
  var h='<div class="by-anim"><div class="by-start">';
  h+='<div class="by-start-icon">🧠</div>';
  h+='<div class="by-start-title">Bilgi Yarışması</div>';
  h+='<div style="margin-bottom:8px"><span class="by-badge" style="font-size:.85rem;padding:4px 16px">'+LEVEL+' Seviyesi</span></div>';
  h+='<div class="by-start-desc">'+QUESTIONS_PER_ROUND+' soru × '+PPQ+' puan = 100 puan<br>Her soruya '+TIME_PER_QUESTION+' saniye süre!</div>';
  var hi=getHigh();
  if(hi>0){
    h+='<div style="margin-bottom:14px;padding:8px 20px;border-radius:10px;background:rgba(168,85,247,.12);border:1px solid rgba(168,85,247,.3);display:inline-block">';
    h+='<span style="color:#a78bfa;font-weight:700;font-size:.9rem">🏅 En Yüksek Puan: '+hi+'</span></div><br>';
  }
  h+='<div class="by-start-features">';
  h+='<div class="by-feat">📚 '+allQ.length+' Soru Havuzu</div>';
  h+='<div class="by-feat">💯 100 Puan</div>';
  h+='<div class="by-feat">🏷️ Kategoriler</div>';
  h+='<div class="by-feat">🏆 Rekor Takibi</div>';
  h+='</div>';
  h+='<button class="by-btn by-btn-gold" onclick="startGame()" style="max-width:300px;margin:0 auto">🚀 Yarışmayı Başlat</button>';
  h+='</div></div>';
  app.innerHTML=h;
}

function spawnConfetti(){
  var colors=["#ffd700","#ef4444","#22c55e","#3b82f6","#a855f7","#ec4899","#f59e0b"];
  for(var i=0;i<40;i++){
    var el=document.createElement("div");
    el.className="confetti-piece";
    el.style.left=Math.random()*100+"vw";
    el.style.background=colors[Math.floor(Math.random()*colors.length)];
    el.style.animationDelay=Math.random()*1.5+"s";
    el.style.animationDuration=(2+Math.random()*2)+"s";
    el.style.width=(5+Math.random()*8)+"px";
    el.style.height=(5+Math.random()*8)+"px";
    document.body.appendChild(el);
    setTimeout(function(e){e.remove();},4000,el);
  }
}

var ACx=null;
function snd(f,d,t){try{if(!ACx)ACx=new(window.AudioContext||window.webkitAudioContext)();var o=ACx.createOscillator(),g=ACx.createGain();o.connect(g);g.connect(ACx.destination);o.type=t||"sine";o.frequency.value=f;g.gain.setValueAtTime(0.1,ACx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,ACx.currentTime+d);o.start();o.stop(ACx.currentTime+d);}catch(e){}}
function playCorrect(){snd(523,.1);setTimeout(function(){snd(659,.1)},100);setTimeout(function(){snd(784,.2)},200);}
function playWrong(){snd(300,.2,"sawtooth");setTimeout(function(){snd(200,.3,"sawtooth")},200);}

renderStart();
</script></body></html>'''

    html = html.replace('__LEVEL__', level_label)
    html = html.replace('__QUESTIONS_JSON__', _build_questions_json(level))
    return html


def _build_questions_json(level: str) -> str:
    """Soru bankasını JSON formatına çevir."""
    raw = _get_by_questions(level).strip()
    if not raw or raw.startswith("__"):
        return "[]"
    questions = []
    import re
    for m in re.finditer(
        r'\{k:"([^"]*)",s:"([^"]*)",o:\[([^\]]*)\],d:(\d+),a:"([^"]*)"\}',
        raw
    ):
        opts = [o.strip().strip('"') for o in m.group(3).split('","')]
        questions.append({
            "k": m.group(1), "s": m.group(2),
            "o": opts, "d": int(m.group(4)), "a": m.group(5)
        })
    return _json.dumps(questions, ensure_ascii=False)


def render_bilgi_yarismasi():
    """Bilgi Yarismasi ana render fonksiyonu — CSS enjeksiyonu ile."""
    inject_common_css("byg")
    styled_header("Bilgi Yarismasi", "Premium HTML5 Quiz Oyunu", icon="🧠")
