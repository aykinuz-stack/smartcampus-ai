#!/usr/bin/env python3
"""Generate first 250 lise questions"""
import os

questions = [
# === TARİH (50) ===
'{k:"Tarih",s:"Vestfalya Barışı hangi yılda imzalandı?",o:["1618","1648","1713","1789"],d:1,a:"Vestfalya Barışı 1648 de imzalanmış ve modern devletler sistemini kurmuştur."}',
'{k:"Tarih",s:"Rönesans hangi ülkede başlamıştır?",o:["Fransa","İngiltere","İtalya","Almanya"],d:2,a:"Rönesans 14. yüzyılda İtalya da başlamıştır."}',
'{k:"Tarih",s:"Magna Carta hangi yılda imzalanmıştır?",o:["1066","1215","1453","1789"],d:1,a:"Magna Carta 1215 yılında İngiltere de imzalanmıştır."}',
'{k:"Tarih",s:"Amerikan Bağımsızlık Bildirgesi hangi yıl ilan edildi?",o:["1763","1776","1789","1812"],d:1,a:"Amerikan Bağımsızlık Bildirgesi 4 Temmuz 1776 da ilan edilmiştir."}',
'{k:"Tarih",s:"Bolşevik Devrimi hangi yılda gerçekleşti?",o:["1905","1914","1917","1922"],d:2,a:"Bolşevik Devrimi Ekim 1917 de Rusya da gerçekleşmiştir."}',
'{k:"Tarih",s:"Birleşmiş Milletler hangi yılda kuruldu?",o:["1919","1939","1945","1950"],d:2,a:"Birleşmiş Milletler 1945 yılında kurulmuştur."}',
'{k:"Tarih",s:"NATO hangi yılda kuruldu?",o:["1945","1947","1949","1955"],d:2,a:"NATO (Kuzey Atlantik Antlaşması Örgütü) 1949 yılında kurulmuştur."}',
'{k:"Tarih",s:"Berlin Duvarı hangi yılda yıkıldı?",o:["1985","1987","1989","1991"],d:2,a:"Berlin Duvarı 9 Kasım 1989 da yıkılmıştır."}',
'{k:"Tarih",s:"Osmanlı Devletinde ilk anayasa hangi dönemde hazırlandı?",o:["Tanzimat","I. Meşrutiyet","II. Meşrutiyet","Cumhuriyet"],d:1,a:"İlk anayasa Kanun-i Esasi 1876 I. Meşrutiyet döneminde hazırlanmıştır."}',
'{k:"Tarih",s:"Türkiye hangi yılda NATO ya katıldı?",o:["1949","1950","1952","1955"],d:2,a:"Türkiye 1952 yılında NATO ya katılmıştır."}',
'{k:"Tarih",s:"Lale Devri hangi yüzyılda yaşanmıştır?",o:["16. yy","17. yy","18. yy","19. yy"],d:2,a:"Lale Devri 18. yüzyılda 1718-1730 yılları arasında yaşanmıştır."}',
'{k:"Tarih",s:"Yavuz Sultan Selim hangi savaşla Mısırı fethetti?",o:["Çaldıran","Ridaniye","Preveze","Mohaç"],d:1,a:"Yavuz Sultan Selim 1517 Ridaniye Savaşı ile Mısırı fethetti."}',
'{k:"Tarih",s:"İttihat ve Terakki Cemiyeti hangi olayla iktidara geldi?",o:["31 Mart","II. Meşrutiyet","Balkan Savaşları","I. Dünya Savaşı"],d:1,a:"İttihat ve Terakki 1908 II. Meşrutiyet ilanıyla iktidara gelmiştir."}',
'{k:"Tarih",s:"Waterloo Savaşı kim yenilmiştir?",o:["İngiltere","Prusya","Napolyon","Rusya"],d:2,a:"Napolyon 1815 Waterloo Savaşında yenilerek sürgüne gönderilmiştir."}',
'{k:"Tarih",s:"Endüstri Devriminde buhar makinesini kim geliştirdi?",o:["Edison","Newton","James Watt","Tesla"],d:2,a:"James Watt buhar makinesini geliştirerek Endüstri Devrimine katkı sağlamıştır."}',
'{k:"Tarih",s:"Düyun-u Umumiye ne demektir?",o:["Meclis","Borç idaresi","Ordu","Mahkeme"],d:1,a:"Düyun-u Umumiye Osmanlı dış borçlarını yönetmek için kurulan idaredir."}',
'{k:"Tarih",s:"Mudros Ateşkesinden sonra hangi antlaşma dayatıldı?",o:["Lozan","Sevr","Ankara","Kars"],d:1,a:"Sevr Antlaşması Osmanlıya dayatılmış ancak TBMM kabul etmemiştir."}',
'{k:"Tarih",s:"Tekalif-i Milliye emirleri ne amaçla çıkarıldı?",o:["Eğitim","Savaş ihtiyaçlarını karşılamak","Ticaret","Tarım"],d:1,a:"Tekalif-i Milliye emirleri Kurtuluş Savaşı için kaynak toplamak amacıyla çıkarılmıştır."}',
'{k:"Tarih",s:"Avrupa Birliği hangi antlaşmayla kuruldu?",o:["Roma","Paris","Maastricht","Lizbon"],d:2,a:"Avrupa Birliği 1992 Maastricht Antlaşması ile kurulmuştur."}',
'{k:"Tarih",s:"Osmanlıda devşirme sistemi nedir?",o:["Vergi sistemi","Hristiyan çocukların askere alınması","Ticaret sistemi","Eğitim sistemi"],d:1,a:"Devşirme sistemi Hristiyan ailelerden çocuk alınarak Osmanlı ordusuna kazandırılmasıdır."}',
'{k:"Tarih",s:"Marshall Planı hangi ülke tarafından uygulandı?",o:["SSCB","İngiltere","ABD","Fransa"],d:2,a:"Marshall Planı II. Dünya Savaşı sonrası Avrupa yı yeniden inşa etmek için ABD tarafından uygulandı."}',
'{k:"Tarih",s:"Piri Reis Haritası hangi yüzyılda çizildi?",o:["14. yy","15. yy","16. yy","17. yy"],d:2,a:"Piri Reis Haritası 1513 yılında 16. yüzyılda çizilmiştir."}',
'{k:"Tarih",s:"Kurtuluş Savaşının ilk askeri zafer hangisidir?",o:["Sakarya","İnönü","Dumlupınar","Başkomutanlık"],d:1,a:"I. İnönü Muharebesi (1921) Kurtuluş Savaşının ilk askeri zaferidir."}',
'{k:"Tarih",s:"Atatürk ilkelerinden hangisi ekonomi politikasını belirler?",o:["Halkçılık","Devletçilik","Laiklik","Milliyetçilik"],d:1,a:"Devletçilik ilkesi ekonomi politikasını belirler."}',
'{k:"Tarih",s:"Tanzimat Fermanının en önemli yeniliği nedir?",o:["Matbaa","Can ve mal güvenliği","Meclis","Cumhuriyet"],d:1,a:"Tanzimat Fermanı ile tüm vatandaşlara can ve mal güvencesi sağlanmıştır."}',
'{k:"Tarih",s:"Türk Tarih Kurumu hangi yılda kuruldu?",o:["1928","1931","1934","1938"],d:1,a:"Türk Tarih Kurumu 1931 yılında kurulmuştur."}',
'{k:"Tarih",s:"Türk Dil Kurumu hangi yılda kuruldu?",o:["1928","1930","1932","1935"],d:2,a:"Türk Dil Kurumu 1932 yılında kurulmuştur."}',
'{k:"Tarih",s:"Kabotaj Kanunu hangi yılda kabul edildi?",o:["1924","1926","1928","1930"],d:1,a:"Kabotaj Kanunu 1 Temmuz 1926 da kabul edilerek deniz ticareti Türklere verilmiştir."}',
'{k:"Tarih",s:"Soğuk Savaşta Varşova Paktı hangi yılda kuruldu?",o:["1949","1951","1955","1961"],d:2,a:"Varşova Paktı 1955 yılında SSCB liderliğinde kurulmuştur."}',
'{k:"Tarih",s:"Kıbrıs Barış Harekatı hangi yılda yapıldı?",o:["1960","1964","1974","1983"],d:2,a:"Kıbrıs Barış Harekatı 20 Temmuz 1974 te gerçekleştirilmiştir."}',
'{k:"Tarih",s:"Osmanlıda Islahat Fermanı hangi yılda ilan edildi?",o:["1839","1856","1876","1908"],d:1,a:"Islahat Fermanı 1856 yılında ilan edilmiştir."}',
'{k:"Tarih",s:"Hz. Muhammed hangi yılda Hicret etmiştir?",o:["610","622","630","632"],d:1,a:"Hicret 622 yılında Mekke den Medine ye göçtür."}',
'{k:"Tarih",s:"Haçlı Seferleri kaç yüzyıl sürmüştür?",o:["1","2","3","4"],d:1,a:"Haçlı Seferleri 11.-13. yüzyıllar arasında yaklaşık 2 yüzyıl sürmüştür."}',
'{k:"Tarih",s:"Matbaayı Osmanlıya kim getirmiştir?",o:["Mimar Sinan","İbrahim Müteferrika","Evliya Çelebi","Katip Çelebi"],d:1,a:"İbrahim Müteferrika 1727 de Osmanlıda ilk matbaayı kurmuştur."}',
'{k:"Tarih",s:"30 Yıl Savaşları hangi kıtada yaşanmıştır?",o:["Asya","Afrika","Avrupa","Amerika"],d:2,a:"30 Yıl Savaşları 1618-1648 arasında Avrupa da yaşanmıştır."}',
'{k:"Tarih",s:"Sanayi Devrimi ile ortaya çıkan sınıf hangisidir?",o:["Aristokrasi","Burjuvazi ve işçi sınıfı","Ruhban sınıfı","Köylü sınıfı"],d:1,a:"Sanayi Devrimi ile burjuvazi güçlenmiş ve işçi sınıfı ortaya çıkmıştır."}',
'{k:"Tarih",s:"Truman Doktrini hangi yılda ilan edildi?",o:["1945","1947","1949","1950"],d:1,a:"Truman Doktrini 1947 de komünizme karşı ABD nin yardım politikasıdır."}',
'{k:"Tarih",s:"İnsan Hakları Evrensel Beyannamesi hangi yılda kabul edildi?",o:["1945","1948","1950","1960"],d:1,a:"İnsan Hakları Evrensel Beyannamesi 10 Aralık 1948 de BM tarafından kabul edilmiştir."}',
'{k:"Tarih",s:"Türkiye de çok partili hayata ne zaman geçildi?",o:["1923","1930","1946","1950"],d:2,a:"Türkiye de çok partili hayata fiilen 1946 yılında geçilmiştir."}',
'{k:"Tarih",s:"Demokrat Parti hangi yılda iktidara geldi?",o:["1946","1948","1950","1952"],d:2,a:"Demokrat Parti 14 Mayıs 1950 seçimleriyle iktidara gelmiştir."}',
'{k:"Tarih",s:"Çaldıran Savaşı hangi yılda yapıldı?",o:["1453","1514","1526","1538"],d:1,a:"Çaldıran Savaşı 1514 yılında Osmanlı ile Safeviler arasında yapılmıştır."}',
'{k:"Tarih",s:"Avrupa Konseyi hangi yılda kuruldu?",o:["1945","1947","1949","1951"],d:2,a:"Avrupa Konseyi 1949 yılında kurulmuş, Türkiye kurucu üyedir."}',
'{k:"Tarih",s:"Balkan Savaşları hangi yıllar arasında yapıldı?",o:["1908-1910","1912-1913","1914-1918","1919-1922"],d:1,a:"Balkan Savaşları 1912-1913 yılları arasında yapılmıştır."}',
'{k:"Tarih",s:"Osmanlı padişahlarından hangisi en uzun süre tahtta kalmıştır?",o:["Fatih","Yavuz","Kanuni","II. Abdülhamid"],d:2,a:"Kanuni Sultan Süleyman 46 yıl ile en uzun süre tahtta kalan padişahtır."}',
# === COĞRAFYA (50) ===
'{k:"Coğrafya",s:"Tektonik plaka hareketleri ne oluşturur?",o:["Rüzgar","Deprem ve volkan","Yağmur","Gel-git"],d:1,a:"Tektonik plaka hareketleri deprem volkanik aktivite ve dağ oluşumuna neden olur."}',
'{k:"Coğrafya",s:"Coriolis etkisi nedir?",o:["Depremlerin sebebi","Dünya dönüşünün rüzgar ve akıntıları saptırması","Volkanik etki","Gel-git olayı"],d:1,a:"Coriolis etkisi Dünya nın dönüşünden kaynaklanan rüzgar ve akıntıların sapmasıdır."}',
'{k:"Coğrafya",s:"Fay hattı nedir?",o:["Dağ zirvesi","Yer kabuğundaki kırık hattı","Nehir yatağı","Okyanus dibi"],d:1,a:"Fay hattı yer kabuğundaki tektonik plakaların birleştiği kırık hattıdır."}',
'{k:"Coğrafya",s:"El Nino etkisi nedir?",o:["Deprem","Pasifik de deniz suyu sıcaklık artışı","Volkanik patlama","Tsunami"],d:1,a:"El Nino Pasifik Okyanusundaki anormal deniz suyu ısınmasıdır."}',
'{k:"Coğrafya",s:"Orojenez ne demektir?",o:["Deprem oluşumu","Dağ oluşumu","Kıta kayması","Volkanik patlama"],d:1,a:"Orojenez tektonik kuvvetlerle dağ oluşumu sürecidir."}',
'{k:"Coğrafya",s:"Karst topoğrafyası hangi kayaçta gelişir?",o:["Granit","Bazalt","Kireçtaşı","Kumtaşı"],d:2,a:"Karst topoğrafyası kireçtaşının çözünmesiyle gelişir."}',
'{k:"Coğrafya",s:"Rift vadisi nasıl oluşur?",o:["Aşınmayla","Tektonik plakaların birbirinden uzaklaşmasıyla","Volkanla","Buzul erozyonuyla"],d:1,a:"Rift vadisi tektonik plakaların birbirinden uzaklaşmasıyla oluşur."}',
'{k:"Coğrafya",s:"Dünya nın en derin noktası neresidir?",o:["Grand Kanyon","Mariana Çukuru","Baykal Gölü","Kola Kuyusu"],d:1,a:"Mariana Çukuru yaklaşık 11000 m ile dünyanın en derin noktasıdır."}',
'{k:"Coğrafya",s:"Jet akımı nedir?",o:["Uçak rotası","Atmosferin üst katmanlarındaki hızlı hava akımı","Okyanus akıntısı","Volkanik gaz"],d:1,a:"Jet akımı troposferin üst kısmında esen çok hızlı hava akımıdır."}',
'{k:"Coğrafya",s:"Monoson ikliminin en belirgin özelliği nedir?",o:["Sürekli kurak","Mevsimsel rüzgar değişimi ve yoğun yağış","Soğuk kış","Ilıman yaz"],d:1,a:"Muson ikliminde mevsimsel rüzgar değişimi ve yoğun yağış dönemleri karakteristiktir."}',
'{k:"Coğrafya",s:"GAP hangi nehirler üzerinde kurulmuştur?",o:["Kızılırmak-Sakarya","Fırat-Dicle","Seyhan-Ceyhan","Meriç-Ergene"],d:1,a:"GAP (Güneydoğu Anadolu Projesi) Fırat ve Dicle nehirleri üzerine kurulmuştur."}',
'{k:"Coğrafya",s:"Moren ne demektir?",o:["Volkanik kayaç","Buzulun taşıdığı malzeme birikintisi","Kum tepesi","Akarsu yatağı"],d:1,a:"Moren buzulların taşıyıp biriktirdiği kaya ve toprak yığınıdır."}',
'{k:"Coğrafya",s:"İzostazi kavramı neyi açıklar?",o:["Hava basıncı","Yer kabuğunun denge durumu","Okyanus akıntıları","Rüzgar oluşumu"],d:1,a:"İzostazi yer kabuğunun manto üzerinde denge durumunda bulunmasıdır."}',
'{k:"Coğrafya",s:"Meridyen boylam farkı neyi etkiler?",o:["Mevsimler","Saat farkı","Yağış","Sıcaklık"],d:1,a:"Meridyenler arası 15 derecelik fark 1 saatlik saat farkına karşılık gelir."}',
'{k:"Coğrafya",s:"Türkiye de en çok deprem yaşanan fay hangisidir?",o:["Doğu Anadolu","Kuzey Anadolu","Batı Anadolu","Güneydoğu"],d:1,a:"Kuzey Anadolu Fay Hattı Türkiye nin en aktif ve tehlikeli fay hattıdır."}',
'{k:"Coğrafya",s:"Taiga biyomu nerelerde bulunur?",o:["Tropiklerde","Kuzeyde iğne yapraklı orman kuşağı","Çöllerde","Kutuplarda"],d:1,a:"Taiga kuzeyin soğuk bölgelerinde bulunan iğne yapraklı orman biyomudur."}',
'{k:"Coğrafya",s:"Çöl ortamında hangi fiziksel ayrışma daha yaygındır?",o:["Kimyasal","Biyolojik","Termal (sıcaklık farkı)","Buzul"],d:2,a:"Çöllerde gece-gündüz sıcaklık farkı nedeniyle termal ayrışma yaygındır."}',
'{k:"Coğrafya",s:"Heyelan en çok hangi koşullarda oluşur?",o:["Kurak arazide","Eğimli arazide yoğun yağış sonrası","Düz ovada","Çöl ortamında"],d:1,a:"Heyelan genellikle eğimli arazilerde yoğun yağış sonrası toprak kaymasıyla oluşur."}',
'{k:"Coğrafya",s:"Stratosferde bulunan koruyucu tabaka hangisidir?",o:["Troposfer","Ozon tabakası","Mezosfer","Termosfer"],d:1,a:"Ozon tabakası stratosferde bulunur ve zararlı UV ışınlarını süzer."}',
'{k:"Coğrafya",s:"Batı Karadeniz in en önemli ekonomik faaliyeti nedir?",o:["Tarım","Madencilik","Turizm","Hayvancılık"],d:1,a:"Batı Karadeniz de Zonguldak bölgesinde taşkömürü madenciliği önemli ekonomik faaliyettir."}',
'{k:"Coğrafya",s:"Tünel vadisi nasıl oluşur?",o:["Volkanla","Akarsu erozyonuyla","Rüzgarla","Buzulla"],d:1,a:"Tünel vadisi genellikle akarsuyun kayalık arazi içinden geçmesiyle oluşur."}',
'{k:"Coğrafya",s:"Epirojenez ne demektir?",o:["Dağ oluşumu","Kıta oluşumu (yükselme-alçalma)","Deprem","Volkan"],d:1,a:"Epirojenez geniş alanları etkileyen yavaş yükselme ve alçalma hareketleridir."}',
'{k:"Coğrafya",s:"Litosfer nedir?",o:["Atmosferin alt katmanı","Yer kabuğu ve üst manto","Okyanus tabanı","Volkanik bölge"],d:1,a:"Litosfer yer kabuğu ve üst mantonun katı kısmından oluşan katmandır."}',
'{k:"Coğrafya",s:"Enlem sıcaklığı nasıl etkiler?",o:["Etkilemez","Enlem arttıkça sıcaklık azalır","Enlem arttıkça sıcaklık artar","Sadece yağışı etkiler"],d:1,a:"Ekvatorda en yüksek sıcaklık vardır kutuplara gidildikçe sıcaklık azalır."}',
'{k:"Coğrafya",s:"Konveksiyonel yağış nasıl oluşur?",o:["Dağa çarparak","Cephe ile","Yüzeyin ısınmasıyla havanın yükselmesi","Rüzgarla"],d:2,a:"Konveksiyonel yağış yüzeyin aşırı ısınmasıyla havanın yükselmesi sonucu oluşur."}',
'{k:"Coğrafya",s:"Astenosfer nedir?",o:["Atmosfer katmanı","Mantonun akışkan üst kısmı","Yer çekirdeği","Okyanus tabanı"],d:1,a:"Astenosfer mantonun yarı akışkan kısmıdır litosfer plakaları üzerinde hareket eder."}',
# === BİLİM (25) - ilk yarı ===
'{k:"Bilim",s:"Avogadro sayısı yaklaşık kaçtır?",o:["3.14 x 10^8","6.02 x 10^23","9.81","1.6 x 10^-19"],d:1,a:"Avogadro sayısı yaklaşık 6.02 x 10^23 tür ve 1 moldeki tanecik sayısını ifade eder."}',
'{k:"Bilim",s:"Heisenberg belirsizlik ilkesi neyi ifade eder?",o:["Enerji korunumu","Konum ve momentum aynı anda kesin ölçülemez","Işık hızı sabittir","Kütle enerji eşdeğerliği"],d:1,a:"Heisenberg ilkesi bir parçacığın konumu ve momentumunun aynı anda kesin ölçülemeyeceğini belirtir."}',
'{k:"Bilim",s:"RNA nın DNA dan farkı nedir?",o:["Çift sarmal","Tek sarmallı ve riboz şekeri içerir","Daha büyük","Proteindir"],d:1,a:"RNA tek sarmallı yapıdadır ve deoksiriboz yerine riboz şekeri içerir."}',
'{k:"Bilim",s:"Entropi ne demektir?",o:["Enerji birimi","Düzensizlik ölçüsü","Basınç birimi","Kuvvet türü"],d:1,a:"Entropi termodinamikte düzensizliğin ölçüsüdür."}',
'{k:"Bilim",s:"Kara delik nedir?",o:["Uzay boşluğu","Çekim kuvveti ışığın bile kaçamadığı bölge","Yıldız patlaması","Gezegen"],d:1,a:"Kara delik çekim kuvveti o kadar güçlü olan bölgedir ki ışık bile kaçamaz."}',
'{k:"Bilim",s:"Ohm kanunu nedir?",o:["F=ma","V=IR","E=mc2","PV=nRT"],d:1,a:"Ohm kanunu gerilim = akım x direnç yani V=IR formülüyle ifade edilir."}',
'{k:"Bilim",s:"Kromozom sayısı insanda kaçtır?",o:["23","44","46","48"],d:2,a:"İnsanda 46 kromozom (23 çift) bulunur."}',
'{k:"Bilim",s:"Periyodik tabloda soy gazlar hangi gruptadır?",o:["1. grup","7. grup","8A grubu","Geçiş metalleri"],d:2,a:"Soy gazlar periyodik tablonun 8A (18.) grubundadır."}',
'{k:"Bilim",s:"Fotoelektrik olay nedir?",o:["Fotoğrafçılık","Işığın metalden elektron koparması","Elektrik üretimi","Lens oluşumu"],d:1,a:"Fotoelektrik olay ışığın metal yüzeye çarparak elektron koparmasıdır."}',
'{k:"Bilim",s:"Mitoz bölünme sonucunda kaç hücre oluşur?",o:["1","2","4","8"],d:1,a:"Mitoz bölünme sonucunda genetik olarak özdeş 2 hücre oluşur."}',
'{k:"Bilim",s:"Mayoz bölünme sonucunda kaç hücre oluşur?",o:["1","2","4","8"],d:2,a:"Mayoz bölünme sonucunda 4 haploid hücre oluşur."}',
'{k:"Bilim",s:"Standart basınç kaç atmosferdir?",o:["0.5","1","2","10"],d:1,a:"Standart basınç 1 atmosfer yani 101325 Pascal dir."}',
'{k:"Bilim",s:"Doppler etkisi neyi açıklar?",o:["Işık hızı","Ses kaynağı hareket edince frekans değişimi","Çekim kuvveti","Manyetik alan"],d:1,a:"Doppler etkisi ses veya ışık kaynağı hareket ederken gözlemciye göre frekans değişimini açıklar."}',
'{k:"Bilim",s:"Elektromanyetik spektrumda en kısa dalga boylu ışın hangisidir?",o:["Radyo dalgası","Kızılötesi","Mor ötesi","Gama ışını"],d:3,a:"Gama ışınları elektromanyetik spektrumda en kısa dalga boyuna sahiptir."}',
'{k:"Bilim",s:"Mendel in birinci yasası nedir?",o:["Bağımsız dağılım","Ayrışma (segregasyon)","Dominant gen","Mutasyon"],d:1,a:"Mendel in birinci yasası alellerin gamet oluşumunda birbirinden ayrılmasıdır."}',
'{k:"Bilim",s:"Joule neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:2,a:"Joule SI birim sisteminde enerjinin birimidir."}',
'{k:"Bilim",s:"Watt neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:1,a:"Watt güç (birim zamanda yapılan iş) birimidir."}',
'{k:"Bilim",s:"Pascal neyin birimidir?",o:["Kuvvet","Güç","Enerji","Basınç"],d:3,a:"Pascal basınç birimidir."}',
'{k:"Bilim",s:"Katalizör ne yapar?",o:["Tepkimeyi durdurur","Tepkime hızını değiştirir kendisi değişmez","Tepkimeye katılır","Ürün oluşturur"],d:1,a:"Katalizör kimyasal tepkime hızını değiştirir ancak kendisi tepkimede tüketilmez."}',
'{k:"Bilim",s:"Hubble Yasası neyi ifade eder?",o:["Gezegenler","Evrenin genişlediğini","Atom yapısı","Genetik"],d:1,a:"Hubble Yasası galaksilerin bizden uzaklaştığını yani evrenin genişlediğini gösterir."}',
'{k:"Bilim",s:"Nötron yıldızı nasıl oluşur?",o:["Güneşten","Büyük yıldızın çökmesiyle","Gezegenlerden","Kara delikten"],d:1,a:"Nötron yıldızı süpernova patlamasından sonra büyük bir yıldızın çekirdeğinin çökmesiyle oluşur."}',
'{k:"Bilim",s:"Enzimler ne tür moleküllerdir?",o:["Karbonhidrat","Lipid","Protein","Nükleik asit"],d:2,a:"Enzimler biyolojik katalizör görevi gören protein molekülleridir."}',
'{k:"Bilim",s:"Endotermik tepkime ne demektir?",o:["Isı veren","Isı alan","Nötr","Gaz çıkaran"],d:1,a:"Endotermik tepkime çevreden ısı alan tepkimedir."}',
'{k:"Bilim",s:"Ekzotermik tepkime ne demektir?",o:["Isı alan","Isı veren","Nötr","Gaz alan"],d:1,a:"Ekzotermik tepkime çevreye ısı veren tepkimedir."}',
'{k:"Bilim",s:"Kuantum fiziğinin kurucusu kimdir?",o:["Newton","Einstein","Planck","Bohr"],d:2,a:"Max Planck kuantum fiziğinin kurucusu olarak kabul edilir."}',
'{k:"Bilim",s:"CRISPR teknolojisi ne amaçla kullanılır?",o:["Teleskop","Gen düzenleme","Nükleer enerji","İlaç üretimi"],d:1,a:"CRISPR DNA düzenleme teknolojisidir gen terapisi ve araştırmada kullanılır."}',
]

filepath = os.path.join("c:", os.sep, "Users", "safir", "OneDrive", "Masaüstü", "SmartCampusAI", "views", "_by_lise.txt")

with open(filepath, "w", encoding="utf-8") as f:
    for q in questions:
        f.write(q + "\n")

with open(filepath, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip().startswith("{k:")]
    print(f"Total: {len(lines)}")
    cats = {}
    for l in lines:
        cat = l.split('"')[1]
        cats[cat] = cats.get(cat, 0) + 1
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")
