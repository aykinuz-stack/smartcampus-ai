#!/usr/bin/env python3
import os

questions = [
# Deyimler +25
'{k:"Deyimler",s:"Son sözü söylemek ne demektir?",o:["Konuşmayı bitirmek","Kesin kararı vermek","Sessiz kalmak","Özür dilemek"],d:1,a:"Son sözü söylemek bir konuda kesin ve nihai kararı vermek demektir."}',
'{k:"Deyimler",s:"Çıkmaza girmek ne demektir?",o:["Dar yolda kalmak","Çözümsüz bir duruma düşmek","Kaybolmak","Yürümek"],d:1,a:"Bir sorunun çözümsüz hale gelmesi demektir."}',
'{k:"Deyimler",s:"Eli uzun olmak ne demektir?",o:["Uzun kolları olmak","Hırsızlık yapma eğiliminde olmak","Yardımsever olmak","Uzağa ulaşmak"],d:1,a:"Başkalarının eşyalarına el uzatmak hırsızlık eğilimi göstermek demektir."}',
'{k:"Deyimler",s:"Kalbi kırılmak ne anlama gelir?",o:["Kalp krizi","Çok üzülmek hayal kırıklığına uğramak","Korkuya kapılmak","Sevinmek"],d:1,a:"Birine kırgın olmak çok üzülmek demektir."}',
'{k:"Deyimler",s:"Pabucunu dama atmak ne demektir?",o:["Temizlik yapmak","Birinin yerini almak onu geçmek","Ayakkabı almak","Dans etmek"],d:1,a:"Birinin işinde kendinden üstün olmak onu geçmek demektir."}',
'{k:"Deyimler",s:"Dümeni kırmak ne demektir?",o:["Gemi sürmek","Yolunu değiştirmek planını bozmak","Dümeni tamir etmek","Yüzmek"],d:1,a:"Planını veya yönünü ani olarak değiştirmek demektir."}',
'{k:"Deyimler",s:"Maşa gibi kullanmak ne demektir?",o:["Yemek yapmak","Birini kendi çıkarı için alet etmek","Ateş yakmak","Temizlik yapmak"],d:1,a:"Birini kendi işlerini yaptırmak için alet olarak kullanmak demektir."}',
'{k:"Deyimler",s:"Yüzünü ekşitmek ne demektir?",o:["Limon yemek","Hoşnutsuzluğunu yüz ifadesiyle göstermek","Ağlamak","Gülmek"],d:1,a:"Memnuniyetsizliğini yüz ifadesiyle belli etmek demektir."}',
'{k:"Deyimler",s:"Gemi azıya almak ne demektir?",o:["Gemi kullanmak","Kontrol dışına çıkmak başına buyruk olmak","Yemek yemek","Denize açılmak"],d:1,a:"Kontrolden çıkmak kimsenin sözünü dinlememek demektir."}',
'{k:"Deyimler",s:"Yüzüne gülmek ne demektir?",o:["Mutlu olmak","İki yüzlü davranmak","Komik bulmak","Sevinmek"],d:1,a:"Yüzüne gülerken arkadan kötü konuşmak iki yüzlülük demektir."}',
'{k:"Deyimler",s:"Ağzını aramak ne demektir?",o:["Dişçiye gitmek","Birinden üstü kapalı bilgi almaya çalışmak","Yemek aramak","Konuşmak"],d:1,a:"Dolaylı sorularla birinden gizlice bilgi almaya çalışmak demektir."}',
'{k:"Deyimler",s:"Taban tabana zıt olmak ne demektir?",o:["Ayakkabı giymek","Tamamen birbirine aykırı olmak","Yürümek","Aynı olmak"],d:1,a:"İki şeyin birbirine tamamen zıt ve uyumsuz olması demektir."}',
'{k:"Deyimler",s:"Gözü yüksekte olmak ne demektir?",o:["Yüksekten korkmak","Hep daha iyisini istemek","Gözlük takmak","Uzağı görmek"],d:1,a:"Her zaman daha iyisini daha yükseğini istemek demektir."}',
'{k:"Deyimler",s:"İpin ucunu kaçırmak ne demektir?",o:["İp koparmak","Kontrolü kaybetmek","İp atlamak","Düğüm atmak"],d:1,a:"Bir işin veya durumun kontrolünü kaybetmek demektir."}',
'{k:"Deyimler",s:"Can havliyle ne demektir?",o:["Sakin olmak","Büyük korku veya panikle","Mutlulukla","Heyecanla"],d:1,a:"Ölüm korkusuyla büyük bir panikle hareket etmek demektir."}',
'{k:"Deyimler",s:"Balık kavağa çıkınca ne demektir?",o:["Balık tutmak","Olmayacak bir zaman asla","Ağaç tırmanmak","Çok beklemek"],d:1,a:"Asla gerçekleşmeyecek bir zaman dilimini ifade eder."}',
'{k:"Deyimler",s:"Daldan dala konmak ne demektir?",o:["Kuş olmak","Sürekli konu değiştirmek","Ağaçlara tırmanmak","Gezmek"],d:1,a:"Konuşurken sürekli konu değiştirmek bir konuda karar kılamamak demektir."}',
'{k:"Deyimler",s:"Elinin hamuru ile erkek işine karışmak ne anlama gelir?",o:["Yemek yapmak","Bilmediği işe karışmak","Hamur yoğurmak","Yardım etmek"],d:1,a:"Bilmediği bir konuya karışmak yetkinliği olmayan işlere burnunu sokmak demektir."}',
'{k:"Deyimler",s:"Çorap söküğü gibi gitmek ne demektir?",o:["Çorap yırtılmak","Bir şeyin peş peşe devam etmesi","Alışveriş yapmak","Koşmak"],d:1,a:"Bir işin veya olayın zincirleme şekilde birbirini izlemesi demektir."}',
'{k:"Deyimler",s:"Pabuç bırakmamak ne demektir?",o:["Ayakkabı almak","Boyun eğmemek teslim olmamak","Koşmak","Kaçmak"],d:1,a:"Hiçbir zorluk karşısında boyun eğmemek teslim olmamak demektir."}',
'{k:"Deyimler",s:"Sinek avlamak ne demektir?",o:["Böcek yakalamak","Boş oturmak işsiz olmak","Temizlik yapmak","Spor yapmak"],d:1,a:"Hiçbir iş yapmadan boş oturmak demektir."}',
'{k:"Deyimler",s:"Göz yummak ne demektir?",o:["Uyumak","Bir hatayı görmezden gelmek","Göz kapamak","Karanlık"],d:1,a:"Bir hatayı veya yanlışı bilerek görmezden gelmek demektir."}',
'{k:"Deyimler",s:"Burun kıvırmak ne demektir?",o:["Hapşırmak","Beğenmemek küçümsemek","Koku almak","Aksırmak"],d:1,a:"Bir şeyi beğenmeyip küçümsemek demektir."}',
'{k:"Deyimler",s:"Yelkenleri suya indirmek ne demektir?",o:["Denize açılmak","Pes etmek boyun eğmek","Yüzmek","Gemi yapmak"],d:1,a:"Pes etmek karşısındakinin gücünü kabul edip boyun eğmek demektir."}',
'{k:"Deyimler",s:"Ağzına bir parmak bal çalmak ne demektir?",o:["Bal yemek","Küçük bir iyilikle birini oyalamak","Tatlı yapmak","Diş fırçalamak"],d:1,a:"Küçük bir iyilik veya söz vererek birini geçici olarak memnun etmek ve oyalamak demektir."}',
# Atasözleri +25
'{k:"Atasözleri",s:"Bir mum diğer mumu tutuşturmakla ışığından kaybetmez ne anlatır?",o:["Mum yakmak","Paylaşmak seni eksiltmez","Yangın söndürmek","Aydınlatma"],d:1,a:"Bilgini veya iyiliğini paylaşmak seni eksiltmez aksine çoğaltır."}',
'{k:"Atasözleri",s:"İnsan yedisinde ne ise yetmişinde de odur ne demektir?",o:["Yaşlanmak","Karakter küçük yaşta oluşur","Sağlık","Spor yapmak"],d:1,a:"İnsanın temel karakteri küçük yaşta şekillenir ve ömür boyu değişmez."}',
'{k:"Atasözleri",s:"Çalma kapıyı çalarlar kapını ne anlatır?",o:["Kapı çalmak","Kötülük yapana kötülük yapılır","Zil çalmak","Hırsızlık"],d:1,a:"Başkasına kötülük yapan kişi bir gün aynı kötülükle karşılaşır."}',
'{k:"Atasözleri",s:"Dost acı söyler ne demektir?",o:["Kötü konuşmak","Gerçek dost doğruyu söyler","Tartışmak","Kavga etmek"],d:1,a:"Gerçek dost hoşuna gitmese bile doğruyu söyler."}',
'{k:"Atasözleri",s:"Su uyur düşman uyumaz ne anlatır?",o:["Uykusuzluk","Düşmanına karşı her zaman uyanık ol","Su kaynatmak","Gece nöbeti"],d:1,a:"Düşmanın her zaman tetikte olduğunu sende uyanık olmalısın."}',
'{k:"Atasözleri",s:"Ağlamayan çocuğa meme vermezler ne demektir?",o:["Bebek bakımı","İstediğini söylemezsen alamazsın","Ağlamak","Doktor olmak"],d:1,a:"İhtiyacını ve istediğini dile getirmezsen kimse yardım etmez."}',
'{k:"Atasözleri",s:"Aşağı tükürsem sakal yukarı tükürsem bıyık ne anlatır?",o:["Temizlik","İki seçenek de kötü çıkmaz durum","Berber olmak","Tıraş olmak"],d:1,a:"Her iki seçeneğin de kötü olduğu çıkmaz durumu ifade eder."}',
'{k:"Atasözleri",s:"Dikensiz gül olmaz ne demektir?",o:["Gül yetiştirmek","Her güzel şeyin bir zorluğu vardır","Bahçe bakmak","Çiçek almak"],d:1,a:"Her güzel şeyin yanında bir zorluk veya sıkıntı da vardır."}',
'{k:"Atasözleri",s:"Gün doğmadan neler doğar ne anlatır?",o:["Sabah erken kalkmak","Beklenmedik olaylar olabilir","Doğum","Güneşi izlemek"],d:1,a:"Her an beklenmedik olumlu veya olumsuz gelişmeler olabilir."}',
'{k:"Atasözleri",s:"Hamama giren terler ne demektir?",o:["Temizlik","İşe girişen zorluğuna katlanır","Saunaya gitmek","Spor yapmak"],d:1,a:"Bir işe girişen kişi o işin zorluklarına da katlanmalıdır."}',
'{k:"Atasözleri",s:"Kaz gelecek yerden tavuk esirgenmez ne anlatır?",o:["Tavuk beslemek","Büyük kazanç için küçük harcama yapılır","Kaz avlamak","Market alışverişi"],d:1,a:"Büyük kazanç elde etmek için küçük fedakarlıklar yapmak gerekir."}',
'{k:"Atasözleri",s:"Sel gider kum kalır ne demektir?",o:["Sel felaketi","Geçici olaylar gider kalıcı sonuçlar kalır","Kum oyunu","Çöl oluşumu"],d:1,a:"Olaylar geçicidir ama bıraktığı izler ve sonuçlar kalıcıdır."}',
'{k:"Atasözleri",s:"Yalancının mumu yatsıya kadar yanar ne anlatır?",o:["Mum yakmak","Yalan er geç ortaya çıkar","Gece lambaları","Elektrik kesintisi"],d:1,a:"Yalancı bir süre idare edebilir ama sonunda yalanı ortaya çıkar."}',
'{k:"Atasözleri",s:"Ateş düştüğü yeri yakar ne demektir?",o:["Yangın söndürmek","Felaket en çok yaşayanı etkiler","Ateş yakmak","Soba kurmak"],d:1,a:"Bir felaket veya sıkıntı en çok onu yaşayan kişiyi etkiler."}',
'{k:"Atasözleri",s:"Dolu küpten ses çıkmaz ne anlatır?",o:["Küp doldurmak","Bilgili ve olgun insan sessizdir","Müzik yapmak","Depolama"],d:1,a:"Gerçekten bilgili ve olgun insan gereksiz gürültü yapmaz."}',
'{k:"Atasözleri",s:"Herkesin bir bildiği vardır ne demektir?",o:["Herkes bilgili","Her insanın farklı bilgi ve tecrübesi vardır","Okula gitmek","Ders çalışmak"],d:1,a:"Her insanın kendine göre bir bilgisi ve tecrübesi vardır küçümsenmemeli."}',
'{k:"Atasözleri",s:"Kervan yolda düzülür ne anlatır?",o:["Kervan sürmek","İşler yapılırken düzene girer","Yol yapmak","Seyahat etmek"],d:1,a:"Bir işe başlanıp yolda sorunlar çözülerek düzene sokulur."}',
'{k:"Atasözleri",s:"Meyve veren ağaç taşlanır ne demektir?",o:["Meyve toplamak","Başarılı insan kıskançlık ve saldırıya uğrar","Taş atmak","Ağaç dikmek"],d:1,a:"Başarılı ve üretken insanlar her zaman eleştiri ve kıskançlığa hedef olur."}',
'{k:"Atasözleri",s:"Gülü seven dikenine katlanır ne anlatır?",o:["Gül yetiştirmek","Sevdiğinin zorluklarına katlanırsın","Çiçek almak","Bahçe işi"],d:1,a:"Bir şeyi veya birini gerçekten seviyorsan zorluklarına da katlanmalısın."}',
'{k:"Atasözleri",s:"Taşıma suyla değirmen dönmez ne demektir?",o:["Su taşımak","Dışarıdan destekle sürdürülen iş kalıcı olmaz","Değirmen yapmak","Su bulmak"],d:1,a:"Kendi kaynağı olmayan dışarıdan destekle sürdürülen iş kalıcı olmaz."}',
'{k:"Atasözleri",s:"Kardeş kardeşi bıçaklar sofrada barışır ne anlatır?",o:["Kavga etmek","Aile bağları güçlüdür küslük sürmez","Yemek yemek","Bıçak kullanmak"],d:1,a:"Aile içi küsler uzun sürmez çünkü aile bağları güçlüdür."}',
'{k:"Atasözleri",s:"Aç ayı oynamaz ne demektir?",o:["Hayvanat bahçesi","Karşılığı olmayan iş için kimse çaba göstermez","Ayı beslemek","Sirk gösterisi"],d:1,a:"Karşılığını görmeden kimse emek harcamak istemez."}',
'{k:"Atasözleri",s:"Lafla peynir gemisi yürümez ne anlatır?",o:["Gemi kullanmak","Sadece konuşmayla iş olmaz eylem lazım","Peynir yapmak","Denizcilik"],d:1,a:"Sadece konuşarak iş yapılmaz harekete geçmek gerekir."}',
'{k:"Atasözleri",s:"Yarım doktor candan yarım hoca dinden eder ne demektir?",o:["Doktor olmak","Yarım bilgi tehlikelidir","Okula gitmek","Ders çalışmak"],d:1,a:"Eksik ve yarım bilgi tam bilmemekten daha tehlikelidir."}',
'{k:"Atasözleri",s:"Davulun sesi uzaktan hoş gelir ne anlatır?",o:["Müzik dinlemek","Uzaktan güzel görünen şey yakından öyle olmayabilir","Davul çalmak","Konser"],d:1,a:"Uzaktan güzel ve çekici görünen her şey yakınından bakıldığında öyle olmayabilir."}',
]

filepath = os.path.join("c:", os.sep, "Users", "safir", "OneDrive", "Masaüstü", "SmartCampusAI", "views", "_by_ortaokul.txt")

with open(filepath, "a", encoding="utf-8") as f:
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
