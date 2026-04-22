"""Kim Milyoner Olmak İster — Premium HTML5 oyunu, 4 seviye, geniş soru bankası."""

from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("default")
except Exception:
    pass

# ══════════════════════════════════════════════════════════════════════════════
# SEVİYE BAZLI SORU BANKALARI
# ══════════════════════════════════════════════════════════════════════════════

def _get_questions(level: str) -> str:
    """Seviyeye göre JavaScript soru bankası döndürür."""
    if level == "ilkokul":
        return _QUESTIONS_ILKOKUL
    elif level == "ortaokul":
        return _QUESTIONS_ORTAOKUL
    elif level == "lise":
        return _QUESTIONS_LISE
    else:
        return _QUESTIONS_YETISKIN

_QUESTIONS_ILKOKUL = r"""
easy:[
{q:"Bir yılda kaç ay vardır?",a:["10","11","12","13"],c:2},
{q:"Gökkuşağında kaç renk vardır?",a:["5","6","7","8"],c:2},
{q:"Hangi hayvan 'miyav' diye ses çıkarır?",a:["Köpek","Kedi","Kuş","Tavşan"],c:1},
{q:"Güneş hangi yönden doğar?",a:["Batı","Kuzey","Güney","Doğu"],c:3},
{q:"Bir haftada kaç gün vardır?",a:["5","6","7","8"],c:2},
{q:"Hangisi bir renk değildir?",a:["Mavi","Kare","Kırmızı","Yeşil"],c:1},
{q:"İnsan vücudunda kaç göz vardır?",a:["1","2","3","4"],c:1},
{q:"Arı ne üretir?",a:["Süt","Yumurta","Bal","Peynir"],c:2},
{q:"Hangisi bir meyve değildir?",a:["Elma","Havuç","Portakal","Üzüm"],c:1},
{q:"Kaç tane ana yön vardır?",a:["2","3","4","6"],c:2},
{q:"Hangisi bir sebzedir?",a:["Çilek","Domates","Kiraz","Muz"],c:1},
{q:"Türkiye'nin başkenti neresidir?",a:["İstanbul","Ankara","İzmir","Bursa"],c:1},
{q:"Hangi mevsimde yapraklar dökülür?",a:["İlkbahar","Yaz","Sonbahar","Kış"],c:2},
{q:"Bir günde kaç saat vardır?",a:["12","20","24","30"],c:2},
{q:"Hangisi bir hayvan değildir?",a:["Aslan","Kaplan","Masa","Fil"],c:2},
{q:"Suyun rengi nedir?",a:["Mavi","Kırmızı","Renksiz","Yeşil"],c:2},
{q:"Hangisi bir gezegen değildir?",a:["Mars","Ay","Jüpiter","Venüs"],c:1},
{q:"Atatürk'ün adı nedir?",a:["Mustafa Kemal","İsmet","Fevzi","Kazım"],c:0},
{q:"Türk bayrağının rengi nedir?",a:["Mavi-Beyaz","Kırmızı-Beyaz","Yeşil-Beyaz","Sarı-Kırmızı"],c:1},
{q:"Hangisi bir mevsim değildir?",a:["İlkbahar","Yaz","Pazar","Kış"],c:2},
{q:"Dünya'nın uydusu hangisidir?",a:["Güneş","Ay","Mars","Yıldız"],c:1},
{q:"Cumhuriyet Bayramı ne zaman kutlanır?",a:["23 Nisan","19 Mayıs","30 Ağustos","29 Ekim"],c:3},
{q:"Hangisi suda yaşar?",a:["Kartal","Balık","Aslan","Kedi"],c:1},
{q:"İnsan vücudunda kaç kulak vardır?",a:["1","2","3","4"],c:1},
{q:"Hangisi okul malzemesidir?",a:["Tava","Defter","Çatal","Tabak"],c:1},
{q:"Kış mevsiminde ne yağar?",a:["Kum","Yaprak","Kar","Çiçek"],c:2},
{q:"23 Nisan ne bayramıdır?",a:["Zafer Bayramı","Çocuk Bayramı","Gençlik Bayramı","Cumhuriyet Bayramı"],c:1},
{q:"Hangisi uçar?",a:["Balık","Kurbağa","Kuş","Yılan"],c:2},
{q:"Alfabemizde kaç harf vardır?",a:["26","28","29","31"],c:2},
{q:"İstanbul hangi kıtada yer alır?",a:["Sadece Avrupa","Sadece Asya","Hem Avrupa hem Asya","Afrika"],c:2},
{q:"Hangisi bir müzik aletidir?",a:["Kalem","Keman","Silgi","Cetvel"],c:1},
{q:"Ağrı Dağı Türkiye'nin en ne dağıdır?",a:["En alçak","En güzel","En yüksek","En küçük"],c:2},
{q:"Bir saatte kaç dakika vardır?",a:["30","45","60","100"],c:2},
{q:"Hangisi bir iç organ değildir?",a:["Kalp","Beyin","Karaciğer","Dirsek"],c:3},
{q:"Süt hangi hayvandan elde edilir?",a:["Tavuk","İnek","Balık","Kaplumbağa"],c:1},
{q:"Hangisi Türkiye'nin komşusu değildir?",a:["Yunanistan","İran","Almanya","Suriye"],c:2},
{q:"Dünya'da kaç kıta vardır?",a:["5","6","7","8"],c:2},
{q:"Hangisi bir spor dalı değildir?",a:["Futbol","Yüzme","Okuma","Basketbol"],c:2},
{q:"Güneş sistemimizdeki en büyük gezegen hangisidir?",a:["Dünya","Mars","Jüpiter","Venüs"],c:2},
{q:"Hangisi bir kuştur?",a:["Penguen","Yunus","Kedi","Köpek"],c:0},
{q:"Fransa'nın başkenti neresidir?",a:["Londra","Berlin","Paris","Roma"],c:2},
{q:"İtalya'nın başkenti neresidir?",a:["Madrid","Roma","Atina","Lizbon"],c:1},
{q:"Almanya'nın başkenti neresidir?",a:["Viyana","Berlin","Münih","Hamburg"],c:1},
{q:"İngiltere'nin başkenti neresidir?",a:["Paris","Dublin","Londra","Edinburgh"],c:2},
{q:"Japonya'nın başkenti neresidir?",a:["Pekin","Seul","Tokyo","Osaka"],c:2},
{q:"Mısır'ın başkenti neresidir?",a:["Kahire","İskenderiye","Bağdat","Tunus"],c:0},
{q:"Yunanistan'ın başkenti neresidir?",a:["İstanbul","İzmir","Atina","Selanik"],c:2},
{q:"'Damlaya damlaya göl olur' ne demektir?",a:["Su tasarrufu yap","Az az biriktir, çok olur","Göle git","Yağmur yağar"],c:1},
{q:"'Armut piş ağzıma düş' ne demektir?",a:["Meyve ye","Hiç çalışmadan sonuç bekle","Ağaca çık","Armut topla"],c:1},
{q:"'Sakla samanı gelir zamanı' ne demektir?",a:["Saman al","Her şeyin lazım olacağı gün gelir","Samanlığa git","Zamanı bekle"],c:1},
{q:"'Ağaçtan elma düşer' atasözünü tamamla: Ağaçtan elma düşer, ...",a:["armut düşer","yere düşer","dalından düşer","dibine düşer"],c:3},
{q:"'Bal tutan parmağını yalar' ne demektir?",a:["Bal ye","Fırsatı değerlendiren kazanır","Parmağını yıka","Tatlı ye"],c:1},
{q:"'İşleyen demir pas tutmaz' ne demektir?",a:["Demiri boyat","Çalışan kişi her zaman sağlıklı kalır","Demir al","Pas söker"],c:1},
{q:"'Yuvarlanan taş yosun tutmaz' ne demektir?",a:["Taş at","Sürekli yer değiştiren tutunmaz","Yosun topla","Taş yuvala"],c:1},
{q:"Hangisi Türkiye'nin en uzun nehridir?",a:["Sakarya","Kızılırmak","Fırat","Dicle"],c:1},
{q:"Nil Nehri hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:2},
{q:"En büyük kıta hangisidir?",a:["Afrika","Avrupa","Asya","Amerika"],c:2},
{q:"En küçük kıta hangisidir?",a:["Avrupa","Avustralya","Antarktika","Afrika"],c:1},
{q:"Hangisi bir okyanus değildir?",a:["Atlas","Akdeniz","Hint","Pasifik"],c:1},
{q:"Karadeniz Türkiye'nin hangi yönündedir?",a:["Güney","Kuzey","Doğu","Batı"],c:1},
{q:"Akdeniz Türkiye'nin hangi yönündedir?",a:["Kuzey","Güney","Doğu","Batı"],c:1},
{q:"Hangisi bir deniz değildir?",a:["Karadeniz","Akdeniz","Van Gölü","Ege Denizi"],c:2},
{q:"Uludağ hangi şehirdedir?",a:["İstanbul","Ankara","Bursa","Antalya"],c:2},
{q:"Erciyes Dağı hangi şehirdedir?",a:["Kayseri","Konya","Sivas","Erzurum"],c:0},
{q:"Dünya'nın en yüksek dağı hangisidir?",a:["Ağrı Dağı","Alpler","Everest","Kilimanjaro"],c:2},
{q:"Hangisi Afrika'da bir ülkedir?",a:["Brezilya","Mısır","Hindistan","Çin"],c:1},
{q:"Hangisi Avrupa'da bir ülkedir?",a:["Japonya","Kanada","Fransa","Avustralya"],c:2},
{q:"Van Gölü hangi bölgemizdedir?",a:["Karadeniz","Akdeniz","Doğu Anadolu","Marmara"],c:2},
{q:"Hangisi bir trafik kuralıdır?",a:["Koş","Kırmızıda dur","Atla","Bağır"],c:1},
{q:"İnsan vücudunda kaç parmak vardır?",a:["8","10","12","20"],c:3},
{q:"Terazi hangi iş için kullanılır?",a:["Kesmek","Tartmak","Dikmek","Boyamak"],c:1},
{q:"Hangisi bir meslek değildir?",a:["Doktor","Öğretmen","Sandalye","Mühendis"],c:2},
{q:"Pamuk hangi mevsimde toplanır?",a:["İlkbahar","Yaz","Sonbahar","Kış"],c:2},
{q:"Çin'in başkenti neresidir?",a:["Tokyo","Pekin","Seul","Şangay"],c:1},
{q:"ABD'nin başkenti neresidir?",a:["New York","Los Angeles","Washington","Chicago"],c:2},
{q:"Brezilya'nın başkenti neresidir?",a:["Rio de Janeiro","Sao Paulo","Brasilia","Salvador"],c:2},
{q:"Güneş bir ne türüdür?",a:["Gezegen","Uydu","Yıldız","Asteroid"],c:2},
{q:"Kurbağa yavrusuna ne denir?",a:["Civciv","İribaş","Tırtıl","Buzağı"],c:1},
{q:"Hangisi kutup hayvanıdır?",a:["Aslan","Zürafa","Penguen","Maymun"],c:2},
{q:"Piyanoda kaç tuş vardır?",a:["44","66","78","88"],c:3},
{q:"Türkiye kaç coğrafi bölgeye ayrılır?",a:["5","6","7","8"],c:2},
{q:"Hangisi Marmara Bölgesi'nde bir şehirdir?",a:["Antalya","Edirne","Ankara","Trabzon"],c:1},
{q:"Dünya'nın şekli neye benzer?",a:["Küp","Küre","Silindir","Koni"],c:1},
{q:"Hangisi doğal afet değildir?",a:["Deprem","Sel","Yangın","Yürümek"],c:3},
{q:"Peynir neden yapılır?",a:["Yumurta","Bal","Süt","Şeker"],c:2},
{q:"Yumurta hangi hayvandan elde edilir?",a:["İnek","Koyun","Tavuk","Keçi"],c:2},
{q:"Ispanya'nın başkenti neresidir?",a:["Barselona","Madrid","Lizbon","Roma"],c:1},
{q:"Güney Kore'nin başkenti neresidir?",a:["Tokyo","Pekin","Seul","Taipei"],c:2},
{q:"Hindistan'ın başkenti neresidir?",a:["Mumbai","Kalküta","Yeni Delhi","Goa"],c:2},
{q:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",a:["Yılan yakala","Güzel konuşma her kapıyı açar","Tatlı ye","Delik kaz"],c:1},
{q:"'Bir elin nesi var iki elin sesi var' ne demektir?",a:["El çırp","Birlikte iş yapmak daha iyi","İki el yıka","Tek el kötü"],c:1},
{q:"Hangisi kış sporlarından değildir?",a:["Kayak","Buz hokeyi","Tenis","Buz pateni"],c:2},
{q:"Futbolda bir takımda kaç oyuncu sahada bulunur?",a:["9","10","11","12"],c:2},
{q:"Hangisi hem suda hem karada yaşar?",a:["Balık","Kuş","Kurbağa","Yılan"],c:2},
{q:"Çiçeklerin tozlaşmasına en çok hangi canlı yardım eder?",a:["Kuş","Balık","Arı","Kedi"],c:2},
{q:"Hangisi bir tahıl ürünüdür?",a:["Elma","Buğday","Domates","Patates"],c:1},
{q:"Portakal hangi vitamini içerir?",a:["A vitamini","B vitamini","C vitamini","D vitamini"],c:2},
{q:"Kanada'nın başkenti neresidir?",a:["Toronto","Vancouver","Ottawa","Montreal"],c:2},
{q:"Avustralya'nın başkenti neresidir?",a:["Sidney","Melbourne","Canberra","Brisbane"],c:2},
{q:"Hangisi Ege Bölgesi'nde bir şehirdir?",a:["Trabzon","İzmir","Adana","Erzurum"],c:1},
{q:"Güneş sistemimizde kaç gezegen vardır?",a:["6","7","8","9"],c:2},
{q:"İstanbul'u Avrupa ve Asya'ya bölen su yolu nedir?",a:["Çanakkale Boğazı","İstanbul Boğazı","Süveyş Kanalı","Panama Kanalı"],c:1},
{q:"Hangi organ kanı pompalar?",a:["Beyin","Böbrek","Kalp","Mide"],c:2},
{q:"Hangisi bir memeli değildir?",a:["Kedi","Köpek","Yılan","At"],c:2},
{q:"Mars gezegeninin rengi nedir?",a:["Mavi","Yeşil","Kırmızı","Sarı"],c:2},
{q:"Dünyanın en uzun nehri hangisidir?",a:["Amazon","Nil","Fırat","Tuna"],c:1},
{q:"Atlas Okyanusu hangi kıtalar arasındadır?",a:["Asya-Afrika","Amerika-Avrupa/Afrika","Asya-Avustralya","Avrupa-Asya"],c:1},
{q:"Hangisi Güney Amerika'da bir ülkedir?",a:["Mısır","Hindistan","Arjantin","İtalya"],c:2},
{q:"Arjantin'in başkenti neresidir?",a:["Lima","Santiago","Buenos Aires","Bogota"],c:2},
{q:"Meksika'nın başkenti neresidir?",a:["Havana","Meksiko","Lima","Bogota"],c:1},
{q:"'Gülme komşuna gelir başına' ne demektir?",a:["Gülme","Başkasının başına gelen senin de başına gelebilir","Komşuya git","Başını koru"],c:1},
{q:"'Acele işe şeytan karışır' ne demektir?",a:["Şeytandan kaç","Acele eden hata yapar","Hızlı koş","İşi bırak"],c:1},
{q:"Amazon Nehri hangi kıtadadır?",a:["Afrika","Avrupa","Güney Amerika","Asya"],c:2},
{q:"Kapadokya hangi bölgemizdedir?",a:["Akdeniz","İç Anadolu","Ege","Karadeniz"],c:1},
{q:"Hangisi bir nota değildir?",a:["Do","Re","Ka","Mi"],c:2},
{q:"Olimpiyat oyunları kaç yılda bir yapılır?",a:["2","3","4","5"],c:2},
{q:"Hangisi sürüngen değildir?",a:["Yılan","Kertenkele","Kaplumbağa","Tavşan"],c:3},
{q:"İpek böceği ne üretir?",a:["Bal","İpek","Süt","Yün"],c:1},
{q:"'Çalışan demir ışıldar' ne demektir?",a:["Demir parla","Çalışkan kişi başarır","Demir ov","Işık yak"],c:1},
{q:"Meksika hangi kıtadadır?",a:["Güney Amerika","Avrupa","Kuzey Amerika","Asya"],c:2},
{q:"Hangisi bir böcektir?",a:["Kurbağa","Uğur böceği","Yarasa","Kertenkele"],c:1},
{q:"En hızlı kara hayvanı hangisidir?",a:["Aslan","Çita","At","Tavşan"],c:1},
{q:"Hangi gezegen Güneş'e en yakındır?",a:["Venüs","Dünya","Merkür","Mars"],c:2},
{q:"İnsan iskeletinde yaklaşık kaç kemik vardır?",a:["106","206","306","406"],c:1},
{q:"Hangisi bir çalgı aletidir?",a:["Kalem","Bağlama","Cetvel","Silgi"],c:1}
],
medium:[
{q:"Türkiye'nin en büyük gölü hangisidir?",a:["Tuz Gölü","Beyşehir Gölü","Van Gölü","Burdur Gölü"],c:2},
{q:"Dünya'nın en büyük okyanusu hangisidir?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Hangi nehir İstanbul'dan geçer?",a:["Kızılırmak","Sakarya","Haliç","Fırat"],c:2},
{q:"Tuz Gölü hangi bölgemizdedir?",a:["Marmara","İç Anadolu","Ege","Akdeniz"],c:1},
{q:"Fırat Nehri hangi denize dökülür?",a:["Karadeniz","Akdeniz","Basra Körfezi","Hazar Denizi"],c:2},
{q:"Kızılırmak hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Tuna Nehri hangi kıtadadır?",a:["Asya","Afrika","Avrupa","Amerika"],c:2},
{q:"Himalaya Dağları hangi kıtadadır?",a:["Avrupa","Afrika","Asya","Amerika"],c:2},
{q:"Alp Dağları hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:1},
{q:"And Dağları hangi kıtadadır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Kilimanjaro Dağı hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Ağrı Dağı'nın yüksekliği yaklaşık kaç metredir?",a:["3000","4000","5137","6000"],c:2},
{q:"Antarktika kıtasında ne bulunur?",a:["Çöl","Orman","Buzullar","Şehirler"],c:2},
{q:"Hangisi Karadeniz Bölgesi'nde bir şehirdir?",a:["Antalya","Trabzon","İzmir","Konya"],c:1},
{q:"İstanbul Boğazı hangi denizleri birleştirir?",a:["Akdeniz-Ege","Karadeniz-Marmara","Ege-Marmara","Karadeniz-Akdeniz"],c:1},
{q:"Çanakkale Boğazı hangi denizleri birleştirir?",a:["Karadeniz-Marmara","Ege-Marmara","Akdeniz-Ege","Karadeniz-Ege"],c:1},
{q:"'Dost kara günde belli olur' ne demektir?",a:["Kara gün gelir","Gerçek dost zor zamanda yanında olur","Dostu ara","Güneşli hava güzel"],c:1},
{q:"'Mart kapıdan baktırır kazma kürek yaktırır' ne demektir?",a:["Mart'ta bahçe yap","Mart ayı havası çok değişken","Kapıyı kapat","Kazma al"],c:1},
{q:"'Ağır ol batman gelsin' ne demektir?",a:["Kilo al","Ağırlık koy","Ağırbaşlı davranırsan değerin artar","Batman'a git"],c:2},
{q:"'El elden üstündür' ne demektir?",a:["Elini yıka","Her zaman daha iyisi vardır","Eller güzel","El sık"],c:1},
{q:"'Komşu komşunun külüne muhtaçtır' ne demektir?",a:["Kül topla","İnsanlar birbirine ihtiyaç duyar","Komşuya git","Kül at"],c:1},
{q:"Avusturya'nın başkenti neresidir?",a:["Berlin","Bern","Viyana","Prag"],c:2},
{q:"Polonya'nın başkenti neresidir?",a:["Prag","Varşova","Budapeşte","Bükreş"],c:1},
{q:"İsviçre'nin başkenti neresidir?",a:["Zürih","Cenevre","Bern","Basel"],c:2},
{q:"Norveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Kopenhag","Oslo"],c:3},
{q:"İsveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Oslo","Kopenhag"],c:0},
{q:"Portekiz'in başkenti neresidir?",a:["Madrid","Lizbon","Porto","Sevilla"],c:1},
{q:"Türkiye'nin en büyük adası hangisidir?",a:["Bozcaada","Gökçeada","Akdamar","Kekova"],c:1},
{q:"Sakarya Nehri hangi denize dökülür?",a:["Ege","Akdeniz","Karadeniz","Marmara"],c:2},
{q:"Gediz Nehri hangi denize dökülür?",a:["Karadeniz","Akdeniz","Ege","Marmara"],c:2},
{q:"Dicle Nehri hangi bölgemizden doğar?",a:["Karadeniz","Akdeniz","İç Anadolu","Güneydoğu Anadolu"],c:3},
{q:"Hangi göl tuzlu sudur?",a:["Beyşehir Gölü","Tuz Gölü","Abant Gölü","Tortum Gölü"],c:1},
{q:"Pamukkale hangi şehirdedir?",a:["Muğla","Aydın","Denizli","Burdur"],c:2},
{q:"Efes Antik Kenti hangi şehirdedir?",a:["Aydın","İzmir","Muğla","Manisa"],c:1},
{q:"Çin Seddi hangi ülkededir?",a:["Japonya","Hindistan","Çin","Moğolistan"],c:2},
{q:"Piramitler hangi ülkededir?",a:["Türkiye","Irak","Mısır","Libya"],c:2},
{q:"İstiklal Marşı'nı kim yazmıştır?",a:["Atatürk","Mehmet Akif Ersoy","Namık Kemal","Yunus Emre"],c:1},
{q:"Türkiye Cumhuriyeti ne zaman kuruldu?",a:["1920","1923","1925","1930"],c:1},
{q:"Hangisi bir bakliyattır?",a:["Elma","Mercimek","Portakal","Patates"],c:1},
{q:"Buğday hangi ürün grubundadır?",a:["Meyve","Sebze","Tahıl","Bakliyat"],c:2},
{q:"Hangisi Akdeniz Bölgesi'nde bir şehirdir?",a:["Trabzon","Edirne","Antalya","Erzurum"],c:2},
{q:"Hangisi Güneydoğu Anadolu'da bir şehirdir?",a:["Trabzon","İzmir","Bursa","Gaziantep"],c:3},
{q:"Çikolata hangi bitkiden yapılır?",a:["Kahve","Kakao","Çay","Vanilya"],c:1},
{q:"Havuç hangi vitamini içerir?",a:["C vitamini","B vitamini","A vitamini","D vitamini"],c:2},
{q:"İğne yapraklı ağaçlara ne denir?",a:["Yaprak döken","İbreli","Tropikal","Çalı"],c:1},
{q:"Fotosentez için bitkinin neye ihtiyacı vardır?",a:["Gece","Güneş ışığı","Rüzgar","Kar"],c:1},
{q:"Hangisi yenilenebilir enerji kaynağıdır?",a:["Kömür","Petrol","Güneş","Doğalgaz"],c:2},
{q:"Ses hangi ortamda yayılmaz?",a:["Su","Hava","Boşluk","Demir"],c:2},
{q:"Göç eden kuşlara ne ad verilir?",a:["Yerleşik","Göçmen","Yırtıcı","Evcil"],c:1},
{q:"'Anlayana sivrisinek saz, anlamayana davul zurna az' ne demektir?",a:["Müzik çal","Anlayan az sözle kavrar, anlamayana çok söz de yetmez","Sivrisinek yakala","Davul zurna çal"],c:1},
{q:"'Görünüşe aldanma' ne demektir?",a:["Güzel giy","Dış görünüş yanıltıcı olabilir","Aynaya bak","Süslen"],c:1},
{q:"Hollanda'nın başkenti neresidir?",a:["Rotterdam","Amsterdam","Lahey","Brüksel"],c:1},
{q:"Belçika'nın başkenti neresidir?",a:["Amsterdam","Brüksel","Luxemburg","Paris"],c:1},
{q:"İran'ın başkenti neresidir?",a:["Bağdat","Tahran","Şam","Kabil"],c:1},
{q:"Irak'ın başkenti neresidir?",a:["Tahran","Şam","Bağdat","Amman"],c:2},
{q:"Büyük Menderes Nehri hangi denize dökülür?",a:["Karadeniz","Akdeniz","Ege","Marmara"],c:2},
{q:"Yeşilırmak hangi denize dökülür?",a:["Akdeniz","Ege","Marmara","Karadeniz"],c:3},
{q:"Nemrut Dağı hangi ilimizde bulunur?",a:["Ağrı","Adıyaman","Kars","Van"],c:1},
{q:"Kaçkar Dağları hangi bölgemizdedir?",a:["İç Anadolu","Doğu Anadolu","Karadeniz","Akdeniz"],c:2},
{q:"Dünya'da en çok konuşulan dil hangisidir?",a:["İngilizce","İspanyolca","Çince","Hintçe"],c:2},
{q:"Danimarka'nın başkenti neresidir?",a:["Oslo","Helsinki","Stockholm","Kopenhag"],c:3},
{q:"Basketbolda bir takımda sahada kaç kişi bulunur?",a:["5","6","7","11"],c:0},
{q:"Voleybolda bir takımda sahada kaç kişi bulunur?",a:["5","6","7","11"],c:1},
{q:"Dünyanın en küçük kuşu hangisidir?",a:["Serçe","Arı kuşu","Saka","Kanarya"],c:1},
{q:"Termometre neyi ölçer?",a:["Ağırlık","Sıcaklık","Uzunluk","Hız"],c:1},
{q:"Barometre neyi ölçer?",a:["Sıcaklık","Nem","Hava basıncı","Rüzgar"],c:2},
{q:"Hangisi bir çalgı ailesi değildir?",a:["Yaylılar","Üflemeliler","Vurmalılar","Kalemler"],c:3},
{q:"Piyano hangi çalgı ailesine aittir?",a:["Yaylı","Üflemeli","Vurmalı","Tuşlu"],c:3},
{q:"Keman kaç telli bir çalgıdır?",a:["3","4","5","6"],c:1},
{q:"Gitar kaç telli bir çalgıdır?",a:["4","5","6","7"],c:2},
{q:"Ceylan Deresi hangi türe ait bir eserdir?",a:["Şiir","Türkü","Roman","Masal"],c:1},
{q:"19 Mayıs ne bayramıdır?",a:["Çocuk Bayramı","Zafer Bayramı","Gençlik ve Spor Bayramı","Cumhuriyet Bayramı"],c:2},
{q:"30 Ağustos ne bayramıdır?",a:["Çocuk Bayramı","Gençlik Bayramı","Zafer Bayramı","Cumhuriyet Bayramı"],c:2},
{q:"Finlandiya'nın başkenti neresidir?",a:["Oslo","Stockholm","Helsinki","Kopenhag"],c:2},
{q:"Romanya'nın başkenti neresidir?",a:["Budapeşte","Sofya","Bükreş","Belgrad"],c:2},
{q:"Bulgaristan'ın başkenti neresidir?",a:["Bükreş","Belgrad","Sofya","Atina"],c:2},
{q:"Sırbistan'ın başkenti neresidir?",a:["Sofya","Bükreş","Zagreb","Belgrad"],c:3},
{q:"Çeşme hangi şehirdedir?",a:["Muğla","Aydın","İzmir","Antalya"],c:2},
{q:"Kapadokya'nın peri bacaları nasıl oluşmuştur?",a:["İnsan yapımı","Volkanik erozyon","Deprem","Sel"],c:1},
{q:"Hangisi Türkiye'nin iç denizi sayılır?",a:["Karadeniz","Akdeniz","Marmara Denizi","Ege Denizi"],c:2},
{q:"Antarktika'da hangi hayvan yaşar?",a:["Kutup ayısı","Penguen","Aslan","Maymun"],c:1},
{q:"Kuzey Kutbu'nda hangi hayvan yaşar?",a:["Penguen","Zürafa","Kutup ayısı","Kanguru"],c:2},
{q:"'Atasözü' ne demektir?",a:["Babanın sözü","Halkın deneyimlerinden çıkan özlü söz","Öğretmenin sözü","Kitaptaki söz"],c:1},
{q:"'Deyim' ne demektir?",a:["Gerçek anlamı dışında kullanılan kalıplaşmış söz","Uzun cümle","Şiir","Masal"],c:0},
{q:"Küba'nın başkenti neresidir?",a:["Meksiko","Havana","Lima","Bogota"],c:1},
{q:"Suudi Arabistan'ın başkenti neresidir?",a:["Dubai","Mekke","Riyad","Medine"],c:2},
{q:"Toros Dağları hangi bölgemizdedir?",a:["Karadeniz","Akdeniz","İç Anadolu","Ege"],c:1},
{q:"Aras Nehri hangi bölgemizden geçer?",a:["Marmara","Ege","Doğu Anadolu","Akdeniz"],c:2},
{q:"Meriç Nehri hangi bölgemizdedir?",a:["Karadeniz","Marmara","Ege","İç Anadolu"],c:1},
{q:"Suya batmayan metal hangisidir?",a:["Demir","Bakır","Sodyum","Altın"],c:2},
{q:"Hangisi fosil yakıt değildir?",a:["Kömür","Petrol","Rüzgar","Doğalgaz"],c:2},
{q:"Hint Okyanusu hangi kıtalar arasındadır?",a:["Amerika-Avrupa","Asya-Afrika-Avustralya","Avrupa-Afrika","Amerika-Asya"],c:1},
{q:"Kuzey Buz Denizi (Arktik) nerededir?",a:["Güney Kutbu","Kuzey Kutbu","Ekvator","Tropikal bölge"],c:1},
{q:"'Minareyi çalan kılıfını hazırlar' ne demektir?",a:["Minare yap","Kötülük yapan önlemini alır","Kılıf dik","Çalmak kötü"],c:1},
{q:"'Bugünün işini yarına bırakma' ne demektir?",a:["Yarın tatil","İşini zamanında yap","Bugün dinlen","Yarın çalış"],c:1},
{q:"Kolombiya'nın başkenti neresidir?",a:["Lima","Buenos Aires","Bogota","Santiago"],c:2},
{q:"Şili'nin başkenti neresidir?",a:["Buenos Aires","Lima","Montevideo","Santiago"],c:3},
{q:"Seyhan Nehri hangi şehirden geçer?",a:["Mersin","Antalya","Adana","Hatay"],c:2},
{q:"Ceyhan Nehri hangi bölgededir?",a:["Karadeniz","İç Anadolu","Akdeniz","Ege"],c:2},
{q:"Süphan Dağı hangi ilimizde bulunur?",a:["Ağrı","Van","Bitlis","Muş"],c:2},
{q:"İda (Kaz) Dağı hangi ilimize yakındır?",a:["İstanbul","Çanakkale","İzmir","Bursa"],c:1},
{q:"Hangisi bir ada ülkesidir?",a:["Almanya","İtalya","İngiltere","Fransa"],c:2},
{q:"Dünya'nın en büyük çölü hangisidir?",a:["Gobi","Sahra","Atacama","Kalahari"],c:1},
{q:"Gökkuşağının ilk rengi nedir?",a:["Mavi","Kırmızı","Yeşil","Sarı"],c:1},
{q:"Dünya'nın katmanlarından hangisi en dıştadır?",a:["Çekirdek","Manto","Yer kabuğu","İç çekirdek"],c:2},
{q:"Hangisi bir orkestra çalgısı değildir?",a:["Flüt","Obua","Saz","Klarnet"],c:2},
{q:"Mozart hangi ülkede doğmuştur?",a:["Almanya","İtalya","Avusturya","Fransa"],c:2},
{q:"Beethoven hangi ülkelidir?",a:["Avusturya","İtalya","Almanya","Fransa"],c:2},
{q:"Nasrettin Hoca hangi yüzyılda yaşamıştır?",a:["11.","12.","13.","14."],c:2},
{q:"Keloğlan masallarında Keloğlan'ın özelliği nedir?",a:["Uzun saçlı","Kel","Kısa boylu","Şişman"],c:1},
{q:"Mısır'ın para birimi nedir?",a:["Dolar","Riyal","Lira","Mısır Lirası"],c:3},
{q:"Firavunlar hangi ülkenin eski yöneticileriydi?",a:["Irak","Mısır","İran","Hindistan"],c:1},
{q:"'Ağaç yaşken eğilir' ne demektir?",a:["Ağaç kes","Eğitim küçükken verilir","Ağaç dik","Yaşlan"],c:1},
{q:"'Yalancının mumu yatsıya kadar yanar' ne demektir?",a:["Mum yak","Yalan er geç ortaya çıkar","Yatsı namazı kıl","Gece ol"],c:1},
{q:"Endonezya hangi kıtadadır?",a:["Afrika","Avrupa","Asya","Güney Amerika"],c:2},
{q:"Hangisi bir su sporudur?",a:["Futbol","Yüzme","Koşu","Tenis"],c:1},
{q:"Çekya'nın başkenti neresidir?",a:["Bratislava","Varşova","Budapeşte","Prag"],c:3},
{q:"Amazon Nehri dünyanın en ne nehridir?",a:["En kısa","En dar","Suyu en bol","En tuzlu"],c:2},
{q:"Dünya'da en çok ada bulunan ülke hangisidir?",a:["Japonya","Filipinler","İsveç","Endonezya"],c:3},
{q:"Hangi gezegen Güneş'e en yakındır?",a:["Dünya","Venüs","Merkür","Mars"],c:2},
{q:"Nobel ödülü hangi ülkede verilir?",a:["ABD","İngiltere","İsveç","Almanya"],c:2},
{q:"Hangisi bir Türk halk oyunudur?",a:["Vals","Tango","Horon","Samba"],c:2},
{q:"Piri Reis neyle ünlüdür?",a:["Şiir","Harita","Müzik","Resim"],c:1},
{q:"Hangisi bir olimpiyat sporu değildir?",a:["Yüzme","Jimnastik","Bilardo","Atletizm"],c:2},
{q:"Dünya'nın en uzun nehri hangisidir?",a:["Amazon","Nil","Tuna","Mississippi"],c:1}
],
hard:[
{q:"'Üzüm üzüme baka baka kararır' ne demektir?",a:["Üzüm ye","İnsanlar çevresinden etkilenir","Üzüm topla","Bağa git"],c:1},
{q:"'Yerin kulağı vardır' ne demektir?",a:["Yer dinler","Her yerde seni duyabilirler, dikkatli ol","Kulak temizle","Yere eğil"],c:1},
{q:"'Bıçak kemiğe dayandı' ne demektir?",a:["Kemik kır","Tahammülün sınırına gelindi","Bıçak kes","Et ye"],c:1},
{q:"'Sütten ağzı yanan yoğurdu üfleyerek yer' ne demektir?",a:["Yoğurt ye","Kötü tecrübe yaşayan çok temkinli olur","Süt iç","Üfle"],c:1},
{q:"'Gönül ne kahve ister ne kahvehane' ne demektir?",a:["Kahve iç","Önemli olan samimiyet ve dostluktur","Kahvehaneye git","Kahve yapma"],c:1},
{q:"'Lafla peynir gemisi yürümez' ne demektir?",a:["Peynir al","Sadece konuşmakla iş olmaz, eylem gerek","Gemi sür","Laf etme"],c:1},
{q:"'Deveye hendek atlatmak' ne demektir?",a:["Deve bin","Zor ve imkansız bir işi yaptırmak","Hendek kaz","Deve sat"],c:1},
{q:"'Ayağını yorganına göre uzat' ne demektir?",a:["Uyu","Harcamalarını gelirine göre ayarla","Yorgan al","Ayağını uzat"],c:1},
{q:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",a:["Ateş yak","Her söylentinin bir gerçeklik payı vardır","Duman çıkar","Yangın söndür"],c:1},
{q:"'Kırk yıllık Kani olur mu Yani' ne demektir?",a:["İsim değiştir","Eski alışkanlıklar kolay değişmez","Kırk yıl bekle","Yeni ol"],c:1},
{q:"Ukrayna'nın başkenti neresidir?",a:["Moskova","Minsk","Kiev","Varşova"],c:2},
{q:"Fırat Nehri hangi ülkelerden geçer?",a:["Türkiye-İran-Irak","Türkiye-Suriye-Irak","Türkiye-Gürcistan","Türkiye-Ermenistan"],c:1},
{q:"Dicle Nehri'nin uzunluğu yaklaşık kaç km'dir?",a:["900","1900","2900","3900"],c:1},
{q:"Ganj Nehri hangi ülkededir?",a:["Çin","Pakistan","Hindistan","Bangladeş"],c:2},
{q:"Mississippi Nehri hangi ülkededir?",a:["Kanada","Brezilya","ABD","Meksika"],c:2},
{q:"Volga Nehri hangi ülkededir?",a:["Ukrayna","Polonya","Almanya","Rusya"],c:3},
{q:"Ren Nehri hangi kıtadadır?",a:["Asya","Afrika","Güney Amerika","Avrupa"],c:3},
{q:"Hazar Denizi aslında ne tür bir su kütlesidir?",a:["Deniz","Okyanus","Göl","Kanal"],c:2},
{q:"Baykal Gölü hangi ülkededir?",a:["Çin","Moğolistan","Rusya","Kazakistan"],c:2},
{q:"Dünya'nın en derin gölü hangisidir?",a:["Van Gölü","Hazar","Baykal","Viktorya"],c:2},
{q:"Viktorya Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Büyük Set Resifi hangi ülkenin kıyısındadır?",a:["Brezilya","Hindistan","Avustralya","Meksika"],c:2},
{q:"Panama Kanalı hangi okyanusları birleştirir?",a:["Atlas-Hint","Pasifik-Atlas","Hint-Pasifik","Atlas-Arktik"],c:1},
{q:"Süveyş Kanalı hangi ülkededir?",a:["Türkiye","Irak","Suriye","Mısır"],c:3},
{q:"Ilgaz Dağı hangi illerimiz arasındadır?",a:["Ankara-Çankırı","Çankırı-Kastamonu","Bolu-Düzce","Sinop-Samsun"],c:1},
{q:"Bolkar Dağları hangi bölgemizdedir?",a:["Doğu Anadolu","İç Anadolu","Akdeniz","Karadeniz"],c:2},
{q:"Munzur Dağları hangi ilimizde bulunur?",a:["Erzurum","Erzincan","Tunceli","Bingöl"],c:2},
{q:"Türkiye'de en çok yağış alan bölge hangisidir?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Marmara Denizi Türkiye'nin neresindedir?",a:["Güney","Kuzey","Kuzeybatı","Güneydoğu"],c:2},
{q:"Çin'in en uzun nehri hangisidir?",a:["Sarı Irmak","Yangtze","Mekong","Amur"],c:1},
{q:"Sarı Irmak hangi ülkededir?",a:["Japonya","Hindistan","Çin","Kore"],c:2},
{q:"Mekong Nehri hangi bölgeden geçer?",a:["Orta Doğu","Güneydoğu Asya","Kuzey Afrika","Güney Amerika"],c:1},
{q:"Mariana Çukuru hangi okyanustadır?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Mariana Çukuru yaklaşık kaç metre derindir?",a:["5000","8000","11000","15000"],c:2},
{q:"Türkiye'nin yüzölçümü yaklaşık kaç km²'dir?",a:["483.000","583.000","683.000","783.000"],c:3},
{q:"Hangi ülke hem Avrupa'da hem Asya'da toprak sahibidir?",a:["Yunanistan","Mısır","Türkiye","İran"],c:2},
{q:"Nasrettin Hoca hangi şehirle özdeşleşmiştir?",a:["Konya","Eskişehir","Akşehir","Afyon"],c:2},
{q:"Yunus Emre ne tür eserler yazmıştır?",a:["Roman","Tiyatro","Şiir","Hikaye"],c:2},
{q:"'Karga kekliğe bakıp yürümeye kalkmış' ne demektir?",a:["Karga izle","Özenmek kendine zarar verir","Keklik yakala","Kuş seyret"],c:1},
{q:"'Su uyur düşman uyumaz' ne demektir?",a:["Su iç","Her zaman tetikte ol","Uyu","Düşmanı sev"],c:1},
{q:"'Ava giden avlanır' ne demektir?",a:["Ava git","Başkasına kötülük yapmaya çalışan kendisi zarar görür","Avlan","Ormana git"],c:1},
{q:"'Taşıma su ile değirmen dönmez' ne demektir?",a:["Su taşı","Dışarıdan sürekli destek alarak iş sürdürülmez","Değirmen yap","Su getir"],c:1},
{q:"Tuz Gölü hangi iller arasındadır?",a:["Ankara-Konya-Aksaray","İstanbul-Bursa","İzmir-Manisa","Antalya-Burdur"],c:0},
{q:"Burdur Gölü neden önemlidir?",a:["En büyük göl","Tuzlu göl","Kuş cenneti","Ada göl"],c:2},
{q:"Sapanca Gölü hangi bölgemizdedir?",a:["İç Anadolu","Ege","Marmara","Karadeniz"],c:2},
{q:"Tortum Gölü hangi ilimizde bulunur?",a:["Artvin","Erzurum","Kars","Trabzon"],c:1},
{q:"Abant Gölü hangi ilimizde bulunur?",a:["Düzce","Bolu","Ankara","Eskişehir"],c:1},
{q:"Eğirdir Gölü hangi ilimizde bulunur?",a:["Burdur","Antalya","Konya","Isparta"],c:3},
{q:"Aral Gölü hangi kıtadadır?",a:["Avrupa","Asya","Afrika","Amerika"],c:1},
{q:"Büyük Göller hangi ülkelerdedir?",a:["Rusya-Çin","ABD-Kanada","Brezilya-Arjantin","İngiltere-Fransa"],c:1},
{q:"Kongo Nehri hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Zambezi Nehri'ndeki ünlü şelale hangisidir?",a:["Niagara","Angel","Victoria","İguazu"],c:2},
{q:"Niagara Şelalesi hangi ülkeler arasındadır?",a:["Brezilya-Arjantin","ABD-Kanada","Meksika-ABD","Zambiya-Zimbabve"],c:1},
{q:"K2 dağı hangi sıradağ sistemindedir?",a:["Alpler","Himalayalar","Karakurum","And"],c:2},
{q:"McKinley (Denali) Dağı hangi ülkededir?",a:["Kanada","ABD","Meksika","Rusya"],c:1},
{q:"Vezüv Yanardağı hangi ülkededir?",a:["Yunanistan","Türkiye","İtalya","İspanya"],c:2},
{q:"Fuji Dağı hangi ülkededir?",a:["Çin","Kore","Japonya","Vietnam"],c:2},
{q:"Türkiye'nin en uzun sınırı hangi ülkeyledir?",a:["Suriye","İran","Irak","Yunanistan"],c:0},
{q:"'Denizden çıkmış balığa benzemek' ne demektir?",a:["Balık tut","Şaşkın ve çaresiz kalmak","Yüz","Denize git"],c:1},
{q:"'Kendi düşen ağlamaz' ne demektir?",a:["Ağlama","Hatasının sonucuna katlanan şikayet etmez","Düşme","Koş"],c:1},
{q:"'İğneyi kendine çuvaldızı başkasına batır' ne demektir?",a:["İğne batır","Önce kendini eleştir sonra başkalarını","Dikiş dik","Çuvaldız al"],c:1},
{q:"'Nerde hareket orda bereket' ne demektir?",a:["Hareket et","Çalışan ve harekete geçen bereketini bulur","Bereket getir","Dur"],c:1},
{q:"'Davulun sesi uzaktan hoş gelir' ne demektir?",a:["Davul çal","Uzaktan güzel görünen yakından öyle olmayabilir","Uzak dur","Müzik dinle"],c:1},
{q:"'Her işte bir hayır vardır' ne demektir?",a:["Hayır de","Kötü görünen olaylarda da iyi taraf olabilir","İş yap","Hayır bul"],c:1},
{q:"Avustralya hangi kıtadır?",a:["Ada","Kıta","Yarımada","Takımada"],c:1},
{q:"Hangisi bir yarımada değildir?",a:["Arabistan","İskandinavya","Avustralya","İtalya"],c:2},
{q:"Ekvator çizgisi neyi böler?",a:["Doğu-Batı","Kuzey-Güney","Gece-Gündüz","Yaz-Kış"],c:1},
{q:"Greenwich meridyeni neyi belirler?",a:["Enlem","Boylam başlangıcı","Yükseklik","Derinlik"],c:1},
{q:"Türkiye kaç yarımkürededir?",a:["Sadece Kuzey","Sadece Doğu","Kuzey ve Doğu","Kuzey ve Batı"],c:2},
{q:"Futbolda ofsayt kuralı ne demektir?",a:["Elle oynama","Hücum oyuncusu savunma çizgisinin gerisinde kalma","Kırmızı kart","Penaltı"],c:1},
{q:"Hangi sporda 'smash' vuruşu yapılır?",a:["Futbol","Basketbol","Badminton","Yüzme"],c:2},
{q:"Türkiye'nin ilk kadın pilotu kimdir?",a:["Sabiha Gökçen","Halide Edip","Afet İnan","Latife Hanım"],c:0},
{q:"Leonardo da Vinci hangi yüzyılda yaşamıştır?",a:["13-14.","14-15.","15-16.","16-17."],c:2},
{q:"Mona Lisa tablosu hangi müzededir?",a:["British Museum","Prado","Louvre","Uffizi"],c:2},
{q:"Hangisi bir Türk halk müziği çalgısıdır?",a:["Piyano","Keman","Bağlama","Gitar"],c:2},
{q:"Hangisi bir Türk sanat müziği formu değildir?",a:["Şarkı","Gazel","Rock","Beste"],c:2},
{q:"Barış Manço hangi müzik türünde eserler vermiştir?",a:["Klasik","Anadolu Rock","Jazz","Opera"],c:1},
{q:"İlk Türk devleti hangisidir?",a:["Osmanlı","Selçuklu","Göktürk","Büyük Hun"],c:3},
{q:"Malazgirt Savaşı kaç yılında yapılmıştır?",a:["1071","1176","1243","1453"],c:0},
{q:"İstanbul'un fethi kaç yılındadır?",a:["1071","1299","1453","1923"],c:2},
{q:"Osmanlı Devleti'nin kurucusu kimdir?",a:["Fatih","Kanuni","Osman Gazi","Yavuz"],c:2},
{q:"Kurtuluş Savaşı hangi yıllar arasında yapılmıştır?",a:["1914-1918","1919-1922","1923-1930","1939-1945"],c:1},
{q:"TBMM ne zaman açılmıştır?",a:["29 Ekim 1923","23 Nisan 1920","19 Mayıs 1919","30 Ağustos 1922"],c:1},
{q:"'Körle yatan şaşı kalkar' ne demektir?",a:["Uyu","Kötü arkadaş kötü alışkanlık kazandırır","Şaşı ol","Gözlük tak"],c:1},
{q:"'Tencere yuvarlanmış kapağını bulmuş' ne demektir?",a:["Tencere al","Birbirine uygun kişiler bir araya gelir","Kapak bul","Yemek yap"],c:1},
{q:"Hırvatistan'ın başkenti neresidir?",a:["Belgrad","Ljubljana","Zagreb","Saraybosna"],c:2},
{q:"Bosna Hersek'in başkenti neresidir?",a:["Zagreb","Belgrad","Saraybosna","Podgorica"],c:2},
{q:"Coruh Nehri hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Dalaman Çayı hangi denize dökülür?",a:["Karadeniz","Akdeniz","Ege","Marmara"],c:1},
{q:"Manavgat Çayı hangi şehirdedir?",a:["Mersin","Muğla","Antalya","İzmir"],c:2},
{q:"Köprülü Kanyon hangi şehirdedir?",a:["Muğla","Antalya","Burdur","Isparta"],c:1},
{q:"Kapıdağ Yarımadası hangi denizde bulunur?",a:["Karadeniz","Ege","Akdeniz","Marmara"],c:3},
{q:"Sinop Yarımadası hangi denize uzanır?",a:["Marmara","Ege","Akdeniz","Karadeniz"],c:3},
{q:"Datça Yarımadası hangi bölgededir?",a:["Marmara","Karadeniz","Ege","İç Anadolu"],c:2},
{q:"Evliya Çelebi neyle ünlüdür?",a:["Resim","Seyahatname","Müzik","Şiir"],c:1},
{q:"Hangisi Atatürk'ün yaptığı inkılaplardandır?",a:["Matbaa","Harf İnkılabı","Telgraf","Radyo"],c:1},
{q:"Dünya'nın en büyük okyanusu hangisidir?",a:["Atlantik","Hint","Pasifik","Arktik"],c:2},
{q:"Hangisi bir Rönesans sanatçısıdır?",a:["Picasso","Leonardo da Vinci","Van Gogh","Monet"],c:1},
{q:"Hangi icat Thomas Edison'a aittir?",a:["Telefon","Ampul","Radyo","Televizyon"],c:1},
{q:"FIFA Dünya Kupası hangi spordadır?",a:["Basketbol","Voleybol","Futbol","Tenis"],c:2},
{q:"Hangisi Türkiye'nin yedi bölgesinden biri değildir?",a:["Marmara","Trakya","Akdeniz","Karadeniz"],c:1},
{q:"Göreme hangi ilimizde yer alır?",a:["Kayseri","Nevşehir","Aksaray","Niğde"],c:1},
{q:"Hangi müzik aleti telli çalgıdır?",a:["Davul","Flüt","Gitar","Trompet"],c:2},
{q:"Türk edebiyatının en ünlü şairlerinden biri kimdir?",a:["Newton","Einstein","Yunus Emre","Pasteur"],c:2},
{q:"Hangisi bir Akdeniz ülkesi değildir?",a:["İtalya","Yunanistan","Norveç","İspanya"],c:2},
{q:"Dünya'nın en kalabalık ülkesi hangisidir?",a:["ABD","Hindistan","Rusya","Brezilya"],c:1},
{q:"Hangi buluşu Graham Bell yapmıştır?",a:["Ampul","Telefon","Radyo","Bilgisayar"],c:1},
{q:"Mozart hangi ülkedendir?",a:["Almanya","İtalya","Avusturya","Fransa"],c:2},
{q:"Hangisi bir su sporudur?",a:["Boks","Güreş","Kürek","Karate"],c:2},
{q:"Nasrettin Hoca hangi ilimizden gelmiştir?",a:["Konya","Ankara","Aksaray","Eskişehir"],c:0},
{q:"Hangi hayvan gece görüşü en iyi olandır?",a:["Tavuk","Baykuş","Güvercin","Serçe"],c:1},
{q:"Hangisi Yedi Harika'dandır?",a:["Eyfel Kulesi","Mısır Piramitleri","Big Ben","Kız Kulesi"],c:1},
{q:"Dünya'nın en soğuk kıtası hangisidir?",a:["Avrupa","Asya","Antarktika","Kuzey Amerika"],c:2},
{q:"Hangisi bir Nobel dalıdır?",a:["Spor","Edebiyat","Tarih","Coğrafya"],c:1},
{q:"Hangi padişah döneminde İstanbul fethedildi?",a:["Yavuz","Kanuni","Fatih","Murat"],c:2},
{q:"Hangisi bir olimpiyat sembolüdür?",a:["Yıldız","Beş halka","Üçgen","Kare"],c:1},
{q:"Venedik hangi ülkededir?",a:["Fransa","İspanya","İtalya","Yunanistan"],c:2},
{q:"Barış Manço hangi alanda ünlüdür?",a:["Spor","Müzik","Edebiyat","Sinema"],c:1},
{q:"Hangisi bir takım sporu değildir?",a:["Futbol","Basketbol","Tenis","Voleybol"],c:2},
{q:"Dünya'nın en uzun duvarı hangisidir?",a:["Berlin Duvarı","Çin Seddi","Adriyatik Duvarı","Roma Duvarı"],c:1},
{q:"Hangisi bir geleneksel Türk el sanatıdır?",a:["Origami","Ebru","Bonsai","İkebana"],c:1},
{q:"Ay'a ilk ayak basan insan kimdir?",a:["Gagarin","Armstrong","Aldrin","Collins"],c:1},
{q:"Hangisi bir Türk marşıdır?",a:["Marseyyez","İstiklal Marşı","God Save","Star Spangled"],c:1},
{q:"Çanakkale Savaşı hangi savaşın parçasıdır?",a:["Kurtuluş Savaşı","I. Dünya Savaşı","II. Dünya Savaşı","Balkan Savaşı"],c:1}
],
very_hard:[
{q:"'Sürüden ayrılanı kurt kapar' ne demektir?",a:["Kurt yakala","Topluluktan ayrılan tehlikeye düşer","Sürüye kat","Kurt besle"],c:1},
{q:"'Mum dibine ışık vermez' ne demektir?",a:["Mum yak","Kişi en yakınlarına fayda sağlayamayabilir","Işık aç","Karanlık"],c:1},
{q:"'Hamama giren terler' ne demektir?",a:["Hamama git","Bir işe girişen zorluklarına katlanır","Terle","Yıkan"],c:1},
{q:"'Olmaz olmaz deme olmaz olmaz' ne demektir?",a:["Olmaz de","Hiçbir şeyi imkansız görme","Her şey olur","Olur de"],c:1},
{q:"'Bakarsan bağ olur bakmazsan dağ olur' ne demektir?",a:["Bağ dik","İlgilenirsen güzelleşir, ilgilenmezsen bozulur","Dağa çık","Bağa git"],c:1},
{q:"'Ak akçe kara gün içindir' ne demektir?",a:["Para harca","Paranı zor günler için biriktir","Akçe bul","Kara gün gelir"],c:1},
{q:"'Abanoz böceği meşeyi yer' ne demektir?",a:["Böcek yakala","Küçük ama sürekli zarar büyük sonuçlar doğurur","Meşe kes","Ağaç dik"],c:1},
{q:"'Her kuşun eti yenmez' ne demektir?",a:["Kuş ye","Her kişiyle başa çıkılamaz","Kuş yakala","Et ye"],c:1},
{q:"'Dut yemiş bülbüle döndü' ne demektir?",a:["Dut ye","Sessizleşti, sustu","Bülbül dinle","Şarkı söyle"],c:1},
{q:"'Çoğu zarar azı karar' ne demektir?",a:["Az ye","Her şeyin ölçüsünü bil, fazlası zararlı","Çok al","Az harca"],c:1},
{q:"Orinoko Nehri hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Avrupa"],c:2},
{q:"İndus Nehri hangi ülkelerden geçer?",a:["Hindistan-Bangladeş","Çin-Hindistan-Pakistan","Hindistan-Nepal","Çin-Moğolistan"],c:1},
{q:"Lena Nehri hangi ülkededir?",a:["Kanada","Çin","Rusya","ABD"],c:2},
{q:"Ob Nehri hangi ülkededir?",a:["Çin","Rusya","Kanada","ABD"],c:1},
{q:"Yenisey Nehri hangi ülkededir?",a:["Kanada","Rusya","Çin","Moğolistan"],c:1},
{q:"Niger Nehri hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Murray Nehri hangi ülkededir?",a:["ABD","Kanada","Avustralya","Yeni Zelanda"],c:2},
{q:"Aconcagua Dağı hangi ülkededir?",a:["Şili","Peru","Brezilya","Arjantin"],c:3},
{q:"Elbrus Dağı hangi ülkededir?",a:["Türkiye","Gürcistan","Rusya","İran"],c:2},
{q:"Mont Blanc hangi ülkeler arasındadır?",a:["İsviçre-Avusturya","Fransa-İtalya","İspanya-Fransa","İtalya-Avusturya"],c:1},
{q:"Avrupa'nın en yüksek dağı hangisidir?",a:["Mont Blanc","Elbrus","Mattherhorn","Olimpos"],c:1},
{q:"Afrika'nın en yüksek dağı hangisidir?",a:["Atlas","Kenya","Kilimanjaro","Ruwenzori"],c:2},
{q:"Kuzey Amerika'nın en yüksek dağı hangisidir?",a:["Rocky","McKinley (Denali)","Appalachian","Sierra Nevada"],c:1},
{q:"Güney Amerika'nın en yüksek dağı hangisidir?",a:["Chimborazo","Huascaran","Cotopaxi","Aconcagua"],c:3},
{q:"Avustralya'nın en yüksek dağı hangisidir?",a:["Uluru","Kosciuszko","Blue Mountain","Cook"],c:1},
{q:"Antarktika'nın en yüksek dağı hangisidir?",a:["Erebus","Kirkpatrick","Vinson","Sidley"],c:2},
{q:"Çad Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Afrika","Avrupa"],c:2},
{q:"Titicaca Gölü hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Kuzey Amerika"],c:2},
{q:"Balkaş Gölü hangi ülkededir?",a:["Rusya","Moğolistan","Kazakistan","Kırgızistan"],c:2},
{q:"Ladoga Gölü hangi ülkededir?",a:["Finlandiya","İsveç","Norveç","Rusya"],c:3},
{q:"Tanganyika Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Malavi Gölü hangi kıtadadır?",a:["Asya","Afrika","Güney Amerika","Avrupa"],c:1},
{q:"Pasifik Okyanusu dünya yüzeyinin yüzde kaçını kaplar?",a:["15","22","30","46"],c:2},
{q:"Dünya'da kaç okyanus vardır?",a:["3","4","5","6"],c:2},
{q:"Güney Buz Denizi (Antarktik Okyanus) hangi kıtanın çevresindedir?",a:["Arktik","Avustralya","Antarktika","Güney Amerika"],c:2},
{q:"Sargasso Denizi hangi okyanustadır?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Hangi boğaz Asya ve Kuzey Amerika'yı ayırır?",a:["Cebelitarık","Malakka","Bering","Hürmüz"],c:2},
{q:"Cebelitarık Boğazı hangi kıtaları ayırır?",a:["Avrupa-Asya","Asya-Afrika","Avrupa-Afrika","Amerika-Avrupa"],c:2},
{q:"Pangea ne demektir?",a:["İlk okyanus","Tüm kıtaların birleşik hali","İlk atmosfer","İlk göl"],c:1},
{q:"Gondwana hangi kıtaları içeriyordu?",a:["Avrupa-Asya","Afrika-G.Amerika-Avustralya-Antarktika-Hindistan","K.Amerika-Avrupa","Asya-K.Amerika"],c:1},
{q:"Laurasia hangi kıtaları içeriyordu?",a:["Afrika-G.Amerika","K.Amerika-Avrupa-Asya","Avustralya-Antarktika","G.Amerika-Afrika"],c:1},
{q:"Hangi sıradağ Kuzey Amerika'nın batısında uzanır?",a:["Appalachian","And","Rocky","Atlas"],c:2},
{q:"Appalachian Dağları hangi ülkededir?",a:["Kanada","Meksika","ABD","Brezilya"],c:2},
{q:"Atlas Dağları hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Ural Dağları hangi kıtaları ayırır?",a:["Avrupa-Afrika","Avrupa-Asya","Asya-Amerika","Asya-Afrika"],c:1},
{q:"'Dervişin fikri neyse zikri de odur' ne demektir?",a:["Dua et","Kişi aklından geçeni söyler","Derviş ol","Fikir sor"],c:1},
{q:"'El el ile değil gönül gönül ile' ne demektir?",a:["El sık","Gerçek bağ yürekten kurulur","Gönül al","El aç"],c:1},
{q:"'Aşk olmayınca meşk olmaz' ne demektir?",a:["Aşık ol","Sevgi olmadan öğrenmek/çalışmak olmaz","Meşk et","Müzik çal"],c:1},
{q:"'Kaz gelecek yerden tavuk esirgenmez' ne demektir?",a:["Kaz besle","Büyük kazanç için küçük harcama yapılır","Tavuk sat","Kaz ye"],c:1},
{q:"'Besle kargayı oysun gözünü' ne demektir?",a:["Karga besle","İyilik yaptığın kişi sana kötülük yapabilir","Göz kapat","Kargayı kov"],c:1},
{q:"Mimar Sinan'ın en ünlü eseri hangisidir?",a:["Sultanahmet","Süleymaniye","Selimiye","Ayasofya"],c:2},
{q:"Piri Reis neyle tanınır?",a:["Şiir","Harita","Mimari","Müzik"],c:1},
{q:"Hezarfen Ahmet Çelebi neyle tanınır?",a:["Roket","Uçma denemesi","Denizaltı","Teleskop"],c:1},
{q:"İbn-i Sina hangi alanda öncüdür?",a:["Matematik","Mimari","Tıp","Astronomi"],c:2},
{q:"Ali Kuşçu hangi alanda çalışmıştır?",a:["Tıp","Astronomi","Mimari","Edebiyat"],c:1},
{q:"Fatih Sultan Mehmet İstanbul'u fethettiğinde kaç yaşındaydı?",a:["18","21","25","30"],c:1},
{q:"Çanakkale Savaşı hangi yılda yapılmıştır?",a:["1912","1915","1918","1922"],c:1},
{q:"Sakarya Meydan Muharebesi hangi yılda yapılmıştır?",a:["1920","1921","1922","1923"],c:1},
{q:"Büyük Taarruz hangi yılda başlamıştır?",a:["1920","1921","1922","1923"],c:2},
{q:"Lozan Antlaşması hangi yılda imzalanmıştır?",a:["1920","1921","1922","1923"],c:3},
{q:"Anadolu Hisarı'nı kim yaptırmıştır?",a:["Fatih Sultan Mehmet","Yıldırım Bayezid","Kanuni","II. Mehmet"],c:1},
{q:"Rumeli Hisarı'nı kim yaptırmıştır?",a:["Yıldırım Bayezid","Fatih Sultan Mehmet","Kanuni","Murat II"],c:1},
{q:"Selimiye Camii hangi şehirdedir?",a:["İstanbul","Bursa","Edirne","Ankara"],c:2},
{q:"Türkiye'nin en kalabalık şehri hangisidir?",a:["Ankara","İzmir","İstanbul","Bursa"],c:2},
{q:"Göbeklitepe hangi şehirdedir?",a:["Diyarbakır","Mardin","Şanlıurfa","Gaziantep"],c:2},
{q:"Karain Mağarası hangi şehirdedir?",a:["Antalya","Mersin","Muğla","Burdur"],c:0},
{q:"Truva Antik Kenti hangi şehirdedir?",a:["İzmir","Çanakkale","Balıkesir","Manisa"],c:1},
{q:"Aspendos Antik Tiyatrosu hangi şehirdedir?",a:["İzmir","Muğla","Antalya","Mersin"],c:2},
{q:"Sümela Manastırı hangi şehirdedir?",a:["Artvin","Rize","Trabzon","Giresun"],c:2},
{q:"Divriği Ulu Camii hangi şehirdedir?",a:["Erzurum","Sivas","Kayseri","Malatya"],c:1},
{q:"Dünya'nın en uzun kıyı şeridine sahip ülke hangisidir?",a:["ABD","Avustralya","Kanada","Rusya"],c:2},
{q:"Dünya'nın en kalabalık ülkesi hangisidir?",a:["ABD","Çin","Hindistan","Endonezya"],c:2},
{q:"Amazon Yağmur Ormanları büyük bölümü hangi ülkededir?",a:["Kolombiya","Peru","Venezuela","Brezilya"],c:3},
{q:"Sahra Çölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Gobi Çölü hangi ülkelerdedir?",a:["İran-Irak","Çin-Moğolistan","Hindistan-Pakistan","Mısır-Libya"],c:1},
{q:"'Et tırnaktan ayrılmaz' ne demektir?",a:["Et ye","Yakın akrabalar birbirinden kopmaz","Tırnak kes","Et kes"],c:1},
{q:"'Hazıra dağlar dayanmaz' ne demektir?",a:["Dağa çık","Çalışmadan harcanan ne kadar çok olursa olsun biter","Hazırla","Dağı aş"],c:1},
{q:"'İki cambaz bir ipte oynamaz' ne demektir?",a:["Cambaz ol","Aynı yerde iki lider olmaz","İp atla","Cambaz seyret"],c:1},
{q:"Dünyanın en büyük adası hangisidir?",a:["Madagaskar","Borneo","Grönland","Sumatra"],c:2},
{q:"Dünyanın en yüksek şelalesi hangisidir?",a:["Niagara","Victoria","Angel","İguazu"],c:2},
{q:"Congo Nehri hangi okyanusa dökülür?",a:["Hint","Pasifik","Atlas","Arktik"],c:2},
{q:"Okavango Deltası hangi ülkededir?",a:["Güney Afrika","Tanzanya","Botsvana","Kenya"],c:2},
{q:"Takla Makan Çölü hangi ülkededir?",a:["Moğolistan","İran","Çin","Pakistan"],c:2},
{q:"Kalahari Çölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"'Gülü seven dikenine katlanır' ne demektir?",a:["Gül topla","Bir şeyi seven zorluklarına da katlanır","Diken batır","Bahçe yap"],c:1},
{q:"'Aç ayı oynamaz' ne demektir?",a:["Ayı besle","Karşılığı olmadan kimse çalışmaz","Ayı izle","Oyun oyna"],c:1},
{q:"'Her yiğidin bir yoğurt yiyişi vardır' ne demektir?",a:["Yoğurt ye","Herkesin kendine göre bir yöntemi vardır","Yiğit ol","Yoğurt yap"],c:1},
{q:"'Boş çuval ayakta durmaz' ne demektir?",a:["Çuval doldur","Bilgisiz ve beceriksiz kişi başarısız olur","Çuval at","Ayakta dur"],c:1},
{q:"'Yuvayı dişi kuş yapar' ne demektir?",a:["Kuş besle","Evi asıl düzenleyen kadındır","Yuva yap","Kuş izle"],c:1},
{q:"Dünya'nın çekirdeği hangi metallerden oluşur?",a:["Bakır-Çinko","Altın-Gümüş","Demir-Nikel","Alüminyum-Titan"],c:2},
{q:"Büyük Okyanus'un diğer adı nedir?",a:["Atlas","Pasifik","Hint","Arktik"],c:1},
{q:"İklim ve hava durumu arasındaki fark nedir?",a:["Fark yok","İklim uzun süreli, hava durumu kısa süreli","İklim kısa süreli","Hava durumu uzun süreli"],c:1},
{q:"Rüzgar nasıl oluşur?",a:["Güneş doğunca","Basınç farkından","Yağmur yağınca","Deprem olunca"],c:1},
{q:"Türkiye'nin en doğusundaki il hangisidir?",a:["Van","Kars","Hakkari","Iğdır"],c:2},
{q:"Dünyanın en derin noktası neresidir?",a:["Everest","Mariana Çukuru","Amazon","Büyük Kanyon"],c:1},
{q:"Hangi bilim insanı yerçekimini keşfetti?",a:["Einstein","Galileo","Newton","Darwin"],c:2},
{q:"Hangisi Picasso'nun bir eseridir?",a:["Mona Lisa","Guernica","Yıldızlı Gece","Çığlık"],c:1},
{q:"Olimpiyat bayrağında kaç halka vardır?",a:["3","4","5","6"],c:2},
{q:"Efes Antik Kenti hangi ilimizde yer alır?",a:["Aydın","İzmir","Muğla","Denizli"],c:1},
{q:"Hangisi bir Türk bilim insanıdır?",a:["Einstein","Aziz Sancar","Newton","Pasteur"],c:1},
{q:"Dünya'nın en büyük çölü hangisidir?",a:["Gobi","Sahra","Atacama","Kalahari"],c:1},
{q:"Hangisi klasik müzik bestecisidir?",a:["Beatles","Beethoven","Elvis","Madonna"],c:1},
{q:"Sümerlerin icadı olan yazı türü hangisidir?",a:["Hiyeroglif","Çivi yazısı","Latin","Arap"],c:1},
{q:"Hangi sanatçı 'Yıldızlı Gece' tablosunu yapmıştır?",a:["Picasso","Monet","Van Gogh","Da Vinci"],c:2},
{q:"Türkiye'nin en eski şehirlerinden biri hangisidir?",a:["Ankara","İstanbul","Çatalhöyük","İzmir"],c:2},
{q:"Hangisi bir Türk filmidir?",a:["Titanik","Babam ve Oğlum","Harry Potter","Avatar"],c:1},
{q:"Uzay'a giden ilk insan kimdir?",a:["Armstrong","Gagarin","Aldrin","Glenn"],c:1},
{q:"Hangisi bir dünya klasiği romandır?",a:["Çalıkuşu","Don Kişot","Sinekli Bakkal","Yaprak Dökümü"],c:1},
{q:"Wimbledon hangi sporun turnuvasıdır?",a:["Golf","Futbol","Tenis","Kriket"],c:2},
{q:"Hangisi antik uygarlıklardan biridir?",a:["Osmanlı","Roma","Selçuklu","Safevi"],c:1},
{q:"Topkapı Sarayı hangi şehirdedir?",a:["Ankara","Edirne","İstanbul","Bursa"],c:2},
{q:"Hangisi bir müzik notası değildir?",a:["Sol","La","Pa","Si"],c:2},
{q:"Shakespeare hangi ülkedendir?",a:["Fransa","İtalya","İngiltere","Almanya"],c:2},
{q:"Nuh'un Gemisi efsanesi hangi dağla ilişkilidir?",a:["Uludağ","Erciyes","Ağrı","Süphan"],c:2},
{q:"Hangisi bir dans türü değildir?",a:["Vals","Tango","Akrostiş","Samba"],c:2},
{q:"Frida Kahlo hangi sanat dalında ünlüdür?",a:["Müzik","Resim","Edebiyat","Heykel"],c:1},
{q:"Hangisi bir su altı sporu değildir?",a:["Dalış","Sörfing","Eskrim","Yüzme"],c:2},
{q:"Dünya'nın en yüksek binası hangi ülkededir?",a:["ABD","Çin","BAE","Malezya"],c:2},
{q:"Hangisi bir Türk tatlısıdır?",a:["Tiramisu","Baklava","Cheesecake","Brownie"],c:1},
{q:"Einstein hangi alanda Nobel almıştır?",a:["Kimya","Edebiyat","Fizik","Tıp"],c:2},
{q:"Hangisi bir kış olimpiyat sporudur?",a:["Yüzme","Buz pateni","Bisiklet","Atletizm"],c:1},
{q:"Türkiye'de en çok konuşulan ikinci dil hangisidir?",a:["Arapça","Kürtçe","İngilizce","Almanca"],c:1},
{q:"Hangisi bir tarihi yapıdır?",a:["AVM","Selimiye Camii","Stadyum","Havalimanı"],c:1},
{q:"Magellan neyle ünlüdür?",a:["Resim","Dünya turu","Müzik","Şiir"],c:1}
]
"""

_QUESTIONS_ORTAOKUL = r"""
easy:[
{q:"Türkiye'nin en kalabalık şehri hangisidir?",a:["Ankara","İzmir","İstanbul","Bursa"],c:2},
{q:"Hangisi bir element değildir?",a:["Oksijen","Su","Demir","Altın"],c:1},
{q:"DNA'nın açılımı nedir?",a:["Deoksiribo Nükleik Asit","Direk Nükleer Asit","Dünya Nükleer Ağı","Dernek Nükleer Araştırma"],c:0},
{q:"Fotosentez hangi organelde gerçekleşir?",a:["Mitokondri","Kloroplast","Ribozom","Golgi"],c:1},
{q:"Hangisi Newton'un yasalarından değildir?",a:["Eylemsizlik","F=m.a","Etki-Tepki","Kaldırma kuvveti"],c:3},
{q:"Suyun kaynama noktası kaç derecedir?",a:["90°C","95°C","100°C","110°C"],c:2},
{q:"Suyun donma noktası kaç derecedir?",a:["-10°C","-5°C","0°C","5°C"],c:2},
{q:"Hangisi asit değildir?",a:["Limon suyu","Sirke","Sabun","Mide sıvısı"],c:2},
{q:"Periyodik tabloda kaç element vardır?",a:["108","112","118","124"],c:2},
{q:"Altın'ın kimyasal sembolü nedir?",a:["Al","Ag","Au","At"],c:2},
{q:"Gümüş'ün kimyasal sembolü nedir?",a:["Gm","Au","Ag","Gu"],c:2},
{q:"Demir'in kimyasal sembolü nedir?",a:["De","Fe","Ir","Dr"],c:1},
{q:"Türkiye Cumhuriyeti kaç yılında kurulmuştur?",a:["1920","1921","1922","1923"],c:3},
{q:"İstanbul'un fethi kaç yılındadır?",a:["1071","1299","1453","1517"],c:2},
{q:"Malazgirt Savaşı kimin döneminde yapılmıştır?",a:["Fatih Sultan Mehmet","Alparslan","Kılıç Arslan","Osman Gazi"],c:1},
{q:"Osmanlı Devleti kaç yılında kurulmuştur?",a:["1071","1243","1299","1326"],c:2},
{q:"Atatürk'ün doğum yılı kaçtır?",a:["1878","1880","1881","1883"],c:2},
{q:"TBMM ne zaman açılmıştır?",a:["23 Nisan 1920","29 Ekim 1923","19 Mayıs 1919","30 Ağustos 1922"],c:0},
{q:"Hangisi Atatürk'ün ilkelerinden değildir?",a:["Cumhuriyetçilik","Milliyetçilik","Krallık","Laiklik"],c:2},
{q:"Dünya'nın Güneş etrafındaki dönüşü ne kadar sürer?",a:["24 saat","30 gün","365 gün","730 gün"],c:2},
{q:"Ay'ın Dünya etrafındaki dönüşü ne kadar sürer?",a:["7 gün","15 gün","29.5 gün","60 gün"],c:2},
{q:"Hangisi iç gezegen değildir?",a:["Merkür","Venüs","Dünya","Jüpiter"],c:3},
{q:"Güneş sistemimizdeki en büyük gezegen hangisidir?",a:["Satürn","Jüpiter","Uranüs","Neptün"],c:1},
{q:"Halkalı gezegen hangisidir?",a:["Mars","Venüs","Jüpiter","Satürn"],c:3},
{q:"'Üzüm üzüme baka baka kararır' ne demektir?",a:["Üzüm ye","İnsanlar çevresinden etkilenir","Üzüm topla","Bağa git"],c:1},
{q:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",a:["Yılan yakala","Güzel konuşma her kapıyı açar","Tatlı ye","Yılan besle"],c:1},
{q:"'Damlaya damlaya göl olur' ne demektir?",a:["Göl gez","Az az biriktirince çoğalır","Su iç","Yağmur yağar"],c:1},
{q:"'İşleyen demir pas tutmaz' ne demektir?",a:["Demir al","Çalışan sağlıklı kalır","Pas sil","Demir sat"],c:1},
{q:"'Bal tutan parmağını yalar' ne demektir?",a:["Bal ye","Fırsattan yararlanan kazanır","Parmak yala","Bal al"],c:1},
{q:"'Yuvarlanan taş yosun tutmaz' ne demektir?",a:["Taş at","Sürekli yer değiştiren tutunamaz","Yosun topla","Taş kır"],c:1},
{q:"'Sakla samanı gelir zamanı' ne demektir?",a:["Saman al","Her şeyin lazım olacağı gün gelir","Zamansız","Saman yak"],c:1},
{q:"'Armut piş ağzıma düş' ne demektir?",a:["Armut ye","Çalışmadan sonuç beklemek","Meyve al","Ağzını aç"],c:1},
{q:"'Minareyi çalan kılıfını hazırlar' ne demektir?",a:["Kılıf dik","Kötülük yapan önceden önlem alır","Minare yap","Çal"],c:1},
{q:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",a:["Ateş yak","Her söylentinin gerçeklik payı var","Duman çıkar","Yangın söndür"],c:1},
{q:"'Komşu komşunun külüne muhtaçtır' ne demektir?",a:["Kül al","İnsanlar birbirine muhtaçtır","Komşu ziyaret et","Kül at"],c:1},
{q:"'Acele işe şeytan karışır' ne demektir?",a:["Şeytan var","Aceleyle yapılan iş hatalı olur","Hızlı koş","Yavaş yürü"],c:1},
{q:"Fransa'nın başkenti neresidir?",a:["Londra","Berlin","Paris","Roma"],c:2},
{q:"İtalya'nın başkenti neresidir?",a:["Madrid","Roma","Atina","Lizbon"],c:1},
{q:"Almanya'nın başkenti neresidir?",a:["Viyana","Berlin","Münih","Hamburg"],c:1},
{q:"Japonya'nın başkenti neresidir?",a:["Pekin","Seul","Tokyo","Osaka"],c:2},
{q:"Mısır'ın başkenti neresidir?",a:["İskenderiye","Kahire","Bağdat","Tunus"],c:1},
{q:"Brezilya'nın başkenti neresidir?",a:["Rio de Janeiro","Sao Paulo","Brasilia","Salvador"],c:2},
{q:"Kanada'nın başkenti neresidir?",a:["Toronto","Vancouver","Ottawa","Montreal"],c:2},
{q:"Avustralya'nın başkenti neresidir?",a:["Sidney","Melbourne","Canberra","Brisbane"],c:2},
{q:"ABD'nin başkenti neresidir?",a:["New York","Los Angeles","Washington","Chicago"],c:2},
{q:"Hindistan'ın başkenti neresidir?",a:["Mumbai","Kalküta","Yeni Delhi","Goa"],c:2},
{q:"Güney Kore'nin başkenti neresidir?",a:["Tokyo","Pekin","Seul","Taipei"],c:2},
{q:"Dünya'nın en uzun nehri hangisidir?",a:["Amazon","Nil","Mississippi","Yangtze"],c:1},
{q:"Dünya'nın en büyük okyanusu hangisidir?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Kızılırmak hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Fırat Nehri nereye dökülür?",a:["Karadeniz","Akdeniz","Basra Körfezi","Hazar Denizi"],c:2},
{q:"Tuna Nehri hangi denize dökülür?",a:["Akdeniz","Karadeniz","Ege","Baltık"],c:1},
{q:"Ağrı Dağı'nın yüksekliği yaklaşık kaç metredir?",a:["3000","4000","5137","6000"],c:2},
{q:"Türkiye'nin en büyük gölü hangisidir?",a:["Tuz Gölü","Beyşehir","Van Gölü","Burdur"],c:2},
{q:"Dünya'da kaç kıta vardır?",a:["5","6","7","8"],c:2},
{q:"En büyük kıta hangisidir?",a:["Afrika","Avrupa","Asya","Kuzey Amerika"],c:2},
{q:"En küçük kıta hangisidir?",a:["Antarktika","Avustralya","Avrupa","Güney Amerika"],c:1},
{q:"Karadeniz ile Marmara'yı birleştiren boğaz hangisidir?",a:["Çanakkale","İstanbul","Cebelitarık","Hürmüz"],c:1},
{q:"Dünya'nın en yüksek dağı hangisidir?",a:["K2","Ağrı","Everest","Kilimanjaro"],c:2},
{q:"Himalaya Dağları hangi kıtadadır?",a:["Avrupa","Afrika","Asya","Amerika"],c:2},
{q:"And Dağları hangi kıtadadır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"İstanbul Boğazı hangi denizleri birleştirir?",a:["Ege-Marmara","Karadeniz-Marmara","Akdeniz-Ege","Karadeniz-Ege"],c:1},
{q:"Hangisi Türkiye'nin denize kıyısı olmayan bölgesidir?",a:["Akdeniz","Ege","İç Anadolu","Karadeniz"],c:2},
{q:"Voleybolda bir takımda sahada kaç kişi bulunur?",a:["5","6","7","11"],c:1},
{q:"Basketbolda bir sayı atışı en fazla kaç puan eder?",a:["1","2","3","4"],c:2},
{q:"Olimpiyat halkaları kaç tanedir?",a:["4","5","6","7"],c:1},
{q:"FIFA Dünya Kupası kaç yılda bir düzenlenir?",a:["2","3","4","5"],c:2},
{q:"İnsan vücudundaki en büyük organ hangisidir?",a:["Kalp","Karaciğer","Deri","Beyin"],c:2},
{q:"Hangisi vitamin değildir?",a:["A","B","K","P"],c:3},
{q:"İnsanda kaç çift kaburga kemiği vardır?",a:["10","12","14","16"],c:1},
{q:"Türkiye'de en çok yetişen tarım ürünü hangisidir?",a:["Muz","Buğday","Pirinç","Pamuk"],c:1},
{q:"Hangisi bir ada ülkesidir?",a:["Fransa","İsviçre","Küba","Portekiz"],c:2},
{q:"Sahra Çölü hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:2},
{q:"Türkiye kaç coğrafi bölgeye ayrılır?",a:["5","6","7","8"],c:2},
{q:"Hangisi bir yarımada değildir?",a:["İtalya","İskandinavya","Avustralya","Arabistan"],c:2},
{q:"İklim kuşaklarından hangisi sıcak kuşaktır?",a:["Kutup","Ilıman","Tropikal","Serin"],c:2},
{q:"Ekvator çizgisi neyi ayırır?",a:["Doğu-Batı","Kuzey-Güney yarımküre","Gece-Gündüz","Deniz-Kara"],c:1},
{q:"Greenwich meridyeni neyi belirler?",a:["Enlem başlangıcı","Boylam başlangıcı","Yükseklik","Derinlik"],c:1},
{q:"Rüzgar nasıl oluşur?",a:["Depremle","Yağmurla","Basınç farkıyla","Sıcaklıkla"],c:2},
{q:"Tsunami ne demektir?",a:["Deprem","Dev deniz dalgası","Kasırga","Hortum"],c:1},
{q:"Richter ölçeği neyi ölçer?",a:["Rüzgar hızı","Deprem şiddeti","Sıcaklık","Yağış"],c:1},
{q:"Fosil yakıt olmayan enerji kaynağı hangisidir?",a:["Kömür","Petrol","Rüzgar","Doğalgaz"],c:2},
{q:"Mozart hangi ülkelidir?",a:["Almanya","Avusturya","İtalya","Fransa"],c:1},
{q:"Beethoven hangi ülkelidir?",a:["Avusturya","Almanya","İtalya","Fransa"],c:1},
{q:"Hangisi bir Türk halk çalgısıdır?",a:["Piyano","Bağlama","Gitar","Keman"],c:1},
{q:"Aşık Veysel hangi sanat dalında ünlüdür?",a:["Resim","Müzik","Heykel","Mimari"],c:1},
{q:"Nasrettin Hoca nerelidir?",a:["Konya","Eskişehir","Akşehir","Karaman"],c:2},
{q:"İspanya'nın başkenti neresidir?",a:["Barselona","Madrid","Lizbon","Sevilla"],c:1},
{q:"Portekiz'in başkenti neresidir?",a:["Madrid","Lizbon","Porto","Sevilla"],c:1},
{q:"Norveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Kopenhag","Oslo"],c:3},
{q:"İsveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Oslo","Kopenhag"],c:0},
{q:"Danimarka'nın başkenti neresidir?",a:["Oslo","Helsinki","Stockholm","Kopenhag"],c:3},
{q:"Finlandiya'nın başkenti neresidir?",a:["Oslo","Stockholm","Helsinki","Kopenhag"],c:2},
{q:"İsviçre'nin başkenti neresidir?",a:["Zürih","Cenevre","Bern","Basel"],c:2},
{q:"Avusturya'nın başkenti neresidir?",a:["Münih","Viyana","Prag","Budapeşte"],c:1},
{q:"Polonya'nın başkenti neresidir?",a:["Prag","Varşova","Budapeşte","Bükreş"],c:1},
{q:"Çekya'nın başkenti neresidir?",a:["Bratislava","Varşova","Budapeşte","Prag"],c:3},
{q:"Romanya'nın başkenti neresidir?",a:["Budapeşte","Sofya","Bükreş","Belgrad"],c:2},
{q:"Bulgaristan'ın başkenti neresidir?",a:["Bükreş","Belgrad","Sofya","Atina"],c:2},
{q:"Yunanistan'ın başkenti neresidir?",a:["İstanbul","Selanik","Atina","Girit"],c:2},
{q:"İran'ın başkenti neresidir?",a:["Bağdat","Tahran","Şam","Kabil"],c:1},
{q:"Irak'ın başkenti neresidir?",a:["Tahran","Şam","Bağdat","Amman"],c:2},
{q:"Meksika'nın başkenti neresidir?",a:["Havana","Meksiko","Lima","Bogota"],c:1},
{q:"Arjantin'in başkenti neresidir?",a:["Santiago","Lima","Buenos Aires","Montevideo"],c:2},
{q:"Kolombiya'nın başkenti neresidir?",a:["Lima","Bogota","Quito","Santiago"],c:1},
{q:"Şili'nin başkenti neresidir?",a:["Buenos Aires","Lima","Montevideo","Santiago"],c:3},
{q:"Hangisi bir baklagil değildir?",a:["Nohut","Mercimek","Buğday","Fasulye"],c:2},
{q:"Dünyanın en soğuk kıtası hangisidir?",a:["Avrupa","Asya","Arktik","Antarktika"],c:3},
{q:"Türkiye'nin en batısındaki il hangisidir?",a:["İzmir","Çanakkale","Edirne","Muğla"],c:2},
{q:"Türkiye'nin en kuzeyindeki il hangisidir?",a:["Trabzon","Sinop","Artvin","Rize"],c:1},
{q:"Ekvator'dan geçen kıta sayısı kaçtır?",a:["2","3","4","5"],c:1},
{q:"Kutup yıldızı hangi yönü gösterir?",a:["Güney","Doğu","Batı","Kuzey"],c:3},
{q:"Hangisi Dünya'nın en büyük ülkesidir?",a:["Çin","ABD","Kanada","Rusya"],c:3},
{q:"Kuzey yarımkürede en uzun gündüz hangi tarihtedir?",a:["21 Mart","21 Haziran","23 Eylül","21 Aralık"],c:1},
{q:"Hangisi bir Rönesans dönemi sanatçısıdır?",a:["Picasso","Michelangelo","Monet","Van Gogh"],c:1},
{q:"Olimpiyat Oyunları ilk olarak hangi ülkede düzenlendi?",a:["Roma","Mısır","Yunanistan","İran"],c:2},
{q:"Hangisi bir Türk destanıdır?",a:["İlyada","Oğuz Kağan","Odysseia","Beowulf"],c:1},
{q:"Futbolda dünya kupasını en çok kazanan ülke hangisidir?",a:["Almanya","Arjantin","İtalya","Brezilya"],c:3},
{q:"Hangisi Nobel ödülü alan Türk yazardır?",a:["Yaşar Kemal","Orhan Pamuk","Nazım Hikmet","Ahmet Hamdi Tanpınar"],c:1},
{q:"Türkiye hangi kıtada yer alır?",a:["Sadece Avrupa","Sadece Asya","Avrupa ve Asya","Afrika"],c:2},
{q:"İstiklal Marşı hangi yıl kabul edilmiştir?",a:["1920","1921","1923","1924"],c:1},
{q:"Hangisi bir klasik müzik bestecisidir?",a:["Beatles","Tarkan","Bach","Sezen Aksu"],c:2},
{q:"Hangisi bir takımyıldızıdır?",a:["Mars","Venüs","Büyük Ayı","Jüpiter"],c:2},
{q:"Hangisi bir kış sporudur?",a:["Tenis","Yüzme","Biatlon","Basketbol"],c:2},
{q:"Hangisi UNESCO Dünya Mirası listesinde yer alır?",a:["Ankara Kalesi","Kapadokya","Taksim","Kızılay"],c:1}
],
medium:[
{q:"'Dost kara günde belli olur' ne demektir?",a:["Kara gün gelir","Gerçek dost zor zamanda yanında olur","Gün gelir","Dost bul"],c:1},
{q:"'Gülme komşuna gelir başına' ne demektir?",a:["Gülme","Başkasının başına gelen senin de başına gelebilir","Komşuya git","Gül topla"],c:1},
{q:"'Lafla peynir gemisi yürümez' ne demektir?",a:["Peynir al","Sadece konuşmakla iş olmaz, eylem gerek","Gemi sür","Laf etme"],c:1},
{q:"'Ayağını yorganına göre uzat' ne demektir?",a:["Uyu","Gelirine göre harca","Yorgan al","Uzat"],c:1},
{q:"'Sütten ağzı yanan yoğurdu üfleyerek yer' ne demektir?",a:["Yoğurt ye","Kötü deneyim yaşayan aşırı tedbirli olur","Süt iç","Üfle"],c:1},
{q:"'Bıçak kemiğe dayandı' ne demektir?",a:["Bıçak kes","Tahammülün sonuna gelindi","Kemik kır","Keskin ol"],c:1},
{q:"'Deveye hendek atlatmak' ne demektir?",a:["Deve bin","Zor bir işi yaptırmaya çalışmak","Hendek kaz","Deve sat"],c:1},
{q:"'Yerin kulağı vardır' ne demektir?",a:["Yer dinler","Her yerde seni duyabilirler","Kulak ver","Yere bak"],c:1},
{q:"'Gönül ne kahve ister ne kahvehane' ne demektir?",a:["Kahve iç","Önemli olan dostluk ve samimiyettir","Kahvehane aç","Gönül al"],c:1},
{q:"'Kırk yıllık Kani olur mu Yani' ne demektir?",a:["İsim değiş","Eski alışkanlıklar kolay değişmez","Kırk yıl bekle","Yani de"],c:1},
{q:"Amazon Nehri hangi kıtadadır?",a:["Afrika","Avrupa","Güney Amerika","Asya"],c:2},
{q:"Mississippi Nehri hangi ülkededir?",a:["Kanada","Brezilya","ABD","Meksika"],c:2},
{q:"Volga Nehri hangi ülkededir?",a:["Almanya","Polonya","Ukrayna","Rusya"],c:3},
{q:"Ganj Nehri hangi ülkededir?",a:["Çin","Pakistan","Hindistan","Bangladesh"],c:2},
{q:"Yangtze Nehri hangi ülkededir?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"Dicle Nehri hangi ülkelerden geçer?",a:["Türkiye-İran","Türkiye-Irak","Türkiye-Suriye","İran-Irak"],c:1},
{q:"Sakarya Nehri hangi denize dökülür?",a:["Ege","Akdeniz","Karadeniz","Marmara"],c:2},
{q:"Gediz Nehri hangi denize dökülür?",a:["Karadeniz","Marmara","Ege","Akdeniz"],c:2},
{q:"Büyük Menderes hangi denize dökülür?",a:["Karadeniz","Marmara","Ege","Akdeniz"],c:2},
{q:"Seyhan Nehri hangi şehirden geçer?",a:["Mersin","Antalya","Adana","Hatay"],c:2},
{q:"Kilimanjaro Dağı hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Alp Dağları hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:1},
{q:"Uludağ hangi şehirdedir?",a:["İstanbul","Ankara","Bursa","Antalya"],c:2},
{q:"Erciyes Dağı hangi şehirdedir?",a:["Kayseri","Konya","Sivas","Erzurum"],c:0},
{q:"Kaçkar Dağları hangi bölgededir?",a:["İç Anadolu","Doğu Anadolu","Karadeniz","Akdeniz"],c:2},
{q:"Toros Dağları hangi bölgededir?",a:["Karadeniz","Akdeniz","İç Anadolu","Ege"],c:1},
{q:"Baykal Gölü hangi ülkededir?",a:["Çin","Moğolistan","Rusya","Kazakistan"],c:2},
{q:"Hazar Denizi aslında nedir?",a:["Deniz","Okyanus","Göl","Kanal"],c:2},
{q:"Tuz Gölü hangi bölgededir?",a:["Marmara","İç Anadolu","Ege","Akdeniz"],c:1},
{q:"Panama Kanalı hangi okyanusları birleştirir?",a:["Atlas-Hint","Pasifik-Atlas","Hint-Pasifik","Atlas-Arktik"],c:1},
{q:"Süveyş Kanalı hangi ülkededir?",a:["Türkiye","Irak","İsrail","Mısır"],c:3},
{q:"Mariana Çukuru hangi okyanustadır?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Pangea ne demektir?",a:["İlk deniz","Tüm kıtaların birleşik hali","İlk atmosfer","İlk göl"],c:1},
{q:"Ural Dağları hangi kıtaları ayırır?",a:["Avrupa-Afrika","Avrupa-Asya","Asya-Amerika","Asya-Afrika"],c:1},
{q:"Ukrayna'nın başkenti neresidir?",a:["Moskova","Minsk","Kiev","Varşova"],c:2},
{q:"Hırvatistan'ın başkenti neresidir?",a:["Belgrad","Ljubljana","Zagreb","Saraybosna"],c:2},
{q:"Sırbistan'ın başkenti neresidir?",a:["Sofya","Bükreş","Zagreb","Belgrad"],c:3},
{q:"Bosna Hersek'in başkenti neresidir?",a:["Zagreb","Belgrad","Saraybosna","Podgorica"],c:2},
{q:"Çanakkale Savaşı kaç yılında yapılmıştır?",a:["1912","1914","1915","1918"],c:2},
{q:"Kurtuluş Savaşı kaç yılları arasında yapılmıştır?",a:["1914-1918","1919-1922","1923-1930","1939-1945"],c:1},
{q:"Sakarya Meydan Muharebesi hangi yılda yapılmıştır?",a:["1919","1920","1921","1922"],c:2},
{q:"Büyük Taarruz hangi yılda başlamıştır?",a:["1920","1921","1922","1923"],c:2},
{q:"Lozan Antlaşması hangi yılda imzalanmıştır?",a:["1920","1921","1922","1923"],c:3},
{q:"Osmanlı Devleti'ni kuran kişi kimdir?",a:["Fatih","Yavuz","Osman Bey","Ertuğrul"],c:2},
{q:"Kanuni Sultan Süleyman kaçıncı padişahtır?",a:["7.","8.","9.","10."],c:3},
{q:"Lale Devri hangi padişah dönemindedir?",a:["III. Ahmed","III. Selim","II. Mahmud","I. Abdülhamid"],c:0},
{q:"Tanzimat Fermanı kaç yılında ilan edilmiştir?",a:["1808","1839","1876","1908"],c:1},
{q:"Meşrutiyet ne demektir?",a:["Padişahlık","Anayasal yönetim","Cumhuriyet","Diktatörlük"],c:1},
{q:"Hücrenin enerji santralı hangi organeldir?",a:["Çekirdek","Ribozom","Mitokondri","Golgi"],c:2},
{q:"Hücrenin yönetim merkezi neresidir?",a:["Mitokondri","Ribozom","Çekirdek","Lizozom"],c:2},
{q:"Hangisi bir bileşik değildir?",a:["Su","Tuz","Oksijen","Şeker"],c:2},
{q:"pH 7 ne ifade eder?",a:["Asit","Baz","Nötr","Alkali"],c:2},
{q:"Hangisi bir asittir?",a:["Sabun","Limon suyu","Çamaşır suyu","Süt"],c:1},
{q:"Ses hangi ortamda en hızlı yayılır?",a:["Hava","Su","Boşluk","Katı"],c:3},
{q:"Işık hızı saniyede yaklaşık kaç km'dir?",a:["100.000","200.000","300.000","400.000"],c:2},
{q:"Mona Lisa tablosunu kim yapmıştır?",a:["Michelangelo","Raphael","Leonardo da Vinci","Botticelli"],c:2},
{q:"Van Gogh'un en ünlü tablosu hangisidir?",a:["Mona Lisa","Yıldızlı Gece","Guernica","Çığlık"],c:1},
{q:"Piramitler hangi uygarlığa aittir?",a:["Roma","Yunan","Mısır","Hitit"],c:2},
{q:"Petra Antik Kenti hangi ülkededir?",a:["Mısır","Irak","Ürdün","Suriye"],c:2},
{q:"Çin Seddi kaç yıldan fazladır?",a:["500","1000","2000","3000"],c:2},
{q:"Efes Antik Kenti hangi şehirdedir?",a:["Aydın","Muğla","İzmir","Manisa"],c:2},
{q:"Pamukkale hangi şehirdedir?",a:["Muğla","Aydın","Denizli","Burdur"],c:2},
{q:"Kapadokya hangi bölgededir?",a:["Akdeniz","İç Anadolu","Ege","Karadeniz"],c:1},
{q:"Göbeklitepe hangi şehirdedir?",a:["Diyarbakır","Mardin","Şanlıurfa","Gaziantep"],c:2},
{q:"Nemrut Dağı hangi ildedir?",a:["Ağrı","Adıyaman","Kars","Van"],c:1},
{q:"Aspendos hangi şehirdedir?",a:["İzmir","Muğla","Antalya","Mersin"],c:2},
{q:"Sümela Manastırı hangi şehirdedir?",a:["Artvin","Rize","Trabzon","Giresun"],c:2},
{q:"İstiklal Marşı'nı kim yazmıştır?",a:["Atatürk","Mehmet Akif Ersoy","Namık Kemal","Tevfik Fikret"],c:1},
{q:"İstiklal Marşı kaç yılında kabul edilmiştir?",a:["1920","1921","1922","1923"],c:1},
{q:"Hangisi Cumhuriyetin ilanından sonra yapılan inkılaplardan değildir?",a:["Harf devrimi","Şapka devrimi","Tanzimat","Soyadı kanunu"],c:2},
{q:"Harf devrimi kaç yılında yapılmıştır?",a:["1923","1925","1928","1930"],c:2},
{q:"Kadınlara seçme ve seçilme hakkı kaç yılında verilmiştir?",a:["1923","1928","1930","1934"],c:3},
{q:"Hangisi yenilenebilir enerji kaynağı değildir?",a:["Güneş","Rüzgar","Doğalgaz","Jeotermal"],c:2},
{q:"Ozon tabakası neyi engeller?",a:["Yağmuru","Rüzgarı","Zararlı UV ışınlarını","Sıcaklığı"],c:2},
{q:"Sera etkisine en çok neden olan gaz hangisidir?",a:["Oksijen","Azot","Karbondioksit","Helyum"],c:2},
{q:"Deprem dalgalarını ölçen alete ne denir?",a:["Barometre","Sismograf","Termometre","Higrometre"],c:1},
{q:"Naim Süleymanoğlu hangi spor dalında başarılıdır?",a:["Güreş","Halter","Boks","Atletizm"],c:1},
{q:"Türkiye'nin en çok madalya aldığı olimpiyat sporu hangisidir?",a:["Futbol","Güreş","Halter","Basketbol"],c:1},
{q:"1896'da ilk modern olimpiyatlar nerede yapılmıştır?",a:["Paris","Londra","Atina","Roma"],c:2},
{q:"UEFA Şampiyonlar Ligi kupasının resmi adı nedir?",a:["FIFA Trophy","Big Ear","UEFA Cup","Champions Cup"],c:1},
{q:"Piri Reis neyle ünlüdür?",a:["Şiir","Dünya haritası","Mimari","Müzik"],c:1},
{q:"Mimar Sinan'ın ustalık eseri hangisidir?",a:["Süleymaniye","Selimiye","Sultanahmet","Şehzade"],c:1},
{q:"Evliya Çelebi neyle tanınır?",a:["Savaş","Seyahatname","Mimari","Tıp"],c:1},
{q:"Katip Çelebi neyle tanınır?",a:["Coğrafya ve bibliyografya","Şiir","Mimari","Müzik"],c:0},
{q:"İbn-i Sina hangi alanda öncüdür?",a:["Matematik","Mimari","Tıp","Astronomi"],c:2},
{q:"Harezmi hangi alanda öncüdür?",a:["Tıp","Cebir/Matematik","Mimari","Coğrafya"],c:1},
{q:"Biruni hangi alanlarla ilgilenmiştir?",a:["Şiir","Astronomi ve matematik","Mimari","Müzik"],c:1},
{q:"'Ağır ol batman gelsin' ne demektir?",a:["Kilo al","Ağırbaşlı davran","Batman'a git","Ağırlık koy"],c:1},
{q:"'El elden üstündür' ne demektir?",a:["Elini yıka","Her zaman daha iyisi vardır","El sık","Eller güzel"],c:1},
{q:"'Mart kapıdan baktırır kazma kürek yaktırır' ne demektir?",a:["Mart'ta bahçe yap","Mart havası çok değişken","Kapıyı aç","Kazma al"],c:1},
{q:"'Görünüşe aldanma' ne demektir?",a:["Güzel giy","Dış görünüş yanıltıcı olabilir","Aynaya bak","Süslen"],c:1},
{q:"'Anlayana sivrisinek saz anlamayana davul zurna az' ne demektir?",a:["Müzik çal","Anlayan az sözle kavrar","Sivrisinek yakala","Davul çal"],c:1},
{q:"Aras Nehri hangi bölgeden geçer?",a:["Marmara","Ege","Doğu Anadolu","Akdeniz"],c:2},
{q:"Meriç Nehri hangi bölgededir?",a:["Karadeniz","Marmara","Ege","İç Anadolu"],c:1},
{q:"Coruh Nehri hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Yeşilırmak hangi denize dökülür?",a:["Akdeniz","Ege","Marmara","Karadeniz"],c:3},
{q:"Nemrut Krater Gölü hangi ildedir?",a:["Adıyaman","Bitlis","Van","Muş"],c:1},
{q:"Abant Gölü hangi ildedir?",a:["Düzce","Bolu","Ankara","Eskişehir"],c:1},
{q:"Eğirdir Gölü hangi ildedir?",a:["Burdur","Antalya","Konya","Isparta"],c:3},
{q:"Sapanca Gölü hangi bölgededir?",a:["İç Anadolu","Ege","Marmara","Karadeniz"],c:2},
{q:"Burdur Gölü neden önemlidir?",a:["En büyük göl","Tuzlu göl","Kuş cenneti","Ada göl"],c:2},
{q:"Tortum Gölü hangi ildedir?",a:["Artvin","Erzurum","Kars","Trabzon"],c:1},
{q:"Çıldır Gölü hangi ildedir?",a:["Erzurum","Ağrı","Kars","Van"],c:2},
{q:"Süphan Dağı hangi ildedir?",a:["Ağrı","Van","Bitlis","Muş"],c:2},
{q:"İlgaz Dağı hangi iller arasındadır?",a:["Ankara-Çankırı","Çankırı-Kastamonu","Bolu-Düzce","Sinop-Samsun"],c:1},
{q:"Bolkar Dağları hangi bölgededir?",a:["Doğu Anadolu","İç Anadolu","Akdeniz","Karadeniz"],c:2},
{q:"Munzur Dağları hangi ildedir?",a:["Erzurum","Erzincan","Tunceli","Bingöl"],c:2},
{q:"Dünya'nın en kalabalık ülkesi hangisidir?",a:["ABD","Çin","Hindistan","Endonezya"],c:2},
{q:"Dünya'nın en geniş yüzölçümüne sahip ülke hangisidir?",a:["ABD","Çin","Kanada","Rusya"],c:3},
{q:"Dünya'nın en küçük ülkesi hangisidir?",a:["Monako","Vatikan","San Marino","Lihtenştayn"],c:1},
{q:"Euro hangi bölgenin para birimidir?",a:["Asya","Amerika","Avrupa Birliği","Afrika"],c:2},
{q:"BM Güvenlik Konseyi'nin daimi üye sayısı kaçtır?",a:["3","4","5","7"],c:2},
{q:"Kızılay ne zaman kurulmuştur?",a:["1868","1877","1919","1923"],c:0},
{q:"Kızılhaç nerede kurulmuştur?",a:["Paris","Londra","Cenevre","Viyana"],c:2},
{q:"Hangisi bir bulaşıcı hastalık değildir?",a:["Grip","Kızamık","Şeker hastalığı","Verem"],c:2},
{q:"Hangi vitamin kemik sağlığı için gereklidir?",a:["A","B","C","D"],c:3},
{q:"'Tatlı sözle yılanı deliğinden çıkarırlar' atasözünde ne anlatılır?",a:["Yılan bakımı","Güzel konuşmanın gücü","Yılan avı","Tatlı yemek"],c:1},
{q:"'Bugünün işini yarına bırakma' ne demektir?",a:["Yarın tatil","İşini zamanında yap","Bugün dinlen","Yarın çalış"],c:1},
{q:"Mona Lisa tablosu hangi müzededir?",a:["British Museum","Uffizi","Louvre","Prado"],c:2},
{q:"Hangisi bir Osmanlı sadrazamıdır?",a:["Kanuni","Sokullu Mehmet Paşa","İbni Sina","Yavuz"],c:1},
{q:"Hangisi olimpiyat dalı değildir?",a:["Okçuluk","Kriket","Halter","Eskrim"],c:1},
{q:"Charlie Chaplin hangi sanat dalında ünlüdür?",a:["Resim","Müzik","Sinema","Edebiyat"],c:2},
{q:"Anadolu Medeniyetleri Müzesi hangi şehirdedir?",a:["İstanbul","Ankara","İzmir","Antalya"],c:1},
{q:"Hangisi bir spor terimdir?",a:["Sone","Ofsayt","Gazel","Rönesans"],c:1},
{q:"Türkiye'nin ilk kadın milletvekilleri hangi yıl seçildi?",a:["1930","1934","1938","1946"],c:1}
],
hard:[
{q:"'Sürüden ayrılanı kurt kapar' ne demektir?",a:["Kurt yakala","Topluluktan ayrılan tehlikeye düşer","Sürüye katıl","Kurt besle"],c:1},
{q:"'Mum dibine ışık vermez' ne demektir?",a:["Mum yak","Kişi en yakınlarına fayda sağlayamayabilir","Işık aç","Karanlık"],c:1},
{q:"'Hamama giren terler' ne demektir?",a:["Hamama git","Bir işe giren zorluklarına katlanır","Terle","Yıkan"],c:1},
{q:"'Ak akçe kara gün içindir' ne demektir?",a:["Para harca","Zor günler için biriktir","Akçe bul","Kara gün gelir"],c:1},
{q:"'Besle kargayı oysun gözünü' ne demektir?",a:["Karga besle","İyilik yaptığın kişi kötülük yapabilir","Göz kapat","Kargayı kov"],c:1},
{q:"'Kaz gelecek yerden tavuk esirgenmez' ne demektir?",a:["Kaz besle","Büyük kazanç için küçük harcama yapılır","Tavuk sat","Kaz ye"],c:1},
{q:"'Dervişin fikri neyse zikri de odur' ne demektir?",a:["Dua et","Kişi aklındakini söyler","Derviş ol","Fikir sor"],c:1},
{q:"'Körle yatan şaşı kalkar' ne demektir?",a:["Uyu","Kötü arkadaş kötü alışkanlık kazandırır","Şaşı ol","Gözlük tak"],c:1},
{q:"'Aşk olmayınca meşk olmaz' ne demektir?",a:["Aşık ol","Sevgi olmadan çalışma olmaz","Meşk et","Müzik çal"],c:1},
{q:"'Olmaz olmaz deme olmaz olmaz' ne demektir?",a:["Olmaz de","Hiçbir şeyi imkansız görme","Her şey olur","Olur de"],c:1},
{q:"'Bakarsan bağ olur bakmazsan dağ olur' ne demektir?",a:["Bağ dik","İlgilenirsen güzel, ilgilenmezsen bozulur","Dağa çık","Bağ al"],c:1},
{q:"'Davulun sesi uzaktan hoş gelir' ne demektir?",a:["Davul çal","Uzaktan güzel görünen yakından öyle olmayabilir","Uzak dur","Müzik dinle"],c:1},
{q:"'Her yiğidin bir yoğurt yiyişi vardır' ne demektir?",a:["Yoğurt ye","Herkesin kendine has yöntemi var","Yiğit ol","Yoğurt yap"],c:1},
{q:"'Boş çuval ayakta durmaz' ne demektir?",a:["Çuval doldur","Bilgisiz kişi başarısız olur","Çuval at","Ayakta dur"],c:1},
{q:"İndus Nehri hangi ülkelerden geçer?",a:["Hindistan-Bangladeş","Çin-Hindistan-Pakistan","Nepal-Hindistan","Çin-Moğolistan"],c:1},
{q:"Mekong Nehri hangi bölgeden geçer?",a:["Orta Doğu","Güneydoğu Asya","Kuzey Afrika","Güney Amerika"],c:1},
{q:"Ren Nehri hangi denize dökülür?",a:["Akdeniz","Baltık","Karadeniz","Kuzey Denizi"],c:3},
{q:"Nijer Nehri hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Kongo Nehri hangi okyanusa dökülür?",a:["Hint","Pasifik","Atlas","Arktik"],c:2},
{q:"Zambezi Nehri'ndeki ünlü şelale hangisidir?",a:["Niagara","Angel","Victoria","İguazu"],c:2},
{q:"Orinoko Nehri hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Avrupa"],c:2},
{q:"Murray Nehri hangi ülkededir?",a:["ABD","Kanada","Avustralya","Yeni Zelanda"],c:2},
{q:"Ob Nehri hangi ülkededir?",a:["Çin","Rusya","Kanada","ABD"],c:1},
{q:"Yenisey Nehri hangi ülkededir?",a:["Kanada","Rusya","Çin","Moğolistan"],c:1},
{q:"Lena Nehri hangi ülkededir?",a:["Kanada","Çin","Rusya","ABD"],c:2},
{q:"K2 Dağı hangi sıradağ sistemindedir?",a:["Alpler","Himalayalar","Karakurum","And"],c:2},
{q:"Aconcagua Dağı hangi ülkededir?",a:["Şili","Peru","Brezilya","Arjantin"],c:3},
{q:"Elbrus Dağı hangi ülkededir?",a:["Türkiye","Gürcistan","Rusya","İran"],c:2},
{q:"Mont Blanc hangi ülkeler arasındadır?",a:["İsviçre-Avusturya","Fransa-İtalya","İspanya-Fransa","İtalya-Avusturya"],c:1},
{q:"McKinley (Denali) Dağı hangi ülkededir?",a:["Kanada","ABD","Meksika","Rusya"],c:1},
{q:"Fuji Dağı hangi ülkededir?",a:["Çin","Kore","Japonya","Vietnam"],c:2},
{q:"Vezüv Yanardağı hangi ülkededir?",a:["Yunanistan","Türkiye","İtalya","İspanya"],c:2},
{q:"Etna Yanardağı hangi ülkededir?",a:["Yunanistan","Türkiye","İspanya","İtalya"],c:3},
{q:"Viktorya Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Titicaca Gölü hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Kuzey Amerika"],c:2},
{q:"Tanganyika Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Aral Gölü hangi kıtadadır?",a:["Avrupa","Asya","Afrika","Amerika"],c:1},
{q:"Çad Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Afrika","Avrupa"],c:2},
{q:"Büyük Set Resifi hangi ülkenin kıyısındadır?",a:["Brezilya","Hindistan","Avustralya","Meksika"],c:2},
{q:"Bering Boğazı hangi kıtaları ayırır?",a:["Avrupa-Afrika","Asya-Kuzey Amerika","Avrupa-Asya","Afrika-Asya"],c:1},
{q:"Cebelitarık Boğazı hangi kıtaları ayırır?",a:["Avrupa-Asya","Asya-Afrika","Avrupa-Afrika","Amerika-Avrupa"],c:2},
{q:"Hürmüz Boğazı hangi ülkeler arasındadır?",a:["Türkiye-Yunanistan","İran-Umman","Mısır-Suudi Arabistan","Yemen-Cibuti"],c:1},
{q:"Malakka Boğazı hangi ülkeler arasındadır?",a:["Japonya-Kore","Malezya-Endonezya","Çin-Vietnam","Filipinler-Tayvan"],c:1},
{q:"Küba'nın başkenti neresidir?",a:["Meksiko","Havana","Lima","Bogota"],c:1},
{q:"Türkiye'nin yüzölçümü yaklaşık kaç km²'dir?",a:["483.000","583.000","683.000","783.000"],c:3},
{q:"Dünya'nın en büyük çölü hangisidir?",a:["Gobi","Sahra","Atacama","Kalahari"],c:1},
{q:"Gobi Çölü hangi ülkelerdedir?",a:["İran-Irak","Çin-Moğolistan","Hindistan-Pakistan","Mısır-Libya"],c:1},
{q:"Atacama Çölü hangi ülkededir?",a:["Arjantin","Peru","Şili","Meksika"],c:2},
{q:"İklim değişikliğine en çok katkıda bulunan gaz hangisidir?",a:["Oksijen","Azot","Karbondioksit","Helyum"],c:2},
{q:"Tropikal yağmur ormanları en çok hangi kıtadadır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Orhan Pamuk Nobel Edebiyat Ödülü'nü hangi yıl aldı?",a:["2004","2005","2006","2008"],c:2},
{q:"Yaşar Kemal'in en ünlü eseri hangisidir?",a:["Tutunamayanlar","İnce Memed","Kürk Mantolu Madonna","Huzur"],c:1},
{q:"'Tutunamayanlar' kimin eseridir?",a:["Yaşar Kemal","Oğuz Atay","Orhan Pamuk","Ahmet Hamdi Tanpınar"],c:1},
{q:"Nazım Hikmet ne tür eserler yazmıştır?",a:["Roman","Şiir","Tiyatro","Deneme"],c:1},
{q:"Yunus Emre hangi yüzyılda yaşamıştır?",a:["11.","12.","13.","14."],c:2},
{q:"Mevlana hangi şehirle özdeşleşmiştir?",a:["İstanbul","Ankara","Konya","Bursa"],c:2},
{q:"Shakespeare hangi ülkelidir?",a:["Fransa","Almanya","İtalya","İngiltere"],c:3},
{q:"'Romeo ve Juliet' kimin eseridir?",a:["Dante","Goethe","Shakespeare","Hugo"],c:2},
{q:"Nikola Tesla hangi alanda çalışmıştır?",a:["Tıp","Elektrik/Alternatif akım","Kimya","Biyoloji"],c:1},
{q:"Thomas Edison neyi icat etmiştir?",a:["Telefon","Ampul","Radyo","Televizyon"],c:1},
{q:"Graham Bell neyi icat etmiştir?",a:["Ampul","Telgraf","Telefon","Radyo"],c:2},
{q:"Wright Kardeşler neyle tanınır?",a:["Otomobil","Tren","Uçak","Gemi"],c:2},
{q:"Usain Bolt hangi spor dalında ünlüdür?",a:["Yüzme","Atletizm","Boks","Tenis"],c:1},
{q:"Cristiano Ronaldo hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:2},
{q:"Lionel Messi hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:3},
{q:"2022 FIFA Dünya Kupası nerede yapılmıştır?",a:["Rusya","Brezilya","Katar","Güney Afrika"],c:2},
{q:"Türkiye'nin ilk kadın pilotu kimdir?",a:["Sabiha Gökçen","Halide Edip","Afet İnan","Latife Hanım"],c:0},
{q:"Aziz Sancar hangi alanda Nobel ödülü almıştır?",a:["Fizik","Kimya","Tıp","Barış"],c:1},
{q:"Marie Curie hangi alanda Nobel ödülü almıştır?",a:["Edebiyat","Fizik ve Kimya","Tıp","Barış"],c:1},
{q:"Albert Einstein'ın en ünlü formülü hangisidir?",a:["F=ma","E=mc²","PV=nRT","V=IR"],c:1},
{q:"Newton hangi meyvenin düşmesiyle yerçekimini keşfetmiştir?",a:["Armut","Portakal","Elma","Erik"],c:2},
{q:"Kopernik neyi savunmuştur?",a:["Dünya merkezli evren","Güneş merkezli evren","Sabit evren","Genişleyen evren"],c:1},
{q:"Galile hangi aletle gökyüzünü incelemiştir?",a:["Mikroskop","Teleskop","Dürbün","Pusula"],c:1},
{q:"'Gülü seven dikenine katlanır' ne demektir?",a:["Gül topla","Bir şeyi seven zorluğuna katlanır","Diken batır","Bahçe yap"],c:1},
{q:"'Hazıra dağlar dayanmaz' ne demektir?",a:["Dağa git","Harcanan ne kadar çok olursa olsun biter","Hazırla","Dağ aş"],c:1},
{q:"'Yuvayı dişi kuş yapar' ne demektir?",a:["Kuş besle","Evi kadın düzenler","Yuva yap","Kuş izle"],c:1},
{q:"'Su uyur düşman uyumaz' ne demektir?",a:["Su iç","Her zaman tetikte ol","Uyu","Düşmanı sev"],c:1},
{q:"'Ava giden avlanır' ne demektir?",a:["Ava git","Kötülük yapan kendisi zarar görür","Avlan","Tuzak kur"],c:1},
{q:"'Taşıma su ile değirmen dönmez' ne demektir?",a:["Su taşı","Dışarıdan destek alarak iş sürdürülmez","Değirmen yap","Su getir"],c:1},
{q:"Dalaman Çayı hangi denize dökülür?",a:["Karadeniz","Akdeniz","Ege","Marmara"],c:1},
{q:"Manavgat Çayı hangi şehirdedir?",a:["Mersin","Muğla","Antalya","İzmir"],c:2},
{q:"Ceyhan Nehri hangi bölgededir?",a:["Karadeniz","İç Anadolu","Akdeniz","Ege"],c:2},
{q:"Batı Anadolu akarsularının çoğu hangi denize dökülür?",a:["Karadeniz","Akdeniz","Ege","Marmara"],c:2},
{q:"Türkiye'nin en yağışlı yeri neresidir?",a:["Antalya","İstanbul","Rize","Trabzon"],c:2},
{q:"Fön rüzgarı ne tür bir rüzgardır?",a:["Soğuk-kuru","Sıcak-kuru","Soğuk-nemli","Sıcak-nemli"],c:1},
{q:"Poyraz rüzgarı hangi yönden eser?",a:["Güneybatı","Kuzeydoğu","Kuzeybatı","Güneydoğu"],c:1},
{q:"Lodos rüzgarı hangi yönden eser?",a:["Kuzeydoğu","Kuzeybatı","Güneybatı","Güneydoğu"],c:2},
{q:"Karstik arazi en çok hangi bölgemizde görülür?",a:["Karadeniz","Ege","Akdeniz","İç Anadolu"],c:2},
{q:"Türkiye'nin en uzun tüneli hangisidir?",a:["Bolu Tüneli","Ovit Tüneli","Ilgaz Tüneli","Zigana Tüneli"],c:1},
{q:"I. Dünya Savaşı kaç yılında başlamıştır?",a:["1912","1914","1916","1918"],c:1},
{q:"II. Dünya Savaşı kaç yılında sona ermiştir?",a:["1943","1944","1945","1946"],c:2},
{q:"Soğuk Savaş hangi ülkeler arasındaydı?",a:["ABD-Çin","ABD-SSCB","İngiltere-Fransa","Almanya-Rusya"],c:1},
{q:"Berlin Duvarı kaç yılında yıkılmıştır?",a:["1985","1987","1989","1991"],c:2},
{q:"SSCB kaç yılında dağılmıştır?",a:["1989","1990","1991","1993"],c:2},
{q:"Çanakkale Savaşı'nda hangi cephe açılmıştır?",a:["Kafkas","Kanal","Çanakkale","Irak"],c:2},
{q:"Mustafa Kemal ilk askeri başarısını nerede kazanmıştır?",a:["Çanakkale","Sakarya","Dumlupınar","Trablusgarp"],c:0},
{q:"Mudanya Ateşkes Antlaşması kaç yılında imzalanmıştır?",a:["1920","1921","1922","1923"],c:2},
{q:"Dünya nüfusu yaklaşık kaç milyardır?",a:["5","6","7","8"],c:3},
{q:"Okyanusların toplam yüzölçümü karaların kaç katıdır?",a:["1","2","3","4"],c:1},
{q:"Sıfır meridyeni hangi şehirden geçer?",a:["Paris","New York","Londra","Berlin"],c:2},
{q:"Galileo Galilei neyi keşfetmiştir?",a:["Amerika","Jüpiter uyduları","Penisilin","DNA"],c:1},
{q:"Hangisi bir Osmanlı minyatür sanatçısıdır?",a:["Matrakçı Nasuh","Da Vinci","Monet","Rembrandt"],c:0},
{q:"Dünya Kupası'nı en çok kazanan futbol takımı hangisidir?",a:["Almanya","İtalya","Brezilya","Arjantin"],c:2},
{q:"Hangisi bir opera bestecisidir?",a:["Bach","Verdi","Chopin","Liszt"],c:1},
{q:"Troya Antik Kenti hangi ilimizde yer alır?",a:["İzmir","Çanakkale","Balıkesir","Edirne"],c:1},
{q:"Formula 1'de en çok şampiyonluk kazanan pilot kimdir?",a:["Senna","Schumacher","Hamilton","Vettel"],c:2},
{q:"Hangisi bir Türk romanıdır?",a:["Savaş ve Barış","Suç ve Ceza","Çalıkuşu","Don Kişot"],c:2},
{q:"Kremlin hangi ülkededir?",a:["Çin","İngiltere","Rusya","Fransa"],c:2},
{q:"Hangisi bir dans yarışması formatıdır?",a:["Survivor","MasterChef","Dancing with Stars","The Voice"],c:2},
{q:"Uzayda yürüyen ilk kadın astronot kimdir?",a:["Sally Ride","Valentina Tereşkova","Svetlana Savitskaya","Mae Jemison"],c:2},
{q:"Hangisi bir Türk hat sanatçısıdır?",a:["Matisse","Hamid Aytaç","Renoir","Cézanne"],c:1},
{q:"Dünya'nın en uzun köprüsü hangi ülkededir?",a:["ABD","Japonya","Çin","İngiltere"],c:2},
{q:"Hangisi bir müzik festivalidir?",a:["Cannes","Sundance","Eurovision","Oscar"],c:2},
{q:"Pekin Operası hangi ülkenin sanatıdır?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"Hangisi bir kış olimpiyat sporu değildir?",a:["Kayaklı koşu","Curling","Badminton","Biatlon"],c:2},
{q:"Türkiye'nin ilk olimpiyat madalyası hangi spordandır?",a:["Halter","Güreş","Boks","Atletizm"],c:1},
{q:"Hangisi bir fotoğraf sanatçısıdır?",a:["Ansel Adams","Beethoven","Chopin","Shakespeare"],c:0},
{q:"Super Bowl hangi sporun final maçıdır?",a:["Basketbol","Beyzbol","Amerikan Futbolu","Buz Hokeyi"],c:2},
{q:"Hangisi bir Türk mimari eseridir?",a:["Taj Mahal","Selimiye Camii","Sagrada Familia","Notre Dame"],c:1},
{q:"Milli Mücadele döneminin ünlü kadın kahramanı kimdir?",a:["Halide Edip Adıvar","Sabiha Gökçen","Afet İnan","Latife Hanım"],c:0},
{q:"Hangisi bir Akdeniz yemeğidir?",a:["Sushi","Ramen","Hummus","Dim Sum"],c:2},
{q:"Emmy ödülü hangi alandadır?",a:["Sinema","Televizyon","Müzik","Edebiyat"],c:1},
{q:"Hangisi bir su sporu değildir?",a:["Yelken","Kano","Eskrim","Sörf"],c:2},
{q:"Osmanlı'da ilk matbaa ne zaman kuruldu?",a:["1629","1727","1839","1876"],c:1},
{q:"Hangisi bir müze değildir?",a:["Prado","Hermitage","Wimbledon","Uffizi"],c:2}
],
very_hard:[
{q:"'Abanoz böceği meşeyi yer' ne demektir?",a:["Böcek yakala","Küçük ama sürekli zarar büyük sonuç doğurur","Meşe kes","Böcek besle"],c:1},
{q:"'Dut yemiş bülbüle döndü' ne demektir?",a:["Dut ye","Sessizleşti, sustu","Bülbül dinle","Şarkı söyle"],c:1},
{q:"'Çoğu zarar azı karar' ne demektir?",a:["Az ye","Her şeyin fazlası zararlıdır","Çok al","Az harca"],c:1},
{q:"'Her kuşun eti yenmez' ne demektir?",a:["Kuş ye","Her kişiyle uğraşılmaz","Kuş yakala","Et ye"],c:1},
{q:"'İğneyi kendine çuvaldızı başkasına batır' ne demektir?",a:["İğne batır","Önce kendini eleştir sonra başkalarını","Dikiş dik","Çuvaldız al"],c:1},
{q:"'Et tırnaktan ayrılmaz' ne demektir?",a:["Et ye","Yakın akrabalar birbirinden kopmaz","Tırnak kes","Et kes"],c:1},
{q:"'İki cambaz bir ipte oynamaz' ne demektir?",a:["Cambaz ol","Aynı yerde iki lider olmaz","İp atla","Cambaz izle"],c:1},
{q:"'Denizden çıkmış balığa benzemek' ne demektir?",a:["Balık tut","Şaşkın ve çaresiz kalmak","Yüz","Denize git"],c:1},
{q:"'Karga kekliğe bakıp yürümeye kalkmış' ne demektir?",a:["Karga izle","Özenmek kendine zarar verir","Keklik yakala","Kuş seyret"],c:1},
{q:"'Aç ayı oynamaz' ne demektir?",a:["Ayı besle","Karşılığı olmadan çalışılmaz","Ayı izle","Oyun oyna"],c:1},
{q:"'Kendi düşen ağlamaz' ne demektir?",a:["Ağlama","Hatasının sonucuna kişi katlanır","Düşme","Koş"],c:1},
{q:"'Nerde hareket orda bereket' ne demektir?",a:["Hareket et","Çalışan bereketini bulur","Bereket getir","Dur"],c:1},
{q:"Suudi Arabistan'ın başkenti neresidir?",a:["Dubai","Mekke","Riyad","Medine"],c:2},
{q:"Mariana Çukuru yaklaşık kaç metre derindir?",a:["5000","8000","11000","15000"],c:2},
{q:"Dünya'nın en derin gölü hangisidir?",a:["Van Gölü","Hazar","Baykal","Viktorya"],c:2},
{q:"Dünya'nın en büyük adası hangisidir?",a:["Madagaskar","Borneo","Grönland","Sumatra"],c:2},
{q:"Niagara Şelalesi hangi ülkeler arasındadır?",a:["Brezilya-Arjantin","ABD-Kanada","Meksika-ABD","Zambiya-Zimbabve"],c:1},
{q:"Angel Şelalesi hangi ülkededir?",a:["Brezilya","Kolombiya","Venezuela","Peru"],c:2},
{q:"İguazu Şelalesi hangi ülkeler arasındadır?",a:["ABD-Kanada","Brezilya-Arjantin","Zambiya-Zimbabve","Peru-Ekvador"],c:1},
{q:"Dünya'nın en yüksek şelalesi hangisidir?",a:["Niagara","Victoria","Angel","İguazu"],c:2},
{q:"Gondwana neyi ifade eder?",a:["Eski kuzey süper kıtası","Eski güney süper kıtası","İlk okyanus","İlk atmosfer"],c:1},
{q:"Laurasia neyi ifade eder?",a:["Eski güney kıtası","Eski kuzey süper kıtası","İlk göl","İlk dağ"],c:1},
{q:"Rocky Dağları hangi kıtadadır?",a:["Güney Amerika","Avrupa","Asya","Kuzey Amerika"],c:3},
{q:"Appalachian Dağları hangi ülkededir?",a:["Kanada","Meksika","ABD","Brezilya"],c:2},
{q:"Atlas Dağları hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Takla Makan Çölü hangi ülkededir?",a:["Moğolistan","İran","Çin","Pakistan"],c:2},
{q:"Kalahari Çölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Okavango Deltası hangi ülkededir?",a:["Güney Afrika","Tanzanya","Botsvana","Kenya"],c:2},
{q:"Pasifik Okyanusu dünya yüzeyinin yüzde kaçını kaplar?",a:["15","22","30","46"],c:2},
{q:"Sargasso Denizi hangi okyanustadır?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Güney Buz Denizi hangi kıtanın çevresindedir?",a:["Arktik","Avustralya","Antarktika","Güney Amerika"],c:2},
{q:"Dünya'nın en uzun kıyı şeridine sahip ülke hangisidir?",a:["ABD","Avustralya","Kanada","Rusya"],c:2},
{q:"Amazon Yağmur Ormanları büyük bölümü hangi ülkededir?",a:["Kolombiya","Peru","Venezuela","Brezilya"],c:3},
{q:"Fatih Sultan Mehmet İstanbul'u fethettiğinde kaç yaşındaydı?",a:["18","21","25","30"],c:1},
{q:"İlk Türk devleti hangisidir?",a:["Osmanlı","Selçuklu","Göktürk","Büyük Hun"],c:3},
{q:"Göbeklitepe dünyanın en eski nesidir?",a:["Şehri","Tapınağı","Mezarlığı","Sarayı"],c:1},
{q:"Truva Savaşı hangi antik medeniyetler arasında olmuştur?",a:["Mısır-Hitit","Yunan-Truva","Roma-Kartaca","Pers-Yunan"],c:1},
{q:"Hammurabi Kanunları hangi uygarlığa aittir?",a:["Mısır","Babil","Hitit","Asur"],c:1},
{q:"Roma İmparatorluğu'nun batı yarısı kaç yılında yıkılmıştır?",a:["395","410","455","476"],c:3},
{q:"İpek Yolu hangi kıtaları bağlıyordu?",a:["Afrika-Avrupa","Asya-Avrupa","Amerika-Avrupa","Asya-Afrika"],c:1},
{q:"Baharat Yolu hangi bölgeler arasındaydı?",a:["Avrupa-Uzak Doğu","Amerika-Afrika","Avustralya-Asya","Afrika-Güney Amerika"],c:0},
{q:"Leonardo da Vinci hangi yüzyılda yaşamıştır?",a:["13-14.","14-15.","15-16.","16-17."],c:2},
{q:"Michelangelo'nun en ünlü heykeli hangisidir?",a:["Venüs","David","Zeus","Atlas"],c:1},
{q:"Picasso hangi sanat akımının kurucularındandır?",a:["İzlenimcilik","Kübizm","Sürrealizm","Romantizm"],c:1},
{q:"Salvador Dalí hangi sanat akımına aittir?",a:["Kübizm","İzlenimcilik","Sürrealizm","Pop Art"],c:2},
{q:"'Guernica' tablosu kimin eseridir?",a:["Dalí","Monet","Picasso","Van Gogh"],c:2},
{q:"Vivaldi hangi ülkelidir?",a:["Almanya","Avusturya","Fransa","İtalya"],c:3},
{q:"'Dört Mevsim' kimin eseridir?",a:["Mozart","Bach","Vivaldi","Beethoven"],c:2},
{q:"Çaykovski hangi ülkelidir?",a:["Polonya","Almanya","Avusturya","Rusya"],c:3},
{q:"'Kuğu Gölü' kimin eseridir?",a:["Mozart","Vivaldi","Çaykovski","Beethoven"],c:2},
{q:"Barış Manço hangi müzik türünde eserler vermiştir?",a:["Klasik","Anadolu Rock","Jazz","Opera"],c:1},
{q:"Zeki Müren hangi sanat dalında ünlüdür?",a:["Resim","Türk Sanat Müziği","Heykel","Mimari"],c:1},
{q:"Neşet Ertaş hangi müzik türünde eserler vermiştir?",a:["Pop","Halk Müziği","Sanat Müziği","Rock"],c:1},
{q:"Aşık Veysel neyle tanınır?",a:["Resim","Saz ve türkü","Roman","Tiyatro"],c:1},
{q:"Michael Phelps hangi spor dalında rekor kırmıştır?",a:["Atletizm","Boks","Yüzme","Tenis"],c:2},
{q:"NBA'de en çok sayı atan oyuncu kimdir?",a:["Michael Jordan","Kobe Bryant","LeBron James","Kareem Abdul-Jabbar"],c:2},
{q:"Serena Williams hangi spor dalında ünlüdür?",a:["Golf","Tenis","Yüzme","Atletizm"],c:1},
{q:"Roger Federer hangi ülkelidir?",a:["Avusturya","Almanya","İsveç","İsviçre"],c:3},
{q:"Galatasaray UEFA Kupası'nı hangi yıl kazanmıştır?",a:["1998","2000","2002","2004"],c:1},
{q:"Fenerbahçe hangi yıl kurulmuştur?",a:["1899","1903","1905","1907"],c:3},
{q:"Beşiktaş hangi yıl kurulmuştur?",a:["1899","1903","1905","1907"],c:1},
{q:"Galatasaray hangi yıl kurulmuştur?",a:["1899","1903","1905","1907"],c:3},
{q:"Charles Darwin hangi teoriyi ortaya koymuştur?",a:["Görelilik","Evrim","Atom","Hücre"],c:1},
{q:"Louis Pasteur hangi alanda çalışmıştır?",a:["Fizik","Matematik","Mikrobiyoloji","Astronomi"],c:2},
{q:"Mendel hangi alanda çalışmıştır?",a:["Fizik","Kimya","Astronomi","Genetik"],c:3},
{q:"Röntgen neyi keşfetmiştir?",a:["Radyo dalgaları","X ışınları","Gama ışınları","Ultraviyole"],c:1},
{q:"Fleming hangi ilacı keşfetmiştir?",a:["Aspirin","Penisilin","İnsülin","Morfin"],c:1},
{q:"Dünya'nın en kalabalık şehri hangisidir?",a:["Pekin","New York","Tokyo","İstanbul"],c:2},
{q:"Birleşmiş Milletler merkezi nerededir?",a:["Londra","Paris","New York","Cenevre"],c:2},
{q:"NATO merkezi nerededir?",a:["Washington","New York","Brüksel","Londra"],c:2},
{q:"Avrupa Birliği'nin merkezi nerededir?",a:["Paris","Berlin","Brüksel","Strasbourg"],c:2},
{q:"UNESCO merkezi nerededir?",a:["New York","Londra","Cenevre","Paris"],c:3},
{q:"Dünya'nın en kuru çölü hangisidir?",a:["Sahra","Gobi","Atacama","Kalahari"],c:2},
{q:"Dünya'nın en yağışlı yeri neresidir?",a:["Amazon","Cherrapunji","Kongo","Borneo"],c:1},
{q:"Türkiye'de en az yağış alan bölge hangisidir?",a:["Ege","İç Anadolu","Marmara","Doğu Anadolu"],c:1},
{q:"Hangi il Türkiye'nin en güneydoğusundadır?",a:["Van","Hakkari","Şırnak","Mardin"],c:2},
{q:"Datça Yarımadası hangi bölgededir?",a:["Marmara","Karadeniz","Ege","Akdeniz"],c:2},
{q:"Sinop Yarımadası hangi denize uzanır?",a:["Marmara","Ege","Akdeniz","Karadeniz"],c:3},
{q:"Edirne Selimiye Camii kimin eseridir?",a:["Fatih","Kanuni","Mimar Sinan","II. Selim"],c:2},
{q:"Ahlat Selçuklu Mezarlığı hangi ildedir?",a:["Van","Bitlis","Muş","Ağrı"],c:1},
{q:"Divriği Ulu Camii hangi ildedir?",a:["Erzurum","Sivas","Kayseri","Malatya"],c:1},
{q:"Topkapı Sarayı hangi padişah döneminde yapılmıştır?",a:["Fatih Sultan Mehmet","Kanuni","Yavuz","II. Bayezid"],c:0},
{q:"Dolmabahçe Sarayı hangi padişah döneminde yapılmıştır?",a:["Kanuni","III. Selim","Abdülmecid","II. Abdülhamid"],c:2},
{q:"Galata Kulesi hangi dönemden kalmıştır?",a:["Roma","Bizans","Ceneviz","Osmanlı"],c:2},
{q:"Kız Kulesi nerededir?",a:["Çanakkale Boğazı","İstanbul Boğazı","Haliç","Marmara"],c:1},
{q:"Ani Harabeleri hangi ildedir?",a:["Erzurum","Kars","Iğdır","Ağrı"],c:1},
{q:"Zeugma Mozaik Müzesi hangi ildedir?",a:["Şanlıurfa","Mardin","Diyarbakır","Gaziantep"],c:3},
{q:"Perge Antik Kenti hangi ildedir?",a:["İzmir","Muğla","Antalya","Mersin"],c:2},
{q:"Side Antik Kenti hangi ildedir?",a:["İzmir","Muğla","Antalya","Mersin"],c:2},
{q:"Myra Antik Kenti hangi ildedir?",a:["İzmir","Muğla","Antalya","Mersin"],c:2},
{q:"İshak Paşa Sarayı hangi ildedir?",a:["Kars","Ağrı","Van","Iğdır"],c:1},
{q:"Hasankeyf hangi ildedir?",a:["Mardin","Şırnak","Batman","Siirt"],c:2},
{q:"Safranbolu evleri hangi ildedir?",a:["Bolu","Kastamonu","Karabük","Çankırı"],c:2},
{q:"Beypazarı hangi ilin ilçesidir?",a:["Eskişehir","Bolu","Ankara","Çankırı"],c:2},
{q:"Altın Küre ödülü hangi alandadır?",a:["Edebiyat","Spor","Sinema ve TV","Müzik"],c:2},
{q:"Hangisi bir savaş sanatıdır?",a:["Origami","Aikido","Bonsai","İkebana"],c:1},
{q:"Dünya'nın en eski üniversitesi hangi ülkededir?",a:["İngiltere","İtalya","Fas","Mısır"],c:2},
{q:"Hangisi bir Türk halk hikayesidir?",a:["Romeo ve Juliet","Ferhat ile Şirin","Hamlet","Antigone"],c:1},
{q:"NBA'de en çok şampiyonluk kazanan takım hangisidir?",a:["Lakers","Celtics","Bulls","Warriors"],c:1},
{q:"Hangisi bir çağdaş sanat akımıdır?",a:["Gotik","Pop Art","Romanik","Barok"],c:1},
{q:"Efes Celsus Kütüphanesi kaç yılında inşa edildi?",a:["MS 100","MS 135","MS 200","MS 250"],c:1},
{q:"Hangisi bir yönetmen değildir?",a:["Kubrick","Hitchcock","Hemingway","Coppola"],c:2},
{q:"Maratona adını veren savaş hangi ülkede yapıldı?",a:["İtalya","Türkiye","Yunanistan","Mısır"],c:2},
{q:"Hangisi bir geleneksel Japon tiyatrosudur?",a:["Kabuki","Flamenco","Opera","Bale"],c:0},
{q:"Grammy ödülü hangi alandadır?",a:["Sinema","Edebiyat","Müzik","Tiyatro"],c:2},
{q:"Hangisi dünyaca ünlü bir Türk edebiyatçıdır?",a:["Tolstoy","Elif Şafak","Hugo","Dickens"],c:1},
{q:"Usain Bolt hangi mesafede dünya rekoru kırmıştır?",a:["200m","400m","100m","800m"],c:2},
{q:"Hangisi bir heykel türüdür?",a:["Fresk","Rölyef","Mozaik","Vitray"],c:1},
{q:"İpek Yolu nereden nereye uzanırdı?",a:["Roma-Mısır","Çin-Avrupa","Hindistan-Afrika","Japonya-Rusya"],c:1},
{q:"Hangisi bir Türk destanı değildir?",a:["Manas","Oğuz Kağan","İlyada","Ergenekon"],c:2},
{q:"Wimbledon turnuvası hangi yüzeyde oynanır?",a:["Toprak","Çim","Sert zemin","Halı"],c:1},
{q:"Hangisi bir bale yapıtıdır?",a:["Carmen","Kuğu Gölü","Boheme","Tosca"],c:1},
{q:"Cannes Film Festivali hangi ülkede düzenlenir?",a:["İtalya","İspanya","Fransa","Almanya"],c:2},
{q:"Hangisi Osmanlı döneminde yazılmış bir eserdir?",a:["İlyada","Leyla ile Mecnun","Don Kişot","Hamlet"],c:1},
{q:"Modern pentatlonda kaç disiplin vardır?",a:["3","4","5","6"],c:2},
{q:"Hangisi bir Türk sinema ödülüdür?",a:["Oscar","BAFTA","Altın Portakal","Cannes Palmiye"],c:2},
{q:"Rönesans hangi yüzyılda başlamıştır?",a:["12.","13.","14.","15."],c:2},
{q:"Hangisi bir buz dansı figürüdür?",a:["Libre","Twist","Twizzle","Rumba"],c:2},
{q:"Dünya'nın en çok ziyaret edilen müzesi hangisidir?",a:["British Museum","Met","Louvre","Hermitage"],c:2},
{q:"Hangisi bir Türk mimarıdır?",a:["Gaudi","Mimar Sinan","Le Corbusier","Frank Lloyd Wright"],c:1},
{q:"Hangisi paralimpik spor değildir?",a:["Tekerlekli sandalye basketbol","Goalball","Polo","Boccia"],c:2},
{q:"Aşık Veysel hangi sanat dalında ünlüdür?",a:["Resim","Müzik ve Şiir","Heykel","Sinema"],c:1},
{q:"Hangisi bir film türü değildir?",a:["Western","Film Noir","Sone","Thriller"],c:2},
{q:"Dünya Satranç Şampiyonası'nı en uzun süre elinde tutan kimdir?",a:["Fischer","Kasparov","Carlsen","Karpov"],c:1}
]
"""

_QUESTIONS_LISE = r"""
easy:[
{q:"Periyodik tablonun ilk elementi hangisidir?",a:["Helyum","Hidrojen","Lityum","Karbon"],c:1},
{q:"Newton'un ikinci hareket yasası nedir?",a:["F=ma","E=mc²","PV=nRT","V=IR"],c:0},
{q:"Osmanlı Devleti kaç yılında kurulmuştur?",a:["1071","1243","1299","1326"],c:2},
{q:"İstanbul'un fethi kaç yılındadır?",a:["1071","1389","1453","1517"],c:2},
{q:"Atatürk'ün doğduğu şehir neresidir?",a:["İstanbul","Ankara","Selanik","İzmir"],c:2},
{q:"DNA'nın yapısını kim keşfetmiştir?",a:["Mendel","Darwin","Watson ve Crick","Pasteur"],c:2},
{q:"Hangisi Nobel ödülü kategorisi değildir?",a:["Fizik","Kimya","Matematik","Edebiyat"],c:2},
{q:"Fotosentezde üretilen gaz hangisidir?",a:["Karbondioksit","Azot","Oksijen","Helyum"],c:2},
{q:"Hücrenin enerji santralı hangisidir?",a:["Çekirdek","Ribozom","Mitokondri","Golgi"],c:2},
{q:"Hangisi bir asit değildir?",a:["HCl","H2SO4","NaOH","HNO3"],c:2},
{q:"pH 1 ne ifade eder?",a:["Güçlü baz","Nötr","Güçlü asit","Zayıf baz"],c:2},
{q:"Avogadro sayısı yaklaşık kaçtır?",a:["3.14x10^8","6.02x10^23","6.67x10^-11","9.8"],c:1},
{q:"Işık hızı yaklaşık kaç m/s'dir?",a:["3x10^6","3x10^8","3x10^10","3x10^12"],c:1},
{q:"Türkiye Cumhuriyeti'nin kurucusu kimdir?",a:["İsmet İnönü","Mustafa Kemal Atatürk","Fevzi Çakmak","Kazım Karabekir"],c:1},
{q:"Fransa'nın başkenti neresidir?",a:["Londra","Berlin","Paris","Roma"],c:2},
{q:"Almanya'nın başkenti neresidir?",a:["Viyana","Berlin","Münih","Hamburg"],c:1},
{q:"Japonya'nın başkenti neresidir?",a:["Pekin","Seul","Tokyo","Osaka"],c:2},
{q:"Brezilya'nın başkenti neresidir?",a:["Rio","Sao Paulo","Brasilia","Salvador"],c:2},
{q:"Avustralya'nın başkenti neresidir?",a:["Sidney","Melbourne","Canberra","Brisbane"],c:2},
{q:"Kanada'nın başkenti neresidir?",a:["Toronto","Vancouver","Ottawa","Montreal"],c:2},
{q:"Hindistan'ın başkenti neresidir?",a:["Mumbai","Kalküta","Yeni Delhi","Goa"],c:2},
{q:"Mısır'ın başkenti neresidir?",a:["İskenderiye","Kahire","Bağdat","Tunus"],c:1},
{q:"Güney Kore'nin başkenti neresidir?",a:["Tokyo","Pekin","Seul","Taipei"],c:2},
{q:"İsviçre'nin başkenti neresidir?",a:["Zürih","Cenevre","Bern","Basel"],c:2},
{q:"Dünyanın en uzun nehri hangisidir?",a:["Amazon","Nil","Mississippi","Yangtze"],c:1},
{q:"Kızılırmak hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Fırat Nehri nereye dökülür?",a:["Karadeniz","Akdeniz","Basra Körfezi","Hazar"],c:2},
{q:"Ağrı Dağı'nın yüksekliği yaklaşık kaçtır?",a:["3137m","4137m","5137m","6137m"],c:2},
{q:"Türkiye'nin en büyük gölü hangisidir?",a:["Tuz","Beyşehir","Van","Burdur"],c:2},
{q:"Everest Dağı hangi sıradağ sistemindedir?",a:["Alpler","Karakurum","Himalayalar","And"],c:2},
{q:"Mariana Çukuru hangi okyanustadır?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Pangea ne demektir?",a:["İlk deniz","Süper kıta","İlk atmosfer","İlk göl"],c:1},
{q:"'Damlaya damlaya göl olur' ne demektir?",a:["Göle git","Birikim zamanla büyür","Su iç","Yağmur yağar"],c:1},
{q:"'İşleyen demir pas tutmaz' ne demektir?",a:["Demir al","Çalışan sağlıklı kalır","Pas sil","Demir sat"],c:1},
{q:"'Sakla samanı gelir zamanı' ne demektir?",a:["Saman al","Her şeyin lazım olacağı gün gelir","Zamanı bekle","Saman yak"],c:1},
{q:"'Armut piş ağzıma düş' ne demektir?",a:["Armut ye","Çaba göstermeden sonuç beklemek","Meyve al","Armut topla"],c:1},
{q:"'Bal tutan parmağını yalar' ne demektir?",a:["Bal ye","Fırsattan yararlanan kazanır","El yıka","Bal al"],c:1},
{q:"'Acele işe şeytan karışır' ne demektir?",a:["Şeytan var","Aceleyle hata yapılır","Hızlı koş","Yavaş yürü"],c:1},
{q:"'Yuvarlanan taş yosun tutmaz' ne demektir?",a:["Taş at","Sürekli değişen tutunamaz","Yosun topla","Taş kır"],c:1},
{q:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",a:["Yılan yakala","Güzel konuşma her kapıyı açar","Tatlı ye","Yılan besle"],c:1},
{q:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",a:["Ateş yak","Her söylentinin gerçeklik payı var","Duman çıkar","Yangın söndür"],c:1},
{q:"Shakespeare hangi ülkelidir?",a:["Fransa","Almanya","İtalya","İngiltere"],c:3},
{q:"Rönesans hangi ülkede başlamıştır?",a:["Fransa","İngiltere","İtalya","Almanya"],c:2},
{q:"Sanayi Devrimi hangi ülkede başlamıştır?",a:["Fransa","Almanya","ABD","İngiltere"],c:3},
{q:"Fransız İhtilali hangi yılda olmuştur?",a:["1776","1789","1815","1848"],c:1},
{q:"I. Dünya Savaşı hangi yılda başlamıştır?",a:["1912","1914","1916","1918"],c:1},
{q:"II. Dünya Savaşı hangi yılda bitmiştir?",a:["1943","1944","1945","1946"],c:2},
{q:"Olimpiyat oyunları kaç yılda bir düzenlenir?",a:["2","3","4","5"],c:2},
{q:"FIFA Dünya Kupası kaç yılda bir yapılır?",a:["2","3","4","5"],c:2},
{q:"Usain Bolt 100 metre rekorunu kaç saniyeyle kırdı?",a:["9.58","9.69","9.72","9.85"],c:0},
{q:"Hangisi bir greenhouse gazı değildir?",a:["CO2","Metan","Argon","N2O"],c:2},
{q:"Ozon tabakası atmosferin hangi katmanındadır?",a:["Troposfer","Stratosfer","Mezosfer","Termosfer"],c:1},
{q:"Dünya'nın en büyük okyanusu hangisidir?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Ekvator'un uzunluğu yaklaşık kaç km'dir?",a:["20.000","30.000","40.000","50.000"],c:2},
{q:"Türkiye kaç coğrafi bölgeye ayrılır?",a:["5","6","7","8"],c:2},
{q:"Suyun kimyasal formülü nedir?",a:["CO2","H2O","O2","NaCl"],c:1},
{q:"En ağır doğal element hangisidir?",a:["Altın","Kurşun","Uranyum","Plütonyum"],c:2},
{q:"Hangisi alkali metal değildir?",a:["Lityum","Sodyum","Kalsiyum","Potasyum"],c:2},
{q:"İnsan vücudundaki en büyük organ hangisidir?",a:["Kalp","Karaciğer","Deri","Beyin"],c:2},
{q:"Mozart hangi ülkelidir?",a:["Almanya","İtalya","Avusturya","Fransa"],c:2},
{q:"Beethoven hangi ülkelidir?",a:["Avusturya","Almanya","İtalya","Fransa"],c:1},
{q:"Mona Lisa tablosunu kim yapmıştır?",a:["Michelangelo","Raphael","Leonardo da Vinci","Botticelli"],c:2},
{q:"Van Gogh'un ünlü tablosu hangisidir?",a:["Mona Lisa","Yıldızlı Gece","Guernica","Çığlık"],c:1},
{q:"Polonya'nın başkenti neresidir?",a:["Prag","Varşova","Budapeşte","Bükreş"],c:1},
{q:"Norveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Kopenhag","Oslo"],c:3},
{q:"İsveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Oslo","Kopenhag"],c:0},
{q:"Romanya'nın başkenti neresidir?",a:["Budapeşte","Sofya","Bükreş","Belgrad"],c:2},
{q:"Bulgaristan'ın başkenti neresidir?",a:["Bükreş","Belgrad","Sofya","Atina"],c:2},
{q:"Portekiz'in başkenti neresidir?",a:["Madrid","Lizbon","Porto","Sevilla"],c:1},
{q:"Danimarka'nın başkenti neresidir?",a:["Oslo","Helsinki","Stockholm","Kopenhag"],c:3},
{q:"Finlandiya'nın başkenti neresidir?",a:["Oslo","Stockholm","Helsinki","Kopenhag"],c:2},
{q:"Çekya'nın başkenti neresidir?",a:["Bratislava","Varşova","Budapeşte","Prag"],c:3},
{q:"İran'ın başkenti neresidir?",a:["Bağdat","Tahran","Şam","Kabil"],c:1},
{q:"Arjantin'in başkenti neresidir?",a:["Santiago","Lima","Buenos Aires","Montevideo"],c:2},
{q:"Kolombiya'nın başkenti neresidir?",a:["Lima","Bogota","Quito","Santiago"],c:1},
{q:"Naim Süleymanoğlu hangi spor dalında başarılıdır?",a:["Güreş","Halter","Boks","Atletizm"],c:1},
{q:"Aziz Sancar hangi alanda Nobel ödülü almıştır?",a:["Fizik","Kimya","Tıp","Barış"],c:1},
{q:"Marie Curie hangi elementleri keşfetmiştir?",a:["Oksijen-Azot","Polonyum-Radyum","Helyum-Neon","Demir-Bakır"],c:1},
{q:"Albert Einstein'ın en ünlü formülü nedir?",a:["F=ma","E=mc²","PV=nRT","V=IR"],c:1},
{q:"Kopernik hangi modeli savunmuştur?",a:["Yer merkezli","Güneş merkezli","Ay merkezli","Yıldız merkezli"],c:1},
{q:"Tesla hangi alanda çalışmıştır?",a:["Tıp","Elektrik/AC","Kimya","Astronomi"],c:1},
{q:"Edison neyi geliştirmiştir?",a:["Telefon","Ampul","Radyo","TV"],c:1},
{q:"Bell neyi icat etmiştir?",a:["Ampul","Telgraf","Telefon","Radyo"],c:2},
{q:"Newton hangi meyvenin düşmesiyle yerçekimi keşfetti?",a:["Armut","Portakal","Elma","Erik"],c:2},
{q:"Galile hangi aracı kullanmıştır?",a:["Mikroskop","Teleskop","Pusula","Saat"],c:1},
{q:"Amazon Nehri hangi okyanusa dökülür?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Tuna Nehri hangi denize dökülür?",a:["Akdeniz","Karadeniz","Baltık","Ege"],c:1},
{q:"Mississippi Nehri hangi okyanusa dökülür?",a:["Pasifik","Atlas","Hint","Arktik"],c:1},
{q:"Volga Nehri hangi denize dökülür?",a:["Karadeniz","Baltık","Hazar","Akdeniz"],c:2},
{q:"Ganj Nehri hangi körfeze dökülür?",a:["Basra","Bengal","Aden","Oman"],c:1},
{q:"Sahra Çölü hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:2},
{q:"And Dağları hangi kıtadadır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Himalaya Dağları hangi kıtadadır?",a:["Avrupa","Afrika","Asya","Amerika"],c:2},
{q:"Kilimanjaro hangi ülkededir?",a:["Kenya","Uganda","Tanzanya","Etiyopya"],c:2},
{q:"Büyük Set Resifi hangi ülkedededir?",a:["Brezilya","Hindistan","Avustralya","Meksika"],c:2},
{q:"Hazar Denizi aslında nedir?",a:["Deniz","Okyanus","Göl","Kanal"],c:2},
{q:"Baykal Gölü hangi ülkededir?",a:["Çin","Moğolistan","Rusya","Kazakistan"],c:2},
{q:"Panama Kanalı hangi okyanusları birleştirir?",a:["Atlas-Hint","Pasifik-Atlas","Hint-Pasifik","Atlas-Arktik"],c:1},
{q:"Süveyş Kanalı hangi ülkededir?",a:["Türkiye","İsrail","Irak","Mısır"],c:3},
{q:"İstanbul Boğazı hangi denizleri birleştirir?",a:["Ege-Marmara","Karadeniz-Marmara","Akdeniz-Ege","Karadeniz-Ege"],c:1},
{q:"Orhan Pamuk Nobel ödülünü hangi yıl almıştır?",a:["2004","2005","2006","2008"],c:2},
{q:"Yaşar Kemal'in en ünlü eseri hangisidir?",a:["Tutunamayanlar","İnce Memed","Kürk Mantolu Madonna","Huzur"],c:1},
{q:"Nazım Hikmet ne tür eserler yazmıştır?",a:["Roman","Şiir","Masal","Deneme"],c:1},
{q:"Ahmet Hamdi Tanpınar'ın ünlü romanı hangisidir?",a:["İnce Memed","Tutunamayanlar","Huzur","Çalıkuşu"],c:2},
{q:"Reşat Nuri Güntekin'in ünlü eseri hangisidir?",a:["Huzur","Çalıkuşu","Sinekli Bakkal","Mai ve Siyah"],c:1},
{q:"Halide Edip Adıvar'ın ünlü romanı hangisidir?",a:["Çalıkuşu","Sinekli Bakkal","Huzur","İnce Memed"],c:1},
{q:"İsviçre'nin resmi dili kaç tanedir?",a:["2","3","4","5"],c:2},
{q:"BM'nin daimi Güvenlik Konseyi üyesi kaç ülkedir?",a:["3","4","5","7"],c:2},
{q:"NATO ne zaman kurulmuştur?",a:["1945","1949","1955","1961"],c:1},
{q:"Avrupa Birliği'nin merkezi nerededir?",a:["Paris","Berlin","Brüksel","Strasbourg"],c:2},
{q:"Hangisi halojen grubu elementidir?",a:["Sodyum","Klor","Kalsiyum","Demir"],c:1},
{q:"Güneş'in yüzey sıcaklığı yaklaşık kaç derecedir?",a:["1500°C","3500°C","5500°C","8500°C"],c:2},
{q:"Hangisi bir cüce gezegen değildir?",a:["Plüton","Ceres","Eris","Merkür"],c:3},
{q:"Türkiye'nin en doğusundaki il hangisidir?",a:["Van","Kars","Hakkari","Iğdır"],c:2},
{q:"Türkiye'nin en batısındaki il hangisidir?",a:["İzmir","Muğla","Edirne","Çanakkale"],c:2},
{q:"Dünya'nın en küçük ülkesi hangisidir?",a:["Monako","Vatikan","San Marino","Lihtenştayn"],c:1},
{q:"Dünya'nın en kalabalık ülkesi hangisidir?",a:["ABD","Çin","Hindistan","Endonezya"],c:2},
{q:"Hangisi bir baz değildir?",a:["NaOH","KOH","Ca(OH)2","HCl"],c:3},
{q:"Hangisi bir empresyonist ressamdır?",a:["Picasso","Monet","Dalí","Warhol"],c:1},
{q:"Olimpiyat ateşi nerede yakılır?",a:["Roma","Atina","Paris","Londra"],c:1},
{q:"Hangisi bir Türk Nobel ödüllüsüdür?",a:["Yaşar Kemal","Orhan Pamuk","Nazım Hikmet","Cemal Süreya"],c:1},
{q:"Hangisi bir opera bestecisi değildir?",a:["Verdi","Puccini","Chopin","Wagner"],c:2},
{q:"En çok Oscar ödülü alan film hangisidir?",a:["Titanic","Avatar","Ben-Hur","Godfather"],c:2},
{q:"Hangisi bir UNESCO Dünya Mirası değildir?",a:["Göbeklitepe","Efes","Anıtkabir","Troya"],c:2}
],
medium:[
{q:"'Sütten ağzı yanan yoğurdu üfleyerek yer' ne demektir?",a:["Yoğurt ye","Kötü deneyim yaşayan aşırı tedbirli olur","Süt iç","Üfle"],c:1},
{q:"'Bıçak kemiğe dayandı' ne demektir?",a:["Bıçak kes","Tahammülün sonuna gelindi","Kemik kır","Keskin ol"],c:1},
{q:"'Deveye hendek atlatmak' ne demektir?",a:["Deve bin","Zor işi yaptırmaya çalışmak","Hendek kaz","Deve sat"],c:1},
{q:"'Gönül ne kahve ister ne kahvehane' ne demektir?",a:["Kahve iç","Önemli olan dostluk","Kahve yap","Gönül al"],c:1},
{q:"'Lafla peynir gemisi yürümez' ne demektir?",a:["Peynir al","Konuşmakla iş olmaz eylem gerek","Gemi sür","Laf etme"],c:1},
{q:"'Minareyi çalan kılıfını hazırlar' ne demektir?",a:["Minare yap","Kötülük yapan önlemini alır","Kılıf dik","Çalmak kötü"],c:1},
{q:"'Kırk yıllık Kani olur mu Yani' ne demektir?",a:["İsim değiştir","Eski alışkanlıklar değişmez","Kırk yıl bekle","Yeni ol"],c:1},
{q:"'Dost kara günde belli olur' ne demektir?",a:["Kara gün gelir","Gerçek dost zor zamanda yanında olur","Dost ara","Gün gelir"],c:1},
{q:"'Gülme komşuna gelir başına' ne demektir?",a:["Gülme","Başkasına gelen sana da gelebilir","Komşuya git","Gül topla"],c:1},
{q:"'Körle yatan şaşı kalkar' ne demektir?",a:["Uyu","Kötü arkadaş kötü alışkanlık verir","Şaşı ol","Gözlük tak"],c:1},
{q:"'Sürüden ayrılanı kurt kapar' ne demektir?",a:["Kurt yakala","Topluluktan ayrılan tehlikeye düşer","Sürüye git","Kurt besle"],c:1},
{q:"'Mum dibine ışık vermez' ne demektir?",a:["Mum yak","Kişi yakınlarına fayda sağlayamayabilir","Işık aç","Karanlık"],c:1},
{q:"'Ak akçe kara gün içindir' ne demektir?",a:["Para harca","Zor günler için biriktir","Akçe bul","Kara gün gelir"],c:1},
{q:"'Aşk olmayınca meşk olmaz' ne demektir?",a:["Aşık ol","Sevgi olmadan öğrenim olmaz","Meşk et","Müzik çal"],c:1},
{q:"'Besle kargayı oysun gözünü' ne demektir?",a:["Karga besle","İyilik yaptığın kötülük yapabilir","Göz kapat","Kov"],c:1},
{q:"Ohm yasası nedir?",a:["F=ma","E=mc²","V=IR","PV=nRT"],c:2},
{q:"Coulomb yasası neyi tanımlar?",a:["Manyetik kuvvet","Elektrik kuvveti","Yerçekimi","Sürtünme"],c:1},
{q:"Entropi ne demektir?",a:["Enerji","Düzensizlik ölçüsü","Kuvvet","Hız"],c:1},
{q:"Mol kavramı neyi ifade eder?",a:["Kütle","Hacim","Madde miktarı","Yoğunluk"],c:2},
{q:"Hücre bölünmesinin iki türü nedir?",a:["Fotosentez-Solunum","Mitoz-Mayoz","Osmoz-Difüzyon","Sentez-Analiz"],c:1},
{q:"Mayoz bölünme sonucu kaç hücre oluşur?",a:["2","3","4","8"],c:2},
{q:"Mitoz bölünme sonucu kaç hücre oluşur?",a:["1","2","3","4"],c:1},
{q:"Mendel hangi bitkiyle genetik deneyleri yapmıştır?",a:["Buğday","Bezelye","Domates","Mısır"],c:1},
{q:"Kromozom sayısı insanda kaçtır?",a:["23","44","46","48"],c:2},
{q:"RNA'nın görevi nedir?",a:["Enerji üretmek","Protein sentezi","Yağ depolamak","Sindirim"],c:1},
{q:"Enzim ne tür bir moleküldür?",a:["Karbonhidrat","Yağ","Protein","Nükleik asit"],c:2},
{q:"Osmoz nedir?",a:["Gazların yayılması","Suyun yarı geçirgen zardan geçişi","Işığın kırılması","Sesin yayılması"],c:1},
{q:"Difüzyon nedir?",a:["Suyun hareketi","Maddelerin yoğun ortamdan seyreke yayılması","Işığın yansıması","Enerji dönüşümü"],c:1},
{q:"Katalizör ne işe yarar?",a:["Enerji üretir","Tepkimeyi hızlandırır","Madde üretir","Isı verir"],c:1},
{q:"Tanzimat Fermanı kaç yılında ilan edilmiştir?",a:["1808","1839","1876","1908"],c:1},
{q:"Kanun-i Esasi kaç yılında ilan edilmiştir?",a:["1839","1856","1876","1908"],c:2},
{q:"II. Meşrutiyet kaç yılında ilan edilmiştir?",a:["1876","1893","1908","1918"],c:2},
{q:"Viyana Kuşatması kaç yılındadır?",a:["1529","1571","1683","1699"],c:2},
{q:"Mohaç Savaşı kaç yılındadır?",a:["1453","1517","1526","1571"],c:2},
{q:"Preveze Deniz Savaşı kaç yılındadır?",a:["1453","1517","1538","1571"],c:2},
{q:"Lepanto (İnebahtı) Deniz Savaşı kaç yılındadır?",a:["1538","1571","1683","1699"],c:1},
{q:"Karlofça Antlaşması kaç yılında imzalanmıştır?",a:["1683","1699","1718","1774"],c:1},
{q:"Küçük Kaynarca Antlaşması kaç yılındadır?",a:["1699","1718","1739","1774"],c:3},
{q:"Ukrayna'nın başkenti neresidir?",a:["Moskova","Minsk","Kiev","Varşova"],c:2},
{q:"Hırvatistan'ın başkenti neresidir?",a:["Belgrad","Ljubljana","Zagreb","Saraybosna"],c:2},
{q:"Sırbistan'ın başkenti neresidir?",a:["Sofya","Bükreş","Zagreb","Belgrad"],c:3},
{q:"Bosna'nın başkenti neresidir?",a:["Zagreb","Belgrad","Saraybosna","Podgorica"],c:2},
{q:"Küba'nın başkenti neresidir?",a:["Meksiko","Havana","Lima","Bogota"],c:1},
{q:"Şili'nin başkenti neresidir?",a:["Buenos Aires","Lima","Montevideo","Santiago"],c:3},
{q:"Dicle Nehri hangi ülkelerden geçer?",a:["Türkiye-İran","Türkiye-Irak","Türkiye-Suriye","İran-Irak"],c:1},
{q:"Yangtze Nehri hangi ülkededir?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"Mekong Nehri hangi bölgeden geçer?",a:["Orta Doğu","Güneydoğu Asya","Kuzey Afrika","Güney Amerika"],c:1},
{q:"Ren Nehri hangi denize dökülür?",a:["Akdeniz","Baltık","Karadeniz","Kuzey Denizi"],c:3},
{q:"Kongo Nehri hangi okyanusa dökülür?",a:["Hint","Pasifik","Atlas","Arktik"],c:2},
{q:"K2 Dağı hangi ülkededir?",a:["Nepal","Çin","Pakistan","Hindistan"],c:2},
{q:"Mont Blanc hangi ülkeler arasındadır?",a:["İsviçre-Avusturya","Fransa-İtalya","İspanya-Fransa","İtalya-Avusturya"],c:1},
{q:"Elbrus Dağı hangi ülkededir?",a:["Türkiye","Gürcistan","Rusya","İran"],c:2},
{q:"Aconcagua hangi kıtanın en yüksek dağıdır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Viktorya Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Titicaca Gölü hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Kuzey Amerika"],c:2},
{q:"Büyük Göller hangi ülkeler arasındadır?",a:["Rusya-Çin","ABD-Kanada","Brezilya-Arjantin","İngiltere-Fransa"],c:1},
{q:"Bering Boğazı hangi kıtaları ayırır?",a:["Avrupa-Afrika","Asya-Kuzey Amerika","Avrupa-Asya","Afrika-Asya"],c:1},
{q:"Cebelitarık Boğazı hangi kıtaları ayırır?",a:["Avrupa-Asya","Asya-Afrika","Avrupa-Afrika","Amerika-Avrupa"],c:2},
{q:"Picasso hangi sanat akımının öncülerindendir?",a:["İzlenimcilik","Kübizm","Sürrealizm","Romantizm"],c:1},
{q:"Dalí hangi sanat akımına aittir?",a:["Kübizm","İzlenimcilik","Sürrealizm","Pop Art"],c:2},
{q:"Vivaldi hangi ülkelidir?",a:["Almanya","Avusturya","Fransa","İtalya"],c:3},
{q:"Çaykovski hangi ülkelidir?",a:["Polonya","Almanya","Avusturya","Rusya"],c:3},
{q:"Verdi hangi müzik türünde eserler vermiştir?",a:["Senfoni","Opera","Konçerto","Sonat"],c:1},
{q:"Wagner hangi ülkelidir?",a:["Avusturya","İtalya","Fransa","Almanya"],c:3},
{q:"Mimar Sinan'ın ustalık eseri hangisidir?",a:["Süleymaniye","Selimiye","Sultanahmet","Şehzade"],c:1},
{q:"Evliya Çelebi neyle tanınır?",a:["Savaş","Seyahatname","Mimari","Tıp"],c:1},
{q:"Piri Reis neyle tanınır?",a:["Şiir","Dünya haritası","Mimari","Müzik"],c:1},
{q:"İbn-i Sina hangi alanda öncüdür?",a:["Matematik","Mimari","Tıp","Astronomi"],c:2},
{q:"Harezmi neyin temelini atmıştır?",a:["Tıp","Cebir","Mimari","Coğrafya"],c:1},
{q:"Cristiano Ronaldo hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:2},
{q:"Lionel Messi hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:3},
{q:"Roger Federer hangi ülkelidir?",a:["Avusturya","Almanya","İsveç","İsviçre"],c:3},
{q:"Michael Phelps hangi spor dalında ünlüdür?",a:["Atletizm","Boks","Yüzme","Tenis"],c:2},
{q:"Türkiye en çok olimpiyat madalyasını hangi sporda almıştır?",a:["Futbol","Güreş","Halter","Basketbol"],c:1},
{q:"Galatasaray UEFA Kupası'nı hangi yıl kazanmıştır?",a:["1998","2000","2002","2004"],c:1},
{q:"1896 modern olimpiyatları nerede yapılmıştır?",a:["Paris","Londra","Atina","Roma"],c:2},
{q:"Toros Dağları hangi bölgemizin kıyı kenarında uzanır?",a:["Karadeniz","Ege","Akdeniz","Marmara"],c:2},
{q:"Hangisi bir soy gaz değildir?",a:["Helyum","Neon","Argon","Oksijen"],c:3},
{q:"Planck sabiti hangi alanda kullanılır?",a:["Termodinamik","Kuantum mekaniği","Optik","Akustik"],c:1},
{q:"Doppler etkisi neyi açıklar?",a:["Işık kırılması","Dalga frekans değişimi","Yerçekimi","Manyetizma"],c:1},
{q:"Bernoulli prensibi neyle ilgilidir?",a:["Elektrik","Akışkan dinamiği","Termodinamik","Optik"],c:1},
{q:"Kepler yasaları neyi tanımlar?",a:["Atom yapısı","Gezegen hareketleri","Işık kırılması","Ses yayılması"],c:1},
{q:"Archimedes ilkesi neyi açıklar?",a:["Kaldırma kuvveti","Yerçekimi","Manyetizma","Elektrik"],c:0},
{q:"Ampere yasası neyle ilgilidir?",a:["Yerçekimi","Elektrik akımı ve manyetik alan","Ses dalgaları","Işık"],c:1},
{q:"Faraday yasası neyi açıklar?",a:["Elektromanyetik indüksiyon","Yerçekimi","Optik","Termodinamik"],c:0},
{q:"Boyle yasası neyi tanımlar?",a:["Sıcaklık-hacim","Basınç-hacim","Kütle-hız","Kuvvet-ivme"],c:1},
{q:"Charles yasası neyi tanımlar?",a:["Basınç-hacim","Sıcaklık-hacim","Kütle-enerji","Kuvvet-mesafe"],c:1},
{q:"Mevlana'nın doğum yeri neresidir?",a:["Konya","İstanbul","Belh","Bağdat"],c:2},
{q:"Fuzuli hangi edebiyat dönemine aittir?",a:["Tanzimat","Divan","Milli","Cumhuriyet"],c:1},
{q:"Nedim hangi dönemin şairidir?",a:["Fatih dönemi","Kanuni dönemi","Lale Devri","Tanzimat"],c:2},
{q:"Baki hangi padişahın şairidir?",a:["Fatih","Yavuz","Kanuni","III. Murad"],c:2},
{q:"Namık Kemal hangi edebiyat dönemine aittir?",a:["Divan","Tanzimat","Servet-i Fünun","Fecr-i Ati"],c:1},
{q:"Tevfik Fikret hangi edebiyat dönemine aittir?",a:["Divan","Tanzimat","Servet-i Fünun","Milli Edebiyat"],c:2},
{q:"Ziya Gökalp hangi akımın savunucusudur?",a:["Osmanlıcılık","İslamcılık","Türkçülük","Batıcılık"],c:2},
{q:"Ömer Seyfettin hangi edebiyat dönemine aittir?",a:["Tanzimat","Servet-i Fünun","Milli Edebiyat","Cumhuriyet"],c:2},
{q:"Halit Ziya Uşaklıgil'in ünlü eseri hangisidir?",a:["Çalıkuşu","Mai ve Siyah","İnce Memed","Huzur"],c:1},
{q:"Sabahattin Ali'nin ünlü romanı hangisidir?",a:["İnce Memed","Kürk Mantolu Madonna","Huzur","Çalıkuşu"],c:1},
{q:"Oğuz Atay'ın ünlü eseri hangisidir?",a:["İnce Memed","Kürk Mantolu Madonna","Tutunamayanlar","Huzur"],c:2},
{q:"'Kürk Mantolu Madonna' kimin eseridir?",a:["Yaşar Kemal","Orhan Pamuk","Sabahattin Ali","Ahmet Hamdi Tanpınar"],c:2},
{q:"Dünya'nın en büyük çölü hangisidir?",a:["Gobi","Sahra","Atacama","Kalahari"],c:1},
{q:"Karadeniz Bölgesi'nin en yüksek dağı hangisidir?",a:["Ilgaz","Bolu","Kaçkar","Zigana"],c:2},
{q:"Doğu Anadolu Bölgesi'nin en önemli gölü hangisidir?",a:["Tuz Gölü","Burdur","Van","Eğirdir"],c:2},
{q:"Galileo Galilei neyi keşfetmiştir?",a:["Amerika","Jüpiter uyduları","Penisilin","DNA"],c:1},
{q:"Hangisi bir Osmanlı minyatür sanatçısıdır?",a:["Matrakçı Nasuh","Da Vinci","Monet","Rembrandt"],c:0},
{q:"Dünya Kupası'nı en çok kazanan futbol takımı hangisidir?",a:["Almanya","İtalya","Brezilya","Arjantin"],c:2},
{q:"Hangisi bir opera bestecisidir?",a:["Bach","Verdi","Chopin","Liszt"],c:1},
{q:"Troya Antik Kenti hangi ilimizde yer alır?",a:["İzmir","Çanakkale","Balıkesir","Edirne"],c:1},
{q:"Formula 1'de en çok şampiyonluk kazanan pilot kimdir?",a:["Senna","Schumacher","Hamilton","Vettel"],c:2},
{q:"Hangisi bir Türk romanıdır?",a:["Savaş ve Barış","Suç ve Ceza","Çalıkuşu","Don Kişot"],c:2},
{q:"Kremlin hangi ülkededir?",a:["Çin","İngiltere","Rusya","Fransa"],c:2},
{q:"Hangisi bir dans yarışması formatıdır?",a:["Survivor","MasterChef","Dancing with Stars","The Voice"],c:2},
{q:"Uzayda yürüyen ilk kadın astronot kimdir?",a:["Sally Ride","Valentina Tereşkova","Svetlana Savitskaya","Mae Jemison"],c:2},
{q:"Hangisi bir Türk hat sanatçısıdır?",a:["Matisse","Hamid Aytaç","Renoir","Cézanne"],c:1},
{q:"Dünya'nın en uzun köprüsü hangi ülkededir?",a:["ABD","Japonya","Çin","İngiltere"],c:2},
{q:"Hangisi bir müzik festivalidir?",a:["Cannes","Sundance","Eurovision","Oscar"],c:2},
{q:"Pekin Operası hangi ülkenin sanatıdır?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"Hangisi bir kış olimpiyat sporu değildir?",a:["Kayaklı koşu","Curling","Badminton","Biatlon"],c:2},
{q:"Türkiye'nin ilk olimpiyat madalyası hangi spordandır?",a:["Halter","Güreş","Boks","Atletizm"],c:1},
{q:"Hangisi bir fotoğraf sanatçısıdır?",a:["Ansel Adams","Beethoven","Chopin","Shakespeare"],c:0},
{q:"Super Bowl hangi sporun final maçıdır?",a:["Basketbol","Beyzbol","Amerikan Futbolu","Buz Hokeyi"],c:2},
{q:"Hangisi bir Türk mimari eseridir?",a:["Taj Mahal","Selimiye Camii","Sagrada Familia","Notre Dame"],c:1},
{q:"Milli Mücadele döneminin ünlü kadın kahramanı kimdir?",a:["Halide Edip Adıvar","Sabiha Gökçen","Afet İnan","Latife Hanım"],c:0},
{q:"Hangisi bir Akdeniz yemeğidir?",a:["Sushi","Ramen","Hummus","Dim Sum"],c:2},
{q:"Emmy ödülü hangi alandadır?",a:["Sinema","Televizyon","Müzik","Edebiyat"],c:1}
],
hard:[
{q:"'Hamama giren terler' ne demektir?",a:["Hamama git","Bir işe giren zorluğuna katlanır","Terle","Yıkan"],c:1},
{q:"'Bakarsan bağ olur bakmazsan dağ olur' ne demektir?",a:["Bağ dik","İlgilenirsen güzel bakmazsan kötü olur","Dağa çık","Bağ al"],c:1},
{q:"'Davulun sesi uzaktan hoş gelir' ne demektir?",a:["Davul çal","Uzaktan güzel görünen yakından öyle olmayabilir","Uzak dur","Müzik dinle"],c:1},
{q:"'Her yiğidin bir yoğurt yiyişi vardır' ne demektir?",a:["Yoğurt ye","Herkesin kendine has yöntemi var","Yiğit ol","Yoğurt yap"],c:1},
{q:"'Boş çuval ayakta durmaz' ne demektir?",a:["Çuval doldur","Bilgisiz kişi başarısız olur","Çuval at","Ayakta dur"],c:1},
{q:"'Kaz gelecek yerden tavuk esirgenmez' ne demektir?",a:["Kaz besle","Büyük kazanç için küçük harcama yapılır","Tavuk sat","Kaz ye"],c:1},
{q:"'Dervişin fikri neyse zikri de odur' ne demektir?",a:["Dua et","Aklındakini söyler","Derviş ol","Fikir sor"],c:1},
{q:"'Karga kekliğe bakıp yürümeye kalkmış' ne demektir?",a:["Karga izle","Taklitçilik zararlıdır","Keklik yakala","Kuş seyret"],c:1},
{q:"'Abanoz böceği meşeyi yer' ne demektir?",a:["Böcek yakala","Küçük zarar sürekli olursa büyür","Meşe kes","Böcek besle"],c:1},
{q:"'Dut yemiş bülbüle döndü' ne demektir?",a:["Dut ye","Sessizleşti sustu","Bülbül dinle","Şarkı söyle"],c:1},
{q:"'Her kuşun eti yenmez' ne demektir?",a:["Kuş ye","Herkesle uğraşılmaz","Kuş yakala","Et ye"],c:1},
{q:"'İğneyi kendine çuvaldızı başkasına batır' ne demektir?",a:["İğne batır","Önce kendini eleştir","Dikiş dik","Çuvaldız al"],c:1},
{q:"'Et tırnaktan ayrılmaz' ne demektir?",a:["Et ye","Yakın akrabalar kopmaz","Tırnak kes","Et kes"],c:1},
{q:"'İki cambaz bir ipte oynamaz' ne demektir?",a:["Cambaz ol","Aynı yerde iki lider olmaz","İp atla","Cambaz izle"],c:1},
{q:"'Ava giden avlanır' ne demektir?",a:["Ava git","Kötülük yapan kendisi zarar görür","Avlan","Tuzak kur"],c:1},
{q:"Heisenberg belirsizlik ilkesi ne söyler?",a:["Konum ve momentum aynı anda kesin ölçülemez","Enerji korunur","Entropi artar","Işık sabit hızda"],c:0},
{q:"Altın oran yaklaşık kaçtır?",a:["1.414","2.718","3.141","1.618"],c:3},
{q:"Higgs bozonu ne sağlar?",a:["Işık","Manyetizma","Kütle","Yerçekimi"],c:2},
{q:"Nötron yıldızı ne oluşturur?",a:["Beyaz cüce","Kara delik","Pulsar","Nebula"],c:2},
{q:"Flor hangi özelliğiyle bilinir?",a:["En ağır","En elektronegatif","En büyük","En az reaktif"],c:1},
{q:"Pauli dışlama ilkesi ne söyler?",a:["İki fermiyonun aynı kuantum hali yok","Enerji kuantumlu","Dalga-parçacık","Belirsizlik"],c:0},
{q:"Aziz Sancar DNA tamirinin hangi mekanizmasını çözmüştür?",a:["Replikasyon","Transkripsiyon","Nükleotid eksizyon tamiri","Translasyon"],c:2},
{q:"CRISPR teknolojisi ne için kullanılır?",a:["Gen düzenleme","İlaç üretimi","Görüntüleme","Enerji"],c:0},
{q:"Karanlık madde evrenin yüzde kaçını oluşturur?",a:["5","15","27","68"],c:2},
{q:"Chandrasekhar limiti neyi belirler?",a:["Beyaz cüce kütle sınırı","Kara delik yarıçapı","Nötron yıldızı","Galaksi boyutu"],c:0},
{q:"Standart Model'de kaç temel parçacık vardır?",a:["12","17","24","36"],c:1},
{q:"Lale Devri hangi padişah dönemindedir?",a:["III. Ahmed","III. Selim","II. Mahmud","I. Abdülhamid"],c:0},
{q:"Yavuz Sultan Selim hangi savaşla Mısır'ı almıştır?",a:["Çaldıran","Mercidabık","Ridaniye","Mohaç"],c:2},
{q:"Kırım hangi antlaşmayla kaybedilmiştir?",a:["Karlofça","Küçük Kaynarca","Edirne","Berlin"],c:1},
{q:"Osmanlı'nın son padişahı kimdir?",a:["Abdülhamid II","Mehmed V","Mehmed VI","Vahdettin"],c:2},
{q:"Mondros Ateşkesi hangi yılda imzalanmıştır?",a:["1916","1917","1918","1919"],c:2},
{q:"Sevr Antlaşması hangi yılda imzalanmıştır?",a:["1918","1919","1920","1921"],c:2},
{q:"Suudi Arabistan'ın başkenti neresidir?",a:["Dubai","Mekke","Riyad","Medine"],c:2},
{q:"Lena Nehri hangi ülkededir?",a:["Kanada","Çin","Rusya","ABD"],c:2},
{q:"Ob Nehri hangi ülkededir?",a:["Çin","Rusya","Kanada","ABD"],c:1},
{q:"Yenisey Nehri hangi ülkededir?",a:["Kanada","Rusya","Çin","Moğolistan"],c:1},
{q:"Nijer Nehri hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Orinoko Nehri hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Avrupa"],c:2},
{q:"Murray Nehri hangi ülkededir?",a:["ABD","Kanada","Avustralya","Yeni Zelanda"],c:2},
{q:"İndus Nehri hangi ülkelerden geçer?",a:["Hindistan-Bangladeş","Çin-Hindistan-Pakistan","Nepal-Hindistan","Çin-Moğolistan"],c:1},
{q:"Atacama Çölü hangi ülkededir?",a:["Arjantin","Peru","Şili","Meksika"],c:2},
{q:"Gobi Çölü hangi ülkelerdedir?",a:["İran-Irak","Çin-Moğolistan","Hindistan-Pakistan","Mısır-Libya"],c:1},
{q:"Takla Makan Çölü hangi ülkededir?",a:["Moğolistan","İran","Çin","Pakistan"],c:2},
{q:"McKinley (Denali) hangi kıtanın en yüksek dağıdır?",a:["Avrupa","Asya","Güney Amerika","Kuzey Amerika"],c:3},
{q:"Fuji Dağı hangi ülkededir?",a:["Çin","Kore","Japonya","Vietnam"],c:2},
{q:"Vezüv Yanardağı hangi ülkededir?",a:["Yunanistan","Türkiye","İtalya","İspanya"],c:2},
{q:"Etna Yanardağı hangi ülkededir?",a:["Yunanistan","İspanya","Türkiye","İtalya"],c:3},
{q:"Tanganyika Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Aral Gölü neden küçülmüştür?",a:["Deprem","Sulama için su çekilmesi","Küresel ısınma","Volkanik aktivite"],c:1},
{q:"Çad Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Afrika","Avrupa"],c:2},
{q:"Hürmüz Boğazı hangi bölgededir?",a:["Akdeniz","Basra Körfezi","Kızıldeniz","Güneydoğu Asya"],c:1},
{q:"Malakka Boğazı hangi bölgededir?",a:["Orta Doğu","Akdeniz","Güneydoğu Asya","Güney Amerika"],c:2},
{q:"'Gülü seven dikenine katlanır' ne demektir?",a:["Gül topla","Bir şeyi seven zorluklarına katlanır","Diken batır","Bahçe yap"],c:1},
{q:"'Hazıra dağlar dayanmaz' ne demektir?",a:["Dağa git","Çalışmadan harcanan biter","Hazırla","Dağ aş"],c:1},
{q:"'Yuvayı dişi kuş yapar' ne demektir?",a:["Kuş besle","Evi kadın düzenler","Yuva yap","Kuş izle"],c:1},
{q:"'Su uyur düşman uyumaz' ne demektir?",a:["Su iç","Tetikte ol","Uyu","Düşmanı sev"],c:1},
{q:"'Taşıma su ile değirmen dönmez' ne demektir?",a:["Su taşı","Dışarıdan destek alarak iş sürdürülmez","Değirmen yap","Su getir"],c:1},
{q:"Westfalya Barışı hangi yılda imzalanmıştır?",a:["1555","1618","1648","1713"],c:2},
{q:"Magna Carta hangi yılda imzalanmıştır?",a:["1066","1215","1453","1492"],c:1},
{q:"Amerikan Bağımsızlık Bildirgesi hangi yılda ilan edilmiştir?",a:["1776","1789","1812","1848"],c:0},
{q:"Waterloo Savaşı hangi yılda olmuştur?",a:["1805","1812","1815","1820"],c:2},
{q:"Osmanlı'da ilk matbaa hangi padişah döneminde kurulmuştur?",a:["III. Ahmed","II. Mahmud","III. Selim","Abdülmecid"],c:0},
{q:"Islahat Fermanı hangi yılda ilan edilmiştir?",a:["1839","1856","1876","1908"],c:1},
{q:"Trablusgarp Savaşı hangi yılda yapılmıştır?",a:["1908","1911","1912","1914"],c:1},
{q:"Balkan Savaşları hangi yıllarda olmuştur?",a:["1908-1910","1912-1913","1914-1915","1916-1917"],c:1},
{q:"Dumlupınar Savaşı hangi yılda yapılmıştır?",a:["1920","1921","1922","1923"],c:2},
{q:"Amasya Genelgesi hangi yılda yayınlanmıştır?",a:["1919","1920","1921","1922"],c:0},
{q:"Erzurum Kongresi hangi yılda yapılmıştır?",a:["1919","1920","1921","1922"],c:0},
{q:"Sivas Kongresi hangi yılda yapılmıştır?",a:["1919","1920","1921","1922"],c:0},
{q:"Saltanat ne zaman kaldırılmıştır?",a:["1920","1922","1923","1924"],c:1},
{q:"Halifelik ne zaman kaldırılmıştır?",a:["1922","1923","1924","1925"],c:2},
{q:"Kabotaj Kanunu hangi yılda çıkarılmıştır?",a:["1923","1924","1925","1926"],c:3},
{q:"Soyadı Kanunu hangi yılda çıkarılmıştır?",a:["1930","1932","1934","1936"],c:2},
{q:"Kadınlara seçme-seçilme hakkı hangi yıl verilmiştir?",a:["1930","1932","1934","1936"],c:2},
{q:"Montrö Boğazlar Sözleşmesi hangi yılda imzalanmıştır?",a:["1923","1930","1936","1938"],c:2},
{q:"Hatay hangi yıl Türkiye'ye katılmıştır?",a:["1936","1938","1939","1940"],c:2},
{q:"Bağlama kaç telli bir çalgıdır?",a:["3","5","7","9"],c:2},
{q:"Ney hangi malzemeden yapılır?",a:["Ağaç","Kamış","Metal","Plastik"],c:1},
{q:"Kanun hangi çalgı grubuna aittir?",a:["Yaylı","Üflemeli","Telli","Vurmalı"],c:2},
{q:"Kudüm hangi çalgı grubuna aittir?",a:["Telli","Üflemeli","Yaylı","Vurmalı"],c:3},
{q:"İmpresyonizm (İzlenimcilik) hangi alanda bir akımdır?",a:["Müzik","Resim","Mimari","Heykel"],c:1},
{q:"Monet hangi sanat akımının temsilcisidir?",a:["Kübizm","Sürrealizm","İzlenimcilik","Pop Art"],c:2},
{q:"Edvard Munch'un 'Çığlık' tablosu hangi akıma aittir?",a:["İzlenimcilik","Ekspresyonizm","Kübizm","Sürrealizm"],c:1},
{q:"Andy Warhol hangi sanat akımının temsilcisidir?",a:["Kübizm","Sürrealizm","Pop Art","Minimalizm"],c:2},
{q:"Rönesans hangi yüzyıllarda yaşanmıştır?",a:["11-13.","13-14.","14-17.","17-19."],c:2},
{q:"Barok dönem hangi yüzyılları kapsar?",a:["14-15.","15-16.","17-18.","18-19."],c:2},
{q:"Romantik dönem müziği hangi yüzyılda yaygınlaşmıştır?",a:["17.","18.","19.","20."],c:2},
{q:"Klasisizm hangi ülkede ortaya çıkmıştır?",a:["İngiltere","İtalya","Almanya","Fransa"],c:3},
{q:"Realizm (Gerçekçilik) hangi yüzyılda ortaya çıkmıştır?",a:["17.","18.","19.","20."],c:2},
{q:"Naturalizm hangi akımın devamıdır?",a:["Romantizm","Realizm","Klasisizm","Sürrealizm"],c:1},
{q:"İndus Vadisi Uygarlığı hangi bölgededir?",a:["Mezopotamya","Mısır","Güney Asya","Çin"],c:2},
{q:"Mezopotamya hangi nehirler arasındadır?",a:["Nil-Kızıldeniz","Dicle-Fırat","İndus-Ganj","Sarı-Yangtze"],c:1},
{q:"Sümer uygarlığı nerede kurulmuştur?",a:["Mısır","Anadolu","Mezopotamya","Çin"],c:2},
{q:"Hammurabi Kanunları hangi uygarlığa aittir?",a:["Mısır","Babil","Hitit","Asur"],c:1},
{q:"Fenikeliler neyi icat etmiştir?",a:["Tekerlek","Alfabe","Barut","Pusula"],c:1},
{q:"Roma İmparatorluğu'nun batı yarısı kaç yılında yıkılmıştır?",a:["395","410","455","476"],c:3},
{q:"İpek Yolu hangi kıtaları bağlıyordu?",a:["Afrika-Avrupa","Asya-Avrupa","Amerika-Avrupa","Asya-Afrika"],c:1},
{q:"Göbeklitepe dünyada bilinen en eski nedir?",a:["Şehir","Tapınak","Mezarlık","Saray"],c:1},
{q:"Altın Küre ödülü hangi alandadır?",a:["Edebiyat","Spor","Sinema ve TV","Müzik"],c:2},
{q:"Hangisi bir savaş sanatıdır?",a:["Origami","Aikido","Bonsai","İkebana"],c:1},
{q:"Dünya'nın en eski üniversitesi hangi ülkededir?",a:["İngiltere","İtalya","Fas","Mısır"],c:2},
{q:"Hangisi bir Türk halk hikayesidir?",a:["Romeo ve Juliet","Ferhat ile Şirin","Hamlet","Antigone"],c:1},
{q:"NBA'de en çok şampiyonluk kazanan takım hangisidir?",a:["Lakers","Celtics","Bulls","Warriors"],c:1},
{q:"Hangisi bir çağdaş sanat akımıdır?",a:["Gotik","Pop Art","Romanik","Barok"],c:1},
{q:"Efes Celsus Kütüphanesi kaç yılında inşa edildi?",a:["MS 100","MS 135","MS 200","MS 250"],c:1},
{q:"Hangisi bir yönetmen değildir?",a:["Kubrick","Hitchcock","Hemingway","Coppola"],c:2},
{q:"Maratona adını veren savaş hangi ülkede yapıldı?",a:["İtalya","Türkiye","Yunanistan","Mısır"],c:2},
{q:"Hangisi bir geleneksel Japon tiyatrosudur?",a:["Kabuki","Flamenco","Opera","Bale"],c:0},
{q:"Grammy ödülü hangi alandadır?",a:["Sinema","Edebiyat","Müzik","Tiyatro"],c:2},
{q:"Hangisi dünyaca ünlü bir Türk edebiyatçıdır?",a:["Tolstoy","Elif Şafak","Hugo","Dickens"],c:1},
{q:"Usain Bolt hangi mesafede dünya rekoru kırmıştır?",a:["200m","400m","100m","800m"],c:2},
{q:"Hangisi bir heykel türüdür?",a:["Fresk","Rölyef","Mozaik","Vitray"],c:1},
{q:"İpek Yolu nereden nereye uzanırdı?",a:["Roma-Mısır","Çin-Avrupa","Hindistan-Afrika","Japonya-Rusya"],c:1},
{q:"Hangisi bir Türk destanı değildir?",a:["Manas","Oğuz Kağan","İlyada","Ergenekon"],c:2},
{q:"Wimbledon turnuvası hangi yüzeyde oynanır?",a:["Toprak","Çim","Sert zemin","Halı"],c:1},
{q:"Hangisi bir bale yapıtıdır?",a:["Carmen","Kuğu Gölü","Boheme","Tosca"],c:1},
{q:"Cannes Film Festivali hangi ülkede düzenlenir?",a:["İtalya","İspanya","Fransa","Almanya"],c:2},
{q:"Hangisi Osmanlı döneminde yazılmış bir eserdir?",a:["İlyada","Leyla ile Mecnun","Don Kişot","Hamlet"],c:1},
{q:"Modern pentatlonda kaç disiplin vardır?",a:["3","4","5","6"],c:2},
{q:"Hangisi bir Türk sinema ödülüdür?",a:["Oscar","BAFTA","Altın Portakal","Cannes Palmiye"],c:2},
{q:"Rönesans hangi yüzyılda başlamıştır?",a:["12.","13.","14.","15."],c:2},
{q:"Hangisi bir buz dansı figürüdür?",a:["Libre","Twist","Twizzle","Rumba"],c:2},
{q:"Dünya'nın en çok ziyaret edilen müzesi hangisidir?",a:["British Museum","Met","Louvre","Hermitage"],c:2},
{q:"Hangisi bir Türk mimarıdır?",a:["Gaudi","Mimar Sinan","Le Corbusier","Frank Lloyd Wright"],c:1}
],
very_hard:[
{q:"Yang-Mills teorisi neyle ilgilidir?",a:["Ayar alanları","Kütle çekim","Termodinamik","Optik"],c:0},
{q:"Poincaré konjektürünü kim kanıtladı?",a:["Andrew Wiles","Grigori Perelman","Terence Tao","Peter Scholze"],c:1},
{q:"Karanlık enerji evrenin yüzde kaçıdır?",a:["5","27","68","95"],c:2},
{q:"Hawking radyasyonu nereden yayılır?",a:["Güneş","Kara delik","Nötron yıldızı","Pulsar"],c:1},
{q:"Renormalizasyon hangi teoride kullanılır?",a:["Kuantum alan teorisi","Görelilik","Klasik mekanik","Termodinamik"],c:0},
{q:"Fermat'ın son teoremini kim kanıtladı?",a:["Euler","Gauss","Andrew Wiles","Ramanujan"],c:2},
{q:"Bell eşitsizliği neyi test eder?",a:["Yerel gerçekçilik","Enerji korunumu","Kütle korunumu","Süperpozisyon"],c:0},
{q:"Kozmolojik sabit neyi temsil eder?",a:["Genişleme hızı","Karanlık enerji yoğunluğu","Kütle çekim","Işık hızı"],c:1},
{q:"AdS/CFT eşleşmesi kime aittir?",a:["Witten","Maldacena","Hawking","Penrose"],c:1},
{q:"Türkiye'nin ilk atom reaktörü nerede?",a:["Ankara-Çekmece","İstanbul-Çekmece","Mersin-Akkuyu","Sinop"],c:1},
{q:"QCD'de renk yükü kaç çeşittir?",a:["2","3","4","6"],c:1},
{q:"Noether teoremi neyi bağlar?",a:["Simetri ve korunum yasaları","Kütle ve enerji","Hız ve ivme","Basınç ve hacim"],c:0},
{q:"Gödel'in eksiklik teoremi neyle ilgilidir?",a:["Matematik","Fizik","Kimya","Biyoloji"],c:0},
{q:"'Olmaz olmaz deme olmaz olmaz' ne demektir?",a:["Olmaz de","Hiçbir şeyi imkansız görme","Her şey olur","Olur de"],c:1},
{q:"'Çoğu zarar azı karar' ne demektir?",a:["Az ye","Her şeyin fazlası zararlıdır","Çok al","Az harca"],c:1},
{q:"Riemann hipotezi neyle ilgilidir?",a:["Asal sayılar","Geometri","Topoloji","İstatistik"],c:0},
{q:"Dirac denklemi neyi tanımlar?",a:["Rölativistik kuantum","Klasik mekanik","Termodinamik","Optik"],c:0},
{q:"Lagrange noktaları neyi belirler?",a:["Çekim dengesi","Manyetik alan","Elektrik alan","Işık yolu"],c:0},
{q:"Topological insulator ne demektir?",a:["Yüzey iletken iç yalıtkan","Tam iletken","Tam yalıtkan","Yarı iletken"],c:0},
{q:"İlk kuantum bilgisayarı hangi şirket yaptı?",a:["Google","IBM","Microsoft","Intel"],c:1},
{q:"Kip-Thorne hangi alanda Nobel aldı?",a:["Kuantum","Yerçekimi dalgaları","Parçacık fiziği","Kozmoloji"],c:1},
{q:"Pablo Picasso'nun 'Guernica' tablosu hangi savaşı konu alır?",a:["I. Dünya Savaşı","İspanya İç Savaşı","II. Dünya Savaşı","Kore Savaşı"],c:1},
{q:"Usain Bolt 100 metre dünya rekorunu kaç saniyeyle kırdı?",a:["9.58","9.69","9.72","9.85"],c:0},
{q:"Piri Reis Haritası hangi yüzyıla aittir?",a:["14.","15.","16.","17."],c:2},
{q:"'Saatleri Ayarlama Enstitüsü' kimin eseridir?",a:["Ahmet Hamdi Tanpınar","Yakup Kadri","Halit Ziya","Reşat Nuri"],c:0},
{q:"Frida Kahlo hangi ülkeli bir ressamdır?",a:["İspanya","Arjantin","Meksika","Brezilya"],c:2},
{q:"Wolfgang Amadeus Mozart kaç yaşında vefat etmiştir?",a:["31","35","40","45"],c:1},
{q:"Nikola Tesla hangi alanda öncüdür?",a:["Alternatif akım","Doğru akım","Nükleer enerji","Buhar makinesi"],c:0},
{q:"İlk Türk romanı hangisidir?",a:["Taaşşuk-ı Talat ve Fitnat","İntibah","Araba Sevdası","Sergüzeşt"],c:0},
{q:"Vincent van Gogh'un en ünlü tablosu hangisidir?",a:["Mona Lisa","Çığlık","Yıldızlı Gece","Guernica"],c:2},
{q:"Naim Süleymanoğlu olimpiyat altın madalyası kazanmıştır?",a:["Evet, 1","Evet, 2","Evet, 3","Hayır"],c:2},
{q:"Kapadokya hangi bölgededir?",a:["Ege","Akdeniz","İç Anadolu","Karadeniz"],c:2},
{q:"Bach hangi dönemin bestecisidir?",a:["Rönesans","Barok","Klasik","Romantik"],c:1},
{q:"Marie Curie hangi iki alanda Nobel almıştır?",a:["Fizik ve Kimya","Fizik ve Tıp","Kimya ve Edebiyat","Tıp ve Barış"],c:0},
{q:"Niagara Şelalesi hangi ülkeler arasındadır?",a:["Brezilya-Arjantin","ABD-Kanada","Meksika-ABD","Zambiya-Zimbabve"],c:1},
{q:"Angel Şelalesi hangi ülkededir?",a:["Brezilya","Kolombiya","Venezuela","Peru"],c:2},
{q:"Gondwana neyi ifade eder?",a:["Eski kuzey süper kıtası","Eski güney süper kıtası","İlk okyanus","İlk atmosfer"],c:1},
{q:"Laurasia neyi ifade eder?",a:["Eski güney kıtası","Eski kuzey süper kıtası","İlk göl","İlk dağ"],c:1},
{q:"Rocky Dağları hangi kıtadadır?",a:["Güney Amerika","Avrupa","Asya","Kuzey Amerika"],c:3},
{q:"Atlas Dağları hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Ural Dağları hangi kıtaları ayırır?",a:["Avrupa-Afrika","Avrupa-Asya","Asya-Amerika","Asya-Afrika"],c:1},
{q:"Vinson Dağı hangi kıtanın en yüksek dağıdır?",a:["Avustralya","Güney Amerika","Avrupa","Antarktika"],c:3},
{q:"Kosciuszko Dağı hangi kıtanın en yüksek dağıdır?",a:["Avustralya","Güney Amerika","Antarktika","Avrupa"],c:0},
{q:"Elbrus Dağı hangi kıtanın en yüksek dağıdır?",a:["Asya","Kuzey Amerika","Avrupa","Afrika"],c:2},
{q:"Pasifik Okyanusu dünya yüzeyinin yüzde kaçını kaplar?",a:["15","22","30","46"],c:2},
{q:"Sargasso Denizi hangi okyanustadır?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Mariana Çukuru yaklaşık kaç metre derindir?",a:["5000","8000","11000","15000"],c:2},
{q:"Dünya'nın en büyük adası hangisidir?",a:["Madagaskar","Borneo","Grönland","Sumatra"],c:2},
{q:"Dünya'nın en yüksek şelalesi hangisidir?",a:["Niagara","Victoria","Angel","İguazu"],c:2},
{q:"'Aç ayı oynamaz' ne demektir?",a:["Ayı besle","Karşılığı olmadan çalışılmaz","Ayı izle","Oyun oyna"],c:1},
{q:"'Nerde hareket orda bereket' ne demektir?",a:["Hareket et","Çalışan bereketini bulur","Bereket getir","Dur"],c:1},
{q:"'Denizden çıkmış balığa benzemek' ne demektir?",a:["Balık tut","Şaşkın ve çaresiz kalmak","Yüz","Denize git"],c:1},
{q:"'Kendi düşen ağlamaz' ne demektir?",a:["Ağlama","Hatasının sonucuna kişi katlanır","Düşme","Koş"],c:1},
{q:"Witten M-teorisinde kaç boyut var?",a:["10","11","12","26"],c:1},
{q:"Birch ve Swinnerton-Dyer konjektürü neyle ilgili?",a:["Eliptik eğriler","Asal sayılar","Topoloji","Grafik"],c:0},
{q:"Navier-Stokes problemi ne tür bir problemdir?",a:["Milenyum","Hilbert","Fields","Abel"],c:0},
{q:"Holografik ilke kime atfedilir?",a:["Bekenstein-'t Hooft","Einstein","Hawking","Penrose"],c:0},
{q:"ER=EPR konjektürü neyi bağlar?",a:["Solucan deliği ve dolanıklık","Kütle ve enerji","Hız ve ivme","Foton ve elektron"],c:0},
{q:"Feza Gürsey neyle tanınır?",a:["Simetri grupları","Sicim teorisi","Kara delik","Kozmoloji"],c:0},
{q:"Hodge konjektürü hangi milenyum problemidir?",a:["6.","1.","3.","7."],c:0},
{q:"İlk kuantum bilgisayar şirketi hangisidir?",a:["Google","IBM","Microsoft","Intel"],c:1},
{q:"Penrose CCC modeli neyi önerir?",a:["Döngüsel evren","Tek evren","Çoklu evren","Durgun evren"],c:0},
{q:"Cahit Arf hangi matematiksel kavramla tanınır?",a:["Arf değişmezi","Arf denklemi","Arf teoremi","Arf fonksiyonu"],c:0},
{q:"Oktay Sinanoğlu hangi alanda çalışmıştır?",a:["Fizik","Kuantum kimyası","Biyoloji","Astronomi"],c:1},
{q:"Shor algoritması ne yapar?",a:["Faktorizasyon","Sıralama","Arama","Optimizasyon"],c:0},
{q:"Calabi-Yau manifoldu nerede kullanılır?",a:["Sicim teorisi","Görelilik","Termodinamik","Optik"],c:0},
{q:"Bekenstein-Hawking formülü neyi verir?",a:["Kara delik entropisi","Kütle","Yarıçap","Sıcaklık"],c:0},
{q:"Ramanujan'ın 1729 sayısı neden özeldir?",a:["İki küpün toplamı 2 farklı yol","Asal","Fibonacci","Mükemmel sayı"],c:0},
{q:"Kolmogorov karmaşıklığı neyi ölçer?",a:["Bilgi sıkıştırılabilirliği","Hesaplama zamanı","Bellek","Bant genişliği"],c:0},
{q:"İnflaton alanı neyi sürükler?",a:["Kozmik enflasyon","Karanlık enerji","Kütle çekim","Manyetik alan"],c:0},
{q:"Sachdev-Ye-Kitaev modeli neyi tanımlar?",a:["Kuantum kaos","Süper akışkan","Süper iletken","Bose-Einstein"],c:0},
{q:"Grossman hangi alanda Nobel aldı?",a:["Fizik","Kimya","Tıp","Edebiyat"],c:0},
{q:"Türk matematikçi Cahit Arf kaç yılında doğmuştur?",a:["1910","1920","1930","1940"],c:0},
{q:"Maldacena konjektürü (AdS/CFT) kaç boyut eşler?",a:["3-4","4-5","5-10","10-11"],c:1},
{q:"Langlands programı neyi birleştirir?",a:["Sayı teorisi ve geometri","Fizik ve kimya","Biyoloji ve matematik","Astronomi ve fizik"],c:0},
{q:"Thurston geometrizasyon neyi sınıflar?",a:["3-manifoldlar","Düğüm","Grafik","Matris"],c:0},
{q:"Kitaev topolojik kuantum kodu nedir?",a:["Hata düzeltme","Şifreleme","Sıkıştırma","İletişim"],c:0},
{q:"Kontsevich neyle Fields Madalyası aldı?",a:["Deformasyon kuantizasyonu","Asal sayı","Topoloji","Grafik"],c:0},
{q:"Grothendieck hangi alanda çığır açtı?",a:["Cebirsel geometri","Topoloji","Analiz","İstatistik"],c:0},
{q:"P=NP problemi hangi alana aittir?",a:["Hesaplama karmaşıklığı","Cebir","Geometri","İstatistik"],c:0},
{q:"Dark photon nedir?",a:["Karanlık madde taşıyıcı adayı","Foton antiparçacık","X-ışını","Gama ışını"],c:0},
{q:"Weinberg-Salam modeli neyi birleştirir?",a:["Elektrozayıf kuvvet","Güçlü+zayıf","Dört kuvvet","Kütle çekim+EM"],c:0},
{q:"Penrose-Hawking tekillik teoremleri neyi kanıtlar?",a:["Tekillik kaçınılmaz","Kara delik yok","Evren sonsuz","Işık hızı değişir"],c:0},
{q:"'Her şeyin bir vakti var' atasözü neyi ifade eder?",a:["Zaman önemli","Her işin uygun zamanı vardır sabırlı ol","Vakit nakit","Acele et"],c:1},
{q:"'Körün istediği bir göz Allah verdi iki göz' ne demektir?",a:["Göz tedavisi","Beklentinin üzerinde karşılık bulmak","Göz doktoru","İki göz iyi"],c:1},
{q:"'Su testisi su yolunda kırılır' ne demektir?",a:["Testi al","Sürekli tehlikeyle uğraşan sonunda zarar görür","Su iç","Yol yap"],c:1},
{q:"'Dostlar alışverişte görsün' ne demektir?",a:["Alışveriş yap","Görünüşte yapılan göstermelik iş","Dost edin","Market git"],c:1},
{q:"'Dikensiz gül olmaz' ne demektir?",a:["Gül dik","Her güzel şeyin bir zorluğu vardır","Diken topla","Bahçe yap"],c:1},
{q:"'Alçak uçan yüksekten uçar' ne demektir?",a:["Uç","Mütevazı olan gerçek başarıya ulaşır","Yüksel","Alçal"],c:1},
{q:"'Üç kağıtçıya aldanmak' ne demektir?",a:["Kağıt al","Dolandırıcılığa kanmak","Üç say","Kağıt yaz"],c:1},
{q:"'Astarı yüzünden pahalı olmak' ne demektir?",a:["Pahalı al","İşin maliyetinin asıldan fazla olması","Kumaş al","Yüz yıka"],c:1},
{q:"'Abayı yakmak' ne demektir?",a:["Ateş yak","Birine çok aşık olmak","Elbise yak","Isın"],c:1},
{q:"'Çam sakızı çoban armağanı' ne demektir?",a:["Sakız çiğne","Değeri az ama gönülden verilen hediye","Çoban ol","Armut ye"],c:1},
{q:"'Deve kuşu gibi başını kuma gömmek' ne demektir?",a:["Deve bin","Gerçeklerden kaçmak","Kum at","Kuş izle"],c:1},
{q:"'İpe sapa gelmemek' ne demektir?",a:["İp atla","Düzensiz ve kuralsız olmak","Sap tutmak","İp bağla"],c:1},
{q:"'Atı alan Üsküdar'ı geçti' ne demektir?",a:["At bin","Fırsat kaçtı, artık çok geç","Üsküdar'a git","At sat"],c:1},
{q:"'Kesenin ağzını açmak' ne demektir?",a:["Kese al","Bol bol para harcamaya başlamak","Ağzını aç","Kese dik"],c:1},
{q:"'Kulağına küpe olmak' ne demektir?",a:["Küpe tak","Yaşanılan olaydan ders almak","Kulak ver","Küpe al"],c:1},
{q:"'Nalıncı keseri gibi kendine yontmak' ne demektir?",a:["Kes","Her işi kendi çıkarına göre yapmak","Yont","Nalın yap"],c:1},
{q:"'Pirince giderken evdeki bulgurdan olmak' ne demektir?",a:["Pirinç al","Daha iyisini ararken elindekini kaybetmek","Bulgur ye","Pirince git"],c:1},
{q:"'Saman altından su yürütmek' ne demektir?",a:["Su taşı","Gizlice iş çevirmek","Saman al","Su ver"],c:1},
{q:"'Tabanları yağlamak' ne demektir?",a:["Yağ sür","Gizlice kaçmak","Ayak yıka","Yağ al"],c:1},
{q:"'Ağzı süt kokmak' ne demektir?",a:["Süt iç","Çok genç ve tecrübesiz olmak","Ağız yıka","Süt al"],c:1},
{q:"'Kabak tadı vermek' ne demektir?",a:["Kabak ye","Bir şeyin usandırıcı hale gelmesi","Tat ver","Kabak dik"],c:1},
{q:"'Pişmiş aşa su katmak' ne demektir?",a:["Yemek yap","Olmuş bitmiş işi bozmak","Su koy","Aş ye"],c:1},
{q:"'Yelkenleri suya indirmek' ne demektir?",a:["Yelken aç","Pes etmek, boyun eğmek","Yüz","Gemi sür"],c:1},
{q:"'Devede kulak kalmak' ne demektir?",a:["Deve dinle","Çok az ve önemsiz olmak","Kulak ver","Deve sat"],c:1},
{q:"'Etekleri zil çalmak' ne demektir?",a:["Zil çal","Çok sevinmek","Etek giy","Zil al"],c:1},
{q:"'Gözden düşmek' ne demektir?",a:["Göz kapat","Değerini ve itibarını kaybetmek","Düşmek","Göz aç"],c:1},
{q:"'İncir çekirdeğini doldurmaz' ne demektir?",a:["İncir ye","Çok küçük ve önemsiz olmak","Çekirdek at","İncir topla"],c:1},
{q:"'Kaşıkla verip sapıyla göz çıkarmak' ne demektir?",a:["Kaşık ver","Azıcık iyilik edip çok kötülük yapmak","Göz kapat","Sap tut"],c:1},
{q:"'Balık kavağa çıkınca' ne demektir?",a:["Balık tut","Asla, imkansız","Kavak dik","Balık ye"],c:1},
{q:"'Araba devrilince yol gösteren çok olur' ne demektir?",a:["Araba sür","İş olup bittikten sonra akıl veren çok olur","Yol sor","Araba al"],c:1},
{q:"'Bin bilsen de bir bilene danış' ne demektir?",a:["Bil","Ne kadar bilgili olursan ol tecrübelilere danış","Danış","Sor"],c:1},
{q:"Hangisi bir postmodern romancıdır?",a:["Tolstoy","Dostoyevski","Italo Calvino","Hugo"],c:2},
{q:"Stravinsky hangi müzik döneminin bestecisidir?",a:["Barok","Klasik","Romantik","Modern"],c:3},
{q:"Hangisi bir felsefe akımıdır?",a:["Kübizm","Fovizm","Varoluşçuluk","Dadaizm"],c:2},
{q:"Bir futbol takımında toplam kaç oyuncu forma giyebilir?",a:["16","18","20","23"],c:1},
{q:"Hangisi bir Japon savaş sanatı değildir?",a:["Kendo","Sumo","Capoeira","Jujitsu"],c:2},
{q:"Dünya'nın en pahalı tablosu kime aittir?",a:["Picasso","Da Vinci","Van Gogh","Monet"],c:1},
{q:"Hangisi bir edebiyat ödülüdür?",a:["Grammy","Emmy","Booker","Tony"],c:2},
{q:"Machu Picchu hangi uygarlığa aittir?",a:["Aztek","Maya","İnka","Olmek"],c:2},
{q:"Hangisi bir çağdaş dans türüdür?",a:["Menuet","Vals","Kontemporer","Polka"],c:2},
{q:"F1'de Monaco Grand Prix hangi şehirde yapılır?",a:["Nice","Cannes","Monte Carlo","Marsilya"],c:2},
{q:"Hangisi bir Türk bilim insanı değildir?",a:["Aziz Sancar","Gazi Yaşargil","Marie Curie","Cahit Arf"],c:2},
{q:"Dünya Sağlık Örgütü hangi yıl kuruldu?",a:["1945","1948","1951","1955"],c:1},
{q:"Hangisi bir sinema ödülü değildir?",a:["Oscar","BAFTA","Pulitzer","César"],c:2},
{q:"Berlin Film Festivali'nin büyük ödülü nedir?",a:["Altın Palmiye","Altın Aslan","Altın Ayı","Altın Küre"],c:2}
]
"""

_QUESTIONS_YETISKIN = r"""
easy:[
{q:"Türkiye'nin başkenti neresidir?",a:["İstanbul","Ankara","İzmir","Bursa"],c:1},
{q:"Suyun kimyasal formülü nedir?",a:["CO2","H2O","O2","NaCl"],c:1},
{q:"DNA'nın açılımı nedir?",a:["Deoksiribo Nükleik Asit","Direk Nükleer Asit","Dünya Nükleer Ağı","Dernek Araştırma"],c:0},
{q:"E=mc² formülü kime aittir?",a:["Newton","Einstein","Bohr","Planck"],c:1},
{q:"Periyodik tablonun ilk elementi nedir?",a:["Helyum","Hidrojen","Lityum","Karbon"],c:1},
{q:"Osmanlı Devleti kaç yılında kurulmuştur?",a:["1071","1243","1299","1326"],c:2},
{q:"İstanbul'un fethi kaç yılındadır?",a:["1071","1389","1453","1517"],c:2},
{q:"Işık hızı yaklaşık kaç km/s'dir?",a:["100.000","200.000","300.000","400.000"],c:2},
{q:"Güneş sistemimizdeki en büyük gezegen hangisidir?",a:["Satürn","Jüpiter","Uranüs","Neptün"],c:1},
{q:"Newton'un ikinci yasası nedir?",a:["F=ma","E=mc²","PV=nRT","V=IR"],c:0},
{q:"Atatürk'ün doğum yılı kaçtır?",a:["1878","1880","1881","1883"],c:2},
{q:"Cumhuriyet ne zaman ilan edilmiştir?",a:["1920","1921","1922","1923"],c:3},
{q:"Fransa'nın başkenti neresidir?",a:["Londra","Berlin","Paris","Roma"],c:2},
{q:"Almanya'nın başkenti neresidir?",a:["Viyana","Berlin","Münih","Hamburg"],c:1},
{q:"İtalya'nın başkenti neresidir?",a:["Madrid","Roma","Atina","Lizbon"],c:1},
{q:"Japonya'nın başkenti neresidir?",a:["Pekin","Seul","Tokyo","Osaka"],c:2},
{q:"Brezilya'nın başkenti neresidir?",a:["Rio","Sao Paulo","Brasilia","Salvador"],c:2},
{q:"Avustralya'nın başkenti neresidir?",a:["Sidney","Melbourne","Canberra","Brisbane"],c:2},
{q:"Kanada'nın başkenti neresidir?",a:["Toronto","Vancouver","Ottawa","Montreal"],c:2},
{q:"ABD'nin başkenti neresidir?",a:["New York","Los Angeles","Washington","Chicago"],c:2},
{q:"Hindistan'ın başkenti neresidir?",a:["Mumbai","Kalküta","Yeni Delhi","Goa"],c:2},
{q:"Mısır'ın başkenti neresidir?",a:["İskenderiye","Kahire","Bağdat","Tunus"],c:1},
{q:"Güney Kore'nin başkenti neresidir?",a:["Tokyo","Pekin","Seul","Taipei"],c:2},
{q:"İsviçre'nin başkenti neresidir?",a:["Zürih","Cenevre","Bern","Basel"],c:2},
{q:"Avusturya'nın başkenti neresidir?",a:["Münih","Viyana","Prag","Budapeşte"],c:1},
{q:"Polonya'nın başkenti neresidir?",a:["Prag","Varşova","Budapeşte","Bükreş"],c:1},
{q:"Norveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Kopenhag","Oslo"],c:3},
{q:"İsveç'in başkenti neresidir?",a:["Stockholm","Helsinki","Oslo","Kopenhag"],c:0},
{q:"Portekiz'in başkenti neresidir?",a:["Madrid","Lizbon","Porto","Sevilla"],c:1},
{q:"Dünyanın en uzun nehri hangisidir?",a:["Amazon","Nil","Mississippi","Yangtze"],c:1},
{q:"Dünyanın en yüksek dağı hangisidir?",a:["K2","Ağrı","Everest","Kilimanjaro"],c:2},
{q:"Dünyanın en büyük okyanusu hangisidir?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Türkiye'nin en büyük gölü hangisidir?",a:["Tuz","Beyşehir","Van","Burdur"],c:2},
{q:"Kızılırmak hangi denize dökülür?",a:["Akdeniz","Ege","Karadeniz","Marmara"],c:2},
{q:"Fırat Nehri nereye dökülür?",a:["Karadeniz","Akdeniz","Basra Körfezi","Hazar"],c:2},
{q:"Ağrı Dağı'nın yüksekliği yaklaşık kaçtır?",a:["3137m","4137m","5137m","6137m"],c:2},
{q:"Himalaya Dağları hangi kıtadadır?",a:["Avrupa","Afrika","Asya","Amerika"],c:2},
{q:"And Dağları hangi kıtadadır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Sahra Çölü hangi kıtadadır?",a:["Asya","Avrupa","Afrika","Amerika"],c:2},
{q:"Pangea ne demektir?",a:["İlk deniz","Süper kıta","İlk atmosfer","İlk göl"],c:1},
{q:"'Damlaya damlaya göl olur' ne demektir?",a:["Göle git","Birikim zamanla büyür","Su iç","Yağmur yağar"],c:1},
{q:"'İşleyen demir pas tutmaz' ne demektir?",a:["Demir al","Çalışan sağlıklı kalır","Pas sil","Demir sat"],c:1},
{q:"'Tatlı dil yılanı deliğinden çıkarır' ne demektir?",a:["Yılan yakala","Güzel sözle her kapı açılır","Tatlı ye","Yılan besle"],c:1},
{q:"'Ateş olmayan yerden duman çıkmaz' ne demektir?",a:["Ateş yak","Her söylentinin gerçeklik payı var","Duman çıkar","Yangın söndür"],c:1},
{q:"'Acele işe şeytan karışır' ne demektir?",a:["Şeytan var","Aceleyle hata yapılır","Hızlı koş","Yavaş yürü"],c:1},
{q:"'Armut piş ağzıma düş' ne demektir?",a:["Armut ye","Çalışmadan sonuç beklemek","Meyve al","Armut topla"],c:1},
{q:"'Bal tutan parmağını yalar' ne demektir?",a:["Bal ye","Fırsat değerlendiren kazanır","El yıka","Bal al"],c:1},
{q:"'Sakla samanı gelir zamanı' ne demektir?",a:["Saman al","Her şeyin lazım olacağı gün gelir","Zamanı bekle","Saman yak"],c:1},
{q:"'Yuvarlanan taş yosun tutmaz' ne demektir?",a:["Taş at","Sürekli değişen tutunamaz","Yosun topla","Taş kır"],c:1},
{q:"Shakespeare hangi ülkelidir?",a:["Fransa","Almanya","İtalya","İngiltere"],c:3},
{q:"Rönesans hangi ülkede başlamıştır?",a:["Fransa","İngiltere","İtalya","Almanya"],c:2},
{q:"Sanayi Devrimi hangi ülkede başlamıştır?",a:["Fransa","Almanya","ABD","İngiltere"],c:3},
{q:"Fransız İhtilali hangi yılda olmuştur?",a:["1776","1789","1815","1848"],c:1},
{q:"Marie Curie hangi elementleri keşfetmiştir?",a:["Oksijen-Azot","Polonyum-Radyum","Helyum-Neon","Demir-Bakır"],c:1},
{q:"DNA yapısını kim keşfetmiştir?",a:["Mendel","Darwin","Watson ve Crick","Pasteur"],c:2},
{q:"Tesla hangi alanda çalışmıştır?",a:["Tıp","Alternatif akım","Kimya","Astronomi"],c:1},
{q:"Edison neyi geliştirmiştir?",a:["Telefon","Ampul","Radyo","TV"],c:1},
{q:"Kopernik hangi modeli savunmuştur?",a:["Yer merkezli","Güneş merkezli","Ay merkezli","Yıldız merkezli"],c:1},
{q:"Newton yerçekimini hangi meyveyle keşfetti?",a:["Armut","Portakal","Elma","Erik"],c:2},
{q:"Galile hangi aracı kullanmıştır?",a:["Mikroskop","Teleskop","Pusula","Saat"],c:1},
{q:"Mona Lisa kimin eseridir?",a:["Michelangelo","Raphael","Leonardo da Vinci","Botticelli"],c:2},
{q:"Van Gogh'un ünlü tablosu hangisidir?",a:["Mona Lisa","Yıldızlı Gece","Guernica","Çığlık"],c:1},
{q:"Mozart hangi ülkelidir?",a:["Almanya","İtalya","Avusturya","Fransa"],c:2},
{q:"Beethoven hangi ülkelidir?",a:["Avusturya","Almanya","İtalya","Fransa"],c:1},
{q:"Olimpiyat oyunları kaç yılda bir düzenlenir?",a:["2","3","4","5"],c:2},
{q:"FIFA Dünya Kupası en çok kazanan ülke hangisidir?",a:["Almanya","Arjantin","İtalya","Brezilya"],c:3},
{q:"İnsan vücudundaki en büyük organ hangisidir?",a:["Kalp","Karaciğer","Deri","Beyin"],c:2},
{q:"Hangisi bir greenhouse gazı değildir?",a:["CO2","Metan","Argon","N2O"],c:2},
{q:"Ozon tabakası atmosferin hangi katmanındadır?",a:["Troposfer","Stratosfer","Mezosfer","Termosfer"],c:1},
{q:"İstanbul Boğazı hangi denizleri birleştirir?",a:["Ege-Marmara","Karadeniz-Marmara","Akdeniz-Ege","Karadeniz-Ege"],c:1},
{q:"Panama Kanalı hangi okyanusları birleştirir?",a:["Atlas-Hint","Pasifik-Atlas","Hint-Pasifik","Atlas-Arktik"],c:1},
{q:"Süveyş Kanalı hangi ülkededir?",a:["Türkiye","İsrail","Irak","Mısır"],c:3},
{q:"Hazar Denizi aslında nedir?",a:["Deniz","Okyanus","Göl","Kanal"],c:2},
{q:"Orhan Pamuk Nobel ödülünü hangi yıl almıştır?",a:["2004","2005","2006","2008"],c:2},
{q:"Aziz Sancar hangi alanda Nobel aldı?",a:["Fizik","Kimya","Tıp","Barış"],c:1},
{q:"Naim Süleymanoğlu hangi sporda başarılıdır?",a:["Güreş","Halter","Boks","Atletizm"],c:1},
{q:"Danimarka'nın başkenti neresidir?",a:["Oslo","Helsinki","Stockholm","Kopenhag"],c:3},
{q:"Finlandiya'nın başkenti neresidir?",a:["Oslo","Stockholm","Helsinki","Kopenhag"],c:2},
{q:"Çekya'nın başkenti neresidir?",a:["Bratislava","Varşova","Budapeşte","Prag"],c:3},
{q:"Romanya'nın başkenti neresidir?",a:["Budapeşte","Sofya","Bükreş","Belgrad"],c:2},
{q:"Bulgaristan'ın başkenti neresidir?",a:["Bükreş","Belgrad","Sofya","Atina"],c:2},
{q:"Yunanistan'ın başkenti neresidir?",a:["İstanbul","Selanik","Atina","Girit"],c:2},
{q:"İran'ın başkenti neresidir?",a:["Bağdat","Tahran","Şam","Kabil"],c:1},
{q:"Arjantin'in başkenti neresidir?",a:["Santiago","Lima","Buenos Aires","Montevideo"],c:2},
{q:"Kolombiya'nın başkenti neresidir?",a:["Lima","Bogota","Quito","Santiago"],c:1},
{q:"Şili'nin başkenti neresidir?",a:["Buenos Aires","Lima","Montevideo","Santiago"],c:3},
{q:"Avogadro sayısı yaklaşık kaçtır?",a:["3.14x10^8","6.02x10^23","6.67x10^-11","9.8"],c:1},
{q:"İspanya'nın başkenti neresidir?",a:["Barselona","Madrid","Lizbon","Sevilla"],c:1},
{q:"Meksika'nın başkenti neresidir?",a:["Havana","Meksiko","Lima","Bogota"],c:1},
{q:"Amazon Nehri hangi okyanusa dökülür?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Tuna Nehri hangi denize dökülür?",a:["Akdeniz","Karadeniz","Baltık","Ege"],c:1},
{q:"Volga Nehri hangi denize dökülür?",a:["Karadeniz","Baltık","Hazar","Akdeniz"],c:2},
{q:"Baykal Gölü hangi ülkededir?",a:["Çin","Moğolistan","Rusya","Kazakistan"],c:2},
{q:"Kilimanjaro hangi ülkededir?",a:["Kenya","Uganda","Tanzanya","Etiyopya"],c:2},
{q:"Irak'ın başkenti neresidir?",a:["Tahran","Şam","Bağdat","Amman"],c:2},
{q:"Küba'nın başkenti neresidir?",a:["Meksiko","Havana","Lima","Bogota"],c:1},
{q:"Büyük Set Resifi hangi ülkededir?",a:["Brezilya","Hindistan","Avustralya","Meksika"],c:2},
{q:"Mariana Çukuru hangi okyanustadır?",a:["Atlas","Hint","Arktik","Pasifik"],c:3},
{q:"Nil Nehri hangi denize dökülür?",a:["Kızıldeniz","Akdeniz","Hint Okyanusu","Atlas Okyanusu"],c:1},
{q:"Tuna Nehri hangi denize dökülür?",a:["Adriyatik","Ege","Karadeniz","Akdeniz"],c:2},
{q:"Ganj Nehri hangi ülkededir?",a:["Çin","Pakistan","Hindistan","Bangladeş"],c:2},
{q:"Kongo Nehri hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Ural Dağları hangi iki kıtayı ayırır?",a:["Asya-Afrika","Avrupa-Afrika","Avrupa-Asya","Asya-Kuzey Amerika"],c:2},
{q:"Kilimanjaro Dağı hangi ülkededir?",a:["Kenya","Uganda","Tanzanya","Etiyopya"],c:2},
{q:"McKinley (Denali) Dağı hangi ülkededir?",a:["Kanada","Rusya","ABD","Meksika"],c:2},
{q:"Okyanusya'nın en büyük ülkesi hangisidir?",a:["Yeni Zelanda","Papua Yeni Gine","Fiji","Avustralya"],c:3},
{q:"'Ayağını yorganına göre uzat' ne demektir?",a:["Yat uyu","İmkanların ölçüsünde harca","Yorgan al","Ayak uzat"],c:1},
{q:"'Damlaya damlaya göl olur' ne demektir?",a:["Göl gez","Küçük birikimler büyük sonuçlar doğurur","Su iç","Damla say"],c:1},
{q:"'Dost kara günde belli olur' ne demektir?",a:["Dost edin","Gerçek dost zor zamanda yanında durur","Kara giy","Gün say"],c:1},
{q:"'El elden üstündür' ne demektir?",a:["El tut","Her zaman daha iyisi vardır","El sık","Üstün ol"],c:1},
{q:"'Gülme komşuna gelir başına' ne demektir?",a:["Gül","Başkasının başına gelene gülme sana da gelebilir","Komşu ziyaret et","Baş eğ"],c:1},
{q:"Hazar Denizi aslında nedir?",a:["Deniz","Okyanus","Göl","Körfez"],c:2},
{q:"Baykal Gölü hangi ülkededir?",a:["Çin","Kazakistan","Moğolistan","Rusya"],c:3},
{q:"Victoria Gölü hangi kıtadadır?",a:["Güney Amerika","Asya","Avrupa","Afrika"],c:3},
{q:"Grönland hangi ülkeye bağlıdır?",a:["Norveç","İzlanda","Danimarka","Kanada"],c:2},
{q:"Antarktika'da hangi ülkenin araştırma üssü yoktur?",a:["Türkiye","Brezilya","Çin","Hindistan"],c:0},
{q:"Atlas Okyanusu hangi iki kıtayı ayırır?",a:["Asya-Afrika","Avrupa-Asya","Amerika-Avrupa/Afrika","Avustralya-Asya"],c:2},
{q:"Meksika Körfezi hangi okyanusa bağlıdır?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Everest Dağı hangi iki ülke sınırındadır?",a:["Hindistan-Çin","Nepal-Çin","Pakistan-Çin","Butan-Nepal"],c:1},
{q:"Sahara Çölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avustralya","Afrika"],c:3},
{q:"Amazon Yağmur Ormanları'nın büyük kısmı hangi ülkededir?",a:["Kolombiya","Peru","Venezuela","Brezilya"],c:3},
{q:"'Bal tutan parmağını yalar' ne demektir?",a:["Bal ye","İşin başındaki kendi çıkarını sağlar","Parmak yala","Bal tut"],c:1},
{q:"'Çalıma dalkavukluk yapma' hangi atasözüdür?",a:["Yağcılık yapma","Ağaca dayanma kurur","Çalıya yaklaşma","Bu bir atasözü değil"],c:3},
{q:"Panama Kanalı hangi iki okyanusu birleştirir?",a:["Atlas-Hint","Pasifik-Hint","Atlas-Pasifik","Arktik-Atlas"],c:2},
{q:"Süveyş Kanalı hangi iki denizi birleştirir?",a:["Karadeniz-Akdeniz","Akdeniz-Kızıldeniz","Kızıldeniz-Hint Okyanusu","Ege-Akdeniz"],c:1},
{q:"Hangisi bir empresyonist ressamdır?",a:["Picasso","Monet","Dalí","Warhol"],c:1},
{q:"Olimpiyat ateşi nerede yakılır?",a:["Roma","Atina","Paris","Londra"],c:1},
{q:"Hangisi bir Türk Nobel ödüllüsüdür?",a:["Yaşar Kemal","Orhan Pamuk","Nazım Hikmet","Cemal Süreya"],c:1},
{q:"Hangisi bir opera bestecisi değildir?",a:["Verdi","Puccini","Chopin","Wagner"],c:2},
{q:"En çok Oscar ödülü alan film hangisidir?",a:["Titanic","Avatar","Ben-Hur","Godfather"],c:2},
{q:"Hangisi bir UNESCO Dünya Mirası değildir?",a:["Göbeklitepe","Efes","Anıtkabir","Troya"],c:2},
{q:"Sürrealizm akımının kurucusu kimdir?",a:["Monet","André Breton","Picasso","Dalí"],c:1},
{q:"Hangisi bir tenis Grand Slam turnuvası değildir?",a:["Wimbledon","Roland Garros","Masters","US Open"],c:2},
{q:"Dünya'nın en büyük adasını hangi ülke yönetir?",a:["Kanada","ABD","Danimarka","İngiltere"],c:2},
{q:"Hangisi bir barok dönem bestecisidir?",a:["Mozart","Beethoven","Vivaldi","Chopin"],c:2},
{q:"İstanbul hangi yılda Avrupa Kültür Başkenti oldu?",a:["2005","2008","2010","2012"],c:2},
{q:"Hangisi bir fotoğrafçılık terimi değildir?",a:["Diyafram","Enstantane","Crescendo","ISO"],c:2},
{q:"Dünya'nın en eski medeniyeti hangisidir?",a:["Mısır","Sümer","Roma","Yunan"],c:1},
{q:"Hangisi bir Türk ozanıdır?",a:["Shakespeare","Pir Sultan Abdal","Goethe","Byron"],c:1},
{q:"Hangisi bir dövüş sanatı değildir?",a:["Judo","Aikido","Pilates","Karate"],c:2},
{q:"Pulitzer ödülü hangi alandadır?",a:["Sinema","Müzik","Gazetecilik ve Edebiyat","Bilim"],c:2},
{q:"Osmanlı İmparatorluğu kaç yıl sürmüştür?",a:["400","500","600","700"],c:2},
{q:"Hangisi bir tiyatro yazarıdır?",a:["Chopin","Molière","Monet","Vivaldi"],c:1},
{q:"Avrupa Futbol Şampiyonası kaç yılda bir yapılır?",a:["2","3","4","5"],c:2},
{q:"Hangisi bir Türk destanıdır?",a:["Kalevala","Nibelungen","Dede Korkut","Beowulf"],c:2},
{q:"Dünya'nın en kalabalık şehri hangisidir?",a:["Pekin","New York","Tokyo","İstanbul"],c:2},
{q:"Hangisi bir müzik aleti ailesi değildir?",a:["Yaylılar","Üflemeliler","Vurmalılar","Çizgiler"],c:3}
],
medium:[
{q:"'Sütten ağzı yanan yoğurdu üfleyerek yer' ne demektir?",a:["Yoğurt ye","Kötü deneyim yaşayan aşırı tedbirli olur","Süt iç","Üfle"],c:1},
{q:"'Bıçak kemiğe dayandı' ne demektir?",a:["Bıçak kes","Tahammülün sonuna gelindi","Kemik kır","Keskin ol"],c:1},
{q:"'Gönül ne kahve ister ne kahvehane' ne demektir?",a:["Kahve iç","Önemli olan dostluk","Kahve yap","Gönül al"],c:1},
{q:"'Lafla peynir gemisi yürümez' ne demektir?",a:["Peynir al","Konuşmakla iş olmaz eylem gerek","Gemi sür","Laf etme"],c:1},
{q:"'Minareyi çalan kılıfını hazırlar' ne demektir?",a:["Minare yap","Kötülük yapan önlemini alır","Kılıf dik","Çalmak kötü"],c:1},
{q:"'Dost kara günde belli olur' ne demektir?",a:["Kara gün","Gerçek dost zor zamanda yanında olur","Dost ara","Gün gelir"],c:1},
{q:"'Sürüden ayrılanı kurt kapar' ne demektir?",a:["Kurt yakala","Topluluktan ayrılan tehlikeye düşer","Sürüye git","Kurt besle"],c:1},
{q:"'Mum dibine ışık vermez' ne demektir?",a:["Mum yak","Kişi yakınlarına fayda sağlayamayabilir","Işık aç","Karanlık"],c:1},
{q:"'Ak akçe kara gün içindir' ne demektir?",a:["Para harca","Zor günler için biriktir","Akçe bul","Kara gün gelir"],c:1},
{q:"'Besle kargayı oysun gözünü' ne demektir?",a:["Karga besle","İyilik yaptığın kötülük yapabilir","Göz kapat","Kov"],c:1},
{q:"'Aşk olmayınca meşk olmaz' ne demektir?",a:["Aşık ol","Sevgi olmadan öğrenim olmaz","Meşk et","Müzik çal"],c:1},
{q:"'Kaz gelecek yerden tavuk esirgenmez' ne demektir?",a:["Kaz besle","Büyük kazanç için küçük harcama yapılır","Tavuk sat","Kaz ye"],c:1},
{q:"'Dervişin fikri neyse zikri de odur' ne demektir?",a:["Dua et","Aklındakini söyler","Derviş ol","Fikir sor"],c:1},
{q:"'Körle yatan şaşı kalkar' ne demektir?",a:["Uyu","Kötü arkadaş kötü alışkanlık verir","Şaşı ol","Gözlük tak"],c:1},
{q:"'Deveye hendek atlatmak' ne demektir?",a:["Deve bin","Zor bir işi yaptırmak","Hendek kaz","Deve sat"],c:1},
{q:"Ohm yasası nedir?",a:["F=ma","E=mc²","V=IR","PV=nRT"],c:2},
{q:"Entropi ne demektir?",a:["Enerji","Düzensizlik ölçüsü","Kuvvet","Hız"],c:1},
{q:"Mendel hangi bitkiyle genetik deneyleri yapmıştır?",a:["Buğday","Bezelye","Domates","Mısır"],c:1},
{q:"İnsan kromozom sayısı kaçtır?",a:["23","44","46","48"],c:2},
{q:"Enzim ne tür bir moleküldür?",a:["Karbonhidrat","Yağ","Protein","Nükleik asit"],c:2},
{q:"Tanzimat Fermanı kaç yılında ilan edilmiştir?",a:["1808","1839","1876","1908"],c:1},
{q:"Kanun-i Esasi kaç yılında ilan edilmiştir?",a:["1839","1856","1876","1908"],c:2},
{q:"II. Meşrutiyet kaç yılında ilan edilmiştir?",a:["1876","1893","1908","1918"],c:2},
{q:"Fransız İhtilali'nin temel ilkeleri nedir?",a:["Güç-Servet-Toprak","Özgürlük-Eşitlik-Kardeşlik","Din-Devlet-Millet","Bilim-Sanat-Ticaret"],c:1},
{q:"Sanayi Devrimi'nin en önemli icadı nedir?",a:["Telgraf","Buhar makinesi","Telefon","Elektrik"],c:1},
{q:"Viyana Kongresi hangi yılda yapılmıştır?",a:["1789","1804","1815","1848"],c:2},
{q:"ABD Bağımsızlık Savaşı hangi yılda başlamıştır?",a:["1765","1775","1789","1800"],c:1},
{q:"Magna Carta hangi yılda imzalanmıştır?",a:["1066","1215","1453","1492"],c:1},
{q:"Ukrayna'nın başkenti neresidir?",a:["Moskova","Minsk","Kiev","Varşova"],c:2},
{q:"Hırvatistan'ın başkenti neresidir?",a:["Belgrad","Ljubljana","Zagreb","Saraybosna"],c:2},
{q:"Sırbistan'ın başkenti neresidir?",a:["Sofya","Bükreş","Zagreb","Belgrad"],c:3},
{q:"Bosna'nın başkenti neresidir?",a:["Zagreb","Belgrad","Saraybosna","Podgorica"],c:2},
{q:"Picasso hangi sanat akımının öncülerindendir?",a:["İzlenimcilik","Kübizm","Sürrealizm","Romantizm"],c:1},
{q:"Dalí hangi sanat akımına aittir?",a:["Kübizm","İzlenimcilik","Sürrealizm","Pop Art"],c:2},
{q:"Vivaldi hangi ülkelidir?",a:["Almanya","Avusturya","Fransa","İtalya"],c:3},
{q:"Çaykovski hangi ülkelidir?",a:["Polonya","Almanya","Avusturya","Rusya"],c:3},
{q:"Verdi hangi müzik türünde eserler vermiştir?",a:["Senfoni","Opera","Konçerto","Sonat"],c:1},
{q:"Mimar Sinan'ın ustalık eseri hangisidir?",a:["Süleymaniye","Selimiye","Sultanahmet","Şehzade"],c:1},
{q:"İbn-i Sina'nın tıp alanındaki eseri hangisidir?",a:["Seyahatname","El-Kanun fi't-Tıp","Cihannüma","Kitab-ül Hind"],c:1},
{q:"Harezmi neyin temelini atmıştır?",a:["Tıp","Cebir","Mimari","Coğrafya"],c:1},
{q:"Cristiano Ronaldo hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:2},
{q:"Lionel Messi hangi ülkelidir?",a:["Brezilya","İspanya","Portekiz","Arjantin"],c:3},
{q:"Roger Federer hangi ülkelidir?",a:["Avusturya","Almanya","İsveç","İsviçre"],c:3},
{q:"Michael Phelps hangi spor dalında ünlüdür?",a:["Atletizm","Boks","Yüzme","Tenis"],c:2},
{q:"Galatasaray UEFA Kupası'nı hangi yıl kazanmıştır?",a:["1998","2000","2002","2004"],c:1},
{q:"Mississippi Nehri hangi okyanusa dökülür?",a:["Pasifik","Atlas","Hint","Arktik"],c:1},
{q:"Ganj Nehri hangi körfeze dökülür?",a:["Basra","Bengal","Aden","Oman"],c:1},
{q:"Yangtze Nehri hangi ülkededir?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"K2 Dağı hangi ülkededir?",a:["Nepal","Çin","Pakistan","Hindistan"],c:2},
{q:"Mont Blanc hangi ülkeler arasındadır?",a:["İsviçre-Avusturya","Fransa-İtalya","İspanya-Fransa","İtalya-Avusturya"],c:1},
{q:"Elbrus Dağı hangi ülkededir?",a:["Türkiye","Gürcistan","Rusya","İran"],c:2},
{q:"Aconcagua hangi kıtanın en yüksek dağıdır?",a:["Avrupa","Asya","Güney Amerika","Afrika"],c:2},
{q:"Viktorya Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Titicaca Gölü hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Kuzey Amerika"],c:2},
{q:"Bering Boğazı hangi kıtaları ayırır?",a:["Avrupa-Afrika","Asya-Kuzey Amerika","Avrupa-Asya","Afrika-Asya"],c:1},
{q:"Cebelitarık Boğazı hangi kıtaları ayırır?",a:["Avrupa-Asya","Asya-Afrika","Avrupa-Afrika","Amerika-Avrupa"],c:2},
{q:"Ural Dağları hangi kıtaları ayırır?",a:["Avrupa-Afrika","Avrupa-Asya","Asya-Amerika","Asya-Afrika"],c:1},
{q:"'Kırk yıllık Kani olur mu Yani' ne demektir?",a:["İsim değiştir","Eski alışkanlıklar değişmez","Kırk yıl bekle","Yeni ol"],c:1},
{q:"'Hamama giren terler' ne demektir?",a:["Hamama git","Bir işe giren zorluğuna katlanır","Terle","Yıkan"],c:1},
{q:"'Bakarsan bağ olur bakmazsan dağ olur' ne demektir?",a:["Bağ dik","İlgilenirsen güzel bakmazsan kötü olur","Dağa çık","Bağ al"],c:1},
{q:"'Davulun sesi uzaktan hoş gelir' ne demektir?",a:["Davul çal","Uzaktan güzel görünen yakından öyle olmayabilir","Uzak dur","Müzik dinle"],c:1},
{q:"'Her yiğidin bir yoğurt yiyişi vardır' ne demektir?",a:["Yoğurt ye","Herkesin kendine has yöntemi var","Yiğit ol","Yoğurt yap"],c:1},
{q:"'Boş çuval ayakta durmaz' ne demektir?",a:["Çuval doldur","Bilgisiz kişi başarısız olur","Çuval at","Ayakta dur"],c:1},
{q:"Mançurya hangi ülkenin tarihî bölgesidir?",a:["Japonya","Kore","Çin","Moğolistan"],c:2},
{q:"Volta Nehri hangi ülkededir?",a:["Nijerya","Gana","Senegal","Mali"],c:1},
{q:"Ob-İrtiş Nehri hangi ülkededir?",a:["Kazakistan","Çin","Rusya","Moğolistan"],c:2},
{q:"Elbruz Dağı hangi ülkededir?",a:["Türkiye","İran","Gürcistan","Rusya"],c:3},
{q:"Mont Blanc hangi iki ülke sınırındadır?",a:["İsviçre-İtalya","Fransa-İtalya","Avusturya-İtalya","Fransa-İsviçre"],c:1},
{q:"Madagaskar hangi okyanustadır?",a:["Atlas","Pasifik","Hint","Arktik"],c:2},
{q:"'Ağaç yaşken eğilir' ne demektir?",a:["Ağaç ek","Eğitim küçükken verilir","Ağaç kes","Yaşla"],c:1},
{q:"'Ak akçe kara gün içindir' ne demektir?",a:["Para harca","Tasarruf zor günler için yapılmalı","Akçe say","Kara gün bul"],c:1},
{q:"'Araba devrilince yol gösteren çok olur' ne demektir?",a:["Araba sür","İş işten geçince akıl veren çoktur","Yol sor","Araba al"],c:1},
{q:"'Atı alan Üsküdar'ı geçti' ne demektir?",a:["At bin","Fırsat çoktan kaçırıldı","Üsküdar git","At yarış"],c:1},
{q:"'Bülbülü altın kafese koymuşlar ah vatanım demiş' ne demektir?",a:["Kafes al","Zenginlik vatan özlemini gidermez","Bülbül besle","Altın al"],c:1},
{q:"Bering Boğazı hangi iki kıtayı ayırır?",a:["Avrupa-Asya","Asya-Kuzey Amerika","Kuzey-Güney Amerika","Afrika-Avrupa"],c:1},
{q:"Cebelitarık Boğazı hangi iki kıtayı ayırır?",a:["Asya-Afrika","Avrupa-Asya","Avrupa-Afrika","Amerika-Avrupa"],c:2},
{q:"Malakka Boğazı hangi iki ülke arasındadır?",a:["Hindistan-Sri Lanka","Endonezya-Malezya","Filipinler-Tayvan","Tayland-Myanmar"],c:1},
{q:"Karakum Çölü hangi ülkededir?",a:["İran","Afganistan","Türkmenistan","Özbekistan"],c:2},
{q:"Gobi Çölü hangi ülkededir?",a:["Kazakistan","Çin/Moğolistan","Rusya","Pakistan"],c:1},
{q:"Mekong Nehri hangi bölgededir?",a:["Orta Doğu","Güney Asya","Güneydoğu Asya","Doğu Avrupa"],c:2},
{q:"İndus Nehri hangi ülkededir?",a:["Hindistan","Bangladeş","Pakistan","Nepal"],c:2},
{q:"'Dağ dağa kavuşmaz insan insana kavuşur' ne demektir?",a:["Dağ tırman","İnsanlar bir gün mutlaka karşılaşır","Dağ sev","İnsan bul"],c:1},
{q:"'Eceli gelen köpek cami duvarına işer' ne demektir?",a:["Köpek besle","Sonu gelen pervasızlaşır","Cami git","Duvar ör"],c:1},
{q:"'Elden gelen öğün olmaz o da vaktinde bulunmaz' ne demektir?",a:["Yemek pişir","Başkasından gelene güvenilmez","El tut","Öğün ye"],c:1},
{q:"'Görünen köy kılavuz istemez' ne demektir?",a:["Köy gez","Belli olan şey için açıklamaya gerek yok","Kılavuz bul","Köy kur"],c:1},
{q:"'Her işte bir hayır vardır' ne demektir?",a:["Hayır yap","Kötü görünen olayların iyi tarafı olabilir","İş yap","Hayır de"],c:1},
{q:"Titicaca Gölü hangi iki ülke sınırındadır?",a:["Brezilya-Arjantin","Şili-Bolivya","Peru-Bolivya","Kolombiya-Ekvador"],c:2},
{q:"Aral Gölü hangi ülkelerdedir?",a:["İran-Türkmenistan","Kazakistan-Özbekistan","Rusya-Kazakistan","Moğolistan-Çin"],c:1},
{q:"Antarktika'da en düşük sıcaklık kaç derece ölçülmüştür?",a:["-78°C","-89.2°C","-56°C","-92°C"],c:1},
{q:"Dünya'nın en derin gölü hangisidir?",a:["Hazar","Victoria","Baykal","Tanganyika"],c:2},
{q:"'İşleyen demir ışıldar' ne demektir?",a:["Demir işle","Sürekli çalışan gelişir ve parlak kalır","Işık yak","Demir ısıt"],c:1},
{q:"'Kaz gelecek yerden tavuk esirgenmez' ne demektir?",a:["Tavuk besle","Büyük gelir bekleniyorsa küçük harcamadan çekinilmez","Kaz al","Tavuk kes"],c:1},
{q:"'Körle yatan şaşı kalkar' ne demektir?",a:["Uyu","Kötü arkadaş kötü alışkanlık verir","Kalk","Gör"],c:1},
{q:"'Lafla peynir gemisi yürümez' ne demektir?",a:["Peynir ye","Sadece konuşmayla iş yapılmaz","Gemi sür","Laf at"],c:1},
{q:"'Minareyi çalan kılıfını hazırlar' ne demektir?",a:["Minare çal","Büyük iş yapacak olan önlem alır","Kılıf dik","Çal"],c:1},
{q:"'Nerede birlik orada dirlik' ne demektir?",a:["Birlik kur","Birlik olan yerde huzur olur","Dirlik bul","Bir ol"],c:1},
{q:"Fırat Nehri hangi ülkelerden geçer?",a:["Türkiye-Suriye-Irak","İran-Irak-Kuveyt","Türkiye-İran-Irak","Suriye-Ürdün-Irak"],c:0},
{q:"Galileo Galilei neyi keşfetmiştir?",a:["Amerika","Jüpiter uyduları","Penisilin","DNA"],c:1},
{q:"Hangisi bir Osmanlı minyatür sanatçısıdır?",a:["Matrakçı Nasuh","Da Vinci","Monet","Rembrandt"],c:0},
{q:"Dünya Kupası'nı en çok kazanan futbol takımı hangisidir?",a:["Almanya","İtalya","Brezilya","Arjantin"],c:2},
{q:"Hangisi bir opera bestecisidir?",a:["Bach","Verdi","Chopin","Liszt"],c:1},
{q:"Troya Antik Kenti hangi ilimizde yer alır?",a:["İzmir","Çanakkale","Balıkesir","Edirne"],c:1},
{q:"Formula 1'de en çok şampiyonluk kazanan pilot kimdir?",a:["Senna","Schumacher","Hamilton","Vettel"],c:2},
{q:"Hangisi bir Türk romanıdır?",a:["Savaş ve Barış","Suç ve Ceza","Çalıkuşu","Don Kişot"],c:2},
{q:"Kremlin hangi ülkededir?",a:["Çin","İngiltere","Rusya","Fransa"],c:2},
{q:"Hangisi bir dans yarışması formatıdır?",a:["Survivor","MasterChef","Dancing with Stars","The Voice"],c:2},
{q:"Uzayda yürüyen ilk kadın astronot kimdir?",a:["Sally Ride","Valentina Tereşkova","Svetlana Savitskaya","Mae Jemison"],c:2},
{q:"Hangisi bir Türk hat sanatçısıdır?",a:["Matisse","Hamid Aytaç","Renoir","Cézanne"],c:1},
{q:"Dünya'nın en uzun köprüsü hangi ülkededir?",a:["ABD","Japonya","Çin","İngiltere"],c:2},
{q:"Hangisi bir müzik festivalidir?",a:["Cannes","Sundance","Eurovision","Oscar"],c:2},
{q:"Pekin Operası hangi ülkenin sanatıdır?",a:["Japonya","Kore","Çin","Vietnam"],c:2},
{q:"Hangisi bir kış olimpiyat sporu değildir?",a:["Kayaklı koşu","Curling","Badminton","Biatlon"],c:2},
{q:"Türkiye'nin ilk olimpiyat madalyası hangi spordandır?",a:["Halter","Güreş","Boks","Atletizm"],c:1},
{q:"Hangisi bir fotoğraf sanatçısıdır?",a:["Ansel Adams","Beethoven","Chopin","Shakespeare"],c:0},
{q:"Super Bowl hangi sporun final maçıdır?",a:["Basketbol","Beyzbol","Amerikan Futbolu","Buz Hokeyi"],c:2},
{q:"Hangisi bir Türk mimari eseridir?",a:["Taj Mahal","Selimiye Camii","Sagrada Familia","Notre Dame"],c:1},
{q:"Milli Mücadele döneminin ünlü kadın kahramanı kimdir?",a:["Halide Edip Adıvar","Sabiha Gökçen","Afet İnan","Latife Hanım"],c:0},
{q:"Hangisi bir Akdeniz yemeğidir?",a:["Sushi","Ramen","Hummus","Dim Sum"],c:2},
{q:"Emmy ödülü hangi alandadır?",a:["Sinema","Televizyon","Müzik","Edebiyat"],c:1},
{q:"Hangisi bir su sporu değildir?",a:["Yelken","Kano","Eskrim","Sörf"],c:2},
{q:"Osmanlı'da ilk matbaa ne zaman kuruldu?",a:["1629","1727","1839","1876"],c:1},
{q:"Hangisi bir müze değildir?",a:["Prado","Hermitage","Wimbledon","Uffizi"],c:2},
{q:"Dünya Atletizm Şampiyonası kaç yılda bir yapılır?",a:["Her yıl","2 yılda","3 yılda","4 yılda"],c:1},
{q:"Hangisi bir Türk filmi yönetmenidir?",a:["Spielberg","Nuri Bilge Ceylan","Tarantino","Scorsese"],c:1},
{q:"Avrupa Birliği'nin merkezi hangi şehirdedir?",a:["Paris","Berlin","Brüksel","Viyana"],c:2},
{q:"Hangisi bir Türk marşıdır?",a:["La Marseillaise","İzmir Marşı","Star Spangled","God Save"],c:1}
],
hard:[
{q:"'Abanoz böceği meşeyi yer' ne demektir?",a:["Böcek yakala","Küçük zarar sürekli olursa büyür","Meşe kes","Böcek besle"],c:1},
{q:"'Dut yemiş bülbüle döndü' ne demektir?",a:["Dut ye","Sessizleşti sustu","Bülbül dinle","Şarkı söyle"],c:1},
{q:"'Çoğu zarar azı karar' ne demektir?",a:["Az ye","Her şeyin fazlası zararlıdır","Çok al","Az harca"],c:1},
{q:"'Her kuşun eti yenmez' ne demektir?",a:["Kuş ye","Herkesle uğraşılmaz","Kuş yakala","Et ye"],c:1},
{q:"'İğneyi kendine çuvaldızı başkasına batır' ne demektir?",a:["İğne batır","Önce kendini eleştir","Dikiş dik","Çuvaldız al"],c:1},
{q:"'Et tırnaktan ayrılmaz' ne demektir?",a:["Et ye","Yakın akrabalar kopmaz","Tırnak kes","Et kes"],c:1},
{q:"'İki cambaz bir ipte oynamaz' ne demektir?",a:["Cambaz ol","Aynı yerde iki lider olmaz","İp atla","Cambaz izle"],c:1},
{q:"'Ava giden avlanır' ne demektir?",a:["Ava git","Kötülük yapan kendisi zarar görür","Avlan","Tuzak kur"],c:1},
{q:"'Su uyur düşman uyumaz' ne demektir?",a:["Su iç","Tetikte ol","Uyu","Düşmanı sev"],c:1},
{q:"'Taşıma su ile değirmen dönmez' ne demektir?",a:["Su taşı","Dışarıdan destek alarak iş sürdürülmez","Değirmen yap","Su getir"],c:1},
{q:"'Karga kekliğe bakıp yürümeye kalkmış' ne demektir?",a:["Karga izle","Taklitçilik zararlıdır","Keklik yakala","Kuş seyret"],c:1},
{q:"'Olmaz olmaz deme olmaz olmaz' ne demektir?",a:["Olmaz de","Hiçbir şeyi imkansız görme","Her şey olur","Olur de"],c:1},
{q:"'Gülü seven dikenine katlanır' ne demektir?",a:["Gül topla","Bir şeyi seven zorluklarına katlanır","Diken batır","Bahçe yap"],c:1},
{q:"'Hazıra dağlar dayanmaz' ne demektir?",a:["Dağa git","Çalışmadan harcanan biter","Hazırla","Dağ aş"],c:1},
{q:"'Yuvayı dişi kuş yapar' ne demektir?",a:["Kuş besle","Evi kadın düzenler","Yuva yap","Kuş izle"],c:1},
{q:"P=NP problemi hangi alana aittir?",a:["Hesaplama karmaşıklığı","Cebir","Geometri","İstatistik"],c:0},
{q:"Shor algoritması ne yapar?",a:["Faktorizasyon","Sıralama","Arama","Optimizasyon"],c:0},
{q:"Calabi-Yau manifoldu nerede kullanılır?",a:["Sicim teorisi","Görelilik","Termodinamik","Optik"],c:0},
{q:"Bekenstein-Hawking formülü neyi verir?",a:["Kara delik entropisi","Kütle","Yarıçap","Sıcaklık"],c:0},
{q:"Ramanujan'ın 1729 sayısı neden özeldir?",a:["İki küpün toplamı 2 farklı yol","Asal","Fibonacci","Mükemmel sayı"],c:0},
{q:"Kolmogorov karmaşıklığı neyi ölçer?",a:["Bilgi sıkıştırılabilirliği","Hesaplama zamanı","Bellek","Bant genişliği"],c:0},
{q:"Weinberg-Salam modeli neyi birleştirir?",a:["Elektrozayıf kuvvet","Güçlü+zayıf","Dört kuvvet","Kütle çekim+EM"],c:0},
{q:"İnflaton alanı neyi sürükler?",a:["Kozmik enflasyon","Karanlık enerji","Kütle çekim","Manyetik alan"],c:0},
{q:"Penrose-Hawking tekillik teoremleri neyi kanıtlar?",a:["Tekillik kaçınılmaz","Kara delik yok","Evren sonsuz","Işık hızı değişir"],c:0},
{q:"Cahit Arf'ın doğum yılı kaçtır?",a:["1910","1920","1930","1940"],c:0},
{q:"Grothendieck hangi alanda çığır açtı?",a:["Cebirsel geometri","Topoloji","Analiz","İstatistik"],c:0},
{q:"Dark photon nedir?",a:["Karanlık madde taşıyıcı adayı","Foton antiparçacık","X-ışını","Gama ışını"],c:0},
{q:"Heisenberg belirsizlik ilkesi ne söyler?",a:["Konum ve momentum kesin ölçülemez","Enerji korunur","Entropi artar","Işık sabit"],c:0},
{q:"Altın oran yaklaşık kaçtır?",a:["1.414","2.718","3.141","1.618"],c:3},
{q:"Higgs bozonu ne sağlar?",a:["Işık","Manyetizma","Kütle","Yerçekimi"],c:2},
{q:"Pauli dışlama ilkesi ne söyler?",a:["İki fermiyonun aynı kuantum hali yok","Enerji kuantumlu","Dalga-parçacık","Belirsizlik"],c:0},
{q:"CRISPR teknolojisi ne için kullanılır?",a:["Gen düzenleme","İlaç üretimi","Görüntüleme","Enerji"],c:0},
{q:"Karanlık madde evrenin yüzde kaçını oluşturur?",a:["5","15","27","68"],c:2},
{q:"Chandrasekhar limiti neyi belirler?",a:["Beyaz cüce kütle sınırı","Kara delik yarıçapı","Nötron yıldızı","Galaksi boyutu"],c:0},
{q:"Standart Model'de kaç temel parçacık var?",a:["12","17","24","36"],c:1},
{q:"Gödel'in eksiklik teoremi neyle ilgilidir?",a:["Matematik","Fizik","Kimya","Biyoloji"],c:0},
{q:"Riemann hipotezi neyle ilgilidir?",a:["Asal sayılar","Geometri","Topoloji","İstatistik"],c:0},
{q:"Dirac denklemi neyi tanımlar?",a:["Rölativistik kuantum","Klasik mekanik","Termodinamik","Optik"],c:0},
{q:"Lagrange noktaları neyi belirler?",a:["Çekim dengesi","Manyetik alan","Elektrik alan","Işık yolu"],c:0},
{q:"Nötron yıldızı ne oluşturur?",a:["Beyaz cüce","Kara delik","Pulsar","Nebula"],c:2},
{q:"Suudi Arabistan'ın başkenti neresidir?",a:["Dubai","Mekke","Riyad","Medine"],c:2},
{q:"Ob Nehri hangi ülkededir?",a:["Çin","Rusya","Kanada","ABD"],c:1},
{q:"Yenisey Nehri hangi ülkededir?",a:["Kanada","Rusya","Çin","Moğolistan"],c:1},
{q:"Lena Nehri hangi ülkededir?",a:["Kanada","Çin","Rusya","ABD"],c:2},
{q:"Nijer Nehri hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Murray Nehri hangi ülkededir?",a:["ABD","Kanada","Avustralya","Yeni Zelanda"],c:2},
{q:"İndus Nehri hangi ülkelerden geçer?",a:["Hindistan-Bangladeş","Çin-Hindistan-Pakistan","Nepal-Hindistan","Çin-Moğolistan"],c:1},
{q:"Mekong Nehri hangi bölgeden geçer?",a:["Orta Doğu","Güneydoğu Asya","Kuzey Afrika","Güney Amerika"],c:1},
{q:"Orinoko Nehri hangi kıtadadır?",a:["Afrika","Asya","Güney Amerika","Avrupa"],c:2},
{q:"Kongo Nehri hangi okyanusa dökülür?",a:["Hint","Pasifik","Atlas","Arktik"],c:2},
{q:"Gobi Çölü hangi ülkelerdedir?",a:["İran-Irak","Çin-Moğolistan","Hindistan-Pakistan","Mısır-Libya"],c:1},
{q:"Atacama Çölü hangi ülkededir?",a:["Arjantin","Peru","Şili","Meksika"],c:2},
{q:"Takla Makan Çölü hangi ülkededir?",a:["Moğolistan","İran","Çin","Pakistan"],c:2},
{q:"Fuji Dağı hangi ülkededir?",a:["Çin","Kore","Japonya","Vietnam"],c:2},
{q:"Vezüv Yanardağı hangi ülkededir?",a:["Yunanistan","Türkiye","İtalya","İspanya"],c:2},
{q:"Tanganyika Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Çad Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Afrika","Avrupa"],c:2},
{q:"Hürmüz Boğazı hangi bölgededir?",a:["Akdeniz","Basra Körfezi","Kızıldeniz","Güneydoğu Asya"],c:1},
{q:"Malakka Boğazı hangi bölgededir?",a:["Orta Doğu","Akdeniz","Güneydoğu Asya","Güney Amerika"],c:2},
{q:"'Denizden çıkmış balığa benzemek' ne demektir?",a:["Balık tut","Şaşkın ve çaresiz kalmak","Yüz","Denize git"],c:1},
{q:"'Kendi düşen ağlamaz' ne demektir?",a:["Ağlama","Hatasının sonucuna kişi katlanır","Düşme","Koş"],c:1},
{q:"'Nerde hareket orda bereket' ne demektir?",a:["Hareket et","Çalışan bereketini bulur","Bereket getir","Dur"],c:1},
{q:"'Aç ayı oynamaz' ne demektir?",a:["Ayı besle","Karşılığı olmadan çalışılmaz","Ayı izle","Oyun oyna"],c:1},
{q:"Transsibirya Demiryolu hangi iki şehri bağlar?",a:["Moskova-Pekin","Moskova-Vladivostok","St.Petersburg-Tokyo","Kiev-Şanghay"],c:1},
{q:"Karadeniz'in tuzluluk oranı neden düşüktür?",a:["Derin olduğu için","Çok sayıda nehir döküldüğü için","Soğuk olduğu için","Kapalı olduğu için"],c:1},
{q:"Çad Gölü hangi kıtadadır?",a:["Asya","Güney Amerika","Avrupa","Afrika"],c:3},
{q:"Patagunya hangi ülkededir?",a:["Şili","Brezilya","Arjantin","Peru"],c:2},
{q:"'Ölmüş eşek kurttan korkmaz' ne demektir?",a:["Eşek al","Her şeyini kaybeden korkusuz olur","Kurt avla","Eşek sür"],c:1},
{q:"'Pilav yiyen kaşığını yanında taşır' ne demektir?",a:["Pilav pişir","İhtiyacını karşılayacak aracı hazırlayan faydalanır","Kaşık al","Çanta taşı"],c:1},
{q:"'Sona kalan dona kalır' ne demektir?",a:["Son ol","Geç kalan zararlı çıkar","Don giy","Bekle"],c:1},
{q:"'Tencere yuvarlanmış kapağını bulmuş' ne demektir?",a:["Yemek pişir","Benzer kişiler birbirini bulur","Kapak ara","Tencere al"],c:1},
{q:"'Üzüm üzüme baka baka kararır' ne demektir?",a:["Üzüm ye","İnsanlar çevresinden etkilenir","Üzüm topla","Bağ kur"],c:1},
{q:"'Yuvarlanan taş yosun tutmaz' ne demektir?",a:["Taş at","Sürekli yer değiştiren birikim yapamaz","Yosun topla","Taş yuvarla"],c:1},
{q:"Zambezi Nehri hangi şelaleyi oluşturur?",a:["Niagara","Angel","Victoria","İguazu"],c:2},
{q:"Orinoko Nehri hangi ülkededir?",a:["Brezilya","Kolombiya","Venezuela","Peru"],c:2},
{q:"Uluğ Bey hangi alandaki çalışmalarıyla tanınır?",a:["Tıp","Astronomi","Kimya","Felsefe"],c:1},
{q:"Kızılırmak Türkiye'nin en uzun nehridir. Nereye dökülür?",a:["Akdeniz","Ege Denizi","Marmara Denizi","Karadeniz"],c:3},
{q:"Dicle Nehri hangi ülkelerden geçer?",a:["Türkiye-Irak","İran-Irak","Suriye-Irak","Türkiye-Suriye"],c:0},
{q:"Büyük Sahra hangi kıtanın en büyük çölüdür?",a:["Asya","Avustralya","Afrika","Güney Amerika"],c:2},
{q:"Atacama Çölü hangi ülkededir?",a:["Peru","Arjantin","Şili","Bolivya"],c:2},
{q:"Himalaya Dağları hangi iki levha çarpışmasıyla oluşmuştur?",a:["Pasifik-Avrasya","Hint-Avrasya","Afrika-Avrasya","Nazca-Güney Amerika"],c:1},
{q:"'Eşeğe altın semer vursan da eşektir' ne demektir?",a:["Eşek al","Değersiz kişi süslense de değişmez","Semer yap","Altın al"],c:1},
{q:"'Havlayana köpek ısırmaz' ne demektir?",a:["Köpek besle","Çok gürültü yapan tehlikeli değildir","Köpek tut","Havla"],c:1},
{q:"'İğneyle kuyu kazmak' ne demektir?",a:["Kuyu kaz","Çok zor ve uzun sürecek iş yapmak","İğne dik","Su çek"],c:1},
{q:"'Kılıç yarası geçer dil yarası geçmez' ne demektir?",a:["Kılıç savaş","Sözle verilen acı fiziksel acıdan daha kalıcıdır","Dil öğren","Yara sar"],c:1},
{q:"'Mart kapıdan baktırır kazma kürek yaktırır' ne demektir?",a:["Mart'ta gez","Mart ayı havası çok değişkendir","Kazma al","Yakacak al"],c:1},
{q:"Okhotsk Denizi hangi ülkenin kıyısındadır?",a:["Çin","Japonya","Kore","Rusya"],c:3},
{q:"Kerelen Nehri hangi ülkededir?",a:["Çin","Rusya","Moğolistan","Kazakistan"],c:2},
{q:"Şatt-ül Arap hangi iki nehrin birleşimidir?",a:["Nil-Mavi Nil","Fırat-Dicle","Ganj-Brahmaputra","İndus-Sutlej"],c:1},
{q:"Van Gölü hangi özelliğiyle bilinir?",a:["Tatlı su gölü","Sodalı göl","Acı su gölü","Tuzlu göl"],c:1},
{q:"'Bir elin nesi var iki elin sesi var' ne demektir?",a:["El çırp","Birlikte çalışmak daha verimlidir","El tut","Ses çıkar"],c:1},
{q:"'Cahile söz anlatmak deveye hendek atlatmaktan zordur' ne demektir?",a:["Deve bin","Bilgisiz birini ikna etmek çok zordur","Hendek kaz","Söz söyle"],c:1},
{q:"Kerguelen Adaları hangi okyanustadır?",a:["Atlas","Pasifik","Arktik","Hint"],c:3},
{q:"Spratly Adaları hangi denizde bulunur?",a:["Akdeniz","Karadeniz","Güney Çin Denizi","Japon Denizi"],c:2},
{q:"Bermuda Üçgeni hangi okyanustadır?",a:["Pasifik","Hint","Arktik","Atlas"],c:3},
{q:"'Sakla samanı gelir zamanı' ne demektir?",a:["Saman topla","Biriktirilen şey bir gün işe yarar","Zaman bekle","Sakla"],c:1},
{q:"'Yel kayadan ne koparır' ne demektir?",a:["Rüzgar es","Güçlü olana güçsüz zarar veremez","Kaya kır","Yel gönder"],c:1},
{q:"Altın Küre ödülü hangi alandadır?",a:["Edebiyat","Spor","Sinema ve TV","Müzik"],c:2},
{q:"Hangisi bir savaş sanatıdır?",a:["Origami","Aikido","Bonsai","İkebana"],c:1},
{q:"Dünya'nın en eski üniversitesi hangi ülkededir?",a:["İngiltere","İtalya","Fas","Mısır"],c:2},
{q:"Hangisi bir Türk halk hikayesidir?",a:["Romeo ve Juliet","Ferhat ile Şirin","Hamlet","Antigone"],c:1},
{q:"NBA'de en çok şampiyonluk kazanan takım hangisidir?",a:["Lakers","Celtics","Bulls","Warriors"],c:1},
{q:"Hangisi bir çağdaş sanat akımıdır?",a:["Gotik","Pop Art","Romanik","Barok"],c:1},
{q:"Efes Celsus Kütüphanesi kaç yılında inşa edildi?",a:["MS 100","MS 135","MS 200","MS 250"],c:1},
{q:"Hangisi bir yönetmen değildir?",a:["Kubrick","Hitchcock","Hemingway","Coppola"],c:2},
{q:"Maratona adını veren savaş hangi ülkede yapıldı?",a:["İtalya","Türkiye","Yunanistan","Mısır"],c:2},
{q:"Hangisi bir geleneksel Japon tiyatrosudur?",a:["Kabuki","Flamenco","Opera","Bale"],c:0},
{q:"Grammy ödülü hangi alandadır?",a:["Sinema","Edebiyat","Müzik","Tiyatro"],c:2},
{q:"Hangisi dünyaca ünlü bir Türk edebiyatçıdır?",a:["Tolstoy","Elif Şafak","Hugo","Dickens"],c:1},
{q:"Usain Bolt hangi mesafede dünya rekoru kırmıştır?",a:["200m","400m","100m","800m"],c:2},
{q:"Hangisi bir heykel türüdür?",a:["Fresk","Rölyef","Mozaik","Vitray"],c:1},
{q:"İpek Yolu nereden nereye uzanırdı?",a:["Roma-Mısır","Çin-Avrupa","Hindistan-Afrika","Japonya-Rusya"],c:1},
{q:"Hangisi bir Türk destanı değildir?",a:["Manas","Oğuz Kağan","İlyada","Ergenekon"],c:2},
{q:"Wimbledon turnuvası hangi yüzeyde oynanır?",a:["Toprak","Çim","Sert zemin","Halı"],c:1},
{q:"Hangisi bir bale yapıtıdır?",a:["Carmen","Kuğu Gölü","Boheme","Tosca"],c:1},
{q:"Cannes Film Festivali hangi ülkede düzenlenir?",a:["İtalya","İspanya","Fransa","Almanya"],c:2}
],
very_hard:[
{q:"Maldacena konjektürü (AdS/CFT) kaç boyut eşler?",a:["3-4","4-5","5-10","10-11"],c:1},
{q:"Langlands programı neyi birleştirir?",a:["Sayı teorisi ve geometri","Fizik ve kimya","Biyoloji ve matematik","Astronomi ve fizik"],c:0},
{q:"Thurston geometrizasyon neyi sınıflar?",a:["3-manifoldlar","Düğüm","Grafik","Matris"],c:0},
{q:"Kitaev topolojik kuantum kodu nedir?",a:["Hata düzeltme","Şifreleme","Sıkıştırma","İletişim"],c:0},
{q:"Navier-Stokes problemi ne tür bir problemdir?",a:["Milenyum","Hilbert","Fields","Abel"],c:0},
{q:"Witten M-teorisinde kaç boyut var?",a:["10","11","12","26"],c:1},
{q:"Birch ve Swinnerton-Dyer konjektürü neyle ilgili?",a:["Eliptik eğriler","Asal sayılar","Topoloji","Grafik"],c:0},
{q:"Penrose CCC modeli neyi önerir?",a:["Döngüsel evren","Tek evren","Çoklu evren","Durgun evren"],c:0},
{q:"Holografik ilke kime atfedilir?",a:["Bekenstein-'t Hooft","Einstein","Hawking","Penrose"],c:0},
{q:"Sachdev-Ye-Kitaev modeli neyi tanımlar?",a:["Kuantum kaos","Süper akışkan","Süper iletken","Bose-Einstein"],c:0},
{q:"ER=EPR konjektürü neyi bağlar?",a:["Solucan deliği ve dolanıklık","Kütle ve enerji","Hız ve ivme","Foton ve elektron"],c:0},
{q:"Feza Gürsey neyle tanınır?",a:["Simetri grupları","Sicim teorisi","Kara delik","Kozmoloji"],c:0},
{q:"Hodge konjektürü hangi milenyum problemidir?",a:["6.","1.","3.","7."],c:0},
{q:"Kontsevich neyle Fields Madalyası aldı?",a:["Deformasyon kuantizasyonu","Asal sayı","Topoloji","Grafik"],c:0},
{q:"Yang-Mills teorisi neyle ilgilidir?",a:["Ayar alanları","Kütle çekim","Termodinamik","Optik"],c:0},
{q:"Poincaré konjektürünü kim kanıtladı?",a:["Andrew Wiles","Grigori Perelman","Terence Tao","Peter Scholze"],c:1},
{q:"Karanlık enerji evrenin yüzde kaçıdır?",a:["5","27","68","95"],c:2},
{q:"Hawking radyasyonu nereden yayılır?",a:["Güneş","Kara delik","Nötron yıldızı","Pulsar"],c:1},
{q:"Renormalizasyon hangi teoride kullanılır?",a:["Kuantum alan teorisi","Görelilik","Klasik mekanik","Termodinamik"],c:0},
{q:"Fermat'ın son teoremini kim kanıtladı?",a:["Euler","Gauss","Andrew Wiles","Ramanujan"],c:2},
{q:"Bell eşitsizliği neyi test eder?",a:["Yerel gerçekçilik","Enerji korunumu","Kütle korunumu","Süperpozisyon"],c:0},
{q:"Kozmolojik sabit neyi temsil eder?",a:["Genişleme hızı","Karanlık enerji yoğunluğu","Kütle çekim","Işık hızı"],c:1},
{q:"AdS/CFT eşleşmesi kime aittir?",a:["Witten","Maldacena","Hawking","Penrose"],c:1},
{q:"QCD'de renk yükü kaç çeşittir?",a:["2","3","4","6"],c:1},
{q:"Noether teoremi neyi bağlar?",a:["Simetri ve korunum yasaları","Kütle ve enerji","Hız ve ivme","Basınç ve hacim"],c:0},
{q:"Topological insulator ne demektir?",a:["Yüzey iletken iç yalıtkan","Tam iletken","Tam yalıtkan","Yarı iletken"],c:0},
{q:"Kip-Thorne hangi alanda Nobel aldı?",a:["Kuantum","Yerçekimi dalgaları","Parçacık fiziği","Kozmoloji"],c:1},
{q:"Milgrom MOND teorisi neye alternatif?",a:["Karanlık madde","Karanlık enerji","Sicim teorisi","Kuantum"],c:0},
{q:"'Abayı yakmak' ne demektir?",a:["Ateş yak","Birine çok aşık olmak","Elbise yak","Isın"],c:1},
{q:"'Çam sakızı çoban armağanı' ne demektir?",a:["Sakız çiğne","Değeri az ama gönülden verilen hediye","Çoban ol","Armut ye"],c:1},
{q:"'Deve kuşu gibi başını kuma gömmek' ne demektir?",a:["Deve bin","Gerçeklerden kaçmak","Kum at","Kuş izle"],c:1},
{q:"'İpe sapa gelmemek' ne demektir?",a:["İp atla","Düzensiz ve kuralsız olmak","Sap tut","İp bağla"],c:1},
{q:"'Atı alan Üsküdar'ı geçti' ne demektir?",a:["At bin","Fırsat kaçtı artık çok geç","Üsküdar'a git","At sat"],c:1},
{q:"'Saman altından su yürütmek' ne demektir?",a:["Su taşı","Gizlice iş çevirmek","Saman al","Su ver"],c:1},
{q:"'Tabanları yağlamak' ne demektir?",a:["Yağ sür","Gizlice kaçmak","Ayak yıka","Yağ al"],c:1},
{q:"'Ağzı süt kokmak' ne demektir?",a:["Süt iç","Çok genç ve tecrübesiz olmak","Ağız yıka","Süt al"],c:1},
{q:"'Kabak tadı vermek' ne demektir?",a:["Kabak ye","Bir şeyin usandırıcı hale gelmesi","Tat ver","Kabak dik"],c:1},
{q:"'Pişmiş aşa su katmak' ne demektir?",a:["Yemek yap","Olmuş bitmiş işi bozmak","Su koy","Aş ye"],c:1},
{q:"'Yelkenleri suya indirmek' ne demektir?",a:["Yelken aç","Pes etmek boyun eğmek","Yüz","Gemi sür"],c:1},
{q:"'Devede kulak kalmak' ne demektir?",a:["Deve dinle","Çok az ve önemsiz olmak","Kulak ver","Deve sat"],c:1},
{q:"'Nalıncı keseri gibi kendine yontmak' ne demektir?",a:["Kes","Her işi kendi çıkarına göre yapmak","Yont","Nalın yap"],c:1},
{q:"'Pirince giderken bulgurdan olmak' ne demektir?",a:["Pirinç al","Daha iyisini ararken eldekini kaybetmek","Bulgur ye","Pirince git"],c:1},
{q:"'Kesenin ağzını açmak' ne demektir?",a:["Kese al","Bol bol para harcamaya başlamak","Ağzını aç","Kese dik"],c:1},
{q:"'Kulağına küpe olmak' ne demektir?",a:["Küpe tak","Yaşanılan olaydan ders almak","Kulak ver","Küpe al"],c:1},
{q:"'Kaşıkla verip sapıyla göz çıkarmak' ne demektir?",a:["Kaşık ver","Azıcık iyilik edip çok kötülük yapmak","Göz kapat","Sap tut"],c:1},
{q:"'Etekleri zil çalmak' ne demektir?",a:["Zil çal","Çok sevinmek","Etek giy","Zil al"],c:1},
{q:"'Gözden düşmek' ne demektir?",a:["Göz kapat","Değerini kaybetmek","Düşmek","Göz aç"],c:1},
{q:"'İncir çekirdeğini doldurmaz' ne demektir?",a:["İncir ye","Çok küçük ve önemsiz olmak","Çekirdek at","İncir topla"],c:1},
{q:"'Su testisi su yolunda kırılır' ne demektir?",a:["Testi al","Tehlikeyle sürekli uğraşan sonunda zarar görür","Su iç","Yol yap"],c:1},
{q:"'Dostlar alışverişte görsün' ne demektir?",a:["Alışveriş yap","Göstermelik iş yapmak","Dost edin","Market git"],c:1},
{q:"'Dikensiz gül olmaz' ne demektir?",a:["Gül dik","Her güzel şeyin zorluğu var","Diken topla","Bahçe yap"],c:1},
{q:"'Alçak uçan yüksekten uçar' ne demektir?",a:["Uç","Mütevazı olan başarır","Yüksel","Alçal"],c:1},
{q:"Niagara Şelalesi hangi ülkeler arasındadır?",a:["Brezilya-Arjantin","ABD-Kanada","Meksika-ABD","Zambiya-Zimbabve"],c:1},
{q:"Angel Şelalesi hangi ülkededir?",a:["Brezilya","Kolombiya","Venezuela","Peru"],c:2},
{q:"İguazu Şelalesi hangi ülkeler arasındadır?",a:["ABD-Kanada","Brezilya-Arjantin","Zambiya-Zimbabve","Peru-Ekvador"],c:1},
{q:"Gondwana neyi ifade eder?",a:["Eski kuzey kıtası","Eski güney süper kıtası","İlk okyanus","İlk atmosfer"],c:1},
{q:"Laurasia neyi ifade eder?",a:["Eski güney kıtası","Eski kuzey süper kıtası","İlk göl","İlk dağ"],c:1},
{q:"Pasifik Okyanusu dünya yüzeyinin yüzde kaçını kaplar?",a:["15","22","30","46"],c:2},
{q:"Sargasso Denizi hangi okyanustadır?",a:["Pasifik","Hint","Atlas","Arktik"],c:2},
{q:"Mariana Çukuru yaklaşık kaç metre derindir?",a:["5000","8000","11000","15000"],c:2},
{q:"Dünyanın en büyük adası hangisidir?",a:["Madagaskar","Borneo","Grönland","Sumatra"],c:2},
{q:"Dünyanın en yüksek şelalesi hangisidir?",a:["Niagara","Victoria","Angel","İguazu"],c:2},
{q:"Rocky Dağları hangi kıtadadır?",a:["Güney Amerika","Avrupa","Asya","Kuzey Amerika"],c:3},
{q:"Atlas Dağları hangi kıtadadır?",a:["Asya","Avrupa","Güney Amerika","Afrika"],c:3},
{q:"Vinson Dağı hangi kıtanın en yüksek dağıdır?",a:["Avustralya","Güney Amerika","Avrupa","Antarktika"],c:3},
{q:"Aral Gölü neden küçülmüştür?",a:["Deprem","Sulama için su çekilmesi","Küresel ısınma","Volkanik aktivite"],c:1},
{q:"Okavango Deltası hangi ülkededir?",a:["Güney Afrika","Tanzanya","Botsvana","Kenya"],c:2},
{q:"'Balık kavağa çıkınca' ne demektir?",a:["Balık tut","Asla imkansız","Kavak dik","Balık ye"],c:1},
{q:"'Araba devrilince yol gösteren çok olur' ne demektir?",a:["Araba sür","İş bittikten sonra akıl veren çok olur","Yol sor","Araba al"],c:1},
{q:"'Bin bilsen de bir bilene danış' ne demektir?",a:["Bil","Ne kadar bilgili olsan da tecrübelilere danış","Danış","Sor"],c:1},
{q:"Noether teoremi neyi bağlar?",a:["Kütle-enerji","Simetri-korunum yasası","Hız-zaman","Basınç-hacim"],c:1},
{q:"Riemann hipotezi hangi fonksiyonla ilgilidir?",a:["Gamma","Beta","Zeta","Theta"],c:2},
{q:"P vs NP problemi hangi alanla ilgilidir?",a:["Fizik","Hesaplama karmaşıklığı","Biyoloji","Kimya"],c:1},
{q:"Hodge konjektürü hangi alanla ilgilidir?",a:["Cebirsel geometri","Topoloji","Analiz","Olasılık"],c:0},
{q:"Yang-Mills teorisi hangi kuvvetle ilgilidir?",a:["Kütle çekim","Güçlü nükleer","Elektromanyetik","Zayıf nükleer"],c:1},
{q:"Birch ve Swinnerton-Dyer konjektürü neyle ilgilidir?",a:["Asal sayılar","Eliptik eğriler","Grafik teorisi","Olasılık"],c:1},
{q:"Navier-Stokes denklemi hangi alanla ilgilidir?",a:["Elektrik","Akışkanlar mekaniği","Termodinamik","Optik"],c:1},
{q:"Poincaré konjektürünü kim ispatlamıştır?",a:["Andrew Wiles","Grigori Perelman","Terence Tao","Peter Scholze"],c:1},
{q:"Fermat'ın Son Teoremi'ni kim ispatlamıştır?",a:["Euler","Gauss","Andrew Wiles","Hilbert"],c:2},
{q:"Göbekli Tepe kaç yıl öncesine tarihlenir?",a:["5.000","8.000","12.000","3.000"],c:2},
{q:"Çatalhöyük hangi ildedir?",a:["Şanlıurfa","Diyarbakır","Konya","Kayseri"],c:2},
{q:"Mohenjo-daro hangi ülkededir?",a:["Hindistan","Bangladeş","Pakistan","Nepal"],c:2},
{q:"Rosetta Taşı hangi dilleri içerir?",a:["Latince-Yunanca","Hiyeroglif-Demotik-Yunanca","Sümerce-Akadca","Aramice-İbranice"],c:1},
{q:"Heisenberg belirsizlik ilkesi neyi sınırlar?",a:["Hız ölçümü","Konum ve momentum eş zamanlı ölçümü","Sıcaklık ölçümü","Kütle ölçümü"],c:1},
{q:"Bell eşitsizliği hangi konuyla ilgilidir?",a:["Görelilik","Kuantum dolanıklık","Termodinamik","Elektromanyetizma"],c:1},
{q:"Hubble sabiti neyi ölçer?",a:["Yıldız parlaklığı","Evrenin genişleme hızı","Galaksi sayısı","Gezegen hızı"],c:1},
{q:"Chandrasekhar limiti neyi belirler?",a:["Gezegen kütlesi","Beyaz cüce yıldız üst kütle sınırı","Kara delik yarıçapı","Galaksi boyutu"],c:1},
{q:"CRISPR-Cas9 hangi alanda devrim yaratmıştır?",a:["Nükleer fizik","Gen düzenleme","Malzeme bilimi","Uzay araştırmaları"],c:1},
{q:"Hawking radyasyonu neyle ilgilidir?",a:["Güneş","Nötron yıldızları","Kara delikler","Kuasarlar"],c:2},
{q:"'Deve yarışa giremez' deyimi var mıdır?",a:["Evet, atasözüdür","Hayır, böyle bir deyim yoktur","Evet, deyimdir","Evet, halk söylemidir"],c:1},
{q:"Schrödinger'in kedisi hangi konuyu anlatır?",a:["Görelilik","Kuantum süperpozisyon","Termodinamik","Optik"],c:1},
{q:"Karst topoğrafyası hangi kayaçta oluşur?",a:["Granit","Bazalt","Kireçtaşı","Gnays"],c:2},
{q:"Laurasia ve Gondwana ne zaman ayrılmıştır?",a:["500 milyon yıl","200 milyon yıl","50 milyon yıl","1 milyar yıl"],c:1},
{q:"Pangea süperkıtası ne zaman vardı?",a:["500 milyon yıl önce","335-175 milyon yıl önce","50 milyon yıl önce","1 milyar yıl önce"],c:1},
{q:"Mariyana Çukuru'nun derinliği kaç metredir?",a:["8.848","10.994","7.500","12.000"],c:1},
{q:"Drake denklemi neyi tahmin eder?",a:["Gezegen sayısı","Evrendeki iletişim kurabilecek medeniyet sayısı","Yıldız ömrü","Galaksi uzaklığı"],c:1},
{q:"Olbers paradoksu neyi sorgular?",a:["Güneş'in enerji kaynağı","Gökyüzü neden gece karanlık","Gezegen yörüngeleri","Ay'ın oluşumu"],c:1},
{q:"'Çoban armağanı' ne demektir?",a:["Hediye","Sade ama içten hediye","Çoban","Armağan ver"],c:1},
{q:"'Engerek yılanı kendi yavrusunu yer' ne demektir?",a:["Yılan besle","Kötü kişi yakınlarına da zarar verir","Yavru bak","Yılan tut"],c:1},
{q:"'Fikir iki olunca yol alır' ne demektir?",a:["Fikir ver","Birden fazla görüş sorunu çözer","Yol yürü","İki düşün"],c:1},
{q:"Karanlık madde evrenin yüzde kaçını oluşturur?",a:["%5","%15","%27","%68"],c:2},
{q:"Karanlık enerji evrenin yüzde kaçını oluşturur?",a:["%5","%27","%68","%95"],c:2},
{q:"Kozmik mikrodalga arka plan radyasyonu kaç Kelvin'dir?",a:["0 K","2.725 K","100 K","5.5 K"],c:1},
{q:"Schwarzschild yarıçapı neyi tanımlar?",a:["Yıldız yarıçapı","Kara delik olay ufku","Gezegen yörüngesi","Galaksi çapı"],c:1},
{q:"Kuiper Kuşağı nerededir?",a:["Mars-Jüpiter arası","Neptün ötesi","Güneş yakını","Merkür yörüngesinde"],c:1},
{q:"Hangisi bir postmodern romancıdır?",a:["Tolstoy","Dostoyevski","Italo Calvino","Hugo"],c:2},
{q:"Stravinsky hangi müzik döneminin bestecisidir?",a:["Barok","Klasik","Romantik","Modern"],c:3},
{q:"Hangisi bir felsefe akımıdır?",a:["Kübizm","Fovizm","Varoluşçuluk","Dadaizm"],c:2},
{q:"Bir futbol takımında toplam kaç oyuncu forma giyebilir?",a:["16","18","20","23"],c:1},
{q:"Hangisi bir Japon savaş sanatı değildir?",a:["Kendo","Sumo","Capoeira","Jujitsu"],c:2},
{q:"Dünya'nın en pahalı tablosu kime aittir?",a:["Picasso","Da Vinci","Van Gogh","Monet"],c:1}
]
"""

def _build_milyoner_html(level: str = "yetiskin") -> str:
    """Kim Milyoner Olmak İster — 4 seviye, 100+ soru/seviye, 3 joker, premium tasarım."""
    questions_js = _get_questions(level)
    level_labels = {"ilkokul": "İlkokul", "ortaokul": "Ortaokul", "lise": "Lise", "yetiskin": "Yetişkin"}
    level_label = level_labels.get(level, "Yetişkin")
    html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box}body,html{width:100%;height:100%;overflow:hidden;background:#060620;font-family:'Segoe UI',sans-serif}</style>
</head><body>
<canvas id="gc" width="700" height="650"></canvas>
<script>
var c=document.getElementById("gc"),x=c.getContext("2d"),W=700,H=650;
var state="start",qIdx=0,selected=-1,confirmed=false;
var jokers={fifty:true,audience:true,phone:true};
var fiftyRemoved=[],audienceData=[],phoneAnswer=-1;
var showAudience=false,showPhone=false;
var correctFlash=0,wrongFlash=0,winAnim=0;
var currentQuestions=[];
var totalCorrect=0,totalPlayed=0;
var LEVEL_LABEL="__LEVEL_LABEL__";

var MONEY=[100,200,300,500,1000,2000,4000,8000,16000,32000,64000,125000,250000,500000,1000000];
var SAFE=[4,9];

/* ══════════════════ SORU BANKASI ══════════════════ */
var allQuestions={
__QUESTIONS_JS__
};

function shuffleArray(arr){
  for(var i=arr.length-1;i>0;i--){
    var j=Math.floor(Math.random()*(i+1));
    var t=arr[i];arr[i]=arr[j];arr[j]=t;
  }
  return arr;
}

function isBK(q){return q.q.indexOf("başkent")!==-1||q.q.indexOf("Başkent")!==-1;}

function pickQuestions(){
  var KEY="km_used_"+LEVEL_LABEL;
  var used=[];
  try{used=JSON.parse(localStorage.getItem(KEY)||"[]");}catch(e){used=[];}

  function pickFromPool(pool,n){
    var avail=pool.filter(function(q){return used.indexOf(q.q)===-1;});
    if(avail.length<n){
      used=[];
      try{localStorage.setItem(KEY,"[]");}catch(e){}
      avail=pool.slice();
    }
    /* %50 Genel Kültür garantisi: en az yarısı GK (non-başkent) olacak */
    var gk=shuffleArray(avail.filter(function(q){return !isBK(q);}));
    var bk=shuffleArray(avail.filter(function(q){return isBK(q);}));
    var gkCount=Math.ceil(n*0.5);
    var bkCount=n-gkCount;
    var result=[];
    for(var i=0;i<Math.min(gkCount,gk.length);i++) result.push(gk[i]);
    for(var i=0;i<Math.min(bkCount,bk.length);i++) result.push(bk[i]);
    /* Eksik kaldıysa diğer havuzdan tamamla */
    if(result.length<n){
      var rest=avail.filter(function(q){return result.indexOf(q)===-1;});
      rest=shuffleArray(rest);
      while(result.length<n&&rest.length>0) result.push(rest.shift());
    }
    return shuffleArray(result);
  }

  var e=pickFromPool(allQuestions.easy,4);
  var m=pickFromPool(allQuestions.medium,5);
  var h=pickFromPool(allQuestions.hard,3);
  var vh=pickFromPool(allQuestions.very_hard,3);
  currentQuestions=e.concat(m).concat(h).concat(vh);

  /* Başkent soruları art arda gelmesin */
  for(var i=1;i<currentQuestions.length;i++){
    if(isBK(currentQuestions[i])&&isBK(currentQuestions[i-1])){
      for(var j=i+1;j<currentQuestions.length;j++){
        if(!isBK(currentQuestions[j])){
          var tmp=currentQuestions[i];
          currentQuestions[i]=currentQuestions[j];
          currentQuestions[j]=tmp;
          break;
        }
      }
    }
  }

  for(var i=0;i<currentQuestions.length;i++){used.push(currentQuestions[i].q);}
  try{localStorage.setItem(KEY,JSON.stringify(used));}catch(e){}
}

var LETTERS=["A","B","C","D"];
var ACx=null;
function snd(f,d,t){try{if(!ACx)ACx=new(window.AudioContext||window.webkitAudioContext)();var o=ACx.createOscillator(),g=ACx.createGain();o.connect(g);g.connect(ACx.destination);o.type=t||"sine";o.frequency.value=f;g.gain.setValueAtTime(0.13,ACx.currentTime);g.gain.exponentialRampToValueAtTime(0.001,ACx.currentTime+d);o.start();o.stop(ACx.currentTime+d);}catch(e){}}
function playCorrect(){snd(523,0.12);setTimeout(function(){snd(659,0.12)},120);setTimeout(function(){snd(784,0.25)},240);}
function playWrong(){snd(300,0.25,"sawtooth");setTimeout(function(){snd(200,0.4,"sawtooth")},250);}
function playClick(){snd(600,0.06);}
function playSelect(){snd(440,0.08);setTimeout(function(){snd(550,0.08)},80);}
function playWin(){for(var i=0;i<8;i++)setTimeout(function(n){snd(400+n*70,0.18)},n*100,i);}
function playStart(){snd(392,0.15);setTimeout(function(){snd(523,0.15)},150);setTimeout(function(){snd(659,0.25)},300);}
function playMilestone(){snd(523,0.1);setTimeout(function(){snd(659,0.1)},100);setTimeout(function(){snd(784,0.1)},200);setTimeout(function(){snd(1047,0.3)},300);}

function fmt(n){return n.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,".")+" TL";}

function rRect(rx,ry,rw,rh,rr,fill,stroke,lw){
  x.beginPath();x.moveTo(rx+rr,ry);x.lineTo(rx+rw-rr,ry);x.quadraticCurveTo(rx+rw,ry,rx+rw,ry+rr);x.lineTo(rx+rw,ry+rh-rr);x.quadraticCurveTo(rx+rw,ry+rh,rx+rw-rr,ry+rh);x.lineTo(rx+rr,ry+rh);x.quadraticCurveTo(rx,ry+rh,rx,ry+rh-rr);x.lineTo(rx,ry+rr);x.quadraticCurveTo(rx,ry,rx+rr,ry);x.closePath();
  if(fill){x.fillStyle=fill;x.fill();}if(stroke){x.strokeStyle=stroke;x.lineWidth=lw||2;x.stroke();}
}

var particles=[];
function spawn(px,py,n,col){for(var i=0;i<n;i++)particles.push({x:px,y:py,vx:(Math.random()-0.5)*7,vy:(Math.random()-0.5)*7-2,life:50+Math.random()*50,ml:100,r:1.5+Math.random()*3,col:col||"#ffd700"});}

function drawBG(){
  var bg=x.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,"#060620");bg.addColorStop(0.3,"#0d0d3a");bg.addColorStop(0.7,"#0a0a30");bg.addColorStop(1,"#050518");
  x.fillStyle=bg;x.fillRect(0,0,W,H);
  // Subtle stars
  for(var i=0;i<40;i++){
    var sx=((i*137+51)%W),sy=((i*97+33)%(H-100));
    x.globalAlpha=0.2+0.3*Math.abs(Math.sin(Date.now()/2000+i*0.7));
    x.fillStyle="#aaccff";x.beginPath();x.arc(sx,sy,0.8,0,Math.PI*2);x.fill();
  }
  x.globalAlpha=1;
}

function drawParticles(){
  for(var i=particles.length-1;i>=0;i--){
    var p=particles[i];p.x+=p.vx;p.y+=p.vy;p.vy+=0.12;p.life--;
    x.globalAlpha=Math.max(0,p.life/p.ml);x.fillStyle=p.col;
    x.beginPath();x.arc(p.x,p.y,p.r,0,Math.PI*2);x.fill();
    if(p.life<=0)particles.splice(i,1);
  }
  x.globalAlpha=1;
}

/* ══════════ START SCREEN ══════════ */
function drawStart(){
  drawBG();
  // Diamond logo
  var t=Date.now()/1000;
  x.save();x.translate(W/2,155);x.rotate(Math.sin(t)*0.05);
  var dg=x.createRadialGradient(0,0,10,0,0,70);
  dg.addColorStop(0,"rgba(255,215,0,0.4)");dg.addColorStop(1,"rgba(255,215,0,0)");
  x.fillStyle=dg;x.beginPath();x.moveTo(0,-70);x.lineTo(70,0);x.lineTo(0,70);x.lineTo(-70,0);x.closePath();x.fill();
  x.strokeStyle="#ffd700";x.lineWidth=2.5;x.stroke();
  // Inner
  x.beginPath();x.moveTo(0,-42);x.lineTo(42,0);x.lineTo(0,42);x.lineTo(-42,0);x.closePath();
  x.fillStyle="rgba(255,215,0,0.15)";x.fill();x.strokeStyle="#ffd700";x.lineWidth=1.5;x.stroke();
  // TL
  x.fillStyle="#ffd700";x.font="bold 28px 'Segoe UI'";x.textAlign="center";x.textBaseline="middle";
  x.fillText("₺",0,0);
  x.restore();

  // Title
  x.shadowColor="#ffd700";x.shadowBlur=25;
  x.fillStyle="#ffd700";x.font="bold 38px 'Segoe UI'";x.textAlign="center";
  x.fillText("KİM MİLYONER",W/2,280);
  x.fillText("OLMAK İSTER?",W/2,325);
  x.shadowBlur=0;

  x.fillStyle="#7777bb";x.font="15px 'Segoe UI'";
  x.fillText("15 Soru  ·  3 Joker  ·  1.000.000 ₺ Büyük Ödül",W/2,360);
  x.fillStyle="#ffd700";x.font="bold 14px 'Segoe UI'";
  x.fillText("◆ "+LEVEL_LABEL+" Seviyesi ◆",W/2,385);
  x.fillStyle="#7777bb";x.font="13px 'Segoe UI'";
  x.fillText("Her Oyunda Farklı Sorular  ·  Diamond 3D Edition",W/2,405);

  // Start button
  var pulse=0.85+Math.sin(Date.now()/400)*0.15;
  x.globalAlpha=pulse;
  var sg=x.createLinearGradient(W/2-130,430,W/2+130,480);
  sg.addColorStop(0,"#8B6914");sg.addColorStop(0.5,"#ffd700");sg.addColorStop(1,"#8B6914");
  rRect(W/2-130,432,260,52,26,sg,"#ffd700");
  x.globalAlpha=1;
  x.fillStyle="#0B0F19";x.font="bold 24px 'Segoe UI'";
  x.fillText("BAŞLA",W/2,465);

  // Stats
  if(totalPlayed>0){
    x.fillStyle="#666";x.font="13px 'Segoe UI'";
    x.fillText("Oynanan: "+totalPlayed+"  |  Kazanılan: "+totalCorrect+" soru",W/2,530);
  }

  // Money ladder preview
  x.fillStyle="#555";x.font="12px 'Segoe UI'";
  x.fillText("100 → 1.000 → 32.000 → 1.000.000 ₺",W/2,560);
  x.fillText("Garanti Basamakları: 5. Soru (1.000 ₺)  ·  10. Soru (32.000 ₺)",W/2,580);
}

/* ══════════ PLAY SCREEN ══════════ */
function drawMoneyLadder(){
  var lw=140,lh=26,lx=W-lw-12,startY=52;
  for(var i=14;i>=0;i--){
    var ly=startY+(14-i)*(lh+3);
    var isSafe=SAFE.indexOf(i)>=0;
    var isCurrent=i===qIdx;
    var isPassed=i<qIdx;
    var bg,tc,bc;
    if(isCurrent){bg="rgba(255,215,0,0.25)";tc="#ffd700";bc="#ffd700";}
    else if(isPassed){bg="rgba(0,200,100,0.15)";tc="#22cc66";bc="rgba(0,200,100,0.4)";}
    else if(isSafe){bg="rgba(255,255,255,0.06)";tc="#ddd";bc="rgba(255,215,0,0.4)";}
    else{bg="rgba(80,80,160,0.08)";tc="#7777aa";bc="rgba(80,80,160,0.2)";}
    rRect(lx,ly,lw,lh,4,bg,bc,isCurrent?2:1);
    x.font=(isCurrent?"bold ":"")+"11px 'Segoe UI'";
    x.fillStyle=tc;x.textAlign="left";
    x.fillText((i+1)+".",lx+6,ly+17);
    x.textAlign="right";
    x.fillText(fmt(MONEY[i]),lx+lw-6,ly+17);
  }
}

function drawJokers(){
  var jy=8,jw=72,jh=32,jx=12;
  var jks=[{k:"fifty",l:"50:50"},{k:"audience",l:"Seyirci"},{k:"phone",l:"Telefon"}];
  for(var i=0;i<3;i++){
    var jxx=jx+i*(jw+8);
    var active=jokers[jks[i].k];
    var bg=active?"rgba(255,215,0,0.15)":"rgba(60,60,60,0.2)";
    var bc=active?"rgba(255,215,0,0.6)":"rgba(60,60,60,0.3)";
    rRect(jxx,jy,jw,jh,8,bg,bc);
    x.font=(active?"bold ":"")+"12px 'Segoe UI'";
    x.fillStyle=active?"#ffd700":"#444";
    x.textAlign="center";
    x.fillText(jks[i].l,jxx+jw/2,jy+21);
  }
}

function wrapText(text,maxW){
  var words=text.split(" "),lines=[],line="";
  for(var i=0;i<words.length;i++){
    var test=line+(line?" ":"")+words[i];
    if(x.measureText(test).width>maxW&&line){lines.push(line);line=words[i];}
    else{line=test;}
  }
  if(line)lines.push(line);return lines;
}

function drawQuestion(){
  var q=currentQuestions[qIdx];
  var qbx=12,qby=50,qbw=525,qbh=80;
  var qg=x.createLinearGradient(qbx,qby,qbx,qby+qbh);
  qg.addColorStop(0,"rgba(25,25,70,0.95)");qg.addColorStop(1,"rgba(15,15,50,0.95)");
  rRect(qbx,qby,qbw,qbh,12,qg,"rgba(100,100,200,0.4)");

  x.font="bold 12px 'Segoe UI'";x.fillStyle="#ffd700";x.textAlign="left";
  x.fillText("Soru "+(qIdx+1)+"/15",qbx+14,qby+18);
  x.textAlign="right";x.fillText(fmt(MONEY[qIdx]),qbx+qbw-14,qby+18);

  x.font="15px 'Segoe UI'";x.fillStyle="#fff";x.textAlign="center";
  var lines=wrapText(q.q,qbw-36);
  var lH=20,tH=lines.length*lH;
  var sY=qby+22+(qbh-22-tH)/2+14;
  for(var i=0;i<lines.length;i++)x.fillText(lines[i],qbx+qbw/2,sY+i*lH);
}

function drawAnswers(){
  var q=currentQuestions[qIdx];
  var aw=258,ah=52,positions=[[12,148],[275,148],[12,210],[275,210]];
  for(var i=0;i<4;i++){
    if(fiftyRemoved.indexOf(i)>=0){
      // Draw dimmed slot
      rRect(positions[i][0],positions[i][1],aw,ah,10,"rgba(20,20,40,0.3)","rgba(40,40,60,0.2)");
      continue;
    }
    var px=positions[i][0],py=positions[i][1];
    var bg,bc,tc;
    if(confirmed&&i===q.c){
      bg="rgba(0,200,80,0.35)";bc="#00dd55";tc="#00ff66";
    }else if(confirmed&&i===selected&&i!==q.c){
      bg="rgba(220,40,40,0.35)";bc="#ee3333";tc="#ff6666";
    }else if(i===selected&&!confirmed){
      bg="rgba(255,215,0,0.25)";bc="#ffd700";tc="#ffd700";
    }else{
      bg="rgba(25,25,70,0.75)";bc="rgba(100,100,200,0.35)";tc="#ccc";
    }
    rRect(px,py,aw,ah,10,bg,bc);

    x.font="bold 16px 'Segoe UI'";x.fillStyle="#ffd700";x.textAlign="left";
    x.fillText(LETTERS[i]+":",px+14,py+31);

    x.font="14px 'Segoe UI'";x.fillStyle=tc;
    var aL=wrapText(q.a[i],aw-50);
    if(aL.length===1){x.fillText(aL[0],px+42,py+31);}
    else{for(var li=0;li<aL.length;li++)x.fillText(aL[li],px+42,py+20+li*17);}
  }
}

function drawConfirmBtn(){
  if(selected<0||confirmed)return;
  var bx=140,by=540,bw=260,bh=48;
  var bg=x.createLinearGradient(bx,by,bx+bw,by+bh);
  bg.addColorStop(0,"#8B6914");bg.addColorStop(0.5,"#ffd700");bg.addColorStop(1,"#8B6914");
  rRect(bx,by,bw,bh,24,bg,"#ffd700");
  x.fillStyle="#0B0F19";x.font="bold 18px 'Segoe UI'";x.textAlign="center";
  x.fillText("SON CEVAP",bx+bw/2,by+31);
}

function drawGiveUpBtn(){
  if(confirmed)return;
  var bx=420,by=548,bw=110,bh=32;
  rRect(bx,by,bw,bh,16,"rgba(100,50,50,0.3)","rgba(200,100,100,0.4)");
  x.fillStyle="#cc8888";x.font="12px 'Segoe UI'";x.textAlign="center";
  x.fillText("Çekiliyorum",bx+bw/2,by+21);
}

function drawSafeInfo(){
  var earned=0;
  for(var s=SAFE.length-1;s>=0;s--){if(qIdx>SAFE[s]){earned=MONEY[SAFE[s]];break;}}
  x.font="11px 'Segoe UI'";x.fillStyle="#555";x.textAlign="left";
  x.fillText("Garanti: "+fmt(earned),12,635);
}

function drawAudiencePanel(){
  if(!showAudience)return;
  var px=50,py=290,pw=440,ph=210;
  rRect(px,py,pw,ph,15,"rgba(8,8,35,0.97)","#ffd700",2);
  x.font="bold 15px 'Segoe UI'";x.fillStyle="#ffd700";x.textAlign="center";
  x.fillText("Seyirci Sonuçları",px+pw/2,py+28);
  var barW=55,barMaxH=120,total=px+pw;
  var validCount=4-fiftyRemoved.length;
  var startX=px+(pw-validCount*(barW+30))/2+15;
  var idx=0;
  for(var i=0;i<4;i++){
    if(fiftyRemoved.indexOf(i)>=0)continue;
    var bx2=startX+idx*(barW+30);idx++;
    var bh2=audienceData[i]/100*barMaxH;
    var by2=py+ph-35-bh2;
    var gd=x.createLinearGradient(bx2,by2,bx2,by2+bh2);
    gd.addColorStop(0,"#ffd700");gd.addColorStop(1,"#8B6914");
    rRect(bx2,by2,barW,bh2,4,gd);
    x.font="bold 13px 'Segoe UI'";x.fillStyle="#fff";x.textAlign="center";
    x.fillText("%"+audienceData[i],bx2+barW/2,by2-8);
    x.fillStyle="#ffd700";x.fillText(LETTERS[i],bx2+barW/2,py+ph-15);
  }
  x.font="11px 'Segoe UI'";x.fillStyle="#666";x.fillText("Tıklayarak kapatın",px+pw/2,py+ph-2);
}

function drawPhonePanel(){
  if(!showPhone)return;
  var px=50,py=310,pw=440,ph=140;
  rRect(px,py,pw,ph,15,"rgba(8,8,35,0.97)","#ffd700",2);
  x.font="bold 15px 'Segoe UI'";x.fillStyle="#ffd700";x.textAlign="center";
  x.fillText("Telefon Jokeri",px+pw/2,py+28);
  var q=currentQuestions[qIdx];
  x.font="15px 'Segoe UI'";x.fillStyle="#ddd";
  x.fillText('"Bence cevap '+LETTERS[phoneAnswer]+': '+q.a[phoneAnswer]+'"',px+pw/2,py+65);
  var conf=phoneAnswer===q.c?Math.floor(70+Math.random()*25):Math.floor(20+Math.random()*40);
  x.fillStyle="#999";x.font="13px 'Segoe UI'";
  x.fillText("— Arkadaşın %"+conf+" emin",px+pw/2,py+90);
  x.font="11px 'Segoe UI'";x.fillStyle="#666";x.fillText("Tıklayarak kapatın",px+pw/2,py+125);
}

function drawPlay(){
  drawBG();
  drawMoneyLadder();drawJokers();drawQuestion();drawAnswers();
  drawConfirmBtn();drawGiveUpBtn();drawSafeInfo();
  if(showAudience)drawAudiencePanel();
  if(showPhone)drawPhonePanel();
  drawParticles();

  if(confirmed&&correctFlash>0){
    correctFlash--;
    if(correctFlash===0){
      totalCorrect++;qIdx++;selected=-1;confirmed=false;fiftyRemoved=[];
      showAudience=false;showPhone=false;
      if(qIdx>=15){state="win";playWin();winAnim=0;}
      else if(SAFE.indexOf(qIdx-1)>=0)playMilestone();
    }
  }
  if(confirmed&&wrongFlash>0){wrongFlash--;if(wrongFlash===0)state="lose";}
}

/* ══════════ WIN / LOSE SCREENS ══════════ */
function drawWin(){
  drawBG();winAnim++;
  if(winAnim%3===0)spawn(Math.random()*W,30,2,["#ffd700","#ff6b6b","#4ecdc4","#45b7d1","#ff69b4"][Math.floor(Math.random()*5)]);
  drawParticles();

  x.save();x.translate(W/2,140);
  var sc=1+Math.sin(Date.now()/500)*0.05;x.scale(sc,sc);
  x.beginPath();x.moveTo(0,-55);x.lineTo(55,0);x.lineTo(0,55);x.lineTo(-55,0);x.closePath();
  x.fillStyle="rgba(255,215,0,0.3)";x.fill();x.strokeStyle="#ffd700";x.lineWidth=3;x.stroke();
  x.fillStyle="#ffd700";x.font="bold 24px 'Segoe UI'";x.textAlign="center";x.textBaseline="middle";
  x.fillText("₺",0,0);x.restore();

  x.shadowColor="#ffd700";x.shadowBlur=30;
  x.fillStyle="#ffd700";x.font="bold 44px 'Segoe UI'";x.textAlign="center";
  x.fillText("TEBRİKLER!",W/2,270);x.shadowBlur=0;

  x.fillStyle="#fff";x.font="bold 26px 'Segoe UI'";
  x.fillText("1.000.000 ₺ Kazandınız!",W/2,320);
  x.fillStyle="#8888cc";x.font="16px 'Segoe UI'";
  x.fillText("15 sorunun tamamını doğru yanıtladınız!",W/2,355);

  rRect(W/2-110,420,220,50,25,"rgba(255,215,0,0.2)","#ffd700");
  x.fillStyle="#ffd700";x.font="bold 20px 'Segoe UI'";x.fillText("Tekrar Oyna",W/2,452);
}

function drawLose(){
  drawBG();
  var earned=0;
  for(var s=SAFE.length-1;s>=0;s--){if(qIdx>SAFE[s]){earned=MONEY[SAFE[s]];break;}}
  var q=currentQuestions[qIdx];

  x.fillStyle="#ff5555";x.font="bold 38px 'Segoe UI'";x.textAlign="center";
  x.fillText("YANLIŞ CEVAP!",W/2,160);

  x.fillStyle="#aaa";x.font="16px 'Segoe UI'";
  x.fillText("Doğru cevap:",W/2,210);
  x.fillStyle="#00dd55";x.font="bold 20px 'Segoe UI'";
  x.fillText(LETTERS[q.c]+") "+q.a[q.c],W/2,240);

  // Earned box
  rRect(W/2-160,280,320,90,15,"rgba(255,215,0,0.08)","rgba(255,215,0,0.3)");
  x.fillStyle="#ffd700";x.font="bold 28px 'Segoe UI'";
  x.fillText(fmt(earned),W/2,320);
  x.fillStyle="#888";x.font="14px 'Segoe UI'";
  x.fillText(earned>0?"Garanti basamağından kazancınız":"Maalesef kazancınız yok",W/2,350);

  x.fillStyle="#7777aa";x.font="15px 'Segoe UI'";
  x.fillText((qIdx+1)+". soruda elendiniz",W/2,410);

  rRect(W/2-110,460,220,50,25,"rgba(255,215,0,0.2)","#ffd700");
  x.fillStyle="#ffd700";x.font="bold 20px 'Segoe UI'";x.fillText("Tekrar Oyna",W/2,492);
}

function drawGiveUp(){
  drawBG();
  var earned=qIdx>0?MONEY[qIdx-1]:0;

  x.fillStyle="#ffd700";x.font="bold 34px 'Segoe UI'";x.textAlign="center";
  x.fillText("ÇEKİLDİNİZ",W/2,180);

  rRect(W/2-160,230,320,90,15,"rgba(255,215,0,0.08)","rgba(255,215,0,0.3)");
  x.fillStyle="#ffd700";x.font="bold 30px 'Segoe UI'";
  x.fillText(fmt(earned),W/2,270);
  x.fillStyle="#888";x.font="15px 'Segoe UI'";
  x.fillText("Toplam kazancınız",W/2,300);

  x.fillStyle="#7777aa";x.font="16px 'Segoe UI'";
  x.fillText(qIdx+" soru doğru yanıtlandı",W/2,370);

  rRect(W/2-110,430,220,50,25,"rgba(255,215,0,0.2)","#ffd700");
  x.fillStyle="#ffd700";x.font="bold 20px 'Segoe UI'";x.fillText("Tekrar Oyna",W/2,462);
}

/* ══════════ JOKER LOGIC ══════════ */
function useFifty(){
  if(!jokers.fifty||confirmed)return;jokers.fifty=false;
  var q=currentQuestions[qIdx],wr=[];
  for(var i=0;i<4;i++){if(i!==q.c)wr.push(i);}
  wr.sort(function(){return Math.random()-0.5;});
  fiftyRemoved=[wr[0],wr[1]];
  if(fiftyRemoved.indexOf(selected)>=0)selected=-1;
  playClick();
}
function useAudience(){
  if(!jokers.audience||confirmed)return;jokers.audience=false;
  var q=currentQuestions[qIdx];audienceData=[0,0,0,0];
  var cp=40+Math.floor(Math.random()*35);audienceData[q.c]=cp;var rem=100-cp;
  for(var i=0;i<4;i++){if(i===q.c||fiftyRemoved.indexOf(i)>=0)continue;var sh=Math.floor(Math.random()*rem);audienceData[i]=sh;rem-=sh;}
  for(var i=0;i<4;i++){if(i!==q.c&&fiftyRemoved.indexOf(i)<0){audienceData[i]+=rem;break;}}
  showAudience=true;playClick();
}
function usePhone(){
  if(!jokers.phone||confirmed)return;jokers.phone=false;
  var q=currentQuestions[qIdx];
  if(Math.random()<0.75){phoneAnswer=q.c;}
  else{var opts=[];for(var i=0;i<4;i++){if(i!==q.c&&fiftyRemoved.indexOf(i)<0)opts.push(i);}phoneAnswer=opts.length?opts[Math.floor(Math.random()*opts.length)]:q.c;}
  showPhone=true;playClick();
}

/* ══════════ INPUT ══════════ */
function handleClick(mx,my){
  if(state==="start"){
    if(mx>W/2-130&&mx<W/2+130&&my>432&&my<484){
      state="play";pickQuestions();qIdx=0;selected=-1;confirmed=false;
      jokers={fifty:true,audience:true,phone:true};
      fiftyRemoved=[];particles=[];totalPlayed++;
      showAudience=false;showPhone=false;
      playStart();
    }
    return;
  }
  if(state==="win"||state==="lose"){
    if(mx>W/2-110&&mx<W/2+110&&my>420&&my<(state==="win"?470:510)){state="start";particles=[];}
    return;
  }
  if(state==="giveup"){
    if(mx>W/2-110&&mx<W/2+110&&my>430&&my<480){state="start";particles=[];}
    return;
  }
  if(state!=="play")return;

  if(showAudience){showAudience=false;return;}
  if(showPhone){showPhone=false;return;}
  if(confirmed)return;

  // Jokers
  if(my>8&&my<40){
    if(mx>12&&mx<84){useFifty();return;}
    if(mx>92&&mx<164){useAudience();return;}
    if(mx>172&&mx<244){usePhone();return;}
  }

  // Answers
  var positions=[[12,148],[275,148],[12,210],[275,210]];
  for(var i=0;i<4;i++){
    if(fiftyRemoved.indexOf(i)>=0)continue;
    if(mx>positions[i][0]&&mx<positions[i][0]+258&&my>positions[i][1]&&my<positions[i][1]+52){
      selected=i;playSelect();return;
    }
  }

  // Confirm
  if(selected>=0&&mx>140&&mx<400&&my>540&&my<588){
    confirmed=true;
    var q=currentQuestions[qIdx];
    if(selected===q.c){playCorrect();correctFlash=55;spawn(W/2,180,15,"#ffd700");}
    else{playWrong();wrongFlash=70;}
    return;
  }

  // Give up
  if(mx>420&&mx<530&&my>548&&my<580){
    state="giveup";return;
  }
}

c.addEventListener("click",function(e){
  var r=c.getBoundingClientRect();
  handleClick((e.clientX-r.left)*c.width/r.width,(e.clientY-r.top)*c.height/r.height);
});
c.addEventListener("touchstart",function(e){
  e.preventDefault();var t=e.touches[0],r=c.getBoundingClientRect();
  handleClick((t.clientX-r.left)*c.width/r.width,(t.clientY-r.top)*c.height/r.height);
},{passive:false});

function loop(){
  if(state==="start")drawStart();
  else if(state==="play")drawPlay();
  else if(state==="win")drawWin();
  else if(state==="lose")drawLose();
  else if(state==="giveup")drawGiveUp();
  requestAnimationFrame(loop);
}
loop();
</script></body></html>'''
    return html.replace("__LEVEL_LABEL__", level_label).replace("__QUESTIONS_JS__", questions_js)


def render_milyoner():
    """Kim Milyoner Olmak Ister ana render fonksiyonu — CSS enjeksiyonu ile."""
    inject_common_css("myg")
    styled_header("Kim Milyoner Olmak Ister", "Premium HTML5 Oyunu", icon="💎")
