# -*- coding: utf-8 -*-
"""Kisisel Dil Gelisimi (KDG) Engine - CEFR Uyumlu Diamond Premium Platform."""
import json
import os


def _load_cefr_data():
    """Load word and grammar JSON files."""
    base = os.path.join(os.path.dirname(__file__), "..", "data", "english")
    w_path = os.path.join(base, "cefr_words.json")
    g_path = os.path.join(base, "cefr_grammar.json")
    with open(w_path, "r", encoding="utf-8") as f:
        words = json.load(f)
    with open(g_path, "r", encoding="utf-8") as f:
        grammar = json.load(f)
    return words, grammar


def build_kdg_html(username: str = "misafir") -> str:
    """Kisisel Dil Gelisimi tam HTML/JS uygulamasi dondurur."""
    words, grammar = _load_cefr_data()
    wj = json.dumps(words, ensure_ascii=False)
    gj = json.dumps(grammar, ensure_ascii=False)
    u = username.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    return _KDG_CSS + _kdg_body(u, wj, gj)



def build_ortaokul_html(username: str = "misafir", grade: str = "5",
                         sublevel: str = "A2.1") -> str:
    """Ortaokul sinif bazli KDG - her sinifa ozel A2 alt-seviye icerigi."""
    import json as _json
    username_grade = f"{username}_ortaokul_{grade}"
    _GRADE_WORDS = {
        "0": {
            "Renkler \U0001f3a8": [
                {"t":"k\u0131rm\u0131z\u0131","e":"red"},{"t":"mavi","e":"blue"},{"t":"sar\u0131","e":"yellow"},
                {"t":"ye\u015fil","e":"green"},{"t":"turuncu","e":"orange"},{"t":"mor","e":"purple"},
                {"t":"pembe","e":"pink"},{"t":"siyah","e":"black"},{"t":"beyaz","e":"white"},{"t":"kahverengi","e":"brown"}
            ],
            "Hayvanlar \U0001f43e": [
                {"t":"kedi","e":"cat"},{"t":"k\u00f6pek","e":"dog"},{"t":"ku\u015f","e":"bird"},
                {"t":"bal\u0131k","e":"fish"},{"t":"tav\u015fan","e":"rabbit"},{"t":"kaplumba\u011fa","e":"turtle"},
                {"t":"kelebek","e":"butterfly"},{"t":"inek","e":"cow"},{"t":"at","e":"horse"},{"t":"tavuk","e":"chicken"}
            ],
            "Aile \U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466": [
                {"t":"anne","e":"mum"},{"t":"baba","e":"dad"},{"t":"karde\u015f","e":"sibling"},
                {"t":"b\u00fcy\u00fckanne","e":"grandma"},{"t":"b\u00fcy\u00fckbaba","e":"grandpa"},{"t":"bebek","e":"baby"},
                {"t":"aile","e":"family"},{"t":"ev","e":"home"},{"t":"sevgi","e":"love"},{"t":"mutlu","e":"happy"}
            ],
            "Say\u0131lar \U0001f522": [
                {"t":"bir","e":"one"},{"t":"iki","e":"two"},{"t":"\u00fc\u00e7","e":"three"},
                {"t":"d\u00f6rt","e":"four"},{"t":"be\u015f","e":"five"},{"t":"alt\u0131","e":"six"},
                {"t":"yedi","e":"seven"},{"t":"sekiz","e":"eight"},{"t":"dokuz","e":"nine"},{"t":"on","e":"ten"}
            ],
            "Meyveler \U0001f34e": [
                {"t":"elma","e":"apple"},{"t":"muz","e":"banana"},{"t":"portakal","e":"orange"},
                {"t":"\u00e7ilek","e":"strawberry"},{"t":"\u00fcz\u00fcm","e":"grape"},{"t":"karpuz","e":"watermelon"},
                {"t":"armut","e":"pear"},{"t":"kiraz","e":"cherry"},{"t":"\u015feftali","e":"peach"},{"t":"limon","e":"lemon"}
            ],
        },
        "5": {
            "Seyahat \u2708\ufe0f": [
                {"t":"havaalani","e":"airport"},{"t":"otel","e":"hotel"},{"t":"bilet","e":"ticket"},{"t":"pasaport","e":"passport"},
                {"t":"bavul","e":"suitcase"},{"t":"ucak","e":"airplane"},{"t":"tren","e":"train"},{"t":"otobus","e":"bus"},
                {"t":"taksi","e":"taxi"},{"t":"gemi","e":"ship"},{"t":"harita","e":"map"},{"t":"rehber","e":"guide"},
                {"t":"rezervasyon","e":"reservation"},{"t":"gidis","e":"departure"},{"t":"varis","e":"arrival"},
                {"t":"gumruk","e":"customs"},{"t":"vize","e":"visa"},{"t":"tur","e":"tour"},{"t":"plaj","e":"beach"},{"t":"muze","e":"museum"}
            ],
            "Alisveris \U0001f6d2": [
                {"t":"magaza","e":"store"},{"t":"fiyat","e":"price"},{"t":"ucuz","e":"cheap"},{"t":"pahali","e":"expensive"},
                {"t":"indirim","e":"discount"},{"t":"kasa","e":"cashier"},{"t":"para","e":"money"},{"t":"kredi karti","e":"credit card"},
                {"t":"market","e":"supermarket"},{"t":"fis","e":"receipt"},{"t":"odeme","e":"payment"},{"t":"beden","e":"size"},
                {"t":"renk","e":"color"},{"t":"hediye","e":"gift"},{"t":"canta","e":"bag"},{"t":"satici","e":"seller"},
                {"t":"musteri","e":"customer"},{"t":"vitrin","e":"shop window"},{"t":"deneme kabini","e":"fitting room"},{"t":"iade","e":"refund"}
            ],
            "Saglik \U0001f3e5": [
                {"t":"hastane","e":"hospital"},{"t":"doktor","e":"doctor"},{"t":"hemsire","e":"nurse"},{"t":"ilac","e":"medicine"},
                {"t":"eczane","e":"pharmacy"},{"t":"ates","e":"fever"},{"t":"bas agrisi","e":"headache"},{"t":"oksuruk","e":"cough"},
                {"t":"grip","e":"flu"},{"t":"alerji","e":"allergy"},{"t":"recete","e":"prescription"},{"t":"ameliyat","e":"surgery"},
                {"t":"acil","e":"emergency"},{"t":"ambulans","e":"ambulance"},{"t":"dis hekimi","e":"dentist"},
                {"t":"goz doktoru","e":"eye doctor"},{"t":"kan","e":"blood"},{"t":"bandaj","e":"bandage"},
                {"t":"agri","e":"pain"},{"t":"iyilesmek","e":"to recover"}
            ],
        },
        "6": {
            "Hobiler \U0001f3ae": [
                {"t":"yuzmek","e":"swimming"},{"t":"kosmak","e":"running"},{"t":"okumak","e":"reading"},{"t":"muzik","e":"music"},
                {"t":"resim yapmak","e":"painting"},{"t":"dans","e":"dancing"},{"t":"fotograf","e":"photography"},
                {"t":"bahcecilik","e":"gardening"},{"t":"yemek pisirmek","e":"cooking"},{"t":"seyahat","e":"traveling"},
                {"t":"satranc","e":"chess"},{"t":"bisiklet","e":"cycling"},{"t":"balik tutmak","e":"fishing"},
                {"t":"kamp","e":"camping"},{"t":"yuruyus","e":"hiking"},{"t":"yoga","e":"yoga"},
                {"t":"film izlemek","e":"watching movies"},{"t":"alisveris","e":"shopping"},{"t":"dikis","e":"sewing"},
                {"t":"koleksiyon","e":"collecting"}
            ],
            "Meslekler \U0001f4bc": [
                {"t":"muhendis","e":"engineer"},{"t":"avukat","e":"lawyer"},{"t":"mimar","e":"architect"},
                {"t":"polis","e":"police officer"},{"t":"itfaiyeci","e":"firefighter"},{"t":"asci","e":"chef"},
                {"t":"garson","e":"waiter"},{"t":"pilot","e":"pilot"},{"t":"sofor","e":"driver"},{"t":"gazeteci","e":"journalist"},
                {"t":"programci","e":"programmer"},{"t":"muhasebeci","e":"accountant"},{"t":"eczaci","e":"pharmacist"},
                {"t":"ciftci","e":"farmer"},{"t":"kasap","e":"butcher"},{"t":"berber","e":"barber"},
                {"t":"terzi","e":"tailor"},{"t":"mudur","e":"manager"},{"t":"sekreter","e":"secretary"},{"t":"asker","e":"soldier"}
            ],
            "Sehir \U0001f3d9\ufe0f": [
                {"t":"park","e":"park"},{"t":"restoran","e":"restaurant"},{"t":"banka","e":"bank"},{"t":"postane","e":"post office"},
                {"t":"kutuphane","e":"library"},{"t":"sinema","e":"cinema"},{"t":"tiyatro","e":"theater"},{"t":"stadyum","e":"stadium"},
                {"t":"kopru","e":"bridge"},{"t":"cadde","e":"street"},{"t":"sokak","e":"alley"},{"t":"meydan","e":"square"},
                {"t":"bina","e":"building"},{"t":"apartman","e":"apartment"},{"t":"otopark","e":"parking lot"},
                {"t":"trafik","e":"traffic"},{"t":"kavsak","e":"intersection"},{"t":"kaldirim","e":"sidewalk"},
                {"t":"durak","e":"bus stop"},{"t":"istasyon","e":"station"}
            ],
        },
        "7": {
            "Duygular \U0001f4ad": [
                {"t":"mutlu","e":"happy"},{"t":"uzgun","e":"sad"},{"t":"kizgin","e":"angry"},{"t":"korkmus","e":"scared"},
                {"t":"saskin","e":"surprised"},{"t":"heyecanli","e":"excited"},{"t":"yorgun","e":"tired"},
                {"t":"endiseli","e":"worried"},{"t":"gururlu","e":"proud"},{"t":"utangac","e":"shy"},
                {"t":"kiskanc","e":"jealous"},{"t":"sinirli","e":"nervous"},{"t":"umutlu","e":"hopeful"},
                {"t":"yalniz","e":"lonely"},{"t":"huzurlu","e":"peaceful"},{"t":"cesaretli","e":"brave"},
                {"t":"merakli","e":"curious"},{"t":"sabirli","e":"patient"},{"t":"minnettar","e":"grateful"},
                {"t":"hayal kirikligi","e":"disappointed"}
            ],
            "Doga \U0001f33f": [
                {"t":"agac","e":"tree"},{"t":"cicek","e":"flower"},{"t":"dag","e":"mountain"},{"t":"nehir","e":"river"},
                {"t":"gol","e":"lake"},{"t":"deniz","e":"sea"},{"t":"orman","e":"forest"},{"t":"col","e":"desert"},
                {"t":"ada","e":"island"},{"t":"vadi","e":"valley"},{"t":"selale","e":"waterfall"},{"t":"toprak","e":"soil"},
                {"t":"kaya","e":"rock"},{"t":"kum","e":"sand"},{"t":"gokyuzu","e":"sky"},{"t":"yildiz","e":"star"},
                {"t":"ay","e":"moon"},{"t":"gunes","e":"sun"},{"t":"gokkusagi","e":"rainbow"},{"t":"volkan","e":"volcano"}
            ],
        },
        "8": {
            "Gunluk Rutin \U0001f550": [
                {"t":"uyanmak","e":"to wake up"},{"t":"kalkmak","e":"to get up"},{"t":"dus almak","e":"to take a shower"},
                {"t":"giyinmek","e":"to get dressed"},{"t":"kahvalti","e":"breakfast"},{"t":"ogle yemegi","e":"lunch"},
                {"t":"aksam yemegi","e":"dinner"},{"t":"uyumak","e":"to sleep"},{"t":"calismak","e":"to work"},
                {"t":"dinlenmek","e":"to rest"},{"t":"temizlemek","e":"to clean"},{"t":"yikamak","e":"to wash"},
                {"t":"utu yapmak","e":"to iron"},{"t":"alisveris yapmak","e":"to shop"},{"t":"egzersiz","e":"exercise"},
                {"t":"dis fircalamak","e":"to brush teeth"},{"t":"yemek yapmak","e":"to cook"},
                {"t":"televizyon izlemek","e":"to watch TV"},{"t":"gazete okumak","e":"to read newspaper"},
                {"t":"yatmak","e":"to go to bed"}
            ],
            "Giyim \U0001f454": [
                {"t":"gomlek","e":"shirt"},{"t":"pantolon","e":"trousers"},{"t":"elbise","e":"dress"},{"t":"etek","e":"skirt"},
                {"t":"ceket","e":"jacket"},{"t":"mont","e":"coat"},{"t":"ayakkabi","e":"shoe"},{"t":"cizme","e":"boot"},
                {"t":"sapka","e":"hat"},{"t":"eldiven","e":"glove"},{"t":"atki","e":"scarf"},{"t":"kravat","e":"tie"},
                {"t":"corap","e":"sock"},{"t":"ic camasiri","e":"underwear"},{"t":"mayo","e":"swimsuit"},
                {"t":"esofman","e":"tracksuit"},{"t":"kazak","e":"sweater"},{"t":"yelek","e":"vest"},
                {"t":"terlik","e":"slipper"},{"t":"kemer","e":"belt"}
            ],
        },
        "9": {
            "Akademik Kelimeler \U0001f4da": [
                {"t":"burs","e":"scholarship"},{"t":"ders programi","e":"curriculum"},{"t":"donem","e":"semester"},
                {"t":"not ortalamasi","e":"GPA"},{"t":"mezuniyet","e":"graduation"},{"t":"yurt disi","e":"abroad"},
                {"t":"basvuru","e":"application"},{"t":"arastirma","e":"research"},{"t":"laboratuvar","e":"laboratory"},
                {"t":"akademik","e":"academic"},{"t":"odev","e":"assignment"},{"t":"tartisma","e":"debate"},
                {"t":"son tarih","e":"deadline"},{"t":"diploma","e":"diploma"},{"t":"deneme","e":"essay"},
                {"t":"degisim","e":"exchange"},{"t":"fakulte","e":"faculty"},{"t":"yuksek lisans","e":"master's degree"},
                {"t":"doktora","e":"PhD"},{"t":"profesor","e":"professor"}
            ],
            "Teknoloji \U0001f4f1": [
                {"t":"sosyal medya","e":"social media"},{"t":"uygulama","e":"application"},{"t":"yapay zeka","e":"AI"},
                {"t":"siber guvenlik","e":"cybersecurity"},{"t":"dijital okuryazarlik","e":"digital literacy"},
                {"t":"veri","e":"data"},{"t":"algoritma","e":"algorithm"},{"t":"gizlilik","e":"privacy"},
                {"t":"icerik","e":"content"},{"t":"yayin","e":"broadcast"},{"t":"haber kaynagi","e":"news source"},
                {"t":"gazetecilik","e":"journalism"},{"t":"medya okuryazarligi","e":"media literacy"},
                {"t":"dezenformasyon","e":"misinformation"},{"t":"cevrimici","e":"online"},
                {"t":"platform","e":"platform"},{"t":"takipci","e":"follower"},{"t":"paylasim","e":"sharing"},
                {"t":"sanal","e":"virtual"},{"t":"gerceklik","e":"reality"}
            ],
        },
        "10": {
            "Kariyer \U0001f4bc": [
                {"t":"kariyer","e":"career"},{"t":"ozgecmis","e":"CV/resume"},{"t":"mulakat","e":"interview"},
                {"t":"deneyim","e":"experience"},{"t":"nitelik","e":"qualification"},{"t":"maas","e":"salary"},
                {"t":"isveren","e":"employer"},{"t":"calisan","e":"employee"},{"t":"staj","e":"internship"},
                {"t":"girisimci","e":"entrepreneur"},{"t":"yonetici","e":"manager"},{"t":"departman","e":"department"},
                {"t":"sirket","e":"corporation"},{"t":"toplanti","e":"meeting"},{"t":"sunum","e":"presentation"},
                {"t":"hedef","e":"goal"},{"t":"strateji","e":"strategy"},{"t":"butce","e":"budget"},
                {"t":"gelir","e":"income"},{"t":"yatirim","e":"investment"}
            ],
            "Cevre \U0001f30d": [
                {"t":"iklim degisikligi","e":"climate change"},{"t":"kuresel isinma","e":"global warming"},
                {"t":"geri donusum","e":"recycling"},{"t":"surdurulebilir","e":"sustainable"},
                {"t":"kirlilik","e":"pollution"},{"t":"yenilenebilir enerji","e":"renewable energy"},
                {"t":"karbon ayak izi","e":"carbon footprint"},{"t":"ekosistem","e":"ecosystem"},
                {"t":"biyocesitlilik","e":"biodiversity"},{"t":"nesli tukenmek","e":"endangered"},
                {"t":"sera etkisi","e":"greenhouse effect"},{"t":"dogal kaynak","e":"natural resource"},
                {"t":"atik","e":"waste"},{"t":"enerji tasarrufu","e":"energy saving"},
                {"t":"organik","e":"organic"},{"t":"koruma","e":"conservation"},
                {"t":"tuketim","e":"consumption"},{"t":"azaltmak","e":"reduce"},
                {"t":"yeniden kullanmak","e":"reuse"},{"t":"donusturmek","e":"transform"}
            ],
        },
        "11": {
            "Akademik Yazim \U0001f4dd": [
                {"t":"tez","e":"thesis"},{"t":"hipotez","e":"hypothesis"},{"t":"arguman","e":"argument"},
                {"t":"kanit","e":"evidence"},{"t":"alinti","e":"quotation"},{"t":"kaynak","e":"source"},
                {"t":"dipnot","e":"footnote"},{"t":"bibliyografya","e":"bibliography"},{"t":"ozet","e":"abstract"},
                {"t":"giris","e":"introduction"},{"t":"sonuc","e":"conclusion"},{"t":"analiz","e":"analysis"},
                {"t":"sentez","e":"synthesis"},{"t":"elestiri","e":"criticism"},{"t":"degerlendirme","e":"evaluation"},
                {"t":"karsilastirma","e":"comparison"},{"t":"siniflandirma","e":"classification"},
                {"t":"tanim","e":"definition"},{"t":"aciklama","e":"explanation"},{"t":"tartisma","e":"discussion"}
            ],
            "Bilim \U0001f52c": [
                {"t":"deney","e":"experiment"},{"t":"gozlem","e":"observation"},{"t":"teori","e":"theory"},
                {"t":"kesif","e":"discovery"},{"t":"icat","e":"invention"},{"t":"yenilik","e":"innovation"},
                {"t":"teknoloji","e":"technology"},{"t":"muhendislik","e":"engineering"},
                {"t":"biyoteknoloji","e":"biotechnology"},{"t":"genetik","e":"genetics"},
                {"t":"uzay","e":"space"},{"t":"evren","e":"universe"},{"t":"gezegen","e":"planet"},
                {"t":"iklim","e":"climate"},{"t":"enerji","e":"energy"},{"t":"atom","e":"atom"},
                {"t":"molekul","e":"molecule"},{"t":"hucre","e":"cell"},{"t":"evrim","e":"evolution"},
                {"t":"yapay zeka","e":"artificial intelligence"}
            ],
        },
        "12": {
            "Universite Hazirlik \U0001f393": [
                {"t":"basvuru formu","e":"application form"},{"t":"kabul mektubu","e":"acceptance letter"},
                {"t":"burs","e":"scholarship"},{"t":"kampus","e":"campus"},{"t":"yurt","e":"dormitory"},
                {"t":"kayit","e":"enrollment"},{"t":"akademik danisman","e":"academic advisor"},
                {"t":"transkript","e":"transcript"},{"t":"kredi","e":"credit"},{"t":"secmeli ders","e":"elective"},
                {"t":"zorunlu ders","e":"compulsory"},{"t":"laboratuvar","e":"laboratory"},
                {"t":"kutuphane","e":"library"},{"t":"seminer","e":"seminar"},{"t":"konferans","e":"conference"},
                {"t":"arastirma gorevlisi","e":"research assistant"},{"t":"dekan","e":"dean"},
                {"t":"rektor","e":"rector"},{"t":"lisansustu","e":"postgraduate"},{"t":"bolum","e":"department"}
            ],
            "Is Ingilizcesi \U0001f4b0": [
                {"t":"muzakere","e":"negotiation"},{"t":"sozlesme","e":"contract"},{"t":"fatura","e":"invoice"},
                {"t":"kar","e":"profit"},{"t":"zarar","e":"loss"},{"t":"pazar","e":"market"},
                {"t":"musteri","e":"client"},{"t":"tedarikci","e":"supplier"},{"t":"lojistik","e":"logistics"},
                {"t":"ihracat","e":"export"},{"t":"ithalat","e":"import"},{"t":"doviz","e":"foreign exchange"},
                {"t":"borsa","e":"stock market"},{"t":"sigorta","e":"insurance"},{"t":"vergi","e":"tax"},
                {"t":"reklam","e":"advertisement"},{"t":"marka","e":"brand"},{"t":"patent","e":"patent"},
                {"t":"telif hakki","e":"copyright"},{"t":"ticaret","e":"trade"}
            ],
        },
    }
    _GRADE_GRAMMAR = {
        "0": [{"n":"Hello & Goodbye","f":"Hi! / Hello! / Bye! / Goodbye!","x":"Merhaba! \u2192 <b>Hello!</b>","e":"Selamlasma ve vedalasma kaliplari."},
              {"n":"I like... / I have...","f":"I like + nesne / I have + nesne","x":"Kedileri severim \u2192 I <b>like</b> cats.","e":"Basit cumle kaliplari."}],
        "5": [{"n":"Past Simple","f":"Subject + Verb-ed / V2","x":"Dun gittim \u2192 I <b>went</b> yesterday.","e":"Gecmiste tamamlanmis eylemler."},
              {"n":"Future (will / going to)","f":"will + verb / am-is-are going to + verb","x":"Yarin gelecek \u2192 She <b>will</b> come tomorrow.","e":"Will ani kararlar, going to planlanmis eylemler."}],
        "6": [{"n":"Comparatives","f":"adj+er/more adj | the adj+est/the most adj","x":"Daha buyuk \u2192 <b>bigger</b>","e":"Kisa sifatlara -er/-est eklenir."},
              {"n":"Present Continuous","f":"Subject + am/is/are + Verb-ing","x":"Su an okuyorum \u2192 I <b>am reading</b> now.","e":"Su anda devam eden eylemler."}],
        "7": [{"n":"Modal Verbs","f":"must / should / have to + base verb","x":"Calismasin \u2192 You <b>should</b> study.","e":"Must zorunluluk, should tavsiye."},
              {"n":"Countable & Uncountable","f":"countable: a/an, many, few | uncountable: much, little","x":"Cok su \u2192 <b>much</b> water","e":"Sayilabilen isimler cogul olabilir."}],
        "8": [{"n":"Adverbs of Frequency","f":"always > usually > often > sometimes > rarely > never","x":"Her zaman erken kalkarim \u2192 I <b>always</b> wake up early.","e":"Siklik zarflari genellikle fiilden once gelir."},
              {"n":"Conjunctions","f":"and / but / or / because","x":"Yorgunum ama mutluyum \u2192 I am tired <b>but</b> happy.","e":"Baglaclar cumleleri birbirine baglar."}],
        "9": [{"n":"Present Perfect","f":"have/has + V3","x":"Uc ulke ziyaret ettim \u2192 I <b>have visited</b> three countries.","e":"Gecmiste baslayip etkisi devam eden eylemler."},
              {"n":"Conditionals Type 2","f":"If + Past Simple, would + V1","x":"Param olsa seyahat ederdim \u2192 If I <b>had</b> money, I <b>would travel</b>.","e":"Gerceklesmesi dusuk durumlar."}],
        "10": [{"n":"Past Perfect","f":"had + V3","x":"O gelmeden yemistim \u2192 I <b>had eaten</b> before she arrived.","e":"Gecmiste bir olaydan once tamamlanan eylemler."},
               {"n":"Passive Voice","f":"be + V3","x":"Yeni okul insa ediliyor \u2192 A new school <b>is being built</b>.","e":"Eylemi yapanin degil etkilenenin onemli oldugu durumlar."}],
        "11": [{"n":"Conditionals Type 3","f":"If + Past Perfect, would have + V3","x":"Calissaydim gecerdim \u2192 If I <b>had studied</b>, I <b>would have passed</b>.","e":"Gecmiste gerceklesmemis durumlar."},
               {"n":"Causative Structures","f":"have/get + object + V3","x":"Arabami tamir ettirdim \u2192 I <b>had</b> my car <b>repaired</b>.","e":"Bir isi baskasina yaptirma."}],
        "12": [{"n":"Mixed Conditionals","f":"If + Past Perfect, would + V1","x":"Tip okusaydim simdi doktor olurdum \u2192 If I <b>had studied</b> medicine, I <b>would be</b> a doctor.","e":"Farkli zamanlardaki kosul ve sonuclari birlestirir."},
               {"n":"Subjunctive","f":"suggest/recommend + (that) + base form","x":"Daha cok calismasini oneririm \u2192 I suggest that he <b>study</b> harder.","e":"suggest, recommend gibi fiillerden sonra yali fiil kullanilir."}],
    }
    _GRADE_INFO = {
        "0": {"name": "Pre-A1 \u2014 Okul Oncesi", "color": "#f59e0b", "icon": "\U0001f9d2"},
        "5": {"name": "A2.1 \u2014 Temel Iletisim", "color": "#4caf50", "icon": "\U0001f4d7"},
        "6": {"name": "A2.2 \u2014 Gelisim", "color": "#2196f3", "icon": "\U0001f4d8"},
        "7": {"name": "A2.3 \u2014 Pekistirme", "color": "#ff9800", "icon": "\U0001f4d9"},
        "8": {"name": "A2.4 \u2014 Tamamlama", "color": "#f44336", "icon": "\U0001f4d5"},
        "9": {"name": "B1.1 \u2014 Bagimsiz Baslangic", "color": "#00897b", "icon": "\U0001f4d8"},
        "10": {"name": "B1.2 \u2014 Bagimsiz Gelisim", "color": "#5c6bc0", "icon": "\U0001f4d7"},
        "11": {"name": "B1.3 \u2014 Bagimsiz Pekistirme", "color": "#8e24aa", "icon": "\U0001f4d9"},
        "12": {"name": "B1.4 \u2014 Bagimsiz Tamamlama", "color": "#c62828", "icon": "\U0001f4d5"},
    }
    words_data = _json.dumps(_GRADE_WORDS.get(grade, {}), ensure_ascii=False)
    grammar_data = _json.dumps(_GRADE_GRAMMAR.get(grade, []), ensure_ascii=False)
    info = _GRADE_INFO.get(grade, _GRADE_INFO["5"])
    info_json = _json.dumps(info, ensure_ascii=False)
    # Reuse the main KDG engine but with grade-specific data injected
    # This returns a simplified single-level version
    return _KDG_CSS + f"""
<div id="kdg"><div id="kdg-content"></div></div>
<script>
(function(){{
"use strict";
var USER="{username_grade}";var GRADE="{grade}";var SUBLEVEL="{sublevel}";
var INFO={info_json};var W={words_data};var G={grammar_data};
var ttsVoice=null;
function initTTS(){{if(!window.speechSynthesis)return;function pick(){{var v=speechSynthesis.getVoices();var p=['Google US English','Google UK English Female','Microsoft Zira','Samantha'];for(var i=0;i<p.length;i++)for(var j=0;j<v.length;j++)if(v[j].name.indexOf(p[i])!==-1&&v[j].lang.indexOf('en')===0){{ttsVoice=v[j];return;}}for(var j=0;j<v.length;j++)if(v[j].lang.indexOf('en')===0){{ttsVoice=v[j];return;}}}}if(speechSynthesis.getVoices().length)pick();speechSynthesis.onvoiceschanged=pick;}}
initTTS();
function speak(text){{if(!window.speechSynthesis)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=0.85;if(ttsVoice)u.voice=ttsVoice;speechSynthesis.speak(u);}}
function speakEN(t){{speak(t);}}
var S={{screen:'dashboard',cat:'',learnIdx:0,flipped:false,quiz:{{qs:[],cur:0,score:0,answered:false,selected:-1}},exam:{{qs:[],cur:0,score:0,answered:false,selected:-1,timer:null,timeLeft:900}}}};
var P=loadProgress();
function loadProgress(){{try{{var d=localStorage.getItem('kdg_'+USER);return d?JSON.parse(d):{{cats:{{}},grammarDone:false,examPassed:false,examScore:0}};}}catch(e){{return {{cats:{{}},grammarDone:false,examPassed:false,examScore:0}};}}}}
function saveProgress(){{try{{localStorage.setItem('kdg_'+USER,JSON.stringify(P));}}catch(e){{}}}}
function catsDone(){{var cats=Object.keys(W);var done=0;cats.forEach(function(c){{if(P.cats[c]&&P.cats[c].quizPassed)done++;}});return {{done:done,total:cats.length}};}}
function levelPct(){{var cd=catsDone();var steps=cd.total+1+1;var done=cd.done+(P.grammarDone?1:0)+(P.examPassed?1:0);return Math.round(done/steps*100);}}
function totalWords(){{var t=0;Object.keys(W).forEach(function(c){{t+=W[c].length;}});return t;}}
function learnedWords(){{var t=0;Object.keys(P.cats).forEach(function(c){{if(P.cats[c]&&P.cats[c].learned)t+=P.cats[c].learned.length;}});return t;}}
function shuffle(a){{for(var i=a.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}}return a;}}
function genCatQuiz(cat){{var words=W[cat];if(!words)return[];var pool=shuffle(words.slice());var qs=[];pool.slice(0,Math.min(10,pool.length)).forEach(function(w){{var opts=[w.e];var others=words.filter(function(x){{return x.e!==w.e;}});shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].e);shuffle(opts);qs.push({{stem:w.t,opts:opts,correct:opts.indexOf(w.e)}});}});return qs;}}
function genExam(){{var qs=[];var allW=[];Object.keys(W).forEach(function(c){{W[c].forEach(function(w){{allW.push(w);}});}});shuffle(allW);allW.slice(0,15).forEach(function(w){{var opts=[w.e];var others=allW.filter(function(x){{return x.e!==w.e;}});shuffle(others);for(var i=0;i<3;i++)opts.push(others[i].e);shuffle(opts);qs.push({{stem:w.t+' = ?',opts:opts,correct:opts.indexOf(w.e)}});}});shuffle(G.slice()).slice(0,5).forEach(function(g){{var correct=g.f;var opts=[correct,'Wrong: '+g.f.split('/').reverse().join('/').substring(0,40)];shuffle(opts);qs.push({{stem:g.n+': Dogru formul hangisi?',opts:opts,correct:opts.indexOf(correct)}});}});return shuffle(qs);}}
var $=document.getElementById('kdg-content');
function h(tag,cls,inner){{return '<'+tag+(cls?' class="'+cls+'"':'')+'>'+inner+'</'+tag+'>';}}
function render(){{switch(S.screen){{case'dashboard':renderDash();break;case'learn':renderLearn();break;case'quiz':renderQuiz();break;case'grammar':renderGrammar();break;case'exam':renderExam();break;case'examResult':renderExamResult();break;case'catResult':renderCatResult();break;}}}}
function renderDash(){{var tw=totalWords(),lw=learnedWords(),pct=levelPct(),cd=catsDone();var o='';o+=h('div','kdg-top',h('div','kdg-logo',INFO.icon+' <span>'+GRADE+'. Sinif Ingilizce</span> <small style="font-size:.5em;color:#8a6914;letter-spacing:2px">'+SUBLEVEL+' DIAMOND</small>')+h('div','kdg-stats','\\ud83d\\udcda <b>'+lw+'</b>/'+tw+' kelime | \\ud83c\\udfc6 <b>'+pct+'</b>% | \\ud83d\\udc64 <b>'+USER.split('_')[0]+'</b>'));var body='';body+='<div style="background:linear-gradient(135deg,'+INFO.color+'22,'+INFO.color+'11);border:1px solid '+INFO.color+'44;border-radius:12px;padding:16px 20px;margin-bottom:16px"><div style="font-size:1.1rem;font-weight:800;color:'+INFO.color+'">'+INFO.icon+' CEFR '+SUBLEVEL+' \\u2014 '+INFO.name+'</div><div style="font-size:.8rem;color:#999;margin-top:4px">Ilerleme: %'+pct+' | '+cd.done+'/'+cd.total+' kategori tamamlandi</div><div class="kdg-pbar" style="margin-top:8px"><div class="kdg-pfill" style="width:'+pct+'%;background:'+INFO.color+'"></div></div></div>';body+=h('div','kdg-sh',h('h3','','\\ud83d\\udcda Kelime Kategorileri ('+cd.done+'/'+cd.total+')'));body+='<div class="kdg-cats">';Object.keys(W).forEach(function(c){{var words=W[c];var cp=P.cats[c]||{{}};var done=cp.quizPassed;var learned=(cp.learned||[]).length;body+='<div class="kdg-cat'+(done?' done':'')+'" data-cat="'+c+'"><div class="cat-icon">'+c.split(' ').pop()+'</div><div class="cat-info"><div class="cat-name">'+c.split(' ')[0]+'</div><div class="cat-sub">'+learned+'/'+words.length+' ogrenildi</div></div><span class="cat-badge" style="background:'+(done?'rgba(76,175,80,.2);color:#81c784':'rgba(255,255,255,.1);color:#999')+'">'+(done?'\\u2705 Tamam':'\\u25b6 Basla')+'</span></div>';}});body+='</div>';var allCatsDone=cd.done>=cd.total;body+=h('div','kdg-sh',h('h3','','\\ud83d\\udcd6 Gramer Calismasi'));if(allCatsDone||P.grammarDone)body+='<button class="kdg-gram-btn'+(P.grammarDone?' done':'')+'" onclick="goGrammar()">'+(P.grammarDone?'\\u2705 Gramer Tamamlandi':'\\ud83d\\udcd6 Gramer Calis ('+G.length+' konu)')+'</button>';else body+='<button class="kdg-gram-btn locked" style="cursor:not-allowed;opacity:.5">\\ud83d\\udd12 Tum kategorileri tamamla ('+cd.done+'/'+cd.total+')</button>';var examReady=allCatsDone&&P.grammarDone;body+=h('div','kdg-sh',h('h3','','\\ud83c\\udfaf Seviye Sinavi'));if(P.examPassed)body+='<div class="kdg-exam-btn ready" onclick="goExam()" style="cursor:pointer">\\u2705 Sinav Gecildi ('+P.examScore+'/20) \\u2014 Tekrar Coz</div>';else if(examReady)body+='<div class="kdg-exam-btn ready" onclick="goExam()">\\ud83c\\udfaf Seviye Sinavina Gir (20 soru, %70 gecme)</div>';else body+='<div class="kdg-exam-btn locked">\\ud83d\\udd12 Gramer calismasini tamamla</div>';o+=h('div','kdg-body',body);$.innerHTML=o;document.querySelectorAll('.kdg-cat').forEach(function(el){{el.onclick=function(){{S.cat=this.dataset.cat;S.learnIdx=0;S.flipped=false;S.screen='learn';render();}};}});}}
function renderLearn(){{var cat=S.cat;var words=W[cat];if(!words||!words.length){{S.screen='dashboard';render();return;}}var idx=S.learnIdx;if(idx>=words.length)idx=words.length-1;var w=words[idx];var o='';o+=h('div','kdg-top','<button class="kdg-back" onclick="goDash()">\\u2190 '+cat.split(' ')[0]+'</button>'+h('div','kdg-logo','\\ud83d\\udcd6 Kelime Ogren')+h('div','kdg-stats',(idx+1)+'/'+words.length));var body='';body+=h('div','kdg-title',h('p','',cat+' \\u2014 '+SUBLEVEL));body+='<div class="kdg-pbar" style="margin-bottom:20px"><div class="kdg-pfill" style="width:'+((idx+1)/words.length*100)+'%;background:'+INFO.color+'"></div></div>';body+='<div class="kdg-flash">';if(!S.flipped)body+='<div class="kdg-fcard" onclick="flipCard()"><div class="fc-label">TURKCE</div><div class="fc-word">'+w.t+'</div><div class="fc-hint">Karti cevirmek icin tikla</div></div>';else{{body+='<div class="kdg-fcard" style="border-color:'+INFO.color+'"><div class="fc-label">ENGLISH</div><div class="fc-word" style="color:'+INFO.color+'">'+w.e+' <span class="kdg-speak" onclick="event.stopPropagation();speakEN(\\''+w.e.replace(/'/g,"\\\\'")+'\\')">\\ud83d\\udd0a</span></div><div class="fc-trans" style="margin-top:8px">'+w.t+'</div></div>';}}body+='</div>';body+='<div class="kdg-fctrls" style="margin-top:16px">';if(!S.flipped)body+='<button class="kdg-back btn-flip" onclick="flipCard()">\\ud83d\\udd04 Cevir</button>';else{{body+='<button class="kdg-back btn-again" onclick="learnNext(false)">\\ud83d\\udd04 Tekrar</button>';body+='<button class="kdg-back btn-know" onclick="learnNext(true)">\\u2705 Biliyorum</button>';}}body+='</div>';if(idx>=words.length-1&&S.flipped)body+='<div style="text-align:center;margin-top:20px"><button class="kdg-back btn-next" onclick="startCatQuiz()" style="padding:12px 32px;font-size:.95rem">\\ud83c\\udfaf Quiz\\'e Gec (10 soru)</button></div>';o+=h('div','kdg-body',body);$.innerHTML=o;if(S.flipped&&w)setTimeout(function(){{speakEN(w.e);}},250);}}
function renderQuiz(){{var q=S.quiz;if(!q.qs.length){{S.screen='dashboard';render();return;}}var cur=q.qs[q.cur];var o='';o+=h('div','kdg-top','<button class="kdg-back" onclick="goDash()">\\u2190 Vazgec</button>'+h('div','kdg-logo','\\ud83c\\udfaf Kelime Quiz')+h('div','kdg-stats','Soru: <b>'+(q.cur+1)+'</b>/'+q.qs.length+' | Dogru: <b>'+q.score+'</b>'));var body='';body+='<div class="kdg-pbar" style="margin-bottom:20px"><div class="kdg-pfill" style="width:'+((q.cur+1)/q.qs.length*100)+'%;background:'+INFO.color+'"></div></div>';body+='<div class="kdg-quiz"><div class="kdg-qcard"><div class="q-num">Soru '+(q.cur+1)+'/'+q.qs.length+'</div><div class="q-stem">'+cur.stem+' kelimesinin Ingilizcesi nedir?</div><div class="kdg-opts">';cur.opts.forEach(function(opt,i){{var cls='kdg-opt';if(q.answered){{cls+=' disabled';if(i===cur.correct)cls+=' correct';else if(i===q.selected)cls+=' wrong';}}body+='<div class="'+cls+'" data-idx="'+i+'" onclick="quizAnswer('+i+')">'+String.fromCharCode(65+i)+') '+opt+'</div>';}});body+='</div></div>';if(q.answered){{body+='<div style="text-align:center;margin-top:12px">';if(q.cur<q.qs.length-1)body+='<button class="kdg-back btn-next" onclick="quizNext()">Sonraki \\u2192</button>';else body+='<button class="kdg-back btn-next" onclick="finishCatQuiz()">Sonuclari Gor</button>';body+='</div>';}}body+='</div>';o+=h('div','kdg-body',body);$.innerHTML=o;}}
function renderCatResult(){{var q=S.quiz;var passed=q.score>=7;if(passed){{if(!P.cats[S.cat])P.cats[S.cat]={{learned:[],quizPassed:false}};P.cats[S.cat].quizPassed=true;saveProgress();}}var o='';o+=h('div','kdg-top',h('div','kdg-logo','\\ud83d\\udcca Quiz Sonucu'));var body='<div class="kdg-result"><div class="res-icon">'+(passed?'\\ud83c\\udf89':'\\ud83d\\ude14')+'</div><div class="res-title" style="color:'+(passed?'#81c784':'#e57373')+'">'+(passed?'TEBRIKLER!':'Tekrar Dene')+'</div><div class="res-score" style="color:'+INFO.color+'">'+q.score+'/'+q.qs.length+'</div><div class="res-msg">'+(passed?'Kategoriyi basariyla tamamladin!':'Gecmek icin 7/10 dogru gerekli.')+'</div><button class="res-btn" onclick="goDash()">\\u2190 Ana Sayfa</button></div>';o+=h('div','kdg-body',body);$.innerHTML=o;}}
function renderGrammar(){{var o='';o+=h('div','kdg-top','<button class="kdg-back" onclick="goDash()">\\u2190 Geri</button>'+h('div','kdg-logo','\\ud83d\\udcd6 '+SUBLEVEL+' Gramer')+h('div','kdg-stats',G.length+' konu'));var body='<div class="kdg-gram">';G.forEach(function(g,i){{body+='<div class="kdg-gcard">';body+=h('h3','','\\ud83d\\udccc '+(i+1)+'. '+g.n);body+='<div class="g-formula">'+g.f+'</div><div class="g-exp">'+g.e+'</div><div class="g-ex">'+g.x+' <span class="kdg-speak-sm" onclick="speakEN(\\''+g.x.replace(/<[^>]*>/g,'').replace(/'/g,"\\\\'")+'\\')">\\ud83d\\udd0a</span></div></div>';}});body+='<div style="text-align:center;margin-top:16px"><button class="kdg-back btn-next" onclick="finishGrammar()" style="padding:12px 32px">'+(P.grammarDone?'\\u2705 Tamamlandi':'\\u2705 Grameri Tamamla')+'</button></div></div>';o+=h('div','kdg-body',body);$.innerHTML=o;}}
function renderExam(){{var q=S.exam;if(!q.qs.length){{S.screen='dashboard';render();return;}}var cur=q.qs[q.cur];var o='';o+=h('div','kdg-top','<button class="kdg-back" onclick="abandonExam()">\\u2190 Vazgec</button>'+h('div','kdg-logo','\\ud83c\\udfaf '+SUBLEVEL+' Sinavi')+h('div','kdg-stats',''));var body='';var mins=Math.floor(q.timeLeft/60),secs=q.timeLeft%60;body+='<div class="kdg-exam-bar"><div class="eb-time">\\u23f1 '+mins+':'+(secs<10?'0':'')+secs+'</div><div class="eb-prog">Soru '+(q.cur+1)+'/'+q.qs.length+' | Dogru: '+q.score+'</div></div>';body+='<div class="kdg-pbar" style="margin-bottom:16px"><div class="kdg-pfill" style="width:'+((q.cur+1)/q.qs.length*100)+'%;background:'+INFO.color+'"></div></div>';body+='<div class="kdg-quiz"><div class="kdg-qcard"><div class="q-num">Soru '+(q.cur+1)+'/'+q.qs.length+'</div><div class="q-stem">'+cur.stem+'</div><div class="kdg-opts">';cur.opts.forEach(function(opt,i){{var cls='kdg-opt';if(q.answered){{cls+=' disabled';if(i===cur.correct)cls+=' correct';else if(i===q.selected)cls+=' wrong';}}body+='<div class="'+cls+'" onclick="examAnswer('+i+')">'+String.fromCharCode(65+i)+') '+opt+'</div>';}});body+='</div></div>';if(q.answered){{body+='<div style="text-align:center;margin-top:12px">';if(q.cur<q.qs.length-1)body+='<button class="kdg-back btn-next" onclick="examNext()">Sonraki \\u2192</button>';else body+='<button class="kdg-back btn-next" onclick="finishExam()">Sinavi Bitir</button>';body+='</div>';}}body+='</div>';o+=h('div','kdg-body',body);$.innerHTML=o;}}
function renderExamResult(){{var q=S.exam;var total=q.qs.length;var passed=q.score>=Math.ceil(total*0.7);if(passed){{P.examPassed=true;P.examScore=q.score;saveProgress();}}var o='';o+=h('div','kdg-top',h('div','kdg-logo','\\ud83d\\udcca Sinav Sonucu'));var body='<div class="kdg-result"><div class="res-icon">'+(passed?'\\ud83c\\udfc6':'\\ud83d\\udcdd')+'</div><div class="res-title" style="color:'+(passed?'#e8d48b':'#e57373')+'">'+(passed?SUBLEVEL+' SEVIYE GECILDI!':'Tekrar Dene')+'</div><div class="res-score" style="color:'+INFO.color+'">'+q.score+'/'+total+'</div><div class="res-msg">'+(passed?'Tebrikler! '+SUBLEVEL+' seviyesini basariyla tamamladin!':'Gecmek icin %70 dogru gerekli ('+Math.ceil(total*0.7)+'/'+total+')')+'</div><button class="res-btn" onclick="goDash()">\\u2190 Ana Sayfaya Don</button></div>';o+=h('div','kdg-body',body);$.innerHTML=o;}}
window.goDash=function(){{S.screen='dashboard';render();}};
window.goGrammar=function(){{S.screen='grammar';render();}};
window.flipCard=function(){{S.flipped=!S.flipped;render();}};
window.learnNext=function(known){{var cat=S.cat;if(!P.cats[cat])P.cats[cat]={{learned:[],quizPassed:false,retry:[]}};if(known&&P.cats[cat].learned.indexOf(S.learnIdx)===-1){{P.cats[cat].learned.push(S.learnIdx);saveProgress();}}else if(!known){{if(!P.cats[cat].retry)P.cats[cat].retry=[];if(P.cats[cat].retry.indexOf(S.learnIdx)===-1)P.cats[cat].retry.push(S.learnIdx);saveProgress();}}S.learnIdx++;S.flipped=false;var words=W[cat];if(S.learnIdx>=words.length){{var retryList=P.cats[cat].retry||[];if(retryList.length>0){{S.learnIdx=retryList.shift();P.cats[cat].retry=retryList;saveProgress();}}else{{S.learnIdx=words.length-1;S.flipped=true;}}}}render();}};
window.startCatQuiz=function(){{S.quiz={{qs:genCatQuiz(S.cat),cur:0,score:0,answered:false,selected:-1}};S.screen='quiz';render();}};
window.quizAnswer=function(idx){{if(S.quiz.answered)return;S.quiz.answered=true;S.quiz.selected=idx;if(idx===S.quiz.qs[S.quiz.cur].correct)S.quiz.score++;render();}};
window.quizNext=function(){{S.quiz.cur++;S.quiz.answered=false;S.quiz.selected=-1;render();}};
window.finishCatQuiz=function(){{S.screen='catResult';render();}};
window.goExam=function(){{var qs=genExam();S.exam={{qs:qs,cur:0,score:0,answered:false,selected:-1,timeLeft:900}};if(S.exam.timer)clearInterval(S.exam.timer);S.exam.timer=setInterval(function(){{S.exam.timeLeft--;if(S.exam.timeLeft<=0){{clearInterval(S.exam.timer);window.finishExam();}}else if(S.screen==='exam'){{var te=document.querySelector('.eb-time');if(te){{var m=Math.floor(S.exam.timeLeft/60);var s=S.exam.timeLeft%60;te.textContent='\\u23f1 '+m+':'+(s<10?'0':'')+s;}}}}}},1000);S.screen='exam';render();}};
window.examAnswer=function(idx){{if(S.exam.answered)return;S.exam.answered=true;S.exam.selected=idx;if(idx===S.exam.qs[S.exam.cur].correct)S.exam.score++;render();}};
window.examNext=function(){{S.exam.cur++;S.exam.answered=false;S.exam.selected=-1;render();}};
window.finishExam=function(){{if(S.exam.timer){{clearInterval(S.exam.timer);S.exam.timer=null;}}S.screen='examResult';render();}};
window.abandonExam=function(){{if(S.exam.timer){{clearInterval(S.exam.timer);S.exam.timer=null;}}S.screen='dashboard';render();}};
window.finishGrammar=function(){{P.grammarDone=true;saveProgress();S.screen='dashboard';render();}};
render();
}})();
</script>
"""


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
A1:{{n:'Beginner',t:'Baslangic',c:'#10b981',i:'\\ud83c\\udf31',r:0}},
A2:{{n:'Elementary',t:'Temel',c:'#06b6d4',i:'\\ud83d\\ude80',r:1}},
B1:{{n:'Intermediate',t:'Orta',c:'#3b82f6',i:'\\ud83d\\udcaa',r:2}},
B2:{{n:'Upper-Intermediate',t:'Ust Orta',c:'#8b5cf6',i:'\\ud83d\\udd25',r:3}},
C1:{{n:'Advanced',t:'Ileri',c:'#ec4899',i:'\\u2b50',r:4}},
C2:{{n:'Mastery',t:'Ustalik',c:'#f59e0b',i:'\\ud83d\\udc51',r:5}}
}};

