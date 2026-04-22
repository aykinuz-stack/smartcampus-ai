# -*- coding: utf-8 -*-
"""Kisisel Dil Gelisimi Almanca (KDG-DE) Engine - CEFR Uyumlu Diamond Premium Platform."""
import json
import os


def _load_german_cefr_data():
    """Load word and grammar JSON files."""
    base = os.path.join(os.path.dirname(__file__), "..", "data", "german")
    w_path = os.path.join(base, "cefr_words.json")
    g_path = os.path.join(base, "cefr_grammar.json")
    with open(w_path, "r", encoding="utf-8") as f:
        words = json.load(f)
    with open(g_path, "r", encoding="utf-8") as f:
        grammar = json.load(f)
    return words, grammar


def build_kdg_german_html(username: str = "misafir") -> str:
    """Kisisel Dil Gelisimi tam HTML/JS uygulamasi dondurur."""
    words, grammar = _load_german_cefr_data()
    wj = json.dumps(words, ensure_ascii=False)
    gj = json.dumps(grammar, ensure_ascii=False)
    u = username.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    return _KDG_CSS + _kdg_body(u, wj, gj)


def _kdg_body(username, words_js, grammar_js):
    return f'''<div id="kdg-app"></div>
<script>
(function(){{
"use strict";
var USER="{username}";
var WORDS={words_js};
var GRAMMAR={grammar_js};
var LEVELS=['A1','A2','B1','B2','C1','C2'];
var LINFO={{
A1:{{n:'Anfänger',t:'Baslangic',c:'#10b981',i:'\\ud83c\\udf31',r:0}},
A2:{{n:'Grundstufe',t:'Temel',c:'#06b6d4',i:'\\ud83d\\ude80',r:1}},
B1:{{n:'Mittelstufe',t:'Orta',c:'#3b82f6',i:'\\ud83d\\udcaa',r:2}},
B2:{{n:'Obere Mittelstufe',t:'Ust Orta',c:'#8b5cf6',i:'\\ud83d\\udd25',r:3}},
C1:{{n:'Fortgeschritten',t:'Ileri',c:'#ec4899',i:'\\u2b50',r:4}},
C2:{{n:'Meisterschaft',t:'Ustalik',c:'#f59e0b',i:'\\ud83d\\udc51',r:5}}
}};

// ===================== READING TEXTS =====================
var READINGS={{
A1:[
{{title:"Mein Tag",text:"Ich wache um sieben Uhr auf. Ich esse Fruhstuck. Ich gehe mit dem Bus zur Schule. Um zwolf Uhr esse ich Mittagessen. Nach der Schule spiele ich mit meinen Freunden. Am Abend mache ich meine Hausaufgaben. Um neun Uhr gehe ich ins Bett.",tr:"Yedide uyaniyorum. Kahvalti ediyorum. Otobusle okula gidiyorum. On ikide ogle yemegi yiyorum. Okuldan sonra arkadaslarimla oynuyorum. Aksam odevimi yapiyorum. Dokuzda yatiyorum.",qs:[{{q:"Saat kacta uyaniyur?",opts:["Alti","Yedi","Sekiz","Dokuz"],a:1}},{{q:"Okula nasil gidiyor?",opts:["Arabayla","Trenle","Otobusle","Yuruyerek"],a:2}},{{q:"Okuldan sonra ne yapiyor?",opts:["Uyuyor","Arkadaslariyla oynuyor","TV izliyor","Okuyor"],a:1}}]}},
{{title:"Meine Familie",text:"Ich heisse Ali. Ich habe eine grosse Familie. Mein Vater ist Lehrer. Meine Mutter ist Arztin. Ich habe eine Schwester und einen Bruder. Meine Schwester ist zehn Jahre alt. Mein Bruder ist funf.",tr:"Benim adim Ali. Buyuk bir ailem var. Babam ogretmen. Annem doktor. Bir kiz kardesim ve bir erkek kardesim var.",qs:[{{q:"Babanin meslegi ne?",opts:["Doktor","Ogretmen","Muhendis","Sofor"],a:1}},{{q:"Erkek kardesi kac yasinda?",opts:["Uc","Bes","Yedi","On"],a:1}},{{q:"Ailede kac cocuk var?",opts:["Bir","Iki","Uc","Dort"],a:1}}]}},
{{title:"Das Wetter",text:"Heute ist das Wetter schon. Die Sonne scheint. Es ist warm. Ich gehe in den Park. Die Kinder spielen dort. Die Vogel singen in den Baumen. Ich bin glucklich.",tr:"Bugun hava guzel. Gunes parliyor. Hava sicak. Parka gidiyorum. Cocuklar orada oynuyor. Kuslar agaclarda sarki soyluyor. Mutluyum.",qs:[{{q:"Hava nasil?",opts:["Yagmurlu","Gunesli","Karli","Bulutlu"],a:1}},{{q:"Nereye gidiyor?",opts:["Okula","Eve","Parka","Markete"],a:2}},{{q:"Kuslar ne yapiyor?",opts:["Ucuyor","Sarki soyluyor","Uyuyor","Yiyor"],a:1}}]}}
],
A2:[
{{title:"Im Supermarkt",text:"Gestern bin ich zum Supermarkt gegangen. Ich habe Brot, Milch und Obst gekauft. An der Kasse war eine lange Schlange. Ich habe mit Karte bezahlt. Zu Hause habe ich das Obst gewaschen und gegessen.",tr:"Dun supermarkete gittim. Ekmek, sut ve meyve aldim. Kasada uzun bir kuyruk vardi. Kartla odedim. Evde meyveleri yikadim ve yedim.",qs:[{{q:"Nereden alisveris yapmis?",opts:["Bakkal","Supermarket","Pazar","Online"],a:1}},{{q:"Nasil odemis?",opts:["Nakit","Kartla","Cekle","Havale"],a:1}},{{q:"Evde ne yapmis?",opts:["Pisirmis","Meyveleri yikayip yemis","Uyumus","TV izlemis"],a:1}}]}},
{{title:"Meine Reise nach Berlin",text:"Letzten Sommer bin ich nach Berlin gereist. Ich bin mit dem Zug gefahren. Die Reise hat drei Stunden gedauert. In Berlin habe ich das Brandenburger Tor und den Fernsehturm besucht. Das Essen war lecker.",tr:"Gecen yaz Berlin'e seyahat ettim. Trenle gittim. Yolculuk uc saat surdu. Berlin'de Brandenburg Kapisi'ni ve TV Kulesi'ni ziyaret ettim. Yemekler lezzetliydi.",qs:[{{q:"Nasil seyahat etmis?",opts:["Ucakla","Otobusle","Trenle","Arabayla"],a:2}},{{q:"Yolculuk ne kadar surmus?",opts:["Bir saat","Iki saat","Uc saat","Bes saat"],a:2}},{{q:"Berlin'de ne ziyaret etmis?",opts:["Muze","Brandenburg Kapisi","Stadyum","Universite"],a:1}}]}},
{{title:"Beim Arzt",text:"Ich hatte gestern Kopfschmerzen und bin zum Arzt gegangen. Der Arzt hat mich untersucht. Er hat gesagt, ich soll viel Wasser trinken und mich ausruhen. Er hat mir auch Medikamente verschrieben.",tr:"Dun basim agriyordu ve doktora gittim. Doktor beni muayene etti. Cok su icmemi ve dinlenmemi soyledi. Ayrica ilac yazdi.",qs:[{{q:"Neden doktora gitmis?",opts:["Karin agrisi","Bas agrisi","Dis agrisi","Sirt agrisi"],a:1}},{{q:"Doktor ne onermis?",opts:["Ameliyat","Su icmek ve dinlenmek","Spor yapmak","Diyet"],a:1}},{{q:"Doktor ayrica ne yapmis?",opts:["Kan almis","Ilac yazmis","Rontgen cekmis","Ameliyat onermis"],a:1}}]}}
],
B1:[
{{title:"Umweltschutz",text:"Der Umweltschutz ist heute wichtiger denn je. Wir mussen unseren Planeten schutzen. Recycling ist ein guter Anfang. Wir sollten auch weniger Plastik verwenden und mehr offentliche Verkehrsmittel benutzen. Jeder kann etwas fur die Umwelt tun.",tr:"Cevre koruma bugun her zamankinden daha onemli. Gezegenimizi korumaliyiz. Geri donusum iyi bir baslangic. Daha az plastik kullanmali ve daha cok toplu tasima kullanmaliyiz.",qs:[{{q:"Metnin ana konusu ne?",opts:["Seyahat","Cevre koruma","Egitim","Saglik"],a:1}},{{q:"Ne yapilmasi oneriliyor?",opts:["Daha cok araba kullanmak","Daha az plastik kullanmak","Hicbir sey yapmamak","Daha cok ucmak"],a:1}},{{q:"Cevre icin ne gerekiyor?",opts:["Bireysel caba","Isbirligi","Para","Teknoloji"],a:0}}]}},
{{title:"Das deutsche Schulsystem",text:"Das deutsche Schulsystem ist anders als in der Turkei. Nach der Grundschule gehen die Kinder in verschiedene Schultypen: Gymnasium, Realschule oder Hauptschule. Das Gymnasium dauert bis zur 12. oder 13. Klasse und bereitet auf das Studium vor.",tr:"Alman egitim sistemi Turkiye'den farklidir. Ilkokuldan sonra cocuklar farkli okul turlerine gider: Gymnasium, Realschule veya Hauptschule.",qs:[{{q:"Gymnasium'un amaci ne?",opts:["Meslek ogretmek","Universiteye hazirlamak","Spor egitimi","Sanat egitimi"],a:1}},{{q:"Kac farkli okul turu var?",opts:["Iki","Uc","Dort","Bes"],a:1}},{{q:"Hangi okul turu mevcut?",opts:["Gymnasium","College","Academy","Institute"],a:0}}]}}
],
B2:[
{{title:"Kunstliche Intelligenz",text:"Kunstliche Intelligenz verandert unsere Welt grundlegend. Von selbstfahrenden Autos bis zu medizinischen Diagnosen werden KI-Systeme immer leistungsfahiger. Allerdings wirft diese Entwicklung auch ethische Fragen auf. Wer ist verantwortlich, wenn eine KI einen Fehler macht?",tr:"Yapay zeka dunyamizi temelden degistiriyor. Otonom araclardan tibbi teshislere kadar yapay zeka sistemleri giderek daha guclu hale geliyor. Ancak bu gelisme etik sorulari da beraberinde getiriyor.",qs:[{{q:"Metnin ana konusu ne?",opts:["Cevre","Yapay zeka ve etik sorunlar","Saglik","Egitim"],a:1}},{{q:"Hangi sorun vurgulaniyor?",opts:["Maliyet","Hiz","Sorumluluk ve gizlilik","Enerji"],a:2}},{{q:"Toplumun ne yapmasi gerekiyor?",opts:["Beklemesi","Sorulari yanitlamasi","Teknolojiyi yasaklamasi","Hicbir sey"],a:1}}]}},
{{title:"Migration in Europa",text:"Migration ist eines der wichtigsten Themen in der europaischen Politik. Millionen Menschen verlassen ihre Heimat wegen Krieg, Armut oder Verfolgung. Die Integration dieser Menschen stellt die Aufnahmelander vor grosse Herausforderungen.",tr:"Goc, Avrupa siyasetinin en onemli konularindan biridir. Milyonlarca insan savas, yoksulluk veya zulum nedeniyle vatanlarini terk ediyor.",qs:[{{q:"Insanlar neden goc ediyor?",opts:["Tatil icin","Savas, yoksulluk, zulum","Egitim","Merak"],a:1}},{{q:"Gocmenler topluma nasil katkida bulunuyor?",opts:["Kulturel cesitlilik ve ekonomi","Spor","Siyaset","Bilim"],a:0}},{{q:"Ne tur bir yaklasim gerekli?",opts:["Kati","Dengeli","Gevsek","Kayitsiz"],a:1}}]}}
],
C1:[
{{title:"Die Zukunft der Arbeit",text:"Die Digitalisierung und Automatisierung verandern die Arbeitswelt tiefgreifend. Viele traditionelle Berufe werden durch kunstliche Intelligenz und Robotik ersetzt. Gleichzeitig entstehen neue Berufsfelder. Die lebenslange Weiterbildung wird zur Notwendigkeit.",tr:"Dijitallesme ve otomasyon is dunyasini koklu bir sekilde degistiriyor. Pek cok geleneksel meslek yapay zeka ve robotik tarafindan ikame ediliyor. Ayni zamanda yeni is alanlari ortaya cikiyor.",qs:[{{q:"Is dunyasini ne degistiriyor?",opts:["Dogal afetler","Dijitallesme ve otomasyon","Goc","Savaslar"],a:1}},{{q:"Ne zorunluluk haline geliyor?",opts:["Emeklilik","Yasam boyu egitim","Goc","Tasarruf"],a:1}},{{q:"Basari icin ne gerekli?",opts:["Sans","Uyum yetenegi","Zenginlik","Konum"],a:1}}]}},
{{title:"Philosophie des Glucks",text:"Was bedeutet Gluck? Philosophen beschaftigen sich seit Jahrtausenden mit dieser Frage. Aristoteles sah das Gluck in der Tugend. Die moderne positive Psychologie unterscheidet zwischen hedonischem und eudaimonischem Wohlbefinden.",tr:"Mutluluk ne demek? Filozoflar binlerce yildir bu soruyla ilgileniyor. Aristoteles mutlulugu erdemde goruyordu.",qs:[{{q:"Aristoteles'e gore mutluluk nerede?",opts:["Zevkte","Erdemde","Parada","Gucte"],a:1}},{{q:"Surdurulebilir mutluluk neden kaynaklaniyor?",opts:["Maddi varliklar","Anlamli iliskiler","Sohret","Guc"],a:1}},{{q:"Hangi iki refah turu arasinda ayrim yapiliyor?",opts:["Hedonik ve eudaimonik","Fiziksel ve zihinsel","Bireysel ve toplumsal","Ekonomik ve sosyal"],a:0}}]}}
],
C2:[
{{title:"Sprachphilosophie und Wirklichkeit",text:"Die Beziehung zwischen Sprache und Wirklichkeit ist ein zentrales Thema der analytischen Philosophie. Wittgenstein argumentierte, dass die Grenzen unserer Sprache die Grenzen unserer Welt bedeuten. Diese These wurde spater von der Sapir-Whorf-Hypothese aufgegriffen.",tr:"Dil ile gerceklik arasindaki iliski analitik felsefenin merkezi bir konusudur. Wittgenstein dilimizin sinirlarinin dunyamizin sinirlari anlamina geldigini savunmustur.",qs:[{{q:"Wittgenstein'a gore dil neyi belirler?",opts:["Duygulari","Dunyamizin sinirlarini","Zekayi","Hafizayi"],a:1}},{{q:"Sapir-Whorf hipotezi neyi savunur?",opts:["Tum diller aynidir","Dil yapisi dusunceyi etkiler","Dil gereksizdir","Dusunce dilden bagimsizdir"],a:1}},{{q:"Tartismanin etkiledigi alan hangisi?",opts:["Matematik","Epistemoloji","Fizik","Biyoloji"],a:1}}]}},
{{title:"Quantenmechanik und Determinismus",text:"Die Quantenmechanik hat unser Verstandnis der physikalischen Realitat grundlegend erschuttert. Heisenbergs Unscharferelation zeigt, dass Ort und Impuls eines Teilchens nicht gleichzeitig exakt bestimmt werden konnen. Dies stellt den klassischen Determinismus infrage.",tr:"Kuantum mekanigi fiziksel gerceklik anlayisimizi temelden sarsmistir. Heisenberg'in belirsizlik ilkesi, bir parcacigin konumu ve momentumunun ayni anda tam olarak belirlenemeyecegini gosterir.",qs:[{{q:"Heisenberg neyi gostermis?",opts:["Isik hizini","Konum ve momentumun ayni anda belirlenemeyecegini","Atomun yapisini","Kutlecekimi"],a:1}},{{q:"Einstein'in tavri neydi?",opts:["Kabul","Olasiliksal yorumu reddetme","Kayitsiz","Destekleme"],a:1}},{{q:"Bell deneyleri neyi kanitlamis?",opts:["Einstein hakli","Kuantum mekanigi dogru","Determinizm dogru","Hicbiri"],a:1}}]}}
]
}}


// ===================== WRITING PROMPTS =====================
var WPROMPTS={{
A1:["Ailenizi Almanca tanitin (5-8 cumle).","Odanizi Almanca tarif edin.","Her gun ne yaparsiniz? Gunluk rutininizi Almanca yazin.","En sevdiginiz yemegi Almanca anlatin.","En iyi arkadasinizi Almanca tarif edin.","Okulunuzu Almanca anlatin.","En sevdiginiz hayvani Almanca tarif edin.","Sehrinizi Almanca anlatin."],
A2:["Son tatilinizi Almanca anlatin (8-10 cumle).","En iyi arkadasinizi ve birlikte ne yaptiginizi Almanca yazin.","Hobinizi ve neden sevdiginizi Almanca anlatin.","Gecen hafta sonu ne yaptiniz? Almanca anlatin.","Bir mektup arkadasina kendinizi Almanca tanitin.","Yasadiginiz evi Almanca tarif edin.","Ulkenizdeki bir kutlamayi Almanca anlatin.","En sevdiginiz mevsimi Almanca anlatin.","Sevdiginiz bir ogretmeni Almanca tarif edin.","Buyudugunuzde ne olmak istiyorsunuz? Almanca yazin."],
B1:["Sosyal medyanin avantajlari ve dezavantajlari hakkinda Almanca yazin.","Unutulmaz bir seyahati Almanca anlatin.","Piyango kazansaniz ne yapardiniz? Almanca yazin.","Almanca ogrenmenin onemini Almanca yazin.","Okullar odev vermeli mi? Almanca fikirlerinizi yazin.","Fast foodun saglik uzerindeki etkilerini Almanca anlatin.","Hayatinizi etkileyen bir kisiyi Almanca anlatin.","Egitimde teknolojinin rolunu Almanca tartisin.","Buyuk sehirde yasmanin avantajlarini Almanca yazin.","Bir cevre sorununu Almanca anlatin ve cozum onerin."],
B2:["Teknolojinin egitim uzerindeki etkisini Almanca tartisin.","Medyanin kamuoyunu sekillendirmedeki rolunu Almanca anlatin.","Universite egitimi ucretsiz olmali mi? Her iki tarafi Almanca tartisin.","Kuresellesmenin yerel kulturler uzerindeki etkilerini Almanca analiz edin.","Hukumetler sosyal medyayi ne olcude kontrol etmeli? Almanca yazin.","Hayvan deneyleri cevresindeki etik sorunlari Almanca tartisin.","Modern sehirlerde cokkulturlulugun zorluklarini Almanca anlatin.","Ekonomik buyume ile mutluluk arasindaki iliskiyi Almanca analiz edin.","Oy kullanma zorunlu olmali mi? Almanca argumanlarinizi sunun.","Yapay zekanin is dunyasinin gelecegini Almanca yazin."],
C1:["Yapay zekanin modern saglik hizmetlerindeki rolunu Almanca degerlendirin.","Genetik muhendisliginin etik sonuclarini Almanca tartisin.","Hukumetler interneti ne olcude duzenlemeli? Almanca yazin.","Ekonomik buyume ile cevresel surdurulebilirlik arasindaki iliskiyi Almanca analiz edin.","Kuresellesmenin gelismis ulkelere daha fazla yarar sagladigi argumanini Almanca degerlendirin.","Sosyal medyanin demokratik surecleri guclendirip guclendirmedigini Almanca tartisin.","Uluslararasi orgutlerin barisi korumadaki etkinligini Almanca degerlendirin.","Otomasyonun istihdam uzerindeki etkisini Almanca analiz edin.","Egitimin sosyal hareketliligi tesvik etmedeki rolunu Almanca degerlendirin.","Uzay kolonizasyonunun felsefi sonuclarini Almanca tartisin."],
C2:["Yapay sistemlerde bilinc kavraminin felsefi sonuclarini Almanca inceleyin.","Dilin dusunceyi sekillendirdigi fikrini Almanca degerlendirin.","Demokratik toplumlarda bireysel ozgurluk ile kolektif sorumluluk arasindaki gerilimi Almanca tartisin.","Post-truth siyasetin epistemolojik zorluklarini Almanca analiz edin.","Neoliberal kapitalizme alternatif olarak kuculme kavramini Almanca analiz edin.","Anlatinin tarihsel gercekligi insa etmedeki rolunu Almanca inceleyin.","Bilimsel nesnelligin ulasilabilir olup olmadigini Almanca degerlendirin.","Otonom silah sistemlerine uygulanabilir etik cerceleri Almanca tartisin.","CRISPR teknolojisinin insan evrimi icin sonuclarini Almanca analiz edin.","Dilsel cesitlilik ile bilissel cesitlilik arasindaki iliskiyi Almanca inceleyin."]
}}


// ===================== TTS ENGINE (Kadin sesi, berrak, yavas) =====================
var ttsV=null,ttsR=false;
function initTTS(){{
  if(!window.speechSynthesis)return;
  function pick(){{var v=speechSynthesis.getVoices();
    // Oncelik: Kadin sesleri (net, berrak)
    var fem=['Microsoft Katja','Google Deutsch Female','Anna','Microsoft Hedda',
             'Petra','Sara','Marlene','Vicki','Google Deutsch','Google DE'];
    for(var i=0;i<fem.length;i++)for(var j=0;j<v.length;j++)
      if(v[j].name.indexOf(fem[i])!==-1&&v[j].lang.indexOf('de')===0){{ttsV=v[j];ttsR=true;return;}}
    // Fallback: herhangi bir Almanca kadin sesi (gender bilgisi varsa)
    for(var j=0;j<v.length;j++)if(v[j].lang.indexOf('de')===0&&v[j].name.toLowerCase().match(/female|woman|katja|hedda|anna|petra|sara|marlene|vicki/)){{ttsV=v[j];ttsR=true;return;}}
    // Son fallback: herhangi bir Almanca ses
    for(var j=0;j<v.length;j++)if(v[j].lang.indexOf('de')===0){{ttsV=v[j];ttsR=true;return;}}
    ttsR=true;
  }}
  if(speechSynthesis.getVoices().length)pick();
  speechSynthesis.onvoiceschanged=pick;
}}
initTTS();
var ttsRate=0.72;
function speak(text){{
  if(!window.speechSynthesis)return;speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance(text);u.lang='de-DE';u.rate=ttsRate;u.pitch=1.05;u.volume=1;
  if(ttsV)u.voice=ttsV;
  speechSynthesis.speak(u);
}}
function speakSlow(text){{
  if(!window.speechSynthesis)return;speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance(text);u.lang='de-DE';u.rate=0.55;u.pitch=1.05;u.volume=1;
  if(ttsV)u.voice=ttsV;
  speechSynthesis.speak(u);
}}

// ===================== STATE =====================
var TAB='dash';
var S={{
  level:'A1',cat:'',learnIdx:0,flipped:false,subTab:'',
  quiz:{{qs:[],cur:0,score:0,ans:false,sel:-1,type:'',timer:null,timeLeft:0,startTime:0}},
  readIdx:0,listenIdx:0,writeIdx:0,gramIdx:-1,
  dictText:'',dictInput:'',listenSpeed:0.72,
  speakIdx:0,phraseSub:'phrasal',recording:false,spokenText:'',
  placement:null
}};

// ===================== PROGRESS (localStorage) =====================
var PK='kdg_de_'+USER;
var P=loadP();
function loadP(){{try{{var d=localStorage.getItem(PK);return d?JSON.parse(d):initP();}}catch(e){{return initP();}}}}
function initP(){{return {{xp:0,streak:0,lastDate:'',levels:{{}},quizHistory:[],badges:[],placementDone:false,placementLevel:'',darkMode:false,timeSpent:{{}},writings:[]}};}}
function saveP(){{try{{localStorage.setItem(PK,JSON.stringify(P));}}catch(e){{}}}}
function getLP(lv){{if(!P.levels[lv])P.levels[lv]={{cats:{{}},gramDone:{{}},examPassed:false,examScore:0,wordsLearned:[]}};return P.levels[lv];}}
function isUnlocked(lv){{
  var idx=LEVELS.indexOf(lv);if(idx<=0)return true;
  var prev=LEVELS[idx-1];var lp=P.levels[prev];
  return lp&&lp.examPassed;
}}
function addXP(n){{P.xp+=n;checkStreak();checkBadges();saveP();}}
function checkStreak(){{
  var today=new Date().toISOString().slice(0,10);
  if(P.lastDate===today)return;
  var y=new Date();y.setDate(y.getDate()-1);var yd=y.toISOString().slice(0,10);
  if(P.lastDate===yd)P.streak++;else if(P.lastDate!==today)P.streak=1;
  P.lastDate=today;
}}
function checkBadges(){{
  var bs=P.badges;
  function ab(id){{if(bs.indexOf(id)===-1)bs.push(id);}}
  if(P.xp>=100)ab('xp100');if(P.xp>=500)ab('xp500');if(P.xp>=1000)ab('xp1k');if(P.xp>=5000)ab('xp5k');
  if(P.streak>=3)ab('s3');if(P.streak>=7)ab('s7');if(P.streak>=30)ab('s30');
  var tq=P.quizHistory.length;if(tq>=5)ab('q5');if(tq>=20)ab('q20');if(tq>=50)ab('q50');
  LEVELS.forEach(function(lv){{var lp=P.levels[lv];if(lp&&lp.examPassed)ab('pass_'+lv);}});
}}
// ===================== PLACEMENT TEST =====================
function genPlacement(){{
  var qs=[];
  // 4 questions per level (vocab + grammar mix), total 24
  LEVELS.forEach(function(lv){{
    var cats=WORDS[lv]?WORDS[lv].categories:{{}};var all=[];
    Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
    all=shuffle(all);
    // 2 vocab MCQ
    all.slice(0,2).forEach(function(w){{
      var opts=[w.t];var oth=all.filter(function(x){{return x.t!==w.t;}});oth=shuffle(oth);
      for(var i=0;i<3;i++)opts.push(oth[i%oth.length].t);
      opts=shuffle(opts);qs.push({{stem:w.e+' = ?',opts:opts,correct:opts.indexOf(w.t),lv:lv,type:'vocab'}});
    }});
    // 1 reverse (TR->EN)
    if(all.length>3){{
      var w=all[2];var opts2=[w.e];var oth2=all.filter(function(x){{return x.e!==w.e;}});oth2=shuffle(oth2);
      for(var j=0;j<3;j++)opts2.push(oth2[j%oth2.length].e);
      opts2=shuffle(opts2);qs.push({{stem:w.t+' = ? (Deutsch)',opts:opts2,correct:opts2.indexOf(w.e),lv:lv,type:'vocab'}});
    }}
    // 1 grammar
    var gs=GRAMMAR[lv]||[];
    if(gs.length){{
      var g=gs[Math.floor(Math.random()*gs.length)];
      var exs=g.exercises||[];
      if(exs.length){{
        var ex=exs[Math.floor(Math.random()*exs.length)];
        var correct=ex.a;var wrongs=[correct+'s',correct.split('').reverse().join(''),correct.replace(/\\w/,'_')];
        var gopts=[correct];wrongs.forEach(function(wr){{if(gopts.indexOf(wr)===-1&&gopts.length<4)gopts.push(wr);}});
        while(gopts.length<4)gopts.push('---');gopts=shuffle(gopts);
        qs.push({{stem:'['+lv+' Grammar] '+ex.q,opts:gopts,correct:gopts.indexOf(correct),lv:lv,type:'grammar'}});
      }}
    }}
  }});
  return qs;
}}
function calcPlacementLevel(answers){{
  // Score per level
  var scores={{}};LEVELS.forEach(function(l){{scores[l]=0;}});
  answers.forEach(function(a){{if(a.correct)scores[a.lv]++;}});
  // Find highest level with >=50% correct (2 out of 4)
  var result='A1';
  for(var i=LEVELS.length-1;i>=0;i--){{
    if(scores[LEVELS[i]]>=2){{result=LEVELS[i];break;}}
  }}
  return result;
}}
function renderPlacement(){{
  var pt=S.placement;
  if(!pt)return '';
  if(pt.done){{
    var lv=pt.result;var li=LINFO[lv];
    var o='<div style="text-align:center;padding:60px 20px">';
    o+='<div style="font-size:4rem;margin-bottom:16px">'+li.i+'</div>';
    o+='<div class="hd shm" style="font-size:2rem;margin-bottom:12px">Seviye Belirleme Tamamlandi!</div>';
    o+='<div style="font-size:1rem;color:var(--txt2);margin-bottom:8px">Dogru: <b>'+pt.score+'/'+pt.qs.length+'</b></div>';
    o+='<div style="display:inline-block;padding:12px 36px;border-radius:20px;background:'+li.c+';color:#fff;font-size:1.5rem;font-weight:900;margin:20px 0">'+lv+' - '+li.t+'</div>';
    o+='<div style="font-size:.88rem;color:var(--txt3);margin:16px 0 24px">Bu seviyeden baslamani oneriyoruz. Istersen degistirebilirsin.</div>';
    o+='<button class="btn btn-g" style="font-size:1rem;padding:14px 40px" onclick="finishPlacement()">Basla!</button>';
    o+='</div>';
    return o;
  }}
  var cur=pt.qs[pt.cur];
  var pct=Math.round((pt.cur+1)/pt.qs.length*100);
  var o='<div style="text-align:center;padding:20px">';
  o+='<div class="hd" style="font-size:1.3rem;color:var(--accent1);margin-bottom:8px">Seviye Belirleme Testi</div>';
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:16px">Soru '+(pt.cur+1)+'/'+pt.qs.length+'</div>';
  o+='<div class="pb pb-g" style="margin-bottom:20px;height:6px"><div class="fl" style="width:'+pct+'%"></div></div>';
  o+='<div style="display:inline-block;padding:3px 10px;border-radius:6px;background:rgba(99,102,241,.1);color:var(--accent1);font-size:.72rem;font-weight:700;margin-bottom:16px">'+cur.lv+' '+cur.type+'</div>';
  o+='<div class="qw"><div class="cd" style="padding:28px">';
  o+='<div class="qst">'+cur.stem+'</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(pt.ans){{cls+=' dis';if(i===cur.correct)cls+=' ok';else if(i===pt.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-pti="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(pt.ans){{
    o+='<div style="margin-top:16px"><button class="btn btn-g" onclick="placementNext()">'+
      (pt.cur<pt.qs.length-1?'Sonraki \\u2192':'Sonucu Gor')+'</button></div>';
  }}
  o+='</div></div>';
  return o;
}}

// ===================== DARK MODE =====================
function applyDark(){{
  var r=document.documentElement;
  if(P.darkMode){{
    r.style.setProperty('--bg','#0B0F19');r.style.setProperty('--card','#94A3B8');
    r.style.setProperty('--card2','#334155');r.style.setProperty('--txt','#1A2035');
    r.style.setProperty('--txt2','#cbd5e1');r.style.setProperty('--txt3','#64748b');
  }}else{{
    r.style.setProperty('--bg','#0B0F19');r.style.setProperty('--card','#ffffff');
    r.style.setProperty('--card2','#111827');r.style.setProperty('--txt','#0B0F19');
    r.style.setProperty('--txt2','#475569');r.style.setProperty('--txt3','#94a3b8');
  }}
}}

// ===================== TIME TRACKING =====================
var _timeStart=Date.now();
setInterval(function(){{
  var now=Date.now();var elapsed=Math.round((now-_timeStart)/1000);
  if(!P.timeSpent)P.timeSpent={{}};
  var today=new Date().toISOString().slice(0,10);
  P.timeSpent[today]=(P.timeSpent[today]||0)+1;
  _timeStart=now;
  if(elapsed%30===0)saveP();
}},1000);

// ===================== PHRASAL VERBS & IDIOMS DATA =====================
var PHRASAL_VERBS={{
A1:[{{pv:'aufwachen',tr:'uyanmak',ex:'Ich wache um sieben Uhr auf.'}},{{pv:'aufstehen',tr:'kalkmak',ex:'Sie steht fruh auf.'}},{{pv:'sich setzen',tr:'oturmak',ex:'Bitte setzen Sie sich.'}},{{pv:'anziehen',tr:'giymek',ex:'Zieh deinen Mantel an.'}},{{pv:'ausziehen',tr:'cikarmak',ex:'Zieh deine Schuhe aus.'}},{{pv:'anmachen',tr:'acmak',ex:'Mach den Fernseher an.'}},{{pv:'ausmachen',tr:'kapatmak',ex:'Mach das Licht aus.'}},{{pv:'anschauen',tr:'bakmak',ex:'Schau die Tafel an.'}},{{pv:'zuhoren',tr:'dinlemek',ex:'Hor dem Lehrer zu.'}},{{pv:'einkaufen',tr:'alisveris yapmak',ex:'Ich kaufe im Supermarkt ein.'}}],
A2:[{{pv:'suchen nach',tr:'aramak',ex:'Ich suche nach meinen Schlusseln.'}},{{pv:'aufgeben',tr:'pes etmek',ex:'Gib nicht auf!'}},{{pv:'abholen',tr:'almak',ex:'Hol mich bitte ab.'}},{{pv:'wegwerfen',tr:'atmak',ex:'Wirf den Mull weg.'}},{{pv:'zuruckkommen',tr:'geri donmek',ex:'Komm bald zuruck!'}},{{pv:'herausfinden',tr:'ogrenmek',ex:'Ich habe die Antwort herausgefunden.'}},{{pv:'weitermachen',tr:'devam etmek',ex:'Mach bitte weiter.'}},{{pv:'ausgehen',tr:'bitmek',ex:'Die Milch ist ausgegangen.'}},{{pv:'aufbauen',tr:'kurmak',ex:'Bau das Gerat auf.'}},{{pv:'trainieren',tr:'egzersiz yapmak',ex:'Ich trainiere jeden Tag.'}}],
B1:[{{pv:'ansprechen',tr:'gundeme getirmek',ex:'Sie hat einen guten Punkt angesprochen.'}},{{pv:'durchfuhren',tr:'uygulamak',ex:'Wir mussen den Plan durchfuhren.'}},{{pv:'sich befassen mit',tr:'ilgilenmek',ex:'Ich befasse mich mit diesem Problem.'}},{{pv:'nachgeben',tr:'boyun egmek',ex:'Sie hat schliesslich nachgegeben.'}},{{pv:'mithalten',tr:'ayak uydurmak',ex:'Halt mit der Klasse mit.'}},{{pv:'untersuchen',tr:'arastirmak',ex:'Wir werden das Problem untersuchen.'}},{{pv:'aufschieben',tr:'ertelemek',ex:'Schieb deine Hausaufgaben nicht auf.'}},{{pv:'ubernehmen',tr:'devralmak',ex:'Sie hat die Firma ubernommen.'}},{{pv:'teilnehmen an',tr:'katilmak',ex:'Ich nehme am Kurs teil.'}},{{pv:'sich vorbereiten auf',tr:'hazirlanmak',ex:'Ich bereite mich auf die Prufung vor.'}}],
B2:[{{pv:'zusammenbrechen',tr:'bozulmak/cokmek',ex:'Das Auto ist zusammengebrochen.'}},{{pv:'absagen',tr:'iptal etmek',ex:'Sie haben das Treffen abgesagt.'}},{{pv:'einschranken',tr:'azaltmak',ex:'Schranke den Zucker ein.'}},{{pv:'abbrechen',tr:'birakmak',ex:'Er hat die Schule abgebrochen.'}},{{pv:'scheitern',tr:'suya dusmek',ex:'Das Geschaft ist gescheitert.'}},{{pv:'davonkommen',tr:'yanina kar kalmak',ex:'Er ist damit davongekommen.'}},{{pv:'durchhalten',tr:'dayanmak',ex:'Halte einen Moment durch.'}},{{pv:'nachholen',tr:'telafi etmek',ex:'Ich werde die verlorene Zeit nachholen.'}},{{pv:'ertragen',tr:'katlanmak',ex:'Ich kann diesen Larm nicht ertragen.'}},{{pv:'ablehnen',tr:'reddetmek',ex:'Sie hat das Angebot abgelehnt.'}}],
C1:[{{pv:'ausmachen',tr:'olusturmak',ex:'Das macht den Unterschied aus.'}},{{pv:'bedenken',tr:'akilda tutmak',ex:'Bedenke die Frist.'}},{{pv:'hinauslaufen auf',tr:'oze inmek',ex:'Es lauft auf Geld hinaus.'}},{{pv:'auffrischen',tr:'tazelemek',ex:'Frische deine Grammatik auf.'}},{{pv:'wirken als',tr:'izlenimi vermek',ex:'Sie wirkt selbstbewusst.'}},{{pv:'abschaffen',tr:'ortadan kaldirmak',ex:'Sie haben die alten Regeln abgeschafft.'}},{{pv:'gerecht werden',tr:'karsilamak',ex:'Werde den Erwartungen gerecht.'}},{{pv:'eingrenzen',tr:'daraltmak',ex:'Grenze die Moglichkeiten ein.'}},{{pv:'ausschliessen',tr:'elemek',ex:'Wir konnen diese Moglichkeit nicht ausschliessen.'}},{{pv:'dammern',tr:'farkina varmak',ex:'Es dammerte mir plotzlich.'}}],
C2:[{{pv:'verblufft sein',tr:'sasirmak',ex:'Ich war von der Nachricht verblufft.'}},{{pv:'einbringen',tr:'kullanmak',ex:'Bring Erfahrung in das Problem ein.'}},{{pv:'ins Spiel kommen',tr:'devreye girmek',ex:'Andere Faktoren kommen ins Spiel.'}},{{pv:'beschonigen',tr:'goz ardi etmek',ex:'Beschonige die Probleme nicht.'}},{{pv:'ausarbeiten',tr:'halletmek',ex:'Wir haben eine Vereinbarung ausgearbeitet.'}},{{pv:'sich klammern an',tr:'yapisip kalmak',ex:'Sie klammerte sich an die Idee.'}},{{pv:'auslaufen lassen',tr:'kademe kademe kaldirmak',ex:'Sie haben das alte System auslaufen lassen.'}},{{pv:'herunterleiern',tr:'art arda sayip dokmek',ex:'Er hat eine Liste heruntergeleiert.'}},{{pv:'zuruckschrecken vor',tr:'cekinmek',ex:'Schrecke nicht vor Herausforderungen zuruck.'}},{{pv:'sich konzentrieren auf',tr:'odaklanmak',ex:'Konzentriere dich auf das Hauptproblem.'}}]
}}

var IDIOMS={{
A1:[{{idiom:'das Eis brechen',tr:'buzlari kirmak',ex:'Ein Witz kann das Eis brechen.',meaning:'Menschen sich wohler fuhlen lassen'}},{{idiom:'ein Kinderspiel',tr:'cok kolay',ex:'Die Prufung war ein Kinderspiel.',meaning:'Sehr einfach'}},{{idiom:'die Nase voll haben',tr:'bikmak',ex:'Ich habe die Nase voll.',meaning:'Genug von etwas haben'}},{{idiom:'Daumen drucken',tr:'basarilar dilemek',ex:'Ich drucke dir die Daumen!',meaning:'Jemandem Gluck wunschen'}},{{idiom:'den Nagel auf den Kopf treffen',tr:'tam isabetli konusmak',ex:'Du hast den Nagel auf den Kopf getroffen.',meaning:'Genau das Richtige sagen'}}],
A2:[{{idiom:'ins Gras beissen',tr:'olmek (argo)',ex:'Der Held hat ins Gras gebissen.',meaning:'Sterben (umgangssprachlich)'}},{{idiom:'die Katze aus dem Sack lassen',tr:'sirri aciga cikarmak',ex:'Er hat die Katze aus dem Sack gelassen.',meaning:'Ein Geheimnis verraten'}},{{idiom:'sich den Kopf zerbrechen',tr:'kafa yormak',ex:'Ich zerbreche mir den Kopf daruber.',meaning:'Intensiv nachdenken'}},{{idiom:'zwei Fliegen mit einer Klappe schlagen',tr:'bir tasla iki kus vurmak',ex:'Wir konnen zwei Fliegen mit einer Klappe schlagen.',meaning:'Zwei Dinge gleichzeitig erledigen'}},{{idiom:'alle Jubeljahre',tr:'kirk yilda bir',ex:'Wir gehen alle Jubeljahre essen.',meaning:'Sehr selten'}}],
B1:[{{idiom:'den Ball flach halten',tr:'sakin olmak',ex:'Wir sollten den Ball flach halten.',meaning:'Sich zuruckhalten'}},{{idiom:'die Nacht zum Tag machen',tr:'gece gec saatlere kadar calismak',ex:'Sie hat die Nacht zum Tag gemacht.',meaning:'Die ganze Nacht durcharbeiten'}},{{idiom:'kalte Fusse bekommen',tr:'son anda korkmak',ex:'Er hat kalte Fusse bekommen.',meaning:'Nervos und zogerlich werden'}},{{idiom:'eine Extrameile gehen',tr:'ekstra efor sarf etmek',ex:'Sie geht immer eine Extrameile.',meaning:'Mehr tun als erwartet'}},{{idiom:'den Anschluss verpassen',tr:'firsat kacirmak',ex:'Du hast den Anschluss verpasst.',meaning:'Eine Gelegenheit verpassen'}}],
B2:[{{idiom:'um den heissen Brei herumreden',tr:'lafi dolandirmak',ex:'Hor auf, um den heissen Brei herumzureden.',meaning:'Etwas nicht direkt sagen'}},{{idiom:'Abstriche machen',tr:'odun vermek',ex:'Mach keine Abstriche bei der Sicherheit.',meaning:'Kompromisse eingehen'}},{{idiom:'im selben Boot sitzen',tr:'ayni durumda olmak',ex:'Wir sitzen alle im selben Boot.',meaning:'In der gleichen Situation sein'}},{{idiom:'auf dem Zaun sitzen',tr:'kararsiz kalmak',ex:'Hor auf, auf dem Zaun zu sitzen.',meaning:'Keine Entscheidung treffen'}},{{idiom:'die Spitze des Eisbergs',tr:'buzdaginin gorunen kismi',ex:'Das ist nur die Spitze des Eisbergs.',meaning:'Ein kleiner Teil eines grosseren Problems'}}],
C1:[{{idiom:'auf dem Holzweg sein',tr:'yanlis yolda olmak',ex:'Du bist auf dem Holzweg.',meaning:'Sich irren'}},{{idiom:'in den sauren Apfel beissen',tr:'disini sikmak',ex:'Wir mussen in den sauren Apfel beissen.',meaning:'Etwas Unangenehmes ertragen'}},{{idiom:'ein zweischneidiges Schwert',tr:'iki ucu keskin bicak',ex:'Soziale Medien sind ein zweischneidiges Schwert.',meaning:'Etwas mit Vor- und Nachteilen'}},{{idiom:'den Teufel an die Wand malen',tr:'kotu seyleri ongormek',ex:'Mal nicht den Teufel an die Wand.',meaning:'Das Schlimmste befurchten'}},{{idiom:'der Elefant im Raum',tr:'gorunmeyen fil',ex:'Sprechen wir den Elefanten im Raum an.',meaning:'Ein offensichtliches Problem'}}],
C2:[{{idiom:'Hobsons Wahl',tr:'seceneksiz secenek',ex:'Es war Hobsons Wahl.',meaning:'Eine Wahl mit nur einer Option'}},{{idiom:'Pyrrhussieg',tr:'zarar veren zafer',ex:'Es war ein Pyrrhussieg.',meaning:'Ein Sieg, der zu viel kostet'}},{{idiom:'Zwickmuhle',tr:'cikmaz durum',ex:'Das ist eine echte Zwickmuhle.',meaning:'Eine paradoxe Situation ohne Ausweg'}},{{idiom:'Damoklesschwert',tr:'Demokles\\'in kilici',ex:'Die Frist hangt wie ein Damoklesschwert uber uns.',meaning:'Eine allgegenwartige Bedrohung'}},{{idiom:'die Buchse der Pandora',tr:'Pandora\\'nin kutusu',ex:'Dieses Thema ist die Buchse der Pandora.',meaning:'Eine Quelle vieler Probleme'}}]
}}


// ===================== READING GLOSSARY =====================
var GLOSSARY={{
A1:{{Tisch:'masa',Katze:'kedi',Morgen:'sabah',Schule:'okul',Bus:'otobus',Freund:'arkadas',Hausaufgaben:'odev',Abend:'aksam',Bett:'yatak',Wetter:'hava',sonnig:'gunesli',Garten:'bahce',Lehrer:'ogretmen',Haus:'ev',Familie:'aile',Buch:'kitap',Tag:'gun',Wasser:'su',Milch:'sut',Brot:'ekmek'}},
A2:{{Supermarkt:'supermarket',gestern:'dun',Zug:'tren',bequem:'konforlu',Telefon:'telefon',kaputt:'bozuk',Reise:'gezi',Wochenende:'hafta sonu',Arzt:'doktor',Kopfschmerzen:'bas agrisi',Medikament:'ilac',teuer:'pahali',Bibliothek:'kutuphane',Museum:'muze',Fahrkarte:'bilet',Flughafen:'havalimani',Hotel:'otel',bezahlen:'odemek',Schlange:'kuyruk',Karte:'kart'}},
B1:{{obwohl:'ragmen',Umwelt:'cevre',Recycling:'geri donusum',Plastik:'plastik',Schulsystem:'egitim sistemi',Grundschule:'ilkokul',Gymnasium:'lise',Abitur:'bitirme sinavi',Mitarbeiter:'calisan',Verantwortung:'sorumluluk',Erfahrung:'deneyim',Herausforderung:'zorluk',Gelegenheit:'firsat',nachhaltig:'surdurulebilir',Bildung:'egitim',Gesellschaft:'toplum',Pr\u00e4sentation:'sunum',Vorteil:'fayda',Gemeinschaft:'topluluk',wichtig:'onemli'}},
B2:{{beispiellos:'gorulmemis',Revolution:'devrim',gleichzeitig:'ayni anda',bedeutend:'onemli',Hypothese:'hipotez',autonom:'ozerk',Infrastruktur:'altyapi',empirisch:'deneysel',pragmatisch:'pragmatik',Migration:'goc',Verfolgung:'zulum',Integration:'entegrasyon',Vielfalt:'cesitlilik',Beitrag:'katki',ethisch:'etik',Diagnose:'teshis',Algorithmus:'algoritma',Daten:'veri',Privatsph\u00e4re:'gizlilik',K\u00fcnstliche:'yapay'}},
C1:{{Digitalisierung:'dijitallesme',Automatisierung:'otomasyon',Weiterbildung:'ileri egitim',Arbeitnehmer:'calisan',Regierung:'hukumet',Tugend:'erdem',Wohlbefinden:'refah',Philosophie:'felsefe',Gl\u00fcck:'mutluluk',Forschung:'arastirma',Bewusstsein:'bilinc',Nachhaltigkeit:'surdurulebilirlik',Gerechtigkeit:'adalet',Freiheit:'ozgurluk',Gleichheit:'esitlik',Demokratie:'demokrasi',Erkenntnis:'bilgi',Anpassungsf\u00e4higkeit:'uyum yetenegi',Sinnhaftigkeit:'anlamlilik',Selbstverwirklichung:'kendini gerceklestirme'}},
C2:{{erkenntnistheoretisch:'bilgi kuramsal',ontologisch:'varolussal',hermeneutisch:'yorumsal',dialektisch:'diyalektik',Quantenmechanik:'kuantum mekanigi',Wirklichkeit:'gerceklik',Sprachphilosophie:'dil felsefesi',Dekonstruktion:'yapisokum',Epistemologie:'epistemoloji',Paradigma:'paradigma',Diskurs:'soylem',Hegemonie:'hegemonya',Determinismus:'determinizm',Unsch\u00e4rferelation:'belirsizlik ilkesi',Ph\u00e4nomenologie:'fenomenoloji',Hermeneutik:'hermeneutik',Axiologie:'deger bilimi',Intersubjektivit\u00e4t:'oznelerarasilik',Performativit\u00e4t:'performativite',Metanarration:'ustanlati'}}
}}


function totalWordsForLevel(lv){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var t=0;
  Object.keys(cats).forEach(function(c){{t+=cats[c].length;}});return t;
}}
function learnedWordsForLevel(lv){{
  var lp=getLP(lv);return(lp.wordsLearned||[]).length;
}}
function totalWordsAll(){{var t=0;LEVELS.forEach(function(l){{t+=totalWordsForLevel(l);}});return t;}}
function learnedWordsAll(){{var t=0;LEVELS.forEach(function(l){{t+=learnedWordsForLevel(l);}});return t;}}
function catsDone(lv){{
  var lp=getLP(lv);var cats=WORDS[lv]?Object.keys(WORDS[lv].categories):[];
  var d=0;cats.forEach(function(c){{if(lp.cats[c]&&lp.cats[c].passed)d++;}});
  return {{done:d,total:cats.length}};
}}
function gramsDone(lv){{
  var lp=getLP(lv);var gs=GRAMMAR[lv]||[];var d=0;
  gs.forEach(function(g,i){{if(lp.gramDone[i])d++;}});
  return {{done:d,total:gs.length}};
}}
function levelPct(lv){{
  var cd=catsDone(lv),gd=gramsDone(lv);
  var total=cd.total+gd.total+1;
  var done=cd.done+gd.done+(getLP(lv).examPassed?1:0);
  return total>0?Math.round(done/total*100):0;
}}
function currentLevel(){{
  for(var i=LEVELS.length-1;i>=0;i--){{var lp=P.levels[LEVELS[i]];if(lp&&lp.examPassed)return LEVELS[Math.min(i+1,LEVELS.length-1)];}}
  return 'A1';
}}

// ===================== QUIZ GENERATORS =====================
function shuffle(a){{var b=a.slice();for(var i=b.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=b[i];b[i]=b[j];b[j]=t;}}return b;}}
function genCatQuiz(lv,cat){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var words=cats[cat]||[];if(!words.length)return[];
  var pool=shuffle(words).slice(0,10);var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  var qs=[];
  pool.forEach(function(w){{
    var opts=[w.t];var others=all.filter(function(x){{return x.t!==w.t;}});
    others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].t);
    var hint=w.p?'<br><span style="color:#f59e0b;font-size:.8em;font-style:italic">\\ud83d\\udde3 '+w.p+'</span>':'';
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udd0a '+w.e+hint+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w}});
  }});return qs;
}}
function genLevelQuiz(lv){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all);var pool=all.slice(0,20);var qs=[];
  pool.forEach(function(w,idx){{
    var pHint=w.p?'<br><span style="color:#f59e0b;font-size:.8em;font-style:italic">\\ud83d\\udde3 '+w.p+'</span>':'';
    var qtype=idx%4;
    if(qtype===0){{
      var isTF=Math.random()>0.5;
      var shown=isTF?w.t:all[Math.floor(Math.random()*all.length)].t;
      qs.push({{stem:'\\u2753 "'+w.e+'"'+pHint+' = "'+shown+'" — Dogru mu?',opts:['Dogru (True)','Yanlis (False)'],correct:isTF?0:1,word:w,qtype:'tf'}});
    }}else if(qtype===1){{
      var opts2=[w.e];var oth2=all.filter(function(x){{return x.e!==w.e;}});
      oth2=shuffle(oth2);for(var j=0;j<Math.min(3,oth2.length);j++)opts2.push(oth2[j].e);
      opts2=shuffle(opts2);qs.push({{stem:'\\ud83c\\uddf9\\ud83c\\uddf7 '+w.t+' = ?',opts:opts2,correct:opts2.indexOf(w.e),word:w,qtype:'reverse'}});
    }}else{{
      var opts=[w.t];var others=all.filter(function(x){{return x.t!==w.t;}});
      others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].t);
      opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udd0a '+w.e+pHint+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w,qtype:'mcq'}});
    }}
  }});return shuffle(qs);
}}
// ============ MATCHING QUIZ ============
function genMatchQuiz(lv){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all).slice(0,6);
  var left=all.map(function(w){{return w.e;}});
  var right=shuffle(all.map(function(w){{return w.t;}}));
  return {{left:left,right:right,answers:all,matched:{{}},total:all.length}};
}}
function genExam(lv){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all);var qs=[];
  all.slice(0,20).forEach(function(w){{
    var opts=[w.t];var others=all.filter(function(x){{return x.t!==w.t;}});
    others=shuffle(others);for(var i=0;i<3;i++)opts.push(others[i].t);
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udd24 '+w.e+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w}});
  }});
  var gs=GRAMMAR[lv]||[];shuffle(gs).slice(0,10).forEach(function(g){{
    var exs=g.exercises||[];if(!exs.length)return;
    var ex=exs[Math.floor(Math.random()*exs.length)];
    var correct=ex.a;var wrongs=[correct+'s',correct.split('').reverse().join(''),correct+' not'];
    var opts=[correct];wrongs.forEach(function(wr){{if(opts.indexOf(wr)===-1&&opts.length<4)opts.push(wr);}});
    while(opts.length<4)opts.push('---');
    opts=shuffle(opts);
    qs.push({{stem:'\\ud83d\\udcd6 '+ex.q,opts:opts,correct:opts.indexOf(correct)}});
  }});
  return shuffle(qs);
}}

// ===================== RENDER ENGINE =====================
var $=document.getElementById('kdg-app');
function h(tag,cls,inner,attrs){{var s='<'+tag;if(cls)s+=' class="'+cls+'"';if(attrs)s+=' '+attrs;s+='>'+inner+'</'+tag+'>';return s;}}
function render(){{
  // Placement test intercept
  if(S.placement&&!S.placement.finished){{
    $.innerHTML=renderPlacement();bindEvents();return;
  }}
  var o='';
  // TOPBAR with dark mode toggle
  o+=h('div','topbar',
    '<div style="display:flex;align-items:center;gap:10px">'+
    '<span style="font-size:1.5rem">\\ud83d\\udc8e</span>'+
    '<div><div class="logo-text">SmartCampus KDG</div><div class="logo-sub">CEFR DIAMOND EDITION</div></div></div>'+
    '<div class="uinfo" style="display:flex;align-items:center;gap:12px">'+
    '<span onclick="toggleDark()" style="cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:8px;background:rgba(99,102,241,.08);transition:all .2s" title="Karanlik/Aydinlik Mod">'+(P.darkMode?'\\u2600\\ufe0f':'\\ud83c\\udf19')+'</span>'+
    '\\ud83d\\udc64 <b>'+USER+'</b> &nbsp;|&nbsp; \\u2b50 <b>'+P.xp+'</b> XP &nbsp;|&nbsp; \\ud83d\\udd25 <b>'+P.streak+'</b> gun seri</div>'
  );
  // NAV TABS
  var tabs=[
    ['dash','\\ud83c\\udfe0','Dashboard'],['vocab','\\ud83d\\udcda','Vocabulary'],['grammar','\\ud83d\\udcd0','Grammar'],
    ['quiz','\\ud83c\\udfaf','Quiz Center'],['reading','\\ud83d\\udcd6','Reading'],['listening','\\ud83c\\udf99','Listening'],
    ['speaking','\\ud83c\\udfa4','Speaking'],['writing','\\u270d\\ufe0f','Writing'],['phrases','\\ud83d\\udcac','Phrases'],['progress','\\ud83d\\udcc8','Progress']
  ];
  var nt='<div class="ntabs">';
  tabs.forEach(function(t){{nt+=h('div','ntab'+(TAB===t[0]?' act':''),'<span class="tab-icon">'+t[1]+'</span> '+t[2],'onclick="goTab(\\''+t[0]+'\\')"');}});
  nt+='</div>';o+=nt;
  // CONTENT
  switch(TAB){{
    case'dash':o+=renderDash();break;
    case'vocab':o+=renderVocab();break;
    case'grammar':o+=renderGrammar();break;
    case'quiz':o+=renderQuiz();break;
    case'reading':o+=renderReading();break;
    case'listening':o+=renderListening();break;
    case'speaking':o+=renderSpeaking();break;
    case'writing':o+=renderWriting();break;
    case'phrases':o+=renderPhrases();break;
    case'progress':o+=renderProgress();break;
  }}
  $.innerHTML=o;bindEvents();
}}

// ===================== DASHBOARD =====================
function renderDash(){{
  var cl=currentLevel(),li=LINFO[cl];
  var tw=totalWordsAll(),lw=learnedWordsAll();
  var wpct=tw>0?Math.round(lw/tw*100):0;
  var o='';
  // Welcome banner with gradient
  o+='<div class="cd cd-gold fade-up" style="margin-bottom:24px;padding:28px 32px;border-radius:20px">';
  o+='<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px">';
  o+='<div><div class="hd shm" style="font-size:1.7rem;font-weight:900;letter-spacing:-.03em">Hos Geldin, '+USER+'!</div>';
  o+='<div style="color:var(--txt2);margin-top:8px;font-size:.88rem;font-weight:500">Mevcut Seviyen: <span style="display:inline-block;padding:3px 12px;border-radius:8px;font-weight:700;font-size:.8rem;color:#fff;background:'+li.c+'">'+cl+' - '+li.t+'</span></div></div>';
  o+='<div style="text-align:right"><div style="font-size:3.2rem;filter:drop-shadow(0 4px 8px rgba(0,0,0,.08))">'+li.i+'</div>';
  o+='<div style="font-size:.72rem;color:var(--txt3);font-weight:700;letter-spacing:2px;text-transform:uppercase">CEFR '+cl+'</div></div>';
  o+='</div>';
  if(!P.placementDone){{
    o+='<div style="margin-top:14px;padding:12px 16px;border-radius:12px;background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(236,72,153,.08));border:1px solid rgba(99,102,241,.15)">';
    o+='<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">';
    o+='<div style="font-size:.85rem;color:var(--accent1);font-weight:600">\\ud83c\\udfaf Seviyeni belirlemek icin test coz!</div>';
    o+='<button class="btn btn-g" style="font-size:.8rem;padding:8px 20px" onclick="startPlacement()">Seviye Testi Baslat</button>';
    o+='</div></div>';
  }}
  o+='</div>';
  // Stats row - modern gradient cards
  o+='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px">';
  var stats=[
    {{icon:'\\ud83d\\udcda',val:lw+'/'+tw,lbl:'Kelime',grad:'linear-gradient(135deg,#6366f1,#818cf8)',pct:wpct}},
    {{icon:'\\ud83c\\udfaf',val:P.quizHistory.length,lbl:'Quiz',grad:'linear-gradient(135deg,#8b5cf6,#a78bfa)',pct:0}},
    {{icon:'\\ud83d\\udd25',val:P.streak,lbl:'Gun Serisi',grad:'linear-gradient(135deg,#f59e0b,#fbbf24)',pct:0}},
    {{icon:'\\u2b50',val:P.xp,lbl:'Toplam XP',grad:'linear-gradient(135deg,#ec4899,#f472b6)',pct:0}}
  ];
  stats.forEach(function(st,si){{
    o+='<div class="cd fade-up" style="text-align:center;padding:22px 14px;animation-delay:'+(si*0.08)+'s;border-radius:18px">';
    o+='<div style="width:48px;height:48px;border-radius:14px;background:'+st.grad+';display:inline-flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:12px;box-shadow:0 4px 14px rgba(99,102,241,.2)">'+st.icon+'</div>';
    o+='<div style="font-family:\\'Plus Jakarta Sans\\',sans-serif;font-size:1.6rem;font-weight:900;color:var(--txt);margin-bottom:4px;letter-spacing:-.02em">'+st.val+'</div>';
    o+='<div style="font-size:.68rem;color:var(--txt3);text-transform:uppercase;letter-spacing:1.5px;font-weight:700">'+st.lbl+'</div>';
    if(st.pct>0){{
      o+='<div style="margin-top:10px;height:4px;background:rgba(0,0,0,.06);border-radius:2px;overflow:hidden"><div style="height:100%;width:'+st.pct+'%;background:'+st.grad+';border-radius:2px"></div></div>';
    }}
    o+='</div>';
  }});
  o+='</div>';
  // Level overview
  o+=h('div','shd',h('h3','hd','\\ud83c\\udf10 CEFR Seviye Haritasi'));
  o+='<div class="g3" style="margin-bottom:24px">';
  var lvColors=['linear-gradient(135deg,#10b981,#34d399)','linear-gradient(135deg,#06b6d4,#22d3ee)','linear-gradient(135deg,#3b82f6,#60a5fa)','linear-gradient(135deg,#8b5cf6,#a78bfa)','linear-gradient(135deg,#ec4899,#f472b6)','linear-gradient(135deg,#f59e0b,#fbbf24)'];
  LEVELS.forEach(function(lv,li3){{
    var li2=LINFO[lv],pct=levelPct(lv),ul=isUnlocked(lv);
    var lp=getLP(lv);
    var twl=totalWordsForLevel(lv),lwl=learnedWordsForLevel(lv);
    var gd2=gramsDone(lv);
    o+='<div class="cd lvc fade-up'+(ul?'':' lk')+'" data-lv="'+lv+'" style="animation-delay:'+(li3*0.06)+'s;border-radius:18px">';
    o+='<div style="display:inline-block;padding:8px 24px;border-radius:24px;font-weight:800;font-size:.92rem;color:#fff;margin-bottom:12px;background:'+lvColors[li3]+';box-shadow:0 4px 14px rgba(0,0,0,.12);letter-spacing:.02em">'+lv+'</div>';
    o+='<div style="font-size:.82rem;color:var(--txt2);margin-bottom:4px;font-weight:600">'+li2.i+' '+li2.t+'</div>';
    o+='<div style="font-size:.74rem;color:var(--accent1);font-weight:700;margin:6px 0">\\ud83d\\udcda '+twl+' kelime</div>';
    if(!ul){{
      o+='<div style="font-size:1.5rem;margin:12px 0;opacity:.6">\\ud83d\\udd12</div>';
      o+='<div style="font-size:.68rem;color:var(--txt3);font-weight:500">Onceki seviyeyi tamamla</div>';
    }}else{{
      o+='<div style="font-size:.72rem;color:var(--txt3);margin:6px 0;font-weight:500">'+lwl+'/'+twl+' kelime | '+gd2.done+'/'+gd2.total+' gramer</div>';
      o+='<div class="pb pb-g" style="margin:10px 0;height:8px"><div class="fl" style="width:'+pct+'%"></div></div>';
      o+='<div style="font-size:.72rem;font-weight:700;color:'+(pct>=100?'var(--grn)':'var(--txt2)')+'">%'+pct+(lp.examPassed?' \\u2705':'')+'</div>';
    }}
    o+='</div>';
  }});
  o+='</div>';
  // Quick actions - modern cards with icons
  o+=h('div','shd',h('h3','hd','\\u26a1 Hizli Erisim'));
  o+='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">';
  var actions=[
    {{tab:'vocab',icon:'\\ud83d\\udcda',name:'Kelime Calis',desc:'Flashcard ile kelime ogrenme',grad:'linear-gradient(135deg,#6366f1,#818cf8)'}},
    {{tab:'grammar',icon:'\\ud83d\\udcd0',name:'Gramer',desc:'Kural ve interaktif alistirmalar',grad:'linear-gradient(135deg,#8b5cf6,#a78bfa)'}},
    {{tab:'quiz',icon:'\\ud83c\\udfaf',name:'Quiz Coz',desc:'Bilgini test et, seviye atla',grad:'linear-gradient(135deg,#ec4899,#f472b6)'}},
    {{tab:'reading',icon:'\\ud83d\\udcd6',name:'Okuma',desc:'Seviyene uygun metinler',grad:'linear-gradient(135deg,#06b6d4,#22d3ee)'}},
    {{tab:'listening',icon:'\\ud83c\\udfa7',name:'Dinleme',desc:'5 farkli dinleme aktivitesi',grad:'linear-gradient(135deg,#f59e0b,#fbbf24)'}},
    {{tab:'writing',icon:'\\u270d\\ufe0f',name:'Yazma',desc:'Konu bazli yazma pratigi',grad:'linear-gradient(135deg,#10b981,#34d399)'}}
  ];
  actions.forEach(function(a,ai){{
    o+='<div class="cd fade-up" style="cursor:pointer;padding:22px;text-align:center;animation-delay:'+(ai*0.06)+'s;border-radius:18px" onclick="goTab(\\''+a.tab+'\\')">';
    o+='<div style="width:52px;height:52px;border-radius:16px;background:'+a.grad+';display:inline-flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:14px;box-shadow:0 6px 18px rgba(0,0,0,.1)">'+a.icon+'</div>';
    o+='<div style="font-size:.9rem;font-weight:700;color:var(--txt);margin-bottom:4px;letter-spacing:-.01em">'+a.name+'</div>';
    o+='<div style="font-size:.72rem;color:var(--txt3);font-weight:500">'+a.desc+'</div>';
    o+='</div>';
  }});
  o+='</div>';
  return o;
}}

// ===================== VOCABULARY =====================
function renderVocab(){{
  var lv=S.level,cats=WORDS[lv]?WORDS[lv].categories:{{}},catKeys=Object.keys(cats);
  var lp=getLP(lv);
  if(S.subTab==='learn')return renderFlashcard();
  if(S.subTab==='catQuizRun')return renderQuizRun();
  if(S.subTab==='catResult')return renderCatResult();
  var o='';
  // Level selector
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83d\\udcda '+lv+' Kelime Kategorileri ('+catsDone(lv).done+'/'+catsDone(lv).total+')'));
  o+='<div class="g2">';
  catKeys.forEach(function(c){{
    var words=cats[c];var cp=lp.cats[c]||{{}};var done=cp.passed;
    var lrn=(lp.wordsLearned||[]).filter(function(w){{return w.cat===c&&w.lv===lv;}}).length;
    o+='<div class="cd ctc'+(done?' ctd':'')+'" data-cat="'+c.replace(/"/g,'&quot;')+'" data-lv="'+lv+'">';
    o+='<div class="ce">'+c.split(' ').pop()+'</div>';
    o+='<div class="ci"><div class="cn">'+c.split(' ').slice(0,-1).join(' ')+'</div>';
    o+='<div class="cs">'+lrn+'/'+words.length+' ogrenildi</div></div>';
    o+='<span class="cb" style="background:'+(done?'rgba(76,175,80,.15);color:#81c784':'rgba(255,255,255,.08);color:var(--txt3)')+'">'+(done?'\\u2705 Tamam':'\\u25b6 Basla')+'</span>';
    o+='</div>';
  }});
  o+='</div>';
  return o;
}}

function renderFlashcard(){{
  var lv=S.level,cat=S.cat;
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var words=cats[cat]||[];
  if(!words.length){{S.subTab='';return renderVocab();}}
  var idx=S.learnIdx;if(idx>=words.length)idx=words.length-1;
  var w=words[idx];var lp=getLP(lv);
  var isLearned=(lp.wordsLearned||[]).some(function(x){{return x.e===w.e&&x.lv===lv;}});
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';render()">\\u2190 Kategoriler</button>';
  o+='<div style="text-align:center;margin:12px 0"><span class="hd" style="color:var(--gl);font-size:1.1rem">'+cat+'</span>';
  o+='<div style="color:var(--txt3);font-size:.78rem;margin-top:4px">'+(idx+1)+'/'+words.length+'</div></div>';
  o+='<div class="pb pb-g" style="margin-bottom:20px"><div class="fl" style="width:'+((idx+1)/words.length*100)+'%"></div></div>';
  o+='<div class="fcon">';
  var pron=w.p||'';
  if(!S.flipped){{
    o+='<div class="fcrd" onclick="flipCard()">';
    o+='<div class="fcl">DEUTSCH</div>';
    o+='<div class="fcw">'+w.e+'</div>';
    if(pron)o+='<div style="color:#f59e0b;font-size:.88rem;margin-top:6px;font-style:italic;letter-spacing:.5px">\\ud83d\\udde3 Okunu\\u015fu: '+pron+'</div>';
    o+='<div style="display:flex;gap:10px;justify-content:center;margin-top:10px">';
    o+='<span class="spk" onclick="event.stopPropagation();speak(\\''+w.e.replace(/'/g,"\\\\'")+'\\')" title="Normal hiz" style="cursor:pointer;font-size:1.3rem">\\ud83d\\udd0a</span>';
    o+='<span class="spk" onclick="event.stopPropagation();speakSlow(\\''+w.e.replace(/'/g,"\\\\'")+'\\')" title="Yavas dinle" style="cursor:pointer;font-size:1.1rem;opacity:.7">\\ud83d\\udc22</span>';
    o+='</div>';
    o+='<div class="fch">Karti cevirmek icin tikla</div></div>';
  }}else{{
    o+='<div class="fcrd" style="border-color:'+LINFO[lv].c+'">';
    o+='<div class="fcl">TURKCE</div>';
    o+='<div class="fcw" style="color:'+LINFO[lv].c+'">'+w.t+'</div>';
    o+='<div class="fce" style="color:var(--txt2);font-size:.9rem;margin-top:6px">'+w.e+'</div>';
    if(pron)o+='<div style="color:#f59e0b;font-size:.82rem;margin-top:4px;font-style:italic">\\ud83d\\udde3 '+pron+'</div>';
    o+='<div style="display:flex;gap:10px;justify-content:center;margin-top:8px">';
    o+='<span class="spk" onclick="event.stopPropagation();speak(\\''+w.e.replace(/'/g,"\\\\'")+'\\')" title="Normal hiz" style="cursor:pointer;font-size:1.2rem">\\ud83d\\udd0a</span>';
    o+='<span class="spk" onclick="event.stopPropagation();speakSlow(\\''+w.e.replace(/'/g,"\\\\'")+'\\')" title="Yavas dinle" style="cursor:pointer;font-size:1rem;opacity:.7">\\ud83d\\udc22</span>';
    o+='</div>';
    o+='</div>';
  }}
  o+='</div>';
  o+='<div class="fcb">';
  if(!S.flipped){{
    o+='<button class="btn btn-o" onclick="flipCard()">\\ud83d\\udd04 Cevir</button>';
  }}else{{
    o+='<button class="btn btn-rd" onclick="learnNext(false)">\\ud83d\\udd04 Tekrar</button>';
    o+='<button class="btn btn-gr" onclick="learnNext(true)">\\u2705 Biliyorum</button>';
  }}
  o+='</div>';
  if(idx>=words.length-1&&S.flipped){{
    o+='<div style="text-align:center;margin-top:20px">';
    o+='<button class="btn btn-g" onclick="startCatQuiz()">\\ud83c\\udfaf Quiz\\'e Gec (10 soru)</button></div>';
  }}
  return o;
}}

function renderQuizRun(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderVocab();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';render()">\\u2190 Vazgec</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="pb pb-g" style="margin-bottom:16px"><div class="fl" style="width:'+((q.cur+1)/q.qs.length*100)+'%"></div></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px">';
  o+='<div class="qst">'+cur.stem+'</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.correct)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-qi="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="quizNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishCatQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

function renderCatResult(){{
  var q=S.quiz;var passed=q.score>=7;
  if(passed){{
    var lp=getLP(S.level);if(!lp.cats[S.cat])lp.cats[S.cat]={{}};
    lp.cats[S.cat].passed=true;addXP(50);saveP();
  }}
  var o='<div class="rsc">';
  o+='<div class="ri">'+(passed?'\\ud83c\\udf89':'\\ud83d\\ude14')+'</div>';
  o+='<div class="rt hd" style="color:'+(passed?'#81c784':'#ef9a9a')+'">'+(passed?'TEBRIKLER!':'Tekrar Dene')+'</div>';
  o+='<div class="rv">'+q.score+'/'+q.qs.length+'</div>';
  o+='<div class="rm">'+(passed?'Kategoriyi basariyla tamamladin!':'Gecmek icin 7/10 dogru gerekli.')+'</div>';
  o+='<button class="btn btn-g" onclick="S.subTab=\\'\\';render()">\\u2190 Kategoriler</button>';
  o+='</div>';
  return o;
}}

// ===================== GRAMMAR =====================
function renderGrammar(){{
  var lv=S.level,gs=GRAMMAR[lv]||[];
  var lp=getLP(lv);
  var o='';
  // Level selector
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83d\\udcd6 '+lv+' Gramer Konulari ('+gramsDone(lv).done+'/'+gramsDone(lv).total+')'));
  o+='<div class="gram-scroll">';
  gs.forEach(function(g,i){{
    var done=lp.gramDone[i];
    o+='<div class="cd grc'+(done?' ctd':'')+'" style="margin-bottom:14px">';
    o+=h('h4','','\\ud83d\\udccc '+(i+1)+'. '+g.topic+(done?' \\u2705':''));
    o+='<div class="gru">'+g.rule+'</div>';
    o+='<div class="gre">'+g.explanation_tr+'</div>';
    if(g.examples){{
      g.examples.forEach(function(ex){{
        o+='<div class="grx"><b>'+ex.en+'</b> ';
        o+='<span class="spk spks" onclick="speak(\\''+ex.en.replace(/'/g,"\\\\'")+'\\')" title="Normal">\\ud83d\\udd0a</span> ';
        o+='<span class="spk spks" onclick="speakSlow(\\''+ex.en.replace(/'/g,"\\\\'")+'\\')" title="Yavas" style="opacity:.6;font-size:.8em">\\ud83d\\udc22</span>';
        o+='<br><span style="color:#888">'+ex.tr+'</span></div>';
      }});
    }}
    // Exercises
    if(g.exercises&&g.exercises.length){{
      var exTotal=g.exercises.length;
      var exDoneCount=0;
      if(lp.gramExDone&&lp.gramExDone[i]){{exDoneCount=Object.keys(lp.gramExDone[i]).length;}}
      o+='<div style="margin-top:12px;padding:12px;background:rgba(255,255,255,.03);border-radius:10px">';
      o+='<div style="font-size:.78rem;color:var(--gl);font-weight:700;margin-bottom:8px">\\u270d\\ufe0f Alistirmalar ('+exDoneCount+'/'+exTotal+')</div>';
      g.exercises.forEach(function(ex,ei){{
        var eid='ge_'+i+'_'+ei;
        var exAlreadyDone=(lp.gramExDone&&lp.gramExDone[i]&&lp.gramExDone[i][ei]);
        var exType=ei%3; // 0=fill_blank, 1=MCQ, 2=error_correction
        o+='<div style="margin-bottom:10px;font-size:.85rem;padding:8px;border-radius:8px;background:rgba(99,102,241,.02)" id="wrap_'+eid+'">';
        if(exAlreadyDone){{
          o+='<span style="color:#888">'+(ei+1)+'. '+ex.q+'</span> ';
          o+='<input class="gin ok" value="'+ex.a.replace(/"/g,'&quot;')+'" disabled style="color:#81c784;font-weight:600"> \\u2705';
        }}else if(exType===1){{
          // MCQ type
          var mcqOpts=[ex.a];
          var wrongs=[ex.a+'s',ex.a+'ing',ex.a.length>3?ex.a.substring(0,ex.a.length-1)+'ed':'not '+ex.a,'the '+ex.a];
          wrongs.forEach(function(w){{if(mcqOpts.indexOf(w)===-1&&w!==ex.a&&mcqOpts.length<4)mcqOpts.push(w);}});
          while(mcqOpts.length<4)mcqOpts.push('---');
          mcqOpts=shuffle(mcqOpts);
          var correctMcq=mcqOpts.indexOf(ex.a);
          o+='<span style="color:#888">'+(ei+1)+'. '+ex.q+' <span style="font-size:.68rem;color:var(--accent2);font-weight:700">[MCQ]</span></span>';
          o+='<div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap">';
          mcqOpts.forEach(function(opt,oi){{
            o+='<div class="qo" style="padding:6px 14px;font-size:.82rem;display:inline-block;flex:none" data-gmcq="'+eid+'" data-gmi="'+oi+'" data-gmc="'+correctMcq+'" data-ggidx="'+i+'">'+String.fromCharCode(65+oi)+') '+opt+'</div>';
          }});
          o+='</div>';
        }}else if(exType===2){{
          // Error correction type
          var wrongSent=ex.q.replace('___','<b style="color:var(--red);text-decoration:underline wavy var(--red)">'+ex.a+'ed</b>');
          o+='<span style="color:#888">'+(ei+1)+'. Cumledeki hatayi bulun ve dogrusunu yazin: <span style="font-size:.68rem;color:var(--accent3);font-weight:700">[Error Fix]</span></span>';
          o+='<div style="padding:8px 12px;background:rgba(239,68,68,.04);border-radius:8px;margin:6px 0;font-size:.85rem;border-left:3px solid var(--red)">'+ex.q.replace('___','<b style="color:var(--red)">______</b>')+'</div>';
          o+='<input class="gin" id="'+eid+'" data-ans="'+ex.a.replace(/"/g,'&quot;')+'" placeholder="Dogru kelimeyi yaz..." onkeypress="if(event.key===\\'Enter\\')checkGramEx(\\''+eid+'\\','+i+')">';
          o+=' <button class="btn btn-o" style="padding:4px 12px;font-size:.75rem" onclick="checkGramEx(\\''+eid+'\\','+i+')">\\u2714</button>';
        }}else{{
          // Original fill_blank type
          o+='<span style="color:#888">'+(ei+1)+'. '+ex.q+' <span style="font-size:.68rem;color:var(--accent4);font-weight:700">[Fill]</span></span> ';
          o+='<input class="gin" id="'+eid+'" data-ans="'+ex.a.replace(/"/g,'&quot;')+'" placeholder="cevap..." onkeypress="if(event.key===\\'Enter\\')checkGramEx(\\''+eid+'\\','+i+')">';
          o+=' <button class="btn btn-o" style="padding:4px 12px;font-size:.75rem" onclick="checkGramEx(\\''+eid+'\\','+i+')">\\u2714</button>';
        }}
        o+='</div>';
      }});
      o+='</div>';
    }}
    o+='</div>';
  }});
  o+='</div>';
  return o;
}}

// ===================== QUIZ CENTER =====================
function renderQuiz(){{
  if(S.subTab==='quizRun')return renderQuizRunGeneric();
  if(S.subTab==='examRun')return renderExamRun();
  if(S.subTab==='quizResult')return renderQuizResult();
  if(S.subTab==='examResult')return renderExamResult();
  if(S.subTab==='matchRun')return renderMatchQuiz();
  if(S.subTab==='srRun')return renderSRQuiz();
  var lv=S.level;
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83c\\udfaf '+lv+' Quiz Center'));
  o+='<div class="g3">';
  // Category quiz
  o+='<div class="cd" style="text-align:center;padding:24px;cursor:pointer" onclick="startLevelQuiz(\\'cat\\')">';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">\\ud83d\\udcda</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Category Quiz</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">Rastgele kategoriden 10 soru</div></div>';
  // Level quiz (mixed: MCQ + True/False + Reverse)
  o+='<div class="cd" style="text-align:center;padding:24px;cursor:pointer" onclick="startLevelQuiz(\\'level\\')">';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">\\ud83c\\udfaf</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Mixed Quiz</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">MCQ + True/False + Reverse (20 soru)</div></div>';
  // Matching quiz
  o+='<div class="cd" style="text-align:center;padding:24px;cursor:pointer" onclick="startMatchQuiz()">';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">\\ud83d\\udd17</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Matching</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">6 kelimeyi eslestir (EN \\u2194 TR)</div></div>';
  // Spaced repetition
  var srCount=getSRWords().length;
  o+='<div class="cd" style="text-align:center;padding:24px;cursor:pointer" onclick="startSRQuiz()">';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">\\ud83e\\udde0</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Spaced Repetition</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">Tekrar gereken: <b>'+srCount+'</b> kelime</div></div>';
  // Weak area quiz
  o+='<div class="cd" style="text-align:center;padding:24px;cursor:pointer" onclick="startWeakQuiz()">';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">\\ud83d\\udcc9</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Weak Areas</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">Zayif alanlarina odaklan</div></div>';
  // Level exam
  var cd=catsDone(lv),gd=gramsDone(lv);
  var examReady=cd.done>=Math.ceil(cd.total*0.5);
  var lp=getLP(lv);
  o+='<div class="cd'+(examReady?'':' lk')+'" style="text-align:center;padding:24px;'+(examReady?'cursor:pointer':'cursor:not-allowed;opacity:.5')+'" '+(examReady?'onclick="startExam()"':'')+'>';
  o+='<div style="font-size:2.5rem;margin-bottom:10px">'+(lp.examPassed?'\\ud83c\\udfc6':'\\ud83d\\udcdd')+'</div>';
  o+='<div class="hd" style="color:var(--gl);font-size:1rem;margin-bottom:6px">Level Exam</div>';
  o+='<div style="font-size:.78rem;color:var(--txt3)">'+(lp.examPassed?'Gecildi! ('+lp.examScore+' puan) - Tekrar coz':'30 soru, %70 gecme, 15 dk')+'</div></div>';
  o+='</div>';
  // Quiz history
  if(P.quizHistory.length){{
    o+=h('div','shd',h('h3','hd','\\ud83d\\udcca Son Quizler'));
    o+='<div style="overflow-x:auto"><table style="width:100%;font-size:.82rem;border-collapse:collapse">';
    o+='<tr style="color:var(--txt3);border-bottom:1px solid rgba(255,255,255,.06)"><th style="padding:8px;text-align:left">Tarih</th><th>Seviye</th><th>Tur</th><th>Skor</th><th>Sonuc</th></tr>';
    P.quizHistory.slice(-10).reverse().forEach(function(qh){{
      var passed=qh.score>=qh.total*0.7;
      o+='<tr style="border-bottom:1px solid rgba(255,255,255,.04)">';
      o+='<td style="padding:6px 8px">'+qh.date+'</td><td style="text-align:center">'+qh.level+'</td>';
      o+='<td style="text-align:center">'+qh.type+'</td><td style="text-align:center">'+qh.score+'/'+qh.total+'</td>';
      o+='<td style="text-align:center;color:'+(passed?'#81c784':'#ef9a9a')+'">'+(passed?'\\u2705':'\\u274c')+'</td></tr>';
    }});
    o+='</table></div>';
  }}
  return o;
}}

function renderQuizRunGeneric(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderQuiz();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Vazgec</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="pb pb-g" style="margin-bottom:16px"><div class="fl" style="width:'+((q.cur+1)/q.qs.length*100)+'%"></div></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px">';
  o+='<div class="qst">'+cur.stem+'</div><div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.correct)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-qi="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="quizNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

function renderExamRun(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderQuiz();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="abandonExam()">\\u2190 Vazgec</button>';
  var mins=Math.floor(q.timeLeft/60),secs=q.timeLeft%60;
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;align-items:center">';
  o+='<span style="font-size:.82rem">Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+' | Dogru: <b style="color:#81c784">'+q.score+'</b></span>';
  o+='<span id="exam-timer" style="font-size:1rem;font-weight:700;color:var(--org)">\\u23f1 '+mins+':'+(secs<10?'0':'')+secs+'</span></div>';
  o+='<div class="pb pb-g" style="margin-bottom:16px"><div class="fl" style="width:'+((q.cur+1)/q.qs.length*100)+'%"></div></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px">';
  o+='<div class="qst">'+cur.stem+'</div><div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.correct)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-qi="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="quizNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishExam()">Sinavi Bitir</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

function renderQuizResult(){{
  var q=S.quiz;var passed=q.score>=Math.ceil(q.qs.length*0.7);
  var o='<div class="rsc">';
  o+='<div class="ri">'+(passed?'\\ud83c\\udf89':'\\ud83d\\ude14')+'</div>';
  o+='<div class="rt hd" style="color:'+(passed?'#81c784':'#ef9a9a')+'">'+(passed?'Harika!':'Daha fazla calis!')+'</div>';
  o+='<div class="rv">'+q.score+'/'+q.qs.length+'</div>';
  o+='<div class="rm">'+S.level+' '+q.type+' tamamlandi.</div>';
  o+='<button class="btn btn-g" onclick="S.subTab=\\'\\';render()">\\u2190 Quiz Merkezi</button>';
  o+='</div>';
  return o;
}}

function renderExamResult(){{
  var q=S.quiz;var total=q.qs.length;var passed=q.score>=Math.ceil(total*0.7);
  if(passed){{
    var lp=getLP(S.level);lp.examPassed=true;lp.examScore=q.score;addXP(200);saveP();
  }}
  var o='<div class="rsc">';
  o+='<div class="ri">'+(passed?'\\ud83c\\udfc6':'\\ud83d\\udcdd')+'</div>';
  o+='<div class="rt hd" style="color:'+(passed?'var(--gl)':'#ef9a9a')+'">'+(passed?S.level+' SEVIYE GECILDI!':'Tekrar Dene')+'</div>';
  o+='<div class="rv">'+q.score+'/'+total+'</div>';
  o+='<div class="rm">'+(passed?'Tebrikler! '+S.level+' seviyesini basariyla tamamladin!':'Gecmek icin %70 dogru gerekli ('+Math.ceil(total*0.7)+'/'+total+')')+'</div>';
  o+='<button class="btn btn-g" onclick="S.subTab=\\'\\';render()">\\u2190 Quiz Merkezi</button>';
  o+='</div>';
  return o;
}}

// ===================== READING =====================
function renderReading(){{
  var lv=S.level;var texts=READINGS[lv]||[];
  if(S.subTab==='readText')return renderReadText();
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83d\\udcd6 '+lv+' Okuma Metinleri'));
  if(!texts.length){{o+='<div class="cd" style="text-align:center;padding:30px;color:var(--txt3)">Bu seviye icin metin yakinda eklenecek.</div>';return o;}}
  o+='<div class="g2">';
  texts.forEach(function(t,i){{
    o+='<div class="cd ctc" onclick="openReading('+i+')">';
    o+='<div class="ce">\\ud83d\\udcd6</div>';
    o+='<div class="ci"><div class="cn">'+t.title+'</div>';
    o+='<div class="cs">'+t.text.split(' ').length+' kelime | '+t.qs.length+' soru</div></div>';
    o+='</div>';
  }});
  o+='</div>';
  return o;
}}

function renderReadText(){{
  var lv=S.level;var texts=READINGS[lv]||[];var t=texts[S.readIdx];
  if(!t){{S.subTab='';return renderReading();}}
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';render()">\\u2190 Metinler</button>';
  o+='<div class="hd" style="color:var(--gl);font-size:1.15rem;margin:12px 0;text-align:center">'+t.title+'</div>';
  // Make words clickable for glossary
  var glossary=GLOSSARY[lv]||{{}};
  var textWithGloss=t.text.replace(/\\b([A-Za-z]+)\\b/g,function(match){{
    var low=match.toLowerCase();
    if(glossary[low]){{
      return '<span class="gloss-word" data-word="'+match+'" data-tr="'+glossary[low]+'" title="'+glossary[low]+'">'+match+'</span>';
    }}
    return match;
  }});
  o+='<div class="cd rtx" style="margin-bottom:16px">'+textWithGloss;
  o+='<br><button class="spk" onclick="speak(\\''+t.text.replace(/'/g,"\\\\'").substring(0,200)+'\\')" style="margin-top:10px" title="Dinle">\\ud83d\\udd0a</button>';
  o+='<div id="gloss-popup" style="display:none;position:absolute;padding:10px 16px;background:var(--card);border:1.5px solid var(--accent1);border-radius:10px;box-shadow:var(--shadow-lg);font-size:.82rem;z-index:99;max-width:250px"><div id="gloss-en" style="font-weight:700;color:var(--accent1)"></div><div id="gloss-tr" style="color:var(--txt2);margin-top:3px"></div><span class="spk spks" id="gloss-speak" style="margin-top:4px;display:inline-block" title="Dinle">\\ud83d\\udd0a</span></div>';
  o+='</div>';
  o+='<div class="cd" style="margin-bottom:16px;padding:14px;background:rgba(255,255,255,.02)">';
  o+='<div style="font-size:.78rem;color:var(--txt3);margin-bottom:6px">\\ud83c\\uddf9\\ud83c\\uddf7 Turkce Ceviri</div>';
  o+='<div style="font-size:.85rem;color:#999;line-height:1.7">'+t.tr+'</div></div>';
  // Comprehension questions
  o+=h('div','shd',h('h3','hd','\\u2753 Anlama Sorulari'));
  t.qs.forEach(function(q,qi){{
    o+='<div class="cd" style="margin-bottom:10px;padding:14px" id="rq_'+qi+'">';
    o+='<div style="font-size:.88rem;color:var(--gl);margin-bottom:10px">'+(qi+1)+'. '+q.q+'</div>';
    o+='<div class="qop">';
    q.opts.forEach(function(opt,oi){{
      o+='<div class="qo" data-rqi="'+qi+'" data-roi="'+oi+'" data-ra="'+q.a+'">'+String.fromCharCode(65+oi)+') '+opt+'</div>';
    }});
    o+='</div></div>';
  }});
  return o;
}}

// ===================== LISTENING DATA =====================
var LISTEN_SENT={{}};
LISTEN_SENT['A1']=[
  {{s:"Die Katze ist auf dem Tisch.",q:"Kedi nerede?",opts:["Masanin ustunde","Yerde","Sandalyede","Yatagda"],a:0}},
  {{s:"Ich hei\u00dfe Johann und ich bin Lehrer.",q:"Johann ne is yapiyor?",opts:["Ogretmen","Doktor","Muhendis","Asci"],a:0}},
  {{s:"Ich wache jeden Morgen um sieben Uhr auf.",q:"Saat kacta kalkiyor?",opts:["7","8","6","9"],a:0}},
  {{s:"Sie mag \u00c4pfel und Orangen.",q:"O ne sever?",opts:["Elma ve portakal","Muz ve cilek","Uzum ve karpuz","Armut ve seftali"],a:0}},
  {{s:"Das Wetter ist heute sonnig.",q:"Hava nasil?",opts:["Gunesli","Yagmurlu","Bulutlu","Karli"],a:0}},
  {{s:"Es gibt drei B\u00fccher im Regal.",q:"Rafta kac kitap var?",opts:["3","2","5","4"],a:0}},
  {{s:"Ich fahre mit dem Bus zur Schule.",q:"Okula nasil gidiyor?",opts:["Otobusle","Yuruyerek","Arabayla","Bisikletle"],a:0}},
  {{s:"Wir essen um acht Uhr abends zu Abend.",q:"Aksam yemegi saat kacta?",opts:["8","7","9","6"],a:0}}
];
LISTEN_SENT['A2']=[
  {{s:"Ich bin gestern zum Supermarkt gegangen und habe Milch und Brot gekauft.",q:"Dun nereye gitti?",opts:["Supermarkete","Okula","Hastaneye","Parka"],a:0}},
  {{s:"Sie tr\u00e4gt ein blaues Kleid, weil es ihre Lieblingsfarbe ist.",q:"En sevdigi renk ne?",opts:["Mavi","Kirmizi","Yesil","Sari"],a:0}},
  {{s:"Der Zug f\u00e4hrt um halb zehn von Gleis zwei ab.",q:"Tren saat kacta kalkiyor?",opts:["9:30","9:00","10:30","8:30"],a:0}},
  {{s:"Mein Bruder ist gr\u00f6\u00dfer als ich, aber ich bin schneller.",q:"Kim daha hizli?",opts:["Ben","Erkek kardesim","Ikisi de esit","Belli degil"],a:0}},
  {{s:"Der Film beginnt um sieben und endet um halb zehn.",q:"Film ne kadar suruyor?",opts:["2.5 saat","2 saat","3 saat","1.5 saat"],a:0}}
];
LISTEN_SENT['B1']=[
  {{s:"Obwohl es stark regnete, beschlossen wir, im Park spazieren zu gehen.",q:"Neden yuruyuse ciktilar?",opts:["Butun gun icerde kaldilar","Hava guzeldi","Doktor onerdi","Kosuya gideceklerdi"],a:0}},
  {{s:"Sie lernt seit drei Jahren Deutsch und kann jetzt ein Gespr\u00e4ch f\u00fchren.",q:"Kac yildir Almanca ogreniyor?",opts:["3","5","2","1"],a:0}},
  {{s:"Das Unternehmen hat angek\u00fcndigt, f\u00fcnfzig neue Mitarbeiter einzustellen.",q:"Kac yeni calisan ise alinacak?",opts:["50","30","100","25"],a:0}},
  {{s:"Ich reise lieber mit dem Zug, weil es bequemer ist.",q:"Neden treni tercih ediyor?",opts:["Daha konforlu","Daha ucuz","Daha hizli","Daha guvenli"],a:0}},
  {{s:"Das Museum ist jeden Tag au\u00dfer Montag ge\u00f6ffnet.",q:"Muze ne zaman kapali?",opts:["Pazartesi","Sali","Pazar","Cuma"],a:0}}
];
LISTEN_SENT['B2']=[
  {{s:"Trotz des wirtschaftlichen Abschwungs gelang es dem Startup, Finanzierung zu sichern.",q:"Startup neden fon alabildi?",opts:["Yenilikci yaklasimi","Dusuk maliyetleri","Buyuk musteri portfoyu","Hukumet destegi"],a:0}},
  {{s:"Forschungen zeigen, dass regelm\u00e4\u00dfiger Sport bessere psychische Gesundheit bringt.",q:"Egzersizin etkisi nedir?",opts:["Daha yuksek verimlilik","Etkisi yok","Azaltir","Belirsiz"],a:0}},
  {{s:"Der Konferenzredner betonte, dass k\u00fcnstliche Intelligenz die Gesundheitsbranche ver\u00e4ndern wird.",q:"Konusmaci ne hakkinda konusuyor?",opts:["Yapay zekanin saglik sektorunu donusturmesi","Egitim reformu","Iklim degisikligi","Ekonomik buyume"],a:0}}
];
LISTEN_SENT['C1']=[
  {{s:"Die Auswirkungen des Quantencomputings auf die Cybersicherheit sind tiefgreifend.",q:"Kuantum bilgisayarlarin tehdidi nedir?",opts:["Mevcut sifreleme yontemlerini kirabilir","Cok pahali","Enerji tuketiyor","Yavas calisir"],a:0}},
  {{s:"Die philosophische Debatte \u00fcber Bewusstsein wurde durch neurowissenschaftliche Fortschritte wiederbelebt.",q:"Norolojik bulgular ne one suruyor?",opts:["Kararlarimiz noral aktivite tarafindan belirlenebilir","Ozgur irade kesin","Bilinc olculemez","Beyin aktivitesi rastgele"],a:0}},
  {{s:"In einer zunehmend vernetzten Welt ist interkulturelle Kommunikation unverzichtbar.",q:"Hangi beceri vazgecilmez?",opts:["Kulturler arasi iletisim","Teknik bilgi","Finansal analiz","Proje yonetimi"],a:0}}
];
LISTEN_SENT['C2']=[
  {{s:"Die erkenntnistheoretischen Auswirkungen der poststrukturalistischen Theorie stellen den Begriff der objektiven Wahrheit infrage.",q:"Post-yapisalci teori neyi sorguluyor?",opts:["Nesnel gerceklik kavramini","Bilimsel yontemi","Matematiksel kesinligi","Tarihsel kaynaklari"],a:0}},
  {{s:"Die Synthese unterschiedlicher philosophischer Traditionen bietet ein ganzheitlicheres Verst\u00e4ndnis des Bewusstseins.",q:"Butunsel bilinc anlayisi nasil elde edilir?",opts:["Farkli felsefi geleneklerin sentezi ile","Tek bir paradigma ile","Sadece Bati cerceve ile","Sadece Dogu pratikleri ile"],a:0}},
  {{s:"Das Zusammenspiel zwischen epigenetischen Modifikationen und Umweltreizen hat unser Verst\u00e4ndnis der Vererbung revolutioniert.",q:"Epigenetik ne gosteriyor?",opts:["Gen ifadesi DNA degismeden cevre ile degisebilir","DNA mutasyonu gereklidir","Kalitim sadece genetiktir","Cevre etkisi yoktur"],a:0}}
]


// Dialogue data per level
var LISTEN_DLG={{}};
LISTEN_DLG['A1']=[
  {{title:"Im Restaurant",dlg:[{{sp:"A",t:"Hallo! Kann ich bitte eine Speisekarte haben?"}},{{sp:"B",t:"Nat\u00fcrlich! Hier, bitte."}},{{sp:"A",t:"Ich m\u00f6chte eine Pizza und ein Glas Wasser."}},{{sp:"B",t:"Das macht zehn Euro."}}],q:"M\u00fcsteri ne siparis etti?",opts:["Pizza ve su","Hamburger ve kola","Salata ve cay","Makarna ve meyve suyu"],a:0}},
  {{title:"Sich vorstellen",dlg:[{{sp:"A",t:"Hallo, ich hei\u00dfe Sarah. Wie hei\u00dft du?"}},{{sp:"B",t:"Ich bin Tom. Freut mich."}},{{sp:"A",t:"Woher kommst du, Tom?"}},{{sp:"B",t:"Ich komme aus Kanada."}}],q:"Tom nereli?",opts:["Kanada","Amerika","Ingiltere","Avustralya"],a:0}}
];
LISTEN_DLG['A2']=[
  {{title:"Arzttermin",dlg:[{{sp:"A",t:"Guten Morgen. Ich habe einen Termin um zehn Uhr."}},{{sp:"B",t:"Wie ist Ihr Name, bitte?"}},{{sp:"A",t:"Maria Lopez."}},{{sp:"B",t:"Dr. Schmidt wird Sie in f\u00fcnf Minuten sehen."}}],q:"Randevu saat kacta?",opts:["10:00","9:00","11:00","10:30"],a:0}},
  {{title:"Hotelreservierung",dlg:[{{sp:"A",t:"Ich m\u00f6chte ein Zimmer f\u00fcr zwei N\u00e4chte buchen."}},{{sp:"B",t:"Einzel- oder Doppelzimmer?"}},{{sp:"A",t:"Doppelzimmer, bitte."}},{{sp:"B",t:"Das kostet achtzig Euro pro Nacht."}}],q:"Gecelik ucret ne kadar?",opts:["80 euro","60 euro","100 euro","50 euro"],a:0}}
];
LISTEN_DLG['B1']=[
  {{title:"Besprechung",dlg:[{{sp:"A",t:"Der Umsatz ist um f\u00fcnfzehn Prozent gestiegen."}},{{sp:"B",t:"Das sind tolle Nachrichten."}},{{sp:"A",t:"Wir planen die Einf\u00fchrung im M\u00e4rz."}},{{sp:"B",t:"Ausgezeichnet."}}],q:"Gelir ne kadar artti?",opts:["Yuzde 15","Yuzde 10","Yuzde 20","Yuzde 5"],a:0}}
];
LISTEN_DLG['B2']=[
  {{title:"Gesch\u00e4ftsverhandlung",dlg:[{{sp:"A",t:"Wir bieten zehn Prozent Rabatt auf Gro\u00dfbestellungen."}},{{sp:"B",t:"Unsere Konkurrenten bieten f\u00fcnfzehn Prozent."}},{{sp:"A",t:"Wir k\u00f6nnen zw\u00f6lf Prozent bei einem Zweijahresvertrag anbieten."}},{{sp:"B",t:"Ich bespreche das mit meinem Team."}}],q:"Son indirim teklifi ne?",opts:["Yuzde 12","Yuzde 10","Yuzde 15","Yuzde 8"],a:0}}
];
LISTEN_DLG['C1']=[
  {{title:"Philosophische Diskussion",dlg:[{{sp:"A",t:"Untergr\u00e4bt moralischer Relativismus universelle Menschenrechte?"}},{{sp:"B",t:"Man kann kulturelle Unterschiede anerkennen."}},{{sp:"A",t:"Wie bestimmt man universelle Rechte?"}},{{sp:"B",t:"Durch interkulturellen Dialog und Konsens."}}],q:"Evrensel haklari belirleme yontemi ne?",opts:["Kulturler arasi diyalog","Tek bir kulturun dayatmasi","BM kararlari","Felsefi teoriler"],a:0}}
];
LISTEN_DLG['C2']=[
  {{title:"Erkenntnistheoretische Bewertung",dlg:[{{sp:"A",t:"Der hermeneutische Zirkel stellt eine Herausforderung dar."}},{{sp:"B",t:"Gadamer argumentierte, dass Vorurteile konstitutiv sind."}},{{sp:"A",t:"Besteht die Gefahr ideologischer Voreingenommenheit?"}},{{sp:"B",t:"Nur wenn kommunikative Rationalit\u00e4t versagt."}}],q:"Habermas'in onerisi ne?",opts:["Iletisimsel akilcilik","On yargilarin kaldirilmasi","Geleneksel yorumun korunmasi","Metinsel analiz"],a:0}}
]


// Fill-in-the-blank listening data
var LISTEN_FILL={{}};
LISTEN_FILL['A1']=[
  {{s:"Ich habe einen ___ Hund zu Hause.",w:"gro\u00dfen",opts:["gro\u00dfen","kleinen","roten","schnellen"]}},
  {{s:"Sie geht jeden Tag zur ___.",w:"Schule",opts:["Schule","Park","Hause","Bett"]}},
  {{s:"Wir essen ___ zum Fr\u00fchst\u00fcck.",w:"Eier",opts:["Eier","Abendessen","Mittagessen","Schuhe"]}},
  {{s:"Der Himmel ist heute ___.",w:"blau",opts:["blau","gr\u00fcn","braun","rosa"]}},
  {{s:"Er trinkt morgens ___.",w:"Kaffee",opts:["Kaffee","Suppe","Eis","Sand"]}}
];
LISTEN_FILL['A2']=[
  {{s:"Ich ___ seit zwanzig Minuten auf den Bus.",w:"warte",opts:["warte","laufe","sitze","esse"]}},
  {{s:"Sie ___ dreimal pro Woche ins Fitnessstudio.",w:"geht",opts:["geht","l\u00e4uft","f\u00e4hrt","schwimmt"]}},
  {{s:"Das Museum war ___ als ich erwartet hatte.",w:"gr\u00f6\u00dfer",opts:["gr\u00f6\u00dfer","kleiner","\u00e4lter","neuer"]}},
  {{s:"Er hat seine Schl\u00fcssel im B\u00fcro ___.",w:"vergessen",opts:["vergessen","gefunden","verloren","gebrochen"]}}
];
LISTEN_FILL['B1']=[
  {{s:"Wenn ich mehr Zeit ___, w\u00fcrde ich Gitarre lernen.",w:"h\u00e4tte",opts:["h\u00e4tte","habe","werde","w\u00fcrde"]}},
  {{s:"Das Projekt wurde ___ abgeschlossen.",w:"erfolgreich",opts:["erfolgreich","langsam","schlecht","nie"]}},
  {{s:"Trotz der ___ haben sie den Marathon beendet.",w:"Schwierigkeiten",opts:["Schwierigkeiten","Wetter","Essen","Verkehr"]}}
];
LISTEN_FILL['B2']=[
  {{s:"Die Entscheidung wurde mit ___ aufgenommen.",w:"Kritik",opts:["Kritik","Zustimmung","Stille","Verwirrung"]}},
  {{s:"H\u00e4tte sie davon ___, h\u00e4tte sie sich vorbereitet.",w:"gewusst",opts:["gewusst","erz\u00e4hlt","geh\u00f6rt","gesagt"]}},
  {{s:"Der Roman bietet eine ___ Kritik der Konsumkultur.",w:"\u00fcberzeugende",opts:["\u00fcberzeugende","langweilige","einfache","kurze"]}}
];
LISTEN_FILL['C1']=[
  {{s:"Sein Argument, obwohl ___ konstruiert, hatte L\u00fccken.",w:"sorgf\u00e4ltig",opts:["sorgf\u00e4ltig","schlecht","hastig","zuf\u00e4llig"]}},
  {{s:"Der Ausschuss erreichte eine ___ Entscheidung.",w:"einstimmige",opts:["einstimmige","schnelle","teilweise","geteilte"]}},
  {{s:"___ Fortschritte in der Biotechnologie werfen ethische Fragen auf.",w:"J\u00fcngste",opts:["J\u00fcngste","Antike","Geringf\u00fcgige","Theoretische"]}}
];
LISTEN_FILL['C2']=[
  {{s:"Die ___ Natur des Bewusstseins bleibt r\u00e4tselhaft.",w:"r\u00e4tselhafte",opts:["r\u00e4tselhafte","einfache","physische","digitale"]}},
  {{s:"Seine ___ Analyse erwies sich als vorausschauend.",w:"nuancierte",opts:["nuancierte","kurze","fehlerhafte","beil\u00e4ufige"]}},
  {{s:"Die ___ der Theorie liegt in der Vers\u00f6hnung von Befunden.",w:"Eleganz",opts:["Eleganz","Schw\u00e4che","Komplexit\u00e4t","Herkunft"]}}
]


// ===================== LISTENING =====================
function renderListening(){{
  var lv=S.level;
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var catKeys=Object.keys(cats);
  if(S.subTab==='dictation')return renderDictation();
  if(S.subTab==='listenQuiz')return renderListenQuiz();
  if(S.subTab==='sentListen')return renderSentListen();
  if(S.subTab==='dialogListen')return renderDialogListen();
  if(S.subTab==='fillListen')return renderFillListen();
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83c\\udf99 '+lv+' Dinleme Aktiviteleri'));
  // Speed control
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;align-items:center"><span style="font-size:.8rem;color:var(--txt3)">Hiz:</span>';
  [0.6,0.75,0.85,1.0].forEach(function(sp){{
    o+='<button class="spbtn'+(S.listenSpeed===sp?' act':'')+'" onclick="setSpeed('+sp+')">'+sp+'x</button>';
  }});
  o+='</div>';
  var sentCount=(LISTEN_SENT[lv]||[]).length;
  var dlgCount=(LISTEN_DLG[lv]||[]).length;
  var fillCount=(LISTEN_FILL[lv]||[]).length;
  o+='<div class="g2">';
  o+='<div class="cd ctc" onclick="startListenQuiz()"><div class="ce">\\ud83c\\udfa7</div><div class="ci"><div class="cn">Dinle ve Sec</div><div class="cs">Kelimeyi duyup dogru secenegi sec (10 soru)</div></div></div>';
  o+='<div class="cd ctc" onclick="startDictation()"><div class="ce">\\u270d\\ufe0f</div><div class="ci"><div class="cn">Dikte</div><div class="cs">Duydugun kelimeyi yaz (10 soru)</div></div></div>';
  o+='<div class="cd ctc" onclick="startSentListen()"><div class="ce">\\ud83d\\udde3\\ufe0f</div><div class="ci"><div class="cn">Cumle Dinleme</div><div class="cs">Cumleyi dinle, anlama sorusunu cevapla ('+sentCount+' cumle)</div></div></div>';
  o+='<div class="cd ctc" onclick="startDialogListen()"><div class="ce">\\ud83d\\udcac</div><div class="ci"><div class="cn">Diyalog Anlama</div><div class="cs">Konusmayi dinle, soruyu cevapla ('+dlgCount+' diyalog)</div></div></div>';
  o+='<div class="cd ctc" onclick="startFillListen()"><div class="ce">\\ud83d\\udd24</div><div class="ci"><div class="cn">Bosluk Doldur</div><div class="cs">Cumledeki eksik kelimeyi bul ('+fillCount+' soru)</div></div></div>';
  o+='</div>';
  return o;
}}

function renderListenQuiz(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderListening();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Geri</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px;text-align:center">';
  o+='<div style="margin-bottom:16px"><button class="spk" onclick="speak(\\''+cur.word.e.replace(/'/g,"\\\\'")+'\\')" style="width:60px;height:60px;font-size:1.5rem">\\ud83d\\udd0a</button></div>';
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:16px">Kelimeyi dinle ve Turkce karsiligini sec:</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.correct)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-qi="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="quizNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

function renderDictation(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderListening();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Geri</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Kelime <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px;text-align:center">';
  o+='<div style="margin-bottom:16px"><button class="spk" onclick="speak(\\''+cur.word.e.replace(/'/g,"\\\\'")+'\\')" style="width:60px;height:60px;font-size:1.5rem">\\ud83d\\udd0a</button></div>';
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:16px">Duydugun kelimeyi yaz:</div>';
  o+='<input class="din" id="dict-input" placeholder="Almanca kelimeyi yaz..." style="text-align:center;max-width:300px;margin:0 auto;display:block" onkeypress="if(event.key===\\'Enter\\')checkDict()">';
  if(q.ans){{
    var isOk=q.sel===1;
    o+='<div style="margin-top:12px;font-size:.9rem;color:'+(isOk?'#81c784':'#ef9a9a')+'">'+
      (isOk?'\\u2705 Dogru!':'\\u274c Yanlis! Dogru cevap: <b>'+cur.word.e+'</b>')+'</div>';
    o+='<div style="margin-top:12px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="dictNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}else{{
    o+='<div style="margin-top:12px"><button class="btn btn-g" onclick="checkDict()">Kontrol Et</button></div>';
  }}
  o+='</div></div>';
  return o;
}}

// ============ Sentence Listening ============
function renderSentListen(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderListening();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Geri</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px;text-align:center">';
  o+='<div style="margin-bottom:12px"><button class="spk" onclick="speak(\\''+cur.s.replace(/'/g,"\\\\'").replace(/"/g,'')+'\\')" style="width:60px;height:60px;font-size:1.5rem">\\ud83d\\udd0a</button></div>';
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:6px">Cumleyi dinle ve soruyu cevapla:</div>';
  if(q.ans){{o+='<div style="padding:8px 14px;background:rgba(99,102,241,.06);border-radius:8px;margin-bottom:10px;font-size:.82rem;color:var(--accent1);font-style:italic;border-left:3px solid var(--accent1)">\\ud83d\\udcc4 Transkript: "'+cur.s+'"</div>';}}
  else{{o+='<div style="margin-bottom:6px"><button class="btn btn-o" style="font-size:.72rem;padding:4px 12px" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display===\\'none\\'?\\'block\\':\\'none\\'">\\ud83d\\udc41 Transkript Goster</button><div style="display:none;padding:6px 12px;margin-top:4px;background:rgba(99,102,241,.06);border-radius:8px;font-size:.82rem;color:var(--accent1);font-style:italic">'+cur.s+'</div></div>';}}
  o+='<div style="font-size:.9rem;font-weight:600;margin-bottom:16px;color:var(--gold)">'+cur.q+'</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.a)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-sli="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="sentListenNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

// ============ Dialog Listening ============
function renderDialogListen(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderListening();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Geri</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Diyalog <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px">';
  o+='<div style="font-size:.9rem;font-weight:700;margin-bottom:12px;color:var(--gold)">\\ud83d\\udcac '+cur.title+'</div>';
  // Play all button
  var allText=cur.dlg.map(function(d){{return d.t;}}).join('. ');
  o+='<div style="margin-bottom:12px;text-align:center"><button class="spk" onclick="speak(\\''+allText.replace(/'/g,"\\\\'").replace(/"/g,'')+'\\')" style="font-size:1.1rem;padding:8px 16px">\\ud83d\\udd0a Diyalogu Dinle</button></div>';
  // Show dialogue lines
  cur.dlg.forEach(function(d){{
    var bgCol=d.sp==='A'?'rgba(201,168,76,.08)':'rgba(76,133,201,.08)';
    var icon=d.sp==='A'?'\\ud83d\\udc64':'\\ud83d\\udc65';
    o+='<div style="display:flex;gap:8px;margin-bottom:6px;padding:8px 12px;border-radius:8px;background:'+bgCol+'">';
    o+='<span style="font-weight:700">'+icon+' '+d.sp+':</span>';
    o+='<span style="font-size:.85rem">'+d.t+'</span></div>';
  }});
  o+='<div style="font-size:.9rem;font-weight:600;margin:16px 0 12px;color:var(--txt)">'+cur.q+'</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    if(q.ans){{cls+=' dis';if(i===cur.a)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-dli="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="dialogListenNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

// ============ Fill-in-the-Blank Listening ============
function renderFillListen(){{
  var q=S.quiz;if(!q.qs.length){{S.subTab='';return renderListening();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Geri</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Soru <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span><span>Dogru: <b style="color:#81c784">'+q.score+'</b></span></div>';
  o+='<div class="qw"><div class="cd" style="padding:24px;text-align:center">';
  var fullSent=cur.s.replace('___',cur.w);
  o+='<div style="margin-bottom:12px"><button class="spk" onclick="speak(\\''+fullSent.replace(/'/g,"\\\\'").replace(/"/g,'')+'\\')" style="width:60px;height:60px;font-size:1.5rem">\\ud83d\\udd0a</button></div>';
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:6px">Cumleyi dinle, eksik kelimeyi sec:</div>';
  if(q.ans){{o+='<div style="padding:6px 12px;background:rgba(99,102,241,.06);border-radius:8px;margin-bottom:10px;font-size:.82rem;color:var(--accent1);font-style:italic;border-left:3px solid var(--accent1)">\\ud83d\\udcc4 '+fullSent+'</div>';}}
  o+='<div style="font-size:1.05rem;font-weight:600;margin-bottom:16px;color:var(--txt)">'+cur.s.replace('___','<span style="color:var(--gold);border-bottom:2px dashed var(--gold)">______</span>')+'</div>';
  o+='<div class="qop">';
  cur.opts.forEach(function(opt,i){{
    var cls='qo';
    var correctIdx=cur.opts.indexOf(cur.w);
    if(q.ans){{cls+=' dis';if(i===correctIdx)cls+=' ok';else if(i===q.sel)cls+=' no';}}
    o+='<div class="'+cls+'" data-fli="'+i+'">'+String.fromCharCode(65+i)+') '+opt+'</div>';
  }});
  o+='</div></div>';
  if(q.ans){{
    o+='<div style="text-align:center;margin-top:14px">';
    if(q.cur<q.qs.length-1)o+='<button class="btn btn-g" onclick="fillListenNext()">Sonraki \\u2192</button>';
    else o+='<button class="btn btn-g" onclick="finishGenericQuiz()">Sonuclari Gor</button>';
    o+='</div>';
  }}
  o+='</div>';
  return o;
}}

// ===================== WRITING =====================
function renderWriting(){{
  var lv=S.level;var prompts=WPROMPTS[lv]||[];
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\u270d\\ufe0f '+lv+' Yazma'));
  o+='<div class="cd" style="margin-bottom:14px;padding:16px">';
  o+='<div style="font-size:.82rem;color:var(--gl);font-weight:700;margin-bottom:8px">Konu Sec:</div>';
  prompts.forEach(function(p,i){{
    o+='<div class="qo" style="margin-bottom:6px;font-size:.85rem;'+(S.writeIdx===i?'border-color:var(--gold);background:rgba(201,168,76,.08)':'')+'" onclick="S.writeIdx='+i+';render()">\\ud83d\\udccc '+p+'</div>';
  }});
  o+='</div>';
  o+='<div class="cd" style="padding:16px">';
  o+='<div style="font-size:.85rem;color:var(--gl);margin-bottom:10px"><b>Konu:</b> '+prompts[S.writeIdx]+'</div>';
  o+='<textarea class="wta" id="write-area" placeholder="Buraya yaz..."></textarea>';
  o+='<div style="display:flex;justify-content:space-between;align-items:center;margin-top:12px;flex-wrap:wrap;gap:8px">';
  o+='<span id="wcount" style="font-size:.82rem;color:var(--txt3);font-weight:600">0 kelime</span>';
  o+='<div style="display:flex;gap:8px;align-items:center">';
  o+='<button class="btn btn-g" onclick="analyzeWriting()" style="padding:8px 20px">\\ud83d\\udcca Analiz Et</button>';
  o+='<button class="btn btn-o" onclick="document.getElementById(\\'write-area\\').value=\\'\\';render()" style="padding:8px 16px">\\ud83d\\uddd1 Temizle</button>';
  o+='</div></div>';
  o+='<div id="write-feedback"></div>';
  o+='</div>';
  // Writing history
  if(P.writings&&P.writings.length){{
    o+='<div class="cd" style="margin-top:14px;padding:16px">';
    o+='<div style="font-size:.82rem;color:var(--gl);font-weight:700;margin-bottom:8px">\\ud83d\\udcdd Son Yazilarim ('+P.writings.length+')</div>';
    P.writings.slice(-5).reverse().forEach(function(wr){{
      o+='<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(0,0,0,.04);font-size:.78rem">';
      o+='<span>'+wr.date+' | '+wr.level+'</span>';
      o+='<span>'+wr.words+' kelime | %'+wr.diversity+' cesitlilik</span></div>';
    }});
    o+='</div>';
  }}
  return o;
}}

// ===================== PROGRESS =====================
function renderProgress(){{
  var o='';
  o+=h('div','shd',h('h3','hd','\\ud83d\\udcc8 Genel Ilerleme'));
  // Overall stats
  o+='<div class="g4" style="margin-bottom:20px">';
  o+=h('div','cd stc','<div class="si">\\u2b50</div><div class="sv">'+P.xp+'</div><div class="sl">Toplam XP</div>');
  o+=h('div','cd stc','<div class="si">\\ud83d\\udd25</div><div class="sv">'+P.streak+'</div><div class="sl">Gun Serisi</div>');
  o+=h('div','cd stc','<div class="si">\\ud83d\\udcda</div><div class="sv">'+learnedWordsAll()+'/'+totalWordsAll()+'</div><div class="sl">Kelime</div>');
  o+=h('div','cd stc','<div class="si">\\ud83c\\udfaf</div><div class="sv">'+P.quizHistory.length+'</div><div class="sl">Quiz</div>');
  o+='</div>';
  // Per-level progress
  o+=h('div','shd',h('h3','hd','\\ud83c\\udf10 Seviye Detaylari'));
  LEVELS.forEach(function(lv){{
    var li=LINFO[lv],pct=levelPct(lv),ul=isUnlocked(lv);
    var cd2=catsDone(lv),gd2=gramsDone(lv),lp=getLP(lv);
    o+='<div class="cd" style="margin-bottom:12px;padding:16px'+(ul?'':';opacity:.4')+'">';
    o+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">';
    o+='<div><span class="bdg'+(lp.examPassed?' on':'')+'" style="margin-right:8px">'+li.i+' '+lv+' - '+li.t+(lp.examPassed?' \\u2705':'')+'</span></div>';
    o+='<span style="font-size:.82rem;color:var(--txt3)">%'+pct+'</span></div>';
    o+='<div class="pb pb-g" style="margin-bottom:6px"><div class="fl" style="width:'+pct+'%"></div></div>';
    o+='<div style="display:flex;gap:16px;font-size:.75rem;color:var(--txt3)">';
    o+='<span>\\ud83d\\udcda Kelime: '+learnedWordsForLevel(lv)+'/'+totalWordsForLevel(lv)+'</span>';
    o+='<span>\\ud83d\\udcdd Kategori: '+cd2.done+'/'+cd2.total+'</span>';
    o+='<span>\\ud83d\\udcd6 Gramer: '+gd2.done+'/'+gd2.total+'</span>';
    o+='<span>\\ud83c\\udfaf Sinav: '+(lp.examPassed?'\\u2705':'\\u274c')+'</span></div>';
    o+='</div>';
  }});
  // Badges
  o+=h('div','shd',h('h3','hd','\\ud83c\\udfc5 Rozetler'));
  var allBadges=[
    {{id:'xp100',i:'\\u2b50',n:'100 XP'}},{{id:'xp500',i:'\\ud83c\\udf1f',n:'500 XP'}},
    {{id:'xp1k',i:'\\ud83d\\udca5',n:'1000 XP'}},{{id:'xp5k',i:'\\ud83d\\udc8e',n:'5000 XP'}},
    {{id:'s3',i:'\\ud83d\\udd25',n:'3 Gun Seri'}},{{id:'s7',i:'\\ud83c\\udf1e',n:'7 Gun Seri'}},{{id:'s30',i:'\\ud83c\\udfc6',n:'30 Gun Seri'}},
    {{id:'q5',i:'\\ud83c\\udfaf',n:'5 Quiz'}},{{id:'q20',i:'\\ud83d\\udcaa',n:'20 Quiz'}},{{id:'q50',i:'\\ud83e\\udde0',n:'50 Quiz'}},
    {{id:'pass_A1',i:'\\ud83c\\udf31',n:'A1 Gecti'}},{{id:'pass_A2',i:'\\ud83d\\udcd7',n:'A2 Gecti'}},
    {{id:'pass_B1',i:'\\ud83d\\udcd8',n:'B1 Gecti'}},{{id:'pass_B2',i:'\\ud83d\\udcd9',n:'B2 Gecti'}},
    {{id:'pass_C1',i:'\\ud83d\\udcd5',n:'C1 Gecti'}},{{id:'pass_C2',i:'\\ud83d\\udc51',n:'C2 Gecti'}}
  ];
  o+='<div style="display:flex;flex-wrap:wrap;gap:8px">';
  allBadges.forEach(function(b){{
    var earned=P.badges.indexOf(b.id)!==-1;
    o+='<span class="bdg'+(earned?' on':'')+'">'+b.i+' '+b.n+'</span>';
  }});
  o+='</div>';
  // Weak area summary
  var weakAll=getWeakAreas();
  if(weakAll.length){{
    o+=h('div','shd',h('h3','hd','\\ud83d\\udcc9 Zayif Alanlar ('+S.level+')'));
    o+='<div class="cd" style="padding:16px">';
    var vocW=weakAll.filter(function(w){{return w.type==='vocab';}});
    var gramW=weakAll.filter(function(w){{return w.type==='gram';}});
    if(vocW.length){{
      o+='<div style="font-size:.82rem;font-weight:700;color:var(--red);margin-bottom:8px">\\ud83d\\udcda Kelime ('+vocW.length+' zayif kategori):</div>';
      vocW.forEach(function(w){{
        o+='<div style="font-size:.78rem;color:var(--txt2);margin-bottom:4px">\\u2022 '+w.cat+' (%'+w.pct+' tamamlandi)</div>';
      }});
    }}
    if(gramW.length){{
      o+='<div style="font-size:.82rem;font-weight:700;color:var(--org);margin:10px 0 8px">\\ud83d\\udcd0 Gramer ('+gramW.length+' tamamlanmamis konu):</div>';
      gramW.forEach(function(w){{
        o+='<div style="font-size:.78rem;color:var(--txt2);margin-bottom:4px">\\u2022 '+w.topic+'</div>';
      }});
    }}
    o+='<div style="margin-top:12px"><button class="btn btn-g" onclick="startWeakQuiz()" style="font-size:.8rem">\\ud83d\\udcc9 Zayif Alan Quizi Baslat</button></div>';
    o+='</div>';
  }}
  return o;
}}

// ===================== EVENT BINDING =====================
function bindEvents(){{
  // Cat card clicks (vocab)
  document.querySelectorAll('[data-cat]').forEach(function(el){{
    el.onclick=function(){{
      S.cat=this.dataset.cat;S.level=this.dataset.lv||S.level;
      S.learnIdx=0;S.flipped=false;S.subTab='learn';render();
    }};
  }});
  // Quiz option clicks
  document.querySelectorAll('.qo:not(.dis)').forEach(function(el){{
    if(el.dataset.qi!==undefined){{
      el.onclick=function(){{quizAnswer(parseInt(this.dataset.qi));}};
    }}
    if(el.dataset.rqi!==undefined){{
      el.onclick=function(){{
        var qi=parseInt(this.dataset.rqi),oi=parseInt(this.dataset.roi),a=parseInt(this.dataset.ra);
        var wrap=document.getElementById('rq_'+qi);if(!wrap)return;
        var opts=wrap.querySelectorAll('.qo');
        opts.forEach(function(o,idx){{o.classList.add('dis');if(idx===a)o.classList.add('ok');else if(idx===oi&&oi!==a)o.classList.add('no');}});
        if(oi===a)addXP(5);saveP();
      }};
    }}
  }});
  // Level card clicks (dashboard)
  document.querySelectorAll('.lvc:not(.lk)').forEach(function(el){{
    el.onclick=function(){{
      var lv=this.dataset.lv;if(lv){{S.level=lv;TAB='vocab';render();}}
    }};
  }});
  // Writing word count
  var wa=document.getElementById('write-area');
  if(wa){{
    wa.oninput=function(){{
      var wc=this.value.trim()?this.value.trim().split(/\\s+/).length:0;
      var el=document.getElementById('wcount');if(el)el.textContent=wc+' kelime';
    }};
  }}
}}

// ===================== ACTIONS =====================
window.goTab=function(t){{TAB=t;S.subTab='';render();}};
window.setLevel=function(l){{S.level=l;S.subTab='';render();}};
window.flipCard=function(){{S.flipped=!S.flipped;render();if(S.flipped){{var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};var w=(cats[S.cat]||[])[S.learnIdx];if(w)setTimeout(function(){{speak(w.e);}},200);}}}};
window.learnNext=function(known){{
  var lp=getLP(S.level);
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};
  var w=(cats[S.cat]||[])[S.learnIdx];
  if(known){{
    if(w){{
      if(!lp.wordsLearned)lp.wordsLearned=[];
      var exists=lp.wordsLearned.some(function(x){{return x.e===w.e&&x.lv===S.level;}});
      if(!exists){{lp.wordsLearned.push({{e:w.e,t:w.t,cat:S.cat,lv:S.level}});addXP(2);}}
      saveP();
    }}
  }}else{{
    if(!S.retryQueue)S.retryQueue=[];
    if(S.retryQueue.indexOf(S.learnIdx)===-1)S.retryQueue.push(S.learnIdx);
  }}
  S.learnIdx++;S.flipped=false;
  var words=cats[S.cat]||[];
  if(S.learnIdx>=words.length){{
    if(S.retryQueue&&S.retryQueue.length>0){{
      S.learnIdx=S.retryQueue.shift();
    }}else{{
      S.learnIdx=words.length-1;S.flipped=true;
    }}
  }}
  render();
}};
window.startCatQuiz=function(){{
  S.quiz={{qs:genCatQuiz(S.level,S.cat),cur:0,score:0,ans:false,sel:-1,type:'Kategori'}};
  S.subTab='catQuizRun';render();
}};
window.quizAnswer=function(idx){{
  if(S.quiz.ans)return;S.quiz.ans=true;S.quiz.sel=idx;
  if(idx===S.quiz.qs[S.quiz.cur].correct){{S.quiz.score++;addXP(5);}}
  saveP();render();
  var cur=S.quiz.qs[S.quiz.cur];
  if(cur.word)setTimeout(function(){{speak(cur.word.e);}},200);
}};
window.quizNext=function(){{S.quiz.cur++;S.quiz.ans=false;S.quiz.sel=-1;render();
  if(S.subTab==='listenQuiz'){{var cur=S.quiz.qs[S.quiz.cur];if(cur&&cur.word)setTimeout(function(){{speak(cur.word.e);}},400);}}
}};
window.finishCatQuiz=function(){{
  P.quizHistory.push({{date:new Date().toISOString().slice(0,10),level:S.level,type:'Kategori',score:S.quiz.score,total:S.quiz.qs.length}});
  saveP();S.subTab='catResult';render();
}};
window.startLevelQuiz=function(type){{
  var qs=type==='cat'?genCatQuiz(S.level,Object.keys(WORDS[S.level]?WORDS[S.level].categories:{{}})[Math.floor(Math.random()*Object.keys(WORDS[S.level]?WORDS[S.level].categories:{{}}).length)]||''):genLevelQuiz(S.level);
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:type==='cat'?'Kategori':'Seviye'}};
  S.subTab='quizRun';render();
}};
window.finishGenericQuiz=function(){{
  P.quizHistory.push({{date:new Date().toISOString().slice(0,10),level:S.level,type:S.quiz.type||'Quiz',score:S.quiz.score,total:S.quiz.qs.length}});
  addXP(S.quiz.score*3);saveP();S.subTab='quizResult';render();
}};
window.startExam=function(){{
  var qs=genExam(S.level);
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Sinav',timer:null,timeLeft:900}};
  if(S.quiz.timer)clearInterval(S.quiz.timer);
  S.quiz.timer=setInterval(function(){{
    S.quiz.timeLeft--;
    if(S.quiz.timeLeft<=0){{clearInterval(S.quiz.timer);window.finishExam();}}
    else{{var te=document.getElementById('exam-timer');
      if(te){{var m=Math.floor(S.quiz.timeLeft/60),s=S.quiz.timeLeft%60;te.textContent='\\u23f1 '+m+':'+(s<10?'0':'')+s;}}
    }}
  }},1000);
  S.subTab='examRun';render();
}};
window.finishExam=function(){{
  if(S.quiz.timer){{clearInterval(S.quiz.timer);S.quiz.timer=null;}}
  P.quizHistory.push({{date:new Date().toISOString().slice(0,10),level:S.level,type:'Sinav',score:S.quiz.score,total:S.quiz.qs.length}});
  saveP();S.subTab='examResult';render();
}};
window.abandonExam=function(){{
  if(S.quiz.timer){{clearInterval(S.quiz.timer);S.quiz.timer=null;}}
  S.subTab='';S.quiz.qs=[];render();
}};
window.checkGramEx=function(eid,gi){{
  var inp=document.getElementById(eid);if(!inp)return;
  var ans=inp.dataset.ans;var val=inp.value.trim();
  if(val.toLowerCase()===ans.toLowerCase()){{
    inp.classList.remove('no');inp.classList.add('ok');inp.disabled=true;
    var lp=getLP(S.level);
    if(!lp.gramExDone)lp.gramExDone={{}};
    if(!lp.gramExDone[gi])lp.gramExDone[gi]={{}};
    var parts=eid.split('_');var ei=parseInt(parts[2]);
    lp.gramExDone[gi][ei]=true;
    // Check if ALL exercises for this grammar topic are done
    var gs=GRAMMAR[S.level]||[];var totalEx=(gs[gi]&&gs[gi].exercises)?gs[gi].exercises.length:1;
    var doneEx=Object.keys(lp.gramExDone[gi]).length;
    if(doneEx>=totalEx){{lp.gramDone[gi]=true;}}
    addXP(10);saveP();
    // Update visual: show progress count
    var wrap=document.getElementById('wrap_'+eid);
    if(wrap){{var badge=wrap.querySelector('.exok');if(!badge){{var sp=document.createElement('span');sp.className='exok';sp.style.cssText='color:#81c784;font-size:.8rem;margin-left:6px';sp.textContent='\\u2705';wrap.appendChild(sp);}}}}
    // Update topic header if all done
    if(doneEx>=totalEx){{render();}}
  }}else{{
    inp.classList.remove('ok');inp.classList.add('no');
  }}
}};
window.openReading=function(i){{S.readIdx=i;S.subTab='readText';render();}};
window.setSpeed=function(sp){{S.listenSpeed=sp;ttsRate=sp;render();}};
window.startListenQuiz=function(){{
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all).slice(0,10);var qs=[];
  all.forEach(function(w){{
    var opts=[w.t];var others=all.filter(function(x){{return x.t!==w.t;}});
    others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].t);
    opts=shuffle(opts);qs.push({{stem:'Dinle',opts:opts,correct:opts.indexOf(w.t),word:w}});
  }});
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Dinleme'}};
  S.subTab='listenQuiz';render();
  setTimeout(function(){{if(qs[0]&&qs[0].word)speak(qs[0].word.e);}},500);
}};
window.startDictation=function(){{
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all).slice(0,10);var qs=[];
  all.forEach(function(w){{qs.push({{word:w}});}});
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Dikte'}};
  S.subTab='dictation';render();
  setTimeout(function(){{if(qs[0]&&qs[0].word)speak(qs[0].word.e);}},500);
}};
window.checkDict=function(){{
  var inp=document.getElementById('dict-input');if(!inp)return;
  var val=inp.value.trim().toLowerCase();
  var cur=S.quiz.qs[S.quiz.cur];
  if(val===cur.word.e.toLowerCase()){{S.quiz.score++;S.quiz.sel=1;addXP(5);}}
  else S.quiz.sel=0;
  S.quiz.ans=true;saveP();render();
}};
window.dictNext=function(){{S.quiz.cur++;S.quiz.ans=false;S.quiz.sel=-1;render();
  var cur=S.quiz.qs[S.quiz.cur];if(cur&&cur.word)setTimeout(function(){{speak(cur.word.e);}},400);
}};
window.speakDE=speak;

// ============ MATCHING QUIZ RENDER ============
function renderMatchQuiz(){{
  var m=S.match;if(!m){{S.subTab='';return renderQuiz();}}
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.match=null;render()">\\u2190 Vazgec</button>';
  o+=h('div','shd',h('h3','hd','\\ud83d\\udd17 Eslestirme - '+m.total+' kelime'));
  var matchedCount=Object.keys(m.matched).length;
  o+='<div style="font-size:.82rem;color:var(--txt3);margin-bottom:16px">Eslestirilen: <b style="color:var(--grn)">'+matchedCount+'</b>/'+m.total+'</div>';
  if(matchedCount>=m.total){{
    addXP(m.total*5);
    P.quizHistory.push({{date:new Date().toISOString().slice(0,10),level:S.level,type:'Eslestirme',score:m.total,total:m.total}});
    saveP();
    o+='<div class="rsc"><div class="ri">\\ud83c\\udf89</div><div class="rt">Tebrikler!</div>';
    o+='<div class="rv">'+m.total+'/'+m.total+'</div>';
    o+='<div class="rm">Tum kelimeler eslesti!</div>';
    o+='<button class="btn btn-g" onclick="S.subTab=\\'\\';S.match=null;render()">Quiz Merkezine Don</button></div>';
    return o;
  }}
  o+='<div style="display:grid;grid-template-columns:1fr 40px 1fr;gap:8px;max-width:700px;margin:0 auto">';
  o+='<div>';
  m.left.forEach(function(en,i){{
    var done=m.matched[i]!==undefined;
    var sel=S.matchSel===i;
    o+='<div style="padding:12px 16px;margin-bottom:8px;border-radius:12px;cursor:'+(done?'default':'pointer')+';font-weight:600;font-size:.88rem;text-align:center;transition:all .2s;';
    if(done)o+='background:rgba(16,185,129,.1);border:1.5px solid rgba(16,185,129,.3);color:var(--grn);opacity:.6"';
    else if(sel)o+='background:rgba(99,102,241,.12);border:1.5px solid rgba(99,102,241,.5);color:var(--accent1);box-shadow:0 0 12px rgba(99,102,241,.15)"';
    else o+='background:var(--card);border:1.5px solid rgba(0,0,0,.1);color:var(--txt)"';
    o+=' data-ml="'+i+'">'+en+(done?' \\u2705':'')+'</div>';
  }});
  o+='</div>';
  o+='<div style="display:flex;flex-direction:column;justify-content:center;align-items:center;color:var(--txt3)"><span style="font-size:1.2rem">\\u2194\\ufe0f</span></div>';
  o+='<div>';
  m.right.forEach(function(tr,j){{
    var done=false;Object.keys(m.matched).forEach(function(k){{if(m.matched[k]===j)done=true;}});
    o+='<div style="padding:12px 16px;margin-bottom:8px;border-radius:12px;cursor:'+(done?'default':'pointer')+';font-size:.88rem;text-align:center;transition:all .2s;';
    if(done)o+='background:rgba(16,185,129,.1);border:1.5px solid rgba(16,185,129,.3);color:var(--grn);opacity:.6"';
    else o+='background:var(--card);border:1.5px solid rgba(0,0,0,.1);color:var(--txt)"';
    o+=' data-mr="'+j+'">'+tr+(done?' \\u2705':'')+'</div>';
  }});
  o+='</div></div>';
  return o;
}}

// ============ SPACED REPETITION ENGINE ============
function getSRWords(){{
  if(!P.sr)P.sr={{}};
  var now=Date.now();var due=[];
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};
  Object.keys(cats).forEach(function(c){{
    cats[c].forEach(function(w){{
      var key=S.level+'_'+w.e;
      var sr=P.sr[key];
      if(!sr){{due.push(w);return;}}
      if(sr.next<=now)due.push(w);
    }});
  }});
  return due.slice(0,20);
}}
function updateSR(word,correct){{
  if(!P.sr)P.sr={{}};
  var key=S.level+'_'+word.e;
  var sr=P.sr[key]||{{interval:1,ease:2.5,reps:0}};
  if(correct){{
    sr.reps++;
    if(sr.reps===1)sr.interval=1;
    else if(sr.reps===2)sr.interval=3;
    else sr.interval=Math.round(sr.interval*sr.ease);
    sr.ease=Math.max(1.3,sr.ease+0.1);
  }}else{{
    sr.reps=0;sr.interval=1;
    sr.ease=Math.max(1.3,sr.ease-0.2);
  }}
  sr.next=Date.now()+sr.interval*86400000;
  sr.last=Date.now();
  P.sr[key]=sr;saveP();
}}
function renderSRQuiz(){{
  var q=S.quiz;if(!q||!q.qs||!q.qs.length){{S.subTab='';return renderQuiz();}}
  var cur=q.qs[q.cur];
  var o='';
  o+='<button class="bbk" onclick="S.subTab=\\'\\';S.quiz.qs=[];render()">\\u2190 Vazgec</button>';
  o+='<div style="display:flex;justify-content:space-between;margin:12px 0;font-size:.82rem">';
  o+='<span>Kelime <b>'+(q.cur+1)+'</b>/'+q.qs.length+'</span>';
  o+='<span>\\ud83e\\udde0 Spaced Repetition</span></div>';
  o+='<div class="qw"><div class="cd" style="padding:32px;text-align:center">';
  o+='<div style="font-size:.7rem;color:var(--txt3);text-transform:uppercase;letter-spacing:3px;margin-bottom:16px">Bu kelimeyi biliyor musun?</div>';
  o+='<div style="font-size:2rem;font-weight:900;color:var(--accent1);margin-bottom:8px">'+cur.e+'</div>';
  o+='<div style="margin-bottom:16px"><button class="spk" onclick="speak(\\''+cur.e.replace(/'/g,"\\\\'")+'\\')" style="font-size:1.2rem">\\ud83d\\udd0a</button></div>';
  if(q.ans){{
    o+='<div style="font-size:1.3rem;color:var(--txt);margin:16px 0;font-weight:600">'+cur.t+'</div>';
    o+='<div style="display:flex;gap:12px;justify-content:center;margin-top:20px">';
    o+='<button class="btn btn-rd" onclick="srAnswer(false)" style="padding:12px 28px">\\u274c Bilmiyorum</button>';
    o+='<button class="btn btn-gr" onclick="srAnswer(true)" style="padding:12px 28px">\\u2705 Biliyorum</button>';
    o+='</div>';
  }}else{{
    o+='<div style="margin-top:20px"><button class="btn btn-g" onclick="S.quiz.ans=true;render()">Cevabi Goster</button></div>';
  }}
  o+='</div></div>';
  return o;
}}

// ============ WEAK AREA ANALYSIS ============
function getWeakAreas(){{
  var weak=[];
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};
  var lp=getLP(S.level);
  Object.keys(cats).forEach(function(c){{
    var words=cats[c];
    var learned=(lp.wordsLearned||[]).filter(function(w){{return w.cat===c&&w.lv===S.level;}}).length;
    var pct=words.length>0?Math.round(learned/words.length*100):100;
    if(pct<50)weak.push({{cat:c,pct:pct,words:words,type:'vocab'}});
  }});
  var gs=GRAMMAR[S.level]||[];
  gs.forEach(function(g,i){{
    if(!lp.gramDone||!lp.gramDone[i])weak.push({{topic:g.topic,idx:i,type:'gram'}});
  }});
  return weak;
}}

// ============ STARTER FUNCTIONS ============
window.startMatchQuiz=function(){{
  S.match=genMatchQuiz(S.level);
  S.matchSel=-1;
  S.subTab='matchRun';render();
}};
window.startSRQuiz=function(){{
  var words=getSRWords();
  if(!words.length){{alert('Tekrar gereken kelime yok! Harika!');return;}}
  S.quiz={{qs:words,cur:0,score:0,ans:false,sel:-1,type:'Spaced Repetition'}};
  S.subTab='srRun';render();
}};
window.srAnswer=function(correct){{
  var cur=S.quiz.qs[S.quiz.cur];
  updateSR(cur,correct);
  if(correct){{S.quiz.score++;addXP(5);}}
  S.quiz.cur++;S.quiz.ans=false;
  if(S.quiz.cur>=S.quiz.qs.length){{
    P.quizHistory.push({{date:new Date().toISOString().slice(0,10),level:S.level,type:'Spaced Rep',score:S.quiz.score,total:S.quiz.qs.length}});
    saveP();S.subTab='quizResult';render();
  }}else render();
}};
window.startWeakQuiz=function(){{
  var weak=getWeakAreas();
  if(!weak.length){{alert('Zayif alan yok, harika gidiyorsun!');return;}}
  var vocabWeak=weak.filter(function(w){{return w.type==='vocab';}});
  if(!vocabWeak.length){{alert('Kelime zayifligin yok! Gramere odaklan.');return;}}
  var all=[];var allPool=[];
  var cats=WORDS[S.level]?WORDS[S.level].categories:{{}};
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{allPool.push(w);}});}});
  vocabWeak.forEach(function(w){{w.words.forEach(function(wd){{all.push(wd);}});}});
  all=shuffle(all).slice(0,15);var qs=[];
  all.forEach(function(w){{
    var opts=[w.t];var others=allPool.filter(function(x){{return x.t!==w.t;}});
    others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].t);
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udcc9 '+w.e+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w}});
  }});
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Zayif Alan'}};
  S.subTab='quizRun';render();
}};

// ============ New Listening Starters ============
window.startSentListen=function(){{
  var data=LISTEN_SENT[S.level]||[];if(!data.length)return;
  var qs=shuffle(data.slice());
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Cumle Dinleme'}};
  S.subTab='sentListen';render();
  setTimeout(function(){{if(qs[0])speak(qs[0].s);}},500);
}};
window.startDialogListen=function(){{
  var data=LISTEN_DLG[S.level]||[];if(!data.length)return;
  var qs=shuffle(data.slice());
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Diyalog Anlama'}};
  S.subTab='dialogListen';render();
}};
window.startFillListen=function(){{
  var data=LISTEN_FILL[S.level]||[];if(!data.length)return;
  var qs=shuffle(data.slice());
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Bosluk Doldur'}};
  S.subTab='fillListen';render();
  var fullSent=qs[0].s.replace('___',qs[0].w);
  setTimeout(function(){{speak(fullSent);}},500);
}};
window.sentListenNext=function(){{
  S.quiz.cur++;S.quiz.ans=false;S.quiz.sel=-1;render();
  var cur=S.quiz.qs[S.quiz.cur];
  if(cur)setTimeout(function(){{speak(cur.s);}},400);
}};
window.dialogListenNext=function(){{
  S.quiz.cur++;S.quiz.ans=false;S.quiz.sel=-1;render();
}};
window.fillListenNext=function(){{
  S.quiz.cur++;S.quiz.ans=false;S.quiz.sel=-1;render();
  var cur=S.quiz.qs[S.quiz.cur];
  if(cur){{var fullSent=cur.s.replace('___',cur.w);setTimeout(function(){{speak(fullSent);}},400);}}
}};

// Click handlers for new listening types
document.addEventListener('click',function(e){{
  // Sentence listening answer
  if(e.target.dataset.sli!==undefined&&!S.quiz.ans){{
    var idx=parseInt(e.target.dataset.sli);
    S.quiz.sel=idx;
    var cur=S.quiz.qs[S.quiz.cur];
    if(idx===cur.a){{S.quiz.score++;addXP(8);}}
    S.quiz.ans=true;saveP();render();
  }}
  // Dialog listening answer
  if(e.target.dataset.dli!==undefined&&!S.quiz.ans){{
    var idx=parseInt(e.target.dataset.dli);
    S.quiz.sel=idx;
    var cur=S.quiz.qs[S.quiz.cur];
    if(idx===cur.a){{S.quiz.score++;addXP(10);}}
    S.quiz.ans=true;saveP();render();
  }}
  // Fill listening answer
  if(e.target.dataset.fli!==undefined&&!S.quiz.ans){{
    var idx=parseInt(e.target.dataset.fli);
    S.quiz.sel=idx;
    var cur=S.quiz.qs[S.quiz.cur];
    var correctIdx=cur.opts.indexOf(cur.w);
    if(idx===correctIdx){{S.quiz.score++;addXP(6);}}
    S.quiz.ans=true;saveP();render();
  }}
  // Matching quiz clicks
  if(e.target.dataset.ml!==undefined&&S.match){{
    var mli=parseInt(e.target.dataset.ml);
    if(S.match.matched[mli]!==undefined)return;
    S.matchSel=mli;render();
  }}
  if(e.target.dataset.mr!==undefined&&S.match&&S.matchSel>=0){{
    var mri=parseInt(e.target.dataset.mr);
    var done3=false;Object.keys(S.match.matched).forEach(function(k){{if(S.match.matched[k]===mri)done3=true;}});
    if(done3)return;
    var enW=S.match.left[S.matchSel];
    var trW=S.match.right[mri];
    var ok3=S.match.answers.some(function(a){{return a.e===enW&&a.t===trW;}});
    if(ok3){{S.match.matched[S.matchSel]=mri;addXP(5);}}
    S.matchSel=-1;render();
  }}
}});

// ============ WRITING FEEDBACK ============
window.analyzeWriting=function(){{
  var ta=document.getElementById('write-area');if(!ta)return;
  var text=ta.value.trim();if(!text){{alert('Once bir seyler yaz!');return;}}
  var words=text.split(/\\s+/).filter(function(w){{return w.length>0;}});
  var wc=words.length;
  var sentences=text.split(/[.!?]+/).filter(function(s){{return s.trim().length>0;}});
  var sc=sentences.length;
  var avgWPS=sc>0?Math.round(wc/sc*10)/10:0;
  var issues=[];
  if(text.charAt(0)!==text.charAt(0).toUpperCase())issues.push('Cumle buyuk harfle baslamali');
  if(!/[.!?]$/.test(text))issues.push('Cumle noktalama ile bitmeli');
  var repeated={{}};words.forEach(function(w){{var lw=w.toLowerCase();repeated[lw]=(repeated[lw]||0)+1;}});
  Object.keys(repeated).forEach(function(w){{if(repeated[w]>3&&w.length>3)issues.push('"'+w+'" kelimesi '+repeated[w]+' kez tekrarlandi');}});
  var targets={{A1:{{min:20,max:60}},A2:{{min:40,max:100}},B1:{{min:80,max:200}},B2:{{min:150,max:350}},C1:{{min:250,max:500}},C2:{{min:350,max:600}}}};
  var t=targets[S.level]||{{min:50,max:200}};
  var lengthOk=wc>=t.min&&wc<=t.max;
  var unique=Object.keys(repeated).length;
  var diversity=wc>0?Math.round(unique/wc*100):0;
  var fb='<div style="padding:16px;background:var(--card);border-radius:14px;border:1.5px solid rgba(99,102,241,.15);margin-top:16px">';
  fb+='<div style="font-weight:700;color:var(--accent1);margin-bottom:12px;font-size:.9rem">\\ud83d\\udcdd Yazma Analizi</div>';
  fb+='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px">';
  fb+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.05);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent1)">'+wc+'</div><div style="font-size:.68rem;color:var(--txt3)">Kelime</div></div>';
  fb+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.05);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent1)">'+sc+'</div><div style="font-size:.68rem;color:var(--txt3)">Cumle</div></div>';
  fb+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.05);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent1)">'+avgWPS+'</div><div style="font-size:.68rem;color:var(--txt3)">Ort. Kelime/Cumle</div></div>';
  fb+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.05);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:'+(diversity>60?'var(--grn)':'var(--red)')+'">%'+diversity+'</div><div style="font-size:.68rem;color:var(--txt3)">Kelime Cesitliligi</div></div>';
  fb+='</div>';
  fb+='<div style="font-size:.82rem;margin-bottom:8px;color:'+(lengthOk?'var(--grn)':'var(--org)')+'">'+(lengthOk?'\\u2705':'\\u26a0\\ufe0f')+' Kelime: '+wc+' ('+S.level+' hedef: '+t.min+'-'+t.max+')</div>';
  if(issues.length){{
    fb+='<div style="margin-top:10px;padding:10px;background:rgba(239,68,68,.05);border-radius:10px;border:1px solid rgba(239,68,68,.1)">';
    fb+='<div style="font-size:.78rem;font-weight:700;color:var(--red);margin-bottom:6px">\\u26a0\\ufe0f Dikkat:</div>';
    issues.forEach(function(is){{fb+='<div style="font-size:.78rem;color:var(--txt2);margin-bottom:3px">\\u2022 '+is+'</div>';}});
    fb+='</div>';
  }}else{{
    fb+='<div style="margin-top:10px;padding:10px;background:rgba(16,185,129,.05);border-radius:10px"><div style="font-size:.82rem;color:var(--grn)">\\u2705 Temel kontrollerde sorun yok!</div></div>';
  }}
  if(!P.writings)P.writings=[];
  P.writings.push({{date:new Date().toISOString().slice(0,10),level:S.level,words:wc,diversity:diversity}});
  addXP(Math.min(wc,50));saveP();
  fb+='<div style="margin-top:10px;font-size:.75rem;color:var(--txt3)">\\u2b50 +'+Math.min(wc,50)+' XP kazandin!</div></div>';
  var container=document.getElementById('write-feedback');
  if(container)container.innerHTML=fb;
  else{{var d=document.createElement('div');d.id='write-feedback';d.innerHTML=fb;ta.parentNode.appendChild(d);}}
}};
setInterval(function(){{
  var ta=document.getElementById('write-area');var wc=document.getElementById('wcount');
  if(ta&&wc){{var w=ta.value.trim().split(/\\s+/).filter(function(x){{return x.length>0;}});wc.textContent=w.length+' kelime';}}
}},500);

// ===================== SPEAKING MODULE =====================
var _recognition=null;
var _speechSupported=!!(window.SpeechRecognition||window.webkitSpeechRecognition);
function initSpeechRecognition(){{
  if(!_speechSupported)return;
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  _recognition=new SR();
  _recognition.lang='de-DE';_recognition.continuous=false;_recognition.interimResults=false;
  _recognition.maxAlternatives=3;
}}
if(_speechSupported)initSpeechRecognition();

var SPEAK_PROMPTS={{
  A1:['Hallo, ich hei\u00dfe...','Ich esse gerne...','Meine Lieblingsfarbe ist...','Ich wohne in...','Heute ist das Wetter...'],
  A2:['Erz\u00e4hlen Sie von Ihrem Tagesablauf.','Beschreiben Sie Ihre Familie.','Was haben Sie letztes Wochenende gemacht?','Was ist Ihr Lieblingshobby?','Beschreiben Sie das Wetter heute.'],
  B1:['Beschreiben Sie Ihr ideales Reiseziel.','Was sind die Vorteile des Deutschlernens?','Erz\u00e4hlen Sie von einem Buch oder Film.','Erkl\u00e4ren Sie die Bedeutung gesunder Ern\u00e4hrung.','Beschreiben Sie Ihre Heimatstadt.'],
  B2:['Diskutieren Sie den Einfluss sozialer Medien.','Vergleichen Sie Stadt- und Landleben.','Beschreiben Sie eine herausfordernde Situation.','Sprechen Sie \u00fcber Technologie in der Bildung.','Diskutieren Sie Umweltprobleme und L\u00f6sungen.'],
  C1:['Analysieren Sie die ethischen Implikationen der KI.','Diskutieren Sie Wirtschaftswachstum und Nachhaltigkeit.','Bewerten Sie internationale Organisationen.','Wie beeinflusst Globalisierung kulturelle Identit\u00e4t?','Diskutieren Sie die Zukunft der Arbeit.'],
  C2:['Kritisieren Sie die philosophischen Grundlagen der Menschenrechte.','Analysieren Sie Post-Truth-Politik.','Diskutieren Sie Quantencomputing und Kryptographie.','Bewerten Sie verschiedene Bewusstseinstheorien.','Analysieren Sie Sprache und Denken.']
}}


function renderSpeaking(){{
  var lv=S.level;
  var prompts=SPEAK_PROMPTS[lv]||[];
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  o+=h('div','shd',h('h3','hd','\\ud83c\\udfa4 '+lv+' Konusma Pratigi'));
  if(!_speechSupported){{
    o+='<div class="cd" style="text-align:center;padding:30px;color:var(--red)">\\u26a0\\ufe0f Tarayiciniz konusma tanima desteklemiyor. Chrome/Edge kullanin.</div>';
    return o;
  }}
  // Prompt selection
  o+='<div class="cd" style="margin-bottom:16px;padding:16px">';
  o+='<div style="font-size:.82rem;color:var(--accent1);font-weight:700;margin-bottom:8px">Konu Sec:</div>';
  prompts.forEach(function(p,i){{
    o+='<div class="qo" style="margin-bottom:6px;font-size:.85rem;'+(S.speakIdx===i?'border-color:var(--accent1);background:rgba(99,102,241,.06)':'')+'" onclick="S.speakIdx='+i+';render()">\\ud83d\\udccc '+p+'</div>';
  }});
  o+='</div>';
  // Recording area
  o+='<div class="cd" style="padding:24px;text-align:center">';
  o+='<div style="font-size:.9rem;color:var(--accent1);font-weight:600;margin-bottom:16px">'+prompts[S.speakIdx||0]+'</div>';
  o+='<div style="margin-bottom:16px">';
  o+='<button class="btn '+(S.recording?'btn-rd':'btn-g')+'" style="font-size:1rem;padding:16px 36px;border-radius:50px" onclick="'+(S.recording?'stopRecording()':'startRecording()')+'">'+
    (S.recording?'\\u23f9 Durdur':'\\ud83c\\udfa4 Konusmaya Basla')+'</button>';
  o+='</div>';
  if(S.recording){{
    o+='<div style="display:flex;align-items:center;justify-content:center;gap:8px;color:var(--red);font-size:.85rem;animation:pulse 1.5s infinite">\\ud83d\\udd34 Dinleniyor...</div>';
  }}
  if(S.spokenText){{
    o+='<div style="margin-top:16px;padding:16px;background:rgba(99,102,241,.04);border-radius:12px;border:1.5px solid rgba(99,102,241,.12)">';
    o+='<div style="font-size:.72rem;color:var(--txt3);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;font-weight:700">Algilanan Metin</div>';
    o+='<div style="font-size:1rem;color:var(--txt);line-height:1.6">'+S.spokenText+'</div>';
    o+='</div>';
    // Analysis
    var words=S.spokenText.split(/\\s+/).filter(function(w){{return w.length>0;}});
    var wc=words.length;
    var unique={{}};words.forEach(function(w){{unique[w.toLowerCase()]=1;}});
    var diversity=wc>0?Math.round(Object.keys(unique).length/wc*100):0;
    o+='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px">';
    o+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.04);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent1)">'+wc+'</div><div style="font-size:.68rem;color:var(--txt3)">Kelime</div></div>';
    o+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.04);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent2)">%'+diversity+'</div><div style="font-size:.68rem;color:var(--txt3)">Cesitlilik</div></div>';
    o+='<div style="text-align:center;padding:10px;background:rgba(99,102,241,.04);border-radius:10px"><div style="font-size:1.3rem;font-weight:800;color:var(--accent6)">'+Object.keys(unique).length+'</div><div style="font-size:.68rem;color:var(--txt3)">Benzersiz</div></div>';
    o+='</div>';
    o+='<div style="margin-top:12px"><button class="btn btn-g" onclick="speak(\\''+S.spokenText.replace(/'/g,"\\\\'").substring(0,200)+'\\')" style="margin-right:8px">\\ud83d\\udd0a Dogru Telaffuzu Dinle</button>';
    o+='<button class="btn btn-o" onclick="S.spokenText=\\'\\';render()">\\ud83d\\uddd1 Temizle</button></div>';
  }}
  o+='</div>';
  // Pronunciation practice section
  o+='<div class="cd" style="margin-top:16px;padding:16px">';
  o+='<div style="font-size:.88rem;font-weight:700;color:var(--accent1);margin-bottom:12px">\\ud83d\\udde3\\ufe0f Telaffuz Pratigi</div>';
  var practiceWords=[];
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};
  Object.keys(cats).forEach(function(c){{cats[c].slice(0,2).forEach(function(w){{practiceWords.push(w);}});}});
  practiceWords=shuffle(practiceWords).slice(0,8);
  o+='<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px">';
  practiceWords.forEach(function(w){{
    o+='<div class="cd" style="padding:10px 14px;display:flex;align-items:center;justify-content:space-between;cursor:pointer" onclick="speak(\\''+w.e.replace(/'/g,"\\\\'")+'\\')">';
    o+='<div><div style="font-size:.88rem;font-weight:700;color:var(--txt)">'+w.e+'</div><div style="font-size:.74rem;color:var(--txt3)">'+w.t+'</div></div>';
    o+='<span class="spk spks">\\ud83d\\udd0a</span></div>';
  }});
  o+='</div></div>';
  return o;
}}

// ===================== PHRASES MODULE =====================
function renderPhrases(){{
  var lv=S.level;
  var pvs=PHRASAL_VERBS[lv]||[];
  var ids=IDIOMS[lv]||[];
  var o='';
  o+='<div style="display:flex;gap:6px;margin-bottom:16px;flex-wrap:wrap">';
  LEVELS.forEach(function(l){{
    var ul=isUnlocked(l);
    o+='<button class="btn '+(S.level===l?'btn-g':'btn-o')+'" '+(ul?'onclick="setLevel(\\''+l+'\\')"':'disabled style="opacity:.4"')+'>'+l+'</button>';
  }});
  o+='</div>';
  // Sub tabs
  var psub=S.phraseSub||'phrasal';
  o+='<div style="display:flex;gap:8px;margin-bottom:16px">';
  o+='<button class="btn '+(psub==='phrasal'?'btn-g':'btn-o')+'" onclick="S.phraseSub=\\'phrasal\\';render()">Phrasal Verbs ('+pvs.length+')</button>';
  o+='<button class="btn '+(psub==='idioms'?'btn-g':'btn-o')+'" onclick="S.phraseSub=\\'idioms\\';render()">Idioms ('+ids.length+')</button>';
  o+='</div>';
  if(psub==='phrasal'){{
    o+=h('div','shd',h('h3','hd','\\ud83d\\udcac '+lv+' Phrasal Verbs'));
    if(!pvs.length){{o+='<div class="cd" style="text-align:center;padding:20px;color:var(--txt3)">Bu seviye icin icerik yakinda eklenecek.</div>';return o;}}
    o+='<div class="gram-scroll">';
    pvs.forEach(function(pv,i){{
      o+='<div class="cd" style="margin-bottom:10px;padding:14px">';
      o+='<div style="display:flex;justify-content:space-between;align-items:center">';
      o+='<div style="font-size:1rem;font-weight:800;color:var(--accent1)">'+pv.pv+'</div>';
      o+='<span class="spk spks" onclick="speak(\\''+pv.pv.replace(/'/g,"\\\\'")+'\\')" title="Dinle">\\ud83d\\udd0a</span></div>';
      o+='<div style="font-size:.85rem;color:var(--accent2);font-weight:600;margin:4px 0">'+pv.tr+'</div>';
      o+='<div style="font-size:.82rem;color:var(--txt2);padding:6px 10px;background:rgba(99,102,241,.04);border-radius:8px;margin-top:6px;font-style:italic">"'+pv.ex+'"</div>';
      o+='</div>';
    }});
    o+='</div>';
    // Practice quiz
    o+='<div style="margin-top:16px;text-align:center"><button class="btn btn-g" onclick="startPhrasalQuiz()">\\ud83c\\udfaf Phrasal Verb Quizi Baslat</button></div>';
  }}else{{
    o+=h('div','shd',h('h3','hd','\\ud83d\\udca1 '+lv+' Idioms'));
    if(!ids.length){{o+='<div class="cd" style="text-align:center;padding:20px;color:var(--txt3)">Bu seviye icin icerik yakinda eklenecek.</div>';return o;}}
    o+='<div class="gram-scroll">';
    ids.forEach(function(id2,i){{
      o+='<div class="cd" style="margin-bottom:10px;padding:14px">';
      o+='<div style="display:flex;justify-content:space-between;align-items:center">';
      o+='<div style="font-size:1rem;font-weight:800;color:var(--accent3)">'+id2.idiom+'</div>';
      o+='<span class="spk spks" onclick="speak(\\''+id2.idiom.replace(/'/g,"\\\\'")+'\\')" title="Dinle">\\ud83d\\udd0a</span></div>';
      o+='<div style="font-size:.82rem;color:var(--txt2);margin:4px 0"><b>Meaning:</b> '+id2.meaning+'</div>';
      o+='<div style="font-size:.85rem;color:var(--accent2);font-weight:600">'+id2.tr+'</div>';
      o+='<div style="font-size:.82rem;color:var(--txt2);padding:6px 10px;background:rgba(236,72,153,.04);border-radius:8px;margin-top:6px;font-style:italic">"'+id2.ex+'"</div>';
      o+='</div>';
    }});
    o+='</div>';
    o+='<div style="margin-top:16px;text-align:center"><button class="btn btn-g" onclick="startIdiomQuiz()">\\ud83c\\udfaf Idiom Quizi Baslat</button></div>';
  }}
  return o;
}}

// ===================== CERTIFICATE =====================
function generateCertificate(lv){{
  var li=LINFO[lv];
  var date=new Date().toLocaleDateString('tr-TR',{{year:'numeric',month:'long',day:'numeric'}});
  var certHTML='<div id="cert-preview" style="width:800px;padding:60px;background:linear-gradient(135deg,#94A3B8,#0B0F19);border:4px solid '+li.c+';border-radius:24px;text-align:center;margin:20px auto;position:relative;overflow:hidden">';
  certHTML+='<div style="position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,'+li.c+',#6366f1,#ec4899,'+li.c+')"></div>';
  certHTML+='<div style="font-size:3rem;margin-bottom:8px">'+li.i+'</div>';
  certHTML+='<div style="font-size:.8rem;color:#94a3b8;text-transform:uppercase;letter-spacing:6px;margin-bottom:8px">CERTIFICATE OF ACHIEVEMENT</div>';
  certHTML+='<div style="font-size:2.2rem;font-weight:900;background:linear-gradient(135deg,'+li.c+',#8b5cf6,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:16px 0">'+lv+' - '+li.t+'</div>';
  certHTML+='<div style="font-size:.9rem;color:#cbd5e1;margin:16px 0 8px">Bu sertifika</div>';
  certHTML+='<div style="font-size:1.5rem;font-weight:800;color:#1A2035;margin:8px 0 16px">'+USER+'</div>';
  certHTML+='<div style="font-size:.85rem;color:#94a3b8;line-height:1.8">CEFR '+lv+' ('+li.n+') seviyesini basariyla tamamladigini onaylar.<br>SmartCampus Kisisel Dil Gelisimi Platformu</div>';
  certHTML+='<div style="margin-top:24px;padding-top:20px;border-top:1px solid rgba(99,102,241,.2)">';
  certHTML+='<div style="font-size:.82rem;color:'+li.c+';font-weight:600">'+date+'</div>';
  certHTML+='<div style="font-size:.72rem;color:#64748b;margin-top:4px">SmartCampus CEFR Diamond Edition</div>';
  certHTML+='</div>';
  certHTML+='<div style="position:absolute;bottom:0;left:0;right:0;height:6px;background:linear-gradient(90deg,#ec4899,#6366f1,'+li.c+',#6366f1,#ec4899)"></div>';
  certHTML+='</div>';
  return certHTML;
}}

// ===================== PLACEMENT STARTERS =====================
window.startPlacement=function(){{
  var qs=genPlacement();
  S.placement={{qs:qs,cur:0,score:0,ans:false,sel:-1,done:false,answers:[],result:'',finished:false}};
  render();
}};
window.placementNext=function(){{
  var pt=S.placement;
  pt.answers.push({{lv:pt.qs[pt.cur].lv,correct:pt.sel===pt.qs[pt.cur].correct}});
  pt.cur++;pt.ans=false;pt.sel=-1;
  if(pt.cur>=pt.qs.length){{
    pt.done=true;
    pt.result=calcPlacementLevel(pt.answers);
    pt.score=pt.answers.filter(function(a){{return a.correct;}}).length;
  }}
  render();
}};
window.finishPlacement=function(){{
  P.placementDone=true;
  P.placementLevel=S.placement.result;
  S.level=S.placement.result;
  S.placement.finished=true;
  addXP(50);saveP();TAB='dash';render();
}};
// Placement test answer click handler
document.addEventListener('click',function(e){{
  if(e.target.dataset.pti!==undefined&&S.placement&&!S.placement.ans){{
    var idx=parseInt(e.target.dataset.pti);
    S.placement.sel=idx;
    S.placement.ans=true;
    if(idx===S.placement.qs[S.placement.cur].correct)S.placement.score++;
    render();
  }}
  // Grammar MCQ click handler
  if(e.target.dataset.gmcq!==undefined){{
    var eid2=e.target.dataset.gmcq;
    var gmi=parseInt(e.target.dataset.gmi);
    var gmc=parseInt(e.target.dataset.gmc);
    var ggidx=parseInt(e.target.dataset.ggidx);
    var allBtns=document.querySelectorAll('[data-gmcq="'+eid2+'"]');
    allBtns.forEach(function(b,bi){{b.classList.add('dis');if(bi===gmc)b.classList.add('ok');else if(bi===gmi&&gmi!==gmc)b.classList.add('no');}});
    if(gmi===gmc){{
      var lp=getLP(S.level);
      if(!lp.gramExDone)lp.gramExDone={{}};
      if(!lp.gramExDone[ggidx])lp.gramExDone[ggidx]={{}};
      var parts=eid2.split('_');var ei2=parseInt(parts[2]);
      lp.gramExDone[ggidx][ei2]=true;
      var gs=GRAMMAR[S.level]||[];var totalEx2=(gs[ggidx]&&gs[ggidx].exercises)?gs[ggidx].exercises.length:1;
      if(Object.keys(lp.gramExDone[ggidx]).length>=totalEx2)lp.gramDone[ggidx]=true;
      addXP(10);saveP();
    }}
  }}
  // Reading glossary click handler
  if(e.target.classList.contains('gloss-word')){{
    var popup=document.getElementById('gloss-popup');
    if(popup){{
      var word=e.target.dataset.word;var tr=e.target.dataset.tr;
      document.getElementById('gloss-en').textContent='\\ud83d\\udd0a '+word;
      document.getElementById('gloss-tr').textContent=tr;
      document.getElementById('gloss-speak').onclick=function(){{speak(word);}};
      popup.style.display='block';
      var rect=e.target.getBoundingClientRect();
      popup.style.position='fixed';popup.style.top=(rect.bottom+5)+'px';popup.style.left=rect.left+'px';
      speak(word);
      setTimeout(function(){{popup.style.display='none';}},4000);
    }}
  }}
}});

// ===================== DARK MODE TOGGLE =====================
window.toggleDark=function(){{
  P.darkMode=!P.darkMode;applyDark();saveP();render();
}};

// ===================== SPEAKING STARTERS =====================
window.startRecording=function(){{
  if(!_recognition)return;
  S.recording=true;S.spokenText='';render();
  _recognition.start();
  _recognition.onresult=function(evt){{
    var transcript='';
    for(var i=0;i<evt.results.length;i++)transcript+=evt.results[i][0].transcript;
    S.spokenText=transcript;S.recording=false;
    addXP(Math.min(transcript.split(/\\s+/).length,30));saveP();render();
  }};
  _recognition.onerror=function(){{S.recording=false;render();}};
  _recognition.onend=function(){{if(S.recording){{S.recording=false;render();}}}};
}};
window.stopRecording=function(){{
  if(_recognition)_recognition.stop();
  S.recording=false;render();
}};

// ===================== PHRASAL QUIZ STARTERS =====================
window.startPhrasalQuiz=function(){{
  var pvs=PHRASAL_VERBS[S.level]||[];if(!pvs.length)return;
  pvs=shuffle(pvs.slice());var qs=[];
  pvs.forEach(function(pv){{
    var opts=[pv.tr];
    var allPvs=PHRASAL_VERBS[S.level]||[];
    var others=allPvs.filter(function(x){{return x.tr!==pv.tr;}});
    others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].tr);
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udcac "'+pv.pv+'" ne demek?',opts:opts,correct:opts.indexOf(pv.tr),word:{{e:pv.pv,t:pv.tr}}}});
  }});
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Phrasal Verbs'}};
  S.subTab='quizRun';TAB='quiz';render();
}};
window.startIdiomQuiz=function(){{
  var ids=IDIOMS[S.level]||[];if(!ids.length)return;
  ids=shuffle(ids.slice());var qs=[];
  ids.forEach(function(id2){{
    var opts=[id2.meaning];
    var allIds=IDIOMS[S.level]||[];
    var others=allIds.filter(function(x){{return x.meaning!==id2.meaning;}});
    others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].meaning);
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udca1 "'+id2.idiom+'" means?',opts:opts,correct:opts.indexOf(id2.meaning),word:{{e:id2.idiom,t:id2.tr}}}});
  }});
  S.quiz={{qs:qs,cur:0,score:0,ans:false,sel:-1,type:'Idioms'}};
  S.subTab='quizRun';TAB='quiz';render();
}};

// ===================== CERTIFICATE STARTERS =====================
window.showCertificate=function(lv){{
  var certHTML=generateCertificate(lv);
  var modal=document.createElement('div');
  modal.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.7);z-index:999;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(6px)';
  modal.innerHTML='<div style="max-width:860px;width:95%;max-height:90vh;overflow-y:auto;position:relative">'+
    '<button onclick="this.parentElement.parentElement.remove()" style="position:absolute;top:10px;right:16px;background:rgba(255,255,255,.1);border:none;color:#fff;font-size:1.5rem;cursor:pointer;padding:4px 10px;border-radius:50%;z-index:1000">\\u2715</button>'+
    certHTML+
    '<div style="text-align:center;margin-top:16px"><button class="btn btn-g" onclick="downloadCert(\\''+lv+'\\')">\\ud83d\\udce5 Sertifikayi Indir</button></div>'+
    '</div>';
  document.body.appendChild(modal);
}};
window.downloadCert=function(lv){{
  var el=document.getElementById('cert-preview');if(!el)return;
  // Use canvas to create downloadable image
  var c=document.createElement('canvas');c.width=800;c.height=500;
  var ctx=c.getContext('2d');
  ctx.fillStyle='#0B0F19';ctx.fillRect(0,0,800,500);
  ctx.fillStyle='#6366f1';ctx.fillRect(0,0,800,6);ctx.fillRect(0,494,800,6);
  ctx.fillStyle='#1A2035';ctx.font='bold 14px sans-serif';ctx.textAlign='center';
  ctx.fillText('CERTIFICATE OF ACHIEVEMENT',400,80);
  ctx.font='bold 36px sans-serif';ctx.fillStyle='#8b5cf6';
  ctx.fillText(lv+' - '+LINFO[lv].t,400,160);
  ctx.fillStyle='#cbd5e1';ctx.font='16px sans-serif';
  ctx.fillText('Bu sertifika',400,220);
  ctx.fillStyle='#1A2035';ctx.font='bold 28px sans-serif';
  ctx.fillText(USER,400,260);
  ctx.fillStyle='#94a3b8';ctx.font='14px sans-serif';
  ctx.fillText('CEFR '+lv+' seviyesini basariyla tamamladigini onaylar.',400,310);
  ctx.fillText('SmartCampus Kisisel Dil Gelisimi Platformu',400,335);
  ctx.fillStyle='#6366f1';ctx.font='12px sans-serif';
  ctx.fillText(new Date().toLocaleDateString('tr-TR'),400,420);
  var link=document.createElement('a');link.download='SmartCampus_CEFR_'+lv+'_Certificate.png';
  link.href=c.toDataURL('image/png');link.click();
}};

// ===================== ENHANCED PROGRESS =====================
var _origRenderProgress=renderProgress;
renderProgress=function(){{
  var o=_origRenderProgress();
  // Time tracking analytics
  o+=h('div','shd',h('h3','hd','\\u23f0 Calisma Suresi'));
  o+='<div class="cd" style="padding:16px;margin-bottom:16px">';
  if(P.timeSpent){{
    var days=Object.keys(P.timeSpent).sort().slice(-7);
    if(days.length){{
      o+='<div style="display:flex;align-items:flex-end;gap:8px;height:120px;margin-bottom:12px">';
      var maxT=1;days.forEach(function(d){{if(P.timeSpent[d]>maxT)maxT=P.timeSpent[d];}});
      days.forEach(function(d){{
        var mins=Math.round(P.timeSpent[d]/60);
        var h2=Math.max(8,Math.round(P.timeSpent[d]/maxT*100));
        o+='<div style="flex:1;text-align:center">';
        o+='<div style="font-size:.68rem;color:var(--txt3);margin-bottom:4px">'+mins+'dk</div>';
        o+='<div style="height:'+h2+'px;background:linear-gradient(180deg,var(--accent1),var(--accent2));border-radius:6px 6px 0 0;transition:height .5s"></div>';
        o+='<div style="font-size:.62rem;color:var(--txt3);margin-top:4px">'+d.slice(5)+'</div>';
        o+='</div>';
      }});
      o+='</div>';
      var totalMins=0;Object.keys(P.timeSpent).forEach(function(d){{totalMins+=P.timeSpent[d];}});
      totalMins=Math.round(totalMins/60);
      o+='<div style="font-size:.82rem;color:var(--txt2)">Toplam: <b>'+totalMins+'</b> dakika | Son 7 gun gosteriliyor</div>';
    }}else{{o+='<div style="color:var(--txt3);font-size:.85rem">Henuz veri yok.</div>';}}
  }}
  o+='</div>';
  // Quiz accuracy trends
  o+=h('div','shd',h('h3','hd','\\ud83d\\udcc9 Quiz Basari Trendi'));
  o+='<div class="cd" style="padding:16px;margin-bottom:16px">';
  var recent=P.quizHistory.slice(-10);
  if(recent.length){{
    o+='<div style="display:flex;align-items:flex-end;gap:6px;height:100px;margin-bottom:12px">';
    recent.forEach(function(q,qi){{
      var pct2=q.total>0?Math.round(q.score/q.total*100):0;
      var barH=Math.max(8,pct2);
      var barCol=pct2>=80?'var(--grn)':pct2>=60?'var(--org)':'var(--red)';
      o+='<div style="flex:1;text-align:center">';
      o+='<div style="font-size:.62rem;color:var(--txt3);margin-bottom:2px">%'+pct2+'</div>';
      o+='<div style="height:'+barH+'px;background:'+barCol+';border-radius:4px 4px 0 0"></div>';
      o+='<div style="font-size:.58rem;color:var(--txt3);margin-top:2px">'+q.type.slice(0,4)+'</div>';
      o+='</div>';
    }});
    o+='</div>';
    var avgScore=0;recent.forEach(function(q){{avgScore+=q.total>0?q.score/q.total*100:0;}});
    avgScore=Math.round(avgScore/recent.length);
    o+='<div style="font-size:.82rem;color:var(--txt2)">Ortalama basari: <b style="color:'+(avgScore>=70?'var(--grn)':'var(--red)')+'">%'+avgScore+'</b> (son '+recent.length+' quiz)</div>';
  }}else{{o+='<div style="color:var(--txt3);font-size:.85rem">Henuz quiz yapilmamis.</div>';}}
  o+='</div>';
  // Certificate section
  o+=h('div','shd',h('h3','hd','\\ud83c\\udfc6 Sertifikalar'));
  o+='<div class="cd" style="padding:16px">';
  o+='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">';
  LEVELS.forEach(function(lv2){{
    var li=LINFO[lv2];var lp=P.levels[lv2];var passed=lp&&lp.examPassed;
    o+='<div style="text-align:center;padding:16px;border-radius:14px;border:1.5px solid '+(passed?li.c:'rgba(0,0,0,.06)')+';background:'+(passed?'rgba(99,102,241,.04)':'var(--card2)')+';transition:all .3s">';
    o+='<div style="font-size:2rem;margin-bottom:6px">'+li.i+'</div>';
    o+='<div style="font-size:.82rem;font-weight:700;color:'+(passed?li.c:'var(--txt3)')+'">'+lv2+' - '+li.t+'</div>';
    if(passed){{
      o+='<div style="margin-top:8px"><button class="btn btn-g" style="font-size:.72rem;padding:5px 14px" onclick="showCertificate(\\''+lv2+'\\')">\\ud83c\\udfc5 Sertifika</button></div>';
    }}else{{
      o+='<div style="font-size:.72rem;color:var(--txt3);margin-top:8px">\\ud83d\\udd12 Sinavi gecin</div>';
    }}
    o+='</div>';
  }});
  o+='</div></div>';
  return o;
}};

// ===================== INIT =====================
checkStreak();applyDark();saveP();render();
}})();
</script>
'''


