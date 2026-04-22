#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lise sorularını 500'e tamamla - Eksik: Coğrafya+2, Başkentler+10, Doğa+20, Türkiye+24, Spor+25, Matematik+25, Deyimler+25, Atasözleri+25 = 156"""
import pathlib, re
from collections import Counter

FILE = pathlib.Path(__file__).with_name("_by_lise.txt")

NEW = r'''
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
'''

with open(FILE, "a", encoding="utf-8") as f:
    f.write(NEW)

# Count
with open(FILE, "r", encoding="utf-8") as f:
    txt = f.read()
cats = re.findall(r'k:"([^"]+)"', txt)
c = Counter(cats)
print(f"Total: {len(cats)}")
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
