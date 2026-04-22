#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kim Milyoner Olmak İster — Başkent sorularını 40 ülkeye indir,
çıkan soruların yerine genel kültür soruları ekle.
"""
import pathlib, re
from collections import Counter

FILE = pathlib.Path(__file__).with_name("milyoner_game.py")

# ═══════════════════════════════════════════════
# 40 ÖNEMLİ ÜLKE LİSTESİ
# ═══════════════════════════════════════════════
IMPORTANT_40 = {
    # Americas (8)
    "ABD", "Kanada", "Meksika", "Brezilya", "Arjantin", "Kolombiya", "Şili", "Küba",
    # Western Europe (10)
    "İngiltere", "Fransa", "Almanya", "İtalya", "İspanya", "Ispanya",
    "Hollanda", "Belçika", "İsviçre", "Avusturya", "Portekiz",
    # Northern Europe (4)
    "İsveç", "Norveç", "Danimarka", "Finlandiya",
    # Balkans (5)
    "Yunanistan", "Bulgaristan", "Romanya", "Sırbistan", "Hırvatistan",
    # Eastern Europe (3)
    "Polonya", "Ukrayna", "Çekya",
    # Middle East (5)
    "İran", "Irak", "Mısır", "İsrail", "Suudi Arabistan",
    # Asia (4)
    "Çin", "Japonya", "Güney Kore", "Hindistan",
    # Oceania (1)
    "Avustralya",
    # Duplicates for alternate spellings
    "Bosna", "Bosna Hersek",
}

def is_baskent(q_text):
    return "başkent" in q_text.lower()

def get_country(q_text):
    m = re.match(r"(.+?)'", q_text)
    return m.group(1) if m else ""

def is_important_country(q_text):
    country = get_country(q_text)
    return country in IMPORTANT_40 or country == "Türkiye"

# ═══════════════════════════════════════════════
# YEDEK GENEL KÜLTÜR SORULARI (her seviye için)
# ═══════════════════════════════════════════════

# İlkokul GK yedekleri
GK_ILKOKUL_EASY = [
    '{q:"Hangisi bir çalgı aletidir?",a:["Kalem","Bağlama","Cetvel","Silgi"],c:1}',
    '{q:"Hangi renk kırmızı ve sarının karışımıdır?",a:["Mor","Yeşil","Turuncu","Mavi"],c:2}',
    '{q:"İnsan vücudunda kaç parmak vardır?",a:["8","10","12","20"],c:1}',
    '{q:"Hangisi bir kuştur?",a:["Kaplumbağa","Serçe","Kedi","Balık"],c:1}',
    '{q:"Hangi mevsimde çiçekler açar?",a:["Kış","Sonbahar","İlkbahar","Yaz"],c:2}',
    '{q:"19 Mayıs hangi bayramdır?",a:["Zafer","Cumhuriyet","Çocuk","Gençlik ve Spor"],c:3}',
    '{q:"Hangisi bir süt ürünüdür?",a:["Ekmek","Peynir","Pirinç","Domates"],c:1}',
    '{q:"Bir saatte kaç dakika vardır?",a:["30","45","60","100"],c:2}',
    '{q:"Hangi organ ile görürüz?",a:["Kulak","Burun","Göz","Ağız"],c:2}',
    '{q:"Hangisi denizde yaşamaz?",a:["Yunus","Köpekbalığı","Kartal","Ahtapot"],c:2}',
    '{q:"Yağmur hangi buluttan yağar?",a:["Beyaz bulut","Kara bulut","Parlak bulut","Küçük bulut"],c:1}',
    '{q:"Hangisi bir spor dalıdır?",a:["Resim","Müzik","Yüzme","Okuma"],c:2}',
    '{q:"Ay hangi gökcismidir?",a:["Yıldız","Gezegen","Uydu","Güneş"],c:2}',
    '{q:"İnsan vücudunda kaç diş olur (yetişkin)?",a:["20","28","32","36"],c:2}',
    '{q:"Hangisi bir sebze değildir?",a:["Patlıcan","Biber","Muz","Havuç"],c:2}',
    '{q:"Bir dakikada kaç saniye vardır?",a:["30","50","60","100"],c:2}',
    '{q:"Hangisi bir kış sporudur?",a:["Yüzme","Kayak","Tenis","Bisiklet"],c:1}',
    '{q:"Hangi hayvan yumurtlamaz?",a:["Tavuk","Kaplumbağa","Kedi","Timsah"],c:2}',
    '{q:"Güneş sistemimizdeki en büyük gezegen hangisidir?",a:["Mars","Dünya","Jüpiter","Satürn"],c:2}',
    '{q:"Hangisi bir iletişim aracı değildir?",a:["Telefon","Mektup","Masa","E-posta"],c:2}',
    '{q:"Diş fırçalamak ne için önemlidir?",a:["Eğlence","Sağlık","Spor","Uyku"],c:1}',
    '{q:"Hangi hayvanın burnu çok uzundur?",a:["Kedi","Tavşan","Fil","Köpek"],c:2}',
    '{q:"Hangisi okyanustur?",a:["Akdeniz","Karadeniz","Pasifik","Van Gölü"],c:2}',
    '{q:"Bir yılda kaç hafta vardır?",a:["48","50","52","54"],c:2}',
    '{q:"Hangisi Atatürk\'ün sözüdür?",a:["Vatan sağolsun","Ne mutlu Türküm diyene","Dur yolcu","İlerle"],c:1}',
    '{q:"İstiklal Marşı\'nı kim yazmıştır?",a:["Atatürk","Mehmet Akif","Nazım Hikmet","Yunus Emre"],c:1}',
    '{q:"Türk bayrağında hangi semboller vardır?",a:["Güneş ve Yıldız","Ay ve Güneş","Ay ve Yıldız","Yıldız ve Çiçek"],c:2}',
    '{q:"Hangisi bir yazarımızdır?",a:["Barış Manço","Tarkan","Orhan Pamuk","İbrahim Tatlıses"],c:2}',
    '{q:"Hangisi Türkiye\'nin komşusu değildir?",a:["Yunanistan","İtalya","Gürcistan","Suriye"],c:1}',
    '{q:"En küçük kıtamız hangisidir?",a:["Asya","Avrupa","Avustralya","Afrika"],c:2}',
]

GK_ILKOKUL_MEDIUM = [
    '{q:"Hangi gezegen Güneş\'e en yakındır?",a:["Dünya","Venüs","Merkür","Mars"],c:2}',
    '{q:"Nobel ödülü hangi ülkede verilir?",a:["ABD","İngiltere","İsveç","Almanya"],c:2}',
    '{q:"Hangisi bir Türk halk oyunudur?",a:["Vals","Tango","Horon","Samba"],c:2}',
    '{q:"Piri Reis neyle ünlüdür?",a:["Şiir","Harita","Müzik","Resim"],c:1}',
    '{q:"Hangisi bir olimpiyat sporu değildir?",a:["Yüzme","Jimnastik","Bilardo","Atletizm"],c:2}',
    '{q:"Dünya\'nın en uzun nehri hangisidir?",a:["Amazon","Nil","Tuna","Mississippi"],c:1}',
    '{q:"Hangisi bir müzik türüdür?",a:["Figür","Caz","Rönesans","Barok"],c:1}',
    '{q:"İlk Türk kadın pilot kimdir?",a:["Halide Edip","Sabiha Gökçen","Afet İnan","Latife Hanım"],c:1}',
    '{q:"Hangisi bir kıta değildir?",a:["Avrupa","Asya","Akdeniz","Afrika"],c:2}',
    '{q:"Futbolda bir takım kaç kişidir?",a:["9","10","11","12"],c:2}',
    '{q:"En yüksek dağımız hangisidir?",a:["Uludağ","Erciyes","Süphan","Ağrı Dağı"],c:3}',
    '{q:"Hangisi bir Türk destanıdır?",a:["İlyada","Ergenekon","Odysseia","Şehname"],c:1}',
    '{q:"Hangisi bir nota değildir?",a:["Do","Re","Ka","Mi"],c:2}',
    '{q:"Yeşilay ne ile mücadele eder?",a:["Çevre kirliliği","Zararlı alışkanlıklar","Trafik","Yangın"],c:1}',
    '{q:"Hangisi Osmanlı padişahıdır?",a:["Cengiz Han","Fatih Sultan Mehmet","İskender","Sezar"],c:1}',
    '{q:"Kızılay ne yapar?",a:["Ağaç diker","Kan toplar ve yardım eder","Spor yapar","Yol yapar"],c:1}',
    '{q:"Hangi ülke pizza ile ünlüdür?",a:["Fransa","İtalya","Almanya","İngiltere"],c:1}',
    '{q:"Hangisi bir geleneksel Türk içeceğidir?",a:["Kola","Ayran","Sprite","Fanta"],c:1}',
    '{q:"Mevlana hangi şehirde yaşamıştır?",a:["İstanbul","Ankara","Konya","Bursa"],c:2}',
    '{q:"Galata Kulesi hangi şehirdedir?",a:["Ankara","İzmir","İstanbul","Bursa"],c:2}',
    '{q:"Hangisi bir Türk sporcudur?",a:["Messi","Ronaldo","Naim Süleymanoğlu","Neymar"],c:2}',
    '{q:"Hangisi bir gezegenimiz değildir?",a:["Mars","Plüton","Jüpiter","Satürn"],c:1}',
    '{q:"Dünya hangi galakside yer alır?",a:["Andromeda","Samanyolu","Büyük Ayı","Küçük Ayı"],c:1}',
    '{q:"Hangisi UNESCO Dünya Mirası\'dır?",a:["Ankara Kalesi","Pamukkale","Taksim Meydanı","Kızılay"],c:1}',
    '{q:"Hangisi bir Türk yemeğidir?",a:["Sushi","Pizza","Mantı","Paella"],c:2}',
    '{q:"Posta güvercini ne için kullanılırdı?",a:["Yarış","Haberleşme","Süs","Avlanma"],c:1}',
    '{q:"Hangisi bir deniz canlısı değildir?",a:["Yunus","Köpekbalığı","Kartal","Denizanası"],c:2}',
    '{q:"Olimpiyat oyunları kaç yılda bir yapılır?",a:["2","3","4","5"],c:2}',
    '{q:"Hangisi bir Türk masalıdır?",a:["Pamuk Prenses","Keloğlan","Rapunzel","Sindirella"],c:1}',
    '{q:"Hangi hayvan çok yavaş hareket eder?",a:["Çita","Tavşan","Kaplumbağa","At"],c:2}',
]

GK_ILKOKUL_HARD = [
    '{q:"Evliya Çelebi neyle ünlüdür?",a:["Resim","Seyahatname","Müzik","Şiir"],c:1}',
    '{q:"Hangisi Atatürk\'ün yaptığı inkılaplardandır?",a:["Matbaa","Harf İnkılabı","Telgraf","Radyo"],c:1}',
    '{q:"Dünya\'nın en büyük okyanusu hangisidir?",a:["Atlantik","Hint","Pasifik","Arktik"],c:2}',
    '{q:"Hangisi bir Rönesans sanatçısıdır?",a:["Picasso","Leonardo da Vinci","Van Gogh","Monet"],c:1}',
    '{q:"Hangi icat Thomas Edison\'a aittir?",a:["Telefon","Ampul","Radyo","Televizyon"],c:1}',
    '{q:"FIFA Dünya Kupası hangi spordadır?",a:["Basketbol","Voleybol","Futbol","Tenis"],c:2}',
    '{q:"Hangisi Türkiye\'nin yedi bölgesinden biri değildir?",a:["Marmara","Trakya","Akdeniz","Karadeniz"],c:1}',
    '{q:"Göreme hangi ilimizde yer alır?",a:["Kayseri","Nevşehir","Aksaray","Niğde"],c:1}',
    '{q:"Hangi müzik aleti telli çalgıdır?",a:["Davul","Flüt","Gitar","Trompet"],c:2}',
    '{q:"Türk edebiyatının en ünlü şairlerinden biri kimdir?",a:["Newton","Einstein","Yunus Emre","Pasteur"],c:2}',
    '{q:"Hangisi bir Akdeniz ülkesi değildir?",a:["İtalya","Yunanistan","Norveç","İspanya"],c:2}',
    '{q:"Dünya\'nın en kalabalık ülkesi hangisidir?",a:["ABD","Hindistan","Rusya","Brezilya"],c:1}',
    '{q:"Hangi buluşu Graham Bell yapmıştır?",a:["Ampul","Telefon","Radyo","Bilgisayar"],c:1}',
    '{q:"Mozart hangi ülkedendir?",a:["Almanya","İtalya","Avusturya","Fransa"],c:2}',
    '{q:"Hangisi bir su sporudur?",a:["Boks","Güreş","Kürek","Karate"],c:2}',
    '{q:"Nasrettin Hoca hangi ilimizden gelmiştir?",a:["Konya","Ankara","Aksaray","Eskişehir"],c:0}',
    '{q:"Hangi hayvan gece görüşü en iyi olandır?",a:["Tavuk","Baykuş","Güvercin","Serçe"],c:1}',
    '{q:"Hangisi Yedi Harika\'dandır?",a:["Eyfel Kulesi","Mısır Piramitleri","Big Ben","Kız Kulesi"],c:1}',
    '{q:"Dünya\'nın en soğuk kıtası hangisidir?",a:["Avrupa","Asya","Antarktika","Kuzey Amerika"],c:2}',
    '{q:"Hangisi bir Nobel dalıdır?",a:["Spor","Edebiyat","Tarih","Coğrafya"],c:1}',
    '{q:"Hangi padişah döneminde İstanbul fethedildi?",a:["Yavuz","Kanuni","Fatih","Murat"],c:2}',
    '{q:"Hangisi bir olimpiyat sembolüdür?",a:["Yıldız","Beş halka","Üçgen","Kare"],c:1}',
    '{q:"Venedik hangi ülkededir?",a:["Fransa","İspanya","İtalya","Yunanistan"],c:2}',
    '{q:"Barış Manço hangi alanda ünlüdür?",a:["Spor","Müzik","Edebiyat","Sinema"],c:1}',
    '{q:"Hangisi bir takım sporu değildir?",a:["Futbol","Basketbol","Tenis","Voleybol"],c:2}',
    '{q:"Dünya\'nın en uzun duvarı hangisidir?",a:["Berlin Duvarı","Çin Seddi","Adriyatik Duvarı","Roma Duvarı"],c:1}',
    '{q:"Hangisi bir geleneksel Türk el sanatıdır?",a:["Origami","Ebru","Bonsai","İkebana"],c:1}',
    '{q:"Ay\'a ilk ayak basan insan kimdir?",a:["Gagarin","Armstrong","Aldrin","Collins"],c:1}',
    '{q:"Hangisi bir Türk marşıdır?",a:["Marseyyez","İstiklal Marşı","God Save","Star Spangled"],c:1}',
    '{q:"Çanakkale Savaşı hangi savaşın parçasıdır?",a:["Kurtuluş Savaşı","I. Dünya Savaşı","II. Dünya Savaşı","Balkan Savaşı"],c:1}',
]

GK_ILKOKUL_VHARD = [
    '{q:"Dünyanın en derin noktası neresidir?",a:["Everest","Mariana Çukuru","Amazon","Büyük Kanyon"],c:1}',
    '{q:"Hangi bilim insanı yerçekimini keşfetti?",a:["Einstein","Galileo","Newton","Darwin"],c:2}',
    '{q:"Hangisi Picasso\'nun bir eseridir?",a:["Mona Lisa","Guernica","Yıldızlı Gece","Çığlık"],c:1}',
    '{q:"Olimpiyat bayrağında kaç halka vardır?",a:["3","4","5","6"],c:2}',
    '{q:"Efes Antik Kenti hangi ilimizde yer alır?",a:["Aydın","İzmir","Muğla","Denizli"],c:1}',
    '{q:"Hangisi bir Türk bilim insanıdır?",a:["Einstein","Aziz Sancar","Newton","Pasteur"],c:1}',
    '{q:"Dünya\'nın en büyük çölü hangisidir?",a:["Gobi","Sahra","Atacama","Kalahari"],c:1}',
    '{q:"Hangisi klasik müzik bestecisidir?",a:["Beatles","Beethoven","Elvis","Madonna"],c:1}',
    '{q:"Sümerlerin icadı olan yazı türü hangisidir?",a:["Hiyeroglif","Çivi yazısı","Latin","Arap"],c:1}',
    '{q:"Hangi sanatçı \'Yıldızlı Gece\' tablosunu yapmıştır?",a:["Picasso","Monet","Van Gogh","Da Vinci"],c:2}',
    '{q:"Türkiye\'nin en eski şehirlerinden biri hangisidir?",a:["Ankara","İstanbul","Çatalhöyük","İzmir"],c:2}',
    '{q:"Hangisi bir Türk filmidir?",a:["Titanik","Babam ve Oğlum","Harry Potter","Avatar"],c:1}',
    '{q:"Uzay\'a giden ilk insan kimdir?",a:["Armstrong","Gagarin","Aldrin","Glenn"],c:1}',
    '{q:"Hangisi bir dünya klasiği romandır?",a:["Çalıkuşu","Don Kişot","Sinekli Bakkal","Yaprak Dökümü"],c:1}',
    '{q:"Wimbledon hangi sporun turnuvasıdır?",a:["Golf","Futbol","Tenis","Kriket"],c:2}',
    '{q:"Hangisi antik uygarlıklardan biridir?",a:["Osmanlı","Roma","Selçuklu","Safevi"],c:1}',
    '{q:"Topkapı Sarayı hangi şehirdedir?",a:["Ankara","Edirne","İstanbul","Bursa"],c:2}',
    '{q:"Hangisi bir müzik notası değildir?",a:["Sol","La","Pa","Si"],c:2}',
    '{q:"Shakespeare hangi ülkedendir?",a:["Fransa","İtalya","İngiltere","Almanya"],c:2}',
    '{q:"Nuh\'un Gemisi efsanesi hangi dağla ilişkilidir?",a:["Uludağ","Erciyes","Ağrı","Süphan"],c:2}',
    '{q:"Hangisi bir dans türü değildir?",a:["Vals","Tango","Akrostiş","Samba"],c:2}',
    '{q:"Frida Kahlo hangi sanat dalında ünlüdür?",a:["Müzik","Resim","Edebiyat","Heykel"],c:1}',
    '{q:"Hangisi bir su altı sporu değildir?",a:["Dalış","Sörfing","Eskrim","Yüzme"],c:2}',
    '{q:"Dünya\'nın en yüksek binası hangi ülkededir?",a:["ABD","Çin","BAE","Malezya"],c:2}',
    '{q:"Hangisi bir Türk tatlısıdır?",a:["Tiramisu","Baklava","Cheesecake","Brownie"],c:1}',
    '{q:"Einstein hangi alanda Nobel almıştır?",a:["Kimya","Edebiyat","Fizik","Tıp"],c:2}',
    '{q:"Hangisi bir kış olimpiyat sporudur?",a:["Yüzme","Buz pateni","Bisiklet","Atletizm"],c:1}',
    '{q:"Türkiye\'de en çok konuşulan ikinci dil hangisidir?",a:["Arapça","Kürtçe","İngilizce","Almanca"],c:1}',
    '{q:"Hangisi bir tarihi yapıdır?",a:["AVM","Selimiye Camii","Stadyum","Havalimanı"],c:1}',
    '{q:"Magellan neyle ünlüdür?",a:["Resim","Dünya turu","Müzik","Şiir"],c:1}',
]

# Ortaokul GK yedekleri
GK_ORTAOKUL_EASY = [
    '{q:"Hangisi bir Rönesans dönemi sanatçısıdır?",a:["Picasso","Michelangelo","Monet","Van Gogh"],c:1}',
    '{q:"Olimpiyat Oyunları ilk olarak hangi ülkede düzenlendi?",a:["Roma","Mısır","Yunanistan","İran"],c:2}',
    '{q:"Hangisi bir Türk destanıdır?",a:["İlyada","Oğuz Kağan","Odysseia","Beowulf"],c:1}',
    '{q:"Futbolda dünya kupasını en çok kazanan ülke hangisidir?",a:["Almanya","Arjantin","İtalya","Brezilya"],c:3}',
    '{q:"Hangisi Nobel ödülü alan Türk yazardır?",a:["Yaşar Kemal","Orhan Pamuk","Nazım Hikmet","Ahmet Hamdi Tanpınar"],c:1}',
    '{q:"En büyük kıta hangisidir?",a:["Afrika","Avrupa","Asya","Kuzey Amerika"],c:2}',
    '{q:"Türkiye hangi kıtada yer alır?",a:["Sadece Avrupa","Sadece Asya","Avrupa ve Asya","Afrika"],c:2}',
    '{q:"İstiklal Marşı hangi yıl kabul edilmiştir?",a:["1920","1921","1923","1924"],c:1}',
    '{q:"Hangisi bir klasik müzik bestecisidir?",a:["Beatles","Tarkan","Bach","Sezen Aksu"],c:2}',
    '{q:"Hangisi bir takımyıldızıdır?",a:["Mars","Venüs","Büyük Ayı","Jüpiter"],c:2}',
    '{q:"Hangisi bir kış sporudur?",a:["Tenis","Yüzme","Biatlon","Basketbol"],c:2}',
    '{q:"Hangisi UNESCO Dünya Mirası listesinde yer alır?",a:["Ankara Kalesi","Kapadokya","Taksim","Kızılay"],c:1}',
    '{q:"Hangisi bir Türk filmidir?",a:["Titanik","Ayla","Avatar","Star Wars"],c:1}',
    '{q:"Dünya nüfusu yaklaşık kaç milyardır?",a:["5","6","8","10"],c:2}',
    '{q:"Kuran-ı Kerim kaç sureden oluşur?",a:["100","114","120","124"],c:1}',
    '{q:"Hangisi bir deniz aracı türüdür?",a:["Planör","Helikopter","Fırkateyn","Lokomotif"],c:2}',
    '{q:"Hangisi antik yedi harikadan biridir?",a:["Eyfel Kulesi","İskenderiye Feneri","Özgürlük Heykeli","Big Ben"],c:1}',
    '{q:"Türkiye\'nin en büyük stadyumu hangisidir?",a:["Ali Sami Yen","Atatürk Olimpiyat","Şükrü Saracoğlu","İnönü"],c:1}',
    '{q:"Hangisi bir dans türüdür?",a:["Sonnet","Haiku","Flamenko","Heykel"],c:2}',
    '{q:"Dünya\'nın en küçük ülkesi hangisidir?",a:["Monako","Liechtenstein","Vatikan","San Marino"],c:2}',
    '{q:"Hangisi bir Türk müzik aletidir?",a:["Piyano","Gitar","Ney","Flüt"],c:2}',
    '{q:"Hangi sporda \'set\' kavramı kullanılır?",a:["Futbol","Voleybol","Atletizm","Güreş"],c:1}',
    '{q:"Hangisi bir roman türüdür?",a:["Sonet","Gazel","Polisiye","Kaside"],c:2}',
    '{q:"Eskişehir hangi bölgemizdedir?",a:["Marmara","Ege","İç Anadolu","Karadeniz"],c:2}',
    '{q:"Hangisi Osmanlı mimarisinin eseridir?",a:["Eyfel Kulesi","Süleymaniye Camii","Big Ben","Kolezyum"],c:1}',
    '{q:"Hangisi bir kıtalar arası yarışmadır?",a:["Premier Lig","La Liga","Şampiyonlar Ligi","Serie A"],c:2}',
    '{q:"Hangisi bir Türk ressam değildir?",a:["Osman Hamdi Bey","İbrahim Çallı","Pablo Picasso","Fikret Muallâ"],c:2}',
    '{q:"Euro para birimi kaç ülkede kullanılır?",a:["10","15","20","27"],c:2}',
    '{q:"Hangisi bir klasik Türk edebiyatı nazım biçimidir?",a:["Roman","Gazel","Makale","Hikaye"],c:1}',
    '{q:"Hangisi bir buz sporu değildir?",a:["Buz hokeyi","Curling","Buz pateni","Badminton"],c:3}',
]

GK_ORTAOKUL_MEDIUM = [
    '{q:"Mona Lisa tablosu hangi müzededir?",a:["British Museum","Uffizi","Louvre","Prado"],c:2}',
    '{q:"Hangisi bir Osmanlı sadrazamıdır?",a:["Kanuni","Sokullu Mehmet Paşa","İbni Sina","Yavuz"],c:1}',
    '{q:"Hangisi olimpiyat dalı değildir?",a:["Okçuluk","Kriket","Halter","Eskrim"],c:1}',
    '{q:"Charlie Chaplin hangi sanat dalında ünlüdür?",a:["Resim","Müzik","Sinema","Edebiyat"],c:2}',
    '{q:"Anadolu Medeniyetleri Müzesi hangi şehirdedir?",a:["İstanbul","Ankara","İzmir","Antalya"],c:1}',
    '{q:"Hangisi bir spor terimdir?",a:["Sone","Ofsayt","Gazel","Rönesans"],c:1}',
    '{q:"Türkiye\'nin ilk kadın milletvekilleri hangi yıl seçildi?",a:["1930","1934","1938","1946"],c:1}',
    '{q:"Hangisi bir bale terimi değildir?",a:["Plié","Arabesque","Crescendo","Pirouette"],c:2}',
    '{q:"Dünya\'nın en yüksek dağı hangisidir?",a:["K2","Kilimanjaro","Everest","Mont Blanc"],c:2}',
    '{q:"Hangisi bir müzik dönemidir?",a:["Rönesans","Gotik","Barok","Neolitik"],c:2}',
    '{q:"Hangisi bir Türk sporcudur?",a:["Usain Bolt","Halil Mutlu","Michael Phelps","Roger Federer"],c:1}',
    '{q:"Sümela Manastırı hangi ilimizdedir?",a:["Rize","Trabzon","Artvin","Giresun"],c:1}',
    '{q:"Hangisi bir edebiyat akımıdır?",a:["Kübizm","Barok","Romantizm","Gotik"],c:2}',
    '{q:"Dünya\'nın en büyük gölü hangisidir?",a:["Van Gölü","Baykal","Hazar","Victoria"],c:2}',
    '{q:"Hangisi bir Türk bestecisidir?",a:["Vivaldi","Itri","Mozart","Bach"],c:1}',
    '{q:"Akdeniz Oyunları kaç yılda bir düzenlenir?",a:["2","3","4","5"],c:2}',
    '{q:"Hangisi bir tiyatro türüdür?",a:["Roman","Hikaye","Komedi","Masal"],c:2}',
    '{q:"Türkiye\'nin en uzun nehri hangisidir?",a:["Fırat","Kızılırmak","Dicle","Sakarya"],c:1}',
    '{q:"Hangisi bir heykel sanatçısıdır?",a:["Monet","Rodin","Beethoven","Shakespeare"],c:1}',
    '{q:"Tour de France hangi sporun yarışıdır?",a:["Koşu","Bisiklet","Yüzme","Kayak"],c:1}',
    '{q:"Hangisi eski Mısır\'ın sembolüdür?",a:["Kolezyum","Piramitler","Akropolis","Machu Picchu"],c:1}',
    '{q:"Hangisi bir Türk şairidir?",a:["Byron","Goethe","Fuzuli","Hugo"],c:2}',
    '{q:"Dünya sağlık örgütünün kısaltması nedir?",a:["UNESCO","WHO","NATO","UNICEF"],c:1}',
    '{q:"Hangisi bir olimpiyat disiplini değildir?",a:["Triatlon","Modern Pentatlon","Darts","Jimnastik"],c:2}',
    '{q:"Dolmabahçe Sarayı hangi şehirdedir?",a:["Ankara","İstanbul","Edirne","Bursa"],c:1}',
    '{q:"Hangisi bir sanat akımıdır?",a:["Merkantilizm","Emperyalizm","Empresyonizm","Feodalizm"],c:2}',
    '{q:"UEFA Şampiyonlar Ligi kupası hangi ülkede en çok kazanıldı?",a:["İngiltere","İtalya","İspanya","Almanya"],c:2}',
    '{q:"Hangisi bir Japon sanatıdır?",a:["Ebru","Origami","Minyatür","Fresk"],c:1}',
    '{q:"La Scala hangi ülkedeki ünlü opera binasıdır?",a:["Fransa","İngiltere","İtalya","Avusturya"],c:2}',
    '{q:"Türk mutfağının vazgeçilmez yemeği hangisidir?",a:["Sushi","Kebap","Pizza","Paella"],c:1}',
]

GK_ORTAOKUL_HARD = [
    '{q:"Galileo Galilei neyi keşfetmiştir?",a:["Amerika","Jüpiter uyduları","Penisilin","DNA"],c:1}',
    '{q:"Hangisi bir Osmanlı minyatür sanatçısıdır?",a:["Matrakçı Nasuh","Da Vinci","Monet","Rembrandt"],c:0}',
    '{q:"Dünya Kupası\'nı en çok kazanan futbol takımı hangisidir?",a:["Almanya","İtalya","Brezilya","Arjantin"],c:2}',
    '{q:"Hangisi bir opera bestecisidir?",a:["Bach","Verdi","Chopin","Liszt"],c:1}',
    '{q:"Troya Antik Kenti hangi ilimizde yer alır?",a:["İzmir","Çanakkale","Balıkesir","Edirne"],c:1}',
    '{q:"Formula 1\'de en çok şampiyonluk kazanan pilot kimdir?",a:["Senna","Schumacher","Hamilton","Vettel"],c:2}',
    '{q:"Hangisi bir Türk romanıdır?",a:["Savaş ve Barış","Suç ve Ceza","Çalıkuşu","Don Kişot"],c:2}',
    '{q:"Kremlin hangi ülkededir?",a:["Çin","İngiltere","Rusya","Fransa"],c:2}',
    '{q:"Hangisi bir dans yarışması formatıdır?",a:["Survivor","MasterChef","Dancing with Stars","The Voice"],c:2}',
    '{q:"Uzayda yürüyen ilk kadın astronot kimdir?",a:["Sally Ride","Valentina Tereşkova","Svetlana Savitskaya","Mae Jemison"],c:2}',
    '{q:"Hangisi bir Türk hat sanatçısıdır?",a:["Matisse","Hamid Aytaç","Renoir","Cézanne"],c:1}',
    '{q:"Dünya\'nın en uzun köprüsü hangi ülkededir?",a:["ABD","Japonya","Çin","İngiltere"],c:2}',
    '{q:"Hangisi bir müzik festivalidir?",a:["Cannes","Sundance","Eurovision","Oscar"],c:2}',
    '{q:"Pekin Operası hangi ülkenin sanatıdır?",a:["Japonya","Kore","Çin","Vietnam"],c:2}',
    '{q:"Hangisi bir kış olimpiyat sporu değildir?",a:["Kayaklı koşu","Curling","Badminton","Biatlon"],c:2}',
    '{q:"Türkiye\'nin ilk olimpiyat madalyası hangi spordandır?",a:["Halter","Güreş","Boks","Atletizm"],c:1}',
    '{q:"Hangisi bir fotoğraf sanatçısıdır?",a:["Ansel Adams","Beethoven","Chopin","Shakespeare"],c:0}',
    '{q:"Super Bowl hangi sporun final maçıdır?",a:["Basketbol","Beyzbol","Amerikan Futbolu","Buz Hokeyi"],c:2}',
    '{q:"Hangisi bir Türk mimari eseridir?",a:["Taj Mahal","Selimiye Camii","Sagrada Familia","Notre Dame"],c:1}',
    '{q:"Milli Mücadele döneminin ünlü kadın kahramanı kimdir?",a:["Halide Edip Adıvar","Sabiha Gökçen","Afet İnan","Latife Hanım"],c:0}',
    '{q:"Hangisi bir Akdeniz yemeğidir?",a:["Sushi","Ramen","Hummus","Dim Sum"],c:2}',
    '{q:"Emmy ödülü hangi alandadır?",a:["Sinema","Televizyon","Müzik","Edebiyat"],c:1}',
    '{q:"Hangisi bir su sporu değildir?",a:["Yelken","Kano","Eskrim","Sörf"],c:2}',
    '{q:"Osmanlı\'da ilk matbaa ne zaman kuruldu?",a:["1629","1727","1839","1876"],c:1}',
    '{q:"Hangisi bir müze değildir?",a:["Prado","Hermitage","Wimbledon","Uffizi"],c:2}',
    '{q:"Dünya Atletizm Şampiyonası kaç yılda bir yapılır?",a:["Her yıl","2 yılda","3 yılda","4 yılda"],c:1}',
    '{q:"Hangisi bir Türk filmi yönetmenidir?",a:["Spielberg","Nuri Bilge Ceylan","Tarantino","Scorsese"],c:1}',
    '{q:"Avrupa Birliği\'nin merkezi hangi şehirdedir?",a:["Paris","Berlin","Brüksel","Viyana"],c:2}',
    '{q:"Hangisi bir Türk marşıdır?",a:["La Marseillaise","İzmir Marşı","Star Spangled","God Save"],c:1}',
    '{q:"Roland Garros hangi spor dalının turnuvasıdır?",a:["Golf","Tenis","Kriket","Polo"],c:1}',
]

GK_ORTAOKUL_VHARD = [
    '{q:"Altın Küre ödülü hangi alandadır?",a:["Edebiyat","Spor","Sinema ve TV","Müzik"],c:2}',
    '{q:"Hangisi bir savaş sanatıdır?",a:["Origami","Aikido","Bonsai","İkebana"],c:1}',
    '{q:"Dünya\'nın en eski üniversitesi hangi ülkededir?",a:["İngiltere","İtalya","Fas","Mısır"],c:2}',
    '{q:"Hangisi bir Türk halk hikayesidir?",a:["Romeo ve Juliet","Ferhat ile Şirin","Hamlet","Antigone"],c:1}',
    '{q:"NBA\'de en çok şampiyonluk kazanan takım hangisidir?",a:["Lakers","Celtics","Bulls","Warriors"],c:1}',
    '{q:"Hangisi bir çağdaş sanat akımıdır?",a:["Gotik","Pop Art","Romanik","Barok"],c:1}',
    '{q:"Efes Celsus Kütüphanesi kaç yılında inşa edildi?",a:["MS 100","MS 135","MS 200","MS 250"],c:1}',
    '{q:"Hangisi bir yönetmen değildir?",a:["Kubrick","Hitchcock","Hemingway","Coppola"],c:2}',
    '{q:"Maratona adını veren savaş hangi ülkede yapıldı?",a:["İtalya","Türkiye","Yunanistan","Mısır"],c:2}',
    '{q:"Hangisi bir geleneksel Japon tiyatrosudur?",a:["Kabuki","Flamenco","Opera","Bale"],c:0}',
    '{q:"Grammy ödülü hangi alandadır?",a:["Sinema","Edebiyat","Müzik","Tiyatro"],c:2}',
    '{q:"Hangisi dünyaca ünlü bir Türk edebiyatçıdır?",a:["Tolstoy","Elif Şafak","Hugo","Dickens"],c:1}',
    '{q:"Usain Bolt hangi mesafede dünya rekoru kırmıştır?",a:["200m","400m","100m","800m"],c:2}',
    '{q:"Hangisi bir heykel türüdür?",a:["Fresk","Rölyef","Mozaik","Vitray"],c:1}',
    '{q:"İpek Yolu nereden nereye uzanırdı?",a:["Roma-Mısır","Çin-Avrupa","Hindistan-Afrika","Japonya-Rusya"],c:1}',
    '{q:"Hangisi bir Türk destanı değildir?",a:["Manas","Oğuz Kağan","İlyada","Ergenekon"],c:2}',
    '{q:"Wimbledon turnuvası hangi yüzeyde oynanır?",a:["Toprak","Çim","Sert zemin","Halı"],c:1}',
    '{q:"Hangisi bir bale yapıtıdır?",a:["Carmen","Kuğu Gölü","Boheme","Tosca"],c:1}',
    '{q:"Cannes Film Festivali hangi ülkede düzenlenir?",a:["İtalya","İspanya","Fransa","Almanya"],c:2}',
    '{q:"Hangisi Osmanlı döneminde yazılmış bir eserdir?",a:["İlyada","Leyla ile Mecnun","Don Kişot","Hamlet"],c:1}',
    '{q:"Modern pentatlonda kaç disiplin vardır?",a:["3","4","5","6"],c:2}',
    '{q:"Hangisi bir Türk sinema ödülüdür?",a:["Oscar","BAFTA","Altın Portakal","Cannes Palmiye"],c:2}',
    '{q:"Rönesans hangi yüzyılda başlamıştır?",a:["12.","13.","14.","15."],c:2}',
    '{q:"Hangisi bir buz dansı figürüdür?",a:["Libre","Twist","Twizzle","Rumba"],c:2}',
    '{q:"Dünya\'nın en çok ziyaret edilen müzesi hangisidir?",a:["British Museum","Met","Louvre","Hermitage"],c:2}',
    '{q:"Hangisi bir Türk mimarıdır?",a:["Gaudi","Mimar Sinan","Le Corbusier","Frank Lloyd Wright"],c:1}',
    '{q:"Hangisi paralimpik spor değildir?",a:["Tekerlekli sandalye basketbol","Goalball","Polo","Boccia"],c:2}',
    '{q:"Aşık Veysel hangi sanat dalında ünlüdür?",a:["Resim","Müzik ve Şiir","Heykel","Sinema"],c:1}',
    '{q:"Hangisi bir film türü değildir?",a:["Western","Film Noir","Sone","Thriller"],c:2}',
    '{q:"Dünya Satranç Şampiyonası\'nı en uzun süre elinde tutan kimdir?",a:["Fischer","Kasparov","Carlsen","Karpov"],c:1}',
]

# Lise ve Yetişkin GK yedekleri benzer yapıda
GK_LISE_EASY = [
    '{q:"Rönesans hangi ülkede başlamıştır?",a:["Fransa","İngiltere","İtalya","Almanya"],c:2}',
    '{q:"Hangisi bir empresyonist ressamdır?",a:["Picasso","Monet","Dalí","Warhol"],c:1}',
    '{q:"Olimpiyat ateşi nerede yakılır?",a:["Roma","Atina","Paris","Londra"],c:1}',
    '{q:"Hangisi bir Türk Nobel ödüllüsüdür?",a:["Yaşar Kemal","Orhan Pamuk","Nazım Hikmet","Cemal Süreya"],c:1}',
    '{q:"Hangisi bir opera bestecisi değildir?",a:["Verdi","Puccini","Chopin","Wagner"],c:2}',
    '{q:"En çok Oscar ödülü alan film hangisidir?",a:["Titanic","Avatar","Ben-Hur","Godfather"],c:2}',
    '{q:"Hangisi bir UNESCO Dünya Mirası değildir?",a:["Göbeklitepe","Efes","Anıtkabir","Troya"],c:2}',
    '{q:"Sürrealizm akımının kurucusu kimdir?",a:["Monet","André Breton","Picasso","Dalí"],c:1}',
    '{q:"Hangisi bir tenis Grand Slam turnuvası değildir?",a:["Wimbledon","Roland Garros","Masters","US Open"],c:2}',
    '{q:"Dünya\'nın en büyük adasını hangi ülke yönetir?",a:["Kanada","ABD","Danimarka","İngiltere"],c:2}',
    '{q:"Hangisi bir barok dönem bestecisidir?",a:["Mozart","Beethoven","Vivaldi","Chopin"],c:2}',
    '{q:"İstanbul hangi yılda Avrupa Kültür Başkenti oldu?",a:["2005","2008","2010","2012"],c:2}',
    '{q:"Hangisi bir fotoğrafçılık terimi değildir?",a:["Diyafram","Enstantane","Crescendo","ISO"],c:2}',
    '{q:"Dünya\'nın en eski medeniyeti hangisidir?",a:["Mısır","Sümer","Roma","Yunan"],c:1}',
    '{q:"Hangisi bir Türk ozanıdır?",a:["Shakespeare","Pir Sultan Abdal","Goethe","Byron"],c:1}',
    '{q:"Hangisi bir dövüş sanatı değildir?",a:["Judo","Aikido","Pilates","Karate"],c:2}',
    '{q:"Pulitzer ödülü hangi alandadır?",a:["Sinema","Müzik","Gazetecilik ve Edebiyat","Bilim"],c:2}',
    '{q:"Osmanlı İmparatorluğu kaç yıl sürmüştür?",a:["400","500","600","700"],c:2}',
    '{q:"Hangisi bir tiyatro yazarıdır?",a:["Chopin","Molière","Monet","Vivaldi"],c:1}',
    '{q:"Avrupa Futbol Şampiyonası kaç yılda bir yapılır?",a:["2","3","4","5"],c:2}',
    '{q:"Hangisi bir Türk destanıdır?",a:["Kalevala","Nibelungen","Dede Korkut","Beowulf"],c:2}',
    '{q:"Dünya\'nın en kalabalık şehri hangisidir?",a:["Pekin","New York","Tokyo","İstanbul"],c:2}',
    '{q:"Hangisi bir müzik aleti ailesi değildir?",a:["Yaylılar","Üflemeliler","Vurmalılar","Çizgiler"],c:3}',
    '{q:"Selçuklu mimarisinin en önemli eseri hangisidir?",a:["Topkapı","Dolmabahçe","Divriği Ulu Camii","Süleymaniye"],c:2}',
    '{q:"Hangisi bir sanat galerisi değildir?",a:["Tate Modern","MoMA","Wimbledon","Guggenheim"],c:2}',
    '{q:"Hangisi bir antik uygarlık değildir?",a:["Hitit","Sümer","Osmanlı","Lidya"],c:2}',
    '{q:"Cannes\'da verilen en büyük ödül nedir?",a:["Altın Ayı","Altın Palmiye","Altın Aslan","Altın Küre"],c:1}',
    '{q:"Hangisi bir Türk sporcusu değildir?",a:["Naim Süleymanoğlu","Halil Mutlu","Roger Federer","Taha Akgül"],c:2}',
    '{q:"Piramitler hangi medeniyete aittir?",a:["Roma","Yunan","Mısır","Pers"],c:2}',
    '{q:"Hangisi bir edebiyat türü değildir?",a:["Roman","Hikaye","Sonat","Şiir"],c:2}',
]

GK_LISE_MEDIUM = GK_ORTAOKUL_HARD.copy()  # reuse — different level
GK_LISE_HARD = GK_ORTAOKUL_VHARD.copy()

GK_LISE_VHARD = [
    '{q:"Hangisi bir postmodern romancıdır?",a:["Tolstoy","Dostoyevski","Italo Calvino","Hugo"],c:2}',
    '{q:"Stravinsky hangi müzik döneminin bestecisidir?",a:["Barok","Klasik","Romantik","Modern"],c:3}',
    '{q:"Hangisi bir felsefe akımıdır?",a:["Kübizm","Fovizm","Varoluşçuluk","Dadaizm"],c:2}',
    '{q:"Bir futbol takımında toplam kaç oyuncu forma giyebilir?",a:["16","18","20","23"],c:1}',
    '{q:"Hangisi bir Japon savaş sanatı değildir?",a:["Kendo","Sumo","Capoeira","Jujitsu"],c:2}',
    '{q:"Dünya\'nın en pahalı tablosu kime aittir?",a:["Picasso","Da Vinci","Van Gogh","Monet"],c:1}',
    '{q:"Hangisi bir edebiyat ödülüdür?",a:["Grammy","Emmy","Booker","Tony"],c:2}',
    '{q:"Machu Picchu hangi uygarlığa aittir?",a:["Aztek","Maya","İnka","Olmek"],c:2}',
    '{q:"Hangisi bir çağdaş dans türüdür?",a:["Menuet","Vals","Kontemporer","Polka"],c:2}',
    '{q:"F1\'de Monaco Grand Prix hangi şehirde yapılır?",a:["Nice","Cannes","Monte Carlo","Marsilya"],c:2}',
    '{q:"Hangisi bir Türk bilim insanı değildir?",a:["Aziz Sancar","Gazi Yaşargil","Marie Curie","Cahit Arf"],c:2}',
    '{q:"Dünya Sağlık Örgütü hangi yıl kuruldu?",a:["1945","1948","1951","1955"],c:1}',
    '{q:"Hangisi bir sinema ödülü değildir?",a:["Oscar","BAFTA","Pulitzer","César"],c:2}',
    '{q:"Berlin Film Festivali\'nin büyük ödülü nedir?",a:["Altın Palmiye","Altın Aslan","Altın Ayı","Altın Küre"],c:2}',
    '{q:"Hangisi bir Türk yazarı değildir?",a:["Sabahattin Ali","Halide Edip","Franz Kafka","Yaşar Kemal"],c:2}',
    '{q:"Dekatlon kaç disiplinden oluşur?",a:["5","8","10","12"],c:2}',
    '{q:"Hangisi bir mimari üslup değildir?",a:["Gotik","Art Deco","Empresyonizm","Barok"],c:2}',
    '{q:"Dünya\'nın en yüksek şelalesi hangisidir?",a:["Niagara","Angel","Victoria","Iguazu"],c:1}',
    '{q:"Hangisi bir Türk müzisyendir?",a:["Pavarotti","İdil Biret","Lang Lang","Yo-Yo Ma"],c:1}',
    '{q:"Kolezyum hangi şehirdedir?",a:["Atina","Kahire","Roma","İstanbul"],c:2}',
    '{q:"Hangisi bir fantastik edebiyat yazarıdır?",a:["Hemingway","Tolkien","Steinbeck","Chekhov"],c:1}',
    '{q:"Dünya Kupası\'nda en çok gol atan futbolcu kimdir?",a:["Pelé","Maradona","Miroslav Klose","Ronaldo"],c:2}',
    '{q:"Hangisi bir grafik sanatı türü değildir?",a:["Baskı","Gravür","Litografi","Füg"],c:3}',
    '{q:"Venedik Film Festivali\'nin büyük ödülü nedir?",a:["Altın Ayı","Altın Palmiye","Altın Aslan","BAFTA"],c:2}',
    '{q:"Hangisi bir Türk karikatüristidir?",a:["Charles Schulz","Turhan Selçuk","Hergé","Walt Disney"],c:1}',
    '{q:"Dünya\'nın en uzun kıyı şeridine sahip ülke hangisidir?",a:["Rusya","Endonezya","Kanada","Avustralya"],c:2}',
    '{q:"Hangisi bir müzikal değildir?",a:["Cats","Hamlet","Les Misérables","Phantom of the Opera"],c:1}',
    '{q:"Altın Portakal hangi şehirde düzenlenir?",a:["İstanbul","Ankara","Antalya","İzmir"],c:2}',
    '{q:"Hangisi bir yemek yarışmasıdır?",a:["The Voice","MasterChef","X Factor","Dancing Stars"],c:1}',
    '{q:"Türkiye\'nin en ünlü minyatürcüsü kimdir?",a:["Matrakçı Nasuh","Sinan","Itri","Evliya Çelebi"],c:0}',
]

GK_YETISKIN_EASY = GK_LISE_EASY.copy()
GK_YETISKIN_MEDIUM = GK_LISE_MEDIUM.copy()
GK_YETISKIN_HARD = GK_LISE_HARD.copy()
GK_YETISKIN_VHARD = GK_LISE_VHARD.copy()

ALL_REPLACEMENTS = {
    "ILKOKUL": {"easy": GK_ILKOKUL_EASY, "medium": GK_ILKOKUL_MEDIUM, "hard": GK_ILKOKUL_HARD, "very_hard": GK_ILKOKUL_VHARD},
    "ORTAOKUL": {"easy": GK_ORTAOKUL_EASY, "medium": GK_ORTAOKUL_MEDIUM, "hard": GK_ORTAOKUL_HARD, "very_hard": GK_ORTAOKUL_VHARD},
    "LISE": {"easy": GK_LISE_EASY, "medium": GK_LISE_MEDIUM, "hard": GK_LISE_HARD, "very_hard": GK_LISE_VHARD},
    "YETISKIN": {"easy": GK_YETISKIN_EASY, "medium": GK_YETISKIN_MEDIUM, "hard": GK_YETISKIN_HARD, "very_hard": GK_YETISKIN_VHARD},
}


def process():
    txt = FILE.read_text(encoding="utf-8")

    # Find each level block
    level_vars = [
        ("ILKOKUL", "_QUESTIONS_ILKOKUL"),
        ("ORTAOKUL", "_QUESTIONS_ORTAOKUL"),
        ("LISE", "_QUESTIONS_LISE"),
        ("YETISKIN", "_QUESTIONS_YETISKIN"),
    ]

    for lv_key, lv_var in level_vars:
        # Find the raw string boundaries
        marker = lv_var + ' = r"""'
        start = txt.find(marker)
        if start == -1:
            print(f"HATA: {lv_var} bulunamadı!")
            continue
        content_start = start + len(marker)
        end = txt.find('"""', content_start)

        block = txt[content_start:end]

        # Process each difficulty pool
        for diff in ["easy", "medium", "hard", "very_hard"]:
            diff_marker = diff + ":["
            d_start = block.find(diff_marker)
            if d_start == -1:
                continue

            # Find the closing bracket for this array
            bracket_depth = 0
            d_content_start = d_start + len(diff_marker)
            d_end = d_content_start
            in_string = False
            escape_next = False

            for i in range(d_content_start, len(block)):
                ch = block[i]
                if escape_next:
                    escape_next = False
                    continue
                if ch == '\\':
                    escape_next = True
                    continue
                if ch == '"':
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    if bracket_depth == 0:
                        d_end = i
                        break
                    bracket_depth -= 1

            pool_content = block[d_content_start:d_end]

            # Parse individual questions
            questions = re.findall(r'\{q:"[^"]*"[^}]*\}', pool_content)

            kept = []
            removed = 0
            for q_str in questions:
                q_match = re.search(r'q:"([^"]*)"', q_str)
                if not q_match:
                    kept.append(q_str)
                    continue
                q_text = q_match.group(1)
                if is_baskent(q_text):
                    if is_important_country(q_text):
                        kept.append(q_str)
                    else:
                        removed += 1
                else:
                    kept.append(q_str)

            # Add replacement GK questions
            replacements = ALL_REPLACEMENTS[lv_key][diff]
            added = 0
            for rep in replacements:
                if added >= removed:
                    break
                # Check for duplicate questions
                rep_q = re.search(r'q:"([^"]*)"', rep)
                if rep_q:
                    dup = False
                    for k in kept:
                        if rep_q.group(1) in k:
                            dup = True
                            break
                    if not dup:
                        kept.append(rep)
                        added += 1

            print(f"{lv_key} {diff}: {len(questions)} -> kept {len(questions)-removed}, removed {removed} başkent, added {added} GK")

            # Rebuild pool content
            new_pool = ",\n".join(kept)
            block = block[:d_content_start] + "\n" + new_pool + "\n" + block[d_end:]

        # Write back
        txt = txt[:content_start] + block + txt[end:]

    FILE.write_text(txt, encoding="utf-8")
    print("\nDosya güncellendi!")

    # Verify
    txt2 = FILE.read_text(encoding="utf-8")
    total_q = len(re.findall(r'\{q:', txt2))
    total_bk = len(re.findall(r'başkent', txt2, re.IGNORECASE))
    print(f"Toplam soru: {total_q}")
    print(f"Toplam başkent sorusu: {total_bk}")

    # Per level check
    for lv_name, lv_var in level_vars:
        start = txt2.find(lv_var + ' = r"""')
        next_markers = [txt2.find('\n_QUESTIONS_', start+50), txt2.find('\ndef _build_', start+50)]
        next_markers = [x for x in next_markers if x > 0]
        end = min(next_markers) if next_markers else len(txt2)
        chunk = txt2[start:end]
        qs = len(re.findall(r'\{q:', chunk))
        bks = len(re.findall(r'başkent', chunk, re.IGNORECASE))
        print(f"  {lv_name}: {qs} soru, {bks} başkent")


if __name__ == "__main__":
    process()