_KDG_CSS = """<style>
/* font: sistem fontu kullaniliyor */
    *{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0B0F19;--card:#ffffff;--card2:#111827;--gold:#6366f1;--gl:#4f46e5;--gd:#818cf8;
--txt:#0B0F19;--txt2:#475569;--txt3:#94a3b8;--grn:#10b981;--red:#ef4444;--blu:#3b82f6;--org:#f59e0b;--r:16px;
--accent1:#6366f1;--accent2:#8b5cf6;--accent3:#ec4899;--accent4:#06b6d4;--accent5:#f59e0b;--accent6:#10b981;
--shadow-sm:0 1px 2px rgba(0,0,0,.05);--shadow:0 4px 6px -1px rgba(0,0,0,.07),0 2px 4px -2px rgba(0,0,0,.05);--shadow-lg:0 10px 15px -3px rgba(0,0,0,.08),0 4px 6px -4px rgba(0,0,0,.04);--shadow-xl:0 20px 25px -5px rgba(0,0,0,.08),0 8px 10px -6px rgba(0,0,0,.04)}
html,body{background:var(--bg);color:var(--txt);font-family:'Plus Jakarta Sans','Inter',system-ui,-apple-system,sans-serif;min-height:100vh;overflow-x:hidden;font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased}
body::before{content:'';position:fixed;top:-40%;right:-20%;width:80%;height:80%;pointer-events:none;z-index:0;
background:radial-gradient(ellipse,rgba(99,102,241,.06),transparent 70%)}
body::after{content:'';position:fixed;bottom:-30%;left:-20%;width:70%;height:70%;pointer-events:none;z-index:0;
background:radial-gradient(ellipse,rgba(236,72,153,.04),transparent 70%)}
.hd{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;letter-spacing:-.02em}
#kdg-app{max-width:1100px;margin:0 auto;padding:0 20px;position:relative;z-index:1}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:16px 0;margin-bottom:24px;position:relative}
.topbar::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.15),rgba(236,72,153,.1),transparent)}
.topbar .logo-text{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.4rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.topbar .logo-sub{font-size:.62rem;color:var(--txt3);letter-spacing:3px;text-transform:uppercase;font-weight:600}
.topbar .uinfo{font-size:.82rem;color:var(--txt2)}
.topbar .uinfo b{color:var(--accent1);font-weight:700}
.ntabs{display:flex;gap:6px;overflow-x:auto;padding:6px 0 16px;margin-bottom:20px;scrollbar-width:none}
.ntabs::-webkit-scrollbar{display:none}
.ntab{padding:10px 18px;border-radius:12px;cursor:pointer;font-size:.78rem;font-weight:600;color:var(--txt3);background:transparent;border:1.5px solid transparent;transition:all .3s cubic-bezier(.4,0,.2,1);white-space:nowrap;display:flex;align-items:center;gap:6px}
.ntab:hover{color:var(--txt2);background:rgba(99,102,241,.05);transform:translateY(-1px)}
.ntab.act{color:#fff;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-color:transparent;box-shadow:0 4px 15px rgba(99,102,241,.3),0 0 0 1px rgba(99,102,241,.1);transform:translateY(-1px)}
.cd{background:var(--card);border:1.5px solid rgba(0,0,0,.06);border-radius:var(--r);padding:22px;transition:all .3s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden;box-shadow:var(--shadow-sm)}
.cd::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent1),var(--accent2),var(--accent3));opacity:0;transition:opacity .3s}
.cd:hover{border-color:rgba(99,102,241,.15);box-shadow:var(--shadow-lg);transform:translateY(-2px)}
.cd:hover::before{opacity:1}
.cd-gold{border:1.5px solid rgba(99,102,241,.12);background:linear-gradient(135deg,rgba(99,102,241,.03),rgba(139,92,246,.02),rgba(236,72,153,.02),#ffffff)}
.btn{padding:10px 24px;border-radius:12px;border:none;font-weight:700;font-size:.82rem;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1);font-family:inherit;letter-spacing:.01em}
.btn-g{background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;box-shadow:0 4px 14px rgba(99,102,241,.3)}
.btn-g:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(99,102,241,.35)}
.btn-o{background:transparent;border:1.5px solid rgba(99,102,241,.25);color:var(--accent1);font-weight:600}
.btn-o:hover{background:rgba(99,102,241,.05);border-color:rgba(99,102,241,.4)}
.btn-gr{background:linear-gradient(135deg,#10b981,#059669);color:#fff;box-shadow:0 4px 14px rgba(16,185,129,.25)}
.btn-rd{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;box-shadow:0 4px 14px rgba(239,68,68,.25)}
.pb{height:8px;background:rgba(0,0,0,.06);border-radius:4px;overflow:hidden}
.pb .fl{height:100%;border-radius:4px;transition:width .6s cubic-bezier(.4,0,.2,1)}
.pb-g .fl{background:linear-gradient(90deg,#6366f1,#8b5cf6,#a78bfa)}
.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.g4{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
@media(max-width:768px){.g2,.g3{grid-template-columns:1fr}}
.stc{text-align:center;padding:20px 14px;border-radius:var(--r)}
.stc .si{font-size:2rem;margin-bottom:8px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.1))}
.stc .sv{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.8rem;font-weight:900;color:var(--accent1);margin-bottom:4px;letter-spacing:-.02em}
.stc .sl{font-size:.68rem;color:var(--txt3);text-transform:uppercase;letter-spacing:1.5px;font-weight:600}
.lvc{cursor:pointer;text-align:center;padding:20px 14px}
.lvc.lk{opacity:.35;cursor:not-allowed;filter:grayscale(.5)}
.lvc .lb{display:inline-block;padding:8px 22px;border-radius:24px;font-weight:800;font-size:.9rem;color:#fff;margin-bottom:10px;box-shadow:0 4px 14px rgba(0,0,0,.15);letter-spacing:.02em}
.lvc .ln{font-size:.78rem;color:var(--txt2);margin-bottom:6px;font-weight:500}
.lvc .lc{font-size:.7rem;color:var(--txt3);font-weight:600}
.ctc{cursor:pointer;display:flex;align-items:center;gap:16px;padding:16px 18px}
.ctc .ce{font-size:1.8rem;filter:drop-shadow(0 2px 4px rgba(0,0,0,.1))}
.ctc .ci{flex:1}
.ctc .cn{font-size:.9rem;font-weight:700;color:var(--txt);letter-spacing:-.01em}
.ctc .cs{font-size:.74rem;color:var(--txt3);margin-top:3px;font-weight:500}
.ctc .cb{font-size:.72rem;padding:5px 14px;border-radius:10px;font-weight:700}
.ctd{border-color:rgba(16,185,129,.2)!important;background:linear-gradient(145deg,rgba(16,185,129,.05),rgba(16,185,129,.02))!important}
.fcon{max-width:500px;margin:0 auto;perspective:1000px}
.fcrd{width:100%;min-height:260px;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all .5s cubic-bezier(.4,0,.2,1);background:#fff;border:2px solid rgba(99,102,241,.12);padding:40px;box-shadow:var(--shadow);position:relative}
.fcrd::before{content:'';position:absolute;top:-1px;left:15%;right:15%;height:3px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.5),rgba(139,92,246,.5),transparent);border-radius:2px}
.fcrd:hover{border-color:rgba(99,102,241,.25);box-shadow:var(--shadow-xl);transform:translateY(-4px)}
.fcl{font-size:.7rem;color:var(--txt3);text-transform:uppercase;letter-spacing:4px;margin-bottom:16px;font-weight:700}
.fcw{font-family:'Plus Jakarta Sans',sans-serif;font-size:2.4rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.fch{font-size:.72rem;color:var(--txt3);margin-top:20px;font-weight:500}
.fct{font-size:1.2rem;color:var(--txt2);font-style:italic;margin-top:8px}
.fce{font-size:.9rem;color:var(--txt3)}
.fcb{display:flex;gap:12px;justify-content:center;margin-top:20px}
.qw{max-width:600px;margin:0 auto}
.qst{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.1rem;font-weight:800;color:var(--accent1);margin-bottom:18px;line-height:1.5}
.qop{display:flex;flex-direction:column;gap:10px}
.qo{padding:14px 20px;border-radius:14px;border:1.5px solid rgba(0,0,0,.08);background:#111827;cursor:pointer;transition:all .25s cubic-bezier(.4,0,.2,1);font-size:.88rem;color:var(--txt);font-weight:500}
.qo:hover{border-color:rgba(99,102,241,.3);background:rgba(99,102,241,.04);transform:translateX(4px)}
.qo.ok{border-color:var(--grn);background:rgba(16,185,129,.08);color:#065f46;font-weight:600}
.qo.no{border-color:var(--red);background:rgba(239,68,68,.06);color:#991b1b;font-weight:600}
.qo.dis{pointer-events:none;opacity:.7}
.grc{margin-bottom:16px}
.grc h4{font-family:'Plus Jakarta Sans',sans-serif;color:var(--accent1);margin-bottom:10px;font-size:.95rem;font-weight:800}
.gru{background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(139,92,246,.04));border-left:3px solid var(--accent1);padding:12px 18px;border-radius:0 12px 12px 0;font-family:'Fira Code',Consolas,monospace;font-size:.82rem;color:var(--accent1);margin:12px 0;font-weight:500}
.gre{font-size:.84rem;color:var(--txt2);line-height:1.8;margin-bottom:12px}
.grx{font-size:.84rem;color:var(--txt2);padding:10px 16px;border-left:2px solid rgba(99,102,241,.2);margin:8px 0;background:rgba(248,250,252,.5);border-radius:0 8px 8px 0}
.grx b{color:#059669;font-weight:700}
.gin{background:#fff;border:1.5px solid rgba(0,0,0,.12);color:var(--txt);padding:10px 16px;border-radius:10px;font-size:.85rem;width:200px;font-family:inherit;outline:none;transition:all .2s}
.gin:focus{border-color:rgba(99,102,241,.5);box-shadow:0 0 0 3px rgba(99,102,241,.1)}
.gin.ok{border-color:var(--grn);background:rgba(16,185,129,.06);box-shadow:0 0 0 3px rgba(16,185,129,.08)}
.gin.no{border-color:var(--red);background:rgba(239,68,68,.04);box-shadow:0 0 0 3px rgba(239,68,68,.08)}
.rtx{background:#111827;border-radius:14px;padding:24px;line-height:2;font-size:.92rem;border:1.5px solid rgba(0,0,0,.05);color:var(--txt)}
.wta{width:100%;min-height:200px;background:#fff;border:1.5px solid rgba(0,0,0,.1);border-radius:14px;padding:18px;color:var(--txt);font-family:inherit;font-size:.9rem;line-height:1.8;resize:vertical;outline:none;transition:all .2s}
.wta:focus{border-color:rgba(99,102,241,.4);box-shadow:0 0 0 3px rgba(99,102,241,.08)}
.bdg{display:inline-flex;align-items:center;gap:6px;padding:7px 16px;border-radius:24px;font-size:.72rem;font-weight:700;border:1.5px solid rgba(0,0,0,.06);background:#111827;color:var(--txt3)}
.bdg.on{border-color:rgba(99,102,241,.3);background:linear-gradient(135deg,rgba(99,102,241,.08),rgba(139,92,246,.05));color:var(--accent1);box-shadow:0 2px 8px rgba(99,102,241,.1)}
.spk{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;border:1.5px solid rgba(99,102,241,.2);background:linear-gradient(135deg,rgba(99,102,241,.06),rgba(139,92,246,.04));cursor:pointer;font-size:1rem;transition:all .25s;vertical-align:middle}
.spk:hover{background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(139,92,246,.08));transform:scale(1.1);box-shadow:0 4px 12px rgba(99,102,241,.15)}
.spks{width:26px;height:26px;font-size:.78rem;border:1.5px solid rgba(0,0,0,.08);background:#111827}
.shd{display:flex;align-items:center;gap:12px;margin:24px 0 16px;padding-bottom:12px;border-bottom:1.5px solid rgba(99,102,241,.08);position:relative}
.shd::after{content:'';position:absolute;bottom:-1.5px;left:0;width:80px;height:3px;background:linear-gradient(90deg,var(--accent1),var(--accent2),transparent);border-radius:2px}
.shd h3{font-family:'Plus Jakarta Sans',sans-serif;color:var(--accent1);font-weight:800;letter-spacing:-.02em}
.rsc{text-align:center;padding:40px 20px}
.rsc .ri{font-size:4.5rem;margin-bottom:16px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.1))}
.rsc .rt{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.8rem;font-weight:900;margin-bottom:8px;color:var(--txt);letter-spacing:-.02em}
.rsc .rv{font-family:'Plus Jakarta Sans',sans-serif;font-size:3.2rem;font-weight:900;background:linear-gradient(135deg,#6366f1,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:16px 0}
.rsc .rm{font-size:.88rem;color:var(--txt2);margin-bottom:24px}
.bbk{cursor:pointer;padding:8px 16px;border-radius:10px;font-size:.8rem;background:transparent;border:1.5px solid rgba(99,102,241,.2);color:var(--accent1);transition:all .25s;font-family:inherit;font-weight:600}
.bbk:hover{background:rgba(99,102,241,.05);transform:translateX(-2px)}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
.shm{background:linear-gradient(90deg,#6366f1,#8b5cf6,#ec4899,#8b5cf6,#6366f1);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 4s ease infinite}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes glow{0%,100%{box-shadow:0 0 5px rgba(99,102,241,.2)}50%{box-shadow:0 0 20px rgba(99,102,241,.3)}}
.fade-up{animation:fadeUp .5s ease forwards}
::-webkit-scrollbar{width:10px}::-webkit-scrollbar-track{background:#e2e8f0;border-radius:5px}::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#6366f1,#8b5cf6);border-radius:5px;border:2px solid #e2e8f0}::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#4f46e5,#7c3aed)}
.din{width:100%;padding:14px 18px;background:#fff;border:1.5px solid rgba(0,0,0,.1);border-radius:12px;color:var(--txt);font-size:.9rem;font-family:inherit;outline:none;transition:all .2s}
.din:focus{border-color:rgba(99,102,241,.4);box-shadow:0 0 0 3px rgba(99,102,241,.08)}
.spbtn{padding:6px 14px;border-radius:10px;font-size:.76rem;cursor:pointer;border:1.5px solid rgba(0,0,0,.08);background:transparent;color:var(--txt2);transition:all .25s;font-weight:600}
.spbtn.act{border-color:rgba(99,102,241,.3);color:var(--accent1);background:rgba(99,102,241,.06)}
.spbtn:hover{border-color:rgba(99,102,241,.2);background:rgba(99,102,241,.03)}
.gram-scroll{max-height:65vh;overflow-y:scroll!important;padding-right:12px;scroll-behavior:smooth;scrollbar-width:auto;scrollbar-color:#6366f1 #e2e8f0;border-right:3px solid transparent}
.gram-scroll::-webkit-scrollbar{width:14px!important;display:block!important}
.gram-scroll::-webkit-scrollbar-track{background:#e2e8f0;border-radius:7px;border:2px solid #0B0F19}
.gram-scroll::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#6366f1,#8b5cf6,#ec4899);border-radius:7px;border:2px solid #e2e8f0;min-height:60px}
.gram-scroll::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#4f46e5,#7c3aed,#db2777);box-shadow:0 0 8px rgba(99,102,241,.5)}
.gloss-word{text-decoration:underline dotted rgba(99,102,241,.4);cursor:help;transition:all .2s;border-radius:2px;padding:0 2px}
.gloss-word:hover{background:rgba(99,102,241,.1);text-decoration-color:var(--accent1);color:var(--accent1)}
</style>"""