// ===================== READING TEXTS =====================
var READINGS={{
A1:[
{{title:"My Day",text:"I wake up at seven. I eat breakfast. I go to school by bus. I have lunch at twelve. I play with my friends after school. I do my homework in the evening. I go to bed at nine.",tr:"Yedide uyaniyorum. Kahvalti ediyorum. Otobusle okula gidiyorum. On ikide ogle yemegi yiyorum. Okuldan sonra arkadaslarimla oynuyorum. Aksam odevimi yapiyorum. Dokuzda yatiyorum.",qs:[{{q:"What time does the person wake up?",opts:["Six","Seven","Eight","Nine"],a:1}},{{q:"How does the person go to school?",opts:["By car","By train","By bus","On foot"],a:2}},{{q:"What does the person do after school?",opts:["Sleeps","Plays with friends","Watches TV","Reads"],a:1}}]}},
{{title:"My Family",text:"My name is Ali. I have a big family. My father is a teacher. My mother is a doctor. I have one sister and one brother. My sister is ten years old. My brother is five. We have a cat named Mimi. We live in a house with a garden.",tr:"Benim adim Ali. Buyuk bir ailem var. Babam ogretmen. Annem doktor. Bir kiz kardesim ve bir erkek kardesim var. Kiz kardesim on yasinda. Erkek kardesim bes yasinda. Mimi adinda bir kedimiz var. Bahceli bir evde yasiyoruz.",qs:[{{q:"What is the father's job?",opts:["Doctor","Teacher","Engineer","Driver"],a:1}},{{q:"How old is the brother?",opts:["Three","Five","Seven","Ten"],a:1}},{{q:"What is the cat's name?",opts:["Ali","Mimi","Kitty","Tom"],a:1}}]}},
{{title:"My School",text:"I go to a big school. There are many classrooms. My classroom is on the second floor. I sit next to my friend Ayse. My favourite subject is English. I also like Art. We have a big playground. I play football there every day.",tr:"Buyuk bir okula gidiyorum. Bircok sinif var. Sinifim ikinci katta. Arkadasim Ayse'nin yaninda oturuyorum. En sevdigim ders Ingilizce. Resim dersini de seviyorum. Buyuk bir oyun alanima var. Her gun orada futbol oynuyorum.",qs:[{{q:"Where is the classroom?",opts:["First floor","Second floor","Third floor","Ground floor"],a:1}},{{q:"What is the favourite subject?",opts:["Math","Science","English","Music"],a:2}},{{q:"What sport does the person play?",opts:["Basketball","Tennis","Football","Volleyball"],a:2}}]}},
{{title:"My Pet",text:"I have a dog. His name is Buddy. He is brown and white. He is two years old. He likes to play in the garden. He eats meat and biscuits. I walk him every morning. He sleeps on my bed at night. I love my dog very much.",tr:"Bir kopegim var. Adi Buddy. Kahverengi ve beyaz. Iki yasinda. Bahcede oynamayi seviyor. Et ve biskuvi yiyor. Her sabah onu gezdiriyorum. Gece yatakimda uyuyor. Kopegimi cok seviyorum.",qs:[{{q:"What colour is the dog?",opts:["Black","Brown and white","Grey","Yellow"],a:1}},{{q:"How old is Buddy?",opts:["One","Two","Three","Five"],a:1}},{{q:"When does the person walk the dog?",opts:["Evening","Afternoon","Morning","Night"],a:2}}]}},
{{title:"At the Restaurant",text:"Today we go to a restaurant. I sit at a table near the window. The waiter brings the menu. I order pizza and orange juice. My mother orders salad and water. My father orders chicken and coffee. The food is very delicious. We pay the bill and go home.",tr:"Bugun bir restorana gidiyoruz. Pencerenin yaninda bir masaya oturuyorum. Garson menuyu getiriyor. Pizza ve portakal suyu siparis ediyorum. Annem salata ve su siparis ediyor. Babam tavuk ve kahve siparis ediyor. Yemek cok lezzetli. Hesabi oduyoruz ve eve gidiyoruz.",qs:[{{q:"Where does the person sit?",opts:["Near the door","Near the window","In the garden","At the bar"],a:1}},{{q:"What does the person order to drink?",opts:["Water","Coffee","Orange juice","Tea"],a:2}},{{q:"What does the father order?",opts:["Pizza","Salad","Chicken","Fish"],a:2}}]}},
{{title:"The Weather",text:"Today the weather is sunny. It is very hot. I wear a T-shirt and shorts. I drink cold water. In winter, it is cold and it snows. I wear a coat and gloves. In spring, it rains sometimes. I take my umbrella to school. I like summer the best.",tr:"Bugun hava gunesli. Cok sicak. Tisort ve sort giyiyorum. Soguk su iciyorum. Kista hava soguk ve kar yagiyor. Mont ve eldiven giyiyorum. Ilkbaharda bazen yagmur yagiyor. Semsiyemi okula gotururum. Yazi en cok seviyorum.",qs:[{{q:"What is today's weather?",opts:["Rainy","Cloudy","Sunny","Snowy"],a:2}},{{q:"What does the person wear in winter?",opts:["T-shirt","Coat and gloves","Shorts","Sandals"],a:1}},{{q:"Which season does the person like best?",opts:["Spring","Winter","Autumn","Summer"],a:3}}]}},
{{title:"Shopping Day",text:"I go to the shop with my sister. We need milk, eggs, and bread. The shop is near our house. I carry the basket. My sister chooses the fruit. She likes apples and bananas. We pay at the counter. The total is ten lira. We walk home together. Shopping is fun with my sister.",tr:"Kiz kardesimle markete gidiyorum. Sut, yumurta ve ekmege ihtiyacimiz var. Market evimizin yakininda. Sepeti ben tasiyorum. Kiz kardesim meyveleri seciyor. Elma ve muzu seviyor. Kasada odeme yapiyoruz. Toplam on lira. Birlikte eve yuruyoruz. Kiz kardesimle alisveris yapmak eglenceli.",qs:[{{q:"What do they need from the shop?",opts:["Meat and fish","Milk, eggs, and bread","Toys and games","Clothes"],a:1}},{{q:"Who chooses the fruit?",opts:["The mother","The father","The sister","The person"],a:2}},{{q:"How much do they pay?",opts:["Five lira","Ten lira","Fifteen lira","Twenty lira"],a:1}}]}},
{{title:"My Classroom",text:"My classroom is big and bright. There are twenty desks. The walls are white. There is a big board at the front. My teacher writes on the board every day. There are pictures on the walls. We have a bookshelf with many books. I sit in the third row. My friend Mehmet sits behind me. I like my classroom very much.",tr:"Sinifim buyuk ve aydinlik. Yirmi sira var. Duvarlar beyaz. Onde buyuk bir tahta var. Ogretmenim her gun tahtaya yaziyor. Duvarlarda resimler var. Bircok kitabi olan bir kitapligimiz var. Ucuncu sirada oturuyorum. Arkadasim Mehmet arkamda oturuyor. Sinifimi cok seviyorum.",qs:[{{q:"How many desks are there?",opts:["Ten","Fifteen","Twenty","Thirty"],a:2}},{{q:"Where does the person sit?",opts:["First row","Second row","Third row","Last row"],a:2}},{{q:"What colour are the walls?",opts:["Blue","Yellow","Green","White"],a:3}}]}},
{{title:"A Picnic in the Park",text:"On Sunday, we go to the park. My mother makes sandwiches. My father brings juice and water. I play on the swings. My little brother runs on the grass. We sit under a big tree and eat. The sandwiches are very tasty. After lunch, we fly a kite. The park is very green and beautiful. I love picnics.",tr:"Pazar gunu parka gidiyoruz. Annem sandvic yapiyor. Babam meyve suyu ve su getiriyor. Salincakta oynuyorum. Kucuk kardesim cimlerde kosuyor. Buyuk bir agacin altinda oturup yiyoruz. Sandvicler cok lezzetli. Ogle yemeginden sonra ucurtma ucuruyoruz. Park cok yesil ve guzel. Piknikleri seviyorum.",qs:[{{q:"What day do they go to the park?",opts:["Saturday","Sunday","Monday","Friday"],a:1}},{{q:"What does the mother make?",opts:["Pizza","Cake","Sandwiches","Soup"],a:2}},{{q:"What do they do after lunch?",opts:["Sleep","Swim","Fly a kite","Go home"],a:2}}]}},
{{title:"My Favourite Sport",text:"I like football very much. I play football every afternoon. My team has eight players. I am the goalkeeper. My friend Emre is very fast. He scores many goals. We play in the school garden. Our coach is Mr Kemal. He teaches us new tricks. We have a match every Saturday. Last week we won three to one. I want to be a footballer.",tr:"Futbolu cok seviyorum. Her ogle sonrasi futbol oynuyorum. Takimimda sekiz oyuncu var. Ben kaleciyim. Arkadasim Emre cok hizli. Cok gol atiyor. Okul bahcesinde oynuyoruz. Kocumuz Kemal Bey. Bize yeni numaralar ogretiyor. Her cumartesi macimiz var. Gecen hafta uc bir kazandik. Futbolcu olmak istiyorum.",qs:[{{q:"What position does the person play?",opts:["Striker","Midfielder","Goalkeeper","Defender"],a:2}},{{q:"When do they have matches?",opts:["Sunday","Monday","Friday","Saturday"],a:3}},{{q:"What was the score last week?",opts:["Two to one","Three to one","Three to two","One to zero"],a:1}}]}}
],
A2:[
{{title:"A Trip to the Market",text:"Last Saturday, I went to the market with my mother. We bought fresh vegetables and fruits. The tomatoes were very red and cheap. My mother also bought some fish for dinner. I helped her carry the bags. On the way home, we stopped at a bakery and bought some bread. It was a nice morning.",tr:"Gecen cumartesi annemle pazara gittim. Taze sebze ve meyveler aldik. Domatesler cok kirmizi ve ucuzdu. Annem aksam yemegi icin balik da aldi. Cantalari tasimada ona yardim ettim. Eve donerken bir firina durarak ekmek aldik. Guzel bir sabahti.",qs:[{{q:"When did they go to the market?",opts:["Last Sunday","Last Saturday","Last Friday","Yesterday"],a:1}},{{q:"What did the mother buy for dinner?",opts:["Chicken","Meat","Fish","Pasta"],a:2}},{{q:"Where did they stop on the way home?",opts:["A cafe","A bakery","A shop","A park"],a:1}}]}},
{{title:"My Best Friend",text:"My best friend is Elif. We have been friends since primary school. She is tall with brown hair. She likes reading books and playing volleyball. Every weekend, we meet at the park or go to the cinema. She wants to be a doctor in the future. I think she will be a great one because she is very kind and hardworking.",tr:"En iyi arkadasim Elif. Ilkokuldan beri arkadasiz. Uzun boylu ve kahverengi sacli. Kitap okumak ve voleybol oynamak seviyor. Her hafta sonu parkta bulusuyoruz ya da sinemaya gidiyoruz. Gelecekte doktor olmak istiyor. Bence harika bir doktor olacak cunku cok nazik ve caliskan.",qs:[{{q:"What sport does Elif like?",opts:["Basketball","Football","Volleyball","Tennis"],a:2}},{{q:"What does Elif want to be?",opts:["Teacher","Doctor","Lawyer","Engineer"],a:1}},{{q:"How is Elif described?",opts:["Lazy","Kind and hardworking","Funny","Quiet"],a:1}}]}},
{{title:"A Birthday Party",text:"Yesterday was my birthday. I turned thirteen. My parents organized a surprise party for me. All my friends came to our house. We had a big chocolate cake with candles. I blew out the candles and made a wish. We played music and danced. My friends gave me wonderful presents. It was the best birthday ever!",tr:"Dun dogum gunumdu. On uc yasima girdim. Ailem benim icin surpriz bir parti duzenledi. Tum arkadaslarim evimize geldi. Mumlu buyuk bir cikolatali pastamiz vardi. Mumlari ufledim ve dilek tuttum. Muzik acip dans ettik. Arkadaslarim harika hediyeler verdi. Simdiye kadarki en guzel dogum gunuydu!",qs:[{{q:"How old did the person turn?",opts:["Twelve","Thirteen","Fourteen","Fifteen"],a:1}},{{q:"What kind of cake was it?",opts:["Vanilla","Strawberry","Chocolate","Lemon"],a:2}},{{q:"Who organized the party?",opts:["Friends","Teachers","Parents","Neighbours"],a:2}}]}},
{{title:"Lost in the City",text:"Last week, I visited Istanbul for the first time. I took the metro to Taksim Square. I wanted to see the famous Istiklal Street. But I took the wrong exit and got lost. I asked a shopkeeper for directions. He was very helpful and showed me the way on a map. I finally found Istiklal Street and enjoyed walking there. I bought some souvenirs for my family.",tr:"Gecen hafta ilk kez Istanbul'u ziyaret ettim. Metroyla Taksim Meydani'na gittim. Unlu Istiklal Caddesi'ni gormek istedim. Ama yanlis cikistan ciktim ve kayboldum. Bir dukkanciya yol sordum. Cok yardimci oldu ve haritada yolu gosterdi. Sonunda Istiklal Caddesi'ni buldum ve orada yurumekten keyif aldim. Ailem icin hediyelik esyalar aldim.",qs:[{{q:"Where did the person visit?",opts:["Ankara","Izmir","Istanbul","Antalya"],a:2}},{{q:"How did the person get to Taksim?",opts:["By bus","By taxi","By metro","On foot"],a:2}},{{q:"Who helped with directions?",opts:["A tourist","A policeman","A shopkeeper","A student"],a:2}}]}},
{{title:"My Hobby: Photography",text:"I started taking photos two years ago. My uncle gave me his old camera. At first, my photos were not very good. But I practised every day. I took photos of flowers, animals, and buildings. Now I am much better. Last month, I won second place in a school photography competition. My teacher was very proud of me. I want to become a professional photographer one day.",tr:"Iki yil once fotograf cekmeye basladim. Amcam eski kamerasini bana verdi. Baslangicta fotograflarim cok iyi degildi. Ama her gun pratik yaptim. Ciceklerin, hayvanlarin ve binalarin fotograflarini cektim. Simdi cok daha iyiyim. Gecen ay okul fotograf yarismasinda ikinci oldum. Ogretmenim benimle cok gurur duydu. Bir gun profesyonel fotograf olmak istiyorum.",qs:[{{q:"Who gave the camera?",opts:["Father","Teacher","Uncle","Friend"],a:2}},{{q:"What place did the person win?",opts:["First","Second","Third","Fourth"],a:1}},{{q:"How long has the person been taking photos?",opts:["One year","Two years","Three years","Six months"],a:1}}]}},
{{title:"A Rainy Day",text:"It was raining heavily this morning. I forgot my umbrella at home. When I arrived at school, I was completely wet. My teacher gave me a towel. During the break, we could not play outside. We played board games in the classroom instead. After school, the rain stopped and a beautiful rainbow appeared in the sky. My mother picked me up by car. It turned out to be a good day after all.",tr:"Bu sabah siddetli yagmur yagiyordu. Semsiyemi evde unuttum. Okula vardigimda tamamen islaktim. Ogretmenim bana bir havlu verdi. Teneffuste disarida oynayamadik. Onun yerine sinifta masa oyunlari oynadik. Okuldan sonra yagmur durdu ve gokyuzunde guzel bir gokkusagi belirdi. Annem beni arabayla aldi. Sonucta guzel bir gun oldu.",qs:[{{q:"Why was the person wet?",opts:["Fell in water","Forgot umbrella","No coat","Played in rain"],a:1}},{{q:"What appeared after the rain?",opts:["Sun","Stars","Rainbow","Snow"],a:2}},{{q:"What did they play during break?",opts:["Football","Board games","Video games","Cards"],a:1}}]}},
{{title:"My Neighbourhood",text:"I live in a quiet neighbourhood near the city centre. There is a small park across the street where children play every evening. Next to the park, there is a grocery shop and a pharmacy. Our neighbours are very friendly. Mrs Ayse, who lives next door, often brings us homemade cakes. On weekends, the neighbourhood becomes lively because there is a farmers market. I enjoy living here because everything I need is within walking distance.",tr:"Sehir merkezine yakin sakin bir mahallede yasiyorum. Sokaginkarsiinda her aksam cocuklarin oynadigi kucuk bir park var. Parkin yaninda bir bakkal ve bir eczane var. Komsularimiz cok dost canlis. Yan komsum Ayse Hanim bize sikca ev yapimi kek getirir. Hafta sonlari mahalle canlanir cunku pazar kurulur. Burada yasamayi seviyorum cunku ihtiyacim olan her sey yurume mesafesinde.",qs:[{{q:"Where is the neighbourhood?",opts:["In the countryside","Near the city centre","By the sea","On a mountain"],a:1}},{{q:"What does Mrs Ayse bring?",opts:["Flowers","Books","Homemade cakes","Vegetables"],a:2}},{{q:"What happens on weekends?",opts:["A concert","A farmers market","A football match","A parade"],a:1}}]}},
{{title:"Cooking with Grandma",text:"Every Sunday, I visit my grandmother. She teaches me how to cook traditional dishes. Last week, we made lentil soup together. First, we washed the lentils and chopped the onions. Then we put everything in a big pot with water. While the soup was cooking, my grandmother told me stories about her childhood. The soup was ready in forty minutes. We ate it with fresh bread. It was the best soup I have ever tasted. I want to learn all her recipes.",tr:"Her pazar babaannemi ziyaret ediyorum. Bana geleneksel yemekler yapmayi ogretiyor. Gecen hafta birlikte mercimek corbasi yaptik. Oncelikle mercimekleri yikadik ve soganlari dogradik. Sonra her seyi buyuk bir tencereye su ile koyduk. Corba pisarken babaannem bana cocuklugunden hikayeler anlatti. Corba kirk dakikada hazir oldu. Taze ekmekle yedik. Simdiye kadar tattigi en iyi corba. Tum tariflerini ogrenmek istiyorum.",qs:[{{q:"When does the person visit grandmother?",opts:["Saturday","Sunday","Monday","Friday"],a:1}},{{q:"What did they cook?",opts:["Chicken","Pasta","Lentil soup","Rice"],a:2}},{{q:"How long did the soup take?",opts:["Twenty minutes","Thirty minutes","Forty minutes","One hour"],a:2}}]}},
{{title:"The School Trip",text:"Our class went on a trip to the science museum last Thursday. We took the school bus early in the morning. The museum was in the next town, about one hour away. Inside, there were many interesting exhibits about space, dinosaurs, and the human body. My favourite part was the planetarium show. We saw the planets and stars on a big dome screen. After the show, we had lunch in the museum garden. Our teacher took a group photo before we left. Everyone agreed it was the best school trip of the year.",tr:"Sinifimiz gecen persembe bilim muzesine geziye gitti. Sabah erken okul servisine bindik. Muze bir sonraki kasabadaydı, yaklasik bir saat uzakta. Icinde uzay, dinozorlar ve insan vucut hakkinda bircok ilginc sergi vardi. En sevdigim kisim planetaryum gosterisiydi. Buyuk bir kubbe ekraninda gezegenleri ve yildizlari gorduk. Gosteriden sonra muze bahcesinde ogle yemegi yedik. Ogretmenimiz ayrilmadan once grup fotografi cekti. Herkes yilin en iyi okul gezisi oldugu konusunda hemsfikirdi.",qs:[{{q:"Where did they go?",opts:["A zoo","A science museum","A factory","An amusement park"],a:1}},{{q:"What was the favourite part?",opts:["Dinosaur exhibit","Space exhibit","Planetarium show","Lunch"],a:2}},{{q:"How did they travel?",opts:["By train","By car","By school bus","On foot"],a:2}}]}},
{{title:"A Letter to My Pen Pal",text:"I have a pen pal from England. Her name is Lucy. We write to each other every month. In her last letter, she told me about her school and her pet rabbit. She also sent me a photo of her town. It looks very green and rainy. I wrote back and told her about my city and my favourite places. I sent her a postcard of the seaside. We plan to video call next week. I am very excited because it will be the first time we see each other. Having a pen pal is a wonderful way to learn about other countries.",tr:"Ingiltere'den bir mektup arkadasim var. Adi Lucy. Her ay birbirimize yaziyoruz. Son mektubunda bana okulunu ve evcil tavsanini anlatti. Kasabasinin bir fotografini da gonderdi. Cok yesil ve yagmurlu gorunuyor. Ben de sehrimi ve en sevdigim yerleri anlattim. Ona sahil kenarinin bir kartpostalini gonderdim. Gelecek hafta goruntulu arama yapmayi planliyoruz. Cok heyecanliyim cunku ilk kez birbirimizi gorecegiz. Mektup arkadasi edinmek baska ulkeleri ogrenmenin harika bir yolu.",qs:[{{q:"Where is the pen pal from?",opts:["France","Germany","England","Spain"],a:2}},{{q:"How often do they write?",opts:["Every week","Every month","Every year","Every day"],a:1}},{{q:"What are they planning to do?",opts:["Meet in person","Video call","Send a gift","Write a book"],a:1}}]}}
],
B1:[
{{title:"The Digital Age",text:"Technology has changed the way we live, work, and communicate. Smartphones have become an essential part of daily life. Social media platforms connect millions of people worldwide. However, there are concerns about privacy and the impact of screen time on mental health. Many experts recommend limiting social media use and taking regular breaks from screens. Finding a balance between technology and real-life interactions is becoming increasingly important in modern society.",tr:"Teknoloji yasam, calisma ve iletisim seklirimizi degistirdi. Akilli telefonlar gunluk yasamin vazgecilmez bir parcasi oldu. Sosyal medya platformlari dunya capinda milyonlarca insani birbirine bagliyor. Ancak gizlilik ve ekran suresinin ruh sagligi uzerindeki etkisi konusunda endiseler var.",qs:[{{q:"What has become an essential part of daily life?",opts:["Computers","Smartphones","Television","Radio"],a:1}},{{q:"What are experts concerned about?",opts:["Cost of phones","Privacy and mental health","Internet speed","Battery life"],a:1}},{{q:"What do experts recommend?",opts:["Using more social media","Buying new phones","Limiting screen time","Avoiding technology completely"],a:2}}]}},
{{title:"Climate Change",text:"Climate change is one of the biggest challenges facing humanity today. Rising temperatures are causing glaciers to melt, sea levels to rise, and extreme weather events to become more frequent. Scientists warn that we must reduce carbon emissions significantly to prevent catastrophic consequences. Renewable energy sources like solar and wind power offer promising alternatives to fossil fuels. Individual actions, such as recycling and reducing energy consumption, also contribute to the fight against climate change.",tr:"Iklim degisikligi gunumuzde insanligin karsilastigi en buyuk sorunlardan biri. Artan sicakliklar buzullarin erimesine, deniz seviyelerinin yukselmesine ve asiri hava olaylarinin artmasina neden oluyor.",qs:[{{q:"What is causing glaciers to melt?",opts:["Pollution","Rising temperatures","Earthquakes","Wind"],a:1}},{{q:"What do renewable energy sources include?",opts:["Coal and gas","Solar and wind","Nuclear only","Oil"],a:1}},{{q:"What individual action is mentioned?",opts:["Driving more","Recycling","Flying less","Eating less"],a:1}}]}},
{{title:"The History of Coffee",text:"Coffee is one of the most popular drinks in the world. It was first discovered in Ethiopia by a goat herder named Kaldi. He noticed that his goats became very energetic after eating certain berries. The drink spread from Ethiopia to the Arab world in the 15th century. Coffee houses became important social gathering places. Today, billions of cups of coffee are consumed every day. Turkey has a rich coffee culture, and Turkish coffee is famous worldwide.",tr:"Kahve dunyanin en populer iceceklerinden biridir. Ilk olarak Etiyopya'da Kaldi adinda bir keci cobani tarafindan kesfedildi. Kecilerinin belirli meyveleri yedikten sonra cok enerjik oldugunu fark etti. Icecek 15. yuzyilda Etiyopya'dan Arap dunyasina yayildi.",qs:[{{q:"Where was coffee first discovered?",opts:["Brazil","Turkey","Ethiopia","Colombia"],a:2}},{{q:"Who discovered coffee?",opts:["A farmer","A goat herder","A scientist","A king"],a:1}},{{q:"When did coffee spread to the Arab world?",opts:["13th century","14th century","15th century","16th century"],a:2}}]}},
{{title:"Remote Work",text:"Since the pandemic, remote work has become increasingly common. Many employees now work from home at least a few days a week. Companies have invested in digital tools for video conferencing and project management. While remote work offers flexibility and eliminates commuting, it also presents challenges such as isolation and difficulty separating work from personal life. Some companies have adopted a hybrid model, combining office and remote work to get the best of both worlds.",tr:"Pandemiden bu yana uzaktan calisma giderek yayginlasti. Bircok calisan artik haftada en az birkac gun evden calisiyor. Sirketler video konferans ve proje yonetimi icin dijital araclara yatirim yapti.",qs:[{{q:"What has become common since the pandemic?",opts:["Travel","Remote work","Night shifts","Early retirement"],a:1}},{{q:"What is a challenge of remote work?",opts:["High salary","Isolation","Too much travel","Office noise"],a:1}},{{q:"What is a hybrid model?",opts:["Only office","Only remote","Mix of office and remote","Freelancing"],a:2}}]}},
{{title:"Healthy Eating",text:"A balanced diet is essential for good health. Nutritionists recommend eating plenty of fruits, vegetables, and whole grains. Protein from fish, lean meat, and legumes helps build and repair muscles. Drinking enough water throughout the day is equally important. Processed foods high in sugar and salt should be limited. Regular meals at consistent times help maintain energy levels. Making small changes to your diet can lead to significant improvements in your overall well-being.",tr:"Dengeli beslenme iyi saglik icin gereklidir. Beslenme uzmanlari bol meyve, sebze ve tam tahil tuketmeyi oneriyor. Balik, yagsiz et ve baklagillerden alinan protein kaslarin onarimina yardimci olur.",qs:[{{q:"What do nutritionists recommend eating?",opts:["Fast food","Fruits and vegetables","Only meat","Sweets"],a:1}},{{q:"What should be limited?",opts:["Water","Fruits","Processed foods","Exercise"],a:2}},{{q:"What helps maintain energy levels?",opts:["Skipping meals","Sleeping more","Regular meals","Caffeine"],a:2}}]}},
{{title:"Learning a Second Language",text:"Learning a foreign language opens doors to new cultures and opportunities. Research shows that bilingual people often have better memory and problem-solving skills. The best way to learn is through consistent practice. Watching films, reading books, and speaking with native speakers are all effective methods. Many language learners find that immersion is the fastest way to become fluent. Even making mistakes is an important part of the learning process because it helps you improve.",tr:"Yabanci dil ogrenmek yeni kulturlere ve firsatlara kapilar acar. Arastirmalar iki dilli insanlarin genellikle daha iyi hafiza ve problem cozme becerilerine sahip oldugunu gosteriyor.",qs:[{{q:"What do bilingual people have better?",opts:["Vision","Memory and problem-solving","Physical strength","Hearing"],a:1}},{{q:"What is the fastest way to become fluent?",opts:["Reading only","Grammar study","Immersion","Watching TV"],a:2}},{{q:"Are mistakes important in learning?",opts:["No, never","Yes, they help improve","Only at advanced level","Only for children"],a:1}}]}},
{{title:"The Power of Reading",text:"Reading is one of the most effective ways to expand your knowledge and improve your language skills. Studies show that people who read regularly have a larger vocabulary and better writing abilities. Reading fiction, in particular, has been linked to greater empathy because it allows readers to experience different perspectives and emotions. Libraries and bookshops continue to play an important role in communities, although e-books and audiobooks are becoming increasingly popular. Many successful people attribute their achievements to a lifelong reading habit. Even spending just twenty minutes a day with a book can make a significant difference over time.",tr:"Okuma, bilginizi genisletmenin ve dil becerilerinizi gelistirmenin en etkili yollarindan biridir. Arastirmalar duzenli okuyan kisilerin daha genis kelime hazinesine ve daha iyi yazma becerilerine sahip oldugunu gostermektedir. Ozellikle kurgu okumak, okuyucularin farkli bakis acilari ve duygulari deneyimlemesine izin verdigi icin daha fazla empatiyle iliskilendirilmistir.",qs:[{{q:"What does reading fiction improve?",opts:["Math skills","Empathy","Physical health","Memory only"],a:1}},{{q:"How much daily reading can make a difference?",opts:["Five minutes","Ten minutes","Twenty minutes","One hour"],a:2}},{{q:"What is becoming more popular?",opts:["Newspapers","E-books and audiobooks","Handwriting","Magazines"],a:1}}]}},
{{title:"Volunteering and Community",text:"Volunteering is an activity that benefits both the community and the individual. People who volunteer regularly report higher levels of happiness and life satisfaction. Volunteering can take many forms, from helping at a local food bank to teaching children in after-school programmes. It also provides valuable experience that can enhance a person's career prospects. Many universities look favourably on applicants who have volunteered. In Turkey, youth volunteering has grown significantly in recent years, with organisations focusing on education, environmental protection, and animal welfare. Giving your time to help others is one of the most rewarding things you can do.",tr:"Gonulluluk hem topluma hem bireye fayda saglayan bir faaliyettir. Duzenli gonulluluk yapan kisiler daha yuksek mutluluk ve yasam memnuniyeti bildirmektedir. Gonulluluk yerel gida bankasindan yardim etmekten okul sonrasi programlarda cocuklara ogretmenlige kadar bircok sekilde olabilir.",qs:[{{q:"What do volunteers report?",opts:["More stress","Higher happiness","Less free time","Lower income"],a:1}},{{q:"What do universities value?",opts:["Volunteering experience","Sports only","Wealth","Social media followers"],a:0}},{{q:"What areas do Turkish youth organisations focus on?",opts:["Only sports","Education and environment","Only politics","Only technology"],a:1}}]}},
{{title:"Public Transport vs Private Cars",text:"The debate between public transport and private cars continues in cities around the world. Public transport systems such as buses, trams, and metros can carry large numbers of people efficiently, reducing traffic congestion and carbon emissions. However, many people prefer the convenience and flexibility of driving their own car. In some cities, poor public transport infrastructure makes private cars a necessity rather than a choice. Governments are investing in modern transport networks to encourage people to leave their cars at home. Cycling infrastructure is also expanding, with dedicated bike lanes appearing in more and more cities. A combination of good public transport and cycling facilities seems to be the best solution for sustainable urban mobility.",tr:"Toplu tasima ve ozel araclar arasindaki tartisma dunya sehirlerinde devam etmektedir. Otobus, tramvay ve metro gibi toplu tasima sistemleri cok sayida insani verimli bir sekilde tasiyarak trafik sikisikligini ve karbon emisyonlarini azaltabilir.",qs:[{{q:"What does public transport reduce?",opts:["Jobs","Congestion and emissions","Population","Tourism"],a:1}},{{q:"Why do some people need private cars?",opts:["For fun","Poor public transport","To show off","For exercise"],a:1}},{{q:"What is expanding in more cities?",opts:["Airports","Cycling infrastructure","Shopping malls","Parking areas"],a:1}}]}},
{{title:"Sleep and Productivity",text:"Scientists have long studied the relationship between sleep and daily performance. Research consistently shows that adults need between seven and nine hours of sleep per night for optimal health and productivity. During sleep, the brain processes information from the day, consolidates memories, and repairs itself. Lack of sleep has been linked to poor concentration, weakened immune function, and increased risk of chronic diseases. Despite this evidence, many people sacrifice sleep for work or entertainment. The blue light from screens can disrupt the production of melatonin, a hormone that regulates sleep. Experts recommend avoiding screens for at least one hour before bedtime and maintaining a regular sleep schedule.",tr:"Bilim insanlari uyku ile gunluk performans arasindaki iliskiyi uzun suredir arastirmaktadir. Arastirmalar yetiskinlerin optimal saglik ve verimlilik icin gecede yedi ile dokuz saat uyuya ihtiyac duydugunu tutarli olarak gostermektedir.",qs:[{{q:"How much sleep do adults need?",opts:["5-6 hours","7-9 hours","10-12 hours","4-5 hours"],a:1}},{{q:"What does blue light disrupt?",opts:["Vision","Melatonin production","Appetite","Mood"],a:1}},{{q:"What should you avoid before bedtime?",opts:["Reading","Screens","Water","Walking"],a:1}}]}}
],
B2:[
{{title:"The Ethics of AI",text:"Artificial intelligence is transforming industries from healthcare to finance, raising profound ethical questions. While AI can diagnose diseases more accurately than human doctors in some cases, concerns about algorithmic bias and accountability persist. Who is responsible when an AI system makes an error that harms a patient? The European Union has proposed comprehensive regulations requiring transparency in AI decision-making. Critics argue these regulations could stifle innovation, while proponents believe they are essential for protecting fundamental human rights in an increasingly automated world.",tr:"Yapay zeka, sagliktan finansa kadar sektorleri donusturuyor ve derin etik sorular ortaya cikariyor.",qs:[{{q:"What ethical concern is raised about AI in healthcare?",opts:["Cost","Bias and accountability","Speed","Availability"],a:1}},{{q:"What has the EU proposed?",opts:["Banning AI","Regulations for transparency","More funding","AI competitions"],a:1}},{{q:"What do critics say about regulations?",opts:["They are perfect","They could stifle innovation","They are too weak","They help innovation"],a:1}}]}},
{{title:"Urbanisation Challenges",text:"Over half of the world's population now lives in cities, and this number is expected to grow to 68% by 2050. Rapid urbanisation creates significant challenges including housing shortages, traffic congestion, and environmental degradation. Many cities struggle to provide adequate infrastructure and public services for their expanding populations. Smart city technologies offer potential solutions, using data analytics and IoT to optimise transport, energy consumption, and waste management. However, there are concerns about surveillance and data privacy in these increasingly connected urban environments.",tr:"Dunya nufusunun yaridan fazlasi artik sehirlerde yasiyor ve bu sayinin 2050'ye kadar %68'e cikacagi tahmin ediliyor.",qs:[{{q:"What percentage will live in cities by 2050?",opts:["50%","60%","68%","75%"],a:2}},{{q:"What technology is mentioned as a solution?",opts:["Nuclear power","Smart city tech","Space tech","Farming tech"],a:1}},{{q:"What is a concern about smart cities?",opts:["Cost","Surveillance and privacy","Too slow","Unemployment"],a:1}}]}},
{{title:"The Gig Economy",text:"The traditional concept of lifelong employment with a single company is rapidly evolving. The gig economy, characterised by short-term contracts and freelance work, has expanded dramatically with the rise of digital platforms. Workers in the gig economy enjoy flexibility and autonomy but often lack benefits such as health insurance, paid leave, and pension contributions. Governments worldwide are grappling with how to regulate this new form of work while preserving its innovative character. The debate raises fundamental questions about workers' rights and the future of employment.",tr:"Tek bir sirkette omur boyu istihdam geleneksel kavrami hizla degisiyor.",qs:[{{q:"What characterises the gig economy?",opts:["Lifetime jobs","Short-term contracts","Government jobs","Factory work"],a:1}},{{q:"What do gig workers lack?",opts:["Freedom","Flexibility","Health insurance and benefits","Creativity"],a:2}},{{q:"What are governments trying to do?",opts:["Ban gig work","Regulate it","Ignore it","Promote only office work"],a:1}}]}},
{{title:"Mental Health Awareness",text:"Mental health has emerged as a critical public health issue in the 21st century. The World Health Organisation reports that depression is the leading cause of disability worldwide. Despite growing awareness, stigma surrounding mental health conditions persists in many societies, preventing individuals from seeking help. Schools and workplaces are increasingly implementing well-being programmes to address this crisis. Cognitive behavioural therapy and mindfulness practices have shown promising results in treating anxiety and depression. Experts emphasise that mental health should be treated with the same urgency as physical health.",tr:"Ruh sagligi 21. yuzyilda kritik bir halk sagligi sorunu olarak ortaya cikmistir.",qs:[{{q:"What is the leading cause of disability?",opts:["Heart disease","Cancer","Depression","Diabetes"],a:2}},{{q:"What prevents people from seeking help?",opts:["Cost","Stigma","Distance","Lack of doctors"],a:1}},{{q:"What practices show promising results?",opts:["Surgery","CBT and mindfulness","Medication only","Exercise only"],a:1}}]}},
{{title:"Renewable Energy Transition",text:"The transition from fossil fuels to renewable energy sources represents one of the most significant industrial shifts in human history. Solar panel costs have decreased by over 90% in the past decade, making them competitive with traditional energy sources. Wind energy capacity has similarly expanded, with offshore wind farms becoming increasingly viable. However, the intermittent nature of solar and wind power necessitates significant investment in energy storage solutions. Battery technology is advancing rapidly, with lithium-ion batteries becoming more efficient and affordable. The challenge remains to achieve this transition quickly enough to meet climate targets while ensuring energy security.",tr:"Fosil yakillardan yenilenebilir enerji kaynaklarina gecis, insanlik tarihindeki en onemli endustriyel degisimlerden birini temsil etmektedir.",qs:[{{q:"How much have solar panel costs decreased?",opts:["50%","70%","80%","Over 90%"],a:3}},{{q:"What is the main challenge of solar/wind?",opts:["Cost","Intermittent nature","Pollution","Noise"],a:1}},{{q:"What technology is advancing for storage?",opts:["Nuclear","Hydrogen","Lithium-ion batteries","Coal"],a:2}}]}},
{{title:"The Psychology of Persuasion",text:"Understanding how persuasion works has fascinated scholars since antiquity, but modern psychological research has brought unprecedented rigour to this field. Robert Cialdini identified six key principles of influence: reciprocity, commitment, social proof, authority, liking, and scarcity. These principles operate largely below conscious awareness, making them particularly potent in advertising, politics, and negotiations. The digital age has amplified their reach; targeted advertising exploits vast quantities of personal data to craft highly personalised persuasive messages. Behavioural nudges, subtle changes in how choices are presented, have been adopted by governments worldwide to encourage beneficial behaviours such as organ donation and pension savings. Critics argue that the line between persuasion and manipulation is dangerously thin, raising important questions about autonomy and informed consent in an era of sophisticated psychological targeting.",tr:"Iknanin nasil isleyigini anlamak antik caglardan beri akademisyenleri buyulemistir, ancak modern psikolojik arastirmalar bu alana benzeri gorulmemis bir titizlik getirmistir.",qs:[{{q:"How many principles of influence did Cialdini identify?",opts:["Four","Five","Six","Eight"],a:2}},{{q:"What do behavioural nudges change?",opts:["Laws","How choices are presented","Prices","Education"],a:1}},{{q:"What concern do critics raise?",opts:["Cost","Line between persuasion and manipulation","Complexity","Lack of research"],a:1}}]}},
{{title:"Ocean Acidification",text:"While climate change dominates environmental discourse, ocean acidification represents an equally devastating but less publicised consequence of rising carbon dioxide emissions. The oceans absorb approximately one-quarter of all CO2 produced by human activities, triggering chemical reactions that increase acidity. Since the Industrial Revolution, ocean acidity has increased by roughly thirty per cent. This shift threatens marine ecosystems on a fundamental level, particularly organisms that build calcium carbonate shells and skeletons, including corals, molluscs, and certain plankton species. Coral reefs, which support approximately twenty-five per cent of all marine species, face a particularly bleak prognosis. The economic implications are profound, as billions of people depend on marine resources for food and livelihoods. Addressing ocean acidification requires the same carbon reduction strategies needed for climate change mitigation.",tr:"Iklim degisikligi cevre soylemlerine hakim olurken, okyanus asitlenmesi artan karbondioksit emisyonlarinin esit derecede yikici ancak daha az duyurulan bir sonucunu temsil etmektedir.",qs:[{{q:"How much CO2 do oceans absorb?",opts:["Ten per cent","One-quarter","One-half","Seventy per cent"],a:1}},{{q:"How much has ocean acidity increased?",opts:["Ten per cent","Twenty per cent","Thirty per cent","Fifty per cent"],a:2}},{{q:"What percentage of marine species do coral reefs support?",opts:["Ten per cent","Twenty-five per cent","Fifty per cent","Seventy per cent"],a:1}}]}},
{{title:"The Architecture of Misinformation",text:"Misinformation has evolved from isolated incidents of rumour into a sophisticated, often industrialised phenomenon that poses existential threats to democratic governance. Research reveals that false information spreads approximately six times faster than accurate reporting on social media platforms, partly because it tends to provoke stronger emotional responses. State-sponsored disinformation campaigns have been documented across multiple countries, employing coordinated networks of fake accounts to amplify divisive narratives. The deep fake technology, which uses artificial intelligence to create convincing fabricated videos, adds a particularly alarming dimension to this challenge. Fact-checking organisations have proliferated in response, yet they face the fundamental asymmetry between the speed of misinformation production and the time required for rigorous verification. Educational institutions are increasingly recognising the need to equip citizens with critical media literacy skills as a long-term countermeasure.",tr:"Dezenformasyon, izole dedikodu olaylarindan demokratik yonetisime varolussel tehditler olusturan sofistike, cogu zaman endustrilestirilmis bir olguya evrilmistir.",qs:[{{q:"How much faster does false information spread?",opts:["Twice","Three times","Six times","Ten times"],a:2}},{{q:"What technology creates fabricated videos?",opts:["VR","Deep fake","Blockchain","5G"],a:1}},{{q:"What is proposed as a long-term solution?",opts:["Censorship","Critical media literacy","Banning social media","Government control"],a:1}}]}},
{{title:"Bioethics in the Genomic Era",text:"The rapid advancement of genomic technologies has outpaced the development of ethical frameworks necessary to govern their application. Whole genome sequencing, now available for under a thousand dollars, enables the identification of genetic predispositions to diseases, but raises profound questions about genetic privacy and discrimination. Insurance companies and employers could theoretically use genetic information to deny coverage or employment, a concern that has prompted legislation such as the Genetic Information Nondiscrimination Act in the United States. Prenatal genetic testing presents particularly complex moral dilemmas, as parents face decisions about selecting embryos based on genetic characteristics. The boundary between therapeutic intervention and genetic enhancement remains contested among bioethicists. Furthermore, the question of who owns genetic data has become increasingly urgent as private companies accumulate vast genomic databases through consumer DNA testing services.",tr:"Genomik teknolojilerin hizli ilerlemesi, uygulamalarini yonetmek icin gerekli etik cercevelerin gelistirilmesini geride birakti.",qs:[{{q:"How much does whole genome sequencing cost now?",opts:["Under $100","Under $1000","Under $10000","Under $100000"],a:1}},{{q:"What does GINA protect against?",opts:["Hacking","Genetic discrimination","Medical errors","Privacy online"],a:1}},{{q:"What ethical debate exists about prenatal testing?",opts:["Cost concerns","Selecting embryos by genetics","Hospital quality","Doctor training"],a:1}}]}},
{{title:"Urban Green Spaces and Well-being",text:"A growing body of evidence demonstrates that urban green spaces confer significant benefits on both physical and psychological health. Longitudinal studies conducted across multiple countries reveal that residents living within three hundred metres of parks or gardens report lower rates of anxiety, depression, and cardiovascular disease. The mechanisms underlying these benefits are multifaceted: green spaces encourage physical activity, reduce air pollution through natural filtration, mitigate the urban heat island effect, and provide settings for social interaction that combat loneliness. The concept of biophilia, humanity's innate affinity for nature, suggests that these benefits may be deeply rooted in our evolutionary history. Despite this evidence, urban green spaces are often inequitably distributed, with wealthier neighbourhoods enjoying substantially greater access. Urban planners are increasingly incorporating green infrastructure into city development strategies, recognising that parks, street trees, and green corridors represent investments in public health rather than mere aesthetic amenities.",tr:"Artan kanitlar kentsel yesil alanlarin hem fiziksel hem de psikolojik saglik uzerinde onemli faydalar sagladigini gostermektedir.",qs:[{{q:"What distance from parks shows health benefits?",opts:["100 metres","300 metres","500 metres","1 kilometre"],a:1}},{{q:"What is biophilia?",opts:["Fear of nature","Innate affinity for nature","Plant science","Green architecture"],a:1}},{{q:"What problem exists with green space distribution?",opts:["Too many parks","Inequitable access","Too expensive","Lack of interest"],a:1}}]}}
],
C1:[
{{title:"The Paradox of Choice",text:"In contemporary consumer culture, we are inundated with an unprecedented array of choices in virtually every domain of life. Psychologist Barry Schwartz argues in his seminal work that this abundance of options, rather than liberating us, often leads to decision paralysis, anxiety, and diminished satisfaction. The phenomenon, known as the paradox of choice, suggests that beyond a certain threshold, additional alternatives cease to be beneficial and instead become psychologically burdensome. Research in behavioural economics corroborates this thesis, demonstrating that individuals presented with fewer options frequently report greater contentment with their selections.",tr:"Cagdas tuketim kulturunde, yasamin hemen her alaninda benzeri gorulmemis bir secenek dizisiyle karsi karsiyayiz.",qs:[{{q:"What does the paradox of choice suggest?",opts:["More choices always help","Too many choices can be harmful","Choices don't matter","People like having no choice"],a:1}},{{q:"What field corroborates Schwartz's thesis?",opts:["Physics","Behavioural economics","Literature","Biology"],a:1}}]}},
{{title:"Post-Truth and Media Literacy",text:"The proliferation of digital media has fundamentally altered the information landscape, giving rise to what scholars term the 'post-truth era'. In this environment, emotional appeals and personal beliefs frequently override objective evidence in shaping public opinion. Social media algorithms, designed to maximise engagement, tend to amplify sensational and divisive content, creating filter bubbles that reinforce existing biases. Media literacy education has consequently become imperative. Critical thinking skills enable individuals to evaluate sources, identify logical fallacies, and distinguish between credible journalism and disinformation. Several countries have begun integrating media literacy into their national curricula.",tr:"Dijital medyanin yayilmasi bilgi ortamini temelden degistirdi ve akademisyenlerin 'hakikat sonrasi donem' olarak adlandirdigi duruma yol acti.",qs:[{{q:"What overrides evidence in the post-truth era?",opts:["Science","Emotional appeals and beliefs","Government data","Academic research"],a:1}},{{q:"What do social media algorithms amplify?",opts:["Educational content","Sensational content","Scientific papers","Government news"],a:1}},{{q:"What has become imperative?",opts:["Social media bans","Media literacy education","Censorship","More TV channels"],a:1}}]}},
{{title:"Neurodiversity in the Workplace",text:"The concept of neurodiversity challenges the conventional notion that neurological differences such as autism, ADHD, and dyslexia are inherently deficits requiring correction. Instead, this paradigm recognises that cognitive variation is a natural and potentially valuable aspect of human diversity. Forward-thinking organisations have begun to redesign their recruitment processes and work environments to accommodate neurodiverse employees. Research indicates that teams incorporating diverse cognitive styles often demonstrate enhanced problem-solving capabilities and innovation. Companies such as SAP, Microsoft, and JP Morgan have established dedicated neurodiversity hiring programmes, reporting significant benefits.",tr:"Noroceisitlilik kavrami, otizm, DEHB ve disleksi gibi norolojik farkliliklarin duzeltme gerektiren eksiklikler oldugu geleneksel gorusune meydan okur.",qs:[{{q:"What does neurodiversity challenge?",opts:["Intelligence tests","The deficit view of neurological differences","Workplace rules","Education systems"],a:1}},{{q:"What do diverse cognitive teams show?",opts:["More conflict","Enhanced problem-solving","Slower work","Higher costs"],a:1}},{{q:"Which company has a neurodiversity programme?",opts:["Apple","Tesla","SAP","Amazon"],a:2}}]}},
{{title:"The Future of Food",text:"As the global population approaches ten billion, food systems face unprecedented pressure to produce more with fewer resources. Vertical farming, cultivating crops in stacked indoor layers using controlled environments, offers a promising solution for urban food production. Lab-grown meat, produced by culturing animal cells, could dramatically reduce the environmental footprint of protein production. Precision agriculture employs satellite imagery, drones, and AI to optimise crop yields while minimising water and pesticide usage. Gene editing technologies like CRISPR enable the development of crop varieties resistant to disease and climate stress. These innovations collectively suggest a radical transformation of how humanity will feed itself.",tr:"Kuresel nufus on milyara yaklasirken, gida sistemleri daha az kaynakla daha fazla uretim yapmak icin benzersiz bir baskinla karsi karsiya.",qs:[{{q:"What is vertical farming?",opts:["Farming on hills","Indoor stacked crop cultivation","Underground farming","Floating farms"],a:1}},{{q:"What could reduce protein production's footprint?",opts:["More cattle","Organic farming","Lab-grown meat","Fish farming"],a:2}},{{q:"What does CRISPR enable?",opts:["Faster cooking","Disease-resistant crops","Better packaging","Cheaper transport"],a:1}}]}},
{{title:"Digital Currencies and Central Banking",text:"The emergence of cryptocurrencies has compelled central banks worldwide to reconsider the nature of money itself. Central Bank Digital Currencies represent sovereign digital money that could transform monetary policy implementation and financial inclusion. Unlike decentralised cryptocurrencies such as Bitcoin, CBDCs would be issued and regulated by central authorities. China's digital yuan pilot programme has been among the most advanced, whilst the European Central Bank continues to explore a digital euro. Proponents argue that CBDCs could reduce transaction costs, combat money laundering, and extend banking services to unbanked populations. Critics, however, raise concerns about government surveillance capabilities and the potential disintermediation of commercial banks.",tr:"Kripto paralarin ortaya cikisi, dunya capinda merkez bankalarini paranin dogasini yeniden dusunmeye zorladi.",qs:[{{q:"What are CBDCs?",opts:["Private crypto","Sovereign digital money","Bank stocks","Credit cards"],a:1}},{{q:"Which country has an advanced CBDC pilot?",opts:["USA","UK","China","Japan"],a:2}},{{q:"What concern do critics raise?",opts:["Inflation","Government surveillance","Too expensive","Too slow"],a:1}}]}},
{{title:"The Attention Economy",text:"In an era of information superabundance, human attention has emerged as the scarcest and most contested resource. Technology companies have engineered increasingly sophisticated mechanisms to capture and retain user engagement, deploying variable reward schedules reminiscent of slot machines, infinite scrolling interfaces, and algorithmically curated content feeds designed to exploit psychological vulnerabilities. The consequences of this attention economy extend beyond individual well-being to encompass societal-level effects, including the fragmentation of shared narratives, the erosion of deep reading and sustained concentration, and the commodification of intimate personal data. Tristan Harris, a former Google design ethicist, has been particularly vocal in articulating how persuasive technology design creates what he terms a race to the bottom of the brain stem. The growing movement for humane technology advocates for regulatory frameworks that would compel platforms to prioritise user welfare over engagement metrics, though critics question whether such regulation can keep pace with technological innovation.",tr:"Bilgi bollugu caginda, insan dikkati en kitsit ve en cok tartisilan kaynak olarak ortaya cikmistir.",qs:[{{q:"What has emerged as the scarcest resource?",opts:["Money","Time","Human attention","Energy"],a:2}},{{q:"Who is Tristan Harris?",opts:["A politician","A former Google design ethicist","A professor","A journalist"],a:1}},{{q:"What does the humane technology movement advocate?",opts:["More engagement","Regulatory frameworks for user welfare","Banning technology","More advertising"],a:1}}]}},
{{title:"Linguistic Relativity Revisited",text:"The relationship between language and thought has fascinated philosophers and linguists for centuries, but contemporary research in cognitive science has reinvigorated this discourse with empirical rigour. The Sapir-Whorf hypothesis, in its strong form suggesting that language determines thought, has largely been abandoned; however, its weaker variant, proposing that language influences cognitive processes, has garnered substantial experimental support. Studies by Lera Boroditsky and colleagues have demonstrated that speakers of languages with different spatial reference systems, temporal metaphors, or colour terminology exhibit measurably different patterns of perception and reasoning. For instance, speakers of Kuuk Thaayorre, an Australian Aboriginal language that uses cardinal directions rather than relative spatial terms, demonstrate superior spatial orientation. The implications extend to second language acquisition, suggesting that learning a new language does not merely provide a communicative tool but potentially restructures aspects of cognition, offering learners genuinely novel perspectives on reality.",tr:"Dil ve dusunce arasindaki iliski yuzyillardir filozoflari ve dilbilimcileri buyulemistir, ancak bilissel bilimdeki cagdas arastirmalar bu soylemi ampirik titizlikle yeniden canlandirmistir.",qs:[{{q:"What has happened to the strong Sapir-Whorf hypothesis?",opts:["It was confirmed","It was largely abandoned","It was strengthened","It was never tested"],a:1}},{{q:"What did Boroditsky's studies demonstrate?",opts:["All languages are the same","Language influences perception","Grammar is universal","Translation is impossible"],a:1}},{{q:"What does learning a new language potentially do?",opts:["Nothing cognitive","Restructures aspects of cognition","Reduces intelligence","Only helps communication"],a:1}}]}},
{{title:"The Ethics of Algorithmic Governance",text:"As governments increasingly delegate decision-making processes to algorithmic systems, fundamental questions arise about accountability, transparency, and democratic legitimacy. Predictive policing algorithms, welfare eligibility assessments, and judicial risk scoring tools now influence consequential decisions affecting millions of citizens. Proponents argue that algorithms can reduce human bias and improve consistency in administrative decisions. However, extensive research has revealed that these systems frequently encode and amplify existing societal biases, disproportionately affecting marginalised communities. The opacity of many machine learning models, often described as black boxes, compounds the problem by making it difficult for affected individuals to understand or contest algorithmic decisions. The European Union proposed AI Act attempts to address these concerns through a risk-based regulatory framework that would impose stringent requirements on high-risk AI systems. Legal scholars debate whether existing constitutional frameworks adequately protect citizens against algorithmic harms or whether entirely new legal paradigms are required.",tr:"Hukumetler karar alma sureclerini giderek daha fazla algoritmik sistemlere devrettikce, hesap verebilirlik, seffaflik ve demokratik mesruiyet hakkinda temel sorular ortaya cikmaktadir.",qs:[{{q:"What is a concern about algorithmic systems?",opts:["Speed","Encoding existing biases","Cost savings","Too much transparency"],a:1}},{{q:"What are opaque ML models often called?",opts:["White boxes","Glass boxes","Black boxes","Grey boxes"],a:2}},{{q:"What approach does the EU AI Act take?",opts:["Ban all AI","Risk-based framework","No regulation","Industry self-regulation"],a:1}}]}},
{{title:"Intergenerational Justice and Climate Policy",text:"The concept of intergenerational justice presents a profound philosophical challenge for climate policy, requiring present generations to make significant sacrifices for the benefit of people who do not yet exist. Traditional economic frameworks, which heavily discount future costs and benefits, systematically undervalue the welfare of future generations, leading to policy recommendations that many ethicists consider morally indefensible. The influential Stern Review on the Economics of Climate Change challenged conventional discounting practices, arguing that the well-being of future generations deserves substantially greater weight in present-day calculations. Philosopher John Rawls veil of ignorance thought experiment provides another compelling framework: if individuals did not know which generation they would inhabit, rational agents would advocate for policies ensuring adequate environmental conditions across all time periods. Youth climate movements, exemplified by Greta Thunberg and Fridays for Future, have forcefully articulated this intergenerational dimension, framing climate inaction as a violation of the rights of young people and future generations.",tr:"Kusaklararasi adalet kavrami, iklim politikasi icin derin bir felsefi zorluk sunarak mevcut nesillerin henuz var olmayan insanlarin yararina onemli fedakarliklar yapmasini gerektirmektedir.",qs:[{{q:"What do traditional economic frameworks do to future welfare?",opts:["Overvalue it","Systematically undervalue it","Ignore it completely","Measure it accurately"],a:1}},{{q:"What did the Stern Review challenge?",opts:["Climate science","Conventional discounting practices","Renewable energy","Youth movements"],a:1}},{{q:"What framework does Rawls provide?",opts:["Cost-benefit analysis","Veil of ignorance","Market theory","Game theory"],a:1}}]}},
{{title:"The Microbiome Revolution",text:"The discovery that the human body harbours trillions of microorganisms, collectively termed the microbiome, has precipitated a paradigm shift in biomedical science. These microbial communities, predominantly residing in the gastrointestinal tract, are now understood to play crucial roles in immune system development, nutrient metabolism, pathogen resistance, and even neurological function through what researchers term the gut-brain axis. Perturbations of the microbiome, or dysbiosis, have been implicated in conditions ranging from inflammatory bowel disease and obesity to depression and autoimmune disorders. The therapeutic potential is immense: faecal microbiota transplantation has proven remarkably effective against recurrent Clostridioides difficile infections, whilst researchers are exploring microbiome-based interventions for metabolic syndrome and certain cancers. However, the complexity of microbial ecosystems, which vary significantly between individuals and are influenced by diet, medication, geography, and genetics, makes standardised therapeutic approaches exceptionally challenging. The field remains in its relative infancy, and researchers caution against premature commercialisation of probiotic products that outpace scientific evidence.",tr:"Insan vucudunun toplu olarak mikrobiyom olarak adlandirilan trilyonlarca mikroorganizmayi barindirdigi kesfi, biyomedikal bilimde bir paradigma degisikligini tetiklemistir.",qs:[{{q:"Where do most microbiome organisms reside?",opts:["Skin","Lungs","Gastrointestinal tract","Blood"],a:2}},{{q:"What is the gut-brain axis?",opts:["A surgery technique","Microbiome-neurological connection","A type of bacteria","A diet plan"],a:1}},{{q:"What treatment works against C. difficile?",opts:["Antibiotics only","Faecal microbiota transplantation","Surgery","Probiotics alone"],a:1}}]}}
],
C2:[
{{title:"Epistemic Humility",text:"The contemporary discourse surrounding epistemic humility invites a fundamental reassessment of how we conceptualise knowledge acquisition and intellectual certainty. Distinguished from mere self-deprecation or intellectual timidity, epistemic humility constitutes a sophisticated metacognitive stance that acknowledges the inherent limitations of human cognition whilst simultaneously maintaining a robust commitment to rational inquiry. Philosophers from Socrates to contemporary epistemologists have grappled with the productive tension between acknowledging what we do not know and the imperative to expand the frontiers of understanding. In an era characterised by the proliferation of information and the attendant challenges of misinformation, cultivating epistemic humility has become not merely an intellectual virtue but a pragmatic necessity.",tr:"Epistemik alcakgonulluluk etrafindaki cagdas soylem, bilgi edinimi ve entelektuel kesinligi nasil kavramsallastigimizin temel bir yeniden degerlendirilmesine davet eder.",qs:[{{q:"What is epistemic humility distinguished from?",opts:["Arrogance","Self-deprecation and timidity","Confidence","Ignorance"],a:1}},{{q:"Epistemic humility is described as?",opts:["Unnecessary","A pragmatic necessity","Outdated","Simple"],a:1}}]}},
{{title:"The Anthropocene Debate",text:"The proposition to designate the current geological epoch as the Anthropocene has generated considerable scholarly debate across disciplines. Advocates contend that human activity has so fundamentally altered Earth's geological, atmospheric, and biological systems that a formal stratigraphic distinction is warranted. The precise commencement date remains contentious: some scholars argue for the advent of agriculture approximately twelve thousand years ago, whilst others point to the Great Acceleration following the Second World War as the definitive marker. The International Commission on Stratigraphy has deliberated extensively, with the Anthropocene Working Group proposing Crawford Lake in Ontario as a Global Boundary Stratotype Section and Point. Beyond its scientific significance, the Anthropocene concept carries profound philosophical implications about humanity's relationship with the natural world and our collective responsibility for planetary stewardship.",tr:"Mevcut jeolojik donemi Antroposen olarak adlandirma onerisi disiplinler arasi kayda deger akademik tartisma yaratmistir.",qs:[{{q:"What does the Anthropocene concept refer to?",opts:["A new planet","Human-altered geological epoch","Climate cooling","Ocean currents"],a:1}},{{q:"What was proposed as a reference point?",opts:["Mount Everest","Crawford Lake","Grand Canyon","Dead Sea"],a:1}},{{q:"What philosophical issue does it raise?",opts:["Space travel","Humanity's responsibility for the planet","Technology ethics","Economic growth"],a:1}}]}},
{{title:"Consciousness and Machine Intelligence",text:"The question of whether artificial systems can possess genuine consciousness constitutes one of the most profound philosophical challenges of the twenty-first century. The so-called 'hard problem of consciousness', articulated by David Chalmers, concerns why and how physical processes give rise to subjective experience. Functionalist accounts suggest that consciousness is substrate-independent and could theoretically emerge in any sufficiently complex information-processing system. Conversely, biological naturalists such as John Searle argue that consciousness is an inherently biological phenomenon that cannot be replicated through computation alone. The Chinese Room thought experiment illustrates this position, demonstrating that syntactic manipulation of symbols need not entail semantic understanding. As large language models exhibit increasingly sophisticated behavioural outputs, the demarcation between genuine understanding and mere simulation becomes ever more philosophically fraught.",tr:"Yapay sistemlerin gercek bilince sahip olup olamayacagi sorusu, yirmi birinci yuzyilin en derin felsefi zorluklarindan birini olusturmaktadir.",qs:[{{q:"Who articulated the 'hard problem of consciousness'?",opts:["Turing","Searle","Chalmers","Dennett"],a:2}},{{q:"What does functionalism suggest?",opts:["Only brains can be conscious","Consciousness needs biology","Consciousness is substrate-independent","Machines cannot think"],a:2}},{{q:"What does the Chinese Room demonstrate?",opts:["AI can think","Symbol manipulation is not understanding","Computers are fast","Language is simple"],a:1}}]}},
{{title:"Degrowth Economics",text:"The degrowth movement presents a radical critique of the prevailing economic paradigm that equates prosperity with perpetual GDP expansion. Proponents argue that infinite growth on a finite planet is not merely unsustainable but fundamentally incompatible with ecological integrity and genuine human flourishing. Drawing on the work of economists such as Serge Latouche and anthropologist Jason Hickel, the movement advocates for a planned reduction of energy and resource throughput whilst simultaneously improving quality of life through equitable redistribution. This entails reimagining metrics of societal progress beyond GDP, embracing indicators such as the Genuine Progress Indicator or Bhutan's Gross National Happiness index. Critics contend that degrowth is politically infeasible and could precipitate unemployment and poverty, particularly in developing nations.",tr:"Kuculsme hareketi, refahi surekli GSYH buyumesiyle esitleyen hakim ekonomik paradigmanin radikal bir elestirisini sunar.",qs:[{{q:"What does degrowth critique?",opts:["Technology","Perpetual GDP growth paradigm","Democracy","Education"],a:1}},{{q:"What alternative metric is mentioned?",opts:["Stock market","Gross National Happiness","Military spending","Trade volume"],a:1}},{{q:"What do critics say about degrowth?",opts:["It is too expensive","It is politically infeasible","It is too popular","It works perfectly"],a:1}}]}},
{{title:"Quantum Computing Implications",text:"Quantum computing represents a paradigmatic shift in computational capability that promises to reshape fields ranging from cryptography to pharmaceutical research. Unlike classical bits, which exist in binary states, quantum bits or qubits exploit superposition and entanglement to perform certain calculations exponentially faster. Google's achievement of quantum supremacy in 2019, subsequently contested by IBM, demonstrated a computation that would have taken classical supercomputers millennia. The implications for cryptographic security are particularly consequential: Shor's algorithm, when implemented on a sufficiently powerful quantum computer, could render current RSA encryption obsolete. Post-quantum cryptography research has consequently become an urgent priority for national security agencies. Simultaneously, quantum simulation capabilities could revolutionise drug discovery by accurately modelling molecular interactions at the quantum level.",tr:"Kuantum bilisim, kriptografiden ilac arastirmasina kadar alanlari yeniden sekillendirmeye soz veren hesaplama yeteneginde paradigmatik bir degisimi temsil eder.",qs:[{{q:"What do qubits exploit?",opts:["Binary states","Superposition and entanglement","Electrical signals","Light waves"],a:1}},{{q:"What could Shor's algorithm make obsolete?",opts:["Quantum computers","Classical physics","RSA encryption","The internet"],a:2}},{{q:"What could quantum simulation revolutionise?",opts:["Social media","Drug discovery","Space travel","Agriculture"],a:1}}]}},
{{title:"The Phenomenology of Time",text:"The nature of temporal experience constitutes one of the most enduring and perplexing problems in philosophy, straddling the boundaries between metaphysics, phenomenology, and cognitive science. Augustine of Hippo famously articulated the paradox: we speak confidently about time, yet when pressed to define it, find ourselves confounded. Husserl's analysis of time-consciousness distinguished between retention, the immediate awareness of what has just passed, primal impression, the awareness of the present moment, and protention, the anticipation of what is about to occur. This tripartite structure suggests that temporal experience is never punctual but always extends across a specious present. Heidegger radicalised this analysis by arguing that temporality is not merely a feature of consciousness but the fundamental horizon of Being itself, with authentic existence requiring a confrontation with one's finitude. Contemporary neuroscience has complicated these philosophical accounts by demonstrating that subjective time perception is remarkably plastic, influenced by emotional state, attentional focus, body temperature, and neurological conditions. The discovery that the brain constructs temporal experience through multiple neural mechanisms rather than possessing a single internal clock challenges naive assumptions about the objectivity of temporal perception.",tr:"Zamansal deneyimin dogasi, metafizik, fenomenoloji ve bilissel bilim arasindaki sinirlari asarak felsefedeki en kalici ve sasirtici problemlerden birini olusturmaktadir.",qs:[{{q:"What tripartite structure did Husserl identify?",opts:["Past, present, future","Retention, primal impression, protention","Memory, perception, imagination","Beginning, middle, end"],a:1}},{{q:"What did Heidegger argue about temporality?",opts:["It is an illusion","It is the fundamental horizon of Being","It is only physical","It does not exist"],a:1}},{{q:"What has neuroscience shown about time perception?",opts:["It is perfectly accurate","It is constructed by multiple neural mechanisms","It cannot be studied","It is the same for everyone"],a:1}}]}},
{{title:"Postcolonial Epistemologies",text:"The postcolonial critique of Western epistemological hegemony has emerged as one of the most intellectually consequential developments in contemporary scholarship, fundamentally interrogating whose knowledge counts and through what mechanisms certain ways of knowing have been systematically marginalised. Scholars such as Boaventura de Sousa Santos have articulated the concept of epistemicide, the systematic destruction of indigenous knowledge systems through colonial violence and subsequent institutional perpetuation. Walter Mignolo's notion of epistemic disobedience calls for a deliberate delinking from Eurocentric frameworks that have historically positioned Western scientific rationality as the universal standard against which all other knowledge traditions are measured. This critique does not advocate for relativism or the abandonment of rigorous inquiry; rather, it argues for an ecology of knowledges that recognises the validity of multiple epistemological traditions and their potential contributions to addressing contemporary global challenges. Indigenous ecological knowledge, for instance, has proven invaluable in biodiversity conservation and sustainable resource management, often surpassing Western scientific approaches in specific contexts.",tr:"Bati epistemolojik hegemonyasinin postkolonyal elestirisi, kimin bilgisinin gecerli sayildigi ve belirli bilme yollarinin hangi mekanizmalarla sistematik olarak marjinalize edildigi konusunu temelden sorgulayarak cagdas akademide en onemli entelektuel gelismelerden biri olarak ortaya cikmistir.",qs:[{{q:"What is epistemicide?",opts:["Study of knowledge","Systematic destruction of indigenous knowledge","A type of philosophy","Academic fraud"],a:1}},{{q:"What does Mignolo call for?",opts:["More Western science","Epistemic disobedience","Abandoning all knowledge","Cultural isolation"],a:1}},{{q:"What has indigenous ecological knowledge proven useful for?",opts:["Space exploration","Biodiversity conservation","Industrial production","Military strategy"],a:1}}]}},
{{title:"The Paradox of Tolerance",text:"Karl Popper's paradox of tolerance, first articulated in The Open Society and Its Enemies, presents a fundamental challenge for liberal democratic societies: if a society is tolerant without limit, its ability to be tolerant will eventually be seized or destroyed by the intolerant. This philosophical puzzle has acquired renewed urgency in the context of social media platforms grappling with content moderation, the resurgence of extremist movements exploiting democratic freedoms, and the broader question of where the boundaries of permissible discourse should be drawn. John Rawls's reformulation frames the issue in terms of an unreasonable use of public reason, arguing that intolerant groups forfeit their claim to tolerance when they genuinely threaten the constitutional order. Jurgen Habermas offers an alternative perspective through his discourse ethics, suggesting that the legitimacy of any boundary on speech must itself be established through inclusive deliberative processes. The practical implications are profound: democratic societies must navigate between the Scylla of excessive censorship, which undermines the very openness they seek to protect, and the Charybdis of unlimited tolerance, which may enable forces that seek to destroy democratic institutions from within.",tr:"Karl Popper'in tolerans paradoksu, liberal demokratik toplumlar icin temel bir zorluk sunmaktadir: eger bir toplum sinirsiz toleransli olursa, toleransli olabilme yetenegi sonunda toleranssizlar tarafindan ele gecirilecek veya yok edilecektir.",qs:[{{q:"Who first articulated the paradox of tolerance?",opts:["Rawls","Habermas","Popper","Mill"],a:2}},{{q:"What does Rawls argue about intolerant groups?",opts:["They should always be tolerated","They forfeit their claim to tolerance","They should be ignored","They strengthen democracy"],a:1}},{{q:"What two dangers must democracies navigate between?",opts:["War and peace","Excessive censorship and unlimited tolerance","Wealth and poverty","Freedom and order"],a:1}}]}},
{{title:"Complexity Theory and Emergent Systems",text:"Complexity theory represents a profound departure from the reductionist paradigm that has dominated Western scientific thought since the Enlightenment, proposing instead that many of the most significant phenomena in nature and society arise from the interactions of simple components following local rules, without any centralised coordination or blueprint. The behaviour of ant colonies, the formation of market prices, the emergence of consciousness, and the evolution of language all exemplify emergent properties that cannot be predicted from or reduced to the characteristics of their constituent elements. Stuart Kauffman's work on self-organisation at the edge of chaos suggests that complex adaptive systems naturally evolve toward a critical state where they are maximally sensitive to perturbation, enabling both stability and innovation. The Santa Fe Institute has been instrumental in developing cross-disciplinary approaches to complexity, drawing on insights from physics, biology, economics, and computer science. The implications for social policy are profound: attempts to control complex systems through top-down intervention frequently produce unintended consequences, suggesting that effective governance may require embracing uncertainty and fostering conditions for beneficial emergence rather than imposing predetermined outcomes.",tr:"Karmasiklik teorisi, dogada ve toplumda en onemli olgularin bircogonun basit bilesenlerin yerel kurallari izleyerek merkezi bir koordinasyon olmaksizin etkilesimlerinden ortaya ciktigini onererek Aydinlanma'dan bu yana Bati bilimsel dusuncesine hakim olan indirgemeci paradigmadan derin bir kopusu temsil etmektedir.",qs:[{{q:"What does complexity theory challenge?",opts:["Evolution","The reductionist paradigm","Mathematics","Quantum physics"],a:1}},{{q:"What does Kauffman's work suggest about complex systems?",opts:["They are random","They evolve toward the edge of chaos","They are always stable","They cannot be studied"],a:1}},{{q:"What do top-down interventions in complex systems often produce?",opts:["Perfect outcomes","Unintended consequences","No effect","Immediate success"],a:1}}]}},
{{title:"The Philosophy of Personal Identity",text:"The question of what constitutes personal identity across time has generated some of the most imaginative thought experiments in philosophical history, from Locke's prince and cobbler scenario to Derek Parfit's teletransportation paradox. The psychological continuity theory, which locates identity in connected chains of memory, intention, and personality, faces the challenge that memories are reconstructive rather than reproductive, meaning that our sense of autobiographical continuity may be substantially confabulated. The biological continuity view, which grounds identity in bodily continuity, must contend with the fact that virtually all cellular material is replaced over approximately seven years. Parfit's revolutionary contribution was to argue that personal identity is not what matters in survival; rather, what matters is psychological continuity and connectedness, which can theoretically hold in branching cases where identity, being a one-one relation, cannot. This has profound implications for ethics, particularly regarding our obligations to our future selves, the rationality of prudential concern, and the justification of punishment. The advent of technologies such as brain-computer interfaces, whole brain emulation, and advanced prosthetics renders these once purely theoretical questions increasingly pertinent to practical decision-making.",tr:"Zaman icinde kisisel kimligi neyin olusturdugu sorusu, felsefi tarihin en yaratici dusunce deneylerinden bazilarini uretmistir.",qs:[{{q:"What does the psychological continuity theory locate identity in?",opts:["DNA","Memory and personality chains","Physical body","Soul"],a:1}},{{q:"What was Parfit's revolutionary argument?",opts:["Identity is everything","Personal identity is not what matters in survival","Memory is perfect","The body defines us"],a:1}},{{q:"What modern technologies make these questions practical?",opts:["Social media","Brain-computer interfaces","Electric cars","Smartphones"],a:1}}]}}
]
}};

