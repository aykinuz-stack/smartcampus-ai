# -*- coding: utf-8 -*-
"""
SmartCampusAI - Kitap Ozetleri Veritabani
200 kitap ozeti: kategori, ozet, karakterler, temalar, alintilar
"""

KITAP_OZETLERI = {

    # ========================== RUS EDEBIYATI (20) ==========================

    "Suc ve Ceza - Dostoyevski": {
        "kategori": "Rus Edebiyati",
        "ozet": "Yoksul bir universite ogrencisi olan Raskolnikov, kendini siradan insanlarin ustunde goren bir teoriyle tefeci bir kadini oldurur. Cinayetin ardindan vicdan azabi ve paranoya icinde kivranirken, Sonya adli genc bir kadinin sevgisi onu teslim olmaya ikna eder. Roman, insanin ahlaki sinirlarini ve gucun mesuliyet gerektirdigini sorgular.",
        "karakterler": [
            ("Raskolnikov", "Cinayeti isleyen zeki ama bunalimli universite ogrencisi"),
            ("Sonya Marmeladova", "Ailesi icin kendini feda eden, derin imana sahip genc kadin"),
            ("Porfirii Petroviç", "Raskolnikov'u psikolojik olarak kosistiren zeki dedektif")
        ],
        "temalar": ["Vicdan azabi ve kefaret", "Ustun insan teorisi", "Iman ve kurtulis"],
        "alintilar": [
            "Acı çekmek de, keder duymak da geniş görüşlü ve derin yürekli insanların kaderidir.",
            "İnsan her şeye alışır, alçak herif!"
        ]
    },
    "Karamazov Kardesler - Dostoyevski": {
        "kategori": "Rus Edebiyati",
        "ozet": "Karamazov ailesinin uc oglu -akilli Ivan, tutkulu Dmitri ve masum Alyosa- babalarinin oldurulmesiyle birlikte derin bir ahlaki krize suruklenirler. Roman, iman ile suphecilik, ozgurluk ile sorumluluk arasindaki catismayi bir aile draminin icinden isler. Dostoyevski'nin son ve en kapsamli eseridir.",
        "karakterler": [
            ("Dmitri Karamazov", "Tutkulu, nobran ama iyi kalpli buyuk kardes"),
            ("Ivan Karamazov", "Tanri'nin varligini sorgulayan entelektuel orta kardes"),
            ("Alyosa Karamazov", "Manastirda yetismis, saf ve iyi niyetli kucuk kardes")
        ],
        "temalar": ["Iman ve suphecilik", "Baba-ogul catismasi", "Ozgur irade ve ahlak"],
        "alintilar": [
            "Güzellik korkunç bir şeydir. Tanrı ile şeytan orada savaşır ve savaş alanı insanın kalbidir.",
            "Her şey mübahtır, eğer Tanrı yoksa."
        ]
    },
    "Budala - Dostoyevski": {
        "kategori": "Rus Edebiyati",
        "ozet": "Prens Miskin, saf ve iyi kalpli bir adam olarak Petersburg sosyetesine doner. Nastasya Filippovna'ya duyulan ask ve Rogojin'in saplantili tutkusu etrafinda gelisen olaylar, iyiligin dunya tarafindan nasil ezildigini gosterir. Roman, gercek bir Hristiyan'in modern toplumda yasayip yasamayacagini sorgular.",
        "karakterler": [
            ("Prens Miskin", "Epilepsi hastasi, son derece iyi kalpli ve saf bir adam"),
            ("Nastasya Filippovna", "Guzel, gururlu ve kendi yikimina suruklenen trajik kadin"),
            ("Rogojin", "Nastasya'ya saplantili bir tutku besleyen zengin tuccar oglu")
        ],
        "temalar": ["Masumiyetin yikilisi", "Iyi ile kotunun mucadelesi", "Toplumsal ikilik"],
        "alintilar": [
            "Güzellik dünyayı kurtaracak.",
            "Alçakgönüllülük müthiş bir güçtür."
        ]
    },
    "Savas ve Baris - Tolstoy": {
        "kategori": "Rus Edebiyati",
        "ozet": "Napoleon'un Rusya seferini arka plan alan bu dev roman, Bolkonski, Rostov ve Bezuhov ailelerinin hayatlari uzerinden savas, ask ve toplumsal donusumleri anlatir. Tolstoy, tarihin buyuk adamlar tarafindan degil, sayisiz kucuk olaylar tarafindan sekillendigini savunur. Rus edebiyatinin en onemli eserlerinden biridir.",
        "karakterler": [
            ("Prens Andrei Bolkonski", "Idealist, savasda anlam arayan soylu bir subay"),
            ("Pierre Bezuhov", "Hayatin anlamini arayan zengin ama bocalayen bir adam"),
            ("Natasa Rostova", "Hayat dolu, tutkulu ve olgunlasan genc bir kadin")
        ],
        "temalar": ["Savas ve insan kaderi", "Tarihin akisi", "Bireysel anlam arayisi"],
        "alintilar": [
            "Hayattaki en büyük mutluluk, sevildiğinize ve sevilmeye layık olduğunuza inanmaktır.",
            "Herkes dünyayı değiştirmeyi düşünür, ama kimse kendini değiştirmeyi düşünmez."
        ]
    },
    "Anna Karenina - Tolstoy": {
        "kategori": "Rus Edebiyati",
        "ozet": "Aristokrat Anna Karenina, soguk kocasi Karenin'i birakarak yakisikli subay Vronski ile yasak bir aska atilir. Toplumun dislamasi ve ic huzursuzlugu onu trajik bir sona goturur. Paralel olarak anlatilan Levin'in hikayesi ise toprakta ve iste anlam bulan bir yasamin alternatifini sunar.",
        "karakterler": [
            ("Anna Karenina", "Tutkulu ve guzel ama toplum baskisi altinda ezilen kadin"),
            ("Vronski", "Anna'ya asik olan yakisikli ve zengin subay"),
            ("Levin", "Kirsal hayatta anlam arayan, Tolstoy'un alter ego'su")
        ],
        "temalar": ["Yasak ask ve toplumsal yargi", "Aile ve mutluluk", "Anlam arayisi"],
        "alintilar": [
            "Mutlu ailelerin hepsi birbirine benzer; her mutsuz aile ise kendince mutsuz olur.",
            "Beni affetmiyorlarsa, benim için daha kötü."
        ]
    },
    "Olu Canlar - Gogol": {
        "kategori": "Rus Edebiyati",
        "ozet": "Cicikov adli bir dolandirici, olu serflerin tapularini satin alarak hayali bir servet olusturmaya calisir. Gogol, Cicikov'un ziyaret ettigi toprak sahiplerinin her birini farkli bir insani zaafi temsil edecek sekilde cizerken, Rus toplumunun curumusluklugunu hicveder. Eser, Rus edebiyatinin ilk buyuk hiciv romanidir.",
        "karakterler": [
            ("Cicikov", "Kibar gorunumlu, kurnaz ve hirsli dolandirici"),
            ("Manilov", "Hayalperest, bos bos vakit geciren soylu toprak sahibi"),
            ("Nozdryov", "Yalanci, kumarbaz ve kavgaci bir toprak sahibi")
        ],
        "temalar": ["Toplumsal yozlasma", "Acgozluluk ve hirs", "Rus toplumunun hicvi"],
        "alintilar": [
            "Rusya'ya bakıyorum ve onu anlayamıyorum.",
            "Dünyada hiçbir şey, uzun süre kalıcı değildir."
        ]
    },
    "Babalar ve Ogullar - Turgenyev": {
        "kategori": "Rus Edebiyati",
        "ozet": "Genc nihilist Bazarov, arkadasi Arkadi ile birlikte tayin edildigi kasabaya doner ve eski kusakla catisir. Bazarov tum otoriteyi ve geleneği reddederken, askin gucu karsisinda bocalar. Roman, 1860'lar Rusya'sindaki kusak catismasini ve nihilizm akimini edebi bir sekildeisler.",
        "karakterler": [
            ("Bazarov", "Her seyi reddeden, bilime inanan genc nihilist"),
            ("Arkadi Kirsanov", "Bazarov'un etkisindeki ama daha ilimli genc"),
            ("Pavel Petroviç", "Eski duzeni savunan, aristokrat amca")
        ],
        "temalar": ["Kusak catismasi", "Nihilizm ve idealizm", "Ask ve zaaf"],
        "alintilar": [
            "Bir nihilist, hiçbir otoriteye boyun eğmeyen insandır.",
            "Doğa bir tapınak değil, bir atölyedir."
        ]
    },
    "Yevgeni Onegin - Puskin": {
        "kategori": "Rus Edebiyati",
        "ozet": "Sıkılmış aristokrat Onegin, kendisine aşkını itiraf eden saf köy kızı Tatyana'yı reddeder. Yıllar sonra olgun ve görkemli bir kadın olarak karşısına çıkan Tatyana'ya aşık olur, ancak bu kez o reddedilir. Puşkin'in manzum romanı, Rus edebiyatının kurucu eserlerinden biridir.",
        "karakterler": [
            ("Yevgeni Onegin", "Hayattan bezmiş, alaycı ve soğuk aristokrat genç"),
            ("Tatyana Larina", "Kitap kurdu, duyarlı ve güçlü iradeli köy kızı"),
            ("Lenski", "Romantik, idealist genç şair ve Onegin'in arkadaşı")
        ],
        "temalar": ["Kaçırılmış aşk", "Toplumsal sınıf ve beklentiler", "Olgunlaşma"],
        "alintilar": [
            "Ben sizi seviyorum, bundan ne çıkar ki?",
            "Mutluluk öyle yakınımızdaydı ki..."
        ]
    },
    "Martı - Cehov": {
        "kategori": "Rus Edebiyati",
        "ozet": "Genc yazar Treplev, unlu aktris annesi Arkadina'nin golgesinde kalarak sanatsal basarisizlikla mucadele eder. Nina adli genc kiz, unlu yazar Trigorin ile birlikte olur ve hayal kirikligina ugrar. Oyun, sanatin dogasi, nesiller arasi catisma ve karsilanmayan asklari bir gol kenarinda gerceklestirilen sahne etrafinda isler.",
        "karakterler": [
            ("Treplev", "Yeni sanat arayisindaki genc, mutsuz yazar"),
            ("Nina", "Oyunculuk hayali kuran, saf ve hevesli genc kadin"),
            ("Trigorin", "Basarili ama tatminsiz unlu yazar")
        ],
        "temalar": ["Sanat ve basarisizlik", "Karsilanmayan ask", "Nesil catismasi"],
        "alintilar": [
            "İnsanlar yemek yer, içer, aşık olur; bu arada hayatları yıkılır.",
            "Yeni biçimler lazım bize, yeni biçimler."
        ]
    },
    "Ana - Gorki": {
        "kategori": "Rus Edebiyati",
        "ozet": "Fabrika iscisi Pavel'in annesi Pelagea Nilovna, oglu devrimci mucadeleye katildiktan sonra yavasca siyasi bilinc kazanir. Baslangicta korkak ve cahil olan anne, zamanla isci hareketinin en cesur savunucularindan birine donusur. Roman, Sovyet edebiyatinin kurucu eserlerinden biri olarak kabul edilir.",
        "karakterler": [
            ("Pelagea Nilovna", "Devrimci bilincle donusen isci annesi"),
            ("Pavel Vlasov", "Sosyalist ideallere baglanmis genc isci"),
            ("Andrei", "Pavel'in yakin arkadasi ve yoldasi")
        ],
        "temalar": ["Sinif mucadelesi", "Bireysel donusum", "Analik ve fedakarlik"],
        "alintilar": [
            "İnsan! Bu sözcük ne güzel, ne gururlu!",
            "Korku, köleliğin anasıdır."
        ]
    },
    "Doktor Jivago - Pasternak": {
        "kategori": "Rus Edebiyati",
        "ozet": "Sair ve doktor Yuri Jivago, Rus Devrimi ve ic savas sirasinda hayatta kalmaya calisiken buyuk askini Lara ile yasadigi tutkulu iliskiyle parcalanir. Roman, bireyin tarih karsisindaki gucsuzlugunu ve sanatcinin ozgurluk arayisini lirik bir dille anlatir. Pasternak'a Nobel Edebiyat Odulu kazandirmis ancak Sovyetler Birligi'nde yasaklanmistir.",
        "karakterler": [
            ("Yuri Jivago", "Duyarli, sair ruhlu doktor"),
            ("Lara Antipova", "Guclu, guzel ve dirençli kadin; Jivago'nun buyuk aski"),
            ("Tonya", "Jivago'nun sadik ve sevgi dolu esi")
        ],
        "temalar": ["Devrim ve birey", "Ask ve sadakat", "Sanat ve ozgurluk"],
        "alintilar": [
            "İnsan yaşamak için doğar, hayatı incelemek için değil.",
            "Hayat hiçbir zaman bir madde değildir; sürekli kendini yenileyen bir süreçtir."
        ]
    },
    "Usta ve Margarita - Bulgakov": {
        "kategori": "Rus Edebiyati",
        "ozet": "Seytan Voland, maiyetiyle birlikte Sovyet Moskova'sina gelir ve toplumun ikiyuzlulugunu ifsa eder. Paralel olarak Usta'nin yazdigi Pontius Pilatus romani ve Margarita'nin Usta'yi kurtarmak icin seytanla anlasmasi anlatilir. Bulgakov'un baskiyapi olan eseri, fantastik ogeler ve hicvi ustaca harmanlayan bir basyapittir.",
        "karakterler": [
            ("Usta", "Romani sansure ugrayan ve akil hastanesine kapanan yazar"),
            ("Margarita", "Usta'yi kurtarmak icin cadiya donusen sadik sevgili"),
            ("Voland", "Moskova'ya gelen gizemli ve guclu seytan figuru")
        ],
        "temalar": ["Iyilik ve kotuluk", "Sanat ve sansur", "Ask ve fedakarlik"],
        "alintilar": [
            "El yazmalar yanmaz!",
            "Korkaklık, insanın en büyük günahıdır."
        ]
    },
    "Dirilis - Tolstoy": {
        "kategori": "Rus Edebiyati",
        "ozet": "Prens Nehlyudov, juri uyesi olarak katildigi bir davada, gencliginde bastan cikarip terk ettigi Maslova'yi tanir. Vicdan azabiyla yanip tutusarak onun beraat etmesi icin mucadele eder ve sonunda Sibirya'ya kadar pesinden gider. Tolstoy, adalet sistemi ve toplumsal esitsizligi sert bir dille elestirdigi bu romanla kendi ahlak felsefesini ortaya koyar.",
        "karakterler": [
            ("Nehlyudov", "Gecmisteki hatasiyla yuzlesen soylu prens"),
            ("Maslova", "Hayatin dibine dusmus ama onurunu koruyan genc kadin"),
            ("Simonson", "Sibirya'daki siyasi mahkum ve idealist")
        ],
        "temalar": ["Vicdan ve kefaret", "Adalet sistemi elestirisi", "Manevi dirilis"],
        "alintilar": [
            "Herkes dünyayı değiştirmeyi düşünür ama kimse kendini değiştirmeyi düşünmez.",
            "İnsanın en büyük günahı, başkalarının acısına kayıtsız kalmaktır."
        ]
    },
    "Mufattis - Gogol": {
        "kategori": "Rus Edebiyati",
        "ozet": "Kucuk bir kasabaya gelen serseri Hlestakov, yanlis anlasma sonucu baskentin mufettisi sanilir. Kasaba yoneticileri rusvet ve dalkavuklukla onu memnun etmeye calisirken, Gogol burokrasinin curumeslugunu hicveder. Oyun, gercek mufettisin gelisiyle son bulur ve herkes dona kalir.",
        "karakterler": [
            ("Hlestakov", "Mufettis sanilan serseri ve palavraci genc"),
            ("Belediye Baskani", "Yolsuzluklari gizlemeye calisan korkak yetkili"),
            ("Anna Andreyevna", "Baskanin kendini begenmiş esi")
        ],
        "temalar": ["Burokrasi hicvi", "Goruntu ve gerceklik", "Rusvet ve yolsuzluk"],
        "alintilar": [
            "Kendi suratınıza kızmanın ne anlamı var? Kızacaksanız aynaya kızın!",
            "Herkese gülüyorsunuz ama kendinize gülüyorsunuz!"
        ]
    },
    "Visne Bahcesi - Cehov": {
        "kategori": "Rus Edebiyati",
        "ozet": "Aristokrat Ranevskaya ailesi, borclarini odeyemedikleri icin sevdikleri visne bahcesini kaybetme tehlikesiyle karsi karsiyayadir. Eski serf Lopakhin bahceyi satin alir ve eski duzeni temsil eden agaclar kesilir. Oyun, Rusya'daki toplumsal donusumu ve gecmise tutunmanin beyhudeligini melankolik bir dille anlatir.",
        "karakterler": [
            ("Ranevskaya", "Gecmise tutunun duygusal ve savurgan aristokrat kadin"),
            ("Lopakhin", "Eski serf ailesinden gelen basarili is adami"),
            ("Trofimov", "Idealist ve hayalperest universite ogrencisi")
        ],
        "temalar": ["Toplumsal degisim", "Gecmise ozlem", "Sinif donusumu"],
        "alintilar": [
            "Tüm Rusya bizim bahçemizdir.",
            "Yeni bir hayat başlıyor!"
        ]
    },
    "Ucurum - Turgenyev": {
        "kategori": "Rus Edebiyati",
        "ozet": "Sanatci Rayski, tayin edildigi kasabada teyzesinin yaninda yasarken genc ve gizemli Vera'ya asik olur. Vera'nin nihilist Mark Volokhov ile gizli iliskisi, ailenin degerlerini sarsar. Roman, Rusya'da yeni kusaklarin geleneksel degerlerle catismasini, ask ve ahlak ikilemi uzerinden isler.",
        "karakterler": [
            ("Rayski", "Hayalperest ve karasiz sanatci ruhlu genc"),
            ("Vera", "Bagimiz ve guclu iradeli genc kadin"),
            ("Babuska Tatyana", "Geleneksel degerleri temsil eden bilge buyukanne")
        ],
        "temalar": ["Gelenek ve modernlik", "Ask ve ahlak", "Sanatci bocalamasi"],
        "alintilar": [
            "Hayat kısa, sanat uzundur.",
            "İnsan ancak sevdiği zaman gerçekten yaşar."
        ]
    },
    "Savasilmayan Adam - Gorki": {
        "kategori": "Rus Edebiyati",
        "ozet": "Gorki'nin otobiyografik uclemesinin ilk cildi olan Cocukluk, yazarin buyukanne ve buyukbabasiyla gecen zorlu cocukluk yillarini anlatir. Yoksulluk, siddet ve aile ici catismalarin ortasinda buyukannesinin masallari ve sevgisi kucuk Aleksei'nin siginagi olur. Eser, Rus halk hayatinin canli bir tablosunu cizer.",
        "karakterler": [
            ("Aleksei", "Gorki'nin kendisi; merakli ve duyarli bir cocuk"),
            ("Buyukanne Akulina", "Sevgi dolu, masal anlatan, guclu kadin"),
            ("Buyukbaba Kasirin", "Sert, cimri ama zamanla yumusan yasli adam")
        ],
        "temalar": ["Cocukluk ve masumiyetin kaybı", "Yoksulluk", "Aile baglari"],
        "alintilar": [
            "Büyükannem olmasaydı, sevgisiz büyürdüm.",
            "İnsanlar iyi doğar, hayat onları kötü yapar."
        ]
    },
    "Beyaz Geceler - Dostoyevski": {
        "kategori": "Rus Edebiyati",
        "ozet": "Petersburg'da yalniz ve hayalperest bir genc adam, beyaz gecelerden birinde Nastenka adli genc bir kadina rastlar. Dort gece boyunca aralarinda derin bir bag kurulur, ancak Nastenka'nin gercek sevgilisi geri doner. Genc adam kirik kalbiyle yalnizligina doner ama yasadigi ask icin sukranini ifade eder.",
        "karakterler": [
            ("Hayalperest", "Adsiz anlatici; yalniz, duyarli ve romantik genc"),
            ("Nastenka", "Sevgilisini bekleyen, canli ve sicakkanlı genc kadin"),
            ("Sevgili", "Nastenka'nin bir yildir bekledigi adam")
        ],
        "temalar": ["Yalnizlik ve hayal", "Karsilanmayan ask", "Fedakarlik"],
        "alintilar": [
            "Bir dakikalık mutluluk! Koca bir insan ömrü için yeterli değil mi bu?",
            "Tanrım, koca bir mutluluk anı! Bir insan ömrüne az mıdır bu?"
        ]
    },
    "Yeraltindan Notlar - Dostoyevski": {
        "kategori": "Rus Edebiyati",
        "ozet": "Adsiz anlatici, toplumdan kopuk bir sekilde 'yeralti'nda yasayan, kendi bilincinin esiri olmus bir memurdur. Rasyonalizme ve ilerleme inancina isyan ederek insanin irrasyonel dogasini savunur. Roman, varoluşçulugun oncul metinlerinden sayilir ve modern insanin yabancilaşmasini derinlemesine isler.",
        "karakterler": [
            ("Yeralti Adami", "Toplumdan kopuk, kindar ve asiri bilinçli anlatici"),
            ("Liza", "Yeralti adaminın kısa sure iliskiye girdigi genc kadın"),
            ("Zverkov", "Anlaticinin kiskandigi eski okul arkadasi")
        ],
        "temalar": ["Yabancilaşma", "Ozgur irade ve akıl", "Toplumsal isyan"],
        "alintilar": [
            "Ben hasta bir adamım... Kötü bir adamım. Sevimsiz bir adamım.",
            "İki kere iki dört eder, bu artık hayat değil, ölümün başlangıcıdır."
        ]
    },
    "Kazaklar - Tolstoy": {
        "kategori": "Rus Edebiyati",
        "ozet": "Genc Moskovali Olenin, sehir hayatindan kaçarak Kafkasya'daki bir Kazak koyune yerlesir. Dogayla ic ice ozgur yasam onu buyulerken, Kazak kizi Maryana'ya asik olur. Ancak iki farkli dunyanin insanlari arasindaki ucurum asılamaz ve Olenin hayal kirikligiyla geri doner.",
        "karakterler": [
            ("Olenin", "Dogada anlam arayan idealist Moskovali genc"),
            ("Maryana", "Guzel, guclu ve bagimsiz Kazak kizi"),
            ("Yerosska", "Yasli, bilge ve hayat dolu Kazak avcisi")
        ],
        "temalar": ["Dogaya donus", "Medeniyet ve ilkellik", "Yabancılasma"],
        "alintilar": [
            "Mutluluk başkalarını mutlu etmektir.",
            "Her şey güzel burada, doğanın ortasında insan kendini buluyor."
        ]
    },

    # ========================== FRANSIZ EDEBIYATI (20) ==========================

    "Sefiller - Victor Hugo": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Bir somun ekmek caldiği icin 19 yil hapis yatan Jean Valjean, tahliye sonrasi bir piskoposun merhameti sayesinde hayatini degistirir. Fabrika iscisi Fantine'in kizi Cosette'i sahiplenir ve yeni bir hayat kurar. Mufattis Javert ise onu durmaksizin kovalar. Hugo, adalet, merhamet ve toplumsal esitsizligi dev bir fresk icinde isler.",
        "karakterler": [
            ("Jean Valjean", "Hapisten ciktiktan sonra iyi bir insan olmaya calisan eski mahkum"),
            ("Javert", "Yasayi korkusuzca uygulayan, bagnaz polis mufettisi"),
            ("Cosette", "Valjean'in buyuttugu, masum ve guzel genc kiz")
        ],
        "temalar": ["Adalet ve merhamet", "Toplumsal esitsizlik", "Kisisel donusum"],
        "alintilar": [
            "Dünyanın en güçlü orduları bile bir fikrin zamanı geldiğinde onu durduramaz.",
            "Sevmek, hareket etmektir."
        ]
    },
    "Notre-Dame'in Kamburu - Victor Hugo": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Notre-Dame katedralinin cambaz Quasimodo, guzel Cingene kizi Esmeralda'ya platonik bir ask besler. Rahip Frollo ise Esmeralda'ya saplandili bir tutku duyar ve onu ele geciremeyince yikimina sebep olur. Hugo, ortacag Paris'ini canlandirirken dislanmislarin dramiyla mimari mirasin onemini bir arada isler.",
        "karakterler": [
            ("Quasimodo", "Cirkin ama iyi kalpli kambur can calan"),
            ("Esmeralda", "Guzel, ozgur ruhlu Cingene dansci"),
            ("Frollo", "Tutkusunun esiri olan karanlik rahip")
        ],
        "temalar": ["Dis gorunus ve ic guzellik", "Sapkınlik ve tutku", "Toplumsal dislama"],
        "alintilar": [
            "Bir damla su yeter, bir insanı hayata döndürmeye.",
            "Kader! İşte korkunç sözcük."
        ]
    },
    "Uc Silahsorler - Alexandre Dumas": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Genc Gaskonlu d'Artagnan, Paris'e gelerek kralın muhafizlarina katilmak ister. Athos, Porthos ve Aramis ile tanisip dostluk kurar ve birlikte Kardinal Richelieu'nun entrikalarına karsi mucadele ederler. Macera, dostluk ve onur temalarini isleyen eser, dunya edebiyatinin en sevilen macera romanlarindan biridir.",
        "karakterler": [
            ("d'Artagnan", "Cesur, atilgan ve sadik genc Gaskonlu"),
            ("Athos", "Soylu, gizemli gecmisi olan melankolik silahsor"),
            ("Milady de Winter", "Guclu, tehlikeli ve entrikaci kadin casus")
        ],
        "temalar": ["Dostluk ve sadakat", "Macera ve cesaret", "Onur ve sovalyelik"],
        "alintilar": [
            "Hepimiz birimiz, birimiz hepimiz için!",
            "Beklemek en zor şeydir ama en çok pişman olunan şey de acele etmektir."
        ]
    },
    "Monte Kristo Kontu - Alexandre Dumas": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Genc denizci Edmond Dantes, iftiraya uğrayarak 14 yıl hapis yatar. Hapishanede tanistigi rahipten edindiği bilgi ve hazine sayesinde zengin Monte Kristo Kontu kimligine burunur. Kendisine ihanet edenleri tek tek bulur ve sabırla intikamini alir. Roman, intikami ve kaderi sorgulayan destansı bir eserdir.",
        "karakterler": [
            ("Edmond Dantes", "Haksiz yere hapsedilen, intikam arayan genc denizci"),
            ("Abbe Faria", "Dantes'e hapishanede bilgiyi ve hazineyi aktaran yasli rahip"),
            ("Fernand Mondego", "Dantes'e ihanet eden eski arkadasi")
        ],
        "temalar": ["Intikam ve adalet", "Sabir ve plan", "Kader ve ilahi adalet"],
        "alintilar": [
            "Bekle ve umut et!",
            "İnsan ancak acı çekerek güçlenir; acı çekmeden bilgelik olmaz."
        ]
    },
    "Madame Bovary - Gustave Flaubert": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Tasra doktoru Charles Bovary'nin karisi Emma, romantik romanlarda okudugu hayati yasayamadigii icin mutsuz olur. Aldatma ve savurganlığa suruklenen Emma, borclar ve hayal kirikliklari sonunda kendini zehirleyerek intihar eder. Flaubert, burjuva toplumunun ikiyzluuluğunu ve romantizmin tehlikelerini amansız bir gercekcilikle ortaya koyar.",
        "karakterler": [
            ("Emma Bovary", "Hayalleriyle gerceklik arasinda ezilen mutsuz kadin"),
            ("Charles Bovary", "Karisini seven ama anlayamayan siradan doktor"),
            ("Rodolphe", "Emma'yi bastan cikaran sorumsuz toprak sahibi")
        ],
        "temalar": ["Hayal ve gerceklik", "Burjuva elestirisi", "Kadinin toplumsal konumu"],
        "alintilar": [
            "İnsan kendi kaderinin mimarıdır, ama malzeme eksik olunca bina çöker.",
            "Her gülümsemenin arkasında bir esneme gizlidir."
        ]
    },
    "Kirmizi ve Siyah - Stendhal": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Marangoz oglu Julien Sorel, zekası ve hirsiyla toplumsal sinif merdivenlerini tirmanmaya calişir. Once belediye baskaninin karisiyla, sonra bir marki kizyla ilişki yasaarak yukselmek ister. Ancak tutkusu ve gururu onu trajik bir sona surukler. Stendhal, Restorasyon doneminin ikiyuzlulugunu ve sinif catismasini derinlemesine isler.",
        "karakterler": [
            ("Julien Sorel", "Hirsli, zeki ve gururlu genc adam"),
            ("Madame de Renal", "Julien'e asik olan soylu kadin"),
            ("Mathilde de la Mole", "Maceraperest ve gururlu soylu genc kız")
        ],
        "temalar": ["Sinif atlama hirsi", "Ask ve iktidar", "Ikiyzluluk"],
        "alintilar": [
            "Silahım yalnızca yeteneğimdir.",
            "Asıl büyük suç yoksul doğmaktır."
        ]
    },
    "Goriot Baba - Honore de Balzac": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Yasli un tuccar Goriot, iki kizini sosyete hayatina hazirlamak icin tum servetini harcar. Kizlari zenginlesip sosyeteye girince babalarina sirt ceviarir. Genc hukuk ogrencisi Rastignac, bu dramı yakindan izlerken Paris'in acımasizligini ogenir. Balzac, para ve insani degerlerin catismasini acımasızca sergiler.",
        "karakterler": [
            ("Goriot Baba", "Kizlari icin her seyi feda eden ama terk edilen baba"),
            ("Rastignac", "Toplumsal merdiveni tirmanmaya kararlı genc ogrenci"),
            ("Vautrin", "Gizemli ve tehlikeli eski mahkum")
        ],
        "temalar": ["Babalik ve nankorluk", "Para ve ahlak", "Toplumsal hirsi"],
        "alintilar": [
            "Toplumun arkasında daima bir suç vardır.",
            "Bir babanın sevgisi, karşılık beklemeden verilir."
        ]
    },
    "Denizler Altinda Yirmi Bin Fersah - Jules Verne": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Gizemli Kaptan Nemo, muhtesem denizaltisi Nautilus ile okyanuslarin derinliklerini kesifeder. Professor Aronnax ve arkadaslari onun tutsagi olarak bu yolculuga katilir. Nemo'nun medeniyete olan ofkesi ve denizlerin gizleri romanin merkezindedir. Verne, bilim kurgu turünun temellerini atan bu eserde teknoloji ve insanlik iliskisini sorgular.",
        "karakterler": [
            ("Kaptan Nemo", "Gizemli, dahi ve insanliktan kopmus denizalti kaptani"),
            ("Professor Aronnax", "Merakli ve bilgili deniz bilimci"),
            ("Ned Land", "Kacmak isteyen usta zıpkinci")
        ],
        "temalar": ["Bilim ve teknoloji", "Ozgurluk ve yalnizlik", "Doga ve kesif"],
        "alintilar": [
            "Deniz her şeydir. Sonsuz bir huzur kaynağıdır.",
            "Dünya beni ilgilendirmiyor artık, yalnızca deniz."
        ]
    },
    "Yabanci - Albert Camus": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Meursault, annesinin cenaze toreninde aglamaz, ertesi gun denize gidip eglenir. Bir Arap'i nedensizce oldurdukten sonra yargilanir; ancak mahkumiyet, cinayetten cok toplumsal normlara uymama uerine kurulur. Camus'nun absurd felsefesinin edebiyata yansimasi olan eser, anlamsizlik karsisinda bireysel ozgurluğu savunur.",
        "karakterler": [
            ("Meursault", "Duygusuz gorunen, toplumsal normlari reddeden anlatici"),
            ("Marie", "Meursault'nun kiz arkadasi"),
            ("Raymond", "Meursault'yu cinayete surukleyen siddete yatkin komsu")
        ],
        "temalar": ["Absurd ve anlamsizlik", "Toplumsal yargi", "Varoluşsal ozgurluk"],
        "alintilar": [
            "Bugün annem öldü. Ya da dün, bilmiyorum.",
            "İnsan alışır her şeye, bu korkunç bir şey."
        ]
    },
    "Bulanti - Jean-Paul Sartre": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Antoine Roquentin, kucuk bir kasabada tarih arastirmasi yaparken gittikce derinlesen bir varoluşsal bunalima suriklenir. Nesnelerin ve varolusun anlamsizligi onu fiziksel bir bulanti olarak etkiler. Roman, varoluscululugun temel metinlerinden biri olarak kabul edilir ve insanin kendi varolusunu yaratmak zorunda oldugunu isler.",
        "karakterler": [
            ("Antoine Roquentin", "Varolustun anlamsizligiyla yuzlesen yalniz arastirmaci"),
            ("Autodidact", "Kutuphanedeki kitaplari alfabetik okuyan garip adam"),
            ("Anny", "Roquentin'in eski sevgilisi")
        ],
        "temalar": ["Varoluşsal bunalim", "Ozgurluk ve sorumluluk", "Anlam arayisi"],
        "alintilar": [
            "Cehennem başkalarıdır.",
            "Varoluş özden önce gelir."
        ]
    },
    "Kucuk Prens - Antoine de Saint-Exupery": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Sahrda zorunlu inis yapan bir pilot, baska bir gezegenden gelen Kucuk Prens ile tanisir. Kucuk Prens, gezerken ugradigi gezegenlerdeki garip yetiskinleri ve dunya serüvenini anlatir. Gulu, tilkisi ve cölu ile hayatin gercek degerlerini kesfeder. Eser, buyuklerin unuttugu gercekleri cocuksu bir bakisla hatirlatir.",
        "karakterler": [
            ("Kucuk Prens", "Kendi gezegeninden gelen masum ve bilge cocuk"),
            ("Tilki", "Evcillestirme ve baglarin onemini ogreten bilge hayvan"),
            ("Gul", "Kucuk Prens'in gezegenindeki kaprisli ama sevdigi cicek")
        ],
        "temalar": ["Dostluk ve sevgi", "Gercek degerlerin kesfı", "Cocuksu bakis ve bilgelik"],
        "alintilar": [
            "İnsan ancak yüreğiyle baktığında doğru görebilir, asıl gerçekler gözle görülmez.",
            "Sen gülüne verdiğin zamanla güzelsin."
        ]
    },
    "Germinal - Emile Zola": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Genc isci Etienne Lantier, Kuzey Fransa'daki komur madenlerinde calismaya baslar ve iscilerin insanlik disi kosullarini gorerek grevi orgutler. Grev siddete doner, isciler aclik ve baskiyla yuz yuze gelir. Zola, emek mucadelesini ve sinif catismasini dogalci bir tavírla, madenlerin karanliginda canlandirir.",
        "karakterler": [
            ("Etienne Lantier", "Grevi orgutleyen idealist genc isci"),
            ("Catherine Maheu", "Etienne'in asik oldugu genc kadin madenci"),
            ("Maheu ailesi", "Nesillerdir madende calisan yoksul isci ailesi")
        ],
        "temalar": ["Sinif mucadelesi", "Emek ve somuru", "Umit ve isyan"],
        "alintilar": [
            "Ekmek! Ekmek! Ekmek istiyoruz!",
            "Tohumlar atılmıştı, günün birinde filizleneceklerdi."
        ]
    },
    "Sekseninci Gunde Devri Alem - Jules Verne": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Ingiliz centilmeni Phileas Fogg, Reform Kulubu'nde dunyanin 80 gunde dolasilabilecegine dair bahse girer. Uşağı Passepartout ile birlikte tren, gemi ve fil sirtinda bir dünya turuna cikar. Yolda maceralar yaşar, bir kadini kurtarir ve suçlu sanilir. Son anda tarihi atlayarak bahsi kazanır.",
        "karakterler": [
            ("Phileas Fogg", "Soğukkanli, dakik ve zengin İngiliz centilmeni"),
            ("Passepartout", "Sadik, neşeli ve becerikli Fransiz uşak"),
            ("Dedektif Fix", "Fogg'u hirsiz sanan ve takip eden polis")
        ],
        "temalar": ["Macera ve keşif", "Irade ve kararlılık", "Zaman ve hız"],
        "alintilar": [
            "İmkânsız diye bir şey yoktur, yalnızca yetersiz irade vardır.",
            "Her dakikanın değeri vardır, bir dakika bile kaybetmeye hakkımız yok."
        ]
    },
    "Veba - Albert Camus": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Cezayir'in Oran sehrinde veba salgini patlak verir ve sehir karantinaya alinir. Doktor Rieux, salgina karsi umutsuzca mucadele ederken, insanlarin farkli tepkilerini gozlemler. Kimi kacar, kimi direniseder, kimi kar-zarar hesabi yapar. Camus, insanlik durumunu bir alegoriye dönüşturerek dayanisma ve direnisin onemini vurgular.",
        "karakterler": [
            ("Doktor Rieux", "Salgina karsı yorulmaksizin mucadele eden doktor"),
            ("Tarrou", "Gönüllü sağlık ekiplerini organize eden idealist"),
            ("Rambert", "Kaçmak isteyen ama sonunda kalıp mucadele eden gazeteci")
        ],
        "temalar": ["Direnis ve dayanisma", "Absurd ve anlam", "Insan onuru"],
        "alintilar": [
            "Alışkanlık, büyük sessizliklerin çocuğudur.",
            "Bu savaşta kazanılabilecek tek şey bilgi ve anıdır."
        ]
    },
    "Tehlikeli Iliskiler - Choderlos de Laclos": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Vicomt de Valmont ve Marquise de Merteuil, aristokrat toplumda entrika ve basdan cikarma oyunlari oynarlar. Valmont masum Madame de Tourvel'i bastan cikarma gorevini ustlenir ancak gercekten asik olur. Mektuplar yoluyla anlatilan roman, 18. yuzyıl Fransa'sında ahlaki cozulmenin ve guc oyunlarinin acımasız bir portresini cizer.",
        "karakterler": [
            ("Valmont", "Karizmatik, manipulatif ve sonunda asin kurban olan aristokrat"),
            ("Marquise de Merteuil", "Zeki, hesapci ve tehlikeli aristokrat kadın"),
            ("Madame de Tourvel", "Erdemli ama Valmont'un tuzagina dusen kadin")
        ],
        "temalar": ["Manipulasyon ve guc", "Ask ve tutku", "Ahlaki cozulme"],
        "alintilar": [
            "Savaş alanında silahları aşk olan bir savaşçıyım.",
            "İntikam soğuk yenir."
        ]
    },
    "Toprak - Emile Zola": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Beauce ovasindaki köylülerin toprak hirsi ve aile ici catismalari anlatilir. Yasli ciftci Fouan, topragini cocuklarina bolusturunce aile ici kavgalar, cinayet ve ihanete sahne olur. Zola, köy hayatinin romantik goruntusunun arkasindaki acgozluluk ve vahşeti dogalcı bir tavırla gozler onune serer.",
        "karakterler": [
            ("Jean Macquart", "Köye gelen disaridan gelen dürüst isçi"),
            ("Fouan", "Topragini dagitan ve perisan olan yasli ciftci"),
            ("Buteau", "Açgözlü ve gaddar oğul")
        ],
        "temalar": ["Toprak hirsi", "Aile ici catisma", "Koy hayatinin gerçekleri"],
        "alintilar": [
            "Toprak yalan söylemez.",
            "İnsanın en büyük düşmanı kendi kanıdır."
        ]
    },

    # ========================== INGILIZ EDEBIYATI (20) ==========================

    "Oliver Twist - Charles Dickens": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Yetimhanede buyuyen Oliver, aclik cekmekten yorulup Londra'ya kacar ve oreada Fagin'in hirsiz cetesine katilir. Masum Oliver, suç dnyasinin icinde bile iyiligini korur ve sonunda gercek ailesini bulur. Dickens, Victoria donemindeki yoksulluk, cocuk istismari ve toplumsal adaletsizliği sert bir dille elestrir.",
        "karakterler": [
            ("Oliver Twist", "Masum, iyi kalpli yetim cocuk"),
            ("Fagin", "Cocuk hirsizlari yoneten kurnaz yasli adam"),
            ("Bill Sikes", "Vahsi ve acımasız suçlu")
        ],
        "temalar": ["Cocuk yoksullugu", "Iyilik ve masumiyetin gucu", "Toplumsal adalet"],
        "alintilar": [
            "Lütfen efendim, biraz daha alabilir miyim?",
            "Dünyada en çok aldatılan insanlar, en az şüphe edenlerdir."
        ]
    },
    "Iki Sehrin Hikayesi - Charles Dickens": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Fransiz Devrimi srasinda Londra ve Paris arasinda gecen roman, Dr. Manette'in Bastille'den kurtulmasından sonra gelisen olaylari anlatir. Avukat Sydney Carton, sevdigi kadin Lucie'nin kocasi Charles Darnay'i kurtarmak icin darağacına gider. Dickens, fedakarlik, devrim ve adalet temalarini etkileyici bir tarihsel arka planda isler.",
        "karakterler": [
            ("Sydney Carton", "Hayatini baskasi icin feda eden avukat"),
            ("Charles Darnay", "Soylu kokeninden kaçan iyi kalpli Fransiz"),
            ("Lucie Manette", "Babsina ve kocasina sadik, sevgi dolu genc kadin")
        ],
        "temalar": ["Fedakarlik ve kurtuluş", "Devrim ve siddet", "Ask ve sadakat"],
        "alintilar": [
            "Bu yaptığım, yaptığım en iyi şey; gittiğim yer, gittiğim en iyi yer.",
            "Zamanların en iyisiydi, zamanların en kötüsüydü."
        ]
    },
    "Buyuk Beklentiler - Charles Dickens": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Yoksul yetim Pip, gizemli bir hayırsever sayesinde Londra'da centilmen olma firsati yakalar. Zenginligin ve toplumsal statu hirsinın onu nasıl degistirdigini fark edene kadar gercek degerleri goremez. Miss Havisham'in manipulasyonu ve Estella'ya duyduğu ask, Pip'in olgunlasma yolculugunu sekillendirir.",
        "karakterler": [
            ("Pip", "Buyuk beklentilerle buyuyen yetim cocuk"),
            ("Miss Havisham", "Dugununde terk edilmis, intikam planlayan eksantrik kadin"),
            ("Estella", "Miss Havisham tarafindan erkekleri kiracak sekilde yetistirilen guzel kiz")
        ],
        "temalar": ["Sinif ve kimlik", "Gercek degerler ve sahte hayaller", "Olgunlasma"],
        "alintilar": [
            "Acı çekmek, güçlenmektir.",
            "Kalbini kırdığım için sana minnettarım; çünkü kırılması gereken şeyi kırdım."
        ]
    },
    "Jane Eyre - Charlotte Bronte": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Yetim ve yoksul Jane Eyre, Thornfield Maliknesine mürebbiye olarak gelir ve gizemli ev sahibi Rochester'a asik olur. Dugun gununde Rochester'in tavan arasinda kapali tuttuğu deli esi ortaya cikar. Jane onurunu koruyarak gider ancak sonunda ask ve ozgurluk arasında bir denge bulur.",
        "karakterler": [
            ("Jane Eyre", "Bagimsiz, ilkeli ve guclu iradeli genc kadin"),
            ("Edward Rochester", "Karanlik sirri olan ama tutkulu ev sahibi"),
            ("Bertha Mason", "Tavan arasinda saklanan Rochester'in deli esi")
        ],
        "temalar": ["Kadin bagimsizligi", "Ask ve onur", "Sinif esitsizligi"],
        "alintilar": [
            "Ben bir kuş değilim; beni hiçbir ağ tutamaz. Özgür iradeye sahip bağımsız bir insanım.",
            "Güzellik satın alınamaz, kazanılır."
        ]
    },
    "Ugultulu Tepeler - Emily Bronte": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Heathcliff, kimsesiz bir cocuk olarak Earnshaw ailesine getirilir ve Catherine'e derin bir ask duyar. Catherine'in zengin Edgar Linton ile evlenmesi Heathcliff'i intikamc bir canvara donusturur. Iki nesil boyunca surecek yikici bir ask ve intikam sarmalı, Yorkshire bocalarinin kasvetli atmosferinde gerceklesir.",
        "karakterler": [
            ("Heathcliff", "Aski intikama donusen karanlik ve tutkulu adam"),
            ("Catherine Earnshaw", "Heathcliff'i seven ama sosyal statüyü seçen kadin"),
            ("Edgar Linton", "Catherine'in kocası olan nazik ama zayif centilmen")
        ],
        "temalar": ["Yikici ask", "Intikam", "Dogayla bütünleşme"],
        "alintilar": [
            "Ben Heathcliff'im! O her zaman aklımda, kendim olarak değil, benden daha çok ben olarak.",
            "Ruhlarımız aynı maddeden yapılmıştır."
        ]
    },
    "Gurur ve Onyargi - Jane Austen": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Elizabeth Bennet, zengin ve kibirli gorunen Mr. Darcy ile ilk karşilasmada birbirlerinden hoslanmazlar. Zamanla onyargilarini aşarak birbirlerini tanirlar; Elizabeth Darcy'nin aslında iyi bir adam oldugunu, Darcy ise Elizabeth'in zekasini takdir ettigini kavrar. Austen, Regency donemi İngiltresi'nde sinif, evlilik ve kadin kimligini ince bir iroaniyle isler.",
        "karakterler": [
            ("Elizabeth Bennet", "Zeki, esprili ve bagimsiz genc kadin"),
            ("Mr. Darcy", "Zengin, kibirli gorunen ama aslinda onurlu centilmen"),
            ("Mrs. Bennet", "Kizlarini zengin kocaya vermek isteyen telaşlı anne")
        ],
        "temalar": ["Onyargi ve gerceklik", "Ask ve evlilik", "Sinif farkliliklari"],
        "alintilar": [
            "Servet sahibi bekar bir erkeğin, bir eşe ihtiyaç duyduğu evrensel bir gerçektir.",
            "Kibir ile gösteriş arasında büyük fark vardır."
        ]
    },
    "Dorian Gray'in Portresi - Oscar Wilde": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Genc ve guzel Dorian Gray, portresinin kendi yerine yaslanmasini diler ve dilegi gerceklesir. Yillar boyunca genc kalan Dorian, ahlaki çöküse sürüklenirken tüm günahları portresine yansir. Sonunda tabloyu bicakladiginda, portredeki gencliğe kavusur ama Dorian bir anda yaslanarak olur.",
        "karakterler": [
            ("Dorian Gray", "Ebedi gencliğe kavusan ama ahlaken cürüyen genc adam"),
            ("Lord Henry", "Dorian'i etkileyen, hedonist ve alaycı aristokrat"),
            ("Basil Hallward", "Dorian'in portresini yapan ve onun iyiligine inanan ressam")
        ],
        "temalar": ["Guzellik ve ahlak", "Hedonizm", "Sanat ve gerceklik"],
        "alintilar": [
            "Her portrenin arkasında ressamın ruhu vardır.",
            "Günaha karşı koymanın tek yolu, ona teslim olmaktır."
        ]
    },
    "Define Adasi - Robert Louis Stevenson": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Genc Jim Hawkins, olen bir denizciden hazine haritasi bulur ve macera yolculuguna cikar. Gemi mürettebati arasina karisan korsan John Silver, elesbasiligin ele gecirmeyi planlar. Jim'in cesareti ve zekasi sayesinde hazine bulunur ve korsanlara karsi zafer kazanilir.",
        "karakterler": [
            ("Jim Hawkins", "Cesur ve merakli genc anlatici"),
            ("Long John Silver", "Tek bacakli, karizmatik ve kurnaz korsan"),
            ("Kaptan Smollett", "Disiplinli ve guvenilir gemi kaptani")
        ],
        "temalar": ["Macera ve cesaret", "Sadakat ve ihanet", "Buyume ve olgunlasma"],
        "alintilar": [
            "Ölü adamlar masal anlatmaz.",
            "Her yiğidin gönlünde bir korsan yatar."
        ]
    },
    "Frankenstein - Mary Shelley": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Bilim insani Victor Frankenstein, olu dokulardan canli bir yaratik olusturur ancak yarattigi varliktan dehsetle kacar. Terk edilen yaratik, yalnizlik ve reddedilmenin acisiyla intikam arar ve Frankenstein'in sevdiklerini tek tek oldurur. Shelley, bilimsel hirsin ve yaraticinin sorumlulugunun sonuclarini sorgular.",
        "karakterler": [
            ("Victor Frankenstein", "Doğanin sirrini cozmeye calisan hirsli bilim insani"),
            ("Yaratik", "Çirkin disina ragmen duygu ve zeka sahibi yapay varlik"),
            ("Elizabeth", "Frankenstein'in nişanlısı ve yaratiğin kurbani")
        ],
        "temalar": ["Bilimin sinirlari", "Yaratici ve yaratilan", "Yalnizlik ve reddedilme"],
        "alintilar": [
            "Dikkat et, çünkü korkusuzum ve bu yüzden güçlüyüm.",
            "Hiçbir şey insanın ruhunu, başkalarının sevgisinden mahrum kalmak kadar yıkmaz."
        ]
    },
    "1984 - George Orwell": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Winston Smith, totaliter Parti'nin her seyi kontrol ettigi Okyanusya'da yasadir. Buyuk Birader'in gozettimi altında dusunce ozgurlugu bile yok edilmistir. Winston, Julia ile yasak bir ask yasayarak sisteme isyan etmeye calisir ancak Düşünce Polisi tarafindan yakalanir ve kisiliginden sıyrılana kadar iskenmeye maruz kalir.",
        "karakterler": [
            ("Winston Smith", "Sisteme gizlice isyan eden Doğruluk Bakanliği çalışanı"),
            ("Julia", "Winston'la birlikte Parti'ye karsi direnen genc kadin"),
            ("O'Brien", "Winston'u tuzaga dusuren gizemli Parti yetkilisi")
        ],
        "temalar": ["Totalitarizm", "Bireysel ozgurluk", "Gerceklik kontrolu"],
        "alintilar": [
            "Büyük Birader sizi izliyor.",
            "Özgürlük, iki artı ikinin dört ettiğini söyleyebilmektir."
        ]
    },
    "Hayvan Ciftligi - George Orwell": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Manor Ciftligindeki hayvanlar, insanlarin zulmünden kurtulmak icin devrim yapar. Domuzlar liderliginde kurlan yeni duzende esitlik vaat edilir, ancak domuzlar zamanla insanlardan daha baskıcı hale gelir. Orwell, Sovyet devriminin yozlasmasini bir allegori ile anlattigi bu kisa romanda iktidarin yozlastırici etkisini gosterir.",
        "karakterler": [
            ("Napoleon", "Iktidari ele geciren acımasız domuz diktatr"),
            ("Boxer", "Sadik, caliskan ama sonunda ihanete ugrayan at"),
            ("Squealer", "Propagandayla hayvanları manipüle eden konuskan domuz")
        ],
        "temalar": ["Iktidar ve yozlaşma", "Devrim ve ihanet", "Propaganda"],
        "alintilar": [
            "Bütün hayvanlar eşittir, ama bazı hayvanlar daha eşittir.",
            "Dört bacak iyi, iki bacak kötü!"
        ]
    },
    "Cesur Yeni Dunya - Aldous Huxley": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Gelecekte insanlar genetik muhendislikle uretilir, sinifara ayrilir ve mutluluk ilaci soma ile uyumsuz hale getirilir. Vahsi John, bu mükemmel dünyanın disinda büyumüs biridir ve sisteme meydan okur. Huxley, mutluluk ve ozgurluk arasindaki secimi sorgulayarak teknolojik totalitarizmin tehlikelerini sergiler.",
        "karakterler": [
            ("Bernard Marx", "Sisteme uyum saglayamayan, dusuk boy Alpha"),
            ("John Vahsi", "Rezervasyonda buyumus, Shakespeare okuyan isyanci"),
            ("Lenina Crowne", "Sistemin ideal vatandası olan genc kadin")
        ],
        "temalar": ["Distopya ve kontrol", "Ozgurluk ve mutluluk", "Teknoloji ve insanlik"],
        "alintilar": [
            "Mutsuz olma hakkını istiyorum.",
            "Gerçek mutluluk her zaman çirkin görünür."
        ]
    },
    "Sineklerin Efendisi - William Golding": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Bir grup Ingiliz okul cocugu, ucak kazasi sonucu issiz bir adada mahsur kalir. Baslangicta demokretik kurallar olusturmaya calisirlar, ancak zamanla vahşete suruklenirler. Ralph'in liderligine karsi Jack'in barbarligi galip gelir. Golding, medeniyetin ince kabuğunun altindaki insani vahşeti ve kötülugun dogasini sorgular.",
        "karakterler": [
            ("Ralph", "Düzen ve kurallari savunan demokratik lider"),
            ("Jack", "Avcılık ve guce tapan vahsi lider"),
            ("Piggy", "Akil ve mantigi temsil eden gozluklu, sisman cocuk")
        ],
        "temalar": ["Insanin doğasi", "Medeniyet ve barbarlık", "Guc ve liderlik"],
        "alintilar": [
            "Canavar dışarıda değil, içimizde.",
            "Kurallar! Kurallar! Tek sahip olduğumuz şey kurallar!"
        ]
    },
    "Yuzuklerin Efendisi - J.R.R. Tolkien": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Hobbit Frodo Baggins, karanlik lord Sauron'un guc yuzu olan Tek Yuzugu imha etmek icin tehlikeli bir yolculuga cikar. Yuzuk Kardesliği ile birlikte Orta Dunya'yi kurtarmaya calisirken, yuzugün yozlastirici gucu her an onu tehdit eder. Tolkien'in epik fantasisi, iyilik ve kötüluk arasindaki ebedi mucadeleyi efsanevi bir evren icinde anlatir.",
        "karakterler": [
            ("Frodo Baggins", "Yuzugu tasiyan cesur ve fedakar hobbit"),
            ("Gandalf", "Bilge ve güclü büyücü, Kardesligin rehberi"),
            ("Aragorn", "Sürgündeki kral, insanligin umidi")
        ],
        "temalar": ["Iyilik ve kotuluk", "Gucun yozlastirmasi", "Dostluk ve fedakarlik"],
        "alintilar": [
            "Yaşadığımız zamana karar vermek bize düşmez, tek yapabileceğimiz bize verilen zamanla ne yapacağımıza karar vermektir.",
            "Parlayan her şey altın değildir."
        ]
    },
    "Harry Potter ve Felsefe Tasi - J.K. Rowling": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Yetim Harry Potter, 11 yasinda bir buyucu oldugunu ogrenir ve Hogwarts Buyuculuk Okulu'na gider. Okulda arkadaslik kurar, buyuculuk ogranir ve karanlik buyucu Voldemort'un geri donme planlarina karsi mucadele eder. Rowling, buyuma, dostluk ve cesaret temalarini büyülü bir dünyada isler.",
        "karakterler": [
            ("Harry Potter", "Yetim buyucu cocuk, Seçilmiş Kisi"),
            ("Hermione Granger", "Zeki ve çalışkan muggle doğumlu cadı"),
            ("Ron Weasley", "Harry'nin sadik ve esprili en yakin arkadasi")
        ],
        "temalar": ["Buyume ve kimlik", "Dostluk ve cesaret", "Iyilik ve kotuluk"],
        "alintilar": [
            "Düşmanlarımıza karşı çıkmak cesaret ister ama dostlarımıza karşı çıkmak daha çok cesaret ister.",
            "Mutluluk en karanlık zamanlarda bile bulunabilir, eğer ışığı açmayı hatırlarsan."
        ]
    },
    "Robinson Crusoe - Daniel Defoe": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Robinson Crusoe, gemi kazasindan sag kurtularak issiz bir adaya düşer. 28 yil boyunca tek basina hayatta kalmayi ogrenir: barinak yapar, tarim yapar, hayvan yetistirir. Bir yerliden kurtardigi Cuma ile birlikte yasam mucadelesini surdurur. Defoe, insanin doga karsisındaki mucadelesini ve iradesinin gucunu anlatir.",
        "karakterler": [
            ("Robinson Crusoe", "Issiz adada hayatta kalan pratik ve iradeli denizci"),
            ("Cuma", "Crusoe'nin kurtardıgi ve egittigi yerli adam"),
            ("Crusoe'nun babasi", "Oglanı maceralardan vazgecirmeye calisan baba")
        ],
        "temalar": ["Hayatta kalma", "Insan ve doga", "Uygarlıgin kurulması"],
        "alintilar": [
            "Korku, tehlikenin kendisinden daha tehlikelidir.",
            "Yalnızlıkta insan, kendi en iyi arkadaşı olmayı öğrenir."
        ]
    },
    "Guliver'in Gezileri - Jonathan Swift": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Gemi doktoru Lemuel Guliver, dört ayri yolculukta fantastik ulkeleri ziyaret eder: cuceler ulkesi Liliput, devler ulkesi Brobdingnag, ucak ada Laputa ve atlar ulkesi Houyhnhnm. Her ulke, insan toplumunun farkli bir zaafini hicveder. Swift, insanlik durumunu ince bir alayla elestiren bu eserle siyasi hicvin basyapitini ortaya koyar.",
        "karakterler": [
            ("Lemuel Guliver", "Merakli ve saf gemi doktoru"),
            ("Liliput Krali", "Küçük boyuna ragmen buyuk iktidar hirsi olan hukumdar"),
            ("Houyhnhnmlar", "Akli ve erdemli temsil eden konusan atlar")
        ],
        "temalar": ["Insan dogasinin elestirisi", "Siyasi hiciv", "Gerceklik ve perspektif"],
        "alintilar": [
            "Savaşlar, yeterince yiyecek veya yeterince yer olmadığı için değil, yeterince akıl olmadığı için çıkar.",
            "Her insanın gözünde kendi ülkesi dünyanın merkezidir."
        ]
    },
    "Dr. Jekyll ve Mr. Hyde - Robert Louis Stevenson": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Saygin doktor Henry Jekyll, insanin iceindeki kotu tarafı ayirmak icin bir iksir gelisir. Iksiri ictiginde canavarca Mr. Hyde'a donusur. Zamanla Hyde kontrolden cikar ve Jekyll kimligine geri donemez hale gelir. Stevenson, insanin icindeki ikilik ve ahlaki catismayi gerilim dolu bir anlatimla isler.",
        "karakterler": [
            ("Dr. Jekyll", "Saygin ama karanlık tarafinni kesfetmek isteyen doktor"),
            ("Mr. Hyde", "Jekyll'in kotu ve canavarca alter egosu"),
            ("Mr. Utterson", "Gercegi arastiran sadik avukat arkadas")
        ],
        "temalar": ["Insanin ikili dogasi", "Iyilik ve kotuluğun ayriliği", "Bilimin sinilari"],
        "alintilar": [
            "İnsan gerçekte bir değil, iki varlıktır.",
            "Her günahın arkasında gizli bir zevk yatar."
        ]
    },

    # ========================== AMERIKAN EDEBIYATI (20) ==========================

    "Tom Sawyer'in Maceralari - Mark Twain": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Yaramaz ve hayalperest Tom Sawyer, Mississippi Nehri kıyisindaki kasabada arkadaslariyla maceralar yasar. Cit boyama hilesinden mezarlikta cinayete taniklığa, definece aramadan kayip cocuk olarak geri donmeye kadar sayisiz serüven gecirir. Twain, Amerikan cocuklugunu neşeli ve hicivli bir dille canlandirir.",
        "karakterler": [
            ("Tom Sawyer", "Yaramaz, zeki ve maceraperest cocuk"),
            ("Huckleberry Finn", "Tom'un en yakin arkadasi, serseri cocuk"),
            ("Becky Thatcher", "Tom'un asık oldugu kiz")
        ],
        "temalar": ["Cocukluk ve macera", "Ozgurluk", "Toplumsal kurallar ve isyan"],
        "alintilar": [
            "İşi sevmek onu eğlenceye dönüştürür.",
            "Okulu asmanın tadını, okula gitmeden bilemezsin."
        ]
    },
    "Huckleberry Finn'in Maceralari - Mark Twain": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Huck Finn, alkolik babasindan kacarak kole Jim ile birlikte Mississippi'de sal yolculuğuna cikar. Yolda dolandiricilar, aile kavgalari ve tehlikelerle karsilasir. Huck, toplumun koleliğe bakışına ragmen Jim'in ozgurlugu icin savasmaya karar verir. Twain, irk ayrimcilığı ve toplumsal ikiyüzlulugu cocugun gozunden elestrir.",
        "karakterler": [
            ("Huck Finn", "Toplum kurallarini reddeden özgur ruhlu cocuk"),
            ("Jim", "Ozgurlugune kavusmak isteyen kacak kole"),
            ("Tom Sawyer", "Huck'in maceraperest arkadasi")
        ],
        "temalar": ["Irk ayrimciliği", "Ozgurluk ve vicdan", "Toplumsal elestiri"],
        "alintilar": [
            "Pekâlâ, o zaman cehenneme gideyim!",
            "Doğru olanı yapmak bazen en zor olandır."
        ]
    },
    "Moby Dick - Herman Melville": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Kaptan Ahab, bacagını kopartan beyaz balina Moby Dick'e karsi saplantili bir intikam pesinde kosar. Gemici Ishmael'in gozunden anlatilan roman, insanin doğa karsisindaki gucsuzlugunu ve saplantinin yikicilığını isler. Melville, denizcilik dünyasını alegorik bir derinlikle betimleyerek Amerikan edebiyatinin en büyük eserlerinden birini yaratmistir.",
        "karakterler": [
            ("Kaptan Ahab", "Beyaz balinaya saplantili intikam gudeı deli kaptan"),
            ("Ishmael", "Olayları anlatan genç denizci"),
            ("Moby Dick", "Dev beyaz kasalot balinası")
        ],
        "temalar": ["Saplanti ve yikim", "Insan ve doğa", "Kader ve irade"],
        "alintilar": [
            "Beni adımla çağırın: Ishmael.",
            "Ölümden korkmuyorum; ama yaşamadan ölmekten korkuyorum."
        ]
    },
    "Buyuk Gatsby - F. Scott Fitzgerald": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Gizemli milyoner Jay Gatsby, Long Island'da gondermeli partiler vererek eski aski Daisy'i geri kazanmayi planlar. Nick Carraway'in gozunden anlatilan hikaye, Amerikan rüyasinin iciinin bosluğunu ortaya koyar. Gatsby'nin hayalleri, zenginligin ve statunun ardindaki yalnizlik ve trajediyle son bulur.",
        "karakterler": [
            ("Jay Gatsby", "Daisy icin zengin olan gizemli ve romantik adam"),
            ("Daisy Buchanan", "Guzel ama yüzeysel ve karasiz ust sinif kadini"),
            ("Nick Carraway", "Olaylari izleyen ve anlatan dürüst anlatici")
        ],
        "temalar": ["Amerikan rüyasinin cokusu", "Ask ve hayal kirikligi", "Zenginlik ve ahlak"],
        "alintilar": [
            "Ve böylece karşı akıntıya rağmen kürek çekmeye devam ediyoruz; durmaksızın geçmişe sürüklenerek.",
            "Gatsby yeşil ışığa inanıyordu."
        ]
    },
    "Farelere ve Insanlara - John Steinbeck": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Gezici tarim iscileri George ve zihinsel engelli arkadasi Lennie, kendi ciftliklerine sahip olma hayali kurarlar. Lennie'nin kontrol edemedigi gücü, istemsiz bir cinayetle sonuclanir ve George en zor karari vermek zorunda kalir. Steinbeck, Büyük Buhran döneminde emekci sinifin umitsizliğini ve dostluğun gücünü trajik bir dille anlatır.",
        "karakterler": [
            ("George Milton", "Küçuk yapili, zeki ve koruyucu gezici isci"),
            ("Lennie Small", "Dev yapilı ama zihinsel engelli, masum adam"),
            ("Curley'in karisi", "Yalniz ve ilgi arayan, trajik sonu olan genc kadin")
        ],
        "temalar": ["Dostluk ve fedakarlik", "Amerikan ruyasi", "Yalnizlik ve umitsizlik"],
        "alintilar": [
            "Bir insanın başka bir insanla konuşacağı biri olması güzel bir şeydir.",
            "Tavşanlardan bana anlat, George."
        ]
    },
    "Gazap Uzumleri - John Steinbeck": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Joad ailesi, Büyük Buhran ve toz firtinalari yuzünden Oklahoma'daki ciftliklerini terk ederek Kaliforniya'ya göç eder. Vaat edilen topraklarda sefaletten baska bir sey bulamazlar; sömurü, aclik ve sosyal adaletsizlik ile yuz yuze gelirler. Steinbeck, göcmen iscilerin trajedisini epik bir boyutta anlatir.",
        "karakterler": [
            ("Tom Joad", "Sartli tahliye olmus, ailesiyle birlikte göc eden genc adam"),
            ("Ma Joad", "Aileyi bir arada tutan guclu ve fedakar anne"),
            ("Jim Casy", "Eski papaz, sendika örgutcusu olarak mucadele eder")
        ],
        "temalar": ["Goc ve yerinden edilme", "Toplumsal adalet", "Ailenin gucu"],
        "alintilar": [
            "Nerede haksızlık varsa orada olacağım.",
            "Gazap üzümleri ağır ağır olgunlaşıyor."
        ]
    },
    "Cavdarda Biri Var - J.D. Salinger": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "On alti yasindaki Holden Caulfield, okuldan atildiktan sonra New York sokaklarinda dolanir. Buyuklerin sahtekarligina öfke duyan Holden, masumiyet ve cocuklugun yitirilmesine isyan eder. Kardeşi Phoebe'ye cavdanlıkta cocuklari korumak istedigini söyler. Salinger, ergenlik bunalimini Amerikan edebiyatinin en ikonik sesiyle anlatır.",
        "karakterler": [
            ("Holden Caulfield", "Isyankar, hassas ve bunalimli ergen anlatici"),
            ("Phoebe", "Holden'in cok sevdiği küçuk kız kardeşi"),
            ("Mr. Antolini", "Holden'a yardim etmeye calisan eski öğretmeni")
        ],
        "temalar": ["Ergenlik bunalimi", "Sahtekarlik ve masumiyetin kaybi", "Yalnızlik"],
        "alintilar": [
            "Büyüklerin çoğu sahtekar. Bunu söylüyorum işte.",
            "Çavdarlıkta oyun oynayan çocukları yakalamak istiyorum, uçurumdan düşmeden önce."
        ]
    },
    "Yaslı Adam ve Deniz - Ernest Hemingway": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Yasli Kübalı balıkçı Santiago, 84 gündür hic balik tutamamisken açık denizde dev bir kılıç balığıyla mucadeleye girer. Günlerce süren amansiz savasta baligini yener ama köpekbaliklari ganimetini yer. Santiago eli bos ama yenilmemis olarak döner. Hemingway, insanin doğa karsisindaki onurlu direnişini yalın bir dille anlatir.",
        "karakterler": [
            ("Santiago", "Yasli, yoksul ama yenilmeyen Kübalı balıkçı"),
            ("Manolin", "Santiago'ya büyük saygi duyan genç çırak"),
            ("Kılıç balığı", "Santiago'nun saygı duyduğu dev rakip")
        ],
        "temalar": ["Insanin doğayla mücadelesi", "Onur ve dayanıklılık", "Yenilgi ve zafer"],
        "alintilar": [
            "İnsan yok olmak için yaratılmış olabilir ama yenilmek için değil.",
            "Şimdi onu yeneceğim; ne kadar büyük olursa olsun."
        ]
    },
    "Silahara Veda - Ernest Hemingway": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Birinci Dünya Savaşı'nda İtalyan cephesinde ambulans soförlüğü yapan Amerikalı Frederick Henry, İngiliz hemşire Catherine Barkley'e aşık olur. Savas, yaralanma ve kayip arasinda ask iliskisi derinlesir. Isviçre'ye kaçsalar da Catherine doğumda ölür. Hemingway, savaşın anlamsizligini ve askin kırılganlığını kendi deneyimlerinden beslenerek anlatir.",
        "karakterler": [
            ("Frederick Henry", "Savaşta anlam arayan Amerikalı ambulans şoförü"),
            ("Catherine Barkley", "Henry'yi seven İngiliz hemşire"),
            ("Rinaldi", "Henry'nin İtalyan doktor arkadaşı")
        ],
        "temalar": ["Savaş ve anlamsızlık", "Aşk ve kayıp", "Bireysel yalnizlik"],
        "alintilar": [
            "Dünya herkesi kırar; ve sonra kırılan yerlerden güçleneenler olur.",
            "Savaşa veda etmek yetmez, silahlara da veda etmek gerek."
        ]
    },
    "Bülbülü Öldürmek - Harper Lee": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Alabama'da yasayan kucuk Scout Finch, avukat babasi Atticus'un siyah bir adami haksız yere suclanan davada savunmasını izler. Irk ayrımcılığının derin kökleri ve masum insanların toplumsal onyargi tarafindan ezilmesi, bir cocugun gozünden anlatilir. Lee, adalet, empati ve ahlaki cesaret üzerine Amerikan edebiyatının en sevilen eserlerinden birini yazmistir.",
        "karakterler": [
            ("Scout Finch", "Merakli, dürüst ve sorgulayan küçük kız anlatıcı"),
            ("Atticus Finch", "Adil, cesur ve ilkeli avukat baba"),
            ("Tom Robinson", "Haksız yere suçlanan masum siyah adam")
        ],
        "temalar": ["Irk ayrımcılığı", "Adalet ve ahlak", "Masumiyet ve büyüme"],
        "alintilar": [
            "Bir insanı gerçekten anlamak istiyorsan onun derisinin içine girip dolaşman gerekir.",
            "Bir bülbülü öldürmek günahtır, çünkü onlar yalnızca şarkı söyler."
        ]
    },
    "Ucurtma Avcisi - Khaled Hosseini": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Afgan çocuk Emir, en yakın arkadaşı ve hizmetçisi Hassan'a yapılan zulme sessiz kalır ve bu suçluluk onu yıllarca takip eder. Taliban döneminde Afganistan'a geri dönerek Hassan'ın oğlunu kurtarır ve geçmişiyle yüzleşir. Hosseini, dostluk, ihanet ve kefareti Afganistan'ın trajik tarihiyle harmanlayarak evrensel bir hikaye anlatır.",
        "karakterler": [
            ("Emir", "Suçluluk duygusunu taşıyan ve kefaret arayan anlatıcı"),
            ("Hassan", "Sadık, cesur ve masum hizmetçi çocuk"),
            ("Baba", "Güçlü, onurlu ama sırlarla dolu Emir'in babası")
        ],
        "temalar": ["Suçluluk ve kefaret", "Dostluk ve ihanet", "Göç ve kimlik"],
        "alintilar": [
            "Senin için bin kere bile!",
            "Çocukken attığımız her adım, yetişkinliğimizin temelini oluşturur."
        ]
    },
    "Küçük Kadınlar - Louisa May Alcott": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "İç Savaş sırasında babaları cephede olan March ailesinin dört kız kardeşi -Meg, Jo, Beth ve Amy- anneleriyle birlikte büyümenin zorluklarıyla yüzleşir. Her biri farklı hayalleri ve kişilikleriyle kendi yolunu çizer. Alcott, kadınlığa geçiş sürecini, aile bağlarını ve bireysel özgürlüğü sıcak bir dille anlatır.",
        "karakterler": [
            ("Jo March", "Yazar olmak isteyen bağımsız ve isyankâr kız"),
            ("Beth March", "Utangaç, müziksever ve fedakâr en küçük kardeş"),
            ("Meg March", "Geleneksel ve şefkatli büyük kardeş")
        ],
        "temalar": ["Büyüme ve kadınlık", "Aile bağları", "Bağımsızlık ve gelenek"],
        "alintilar": [
            "Kadınların da zekâları ve ruhları var, yalnızca güzellik ve para değil.",
            "Kalemin kılıçtan güçlü olduğuna inanıyorum."
        ]
    },
    "Vahşetin Çağrısı - Jack London": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Evcil köpek Buck, Kaliforniya'daki rahat yaşamından çalınarak Alaska'nın buz çöllerine kızak köpeği olarak gönderilir. Vahşi doğada hayatta kalmayı öğrenirken içindeki ilkel güdüler uyanır. Sonunda insanlardan koparak kurt sürüsüne katılır. London, doğanın acımasız yasalarını ve içgüdüsel gücü etkileyici bir şekilde anlatır.",
        "karakterler": [
            ("Buck", "Evcil hayattan vahşi doğaya dönen güçlü köpek"),
            ("John Thornton", "Buck'ın son ve en çok sevdiği sahibi"),
            ("Spitz", "Buck'ın kızak ekibindeki acımasız rakibi")
        ],
        "temalar": ["Doğaya dönüş", "Hayatta kalma", "İçgüdü ve uygarlık"],
        "alintilar": [
            "Ölüm soğuk ve karanlıktı ama yaşam sıcak ve parlaktı.",
            "Güçlü olan hayatta kalır, zayıf olan yok olur."
        ]
    },
    "Fahrenheit 451 - Ray Bradbury": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Gelecekte kitaplar yasaklanmış ve itfaiyeciler yangın söndürmek yerine kitap yakmakla görevlendirilmiştir. İtfaiyeci Montag, yaktığı kitaplardan birini okuyunca hayatı değişir ve sisteme karşı çıkmaya başlar. Bradbury, düşünce özgürlüğünün bastırılmasını ve teknolojinin insanları uyuşturmasını distopik bir gelecekte anlatır.",
        "karakterler": [
            ("Guy Montag", "Kitap yakan ama gerçeği keşfeden itfaiyeci"),
            ("Clarisse McClellan", "Montag'ı sorgulamaya başlatan genç kız"),
            ("Kaptan Beatty", "Kitapların neden yakılması gerektiğini savunan itfaiye şefi")
        ],
        "temalar": ["Sansür ve düşünce özgürlüğü", "Teknoloji ve yabancılaşma", "Bilgi ve cehalet"],
        "alintilar": [
            "Kitap yakmanıza gerek yok, insanların okumasını engelleyin yeter.",
            "Bir kitap, yüklü bir silahtır."
        ]
    },
    "Bin Muhteşem Güneş - Khaled Hosseini": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Afganistan'da iki farklı nesilden kadın -gayrimeşru çocuk Meriam ve şehirli Leyla- aynı erkeğin eşleri olarak bir araya gelir. Başlangıçta düşman olan iki kadın, Taliban rejiminin zulmü altında birleşerek dayanışma gösterir. Hosseini, Afgan kadınlarının direncini ve fedakârlığını otuz yıllık tarihsel çerçevede anlatır.",
        "karakterler": [
            ("Meriam", "Gayrimeşru doğan, hayat boyu aşağılanan ama sonunda kahraman olan kadın"),
            ("Leyla", "Eğitimli, cesur ve mücadeleci genç kadın"),
            ("Reşid", "İki kadının da kocası olan şiddete yatkın adam")
        ],
        "temalar": ["Kadın dayanışması", "Savaş ve şiddet", "Umut ve direnç"],
        "alintilar": [
            "İnsan dayanılmaz dediği şeylere de dayanır sonunda.",
            "Kişi bir tek şeyi düşleyebilir, bin muhteşem güneş düşleyebilir."
        ]
    },
    "Martin Eden - Jack London": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Yoksul denizci Martin Eden, zengin Ruth Morse'a âşık olarak entelektüel dünyaya adım atar. Kendi kendini eğiterek yazar olur, ancak başarıya ulaştığında toplumun ikiyüzlülüğünü ve aşkın yüzeyselliğini görür. Hayal kırıklığı onu nihilizme sürükler. London, sınıf atlama hayalinin ve bireysel mücadelenin trajedisini kendi yaşamından esinlenerek anlatır.",
        "karakterler": [
            ("Martin Eden", "Kendi kendini yetiştiren denizci-yazar"),
            ("Ruth Morse", "Martin'in aşık olduğu burjuva kızı"),
            ("Russ Brissenden", "Martin'in sosyalist şair arkadaşı")
        ],
        "temalar": ["Sınıf atlama", "Sanat ve toplum", "Hayal kırıklığı"],
        "alintilar": [
            "Hayat güzeldir ama insanlar onu çirkinleştirir.",
            "Başarı geldiğinde artık onun bir anlamı kalmamıştı."
        ]
    },

    # ========================== ALMAN EDEBIYATI (15) ==========================

    "Dönüşüm - Franz Kafka": {
        "kategori": "Alman Edebiyati",
        "ozet": "Gezici satıcı Gregor Samsa bir sabah dev bir böceğe dönüşmüş olarak uyanır. Ailesi başlangıçta ona bakar ancak zamanla yük olarak görmeye başlar ve Gregor yalnızlık içinde ölür. Kafka, modern insanın yabancılaşmasını, aile içi ilişkilerin kırılganlığını ve bireyin toplum tarafından dışlanmasını alegorik bir dille anlatır.",
        "karakterler": [
            ("Gregor Samsa", "Böceğe dönüşen, ailesini geçindiren gezici satıcı"),
            ("Grete Samsa", "Gregor'un başlangıçta bakan ama sonra reddeden kız kardeşi"),
            ("Baba Samsa", "Oğlunun dönüşümüyle utanç duyan sert baba")
        ],
        "temalar": ["Yabancılaşma", "Aile ve reddedilme", "Kimlik kaybı"],
        "alintilar": [
            "Gregor Samsa bir sabah huzursuz düşlerden uyandığında, kendini yatağında dev bir böceğe dönüşmüş olarak buldu.",
            "Onu böcek olarak görmek yetmez miydi?"
        ]
    },
    "Dava - Franz Kafka": {
        "kategori": "Alman Edebiyati",
        "ozet": "Banka memuru Josef K., bir sabah suçunu bile bilmeden tutuklanır. Mahkeme sisteminin labirentinde kendi davasını anlamaya çalışır ama bürokrasinin absürt işleyişi karşısında çaresiz kalır. Sonunda hiçbir şey anlamadan idam edilir. Kafka, modern bürokrasinin bireyi ezmesini kabus gibi bir atmosferde anlatır.",
        "karakterler": [
            ("Josef K.", "Suçunu bilmeden yargılanan banka memuru"),
            ("Avukat Huld", "Etkisiz ve manipülatif savunma avukatı"),
            ("Rahip", "Josef K.'ya 'Yasa Önünde' alegorisini anlatan kilise rahibi")
        ],
        "temalar": ["Bürokrasi ve absürdlük", "Suç ve suçluluk", "Bireyin çaresizliği"],
        "alintilar": [
            "Birisi Josef K.'ya iftira atmış olmalıydı, çünkü kötü bir şey yapmamış olmasına rağmen bir sabah tutuklandı.",
            "Yasa önünde bir kapıcı durur."
        ]
    },
    "Şato - Franz Kafka": {
        "kategori": "Alman Edebiyati",
        "ozet": "Arazi ölçümcüsü K., Şato tarafından çağrıldığını iddia ederek köye gelir ancak Şato yetkilileriyle asla iletişim kuramaz. Bürokrasinin sonsuz döngüsünde kabul edilmeyi beklerken köy halkı tarafından yabancı muamelesi görür. Kafka'nın tamamlanmamış bu romanı, ulaşılamaz otoritenin ve yabancılığın en güçlü ifadesidir.",
        "karakterler": [
            ("K.", "Şato'ya ulaşmaya çalışan gizemli arazi ölçümcüsü"),
            ("Frieda", "K.'nın sevgilisi olan bar kadını"),
            ("Klamm", "Hiç görünmeyen gizemli Şato yetkilisi")
        ],
        "temalar": ["Bürokrasi ve ulaşılmazlık", "Yabancılık", "Güç ve otorite"],
        "alintilar": [
            "Şato'dan hiçbir zaman kesin bir cevap gelmez.",
            "Bir yabancı olarak burada kalmaya devam edemezsiniz."
        ]
    },
    "Faust - Johann Wolfgang von Goethe": {
        "kategori": "Alman Edebiyati",
        "ozet": "Bilgin Faust, yaşamın anlamını bulamayarak şeytan Mephisto ile bir anlaşma yapar: Mephisto ona dünyevi zevkleri tattıracak, Faust bir an 'Dur, ne güzelsin!' dediğinde ruhunu kaybedecektir. Gretchen trajedisi, iktidar hırsı ve bilgelik arayışı iç içe geçer. Goethe'nin başyapıtı, insanın sınırsız bilgi ve deneyim açlığını evrensel bir boyutta işler.",
        "karakterler": [
            ("Faust", "Bilgi ve deneyim için ruhunu satan bilgin"),
            ("Mephisto", "Kurnaz, alaycı ve karizmatik şeytan"),
            ("Gretchen", "Faust'un aşık olduğu masum genç kız")
        ],
        "temalar": ["Bilgi ve güç hırsı", "İyilik ve kötülük", "Aşk ve trajedi"],
        "alintilar": [
            "Dur, ne güzelsin!",
            "Her şeyi bilmek istiyorum ama hiçbir şey bilmiyorum."
        ]
    },
    "Genç Werther'in Acıları - Johann Wolfgang von Goethe": {
        "kategori": "Alman Edebiyati",
        "ozet": "Genç sanatçı Werther, nişanlı olan Charlotte'a karşılıksız bir aşk besler. Aşkının umutsuzluğu ve dünyayla uyumsuzluğu onu giderek derin bir bunalıma sürükler ve sonunda intihar eder. Goethe'nin mektup romanı, Romantizm akımının başlangıç eserlerinden biri olarak kabul edilir ve yayımlandığında büyük yankı uyandırmıştır.",
        "karakterler": [
            ("Werther", "Aşkın ve hayatın acısına dayanamayan genç sanatçı"),
            ("Charlotte (Lotte)", "Werther'in âşık olduğu nişanlı genç kadın"),
            ("Albert", "Charlotte'un nişanlısı ve kocası")
        ],
        "temalar": ["Karşılıksız aşk", "Romantik bunalım", "Bireysel özgürlük"],
        "alintilar": [
            "Ah, insanoğlu kendi üzerine şikâyet edebilir mi?",
            "Doğa, sonsuz bir güzellik kaynağıdır."
        ]
    },
    "Bozkırkurdu - Hermann Hesse": {
        "kategori": "Alman Edebiyati",
        "ozet": "Orta yaşlı entelektüel Harry Haller, kendini yarı insan yarı kurt olarak görür; medeniyetle içgüdüleri arasında parçalanır. Hermine adlı gizemli bir kadınla tanışması onu yeni deneyimlere açar. Sihirli Tiyatro'da kendi benliğinin çok katmanlı doğasını keşfeder. Hesse, bireyin iç çatışmasını ve bütünleşme arayışını sürrealist bir anlatımla işler.",
        "karakterler": [
            ("Harry Haller", "Kendini toplumdan kopuk hisseden yalnız entelektüel"),
            ("Hermine", "Harry'yi hayata bağlayan gizemli kadın"),
            ("Pablo", "Müzisyen ve Sihirli Tiyatro'nun rehberi")
        ],
        "temalar": ["İç çatışma ve bütünleşme", "Yalnızlık", "Sanat ve yaşam"],
        "alintilar": [
            "Deli olmayanlar için deli olmak zordur.",
            "Her insanın hikâyesi önemlidir, sonsuzdur, Tanrı'nındır."
        ]
    },
    "Siddhartha - Hermann Hesse": {
        "kategori": "Alman Edebiyati",
        "ozet": "Brahman oğlu Siddhartha, ruhsal aydınlanma arayışıyla evinden ayrılır. Çileci yaşamı, dünyevi zevkleri ve ticaret hayatını deneyimledikten sonra bir nehir kenarında kayıkçı olarak huzuru bulur. Hesse, Doğu felsefesinden esinlenerek bireyin kendi yolunu bulma sürecini ve bilgeliğin öğretilmeyip yaşanarak kazanıldığını anlatır.",
        "karakterler": [
            ("Siddhartha", "Aydınlanma arayan Brahman genci"),
            ("Govinda", "Siddhartha'nın sadık arkadaşı"),
            ("Vasudeva", "Nehirden bilgelik öğrenen kayıkçı")
        ],
        "temalar": ["Aydınlanma arayışı", "Deneyim yoluyla öğrenme", "Zamanın döngüselliği"],
        "alintilar": [
            "Nehir her şeyi bilir; nehirden her şey öğrenilebilir.",
            "Bilgelik başkasına aktarılamaz. Bilge bir insanın aktarmaya çalıştığı bilgelik, her zaman budalalık gibi görünür."
        ]
    },
    "Batı Cephesinde Yeni Bir Şey Yok - Erich Maria Remarque": {
        "kategori": "Alman Edebiyati",
        "ozet": "Genç Alman askeri Paul Bäumer, Birinci Dünya Savaşı'nın cephesinde arkadaşlarıyla birlikte hayatta kalmaya çalışır. Savaşın dehşeti, arkadaş kayıpları ve topluma yabancılaşma Paul'ü derinden yaralar. Savaşın bitişine yakın öldürüldüğünde rapor yalnızca 'Batı cephesinde yeni bir şey yok' der. Remarque, savaşın anlamsızlığını kayıp neslin ağzından haykırır.",
        "karakterler": [
            ("Paul Bäumer", "Cephede hayatta kalmaya çalışan genç Alman askeri"),
            ("Kat (Stanislaus Katczinsky)", "Deneyimli ve koruyucu asker, Paul'ün yakın arkadaşı"),
            ("Kantorek", "Öğrencileri savaşa teşvik eden idealist öğretmen")
        ],
        "temalar": ["Savaşın anlamsızlığı", "Kayıp nesil", "Yabancılaşma"],
        "alintilar": [
            "Batı cephesinde yeni bir şey yok.",
            "Biz genç yaşta hayattan koptuk; yirmi yaşında yaşlılardan daha yaşlıyız."
        ]
    },
    "Buddenbrook Ailesi - Thomas Mann": {
        "kategori": "Alman Edebiyati",
        "ozet": "Lübeck'teki zengin tüccar Buddenbrook ailesinin dört kuşak boyunca çöküşünü anlatan roman, maddi refahla birlikte gelen manevi çürümeyi izler. Her nesilde iş zekâsı azalırken sanatsal duyarlılık artar. Mann, burjuva değerlerinin erimesini ve ailenin kaçınılmaz çöküşünü toplumsal bir panorama içinde sunar.",
        "karakterler": [
            ("Thomas Buddenbrook", "Aile geleneğini sürdürmeye çalışan ama içten çöken iş adamı"),
            ("Hanno Buddenbrook", "Müziğe tutkun, hastalıklı son kuşak"),
            ("Tony Buddenbrook", "Ailenin onurunu korumaya çalışan enerjik kadın")
        ],
        "temalar": ["Ailenin çöküşü", "Burjuva değerleri", "Sanat ve ticaret çatışması"],
        "alintilar": [
            "Mutlu insanların tarihi yoktur.",
            "Çalışmak, topluma yararlı olmak... bunlar mutlu etmiyor insanı."
        ]
    },
    "Koku - Patrick Süskind": {
        "kategori": "Alman Edebiyati",
        "ozet": "18. yüzyıl Paris'inde doğan Jean-Baptiste Grenouille, olağanüstü bir koku alma yeteneğine sahiptir ancak kendi bedeni hiçbir koku taşımaz. Mükemmel parfümü yaratmak uğruna genç kızları öldürür. Süskind, dahi ve canavar arasındaki ince çizgiyi, koku duyusunun büyülü dünyasında gerilim dolu bir şekilde anlatır.",
        "karakterler": [
            ("Grenouille", "Üstün koku alma yeteneğine sahip seri katil parfümcü"),
            ("Baldini", "Grenouille'ın parfümcülük öğrendiği yaşlı usta"),
            ("Richis", "Kızını korumaya çalışan zeki tüccar")
        ],
        "temalar": ["Deha ve delilik", "Kimlik ve varoluş", "Sanat ve cinayet"],
        "alintilar": [
            "Kokuları olan her şey var olur, kokusuz olan hiçbir şey.",
            "İnsanları yöneten güç güzellik değil, kokudur."
        ]
    },
    "Okuyucu - Bernhard Schlink": {
        "kategori": "Alman Edebiyati",
        "ozet": "On beş yaşındaki Michael, otuz altı yaşındaki Hanna ile bir yaz aşkı yaşar. Hanna ona kitap okumasını ister ve gizemli bir şekilde kaybolur. Yıllar sonra hukuk öğrencisi Michael, Hanna'yı Nazi savaş suçlusu olarak mahkemede görünce geçmişiyle yüzleşmek zorunda kalır. Schlink, suçluluk, sorumluluk ve nesiller arası hesaplaşmayı etkileyici bir şekilde işler.",
        "karakterler": [
            ("Michael Berg", "Hanna ile ilişkisi yüzünden hayat boyu etkilenen genç adam"),
            ("Hanna Schmitz", "Okuma yazma bilmeyen eski SS gardiyanı"),
            ("Profesör", "Michael'ın hukuk profesörü")
        ],
        "temalar": ["Suçluluk ve sorumluluk", "Nesiller arası hesaplaşma", "Aşk ve utanç"],
        "alintilar": [
            "Yaşadıklarımız hakkında konuşamıyorsak, yazabiliriz.",
            "Anlayış, affetme anlamına gelmiyor."
        ]
    },
    "Bitmeyecek Öykü - Michael Ende": {
        "kategori": "Alman Edebiyati",
        "ozet": "Yalnız çocuk Bastian, bir kitapçıdan çaldığı kitabı okurken kendini Fantasya ülkesinde bulur. Hiçlik tehdidi altındaki bu hayal dünyasını kurtarmak için gerçeklikle hayal arasında yolculuk yapar. Ende, çocukluk hayallerinin gücünü, okuma sevgisini ve cesaretin önemini fantastik bir macera içinde anlatır.",
        "karakterler": [
            ("Bastian", "Kitap okuyarak Fantasya'yı kurtaran çekingen çocuk"),
            ("Atreyu", "Fantasya'yı kurtarmakla görevlendirilen genç savaşçı"),
            ("Çocuksu İmparatoriçe", "Fantasya'nın gizemli yöneticisi")
        ],
        "temalar": ["Hayal gücünün önemi", "Cesaret ve büyüme", "Gerçeklik ve fantezi"],
        "alintilar": [
            "Her gerçek hikâyenin sonu yoktur.",
            "Fantasya'yı yalnızca isimler kurtarabilir."
        ]
    },
    "Uçan Sınıf - Erich Kästner": {
        "kategori": "Alman Edebiyati",
        "ozet": "Bir yatılı okulda okuyan beş erkek çocuğun dostluğu, Noel öncesi yaşanan maceralarla sınanır. Cesaret, arkadaşlık ve adaleti öğrenirken aynı zamanda hayatın acı taraflarıyla da tanışırlar. Kästner, çocuk edebiyatının klasiklerinden birini yazarken yetişkinlerin dünyasına da eleştirel bir bakış atar.",
        "karakterler": [
            ("Martin", "Yoksul ama onurlu ve cesur öğrenci"),
            ("Johnny", "Ebeveynleri tarafından terk edilmiş hassas çocuk"),
            ("Justus", "Öğrencilerin sevdiği adil öğretmen")
        ],
        "temalar": ["Dostluk ve sadakat", "Cesaret", "Çocukluk ve büyüme"],
        "alintilar": [
            "Cesur olmak, korkmamak değil; korkuya rağmen doğru olanı yapmaktır.",
            "Utanılacak şey yoksulluk değil, haksızlıktır."
        ]
    },
    "Teneke Trampet - Günter Grass": {
        "kategori": "Alman Edebiyati",
        "ozet": "Oskar Matzerath, üç yaşında büyümeyi reddederek dünyayı çocuk gözüyle izlemeye karar verir. Teneke trampetini çalarak ve camları çığlığıyla kırarak yetişkinlerin dünyasına isyan eder. Grass, Nazi Almanya'sının yükselişi ve çöküşünü Danzig'de geçen bu absürt hikâye üzerinden hicveder.",
        "karakterler": [
            ("Oskar Matzerath", "Büyümeyi reddeden, teneke trampetli çocuk-adam"),
            ("Agnes Matzerath", "Oskar'ın günahkâr ama sevecen annesi"),
            ("Alfred Matzerath", "Oskar'ın yasal babası, Nazi Partisi üyesi")
        ],
        "temalar": ["Savaş ve suçluluk", "İsyan ve reddediş", "Tarih ve birey"],
        "alintilar": [
            "Her şeyi baştan anlatmaya karar verdim.",
            "Üç yaşımda büyümeyi bıraktım."
        ]
    },
    "Venedik'te Ölüm - Thomas Mann": {
        "kategori": "Alman Edebiyati",
        "ozet": "Yaşlanan yazar Gustav von Aschenbach, Venedik'te tatildeyken Polonyalı genç Tadzio'ya estetik bir hayranlık duyar. Bu tutku onu kolera salgınına rağmen şehirden ayrılmaktan alıkoyar ve sonunda ölümüne yol açar. Mann, güzelliğe tapınmanın yıkıcılığını ve sanatçının ahlaki çöküşünü yoğun bir atmosferde anlatır.",
        "karakterler": [
            ("Gustav von Aschenbach", "Disiplinli ama sonunda tutkusuna yenilen yaşlı yazar"),
            ("Tadzio", "Aschenbach'ın hayran olduğu güzel Polonyalı genç"),
            ("Aschenbach'ın iç sesi", "Apolloncu düzen ile Dionysosçu tutku arasındaki çatışma")
        ],
        "temalar": ["Güzellik ve yıkım", "Sanat ve ahlak", "Ölüm ve tutku"],
        "alintilar": [
            "Güzellik, duyuların bilgeliğe giden tek yoludur.",
            "Tutku, bilgeliğin yıkımıdır."
        ]
    },

    # ========================== TÜRK EDEBİYATI (35) ==========================

    "Kürk Mantolu Madonna - Sabahattin Ali": {
        "kategori": "Turk Edebiyati",
        "ozet": "Raif Efendi, Berlin'de tanıştığı ressam Maria Puder'e derin bir aşk besler ancak çekingenliği ilişkiyi yaşamasına engel olur. Yıllar sonra Ankara'da sıradan bir memur olarak mutsuz bir hayat sürerken geçmişini bir deftere yazar. Sabahattin Ali, karşılıksız aşkın ve cesaretsizliğin trajik sonuçlarını iki kültürün kesişiminde anlatır.",
        "karakterler": [
            ("Raif Efendi", "İçine kapanık, duyarlı ve cesaretsiz memur"),
            ("Maria Puder", "Bağımsız, güçlü iradeli Alman ressam kadın"),
            ("Anlatıcı", "Raif Efendi'nin defterini bulan ve okuyan genç adam")
        ],
        "temalar": ["Karşılıksız aşk", "Cesaretsizlik ve pişmanlık", "Doğu-Batı çatışması"],
        "alintilar": [
            "İnsanlar başkalarının acılarına bu kadar kayıtsız olmasalardı, dünya çok daha güzel olurdu.",
            "Hayatta en büyük talihsizlik, insan olduğunun farkına varmaktır."
        ]
    },
    "İçimizdeki Şeytan - Sabahattin Ali": {
        "kategori": "Turk Edebiyati",
        "ozet": "Genç yazar Ömer, yakışıklı ve karizmatik Macide'ye âşık olur. Evlenirler ancak Ömer'in kararsızlığı, sorumsuzluğu ve kötü arkadaşlıkları evliliği yıkar. Roman, bireyin içindeki yıkıcı dürtüleri ve toplumsal baskıları İstanbul'un 1940'lar atmosferinde işler.",
        "karakterler": [
            ("Ömer", "Yetenekli ama sorumsuz ve kararsız genç yazar"),
            ("Macide", "Sabırlı, fedakâr ve sonunda güçlenen genç kadın"),
            ("Nihat", "Ömer'i kötü yola sürükleyen olumsuz arkadaş")
        ],
        "temalar": ["İç çatışma", "Ahlaki çöküş", "Toplumsal baskı"],
        "alintilar": [
            "Her insanın içinde bir şeytan vardır; mesele onunla nasıl başa çıktığındır.",
            "Günahkâr olmak istemiyordum ama günah benden güçlüydü."
        ]
    },
    "Çalıkuşu - Reşat Nuri Güntekin": {
        "kategori": "Turk Edebiyati",
        "ozet": "Feride, nişanlısı Kâmran'ın ihanetini öğrenince İstanbul'u terk ederek Anadolu'nun uzak köylerinde öğretmenlik yapar. Zorlu koşullara rağmen idealizmiyle mücadele eder ve halkın sevgisini kazanır. Yıllar sonra Kâmran'la yeniden karşılaşır. Güntekin, Cumhuriyet döneminin idealizmini ve Anadolu gerçeğini Feride'nin güçlü kişiliğiyle anlatır.",
        "karakterler": [
            ("Feride (Çalıkuşu)", "İdealist, cesur ve bağımsız genç öğretmen"),
            ("Kâmran", "Feride'yi önce kıran sonra pişman olan kuzen"),
            ("Doktor Hayrullah", "Feride'ye destek olan bilge doktor")
        ],
        "temalar": ["İdealizm ve fedakârlık", "Anadolu gerçeği", "Aşk ve onur"],
        "alintilar": [
            "Ben bir çalıkuşuyum; ne kafese konulabilirim ne de zincire bağlanabilirim.",
            "İnsan sevdiği için değil, seven olduğu için sever."
        ]
    },
    "Yaprak Dökümü - Reşat Nuri Güntekin": {
        "kategori": "Turk Edebiyati",
        "ozet": "Ali Rıza Bey, geleneksel değerlere bağlı dürüst bir devlet memurudur. İstanbul'a taşınmasıyla ailesi hızla yozlaşır: eşi ve kızları lüks yaşam peşinde koşarken aile çöker. Güntekin, Batılılaşmanın yanlış anlaşılmasını ve aile değerlerinin erozyonunu bir babanın trajedisi üzerinden anlatır.",
        "karakterler": [
            ("Ali Rıza Bey", "Dürüst, geleneksel değerlere bağlı baba"),
            ("Hayriye Hanım", "Kocasının değerlerinden uzaklaşan eş"),
            ("Leyla", "Lüks yaşam peşinde koşan büyük kız")
        ],
        "temalar": ["Aile çöküşü", "Yanlış Batılılaşma", "Baba figürünün trajedisi"],
        "alintilar": [
            "Yapraklar dökülür, ağaç kalır; ama ağacın da ömrü vardır.",
            "Bir baba evladından ne bekler? Biraz sevgi, biraz saygı."
        ]
    },
    "Aşk-ı Memnu - Halit Ziya Uşaklıgil": {
        "kategori": "Turk Edebiyati",
        "ozet": "Zengin Adnan Bey'in genç eşi Bihter, üvey oğlu Behlül ile yasak bir ilişkiye başlar. Adnan Bey'in kızı Nihal ise Behlül'e âşıktır. Sırların ortaya çıkmasıyla Bihter intihar eder. Uşaklıgil, Osmanlı üst sınıfının çürümüşlüğünü psikolojik derinlikle işleyerek Türk edebiyatının ilk modern romanlarından birini yazar.",
        "karakterler": [
            ("Bihter", "Yasak aşkın kurbanı olan güzel ve tutkulu genç kadın"),
            ("Behlül", "Sorumsuz, yakışıklı ve bencil genç adam"),
            ("Nihal", "Behlül'e âşık olan masum üvey kız kardeş")
        ],
        "temalar": ["Yasak aşk", "Toplumsal çürüme", "Kadının trajedisi"],
        "alintilar": [
            "Aşk bazen insanı yaşatır, bazen de öldürür.",
            "Yasak olan her şey daha çekici görünür."
        ]
    },
    "Mai ve Siyah - Halit Ziya Uşaklıgil": {
        "kategori": "Turk Edebiyati",
        "ozet": "Genç şair Ahmet Cemil, büyük bir edebi eser yazarak ün kazanma hayali kurar. Kız kardeşinin mutsuz evliliği, yakın arkadaşının ihaneti ve eserinin başarısızlığı onu hayal kırıklığına uğratır. Uşaklıgil, sanatçının toplumla çatışmasını ve hayallerin gerçeklikle yüzleşmesini işler.",
        "karakterler": [
            ("Ahmet Cemil", "Büyük hayaller kuran ama hayal kırıklığına uğrayan genç şair"),
            ("Hüseyin Nazmi", "Ahmet Cemil'in sadık arkadaşı"),
            ("İkbal", "Ahmet Cemil'in mutsuz evlilik yapan kız kardeşi")
        ],
        "temalar": ["Hayal ve gerçeklik", "Sanatçının yalnızlığı", "Hayal kırıklığı"],
        "alintilar": [
            "Hayaller mavi, gerçekler siyahtır.",
            "Yalnızlık, sanatçının en yakın dostu ve en büyük düşmanıdır."
        ]
    },
    "İnce Memed - Yaşar Kemal": {
        "kategori": "Turk Edebiyati",
        "ozet": "Çukurova'nın dağ köylerinde yaşayan İnce Memed, zalim ağa Abdi'nin baskısından kaçarak eşkıya olur. Sevdiği kız Hatçe'yi kurtarmak ve köylüleri ağanın zulmünden kurtarmak için mücadele eder. Yaşar Kemal, Anadolu insanının direniş ruhunu destansı bir dille anlatarak dünya edebiyatında yerini alır.",
        "karakterler": [
            ("İnce Memed", "Zulme karşı dağa çıkan cesur köylü delikanlı"),
            ("Hatçe", "Memed'in sevdiği ve ağanın zulmüne maruz kalan kız"),
            ("Abdi Ağa", "Köylüyü ezen, acımasız toprak ağası")
        ],
        "temalar": ["Zulme karşı direnç", "Adalet arayışı", "Toprak ve emek"],
        "alintilar": [
            "İnsan zulme ne kadar dayanır?",
            "Ağalar var oldukça bu dağlar eşkıyasız kalmaz."
        ]
    },
    "Tutunamayanlar - Oğuz Atay": {
        "kategori": "Turk Edebiyati",
        "ozet": "Selim Işık'ın intiharından sonra arkadaşı Turgut Özben, onun hayatını ve düşüncelerini anlamaya çalışır. Bu arayış Turgut'u da topluma tutunamayan bir aydın olarak kendi bunalımıyla yüzleştirir. Atay, Türk entelektüelinin yabancılaşmasını postmodern anlatım teknikleriyle ve kara mizahla işleyerek Türk edebiyatında çığır açar.",
        "karakterler": [
            ("Turgut Özben", "Arkadaşının ölümüyle sarsılan ve sorgulamaya başlayan aydın"),
            ("Selim Işık", "Topluma tutunamayan ve intihar eden hassas entelektüel"),
            ("Olric", "Selim'in yarattığı alter ego karakter")
        ],
        "temalar": ["Aydın yabancılaşması", "Topluma tutunamama", "Kimlik arayışı"],
        "alintilar": [
            "Yaşamak bir alışkanlıktır, ölmek de.",
            "Herkes gibi olabilmek için çok uğraştım."
        ]
    },
    "Tehlikeli Oyunlar - Oğuz Atay": {
        "kategori": "Turk Edebiyati",
        "ozet": "Hikmet Benol, toplumsal normlardan sıyrılmaya çalışan bir entelektüeldir. Gerçeklik ve kurgu arasında gidip gelerek kendi hayatını bir oyun gibi yaşar. Atay, Türk aydınının bunalımını bu kez daha deneysel ve parçalı bir anlatımla işler.",
        "karakterler": [
            ("Hikmet Benol", "Toplumla uyumsuz, kendini arayan entelektüel"),
            ("Sevgi", "Hikmet'in ilişki yaşadığı kadın"),
            ("Bilge", "Hikmet'in hayatındaki bir diğer kadın")
        ],
        "temalar": ["Entelektüel bunalım", "Gerçeklik ve kurgu", "Yabancılaşma"],
        "alintilar": [
            "Oyun oynamaktan başka çaremiz var mı?",
            "Tehlikeli olan oyun değil, oyunu ciddiye almaktır."
        ]
    },
    "Huzur - Ahmet Hamdi Tanpınar": {
        "kategori": "Turk Edebiyati",
        "ozet": "Mümtaz, İstanbul'un güzelliğine ve tarihine derinden bağlı bir entelektüeldir. Nuran ile yaşadığı aşk, İstanbul'un eski medeniyetlerinin izleriyle iç içe geçer. İkinci Dünya Savaşı'nın yaklaşması ve kişisel krizler bu huzuru tehdit eder. Tanpınar, Doğu-Batı sentezini, zamanın akışını ve güzellik arayışını İstanbul'un ruhunda birleştirir.",
        "karakterler": [
            ("Mümtaz", "İstanbul âşığı, müzik ve edebiyatla dolu entelektüel"),
            ("Nuran", "Mümtaz'ın büyük aşkı, zarif ve kültürlü kadın"),
            ("İhsan", "Mümtaz'ın manevi babası olan bilge hoca")
        ],
        "temalar": ["Doğu-Batı sentezi", "Zaman ve güzellik", "Aşk ve huzur arayışı"],
        "alintilar": [
            "İstanbul'u sevmek, bir medeniyet sevgisidir.",
            "İnsan her şeyin dışında kaldığı zaman gerçek yüzüyle karşılaşır."
        ]
    },
    "Saatleri Ayarlama Enstitüsü - Ahmet Hamdi Tanpınar": {
        "kategori": "Turk Edebiyati",
        "ozet": "Hayri İrdal, Osmanlı'dan Cumhuriyet'e geçiş döneminde yaşayan sıradan bir adamdır. Halit Ayarcı ile birlikte saatleri ayarlama enstitüsü kurar. Roman, modernleşme sürecini, bürokratik absürdlüğü ve kimlik bunalımını ince bir ironiyle hicveder. Tanpınar'ın en eğlenceli ve en derin eseridir.",
        "karakterler": [
            ("Hayri İrdal", "Sıradan, uysal ve sisteme sürüklenen anlatıcı"),
            ("Halit Ayarcı", "Karizmatik, vizyoner ama düzenbaz girişimci"),
            ("Nuri Efendi", "Hayri'nin saatçilik öğrendiği eski zaman ustası")
        ],
        "temalar": ["Modernleşme hicvi", "Kimlik bunalımı", "Bürokrasi ve absürdlük"],
        "alintilar": [
            "Her şeyden önce saatlerimizi ayarlamamız lazım.",
            "İnsan saatine göre yaşar; ama saati kime göre ayarlar?"
        ]
    },
    "Benim Adım Kırmızı - Orhan Pamuk": {
        "kategori": "Turk Edebiyati",
        "ozet": "16. yüzyıl Osmanlı İstanbul'unda minyatürcüler arasında işlenen bir cinayet, Doğu ve Batı sanat anlayışları arasındaki çatışmayı ortaya çıkarır. Kara, eski aşkı Şeküre'ye kavuşmaya çalışırken katili bulmaya da çabalar. Pamuk, perspektif, kimlik ve sanatın doğası üzerine çok sesli bir anlatım kurar.",
        "karakterler": [
            ("Kara", "Cinayet soruşturmasını yürüten ve Şeküre'ye âşık olan genç"),
            ("Şeküre", "Güzel, zeki ve stratejik davranan kadın"),
            ("Enişte Efendi", "Padişahın gizli kitap projesini yöneten nakkaş")
        ],
        "temalar": ["Doğu-Batı sanat çatışması", "Kimlik ve üslup", "Aşk ve cinayet"],
        "alintilar": [
            "Körlük bir renktir.",
            "Resim yapmak, Allah'ın gördüğü gibi görmeye çalışmaktır."
        ]
    },
    "Kar - Orhan Pamuk": {
        "kategori": "Turk Edebiyati",
        "ozet": "Şair Ka, Kars'a gazeteci olarak gider ama şehri kar fırtınası yüzünden dış dünyadan kesilmiş bulur. Türban meselesi, askeri darbe, İslamcılar ve laikler arasındaki gerilim Ka'nın şiir yazma süreciyle iç içe geçer. Pamuk, Türkiye'nin siyasi ve kültürel çelişkilerini kar yağışının büyüsü altında yoğun bir atmosferde anlatır.",
        "karakterler": [
            ("Ka", "Frankfurt'tan Kars'a gelen hassas ve yalnız şair"),
            ("İpek", "Ka'nın âşık olduğu güzel ve gizemli kadın"),
            ("Lacivert", "Karizmatik İslamcı genç lider")
        ],
        "temalar": ["Doğu-Batı gerilimi", "Din ve laiklik", "Yalnızlık ve şiir"],
        "alintilar": [
            "Kar, Allah'ın insanlara eşit davrandığının ispatıdır.",
            "Mutsuzluk, mutlu olmadığını fark etmekle başlar."
        ]
    },
    "Aşk - Elif Şafak": {
        "kategori": "Turk Edebiyati",
        "ozet": "İki paralel hikâye anlatılır: günümüzde Boston'da yaşayan Ella Rubinstein'in hayatı ve 13. yüzyılda Mevlana ile Şems-i Tebrizi'nin dostluğu. Ella, Şems'in aşk kurallarını okudukça kendi hayatını sorgulamaya başlar. Şafak, tasavvuf felsefesini ve ilahi aşkı modern dünyayla buluşturur.",
        "karakterler": [
            ("Ella Rubinstein", "Sıradan hayatından sıkılan Amerikalı ev kadını"),
            ("Şems-i Tebrizi", "Mevlana'yı dönüştüren gezgin derviş"),
            ("Mevlana Celaleddin Rumi", "Şems'in etkisiyle şaire dönüşen büyük mutasavvıf")
        ],
        "temalar": ["İlahi aşk", "Tasavvuf ve dönüşüm", "Geleneksel ve modern kadın"],
        "alintilar": [
            "Aşkın kırk kuralı vardır.",
            "Evrende ne ararsan kendinde ara."
        ]
    },
    "Dokuzuncu Hariciye Koğuşu - Peyami Safa": {
        "kategori": "Turk Edebiyati",
        "ozet": "Diz hastalığı yüzünden hastanede yatan genç anlatıcı, güzel ve modern Nüzhet ile geleneksel Seniha arasında kalır. Hastalığı ve yoksulluğuyla mücadele ederken aşk acısı da çeker. Peyami Safa, Doğu-Batı ikilemine düşen bir gencin iç dünyasını otobiyografik öğelerle anlatır.",
        "karakterler": [
            ("Anlatıcı", "Hasta, yoksul ve ikiye bölünmüş genç adam"),
            ("Nüzhet", "Modern, alafrangalı ve çekici genç kadın"),
            ("Seniha", "Geleneksel değerlere bağlı, içten kadın")
        ],
        "temalar": ["Doğu-Batı ikilemi", "Hastalık ve yoksulluk", "Aşk üçgeni"],
        "alintilar": [
            "Hastanede insan her şeyi daha derin hisseder.",
            "Bir insanı sevmek, onu olduğu gibi kabul etmektir."
        ]
    },
    "Fatih-Harbiye - Peyami Safa": {
        "kategori": "Turk Edebiyati",
        "ozet": "Genç kız Neriman, Fatih'teki geleneksel mahallesindeki hayatla Beyoğlu'ndaki modern yaşam arasında bocalamaktadır. Geleneksel Şinasi ile modern Macit arasında kalan Neriman, sonunda kendi değerlerini tanır. Peyami Safa, Doğu-Batı sentezini İstanbul'un iki yakası üzerinden sembolize eder.",
        "karakterler": [
            ("Neriman", "İki dünya arasında bocalayan genç kız"),
            ("Şinasi", "Geleneksel değerleri temsil eden nişanlı"),
            ("Macit", "Batılı yaşam tarzını temsil eden modern genç")
        ],
        "temalar": ["Doğu-Batı çatışması", "Kimlik arayışı", "Geleneksel ve modern"],
        "alintilar": [
            "Fatih'ten Harbiye'ye gitmek, bir medeniyetten diğerine geçmektir.",
            "İnsan kendi olduğu yerde huzur bulur."
        ]
    },
    "Sinekli Bakkal - Halide Edib Adıvar": {
        "kategori": "Turk Edebiyati",
        "ozet": "Abdülhamid döneminde Sinekli Bakkal mahallesinde geçen roman, imam kızı Rabia'nın müzik ve aşk arasında sıkışmasını anlatır. Batılılaşma çabaları, istibdat rejimi ve halk hayatı iç içe geçer. Halide Edib, Türk toplumunun modernleşme sancılarını mahalle kültürü üzerinden renkli bir dille anlatır.",
        "karakterler": [
            ("Rabia", "Geleneksel ortamda büyüyen ama müziğe tutkun genç kız"),
            ("Peregrini", "İtalyan piyanist ve Rabia'nın müzik öğretmeni"),
            ("Tevfik", "Rabia'yı seven genç imam")
        ],
        "temalar": ["Gelenek ve modernlik", "Kadının yeri", "Müzik ve sanat"],
        "alintilar": [
            "Müzik, insan ruhunun en derin ifadesidir.",
            "Mahalle, bir milletin küçük aynasıdır."
        ]
    },
    "Ateşten Gömlek - Halide Edib Adıvar": {
        "kategori": "Turk Edebiyati",
        "ozet": "Kurtuluş Savaşı sırasında İstanbul'dan Anadolu'ya geçen Peyami, Ayşe ve İhsan'ın hikâyesi anlatılır. Peyami, hemşire Ayşe'ye âşıktır ama Ayşe İhsan'ı sever. Savaşın ateşi içinde aşk ve vatan sevgisi iç içe geçer. Halide Edib, Millî Mücadele'nin ruhunu bizzat yaşadığı deneyimlerle yansıtır.",
        "karakterler": [
            ("Peyami", "Anlatıcı; Ayşe'ye karşılıksız aşk besleyen genç"),
            ("Ayşe", "Fedakâr hemşire ve bağımsızlık savaşçısı"),
            ("İhsan", "Cephedeki kahraman subay")
        ],
        "temalar": ["Vatan sevgisi", "Fedakârlık", "Karşılıksız aşk"],
        "alintilar": [
            "Ateşten gömlek giymek, vatan için her şeyi göze almaktır.",
            "Bu topraklar kanla sulanmadan yeşermez."
        ]
    },
    "Yaban - Yakup Kadri Karaosmanoğlu": {
        "kategori": "Turk Edebiyati",
        "ozet": "Savaşta kolunu kaybeden subay Ahmet Celal, bir Anadolu köyüne yerleşir. Köylülerle arasında derin bir uçurum vardır; ne onları anlar ne de onlar tarafından kabul edilir. Millî Mücadele sırasında bile köylülerin kayıtsızlığı onu şaşırtır. Yakup Kadri, aydın-halk kopukluğunu acı bir dille anlatır.",
        "karakterler": [
            ("Ahmet Celal", "Köyde yabancı kalan yaralı subay-aydın"),
            ("Emine", "Ahmet Celal'in ilgi duyduğu genç köylü kadın"),
            ("Bekir Çavuş", "Köyün ileri gelenlerinden")
        ],
        "temalar": ["Aydın-halk kopukluğu", "Yabancılaşma", "Millî Mücadele"],
        "alintilar": [
            "Ben burada bir yabanım.",
            "Memleketi kurtarmak isteyenler, memleketi tanımıyor."
        ]
    },
    "Kiralık Konak - Yakup Kadri Karaosmanoğlu": {
        "kategori": "Turk Edebiyati",
        "ozet": "Osmanlı'nın son döneminde Naim Efendi'nin konağı, değişen toplumun simgesidir. Üç kuşak arasındaki kültürel uçurum, konağın çöküşüyle paralel ilerler. Yakup Kadri, Osmanlı ailesinin modernleşme sürecindeki çözülüşünü toplumsal bir panorama olarak sunar.",
        "karakterler": [
            ("Naim Efendi", "Eski değerlere bağlı, konak sahibi yaşlı bey"),
            ("Seniha", "Batılı yaşam tarzına özenen genç torun"),
            ("Hakkı Celis", "İdealist ve vatansever genç subay")
        ],
        "temalar": ["Nesil çatışması", "Osmanlı'nın çöküşü", "Batılılaşma"],
        "alintilar": [
            "Konak yıkılırken, bir medeniyet yıkılır.",
            "Eski dünya gidiyor, yeni dünya henüz kurulmuyor."
        ]
    },
    "Devlet Ana - Kemal Tahir": {
        "kategori": "Turk Edebiyati",
        "ozet": "Osmanlı Devleti'nin kuruluş dönemini anlatan roman, Söğüt'teki Türkmen aşiretlerinin devlet kurma sürecini destansı bir dille anlatır. Bacıbey, Osman Bey ve diğer karakterler üzerinden Türk devlet geleneğinin kökleri sorgulanır. Kemal Tahir, Türk tarihini Batılı kalıplardan farklı bir perspektifle yorumlar.",
        "karakterler": [
            ("Bacıbey", "Güçlü, bilge ve devlet kurucu kadın"),
            ("Osman Bey", "Osmanlı Devleti'nin kurucusu"),
            ("Kerim Çelebi", "Aydın ve sorgulayan genç")
        ],
        "temalar": ["Devlet kuruculuğu", "Türk tarih felsefesi", "Kadının rolü"],
        "alintilar": [
            "Devlet, ananın karnından doğar.",
            "Adalet olmadan devlet olmaz."
        ]
    },
    "Bereketli Topraklar Üzerinde - Orhan Kemal": {
        "kategori": "Turk Edebiyati",
        "ozet": "Üç köylü -Yusuf, İflahsızın Yusuf ve Pehlivan Ali- iş bulmak için Çukurova'ya inerler. Fabrikalarda ve tarlalarda insanlık dışı koşullarda çalıştırılır, sömürülür ve ezilirler. Orhan Kemal, göç eden köylülerin kent hayatındaki çaresizliğini ve emek sömürüsünü gerçekçi bir dille anlatır.",
        "karakterler": [
            ("Yusuf", "İyimser ama sömürülen saf köylü genç"),
            ("İflahsızın Yusuf", "Kurnaz ve hayatta kalmaya çalışan köylü"),
            ("Pehlivan Ali", "Güçlü ama saf kalpli köylü")
        ],
        "temalar": ["Emek sömürüsü", "Köyden kente göç", "Sınıf eşitsizliği"],
        "alintilar": [
            "Toprak bereketli ama insanlar aç.",
            "Alın teri kurumadan hakkını al diye öğrettiler bize."
        ]
    },
    "Memleketimden İnsan Manzaraları - Nâzım Hikmet": {
        "kategori": "Turk Edebiyati",
        "ozet": "Bir trende yolculuk eden farklı insanların hikâyelerinin anlatıldığı bu destansı manzum roman, Türkiye'nin toplumsal panoramasını çizer. İşçiler, köylüler, aydınlar ve sıradan insanların hayatları, umutları ve acıları bir arada sunulur. Nâzım Hikmet, Türk toplumunun kolektif portresini şiirsel bir anlatımla ortaya koyar.",
        "karakterler": [
            ("Halil", "Cepheden dönen yoksul köylü"),
            ("Fuat", "Zengin ve bencil iş adamı"),
            ("Galip", "İdealist genç öğretmen")
        ],
        "temalar": ["Toplumsal panorama", "Sınıf farklılıkları", "İnsan hikayeleri"],
        "alintilar": [
            "Memleket isterim, gök mavi, dal yeşil, tarla sarı olsun.",
            "Yaşamak bir ağaç gibi tek ve hür, bir orman gibi kardeşçesine."
        ]
    },
    "Bir Gün Tek Başına - Vedat Türkali": {
        "kategori": "Turk Edebiyati",
        "ozet": "1950'lerin İstanbul'unda devrimci genç İlhan'ın bir gününü anlatan roman, siyasi baskı altındaki solcu aydınların mücadelesini, sevgilerini ve çelişkilerini yoğun bir atmosferde işler. Türkali, bireyin siyasi idealleri ile kişisel hayatı arasındaki gerilimi tek bir gün içinde anlatır.",
        "karakterler": [
            ("İlhan", "Siyasi baskı altında yaşayan devrimci genç"),
            ("Reşit", "İlhan'ın yoldaşı"),
            ("Nermin", "İlhan'ın sevgilisi")
        ],
        "temalar": ["Siyasi mücadele", "Birey ve ideoloji", "Yalnızlık"],
        "alintilar": [
            "Bir gün tek başına kalmak, bütün hayatı sorgulamaktır.",
            "İnsan hem sever hem savaşır."
        ]
    },
    "Küçük Ağa - Tarık Buğra": {
        "kategori": "Turk Edebiyati",
        "ozet": "Millî Mücadele döneminde Akşehir'de geçen roman, İstanbul hükümetinin propagandacısı olarak gelen genç müderris'in zamanla Kuvâ-yı Milliye saflarına geçişini anlatır. Buğra, ideolojik dönüşümü, halkın savaş karşısındaki tutumunu ve bireysel vicdanın sesini tarihi bir çerçevede işler.",
        "karakterler": [
            ("Küçük Ağa", "İstanbul yanlısıyken Millî Mücadele'ye dönen müderris"),
            ("Çolak Salih", "Kuvâ-yı Milliye'nin yerel lideri"),
            ("Eşref Hoca", "Halkı yönlendiren etkili din adamı")
        ],
        "temalar": ["Millî Mücadele", "İdeolojik dönüşüm", "Bireysel vicdan"],
        "alintilar": [
            "İnsan bazen en büyük düşmanının kendisi olduğunu fark eder.",
            "Vatan, ayak bastığın toprak değil, uğruna can verdiğin topraktır."
        ]
    },
    "Ölmeye Yatmak - Adalet Ağaoğlu": {
        "kategori": "Turk Edebiyati",
        "ozet": "Aysel, Cumhuriyet'in ilk kuşağından bir kadın akademisyendir. Bir otel odasında intihar etmeye karar verdiği gece, hayatını gözden geçirir. Çocukluğundan beri taşıdığı toplumsal baskılar, kadın olmanın zorlukları ve modernleşmenin bireysel bedeli sorgulanır. Ağaoğlu, Cumhuriyet ideallerinin bir kadının iç dünyasındaki yansımalarını çok katmanlı bir anlatımla işler.",
        "karakterler": [
            ("Aysel", "Modernleşmenin bedelini ödeyen kadın akademisyen"),
            ("Engin", "Aysel'in öğrencisi ve sevgilisi olan genç adam"),
            ("Ömer", "Aysel'in kocası")
        ],
        "temalar": ["Kadın ve modernleşme", "Cumhuriyet idealleri", "Bireysel bunalım"],
        "alintilar": [
            "Ölmeye yatmak, aslında yaşamayı sorgulamaktır.",
            "Kadın olmak bu memlekette ayrı bir savaştır."
        ]
    },
    "Anayurt Oteli - Yusuf Atılgan": {
        "kategori": "Turk Edebiyati",
        "ozet": "Zebercet, küçük bir kasabadaki Anayurt Oteli'nin yalnız ve içine kapanık müdürüdür. Bir gece otelde kalan gizemli kadına takıntılı bir tutku geliştirir ve kadının gitmesiyle gittikçe dengesini kaybeder. Atılgan, yalnızlığın ve bastırılmış arzuların yıkıcı etkisini klaustrofobik bir atmosferde anlatır.",
        "karakterler": [
            ("Zebercet", "Yalnız, takıntılı ve giderek çözülen otel müdürü"),
            ("Gizemli kadın", "Bir gece otelde kalıp giden ve Zebercet'i saplantıya sürükleyen kadın"),
            ("Otel çalışanları", "Zebercet'in sınırlı sosyal çevresi")
        ],
        "temalar": ["Yalnızlık ve takıntı", "Bastırılmış arzular", "Çözülme"],
        "alintilar": [
            "İnsan yalnızlığa alışır ama yalnızlık insana alışmaz.",
            "Beklemek, en ağır cezadır."
        ]
    },
    "Aylak Adam - Yusuf Atılgan": {
        "kategori": "Turk Edebiyati",
        "ozet": "C., İstanbul sokaklarında aylak aylak dolaşan, toplumsal normlara uymayı reddeden bir adamdır. Ne çalışır ne de bir amacı vardır. Kadınlarla ilişkileri yüzeysel kalır. Atılgan, modern kent insanının anlamsızlık duygusunu ve varoluşsal boşluğunu İstanbul'un sokaklarında dolaştırır.",
        "karakterler": [
            ("C.", "Toplumdan kopuk, amaçsız dolaşan genç adam"),
            ("Güler", "C.'nin ilişki yaşadığı kadınlardan biri"),
            ("Ayşe", "C.'nin karşılaştığı başka bir kadın")
        ],
        "temalar": ["Varoluşsal boşluk", "Aylaklik ve anlamsızlık", "Kent yalnızlığı"],
        "alintilar": [
            "Bir şey yapmamak da bir şey yapmaktır.",
            "Sokaklarda yürümek, kendinden kaçmaktır."
        ]
    },
    "Kuyucaklı Yusuf - Sabahattin Ali": {
        "kategori": "Turk Edebiyati",
        "ozet": "Yetim Yusuf, kaymakam tarafından evlat edinilir ve kızı Muazzez ile evlenir. Kasabadaki kötü niyetli insanların entrikaları Yusuf'u suça sürükler. Taşra hayatının acımasızlığı, iftira ve adaletsizlik Yusuf'un hayatını yıkar. Sabahattin Ali, sıradan insanın toplumsal düzen karşısındaki çaresizliğini sert bir gerçekçilikle anlatır.",
        "karakterler": [
            ("Yusuf", "İyi kalpli ama toplumun kurbanı olan yetim genç"),
            ("Muazzez", "Yusuf'un sevdiği ve evlendiği kaymakamın kızı"),
            ("Şakir", "Yusuf'a düşmanlık besleyen kötü niyetli kasabalı")
        ],
        "temalar": ["Taşra gerçeği", "Adaletsizlik", "Bireyin ezilmesi"],
        "alintilar": [
            "Dünyada en büyük suç, güçsüz doğmaktır.",
            "Kasaba, insanı ya yutar ya kusar."
        ]
    },

    # ========================== İTALYAN EDEBİYATI (10) ==========================

    "İlahi Komedya - Dante Alighieri": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Dante, hayatının ortasında karanlık bir ormanda yolunu kaybeder ve Vergilius rehberliğinde Cehennem ve Araf'ı, ardından Beatrice ile Cennet'i gezer. Her daire farklı günahları veya erdemleri temsil eder. Dante, ortaçağ dünya görüşünü, dini inancı ve aşkı insanlık tarihinin en büyük alegorik şiirinde birleştirir.",
        "karakterler": [
            ("Dante", "Ahiret yolculuğunu yapan şair-anlatıcı"),
            ("Vergilius", "Cehennem ve Araf'ta Dante'nin rehberi olan antik şair"),
            ("Beatrice", "Cennet'te Dante'ye rehberlik eden ilahi aşk figürü")
        ],
        "temalar": ["Günah ve kefaret", "İlahi adalet", "Aşk ve kurtuluş"],
        "alintilar": [
            "Buraya girenler, bütün umutlarınızı bırakın.",
            "Aşk, güneşi ve diğer yıldızları hareket ettiren güçtür."
        ]
    },
    "Dekameron - Giovanni Boccaccio": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Veba salgınından kaçan on genç, Floransa dışında bir villaya sığınarak on gün boyunca birbirlerine hikâyeler anlatır. Yüz hikâyeden oluşan eser, aşk, zekâ, aldatma ve kader gibi temaları mizahi ve erotik bir dille işler. Boccaccio, ortaçağ toplumunun ahlakını sorguulayan İtalyan nesrinin temel eserini yazar.",
        "karakterler": [
            ("Fiammetta", "Hikâye anlatıcılarından biri, zeki ve güzel kadın"),
            ("Dioneo", "En cesur ve esprili hikâyeleri anlatan genç"),
            ("Pampinea", "Grubun lideri olan olgun kadın")
        ],
        "temalar": ["Aşk ve arzu", "Zekâ ve kurnazlık", "Toplumsal hiciv"],
        "alintilar": [
            "Aşk, krallara bile hükmeder.",
            "Talih cesur olanı kayırır."
        ]
    },
    "Prens - Niccolo Machiavelli": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Machiavelli, ideal bir hükümdarın nasıl davranması gerektiğini tartışır. İktidarı ele geçirmek ve korumak için gerektiğinde acımasız olunması gerektiğini savunur. Ahlak ve politikayı birbirinden ayıran bu eser, modern siyaset biliminin kurucu metnidir. Tartışmalı olmakla birlikte, güç ve yönetim üzerine en etkili kitaplardan biri olarak kabul edilir.",
        "karakterler": [
            ("Prens", "İdeal hükümdar modeli"),
            ("Cesare Borgia", "Machiavelli'nin hayranlık duyduğu güçlü lider"),
            ("Lorenzo de' Medici", "Kitabın ithaf edildiği Floransalı prens")
        ],
        "temalar": ["İktidar ve güç", "Ahlak ve politika", "Liderlik"],
        "alintilar": [
            "Amaç, araçları meşrulaştırır.",
            "Sevilmektense korkulan olmak daha güvenlidir."
        ]
    },
    "Pinokyo - Carlo Collodi": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Marangoz Gepetto'nun yaptığı tahta kukla Pinokyo, canlanan ama sürekli başını belaya sokan yaramaz bir çocuğa dönüşür. Yalan söyledikçe burnu uzar, dolandırıcılarla başı derde girer. Sonunda dürüst ve iyi kalpli davranmayı öğrenerek gerçek bir çocuğa dönüşür. Collodi, ahlaki büyümenin önemini fantastik bir macera içinde anlatır.",
        "karakterler": [
            ("Pinokyo", "Gerçek çocuk olmak isteyen yaramaz tahta kukla"),
            ("Gepetto", "Pinokyo'yu yapan sevecen yaşlı marangoz"),
            ("Konuşan Cırcır Böceği", "Pinokyo'ya doğruyu söyleyen bilge rehber")
        ],
        "temalar": ["Dürüstlük ve ahlak", "Büyüme ve sorumluluk", "Sevgi ve dönüşüm"],
        "alintilar": [
            "Bir yalan söylersin, bin yalan söylersin.",
            "Gerçek çocuk olmak, yalnızca et ve kemik olmak değildir."
        ]
    },
    "Gülün Adı - Umberto Eco": {
        "kategori": "Italyan Edebiyati",
        "ozet": "14. yüzyılda İtalya'daki bir Benedikten manastırında gizemli ölümler yaşanır. Fransisken keşiş William ve çırağı Adso, cinayetleri araştırırken yasak bir kitabın izine düşer. Eco, ortaçağ teolojisi, felsefe ve edebiyat bilgisini bir polisiye gerilim içinde harmanlayarak entelektüel bir başyapıt yaratır.",
        "karakterler": [
            ("William of Baskerville", "Sherlock Holmes'u andıran zeki Fransisken keşiş"),
            ("Adso", "William'ın genç çırağı ve anlatıcı"),
            ("Jorge", "Kör, yaşlı ve tehlikeli kütüphaneci keşiş")
        ],
        "temalar": ["Bilgi ve güç", "Din ve dogma", "Gülmenin tehlikesi"],
        "alintilar": [
            "Gülün eski adından geriye yalnızca çıplak isim kalmıştır.",
            "Kitaplar öldürmez; ama onlar için ölenler vardır."
        ]
    },
    "Parsifal'in Son Yolculuğu - Lampedusa": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Sicilya'nın birleşme döneminde Prens Fabrizio Salina, eski aristokrat düzenin çöküşünü izler. Yeğeni Tancredi yeni düzenle uyum sağlarken prens, değişimin kaçınılmazlığını kabullenir ama içten içe hüzün duyar. Lampedusa'nın tek romanı olan Leopar, tarihsel geçişlerin bireysel bedelini zarif bir dille anlatır.",
        "karakterler": [
            ("Prens Fabrizio Salina", "Aristokrasinin çöküşünü izleyen bilge prens"),
            ("Tancredi", "Yeni düzene uyum sağlayan pragmatik yeğen"),
            ("Angelica", "Zengin tüccar kızı, Tancredi'nin nişanlısı")
        ],
        "temalar": ["Toplumsal değişim", "Aristokrasinin çöküşü", "Ölüm ve zaman"],
        "alintilar": [
            "Her şeyin aynı kalması için her şeyin değişmesi gerekir.",
            "Biz leoparlardık, aslanlarız; yerimize çakallar ve koyunlar geçecek."
        ]
    },
    "Görünmez Kentler - Italo Calvino": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Marco Polo, Kubilay Han'a hayali kentleri anlatır. Her kent, insan deneyiminin farklı bir yönünü temsil eder: bellek, arzu, göstergeler, ölüler. Calvino, şehir kavramını felsefi ve şiirsel bir oyun alanına dönüştürerek edebiyatın sınırlarını zorlar.",
        "karakterler": [
            ("Marco Polo", "Kubilay Han'a kentleri anlatan Venedikli gezgin"),
            ("Kubilay Han", "İmparatorluğunun kentlerini hayal eden hükümdar"),
            ("Kentler", "Her biri farklı bir insan deneyimini simgeleyen hayali şehirler")
        ],
        "temalar": ["Bellek ve hayal gücü", "Kent ve medeniyet", "Dil ve anlam"],
        "alintilar": [
            "Cehennem bizim her gün yaşadığımız şeydir.",
            "Bir kenti anlatan, aslında kendini anlatır."
        ]
    },

    # ========================== İSPANYOL / LATİN AMERİKA (15) ==========================

    "Don Kişot - Miguel de Cervantes": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Yaşlı soylu Alonso Quijano, şövalye romanlarını fazla okuyarak aklını kaçırır ve kendini Don Kişot olarak ilan eder. Sadık yardımcısı Sancho Panza ile birlikte yel değirmenlerine saldırır ve hayali düşmanlara karşı savaşır. Cervantes, idealizm ile gerçeklik arasındaki çatışmayı hicvederek modern romanın temellerini atar.",
        "karakterler": [
            ("Don Kişot", "Kendini şövalye sanan hayalperest yaşlı adam"),
            ("Sancho Panza", "Sadık, pratik ve sağduyulu silahtar"),
            ("Dulcinea", "Don Kişot'un hayali prensesi olan köylü kız")
        ],
        "temalar": ["İdealizm ve gerçeklik", "Delilik ve bilgelik", "Macera ve hayal"],
        "alintilar": [
            "Olduğun gibi görün, göründüğün gibi ol.",
            "Yel değirmenlerine saldırmak, bazen en cesur eylemdir."
        ]
    },
    "Yüzyıllık Yalnızlık - Gabriel Garcia Marquez": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Buendía ailesi, Macondo kasabasını kurar ve yedi kuşak boyunca aşk, savaş, çılgınlık ve yalnızlıkla boğuşur. Her nesil aynı hataları tekrar eder ve aile sonunda bir kasırgayla yok olur. Marquez, büyülü gerçekçiliğin başyapıtında Latin Amerika tarihini mitolojik bir dille yeniden yazar.",
        "karakterler": [
            ("Jose Arcadio Buendía", "Macondo'nun kurucusu, hayalperest ve çılgın"),
            ("Ursula Iguarán", "Aileyi ayakta tutan güçlü ve uzun ömürlü anne"),
            ("Albay Aureliano Buendía", "32 savaş başlatan ama hepsini kaybeden kahraman")
        ],
        "temalar": ["Yalnızlık ve kader", "Zaman ve döngüsellik", "Aşk ve tutku"],
        "alintilar": [
            "Yıllar sonra, kurşuna dizileceği gün, Albay Aureliano Buendía babasının onu buzu keşfetmeye götürdüğü o uzak öğleden sonrayı hatırlayacaktı.",
            "Yalnızlık, paylaşılmadıkça büyür."
        ]
    },
    "Kolera Günlerinde Aşk - Gabriel Garcia Marquez": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Florentino Ariza, gençliğinde âşık olduğu Fermina Daza'yı elli yıldan fazla bekler. Fermina, zengin doktor Juvenal Urbino ile evlenir. Urbino'nun ölümünden sonra Florentino aşkını yeniden ilan eder. Marquez, zamanın aşk üzerindeki etkisini ve tutkununun ölümsüzlüğünü büyülü bir dille anlatır.",
        "karakterler": [
            ("Florentino Ariza", "Elli yıl boyunca aşkını bekleyen romantik adam"),
            ("Fermina Daza", "Güçlü iradeli, gururlu kadın"),
            ("Dr. Juvenal Urbino", "Fermina'nın saygın ve kültürlü kocası")
        ],
        "temalar": ["Ebedi aşk", "Zaman ve bekleme", "Yaşlılık ve tutku"],
        "alintilar": [
            "Onu elli bir yıl, dokuz ay ve dört gündür bekliyordum.",
            "Aşk, gençlikte başlar ama yaşlılıkta anlam kazanır."
        ]
    },
    "Ficciones - Jorge Luis Borges": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Borges'in en ünlü öykü derlemesi, labirentler, aynalar, sonsuz kütüphaneler ve paralel evrenler gibi felsefi kavramları edebiyata taşır. Her öykü, gerçeklik, zaman ve kimliğin doğasını sorgulayan entelektüel bir bilmecedir. Borges, kısa öykü formunu felsefi düşüncenin aracına dönüştürür.",
        "karakterler": [
            ("Anlatıcılar", "Her öyküde farklı bir sorgulayıcı ses"),
            ("Ts'ui Pên", "Çatallaşan Bahçeler öyküsünün gizemli yaratıcısı"),
            ("Pierre Menard", "Don Kişot'u yeniden yazan hayali yazar")
        ],
        "temalar": ["Sonsuzluk ve labirent", "Gerçeklik ve kurgu", "Zaman ve kimlik"],
        "alintilar": [
            "Cennet, bir kütüphane biçiminde olmalı.",
            "Bir labirent, kaybolmak için değil, bulmak için vardır."
        ]
    },
    "Ruhlar Evi - Isabel Allende": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Trueba ailesi üç kuşak boyunca Şili'nin siyasi ve toplumsal çalkantılarının ortasında yaşar. Büyükanne Clara'nın doğaüstü yeteneklerinden torunu Alba'nın askeri diktatörlüğe direnişine kadar kadınların güçlü hikayeleri anlatılır. Allende, büyülü gerçekçilikle aile destanını ve siyasi şiddeti birleştirir.",
        "karakterler": [
            ("Clara", "Doğaüstü güçlere sahip ruhani büyükanne"),
            ("Esteban Trueba", "Tutkulu, otoriter ve zamanla yumuşayan aile reisi"),
            ("Alba", "Askeri diktaya direnen cesur torun")
        ],
        "temalar": ["Kadın gücü", "Siyasal şiddet", "Aile ve bellek"],
        "alintilar": [
            "Yazarken hatırlıyorum, hatırladıkça yazıyorum.",
            "İntikam kısır bir döngüdür."
        ]
    },
    "Körlük - Jose Saramago": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Bir şehirde nedensiz bir körlük salgını yayılır ve görme yetisini kaybedenler karantinaya alınır. Tek gören kadın, kocası ve bir grup insanla birlikte hayatta kalmaya çalışır. Saramago, uygarlığın ne kadar kırılgan olduğunu, insanın barbarlığa ne çabuk dönebileceğini alegorik bir anlatımla ortaya koyar.",
        "karakterler": [
            ("Doktorun karısı", "Tek gören ve grubu ayakta tutan kadın"),
            ("Doktor", "Kör olan ilk hastalardan biri"),
            ("Kara gözlüklü kız", "Karantinada dönüşen genç kadın")
        ],
        "temalar": ["Uygarlığın kırılganlığı", "İnsan doğası", "Dayanışma ve şiddet"],
        "alintilar": [
            "Gözlerimiz kör olduğunda aklımız görmüyorsa ne işe yarar?",
            "Körlük, başkalarını görmemektir."
        ]
    },
    "Simyacı - Paulo Coelho": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "İspanyol çoban Santiago, tekrarlayan bir rüyanın peşinden Mısır piramitlerine hazine aramaya gider. Yolculuğunda simyacıyla tanışır ve evrenin dilini, kişisel efsaneyi ve kalbini dinlemeyi öğrenir. Coelho, kişisel dönüşüm ve hayallerin peşinden gitme mesajını alegorik bir macera içinde sunar.",
        "karakterler": [
            ("Santiago", "Hazinesini arayan genç İspanyol çoban"),
            ("Simyacı", "Santiago'ya evrenin sırlarını öğreten bilge"),
            ("Fatima", "Santiago'nun çölde tanışıp sevdiği kadın")
        ],
        "temalar": ["Kişisel efsane", "Hayallerin peşinden gitmek", "Evrenin dili"],
        "alintilar": [
            "Bir şeyi gerçekten istediğin zaman bütün evren sana yardım etmek için işbirliği yapar.",
            "Hazine, yolculuğun kendisidir."
        ]
    },
    "Benim Sessiz Sevgilim - Neruda / Neruda'nın Şiirleri": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Neruda'nın Yirmi Aşk Şiiri ve Bir Umutsuzluk Şarkısı, gençlik aşkının tutkusunu, kaybını ve özlemini yoğun imgelerle anlatır. Doğa metaforları ve bedensel imgelerle dolu şiirler, Latin Amerika şiirinin en çok okunan eserlerinden biri olarak dünya edebiyatında yerini alır.",
        "karakterler": [
            ("Şair", "Aşkını yoğun imgelerle ifade eden genç Neruda"),
            ("Sevgili", "Şiirlerin ilham kaynağı olan kadın(lar)"),
            ("Doğa", "Aşkın metaforu olarak kullanılan evren")
        ],
        "temalar": ["Tutku ve kayıp", "Doğa ve aşk", "Özlem ve umutsuzluk"],
        "alintilar": [
            "Seni seviyorum, ama belki de sevmiyorum. Aşk bu kadar kısa, unutuş bu kadar uzun.",
            "Sessizliğini seviyorum, çünkü orada yokmuşsun gibi."
        ]
    },
    "Pedro Paramo - Juan Rulfo": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Juan Preciado, annesinin vasiyetiyle babası Pedro Páramo'yu bulmak için Comala kasabasına gider. Kasabanın hayaletlerle dolu olduğunu ve tüm sakinlerin ölü olduğunu keşfeder. Rulfo, yaşam ve ölüm arasındaki sınırı silerek Latin Amerika edebiyatının en yenilikçi ve etkileyici kısa romanlarından birini yazar.",
        "karakterler": [
            ("Pedro Páramo", "Acımasız toprak ağası ve kasabanın hakimi"),
            ("Juan Preciado", "Babasını arayan ve gerçeği keşfeden oğul"),
            ("Susana San Juan", "Pedro Páramo'nun hayat boyu sevdiği kadın")
        ],
        "temalar": ["Ölüm ve yaşam", "Güç ve zulüm", "Bellek ve hayalet"],
        "alintilar": [
            "Comala'ya geldim çünkü babamın burada olduğu söylenmişti.",
            "Ölüler de konuşur, yeter ki dinleyen biri olsun."
        ]
    },
    "Labirent Generali - Gabriel Garcia Marquez": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Simon Bolivar'ın son günlerini anlatan roman, büyük özgürleştiriciyi hastalık, hayal kırıklığı ve yalnızlık içinde gösterir. Kurduğu cumhuriyetler parçalanmış, arkadaşları ihanet etmiş, bedeni çürümüştür. Marquez, kahramanın insani yüzünü ve ideallerin çöküşünü dokunaklı bir dille anlatır.",
        "karakterler": [
            ("Simon Bolivar", "Güney Amerika'nın büyük özgürleştiricisi"),
            ("Jose Palacios", "Bolivar'ın sadık uşağı"),
            ("Manuela Sáenz", "Bolivar'ın cesur ve sadık sevgilisi")
        ],
        "temalar": ["Kahramanın düşüşü", "İdeallerin çöküşü", "Yalnızlık ve ölüm"],
        "alintilar": [
            "Tarih bizi affetmeyecek.",
            "Devrim yapmayı bilen, barış yapmayı da bilmelidir."
        ]
    },

    # ========================== JAPON EDEBİYATI (10) ==========================

    "Norveç Ormanı - Haruki Murakami": {
        "kategori": "Japon Edebiyati",
        "ozet": "Toru Watanabe, üniversite yıllarında ölmüş arkadaşı Kizuki'nin kız arkadaşı Naoko ile yakınlaşır. Naoko ruhsal sorunlarla boğuşurken, hayat dolu Midori Watanabe'nin hayatına girer. Kayıp, ölüm ve aşk arasında sıkışan Watanabe, yetişkinliğe geçişin acılarını yaşar. Murakami, 1960'ların Japonya'sında gençliğin melankolisini müzikle harmanlar.",
        "karakterler": [
            ("Toru Watanabe", "Kayıp ve aşk arasında sıkışan genç üniversiteli"),
            ("Naoko", "Ruhsal sorunlarla mücadele eden kırılgan genç kadın"),
            ("Midori", "Hayat dolu, özgür ruhlu ve çekici genç kız")
        ],
        "temalar": ["Kayıp ve yas", "Aşk ve yalnızlık", "Büyümenin acısı"],
        "alintilar": [
            "Ölüm, hayatın karşıtı değil, parçasıdır.",
            "Yalnızca yarısı doğru olan şeyler en acıtanlardır."
        ]
    },
    "Kafka Sahilde - Haruki Murakami": {
        "kategori": "Japon Edebiyati",
        "ozet": "On beş yaşındaki Kafka Tamura evden kaçarak bir kütüphaneye sığınır. Paralel hikâyede yaşlı Nakata, kedilerle konuşabilir ve kayıp hafızasının izini sürer. İki hikâye gizemli şekilde kesişir. Murakami, Yunan tragedyası motifleriyle Japon kültürünü birleştirerek gerçeklik ve bilinçdışı arasında gidip gelen bir roman yazar.",
        "karakterler": [
            ("Kafka Tamura", "Evden kaçan on beş yaşındaki genç"),
            ("Nakata", "Kedilerle konuşabilen yaşlı adam"),
            ("Oshima", "Kütüphanede çalışan bilge ve yardımsever genç")
        ],
        "temalar": ["Kader ve özgür irade", "Bilinçdışı ve gerçeklik", "Büyüme ve kimlik"],
        "alintilar": [
            "Fırtına bittiğinde, ondan nasıl geçtiğini hatırlamayacaksın.",
            "Bazen kader, karanlık bir koridordur."
        ]
    },
    "Botchan - Natsume Soseki": {
        "kategori": "Japon Edebiyati",
        "ozet": "Genç ve dürüst Botchan, Tokyo'dan taşra kasabasına öğretmen olarak gider. Okulda ikiyüzlü meslektaşları ve entrikacı yöneticilerle mücadele eder. Doğrudan ve patavatsız kişiliğiyle taşranın küçük oyunlarına isyan eder. Soseki, Meiji Japonya'sının toplumsal çelişkilerini mizahi ve eleştirel bir dille anlatır.",
        "karakterler": [
            ("Botchan", "Dürüst, doğrudan ve kavgacı genç öğretmen"),
            ("Kırmızı Gömlek", "İkiyüzlü ve entrikacı öğretmen"),
            ("Kiyo", "Botchan'ı çocukluğundan beri seven sadık hizmetçi kadın")
        ],
        "temalar": ["Dürüstlük ve ikiyüzlülük", "Taşra hayatı", "Toplumsal eleştiri"],
        "alintilar": [
            "Dürüstlük, en tehlikeli silahtır.",
            "İnsanlar birbirlerine yalan söylerken gülümserler."
        ]
    },
    "Altın Tapınak - Yukio Mishima": {
        "kategori": "Japon Edebiyati",
        "ozet": "Genç ve kekeme rahip adayı Mizoguchi, Kyoto'daki Kinkaku-ji tapınağının güzelliğine saplantılı bir hayranlık duyar. Güzelliğin onu yaşamaktan alıkoyduğuna inanarak tapınağı ateşe verir. Mishima, güzellik, yıkım ve varoluş arasındaki gerilimi gerçek bir olaydan esinlenerek derin bir psikolojik çözümlemeyle anlatır.",
        "karakterler": [
            ("Mizoguchi", "Güzelliğe saplantılı, kekeme rahip adayı"),
            ("Kashiwagi", "Mizoguchi'yi etkileyen alaycı ve çarpık ayaklı arkadaş"),
            ("Tapınak başrahibi", "İkiyüzlü yaşamıyla Mizoguchi'yi hayal kırıklığına uğratan rahip")
        ],
        "temalar": ["Güzellik ve yıkım", "Saplantı", "Varoluşsal bunalım"],
        "alintilar": [
            "Güzellik, beni yaşamaktan alıkoyuyordu.",
            "Yıkmak da bir yaratmadır."
        ]
    },
    "Denize Düşen Melek - Yukio Mishima": {
        "kategori": "Japon Edebiyati",
        "ozet": "Yaşlanan Shigekuni Honda, genç denizci Toru'da ölmüş arkadaşı Kiyoaki'nin reenkarnasyonunu gördüğüne inanır ve onu evlat edinir. Toru, beklentilerin aksine soğuk ve hesapçı çıkar. Honda'nın tüm reenkarnasyon arayışı boşuna mıydı sorusu eserin merkezindedir. Mishima'nın Bereket Denizi dörtlemesinin son kitabıdır.",
        "karakterler": [
            ("Honda", "Hayat boyu reenkarnasyon izleyen yaşlı adam"),
            ("Toru", "Evlat edinilen ama beklentileri boşa çıkaran genç"),
            ("Satoko", "Honda'nın eski tanıdığı, manastırda yaşayan kadın")
        ],
        "temalar": ["Reenkarnasyon ve yanılsama", "Yaşlılık ve hayal kırıklığı", "Boşluk"],
        "alintilar": [
            "Bellek yanıltıcıdır; yaşanmamış şeyleri bile hatırlarız.",
            "Her son, aslında bir başlangıçtır."
        ]
    },
    "Kar Ülkesi - Yasunari Kawabata": {
        "kategori": "Japon Edebiyati",
        "ozet": "Tokyo'lu seyrek Shimamura, karlı dağ kasabasına giderek geyşa Komako ile ilişki yaşar. Komako onu derinden severken Shimamura kayıtsız ve uzak kalır. Trenle yolculuk ederken camda yansımasını gördüğü Yoko da gizemli bir çekim yaratır. Kawabata, aşkın geçiciliğini ve güzelliğin melankolisini Japon estetiğiyle yoğun bir şekilde işler.",
        "karakterler": [
            ("Shimamura", "Kayıtsız ve uzak Tokyo'lu zengin adam"),
            ("Komako", "Tutkulu ve sadık dağ kasabası geişası"),
            ("Yoko", "Gizemli ve çekici genç kadın")
        ],
        "temalar": ["Geçici güzellik", "Aşk ve kayıtsızlık", "Doğa ve estetik"],
        "alintilar": [
            "Tünelin öbür ucunda kar ülkesi vardı.",
            "Güzellik, bir anda parlayıp sönen bir ışıktır."
        ]
    },
    "Bin Turna Kuşu - Yasunari Kawabata": {
        "kategori": "Japon Edebiyati",
        "ozet": "Genç Kikuji, babasının eski metresiyle ve onun kızıyla karmaşık ilişkiler yaşar. Çay törenleri etrafında dönen hikâyede geleneksel Japon estetiği, suçluluk duygusu ve arzu iç içe geçer. Kawabata, insan ilişkilerinin karmaşıklığını çay kültürünün zarif ritüelleriyle harmanlayarak yoğun bir atmosfer yaratır.",
        "karakterler": [
            ("Kikuji", "Babasının geçmişinden kaçamayan genç adam"),
            ("Chikako", "Entrikacı ve manipülatif yaşlı kadın"),
            ("Fumiko", "Kikuji'nin ilgi duyduğu genç kadın")
        ],
        "temalar": ["Gelenek ve arzu", "Suçluluk ve geçmiş", "Japon estetiği"],
        "alintilar": [
            "Geçmiş, bir çay fincanının dibindeki tortu gibidir.",
            "Güzellik, acının bir başka yüzüdür."
        ]
    },
    "Sasameyuki - Junichiro Tanizaki": {
        "kategori": "Japon Edebiyati",
        "ozet": "Osaka'lı Makioka ailesinin dört kız kardeşinin 1930'lardaki hayatı anlatılır. Geleneksel bir ailenin üçüncü kızına uygun bir koca bulma çabası romanın ana eksenini oluşturur. Tanizaki, İkinci Dünya Savaşı öncesi Japonya'sında geleneksel değerlerin erozyonunu, mevsimler ve doğanın güzelliğiyle harmanlayarak zarif bir aile portresi çizer.",
        "karakterler": [
            ("Sachiko", "Ailenin sorumluluğunu taşıyan ikinci kardeş"),
            ("Yukiko", "Utangaç ve geleneksel üçüncü kardeş"),
            ("Taeko", "Modern ve isyankâr en küçük kardeş")
        ],
        "temalar": ["Gelenek ve modernlik", "Aile ve toplumsal baskı", "Japon estetiği"],
        "alintilar": [
            "Kiraz çiçekleri açar ve düşer; hayat da böyledir.",
            "Gelenekler, sessizce çözülür."
        ]
    },

    # ========================== KLASİK / ANTİK (10) ==========================

    "İlyada - Homeros": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Truva Savaşı'nın onuncu yılında Yunan savaşçı Akhilleus, komutan Agamemnon'la anlaşmazlığa düşerek savaştan çekilir. Arkadaşı Patroklos'un ölümüyle intikam için geri döner ve Truvalı kahraman Hektor'u öldürür. Homeros, savaşın şanını ve trajedisini, onur, öfke ve ölümlülük temaları etrafında anlatır.",
        "karakterler": [
            ("Akhilleus", "En güçlü Yunan savaşçısı, öfkeli ve onurlu"),
            ("Hektor", "Truva'nın cesur ve onurlu prensi"),
            ("Patroklos", "Akhilleus'un en yakın arkadaşı")
        ],
        "temalar": ["Savaş ve onur", "Öfke ve intikam", "Ölümlülük"],
        "alintilar": [
            "Öfke, tanrılara bile hükmeder.",
            "Her insanın kaderi doğduğu anda yazılır."
        ]
    },
    "Odysseia - Homeros": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Truva Savaşı'ndan sonra Kral Odysseus, evine dönmek için on yıl boyunca denizlerde dolaşır. Tek gözlü dev Kiklop, büyücü Kirke, Sirenler ve yeraltı dünyası gibi tehlikelerle karşılaşır. Sadık eşi Penelope onu beklerken, Odysseus sonunda İthaka'ya ulaşarak tahtını geri alır.",
        "karakterler": [
            ("Odysseus", "Kurnaz, cesur ve sabırlı İthaka Kralı"),
            ("Penelope", "Kocasını yıllarca bekleyen sadık eş"),
            ("Telemakhos", "Babasını arayan genç oğul")
        ],
        "temalar": ["Yolculuk ve eve dönüş", "Sadakat ve sabır", "Kurnazlık ve cesaret"],
        "alintilar": [
            "Bana adımı sordun; adım Kimse'dir.",
            "Deniz, insanı hem yok eder hem var eder."
        ]
    },
    "Kral Oidipus - Sofokles": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Thebai Kralı Oidipus, şehirdeki vebayı durdurmak için eski kralın katilini arar. Soruşturma derinleştikçe katilin kendisi olduğunu, farkında olmadan babasını öldürüp annesiyle evlendiğini keşfeder. Kaderden kaçılamayacağının en güçlü ifadesi olan bu trajedi, Batı edebiyatının temel metinlerinden biridir.",
        "karakterler": [
            ("Oidipus", "Gerçeği arayan ama gerçeğin kurbanı olan kral"),
            ("İokaste", "Oidipus'un hem annesi hem karısı olan kraliçe"),
            ("Teiresias", "Gerçeği bilen kör kahin")
        ],
        "temalar": ["Kader ve özgür irade", "Bilgi ve cehalet", "Suç ve kefaret"],
        "alintilar": [
            "Görmek istemeyen gözler en kördür.",
            "Sonunu görmeden hiçbir insana mutlu deme."
        ]
    },
    "Antigone - Sofokles": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Antigone, Kral Kreon'un yasağına rağmen ölen kardeşi Polyneikes'i gömmekte ısrar eder. İlahi yasa ile devlet yasası arasındaki bu çatışma, Antigone'nin ölümüne ve Kreon'un ailesinin yıkımına yol açar. Sofokles, bireysel vicdanın devlet otoritesine karşı duruşunu trajik bir biçimde işler.",
        "karakterler": [
            ("Antigone", "Vicdanının sesini dinleyen cesur genç kadın"),
            ("Kreon", "Devlet otoritesini temsil eden katı kral"),
            ("Haimon", "Antigone'nin nişanlısı ve Kreon'un oğlu")
        ],
        "temalar": ["Bireysel vicdan ve devlet", "Adalet ve yasa", "Kadının direnci"],
        "alintilar": [
            "Ölülerin yasaları, yaşayanların yasalarından üstündür.",
            "Kibir, çöküşün habercisidir."
        ]
    },
    "Medeia - Euripides": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Medeia, kocası İason'un onu terk edip bir prensesle evlenmek istemesiyle intikam planı kurar. Büyücü kadın, rakibini ve kendi çocuklarını öldürerek İason'a en ağır cezayı verir. Euripides, kadının toplumda dışlanmasını ve ihanetin sonuçlarını şok edici bir trajedide anlatır.",
        "karakterler": [
            ("Medeia", "İntikam için her şeyi göze alan güçlü büyücü kadın"),
            ("İason", "Medeia'yı terk eden hırslı ve nankör kahraman"),
            ("Kreon", "Medeia'yı sürgüne göndermeye çalışan Korinthos kralı")
        ],
        "temalar": ["İntikam ve ihanet", "Kadının öfkesi", "Aşk ve nefret"],
        "alintilar": [
            "Kadına yapılabilecek en büyük haksızlık, onu küçümsemektir.",
            "İntikam, soğuk servisi en iyi servistir."
        ]
    },
    "Devlet - Platon": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Sokrates ve muhatabları, ideal devletin nasıl olması gerektiğini tartışır. Adalet kavramını bireyde ve toplumda araştırırken, filozofların yönetmesi gereken bir devlet modeli önerir. Mağara alegorisi, güneş benzetmesi ve çizgi benzetmesi ile bilgi kuramını ortaya koyar. Batı felsefesinin en etkili eserlerinden biridir.",
        "karakterler": [
            ("Sokrates", "Diyaloğu yöneten büyük filozof"),
            ("Glaukon", "Sokrates'in tartışma ortaklarından biri"),
            ("Trasymakhos", "Adaletin güçlünün çıkarı olduğunu savunan sofist")
        ],
        "temalar": ["Adalet", "İdeal devlet", "Bilgi ve hakikat"],
        "alintilar": [
            "İncelenmeyen hayat yaşanmaya değmez.",
            "Gördüğümüz gölgelerdir; gerçekler mağaranın dışındadır."
        ]
    },
    "Elektra - Euripides": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Agamemnon'un kızı Elektra, babasının katili olan annesi Klytaimnestra ve üvey babası Aigisthos'tan intikam almak için kardeşi Orestes'i bekler. Orestes döndüğünde birlikte intikamı gerçekleştirirler ancak vicdanları ağır bir yük taşır. Euripides, adalet ve intikam arasındaki ince çizgiyi sorgualar.",
        "karakterler": [
            ("Elektra", "Babasının intikamına kendini adamış güçlü kadın"),
            ("Orestes", "Sürgünden dönen ve intikamı gerçekleştiren oğul"),
            ("Klytaimnestra", "Kocasını öldüren ve suçluluk taşıyan anne")
        ],
        "temalar": ["İntikam ve adalet", "Aile bağları", "Suçluluk duygusu"],
        "alintilar": [
            "Kan kanla ödenir.",
            "Adalet mi, intikam mı? Aradaki çizgi çok incedir."
        ]
    },
    "Aeneis - Vergilius": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Truva'nın düşüşünden sonra kahraman Aeneas, tanrıların emriyle İtalya'ya giderek Roma'nın temellerini atacak nesli kurmakla görevlendirilir. Fırtınalar, savaşlar ve Kartacalı kraliçe Dido ile yaşadığı trajik aşk yolculuğunu şekillendirir. Vergilius, Roma'nın kuruluş destanını Homeros geleneğiyle birleştirerek Latin edebiyatının başyapıtını yazar.",
        "karakterler": [
            ("Aeneas", "Truvalı kahraman ve Roma'nın efsanevi kurucusu"),
            ("Dido", "Aeneas'a âşık olan ve terk edilince intihar eden Kartaca kraliçesi"),
            ("Turnus", "İtalya'da Aeneas'a karşı savaşan yerli kral")
        ],
        "temalar": ["Görev ve kader", "Aşk ve fedakârlık", "İmparatorluk kuruculuğu"],
        "alintilar": [
            "Silahları ve adamı anlatıyorum.",
            "Kader yolunu bulur."
        ]
    },

    # ========================== FELSEFE (10) ==========================

    "Böyle Buyurdu Zerdüşt - Friedrich Nietzsche": {
        "kategori": "Felsefe",
        "ozet": "Zerdüşt, on yıl dağda inzivadan sonra insanlara üstinsan, ebedi dönüş ve iradenin gücü öğretilerini getirmek üzere iner. Ancak insanlar onu anlamaz. Nietzsche, geleneksel ahlakı yıkan, bireyin kendi değerlerini yaratmasını savunan felsefesini şiirsel ve alegorik bir dille sunar.",
        "karakterler": [
            ("Zerdüşt", "Nietzsche'nin felsefesinin sözcüsü olan bilge"),
            ("Kartal ve yılan", "Zerdüşt'ün gurur ve bilgelik simgesi hayvanları"),
            ("Son insan", "Konfor içinde anlamsız yaşayan sıradan insan")
        ],
        "temalar": ["Üstinsan", "Ebedi dönüş", "Değerlerin yeniden değerlendirilmesi"],
        "alintilar": [
            "Tanrı öldü! Ve onu biz öldürdük.",
            "İnsan, hayvan ile üstinsan arasında gerilmiş bir iptir."
        ]
    },
    "Varlık ve Zaman - Martin Heidegger": {
        "kategori": "Felsefe",
        "ozet": "Heidegger, varlığın anlamını sorgulayarak 'Dasein' (orada-olmak) kavramını merkeze koyar. İnsanın dünyaya fırlatılmışlığı, kaygı, ölüme-doğru-varlık ve zamansallık gibi kavramları derinlemesine inceler. 20. yüzyıl felsefesinin en etkili eserlerinden biri olan kitap, varoluşçuluk ve hermeneutik geleneğini derinden etkilemiştir.",
        "karakterler": [
            ("Dasein", "İnsan varlığını ifade eden felsefi kavram"),
            ("Heidegger", "Varlığın anlamını sorgulayan düşünür"),
            ("Husserl", "Heidegger'in hocası ve fenomenolojinin kurucusu")
        ],
        "temalar": ["Varlığın anlamı", "Zaman ve ölümlülük", "Otantik varoluş"],
        "alintilar": [
            "Varlık nedir sorusu, felsefenin en temel sorusudur.",
            "Dil, varlığın evidir."
        ]
    },
    "Toplum Sözleşmesi - Jean-Jacques Rousseau": {
        "kategori": "Felsefe",
        "ozet": "Rousseau, insanların özgür doğduğunu ancak toplumsal düzenin onları zincirlere vurduğunu savunur. Meşru siyasi otoritenin ancak halkın genel iradesine dayanan bir toplum sözleşmesiyle kurulabileceğini önerir. Esere, Fransız Devrimi'ni esinleyen ve modern demokrasinin temellerini atan düşünceler hakimdir.",
        "karakterler": [
            ("Rousseau", "Eserin yazarı ve düşüncelerinin savunucusu"),
            ("Genel irade", "Toplumun ortak çıkarını temsil eden soyut kavram"),
            ("Egemen", "Halkın kendisi olan yönetim gücü")
        ],
        "temalar": ["Özgürlük ve eşitlik", "Toplumsal sözleşme", "Demokrasi"],
        "alintilar": [
            "İnsan özgür doğar, oysa her yerde zincire vurulmuştur.",
            "Genel irade her zaman doğrudur."
        ]
    },
    "Ütopya - Thomas More": {
        "kategori": "Felsefe",
        "ozet": "More, hayali Ütopya adasını betimleyerek ideal bir toplum düzeni kurar. Özel mülkiyet yoktur, herkes çalışır, eğitim ve sağlık herkese açıktır. Din özgürlüğü ve hoşgörü egemendir. More, kendi döneminin İngilteresi'ni eleştirmek için bu ideal dünyayı bir ayna olarak kullanır.",
        "karakterler": [
            ("Thomas More", "Eserin yazarı ve diyaloğun katılımcısı"),
            ("Raphael Hythloday", "Ütopya'yı ziyaret ettiğini anlatan gezgin"),
            ("Peter Giles", "More'un Antwerp'teki arkadaşı")
        ],
        "temalar": ["İdeal toplum", "Adalet ve eşitlik", "Toplumsal eleştiri"],
        "alintilar": [
            "Özel mülkiyetin olduğu yerde adalet olmaz.",
            "Altın, Ütopya'da çocukların oyuncağıdır."
        ]
    },
    "Özgürlük Üzerine - John Stuart Mill": {
        "kategori": "Felsefe",
        "ozet": "Mill, bireysel özgürlüğün sınırlarını belirleyen zarar ilkesini ortaya koyar: birey, başkalarına zarar vermediği sürece istediğini yapabilmelidir. Düşünce ve ifade özgürlüğünü savunurken, çoğunluğun tiranlığına karşı bireyi korumak gerektiğini vurgular. Liberal düşüncenin temel metinlerinden biri olarak kabul edilir.",
        "karakterler": [
            ("Mill", "Eserin yazarı ve liberal düşüncenin savunucusu"),
            ("Harriet Taylor", "Mill'in eşi ve düşüncelerine katkı sağlayan entelektüel"),
            ("Birey", "Özgürlüğü korunması gereken toplumun üyesi")
        ],
        "temalar": ["Bireysel özgürlük", "İfade özgürlüğü", "Çoğunluğun tiranlığı"],
        "alintilar": [
            "Bir tek kişi hariç tüm insanlık aynı fikirde olsa bile, o tek kişiyi susturmak meşru değildir.",
            "Başkalarına zarar vermedikçe herkes istediği gibi yaşayabilmelidir."
        ]
    },
    "İnsanın Anlam Arayışı - Viktor Frankl": {
        "kategori": "Felsefe",
        "ozet": "Psikiyatrist Viktor Frankl, Nazi toplama kamplarında yaşadığı deneyimleri ve bu deneyimlerden geliştirdiği logoterapi yöntemini anlatır. En korkunç koşullarda bile hayatta kalanların bir anlam, bir amaç bulanlar olduğunu gösterir. Frankl, acının bile anlam taşıyabileceğini ve insanın son özgürlüğünün koşullara karşı tutumunu seçmek olduğunu savunur.",
        "karakterler": [
            ("Viktor Frankl", "Kamplardan sağ çıkan psikiyatrist ve yazar"),
            ("Kamp mahkumları", "Farklı başa çıkma stratejileri gösteren insanlar"),
            ("SS subayları", "İnsanlık dışı koşulları yaratan zalimler")
        ],
        "temalar": ["Anlam arayışı", "Acı ve dayanıklılık", "İnsan iradesi"],
        "alintilar": [
            "Yaşamak için bir nedeni olan insan, neredeyse her nasıla katlanabilir.",
            "İnsandan her şey alınabilir, bir şey hariç: verili koşullarda kendi tutumunu seçme özgürlüğü."
        ]
    },
    "Sofie'nin Dünyası - Jostein Gaarder": {
        "kategori": "Felsefe",
        "ozet": "On dört yaşındaki Sofie, posta kutusuna gelen gizemli mektuplarla felsefe tarihini öğrenmeye başlar. Sokrates'ten Sartre'a kadar büyük düşünürlerle tanışırken kendi varoluşunu da sorgulamaya başlar. Gaarder, felsefe tarihini gençler için anlaşılır ve heyecanlı bir macera romanı formatında sunar.",
        "karakterler": [
            ("Sofie Amundsen", "Felsefe öğrenen meraklı genç kız"),
            ("Alberto Knox", "Sofie'ye felsefe öğreten gizemli öğretmen"),
            ("Hilde", "Sofie'nin varlığını sorgulatan gizemli karakter")
        ],
        "temalar": ["Felsefe tarihi", "Varoluş sorgulaması", "Bilgi ve merak"],
        "alintilar": [
            "Sen kimsin?",
            "Hayret etme yetisini kaybetmiş biri, artık canlı değildir."
        ]
    },

    # ========================== DİĞER (15) ==========================

    "Karanlığın Yüreği - Joseph Conrad": {
        "kategori": "Diger",
        "ozet": "Denizci Marlow, Kongo Nehri boyunca gizemli fildişi tüccarı Kurtz'u bulmaya gider. Yolculuk, sömürgeciliğin vahşetini ve insanın karanlık doğasını ortaya çıkarır. Kurtz'un 'Dehşet! Dehşet!' sözleri, medeniyetin maskesinin ardındaki barbarlığı ifade eder. Conrad, emperyalizmin ahlaki çöküşünü yoğun bir sembolizmle anlatır.",
        "karakterler": [
            ("Marlow", "Hikâyeyi anlatan deneyimli denizci"),
            ("Kurtz", "Afrikan ormanlarında çılgına dönen fildişi tüccarı"),
            ("Yönetici", "Sömürge idarecisi")
        ],
        "temalar": ["Sömürgecilik eleştirisi", "İnsanın karanlık yüzü", "Medeniyet ve barbarlık"],
        "alintilar": [
            "Dehşet! Dehşet!",
            "Biz karanlığın yüreğinde yaşıyoruz."
        ]
    },
    "Drakula - Bram Stoker": {
        "kategori": "Diger",
        "ozet": "Avukat Jonathan Harker, Transilvanya'daki Kont Drakula'nın şatosuna iş için gider ve vampir olduğunu keşfeder. Drakula Londra'ya gelip genç kadınları hedef alınca, Profesör Van Helsing liderliğinde bir grup onu durdurmaya çalışır. Stoker, korku türünün en ikonik eserini mektup ve günlük formatında yazar.",
        "karakterler": [
            ("Kont Drakula", "Yüzyıllardır yaşayan güçlü Transilvanyalı vampir"),
            ("Jonathan Harker", "Drakula'nın şatosuna giden genç avukat"),
            ("Van Helsing", "Vampir avcısı bilge profesör")
        ],
        "temalar": ["İyilik ve kötülük", "Korku ve bilinmeyen", "Cinsellik ve bastırma"],
        "alintilar": [
            "Dikkatli olun. Bu gece dünya, tüm kötülüklere açıktır.",
            "Ölülerin dirilmesi, yaşayanların en büyük korkusudur."
        ]
    },
    "Sherlock Holmes'un Maceraları - Arthur Conan Doyle": {
        "kategori": "Diger",
        "ozet": "Dedektif Sherlock Holmes, Baker Sokağı 221B'deki dairesinden çıkarak Londra'nın en karmaşık suçlarını çözer. Sadık arkadaşı Dr. Watson'ın gözünden anlatılan maceralar, Holmes'un üstün mantık yeteneğini ve gözlem gücünü sergiler. Doyle, polisiye edebiyatının en ünlü karakterini yaratarak türün standartlarını belirler.",
        "karakterler": [
            ("Sherlock Holmes", "Üstün zekâ ve gözlem gücüne sahip özel dedektif"),
            ("Dr. Watson", "Holmes'un sadık arkadaşı ve hikâyelerin anlatıcısı"),
            ("Profesör Moriarty", "Holmes'un dahi suç ustası düşmanı")
        ],
        "temalar": ["Mantık ve gözlem", "Suç ve adalet", "Dostluk"],
        "alintilar": [
            "İmkânsızı eledikten sonra, geriye kalan, ne kadar inanılmaz olursa olsun, gerçek olmalıdır.",
            "Temel, sevgili Watson, temel!"
        ]
    },
    "Otomatik Portakal - Anthony Burgess": {
        "kategori": "Diger",
        "ozet": "Genç Alex, arkadaşlarıyla birlikte şiddet dolu bir yaşam sürer. Yakalanıp hapse girdiğinde, devletin deneysel bir tedaviyle şiddetten arındırılması onu özgür iradesinden yoksun bırakır. Burgess, bireysel özgürlük ile toplumsal düzen arasındaki gerilimi ve devletin birey üzerindeki gücünü distopik bir çerçevede sorgular.",
        "karakterler": [
            ("Alex", "Şiddet ve müzik tutkunu genç suçlu"),
            ("Dr. Brodsky", "Ludovico tedavisini uygulayan bilim insanı"),
            ("Hapishane papazı", "Alex'in özgür iradesini savunan din adamı")
        ],
        "temalar": ["Özgür irade", "Şiddet ve toplum", "Devlet müdahalesi"],
        "alintilar": [
            "İyiliği seçmek zorunda olduğun bir dünyada, iyilik iyilik midir?",
            "Gerçek sorun şuydu: bir insanı iyi olmaya zorlayabilir misiniz?"
        ]
    },
    "Zaman Makinesi - H.G. Wells": {
        "kategori": "Diger",
        "ozet": "Bir bilim insanı, icat ettiği zaman makinesiyle yüz binlerce yıl sonrasına yolculuk yapar. Gelecekte insanlık ikiye ayrılmıştır: yüzeyde yaşayan naif Eloi'ler ve yeraltında yaşayan vahşi Morlock'lar. Wells, sınıf eşitsizliğinin nihai sonucunu bilim kurgu çerçevesinde sunarken, ilerleme kavramını sorgular.",
        "karakterler": [
            ("Zaman Gezgini", "Zaman makinesini icat eden bilim insanı"),
            ("Weena", "Zaman Gezgini'nin sevdiği Eloi kadın"),
            ("Morlock'lar", "Yeraltında yaşayan karanlık yaratıklar")
        ],
        "temalar": ["Sınıf eşitsizliği", "İlerleme ve çöküş", "Zaman ve evrim"],
        "alintilar": [
            "Zaman yolculuğu mümkündür; yalnızca doğru araç gerekir.",
            "Gelecek, bugünün korkularının aynasıdır."
        ]
    },
    "Dünyalar Savaşı - H.G. Wells": {
        "kategori": "Diger",
        "ozet": "Mars'tan gelen uzaylılar İngiltere'yi istila eder. İnsanların tüm silahları yetersiz kalır ve uygarlık çöker. Sonunda uzaylıları yenen insanlar değil, Dünya'nın mikropları olur. Wells, emperyalizmin eleştirisini ters çevirerek İngiliz toplumunun bir istila karşısındaki kırılganlığını gösterir.",
        "karakterler": [
            ("Anlatıcı", "İstilayı yaşayan ve anlatan adsız adam"),
            ("Anlatıcının kardeşi", "Londra'daki kaçışı anlatan ikinci anlatıcı"),
            ("Marslılar", "Üstün teknolojiye sahip istilacı uzaylılar")
        ],
        "temalar": ["İstila ve hayatta kalma", "Emperyalizm eleştirisi", "İnsanın doğa karşısındaki zayıflığı"],
        "alintilar": [
            "Kimse Mars'tan bizi izlediklerini bilmiyordu.",
            "İnsanlığın en büyük savunucusu doğanın kendisidir."
        ]
    },
    "Alice Harikalar Diyarında - Lewis Carroll": {
        "kategori": "Diger",
        "ozet": "Küçük Alice, beyaz bir tavşanın peşinden tavşan deliğine düşerek fantastik bir dünyaya girer. Büyüyüp küçüldüğü, konuşan hayvanlarla ve çılgın karakterlerle karşılaştığı absürt maceralar yaşar. Carroll, çocuk edebiyatının klasiklerinden birini yazarken dil oyunları, mantık bilmeceleri ve toplumsal hicvi iç içe geçirir.",
        "karakterler": [
            ("Alice", "Meraklı ve mantıklı küçük kız"),
            ("Çılgın Şapkacı", "Saçma sapan çay partisi veren eksantrik karakter"),
            ("Kırmızı Kraliçe", "Sürekli kafa kesmek isteyen öfkeli kraliçe")
        ],
        "temalar": ["Absürdlük ve mantık", "Büyüme ve kimlik", "Dil ve anlam"],
        "alintilar": [
            "Hepimiz deliyiz burada.",
            "Nereye gittiğini bilmiyorsan, hangi yol seni oraya götürecek farketmez."
        ]
    },
    "Peter Pan - J.M. Barrie": {
        "kategori": "Diger",
        "ozet": "Hiç büyümeyen çocuk Peter Pan, Wendy ve kardeşlerini uçarak Varolmayan Ülke'ye götürür. Kayıp Çocuklar, korsanlar ve Kaptan Kanca ile maceralar yaşarlar. Sonunda Wendy büyümeyi ve eve dönmeyi seçer. Barrie, çocukluğun masumiyetini ve büyümenin kaçınılmazlığını fantastik bir dünyada anlatır.",
        "karakterler": [
            ("Peter Pan", "Hiç büyümeyen, uçabilen çocuk"),
            ("Wendy Darling", "Peter'a anne olan ve sonunda büyümeyi kabul eden kız"),
            ("Kaptan Kanca", "Peter Pan'ın düşmanı, tek elli korsan")
        ],
        "temalar": ["Çocukluk ve büyüme", "Hayal gücü", "Zaman ve ölümsüzlük"],
        "alintilar": [
            "Büyümek zorunda olmadığınız bir yer var.",
            "Uçmak için tek ihtiyacınız olan güzel, harika ve mutlu düşüncelerdir."
        ]
    },
    "Oz Büyücüsü - L. Frank Baum": {
        "kategori": "Diger",
        "ozet": "Kansas'lı küçük Dorothy, kasırgayla büyülü Oz ülkesine savrulur. Evine dönmek için Zümrüt Şehir'deki büyücüyü bulmaya gider. Yolda beyin isteyen Korkuluk, kalp isteyen Teneke Adam ve cesaret isteyen Korkak Aslan'la arkadaş olur. Baum, aradığımız şeylerin aslında içimizde olduğunu masalsı bir maceryla anlatır.",
        "karakterler": [
            ("Dorothy", "Evine dönmek isteyen cesur küçük kız"),
            ("Korkuluk", "Beyin isteyen ama aslında zeki olan dostça karakter"),
            ("Oz Büyücüsü", "Aslında sıradan bir adam olan sahte büyücü")
        ],
        "temalar": ["İç güç keşfi", "Dostluk ve yolculuk", "Görünüş ve gerçeklik"],
        "alintilar": [
            "Eve giden bir yol her zaman vardır.",
            "Bir kalp, dünyanın en değerli şeyidir."
        ]
    },
    "Görünmez Adam - H.G. Wells": {
        "kategori": "Diger",
        "ozet": "Bilim insanı Griffin, görünmezlik formülünü keşfeder ve kendini görünmez yapar. Ancak görünmezliğin getirdiği güç onu yozlaştırır ve toplumdan tamamen koparak şiddete yönelir. Geri dönüşü olmayan deneyinin kurbanı olur. Wells, bilimin kontrolsüz kullanımını ve gücün yozlaştırcı etkisini bilim kurgu çerçevesinde anlatır.",
        "karakterler": [
            ("Griffin", "Görünmezlik formülünü bulan ama çılgına dönen bilim insanı"),
            ("Dr. Kemp", "Griffin'in eski arkadaşı ve onu durdurmaya çalışan doktor"),
            ("Marvel", "Griffin'in zorla yardımcısı yaptığı serseri")
        ],
        "temalar": ["Bilimin tehlikeleri", "Güç ve yozlaşma", "Yalnızlık ve delilik"],
        "alintilar": [
            "Görünmez olmak, yalnız olmaktır.",
            "Güç, kontrol edilemezse yıkım getirir."
        ]
    },
    "Aya Yolculuk - Jules Verne": {
        "kategori": "Diger",
        "ozet": "Amerikan İç Savaşı'ndan sonra Baltimore Silah Kulübü üyeleri, dev bir topla Ay'a mermi göndermeye karar verir. Cesur maceracılar mermi kapsülüne binerek Ay'a doğru yola çıkar. Verne, gerçekleşmeden yetmiş yıl önce uzay yolculuğunun temel ilkelerini şaşırtıcı bir doğrulukla öngörür.",
        "karakterler": [
            ("Impey Barbicane", "Projenin başındaki kararlı başkan"),
            ("Michel Ardan", "Maceraperest Fransız gönüllü"),
            ("Kaptan Nicholl", "Başlangıçta projeye karşı olan silah uzmanı")
        ],
        "temalar": ["Bilim ve keşif", "İnsan merakı", "Macera ve cesaret"],
        "alintilar": [
            "İmkânsız, yalnızca henüz denenmemiş olanın adıdır.",
            "Bilim, insanlığın en büyük macerası."
        ]
    },
    "Lord Jim - Joseph Conrad": {
        "kategori": "Diger",
        "ozet": "Genç denizci Jim, batan bir gemiden yolcuları terk ederek kaçar ve bu korkaklık onu hayat boyu takip eder. Uzak bir ada toplumunda yeni bir hayat kurmaya çalışır ve orada kahraman olur. Ancak geçmişi onu yakalar. Conrad, onur, suçluluk ve kefaret temalarını egzotik mekânlarda derinlemesine işler.",
        "karakterler": [
            ("Jim", "Tek bir anın korkaklığıyla damgalanan genç denizci"),
            ("Marlow", "Jim'in hikâyesini anlatan denizci"),
            ("Doramin", "Ada toplumunun lideri")
        ],
        "temalar": ["Onur ve korkaklık", "Kefaret arayışı", "Kimlik ve itibar"],
        "alintilar": [
            "Bir an, bütün bir hayatı belirleyebilir.",
            "İnsan, hayali değil, eylemleridir."
        ]
    },
    "Kayıp Dünya - Arthur Conan Doyle": {
        "kategori": "Diger",
        "ozet": "Profesör Challenger, Güney Amerika'da dinozorların hâlâ yaşadığı yüksek bir platoya keşif gezisi düzenler. Gazeteci Malone ve diğer maceracılarla birlikte tarih öncesi canlılarla yüz yüze gelirler. Doyle, bilim kurgu ve macera türlerini birleştirerek keşif ruhunu ve doğanın sırlarını heyecanlı bir anlatımla sunar.",
        "karakterler": [
            ("Profesör Challenger", "Eksantrik, güçlü ve kendine güvenen bilim insanı"),
            ("Edward Malone", "Maceraya atılan genç gazeteci"),
            ("Lord John Roxton", "Deneyimli avcı ve kaşif")
        ],
        "temalar": ["Keşif ve macera", "Bilim ve doğa", "İnsanın merakı"],
        "alintilar": [
            "İmkânsız denen şeyler, sadece henüz keşfedilmemiş olanlardır.",
            "Dünya, sandığımızdan çok daha gizemlidir."
        ]
    },
    "Deniz Feneri - Virginia Woolf": {
        "kategori": "Diger",
        "ozet": "Ramsay ailesi, İskoçya'daki yazlık evlerinden deniz fenerine bir gezi planlar. İlk bölümde gezi ertelenir; yıllar geçer, savaş olur, aile üyeleri ölür. Sonunda gezi gerçekleşir ancak her şey değişmiştir. Woolf, bilinç akışı tekniğiyle zaman, kayıp ve anın değerini derin bir şekilde işler.",
        "karakterler": [
            ("Mrs. Ramsay", "Ailenin merkezi olan sıcak ve şefkatli anne"),
            ("Mr. Ramsay", "Entelektüel ama duygusal olarak uzak baba"),
            ("Lily Briscoe", "Sanatçı kimliğiyle mücadele eden genç ressam")
        ],
        "temalar": ["Zaman ve kayıp", "Sanat ve yaşam", "Aile bağları"],
        "alintilar": [
            "Hiçbir şey sadece bir şey değildir.",
            "Her an, geçmişin ve geleceğin kesişim noktasıdır."
        ]
    },
    "Gulliver'in Gezileri'ndeki Houyhnhnm Ülkesi - Jonathan Swift": {
        "kategori": "Diger",
        "ozet": "Swift'in satirik başyapıtının son bölümünde Gulliver, akıllı atların yönettiği ve insanımsı vahşi Yahoo'ların yaşadığı bir ülkeye gelir. Houyhnhnm'lar mantık ve erdemle yaşarken, Yahoo'lar insanın en kötü halini temsil eder. Gulliver, insanlığa olan inancını kaybeder. Swift, insan doğasının en sert eleştirisini bu bölümde yapar.",
        "karakterler": [
            ("Gulliver", "Artık insanlıktan tiksinmeye başlayan gezgin"),
            ("Houyhnhnm'lar", "Akıl ve erdemin somutlaşmış hali olan atlar"),
            ("Yahoo'lar", "İnsanın hayvani yüzünü temsil eden yaratıklar")
        ],
        "temalar": ["İnsan doğasının eleştirisi", "Akıl ve erdem", "Medeniyet sorgulaması"],
        "alintilar": [
            "İnsan, aklını kötülük için kullanan tek yaratıktır.",
            "Yahoo'lar bizden farklı değildir; biz onlardan farklıyız sanırız."
        ]
    },

    # ========================== EK: TÜRK EDEBİYATI (6) ==========================

    "Yılanı Öldürseler - Yaşar Kemal": {
        "kategori": "Turk Edebiyati",
        "ozet": "Küçük bir Çukurova köyünde yaşayan yaşlı Esme Ana'nın torunu Hasan, kasabadan dönerken bir yılanla karşılaşır ve olaylar gelişir. Köy halkının batıl inançları, doğayla ilişkileri ve modern dünyayla çatışmaları anlatılır. Yaşar Kemal, Anadolu insanının iç dünyasını ve doğaya bakışını yoğun bir şiirsellikle ortaya koyar.",
        "karakterler": [
            ("Hasan", "Köy hayatının içinde büyüyen küçük çocuk"),
            ("Esme Ana", "Bilge ve geleneklere bağlı yaşlı kadın"),
            ("Köylüler", "Batıl inançlarla yaşayan topluluk")
        ],
        "temalar": ["Doğa ve insan", "Batıl inançlar", "Anadolu gerçeği"],
        "alintilar": [
            "Doğa, insandan güçlüdür; insan bunu kabullenmeli.",
            "Yılanı öldürsen de korkusu kalmaz mı?"
        ]
    },
    "Sahibinin Sesi - Orhan Pamuk": {
        "kategori": "Turk Edebiyati",
        "ozet": "Gazeteci Galip, bir gece ansızın kaybolan karısı Rüya'yı ve eniştesi köşe yazarı Celal'i aramaya koyulur. İstanbul'un sokaklarında dolaşırken Celal'in köşe yazılarındaki gizemleri çözmeye çalışır. Pamuk, kimlik, bellek ve İstanbul'un katmanlarını postmodern bir anlatımla birleştirir.",
        "karakterler": [
            ("Galip", "Karısını ve eniştesini arayan avukat"),
            ("Rüya", "Gizemli bir şekilde kaybolan Galip'in karısı"),
            ("Celal", "Ünlü köşe yazarı ve Galip'in enişte")
        ],
        "temalar": ["Kimlik ve benlik", "İstanbul ve bellek", "Kayıp ve arayış"],
        "alintilar": [
            "Her yüzün altında başka bir yüz vardır.",
            "İstanbul, kaybolmak için en güzel şehirdir."
        ]
    },
    "Esir Şehrin İnsanları - Kemal Tahir": {
        "kategori": "Turk Edebiyati",
        "ozet": "İstanbul'un işgal altında olduğu dönemde farklı kesimlerden insanların yaşamları anlatılır. İşbirlikçiler, direnişçiler ve sıradan vatandaşların arasındaki gerilim, şehrin esaret altındaki atmosferiyle birleşir. Kemal Tahir, Millî Mücadele'nin İstanbul cephesini toplumsal bir panorama olarak sunar.",
        "karakterler": [
            ("Kamil", "Direnişe katılan idealist genç"),
            ("Seyfi Bey", "İşgalcilerle işbirliği yapan fırsatçı"),
            ("Neriman", "Savaşın ortasında hayatta kalmaya çalışan kadın")
        ],
        "temalar": ["İşgal ve direniş", "İşbirlikçilik", "Toplumsal çürüme"],
        "alintilar": [
            "Esir şehirde yaşamak, her gün biraz daha ölmektir.",
            "Direnmek, var olmaktır."
        ]
    },
    "Baba Evi - Orhan Kemal": {
        "kategori": "Turk Edebiyati",
        "ozet": "Orhan Kemal'in otobiyografik romanı, çocukluk ve gençlik yıllarını, babası Abdülkadir'in siyasi sürgünle dağılan ailelerini ve yoksulluk içindeki büyüme mücadelesini anlatır. Adana'dan İstanbul'a uzanan yolculukta aile bağları, onur ve hayatta kalma mücadelesi iç içe geçer.",
        "karakterler": [
            ("Anlatıcı", "Orhan Kemal'in kendisi; gençliğinde mücadele eden çocuk"),
            ("Abdülkadir Bey", "Sürgüne gönderilen baba; milletvekili ve idealist"),
            ("Anne", "Ailesini ayakta tutmaya çalışan fedakâr kadın")
        ],
        "temalar": ["Aile ve yoksulluk", "Sürgün ve ayrılık", "Büyüme ve direniş"],
        "alintilar": [
            "Baba evi, insanın ilk vatanıdır.",
            "Yoksulluk, insanın ruhunu da aşındırır."
        ]
    },
    "Bir Düğün Gecesi - Adalet Ağaoğlu": {
        "kategori": "Turk Edebiyati",
        "ozet": "12 Eylül askeri darbesi sonrasında bir düğün gecesinde bir araya gelen farklı kuşaklardan insanların iç dünyaları ve toplumsal yarılmalar anlatılır. Her karakter farklı bir siyasi ve kişisel kriz yaşar. Ağaoğlu, Türkiye'nin 1980 sonrası travmasını tek bir geceye sığdırarak çok sesli bir roman yazar.",
        "karakterler": [
            ("Ömer", "Darbeyle yüzleşen solcu genç"),
            ("Tezel", "Aysel'in kız kardeşi, geleneksel kadın"),
            ("Yıldız", "Modern ama çelişkili genç kadın")
        ],
        "temalar": ["Darbe ve toplumsal travma", "Nesil çatışması", "Bireysel bunalım"],
        "alintilar": [
            "Düğün gecesi, herkesin maskesinin düştüğü geceydi.",
            "Sessizlik, en büyük suç ortağıdır."
        ]
    },
    "Sevdalinka - Necip Fazıl Kısakürek": {
        "kategori": "Turk Edebiyati",
        "ozet": "Kaldırımlar şiiriyle ünlü Necip Fazıl'ın şiir dünyasında İstanbul'un karanlık sokakları, varoluşsal bunalım ve tasavvufi arayış iç içe geçer. Kaldırımları arşınlayan yalnız bir ruhun iç monologu olarak şiirler, bireyin manevi arayışını ve modern dünyanın boşluğunu dile getirir. Türk şiirinin en özgün seslerinden biridir.",
        "karakterler": [
            ("Şair", "Kaldırımlarda dolaşan yalnız ve bunalımlı genç"),
            ("Şehir", "İstanbul'un karanlık ve gizemli sokaklari"),
            ("İç ses", "Şairin manevi arayışını yansıtan bilinç")
        ],
        "temalar": ["Varoluşsal bunalım", "Manevi arayış", "Kent ve yalnızlık"],
        "alintilar": [
            "Kaldırımlar, çilekeş yalnızların annesi.",
            "Sokaktayım, kimsesiz bir sokak ortasında."
        ]
    },

    # ========================== EK: FRANSIZ EDEBİYATI (4) ==========================

    "Vadideki Zambak - Honore de Balzac": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Genç Felix de Vandenesse, bir baloda tanıştığı evli kadın Madame de Mortsauf'a platonik bir aşk besler. Loire vadisindeki malikânesinde geçen yıllar boyunca ruhani bir bağ kurarlar ancak Madame de Mortsauf acımasız kocası yüzünden eriyip gider. Balzac, aşkın idealize edilmiş halini ve kadının toplumsal esaretini doğa betimlemeleriyle harmanlayarak anlatır.",
        "karakterler": [
            ("Felix de Vandenesse", "Platonik aşk besleyen genç adam"),
            ("Madame de Mortsauf", "Erdemli ama mutsuz evli kadın"),
            ("Kont de Mortsauf", "Karısını ezen huysuz koca")
        ],
        "temalar": ["Platonik aşk", "Kadının toplumsal konumu", "Doğa ve ruh"],
        "alintilar": [
            "Gerçek aşk, sahip olmak değil, sevmektir.",
            "Vadideki zambak gibi saf ve ulaşılmazdı."
        ]
    },
    "Kapı - Andre Gide": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Gide'in Dar Kapı romanında Jerome, kuzeni Alissa'ya derin bir aşk besler. Alissa ise dini inançları nedeniyle dünyevi aşktan vazgeçmeyi seçer ve kendini Tanrı'ya adar. Jerome'un mektupları ve Alissa'nın günlüğü üzerinden anlatılan hikâye, fedakârlığın sınırlarını ve dini bağnazlığın aşkı nasıl yok ettiğini sorgular.",
        "karakterler": [
            ("Jerome", "Alissa'ya tutkuyla bağlı olan anlatıcı"),
            ("Alissa", "Aşkı Tanrı için reddeden dinine bağlı kadın"),
            ("Juliette", "Alissa'nın kız kardeşi")
        ],
        "temalar": ["Dini fedakârlık ve aşk", "Kendini feda", "Platonik aşk"],
        "alintilar": [
            "Dar kapıdan girin; çünkü geniş kapıdan girenler kaybolur.",
            "Sevmek, vazgeçmek midir gerçekten?"
        ]
    },
    "Manon Lescaut - Abbe Prevost": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Genç şövalye des Grieux, güzel ama kararsız Manon Lescaut'ya ilk görüşte âşık olur. Manon'un lüks düşkünlüğü ikisini de suça, yoksulluğa ve sürgüne sürükler. Des Grieux her şeyi feda eder ama Manon'un ölümüyle hikâye trajik bir son bulur. Prevost, tutkulu aşkın yıkıcı gücünü 18. yüzyıl Fransa'sında anlatır.",
        "karakterler": [
            ("Des Grieux", "Manon için her şeyi feda eden tutkulu genç"),
            ("Manon Lescaut", "Güzel, çekici ama kararsız ve lüks düşkünü kadın"),
            ("Tiberge", "Des Grieux'nün sadık ve erdemli arkadaşı")
        ],
        "temalar": ["Tutkulu aşk", "Lüks ve ahlak", "Fedakârlık ve yıkım"],
        "alintilar": [
            "Onu seviyorum; bu benim suçum ve kaderim.",
            "Aşk, en güçlü zincirdir."
        ]
    },
    "Cocuk - Emile Zola": {
        "kategori": "Fransiz Edebiyati",
        "ozet": "Zola'nın Nana romanı, İkinci İmparatorluk döneminde bir fahişenin toplumun en üst kademelerine yükselişini ve çevresindeki erkeklerin çöküşünü anlatır. Nana, güzelliğini silah olarak kullanarak Paris sosyetesini yıkar. Zola, toplumsal ikiyüzlülüğü, ahlaki çürümeyi ve kadının araçsallaştırılmasını doğalcı bir üslupla sergiler.",
        "karakterler": [
            ("Nana", "Güzelliğiyle toplumu sarsan eski fahişe"),
            ("Kont Muffat", "Nana'ya saplantılı tutkusuyla yıkılan aristokrat"),
            ("Fontan", "Nana'nın gerçekten sevdiği ama kötü davranan aktör")
        ],
        "temalar": ["Toplumsal ikiyüzlülük", "Kadın ve güç", "Ahlaki çürüme"],
        "alintilar": [
            "Güzellik bir silahtır; onu kullanan da kurban olabilir.",
            "Paris, her günahı bağışlar ama hiçbirini unutmaz."
        ]
    },

    # ========================== EK: İNGİLİZ EDEBİYATI (2) ==========================

    "Hobbit - J.R.R. Tolkien": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Bilbo Baggins, sakin hobbit yaşamından koparılarak büyücü Gandalf ve on üç cücenin ejderha Smaug'un hazinesini geri alma yolculuğuna katılır. Yolda troller, goblinler ve devasa örümceklerle karşılaşır ve Gollum'dan gizemli bir yüzük bulur. Tolkien, sıradan bir bireyin olağanüstü koşullarda cesaret bulmasını masalsı bir macera içinde anlatır.",
        "karakterler": [
            ("Bilbo Baggins", "Maceraya sürüklenen rahat yaşamı seven hobbit"),
            ("Gandalf", "Yolculuğu organize eden bilge büyücü"),
            ("Thorin Meşekalkan", "Cücelerin lideri ve dağ kralı")
        ],
        "temalar": ["Sıradan kahramanlık", "Macera ve büyüme", "Açgözlülük"],
        "alintilar": [
            "Dünyada en sevdiğim şey, sıcak bir ocak başıdır.",
            "Küçük eller büyük işler başarır."
        ]
    },
    "Bir Noel Şarkısı - Charles Dickens": {
        "kategori": "Ingiliz Edebiyati",
        "ozet": "Cimri ve soğuk iş adamı Ebenezer Scrooge, Noel gecesi üç hayalet tarafından ziyaret edilir. Geçmişin, şimdinin ve geleceğin hayaletleri ona yaşamını gösterir. Geleceğin karanlık tablosu Scrooge'u derinden etkiler ve cömert, sevecen bir insana dönüşür. Dickens, Noel'in ruhunu ve insani dönüşümün gücünü kalıcı bir klasik olarak anlatır.",
        "karakterler": [
            ("Ebenezer Scrooge", "Cimri ve soğuk ama sonunda dönüşen yaşlı iş adamı"),
            ("Bob Cratchit", "Scrooge'un düşük maaşlı, sabırlı çalışanı"),
            ("Küçük Tim", "Bob'un hasta ama neşeli küçük oğlu")
        ],
        "temalar": ["Cömertlik ve dönüşüm", "Noel ruhu", "Empati ve merhamet"],
        "alintilar": [
            "Tanrı hepimizi korusun, her birimizi!",
            "İnsanlık benim işimdir. Genel refah benim işimdir."
        ]
    },

    # ========================== EK: AMERİKAN EDEBİYATI (4) ==========================

    "Beyaz Diş - Jack London": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Yarı kurt yarı köpek olan Beyaz Diş, Yukon vahşi doğasında hayatta kalmayı öğrenir. Önce kurtlar arasında, sonra Kızılderililerin yanında ve en sonunda acımasız bir dövüş organizatöründe yaşar. Sevecen bir sahibin eline geçtiğinde ise vahşi doğasını evcilleştirmeyi öğrenir. London, doğanın acımasızlığı ile sevginin dönüştürücü gücünü karşı karşıya koyar.",
        "karakterler": [
            ("Beyaz Diş", "Yarı kurt yarı köpek olan vahşi ama dönüşen hayvan"),
            ("Güzellik Smith", "Beyaz Diş'i dövüş köpeği olarak kullanan acımasız adam"),
            ("Weedon Scott", "Beyaz Diş'i kurtaran ve sevgiyle evcilleştiren mühendis")
        ],
        "temalar": ["Doğa ve uygarlık", "Sevginin gücü", "Hayatta kalma"],
        "alintilar": [
            "Sevgi, vahşetin panzehiridir.",
            "Güçlü olan hayatta kalır; ama sevilen, yaşar."
        ]
    },
    "Marslı Günlükler - Ray Bradbury": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "İnsanlar Mars'ı kolonileştirmeye başlar; ancak her seferinde Mars'ın gizemli yerlileriyle, kendi geçmişleriyle ve doğanın gücüyle yüzleşirler. Bradbury, birbiriyle bağlantılı öykülerle Mars'ı bir ayna olarak kullanır: insanlığın hırsını, nostaljisini ve yıkıcılığını gösterir. Eser, bilim kurgunun en şiirsel örneklerinden biridir.",
        "karakterler": [
            ("Spender", "Mars uygarlığını korumak isteyen idealist astronot"),
            ("Kaptan Wilder", "Vicdanlı ve düşünceli keşif ekibi lideri"),
            ("Marslılar", "Gizemli ve telepatik eski Mars uygarlığının son temsilcileri")
        ],
        "temalar": ["Kolonizasyon eleştirisi", "Nostalji ve kayıp", "İnsan doğası"],
        "alintilar": [
            "Mars, bize kendimizi gösterecek bir aynadır.",
            "Dünya'yı terk etmek, sorunlarını geride bırakmak değildir."
        ]
    },
    "Saatlerin Mirası - F. Scott Fitzgerald": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Fitzgerald'ın Gecenin Bu Yakası romanında, genç ve yetenekli psikiyatrist Dick Diver, zengin ama ruhsal sorunları olan Nicole ile evlenir. Nicole'ün bakımı ve sosyetenin cazibesine kapılan Dick, yavaş yavaş çözülür. Fitzgerald, Amerikan hayalinin çöküşünü, alkolizmi ve yıkıcı ilişkileri Riviera'nın göz alıcı dekoru ardında anlatır.",
        "karakterler": [
            ("Dick Diver", "Yetenekli ama zamanla çöken genç psikiyatrist"),
            ("Nicole Diver", "Zengin, güzel ama ruhsal sorunlu eş"),
            ("Rosemary Hoyt", "Dick'e hayran olan genç aktris")
        ],
        "temalar": ["Çöküş ve yozlaşma", "Zenginlik ve boşluk", "Aşk ve bağımlılık"],
        "alintilar": [
            "Tüm yaşamlar, elbette bir çöküş sürecidir.",
            "Gecelerin en karanlık anı, şafaktan hemen öncedir."
        ]
    },
    "Edebiyat Kulübü - Louisa May Alcott": {
        "kategori": "Amerikan Edebiyati",
        "ozet": "Alcott'un Küçük Erkekler romanı, Jo March'ın kocası Profesör Bhaer ile birlikte açtığı Plumfield okulundaki çocukların hikâyelerini anlatır. Her çocuk farklı bir kişilik ve sorunla gelir; sevgi, disiplin ve eğitimle dönüşürler. Alcott, eğitimin gücünü ve çocukların bireysel değerini sıcak bir anlatımla işler.",
        "karakterler": [
            ("Jo Bhaer (March)", "Plumfield'ı yöneten şefkatli ve enerjik kadın"),
            ("Profesör Bhaer", "Bilge ve sabırlı eğitimci"),
            ("Nat Blake", "Yetim ve utangaç müzisyen çocuk")
        ],
        "temalar": ["Eğitimin dönüştürücü gücü", "Çocukluk ve büyüme", "Aile ve sevgi"],
        "alintilar": [
            "Her çocuk bir mucizedir; mesele onu görebilmektir.",
            "Sevgi en iyi öğretmendir."
        ]
    },

    # ========================== EK: İSPANYOL / LATİN AMERİKA (5) ==========================

    "Başkan Babamız - Miguel Angel Asturias": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Adsız bir Latin Amerika ülkesinde acımasız bir diktatörün korku imparatorluğu anlatılır. Rejimin yarattığı paranoya, ihbar kültürü ve şiddet, sıradan insanların hayatını zehirler. Asturias, büyülü gerçekçilik ögeleriyle diktatörlüğün psikolojik yıkımını ve halkın çaresizliğini betimler.",
        "karakterler": [
            ("Başkan", "Ülkeyi korku ile yöneten gizemli diktatör"),
            ("Cara de Angel", "Diktatörün yakın adamı, sonra muhalif olan güzel yüzlü adam"),
            ("General Canales", "Haksız yere suçlanan eski asker")
        ],
        "temalar": ["Diktatörlük ve korku", "İktidar ve yozlaşma", "Bireysel direniş"],
        "alintilar": [
            "Başkan her yerdedir; görmese bile bilir.",
            "Korku, diktatörün en sadık silahıdır."
        ]
    },
    "Arılar Çağı - Isabel Allende": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Allende'nin Eva Luna romanı, piç doğan bir kızın hikâye anlatma yeteneğiyle hayatta kalma mücadelesini anlatır. Eva, Latin Amerika'nın gerilla savaşları, diktatörlükler ve toplumsal çalkantıları arasında büyür. Hikâye anlatmak onun hem silahı hem de sığınağı olur. Allende, kadın gücünü ve anlatının kurtuluş gücünü kutlar.",
        "karakterler": [
            ("Eva Luna", "Hikâye anlatarak hayatta kalan güçlü kadın"),
            ("Riad Halabi", "Eva'yı koruyan Arap kökenli iyi kalpli adam"),
            ("Huberto Naranjo", "Eva'nın aşkı olan gerilla savaşçısı")
        ],
        "temalar": ["Anlatının gücü", "Kadın mücadelesi", "Latin Amerika tarihi"],
        "alintilar": [
            "Hikâye anlatmak, dünyayı yeniden yaratmaktır.",
            "Kadınlar, kendi hikâyelerini yazmalıdır."
        ]
    },
    "Alef - Jorge Luis Borges": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Borges'in aynı adlı öyküsünde anlatıcı, bir evin bodrumunda Alef'i keşfeder: evrenin tüm noktalarını aynı anda gösteren bir nokta. Bu gizemli deneyim, sonsuzluğu kavramaya çalışan insan aklının sınırlarını ortaya koyar. Borges, metafizik kavramları edebiyata taşıyarak kısa öykü sanatının zirvesine ulaşır.",
        "karakterler": [
            ("Borges (anlatıcı)", "Alef'i keşfeden ve anlamlandırmaya çalışan yazar"),
            ("Carlos Argentino Daneri", "Alef'in bulunduğu evin sahibi olan sıradan şair"),
            ("Beatriz Viterbo", "Anlatıcının ölmüş sevgilisi")
        ],
        "temalar": ["Sonsuzluk ve kavrayış", "Bellek ve kayıp", "Gerçekliğin doğası"],
        "alintilar": [
            "Her şeyi aynı anda gördüm ve hiçbir şeyi anlatamadım.",
            "Sonsuzluk, bir noktada gizlidir."
        ]
    },
    "Altıncı Kıta - Jose Saramago": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Saramago'nun Taş Sal romanında İber Yarımadası Avrupa'dan koparak okyanusta sürüklenmeye başlar. İspanya ve Portekiz halkı yeni bir kıta olarak kendi yoluna giderken, beş yolcu gizemli bir bağla birleşir. Saramago, Avrupa kimliğini, bireysel bağları ve toplumsal aidiyeti fantastik bir olayla sorgular.",
        "karakterler": [
            ("Joana Carda", "Değnekle yere çizgi çizen gizemli kadın"),
            ("Joaquim Sassa", "Denize taş atarak olayları tetikleyen adam"),
            ("Jose Anaiço", "Sığırcıkların takip ettiği öğretmen")
        ],
        "temalar": ["Kimlik ve aidiyet", "Avrupa ve İberya", "İnsan bağları"],
        "alintilar": [
            "Bir çizgi çekersin ve dünya ikiye ayrılır.",
            "Kopuş, bazen yeni bir başlangıçtır."
        ]
    },
    "On Bir Dakika - Paulo Coelho": {
        "kategori": "Ispanyol/Latin Amerika Edebiyati",
        "ozet": "Brezilyalı genç Maria, İsviçre'de daha iyi bir hayat arayışıyla yola çıkar ve kendini fahişelik yaparken bulur. Mesleğinde kutsal ile profan arasındaki çizgiyi keşfederken bir ressamla tanışır ve gerçek aşkı bulur. Coelho, cinsellik, kutsal ve bireysel özgürlük temalarını provokatif ama felsefi bir çerçevede işler.",
        "karakterler": [
            ("Maria", "Daha iyi bir hayat arayan Brezilyalı genç kadın"),
            ("Ralf Hart", "Maria'yı gerçekten gören ve seven ressam"),
            ("Milan", "Gece kulübünün sahibi")
        ],
        "temalar": ["Cinsellik ve kutsallık", "Özgürlük ve seçim", "Aşk ve dönüşüm"],
        "alintilar": [
            "On bir dakika. Dünya on bir dakikada değişebilir.",
            "Bedeni satmak, ruhu satmak değildir."
        ]
    },

    # ========================== EK: JAPON EDEBİYATI (2) ==========================

    "1Q84 - Haruki Murakami": {
        "kategori": "Japon Edebiyati",
        "ozet": "Aomame ve Tengo, paralel bir dünyada birbirlerini aramaktadır. Gökyüzünde iki ay parlayan bu alternatif 1984'te bir tarikat, gizemli bir yazar ve küçük insanlar iç içe geçer. Murakami, aşk, kader ve gerçekliğin doğasını üç ciltlik epik bir romanda işler.",
        "karakterler": [
            ("Aomame", "Spor eğitmeni ve gizli suikastçı kadın"),
            ("Tengo", "Matematik öğretmeni ve yazar"),
            ("Lider", "Tarikatın gizemli ve güçlü başı")
        ],
        "temalar": ["Paralel gerçeklikler", "Aşk ve kader", "Bireysel özgürlük"],
        "alintilar": [
            "İki ay, gökyüzünde asılı duruyordu.",
            "Gerçeklik her zaman tek değildir."
        ]
    },
    "Kokoro - Natsume Soseki": {
        "kategori": "Japon Edebiyati",
        "ozet": "Genç bir üniversite öğrencisi, 'Sensei' dediği yaşlı bir aydınla arkadaşlık kurar. Sensei, geçmişinde yakın arkadaşına yaptığı ihanetin suçluluğunu taşır ve Meiji İmparatoru'nun ölümüyle birlikte intihar eder. Soseki, Japonya'nın modernleşme sürecindeki bireysel yalnızlığı, suçluluk ve sadakati derinden işler.",
        "karakterler": [
            ("Sensei", "Geçmişinin suçluluğunu taşıyan yalnız aydın"),
            ("Anlatıcı", "Sensei'ye hayranlık duyan genç öğrenci"),
            ("K.", "Sensei'nin arkadaşı, ihanet edilen ve intihar eden genç")
        ],
        "temalar": ["Suçluluk ve yalnızlık", "Modernleşme ve gelenek", "Dostluk ve ihanet"],
        "alintilar": [
            "İnsan kalbi, en derin uçurumdan daha karanlıktır.",
            "Yalnızlık, modern insanın kaderidir."
        ]
    },

    # ========================== EK: KLASİK / ANTİK (2) ==========================

    "Oresteia - Aiskhylos": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Üç oyundan oluşan triloji, Agamemnon'un Truva'dan dönüşünde karısı Klytaimnestra tarafından öldürülmesi, oğlu Orestes'in annesini öldürerek intikam alması ve Erinys'lerin peşine düşmesiyle devam eder. Son oyunda Athena'nın kurduğu mahkeme ile kan davası sona erer. Aiskhylos, adaletin bireysel intikamdan kurumsal yargıya evrimini işler.",
        "karakterler": [
            ("Agamemnon", "Truva'dan dönen ve öldürülen Yunan kralı"),
            ("Klytaimnestra", "Kocasını öldüren güçlü ve hesapçı kraliçe"),
            ("Orestes", "Annesini öldürerek babasının intikamını alan oğul")
        ],
        "temalar": ["Adalet ve intikam", "Kan davası ve hukuk", "İlahi düzen"],
        "alintilar": [
            "Acı çekenlere bilgelik verilir.",
            "Kan kanla temizlenmez; ancak adalet temizler."
        ]
    },
    "Symposium - Platon": {
        "kategori": "Klasik/Antik Edebiyat",
        "ozet": "Bir ziyafette Sokrates ve diğer konuklar aşkın (Eros) doğası üzerine konuşmalar yapar. Her konuşmacı farklı bir aşk tanımı sunar. Sokrates, bilge kadın Diotima'dan öğrendiğini aktarır: aşk güzelliğe yönelik bir arayıştır ve bedenden ruha, ruhtan ideaya yükselir. Platon, aşk felsefesinin temellerini bu diyalogda atar.",
        "karakterler": [
            ("Sokrates", "Aşkın felsefi doğasını açıklayan büyük filozof"),
            ("Aristophanes", "İnsanların ikiye bölünmüş yarımlar olduğunu anlatan komedya yazarı"),
            ("Alkibiades", "Sokrates'e tutkusunu itiraf eden genç politikacı")
        ],
        "temalar": ["Aşkın doğası", "Güzellik ve idea", "Ruhun yükselişi"],
        "alintilar": [
            "Aşk, güzelliğin peşinde koşmaktır.",
            "Her insan, kaybettiği diğer yarısını arar."
        ]
    },

    # ========================== EK: İTALYAN EDEBİYATI (3) ==========================

    "Bir Kış Gecesi Eğer Bir Yolcu - Italo Calvino": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Okuyucu, bir roman okumaya başlar ama kitap hatalı basılmıştır. Doğru devamını aradıkça on farklı romanın başlangıcına düşer ve hiçbirini bitiremez. Calvino, okuma eyleminin kendisini roman konusu yaparak edebiyatın sınırlarını zorlayan postmodern bir başyapıt yaratır.",
        "karakterler": [
            ("Okuyucu (Erkek)", "Kitabın devamını arayan sen-anlatıcı"),
            ("Okuyucu (Kadın) - Ludmilla", "Okuma tutkusuyla tanışılan kadın karakter"),
            ("Sahte çevirmen Marana", "Kitapları karıştıran gizemli sahtekâr")
        ],
        "temalar": ["Okuma ve yazma", "Gerçeklik ve kurgu", "Postmodern anlatı"],
        "alintilar": [
            "Bir roman okumaya başlamak üzeresin.",
            "Her başlangıç, sonsuz olasılıkların kapısıdır."
        ]
    },
    "Bir İtalyan Ailesinin Tarihi - Lampedusa": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Lampedusa'nın Leopar romanı, 1860'larda Garibaldi'nin Sicilya'yı fethi sırasında aristokrat Salina ailesinin çöküşünü anlatır. Prens Fabrizio, değişimin kaçınılmaz olduğunu anlayan ama ona karşı hüzünle direnen son büyük aristokrattır. Roman, tarihsel geçişlerin bireysel bedelini zarif bir melankoli ile işler.",
        "karakterler": [
            ("Prens Fabrizio", "Çöken aristokrasinin bilge ve yorgun temsilcisi"),
            ("Tancredi", "Değişime uyum sağlayan pragmatik yeğen"),
            ("Don Calogero", "Yükselen yeni burjuva sınıfının temsilcisi")
        ],
        "temalar": ["Tarihsel dönüşüm", "Aristokrasinin sonu", "Değişim ve kabul"],
        "alintilar": [
            "Her şeyin değişmesi gerekir ki her şey aynı kalsın.",
            "Biz leopardık; yerimize çakallar geçecek."
        ]
    },
    "Aşkın Çöl Halleri - Italo Calvino": {
        "kategori": "Italyan Edebiyati",
        "ozet": "Calvino'nun Varolmayan Şövalye romanında, zırhın içinde bedeni olmayan Şövalye Agilulfo, yalnızca iradesiyle var olur. Her şeyi mükemmel yapmasına rağmen insani sıcaklıktan yoksundur. Yanında bedeni olan ama iradesi olmayan silahtar Gurdulù dolaşır. Calvino, varoluş, kimlik ve insanlık durumunu alegorik bir ortaçağ hikâyesinde sorgular.",
        "karakterler": [
            ("Agilulfo", "Bedeni olmayan ama zırhıyla var olan şövalye"),
            ("Gurdulù", "İradesi olmayan ama bedeni olan savaşçı"),
            ("Rambaldo", "Aşk ve savaş arasında bocalayan genç şövalye")
        ],
        "temalar": ["Varoluş ve kimlik", "İrade ve beden", "Kahramanlık ve anlam"],
        "alintilar": [
            "Var olmak için bir bedene ihtiyacınız yoktur; yalnızca iradeye.",
            "Boş bir zırh, dolu bir kalp kadar gerçek olabilir."
        ]
    },

    # ========================== EK: FELSEFE (3) ==========================

    "Ahlakın Soykütüğü Üzerine - Friedrich Nietzsche": {
        "kategori": "Felsefe",
        "ozet": "Nietzsche, ahlak kavramlarının tarihsel kökenlerini araştırır. İyi ve kötü kavramlarının güçlü ile zayıf arasındaki mücadeleden doğduğunu, köle ahlakının efendi ahlakını bastırdığını savunur. Vicdan azabı ve suçluluğun toplumsal baskının ürünleri olduğunu iddia eder. Eser, Batı ahlak felsefesinin en radikal eleştirilerinden biridir.",
        "karakterler": [
            ("Nietzsche", "Geleneksel ahlakı sorgulayan düşünür"),
            ("Efendi", "Kendi değerlerini yaratan güçlü birey"),
            ("Köle", "Güçlüye karşı resentiment (hınç) duyan zayıf birey")
        ],
        "temalar": ["Ahlakın kökeni", "Güç istenci", "Efendi ve köle ahlakı"],
        "alintilar": [
            "İyi ve kötü yoktur; yalnızca güç ve zayıflık vardır.",
            "Vicdan azabı, içe dönmüş bir saldırganlıktır."
        ]
    },
    "Emile - Jean-Jacques Rousseau": {
        "kategori": "Felsefe",
        "ozet": "Rousseau, hayali öğrencisi Emile'in doğumundan yetişkinliğe kadar ideal eğitimini anlatır. Çocuğun doğal gelişimine saygı gösteren, ezberci değil deneyimsel öğrenmeyi savunan bir eğitim felsefesi ortaya koyar. Toplumun çocuğu bozduğunu ve eğitimin doğaya uygun olması gerektiğini vurgular. Modern pedagojinin temel eserlerinden biridir.",
        "karakterler": [
            ("Emile", "Doğaya uygun eğitilen hayali öğrenci"),
            ("Eğitimci", "Rousseau'nun alter egosu olan ideal öğretmen"),
            ("Sophie", "Emile'in eşi olacak doğal yetiştirilmiş kadın")
        ],
        "temalar": ["Doğal eğitim", "Çocuğun doğası", "Toplum ve yozlaşma"],
        "alintilar": [
            "Her şey, Yaratan'ın elinden çıktığında iyidir; her şey, insanın elinde bozulur.",
            "Çocuğa en iyi eğitim, onu kendi deneyimleriyle öğrenmesine izin vermektir."
        ]
    },
    "Mutluluğun Formülü - Epiktetos": {
        "kategori": "Felsefe",
        "ozet": "Epiktetos'un El Kitabı, Stoa felsefesinin pratik özetini sunar. Kontrol edebildiğimiz şeyler (düşüncelerimiz, tutumlarımız) ile edemediğimiz şeyler (dış olaylar, başkalarının davranışları) arasındaki ayrımı temel alır. Mutluluğun dış koşullardan değil, iç tutumdan geldiğini öğretir. Antik felsefenin en pratik ve etkili metinlerinden biridir.",
        "karakterler": [
            ("Epiktetos", "Eski köle olan Stoacı filozof"),
            ("Öğrenci", "Epiktetos'un öğretilerini dinleyen ve uygulayan kişi"),
            ("Kader/Doğa", "İnsan iradesinin dışındaki güçler")
        ],
        "temalar": ["Kontrol ve kabul", "İç huzur", "Erdem ve mutluluk"],
        "alintilar": [
            "İnsanları rahatsız eden şeyler değil, şeylere ilişkin yargılarıdır.",
            "Senin olan yalnızca kendi tutumundur; geri kalanı sana ait değildir."
        ]
    },

}