// ===================== WRITING PROMPTS =====================
var WPROMPTS={{
A1:["Write about your family (5-8 sentences).","Describe your room. What is in it?","What do you do every day? Write your routine.","Write about your favourite food. Why do you like it?","Describe your best friend. What does he/she look like?","Write about your school. What subjects do you like?","What is your favourite animal? Describe it.","Write about your town or city. What is there?"],
A2:["Write about your last holiday (8-10 sentences).","Describe your best friend and what you do together.","Write about your favourite hobby and why you enjoy it.","What did you do last weekend? Tell the story.","Write a letter to a pen pal introducing yourself.","Describe the house or flat you live in.","Write about a celebration in your country.","What is your favourite season? Why?","Describe a teacher you like and explain why.","Write about what you want to be when you grow up."],
B1:["Write about the advantages and disadvantages of social media.","Describe a memorable trip you have taken.","What would you do if you won the lottery?","Write about the importance of learning English.","Should schools give homework? Give your opinion with reasons.","Write about the effects of fast food on health.","Describe a person who has influenced your life and explain how.","Write about the role of technology in education.","What are the benefits of living in a big city vs a small town?","Write about an environmental problem and suggest solutions."],
B2:["Discuss the impact of technology on education and learning outcomes.","Write about the role of media in shaping public opinion.","Should university education be free? Discuss both sides.","Analyse the effects of globalisation on local cultures.","To what extent should governments control social media?","Discuss the ethical issues surrounding animal testing.","Write about the challenges of multiculturalism in modern cities.","Analyse the relationship between economic growth and happiness.","Should voting be compulsory? Present arguments for and against.","Write about the future of work in an AI-driven world."],
C1:["Critically evaluate the role of artificial intelligence in modern healthcare.","Discuss the ethical implications of genetic engineering and designer babies.","To what extent should governments regulate the internet?","Analyse the relationship between economic growth and environmental sustainability.","Evaluate the argument that globalisation benefits developed nations more than developing ones.","Discuss whether social media has strengthened or weakened democratic processes.","Critically assess the effectiveness of international organisations in maintaining peace.","Analyse the impact of automation on employment and income inequality.","Evaluate the role of education in promoting social mobility.","Discuss the philosophical implications of space colonisation."],
C2:["Examine the philosophical implications of consciousness in artificial systems.","Critically assess the notion that language shapes thought (Sapir-Whorf hypothesis).","Evaluate the tension between individual liberty and collective responsibility in democratic societies.","Discuss the epistemological challenges posed by post-truth politics.","Analyse the concept of degrowth as an alternative to neoliberal capitalism.","Critically examine the role of narrative in constructing historical truth.","Evaluate whether scientific objectivity is attainable or inherently perspectival.","Discuss the ethical frameworks applicable to autonomous weapons systems.","Analyse the implications of CRISPR technology for human evolution.","Examine the relationship between linguistic diversity and cognitive diversity."]
}};

// ===================== TTS ENGINE =====================
var ttsV=null,ttsR=false;
function initTTS(){{
  if(!window.speechSynthesis)return;
  function pick(){{var v=speechSynthesis.getVoices();
    var p=['Google US English','Google UK English Female','Microsoft Zira','Samantha'];
    for(var i=0;i<p.length;i++)for(var j=0;j<v.length;j++)
      if(v[j].name.indexOf(p[i])!==-1&&v[j].lang.indexOf('en')===0){{ttsV=v[j];ttsR=true;return;}}
    for(var j=0;j<v.length;j++)if(v[j].lang.indexOf('en')===0){{ttsV=v[j];ttsR=true;return;}}
    ttsR=true;
  }}
  if(speechSynthesis.getVoices().length)pick();
  speechSynthesis.onvoiceschanged=pick;
}}
initTTS();
var ttsRate=0.85;
function speak(text){{
  if(!window.speechSynthesis)return;speechSynthesis.cancel();
  var u=new SpeechSynthesisUtterance(text);u.lang='en-US';u.rate=ttsRate;u.pitch=1;u.volume=1;
  if(ttsV)u.voice=ttsV;
  speechSynthesis.speak(u);
}}

// ===================== STATE =====================
var TAB='dash';
var S={{
  level:'A1',cat:'',learnIdx:0,flipped:false,subTab:'',
  quiz:{{qs:[],cur:0,score:0,ans:false,sel:-1,type:'',timer:null,timeLeft:0,startTime:0}},
  readIdx:0,listenIdx:0,writeIdx:0,gramIdx:-1,
  dictText:'',dictInput:'',listenSpeed:0.85,
  speakIdx:0,phraseSub:'phrasal',recording:false,spokenText:'',
  placement:null
}};

// ===================== PROGRESS (localStorage) =====================
var PK='kdg_'+USER;
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
      opts2=shuffle(opts2);qs.push({{stem:w.t+' = ? (English)',opts:opts2,correct:opts2.indexOf(w.e),lv:lv,type:'vocab'}});
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
A1:[{{pv:'wake up',tr:'uyanmak',ex:'I wake up at seven.'}},{{pv:'get up',tr:'kalkmak',ex:'She gets up early.'}},{{pv:'sit down',tr:'oturmak',ex:'Please sit down.'}},{{pv:'stand up',tr:'ayaga kalkmak',ex:'Stand up, please.'}},{{pv:'put on',tr:'giymek',ex:'Put on your coat.'}},{{pv:'take off',tr:'cikarmak',ex:'Take off your shoes.'}},{{pv:'turn on',tr:'acmak',ex:'Turn on the TV.'}},{{pv:'turn off',tr:'kapatmak',ex:'Turn off the light.'}},{{pv:'look at',tr:'bakmak',ex:'Look at the board.'}},{{pv:'listen to',tr:'dinlemek',ex:'Listen to the teacher.'}}],
A2:[{{pv:'look for',tr:'aramak',ex:'I am looking for my keys.'}},{{pv:'give up',tr:'pes etmek',ex:"Don't give up!"}},{{pv:'pick up',tr:'almak/toplamak',ex:'Pick up the phone.'}},{{pv:'throw away',tr:'atmak',ex:'Throw away the trash.'}},{{pv:'come back',tr:'geri donmek',ex:'Come back soon!'}},{{pv:'find out',tr:'ogrenmek',ex:'I found out the answer.'}},{{pv:'go on',tr:'devam etmek',ex:'Go on, please.'}},{{pv:'run out',tr:'bitmek/tukenmek',ex:'We ran out of milk.'}},{{pv:'set up',tr:'kurmak',ex:'Set up the equipment.'}},{{pv:'work out',tr:'egzersiz yapmak',ex:'I work out every day.'}}],
B1:[{{pv:'bring up',tr:'gundeme getirmek',ex:'She brought up a good point.'}},{{pv:'carry out',tr:'uygulamak',ex:'We need to carry out the plan.'}},{{pv:'come up with',tr:'bulmak/uretmek',ex:'He came up with a great idea.'}},{{pv:'deal with',tr:'ilgilenmek',ex:'I can deal with this problem.'}},{{pv:'figure out',tr:'cozmek',ex:'I figured out the answer.'}},{{pv:'give in',tr:'boyun egmek',ex:'She finally gave in.'}},{{pv:'keep up',tr:'ayak uydurmak',ex:'Keep up with the class.'}},{{pv:'look into',tr:'arastirmak',ex:'We will look into the issue.'}},{{pv:'put off',tr:'ertelemek',ex:"Don't put off your homework."}},{{pv:'take over',tr:'devralmak',ex:'She took over the company.'}}],
B2:[{{pv:'break down',tr:'bozulmak/cokertmek',ex:'The car broke down.'}},{{pv:'call off',tr:'iptal etmek',ex:'They called off the meeting.'}},{{pv:'cut down on',tr:'azaltmak',ex:'Cut down on sugar.'}},{{pv:'drop out',tr:'birakmak',ex:'He dropped out of school.'}},{{pv:'fall through',tr:'suya dusmek',ex:'The deal fell through.'}},{{pv:'get away with',tr:'yanina kar kalmak',ex:'He got away with it.'}},{{pv:'hold on',tr:'beklemek',ex:'Hold on a moment.'}},{{pv:'make up for',tr:'telafi etmek',ex:'I will make up for lost time.'}},{{pv:'put up with',tr:'katlanmak',ex:'I cannot put up with this noise.'}},{{pv:'turn down',tr:'reddetmek',ex:'She turned down the offer.'}}],
C1:[{{pv:'account for',tr:'aciklamak',ex:'This accounts for the difference.'}},{{pv:'bear in mind',tr:'akilda tutmak',ex:'Bear in mind the deadline.'}},{{pv:'boil down to',tr:'oze inmek',ex:'It boils down to money.'}},{{pv:'brush up on',tr:'tazelemek',ex:'Brush up on your grammar.'}},{{pv:'come across as',tr:'izlenimi vermek',ex:'She comes across as confident.'}},{{pv:'dawn on',tr:'farkina varmak',ex:'It dawned on me suddenly.'}},{{pv:'do away with',tr:'ortadan kaldirmak',ex:'They did away with the old rules.'}},{{pv:'live up to',tr:'karsilamak',ex:'Live up to expectations.'}},{{pv:'narrow down',tr:'daraltmak',ex:'Narrow down the options.'}},{{pv:'rule out',tr:'eleme',ex:'We cannot rule out that possibility.'}}],
C2:[{{pv:'be taken aback',tr:'sasirmak',ex:'I was taken aback by the news.'}},{{pv:'bring to bear',tr:'uygulamak/kullanmak',ex:'Bring experience to bear on the issue.'}},{{pv:'come into play',tr:'devreye girmek',ex:'Other factors come into play.'}},{{pv:'gloss over',tr:'goz ardi etmek',ex:"Don't gloss over the problems."}},{{pv:'hammer out',tr:'uzun sure calisarak halletmek',ex:'We hammered out an agreement.'}},{{pv:'latch onto',tr:'yapisip kalmak',ex:'She latched onto the idea.'}},{{pv:'phase out',tr:'kademe kademe kaldirmak',ex:'They phased out the old system.'}},{{pv:'reel off',tr:'art arda sayip dokmek',ex:'He reeled off a list of names.'}},{{pv:'shy away from',tr:'cekinmek',ex:"Don't shy away from challenges."}},{{pv:'zero in on',tr:'odaklanmak',ex:'Zero in on the main issue.'}}]
}};
var IDIOMS={{
A1:[{{idiom:'break the ice',tr:'buzlari kirmak',ex:'A joke can break the ice.',meaning:'Make people feel more comfortable'}},{{idiom:'a piece of cake',tr:'cok kolay',ex:'The test was a piece of cake.',meaning:'Very easy'}},{{idiom:'hit the books',tr:'ders calismak',ex:"I need to hit the books.",meaning:'Study hard'}},{{idiom:'under the weather',tr:'keyifsiz/hasta',ex:"I'm feeling under the weather.",meaning:'Feeling ill'}},{{idiom:'call it a day',tr:'bugunku isi bitirmek',ex:"Let's call it a day.",meaning:'Stop working'}}],
A2:[{{idiom:'cost an arm and a leg',tr:'cok pahali',ex:'That car costs an arm and a leg.',meaning:'Very expensive'}},{{idiom:'let the cat out of the bag',tr:'sirri aciga cikarmak',ex:'She let the cat out of the bag.',meaning:'Reveal a secret'}},{{idiom:'bite off more than you can chew',tr:'basaramayacagi isi ustlenmek',ex:'He bit off more than he could chew.',meaning:'Take on too much'}},{{idiom:'kill two birds with one stone',tr:'bir tasla iki kus vurmak',ex:'We can kill two birds with one stone.',meaning:'Accomplish two things at once'}},{{idiom:'once in a blue moon',tr:'kirk yilda bir',ex:'We eat out once in a blue moon.',meaning:'Very rarely'}}],
B1:[{{idiom:'the ball is in your court',tr:'karar sende',ex:'The ball is in your court now.',meaning:'It is your decision'}},{{idiom:'burn the midnight oil',tr:'gece geç saatlere kadar calismak',ex:'She burned the midnight oil studying.',meaning:'Work late into the night'}},{{idiom:'get cold feet',tr:'son anda korkmak',ex:'He got cold feet before the presentation.',meaning:'Become nervous and hesitant'}},{{idiom:'go the extra mile',tr:'ekstra efor sarf etmek',ex:'She always goes the extra mile.',meaning:'Do more than expected'}},{{idiom:'miss the boat',tr:'firsat kacirmak',ex:'You missed the boat on that deal.',meaning:'Miss an opportunity'}}],
B2:[{{idiom:'beat around the bush',tr:'lafı dolandirmak',ex:"Stop beating around the bush.",meaning:'Avoid saying something directly'}},{{idiom:'cut corners',tr:'kisa yoldan gitmek',ex:"Don't cut corners on safety.",meaning:'Do something the easiest/cheapest way'}},{{idiom:'in the same boat',tr:'ayni durumda olmak',ex:"We're all in the same boat.",meaning:'In the same difficult situation'}},{{idiom:'sit on the fence',tr:'kararsiz kalmak',ex:"Stop sitting on the fence.",meaning:'Not making a decision'}},{{idiom:'the tip of the iceberg',tr:'buzdaginin gorunen kismi',ex:'This is just the tip of the iceberg.',meaning:'A small part of a bigger problem'}}],
C1:[{{idiom:'barking up the wrong tree',tr:'yanlis kapiya basvurmak',ex:"You're barking up the wrong tree.",meaning:'Looking in the wrong place'}},{{idiom:'bite the bullet',tr:'disleri sikmak',ex:'Time to bite the bullet.',meaning:'Endure a painful situation bravely'}},{{idiom:'a double-edged sword',tr:'iki ucu keskin bicak',ex:'Social media is a double-edged sword.',meaning:'Something with both advantages and disadvantages'}},{{idiom:'play devil\\'s advocate',tr:'muhalif gorusu savunmak',ex:'Let me play devil\\'s advocate.',meaning:'Argue the opposing side'}},{{idiom:'the elephant in the room',tr:'gorunmeyen fil',ex:"Let's address the elephant in the room.",meaning:'An obvious problem no one discusses'}}],
C2:[{{idiom:'Hobson\\'s choice',tr:'seceneksiz secenek',ex:'It was Hobson\\'s choice.',meaning:'A choice with only one option'}},{{idiom:'Pyrrhic victory',tr:'zarar veren zafer',ex:'It was a Pyrrhic victory.',meaning:'A win that costs too much'}},{{idiom:'catch-22',tr:'cikmaz durum',ex:"It's a real catch-22.",meaning:'A paradoxical situation with no escape'}},{{idiom:'Sword of Damocles',tr:'Demokles\\'in kilici',ex:'The deadline hangs like the Sword of Damocles.',meaning:'An ever-present threat'}},{{idiom:'Pandora\\'s box',tr:'Pandoranin kutusu',ex:'Opening that topic is a Pandora\\'s box.',meaning:'A source of many unforeseen troubles'}}]
}};

// ===================== READING GLOSSARY =====================
var GLOSSARY={{
A1:{{table:'masa',cat:'kedi',morning:'sabah',school:'okul',breakfast:'kahvalti',bus:'otobus',friend:'arkadas',homework:'odev',evening:'aksam',bed:'yatak',weather:'hava',sunny:'gunesli',rainy:'yagmurlu',garden:'bahce',teacher:'ogretmen',happy:'mutlu',house:'ev',family:'aile',book:'kitap',day:'gun'}},
A2:{{supermarket:'supermarket',yesterday:'dun',bread:'ekmek',favorite:'favori',train:'tren',platform:'peron',comfortable:'konforlu',phone:'telefon',broken:'kirik',trip:'gezi',weekend:'hafta sonu',recipe:'tarif',nervous:'gergin',interview:'mulakat',expensive:'pahali',medicine:'ilac',appointment:'randevu',library:'kutuphane',museum:'muze',ticket:'bilet'}},
B1:{{although:'ragmen',heavily:'siddetle',decided:'karar verdi',inside:'icerde',reviewers:'elestirmenler',conversation:'konusma',native:'yerel',employees:'calisanlar',comfortable:'konforlu',journey:'yolculuk',museum:'muze',entry:'giris',responsibility:'sorumluluk',environment:'cevre',opportunity:'firsat',community:'topluluk',experience:'deneyim',presentation:'sunum',challenge:'zorluk',benefit:'fayda'}},
B2:{{unprecedented:'gorulmemis',revolution:'devrim',simultaneously:'ayni anda',phenomenon:'fenomen',approximately:'yaklasik',consequence:'sonuc',perspective:'bakis acisi',significant:'onemli',controversy:'tartisma',hypothesis:'hipotez',methodology:'yontem',sustainable:'surdurulebilir',paradigm:'paradigma',autonomous:'ozerk',infrastructure:'altyapi',rhetoric:'retorik',empirical:'deneysel',sophisticated:'sofistike',pragmatic:'pragmatik',resilience:'dayaniksizlik'}},
C1:{{juxtaposition:'yan yana koyma',quintessential:'ozunde olan',exacerbate:'kotulestirmek',ubiquitous:'her yerde olan',albeit:'gerci',preclude:'engellemek',notwithstanding:'ragmen',ostensibly:'gozukte/gorunurde',concomitant:'beraber olan',amalgamation:'birlestirme',esoteric:'ezoterik',dichotomy:'ikiye bolunme',superfluous:'gereksiz',ameliorate:'iyilestirmek',idiosyncratic:'kendine ozgu',propensity:'egilim',vernacular:'yerel dil',antithetical:'zit',surreptitious:'gizli',paradigmatic:'ornek teskil eden'}},
C2:{{epistemological:'bilgi kuramsal',ontological:'varolussa',hermeneutic:'yorumsal',teleological:'ereksel',dialectical:'diyalektik',phenomenological:'fenomenolojik',heuristic:'kesfedici',axiological:'deger bilimsel',praxis:'uygulama',aporia:'cikmaz',liminal:'esik',palimpsest:'palimpsest',simulacrum:'simulakr',rhizomatic:'kokkucugu gibi',deterritorialization:'yurtsuslastirma',performativity:'performativite',metanarrative:'ustanlatı',deconstruction:'yapisokum',intersubjectivity:'oznesarasilik',entelechy:'entelekya'}}
}};

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
    opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udd0a '+w.e+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w}});
  }});return qs;
}}
function genLevelQuiz(lv){{
  var cats=WORDS[lv]?WORDS[lv].categories:{{}};var all=[];
  Object.keys(cats).forEach(function(c){{cats[c].forEach(function(w){{all.push(w);}});}});
  all=shuffle(all);var pool=all.slice(0,20);var qs=[];
  pool.forEach(function(w,idx){{
    // Mix question types: MCQ, True/False, Reverse
    var qtype=idx%4;
    if(qtype===0){{
      // True/False: show a pair, is it correct?
      var isTF=Math.random()>0.5;
      var shown=isTF?w.t:all[Math.floor(Math.random()*all.length)].t;
      qs.push({{stem:'\\u2753 "'+w.e+'" = "'+shown+'" — Dogru mu?',opts:['Dogru (True)','Yanlis (False)'],correct:isTF?0:1,word:w,qtype:'tf'}});
    }}else if(qtype===1){{
      // Reverse: Turkish -> English
      var opts2=[w.e];var oth2=all.filter(function(x){{return x.e!==w.e;}});
      oth2=shuffle(oth2);for(var j=0;j<Math.min(3,oth2.length);j++)opts2.push(oth2[j].e);
      opts2=shuffle(opts2);qs.push({{stem:'\\ud83c\\uddf9\\ud83c\\uddf7 '+w.t+' = ?',opts:opts2,correct:opts2.indexOf(w.e),word:w,qtype:'reverse'}});
    }}else{{
      // Standard MCQ: English -> Turkish
      var opts=[w.t];var others=all.filter(function(x){{return x.t!==w.t;}});
      others=shuffle(others);for(var i=0;i<Math.min(3,others.length);i++)opts.push(others[i].t);
      opts=shuffle(opts);qs.push({{stem:'\\ud83d\\udd0a '+w.e+' = ?',opts:opts,correct:opts.indexOf(w.t),word:w,qtype:'mcq'}});
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
  if(!S.flipped){{
    o+='<div class="fcrd" onclick="flipCard()">';
    o+='<div class="fcl">ENGLISH</div>';
    o+='<div class="fcw">'+w.e+' <span class="spk" onclick="event.stopPropagation();speak(\\''+w.e.replace(/'/g,"\\\\'")+'\\')" title="Dinle">\\ud83d\\udd0a</span></div>';
    o+='<div class="fch">Karti cevirmek icin tikla</div></div>';
  }}else{{
    o+='<div class="fcrd" style="border-color:'+LINFO[lv].c+'">';
    o+='<div class="fcl">TURKCE</div>';
    o+='<div class="fcw" style="color:'+LINFO[lv].c+'">'+w.t+'</div>';
    o+='<div class="fce" style="color:var(--txt2);font-size:.9rem;margin-top:6px">'+w.e+'</div></div>';
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
        o+='<div class="grx"><b>'+ex.en+'</b><br><span style="color:#888">'+ex.tr+'</span> ';
        o+='<span class="spk spks" onclick="speak(\\''+ex.en.replace(/'/g,"\\\\'")+'\\')" title="Dinle">\\ud83d\\udd0a</span></div>';
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
  {{s:"The cat is on the table.",q:"Kedi nerede?",opts:["Masanin ustunde","Yerde","Sandalyede","Yatagin altinda"],a:0}},
  {{s:"My name is John and I am a teacher.",q:"John ne is yapiyor?",opts:["Ogretmen","Doktor","Muhendis","Asci"],a:0}},
  {{s:"I wake up at seven o'clock every morning.",q:"Saat kacta kalkiyor?",opts:["7","8","6","9"],a:0}},
  {{s:"She likes apples and oranges.",q:"O ne sever?",opts:["Elma ve portakal","Muz ve cilek","Uzum ve karpuz","Armut ve seftali"],a:0}},
  {{s:"The weather is sunny today.",q:"Hava nasil?",opts:["Gunesli","Yagmurlu","Bulutlu","Karli"],a:0}},
  {{s:"There are three books on the shelf.",q:"Rafta kac kitap var?",opts:["3","2","5","4"],a:0}},
  {{s:"I go to school by bus.",q:"Okula nasil gidiyor?",opts:["Otobusle","Yuruyerek","Arabayla","Bisikletle"],a:0}},
  {{s:"We have dinner at eight in the evening.",q:"Aksam yemegi saat kacta?",opts:["8","7","9","6"],a:0}}
];
LISTEN_SENT['A2']=[
  {{s:"I went to the supermarket yesterday and bought some milk and bread.",q:"Dun nereye gitti?",opts:["Supermarkete","Okula","Hastaneye","Parka"],a:0}},
  {{s:"She is wearing a blue dress because it is her favorite color.",q:"En sevdigi renk ne?",opts:["Mavi","Kirmizi","Yesil","Sari"],a:0}},
  {{s:"The train leaves at half past nine from platform two.",q:"Tren saat kacta kalkiyor?",opts:["9:30","9:00","10:30","8:30"],a:0}},
  {{s:"My brother is taller than me but I am faster.",q:"Kim daha hizli?",opts:["Ben","Erkek kardesim","Ikisi de esit","Belli degil"],a:0}},
  {{s:"We usually have breakfast at a cafe near the office.",q:"Kahvaltiyi nerede yapiyorlar?",opts:["Ofisin yakinindaki kafede","Evde","Restoranda","Parkta"],a:0}},
  {{s:"The movie starts at seven and finishes at nine thirty.",q:"Film ne kadar suruyor?",opts:["2.5 saat","2 saat","3 saat","1.5 saat"],a:0}},
  {{s:"I need to buy a new phone because mine is broken.",q:"Neden yeni telefon almasi gerekiyor?",opts:["Telefonu kirik","Eski model","Kayip","Yavas"],a:0}},
  {{s:"They are planning a trip to Istanbul next weekend.",q:"Nereye gidecekler?",opts:["Istanbul","Ankara","Izmir","Antalya"],a:0}}
];
LISTEN_SENT['B1']=[
  {{s:"Although it was raining heavily, we decided to go for a walk in the park because we had been inside all day.",q:"Neden yuruyuse ciktilar?",opts:["Butun gun icerde kaldilar","Hava guzeldi","Doktor onerdi","Kosuya gideceklerdi"],a:0}},
  {{s:"The restaurant on the corner serves the best Italian food in town, according to most reviewers.",q:"Restoran ne konuda biliniyor?",opts:["En iyi Italyan yemegi","En ucuz fiyatlar","En buyuk porsiyon","En hizli servis"],a:0}},
  {{s:"She has been studying English for three years and can now hold a basic conversation with native speakers.",q:"Kac yildir Ingilizce ogreniyor?",opts:["3","5","2","1"],a:0}},
  {{s:"If you take the second turning on the left, you will see the library right in front of you.",q:"Kutuphaneye nasil gidilir?",opts:["Ikinci soldan donunce karsida","Birinci sagdan donunce","Duz gidince","Ucuncu soldan donunce"],a:0}},
  {{s:"The company announced that they would hire fifty new employees by the end of the year.",q:"Kac yeni calisan ise alinacak?",opts:["50","30","100","25"],a:0}},
  {{s:"I usually prefer to travel by train because it is more comfortable and I can work during the journey.",q:"Neden treni tercih ediyor?",opts:["Daha konforlu ve calisabilir","Daha ucuz","Daha hizli","Daha guvenli"],a:0}},
  {{s:"The museum is open every day except Monday, and entry is free for students with a valid ID.",q:"Ogrenciler icin ucret nedir?",opts:["Ucretsiz","Yarim fiyat","Tam fiyat","Indirimli"],a:0}},
  {{s:"We need to finish this project before Friday because the client is coming for a presentation on Monday.",q:"Sunum ne zaman?",opts:["Pazartesi","Cuma","Sali","Carsamba"],a:0}}
];
LISTEN_SENT['B2']=[
  {{s:"Despite the economic downturn, the startup managed to secure additional funding from venture capitalists who were impressed by their innovative approach to renewable energy.",q:"Startup neden fon alabildi?",opts:["Yenilenebilir enerjideki yenilikci yaklasimi","Dusuk maliyetleri","Buyuk musteri portfoyu","Hukumet destegi"],a:0}},
  {{s:"Research suggests that people who regularly engage in physical exercise tend to have better mental health outcomes and higher levels of productivity at work.",q:"Egzersizin is verimliligi uzerindeki etkisi nedir?",opts:["Daha yuksek verimlilik","Etkisi yok","Azaltir","Belirsiz"],a:0}},
  {{s:"The conference speaker emphasized that artificial intelligence will fundamentally transform the healthcare industry within the next decade.",q:"Konusmaci ne hakkinda konusuyor?",opts:["Yapay zekanin saglik sektorunu donusturmesi","Egitim reformu","Iklim degisikligi","Ekonomik buyume"],a:0}},
  {{s:"Having lived abroad for over ten years, she found it challenging to readjust to the cultural norms of her home country when she finally returned.",q:"Yurtdisinda kac yil yasadi?",opts:["10 yildan fazla","5 yil","3 yil","20 yil"],a:0}},
  {{s:"The documentary highlighted how deforestation in the Amazon rainforest is contributing to climate change at an alarming rate.",q:"Belgeselin konusu ne?",opts:["Amazon ormansizlasmasi ve iklim degisikligi","Deniz kirliligi","Kentlesme","Hayvan turleri"],a:0}},
  {{s:"Experts recommend that children should spend at least one hour outdoors every day to support their physical and cognitive development.",q:"Uzmanlar cocuklar icin ne oneriyor?",opts:["Gunluk en az 1 saat dis mekan","Gunluk 3 saat TV","Haftada 2 saat spor","Gunluk 2 saat okuma"],a:0}}
];
LISTEN_SENT['C1']=[
  {{s:"The implications of quantum computing for cybersecurity are profound, as current encryption methods may become obsolete once quantum processors achieve sufficient computational power to break them.",q:"Kuantum bilgisayarlarin siber guvenlik icin ana tehdidi nedir?",opts:["Mevcut sifreleme yontemlerini kirabilir","Cok pahali","Enerji tuketiyor","Yavas calisir"],a:0}},
  {{s:"While the government's fiscal policy has succeeded in reducing the budget deficit, critics argue that it has disproportionately affected lower-income households through regressive taxation.",q:"Elestirmenler ne savunuyor?",opts:["Dusuk gelirli haneler orantisiz etkilendi","Politika basarili","Butce acigi artti","Vergiler azaldi"],a:0}},
  {{s:"The philosophical debate surrounding consciousness and free will has been reinvigorated by recent advances in neuroscience, which suggest that our decisions may be predetermined by neural activity.",q:"Norolojik bulgular ne one suruyor?",opts:["Kararlarimiz noral aktivite tarafindan onceden belirlenebilir","Ozgur irade kesin","Bilinc olculemez","Beyin aktivitesi rastgele"],a:0}},
  {{s:"In an increasingly interconnected world, the ability to navigate cross-cultural communication effectively has become an indispensable skill for professionals working in multinational organizations.",q:"Cok uluslu sirketlerde hangi beceri vazgecilmez?",opts:["Kulturler arasi iletisim","Teknik bilgi","Finansal analiz","Proje yonetimi"],a:0}},
  {{s:"The archaeological expedition uncovered artifacts dating back to the third millennium BCE, providing unprecedented insights into the social hierarchies and trading networks of ancient Mesopotamian civilizations.",q:"Buluntular hangi doneme ait?",opts:["MO ucuncu binyil","MO birinci binyil","MS ikinci yuzyil","MO besinci binyil"],a:0}},
  {{s:"Contemporary literary criticism has moved beyond purely textual analysis to incorporate sociopolitical contexts, examining how power structures and ideological frameworks shape narrative construction.",q:"Cagdas edebi elestiri neyi inceliyor?",opts:["Guc yapilari ve ideolojik cercevelerin anlatiya etkisi","Sadece metin analizi","Yazar biyografisi","Okuyucu yorumlari"],a:0}}
];
LISTEN_SENT['C2']=[
  {{s:"The epistemological ramifications of post-structuralist theory challenge the very notion of objective truth, positing instead that knowledge is invariably mediated through linguistic and cultural constructs that resist definitive interpretation.",q:"Post-yapisalci teori neyi sorguluyor?",opts:["Nesnel gerceklik kavramini","Bilimsel yontemi","Matematiksel kesinligi","Tarihsel kaynaklari"],a:0}},
  {{s:"Notwithstanding the ostensible success of monetary easing policies in stimulating short-term growth, the long-term consequences, including asset bubbles and wealth inequality, may prove to be far more deleterious than the initial recession they were designed to mitigate.",q:"Parasal genislemenin uzun vadeli riski nedir?",opts:["Varlik balonlari ve servet esitsizligi","Enflasyonun azalmasi","Issizligin artmasi","Ihracatin dusmesi"],a:0}},
  {{s:"The synthesis of disparate philosophical traditions, from Eastern contemplative practices to Western analytical frameworks, offers a more holistic understanding of human consciousness than any single paradigm can provide.",q:"Butunsel bilinc anlayisi nasil elde edilir?",opts:["Farkli felsefi geleneklerin sentezi ile","Tek bir paradigma ile","Sadece Bati analitik cerceve ile","Sadece Dogu pratikleri ile"],a:0}},
  {{s:"The geopolitical reconfiguration following the dissolution of established alliances has engendered a multipolar world order characterized by shifting allegiances and the emergence of non-state actors as significant players in international relations.",q:"Ittifaklarin cozulmesi neye yol acti?",opts:["Cok kutuplu dunya duzeni","Tek kutuplu dunya","Izolasyonizm","Bolgesel birlik"],a:0}},
  {{s:"The interplay between epigenetic modifications and environmental stimuli has revolutionized our understanding of heredity, demonstrating that gene expression can be altered by experiential factors without changes to the underlying DNA sequence.",q:"Epigenetik ne gosteriyor?",opts:["Gen ifadesi DNA degismeden cevre ile degisebilir","DNA mutasyonu gereklidir","Kalitim sadece genetiktir","Cevre etkisi yoktur"],a:0}}
];

// Dialogue data per level
var LISTEN_DLG={{}};
LISTEN_DLG['A1']=[
  {{title:"Restoranda",dlg:[{{sp:"A",t:"Hello! Can I have a menu, please?"}},{{sp:"B",t:"Of course! Here you are."}},{{sp:"A",t:"I would like a pizza and a glass of water."}},{{sp:"B",t:"That will be ten dollars."}}],q:"Musteri ne siparis etti?",opts:["Pizza ve su","Hamburger ve kola","Salata ve cay","Makarna ve meyve suyu"],a:0}},
  {{title:"Alisveriste",dlg:[{{sp:"A",t:"How much is this T-shirt?"}},{{sp:"B",t:"It is fifteen pounds."}},{{sp:"A",t:"Do you have it in blue?"}},{{sp:"B",t:"Yes, here is the blue one."}}],q:"Tisortun fiyati ne kadar?",opts:["15 pound","10 pound","20 pound","5 pound"],a:0}},
  {{title:"Yol Sorma",dlg:[{{sp:"A",t:"Excuse me, where is the hospital?"}},{{sp:"B",t:"Go straight and turn right at the traffic light."}},{{sp:"A",t:"Is it far from here?"}},{{sp:"B",t:"No, it is about five minutes."}}],q:"Hastane ne kadar uzakta?",opts:["Yaklasik 5 dakika","10 dakika","15 dakika","Cok uzak"],a:0}},
  {{title:"Tanisma",dlg:[{{sp:"A",t:"Hi, my name is Sarah. What is your name?"}},{{sp:"B",t:"I am Tom. Nice to meet you."}},{{sp:"A",t:"Where are you from, Tom?"}},{{sp:"B",t:"I am from Canada."}}],q:"Tom nereli?",opts:["Kanada","Amerika","Ingiltere","Avustralya"],a:0}}
];
LISTEN_DLG['A2']=[
  {{title:"Doktor Randevusu",dlg:[{{sp:"A",t:"Good morning. I have an appointment at ten o'clock."}},{{sp:"B",t:"What is your name, please?"}},{{sp:"A",t:"Maria Lopez."}},{{sp:"B",t:"Yes, Dr. Smith will see you in five minutes. Please take a seat."}}],q:"Randevu saat kacta?",opts:["10:00","9:00","11:00","10:30"],a:0}},
  {{title:"Otel Rezervasyonu",dlg:[{{sp:"A",t:"I would like to book a room for two nights."}},{{sp:"B",t:"Single or double?"}},{{sp:"A",t:"Double, please. With a sea view if possible."}},{{sp:"B",t:"That will be eighty euros per night."}}],q:"Gecelik ucret ne kadar?",opts:["80 euro","60 euro","100 euro","50 euro"],a:0}},
  {{title:"Havalimani",dlg:[{{sp:"A",t:"Can I see your passport and boarding pass, please?"}},{{sp:"B",t:"Here you go. Gate B12, right?"}},{{sp:"A",t:"Actually, the gate has changed to C5."}},{{sp:"B",t:"Thank you for letting me know!"}}],q:"Yeni kapi numarasi ne?",opts:["C5","B12","A3","D7"],a:0}},
  {{title:"Is Gorusmesi",dlg:[{{sp:"A",t:"Why do you want to work for our company?"}},{{sp:"B",t:"I admire your approach to innovation and teamwork."}},{{sp:"A",t:"What are your strongest skills?"}},{{sp:"B",t:"I am good at problem-solving and communication."}}],q:"Adayin en guclu becerileri ne?",opts:["Problem cozme ve iletisim","Matematik ve fizik","Tasarim ve sanat","Satis ve pazarlama"],a:0}}
];
LISTEN_DLG['B1']=[
  {{title:"Toplanti",dlg:[{{sp:"A",t:"Let us start with the sales report. Revenue increased by fifteen percent this quarter."}},{{sp:"B",t:"That is great news. What about the new product launch?"}},{{sp:"A",t:"We are planning to launch it in March. The marketing team is preparing the campaign now."}},{{sp:"B",t:"Excellent. Let us schedule a follow-up meeting next week."}}],q:"Gelir ne kadar artti?",opts:["Yuzde 15","Yuzde 10","Yuzde 20","Yuzde 5"],a:0}},
  {{title:"Universite Danismanligi",dlg:[{{sp:"A",t:"I am thinking about changing my major from history to computer science."}},{{sp:"B",t:"That is a big decision. Have you taken any programming courses?"}},{{sp:"A",t:"Yes, I completed an introductory Python course last semester and really enjoyed it."}},{{sp:"B",t:"I would recommend taking one more advanced course before making the switch."}}],q:"Danismanin onerisi ne?",opts:["Gecmeden once bir ileri kurs daha almasi","Hemen gecmesi","Tarihte kalmasi","Staj yapmasi"],a:0}},
  {{title:"Seyahat Planlama",dlg:[{{sp:"A",t:"I am planning a two-week trip to Japan. Any suggestions?"}},{{sp:"B",t:"You should definitely visit Kyoto for the temples and Tokyo for the technology district."}},{{sp:"A",t:"What about transportation? Is the rail pass worth it?"}},{{sp:"B",t:"Absolutely. The Japan Rail Pass saves you a lot of money if you are traveling between cities."}}],q:"Japonya gezisi icin ne onerildi?",opts:["Kyoto tapinaklar, Tokyo teknoloji bolgesi","Sadece Tokyo","Osaka ve Hiroshima","Sadece Kyoto"],a:0}},
  {{title:"Saglik Kontrolu",dlg:[{{sp:"A",t:"Your blood pressure is slightly higher than normal. Are you under a lot of stress lately?"}},{{sp:"B",t:"Yes, I have been working overtime for the past month."}},{{sp:"A",t:"I recommend reducing your salt intake and trying to exercise at least three times a week."}},{{sp:"B",t:"Should I come back for another check-up?"}},{{sp:"A",t:"Yes, let us schedule one for next month."}}],q:"Doktor ne onerdi?",opts:["Tuz azaltma ve haftada 3 kez egzersiz","Ilac baslama","Ameliyat","Diyet programi"],a:0}}
];
LISTEN_DLG['B2']=[
  {{title:"Is Muzakeresi",dlg:[{{sp:"A",t:"We are prepared to offer a ten percent discount on bulk orders over five hundred units."}},{{sp:"B",t:"That is a reasonable starting point, but our competitors are offering fifteen percent."}},{{sp:"A",t:"We can match twelve percent if you commit to a two-year contract."}},{{sp:"B",t:"Let me discuss this with my team and get back to you by Friday."}}],q:"Son indirim teklifi ne?",opts:["Yuzde 12","Yuzde 10","Yuzde 15","Yuzde 8"],a:0}},
  {{title:"Cevresel Tartisma",dlg:[{{sp:"A",t:"The city council is considering banning single-use plastics by the end of next year."}},{{sp:"B",t:"While I support the initiative, small businesses need time to find affordable alternatives."}},{{sp:"A",t:"Perhaps a phased approach would work, starting with large corporations first?"}},{{sp:"B",t:"That sounds more practical. A gradual transition would minimize the economic impact."}}],q:"Onerilen yaklasim ne?",opts:["Once buyuk sirketlerden baslayan asamali gecis","Aninda yasak","5 yillik gecis","Gonullu katilim"],a:0}},
  {{title:"Akademik Sunum",dlg:[{{sp:"A",t:"My research examines the correlation between social media usage and adolescent mental health."}},{{sp:"B",t:"What methodology did you use?"}},{{sp:"A",t:"A longitudinal study following twelve hundred participants over three years."}},{{sp:"B",t:"That is quite comprehensive. Did you control for socioeconomic variables?"}}],q:"Arastirma kac katilimciyi takip etti?",opts:["1200","500","2000","800"],a:0}}
];
LISTEN_DLG['C1']=[
  {{title:"Felsefi Tartisma",dlg:[{{sp:"A",t:"Do you think moral relativism undermines the possibility of universal human rights?"}},{{sp:"B",t:"Not necessarily. One can acknowledge cultural variation while still maintaining that certain rights are non-negotiable."}},{{sp:"A",t:"But how do you determine which rights are universal without imposing a particular cultural framework?"}},{{sp:"B",t:"Through cross-cultural dialogue and identifying overlapping consensus among diverse traditions."}}],q:"Evrensel haklari belirleme yontemi ne?",opts:["Kulturler arasi diyalog ve ortak uzlasi","Tek bir kulturun dayatmasi","BM kararlari","Felsefi teoriler"],a:0}},
  {{title:"Ekonomik Analiz",dlg:[{{sp:"A",t:"The latest data suggests that automation will displace approximately thirty percent of current jobs within two decades."}},{{sp:"B",t:"However, historical precedent shows that technological revolutions ultimately create more jobs than they eliminate."}},{{sp:"A",t:"The concern is that the transition period could exacerbate inequality if retraining programs are inadequate."}},{{sp:"B",t:"Agreed. Governments need to invest heavily in education and social safety nets."}}],q:"Gecis donemindeki endise ne?",opts:["Yeniden egitim yetersizse esitsizlik artabilir","Is sayisi azalir","Teknoloji durur","Ekonomi coker"],a:0}},
  {{title:"Bilimsel Konferans",dlg:[{{sp:"A",t:"Our findings indicate that CRISPR gene editing could potentially eliminate certain hereditary diseases within a generation."}},{{sp:"B",t:"The ethical implications are staggering. Who decides which traits are diseases and which are natural variation?"}},{{sp:"A",t:"That is precisely why we need an interdisciplinary ethics committee overseeing all clinical applications."}},{{sp:"B",t:"I agree, but we also need public engagement to ensure democratic accountability."}}],q:"CRISPR icin ne oneriliyor?",opts:["Disiplinler arasi etik komite ve kamusal katilim","Sinirsiz kullanim","Sadece ozel sektor denetimi","Yasaklama"],a:0}}
];
LISTEN_DLG['C2']=[
  {{title:"Epistomolojik Degerlendirme",dlg:[{{sp:"A",t:"The hermeneutic circle presents a fundamental challenge to objectivity in textual interpretation."}},{{sp:"B",t:"Indeed, but Gadamer argued that our prejudices are not merely obstacles but constitutive elements of understanding."}},{{sp:"A",t:"Does that not risk legitimizing ideological bias under the guise of interpretive tradition?"}},{{sp:"B",t:"Only if we fail to engage in what Habermas called communicative rationality, subjecting our presuppositions to critical scrutiny."}}],q:"Habermas'in onerisi ne?",opts:["Iletisimsel akilcilik ile on yargilarin elestirel incelenmesi","On yargilarin tamamen kaldirilmasi","Geleneksel yorumun korunmasi","Metinsel analiz"],a:0}},
  {{title:"Jeopolitik Forum",dlg:[{{sp:"A",t:"The Westphalian model of state sovereignty is increasingly inadequate for addressing transnational challenges like climate change and cyberwarfare."}},{{sp:"B",t:"Yet any supranational governance framework faces legitimacy deficits and the free-rider problem."}},{{sp:"A",t:"Perhaps the solution lies in polycentric governance, multiple overlapping jurisdictions with issue-specific mandates."}},{{sp:"B",t:"Ostrom's work on commons governance supports this, but scaling it to global issues remains theoretically and practically contentious."}}],q:"Onerilen yonetisim modeli ne?",opts:["Cok merkezli yonetisim","Tek dunya hukumeti","Ulusal egemenligin guclenmesi","BM reformu"],a:0}},
  {{title:"Norolojik Arastirma",dlg:[{{sp:"A",t:"Our neuroimaging data reveals that consciousness correlates with integrated information processing across distributed cortical networks."}},{{sp:"B",t:"This aligns with Tononi's Integrated Information Theory but raises questions about artificial systems meeting the phi threshold."}},{{sp:"A",t:"If phi is merely a necessary condition rather than sufficient, we need additional criteria to distinguish phenomenal from functional consciousness."}},{{sp:"B",t:"Perhaps the hard problem of consciousness will require a paradigmatic shift in our ontological assumptions."}}],q:"Fenomenal ve fonksiyonel bilinci ayirt etmek icin ne gerekiyor?",opts:["Ek kriterler","Sadece phi esigi","Daha fazla beyin goruntulemesi","Yapay zeka testleri"],a:0}}
];

// Fill-in-the-blank listening data
var LISTEN_FILL={{}};
LISTEN_FILL['A1']=[
  {{s:"I have a ___ dog at home.",w:"big",opts:["big","small","red","fast"]}},
  {{s:"She goes to ___ every day.",w:"school",opts:["school","park","home","bed"]}},
  {{s:"We eat ___ for breakfast.",w:"eggs",opts:["eggs","dinner","lunch","shoes"]}},
  {{s:"The sky is ___ today.",w:"blue",opts:["blue","green","brown","pink"]}},
  {{s:"He drinks ___ in the morning.",w:"coffee",opts:["coffee","soup","ice","sand"]}},
  {{s:"They play ___ after school.",w:"football",opts:["football","piano","chess","cards"]}}
];
LISTEN_FILL['A2']=[
  {{s:"I have been ___ for the bus for twenty minutes.",w:"waiting",opts:["waiting","running","sitting","eating"]}},
  {{s:"She ___ to the gym three times a week.",w:"goes",opts:["goes","runs","walks","drives"]}},
  {{s:"We should ___ a taxi because it is raining.",w:"take",opts:["take","buy","sell","make"]}},
  {{s:"The museum was ___ than I expected.",w:"bigger",opts:["bigger","smaller","older","newer"]}},
  {{s:"He ___ his keys at the office yesterday.",w:"forgot",opts:["forgot","found","lost","broke"]}},
  {{s:"They are ___ a new house near the beach.",w:"building",opts:["building","buying","selling","painting"]}}
];
LISTEN_FILL['B1']=[
  {{s:"If I ___ more time, I would learn to play the guitar.",w:"had",opts:["had","have","will","would"]}},
  {{s:"The project was ___ completed ahead of schedule.",w:"successfully",opts:["successfully","slowly","badly","never"]}},
  {{s:"She has been ___ in London since she graduated from university.",w:"living",opts:["living","working","studying","traveling"]}},
  {{s:"Despite the ___, they managed to finish the marathon.",w:"difficulties",opts:["difficulties","weather","food","traffic"]}},
  {{s:"The company ___ to expand its operations to Asia next year.",w:"plans",opts:["plans","hopes","tries","wants"]}},
  {{s:"I would ___ appreciate it if you could help me with this report.",w:"really",opts:["really","never","hardly","barely"]}}
];
LISTEN_FILL['B2']=[
  {{s:"The government's decision to raise interest rates was met with widespread ___.",w:"criticism",opts:["criticism","approval","silence","confusion"]}},
  {{s:"Had she ___ about the meeting, she would have prepared her presentation.",w:"known",opts:["known","told","heard","said"]}},
  {{s:"The ___ between technology and privacy continues to be a contentious issue.",w:"tension",opts:["tension","balance","gap","bridge"]}},
  {{s:"Researchers have ___ that regular meditation can reduce cortisol levels significantly.",w:"demonstrated",opts:["demonstrated","suggested","hoped","wished"]}},
  {{s:"The novel offers a ___ critique of contemporary consumer culture.",w:"compelling",opts:["compelling","boring","simple","brief"]}},
  {{s:"She spoke with such ___ that the entire audience was captivated.",w:"eloquence",opts:["eloquence","speed","volume","anger"]}}
];
LISTEN_FILL['C1']=[
  {{s:"The ___ of the new policy on marginalized communities has been largely overlooked.",w:"impact",opts:["impact","cost","design","origin"]}},
  {{s:"His argument, though ___ constructed, failed to account for several key variables.",w:"meticulously",opts:["meticulously","poorly","hastily","randomly"]}},
  {{s:"The phenomenon can be ___ attributed to a combination of socioeconomic and environmental factors.",w:"largely",opts:["largely","never","barely","solely"]}},
  {{s:"The committee reached a ___ decision after twelve hours of deliberation.",w:"unanimous",opts:["unanimous","quick","partial","divided"]}},
  {{s:"___ advances in biotechnology raise profound ethical questions about human enhancement.",w:"Recent",opts:["Recent","Ancient","Minor","Theoretical"]}}
];
LISTEN_FILL['C2']=[
  {{s:"The ___ nature of consciousness remains one of philosophy's most intractable problems.",w:"enigmatic",opts:["enigmatic","simple","physical","digital"]}},
  {{s:"His ___ analysis of the geopolitical situation proved remarkably prescient.",w:"nuanced",opts:["nuanced","brief","flawed","casual"]}},
  {{s:"The theory's ___ lies in its ability to reconcile seemingly contradictory empirical findings.",w:"elegance",opts:["elegance","weakness","complexity","origin"]}},
  {{s:"The ___ implications of artificial general intelligence demand immediate interdisciplinary discourse.",w:"existential",opts:["existential","minor","financial","technical"]}},
  {{s:"Her prose style is characterized by a ___ interweaving of personal narrative and philosophical reflection.",w:"seamless",opts:["seamless","clumsy","rapid","minimal"]}}
];

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
  o+='<input class="din" id="dict-input" placeholder="Ingilizce kelimeyi yaz..." style="text-align:center;max-width:300px;margin:0 auto;display:block" onkeypress="if(event.key===\\'Enter\\')checkDict()">';
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
window.speakEN=speak;

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
  _recognition.lang='en-US';_recognition.continuous=false;_recognition.interimResults=false;
  _recognition.maxAlternatives=3;
}}
if(_speechSupported)initSpeechRecognition();

var SPEAK_PROMPTS={{
  A1:['Hello, my name is...','I like to eat...','My favorite color is...','I live in...','Today the weather is...'],
  A2:['Tell me about your daily routine.','Describe your family.','What did you do last weekend?','What is your favorite hobby?','Describe the weather today.'],
  B1:['Describe your ideal vacation destination.','What are the advantages of learning English?','Talk about a book or movie you enjoyed recently.','Explain the importance of healthy eating.','Describe your hometown.'],
  B2:['Discuss the impact of social media on society.','Compare city life and country life.','Describe a challenging situation you overcame.','Talk about the role of technology in education.','Discuss environmental problems and solutions.'],
  C1:['Analyze the ethical implications of artificial intelligence.','Discuss the relationship between economic growth and environmental sustainability.','Evaluate the effectiveness of international organizations.','Analyze how globalization affects cultural identity.','Discuss the future of work in an automated world.'],
  C2:['Critique the philosophical foundations of human rights.','Analyze the epistemological challenges of post-truth politics.','Discuss the implications of quantum computing for cryptography.','Evaluate the merits of different theories of consciousness.','Analyze the relationship between language and thought.']
}};

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


_FLIPBOOK_STORIES = {
    "preschool": [
        {
            "title": "Colors All Around",
            "icon": "\U0001f308",
            "color": "#e91e63",
            "pages": [
                {"img": "\U0001f534", "en": "This is red. The apple is red.", "tr": "Bu k\u0131rm\u0131z\u0131. Elma k\u0131rm\u0131z\u0131d\u0131r."},
                {"img": "\U0001f7e0", "en": "This is orange. The cat is orange.", "tr": "Bu turuncu. Kedi turuncudur."},
                {"img": "\U0001f7e1", "en": "This is yellow. The sun is yellow.", "tr": "Bu sar\u0131. G\u00fcne\u015f sar\u0131d\u0131r."},
                {"img": "\U0001f7e2", "en": "This is green. The tree is green.", "tr": "Bu ye\u015fil. A\u011fa\u00e7 ye\u015fildir."},
                {"img": "\U0001f535", "en": "This is blue. The sky is blue.", "tr": "Bu mavi. G\u00f6ky\u00fcz\u00fc mavidir."},
                {"img": "\U0001f7e3", "en": "This is purple. The flower is purple.", "tr": "Bu mor. \u00c7i\u00e7ek mordur."},
                {"img": "\U0001f308", "en": "Red, orange, yellow, green, blue, purple. I love all the colors! A rainbow has all the colors!", "tr": "K\u0131rm\u0131z\u0131, turuncu, sar\u0131, ye\u015fil, mavi, mor. T\u00fcm renkleri seviyorum! G\u00f6kku\u015fa\u011f\u0131nda t\u00fcm renkler var!"},
            ],
        },
        {
            "title": "My Family",
            "icon": "\U0001f46a",
            "color": "#2196f3",
            "pages": [
                {"img": "\U0001f468", "en": "This is my father. Hello, father!", "tr": "Bu benim babam. Merhaba, baba!"},
                {"img": "\U0001f469", "en": "This is my mother. Hello, mother!", "tr": "Bu benim annem. Merhaba, anne!"},
                {"img": "\U0001f466", "en": "This is my brother. He is five years old.", "tr": "Bu benim erkek karde\u015fim. O be\u015f ya\u015f\u0131nda."},
                {"img": "\U0001f467", "en": "This is my sister. She is three years old.", "tr": "Bu benim k\u0131z karde\u015fim. O \u00fc\u00e7 ya\u015f\u0131nda."},
                {"img": "\U0001f475", "en": "This is my grandmother. She makes cookies.", "tr": "Bu benim b\u00fcy\u00fcannem. O kurabiye yapar."},
                {"img": "\U0001f474", "en": "This is my grandfather. He reads stories.", "tr": "Bu benim b\u00fcy\u00fckbabam. O hikayeler okur."},
                {"img": "\U0001f436", "en": "This is my dog. His name is Buddy. I love my family!", "tr": "Bu benim k\u00f6pe\u011fim. Ad\u0131 Buddy. Ailemi seviyorum!"},
            ],
        },
        {
            "title": "Animals on the Farm",
            "icon": "\U0001f404",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f404", "en": "The cow says moo. The cow is big.", "tr": "Inek m\u00f6\u00f6 der. Inek b\u00fcy\u00fckt\u00fcr."},
                {"img": "\U0001f414", "en": "The chicken says cluck. The chicken is small.", "tr": "Tavuk gidak gidak der. Tavuk k\u00fc\u00e7\u00fckt\u00fcr."},
                {"img": "\U0001f434", "en": "The horse says neigh. The horse is fast.", "tr": "At kineee der. At h\u0131zl\u0131d\u0131r."},
                {"img": "\U0001f437", "en": "The pig says oink. The pig is pink.", "tr": "Domuz oink der. Domuz pembedir."},
                {"img": "\U0001f411", "en": "The sheep says baa. The sheep is fluffy.", "tr": "Koyun mee der. Koyun kabar\u0131kt\u0131r."},
                {"img": "\U0001f436", "en": "The dog says woof. The dog is friendly.", "tr": "K\u00f6pek hav hav der. K\u00f6pek dost canlisidir."},
                {"img": "\U0001f408", "en": "The cat says meow. The cat is soft.", "tr": "Kedi miyav der. Kedi yumu\u015fakt\u0131r."},
                {"img": "\U0001f3e1", "en": "I love the farm! All the animals are my friends.", "tr": "\u00c7iftli\u011fi seviyorum! T\u00fcm hayvanlar benim arkada\u015f\u0131m."},
            ],
        },
    ],
    "1": [
        {
            "title": "My First Day at School",
            "icon": "\U0001f3eb",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f3eb", "en": "Today is my first day at school. I am happy and a little scared. My mother says, 'Don't worry. School is fun!'", "tr": "Bug\u00fcn okulda ilk g\u00fcn\u00fcm. Mutluyum ve biraz korku duyuyorum. Annem 'Endiselenme. Okul eglencelidir!' diyor."},
                {"img": "\U0001f392", "en": "I have a new bag. It is blue. I have a pencil, a book, and an eraser in my bag.", "tr": "Yeni bir \u00e7antam var. Mavi. \u00c7antamda bir kalem, bir kitap ve bir silgi var."},
                {"img": "\U0001f469\u200d\U0001f3eb", "en": "My teacher is very nice. Her name is Miss Elif. She says, 'Good morning, children! Welcome to school!'", "tr": "\u00d6gretmenim \u00e7ok iyi. Ad\u0131 Elif \u00d6gretmen. 'G\u00fcnaydin \u00e7ocuklar! Okula ho\u015f geldiniz!' diyor."},
                {"img": "\U0001f466\U0001f467", "en": "I sit next to a boy. His name is Ali. He says, 'Hello! What is your name?' I say, 'My name is Ece. Nice to meet you!'", "tr": "Bir \u00e7ocugun yan\u0131na oturuyorum. Adi Ali. 'Merhaba! Adin ne?' diyor. 'Adim Ece. Tan\u0131\u015ft\u0131g\u0131m\u0131za memnunum!' diyorum."},
                {"img": "\U0001f3b5", "en": "We sing the ABC song together. A, B, C, D, E, F, G... It is a fun song! I like singing.", "tr": "Birlikte ABC \u015fark\u0131s\u0131 s\u00f6yl\u00fcy\u00f6ruz. A, B, C, D, E, F, G... Eglenceli bir \u015fark\u0131! \u015eark\u0131 s\u00f6ylemeyi seviyorum."},
                {"img": "\U0001f34e", "en": "At lunch time, I eat my sandwich and drink my juice. Ali shares his apple with me. He is a good friend.", "tr": "\u00d6gle yemeginde sandvi\u00e7imi yiyorum ve meyve suyumu i\u00e7iyorum. Ali elmas\u0131n\u0131 benimle payla\u015f\u0131yor. Iyi bir arkada\u015f."},
                {"img": "\U0001f3c3", "en": "After lunch, we play in the garden. We run, jump, and laugh. School is really fun!", "tr": "\u00d6gle yemeginden sonra bah\u00e7ede oynuyoruz. Ko\u015fuyoruz, z\u0131pl\u0131yoruz ve g\u00fcl\u00fcy\u00f6ruz. Okul ger\u00e7ekten eglenceli!"},
                {"img": "\U0001f4ab", "en": "When I go home, my mother asks, 'How was school?' I say, 'It was great! I have a new friend. I love school!'", "tr": "Eve gittigimde annem 'Okul nas\u0131ld\u0131?' diye soruyor. 'Harikayd\u0131! Yeni bir arkada\u015f\u0131m var. Okulu seviyorum!' diyorum."},
            ],
        },
        {
            "title": "My Pet Cat",
            "icon": "\U0001f431",
            "color": "#ff9800",
            "pages": [
                {"img": "\U0001f431", "en": "I have a cat. Her name is Pamuk. She is white and very soft.", "tr": "Bir kedim var. Ad\u0131 Pamuk. Beyaz ve \u00e7ok yumu\u015fak."},
                {"img": "\U0001f3e0", "en": "Pamuk lives in my house. She sleeps on my bed. She is a lazy cat!", "tr": "Pamuk benim evimde ya\u015f\u0131yor. Yatagimda uyuyor. Tembel bir kedi!"},
                {"img": "\U0001f95b", "en": "Every morning, I give Pamuk milk and food. She says, 'Meow!' That means 'Thank you!'", "tr": "Her sabah Pamuk'a s\u00fct ve yemek veriyorum. 'Miyav!' diyor. Bu 'Te\u015fekk\u00fcrler!' demek!"},
                {"img": "\U0001f9f6", "en": "Pamuk likes to play with a ball of yarn. She runs and jumps. She is very funny.", "tr": "Pamuk y\u00fcn yumagiyla oynamayi seviyor. Ko\u015fuyor ve z\u0131pliyor. \u00c7ok komik."},
                {"img": "\U0001f319", "en": "At night, Pamuk sits on the window and looks at the moon. I think she counts the stars.", "tr": "Gece Pamuk pencerede oturup aya bak\u0131yor. San\u0131r\u0131m y\u0131ld\u0131zlar\u0131 say\u0131yor."},
                {"img": "\u2764\ufe0f", "en": "I love Pamuk very much. She is not just a cat. She is my best friend!", "tr": "Pamuk'u \u00e7ok seviyorum. O sadece bir kedi degil. En iyi arkada\u015f\u0131m!"},
            ],
        },
        {
            "title": "Counting Fun",
            "icon": "\U0001f522",
            "color": "#9c27b0",
            "pages": [
                {"img": "\u261d\ufe0f", "en": "One apple. I have one red apple.", "tr": "Bir elma. Bir k\u0131rm\u0131z\u0131 elmam var."},
                {"img": "\u270c\ufe0f", "en": "Two eyes. I have two big eyes.", "tr": "Iki g\u00f6z. Iki b\u00fcy\u00fck g\u00f6z\u00fcm var."},
                {"img": "\U0001f44c", "en": "Three books. I have three books on my desk.", "tr": "\u00dc\u00e7 kitap. Masamda \u00fc\u00e7 kitap var."},
                {"img": "\U0001f596", "en": "Four cats. There are four cats in the garden.", "tr": "D\u00f6rt kedi. Bah\u00e7ede d\u00f6rt kedi var."},
                {"img": "\U0001f590\ufe0f", "en": "Five fingers. I have five fingers on my hand.", "tr": "Be\u015f parmak. Elimde be\u015f parmag\u0131m var."},
                {"img": "\U0001f522", "en": "One, two, three, four, five! I can count to five! Can you count to ten?", "tr": "Bir, iki, \u00fc\u00e7, d\u00f6rt, be\u015f! Be\u015fe kadar sayabiliyorum! Sen ona kadar sayabilir misin?"},
            ],
        },
    ],
    "2": [
        {
            "title": "A Trip to the Zoo",
            "icon": "\U0001f981",
            "color": "#ff9800",
            "pages": [
                {"img": "\U0001f68c", "en": "Today our class is going to the zoo. We take a big yellow bus. My friends and I are very excited.", "tr": "Bug\u00fcn sinifimiz hayvanat bah\u00e7esine gidiyor. B\u00fcy\u00fck sar\u0131 bir otob\u00fcse biniyoruz."},
                {"img": "\U0001f981", "en": "First, we see the lions. The lion is very big and strong. It has a beautiful mane. It roars loudly!", "tr": "\u00d6nce aslanlar\u0131 g\u00f6r\u00fcy\u00f6ruz. Aslan \u00e7ok b\u00fcy\u00fck ve g\u00fc\u00e7l\u00fc. G\u00fczel bir yelesi var."},
                {"img": "\U0001f418", "en": "Then we see the elephants. The elephant is the biggest animal in the zoo. It has a long trunk and big ears.", "tr": "Sonra filleri g\u00f6r\u00fcy\u00f6ruz. Fil hayvanat bah\u00e7esinin en b\u00fcy\u00fck hayvan\u0131."},
                {"img": "\U0001f412", "en": "The monkeys are very funny. They jump from tree to tree. One monkey eats a banana. Another monkey waves at us!", "tr": "Maymunlar \u00e7ok komik. Aga\u00e7tan agaca z\u0131pl\u0131yorlar. Bir maymun muz yiyor."},
                {"img": "\U0001f427", "en": "We visit the penguins. They are black and white. They walk very funny \u2014 left, right, left, right. They swim fast in the water.", "tr": "Penguenleri ziyaret ediyoruz. Siyah ve beyazlar. \u00c7ok komik y\u00fcr\u00fcy\u00f6rlar."},
                {"img": "\U0001f992", "en": "The giraffe is the tallest animal. It has a very long neck. It eats leaves from the top of the tree.", "tr": "Z\u00fcrafa en uzun hayvan. \u00c7ok uzun bir boynu var. Agacin tepesinden yaprak yiyor."},
                {"img": "\U0001f368", "en": "After the zoo, we eat ice cream. I have chocolate ice cream. My friend has strawberry. What a wonderful day!", "tr": "Hayvanat bah\u00e7esinden sonra dondurma yiyoruz. Bende \u00e7ikolatali, arkada\u015fimda \u00e7ilekli. Ne harika bir g\u00fcn!"},
            ],
        },
        {
            "title": "The Four Seasons",
            "icon": "\U0001f338",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f338", "en": "Spring is here! The flowers are blooming. The birds are singing. The weather is warm. I like spring!", "tr": "Ilkbahar geldi! \u00c7i\u00e7ekler a\u00e7\u0131yor. Kuslar \u015fark\u0131 s\u00f6yl\u00fcyor. Hava \u0131l\u0131k."},
                {"img": "\u2600\ufe0f", "en": "Summer is hot! I swim in the sea. I eat ice cream. I play with my friends. Summer is my favourite season.", "tr": "Yaz s\u0131cak! Denizde y\u00fcz\u00fcyorum. Dondurma yiyorum. Arkada\u015flar\u0131mla oynuyorum."},
                {"img": "\U0001f342", "en": "Autumn is cool. The leaves are red, yellow, and orange. They fall from the trees. I like walking on the leaves.", "tr": "Sonbahar serin. Yapraklar k\u0131rm\u0131z\u0131, sar\u0131 ve turuncu. Agaclardan d\u00fc\u015f\u00fcyorlar."},
                {"img": "\u2744\ufe0f", "en": "Winter is cold! It snows. I wear my coat, gloves, and hat. I make a snowman with my brother.", "tr": "K\u0131\u015f soguk! Kar ya\u011f\u0131yor. Montumu, eldivenlerimi ve \u015fapkam\u0131 giyiyorum."},
                {"img": "\U0001f30d", "en": "Spring, summer, autumn, winter. There are four seasons in a year. Every season is special. Which season do you like?", "tr": "Ilkbahar, yaz, sonbahar, k\u0131\u015f. Y\u0131lda d\u00f6rt mevsim var. Her mevsim \u00f6zel. Sen hangi mevsimi seversin?"},
            ],
        },
        {
            "title": "What's the Time?",
            "icon": "\U0001f570\ufe0f",
            "color": "#2196f3",
            "pages": [
                {"img": "\U0001f305", "en": "It is seven o'clock. I wake up. Good morning! Time for breakfast.", "tr": "Saat yedi. Uyan\u0131yorum. G\u00fcnaydin! Kahvalt\u0131 zaman\u0131."},
                {"img": "\U0001f3eb", "en": "It is eight o'clock. I go to school. I walk with my friend. We are not late.", "tr": "Saat sekiz. Okula gidiyorum. Arkada\u015f\u0131mla y\u00fcr\u00fcy\u00f6r\u00fcz."},
                {"img": "\U0001f4da", "en": "It is ten o'clock. I am in class. We are learning English. It is fun!", "tr": "Saat on. S\u0131n\u0131ftay\u0131m. Ingilizce \u00f6greniyoruz. Eglenceli!"},
                {"img": "\U0001f354", "en": "It is twelve o'clock. It is lunch time! I eat my sandwich and drink water.", "tr": "Saat on iki. \u00d6gle yemegi zaman\u0131! Sandvicimi yiyorum ve su i\u00e7iyorum."},
                {"img": "\u26bd", "en": "It is three o'clock. School is over. I play football with my friends in the park.", "tr": "Saat \u00fc\u00e7. Okul bitti. Parkta arkada\u015flar\u0131mla futbol oynuyorum."},
                {"img": "\U0001f4fa", "en": "It is six o'clock. I am at home. I do my homework. Then I watch TV.", "tr": "Saat alt\u0131. Evdeyim. \u00d6devimi yap\u0131yorum. Sonra TV izliyorum."},
                {"img": "\U0001f319", "en": "It is nine o'clock. It is bedtime! Good night! See you tomorrow!", "tr": "Saat dokuz. Yatma zaman\u0131! Iyi geceler! Yar\u0131n g\u00f6r\u00fc\u015f\u00fcr\u00fcz!"},
            ],
        },
    ],
    "3": [
        {
            "title": "The Birthday Party",
            "icon": "\U0001f382",
            "color": "#e91e63",
            "pages": [
                {"img": "\U0001f382", "en": "Today is my birthday. I am nine years old! My mother is making a big chocolate cake. My friends are coming to my party.", "tr": "Bug\u00fcn benim dogum g\u00fcn\u00fcm. Dokuz ya\u015f\u0131nday\u0131m! Annem b\u00fcy\u00fck \u00e7ikolatali pasta yap\u0131yor."},
                {"img": "\U0001f388", "en": "We decorate the house with balloons and ribbons. There are red, blue, and yellow balloons everywhere. The house looks beautiful!", "tr": "Evi balonlar ve kurdelelerle s\u00fcsl\u00fcy\u00f6ruz. Her yerde k\u0131rm\u0131z\u0131, mavi ve sar\u0131 balonlar var."},
                {"img": "\U0001f381", "en": "My friends arrive at two o'clock. They bring presents! Ece gives me a book. Ali gives me a puzzle. I say, 'Thank you very much!'", "tr": "Arkada\u015flar\u0131m saat ikide geliyor. Hediye getiriyorlar! Ece bana bir kitap veriyor."},
                {"img": "\U0001f3b5", "en": "We play games and listen to music. We play musical chairs. Zeynep wins the game. She gets a small prize.", "tr": "Oyunlar oynuyoruz ve m\u00fczik dinliyoruz. M\u00fczikli sandalye oynuyoruz. Zeynep oyunu kazan\u0131yor."},
                {"img": "\U0001f56f\ufe0f", "en": "It is time for the cake! My mother brings the cake with nine candles. Everyone sings 'Happy Birthday to You!' I make a wish and blow out the candles.", "tr": "Pasta zaman\u0131! Annem dokuz mumlu pastayi getiriyor. Herkes Iyi ki Dogdun!' s\u00f6yl\u00fcyor."},
                {"img": "\U0001f370", "en": "The cake is delicious! We all eat cake and drink juice. My friend says, 'This is the best party ever!' I am so happy.", "tr": "Pasta \u00e7ok lezzetli! Hepimiz pasta yiyoruz ve meyve suyu i\u00e7iyoruz."},
                {"img": "\U0001f31f", "en": "At the end of the party, I hug all my friends. 'Thank you for coming! You are the best friends in the world!' What a wonderful birthday!", "tr": "Partinin sonunda t\u00fcm arkada\u015flar\u0131ma sar\u0131l\u0131yorum. 'Geldiginiz i\u00e7in tesekkurler!'"},
            ],
        },
        {
            "title": "The Supermarket Adventure",
            "icon": "\U0001f6d2",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f4dd", "en": "My mother has a shopping list. She says, 'We need bread, milk, eggs, apples, and cheese. Can you help me find them?'", "tr": "Annemin al\u0131\u015fveri\u015f listesi var. 'Ekmek, s\u00fct, yumurta, elma ve peynir laz\u0131m' diyor."},
                {"img": "\U0001f35e", "en": "First, I find the bread. It is in aisle one. There is white bread and brown bread. My mother likes brown bread.", "tr": "Ilk olarak ekmegi buluyorum. Birinci koridorda. Beyaz ekmek ve kepekli ekmek var."},
                {"img": "\U0001f95b", "en": "Then I find the milk. There are big bottles and small bottles. We need two big bottles of milk.", "tr": "Sonra s\u00fct\u00fc buluyorum. B\u00fcy\u00fck siseler ve k\u00fc\u00e7\u00fck siseler var. Iki b\u00fcy\u00fck sise s\u00fct laz\u0131m."},
                {"img": "\U0001f34e", "en": "The apples are in the fruit section. There are red, green, and yellow apples. I choose five red apples. They look delicious!", "tr": "Elmalar meyve b\u00f6l\u00fcm\u00fcnde. K\u0131rm\u0131z\u0131, ye\u015fil ve sar\u0131 elmalar var. Be\u015f k\u0131rm\u0131z\u0131 elma se\u00e7iyorum."},
                {"img": "\U0001f9c0", "en": "I find the cheese next to the milk. My mother asks, 'How much is the cheese?' It is twelve lira. 'That's fine,' she says.", "tr": "Peyniri s\u00fct\u00fcn yan\u0131nda buluyorum. Annem 'Peynir ka\u00e7 lira?' diye soruyor."},
                {"img": "\U0001f4b0", "en": "At the checkout, the total is forty-two lira. My mother pays. I carry the bags to the car. I am a good helper!", "tr": "Kasada toplam k\u0131rk iki lira. Annem \u00f6d\u00fcyor. \u00c7antalari arabaya ta\u015f\u0131yorum."},
                {"img": "\U0001f44d", "en": "My mother says, 'Well done! You are a great shopper!' I feel proud. I can find everything on the list!", "tr": "Annem 'Aferin! Harika bir al\u0131\u015fveri\u015f\u00e7isin!' diyor. Gururlu hissediyorum."},
            ],
        },
        {
            "title": "My Body",
            "icon": "\U0001f9d2",
            "color": "#2196f3",
            "pages": [
                {"img": "\U0001f9d2", "en": "I have a head, two arms, two legs, and a body. This is me! Let me tell you about my body.", "tr": "Bir ba\u015f\u0131m, iki kolum, iki bacag\u0131m ve bir v\u00fccudum var. Bu benim!"},
                {"img": "\U0001f441\ufe0f", "en": "I have two eyes. I can see with my eyes. I see my friends, my school, and the beautiful sky.", "tr": "Iki g\u00f6z\u00fcm var. G\u00f6zlerimle g\u00f6rebiliyorum."},
                {"img": "\U0001f442", "en": "I have two ears. I can hear with my ears. I hear music, birds, and my teacher's voice.", "tr": "Iki kulagim var. Kulaklarimla duyabiliyorum."},
                {"img": "\U0001f443", "en": "I have a nose. I can smell with my nose. I smell flowers, food, and the fresh air.", "tr": "Bir burnum var. Burnumla koklayabiliyorum."},
                {"img": "\U0001f444", "en": "I have a mouth. I can talk, eat, and sing with my mouth. I like to sing English songs!", "tr": "Bir ag\u0131z\u0131m var. Ag\u0131z\u0131mla konu\u015fabilirim, yiyebilirim ve \u015fark\u0131 s\u00f6yleyebilirim."},
                {"img": "\U0001f44b", "en": "I have two hands with ten fingers. I can write, draw, and clap with my hands.", "tr": "On parmagli iki elim var. Ellerimle yazabilirim, \u00e7izebilirim ve alk\u0131\u015flayabilirim."},
                {"img": "\U0001f3c3", "en": "I have two legs and two feet. I can run, jump, and dance. My body is amazing!", "tr": "Iki bacag\u0131m ve iki ayag\u0131m var. Kosabilirim, z\u0131playabilirim ve dans edebilirim."},
            ],
        },
    ],
    "4": [
        {
            "title": "The School Fair",
            "icon": "\U0001f3aa",
            "color": "#9c27b0",
            "pages": [
                {"img": "\U0001f3aa", "en": "Every year, our school has a fair in May. This year, our class is making a food stall. We are going to sell sandwiches and lemonade.", "tr": "Her y\u0131l okulumuzun may\u0131sta bir kermes var. Bu y\u0131l sinifimiz yiyecek stand\u0131 yap\u0131yor."},
                {"img": "\U0001f4cb", "en": "Our teacher says, 'We need to plan everything carefully. Who wants to make sandwiches? Who can bring lemons?' I raise my hand for lemons.", "tr": "\u00d6gretmenimiz 'Her seyi dikkatli planlamal\u0131y\u0131z. Kim sandvi\u00e7 yapabilir? Kim limon getirebilir?' diyor."},
                {"img": "\U0001f950", "en": "On the day of the fair, we arrive early. We prepare twenty cheese sandwiches and thirty glasses of lemonade. Our stall looks great!", "tr": "Kermes g\u00fcn\u00fc erken geliyoruz. Yirmi peynirli sandvi\u00e7 ve otuz bardak limonata hazirliyoruz."},
                {"img": "\U0001f4b0", "en": "Many students come to buy our food. 'How much is one sandwich?' asks a boy. 'It is five lira,' I say. 'And lemonade is three lira.'", "tr": "Birçok \u00f6grenci yiyecegimizi almaya geliyor. 'Bir sandvi\u00e7 ka\u00e7 lira?' diye soruyor bir \u00e7ocuk."},
                {"img": "\U0001f3b5", "en": "There is also a music show. Some students play the guitar and the flute. Other students dance. The fair is very exciting!", "tr": "Bir de m\u00fczik g\u00f6sterisi var. Baz\u0131 \u00f6grenciler gitar ve fl\u00fct \u00e7al\u0131yor. Diger \u00f6grenciler dans ediyor."},
                {"img": "\U0001f3c6", "en": "At the end of the day, we count our money. We made one hundred and fifty lira! The teacher says, 'We will give this money to a children's charity.'", "tr": "G\u00fcn\u00fcn sonunda param\u0131z\u0131 say\u0131yoruz. Y\u00fcz elli lira kazandik!"},
                {"img": "\U0001f31f", "en": "The school fair was amazing. We worked as a team, learned about money, and helped other children. I can't wait for next year's fair!", "tr": "Okul kermesi harikayd\u0131. Tak\u0131m olarak \u00e7al\u0131\u015ft\u0131k, para hakk\u0131nda \u00f6grendik ve diger \u00e7ocuklara yard\u0131m ettik."},
            ],
        },
        {
            "title": "My Dream Job",
            "icon": "\U0001f468\u200d\U0001f680",
            "color": "#2196f3",
            "pages": [
                {"img": "\U0001f469\u200d\U0001f3eb", "en": "There are many jobs in the world. A teacher teaches children at school. My teacher is kind and patient. She helps us learn new things every day.", "tr": "D\u00fcnyada birçok meslek var. \u00d6gretmen okulda \u00e7ocuklara \u00f6gretir. \u00d6gretmenim nazik ve sab\u0131rl\u0131."},
                {"img": "\U0001f468\u200d\u2695\ufe0f", "en": "A doctor helps sick people. Doctors work in hospitals. They wear white coats. My uncle is a doctor. He saves lives!", "tr": "Doktor hasta insanlara yard\u0131m eder. Doktorlar hastanelerde \u00e7al\u0131\u015f\u0131r. Amcam bir doktor."},
                {"img": "\U0001f468\u200d\U0001f692", "en": "A firefighter puts out fires. They are very brave. They also help people in emergencies. They drive big red trucks.", "tr": "Itfaiyeci yang\u0131nlar\u0131 s\u00f6nd\u00fcr\u00fcr. \u00c7ok cesurlar. Acil durumlarda insanlara yard\u0131m ederler."},
                {"img": "\U0001f468\u200d\U0001f373", "en": "A chef cooks food in restaurants. Chefs can make delicious meals from all around the world. I like cooking too!", "tr": "A\u015f\u00e7\u0131 restoranlarda yemek pi\u015firir. A\u015f\u00e7\u0131lar d\u00fcnyan\u0131n her yerinden lezzetli yemekler yapabilir."},
                {"img": "\U0001f468\u200d\U0001f680", "en": "An astronaut travels to space! They fly in rockets and study the stars. Being an astronaut is an exciting job but also very difficult.", "tr": "Astronot uzaya seyahat eder! Roketlerle u\u00e7ar ve y\u0131ld\u0131zlar\u0131 inceler."},
                {"img": "\U0001f469\u200d\U0001f4bb", "en": "A programmer writes codes for computers and apps. Many children today want to become programmers. Technology is the future!", "tr": "Programc\u0131 bilgisayarlar ve uygulamalar i\u00e7in kod yazar. Teknoloji gelecektir!"},
                {"img": "\U0001f468\u200d\U0001f3a8", "en": "An artist creates beautiful paintings and sculptures. Art makes the world more colourful and interesting.", "tr": "Sanat\u00e7\u0131 g\u00fczel resimler ve heykeller yarat\u0131r. Sanat d\u00fcnyay\u0131 daha renkli yapar."},
                {"img": "\U0001f4ab", "en": "What is your dream job? You can be anything you want! Study hard, be kind, and follow your dreams. The future is yours!", "tr": "Hayalindeki meslek ne? Istedigin her sey olabilirsin! \u00c7ok \u00e7al\u0131\u015f, iyi ol ve hayallerinin pe\u015finden git!"},
            ],
        },
        {
            "title": "Save Our Planet",
            "icon": "\U0001f30d",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f30d", "en": "Our planet Earth is beautiful. It has oceans, forests, mountains, and animals. But our planet needs help. We must take care of it.", "tr": "Gezegenimiz D\u00fcnya g\u00fczeldir. Okyanuslar\u0131, ormanlar\u0131, daglar\u0131 ve hayvanlar\u0131 var. Ama gezegenimizin yard\u0131ma ihtiyac\u0131 var."},
                {"img": "\u267b\ufe0f", "en": "We can recycle. Paper, plastic, and glass can be recycled. Don't throw them in the bin \u2014 put them in the recycling box!", "tr": "Geri d\u00f6n\u00fc\u015f\u00fcm yapabiliriz. Kagit, plastik ve cam geri d\u00f6n\u00fc\u015ft\u00fcr\u00fclebilir."},
                {"img": "\U0001f6b0", "en": "We must save water. Turn off the tap when you brush your teeth. Take short showers. Every drop is important!", "tr": "Su tasarrufu yapmal\u0131y\u0131z. Dis f\u0131r\u00e7alarken muslugun kapat. K\u0131sa du\u015f al."},
                {"img": "\U0001f4a1", "en": "We can save energy. Turn off the lights when you leave a room. Walk or ride a bike instead of using a car.", "tr": "Enerji tasarrufu yapabiliriz. Odadan \u00e7\u0131karken \u0131\u015f\u0131klar\u0131 kapat."},
                {"img": "\U0001f333", "en": "We can plant trees. Trees give us oxygen and clean the air. They are homes for birds and animals. Let's plant more trees!", "tr": "Agaç dikebiliriz. Agaçlar bize oksijen verir ve havay\u0131 temizler."},
                {"img": "\U0001f6ae", "en": "Never throw rubbish on the ground. Use the bins. Keep our streets, parks, and beaches clean.", "tr": "Asla yere \u00e7\u00f6p atma. \u00c7\u00f6p kutular\u0131n\u0131 kullan. Sokaklar\u0131m\u0131z\u0131 temiz tutal\u0131m."},
                {"img": "\U0001f31f", "en": "Small actions make a big difference. If everyone helps a little, we can save our beautiful planet. Earth is our home \u2014 let's protect it!", "tr": "K\u00fc\u00e7\u00fck eylemler b\u00fcy\u00fck fark yarat\u0131r. D\u00fcnya bizim evimiz \u2014 onu koruyal\u0131m!"},
            ],
        },
    ],
    "5": [
        {
            "title": "A Day at the Airport",
            "icon": "\u2708\ufe0f",
            "color": "#4caf50",
            "pages": [
                {"img": "\u2708\ufe0f", "en": "Last summer, my family and I went on a holiday. We drove to the airport early in the morning. I was very excited because it was my first time on an airplane!", "tr": "Ge\u00e7en yaz ailemle tatile gittik. Sabah erkenden havalimanina gittik. \u00c7ok heyecanliydim \u00e7\u00fcnk\u00fc ilk kez u\u00e7a\u011fa binecektim!"},
                {"img": "\U0001f9f3", "en": "We had two big suitcases and three small bags. My father showed our passports and tickets at the check-in desk. The woman smiled and said, 'Have a nice flight!'", "tr": "Iki b\u00fcy\u00fck bavulumuz ve \u00fc\u00e7 k\u00fc\u00e7\u00fck \u00e7antamiz vardi. Babam check-in masasinda pasaportlarimizi ve biletlerimizi g\u00f6sterdi."},
                {"img": "\U0001f6c2", "en": "Then we went through customs. A man looked at our passports again. After that, we walked to the gate. There were many people waiting for the same flight.", "tr": "Sonra g\u00fcmr\u00fckten ge\u00e7tik. Bir adam pasaportlarimiza tekrar bakti. Ardidan kapiya y\u00fcr\u00fcd\u00fck."},
                {"img": "\U0001f6eb", "en": "The airplane was very big and white. We found our seats and put on our seatbelts. The pilot said, 'Welcome aboard! We will arrive in two hours.' The plane started to move.", "tr": "U\u00e7ak \u00e7ok b\u00fcy\u00fck ve beyazdi. Koltuklarimizi bulduk ve kemerlerimizi taktik. Pilot 'Hos geldiniz! Iki saat sonra varacagiz' dedi."},
                {"img": "\u2601\ufe0f", "en": "I looked out the window. The houses became very small, like toys. Then we were above the clouds. The sky was so blue and beautiful. I took many photos.", "tr": "Pencereden disari baktim. Evler oyuncak gibi \u00e7ok k\u00fc\u00e7\u00fcld\u00fc. Sonra bulutlarin \u00fcst\u00fcndeydik."},
                {"img": "\U0001f3d6\ufe0f", "en": "We arrived at the hotel in the afternoon. It was near the beach. I could see the sea from my room. 'This is going to be a great holiday!' I said to my sister.", "tr": "\u00d6\u011fleden sonra otele vardik. Plajin yakinindaydi. Odamdan denizi g\u00f6rebiliyordum."},
                {"img": "\U0001f3ca", "en": "Every day we went to the beach. I swam in the sea and built sandcastles. My mother read books under the umbrella. My father took a boat tour around the island.", "tr": "Her g\u00fcn plaja gittik. Denizde y\u00fczdüm ve kumdan kaleler yaptim."},
                {"img": "\U0001f5fa\ufe0f", "en": "On the last day, we visited a museum and walked around the old town. We bought souvenirs for our friends. I bought a small ship model and a map.", "tr": "Son g\u00fcn bir m\u00fcze ziyaret ettik ve eski sehirde dolastik."},
                {"img": "\U0001f60a", "en": "The holiday was wonderful. On the plane home, I thought about all the fun we had. I will never forget my first airplane trip. Next year, I want to travel to a different country!", "tr": "Tatil harikaydı. Ilk u\u00e7ak yolculu\u011fumu asla unutmayaca\u011fim. Gelecek yil farkli bir \u00fclkeye seyahat etmek istiyorum!"},
            ],
        },
        {
            "title": "Shopping with Grandma",
            "icon": "\U0001f6d2",
            "color": "#ff9800",
            "pages": [
                {"img": "\U0001f475", "en": "Every Saturday, I go shopping with my grandmother. She is 68 years old but she is very energetic. She always says, 'A good day starts with a good market!'", "tr": "Her cumartesi b\u00fcy\u00fcannemle alisverise giderim. 68 yasinda ama \u00e7ok enerjik."},
                {"img": "\U0001f3ea", "en": "First, we went to the supermarket. Grandma took a basket and gave me the shopping list. 'We need milk, eggs, bread, cheese, and tomatoes,' she said.", "tr": "\u00d6nce s\u00fcpermarkete gittik. B\u00fcy\u00fcannem bir sepet aldi ve alisveris listesini bana verdi."},
                {"img": "\U0001f34e", "en": "I found the fruits and vegetables section. The apples were cheap today \u2014 only two lira per kilo. But the strawberries were expensive. Grandma said, 'Let's buy the apples.'", "tr": "Meyve ve sebze b\u00f6l\u00fcm\u00fcn\u00fc buldum. Bug\u00fcn elmalar ucuzdu. Ama \u00e7ilekler pahaliydi."},
                {"img": "\U0001f4b0", "en": "At the cashier, Grandma paid with her credit card. The total was forty-five lira. She checked the receipt carefully. 'Always check your receipt,' she told me.", "tr": "Kasada b\u00fcy\u00fcannem kredi kartiyla \u00f6dedi. Toplam kirk bes liraydı. Fisi dikkatlice kontrol etti."},
                {"img": "\U0001f457", "en": "Then we went to a clothes store. I needed a new jacket for school. We looked at many jackets in different colors and sizes. I tried on a blue one in the fitting room.", "tr": "Sonra bir giyim magazasina gittik. Okul i\u00e7in yeni bir cekete ihtiyacim vardi."},
                {"img": "\U0001f381", "en": "'It looks great on you!' said Grandma. The jacket was on sale \u2014 thirty percent discount. She also bought me a gift \u2014 a warm scarf.", "tr": "'\u00c7ok yakisti sana!' dedi b\u00fcy\u00fcannem. Ceket indirimdeydi. Bana bir de hediye aldi \u2014 sicak bir atki."},
                {"img": "\U0001f9fe", "en": "After shopping, we sat in a cafe and drank tea. Grandma counted the money she spent. 'We saved a lot today with the discounts,' she said with a smile.", "tr": "Alisveristen sonra bir kafede oturup \u00e7ay i\u00e7tik. 'Bug\u00fcn indirimlerle \u00e7ok tasarruf ettik' dedi."},
                {"img": "\u2764\ufe0f", "en": "I love shopping with my grandma. She teaches me about money, prices, and how to find good deals. She is the best shopping partner in the world!", "tr": "B\u00fcy\u00fcannemle alisveris yapmayi \u00e7ok seviyorum. D\u00fcnyanin en iyi alisveris arkadasi!"},
            ],
        },
        {
            "title": "The Brave Nurse",
            "icon": "\U0001f3e5",
            "color": "#e91e63",
            "pages": [
                {"img": "\U0001f912", "en": "Last week, I woke up with a terrible headache and a high fever. My mother touched my forehead and said, 'You are very hot! We need to go to the hospital.'", "tr": "Ge\u00e7en hafta korkunç bir baş a\u011frisi ve y\u00fcksek atesle uyandim."},
                {"img": "\U0001f691", "en": "My mother called the doctor and made an appointment. We took a taxi to the hospital. In the emergency room, a kind nurse met us. Her name was Ayse.", "tr": "Annem doktoru aradi ve randevu aldi. Hastaneye taksiyle gittik."},
                {"img": "\U0001f321\ufe0f", "en": "Nurse Ayse checked my temperature. It was 39 degrees! She said, 'Don't worry. The doctor will see you soon. Let me give you some medicine for the fever.'", "tr": "Hemsire Ayse atesimi \u00f6l\u00e7t\u00fc. 39 dereceydi! 'Endiselenme' dedi."},
                {"img": "\U0001f468\u200d\u2695\ufe0f", "en": "The doctor examined me. He listened to my chest and looked in my throat. 'You have the flu,' he said. 'You need to rest at home for three days and take this medicine.'", "tr": "Doktor beni muayene etti. 'Gripin var' dedi. '\u00dc\u00e7 g\u00fcn evde dinlenmen gerekiyor.'"},
                {"img": "\U0001f48a", "en": "He wrote a prescription. We went to the pharmacy next to the hospital. The pharmacist gave us the medicine and said, 'Take one pill in the morning and one at night.'", "tr": "Bir re\u00e7ete yazdi. Hastanenin yanindaki eczaneye gittik."},
                {"img": "\U0001f6cf\ufe0f", "en": "I stayed at home for three days. Nurse Ayse called every day to ask how I was feeling. She said, 'Drink lots of water and eat soup. You will get better soon.'", "tr": "\u00dc\u00e7 g\u00fcn evde kaldim. Hemsire Ayse her g\u00fcn arayip nasil hissettigimi sordu."},
                {"img": "\U0001f4aa", "en": "After three days, my fever was gone and I felt much better. I went back to school. My friends were happy to see me. 'We missed you!' they said.", "tr": "\u00dc\u00e7 g\u00fcn sonra atesim d\u00fcst\u00fc ve kendimi \u00e7ok daha iyi hissettim."},
                {"img": "\U0001f31f", "en": "I wrote a thank-you letter to Nurse Ayse. 'Thank you for helping me get better. You are a real hero!' When I grow up, maybe I will be a nurse too.", "tr": "Hemsire Ayse'ye bir tesekkür mektubu yazdim. 'Sen ger\u00e7ek bir kahramansin!'"},
            ],
        },
    ],
    "6": [
        {
            "title": "My New Hobby",
            "icon": "\U0001f3a8",
            "color": "#2196f3",
            "pages": [
                {"img": "\U0001f914", "en": "My name is Elif. I am twelve years old and I am in the sixth grade. Last month, my art teacher said, 'Everyone should try a new hobby this semester.' I didn't know what to choose.", "tr": "Adim Elif. On iki yasindayim ve altinci siniftayim. '\u00d6\u011fretmenim yeni bir hobi denemeliyiz' dedi."},
                {"img": "\U0001f4f8", "en": "My friend Zeynep likes photography. She takes beautiful photos of flowers and birds. 'Photography is more exciting than painting,' she said. But I am not good at taking photos.", "tr": "Arkadasim Zeynep fotografçiligi seviyor. 'Fotografçilik resim yapmaktan daha heyecanli' dedi."},
                {"img": "\U0001f3b5", "en": "My brother plays the guitar every evening. He is better at music than me. 'Why don't you try dancing?' he suggested. 'It is the most fun activity in the world.'", "tr": "Agabeyim her aksam gitar çalar. 'Neden dansi denemiyorsun?' \u00f6nerdi."},
                {"img": "\U0001f373", "en": "One day, my mother was cooking dinner. 'Can I help you?' I asked. She showed me how to make a simple salad. I liked cutting the vegetables and mixing them together.", "tr": "Bir g\u00fcn annem aksam yemegi pisiriyordu. 'Sana yardim edebilir miyim?' diye sordum."},
                {"img": "\U0001f4d6", "en": "The next day, I borrowed a cookbook from the library. It had recipes from many countries. 'I am going to learn cooking!' I told my family. They were surprised but happy.", "tr": "Ertesi g\u00fcn k\u00fct\u00fcphaneden bir yemek kitabi \u00f6d\u00fcnç aldim. 'Yemek yapmayi \u00f6grenecegim!' dedim."},
                {"img": "\U0001f9c1", "en": "I started with easy recipes \u2014 pancakes, omelettes, and fruit smoothies. Cooking is harder than it looks! My first cake was the worst cake ever, but I didn't give up.", "tr": "Kolay tariflerle basladim. Yemek yapmak g\u00f6r\u00fcnd\u00fc\u011f\u00fcnden daha zor! Ilk pastam k\u00f6t\u00fcyd\u00fc ama vazge\u00e7medim."},
                {"img": "\U0001f382", "en": "After two months of practice, I made a chocolate cake for my mother's birthday. It was delicious! Everyone said it was the best cake they ever ate. I felt so proud.", "tr": "Iki aylik pratikten sonra annemin dogum g\u00fcn\u00fc i\u00e7in \u00e7ikolatali pasta yaptim. \u00c7ok lezzetliydi!"},
                {"img": "\U0001f31f", "en": "Now cooking is my favorite hobby. It is more creative than watching TV and more useful than playing games. My dream is to become a famous chef one day!", "tr": "Simdi yemek yapmak en sevdigim hobi. Hayalim bir g\u00fcn \u00fcnl\u00fc bir asçi olmak!"},
            ],
        },
        {
            "title": "The Football Match",
            "icon": "\u26bd",
            "color": "#4caf50",
            "pages": [
                {"img": "\u26bd", "en": "Kerem is the best football player in our school. He is taller than most students and he runs faster than everyone. Today, our team is playing against Ataturk Middle School.", "tr": "Kerem okulumuzun en iyi futbolcusu. \u00c7ogu \u00f6grenciden daha uzun ve herkesten daha hizli kosuyor."},
                {"img": "\U0001f3df\ufe0f", "en": "The stadium is full of students and parents. Our coach is talking to the team. 'Their goalkeeper is good but their defence is weaker than ours. Play as a team!'", "tr": "Stadyum \u00f6grenci ve velilerle dolu. Antren\u00f6r\u00fcm\u00fcz takimla konusuyor."},
                {"img": "\U0001f4e3", "en": "The referee blows the whistle. The match begins! In the first ten minutes, the other team is attacking more. Their number 10 shoots at our goal. Our goalkeeper saves it!", "tr": "Hakem d\u00fcd\u00fc\u011f\u00fc \u00e7alar. Ma\u00e7 baslar! Diger takim daha \u00e7ok atak yapiyor. Kalecimiz kurtariyor!"},
                {"img": "\U0001f3c3", "en": "Kerem gets the ball and runs towards the other goal. He passes two players. He shoots... but the ball hits the post! 'So close!' everyone shouts.", "tr": "Kerem topu aliyor ve diger kaleye dogru kosuyor. Sut atiyor... ama top direge \u00e7arpiyor!"},
                {"img": "\u23f1\ufe0f", "en": "It is half time. The score is 0-0. The coach says, 'You are playing well. Keep passing the ball quickly. Kerem, try shooting from the left side.'", "tr": "Devre arasi. Skor 0-0. Antren\u00f6r 'Iyi oynuyorsunuz' diyor."},
                {"img": "\U0001f945", "en": "The second half starts. In the 65th minute, I pass the ball to Kerem. He controls it perfectly and kicks it into the net. GOAL! We are winning 1-0!", "tr": "Ikinci yari basliyor. 65. dakikada topu Kerem'e pas atiyorum. GOL! 1-0 \u00f6nde!"},
                {"img": "\U0001f630", "en": "But the other team scores in the 80th minute. The score is 1-1! There are only five minutes left. Everyone is nervous. Can we win this match?", "tr": "Ama diger takim 80. dakikada gol atiyor. Skor 1-1! Sadece bes dakika kaldi."},
                {"img": "\U0001f3c6", "en": "In the last minute, Kerem gets a free kick. He shoots... GOAL! The crowd goes wild! Final score: 2-1. We are the champions!", "tr": "Son dakikada Kerem serbest vurus kazaniyor. Sut atiyor... GOL! Son skor: 2-1. Biz sampiyonuz!"},
            ],
        },
        {
            "title": "Lost in the City",
            "icon": "\U0001f3d9\ufe0f",
            "color": "#9c27b0",
            "pages": [
                {"img": "\U0001f68c", "en": "Last Sunday, I visited my cousin in Istanbul. She lives near Taksim Square. I took the bus from the station, but I got off at the wrong bus stop!", "tr": "Ge\u00e7en pazar Istanbul'daki kuzinime gittim. Yanlis durakta indim!"},
                {"img": "\U0001f5fa\ufe0f", "en": "I looked around. I didn't know this street at all. There were tall buildings, a cinema, and a big park. My phone had no battery.", "tr": "Etrafima baktim. Bu sokagi hi\u00e7 tanimiyordum. Telefonumun sarji bitmisti."},
                {"img": "\U0001f46e", "en": "I walked to the nearest intersection and asked a police officer for help. 'Excuse me, how can I get to Taksim Square?' I asked politely.", "tr": "En yakin kavsaga y\u00fcr\u00fcd\u00fcm ve bir polisten yardim istedim."},
                {"img": "\U0001f687", "en": "'You need to take the metro,' said the officer. 'Walk straight, turn left at the library, and you will see the metro station on the right side.'", "tr": "'Metro almaniz gerekiyor' dedi polis. 'D\u00fcz y\u00fcr\u00fcy\u00fcn, k\u00fct\u00fcphaneden sola d\u00f6n\u00fcn.'"},
                {"img": "\U0001f4cd", "en": "I followed the directions. I walked past a restaurant, a bank, and a post office. Then I saw the library. I turned left and there it was \u2014 the metro station!", "tr": "Yol tarifini takip ettim. Sonra k\u00fct\u00fcphaneyi g\u00f6rd\u00fcm. Metro istasyonu oradaydı!"},
                {"img": "\U0001f3ab", "en": "I bought a ticket and waited on the platform. The train arrived in three minutes. Taksim was only four stops away.", "tr": "Bilet aldim ve platformda bekledim. Tren \u00fc\u00e7 dakikada geldi."},
                {"img": "\U0001f917", "en": "I got off at Taksim and called my cousin from a phone shop. She found me at the square. 'I was so worried about you!' she said and hugged me.", "tr": "Taksim'de indim ve bir telefoncudan kuzinemi aradim. 'Senin i\u00e7in \u00e7ok endislendim!' dedi."},
                {"img": "\U0001f604", "en": "We laughed about my adventure and went to eat pizza. Now I always charge my phone before traveling. Getting lost taught me to ask for directions and be brave!", "tr": "Maceramla ilgili g\u00fcld\u00fck ve pizza yemeye gittik. Kaybolmak bana cesur olmayi \u00f6gretti!"},
            ],
        },
    ],
    "7": [
        {
            "title": "The Science Project",
            "icon": "\U0001f52c",
            "color": "#ff9800",
            "pages": [
                {"img": "\U0001f4cb", "en": "Our science teacher gave us a project: 'You must design something useful for your city.' We had to work in groups of three. I was nervous because I didn't have any ideas.", "tr": "Fen \u00f6gretmenimiz bize bir proje verdi. \u00dc\u00e7er kisilik gruplar halinde \u00e7alismamiz gerekiyordu."},
                {"img": "\U0001f331", "en": "My teammates were Ahmet and Selin. Selin said, 'We should make a smart garden system. It can water the plants automatically.' Ahmet was curious: 'How would that work?'", "tr": "Selin 'Akilli bah\u00e7e sistemi yapmaliyiz. Bitkileri otomatik sulayabilir' dedi."},
                {"img": "\U0001f4a1", "en": "Selin explained: 'We can use a sensor to check if the soil is dry. If it is dry, the system must turn on the water. If the soil is wet, it should stop.'", "tr": "Selin a\u00e7ikladı: 'Toprağın kuru olup olmadığını kontrol i\u00e7in bir sens\u00f6r kullanabiliriz.'"},
                {"img": "\U0001f527", "en": "We started building our project. Ahmet bought the materials \u2014 a small pump, plastic tubes, and a sensor. I designed the box. Selin wrote the code.", "tr": "Projemizi yapmaya basladik. Ahmet malzemeleri aldi. Ben kutuyu tasarladim."},
                {"img": "\U0001f62b", "en": "It wasn't easy. The pump didn't work on the first day. Ahmet was disappointed. 'We should try again,' said Selin patiently. 'Scientists never give up after one failure.'", "tr": "Kolay degildi. Pompa ilk g\u00fcn \u00e7alismadi. Selin sabırla 'Tekrar denemeliyiz' dedi."},
                {"img": "\u2705", "en": "After three weeks of hard work, our smart garden was ready! When the soil was dry, the water turned on. When it was wet, the water stopped. We were so proud.", "tr": "\u00dc\u00e7 haftalik yogun \u00e7alismadan sonra akilli bah\u00e7emiz hazirdi!"},
                {"img": "\U0001f3a4", "en": "On presentation day, I was brave and spoke first. 'Our project can save water and help farmers,' I said confidently. The teacher and students were impressed.", "tr": "Sunum g\u00fcn\u00fcnde cesur davrandim ve ilk ben konustum."},
                {"img": "\U0001f3c5", "en": "We won first place in the school science fair! I learned that teamwork can achieve amazing things.", "tr": "Okul bilim fuarinda birincilik kazandik! Takim \u00e7alismasinin harika seyler basarabilecegini \u00f6grendim."},
            ],
        },
        {
            "title": "Emotions Diary",
            "icon": "\U0001f4d4",
            "color": "#e91e63",
            "pages": [
                {"img": "\U0001f4d4", "en": "My school counselor gave everyone a notebook. 'This is your emotions diary,' she said. 'Every day, write how you feel and why. Understanding your feelings is very important.'", "tr": "Okul rehber \u00f6gretmenimiz herkese bir defter verdi. 'Bu sizin duygu g\u00fcnl\u00fcg\u00fcn\u00fcz' dedi."},
                {"img": "\U0001f60a", "en": "Monday: I felt happy today because I got a good grade on my math exam. When the teacher announced my score, I was surprised and excited.", "tr": "Pazartesi: Bug\u00fcn mutlu hissettim \u00e7\u00fcnk\u00fc matematik sinavindan iyi not aldim."},
                {"img": "\U0001f622", "en": "Tuesday: I felt sad and lonely at lunch. My best friend Melisa sat with other students. I was worried \u2014 was she angry with me? I felt too shy to ask her.", "tr": "Sali: \u00d6gle yemeginde \u00fczg\u00fcn ve yalniz hissettim. En iyi arkadasim baska \u00f6grencilerle oturdu."},
                {"img": "\U0001f624", "en": "Wednesday: I was angry in the morning. My brother used my tablet without asking. The counselor said, 'When you feel angry, take deep breaths and count to ten.'", "tr": "\u00c7arsamba: Sabah kizgindim. Agabeyim tabletimi sormadan kullandi."},
                {"img": "\U0001f917", "en": "Thursday: Melisa talked to me today! She said, 'Sorry I didn't sit with you. I was helping a new student.' I felt relieved and grateful. We hugged and laughed.", "tr": "Persembe: Melisa bug\u00fcn benimle konustu! '\u00d6z\u00fcr dilerim, yeni bir \u00f6grenciye yardim ediyordum' dedi."},
                {"img": "\U0001f630", "en": "Friday: We had a basketball game. I missed the last shot and we lost. I was disappointed. But my teammates said, 'Don't worry. We win and lose together!'", "tr": "Cuma: Basketbol macimiz vardi. Son atisi ka\u00e7irdim ve kaybettik."},
                {"img": "\U0001f9d8", "en": "Saturday: I read my diary at home. I realized that my emotions change every day \u2014 and that is completely normal. I feel hopeful about next week.", "tr": "Cumartesi: Evde g\u00fcnl\u00fcg\u00fcm\u00fc okudum. Duygularimin her g\u00fcn degistigini fark ettim."},
                {"img": "\U0001f48e", "en": "The counselor was right. Writing about my feelings helps me understand myself better. Being brave doesn't mean you never feel scared. It means you keep going.", "tr": "Rehber \u00f6gretmen hakliydi. Cesur olmak asla korkmamak degildir. Devam etmek demektir."},
            ],
        },
        {
            "title": "The Mountain Adventure",
            "icon": "\U0001f3d4\ufe0f",
            "color": "#607d8b",
            "pages": [
                {"img": "\U0001f3d4\ufe0f", "en": "In April, our class went on a nature trip to Uludag. We had to bring warm clothes because the mountain was still cold. 'You must stay with your groups,' said the teacher.", "tr": "Nisan'da sinifimiz Uludag'a doga gezisine gitti. Sicak kiyafetler getirmemiz gerekiyordu."},
                {"img": "\U0001f332", "en": "The forest was beautiful. There were tall pine trees, colorful flowers, and a clear river. We could hear the birds singing. 'Look at that waterfall!' shouted Burak.", "tr": "Orman g\u00fczeldi. Uzun \u00e7am agaçlari, rengârenk \u00e7i\u00e7ekler ve berrak bir nehir vardi."},
                {"img": "\U0001f98c", "en": "As we walked through the valley, we saw deer tracks in the soil. 'The deer must be near the lake,' said the guide. 'They always go there for water.'", "tr": "Vadide y\u00fcr\u00fcrken toprakta geyik izleri g\u00f6rd\u00fck."},
                {"img": "\u26c5", "en": "Suddenly, the sky became cloudy. The wind was getting stronger. 'We should find shelter,' said the teacher nervously. 'It looks like it might rain soon.'", "tr": "Birden g\u00f6ky\u00fcz\u00fc bulutlandi. 'Siginak bulmaliyiz' dedi \u00f6gretmen endiseyle."},
                {"img": "\U0001f3d5\ufe0f", "en": "We found a camping area with a wooden shelter. Just in time! Heavy rain started falling. We sat under the roof, drank hot tea, and listened to the rain.", "tr": "Ahsap siginagi olan bir kamp alani bulduk. Tam zamaninda! Siddetli yagmur yagiyor."},
                {"img": "\U0001f308", "en": "After thirty minutes, the rain stopped. A beautiful rainbow appeared over the mountain. The sun came out and everything looked fresh and clean.", "tr": "Otuz dakika sonra yagmur durdu. Dagin \u00fczerinde g\u00fczel bir g\u00f6kkusagi belirdi."},
                {"img": "\U0001f4f8", "en": "We took many photos near the waterfall and the rainbow. The guide showed us rare plants that only grew on this mountain. Nature is full of surprises.", "tr": "Selale ve g\u00f6kkusaginin yaninda \u00e7ok fotograf \u00e7ektik."},
                {"img": "\u2b50", "en": "On the way home, everyone was tired but peaceful. I looked at the stars from the bus window. Nature is the most precious thing we have. We should protect it.", "tr": "Eve d\u00f6nerken herkes yorgun ama huzurluydu. Doga sahip oldugumuz en degerli sey."},
            ],
        },
    ],
    "8": [
        {
            "title": "A Day Without Technology",
            "icon": "\U0001f4f5",
            "color": "#f44336",
            "pages": [
                {"img": "\U0001f4f5", "en": "Our teacher made an announcement: 'Tomorrow, nobody can use phones, tablets, or computers. It's Digital Detox Day.' We always use technology, so this was going to be difficult.", "tr": "\u00d6gretmenimiz bir duyuru yapti: 'Yarin kimse telefon, tablet veya bilgisayar kullanamaz.'"},
                {"img": "\u23f0", "en": "I usually wake up and immediately check my phone. But today, I woke up to an alarm clock instead. I ate breakfast while talking to my family.", "tr": "Genellikle uyanir uyanmaz telefonumu kontrol ederim. Bug\u00fcn \u00e7alar saatle uyandim."},
                {"img": "\U0001f6b6", "en": "I walked to school because I couldn't use the bus app. On the way, I noticed things I never saw before \u2014 a beautiful garden, a cat sleeping on a wall, and an old bookshop.", "tr": "Otobus uygulamasini kullanamad\u0131\u011f\u0131m i\u00e7in okula y\u00fcr\u00fcd\u00fcm. Hi\u00e7 fark etmedigim seyler g\u00f6rd\u00fcm."},
                {"img": "\U0001f4dd", "en": "In class, we wrote essays by hand instead of typing on computers. My hand hurt after two pages! I realized I rarely write with a pen anymore.", "tr": "Sinifta bilgisayarda yazmak yerine elle kompozisyon yazdik."},
                {"img": "\U0001f3b2", "en": "During lunch break, we played board games and card games instead of watching videos. It was actually more fun than sitting alone with headphones. We laughed so much!", "tr": "\u00d6gle arasinda video izlemek yerine masa oyunlari ve kart oyunlari oynadik."},
                {"img": "\u26bd", "en": "After school, I went to the park with my friends. We played football for two hours. I felt more energetic than usual because I hadn't been sitting in front of a screen all day.", "tr": "Okuldan sonra arkadaslarimla parka gittim. Iki saat futbol oynadik."},
                {"img": "\U0001f319", "en": "In the evening, I helped my mother cook dinner. Then we sat together and played a word game. My father told us funny stories from his childhood. I slept very well.", "tr": "Aksam anneme yemek pisirmesinde yardim ettim. Babam komik hikayeler anlatti."},
                {"img": "\U0001f4ad", "en": "Digital Detox Day taught me something important: technology is useful, but we shouldn't always depend on it. Sometimes the best moments happen when you put your phone down.", "tr": "Dijital Detoks G\u00fcn\u00fc bana \u00f6nemli bir sey \u00f6gretti: teknoloji faydali ama her zaman bagimli olmamaliyiz."},
            ],
        },
        {
            "title": "Getting Ready for High School",
            "icon": "\U0001f393",
            "color": "#673ab7",
            "pages": [
                {"img": "\U0001f4da", "en": "I am in the eighth grade and this is my last year in middle school. Next year, I will start high school. I always do my homework on time.", "tr": "Sekizinci siniftayim ve bu ortaokuldaki son yilim. Gelecek yil liseye baslayacagim."},
                {"img": "\U0001f4c5", "en": "I made a study plan. I usually wake up at seven o'clock. After breakfast, I study math. Then I exercise. In the afternoon, I study English and science.", "tr": "Bir \u00e7alisma plani yaptim. Genellikle saat yedide kalkarim."},
                {"img": "\U0001f469\u200d\U0001f3eb", "en": "My English teacher said, 'You should read English books and watch English videos every day. Because practice is the key to learning a language.'", "tr": "Ingilizce \u00f6gretmenim 'Her g\u00fcn Ingilizce kitap okumalisiniz' dedi."},
                {"img": "\U0001f91d", "en": "My friends and I sometimes study together. We help each other with difficult subjects. Emirhan is good at math, and I am better at English. Teamwork makes studying easier.", "tr": "Arkadaslarimla bazen birlikte \u00e7alisiriz. Zor konularda birbirimize yardim ederiz."},
                {"img": "\U0001f613", "en": "Sometimes I feel stressed and tired. On those days, I go for a walk or listen to music. My mother always says, 'Don't forget to rest.'", "tr": "Bazen stresli ve yorgun hissediyorum. Annem 'Dinlenmeyi unutma' der."},
                {"img": "\U0001f3af", "en": "I want to go to an Anatolian High School because they have excellent English programs. I need to get a high score on the LGS exam.", "tr": "Anadolu Lisesi'ne gitmek istiyorum \u00e7\u00fcnk\u00fc m\u00fckemmel Ingilizce programlari var."},
                {"img": "\U0001f30d", "en": "Learning English is not just for the exam. English opens doors to the world. I want to travel, meet people from different countries, and maybe study abroad.", "tr": "Ingilizce \u00f6grenmek sadece sinav i\u00e7in degil. Ingilizce d\u00fcnyaya kapilar a\u00e7iyor."},
                {"img": "\u2b50", "en": "Whatever happens on the exam, I know that I did my best. My teachers, my family, and my friends all believe in me. The future is bright, and I am ready!", "tr": "Sinavda ne olursa olsun, elimden gelenin en iyisini yaptigimi biliyorum. Gelecek parlak!"},
            ],
        },
        {
            "title": "The Seasons of My Village",
            "icon": "\U0001f3e1",
            "color": "#4caf50",
            "pages": [
                {"img": "\U0001f3e1", "en": "My grandparents live in a small village near the Black Sea. I visit them every summer. The village looks different in every season.", "tr": "B\u00fcy\u00fckanne ve b\u00fcy\u00fckbabam Karadeniz yakininda k\u00fc\u00e7\u00fck bir k\u00f6yde yasiyor."},
                {"img": "\U0001f338", "en": "In spring, the flowers bloom everywhere. The trees turn green and the birds come back from the south. My grandmother always plants tomatoes and peppers in April.", "tr": "Ilkbaharda \u00e7i\u00e7ekler her yerde a\u00e7ar. Agaçlar yeserir ve kuslar g\u00fcneyden geri d\u00f6ner."},
                {"img": "\u2600\ufe0f", "en": "Summer is the busiest season. The farmers harvest wheat and corn. Children swim in the river. The sun sets late, so we sit outside until ten o'clock.", "tr": "Yaz en yogun mevsimdir. \u00c7ift\u00e7iler bugday ve misir hasat eder. \u00c7ocuklar nehirde y\u00fczer."},
                {"img": "\U0001f342", "en": "Autumn brings beautiful colors. The leaves turn red, orange, and yellow. My grandfather picks apples and walnuts. We start wearing jackets and scarves.", "tr": "Sonbahar g\u00fczel renkler getirir. B\u00fcy\u00fckbabam elma ve ceviz toplar."},
                {"img": "\u2744\ufe0f", "en": "Winter is magical in the village. The mountains are covered with snow. We wear thick coats, gloves, and boots. My grandmother makes hot soup every evening.", "tr": "Kis k\u00f6yde b\u00fcy\u00fcl\u00fcd\u00fcr. Daglar karla kaplidir. B\u00fcy\u00fcannem her aksam sicak \u00e7orba yapar."},
                {"img": "\U0001f33f", "en": "The village teaches me things that the city cannot. My grandfather says, 'The earth gives us everything we need. We should take care of it.'", "tr": "K\u00f6y bana sehrin \u00f6gretemeyecegi seyler \u00f6gretir. 'Toprak ihtiyacimiz olan her seyi verir' der."},
                {"img": "\U0001f30d", "en": "Climate change is affecting our village too. Summers are hotter and winters have less snow. The river is smaller every year. We all need to protect nature.", "tr": "Iklim degisikligi k\u00f6y\u00fcm\u00fcz\u00fc de etkiliyor. Yazlar daha sicak ve kislarda daha az kar var."},
                {"img": "\u2764\ufe0f", "en": "I love my village in every season. The air is always fresh, the people are always kind, and the sky is always full of stars. This village will always be my home.", "tr": "K\u00f6y\u00fcm\u00fc her mevsimde seviyorum. Hava her zaman temiz, insanlar her zaman nazik."},
            ],
        },
    ],
    "9": [
        {
            "title": "My Exchange Year in London",
            "icon": "\U0001f1ec\U0001f1e7",
            "color": "#00897b",
            "pages": [
                {"img": "\u2708\ufe0f", "en": "Last September, I started my exchange year in London. I was nervous because it was my first time living abroad. My host family welcomed me at the airport.", "tr": "Ge\u00e7en Eyl\u00fcl, Londra'da de\u011fi\u015fim y\u0131l\u0131ma ba\u015fladim."},
                {"img": "\U0001f3eb", "en": "My new school was very different from my school in Turkey. Students wore uniforms and called teachers 'Sir' or 'Miss'. The lessons were mostly in English.", "tr": "Yeni okulum T\u00fcrkiye'deki okulumdan \u00e7ok farkl\u0131yd\u0131."},
                {"img": "\U0001f4da", "en": "At first, I couldn't understand everything in class. But my classmates were helpful. They explained things slowly and shared their notes with me.", "tr": "Ba\u015fta derslerde her \u015feyi anlayam\u0131yordum ama s\u0131n\u0131f arkada\u015flar\u0131m yard\u0131mc\u0131 oldu."},
                {"img": "\U0001f37d\ufe0f", "en": "The food was challenging! I missed Turkish breakfast and my mother's cooking. But I learned to enjoy fish and chips, and I even tried marmite.", "tr": "Yemekler zorlay\u0131c\u0131yd\u0131! T\u00fcrk kahvalt\u0131s\u0131n\u0131 \u00f6zledim."},
                {"img": "\U0001f3ad", "en": "I visited amazing places: the British Museum, Tower of London, and Buckingham Palace. I even watched a play at Shakespeare's Globe Theatre!", "tr": "Harika yerler ziyaret ettim: British Museum, Tower of London ve Buckingham Saray\u0131."},
                {"img": "\U0001f91d", "en": "I made friends from all over the world \u2014 Japan, Brazil, Germany. We communicated in English, which improved my speaking skills enormously.", "tr": "D\u00fcnyan\u0131n her yerinden arkada\u015flar edindim."},
                {"img": "\U0001f3c6", "en": "By the end of the year, my English was so much better. I could watch movies without subtitles and write essays confidently. The experience changed my life forever.", "tr": "Y\u0131l sonunda \u0130ngilizcem \u00e7ok daha iyiydi. Bu deneyim hayat\u0131m\u0131 sonsuza dek de\u011fi\u015ftirdi."},
            ],
        },
        {
            "title": "The Science Fair Project",
            "icon": "\U0001f52c",
            "color": "#5c6bc0",
            "pages": [
                {"img": "\U0001f4a1", "en": "Our teacher announced a science fair. We had to choose a topic, do research, and present our findings. I decided to study the effects of music on plant growth.", "tr": "\u00d6\u011fretmenimiz bilim fuar\u0131 duyurdu."},
                {"img": "\U0001f33f", "en": "I set up an experiment with three groups of plants. One listened to classical music, another to rock, and the third had no music at all.", "tr": "\u00dc\u00e7 grup bitkiyle deney kurdum."},
                {"img": "\U0001f4ca", "en": "After four weeks, the results were surprising. The plants with classical music grew 20% taller. The rock music group grew slightly less than the silent group.", "tr": "D\u00f6rt hafta sonra sonu\u00e7lar \u015fa\u015f\u0131rt\u0131c\u0131yd\u0131."},
                {"img": "\U0001f4dd", "en": "I wrote a detailed report explaining my methodology, results, and conclusions. I also created charts and graphs to visualize the data.", "tr": "Detayl\u0131 bir rapor yazd\u0131m."},
                {"img": "\U0001f3a4", "en": "On presentation day, I was nervous but prepared. I spoke clearly, showed my data, and answered questions from the judges. They were impressed!", "tr": "Sunum g\u00fcn\u00fc gergindim ama haz\u0131rl\u0131kl\u0131yd\u0131m."},
                {"img": "\U0001f3c6", "en": "I won second place! More importantly, I learned how to conduct research, analyze data, and present findings \u2014 skills I will need in university.", "tr": "\u0130kinci oldum! Ara\u015ft\u0131rma yapmay\u0131 \u00f6\u011frendim."},
            ],
        },
    ],
    "10": [
        {
            "title": "A Gap Year Adventure",
            "icon": "\U0001f30d",
            "color": "#5c6bc0",
            "pages": [
                {"img": "\U0001f5fa\ufe0f", "en": "After finishing high school, my cousin took a gap year. She traveled to five countries in six months and kept a blog about her experiences.", "tr": "Kuzenim liseyi bitirdikten sonra bo\u015f y\u0131l ald\u0131."},
                {"img": "\U0001f1ea\U0001f1f8", "en": "In Spain, she took a two-month language course. She lived with a local family and learned about Spanish culture, food, and traditions.", "tr": "\u0130spanya'da iki ay dil kursu ald\u0131."},
                {"img": "\U0001f1ee\U0001f1f3", "en": "In India, she volunteered at a school for underprivileged children. She taught English and basic computer skills. The children's enthusiasm inspired her.", "tr": "Hindistan'da g\u00f6n\u00fcll\u00fc olarak \u00e7al\u0131\u015ft\u0131."},
                {"img": "\U0001f1ef\U0001f1f5", "en": "Japan fascinated her the most. The combination of ancient traditions and modern technology was incredible. She visited temples and tried sushi.", "tr": "Japonya onu en \u00e7ok etkiledi."},
                {"img": "\U0001f4b0", "en": "She worked part-time in cafes to fund her travels. This taught her budgeting, time management, and cross-cultural communication.", "tr": "Seyahatlerini finanse etmek i\u00e7in kafe ve hostallarda \u00e7al\u0131\u015ft\u0131."},
                {"img": "\U0001f393", "en": "When she returned, she was more mature, confident, and open-minded. She said the gap year was the best education she ever received.", "tr": "D\u00f6nd\u00fc\u011f\u00fcnde daha olgun ve \u00f6zg\u00fcvenli olmu\u015ftu."},
            ],
        },
    ],
    "11": [
        {
            "title": "The Debate That Changed My Mind",
            "icon": "\U0001f3a4",
            "color": "#8e24aa",
            "pages": [
                {"img": "\U0001f4ac", "en": "Our English teacher organized a debate about social media. Half the class argued it was harmful, the other half said it was beneficial. I was on the 'harmful' team.", "tr": "\u0130ngilizce \u00f6\u011fretmenimiz sosyal medya hakk\u0131nda tart\u0131\u015fma d\u00fczenledi."},
                {"img": "\U0001f4f1", "en": "I researched statistics about social media addiction, cyberbullying, and mental health issues. I found studies showing excessive use leads to anxiety.", "tr": "Sosyal medya ba\u011f\u0131ml\u0131l\u0131\u011f\u0131 istatistiklerini ara\u015ft\u0131rd\u0131m."},
                {"img": "\U0001f91d", "en": "During the debate, the other team made excellent points about how social media connects people globally and helps spread awareness about important causes.", "tr": "Tart\u0131\u015fmada di\u011fer tak\u0131m m\u00fckemmel arg\u00fcmanlar sundu."},
                {"img": "\U0001f4a1", "en": "I realized that the truth is somewhere in between. Technology itself is not good or bad \u2014 it depends on how we use it. A valuable lesson in critical thinking.", "tr": "Ger\u00e7e\u011fin ortada bir yerde oldu\u011funu fark ettim."},
                {"img": "\U0001f4dd", "en": "After the debate, I wrote a balanced essay considering both perspectives. My teacher gave me the highest grade and said it showed intellectual maturity.", "tr": "Her iki bak\u0131\u015f a\u00e7\u0131s\u0131n\u0131 de\u011ferlendiren dengeli bir deneme yazd\u0131m."},
                {"img": "\u2b50", "en": "That experience taught me to listen to opposing views before forming my own opinion. In a polarized world, this skill is more important than ever.", "tr": "Bu deneyim kar\u015f\u0131t g\u00f6r\u00fc\u015fleri dinlemeyi \u00f6\u011fretti."},
            ],
        },
    ],
    "12": [
        {
            "title": "My IELTS Journey",
            "icon": "\U0001f4dd",
            "color": "#c62828",
            "pages": [
                {"img": "\U0001f3af", "en": "I decided to take the IELTS exam because I want to study at a university in the UK. My target score was 6.5. I had six months to prepare.", "tr": "IELTS s\u0131nav\u0131na girmeye karar verdim."},
                {"img": "\U0001f4da", "en": "I divided my preparation into four skills: Reading, Writing, Listening, and Speaking. I studied two hours every day and took practice tests every weekend.", "tr": "Haz\u0131rl\u0131\u011f\u0131m\u0131 d\u00f6rt beceriye b\u00f6ld\u00fcm."},
                {"img": "\U0001f4d6", "en": "For Reading, I read English newspapers, magazines, and academic articles. I learned to skim for main ideas and scan for specific information quickly.", "tr": "Reading i\u00e7in \u0130ngilizce gazete ve akademik makaleler okudum."},
                {"img": "\u270d\ufe0f", "en": "Writing was the hardest part. I had to learn to write structured essays with clear introductions, body paragraphs, and conclusions \u2014 all within 40 minutes.", "tr": "Writing en zor k\u0131s\u0131md\u0131."},
                {"img": "\U0001f3a7", "en": "For Listening, I watched podcasts, TED talks, and BBC documentaries. I also practiced with IELTS listening tests to get used to the format.", "tr": "Listening i\u00e7in podcast ve TED talks izledim."},
                {"img": "\U0001f5e3\ufe0f", "en": "Speaking practice was fun. I joined an online speaking club and practiced with students from around the world. We discussed education, technology, and culture.", "tr": "Speaking prati\u011fi e\u011flenceliydim."},
                {"img": "\U0001f3c6", "en": "On exam day, I was calm because I was well-prepared. Two weeks later, I got my score: 7.0! My dream university accepted me!", "tr": "S\u0131nav g\u00fcn\u00fc sakindin. Skor: 7.0! Hayalimdeki \u00fcniversite kabul etti!"},
            ],
        },
    ],
}


def build_flipbook_html(grade: str = "5") -> str:
    """Ortaokul sinif bazli flipbook okuma kitaplari \u2014 Diamond Premium Edition."""
    stories = _FLIPBOOK_STORIES.get(grade, _FLIPBOOK_STORIES["5"])
    stories_json = json.dumps(stories, ensure_ascii=False)

    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!-- font: sistem fontu -->'
        '<style>'
        '*{margin:0;padding:0;box-sizing:border-box}'
        'body{background:linear-gradient(160deg,#060612 0%,#0a0a1a 40%,#0d0d24 100%);'
        'color:#e0e0e0;font-family:"Merriweather",Georgia,serif;min-height:100vh;overflow-x:hidden}'
        'body::before{content:"";position:fixed;inset:0;'
        'background:radial-gradient(ellipse at 20% 50%,rgba(201,168,76,.07),transparent 60%),'
        'radial-gradient(ellipse at 80% 20%,rgba(100,100,255,.04),transparent 50%);'
        'pointer-events:none;z-index:0}'
        '.fb-top{display:flex;align-items:center;justify-content:space-between;'
        'padding:14px 20px;background:linear-gradient(135deg,rgba(201,168,76,.12),rgba(201,168,76,.04));'
        'border-bottom:1px solid rgba(201,168,76,.2);position:relative;z-index:2}'
        '.fb-logo{font-family:"Playfair Display",serif;font-size:1.1rem;font-weight:800;'
        'color:#6366F1;display:flex;align-items:center;gap:8px}'
        '.fb-logo small{font-size:.55em;color:#8a6914;letter-spacing:2px;font-weight:400}'
        '.fb-back{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);'
        'color:#6366F1;padding:6px 14px;border-radius:8px;cursor:pointer;font-size:.8rem;'
        'font-family:inherit;transition:all .2s}'
        '.fb-back:hover{background:rgba(201,168,76,.15)}'
        '.fb-lib{padding:20px;position:relative;z-index:1}'
        '.fb-lib h2{font-family:"Playfair Display",serif;color:#6366F1;font-size:1.3rem;'
        'text-align:center;margin-bottom:20px}'
        '.fb-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}'
        '.fb-card{background:linear-gradient(145deg,rgba(255,255,255,.06),rgba(255,255,255,.02));'
        'border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:24px 20px;'
        'cursor:pointer;transition:all .3s;position:relative;overflow:hidden}'
        '.fb-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;'
        'background:var(--accent);opacity:.6}'
        '.fb-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.4);'
        'border-color:rgba(201,168,76,.3)}'
        '.fb-card .card-icon{font-size:2.8rem;margin-bottom:12px}'
        '.fb-card .card-title{font-family:"Playfair Display",serif;font-size:1.05rem;'
        'color:#e8d48b;font-weight:700;margin-bottom:6px}'
        '.fb-card .card-info{font-size:.75rem;color:#888;line-height:1.5}'
        '.fb-card .card-pages{display:inline-block;background:rgba(201,168,76,.12);color:#6366F1;'
        'padding:3px 10px;border-radius:12px;font-size:.7rem;margin-top:10px}'
        '.fb-reader{padding:16px;position:relative;z-index:1;max-width:720px;margin:0 auto}'
        '.fb-book-title{font-family:"Playfair Display",serif;color:#6366F1;font-size:1.15rem;'
        'text-align:center;margin-bottom:16px}'
        '.fb-page-wrap{perspective:1200px;margin:0 auto;position:relative}'
        '.fb-page{background:linear-gradient(160deg,#1a1a2e,#16162a);'
        'border:1px solid rgba(201,168,76,.15);border-radius:16px;padding:28px 24px;'
        'min-height:380px;position:relative;transition:transform .6s ease;transform-style:preserve-3d}'
        '.fb-page.flip-left{animation:flipLeft .6s ease forwards}'
        '.fb-page.flip-right{animation:flipRight .6s ease forwards}'
        '@keyframes flipLeft{0%{transform:rotateY(0)}50%{transform:rotateY(-15deg)}100%{transform:rotateY(0)}}'
        '@keyframes flipRight{0%{transform:rotateY(0)}50%{transform:rotateY(15deg)}100%{transform:rotateY(0)}}'
        '.fb-page-num{position:absolute;top:12px;right:16px;font-size:.7rem;color:#666;font-style:italic}'
        '.fb-illust{text-align:center;font-size:4rem;margin:12px 0 20px;filter:drop-shadow(0 4px 12px rgba(0,0,0,.3))}'
        '.fb-en{font-size:.95rem;line-height:1.8;color:#d4d4d4;margin-bottom:16px;padding:16px 18px;'
        'background:rgba(201,168,76,.05);border-left:3px solid rgba(201,168,76,.3);border-radius:0 10px 10px 0}'
        '.fb-tr{font-size:.82rem;line-height:1.6;color:#888;padding:12px 18px;'
        'background:rgba(255,255,255,.03);border-radius:10px;border:1px solid rgba(255,255,255,.05)}'
        '.fb-tr::before{content:"\\U0001f1f9\\U0001f1f7 "}'
        '.fb-speak{display:inline-flex;align-items:center;gap:4px;'
        'background:rgba(201,168,76,.12);color:#6366F1;border:1px solid rgba(201,168,76,.2);'
        'padding:5px 12px;border-radius:8px;cursor:pointer;font-size:.75rem;margin-top:10px;'
        'transition:all .2s;font-family:inherit}'
        '.fb-speak:hover{background:rgba(201,168,76,.22)}'
        '.fb-speak.playing{animation:pulse .8s ease infinite}'
        '@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}'
        '.fb-nav{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:20px}'
        '.fb-nav button{background:linear-gradient(135deg,rgba(201,168,76,.15),rgba(201,168,76,.08));'
        'border:1px solid rgba(201,168,76,.25);color:#6366F1;padding:10px 24px;border-radius:10px;'
        'cursor:pointer;font-size:.85rem;font-family:"Merriweather",serif;transition:all .2s}'
        '.fb-nav button:hover:not(:disabled){background:linear-gradient(135deg,rgba(201,168,76,.25),'
        'rgba(201,168,76,.12));transform:translateY(-1px)}'
        '.fb-nav button:disabled{opacity:.3;cursor:not-allowed}'
        '.fb-nav .page-ind{color:#888;font-size:.8rem;min-width:60px;text-align:center}'
        '.fb-prog{height:4px;background:rgba(255,255,255,.06);border-radius:2px;margin:12px 0 0;overflow:hidden}'
        '.fb-prog-fill{height:100%;background:linear-gradient(90deg,#6366F1,#e8d48b);'
        'border-radius:2px;transition:width .4s ease}'
        '.fb-toggle{display:flex;justify-content:center;margin-top:8px}'
        '.fb-toggle label{font-size:.75rem;color:#777;cursor:pointer;display:flex;align-items:center;gap:6px}'
        '.fb-toggle input{accent-color:#6366F1}'
        '</style></head><body>'
        '<div id="fb-app"></div>'
        '<script>'
        '(function(){'
        '"use strict";'
        'var STORIES = ' + stories_json + ';'
        'var ttsVoice=null;'
        'function initTTS(){'
        '  if(!window.speechSynthesis)return;'
        '  function pick(){'
        '    var v=speechSynthesis.getVoices();'
        '    var p=["Google US English","Google UK English Female","Microsoft Zira","Microsoft David","Samantha"];'
        '    for(var i=0;i<p.length;i++){for(var j=0;j<v.length;j++){'
        '      if(v[j].name.indexOf(p[i])!==-1&&v[j].lang.indexOf("en")===0){ttsVoice=v[j];return;}'
        '    }}'
        '    for(var j=0;j<v.length;j++){if(v[j].lang.indexOf("en")===0){ttsVoice=v[j];return;}}'
        '  }'
        '  if(speechSynthesis.getVoices().length)pick();'
        '  speechSynthesis.onvoiceschanged=pick;'
        '}'
        'initTTS();'
        'function speakEN(text){'
        '  if(!window.speechSynthesis)return;'
        '  speechSynthesis.cancel();'
        '  var u=new SpeechSynthesisUtterance(text);'
        '  u.lang="en-US";u.rate=0.8;u.pitch=1.0;u.volume=1.0;'
        '  if(ttsVoice)u.voice=ttsVoice;'
        '  var btns=document.querySelectorAll(".fb-speak");'
        '  btns.forEach(function(b){b.classList.remove("playing");});'
        '  u.onstart=function(){var a=document.querySelector(".fb-speak.active");if(a)a.classList.add("playing");};'
        '  u.onend=function(){btns.forEach(function(b){b.classList.remove("playing");});};'
        '  speechSynthesis.speak(u);'
        '}'
        'var S={screen:"library",storyIdx:0,pageIdx:0,showTR:true};'
        'var $=document.getElementById("fb-app");'
        'function render(){'
        '  if(S.screen==="library")renderLibrary();'
        '  else renderReader();'
        '}'
        'function renderLibrary(){'
        '  var o="<div class=\\"fb-top\\">";'
        '  o+="<div class=\\"fb-logo\\">\\ud83d\\udcda <span>Okuma Kitaplar\\u0131</span> <small>DIAMOND EDITION</small></div>";'
        '  o+="</div>";'
        '  o+="<div class=\\"fb-lib\\">";'
        '  o+="<h2>\\ud83d\\udcd6 Hikaye K\\u00fct\\u00fcphanesi</h2>";'
        '  o+="<div class=\\"fb-grid\\">";'
        '  STORIES.forEach(function(s,i){'
        '    o+="<div class=\\"fb-card\\" style=\\"--accent:"+s.color+"\\" onclick=\\"openStory("+i+")\\">";'
        '    o+="<div class=\\"card-icon\\">"+s.icon+"</div>";'
        '    o+="<div class=\\"card-title\\">"+s.title+"</div>";'
        '    o+="<div class=\\"card-info\\">"+s.pages.length+" sayfa \\u2022 CEFR A2<br>\\u0130ngilizce okuma + T\\u00fcrk\\u00e7e \\u00e7eviri + Sesli dinleme</div>";'
        '    o+="<div class=\\"card-pages\\">\\ud83d\\udcd6 "+s.pages.length+" Sayfa</div>";'
        '    o+="</div>";'
        '  });'
        '  o+="</div></div>";'
        '  $.innerHTML=o;'
        '}'
        'function renderReader(){'
        '  var story=STORIES[S.storyIdx];'
        '  var page=story.pages[S.pageIdx];'
        '  var total=story.pages.length;'
        '  var pct=((S.pageIdx+1)/total*100).toFixed(0);'
        '  var o="<div class=\\"fb-top\\">";'
        '  o+="<button class=\\"fb-back\\" onclick=\\"goLibrary()\\">\\u2190 K\\u00fct\\u00fcphane</button>";'
        '  o+="<div class=\\"fb-logo\\">"+story.icon+" <span>"+story.title+"</span></div>";'
        '  o+="<div style=\\"color:#888;font-size:.75rem\\">"+(S.pageIdx+1)+"/"+total+"</div>";'
        '  o+="</div>";'
        '  o+="<div class=\\"fb-reader\\">";'
        '  o+="<div class=\\"fb-book-title\\">"+story.icon+" "+story.title+"</div>";'
        '  o+="<div class=\\"fb-prog\\"><div class=\\"fb-prog-fill\\" style=\\"width:"+pct+"%\\"></div></div>";'
        '  o+="<div class=\\"fb-page-wrap\\">";'
        '  o+="<div class=\\"fb-page\\" id=\\"fb-page\\">";'
        '  o+="<div class=\\"fb-page-num\\">Sayfa "+(S.pageIdx+1)+" / "+total+"</div>";'
        '  o+="<div class=\\"fb-illust\\">"+page.img+"</div>";'
        '  o+="<div class=\\"fb-en\\">"+page.en+"</div>";'
        '  o+="<button class=\\"fb-speak active\\" onclick=\\"readPage()\\">\\ud83d\\udd0a Dinle</button>";'
        '  if(S.showTR){'
        '    o+="<div class=\\"fb-tr\\" style=\\"margin-top:12px\\">"+page.tr+"</div>";'
        '  }'
        '  o+="</div></div>";'
        '  o+="<div class=\\"fb-toggle\\"><label><input type=\\"checkbox\\" "+(S.showTR?"checked":"")+" onchange=\\"toggleTR(this.checked)\\"> T\\u00fcrk\\u00e7e \\u00e7eviriyi g\\u00f6ster</label></div>";'
        '  o+="<div class=\\"fb-nav\\">";'
        '  o+="<button "+(S.pageIdx<=0?"disabled":"")+" onclick=\\"prevPage()\\">\\u2190 \\u00d6nceki</button>";'
        '  o+="<div class=\\"page-ind\\">"+(S.pageIdx+1)+" / "+total+"</div>";'
        '  o+="<button "+(S.pageIdx>=total-1?"disabled":"")+" onclick=\\"nextPage()\\">Sonraki \\u2192</button>";'
        '  o+="</div>";'
        '  o+="</div>";'
        '  $.innerHTML=o;'
        '}'
        'window.openStory=function(idx){S.storyIdx=idx;S.pageIdx=0;S.screen="reader";render();};'
        'window.goLibrary=function(){if(window.speechSynthesis)speechSynthesis.cancel();S.screen="library";render();};'
        'window.prevPage=function(){'
        '  if(S.pageIdx>0){S.pageIdx--;var p=document.getElementById("fb-page");'
        '  if(p)p.classList.add("flip-right");setTimeout(render,300);}'
        '};'
        'window.nextPage=function(){'
        '  var total=STORIES[S.storyIdx].pages.length;'
        '  if(S.pageIdx<total-1){S.pageIdx++;var p=document.getElementById("fb-page");'
        '  if(p)p.classList.add("flip-left");setTimeout(render,300);}'
        '};'
        'window.toggleTR=function(v){S.showTR=v;render();};'
        'window.readPage=function(){'
        '  var page=STORIES[S.storyIdx].pages[S.pageIdx];'
        '  speakEN(page.en);'
        '};'
        'document.addEventListener("keydown",function(e){'
        '  if(S.screen!=="reader")return;'
        '  if(e.key==="ArrowLeft")window.prevPage();'
        '  else if(e.key==="ArrowRight")window.nextPage();'
        '});'
        'render();'
        '})();'
        '</script></body></html>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# DIJITAL OKUMA KAYNAKLARI — Dis Kutuphane Iframe Embeds
# ══════════════════════════════════════════════════════════════════════════════

_READING_RESOURCES = {
    "preschool": [
        {"title": "StoryWeaver \u2014 Level 1",
         "desc": "Bol g\u00f6rselli, \u00e7ok k\u0131sa ba\u015flang\u0131\u00e7 hikayeleri",
         "icon": "\U0001f4d6", "color": "#4caf50", "level": "Pre-A1",
         "url": "https://storyweaver.org.in/search?level=1&language=English&sort=Relevance"},
        {"title": "StoryWeaver \u2014 Level 2",
         "desc": "Resimli k\u0131sa hikayeler, basit c\u00fcmleler",
         "icon": "\U0001f4da", "color": "#66bb6a", "level": "Pre-A1 / A1",
         "url": "https://storyweaver.org.in/search?level=2&language=English&sort=Relevance"},
        {"title": "Unite for Literacy",
         "desc": "Y\u00fczlerce \u00fccretsiz dijital resimli kitap + sesli anlat\u0131m",
         "icon": "\U0001f4d6", "color": "#2196f3", "level": "Pre-A1",
         "url": "https://www.uniteforliteracy.com/"},
        {"title": "Oxford Owl \u2014 Free eBooks",
         "desc": "\u00c7ocuklar i\u00e7in \u00fccretsiz e-kitap k\u00fct\u00fcphanesi",
         "icon": "\U0001f989", "color": "#9c27b0", "level": "Pre-A1 / A1",
         "url": "https://www.oxfordowl.co.uk/for-home/find-a-book/library-page/"},
        {"title": "British Council Kids \u2014 Short Stories",
         "desc": "K\u0131sa hikayeler + \u00e7\u0131kt\u0131 al\u0131nabilir etkinlikler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/short-stories"},
    ],
    "1": [
        {"title": "British Council Kids \u2014 Short Stories",
         "desc": "\u00c7ocuklara uygun k\u0131sa hikayeler ve okuma etkinlikleri",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/short-stories"},
        {"title": "British Council Kids \u2014 Reading Practice",
         "desc": "Okuma prati\u011fi + interaktif al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/reading-practice"},
        {"title": "StoryWeaver \u2014 Level 2",
         "desc": "A1\u2019e uygun k\u0131sa hikayeler (seviye filtreli)",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A1",
         "url": "https://storyweaver.org.in/search?level=2&language=English&sort=Relevance"},
        {"title": "Unite for Literacy",
         "desc": "Beginner reader resimli kitaplar \u2014 kelime odakl\u0131",
         "icon": "\U0001f4d6", "color": "#2196f3", "level": "Pre-A1 / A1",
         "url": "https://www.uniteforliteracy.com/"},
    ],
    "2": [
        {"title": "British Council Kids \u2014 Short Stories",
         "desc": "\u00c7ocuklara uygun k\u0131sa hikayeler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/short-stories"},
        {"title": "British Council Kids \u2014 Reading Practice",
         "desc": "Okuma prati\u011fi + al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/reading-practice"},
        {"title": "StoryWeaver \u2014 Level 2\u20133",
         "desc": "A1 seviyesine uygun hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A1",
         "url": "https://storyweaver.org.in/search?level=2&level=3&language=English&sort=Relevance"},
        {"title": "Unite for Literacy",
         "desc": "\u00dccretsiz resimli kitaplar",
         "icon": "\U0001f4d6", "color": "#2196f3", "level": "A1",
         "url": "https://www.uniteforliteracy.com/"},
        {"title": "Oxford Owl \u2014 Free eBooks",
         "desc": "\u00c7ocuklar i\u00e7in \u00fccretsiz e-kitap k\u00fct\u00fcphanesi",
         "icon": "\U0001f989", "color": "#9c27b0", "level": "A1",
         "url": "https://www.oxfordowl.co.uk/for-home/find-a-book/library-page/"},
    ],
    "3": [
        {"title": "British Council \u2014 A1 Reading",
         "desc": "A1 seviyesinde k\u0131sa metinler ve al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A1",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/a1-reading"},
        {"title": "British Council Kids \u2014 Short Stories",
         "desc": "\u00c7ocuklara uygun k\u0131sa hikayeler",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/short-stories"},
        {"title": "StoryWeaver \u2014 Level 2\u20133",
         "desc": "A1 seviyesine uygun hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A1",
         "url": "https://storyweaver.org.in/search?level=2&level=3&language=English&sort=Relevance"},
        {"title": "Unite for Literacy",
         "desc": "\u00dccretsiz dijital resimli kitaplar",
         "icon": "\U0001f4d6", "color": "#2196f3", "level": "A1",
         "url": "https://www.uniteforliteracy.com/"},
    ],
    "4": [
        {"title": "British Council \u2014 A1 Reading",
         "desc": "A1 seviyesinde metinler ve g\u00f6revler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A1 / A1+",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/a1-reading"},
        {"title": "British Council Kids \u2014 Reading Practice",
         "desc": "Okuma prati\u011fi + interaktif g\u00f6revler",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A1",
         "url": "https://learnenglishkids.britishcouncil.org/reading-practice"},
        {"title": "StoryWeaver \u2014 Level 3",
         "desc": "A1+ seviyesine uygun hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A1+",
         "url": "https://storyweaver.org.in/search?level=3&language=English&sort=Relevance"},
        {"title": "Oxford Owl \u2014 Free eBooks",
         "desc": "\u00c7ocuklar i\u00e7in \u00fccretsiz e-kitap k\u00fct\u00fcphanesi",
         "icon": "\U0001f989", "color": "#9c27b0", "level": "A1+",
         "url": "https://www.oxfordowl.co.uk/for-home/find-a-book/library-page/"},
    ],
    "5": [
        {"title": "British Council Teens \u2014 A2 Reading",
         "desc": "A2 seviye metinler ve al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A2",
         "url": "https://learnenglishteens.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 A2 Reading",
         "desc": "A2 okuma prati\u011fi (k\u0131sa metinler + g\u00f6revler)",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A2",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "StoryWeaver \u2014 Level 3",
         "desc": "A2 ba\u015flang\u0131\u00e7 hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A2.1",
         "url": "https://storyweaver.org.in/search?level=3&language=English&sort=Relevance"},
        {"title": "ICDL \u2014 Children\u2019s Digital Library",
         "desc": "Ya\u015fa/dile g\u00f6re filtrelenebilen \u00fccretsiz \u00e7ocuk kitaplar\u0131",
         "icon": "\U0001f30d", "color": "#ff9800", "level": "A2",
         "url": "https://childrenslibrary.org/"},
    ],
    "6": [
        {"title": "British Council Teens \u2014 A2 Reading",
         "desc": "A2 seviye metinler ve al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A2",
         "url": "https://learnenglishteens.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 A2 Reading",
         "desc": "A2 okuma prati\u011fi",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A2",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 Story Zone",
         "desc": "A2\u2013B1 i\u00e7in \u00f6zel yaz\u0131lm\u0131\u015f k\u0131sa hikayeler",
         "icon": "\U0001f4d6", "color": "#7b1fa2", "level": "A2 / B1",
         "url": "https://learnenglishteens.britishcouncil.org/study-break/story-zone"},
        {"title": "StoryWeaver \u2014 Level 3\u20134",
         "desc": "A2 seviyesine uygun daha uzun hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A2.2",
         "url": "https://storyweaver.org.in/search?level=3&level=4&language=English&sort=Relevance"},
        {"title": "ICDL \u2014 Children\u2019s Digital Library",
         "desc": "\u00dccretsiz \u00e7ocuk kitaplar\u0131 (online okuma)",
         "icon": "\U0001f30d", "color": "#ff9800", "level": "A2",
         "url": "https://childrenslibrary.org/"},
    ],
    "7": [
        {"title": "British Council Teens \u2014 A2 Reading",
         "desc": "A2 seviye metinler ve g\u00f6revler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A2",
         "url": "https://learnenglishteens.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 Story Zone",
         "desc": "A2\u2013B1 k\u0131sa hikayeler",
         "icon": "\U0001f4d6", "color": "#7b1fa2", "level": "A2 / B1",
         "url": "https://learnenglishteens.britishcouncil.org/study-break/story-zone"},
        {"title": "StoryWeaver \u2014 Level 4",
         "desc": "A2 ileri seviye hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A2.3",
         "url": "https://storyweaver.org.in/search?level=4&language=English&sort=Relevance"},
        {"title": "ICDL \u2014 Children\u2019s Digital Library",
         "desc": "\u00dccretsiz \u00e7ocuk kitaplar\u0131",
         "icon": "\U0001f30d", "color": "#ff9800", "level": "A2",
         "url": "https://childrenslibrary.org/"},
    ],
    "8": [
        {"title": "British Council Teens \u2014 A2 Reading",
         "desc": "A2 seviye metinler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "A2",
         "url": "https://learnenglishteens.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 A2 Reading",
         "desc": "A2 okuma prati\u011fi + g\u00f6revler",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "A2",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/a2-reading"},
        {"title": "British Council \u2014 Story Zone",
         "desc": "A2\u2013B1 hikayeler (9. s\u0131n\u0131fa haz\u0131rl\u0131k)",
         "icon": "\U0001f4d6", "color": "#7b1fa2", "level": "A2 / B1",
         "url": "https://learnenglishteens.britishcouncil.org/study-break/story-zone"},
        {"title": "StoryWeaver \u2014 Level 4",
         "desc": "A2 tamamlama seviyesi hikayeler",
         "icon": "\U0001f4da", "color": "#4caf50", "level": "A2.4",
         "url": "https://storyweaver.org.in/search?level=4&language=English&sort=Relevance"},
        {"title": "ICDL \u2014 Children\u2019s Digital Library",
         "desc": "Ya\u015fa g\u00f6re filtrelenebilen \u00fccretsiz kitaplar",
         "icon": "\U0001f30d", "color": "#ff9800", "level": "A2",
         "url": "https://childrenslibrary.org/"},
    ],
    "9": [
        {"title": "British Council \u2014 B1 Reading",
         "desc": "B1 seviye okuma par\u00e7alar\u0131 ve al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#00897b", "level": "B1",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/b1-reading"},
        {"title": "British Council Teens \u2014 B1 Reading",
         "desc": "Gen\u00e7ler i\u00e7in B1 okuma metinleri",
         "icon": "\U0001f4d6", "color": "#1976d2", "level": "B1",
         "url": "https://learnenglishteens.britishcouncil.org/skills/reading/b1-reading"},
        {"title": "News in Levels \u2014 Level 3",
         "desc": "Ger\u00e7ek haberler B1 seviyesinde",
         "icon": "\U0001f4f0", "color": "#ff9800", "level": "B1",
         "url": "https://www.newsinlevels.com/level/level-3/"},
        {"title": "Breaking News English",
         "desc": "Seviyeli haber metinleri + al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f30d", "color": "#4caf50", "level": "B1",
         "url": "https://breakingnewsenglish.com/"},
        {"title": "StoryWeaver \u2014 Level 4",
         "desc": "B1 seviye uzun hikayeler",
         "icon": "\U0001f4da", "color": "#9c27b0", "level": "B1",
         "url": "https://storyweaver.org.in/search?level=4&language=English&sort=Relevance"},
    ],
    "10": [
        {"title": "British Council \u2014 B1 Reading",
         "desc": "B1 okuma prati\u011fi + g\u00f6revler",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#5c6bc0", "level": "B1",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/b1-reading"},
        {"title": "TED-Ed \u2014 Lessons Worth Sharing",
         "desc": "K\u0131sa e\u011fitici videolar + transkript",
         "icon": "\U0001f393", "color": "#e91e63", "level": "B1-B2",
         "url": "https://ed.ted.com/"},
        {"title": "ReadTheory",
         "desc": "Seviyeye uyarlanm\u0131\u015f okuma al\u0131\u015ft\u0131rmalar\u0131",
         "icon": "\U0001f4d6", "color": "#4caf50", "level": "B1",
         "url": "https://readtheory.org/"},
        {"title": "Newsela",
         "desc": "Ger\u00e7ek haberler farkl\u0131 seviyelerde",
         "icon": "\U0001f4f0", "color": "#2196f3", "level": "B1",
         "url": "https://newsela.com/"},
    ],
    "11": [
        {"title": "British Council \u2014 B1-B2 Reading",
         "desc": "\u0130leri B1 / Ba\u015flang\u0131\u00e7 B2 okuma",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#8e24aa", "level": "B1-B2",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/b1-reading"},
        {"title": "TED Talks \u2014 Transcripts",
         "desc": "TED konu\u015fmalar\u0131 transkriptleri",
         "icon": "\U0001f3a4", "color": "#f44336", "level": "B1-B2",
         "url": "https://www.ted.com/talks"},
        {"title": "Project Gutenberg",
         "desc": "\u00dccretsiz klasik \u0130ngilizce edebiyat",
         "icon": "\U0001f4da", "color": "#795548", "level": "B1-B2",
         "url": "https://www.gutenberg.org/"},
        {"title": "BBC Learning English",
         "desc": "Akademik \u0130ngilizce i\u00e7erikleri",
         "icon": "\U0001f4fb", "color": "#1565c0", "level": "B1-B2",
         "url": "https://www.bbc.co.uk/learningenglish/"},
    ],
    "12": [
        {"title": "IELTS Reading Practice",
         "desc": "IELTS okuma s\u0131nav\u0131 pratik testleri",
         "icon": "\U0001f4cb", "color": "#c62828", "level": "B1-B2",
         "url": "https://www.ielts.org/for-test-takers/sample-test-questions"},
        {"title": "British Council \u2014 B2 Reading",
         "desc": "B2 seviye akademik okuma",
         "icon": "\U0001f1ec\U0001f1e7", "color": "#1565c0", "level": "B2",
         "url": "https://learnenglish.britishcouncil.org/skills/reading/b2-reading"},
        {"title": "Academic Word List",
         "desc": "Akademik kelime listesi + al\u0131\u015ft\u0131rmalar",
         "icon": "\U0001f4dd", "color": "#00897b", "level": "B1-B2",
         "url": "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"},
        {"title": "The Guardian \u2014 Education",
         "desc": "Ger\u00e7ek gazeteden e\u011fitim makaleleri",
         "icon": "\U0001f4f0", "color": "#212121", "level": "B2",
         "url": "https://www.theguardian.com/education"},
        {"title": "VOA Learning English",
         "desc": "Amerikan \u0130ngilizcesi haber ve dersler",
         "icon": "\U0001f310", "color": "#0d47a1", "level": "B1-B2",
         "url": "https://learningenglish.voanews.com/"},
    ],
}


def build_reading_resources_html(grade: str = "5") -> str:
    """Dijital okuma kaynaklari — iframe embed ile dis kutuphane erisimi."""
    resources = _READING_RESOURCES.get(grade, _READING_RESOURCES.get("5", []))
    resources_json = json.dumps(resources, ensure_ascii=False)

    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<!-- font: sistem fontu -->'
        '<style>'
        '*{margin:0;padding:0;box-sizing:border-box}'
        'body{background:linear-gradient(160deg,#060612,#0a0a1a,#0d0d24);'
        'color:#e0e0e0;font-family:"Segoe UI",system-ui,sans-serif;min-height:100vh;overflow-x:hidden}'
        'body::before{content:"";position:fixed;inset:0;'
        'background:radial-gradient(ellipse at 20% 50%,rgba(201,168,76,.06),transparent 60%),'
        'radial-gradient(ellipse at 80% 20%,rgba(100,100,255,.04),transparent 50%);pointer-events:none}'
        '.rr-top{display:flex;align-items:center;justify-content:space-between;'
        'padding:14px 20px;background:linear-gradient(135deg,rgba(201,168,76,.12),rgba(201,168,76,.04));'
        'border-bottom:1px solid rgba(201,168,76,.2);position:relative;z-index:10}'
        '.rr-logo{font-family:"Playfair Display",serif;font-size:1.1rem;font-weight:800;'
        'color:#6366F1;display:flex;align-items:center;gap:8px}'
        '.rr-logo small{font-size:.55em;color:#8a6914;letter-spacing:2px;font-weight:400}'
        '.rr-back{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);'
        'color:#6366F1;padding:6px 14px;border-radius:8px;cursor:pointer;font-size:.8rem;transition:all .2s}'
        '.rr-back:hover{background:rgba(201,168,76,.15)}'
        '.rr-lib{padding:20px;position:relative;z-index:1}'
        '.rr-lib h2{font-family:"Playfair Display",serif;color:#6366F1;font-size:1.2rem;'
        'text-align:center;margin-bottom:6px}'
        '.rr-lib p{text-align:center;color:#777;font-size:.78rem;margin-bottom:18px}'
        '.rr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}'
        '.rr-card{background:linear-gradient(145deg,rgba(255,255,255,.06),rgba(255,255,255,.02));'
        'border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:20px 18px;'
        'cursor:pointer;transition:all .3s;position:relative;overflow:hidden}'
        '.rr-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;'
        'background:var(--clr);opacity:.7}'
        '.rr-card:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(0,0,0,.4);'
        'border-color:rgba(201,168,76,.3)}'
        '.rr-card .c-head{display:flex;align-items:center;gap:12px;margin-bottom:10px}'
        '.rr-card .c-icon{font-size:2rem}'
        '.rr-card .c-title{font-family:"Playfair Display",serif;font-size:.95rem;'
        'color:#e8d48b;font-weight:700;line-height:1.3}'
        '.rr-card .c-desc{font-size:.78rem;color:#999;line-height:1.5;margin-bottom:10px}'
        '.rr-card .c-badge{display:inline-block;background:rgba(201,168,76,.12);color:#6366F1;'
        'padding:2px 10px;border-radius:10px;font-size:.68rem}'
        '.rr-card .c-open{display:inline-block;background:linear-gradient(135deg,rgba(201,168,76,.18),'
        'rgba(201,168,76,.08));color:#6366F1;border:1px solid rgba(201,168,76,.25);'
        'padding:5px 14px;border-radius:8px;font-size:.75rem;margin-top:8px;float:right}'
        '.rr-viewer{position:relative;z-index:1;padding:0}'
        '.rr-iframe{width:100%;height:calc(100vh - 56px);min-height:550px;border:none;'
        'border-radius:0 0 12px 12px;background:#fff}'
        '.rr-loading{display:flex;align-items:center;justify-content:center;height:200px;'
        'color:#888;font-size:.9rem}'
        '.rr-extlink{display:inline-flex;align-items:center;gap:4px;background:rgba(255,255,255,.08);'
        'border:1px solid rgba(255,255,255,.12);color:#90caf9;padding:5px 12px;border-radius:8px;'
        'font-size:.75rem;text-decoration:none;cursor:pointer;transition:all .2s}'
        '.rr-extlink:hover{background:rgba(255,255,255,.15)}'
        '</style></head><body>'
        '<div id="rr-app"></div>'
        '<script>'
        '(function(){'
        '"use strict";'
        'var RES=' + resources_json + ';'
        'var S={screen:"lib",idx:0};'
        'var $=document.getElementById("rr-app");'
        'function render(){'
        '  if(S.screen==="lib")renderLib();'
        '  else renderViewer();'
        '}'
        'function renderLib(){'
        '  var o="<div class=\\"rr-top\\">";'
        '  o+="<div class=\\"rr-logo\\">\\ud83c\\udf10 <span>Dijital Okuma Kaynaklar\\u0131</span> '
        '<small>DIAMOND EDITION</small></div>";'
        '  o+="</div>";'
        '  o+="<div class=\\"rr-lib\\">";'
        '  o+="<h2>\\ud83d\\udcda D\\u0131\\u015f K\\u00fct\\u00fcphane Kaynaklar\\u0131</h2>";'
        '  o+="<p>Uluslararas\\u0131 e\\u011fitim platformlar\\u0131ndan \\u00fccretsiz okuma materyalleri</p>";'
        '  o+="<div class=\\"rr-grid\\">";'
        '  RES.forEach(function(r,i){'
        '    o+="<div class=\\"rr-card\\" style=\\"--clr:"+r.color+"\\" onclick=\\"openRes("+i+")\\">";'
        '    o+="<div class=\\"c-head\\">";'
        '    o+="<div class=\\"c-icon\\">"+r.icon+"</div>";'
        '    o+="<div class=\\"c-title\\">"+r.title+"</div>";'
        '    o+="</div>";'
        '    o+="<div class=\\"c-desc\\">"+r.desc+"</div>";'
        '    o+="<span class=\\"c-badge\\">"+r.level+"</span>";'
        '    o+="<span class=\\"c-open\\">\\u25b6 A\\u00e7</span>";'
        '    o+="</div>";'
        '  });'
        '  o+="</div></div>";'
        '  $.innerHTML=o;'
        '}'
        'function renderViewer(){'
        '  var r=RES[S.idx];'
        '  var o="<div class=\\"rr-top\\">";'
        '  o+="<button class=\\"rr-back\\" onclick=\\"goLib()\\">\\u2190 Kaynaklar</button>";'
        '  o+="<div class=\\"rr-logo\\">"+r.icon+" <span>"+r.title+"</span></div>";'
        '  o+="<a class=\\"rr-extlink\\" href=\\""+r.url+"\\" target=\\"_blank\\">'
        '\\ud83d\\udd17 Yeni sekmede a\\u00e7</a>";'
        '  o+="</div>";'
        '  o+="<div class=\\"rr-viewer\\">";'
        '  o+="<iframe class=\\"rr-iframe\\" src=\\""+r.url+"\\" '
        'sandbox=\\"allow-scripts allow-same-origin allow-popups allow-forms\\" '
        'loading=\\"lazy\\"></iframe>";'
        '  o+="</div>";'
        '  $.innerHTML=o;'
        '}'
        'window.openRes=function(i){S.idx=i;S.screen="viewer";render();};'
        'window.goLib=function(){S.screen="lib";render();};'
        'render();'
        '})();'
        '</script></body></html>'
    )
