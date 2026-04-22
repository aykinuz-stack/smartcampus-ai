"""
SC3D — Üç Boyutlu Egitim Modulu
================================
20 kategori x 20 konu = 400 benzersiz 3D sahne
Three.js prosedural geometri, SmartCampus AI standart format
"""
from __future__ import annotations
import os, json
import streamlit as st
import streamlit.components.v1 as components
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("steam_merkezi")
except Exception:
    pass
from models.sc3d_egitim import SC3DDataStore, SC3DContent
from models.sc3d_scene_info import SCENE_DATA as _EXT_SCENE_DATA
from models._ci24_data import ELEMENTS as _PT_ELEMENTS, ELEMENT_CATS as _PT_CATS
try:
    from models._ci25_data import ILLER as _TR_ILLER, IL_DETAY as _TR_DETAY
except ImportError:
    _TR_ILLER, _TR_DETAY = [], {}
try:
    from models._ci26_data import COG_FEATURES as _COG_FEAT, COG_CATEGORIES as _COG_CATS
except ImportError:
    _COG_FEAT, _COG_CATS = [], {}
try:
    from models._ci27_data import WORLD_COUNTRIES as _WORLD_C, CONTINENT_COLORS as _CONT_CLR
except ImportError:
    _WORLD_C, _CONT_CLR = [], {}
try:
    from models._ci27_geo import COUNTRY_PATHS as _CPATHS
except ImportError:
    _CPATHS = {}
try:
    from models._ci28_data import WORLD_GEO_FEATURES as _WORLD_GEO_FEAT, WORLD_GEO_CATEGORIES as _WORLD_GEO_CATS
except ImportError:
    _WORLD_GEO_FEAT, _WORLD_GEO_CATS = [], {}
try:
    from models._ci31_data import LIDERLER_100 as _LIDERLER_100, LIDER_GRUPLARI as _LIDER_GRUPLARI
except ImportError:
    _LIDERLER_100, _LIDER_GRUPLARI = [], []

# ══════════════════════════════════════════════════════════════
# 20 KATEGORI x 20 KONU
# ══════════════════════════════════════════════════════════════
# (ad, emoji, renk, [20 konu adi])
_CATS = [
    ("Güneş Sistemi", "\U0001f30c", "#FF6B35", [
        "Merkur","Venus","Dünya","Mars","Jupiter",
        "Saturn","Uranus","Neptun","Pluton","Ay",
        "Güneş","Kuyruklu Yildiz","Asteroid Kusagi","Io","Europa",
        "Titan","Ganymede","Samanyolu","Kara Delik","Nebula"]),
    ("Atom Modelleri", "\u269b\ufe0f", "#A855F7", [
        "Hidrojen","Helyum","Lityum","Karbon","Azot",
        "Oksijen","Neon","Sodyum","Demir","Altin",
        "Bakir","Gumus","Uranyum","Kalsiyum","Potasyum",
        "Klor","Fosfor","Kukurt","Silisyum","Titanyum"]),
    ("Hüçre Biyolojisi", "\U0001f9ec", "#22C55E", [
        "Hayvan Hüçresi","Bitki Hüçresi","Bakteri","Mitokondri","Ribozom",
        "Golgi Aygiti","Endoplazmik Retikulum","Lizozom","Hüçre Cekirdegi","Kloroplast",
        "Hüçre Zari","DNA Yapisi","RNA Yapisi","Kromozom","Sentrozom",
        "Vakuol","Peroksizom","Sitoplazma","Hüçre Iskeleti","Vezikul"]),
    ("Insan Anatomisi", "\U0001fac0", "#EC4899", [
        "Kalp","Beyin","Akciger","Karaciger","Bobrek",
        "Mide","Goz","Kulak","Omurga","Kafatasi",
        "El Iskeleti","Dis Yapisi","Kas Sistemi","Sinir Hüçresi","Kemik Doku",
        "Kirmizi Kan Hüçresi","Beyaz Kan Hüçresi","Trombosit","Deri Katmanlari","Sindirim Sistemi"]),
    ("Hayvanlar Alemi", "\U0001f981", "#F59E0B", [
        "Aslan","Kartal","Yunus","Kelebek","Ahtapot",
        "Fil","Penguen","Ari","Yilan","Kaplumbaga",
        "Kanguru","Bukalemun","Flamingo","Kopekbaligi","Papagan",
        "Gergedan","Kurt","Koala","Denizati","Iguana"]),
    ("Dinozorlar", "\U0001f995", "#78716C", [
        "Tyrannosaurus","Triceratops","Stegosaurus","Brontosaurus","Velociraptor",
        "Spinosaurus","Pteranodon","Ankylosaurus","Parasaurolophus","Diplodocus",
        "Allosaurus","Plesiosaurus","Pachycephalosaurus","Dilophosaurus","Iguanodon",
        "Compsognathus","Archaeopteryx","Mosasaurus","Dimetrodon","Megalosaurus"]),
    ("Dünya Coğrafyası", "\U0001f30d", "#10B981", [
        "Volkan","Deprem Fayi","Okyanus","Nehir Deltasi","Col",
        "Buzul","Obruk","Kanyon","Ada","Dag",
        "Plato","Vadi","Magara","Atol","Selale",
        "Gol","Boğaz","Korfez","Yarimada","Ova"]),
    ("Tarihi Yapilar", "\U0001f3db\ufe0f", "#D97706", [
        "Piramit","Kolezyum","Kale","Amfi Tiyatro","Akropol",
        "Köprü","Saat Kulesi","Minare","Kubbe","Kervansaray",
        "Han","Hamam","Cesme","Sur","Kule",
        "Saray","Tapinak","Kilise","Cami","Anit"]),
    ("Geometrik Cisimler", "\U0001f4d0", "#6366F1", [
        "Kup","Kure","Silindir","Koni","Piramit",
        "Prizma","Torus","Dodecahedron","Icosahedron","Octahedron",
        "Tetrahedron","Mobius Seridi","Helis","Elipsoid","Hiperboloid",
        "Paraboloid","Frustum","Torus Dugumu","Kapsul","Yildiz"]),
    ("Fizik Deneyleri", "\u26a1", "#3B82F6", [
        "Sarkac","Kaldirac","Makara","Egik Duzlem","Yay Hareketi",
        "Elektromiknatıs","Tesla Bobini","Dalga Hareketi","Işık Kirilmasi","Mercek",
        "Ayna","Manyetik Alan","Elektrik Alani","Roket Itisi","Jiroskop",
        "Terazi","Pusula","Saat Mekanizmasi","Ses Dalgasi","Sarmal Yay"]),
    ("Kimya Laboratuvari", "\u2697\ufe0f", "#8B5CF6", [
        "Su Molekulu","Karbondioksit","Sodyum Klorur","DNA Sarmal","Benzen Halkasi",
        "Metan","Etanol","Glukoz","Protein Yapisi","Polimer Zinciri",
        "Deney Tupu","Erlenmayer","Buret","Distilasyon","Beher",
        "Santrifuj","Pipet","Bunsen Beki","Kristal Yapi","Amonyak"]),
    ("Uzay Teknolojisi", "\U0001f680", "#EF4444", [
        "Roket","Uzay Mekigi","Uzay Istasyonu","Uydu","Mars Rover",
        "Teleskop","Uzay Kapsulu","Güneş Paneli","Uzay Giysisi","Firlatma Rampasi",
        "Yorunge","Ay Modulu","Uzay Teleskobu","Radyo Anteni","Güneş Yelkeni",
        "Iyon Motoru","Uzay Asansoru","Asteroid Madencisi","Habitat Dome","Uzay Sondasi"]),
    ("Mimari Tasarim", "\U0001f3d7\ufe0f", "#0891B2", [
        "Gokdelen","Villa","Modern Köprü","Stadyum","Havalimani",
        "Tren Istasyonu","Deniz Feneri","Ruzgar Turbini","Güneş Evi","Modern Kule",
        "Muze","Tiyatro","Kutuphane","Hastane","Okul",
        "Park","Marina","Baraj","Sera","Kulube"]),
    ("Mekanik Sistemler", "\u2699\ufe0f", "#64748B", [
        "Disli Cark","Piston","Volan","Kam Mili","Bilyali Yatak",
        "Kayis Kasnak","Zincir Disli","Turbin","Kompresor","Pompa",
        "Hidrolik Silindir","Valf","Yayli Mekanizma","Reduktor","Krank Mili",
        "Biyel Kolu","Supap","Enjektor","Diferansiyel","Amortisor"]),
    ("Elektrik Devreleri", "\U0001f50c", "#0D9488", [
        "LED","Transistor","Kondansator","Direnc","Bobin",
        "Transformator","Elektrik Motoru","Jenerator","Batarya","Güneş Hüçresi",
        "Mikro Cip","Anten","Role","Sigorta","Anahtar",
        "Priz","Osilator","Amplifikator","Filtre Devresi","Sensor"]),
    ("Botanik", "\U0001f33f", "#16A34A", [
        "Çiçek Yapisi","Yaprak","Kok Sistemi","Govde Kesiti","Tohum",
        "Meyve","Mantar","Yosun","Kaktus","Mese Ağaçi",
        "Cam Ağaçi","Palmiye","Egrelti Otu","Orkide","Gul",
        "Papatya","Lale","Ay Ciçegi","Nilufer","Yonca"]),
    ("Jeoloji", "\U0001faa8", "#92400E", [
        "Granit","Mermer","Bazalt","Obsidyen","Kuvars",
        "Ametist","Elmas","Zumrut","Yakut","Safir",
        "Fosil","Stalaktit","Magma Odasi","Sediman Katman","Fay Hatti",
        "Tektonik Plaka","Mineral Yapisi","Kristal Olusumu","Volkanik Kaya","Metamorfik Kaya"]),
    ("Optik ve Işık", "\U0001f4a1", "#FBBF24", [
        "Icbukey Ayna","Disbukey Ayna","Ince Mercek","Kalin Mercek","Prizma",
        "Gokkuşagi","Lazer","Fiber Optik","Mikroskop","Teleskop",
        "Durbun","Kamera Lensi","Kirilma","Yansima","Kirilma Acisi",
        "Polarizasyon","Spektrum","Foton","Dalga Girisimi","Hologram"]),
    ("Deniz Yasami", "\U0001f42c", "#0EA5E9", [
        "Balina","Yunus","Deniz Kaplumbagasi","Büyük Beyaz","Ahtapot",
        "Denizanasi","Mercan","Istiridye","Yengec","Istakoz",
        "Denizyildizi","Denizati","Balon Baligi","Kiliç Baligi","Vatoz",
        "Murekkep Baligi","Deniz Kabugu","Fok","Su Iguana","Penguen"]),
    ("Muzik Aletleri", "\U0001f3b5", "#7C3AED", [
        "Piyano","Gitar","Keman","Davul","Flut",
        "Saksafon","Trompet","Arp","Org","Tambur",
        "Ney","Ud","Kanun","Baglama","Def",
        "Zil","Trombon","Cello","Kontrbas","Klarnet"]),
    ("Bilim Insanlari", "\U0001f52c", "#0369a1", [
        "Einstein","Newton","Tesla","Curie","Darwin",
        "Galileo","Pasteur","Edison","Hawking","Da Vinci",
        "Faraday","Nobel","Archimedes","Copernicus","Kepler",
        "Bohr","Heisenberg","Feynman","Lovelace","Turing"]),
    ("Unlu Ressamlar", "\U0001f3a8", "#be185d", [
        "Leonardo da Vinci","Michelangelo","Van Gogh","Pablo Picasso","Claude Monet",
        "Rembrandt","Salvador Dali","Frida Kahlo","Raphael","Vermeer",
        "Edvard Munch","Gustav Klimt","Caravaggio","Renoir","Cezanne",
        "Kandinsky","Matisse","Botticelli","El Greco","Osman Hamdi Bey"]),
    ("Kasifler ve Kesifler", "\U0001f9ed", "#b45309", [
        "Kristof Kolomb","Marco Polo","Magellan","James Cook","Vasco da Gama",
        "Ibn Battuta","Amundsen","Neil Armstrong","Piri Reis","Zheng He",
        "Livingstone","Hillary ve Norgay","Gagarin","Jacques Cousteau","Leif Erikson",
        "Evliya Celebi","Scott","Drake","Humboldt","Shackleton"]),
    ("Yazarlar ve Eserleri", "\U0001f4da", "#6d28d9", [
        "Shakespeare","Tolstoy","Dostoyevski","Victor Hugo","Franz Kafka",
        "Orhan Pamuk","Yasar Kemal","Nazim Hikmet","Oguz Atay","Sabahattin Ali",
        "Mark Twain","Charles Dickens","Hemingway","Gabriel Garcia Marquez","Albert Camus",
        "Homeros","Cervantes","Goethe","Rumi","Edgar Allan Poe"]),
    ("Periyodik Çizelge", "\U0001f9ea", "#0891b2", ["Periyodik Çizelge"]),
    ("Türkiye İller Haritası", "\U0001f1f9\U0001f1f7", "#dc2626", ["Türkiye İller Haritası"]),
    ("Türkiye Coğrafyası", "\U0001f3d4\ufe0f", "#059669", ["Türkiye Coğrafyası"]),
    ("Dünya Siyasi Haritası", "\U0001f30d", "#0ea5e9", ["Dünya Siyasi Haritası"]),
    ("Dünya Fiziki Haritası", "\U0001f3d4\ufe0f", "#059669", ["Dünya Fiziki Haritası"]),
    ("Dünya Tarihi", "🏛️", "#8B4513", [
        "Kavimler Göçü", "Roma'nın İkiye Bölünmesi", "Batı Roma'nın Yıkılması",
        "Ortaçağ", "Haçlı Seferleri", "İstanbul'un Fethi", "Coğrafi Keşifler",
        "Rönesans ve Reform", "Endüstri Devrimi", "Fransız İhtilali",
        "1. Dünya Savaşı", "2. Dünya Savaşı", "Kurtuluş Savaşı"]),
    ("Büyük İmparatorluklar", "👑", "#DAA520", [
        "Roma İmparatorluğu","Osmanlı İmparatorluğu","Moğol İmparatorluğu",
        "Britanya İmparatorluğu","Pers İmparatorluğu","Bizans İmparatorluğu",
        "Büyük İskender","Han Hanedanlığı","Rus İmparatorluğu","İspanya İmparatorluğu",
        "Abbasi Halifeliği","Emevi Halifeliği","Antik Mısır",
        "Selçuklu İmparatorluğu","Timur İmparatorluğu","Babür İmparatorluğu",
        "Kutsal Roma-Germen","Asur İmparatorluğu","Fransız Sömürge","Portekiz İmparatorluğu"]),
    ("Tarihin 100 Lideri", "🌟", "#C8952E", ["Tarihin 100 Lideri"]),
]

# ══════════════════════════════════════════════════════════════
# SABITLER
# ══════════════════════════════════════════════════════════════
_CLR = {
    "blue": "#2563eb", "dark": "#0f172a", "green": "#10b981",
    "orange": "#f59e0b", "purple": "#8b5cf6", "red": "#ef4444",
    "teal": "#0d9488", "cyan": "#0891b2", "pink": "#ec4899",
    "gray": "#64748b",
}
_DIFF_CLR = {"Kolay": _CLR["green"], "Orta": _CLR["orange"], "Zor": _CLR["red"]}

# ══════════════════════════════════════════════════════════════
# PORTRE + ESER HARITALARI  (ci=20-23: Wikipedia REST API)
# ══════════════════════════════════════════════════════════════
# Portre: Wikipedia article name → fetch thumbnail via REST API
_WIKI = {
    20: [  # Bilim Insanlari
        "Albert_Einstein", "Isaac_Newton", "Nikola_Tesla", "Marie_Curie",
        "Charles_Darwin", "Galileo_Galilei", "Louis_Pasteur", "Thomas_Edison",
        "Stephen_Hawking", "Leonardo_da_Vinci", "Michael_Faraday", "Alfred_Nobel",
        "Archimedes", "Nicolaus_Copernicus", "Johannes_Kepler", "Niels_Bohr",
        "Werner_Heisenberg", "Richard_Feynman", "Ada_Lovelace", "Alan_Turing",
    ],
    21: [  # Ressamlar
        "Leonardo_da_Vinci", "Michelangelo", "Vincent_van_Gogh", "Pablo_Picasso",
        "Claude_Monet", "Rembrandt", "Salvador_Dal\u00ed", "Frida_Kahlo",
        "Raphael", "Johannes_Vermeer", "Edvard_Munch", "Gustav_Klimt",
        "Caravaggio", "Pierre-Auguste_Renoir", "Paul_C\u00e9zanne",
        "Wassily_Kandinsky", "Henri_Matisse", "Sandro_Botticelli",
        "El_Greco", "Osman_Hamdi_Bey",
    ],
    22: [  # Kasifler
        "Christopher_Columbus", "Marco_Polo", "Ferdinand_Magellan", "James_Cook",
        "Vasco_da_Gama", "Ibn_Battuta", "Roald_Amundsen", "Neil_Armstrong",
        "Piri_Reis", "Zheng_He", "David_Livingstone", "Edmund_Hillary",
        "Yuri_Gagarin", "Jacques_Cousteau", "Leif_Erikson",
        "Evliya_%C3%87elebi", "Robert_Falcon_Scott", "Francis_Drake",
        "Alexander_von_Humboldt", "Ernest_Shackleton",
    ],
    23: [  # Yazarlar
        "William_Shakespeare", "Leo_Tolstoy", "Fyodor_Dostoevsky", "Victor_Hugo",
        "Franz_Kafka", "Orhan_Pamuk", "Ya%C5%9Far_Kemal",
        "N%C3%A2z%C4%B1m_Hikmet", "O%C4%9Fuz_Atay", "Sabahattin_Ali",
        "Mark_Twain", "Charles_Dickens", "Ernest_Hemingway",
        "Gabriel_Garc%C3%ADa_M%C3%A1rquez", "Albert_Camus", "Homer",
        "Miguel_de_Cervantes", "Johann_Wolfgang_von_Goethe", "Rumi",
        "Edgar_Allan_Poe",
    ],
}
# Eserler: (wiki_article, turkish_display_name)
_WIKI_WORKS = {
    21: [  # Ressamlar — tablolar
        [("Mona_Lisa","Mona Lisa"),("The_Last_Supper_(Leonardo)","Son Aksam Yemegi"),("Vitruvian_Man","Vitruvius Adami")],
        [("Sistine_Chapel_ceiling","Sistine Sapeli Tavani"),("David_(Michelangelo)","Davut Heykeli")],
        [("The_Starry_Night","Yildizli Gece"),("Sunflowers_(Van_Gogh_series)","Ayçiçekleri")],
        [("Guernica_(Picasso)","Guernica"),("Les_Demoiselles_d%27Avignon","Avignonlu Kizlar")],
        [("Impression,_Sunrise","Izlenim Gundoğumu"),("Water_Lilies_(Monet_series)","Niluferler")],
        [("The_Night_Watch","Gece Devriyesi")],
        [("The_Persistence_of_Memory","Bellegin Azmi")],
        [("The_Two_Fridas","Iki Frida")],
        [("The_School_of_Athens","Atina Okulu"),("Sistine_Madonna","Sistine Meryemi")],
        [("Girl_with_a_Pearl_Earring","Inci Kupeli Kiz"),("The_Milkmaid_(Vermeer)","Sut Doken Kadin")],
        [("The_Scream","Ciglik")],
        [("The_Kiss_(Klimt)","Opüçuk")],
        [("Judith_Beheading_Holofernes_(Caravaggio)","Holofernes'in Basini Kesen Judith")],
        [("Bal_du_moulin_de_la_Galette","Moulin de la Galette Balosu")],
        [("The_Card_Players","Kagit Oyunculari")],
        [("Composition_VIII","Kompozisyon VIII")],
        [("The_Dance_(Matisse)","Dans")],
        [("The_Birth_of_Venus","Venus'un Doğusu")],
        [("The_Burial_of_the_Count_of_Orgaz","Orgaz Kontu'nun Cenazesi")],
        [("The_Tortoise_Trainer","Kaplumbaga Terbiyecisi")],
    ],
    22: [  # Kasifler — kesifler
        [("Voyages_of_Christopher_Columbus","Amerika'nin Kesfi")],
        [("The_Travels_of_Marco_Polo","Doğu Seyahatleri")],
        [("Magellan_expedition","Dünya Turu Seferi")],
        [("Voyages_of_James_Cook","Pasifik Kesifleri")],
        [("Portuguese_discoveries","Hint Deniz Yolu")],
        [("Rihla","Seyahatname")],
        [("South_Pole","Güney Kutbu Seferi")],
        [("Apollo_11","Apollo 11 Ay Yolculugu")],
        [("Piri_Reis_map","Piri Reis Haritasi")],
        [("Treasure_voyages","Deniz Seferleri")],
        [("Zambezi","Afrika Kesifleri")],
        [("1953_British_Mount_Everest_expedition","Everest Tirmanisi")],
        [("Vostok_1","Ilk Uzay Üçusu")],
        [("Aqua-Lung","Denizaltı Kesifleri")],
        [("Norse_colonization_of_North_America","Vinland Kesfi")],
        [("Seyahatname","10 Ciltlik Seyahatname")],
        [("Terra_Nova_expedition","Antarktika Seferi")],
        [("Circumnavigation","Dünya Turu")],
        [("Cosmos:_A_Personal_Voyage","Bilimsel Kesifler")],
        [("Imperial_Trans-Antarctiç_Expedition","Antarktika Dayaniklilik Seferi")],
    ],
    23: [  # Yazarlar — eserler
        [("Hamlet","Hamlet"),("Romeo_and_Juliet","Romeo ve Juliet"),("Macbeth","Macbeth")],
        [("War_and_Peace","Savas ve Baris"),("Anna_Karenina","Anna Karenina")],
        [("Crime_and_Punishment","Süç ve Ceza"),("The_Brothers_Karamazov","Karamazov Kardesler")],
        [("Les_Mis%C3%A9rables","Sefiller"),("The_Hunchback_of_Notre-Dame","Notre Dame'in Kamburu")],
        [("The_Metamorphosis","Dönüşüm"),("The_Trial_(novel)","Dava")],
        [("My_Name_Is_Red","Benim Adim Kirmizi"),("Snow_(Pamuk_novel)","Kar")],
        [("Memed,_My_Hawk","Ince Memed")],
        [("Human_Landscapes_from_My_Country","Memleketimden Insan Manzaralari")],
        [("Tutunamayanlars","Tutunamayanlar")],
        [("Madonna_in_a_Fur_Coat","Kurk Mantolu Madonna")],
        [("Adventures_of_Hüçkleberry_Finn","Hüçkleberry Finn"),("The_Adventures_of_Tom_Sawyer","Tom Sawyer")],
        [("Oliver_Twist","Oliver Twist"),("A_Christmas_Carol","Bir Noel Sarkisi")],
        [("The_Old_Man_and_the_Sea","Yasli Adam ve Deniz"),("A_Farewell_to_Arms","Silahlara Veda")],
        [("One_Hundred_Years_of_Solitude","Yüzyıllik Yalnizlik"),("Love_in_the_Time_of_Cholera","Kolera Gunlerinde Ask")],
        [("The_Stranger_(Camus_novel)","Yabanci"),("The_Plague_(novel)","Veba")],
        [("Iliad","Ilyada"),("Odyssey","Odysseia")],
        [("Don_Quixote","Don Kisot")],
        [("Faust_(Goethe)","Faust"),("The_Sorrows_of_Young_Werther","Genc Werther'in Acilari")],
        [("Masnavi","Mesnevi"),("Diwan-e_Shams-e_Tabrizi","Divan-i Kebir")],
        [("The_Raven","Kuzgun"),("The_Tell-Tale_Heart","Gammaz Yurek")],
    ],
}

# ══════════════════════════════════════════════════════════════
# TUM KATEGORILER BILGI VERITABANI
# _SCENE_INFO[ci][ti] = {baslik, emoji, tanim, seslendirme, özellikler, yapi_bilgileri, ilginc_bilgiler}
# ══════════════════════════════════════════════════════════════
_SCENE_INFO = {}

# ── ci=3: INSAN ANATOMISI ─────────────────────────────────────
_SCENE_INFO[3] = {
    0: {  # Kalp
        "baslik": "İnsan Kalbi",
        "emoji": "\U0001fac0",
        "tanim": "Kalp, göğüsten biraz sola yerleşik, yumruk büyüklüğünde kas yapılı bir organdır. Vücut içindeki tüm kan dolaşımını sağlayan merkezi pompa görevi görür. Günlük ortalama yüz bin kez atar ve yaklaşık yedi bin beş yüz litre kan pompalar.",
        "seslendirme": (
            "İnsan kalbi, yaşamın merkezi motorudur. Göğüsten biraz sola konumlanmış, yumruk büyüklüğünde kas yapılı bir organdır. "
            "Kalp dört odacıktan oluşur: iki üst oda olan atriyumlar ve iki alt oda olan ventriküller. "
            "Sağ atriyum, vücuttan dönen kirli kanı toplar ve sağ ventriküle gönderir. Sağ ventrikül bu kanı akciğerlere pompalar. "
            "Akciğerlerde oksijenlenen kan, sol atriyuma döner. Sol atriyum kanı sol ventriküle iletir. "
            "Sol ventrikül, kalbin en güçlü odasıdır ve oksijenlenmiş kanı aort damarından tüm vücuda pompalar. "
            "Kalp kası, miyokard olarak adlandırılır ve istemsiz çalışır. Yani biz uyurken bile kalp durmadan çalışır. "
            "Kalbin elektrik sistemi, sinüatriyal düğüm tarafından yönetilir. Bu doğal kalp pili saniyede yaklaşık bir buçuk kez uyarı sinyali gönderir. "
            "Koroner arterler kalbin kendi kas dokusunu besleyen damarlardır. Bu damarlar tıkandığında kalp krizi meydana gelir. "
            "Aort, vücudun en büyük atardamarıdır ve kalbin sol ventrikülünden çıkar. "
            "Pulmoner arter ise kanı akciğerlere taşır ve kalbin sağ ventrikülünden çıkar. "
            "Superior vena kava üst vücuttan, inferior vena kava ise alt vücuttan kirli kanı kalbe getirir. "
            "Kalp kapakları kanın tek yönde akmasını sağlar. Dört kapak vardır: mitral, triküspit, aort ve pulmoner kapak. "
            "Bir yetişkin kalbi dakikada ortalama altmış ile yüz arasında atar. Egzersiz sırasında bu sayı yüz seksene çıkabilir. "
            "Kalp günde yaklaşık yüz bin kez atar ve yılda otuz beş milyon kez atar. Bir insan ömrü boyunca kalbi yaklaşık iki buçuk milyar kez atar. "
            "Bebeğin kalbi anne karnında dördüncü haftada atmaya başlar ve doğuma kadar hiç durmaz. "
            "Kalp, vücuttaki en çok çalışan organdır. Bir günde pompaladığı kan ile olimpik bir yüzme havuzunu doldurabilir. "
            "Kalp sağlığını korumak için düzenli egzersiz, dengeli beslenme ve stresten uzak durmak çok önemlidir."
        ),
        "özellikler": [
            ("Ağırlık", "250-350 gram"),
            ("Boyut", "Yumruk büyüklüğünde"),
            ("Günlük Atış", "~100.000 kez"),
            ("Günlük Kan Pompası", "~7.500 litre"),
            ("Oda Sayısı", "4 (2 atriyum + 2 ventrikül)"),
            ("Kapak Sayısı", "4 (mitral, triküspit, aort, pulmoner)"),
            ("Dakikadaki Atış", "60-100 (istirahat)"),
            ("Elektrik Merkezi", "Sinüatriyal düğüm (SA düğüm)"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Sol Atriyum", "Akciğerlerden gelen temiz kanı toplar"),
            ("\U0001f534 Sağ Atriyum", "Vücuttan gelen kirli kanı toplar"),
            ("\U0001f4aa Sol Ventrikül", "En güçlü oda — kanı tüm vücuda pompalar"),
            ("\U0001f4aa Sağ Ventrikül", "Kanı akciğerlere pompalar"),
            ("\U0001f525 Aort", "Vücudun en büyük atardamarı"),
            ("\U0001f535 Pulmoner Arter", "Kanı akciğerlere taşır"),
            ("\U0001f535 Vena Kavalar", "Kirli kanı kalbe getirir"),
            ("\U0001f49b Koroner Arterler", "Kalp kasını besleyen damarlar"),
            ("\U0001f49c Miyokard", "Kalp kas tabakası"),
            ("\U0001f49a Perikard", "Kalbi saran koruyüçu zar"),
        ],
        "ilginc_bilgiler": [
            "Kalp, vücuttan ayrılsa bile kısa süre atmaya devam edebilir çünkü kendi elektrik sistemi vardır.",
            "Kadın kalbi erkek kalbinden biraz daha hızlı atar.",
            "Bir insan ömrü boyunca kalbi yaklaşık 2,5 milyar kez atar.",
            "Kalp krizi en çok pazartesi günleri ve sabah saatlerinde görülür.",
            "Gülmenin kalp sağlığına olumlu etkisi bilimsel olarak kanıtlanmıştır.",
        ],
    },
    1: {  # Beyin
        "baslik": "İnsan Beyni",
        "emoji": "\U0001f9e0",
        "tanim": "Beyin, kafatasının içinde korunan, yaklaşık bir buçuk kilogram ağırlığında, vücudun en karmaşık organıdır. Tüm düşünce, duygu, hareket ve duyusal işlemlerin merkezidir.",
        "seslendirme": (
            "İnsan beyni, evrendeki bilinen en karmaşık yapıdır. Yaklaşık bir buçuk kilogram ağırlığındadır ve kafatasının içinde güvenle korunur. "
            "Beyin yaklaşık seksen altı milyar sinir hücresinden, yani nörondan oluşur. Her nöron binlerce başka nöronla bağlantı kurar. "
            "Beyin iki yarım küreden oluşur: sağ hemisfer ve sol hemisfer. Bu iki yarım küre korpus kallözüm denilen kalın bir sinir demeti ile birbirine bağlanır. "
            "Sol hemisfer genellikle dil, mantık ve analitik düşünme ile ilişkilendirilir. Sağ hemisfer ise yaratıcılık, müzik ve uzaysal algı ile ilgilenir. "
            "Beyin kabuğu, yani korteks, kıvrımlı bir yapıya sahiptir. Bu kıvrımlar sulkus ve girus olarak adlandırılır ve beynin yüzey alanını artırır. "
            "Frontal lob, beynin ön kısmında yer alır ve karar verme, planlama, kişilik gibi üst düzey işlevleri yönetir. "
            "Parietal lob, dokunma, sıcaklık ve ağrı gibi duyusal bilgileri işler. Temporal lob ise işitme ve hafıza ile ilgilenir. "
            "Oksipital lob beynin arka kısmında bulunur ve görme merkezidir. Gözlerden gelen tüm görsel bilgiler burada işlenir. "
            "Serebellum, yani beyincik, beynin arka alt kısmında yer alır. Denge, koordinasyon ve ince motor hareketleri kontrol eder. "
            "Beyin sapı, beyin ile omurilik arasında bağlantı kurar. Nefes alma, kalp atışı ve kan basıncı gibi yaşamsal işlevleri düzenler. "
            "Beyin vücut ağırlığının sadece yüzde ikisini oluşturmasına rağmen, vücuttaki oksijenin yüzde yirmisini tüketir. "
            "Beyin sürekli elektriksel aktivite üretir. Bu aktivite elektroensefalografi, yani EEG ile ölçülebilir. "
            "Nöronlar arası iletişim hem elektriksel hem de kimyasal sinyallerle gerçekleşir. Sinaptik aralıkta nörotransmitterler salınır. "
            "Hipokampüs, beynin derinliklerinde yer alan bir yapıdır ve yeni anıların oluşturulmasında kritik rol oynar. "
            "Amigdala, korku ve duygusal tepkilerden sorumlu olan badem şeklinde küçük bir yapıdır. "
            "Beyin plastisite özelliğine sahiptir, yani yaşam boyu yeni bağlantılar kurabilir ve kendini yenileyebilir. "
            "İnsan beyni, günde yaklaşık yetmiş bin düşünce üretir ve bu düşüncelerin büyük çoğunluğu bilinçaltında gerçekleşir."
        ),
        "özellikler": [
            ("Ağırlık", "~1.400 gram"),
            ("Nöron Sayısı", "~86 milyar"),
            ("Sinaps Sayısı", "~150 trilyon"),
            ("Enerji Tüketimi", "Vücuttaki oksijenin %20'si"),
            ("Hemisfer", "2 (sağ ve sol)"),
            ("Lob Sayısı", "4 (frontal, parietal, temporal, oksipital)"),
            ("Beyin Omurilik Sıvısı", "~150 ml"),
            ("Sinir İletim Hızı", "120 m/s'ye kadar"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7e3 Sol Hemisfer", "Dil, mantık ve analitik düşünme merkezi"),
            ("\U0001f7e3 Sağ Hemisfer", "Yaratıcılık, müzik ve uzaysal algı merkezi"),
            ("\U0001f7e0 Frontal Lob", "Karar verme, planlama ve kişilik"),
            ("\U0001f7e1 Parietal Lob", "Dokunma ve duyusal bilgi işleme"),
            ("\U0001f535 Temporal Lob", "İşitme ve hafıza merkezi"),
            ("\U0001f534 Oksipital Lob", "Görme merkezi"),
            ("\U0001f7e2 Serebellum", "Denge ve koordinasyon"),
            ("\U0001f7e4 Beyin Sapı", "Yaşamsal işlevler: nefes, kalp atışı"),
            ("\U0001f49b Korpus Kallözüm", "İki hemisferi birbirine bağlar"),
            ("\U0001f49c Hipokampüs", "Hafıza oluşturma merkezi"),
        ],
        "ilginc_bilgiler": [
            "Beyin ağrı hissetmez çünkü kendisinde ağrı reseptörü yoktur.",
            "İnsan beyni günde yaklaşık yetmiş bin düşünce üretir.",
            "Beynin yüzde altmışı yağdan oluşur, bu onu vücudun en yağlı organı yapar.",
            "Uyanıkken beyin yaklaşık yirmi watt elektrik üretir, bu küçük bir ampulü yakabilir.",
            "Beyin, yedi dakikadan fazla oksijensiz kalırsa kalıcı hasar oluşmaya başlar.",
        ],
    },
    2: {  # Akciğer
        "baslik": "İnsan Akciğerleri",
        "emoji": "\U0001fac1",
        "tanim": "Akciğerler, göğüs kafesinin içinde yer alan, solunum sisteminin temel organlarıdır. Havadaki oksijeni kana aktarır ve kandan karbondioksiti dışarı atar.",
        "seslendirme": (
            "Akciğerler, yaşam için vazgeçilmez olan solunum organlarıdır. Göğüs kafesinin içinde, kalbin her iki yanında yer alırlar. "
            "Sağ akciğer üç lobdan, sol akciğer ise iki lobdan oluşur. Sol akciğer biraz daha küçüktür çünkü kalbe yer bırakır. "
            "Hava büründan veya ağızdan girerek trakea, yani nefes borusuna ulaşır. Trakea yaklaşık on iki santimetre uzunluğundadır. "
            "Trakea göğüste ikiye ayrılarak sağ ve sol ana bronşları oluşturur. Bronşlar akciğerlere girerek daha küçük dallara ayrılır. "
            "En küçük hava yolları bronşiyol olarak adlandırılır. Bronşiyollerin ucunda alveoller, yani hava kesecikleri bulunur. "
            "İnsan akciğerlerinde yaklaşık üç yüz milyon alveol vardır. Bu alveoller açılsa toplam yüzey alanı bir tenis kortunu kaplar. "
            "Gaz değişimi alveollerde gerçekleşir. Oksijen alveollerden kana geçerken, karbondioksit kandan alveollere geçer. "
            "Bu gaz değişimi difüzyon yoluyla olur ve sadece bir saniyenin dörtte biri kadar sürer. "
            "Diyafram, akciğerlerin altında bulunan kubbe şeklinde bir kastır. Solunumun ana motor kasıdır. "
            "Nefes alırken diyafram kasılarak düzleşir ve akciğerlerin genişlemesine olanak tanır. Nefes verirken gevşer ve kubbe şeklini alır. "
            "Bir yetişkin istirahat halinde dakikada on iki ile yirmi arasında nefes alır. Her nefeste yaklaşık yarım litre hava girer. "
            "Zorlu nefes almada göğüs arası kaslar da devreye girer ve akciğer kapasitesi artar. "
            "Akciğerler plevra zarı ile kaplıdır. Bu zar iki kattan oluşur ve aralarında kayganlaştırıcı sıvı bulunur. "
            "Akciğer kapasitesi yetişkinlerde yaklaşık altı litredir. Ancak normal bir nefeste bunun sadece onda biri kullanılır. "
            "Sigara dumanı akciğerlerdeki silya hücrelerini tahrip eder ve mukuş temizleme mekanizmasını bozar. "
            "Akciğerler sadece solunum yapmaz, aynı zamanda kanın pH dengesini düzenlemede de kritik rol oynar. "
            "Yeni doğan bir bebek ilk nefesini alana kadar akciğerleri sıvı ile doludur. Doğumla birlikte bu sıvı hızla emilir."
        ),
        "özellikler": [
            ("Toplam Ağırlık", "~1.000 gram"),
            ("Alveol Sayısı", "~300 milyon"),
            ("Yüzey Alanı", "~70 m² (tenis kortu)"),
            ("Günlük Nefes", "~20.000 kez"),
            ("Günlük Hava", "~11.000 litre"),
            ("Lob (Sağ/Sol)", "3 / 2"),
            ("Trakea Uzunluğu", "~12 cm"),
            ("Kapasite", "~6 litre (toplam)"),
        ],
        "yapi_bilgileri": [
            ("\U0001f535 Sağ Akciğer", "3 lob — üst, orta ve alt"),
            ("\U0001f535 Sol Akciğer", "2 lob — üst ve alt"),
            ("\U0001f7e4 Trakea", "Hava yolu ana borusu (~12 cm)"),
            ("\U0001f7e0 Ana Bronşlar", "Trakeadan ayrılan sağ ve sol dallar"),
            ("\U0001f7e1 Bronşiyoller", "En küçük hava yolları"),
            ("\U0001f534 Alveoller", "Gaz değişiminin yapıldığı hava kesecikleri"),
            ("\U0001f4aa Diyafram", "Solunumun ana kasıdır"),
            ("\U0001f49c Plevra", "Akciğerleri saran koruyüçu çift zar"),
            ("\U0001f49a Pulmoner Arter", "Kirli kanı akciğerlere taşır"),
            ("\U0001f534 Pulmoner Ven", "Temiz kanı akciğerlerden kalbe taşır"),
        ],
        "ilginc_bilgiler": [
            "Akciğerlerdeki alveollerin toplam yüzey alanı bir tenis kortuna eşittir.",
            "Sağ akciğer sol akciğerden biraz daha büyüktür çünkü kalp sola yaslanmıştır.",
            "Bir insan hayatı boyunca yaklaşık iki yüz elli milyon litre hava solur.",
            "Akciğerler vücuttaki tek organdır ki suya bırakıldığında batar değil yüzer.",
            "Hapşırırken hava saatte yüz altmış kilometreye ulaşabilir.",
        ],
    },
    3: {  # Karaciğer
        "baslik": "İnsan Karaciğeri",
        "emoji": "\U0001fad2",
        "tanim": "Karaciğer, vücudun en büyük iç organıdır. Karın boşluğunun sağ üst kısmında yer alır ve beş yüzden fazla yaşamsal işlevi yerine getirir.",
        "seslendirme": (
            "Karaciğer, insan vücudunun en büyük iç organıdır ve yaşam için vazgeçilmezdir. Karın boşluğunun sağ üst bölgesinde, diyaframın hemen altında yer alır. "
            "Yetişkin bir karaciğer yaklaşık bir buçuk kilogram ağırlığındadır ve köyü kırmızımsı kahverengi bir renktedir. "
            "Karaciğer iki ana lobdan oluşur: büyük sağ lob ve küçük sol lob. Bu loblar falciform ligament adı verilen bağ ile birbirinden ayrılır. "
            "Karaciğer beş yüzden fazla yaşamsal işlev yerine getirir. Bunlar arasında toksinlerin süzülmesi, protein üretimi ve safra salgılanması en önemlileridir. "
            "Safra kesesi, karaciğerin alt yüzeyinde yer alan küçük bir kesedir. Karaciğerin ürettiği safrayı depolar ve gerektiğinde ince bağırsağa salar. "
            "Safra, yağların sindirilmesinde kritik rol oynar. Günde yaklaşık beş yüz ile bin mililitre safra üretilir. "
            "Portal ven, sindirim sisteminden gelen kanı karaciğere taşır. Besinler burada işlenir, zararlı maddeler süzülür. "
            "Hepatik arter ise oksijence zengin kanı karaciğere getirir. Karaciğer çift kan kaynağına sahip nadir organlardan biridir. "
            "Karaciğer, vücuttaki glikoz dengesini düzenler. Fazla gliközü glikojen olarak depolar ve gerektiğinde geri salar. "
            "Albumin ve pıhtılaşma faktörleri gibi önemli proteinler karaciğerde üretilir. "
            "Karaciğer, ilaçların ve alkolün metabolizmasından sorumludur. Zararlı maddeleri parçalayarak vücuttan atılmasını sağlar. "
            "Kolesterol üretiminin büyük kısmı karaciğerde gerçekleşir. Kolesterol hücre zarı yapımı ve hormon üretimi için gereklidir. "
            "Karaciğerin en dikkat çekici özelliği kendini yenileyebilmesidir. Yüzde yetmiş besi alınsa bile birkaç hafta içinde orijinal boyutuna geri dönebilir. "
            "Hepatositler, karaciğerin ana hücreleridir ve karaciğer dokusunun yüzde seksenini oluşturur. "
            "Karaciğer aynı zamanda kan deposu olarak da görev yapar. Vücuttaki toplam kanın yaklaşık yüzde onunu barındırır. "
            "Karaciğer hastalıkları genellikle sessiz ilerler. Sarılık, kaşıntı ve karın şişliği ileri evrelerin belirtileridir. "
            "Sağlıklı bir karaciğer için alkol tüketiminden kaçınmak, dengeli beslenmek ve düzenli egzersiz yapmak önemlidir."
        ),
        "özellikler": [
            ("Ağırlık", "~1.500 gram"),
            ("Lob Sayısı", "2 ana lob (sağ ve sol)"),
            ("İşlev Sayısı", "500+"),
            ("Günlük Safra", "500-1.000 ml"),
            ("Kan Depolama", "Toplam kanın ~%10'u"),
            ("Rejenerasyon", "%75 alınsa bile kendini yeniler"),
            ("Kan Kaynağı", "Çift (portal ven + hepatik arter)"),
            ("Hücre Tipi", "Hepatosit (~%80)"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7e4 Sağ Lob", "Karaciğerin büyük kısmını oluşturur"),
            ("\U0001f7e4 Sol Lob", "Daha küçük, mideye yakın"),
            ("\U0001f7e1 Falciform Ligament", "İki lobu birbirinden ayırır"),
            ("\U0001f7e2 Safra Kesesi", "Safrayı depolar ve salgılar"),
            ("\U0001f535 Portal Ven", "Sindirim organlarından kanı getirir"),
            ("\U0001f534 Hepatik Arter", "Oksijenli kanı karaciğere taşır"),
            ("\U0001f534 Hepatik Venler", "İşlenmiş kanı kalbe gönderir"),
            ("\U0001f49b Safra Kanalları", "Safrayı ince bağırsağa taşır"),
            ("\U0001f49c İnferior Vena Kava", "Alt vücuttan gelen ana toplardamar"),
        ],
        "ilginc_bilgiler": [
            "Karaciğer, vücuttaki tek organ olup kendini tamamen yenileyebilir.",
            "Antik Yunan mitolojisinde Prometheus'un karaciğeri her gece yeniden büyürdü.",
            "Karaciğer dakikada yaklaşık bir buçuk litre kan filtre eder.",
            "Bir bebeğin karaciğeri vücut ağırlığının yüzde besini oluşturur, yetişkinde bu oran yüzde ikidir.",
            "Karaciğer, vücuttaki en sıcak organdır ve yaklaşık kırk derece sıcaklığa sahiptir.",
        ],
    },
    4: {  # Böbrek
        "baslik": "İnsan Böbreği",
        "emoji": "\U0001fac0",
        "tanim": "Böbrekler, belin her iki yanında bulunan fasulye şeklinde organlardır. Kanı filtre ederek atık maddeleri idrar yoluyla vücuttan uzaklaştırır.",
        "seslendirme": (
            "Böbrekler, vücudun doğal filtreleme sistemidir. Belin her iki yanında, omurganın sağında ve solunda birer tane olmak üzere çift olarak bulunurlar. "
            "Her bir böbrek yaklaşık on iki santimetre uzunluğunda ve yüz elli gram ağırlığındadır. Fasulye şekline benzer. "
            "Böbrekler günde yaklaşık yüz seksen litre kanı filtre eder. Ancak bu süzüntünün büyük kısmı geri emilir ve sadece bir buçuk ile iki litre idrar oluşur. "
            "Her böbrekte yaklaşık bir milyon nefron bulunur. Nefronlar böbreğin temel işlevsel birimidir ve filtreleme burada gerçekleşir. "
            "Nefronun başlangıcında glomerül adı verilen kılcal damar yumağı yer alır. Kan burada yüksek basınçla süzülür. "
            "Bowman kapsülü, glomerülü çevreleyen kap şeklinde bir yapıdır ve süzüntüyü toplar. "
            "Proksimal tübül, süzüntüdeki glikoz, amino asitler ve sodyum gibi yararlı maddelerin büyük kısmını geri emer. "
            "Henle kulpu, idrarın yoğunlaştırılmasında rol oynar ve böbreğin iç kısmına doğru uzanır. "
            "Distal tübül ve toplayıcı kanallar, son düzenlemeleri yapar ve idrarı renal pelvise iletir. "
            "Renal pelvis, böbreğin huni şeklindeki merkezi bölgesidir ve idrarı üretere yönlendirir. "
            "Üreter, böbrekten mesaneye uzanan yaklaşık yirmi beş santimetrelik bir kanaldır. "
            "Böbrekler sadece atık filtresi değildir. Kan basıncı düzenleme, kırmızı kan hücresi üretimini uyarma ve D vitamini aktivasyonu da yapar. "
            "Renin hormonu böbreklerden salgılanır ve kan basıncının düzenlenmesinde kritik rol oynar. "
            "Eritropoietin hormonu da böbreklerden salgılanır ve kemik iliğini kırmızı kan hücresi üretmesi için uyarır. "
            "Adrenal bezler, böbreklerin üst kısmında oturur ve kortizol, adrenalin gibi hormonlar üretir. "
            "Böbrek taşları, idrardaki minerallerin kristalleşmesiyle oluşur ve çok şiddetli ağrıya neden olabilir. "
            "Su içmek böbrek sağlığı için çok önemlidir. Günde en az iki litre su tüketmek böbreklerin etkin çalışmasını sağlar."
        ),
        "özellikler": [
            ("Boyut", "~12 x 6 x 3 cm"),
            ("Ağırlık", "~150 gram (her biri)"),
            ("Nefron Sayısı", "~1 milyon (her böbrekte)"),
            ("Günlük Filtrasyon", "~180 litre kan"),
            ("Günlük İdrar", "1,5-2 litre"),
            ("Kan Akışı", "Kalp debisinin ~%25'i"),
            ("Hormon Üretimi", "Renin, Eritropoietin"),
            ("Yapısal Birim", "Nefron"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Renal Korteks", "Böbreğin dış tabakası — glomerüller burada"),
            ("\U0001f7e4 Renal Medülla", "İç bölge — Henle kulpları ve toplayıcı kanallar"),
            ("\U0001f7e1 Renal Pelvis", "Huni şeklinde — idrarı üretere yönlendirir"),
            ("\U0001f535 Üreter", "Böbrekten mesaneye idrar taşır"),
            ("\U0001f534 Renal Arter", "Böbreğe oksijenli kan getirir"),
            ("\U0001f535 Renal Ven", "Filtrelenmiş kanı kalbe döndürür"),
            ("\U0001f7e0 Glomerül", "Kanın süzüldüğü kılcal damar yumağı"),
            ("\U0001f49b Adrenal Bez", "Böbreğin üstünde — hormon üretir"),
            ("\U0001f49c Nefron", "Böbreğin işlevsel birimi"),
        ],
        "ilginc_bilgiler": [
            "Bir insan tek bir böbrekle tamamen sağlıklı yaşayabilir.",
            "Böbrekler günde vücuttaki tüm kanı yaklaşık kırk kez filtre eder.",
            "Her böbrekte yaklaşık bir milyon nefron bulunur, ancak yaşla birlikte bu sayı azalır.",
            "Böbrek nakli en sık yapılan organ naklidir.",
            "Böbrekler saniyede yaklaşık üç buçuk mililitre kan filtre eder.",
        ],
    },
    5: {  # Mide
        "baslik": "İnsan Midesi",
        "emoji": "\U0001f922",
        "tanim": "Mide, karın boşluğunun sol üst kısmında yer alan, J şeklinde kas yapılı bir organdır. Besinlerin mekanik ve kimyasal sindirimini gerçekleştirir.",
        "seslendirme": (
            "Mide, sindirim sisteminin en önemli organlarından biridir. Karın boşluğunun sol üst kısmında yer alır ve J harfine benzer bir şekle sahiptir. "
            "Yemek borusundan gelen besinler mideye kardiya sfinkteri aracılığıyla girer. Bu sfinkter mide asidinin yemek borusuna geri kaçmasını önler. "
            "Mide boş iken yaklaşık elli mililitre hacme sahiptir, ancak yemekten sonra bir buçuk litreye kadar genişleyebilir. "
            "Midenin iç yüzeyi rugae adı verilen kıvrımlarla kaplıdır. Bu kıvrımlar mide genişlediğinde düzleşerek daha fazla alan sağlar. "
            "Mide üç bölgeden oluşur: üstteki fundus, ortadaki gövde ve alttaki antrum. Her bölgenin farklı işlevleri vardır. "
            "Fundus genellikle gaz ve hava biriktirir. Gövde ise asit ve enzimlerin salgılandığı ana bölgedir. "
            "Mide asidi, hidroklorik asit olarak bilinir ve pH değeri bir ile iki arasındadır. Bu kadar asidik bir ortam metalleri bile eritebilir. "
            "Pepsin, midede protein sindirimini başlatan temel enzimdir. İnaktif formu olan pepsinojen, asidik ortamda pepsine dönüşür. "
            "Mide duvarı mukuş tabakasıyla korunur. Bu mukuş tabakası olmasaydı mide kendi kendini sindirir. "
            "Midenin üç kas tabakası vardır: iç oblik, orta sirküler ve dış longitudinal. Bu kaslar besinleri karıştırır ve öğütür. "
            "Mide her yirmi saniyede bir kasılarak besinleri karıştırır. Bu harekete peristaltık hareket denir. "
            "Besinler midede ortalama iki ile dört saat kalır. Yağlı besinler daha uzun süre kalırken, karbonhidratlar daha hızlı geçer. "
            "Pilorus sfinkteri, midenin çıkışında bulunur ve kısmen sindirilmiş besin olan kimusun onikiparmak bağırsağına geçişini kontrol eder. "
            "Mide aynı zamanda B on iki vitamini emilimi için gerekli olan intrinsik faktörü üretir. "
            "Gastrin hormonu mide hücrelerinden salgılanır ve mide asidi üretimini uyarır. "
            "Stres ve düzensiz beslenme mide ülserine yol açabilir. Helicobacter pylori bakterisi de ülserin önemli bir nedenidir. "
            "Mide, vücuttaki en esnek organlardan biridir ve kapasitesini otuz katına kadar artırabilir."
        ),
        "özellikler": [
            ("Boş Hacim", "~50 ml"),
            ("Dolu Hacim", "~1.500 ml"),
            ("Asit pH", "1-2 (çok asidik)"),
            ("Bölge Sayısı", "3 (fundus, gövde, antrum)"),
            ("Kas Tabakası", "3 (oblik, sirküler, longitudinal)"),
            ("Sindirim Süresi", "2-4 saat"),
            ("Günlük Asit", "~1,5 litre HCl"),
            ("Sfinkter", "2 (kardiya ve pilorus)"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Fundus", "Midenin üst kubbe kısmı — gaz biriktirir"),
            ("\U0001f534 Gövde", "Ana bölge — asit ve enzim salgılar"),
            ("\U0001f7e0 Antrum", "Alt bölge — besinleri karıştırır"),
            ("\U0001f7e1 Kardiya Sfinkteri", "Giriş kapağı — reflüyü önler"),
            ("\U0001f7e1 Pilorus Sfinkteri", "Çıkış kapağı — geçişi kontrol eder"),
            ("\U0001f49c Rugae", "İç yüzeydeki kıvrımlar — genişlemeyi sağlar"),
            ("\U0001f7e2 Mukuş Tabakası", "Mideyi kendi asidinden korur"),
            ("\U0001f535 Özofagus", "Yemek borusu — besinleri mideye taşır"),
        ],
        "ilginc_bilgiler": [
            "Mide asidi o kadar güçlüdür ki bir jilet bıçağını eritebilir.",
            "Mide her üç ile dört günde bir mukuş tabakasını tamamen yeniler.",
            "Yüzüstü yatmak sindirim hızını artırır, sırtüstü yatmak ise yavaşlatır.",
            "Mideniz guruldadığında aslında bağırsaklarınız hareket ediyor, mide değil.",
            "Kırmızı etten zengin bir öğünü sindirmek beş saate kadar sürebilir.",
        ],
    },
    6: {  # Göz
        "baslik": "İnsan Gözü",
        "emoji": "\U0001f441\uFE0F",
        "tanim": "Göz, görme duyusunun organıdır. Işığı algılayarak elektriksel sinyallere dönüştürür ve beyne iletir. Yaklaşık yirmi dört milimetre çapında küresel bir yapıdır.",
        "seslendirme": (
            "İnsan gözü, doğanın en mükemmel optik aygıtlarından biridir. Yaklaşık yirmi dört milimetre çapında küresel bir yapıya sahiptir. "
            "Gözün en dış tabakası skleradır. Beyaz sert bir zardır ve gözün şeklini korur. Ön kısımda saydam korneaya dönüşür. "
            "Kornea, ışığın göze girdiği ilk yerdir. Toplam kırılma gücünün üçte ikisini sağlar ve lenssiz bile odaklama yapar. "
            "İris, gözün renkli kısmıdır ve pupillanın boyutunu ayarlayarak göze giren ışık miktarını kontrol eder. "
            "Pupilla, irisin ortasındaki açıklıktır. Karanlıkta genişler, aydınlıkta daralır. Bu refleks otomatik olarak gerçekleşir. "
            "Göz merceği, yani lens, korneanın arkasında yer alır. Siliyer kaslar yardımıyla şeklini değiştirerek yakın ve uzak odaklama yapar. "
            "Vitreus humor, göz küresinin büyük kısmını dolduran jel kıvamında saydam bir maddedir. Gözün şeklini korur. "
            "Retina, gözün en iç tabakasıdır ve ışığa duyarlı hücreleri barındırır. Bir kameranın filmi gibi çalışır. "
            "Retinada iki tür fotoreseptör hücre bulunur: çubuklar ve koniler. Çubuklar loş ışıkta görmeyi, koniler ise renk algısını sağlar. "
            "İnsan gözünde yaklaşık yüz yirmi milyon çubuk ve altı milyon koni hücresi vardır. "
            "Makula, retinanın merkezinde yer alan ve en keskin görüşü sağlayan bölgedir. Okuma ve yüz tanıma gibi işlevlerde kritiktir. "
            "Optik sinir, retinadan gelen elektriksel sinyalleri beynin görme merkezine taşır. Yaklaşık bir milyon sinir lifinden oluşur. "
            "Optik disk, optik sinirin retinadan çıktığı noktadır ve burada fotoreseptör yoktur. Bu nedenle kör nokta olarak bilinir. "
            "Koroid tabaka, retina ile sklera arasında yer alan damar bakımından zengin bir katmandır. Retinanın beslenmesini sağlar. "
            "Gözyaşları sadece duygusal değildir. Gözü nemlendiren, temizleyen ve enfeksiyonlardan koruyan üç farklı gözyaşı tipi vardır. "
            "Göz saniyede elli kez hızlı hareket edebilir ve on milyon farklı renk tonunu ayırt edebilir. "
            "İnsan gözü, karanlığa tam uyum sağlamak için yaklaşık yirmi beş dakikaya ihtiyaç duyar."
        ),
        "özellikler": [
            ("Çap", "~24 mm"),
            ("Ağırlık", "~7,5 gram"),
            ("Çubuk Hücresi", "~120 milyon"),
            ("Koni Hücresi", "~6 milyon"),
            ("Renk Algısı", "~10 milyon ton"),
            ("Görüş Açısı", "~200° (her iki göz)"),
            ("Kırpma", "~15-20 kez/dakika"),
            ("Optik Sinir Lifleri", "~1 milyon"),
        ],
        "yapi_bilgileri": [
            ("\u26aa Sklera", "Beyaz sert dış tabaka — göz şeklini korur"),
            ("\U0001f535 Kornea", "Saydam ön yüzey — ışığı kırar"),
            ("\U0001f7e4 İris", "Renkli halka — pupilla boyutunu ayarlar"),
            ("\u26ab Pupilla", "Işık girişi — büyüklüğü otomatik ayarlanır"),
            ("\U0001f7e1 Lens", "Odaklama — yakın ve uzak görüş"),
            ("\U0001f534 Retina", "Işığa duyarlı iç tabaka — görüntü oluşur"),
            ("\U0001f7e0 Makula", "En keskin görüş merkezi"),
            ("\U0001f7e2 Vitreus Humor", "Göz içi jel — şekli korur"),
            ("\U0001f49b Optik Sinir", "Görüntü sinyallerini beyne taşır"),
            ("\U0001f49c Koroid", "Retinayı besleyen damar tabakası"),
        ],
        "ilginc_bilgiler": [
            "İnsan gözü on milyon farklı renk tonunu ayırt edebilir.",
            "Gözler vücuttaki en hızlı iyileşen organdır — kornea çizikleri kırk sekiz saatte iyileşir.",
            "Göz kırpma refleksi vücuttaki en hızlı kastır, yüz ellinci saniyede tamamlanır.",
            "Her insanın iris deseni parmak izi gibi benzersizdir.",
            "Gözleriniz doğduğunuz günkü boyuttadır, büyümezler.",
        ],
    },
    7: {  # Kulak
        "baslik": "İnsan Kulağı",
        "emoji": "\U0001f442",
        "tanim": "Kulak, işitme ve denge organıdır. Ses dalgalarını algılayıp sinir sinyallerine dönüştürür. Dış kulak, orta kulak ve iç kulak olmak üzere üç bölümden oluşur.",
        "seslendirme": (
            "İnsan kulağı, hem işitme hem de denge duyusunu sağlayan karmaşık bir organdır. Üç ana bölümden oluşur: dış kulak, orta kulak ve iç kulak. "
            "Dış kulak, kulak kepçesi ve kulak kanalından oluşur. Kulak kepçesi ses dalgalarını toplar ve kulak kanalına yönlendirir. "
            "Kulak kepçesi, pinna olarak da bilinir ve kıkırdak yapıdadır. Helix, antihelix, tragus ve lobül gibi bölümlere ayrılır. "
            "Kulak kanalı yaklaşık iki buçuk santimetre uzunluğundadır. İç yüzeyi kıl ve salgı bezleriyle kaplıdır, bunlar kulak kirini üretir. "
            "Kulak kiri, kulağı toz, böcek ve bakterilerden korur. Normalde kendiliğinden dışarı atılır. "
            "Timpanik membran, yani kulak zarı, dış kulak ile orta kulak arasındaki sınırdır. Ses dalgaları zarı titreştirir. "
            "Orta kulak, üç küçük kemikçik içerir: çekiç, örs ve üzengi. Bunlar vücuttaki en küçük kemiklerdir. "
            "Çekiç kulak zarına bağlıdır, örs ortada yer alır, üzengi ise oval pencereye bağlanır. Bu kemikçikler sesi yirmi iki kat güçlendirir. "
            "Östaki borusu, orta kulağı boğaza bağlar. Yutkunma veya esneme sırasında açılarak kulak basıncını dengeler. "
            "İç kulak, koklea ve vestibüler sistem olmak üzere iki ana yapıdan oluşur. "
            "Koklea, salyangöz şeklinde kıvrılmış bir yapıdır ve işitmenin gerçekleştiği bölgedir. İçinde yaklaşık on beş bin tüy hücresi bulunur. "
            "Ses dalgaları koklea içindeki sıvıyı titreştirir. Bu titreşimler tüy hücrelerini uyarır ve elektriksel sinyallere dönüşür. "
            "Vestibüler sistem üç yarım daire kanalı ve iki otolit organdan oluşur. Denge ve baş pozisyonunu algılar. "
            "Yarım daire kanalları birbirine dik üç düzlemde konumlanmıştır. Baş döndüğünde içlerindeki sıvı hareket ederek dönüş algısı oluşturur. "
            "İşitme siniri, yani koklear sinir, kokleadan gelen sinyalleri beynin temporal lobundaki işitme merkezine taşır. "
            "İnsan kulağı yirmi ile yirmi bin hertz arasındaki frekansları duyabilir. Yaşla birlikte yüksek frekansları duyma yeteneği azalır. "
            "Kulak, beynimizin sesleri üç boyutlu olarak konumlandırmasını sağlar. İki kulak arasındaki milisaniye farklar yön algısı oluşturur."
        ),
        "özellikler": [
            ("Bölüm", "3 (dış, orta, iç)"),
            ("Kemikçik", "3 (çekiç, örs, üzengi)"),
            ("Duyma Aralığı", "20-20.000 Hz"),
            ("Koklea Tüy Hücresi", "~15.000"),
            ("Denge Kanalı", "3 yarım daire kanalı"),
            ("Kulak Kanalı", "~2,5 cm"),
            ("Ses Güçlendirme", "22 kat (kemikçikler)"),
            ("En Hassas Frekans", "2.000-5.000 Hz"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7e4 Kulak Kepçesi", "Sesi toplar ve kanala yönlendirir"),
            ("\U0001f7e0 Kulak Kanalı", "Sesi kulak zarına iletir"),
            ("\U0001f534 Kulak Zarı", "Ses dalgalarını titreşime çevirir"),
            ("\U0001f7e1 Çekiç", "Kulak zarına bağlı kemikçik"),
            ("\U0001f7e1 Örs", "Ortadaki kemikçik — sesi iletir"),
            ("\U0001f7e1 Üzengi", "En küçük kemik — oval pencereye bağlı"),
            ("\U0001f535 Koklea", "Salyangöz şekli — işitme merkezi"),
            ("\U0001f7e2 Yarım Daire Kanalları", "Denge algısını sağlar"),
            ("\U0001f49b Östaki Borusu", "Basınç dengelemesi yapar"),
            ("\U0001f49c İşitme Siniri", "Sinyalleri beyne taşır"),
        ],
        "ilginc_bilgiler": [
            "Üzengi kemiği vücudun en küçük kemiğidir, sadece üç milimetre boyundadır.",
            "Kulaklar hiç durmaz — uyurken bile ses dalgalarını algılar, ama beyin bunları filtreler.",
            "İç kulak dengeden de sorumludur, bu yüzden kulak enfeksiyonları baş dönmesine neden olur.",
            "İnsan yüz yirmi desibelin üzerindeki seslere maruz kalırsa kalıcı işitme kaybı yaşayabilir.",
            "Kulak kepçesinin şekli her insanda farklıdır ve parmak izi gibi kimlik tespitinde kullanılabilir.",
        ],
    },
    8: {  # Omurga
        "baslik": "İnsan Omurgası",
        "emoji": "\U0001f9b4",
        "tanim": "Omurga, vücudun ana destek yapısıdır. Otuz üç omurdan oluşur ve S şeklinde bir eğriye sahiptir. İçinden geçen omurilik, beyin ile vücut arasındaki iletişimi sağlar.",
        "seslendirme": (
            "İnsan omurgası, vücudun merkezi destek sütunudur. Otuz üç omurdan oluşur ve doğal bir S eğrisine sahiptir. "
            "Omurga beş bölgeye ayrılır: boyun, göğüs, bel, sakrum ve kuyruk sokumu. Her bölgenin kendine özgü yapısı vardır. "
            "Servikal bölge, yani boyun omurgası, yedi omurdan oluşur. Başın ağırlığını taşır ve boyun hareketlerini sağlar. "
            "İlk boyun omuru atlas adını alır ve başın ileri geri hareketini sağlar. İkinci omur aksis, başın sağa sola dönmesini sağlar. "
            "Torakal bölge, yani göğüs omurgası, on iki omurdan oluşur. Her biri bir çift kaburgaya bağlanır. "
            "Lomber bölge, yani bel omurgası, beş omurdan oluşur. Vücut ağırlığının büyük kısmını taşıdığı için en büyük omurlardır. "
            "Sakrum beş kaynaşmış omurdan oluşur ve pelvis ile bağlantı kurar. Koksiks ise dört kaynaşmış omurdur ve kuyruk sokumu olarak bilinir. "
            "Her omur, bir gövde, bir kemik kanal ve çeşitli çıkıntılardan oluşur. Spinöz çıkıntı arkaya doğru uzanır ve sırtınızda hissedilen çıkıntılardır. "
            "İntervertebral diskler, omurlar arasında yer alan kıkırdak yapılardır. Şok emici görevi görür ve omurganın esnekliğini sağlar. "
            "Disklerin dış kısmı sert anülüs fibrözus, iç kısmı ise yumuşak nükleus pulpözüstan oluşur. Fıtık, iç kısmın dışarı taşmasıdır. "
            "Spinal kord, yani omurilik, omurganın içindeki kanal boyunca uzanır. Beyin ile vücut arasındaki tüm sinir iletişimini sağlar. "
            "Omurilik yaklaşık kırk beş santimetre uzunluğundadır ve birinci lomber omur hizasında sona erer. "
            "Otuz bir çift spinal sinir omurilikten çıkar ve vücudun her bölgesine dağılır. "
            "Omurganın doğal eğrileri şok emme kapasitesini artırır. Lordoz boyun ve belde, kifoz göğüs ve sakrumda görülen eğridir. "
            "Kötü duruş, omurga sağlığını ciddi şekilde etkiler. Uzun süre öne eğik oturmak disk dejenerasyonuna yol açabilir. "
            "Bir insan sabah kalktığında akşama göre yaklaşık bir buçuk santimetre daha uzundur. Gün içinde diskler sıkışarak su kaybeder. "
            "Düzenli egzersiz ve doğru duruş, omurga sağlığını korumanın en etkili yollarıdır."
        ),
        "özellikler": [
            ("Toplam Omur", "33 (7+12+5+5+4)"),
            ("Bölge", "5 (servikal, torakal, lomber, sakral, koksiks)"),
            ("Disk Sayısı", "23 intervertebral disk"),
            ("Omurilik Uzunluğu", "~45 cm"),
            ("Spinal Sinir Çifti", "31 çift"),
            ("Eğri Tipi", "S şekli (lordoz + kifoz)"),
            ("Hareketlilik", "En fazla boyun ve bel"),
            ("İşlev", "Destek, koruma, hareket"),
        ],
        "yapi_bilgileri": [
            ("\U0001f535 Servikal (C1-C7)", "Boyun bölgesi — 7 omur"),
            ("\U0001f7e4 Torakal (T1-T12)", "Göğüs bölgesi — 12 omur"),
            ("\U0001f7e0 Lomber (L1-L5)", "Bel bölgesi — 5 büyük omur"),
            ("\U0001f7e1 Sakrum", "5 kaynaşmış omur — pelvis bağlantısı"),
            ("\U0001f7e1 Koksiks", "4 kaynaşmış omur — kuyruk sokumu"),
            ("\U0001f49c İntervertebral Diskler", "Omurlar arası şok emiciler"),
            ("\U0001f49b Spinal Kord", "Sinir iletişim otoyolu"),
            ("\U0001f534 Spinöz Çıkıntılar", "Sırttan hissedilen kemik çıkıntıları"),
        ],
        "ilginc_bilgiler": [
            "İnsan sabah kalktığında akşama göre yaklaşık bir buçuk santimetre daha uzundur.",
            "Zürafanın da insanla aynı sayıda, yani yedi boyun omuru vardır.",
            "Omurganın toplam esnekliği yüz yirmi dereceye kadar eğilme imkânı tanır.",
            "Omurilik saniyede yüz yirmi metre hızla sinyal iletebilir.",
            "Astronotlar uzayda birkaç santimetre uzar çünkü yerçekimsiz ortamda diskler genişler.",
        ],
    },
    9: {  # Kafatası
        "baslik": "İnsan Kafatası",
        "emoji": "\U0001f480",
        "tanim": "Kafatası, beyni ve yüz yapılarını koruyan kemik bir çerçevedir. Yirmi iki kemikten oluşur: sekiz kranial ve on dört yüz kemiği.",
        "seslendirme": (
            "İnsan kafatası, vücudun en önemli organı olan beyni koruyan sağlam bir kemik yapıdır. "
            "Kafatası toplam yirmi iki kemikten oluşur. Bunların sekizi kraniyum, yani beyin kutusunu, on dördü ise yüz iskeletini oluşturur. "
            "Kraniyum kemikleri frontal, parietal, temporal, oksipital, sfenoid ve etmoid kemiklerdir. "
            "Frontal kemik alnı oluşturur ve ön beyin lobunu korur. Üzerindeki kaş çıkıntıları yüze ifade kazandırır. "
            "İki parietal kemik kafatasının üst ve yan kısımlarını oluşturur. Birbirleriyle sagital sütür ile birleşir. "
            "Temporal kemikler şakak bölgesinde yer alır ve iç kulak yapısını barındırır. "
            "Oksipital kemik kafatasının arka alt kısmında bulunur. Foramen magnum adı verilen büyük delik burada yer alır ve omurilik buradan geçer. "
            "Sfenoid kemik kafatasının tabanında kelebek şeklinde bir kemiktir ve diğer tüm kranial kemiklerle eklem yapar. "
            "Yüz kemikleri arasında en büyüğü mandibula, yani alt çene kemiğidir. Kafatasının tek hareketli kemiğidir. "
            "Maksilla, yani üst çene kemiği, üst diş sırasını barındırır ve bürün tabanını oluşturur. "
            "Zigomatik kemikler elmacık kemikleri olarak bilinir ve yüze karakteristik çıkıntısını verir. "
            "Nazal kemikler bürün köprüsünü oluşturan küçük kemiklerdir. "
            "Orbita, yani göz çukuru, yedi farklı kemiğin bir araya gelmesiyle oluşur ve göz küresini korur. "
            "Kafatası kemikleri sütürler denilen eklemlerle birbirine bağlanır. Bu eklemler hareket etmez ve zamanla kemikleşir. "
            "Yeni doğan bebeklerin kafatasında bıngıldak adı verilen yumuşak alanlar bulunur. Bunlar doğumu kolaylaştırır ve beynin büyümesine olanak tanır. "
            "Ön bıngıldak yaklaşık on sekiz ayda, arka bıngıldak ise iki ile üç ayda kapanır. "
            "Kafatası sadece koruma sağlamaz, aynı zamanda yüz kaslarının tutunma noktası, sinüslerin yuvası ve duygu ifadesinin çerçevesidir."
        ),
        "özellikler": [
            ("Toplam Kemik", "22 (8 kranial + 14 yüz)"),
            ("Hareketli Kemik", "1 (mandibula)"),
            ("Foramen Magnum", "Omuriliğin geçtiği açıklık"),
            ("Sütür", "Kemikleri birleştiren hareketsiz eklemler"),
            ("Sinüs", "4 çift (frontal, maksiller, etmoid, sfenoid)"),
            ("Kalınlık", "~6-7 mm (ortalama)"),
            ("Bıngıldak", "6 adet (yeni doğan)"),
            ("Ağırlık", "~1 kg (mandibula dahil)"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7e1 Frontal Kemik", "Alın — ön beyni korur"),
            ("\U0001f535 Parietal Kemikler", "Kafatasının üst ve yanları"),
            ("\U0001f7e0 Temporal Kemikler", "Şakak — iç kulağı barındırır"),
            ("\U0001f7e4 Oksipital Kemik", "Arka alt — foramen magnum burada"),
            ("\U0001f534 Mandibula", "Alt çene — tek hareketli kemik"),
            ("\U0001f7e1 Maksilla", "Üst çene — üst diş sırası"),
            ("\U0001f49c Zigomatik", "Elmacık kemikleri"),
            ("\U0001f49b Orbita", "Göz çukuru — 7 kemikten oluşur"),
            ("\U0001f7e2 Sfenoid", "Kelebek şekilli taban kemiği"),
        ],
        "ilginc_bilgiler": [
            "Mandibula kafatasının tek hareketli kemiğidir.",
            "Yeni doğan bebeklerin kafatasında altı bıngıldak bulunur, bunlar doğumu kolaylaştırır.",
            "Kafatası kemikleri yetişkinlerde tamamen kaynaşır, ancak bu süreç otuz yaşına kadar sürebilir.",
            "İnsan kafatası bir tondan fazla basınca dayanabilir.",
            "Paranazal sinüsler kafatasını hafifletir ve sesin rezonansına katkıda bulunur.",
        ],
    },
    10: {  # El İskeleti
        "baslik": "İnsan El İskeleti",
        "emoji": "\u270b",
        "tanim": "İnsan eli yirmi yedi kemikten oluşan karmaşık bir yapıdır. Bilek, avuç ve parmak kemiklerini içerir ve insanın en hassas motor becerilerini gerçekleştirmesini sağlar.",
        "seslendirme": (
            "İnsan eli, evrimin en büyük başarılarından biridir. Yirmi yedi kemik, otuzdan fazla kas ve binlerce sinir üçu içerir. "
            "El iskeleti üç bölgeden oluşur: karpal kemikler, yani bilek; metakarpal kemikler, yani avuç; ve falankslar, yani parmak kemikleri. "
            "Karpal bölge sekiz küçük kemikten oluşur. Bu kemikler iki sıra halinde dizilmiştir ve bileğin hareketliliğini sağlar. "
            "Birinci sırada skafoid, lunat, trikuetrum ve pisiform kemikler bulunur. İkinci sırada trapezium, trapezoid, kapitat ve hamat yer alır. "
            "Beş metakarpal kemik avuç içinin iskelet yapısını oluşturur. Her biri bir parmağa karşılık gelir. "
            "Her parmakta üç falanks bulunur: proksimal, orta ve distal. Ancak başparmakta sadece iki falanks vardır: proksimal ve distal. "
            "Toplamda on dört falanks kemiği vardır. Bunlar parmak hareketlerinin temelini oluşturur. "
            "Başparmak, elin en özel parmağıdır. Karşıya gelme hareketi sayesinde nesneleri kavrayabiliriz. Bu yetenek insana özgüdür. "
            "El eklemleri sinoviyal eklemlerdir ve sinoviyal sıvı ile yağlanır. Bu sıvı sürtünmeyi azaltır ve eklem sağlığını korur. "
            "El kasları iki gruba ayrılır: intrinsik kaslar elin içinde, ekstrinsik kaslar ise ön kolda yer alır ve tendonlarla parmakları hareket ettirir. "
            "Karpal tünel, bilek kemikleri ve bağ dokusu arasında oluşan dar bir geçittir. Median sinir ve tendonlar buradan geçer. "
            "El derisi çok hassas dokunma reseptörleri içerir. Parmak uçlarında santimetre kare başına iki bin beş yüze kadar sinir üçu bulunur. "
            "Parmak izleri her insanda farklıdır ve yaşam boyu değişmez. Anne karnında üçüncü ayda oluşmaya başlar. "
            "Elin kavrama gücü yetişkin bir erkekte ortalama kırk kilogram, kadında ise otuz kilogram kadardır. "
            "Tırnaklar parmak uçlarını korur ve ince nesneleri tutmaya yardımcı olur. Ayda yaklaşık üç milimetre uzar. "
            "El, beyin kabuğunun orantısız büyük bir bölümünü kullanır. Homonkülüs modelinde el, vücudun büyük kısmını temsil eder. "
            "İnsan elinin hassasiyeti öylesine yüksektir ki parmak uçları on üç nanometrelik yüzey farklılıklarını bile algılayabilir."
        ),
        "özellikler": [
            ("Toplam Kemik", "27 (8+5+14)"),
            ("Karpal Kemik", "8 (bilek)"),
            ("Metakarpal", "5 (avuç)"),
            ("Falanks", "14 (parmak)"),
            ("Kas Sayısı", "30+ (intrinsik + ekstrinsik)"),
            ("Sinir Üçu", "~2.500/cm² (parmak üçu)"),
            ("Kavrama Gücü", "~40 kg (erkek), ~30 kg (kadın)"),
            ("Eklem Sayısı", "27+ eklem"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7e1 Karpal Kemikler", "8 bilek kemiği — iki sıra halinde"),
            ("\U0001f7e0 Metakarpal Kemikler", "5 avuç kemiği"),
            ("\U0001f534 Proksimal Falanks", "Parmağın ilk kemiği"),
            ("\U0001f534 Orta Falanks", "Parmağın ortası (başparmakta yok)"),
            ("\U0001f534 Distal Falanks", "Parmak üçu kemiği"),
            ("\U0001f49b Başparmak", "2 falanks — karşıya gelme hareketi"),
            ("\U0001f535 Karpal Tünel", "Sinir ve tendonların geçtiği dar geçit"),
            ("\U0001f49c Sinoviyal Eklemler", "Sıvı yağlamalı hareketli eklemler"),
        ],
        "ilginc_bilgiler": [
            "Elin yirmi yedi kemiği vücuttaki toplam kemiklerin yaklaşık dörtte birini oluşturur (iki el toplam elli dört).",
            "Parmakta kas yoktur — parmak hareketleri ön koldaki kaslar tarafından tendonlarla sağlanır.",
            "Başparmağın karşıya gelme hareketi insanı diğer primatlardan ayıran en önemli özelliklerden biridir.",
            "Parmak izleri anne karnında üçüncü ayda oluşur ve hiçbir zaman değişmez.",
            "El beyin kabuğunun orantısız büyük bir bölümünü kullanır — homonkülüs modelinde el çok büyük gösterilir.",
        ],
    },
    11: {  # Diş Yapısı
        "baslik": "İnsan Diş Yapısı",
        "emoji": "\U0001f9b7",
        "tanim": "Diş, ağız boşluğunda çene kemiklerine gömülü sert yapılardır. Besinlerin mekanik sindiriminin ilk adımını gerçekleştirir. Yetişkinde otuz iki kalıcı diş bulunur.",
        "seslendirme": (
            "Dişler, sindirim sisteminin giriş kapısıdır ve besinlerin mekanik olarak parçalanmasını sağlar. "
            "Bir yetişkinin ağzında otuz iki kalıcı diş bulunur. Bunlar kesiçi, köpek, küçük azı ve büyük azı dişleri olarak gruplandırılır. "
            "Her diş iki ana bölümden oluşur: taç ve kök. Taç, diş etinin üzerinde görünen kısımdır. Kök ise çene kemiğinin içine gömülüdür. "
            "Diş minesi, tacı kaplayan beyaz sert tabakadır ve insan vücudundaki en sert dokudur. Yüzde doksan altısı minerallerden oluşur. "
            "Mine tabakasının altında dentin bulunur. Dentin, kemikten daha sert ancak mineden daha yumuşaktır ve dişin büyük kısmını oluşturur. "
            "Dentinin içinde pulpa odası yer alır. Pulpa, kan damarları ve sinirler içeren canlı bir dokudur. Dişin beslenmesini ve duyusunu sağlar. "
            "Diş kökü sementum adı verilen ince bir kemik benzeri tabaka ile kaplıdır. "
            "Periodontal ligament, kökü çevreleyen ve dişi çene kemiğine bağlayan bağ dokusudur. Çiğneme sırasında şok emici görevi görür. "
            "Diş eti, yani gingiva, dişlerin çevresini saran pembe yumuşak dokudur. Sağlıklı diş eti açık pembe renktedir ve kanamaz. "
            "Alveolar kemik, dişlerin gömülü olduğu çene kemiği bölgesidir. Diş kaybı bu kemiğin erimesine yol açabilir. "
            "Kesiçi dişler ön tarafta yer alır ve besinleri kesmek için kullanılır. Üstte dört, altta dört olmak üzere sekiz tanedir. "
            "Köpek dişleri, sivri yapılarıyla yırtma işlevini görür. Toplamda dört adet bulunur. "
            "Küçük azı dişleri, yani premolarlar, sekiz tanedir ve besinleri ezmek ile öğütmek için kullanılır. "
            "Büyük azı dişleri, yani molarlar, on iki tanedir ve en güçlü çiğneme yüzeyine sahiptir. "
            "Yirmi yaş dişleri, üçüncü büyük azı dişleridir ve genellikle on yedi ile yirmi beş yaş arasında çıkar. "
            "Süt dişleri yirmi tanedir ve altı aylıktan itibaren çıkmaya başlar. Altı yaşından itibaren kalıcı dişlerle değiştirilir. "
            "Dişlerin sağlığını korumak için günde en az iki kez fırçalamak, diş ipi kullanmak ve düzenli diş hekimi kontrolü yaptırmak gerekir."
        ),
        "özellikler": [
            ("Kalıcı Diş", "32 adet"),
            ("Süt Dişi", "20 adet"),
            ("Diş Tipi", "4 (kesiçi, köpek, premolar, molar)"),
            ("Mine Sertliği", "Mohs skalası 5 (vücudun en sert dokusu)"),
            ("Mine Mineral", "%96 hidroksiapatit"),
            ("Kök Sayısı", "1-3 (dişe göre değişir)"),
            ("Çiğneme Gücü", "~70 kg (molar bölgesi)"),
            ("İlk Süt Dişi", "~6. ay"),
        ],
        "yapi_bilgileri": [
            ("\u26aa Mine", "En dış tabaka — vücudun en sert dokusu"),
            ("\U0001f7e1 Dentin", "Mine altındaki kemik benzeri tabaka"),
            ("\U0001f534 Pulpa", "Damar ve sinir içeren canlı iç doku"),
            ("\U0001f7e4 Sementum", "Kökü kaplayan ince kemik tabakası"),
            ("\U0001f49c Periodontal Ligament", "Dişi kemiğe bağlayan bağ dokusu"),
            ("\U0001f7e0 Diş Eti", "Dişleri çevreleyen koruyüçu yumuşak doku"),
            ("\U0001f535 Alveolar Kemik", "Dişlerin gömülü olduğu çene kemiği"),
            ("\U0001f49b Kök Kanalı", "Pulpanın kök içindeki bölümü"),
        ],
        "ilginc_bilgiler": [
            "Diş minesi insan vücudundaki en sert dokudur, elmasa yakın sertliktedir.",
            "Bir insanın diş izi parmak izi gibi benzersizdir.",
            "Tükürük günde yaklaşık bir litre üretilir ve dişleri asit saldırılarından korur.",
            "Dişler fosil olarak milyonlarca yıl korunabilir çünkü mine çok dayanıklıdır.",
            "Ortalama bir insan hayatı boyunca yaklaşık otuz sekiz gününü diş fırçalayarak geçirir.",
        ],
    },
    12: {  # Kas Sistemi
        "baslik": "İnsan Kas Sistemi",
        "emoji": "\U0001f4aa",
        "tanim": "Kas sistemi, vücudun hareket etmesini sağlayan dokulardan oluşur. İnsan vücudunda altı yüzden fazla iskelet kası bulunur ve vücut ağırlığının yaklaşık yüzde kırkını oluşturur.",
        "seslendirme": (
            "İnsan kas sistemi, vücudun hareket motorudur. Altı yüzden fazla iskelet kası ile donatılmıştır. "
            "Kaslar vücut ağırlığının yaklaşık yüzde kırkını oluşturur. Üç ana kas tipi vardır: iskelet kası, düz kas ve kalp kası. "
            "İskelet kasları, kemiklere tendonlarla bağlı olan çizgili kaslardır. İrademizle kontrol edilir ve hareketi sağlar. "
            "Düz kaslar, iç organların duvarlarında bulunur. Sindirim, solunum ve dolaşım sistemi organlarında çalışır. İstemsiz çalışır. "
            "Kalp kası, miyokard olarak bilinir ve sadece kalpte bulunur. Hem çizgili hem de istemsiz çalışma özelliği taşır. "
            "Bir kas hücresine miyosit denir. Miyositler miyofibriller içerir ve miyofibriller aktin ve miyozin proteinlerinden oluşur. "
            "Kasılma, aktin ve miyozin filamentlerinin birbiri üzerinde kaymasıyla gerçekleşir. Buna kayan filament teorisi denir. "
            "Kaslar çiftler halinde çalışır: agonist ve antagonist. Örneğin biseps kolun bükülmesini, triseps ise açılmasını sağlar. "
            "Biseps kası ön kolda yer alır ve dirseğin bükülmesinde ana kas olarak çalışır. İki başlı bir kastır. "
            "Bir kas lifinin yapısı katman katmandır: epimisyum en dışta tüm kası, perimisyum kas demetlerini, endomisyum ise tek tek lifleri sarar. "
            "Tendonlar, kasları kemiklere bağlayan güçlü bağ dokularıdır. Kolajen liflerden oluşur ve çok dayanıklıdır. "
            "Fasya, kasları saran saydam zardır. Kaslar arasında kayganlaştırıcı ve koruyüçu görev görür. "
            "Motor nöronlar, beyinden gelen kasılma sinyallerini kaslara iletir. Her motor nöron birçok kas lifini kontrol eder. "
            "Nöromüsküler kavşak, sinir ile kas lifinin buluştuğu noktadır. Burada asetilkolin nörotransmitteri salınarak kasılma tetiklenir. "
            "Kaslar enerjilerinin büyük kısmını ATP molekülünden alır. Yoğun egzersizde laktik asit birikimi kas yorgunluğuna neden olur. "
            "Vücudun en büyük kası gluteus maximus, yani kalça kasıdır. En küçüğü ise kulaktaki stapedius kasıdır. "
            "Düzenli egzersiz kas liflerini kalınlaştırır, dayanıklılığı artırır ve genel sağlığı iyileştirir."
        ),
        "özellikler": [
            ("İskelet Kası", "600+ adet"),
            ("Vücut Ağırlık Oranı", "~%40"),
            ("Kas Tipi", "3 (iskelet, düz, kalp)"),
            ("En Büyük Kas", "Gluteus maximus (kalça)"),
            ("En Küçük Kas", "Stapedius (kulak)"),
            ("En Güçlü Kas", "Masseter (çene)"),
            ("Enerji Kaynağı", "ATP"),
            ("Protein Yapısı", "Aktin ve miyozin"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Kas Karnı", "Kasın şişkin, kasılan bölgesi"),
            ("\u26aa Tendon", "Kası kemiğe bağlayan bağ dokusu"),
            ("\U0001f7e4 Epimisyum", "Tüm kası saran en dış zar"),
            ("\U0001f7e0 Perimisyum", "Kas demetlerini saran zar"),
            ("\U0001f7E1 Endomisyum", "Tek kas lifini saran zar"),
            ("\U0001f535 Miyofibril", "Kas hücresi içindeki kasılan yapı"),
            ("\U0001f49c Fasya", "Kasları saran saydam koruyüçu zar"),
            ("\U0001f49b Nöromüsküler Kavşak", "Sinir-kas bağlantı noktası"),
        ],
        "ilginc_bilgiler": [
            "Gülümsemek on yedi kas kullanır, kaş çatmak ise kırk üç kas gerektirir.",
            "Diliniz tamamen kastan oluşan ve kemiğe bağlı olmayan tek kastır.",
            "Vücuttaki en hızlı kas göz çevresindeki orbikülaris okülidir — gözü saniyenin beşte birinde kırpar.",
            "Kaslar sadece çekebilir, itemez. Bu yüzden her zaman çiftler halinde çalışır.",
            "Bir adım atmak için iki yüzden fazla kas aynı anda koordineli çalışır.",
        ],
    },
    13: {  # Sinir Hücresi
        "baslik": "Sinir Hücresi (Nöron)",
        "emoji": "\u26a1",
        "tanim": "Nöron, sinir sisteminin temel yapı taşıdır. Elektriksel ve kimyasal sinyallerle bilgi ileten özelleşmiş hücrelerdir. İnsan vücudunda yaklaşık seksen altı milyar nöron bulunur.",
        "seslendirme": (
            "Nöronlar, sinir sisteminin temel işlevsel birimleridir. Vücuttaki en özelleşmiş hücreler arasında yer alır. "
            "İnsan beyninde yaklaşık seksen altı milyar nöron bulunur. Her nöron binlerce başka nöronla sinaptik bağlantı kurar. "
            "Bir nöron üç ana bölümden oluşur: soma yani hücre gövdesi, dendritler ve akson. "
            "Soma, nöronun kontrol merkezidir. Çekirdek burada yer alır ve hücrenin metabolik işlevlerini yönetir. "
            "Dendritler, soma'dan dışarı uzanan kısa, dallanmış yapılardır. Diğer nöronlardan gelen sinyalleri alır ve soma'ya iletir. "
            "Her nöronun genellikle çok sayıda dendriti olabilir. Dendritlerde bulunan dikensi çıkıntılar sinaptik bağlantı noktalarını artırır. "
            "Akson, nöronun uzun tek uzantısıdır. Sinyalleri soma'dan uzağa, diğer nöronlara veya hedef dokulara iletir. "
            "Aksonlar birkaç milimetreden bir metreye kadar uzanabilir. Omuriliğin alt kısmından ayak parmağına giden akson en uzunudur. "
            "Miyelin kılıfı, aksonun çevresini saran yağlı bir tabakadır. Schwann hücreleri tarafından oluşturulur ve sinir iletimini hızlandırır. "
            "Ranvier düğümleri, miyelin kılıfının kesintiye uğradığı noktalardır. Sinir impulsu bu düğümler arasında atlayarak çok hızlı ilerler. "
            "Bu atlayıcı iletim sayesinde miyelinli nöronlarda sinyal hızı saniyede yüz yirmi metreye kadar çıkabilir. "
            "Akson terminalleri, aksonun ucundaki düğme şeklinde yapılardır. Burada nörotransmitter maddeleri depolanır. "
            "Sinaps, bir nöronun akson terminali ile diğer nöronun dendriti arasındaki bağlantı bölgesidir. "
            "Sinaptik aralıkta nörotransmitterler salınır. Asetilkolin, dopamin, serotonin ve noradrenalin en önemli nörotransmitterlerdir. "
            "Nöronlar üç tipe ayrılır: duyusal nöronlar bilgiyi beyne taşır, motor nöronlar kaslara komut gönderir, ara nöronlar ise bağlantı kurar. "
            "Aksiyon potansiyeli, nöronun ateşlenmesi sırasında oluşan elektriksel sinyaldir. Ya hep ya hiç kuralına göre çalışır. "
            "Nöroplastisite, beynin yeni sinaptik bağlantılar kurarak kendini yenileme yeteneğidir. Öğrenme ve hafıza bu sayede mümkün olur."
        ),
        "özellikler": [
            ("Beyindeki Nöron", "~86 milyar"),
            ("Sinaps Sayısı", "~150 trilyon"),
            ("İletim Hızı", "120 m/s'ye kadar"),
            ("Nöron Tipi", "3 (duyusal, motor, ara)"),
            ("Akson Uzunluğu", "mm'den 1m'ye kadar"),
            ("Nörotransmitter", "100+ farklı tür"),
            ("Enerji Tüketimi", "Beyin enerjisinin %20'si"),
            ("Sinaptik Gecikme", "~0,5 ms"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7E0 Soma", "Hücre gövdesi — çekirdek ve organeller burada"),
            ("\U0001f7E2 Dendritler", "Sinyal alan dallanmış uzantılar"),
            ("\U0001f535 Akson", "Sinyal ileten uzun tek uzantı"),
            ("\u26aa Miyelin Kılıfı", "Aksonu saran yalıtım tabakası"),
            ("\U0001f534 Ranvier Düğümleri", "Miyelin boşlukları — atlayıcı iletim"),
            ("\U0001f7E1 Akson Terminalleri", "Nörotransmitter salan uç düğmeler"),
            ("\U0001f49c Sinaps", "Nöronlar arası bağlantı bölgesi"),
            ("\U0001f49b Schwann Hücreleri", "Miyelin üreten destek hücreleri"),
            ("\U0001f7E4 Çekirdek", "DNA içeren soma'nın merkezi"),
        ],
        "ilginc_bilgiler": [
            "Beyndeki nöronların toplam uzunluğu uç üça eklenirse yaklaşık seksen bin kilometre eder.",
            "Bir nöron saniyede bin kez ateşlenebilir.",
            "Yetişkin beyninde bazı bölgelerde yeni nöron üretimi devam eder, buna nörogenez denir.",
            "En hızlı sinir impulsu saatte dört yüz otuz kilometre hıza ulaşabilir.",
            "Beyindeki sinaptik bağlantı sayısı galaksideki yıldız sayısından fazladır.",
        ],
    },
    14: {  # Kemik Doku
        "baslik": "İnsan Kemik Dokusu",
        "emoji": "\U0001f9b4",
        "tanim": "Kemik, vücudun sert destek yapısını oluşturan canlı bir dokudur. Yetişkin bir insanda iki yüz altı kemik bulunur. Kemikler koruma, hareket, mineral depolama ve kan hücresi üretimi işlevlerini yerine getirir.",
        "seslendirme": (
            "Kemik, canlı ve sürekli yenilenen dinamik bir dokudur. Yetişkin bir insanda iki yüz altı kemik bulunur. "
            "Kemik dokusu iki ana tipten oluşur: kompakt kemik ve süngerimsi kemik. Her ikisi de aynı kemikte birlikte bulunabilir. "
            "Kompakt kemik, kemiğin dış kısmını oluşturan yoğun ve sert tabakadır. Kemiğin gücünü ve dayanıklılığını sağlar. "
            "Süngerimsi kemik, iç kısımda bulunan gözenekli yapıdır. Hafiflik sağlar ve kemik iliğini barındırır. "
            "Uzun kemikler, örneğin femur, bir gövde ve iki uçtan oluşur. Gövdeye diyafiz, uçlara ise epifiz denir. "
            "Periosteum, kemiğin dış yüzeyini kaplayan ince ancak dayanıklı bir zardır. Kemik büyümesi ve onarımında rol oynar. "
            "Endosteum, kemik iliği boşluğunun iç yüzeyini kaplayan ince bir zardır. "
            "Havers kanalları, kompakt kemik içinde uzunlamasına uzanan küçük kanallardır. İçlerinde kan damarları ve sinirler bulunur. "
            "Havers sistemi veya osteon, kompakt kemiğin yapısal birimidir. Konsantrik lameller halinde Havers kanalını çevreler. "
            "Osteositler, olgun kemik hücreleridir ve lakunalar denilen küçük boşluklarda yaşar. "
            "Osteoblastlar, yeni kemik dokusu üreten hücrelerdir. Kalsiyum ve fosfor mineralleriyle kemik matriksini oluştururlar. "
            "Osteoklastlar, eski veya hasarlı kemik dokusunu yıkan hücrelerdir. Bu süreç kemik yenilenmesi için gereklidir. "
            "Kemik iliği iki türdür: kırmızı ilik kan hücresi üretir, sarı ilik ise yağ depolar. "
            "Kırmızı kemik iliği, vücuttaki tüm kırmızı kan hücrelerini, beyaz kan hücrelerinin çoğunu ve trombositleri üretir. "
            "Kemikler kalsiyum ve fosfor gibi minerallerin ana deposudur. Vücuttaki kalsiyumun yüzde doksan dokuzu kemiklerde bulunur. "
            "Eklem kıkırdağı, kemik uçlarını kaplayan düz ve kaygan bir dokudur. Sürtünmeyi azaltır ve şok emici olarak çalışır. "
            "Kemikler hayat boyu yenilenir. Yetişkin bir insanda kemik dokusu yaklaşık on yılda bir tamamen yenilenir."
        ),
        "özellikler": [
            ("Toplam Kemik", "206 (yetişkin)"),
            ("Bebek Kemik", "~270 (bazıları kaynaşır)"),
            ("En Uzun Kemik", "Femur (uyluk)"),
            ("En Küçük Kemik", "Üzengi (kulak)"),
            ("Kemik Tipi", "2 (kompakt, süngerimsi)"),
            ("Kalsiyum Deposu", "Vücuttaki kalsiyumun %99'u"),
            ("Yenilenme Süresi", "~10 yıl"),
            ("Dayanıklılık", "Betondan 4 kat güçlü"),
        ],
        "yapi_bilgileri": [
            ("\u26aa Kompakt Kemik", "Yoğun dış tabaka — güç ve dayanıklılık"),
            ("\U0001f7E1 Süngerimsi Kemik", "Gözenekli iç yapı — hafiflik"),
            ("\U0001f534 Kırmızı Kemik İliği", "Kan hücresi üretim merkezi"),
            ("\U0001f7E1 Sarı Kemik İliği", "Yağ deposu"),
            ("\U0001f7E4 Periosteum", "Dış koruyüçu zar"),
            ("\U0001f535 Endosteum", "İç yüzey zarı"),
            ("\U0001f7E0 Havers Kanalları", "Damar ve sinir taşıyan kanallar"),
            ("\U0001f49c Eklem Kıkırdağı", "Kemik uçlarını kaplayan kaygan doku"),
            ("\U0001f49b Epifiz", "Kemiğin uç kısımları"),
        ],
        "ilginc_bilgiler": [
            "Kemik, aynı boyuttaki çelik çubuktan daha güçlüdür ancak çok daha hafiftir.",
            "Yeni doğan bir bebekte yaklaşık iki yüz yetmiş kemik vardır, bunların bir kısmı zamanla kaynaşır.",
            "Femur, yani uyluk kemiği, vücudun en uzun ve en güçlü kemiğidir.",
            "Kemikler canlı dokudur ve kırıldığında kendini tamir edebilir.",
            "Bir insan iskeletinin tamamı yaklaşık on yılda bir tamamen yenilenir.",
        ],
    },
    15: {  # Kırmızı Kan Hücresi
        "baslik": "Kırmızı Kan Hücresi (Eritrosit)",
        "emoji": "\U0001fa78",
        "tanim": "Eritrositler, kanın en bol hücreleridir ve oksijen taşıma görevini üstlenir. Bikonkav disk şekline sahip, çekirdeksiz hücrelerdir.",
        "seslendirme": (
            "Kırmızı kan hücreleri, yani eritrositler, kandaki en bol hücrelerdir. Her mikrolitre kanda yaklaşık beş milyon eritrosit bulunur. "
            "Eritrositler, bikonkav disk şeklinde, yani her iki yüzü de içeri çökük yuvarlak hücrelerdir. Bu şekil yüzey alanını artırır. "
            "Olgun eritrositlerde çekirdek yoktur. Bu özellik hücrenin iç hacmini artırarak daha fazla hemoglobin taşımasını sağlar. "
            "Hemoglobin, eritrositlerin içindeki oksijen taşıyıcı proteindir. Her hemoglobin molekülü dört oksijen molekülü bağlayabilir. "
            "Hemoglobindeki demir atomu oksijene bağlandığında kan parlak kırmızı renk alır. Oksijensiz kan daha köyü kırmızıdır. "
            "Bir eritrosit yaklaşık yedi mikrometre çapında ve iki mikrometre kalınlığındadır. İnsan saç telinden çok daha küçüktür. "
            "Eritrositler esnek yapıdadır ve kendilerinden daha dar kılcal damarlardan geçebilmek için şekil değiştirebilir. "
            "Eritrositlerin ömrü yaklaşık yüz yirmi gündür. Yaşlanan eritrositler dalak ve karaciğerde parçalanır. "
            "Kemik iliği her saniye yaklaşık iki milyon yeni eritrosit üretir. Bu üretim eritropoietin hormonu ile düzenlenir. "
            "Toplam kan hacmindeki eritrositlerin oranına hematokrit denir. Erkeklerde yüzde kırk ile elli dört, kadınlarda yüzde otuz altı ile kırk sekiz arasındadır. "
            "Eritrositler oksijen taşımanın yanı sıra karbondioksit uzaklaştırılmasında da rol oynar. "
            "Kan grupları, eritrosit yüzeyindeki antijenlere göre belirlenir. A, B, AB ve O olmak üzere dört ana kan grubu vardır. "
            "Rh faktörü, eritrosit yüzeyindeki bir başka antijen türüdür. Pozitif veya negatif olarak tanımlanır. "
            "Anemi, kanddaki eritrosit veya hemoglobin miktarının normalden düşük olması durumudur. Halsizlik ve solgunluğa neden olur. "
            "Orak hücre anemisinde eritrositler orak şeklini alır ve damarları tıkayarak ciddi ağrı ve organ hasarına yol açar. "
            "Roulo formasyonu, eritrositlerin bözük para dizisi gibi üst üste dizilmesidir. Belirli hastalıklarda görülür. "
            "Eritrositler, vücuttaki toplam hücrelerin yaklaşık yüzde yetmiş besini oluşturur ve hayat boyu sürekli yenilenir."
        ),
        "özellikler": [
            ("Çap", "~7 mikrometre"),
            ("Şekil", "Bikonkav disk"),
            ("Sayı", "~5 milyon/μL"),
            ("Ömür", "~120 gün"),
            ("Üretim Hızı", "~2 milyon/saniye"),
            ("Hemoglobin", "~270 milyon/hücre"),
            ("Çekirdek", "Yok (olgun eritrosit)"),
            ("Hematokrit", "%36-54"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Eritrosit Zarı", "Esnek çift katlı lipit membran"),
            ("\U0001f534 Hemoglobin", "Oksijen taşıyan demir içeren protein"),
            ("\U0001f7E0 Bikonkav Şekil", "Her iki yüzü çökük — yüzey alanı artırır"),
            ("\U0001f535 Demir Atomu", "Oksijen bağlama noktası"),
            ("\U0001f7E1 Hücre İskeleti", "Esnek spektrin ağı — şekli korur"),
            ("\U0001f49c Glikoproteinler", "Kan grubu antijenlerini belirler"),
            ("\U0001f49b Roulo", "Üst üste dizilmiş eritrosit formasyonu"),
        ],
        "ilginc_bilgiler": [
            "Vücuttaki tüm eritrositler uç üça dizilse dünyayı dört kez dolaşır.",
            "Her saniye yaklaşık iki milyon yeni eritrosit üretilir ve aynı sayıda yıkılır.",
            "Eritrositler çekirdeksiz olmaları sayesinde daha fazla oksijen taşıyabilir.",
            "Kan kırmızı görünür çünkü hemoglobindeki demir atomu ışığı kırmızı olarak yansıtır.",
            "Bir damla kanda yaklaşık beş milyon kırmızı kan hücresi bulunur.",
        ],
    },
    16: {  # Beyaz Kan Hücresi
        "baslik": "Beyaz Kan Hücresi (Lökosit)",
        "emoji": "\U0001f6e1\uFE0F",
        "tanim": "Lökositler, bağışıklık sisteminin savaşçı hücreleridir. Vücudu enfeksiyonlara, virüslere ve yabancı maddelere karşı korur. Kanda eritrositlere göre çok daha az sayıdadır.",
        "seslendirme": (
            "Beyaz kan hücreleri, yani lökositler, vücudun savunma ordusudur. Bağışıklık sisteminin temel hücreleridir. "
            "Her mikrolitre kanda dört bin ile on bir bin arasında lökosit bulunur. Bu, eritrositlerin yaklaşık binde biri kadardır. "
            "Lökositler beş ana tipe ayrılır: nötrofiller, lenfositler, monositler, eozinofiller ve bazofiller. "
            "Nötrofiller, lökositlerin yüzde altmış ile yetmişini oluşturur ve bakterilere karşı ilk savunma hattıdır. Fagositoz yaparak bakterileri yutar. "
            "Lenfositler, bağışıklık sisteminin hafıza ve hedefleme birimi olan hücrelerdir. T hücreleri ve B hücreleri olarak ikiye ayrılır. "
            "T hücreleri virüsle enfekte olmuş hücreleri ve kanser hücrelerini doğrudan öldürür. Yardımcı T hücreleri ise bağışıklık yanıtını koordine eder. "
            "B hücreleri antikor üreterek patojenleri işaretler ve nötralize eder. Aşılama B hücrelerinin hafıza oluşturmasına dayanır. "
            "Monositler kanda dolaştıktan sonra dokulara geçerek makrofajlara dönüşür. Makrofajlar büyük partikülleri ve hücre kalıntılarını temizler. "
            "Eozinofiller, parazit enfeksiyonlarına karşı savaşır ve alerjik reaksiyonlarda rol oynar. "
            "Bazofiller en az sayıda bulunan lökosittir ve histamin salgılayarak inflamasyon yanıtını başlatır. "
            "Lökositler kan damarlarının duvarından geçerek dokulara ulaşabilir. Bu süreç diyapedez olarak adlandırılır. "
            "Enfekte veya hasarlı dokular kimyasal sinyaller yayar. Lökositler bu sinyalleri takip ederek enfeksiyon bölgesine ulaşır. Bu süreç kemotaksi olarak bilinir. "
            "Yalancı ayaklar, lökositlerin hareket etmek ve patojenleri yakalamak için oluşturduğu geçiçi uzantılardır. "
            "Ateş, lökositlerin daha etkili çalışması için vücudun sıcaklığını artırması stratejisidir. "
            "Lösemi, beyaz kan hücrelerinin kontrolsüz çoğaldığı bir kanser türüdür. Sağlıklı kan hücresi üretimini bozar. "
            "Lökositlerin ömrü birkaç saatten birkaç yıla kadar değişir. Hafıza hücreleri yıllarca yaşayabilir. "
            "Bağışıklık sistemi, vücudu koruyan bu hücrelerin koordineli çalışmasıyla ayakta durur. Dengeli beslenme ve uyku bağışıklığı güçlendirir."
        ),
        "özellikler": [
            ("Sayı", "4.000-11.000/μL"),
            ("Ana Tip", "5 (nötrofil, lenfosit, monosit, eozinofil, bazofil)"),
            ("En Bol Tip", "Nötrofil (~%60-70)"),
            ("Boyut", "10-15 mikrometre"),
            ("Çekirdek", "Var (loblu veya yuvarlak)"),
            ("Üretim Yeri", "Kemik iliği"),
            ("Ömür", "Saatlerden yıllara kadar"),
            ("Hareket", "Yalancı ayaklarla aktif hareket"),
        ],
        "yapi_bilgileri": [
            ("\U0001f535 Nötrofil", "En bol — bakteri avcısı, fagositoz yapar"),
            ("\U0001f7E2 Lenfosit", "T ve B hücreleri — hedefli bağışıklık"),
            ("\U0001f7E3 Monosit", "Dokulara geçince makrofaj olur"),
            ("\U0001f7E0 Eozinofil", "Parazit savaşçısı ve alerji düzenleyiçi"),
            ("\U0001f534 Bazofil", "Histamin salgılar — inflamasyon başlatır"),
            ("\U0001f49c Yalancı Ayaklar", "Hareket ve yakalama uzantıları"),
            ("\U0001f49b Çekirdek", "Loblu yapı — nötrofilde 3-5 lob"),
            ("\U0001f7E1 Granüller", "Enzim ve kimyasal madde depoları"),
        ],
        "ilginc_bilgiler": [
            "Beyaz kan hücresi sayısı enfeksiyon sırasında üç katına kadar çıkabilir.",
            "Bir nötrofil yaklaşık yirmi bakteri yutabilir ancak bu süreçte kendisi de ölür.",
            "İrin, aslında ölmüş beyaz kan hücreleri, bakteriler ve doku kalıntılarının birikimidir.",
            "Hafıza T hücreleri bir patojeni yıllarca hatırlayabilir — bu aşıların çalışma prensibidir.",
            "Lökositler, eritrositlerin aksine kan damarlarının duvarından geçerek dokulara ulaşabilir.",
        ],
    },
    17: {  # Trombosit
        "baslik": "Trombosit (Kan Pulcuğu)",
        "emoji": "\U0001fa79",
        "tanim": "Trombositler, kanama durdurmada görev alan küçük hücre parçalarıdır. Pıhtılaşma sürecinin başlatıcısıdır ve damar onarımında kritik rol oynar.",
        "seslendirme": (
            "Trombositler, yani kan pulcukları, kanama durdurmada hayati rol oynayan küçük hücre parçalarıdır. "
            "Trombositler gerçek hücre değildir. Kemik iliğindeki megakaryosit adı verilen dev hücrelerin parçalanmasıyla oluşur. "
            "Her mikrolitre kanda yüz elli bin ile dört yüz bin arasında trombosit bulunur. Çapları sadece iki ile üç mikrometredir. "
            "Normal durumda trombositler disk şeklindedir ve kandaki en küçük şekilli elemanlardır. "
            "Damar hasarı oluştuğunda trombositler hızla aktive olur. Şekilleri değişir ve yalancı ayaklar oluşturarak yıldız şekline dönüşür. "
            "Aktive olan trombositler hasar bölgesine yapışır. Bu süreç trombosit adezyonu olarak adlandırılır. "
            "Daha sonra birbirine yapışarak trombosit tıkacı oluşturur. Buna trombosit agregasyonu denir ve kanamanın ilk durduğu adımdır. "
            "Pıhtılaşma kaskadı, on üç farklı pıhtılaşma faktörünün zincirleme reaksiyonudur. Sonunda fibrinojen fibrinine dönüşür. "
            "Fibrin iplikleri, trombosit tıkacının üzerine ağ gibi örülerek kalıcı pıhtıyı oluşturur. Bu ağ kırmızı kan hücrelerini de yakalar. "
            "Pıhtı oluşumu dakikalar içinde tamamlanır ve kanamayı durdurur. Doku iyileştikten sonra pıhtı eritilir. "
            "Von Willebrand faktörü, trombositlerin damar duvarına yapışmasını sağlayan önemli bir proteindir. "
            "Tromboksan A iki, aktive trombositlerden salınır ve daha fazla trombositin toplanmasını uyarır. "
            "Trombositlerin ömrü sekiz ile on gün arasındadır. Yaşlanan trombositler dalakta parçalanır. "
            "Trombositopeni, trombosit sayısının düşük olması durumudur ve aşırı kanamaya yol açabilir. "
            "Trombositoz ise trombosit sayısının yüksek olmasıdır ve pıhtı oluşum riskini artırır. "
            "Aspirin, trombosit aktivasyonunu engelleyerek kan sulandırıcı etki gösterir. Bu nedenle kalp hastaları tarafından kullanılır. "
            "Pıhtılaşma sistemi, kanama ile pıhtı oluşumu arasında hassas bir denge kurar. Bu denge bözülursa ciddi sağlık sorunları ortaya çıkar."
        ),
        "özellikler": [
            ("Sayı", "150.000-400.000/μL"),
            ("Çap", "2-3 mikrometre"),
            ("Ömür", "8-10 gün"),
            ("Şekil", "Disk (inaktif), yıldız (aktif)"),
            ("Çekirdek", "Yok"),
            ("Kaynak", "Megakaryosit (kemik iliği)"),
            ("Pıhtılaşma Faktörü", "13 farklı faktör"),
            ("Yıkım Yeri", "Dalak"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7E1 İnaktif Trombosit", "Düz disk şeklinde — kandaki en küçük eleman"),
            ("\U0001f534 Aktif Trombosit", "Yalancı ayaklı yıldız şekli"),
            ("\u26aa Fibrin İplikleri", "Pıhtıyı güçlendiren protein ağı"),
            ("\U0001f534 Fibrin Ağı", "Kan hücrelerini yakalayan örgü"),
            ("\U0001f7E0 Granüller", "Pıhtılaşma faktörlerini depolar"),
            ("\U0001f535 Von Willebrand Faktörü", "Yapışmayı sağlayan protein"),
            ("\U0001f49c Tromboksan A2", "Agregasyonu uyaran sinyal molekülü"),
            ("\U0001f49b Megakaryosit", "Trombosit üreten dev kemik iliği hücresi"),
        ],
        "ilginc_bilgiler": [
            "Trombositler gerçek hücre değildir — megakaryositlerin kopan parçalarıdır.",
            "Bir megakaryosit binlerce trombosit üretebilir.",
            "Pıhtılaşma kaskadı on üç farklı faktörün zincirleme çalışmasını gerektirir.",
            "Aspirin, trombosit fonksiyonunu geri dönüşümsüz olarak engeller; etki trombosit ömrü boyunca sürer.",
            "Kanayan bir yaraya basınç uygulamak trombositlerin daha hızlı pıhtı oluşturmasını sağlar.",
        ],
    },
    18: {  # Deri Katmanları
        "baslik": "İnsan Derisi Katmanları",
        "emoji": "\U0001f9b4",
        "tanim": "Deri, vücudun en büyük organıdır ve yaklaşık iki metrekare yüzey alanına sahiptir. Epidermis, dermis ve hipodermis olmak üzere üç katmandan oluşur.",
        "seslendirme": (
            "Deri, insan vücudunun en büyük organıdır. Yaklaşık iki metrekare yüzey alanını kaplar ve üç buçuk ile dört kilogram ağırlığındadır. "
            "Deri üç ana katmandan oluşur: epidermis, dermis ve hipodermis. Her katmanın kendine özgü yapı ve işlevleri vardır. "
            "Epidermis, derinin en dış tabakasıdır. Keratinositler denilen hücrelerden oluşur ve dış etkenlerden koruma sağlar. "
            "Epidermisin en dış kısmındaki hücreler ölüdür ve keratin proteiniyle doludur. Bu tabaka sürekli dökülür ve yenilenir. "
            "Melanositler, epidermiste bulunan ve melanin pigmenti üreten hücrelerdir. Melanin cilt rengini belirler ve ultraviyole ışınlardan korur. "
            "Dermis, epidermisin altındaki kalın tabakadır. Kolajen ve elastin lifleri içerir ve deriye dayanıklılık ve esneklik kazandırır. "
            "Dermiste kan damarları, sinir uçları, kıl kökleri, ter bezleri ve yağ bezleri bulunur. "
            "Kıl folikülü, kılın üretildiği dermis içindeki tünel yapıdır. Her folikülün bir sebase bezi ve bir erektör kası vardır. "
            "Sebase bezler, yani yağ bezleri, sebum salgılayarak deri ve kılı yağlar. Cildin kurumasını ve çatlamasını önler. "
            "Ter bezleri iki tiptir: ekrin ter bezleri tüm vücutta bulunur ve sıcaklık düzenlemesi yapar. Apokrin ter bezleri koltuk altı gibi bölgelerde bulunur. "
            "Ter bezleri günde yaklaşık yarım litre ter üretir. Sıcak havalarda veya egzersiz sırasında bu miktar önemli ölçüde artar. "
            "Hipodermis, derinin en alt tabakasıdır ve ağırlıklı olarak yağ dokusundan oluşur. Isı yalıtımı ve enerji depolama işlevi görür. "
            "Derinin sinir uçları beş farklı duyuyu algılar: dokunma, basınç, sıcaklık, soğukluk ve ağrı. "
            "Meissner cisimcikleri hafif dokunmayı, Pacini cisimcikleri ise derin basıncı ve titreşimi algılar. "
            "Deri, D vitamini sentezinde kritik rol oynar. Güneş ışığındaki ultraviyole B ışınları deriye değdiğinde D vitamini üretimi başlar. "
            "Deri bariyer işlevi görür ve vücudu mikroorganizma, kimyasal madde ve fiziksel darbelere karşı korur. "
            "Deri hücreleri yaklaşık yirmi sekiz günde tamamen yenilenir. Bir insan yaşamı boyunca yaklaşık kırk kilogram ölü deri döker."
        ),
        "özellikler": [
            ("Yüzey Alanı", "~2 m²"),
            ("Ağırlık", "~3,5-4 kg"),
            ("Katman", "3 (epidermis, dermis, hipodermis)"),
            ("Kalınlık", "0,5-4 mm (bölgeye göre)"),
            ("Ter Bezi", "~3 milyon"),
            ("Kıl Folikülü", "~5 milyon"),
            ("Sinir Üçu", "cm² başına ~200"),
            ("Yenilenme", "~28 gün"),
        ],
        "yapi_bilgileri": [
            ("\U0001f7E1 Epidermis", "En dış tabaka — koruma ve bariyer"),
            ("\U0001f534 Dermis", "Orta tabaka — damar, sinir, kıl kökü"),
            ("\U0001f7E0 Hipodermis", "En alt tabaka — yağ ve yalıtım"),
            ("\U0001f7E4 Kıl Folikülü", "Kılın üretildiği tünel yapı"),
            ("\U0001f7E2 Sebase Bez", "Yağ salgılayan bez"),
            ("\U0001f535 Ter Bezi", "Sıcaklık düzenleyiçi salgı bezi"),
            ("\U0001f49c Melanosit", "Renk pigmenti üreten hücre"),
            ("\U0001f49b Sinir Uçları", "Dokunma ve ağrı algılayıcıları"),
            ("\U0001f534 Kan Damarları", "Deriyi besleyen damar ağı"),
        ],
        "ilginc_bilgiler": [
            "Deri vücudun en büyük organıdır ve toplam vücut ağırlığının yaklaşık yüzde on altısını oluşturur.",
            "Bir insan yaşamı boyunca yaklaşık kırk kilogram ölü deri döker.",
            "Parmak uçlarındaki deri vücudun en hassas dokunma bölgesidir.",
            "Dudaklar kırmızıdır çünkü orada epidermis çok ince olup alttaki kan damarları görünür.",
            "Deri her dakika yaklaşık otuz bin ile kırk bin ölü hücre döker.",
        ],
    },
    19: {  # Sindirim Sistemi
        "baslik": "İnsan Sindirim Sistemi",
        "emoji": "\U0001f35d",
        "tanim": "Sindirim sistemi, besinlerin alınması, parçalanması, emilmesi ve atık maddelerin vücuttan uzaklaştırılmasını sağlayan organ dizisidir. Ağızdan anüse kadar yaklaşık dokuz metre uzunluğundadır.",
        "seslendirme": (
            "İnsan sindirim sistemi, besinleri vücudun kullanabileceği yapı taşlarına dönüştüren karmaşık bir organ dizisidir. "
            "Sindirim kanalı ağızdan başlar ve anüste sona erer. Toplam uzunluğu yaklaşık dokuz metredir. "
            "Sindirim ağızda başlar. Dişler besinleri mekanik olarak parçalar, tükürük ise nişastayı kimyasal olarak sindirmeye başlar. "
            "Tükürük bezleri günde yaklaşık bir buçuk litre tükürük üretir. Tükürükteki amilaz enzimi karbonhidrat sindirimini başlatır. "
            "Yemek borusu, yani özofagus, yaklaşık yirmi beş santimetre uzunluğundadır. Peristaltık hareketlerle besinleri mideye taşır. "
            "Mide, J şeklinde kas yapılı bir organdır. Hidroklorik asit ve pepsin enzimi ile proteinlerin sindirimini gerçekleştirir. "
            "Besinler midede iki ile dört saat kalır ve kimus adı verilen bulamaç haline gelir. "
            "Onikiparmak bağırsağı, yani duodenum, ince bağırsağın ilk bölümüdür. Buraya pankreas sıvısı ve safra boşalır. "
            "Pankreas, hem sindirim enzimleri hem de insülin hormonu üreten önemli bir bezdir. Günde yaklaşık bir buçuk litre sindirim sıvısı üretir. "
            "Safra, karaciğerde üretilir ve safra kesesinde depolanır. Yağların sindirilmesi için ince bağırsağa salınır. "
            "İnce bağırsak yaklaşık altı metre uzunluğundadır. Duodenum, jejunum ve ileum olarak üç bölüme ayrılır. "
            "İnce bağırsağın iç yüzeyi villuslar ve mikrovilluslarla kaplıdır. Bu yapılar emilim yüzey alanını iki yüz metrekareye çıkarır. "
            "Besinlerin büyük çoğunluğu ince bağırsakta emilir: amino asitler, şekerler, yağ asitleri, vitaminler ve mineraller. "
            "Kalın bağırsak, yani kolon, yaklaşık bir buçuk metre uzunluğundadır. Su ve elektrolitlerin emilimini sağlar. "
            "Kalın bağırsak trilyon düzeyinde faydalı bakteri barındırır. Bu mikrobiyom sindirime yardımcı olur ve bağışıklığı destekler. "
            "Çekum, kalın bağırsağın başlangıcındaki kese şeklinde bölgedir. Apendiks buraya bağlıdır. "
            "Rektum, sindirilmemiş atıkların geçiçi olarak depolandığı son bölgedir. Dışkılama refleksi burada tetiklenir. "
            "Besin ağızdan anüse kadar olan yolculuğunu yaklaşık yirmi dört ile yetmiş iki saatte tamamlar."
        ),
        "özellikler": [
            ("Toplam Uzunluk", "~9 metre"),
            ("İnce Bağırsak", "~6 metre"),
            ("Kalın Bağırsak", "~1,5 metre"),
            ("Emilim Yüzeyi", "~200 m²"),
            ("Günlük Tükürük", "~1,5 litre"),
            ("Günlük Mide Asidi", "~1,5 litre"),
            ("Sindirim Süresi", "24-72 saat"),
            ("Mikrobiyom", "~100 trilyon bakteri"),
        ],
        "yapi_bilgileri": [
            ("\U0001f534 Ağız", "Mekanik ve kimyasal sindirimin başlangıcı"),
            ("\U0001f7E4 Özofagus", "Yemek borusu — besinleri mideye taşır"),
            ("\U0001f7E0 Mide", "J şekilli — asit ve enzimlerle sindirim"),
            ("\U0001f7E1 Duodenum", "İnce bağırsağın ilk bölümü"),
            ("\U0001f7E2 Jejunum ve İleum", "İnce bağırsağın emilim bölgeleri"),
            ("\U0001f535 Karaciğer", "Safra üretimi ve metabolizma merkezi"),
            ("\U0001f7E2 Safra Kesesi", "Safra depolama ve salgılama"),
            ("\U0001f49c Pankreas", "Sindirim enzimleri ve insülin üretimi"),
            ("\U0001f7E4 Kalın Bağırsak", "Su emilimi ve atık depolama"),
            ("\U0001f534 Apendiks", "Çekuma bağlı — bağışıklık işlevi"),
        ],
        "ilginc_bilgiler": [
            "Sindirim sistemi uç üça açılsa yaklaşık bir tenis kortu büyüklüğünde yüzey alanı ortaya çıkar.",
            "Bağırsaklardaki bakteri sayısı vücuttaki insan hücre sayısından fazladır.",
            "Mide her üç ile dört günde bir iç tabakasını tamamen yeniler.",
            "Sindirim sisteminde ikinci bir sinir ağı bulunur, bu nedenle bağırsaklara 'ikinci beyin' denir.",
            "Bir insan yaşamı boyunca yaklaşık otuz beş ton besin sindirir.",
        ],
    },
}

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
def _inject_css():
    if st.session_state.get("_sc3d_css_ok"):
        return
    st.session_state["_sc3d_css_ok"] = True
    inject_common_css("sc3d")
    st.markdown("""<style>
    .stApp {font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
        background:linear-gradient(180deg,#0B0F19 0%,#131825 100%);}
    .stApp > header {background:transparent !important;}
    .stButton > button {border-radius:10px !important;font-weight:600 !important;
        transition:all 0.3s ease !important;}
    .stButton > button:hover {transform:translateY(-1px);}
    .stButton > button[kind="primary"] {
        background:linear-gradient(135deg,#2563eb,#1e40af) !important;
        color:white !important;border:none !important;}
    .streamlit-expanderHeader {background:#111827;border-radius:10px !important;
        border:1px solid #e2e8f0 !important;font-weight:600 !important;}
    </style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 4 STANDART STIL FONKSIYONU
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
# THREE.JS 3D — 400 BENZERSIZ SAHNE
# ══════════════════════════════════════════════════════════════

def _scene_js(ci, ti):
    """Kategori ci (0-19) ve konu ti (0-19) için benzersiz Three.js kodu."""

    if ci == 0:  # Güneş Sistemi — 20 Premium 3D Sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        var _m=function(g,c,o){{var mt=new THREE.MeshPhongMaterial({{color:c,shininess:60}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        var _mb=function(g,c,o){{var mt=new THREE.MeshBasicMaterial({{color:c}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};

        if(T==0){{
        /* ===== MERKUR — Kraterleri ve ince yüzey detaylari ===== */
        var body=_m(new THREE.SphereGeometry(.85,32,32),0x8C7E6A,{{shininess:25}});mainObj.add(body);
        /* Büyük kraterler */
        for(var i=0;i<14;i++){{var cr=_m(new THREE.SphereGeometry(.08+Math.random()*.12,16,16),0x736658,{{shininess:15}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cr.position.set(Math.sin(th)*Math.cos(ph)*.84,Math.cos(th)*.84,Math.sin(th)*Math.sin(ph)*.84);cr.scale.y=.3;cr.lookAt(0,0,0);mainObj.add(cr);}}
        /* Küçük kraterler */
        for(var i=0;i<20;i++){{var sc=_m(new THREE.SphereGeometry(.03+Math.random()*.05,10,10),0x695D50,{{shininess:10}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;sc.position.set(Math.sin(th)*Math.cos(ph)*.85,Math.cos(th)*.85,Math.sin(th)*Math.sin(ph)*.85);sc.scale.y=.25;sc.lookAt(0,0,0);mainObj.add(sc);}}
        /* Caloris Havzasi — büyük carpma kraterleri */
        var cal=_m(new THREE.RingGeometry(.22,.28,24),0x9E8E7A,{{side:THREE.DoubleSide}});cal.position.set(.5,.4,.5);cal.lookAt(0,0,0);mainObj.add(cal);
        var calIn=_m(new THREE.CircleGeometry(.22,24),0x7A6E5E,{{side:THREE.DoubleSide}});calIn.position.set(.5,.4,.5);calIn.lookAt(0,0,0);mainObj.add(calIn);
        /* Yüzey catlaklari / scarps */
        for(var i=0;i<8;i++){{var sc=_m(new THREE.CylinderGeometry(.008,.008,.5,6),0x5C5040,{{shininess:10}});var a=i*.8;sc.position.set(Math.cos(a)*.6,Math.sin(a*1.3)*.5,Math.sin(a)*.6);sc.rotation.z=Math.random()*1.5;sc.rotation.x=Math.random();mainObj.add(sc);}}
        /* Golgeli yari — ince atmosfersiz gece */
        var shadow=_mb(new THREE.SphereGeometry(.87,32,32),0x222222,{{transparent:true,opacity:.3,side:THREE.BackSide}});shadow.position.x=-.3;mainObj.add(shadow);
        }}

        else if(T==1){{
        /* ===== VENUS — Kalin atmosfer, volkancik yüzey ===== */
        /* Kaya govde */
        var body=_m(new THREE.SphereGeometry(1.05,32,32),0xC4943A,{{shininess:20}});mainObj.add(body);
        /* Volkanik yapilar */
        for(var i=0;i<10;i++){{var v=_m(new THREE.ConeGeometry(.08+Math.random()*.1,.15+Math.random()*.12,8),0xB8842E,{{shininess:15}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;v.position.set(Math.sin(th)*Math.cos(ph)*1.02,Math.cos(th)*1.02,Math.sin(th)*Math.sin(ph)*1.02);v.lookAt(0,0,0);v.rotateX(Math.PI);mainObj.add(v);}}
        /* Lav duzlukleri */
        for(var i=0;i<6;i++){{var lv=_m(new THREE.CircleGeometry(.15+Math.random()*.1,16),0xD4A030,{{side:THREE.DoubleSide,emissive:new THREE.Color(0x331100),emissiveIntensity:.2}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;lv.position.set(Math.sin(th)*Math.cos(ph)*1.06,Math.cos(th)*1.06,Math.sin(th)*Math.sin(ph)*1.06);lv.lookAt(0,0,0);mainObj.add(lv);}}
        /* Kalin CO2 atmosferi — 4 katman */
        for(var i=0;i<4;i++){{var atm=_mb(new THREE.SphereGeometry(1.12+i*.08,24,24),0xDEB060,{{transparent:true,opacity:.1-.01*i,side:THREE.DoubleSide}});mainObj.add(atm);}}
        /* Atmosferdeki sulefirik asit bulutlari */
        for(var i=0;i<12;i++){{var cl=_mb(new THREE.SphereGeometry(.15+Math.random()*.2,12,12),0xE8C870,{{transparent:true,opacity:.12}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2,r=1.25+Math.random()*.15;cl.position.set(Math.sin(th)*Math.cos(ph)*r,Math.cos(th)*r,Math.sin(th)*Math.sin(ph)*r);cl.scale.set(1.5,.6,1);mainObj.add(cl);}}
        /* Maxwell dağı */
        var mx=_m(new THREE.ConeGeometry(.14,.25,8),0xA0802A,{{shininess:30}});mx.position.set(0,.98,0);mainObj.add(mx);
        }}

        else if(T==2){{
        /* ===== DUNYA — Okyanus, kita, kutup, bulut, atmosfer ===== */
        /* Okyanus govde */
        var body=_m(new THREE.SphereGeometry(1.1,32,32),0x1a5276,{{shininess:90}});mainObj.add(body);
        /* Kitalar — yaklaşık sekiller */
        var contData=[[0,.5,.8,.25,0x2E7D32],[-.3,.2,1.0,.18,0x388E3C],[.5,-.1,.9,.2,0x43A047],[-.6,-.5,.7,.22,0x2E7D32],[.2,.7,.5,.15,0x388E3C],[.8,.3,.4,.12,0x4CAF50],[-.1,-.9,.3,.14,0x1B5E20]];
        for(var i=0;i<contData.length;i++){{var d=contData[i];var ct=_m(new THREE.SphereGeometry(d[3],12,12),d[4],{{shininess:20}});ct.position.set(d[0]*1.05,d[1]*1.05,d[2]*1.05);ct.scale.set(1.3,.4,1.1);mainObj.add(ct);}}
        /* Kutup buzullari */
        var np=_m(new THREE.SphereGeometry(.3,16,16),0xE8EAF6,{{shininess:100}});np.position.y=1.05;np.scale.set(1.2,.3,1.2);mainObj.add(np);
        var sp=_m(new THREE.SphereGeometry(.25,16,16),0xE8EAF6,{{shininess:100}});sp.position.y=-1.05;sp.scale.set(1.1,.3,1.1);mainObj.add(sp);
        /* Bulut katmani */
        for(var i=0;i<18;i++){{var cl=_mb(new THREE.SphereGeometry(.08+Math.random()*.12,10,10),0xffffff,{{transparent:true,opacity:.25}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cl.position.set(Math.sin(th)*Math.cos(ph)*1.16,Math.cos(th)*1.16,Math.sin(th)*Math.sin(ph)*1.16);cl.scale.set(2,.4,1.2);mainObj.add(cl);}}
        /* Atmosfer */
        var atm=_mb(new THREE.SphereGeometry(1.22,24,24),0x4FC3F7,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});mainObj.add(atm);
        var atm2=_mb(new THREE.SphereGeometry(1.3,24,24),0x81D4FA,{{transparent:true,opacity:.04,side:THREE.DoubleSide}});mainObj.add(atm2);
        }}

        else if(T==3){{
        /* ===== MARS — Kirmizi gezegen, Olympus Mons, Valles Marineris ===== */
        var body=_m(new THREE.SphereGeometry(.95,32,32),0xC1440E,{{shininess:20}});mainObj.add(body);
        /* Olympus Mons — dev kalkan volkani */
        var oly=_m(new THREE.ConeGeometry(.2,.35,16),0xD4763A,{{shininess:15}});oly.position.set(0,.85,-.3);mainObj.add(oly);
        var olyB=_m(new THREE.CylinderGeometry(.25,.3,.06,16),0xC8632E,{{shininess:15}});olyB.position.set(0,.7,-.3);mainObj.add(olyB);
        /* Tharsis volkanlari */
        for(var i=0;i<3;i++){{var tv=_m(new THREE.ConeGeometry(.08,.15,10),0xBB5522,{{shininess:15}});tv.position.set(-.2+i*.15,.6,-.15+i*.1);mainObj.add(tv);}}
        /* Valles Marineris — dev kanyon */
        for(var i=0;i<5;i++){{var vm=_m(new THREE.BoxGeometry(.08,.02,.6-i*.08),0x8B3000,{{shininess:10}});vm.position.set(-.1+i*.06,.1,0);vm.rotation.y=.3;mainObj.add(vm);}}
        /* Kutup buzulu */
        var np=_m(new THREE.SphereGeometry(.2,16,16),0xE8E0D8,{{shininess:80}});np.position.y=.92;np.scale.set(1,.25,1);mainObj.add(np);
        /* Ince atmosfer */
        var atm=_mb(new THREE.SphereGeometry(1.02,24,24),0xD4835A,{{transparent:true,opacity:.06,side:THREE.DoubleSide}});mainObj.add(atm);
        /* Kraterler */
        for(var i=0;i<10;i++){{var cr=_m(new THREE.RingGeometry(.03,.06,12),0xA03500,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cr.position.set(Math.sin(th)*Math.cos(ph)*.96,Math.cos(th)*.96,Math.sin(th)*Math.sin(ph)*.96);cr.lookAt(0,0,0);mainObj.add(cr);}}
        /* Phobos ve Deimos */
        var ph=_m(new THREE.DodecahedronGeometry(.06),0x8A7A6A,{{shininess:20}});ph.position.set(1.4,0,0);mainObj.add(ph);
        var dm=_m(new THREE.DodecahedronGeometry(.04),0x7A6A5A,{{shininess:20}});dm.position.set(-1.6,.2,0);mainObj.add(dm);
        }}

        else if(T==4){{
        /* ===== JUPITER — Gaz devi, bantlar, Büyük Kirmizi Leke ===== */
        var body=_m(new THREE.SphereGeometry(1.8,32,32),0xC8A050,{{shininess:40}});mainObj.add(body);
        /* Atmosferik bantlar */
        var bClrs=[0xD4A840,0xA08030,0xE8C060,0x907020,0xF0D070,0xB09040,0xD4B050,0x806018];
        for(var i=0;i<8;i++){{var band=_m(new THREE.TorusGeometry(1.81,.04,8,64),bClrs[i],{{shininess:30}});band.position.y=-1.2+i*.35;var sc=Math.sqrt(1-Math.pow((-1.2+i*.35)/1.8,2));band.scale.set(sc,1,sc);mainObj.add(band);}}
        /* Büyük Kirmizi Leke — GRS */
        var grs=_m(new THREE.SphereGeometry(.25,24,24),0xCC3322,{{emissive:new THREE.Color(0x551111),emissiveIntensity:.3}});grs.position.set(.8,-.25,1.4);grs.scale.set(1.6,.6,1);mainObj.add(grs);
        var grsR=_m(new THREE.TorusGeometry(.22,.03,8,32),0xDD4433,{{transparent:true,opacity:.6}});grsR.position.copy(grs.position);grsR.lookAt(0,0,0);mainObj.add(grsR);
        /* 4 Galileo uydusu */
        var mClrs=[0xCCCC55,0x8B7355,0xAAAACC,0x887766];var mDst=[2.5,2.8,3.2,3.6];var mSz=[.08,.12,.1,.12];
        for(var i=0;i<4;i++){{var mu=_m(new THREE.SphereGeometry(mSz[i],12,12),mClrs[i],{{shininess:50}});var a=i*1.6;mu.position.set(Math.cos(a)*mDst[i],Math.sin(a*.3)*.1,Math.sin(a)*mDst[i]);mainObj.add(mu);}}
        /* Ince halka */
        var ring=_m(new THREE.TorusGeometry(2.1,.02,8,64),0xAA9966,{{transparent:true,opacity:.15}});ring.rotation.x=1.5;mainObj.add(ring);
        }}

        else if(T==5){{
        /* ===== SATURN — Ihtisam halkalari, bantlar, Titan ===== */
        var body=_m(new THREE.SphereGeometry(1.5,32,32),0xE8D070,{{shininess:35}});body.scale.y=.9;mainObj.add(body);
        /* Atmosferik bantlar */
        for(var i=0;i<6;i++){{var band=_m(new THREE.TorusGeometry(1.51,.03,8,64),i%2?0xC8A840:0xD8C060,{{shininess:20}});band.position.y=-.7+i*.28;var sc=Math.sqrt(Math.max(0,1-Math.pow((-0.7+i*.28)/1.35,2)));band.scale.set(sc,1,sc);mainObj.add(band);}}
        /* Ana halka sistemi — A, B, C, F halkalari */
        var ringData=[[2.0,.08,0xDDCCA0,.5],[2.2,.12,0xC8B888,.6],[2.5,.06,0xBBAAAA,.4],[2.7,.03,0xAA9988,.3],[2.85,.04,0xEEDDBB,.25]];
        for(var i=0;i<ringData.length;i++){{var rd=ringData[i];var rg=_m(new THREE.TorusGeometry(rd[0],rd[1],12,128),rd[2],{{transparent:true,opacity:rd[3]}});rg.rotation.x=1.4;mainObj.add(rg);}}
        /* Cassini Boslugu — köyü ince halka */
        var cass=_m(new THREE.TorusGeometry(2.35,.02,8,64),0x443322,{{transparent:true,opacity:.5}});cass.rotation.x=1.4;mainObj.add(cass);
        /* Encke Boslugu */
        var enc=_m(new THREE.TorusGeometry(2.65,.015,8,48),0x332211,{{transparent:true,opacity:.3}});enc.rotation.x=1.4;mainObj.add(enc);
        /* Titan */
        var titan=_m(new THREE.SphereGeometry(.12,16,16),0xCC9944,{{shininess:40}});titan.position.set(3.2,.3,0);mainObj.add(titan);
        var tatm=_mb(new THREE.SphereGeometry(.16,12,12),0xDDAA55,{{transparent:true,opacity:.15}});tatm.position.copy(titan.position);mainObj.add(tatm);
        /* Diger uydular */
        for(var i=0;i<5;i++){{var sm=_m(new THREE.SphereGeometry(.04+i*.01,8,8),0xCCBBAA,{{shininess:40}});var a=i*1.3+1;sm.position.set(Math.cos(a)*(2.6+i*.25),.1*Math.sin(a),Math.sin(a)*(2.6+i*.25));mainObj.add(sm);}}
        }}

        else if(T==6){{
        /* ===== URANUS — Buz devi, yatik eksen, ince halkalar ===== */
        var body=_m(new THREE.SphereGeometry(1.25,32,32),0x72B5C0,{{shininess:50}});mainObj.add(body);
        /* Atmosferik bant */
        for(var i=0;i<4;i++){{var band=_mb(new THREE.TorusGeometry(1.26,.015,8,64),i%2?0x88CCDD:0x5AA0B0,{{transparent:true,opacity:.15}});band.position.y=-.4+i*.27;var sc=Math.sqrt(Math.max(0,1-Math.pow((-.4+i*.27)/1.25,2)));band.scale.set(sc,1,sc);mainObj.add(band);}}
        /* Yatik halka sistemi — 97 derece */
        for(var i=0;i<5;i++){{var rg=_m(new THREE.TorusGeometry(1.6+i*.15,.015,8,64),0x667788,{{transparent:true,opacity:.2}});rg.rotation.z=1.7;mainObj.add(rg);}}
        /* Kutup parlamasi */
        var glow=_mb(new THREE.SphereGeometry(.4,16,16),0xAAEEFF,{{transparent:true,opacity:.1}});glow.position.set(0,1.1,0);mainObj.add(glow);
        /* 5 ana uydu */
        var uClrs=[0xCCCCCC,0xBBAAAA,0xAABBCC,0x99AABB,0xBBBBCC];var uNm=[1.8,2.0,2.2,2.4,2.6];
        for(var i=0;i<5;i++){{var mu=_m(new THREE.SphereGeometry(.05+i*.01,10,10),uClrs[i],{{shininess:40}});var a=i*1.3;mu.position.set(Math.cos(a)*uNm[i],Math.sin(a)*.3,Math.sin(a)*uNm[i]);mainObj.add(mu);}}
        /* Atmosfer */
        var atm=_mb(new THREE.SphereGeometry(1.32,24,24),0x88DDEE,{{transparent:true,opacity:.06,side:THREE.DoubleSide}});mainObj.add(atm);
        }}

        else if(T==7){{
        /* ===== NEPTUN — Mavi dev, Büyük Karanlik Leke, firtinalar ===== */
        var body=_m(new THREE.SphereGeometry(1.2,32,32),0x2244AA,{{shininess:60}});mainObj.add(body);
        /* Atmosferik bantlar */
        for(var i=0;i<5;i++){{var band=_m(new THREE.TorusGeometry(1.21,.02,8,64),i%2?0x3355BB:0x1133AA,{{transparent:true,opacity:.2}});band.position.y=-.6+i*.3;var sc=Math.sqrt(Math.max(0,1-Math.pow((-.6+i*.3)/1.2,2)));band.scale.set(sc,1,sc);mainObj.add(band);}}
        /* Büyük Karanlik Leke */
        var gds=_m(new THREE.SphereGeometry(.2,20,20),0x112266,{{emissive:new THREE.Color(0x000033),emissiveIntensity:.4}});gds.position.set(.6,.1,1.0);gds.scale.set(1.5,.7,1);mainObj.add(gds);
        var gdsB=_mb(new THREE.RingGeometry(.15,.22,20),0x2255CC,{{transparent:true,opacity:.3,side:THREE.DoubleSide}});gdsB.position.copy(gds.position);gdsB.lookAt(0,0,0);mainObj.add(gdsB);
        /* Beyaz bulut bantlari */
        for(var i=0;i<8;i++){{var cl=_mb(new THREE.SphereGeometry(.06+Math.random()*.08,8,8),0xBBDDFF,{{transparent:true,opacity:.2}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cl.position.set(Math.sin(th)*Math.cos(ph)*1.24,Math.cos(th)*1.24,Math.sin(th)*Math.sin(ph)*1.24);cl.scale.set(2,.3,.8);mainObj.add(cl);}}
        /* Halkalar */
        for(var i=0;i<3;i++){{var rg=_m(new THREE.TorusGeometry(1.5+i*.12,.01,8,48),0x4466AA,{{transparent:true,opacity:.15}});rg.rotation.x=1.45;mainObj.add(rg);}}
        /* Triton */
        var triton=_m(new THREE.SphereGeometry(.1,12,12),0xAABBCC,{{shininess:50}});triton.position.set(-2.0,.2,0);mainObj.add(triton);
        var trAtm=_mb(new THREE.SphereGeometry(.13,10,10),0xBBCCDD,{{transparent:true,opacity:.1}});trAtm.position.copy(triton.position);mainObj.add(trAtm);
        }}

        else if(T==8){{
        /* ===== PLUTON — Cüçe gezegen, kalp deseni, Charon ===== */
        var body=_m(new THREE.SphereGeometry(.6,24,24),0xC8B8A0,{{shininess:25}});mainObj.add(body);
        /* Tombaugh Regio — kalp şeklinde parlak alan */
        var h1=_m(new THREE.SphereGeometry(.18,16,16),0xF0E8D8,{{shininess:40}});h1.position.set(.15,.25,.5);mainObj.add(h1);
        var h2=_m(new THREE.SphereGeometry(.18,16,16),0xF0E8D8,{{shininess:40}});h2.position.set(-.1,.25,.52);mainObj.add(h2);
        var h3=_m(new THREE.SphereGeometry(.12,12,12),0xECE0D0,{{shininess:35}});h3.position.set(.03,.1,.55);mainObj.add(h3);
        /* Koyu bölge */
        var dk=_m(new THREE.SphereGeometry(.2,12,12),0x8A7A5A,{{shininess:15}});dk.position.set(-.4,-.1,.35);mainObj.add(dk);
        /* Azot buzullari */
        for(var i=0;i<5;i++){{var nf=_m(new THREE.SphereGeometry(.06+Math.random()*.04,8,8),0xE8E0D0,{{shininess:60}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;nf.position.set(Math.sin(th)*Math.cos(ph)*.61,Math.cos(th)*.61,Math.sin(th)*Math.sin(ph)*.61);mainObj.add(nf);}}
        /* Ince atmosfer */
        var atm=_mb(new THREE.SphereGeometry(.66,32,32),0xCCBBAA,{{transparent:true,opacity:.06,side:THREE.DoubleSide}});mainObj.add(atm);
        /* Charon */
        var charon=_m(new THREE.SphereGeometry(.3,24,24),0x888888,{{shininess:30}});charon.position.set(1.5,0,0);mainObj.add(charon);
        var chD=_m(new THREE.SphereGeometry(.08,10,10),0x555555,{{shininess:20}});chD.position.set(1.5,.25,0);mainObj.add(chD);
        /* Yoerungeler goster — ince cizgi */
        var orb=_m(new THREE.TorusGeometry(1.5,.005,8,64),0x888888,{{transparent:true,opacity:.15}});orb.rotation.x=Math.PI/2;mainObj.add(orb);
        }}

        else if(T==9){{
        /* ===== AY — Kraterler, denizler, yüzey detay ===== */
        var body=_m(new THREE.SphereGeometry(.95,32,32),0xBBBBBB,{{shininess:20}});mainObj.add(body);
        /* Maria — köyü denizler */
        var mariaData=[[.2,.5,.6,.2,0x777777],[-.3,.3,.7,.18,0x808080],[0,-.2,.8,.15,0x757575],[.4,0,.7,.12,0x727272],[-.2,-.4,.6,.1,0x7A7A7A]];
        for(var i=0;i<mariaData.length;i++){{var d=mariaData[i];var ma=_m(new THREE.CircleGeometry(d[3],20),d[4],{{side:THREE.DoubleSide}});ma.position.set(d[0]*.9,d[1]*.9,d[2]*.9);ma.lookAt(0,0,0);mainObj.add(ma);}}
        /* Büyük kraterler */
        var crData=[[.5,.3,.5,.08],[-.4,.5,.4,.07],[.1,-.6,.5,.09],[-.5,-.2,.6,.06],[.3,-.4,.6,.07],[.6,.1,.4,.05],[-.1,.6,.5,.08]];
        for(var i=0;i<crData.length;i++){{var d=crData[i];var cr=_m(new THREE.RingGeometry(d[3]*.7,d[3],16),0xAAAAAA,{{side:THREE.DoubleSide}});cr.position.set(d[0]*.95,d[1]*.95,d[2]*.95);cr.lookAt(0,0,0);mainObj.add(cr);}}
        /* Küçük kraterler */
        for(var i=0;i<25;i++){{var sc=_m(new THREE.RingGeometry(.01,.025,10),0x999999,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;sc.position.set(Math.sin(th)*Math.cos(ph)*.96,Math.cos(th)*.96,Math.sin(th)*Math.sin(ph)*.96);sc.lookAt(0,0,0);mainObj.add(sc);}}
        /* Işık gradyani — terminator cizgisi */
        var term=_mb(new THREE.SphereGeometry(.97,32,32),0x222222,{{transparent:true,opacity:.25,side:THREE.BackSide}});term.position.x=-.4;mainObj.add(term);
        }}

        else if(T==10){{
        /* ===== GUNES — Yildiz, korona, protuberanslar, güneşh lekeleri ===== */
        /* Fotosfer */
        var body=_m(new THREE.SphereGeometry(2.0,32,32),0xFFAA00,{{emissive:new THREE.Color(0xFF6600),emissiveIntensity:.9,shininess:20}});mainObj.add(body);
        /* Granulasyon dokusu */
        for(var i=0;i<30;i++){{var gr=_mb(new THREE.SphereGeometry(.08+Math.random()*.06,8,8),0xFFCC33,{{transparent:true,opacity:.15}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;gr.position.set(Math.sin(th)*Math.cos(ph)*2.02,Math.cos(th)*2.02,Math.sin(th)*Math.sin(ph)*2.02);mainObj.add(gr);}}
        /* Güneş lekeleri */
        for(var i=0;i<6;i++){{var sp=_m(new THREE.CircleGeometry(.06+Math.random()*.08,16),0x662200,{{side:THREE.DoubleSide}});var th=.3+Math.random()*2.5,ph=Math.random()*Math.PI*2;sp.position.set(Math.sin(th)*Math.cos(ph)*2.01,Math.cos(th)*2.01,Math.sin(th)*Math.sin(ph)*2.01);sp.lookAt(0,0,0);mainObj.add(sp);var pe=_mb(new THREE.RingGeometry(.07+i*.01,.12+i*.01,16),0x994400,{{side:THREE.DoubleSide,transparent:true,opacity:.4}});pe.position.copy(sp.position);pe.lookAt(0,0,0);mainObj.add(pe);}}
        /* Kromosfer */
        var chr=_mb(new THREE.SphereGeometry(2.08,24,24),0xFF4400,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});mainObj.add(chr);
        /* Korona — dış atmosfer */
        for(var i=0;i<6;i++){{var co=_mb(new THREE.SphereGeometry(2.2+i*.2,32,32),0xFFDD88,{{transparent:true,opacity:.04-.004*i,side:THREE.DoubleSide}});mainObj.add(co);}}
        /* Protuberanslar — patlama yaylari */
        for(var i=0;i<3;i++){{var pr=_m(new THREE.TorusGeometry(.4+i*.15,.04,12,32),0xFF4400,{{emissive:new THREE.Color(0xFF2200),emissiveIntensity:.6,transparent:true,opacity:.5}});var a=i*2.1;pr.position.set(Math.cos(a)*2.0,Math.sin(a)*2.0,0);pr.rotation.set(Math.random(),Math.random(),Math.random());mainObj.add(pr);}}
        /* Güneş ruzgari partikulleri */
        for(var i=0;i<40;i++){{var sw=_mb(new THREE.SphereGeometry(.02,4,4),0xFFCC66,{{transparent:true,opacity:.3}});var a=Math.random()*Math.PI*2,r=2.5+Math.random()*2;sw.position.set(Math.cos(a)*r,(Math.random()-.5)*3,Math.sin(a)*r);mainObj.add(sw);}}
        }}

        else if(T==11){{
        /* ===== KUYRUKLU YILDIZ — Cekirdek, koma, toz/iyon kuyrugu ===== */
        /* Cekirdek — düzensiz kaya */
        var nuc=_m(new THREE.DodecahedronGeometry(.3,1),0x333322,{{shininess:10}});nuc.scale.set(1.3,.8,.9);mainObj.add(nuc);
        /* Cekirdek yüzey detay */
        for(var i=0;i<8;i++){{var det=_m(new THREE.SphereGeometry(.05+Math.random()*.04,6,6),0x444433,{{shininess:5}});det.position.set((Math.random()-.5)*.4,(Math.random()-.5)*.25,(Math.random()-.5)*.25);mainObj.add(det);}}
        /* Koma — gaz bulutu */
        var koma=_mb(new THREE.SphereGeometry(.7,32,32),0x88BBFF,{{transparent:true,opacity:.12}});mainObj.add(koma);
        var koma2=_mb(new THREE.SphereGeometry(.5,24,24),0xAADDFF,{{transparent:true,opacity:.08}});mainObj.add(koma2);
        /* Iyon kuyrugu — duz, mavi */
        for(var i=0;i<60;i++){{var ip=_mb(new THREE.SphereGeometry(.015+Math.random()*.02,4,4),0x4488FF,{{transparent:true,opacity:.4-i*.005}});ip.position.set(-1.0-i*.08,(Math.random()-.5)*.15-i*.003,(Math.random()-.5)*.1);mainObj.add(ip);}}
        /* Toz kuyrugu — egri, sari */
        for(var i=0;i<50;i++){{var dp=_mb(new THREE.SphereGeometry(.02+Math.random()*.025,4,4),0xFFDD88,{{transparent:true,opacity:.35-i*.005}});var curve=i*.02;dp.position.set(-0.8-i*.07,curve*curve*.8+Math.random()*.08,(Math.random()-.5)*.3+i*.02);mainObj.add(dp);}}
        /* Jet yapilar — aktif bölge */
        for(var i=0;i<4;i++){{var jt=_mb(new THREE.ConeGeometry(.04,.4,6),0xAADDFF,{{transparent:true,opacity:.15}});jt.position.set((Math.random()-.5)*.2,(Math.random()-.5)*.15,(Math.random()-.5)*.2);jt.rotation.z=2+Math.random()*.5;mainObj.add(jt);}}
        }}

        else if(T==12){{
        /* ===== ASTEROID KUSAGI — Mars-Jupiter arasi, çeşitli goktas ===== */
        /* Güneş — küçük referans */
        var sun=_mb(new THREE.SphereGeometry(.15,12,12),0xFFAA00,{{transparent:true,opacity:.8}});sun.material.emissive=new THREE.Color(0xFF6600);sun.material.emissiveIntensity=1;mainObj.add(sun);
        /* Mars yoerungesi */
        var marsO=_m(new THREE.TorusGeometry(1.2,.005,8,80),0xFF4400,{{transparent:true,opacity:.1}});marsO.rotation.x=Math.PI/2;mainObj.add(marsO);
        /* Jupiter yoerungesi */
        var jupO=_m(new THREE.TorusGeometry(2.8,.005,8,80),0xDDAA33,{{transparent:true,opacity:.1}});jupO.rotation.x=Math.PI/2;mainObj.add(jupO);
        /* Ana kuşak asteroidleri */
        for(var i=0;i<120;i++){{var sz=.02+Math.random()*.06;var ast=_m(new THREE.DodecahedronGeometry(sz,0),Math.random()>.5?0x8A7A6A:0x6A6050,{{shininess:15}});var r=1.6+Math.random()*1.0;var a=Math.random()*Math.PI*2;ast.position.set(Math.cos(a)*r,(Math.random()-.5)*.2,Math.sin(a)*r);ast.rotation.set(Math.random()*3,Math.random()*3,Math.random()*3);mainObj.add(ast);}}
        /* Ceres — en büyük asteroidi */
        var ceres=_m(new THREE.SphereGeometry(.1,16,16),0xAAAA99,{{shininess:30}});ceres.position.set(0,0,2.0);mainObj.add(ceres);
        /* Vesta */
        var vesta=_m(new THREE.DodecahedronGeometry(.07,1),0x999988,{{shininess:25}});vesta.position.set(-1.8,0,.5);mainObj.add(vesta);
        /* Trojan asteroidleri (Jupiter L4/L5) */
        for(var i=0;i<15;i++){{var tr=_m(new THREE.DodecahedronGeometry(.02+Math.random()*.03,0),0x776655,{{shininess:10}});var a=1.0+Math.random()*.3;tr.position.set(Math.cos(a)*2.8,(Math.random()-.5)*.1,Math.sin(a)*2.8);mainObj.add(tr);}}
        }}

        else if(T==13){{
        /* ===== IO — Jupiter uydusu, volkanik aktivite ===== */
        var body=_m(new THREE.SphereGeometry(.8,24,24),0xCCBB44,{{shininess:30}});mainObj.add(body);
        /* Volkanik lekeler — sulefirik tuzlar */
        var vClrs=[0xFF4400,0xCC2200,0xFF6600,0xDD3300,0xFF5500];
        for(var i=0;i<12;i++){{var vs=_m(new THREE.CircleGeometry(.05+Math.random()*.08,12),vClrs[i%5],{{side:THREE.DoubleSide,emissive:new THREE.Color(0x331100),emissiveIntensity:.3}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;vs.position.set(Math.sin(th)*Math.cos(ph)*.81,Math.cos(th)*.81,Math.sin(th)*Math.sin(ph)*.81);vs.lookAt(0,0,0);mainObj.add(vs);}}
        /* Aktif volkanlar — patlama plumu */
        for(var i=0;i<4;i++){{var pl=_mb(new THREE.ConeGeometry(.06,.5,8),0xFFAA33,{{transparent:true,opacity:.25}});var th=.5+Math.random()*2,ph=Math.random()*Math.PI*2;pl.position.set(Math.sin(th)*Math.cos(ph)*.9,Math.cos(th)*.9,Math.sin(th)*Math.sin(ph)*.9);pl.lookAt(0,0,0);mainObj.add(pl);}}
        /* Lav akintilari */
        for(var i=0;i<6;i++){{var lv=_m(new THREE.CylinderGeometry(.01,.01,.2,6),0xFF3300,{{emissive:new THREE.Color(0xFF2200),emissiveIntensity:.5}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;lv.position.set(Math.sin(th)*Math.cos(ph)*.82,Math.cos(th)*.82,Math.sin(th)*Math.sin(ph)*.82);lv.lookAt(0,0,0);mainObj.add(lv);}}
        /* Büyük kararti bölgeler */
        for(var i=0;i<5;i++){{var dk=_m(new THREE.CircleGeometry(.04+Math.random()*.06,10),0x665500,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;dk.position.set(Math.sin(th)*Math.cos(ph)*.805,Math.cos(th)*.805,Math.sin(th)*Math.sin(ph)*.805);dk.lookAt(0,0,0);mainObj.add(dk);}}
        }}

        else if(T==14){{
        /* ===== EUROPA — Buzla kapli, catlaklarla dolu okyanus dünyası ===== */
        /* Buz kabugu */
        var body=_m(new THREE.SphereGeometry(.8,24,24),0xCCDDEE,{{shininess:80}});mainObj.add(body);
        /* Yüzey catlaklari — lineae */
        for(var i=0;i<18;i++){{var ln=_m(new THREE.CylinderGeometry(.005,.005,.5+Math.random()*.4,4),0x7A5533,{{shininess:10}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;ln.position.set(Math.sin(th)*Math.cos(ph)*.81,Math.cos(th)*.81,Math.sin(th)*Math.sin(ph)*.81);ln.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(ln);}}
        /* Koyu cizgiler — cekilme catlaklari */
        for(var i=0;i<8;i++){{var dc=_m(new THREE.CylinderGeometry(.008,.008,.3,4),0x554422,{{shininess:5}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;dc.position.set(Math.sin(th)*Math.cos(ph)*.815,Math.cos(th)*.815,Math.sin(th)*Math.sin(ph)*.815);dc.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(dc);}}
        /* Kaos bölgesi — kirilmis buz */
        for(var i=0;i<8;i++){{var ch=_m(new THREE.BoxGeometry(.04,.06,.04),0xAABBCC,{{shininess:60}});ch.position.set(.3+Math.random()*.2,Math.random()*.2-.1,.5+Math.random()*.2);mainObj.add(ch);}}
        /* Alt okyanus parlamasi */
        var oc=_mb(new THREE.SphereGeometry(.72,32,32),0x2244AA,{{transparent:true,opacity:.08}});mainObj.add(oc);
        /* Buz yüzey parlaklık */
        var shine=_mb(new THREE.SphereGeometry(.82,32,32),0xEEEEFF,{{transparent:true,opacity:.05,side:THREE.DoubleSide}});mainObj.add(shine);
        }}

        else if(T==15){{
        /* ===== TITAN — Saturn uydusu, metan denizleri, kalin atmosfer ===== */
        var body=_m(new THREE.SphereGeometry(1.0,24,24),0xBB8833,{{shininess:15}});mainObj.add(body);
        /* Metan denizleri — köyü bölgeler */
        var seaData=[[.2,.7,.5,.15,0x443322],[-.3,.5,.6,.12,0x3A2A1A],[.4,.3,.7,.1,0x4A3828]];
        for(var i=0;i<seaData.length;i++){{var d=seaData[i];var sea=_m(new THREE.CircleGeometry(d[3],16),d[4],{{side:THREE.DoubleSide,shininess:90}});sea.position.set(d[0]*1.01,d[1]*1.01,d[2]*1.01);sea.lookAt(0,0,0);mainObj.add(sea);}}
        /* Kum tepeleri — ekvator bölgesinde */
        for(var i=0;i<10;i++){{var dn=_m(new THREE.ConeGeometry(.03,.06,6),0xAA7722,{{shininess:10}});var a=i*.63;dn.position.set(Math.cos(a)*.98,-.1+Math.random()*.2,Math.sin(a)*.98);dn.rotation.z=Math.random()*.3;mainObj.add(dn);}}
        /* Kalin türüncu atmosfer — 5 katman */
        for(var i=0;i<5;i++){{var atm=_mb(new THREE.SphereGeometry(1.08+i*.06,32,32),0xCC8833,{{transparent:true,opacity:.1-.01*i,side:THREE.DoubleSide}});mainObj.add(atm);}}
        /* Sis katmanlari */
        for(var i=0;i<8;i++){{var hz=_mb(new THREE.SphereGeometry(.1+Math.random()*.12,8,8),0xDDA050,{{transparent:true,opacity:.08}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;hz.position.set(Math.sin(th)*Math.cos(ph)*1.2,Math.cos(th)*1.2,Math.sin(th)*Math.sin(ph)*1.2);hz.scale.set(2,.5,1.3);mainObj.add(hz);}}
        /* Buzlu kriyovolkan */
        var cv=_m(new THREE.ConeGeometry(.06,.12,8),0xDDCCBB,{{shininess:40}});cv.position.set(.5,-.4,.7);cv.lookAt(0,0,0);cv.rotateX(Math.PI);mainObj.add(cv);
        }}

        else if(T==16){{
        /* ===== GANYMEDE — En büyük uydu, oluklu arazi, manyetik alan ===== */
        var body=_m(new THREE.SphereGeometry(.9,24,24),0x8899AA,{{shininess:30}});mainObj.add(body);
        /* Acik bölgeler — oluklu arazi */
        for(var i=0;i<8;i++){{var lt=_m(new THREE.CircleGeometry(.1+Math.random()*.08,16),0xAABBCC,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;lt.position.set(Math.sin(th)*Math.cos(ph)*.91,Math.cos(th)*.91,Math.sin(th)*Math.sin(ph)*.91);lt.lookAt(0,0,0);mainObj.add(lt);}}
        /* Koyu bölgeler — eski yüzey */
        for(var i=0;i<6;i++){{var dk=_m(new THREE.CircleGeometry(.08+Math.random()*.06,12),0x556677,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;dk.position.set(Math.sin(th)*Math.cos(ph)*.905,Math.cos(th)*.905,Math.sin(th)*Math.sin(ph)*.905);dk.lookAt(0,0,0);mainObj.add(dk);}}
        /* Oluklar — paralel cizgiler */
        for(var i=0;i<12;i++){{var gr=_m(new THREE.CylinderGeometry(.003,.003,.3,4),0xBBCCDD,{{shininess:40}});var th=.5+Math.random()*2,ph=Math.random()*Math.PI*2;gr.position.set(Math.sin(th)*Math.cos(ph)*.91,Math.cos(th)*.91,Math.sin(th)*Math.sin(ph)*.91);gr.lookAt(0,0,0);gr.rotateZ(Math.PI/2+i*.05);mainObj.add(gr);}}
        /* Kraterler */
        for(var i=0;i<10;i++){{var cr=_m(new THREE.RingGeometry(.015,.03,10),0x778899,{{side:THREE.DoubleSide}});var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cr.position.set(Math.sin(th)*Math.cos(ph)*.91,Math.cos(th)*.91,Math.sin(th)*Math.sin(ph)*.91);cr.lookAt(0,0,0);mainObj.add(cr);}}
        /* Manyetik alan cizgileri */
        for(var i=0;i<4;i++){{var mg=_m(new THREE.TorusGeometry(1.1+i*.15,.003,8,48),0x4488FF,{{transparent:true,opacity:.08}});mg.rotation.x=Math.PI/2+i*.15;mainObj.add(mg);}}
        }}

        else if(T==17){{
        /* ===== SAMANYOLU — Spiral galaksi yapisal modeli ===== */
        /* Galaktik merkez — siskin yapi */
        var core=_mb(new THREE.SphereGeometry(.35,12,12),0xFFDD88,{{transparent:true,opacity:.6}});mainObj.add(core);
        var core2=_mb(new THREE.SphereGeometry(.25,24,24),0xFFCC66,{{transparent:true,opacity:.8}});mainObj.add(core2);
        var coreG=_mb(new THREE.SphereGeometry(.5,24,24),0xFFEEAA,{{transparent:true,opacity:.15}});mainObj.add(coreG);
        /* Galaktik disk — yassı */
        var disk=_mb(new THREE.CylinderGeometry(2.5,2.5,.06,64),0x555566,{{transparent:true,opacity:.08}});mainObj.add(disk);
        /* Spiral kollar — 4 ana kol */
        for(var arm=0;arm<4;arm++){{var offset=arm*Math.PI/2;for(var i=0;i<80;i++){{var a=offset+i*.1;var r=.4+i*.025;var st=_mb(new THREE.SphereGeometry(.02+Math.random()*.03,4,4),new THREE.Color().setHSL(.12+Math.random()*.08,.3+Math.random()*.3,.5+Math.random()*.3),{{transparent:true,opacity:.4+Math.random()*.3}});st.position.set(Math.cos(a)*r,(Math.random()-.5)*.06,Math.sin(a)*r);mainObj.add(st);}}}}
        /* Parlak yildiz kmeleri — spiral kollarda */
        for(var i=0;i<20;i++){{var cl=_mb(new THREE.SphereGeometry(.04+Math.random()*.03,6,6),0xFFEECC,{{transparent:true,opacity:.5}});var a=Math.random()*Math.PI*2,r=.5+Math.random()*2;cl.position.set(Math.cos(a)*r,(Math.random()-.5)*.04,Math.sin(a)*r);mainObj.add(cl);}}
        /* Güneş konumu göstergesi */
        var sunPos=_mb(new THREE.SphereGeometry(.03,8,8),0xFFFF00,{{transparent:false}});sunPos.position.set(1.3,0,.3);mainObj.add(sunPos);
        var sunRing=_m(new THREE.TorusGeometry(.06,.005,8,16),0xFFFF00,{{transparent:true,opacity:.5}});sunRing.position.copy(sunPos.position);sunRing.rotation.x=Math.PI/2;mainObj.add(sunRing);
        /* Halo — kuresel kumeler */
        for(var i=0;i<15;i++){{var gc=_mb(new THREE.SphereGeometry(.02,4,4),0xAAAA88,{{transparent:true,opacity:.25}});gc.position.set((Math.random()-.5)*4,(Math.random()-.5)*1.5,(Math.random()-.5)*4);mainObj.add(gc);}}
        }}

        else if(T==18){{
        /* ===== KARA DELIK — Olay ufku, akreasyon diski, jet, gravitasyonel lensleme ===== */
        /* Tekillik noktası */
        var sing=_mb(new THREE.SphereGeometry(.15,12,12),0x000000);mainObj.add(sing);
        /* Olay ufku */
        var eh=_m(new THREE.SphereGeometry(.5,24,24),0x050505,{{shininess:0}});mainObj.add(eh);
        /* Foton küresi */
        var ps=_mb(new THREE.SphereGeometry(.6,32,32),0x111111,{{transparent:true,opacity:.4}});mainObj.add(ps);
        /* Akreasyon diski — çok katmanli sıcak gaz */
        var diskClrs=[0xFF2200,0xFF6600,0xFFAA00,0xFFDD00,0xFFFF88];
        for(var i=0;i<5;i++){{var ad=_m(new THREE.TorusGeometry(1.2+i*.3,.08-.01*i,16,80),diskClrs[i],{{emissive:new THREE.Color(diskClrs[i]),emissiveIntensity:.5-.05*i,transparent:true,opacity:.6-.08*i}});ad.rotation.x=1.3;mainObj.add(ad);}}
        /* Ince iç halka — ISCO */
        var isco=_m(new THREE.TorusGeometry(.8,.03,12,48),0xFFFFCC,{{emissive:new THREE.Color(0xFFDD00),emissiveIntensity:.8,transparent:true,opacity:.5}});isco.rotation.x=1.3;mainObj.add(isco);
        /* Relativistik jetler — ust ve alt */
        for(var j=0;j<2;j++){{var dir=j==0?1:-1;for(var i=0;i<15;i++){{var jt=_mb(new THREE.ConeGeometry(.06-.003*i,.25,8),0x6688FF,{{transparent:true,opacity:.4-.02*i}});jt.position.y=dir*(.8+i*.25);if(j==1)jt.rotation.x=Math.PI;mainObj.add(jt);}}var jtG=_mb(new THREE.SphereGeometry(.12,12,12),0xAABBFF,{{transparent:true,opacity:.15}});jtG.position.y=dir*4.2;mainObj.add(jtG);}}
        /* Gravitasyonel lensleme efekti — arka arkaya halkalar */
        for(var i=0;i<3;i++){{var lr=_m(new THREE.TorusGeometry(.7+i*.1,.01,8,48),0xFFCC44,{{transparent:true,opacity:.1}});lr.rotation.y=.5+i*.3;mainObj.add(lr);}}
        /* Gaz spiralleri — akreasyon */
        for(var i=0;i<20;i++){{var gs=_mb(new THREE.SphereGeometry(.02,4,4),0xFF8844,{{transparent:true,opacity:.3}});var a=i*.4;var r=2.5-i*.08;gs.position.set(Math.cos(a)*r,Math.sin(i*.2)*.2,Math.sin(a)*r);mainObj.add(gs);}}
        }}

        else if(T==19){{
        /* ===== NEBULA — Kartal Nebulasi tarzi, yildiz doğum bölgesi ===== */
        /* Ana nebula bulutu — çok katmanli */
        for(var i=0;i<8;i++){{var nb=_mb(new THREE.SphereGeometry(.6+Math.random()*.8,16,16),new THREE.Color().setHSL(.75+Math.random()*.15,.5,.3+Math.random()*.2),{{transparent:true,opacity:.08+Math.random()*.04}});nb.position.set((Math.random()-.5)*1.5,(Math.random()-.5)*2,(Math.random()-.5)*1.5);nb.scale.set(1.5+Math.random(),2+Math.random(),1+Math.random());mainObj.add(nb);}}
        /* Sutunlar — "Yaratilishin Sutunlari" tarzi */
        for(var p=0;p<3;p++){{var pillar=_mb(new THREE.CylinderGeometry(.12+p*.04,.2+p*.03,2+Math.random(),12),new THREE.Color().setHSL(.72,.4,.2),{{transparent:true,opacity:.15}});pillar.position.set(-.6+p*.6,-0.3,0);mainObj.add(pillar);for(var d=0;d<5;d++){{var det=_mb(new THREE.SphereGeometry(.06+Math.random()*.08,8,8),new THREE.Color().setHSL(.7+Math.random()*.1,.3,.25),{{transparent:true,opacity:.1}});det.position.set(-.6+p*.6+Math.random()*.2,-.3+Math.random()*2,(Math.random()-.5)*.3);mainObj.add(det);}}}}
        /* Yeni doğan yildizlar — parlak */
        for(var i=0;i<6;i++){{var ns=_mb(new THREE.SphereGeometry(.04+Math.random()*.03,8,8),0xFFFFCC,{{transparent:false}});ns.position.set((Math.random()-.5)*2,(Math.random()-.5)*2.5,(Math.random()-.5)*1.5);mainObj.add(ns);var nsG=_mb(new THREE.SphereGeometry(.08+Math.random()*.05,8,8),0xFFEEAA,{{transparent:true,opacity:.2}});nsG.position.copy(ns.position);mainObj.add(nsG);}}
        /* Emisyon gazi — kirmizi H-alpha */
        for(var i=0;i<12;i++){{var em=_mb(new THREE.SphereGeometry(.15+Math.random()*.2,8,8),0xFF3355,{{transparent:true,opacity:.06}});em.position.set((Math.random()-.5)*3,(Math.random()-.5)*3,(Math.random()-.5)*2);mainObj.add(em);}}
        /* Yansima nebulasi — mavi */
        for(var i=0;i<8;i++){{var rn=_mb(new THREE.SphereGeometry(.1+Math.random()*.15,8,8),0x4488FF,{{transparent:true,opacity:.05}});rn.position.set((Math.random()-.5)*2.5,(Math.random()-.5)*2.5,(Math.random()-.5)*2);mainObj.add(rn);}}
        /* Arka plan yildizlar */
        for(var i=0;i<80;i++){{var st=_mb(new THREE.SphereGeometry(.01+Math.random()*.015,4,4),0xFFFFFF,{{transparent:true,opacity:.3+Math.random()*.4}});st.position.set((Math.random()-.5)*6,(Math.random()-.5)*6,(Math.random()-.5)*6);mainObj.add(st);}}
        }}

        /* Uzay arka plan yildizlari — tum sahneler için */
        var sG=new THREE.BufferGeometry();var sP=[];for(var i=0;i<500;i++)sP.push((Math.random()-.5)*50,(Math.random()-.5)*50,(Math.random()-.5)*50);sG.setAttribute('position',new THREE.Float32BufferAttribute(sP,3));scene.add(new THREE.Points(sG,new THREE.PointsMaterial({{color:0xffffff,size:.06}})));
        scene.add(mainObj);"""

    if ci == 1:  # Atom Modelleri — 20 Premium 3D Sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        var _m=function(g,c,o){{var mt=new THREE.MeshPhongMaterial({{color:c,shininess:60}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        var _mb=function(g,c,o){{var mt=new THREE.MeshBasicMaterial({{color:c}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        /* Atom parametreleri: [proton, nötron, elektron_katmanlari, cekirdek_renk, elektron_renkleri] */
        var AD=[
        [1,0,[1],0xFF4444,[0x00CCFF]],
        [2,2,[2],0xFF6644,[0x00CCFF]],
        [3,4,[2,1],0xFF4444,[0x00CCFF,0x00FF88]],
        [6,6,[2,4],0xFF4444,[0x00CCFF,0x00FF88]],
        [7,7,[2,5],0xFF4444,[0x00CCFF,0x00FF88]],
        [8,8,[2,6],0xFF4444,[0x00CCFF,0xFF8800]],
        [10,10,[2,8],0xFF4444,[0x00CCFF,0xFF8800]],
        [11,12,[2,8,1],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF]],
        [26,30,[2,8,14,2],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00]],
        [79,118,[2,8,18,32,18,1],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00,0x00FFFF,0xFF6688]],
        [29,35,[2,8,18,1],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00]],
        [47,61,[2,8,18,18,1],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00,0x00FFFF]],
        [92,146,[2,8,18,32,21,9,2],0x44FF44,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00,0x00FFFF,0xFF6688,0xAAFF00]],
        [20,20,[2,8,8,2],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00]],
        [19,20,[2,8,8,1],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00]],
        [17,18,[2,8,7],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF]],
        [15,16,[2,8,5],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF]],
        [16,16,[2,8,6],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF]],
        [14,14,[2,8,4],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF]],
        [22,26,[2,8,10,2],0xFF4444,[0x00CCFF,0xFF8800,0xFF00FF,0xFFFF00]]
        ];
        var d=AD[T];var np=d[0],nn=d[1],shells=d[2],nucClr=d[3],eClrs=d[4];

        /* ===== CEKIRDEK — Proton ve Nötron Kumesi ===== */
        var nucR=Math.pow(np+nn,.333)*.08+.2;
        var nucG=new THREE.Group();
        /* Protonlar — kirmizi */
        for(var i=0;i<Math.min(np,30);i++){{
            var pr=_m(new THREE.SphereGeometry(.055,10,10),0xFF3333,{{shininess:80,emissive:new THREE.Color(0x441111),emissiveIntensity:.2}});
            var phi=Math.acos(1-2*(i+.5)/Math.max(np+nn,1));var theta=Math.PI*(1+Math.sqrt(5))*i;
            var r=nucR*.75;pr.position.set(r*Math.sin(phi)*Math.cos(theta),r*Math.cos(phi),r*Math.sin(phi)*Math.sin(theta));
            nucG.add(pr);
        }}
        /* Nötronlar — mavi */
        for(var i=0;i<Math.min(nn,30);i++){{
            var nt=_m(new THREE.SphereGeometry(.055,10,10),0x3366CC,{{shininess:80,emissive:new THREE.Color(0x111144),emissiveIntensity:.2}});
            var phi=Math.acos(1-2*(i+np+.5)/Math.max(np+nn,1));var theta=Math.PI*(1+Math.sqrt(5))*(i+np);
            var r=nucR*.75;nt.position.set(r*Math.sin(phi)*Math.cos(theta),r*Math.cos(phi),r*Math.sin(phi)*Math.sin(theta));
            nucG.add(nt);
        }}
        /* Cekirdek pariltisi */
        var nucGlow=_mb(new THREE.SphereGeometry(nucR*1.2,24,24),nucClr,{{transparent:true,opacity:.12}});nucG.add(nucGlow);
        var nucGlow2=_mb(new THREE.SphereGeometry(nucR*1.5,20,20),nucClr,{{transparent:true,opacity:.06}});nucG.add(nucGlow2);
        mainObj.add(nucG);

        /* ===== ELEKTRON KABUKLARI ve ORBITLERI ===== */
        window._orbits=[];
        for(var s=0;s<shells.length;s++){{
            var ne=shells[s];var oR=.7+s*.55;var clr=eClrs[s%eClrs.length];
            /* Orbital yolu — 3 eksenli torus */
            for(var ax=0;ax<3;ax++){{
                var orb=_m(new THREE.TorusGeometry(oR,.006,8,80),clr,{{transparent:true,opacity:.12+.04*Math.random()}});
                if(ax==0)orb.rotation.x=Math.PI/2+s*.15;
                else if(ax==1)orb.rotation.y=Math.PI/3+s*.2;
                else orb.rotation.set(Math.PI/4+s*.1,Math.PI/6,0);
                mainObj.add(orb);
            }}
            /* Elektronlar */
            for(var e=0;e<Math.min(ne,8);e++){{
                var el=_m(new THREE.SphereGeometry(.06,12,12),clr,{{emissive:new THREE.Color(clr),emissiveIntensity:.6,shininess:100}});
                var elGlow=_mb(new THREE.SphereGeometry(.1,8,8),clr,{{transparent:true,opacity:.2}});
                var eG=new THREE.Group();eG.add(el);eG.add(elGlow);
                var a=e*Math.PI*2/ne;eG.position.set(Math.cos(a)*oR,Math.sin(a)*oR*.3,Math.sin(a)*oR*.9);
                var oGrp=new THREE.Group();oGrp.add(eG);
                oGrp.rotation.x=Math.PI/2+s*.15+e*.3;
                oGrp.rotation.z=s*.4+e*.2;
                mainObj.add(oGrp);
                window._orbits.push({{el:eG,spd:.015+s*.005+e*.002,rad:oR,grp:oGrp}});
            }}
            /* Kabuk siniri — saydam kure */
            var shell=_mb(new THREE.SphereGeometry(oR+.05,24,24),clr,{{transparent:true,opacity:.03,side:THREE.DoubleSide}});
            mainObj.add(shell);
        }}

        /* ===== ATOM BAZINDA OZEL EFEKTLER ===== */
        if(T==0){{
            /* Hidrojen — elektron olasilik bulutu (1s orbitali) */
            for(var i=0;i<30;i++){{var cl=_mb(new THREE.SphereGeometry(.015,4,4),0x00CCFF,{{transparent:true,opacity:.15}});var r=.3+Math.random()*.6;var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;cl.position.set(r*Math.sin(th)*Math.cos(ph),r*Math.cos(th),r*Math.sin(th)*Math.sin(ph));mainObj.add(cl);}}
        }}
        if(T==3){{
            /* Karbon — sp3 hibrit baglari gosterimi */
            var bDirs=[[0,1,0],[.94,-.33,0],[-.47,-.33,.82],[-.47,-.33,-.82]];
            for(var i=0;i<4;i++){{var bd=_m(new THREE.CylinderGeometry(.015,.015,.5,6),0xAAFFAA,{{transparent:true,opacity:.3}});var d=bDirs[i];bd.position.set(d[0]*.3,d[1]*.3,d[2]*.3);bd.lookAt(d[0],d[1],d[2]);bd.rotateX(Math.PI/2);mainObj.add(bd);var tip=_m(new THREE.SphereGeometry(.04,8,8),0xAAFFAA,{{transparent:true,opacity:.4}});tip.position.set(d[0]*.55,d[1]*.55,d[2]*.55);mainObj.add(tip);}}
        }}
        if(T==5){{
            /* Oksijen — p orbitali lobları */
            for(var i=0;i<2;i++){{var lobe=_mb(new THREE.SphereGeometry(.18,12,12),0xFF8800,{{transparent:true,opacity:.08}});lobe.position.y=i==0?.5:-.5;lobe.scale.set(.6,1,.6);mainObj.add(lobe);}}
        }}
        if(T==8){{
            /* Demir — d orbitali şekli ve manyetik alan cizgileri */
            for(var i=0;i<4;i++){{var mg=_m(new THREE.TorusGeometry(2.0+i*.15,.003,8,48),0x4488FF,{{transparent:true,opacity:.06}});mg.rotation.x=Math.PI/2;mg.rotation.z=i*.2;mainObj.add(mg);}}
        }}
        if(T==9){{
            /* Altin — relativistik 6s orbitali daralmasi (parlak sari) */
            var relGlow=_mb(new THREE.SphereGeometry(.3,16,16),0xFFDD00,{{transparent:true,opacity:.15}});mainObj.add(relGlow);
            for(var i=0;i<20;i++){{var gp=_mb(new THREE.SphereGeometry(.01,4,4),0xFFCC00,{{transparent:true,opacity:.2}});var r=.15+Math.random()*.15;var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;gp.position.set(r*Math.sin(th)*Math.cos(ph),r*Math.cos(th),r*Math.sin(th)*Math.sin(ph));mainObj.add(gp);}}
        }}
        if(T==12){{
            /* Uranyum — radyoaktif bözünma partikulleri */
            for(var i=0;i<8;i++){{var rp=_mb(new THREE.SphereGeometry(.02,4,4),0x44FF44,{{transparent:true,opacity:.4}});var a=Math.random()*Math.PI*2,r=nucR*1.5+Math.random()*1.5;rp.position.set(Math.cos(a)*r,(Math.random()-.5)*1.5,Math.sin(a)*r);mainObj.add(rp);}}
            var radGlow=_mb(new THREE.SphereGeometry(nucR*2,16,16),0x44FF44,{{transparent:true,opacity:.04}});mainObj.add(radGlow);
        }}

        /* Enerji seviyesi cizgileri — etiket */
        for(var s=0;s<shells.length;s++){{
            var lv=_m(new THREE.TorusGeometry(.7+s*.55,.002,8,64),0x888888,{{transparent:true,opacity:.06}});
            lv.rotation.x=Math.PI/2;mainObj.add(lv);
        }}
        scene.add(mainObj);"""

    if ci == 2:  # Hüçre Biyolojisi — 20 Premium 3D Sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        var _m=function(g,c,o){{var mt=new THREE.MeshPhongMaterial({{color:c,shininess:60}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        var _mb=function(g,c,o){{var mt=new THREE.MeshBasicMaterial({{color:c}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};

        if(T==0){{
        /* ===== HAYVAN HUCRESI ===== */
        /* Hüçre zari — saydam kure */
        var mem=_mb(new THREE.SphereGeometry(1.7,24,24),0x88CC88,{{transparent:true,opacity:.1,side:THREE.DoubleSide}});mainObj.add(mem);
        var mem2=_mb(new THREE.SphereGeometry(1.72,24,24),0x66AA66,{{transparent:true,opacity:.05,side:THREE.DoubleSide}});mainObj.add(mem2);
        /* Cekirdek — cift zar */
        var nuc=_m(new THREE.SphereGeometry(.5,12,12),0x6644AA,{{shininess:70,emissive:new THREE.Color(0x220044),emissiveIntensity:.2}});mainObj.add(nuc);
        var nucMem=_mb(new THREE.SphereGeometry(.53,32,32),0x8866CC,{{transparent:true,opacity:.15,side:THREE.DoubleSide}});mainObj.add(nucMem);
        /* Cekirdekçik */
        var nucl=_m(new THREE.SphereGeometry(.15,16,16),0x4422AA,{{emissive:new THREE.Color(0x220055),emissiveIntensity:.3}});nucl.position.set(.1,.1,0);mainObj.add(nucl);
        /* Kromatin */
        for(var i=0;i<6;i++){{var ch=_m(new THREE.TorusGeometry(.2+i*.04,.02,8,24),0x7755BB,{{transparent:true,opacity:.3}});ch.position.set(Math.random()*.15,Math.random()*.15,0);ch.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(ch);}}
        /* Mitokondri — fasulye */
        for(var i=0;i<5;i++){{var mt=_m(new THREE.SphereGeometry(.12,12,12),0xDD6633,{{shininess:40}});mt.scale.set(1.8,.8,.9);var a=.8+i*1.2;mt.position.set(Math.cos(a)*1.0,(Math.random()-.5)*.6,Math.sin(a)*1.0);mt.rotation.z=Math.random()*2;mainObj.add(mt);/* Krista */for(var j=0;j<3;j++){{var kr=_m(new THREE.BoxGeometry(.15,.01,.06),0xCC5522);kr.position.copy(mt.position);kr.position.x+=j*.04-.04;mainObj.add(kr);}}}}
        /* ER — kanal ag */
        for(var i=0;i<8;i++){{var er=_m(new THREE.TorusGeometry(.3+i*.05,.02,8,24),0x4488CC,{{transparent:true,opacity:.2}});er.position.set(-.3+i*.08,.2-.1*i,.3);er.rotation.set(Math.random(),Math.random(),0);mainObj.add(er);}}
        /* Golgi — yassı sisternalar */
        for(var i=0;i<5;i++){{var go=_m(new THREE.CylinderGeometry(.25,.25,.03,16),0xFFCC33,{{transparent:true,opacity:.4}});go.position.set(.8,.1+i*.06,-.3);go.scale.set(1,.5+Math.sin(i*.5)*.2,1);mainObj.add(go);}}
        /* Lizozomlar */
        for(var i=0;i<4;i++){{var lz=_m(new THREE.SphereGeometry(.07,10,10),0xCC4466,{{emissive:new THREE.Color(0x441122),emissiveIntensity:.2}});lz.position.set((Math.random()-.5)*1.2,(Math.random()-.5)*.8,(Math.random()-.5)*1.2);mainObj.add(lz);}}
        /* Sentrozom */
        var cen1=_m(new THREE.CylinderGeometry(.04,.04,.18,9),0x888888,{{shininess:80}});cen1.position.set(.15,-.6,0);mainObj.add(cen1);
        var cen2=_m(new THREE.CylinderGeometry(.04,.04,.18,9),0x888888,{{shininess:80}});cen2.position.set(.15,-.6,0);cen2.rotation.z=Math.PI/2;mainObj.add(cen2);
        /* Ribozomlar — küçük noktalar */
        for(var i=0;i<30;i++){{var rb=_m(new THREE.SphereGeometry(.025,6,6),0xAACC33);rb.position.set((Math.random()-.5)*2.5,(Math.random()-.5)*1.5,(Math.random()-.5)*2.5);if(rb.position.length()>1.6)rb.position.multiplyScalar(1.5/rb.position.length());mainObj.add(rb);}}
        }}

        else if(T==1){{
        /* ===== BITKI HUCRESI ===== */
        /* Hüçre duvari — dikdörtgen prizma */
        var wall=_mb(new THREE.BoxGeometry(3.2,2.2,2.2),0x228833,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});mainObj.add(wall);
        var wall2=_mb(new THREE.BoxGeometry(3.3,2.3,2.3),0x116622,{{transparent:true,opacity:.05,side:THREE.DoubleSide}});mainObj.add(wall2);
        /* Hüçre zari */
        var mem=_mb(new THREE.BoxGeometry(3.0,2.0,2.0),0x66AA66,{{transparent:true,opacity:.06,side:THREE.DoubleSide}});mainObj.add(mem);
        /* Büyük merkezi vakuol */
        var vac=_mb(new THREE.SphereGeometry(.9,32,32),0x4488CC,{{transparent:true,opacity:.12}});vac.position.set(0,0,0);vac.scale.set(1.4,1,.9);mainObj.add(vac);
        var vacM=_mb(new THREE.SphereGeometry(.92,28,28),0x3377BB,{{transparent:true,opacity:.06,side:THREE.DoubleSide}});vacM.scale.copy(vac.scale);mainObj.add(vacM);
        /* Cekirdek — kenara itilmis */
        var nuc=_m(new THREE.SphereGeometry(.3,24,24),0x6644AA,{{shininess:70}});nuc.position.set(1.1,.3,0);mainObj.add(nuc);
        var nucl=_m(new THREE.SphereGeometry(.1,12,12),0x4422AA);nucl.position.set(1.15,.35,0);mainObj.add(nucl);
        /* Kloroplastlar */
        for(var i=0;i<6;i++){{var kl=_m(new THREE.SphereGeometry(.12,12,12),0x44AA44,{{shininess:40}});kl.scale.set(1.6,.6,.9);kl.position.set((Math.random()-.5)*2,(Math.random()-.5)*1.2,(Math.random()-.5)*1.2);mainObj.add(kl);/* Grana */for(var j=0;j<3;j++){{var gr=_m(new THREE.CylinderGeometry(.06,.06,.015,8),0x338833);gr.position.copy(kl.position);gr.position.y+=j*.03-.03;mainObj.add(gr);}}}}
        /* Mitokondri */
        for(var i=0;i<3;i++){{var mt=_m(new THREE.SphereGeometry(.09,10,10),0xDD6633);mt.scale.set(1.5,.8,.8);mt.position.set((Math.random()-.5)*2,(Math.random()-.5)*1,(Math.random()-.5)*1);mainObj.add(mt);}}
        /* ER */
        for(var i=0;i<5;i++){{var er=_m(new THREE.TorusGeometry(.2,.015,8,20),0x6688AA,{{transparent:true,opacity:.2}});er.position.set(.6+i*.08,-.2-.1*i,.4);er.rotation.set(Math.random(),0,0);mainObj.add(er);}}
        /* Plasmodesmata — hüçre duvari delikleri */
        for(var i=0;i<8;i++){{var pd=_m(new THREE.CylinderGeometry(.02,.02,.2,6),0x558844);pd.position.set(1.55,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);pd.rotation.z=Math.PI/2;mainObj.add(pd);}}
        }}

        else if(T==2){{
        /* ===== BAKTERI ===== */
        /* Hüçre duvari — kapsul */
        var cap=_mb(new THREE.SphereGeometry(1.15,32,32),0x88BBCC,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});cap.scale.set(1.5,.8,.8);mainObj.add(cap);
        /* Hüçre zari */
        var mem=_m(new THREE.SphereGeometry(1.0,32,32),0x66AA88,{{transparent:true,opacity:.15,side:THREE.DoubleSide}});mem.scale.set(1.5,.8,.8);mainObj.add(mem);
        /* Nukleoid — dairesel DNA */
        var dna=_m(new THREE.TorusGeometry(.3,.03,12,32),0x4488CC,{{emissive:new THREE.Color(0x112244),emissiveIntensity:.3}});mainObj.add(dna);
        var dna2=_m(new THREE.TorusGeometry(.25,.02,8,24),0x5599DD,{{transparent:true,opacity:.5}});dna2.rotation.x=.5;mainObj.add(dna2);
        /* Plazmidler */
        for(var i=0;i<3;i++){{var pl=_m(new THREE.TorusGeometry(.08,.015,8,16),0x66CCFF);pl.position.set(.5-.3*i,(Math.random()-.5)*.3,.3);mainObj.add(pl);}}
        /* Ribozomlar */
        for(var i=0;i<40;i++){{var rb=_m(new THREE.SphereGeometry(.02,4,4),0xAACC33);rb.position.set((Math.random()-.5)*2,(Math.random()-.5)*.9,(Math.random()-.5)*.9);mainObj.add(rb);}}
        /* Flagellum — kamci */
        for(var i=0;i<25;i++){{var fl=_m(new THREE.SphereGeometry(.015,4,4),0xCCBB88);fl.position.set(-1.5-i*.08,Math.sin(i*.8)*.15,Math.cos(i*.8)*.15);mainObj.add(fl);}}
        /* Pili */
        for(var i=0;i<8;i++){{var pi=_m(new THREE.CylinderGeometry(.008,.008,.4,4),0xBBAA88);var a=i*.8;pi.position.set(Math.cos(a)*1.1,.4*Math.sin(a),Math.sin(a)*.6);pi.lookAt(Math.cos(a)*2,.4*Math.sin(a),Math.sin(a)*1.2);pi.rotateX(Math.PI/2);mainObj.add(pi);}}
        }}

        else if(T==3){{
        /* ===== MITOKONDRI — Detayli kesit ===== */
        /* Dis zar */
        var outer=_m(new THREE.SphereGeometry(1.0,32,32),0xDD6633,{{transparent:true,opacity:.2,side:THREE.DoubleSide}});outer.scale.set(1.6,.9,.9);mainObj.add(outer);
        /* Ic zar — kristali */
        var inner=_m(new THREE.SphereGeometry(.85,32,32),0xCC5522,{{transparent:true,opacity:.15,side:THREE.DoubleSide}});inner.scale.set(1.5,.8,.8);mainObj.add(inner);
        /* Kristalar — iç zar kivrimlari */
        for(var i=0;i<7;i++){{var cr=_m(new THREE.BoxGeometry(.03,.5,.5),0xCC5522,{{transparent:true,opacity:.4}});cr.position.x=-.8+i*.25;cr.scale.y=.5+Math.random()*.5;mainObj.add(cr);}}
        /* Matriks — jel */
        var mat=_mb(new THREE.SphereGeometry(.75,24,24),0xEE8844,{{transparent:true,opacity:.06}});mat.scale.set(1.4,.7,.7);mainObj.add(mat);
        /* mtDNA — küçük dairesel */
        var mtd=_m(new THREE.TorusGeometry(.12,.02,8,16),0x4488CC,{{emissive:new THREE.Color(0x112244),emissiveIntensity:.3}});mtd.position.set(-.3,.2,0);mainObj.add(mtd);
        /* Ribozomlar */
        for(var i=0;i<10;i++){{var rb=_m(new THREE.SphereGeometry(.02,4,4),0xAACC33);rb.position.set((Math.random()-.5)*1.8,(Math.random()-.5)*.6,(Math.random()-.5)*.6);mainObj.add(rb);}}
        /* ATP sentaz — iç zar üzerinde */
        for(var i=0;i<5;i++){{var atp=_m(new THREE.CylinderGeometry(.03,.03,.1,8),0xFFCC33,{{emissive:new THREE.Color(0x664400),emissiveIntensity:.3}});atp.position.set(-.6+i*.3,-.5,0);mainObj.add(atp);var head=_m(new THREE.SphereGeometry(.04,8,8),0xFFDD44);head.position.copy(atp.position);head.position.y-=.07;mainObj.add(head);}}
        /* Zarlar arasi bosluk etiketi */
        var gap=_mb(new THREE.TorusGeometry(.95,.01,8,32),0xFFAA66,{{transparent:true,opacity:.1}});gap.scale.set(1.55,.85,.85);gap.rotation.y=Math.PI/2;mainObj.add(gap);
        }}

        else if(T==4){{
        /* ===== RIBOZOM — Büyük ve küçük alt birim ===== */
        /* Büyük alt birim (60S) */
        var big=_m(new THREE.SphereGeometry(.7,32,32),0x6688AA,{{shininess:40}});big.scale.set(1,.8,1);big.position.y=-.1;mainObj.add(big);
        /* Küçük alt birim (40S) */
        var small=_m(new THREE.SphereGeometry(.5,28,28),0x88AACC,{{shininess:40}});small.scale.set(1.1,.5,.9);small.position.y=.45;mainObj.add(small);
        /* mRNA — zar şeklinde gecen iplik */
        for(var i=0;i<30;i++){{var mr=_m(new THREE.SphereGeometry(.025,4,4),0xFF6644);mr.position.set(-1.5+i*.1,Math.sin(i*.4)*.05+.25,0);mainObj.add(mr);}}
        var mrLine=_m(new THREE.CylinderGeometry(.01,.01,3,6),0xFF6644,{{transparent:true,opacity:.3}});mrLine.position.y=.25;mrLine.rotation.z=Math.PI/2;mainObj.add(mrLine);
        /* tRNA — yonca yapragi */
        var trna=_m(new THREE.SphereGeometry(.12,12,12),0x44CC88);trna.position.set(.15,.25,.5);mainObj.add(trna);
        var trnaS=_m(new THREE.CylinderGeometry(.02,.02,.3,6),0x44CC88);trnaS.position.set(.15,.1,.5);mainObj.add(trnaS);
        var aa=_m(new THREE.SphereGeometry(.06,8,8),0xFFAA33);aa.position.set(.15,-.05,.5);mainObj.add(aa);
        /* A,P,E bölgeleri */
        var sites=[['A',.3,0xFF4444],['P',0,0x44FF44],['E',-.3,0x4444FF]];
        for(var i=0;i<3;i++){{var s=_mb(new THREE.RingGeometry(.08,.12,12),sites[i][2],{{transparent:true,opacity:.3,side:THREE.DoubleSide}});s.position.set(sites[i][1],.25,.01);s.rotation.y=Math.PI/2;mainObj.add(s);}}
        /* Polipeptid zinciri — çıkış */
        for(var i=0;i<8;i++){{var pp=_m(new THREE.SphereGeometry(.04,6,6),0xDDAA33);pp.position.set(-.5-i*.1,-.2+Math.sin(i)*.1,.1);mainObj.add(pp);}}
        }}

        else if(T==5){{
        /* ===== GOLGI AYGITI — Sisternalar ve vezikuller ===== */
        /* Sisterna yiginlari */
        for(var i=0;i<6;i++){{var cis=_m(new THREE.CylinderGeometry(.8-.05*i,.8-.05*i,.04,24),0xFFCC33,{{transparent:true,opacity:.35+i*.05}});cis.position.y=i*.12-.3;cis.scale.set(1,.8+Math.sin(i*.5)*.1,1);mainObj.add(cis);var edge=_m(new THREE.TorusGeometry(.78-.05*i,.02,8,32),0xDDAA22,{{transparent:true,opacity:.25}});edge.position.y=i*.12-.3;mainObj.add(edge);}}
        /* Sis yüzu etiketi */
        var cisL=_mb(new THREE.SphereGeometry(.05,8,8),0x4488CC);cisL.position.set(-1.1,-.3,0);mainObj.add(cisL);
        /* Trans yüzu */
        var transL=_mb(new THREE.SphereGeometry(.05,8,8),0xFF6644);transL.position.set(-1.1,.4,0);mainObj.add(transL);
        /* Tasima vezikulleri — ER'den gelen */
        for(var i=0;i<5;i++){{var tv=_m(new THREE.SphereGeometry(.06,8,8),0x88BBDD);tv.position.set((Math.random()-.5)*.8,-.5-.1*Math.random(),Math.random()*.3);mainObj.add(tv);}}
        /* Salgi vezikulleri — trans'tan cikan */
        for(var i=0;i<4;i++){{var sv=_m(new THREE.SphereGeometry(.07,8,8),0xFF8844);sv.position.set((Math.random()-.5)*1,.6+.1*Math.random(),Math.random()*.3);mainObj.add(sv);}}
        /* Lizozom olsuumu */
        var lyz=_m(new THREE.SphereGeometry(.1,12,12),0xCC4466,{{emissive:new THREE.Color(0x441122),emissiveIntensity:.2}});lyz.position.set(.8,.5,0);mainObj.add(lyz);
        }}

        else if(T==6){{
        /* ===== ENDOPLAZMIK RETIKULUM ===== */
        /* Granullu ER — ribozom kaplı */
        var rerG=new THREE.Group();
        for(var i=0;i<10;i++){{var tube=_m(new THREE.TorusGeometry(.4+i*.06,.04,8,24),0x6688AA,{{transparent:true,opacity:.25}});tube.position.set(-.3+i*.06,.1*Math.sin(i),0);tube.rotation.set(Math.random()*.3,0,Math.random()*.2);rerG.add(tube);/* Ribozomlar */for(var j=0;j<6;j++){{var rb=_m(new THREE.SphereGeometry(.02,4,4),0xAACC33);var a=j*Math.PI/3;rb.position.set(-.3+i*.06+Math.cos(a)*(.4+i*.06),.1*Math.sin(i)+Math.sin(a)*(.4+i*.06),0);rerG.add(rb);}}}}
        rerG.position.x=-.5;mainObj.add(rerG);
        /* Duz ER — tubullar */
        var serG=new THREE.Group();
        for(var i=0;i<8;i++){{var tb=_m(new THREE.CylinderGeometry(.03,.03,.4+Math.random()*.3,8),0x88AACC,{{transparent:true,opacity:.2}});tb.position.set(.5+Math.random()*.5,(Math.random()-.5)*1,Math.random()*.3);tb.rotation.set(Math.random(),0,Math.random()*2);serG.add(tb);}}
        mainObj.add(serG);
        /* Cekirdek zari baglantisi */
        var nucC=_m(new THREE.SphereGeometry(.3,20,20),0x6644AA,{{transparent:true,opacity:.2}});nucC.position.set(-1.2,0,0);mainObj.add(nucC);
        var conn=_m(new THREE.CylinderGeometry(.04,.04,.5,6),0x7766AA,{{transparent:true,opacity:.15}});conn.position.set(-1,0,0);conn.rotation.z=Math.PI/2;mainObj.add(conn);
        /* Tasima vezikulleri */
        for(var i=0;i<5;i++){{var v=_m(new THREE.SphereGeometry(.04,6,6),0xFFCC44);v.position.set(.2+Math.random()*.5,(Math.random()-.5)*.5,Math.random()*.3);mainObj.add(v);}}
        }}

        else if(T==7){{
        /* ===== LIZOZOM — Asidik enzim kesecigi ===== */
        /* Dis zar */
        var mem=_m(new THREE.SphereGeometry(1.0,32,32),0xCC4466,{{transparent:true,opacity:.2,side:THREE.DoubleSide}});mainObj.add(mem);
        /* Glikoprotein kaplama — iç yüzey */
        var gly=_mb(new THREE.SphereGeometry(.95,28,28),0xDD5577,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});mainObj.add(gly);
        /* Asidik iç ortam */
        var acid=_mb(new THREE.SphereGeometry(.9,24,24),0xEE8899,{{transparent:true,opacity:.06}});mainObj.add(acid);
        /* Enzimler — farkli renkli noktalar */
        var eClrs=[0xFF4444,0xFF8844,0xFFCC44,0x44CC44,0x4488CC,0xAA44CC];
        for(var i=0;i<25;i++){{var en=_m(new THREE.SphereGeometry(.04+Math.random()*.03,6,6),eClrs[i%6],{{emissive:new THREE.Color(eClrs[i%6]),emissiveIntensity:.2}});var r=Math.random()*.7;var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;en.position.set(r*Math.sin(th)*Math.cos(ph),r*Math.cos(th),r*Math.sin(th)*Math.sin(ph));mainObj.add(en);}}
        /* Proton pompasi */
        for(var i=0;i<4;i++){{var pp=_m(new THREE.CylinderGeometry(.04,.04,.12,8),0xFFDD44);var a=i*Math.PI/2;pp.position.set(Math.cos(a)*.98,Math.sin(a)*.98,0);pp.lookAt(0,0,0);pp.rotateX(Math.PI/2);mainObj.add(pp);}}
        /* Sindirilen materyal */
        for(var i=0;i<5;i++){{var dm=_mb(new THREE.DodecahedronGeometry(.06),0x887766,{{transparent:true,opacity:.3}});dm.position.set((Math.random()-.5)*.8,(Math.random()-.5)*.8,(Math.random()-.5)*.8);mainObj.add(dm);}}
        }}

        else if(T==8){{
        /* ===== HUCRE CEKIRDEGI ===== */
        /* Cift zar */
        var outer=_m(new THREE.SphereGeometry(1.2,24,24),0x6644AA,{{transparent:true,opacity:.12,side:THREE.DoubleSide}});mainObj.add(outer);
        var inner=_m(new THREE.SphereGeometry(1.15,24,24),0x7755BB,{{transparent:true,opacity:.1,side:THREE.DoubleSide}});mainObj.add(inner);
        /* Cekirdek gözenekleri */
        for(var i=0;i<20;i++){{var np=_m(new THREE.TorusGeometry(.04,.015,8,12),0x9977DD);var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;np.position.set(Math.sin(th)*Math.cos(ph)*1.2,Math.cos(th)*1.2,Math.sin(th)*Math.sin(ph)*1.2);np.lookAt(0,0,0);mainObj.add(np);}}
        /* Kromatin agi */
        for(var i=0;i<15;i++){{var cr=_m(new THREE.TorusGeometry(.15+Math.random()*.2,.015,8,16),0x5533AA,{{transparent:true,opacity:.3}});cr.position.set((Math.random()-.5)*.8,(Math.random()-.5)*.8,(Math.random()-.5)*.8);cr.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(cr);}}
        /* Cekirdekçik */
        var nucl=_m(new THREE.SphereGeometry(.3,24,24),0x3311AA,{{emissive:new THREE.Color(0x110044),emissiveIntensity:.3}});nucl.position.set(.2,.1,0);mainObj.add(nucl);
        /* Lamina — iç zar destegi */
        var lam=_mb(new THREE.SphereGeometry(1.12,24,24),0x8866CC,{{transparent:true,opacity:.04,wireframe:true}});mainObj.add(lam);
        /* mRNA çıkışi — gözene gecis */
        for(var i=0;i<3;i++){{var mr=_m(new THREE.CylinderGeometry(.008,.008,.3,4),0xFF6644,{{emissive:new THREE.Color(0x441100),emissiveIntensity:.3}});var th=.5+i*1.5,ph=i*.8;mr.position.set(Math.sin(th)*Math.cos(ph)*1.3,Math.cos(th)*1.3,Math.sin(th)*Math.sin(ph)*1.3);mr.lookAt(Math.sin(th)*Math.cos(ph)*2,Math.cos(th)*2,Math.sin(th)*Math.sin(ph)*2);mr.rotateX(Math.PI/2);mainObj.add(mr);}}
        }}

        else if(T==9){{
        /* ===== KLOROPLAST ===== */
        /* Dis zar */
        var outer=_m(new THREE.SphereGeometry(1.2,32,32),0x44AA44,{{transparent:true,opacity:.15,side:THREE.DoubleSide}});outer.scale.set(1.5,.7,.9);mainObj.add(outer);
        /* Ic zar */
        var inner=_m(new THREE.SphereGeometry(1.1,28,28),0x55BB55,{{transparent:true,opacity:.1,side:THREE.DoubleSide}});inner.scale.set(1.5,.7,.9);mainObj.add(inner);
        /* Stroma */
        var stroma=_mb(new THREE.SphereGeometry(1.0,24,24),0x66CC66,{{transparent:true,opacity:.05}});stroma.scale.set(1.5,.7,.9);mainObj.add(stroma);
        /* Grana — tilakoid yiginlari */
        for(var i=0;i<5;i++){{for(var j=0;j<4;j++){{var th=_m(new THREE.CylinderGeometry(.12,.12,.02,12),0x338833);th.position.set(-.8+i*.4,-.15+j*.05,(Math.random()-.5)*.3);mainObj.add(th);}}}}
        /* Grana arasi tilakoidler — bağlantı */
        for(var i=0;i<4;i++){{var lt=_m(new THREE.CylinderGeometry(.015,.015,.35,6),0x449944,{{transparent:true,opacity:.3}});lt.position.set(-.6+i*.4,-.05,0);lt.rotation.z=Math.PI/2;mainObj.add(lt);}}
        /* Kloroplast DNA */
        var cpDNA=_m(new THREE.TorusGeometry(.1,.015,8,16),0x4488CC);cpDNA.position.set(.6,.15,0);mainObj.add(cpDNA);
        /* Ribozomlar */
        for(var i=0;i<8;i++){{var rb=_m(new THREE.SphereGeometry(.02,4,4),0xAACC33);rb.position.set((Math.random()-.5)*1.5,(Math.random()-.5)*.5,(Math.random()-.5)*.5);mainObj.add(rb);}}
        /* Nisasta taneleri */
        for(var i=0;i<3;i++){{var st=_m(new THREE.SphereGeometry(.06,8,8),0xEEEECC);st.position.set((Math.random()-.5)*1,(Math.random()-.5)*.3,Math.random()*.2);mainObj.add(st);}}
        }}

        else if(T==10){{
        /* ===== HUCRE ZARI — Akiçi mozaik kesit ===== */
        /* Fosfolipid cift tabaka — dilim gosterimi */
        for(var row=0;row<2;row++){{for(var i=0;i<25;i++){{for(var j=0;j<8;j++){{/* Bas */var hd=_m(new THREE.SphereGeometry(.06,8,8),0x4488CC,{{shininess:80}});hd.position.set(-1.5+i*.12,row==0?.15:-.15,-0.5+j*.14);mainObj.add(hd);/* Kuyruklar */for(var k=0;k<2;k++){{var tl=_m(new THREE.CylinderGeometry(.012,.012,.15,4),0xFFCC44);tl.position.set(-1.5+i*.12+k*.02-.01,row==0?.02:-.02,-0.5+j*.14);mainObj.add(tl);}}}}}}}}
        /* Integral protein — kanal */
        var ch=_m(new THREE.CylinderGeometry(.08,.08,.4,12),0x44AA44,{{shininess:50}});ch.position.set(0,0,0);mainObj.add(ch);
        var chH=_m(new THREE.TorusGeometry(.08,.02,8,16),0x55BB55);chH.position.set(0,.2,0);mainObj.add(chH);
        var chH2=chH.clone();chH2.position.y=-.2;mainObj.add(chH2);
        /* Periferal protein */
        var pp=_m(new THREE.SphereGeometry(.08,10,10),0xFF6644);pp.position.set(.5,.22,0);mainObj.add(pp);
        /* Kolesterol — fosfolipidler arasi */
        for(var i=0;i<6;i++){{var col=_m(new THREE.SphereGeometry(.04,6,6),0xFFAA33);col.position.set(-1+i*.4,0,(Math.random()-.5)*.8);mainObj.add(col);}}
        /* Glikokaliks — şeker zincirleri */
        for(var i=0;i<8;i++){{for(var j=0;j<3;j++){{var gl=_m(new THREE.SphereGeometry(.02,4,4),0xFF88CC);gl.position.set(-1+i*.3,.25+j*.06,(Math.random()-.5)*.6);mainObj.add(gl);}}}}
        }}

        else if(T==11){{
        /* ===== DNA YAPISI — Cift sarmal ===== */
        /* Şeker-fosfat omurgalari ve bazlar */
        for(var i=0;i<40;i++){{var y=i*.08-1.6;var a1=i*.32;var a2=a1+Math.PI;var r=.4;
        /* 1. zincir omurga */
        var s1=_m(new THREE.SphereGeometry(.04,8,8),0x4488CC);s1.position.set(Math.cos(a1)*r,y,Math.sin(a1)*r);mainObj.add(s1);
        /* 2. zincir omurga */
        var s2=_m(new THREE.SphereGeometry(.04,8,8),0x4488CC);s2.position.set(Math.cos(a2)*r,y,Math.sin(a2)*r);mainObj.add(s2);
        /* Baz cifti — koprü */
        var bClrs=[[0xFF4444,0x44FF44],[0xFFCC44,0x4444FF]];var bp=bClrs[i%2];
        var b1=_m(new THREE.CylinderGeometry(.02,.02,r*.45,6),bp[0]);
        b1.position.set(Math.cos(a1)*r*.55,y,Math.sin(a1)*r*.55);b1.lookAt(0,y,0);b1.rotateX(Math.PI/2);mainObj.add(b1);
        var b2=_m(new THREE.CylinderGeometry(.02,.02,r*.45,6),bp[1]);
        b2.position.set(Math.cos(a2)*r*.55,y,Math.sin(a2)*r*.55);b2.lookAt(0,y,0);b2.rotateX(Math.PI/2);mainObj.add(b2);
        /* Omurga baglantisi */
        if(i>0){{var c1=_m(new THREE.CylinderGeometry(.012,.012,.08,4),0x6688AA,{{transparent:true,opacity:.4}});c1.position.set(Math.cos(a1)*r,y-.04,Math.sin(a1)*r);mainObj.add(c1);var c2=c1.clone();c2.position.set(Math.cos(a2)*r,y-.04,Math.sin(a2)*r);mainObj.add(c2);}}
        }}
        /* Hidrojen baglari — nokta cizgi */
        for(var i=0;i<40;i+=2){{var y=i*.08-1.6;var hb=_mb(new THREE.SphereGeometry(.01,4,4),0xFFFFFF,{{transparent:true,opacity:.3}});hb.position.set(0,y,0);mainObj.add(hb);}}
        }}

        else if(T==12){{
        /* ===== RNA YAPISI — Tek zincir + katlanma ===== */
        for(var i=0;i<35;i++){{var y=i*.1-1.8;var a=i*.35;var r=.35+Math.sin(i*.15)*.15;
        var s=_m(new THREE.SphereGeometry(.04,8,8),0xCC4488);s.position.set(Math.cos(a)*r,y,Math.sin(a)*r);mainObj.add(s);
        /* Baz — yana cikan cubuk */
        var bClrs=[0xFF4444,0x44FF44,0xFFCC44,0x4444FF];
        var b=_m(new THREE.CylinderGeometry(.015,.015,.2,6),bClrs[i%4]);b.position.set(Math.cos(a)*r*.6,y,Math.sin(a)*r*.6);b.lookAt(0,y,0);b.rotateX(Math.PI/2);mainObj.add(b);
        }}
        /* Stem-loop yapisi */
        var loop=_m(new THREE.TorusGeometry(.15,.02,8,16),0xDD66AA);loop.position.set(.2,1.0,0);mainObj.add(loop);
        var loop2=_m(new THREE.TorusGeometry(.12,.02,8,12),0xDD66AA);loop2.position.set(-.3,-.5,.2);loop2.rotation.x=.5;mainObj.add(loop2);
        /* 5' cap */
        var cap=_m(new THREE.SphereGeometry(.08,10,10),0xFFAA33,{{emissive:new THREE.Color(0x664400),emissiveIntensity:.3}});cap.position.set(Math.cos(0)*.35,-1.8,Math.sin(0)*.35);mainObj.add(cap);
        /* Poly-A kuyruk */
        for(var i=0;i<8;i++){{var pa=_m(new THREE.SphereGeometry(.03,6,6),0xFF4444);pa.position.set(.5+i*.08,1.7,Math.sin(i*.5)*.05);mainObj.add(pa);}}
        }}

        else if(T==13){{
        /* ===== KROMOZOM — X şekli ===== */
        /* Sol kromatid */
        var lc=_m(new THREE.CylinderGeometry(.18,.15,1.3,16),0x6644AA,{{shininess:50}});lc.position.x=-.22;mainObj.add(lc);
        /* Sag kromatid */
        var rc=_m(new THREE.CylinderGeometry(.18,.15,1.3,16),0x6644AA,{{shininess:50}});rc.position.x=.22;mainObj.add(rc);
        /* Sentromer — baglanma */
        var cen=_m(new THREE.SphereGeometry(.22,16,16),0x8866CC,{{emissive:new THREE.Color(0x220044),emissiveIntensity:.2}});mainObj.add(cen);
        /* Kinetokor */
        var kin1=_m(new THREE.CylinderGeometry(.05,.05,.04,12),0xFFCC33);kin1.position.set(-.3,0,0);kin1.rotation.z=Math.PI/2;mainObj.add(kin1);
        var kin2=kin1.clone();kin2.position.x=.3;mainObj.add(kin2);
        /* Kromatin spiralleri — doku */
        for(var side=-1;side<=1;side+=2){{for(var i=0;i<20;i++){{var sp=_m(new THREE.TorusGeometry(.14,.01,8,12),0x7755BB,{{transparent:true,opacity:.3}});sp.position.set(side*.22,-.6+i*.06,0);sp.rotation.x=Math.PI/2;mainObj.add(sp);}}}}
        /* Telomerler */
        for(var side=-1;side<=1;side+=2){{for(var end=-1;end<=1;end+=2){{var tel=_m(new THREE.SphereGeometry(.08,10,10),0xFFDD44,{{emissive:new THREE.Color(0x664400),emissiveIntensity:.3}});tel.position.set(side*.22,end*.7,0);mainObj.add(tel);}}}}
        /* Ig iplik baglantisi */
        for(var i=0;i<4;i++){{var sp=_m(new THREE.CylinderGeometry(.008,.008,.8,4),0xCCCCCC,{{transparent:true,opacity:.2}});sp.position.set(i%2?-.3:.3,0,0);sp.rotation.z=.3*(i<2?1:-1);sp.rotation.x=.2*(i%2?1:-1);mainObj.add(sp);}}
        }}

        else if(T==14){{
        /* ===== SENTROZOM — Iki sentriyol ===== */
        /* 1. Sentriyol — 9x3 mikrotubul */
        var s1G=new THREE.Group();
        for(var i=0;i<9;i++){{var a=i*Math.PI*2/9;for(var j=0;j<3;j++){{var mt=_m(new THREE.CylinderGeometry(.03,.03,.6,8),0x888888,{{shininess:80}});mt.position.set(Math.cos(a)*.2+Math.cos(a+j*.15)*.05,0,Math.sin(a)*.2+Math.sin(a+j*.15)*.05);s1G.add(mt);}}}}
        s1G.position.set(-.15,0,0);mainObj.add(s1G);
        /* 2. Sentriyol — dik */
        var s2G=s1G.clone();s2G.position.set(.15,0,0);s2G.rotation.x=Math.PI/2;mainObj.add(s2G);
        /* Perisentroler materyal */
        var pcm=_mb(new THREE.SphereGeometry(.5,16,16),0xAAAA88,{{transparent:true,opacity:.06}});mainObj.add(pcm);
        /* Mikrotubul nükleasyonu — yildiz şeklinde dağılan tubuller */
        for(var i=0;i<12;i++){{var mt=_m(new THREE.CylinderGeometry(.008,.008,.8+Math.random()*.5,4),0xCCCC88,{{transparent:true,opacity:.15}});mt.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0);mainObj.add(mt);}}
        /* Gamma-tubulin halkalari */
        for(var i=0;i<6;i++){{var gt=_m(new THREE.TorusGeometry(.04,.008,8,12),0xFFCC44);gt.position.set((Math.random()-.5)*.3,(Math.random()-.5)*.3,(Math.random()-.5)*.3);gt.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(gt);}}
        }}

        else if(T==15){{
        /* ===== VAKUOL ===== */
        /* Tonoplast — vakuol zari */
        var ton=_m(new THREE.SphereGeometry(1.3,24,24),0x4488CC,{{transparent:true,opacity:.12,side:THREE.DoubleSide}});ton.scale.set(1.2,1,.9);mainObj.add(ton);
        /* Hüçre ozsyu — iç sıvı */
        var sap=_mb(new THREE.SphereGeometry(1.25,32,32),0x6699CC,{{transparent:true,opacity:.06}});sap.scale.set(1.2,1,.9);mainObj.add(sap);
        /* Antosiyanin pigmentleri */
        for(var i=0;i<15;i++){{var pg=_mb(new THREE.SphereGeometry(.03+Math.random()*.02,6,6),new THREE.Color().setHSL(.8+Math.random()*.15,.6,.4),{{transparent:true,opacity:.3}});var r=Math.random()*.9;var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;pg.position.set(r*Math.sin(th)*Math.cos(ph)*1.2,r*Math.cos(th),r*Math.sin(th)*Math.sin(ph)*.9);mainObj.add(pg);}}
        /* Mineral kristalleri */
        for(var i=0;i<5;i++){{var mn=_m(new THREE.OctahedronGeometry(.04),0xEEDDCC,{{shininess:100}});mn.position.set((Math.random()-.5)*.8,(Math.random()-.5)*.8,(Math.random()-.5)*.6);mainObj.add(mn);}}
        /* Hüçre duvari ve sitoplazma — dış referans */
        var cw=_mb(new THREE.SphereGeometry(1.7,24,24),0x228833,{{transparent:true,opacity:.05,side:THREE.DoubleSide}});cw.scale.set(1.2,1,.9);mainObj.add(cw);
        var cyt=_mb(new THREE.SphereGeometry(1.6,24,24),0x88CC88,{{transparent:true,opacity:.04,side:THREE.DoubleSide}});cyt.scale.set(1.2,1,.9);mainObj.add(cyt);
        }}

        else if(T==16){{
        /* ===== PEROKSIZOM ===== */
        var mem=_m(new THREE.SphereGeometry(.8,32,32),0xDD8833,{{transparent:true,opacity:.2,side:THREE.DoubleSide}});mainObj.add(mem);
        /* Katalaz enzimleri — kristalize cekirdek */
        var core=_m(new THREE.OctahedronGeometry(.25),0xFFDD44,{{emissive:new THREE.Color(0x664400),emissiveIntensity:.3}});mainObj.add(core);
        /* Oksidaz enzimleri */
        for(var i=0;i<15;i++){{var ox=_m(new THREE.SphereGeometry(.04,6,6),0xCC6622);var r=Math.random()*.5+.1;var th=Math.random()*Math.PI,ph=Math.random()*Math.PI*2;ox.position.set(r*Math.sin(th)*Math.cos(ph),r*Math.cos(th),r*Math.sin(th)*Math.sin(ph));mainObj.add(ox);}}
        /* H2O2 partikulleri */
        for(var i=0;i<8;i++){{var hp=_mb(new THREE.SphereGeometry(.02,4,4),0xAADDFF,{{transparent:true,opacity:.4}});hp.position.set((Math.random()-.5)*.6,(Math.random()-.5)*.6,(Math.random()-.5)*.6);mainObj.add(hp);}}
        /* Yag asidi substrati */
        for(var i=0;i<5;i++){{var fa=_m(new THREE.CylinderGeometry(.01,.01,.3,4),0xFFCC88);fa.position.set((Math.random()-.5)*.5,(Math.random()-.5)*.5,(Math.random()-.5)*.5);fa.rotation.set(Math.random(),0,Math.random());mainObj.add(fa);}}
        }}

        else if(T==17){{
        /* ===== SITOPLAZMA ===== */
        /* Hüçre zarı — referans */
        var mem=_mb(new THREE.SphereGeometry(1.7,32,32),0x88CC88,{{transparent:true,opacity:.08,side:THREE.DoubleSide}});mainObj.add(mem);
        /* Sitosol — jol */
        var sol=_mb(new THREE.SphereGeometry(1.65,24,24),0xAADDAA,{{transparent:true,opacity:.04}});mainObj.add(sol);
        /* Cekirdek */
        var nuc=_m(new THREE.SphereGeometry(.4,20,20),0x6644AA,{{transparent:true,opacity:.3}});mainObj.add(nuc);
        /* Organeller — çeşitli */
        /* Mitokondri */
        for(var i=0;i<3;i++){{var mt=_m(new THREE.SphereGeometry(.1,10,10),0xDD6633);mt.scale.set(1.5,.8,.8);mt.position.set((Math.random()-.5)*2,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);mainObj.add(mt);}}
        /* ER parcalari */
        for(var i=0;i<5;i++){{var er=_m(new THREE.TorusGeometry(.2,.015,8,16),0x6688AA,{{transparent:true,opacity:.15}});er.position.set((Math.random()-.5)*2,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);er.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(er);}}
        /* Ribozomlar */
        for(var i=0;i<40;i++){{var rb=_m(new THREE.SphereGeometry(.02,4,4),0xAACC33);rb.position.set((Math.random()-.5)*2.5,(Math.random()-.5)*2,(Math.random()-.5)*2);if(rb.position.length()>1.5)rb.position.multiplyScalar(1.4/rb.position.length());mainObj.add(rb);}}
        /* Glikojen taneleri */
        for(var i=0;i<10;i++){{var gl=_m(new THREE.SphereGeometry(.03,6,6),0xEEDDCC);gl.position.set((Math.random()-.5)*2,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);mainObj.add(gl);}}
        /* Protein molekulleri */
        for(var i=0;i<12;i++){{var pr=_mb(new THREE.SphereGeometry(.015,4,4),0xFF88CC,{{transparent:true,opacity:.3}});pr.position.set((Math.random()-.5)*2.5,(Math.random()-.5)*2,(Math.random()-.5)*2);if(pr.position.length()>1.5)pr.position.multiplyScalar(1.4/pr.position.length());mainObj.add(pr);}}
        }}

        else if(T==18){{
        /* ===== HUCRE ISKELETI ===== */
        /* Hüçre siniri — referans */
        var mem=_mb(new THREE.SphereGeometry(1.8,24,24),0x88CC88,{{transparent:true,opacity:.05,side:THREE.DoubleSide}});mainObj.add(mem);
        /* Mikrotubuller — kalin, yesil */
        for(var i=0;i<8;i++){{var mt=_m(new THREE.CylinderGeometry(.025,.025,2+Math.random()*1.5,8),0x44AA44,{{shininess:60}});mt.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0);mainObj.add(mt);}}
        /* Mikrofilamentler — ince, kirmizi */
        for(var i=0;i<12;i++){{var mf=_m(new THREE.CylinderGeometry(.01,.01,1.5+Math.random()*1,6),0xDD4444,{{transparent:true,opacity:.4}});mf.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0);mainObj.add(mf);}}
        /* Ara filamentler — orta, mavi */
        for(var i=0;i<6;i++){{var af=_m(new THREE.CylinderGeometry(.015,.015,1.8+Math.random()*1,6),0x4488CC,{{transparent:true,opacity:.35}});af.rotation.set(Math.random()*Math.PI,Math.random()*Math.PI,0);mainObj.add(af);}}
        /* Motor proteinler — mikrotubul üzerinde */
        for(var i=0;i<4;i++){{var mp=_m(new THREE.SphereGeometry(.04,8,8),0xFFCC33,{{emissive:new THREE.Color(0x664400),emissiveIntensity:.3}});mp.position.set((Math.random()-.5)*1.5,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);mainObj.add(mp);/* Yuk */var ld=_m(new THREE.SphereGeometry(.06,8,8),0xFF8844,{{transparent:true,opacity:.4}});ld.position.copy(mp.position);ld.position.y+=.08;mainObj.add(ld);}}
        /* Cekirdek — merkez referans */
        var nuc=_m(new THREE.SphereGeometry(.3,16,16),0x6644AA,{{transparent:true,opacity:.15}});mainObj.add(nuc);
        }}

        else if(T==19){{
        /* ===== VEZIKUL — Tasima sistemi ===== */
        /* Kaynak zar (ER) */
        var er=_m(new THREE.CylinderGeometry(.8,.8,.06,24),0x6688AA,{{transparent:true,opacity:.2}});er.position.y=-1;mainObj.add(er);
        /* Hedef zar (hüçre zari) */
        var pm=_m(new THREE.CylinderGeometry(1,1,.04,24),0x88CC88,{{transparent:true,opacity:.15}});pm.position.y=1.2;mainObj.add(pm);
        /* Golgi — ortada */
        for(var i=0;i<4;i++){{var go=_m(new THREE.CylinderGeometry(.5,.5,.03,20),0xFFCC33,{{transparent:true,opacity:.25}});go.position.y=-.2+i*.1;mainObj.add(go);}}
        /* COPII vezikulleri — ER→Golgi */
        for(var i=0;i<3;i++){{var v=_m(new THREE.SphereGeometry(.08,10,10),0x88BBDD);v.position.set((Math.random()-.5)*.6,-.7+i*.15,Math.random()*.2);mainObj.add(v);}}
        /* COPI vezikulleri — Golgi→ER */
        for(var i=0;i<2;i++){{var v=_m(new THREE.SphereGeometry(.06,8,8),0xCC88DD);v.position.set(.3+i*.15,-.5,Math.random()*.2);mainObj.add(v);}}
        /* Salgi vezikulleri — Golgi→zar */
        for(var i=0;i<4;i++){{var v=_m(new THREE.SphereGeometry(.07,10,10),0xFF8844);v.position.set((Math.random()-.5)*.8,.4+i*.2,Math.random()*.2);mainObj.add(v);}}
        /* Ekzositoz — zarla birlesmis vezikul */
        var exo=_m(new THREE.SphereGeometry(.09,12,12),0xFF8844,{{transparent:true,opacity:.5}});exo.position.set(0,1.15,0);mainObj.add(exo);
        /* Endositoz — zar çokuntüsu */
        var endo=_m(new THREE.SphereGeometry(.08,10,10),0x88CC88,{{transparent:true,opacity:.3}});endo.position.set(.6,1.1,0);mainObj.add(endo);
        /* Sinaptik vezikul detay */
        for(var i=0;i<5;i++){{var sv=_m(new THREE.SphereGeometry(.04,8,8),0xFFDD44);sv.position.set(-.8,.8+i*.08,0);mainObj.add(sv);}}
        /* SNARE proteinleri */
        for(var i=0;i<3;i++){{var sn=_m(new THREE.CylinderGeometry(.01,.01,.15,4),0x44CC44);sn.position.set((Math.random()-.5)*.3,1.05,0);mainObj.add(sn);}}
        }}

        scene.add(mainObj);"""

    if ci == 3:  # Insan Anatomisi
        return f"""mainObj=new THREE.Group();var T={ti};
        var _m=function(g,c,o){{var mt=new THREE.MeshPhongMaterial({{color:c,shininess:60}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        var _mb=function(g,c,o){{var mt=new THREE.MeshBasicMaterial({{color:c}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        if(T==0){{
        /* ===== KALP — Detayli Anatomik Model ===== */
        /* Ana miyokard govde — ust yarim kure + alt konik yapi */
        var hG=new THREE.Group();
        /* Sol ventrikul — büyük, güçlü */
        var lv=_m(new THREE.SphereGeometry(.62,36,36),0xb83a3a,{{shininess:35}});lv.position.set(-.12,-.08,.02);lv.scale.set(.82,1.35,.78);hG.add(lv);
        /* Sag ventrikul — biraz daha küçük, saga yaslı */
        var rv=_m(new THREE.SphereGeometry(.52,32,32),0xc44848,{{shininess:35}});rv.position.set(.22,-.05,.08);rv.scale.set(.7,1.2,.65);hG.add(rv);
        /* Sol atriyum — ust sol arka */
        var la=_m(new THREE.SphereGeometry(.38,28,28),0xc45555,{{shininess:40}});la.position.set(-.22,.52,-.08);la.scale.set(.9,.7,.8);hG.add(la);
        /* Sag atriyum — ust sag on */
        var ra=_m(new THREE.SphereGeometry(.36,28,28),0xcc5e5e,{{shininess:40}});ra.position.set(.25,.52,.05);ra.scale.set(.85,.68,.75);hG.add(ra);
        /* Apex — kalbin alt sivri üçu */
        var apex=_m(new THREE.ConeGeometry(.22,.42,18),0x9a2828);apex.position.set(-.05,-.82,0);hG.add(apex);
        /* Interventrikuler septum */
        var sept=_m(new THREE.BoxGeometry(.04,.95,.42),0xa83232,{{transparent:true,opacity:.7}});sept.position.set(.05,-.05,0);hG.add(sept);
        /* Sulkuslar — yüzey oluklari (yag dokusu) */
        var avs=_m(new THREE.TorusGeometry(.55,.028,8,32),0xe8c84a,{{transparent:true,opacity:.65}});avs.rotation.x=1.57;avs.position.y=.15;hG.add(avs);
        var ivs=_m(new THREE.CylinderGeometry(.022,.018,.95,6),0xe8c84a,{{transparent:true,opacity:.6}});ivs.position.set(.05,-.1,.38);ivs.rotation.x=.15;hG.add(ivs);
        /* ===== BUYUK DAMARLAR ===== */
        /* Aort — kemer şekli */
        var aoS=_m(new THREE.CylinderGeometry(.1,.095,.3,14),0xcc3344);aoS.position.set(-.1,.78,0);hG.add(aoS);
        var aoA=_m(new THREE.TorusGeometry(.22,.09,12,20,2.8),0xcc3344,{{shininess:50}});aoA.position.set(-.1,1.02,0);aoA.rotation.z=-.2;aoA.rotation.x=.1;hG.add(aoA);
        var aoD=_m(new THREE.CylinderGeometry(.085,.08,.55,12),0xbb2d3e);aoD.position.set(-.38,.82,-.12);aoD.rotation.z=.15;hG.add(aoD);
        /* Pulmoner arter */
        var paS=_m(new THREE.CylinderGeometry(.075,.07,.25,12),0x3a5faa);paS.position.set(.08,.76,.1);paS.rotation.z=.12;hG.add(paS);
        var paL=_m(new THREE.CylinderGeometry(.05,.045,.35,8),0x3a5faa);paL.position.set(-.15,.95,.12);paL.rotation.z=.7;hG.add(paL);
        var paR=_m(new THREE.CylinderGeometry(.05,.045,.3,8),0x3a5faa);paR.position.set(.28,.92,.1);paR.rotation.z=-.5;hG.add(paR);
        /* Superior vena kava */
        var svc=_m(new THREE.CylinderGeometry(.065,.06,.5,10),0x2a4a88);svc.position.set(.32,.88,-.05);hG.add(svc);
        /* Inferior vena kava */
        var ivc=_m(new THREE.CylinderGeometry(.07,.065,.4,10),0x2a4a88);ivc.position.set(.3,-.48,-.1);hG.add(ivc);
        /* Pulmoner venler (4 adet) */
        for(var pv=0;pv<4;pv++){{var pvn=_m(new THREE.CylinderGeometry(.032,.028,.2,6),0x993344);pvn.position.set(-.35+pv*.06,.62,-.18-pv*.03);pvn.rotation.z=.3+pv*.08;hG.add(pvn);}}
        /* ===== KORONER DAMARLAR — yüzey üzerinde dallanma ===== */
        /* Sol inen koroner arter (LAD) */
        var lad1=_m(new THREE.CylinderGeometry(.018,.016,.5,6),0xdd4455,{{emissive:new THREE.Color(0x551111),emissiveIntensity:.3}});lad1.position.set(-.05,.15,.4);lad1.rotation.x=.2;hG.add(lad1);
        var lad2=_m(new THREE.CylinderGeometry(.014,.012,.35,5),0xdd4455,{{emissive:new THREE.Color(0x551111),emissiveIntensity:.3}});lad2.position.set(-.12,-.2,.38);lad2.rotation.z=.3;lad2.rotation.x=.15;hG.add(lad2);
        /* Sol sirkumfleks arter */
        var lcx=_m(new THREE.TorusGeometry(.45,.015,6,20,2.2),0xdd4455,{{emissive:new THREE.Color(0x551111),emissiveIntensity:.25}});lcx.rotation.y=1.57;lcx.position.set(-.15,.2,0);hG.add(lcx);
        /* Sag koroner arter */
        var rca=_m(new THREE.TorusGeometry(.42,.015,6,18,2.0),0xdd4455,{{emissive:new THREE.Color(0x551111),emissiveIntensity:.25}});rca.rotation.y=-1.57;rca.position.set(.2,.25,.05);hG.add(rca);
        /* Koroner dallar (8x küçük) */
        for(var cb=0;cb<8;cb++){{var cbn=_m(new THREE.CylinderGeometry(.009,.006,.18+Math.random()*.12,4),0xdd5566,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.2}});var ca=cb*.78;cbn.position.set(Math.cos(ca)*.35,-.15+cb*.08,Math.sin(ca)*.32);cbn.rotation.z=Math.cos(ca)*.4;cbn.rotation.x=Math.sin(ca)*.3;hG.add(cbn);}}
        /* Koroner venler (mavi) */
        for(var cv=0;cv<6;cv++){{var cvn=_m(new THREE.CylinderGeometry(.008,.006,.15+Math.random()*.1,4),0x3355aa,{{transparent:true,opacity:.7}});var cva=cv*.95+.3;cvn.position.set(Math.cos(cva)*.33,-.05+cv*.07,Math.sin(cva)*.3);cvn.rotation.z=Math.cos(cva)*.35;hG.add(cvn);}}
        /* ===== YUZEY DOKUSU — kas lifleri ===== */
        for(var mf=0;mf<12;mf++){{var fib=_m(new THREE.CylinderGeometry(.005,.005,.4+Math.random()*.3,3),0xa03030,{{transparent:true,opacity:.18}});var fa=mf*.52;fib.position.set(Math.cos(fa)*.38,-.2+mf*.06,Math.sin(fa)*.35);fib.rotation.z=.3+Math.random()*.4;fib.rotation.x=Math.random()*.2;hG.add(fib);}}
        /* Perikard — saydam dış katman */
        var peri=_m(new THREE.SphereGeometry(1.0,24,24),0xdd8888,{{transparent:true,opacity:.04,side:THREE.BackSide}});peri.position.y=-.05;peri.scale.set(.82,1.1,.72);hG.add(peri);
        mainObj.add(hG);
        }}
        else if(T==1){{
        /* ===== BEYIN — Sagittal Kesit Gorunumu ===== */
        var bG=new THREE.Group();
        /* Serebrum — ana beyin yarim kuresi (sagittal kesit: yarim kurenin iç yüzeyi) */
        var cer=_m(new THREE.SphereGeometry(1.05,42,42,0,3.14,0,3.14),0xe8c8b0,{{shininess:18,side:THREE.DoubleSide}});cer.position.set(0,.18,0);cer.scale.set(.92,.82,.88);cer.rotation.y=-1.57;bG.add(cer);
        /* Korteks dış yüzey — kivrımlar (girus) */
        for(var gi=0;gi<18;gi++){{var gyr=_m(new THREE.SphereGeometry(.08+Math.random()*.06,10,10),0xdebb9e,{{shininess:12}});var ga=gi*.35-.2;var gr=.75+Math.random()*.2;gyr.position.set(Math.cos(ga)*gr*.6,.22+Math.sin(ga)*gr*.72,-.02);gyr.scale.set(1.2,.8,.4);bG.add(gyr);}}
        /* Sulkuslar — giruslar arasi oluklar */
        for(var si=0;si<14;si++){{var sul=_m(new THREE.CylinderGeometry(.006,.004,.12+Math.random()*.08,4),0xb89880,{{transparent:true,opacity:.5}});var sa=si*.42;sul.position.set(Math.cos(sa)*.65,.2+Math.sin(sa)*.62,-.01);sul.rotation.z=sa+.5;bG.add(sul);}}
        /* Frontal lob cikintisi */
        var frl=_m(new THREE.SphereGeometry(.35,24,24),0xe0c0a5,{{shininess:15}});frl.position.set(.72,.35,0);frl.scale.set(.7,.55,.4);bG.add(frl);
        /* Oksipital lob — arka */
        var occ=_m(new THREE.SphereGeometry(.28,20,20),0xdcb8a0);occ.position.set(-.68,.15,0);occ.scale.set(.6,.55,.4);bG.add(occ);
        /* ===== KORPUS KALLOZUM — beyaz egri bant ===== */
        var ccP=new THREE.TorusGeometry(.42,.045,8,28,.01+2.6);var ccM=new THREE.MeshPhongMaterial({{color:0xf0e8dd,shininess:30}});var ccMesh=new THREE.Mesh(ccP,ccM);ccMesh.position.set(-.02,.32,0);ccMesh.rotation.z=-.15;ccMesh.scale.set(1.05,.55,1);bG.add(ccMesh);
        /* Forniks */
        var frn=_m(new THREE.TorusGeometry(.2,.02,6,16,1.8),0xeee0d0);frn.position.set(.05,.18,0);frn.rotation.z=-.6;bG.add(frn);
        /* ===== TALAMUS — merkezi gri yapı ===== */
        var thal=_m(new THREE.SphereGeometry(.18,18,18),0xc4a08a,{{shininess:20}});thal.position.set(0,.12,0);thal.scale.set(1.1,.75,.5);bG.add(thal);
        /* Hipotalamus */
        var hypo=_m(new THREE.SphereGeometry(.1,14,14),0xc09878);hypo.position.set(.12,-.02,0);bG.add(hypo);
        /* Hipofiz bezi (pitüiter) — asagı sarkan */
        var pitS=_m(new THREE.CylinderGeometry(.015,.012,.1,6),0xccaa88);pitS.position.set(.15,-.1,0);bG.add(pitS);
        var pit=_m(new THREE.SphereGeometry(.06,12,12),0xd4a870,{{shininess:40}});pit.position.set(.15,-.18,0);bG.add(pit);
        /* ===== SEREBELLUM — beyincik (yatay cizgili) ===== */
        var cbl=_m(new THREE.SphereGeometry(.38,28,28),0xd4b494,{{shininess:15}});cbl.position.set(-.38,-.42,0);cbl.scale.set(.85,.7,.5);bG.add(cbl);
        /* Serebellum folia (yatay cizgiler) */
        for(var fl=0;fl<9;fl++){{var fol=_m(new THREE.CylinderGeometry(.3,.3,.005,18),0xc0a080,{{transparent:true,opacity:.35}});fol.position.set(-.38,-.55+fl*.035,0);fol.scale.set(.7,1,.45);bG.add(fol);}}
        /* Arbor vitae — beyincik iç beyaz dal yapisi */
        var arb=_m(new THREE.CylinderGeometry(.02,.008,.22,5),0xf0e0cc);arb.position.set(-.35,-.42,0);arb.rotation.z=.3;bG.add(arb);
        for(var ab=0;ab<4;ab++){{var abr=_m(new THREE.CylinderGeometry(.008,.004,.1,4),0xeeddcc);abr.position.set(-.38+ab*.04,-.38-ab*.03,0);abr.rotation.z=.5+ab*.25;bG.add(abr);}}
        /* ===== BEYIN SAPI ===== */
        /* Mezensefalon (ortabeyin) */
        var mes=_m(new THREE.CylinderGeometry(.12,.13,.18,12),0xccaa90);mes.position.set(-.08,-.2,0);bG.add(mes);
        /* Pons */
        var pons=_m(new THREE.SphereGeometry(.16,16,16),0xc8a888,{{shininess:22}});pons.position.set(-.05,-.38,0);pons.scale.set(.9,.7,.5);bG.add(pons);
        /* Medulla oblongata */
        var med=_m(new THREE.CylinderGeometry(.1,.08,.25,10),0xc4a488);med.position.set(-.02,-.58,0);med.rotation.z=.08;bG.add(med);
        /* Omurilik baslangiçi */
        var spc=_m(new THREE.CylinderGeometry(.06,.05,.35,8),0xc0a080);spc.position.set(.02,-.82,0);spc.rotation.z=.1;bG.add(spc);
        /* ===== IC YAPILAR ===== */
        /* Lateral ventrikul (BOS boslugu) */
        var lvent=_m(new THREE.TorusGeometry(.18,.03,6,14,2.0),0x88bbdd,{{transparent:true,opacity:.35}});lvent.position.set(.05,.32,0);lvent.rotation.z=-.4;lvent.scale.set(1,.6,1);bG.add(lvent);
        /* Üçuncu ventrikul */
        var v3=_m(new THREE.BoxGeometry(.02,.15,.04),0x88bbdd,{{transparent:true,opacity:.3}});v3.position.set(.02,.1,0);bG.add(v3);
        /* Dorduncu ventrikul */
        var v4=_m(new THREE.SphereGeometry(.06,8,8),0x88bbdd,{{transparent:true,opacity:.3}});v4.position.set(-.15,-.35,0);v4.scale.set(.5,1,.4);bG.add(v4);
        /* Pineal bez */
        var pin=_m(new THREE.SphereGeometry(.035,8,8),0xbb8866);pin.position.set(-.12,.2,0);bG.add(pin);
        /* Optik kiazma */
        var opC=_m(new THREE.BoxGeometry(.12,.015,.04),0xeedd88,{{emissive:new THREE.Color(0x443300),emissiveIntensity:.2}});opC.position.set(.22,-.05,0);bG.add(opC);
        /* ===== DAMARLAR ===== */
        /* Baziler arter */
        var bas=_m(new THREE.CylinderGeometry(.015,.012,.4,5),0xcc4444,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.2}});bas.position.set(.05,-.5,.08);bG.add(bas);
        /* Beyin iç damarlari */
        for(var bv=0;bv<5;bv++){{var bvn=_m(new THREE.CylinderGeometry(.006,.005,.15,4),0x44aa55,{{emissive:new THREE.Color(0x114411),emissiveIntensity:.15}});bvn.position.set(-.1+bv*.08,-.1+bv*.04,.01);bvn.rotation.z=.3+bv*.15;bG.add(bvn);}}
        /* Kesit yüzeyi — duz arka yüzey (sagittal görünüm) */
        var cut=_m(new THREE.CircleGeometry(1.1,36),0xf0d8c4,{{side:THREE.DoubleSide,transparent:true,opacity:.12}});cut.position.z=-.01;cut.position.y=.1;bG.add(cut);
        bG.rotation.z=.05;
        mainObj.add(bG);
        }}
        else if(T==2){{
        var rul=_m(new THREE.SphereGeometry(.48,26,26),0xffaabb,{{transparent:true,opacity:.45,shininess:35}});rul.position.set(.55,.42,0);rul.scale.set(.88,.68,.68);mainObj.add(rul);
        var rml=_m(new THREE.SphereGeometry(.38,22,22),0xff99aa,{{transparent:true,opacity:.45}});rml.position.set(.55,-.05,0);rml.scale.set(.82,.52,.62);mainObj.add(rml);
        var rll=_m(new THREE.SphereGeometry(.48,26,26),0xff88aa,{{transparent:true,opacity:.45}});rll.position.set(.55,-.52,0);rll.scale.set(.88,.68,.68);mainObj.add(rll);
        var lul=_m(new THREE.SphereGeometry(.48,26,26),0xffaabb,{{transparent:true,opacity:.45}});lul.position.set(-.55,.28,0);lul.scale.set(.78,.78,.68);mainObj.add(lul);
        var lll=_m(new THREE.SphereGeometry(.48,26,26),0xff88aa,{{transparent:true,opacity:.45}});lll.position.set(-.55,-.38,0);lll.scale.set(.78,.78,.68);mainObj.add(lll);
        var tr=_m(new THREE.CylinderGeometry(.075,.075,.65,10),0xffccdd);tr.position.set(0,.95,0);mainObj.add(tr);
        for(var ti2=0;ti2<5;ti2++){{var tri=_m(new THREE.TorusGeometry(.075,.013,6,12),0xeebb99);tri.rotation.x=1.57;tri.position.set(0,.68+ti2*.11,0);mainObj.add(tri);}}
        var rbr=_m(new THREE.CylinderGeometry(.055,.045,.55,8),0xffbbcc);rbr.position.set(.25,.55,0);rbr.rotation.z=-.5;mainObj.add(rbr);
        var lbr=_m(new THREE.CylinderGeometry(.055,.045,.55,8),0xffbbcc);lbr.position.set(-.25,.55,0);lbr.rotation.z=.5;mainObj.add(lbr);
        for(var sb=0;sb<6;sb++){{var sec=_m(new THREE.CylinderGeometry(.028,.018,.32,6),0xffccdd);var sx=sb<3?.35+sb*.12:-.35-sb*.04+.36;var sy=sb<3?.15-.1*sb:.15-.1*(sb-3);sec.position.set(sx,sy,0);sec.rotation.z=sb<3?-.3-.1*sb:.3+.1*(sb-3);mainObj.add(sec);}}
        var dia=_m(new THREE.SphereGeometry(1.4,26,14,0,6.28,0,.65),0xcc8877,{{transparent:true,opacity:.25}});dia.position.set(0,-.95,0);mainObj.add(dia);
        }}
        else if(T==3){{
        var lb=_m(new THREE.SphereGeometry(1.0,32,32),0x884433,{{shininess:40}});lb.position.set(.1,0,0);lb.scale.set(1.25,.58,.78);mainObj.add(lb);
        var sl=_m(new THREE.SphereGeometry(.48,26,26),0x7a3d2d);sl.position.set(-.62,.05,.1);sl.scale.set(.78,.48,.58);mainObj.add(sl);
        var fl=_m(new THREE.BoxGeometry(.018,.45,.35),0xaa7755,{{transparent:true,opacity:.35}});fl.position.set(-.18,.08,.28);mainObj.add(fl);
        var gb=_m(new THREE.SphereGeometry(.17,16,16),0x55aa55);gb.position.set(.28,-.38,.28);gb.scale.set(.58,.95,.58);mainObj.add(gb);
        var gbn=_m(new THREE.CylinderGeometry(.035,.025,.18,8),0x448844);gbn.position.set(.23,-.22,.22);mainObj.add(gbn);
        var pv=_m(new THREE.CylinderGeometry(.055,.055,.45,8),0x3355aa);pv.position.set(.08,-.52,-.08);mainObj.add(pv);
        var ha=_m(new THREE.CylinderGeometry(.038,.038,.42,8),0xcc3344);ha.position.set(-.05,-.52,0);mainObj.add(ha);
        for(var hv=0;hv<2;hv++){{var hvn=_m(new THREE.CylinderGeometry(.035,.035,.28,8),0x4466aa);hvn.position.set(-.15+hv*.35,.32,-.15);mainObj.add(hvn);}}
        var ivc2=_m(new THREE.CylinderGeometry(.055,.055,.28,8),0x3355aa);ivc2.position.set(.38,.22,-.18);mainObj.add(ivc2);
        }}
        else if(T==4){{
        var kb=_m(new THREE.SphereGeometry(.72,32,32),0x994455,{{shininess:35}});kb.scale.set(.55,.82,.45);mainObj.add(kb);
        var hi=_m(new THREE.SphereGeometry(.28,16,16),0x553333);hi.position.set(.32,0,0);mainObj.add(hi);
        for(var mp=0;mp<6;mp++){{var pyr=_m(new THREE.ConeGeometry(.065,.18,6),0xaa3344);var pa2=mp*.95;pyr.position.set(Math.cos(pa2)*.18,-.15+mp*.06,Math.sin(pa2)*.12);pyr.rotation.z=Math.cos(pa2)*.4;mainObj.add(pyr);}}
        var rp=_m(new THREE.ConeGeometry(.12,.28,10),0xddaa88);rp.position.set(.35,0,0);rp.rotation.z=1.57;mainObj.add(rp);
        var ur=_m(new THREE.CylinderGeometry(.035,.028,.75,8),0xddbb88);ur.position.set(.32,-.6,0);mainObj.add(ur);
        var rart=_m(new THREE.CylinderGeometry(.035,.035,.38,8),0xcc3344);rart.position.set(.48,.08,0);rart.rotation.z=1.57;mainObj.add(rart);
        var rvn=_m(new THREE.CylinderGeometry(.042,.042,.38,8),0x3355aa);rvn.position.set(.48,-.05,0);rvn.rotation.z=1.57;mainObj.add(rvn);
        var adr=_m(new THREE.SphereGeometry(.18,14,14),0xddcc44);adr.position.set(0,.62,0);adr.scale.set(1.5,.38,.78);mainObj.add(adr);
        var cap=_m(new THREE.SphereGeometry(.78,16,16),0x994455,{{transparent:true,opacity:.06,side:THREE.BackSide}});mainObj.add(cap);
        }}
        else if(T==5){{
        var fun=_m(new THREE.SphereGeometry(.34,22,22),0xddaa88,{{shininess:30}});fun.position.set(-.32,.58,0);mainObj.add(fun);
        var bod=_m(new THREE.SphereGeometry(.55,28,28),0xdd9977,{{shininess:30}});bod.scale.set(.78,1.15,.68);mainObj.add(bod);
        var ant=_m(new THREE.SphereGeometry(.28,22,22),0xddbb88);ant.position.set(.28,-.48,0);ant.scale.set(.68,.88,.58);mainObj.add(ant);
        var eso=_m(new THREE.CylinderGeometry(.055,.055,.55,10),0xccaa88);eso.position.set(-.28,.95,0);mainObj.add(eso);
        var pyl=_m(new THREE.CylinderGeometry(.072,.052,.28,10),0xccbb88);pyl.position.set(.48,-.55,0);pyl.rotation.z=-.8;mainObj.add(pyl);
        for(var rg=0;rg<6;rg++){{var rug=_m(new THREE.TorusGeometry(.28+rg*.035,.018,6,22),0xcc9977,{{transparent:true,opacity:.3}});rug.rotation.x=1.57;rug.position.y=-.18+rg*.1;mainObj.add(rug);}}
        var psph=_m(new THREE.TorusGeometry(.055,.018,8,12),0xbb8866);psph.position.set(.52,-.58,0);mainObj.add(psph);
        var om=_m(new THREE.SphereGeometry(.62,16,16),0xddaa88,{{transparent:true,opacity:.05,side:THREE.BackSide}});mainObj.add(om);
        }}
        else if(T==6){{
        var scl=_m(new THREE.SphereGeometry(.88,24,24),0xf5f5f0,{{shininess:55}});mainObj.add(scl);
        var corn=_m(new THREE.SphereGeometry(.32,28,28),0xddeeff,{{transparent:true,opacity:.18,shininess:100}});corn.position.z=.72;mainObj.add(corn);
        var iris=new THREE.Mesh(new THREE.RingGeometry(.11,.3,36,1),new THREE.MeshPhongMaterial({{color:0x2266aa,side:THREE.DoubleSide}}));iris.position.z=.86;mainObj.add(iris);
        for(var il=0;il<14;il++){{var irl=_mb(new THREE.BoxGeometry(.003,.17,.003),0x1155aa);irl.position.set(Math.cos(il*.45)*.2,Math.sin(il*.45)*.2,.865);irl.rotation.z=il*.45;mainObj.add(irl);}}
        var pup=new THREE.Mesh(new THREE.CircleGeometry(.11,26),new THREE.MeshBasicMaterial({{color:0x000000,side:THREE.DoubleSide}}));pup.position.z=.88;mainObj.add(pup);
        var len=_m(new THREE.SphereGeometry(.26,26,26),0xeeeeff,{{transparent:true,opacity:.22}});len.position.z=.48;len.scale.z=.32;mainObj.add(len);
        var cil=_m(new THREE.TorusGeometry(.3,.028,8,26),0x996644);cil.position.z=.52;mainObj.add(cil);
        var ret=_m(new THREE.SphereGeometry(.8,32,32),0xdd8866,{{transparent:true,opacity:.12,side:THREE.BackSide}});mainObj.add(ret);
        var cho=_m(new THREE.SphereGeometry(.84,32,32),0x884422,{{transparent:true,opacity:.06,side:THREE.BackSide}});mainObj.add(cho);
        var opn=_m(new THREE.CylinderGeometry(.072,.055,.55,10),0xddcc88);opn.position.set(0,0,-1.08);opn.rotation.x=1.57;mainObj.add(opn);
        var opd=new THREE.Mesh(new THREE.CircleGeometry(.072,16),new THREE.MeshPhongMaterial({{color:0xffddaa,side:THREE.DoubleSide}}));opd.position.z=-.83;mainObj.add(opd);
        for(var bv=0;bv<5;bv++){{var bvn=_m(new THREE.CylinderGeometry(.007,.007,.35,4),0xcc3333,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.3}});bvn.position.set(Math.cos(bv*1.26)*.15,Math.sin(bv*1.26)*.15,-.82);bvn.rotation.z=bv*1.26;mainObj.add(bvn);}}
        var vit=_m(new THREE.SphereGeometry(.68,16,16),0xeeeeff,{{transparent:true,opacity:.035}});vit.position.z=.08;mainObj.add(vit);
        }}
        else if(T==7){{
        var hx=_m(new THREE.TorusGeometry(.42,.045,8,26,4.5),0xddbb88,{{shininess:25}});hx.position.set(-1.0,.18,0);mainObj.add(hx);
        var ahx=_m(new THREE.TorusGeometry(.28,.035,8,22,3.5),0xccaa77);ahx.position.set(-.95,.12,.04);mainObj.add(ahx);
        var lob=_m(new THREE.SphereGeometry(.18,16,16),0xddbb88);lob.position.set(-.88,-.12,.08);lob.scale.set(.5,1,.7);mainObj.add(lob);
        var trg=_m(new THREE.SphereGeometry(.07,10,10),0xddbb88);trg.position.set(-.78,-.02,.14);mainObj.add(trg);
        var ec=_m(new THREE.CylinderGeometry(.055,.055,.45,10),0xaa8866);ec.position.set(-.5,0,0);ec.rotation.z=1.57;mainObj.add(ec);
        var tym=new THREE.Mesh(new THREE.CircleGeometry(.065,18),new THREE.MeshPhongMaterial({{color:0xeeddcc,side:THREE.DoubleSide}}));tym.position.set(-.25,0,0);tym.rotation.y=1.57;mainObj.add(tym);
        var mal=_m(new THREE.CylinderGeometry(.018,.013,.11,6),0xeeddcc);mal.position.set(-.18,.02,0);mainObj.add(mal);
        var inc=_m(new THREE.BoxGeometry(.045,.035,.028),0xeeddcc);inc.position.set(-.1,.025,0);mainObj.add(inc);
        var stp=_m(new THREE.TorusGeometry(.018,.005,4,8),0xeeddcc);stp.position.set(-.03,.025,0);mainObj.add(stp);
        var ovw=new THREE.Mesh(new THREE.CircleGeometry(.025,10),new THREE.MeshPhongMaterial({{color:0xddccbb,side:THREE.DoubleSide}}));ovw.position.set(0,.02,0);ovw.rotation.y=1.57;mainObj.add(ovw);
        for(var ct=0;ct<3;ct++){{var coc=_m(new THREE.TorusGeometry(.11-ct*.028,.018,6,18,6.28),0xddaa88);coc.position.set(.14+ct*.018,-.04-ct*.035,0);coc.rotation.y=.3*ct;mainObj.add(coc);}}
        for(var sc=0;sc<3;sc++){{var sem=_m(new THREE.TorusGeometry(.11,.01,6,22,5.0),0xddbb99);sem.position.set(.14,.12,0);sem.rotation.x=sc==0?0:sc==1?1.57:0;sem.rotation.z=sc==2?1.57:0;mainObj.add(sem);}}
        var eus=_m(new THREE.CylinderGeometry(.028,.035,.55,8),0xccaa88);eus.position.set(.08,-.48,0);eus.rotation.z=.45;mainObj.add(eus);
        var aud=_m(new THREE.CylinderGeometry(.025,.018,.38,8),0xffdd88,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.3}});aud.position.set(.28,-.08,0);aud.rotation.z=-.3;mainObj.add(aud);
        }}
        else if(T==8){{
        var sy=function(i){{return -1.15+i*.098+.12*Math.sin(i*.22);}};
        var sz2=function(i){{return .065*Math.sin(i*.35-.5);}};
        for(var v=0;v<24;v++){{var vb=_m(new THREE.CylinderGeometry(.11-.001*v,.11-.001*v,.072,10),0xeeddcc,{{shininess:40}});vb.position.set(0,sy(v),sz2(v));mainObj.add(vb);var sp=_m(new THREE.ConeGeometry(.025,.1,4),0xddccbb);sp.position.set(0,sy(v),sz2(v)-.1);sp.rotation.x=1.57;mainObj.add(sp);if(v<23){{var dsc=_m(new THREE.CylinderGeometry(.1,.1,.018,10),0x4488aa,{{transparent:true,opacity:.45}});dsc.position.set(0,(sy(v)+sy(v+1))/2,(sz2(v)+sz2(v+1))/2);mainObj.add(dsc);}}}}
        var sac=_m(new THREE.ConeGeometry(.14,.32,5),0xeeddcc);sac.position.set(0,-1.28,sz2(23));sac.rotation.x=3.14;mainObj.add(sac);
        var cox=_m(new THREE.ConeGeometry(.045,.1,4),0xddccbb);cox.position.set(0,-1.48,sz2(23));cox.rotation.x=3.14;mainObj.add(cox);
        var cord=_m(new THREE.CylinderGeometry(.025,.025,2.3,8),0xffdd88,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.25}});cord.position.set(0,0,-.02);mainObj.add(cord);
        }}
        else if(T==9){{
        var crn=_m(new THREE.SphereGeometry(.82,34,34),0xeeddcc,{{shininess:30}});crn.position.set(0,.22,0);crn.scale.set(.85,1,.88);mainObj.add(crn);
        var les=_m(new THREE.SphereGeometry(.14,16,16),0x222222);les.position.set(-.24,.14,.62);mainObj.add(les);
        var res=_m(new THREE.SphereGeometry(.14,16,16),0x222222);res.position.set(.24,.14,.62);mainObj.add(res);
        var nas=_m(new THREE.ConeGeometry(.09,.16,3),0x333333);nas.position.set(0,-.06,.7);mainObj.add(nas);
        var nbr=_m(new THREE.BoxGeometry(.055,.14,.055),0xddccbb);nbr.position.set(0,.04,.7);mainObj.add(nbr);
        var lzg=_m(new THREE.SphereGeometry(.09,10,10),0xeeddcc);lzg.position.set(-.4,.04,.48);lzg.scale.set(1.5,.55,.78);mainObj.add(lzg);
        var rzg=lzg.clone();rzg.position.x=.4;mainObj.add(rzg);
        var jaw=_m(new THREE.TorusGeometry(.33,.065,8,18,3.14),0xeeddbb);jaw.position.set(0,-.44,.12);mainObj.add(jaw);
        var chin=_m(new THREE.SphereGeometry(.072,10,10),0xeeddbb);chin.position.set(0,-.48,.32);mainObj.add(chin);
        for(var ut=0;ut<9;ut++){{var tooth=_m(new THREE.BoxGeometry(.035,.04,.028),0xffffff);var ta=ut*.32-1.28;tooth.position.set(Math.sin(ta)*.32,-.15,Math.cos(ta)*.22+.35);mainObj.add(tooth);}}
        for(var lt=0;lt<9;lt++){{var ltooth=_m(new THREE.BoxGeometry(.035,.035,.028),0xffffff);var la2=lt*.32-1.28;ltooth.position.set(Math.sin(la2)*.3,-.42,Math.cos(la2)*.2+.18);mainObj.add(ltooth);}}
        var ltmp=_m(new THREE.SphereGeometry(.28,14,14),0xeeddcc);ltmp.position.set(-.62,.12,0);ltmp.scale.set(.5,.8,.6);mainObj.add(ltmp);
        var rtmp=ltmp.clone();rtmp.position.x=.62;mainObj.add(rtmp);
        var fmg=new THREE.Mesh(new THREE.CircleGeometry(.11,16),new THREE.MeshBasicMaterial({{color:0x111111,side:THREE.DoubleSide}}));fmg.position.set(0,-.52,-.18);fmg.rotation.x=-1.0;mainObj.add(fmg);
        var brow=_m(new THREE.CylinderGeometry(.38,.38,.035,14,1,false,0,3.14),0xeeddcc);brow.position.set(0,.28,.58);brow.rotation.x=1.57;mainObj.add(brow);
        }}
        else if(T==10){{
        var bClr=0xeeddcc;var jClr=0xccbbaa;
        var fx=[-.45,-.22,-.05,.12,.28];var fa=[.55,.18,.05,-.05,-.18];
        for(var cp=0;cp<8;cp++){{var carp=_m(new THREE.BoxGeometry(.08,.065,.065),bClr);carp.position.set(-.1+cp%4*.09,-.55+Math.floor(cp/4)*.08,0);mainObj.add(carp);}}
        for(var mc=0;mc<5;mc++){{var meta=_m(new THREE.CylinderGeometry(.028,.032,.38,6),bClr);meta.position.set(fx[mc],-.15+Math.abs(fa[mc])*.1,0);meta.rotation.z=fa[mc]*.35;mainObj.add(meta);var mj=_m(new THREE.SphereGeometry(.032,8,8),jClr);mj.position.set(fx[mc],.05+Math.abs(fa[mc])*.12,0);mainObj.add(mj);}}
        for(var f=0;f<5;f++){{var pp=_m(new THREE.CylinderGeometry(.024,.028,.22,6),bClr);var bx=fx[f]+(f==0?.08:.02)*(f<2?-1:1);pp.position.set(bx,.22+Math.abs(fa[f])*.15,0);pp.rotation.z=fa[f]*.5;mainObj.add(pp);var pj=_m(new THREE.SphereGeometry(.028,8,8),jClr);pj.position.set(bx,.35+Math.abs(fa[f])*.18,0);mainObj.add(pj);if(f>0){{var mp2=_m(new THREE.CylinderGeometry(.021,.024,.16,6),bClr);mp2.position.set(bx,.42+Math.abs(fa[f])*.2,0);mp2.rotation.z=fa[f]*.55;mainObj.add(mp2);var mj2=_m(new THREE.SphereGeometry(.025,8,8),jClr);mj2.position.set(bx,.52+Math.abs(fa[f])*.22,0);mainObj.add(mj2);}}var dp=_m(new THREE.CylinderGeometry(.017,.021,.12,6),bClr);dp.position.set(bx,(f==0?.42:.58)+Math.abs(fa[f])*.23,0);dp.rotation.z=fa[f]*.6;mainObj.add(dp);}}
        var rad=_m(new THREE.CylinderGeometry(.045,.038,.48,8),bClr);rad.position.set(-.05,-.85,0);mainObj.add(rad);
        var uln=_m(new THREE.CylinderGeometry(.038,.032,.48,8),bClr);uln.position.set(.1,-.85,0);mainObj.add(uln);
        }}
        else if(T==11){{
        var enam=_m(new THREE.SphereGeometry(.44,26,26),0xffffff,{{shininess:95}});enam.position.y=.48;enam.scale.set(1,.68,1);mainObj.add(enam);
        for(var cu=0;cu<4;cu++){{var cusp=_m(new THREE.SphereGeometry(.09,10,10),0xffffff);cusp.position.set(Math.cos(cu*1.57)*.15,.78,Math.sin(cu*1.57)*.15);mainObj.add(cusp);}}
        var den=_m(new THREE.SphereGeometry(.36,22,22),0xddcc66);den.position.y=.42;den.scale.set(.88,.62,.88);mainObj.add(den);
        var pulp=_m(new THREE.SphereGeometry(.14,16,16),0xcc3333,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.35}});pulp.position.y=.32;mainObj.add(pulp);
        var r1=_m(new THREE.ConeGeometry(.072,.75,8),0xddcc88);r1.position.set(-.11,-.28,0);mainObj.add(r1);
        var r2=_m(new THREE.ConeGeometry(.072,.75,8),0xddcc88);r2.position.set(.11,-.28,0);mainObj.add(r2);
        var rc1=_m(new THREE.CylinderGeometry(.018,.013,.65,6),0xcc4444,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.25}});rc1.position.set(-.11,-.25,0);mainObj.add(rc1);
        var rc2=rc1.clone();rc2.position.x=.11;mainObj.add(rc2);
        var cem=_m(new THREE.CylinderGeometry(.09,.085,.7,10),0xddddaa,{{transparent:true,opacity:.25}});cem.position.y=-.28;mainObj.add(cem);
        var gin=_m(new THREE.TorusGeometry(.38,.1,8,22),0xff8899);gin.position.y=.08;gin.rotation.x=1.57;mainObj.add(gin);
        var pdl=_m(new THREE.CylinderGeometry(.12,.11,.55,10),0xffccaa,{{transparent:true,opacity:.15}});pdl.position.y=-.18;mainObj.add(pdl);
        var jb=_m(new THREE.BoxGeometry(1.1,.45,.75),0xeeddcc);jb.position.y=-.78;mainObj.add(jb);
        for(var nv=0;nv<3;nv++){{var nvn=_m(new THREE.CylinderGeometry(.006,.006,.25,4),0xffdd44,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.35}});nvn.position.set(-.04+nv*.04,.15,0);mainObj.add(nvn);}}
        }}
        else if(T==12){{
        var belly=_m(new THREE.SphereGeometry(.48,12,12),0xcc4444,{{shininess:30}});belly.scale.set(.58,1.48,.58);mainObj.add(belly);
        var tt=_m(new THREE.CylinderGeometry(.075,.14,.55,10),0xeeeedd,{{shininess:65}});tt.position.y=1.02;mainObj.add(tt);
        var tb=_m(new THREE.CylinderGeometry(.14,.075,.55,10),0xeeeedd,{{shininess:65}});tb.position.y=-1.02;mainObj.add(tb);
        var bt=_m(new THREE.CylinderGeometry(.11,.095,.48,8),0xeeddcc);bt.position.y=1.45;mainObj.add(bt);
        var bb=_m(new THREE.CylinderGeometry(.095,.11,.48,8),0xeeddcc);bb.position.y=-1.45;mainObj.add(bb);
        for(var st=0;st<10;st++){{var str=_m(new THREE.CylinderGeometry(.013,.013,1.75,4),0xbb3333);str.position.set(-.12+st%5*.06,0,-.08+Math.floor(st/5)*.06);mainObj.add(str);}}
        var fas=_m(new THREE.SphereGeometry(.52,18,18),0xeebbbb,{{transparent:true,opacity:.1,side:THREE.BackSide}});fas.scale.set(.62,1.52,.62);mainObj.add(fas);
        for(var bv2=0;bv2<2;bv2++){{var bvn2=_m(new THREE.CylinderGeometry(.008,.008,1.4,4),0xcc3344,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.25}});bvn2.position.set(.2,0,bv2*.12-.06);mainObj.add(bvn2);}}
        }}
        else if(T==13){{
        var soma=_m(new THREE.SphereGeometry(.38,12,12),0xddbb88,{{shininess:30}});soma.position.y=.5;mainObj.add(soma);
        var nuc=_m(new THREE.SphereGeometry(.18,22,22),0x6644aa,{{emissive:new THREE.Color(0x220044),emissiveIntensity:.25}});nuc.position.y=.5;mainObj.add(nuc);
        for(var d=0;d<7;d++){{var den2=_m(new THREE.CylinderGeometry(.028,.018,.45,6),0xddcc88);var da=d*.9;den2.position.set(Math.cos(da)*.35,.72+Math.sin(da)*.15,Math.sin(da)*.25);den2.rotation.z=-Math.cos(da)*.5;den2.rotation.x=Math.sin(da)*.3;mainObj.add(den2);for(var db=0;db<2;db++){{var dbr=_m(new THREE.CylinderGeometry(.013,.008,.22,4),0xccbb77);dbr.position.set(Math.cos(da)*.55+db*.08,.85+Math.sin(da)*.2+db*.06,Math.sin(da)*.35+db*.05);dbr.rotation.z=-Math.cos(da)*.7;mainObj.add(dbr);var dtip=_m(new THREE.SphereGeometry(.015,6,6),0xccbb77);dtip.position.copy(dbr.position);dtip.position.y+=.1;mainObj.add(dtip);}}}}
        var ahil=_m(new THREE.ConeGeometry(.1,.14,10),0xddcc88);ahil.position.y=.22;mainObj.add(ahil);
        var axon=_m(new THREE.CylinderGeometry(.022,.022,2.4,8),0xddcc88);axon.position.y=-1.0;mainObj.add(axon);
        for(var my=0;my<5;my++){{var myl=_m(new THREE.CylinderGeometry(.055,.055,.28,10),0xffffff,{{shininess:72}});myl.position.y=.0-my*.42;mainObj.add(myl);var rnv=_m(new THREE.CylinderGeometry(.028,.028,.045,8),0xddcc88);rnv.position.y=.15-my*.42;mainObj.add(rnv);var scn=_m(new THREE.SphereGeometry(.018,6,6),0x8866cc);scn.position.set(.06,.0-my*.42,.02);mainObj.add(scn);}}
        for(var at=0;at<4;at++){{var atr=_m(new THREE.CylinderGeometry(.018,.013,.18,6),0xddcc88);atr.position.set(-.06+at*.04,-2.15,0);atr.rotation.z=-.15+at*.1;mainObj.add(atr);var syn=_m(new THREE.SphereGeometry(.035,8,8),0xffaa44,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.4}});syn.position.set(-.06+at*.04,-2.28,0);mainObj.add(syn);}}
        }}
        else if(T==14){{
        var comp=_m(new THREE.CylinderGeometry(.34,.34,1.95,22),0xeeddcc,{{shininess:50}});mainObj.add(comp);
        var perio=_m(new THREE.CylinderGeometry(.36,.36,1.95,22),0xddaa88,{{transparent:true,opacity:.12}});mainObj.add(perio);
        var marr=_m(new THREE.CylinderGeometry(.19,.19,1.45,16),0xffcc44,{{transparent:true,opacity:.35}});mainObj.add(marr);
        var epT=_m(new THREE.SphereGeometry(.38,22,22),0xeeddcc);epT.position.y=1.12;epT.scale.set(1,.58,1);mainObj.add(epT);
        var epB=epT.clone();epB.position.y=-1.12;mainObj.add(epB);
        for(var tb2=0;tb2<14;tb2++){{var trb=_m(new THREE.CylinderGeometry(.013,.013,.18,4),0xddccbb);trb.position.set((Math.random()-.5)*.25,1.0+(Math.random()-.5)*.3,(Math.random()-.5)*.25);trb.rotation.set(Math.random()*2,Math.random()*2,Math.random()*2);mainObj.add(trb);}}
        for(var rm=0;rm<8;rm++){{var rms=_m(new THREE.SphereGeometry(.035,6,6),0xcc4444,{{transparent:true,opacity:.28}});rms.position.set((Math.random()-.5)*.2,1.0+(Math.random()-.5)*.2,(Math.random()-.5)*.2);mainObj.add(rms);}}
        for(var hc=0;hc<5;hc++){{var hav=_m(new THREE.CylinderGeometry(.013,.013,1.4,6),0xcc6655,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.2}});hav.position.set(Math.cos(hc*1.26)*.22,0,Math.sin(hc*1.26)*.22);mainObj.add(hav);}}
        var acT=_m(new THREE.SphereGeometry(.4,18,12,0,6.28,0,.95),0xaaddee,{{transparent:true,opacity:.35}});acT.position.y=1.32;mainObj.add(acT);
        var acB=acT.clone();acB.position.y=-1.32;acB.rotation.x=3.14;mainObj.add(acB);
        var endo=_m(new THREE.CylinderGeometry(.21,.21,1.45,14),0xddbbaa,{{transparent:true,opacity:.08}});mainObj.add(endo);
        }}
        else if(T==15){{
        var mkRBC=function(r){{var d=_m(new THREE.SphereGeometry(r,28,28),0xcc3333,{{shininess:50}});d.scale.set(1,.18,1);var t1=_m(new THREE.SphereGeometry(r*.45,12,12),0xaa2222);t1.position.y=r*.05;t1.scale.set(1,.5,1);var t2=t1.clone();t2.position.y=-r*.05;var g=new THREE.Group();g.add(d);g.add(t1);g.add(t2);return g;}};
        var main=mkRBC(.6);mainObj.add(main);
        for(var rb=0;rb<5;rb++){{var rbc=mkRBC(.35);rbc.position.set(-1.2+rb*.55,(Math.random()-.5)*.6,(Math.random()-.5)*.4);rbc.rotation.set(Math.random()*.5,Math.random()*.5,Math.random()*.8);mainObj.add(rbc);}}
        for(var ro=0;ro<3;ro++){{var rou=mkRBC(.32);rou.position.set(.85,.25-ro*.14,.15);mainObj.add(rou);}}
        for(var bg=0;bg<6;bg++){{var bgr=mkRBC(.2);bgr.position.set((Math.random()-.5)*2.5,(Math.random()-.5)*1.5,(Math.random()-.5)*1.5);bgr.material&&(bgr.children[0].material.opacity=.35,bgr.children[0].material.transparent=true);mainObj.add(bgr);}}
        }}
        else if(T==16){{
        var wbc=_m(new THREE.SphereGeometry(.68,32,32),0xeeeeff,{{transparent:true,opacity:.45,shininess:30}});mainObj.add(wbc);
        var ps1=_m(new THREE.SphereGeometry(.18,14,14),0xeeeeff,{{transparent:true,opacity:.35}});ps1.position.set(.58,.18,0);mainObj.add(ps1);
        var ps2=_m(new THREE.SphereGeometry(.14,12,12),0xeeeeff,{{transparent:true,opacity:.35}});ps2.position.set(-.38,.48,.18);mainObj.add(ps2);
        var ps3=_m(new THREE.SphereGeometry(.16,12,12),0xeeeeff,{{transparent:true,opacity:.35}});ps3.position.set(.18,-.48,.28);mainObj.add(ps3);
        var nl1=_m(new THREE.SphereGeometry(.19,18,18),0x6633aa,{{emissive:new THREE.Color(0x220044),emissiveIntensity:.2}});nl1.position.set(-.09,.08,0);mainObj.add(nl1);
        var nl2=_m(new THREE.SphereGeometry(.17,16,16),0x7744bb);nl2.position.set(.09,-.04,.08);mainObj.add(nl2);
        var nl3=_m(new THREE.SphereGeometry(.15,14,14),0x5522aa);nl3.position.set(-.04,-.14,-.08);mainObj.add(nl3);
        var nc1=_m(new THREE.CylinderGeometry(.035,.035,.13,6),0x6633aa);nc1.position.set(0,.02,.04);nc1.rotation.z=.5;mainObj.add(nc1);
        var nc2=_m(new THREE.CylinderGeometry(.035,.035,.11,6),0x6633aa);nc2.position.set(.02,-.09,0);nc2.rotation.z=-.3;mainObj.add(nc2);
        for(var gr2=0;gr2<16;gr2++){{var grn=_m(new THREE.SphereGeometry(.025,6,6),0xcc8844);grn.position.set((Math.random()-.5)*.8,(Math.random()-.5)*.8,(Math.random()-.5)*.5);mainObj.add(grn);}}
        for(var sr=0;sr<5;sr++){{var srbc=_m(new THREE.SphereGeometry(.18,14,14),0xcc3333);srbc.position.set(-1.1+sr*.55,(Math.random()-.5)*.8,(Math.random()-.5)*.3);srbc.scale.set(1,.18,1);mainObj.add(srbc);}}
        }}
        else if(T==17){{
        for(var ip=0;ip<6;ip++){{var plt=_m(new THREE.SphereGeometry(.13,14,14),0xddaaaa);plt.position.set((Math.random()-.5)*1.8,(Math.random()-.5)*1.2,(Math.random()-.5)*.6);plt.scale.set(1,.2,1);plt.rotation.set(Math.random(),Math.random(),Math.random());mainObj.add(plt);}}
        for(var ap=0;ap<3;ap++){{var aplt=_m(new THREE.SphereGeometry(.16,14,14),0xddaaaa);aplt.position.set(-.2+ap*.2,.05+ap*.08,0);aplt.scale.set(1,.25,1);mainObj.add(aplt);for(var pp2=0;pp2<3;pp2++){{var pod=_m(new THREE.ConeGeometry(.025,.09,4),0xddbbbb);pod.position.set(-.2+ap*.2+Math.cos(pp2*2.1)*.15,.05+ap*.08,Math.sin(pp2*2.1)*.12);mainObj.add(pod);}}}}
        for(var fi=0;fi<12;fi++){{var fib=_m(new THREE.CylinderGeometry(.006,.006,.4+Math.random()*.35,4),0xffffcc,{{emissive:new THREE.Color(0x444400),emissiveIntensity:.3}});fib.position.set((Math.random()-.5)*.6,(Math.random()-.5)*.5,(Math.random()-.5)*.3);fib.rotation.set(Math.random()*3,Math.random()*3,Math.random()*3);mainObj.add(fib);}}
        for(var fm=0;fm<8;fm++){{var fmsh=_m(new THREE.CylinderGeometry(.005,.005,.55,4),0xeeee88,{{transparent:true,opacity:.45}});fmsh.position.set((Math.random()-.5)*.4,(Math.random()-.5)*.4,0);fmsh.rotation.set(Math.random()*3.14,0,Math.random()*3.14);mainObj.add(fmsh);}}
        for(var tr2=0;tr2<3;tr2++){{var trbc=_m(new THREE.SphereGeometry(.11,12,12),0xcc3333,{{transparent:true,opacity:.55}});trbc.position.set(-.1+tr2*.1,-.05+tr2*.04,.05);trbc.scale.set(1,.18,1);mainObj.add(trbc);}}
        var sG=new THREE.BufferGeometry();var sP=[];for(var i=0;i<45;i++)sP.push((Math.random()-.5)*3,(Math.random()-.5)*2.5,(Math.random()-.5)*2);sG.setAttribute('position',new THREE.Float32BufferAttribute(sP,3));mainObj.add(new THREE.Points(sG,new THREE.PointsMaterial({{color:0xffcccc,size:.025,transparent:true,opacity:.18}})));
        }}
        else if(T==18){{
        var epi=_m(new THREE.BoxGeometry(2.15,.14,1.15),0xffccaa,{{shininess:40}});epi.position.y=.62;mainObj.add(epi);
        var drm=_m(new THREE.BoxGeometry(2.15,.58,1.15),0xffaaaa);drm.position.y=.18;mainObj.add(drm);
        var hyp=_m(new THREE.BoxGeometry(2.15,.48,1.15),0xffdd88);hyp.position.y=-.34;mainObj.add(hyp);
        var hs=_m(new THREE.CylinderGeometry(.013,.01,.55,6),0x553322);hs.position.set(-.3,.95,0);mainObj.add(hs);
        var hf=_m(new THREE.CylinderGeometry(.032,.018,.45,8),0xddaa88);hf.position.set(-.3,.38,0);mainObj.add(hf);
        var hb=_m(new THREE.SphereGeometry(.035,8,8),0xddaa88);hb.position.set(-.3,.12,0);mainObj.add(hb);
        var seb=_m(new THREE.SphereGeometry(.055,10,10),0xddcc66);seb.position.set(-.18,.42,0);mainObj.add(seb);
        var swg=_m(new THREE.TorusGeometry(.055,.013,6,12),0xaaddff);swg.position.set(.38,.08,0);mainObj.add(swg);
        var swd=_m(new THREE.CylinderGeometry(.009,.009,.45,4),0x88bbdd);swd.position.set(.38,.42,0);mainObj.add(swd);
        for(var bv3=0;bv3<3;bv3++){{var bvn3=_m(new THREE.CylinderGeometry(.01,.01,.75,6),0xcc3344,{{emissive:new THREE.Color(0x441111),emissiveIntensity:.2}});bvn3.position.set(-.5+bv3*.45,.22,0);bvn3.rotation.z=1.57;mainObj.add(bvn3);}}
        for(var vn=0;vn<2;vn++){{var vnl=_m(new THREE.CylinderGeometry(.008,.008,.45,6),0x3355aa);vnl.position.set(.15+vn*.4,.12,0);vnl.rotation.z=1.57;mainObj.add(vnl);}}
        var mei=_m(new THREE.SphereGeometry(.035,8,8),0xffdd44,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.35}});mei.position.set(.08,.52,0);mainObj.add(mei);
        var nf=_m(new THREE.CylinderGeometry(.007,.007,.55,4),0xffdd44,{{emissive:new THREE.Color(0x442200),emissiveIntensity:.25}});nf.position.set(.08,.22,0);mainObj.add(nf);
        for(var fc=0;fc<7;fc++){{var fat=_m(new THREE.SphereGeometry(.072,8,8),0xffee88);fat.position.set(-.6+fc*.2,-.35,0);mainObj.add(fat);}}
        for(var cf=0;cf<4;cf++){{var col=_m(new THREE.CylinderGeometry(.005,.005,.45,4),0xddbbbb,{{transparent:true,opacity:.28}});col.position.set(-.3+cf*.2,.28,0);col.rotation.set(.3,0,.8+cf*.2);mainObj.add(col);}}
        }}
        else if(T==19){{
        var eso2=_m(new THREE.CylinderGeometry(.045,.045,.55,8),0xcc9988);eso2.position.set(0,1.18,0);mainObj.add(eso2);
        var stm=_m(new THREE.SphereGeometry(.32,22,22),0xddaa88);stm.position.set(-.18,.62,0);stm.scale.set(.68,.95,.58);mainObj.add(stm);
        var sfun=_m(new THREE.SphereGeometry(.18,14,14),0xddaa88);sfun.position.set(-.32,.82,0);mainObj.add(sfun);
        var duo=_m(new THREE.TorusGeometry(.14,.045,8,14,3.14),0xddbb88);duo.position.set(.08,.32,0);mainObj.add(duo);
        for(var si=0;si<4;si++){{var sml=_m(new THREE.TorusGeometry(.22+si*.045,.032,6,18),0xffbbaa,{{transparent:true,opacity:.65}});sml.position.y=-.12-si*.08;sml.rotation.x=1.57;sml.rotation.y=si*.4;mainObj.add(sml);}}
        var ac=_m(new THREE.CylinderGeometry(.062,.062,.55,8),0xbb8877);ac.position.set(.58,-.18,0);mainObj.add(ac);
        var tc=_m(new THREE.CylinderGeometry(.062,.062,1.05,8),0xbb8877);tc.position.set(0,.08,0);tc.rotation.z=1.57;mainObj.add(tc);
        var dc=_m(new THREE.CylinderGeometry(.062,.062,.55,8),0xbb8877);dc.position.set(-.58,-.18,0);mainObj.add(dc);
        var sig=_m(new THREE.TorusGeometry(.09,.042,6,10,2.5),0xbb8877);sig.position.set(-.48,-.58,0);mainObj.add(sig);
        var rec=_m(new THREE.CylinderGeometry(.052,.042,.28,8),0xaa7766);rec.position.set(-.28,-.82,0);mainObj.add(rec);
        var liv=_m(new THREE.SphereGeometry(.38,22,22),0x884433);liv.position.set(.48,.72,.12);liv.scale.set(1.15,.55,.65);mainObj.add(liv);
        var gbl=_m(new THREE.SphereGeometry(.072,10,10),0x55aa55);gbl.position.set(.32,.48,.18);mainObj.add(gbl);
        var pan=_m(new THREE.CylinderGeometry(.052,.035,.45,8),0xddcc88);pan.position.set(.12,.28,0);pan.rotation.z=.2;mainObj.add(pan);
        var app=_m(new THREE.CylinderGeometry(.022,.018,.13,6),0xcc8877);app.position.set(.48,-.52,0);mainObj.add(app);
        var bdy=_m(new THREE.SphereGeometry(1.45,16,32),0xffccaa,{{transparent:true,opacity:.028,side:THREE.BackSide}});bdy.position.set(0,.18,0);bdy.scale.set(.58,1.15,.38);mainObj.add(bdy);
        }}
        scene.add(mainObj);"""

    if ci == 4:  # Hayvanlar Alemi — 20 Premium 3D Sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        var _m=function(g,c,o){{var mt=new THREE.MeshPhongMaterial({{color:c,shininess:60}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};
        var _mb=function(g,c,o){{var mt=new THREE.MeshBasicMaterial({{color:c}});if(o){{for(var k in o)mt[k]=o[k];}}return new THREE.Mesh(g,mt);}};

        if(T==0){{
        /* ===== ASLAN ===== */
        var body=_m(new THREE.SphereGeometry(.8,24,24),0xCC8833,{{shininess:30}});body.scale.set(1.4,.9,.85);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.35,20,20),0xCC8833);head.position.set(1.2,.35,0);mainObj.add(head);
        /* Yele */
        for(var i=0;i<20;i++){{var yel=_m(new THREE.SphereGeometry(.12+Math.random()*.08,8,8),0xAA6622,{{transparent:true,opacity:.6}});var a=Math.random()*Math.PI*2;yel.position.set(1.2+Math.cos(a)*.3,.35+Math.sin(a)*.3,Math.sin(a+1)*.3);mainObj.add(yel);}}
        /* Gozler */
        var ey1=_m(new THREE.SphereGeometry(.04,8,8),0xFFCC33);ey1.position.set(1.45,.45,.2);mainObj.add(ey1);
        var ey2=ey1.clone();ey2.position.z=-.2;mainObj.add(ey2);
        var pup1=_mb(new THREE.SphereGeometry(.02,6,6),0x111111);pup1.position.set(1.48,.45,.21);mainObj.add(pup1);
        var pup2=pup1.clone();pup2.position.z=-.21;mainObj.add(pup2);
        /* Bürün */
        var nose=_m(new THREE.SphereGeometry(.06,8,8),0x553322);nose.position.set(1.55,.3,0);mainObj.add(nose);
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.09,.07,.7,8),0xBB7722);var x=i<2?.6:-.4;leg.position.set(x,-.65,i%2?.3:-.3);mainObj.add(leg);var paw=_m(new THREE.SphereGeometry(.09,8,8),0xBB7722);paw.position.set(x,-1,i%2?.3:-.3);mainObj.add(paw);}}
        /* Kuyruk */
        for(var i=0;i<8;i++){{var tl=_m(new THREE.SphereGeometry(.03,6,6),0xCC8833);tl.position.set(-1.2-i*.1,.2+Math.sin(i*.5)*.1,0);mainObj.add(tl);}}
        var tuft=_m(new THREE.SphereGeometry(.07,8,8),0x664411);tuft.position.set(-2,.25,0);mainObj.add(tuft);
        /* Kulaklar */
        var ear1=_m(new THREE.SphereGeometry(.08,8,8),0xCC8833);ear1.position.set(1.1,.65,.2);mainObj.add(ear1);
        var ear2=ear1.clone();ear2.position.z=-.2;mainObj.add(ear2);
        }}

        else if(T==1){{
        /* ===== KARTAL ===== */
        var body=_m(new THREE.SphereGeometry(.5,20,20),0x553322,{{shininess:25}});body.scale.set(1.2,.8,.7);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.2,16,16),0xEEEEDD);head.position.set(.7,.35,0);mainObj.add(head);
        /* Gaga */
        var beak=_m(new THREE.ConeGeometry(.06,.25,8),0xFFCC33,{{shininess:80}});beak.position.set(.95,.3,0);beak.rotation.z=-Math.PI/2;mainObj.add(beak);
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.04,8,8),0xFFDD00);ey.position.set(.82,.4,.12);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.12;mainObj.add(ey2);
        /* Kanatlar */
        for(var side=-1;side<=1;side+=2){{for(var i=0;i<8;i++){{var f=_m(new THREE.BoxGeometry(.3-i*.02,.01,.12-i*.008),0x443322,{{shininess:15}});f.position.set(-.1+i*.02,.15,side*(.35+i*.15));f.rotation.x=side*.1;mainObj.add(f);}}}}
        /* Kuyruk tuyleri */
        for(var i=0;i<5;i++){{var tf=_m(new THREE.BoxGeometry(.2,.008,.08),0x553322);tf.position.set(-.6,0,(i-2)*.1);tf.rotation.y=(i-2)*.05;mainObj.add(tf);}}
        /* Penceler */
        for(var side=-1;side<=1;side+=2){{var leg=_m(new THREE.CylinderGeometry(.03,.025,.35,6),0xFFCC33);leg.position.set(.1,-.4,side*.15);mainObj.add(leg);for(var j=0;j<3;j++){{var cl=_m(new THREE.CylinderGeometry(.01,.005,.12,4),0x333333);cl.position.set(.1+Math.cos(j*.7)*.04,-.6,side*.15+Math.sin(j*.7)*.04);cl.rotation.z=.3;mainObj.add(cl);}}}}
        }}

        else if(T==2){{
        /* ===== YUNUS ===== */
        var body=_m(new THREE.SphereGeometry(.7,24,24),0x6688AA,{{shininess:80}});body.scale.set(2,.7,.6);mainObj.add(body);
        /* Karin — acik renk */
        var belly=_m(new THREE.SphereGeometry(.65,20,20),0xBBCCDD,{{shininess:60}});belly.scale.set(1.8,.5,.55);belly.position.y=-.1;mainObj.add(belly);
        /* Bürün (rostrum) */
        var snout=_m(new THREE.ConeGeometry(.12,.6,12),0x6688AA,{{shininess:70}});snout.position.set(1.5,.05,0);snout.rotation.z=-Math.PI/2;mainObj.add(snout);
        /* Goz */
        var ey=_m(new THREE.SphereGeometry(.04,8,8),0x222222);ey.position.set(1.1,.15,.4);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.4;mainObj.add(ey2);
        /* Sirt yüzgeci */
        var dfin=_m(new THREE.ConeGeometry(.15,.4,8),0x5577AA);dfin.position.set(-.1,.5,0);mainObj.add(dfin);
        /* Gogus yüzgecleri */
        for(var side=-1;side<=1;side+=2){{var pf=_m(new THREE.ConeGeometry(.08,.35,6),0x5577AA);pf.position.set(.5,-.15,side*.5);pf.rotation.z=side*.5;pf.rotation.x=side*.3;mainObj.add(pf);}}
        /* Kuyruk */
        for(var side=-1;side<=1;side+=2){{var flk=_m(new THREE.ConeGeometry(.15,.4,6),0x5577AA);flk.position.set(-1.5,0,side*.2);flk.rotation.z=Math.PI/2;flk.rotation.y=side*.4;mainObj.add(flk);}}
        /* Solunum deligi */
        var bh=_m(new THREE.SphereGeometry(.04,8,8),0x556688);bh.position.set(.5,.5,0);mainObj.add(bh);
        }}

        else if(T==3){{
        /* ===== KELEBEK ===== */
        /* Govde */
        var thorax=_m(new THREE.CylinderGeometry(.04,.04,.3,8),0x222222);mainObj.add(thorax);
        var abdomen=_m(new THREE.CylinderGeometry(.035,.02,.35,8),0x222222);abdomen.position.y=-.3;mainObj.add(abdomen);
        var head=_m(new THREE.SphereGeometry(.06,10,10),0x222222);head.position.y=.2;mainObj.add(head);
        /* Antenler */
        for(var side=-1;side<=1;side+=2){{for(var i=0;i<5;i++){{var an=_m(new THREE.SphereGeometry(.01,4,4),0x333333);an.position.set(side*.03*(1+i*.3),.25+i*.07,0);mainObj.add(an);}}var tip=_m(new THREE.SphereGeometry(.02,6,6),0x333333);tip.position.set(side*.15,.55,0);mainObj.add(tip);}}
        /* Ust kanatlar — renkli */
        for(var side=-1;side<=1;side+=2){{var wing=_m(new THREE.CircleGeometry(.7,20),0xFF6600,{{side:THREE.DoubleSide,transparent:true,opacity:.85}});wing.position.set(side*.4,.1,0);wing.rotation.y=side*.3;wing.scale.set(.8,1,1);mainObj.add(wing);/* Desen */var pat=_m(new THREE.CircleGeometry(.15,12),0x111111,{{side:THREE.DoubleSide}});pat.position.set(side*.5,.2,.01);mainObj.add(pat);var dot=_m(new THREE.CircleGeometry(.06,10),0xFFFFFF,{{side:THREE.DoubleSide}});dot.position.set(side*.35,-.1,.01);mainObj.add(dot);var dot2=_m(new THREE.CircleGeometry(.04,8),0xFFFF00,{{side:THREE.DoubleSide}});dot2.position.set(side*.55,.0,.01);mainObj.add(dot2);}}
        /* Alt kanatlar */
        for(var side=-1;side<=1;side+=2){{var lw=_m(new THREE.CircleGeometry(.5,16),0xFF8800,{{side:THREE.DoubleSide,transparent:true,opacity:.8}});lw.position.set(side*.35,-.25,0);lw.rotation.y=side*.3;mainObj.add(lw);}}
        /* Bacaklar */
        for(var i=0;i<6;i++){{var lg=_m(new THREE.CylinderGeometry(.005,.005,.15,4),0x333333);lg.position.set(-.02+i*.008,-.15,(i%2?1:-1)*.04);lg.rotation.z=.2;mainObj.add(lg);}}
        }}

        else if(T==4){{
        /* ===== AHTAPOT ===== */
        /* Mantle */
        var mantle=_m(new THREE.SphereGeometry(.5,24,24),0xCC4455,{{shininess:50}});mantle.scale.set(.8,1.1,.7);mantle.position.y=.5;mainObj.add(mantle);
        /* Bas/Gozler */
        var head=_m(new THREE.SphereGeometry(.35,20,20),0xCC4455);head.position.y=.1;mainObj.add(head);
        for(var side=-1;side<=1;side+=2){{var ey=_m(new THREE.SphereGeometry(.08,10,10),0xFFCC33);ey.position.set(side*.25,.2,.2);mainObj.add(ey);var pup=_mb(new THREE.SphereGeometry(.04,6,6),0x111111);pup.position.set(side*.28,.2,.26);mainObj.add(pup);}}
        /* 8 kol */
        for(var i=0;i<8;i++){{var a=i*Math.PI/4;for(var j=0;j<10;j++){{var seg=_m(new THREE.SphereGeometry(.04-.002*j,6,6),0xBB3344);var r=.3+j*.12;seg.position.set(Math.cos(a)*r,-.2-j*.08,Math.sin(a)*r);mainObj.add(seg);/* Vantuzlar */if(j%2==0){{var süç=_m(new THREE.TorusGeometry(.025,.008,6,8),0xEEBBCC);süç.position.copy(seg.position);süç.position.y-=.02;mainObj.add(süç);}}}}}}
        /* Sifon */
        var sif=_m(new THREE.CylinderGeometry(.06,.04,.2,8),0xAA3344);sif.position.set(0,-.1,.25);mainObj.add(sif);
        }}

        else if(T==5){{
        /* ===== FIL ===== */
        var body=_m(new THREE.SphereGeometry(1.0,24,24),0x888888,{{shininess:20}});body.scale.set(1.3,1,.9);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.55,20,20),0x888888);head.position.set(1.2,.4,0);mainObj.add(head);
        /* Hortum */
        for(var i=0;i<12;i++){{var tr=_m(new THREE.CylinderGeometry(.08-.004*i,.07-.004*i,.15,8),0x777777);tr.position.set(1.6+i*.03,.3-i*.1,0);tr.rotation.z=-.1*i;mainObj.add(tr);}}
        /* Kulaklar */
        for(var side=-1;side<=1;side+=2){{var ear=_m(new THREE.CircleGeometry(.45,16),0x999999,{{side:THREE.DoubleSide}});ear.position.set(.9,.5,side*.6);ear.rotation.y=side*.3;mainObj.add(ear);}}
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.04,8,8),0x222222);ey.position.set(1.5,.55,.35);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.35;mainObj.add(ey2);
        /* Dişler (fildısıleri) */
        for(var side=-1;side<=1;side+=2){{var tusk=_m(new THREE.CylinderGeometry(.04,.02,.6,8),0xEEDDCC,{{shininess:80}});tusk.position.set(1.6,.0,side*.25);tusk.rotation.z=-.4;mainObj.add(tusk);}}
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.15,.14,.9,10),0x777777);var x=i<2?.7:-.5;leg.position.set(x,-.85,i%2?.35:-.35);mainObj.add(leg);var ft=_m(new THREE.CylinderGeometry(.16,.16,.05,10),0x666666);ft.position.set(x,-1.3,i%2?.35:-.35);mainObj.add(ft);}}
        /* Kuyruk */
        var tail=_m(new THREE.CylinderGeometry(.03,.01,.5,6),0x555555);tail.position.set(-1.3,.2,0);tail.rotation.z=.4;mainObj.add(tail);
        }}

        else if(T==6){{
        /* ===== PENGUEN ===== */
        var body=_m(new THREE.SphereGeometry(.5,20,20),0x222222,{{shininess:40}});body.scale.set(.8,1.2,.7);mainObj.add(body);
        /* Karin — beyaz */
        var belly=_m(new THREE.SphereGeometry(.45,18,18),0xEEEEEE,{{shininess:40}});belly.scale.set(.65,1,.6);belly.position.z=.05;mainObj.add(belly);
        /* Bas */
        var head=_m(new THREE.SphereGeometry(.2,16,16),0x222222);head.position.y=.65;mainObj.add(head);
        /* Gozler + beyaz bant */
        for(var side=-1;side<=1;side+=2){{var wb=_m(new THREE.SphereGeometry(.04,8,8),0xFFFFFF);wb.position.set(side*.12,.7,.12);mainObj.add(wb);var ey=_m(new THREE.SphereGeometry(.025,6,6),0x111111);ey.position.set(side*.13,.7,.15);mainObj.add(ey);}}
        /* Gaga */
        var beak=_m(new THREE.ConeGeometry(.04,.15,8),0xFF8833);beak.position.set(0,.6,.2);beak.rotation.x=-Math.PI/2;mainObj.add(beak);
        /* Kanat/Yuzgecler */
        for(var side=-1;side<=1;side+=2){{var wing=_m(new THREE.ConeGeometry(.08,.45,6),0x333333);wing.position.set(side*.4,.1,0);wing.rotation.z=side*.3;mainObj.add(wing);}}
        /* Ayaklar */
        for(var side=-1;side<=1;side+=2){{var ft=_m(new THREE.BoxGeometry(.12,.03,.15),0xFF8833);ft.position.set(side*.12,-.62,.05);mainObj.add(ft);}}
        }}

        else if(T==7){{
        /* ===== ARI ===== */
        /* Kafa */
        var head=_m(new THREE.SphereGeometry(.2,16,16),0x222222);head.position.set(.45,0,0);mainObj.add(head);
        /* Toraks */
        var thorax=_m(new THREE.SphereGeometry(.22,16,16),0xCC8800);thorax.position.set(.15,0,0);mainObj.add(thorax);
        /* Abdomen — sari siyah seritler */
        var abd=_m(new THREE.SphereGeometry(.3,20,20),0xFFCC00);abd.scale.set(1.3,.8,.8);abd.position.set(-.25,0,0);mainObj.add(abd);
        for(var i=0;i<4;i++){{var str=_m(new THREE.TorusGeometry(.3,.02,8,24),0x222222);str.position.set(-.15-i*.1,0,0);str.rotation.y=Math.PI/2;str.scale.set(1,.8,.8);mainObj.add(str);}}
        /* Kanatlar — saydam */
        for(var side=-1;side<=1;side+=2){{var w1=_mb(new THREE.CircleGeometry(.25,12),0xAABBCC,{{transparent:true,opacity:.3,side:THREE.DoubleSide}});w1.position.set(.15,.15,side*.2);w1.rotation.x=side*.2;mainObj.add(w1);var w2=_mb(new THREE.CircleGeometry(.18,10),0xAABBCC,{{transparent:true,opacity:.25,side:THREE.DoubleSide}});w2.position.set(.0,.12,side*.18);w2.rotation.x=side*.3;mainObj.add(w2);}}
        /* Bacaklar + polen sepeti */
        for(var i=0;i<6;i++){{var lg=_m(new THREE.CylinderGeometry(.015,.01,.2,4),0x222222);lg.position.set(.2-i*.08,-.2,(i%2?.1:-.1));lg.rotation.z=.2;mainObj.add(lg);}}
        var pol=_m(new THREE.SphereGeometry(.04,6,6),0xFFDD44);pol.position.set(-.1,-.25,.1);mainObj.add(pol);
        /* Antenler */
        for(var side=-1;side<=1;side+=2){{var ant=_m(new THREE.CylinderGeometry(.008,.005,.15,4),0x333333);ant.position.set(.55,.1,side*.08);ant.rotation.z=.3;mainObj.add(ant);}}
        /* Igne */
        var sting=_m(new THREE.ConeGeometry(.015,.12,6),0x222222);sting.position.set(-.55,-.02,0);sting.rotation.z=Math.PI/2;mainObj.add(sting);
        /* Gozler */
        for(var side=-1;side<=1;side+=2){{var ey=_m(new THREE.SphereGeometry(.06,10,10),0x442200);ey.position.set(.5,.03,side*.12);mainObj.add(ey);}}
        }}

        else if(T==8){{
        /* ===== YILAN ===== */
        /* Govde — kivrimli silindir dizisi */
        for(var i=0;i<30;i++){{var seg=_m(new THREE.SphereGeometry(.08-.001*i,8,8),i%4<2?0x228B22:0x44AA44);var x=Math.sin(i*.4)*.6;seg.position.set(x,.0-i*.005,-1.5+i*.1);mainObj.add(seg);}}
        /* Bas — üçgen */
        var head=_m(new THREE.SphereGeometry(.12,12,12),0x228B22);head.position.set(0,.05,-1.5);head.scale.set(1.3,.6,1);mainObj.add(head);
        /* Gozler */
        for(var side=-1;side<=1;side+=2){{var ey=_m(new THREE.SphereGeometry(.03,6,6),0xFFCC33);ey.position.set(side*.08,.08,-1.55);mainObj.add(ey);var pup=_mb(new THREE.SphereGeometry(.015,4,4),0x111111);pup.position.set(side*.09,.08,-1.58);mainObj.add(pup);}}
        /* Dil — catalli */
        var tongue=_m(new THREE.CylinderGeometry(.005,.005,.2,4),0xFF2222);tongue.position.set(0,-.02,-1.7);tongue.rotation.x=Math.PI/2;mainObj.add(tongue);
        for(var side=-1;side<=1;side+=2){{var fork=_m(new THREE.CylinderGeometry(.003,.003,.06,3),0xFF2222);fork.position.set(side*.02,-.02,-1.8);fork.rotation.x=Math.PI/2+side*.3;mainObj.add(fork);}}
        /* Pullar — doku */
        for(var i=0;i<15;i++){{var sc=_m(new THREE.CircleGeometry(.02,6),0x1A6B1A,{{side:THREE.DoubleSide}});var x=Math.sin(i*.8)*.5;sc.position.set(x+Math.random()*.05,.09,-1.3+i*.15);sc.lookAt(x,1,-1.3+i*.15);mainObj.add(sc);}}
        }}

        else if(T==9){{
        /* ===== KAPLUMBAGA ===== */
        /* Ust kabuk (karapaks) */
        var shell=_m(new THREE.SphereGeometry(.8,24,24),0x556B2F,{{shininess:30}});shell.scale.set(1.2,.6,1);shell.position.y=.15;mainObj.add(shell);
        /* Kabuk deseni */
        for(var i=0;i<8;i++){{var hex=_m(new THREE.CircleGeometry(.15,6),0x4A5A2A,{{side:THREE.DoubleSide}});var a=i*.8;hex.position.set(Math.cos(a)*.4,.42,Math.sin(a)*.4);hex.lookAt(Math.cos(a)*2,2,Math.sin(a)*2);mainObj.add(hex);}}
        /* Alt kabuk (plastron) */
        var plas=_m(new THREE.SphereGeometry(.7,20,20),0xCCBB88);plas.scale.set(1.1,.3,.9);plas.position.y=-.1;mainObj.add(plas);
        /* Bas */
        var head=_m(new THREE.SphereGeometry(.18,14,14),0x667744);head.position.set(.95,.1,0);mainObj.add(head);
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.03,6,6),0x222222);ey.position.set(1.05,.15,.1);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.1;mainObj.add(ey2);
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.08,.06,.3,8),0x667744);var x=i<2?.5:-.4;leg.position.set(x,-.25,i%2?.4:-.4);mainObj.add(leg);}}
        /* Kuyruk */
        var tail=_m(new THREE.ConeGeometry(.04,.2,6),0x667744);tail.position.set(-.85,0,0);tail.rotation.z=Math.PI/2;mainObj.add(tail);
        }}

        else if(T==10){{
        /* ===== KANGURU ===== */
        var body=_m(new THREE.SphereGeometry(.6,20,20),0xAA7744,{{shininess:25}});body.scale.set(.9,1.2,.7);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.22,16,16),0xAA7744);head.position.set(.3,.8,0);mainObj.add(head);
        /* Kulaklar — uzun */
        for(var side=-1;side<=1;side+=2){{var ear=_m(new THREE.ConeGeometry(.05,.2,8),0xBB8855);ear.position.set(.3,1.05,side*.12);mainObj.add(ear);}}
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.03,6,6),0x222222);ey.position.set(.45,.85,.12);mainObj.add(ey);
        /* Bürün */
        var ns=_m(new THREE.SphereGeometry(.04,8,8),0x553322);ns.position.set(.5,.75,0);mainObj.add(ns);
        /* Arka bacaklar — güçlü */
        for(var side=-1;side<=1;side+=2){{var hleg=_m(new THREE.CylinderGeometry(.1,.08,.7,8),0x997744);hleg.position.set(-.2,-.7,side*.2);hleg.rotation.z=-.2;mainObj.add(hleg);var foot=_m(new THREE.BoxGeometry(.25,.04,.1),0x997744);foot.position.set(-.1,-1.05,side*.2);mainObj.add(foot);}}
        /* On bacaklar — kısa */
        for(var side=-1;side<=1;side+=2){{var fleg=_m(new THREE.CylinderGeometry(.04,.03,.25,6),0xAA7744);fleg.position.set(.3,.15,side*.15);fleg.rotation.z=.5;mainObj.add(fleg);}}
        /* Kuyruk — kalin */
        for(var i=0;i<8;i++){{var tl=_m(new THREE.SphereGeometry(.06-.004*i,6,6),0x997744);tl.position.set(-.3-i*.12,-.5+i*.05,0);mainObj.add(tl);}}
        /* Kese (dışi gosterimi) */
        var poüçh=_m(new THREE.SphereGeometry(.12,10,10),0xBB9966);poüçh.position.set(.1,-.2,.2);mainObj.add(poüçh);
        }}

        else if(T==11){{
        /* ===== BUKALEMUN ===== */
        var body=_m(new THREE.SphereGeometry(.4,20,20),0x44AA44,{{shininess:30}});body.scale.set(1.4,.8,.6);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.2,16,16),0x44AA44);head.position.set(.65,.15,0);mainObj.add(head);
        /* Turret gözler */
        for(var side=-1;side<=1;side+=2){{var eyP=_m(new THREE.SphereGeometry(.1,10,10),0x55BB55);eyP.position.set(.7,.25,side*.18);mainObj.add(eyP);var pup=_m(new THREE.SphereGeometry(.04,6,6),0x222222);pup.position.set(.75,.25,side*.24);mainObj.add(pup);}}
        /* Kask */
        var crest=_m(new THREE.ConeGeometry(.08,.2,8),0x338833);crest.position.set(.65,.35,0);mainObj.add(crest);
        /* Bacaklar — zygodaktil */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.03,.025,.25,6),0x55AA55);var x=i<2?.2:-.3;leg.position.set(x,-.35,i%2?.15:-.15);mainObj.add(leg);}}
        /* Kavrayiçi kuyruk — spiral */
        for(var i=0;i<15;i++){{var tl=_m(new THREE.SphereGeometry(.025-.001*i,6,6),0x44AA44);var a=i*.5;tl.position.set(-.6-i*.05,-.1+Math.sin(a)*.15,Math.cos(a)*.1);mainObj.add(tl);}}
        /* Dil — firlatilmis */
        for(var i=0;i<10;i++){{var dl=_m(new THREE.SphereGeometry(.012,4,4),0xFF6688);dl.position.set(.85+i*.1,.1,0);mainObj.add(dl);}}
        var dlTip=_m(new THREE.SphereGeometry(.04,8,8),0xFF4466);dlTip.position.set(1.85,.1,0);mainObj.add(dlTip);
        }}

        else if(T==12){{
        /* ===== FLAMINGO ===== */
        /* Govde */
        var body=_m(new THREE.SphereGeometry(.35,20,20),0xFF6699,{{shininess:30}});body.scale.set(1,.8,.6);mainObj.add(body);
        /* Boyun — uzun S egri */
        for(var i=0;i<10;i++){{var nk=_m(new THREE.SphereGeometry(.04,6,6),0xFF7799);nk.position.set(.3+Math.sin(i*.3)*.15,.3+i*.1,0);mainObj.add(nk);}}
        /* Bas */
        var head=_m(new THREE.SphereGeometry(.08,12,12),0xFF7799);head.position.set(.35,1.25,0);mainObj.add(head);
        /* Gaga — bukuk */
        var beak=_m(new THREE.ConeGeometry(.03,.12,6),0x333333);beak.position.set(.45,1.2,0);beak.rotation.z=-Math.PI/2-.3;mainObj.add(beak);
        /* Goz */
        var ey=_m(new THREE.SphereGeometry(.02,6,6),0xFFFF00);ey.position.set(.4,1.28,.05);mainObj.add(ey);
        /* Kanatlar */
        for(var side=-1;side<=1;side+=2){{var w=_m(new THREE.ConeGeometry(.2,.5,6),0xFF5588);w.position.set(-.1,.1,side*.3);w.rotation.z=side*.2;mainObj.add(w);}}
        /* Bacaklar — uzun ince */
        for(var side=-1;side<=1;side+=2){{var leg=_m(new THREE.CylinderGeometry(.02,.015,.9,6),0xFF8899);leg.position.set(side*.08,-.6,0);mainObj.add(leg);}}
        /* Ayak */
        for(var side=-1;side<=1;side+=2){{var ft=_m(new THREE.BoxGeometry(.06,.01,.08),0x333333);ft.position.set(side*.08,-1.05,0);mainObj.add(ft);}}
        /* Kuyruk tuyleri */
        for(var i=0;i<3;i++){{var tf=_m(new THREE.ConeGeometry(.03,.15,4),0xFF5577);tf.position.set(-.35,.1,(i-1)*.08);tf.rotation.z=Math.PI/2+.2;mainObj.add(tf);}}
        }}

        else if(T==13){{
        /* ===== KOPEKBALIGI ===== */
        var body=_m(new THREE.SphereGeometry(.6,24,24),0x556677,{{shininess:60}});body.scale.set(2.2,.7,.6);mainObj.add(body);
        /* Karin */
        var belly=_m(new THREE.SphereGeometry(.55,20,20),0xBBCCCC,{{shininess:50}});belly.scale.set(2,.4,.55);belly.position.y=-.1;mainObj.add(belly);
        /* Bas — koni */
        var snout=_m(new THREE.ConeGeometry(.2,.5,12),0x556677);snout.position.set(1.4,.05,0);snout.rotation.z=-Math.PI/2;mainObj.add(snout);
        /* Sirt yüzgeci */
        var dfin=_m(new THREE.ConeGeometry(.12,.45,6),0x445566);dfin.position.set(-.1,.5,0);mainObj.add(dfin);
        /* Kuyruk */
        var utail=_m(new THREE.ConeGeometry(.15,.6,6),0x556677);utail.position.set(-1.4,.3,0);utail.rotation.z=.8;mainObj.add(utail);
        var ltail=_m(new THREE.ConeGeometry(.1,.3,6),0x556677);ltail.position.set(-1.4,-.1,0);ltail.rotation.z=-.3;mainObj.add(ltail);
        /* Gogus yüzgecleri */
        for(var side=-1;side<=1;side+=2){{var pf=_m(new THREE.ConeGeometry(.1,.4,6),0x556677);pf.position.set(.5,-.2,side*.4);pf.rotation.z=side*.3;mainObj.add(pf);}}
        /* Solungac yarikari */
        for(var i=0;i<5;i++){{var gl=_m(new THREE.BoxGeometry(.005,.12,.01),0x334455);gl.position.set(.9+i*.06,.0,.35);mainObj.add(gl);var gl2=gl.clone();gl2.position.z=-.35;mainObj.add(gl2);}}
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.04,8,8),0x111111);ey.position.set(1.2,.15,.3);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.3;mainObj.add(ey2);
        /* Disler */
        for(var i=0;i<8;i++){{var th=_m(new THREE.ConeGeometry(.015,.06,4),0xFFFFFF);th.position.set(1.5+Math.cos(i*.4)*.05,-.08+Math.sin(i*.8)*.02,Math.sin(i*.4)*.12);mainObj.add(th);}}
        }}

        else if(T==14){{
        /* ===== PAPAGAN ===== */
        var body=_m(new THREE.SphereGeometry(.35,20,20),0x33CC33,{{shininess:40}});body.scale.set(.8,1,.6);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.18,16,16),0x33CC33);head.position.set(.15,.5,0);mainObj.add(head);
        /* Gaga — güçlü kanca */
        var ubeak=_m(new THREE.SphereGeometry(.08,10,10),0x333333,{{shininess:80}});ubeak.position.set(.35,.48,0);ubeak.scale.set(1,.8,.7);mainObj.add(ubeak);
        var lbeak=_m(new THREE.SphereGeometry(.05,8,8),0x222222);lbeak.position.set(.32,.4,0);mainObj.add(lbeak);
        /* Gozler — beyaz halka */
        for(var side=-1;side<=1;side+=2){{var wr=_m(new THREE.TorusGeometry(.04,.01,8,12),0xFFFFFF);wr.position.set(.25,.55,side*.12);mainObj.add(wr);var ey=_m(new THREE.SphereGeometry(.025,6,6),0x222222);ey.position.set(.25,.55,side*.13);mainObj.add(ey);}}
        /* Kanatlar — renkli */
        for(var side=-1;side<=1;side+=2){{var w=_m(new THREE.ConeGeometry(.15,.6,6),0x2288CC);w.position.set(-.1,.05,side*.25);w.rotation.z=side*.2;mainObj.add(w);for(var i=0;i<3;i++){{var f=_m(new THREE.BoxGeometry(.15,.005,.06),0xFF3333);f.position.set(-.2-i*.08,-.1+i*.05,side*.28);mainObj.add(f);}}}}
        /* Kuyruk — uzun */
        for(var i=0;i<6;i++){{var tf=_m(new THREE.BoxGeometry(.08,.005,.04),i%2?0xFF3333:0x2288CC);tf.position.set(-.2,-.35-i*.1,(i%3-1)*.04);mainObj.add(tf);}}
        /* Ayaklar — zygodaktil */
        for(var side=-1;side<=1;side+=2){{var ft=_m(new THREE.CylinderGeometry(.02,.015,.15,6),0x666666);ft.position.set(side*.08,-.4,0);mainObj.add(ft);}}
        }}

        else if(T==15){{
        /* ===== GERGEDAN ===== */
        var body=_m(new THREE.SphereGeometry(.9,24,24),0x777777,{{shininess:20}});body.scale.set(1.4,.9,.85);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.4,20,20),0x777777);head.position.set(1.3,.15,0);head.scale.set(1.2,.8,.8);mainObj.add(head);
        /* Boynuzlar */
        var horn1=_m(new THREE.ConeGeometry(.08,.4,8),0xAA9977,{{shininess:50}});horn1.position.set(1.55,.45,0);mainObj.add(horn1);
        var horn2=_m(new THREE.ConeGeometry(.06,.2,8),0xAA9977);horn2.position.set(1.4,.4,0);mainObj.add(horn2);
        /* Kulaklar */
        for(var side=-1;side<=1;side+=2){{var ear=_m(new THREE.ConeGeometry(.06,.12,6),0x888888);ear.position.set(1.1,.45,side*.25);mainObj.add(ear);}}
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.03,6,6),0x222222);ey.position.set(1.45,.2,.25);mainObj.add(ey);
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.13,.12,.7,10),0x666666);var x=i<2?.6:-.5;leg.position.set(x,-.75,i%2?.35:-.35);mainObj.add(leg);}}
        /* Deri kivrimi */
        for(var i=0;i<3;i++){{var fold=_m(new THREE.TorusGeometry(.9,.02,8,32),0x888888,{{transparent:true,opacity:.3}});fold.position.set(-.3+i*.4,0,0);fold.rotation.y=Math.PI/2;fold.scale.set(.85+i*.05,.9,.85);mainObj.add(fold);}}
        }}

        else if(T==16){{
        /* ===== KURT ===== */
        var body=_m(new THREE.SphereGeometry(.55,20,20),0x666666,{{shininess:25}});body.scale.set(1.3,.9,.7);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.22,16,16),0x777777);head.position.set(.8,.3,0);mainObj.add(head);
        /* Bürün — uzun */
        var snout=_m(new THREE.ConeGeometry(.08,.25,8),0x666666);snout.position.set(1.05,.25,0);snout.rotation.z=-Math.PI/2;mainObj.add(snout);
        var nose=_m(new THREE.SphereGeometry(.04,6,6),0x222222);nose.position.set(1.15,.25,0);mainObj.add(nose);
        /* Kulaklar — sivri */
        for(var side=-1;side<=1;side+=2){{var ear=_m(new THREE.ConeGeometry(.05,.15,6),0x777777);ear.position.set(.75,.5,side*.12);mainObj.add(ear);}}
        /* Gozler */
        var ey=_m(new THREE.SphereGeometry(.03,6,6),0xCCAA33);ey.position.set(.9,.35,.12);mainObj.add(ey);
        var ey2=ey.clone();ey2.position.z=-.12;mainObj.add(ey2);
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.05,.04,.5,8),0x666666);var x=i<2?.4:-.3;leg.position.set(x,-.55,i%2?.2:-.2);mainObj.add(leg);}}
        /* Kuyruk — gur */
        for(var i=0;i<8;i++){{var tl=_m(new THREE.SphereGeometry(.04-.003*i,6,6),0x777777);tl.position.set(-.7-i*.06,.1+Math.sin(i*.4)*.05,0);mainObj.add(tl);}}
        /* Tuy dokusu */
        for(var i=0;i<10;i++){{var fur=_m(new THREE.CylinderGeometry(.005,.005,.08,3),0x888888,{{transparent:true,opacity:.3}});fur.position.set((Math.random()-.5)*1,(Math.random()-.3)*.5,(Math.random()-.5)*.5);mainObj.add(fur);}}
        }}

        else if(T==17){{
        /* ===== KOALA ===== */
        var body=_m(new THREE.SphereGeometry(.45,20,20),0xAAAAAA,{{shininess:20}});body.scale.set(.9,1,.7);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.3,18,18),0xBBBBBB);head.position.set(.1,.55,0);mainObj.add(head);
        /* Büyük yuvarlak kulaklar */
        for(var side=-1;side<=1;side+=2){{var ear=_m(new THREE.SphereGeometry(.15,12,12),0xCCCCCC);ear.position.set(0,.8,side*.25);mainObj.add(ear);var earI=_m(new THREE.SphereGeometry(.08,8,8),0xFFCCCC);earI.position.set(.02,.8,side*.28);mainObj.add(earI);}}
        /* Bürün — büyük siyah */
        var nose=_m(new THREE.SphereGeometry(.06,8,8),0x222222);nose.position.set(.35,.5,0);mainObj.add(nose);
        /* Gozler */
        for(var side=-1;side<=1;side+=2){{var ey=_m(new THREE.SphereGeometry(.03,6,6),0x222222);ey.position.set(.3,.6,side*.12);mainObj.add(ey);}}
        /* Kollar — dal kavramaya uygun */
        for(var side=-1;side<=1;side+=2){{var arm=_m(new THREE.CylinderGeometry(.06,.05,.35,8),0xAAAAAA);arm.position.set(.2,.1,side*.3);arm.rotation.z=side*.4;mainObj.add(arm);}}
        /* Bacaklar */
        for(var side=-1;side<=1;side+=2){{var leg=_m(new THREE.CylinderGeometry(.07,.06,.3,8),0xAAAAAA);leg.position.set(-.1,-.35,side*.2);mainObj.add(leg);}}
        /* Okaliptus dali */
        var branch=_m(new THREE.CylinderGeometry(.03,.03,2,6),0x886644);branch.position.set(-.5,0,.3);mainObj.add(branch);
        for(var i=0;i<4;i++){{var leaf=_m(new THREE.SphereGeometry(.06,6,6),0x338833);leaf.scale.set(2,.3,.5);leaf.position.set(-.5+Math.random()*.3,-.4+i*.35,.35);leaf.rotation.z=Math.random();mainObj.add(leaf);}}
        }}

        else if(T==18){{
        /* ===== DENIZATI ===== */
        /* Bas — at şekli */
        var head=_m(new THREE.SphereGeometry(.15,12,12),0xFF8844);head.position.set(0,.8,0);head.scale.set(.8,1,.6);mainObj.add(head);
        /* Bürün — uzun */
        var snout=_m(new THREE.CylinderGeometry(.03,.02,.25,6),0xFF8844);snout.position.set(.15,.75,0);snout.rotation.z=-Math.PI/4;mainObj.add(snout);
        /* Goz */
        var ey=_m(new THREE.SphereGeometry(.03,6,6),0x222222);ey.position.set(.05,.85,.08);mainObj.add(ey);
        /* Taç */
        var crown=_m(new THREE.ConeGeometry(.05,.12,6),0xFFAA55);crown.position.set(-.02,.95,0);mainObj.add(crown);
        /* Govde — kemik plakalar */
        for(var i=0;i<12;i++){{var seg=_m(new THREE.CylinderGeometry(.1-.005*i,.1-.005*i,.08,8),0xFF8844,{{shininess:40}});seg.position.set(0,.65-i*.08,0);mainObj.add(seg);var ring=_m(new THREE.TorusGeometry(.1-.005*i,.008,6,12),0xFFAA66);ring.position.copy(seg.position);mainObj.add(ring);}}
        /* Kuyruk — spiral */
        for(var i=0;i<15;i++){{var tl=_m(new THREE.SphereGeometry(.03-.001*i,6,6),0xFF8844);var a=i*.6;tl.position.set(Math.sin(a)*.1,-.35-i*.04,Math.cos(a)*.1);mainObj.add(tl);}}
        /* Sirt yüzgeci */
        var dfin=_mb(new THREE.CircleGeometry(.08,8),0xFFCC88,{{transparent:true,opacity:.4,side:THREE.DoubleSide}});dfin.position.set(0,.3,.1);mainObj.add(dfin);
        /* Gogus yüzgecleri */
        for(var side=-1;side<=1;side+=2){{var pf=_mb(new THREE.CircleGeometry(.04,6),0xFFCC88,{{transparent:true,opacity:.3,side:THREE.DoubleSide}});pf.position.set(side*.1,.6,0);mainObj.add(pf);}}
        }}

        else if(T==19){{
        /* ===== IGUANA ===== */
        var body=_m(new THREE.SphereGeometry(.4,20,20),0x44AA44,{{shininess:25}});body.scale.set(1.5,.8,.7);mainObj.add(body);
        var head=_m(new THREE.SphereGeometry(.18,14,14),0x44AA44);head.position.set(.75,.2,0);head.scale.set(1.2,.8,.8);mainObj.add(head);
        /* Gerdan derisi (dewlap) */
        var dewlap=_m(new THREE.CircleGeometry(.12,10),0xFF6633,{{side:THREE.DoubleSide,transparent:true,opacity:.6}});dewlap.position.set(.8,0,0);dewlap.rotation.y=Math.PI/2;mainObj.add(dewlap);
        /* Sirt dikenleri */
        for(var i=0;i<12;i++){{var sp=_m(new THREE.ConeGeometry(.02,.1-.003*i,6),0x338833);sp.position.set(.5-i*.1,.35+Math.sin(i*.3)*.05,0);mainObj.add(sp);}}
        /* Gozler */
        for(var side=-1;side<=1;side+=2){{var ey=_m(new THREE.SphereGeometry(.04,8,8),0xFFCC33);ey.position.set(.85,.25,side*.12);mainObj.add(ey);}}
        /* Parietal göz */
        var pEye=_m(new THREE.SphereGeometry(.015,6,6),0xFFFFCC,{{emissive:new THREE.Color(0x666600),emissiveIntensity:.3}});pEye.position.set(.7,.35,0);mainObj.add(pEye);
        /* Bacaklar */
        for(var i=0;i<4;i++){{var leg=_m(new THREE.CylinderGeometry(.04,.03,.3,6),0x44AA44);var x=i<2?.3:-.3;leg.position.set(x,-.35,i%2?.2:-.2);mainObj.add(leg);for(var j=0;j<3;j++){{var claw=_m(new THREE.ConeGeometry(.008,.04,4),0x333333);claw.position.set(x+j*.02-.02,-.52,i%2?.2:-.2);mainObj.add(claw);}}}}
        /* Kuyruk — uzun */
        for(var i=0;i<20;i++){{var tl=_m(new THREE.SphereGeometry(.03-.001*i,6,6),0x44AA44);tl.position.set(-.6-i*.08,-.1+Math.sin(i*.3)*.05,Math.sin(i*.2)*.05);mainObj.add(tl);}}
        /* Pul dokusu */
        for(var i=0;i<8;i++){{var sc=_m(new THREE.CircleGeometry(.025,6),0x3A9A3A,{{side:THREE.DoubleSide}});sc.position.set((Math.random()-.3)*.8,.15,(Math.random()-.5)*.4);sc.lookAt(0,1,0);mainObj.add(sc);}}
        }}

        scene.add(mainObj);"""

    if ci == 5:  # Dinozorlar — 20 premium sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||50,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}

        if(T==0){{
            // T-REX — masif kafatasi, kısa on kollar, devasa arka bacaklar
            var bc=0x7a6b4e;
            // Govde — büyük, yaslanan
            _m(new THREE.SphereGeometry(.65,16,14),bc,{{p:[0,.4,0],s:[1.3,1,.9]}});
            // Boyun — kalin kısa
            _m(new THREE.CylinderGeometry(.22,.3,.5,10),bc,{{p:[.55,.7,0],r:[0,0,-.5]}});
            // Kafatasi — devasa
            _m(new THREE.BoxGeometry(.85,.5,.55),bc,{{p:[1.05,.95,0],sh:60}});
            // Ust cene cikintisi
            _m(new THREE.BoxGeometry(.5,.12,.45),bc,{{p:[1.35,.78,0]}});
            // Alt cene
            _m(new THREE.BoxGeometry(.6,.1,.4),bc,{{p:[1.2,.62,0]}});
            // Disler — ust
            for(var d=0;d<8;d++){{_m(new THREE.ConeGeometry(.025,.12,4),0xeeeecc,{{p:[.95+d*.07,.68,.18],r:[Math.PI,0,0]}});_m(new THREE.ConeGeometry(.025,.12,4),0xeeeecc,{{p:[.95+d*.07,.68,-.18],r:[Math.PI,0,0]}});}}
            // Gozler — ileriye bakan (binokulor)
            _mb(new THREE.SphereGeometry(.06,10,10),0xffdd22,{{p:[1.2,1.02,.22]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[1.23,1.02,.25]}});
            _mb(new THREE.SphereGeometry(.06,10,10),0xffdd22,{{p:[1.2,1.02,-.22]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[1.23,1.02,-.25]}});
            // Goz ustu ibik
            _m(new THREE.BoxGeometry(.15,.08,.12),0x665544,{{p:[1.15,1.1,.2]}});
            _m(new THREE.BoxGeometry(.15,.08,.12),0x665544,{{p:[1.15,1.1,-.2]}});
            // Arka bacaklar — devasa
            _m(new THREE.CylinderGeometry(.14,.1,.9,10),bc,{{p:[-.1,-.15,.3]}});
            _m(new THREE.CylinderGeometry(.1,.12,.4,8),bc,{{p:[-.1,-.65,.3]}});
            _m(new THREE.BoxGeometry(.25,.06,.3),bc,{{p:[-.02,-.88,.3]}});
            _m(new THREE.CylinderGeometry(.14,.1,.9,10),bc,{{p:[-.1,-.15,-.3]}});
            _m(new THREE.CylinderGeometry(.1,.12,.4,8),bc,{{p:[-.1,-.65,-.3]}});
            _m(new THREE.BoxGeometry(.25,.06,.3),bc,{{p:[-.02,-.88,-.3]}});
            // On kollar — kısa 2 parmakli
            _m(new THREE.CylinderGeometry(.04,.035,.25,6),bc,{{p:[.6,.35,.28],r:[0,0,.8]}});
            _m(new THREE.CylinderGeometry(.04,.035,.25,6),bc,{{p:[.6,.35,-.28],r:[0,0,.8]}});
            // Kuyruk — kalin, uzun
            for(var t=0;t<8;t++){{_m(new THREE.SphereGeometry(.2-t*.02,10,8),bc,{{p:[-.6-t*.28,.35+t*.02,0]}});}}
            // Karin alt
            _m(new THREE.SphereGeometry(.45,12,10),0x8a7b5e,{{p:[0,.1,0],s:[1.1,.6,.7]}});
        }}
        else if(T==1){{
            // TRICERATOPS — 3 boynuz, firfir, güçlü govde
            var bc=0x8b7d5c;
            // Govde
            _m(new THREE.SphereGeometry(.7,16,14),bc,{{p:[0,.2,0],s:[1.4,1,.9]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.3,.35,.4,10),bc,{{p:[.7,.35,0],r:[0,0,-.3]}});
            // Kafa
            _m(new THREE.SphereGeometry(.35,14,12),bc,{{p:[1.05,.5,0],s:[1.2,1,.9]}});
            // Gaga
            _m(new THREE.ConeGeometry(.12,.3,8),bc,{{p:[1.4,.42,0],r:[0,0,-1.57]}});
            // Firfir — büyük kemik yaka
            _m(new THREE.SphereGeometry(.55,20,12,0,6.28,0,1.8),0x9b8d6c,{{p:[.7,.65,0],r:[.2,0,.6],s:[1,.15,1]}});
            // Firfir kenari
            for(var f=0;f<10;f++){{var fa=f*.35-.8;_m(new THREE.SphereGeometry(.06,6,6),0xa89d7c,{{p:[.7+Math.cos(fa)*.5,.65+Math.sin(fa)*.45,Math.sin(fa+1)*.15]}});}}
            // Alin boynuzlari — 2 uzun
            _m(new THREE.ConeGeometry(.04,.6,8),0xddccaa,{{p:[1.05,.85,.15],r:[.2,0,.2]}});
            _m(new THREE.ConeGeometry(.04,.6,8),0xddccaa,{{p:[1.05,.85,-.15],r:[-.2,0,.2]}});
            // Bürün boynuzu — kısa
            _m(new THREE.ConeGeometry(.05,.2,6),0xddccaa,{{p:[1.35,.58,0],r:[0,0,.5]}});
            // Gozler
            _mb(new THREE.SphereGeometry(.04,8,8),0x332211,{{p:[1.18,.55,.2]}});
            _mb(new THREE.SphereGeometry(.04,8,8),0x332211,{{p:[1.18,.55,-.2]}});
            // 4 bacak
            for(var i=0;i<4;i++){{var lx=i<2?-.3:.5,lz=i%2?.35:-.35;
            _m(new THREE.CylinderGeometry(.1,.12,.7,8),bc,{{p:[lx,-.3,lz]}});
            _m(new THREE.BoxGeometry(.2,.06,.22),bc,{{p:[lx,-.68,lz]}});}}
            // Kuyruk
            for(var t=0;t<5;t++){{_m(new THREE.SphereGeometry(.18-t*.03,8,6),bc,{{p:[-.7-t*.25,.15-t*.02,0]}});}}
        }}
        else if(T==2){{
            // STEGOSAURUS — sirt plakalari, kuyruk dikenleri
            var bc=0x6b7d4e;
            // Govde
            _m(new THREE.SphereGeometry(.6,16,14),bc,{{p:[0,.15,0],s:[1.5,.9,.85]}});
            // Boyun (egik, bas yere yakin)
            _m(new THREE.CylinderGeometry(.15,.2,.5,8),bc,{{p:[.75,.0,0],r:[0,0,-.8]}});
            // Küçük kafa
            _m(new THREE.SphereGeometry(.15,10,8),bc,{{p:[1.05,-.15,0],s:[1.3,1,1]}});
            _m(new THREE.ConeGeometry(.06,.15,6),bc,{{p:[1.22,-.18,0],r:[0,0,-1.57]}});
            _mb(new THREE.SphereGeometry(.03,6,6),0x222211,{{p:[1.1,-.1,.1]}});
            _mb(new THREE.SphereGeometry(.03,6,6),0x222211,{{p:[1.1,-.1,-.1]}});
            // Sirt plakalari — 17 plaka, 2 sira, zigzag
            for(var p=0;p<9;p++){{var px=-.5+p*.2,py=.55+Math.sin(p*.4)*.15,ps=.1+Math.sin(p*.35+1)*.04;
            _m(new THREE.BoxGeometry(.03,ps*2.5,ps*2),0x8a9b6c,{{p:[px,py,.0],r:[0,0,p*.05-.2]}});}}
            for(var p=0;p<8;p++){{var px=-.4+p*.2,py=.48+Math.sin(p*.4+.5)*.12,ps=.08+Math.sin(p*.35+.5)*.03;
            _m(new THREE.BoxGeometry(.03,ps*2.2,ps*1.8),0x7a8b5c,{{p:[px,py,.0],r:[0,0,p*.05-.15]}});}}
            // Kuyruk dikenleri (thagomizer) — 4 diken
            _m(new THREE.ConeGeometry(.04,.4,6),0xaabb88,{{p:[-1.15,.35,.15],r:[.5,0,-.8]}});
            _m(new THREE.ConeGeometry(.04,.4,6),0xaabb88,{{p:[-1.25,.25,.1],r:[.3,0,-1.1]}});
            _m(new THREE.ConeGeometry(.04,.4,6),0xaabb88,{{p:[-1.15,.35,-.15],r:[-.5,0,-.8]}});
            _m(new THREE.ConeGeometry(.04,.4,6),0xaabb88,{{p:[-1.25,.25,-.1],r:[-.3,0,-1.1]}});
            // Kuyruk
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.15-t*.02,8,6),bc,{{p:[-.6-t*.2,.1+t*.03,0]}});}}
            // 4 bacak (arka uzun, on kısa)
            _m(new THREE.CylinderGeometry(.08,.1,.6,8),bc,{{p:[.4,-.25,.25]}});_m(new THREE.CylinderGeometry(.08,.1,.6,8),bc,{{p:[.4,-.25,-.25]}});
            _m(new THREE.CylinderGeometry(.1,.13,.8,8),bc,{{p:[-.3,-.3,.3]}});_m(new THREE.CylinderGeometry(.1,.13,.8,8),bc,{{p:[-.3,-.3,-.3]}});
        }}
        else if(T==3){{
            // BRONTOSAURUS — çok uzun boyun ve kuyruk, devasa govde
            var bc=0x7a7b5e;
            // Govde — devasa
            _m(new THREE.SphereGeometry(.65,16,14),bc,{{p:[0,0,0],s:[1.3,1,.85]}});
            // Uzun boyun — 6 segment
            for(var n=0;n<7;n++){{var nx=.6+n*.22,ny=.15+n*.18;
            _m(new THREE.SphereGeometry(.15-.01*n,10,8),bc,{{p:[nx,ny,0]}});}}
            // Küçük kafa
            _m(new THREE.SphereGeometry(.1,10,8),bc,{{p:[2.2,1.45,0],s:[1.4,1,1]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0x222211,{{p:[2.32,1.48,.06]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0x222211,{{p:[2.32,1.48,-.06]}});
            // Uzun kuyruk — 10 segment
            for(var t=0;t<10;t++){{_m(new THREE.SphereGeometry(.14-t*.012,8,6),bc,{{p:[-.55-t*.25,-.02+t*.01,0]}});}}
            // 4 sütun bacak
            _m(new THREE.CylinderGeometry(.12,.14,.8,10),bc,{{p:[.35,-.5,.28]}});
            _m(new THREE.CylinderGeometry(.12,.14,.8,10),bc,{{p:[.35,-.5,-.28]}});
            _m(new THREE.CylinderGeometry(.13,.15,.85,10),bc,{{p:[-.25,-.52,.3]}});
            _m(new THREE.CylinderGeometry(.13,.15,.85,10),bc,{{p:[-.25,-.52,-.3]}});
            // Ayak
            for(var f=0;f<4;f++){{var fx=[.35,.35,-.25,-.25][f],fz=[.28,-.28,.3,-.3][f];
            _m(new THREE.BoxGeometry(.22,.06,.22),bc,{{p:[fx,-.95,fz]}});}}
            // Karin
            _m(new THREE.SphereGeometry(.5,12,10),0x8a8b6e,{{p:[0,-.15,0],s:[1.1,.5,.7],op:.8}});
        }}
        else if(T==4){{
            // VELOCIRAPTOR — küçük, cevik, tuylu, orak pence
            var bc=0x7a6644;var fc=0x9a8866;
            // Govde — küçük
            _m(new THREE.SphereGeometry(.3,14,12),bc,{{p:[0,.3,0],s:[1.4,1,.8]}});
            // Tuylenmis govde
            for(var f=0;f<12;f++){{var fa=f*.52;_m(new THREE.ConeGeometry(.02,.15,3),fc,{{p:[-.1+Math.cos(fa)*.2,.3+Math.sin(fa)*.15,Math.sin(fa*2)*.1],r:[Math.random()-.5,0,Math.random()-.5]}});}}
            // Boyun — ince uzun
            _m(new THREE.CylinderGeometry(.06,.1,.35,8),bc,{{p:[.35,.5,0],r:[0,0,-.4]}});
            // Kafa — uzun ve dar
            _m(new THREE.BoxGeometry(.35,.15,.15),bc,{{p:[.6,.65,0]}});
            _m(new THREE.ConeGeometry(.05,.15,6),bc,{{p:[.82,.63,0],r:[0,0,-1.57]}});
            // Disler
            for(var d=0;d<5;d++){{_m(new THREE.ConeGeometry(.01,.05,3),0xeeeecc,{{p:[.5+d*.06,.56,.06],r:[Math.PI,0,0]}});}}
            // Gozler — büyük
            _mb(new THREE.SphereGeometry(.035,8,8),0xffcc22,{{p:[.6,.7,.08]}});
            _mb(new THREE.SphereGeometry(.015,6,6),0x111111,{{p:[.62,.71,.09]}});
            // Arka bacaklar — güçlü
            _m(new THREE.CylinderGeometry(.05,.04,.45,6),bc,{{p:[-.05,.0,.15],r:[0,0,.1]}});
            _m(new THREE.CylinderGeometry(.04,.035,.25,6),bc,{{p:[-.05,-.3,.15]}});
            _m(new THREE.CylinderGeometry(.05,.04,.45,6),bc,{{p:[-.05,.0,-.15],r:[0,0,.1]}});
            _m(new THREE.CylinderGeometry(.04,.035,.25,6),bc,{{p:[-.05,-.3,-.15]}});
            // ORAK PENCE — belirgin
            _m(new THREE.ConeGeometry(.02,.15,4),0xccbbaa,{{p:[.05,-.48,.15],r:[.3,0,.5]}});
            _m(new THREE.ConeGeometry(.02,.15,4),0xccbbaa,{{p:[.05,-.48,-.15],r:[-.3,0,.5]}});
            // On kollar — pençeli
            _m(new THREE.CylinderGeometry(.025,.02,.2,5),bc,{{p:[.3,.25,.15],r:[0,0,.6]}});
            _m(new THREE.CylinderGeometry(.025,.02,.2,5),bc,{{p:[.3,.25,-.15],r:[0,0,.6]}});
            // Sert kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.08-t*.008,6,5),bc,{{p:[-.3-t*.18,.28+t*.01,0]}});}}
            // Kuyruk sertlestiriçi cubuklar
            _m(new THREE.CylinderGeometry(.008,.008,.8,4),0x998877,{{p:[-.7,.33,0],r:[0,0,1.57]}});
        }}
        else if(T==5){{
            // SPINOSAURUS — sirt yelkeni, timsah kafa, yari-süçul
            var bc=0x6b6644;var sc=0xcc8855;
            // Govde
            _m(new THREE.SphereGeometry(.6,16,14),bc,{{p:[0,.15,0],s:[1.4,1,.85]}});
            // Sirt yelkeni — BELIRGIN
            for(var s=0;s<12;s++){{var sx=-.5+s*.12,sh=.25+Math.sin(s*.28+.5)*.2;
            _m(new THREE.BoxGeometry(.015,sh,.01),sc,{{p:[sx,.55+sh/2,0],op:.7,ds:true}});}}
            _m(new THREE.PlaneGeometry(1.3,.7),sc,{{p:[0,.75,0],op:.45,ds:true}});
            // Uzun boyun
            _m(new THREE.CylinderGeometry(.12,.18,.6,8),bc,{{p:[.65,.4,0],r:[0,0,-.5]}});
            // Timsah kafasi — uzun ve dar
            _m(new THREE.BoxGeometry(.7,.18,.2),bc,{{p:[1.2,.6,0]}});
            _m(new THREE.BoxGeometry(.3,.06,.18),bc,{{p:[1.45,.5,0]}});
            // Konik dışler
            for(var d=0;d<8;d++){{_m(new THREE.ConeGeometry(.015,.08,4),0xeeeedd,{{p:[.95+d*.08,.49,.08],r:[Math.PI,0,0]}});}}
            // Gozler
            _mb(new THREE.SphereGeometry(.035,8,8),0xddaa22,{{p:[1.0,.68,.1]}});
            _mb(new THREE.SphereGeometry(.035,8,8),0xddaa22,{{p:[1.0,.68,-.1]}});
            // Arka bacaklar (kısa)
            _m(new THREE.CylinderGeometry(.1,.08,.55,8),bc,{{p:[-.15,-.2,.25]}});
            _m(new THREE.CylinderGeometry(.1,.08,.55,8),bc,{{p:[-.15,-.2,-.25]}});
            // On kollar (büyük, penceli)
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[.4,.05,.22],r:[0,0,.5]}});
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[.4,.05,-.22],r:[0,0,.5]}});
            // Kurek kuyruk
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.16-t*.02,8,6),bc,{{p:[-.55-t*.22,.1,0]}});}}
            _m(new THREE.BoxGeometry(.08,.35,.02),bc,{{p:[-1.6,.1,0],ds:true}});
        }}
        else if(T==6){{
            // PTERANODON — dev kanatlar, ibik, gaga
            var bc=0x9a8877;var wc=0xbbaa88;
            // Govde — küçük
            _m(new THREE.SphereGeometry(.2,12,10),bc,{{p:[0,.2,0],s:[1.2,1,.8]}});
            // Kafa + uzun ibik
            _m(new THREE.SphereGeometry(.12,10,8),bc,{{p:[.3,.4,0],s:[1.3,1,.8]}});
            _m(new THREE.ConeGeometry(.03,.5,6),bc,{{p:[.15,.65,0],r:[0,0,.3]}});
            // Uzun gaga
            _m(new THREE.ConeGeometry(.04,.35,6),0xccbb99,{{p:[.55,.35,0],r:[0,0,-1.57]}});
            // Goz
            _mb(new THREE.SphereGeometry(.02,6,6),0x111111,{{p:[.35,.43,.07]}});
            // KANATLAR — geniş deri zar
            // Sol kanat
            _m(new THREE.PlaneGeometry(1.8,.5),wc,{{p:[-1,.25,.01],r:[0,0,.15],op:.5,ds:true}});
            _m(new THREE.CylinderGeometry(.015,.01,1.8,4),bc,{{p:[-1,.4,.0],r:[0,0,1.5]}});
            // Sag kanat
            _m(new THREE.PlaneGeometry(1.8,.5),wc,{{p:[-1,.25,-.01],r:[0,0,.15],op:.5,ds:true}});
            // Kanat parmak kemikleri
            for(var k=0;k<3;k++){{_m(new THREE.CylinderGeometry(.008,.006,.6-k*.15,3),bc,{{p:[-.5-k*.35,.15+k*.05,.0],r:[0,0,1.4+k*.1]}});}}
            // Arka bacaklar
            _m(new THREE.CylinderGeometry(.025,.02,.25,5),bc,{{p:[-.1,0,.08]}});
            _m(new THREE.CylinderGeometry(.025,.02,.25,5),bc,{{p:[-.1,0,-.08]}});
            // Kısa kuyruk
            _m(new THREE.ConeGeometry(.04,.15,6),bc,{{p:[-.25,.18,0],r:[0,0,1.2]}});
        }}
        else if(T==7){{
            // ANKYLOSAURUS — zirh plakalari, kuyruk topuzu
            var bc=0x6b6b55;var ac=0x888877;
            // Govde — geniş ve düşük
            _m(new THREE.SphereGeometry(.6,16,14),bc,{{p:[0,.15,0],s:[1.3,.65,1.1]}});
            // Zirh plakalari (osteoderms)
            for(var a=0;a<20;a++){{var ax=-.5+Math.random()*1,az=-.4+Math.random()*.8,ay=.35+Math.random()*.15;
            _m(new THREE.BoxGeometry(.12,.06,.12),ac,{{p:[ax,ay,az],r:[0,Math.random(),0]}});}}
            // Yan dikenler
            for(var s=0;s<6;s++){{var sx=-.4+s*.2;
            _m(new THREE.ConeGeometry(.04,.12,4),ac,{{p:[sx,.1,.5],r:[.8,0,0]}});
            _m(new THREE.ConeGeometry(.04,.12,4),ac,{{p:[sx,.1,-.5],r:[-.8,0,0]}});}}
            // Kafa — geniş, zirhlı
            _m(new THREE.BoxGeometry(.35,.2,.35),bc,{{p:[.7,.1,0]}});
            _m(new THREE.BoxGeometry(.15,.06,.3),ac,{{p:[.75,.22,0]}});
            // Gaga
            _m(new THREE.ConeGeometry(.06,.12,6),bc,{{p:[.92,.08,0],r:[0,0,-1.57]}});
            // Goz ustu koruma
            _m(new THREE.ConeGeometry(.04,.08,4),ac,{{p:[.75,.22,.14],r:[.4,0,0]}});
            _m(new THREE.ConeGeometry(.04,.08,4),ac,{{p:[.75,.22,-.14],r:[-.4,0,0]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0x332211,{{p:[.8,.14,.16]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0x332211,{{p:[.8,.14,-.16]}});
            // 4 kısa güçlü bacak
            for(var i=0;i<4;i++){{var lx=i<2?.3:-.3,lz=i%2?.35:-.35;
            _m(new THREE.CylinderGeometry(.09,.11,.4,8),bc,{{p:[lx,-.2,lz]}});}}
            // Kuyruk + TOPUZ
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.12-t*.008,8,6),bc,{{p:[-.55-t*.2,.1,0]}});}}
            // Kuyruk topuzu — büyük
            _m(new THREE.SphereGeometry(.2,10,8),ac,{{p:[-1.8,.08,0],s:[1.3,.7,1.2],sh:70}});
        }}
        else if(T==8){{
            // PARASAUROLOPHUS — tup ibik, ordek gagasi
            var bc=0x7a8855;
            // Govde
            _m(new THREE.SphereGeometry(.55,16,14),bc,{{p:[0,.2,0],s:[1.3,.95,.8]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.1,.15,.45,8),bc,{{p:[.55,.5,0],r:[0,0,-.4]}});
            // Kafa
            _m(new THREE.SphereGeometry(.18,12,10),bc,{{p:[.85,.7,0],s:[1.3,1,.9]}});
            // UZUN TUP IBIK — belirgin
            _m(new THREE.CylinderGeometry(.04,.03,.9,8),0x8a9965,{{p:[.5,1.05,0],r:[0,0,1.0]}});
            _m(new THREE.SphereGeometry(.04,6,6),0x8a9965,{{p:[.1,1.25,0]}});
            // Ordek gagasi
            _m(new THREE.BoxGeometry(.25,.08,.14),0x998866,{{p:[1.05,.65,0]}});
            _m(new THREE.BoxGeometry(.12,.04,.12),0x998866,{{p:[1.15,.59,0]}});
            // Gozler
            _mb(new THREE.SphereGeometry(.03,8,8),0x223311,{{p:[.92,.75,.1]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0x223311,{{p:[.92,.75,-.1]}});
            // Arka bacaklar (güçlü)
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.2,.2]}});
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.2,-.2]}});
            // On kollar
            _m(new THREE.CylinderGeometry(.05,.04,.35,6),bc,{{p:[.35,.05,.18],r:[0,0,.3]}});
            _m(new THREE.CylinderGeometry(.05,.04,.35,6),bc,{{p:[.35,.05,-.18],r:[0,0,.3]}});
            // Kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.14-t*.015,8,6),bc,{{p:[-.5-t*.2,.15,0]}});}}
        }}
        else if(T==9){{
            // DIPLODOCUS — en uzun boyun+kuyruk
            var bc=0x7a7a5e;
            // Govde
            _m(new THREE.SphereGeometry(.55,16,14),bc,{{p:[0,0,0],s:[1.2,.9,.8]}});
            // Çok uzun boyun — 8 segment
            for(var n=0;n<9;n++){{var nx=.5+n*.2,ny=.1+n*.15;
            _m(new THREE.SphereGeometry(.12-.005*n,8,6),bc,{{p:[nx,ny,0]}});}}
            // Küçük kafa
            _m(new THREE.SphereGeometry(.08,8,6),bc,{{p:[2.35,1.35,0],s:[1.5,1,1]}});
            _mb(new THREE.SphereGeometry(.02,5,5),0x222211,{{p:[2.42,1.37,.05]}});
            // Çok uzun kuyruk — 12 segment (kirbac)
            for(var t=0;t<13;t++){{_m(new THREE.SphereGeometry(.12-t*.008,6,5),bc,{{p:[-.45-t*.2,-.02+t*.005,0]}});}}
            // 4 sütun bacak
            _m(new THREE.CylinderGeometry(.1,.12,.7,8),bc,{{p:[.3,-.4,.22]}});
            _m(new THREE.CylinderGeometry(.1,.12,.7,8),bc,{{p:[.3,-.4,-.22]}});
            _m(new THREE.CylinderGeometry(.11,.13,.75,8),bc,{{p:[-.2,-.42,.24]}});
            _m(new THREE.CylinderGeometry(.11,.13,.75,8),bc,{{p:[-.2,-.42,-.24]}});
        }}
        else if(T==10){{
            // ALLOSAURUS — göz ustu ibikler, balta kafatasi
            var bc=0x776655;
            // Govde
            _m(new THREE.SphereGeometry(.5,16,14),bc,{{p:[0,.3,0],s:[1.3,1,.85]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.12,.18,.45,8),bc,{{p:[.5,.6,0],r:[0,0,-.45]}});
            // Kafatasi — balta sekilli
            _m(new THREE.BoxGeometry(.55,.3,.3),bc,{{p:[.9,.8,0]}});
            _m(new THREE.BoxGeometry(.3,.08,.25),bc,{{p:[1.1,.68,0]}});
            // Goz ustu ibikler — BELIRGIN
            _m(new THREE.BoxGeometry(.12,.1,.08),0xaa6644,{{p:[.85,.98,.12]}});
            _m(new THREE.BoxGeometry(.12,.1,.08),0xaa6644,{{p:[.85,.98,-.12]}});
            // Disler
            for(var d=0;d<6;d++){{_m(new THREE.ConeGeometry(.015,.08,3),0xeeddcc,{{p:[.7+d*.07,.62,.12],r:[Math.PI,0,0]}});}}
            // Gozler
            _mb(new THREE.SphereGeometry(.035,8,8),0xddaa11,{{p:[.88,.85,.15]}});
            _mb(new THREE.SphereGeometry(.035,8,8),0xddaa11,{{p:[.88,.85,-.15]}});
            // Güçlu arka bacaklar
            _m(new THREE.CylinderGeometry(.1,.08,.75,8),bc,{{p:[-.1,-.15,.22]}});
            _m(new THREE.CylinderGeometry(.1,.08,.75,8),bc,{{p:[-.1,-.15,-.22]}});
            _m(new THREE.BoxGeometry(.2,.05,.2),bc,{{p:[-.05,-.56,.22]}});
            _m(new THREE.BoxGeometry(.2,.05,.2),bc,{{p:[-.05,-.56,-.22]}});
            // Üç parmakli on kollar — güçlü
            _m(new THREE.CylinderGeometry(.05,.04,.3,6),bc,{{p:[.4,.2,.2],r:[0,0,.6]}});
            _m(new THREE.CylinderGeometry(.05,.04,.3,6),bc,{{p:[.4,.2,-.2],r:[0,0,.6]}});
            for(var c=0;c<3;c++){{_m(new THREE.ConeGeometry(.012,.06,3),0xbbaa88,{{p:[.52,.12+c*.03,.2+c*.02-.03],r:[0,0,1]}});}}
            // Kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.15-t*.015,8,6),bc,{{p:[-.5-t*.22,.25,0]}});}}
        }}
        else if(T==11){{
            // PLESIOSAURUS — uzun boyun, 4 yüzgec, deniz sürüngeni
            var bc=0x556677;var fc=0x667788;
            // Govde — aerodinamik
            _m(new THREE.SphereGeometry(.45,16,14),bc,{{p:[0,0,0],s:[1.5,.7,.9]}});
            // Çok uzun boyun — 10 segment
            for(var n=0;n<11;n++){{var nx=.5+n*.18,ny=n*.12;
            _m(new THREE.SphereGeometry(.08-.002*n,8,6),bc,{{p:[nx,ny,0]}});}}
            // Küçük kafa
            _m(new THREE.SphereGeometry(.08,8,6),bc,{{p:[2.5,1.2,0],s:[1.6,1,1]}});
            _mb(new THREE.SphereGeometry(.02,5,5),0x111122,{{p:[2.58,1.23,.05]}});
            // Ic içe gecen dışler
            for(var d=0;d<5;d++){{_m(new THREE.ConeGeometry(.008,.06,3),0xddddcc,{{p:[2.55+d*.03,1.14,.04],r:[Math.PI,0,0]}});}}
            // 4 yüzgec — kanat şeklinde
            _m(new THREE.PlaneGeometry(.6,.18),fc,{{p:[.25,-.1,.4],r:[-.3,.3,0],op:.7,ds:true}});
            _m(new THREE.PlaneGeometry(.6,.18),fc,{{p:[.25,-.1,-.4],r:[.3,.3,0],op:.7,ds:true}});
            _m(new THREE.PlaneGeometry(.5,.15),fc,{{p:[-.25,-.1,.35],r:[-.3,-.3,0],op:.7,ds:true}});
            _m(new THREE.PlaneGeometry(.5,.15),fc,{{p:[-.25,-.1,-.35],r:[.3,-.3,0],op:.7,ds:true}});
            // Kuyruk — kısa
            for(var t=0;t<4;t++){{_m(new THREE.SphereGeometry(.1-t*.02,6,5),bc,{{p:[-.55-t*.15,-.02,0]}});}}
            // Su efekti
            for(var w=0;w<8;w++){{_mb(new THREE.SphereGeometry(.04,5,4),0x4488cc,{{p:[(Math.random()-.5)*2.5,(Math.random()-.5)*.8,(Math.random()-.5)*1],op:.15}});}}
        }}
        else if(T==12){{
            // PACHYCEPHALOSAURUS — kubbe kafatasi
            var bc=0x7a7755;
            // Govde
            _m(new THREE.SphereGeometry(.4,14,12),bc,{{p:[0,.25,0],s:[1.2,.95,.8]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.08,.12,.3,8),bc,{{p:[.4,.5,0],r:[0,0,-.3]}});
            // Kafa
            _m(new THREE.SphereGeometry(.15,12,10),bc,{{p:[.6,.65,0]}});
            // KUBBE — kalin, yuvarlak, belirgin
            _m(new THREE.SphereGeometry(.18,14,10,0,6.28,0,1.8),0x8a8866,{{p:[.6,.78,0],sh:80}});
            // Kubbe çevresi cikintilari
            for(var k=0;k<8;k++){{var ka=k*.8;
            _m(new THREE.SphereGeometry(.03,5,4),0x9a9876,{{p:[.6+Math.cos(ka)*.16,.68+Math.sin(ka)*.06,Math.sin(ka)*.12]}});}}
            // Küçük gaga
            _m(new THREE.ConeGeometry(.04,.12,6),bc,{{p:[.78,.6,0],r:[0,0,-1.57]}});
            // Gozler
            _mb(new THREE.SphereGeometry(.025,6,6),0x332211,{{p:[.68,.65,.1]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0x332211,{{p:[.68,.65,-.1]}});
            // Arka bacaklar — güçlü
            _m(new THREE.CylinderGeometry(.07,.06,.55,8),bc,{{p:[-.05,-.1,.15]}});
            _m(new THREE.CylinderGeometry(.07,.06,.55,8),bc,{{p:[-.05,-.1,-.15]}});
            // Kısa on kollar
            _m(new THREE.CylinderGeometry(.03,.025,.2,5),bc,{{p:[.25,.15,.12],r:[0,0,.5]}});
            _m(new THREE.CylinderGeometry(.03,.025,.2,5),bc,{{p:[.25,.15,-.12],r:[0,0,.5]}});
            // Kuyruk — sert
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.1-t*.012,7,5),bc,{{p:[-.35-t*.18,.2,0]}});}}
        }}
        else if(T==13){{
            // DILOPHOSAURUS — cift tepecik, cevik
            var bc=0x6b7755;
            // Govde
            _m(new THREE.SphereGeometry(.4,14,12),bc,{{p:[0,.3,0],s:[1.3,.95,.8]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.08,.12,.4,8),bc,{{p:[.45,.55,0],r:[0,0,-.4]}});
            // Kafa — ince uzun
            _m(new THREE.BoxGeometry(.35,.15,.18),bc,{{p:[.75,.75,0]}});
            _m(new THREE.ConeGeometry(.05,.15,6),bc,{{p:[.95,.72,0],r:[0,0,-1.57]}});
            // CIFT TEPECIK — belirgin cift ibik
            _m(new THREE.BoxGeometry(.18,.15,.03),0xaa8855,{{p:[.7,.88,.04],r:[0,0,.2],ds:true}});
            _m(new THREE.BoxGeometry(.18,.15,.03),0xaa8855,{{p:[.7,.88,-.04],r:[0,0,.2],ds:true}});
            // Gozler
            _mb(new THREE.SphereGeometry(.025,6,6),0xddaa22,{{p:[.8,.78,.09]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0xddaa22,{{p:[.8,.78,-.09]}});
            // Disler
            for(var d=0;d<5;d++){{_m(new THREE.ConeGeometry(.01,.05,3),0xeeddcc,{{p:[.65+d*.06,.66,.07],r:[Math.PI,0,0]}});}}
            // Arka bacaklar
            _m(new THREE.CylinderGeometry(.08,.06,.6,8),bc,{{p:[-.1,-.05,.18]}});
            _m(new THREE.CylinderGeometry(.08,.06,.6,8),bc,{{p:[-.1,-.05,-.18]}});
            // On kollar
            _m(new THREE.CylinderGeometry(.035,.03,.2,5),bc,{{p:[.3,.2,.15],r:[0,0,.6]}});
            _m(new THREE.CylinderGeometry(.035,.03,.2,5),bc,{{p:[.3,.2,-.15],r:[0,0,.6]}});
            // Kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.12-t*.012,7,5),bc,{{p:[-.4-t*.2,.25,0]}});}}
        }}
        else if(T==14){{
            // IGUANODON — basparmak dikeni, gagamsi agiz
            var bc=0x7a8855;
            // Govde
            _m(new THREE.SphereGeometry(.55,16,14),bc,{{p:[0,.25,0],s:[1.3,.95,.85]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.1,.15,.4,8),bc,{{p:[.55,.5,0],r:[0,0,-.35]}});
            // Kafa
            _m(new THREE.SphereGeometry(.16,12,10),bc,{{p:[.8,.7,0],s:[1.3,1,.9]}});
            // Gaga
            _m(new THREE.BoxGeometry(.15,.08,.12),0x998866,{{p:[.98,.66,0]}});
            // Gozler
            _mb(new THREE.SphereGeometry(.03,8,8),0x332211,{{p:[.85,.75,.1]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0x332211,{{p:[.85,.75,-.1]}});
            // Arka bacaklar — güçlü
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.15,.22]}});
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.15,-.22]}});
            // On kollar + BASPARMAK DIKENI
            _m(new THREE.CylinderGeometry(.05,.04,.3,6),bc,{{p:[.35,.1,.2],r:[0,0,.5]}});
            _m(new THREE.CylinderGeometry(.05,.04,.3,6),bc,{{p:[.35,.1,-.2],r:[0,0,.5]}});
            // Basparmak dikenleri — BELIRGIN
            _m(new THREE.ConeGeometry(.035,.2,6),0xccbb88,{{p:[.48,.15,.22],r:[0,0,.8]}});
            _m(new THREE.ConeGeometry(.035,.2,6),0xccbb88,{{p:[.48,.15,-.22],r:[0,0,.8]}});
            // Kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.15-t*.015,8,6),bc,{{p:[-.5-t*.2,.2,0]}});}}
        }}
        else if(T==15){{
            // COMPSOGNATHUS — çok küçük, cevik, hizli
            var bc=0x887766;
            // Küçük govde
            _m(new THREE.SphereGeometry(.15,12,10),bc,{{p:[0,.35,0],s:[1.3,1,.8]}});
            // Ince boyun
            _m(new THREE.CylinderGeometry(.03,.05,.2,6),bc,{{p:[.18,.45,0],r:[0,0,-.4]}});
            // Küçük kafa — büyük gözlu
            _m(new THREE.SphereGeometry(.08,10,8),bc,{{p:[.28,.52,0],s:[1.3,1,.9]}});
            _m(new THREE.ConeGeometry(.025,.1,5),bc,{{p:[.38,.5,0],r:[0,0,-1.57]}});
            // Büyük gözler
            _mb(new THREE.SphereGeometry(.025,6,6),0xddcc22,{{p:[.32,.56,.05]}});
            _mb(new THREE.SphereGeometry(.012,4,4),0x111111,{{p:[.34,.57,.06]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0xddcc22,{{p:[.32,.56,-.05]}});
            // Küçük dışler
            for(var d=0;d<3;d++){{_m(new THREE.ConeGeometry(.005,.03,3),0xeeeedd,{{p:[.32+d*.03,.47,.03],r:[Math.PI,0,0]}});}}
            // Ince arka bacaklar
            _m(new THREE.CylinderGeometry(.025,.02,.3,5),bc,{{p:[-.02,.15,.06]}});
            _m(new THREE.CylinderGeometry(.025,.02,.3,5),bc,{{p:[-.02,.15,-.06]}});
            _m(new THREE.CylinderGeometry(.02,.015,.15,4),bc,{{p:[-.02,-.02,.06]}});
            _m(new THREE.CylinderGeometry(.02,.015,.15,4),bc,{{p:[-.02,-.02,-.06]}});
            // Küçük on kollar
            _m(new THREE.CylinderGeometry(.012,.01,.1,4),bc,{{p:[.1,.3,.05],r:[0,0,.6]}});
            _m(new THREE.CylinderGeometry(.012,.01,.1,4),bc,{{p:[.1,.3,-.05],r:[0,0,.6]}});
            // Uzun kuyruk
            for(var t=0;t<8;t++){{_m(new THREE.SphereGeometry(.04-t*.003,5,4),bc,{{p:[-.12-t*.1,.32+t*.005,0]}});}}
            // Proto-tuyler
            for(var f=0;f<6;f++){{_m(new THREE.ConeGeometry(.008,.06,3),0x998877,{{p:[-.05+Math.cos(f)*.1,.38+Math.sin(f)*.05,Math.sin(f*2)*.04],r:[Math.random()-.5,0,Math.random()-.5]}});}}
        }}
        else if(T==16){{
            // ARCHAEOPTERYX — gecis formu, tuyler+dışler+pence
            var bc=0x665544;var fc=0x888866;
            // Küçük govde
            _m(new THREE.SphereGeometry(.12,12,10),bc,{{p:[0,.35,0],s:[1.2,1,.8]}});
            // Tuy kaplamali govde
            for(var f=0;f<8;f++){{_m(new THREE.ConeGeometry(.015,.1,3),fc,{{p:[-.03+Math.cos(f*.8)*.08,.35+Math.sin(f*.8)*.06,Math.sin(f*1.5)*.05],r:[Math.random()-.5,0,Math.random()-.5]}});}}
            // Boyun
            _m(new THREE.CylinderGeometry(.025,.04,.15,6),bc,{{p:[.12,.44,0],r:[0,0,-.3]}});
            // Kafa — dışli (dinozor özelliği)
            _m(new THREE.SphereGeometry(.06,8,6),bc,{{p:[.2,.5,0],s:[1.4,1,.9]}});
            _m(new THREE.ConeGeometry(.02,.08,5),bc,{{p:[.3,.48,0],r:[0,0,-1.57]}});
            // Disler (kuşlarda yok)
            for(var d=0;d<3;d++){{_m(new THREE.ConeGeometry(.004,.025,3),0xeeeedd,{{p:[.22+d*.02,.46,.025],r:[Math.PI,0,0]}});}}
            // Goz
            _mb(new THREE.SphereGeometry(.015,5,5),0x332211,{{p:[.22,.52,.035]}});
            // KANATLAR — asimetrik üçus tuyleri
            for(var w=0;w<6;w++){{var wl=.12+w*.05;
            _m(new THREE.PlaneGeometry(wl,.03),fc,{{p:[-.05-w*.06,.32-w*.01,.01+w*.02],r:[-.2,0,.3+w*.1],op:.7,ds:true}});
            _m(new THREE.PlaneGeometry(wl,.03),fc,{{p:[-.05-w*.06,.32-w*.01,-.01-w*.02],r:[.2,0,.3+w*.1],op:.7,ds:true}});}}
            // Kanat penceleri (kuşlarda yok)
            _m(new THREE.ConeGeometry(.008,.04,3),0xbbaa88,{{p:[-.25,.28,.08],r:[.5,0,.5]}});
            _m(new THREE.ConeGeometry(.008,.04,3),0xbbaa88,{{p:[-.25,.28,-.08],r:[-.5,0,.5]}});
            // Arka bacaklar
            _m(new THREE.CylinderGeometry(.02,.015,.18,4),bc,{{p:[-.02,.22,.04]}});
            _m(new THREE.CylinderGeometry(.02,.015,.18,4),bc,{{p:[-.02,.22,-.04]}});
            // UZUN KEMIKLI KUYRUK — tuylu (kuşlarda yok)
            for(var t=0;t<8;t++){{_m(new THREE.SphereGeometry(.02-t*.001,4,3),bc,{{p:[-.1-t*.06,.32+t*.002,0]}});}}
            for(var tf=0;tf<6;tf++){{_m(new THREE.PlaneGeometry(.06,.015),fc,{{p:[-.2-tf*.04,.32,.005+tf*.003],r:[0,0,.1],op:.6,ds:true}});
            _m(new THREE.PlaneGeometry(.06,.015),fc,{{p:[-.2-tf*.04,.32,-.005-tf*.003],r:[0,0,.1],op:.6,ds:true}});}}
        }}
        else if(T==17){{
            // MOSASAURUS — dev deniz sürüngeni, güçlü ceneler
            var bc=0x445566;
            // Uzun govde — aerodinamik
            _m(new THREE.SphereGeometry(.4,16,14),bc,{{p:[0,0,0],s:[2,.7,.8]}});
            // Kafa — güçlü ceneler
            _m(new THREE.BoxGeometry(.5,.22,.25),bc,{{p:[.9,.08,0]}});
            _m(new THREE.BoxGeometry(.25,.08,.22),bc,{{p:[1.15,0,0]}});
            // Cift sira dışler
            for(var d=0;d<7;d++){{_m(new THREE.ConeGeometry(.012,.06,3),0xeeeedd,{{p:[.75+d*.07,.0,.1],r:[Math.PI,0,0]}});
            _m(new THREE.ConeGeometry(.01,.04,3),0xeeeedd,{{p:[.78+d*.06,.02,.06],r:[Math.PI,0,0]}});}}
            // Gozler
            _mb(new THREE.SphereGeometry(.03,8,8),0xddcc44,{{p:[.85,.15,.12]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0xddcc44,{{p:[.85,.15,-.12]}});
            // 4 yüzgec
            _m(new THREE.PlaneGeometry(.4,.12),0x556677,{{p:[.3,-.05,.35],r:[-.4,.3,0],op:.6,ds:true}});
            _m(new THREE.PlaneGeometry(.4,.12),0x556677,{{p:[.3,-.05,-.35],r:[.4,.3,0],op:.6,ds:true}});
            _m(new THREE.PlaneGeometry(.35,.1),0x556677,{{p:[-.3,-.05,.3],r:[-.4,-.3,0],op:.6,ds:true}});
            _m(new THREE.PlaneGeometry(.35,.1),0x556677,{{p:[-.3,-.05,-.3],r:[.4,-.3,0],op:.6,ds:true}});
            // Güçlu yassı kuyruk
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.15-t*.015,8,6),bc,{{p:[-.6-t*.22,0,0],s:[1,1-t*.05,1+t*.08]}});}}
            _m(new THREE.PlaneGeometry(.25,.2),0x556677,{{p:[-1.9,0,0],op:.5,ds:true}});
            // Su efekti
            for(var w=0;w<6;w++){{_mb(new THREE.SphereGeometry(.05,4,4),0x3366aa,{{p:[(Math.random()-.5)*2.5,(Math.random()-.5)*.6,(Math.random()-.5)*.8],op:.12}});}}
            // Karin
            _m(new THREE.SphereGeometry(.35,10,8),0x667788,{{p:[0,-.1,0],s:[1.8,.4,.65]}});
        }}
        else if(T==18){{
            // DIMETRODON — sirt yelkeni, memeli atasi
            var bc=0x7a6b55;var sc=0xcc8844;
            // Govde — düşük, geniş
            _m(new THREE.SphereGeometry(.4,14,12),bc,{{p:[0,.1,0],s:[1.4,.8,.9]}});
            // SIRT YELKENI — devasa
            for(var s=0;s<14;s++){{var sx=-.5+s*.1,sh=.15+Math.sin(s*.25+.3)*.25;
            _m(new THREE.CylinderGeometry(.008,.008,sh,4),0xaa7744,{{p:[sx,.4+sh/2,0]}});}}
            _m(new THREE.PlaneGeometry(1.2,.65),sc,{{p:[0,.55,0],op:.5,ds:true}});
            // Kafa — güçlü ceneler
            _m(new THREE.BoxGeometry(.35,.2,.2),bc,{{p:[.65,.12,0]}});
            // Heterodon dışler — farkli boyutlar
            _m(new THREE.ConeGeometry(.02,.1,4),0xeeddcc,{{p:[.75,.0,.08],r:[Math.PI,0,0]}});
            _m(new THREE.ConeGeometry(.015,.06,3),0xeeddcc,{{p:[.8,.02,.08],r:[Math.PI,0,0]}});
            _m(new THREE.ConeGeometry(.02,.08,4),0xeeddcc,{{p:[.7,.02,.08],r:[Math.PI,0,0]}});
            // Gozler
            _mb(new THREE.SphereGeometry(.025,6,6),0xddaa22,{{p:[.7,.2,.1]}});
            _mb(new THREE.SphereGeometry(.025,6,6),0xddaa22,{{p:[.7,.2,-.1]}});
            // 4 bacak — yanlara acilan (surugen tarzi)
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[.25,-.1,.35],r:[.8,0,0]}});
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[.25,-.1,-.35],r:[-.8,0,0]}});
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[-.25,-.1,.35],r:[.8,0,0]}});
            _m(new THREE.CylinderGeometry(.06,.05,.35,6),bc,{{p:[-.25,-.1,-.35],r:[-.8,0,0]}});
            // Kuyruk
            for(var t=0;t<6;t++){{_m(new THREE.SphereGeometry(.12-t*.015,7,5),bc,{{p:[-.5-t*.18,.05,0]}});}}
        }}
        else if(T==19){{
            // MEGALOSAURUS — ilk adlandirilan dinozor, teropod
            var bc=0x6b6655;
            // Govde
            _m(new THREE.SphereGeometry(.5,16,14),bc,{{p:[0,.3,0],s:[1.3,.95,.85]}});
            // Boyun
            _m(new THREE.CylinderGeometry(.1,.15,.4,8),bc,{{p:[.5,.55,0],r:[0,0,-.4]}});
            // Kafa — güçlü cene
            _m(new THREE.BoxGeometry(.45,.25,.25),bc,{{p:[.85,.75,0]}});
            _m(new THREE.BoxGeometry(.2,.08,.2),bc,{{p:[1.05,.65,0]}});
            // Disler — tirtikli
            for(var d=0;d<6;d++){{_m(new THREE.ConeGeometry(.012,.07,3),0xeeddcc,{{p:[.68+d*.06,.61,.1],r:[Math.PI,0,0]}});}}
            // Gozler
            _mb(new THREE.SphereGeometry(.03,8,8),0xccaa22,{{p:[.82,.82,.12]}});
            _mb(new THREE.SphereGeometry(.03,8,8),0xccaa22,{{p:[.82,.82,-.12]}});
            // Güçlu arka bacaklar
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.1,.22]}});
            _m(new THREE.CylinderGeometry(.1,.08,.7,8),bc,{{p:[-.1,-.1,-.22]}});
            _m(new THREE.BoxGeometry(.2,.05,.2),bc,{{p:[-.05,-.48,.22]}});
            _m(new THREE.BoxGeometry(.2,.05,.2),bc,{{p:[-.05,-.48,-.22]}});
            // Üç parmakli on kollar
            _m(new THREE.CylinderGeometry(.045,.035,.25,6),bc,{{p:[.35,.2,.18],r:[0,0,.6]}});
            _m(new THREE.CylinderGeometry(.045,.035,.25,6),bc,{{p:[.35,.2,-.18],r:[0,0,.6]}});
            // Kuyruk
            for(var t=0;t<7;t++){{_m(new THREE.SphereGeometry(.14-t*.014,8,6),bc,{{p:[-.5-t*.22,.25,0]}});}}
            // Zemin — tarihi hava
            _m(new THREE.BoxGeometry(3,.03,2),0x554433,{{p:[0,-.52,0],op:.3}});
        }}

        scene.add(mainObj);"""

    if ci == 6:  # Dünya Coğrafyası — 20 premium sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||50,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}

        if(T==0){{
            // VOLKAN — kesit görünüm: magma odasi, baca, krater, lav akisi
            // Ana koni
            _m(new THREE.ConeGeometry(1.2,2.0,20),0x6b5b44,{{p:[0,-.1,0]}});
            // Krater — ustekte cukur
            _m(new THREE.CylinderGeometry(.35,.25,.15,16),0x553322,{{p:[0,.9,0]}});
            // Lav gölü (krater içinde)
            _m(new THREE.CylinderGeometry(.22,.22,.06,14),0xff3300,{{p:[0,.88,0],em:0xff2200,ei:.8}});
            // Magma odasi (alt)
            _m(new THREE.SphereGeometry(.5,14,12),0xff4400,{{p:[0,-1.3,0],em:0xff2200,ei:.6,op:.7}});
            // Baca (iç kanal)
            _m(new THREE.CylinderGeometry(.08,.15,1.5,8),0xcc3300,{{p:[0,-.1,0],op:.5,em:0xff3300,ei:.4}});
            // Lav akintilari (yan)
            for(var l=0;l<4;l++){{var la=l*1.57;
            _m(new THREE.CylinderGeometry(.03,.06,.8,6),0xff5500,{{p:[Math.cos(la)*.5,-.3,Math.sin(la)*.5],r:[Math.cos(la)*.5,0,Math.sin(la)*.5],em:0xff3300,ei:.5,op:.7}});}}
            // Duman/kul parcaciklari
            for(var s=0;s<15;s++){{_mb(new THREE.SphereGeometry(.04+Math.random()*.04,5,4),0x888888,{{p:[(Math.random()-.5)*.5,1.0+Math.random()*.8,(Math.random()-.5)*.5],op:.3}});}}
            // Zemin
            _m(new THREE.BoxGeometry(3.5,.08,3.5),0x4a3b2a,{{p:[0,-1.15,0]}});
            // Yan yamac katmanlari (jeolojik)
            for(var k=0;k<3;k++){{_m(new THREE.TorusGeometry(1.0-k*.15,.04,6,20),0x7a6b5a,{{p:[0,-.5+k*.35,0],r:[1.57,0,0],op:.4}});}}
        }}
        else if(T==1){{
            // DEPREM FAYI — tektonik plakalar, kirik hatti, sismik dalgalar
            // Sol plaka
            _m(new THREE.BoxGeometry(1.6,.4,2.0),0x8b7b55,{{p:[-.9,-.2,0]}});
            // Sag plaka (kayma)
            _m(new THREE.BoxGeometry(1.6,.4,2.0),0x7a6b45,{{p:[.9,-.3,0]}});
            // Fay hatti (kirik cizgi)
            _m(new THREE.BoxGeometry(.06,.5,2.2),0xcc3333,{{p:[0,-.2,0],em:0xcc2222,ei:.3}});
            // Alt katmanlar (magma)
            _m(new THREE.BoxGeometry(3.8,.3,2.2),0xcc6633,{{p:[0,-.65,0],em:0xaa4422,ei:.2}});
            _m(new THREE.BoxGeometry(3.8,.5,2.2),0xff5533,{{p:[0,-1.1,0],em:0xff3322,ei:.3,op:.6}});
            // Kayma oklari
            _m(new THREE.ConeGeometry(.08,.25,6),0xffaa33,{{p:[-.5,.15,0],r:[0,0,1.2]}});
            _m(new THREE.ConeGeometry(.08,.25,6),0xffaa33,{{p:[.5,.05,0],r:[0,0,-1.2]}});
            // Sismik dalgalar (dairesel)
            for(var w=0;w<5;w++){{_m(new THREE.TorusGeometry(.3+w*.25,.015,6,24),0xffcc44,{{p:[0,-.15,0],r:[1.57,0,0],op:.5-w*.08,em:0xffaa22,ei:.2}});}}
            // Kirik parcalari
            for(var f=0;f<6;f++){{_m(new THREE.DodecahedronGeometry(.06+Math.random()*.04),0x998877,{{p:[(Math.random()-.5)*.3,.0+Math.random()*.15,(Math.random()-.5)*1.5]}});}}
            // Yüzey yapilar (hasar)
            _m(new THREE.BoxGeometry(.3,.2,.2),0x887766,{{p:[-.6,.1,.5],r:[0,0,.15]}});
            _m(new THREE.BoxGeometry(.2,.15,.2),0x887766,{{p:[.7,.05,-.4],r:[0,0,-.1]}});
        }}
        else if(T==2){{
            // OKYANUS — derin deniz kesiti: yüzey dalgalari, derinlik katmanlari, sirt
            // Su yüzeyi
            _m(new THREE.BoxGeometry(3,.06,2.5),0x1166bb,{{p:[0,.8,0],op:.5,sh:90}});
            // Dalgalar
            for(var w=0;w<8;w++){{_m(new THREE.TorusGeometry(.15,.02,4,16,3.14),0x2288cc,{{p:[-1.2+w*.35,.83,0],r:[0,1.57,0],op:.4}});}}
            // Derin su katmanlari
            _m(new THREE.BoxGeometry(3,1.2,2.5),0x0044aa,{{p:[0,.1,0],op:.25}});
            _m(new THREE.BoxGeometry(3,.5,2.5),0x002266,{{p:[0,-.65,0],op:.3}});
            // Okyanus tabani
            _m(new THREE.BoxGeometry(3,.1,2.5),0x554433,{{p:[0,-.95,0]}});
            // Okyanus ortasi sirt (dağ silsilesi)
            for(var r=0;r<6;r++){{_m(new THREE.ConeGeometry(.15+Math.random()*.1,.3+Math.random()*.2,6),0x665544,{{p:[-.6+r*.25,-.75,(Math.random()-.5)*.5]}});}}
            // Sirt yariginda magma
            _m(new THREE.CylinderGeometry(.02,.05,.15,6),0xff4400,{{p:[0,-.7,0],em:0xff3300,ei:.6}});
            // Deniz canlilari (siluetler)
            _m(new THREE.SphereGeometry(.08,8,6),0x3388aa,{{p:[.8,.5,.3],s:[2,.6,.6]}});
            _m(new THREE.SphereGeometry(.04,6,4),0x44aacc,{{p:[-.5,.4,-.2],s:[1.5,.5,.5]}});
            // Mercan
            for(var c=0;c<4;c++){{_m(new THREE.ConeGeometry(.05,.15,5),0xcc5566,{{p:[.5+c*.15,-.88,.6]}});}}
        }}
        else if(T==3){{
            // NEHIR DELTASI — dallanma, alivyon, denize dökülme
            // Deniz
            _m(new THREE.BoxGeometry(3,.05,3),0x2277aa,{{p:[0,-.8,0],op:.5,sh:80}});
            // Delta üçgeni (alivyon birikim)
            _m(new THREE.ConeGeometry(1.2,.15,3),0xaa9966,{{p:[0,-.72,0],r:[0,.52,0]}});
            // Ana nehir kanali
            _m(new THREE.CylinderGeometry(.06,.04,1.5,6),0x3388bb,{{p:[0,-.2,-.5],r:[.6,0,0],op:.7}});
            // Dallanma kanallari
            for(var d=0;d<5;d++){{var da=-.4+d*.2,dl=.4+Math.random()*.3;
            _m(new THREE.CylinderGeometry(.03,.02,dl,4),0x3388bb,{{p:[da*1.2,-.72,da*.5],r:[.3+d*.1,d*.3,da],op:.6}});}}
            // Bitki ortüsü (dalta üzerinde)
            for(var v=0;v<12;v++){{_m(new THREE.ConeGeometry(.06,.15,5),0x228833,{{p:[(Math.random()-.5)*1.8,-.62,(Math.random()-.5)*1.5]}});}}
            // Alivyon katmanlari (yan kesit)
            _m(new THREE.BoxGeometry(2,.04,2),0xbb9955,{{p:[0,-.76,0],op:.5}});
            _m(new THREE.BoxGeometry(1.6,.04,1.6),0xccaa66,{{p:[0,-.73,0],op:.4}});
            // Kara
            _m(new THREE.BoxGeometry(1,.15,3),0x558833,{{p:[-1.2,-.72,-0]}});
        }}
        else if(T==4){{
            // COL — kum tepeleri, kumtasi, kaktus, vaha
            // Kum zemini
            _m(new THREE.BoxGeometry(3.5,.1,3),0xdeb887,{{p:[0,-.9,0]}});
            // Büyük kum tepeleri
            for(var d=0;d<5;d++){{_m(new THREE.SphereGeometry(.4+d*.08,14,8,0,6.28,0,1.57),0xd2b48c,{{p:[-1.2+d*.6,-.85,-.5+d*.25]}});}}
            // Barchan (hilal) kum tepesi
            _m(new THREE.SphereGeometry(.6,16,10,0,6.28,0,1.57),0xc4a070,{{p:[.5,-.85,.5]}});
            _m(new THREE.ConeGeometry(.15,.3,4),0xc4a070,{{p:[1.0,-.78,.7],r:[0,.5,-.3]}});
            // Kumtasi katmanlari
            _m(new THREE.BoxGeometry(3,.06,2),0xba9060,{{p:[0,-.95,.8],op:.5}});
            _m(new THREE.BoxGeometry(2.5,.04,1.5),0xa88050,{{p:[0,-1.0,.7],op:.4}});
            // Kaktus
            _m(new THREE.CylinderGeometry(.04,.05,.5,8),0x228833,{{p:[-1.0,-.6,-.8]}});
            _m(new THREE.CylinderGeometry(.025,.03,.2,6),0x228833,{{p:[-.92,-.5,-.8],r:[0,0,.8]}});
            _m(new THREE.CylinderGeometry(.025,.03,.15,6),0x228833,{{p:[-1.08,-.55,-.8],r:[0,0,-.7]}});
            // Vaha (küçük su birikintisi + palmiye)
            _m(new THREE.CylinderGeometry(.2,.2,.03,12),0x3388aa,{{p:[1.0,-.84,-.6],op:.6}});
            _m(new THREE.CylinderGeometry(.03,.035,.5,6),0x664422,{{p:[1.15,-.55,-.6]}});
            _m(new THREE.SphereGeometry(.15,8,6,0,6.28,0,1.8),0x228833,{{p:[1.15,-.28,-.6]}});
        }}
        else if(T==5){{
            // BUZUL — buz kütlesi, catlaklar, morenleri, erime suyu
            // Ana buzul kütlesi
            _m(new THREE.BoxGeometry(2.5,.8,2),0xddeeFF,{{p:[0,-.3,0],op:.65,sh:95}});
            // Ust yüzey düzensizlikleri
            for(var b=0;b<6;b++){{_m(new THREE.DodecahedronGeometry(.15+Math.random()*.1),0xccddff,{{p:[(Math.random()-.5)*2,.15,(Math.random()-.5)*1.5],op:.5,sh:90}});}}
            // Catlaklar (mavi)
            for(var c=0;c<5;c++){{_m(new THREE.BoxGeometry(.02,.82,Math.random()*.5+.3),0x4488cc,{{p:[-.8+c*.4,-.3,0],op:.4}});}}
            // Buzul dili (onen kısım)
            _m(new THREE.SphereGeometry(.5,12,8,0,6.28,0,1.57),0xccddff,{{p:[1.2,-.7,0],r:[0,0,.3],op:.5,sh:90}});
            // Morenler (kayalar)
            for(var m=0;m<8;m++){{_m(new THREE.DodecahedronGeometry(.06+Math.random()*.05),0x887766,{{p:[1.0+Math.random()*.5,-.65,(Math.random()-.5)*1.5]}});}}
            // Erime suyu kanali
            _m(new THREE.CylinderGeometry(.03,.05,.8,5),0x3388cc,{{p:[1.5,-.75,0],r:[0,0,.3],op:.6}});
            // Zemin
            _m(new THREE.BoxGeometry(3.5,.08,2.5),0x667766,{{p:[0,-.75,0]}});
        }}
        else if(T==6){{
            // OBRUK — dairesel çokme, katmanlar, yeraltı suyu
            // Yüzey zemini
            _m(new THREE.BoxGeometry(3,.15,3),0x558833,{{p:[0,.3,0]}});
            // Obruk deliği (dairesel)
            _m(new THREE.CylinderGeometry(.8,.6,1.2,20),0x443322,{{p:[0,-.35,0]}});
            // Katmanli duvarlar
            _m(new THREE.TorusGeometry(.75,.04,6,20),0xaa9966,{{p:[0,.1,0],r:[1.57,0,0]}});
            _m(new THREE.TorusGeometry(.7,.03,6,18),0x887755,{{p:[0,-.1,0],r:[1.57,0,0]}});
            _m(new THREE.TorusGeometry(.65,.04,6,16),0x998866,{{p:[0,-.3,0],r:[1.57,0,0]}});
            // Dipteki su
            _m(new THREE.CylinderGeometry(.55,.55,.06,16),0x2266aa,{{p:[0,-.9,0],op:.6,sh:90}});
            // Kireçtasi eriyik katman
            _m(new THREE.BoxGeometry(3,.2,3),0xccbb99,{{p:[0,-.6,0],op:.3}});
            // Çokmus kaya parcalari
            for(var r=0;r<5;r++){{_m(new THREE.DodecahedronGeometry(.08+Math.random()*.06),0x887766,{{p:[(Math.random()-.5)*.8,-.7,(Math.random()-.5)*.8]}});}}
            // Bitki ortusu (kenar)
            for(var v=0;v<8;v++){{var va=v*.79;_m(new THREE.ConeGeometry(.06,.15,5),0x228833,{{p:[Math.cos(va)*.9,.4,Math.sin(va)*.9]}});}}
        }}
        else if(T==7){{
            // KANYON — derin yarma vadi, katmanli kayalar, nehir
            // Sol duvar
            _m(new THREE.BoxGeometry(.6,2.0,2.5),0x8b6b44,{{p:[-.8,-.1,0]}});
            // Sag duvar
            _m(new THREE.BoxGeometry(.6,2.0,2.5),0x7b5b34,{{p:[.8,-.1,0]}});
            // Katman cizgileri (sol)
            for(var k=0;k<6;k++){{_m(new THREE.BoxGeometry(.62,.03,2.5),0xaa8855+k*0x111100,{{p:[-.8,-.8+k*.3,0]}});}}
            // Katman cizgileri (sag)
            for(var k=0;k<6;k++){{_m(new THREE.BoxGeometry(.62,.03,2.5),0x997744+k*0x111100,{{p:[.8,-.8+k*.3,0]}});}}
            // Kanyon tabani
            _m(new THREE.BoxGeometry(.9,.08,2.5),0x554433,{{p:[0,-1.1,0]}});
            // Nehir (tabanda)
            _m(new THREE.BoxGeometry(.3,.04,2.5),0x2277aa,{{p:[0,-1.05,0],op:.6,sh:80}});
            // Ust kenar kayalari
            for(var r=0;r<6;r++){{_m(new THREE.DodecahedronGeometry(.1+Math.random()*.06),0x8b7b55,{{p:[(r%2?-1.1:1.1),.9,(Math.random()-.5)*2]}});}}
            // Tabanda cakil taslar
            for(var c=0;c<10;c++){{_m(new THREE.SphereGeometry(.03+Math.random()*.03,5,4),0x998877,{{p:[(Math.random()-.5)*.6,-1.05,(Math.random()-.5)*2]}});}}
        }}
        else if(T==8){{
            // ADA — okyanusta ada, plaj, bitki ortusu, resif
            // Okyanus
            _m(new THREE.BoxGeometry(3.5,.05,3.5),0x1166aa,{{p:[0,-.6,0],op:.5,sh:80}});
            // Ana ada (tabani)
            _m(new THREE.ConeGeometry(1.0,.8,12),0x8b7b55,{{p:[0,-.25,0]}});
            // Ust toprak
            _m(new THREE.SphereGeometry(.6,14,10,0,6.28,0,1.57),0x558833,{{p:[0,-.2,0]}});
            // Plaj (kum seridi)
            _m(new THREE.TorusGeometry(.7,.08,4,20),0xddcc99,{{p:[0,-.2,0],r:[1.57,0,0]}});
            // Palmiyeler
            for(var p=0;p<3;p++){{var pa=p*2.1;
            _m(new THREE.CylinderGeometry(.03,.04,.4,6),0x664422,{{p:[Math.cos(pa)*.25,.05,Math.sin(pa)*.25],r:[Math.cos(pa)*.2,0,Math.sin(pa)*.2]}});
            _m(new THREE.SphereGeometry(.1,6,4,0,6.28,0,1.5),0x228833,{{p:[Math.cos(pa)*.3,.3,Math.sin(pa)*.3]}});}}
            // Mercan resifi
            for(var c=0;c<8;c++){{var ca=c*.79;_m(new THREE.ConeGeometry(.05,.12,5),0xcc5566,{{p:[Math.cos(ca)*1.0,-.58,Math.sin(ca)*1.0]}});}}
            // Dalgalar
            for(var w=0;w<6;w++){{_m(new THREE.TorusGeometry(.8+w*.15,.015,4,20),0x3399cc,{{p:[0,-.58,0],r:[1.57,0,0],op:.3-w*.04}});}}
        }}
        else if(T==9){{
            // DAG — zirveli dag, kar, ağaç hatti, yamaç
            // Ana dağ govdesi
            _m(new THREE.ConeGeometry(1.5,2.5,12),0x7b6b4a,{{p:[0,-.05,0]}});
            // Kar siperi (zirve)
            _m(new THREE.ConeGeometry(.4,.5,10),0xeeeeff,{{p:[0,1.0,0],sh:90}});
            // Ikinci dag
            _m(new THREE.ConeGeometry(1.0,1.8,10),0x6b5b3a,{{p:[-1.2,-.45,.3]}});
            _m(new THREE.ConeGeometry(.25,.3,8),0xeeeeff,{{p:[-1.2,.4,.3],sh:90}});
            // Ağaç hatti (orta yükseklik)
            for(var t=0;t<10;t++){{var ta=t*.63;
            _m(new THREE.ConeGeometry(.08,.2,5),0x226622,{{p:[Math.cos(ta)*.8,-.5,Math.sin(ta)*.8]}});
            _m(new THREE.CylinderGeometry(.015,.02,.08,4),0x553311,{{p:[Math.cos(ta)*.8,-.62,Math.sin(ta)*.8]}});}}
            // Kayalik yamac detaylari
            for(var r=0;r<6;r++){{_m(new THREE.DodecahedronGeometry(.08),0x887766,{{p:[(Math.random()-.5)*1.5,-.7+Math.random()*.5,(Math.random()-.5)*1.5]}});}}
            // Zemin
            _m(new THREE.BoxGeometry(3.5,.08,3),0x557733,{{p:[0,-1.3,0]}});
        }}
        else if(T==10){{
            // PLATO — duz zirveli yukselti, kenar üçurumlari
            // Ana plato yüzeyi
            _m(new THREE.BoxGeometry(2.5,.15,2),0x889966,{{p:[0,.3,0]}});
            // Dikine kenar üçurumlari
            _m(new THREE.BoxGeometry(2.5,.8,.08),0x8b7b55,{{p:[0,-.05,1.0]}});
            _m(new THREE.BoxGeometry(2.5,.8,.08),0x7b6b45,{{p:[0,-.05,-1.0]}});
            _m(new THREE.BoxGeometry(.08,.8,2),0x8b7b55,{{p:[1.25,-.05,0]}});
            _m(new THREE.BoxGeometry(.08,.8,2),0x7b6b45,{{p:[-1.25,-.05,0]}});
            // Katman cizgileri
            for(var k=0;k<4;k++){{var ky=-.3+k*.2;
            _m(new THREE.BoxGeometry(2.5,.02,2),0x998866,{{p:[0,ky,0],op:.5}});}}
            // Ust yüzey bitki ortusu
            for(var v=0;v<8;v++){{_m(new THREE.ConeGeometry(.06,.12,4),0x338833,{{p:[(Math.random()-.5)*2,.4,(Math.random()-.5)*1.5]}});}}
            // Etraf ova
            _m(new THREE.BoxGeometry(3.5,.05,3),0x668844,{{p:[0,-.5,0]}});
            // Nehir (kenardan dokulen)
            _m(new THREE.CylinderGeometry(.03,.02,.8,5),0x3388aa,{{p:[1.25,-.1,.5],r:[0,0,.1],op:.6}});
        }}
        else if(T==11){{
            // VADI — iki dağ arasi cukur, nehir, bitki ortusu
            // Sol dağ yamaci
            _m(new THREE.ConeGeometry(1.0,2.0,8),0x7b6b4a,{{p:[-1.2,.0,.0]}});
            // Sag dağ yamaci
            _m(new THREE.ConeGeometry(.9,1.8,8),0x6b5b3a,{{p:[1.2,-.1,.0]}});
            // Vadi tabani
            _m(new THREE.BoxGeometry(1.2,.1,2.5),0x558833,{{p:[0,-.9,0]}});
            // Nehir
            _m(new THREE.CylinderGeometry(.05,.05,2.5,6),0x2277aa,{{p:[0,-.85,0],r:[1.57,0,0],op:.6}});
            // Ağaçlar (tabanda)
            for(var t=0;t<8;t++){{_m(new THREE.ConeGeometry(.08,.2,5),0x228822,{{p:[(Math.random()-.5)*.8,-.7,(Math.random()-.5)*2]}});
            _m(new THREE.CylinderGeometry(.015,.02,.1,4),0x553311,{{p:[(Math.random()-.5)*.8,-.82,(Math.random()-.5)*2]}});}}
            // Yamac detaylari
            for(var r=0;r<5;r++){{_m(new THREE.DodecahedronGeometry(.06),0x887766,{{p:[(r%2?-.6:.6),-.5+Math.random()*.3,(Math.random()-.5)*2]}});}}
            // Zemin
            _m(new THREE.BoxGeometry(3.5,.05,3),0x667744,{{p:[0,-1.0,0]}});
        }}
        else if(T==12){{
            // MAGARA — giriş, stalaktit, stalagmit, yeraltı gölü
            // Magara dışi kayalik
            _m(new THREE.SphereGeometry(1.2,14,12),0x7b6b4a,{{p:[0,.2,0],s:[1.5,1,1]}});
            // Magara girişi (köyü delik)
            _m(new THREE.CylinderGeometry(.45,.4,.2,12),0x221100,{{p:[0,-.1,1.2],r:[1.57,0,0]}});
            // Ic mekan (kesit)
            _m(new THREE.SphereGeometry(.8,12,10),0x332211,{{p:[0,-.2,0],s:[1.5,.8,1],op:.5}});
            // Stalaktitler (tavandan sarkan)
            for(var s=0;s<8;s++){{_m(new THREE.ConeGeometry(.03,.2+Math.random()*.15,5),0xccbb99,{{p:[(Math.random()-.5)*1.2,.4,(Math.random()-.5)*.8],r:[Math.PI,0,0]}});}}
            // Stalagmitler (yerden cikan)
            for(var s=0;s<6;s++){{_m(new THREE.ConeGeometry(.03,.15+Math.random()*.1,5),0xbbaa88,{{p:[(Math.random()-.5)*1,-.55,(Math.random()-.5)*.6]}});}}
            // Yeraltı gölü
            _m(new THREE.CylinderGeometry(.35,.35,.03,12),0x1155aa,{{p:[.3,-.6,.0],op:.5,sh:80}});
            // Damla suyu parlama
            _mb(new THREE.SphereGeometry(.02,4,4),0x88aadd,{{p:[-.2,.1,.2],op:.5}});
        }}
        else if(T==13){{
            // ATOL — halka resif, lagün, acik okyanus
            // Okyanus
            _m(new THREE.BoxGeometry(3.5,.05,3.5),0x1155aa,{{p:[0,-.5,0],op:.5,sh:80}});
            // Halka resif
            _m(new THREE.TorusGeometry(.9,.12,8,24),0xddcc88,{{p:[0,-.42,0],r:[1.57,0,0]}});
            // Lagün (iç su — acik mavi)
            _m(new THREE.CylinderGeometry(.75,.75,.04,20),0x33aadd,{{p:[0,-.44,0],op:.6,sh:90}});
            // Mercan resifi detaylari
            for(var c=0;c<12;c++){{var ca=c*.524;
            _m(new THREE.ConeGeometry(.04,.1,4),0xcc6677,{{p:[Math.cos(ca)*.9,-.35,Math.sin(ca)*.9]}});}}
            // Küçük adaciklar (motu)
            for(var m=0;m<3;m++){{var ma=m*2.1;
            _m(new THREE.SphereGeometry(.08,6,4,0,6.28,0,1.57),0x558833,{{p:[Math.cos(ma)*.9,-.38,Math.sin(ma)*.9]}});}}
            // Palmiye
            _m(new THREE.CylinderGeometry(.015,.02,.15,4),0x664422,{{p:[.9,-.28,0]}});
            _m(new THREE.SphereGeometry(.05,5,3,0,6.28,0,1.5),0x228833,{{p:[.9,-.2,0]}});
        }}
        else if(T==14){{
            // SELALE — yükseklik farki, su dokulen kaya, havuz
            // Kaya duvar (üçurum)
            _m(new THREE.BoxGeometry(1.2,1.8,.8),0x7b6b4a,{{p:[0,.0,0]}});
            // Ust yüzey
            _m(new THREE.BoxGeometry(1.5,.1,1),0x558833,{{p:[0,.9,0]}});
            // Su kaynagi (ust nehir)
            _m(new THREE.BoxGeometry(.3,.04,.5),0x2277aa,{{p:[0,.88,-.4],op:.6}});
            // SELALE (dusen su)
            _m(new THREE.BoxGeometry(.3,1.6,.08),0x66bbee,{{p:[0,.05,.42],op:.45,sh:90}});
            // Su damlaciklari (sis)
            for(var d=0;d<12;d++){{_mb(new THREE.SphereGeometry(.02+Math.random()*.02,4,3),0xaaddff,{{p:[(Math.random()-.5)*.5,-.5+Math.random()*.5,.5+Math.random()*.2],op:.3}});}}
            // Alt havuz
            _m(new THREE.CylinderGeometry(.5,.6,.08,14),0x2266aa,{{p:[0,-.85,.3],op:.6,sh:80}});
            // Çıkış akintisi
            _m(new THREE.CylinderGeometry(.04,.03,.6,5),0x3388aa,{{p:[.4,-.85,.5],r:[0,.5,1.57],op:.5}});
            // Kenar kayalar
            for(var r=0;r<4;r++){{_m(new THREE.DodecahedronGeometry(.1),0x887766,{{p:[(r%2?-.7:.7),-.7,.4]}});}}
            // Bitki (kenar)
            for(var v=0;v<5;v++){{_m(new THREE.ConeGeometry(.06,.15,4),0x228833,{{p:[(Math.random()-.5)*1.2,.8,(Math.random()-.5)*.6]}});}}
        }}
        else if(T==15){{
            // GOL — çevreli su kütlesi, kıyılar, adacik
            // Gol suyu
            _m(new THREE.CylinderGeometry(1.1,1.1,.06,20),0x2277aa,{{p:[0,-.3,0],op:.55,sh:85}});
            // Kiyi hatti
            _m(new THREE.TorusGeometry(1.15,.06,4,24),0xddcc88,{{p:[0,-.3,0],r:[1.57,0,0]}});
            // Çevre arazi
            _m(new THREE.BoxGeometry(3.5,.08,3.5),0x558833,{{p:[0,-.38,0]}});
            // Küçük adacik
            _m(new THREE.SphereGeometry(.12,8,6,0,6.28,0,1.57),0x668844,{{p:[.3,-.26,-.2]}});
            // Ağaçlar (kiyi)
            for(var t=0;t<8;t++){{var ta=t*.79;var tr=1.3;
            _m(new THREE.ConeGeometry(.06,.15,5),0x227722,{{p:[Math.cos(ta)*tr,-.2,Math.sin(ta)*tr]}});
            _m(new THREE.CylinderGeometry(.012,.015,.08,4),0x553311,{{p:[Math.cos(ta)*tr,-.3,Math.sin(ta)*tr]}});}}
            // Dağlar (arka plan)
            _m(new THREE.ConeGeometry(.5,.8,6),0x6b5b44,{{p:[-1.2,.0,-1.2]}});
            _m(new THREE.ConeGeometry(.4,.6,6),0x5b4b34,{{p:[1.0,.0,-1.0]}});
            // Yansima efekti
            _m(new THREE.ConeGeometry(.3,.4,6),0x3377aa,{{p:[-1.0,-.32,-1.0],r:[Math.PI,0,0],op:.2}});
        }}
        else if(T==16){{
            // BOGAZ — iki kara arasi dar su geçidi
            // Sol kara
            _m(new THREE.BoxGeometry(1.2,.5,3),0x558833,{{p:[-1.1,-.3,0]}});
            _m(new THREE.ConeGeometry(.4,.5,6),0x6b5b44,{{p:[-1.0,.15,.8]}});
            _m(new THREE.ConeGeometry(.3,.4,5),0x5b4b34,{{p:[-1.2,.1,-.5]}});
            // Sag kara
            _m(new THREE.BoxGeometry(1.2,.5,3),0x558833,{{p:[1.1,-.3,0]}});
            _m(new THREE.ConeGeometry(.35,.45,6),0x6b5b44,{{p:[1.0,.12,-.6]}});
            // Su yolu (boğaz)
            _m(new THREE.BoxGeometry(.8,.04,3),0x1166aa,{{p:[0,-.3,0],op:.6,sh:80}});
            // Su akintisi oklari
            for(var a=0;a<4;a++){{_m(new THREE.ConeGeometry(.04,.12,4),0x3399cc,{{p:[0,-.27,-1+a*.7],r:[1.2,0,0],op:.5}});}}
            // Kiyi kayaliklari
            for(var r=0;r<6;r++){{_m(new THREE.DodecahedronGeometry(.06),0x887766,{{p:[(r%2?-.45:.45),-.25,(Math.random()-.5)*2.5]}});}}
            // Dalgalar
            for(var w=0;w<5;w++){{_m(new THREE.TorusGeometry(.15,.01,3,12,3.14),0x3388cc,{{p:[0,-.28,-1+w*.5],r:[0,1.57,0],op:.3}});}}
        }}
        else if(T==17){{
            // KORFEZ — kara içine girinti yapan deniz
            // Acik deniz
            _m(new THREE.BoxGeometry(3.5,.05,3.5),0x1166aa,{{p:[0,-.5,0],op:.5}});
            // Korfez suyu (daha acik)
            _m(new THREE.SphereGeometry(.9,14,10,0,3.14,0,1.57),0x2288bb,{{p:[0,-.47,-.5],r:[0,0,0],op:.5,sh:80}});
            // Çevreleyen kara (U şekli)
            _m(new THREE.BoxGeometry(3.5,.15,1.5),0x558833,{{p:[0,-.42,-1.2]}});
            _m(new THREE.BoxGeometry(.8,.15,2),0x558833,{{p:[-1.4,-.42,-.3]}});
            _m(new THREE.BoxGeometry(.8,.15,2),0x558833,{{p:[1.4,-.42,-.3]}});
            // Tepeler
            _m(new THREE.ConeGeometry(.3,.4,6),0x6b5b44,{{p:[-1.2,-.2,-1.0]}});
            _m(new THREE.ConeGeometry(.25,.35,5),0x5b4b34,{{p:[1.1,-.22,-.8]}});
            // Liman (küçük)
            _m(new THREE.BoxGeometry(.2,.05,.1),0x887766,{{p:[0,-.42,-.9]}});
            // Tekneler
            _m(new THREE.BoxGeometry(.06,.03,.1),0xffffff,{{p:[.2,-.42,-.5]}});
            _m(new THREE.BoxGeometry(.05,.025,.08),0xdddddd,{{p:[-.3,-.42,-.3]}});
        }}
        else if(T==18){{
            // YARIMADA — üç tarafı su ile cevrili kara
            // Deniz
            _m(new THREE.BoxGeometry(3.5,.05,3.5),0x1166aa,{{p:[0,-.5,0],op:.5,sh:80}});
            // Ana kara (baglanti)
            _m(new THREE.BoxGeometry(3.5,.15,1),0x558833,{{p:[0,-.42,-1.3]}});
            // Yarimada cikintisi
            _m(new THREE.CylinderGeometry(.6,.5,.15,12,1,false,0,3.14),0x668844,{{p:[0,-.42,0],r:[0,0,0]}});
            _m(new THREE.BoxGeometry(1.2,.15,1.2),0x668844,{{p:[0,-.42,-.6]}});
            // Kiyi hatti
            _m(new THREE.TorusGeometry(.6,.03,4,16,3.14),0xddcc88,{{p:[0,-.42,0]}});
            // Tepeler
            _m(new THREE.ConeGeometry(.2,.3,6),0x6b5b44,{{p:[-.2,-.22,-.5]}});
            _m(new THREE.ConeGeometry(.15,.25,5),0x5b4b34,{{p:[.3,-.25,-.3]}});
            // Ağaçlar
            for(var t=0;t<6;t++){{_m(new THREE.ConeGeometry(.05,.12,4),0x227722,{{p:[(Math.random()-.5)*.8,-.3,(Math.random()-.5)*.8-.3]}});}}
            // Dalgalar
            for(var w=0;w<4;w++){{var wa=w*.8;_m(new THREE.TorusGeometry(.7+w*.1,.01,3,14,3.14),0x3399cc,{{p:[0,-.48,0],r:[1.57,0,wa*.2],op:.25}});}}
        }}
        else if(T==19){{
            // OVA — geniş duz arazi, tarım, nehir
            // Geniş duz zemin
            _m(new THREE.BoxGeometry(3.5,.08,3.5),0x668833,{{p:[0,-.3,0]}});
            // Tarım tarlalari (kareli desen)
            for(var f=0;f<6;f++){{for(var g=0;g<6;g++){{var fc2=[0x558822,0x77aa33,0x669922,0x88bb44][(f+g)%4];
            _m(new THREE.BoxGeometry(.5,.02,.5),fc2,{{p:[-1.3+f*.5,-.25,-1.3+g*.5]}});}}}}
            // Nehir (kivrilarak geciyor)
            for(var r=0;r<8;r++){{_m(new THREE.CylinderGeometry(.04,.04,.5,5),0x2277aa,{{p:[-.8+r*.15,-.26,-1.5+r*.4],r:[.6+r*.08,r*.2,0],op:.6}});}}
            // Uzak dağlar (arka plan)
            _m(new THREE.ConeGeometry(.6,.6,6),0x7b6b4a,{{p:[-1.5,.0,1.5],op:.4}});
            _m(new THREE.ConeGeometry(.5,.5,5),0x6b5b3a,{{p:[1.2,.0,1.3],op:.4}});
            _m(new THREE.ConeGeometry(.7,.7,7),0x5b4b2a,{{p:[0,.05,1.5],op:.35}});
            // Yol
            _m(new THREE.BoxGeometry(.1,.01,3.5),0xaa9977,{{p:[.8,-.24,0]}});
            // Ev (küçük)
            _m(new THREE.BoxGeometry(.15,.1,.12),0xccbbaa,{{p:[.5,-.2,.3]}});
            _m(new THREE.ConeGeometry(.1,.08,4),0xaa4422,{{p:[.5,-.12,.3],r:[0,.79,0]}});
        }}

        scene.add(mainObj);"""

    if ci == 7:  # Tarihi Yapilar — 20 premium sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||50,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}

        if(T==0){{
            // PIRAMIT — Mısır piramidi, basamakli iç yapi, giriş, sfenks
            var sc=0xdaa520;
            // Ana piramit
            _m(new THREE.ConeGeometry(1.5,2.2,4),sc,{{p:[0,.3,0],sh:40,r:[0,.79,0]}});
            // Kumtasi katmanlari
            for(var k=0;k<8;k++){{_m(new THREE.BoxGeometry(2.8-k*.3,.03,2.8-k*.3),0xc4a035,{{p:[0,-.65+k*.28,0],r:[0,.79,0],op:.5}});}}
            // Giris
            _m(new THREE.BoxGeometry(.25,.35,.1),0x553311,{{p:[0,-.35,.78]}});
            // Piramit tepesi (altın kaplama)
            _m(new THREE.ConeGeometry(.15,.2,4),0xffd700,{{p:[0,1.35,0],sh:90,r:[0,.79,0]}});
            // Zemin (col)
            _m(new THREE.BoxGeometry(4,.06,4),0xdeb887,{{p:[0,-.8,0]}});
            // Sfenks (küçük)
            _m(new THREE.BoxGeometry(.35,.2,.6),sc,{{p:[1.2,-.65,.8]}});
            _m(new THREE.SphereGeometry(.12,8,6),sc,{{p:[1.2,-.5,.8],s:[1,.8,1]}});
            // Ikinci piramit (arka)
            _m(new THREE.ConeGeometry(.8,1.3,4),0xc4a035,{{p:[-1.3,.0,-1],r:[0,.79,0],op:.6}});
        }}
        else if(T==1){{
            // KOLEZYUM — Roma amfi tiyatrosu, kemerler, arena
            var sc=0xc4a87c;
            // Dis duvar (elips)
            for(var a=0;a<28;a++){{var an=a*6.28/28;
            _m(new THREE.BoxGeometry(.12,1.1,.12),sc,{{p:[Math.cos(an)*1.5,.1,Math.sin(an)*1.5]}});}}
            // Ust kenar
            _m(new THREE.TorusGeometry(1.5,.06,6,28),sc,{{p:[0,.65,0],r:[1.57,0,0]}});
            // Orta kenar
            _m(new THREE.TorusGeometry(1.5,.04,4,28),0xb09870,{{p:[0,.2,0],r:[1.57,0,0]}});
            // Taban
            _m(new THREE.CylinderGeometry(1.6,1.6,.08,28),sc,{{p:[0,-.45,0]}});
            // Arena zemini
            _m(new THREE.CylinderGeometry(1.0,1.0,.04,20),0xddcc99,{{p:[0,-.42,0]}});
            // Ic tribun basamaklari
            for(var s=0;s<4;s++){{_m(new THREE.TorusGeometry(1.0+s*.12,.04,4,20),0xb89878,{{p:[0,-.35+s*.15,0],r:[1.57,0,0]}});}}
            // Kemerler (giriş)
            for(var k=0;k<6;k++){{var ka=k*1.05;_m(new THREE.TorusGeometry(.08,.02,6,8,3.14),sc,{{p:[Math.cos(ka)*1.5,-.15,Math.sin(ka)*1.5],r:[0,ka+1.57,0]}});}}
            // Yikik bolum (gerçekci)
            _m(new THREE.BoxGeometry(.3,.6,.12),sc,{{p:[1.2,.4,.8],r:[0,0,.15],op:.6}});
        }}
        else if(T==2){{
            // KALE — surlar, kuleler, hendek, iç avlu
            var sc=0x8a8070;
            // Dis surlar
            _m(new THREE.BoxGeometry(2.8,.9,.12),sc,{{p:[0,.0,1.2]}});
            _m(new THREE.BoxGeometry(2.8,.9,.12),sc,{{p:[0,.0,-1.2]}});
            _m(new THREE.BoxGeometry(.12,.9,2.4),sc,{{p:[1.4,.0,0]}});
            _m(new THREE.BoxGeometry(.12,.9,2.4),sc,{{p:[-1.4,.0,0]}});
            // Mazgallar (sur ustu)
            for(var m=0;m<12;m++){{_m(new THREE.BoxGeometry(.15,.12,.14),sc,{{p:[-1.2+m*.22,.5,1.2]}});}}
            // 4 kose kulesi
            for(var k=0;k<4;k++){{var kx=k<2?-1.4:1.4,kz=k%2?1.2:-1.2;
            _m(new THREE.CylinderGeometry(.2,.22,.8,10),sc,{{p:[kx,.0,kz]}});
            _m(new THREE.ConeGeometry(.22,.3,10),0x884433,{{p:[kx,.55,kz]}});}}
            // Ana kapi
            _m(new THREE.BoxGeometry(.5,.55,.14),0x553322,{{p:[0,-.2,1.22]}});
            _m(new THREE.TorusGeometry(.22,.02,6,8,3.14),sc,{{p:[0,.05,1.22]}});
            // Ic bina (kale)
            _m(new THREE.BoxGeometry(.8,.7,.6),sc,{{p:[0,.0,0]}});
            _m(new THREE.ConeGeometry(.5,.4,4),0x884433,{{p:[0,.55,0],r:[0,.79,0]}});
            // Hendek
            _m(new THREE.TorusGeometry(1.8,.12,4,20),0x336699,{{p:[0,-.55,0],r:[1.57,0,0],op:.4}});
        }}
        else if(T==3){{
            // AMFI TIYATRO — yarim daire tribun, sahne, orkestra
            var sc=0xc4a87c;
            // Yarim daire tribun basamaklari
            for(var s=0;s<6;s++){{_m(new THREE.CylinderGeometry(.6+s*.2,.6+s*.2,.12,20,1,false,0,3.14),sc,{{p:[0,-.3+s*.15,0],r:[0,0,0]}});}}
            // Sahne platformu
            _m(new THREE.BoxGeometry(1.6,.08,.6),0xaa9070,{{p:[0,-.42,-.5]}});
            // Sahne arka duvari (skene)
            _m(new THREE.BoxGeometry(1.8,.8,.08),sc,{{p:[0,.0,-.8]}});
            // Sutunlar (skene onunde)
            for(var c=0;c<5;c++){{_m(new THREE.CylinderGeometry(.04,.05,.7,8),sc,{{p:[-.6+c*.3,-.05,-.75]}});}}
            // Orkestra alani (yarim daire)
            _m(new THREE.CylinderGeometry(.5,.5,.04,16,1,false,0,3.14),0xddcc99,{{p:[0,-.44,0]}});
            // Giriş yolları
            _m(new THREE.BoxGeometry(.15,.1,1),0xaa9070,{{p:[-.8,-.44,.2],r:[0,.3,0]}});
            _m(new THREE.BoxGeometry(.15,.1,1),0xaa9070,{{p:[.8,-.44,.2],r:[0,-.3,0]}});
        }}
        else if(T==4){{
            // AKROPOL — yüksek tepe, tapinak, sütunlar, Parthenon
            var sc=0xddddcc;
            // Tepe
            _m(new THREE.CylinderGeometry(1.2,1.5,.6,12),0x8a7a5a,{{p:[0,-.5,0]}});
            // Platform
            _m(new THREE.BoxGeometry(2.2,.12,1.4),sc,{{p:[0,-.15,0]}});
            // Parthenon sütunlari
            for(var c=0;c<8;c++){{_m(new THREE.CylinderGeometry(.04,.05,.7,8),sc,{{p:[-.7+c*.2,.2,-.5]}});
            _m(new THREE.CylinderGeometry(.04,.05,.7,8),sc,{{p:[-.7+c*.2,.2,.5]}});}}
            // Yan sütunlar
            for(var s=0;s<4;s++){{_m(new THREE.CylinderGeometry(.04,.05,.7,8),sc,{{p:[-.7,.2,-.3+s*.25]}});
            _m(new THREE.CylinderGeometry(.04,.05,.7,8),sc,{{p:[.7,.2,-.3+s*.25]}});}}
            // Cati (üçgen alinlik)
            _m(new THREE.BoxGeometry(1.6,.06,1.1),sc,{{p:[0,.58,0]}});
            _m(new THREE.ConeGeometry(.8,.25,3),sc,{{p:[0,.72,0],r:[0,1.57,1.57],s:[1,1,.4]}});
            // Basamaklar
            for(var b=0;b<3;b++){{_m(new THREE.BoxGeometry(2.4-b*.15,.04,1.6-b*.1),sc,{{p:[0,-.2-b*.05,0]}});}}
        }}
        else if(T==5){{
            // KOPRU — kemerli tas köprü, nehir, korkuluk
            var sc=0x998877;
            // Köprü tabliyesi
            _m(new THREE.BoxGeometry(3,.1,.6),sc,{{p:[0,.3,0]}});
            // Kemerler
            for(var k=0;k<3;k++){{_m(new THREE.TorusGeometry(.35,.06,8,12,3.14),sc,{{p:[-1+k*1,-.1,0],r:[0,1.57,0]}});}}
            // Ayaklar
            for(var a=0;a<4;a++){{_m(new THREE.BoxGeometry(.15,.7,.5),sc,{{p:[-1.3+a*.87,-.1,0]}});}}
            // Korkuluklar
            for(var r=0;r<12;r++){{_m(new THREE.CylinderGeometry(.015,.015,.2,5),sc,{{p:[-1.2+r*.22,.45,.28]}});
            _m(new THREE.CylinderGeometry(.015,.015,.2,5),sc,{{p:[-1.2+r*.22,.45,-.28]}});}}
            _m(new THREE.BoxGeometry(2.6,.02,.03),sc,{{p:[0,.55,.28]}});
            _m(new THREE.BoxGeometry(2.6,.02,.03),sc,{{p:[0,.55,-.28]}});
            // Nehir
            _m(new THREE.BoxGeometry(3.5,.04,2),0x2277aa,{{p:[0,-.55,0],op:.5}});
            // Kiyi
            _m(new THREE.BoxGeometry(3.5,.08,.5),0x667744,{{p:[0,-.5,1]}});
            _m(new THREE.BoxGeometry(3.5,.08,.5),0x667744,{{p:[0,-.5,-1]}});
        }}
        else if(T==6){{
            // SAAT KULESI — Galata/Big Ben tarzi
            var sc=0xb09878;
            // Govde
            _m(new THREE.BoxGeometry(.6,2.2,.6),sc,{{p:[0,.3,0]}});
            // Ust bolum (daha geniş)
            _m(new THREE.BoxGeometry(.7,.4,.7),sc,{{p:[0,1.45,0]}});
            // Saat kadrani (4 yüz)
            for(var f=0;f<4;f++){{var fx=[0,0,.38,-.38][f],fz=[.38,-.38,0,0][f],ry=[0,3.14,1.57,-1.57][f];
            _m(new THREE.CylinderGeometry(.2,.2,.02,16),0xeeeedd,{{p:[fx,1.45,fz],r:[0,ry,1.57],sh:80}});
            // Akrep+yelkovan
            _m(new THREE.BoxGeometry(.01,.15,.01),0x222222,{{p:[fx,1.48,fz]}});
            _m(new THREE.BoxGeometry(.01,.1,.01),0x222222,{{p:[fx+.02,1.45,fz],r:[0,0,.8]}});}}
            // Sivri cati
            _m(new THREE.ConeGeometry(.4,.6,4),0x884433,{{p:[0,1.95,0],r:[0,.79,0]}});
            // Giris kapısı
            _m(new THREE.BoxGeometry(.25,.4,.02),0x553322,{{p:[0,-.6,.32]}});
            _m(new THREE.TorusGeometry(.12,.02,6,8,3.14),sc,{{p:[0,-.4,.32]}});
            // Zemin
            _m(new THREE.CylinderGeometry(.8,.8,.06,16),0x887766,{{p:[0,-.85,0]}});
        }}
        else if(T==7){{
            // MINARE — ince uzun, serefe, koni cati
            var sc=0xccccbb;
            // Kaide
            _m(new THREE.CylinderGeometry(.25,.3,.4,12),sc,{{p:[0,-.7,0]}});
            // Govde
            _m(new THREE.CylinderGeometry(.15,.22,2.0,12),sc,{{p:[0,.3,0]}});
            // Serefe (balkon)
            _m(new THREE.CylinderGeometry(.28,.28,.06,14),sc,{{p:[0,1.0,0]}});
            // Serefe korkulugu
            for(var k=0;k<10;k++){{var ka=k*.63;_m(new THREE.CylinderGeometry(.008,.008,.1,4),sc,{{p:[Math.cos(ka)*.28,1.08,Math.sin(ka)*.28]}});}}
            // Ust govde
            _m(new THREE.CylinderGeometry(.1,.15,.5,10),sc,{{p:[0,1.3,0]}});
            // Koni seri (sivri cati)
            _m(new THREE.ConeGeometry(.12,.45,10),0x667766,{{p:[0,1.78,0]}});
            // Alem (tepede)
            _m(new THREE.SphereGeometry(.025,6,6),0xdaa520,{{p:[0,2.02,0]}});
            _m(new THREE.ConeGeometry(.01,.05,4),0xdaa520,{{p:[0,2.07,0]}});
            // Pencereler
            for(var w=0;w<5;w++){{_mb(new THREE.BoxGeometry(.05,.1,.02),0x556688,{{p:[0,-.3+w*.35,.16]}});}}
        }}
        else if(T==8){{
            // KUBBE — Ayasofya/Suleymaniye tarzi
            var sc=0xccbbaa;
            // Ana kubbe
            _m(new THREE.SphereGeometry(1.0,28,16,0,6.28,0,1.57),sc,{{p:[0,.4,0],sh:60}});
            // Kubbe kasnak (drum)
            _m(new THREE.CylinderGeometry(1.0,1.05,.3,24),sc,{{p:[0,-.05,0]}});
            // Kasnak pencereleri
            for(var w=0;w<12;w++){{var wa=w*.524;_mb(new THREE.BoxGeometry(.08,.15,.02),0x88aacc,{{p:[Math.cos(wa)*1.0,.0,Math.sin(wa)*1.0],r:[0,wa,0]}});}}
            // Yarim kubbeler (Ayasofya tarzi)
            _m(new THREE.SphereGeometry(.5,16,10,0,6.28,0,1.57),sc,{{p:[0,.1,1.0],op:.7}});
            _m(new THREE.SphereGeometry(.5,16,10,0,6.28,0,1.57),sc,{{p:[0,.1,-1.0],op:.7}});
            // Taban yapi
            _m(new THREE.BoxGeometry(2.5,.15,2.5),sc,{{p:[0,-.25,0]}});
            // Sutunlar
            for(var c=0;c<8;c++){{var ca=c*.79;_m(new THREE.CylinderGeometry(.05,.06,.4,8),sc,{{p:[Math.cos(ca)*1.1,-.35,Math.sin(ca)*1.1]}});}}
            // Alem (tepede)
            _m(new THREE.SphereGeometry(.06,8,6),0xdaa520,{{p:[0,1.42,0]}});
        }}
        else if(T==9){{
            // KERVANSARAY — Selcuklu tarzi, avlu, han odasi
            var sc=0xa89878;
            // Dikdörtgen dış duvarlar
            _m(new THREE.BoxGeometry(2.5,.8,.1),sc,{{p:[0,.0,1.0]}});
            _m(new THREE.BoxGeometry(2.5,.8,.1),sc,{{p:[0,.0,-1.0]}});
            _m(new THREE.BoxGeometry(.1,.8,2),sc,{{p:[1.25,.0,0]}});
            _m(new THREE.BoxGeometry(.1,.8,2),sc,{{p:[-1.25,.0,0]}});
            // Giris portali (tac kapi)
            _m(new THREE.BoxGeometry(.6,.7,.12),0x887766,{{p:[0,.0,1.02]}});
            _m(new THREE.TorusGeometry(.25,.03,8,10,3.14),sc,{{p:[0,.3,1.02]}});
            // Ic avlu
            _m(new THREE.BoxGeometry(2.2,.04,1.7),0xccbb99,{{p:[0,-.4,0]}});
            // Avlu içinde havuz
            _m(new THREE.CylinderGeometry(.2,.2,.04,12),0x3377aa,{{p:[0,-.38,0],op:.5}});
            // Oda kemerleri
            for(var k=0;k<5;k++){{_m(new THREE.TorusGeometry(.15,.02,6,8,3.14),sc,{{p:[-.8+k*.4,.15,.95],r:[1.57,0,0]}});}}
            // Cati
            _m(new THREE.BoxGeometry(2.6,.06,2.1),sc,{{p:[0,.42,0]}});
        }}
        else if(T==10){{
            // HAN — Osmanli ticaret hani, 2 katli, avlu
            var sc=0xaa9878;
            // Dis duvarlar (kare)
            _m(new THREE.BoxGeometry(2,.9,.08),sc,{{p:[0,.1,.9]}});
            _m(new THREE.BoxGeometry(2,.9,.08),sc,{{p:[0,.1,-.9]}});
            _m(new THREE.BoxGeometry(.08,.9,1.8),sc,{{p:[1,.1,0]}});
            _m(new THREE.BoxGeometry(.08,.9,1.8),sc,{{p:[-1,.1,0]}});
            // Ic avlu
            _m(new THREE.BoxGeometry(1.7,.04,1.5),0xccbb99,{{p:[0,-.35,0]}});
            // 2. kat revak (iç balkon)
            _m(new THREE.BoxGeometry(1.8,.04,1.6),sc,{{p:[0,.35,0],op:.3}});
            // Sutunlar (avlu çevresi)
            for(var c=0;c<8;c++){{var cx=c<4?-.7+c*.47:-.7+(c-4)*.47,cz=c<4?.75:-.75;
            _m(new THREE.CylinderGeometry(.03,.035,.5,6),sc,{{p:[cx,.1,cz]}});}}
            // Giris portali
            _m(new THREE.BoxGeometry(.4,.5,.1),0x553322,{{p:[0,-.1,.92]}});
            _m(new THREE.TorusGeometry(.18,.02,6,8,3.14),sc,{{p:[0,.15,.92]}});
            // Cati
            _m(new THREE.BoxGeometry(2.1,.05,1.9),0x884433,{{p:[0,.58,0]}});
        }}
        else if(T==11){{
            // HAMAM — kubbeli, sıcaklık/soğuk bolum, kurna
            var sc=0xbbaa99;
            // Ana kubbe
            _m(new THREE.SphereGeometry(.6,20,12,0,6.28,0,1.57),sc,{{p:[0,.35,0],sh:60}});
            // Kubbe kasnak
            _m(new THREE.CylinderGeometry(.6,.65,.15,16),sc,{{p:[0,.05,0]}});
            // Beden duvarlari
            _m(new THREE.CylinderGeometry(.7,.75,.5,16),sc,{{p:[0,-.2,0]}});
            // Ikinci kubbe (soğuk bolum)
            _m(new THREE.SphereGeometry(.4,16,10,0,6.28,0,1.57),sc,{{p:[-.8,.15,0],sh:50}});
            _m(new THREE.CylinderGeometry(.42,.45,.3,12),sc,{{p:[-.8,-.1,0]}});
            // Baca (buhar)
            _m(new THREE.CylinderGeometry(.05,.06,.3,6),sc,{{p:[0,.75,0]}});
            for(var s=0;s<5;s++){{_mb(new THREE.SphereGeometry(.03,4,3),0xdddddd,{{p:[(Math.random()-.5)*.1,.9+s*.06,0],op:.3}});}}
            // Giris
            _m(new THREE.BoxGeometry(.25,.35,.08),0x553322,{{p:[-.8,-.2,.43]}});
            // Zemin
            _m(new THREE.BoxGeometry(2.5,.05,2),0x887766,{{p:[-.3,-.48,0]}});
        }}
        else if(T==12){{
            // CESME — Osmanli cesme, lule, ayna tasi, kitabe
            var sc=0xbbaa99;
            // Ana duvar (arka)
            _m(new THREE.BoxGeometry(1.2,1.2,.15),sc,{{p:[0,.1,0]}});
            // Yan kanatlar
            _m(new THREE.BoxGeometry(.1,1,.12),sc,{{p:[-.65,.0,.06]}});
            _m(new THREE.BoxGeometry(.1,1,.12),sc,{{p:[.65,.0,.06]}});
            // Ust saçak
            _m(new THREE.BoxGeometry(1.5,.06,.25),sc,{{p:[0,.72,0]}});
            // Tepe susu (aleme)
            _m(new THREE.SphereGeometry(.04,6,6),0xdaa520,{{p:[0,.78,0]}});
            // Kitabe yeri
            _m(new THREE.BoxGeometry(.6,.15,.02),0xeeddcc,{{p:[0,.55,.08]}});
            // Ayna tasi (ortadaki ovallik)
            _m(new THREE.CylinderGeometry(.2,.2,.03,16),0xeeddcc,{{p:[0,.2,.08],r:[1.57,0,0]}});
            // Lule (su agzi)
            _m(new THREE.CylinderGeometry(.02,.025,.12,6),0xccaa44,{{p:[0,.05,.12],r:[1.3,0,0]}});
            // Su
            _m(new THREE.CylinderGeometry(.01,.015,.2,4),0x4488bb,{{p:[0,-.1,.15],op:.5}});
            // Yalak (tekne)
            _m(new THREE.BoxGeometry(.6,.1,.2),sc,{{p:[0,-.4,.12]}});
            _m(new THREE.BoxGeometry(.55,.04,.15),0x3377aa,{{p:[0,-.38,.12],op:.4}});
        }}
        else if(T==13){{
            // SUR — savunma surlari, burclar, mazgallar
            var sc=0x8a8070;
            // Ana sur duvari
            _m(new THREE.BoxGeometry(3.5,.9,.2),sc,{{p:[0,.0,0]}});
            // Mazgallar
            for(var m=0;m<14;m++){{_m(new THREE.BoxGeometry(.15,.12,.22),sc,{{p:[-1.6+m*.24,.5,0]}});}}
            // Burclar (cikinti kuleler)
            for(var b=0;b<3;b++){{_m(new THREE.CylinderGeometry(.2,.22,.95,10),sc,{{p:[-1.3+b*1.3,.02,.15]}});
            _m(new THREE.ConeGeometry(.22,.2,10),0x887766,{{p:[-1.3+b*1.3,.52,.15]}});}}
            // Sur kapısı
            _m(new THREE.BoxGeometry(.4,.5,.22),0x553322,{{p:[0,-.2,.0]}});
            _m(new THREE.TorusGeometry(.18,.025,6,8,3.14),sc,{{p:[0,.05,.1]}});
            // Ic yurume yolu
            _m(new THREE.BoxGeometry(3.3,.05,.15),sc,{{p:[0,.35,-.1]}});
            // Hendek
            _m(new THREE.BoxGeometry(3.5,.08,.5),0x336699,{{p:[0,-.55,.5],op:.3}});
        }}
        else if(T==14){{
            // KULE — gözetleme kulesi, fenar kulesi tarzi
            var sc=0xb09878;
            // Taban (geniş)
            _m(new THREE.CylinderGeometry(.4,.5,.5,12),sc,{{p:[0,-.6,0]}});
            // Govde
            _m(new THREE.CylinderGeometry(.3,.38,1.5,12),sc,{{p:[0,.2,0]}});
            // Ust balkon
            _m(new THREE.CylinderGeometry(.4,.4,.06,14),sc,{{p:[0,.95,0]}});
            // Korkuluk
            for(var k=0;k<10;k++){{var ka=k*.63;_m(new THREE.CylinderGeometry(.008,.008,.12,4),sc,{{p:[Math.cos(ka)*.4,1.02,Math.sin(ka)*.4]}});}}
            // Ust yapilar (ışık odasi)
            _m(new THREE.CylinderGeometry(.2,.25,.3,10),sc,{{p:[0,1.15,0]}});
            // Cam pencereler
            for(var w=0;w<6;w++){{var wa=w*1.05;_mb(new THREE.BoxGeometry(.08,.15,.02),0xaacc88,{{p:[Math.cos(wa)*.22,1.15,Math.sin(wa)*.22],r:[0,wa,0]}});}}
            // Sivri cati
            _m(new THREE.ConeGeometry(.22,.35,8),0x884433,{{p:[0,1.48,0]}});
            // Bayrak
            _m(new THREE.CylinderGeometry(.008,.008,.3,3),0x666666,{{p:[0,1.78,0]}});
            _m(new THREE.PlaneGeometry(.15,.08),0xcc2222,{{p:[.08,1.85,0],ds:true}});
        }}
        else if(T==15){{
            // SARAY — çok kubbeli, avlulu, gorkemli
            var sc=0xccbbaa;
            // Ana bina
            _m(new THREE.BoxGeometry(2.2,.7,1.2),sc,{{p:[0,.0,0]}});
            // Ana kubbe
            _m(new THREE.SphereGeometry(.4,16,10,0,6.28,0,1.57),sc,{{p:[0,.6,0],sh:60}});
            // Yan kubbeler
            _m(new THREE.SphereGeometry(.25,12,8,0,6.28,0,1.57),sc,{{p:[-.6,.45,0]}});
            _m(new THREE.SphereGeometry(.25,12,8,0,6.28,0,1.57),sc,{{p:[.6,.45,0]}});
            // Giris portali
            _m(new THREE.BoxGeometry(.5,.5,.1),0x887766,{{p:[0,-.05,.62]}});
            _m(new THREE.TorusGeometry(.22,.025,8,10,3.14),sc,{{p:[0,.2,.62]}});
            // Sutunlar (on cephe)
            for(var c=0;c<6;c++){{_m(new THREE.CylinderGeometry(.04,.045,.5,8),sc,{{p:[-.5+c*.2,.1,.6]}});}}
            // Pencereler
            for(var w=0;w<5;w++){{_mb(new THREE.BoxGeometry(.1,.15,.02),0x5577aa,{{p:[-.4+w*.2,.15,.62]}});}}
            // Avlu duvarlari
            _m(new THREE.BoxGeometry(3,.4,.06),sc,{{p:[0,-.15,1.2],op:.5}});
            // Bahce (zemin)
            _m(new THREE.BoxGeometry(3.5,.05,3),0x448833,{{p:[0,-.38,0]}});
        }}
        else if(T==16){{
            // TAPINAK — antik Yunan/Roma, sütunlu, alinlikli
            var sc=0xddddcc;
            // Platform (stylobate)
            for(var s=0;s<3;s++){{_m(new THREE.BoxGeometry(2.2-s*.1,.06,1.4-s*.06),sc,{{p:[0,-.45+s*.06,0]}});}}
            // Sutunlar (on ve arka)
            for(var c=0;c<6;c++){{_m(new THREE.CylinderGeometry(.05,.06,.9,10),sc,{{p:[-.5+c*.2,.1,-.55]}});
            _m(new THREE.CylinderGeometry(.05,.06,.9,10),sc,{{p:[-.5+c*.2,.1,.55]}});}}
            // Yan sütunlar
            for(var c=0;c<3;c++){{_m(new THREE.CylinderGeometry(.05,.06,.9,10),sc,{{p:[-.5,.1,-.35+c*.35]}});
            _m(new THREE.CylinderGeometry(.05,.06,.9,10),sc,{{p:[.5,.1,-.35+c*.35]}});}}
            // Architrave
            _m(new THREE.BoxGeometry(1.2,.06,1.2),sc,{{p:[0,.58,0]}});
            // Üçgen alinlik
            _m(new THREE.ConeGeometry(.55,.25,3),sc,{{p:[0,.73,0],r:[0,0,1.57],s:[1,.3,1]}});
            // Cella (iç mekan)
            _m(new THREE.BoxGeometry(.8,.7,.8),sc,{{p:[0,.0,0],op:.3}});
        }}
        else if(T==17){{
            // KILISE — gotik, sivri kemerler, gul pencere, kuleler
            var sc=0xaa9988;
            // Ana govde
            _m(new THREE.BoxGeometry(1.0,1.0,.6),sc,{{p:[0,.1,0]}});
            // Nef (uzun bolum)
            _m(new THREE.BoxGeometry(.5,.8,1.2),sc,{{p:[0,.0,-.6]}});
            // Sivri cati
            _m(new THREE.ConeGeometry(.55,.4,4),0x667766,{{p:[0,.7,0],r:[0,.79,0]}});
            // Apse (yarim daire arka)
            _m(new THREE.CylinderGeometry(.3,.3,.7,10,1,false,0,3.14),sc,{{p:[0,.0,-1.2],r:[0,3.14,0]}});
            // Iki kule (on cephe)
            _m(new THREE.BoxGeometry(.25,.7,.25),sc,{{p:[-.45,.4,.3]}});
            _m(new THREE.ConeGeometry(.15,.3,4),0x667766,{{p:[-.45,.88,.3],r:[0,.79,0]}});
            _m(new THREE.BoxGeometry(.25,.7,.25),sc,{{p:[.45,.4,.3]}});
            _m(new THREE.ConeGeometry(.15,.3,4),0x667766,{{p:[.45,.88,.3],r:[0,.79,0]}});
            // Gul pencere
            _m(new THREE.TorusGeometry(.1,.015,6,12),0xdd8844,{{p:[0,.35,.31],em:0xdd6622,ei:.2}});
            _mb(new THREE.CylinderGeometry(.08,.08,.01,12),0x5588aa,{{p:[0,.35,.31],r:[1.57,0,0],op:.5}});
            // Giris
            _m(new THREE.BoxGeometry(.2,.35,.06),0x553322,{{p:[0,-.15,.31]}});
            _m(new THREE.TorusGeometry(.09,.015,6,8,3.14),sc,{{p:[0,.05,.31]}});
        }}
        else if(T==18){{
            // CAMI — kubbe, minare, avlu, sadirvan
            var sc=0xccccbb;
            // Ana kubbe
            _m(new THREE.SphereGeometry(.7,24,14,0,6.28,0,1.57),sc,{{p:[0,.5,0],sh:60}});
            // Kasnak
            _m(new THREE.CylinderGeometry(.7,.75,.2,20),sc,{{p:[0,.15,0]}});
            // Ana bina
            _m(new THREE.BoxGeometry(1.6,.6,1.4),sc,{{p:[0,-.15,0]}});
            // Yarim kubbeler
            _m(new THREE.SphereGeometry(.35,14,8,0,6.28,0,1.57),sc,{{p:[0,.25,.7],op:.7}});
            _m(new THREE.SphereGeometry(.35,14,8,0,6.28,0,1.57),sc,{{p:[0,.25,-.7],op:.7}});
            // Minare (sol)
            _m(new THREE.CylinderGeometry(.06,.08,1.8,10),sc,{{p:[-1,.4,.7]}});
            _m(new THREE.ConeGeometry(.08,.3,8),0x667766,{{p:[-1,1.45,.7]}});
            _m(new THREE.CylinderGeometry(.1,.1,.03,10),sc,{{p:[-1,1.1,.7]}});
            // Minare (sag)
            _m(new THREE.CylinderGeometry(.06,.08,1.8,10),sc,{{p:[1,.4,-.7]}});
            _m(new THREE.ConeGeometry(.08,.3,8),0x667766,{{p:[1,1.45,-.7]}});
            _m(new THREE.CylinderGeometry(.1,.1,.03,10),sc,{{p:[1,1.1,-.7]}});
            // Avlu
            _m(new THREE.BoxGeometry(1.6,.04,1),0xccbb99,{{p:[0,-.48,.9]}});
            // Sadirvan
            _m(new THREE.CylinderGeometry(.1,.1,.04,8),0x888888,{{p:[0,-.45,.9]}});
            _m(new THREE.SphereGeometry(.08,8,5,0,6.28,0,1.57),0x888888,{{p:[0,-.42,.9]}});
            // Alem
            _m(new THREE.SphereGeometry(.04,6,6),0xdaa520,{{p:[0,1.22,0]}});
        }}
        else if(T==19){{
            // ANIT — dikilitaş/anit yapilar
            var sc=0xcccccc;
            // Kaide (geniş)
            _m(new THREE.BoxGeometry(1.2,.3,1.2),0x888888,{{p:[0,-.7,0]}});
            _m(new THREE.BoxGeometry(1,.2,1),0x999999,{{p:[0,-.5,0]}});
            // Dikilitaş govde
            _m(new THREE.CylinderGeometry(.15,.2,2.2,4),sc,{{p:[0,.5,0],r:[0,.79,0]}});
            // Piramit tepe
            _m(new THREE.ConeGeometry(.15,.3,4),0xdaa520,{{p:[0,1.75,0],r:[0,.79,0]}});
            // Kabartma süslemeler
            for(var h=0;h<6;h++){{_m(new THREE.BoxGeometry(.16,.04,.01),0xbbbbaa,{{p:[0,-.2+h*.3,.16],r:[0,.79,0]}});}}
            // Basamaklar
            for(var s=0;s<4;s++){{_m(new THREE.BoxGeometry(1.4-s*.15,.06,1.4-s*.15),0x888888,{{p:[0,-.85-s*.06,0]}});}}
            // Zemin
            _m(new THREE.CylinderGeometry(1.5,1.5,.04,20),0x777777,{{p:[0,-.95,0]}});
            // Bayrak direkleri
            _m(new THREE.CylinderGeometry(.01,.01,.8,3),0x666666,{{p:[-.8,-.3,0]}});
            _m(new THREE.CylinderGeometry(.01,.01,.8,3),0x666666,{{p:[.8,-.3,0]}});
        }}

        scene.add(mainObj);"""

    if ci == 8:  # Geometrik Cisimler — 20 premium sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||60,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide,flatShading:!!o.fs,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);mainObj.add(m);return m;}}
        // Her sekil: ana cisim + wireframe + eksenler + kose noktalari
        var hues=[0,.05,.1,.15,.2,.25,.33,.38,.44,.5,.55,.61,.67,.72,.78,.83,.88,.92,.04,.14];
        var hc=new THREE.Color().setHSL(hues[T],.65,.5);
        // Eksen cizgileri
        _mb(new THREE.CylinderGeometry(.005,.005,2.8,3),0xff3333,{{r:[0,0,1.57]}});
        _mb(new THREE.CylinderGeometry(.005,.005,2.8,3),0x33ff33,{{}});
        _mb(new THREE.CylinderGeometry(.005,.005,2.8,3),0x3333ff,{{r:[1.57,0,0]}});
        // Eksen üçlari
        _mb(new THREE.ConeGeometry(.03,.08,4),0xff3333,{{p:[1.4,0,0],r:[0,0,-1.57]}});
        _mb(new THREE.ConeGeometry(.03,.08,4),0x33ff33,{{p:[0,1.4,0]}});
        _mb(new THREE.ConeGeometry(.03,.08,4),0x3333ff,{{p:[0,0,1.4],r:[1.57,0,0]}});

        if(T==0){{
            // KUP — 6 yüz, 12 kenar, 8 kose
            _m(new THREE.BoxGeometry(1.2,1.2,1.2),hc,{{sh:70,fs:true}});
            _mb(new THREE.BoxGeometry(1.2,1.2,1.2),0xffffff,{{op:.15,wf:true}});
            // Kose noktalari
            for(var x=-1;x<=1;x+=2)for(var y=-1;y<=1;y+=2)for(var z=-1;z<=1;z+=2)
            {{_mb(new THREE.SphereGeometry(.04,6,6),0xffdd33,{{p:[x*.6,y*.6,z*.6]}});}}
            // Kosegen (iç)
            _mb(new THREE.CylinderGeometry(.008,.008,2.08,3),0xffaa33,{{r:[0,0,.62],p:[0,0,0],op:.4}});
        }}
        else if(T==1){{
            // KURE — sürekli egri yüzey, sonsuz simetri
            _m(new THREE.SphereGeometry(.95,24,24),hc,{{sh:90,op:.7}});
            _mb(new THREE.SphereGeometry(.96,24,24),0xffffff,{{op:.1,wf:true}});
            // Ekvator
            _m(new THREE.TorusGeometry(.96,.012,6,48),0xffdd33,{{r:[1.57,0,0]}});
            // Meridyen
            _m(new THREE.TorusGeometry(.96,.012,6,48),0xff6633,{{}});
            _m(new THREE.TorusGeometry(.96,.012,6,48),0x33ff66,{{r:[0,1.57,0]}});
            // Merkez
            _mb(new THREE.SphereGeometry(.04,8,8),0xffffff,{{}});
            // Yariçap cizgisi
            _mb(new THREE.CylinderGeometry(.008,.008,.95,3),0xffffff,{{r:[0,0,1.57],p:[.475,0,0],op:.5}});
        }}
        else if(T==2){{
            // SILINDIR — 2 daire yüz, 1 egri yüz
            _m(new THREE.CylinderGeometry(.65,.65,1.4,28),hc,{{sh:70}});
            _mb(new THREE.CylinderGeometry(.65,.65,1.4,16),0xffffff,{{op:.12,wf:true}});
            // Ust ve alt daire vurgusu
            _m(new THREE.TorusGeometry(.65,.015,6,28),0xffdd33,{{p:[0,.7,0],r:[1.57,0,0]}});
            _m(new THREE.TorusGeometry(.65,.015,6,28),0xffdd33,{{p:[0,-.7,0],r:[1.57,0,0]}});
            // Yükseklik cizgisi
            _mb(new THREE.CylinderGeometry(.008,.008,1.4,3),0xffaa33,{{p:[.65,0,0]}});
            // Yariçap
            _mb(new THREE.CylinderGeometry(.008,.008,.65,3),0xff6633,{{p:[.325,.7,0],r:[0,0,1.57]}});
        }}
        else if(T==3){{
            // KONI — 1 tepe, 1 daire taban
            _m(new THREE.ConeGeometry(.75,1.5,24),hc,{{sh:70}});
            _mb(new THREE.ConeGeometry(.75,1.5,16),0xffffff,{{op:.12,wf:true}});
            // Taban dairesi
            _m(new THREE.TorusGeometry(.75,.015,6,24),0xffdd33,{{p:[0,-.75,0],r:[1.57,0,0]}});
            // Tepe noktası
            _mb(new THREE.SphereGeometry(.04,8,8),0xff3333,{{p:[0,.75,0]}});
            // Ana cizgi (yükseklik)
            _mb(new THREE.CylinderGeometry(.008,.008,1.5,3),0xffaa33,{{}});
            // Yan yüzey cizgisi
            _mb(new THREE.CylinderGeometry(.008,.008,1.68,3),0xff6633,{{p:[.375,0,.0],r:[0,0,.46]}});
        }}
        else if(T==4){{
            // PIRAMIT — 4 üçgen yüz + 1 kare taban
            _m(new THREE.ConeGeometry(.9,1.3,4),hc,{{fs:true,sh:60,r:[0,.79,0]}});
            _mb(new THREE.ConeGeometry(.9,1.3,4),0xffffff,{{op:.15,wf:true,r:[0,.79,0]}});
            // Kose noktalari
            _mb(new THREE.SphereGeometry(.04,6,6),0xff3333,{{p:[0,.65,0]}});
            for(var i=0;i<4;i++){{var a=i*1.57+.79;_mb(new THREE.SphereGeometry(.035,6,6),0xffdd33,{{p:[Math.cos(a)*.9,-.65,Math.sin(a)*.9]}});}}
            // Yükseklik
            _mb(new THREE.CylinderGeometry(.008,.008,1.3,3),0xffaa33,{{}});
        }}
        else if(T==5){{
            // PRIZMA — dikdörtgenler prizması
            _m(new THREE.BoxGeometry(.8,1.4,1.0),hc,{{fs:true,sh:60}});
            _mb(new THREE.BoxGeometry(.8,1.4,1.0),0xffffff,{{op:.12,wf:true}});
            // Kose noktalari
            for(var x=-1;x<=1;x+=2)for(var y=-1;y<=1;y+=2)for(var z=-1;z<=1;z+=2)
            {{_mb(new THREE.SphereGeometry(.03,5,5),0xffdd33,{{p:[x*.4,y*.7,z*.5]}});}}
        }}
        else if(T==6){{
            // TORUS — halka, iç ve dış yariçap
            _m(new THREE.TorusGeometry(.7,.22,20,48),hc,{{sh:80}});
            _mb(new THREE.TorusGeometry(.7,.22,12,24),0xffffff,{{op:.1,wf:true}});
            // Ic ve dış daire
            _m(new THREE.TorusGeometry(.48,.012,6,32),0xff6633,{{r:[1.57,0,0]}});
            _m(new THREE.TorusGeometry(.92,.012,6,32),0xffdd33,{{r:[1.57,0,0]}});
            // Kesit dairesi
            _m(new THREE.TorusGeometry(.22,.01,12,6),0x33ff66,{{p:[.7,0,0]}});
        }}
        else if(T==7){{
            // DODECAHEDRON — 12 beşgen yüz
            _m(new THREE.DodecahedronGeometry(.9),hc,{{fs:true,sh:60}});
            _mb(new THREE.DodecahedronGeometry(.91),0xffffff,{{op:.15,wf:true}});
        }}
        else if(T==8){{
            // ICOSAHEDRON — 20 üçgen yüz
            _m(new THREE.IcosahedronGeometry(.9),hc,{{fs:true,sh:60}});
            _mb(new THREE.IcosahedronGeometry(.91),0xffffff,{{op:.15,wf:true}});
        }}
        else if(T==9){{
            // OCTAHEDRON — 8 üçgen yüz
            _m(new THREE.OctahedronGeometry(.9),hc,{{fs:true,sh:60}});
            _mb(new THREE.OctahedronGeometry(.91),0xffffff,{{op:.15,wf:true}});
            // 6 kose noktası
            var ov=[[0,1,0],[0,-1,0],[1,0,0],[-1,0,0],[0,0,1],[0,0,-1]];
            for(var i=0;i<6;i++){{_mb(new THREE.SphereGeometry(.04,6,6),0xffdd33,{{p:[ov[i][0]*.9,ov[i][1]*.9,ov[i][2]*.9]}});}}
        }}
        else if(T==10){{
            // TETRAHEDRON — 4 üçgen yüz, en basit platonik
            _m(new THREE.TetrahedronGeometry(1.0),hc,{{fs:true,sh:60}});
            _mb(new THREE.TetrahedronGeometry(1.01),0xffffff,{{op:.15,wf:true}});
        }}
        else if(T==11){{
            // MOBIUS SERIDI — tek yüzlu, tek kenarli
            // Parametrik mobius
            var pts=[];for(var i=0;i<=60;i++){{var t=i/60*6.28;var hw=.2;
            var x1=(1+hw*Math.cos(t/2))*Math.cos(t),z1=(1+hw*Math.cos(t/2))*Math.sin(t),y1=hw*Math.sin(t/2);
            var x2=(1-hw*Math.cos(t/2))*Math.cos(t),z2=(1-hw*Math.cos(t/2))*Math.sin(t),y2=-hw*Math.sin(t/2);}}
            // Torus ile yaklaşım (3 kesit = mobius benzeri)
            _m(new THREE.TorusGeometry(.7,.08,3,80),hc,{{sh:70,ds:true}});
            _mb(new THREE.TorusGeometry(.7,.08,3,40),0xffffff,{{op:.12,wf:true,ds:true}});
            // Yonlendirme oku (tek tarafli)
            for(var a=0;a<6;a++){{var an=a*1.05;_mb(new THREE.ConeGeometry(.03,.08,4),0xffdd33,{{p:[Math.cos(an)*.7,.08*Math.sin(an/2),Math.sin(an)*.7],r:[0,-an,0]}});}}
        }}
        else if(T==12){{
            // HELIS — spiral yapilar
            // Sarmal (torus knot p=2,q=3 benzeri ama basit helis)
            for(var i=0;i<80;i++){{var t=i/80*6.28*3;var r=.5;
            _m(new THREE.SphereGeometry(.04,6,5),hc,{{p:[Math.cos(t)*r,-.8+i*.025,Math.sin(t)*r]}});}}
            // Merkez eksen
            _mb(new THREE.CylinderGeometry(.008,.008,2.2,3),0xffaa33,{{op:.4}});
            // Ust daire
            _m(new THREE.TorusGeometry(.5,.008,4,20),0xffdd33,{{p:[0,1.1,0],r:[1.57,0,0],op:.3}});
        }}
        else if(T==13){{
            // ELIPSOID — 3 farkli yariçap
            _m(new THREE.SphereGeometry(.8,36,36),hc,{{s:[1.3,.7,1],sh:80,op:.8}});
            _mb(new THREE.SphereGeometry(.81,18,18),0xffffff,{{s:[1.3,.7,1],op:.1,wf:true}});
            // 3 eksen
            _mb(new THREE.CylinderGeometry(.01,.01,2.1,3),0xff6633,{{r:[0,0,1.57]}});
            _mb(new THREE.CylinderGeometry(.01,.01,1.12,3),0x33ff66,{{}});
            _mb(new THREE.CylinderGeometry(.01,.01,1.6,3),0x3366ff,{{r:[1.57,0,0]}});
        }}
        else if(T==14){{
            // HIPERBOLOID — eyer şeklinde cift egri yüzey
            // Tek yaprak hiperboloid (silindir twist ile)
            for(var i=0;i<30;i++){{var t=i/30*6.28;var r=.5+.15*Math.cos(i*.3);
            _m(new THREE.SphereGeometry(.03,5,4),hc,{{p:[Math.cos(t)*r,-.8+i*.055,Math.sin(t)*r]}});}}
            for(var i=0;i<30;i++){{var t=i/30*6.28+.1;var r=.5+.15*Math.cos(i*.3+3.14);
            _m(new THREE.SphereGeometry(.03,5,4),hc,{{p:[Math.cos(t)*r,-.8+i*.055,Math.sin(t)*r]}});}}
            // Bel dairesi
            _m(new THREE.TorusGeometry(.5,.01,6,24),0xffdd33,{{r:[1.57,0,0]}});
            // Wireframe yaklasim
            _m(new THREE.CylinderGeometry(.6,.6,1.5,20),hc,{{op:.15}});
            _mb(new THREE.CylinderGeometry(.6,.6,1.5,12),0xffffff,{{op:.08,wf:true}});
        }}
        else if(T==15){{
            // PARABOLOID — parabol donmesi
            // Noktalarla parabol yüzey
            for(var i=0;i<40;i++){{var t=i/40*6.28;for(var h=0;h<5;h++){{var r=(h+1)*.15;
            _m(new THREE.SphereGeometry(.025,5,4),hc,{{p:[Math.cos(t)*r,-.6+h*h*.1,Math.sin(t)*r]}});}}}}
            // Yaklasim geometri
            _m(new THREE.ConeGeometry(.75,1.2,24,1,true),hc,{{op:.3,ds:true}});
            _mb(new THREE.ConeGeometry(.75,1.2,12,1,true),0xffffff,{{op:.1,wf:true,ds:true}});
            // Odak noktası
            _mb(new THREE.SphereGeometry(.05,8,8),0xff3333,{{p:[0,.1,0]}});
            // Eksen
            _mb(new THREE.CylinderGeometry(.008,.008,1.8,3),0xffaa33,{{op:.5}});
        }}
        else if(T==16){{
            // FRUSTUM — kesik koni (piramit)
            _m(new THREE.CylinderGeometry(.4,.8,1.3,20),hc,{{sh:70}});
            _mb(new THREE.CylinderGeometry(.4,.8,1.3,12),0xffffff,{{op:.12,wf:true}});
            // Ust daire
            _m(new THREE.TorusGeometry(.4,.012,6,20),0xffdd33,{{p:[0,.65,0],r:[1.57,0,0]}});
            // Alt daire
            _m(new THREE.TorusGeometry(.8,.012,6,20),0xffdd33,{{p:[0,-.65,0],r:[1.57,0,0]}});
            // Hayali tam koni cizgisi
            _mb(new THREE.CylinderGeometry(0,.8,2.6,12),0xffaa33,{{op:.08,wf:true}});
            // Yükseklik
            _mb(new THREE.CylinderGeometry(.008,.008,1.3,3),0xff6633,{{}});
        }}
        else if(T==17){{
            // TORUS DUGUMU — trefoil knot
            _m(new THREE.TorusKnotGeometry(.55,.12,100,12,2,3),hc,{{sh:80}});
            _mb(new THREE.TorusKnotGeometry(.55,.12,50,8,2,3),0xffffff,{{op:.1,wf:true}});
        }}
        else if(T==18){{
            // KAPSUL — silindir + 2 yarikure
            _m(new THREE.CylinderGeometry(.5,.5,.8,24),hc,{{sh:70}});
            _m(new THREE.SphereGeometry(.5,24,12,0,6.28,0,1.57),hc,{{p:[0,.4,0],sh:70}});
            _m(new THREE.SphereGeometry(.5,24,12,0,6.28,1.57,1.57),hc,{{p:[0,-.4,0],sh:70}});
            // Wireframe
            _mb(new THREE.CylinderGeometry(.51,.51,.8,12),0xffffff,{{op:.1,wf:true}});
            // Birlestirme cizgileri
            _m(new THREE.TorusGeometry(.5,.01,6,24),0xffdd33,{{p:[0,.4,0],r:[1.57,0,0]}});
            _m(new THREE.TorusGeometry(.5,.01,6,24),0xffdd33,{{p:[0,-.4,0],r:[1.57,0,0]}});
        }}
        else if(T==19){{
            // YILDIZ — 3D yildiz polyhedron
            // Stellated octahedron (yildiz octahedron)
            _m(new THREE.OctahedronGeometry(.7),hc,{{fs:true,sh:60}});
            // 8 sivri cikinti (yildiz üçlari)
            var sv=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]];
            for(var i=0;i<8;i++){{var s=sv[i];_m(new THREE.ConeGeometry(.15,.5,4),hc,{{p:[s[0]*.5,s[1]*.5,s[2]*.5],r:[s[1]<0?3.14:0,0,s[0]*s[2]*.3],fs:true}});}}
            _mb(new THREE.OctahedronGeometry(.71),0xffffff,{{op:.12,wf:true}});
            // Merkez parlama
            _mb(new THREE.SphereGeometry(.08,8,8),0xffdd33,{{op:.4}});
        }}

        scene.add(mainObj);"""

    if ci == 9:  # Fizik Deneyleri — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        if(T==0){{
            // SARKAC - Pendulum: destek, ip, kure, hareket yolu, aci
            var base=_m(new THREE.BoxGeometry(1.6,.08,.6),0x555555,{{p:[0,-1.5,0]}});mainObj.add(base);
            var lP=_m(new THREE.CylinderGeometry(.04,.05,2.8,8),0x666666,{{p:[-.6,-0.1,0]}});mainObj.add(lP);
            var rP=_m(new THREE.CylinderGeometry(.04,.05,2.8,8),0x666666,{{p:[.6,-0.1,0]}});mainObj.add(rP);
            var top=_m(new THREE.BoxGeometry(1.4,.08,.4),0x555555,{{p:[0,1.3,0]}});mainObj.add(top);
            // ip (egik pozisyon)
            var rope=_m(new THREE.CylinderGeometry(.012,.012,2.0,6),0xaa8855,{{p:[-.55,0.1,0],r:[0,0,0.4]}});mainObj.add(rope);
            // bob
            var bob=_m(new THREE.SphereGeometry(.2,24,24),0xdd3333,{{p:[-1.3,-0.9,0],sh:90}});mainObj.add(bob);
            // denge pozisyonu (kesik cizgi)
            for(var d=0;d<10;d++){{var dd=_mb(new THREE.SphereGeometry(.015,6,6),0x888888,{{p:[0,1.3-d*.25,0]}});mainObj.add(dd);}}
            // hareket yolu (yay)
            for(var a=0;a<16;a++){{var ang=-0.5+a*0.0625;var ax=Math.sin(ang)*2.0;var ay=1.3-Math.cos(ang)*2.0;var tr=_mb(new THREE.SphereGeometry(.025,6,6),0xff6644,{{p:[ax,ay,0],op:0.3+a*0.04}});mainObj.add(tr);}}
            // aci yay gosterimi
            var arc=_m(new THREE.TorusGeometry(.5,.01,8,20,0.5),0xffaa33,{{p:[0,1.3,0],r:[0,0,-0.25]}});mainObj.add(arc);
            // theta etiketi - küçük kure
            var thM=_mb(new THREE.SphereGeometry(.04,8,8),0xffdd00,{{p:[-.3,1.0,0]}});mainObj.add(thM);
            // zemin
            var floor=_m(new THREE.BoxGeometry(2.0,.03,1.0),0x444444,{{p:[0,-1.54,0]}});mainObj.add(floor);
        }}
        else if(T==1){{
            // KALDIRAC - Lever: kol, dayanak, kuvvet ok, yuk, mesafe isaretleri
            var fulcrum=_m(new THREE.ConeGeometry(.18,.35,3),0x666666,{{p:[0,-.65,0]}});mainObj.add(fulcrum);
            var beam=_m(new THREE.BoxGeometry(3.2,.07,.25),0x8B5A2B,{{p:[0,-.47,0],r:[0,0,-0.08]}});mainObj.add(beam);
            // yuk (sol taraf)
            var load=_m(new THREE.BoxGeometry(.4,.4,.35),0xcc3333,{{p:[-1.3,-.15,0]}});mainObj.add(load);
            var lLbl=_mb(new THREE.SphereGeometry(.05,8,8),0xff0000,{{p:[-1.3,.15,0]}});mainObj.add(lLbl);
            // kuvvet oku (sag taraf - asagi itme)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(1.3,.3,0),0.7,0x00cc44,.12,.08));
            // ağırlık oku (yuk üzerinde)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-1.3,-.35,0),0.4,0xff4444,.1,.07));
            // mesafe isaretleri
            for(var t=-6;t<=6;t++){{var tick=_mb(new THREE.BoxGeometry(.02,.06,.25),0xaaaaaa,{{p:[t*0.25,-.44,0]}});mainObj.add(tick);}}
            // dayanak noktası gösterge
            var pvDot=_mb(new THREE.SphereGeometry(.04,8,8),0xffdd00,{{p:[0,-.48,0]}});mainObj.add(pvDot);
            // zemin
            var fl=_m(new THREE.BoxGeometry(3.5,.04,.8),0x444444,{{p:[0,-.84,0]}});mainObj.add(fl);
            // effort kisi (basit figur)
            var hand=_m(new THREE.SphereGeometry(.08,10,10),0xffcc88,{{p:[1.3,.45,0]}});mainObj.add(hand);
        }}
        else if(T==2){{
            // MAKARA - Pulley: çerçeve, kasnak, ip, ağırlık, kuvvet oku
            var frame=_m(new THREE.CylinderGeometry(.035,.04,2.2,8),0x555555,{{p:[0,.3,0]}});mainObj.add(frame);
            var fBase=_m(new THREE.BoxGeometry(.8,.06,.5),0x555555,{{p:[0,-0.8,0]}});mainObj.add(fBase);
            var fTop=_m(new THREE.BoxGeometry(.6,.06,.3),0x555555,{{p:[0,1.4,0]}});mainObj.add(fTop);
            // kasnak (teker)
            var wheel=_m(new THREE.TorusGeometry(.3,.05,12,32),0x888888,{{p:[0,1.1,0],sh:90}});mainObj.add(wheel);
            var axle=_m(new THREE.CylinderGeometry(.04,.04,.15,8),0xaaaaaa,{{p:[0,1.1,.0],r:[1.57,0,0]}});mainObj.add(axle);
            // ip - sol (yuk tarafi)
            var ropeL=_m(new THREE.CylinderGeometry(.012,.012,1.5,6),0xaa8844,{{p:[-.3,.35,0]}});mainObj.add(ropeL);
            // ip - sag (cekme tarafi)
            var ropeR=_m(new THREE.CylinderGeometry(.012,.012,1.0,6),0xaa8844,{{p:[.3,.6,0]}});mainObj.add(ropeR);
            // ağırlık
            var wt=_m(new THREE.BoxGeometry(.35,.35,.3),0xdd4444,{{p:[-.3,-.45,0]}});mainObj.add(wt);
            // 2. ağırlık etiket
            var wLbl=_mb(new THREE.SphereGeometry(.04,8,8),0xff8800,{{p:[-.3,-.2,0]}});mainObj.add(wLbl);
            // cekme kuvveti oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(.3,.6,0),0.6,0x44cc44,.1,.07));
            // kasnak olugu detay
            var groove=_m(new THREE.TorusGeometry(.3,.02,8,32),0x666666,{{p:[0,1.1,0.06]}});mainObj.add(groove);
        }}
        else if(T==3){{
            // EGIK DUZLEM - Inclined Plane: rampa, cisim, kuvvet oklari, aci
            // rampa üçgeni
            var ramp=_m(new THREE.BoxGeometry(2.5,.06,.8),0x8B7355,{{p:[-.1,0,0],r:[0,0,-0.35]}});mainObj.add(ramp);
            // zemin
            var ground=_m(new THREE.BoxGeometry(3.0,.04,.8),0x555555,{{p:[0,-0.95,0]}});mainObj.add(ground);
            // dikey duvar
            var wall=_m(new THREE.BoxGeometry(.04,1.2,.8),0x666666,{{p:[1.05,-0.35,0]}});mainObj.add(wall);
            // cisim (kutu)
            var block=_m(new THREE.BoxGeometry(.35,.35,.35),0xdd4444,{{p:[-.4,.15,0]}});mainObj.add(block);
            // ağırlık kuvveti (asagi)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-.4,.15,0),0.6,0xff4444,.1,.07));
            // normal kuvvet (yüzeyden dik)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-Math.sin(.35),Math.cos(.35),0).normalize(),new THREE.Vector3(-.4,.15,0),0.5,0x44cc44,.1,.07));
            // surtunsuz kayma kuvveti (rampa boyunca asagi)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(Math.cos(.35),Math.sin(.35),0).normalize(),new THREE.Vector3(-.4,.15,0),0.4,0x4488ff,.1,.07));
            // aci yay
            var angArc=_m(new THREE.TorusGeometry(.4,.01,8,16,0.35),0xffaa33,{{p:[-.9,-.95,0]}});mainObj.add(angArc);
            // h yükseklik cizgisi (dikey)
            for(var h=0;h<8;h++){{var hd=_mb(new THREE.SphereGeometry(.015,6,6),0xffdd44,{{p:[1.05,-.95+h*.15,0]}});mainObj.add(hd);}}
            // etiketler
            var mDot=_mb(new THREE.SphereGeometry(.04,8,8),0xff8800,{{p:[-.4,.4,0]}});mainObj.add(mDot);
        }}
        else if(T==4){{
            // YAY HAREKETI - Spring Motion: yay, kütle, denge, genlik
            // duvar
            var wall=_m(new THREE.BoxGeometry(.12,1.2,.6),0x666666,{{p:[-1.6,0,0]}});mainObj.add(wall);
            // yay bobinleri (zigzag)
            for(var i=0;i<16;i++){{var coil=_m(new THREE.TorusGeometry(.12,.02,8,16),0x888888,{{p:[-1.5+i*0.09,(i%2==0?0.05:-0.05),0],r:[1.57,0,0],sh:90}});mainObj.add(coil);}}
            // kütle
            var mass=_m(new THREE.BoxGeometry(.4,.4,.4),0xdd4444,{{p:[0.0,0,0]}});mainObj.add(mass);
            // denge cizgisi (dikey kesikli)
            for(var d=0;d<12;d++){{var dl=_mb(new THREE.SphereGeometry(.012,6,6),0x44ff44,{{p:[0.0,-.6+d*.1,0]}});mainObj.add(dl);}}
            // genlik oklari
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(0.0,.5,0),0.5,0xff8844,.08,.06));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(0.0,.5,0),0.5,0xff8844,.08,.06));
            // geri cagirma kuvveti oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(0.2,0,0),0.6,0x4488ff,.1,.07));
            // F=-kx etiketi
            var fLbl=_mb(new THREE.SphereGeometry(.04,8,8),0xffdd00,{{p:[-.2,.35,0]}});mainObj.add(fLbl);
            // zemin
            var fl=_m(new THREE.BoxGeometry(3.5,.03,.6),0x444444,{{p:[-.3,-.62,0]}});mainObj.add(fl);
        }}
        else if(T==5){{
            // ELEKTROMIKNATÎS - Electromagnet: demir cekirdek, sarim, alan cizgileri, pil
            // demir cekirdek
            var core=_m(new THREE.CylinderGeometry(.12,.12,1.8,12),0x888888,{{p:[0,0,0],r:[0,0,1.57],sh:90}});mainObj.add(core);
            // sarim bobinleri (sag el kurali)
            for(var w=0;w<20;w++){{var coil=_m(new THREE.TorusGeometry(.22,.025,8,20),0xcc6600,{{p:[-0.7+w*0.07,0,0],r:[0,1.57,0],sh:60}});mainObj.add(coil);}}
            // manyetik alan cizgileri (N kutbu - sag)
            for(var f=0;f<6;f++){{var ang=f*1.047;var fx=0.9+Math.cos(ang)*0.4;var fy=Math.sin(ang)*0.5;
            var fLine=_m(new THREE.TorusGeometry(0.5,.008,6,20,3.14),0x4488ff,{{p:[fx*.5,fy,0],r:[0,0,ang],op:0.6}});mainObj.add(fLine);}}
            // N/S kutup isaretleri
            var nPole=_mb(new THREE.SphereGeometry(.06,8,8),0xff3333,{{p:[.95,0,0]}});mainObj.add(nPole);
            var sPole=_mb(new THREE.SphereGeometry(.06,8,8),0x3333ff,{{p:[-.95,0,0]}});mainObj.add(sPole);
            // pil
            var bat=_m(new THREE.BoxGeometry(.35,.2,.15),0x333333,{{p:[0,-.7,0]}});mainObj.add(bat);
            var bPlus=_mb(new THREE.SphereGeometry(.03,6,6),0xff0000,{{p:[.12,-.7,0.08]}});mainObj.add(bPlus);
            var bMin=_mb(new THREE.SphereGeometry(.03,6,6),0x0000ff,{{p:[-.12,-.7,0.08]}});mainObj.add(bMin);
            // kablolar
            var cL=_m(new THREE.CylinderGeometry(.015,.015,.6,6),0xcc3333,{{p:[-.5,-.35,0],r:[0,0,0.3]}});mainObj.add(cL);
            var cR=_m(new THREE.CylinderGeometry(.015,.015,.6,6),0x3333cc,{{p:[.5,-.35,0],r:[0,0,-0.3]}});mainObj.add(cR);
            // demir parca cekilme
            var iron=_m(new THREE.BoxGeometry(.12,.12,.12),0x999999,{{p:[1.4,0,0]}});mainObj.add(iron);
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(1.4,0,0),0.3,0x44ff44,.06,.05));
        }}
        else if(T==6){{
            // TESLA BOBINI - Tesla Coil: primer bobin, sekonder bobin, toroid, kivilcim
            // taban
            var base=_m(new THREE.CylinderGeometry(.6,.65,.15,24),0x444444,{{p:[0,-1.2,0]}});mainObj.add(base);
            // primer bobin (altta kısa geniş)
            for(var p=0;p<6;p++){{var pc=_m(new THREE.TorusGeometry(.45,.025,8,32),0xcc6600,{{p:[0,-1.05+p*.08,0],sh:60}});mainObj.add(pc);}}
            // sekonder bobin (uzun ince)
            var secCore=_m(new THREE.CylinderGeometry(.08,.08,2.0,12),0x666666,{{p:[0,0,0],sh:50}});mainObj.add(secCore);
            for(var s=0;s<28;s++){{var sc=_m(new THREE.TorusGeometry(.12,.015,8,24),0xcc7700,{{p:[0,-0.7+s*.07,0],sh:50}});mainObj.add(sc);}}
            // toroid (ust)
            var toroid=_m(new THREE.TorusGeometry(.35,.1,16,32),0xbbbbbb,{{p:[0,1.2,0],sh:100}});mainObj.add(toroid);
            // kivilcim/ark (emissive)
            for(var k=0;k<5;k++){{var ang=k*1.256;var kLen=0.5+Math.random()*0.3;
            var spark=_m(new THREE.CylinderGeometry(.008,.003,kLen,4),0x8844ff,{{p:[Math.sin(ang)*(0.35+kLen*.4),1.2+Math.cos(ang)*kLen*.3,Math.cos(ang)*.2],r:[Math.cos(ang)*.5,0,ang],em:0x6633cc}});mainObj.add(spark);}}
            // parlama halo
            var glow=_m(new THREE.SphereGeometry(.5,16,16),0x6633ff,{{p:[0,1.2,0],op:0.15,em:0x4422aa}});mainObj.add(glow);
        }}
        else if(T==7){{
            // DALGA HAREKETI - Wave Motion: enine dalga, dalga boyu, genlik
            // dalga parcaciklari (sinusoidal)
            for(var w=0;w<50;w++){{var wx=-2.5+w*0.1;var wy=Math.sin(w*0.5)*0.6;
            var dot=_m(new THREE.SphereGeometry(.04,10,10),0x4488ff,{{p:[wx,wy,0],sh:80}});mainObj.add(dot);
            // baglanti cizgileri
            if(w>0){{var pwx=-2.5+(w-1)*0.1;var pwy=Math.sin((w-1)*0.5)*0.6;
            var seg=_m(new THREE.CylinderGeometry(.01,.01,0.12,4),0x3366cc,{{p:[(wx+pwx)/2,(wy+pwy)/2,0]}});mainObj.add(seg);}}}}
            // denge ekseni
            var axis=_m(new THREE.CylinderGeometry(.008,.008,5.5,4),0x888888,{{p:[0,0,0],r:[0,0,1.57]}});mainObj.add(axis);
            // dalga boyu ok (lambda)
            var lam1=-2.0,lam2=-2.0+Math.PI*0.2;
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(-1.7,-.9,0),1.26,0xff8844,.08,.06));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(-.44,-.9,0),1.26,0xff8844,.08,.06));
            // lambda etiket
            var lamDot=_mb(new THREE.SphereGeometry(.04,8,8),0xffaa33,{{p:[-1.1,-.85,0]}});mainObj.add(lamDot);
            // genlik ok (A)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(-2.1,0,0),0.6,0x44ff44,.08,.06));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-2.1,0,0),0.6,0x44ff44,.08,.06));
            // ilerleme yonu oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(1.5,.9,0),0.8,0xff4444,.1,.07));
        }}
        else if(T==8){{
            // ISIK KIRILMASI - Light Refraction: prizma, giriş isini, kirik isin, normal
            // cam prizma (üçgen)
            var prismGeo=new THREE.CylinderGeometry(.01,.8,1.2,3);
            var prism=_m(prismGeo,0x88bbee,{{p:[0,0,0],r:[0,0,0],op:0.35,sh:100}});mainObj.add(prism);
            var prismWf=_mb(prismGeo,0x6699cc,{{p:[0,0,0],wf:true,op:0.6}});mainObj.add(prismWf);
            // giriş beyaz ışık isini
            var inRay=_m(new THREE.CylinderGeometry(.02,.02,2.0,6),0xffffff,{{p:[-1.3,.2,0],r:[0,0,0.6],em:0x888888}});mainObj.add(inRay);
            // çıkış renk spektrumu (VIBGYOR)
            var specColors=[0xff0000,0xff6600,0xffff00,0x00ff00,0x0088ff,0x4400ff,0x8800ff];
            for(var s=0;s<7;s++){{var sa=0.15+s*0.08;
            var ray=_m(new THREE.CylinderGeometry(.012,.012,1.6,4),specColors[s],{{p:[1.0+s*0.08,-.3-s*0.12,0],r:[0,0,-0.6-s*0.06],em:specColors[s]}});mainObj.add(ray);}}
            // normal cizgisi (kesikli)
            for(var n=0;n<10;n++){{var nd=_mb(new THREE.SphereGeometry(.015,6,6),0xaaaaaa,{{p:[-.35,-.6+n*.12,0]}});mainObj.add(nd);}}
            // aci isaretleri
            var arcIn=_m(new THREE.TorusGeometry(.25,.008,6,16,.5),0xffdd44,{{p:[-.35,.1,0],r:[0,0,0.3]}});mainObj.add(arcIn);
        }}
        else if(T==9){{
            // MERCEK - Convex Lens: mercek, odak noktalari, optik eksen, isinlar, goruntu
            // ince mercek (bikonveks)
            var lens=_m(new THREE.SphereGeometry(.6,32,32),0x88ccee,{{p:[0,0,0],s:[0.08,1,1],op:0.3,sh:100}});mainObj.add(lens);
            var lensEdge=_mb(new THREE.TorusGeometry(.6,.015,8,32),0x6699bb,{{p:[0,0,0]}});mainObj.add(lensEdge);
            // optik eksen
            var optAxis=_m(new THREE.CylinderGeometry(.006,.006,4.5,4),0x888888,{{p:[0,0,0],r:[0,0,1.57]}});mainObj.add(optAxis);
            // odak noktalari (F ve F')
            var f1=_mb(new THREE.SphereGeometry(.05,10,10),0xff4444,{{p:[-0.8,0,0]}});mainObj.add(f1);
            var f2=_mb(new THREE.SphereGeometry(.05,10,10),0xff4444,{{p:[0.8,0,0]}});mainObj.add(f2);
            // nesne (ok)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(-1.6,0,0),0.7,0x44cc44,.1,.07));
            // goruntu (ters ok)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(1.6,0,0),0.5,0xff8844,.08,.06));
            // isinlar: paralel -> odak, merkez -> duz, odak -> paralel
            var r1=_m(new THREE.CylinderGeometry(.008,.008,1.6,4),0xffdd44,{{p:[-.8,.7,0],r:[0,0,1.57],em:0x886600}});mainObj.add(r1);
            var r1b=_m(new THREE.CylinderGeometry(.008,.008,1.8,4),0xffdd44,{{p:[.9,.2,0],r:[0,0,1.3],em:0x886600}});mainObj.add(r1b);
            var r2=_m(new THREE.CylinderGeometry(.008,.008,3.5,4),0xffdd44,{{p:[0,.25,0],r:[0,0,1.47],em:0x886600}});mainObj.add(r2);
            // 2F noktalari
            var f2a=_mb(new THREE.SphereGeometry(.035,8,8),0x8844ff,{{p:[-1.6,0,0]}});mainObj.add(f2a);
            var f2b=_mb(new THREE.SphereGeometry(.035,8,8),0x8844ff,{{p:[1.6,0,0]}});mainObj.add(f2b);
        }}
        else if(T==10){{
            // AYNA - Concave Mirror: cukur ayna, odak, merkez, isinlar
            // cukur ayna (yarim kure kesimi)
            var mirror=_m(new THREE.SphereGeometry(1.5,32,32,0,Math.PI*2,0,0.4),0xccccee,{{p:[1.2,0,0],r:[0,0,-1.57],sh:120}});mainObj.add(mirror);
            var mirrorBack=_m(new THREE.SphereGeometry(1.52,32,32,0,Math.PI*2,0,0.4),0x555555,{{p:[1.2,0,0],r:[0,0,-1.57]}});mainObj.add(mirrorBack);
            // optik eksen
            var oAxis=_m(new THREE.CylinderGeometry(.006,.006,4.0,4),0x888888,{{p:[-.5,0,0],r:[0,0,1.57]}});mainObj.add(oAxis);
            // odak F
            var fPt=_mb(new THREE.SphereGeometry(.05,10,10),0xff4444,{{p:[.45,0,0]}});mainObj.add(fPt);
            // merkez C
            var cPt=_mb(new THREE.SphereGeometry(.05,10,10),0x4444ff,{{p:[1.2,0,0]}});mainObj.add(cPt);
            // nesne
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(-1.0,0,0),0.6,0x44cc44,.1,.07));
            // goruntu (ters)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(.1,0,0),0.3,0xff8844,.08,.06));
            // yansima isinlari
            var yr1=_m(new THREE.CylinderGeometry(.008,.008,2.2,4),0xffdd44,{{p:[.1,.6,0],r:[0,0,1.57],em:0x886600}});mainObj.add(yr1);
            var yr2=_m(new THREE.CylinderGeometry(.008,.008,1.5,4),0xffdd44,{{p:[-.2,.35,0],r:[0,0,1.2],em:0x886600}});mainObj.add(yr2);
        }}
        else if(T==11){{
            // MANYETIK ALAN - Magnetiç Field: cubuk miknatîs, alan cizgileri, demir tözü
            // cubuk miknatîs
            var magN=_m(new THREE.BoxGeometry(.8,.3,.25),0xcc2222,{{p:[.4,0,0]}});mainObj.add(magN);
            var magS=_m(new THREE.BoxGeometry(.8,.3,.25),0x2222cc,{{p:[-.4,0,0]}});mainObj.add(magS);
            // N ve S etiket noktası
            var nDot=_mb(new THREE.SphereGeometry(.04,8,8),0xff6666,{{p:[.7,.2,0]}});mainObj.add(nDot);
            var sDot=_mb(new THREE.SphereGeometry(.04,8,8),0x6666ff,{{p:[-.7,.2,0]}});mainObj.add(sDot);
            // manyetik alan cizgileri (8 cift simetrik)
            for(var f=0;f<8;f++){{var fR=0.3+f*0.12;var fAng=f*0.15;
            var fLine=_m(new THREE.TorusGeometry(fR,.007,6,32,3.14),0x44aaff,{{p:[0,0,f%2?0.1:-0.1],r:[1.57+fAng,0,0],op:0.5+f*0.04}});mainObj.add(fLine);
            var fLine2=_m(new THREE.TorusGeometry(fR,.007,6,32,3.14),0x44aaff,{{p:[0,0,f%2?-0.1:0.1],r:[-1.57-fAng,0,0],op:0.5+f*0.04}});mainObj.add(fLine2);}}
            // demir tözü parcaciklari (dağılim)
            for(var p=0;p<40;p++){{var px=(Math.random()-0.5)*2.5;var py=(Math.random()-0.5)*1.5;
            var dist=Math.sqrt(px*px+py*py);if(dist<0.5)continue;
            var iron=_mb(new THREE.SphereGeometry(.015,4,4),0x666666,{{p:[px,py,(Math.random()-0.5)*0.3],op:0.6}});mainObj.add(iron);}}
            // ok yonleri (N'den S'ye dış)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0).normalize(),new THREE.Vector3(.8,.3,0),0.4,0xff6644,.06,.04));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0).normalize(),new THREE.Vector3(0,1.0,0),0.3,0xff6644,.06,.04));
        }}
        else if(T==12){{
            // ELEKTRIK ALANI - Electriç Field: iki yuk, alan cizgileri, esipotansiyel
            // pozitif yuk
            var posQ=_m(new THREE.SphereGeometry(.18,20,20),0xff3333,{{p:[-.8,0,0],sh:80,em:0x441111}});mainObj.add(posQ);
            // negatif yuk
            var negQ=_m(new THREE.SphereGeometry(.18,20,20),0x3333ff,{{p:[.8,0,0],sh:80,em:0x111144}});mainObj.add(negQ);
            // + ve - isaretleri
            var plus1=_m(new THREE.BoxGeometry(.15,.03,.03),0xffffff,{{p:[-.8,0,0.1]}});mainObj.add(plus1);
            var plus2=_m(new THREE.BoxGeometry(.03,.15,.03),0xffffff,{{p:[-.8,0,0.1]}});mainObj.add(plus2);
            var minus=_m(new THREE.BoxGeometry(.15,.03,.03),0xffffff,{{p:[.8,0,0.1]}});mainObj.add(minus);
            // alan cizgileri (pozitiften negatife)
            for(var f=0;f<10;f++){{var fAng=-1.2+f*0.27;
            var startX=-.8+Math.cos(fAng)*0.25;var startY=Math.sin(fAng)*0.25;
            var endX=.8-Math.cos(fAng)*0.25;var endY=-Math.sin(fAng)*0.25;
            var fSeg=_m(new THREE.CylinderGeometry(.006,.006,1.3,4),0xffaa33,{{p:[(startX+endX)/2,(startY+endY)/2,0],r:[0,0,Math.atan2(endY-startY,endX-startX)+1.57],op:0.6,em:0x553300}});mainObj.add(fSeg);}}
            // esipotansiyel cizgileri (daireler)
            for(var e=1;e<=3;e++){{var eCirc=_m(new THREE.TorusGeometry(e*0.25,.005,6,24),0x44ff44,{{p:[-.8,0,0],op:0.3}});mainObj.add(eCirc);
            var eCirc2=_m(new THREE.TorusGeometry(e*0.25,.005,6,24),0x44ff44,{{p:[.8,0,0],op:0.3}});mainObj.add(eCirc2);}}
        }}
        else if(T==13){{
            // ROKET ITISI - Rocket Propulsion: govde, bürün, kanatlar, egzoz, itis oku
            // govde
            var body=_m(new THREE.CylinderGeometry(.25,.28,1.8,16),0xcccccc,{{p:[0,.3,0],sh:80}});mainObj.add(body);
            // bürün konisi
            var nose=_m(new THREE.ConeGeometry(.25,.6,16),0xff4444,{{p:[0,1.5,0]}});mainObj.add(nose);
            // ust bant
            var band=_m(new THREE.CylinderGeometry(.26,.26,.08,16),0x333333,{{p:[0,1.15,0]}});mainObj.add(band);
            // alt bant
            var band2=_m(new THREE.CylinderGeometry(.29,.29,.08,16),0x333333,{{p:[0,-.55,0]}});mainObj.add(band2);
            // 4 kanat (fin)
            for(var fn=0;fn<4;fn++){{var fAng=fn*1.57;
            var fin=_m(new THREE.BoxGeometry(.02,.5,.3),0x444444,{{p:[Math.sin(fAng)*.35,-.4,Math.cos(fAng)*.35],r:[0,fAng,0.2]}});mainObj.add(fin);}}
            // nözül
            var nozzle=_m(new THREE.CylinderGeometry(.2,.15,.2,12),0x888888,{{p:[0,-.65,0],sh:90}});mainObj.add(nozzle);
            // egzoz alevi
            var flame1=_m(new THREE.ConeGeometry(.18,.8,12),0xff6600,{{p:[0,-1.15,0],r:[Math.PI,0,0],em:0xcc4400,op:0.8}});mainObj.add(flame1);
            var flame2=_m(new THREE.ConeGeometry(.1,.6,8),0xffcc00,{{p:[0,-1.05,0],r:[Math.PI,0,0],em:0xcc8800,op:0.7}});mainObj.add(flame2);
            var flame3=_m(new THREE.ConeGeometry(.05,.4,6),0xffffff,{{p:[0,-.95,0],r:[Math.PI,0,0],em:0xcccccc,op:0.9}});mainObj.add(flame3);
            // itis kuvveti oku (yukari)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(.5,1.0,0),0.8,0x00ff44,.12,.08));
            // ağırlık oku (asagi)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(.5,.0,0),0.5,0xff4444,.1,.07));
            // duman parcaciklari
            for(var s=0;s<8;s++){{var sm=_m(new THREE.SphereGeometry(.06+s*.02,8,8),0x888888,{{p:[(Math.random()-.5)*.3,-1.5-s*.15,(Math.random()-.5)*.3],op:0.3-s*.03}});mainObj.add(sm);}}
        }}
        else if(T==14){{
            // JIROSKOP - Gyroscope: donen tekerlek, gimbal halkalari, eksen
            // dış gimbal (büyük halka)
            var outerG=_m(new THREE.TorusGeometry(.9,.03,8,48),0x888888,{{p:[0,0,0],sh:80}});mainObj.add(outerG);
            // orta gimbal (dikey halka)
            var midG=_m(new THREE.TorusGeometry(.7,.03,8,40),0xaaaa55,{{p:[0,0,0],r:[1.57,0,0],sh:80}});mainObj.add(midG);
            // iç gimbal (yatay halka)
            var innerG=_m(new THREE.TorusGeometry(.5,.03,8,36),0x55aaaa,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(innerG);
            // volan (rotor)
            var rotor=_m(new THREE.CylinderGeometry(.35,.35,.08,32),0xdddddd,{{p:[0,0,0],sh:100}});mainObj.add(rotor);
            var rotorRim=_m(new THREE.TorusGeometry(.35,.04,8,32),0xcccccc,{{p:[0,0,0],sh:90}});mainObj.add(rotorRim);
            // eksen cubugu
            var axle=_m(new THREE.CylinderGeometry(.02,.02,1.2,8),0x666666,{{p:[0,0,0]}});mainObj.add(axle);
            // donme yonu oklari
            for(var a=0;a<4;a++){{var aa=a*1.57;
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(Math.cos(aa+1.57),0,Math.sin(aa+1.57)).normalize(),new THREE.Vector3(Math.cos(aa)*.4,0,Math.sin(aa)*.4),0.2,0xff8844,.05,.04));}}
            // taban
            var stand=_m(new THREE.CylinderGeometry(.08,.15,.4,8),0x555555,{{p:[0,-1.0,0]}});mainObj.add(stand);
            var baseP=_m(new THREE.CylinderGeometry(.25,.3,.06,16),0x444444,{{p:[0,-1.2,0]}});mainObj.add(baseP);
            // precesyon oku (ust)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(0,.7,0),0.5,0x44ff44,.08,.06));
        }}
        else if(T==15){{
            // TERAZI - Balance Scale: orta direk, kol, 2 kefe, ibre, olcek
            // taban
            var base=_m(new THREE.CylinderGeometry(.4,.45,.08,24),0x666666,{{p:[0,-1.3,0]}});mainObj.add(base);
            // direk
            var pillar=_m(new THREE.CylinderGeometry(.05,.06,2.0,8),0x888888,{{p:[0,-.3,0],sh:80}});mainObj.add(pillar);
            // ust pivot noktası
            var pivotPt=_m(new THREE.SphereGeometry(.08,12,12),0xaaaa44,{{p:[0,.7,0],sh:90}});mainObj.add(pivotPt);
            // kol (hafif egik)
            var arm=_m(new THREE.BoxGeometry(2.5,.06,.12),0xccaa44,{{p:[0,.7,0],r:[0,0,-0.05]}});mainObj.add(arm);
            // sol kefe zincirleri
            for(var c=0;c<3;c++){{var ca=c*2.094;
            var chain=_m(new THREE.CylinderGeometry(.01,.01,.6,4),0xaaaa44,{{p:[-1.1+Math.sin(ca)*.08,.35,Math.cos(ca)*.08]}});mainObj.add(chain);}}
            // sol kefe (tabak)
            var panL=_m(new THREE.CylinderGeometry(.3,.28,.04,20),0xccaa44,{{p:[-1.1,.05,0],sh:70}});mainObj.add(panL);
            // sag kefe zincirleri
            for(var c=0;c<3;c++){{var ca=c*2.094;
            var chainR=_m(new THREE.CylinderGeometry(.01,.01,.55,4),0xaaaa44,{{p:[1.1+Math.sin(ca)*.08,.4,Math.cos(ca)*.08]}});mainObj.add(chainR);}}
            // sag kefe
            var panR=_m(new THREE.CylinderGeometry(.3,.28,.04,20),0xccaa44,{{p:[1.1,.12,0],sh:70}});mainObj.add(panR);
            // sol kefeye ağırlık
            var wt1=_m(new THREE.CylinderGeometry(.08,.08,.12,10),0xdd4444,{{p:[-1.1,.15,0]}});mainObj.add(wt1);
            var wt2=_m(new THREE.CylinderGeometry(.06,.06,.1,10),0xdd6644,{{p:[-1.0,.15,0]}});mainObj.add(wt2);
            // ibre
            var needle=_m(new THREE.CylinderGeometry(.015,.005,.5,4),0xff4444,{{p:[0,.4,0.08]}});mainObj.add(needle);
            // olcek yay (arka)
            var scale=_m(new THREE.TorusGeometry(.2,.008,6,20,2.0),0xdddddd,{{p:[0,.15,0.08],r:[0,0,-0.15]}});mainObj.add(scale);
        }}
        else if(T==16){{
            // PUSULA - Compass: govde, igne, kardinal yonler, cam kapak
            // dış govde (silindir)
            var housing=_m(new THREE.CylinderGeometry(.9,.9,.15,32),0xcc8833,{{p:[0,0,0],sh:70}});mainObj.add(housing);
            var rim=_m(new THREE.TorusGeometry(.9,.04,8,32),0xaa6622,{{p:[0,0,0],sh:60}});mainObj.add(rim);
            // kadran (beyaz disk)
            var dial=_m(new THREE.CylinderGeometry(.82,.82,.02,32),0xf5f5dc,{{p:[0,.05,0]}});mainObj.add(dial);
            // kardinal yon isaretleri (N-S-E-W)
            var dirs=[0,1.57,3.14,4.71];var dClr=[0xff0000,0x333333,0x333333,0x333333];
            for(var d=0;d<4;d++){{var dx=Math.sin(dirs[d])*.65;var dz=Math.cos(dirs[d])*.65;
            var mark=_m(new THREE.BoxGeometry(.04,.04,.12),dClr[d],{{p:[dx,.08,dz]}});mainObj.add(mark);}}
            // ara yonler (8 cizgi)
            for(var s=0;s<8;s++){{var sa=s*0.785;var sx=Math.sin(sa)*.55;var sz=Math.cos(sa)*.55;
            var tick=_m(new THREE.BoxGeometry(.02,.04,.06),0x666666,{{p:[sx,.08,sz]}});mainObj.add(tick);}}
            // pusula ignesi - kuzey (kirmizi)
            var needleN=_m(new THREE.ConeGeometry(.06,.6,3),0xff2222,{{p:[0,.12,.25],r:[1.57,0,0],em:0x441111}});mainObj.add(needleN);
            // pusula ignesi - güney (beyaz)
            var needleS=_m(new THREE.ConeGeometry(.06,.6,3),0xdddddd,{{p:[0,.12,-.25],r:[-1.57,0,0]}});mainObj.add(needleS);
            // pivot noktası
            var pivotC=_m(new THREE.SphereGeometry(.04,10,10),0xccaa33,{{p:[0,.14,0],sh:100}});mainObj.add(pivotC);
            // cam kapak (seffaf kubbe)
            var glass=_m(new THREE.SphereGeometry(.85,24,24,0,Math.PI*2,0,Math.PI/3),0xeeeeff,{{p:[0,.0,0],op:0.15,sh:120}});mainObj.add(glass);
            // derece halkalari
            var degRing=_m(new THREE.TorusGeometry(.75,.005,6,60),0xaaaaaa,{{p:[0,.06,0],op:0.5}});mainObj.add(degRing);
        }}
        else if(T==17){{
            // SAAT MEKANIZMASI - Clock Mechanism: dışli carklar, escapement, sarkac, çerçeve
            // çerçeve
            var frame1=_m(new THREE.BoxGeometry(.06,2.2,.3),0x8B6914,{{p:[-.8,0,0]}});mainObj.add(frame1);
            var frame2=_m(new THREE.BoxGeometry(.06,2.2,.3),0x8B6914,{{p:[.8,0,0]}});mainObj.add(frame2);
            var frameT=_m(new THREE.BoxGeometry(1.7,.06,.3),0x8B6914,{{p:[0,1.1,0]}});mainObj.add(frameT);
            var frameB=_m(new THREE.BoxGeometry(1.7,.06,.3),0x8B6914,{{p:[0,-1.1,0]}});mainObj.add(frameB);
            // ana dışli (büyük)
            var mainGear=_m(new THREE.CylinderGeometry(.45,.45,.06,24),0xccaa44,{{p:[-.2,.3,0],sh:80}});mainObj.add(mainGear);
            // dışli dışleri (büyük)
            for(var t=0;t<16;t++){{var ta=t*0.393;
            var tooth=_m(new THREE.BoxGeometry(.06,.04,.06),0xbbaa33,{{p:[-.2+Math.cos(ta)*.48,.3+Math.sin(ta)*.48,0]}});mainObj.add(tooth);}}
            // orta dışli
            var midGear=_m(new THREE.CylinderGeometry(.25,.25,.06,16),0xddbb55,{{p:[.3,.1,0.05],sh:80}});mainObj.add(midGear);
            for(var t=0;t<10;t++){{var ta=t*0.628;
            var tooth=_m(new THREE.BoxGeometry(.04,.03,.06),0xccaa44,{{p:[.3+Math.cos(ta)*.28,.1+Math.sin(ta)*.28,0.05]}});mainObj.add(tooth);}}
            // küçük dışli
            var smGear=_m(new THREE.CylinderGeometry(.15,.15,.06,12),0xeecc66,{{p:[.1,-.4,0.1],sh:80}});mainObj.add(smGear);
            for(var t=0;t<8;t++){{var ta=t*0.785;
            var tooth=_m(new THREE.BoxGeometry(.03,.025,.06),0xddbb55,{{p:[.1+Math.cos(ta)*.17,-.4+Math.sin(ta)*.17,0.1]}});mainObj.add(tooth);}}
            // eksen cubuklar
            var ax1=_m(new THREE.CylinderGeometry(.02,.02,.2,6),0x888888,{{p:[-.2,.3,0],r:[1.57,0,0]}});mainObj.add(ax1);
            var ax2=_m(new THREE.CylinderGeometry(.02,.02,.2,6),0x888888,{{p:[.3,.1,0.05],r:[1.57,0,0]}});mainObj.add(ax2);
            // escapement carki
            var escWheel=_m(new THREE.TorusGeometry(.12,.015,6,24),0xccaa33,{{p:[-.2,-.5,0],sh:90}});mainObj.add(escWheel);
            // sarkac cubugu
            var pendRod=_m(new THREE.CylinderGeometry(.01,.01,.9,6),0x888888,{{p:[-.2,-.95,0]}});mainObj.add(pendRod);
            // sarkac ağırlık
            var pendBob=_m(new THREE.SphereGeometry(.08,12,12),0xccaa44,{{p:[-.2,-1.4,0],sh:90}});mainObj.add(pendBob);
        }}
        else if(T==18){{
            // SES DALGASI - Sound Wave: boyuna dalga, sikisma/seyrelme, hoparlor
            // hoparlor
            var spkBody=_m(new THREE.CylinderGeometry(.15,.3,.3,16),0x333333,{{p:[-2.0,0,0],r:[0,0,1.57]}});mainObj.add(spkBody);
            var spkCone=_m(new THREE.CylinderGeometry(.3,.12,.15,16),0x666666,{{p:[-1.82,0,0],r:[0,0,1.57]}});mainObj.add(spkCone);
            var spkCenter=_m(new THREE.SphereGeometry(.06,10,10),0x444444,{{p:[-1.78,0,0]}});mainObj.add(spkCenter);
            // boyuna dalga parcaciklari (sikisma/seyrelme)
            for(var w=0;w<40;w++){{var wx=-1.5+w*0.08;
            var compression=Math.sin(w*0.6)*0.03;
            var actualX=wx+compression;
            var density=0.5+Math.cos(w*0.6)*0.4;
            var pSize=0.02+density*0.02;
            var dot=_m(new THREE.SphereGeometry(pSize,8,8),0x4488ff,{{p:[actualX,0,0],op:0.4+density*0.5}});mainObj.add(dot);
            // usteki ve alttaki parcaciklar
            var dotUp=_m(new THREE.SphereGeometry(pSize*0.8,6,6),0x4488ff,{{p:[actualX,.3,0],op:0.3+density*0.4}});mainObj.add(dotUp);
            var dotDn=_m(new THREE.SphereGeometry(pSize*0.8,6,6),0x4488ff,{{p:[actualX,-.3,0],op:0.3+density*0.4}});mainObj.add(dotDn);}}
            // sikisma bölgeleri etiketi
            var compZone=_m(new THREE.BoxGeometry(.3,.03,.03),0xff4444,{{p:[-0.5,.6,0],em:0x441111}});mainObj.add(compZone);
            // seyrelme bölgesi etiketi
            var rarZone=_m(new THREE.BoxGeometry(.3,.03,.03),0x44ff44,{{p:[0.3,.6,0],em:0x114411}});mainObj.add(rarZone);
            // ilerleme yonu oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(0.5,.8,0),0.8,0xff8844,.1,.07));
            // basinc grafigi (ust)
            for(var g=0;g<30;g++){{var gx=-1.5+g*0.1;var gy=.9+Math.sin(g*0.6)*0.2;
            var gDot=_mb(new THREE.SphereGeometry(.015,6,6),0xffaa33,{{p:[gx,gy,0]}});mainObj.add(gDot);}}
        }}
        else if(T==19){{
            // SARMAL YAY - Heliçal Spring: detayli bobin, kütle, denge, F=-kx
            // duvar/destek
            var wall=_m(new THREE.BoxGeometry(.1,1.4,.6),0x666666,{{p:[-1.8,0,0]}});mainObj.add(wall);
            // yay helis (3D sarmal)
            var springPts=[];
            for(var i=0;i<120;i++){{var t=i*0.15;var sx=-1.7+t*0.018;var sy=Math.cos(t)*0.15;var sz=Math.sin(t)*0.15;
            var sPt=_m(new THREE.SphereGeometry(.02,6,6),0xaaaaaa,{{p:[sx,sy,sz],sh:90}});mainObj.add(sPt);}}
            // kütle
            var mass=_m(new THREE.BoxGeometry(.45,.45,.45),0xdd4444,{{p:[.4,0,0]}});mainObj.add(mass);
            // denge pozisyonu (dikey kesik cizgi)
            for(var d=0;d<10;d++){{var dl=_mb(new THREE.SphereGeometry(.012,6,6),0x44ff44,{{p:[.4,-.7+d*.14,0]}});mainObj.add(dl);}}
            // F=-kx kuvvet oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(.65,0,0),0.5,0x4488ff,.1,.07));
            // x uzama oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(-.2,.6,0),0.6,0xff8844,.08,.06));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(-.2,.6,0),0.4,0xff8844,.08,.06));
            // zemin
            var fl=_m(new THREE.BoxGeometry(3.5,.03,.6),0x444444,{{p:[-.5,-.72,0]}});mainObj.add(fl);
            // yay sabiti k etiketi
            var kLbl=_mb(new THREE.SphereGeometry(.04,8,8),0xffdd00,{{p:[-.8,.5,0]}});mainObj.add(kLbl);
            // enerji göstergesi (potansiyel enerji)
            for(var e=0;e<5;e++){{var eBar=_m(new THREE.BoxGeometry(.08,.05+e*.06,.08),0x44ccff,{{p:[1.2,-.7+e*.15,0],op:0.4+e*0.12}});mainObj.add(eBar);}}
        }}

        scene.add(mainObj);"""

    if ci == 10:  # Kimya Laboratuvari — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _bond(p1,p2,c,r){{r=r||.03;var dx=p2[0]-p1[0],dy=p2[1]-p1[1],dz=p2[2]-p1[2];var len=Math.sqrt(dx*dx+dy*dy+dz*dz);var b=_m(new THREE.CylinderGeometry(r,r,len,8),c,{{p:[(p1[0]+p2[0])/2,(p1[1]+p2[1])/2,(p1[2]+p2[2])/2]}});b.lookAt(p2[0],p2[1],p2[2]);b.rotateX(Math.PI/2);return b;}}

        if(T==0){{
            // SU MOLEKULU H2O - oksijen + 2 hidrojen, 104.5 derece
            var O=_m(new THREE.SphereGeometry(.35,24,24),0xff3333,{{p:[0,0,0],sh:80}});mainObj.add(O);
            var H1=_m(new THREE.SphereGeometry(.25,20,20),0xffffff,{{p:[-.7,.5,0],sh:80}});mainObj.add(H1);
            var H2=_m(new THREE.SphereGeometry(.25,20,20),0xffffff,{{p:[.7,.5,0],sh:80}});mainObj.add(H2);
            mainObj.add(_bond([0,0,0],[-.7,.5,0],0xaaaaaa,.04));
            mainObj.add(_bond([0,0,0],[.7,.5,0],0xaaaaaa,.04));
            // elektron yoğunluk bulutu
            var cloud=_m(new THREE.SphereGeometry(.55,16,16),0x4488ff,{{p:[0,0,0],op:0.1}});mainObj.add(cloud);
            // aci gosterimi
            var arc=_m(new THREE.TorusGeometry(.3,.008,6,16,1.82),0xffaa33,{{p:[0,0,0],r:[0,0,0.67]}});mainObj.add(arc);
            // etiket noktalari
            var oLbl=_mb(new THREE.SphereGeometry(.05,8,8),0xff0000,{{p:[0,-.45,0]}});mainObj.add(oLbl);
        }}
        else if(T==1){{
            // KARBONDIOKSIT CO2 - dogrusal, C + 2 O, cift bag
            var C=_m(new THREE.SphereGeometry(.3,24,24),0x333333,{{p:[0,0,0],sh:60}});mainObj.add(C);
            var O1=_m(new THREE.SphereGeometry(.35,24,24),0xff3333,{{p:[-1.0,0,0],sh:80}});mainObj.add(O1);
            var O2=_m(new THREE.SphereGeometry(.35,24,24),0xff3333,{{p:[1.0,0,0],sh:80}});mainObj.add(O2);
            // cift baglar (ust ve alt cizgi)
            mainObj.add(_bond([-.15,0.06,0],[-.65,0.06,0],0xaaaaaa,.025));
            mainObj.add(_bond([-.15,-0.06,0],[-.65,-0.06,0],0xaaaaaa,.025));
            mainObj.add(_bond([.15,0.06,0],[.65,0.06,0],0xaaaaaa,.025));
            mainObj.add(_bond([.15,-0.06,0],[.65,-0.06,0],0xaaaaaa,.025));
            // 180 derece dogrusal gösterge
            var lin=_m(new THREE.CylinderGeometry(.005,.005,2.2,4),0xffaa33,{{p:[0,-.5,0],r:[0,0,1.57]}});mainObj.add(lin);
        }}
        else if(T==2){{
            // SODYUM KLORUR NaCl - kristal kafes (3x3x3)
            for(var x=-1;x<=1;x++)for(var y=-1;y<=1;y++)for(var z=-1;z<=1;z++){{
            var isNa=(x+y+z)%2==0;
            var atom=_m(new THREE.SphereGeometry(isNa?.15:.2,16,16),isNa?0x8844cc:0x44cc44,{{p:[x*.5,y*.5,z*.5],sh:80}});mainObj.add(atom);}}
            // baglantilar (kenarlar boyunca)
            for(var x=-1;x<=1;x++)for(var y=-1;y<=1;y++)for(var z=-1;z<=1;z++){{
            if(x<1)mainObj.add(_bond([x*.5,y*.5,z*.5],[(x+1)*.5,y*.5,z*.5],0x888888,.01));
            if(y<1)mainObj.add(_bond([x*.5,y*.5,z*.5],[x*.5,(y+1)*.5,z*.5],0x888888,.01));}}
        }}
        else if(T==3){{
            // DNA SARMALI - cift helis, baz ciftleri, şeker-fosfat omurgasi
            for(var i=0;i<30;i++){{var t=i*0.35;var y=-1.5+i*0.1;
            // omurga 1
            var x1=Math.cos(t)*0.5,z1=Math.sin(t)*0.5;
            var s1=_m(new THREE.SphereGeometry(.06,8,8),0x4488cc,{{p:[x1,y,z1]}});mainObj.add(s1);
            // omurga 2
            var x2=Math.cos(t+3.14)*0.5,z2=Math.sin(t+3.14)*0.5;
            var s2=_m(new THREE.SphereGeometry(.06,8,8),0xcc4488,{{p:[x2,y,z2]}});mainObj.add(s2);
            // baz ciftleri (her 3'te bir)
            if(i%3==0){{var bazClr=[0x44cc44,0xffaa33,0xff4444,0x4444ff];
            mainObj.add(_bond([x1,y,z1],[x2,y,z2],bazClr[i%4],.025));}}
            // omurga baglantilari
            if(i>0){{var pt=i-1;var ptt=pt*0.35;var py=-1.5+pt*0.1;
            mainObj.add(_bond([Math.cos(ptt)*0.5,py,Math.sin(ptt)*0.5],[x1,y,z1],0x4488cc,.015));
            mainObj.add(_bond([Math.cos(ptt+3.14)*0.5,py,Math.sin(ptt+3.14)*0.5],[x2,y,z2],0xcc4488,.015));}}}}
        }}
        else if(T==4){{
            // BENZEN HALKASI C6H6 - altıgen, alternan cift bag
            var R=0.7;
            for(var i=0;i<6;i++){{var ang=i*1.047;var nx=(i+1)%6;var nAng=nx*1.047;
            // karbon atomlari
            var cx=Math.cos(ang)*R,cy=Math.sin(ang)*R;
            var C=_m(new THREE.SphereGeometry(.15,16,16),0x333333,{{p:[cx,cy,0],sh:60}});mainObj.add(C);
            // C-C baglari
            mainObj.add(_bond([cx,cy,0],[Math.cos(nAng)*R,Math.sin(nAng)*R,0],0x888888,.03));
            // alternan cift bag (iç)
            if(i%2==0){{mainObj.add(_bond([Math.cos(ang)*R*.8,Math.sin(ang)*R*.8,0],[Math.cos(nAng)*R*.8,Math.sin(nAng)*R*.8,0],0xaaaa44,.015));}}
            // hidrojen atomlari (dış)
            var hx=Math.cos(ang)*1.15,hy=Math.sin(ang)*1.15;
            var H=_m(new THREE.SphereGeometry(.1,12,12),0xffffff,{{p:[hx,hy,0],sh:80}});mainObj.add(H);
            mainObj.add(_bond([cx,cy,0],[hx,hy,0],0xcccccc,.02));}}
            // delokalize elektron bulutu
            var pi=_m(new THREE.TorusGeometry(.55,.1,8,32),0x4488ff,{{p:[0,0,0],op:0.1}});mainObj.add(pi);
        }}
        else if(T==5){{
            // METAN CH4 - tetraedral, C + 4 H
            var C=_m(new THREE.SphereGeometry(.3,24,24),0x333333,{{p:[0,0,0],sh:60}});mainObj.add(C);
            var hPos=[[0,.8,.3],[-.75,-.35,.3],[.75,-.35,.3],[0,.1,-.8]];
            for(var h=0;h<4;h++){{var H=_m(new THREE.SphereGeometry(.2,16,16),0xffffff,{{p:hPos[h],sh:80}});mainObj.add(H);
            mainObj.add(_bond([0,0,0],hPos[h],0xaaaaaa,.035));}}
            // tetraedral aci gosterimi
            var tetArc=_m(new THREE.TorusGeometry(.35,.006,6,16,.95),0xffaa33,{{p:[0,0,0],r:[0.3,0,-0.4]}});mainObj.add(tetArc);
        }}
        else if(T==6){{
            // ETANOL C2H5OH - 2 karbon + OH grubu
            // C1
            var C1=_m(new THREE.SphereGeometry(.22,20,20),0x333333,{{p:[-.5,0,0],sh:60}});mainObj.add(C1);
            // C2
            var C2=_m(new THREE.SphereGeometry(.22,20,20),0x333333,{{p:[.5,0,0],sh:60}});mainObj.add(C2);
            mainObj.add(_bond([-.5,0,0],[.5,0,0],0x888888,.04));
            // OH grubu
            var O=_m(new THREE.SphereGeometry(.25,20,20),0xff3333,{{p:[1.2,.4,0],sh:80}});mainObj.add(O);
            mainObj.add(_bond([.5,0,0],[1.2,.4,0],0xaaaaaa,.03));
            var Hoh=_m(new THREE.SphereGeometry(.15,14,14),0xffffff,{{p:[1.7,.7,0],sh:80}});mainObj.add(Hoh);
            mainObj.add(_bond([1.2,.4,0],[1.7,.7,0],0xcccccc,.02));
            // C1 hidrojenleri (3)
            var c1h=[[-.5,.6,.3],[-.5,.6,-.3],[-1.1,-.2,0]];
            for(var h=0;h<3;h++){{mainObj.add(_m(new THREE.SphereGeometry(.15,12,12),0xffffff,{{p:c1h[h]}}));mainObj.add(_bond([-.5,0,0],c1h[h],0xcccccc,.02));}}
            // C2 hidrojenleri (2)
            var c2h=[[.5,.6,.3],[.5,-.6,.3]];
            for(var h=0;h<2;h++){{mainObj.add(_m(new THREE.SphereGeometry(.15,12,12),0xffffff,{{p:c2h[h]}}));mainObj.add(_bond([.5,0,0],c2h[h],0xcccccc,.02));}}
        }}
        else if(T==7){{
            // GLUKOZ C6H12O6 - halka formu (piranoz)
            var R=0.6;
            // 5 karbon + 1 oksijen halka
            var ringAtoms=[];
            for(var i=0;i<6;i++){{var ang=i*1.047;var px=Math.cos(ang)*R,py=Math.sin(ang)*R;
            var isO=(i==0);var at=_m(new THREE.SphereGeometry(isO?.2:.18,16,16),isO?0xff3333:0x333333,{{p:[px,py,0],sh:isO?80:60}});
            mainObj.add(at);ringAtoms.push([px,py,0]);
            // halka baglari
            var nx=(i+1)%6;var nAng=nx*1.047;
            mainObj.add(_bond([px,py,0],[Math.cos(nAng)*R,Math.sin(nAng)*R,0],0x888888,.025));
            // OH gruplari (karbonlara)
            if(!isO){{var ohAng=ang+0.5;var ox=px+Math.cos(ohAng)*.45,oy=py+Math.sin(ohAng)*.45;
            var oh=_m(new THREE.SphereGeometry(.12,10,10),0xff4444,{{p:[ox,oy,.15],op:0.8}});mainObj.add(oh);
            mainObj.add(_bond([px,py,0],[ox,oy,.15],0xcc8888,.015));}}}}
            // CH2OH kolu
            mainObj.add(_bond(ringAtoms[1],[ringAtoms[1][0]+.4,ringAtoms[1][1]+.5,.2],0x888888,.02));
            var ch2oh=_m(new THREE.SphereGeometry(.15,10,10),0x333333,{{p:[ringAtoms[1][0]+.4,ringAtoms[1][1]+.5,.2]}});mainObj.add(ch2oh);
        }}
        else if(T==8){{
            // PROTEIN YAPISI - alfa helis + beta tabaka
            // alfa helis (spiral)
            for(var i=0;i<25;i++){{var t=i*0.5;var px=Math.cos(t)*0.4;var py=-1.2+i*0.1;var pz=Math.sin(t)*0.4;
            var aa=_m(new THREE.SphereGeometry(.08,10,10),i%4==0?0xff4444:i%4==1?0x4444ff:i%4==2?0x44ff44:0xffaa44,{{p:[px,py,pz]}});mainObj.add(aa);
            if(i>0){{var pt=i-1;var ptt=pt*0.5;mainObj.add(_bond([Math.cos(ptt)*0.4,-1.2+pt*0.1,Math.sin(ptt)*0.4],[px,py,pz],0xcccccc,.015));}}}}
            // beta tabaka (sag tarafta)
            for(var s=0;s<3;s++){{for(var r=0;r<6;r++){{
            var bx=1.0+s*0.3;var by=-0.8+r*0.25;
            var bAt=_m(new THREE.SphereGeometry(.06,8,8),0x44aaff,{{p:[bx,by,0]}});mainObj.add(bAt);}}
            // ok yonleri (yukari/asagi alternan)
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,s%2?1:-1,0),new THREE.Vector3(1.0+s*0.3,s%2?-1.0:0.5,0),0.3,0xffaa33,.06,.04));}}
            // H-bag noktalari
            for(var h=0;h<4;h++){{var hb=_mb(new THREE.SphereGeometry(.025,6,6),0xff8844,{{p:[1.15+h%2*.3,-.5+h*.3,0]}});mainObj.add(hb);}}
        }}
        else if(T==9){{
            // POLIMER ZINCIRI - tekrarlayan monomer birimleri
            for(var m=0;m<12;m++){{var mx=-2.5+m*0.42;var my=Math.sin(m*0.8)*0.2;
            var monomer=_m(new THREE.SphereGeometry(.12,12,12),m%3==0?0xff4444:m%3==1?0x4444ff:0x44ff44,{{p:[mx,my,0],sh:70}});mainObj.add(monomer);
            if(m>0){{var pmx=-2.5+(m-1)*0.42;var pmy=Math.sin((m-1)*0.8)*0.2;
            mainObj.add(_bond([pmx,pmy,0],[mx,my,0],0x888888,.025));}}
            // yan gruplar (her 2. monomere)
            if(m%2==0){{var sg=_m(new THREE.SphereGeometry(.07,8,8),0xffaa44,{{p:[mx,my+.25,0]}});mainObj.add(sg);
            mainObj.add(_bond([mx,my,0],[mx,my+.25,0],0xaaaaaa,.012));}}}}
            // tekrar birimi gosterimi
            var rep=_mb(new THREE.BoxGeometry(.8,.6,.02),0xffdd44,{{p:[-.5,0,0.1],op:0.15}});mainObj.add(rep);
        }}
        else if(T==10){{
            // DENEY TUPU - cam tup, sıvı, agiz, tutacak
            var tube=_m(new THREE.CylinderGeometry(.12,.12,1.6,20),0xccddee,{{p:[0,.2,0],op:0.3,sh:100}});mainObj.add(tube);
            // alt yuvarlak (hemisfer)
            var bottom=_m(new THREE.SphereGeometry(.12,20,20,0,6.28,1.57,1.57),0xccddee,{{p:[0,-.6,0],op:0.3,sh:100}});mainObj.add(bottom);
            // agiz halka
            var rim=_m(new THREE.TorusGeometry(.14,.02,8,20),0xccddee,{{p:[0,1.0,0],r:[1.57,0,0]}});mainObj.add(rim);
            // sıvı
            var liq=_m(new THREE.CylinderGeometry(.1,.1,.6,16),0x4488ff,{{p:[0,-.1,0],op:0.5}});mainObj.add(liq);
            // kabarciklar
            for(var b=0;b<5;b++){{var bub=_m(new THREE.SphereGeometry(.02+b*.005,8,8),0x88ccff,{{p:[(Math.random()-.5)*.08,-.2+b*.15,0],op:0.4}});mainObj.add(bub);}}
            // tutacak/stand
            var clamp=_m(new THREE.TorusGeometry(.15,.025,6,16),0x888888,{{p:[0,.5,0],r:[1.57,0,0],sh:80}});mainObj.add(clamp);
            var rod=_m(new THREE.CylinderGeometry(.02,.02,.8,6),0x888888,{{p:[.2,.5,0],r:[0,0,1.57]}});mainObj.add(rod);
        }}
        else if(T==11){{
            // ERLENMAYER - konik flask, boyun, sıvı, olcek cizgileri
            var body=_m(new THREE.CylinderGeometry(.1,.45,.9,20),0xccddee,{{p:[0,-.2,0],op:0.3,sh:100}});mainObj.add(body);
            var neck=_m(new THREE.CylinderGeometry(.08,.1,.45,16),0xccddee,{{p:[0,.4,0],op:0.3,sh:100}});mainObj.add(neck);
            var rim=_m(new THREE.TorusGeometry(.09,.015,8,16),0xccddee,{{p:[0,.62,0],r:[1.57,0,0]}});mainObj.add(rim);
            // sıvı
            var liq=_m(new THREE.CylinderGeometry(.08,.38,.5,20),0x44dd44,{{p:[0,-.3,0],op:0.45}});mainObj.add(liq);
            // olcek cizgileri
            for(var s=0;s<5;s++){{var sc=_m(new THREE.BoxGeometry(.08,.005,.01),0xffffff,{{p:[.35-s*.03,-.55+s*.12,0]}});mainObj.add(sc);}}
            // taban
            var base=_m(new THREE.CylinderGeometry(.46,.46,.03,20),0xccddee,{{p:[0,-.66,0],op:0.4}});mainObj.add(base);
        }}
        else if(T==12){{
            // BURET - uzun cam tup, musluk, olcek, stant
            var tube=_m(new THREE.CylinderGeometry(.04,.04,2.2,12),0xccddee,{{p:[0,.3,0],op:0.35,sh:100}});mainObj.add(tube);
            var topOpen=_m(new THREE.CylinderGeometry(.05,.04,.05,12),0xccddee,{{p:[0,1.42,0]}});mainObj.add(topOpen);
            // musluk
            var tap=_m(new THREE.CylinderGeometry(.015,.015,.12,8),0x2255cc,{{p:[.06,-.75,0],r:[0,0,1.57]}});mainObj.add(tap);
            var tapH=_m(new THREE.BoxGeometry(.06,.02,.04),0x2255cc,{{p:[.13,-.75,0]}});mainObj.add(tapH);
            // çıkış üçu
            var tip=_m(new THREE.CylinderGeometry(.015,.01,.15,8),0xccddee,{{p:[0,-.9,0]}});mainObj.add(tip);
            // sıvı (içeride)
            var liq=_m(new THREE.CylinderGeometry(.035,.035,1.2,12),0xff6644,{{p:[0,.1,0],op:0.4}});mainObj.add(liq);
            // olcek cizgileri
            for(var s=0;s<15;s++){{var sc=_m(new THREE.BoxGeometry(s%5==0?.06:.03,.003,.01),0x333333,{{p:[.04,-.4+s*.12,0]}});mainObj.add(sc);}}
            // stant
            var stand=_m(new THREE.CylinderGeometry(.025,.03,2.6,8),0x888888,{{p:[-.15,.1,0]}});mainObj.add(stand);
            var clmp=_m(new THREE.TorusGeometry(.05,.015,6,12),0x888888,{{p:[0,.8,0],r:[1.57,0,0]}});mainObj.add(clmp);
        }}
        else if(T==13){{
            // DISTILASYON - flask, kondenser, toplama, baglanti
            // kaynatma flaski
            var flask=_m(new THREE.SphereGeometry(.35,20,20),0xccddee,{{p:[-1.0,-.2,0],op:0.3,sh:100}});mainObj.add(flask);
            var fNeck=_m(new THREE.CylinderGeometry(.06,.08,.4,12),0xccddee,{{p:[-1.0,.2,0],op:0.3}});mainObj.add(fNeck);
            // sıvı (içeride)
            var fLiq=_m(new THREE.SphereGeometry(.28,16,16),0x4488ff,{{p:[-1.0,-.25,0],op:0.4}});mainObj.add(fLiq);
            // baglanti borusu (egik)
            var conn=_m(new THREE.CylinderGeometry(.04,.04,1.2,8),0xccddee,{{p:[-.3,.5,0],r:[0,0,0.7],op:0.3}});mainObj.add(conn);
            // kondenser (dış ceket)
            var cond=_m(new THREE.CylinderGeometry(.12,.12,1.4,14),0xccddee,{{p:[.7,.0,0],r:[0,0,0.3],op:0.25}});mainObj.add(cond);
            // iç boru
            var inner=_m(new THREE.CylinderGeometry(.04,.04,1.5,8),0xccddee,{{p:[.7,.0,0],r:[0,0,0.3],op:0.3}});mainObj.add(inner);
            // su giriş/çıkış
            var wIn=_m(new THREE.CylinderGeometry(.02,.02,.15,6),0x4488ff,{{p:[.5,-.12,0],r:[0,0,1.57]}});mainObj.add(wIn);
            var wOut=_m(new THREE.CylinderGeometry(.02,.02,.15,6),0xff4444,{{p:[.9,.12,0],r:[0,0,1.57]}});mainObj.add(wOut);
            // toplama flaski
            var cFlask=_m(new THREE.CylinderGeometry(.08,.2,.5,14),0xccddee,{{p:[1.4,-.5,0],op:0.3}});mainObj.add(cFlask);
            // toplanan sıvı
            var cLiq=_m(new THREE.CylinderGeometry(.06,.18,.2,14),0x44ccff,{{p:[1.4,-.55,0],op:0.45}});mainObj.add(cLiq);
            // isitiçi
            var heat=_m(new THREE.CylinderGeometry(.3,.3,.06,16),0x444444,{{p:[-1.0,-.6,0]}});mainObj.add(heat);
            var coil=_m(new THREE.TorusGeometry(.2,.015,6,24),0xff4444,{{p:[-1.0,-.55,0],r:[1.57,0,0],em:0x661111}});mainObj.add(coil);
        }}
        else if(T==14){{
            // BEHER - geniş agizli cam kap, sıvı, gagasi
            var body=_m(new THREE.CylinderGeometry(.4,.35,.9,20),0xccddee,{{p:[0,-.1,0],op:0.3,sh:100}});mainObj.add(body);
            // agiz (ust)
            var rim=_m(new THREE.TorusGeometry(.4,.015,8,20),0xccddee,{{p:[0,.35,0],r:[1.57,0,0]}});mainObj.add(rim);
            // gaga (dokme agzi)
            var spout=_m(new THREE.ConeGeometry(.06,.1,4),0xccddee,{{p:[.4,.38,0],r:[0,0,-.5],op:0.4}});mainObj.add(spout);
            // sıvı
            var liq=_m(new THREE.CylinderGeometry(.37,.32,.5,20),0x44aaff,{{p:[0,-.15,0],op:0.45}});mainObj.add(liq);
            // olcek cizgileri
            for(var s=0;s<6;s++){{var sc=_m(new THREE.BoxGeometry(.06,.004,.01),0xffffff,{{p:[.36,-.5+s*.12,0]}});mainObj.add(sc);}}
            // karistirma cubugu
            var stir=_m(new THREE.CylinderGeometry(.015,.015,.7,6),0xccddee,{{p:[.1,.15,0],r:[0,0,0.15],op:0.5}});mainObj.add(stir);
            // taban
            var base=_m(new THREE.CylinderGeometry(.36,.36,.03,20),0xccddee,{{p:[0,-.56,0],op:0.4}});mainObj.add(base);
        }}
        else if(T==15){{
            // SANTRIFUJ - govde, rotor, tupler, kapak
            var body=_m(new THREE.CylinderGeometry(.7,.75,.5,24),0xdddddd,{{p:[0,-.1,0],sh:60}});mainObj.add(body);
            // kapak
            var lid=_m(new THREE.CylinderGeometry(.68,.7,.06,24),0xcccccc,{{p:[0,.2,0],sh:70}});mainObj.add(lid);
            // rotor (içeride gorune)
            var rotor=_m(new THREE.CylinderGeometry(.5,.5,.08,24),0x888888,{{p:[0,0,0],sh:80}});mainObj.add(rotor);
            // tup yuvalari
            for(var t=0;t<8;t++){{var ta=t*0.785;var tx=Math.cos(ta)*0.35,tz=Math.sin(ta)*0.35;
            var slot=_m(new THREE.CylinderGeometry(.04,.04,.15,8),0x666666,{{p:[tx,.05,tz]}});mainObj.add(slot);
            // tup (bazi dolu)
            if(t<5){{var tb=_m(new THREE.CylinderGeometry(.03,.03,.12,8),t%2?0xff4444:0x4488ff,{{p:[tx,.1,tz],op:0.6}});mainObj.add(tb);}}}}
            // kontrol paneli
            var panel=_m(new THREE.BoxGeometry(.3,.15,.02),0x333333,{{p:[0,.0,.76]}});mainObj.add(panel);
            var btn=_m(new THREE.SphereGeometry(.03,8,8),0x44ff44,{{p:[-.05,.03,.77],em:0x228822}});mainObj.add(btn);
            // donme oklari
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(-.2,.35,0),0.4,0xff8844,.06,.04));
        }}
        else if(T==16){{
            // PIPET - ince cam boru, balonlu, olcekli
            var tube=_m(new THREE.CylinderGeometry(.025,.025,2.0,10),0xccddee,{{p:[0,.2,0],op:0.35,sh:100}});mainObj.add(tube);
            // ust balon (lastik)
            var bulb=_m(new THREE.SphereGeometry(.1,14,14),0xcc4444,{{p:[0,1.25,0]}});mainObj.add(bulb);
            // alt üçuz sivrilme
            var tip=_m(new THREE.ConeGeometry(.025,.15,8),0xccddee,{{p:[0,-.85,0],r:[Math.PI,0,0],op:0.4}});mainObj.add(tip);
            // sıvı içeride
            var liq=_m(new THREE.CylinderGeometry(.02,.02,.6,8),0x4488ff,{{p:[0,-.1,0],op:0.5}});mainObj.add(liq);
            // olcek cizgileri
            for(var s=0;s<10;s++){{var sc=_m(new THREE.BoxGeometry(s%5==0?.05:.03,.002,.01),0x333333,{{p:[.03,-.5+s*.1,0]}});mainObj.add(sc);}}
        }}
        else if(T==17){{
            // BUNSEN BEKI - govde, hava deligi, alev, gaz borusu
            var base=_m(new THREE.CylinderGeometry(.25,.3,.08,20),0x333333,{{p:[0,-.7,0],sh:60}});mainObj.add(base);
            var body=_m(new THREE.CylinderGeometry(.06,.08,.8,14),0xaaaaaa,{{p:[0,-.25,0],sh:80}});mainObj.add(body);
            // hava deligi halka
            var airRing=_m(new THREE.TorusGeometry(.09,.02,8,16),0x888888,{{p:[0,-.55,0],r:[1.57,0,0]}});mainObj.add(airRing);
            // boru agzi
            var top=_m(new THREE.CylinderGeometry(.065,.06,.04,12),0xaaaaaa,{{p:[0,.15,0]}});mainObj.add(top);
            // iç mavi alev (kon)
            var innerFlame=_m(new THREE.ConeGeometry(.04,.5,12),0x2244ff,{{p:[0,.45,0],em:0x112288,op:0.7}});mainObj.add(innerFlame);
            // dış alev (büyük kon)
            var outerFlame=_m(new THREE.ConeGeometry(.07,.7,12),0xff8800,{{p:[0,.5,0],em:0x884400,op:0.4}});mainObj.add(outerFlame);
            // parlama
            var glow=_m(new THREE.SphereGeometry(.15,10,10),0xffaa44,{{p:[0,.4,0],op:0.15,em:0x664400}});mainObj.add(glow);
            // gaz borusu
            var gasTube=_m(new THREE.CylinderGeometry(.02,.02,.6,8),0xaa8844,{{p:[-.4,-.7,0],r:[0,0,1.57]}});mainObj.add(gasTube);
            // gaz vana
            var valve=_m(new THREE.CylinderGeometry(.03,.03,.06,8),0x666666,{{p:[-.15,-.55,0],r:[0,0,1.57]}});mainObj.add(valve);
        }}
        else if(T==18){{
            // KRISTAL YAPI - birim hüçre, atomlar, baglar (FCC/BCC)
            // BCC kristal kafes
            for(var x=0;x<3;x++)for(var y=0;y<3;y++)for(var z=0;z<3;z++){{
            var ax=(-1+x)*0.6,ay=(-1+y)*0.6,az=(-1+z)*0.6;
            var corner=_m(new THREE.SphereGeometry(.08,12,12),0x4488cc,{{p:[ax,ay,az],sh:80}});mainObj.add(corner);}}
            // merkez atomlari (BCC)
            for(var x=0;x<2;x++)for(var y=0;y<2;y++)for(var z=0;z<2;z++){{
            var cx=(-0.5+x)*0.6,cy=(-0.5+y)*0.6,cz=(-0.5+z)*0.6;
            var center=_m(new THREE.SphereGeometry(.1,12,12),0xff6644,{{p:[cx,cy,cz],sh:80}});mainObj.add(center);}}
            // kenar baglari (birim hüçre)
            var u=0.6;
            for(var i=-1;i<=0;i++)for(var j=-1;j<=0;j++){{
            mainObj.add(_bond([i*u,j*u,-u],[(i+1)*u,j*u,-u],0x888888,.008));
            mainObj.add(_bond([i*u,j*u,-u],[i*u,(j+1)*u,-u],0x888888,.008));
            mainObj.add(_bond([i*u,j*u,-u],[i*u,j*u,0],0x888888,.008));}}
            // birim hüçre vurgulama
            var cell=_mb(new THREE.BoxGeometry(.6,.6,.6),0xffdd44,{{p:[-.3,-.3,-.3],wf:true,op:0.4}});mainObj.add(cell);
        }}
        else if(T==19){{
            // AMONYAK NH3 - piramidal, N + 3 H
            var N=_m(new THREE.SphereGeometry(.3,24,24),0x4444ff,{{p:[0,.2,0],sh:80}});mainObj.add(N);
            var hPos=[[-.6,-.3,.3],[.6,-.3,.3],[0,-.3,-.6]];
            for(var h=0;h<3;h++){{var H=_m(new THREE.SphereGeometry(.2,16,16),0xffffff,{{p:hPos[h],sh:80}});mainObj.add(H);
            mainObj.add(_bond([0,.2,0],hPos[h],0xaaaaaa,.035));}}
            // yalıtkan elektron cifti (ust)
            var lp=_m(new THREE.SphereGeometry(.12,10,10),0xffdd44,{{p:[0,.7,0],op:0.3}});mainObj.add(lp);
            // piramidal sekil gosterimi
            for(var i=0;i<3;i++){{var n=(i+1)%3;
            mainObj.add(_bond(hPos[i],hPos[n],0x888888,.01));}}
            // aci gosterimi
            var arc=_m(new THREE.TorusGeometry(.3,.006,6,16,.8),0xffaa33,{{p:[0,.2,0],r:[0.8,0,0]}});mainObj.add(arc);
        }}

        scene.add(mainObj);"""

    if ci == 11:  # Uzay Teknolojisi — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        if(T==0){{
            // ROKET - govde, bürün, kanatlar, kademeler, nözül, alev
            var s1=_m(new THREE.CylinderGeometry(.35,.4,1.2,20),0xdddddd,{{p:[0,-.5,0],sh:80}});mainObj.add(s1);
            var s2=_m(new THREE.CylinderGeometry(.3,.35,.8,20),0xcccccc,{{p:[0,.3,0],sh:80}});mainObj.add(s2);
            var s3=_m(new THREE.CylinderGeometry(.22,.3,.5,16),0xbbbbbb,{{p:[0,.85,0],sh:80}});mainObj.add(s3);
            var nose=_m(new THREE.ConeGeometry(.22,.5,16),0xff4444,{{p:[0,1.35,0]}});mainObj.add(nose);
            // kademe ayirma cizgileri
            var sep1=_m(new THREE.TorusGeometry(.36,.02,6,20),0x444444,{{p:[0,.1,0],r:[1.57,0,0]}});mainObj.add(sep1);
            var sep2=_m(new THREE.TorusGeometry(.31,.015,6,16),0x444444,{{p:[0,.7,0],r:[1.57,0,0]}});mainObj.add(sep2);
            // 4 kanat
            for(var f=0;f<4;f++){{var fin=_m(new THREE.BoxGeometry(.5,.45,.04),0x888888,{{p:[Math.sin(f*1.57)*.4,-1.0,Math.cos(f*1.57)*.4],r:[0,f*1.57,0.15]}});mainObj.add(fin);}}
            // nözül
            var noz=_m(new THREE.CylinderGeometry(.3,.2,.15,16),0x555555,{{p:[0,-1.15,0],sh:90}});mainObj.add(noz);
            // alev
            var fl1=_m(new THREE.ConeGeometry(.25,1.0,12),0xff6600,{{p:[0,-1.75,0],r:[Math.PI,0,0],em:0xcc4400,op:0.8}});mainObj.add(fl1);
            var fl2=_m(new THREE.ConeGeometry(.12,.7,8),0xffcc00,{{p:[0,-1.55,0],r:[Math.PI,0,0],em:0xcc8800,op:0.7}});mainObj.add(fl2);
        }}
        else if(T==1){{
            // UZAY MEKIGI - govde, kanatlar, kuyruk, isı kalkani, kargo kapagi
            var body=_m(new THREE.CylinderGeometry(.2,.25,2.0,16),0xeeeeee,{{p:[0,0,0],r:[0,0,0],sh:80}});mainObj.add(body);
            var nose=_m(new THREE.SphereGeometry(.2,16,16,0,6.28,0,1.57),0x333333,{{p:[0,1.0,0],sh:50}});mainObj.add(nose);
            // delta kanatlar
            var wingL=_m(new THREE.BoxGeometry(1.0,.03,.5),0xeeeeee,{{p:[-.6,-.3,0],r:[0,0,-0.1]}});mainObj.add(wingL);
            var wingR=_m(new THREE.BoxGeometry(1.0,.03,.5),0xeeeeee,{{p:[.6,-.3,0],r:[0,0,0.1]}});mainObj.add(wingR);
            // dikey kuyruk
            var tail=_m(new THREE.BoxGeometry(.04,.6,.3),0xeeeeee,{{p:[0,.1,.2]}});mainObj.add(tail);
            // motor nözülleri (3)
            for(var n=0;n<3;n++){{var nz=_m(new THREE.CylinderGeometry(.08,.06,.1,10),0x555555,{{p:[(n-1)*.12,-1.0,0],sh:90}});mainObj.add(nz);}}
            // kargo kapagi cizgisi
            var cargo=_m(new THREE.BoxGeometry(.15,.8,.01),0xcccccc,{{p:[0,.2,.22]}});mainObj.add(cargo);
            // isi kalkani (alt)
            var heat=_m(new THREE.CylinderGeometry(.26,.26,.05,16),0x222222,{{p:[0,-1.0,0]}});mainObj.add(heat);
        }}
        else if(T==2){{
            // UZAY ISTASYONU - moduller, güneş panelleri, truss
            // merkez modul
            var hub=_m(new THREE.CylinderGeometry(.15,.15,.5,12),0xcccccc,{{p:[0,0,0],r:[0,0,1.57],sh:70}});mainObj.add(hub);
            // laboratuvar modulleri
            for(var m=0;m<4;m++){{var ang=m*1.57;var mod=_m(new THREE.CylinderGeometry(.12,.12,.7,10),0xbbbbbb,{{p:[Math.cos(ang)*.4,0,Math.sin(ang)*.4],r:[0,0,1.57]}});mainObj.add(mod);}}
            // truss (ana kirish)
            var truss=_m(new THREE.BoxGeometry(3.5,.04,.04),0x888888,{{p:[0,0,0]}});mainObj.add(truss);
            // güneş panelleri (4 cift)
            for(var s=0;s<4;s++){{var sx=(s-1.5)*0.9;
            var pan=_m(new THREE.BoxGeometry(.6,.02,.35),0x223388,{{p:[sx,.15,0],sh:80}});mainObj.add(pan);
            var pan2=_m(new THREE.BoxGeometry(.6,.02,.35),0x223388,{{p:[sx,-.15,0],sh:80}});mainObj.add(pan2);}}
            // radyator panelleri
            var rad1=_m(new THREE.BoxGeometry(.3,.02,.5),0xdddddd,{{p:[-.8,0,.4]}});mainObj.add(rad1);
            var rad2=_m(new THREE.BoxGeometry(.3,.02,.5),0xdddddd,{{p:[.8,0,.4]}});mainObj.add(rad2);
            // kenetlenme portu
            var dock=_m(new THREE.CylinderGeometry(.08,.08,.15,10),0xaaaaaa,{{p:[0,0,.35]}});mainObj.add(dock);
        }}
        else if(T==3){{
            // UYDU - govde, güneş panelleri, anten, sensor
            var body=_m(new THREE.BoxGeometry(.5,.4,.35),0xcccccc,{{p:[0,0,0],sh:70}});mainObj.add(body);
            // güneş panelleri
            var panL=_m(new THREE.BoxGeometry(.9,.02,.5),0x223388,{{p:[-.75,0,0],sh:80}});mainObj.add(panL);
            var panR=_m(new THREE.BoxGeometry(.9,.02,.5),0x223388,{{p:[.75,0,0],sh:80}});mainObj.add(panR);
            // panel baglanti kolları
            var armL=_m(new THREE.BoxGeometry(.1,.02,.04),0x888888,{{p:[-.32,0,0]}});mainObj.add(armL);
            var armR=_m(new THREE.BoxGeometry(.1,.02,.04),0x888888,{{p:[.32,0,0]}});mainObj.add(armR);
            // canak anten
            var dışh=_m(new THREE.SphereGeometry(.18,16,10,0,6.28,0,1.2),0xdddddd,{{p:[0,.3,0],sh:80}});mainObj.add(dışh);
            var feed=_m(new THREE.CylinderGeometry(.015,.015,.2,6),0xaaaaaa,{{p:[0,.4,0]}});mainObj.add(feed);
            // alt sensor
            var sensor=_m(new THREE.CylinderGeometry(.08,.08,.1,10),0x444444,{{p:[0,-.25,0]}});mainObj.add(sensor);
            var lens=_m(new THREE.SphereGeometry(.06,10,10),0x224488,{{p:[0,-.32,0],sh:100}});mainObj.add(lens);
        }}
        else if(T==4){{
            // MARS ROVER - govde, 6 tekerlek, mast, kamera, robotik kol
            var body=_m(new THREE.BoxGeometry(.7,.25,.5),0xbb8844,{{p:[0,0,0]}});mainObj.add(body);
            // 6 tekerlek (rocker-bogie)
            var wPos=[[-0.3,-.2,.3],[0,-.2,.3],[.3,-.2,.3],[-0.3,-.2,-.3],[0,-.2,-.3],[.3,-.2,-.3]];
            for(var w=0;w<6;w++){{var wh=_m(new THREE.CylinderGeometry(.1,.1,.06,16),0x444444,{{p:wPos[w],r:[1.57,0,0],sh:50}});mainObj.add(wh);
            var spoke=_m(new THREE.BoxGeometry(.015,.015,.18),0x666666,{{p:wPos[w],r:[1.57,0,0]}});mainObj.add(spoke);}}
            // bogie kolu
            var bogL=_m(new THREE.BoxGeometry(.5,.02,.02),0x888888,{{p:[0,-.12,.3]}});mainObj.add(bogL);
            var bogR=_m(new THREE.BoxGeometry(.5,.02,.02),0x888888,{{p:[0,-.12,-.3]}});mainObj.add(bogR);
            // mast + kamera
            var mast=_m(new THREE.CylinderGeometry(.02,.025,.4,8),0x888888,{{p:[.15,.3,0]}});mainObj.add(mast);
            var camHead=_m(new THREE.BoxGeometry(.12,.08,.1),0x666666,{{p:[.15,.52,0]}});mainObj.add(camHead);
            var camLens=_m(new THREE.SphereGeometry(.03,8,8),0x224488,{{p:[.15,.52,.06],sh:100}});mainObj.add(camLens);
            // güneş paneli
            var solar=_m(new THREE.BoxGeometry(.6,.02,.35),0x223388,{{p:[0,.15,0],sh:80}});mainObj.add(solar);
            // robotik kol
            var arm1=_m(new THREE.CylinderGeometry(.015,.015,.3,6),0x888888,{{p:[-.25,.15,.2],r:[0.5,0,0.3]}});mainObj.add(arm1);
            var arm2=_m(new THREE.CylinderGeometry(.012,.012,.2,6),0x888888,{{p:[-.35,.3,.3],r:[0.3,0,0]}});mainObj.add(arm2);
        }}
        else if(T==5){{
            // TELESKOP - ana tup, ayna/lens, montaj, tripod
            var tube=_m(new THREE.CylinderGeometry(.18,.2,1.5,16),0xdddddd,{{p:[0,.3,0],r:[0,0,0.3],sh:70}});mainObj.add(tube);
            // lens (on)
            var lens=_m(new THREE.SphereGeometry(.18,16,16),0x88bbee,{{p:[.55,.8,0],s:[1,1,.15],op:0.3,sh:100}});mainObj.add(lens);
            // gözleme üçu
            var eye=_m(new THREE.CylinderGeometry(.04,.06,.15,10),0x333333,{{p:[-.5,-.1,0],r:[0,0,0.3]}});mainObj.add(eye);
            // montaj (fork)
            var mount=_m(new THREE.BoxGeometry(.1,.3,.15),0x888888,{{p:[0,-.15,0]}});mainObj.add(mount);
            // tripod
            for(var l=0;l<3;l++){{var la=l*2.094;
            var leg=_m(new THREE.CylinderGeometry(.02,.025,.8,6),0x444444,{{p:[Math.sin(la)*.2,-.55,Math.cos(la)*.2],r:[Math.cos(la)*0.2,0,Math.sin(la)*-0.2]}});mainObj.add(leg);}}
            // bulüçu teleskop
            var finder=_m(new THREE.CylinderGeometry(.03,.04,.3,8),0xcccccc,{{p:[.1,.55,.12],r:[0,0,0.3]}});mainObj.add(finder);
        }}
        else if(T==6){{
            // UZAY KAPSULU - konik govde, isi kalkani, parasüt, pencereler
            var capsule=_m(new THREE.ConeGeometry(.5,.9,16),0xcccccc,{{p:[0,.1,0],sh:70}});mainObj.add(capsule);
            var heatShield=_m(new THREE.CylinderGeometry(.5,.5,.06,20),0x553322,{{p:[0,-.35,0]}});mainObj.add(heatShield);
            // pencereler
            for(var w=0;w<3;w++){{var wa=w*2.094;
            var win=_m(new THREE.SphereGeometry(.06,10,10),0x224488,{{p:[Math.sin(wa)*.35,.2,Math.cos(wa)*.35],sh:100}});mainObj.add(win);}}
            // ust kenetlenme portu
            var dock=_m(new THREE.CylinderGeometry(.1,.12,.1,12),0x888888,{{p:[0,.6,0]}});mainObj.add(dock);
            // parasüt (acik)
            var chute=_m(new THREE.SphereGeometry(.6,16,8,0,6.28,0,1.2),0xff6644,{{p:[0,1.4,0],op:0.4}});mainObj.add(chute);
            // parasüt ipleri
            for(var r=0;r<6;r++){{var ra=r*1.047;
            var rope=_m(new THREE.CylinderGeometry(.005,.005,.7,4),0xdddddd,{{p:[Math.sin(ra)*.2,1.0,Math.cos(ra)*.2],r:[Math.cos(ra)*0.3,0,Math.sin(ra)*-0.3]}});mainObj.add(rope);}}
        }}
        else if(T==7){{
            // GUNES PANELI - hüçre dizisi, çerçeve, montaj, kablolar
            var frame=_m(new THREE.BoxGeometry(2.0,.04,1.2),0x888888,{{p:[0,0,0]}});mainObj.add(frame);
            // hüçre gridi
            for(var x=0;x<8;x++)for(var y=0;y<5;y++){{
            var cell=_m(new THREE.BoxGeometry(.22,.02,.2),0x1a2a6c,{{p:[-.88+x*.25,.03,-.48+y*.24],sh:90}});mainObj.add(cell);
            // hüçre cizgileri
            var line=_m(new THREE.BoxGeometry(.22,.025,.003),0xaaaaaa,{{p:[-.88+x*.25,.04,-.38+y*.24]}});mainObj.add(line);}}
            // montaj kolu
            var arm=_m(new THREE.CylinderGeometry(.03,.03,.6,8),0x666666,{{p:[0,-.3,0]}});mainObj.add(arm);
            var pivot=_m(new THREE.SphereGeometry(.05,10,10),0x888888,{{p:[0,-.6,0]}});mainObj.add(pivot);
            // güneş ışıklari
            for(var r=0;r<5;r++){{mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-1+r*.5,1.0,0),0.5,0xffdd44,.06,.04));}}
        }}
        else if(T==8){{
            // UZAY GIYSISI - kask, govde, kolluklar, bacaklar, yasam destek
            // kask
            var helmet=_m(new THREE.SphereGeometry(.3,20,20),0xeeeeee,{{p:[0,1.0,0],sh:80}});mainObj.add(helmet);
            var visor=_m(new THREE.SphereGeometry(.28,16,16,0,6.28,0,1.2),0x224488,{{p:[0,1.0,0.05],sh:100}});mainObj.add(visor);
            // govde
            var torso=_m(new THREE.CylinderGeometry(.3,.25,.7,14),0xeeeeee,{{p:[0,.5,0],sh:60}});mainObj.add(torso);
            // kollar
            var armL=_m(new THREE.CylinderGeometry(.1,.08,.5,8),0xeeeeee,{{p:[-.4,.55,0],r:[0,0,0.3]}});mainObj.add(armL);
            var armR=_m(new THREE.CylinderGeometry(.1,.08,.5,8),0xeeeeee,{{p:[.4,.55,0],r:[0,0,-0.3]}});mainObj.add(armR);
            // eldivenler
            var gL=_m(new THREE.SphereGeometry(.08,10,10),0xdddddd,{{p:[-.55,.35,0]}});mainObj.add(gL);
            var gR=_m(new THREE.SphereGeometry(.08,10,10),0xdddddd,{{p:[.55,.35,0]}});mainObj.add(gR);
            // bacaklar
            var legL=_m(new THREE.CylinderGeometry(.1,.1,.6,8),0xeeeeee,{{p:[-.12,-.1,0]}});mainObj.add(legL);
            var legR=_m(new THREE.CylinderGeometry(.1,.1,.6,8),0xeeeeee,{{p:[.12,-.1,0]}});mainObj.add(legR);
            // botlar
            var bootL=_m(new THREE.BoxGeometry(.12,.1,.18),0xcccccc,{{p:[-.12,-.45,0]}});mainObj.add(bootL);
            var bootR=_m(new THREE.BoxGeometry(.12,.1,.18),0xcccccc,{{p:[.12,-.45,0]}});mainObj.add(bootR);
            // yasam destek paketi (sirt)
            var pack=_m(new THREE.BoxGeometry(.25,.35,.12),0xdddddd,{{p:[0,.5,-.18]}});mainObj.add(pack);
        }}
        else if(T==9){{
            // FIRLATMA RAMPASI - kule, rampa, roket, servis kollari
            // rampa platformu
            var pad=_m(new THREE.CylinderGeometry(.8,.9,.1,20),0x888888,{{p:[0,-1.2,0]}});mainObj.add(pad);
            // servis kulesi
            var tower=_m(new THREE.BoxGeometry(.2,.2,2.8),0xff4444,{{p:[.5,0,.0],r:[0,0,0]}});mainObj.add(tower);
            for(var l=0;l<8;l++){{var lev=_m(new THREE.BoxGeometry(.3,.02,.02),0xcc3333,{{p:[.5,-1.0+l*.35,0]}});mainObj.add(lev);}}
            // roket (basit)
            var rocket=_m(new THREE.CylinderGeometry(.15,.2,1.8,12),0xdddddd,{{p:[0,-.1,0],sh:70}});mainObj.add(rocket);
            var rNose=_m(new THREE.ConeGeometry(.15,.35,12),0xeeeeee,{{p:[0,.8,0]}});mainObj.add(rNose);
            // servis kollari
            for(var a=0;a<3;a++){{var arm=_m(new THREE.BoxGeometry(.3,.03,.03),0xcc4444,{{p:[.35,-.5+a*.5,0]}});mainObj.add(arm);}}
            // alev deflektoru
            var defl=_m(new THREE.CylinderGeometry(.5,.3,.15,16),0x555555,{{p:[0,-1.15,0]}});mainObj.add(defl);
            // duman
            for(var s=0;s<6;s++){{var sm=_m(new THREE.SphereGeometry(.15+s*.05,8,8),0xcccccc,{{p:[(Math.random()-.5)*.4,-1.3-s*.1,(Math.random()-.5)*.4],op:0.2-s*.02}});mainObj.add(sm);}}
        }}
        else if(T==10){{
            // YORUNGE - gezegen, uydu, eliptik yorunge, hiz oklari
            var planet=_m(new THREE.SphereGeometry(.5,24,24),0x4488cc,{{p:[0,0,0],sh:60}});mainObj.add(planet);
            // yorunge cizgisi
            var orbit=_m(new THREE.TorusGeometry(1.2,.01,8,64),0xffaa33,{{p:[0,0,0],r:[1.3,0,0],op:0.5}});mainObj.add(orbit);
            // uydu
            var sat=_m(new THREE.BoxGeometry(.1,.08,.06),0xcccccc,{{p:[1.2,0,0],sh:80}});mainObj.add(sat);
            var satP=_m(new THREE.BoxGeometry(.3,.01,.08),0x223388,{{p:[1.2,0,0]}});mainObj.add(satP);
            // hiz oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1),new THREE.Vector3(1.2,0,0),0.4,0x44ff44,.06,.04));
            // cekimsel kuvvet oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-1,0,0),new THREE.Vector3(1.2,0,0),0.3,0xff4444,.06,.04));
            // atmosfer
            var atm=_m(new THREE.SphereGeometry(.55,20,20),0x88ccff,{{p:[0,0,0],op:0.1}});mainObj.add(atm);
        }}
        else if(T==11){{
            // AY MODULU - inis/çıkış asamasi, bacaklar, anten, merdiven
            // inis asamasi
            var descent=_m(new THREE.CylinderGeometry(.4,.45,.3,8),0xccaa44,{{p:[0,-.15,0]}});mainObj.add(descent);
            // çıkış asamasi (ust)
            var ascent=_m(new THREE.BoxGeometry(.4,.35,.35),0xaaaaaa,{{p:[0,.2,0],sh:60}});mainObj.add(ascent);
            // pencere
            var win=_m(new THREE.SphereGeometry(.08,10,10),0x224488,{{p:[0,.25,.2],sh:100}});mainObj.add(win);
            // 4 bacak
            for(var l=0;l<4;l++){{var la=l*1.57+0.785;
            var leg=_m(new THREE.CylinderGeometry(.02,.02,.5,6),0xaaaa44,{{p:[Math.sin(la)*.5,-.4,Math.cos(la)*.5],r:[Math.cos(la)*0.3,0,-Math.sin(la)*0.3]}});mainObj.add(leg);
            var foot=_m(new THREE.CylinderGeometry(.12,.15,.03,8),0xaaaa44,{{p:[Math.sin(la)*.6,-.65,Math.cos(la)*.6]}});mainObj.add(foot);}}
            // anten
            var ant=_m(new THREE.CylinderGeometry(.01,.01,.4,6),0xdddddd,{{p:[.15,.45,0]}});mainObj.add(ant);
            var dışh=_m(new THREE.SphereGeometry(.1,10,8,0,6.28,0,1.2),0xdddddd,{{p:[.15,.65,0]}});mainObj.add(dışh);
            // merdiven
            for(var s=0;s<5;s++){{var step=_m(new THREE.BoxGeometry(.1,.015,.04),0xaaaa44,{{p:[0,-.5+s*.1,.4]}});mainObj.add(step);}}
        }}
        else if(T==12){{
            // UZAY TELESKOBU - Hubble benzeri, güneş panelleri, anten
            var tube=_m(new THREE.CylinderGeometry(.3,.3,1.8,20),0xcccccc,{{p:[0,0,0],sh:70}});mainObj.add(tube);
            // on aciklik (siyah)
            var aperture=_m(new THREE.CylinderGeometry(.28,.28,.05,20),0x111111,{{p:[0,.92,0]}});mainObj.add(aperture);
            // güneş panelleri
            var spL=_m(new THREE.BoxGeometry(.8,.02,.5),0x223388,{{p:[-.7,-.2,0],sh:80}});mainObj.add(spL);
            var spR=_m(new THREE.BoxGeometry(.8,.02,.5),0x223388,{{p:[.7,-.2,0],sh:80}});mainObj.add(spR);
            // anten dizisi
            var ant1=_m(new THREE.SphereGeometry(.12,12,8,0,6.28,0,1.2),0xdddddd,{{p:[0,.4,.35]}});mainObj.add(ant1);
            var ant2=_m(new THREE.CylinderGeometry(.01,.01,.2,6),0xcccccc,{{p:[0,.5,.35]}});mainObj.add(ant2);
            // alt ekipman alani
            var equip=_m(new THREE.BoxGeometry(.35,.3,.25),0xbbbbbb,{{p:[0,-.7,.15]}});mainObj.add(equip);
            // termal koruma
            var thermal=_m(new THREE.CylinderGeometry(.32,.32,1.82,20),0xdddddd,{{p:[0,0,0],op:0.2}});mainObj.add(thermal);
        }}
        else if(T==13){{
            // RADYO ANTENI - canak, besleme, montaj, ayak
            var dışh=_m(new THREE.SphereGeometry(1.0,24,16,0,6.28,0,1.0),0xdddddd,{{p:[0,.3,0],sh:70}});mainObj.add(dışh);
            // besleme kornasi
            var feed=_m(new THREE.CylinderGeometry(.03,.08,.2,8),0x888888,{{p:[0,.8,0]}});mainObj.add(feed);
            // besleme destek kollari
            for(var s=0;s<3;s++){{var sa=s*2.094;
            var strut=_m(new THREE.CylinderGeometry(.01,.01,.6,4),0xaaaaaa,{{p:[Math.sin(sa)*.3,.55,Math.cos(sa)*.3],r:[Math.cos(sa)*0.3,0,-Math.sin(sa)*0.3]}});mainObj.add(strut);}}
            // montaj
            var mount=_m(new THREE.CylinderGeometry(.08,.1,.2,10),0x888888,{{p:[0,-.2,0]}});mainObj.add(mount);
            // ayak/kule
            var tower=_m(new THREE.CylinderGeometry(.06,.1,1.0,8),0x666666,{{p:[0,-.75,0]}});mainObj.add(tower);
            var base=_m(new THREE.CylinderGeometry(.3,.35,.08,16),0x555555,{{p:[0,-1.25,0]}});mainObj.add(base);
        }}
        else if(T==14){{
            // GUNES YELKENI - büyük kare yelken, uzay araci, ışık basinci
            // yelken (büyük kare)
            var sail=_m(new THREE.BoxGeometry(2.5,.005,2.5),0xdddddd,{{p:[0,.3,0],sh:100,op:0.3}});mainObj.add(sail);
            // yelken destek cubulari
            var d1=_m(new THREE.CylinderGeometry(.008,.008,3.5,4),0xaaaaaa,{{p:[0,.3,0],r:[0,0.785,1.57]}});mainObj.add(d1);
            var d2=_m(new THREE.CylinderGeometry(.008,.008,3.5,4),0xaaaaaa,{{p:[0,.3,0],r:[0,-0.785,1.57]}});mainObj.add(d2);
            // uzay araci (küçük kutu)
            var craft=_m(new THREE.BoxGeometry(.2,.15,.15),0xcccccc,{{p:[0,0,0],sh:70}});mainObj.add(craft);
            // ışık basinci oklari
            for(var r=0;r<5;r++){{mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-1+r*.5,1.2,0),0.5,0xffdd44,.06,.04));}}
            // itis oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(0,-.5,0),0.5,0x44ff44,.08,.06));
        }}
        else if(T==15){{
            // IYON MOTORU - govde, izgara, plazma, güneş paneli
            var body=_m(new THREE.CylinderGeometry(.25,.25,.6,16),0xaaaaaa,{{p:[0,0,0],r:[0,0,1.57],sh:70}});mainObj.add(body);
            // iyon çıkış izgarasi
            var grid=_m(new THREE.CylinderGeometry(.22,.22,.04,16),0x888888,{{p:[-.35,0,0],r:[0,0,1.57],sh:60}});mainObj.add(grid);
            // iyon huzmesi (mavi parlama)
            var beam=_m(new THREE.ConeGeometry(.25,1.0,12),0x4488ff,{{p:[-.9,0,0],r:[0,0,1.57],em:0x224488,op:0.4}});mainObj.add(beam);
            var beamCore=_m(new THREE.ConeGeometry(.1,.7,8),0x88ccff,{{p:[-.8,0,0],r:[0,0,1.57],em:0x4466cc,op:0.6}});mainObj.add(beamCore);
            // gaz deposu
            var tank=_m(new THREE.SphereGeometry(.15,12,12),0x666666,{{p:[.3,.2,0]}});mainObj.add(tank);
            // güneş paneli
            var panel=_m(new THREE.BoxGeometry(.6,.02,.4),0x223388,{{p:[0,.35,0],sh:80}});mainObj.add(panel);
        }}
        else if(T==16){{
            // UZAY ASANSORU - yer, kablo, karsi ağırlık, gondol
            // dünya yüzeyi
            var earth=_m(new THREE.SphereGeometry(.6,20,20,0,6.28,0,1.2),0x4488cc,{{p:[0,-1.5,0]}});mainObj.add(earth);
            // kablo
            var cable=_m(new THREE.CylinderGeometry(.008,.008,3.5,4),0xaaaaaa,{{p:[0,.2,0]}});mainObj.add(cable);
            // karsi ağırlık (ust)
            var cw=_m(new THREE.BoxGeometry(.2,.2,.2),0x888888,{{p:[0,1.95,0]}});mainObj.add(cw);
            // gondol (tirmaniçi)
            var gondola=_m(new THREE.BoxGeometry(.15,.2,.1),0xdddddd,{{p:[0,.3,0],sh:70}});mainObj.add(gondola);
            // yuk oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(.15,.3,0),0.3,0x44ff44,.05,.04));
            // GEO yorunge halkasi
            var geo=_m(new THREE.TorusGeometry(1.5,.005,6,48),0xffaa33,{{p:[0,-1.5,0],r:[1.57,0,0],op:0.3}});mainObj.add(geo);
        }}
        else if(T==17){{
            // ASTEROID MADENCISI - gövde, matkap, robotik kol, asteroid
            // asteroid
            var ast=_m(new THREE.DodecahedronGeometry(.6),0x888877,{{p:[.8,0,0],sh:30}});mainObj.add(ast);
            // madenci araci
            var craft=_m(new THREE.BoxGeometry(.35,.25,.25),0xaaaaaa,{{p:[-.4,0,0],sh:60}});mainObj.add(craft);
            // matkap
            var drill=_m(new THREE.ConeGeometry(.05,.3,8),0xccaa33,{{p:[0,0,0],r:[0,0,-1.57]}});mainObj.add(drill);
            var drillShaft=_m(new THREE.CylinderGeometry(.03,.03,.2,8),0x888888,{{p:[-.15,0,0],r:[0,0,1.57]}});mainObj.add(drillShaft);
            // güneş panelleri
            var sp1=_m(new THREE.BoxGeometry(.4,.02,.25),0x223388,{{p:[-.4,.25,0]}});mainObj.add(sp1);
            // depolama konteyneri
            var cargo=_m(new THREE.BoxGeometry(.15,.15,.15),0x885533,{{p:[-.6,0,.15]}});mainObj.add(cargo);
            // parcaciklar (kazi)
            for(var p=0;p<8;p++){{var pp=_m(new THREE.SphereGeometry(.02,6,6),0xaaaa66,{{p:[.1+Math.random()*.3,(Math.random()-.5)*.3,(Math.random()-.5)*.3],op:0.5}});mainObj.add(pp);}}
        }}
        else if(T==18){{
            // HABITAT DOME - kubbe, taban, iç mekan, hava kilidi
            // taban platformu
            var base=_m(new THREE.CylinderGeometry(.9,.95,.1,24),0x888888,{{p:[0,-.5,0]}});mainObj.add(base);
            // kubbe (yari-seffaf)
            var dome=_m(new THREE.SphereGeometry(.85,24,24,0,6.28,0,1.57),0xccddee,{{p:[0,-.45,0],op:0.2,sh:100}});mainObj.add(dome);
            // iç yapi (kat)
            var floor1=_m(new THREE.CylinderGeometry(.7,.7,.03,20),0xbbbbaa,{{p:[0,-.35,0]}});mainObj.add(floor1);
            // bitki yetistirme alani
            for(var p=0;p<5;p++){{var plant=_m(new THREE.ConeGeometry(.05,.15,6),0x44aa44,{{p:[-.3+p*.15,-.2,0]}});mainObj.add(plant);}}
            // hava kilidi
            var airlock=_m(new THREE.CylinderGeometry(.12,.12,.2,10),0x666666,{{p:[.85,-.35,0],r:[0,0,1.57]}});mainObj.add(airlock);
            // güneş panelleri (dış)
            var sp=_m(new THREE.BoxGeometry(.5,.02,.3),0x223388,{{p:[-.8,-.2,.5],r:[0.3,0,0]}});mainObj.add(sp);
        }}
        else if(T==19){{
            // UZAY SONDASI - kompakt govde, anten, nükleer güç, sensörler
            var body=_m(new THREE.CylinderGeometry(.2,.25,.6,12),0xcccccc,{{p:[0,0,0],sh:70}});mainObj.add(body);
            // büyük canak anten
            var dışh=_m(new THREE.SphereGeometry(.5,16,12,0,6.28,0,1.0),0xdddddd,{{p:[0,.4,0],sh:80}});mainObj.add(dışh);
            var feed=_m(new THREE.CylinderGeometry(.015,.015,.3,6),0xaaaaaa,{{p:[0,.7,0]}});mainObj.add(feed);
            // RTG (nukleer güç)
            var rtg=_m(new THREE.CylinderGeometry(.06,.06,.4,8),0x444444,{{p:[.3,-.1,0],r:[0,0,0.5]}});mainObj.add(rtg);
            var rtgFin=_m(new THREE.BoxGeometry(.25,.02,.08),0x555555,{{p:[.35,-.15,0]}});mainObj.add(rtgFin);
            // bilimsel aletler
            var mag=_m(new THREE.CylinderGeometry(.01,.01,.5,4),0xdddddd,{{p:[-.15,-.3,0],r:[0,0,-0.5]}});mainObj.add(mag);
            var cam=_m(new THREE.CylinderGeometry(.04,.03,.1,8),0x333333,{{p:[0,-.35,.15]}});mainObj.add(cam);
        }}

        // yildiz arka plan
        var sG=new THREE.BufferGeometry();var sP=[];for(var i=0;i<200;i++)sP.push((Math.random()-.5)*30,(Math.random()-.5)*30,(Math.random()-.5)*30);sG.setAttribute('position',new THREE.Float32BufferAttribute(sP,3));scene.add(new THREE.Points(sG,new THREE.PointsMaterial({{color:0xffffff,size:.05}})));
        scene.add(mainObj);"""

    if ci == 12:  # Mimari Tasarim — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        var ground=_m(new THREE.BoxGeometry(4,.06,3),0x558B2F,{{p:[0,-1.3,0]}});mainObj.add(ground);

        if(T==0){{
            // GOKDELEN - cam cephe, katlar, tavan bahcesi
            for(var f=0;f<14;f++){{var fl=_m(new THREE.BoxGeometry(.8,.2,.7),0x6688aa,{{p:[0,-1.0+f*.22,0],sh:80}});mainObj.add(fl);
            for(var w=0;w<4;w++){{var win=_m(new THREE.BoxGeometry(.14,.14,.02),0xaaddff,{{p:[-.28+w*.18,-1.0+f*.22,.36],em:0x335566}});mainObj.add(win);}}}}
            // tavan bahcesi
            var roof=_m(new THREE.BoxGeometry(.85,.04,.75),0x44aa44,{{p:[0,2.1,0]}});mainObj.add(roof);
            // giriş lobisi
            var lobby=_m(new THREE.BoxGeometry(.3,.35,.05),0x88ccee,{{p:[0,-1.05,.36],op:0.4,sh:100}});mainObj.add(lobby);
        }}
        else if(T==1){{
            // VILLA - 2 katli, havuz, garaj, bahce
            var main=_m(new THREE.BoxGeometry(1.2,.6,.8),0xddccaa,{{p:[0,-.7,0]}});mainObj.add(main);
            var upper=_m(new THREE.BoxGeometry(.8,.5,.7),0xddccaa,{{p:[.15,-.15,0]}});mainObj.add(upper);
            var roof=_m(new THREE.BoxGeometry(1.3,.04,.85),0x884433,{{p:[0,-.38,0],r:[0,0,0.05]}});mainObj.add(roof);
            var roof2=_m(new THREE.BoxGeometry(.9,.04,.75),0x884433,{{p:[.15,.12,0]}});mainObj.add(roof2);
            // pencereler
            for(var w=0;w<3;w++){{var win=_m(new THREE.BoxGeometry(.12,.15,.02),0xaaddff,{{p:[-.4+w*.3,-.65,.41],em:0x335566}});mainObj.add(win);}}
            // havuz
            var pool=_m(new THREE.BoxGeometry(.5,.06,.35),0x44aacc,{{p:[-.7,-1.0,.5],em:0x114455}});mainObj.add(pool);
            // garaj
            var garage=_m(new THREE.BoxGeometry(.35,.3,.4),0xccccbb,{{p:[.7,-.85,.3]}});mainObj.add(garage);
        }}
        else if(T==2){{
            // MODERN KOPRU - asma köprü, kablolar, ayaklar
            // yol tabliyesi
            var deck=_m(new THREE.BoxGeometry(3.0,.06,.5),0x888888,{{p:[0,-.5,0]}});mainObj.add(deck);
            // 2 kule
            var tL=_m(new THREE.BoxGeometry(.1,.1,1.8),0xcccccc,{{p:[-0.8,0.35,0]}});mainObj.add(tL);
            var tR=_m(new THREE.BoxGeometry(.1,.1,1.8),0xcccccc,{{p:[0.8,0.35,0]}});mainObj.add(tR);
            // ana kablo (catenary)
            for(var c=0;c<20;c++){{var cx=-1.2+c*0.12;var cy=1.0-Math.pow(cx,2)*0.3;
            var cPt=_m(new THREE.SphereGeometry(.015,6,6),0x4488cc,{{p:[cx,cy,0]}});mainObj.add(cPt);}}
            // dikey kablolar
            for(var v=0;v<12;v++){{var vx=-0.8+v*0.145;var vy=1.0-Math.pow(vx,2)*0.3;
            var vCable=_m(new THREE.CylinderGeometry(.005,.005,vy+0.5,4),0x4488cc,{{p:[vx,(vy-.5)/2,0]}});mainObj.add(vCable);}}
            // su
            var water=_m(new THREE.BoxGeometry(3.5,.03,2.0),0x2266aa,{{p:[0,-1.0,0],op:0.5}});mainObj.add(water);
        }}
        else if(T==3){{
            // STADYUM - oval, tribunler, saha, ışıklar
            var ring=_m(new THREE.TorusGeometry(.8,.3,8,24),0xcccccc,{{p:[0,-.5,0],r:[1.57,0,0]}});mainObj.add(ring);
            // saha (yesil)
            var field=_m(new THREE.CylinderGeometry(.65,.65,.03,24),0x44aa44,{{p:[0,-.7,0]}});mainObj.add(field);
            // cizgiler
            var center=_m(new THREE.TorusGeometry(.15,.005,6,20),0xffffff,{{p:[0,-.68,0],r:[1.57,0,0]}});mainObj.add(center);
            // ışık direkleri
            for(var l=0;l<4;l++){{var la=l*1.57;
            var pole=_m(new THREE.CylinderGeometry(.02,.025,.8,6),0x888888,{{p:[Math.sin(la)*1.0,-.1,Math.cos(la)*1.0]}});mainObj.add(pole);
            var light=_m(new THREE.BoxGeometry(.1,.04,.06),0xffffcc,{{p:[Math.sin(la)*1.0,.3,Math.cos(la)*1.0],em:0x888844}});mainObj.add(light);}}
        }}
        else if(T==4){{
            // HAVALIMANI - terminal, kontrol kulesi, pist, üçak
            var terminal=_m(new THREE.BoxGeometry(2.0,.4,.6),0xcccccc,{{p:[0,-.8,-.3],sh:60}});mainObj.add(terminal);
            // cam cephe
            var glass=_m(new THREE.BoxGeometry(2.0,.35,.02),0x88ccee,{{p:[0,-.78,.01],op:0.3,sh:100}});mainObj.add(glass);
            // kontrol kulesi
            var twrBase=_m(new THREE.CylinderGeometry(.06,.08,.8,10),0xcccccc,{{p:[.7,-.2,-.3]}});mainObj.add(twrBase);
            var twrTop=_m(new THREE.CylinderGeometry(.12,.1,.15,12),0x88ccee,{{p:[.7,.2,-.3],sh:100}});mainObj.add(twrTop);
            // pist
            var runway=_m(new THREE.BoxGeometry(2.5,.02,.25),0x555555,{{p:[0,-1.0,.5]}});mainObj.add(runway);
            // pist cizgileri
            for(var s=0;s<10;s++){{var sl=_m(new THREE.BoxGeometry(.15,.025,.03),0xffffff,{{p:[-1.1+s*.25,-0.99,.5]}});mainObj.add(sl);}}
            // üçak (basit)
            var plane=_m(new THREE.CylinderGeometry(.03,.03,.4,8),0xeeeeee,{{p:[-.3,-.85,.5],r:[0,0,1.57]}});mainObj.add(plane);
            var pWing=_m(new THREE.BoxGeometry(.3,.01,.06),0xeeeeee,{{p:[-.3,-.84,.5]}});mainObj.add(pWing);
        }}
        else if(T==5){{
            // TREN ISTASYONU - peron, catı, raylar, saat
            var peron=_m(new THREE.BoxGeometry(2.5,.1,.8),0xbbbbaa,{{p:[0,-1.0,0]}});mainObj.add(peron);
            // catı (kemerli)
            for(var a=0;a<5;a++){{var arch=_m(new THREE.TorusGeometry(.5,.02,6,16,3.14),0x888888,{{p:[-1.0+a*.5,.0,0],r:[0,1.57,0]}});mainObj.add(arch);}}
            var roofP=_m(new THREE.BoxGeometry(2.2,.02,.8),0xaaaaaa,{{p:[0,.3,0],op:0.5}});mainObj.add(roofP);
            // raylar
            for(var r=0;r<2;r++){{var rail=_m(new THREE.BoxGeometry(3.0,.02,.02),0x888888,{{p:[0,-1.05,-.3+r*.15]}});mainObj.add(rail);}}
            // saat
            var clock=_m(new THREE.CylinderGeometry(.08,.08,.02,16),0xffffff,{{p:[0,.15,.41]}});mainObj.add(clock);
        }}
        else if(T==6){{
            // DENIZ FENERI - govde, ışık odasi, galeri, kayalik
            var base=_m(new THREE.CylinderGeometry(.35,.45,.3,16),0xaaaaaa,{{p:[0,-1.0,0]}});mainObj.add(base);
            var body=_m(new THREE.CylinderGeometry(.2,.3,1.8,16),0xffffff,{{p:[0,.1,0],sh:60}});mainObj.add(body);
            // kirmizi bant
            var band=_m(new THREE.CylinderGeometry(.22,.22,.15,16),0xff3333,{{p:[0,.5,0]}});mainObj.add(band);
            // galeri (balkon)
            var gallery=_m(new THREE.CylinderGeometry(.28,.28,.06,16),0x888888,{{p:[0,1.05,0]}});mainObj.add(gallery);
            var railing=_m(new THREE.TorusGeometry(.28,.01,6,20),0x888888,{{p:[0,1.12,0],r:[1.57,0,0]}});mainObj.add(railing);
            // ışık odasi
            var lantern=_m(new THREE.CylinderGeometry(.18,.2,.25,12),0xccddee,{{p:[0,1.2,0],op:0.4,sh:100}});mainObj.add(lantern);
            var light=_m(new THREE.SphereGeometry(.1,12,12),0xffee44,{{p:[0,1.2,0],em:0xccaa22}});mainObj.add(light);
            // kubbe
            var dome=_m(new THREE.SphereGeometry(.18,12,12,0,6.28,0,1.57),0x444444,{{p:[0,1.33,0]}});mainObj.add(dome);
            // kayalik
            for(var r=0;r<6;r++){{var rock=_m(new THREE.DodecahedronGeometry(.15+Math.random()*.1),0x887766,{{p:[(Math.random()-.5)*.8,-1.15,(Math.random()-.5)*.5]}});mainObj.add(rock);}}
        }}
        else if(T==7){{
            // RUZGAR TURBINI - kule, nasel, 3 kanat, taban
            var tower=_m(new THREE.CylinderGeometry(.05,.08,2.5,10),0xeeeeee,{{p:[0,.0,0],sh:60}});mainObj.add(tower);
            // nasel
            var nacelle=_m(new THREE.CylinderGeometry(.1,.1,.25,10),0xdddddd,{{p:[0,1.25,0.05],r:[1.57,0,0],sh:70}});mainObj.add(nacelle);
            // hub
            var hub=_m(new THREE.SphereGeometry(.08,10,10),0xcccccc,{{p:[0,1.25,.18]}});mainObj.add(hub);
            // 3 kanat
            for(var b=0;b<3;b++){{var bAng=b*2.094;
            var blade=_m(new THREE.BoxGeometry(.06,1.1,.03),0xffffff,{{p:[Math.sin(bAng)*.55,1.25+Math.cos(bAng)*.55,.2],r:[0,0,bAng]}});mainObj.add(blade);}}
            // taban
            var base=_m(new THREE.CylinderGeometry(.2,.25,.08,16),0xaaaaaa,{{p:[0,-1.25,0]}});mainObj.add(base);
        }}
        else if(T==8){{
            // GUNES EVI - cati panelli, pasif enerji, yesil cati
            var body=_m(new THREE.BoxGeometry(1.0,.6,.7),0xddccaa,{{p:[0,-.7,0]}});mainObj.add(body);
            // egik cati (güneş panelli)
            var roof=_m(new THREE.BoxGeometry(1.1,.04,.8),0x223388,{{p:[0,-.35,0],r:[0,0,0.1],sh:80}});mainObj.add(roof);
            // cam duvar (güney)
            var glass=_m(new THREE.BoxGeometry(.8,.45,.02),0x88ccee,{{p:[0,-.68,.36],op:0.3,sh:100}});mainObj.add(glass);
            // yesil cati
            for(var p=0;p<6;p++){{var plant=_m(new THREE.SphereGeometry(.06,8,8),0x44aa44,{{p:[-.3+p*.12,-.3,.2]}});mainObj.add(plant);}}
            // pencereler
            for(var w=0;w<2;w++){{var win=_m(new THREE.BoxGeometry(.15,.2,.02),0xaaddff,{{p:[-.3+w*.6,-.65,-.36],em:0x335566}});mainObj.add(win);}}
        }}
        else if(T==9){{
            // MODERN KULE - dinamik form, gözlem katı
            for(var f=0;f<12;f++){{var r=0.35-f*.015;var rot=f*0.1;
            var fl=_m(new THREE.CylinderGeometry(r,r+.02,.2,16),0x8888aa,{{p:[0,-1.0+f*.22,0],r:[0,rot,0],sh:80}});mainObj.add(fl);}}
            // gözlem katı (geniş)
            var obs=_m(new THREE.CylinderGeometry(.4,.35,.15,16),0x88ccee,{{p:[0,1.6,0],sh:100}});mainObj.add(obs);
            // anten
            var ant=_m(new THREE.CylinderGeometry(.015,.005,.4,6),0xcccccc,{{p:[0,1.85,0]}});mainObj.add(ant);
        }}
        else if(T==10){{
            // MUZE - modern form, büyük giriş, cam tavan
            var body=_m(new THREE.BoxGeometry(1.5,.7,.8),0xeeeeee,{{p:[0,-.65,0],sh:60}});mainObj.add(body);
            // cam tavan
            var glassCeil=_m(new THREE.BoxGeometry(1.0,.03,.6),0x88ccee,{{p:[0,-.27,0],op:0.3,sh:100}});mainObj.add(glassCeil);
            // giriş portali
            var portal=_m(new THREE.BoxGeometry(.5,.55,.04),0x88ccee,{{p:[0,-.6,.42],op:0.35,sh:100}});mainObj.add(portal);
            // merdivenler
            for(var s=0;s<4;s++){{var step=_m(new THREE.BoxGeometry(.6,.04,.08),0xcccccc,{{p:[0,-1.02+s*.05,.5+s*.08]}});mainObj.add(step);}}
        }}
        else if(T==11){{
            // TIYATRO - sahne, seyirci, perde
            var body=_m(new THREE.BoxGeometry(1.4,.8,.9),0xccbbaa,{{p:[0,-.6,0]}});mainObj.add(body);
            // sahne
            var stage=_m(new THREE.BoxGeometry(1.0,.06,.4),0x884422,{{p:[0,-.85,.15]}});mainObj.add(stage);
            // perde
            var curtainL=_m(new THREE.BoxGeometry(.15,.5,.02),0xcc2222,{{p:[-.4,-.55,.36]}});mainObj.add(curtainL);
            var curtainR=_m(new THREE.BoxGeometry(.15,.5,.02),0xcc2222,{{p:[.4,-.55,.36]}});mainObj.add(curtainR);
            // tribun basamaklari
            for(var r=0;r<4;r++){{var row=_m(new THREE.BoxGeometry(1.0,.08,.12),0x886655,{{p:[0,-.8+r*.12,-.2-r*.12]}});mainObj.add(row);}}
            // kubbe
            var dome=_m(new THREE.SphereGeometry(.5,16,8,0,6.28,0,1.2),0xccbbaa,{{p:[0,-.1,0]}});mainObj.add(dome);
        }}
        else if(T==12){{
            // KUTUPHANE - raf duvarlari, okuma alani, kubbe
            var body=_m(new THREE.BoxGeometry(1.2,.7,.8),0xddddcc,{{p:[0,-.65,0]}});mainObj.add(body);
            // kitap raflari
            for(var s=0;s<4;s++){{for(var sh=0;sh<3;sh++){{
            var shelf=_m(new THREE.BoxGeometry(.2,.03,.12),0x885533,{{p:[-.4+s*.25,-.85+sh*.15,-.25]}});mainObj.add(shelf);
            // kitaplar
            for(var b=0;b<3;b++){{var book=_m(new THREE.BoxGeometry(.04,.1,.1),[0xcc3333,0x3333cc,0x33cc33,0xcccc33][b%4],{{p:[-.42+s*.25+b*.05,-.8+sh*.15,-.25]}});mainObj.add(book);}}}}}}
            // kubbe
            var dome=_m(new THREE.SphereGeometry(.4,16,8,0,6.28,0,1.2),0xddddcc,{{p:[0,-.2,0]}});mainObj.add(dome);
        }}
        else if(T==13){{
            // HASTANE - H isareti, ambulans girişi, katlar
            var body=_m(new THREE.BoxGeometry(1.2,.8,.7),0xeeeeee,{{p:[0,-.6,0]}});mainObj.add(body);
            // kirmizi haç
            var h1=_m(new THREE.BoxGeometry(.2,.06,.02),0xff0000,{{p:[0,-.35,.36]}});mainObj.add(h1);
            var h2=_m(new THREE.BoxGeometry(.06,.2,.02),0xff0000,{{p:[0,-.35,.36]}});mainObj.add(h2);
            // pencereler
            for(var f=0;f<3;f++)for(var w=0;w<4;w++){{var win=_m(new THREE.BoxGeometry(.1,.1,.02),0xaaddff,{{p:[-.35+w*.22,-.8+f*.25,.36],em:0x335566}});mainObj.add(win);}}
            // ambulans girişi
            var canopy=_m(new THREE.BoxGeometry(.4,.04,.25),0xcccccc,{{p:[-.3,-0.95,.5]}});mainObj.add(canopy);
        }}
        else if(T==14){{
            // OKUL - 2 katli, bahce, bayrak
            var body=_m(new THREE.BoxGeometry(1.4,.6,.6),0xddddcc,{{p:[0,-.7,0]}});mainObj.add(body);
            var upper=_m(new THREE.BoxGeometry(1.2,.5,.55),0xddddcc,{{p:[0,-.2,0]}});mainObj.add(upper);
            // pencereler
            for(var w=0;w<5;w++){{var win=_m(new THREE.BoxGeometry(.12,.12,.02),0xaaddff,{{p:[-.5+w*.25,-.65,.31],em:0x335566}});mainObj.add(win);}}
            // bayrak diregi
            var pole=_m(new THREE.CylinderGeometry(.01,.015,.8,6),0xaaaaaa,{{p:[.5,.2,0]}});mainObj.add(pole);
            var flag=_m(new THREE.BoxGeometry(.2,.1,.01),0xff0000,{{p:[.6,.5,0]}});mainObj.add(flag);
            // bahce
            for(var t=0;t<3;t++){{var tree=_m(new THREE.ConeGeometry(.08,.2,8),0x44aa44,{{p:[-.5+t*.5,-1.1,.5]}});mainObj.add(tree);}}
        }}
        else if(T==15){{
            // PARK - yuruyus yolu, bank, ağaçlar, havuz
            var path=_m(new THREE.BoxGeometry(.2,.02,2.0),0xbbaa88,{{p:[0,-1.25,0]}});mainObj.add(path);
            // ağaçlar
            for(var t=0;t<5;t++){{var trunk=_m(new THREE.CylinderGeometry(.02,.03,.3,6),0x885533,{{p:[-.5+t*.25,-1.0,(t%2?-.3:.3)]}});mainObj.add(trunk);
            var crown=_m(new THREE.SphereGeometry(.15,10,10),0x44aa44,{{p:[-.5+t*.25,-.8,(t%2?-.3:.3)]}});mainObj.add(crown);}}
            // bank
            var bench=_m(new THREE.BoxGeometry(.25,.02,.08),0x885533,{{p:[.3,-1.1,.15]}});mainObj.add(bench);
            // küçük havuz
            var pond=_m(new THREE.CylinderGeometry(.2,.2,.03,16),0x4488cc,{{p:[-.3,-1.24,.0],em:0x223355}});mainObj.add(pond);
        }}
        else if(T==16){{
            // MARINA - iskele, tekne, deniz
            var water=_m(new THREE.BoxGeometry(3,.03,2),0x2266aa,{{p:[0,-1.1,0],op:0.5}});mainObj.add(water);
            // iskele
            var dock=_m(new THREE.BoxGeometry(.15,.04,1.2),0x885533,{{p:[0,-1.0,0]}});mainObj.add(dock);
            // tekneler
            for(var b=0;b<3;b++){{var hull=_m(new THREE.SphereGeometry(.12,8,8,0,6.28,1.57,1.57),0xeeeeee,{{p:[.25,-1.05,-.3+b*.3],s:[1.5,.5,1]}});mainObj.add(hull);
            var mast=_m(new THREE.CylinderGeometry(.005,.005,.3,4),0xaaaaaa,{{p:[.25,-.85,-.3+b*.3]}});mainObj.add(mast);}}
        }}
        else if(T==17){{
            // BARAJ - beton govde, su, kapaklari
            var dam=_m(new THREE.BoxGeometry(.2,1.2,2.0),0xaaaaaa,{{p:[0,-.4,0]}});mainObj.add(dam);
            // su (yüksek taraf)
            var waterH=_m(new THREE.BoxGeometry(1.0,.8,2.0),0x2266aa,{{p:[-.6,-.6,0],op:0.4}});mainObj.add(waterH);
            // su (alcak taraf)
            var waterL=_m(new THREE.BoxGeometry(1.0,.3,2.0),0x2266aa,{{p:[.6,-.85,0],op:0.4}});mainObj.add(waterL);
            // kapaklar
            for(var g=0;g<3;g++){{var gate=_m(new THREE.BoxGeometry(.04,.15,.2),0x888888,{{p:[.1,-.7,-.4+g*.4]}});mainObj.add(gate);}}
            // enerji santrali
            var plant=_m(new THREE.BoxGeometry(.25,.2,.4),0xcccccc,{{p:[.4,-0.9,0]}});mainObj.add(plant);
        }}
        else if(T==18){{
            // SERA - cam/plastik yapi, bitkiler, iklim kontrolu
            var frame=_m(new THREE.BoxGeometry(1.2,.02,.7),0xaaaaaa,{{p:[0,-1.0,0]}});mainObj.add(frame);
            // cam duvarlar
            var wallF=_m(new THREE.BoxGeometry(1.2,.5,.02),0xcceecc,{{p:[0,-.73,.35],op:0.2,sh:100}});mainObj.add(wallF);
            var wallB=_m(new THREE.BoxGeometry(1.2,.5,.02),0xcceecc,{{p:[0,-.73,-.35],op:0.2}});mainObj.add(wallB);
            var wallL=_m(new THREE.BoxGeometry(.02,.5,.7),0xcceecc,{{p:[-.6,-.73,0],op:0.2}});mainObj.add(wallL);
            var wallR=_m(new THREE.BoxGeometry(.02,.5,.7),0xcceecc,{{p:[.6,-.73,0],op:0.2}});mainObj.add(wallR);
            // kemerli tavan
            for(var a=0;a<6;a++){{var arch=_m(new THREE.TorusGeometry(.35,.01,6,12,3.14),0xaaaaaa,{{p:[-.5+a*.2,-.48,0],r:[0,1.57,0]}});mainObj.add(arch);}}
            // bitkiler
            for(var p=0;p<6;p++){{var plant=_m(new THREE.ConeGeometry(.05,.15,6),0x44aa44,{{p:[-.4+p*.16,-.85,0]}});mainObj.add(plant);}}
        }}
        else if(T==19){{
            // KULUBE - ahsap, baca, sundurma
            var body=_m(new THREE.BoxGeometry(.6,.45,.5),0x8B5A2B,{{p:[0,-.8,0]}});mainObj.add(body);
            // üçgen cati
            var roof=_m(new THREE.ConeGeometry(.5,.3,4),0x663311,{{p:[0,-.5,0],r:[0,0.785,0]}});mainObj.add(roof);
            // kapi
            var door=_m(new THREE.BoxGeometry(.12,.22,.02),0x553311,{{p:[0,-.88,.26]}});mainObj.add(door);
            // pencere
            var win=_m(new THREE.BoxGeometry(.1,.1,.02),0xaaddff,{{p:[.18,-.72,.26],em:0x335566}});mainObj.add(win);
            // baca
            var chimney=_m(new THREE.BoxGeometry(.08,.2,.08),0x884433,{{p:[.15,-.35,.1]}});mainObj.add(chimney);
            // sundurma
            var porch=_m(new THREE.BoxGeometry(.3,.02,.15),0x885533,{{p:[0,-.98,.35]}});mainObj.add(porch);
            // cit
            for(var f=0;f<6;f++){{var fence=_m(new THREE.BoxGeometry(.02,.15,.02),0x885533,{{p:[-.4+f*.15,-1.0,.6]}});mainObj.add(fence);}}
        }}

        scene.add(mainObj);"""

    if ci == 13:  # Mekanik Sistemler — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        if(T==0){{
            // DISLI CARK - iki kavisan dışli, dışler, eksen
            var g1=_m(new THREE.CylinderGeometry(.6,.6,.12,32),0xaaaaaa,{{p:[-.5,0,0],sh:90}});mainObj.add(g1);
            for(var t=0;t<16;t++){{var a=t*0.393;var tooth=_m(new THREE.BoxGeometry(.08,.12,.12),0xbbbbbb,{{p:[-.5+Math.cos(a)*.64,Math.sin(a)*.64,0],r:[0,0,a],sh:80}});mainObj.add(tooth);}}
            var ax1=_m(new THREE.CylinderGeometry(.06,.06,.25,10),0x888888,{{p:[-.5,0,0],r:[1.57,0,0],sh:90}});mainObj.add(ax1);
            // ikinci dışli (küçük)
            var g2=_m(new THREE.CylinderGeometry(.35,.35,.12,24),0x999999,{{p:[.55,.45,0],sh:90}});mainObj.add(g2);
            for(var t=0;t<10;t++){{var a=t*0.628;var tooth2=_m(new THREE.BoxGeometry(.07,.1,.12),0xaaaaaa,{{p:[.55+Math.cos(a)*.39,.45+Math.sin(a)*.39,0],r:[0,0,a],sh:80}});mainObj.add(tooth2);}}
            var ax2=_m(new THREE.CylinderGeometry(.05,.05,.25,10),0x888888,{{p:[.55,.45,0],r:[1.57,0,0],sh:90}});mainObj.add(ax2);
            // donme oklari
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(-.5,.75,0),0.3,0xff4444,.06,.04));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(.55,.9,0),0.3,0x4444ff,.06,.04));
        }}
        else if(T==1){{
            // PISTON - silindir, piston kafasi, segmanlar, biyel, krank
            var cyl=_m(new THREE.CylinderGeometry(.3,.3,1.2,20),0x888888,{{p:[0,.2,0],op:0.3,sh:100}});mainObj.add(cyl);
            // piston kafasi
            var head=_m(new THREE.CylinderGeometry(.27,.27,.15,20),0xaaaaaa,{{p:[0,.5,0],sh:90}});mainObj.add(head);
            // segmanlar
            for(var s=0;s<3;s++){{var seg=_m(new THREE.TorusGeometry(.28,.012,6,24),0x555555,{{p:[0,.42-s*.06,0],r:[1.57,0,0]}});mainObj.add(seg);}}
            // piston biyel cubugu
            var rod=_m(new THREE.CylinderGeometry(.04,.04,.8,8),0x888888,{{p:[0,0,0],sh:80}});mainObj.add(rod);
            // krank mili baglantisi
            var crankPin=_m(new THREE.SphereGeometry(.06,10,10),0xaaaaaa,{{p:[0,-.4,0],sh:90}});mainObj.add(crankPin);
            // buji
            var spark=_m(new THREE.CylinderGeometry(.025,.015,.15,8),0xcccccc,{{p:[0,.85,0],sh:90}});mainObj.add(spark);
            // hareket oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(.4,.3,0),0.4,0xff4444,.08,.06));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(.4,.3,0),0.4,0x4444ff,.08,.06));
        }}
        else if(T==2){{
            // VOLAN - agir disk, eksen, balanslama
            var disk=_m(new THREE.CylinderGeometry(.8,.8,.1,32),0xaaaaaa,{{p:[0,0,0],sh:90}});mainObj.add(disk);
            var rim=_m(new THREE.TorusGeometry(.8,.04,8,32),0x999999,{{p:[0,0,0],r:[1.57,0,0],sh:80}});mainObj.add(rim);
            // iç yapı (kollar)
            for(var s=0;s<6;s++){{var sa=s*1.047;
            var spoke=_m(new THREE.BoxGeometry(.6,.03,.04),0xbbbbbb,{{p:[Math.cos(sa)*.3,0,Math.sin(sa)*.3],r:[0,sa,0],sh:80}});mainObj.add(spoke);}}
            // eksen
            var axle=_m(new THREE.CylinderGeometry(.06,.06,.4,12),0x888888,{{p:[0,0,0],r:[1.57,0,0],sh:90}});mainObj.add(axle);
            // donme oku
            for(var a=0;a<4;a++){{var aa=a*1.57;
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(-Math.sin(aa),0,Math.cos(aa)),new THREE.Vector3(Math.cos(aa)*.9,0,Math.sin(aa)*.9),0.2,0xff8844,.05,.04));}}
        }}
        else if(T==3){{
            // KAM MILI - kam profili, mil, itiçi, supap
            var shaft=_m(new THREE.CylinderGeometry(.05,.05,2.0,10),0x888888,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(shaft);
            // kam profilleri (4 kam)
            for(var k=0;k<4;k++){{var kx=-0.6+k*0.4;
            var cam=_m(new THREE.CylinderGeometry(.2,.2,.06,20),0xaaaaaa,{{p:[kx,0.05,0],r:[1.57,0,0],sh:90}});mainObj.add(cam);
            // kam cikintisi (oval)
            var lobe=_m(new THREE.SphereGeometry(.12,12,12),0xbbbbbb,{{p:[kx,.22,0],s:[1,1.5,.8],sh:80}});mainObj.add(lobe);
            // itiçi (follower)
            var follower=_m(new THREE.CylinderGeometry(.04,.04,.4,8),0x888888,{{p:[kx,.55,0],sh:70}});mainObj.add(follower);
            // supap (ust)
            var valve=_m(new THREE.CylinderGeometry(.08,.08,.03,12),0x666666,{{p:[kx,.76,0],sh:80}});mainObj.add(valve);}}
        }}
        else if(T==4){{
            // BILYALI YATAK - dış bilezik, iç bilezik, bilyalar, kafes
            var outer=_m(new THREE.TorusGeometry(.7,.08,8,32),0xaaaaaa,{{p:[0,0,0],sh:100}});mainObj.add(outer);
            var inner=_m(new THREE.TorusGeometry(.4,.06,8,24),0xbbbbbb,{{p:[0,0,0],sh:100}});mainObj.add(inner);
            // bilyalar
            for(var b=0;b<12;b++){{var ba=b*0.524;var bx=Math.cos(ba)*0.55,by=Math.sin(ba)*0.55;
            var ball=_m(new THREE.SphereGeometry(.06,16,16),0xdddddd,{{p:[bx,by,0],sh:120}});mainObj.add(ball);}}
            // kafes (tutüçu)
            var cage=_m(new THREE.TorusGeometry(.55,.015,6,32),0xccaa44,{{p:[0,0,0],op:0.5}});mainObj.add(cage);
            // eksen
            var axle=_m(new THREE.CylinderGeometry(.08,.08,.3,12),0x888888,{{p:[0,0,0],r:[1.57,0,0],sh:80}});mainObj.add(axle);
        }}
        else if(T==5){{
            // KAYIS KASNAK - 2 kasnak, kayis, gergi
            var p1=_m(new THREE.CylinderGeometry(.4,.4,.1,24),0xaaaaaa,{{p:[-.6,0,0],sh:80}});mainObj.add(p1);
            var p1groove=_m(new THREE.TorusGeometry(.4,.025,6,24),0x888888,{{p:[-.6,0,0],sh:70}});mainObj.add(p1groove);
            var p2=_m(new THREE.CylinderGeometry(.25,.25,.1,20),0xaaaaaa,{{p:[.7,0,0],sh:80}});mainObj.add(p2);
            var p2groove=_m(new THREE.TorusGeometry(.25,.02,6,20),0x888888,{{p:[.7,0,0],sh:70}});mainObj.add(p2groove);
            // kayis (ust ve alt duz kısım + yay)
            var beltTop=_m(new THREE.BoxGeometry(1.3,.02,.08),0x333333,{{p:[.05,.35,0]}});mainObj.add(beltTop);
            var beltBot=_m(new THREE.BoxGeometry(1.3,.02,.08),0x333333,{{p:[.05,-.35,0]}});mainObj.add(beltBot);
            // eksekler
            var ax1=_m(new THREE.CylinderGeometry(.04,.04,.2,8),0x888888,{{p:[-.6,0,0],r:[1.57,0,0]}});mainObj.add(ax1);
            var ax2=_m(new THREE.CylinderGeometry(.04,.04,.2,8),0x888888,{{p:[.7,0,0],r:[1.57,0,0]}});mainObj.add(ax2);
            // gergi
            var tensioner=_m(new THREE.CylinderGeometry(.08,.08,.06,12),0x666666,{{p:[.1,-.42,0],sh:70}});mainObj.add(tensioner);
        }}
        else if(T==6){{
            // ZINCIR DISLI - 2 dışli, zincir halkalari
            var sp1=_m(new THREE.CylinderGeometry(.4,.4,.06,24),0xaaaaaa,{{p:[-.55,0,0],sh:80}});mainObj.add(sp1);
            for(var t=0;t<12;t++){{var ta=t*0.524;var tooth=_m(new THREE.BoxGeometry(.04,.08,.06),0xbbbbbb,{{p:[-.55+Math.cos(ta)*.44,Math.sin(ta)*.44,0],r:[0,0,ta]}});mainObj.add(tooth);}}
            var sp2=_m(new THREE.CylinderGeometry(.25,.25,.06,16),0xaaaaaa,{{p:[.6,0,0],sh:80}});mainObj.add(sp2);
            for(var t=0;t<8;t++){{var ta=t*0.785;var tooth=_m(new THREE.BoxGeometry(.035,.06,.06),0xbbbbbb,{{p:[.6+Math.cos(ta)*.28,Math.sin(ta)*.28,0],r:[0,0,ta]}});mainObj.add(tooth);}}
            // zincir halkalari (ust ve alt)
            for(var c=0;c<20;c++){{var cx=-.55+c*0.06;
            var link=_m(new THREE.TorusGeometry(.02,.005,4,8),0x888888,{{p:[cx,.44,0],r:[0,c%2?1.57:0,0],sh:60}});mainObj.add(link);
            var link2=_m(new THREE.TorusGeometry(.02,.005,4,8),0x888888,{{p:[cx,-.44,0],r:[0,c%2?1.57:0,0],sh:60}});mainObj.add(link2);}}
        }}
        else if(T==7){{
            // TURBIN - kanatlar, govde, eksen, giriş/çıkış
            var hub=_m(new THREE.SphereGeometry(.2,16,16),0xbbbbbb,{{p:[0,0,0],sh:90}});mainObj.add(hub);
            // kanatlar (10 adet)
            for(var b=0;b<10;b++){{var ba=b*0.628;
            var blade=_m(new THREE.BoxGeometry(.06,.55,.08),0xaaaaaa,{{p:[Math.cos(ba)*.4,Math.sin(ba)*.4,0],r:[0,0,ba+0.3],sh:80}});mainObj.add(blade);}}
            // dış govde (kasa)
            var casing=_m(new THREE.TorusGeometry(.7,.06,8,32),0x888888,{{p:[0,0,0],sh:60}});mainObj.add(casing);
            // eksen
            var shaft=_m(new THREE.CylinderGeometry(.04,.04,.6,8),0x888888,{{p:[0,0,0],r:[1.57,0,0],sh:80}});mainObj.add(shaft);
            // akis yonu oklari
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,0,1),new THREE.Vector3(0,0,-.6),0.4,0x4488ff,.08,.06));
        }}
        else if(T==8){{
            // KOMPRESOR - silindir, piston, valf, basinc hatti
            var cyl=_m(new THREE.CylinderGeometry(.3,.3,.8,16),0x888888,{{p:[0,0,0],op:0.4,sh:80}});mainObj.add(cyl);
            var piston=_m(new THREE.CylinderGeometry(.27,.27,.08,16),0xaaaaaa,{{p:[0,.2,0],sh:90}});mainObj.add(piston);
            var rod=_m(new THREE.CylinderGeometry(.04,.04,.5,8),0x888888,{{p:[0,.5,0]}});mainObj.add(rod);
            // giriş valf
            var inV=_m(new THREE.CylinderGeometry(.06,.06,.15,8),0x4488cc,{{p:[-.35,-.2,0],r:[0,0,1.57]}});mainObj.add(inV);
            // çıkış valf
            var outV=_m(new THREE.CylinderGeometry(.06,.06,.15,8),0xff6644,{{p:[.35,-.2,0],r:[0,0,1.57]}});mainObj.add(outV);
            // basinc deposu
            var tank=_m(new THREE.SphereGeometry(.25,14,14),0x888888,{{p:[.8,-.2,0],sh:60}});mainObj.add(tank);
            var pipe=_m(new THREE.CylinderGeometry(.03,.03,.3,6),0x888888,{{p:[.55,-.2,0],r:[0,0,1.57]}});mainObj.add(pipe);
        }}
        else if(T==9){{
            // POMPA - govde, cark, giriş/çıkış, mil
            var body=_m(new THREE.CylinderGeometry(.45,.45,.3,20),0x888888,{{p:[0,0,0],r:[1.57,0,0],sh:60}});mainObj.add(body);
            // cark (impeller)
            for(var v=0;v<6;v++){{var va=v*1.047;
            var vane=_m(new THREE.BoxGeometry(.3,.04,.25),0xaaaaaa,{{p:[Math.cos(va)*.2,Math.sin(va)*.2,0],r:[0,0,va+0.5],sh:80}});mainObj.add(vane);}}
            var axle=_m(new THREE.CylinderGeometry(.04,.04,.5,8),0x888888,{{p:[0,0,.3],r:[1.57,0,0]}});mainObj.add(axle);
            // giriş borusu
            var inlet=_m(new THREE.CylinderGeometry(.1,.1,.4,10),0x4488cc,{{p:[0,0,-.3],r:[1.57,0,0]}});mainObj.add(inlet);
            // çıkış borusu
            var outlet=_m(new THREE.CylinderGeometry(.08,.08,.3,10),0xff6644,{{p:[.5,.1,0],r:[0,0,1.57]}});mainObj.add(outlet);
        }}
        else if(T==10){{
            // HIDROLIK SILINDIR - silindir, piston kolu, baglanti, boru
            var cyl=_m(new THREE.CylinderGeometry(.15,.15,1.2,16),0x888888,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(cyl);
            // piston kolu
            var rod=_m(new THREE.CylinderGeometry(.05,.05,.8,10),0xcccccc,{{p:[.9,0,0],r:[0,0,1.57],sh:100}});mainObj.add(rod);
            // baglanti parmaliklari
            var mount1=_m(new THREE.SphereGeometry(.08,10,10),0xaaaaaa,{{p:[-.65,0,0],sh:80}});mainObj.add(mount1);
            var mount2=_m(new THREE.SphereGeometry(.06,10,10),0xaaaaaa,{{p:[1.3,0,0],sh:80}});mainObj.add(mount2);
            // hidrolik boru
            var pipe1=_m(new THREE.CylinderGeometry(.025,.025,.4,6),0x444444,{{p:[-.3,.3,0]}});mainObj.add(pipe1);
            var pipe2=_m(new THREE.CylinderGeometry(.025,.025,.4,6),0x444444,{{p:[.1,.3,0]}});mainObj.add(pipe2);
            // basinc oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(.5,0,0),0.5,0xff4444,.08,.06));
        }}
        else if(T==11){{
            // VALF - govde, disk, mil, volan
            var body=_m(new THREE.SphereGeometry(.3,16,16),0x888888,{{p:[0,0,0],sh:70}});mainObj.add(body);
            // giriş/çıkış borulari
            var pIn=_m(new THREE.CylinderGeometry(.1,.1,.5,10),0x888888,{{p:[-.5,0,0],r:[0,0,1.57],sh:60}});mainObj.add(pIn);
            var pOut=_m(new THREE.CylinderGeometry(.1,.1,.5,10),0x888888,{{p:[.5,0,0],r:[0,0,1.57],sh:60}});mainObj.add(pOut);
            // mil
            var stem=_m(new THREE.CylinderGeometry(.03,.03,.5,8),0xaaaaaa,{{p:[0,.4,0],sh:80}});mainObj.add(stem);
            // volan (el carki)
            var wheel=_m(new THREE.TorusGeometry(.15,.02,6,16),0xcc4444,{{p:[0,.65,0],r:[1.57,0,0]}});mainObj.add(wheel);
            // iç disk
            var disc=_m(new THREE.CylinderGeometry(.08,.08,.03,12),0xaaaaaa,{{p:[0,0,0],sh:90}});mainObj.add(disc);
        }}
        else if(T==12){{
            // YAYLI MEKANIZMA - yay, pistonlar, kasa
            var casing=_m(new THREE.CylinderGeometry(.2,.2,.8,14),0x888888,{{p:[0,0,0],op:0.3,sh:60}});mainObj.add(casing);
            // yay bobinleri
            for(var c=0;c<12;c++){{var coil=_m(new THREE.TorusGeometry(.15,.015,8,16),0xcccccc,{{p:[0,-.3+c*.05,0],r:[1.57,0,0],sh:90}});mainObj.add(coil);}}
            // ust plaka
            var topP=_m(new THREE.CylinderGeometry(.18,.18,.04,14),0xaaaaaa,{{p:[0,.35,0],sh:80}});mainObj.add(topP);
            // alt plaka
            var botP=_m(new THREE.CylinderGeometry(.18,.18,.04,14),0xaaaaaa,{{p:[0,-.35,0],sh:80}});mainObj.add(botP);
            // kuvvet oklari
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(0,.55,0),0.3,0xff4444,.06,.04));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(0,-.55,0),0.3,0x4444ff,.06,.04));
        }}
        else if(T==13){{
            // REDUKTOR - dış govde, iç dışli ciftleri
            var housing=_m(new THREE.BoxGeometry(.8,.6,.4),0x888888,{{p:[0,0,0],sh:50}});mainObj.add(housing);
            // giriş mili
            var inShaft=_m(new THREE.CylinderGeometry(.04,.04,.4,8),0xaaaaaa,{{p:[-.6,0,0],r:[0,0,1.57],sh:80}});mainObj.add(inShaft);
            // çıkış mili
            var outShaft=_m(new THREE.CylinderGeometry(.06,.06,.4,8),0xaaaaaa,{{p:[.6,0,0],r:[0,0,1.57],sh:80}});mainObj.add(outShaft);
            // iç dışli 1 (büyük)
            var g1=_m(new THREE.CylinderGeometry(.2,.2,.06,20),0xbbbbbb,{{p:[-.15,.1,0.21],sh:80}});mainObj.add(g1);
            // iç dışli 2 (küçük)
            var g2=_m(new THREE.CylinderGeometry(.1,.1,.06,16),0xcccccc,{{p:[.15,-.05,0.21],sh:80}});mainObj.add(g2);
            // montaj civatalar
            for(var b=0;b<4;b++){{var bx=(b%2?1:-1)*.35,by=(b<2?1:-1)*.25;
            var bolt=_m(new THREE.CylinderGeometry(.03,.03,.06,6),0xcccccc,{{p:[bx,by,.21],sh:90}});mainObj.add(bolt);}}
        }}
        else if(T==14){{
            // KRANK MILI - ana mil, krank kollari, yatak boslulari
            var mainShaft=_m(new THREE.CylinderGeometry(.05,.05,2.5,10),0x888888,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(mainShaft);
            // krank kollari (4 silindir için)
            for(var c=0;c<4;c++){{var cx=-0.8+c*0.5;var offset=(c%2==0)?0.2:-0.2;
            // krank kolu
            var arm=_m(new THREE.BoxGeometry(.04,.3,.08),0xaaaaaa,{{p:[cx,offset*.5,0],sh:70}});mainObj.add(arm);
            // krank pimi
            var pin=_m(new THREE.CylinderGeometry(.04,.04,.12,8),0xbbbbbb,{{p:[cx,offset,0],r:[1.57,0,0],sh:90}});mainObj.add(pin);}}
            // karsi ağırlıklar
            for(var w=0;w<4;w++){{var wx=-0.8+w*0.5;var wo=(w%2==0)?-0.15:0.15;
            var cw=_m(new THREE.SphereGeometry(.06,8,8),0x999999,{{p:[wx,wo,0]}});mainObj.add(cw);}}
        }}
        else if(T==15){{
            // BIYEL KOLU - H-kesit, büyük/küçük göz, civatalar
            // govde (I-kesit)
            var web=_m(new THREE.BoxGeometry(.08,.9,.04),0xaaaaaa,{{p:[0,0,0],sh:80}});mainObj.add(web);
            var topFlange=_m(new THREE.BoxGeometry(.15,.04,.06),0xbbbbbb,{{p:[0,.45,0],sh:80}});mainObj.add(topFlange);
            var botFlange=_m(new THREE.BoxGeometry(.15,.04,.06),0xbbbbbb,{{p:[0,-.45,0],sh:80}});mainObj.add(botFlange);
            // büyük göz (krank tarafi)
            var bigEnd=_m(new THREE.TorusGeometry(.12,.04,8,16),0xaaaaaa,{{p:[0,-.5,0],sh:90}});mainObj.add(bigEnd);
            // küçük göz (piston tarafi)
            var smallEnd=_m(new THREE.TorusGeometry(.06,.03,8,12),0xbbbbbb,{{p:[0,.5,0],sh:90}});mainObj.add(smallEnd);
            // büyük göz civatalar
            var boltL=_m(new THREE.CylinderGeometry(.02,.02,.15,6),0xcccccc,{{p:[-.1,-.55,0],sh:80}});mainObj.add(boltL);
            var boltR=_m(new THREE.CylinderGeometry(.02,.02,.15,6),0xcccccc,{{p:[.1,-.55,0],sh:80}});mainObj.add(boltR);
        }}
        else if(T==16){{
            // SUPAP - supap kafasi, mil, yay, yatagi
            // supap kafasi (mantar)
            var head=_m(new THREE.CylinderGeometry(.15,.15,.04,16),0xaaaaaa,{{p:[0,-.4,0],sh:90}});mainObj.add(head);
            var seat=_m(new THREE.TorusGeometry(.15,.015,6,16),0x888888,{{p:[0,-.38,0],r:[1.57,0,0]}});mainObj.add(seat);
            // supap mili
            var stem=_m(new THREE.CylinderGeometry(.03,.03,.8,8),0xcccccc,{{p:[0,.0,0],sh:90}});mainObj.add(stem);
            // supap yayi
            for(var c=0;c<10;c++){{var coil=_m(new THREE.TorusGeometry(.08,.012,6,12),0xcccccc,{{p:[0,-.15+c*.06,0],r:[1.57,0,0],sh:80}});mainObj.add(coil);}}
            // kilavuz burc
            var guide=_m(new THREE.CylinderGeometry(.05,.05,.3,10),0x888888,{{p:[0,.3,0],sh:60}});mainObj.add(guide);
            // yatak
            var retainer=_m(new THREE.CylinderGeometry(.1,.1,.03,14),0xaaaaaa,{{p:[0,.45,0],sh:80}});mainObj.add(retainer);
        }}
        else if(T==17){{
            // ENJEKTOR - govde, nözül, bobin, yakit girişi
            var body=_m(new THREE.CylinderGeometry(.08,.1,.6,12),0x333333,{{p:[0,0,0],sh:60}});mainObj.add(body);
            // nözül
            var nozzle=_m(new THREE.ConeGeometry(.04,.15,8),0x555555,{{p:[0,-.38,0],r:[Math.PI,0,0],sh:80}});mainObj.add(nozzle);
            // bobin
            for(var c=0;c<8;c++){{var coil=_m(new THREE.TorusGeometry(.1,.008,6,12),0xcc8833,{{p:[0,-.1+c*.04,0],r:[1.57,0,0]}});mainObj.add(coil);}}
            // yakit girişi
            var inlet=_m(new THREE.CylinderGeometry(.03,.03,.2,8),0x444444,{{p:[0,.4,0]}});mainObj.add(inlet);
            // konnektoor
            var conn=_m(new THREE.BoxGeometry(.12,.08,.06),0x333333,{{p:[.1,.1,0]}});mainObj.add(conn);
            // sprey deseni
            for(var s=0;s<5;s++){{var sa=-0.3+s*0.15;
            var spray=_m(new THREE.CylinderGeometry(.002,.002,.2,4),0xffaa44,{{p:[Math.sin(sa)*.05,-.55,Math.cos(sa)*.05],r:[sa,0,0],em:0x664400,op:0.5}});mainObj.add(spray);}}
        }}
        else if(T==18){{
            // DIFERANSIYEL - mahfaza, tahrik dışlisi, gezegen dışlileri
            var housing=_m(new THREE.SphereGeometry(.5,16,16),0x888888,{{p:[0,0,0],op:0.3,sh:60}});mainObj.add(housing);
            // tahrik (ring) dışlisi
            var ring=_m(new THREE.TorusGeometry(.4,.04,8,32),0xaaaaaa,{{p:[0,0,0],sh:80}});mainObj.add(ring);
            // pinyon dışlisi
            var pinion=_m(new THREE.CylinderGeometry(.1,.1,.08,12),0xbbbbbb,{{p:[0,-.4,0],sh:80}});mainObj.add(pinion);
            // gezegen dışlileri (2)
            var pg1=_m(new THREE.CylinderGeometry(.08,.08,.06,10),0xcccccc,{{p:[-.15,0,.1],r:[1.57,0,0],sh:90}});mainObj.add(pg1);
            var pg2=_m(new THREE.CylinderGeometry(.08,.08,.06,10),0xcccccc,{{p:[.15,0,.1],r:[1.57,0,0],sh:90}});mainObj.add(pg2);
            // yari akslar
            var axL=_m(new THREE.CylinderGeometry(.04,.04,.6,8),0x888888,{{p:[-.7,0,0],r:[0,0,1.57],sh:80}});mainObj.add(axL);
            var axR=_m(new THREE.CylinderGeometry(.04,.04,.6,8),0x888888,{{p:[.7,0,0],r:[0,0,1.57],sh:80}});mainObj.add(axR);
            // giriş mili
            var input=_m(new THREE.CylinderGeometry(.03,.03,.5,8),0x888888,{{p:[0,-.7,0]}});mainObj.add(input);
        }}
        else if(T==19){{
            // AMORTISOR - dış tup, iç piston, yay, montaj gözleri
            var outerTube=_m(new THREE.CylinderGeometry(.12,.12,1.2,14),0x888888,{{p:[0,-.1,0],sh:60}});mainObj.add(outerTube);
            var innerRod=_m(new THREE.CylinderGeometry(.04,.04,.8,10),0xcccccc,{{p:[0,.6,0],sh:100}});mainObj.add(innerRod);
            // yay
            for(var c=0;c<14;c++){{var coil=_m(new THREE.TorusGeometry(.18,.015,8,16),0xcccccc,{{p:[0,-.5+c*.08,0],r:[1.57,0,0],sh:80}});mainObj.add(coil);}}
            // ust montaj göz
            var topMount=_m(new THREE.TorusGeometry(.04,.02,6,10),0xaaaaaa,{{p:[0,1.0,0],sh:80}});mainObj.add(topMount);
            // alt montaj göz
            var botMount=_m(new THREE.TorusGeometry(.05,.025,6,10),0xaaaaaa,{{p:[0,-.7,0],sh:80}});mainObj.add(botMount);
            // toz koruma (bellow)
            var boot=_m(new THREE.CylinderGeometry(.1,.13,.3,12),0x333333,{{p:[0,.3,0],op:0.6}});mainObj.add(boot);
        }}

        scene.add(mainObj);"""

    if ci == 14:  # Elektrik Devreleri — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        if(T==0){{
            // LED - kubbe, chip, reflektör, bacaklar, ışık
            var dome=_m(new THREE.SphereGeometry(.3,20,20,0,6.28,0,2.0),0xff0000,{{p:[0,.15,0],op:0.6,sh:100,em:0xaa0000}});mainObj.add(dome);
            var chip=_m(new THREE.BoxGeometry(.08,.04,.08),0xffcc00,{{p:[0,-.05,0],em:0x886600}});mainObj.add(chip);
            var base=_m(new THREE.CylinderGeometry(.3,.3,.1,20),0xcccccc,{{p:[0,-.12,0]}});mainObj.add(base);
            var legA=_m(new THREE.CylinderGeometry(.015,.015,.5,6),0xaaaaaa,{{p:[-.08,-.4,0]}});mainObj.add(legA);
            var legK=_m(new THREE.CylinderGeometry(.015,.015,.4,6),0xaaaaaa,{{p:[.08,-.35,0]}});mainObj.add(legK);
            var glow=_m(new THREE.SphereGeometry(.45,12,12),0xff2222,{{p:[0,.15,0],op:0.1,em:0xff0000}});mainObj.add(glow);
        }}
        else if(T==1){{
            // TRANSISTOR - govde, 3 bacak, tip
            var body=_m(new THREE.CylinderGeometry(.2,.2,.15,16),0x333333,{{p:[0,.1,0],r:[1.57,0,0],sh:50}});mainObj.add(body);
            var flat=_m(new THREE.BoxGeometry(.38,.15,.01),0x333333,{{p:[0,.1,-.1]}});mainObj.add(flat);
            // tab (ust)
            var tab=_m(new THREE.BoxGeometry(.12,.08,.01),0x333333,{{p:[0,.22,-.1]}});mainObj.add(tab);
            // 3 bacak (B,C,E)
            var legB=_m(new THREE.CylinderGeometry(.012,.012,.5,6),0xaaaaaa,{{p:[-.1,-.2,0]}});mainObj.add(legB);
            var legC=_m(new THREE.CylinderGeometry(.012,.012,.5,6),0xaaaaaa,{{p:[0,-.2,0]}});mainObj.add(legC);
            var legE=_m(new THREE.CylinderGeometry(.012,.012,.5,6),0xaaaaaa,{{p:[.1,-.2,0]}});mainObj.add(legE);
            // etiket noktalari
            var bLbl=_mb(new THREE.SphereGeometry(.025,6,6),0xff4444,{{p:[-.1,-.5,0]}});mainObj.add(bLbl);
            var cLbl=_mb(new THREE.SphereGeometry(.025,6,6),0x44ff44,{{p:[0,-.5,0]}});mainObj.add(cLbl);
            var eLbl=_mb(new THREE.SphereGeometry(.025,6,6),0x4444ff,{{p:[.1,-.5,0]}});mainObj.add(eLbl);
        }}
        else if(T==2){{
            // KONDANSATOR - elektrolitik, silindirik, kutupluluk
            var body=_m(new THREE.CylinderGeometry(.2,.2,.6,16),0x333399,{{p:[0,.1,0],sh:50}});mainObj.add(body);
            var stripe=_m(new THREE.CylinderGeometry(.21,.21,.03,16),0xaaaaaa,{{p:[0,.35,0]}});mainObj.add(stripe);
            // kutupluluk isareti
            var plus=_m(new THREE.BoxGeometry(.1,.015,.01),0xffffff,{{p:[0,.3,.21]}});mainObj.add(plus);
            var plus2=_m(new THREE.BoxGeometry(.015,.1,.01),0xffffff,{{p:[0,.3,.21]}});mainObj.add(plus2);
            // bacaklar
            var legP=_m(new THREE.CylinderGeometry(.015,.015,.4,6),0xaaaaaa,{{p:[-.06,-.25,0]}});mainObj.add(legP);
            var legN=_m(new THREE.CylinderGeometry(.015,.015,.35,6),0xaaaaaa,{{p:[.06,-.23,0]}});mainObj.add(legN);
            // degerler
            var label=_m(new THREE.BoxGeometry(.15,.08,.01),0x222266,{{p:[0,.1,.21]}});mainObj.add(label);
        }}
        else if(T==3){{
            // DIRENC - govde, renk bantlari, bacaklar
            var body=_m(new THREE.CylinderGeometry(.1,.1,.5,12),0xddbb88,{{p:[0,0,0],r:[0,0,1.57],sh:50}});mainObj.add(body);
            // 4 renk bandi
            var bandClrs=[0xff0000,0x000000,0xff8800,0xccaa00];
            for(var b=0;b<4;b++){{var band=_m(new THREE.CylinderGeometry(.105,.105,.03,12),bandClrs[b],{{p:[-.12+b*.08,0,0],r:[0,0,1.57]}});mainObj.add(band);}}
            // bacaklar
            var legL=_m(new THREE.CylinderGeometry(.012,.012,.4,6),0xaaaaaa,{{p:[-.45,0,0],r:[0,0,1.57]}});mainObj.add(legL);
            var legR=_m(new THREE.CylinderGeometry(.012,.012,.4,6),0xaaaaaa,{{p:[.45,0,0],r:[0,0,1.57]}});mainObj.add(legR);
        }}
        else if(T==4){{
            // BOBIN (Indüçtor) - sarim, cekirdek, bacaklar
            var core=_m(new THREE.CylinderGeometry(.06,.06,.6,8),0x555555,{{p:[0,0,0],r:[0,0,1.57]}});mainObj.add(core);
            for(var w=0;w<14;w++){{var coil=_m(new THREE.TorusGeometry(.12,.015,8,16),0xcc7722,{{p:[-.3+w*.045,0,0],r:[0,1.57,0],sh:60}});mainObj.add(coil);}}
            var legL=_m(new THREE.CylinderGeometry(.012,.012,.3,6),0xaaaaaa,{{p:[-.45,-.15,0]}});mainObj.add(legL);
            var legR=_m(new THREE.CylinderGeometry(.012,.012,.3,6),0xaaaaaa,{{p:[.45,-.15,0]}});mainObj.add(legR);
        }}
        else if(T==5){{
            // TRANSFORMATOR - E-I cekirdek, primer/sekonder sarim
            // E-I cekirdek
            var eCore=_m(new THREE.BoxGeometry(.15,.8,.6),0x555555,{{p:[-.2,0,0]}});mainObj.add(eCore);
            var iCore=_m(new THREE.BoxGeometry(.15,.8,.6),0x555555,{{p:[.2,0,0]}});mainObj.add(iCore);
            var topBar=_m(new THREE.BoxGeometry(.55,.1,.6),0x555555,{{p:[0,.35,0]}});mainObj.add(topBar);
            var botBar=_m(new THREE.BoxGeometry(.55,.1,.6),0x555555,{{p:[0,-.35,0]}});mainObj.add(botBar);
            // primer sarim (sol)
            for(var w=0;w<10;w++){{var pw=_m(new THREE.TorusGeometry(.18,.01,6,12),0xcc7722,{{p:[-.2,-.25+w*.05,0],r:[0,1.57,0]}});mainObj.add(pw);}}
            // sekonder sarim (sag)
            for(var w=0;w<14;w++){{var sw=_m(new THREE.TorusGeometry(.18,.008,6,12),0xcc4422,{{p:[.2,-.3+w*.045,0],r:[0,1.57,0]}});mainObj.add(sw);}}
        }}
        else if(T==6){{
            // ELEKTRIK MOTORU - stator, rotor, sarimlar, mil
            var stator=_m(new THREE.CylinderGeometry(.5,.5,.4,24),0x888888,{{p:[0,0,0],r:[1.57,0,0],sh:60}});mainObj.add(stator);
            var rotor=_m(new THREE.CylinderGeometry(.25,.25,.35,16),0xaaaaaa,{{p:[0,0,0],r:[1.57,0,0],sh:80}});mainObj.add(rotor);
            // sarimlar (stator)
            for(var s=0;s<6;s++){{var sa=s*1.047;
            var coil=_m(new THREE.BoxGeometry(.08,.12,.35),0xcc7722,{{p:[Math.cos(sa)*.38,Math.sin(sa)*.38,0],r:[0,0,sa]}});mainObj.add(coil);}}
            // mil
            var shaft=_m(new THREE.CylinderGeometry(.04,.04,.8,8),0xcccccc,{{p:[0,0,0],r:[1.57,0,0],sh:100}});mainObj.add(shaft);
            // donme oku
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,1,0),new THREE.Vector3(.6,.0,0),0.3,0xff8844,.06,.04));
        }}
        else if(T==7){{
            // JENERATOR - stator, rotor, mıknatıslar, çıkış klemens
            var body=_m(new THREE.CylinderGeometry(.45,.45,.5,20),0x666666,{{p:[0,0,0],r:[1.57,0,0],sh:50}});mainObj.add(body);
            // mıknatıslar (N/S)
            for(var m=0;m<4;m++){{var ma=m*1.57;var isN=m%2==0;
            var mag=_m(new THREE.BoxGeometry(.08,.2,.45),isN?0xff3333:0x3333ff,{{p:[Math.cos(ma)*.35,Math.sin(ma)*.35,0],r:[0,0,ma]}});mainObj.add(mag);}}
            // rotor bobini
            var rotorCoil=_m(new THREE.CylinderGeometry(.15,.15,.4,12),0xcc7722,{{p:[0,0,0],r:[1.57,0,0]}});mainObj.add(rotorCoil);
            var shaft=_m(new THREE.CylinderGeometry(.03,.03,.9,8),0xaaaaaa,{{p:[0,0,0],r:[1.57,0,0],sh:90}});mainObj.add(shaft);
            // çıkış terminalleri
            var termP=_m(new THREE.CylinderGeometry(.03,.03,.06,8),0xff4444,{{p:[.2,.3,.28]}});mainObj.add(termP);
            var termN=_m(new THREE.CylinderGeometry(.03,.03,.06,8),0x333333,{{p:[-.2,.3,.28]}});mainObj.add(termN);
        }}
        else if(T==8){{
            // BATARYA - silindirik pil, +/-, iç yapi
            var cell=_m(new THREE.CylinderGeometry(.2,.2,.8,16),0x333333,{{p:[0,0,0],sh:50}});mainObj.add(cell);
            // pozitif üçuz (cikinti)
            var pos=_m(new THREE.CylinderGeometry(.06,.06,.06,10),0xcccccc,{{p:[0,.43,0],sh:90}});mainObj.add(pos);
            // negatif üçuz (duz)
            var neg=_m(new THREE.CylinderGeometry(.2,.2,.02,16),0xaaaaaa,{{p:[0,-.41,0]}});mainObj.add(neg);
            // etiket
            var label=_m(new THREE.CylinderGeometry(.21,.21,.5,16),0xdd4444,{{p:[0,.05,0]}});mainObj.add(label);
            // + isareti
            var p1=_m(new THREE.BoxGeometry(.12,.03,.01),0xffffff,{{p:[0,.3,.21]}});mainObj.add(p1);
            var p2=_m(new THREE.BoxGeometry(.03,.12,.01),0xffffff,{{p:[0,.3,.21]}});mainObj.add(p2);
            // - isareti
            var m1=_m(new THREE.BoxGeometry(.1,.03,.01),0xffffff,{{p:[0,-.2,.21]}});mainObj.add(m1);
        }}
        else if(T==9){{
            // GUNES HUCRESI - fotovoltaik hüçre, katmanlar, kablolar
            var cell=_m(new THREE.BoxGeometry(1.0,.06,.8),0x1a2a6c,{{p:[0,.0,0],sh:90}});mainObj.add(cell);
            // hüçre grid cizgileri
            for(var g=0;g<8;g++){{var gridL=_m(new THREE.BoxGeometry(1.0,.07,.003),0xaaaaaa,{{p:[0,.04,-.35+g*.1]}});mainObj.add(gridL);}}
            // bus bar
            var busL=_m(new THREE.BoxGeometry(.005,.07,.8),0xaaaaaa,{{p:[-.3,.04,0]}});mainObj.add(busL);
            var busR=_m(new THREE.BoxGeometry(.005,.07,.8),0xaaaaaa,{{p:[.3,.04,0]}});mainObj.add(busR);
            // güneş ışıklari
            for(var r=0;r<5;r++){{mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(0,-1,0),new THREE.Vector3(-.4+r*.2,.7,0),0.3,0xffdd44,.05,.03));}}
            // çıkış kablolari
            var cableP=_m(new THREE.CylinderGeometry(.01,.01,.3,6),0xff4444,{{p:[.4,-.15,0]}});mainObj.add(cableP);
            var cableN=_m(new THREE.CylinderGeometry(.01,.01,.3,6),0x333333,{{p:[-.4,-.15,0]}});mainObj.add(cableN);
        }}
        else if(T==10){{
            // MIKRO CIP (IC) - DIP paketi, bacaklar, die
            var body=_m(new THREE.BoxGeometry(.5,.12,.25),0x333333,{{p:[0,.1,0],sh:40}});mainObj.add(body);
            // pin1 isareti
            var dot=_mb(new THREE.SphereGeometry(.02,6,6),0xaaaaaa,{{p:[-.2,.17,.1]}});mainObj.add(dot);
            // bacaklar (2x8=16 pin)
            for(var p=0;p<8;p++){{
            var pinT=_m(new THREE.BoxGeometry(.015,.08,.03),0xaaaaaa,{{p:[-.2+p*.055,.04,.15],sh:80}});mainObj.add(pinT);
            var pinB=_m(new THREE.BoxGeometry(.015,.08,.03),0xaaaaaa,{{p:[-.2+p*.055,.04,-.15],sh:80}});mainObj.add(pinB);}}
            // die (içerideki cip)
            var die=_m(new THREE.BoxGeometry(.15,.02,.1),0xaaaaaa,{{p:[0,.16,0],sh:100}});mainObj.add(die);
        }}
        else if(T==11){{
            // ANTEN - dipol, reflektör, elemanlar
            var boom=_m(new THREE.CylinderGeometry(.01,.01,1.5,6),0xaaaaaa,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(boom);
            // reflektör
            var reflector=_m(new THREE.CylinderGeometry(.01,.01,.6,6),0xaaaaaa,{{p:[-.5,0,0],sh:80}});mainObj.add(reflector);
            // direktör elemanlar
            for(var d=0;d<5;d++){{var dir=_m(new THREE.CylinderGeometry(.008,.008,.5-d*.04,6),0xcccccc,{{p:[.1+d*.2,0,0],sh:80}});mainObj.add(dir);}}
            // dipol (aktif)
            var dipoleL=_m(new THREE.CylinderGeometry(.012,.012,.25,6),0xcc7722,{{p:[-.1,.13,0]}});mainObj.add(dipoleL);
            var dipoleR=_m(new THREE.CylinderGeometry(.012,.012,.25,6),0xcc7722,{{p:[-.1,-.13,0]}});mainObj.add(dipoleR);
            // kablo
            var coax=_m(new THREE.CylinderGeometry(.008,.008,.5,6),0x333333,{{p:[-.1,0,-.25],r:[1.57,0,0]}});mainObj.add(coax);
        }}
        else if(T==12){{
            // ROLE - bobin, kontak, yay, govde
            var body=_m(new THREE.BoxGeometry(.5,.35,.3),0x444444,{{p:[0,.1,0],sh:40}});mainObj.add(body);
            // bobin
            for(var c=0;c<8;c++){{var coil=_m(new THREE.TorusGeometry(.1,.008,6,12),0xcc7722,{{p:[-.1,.1,-.05+c*.02],r:[1.57,0,0]}});mainObj.add(coil);}}
            // demir cekirdek
            var core=_m(new THREE.BoxGeometry(.06,.2,.12),0x888888,{{p:[-.1,.1,0]}});mainObj.add(core);
            // kontaklar
            var ncont=_m(new THREE.BoxGeometry(.04,.04,.15),0xcccccc,{{p:[.15,.2,0],sh:90}});mainObj.add(ncont);
            var comCont=_m(new THREE.BoxGeometry(.04,.04,.15),0xcccccc,{{p:[.15,.05,0],sh:90}});mainObj.add(comCont);
            // bacaklar
            for(var p=0;p<5;p++){{var pin=_m(new THREE.CylinderGeometry(.01,.01,.2,6),0xaaaaaa,{{p:[-.2+p*.1,-.1,0]}});mainObj.add(pin);}}
        }}
        else if(T==13){{
            // SIGORTA - cam tup, tel, kapaklar
            var tube=_m(new THREE.CylinderGeometry(.06,.06,.5,12),0xccddee,{{p:[0,0,0],r:[0,0,1.57],op:0.35,sh:100}});mainObj.add(tube);
            // tel (ince)
            var wire=_m(new THREE.CylinderGeometry(.003,.003,.4,4),0xdddddd,{{p:[0,0,0],r:[0,0,1.57],sh:80}});mainObj.add(wire);
            // metal kapaklar
            var capL=_m(new THREE.CylinderGeometry(.065,.065,.05,12),0xaaaaaa,{{p:[-.27,0,0],r:[0,0,1.57],sh:90}});mainObj.add(capL);
            var capR=_m(new THREE.CylinderGeometry(.065,.065,.05,12),0xaaaaaa,{{p:[.27,0,0],r:[0,0,1.57],sh:90}});mainObj.add(capR);
        }}
        else if(T==14){{
            // ANAHTAR - toggle switch, govde, kontaklar
            var body=_m(new THREE.BoxGeometry(.3,.15,.2),0x444444,{{p:[0,0,0],sh:40}});mainObj.add(body);
            var toggle=_m(new THREE.CylinderGeometry(.03,.03,.2,8),0xcccccc,{{p:[.05,.15,0],r:[0,0,-0.3],sh:80}});mainObj.add(toggle);
            var knob=_m(new THREE.SphereGeometry(.04,8,8),0xdddddd,{{p:[.08,.25,0]}});mainObj.add(knob);
            var termA=_m(new THREE.CylinderGeometry(.015,.015,.15,6),0xaaaaaa,{{p:[-.08,-.1,0]}});mainObj.add(termA);
            var termB=_m(new THREE.CylinderGeometry(.015,.015,.15,6),0xaaaaaa,{{p:[.08,-.1,0]}});mainObj.add(termB);
        }}
        else if(T==15){{
            // PRIZ - yüz plakası, yuvalar, topraklama
            var plate=_m(new THREE.BoxGeometry(.5,.5,.04),0xeeeeee,{{p:[0,0,0],sh:60}});mainObj.add(plate);
            var inner=_m(new THREE.CylinderGeometry(.18,.18,.06,20),0xdddddd,{{p:[0,0,.03]}});mainObj.add(inner);
            // yuvalar
            var slotL=_m(new THREE.BoxGeometry(.04,.12,.04),0x333333,{{p:[-.06,.05,.04]}});mainObj.add(slotL);
            var slotR=_m(new THREE.BoxGeometry(.04,.12,.04),0x333333,{{p:[.06,.05,.04]}});mainObj.add(slotR);
            // topraklama
            var ground=_m(new THREE.CylinderGeometry(.02,.02,.06,8),0xccaa33,{{p:[0,-.08,.04],r:[1.57,0,0]}});mainObj.add(ground);
        }}
        else if(T==16){{
            // OSILATOR - kristal + devre, sinyal çıkışi
            var pcb=_m(new THREE.BoxGeometry(.8,.04,.5),0x1a5c1a,{{p:[0,-.1,0]}});mainObj.add(pcb);
            var crystal=_m(new THREE.CylinderGeometry(.08,.08,.04,16),0xdddddd,{{p:[0,.0,0],sh:90}});mainObj.add(crystal);
            // sinyal dalgası
            for(var w=0;w<20;w++){{var wx=.2+w*.06;var wy=Math.sin(w*1.2)*0.15;
            var dot=_mb(new THREE.SphereGeometry(.015,6,6),0x44ff44,{{p:[wx,wy+.2,0]}});mainObj.add(dot);}}
            // IC
            var iç=_m(new THREE.BoxGeometry(.2,.06,.12),0x333333,{{p:[-.2,.0,0]}});mainObj.add(iç);
            // kondansator
            var cap=_m(new THREE.CylinderGeometry(.04,.04,.08,8),0x885522,{{p:[.1,.0,.15]}});mainObj.add(cap);
        }}
        else if(T==17){{
            // AMPLIFIKATOR - operasyonel amplifikator, giriş/çıkış
            var body=_m(new THREE.BoxGeometry(.06,.5,.5),0x333333,{{p:[0,0,0]}});mainObj.add(body);
            // üçgen sembol
            var tri1=_m(new THREE.BoxGeometry(.01,.4,.01),0xffffff,{{p:[0,0,-.2],r:[0,0,0.5]}});mainObj.add(tri1);
            // giriş pinleri
            var inP=_m(new THREE.CylinderGeometry(.01,.01,.3,4),0xaaaaaa,{{p:[-.18,.1,0],r:[0,0,1.57]}});mainObj.add(inP);
            var inN=_m(new THREE.CylinderGeometry(.01,.01,.3,4),0xaaaaaa,{{p:[-.18,-.1,0],r:[0,0,1.57]}});mainObj.add(inN);
            // + ve - isaretleri
            var pLbl=_mb(new THREE.SphereGeometry(.02,6,6),0x44ff44,{{p:[-.08,.1,0]}});mainObj.add(pLbl);
            var nLbl=_mb(new THREE.SphereGeometry(.02,6,6),0xff4444,{{p:[-.08,-.1,0]}});mainObj.add(nLbl);
            // çıkış
            var out=_m(new THREE.CylinderGeometry(.01,.01,.3,4),0xaaaaaa,{{p:[.18,0,0],r:[0,0,1.57]}});mainObj.add(out);
            // besleme pinleri
            var vcc=_m(new THREE.CylinderGeometry(.01,.01,.2,4),0xff4444,{{p:[0,.3,0]}});mainObj.add(vcc);
            var vee=_m(new THREE.CylinderGeometry(.01,.01,.2,4),0x4444ff,{{p:[0,-.3,0]}});mainObj.add(vee);
        }}
        else if(T==18){{
            // FILTRE DEVRESI - PCB, R, L, C bilesenleri
            var pcb=_m(new THREE.BoxGeometry(1.2,.04,.6),0x1a5c1a,{{p:[0,-.15,0]}});mainObj.add(pcb);
            // direnc
            var res=_m(new THREE.CylinderGeometry(.04,.04,.2,8),0xddbb88,{{p:[-.3,.0,0],r:[0,0,1.57]}});mainObj.add(res);
            // bobin
            for(var w=0;w<6;w++){{var coil=_m(new THREE.TorusGeometry(.05,.008,6,10),0xcc7722,{{p:[-.05+w*.025,.0,0],r:[0,1.57,0]}});mainObj.add(coil);}}
            // kondansatör
            var cap=_m(new THREE.CylinderGeometry(.06,.06,.12,10),0x333399,{{p:[.3,.0,0]}});mainObj.add(cap);
            // baglanti cizgileri (PCB iz)
            var tr1=_m(new THREE.BoxGeometry(.3,.015,.01),0x44aa44,{{p:[-.15,-.13,0],em:0x226622}});mainObj.add(tr1);
            var tr2=_m(new THREE.BoxGeometry(.3,.015,.01),0x44aa44,{{p:[.15,-.13,0],em:0x226622}});mainObj.add(tr2);
            // giriş/çıkış ok
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(-.6,.0,0),0.2,0xff4444,.04,.03));
            mainObj.add(new THREE.ArrowHelper(new THREE.Vector3(1,0,0),new THREE.Vector3(.45,.0,0),0.2,0x44ff44,.04,.03));
        }}
        else if(T==19){{
            // SENSOR - govde, algilama elemani, kablo, LED
            var body=_m(new THREE.CylinderGeometry(.12,.12,.4,14),0x333333,{{p:[0,0,0],sh:50}});mainObj.add(body);
            // algilama yüzeyi
            var sensor=_m(new THREE.CylinderGeometry(.1,.1,.02,14),0x224488,{{p:[0,.21,0],sh:100}});mainObj.add(sensor);
            // kablo
            var cable=_m(new THREE.CylinderGeometry(.025,.025,.5,8),0x444444,{{p:[0,-.45,0]}});mainObj.add(cable);
            // kablo üçlari (3 tel)
            var red=_m(new THREE.CylinderGeometry(.008,.008,.15,4),0xff0000,{{p:[-.03,-.72,0]}});mainObj.add(red);
            var blk=_m(new THREE.CylinderGeometry(.008,.008,.15,4),0x000000,{{p:[0,-.72,0]}});mainObj.add(blk);
            var yel=_m(new THREE.CylinderGeometry(.008,.008,.15,4),0xffff00,{{p:[.03,-.72,0]}});mainObj.add(yel);
            // LED gösterge
            var led=_m(new THREE.SphereGeometry(.03,8,8),0x44ff44,{{p:[.1,.0,.12],em:0x228822}});mainObj.add(led);
            // algilama dalgalari
            for(var w=0;w<3;w++){{var wave=_m(new THREE.TorusGeometry(.15+w*.08,.003,6,16,2.0),0x44aaff,{{p:[0,.3+w*.1,0],op:0.3-w*.08}});mainObj.add(wave);}}
        }}

        scene.add(mainObj);"""

    if ci == 15:  # Botanik — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mat=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||70,transparent:!!o.op,opacity:o.op||1.0,emissive:o.em||0,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mat=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1.0,wireframe:!!o.wf,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mat);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        if(T==0){{
            // CICEK YAPISI - tabanlik, canak, tac yaprak, erkek/dışi organ
            var stem=_m(new THREE.CylinderGeometry(.04,.05,.8,8),0x228B22,{{p:[0,-.3,0]}});mainObj.add(stem);
            // tabanlik (reseptakl)
            var recep=_m(new THREE.SphereGeometry(.12,12,12),0x44aa44,{{p:[0,.15,0]}});mainObj.add(recep);
            // canak yapraklar (sepal)
            for(var s=0;s<5;s++){{var sa=s*1.257;
            var sepal=_m(new THREE.SphereGeometry(.1,8,8),0x33aa33,{{p:[Math.cos(sa)*.2,.1,Math.sin(sa)*.2],s:[1.5,.3,1]}});mainObj.add(sepal);}}
            // tac yapraklar (petal)
            for(var p=0;p<5;p++){{var pa=p*1.257+0.628;
            var petal=_m(new THREE.SphereGeometry(.18,10,10),0xff66aa,{{p:[Math.cos(pa)*.25,.25,Math.sin(pa)*.25],s:[1.5,.3,1]}});mainObj.add(petal);}}
            // erkek organlar (stamen)
            for(var st=0;st<6;st++){{var sa=st*1.047;
            var filament=_m(new THREE.CylinderGeometry(.008,.008,.2,4),0xcccc44,{{p:[Math.cos(sa)*.08,.35,Math.sin(sa)*.08]}});mainObj.add(filament);
            var anther=_m(new THREE.SphereGeometry(.03,6,6),0xffcc00,{{p:[Math.cos(sa)*.08,.46,Math.sin(sa)*.08]}});mainObj.add(anther);}}
            // dışi organ (pistil)
            var style=_m(new THREE.CylinderGeometry(.015,.015,.25,6),0xaacc44,{{p:[0,.4,0]}});mainObj.add(style);
            var stigma=_m(new THREE.SphereGeometry(.04,8,8),0xccdd44,{{p:[0,.55,0]}});mainObj.add(stigma);
            var ovary=_m(new THREE.SphereGeometry(.08,10,10),0x44aa44,{{p:[0,.15,0]}});mainObj.add(ovary);
        }}
        else if(T==1){{
            // YAPRAK - yaprak ayi, damar sistemi, sap, stoma
            var blade=_m(new THREE.SphereGeometry(.6,16,16),0x44aa44,{{p:[0,.2,0],s:[1.2,.08,0.8],ds:true}});mainObj.add(blade);
            // ana damar (midrib)
            var midrib=_m(new THREE.CylinderGeometry(.015,.01,.9,6),0x33aa33,{{p:[0,.2,0],r:[0,0,0]}});mainObj.add(midrib);
            // yan damarlar
            for(var v=0;v<6;v++){{var vy=-.15+v*.1;
            var veinL=_m(new THREE.CylinderGeometry(.005,.003,.3,4),0x33aa33,{{p:[-.12,.2+vy*0.1,vy],r:[0.5,0,0.5]}});mainObj.add(veinL);
            var veinR=_m(new THREE.CylinderGeometry(.005,.003,.3,4),0x33aa33,{{p:[.12,.2+vy*0.1,vy],r:[0.5,0,-0.5]}});mainObj.add(veinR);}}
            // yaprak sapi (petiole)
            var petiole=_m(new THREE.CylinderGeometry(.02,.025,.3,6),0x228B22,{{p:[0,-.3,-.35],r:[0.5,0,0]}});mainObj.add(petiole);
        }}
        else if(T==2){{
            // KOK SISTEMI - ana kok, yan kokler, kok tuyleri, toprak
            // toprak kesiti
            var soil=_m(new THREE.BoxGeometry(1.5,.04,1.0),0x553311,{{p:[0,.0,0]}});mainObj.add(soil);
            // ana kok (kazikok)
            var mainRoot=_m(new THREE.CylinderGeometry(.05,.02,1.2,8),0xaa8855,{{p:[0,-.6,0]}});mainObj.add(mainRoot);
            // yan kokler
            for(var r=0;r<8;r++){{var ry=-.2-r*.12;var ra=(r%4)*1.57+r*.3;
            var lateral=_m(new THREE.CylinderGeometry(.02,.008,.4,6),0xbb9966,{{p:[Math.sin(ra)*.15,ry,Math.cos(ra)*.15],r:[Math.cos(ra)*0.5,0,-Math.sin(ra)*0.5]}});mainObj.add(lateral);}}
            // kok tuyleri (en alttaki üçlar)
            for(var h=0;h<20;h++){{var ha=(Math.random()-.5)*3.14;
            var hair=_m(new THREE.CylinderGeometry(.002,.002,.08,3),0xddcc99,{{p:[Math.sin(ha)*.04,-1.15+Math.random()*.1,Math.cos(ha)*.04],r:[ha*.3,0,ha*.2]}});mainObj.add(hair);}}
            // govde (ustte)
            var stem=_m(new THREE.CylinderGeometry(.04,.05,.4,8),0x228B22,{{p:[0,.2,0]}});mainObj.add(stem);
        }}
        else if(T==3){{
            // GOVDE KESITI - epidermis, korteks, ksilem, floem, öz
            var outer=_m(new THREE.CylinderGeometry(.6,.6,.15,24),0x44aa44,{{p:[0,0,0],r:[1.57,0,0]}});mainObj.add(outer);
            // epidermis
            var epid=_m(new THREE.TorusGeometry(.6,.03,8,32),0x33aa33,{{p:[0,0,.08]}});mainObj.add(epid);
            // korteks
            var cortex=_m(new THREE.CylinderGeometry(.5,.5,.02,24),0x66cc66,{{p:[0,0,.08]}});mainObj.add(cortex);
            // vaskuler demet halkasi
            for(var v=0;v<8;v++){{var va=v*0.785;
            // ksilem (iç)
            var xylem=_m(new THREE.CylinderGeometry(.06,.06,.04,8),0x884433,{{p:[Math.cos(va)*.35,Math.sin(va)*.35,.08],r:[1.57,0,0]}});mainObj.add(xylem);
            // floem (dış)
            var phloem=_m(new THREE.CylinderGeometry(.04,.04,.04,8),0x44aa44,{{p:[Math.cos(va)*.42,Math.sin(va)*.42,.08],r:[1.57,0,0]}});mainObj.add(phloem);}}
            // oz (pith)
            var pith=_m(new THREE.CylinderGeometry(.15,.15,.04,16),0xeeddcc,{{p:[0,0,.08]}});mainObj.add(pith);
        }}
        else if(T==4){{
            // TOHUM - tohum kabugu, embriyo, endosperm, kotiledon
            var coat=_m(new THREE.SphereGeometry(.5,20,20),0xaa8855,{{p:[0,0,0],sh:50}});mainObj.add(coat);
            // kesit gosterimi (yari seffaf)
            var half=_m(new THREE.SphereGeometry(.48,20,20,0,3.14),0xddccaa,{{p:[0,0,0],op:0.6}});mainObj.add(half);
            // endosperm
            var endosperm=_m(new THREE.SphereGeometry(.35,16,16,0,3.14),0xeeddbb,{{p:[0,0,0]}});mainObj.add(endosperm);
            // embriyo
            var embryo=_m(new THREE.SphereGeometry(.1,10,10),0x66aa44,{{p:[0,.15,0]}});mainObj.add(embryo);
            // kotiledonlar (2)
            var cotL=_m(new THREE.SphereGeometry(.15,10,10),0x88bb66,{{p:[-.12,.0,0],s:[1,.5,1]}});mainObj.add(cotL);
            var cotR=_m(new THREE.SphereGeometry(.15,10,10),0x88bb66,{{p:[.12,.0,0],s:[1,.5,1]}});mainObj.add(cotR);
            // hilum
            var hilum=_m(new THREE.SphereGeometry(.04,8,8),0x665533,{{p:[0,-.5,0]}});mainObj.add(hilum);
        }}
        else if(T==5){{
            // MEYVE - elma kesiti, carpel, tohum, kabuk, oz
            var skin=_m(new THREE.SphereGeometry(.6,20,20),0xcc2222,{{p:[0,0,0],sh:60}});mainObj.add(skin);
            // kesit (yari)
            var flesh=_m(new THREE.SphereGeometry(.55,20,20,0,3.14),0xeedd88,{{p:[0,0,0]}});mainObj.add(flesh);
            // oz bölgesi
            var core=_m(new THREE.SphereGeometry(.15,12,12),0xccbb88,{{p:[0,0,0]}});mainObj.add(core);
            // tohumlar
            for(var s=0;s<5;s++){{var sa=s*1.257;
            var seed=_m(new THREE.SphereGeometry(.04,8,8),0x553322,{{p:[Math.cos(sa)*.1,Math.sin(sa)*.1,0]}});mainObj.add(seed);}}
            // sap
            var stem=_m(new THREE.CylinderGeometry(.02,.015,.2,6),0x885533,{{p:[0,.65,0]}});mainObj.add(stem);
            // canak yaprak kalıntısi
            var calyx=_m(new THREE.SphereGeometry(.05,6,6),0x668844,{{p:[0,-.6,0]}});mainObj.add(calyx);
        }}
        else if(T==6){{
            // MANTAR - sapka, sap, lamel, spor, miselium
            var cap=_m(new THREE.SphereGeometry(.45,20,12,0,6.28,0,1.57),0xcc4422,{{p:[0,.4,0]}});mainObj.add(cap);
            // sapka benekleri
            for(var s=0;s<8;s++){{var sa=s*0.785;var sr=0.2+Math.random()*0.15;
            var spot=_m(new THREE.SphereGeometry(.04,6,6),0xffffff,{{p:[Math.cos(sa)*sr,.55+Math.random()*.1,Math.sin(sa)*sr]}});mainObj.add(spot);}}
            // lameller
            for(var l=0;l<12;l++){{var la=l*0.524;
            var gill=_m(new THREE.BoxGeometry(.3,.005,.04),0xddbbaa,{{p:[Math.cos(la)*.15,.35,Math.sin(la)*.15],r:[0,la,0]}});mainObj.add(gill);}}
            // sap
            var stipe=_m(new THREE.CylinderGeometry(.06,.08,.5,10),0xddccaa,{{p:[0,.05,0]}});mainObj.add(stipe);
            // etek (ring)
            var ring=_m(new THREE.TorusGeometry(.08,.01,6,12),0xddddcc,{{p:[0,.2,0],r:[1.57,0,0]}});mainObj.add(ring);
            // miselium
            for(var m=0;m<10;m++){{var ma=m*0.628;
            var hypha=_m(new THREE.CylinderGeometry(.003,.003,.2,3),0xccccbb,{{p:[Math.sin(ma)*.1,-.25,Math.cos(ma)*.1],r:[Math.random()*.5,0,Math.random()-.5]}});mainObj.add(hypha);}}
        }}
        else if(T==7){{
            // YOSUN - tallus, rizoid, sporangium
            // su yüzeyi
            var water=_m(new THREE.BoxGeometry(1.5,.02,1.0),0x2266aa,{{p:[0,-.6,0],op:0.3}});mainObj.add(water);
            // kaya
            var rock=_m(new THREE.DodecahedronGeometry(.3),0x888877,{{p:[0,-.4,0]}});mainObj.add(rock);
            // yosun kumeleri
            for(var y=0;y<15;y++){{var ya=y*0.42;var yr=0.2+Math.random()*0.15;
            var frond=_m(new THREE.CylinderGeometry(.01,.015,.15+Math.random()*.15,4),0x228844,{{p:[Math.cos(ya)*yr,-.2+Math.random()*.2,Math.sin(ya)*yr],r:[Math.random()*.3,0,Math.random()-.5]}});mainObj.add(frond);}}
        }}
        else if(T==8){{
            // KAKTUS - silindirik govde, dikenler, çiçek, kok
            var body=_m(new THREE.CylinderGeometry(.2,.25,.8,12),0x447733,{{p:[0,0,0]}});mainObj.add(body);
            // kaburgalar (8)
            for(var r=0;r<8;r++){{var ra=r*0.785;
            var rib=_m(new THREE.BoxGeometry(.03,.7,.04),0x448833,{{p:[Math.cos(ra)*.22,.0,Math.sin(ra)*.22],r:[0,ra,0]}});mainObj.add(rib);}}
            // dikenler
            for(var s=0;s<20;s++){{var sa=s*0.314;var sy=-.25+s*.04;
            var spine=_m(new THREE.ConeGeometry(.008,.1,3),0xdddd88,{{p:[Math.cos(sa)*.28,sy,Math.sin(sa)*.28],r:[0,0,-Math.cos(sa)*1.2]}});mainObj.add(spine);}}
            // çiçek (ust)
            for(var p=0;p<5;p++){{var pa=p*1.257;
            var petal=_m(new THREE.SphereGeometry(.08,8,8),0xff6688,{{p:[Math.cos(pa)*.1,.5,Math.sin(pa)*.1],s:[1.5,.4,1]}});mainObj.add(petal);}}
            // toprak
            var soil=_m(new THREE.CylinderGeometry(.3,.3,.03,16),0x553311,{{p:[0,-.42,0]}});mainObj.add(soil);
        }}
        else if(T==9){{
            // MESE AGACI - govde, dallar, yaprak kumesi, meyveler
            var trunk=_m(new THREE.CylinderGeometry(.08,.12,.8,8),0x885533,{{p:[0,-.5,0]}});mainObj.add(trunk);
            // ana dallar
            for(var b=0;b<5;b++){{var ba=b*1.257;var bH=-.1+b*.12;
            var branch=_m(new THREE.CylinderGeometry(.02,.04,.4,6),0x886644,{{p:[Math.cos(ba)*.2,bH,Math.sin(ba)*.2],r:[Math.cos(ba)*0.5,0,-Math.sin(ba)*0.5]}});mainObj.add(branch);}}
            // yaprak kumesi (büyük kure)
            var canopy=_m(new THREE.SphereGeometry(.6,16,16),0x228B22,{{p:[0,.3,0]}});mainObj.add(canopy);
            var canopy2=_m(new THREE.SphereGeometry(.4,12,12),0x33aa33,{{p:[.3,.2,0]}});mainObj.add(canopy2);
            var canopy3=_m(new THREE.SphereGeometry(.35,12,12),0x2d9e2d,{{p:[-.25,.25,.2]}});mainObj.add(canopy3);
            // palamutlar
            for(var a=0;a<3;a++){{var ac=_m(new THREE.SphereGeometry(.03,8,8),0x885533,{{p:[(a-1)*.15,-.15,.4]}});mainObj.add(ac);}}
        }}
        else if(T==10){{
            // CAM AGACI - ignemsi govde, koni şekli, kozalak
            var trunk=_m(new THREE.CylinderGeometry(.06,.1,.8,8),0x885533,{{p:[0,-.5,0]}});mainObj.add(trunk);
            // koni şeklinde dallar
            for(var l=0;l<5;l++){{var ly=-.2+l*.25;var lr=.5-l*.08;
            var layer=_m(new THREE.ConeGeometry(lr,.2,12),0x225522,{{p:[0,ly,0]}});mainObj.add(layer);}}
            // kozalaklar
            for(var c=0;c<3;c++){{var ca=c*2.094;
            var cone=_m(new THREE.ConeGeometry(.04,.1,8),0x885533,{{p:[Math.cos(ca)*.2,-.3,Math.sin(ca)*.2],r:[Math.PI,0,0]}});mainObj.add(cone);}}
        }}
        else if(T==11){{
            // PALMIYE - uzun govde, yaprak tacı, Hindistan cevizi
            var trunk=_m(new THREE.CylinderGeometry(.06,.08,1.6,10),0xaa8855,{{p:[0,.0,0]}});mainObj.add(trunk);
            // govde halkalari
            for(var r=0;r<10;r++){{var ring=_m(new THREE.TorusGeometry(.07,.01,6,12),0xbb9966,{{p:[0,-.7+r*.16,0],r:[1.57,0,0]}});mainObj.add(ring);}}
            // yaprak taclari (palmiye yapragi)
            for(var f=0;f<8;f++){{var fa=f*0.785;
            var frond=_m(new THREE.CylinderGeometry(.008,.005,.7,4),0x33aa33,{{p:[Math.cos(fa)*.3,.95,Math.sin(fa)*.3],r:[Math.cos(fa)*0.8,0,-Math.sin(fa)*0.8]}});mainObj.add(frond);
            // yapraklar
            for(var l=0;l<4;l++){{var leaf=_m(new THREE.SphereGeometry(.06,6,6),0x44bb44,{{p:[Math.cos(fa)*(.15+l*.15),.95-l*.03,Math.sin(fa)*(.15+l*.15)],s:[1,.2,1]}});mainObj.add(leaf);}}}}
            // hindistan cevizi
            var coconut=_m(new THREE.SphereGeometry(.06,10,10),0x885533,{{p:[.15,.7,0]}});mainObj.add(coconut);
        }}
        else if(T==12){{
            // EGRELTI OTU - rizom, yaprak, sorus, fiddlehead
            var rhizome=_m(new THREE.CylinderGeometry(.03,.04,.4,6),0x885533,{{p:[0,-.5,0],r:[0,0,0.3]}});mainObj.add(rhizome);
            // yaprak saplari (frond)
            for(var f=0;f<5;f++){{var fa=f*0.4-0.8;
            var stipe=_m(new THREE.CylinderGeometry(.012,.015,.6,6),0x228B22,{{p:[fa*.3,-.1,0],r:[0,0,fa*0.3]}});mainObj.add(stipe);
            // yapraklar (pinna)
            for(var p=0;p<6;p++){{var py=-.3+p*.1;
            var pinna=_m(new THREE.SphereGeometry(.06,6,6),0x33aa33,{{p:[fa*.3+.08,py+.1,0],s:[2,.3,1]}});mainObj.add(pinna);
            var pinna2=_m(new THREE.SphereGeometry(.06,6,6),0x33aa33,{{p:[fa*.3-.08,py+.1,0],s:[2,.3,1]}});mainObj.add(pinna2);}}}}
            // fiddlehead (kivrik üç)
            var fiddle=_m(new THREE.TorusGeometry(.05,.01,6,12,4.0),0x44aa44,{{p:[.4,.25,0]}});mainObj.add(fiddle);
        }}
        else if(T==13){{
            // ORKIDE - gov, hava kokleri, çiçek, pseudobulb
            var stem=_m(new THREE.CylinderGeometry(.025,.03,.5,8),0x228B22,{{p:[0,.1,0]}});mainObj.add(stem);
            // pseudobulb
            var bulb=_m(new THREE.SphereGeometry(.1,10,10),0x44aa44,{{p:[0,-.2,0],s:[1,1.5,1]}});mainObj.add(bulb);
            // çiçek (3 sepal + 3 petal + labellum)
            for(var s=0;s<3;s++){{var sa=s*2.094;
            var sepal=_m(new THREE.SphereGeometry(.12,8,8),0xcc44aa,{{p:[Math.cos(sa)*.2,.5,Math.sin(sa)*.2],s:[1.5,.3,1]}});mainObj.add(sepal);}}
            for(var p=0;p<2;p++){{var pa=p*2.094+1.047;
            var petal=_m(new THREE.SphereGeometry(.1,8,8),0xdd66bb,{{p:[Math.cos(pa)*.15,.5,Math.sin(pa)*.15],s:[1.5,.4,1]}});mainObj.add(petal);}}
            // labellum (dudak)
            var lip=_m(new THREE.SphereGeometry(.15,10,10),0xff88cc,{{p:[0,.45,.15],s:[1.2,.5,1.5]}});mainObj.add(lip);
            // hava kokleri
            for(var r=0;r<4;r++){{var root=_m(new THREE.CylinderGeometry(.008,.005,.3,4),0xaabb88,{{p:[(r-1.5)*.08,-.4,0],r:[0.3,0,(r-1.5)*0.2]}});mainObj.add(root);}}
        }}
        else if(T==14){{
            // GUL - gonca, yapraklar, dikenler, sap
            var stem=_m(new THREE.CylinderGeometry(.03,.04,.9,8),0x228B22,{{p:[0,-.2,0]}});mainObj.add(stem);
            // dikenler
            for(var t=0;t<6;t++){{var thorn=_m(new THREE.ConeGeometry(.015,.06,4),0x885533,{{p:[(t%2?1:-1)*.04,-.5+t*.12,0],r:[0,0,(t%2?-1:1)*1.0]}});mainObj.add(thorn);}}
            // gonca (katmanli yapraklar)
            for(var l=0;l<12;l++){{var la=l*0.524+l*.1;var lr=.08+l*.015;var lh=.35+l*.02;
            var petal=_m(new THREE.SphereGeometry(lr,8,8),0xcc2244,{{p:[Math.cos(la)*lr*.8,lh,Math.sin(la)*lr*.8],s:[1.5,.3,1]}});mainObj.add(petal);}}
            // yapraklar (bileşik)
            for(var lf=0;lf<3;lf++){{var lfA=lf*1.5-1.5;
            var leaf=_m(new THREE.SphereGeometry(.08,8,8),0x33aa33,{{p:[.15,-.3+lf*.15,0],s:[2,.3,1]}});mainObj.add(leaf);}}
        }}
        else if(T==15){{
            // PAPATYA - disk + ray çiçekler, involukr, sap
            var stem=_m(new THREE.CylinderGeometry(.025,.03,.6,8),0x228B22,{{p:[0,-.2,0]}});mainObj.add(stem);
            // disk (merkez)
            var disk=_m(new THREE.CylinderGeometry(.15,.15,.04,20),0xffcc00,{{p:[0,.15,0]}});mainObj.add(disk);
            // ray çiçekler (beyaz yapraklar)
            for(var r=0;r<16;r++){{var ra=r*0.393;
            var ray=_m(new THREE.SphereGeometry(.1,8,8),0xffffff,{{p:[Math.cos(ra)*.28,.15,Math.sin(ra)*.28],s:[1.8,.2,.6],r:[0,ra,0]}});mainObj.add(ray);}}
            // involukr (canak yapraklar)
            for(var i=0;i<8;i++){{var ia=i*0.785;
            var bract=_m(new THREE.SphereGeometry(.06,6,6),0x44aa44,{{p:[Math.cos(ia)*.18,.08,Math.sin(ia)*.18],s:[1.5,.3,.8]}});mainObj.add(bract);}}
            // yapraklar
            var leaf1=_m(new THREE.SphereGeometry(.08,8,8),0x33aa33,{{p:[.12,-.15,0],s:[2.5,.3,1]}});mainObj.add(leaf1);
            var leaf2=_m(new THREE.SphereGeometry(.08,8,8),0x33aa33,{{p:[-.1,-.25,0],s:[2.5,.3,1]}});mainObj.add(leaf2);
        }}
        else if(T==16){{
            // LALE - sogan, sap, yaprak, çiçek
            var bulb=_m(new THREE.SphereGeometry(.15,12,12),0xaa8855,{{p:[0,-.65,0],s:[1,1.2,1]}});mainObj.add(bulb);
            var stem=_m(new THREE.CylinderGeometry(.03,.04,.8,8),0x228B22,{{p:[0,-.15,0]}});mainObj.add(stem);
            // yapraklar (uzun sivri)
            for(var l=0;l<3;l++){{var la=l*2.094;
            var leaf=_m(new THREE.CylinderGeometry(.005,.03,.5,6),0x33aa33,{{p:[Math.cos(la)*.08,-.3,Math.sin(la)*.08],r:[Math.cos(la)*0.1,0,-Math.sin(la)*0.1]}});mainObj.add(leaf);}}
            // çiçek (6 petal, kadeh şekli)
            for(var p=0;p<6;p++){{var pa=p*1.047;
            var petal=_m(new THREE.SphereGeometry(.12,8,8),0xff2244,{{p:[Math.cos(pa)*.12,.35,Math.sin(pa)*.12],s:[1,.8,.5]}});mainObj.add(petal);}}
            // erkek organlar
            for(var s=0;s<6;s++){{var sa=s*1.047;
            var stamen=_m(new THREE.CylinderGeometry(.005,.005,.1,4),0xffcc00,{{p:[Math.cos(sa)*.05,.35,Math.sin(sa)*.05]}});mainObj.add(stamen);}}
        }}
        else if(T==17){{
            // AYCICEGI - büyük disk, yapraklar, sap
            var stem=_m(new THREE.CylinderGeometry(.04,.06,1.2,8),0x228B22,{{p:[0,-.2,0]}});mainObj.add(stem);
            // büyük disk
            var disk=_m(new THREE.CylinderGeometry(.35,.35,.06,24),0x885522,{{p:[0,.45,0]}});mainObj.add(disk);
            // disk desen (spiral tohumlar)
            for(var s=0;s<30;s++){{var phi=s*2.4;var r=0.02*Math.sqrt(s);
            var seed=_m(new THREE.SphereGeometry(.015,4,4),0x444422,{{p:[Math.cos(phi)*r*5,.48,Math.sin(phi)*r*5]}});mainObj.add(seed);}}
            // yapraklar (büyük sari)
            for(var p=0;p<14;p++){{var pa=p*0.449;
            var petal=_m(new THREE.SphereGeometry(.15,8,8),0xffcc00,{{p:[Math.cos(pa)*.45,.45,Math.sin(pa)*.45],s:[1.5,.25,.6],r:[0,pa,0]}});mainObj.add(petal);}}
            // govde yapraklari
            for(var l=0;l<4;l++){{var leaf=_m(new THREE.SphereGeometry(.12,8,8),0x33aa33,{{p:[(l%2?1:-1)*.15,-.5+l*.2,0],s:[2.5,.3,1]}});mainObj.add(leaf);}}
        }}
        else if(T==18){{
            // NILUFER - su yüzeyi, yüzüçu yapraklar, çiçek
            var water=_m(new THREE.CylinderGeometry(1.0,1.0,.03,24),0x2266aa,{{p:[0,-.3,0],op:0.4}});mainObj.add(water);
            // yaprak (daire, yüzüçu)
            var pad=_m(new THREE.CylinderGeometry(.4,.4,.015,24),0x33aa33,{{p:[-.2,-.28,-.1]}});mainObj.add(pad);
            var pad2=_m(new THREE.CylinderGeometry(.3,.3,.015,20),0x338833,{{p:[.3,-.28,.2]}});mainObj.add(pad2);
            // çiçek
            for(var l=0;l<3;l++){{for(var p=0;p<8;p++){{var pa=p*0.785+l*0.2;var pr=.1+l*.06;
            var petal=_m(new THREE.SphereGeometry(.08-l*.01,8,8),l==0?0xff88cc:l==1?0xffaacc:0xffccdd,{{p:[Math.cos(pa)*pr,-.15+l*.05,Math.sin(pa)*pr],s:[1.3,.3,.8]}});mainObj.add(petal);}}}}
            // merkez (stamen)
            var center=_m(new THREE.SphereGeometry(.05,10,10),0xffdd44,{{p:[0,-.1,0]}});mainObj.add(center);
            // su kok sapi
            var rootStem=_m(new THREE.CylinderGeometry(.01,.01,.3,4),0x225522,{{p:[0,-.45,0]}});mainObj.add(rootStem);
        }}
        else if(T==19){{
            // YONCA - 3 yaprak, sap, çiçek
            var stem=_m(new THREE.CylinderGeometry(.015,.02,.4,6),0x228B22,{{p:[0,-.2,0]}});mainObj.add(stem);
            // 3 yaprak (trifoliate)
            for(var l=0;l<3;l++){{var la=l*2.094;
            var leaf=_m(new THREE.SphereGeometry(.15,10,10),0x33aa33,{{p:[Math.cos(la)*.12,.1,Math.sin(la)*.12],s:[1,.2,1]}});mainObj.add(leaf);
            // yaprak damar
            var vein=_m(new THREE.BoxGeometry(.005,.01,.1),0x228822,{{p:[Math.cos(la)*.12,.12,Math.sin(la)*.12],r:[0,la,0]}});mainObj.add(vein);}}
            // sap-yaprak baglantisi
            for(var p=0;p<3;p++){{var pa=p*2.094;
            var petiole=_m(new THREE.CylinderGeometry(.005,.005,.1,4),0x228B22,{{p:[Math.cos(pa)*.06,.02,Math.sin(pa)*.06],r:[Math.cos(pa)*0.5,0,-Math.sin(pa)*0.5]}});mainObj.add(petiole);}}
            // çiçek (küçük mor top)
            var flower=_m(new THREE.SphereGeometry(.08,10,10),0xcc44cc,{{p:[0,.2,0]}});mainObj.add(flower);
        }}

        scene.add(mainObj);"""

    if ci == 16:  # Jeoloji — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||60,transparent:!!o.op,opacity:o.op||1,flatShading:!!o.fs,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

        // T=0 Granit — taneli derinlik yapısı
        if(T==0){{
            var base=_m(new THREE.DodecahedronGeometry(.9),0x999999,{{fs:true}});mainObj.add(base);
            // feldspat taneleri (pembe)
            for(var i=0;i<18;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.6+Math.random()*.35;var g=_m(new THREE.BoxGeometry(.08+Math.random()*.06,.06+Math.random()*.04,.05+Math.random()*.04),0xdd9999,{{p:[Math.sin(b)*Math.cos(a)*r,Math.sin(b)*Math.sin(a)*r,Math.cos(b)*r],fs:true}});g.rotation.set(Math.random()*3,Math.random()*3,0);mainObj.add(g);}}
            // kuvars taneleri (beyazımsı)
            for(var i=0;i<12;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.55+Math.random()*.4;mainObj.add(_m(new THREE.SphereGeometry(.04+Math.random()*.03,6,6),0xeeeedd,{{p:[Math.sin(b)*Math.cos(a)*r,Math.sin(b)*Math.sin(a)*r,Math.cos(b)*r]}}));}}
            // mika pulları (siyah)
            for(var i=0;i<10;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.65+Math.random()*.3;mainObj.add(_m(new THREE.CylinderGeometry(.04,.04,.01,6),0x333333,{{p:[Math.sin(b)*Math.cos(a)*r,Math.sin(b)*Math.sin(a)*r,Math.cos(b)*r],sh:90}}));}}
        }}

        // T=1 Mermer — damarli parlak yapi
        if(T==1){{
            var body=_m(new THREE.SphereGeometry(.9,32,32),0xf5f0e8,{{sh:120}});mainObj.add(body);
            // mermer damarları (gri-yeşilimsi)
            for(var i=0;i<8;i++){{var curve=new THREE.TorusGeometry(.85+i*.01,.012,8,40,Math.PI*(0.6+Math.random()*.8));var vein=_m(curve,0x889988,{{r:[Math.random()*3.14,Math.random()*3.14,Math.random()*3.14],op:.6}});mainObj.add(vein);}}
            // parlak yüzey katmanı
            mainObj.add(_m(new THREE.SphereGeometry(.92,32,32),0xffffff,{{op:.08}}));
            // kesit düzlem (yarı gösterim)
            mainObj.add(_m(new THREE.PlaneGeometry(1.2,1.2),0xf8f4ec,{{p:[0,0,.65],op:.3}}));
        }}

        // T=2 Bazalt — köyü volkanik, sütunlu
        if(T==2){{
            // bazalt sütunları (altıgen prizma grubu)
            for(var i=0;i<7;i++){{var ang=i==0?0:i*1.047;var rx=i==0?0:Math.cos(ang)*.35;var rz=i==0?0:Math.sin(ang)*.35;var h=.8+Math.random()*.5;mainObj.add(_m(new THREE.CylinderGeometry(.17,.17,h,6),0x444444,{{p:[rx,-(.9-h)/2,rz],fs:true}}));}}
            // üst yüzey detayları
            for(var i=0;i<7;i++){{var ang=i==0?0:i*1.047;var rx=i==0?0:Math.cos(ang)*.35;var rz=i==0?0:Math.sin(ang)*.35;mainObj.add(_m(new THREE.CylinderGeometry(.16,.16,.02,6),0x555555,{{p:[rx,.45,rz]}}));}}
            // zemin kaya parçaları
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.DodecahedronGeometry(.08),0x3a3a3a,{{p:[(Math.random()-.5)*.8,-.7,(Math.random()-.5)*.8],fs:true}}));
        }}

        // T=3 Obsidyen — volkanik cam, parlak siyah
        if(T==3){{
            var body=_m(new THREE.DodecahedronGeometry(.85),0x111118,{{sh:150}});mainObj.add(body);
            // cam parlaklık katmanı
            mainObj.add(_m(new THREE.DodecahedronGeometry(.87),0x4444ff,{{op:.06}}));
            // kırılma yüzeyleri (keskin kenarlar)
            for(var i=0;i<6;i++){{var sz=.3+Math.random()*.2;mainObj.add(_m(new THREE.PlaneGeometry(sz,sz),0x222233,{{p:[(Math.random()-.5)*1,(Math.random()-.5)*1,(Math.random()-.5)*1],r:[Math.random()*3,Math.random()*3,0],op:.4,sh:200}}));}}
            // derin yansıma noktaları
            for(var i=0;i<8;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.02,6,6),0x8888ff,{{p:[(Math.random()-.5)*.6,(Math.random()-.5)*.6,(Math.random()-.5)*.6],op:.5}}));}}
        }}

        // T=4 Kuvars — altıgen kristal prizması
        if(T==4){{
            // ana kristal gövdesi (altıgen prizma)
            var body=_m(new THREE.CylinderGeometry(.35,.35,1.2,6),0xddddff,{{sh:120,op:.7}});mainObj.add(body);
            // üst piramit uç
            mainObj.add(_m(new THREE.ConeGeometry(.35,.45,6),0xddddff,{{p:[0,.82,0],sh:120,op:.7}}));
            // alt piramit uç
            mainObj.add(_m(new THREE.ConeGeometry(.35,.3,6),0xccccee,{{p:[0,-.75,0],r:[Math.PI,0,0],sh:100,op:.6}}));
            // iç yansıma eksen çizgisi
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,1.5,4),0xffffff,{{op:.2}}));
            // yüzey çizgileri (büyüme çizgileri)
            for(var i=0;i<6;i++){{var a=i*1.047;mainObj.add(_m(new THREE.BoxGeometry(.005,.9,.005),0xbbbbee,{{p:[Math.cos(a)*.35,0,Math.sin(a)*.35],op:.3}}));}}
            // ikincil küçük kristaller
            mainObj.add(_m(new THREE.CylinderGeometry(.12,.12,.4,6),0xeeeeff,{{p:[.45,-.3,.2],r:[0,0,.4],sh:120,op:.6}}));
            mainObj.add(_m(new THREE.ConeGeometry(.12,.15,6),0xeeeeff,{{p:[.55,-.1,.25],r:[0,0,.4],sh:120,op:.6}}));
        }}

        // T=5 Ametist — mor kristal kümesi
        if(T==5){{
            // kaya tabanı
            var base=_m(new THREE.DodecahedronGeometry(.5),0x887766,{{p:[0,-.4,0],s:[1.5,.5,1.2],fs:true}});mainObj.add(base);
            // ametist kristalleri (farklı boyutlarda)
            var crColors=[0x9944cc,0x8833bb,0xaa55dd,0x7722aa,0xbb66ee];
            for(var i=0;i<9;i++){{var h=.3+Math.random()*.6;var cr=.06+Math.random()*.08;var px=(Math.random()-.5)*.6;var pz=(Math.random()-.5)*.5;var cg=new THREE.CylinderGeometry(cr*.3,cr,h,6);mainObj.add(_m(cg,crColors[i%5],{{p:[px,-.1+h/2,pz],r:[Math.random()*.3-.15,0,Math.random()*.3-.15],sh:140,op:.75}}));}}
            // kristal uç parlamaları
            for(var i=0;i<6;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.02,6,6),0xdd88ff,{{p:[(Math.random()-.5)*.5,.3+Math.random()*.5,(Math.random()-.5)*.4],op:.6}}));}}
        }}

        // T=6 Elmas — sekizgen kristal
        if(T==6){{
            // oktahedron ana kristal
            var dia=_m(new THREE.OctahedronGeometry(.75),0xeeffff,{{sh:200,op:.5}});mainObj.add(dia);
            // iç ışık kırılması
            mainObj.add(_mb(new THREE.OctahedronGeometry(.3),0xffffff,{{op:.3}}));
            // facet highlight çizgileri
            for(var i=0;i<12;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.6;mainObj.add(_mb(new THREE.SphereGeometry(.015,4,4),0xffffff,{{p:[Math.sin(b)*Math.cos(a)*r,Math.cos(b)*r,Math.sin(b)*Math.sin(a)*r],op:.7}}));}}
            // gökkuşağı yansımaları
            var rClrs=[0xff4444,0x44ff44,0x4444ff,0xffff44,0xff44ff];
            for(var i=0;i<5;i++){{var a=i*1.256;mainObj.add(_mb(new THREE.PlaneGeometry(.1,.1),rClrs[i],{{p:[Math.cos(a)*.55,Math.sin(a)*.55,.3],r:[0,0,a],op:.25,ds:true}}));}}
            // dış parıltı
            mainObj.add(_m(new THREE.OctahedronGeometry(.8),0xffffff,{{op:.04}}));
        }}

        // T=7 Zümrüt — altıgen yeşil kristal
        if(T==7){{
            // ana gövde (altıgen prizma)
            mainObj.add(_m(new THREE.CylinderGeometry(.3,.3,1.1,6),0x22aa44,{{sh:130,op:.65}}));
            // üst piramit
            mainObj.add(_m(new THREE.ConeGeometry(.3,.35,6),0x22bb44,{{p:[0,.72,0],sh:130,op:.65}}));
            // alt piramit
            mainObj.add(_m(new THREE.ConeGeometry(.3,.25,6),0x199938,{{p:[0,-.67,0],r:[Math.PI,0,0],sh:110,op:.6}}));
            // iç inklüzyonlar (küçük kabarcıklar)
            for(var i=0;i<8;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.02+Math.random()*.02,6,6),0x44cc66,{{p:[(Math.random()-.5)*.3,(Math.random()-.5)*.6,(Math.random()-.5)*.3],op:.3}}));}}
            // yüzey çatlakları
            for(var i=0;i<4;i++){{mainObj.add(_m(new THREE.BoxGeometry(.003,.4+Math.random()*.3,.003),0x118833,{{p:[(Math.random()-.5)*.2,(Math.random()-.5)*.4,(Math.random()-.5)*.2],op:.5}}));}}
            // ana kaya matris
            mainObj.add(_m(new THREE.DodecahedronGeometry(.35),0x887766,{{p:[-.5,-.3,.2],fs:true,s:[1,.6,.8]}}));
        }}

        // T=8 Yakut — kırmızı korund kristali
        if(T==8){{
            // ana altıgen prizma gövde
            mainObj.add(_m(new THREE.CylinderGeometry(.35,.35,.9,6),0xcc1133,{{sh:150,op:.7}}));
            // üst düz terminasyon
            mainObj.add(_m(new THREE.CylinderGeometry(.33,.35,.05,6),0xdd2244,{{p:[0,.47,0],sh:160}}));
            // alt terminasyon
            mainObj.add(_m(new THREE.CylinderGeometry(.35,.33,.05,6),0xbb0022,{{p:[0,-.47,0],sh:140}}));
            // iç parıltı (yıldız etkisi - asterism)
            for(var i=0;i<3;i++){{var a=i*1.047;mainObj.add(_mb(new THREE.BoxGeometry(.005,.7,.005),0xff4466,{{r:[0,0,a],op:.4}}));}}
            // dış glow
            mainObj.add(_m(new THREE.CylinderGeometry(.4,.4,.95,6),0xff2244,{{op:.06,em:0xff2244,ei:.3}}));
            // kaya matrisi
            mainObj.add(_m(new THREE.DodecahedronGeometry(.3),0x998877,{{p:[.55,-.2,0],fs:true}}));
        }}

        // T=9 Safir — mavi korund kristali
        if(T==9){{
            // ana gövde (altıgen bipiramit)
            mainObj.add(_m(new THREE.CylinderGeometry(.32,.32,.8,6),0x2244aa,{{sh:150,op:.7}}));
            mainObj.add(_m(new THREE.ConeGeometry(.32,.4,6),0x2255bb,{{p:[0,.6,0],sh:150,op:.7}}));
            mainObj.add(_m(new THREE.ConeGeometry(.32,.35,6),0x1133aa,{{p:[0,-.57,0],r:[Math.PI,0,0],sh:140,op:.65}}));
            // iç glow
            mainObj.add(_mb(new THREE.SphereGeometry(.2,16,16),0x4488ff,{{op:.15}}));
            // zonlama çizgileri
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.TorusGeometry(.32,.005,4,6),0x3366cc,{{p:[0,-.3+i*.15,0],r:[Math.PI/2,0,0],op:.4}}));
            // yıldız etkisi
            for(var i=0;i<3;i++){{var a=i*1.047;mainObj.add(_mb(new THREE.BoxGeometry(.004,.6,.004),0x88aaff,{{r:[0,0,a],op:.35}}));}}
        }}

        // T=10 Fosil — taş içinde korunmuş organizma
        if(T==10){{
            // sedimanter kaya matris
            var rock=_m(new THREE.BoxGeometry(1.6,1.1,.5),0xccbb99,{{s:[1,1,1]}});mainObj.add(rock);
            // ammonit spiral fosil
            for(var i=0;i<28;i++){{var a=i*.35;var r=.05+i*.015;var fx=Math.cos(a)*r;var fy=Math.sin(a)*r;mainObj.add(_m(new THREE.SphereGeometry(.03+i*.001,6,6),0xaa9966,{{p:[fx,fy,.26]}}));}}
            // kaburgalar (ammonit çizgileri)
            for(var i=0;i<12;i++){{var a=i*.6;var r=.08+i*.03;mainObj.add(_m(new THREE.BoxGeometry(.005,.04,.02),0x998855,{{p:[Math.cos(a)*r,Math.sin(a)*r,.27],r:[0,0,a]}}));}}
            // ikinci küçük fosil (trilobit)
            mainObj.add(_m(new THREE.SphereGeometry(.1,8,8),0xbb9977,{{p:[.5,-.2,.26],s:[1,.6,.3]}}));
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.BoxGeometry(.18,.005,.01),0xaa8866,{{p:[.5,-.15+i*.03,.27]}}));
            // taş çatlakları
            for(var i=0;i<3;i++)mainObj.add(_m(new THREE.BoxGeometry(.005,.4+Math.random()*.3,.01),0xbbaa88,{{p:[(Math.random()-.5)*1.2,(Math.random()-.5)*.6,.26],r:[0,0,Math.random()*1-.5]}}));
        }}

        // T=11 Stalaktit — mağara oluşumu
        if(T==11){{
            // mağara tavanı
            mainObj.add(_m(new THREE.BoxGeometry(2.5,.2,1.8),0x776655,{{p:[0,1.1,0]}}));
            // stalaktitler (tavandan sarkan)
            for(var i=0;i<7;i++){{var px=(i-3)*.3;var h=.4+Math.random()*.7;mainObj.add(_m(new THREE.ConeGeometry(.05+Math.random()*.04,h,8),0xccbbaa,{{p:[px,1-h/2,(Math.random()-.5)*.3],sh:80}}));}}
            // stalagmitler (tabandan yükselen)
            var floor_y=-0.8;
            mainObj.add(_m(new THREE.BoxGeometry(2.5,.15,1.8),0x665544,{{p:[0,floor_y,0]}}));
            for(var i=0;i<5;i++){{var px=(i-2)*.35;var h=.3+Math.random()*.5;mainObj.add(_m(new THREE.ConeGeometry(.06+Math.random()*.04,h,8),0xddccbb,{{p:[px,floor_y+.075+h/2,(Math.random()-.5)*.3],r:[Math.PI,0,0],sh:70}}));}}
            // su damlası
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x88bbff,{{p:[0,.55,0],op:.7}}));
            // su birikintisi
            mainObj.add(_m(new THREE.CylinderGeometry(.4,.45,.02,16),0x5588aa,{{p:[0,floor_y+.08,0],op:.4,sh:120}}));
        }}

        // T=12 Magma Odası — yeraltı magma deposu
        if(T==12){{
            // yer kabuğu kesiti
            mainObj.add(_m(new THREE.BoxGeometry(2.2,1.2,1.5),0x8B7355,{{p:[0,.5,0],op:.4}}));
            // magma odası (büyük boşluk)
            mainObj.add(_m(new THREE.SphereGeometry(.7,20,20),0xff3300,{{p:[0,-.1,0],em:0xff2200,ei:.5,s:[1.3,.8,1]}}));
            // kızgın magma parçacıkları
            for(var i=0;i<20;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.02+Math.random()*.03,6,6),0xff6600,{{p:[(Math.random()-.5)*1,(Math.random()-.5)*.5-.1,(Math.random()-.5)*.8],op:.6+Math.random()*.4}}));}}
            // magma kanalı (yukarı baca)
            mainObj.add(_m(new THREE.CylinderGeometry(.08,.15,.8,10),0xff4400,{{p:[0,.7,0],em:0xff2200,ei:.3,op:.6}}));
            // volkan tepesi (üstte)
            mainObj.add(_m(new THREE.ConeGeometry(.35,.3,12),0x776655,{{p:[0,1.2,0]}}));
            // yan kanallar
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.06,.5,8),0xff5500,{{p:[.4,.3,0],r:[0,0,.6],em:0xff2200,ei:.2,op:.5}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.06,.4,8),0xff5500,{{p:[-.35,.2,0],r:[0,0,-.5],em:0xff2200,ei:.2,op:.5}}));
        }}

        // T=13 Sediman Katman — tortul tabakalar
        if(T==13){{
            var layerColors=[0xddcc99,0xbb9966,0xccaa77,0x998855,0xddbb88,0xaa8844,0xccbb99,0x887744];
            var yy=-0.8;
            for(var i=0;i<8;i++){{var h=.15+Math.random()*.1;mainObj.add(_m(new THREE.BoxGeometry(1.8,h,1.2),layerColors[i],{{p:[0,yy+h/2,0]}}));yy+=h;}}
            // fosil katman işaretleri
            for(var i=0;i<4;i++){{mainObj.add(_m(new THREE.SphereGeometry(.03,6,6),0x776644,{{p:[(Math.random()-.5)*1.2,-.8+i*.35+Math.random()*.1,.61]}}));}}
            // erozyon çizgileri (üst)
            for(var i=0;i<3;i++)mainObj.add(_m(new THREE.BoxGeometry(1.6,.005,.005),0x997755,{{p:[0,yy-.05,(Math.random()-.5)*.8]}}));
            // ölçek çubuğu (yanda)
            mainObj.add(_m(new THREE.BoxGeometry(.02,yy+.8,.02),0x333333,{{p:[1,yy/2-.4,0]}}));
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.BoxGeometry(.06,.005,.005),0x333333,{{p:[1,-.8+i*(yy+.8)/4,0]}}));
        }}

        // T=14 Fay Hattı — kırılma ve kayma
        if(T==14){{
            // sol blok (yukarı kalkmış)
            mainObj.add(_m(new THREE.BoxGeometry(1,.9,1.2),0xbb9966,{{p:[-.55,.15,0]}}));
            // sağ blok (aşağı kaymış)
            mainObj.add(_m(new THREE.BoxGeometry(1,.9,1.2),0xaa8855,{{p:[.55,-.15,0]}}));
            // fay düzlemi (arası)
            mainObj.add(_m(new THREE.PlaneGeometry(.05,1.2),0x553322,{{p:[0,0,.61],r:[0,0,.15]}}));
            // katman çizgileri (uyumsuzluk gösterimi)
            for(var i=0;i<4;i++){{var y=-.3+i*.2;mainObj.add(_m(new THREE.BoxGeometry(.95,.01,.01),0xccaa77,{{p:[-.55,y+.15,.61]}}));mainObj.add(_m(new THREE.BoxGeometry(.95,.01,.01),0xccaa77,{{p:[.55,y-.15,.61]}}));}}
            // hareket okları
            mainObj.add(_m(new THREE.ConeGeometry(.04,.12,6),0xff4444,{{p:[-.55,.7,0]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.04,.12,6),0xff4444,{{p:[.55,-.7,0],r:[Math.PI,0,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.2,6),0xff4444,{{p:[-.55,.55,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.2,6),0xff4444,{{p:[.55,-.55,0]}}));
            // deprem dalgaları
            for(var i=1;i<=3;i++)mainObj.add(_m(new THREE.TorusGeometry(i*.2,.008,8,24),0xff6644,{{p:[0,0,.3],r:[Math.PI/2,0,0],op:.4/i}}));
        }}

        // T=15 Tektonik Plaka — iki plaka hareketi
        if(T==15){{
            // sol plaka (okyanus kabuğu, ince)
            mainObj.add(_m(new THREE.BoxGeometry(1.2,.15,1.5),0x556677,{{p:[-.6,.2,0]}}));
            // sağ plaka (kıtasal kabuk, kalın)
            mainObj.add(_m(new THREE.BoxGeometry(1.2,.3,1.5),0xbbaa77,{{p:[.6,.25,0]}}));
            // manto (altta)
            mainObj.add(_m(new THREE.BoxGeometry(2.8,.6,1.5),0xcc5533,{{p:[0,-.35,0],em:0xcc3311,ei:.2}}));
            // dalma batma zonu (subdüçtion)
            for(var i=0;i<8;i++)mainObj.add(_m(new THREE.BoxGeometry(.12,.04,.8),0x556677,{{p:[-.1-i*.1,.1-i*.08,0],r:[0,0,-.3]}}));
            // volkan (üstte)
            mainObj.add(_m(new THREE.ConeGeometry(.15,.35,10),0x887766,{{p:[.3,.55,0]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0xff4400,{{p:[.3,.75,0],op:.7}}));
            // hareket okları
            mainObj.add(_m(new THREE.ConeGeometry(.03,.1,6),0x44aaff,{{p:[-1.1,.2,0],r:[0,0,Math.PI/2]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.03,.1,6),0x44aaff,{{p:[1.1,.25,0],r:[0,0,-Math.PI/2]}}));
            // manto konveksiyon akımları
            for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.TorusGeometry(.25,.01,8,16,Math.PI),0xff8855,{{p:[-.5+i*.5,-.35,0],r:[0,Math.PI/2,0],op:.4}}));}}
        }}

        // T=16 Mineral Yapısı — kristal kafes sistemi
        if(T==16){{
            // atomlar (3x3x3 kafes)
            for(var x=-1;x<=1;x++)for(var y=-1;y<=1;y++)for(var z=-1;z<=1;z++){{
                var clr=(x+y+z)%2==0?0x44aaff:0xff6644;
                mainObj.add(_m(new THREE.SphereGeometry(.08,10,10),clr,{{p:[x*.4,y*.4,z*.4],sh:100}}));
            }}
            // bağ çizgileri (x ekseninde)
            for(var x=-1;x<1;x++)for(var y=-1;y<=1;y++)for(var z=-1;z<=1;z++){{
                mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.4,6),0xaaaaaa,{{p:[(x+.5)*.4,y*.4,z*.4],r:[0,0,Math.PI/2],op:.4}}));
            }}
            // bağ çizgileri (y ekseninde)
            for(var x=-1;x<=1;x++)for(var y=-1;y<1;y++)for(var z=-1;z<=1;z++){{
                mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.4,6),0xaaaaaa,{{p:[x*.4,(y+.5)*.4,z*.4],op:.4}}));
            }}
            // birim hücre vurgusu
            mainObj.add(_mb(new THREE.BoxGeometry(.4,.4,.4),0xffff44,{{op:.08}}));
        }}

        // T=17 Kristal Oluşumu — büyüme aşamaları
        if(T==17){{
            // çekirdek (küçük kristal tohum)
            mainObj.add(_m(new THREE.OctahedronGeometry(.08),0xddddff,{{p:[-1,0,0],sh:120}}));
            // büyüme 1
            mainObj.add(_m(new THREE.OctahedronGeometry(.18),0xccccff,{{p:[-.5,0,0],sh:120,op:.8}}));
            // büyüme 2
            mainObj.add(_m(new THREE.OctahedronGeometry(.32),0xbbbbff,{{p:[.1,0,0],sh:120,op:.7}}));
            // tam kristal
            mainObj.add(_m(new THREE.OctahedronGeometry(.5),0xaaaaff,{{p:[.8,0,0],sh:130,op:.6}}));
            // ok (büyüme yönü)
            for(var i=0;i<3;i++)mainObj.add(_m(new THREE.ConeGeometry(.03,.08,6),0xffaa44,{{p:[-.75+i*.55,-.5,0],r:[0,0,-Math.PI/2]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,1.8,6),0xffaa44,{{p:[-.1,-.5,0],r:[0,0,Math.PI/2]}}));
            // çözelti parçacıkları
            for(var i=0;i<15;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.015,4,4),0x88aaff,{{p:[(Math.random()-.5)*2.5,(Math.random()-.5)*1,(Math.random()-.5)*.8],op:.3}}));}}
            // etiketler — "Çekirdek → Büyüme → Kristal" ok çizgisi zaten üstte
        }}

        // T=18 Volkanik Kaya — gözenekli yapı
        if(T==18){{
            var body=_m(new THREE.DodecahedronGeometry(.85),0x555544,{{fs:true}});mainObj.add(body);
            // gözenekler (vesiçular texture)
            for(var i=0;i<25;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.5+Math.random()*.35;mainObj.add(_mb(new THREE.SphereGeometry(.03+Math.random()*.04,8,8),0x333322,{{p:[Math.sin(b)*Math.cos(a)*r,Math.cos(b)*r,Math.sin(b)*Math.sin(a)*r],op:.6}}));}}
            // mineral kristaller (küçük parlak noktalar)
            for(var i=0;i<8;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.7;mainObj.add(_m(new THREE.OctahedronGeometry(.02),0xdddddd,{{p:[Math.sin(b)*Math.cos(a)*r,Math.cos(b)*r,Math.sin(b)*Math.sin(a)*r],sh:120}}));}}
            // kızıl iç glow (ısı kalıntısı)
            mainObj.add(_mb(new THREE.DodecahedronGeometry(.4),0xff4400,{{op:.08}}));
        }}

        // T=19 Metamorfik Kaya — bantlı/yapraklanma yapısı
        if(T==19){{
            // ana gövde
            mainObj.add(_m(new THREE.SphereGeometry(.85,20,20),0x667766,{{s:[1.2,.9,1],fs:true}}));
            // foliasyon bantları (yapraklanma katmanları)
            for(var i=0;i<10;i++){{var y=-.6+i*.13;mainObj.add(_m(new THREE.BoxGeometry(1.6,.02,1.4),i%2==0?0x556655:0x889988,{{p:[0,y,0],op:.5}}));}}
            // garnet kristalleri (kırmızı noktalar)
            for(var i=0;i<6;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.7;mainObj.add(_m(new THREE.DodecahedronGeometry(.04),0xcc3344,{{p:[Math.sin(b)*Math.cos(a)*r,Math.cos(b)*r,Math.sin(b)*Math.sin(a)*r],sh:100}}));}}
            // mika pulları (parlak gümüş)
            for(var i=0;i<8;i++){{var a=Math.random()*6.28,b=Math.random()*3.14,r=.75;mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.005,6),0xcccccc,{{p:[Math.sin(b)*Math.cos(a)*r,Math.cos(b)*r,Math.sin(b)*Math.sin(a)*r],sh:150}}));}}
        }}

        scene.add(mainObj);"""

    if ci == 17:  # Optik ve Işık — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||60,transparent:!!o.op,opacity:o.op||1,flatShading:!!o.fs,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _ray(x1,y1,x2,y2,clr){{var dx=x2-x1,dy=y2-y1,ln=Math.sqrt(dx*dx+dy*dy);var r=_mb(new THREE.CylinderGeometry(.008,.008,ln,6),clr,{{p:[(x1+x2)/2,(y1+y2)/2,0],r:[0,0,Math.atan2(dx,dy)]}});return r;}}

        // T=0 İçbükey Ayna — concave mirror
        if(T==0){{
            // ayna yüzeyi (içbükey)
            mainObj.add(_m(new THREE.SphereGeometry(1.2,32,32),0xcccccc,{{p:[1,0,0],sh:200,s:[1,1,.1]}}));
            // ayna arkası (köyü)
            mainObj.add(_m(new THREE.SphereGeometry(1.22,32,32),0x444444,{{p:[1.02,0,0],s:[1,1,.1]}}));
            // optik eksen
            mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,3,4),0xaaaaaa,{{r:[0,0,Math.PI/2],op:.4}}));
            // odak noktası F
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0xff4444,{{p:[-.2,0,0]}}));
            // merkez C
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x4444ff,{{p:[.6,0,0]}}));
            // gelen paralel ışınlar
            for(var i=0;i<5;i++){{var y=(i-2)*.18;mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,1.3,6),0xffff44,{{p:[-1,y,0],r:[0,0,Math.PI/2],op:.7}}));}}
            // yansıyan ışınlar (odağa)
            for(var i=0;i<5;i++){{var y=(i-2)*.18;var dx=-.2-(-.2);var dy=0-y;var ln=Math.sqrt((.2)*(0.2)+y*y+.16);mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,.6,6),0xffaa22,{{p:[-.3+(.1),y/2,0],r:[0,0,Math.atan2(.2,y)+Math.PI/2],op:.6}}));}}
            // nesne oku (sol)
            mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.4,6),0x44ff44,{{p:[-1.2,.2,0]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.03,.08,6),0x44ff44,{{p:[-1.2,.42,0]}}));
        }}

        // T=1 Dışbükey Ayna — convex mirror
        if(T==1){{
            // ayna yüzeyi (dışbükey)
            mainObj.add(_m(new THREE.SphereGeometry(1.2,32,32),0xcccccc,{{p:[-1,0,0],sh:200,s:[1,1,.1]}}));
            mainObj.add(_m(new THREE.SphereGeometry(1.22,32,32),0x444444,{{p:[-1.02,0,0],s:[1,1,.1]}}));
            // optik eksen
            mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,3,4),0xaaaaaa,{{r:[0,0,Math.PI/2],op:.4}}));
            // sanal odak noktası F (ayna arkasında)
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0xff4444,{{p:[-.5,0,0],op:.5}}));
            // gelen ışınlar
            for(var i=0;i<5;i++){{var y=(i-2)*.18;mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,1.2,6),0xffff44,{{p:[.8,y,0],r:[0,0,Math.PI/2],op:.7}}));}}
            // yansıyan ışınlar (dağılan)
            for(var i=0;i<5;i++){{var y=(i-2)*.18;var ang=y*.6;mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,.8,6),0xffaa22,{{p:[.6,y+ang*.3,0],r:[0,0,Math.PI/2+ang*.5],op:.6}}));}}
            // sanal görüntü (küçük, dik)
            mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.2,6),0x44ff44,{{p:[-.6,.1,0],op:.4}}));
            mainObj.add(_m(new THREE.ConeGeometry(.02,.06,6),0x44ff44,{{p:[-.6,.22,0],op:.4}}));
        }}

        // T=2 İnce Mercek — biconvex lens
        if(T==2){{
            // lens gövdesi
            var lens=_m(new THREE.SphereGeometry(.7,32,32),0xaaddff,{{sh:120,op:.3,s:[1,1,.15]}});mainObj.add(lens);
            // lens kenar halkası
            mainObj.add(_m(new THREE.TorusGeometry(.7,.02,8,32),0x666666,{{r:[0,0,0]}}));
            // optik eksen
            mainObj.add(_mb(new THREE.CylinderGeometry(.004,.004,3.5,4),0xaaaaaa,{{r:[0,0,Math.PI/2],op:.3}}));
            // odak noktaları
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xff4444,{{p:[.8,0,0]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xff4444,{{p:[-.8,0,0]}}));
            // gelen paralel ışınlar → odakta birleşir
            for(var i=0;i<5;i++){{var y=(i-2)*.15;mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,1.2,6),0xffff44,{{p:[-1.2,y,0],r:[0,0,Math.PI/2],op:.6}}));}}
            // kırılan ışınlar
            for(var i=0;i<5;i++){{var y=(i-2)*.15;var ang=Math.atan2(-y,.8);mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,Math.sqrt(y*y+.64),6),0xff8822,{{p:[.4,y/2,0],r:[0,0,Math.PI/2+ang*.5],op:.5}}));}}
            // nesne ve görüntü okları
            mainObj.add(_m(new THREE.CylinderGeometry(.012,.012,.35,6),0x44ff44,{{p:[-1.5,.18,0]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.025,.07,6),0x44ff44,{{p:[-1.5,.37,0]}}));
        }}

        // T=3 Kalın Mercek — thick lens
        if(T==3){{
            var lens=_m(new THREE.SphereGeometry(.65,32,32),0xaaddff,{{sh:120,op:.35,s:[1,1,.45]}});mainObj.add(lens);
            mainObj.add(_m(new THREE.TorusGeometry(.63,.025,8,32),0x666666));
            mainObj.add(_mb(new THREE.CylinderGeometry(.004,.004,3.5,4),0xaaaaaa,{{r:[0,0,Math.PI/2],op:.3}}));
            // ana düzlemler H, H'
            mainObj.add(_mb(new THREE.PlaneGeometry(.02,1.2),0x44aaff,{{p:[-.1,0,.01],op:.4,ds:true}}));
            mainObj.add(_mb(new THREE.PlaneGeometry(.02,1.2),0x44aaff,{{p:[.1,0,.01],op:.4,ds:true}}));
            // odak noktaları
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xff4444,{{p:[.7,0,0]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xff4444,{{p:[-.7,0,0]}}));
            // ışınlar
            for(var i=0;i<4;i++){{var y=(i-1.5)*.2;mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,1,6),0xffff44,{{p:[-1.2,y,0],r:[0,0,Math.PI/2],op:.6}}));mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,.7,6),0xff8822,{{p:[.6,y*.3,0],r:[0,0,Math.PI/2-y*.3],op:.5}}));}}
        }}

        // T=4 Prizma — ışık kırılması
        if(T==4){{
            // cam prizma (üçgen)
            mainObj.add(_m(new THREE.CylinderGeometry(.6,.6,.6,3),0xddddff,{{sh:120,op:.35,r:[Math.PI/6,0,0]}}));
            // wireframe
            mainObj.add(new THREE.Mesh(new THREE.CylinderGeometry(.61,.61,.61,3),new THREE.MeshBasicMaterial({{color:0x8888cc,wireframe:true,transparent:true,opacity:.3}})));mainObj.children[1].rotation.x=Math.PI/6;
            // beyaz giriş ışını
            mainObj.add(_mb(new THREE.CylinderGeometry(.012,.012,1.2,6),0xffffff,{{p:[-1,0,0],r:[0,0,Math.PI/2]}}));
            // spektrum çıkış ışınları (VIBGYOR)
            var specC=[0xff0000,0xff6600,0xffff00,0x00ff00,0x00aaff,0x4400ff,0x8800ff];
            for(var s=0;s<7;s++){{var ang=-.2+s*.06;mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,1.1,6),specC[s],{{p:[.85,(s-3)*.06,0],r:[0,0,Math.PI/2+ang],op:.8}}));}}
            // giriş normal çizgisi
            mainObj.add(_mb(new THREE.CylinderGeometry(.003,.003,.5,4),0xaaaaaa,{{p:[-.35,.3,0],op:.3}}));
        }}

        // T=5 Gökkuşağı — 7 renk yayı
        if(T==5){{
            var specC=[0xff0000,0xff6600,0xffff00,0x00ff00,0x00aaff,0x4400ff,0x8800ff];
            for(var i=0;i<7;i++){{mainObj.add(_m(new THREE.TorusGeometry(.75+i*.06,.025,12,50,Math.PI),specC[i],{{p:[0,-.2,0],em:specC[i],ei:.2}}));}}
            // zemin (yeşil)
            mainObj.add(_m(new THREE.BoxGeometry(3,.1,1.5),0x44aa44,{{p:[0,-.85,0]}}));
            // güneş (sağ üst)
            mainObj.add(_mb(new THREE.SphereGeometry(.15,16,16),0xffff44,{{p:[1.2,.8,-.3]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.25,16,16),0xffff00,{{p:[1.2,.8,-.3],op:.15}}));
            // yağmur damlaları
            for(var i=0;i<15;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.015,6,6),0x88bbff,{{p:[(Math.random()-.5)*2,Math.random()*1.2-.3,(Math.random()-.5)*.5],op:.4}}));}}
            // bulut
            mainObj.add(_m(new THREE.SphereGeometry(.2,10,10),0xdddddd,{{p:[-.6,.9,0]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.15,10,10),0xcccccc,{{p:[-.4,.85,0]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.17,10,10),0xdddddd,{{p:[-.8,.85,0]}}));
        }}

        // T=6 Lazer — lazer cihazı ve ışın
        if(T==6){{
            // lazer gövdesi
            mainObj.add(_m(new THREE.CylinderGeometry(.12,.12,.8,12),0x444444,{{p:[-1,0,0],r:[0,0,Math.PI/2],sh:80}}));
            // ön açıklık
            mainObj.add(_m(new THREE.CylinderGeometry(.08,.1,.05,12),0x333333,{{p:[-.58,0,0],r:[0,0,Math.PI/2]}}));
            // lazer ışını (kırmızı, parlak)
            mainObj.add(_mb(new THREE.CylinderGeometry(.012,.012,2.2,8),0xff0000,{{p:[.55,0,0],r:[0,0,Math.PI/2]}}));
            // ışın glow
            mainObj.add(_mb(new THREE.CylinderGeometry(.04,.04,2.2,8),0xff2222,{{p:[.55,0,0],r:[0,0,Math.PI/2],op:.12}}));
            // hedef nokta (duvarda)
            mainObj.add(_mb(new THREE.SphereGeometry(.06,12,12),0xff0000,{{p:[1.65,0,0],op:.6}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.12,12,12),0xff0000,{{p:[1.65,0,0],op:.15}}));
            // güç kaynağı kablosu
            mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,.3,6),0x222222,{{p:[-1,-.2,0]}}));
            // kontrol düğmesi
            mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.04,8),0x44ff44,{{p:[-1.1,.13,0],r:[Math.PI/2,0,0]}}));
        }}

        // T=7 Fiber Optik — ışık taşıyan cam lif
        if(T==7){{
            // fiber kablo (eğri yol - birçok segment)
            var pts=[];for(var i=0;i<=30;i++){{var t=i/30;var x=-1.5+t*3;var y=Math.sin(t*Math.PI*2)*.4;pts.push([x,y,0]);}}
            for(var i=0;i<30;i++){{var dx=pts[i+1][0]-pts[i][0],dy=pts[i+1][1]-pts[i][1];var ln=Math.sqrt(dx*dx+dy*dy);mainObj.add(_m(new THREE.CylinderGeometry(.06,.06,ln,10),0x4488cc,{{p:[(pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2,0],r:[0,0,Math.atan2(dx,dy)],op:.5,sh:100}}));}}
            // iç çekirdek (core - daha parlak)
            for(var i=0;i<30;i++){{var dx=pts[i+1][0]-pts[i][0],dy=pts[i+1][1]-pts[i][1];var ln=Math.sqrt(dx*dx+dy*dy);mainObj.add(_mb(new THREE.CylinderGeometry(.02,.02,ln,8),0xaaddff,{{p:[(pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2,0],r:[0,0,Math.atan2(dx,dy)],op:.6}}));}}
            // giriş ışığı
            mainObj.add(_mb(new THREE.SphereGeometry(.08,10,10),0xffff44,{{p:[-1.5,0,0]}}));
            // çıkış ışığı
            mainObj.add(_mb(new THREE.SphereGeometry(.08,10,10),0xffff44,{{p:[1.5,Math.sin(2*Math.PI)*.4,0],op:.8}}));
            // konnektör uçları
            mainObj.add(_m(new THREE.CylinderGeometry(.08,.08,.1,10),0x666666,{{p:[-1.5,0,0],r:[0,0,Math.PI/2]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.08,.08,.1,10),0x666666,{{p:[1.5,0,0],r:[0,0,Math.PI/2]}}));
        }}

        // T=8 Mikroskop
        if(T==8){{
            // taban
            mainObj.add(_m(new THREE.BoxGeometry(.8,.08,.5),0x333333,{{p:[0,-.9,0]}}));
            // kolon
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.06,1.6,10),0x444444,{{p:[-.2,0,0]}}));
            // kol
            mainObj.add(_m(new THREE.BoxGeometry(.08,.5,.08),0x444444,{{p:[-.2,.5,0],r:[0,0,.3]}}));
            // tüp (body tube)
            mainObj.add(_m(new THREE.CylinderGeometry(.07,.07,.6,10),0x555555,{{p:[0,.4,0]}}));
            // oküler lens
            mainObj.add(_m(new THREE.CylinderGeometry(.08,.06,.1,12),0x333333,{{p:[0,.72,0]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.06,16,16),0xaaddff,{{p:[0,.78,0],sh:120,op:.4}}));
            // objektif revolver
            mainObj.add(_m(new THREE.CylinderGeometry(.1,.1,.04,10),0x555555,{{p:[0,.08,0]}}));
            // 3 objektif lens
            for(var i=0;i<3;i++){{var a=i*1.2-.6;mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.15+i*.05,8),0x666666,{{p:[Math.sin(a)*.07,-.02-(.1+i*.025),Math.cos(a)*.07]}}));}}
            // sahne (specimen stage)
            mainObj.add(_m(new THREE.BoxGeometry(.5,.03,.4),0x444444,{{p:[0,-.15,0]}}));
            // lam (preparat)
            mainObj.add(_m(new THREE.BoxGeometry(.2,.01,.06),0xeeeeff,{{p:[0,-.13,0],sh:100,op:.6}}));
            // ışık kaynağı
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.06,.06,10),0xffff88,{{p:[0,-.55,0],em:0xffff44,ei:.4}}));
            // ayar düğmeleri
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.04,.06,10),0x555555,{{p:[.2,0,.1],r:[Math.PI/2,0,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.06,10),0x555555,{{p:[.2,-.15,.1],r:[Math.PI/2,0,0]}}));
        }}

        // T=9 Teleskop — refraktor
        if(T==9){{
            // ana tüp
            mainObj.add(_m(new THREE.CylinderGeometry(.12,.1,1.8,14),0xdddddd,{{r:[0,0,.3],sh:80}}));
            // ön lens (objektif)
            mainObj.add(_m(new THREE.SphereGeometry(.12,16,16),0xaaddff,{{p:[.82,.48,0],sh:120,op:.4,s:[1,1,.2]}}));
            // arka lens (oküler)
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.05,.08,10),0x333333,{{p:[-.78,-.45,0],r:[0,0,.3]}}));
            // tüp bağlantı halkası
            mainObj.add(_m(new THREE.TorusGeometry(.12,.015,8,20),0xaaaaaa,{{p:[0,0,0],r:[.3,Math.PI/2,0]}}));
            // çatal ayak (fork mount)
            mainObj.add(_m(new THREE.BoxGeometry(.06,.3,.06),0x555555,{{p:[.1,-.3,-.1]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.06,.3,.06),0x555555,{{p:[.1,-.3,.1]}}));
            // tripod bacakları
            for(var i=0;i<3;i++){{var a=i*2.094;mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,.7,6),0x444444,{{p:[.1+Math.cos(a)*.15,-.75,Math.sin(a)*.15],r:[Math.cos(a)*.2,0,Math.sin(a)*.2]}}));}}
            // arayıcı dürbün (finder scope)
            mainObj.add(_m(new THREE.CylinderGeometry(.025,.02,.4,8),0x888888,{{p:[.3,.22,.12],r:[0,0,.3]}}));
        }}

        // T=10 Dürbün — binoculars
        if(T==10){{
            // sol tüp
            mainObj.add(_m(new THREE.CylinderGeometry(.12,.1,.8,14),0x333333,{{p:[-.15,0,0],r:[0,0,Math.PI/2],sh:80}}));
            // sağ tüp
            mainObj.add(_m(new THREE.CylinderGeometry(.12,.1,.8,14),0x333333,{{p:[.15,0,0],r:[0,0,Math.PI/2],sh:80}}));
            // köprü (bağlantı)
            mainObj.add(_m(new THREE.BoxGeometry(.3,.1,.12),0x444444,{{p:[0,0,0]}}));
            // ön lensler
            mainObj.add(_m(new THREE.SphereGeometry(.1,16,16),0xaaddff,{{p:[-.15,0,.42],sh:120,op:.4,s:[1,1,.2]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.1,16,16),0xaaddff,{{p:[.15,0,.42],sh:120,op:.4,s:[1,1,.2]}}));
            // oküler lensler
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.05,.06,10),0x222222,{{p:[-.15,0,-.43],r:[Math.PI/2,0,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.05,.06,10),0x222222,{{p:[.15,0,-.43],r:[Math.PI/2,0,0]}}));
            // odak tekerleği
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.04,.08,12),0x555555,{{p:[0,.08,0]}}));
            // kayış halkaları
            mainObj.add(_m(new THREE.TorusGeometry(.015,.005,6,10),0x555555,{{p:[-.25,0,0]}}));
            mainObj.add(_m(new THREE.TorusGeometry(.015,.005,6,10),0x555555,{{p:[.25,0,0]}}));
        }}

        // T=11 Kamera Lensi — DSLR lens
        if(T==11){{
            // lens gövdesi (silindir)
            mainObj.add(_m(new THREE.CylinderGeometry(.35,.3,.9,20),0x222222,{{r:[Math.PI/2,0,0],sh:80}}));
            // ön lens grubu
            mainObj.add(_m(new THREE.SphereGeometry(.33,24,24),0xaaddff,{{p:[0,0,.5],sh:140,op:.3,s:[1,1,.15]}}));
            // ön halka
            mainObj.add(_m(new THREE.TorusGeometry(.35,.015,8,24),0x111111,{{p:[0,0,.46]}}));
            // odak halkası
            mainObj.add(_m(new THREE.TorusGeometry(.36,.02,8,24),0x555555,{{p:[0,0,.15]}}));
            // zoom halkası
            mainObj.add(_m(new THREE.TorusGeometry(.37,.025,8,24),0x444444,{{p:[0,0,-.1]}}));
            // mount (arka bağlantı)
            mainObj.add(_m(new THREE.CylinderGeometry(.28,.3,.05,20),0x666666,{{p:[0,0,-.48],r:[Math.PI/2,0,0]}}));
            // lens reflections (iç lens)
            mainObj.add(_mb(new THREE.SphereGeometry(.2,16,16),0x88aadd,{{p:[0,0,.2],op:.08,s:[1,1,.1]}}));
            // marka çizgisi
            mainObj.add(_m(new THREE.BoxGeometry(.2,.005,.005),0xcc4444,{{p:[0,.35,.3]}}));
        }}

        // T=12 Kırılma — ışığın ortam değiştirmesi
        if(T==12){{
            // hava ortamı (üst, boş)
            mainObj.add(_m(new THREE.BoxGeometry(2,.8,1),0xeeeeff,{{p:[0,.4,0],op:.05}}));
            // cam/su ortamı (alt)
            mainObj.add(_m(new THREE.BoxGeometry(2,.8,1),0x88bbff,{{p:[0,-.4,0],op:.15}}));
            // yüzey çizgisi
            mainObj.add(_mb(new THREE.BoxGeometry(2,.005,.5),0xaaaaaa,{{p:[0,0,0]}}));
            // normal çizgi (dikey kesikli)
            for(var i=0;i<8;i++)mainObj.add(_mb(new THREE.BoxGeometry(.005,.08,.005),0xaaaaaa,{{p:[0,-.3+i*.1,0],op:.4}}));
            // gelen ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,.9,6),0xffff44,{{p:[-.25,.4,0],r:[0,0,.4]}}));
            // kırılan ışın (daha dik)
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,.9,6),0xff8822,{{p:[.15,-.4,0],r:[0,0,.2]}}));
            // giriş açısı yayı
            mainObj.add(_m(new THREE.TorusGeometry(.2,.005,8,16,0.4),0xffff44,{{p:[0,.02,0],r:[Math.PI/2,.3,0],op:.6}}));
            // kırılma açısı yayı
            mainObj.add(_m(new THREE.TorusGeometry(.2,.005,8,16,0.2),0xff8822,{{p:[0,-.02,0],r:[-Math.PI/2,.1,0],op:.6}}));
        }}

        // T=13 Yansıma — düz aynada yansıma
        if(T==13){{
            // düz ayna
            mainObj.add(_m(new THREE.BoxGeometry(.06,1.2,.8),0xcccccc,{{p:[.6,0,0],sh:200}}));
            mainObj.add(_m(new THREE.BoxGeometry(.04,1.25,.85),0x444444,{{p:[.63,0,0]}}));
            // normal çizgi
            mainObj.add(_mb(new THREE.CylinderGeometry(.004,.004,.8,4),0xaaaaaa,{{p:[.2,.3,0],r:[0,0,Math.PI/2],op:.4}}));
            // gelen ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,1,6),0xffff44,{{p:[-.15,.3,0],r:[0,0,Math.PI/2+.5]}}));
            // yansıyan ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,1,6),0xff8822,{{p:[-.15,.3,0],r:[0,0,Math.PI/2-.5]}}));
            // geliş açısı
            mainObj.add(_m(new THREE.TorusGeometry(.2,.005,8,16,0.5),0xffff44,{{p:[.57,.3,0],r:[0,Math.PI/2,Math.PI/2-.25],op:.6}}));
            // yansıma açısı
            mainObj.add(_m(new THREE.TorusGeometry(.2,.005,8,16,0.5),0xff8822,{{p:[.57,.3,0],r:[0,Math.PI/2,Math.PI/2+.25],op:.6}}));
            // nesne (mum)
            mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.3,8),0xeedd88,{{p:[-.8,-.15,0]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0xffaa22,{{p:[-.8,.02,0]}}));
        }}

        // T=14 Kırılma Açısı — Snell yasası
        if(T==14){{
            // iki ortam
            mainObj.add(_m(new THREE.BoxGeometry(2.2,.9,1.2),0xeeeeff,{{p:[0,.45,0],op:.05}}));
            mainObj.add(_m(new THREE.BoxGeometry(2.2,.9,1.2),0x88bbff,{{p:[0,-.45,0],op:.2}}));
            // sınır yüzeyi
            mainObj.add(_mb(new THREE.BoxGeometry(2.2,.008,1.2),0xffffff,{{p:[0,0,0],op:.5}}));
            // normal
            mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,1.6,4),0xaaaaaa,{{p:[0,0,0],op:.4}}));
            // gelen ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.01,.01,.9,6),0xffff44,{{p:[-.22,.42,0],r:[0,0,.45]}}));
            // kırılan ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.01,.01,.9,6),0xff6622,{{p:[.12,-.42,0],r:[0,0,.22]}}));
            // açı yayları (θ1, θ2)
            mainObj.add(_m(new THREE.TorusGeometry(.25,.006,8,20,.45),0xffff44,{{p:[0,.01,0],r:[Math.PI/2,.22,0],op:.7}}));
            mainObj.add(_m(new THREE.TorusGeometry(.25,.006,8,20,.22),0xff6622,{{p:[0,-.01,0],r:[-Math.PI/2,.11,0],op:.7}}));
            // n1, n2 etiket kutuları
            mainObj.add(_m(new THREE.BoxGeometry(.15,.08,.01),0xffffff,{{p:[.8,.4,.61],op:.5}}));
            mainObj.add(_m(new THREE.BoxGeometry(.15,.08,.01),0x88bbff,{{p:[.8,-.4,.61],op:.5}}));
        }}

        // T=15 Polarizasyon — ışık polarizasyonu
        if(T==15){{
            // polarize olmamış ışık kaynağı
            mainObj.add(_mb(new THREE.SphereGeometry(.1,10,10),0xffff44,{{p:[-1.5,0,0]}}));
            // çok yönlü titreşim çizgileri (gelen)
            for(var i=0;i<8;i++){{var a=i*.393;mainObj.add(_mb(new THREE.CylinderGeometry(.003,.003,.2,4),0xffff44,{{p:[-1.2,0,0],r:[a,0,0],op:.5}}));}}
            // gelen ışın
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,.8,6),0xffff44,{{p:[-1.1,0,0],r:[0,0,Math.PI/2],op:.7}}));
            // 1. polarizör filtre
            mainObj.add(_m(new THREE.CylinderGeometry(.4,.4,.03,20),0x888888,{{p:[-.5,0,0],r:[0,0,Math.PI/2],op:.4}}));
            mainObj.add(_m(new THREE.BoxGeometry(.005,.7,.01),0x44ff44,{{p:[-.5,0,0]}}));
            // polarize ışın (tek yön titreşim)
            mainObj.add(_mb(new THREE.CylinderGeometry(.008,.008,.6,6),0x44ff44,{{p:[-.1,0,0],r:[0,0,Math.PI/2]}}));
            for(var i=0;i<6;i++)mainObj.add(_mb(new THREE.CylinderGeometry(.003,.003,.12,4),0x44ff44,{{p:[-.3+i*.1,0,0],op:.5}}));
            // 2. polarizör (analizör)
            mainObj.add(_m(new THREE.CylinderGeometry(.4,.4,.03,20),0x888888,{{p:[.5,0,0],r:[0,0,Math.PI/2],op:.4}}));
            mainObj.add(_m(new THREE.BoxGeometry(.005,.7,.01),0xff4444,{{p:[.5,0,0],r:[0,0,.8]}}));
            // çıkış ışını (azalmış)
            mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,.5,6),0x44ff44,{{p:[1,0,0],r:[0,0,Math.PI/2],op:.3}}));
        }}

        // T=16 Spektrum — ışık spektrumu
        if(T==16){{
            // spektrum çubuğu (yatay renk bandı)
            var specC=[0x8800ff,0x4400ff,0x0044ff,0x00aaff,0x00ff88,0x44ff00,0xffff00,0xff8800,0xff4400,0xff0000];
            for(var i=0;i<10;i++){{mainObj.add(_mb(new THREE.BoxGeometry(.22,.4,.1),specC[i],{{p:[-1.1+i*.24,0,0]}}));}}
            // dalga boyu ölçeği (alt)
            mainObj.add(_mb(new THREE.BoxGeometry(2.4,.005,.01),0xffffff,{{p:[0,-.25,0.06]}}));
            for(var i=0;i<11;i++)mainObj.add(_mb(new THREE.BoxGeometry(.005,.04,.01),0xffffff,{{p:[-1.1+i*.22,-.27,.06]}}));
            // beyaz ışık girişi (sol)
            mainObj.add(_mb(new THREE.CylinderGeometry(.01,.01,.4,6),0xffffff,{{p:[-1.5,0,0],r:[0,0,Math.PI/2]}}));
            // prizma (ortada küçük)
            mainObj.add(_m(new THREE.CylinderGeometry(.15,.15,.15,3),0xddddff,{{p:[-1.3,0,0],r:[Math.PI/6,0,0],op:.3,sh:120}}));
        }}

        // T=17 Foton — ışık parçacığı/dalga ikiliği
        if(T==17){{
            // dalga özelliği (sinüs dalgası)
            for(var i=0;i<40;i++){{var t=i/40;var x=-1.5+t*3;var y=Math.sin(t*Math.PI*6)*.3;mainObj.add(_mb(new THREE.SphereGeometry(.02,6,6),0xffff44,{{p:[x,y,0],op:.7}}));}}
            // dalga bağlantı çizgileri
            for(var i=0;i<39;i++){{var t1=i/40,t2=(i+1)/40;var x1=-1.5+t1*3,y1=Math.sin(t1*Math.PI*6)*.3;var x2=-1.5+t2*3,y2=Math.sin(t2*Math.PI*6)*.3;var dx=x2-x1,dy=y2-y1,ln=Math.sqrt(dx*dx+dy*dy);mainObj.add(_mb(new THREE.CylinderGeometry(.005,.005,ln,4),0xffff44,{{p:[(x1+x2)/2,(y1+y2)/2,0],r:[0,0,Math.atan2(dx,dy)],op:.4}}));}}
            // foton parçacık (parlak küre)
            mainObj.add(_mb(new THREE.SphereGeometry(.08,12,12),0xffff00,{{p:[.5,Math.sin((.5+1.5)/3*Math.PI*6)*.3,0]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.15,12,12),0xffff00,{{p:[.5,Math.sin((.5+1.5)/3*Math.PI*6)*.3,0],op:.15}}));
            // E ve B alan okları
            mainObj.add(_m(new THREE.ConeGeometry(.025,.08,6),0xff4444,{{p:[0,.45,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.15,6),0xff4444,{{p:[0,.35,0]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.025,.08,6),0x4444ff,{{p:[0,0,.45],r:[Math.PI/2,0,0]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.15,6),0x4444ff,{{p:[0,0,.35],r:[Math.PI/2,0,0]}}));
        }}

        // T=18 Dalga Girişimi — iki dalga süperpozisyonu
        if(T==18){{
            // kaynak 1
            mainObj.add(_mb(new THREE.SphereGeometry(.05,8,8),0xff4444,{{p:[-.8,.5,0]}}));
            // kaynak 2
            mainObj.add(_mb(new THREE.SphereGeometry(.05,8,8),0x4444ff,{{p:[-.8,-.5,0]}}));
            // dalga 1 halkaları
            for(var i=1;i<=5;i++)mainObj.add(_m(new THREE.TorusGeometry(i*.2,.008,8,30),0xff4444,{{p:[-.8,.5,0],r:[Math.PI/2,0,0],op:.5/i}}));
            // dalga 2 halkaları
            for(var i=1;i<=5;i++)mainObj.add(_m(new THREE.TorusGeometry(i*.2,.008,8,30),0x4444ff,{{p:[-.8,-.5,0],r:[Math.PI/2,0,0],op:.5/i}}));
            // girişim bölgesi (yapıcı noktalar)
            for(var i=0;i<5;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x44ff44,{{p:[.2+i*.25,0,0],op:.6}}));}}
            // yıkıcı girişim noktaları
            for(var i=0;i<4;i++){{mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0xff8844,{{p:[.3+i*.25,.3,0],op:.4}}));mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0xff8844,{{p:[.3+i*.25,-.3,0],op:.4}}));}}
            // ekran (sağda)
            mainObj.add(_m(new THREE.BoxGeometry(.03,1.4,.8),0xdddddd,{{p:[1.3,0,0],op:.3}}));
            // girişim deseni (ekranda)
            for(var i=0;i<8;i++)mainObj.add(_mb(new THREE.BoxGeometry(.02,.12,.5),i%2==0?0xffffff:0x222222,{{p:[1.32,(i-3.5)*.15,0],op:.5}}));
        }}

        // T=19 Hologram — holografik görüntü
        if(T==19){{
            // lazer kaynağı
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.06,.3,10),0x444444,{{p:[-1.2,.5,0],r:[0,0,Math.PI/2]}}));
            // lazer ışını (referans)
            mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,.8,6),0x44ff44,{{p:[-.7,.5,0],r:[0,0,Math.PI/2],op:.6}}));
            // yarı ayna (beam splitter)
            mainObj.add(_m(new THREE.BoxGeometry(.02,.3,.3),0xaaddff,{{p:[-.3,.5,0],r:[0,0,.78],sh:120,op:.3}}));
            // ikinci ışın (nesne ışını)
            mainObj.add(_mb(new THREE.CylinderGeometry(.006,.006,.8,6),0x44ff44,{{p:[-.3,0,0],op:.5}}));
            // nesne
            mainObj.add(_m(new THREE.DodecahedronGeometry(.12),0xff8844,{{p:[-.3,-.5,0]}}));
            // holografik plaka
            mainObj.add(_m(new THREE.BoxGeometry(.5,.6,.02),0x88aa88,{{p:[.5,0,0],op:.3}}));
            // holografik görüntü (hayalet nesne)
            mainObj.add(_mb(new THREE.DodecahedronGeometry(.15),0x44ff88,{{p:[.5,0,.4],op:.3}}));
            mainObj.add(_mb(new THREE.DodecahedronGeometry(.2),0x44ff88,{{p:[.5,0,.4],op:.1}}));
            // girişim deseni (plaka üzerinde)
            for(var i=0;i<10;i++)mainObj.add(_mb(new THREE.BoxGeometry(.005,.5,.005),0x44ff44,{{p:[.48+i*.005,(Math.random()-.5)*.3,0],op:.3}}));
        }}

        scene.add(mainObj);"""

    if ci == 18:  # Deniz Yasami — Ultra Premium 20 sahne
        return f"""mainObj=new THREE.Group();var T={ti};
        function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||60,transparent:!!o.op,opacity:o.op||1,flatShading:!!o.fs,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
        // su parçacıkları (ortak arka plan)
        var bG=new THREE.BufferGeometry();var bP=[];for(var i=0;i<100;i++)bP.push((Math.random()-.5)*6,(Math.random()-.5)*4,(Math.random()-.5)*6);bG.setAttribute('position',new THREE.Float32BufferAttribute(bP,3));mainObj.add(new THREE.Points(bG,new THREE.PointsMaterial({{color:0x88ccff,size:.04,transparent:true,opacity:.2}})));

        // T=0 Balina — büyük mavi balina
        if(T==0){{
            // gövde (uzun oval)
            mainObj.add(_m(new THREE.SphereGeometry(.7,20,16),0x4466aa,{{s:[2.2,1,1]}}));
            // alt karın (açık renk)
            mainObj.add(_m(new THREE.SphereGeometry(.65,20,16),0x8899bb,{{s:[2,0.8,0.9],p:[0,-.1,0]}}));
            // baş (ön, geniş)
            mainObj.add(_m(new THREE.SphereGeometry(.5,16,16),0x4466aa,{{p:[1.2,.1,0],s:[1.2,1,1]}}));
            // alt çene oluk çizgileri (baleen grooves)
            for(var i=0;i<8;i++)mainObj.add(_m(new THREE.CylinderGeometry(.003,.003,.8,4),0x334488,{{p:[.6+i*.05,-.35,0],r:[0,0,Math.PI/2],op:.5}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x222222,{{p:[1,.15,.45]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x222222,{{p:[1,.15,-.45]}}));
            // kuyruk yüzgeci (yatay)
            mainObj.add(_m(new THREE.BoxGeometry(.6,.03,.8),0x3355aa,{{p:[-1.6,0,0],r:[0,0,.1]}}));
            // sırt yüzgeci (küçük)
            mainObj.add(_m(new THREE.ConeGeometry(.06,.2,6),0x3355aa,{{p:[-.4,.65,0]}}));
            // yan yüzgeçler
            mainObj.add(_m(new THREE.BoxGeometry(.4,.02,.15),0x3355aa,{{p:[.5,-.3,.5],r:[0,.3,.3]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.4,.02,.15),0x3355aa,{{p:[.5,-.3,-.5],r:[0,-.3,-.3]}}));
            // üfleme deliği (su püskürtme)
            mainObj.add(_mb(new THREE.CylinderGeometry(.02,.06,.5,6),0xaaddff,{{p:[1.1,.6,0],op:.3}}));
        }}

        // T=1 Yunus — oyuncu yunus
        if(T==1){{
            // gövde (aerodinamik)
            mainObj.add(_m(new THREE.SphereGeometry(.45,20,16),0x7799bb,{{s:[2.5,1,1]}}));
            // alt karın
            mainObj.add(_m(new THREE.SphereGeometry(.4,16,16),0xaabbcc,{{s:[2.3,.8,.9],p:[0,-.05,0]}}));
            // bürün (uzun gaga)
            mainObj.add(_m(new THREE.ConeGeometry(.1,.5,8),0x7799bb,{{p:[1.3,0,0],r:[0,0,-Math.PI/2]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x222222,{{p:[.7,.1,.35]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x222222,{{p:[.7,.1,-.35]}}));
            // sırt yüzgeci (yüksek üçgen)
            mainObj.add(_m(new THREE.ConeGeometry(.08,.35,6),0x6688aa,{{p:[-.1,.5,0],r:[0,0,.1]}}));
            // kuyruk yüzgeci
            mainObj.add(_m(new THREE.BoxGeometry(.45,.03,.55),0x6688aa,{{p:[-1.2,.05,0],r:[0,0,.15]}}));
            // yan yüzgeçler
            mainObj.add(_m(new THREE.ConeGeometry(.15,.25,5),0x6688aa,{{p:[.3,-.25,.35],r:[.3,0,.8]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.15,.25,5),0x6688aa,{{p:[.3,-.25,-.35],r:[-.3,0,.8]}}));
            // gülümseme ağız çizgisi
            mainObj.add(_m(new THREE.TorusGeometry(.12,.005,6,12,Math.PI*.6),0x445566,{{p:[.9,-.05,.3],r:[0,1,-.3],op:.6}}));
        }}

        // T=2 Deniz Kaplumbağası
        if(T==2){{
            // kabuk (üst)
            mainObj.add(_m(new THREE.SphereGeometry(.6,16,12),0x558844,{{s:[1.3,.6,1],p:[0,.1,0]}}));
            // kabuk desenleri (plakalar)
            for(var i=0;i<6;i++){{var a=i*1.047;mainObj.add(_m(new THREE.SphereGeometry(.15,6,6),0x447733,{{p:[Math.cos(a)*.35,.3,Math.sin(a)*.35],s:[1,.3,1]}}));}}
            mainObj.add(_m(new THREE.SphereGeometry(.12,6,6),0x4a7a3a,{{p:[0,.35,0],s:[1,.3,1]}}));
            // alt kabuk (plastron)
            mainObj.add(_m(new THREE.SphereGeometry(.55,16,12),0xddcc88,{{s:[1.2,.3,0.9],p:[0,-.1,0]}}));
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.15,10,10),0x669955,{{p:[.7,.05,0]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.025,6,6),0x222222,{{p:[.82,.1,.1]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,6,6),0x222222,{{p:[.82,.1,-.1]}}));
            // ön yüzgeçler (kürek şekli)
            mainObj.add(_m(new THREE.BoxGeometry(.5,.03,.18),0x669955,{{p:[.3,-.05,.55],r:[0,.4,.2]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.5,.03,.18),0x669955,{{p:[.3,-.05,-.55],r:[0,-.4,-.2]}}));
            // arka yüzgeçler (küçük)
            mainObj.add(_m(new THREE.BoxGeometry(.2,.02,.1),0x669955,{{p:[-.55,-.05,.35],r:[0,.3,.1]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.2,.02,.1),0x669955,{{p:[-.55,-.05,-.35],r:[0,-.3,-.1]}}));
            // kuyruk
            mainObj.add(_m(new THREE.ConeGeometry(.04,.2,6),0x669955,{{p:[-.8,0,0],r:[0,0,Math.PI/2]}}));
        }}

        // T=3 Büyük Beyaz (Köpekbalığı)
        if(T==3){{
            // gövde (torpil şekli)
            mainObj.add(_m(new THREE.SphereGeometry(.5,20,16),0x778899,{{s:[2.5,1,1]}}));
            // alt karın (beyaz)
            mainObj.add(_m(new THREE.SphereGeometry(.45,16,16),0xcccccc,{{s:[2.3,.8,.9],p:[0,-.08,0]}}));
            // bürün (konik)
            mainObj.add(_m(new THREE.ConeGeometry(.25,.5,10),0x778899,{{p:[1.3,.05,0],r:[0,0,-Math.PI/2]}}));
            // ağız (kırmızı yarık)
            mainObj.add(_mb(new THREE.BoxGeometry(.3,.02,.2),0xcc3333,{{p:[.9,-.2,0]}}));
            // dişler (üst + alt)
            for(var i=0;i<8;i++){{mainObj.add(_m(new THREE.ConeGeometry(.015,.05,4),0xffffff,{{p:[.8+i*.04,-.17,0]}}));mainObj.add(_m(new THREE.ConeGeometry(.015,.05,4),0xffffff,{{p:[.8+i*.04,-.23,0],r:[Math.PI,0,0]}}));}}
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[1,.12,.38]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[1,.12,-.38]}}));
            // sırt yüzgeci (ikonik üçgen)
            mainObj.add(_m(new THREE.ConeGeometry(.12,.45,6),0x667788,{{p:[0,.6,0],r:[0,0,.05]}}));
            // kuyruk yüzgeci (asimetrik)
            mainObj.add(_m(new THREE.BoxGeometry(.3,.02,.4),0x667788,{{p:[-1.3,.15,0],r:[0,0,.3]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.2,.02,.3),0x667788,{{p:[-1.25,-.1,0],r:[0,0,-.15]}}));
            // göğüs yüzgeçleri
            mainObj.add(_m(new THREE.ConeGeometry(.15,.35,5),0x667788,{{p:[.3,-.3,.45],r:[.3,0,.7]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.15,.35,5),0x667788,{{p:[.3,-.3,-.45],r:[-.3,0,.7]}}));
            // solungaç çizgileri
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.BoxGeometry(.005,.12,.01),0x556677,{{p:[.6+i*.04,.0,.42],op:.6}}));
        }}

        // T=4 Ahtapot — 8 kollu
        if(T==4){{
            // baş (büyük kafa)
            mainObj.add(_m(new THREE.SphereGeometry(.4,16,16),0xcc6644,{{p:[0,.4,0],s:[1,1.3,1]}}));
            // göz (büyük)
            mainObj.add(_mb(new THREE.SphereGeometry(.08,10,10),0xffff88,{{p:[.25,.45,.25]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x111111,{{p:[.3,.45,.3]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.08,10,10),0xffff88,{{p:[.25,.45,-.25]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x111111,{{p:[.3,.45,-.3]}}));
            // 8 kol (kıvrımlı)
            for(var a=0;a<8;a++){{var ang=a*0.785;for(var s=0;s<6;s++){{var t=s/6;var r=.2+t*.8;var y=-.1-t*.5-Math.sin(t*3)*.15;var curl=Math.sin(t*4+a)*.15;mainObj.add(_m(new THREE.SphereGeometry(.06-t*.007,8,8),0xcc6644,{{p:[Math.cos(ang)*r+curl,y,Math.sin(ang)*r+curl]}}));}}}}
            // vantuzlar (kol altlarında birkaç tane)
            for(var a=0;a<8;a+=2){{var ang=a*0.785;mainObj.add(_m(new THREE.TorusGeometry(.025,.006,6,8),0xdd8866,{{p:[Math.cos(ang)*.5,-.35,Math.sin(ang)*.5],r:[Math.PI/2,0,0]}}));}}
            // sifon
            mainObj.add(_m(new THREE.CylinderGeometry(.04,.06,.12,8),0xbb5533,{{p:[0,.1,.3]}}));
        }}

        // T=5 Denizanası — yarı saydam
        if(T==5){{
            // şemsiye (bell)
            mainObj.add(_m(new THREE.SphereGeometry(.5,20,12,0,6.28,0,2.2),0xcc88ff,{{op:.35,sh:100}}));
            // iç mide boşluğu
            mainObj.add(_m(new THREE.SphereGeometry(.2,12,12),0xdd99ff,{{p:[0,.1,0],op:.3}}));
            // kenar saçaklar (oral arms)
            for(var i=0;i<4;i++){{var a=i*1.57;for(var s=0;s<8;s++){{var t=s/8;mainObj.add(_m(new THREE.SphereGeometry(.03-t*.002,6,6),0xddaaff,{{p:[Math.cos(a)*.08,-.2-t*.8,Math.sin(a)*.08],op:.4}}));}}}}
            // uzun dokunaçlar
            for(var i=0;i<12;i++){{var a=i*.524;for(var s=0;s<10;s++){{var t=s/10;mainObj.add(_mb(new THREE.SphereGeometry(.008,4,4),0xddbbff,{{p:[Math.cos(a)*(.4+t*.1),-.3-t*1.2+Math.sin(t*6)*.05,Math.sin(a)*(.4+t*.1)],op:.3+Math.random()*.2}}));}}}}
            // biyolüminesans glow
            mainObj.add(_mb(new THREE.SphereGeometry(.55,16,12),0xcc88ff,{{op:.06}}));
        }}

        // T=6 Mercan — dallanmış mercan
        if(T==6){{
            // kaya tabanı
            mainObj.add(_m(new THREE.DodecahedronGeometry(.3),0x887766,{{p:[0,-.6,0],s:[2,.5,1.5],fs:true}}));
            // ana dal gövdesi
            mainObj.add(_m(new THREE.CylinderGeometry(.06,.1,.5,8),0xff6644,{{p:[0,-.2,0]}}));
            // dallar
            var bClrs=[0xff6644,0xff7755,0xff8866,0xff5533];
            for(var i=0;i<6;i++){{var a=i*1.047;var h=.3+Math.random()*.3;mainObj.add(_m(new THREE.CylinderGeometry(.03,.05,h,6),bClrs[i%4],{{p:[Math.cos(a)*.15,.1+h/2,Math.sin(a)*.15],r:[Math.sin(a)*.3,0,Math.cos(a)*.3]}}));}}
            // uç poliplerpolip
            for(var i=0;i<10;i++){{var a=Math.random()*6.28;var r=.1+Math.random()*.25;mainObj.add(_m(new THREE.SphereGeometry(.04,8,8),0xff9977,{{p:[Math.cos(a)*r,.4+Math.random()*.3,Math.sin(a)*r]}}));}}
            // ikinci mercan türü (brain coral)
            mainObj.add(_m(new THREE.SphereGeometry(.25,12,12),0x88aa66,{{p:[.5,-.3,.3]}}));
            for(var i=0;i<8;i++)mainObj.add(_m(new THREE.TorusGeometry(.2+i*.005,.01,6,16,Math.PI),0x7799555,{{p:[.5,-.3+i*.02,.3],r:[Math.random()*.5,Math.random()*.5,0],op:.5}}));
        }}

        // T=7 İstiridye — midye kabuğu
        if(T==7){{
            // üst kabuk
            mainObj.add(_m(new THREE.SphereGeometry(.5,16,12,0,6.28,0,1.8),0xccbbaa,{{p:[0,.03,0],s:[1.2,.5,1],sh:80}}));
            // alt kabuk
            mainObj.add(_m(new THREE.SphereGeometry(.5,16,12,0,6.28,0,1.8),0xddccbb,{{p:[0,-.03,0],s:[1.2,.5,1],r:[Math.PI,0,0],sh:80}}));
            // kabuk radyal çizgileri
            for(var i=0;i<12;i++){{var a=i*.524-.5;mainObj.add(_m(new THREE.BoxGeometry(.005,.02,.5),0xbbaa99,{{p:[Math.cos(a)*.3,.04,Math.sin(a)*.3],r:[0,a,0],op:.5}}));}}
            // inci
            mainObj.add(_m(new THREE.SphereGeometry(.08,16,16),0xfff8ee,{{p:[0,0,.1],sh:200}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.1,16,16),0xffffff,{{p:[0,0,.1],op:.1}}));
            // iç manto (parlak sedef)
            mainObj.add(_m(new THREE.SphereGeometry(.45,16,12,0,6.28,0,1.5),0xeeddcc,{{p:[0,.01,0],s:[1.1,.3,.9],sh:120}}));
        }}

        // T=8 Yengeç
        if(T==8){{
            // gövde (oval kabuk)
            mainObj.add(_m(new THREE.SphereGeometry(.35,12,10),0xcc6633,{{s:[1.4,.5,1.2]}}));
            // göz sapları
            mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.12,6),0xbb5522,{{p:[.25,.18,.15]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.12,6),0xbb5522,{{p:[.25,.18,-.15]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,6,6),0x111111,{{p:[.25,.25,.15]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,6,6),0x111111,{{p:[.25,.25,-.15]}}));
            // kıskaçlar (chelipeds) — büyük
            mainObj.add(_m(new THREE.SphereGeometry(.1,8,8),0xdd7744,{{p:[.55,.05,.35],s:[1.3,.6,1]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.08,.03,.06),0xdd7744,{{p:[.7,.1,.35]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.08,.03,.06),0xdd7744,{{p:[.7,.02,.35]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.1,8,8),0xdd7744,{{p:[.55,.05,-.35],s:[1.3,.6,1]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.08,.03,.06),0xdd7744,{{p:[.7,.1,-.35]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.08,.03,.06),0xdd7744,{{p:[.7,.02,-.35]}}));
            // yürüme bacakları (4 çift)
            for(var i=0;i<4;i++){{var z=.15+i*.12;mainObj.add(_m(new THREE.CylinderGeometry(.015,.012,.25,6),0xbb5522,{{p:[-.1+i*.02,-.12,z],r:[0,0,.6+i*.1]}}));mainObj.add(_m(new THREE.CylinderGeometry(.015,.012,.25,6),0xbb5522,{{p:[-.1+i*.02,-.12,-z],r:[0,0,.6+i*.1]}}));}}
        }}

        // T=9 İstakoz
        if(T==9){{
            // gövde (uzun segmentli)
            mainObj.add(_m(new THREE.CylinderGeometry(.2,.15,.8,10),0xcc4422,{{r:[0,0,Math.PI/2],sh:70}}));
            // baş (cephalothorax)
            mainObj.add(_m(new THREE.SphereGeometry(.22,12,10),0xcc4422,{{p:[.5,.02,0],s:[1.3,1,1]}}));
            // kuyruk segmentleri
            for(var i=0;i<5;i++)mainObj.add(_m(new THREE.CylinderGeometry(.13-i*.015,.14-i*.015,.1,8),0xbb3311,{{p:[-.45-i*.12,0,0],r:[0,0,Math.PI/2]}}));
            // kuyruk yelpazesi
            mainObj.add(_m(new THREE.BoxGeometry(.15,.02,.2),0xbb3311,{{p:[-1.05,0,0]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.1,.02,.12),0xaa2211,{{p:[-1.1,0,.12],r:[0,.3,0]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.1,.02,.12),0xaa2211,{{p:[-1.1,0,-.12],r:[0,-.3,0]}}));
            // kıskaçlar
            for(var s=-1;s<=1;s+=2){{mainObj.add(_m(new THREE.CylinderGeometry(.03,.025,.35,6),0xcc4422,{{p:[.7,.05,s*.25],r:[0,0,-Math.PI/4*s*.3]}}));mainObj.add(_m(new THREE.SphereGeometry(.07,8,6),0xdd5533,{{p:[.9,.12,s*.3],s:[1.2,.5,.8]}}));}}
            // antenler
            mainObj.add(_m(new THREE.CylinderGeometry(.005,.005,.7,4),0xcc5544,{{p:[.8,.15,.15],r:[.2,0,-.5]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.005,.005,.7,4),0xcc5544,{{p:[.8,.15,-.15],r:[-.2,0,-.5]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.03,6,6),0x111111,{{p:[.65,.15,.18]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,6,6),0x111111,{{p:[.65,.15,-.18]}}));
        }}

        // T=10 Denizyıldızı — 5 kollu
        if(T==10){{
            // merkez disk
            mainObj.add(_m(new THREE.CylinderGeometry(.2,.2,.06,16),0xff8844,{{r:[Math.PI/2,0,0]}}));
            // 5 kol
            for(var i=0;i<5;i++){{var a=i*1.2566;for(var s=0;s<6;s++){{var t=s/6;var r=.2+t*.5;var w=.1-t*.012;mainObj.add(_m(new THREE.SphereGeometry(w,8,6),0xff8844,{{p:[Math.cos(a)*r,Math.sin(a)*r,.02]}}));}}}}
            // üst yüzey tüberküller (küçük çıkıntılar)
            for(var i=0;i<5;i++){{var a=i*1.2566;for(var s=0;s<3;s++){{var t=s/6;var r=.3+t*.4;mainObj.add(_m(new THREE.SphereGeometry(.015,4,4),0xffaa66,{{p:[Math.cos(a)*r,Math.sin(a)*r,.07]}}));}}}}
            // alt vantuz ayaklar (tube feet)
            for(var i=0;i<5;i++){{var a=i*1.2566;mainObj.add(_m(new THREE.CylinderGeometry(.005,.005,.06,4),0xeebb88,{{p:[Math.cos(a)*.35,Math.sin(a)*.35,-.05],r:[Math.PI/2,0,0]}}));}}
            // göz noktaları (kol ucunda)
            for(var i=0;i<5;i++){{var a=i*1.2566;mainObj.add(_mb(new THREE.SphereGeometry(.012,6,6),0xff2222,{{p:[Math.cos(a)*.7,Math.sin(a)*.7,.04]}}));}}
        }}

        // T=11 Denizatı
        if(T==11){{
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.15,10,10),0xddaa44,{{p:[0,.7,0],s:[1,1.2,.8]}}));
            // uzun bürün
            mainObj.add(_m(new THREE.CylinderGeometry(.02,.03,.2,8),0xddaa44,{{p:[.12,.7,0],r:[0,0,-Math.PI/2]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.025,6,6),0x222222,{{p:[.05,.78,.1]}}));
            // taç (coronet)
            mainObj.add(_m(new THREE.ConeGeometry(.06,.1,6),0xccaa33,{{p:[0,.88,0]}}));
            // boyun ve gövde (segmentli kavisli)
            for(var i=0;i<12;i++){{var t=i/12;var y=.6-t*1.2;var x=Math.sin(t*2)*.1;mainObj.add(_m(new THREE.CylinderGeometry(.1-t*.005,.1-t*.004,.08,8),0xddaa44,{{p:[x,y,0]}}));}}
            // kuyruk (kıvrımlı spiral)
            for(var i=0;i<10;i++){{var t=i/10;var a=t*3;var r=.15-t*.012;mainObj.add(_m(new THREE.SphereGeometry(.04-t*.002,6,6),0xccaa33,{{p:[Math.sin(a)*.12,-.65-t*.4,Math.cos(a)*.05]}}));}}
            // sırt yüzgeci
            mainObj.add(_m(new THREE.BoxGeometry(.02,.15,.12),0xeebb55,{{p:[-.1,.2,.0],op:.7}}));
        }}

        // T=12 Balon Balığı — şişmiş hali
        if(T==12){{
            // şişmiş gövde (küre)
            mainObj.add(_m(new THREE.SphereGeometry(.6,20,20),0xddcc44,{{sh:70}}));
            // alt karın (açık renk)
            mainObj.add(_m(new THREE.SphereGeometry(.55,16,16),0xeeeedd,{{p:[0,-.1,0]}}));
            // dikenler (tüm yüzeyde)
            for(var i=0;i<30;i++){{var a=Math.random()*6.28,b=Math.random()*3.14;var nx=Math.sin(b)*Math.cos(a),ny=Math.cos(b),nz=Math.sin(b)*Math.sin(a);mainObj.add(_m(new THREE.ConeGeometry(.02,.12,5),0xccbb33,{{p:[nx*.6,ny*.6,nz*.6],r:[Math.atan2(Math.sqrt(nx*nx+nz*nz),ny),Math.atan2(nx,nz),0]}}));}}
            // göz (büyük)
            mainObj.add(_mb(new THREE.SphereGeometry(.08,10,10),0xffffff,{{p:[.4,.15,.35]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x222222,{{p:[.45,.15,.4]}}));
            // ağız (küçük)
            mainObj.add(_mb(new THREE.SphereGeometry(.03,6,6),0xcc6644,{{p:[.6,0,0]}}));
            // küçük yüzgeçler
            mainObj.add(_m(new THREE.BoxGeometry(.12,.08,.02),0xccbb44,{{p:[-.5,.1,.35],op:.6}}));
            mainObj.add(_m(new THREE.BoxGeometry(.12,.08,.02),0xccbb44,{{p:[-.5,.1,-.35],op:.6}}));
            mainObj.add(_m(new THREE.ConeGeometry(.08,.15,5),0xccbb44,{{p:[-.6,0,0],r:[0,0,Math.PI/2],op:.6}}));
        }}

        // T=13 Kılıç Balığı
        if(T==13){{
            // gövde
            mainObj.add(_m(new THREE.SphereGeometry(.35,16,12),0x5566aa,{{s:[2.5,1,1]}}));
            // alt (gümüşümsü)
            mainObj.add(_m(new THREE.SphereGeometry(.3,16,12),0xaabbcc,{{s:[2.3,.8,.9],p:[0,-.05,0]}}));
            // kılıç (uzun bürün)
            mainObj.add(_m(new THREE.ConeGeometry(.04,1,6),0x8899aa,{{p:[1.3,.05,0],r:[0,0,-Math.PI/2]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x222222,{{p:[.55,.1,.28]}}));
            // yüksek sırt yüzgeci
            mainObj.add(_m(new THREE.ConeGeometry(.12,.5,6),0x4455aa,{{p:[0,.5,0]}}));
            // kuyruk yüzgeci (orak şekli)
            mainObj.add(_m(new THREE.BoxGeometry(.2,.02,.35),0x4455aa,{{p:[-.95,.2,0],r:[0,0,.4]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.15,.02,.25),0x4455aa,{{p:[-.9,-.15,0],r:[0,0,-.3]}}));
            // göğüs yüzgeçleri
            mainObj.add(_m(new THREE.ConeGeometry(.1,.25,5),0x5566aa,{{p:[.2,-.2,.3],r:[.3,0,.6]}}));
            mainObj.add(_m(new THREE.ConeGeometry(.1,.25,5),0x5566aa,{{p:[.2,-.2,-.3],r:[-.3,0,.6]}}));
        }}

        // T=14 Vatoz — düz disk gövde
        if(T==14){{
            // gövde (düz disk)
            mainObj.add(_m(new THREE.SphereGeometry(.7,20,12),0x667788,{{s:[1.4,.15,1.2]}}));
            // alt (açık)
            mainObj.add(_m(new THREE.SphereGeometry(.65,16,12),0xbbbbcc,{{s:[1.3,.1,1.1],p:[0,-.03,0]}}));
            // kanatlar (yan uzantılar)
            mainObj.add(_m(new THREE.SphereGeometry(.4,12,8),0x667788,{{p:[0,0,.6],s:[1.2,.1,1]}}));
            mainObj.add(_m(new THREE.SphereGeometry(.4,12,8),0x667788,{{p:[0,0,-.6],s:[1.2,.1,1]}}));
            // göz (üstte)
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x222222,{{p:[.3,.08,.15]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x222222,{{p:[.3,.08,-.15]}}));
            // kuyruk (uzun kamçı)
            for(var i=0;i<12;i++){{var t=i/12;mainObj.add(_m(new THREE.SphereGeometry(.02-t*.001,6,6),0x556677,{{p:[-.6-t*1,Math.sin(t*3)*.05,0]}}));}}
            // alt ağız
            mainObj.add(_mb(new THREE.BoxGeometry(.1,.005,.08),0x998877,{{p:[.2,-.08,0]}}));
            // alt solungaç çizgileri
            for(var i=0;i<5;i++)mainObj.add(_mb(new THREE.BoxGeometry(.06,.003,.005),0xaaaaaa,{{p:[.1,-.08,.06-i*.03],op:.5}}));
        }}

        // T=15 Mürekkep Balığı
        if(T==15){{
            // mantle (gövde)
            mainObj.add(_m(new THREE.SphereGeometry(.35,16,12),0x884444,{{s:[1,1.8,1]}}));
            // yüzgeç (yana uzanan)
            mainObj.add(_m(new THREE.SphereGeometry(.2,12,8),0x884444,{{p:[0,.2,.3],s:[.5,1.5,.1],op:.6}}));
            mainObj.add(_m(new THREE.SphereGeometry(.2,12,8),0x884444,{{p:[0,.2,-.3],s:[.5,1.5,.1],op:.6}}));
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.2,12,12),0x994444,{{p:[0,-.5,0]}}));
            // göz (büyük)
            mainObj.add(_mb(new THREE.SphereGeometry(.06,10,10),0xccffcc,{{p:[.15,-.5,.15]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[.18,-.5,.18]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.06,10,10),0xccffcc,{{p:[.15,-.5,-.15]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.03,8,8),0x111111,{{p:[.18,-.5,-.18]}}));
            // 8 kol + 2 uzun tentakül
            for(var i=0;i<8;i++){{var a=i*.785;for(var s=0;s<5;s++){{var t=s/5;mainObj.add(_m(new THREE.SphereGeometry(.03-t*.004,6,6),0x884444,{{p:[Math.cos(a)*(.1+t*.15),-.7-t*.4,Math.sin(a)*(.1+t*.15)]}}));}}}}
            // uzun tentaküller
            for(var s=0;s<8;s++){{var t=s/8;mainObj.add(_m(new THREE.SphereGeometry(.015,4,4),0xaa5555,{{p:[.1+t*.05,-.7-t*.7,.2]}}));mainObj.add(_m(new THREE.SphereGeometry(.015,4,4),0xaa5555,{{p:[-.1-t*.05,-.7-t*.7,-.2]}}));}}
            // mürekkep bulutu
            mainObj.add(_mb(new THREE.SphereGeometry(.15,10,10),0x222222,{{p:[0,-1.2,0],op:.15}}));
        }}

        // T=16 Deniz Kabuğu — spiral kabuk
        if(T==16){{
            // spiral kabuk (nautilus benzeri)
            for(var i=0;i<40;i++){{var t=i/40;var a=t*8;var r=.1+t*.5;var x=Math.cos(a)*r;var y=Math.sin(a)*r;mainObj.add(_m(new THREE.SphereGeometry(.04+t*.04,8,6),0xddccaa,{{p:[x,y,0],sh:80}}));}}
            // kabuk ağzı (açıklık)
            mainObj.add(_m(new THREE.TorusGeometry(.15,.03,8,12,Math.PI*1.5),0xeeddbb,{{p:[.5,0,0],r:[0,0,-.5],sh:90}}));
            // iç sedef renk
            mainObj.add(_m(new THREE.SphereGeometry(.12,10,10),0xffeecc,{{p:[.45,.05,0],sh:120}}));
            // üst yüzey çizgileri (büyüme çizgileri)
            for(var i=0;i<8;i++){{var t=i/8;var a=t*6;var r=.15+t*.45;mainObj.add(_m(new THREE.TorusGeometry(r,.005,6,12,0.5),0xccbb99,{{p:[0,0,0],r:[0,0,a],op:.4}}));}}
        }}

        // T=17 Fok
        if(T==17){{
            // gövde (torpil şekil)
            mainObj.add(_m(new THREE.SphereGeometry(.45,16,12),0x888888,{{s:[2,1,1]}}));
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.25,12,12),0x999999,{{p:[.8,.1,0]}}));
            // bürün
            mainObj.add(_m(new THREE.SphereGeometry(.08,8,8),0x333333,{{p:[1,.12,0]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x222222,{{p:[.9,.2,.2]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.04,8,8),0x222222,{{p:[.9,.2,-.2]}}));
            // bıyıklar
            for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.003,.003,.2,4),0xdddddd,{{p:[.95,.08,.12],r:[0,0,Math.PI/2+i*.15-.15]}}));mainObj.add(_m(new THREE.CylinderGeometry(.003,.003,.2,4),0xdddddd,{{p:[.95,.08,-.12],r:[0,0,Math.PI/2+i*.15-.15]}}));}}
            // ön yüzgeçler
            mainObj.add(_m(new THREE.BoxGeometry(.25,.02,.15),0x777777,{{p:[.4,-.2,.4],r:[0,.3,.4]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.25,.02,.15),0x777777,{{p:[.4,-.2,-.4],r:[0,-.3,-.4]}}));
            // kuyruk yüzgeçleri
            mainObj.add(_m(new THREE.BoxGeometry(.15,.02,.2),0x777777,{{p:[-.9,0,.1],r:[0,.2,0]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.15,.02,.2),0x777777,{{p:[-.9,0,-.1],r:[0,-.2,0]}}));
        }}

        // T=18 Su İguanası
        if(T==18){{
            // gövde
            mainObj.add(_m(new THREE.SphereGeometry(.3,12,10),0x446644,{{s:[2,1,1]}}));
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.18,10,10),0x446644,{{p:[.65,.05,0],s:[1.2,1,.9]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.03,6,6),0xffaa22,{{p:[.75,.12,.14]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.015,4,4),0x111111,{{p:[.78,.12,.15]}}));
            // sırt ibiği (dorsal crest)
            for(var i=0;i<10;i++){{var t=i/10;mainObj.add(_m(new THREE.ConeGeometry(.02,.08-t*.005,5),0x335533,{{p:[.3-t*.8,.28-t*.02,0]}}));}}
            // ön bacaklar
            mainObj.add(_m(new THREE.CylinderGeometry(.03,.02,.25,6),0x446644,{{p:[.3,-.2,.2],r:[.3,0,.4]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.03,.02,.25,6),0x446644,{{p:[.3,-.2,-.2],r:[-.3,0,.4]}}));
            // arka bacaklar
            mainObj.add(_m(new THREE.CylinderGeometry(.035,.025,.3,6),0x446644,{{p:[-.3,-.2,.2],r:[.3,0,.5]}}));
            mainObj.add(_m(new THREE.CylinderGeometry(.035,.025,.3,6),0x446644,{{p:[-.3,-.2,-.2],r:[-.3,0,.5]}}));
            // kuyruk (uzun, yanal yassı)
            for(var i=0;i<10;i++){{var t=i/10;mainObj.add(_m(new THREE.SphereGeometry(.06-t*.004,6,6),0x446644,{{p:[-.6-t*.8,-.05+Math.sin(t*4)*.05,0],s:[1,1.3,.6]}}));}}
            // pençeli ayaklar
            for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.ConeGeometry(.008,.05,4),0x335533,{{p:[.35+i*.02,-.35,.22],r:[0,0,.5+i*.2]}}));}}
        }}

        // T=19 Penguen
        if(T==19){{
            // gövde (siyah)
            mainObj.add(_m(new THREE.SphereGeometry(.35,16,12),0x222222,{{s:[1,1.5,1]}}));
            // karın (beyaz)
            mainObj.add(_m(new THREE.SphereGeometry(.3,16,12),0xffffff,{{p:[.05,-.05,0],s:[.8,1.3,.8]}}));
            // baş
            mainObj.add(_m(new THREE.SphereGeometry(.18,12,12),0x222222,{{p:[0,.55,0]}}));
            // göz
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xffffff,{{p:[.1,.58,.12]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.015,6,6),0x111111,{{p:[.12,.58,.13]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.025,8,8),0xffffff,{{p:[.1,.58,-.12]}}));
            mainObj.add(_mb(new THREE.SphereGeometry(.015,6,6),0x111111,{{p:[.12,.58,-.13]}}));
            // gaga (türüncu)
            mainObj.add(_m(new THREE.ConeGeometry(.04,.12,6),0xff8822,{{p:[.18,.52,0],r:[0,0,-Math.PI/2]}}));
            // kanat/yüzgeçler
            mainObj.add(_m(new THREE.BoxGeometry(.1,.35,.04),0x333333,{{p:[0,.05,.3],r:[0,0,.3]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.1,.35,.04),0x333333,{{p:[0,.05,-.3],r:[0,0,-.3]}}));
            // ayaklar (türüncu)
            mainObj.add(_m(new THREE.BoxGeometry(.1,.02,.08),0xff8822,{{p:[.05,-.55,.1]}}));
            mainObj.add(_m(new THREE.BoxGeometry(.1,.02,.08),0xff8822,{{p:[.05,-.55,-.1]}}));
            // kuyruk (küçük)
            mainObj.add(_m(new THREE.ConeGeometry(.04,.1,6),0x222222,{{p:[-.15,-.4,0],r:[.3,0,.5]}}));
            // yanak rengi (sarı/türüncu leke — emperor penguen)
            mainObj.add(_m(new THREE.SphereGeometry(.06,8,8),0xffaa22,{{p:[.08,.48,.16],op:.6}}));
            mainObj.add(_m(new THREE.SphereGeometry(.06,8,8),0xffaa22,{{p:[.08,.48,-.16],op:.6}}));
        }}

        scene.add(mainObj);"""

    # ci == 19: Muzik Aletleri — Ultra Premium 20 sahne
    return f"""mainObj=new THREE.Group();var T={ti};
    function _m(g,c,o){{o=o||{{}};var mt=new THREE.MeshPhongMaterial({{color:c,shininess:o.sh||60,transparent:!!o.op,opacity:o.op||1,flatShading:!!o.fs,emissive:o.em?new THREE.Color(o.em):undefined,emissiveIntensity:o.ei||0}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}
    function _mb(g,c,o){{o=o||{{}};var mt=new THREE.MeshBasicMaterial({{color:c,transparent:!!o.op,opacity:o.op||1,side:o.ds?THREE.DoubleSide:THREE.FrontSide}});var m=new THREE.Mesh(g,mt);if(o.p)m.position.set(o.p[0],o.p[1],o.p[2]);if(o.r)m.rotation.set(o.r[0],o.r[1],o.r[2]);if(o.s)m.scale.set(o.s[0],o.s[1],o.s[2]);return m;}}

    // T=0 Piyano — kuyruklu piyano
    if(T==0){{
        // gövde (siyah parlak)
        mainObj.add(_m(new THREE.BoxGeometry(2,.15,.9),0x111111,{{sh:120}}));
        // üst kapak (hafif açık)
        mainObj.add(_m(new THREE.BoxGeometry(1.8,.02,.85),0x111111,{{p:[-.1,.3,-.1],r:[0,0,.15],sh:100}}));
        // kapak destek çubuğu
        mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.25,6),0x333333,{{p:[.4,.2,-.3],r:[0,0,.3]}}));
        // beyaz tuşlar (24)
        for(var k=0;k<24;k++){{mainObj.add(_m(new THREE.BoxGeometry(.065,.03,.45),0xffffff,{{p:[-.75+k*.065,.1,.15],sh:100}}));}}
        // siyah tuşlar
        var bkP=[0,1,3,4,5,7,8,10,11,12,14,15,17,18,19,21,22];
        for(var i=0;i<bkP.length;i++){{mainObj.add(_m(new THREE.BoxGeometry(.04,.05,.28),0x111111,{{p:[-.73+bkP[i]*.065,.13,.05],sh:80}}));}}
        // 3 bacak
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.025,.55,8),0x111111,{{p:[-.8,-.35,.3]}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.025,.55,8),0x111111,{{p:[.8,-.35,.3]}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.025,.55,8),0x111111,{{p:[0,-.35,-.35]}}));
        // nota standı
        mainObj.add(_m(new THREE.BoxGeometry(.8,.3,.02),0x222222,{{p:[0,.3,.38],r:[-.2,0,0]}}));
        // pedallar
        for(var i=0;i<3;i++)mainObj.add(_m(new THREE.BoxGeometry(.06,.01,.15),0xDAA520,{{p:[-.1+i*.1,-.6,.3]}}));
    }}

    // T=1 Gitar — akustik gitar
    else if(T==1){{
        // gövde (8 şekli)
        mainObj.add(_m(new THREE.SphereGeometry(.35,16,16),0x8B4513,{{p:[0,-.3,0],s:[1,.35,1]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.28,16,16),0x8B4513,{{p:[0,.05,0],s:[1,.35,1]}}));
        // üst tabla (açık renk)
        mainObj.add(_m(new THREE.SphereGeometry(.34,16,16),0xDEB887,{{p:[0,-.3,.02],s:[1,.34,.08],sh:80}}));
        mainObj.add(_m(new THREE.SphereGeometry(.27,16,16),0xDEB887,{{p:[0,.05,.02],s:[1,.34,.08],sh:80}}));
        // ses deliği
        mainObj.add(_mb(new THREE.CircleGeometry(.08,20),0x222222,{{p:[0,-.15,.18],ds:true}}));
        mainObj.add(_m(new THREE.TorusGeometry(.09,.005,8,20),0x8B4513,{{p:[0,-.15,.18]}}));
        // sap
        mainObj.add(_m(new THREE.BoxGeometry(.08,1,.04),0x8B4513,{{p:[0,.7,0]}}));
        // perde telleri
        for(var i=0;i<12;i++)mainObj.add(_m(new THREE.BoxGeometry(.075,.003,.005),0xcccccc,{{p:[0,.22+i*.07,0.02]}}));
        // kafa (headstock)
        mainObj.add(_m(new THREE.BoxGeometry(.1,.2,.03),0x8B4513,{{p:[0,1.3,0]}}));
        // burgular
        for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.012,.012,.06,6),0xDAA520,{{p:[.06,1.22+i*.06,0],r:[0,0,Math.PI/2]}}));mainObj.add(_m(new THREE.CylinderGeometry(.012,.012,.06,6),0xDAA520,{{p:[-.06,1.22+i*.06,0],r:[0,0,Math.PI/2]}}));}}
        // 6 tel
        for(var s=0;s<6;s++)mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,1.5,4),0xdddddd,{{p:[-.025+s*.01,.4,0.02],sh:120}}));
        // köprü
        mainObj.add(_m(new THREE.BoxGeometry(.1,.015,.02),0x4a3520,{{p:[0,-.4,.18]}}));
    }}

    // T=2 Keman
    else if(T==2){{
        // gövde (bel girişli)
        mainObj.add(_m(new THREE.SphereGeometry(.22,16,16),0x8B4513,{{p:[0,-.25,0],s:[1,.3,1]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.18,16,16),0x8B4513,{{p:[0,.05,0],s:[1,.3,1]}}));
        mainObj.add(_m(new THREE.BoxGeometry(.15,.2,.3),0x8B4513,{{p:[0,-.1,0],s:[1,.3,1]}}));
        // f delikleri
        mainObj.add(_mb(new THREE.BoxGeometry(.01,.08,.005),0x222222,{{p:[.08,-.15,.15],r:[0,0,.2]}}));
        mainObj.add(_mb(new THREE.BoxGeometry(.01,.08,.005),0x222222,{{p:[-.08,-.15,.15],r:[0,0,-.2]}}));
        // sap
        mainObj.add(_m(new THREE.CylinderGeometry(.02,.025,.55,8),0x8B4513,{{p:[0,.35,0]}}));
        // kafa + kıvrım (scroll)
        mainObj.add(_m(new THREE.BoxGeometry(.05,.08,.03),0x4a3520,{{p:[0,.65,0]}}));
        mainObj.add(_m(new THREE.TorusGeometry(.03,.008,6,10,Math.PI*1.5),0x4a3520,{{p:[0,.72,0],r:[0,Math.PI/2,0]}}));
        // 4 tel
        for(var s=0;s<4;s++)mainObj.add(_m(new THREE.CylinderGeometry(.0015,.0015,.8,4),0xdddddd,{{p:[-.015+s*.01,.2,.14],sh:120}}));
        // köprü
        mainObj.add(_m(new THREE.BoxGeometry(.06,.04,.01),0x4a3520,{{p:[0,-.12,.15]}}));
        // kuyruk parçası
        mainObj.add(_m(new THREE.BoxGeometry(.03,.1,.01),0x222222,{{p:[0,-.32,.15]}}));
        // çene dayanağı
        mainObj.add(_m(new THREE.SphereGeometry(.05,8,8),0x222222,{{p:[.08,-.38,.12],s:[1,.5,.8]}}));
        // burgular
        for(var i=0;i<4;i++)mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.04,6),0x4a3520,{{p:[-.02+i*.013,.63,.02],r:[Math.PI/2,0,0]}}));
    }}

    // T=3 Davul — davul seti
    else if(T==3){{
        // bas davul (kiçk)
        mainObj.add(_m(new THREE.CylinderGeometry(.4,.4,.35,20),0xcc3333,{{p:[0,-.2,-.3],r:[Math.PI/2,0,0]}}));
        mainObj.add(_m(new THREE.CircleGeometry(.39,20),0xeeddcc,{{p:[0,-.2,-.13],sh:40,ds:true}}));
        // trampet (snare)
        mainObj.add(_m(new THREE.CylinderGeometry(.2,.2,.12,16),0xcccccc,{{p:[-.35,.1,.2],sh:80}}));
        mainObj.add(_m(new THREE.CircleGeometry(.19,16),0xeeddcc,{{p:[-.35,.17,.2],r:[-Math.PI/2,0,0],ds:true}}));
        // tom-tom (2)
        mainObj.add(_m(new THREE.CylinderGeometry(.15,.15,.12,14),0xcc3333,{{p:[-.15,.35,-.1]}}));
        mainObj.add(_m(new THREE.CircleGeometry(.14,14),0xeeddcc,{{p:[-.15,.42,-.1],r:[-Math.PI/2,0,0],ds:true}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.15,.15,.12,14),0xcc3333,{{p:[.2,.35,-.1]}}));
        mainObj.add(_m(new THREE.CircleGeometry(.14,14),0xeeddcc,{{p:[.2,.42,-.1],r:[-Math.PI/2,0,0],ds:true}}));
        // floor tom
        mainObj.add(_m(new THREE.CylinderGeometry(.2,.2,.2,16),0xcc3333,{{p:[.5,-.1,.2]}}));
        mainObj.add(_m(new THREE.CircleGeometry(.19,16),0xeeddcc,{{p:[.5,.02,.2],r:[-Math.PI/2,0,0],ds:true}}));
        // zil (hi-hat)
        mainObj.add(_m(new THREE.CylinderGeometry(.15,.15,.005,16),0xDAA520,{{p:[-.55,.5,.15],sh:120}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.15,.15,.005,16),0xDAA520,{{p:[-.55,.52,.15],sh:120}}));
        // crash zil
        mainObj.add(_m(new THREE.CylinderGeometry(.18,.18,.005,16),0xDAA520,{{p:[.3,.6,-.2],r:[0,0,.1],sh:120}}));
        // baget (2)
        mainObj.add(_m(new THREE.CylinderGeometry(.008,.005,.3,6),0xDEB887,{{p:[-.2,.35,.3],r:[.3,.2,.5]}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.008,.005,.3,6),0xDEB887,{{p:[.1,.35,.3],r:[.3,-.2,-.5]}}));
        // standlar
        mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.5,6),0x888888,{{p:[-.55,.25,.15]}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.6,6),0x888888,{{p:[.3,.3,-.2]}}));
    }}

    // T=4 Flüt — yan üflemeli
    else if(T==4){{
        // ana gövde
        mainObj.add(_m(new THREE.CylinderGeometry(.022,.022,1.6,12),0xcccccc,{{r:[0,0,Math.PI/2],sh:120}}));
        // baş parçası (headjoint)
        mainObj.add(_m(new THREE.CylinderGeometry(.024,.022,.35,12),0xcccccc,{{p:[-.65,0,0],r:[0,0,Math.PI/2],sh:120}}));
        // ağızlık deliği (emboüçhure)
        mainObj.add(_mb(new THREE.CircleGeometry(.012,10),0x444444,{{p:[-.6,.025,0],r:[-Math.PI/2,0,0],ds:true}}));
        // perdeler (8 ana perde)
        for(var i=0;i<8;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.018,.018,.005,10),0xdddddd,{{p:[-.15+i*.12,.025,0],sh:120}}));mainObj.add(_m(new THREE.CylinderGeometry(.014,.014,.005,10),0xaaaaaa,{{p:[-.15+i*.12,.03,0],sh:100}}));}}
        // perde mekanizmaları (kol/rod)
        mainObj.add(_m(new THREE.CylinderGeometry(.003,.003,1,4),0xbbbbbb,{{p:[0,.03,.015],r:[0,0,Math.PI/2]}}));
        // çan üçu (foot joint)
        mainObj.add(_m(new THREE.CylinderGeometry(.024,.026,.04,12),0xcccccc,{{p:[.8,0,0],r:[0,0,Math.PI/2],sh:120}}));
    }}

    // T=5 Saksafon — altın pirinç
    else if(T==5){{
        // gövde (konik silindir, hafif eğri)
        for(var i=0;i<10;i++){{var t=i/10;var r=.04+t*.08;var y=-.4+t*.9;var x=t>.7?-(t-.7)*.3:0;mainObj.add(_m(new THREE.CylinderGeometry(r,r+.008,.1,12),0xDAA520,{{p:[x,y,0],sh:100}}));}}
        // çan (bell, geniş ağız)
        mainObj.add(_m(new THREE.CylinderGeometry(.06,.18,.15,14),0xDAA520,{{p:[-.12,.55,0],r:[0,0,.3],sh:100}}));
        // boyun (neck, eğri)
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.03,.25,8),0xDAA520,{{p:[.05,-.5,0],r:[0,0,.2],sh:90}}));
        // ağızlık
        mainObj.add(_m(new THREE.CylinderGeometry(.02,.025,.08,8),0x333333,{{p:[.1,-.6,0],r:[0,0,.4]}}));
        // perdeler (yan tuşlar)
        for(var i=0;i<6;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,.005,8),0xDEB887,{{p:[.03,-.2+i*.15,.05],sh:100}}));mainObj.add(_m(new THREE.CylinderGeometry(.005,.005,.03,4),0xDAA520,{{p:[.03,-.2+i*.15,.035],r:[Math.PI/2,0,0]}}));}}
        // octave key
        mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.005,6),0xDEB887,{{p:[-.02,.2,.04],sh:100}}));
    }}

    // T=6 Trompet — pirinç nefesli
    else if(T==6){{
        // ana boru (3 döngü)
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.6,10),0xDAA520,{{p:[0,0,0],r:[0,0,Math.PI/2],sh:110}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.6,10),0xDAA520,{{p:[0,.12,0],r:[0,0,Math.PI/2],sh:110}}));
        // U-dönüşler
        mainObj.add(_m(new THREE.TorusGeometry(.06,.025,8,12,Math.PI),0xDAA520,{{p:[.3,.06,0],r:[Math.PI/2,0,0],sh:110}}));
        mainObj.add(_m(new THREE.TorusGeometry(.06,.025,8,12,Math.PI),0xDAA520,{{p:[-.3,.06,0],r:[Math.PI/2,Math.PI,0],sh:110}}));
        // çan (bell)
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.15,.2,14),0xDAA520,{{p:[.5,0,0],r:[0,0,-Math.PI/2],sh:110}}));
        // ağızlık
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.02,.08,10),0xC8A020,{{p:[-.38,.12,0],r:[0,0,Math.PI/2]}}));
        // 3 piston valfi
        for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,.12,8),0xC8A020,{{p:[-.08+i*.08,.22,0]}}));mainObj.add(_m(new THREE.SphereGeometry(.022,8,8),0xDEB887,{{p:[-.08+i*.08,.28,0],sh:100}}));}}
        // piston boruları
        for(var i=0;i<3;i++)mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.05,8),0xDAA520,{{p:[-.08+i*.08,.06,0]}}));
        // su tahliye valfi
        mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.04,6),0xC8A020,{{p:[.15,-.04,0],r:[0,0,.5]}}));
    }}

    // T=7 Arp — büyük konser arpı
    else if(T==7){{
        // kolon (dikey, kıvrımlı)
        mainObj.add(_m(new THREE.CylinderGeometry(.04,.05,1.5,10),0x8B4513,{{p:[-.35,.3,0]}}));
        // boyun (üst eğri)
        mainObj.add(_m(new THREE.TorusGeometry(.6,.035,8,16,Math.PI*.55),0x8B4513,{{p:[-.05,.95,0],r:[0,0,-.3]}}));
        // ses kutusu (alt)
        mainObj.add(_m(new THREE.BoxGeometry(.15,.3,.12),0x8B4513,{{p:[-.35,-.3,0]}}));
        mainObj.add(_m(new THREE.ConeGeometry(.12,.4,8),0x8B4513,{{p:[-.1,-.3,0],r:[0,0,-Math.PI/2]}}));
        // teller (12 tel)
        for(var s=0;s<12;s++){{var t=s/12;var topX=-.3+t*.5;var topY=.8+Math.sin(t*1.5)*.2;var botX=-.3+t*.02;var botY=-.4;var ln=Math.sqrt((topX-botX)*(topX-botX)+(topY-botY)*(topY-botY));var ang=Math.atan2(topX-botX,topY-botY);var clr=s%7==0?0xff4444:s%7==3?0x4444ff:0xdddddd;mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,ln,4),clr,{{p:[(topX+botX)/2,(topY+botY)/2,0],r:[0,0,ang],sh:120}}));}}
        // süsleme (üst)
        mainObj.add(_m(new THREE.SphereGeometry(.03,8,8),0xDAA520,{{p:[-.35,1.05,0]}}));
        // pedallar (alt)
        for(var i=0;i<4;i++)mainObj.add(_m(new THREE.BoxGeometry(.03,.01,.04),0x666666,{{p:[-.42+i*.04,-.5,0]}}));
    }}

    // T=8 Org — kilise orgu
    else if(T==8){{
        // ana gövde (konsol)
        mainObj.add(_m(new THREE.BoxGeometry(1.2,.6,.4),0x8B4513,{{p:[0,.3,0]}}));
        // org boruları (arkada, farklı boyutlarda)
        for(var i=0;i<12;i++){{var h=.5+Math.abs(i-6)*.08;mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,h,8),0xcccccc,{{p:[-.55+i*.1,.6+h/2,-.1],sh:100}}));mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.01,8),0xbbbbbb,{{p:[-.55+i*.1,.6+h,-.1]}}));}}
        // klavyeler (2 sıra)
        for(var r=0;r<2;r++){{for(var k=0;k<14;k++){{mainObj.add(_m(new THREE.BoxGeometry(.06,.02,.15),0xffffff,{{p:[-.42+k*.06,.55+r*.08,.18]}}));}}}}
        // pedallar (alt)
        for(var i=0;i<8;i++)mainObj.add(_m(new THREE.BoxGeometry(.08,.01,.2),0x6B3410,{{p:[-.35+i*.1,-.05,.1]}}));
        // stop düğmeleri (yanlarda)
        for(var i=0;i<4;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.02,8),0xffffff,{{p:[.55,.4+i*.06,.15],r:[0,0,Math.PI/2]}}));mainObj.add(_m(new THREE.CylinderGeometry(.015,.015,.02,8),0xffffff,{{p:[-.55,.4+i*.06,.15],r:[0,0,Math.PI/2]}}));}}
        // bank
        mainObj.add(_m(new THREE.BoxGeometry(.6,.03,.2),0x8B4513,{{p:[0,-.15,.25]}}));
    }}

    // T=9 Tambur — Türk tamburu
    else if(T==9){{
        // gövde (yarı küre kase)
        mainObj.add(_m(new THREE.SphereGeometry(.35,20,12,0,6.28,0,2.2),0x8B4513,{{p:[0,-.15,0],sh:70}}));
        // tabla (üst yüzey)
        mainObj.add(_m(new THREE.CircleGeometry(.3,20),0xDEB887,{{p:[0,.06,0],r:[-Math.PI/2,0,0],sh:40,ds:true}}));
        // sap (uzun)
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.03,.9,8),0x8B4513,{{p:[0,.55,0]}}));
        // kafa
        mainObj.add(_m(new THREE.BoxGeometry(.06,.12,.025),0x4a3520,{{p:[0,1.05,0]}}));
        // burgular
        for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.04,6),0x4a3520,{{p:[.04,1+i*.04,0],r:[0,0,Math.PI/2]}}));}}
        // 3 tel (çift)
        for(var s=0;s<3;s++)mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,1,4),0xdddddd,{{p:[-.012+s*.012,.55,0.015],sh:120}}));
        // perdeler (bağırsak)
        for(var i=0;i<15;i++)mainObj.add(_m(new THREE.BoxGeometry(.05,.002,.005),0xccaa88,{{p:[0,.15+i*.05,0.015]}}));
    }}

    // T=10 Ney — kamış üflemeli
    else if(T==10){{
        // kamış gövde
        mainObj.add(_m(new THREE.CylinderGeometry(.015,.018,1.4,8),0xDEB887,{{sh:60}}));
        // boğumlar (6)
        for(var i=0;i<6;i++)mainObj.add(_m(new THREE.CylinderGeometry(.02,.02,.008,8),0xccaa77,{{p:[0,-.5+i*.22,0]}}));
        // parmak delikleri (ön 6 + arka 1)
        for(var i=0;i<6;i++)mainObj.add(_mb(new THREE.CircleGeometry(.005,8),0x333333,{{p:[.02,-.35+i*.15,0],r:[0,Math.PI/2,0],ds:true}}));
        mainObj.add(_mb(new THREE.CircleGeometry(.005,8),0x333333,{{p:[-.02,.1,0],r:[0,-Math.PI/2,0],ds:true}}));
        // üfleme üçu (başpare)
        mainObj.add(_m(new THREE.CylinderGeometry(.016,.02,.06,8),0xccaa66,{{p:[0,.72,0]}}));
        // alt uç
        mainObj.add(_m(new THREE.CylinderGeometry(.019,.015,.03,8),0xccaa66,{{p:[0,-.72,0]}}));
    }}

    // T=11 Ud — armut gövdeli
    else if(T==11){{
        // gövde (armut/yarı küre)
        mainObj.add(_m(new THREE.SphereGeometry(.4,20,12,0,6.28,0,2.5),0x8B4513,{{p:[0,-.2,0],r:[Math.PI,0,0],sh:60}}));
        // tabla (düz ön yüz)
        mainObj.add(_m(new THREE.CircleGeometry(.38,20),0xDEB887,{{p:[0,-.2,.01],sh:50,ds:true}}));
        // ses delikleri (gül - rozet)
        mainObj.add(_m(new THREE.TorusGeometry(.06,.005,8,16),0x4a3520,{{p:[0,-.25,.02]}}));
        mainObj.add(_m(new THREE.TorusGeometry(.08,.003,8,16),0x4a3520,{{p:[0,-.25,.02]}}));
        // sap (kısa, genişçe)
        mainObj.add(_m(new THREE.BoxGeometry(.08,.6,.03),0x8B4513,{{p:[0,.25,0]}}));
        // kafa (geri kıvrık)
        mainObj.add(_m(new THREE.BoxGeometry(.08,.15,.025),0x4a3520,{{p:[0,.6,-.03],r:[.5,0,0]}}));
        // 5 çift tel (11 tel)
        for(var s=0;s<5;s++)mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,.9,4),0xdddddd,{{p:[-.02+s*.01,.15,.015],sh:120}}));
        // perdeler
        for(var i=0;i<10;i++)mainObj.add(_m(new THREE.BoxGeometry(.07,.002,.005),0xccaa88,{{p:[0,.02+i*.05,.015]}}));
        // burgular
        for(var i=0;i<5;i++)mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.05,6),0x4a3520,{{p:[.05,(.58+i*.03),-.04],r:[0,0,Math.PI/2]}}));
    }}

    // T=12 Kanun — yatay telli
    else if(T==12){{
        // trapez gövde
        var pts=[];pts.push(new THREE.Vector2(-.6,-.3));pts.push(new THREE.Vector2(.6,-.3));pts.push(new THREE.Vector2(.4,.3));pts.push(new THREE.Vector2(-.6,.3));
        mainObj.add(_m(new THREE.BoxGeometry(1.3,.06,.7),0x8B4513,{{p:[0,0,0],sh:50}}));
        // üst tabla (açık)
        mainObj.add(_m(new THREE.BoxGeometry(1.25,.005,.65),0xDEB887,{{p:[0,.035,0]}}));
        // 26 tel
        for(var s=0;s<26;s++){{var t=s/26;var len=.55+t*.1;mainObj.add(_m(new THREE.CylinderGeometry(.001,.001,len,4),0xdddddd,{{p:[-.55+s*.04,.04,0],r:[Math.PI/2,0,0],sh:120}}));}}
        // köprü dizisi
        mainObj.add(_m(new THREE.BoxGeometry(.8,.01,.015),0x4a3520,{{p:[.05,.04,.25]}}));
        mainObj.add(_m(new THREE.BoxGeometry(.8,.01,.015),0x4a3520,{{p:[.05,.04,-.25]}}));
        // mandal dizisi (sağ taraf)
        for(var i=0;i<8;i++)mainObj.add(_m(new THREE.CylinderGeometry(.006,.006,.015,6),0xDAA520,{{p:[.5,.05,-.28+i*.07]}}));
        // süsleme (rozet delikleri)
        for(var i=0;i<3;i++)mainObj.add(_m(new THREE.TorusGeometry(.03,.003,6,12),0x4a3520,{{p:[-.3+i*.2,.04,.0]}}));
    }}

    // T=13 Bağlama — saz
    else if(T==13){{
        // gövde (yarı armut)
        mainObj.add(_m(new THREE.SphereGeometry(.3,20,12,0,6.28,0,2.5),0x8B4513,{{p:[0,-.35,0],r:[Math.PI,0,0],sh:60}}));
        // tabla
        mainObj.add(_m(new THREE.CircleGeometry(.28,20),0xDEB887,{{p:[0,-.35,.01],sh:50,ds:true}}));
        // uzun sap
        mainObj.add(_m(new THREE.BoxGeometry(.06,1,.025),0x8B4513,{{p:[0,.25,0]}}));
        // kafa
        mainObj.add(_m(new THREE.BoxGeometry(.06,.12,.02),0x4a3520,{{p:[0,.8,0]}}));
        // burgular (6 — 3 çift)
        for(var i=0;i<3;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.05,6),0x4a3520,{{p:[.04,.76+i*.03,0],r:[0,0,Math.PI/2]}}));mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.05,6),0x4a3520,{{p:[-.04,.76+i*.03,0],r:[0,0,Math.PI/2]}}));}}
        // 7 tel (3 çift + 1)
        for(var s=0;s<3;s++)mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,1.2,4),0xdddddd,{{p:[-.01+s*.01,.1,.013],sh:120}}));
        // perdeler (bağırsak, çoğu eğri)
        for(var i=0;i<18;i++)mainObj.add(_m(new THREE.BoxGeometry(.05,.002,.005),0xccaa88,{{p:[0,-.15+i*.05,.013]}}));
        // tezene (mızrap)
        mainObj.add(_m(new THREE.BoxGeometry(.03,.005,.015),0x990000,{{p:[.15,-.2,.05],r:[0,0,.3]}}));
    }}

    // T=14 Def — çerçeve davul
    else if(T==14){{
        // çerçeve (halka)
        mainObj.add(_m(new THREE.TorusGeometry(.4,.04,10,24),0x8B4513,{{r:[Math.PI/2,0,0]}}));
        // deri (membran)
        mainObj.add(_m(new THREE.CircleGeometry(.4,24),0xeeddcc,{{r:[0,0,0],sh:30,ds:true}}));
        // ziller (5 çift)
        for(var i=0;i<5;i++){{var a=i*1.2566;mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.003,10),0xDAA520,{{p:[Math.cos(a)*.38,Math.sin(a)*.38,.04],sh:120}}));mainObj.add(_m(new THREE.CylinderGeometry(.03,.03,.003,10),0xDAA520,{{p:[Math.cos(a)*.38,Math.sin(a)*.38,-.04],sh:120}}));}}
        // tutma sapı
        mainObj.add(_m(new THREE.BoxGeometry(.04,.12,.04),0x8B4513,{{p:[0,-.45,.0]}}));
    }}

    // T=15 Zil — orkestra zili (crash)
    else if(T==15){{
        // zil diski
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.5,.01,24),0xDAA520,{{sh:140}}));
        // merkez kubbe (bell)
        mainObj.add(_m(new THREE.SphereGeometry(.06,12,8,0,6.28,0,1.8),0xC8A020,{{p:[0,.02,0],sh:150}}));
        // kayış deliği
        mainObj.add(_mb(new THREE.CircleGeometry(.008,8),0x333333,{{p:[0,.06,0],r:[-Math.PI/2,0,0],ds:true}}));
        // deri kayış
        mainObj.add(_m(new THREE.BoxGeometry(.015,.15,.005),0x8B4513,{{p:[0,.1,0]}}));
        // ikinci zil (alttan)
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.48,.01,24),0xC8A020,{{p:[0,-.15,0],sh:130}}));
        mainObj.add(_m(new THREE.SphereGeometry(.06,12,8,0,6.28,0,1.8),0xB89020,{{p:[0,-.13,0],sh:140}}));
        // yüzey çizgileri (lathing)
        for(var i=1;i<5;i++)mainObj.add(_m(new THREE.TorusGeometry(i*.1,.002,6,20),0xBBA030,{{p:[0,.008,0],r:[Math.PI/2,0,0],op:.3}}));
    }}

    // T=16 Trombon — sürgülü
    else if(T==16){{
        // ana boru (U dönüşlü)
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.8,10),0xDAA520,{{p:[-.1,.2,0],r:[0,0,Math.PI/2],sh:110}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.8,10),0xDAA520,{{p:[-.1,-.05,0],r:[0,0,Math.PI/2],sh:110}}));
        // U dönüşleri
        mainObj.add(_m(new THREE.TorusGeometry(.125,.025,8,12,Math.PI),0xDAA520,{{p:[.3,.075,0],r:[Math.PI/2,0,0],sh:110}}));
        mainObj.add(_m(new THREE.TorusGeometry(.125,.025,8,12,Math.PI),0xDAA520,{{p:[-.5,.075,0],r:[Math.PI/2,Math.PI,0],sh:110}}));
        // sürgü (slide) — dış borular
        mainObj.add(_m(new THREE.CylinderGeometry(.028,.028,.7,10),0xC8A020,{{p:[-.1,-.3,0],r:[0,0,Math.PI/2],sh:100}}));
        mainObj.add(_m(new THREE.CylinderGeometry(.028,.028,.7,10),0xC8A020,{{p:[-.1,-.5,0],r:[0,0,Math.PI/2],sh:100}}));
        mainObj.add(_m(new THREE.TorusGeometry(.1,.028,8,12,Math.PI),0xC8A020,{{p:[.25,-.4,0],r:[Math.PI/2,0,0],sh:100}}));
        // çan (bell)
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.15,.2,14),0xDAA520,{{p:[-.55,.2,0],r:[0,0,Math.PI/2],sh:110}}));
        // ağızlık
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.02,.06,10),0xC8A020,{{p:[-.55,-.05,0]}}));
        // su boşaltma valfi
        mainObj.add(_m(new THREE.CylinderGeometry(.008,.008,.03,6),0xC8A020,{{p:[.1,-.08,0],r:[0,0,.5]}}));
    }}

    // T=17 Çello — büyük telli
    else if(T==17){{
        // gövde (büyük 8 şekli)
        mainObj.add(_m(new THREE.SphereGeometry(.35,16,16),0x8B4513,{{p:[0,-.4,0],s:[1,.35,1]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.28,16,16),0x8B4513,{{p:[0,-.05,0],s:[1,.35,1]}}));
        mainObj.add(_m(new THREE.BoxGeometry(.2,.25,.35),0x8B4513,{{p:[0,-.22,0],s:[1,.35,1]}}));
        // tabla
        mainObj.add(_m(new THREE.SphereGeometry(.34,16,16),0xDEB887,{{p:[0,-.4,.02],s:[1,.34,.06]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.27,16,16),0xDEB887,{{p:[0,-.05,.02],s:[1,.34,.06]}}));
        // f delikleri
        mainObj.add(_mb(new THREE.BoxGeometry(.008,.1,.005),0x222222,{{p:[.1,-.25,.2],r:[0,0,.15]}}));
        mainObj.add(_mb(new THREE.BoxGeometry(.008,.1,.005),0x222222,{{p:[-.1,-.25,.2],r:[0,0,-.15]}}));
        // sap
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.03,.7,8),0x8B4513,{{p:[0,.35,0]}}));
        // kafa + kıvrım
        mainObj.add(_m(new THREE.BoxGeometry(.06,.1,.03),0x4a3520,{{p:[0,.75,0]}}));
        mainObj.add(_m(new THREE.TorusGeometry(.03,.008,6,10,Math.PI*1.5),0x4a3520,{{p:[0,.82,0],r:[0,Math.PI/2,0]}}));
        // 4 tel
        for(var s=0;s<4;s++)mainObj.add(_m(new THREE.CylinderGeometry(.002,.002,1,4),0xdddddd,{{p:[-.015+s*.01,.15,.18],sh:120}}));
        // köprü
        mainObj.add(_m(new THREE.BoxGeometry(.06,.05,.01),0x4a3520,{{p:[0,-.22,.2]}}));
        // kuyruk
        mainObj.add(_m(new THREE.BoxGeometry(.03,.12,.01),0x222222,{{p:[0,-.45,.18]}}));
        // sivri ayak (endpin)
        mainObj.add(_m(new THREE.CylinderGeometry(.008,.005,.25,6),0x888888,{{p:[0,-.65,0]}}));
    }}

    // T=18 Kontrbas — en büyük yaylı
    else if(T==18){{
        // gövde
        mainObj.add(_m(new THREE.SphereGeometry(.4,16,16),0x8B4513,{{p:[0,-.5,0],s:[1,.35,1]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.32,16,16),0x8B4513,{{p:[0,-.1,0],s:[1,.35,1]}}));
        // tabla
        mainObj.add(_m(new THREE.SphereGeometry(.38,16,16),0xDEB887,{{p:[0,-.5,.02],s:[1,.34,.06]}}));
        mainObj.add(_m(new THREE.SphereGeometry(.3,16,16),0xDEB887,{{p:[0,-.1,.02],s:[1,.34,.06]}}));
        // uzun sap
        mainObj.add(_m(new THREE.CylinderGeometry(.03,.035,1.1,8),0x8B4513,{{p:[0,.45,0]}}));
        // kafa
        mainObj.add(_m(new THREE.BoxGeometry(.07,.12,.03),0x4a3520,{{p:[0,1.05,0]}}));
        mainObj.add(_m(new THREE.TorusGeometry(.035,.01,6,10,Math.PI*1.5),0x4a3520,{{p:[0,1.13,0],r:[0,Math.PI/2,0]}}));
        // 4 tel
        for(var s=0;s<4;s++)mainObj.add(_m(new THREE.CylinderGeometry(.003,.003,1.5,4),0xdddddd,{{p:[-.02+s*.013,.2,.16],sh:110}}));
        // köprü
        mainObj.add(_m(new THREE.BoxGeometry(.08,.06,.01),0x4a3520,{{p:[0,-.3,.2]}}));
        // kuyruk
        mainObj.add(_m(new THREE.BoxGeometry(.035,.15,.01),0x222222,{{p:[0,-.55,.18]}}));
        // sivri ayak
        mainObj.add(_m(new THREE.CylinderGeometry(.01,.005,.3,6),0x888888,{{p:[0,-.8,0]}}));
        // f delikleri
        mainObj.add(_mb(new THREE.BoxGeometry(.008,.12,.005),0x222222,{{p:[.12,-.35,.2],r:[0,0,.1]}}));
        mainObj.add(_mb(new THREE.BoxGeometry(.008,.12,.005),0x222222,{{p:[-.12,-.35,.2],r:[0,0,-.1]}}));
    }}

    // T=19 Klarnet — siyah tahta nefesli
    else if(T==19){{
        // gövde (siyah, uzun)
        mainObj.add(_m(new THREE.CylinderGeometry(.022,.028,1.2,12),0x222222,{{sh:80}}));
        // çan (bell)
        mainObj.add(_m(new THREE.CylinderGeometry(.028,.06,.08,12),0x222222,{{p:[0,-.64,0],sh:80}}));
        // barel (barrel joint)
        mainObj.add(_m(new THREE.CylinderGeometry(.025,.025,.1,12),0x333333,{{p:[0,.55,0],sh:70}}));
        // ağızlık + kamış
        mainObj.add(_m(new THREE.CylinderGeometry(.02,.025,.08,8),0x333333,{{p:[0,.65,0]}}));
        mainObj.add(_m(new THREE.BoxGeometry(.015,.06,.005),0xDEB887,{{p:[.015,.67,0]}}));
        // perdeler (anahtar mekanizmaları) — gümüş
        for(var i=0;i<7;i++){{mainObj.add(_m(new THREE.CylinderGeometry(.016,.016,.005,8),0xcccccc,{{p:[.03,-.35+i*.12,0],sh:120}}));mainObj.add(_m(new THREE.CylinderGeometry(.004,.004,.025,4),0xcccccc,{{p:[.03,-.35+i*.12,.015],r:[Math.PI/2,0,0]}}));}}
        // register key (başparmak)
        mainObj.add(_m(new THREE.CylinderGeometry(.01,.01,.005,6),0xcccccc,{{p:[-.025,.3,0],sh:120}}));
        // bağlantı halkaları (metal)
        for(var i=0;i<4;i++)mainObj.add(_m(new THREE.TorusGeometry(.025,.003,6,12),0xcccccc,{{p:[0,-.4+i*.3,0],r:[Math.PI/2,0,0],sh:100}}));
        // ligature (ağızlıktaki metal bant)
        mainObj.add(_m(new THREE.TorusGeometry(.022,.003,6,12),0xDAA520,{{p:[0,.63,0],r:[Math.PI/2,0,0],sh:100}}));
    }}

    else{{
        // fallback (basit silindirsel alet)
        mainObj.add(_m(new THREE.CylinderGeometry(.15,.12,.6,12),0x8B4513,{{sh:60}}));
    }}

    scene.add(mainObj);"""


# ══════════════════════════════════════════════════════════════
# 3D HTML BUILDER
# ══════════════════════════════════════════════════════════════

@st.cache_data(show_spinner=False, max_entries=50)
def _build_3d_html(ci, ti, name, height=460):
    """Tam HTML belgesi — Three.js 3D sahne."""
    geo_js = _scene_js(ci, ti)
    extra_anim = ""
    if ci == 1:
        extra_anim = "if(window._orbits)window._orbits.forEach(function(o){var a=_t*o.spd*60;o.el.position.x=Math.cos(a)*o.rad;o.el.position.z=Math.sin(a)*o.rad;});"

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body style="margin:0;padding:0;overflow:hidden;background:#0f172a;touch-action:none">
<div id="sc3dv" style="width:100%;height:{height}px;position:relative;cursor:grab;
    background:linear-gradient(160deg,#0f172a,#1e293b);">
    <div style="position:absolute;top:12px;left:16px;z-index:10;
        font-size:12px;color:rgba(255,255,255,0.4);pointer-events:none;
        font-weight:600;font-family:sans-serif">{name}</div>
    <div style="position:absolute;bottom:10px;right:14px;z-index:10;
        font-size:10px;color:rgba(255,255,255,0.25);pointer-events:none;
        font-family:sans-serif">Surukle: Dondur | Scroll: Zoom</div>
</div>
<script>
window.onload=function(){{
    var c=document.getElementById('sc3dv');
    var w=c.offsetWidth||600,h={height};
    var scene=new THREE.Scene();
    var cam=new THREE.PerspectiveCamera(50,w/h,0.1,1000);cam.position.z=4;
    var rdr=new THREE.WebGLRenderer({{antialias:true,alpha:true}});
    rdr.setSize(w,h);rdr.setPixelRatio(Math.min(window.devicePixelRatio,1.5));
    c.appendChild(rdr.domElement);
    var _dl1=new THREE.DirectionalLight(0xffffff,1.2);_dl1.position.set(5,5,5);scene.add(_dl1);
    var _dl2=new THREE.DirectionalLight(0xffffff,0.6);_dl2.position.set(-3,3,-3);scene.add(_dl2);
    scene.add(new THREE.AmbientLight(0x606080,0.8));
    var mainObj;
    {geo_js}
    var drag=false,pM={{x:0,y:0}},rY=0,rX=0,zm=4;
    c.onmousedown=function(e){{drag=true;pM={{x:e.clientX,y:e.clientY}};c.style.cursor='grabbing';}};
    c.onmousemove=function(e){{if(!drag)return;rY+=(e.clientX-pM.x)*0.008;rX+=(e.clientY-pM.y)*0.008;
        rX=Math.max(-1.5,Math.min(1.5,rX));pM={{x:e.clientX,y:e.clientY}};}};
    c.onmouseup=function(){{drag=false;c.style.cursor='grab';}};
    c.onmouseleave=function(){{drag=false;c.style.cursor='grab';}};
    document.addEventListener('wheel',function(e){{zm+=e.deltaY*0.003;zm=Math.max(1.5,Math.min(12,zm));e.preventDefault();e.stopPropagation();}},{{passive:false}});
    document.addEventListener('touchstart',function(e){{if(e.touches.length===1){{drag=true;pM={{x:e.touches[0].clientX,y:e.touches[0].clientY}};}}e.preventDefault();}},{{passive:false}});
    document.addEventListener('touchmove',function(e){{if(!drag||!e.touches.length)return;rY+=(e.touches[0].clientX-pM.x)*0.008;
        rX+=(e.touches[0].clientY-pM.y)*0.008;rX=Math.max(-1.5,Math.min(1.5,rX));
        pM={{x:e.touches[0].clientX,y:e.touches[0].clientY}};e.preventDefault();}},{{passive:false}});
    document.addEventListener('touchend',function(){{drag=false;}});
    var _t=0;
    function anim(){{requestAnimationFrame(anim);cam.position.z=zm;_t+=0.016;
        if(mainObj){{if(!drag)rY+=0.004;mainObj.rotation.y=rY;mainObj.rotation.x=rX;}}
        {extra_anim}
        rdr.render(scene,cam);}}
    anim();
}};
</script>
</body></html>"""


def _build_portrait_gallery_html(ci, ti, topic_name, height=480):
    """Wikipedia REST API üzerinden portre + eser galerisi HTML bileseni."""
    wiki_article = _WIKI.get(ci, [""])[ti] if ci in _WIKI and ti < len(_WIKI[ci]) else ""
    works_raw = _WIKI_WORKS.get(ci, [[]])[ti] if ci in _WIKI_WORKS and ti < len(_WIKI_WORKS.get(ci, [])) else []
    works_js = json.dumps(works_raw, ensure_ascii=False)
    cat_labels = {20: "Bilim Insani", 21: "Ressam", 22: "Kasif", 23: "Yazar"}
    works_title = {21: "Unlu Eserleri", 22: "Önemli Kesifleri", 23: "Basliça Eserleri"}
    cat_label = cat_labels.get(ci, "")
    w_title = works_title.get(ci, "Eserleri")
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:linear-gradient(160deg,#0f172a,#1e293b);color:#e2e8f0;overflow-x:hidden}}
.gallery{{padding:16px 20px}}
.portrait-sec{{display:flex;gap:20px;align-items:flex-start;margin-bottom:18px}}
.portrait-frame{{flex-shrink:0;width:200px;height:260px;border-radius:16px;overflow:hidden;
  background:linear-gradient(135deg,#1e293b,#334155);border:2px solid rgba(255,255,255,.08);
  box-shadow:0 8px 32px rgba(0,0,0,.4);position:relative}}
.portrait-frame img{{width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s}}
.portrait-frame img.loaded{{opacity:1}}
.portrait-frame .loader{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:36px;height:36px;border:3px solid rgba(255,255,255,.1);border-top-color:#8b5cf6;
  border-radius:50%;animation:spin 1s linear infinite}}
@keyframes spin{{to{{transform:translate(-50%,-50%) rotate(360deg)}}}}
.portrait-frame .fallback{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:4rem;opacity:.3;display:none}}
.info-sec{{flex:1;min-width:0}}
.info-sec h2{{font-size:1.3rem;font-weight:800;color:#1A2035;margin-bottom:4px}}
.info-sec .cat-badge{{display:inline-block;padding:3px 10px;border-radius:20px;
  font-size:.7rem;font-weight:600;background:rgba(139,92,246,.2);color:#c4b5fd;
  margin-bottom:8px}}
.info-sec .desc{{font-size:.82rem;color:#94a3b8;line-height:1.7}}
.works-sec{{margin-top:6px}}
.works-sec h3{{font-size:.95rem;font-weight:700;color:#1A2035;margin-bottom:10px;
  padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,.08)}}
.works-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}}
.work-card{{border-radius:12px;overflow:hidden;background:linear-gradient(135deg,#1e293b,#334155);
  border:1px solid rgba(255,255,255,.06);transition:all .2s;cursor:pointer}}
.work-card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.4);
  border-color:rgba(139,92,246,.3)}}
.work-card .wimg{{width:100%;height:130px;object-fit:cover;background:rgba(255,255,255,.03);
  display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.work-card .wimg img{{width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s}}
.work-card .wimg img.loaded{{opacity:1}}
.work-card .wimg .wloader{{position:absolute;width:24px;height:24px;
  border:2px solid rgba(255,255,255,.08);border-top-color:#a78bfa;border-radius:50%;
  animation:spin .8s linear infinite}}
.work-card .wimg .wfallback{{font-size:2.2rem;opacity:.25;display:none}}
.work-card .wlabel{{padding:8px 10px;font-size:.75rem;font-weight:600;color:#e2e8f0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.modal-overlay{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;
  background:rgba(0,0,0,.85);z-index:1000;align-items:center;justify-content:center;
  cursor:zoom-out}}
.modal-overlay.show{{display:flex}}
.modal-overlay img{{max-width:90%;max-height:90%;border-radius:12px;
  box-shadow:0 20px 60px rgba(0,0,0,.6)}}
.modal-title{{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);
  color:#1A2035;font-size:1rem;font-weight:700;text-align:center;
  background:rgba(15,23,42,.8);padding:8px 20px;border-radius:20px}}
</style></head><body>
<div class="gallery">
<div class="portrait-sec">
  <div class="portrait-frame" id="pFrame">
    <div class="loader" id="pLoader"></div>
    <div class="fallback" id="pFallback">\U0001f9d1\u200d\U0001f3a8</div>
    <img id="pImg" alt="{topic_name}">
  </div>
  <div class="info-sec">
    <h2>{topic_name}</h2>
    <span class="cat-badge">{cat_label}</span>
    <div class="desc" id="pDesc">Bilgi yukleniyor...</div>
  </div>
</div>
<div class="works-sec" id="worksSec" style="display:none">
  <h3>\U0001f3a8 {w_title}</h3>
  <div class="works-grid" id="worksGrid"></div>
</div>
</div>
<div class="modal-overlay" id="modal" onclick="this.className='modal-overlay'">
  <img id="modalImg"><div class="modal-title" id="modalTitle"></div>
</div>
<script>
var wikiArt="{wiki_article}";
var works={works_js};
var API="https://en.wikipedia.org/api/rest_v1/page/summary/";
// Fallback emojileri
var catEmoji={{20:"\U0001f52c",21:"\U0001f3a8",22:"\U0001f9ed",23:"\U0001f4da"}};
var ci={ci};
// Portre yukle
async function loadPortrait(){{
  try{{
    var r=await fetch(API+encodeURIComponent(wikiArt.replace(/%[0-9A-Fa-f]{{2}}/g,function(m){{return decodeURIComponent(m)}})));
    var d=await r.json();
    var url=d.originalimage?d.originalimage.source:(d.thumbnail?d.thumbnail.source:null);
    if(url){{
      var img=document.getElementById("pImg");
      img.onload=function(){{img.classList.add("loaded");document.getElementById("pLoader").style.display="none";}};
      img.onerror=function(){{showFallback()}};
      img.src=url;
    }}else{{showFallback()}}
    if(d.extract)document.getElementById("pDesc").textContent=d.extract;
  }}catch(e){{showFallback()}}
}}
function showFallback(){{
  document.getElementById("pLoader").style.display="none";
  document.getElementById("pFallback").style.display="block";
}}
// Eserleri yukle
async function loadWorks(){{
  if(!works||works.length===0)return;
  document.getElementById("worksSec").style.display="block";
  var grid=document.getElementById("worksGrid");
  for(var i=0;i<works.length;i++){{
    var w=works[i];var wArt=w[0],wName=w[1];
    var card=document.createElement("div");card.className="work-card";
    card.innerHTML='<div class="wimg"><div class="wloader"></div><div class="wfallback">'+
      (catEmoji[ci]||"\U0001f5bc\ufe0f")+'</div></div><div class="wlabel">'+wName+'</div>';
    card.setAttribute("data-name",wName);
    grid.appendChild(card);
    // Gorseli yukle
    (function(cardEl,article,name){{
      fetch(API+encodeURIComponent(article.replace(/%[0-9A-Fa-f]{{2}}/g,function(m){{return decodeURIComponent(m)}})))
        .then(function(r){{return r.json()}})
        .then(function(d){{
          var url=d.originalimage?d.originalimage.source:(d.thumbnail?d.thumbnail.source:null);
          var wimgDiv=cardEl.querySelector(".wimg");
          if(url){{
            var img=document.createElement("img");
            img.onload=function(){{img.classList.add("loaded");
              wimgDiv.querySelector(".wloader").style.display="none";}};
            img.onerror=function(){{wimgDiv.querySelector(".wloader").style.display="none";
              wimgDiv.querySelector(".wfallback").style.display="block";}};
            img.src=url;
            wimgDiv.appendChild(img);
            cardEl.onclick=function(){{
              document.getElementById("modalImg").src=url;
              document.getElementById("modalTitle").textContent=name;
              document.getElementById("modal").className="modal-overlay show";
            }};
          }}else{{
            wimgDiv.querySelector(".wloader").style.display="none";
            wimgDiv.querySelector(".wfallback").style.display="block";
          }}
        }}).catch(function(){{
          var wimgDiv=cardEl.querySelector(".wimg");
          wimgDiv.querySelector(".wloader").style.display="none";
          wimgDiv.querySelector(".wfallback").style.display="block";
        }});
    }})(card,wArt,wName);
  }}
}}
loadPortrait();
loadWorks();
</script></body></html>'''


# ══════════════════════════════════════════════════════════════
# VERI OTOMATIK URETIMI — 400 ICERIK
# ══════════════════════════════════════════════════════════════

def _auto_generate(store):
    """20 kategori x 20 konu = 400 içerik otomatik olustur."""
    contents = []
    for ci, (cat_name, emoji, color, topics) in enumerate(_CATS):
        for ti, topic_name in enumerate(topics):
            code = f"SC3D-{ci:02d}-{ti:02d}"
            contents.append(SC3DContent(
                content_code=code,
                content_name=topic_name,
                category=cat_name,
                sub_category="",
                grade_min=2 + ci % 6,
                grade_max=8 + ci % 5,
                lesson=cat_name,
                unit=f"Unite {ti+1}",
                learning_outcome=f"{topic_name} yapisini 3D olarak inceleyebilme",
                tags=f"3D,{cat_name},{topic_name}",
                difficulty=["Kolay", "Orta", "Zor"][ti % 3],
                estimated_minutes=5 + ti % 10,
                language="TR",
                status="PUBLISHED",
            ))
    store.save_list("contents", [c.to_dict() for c in contents])
    # Temiz hotspot/tour/quiz
    store.save_list("hotspots", [])
    store.save_list("tour_steps", [])
    store.save_list("quizzes", [])
    return len(contents)


# ══════════════════════════════════════════════════════════════
# RENDER FONKSIYONLARI
# ══════════════════════════════════════════════════════════════

def _render_hero(n):
    styled_header("Üç Boyutlu Egitim",
                    f"{n} içerik | {len(_CATS)} kategori | 400 benzersiz 3D sahne",
                    "\U0001f3ac")
    styled_stat_row([
        ("Toplam Icerik", str(n), _CLR["blue"], "\U0001f4da"),
        ("Kategori", str(len(_CATS)), _CLR["purple"], "\U0001f4c2"),
        ("3D Sahne", str(n), _CLR["green"], "\U0001f3ac"),
        ("Konu/Kategori", "20", _CLR["teal"], "\U0001f4ca"),
    ])


def _render_overview():
    styled_section("Kategori Dağılimi", _CLR["blue"])
    for rs in range(0, len(_CATS), 4):
        row = _CATS[rs:rs + 4]
        styled_stat_row([(c[0], "20", c[2], c[1]) for c in row])
    styled_info_banner("Kategori sekmelerine tiklayarak 3D içerikleri kesfet!", "info", "\U0001f3ac")


def _build_periodiç_table_html():
    """118 elementli interaktif periyodik cetvel HTML bileseni."""
    elements_js = json.dumps(
        [[z, sym, name, mass, cat, row, col, info]
         for z, sym, name, mass, cat, row, col, info in _PT_ELEMENTS],
        ensure_ascii=False
    )
    cats_js = json.dumps(_PT_CATS, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:10px 8px}}
.pt-hdr{{text-align:center;padding:8px 0 12px}}
.pt-hdr h2{{font-size:1.2rem;color:#1A2035;margin-bottom:3px}}
.pt-hdr p{{font-size:.75rem;color:#94a3b8}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin-bottom:10px}}
.legend-i{{display:flex;align-items:center;gap:3px;font-size:.6rem;color:#94a3b8}}
.legend-d{{width:9px;height:9px;border-radius:3px}}
.pt-grid{{display:grid;grid-template-columns:repeat(18,1fr);gap:2px;max-width:100%}}
.el{{position:relative;padding:2px 1px;border-radius:4px;cursor:pointer;text-align:center;
  transition:all .15s ease;border:1px solid rgba(255,255,255,.06);min-height:44px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;user-select:none}}
.el:hover{{transform:scale(1.45);z-index:100;box-shadow:0 8px 32px rgba(0,0,0,.6);
  border-color:rgba(255,255,255,.3)}}
.el.sel{{border:2px solid #fbbf24;box-shadow:0 0 12px rgba(251,191,36,.4)}}
.el .z{{font-size:.48rem;opacity:.6;line-height:1}}
.el .sym{{font-size:.82rem;font-weight:800;line-height:1.2}}
.el .nm{{font-size:.38rem;opacity:.7;line-height:1;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;max-width:100%}}
.tt{{display:none;position:fixed;background:linear-gradient(135deg,#1e293b,#334155);
  border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:10px 14px;z-index:1000;
  pointer-events:none;box-shadow:0 10px 40px rgba(0,0,0,.5);min-width:200px}}
.tt.show{{display:block}}
.tt .ts{{font-size:1.4rem;font-weight:800}}
.tt .tn{{font-size:.85rem;font-weight:600;color:#1A2035}}
.tt .tr{{font-size:.72rem;color:#94a3b8;margin-top:2px}}
.sep-l{{font-size:.48rem;color:#64748b;display:flex;align-items:center;justify-content:center;
  white-space:nowrap;border-radius:4px;cursor:default}}
.det{{margin-top:10px;background:linear-gradient(135deg,#1e293b,#334155);border-radius:14px;
  border:1px solid rgba(255,255,255,.08);padding:18px;display:none;
  animation:su .3s ease;position:relative}}
.det.show{{display:block}}
@keyframes su{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.dh{{display:flex;align-items:center;gap:14px;margin-bottom:12px}}
.ds{{width:60px;height:60px;border-radius:14px;display:flex;align-items:center;
  justify-content:center;font-size:1.7rem;font-weight:900;color:#fff}}
.dt h3{{font-size:1.05rem;color:#1A2035}}
.dt p{{font-size:.76rem;color:#94a3b8;margin-top:2px}}
.dg{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}}
.dc{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  border-radius:10px;padding:9px;text-align:center}}
.dc .dl{{font-size:.62rem;color:#64748b;text-transform:uppercase}}
.dc .dv{{font-size:.85rem;font-weight:700;color:#1A2035;margin-top:2px}}
.di{{margin-top:10px;padding:11px 14px;background:rgba(255,255,255,.03);border-radius:10px;
  border:1px solid rgba(255,255,255,.05);font-size:.82rem;color:#cbd5e1;line-height:1.7}}
.cb{{position:absolute;top:10px;right:12px;background:rgba(255,255,255,.08);border:none;
  color:#94a3b8;width:26px;height:26px;border-radius:50%;cursor:pointer;font-size:.9rem;
  display:flex;align-items:center;justify-content:center;transition:all .2s}}
.cb:hover{{background:rgba(239,68,68,.3);color:#f87171}}
</style></head><body>
<div class="pt-hdr"><h2>\U0001f9ea Periyodik Çizelge — 118 Element</h2>
<p>Her elementin uzerine gelin veya tiklayin</p></div>
<div class="legend" id="leg"></div>
<div class="pt-grid" id="ptG"></div>
<div class="det" id="dp"><button class="cb" onclick="cD()">&#10005;</button><div id="dc"></div></div>
<div class="tt" id="tt"></div>
<script>
var E={elements_js};
var CC={cats_js};
var CN={{"Alkali Metal":"Alkali Metal","Toprak Alkali":"Toprak Alkali Metal",
"Gecis Metali":"Gecis Metali","Metal":"Metal","Yarimetal":"Yarimetal","Ametal":"Ametal",
"Halojen":"Halojen","Soy Gaz":"Soy Gaz","Lantanit":"Lantanit","Aktinit":"Aktinit",
"Bilinmeyen":"Bilinmeyen"}};
var lg=document.getElementById("leg");
Object.keys(CC).forEach(function(k){{
  var d=document.createElement("div");d.className="legend-i";
  d.innerHTML='<span class="legend-d" style="background:'+CC[k]+'"></span>'+CN[k];
  lg.appendChild(d)}});
var G=document.getElementById("ptG");
var iL=document.createElement("div");iL.className="sep-l";
iL.style.cssText="grid-row:6;grid-column:3;background:rgba(251,146,60,.12);border:1px dashed rgba(251,146,60,.3)";
iL.textContent="57-71";G.appendChild(iL);
var iA=document.createElement("div");iA.className="sep-l";
iA.style.cssText="grid-row:7;grid-column:3;background:rgba(244,114,182,.12);border:1px dashed rgba(244,114,182,.3)";
iA.textContent="89-103";G.appendChild(iA);
var gp=document.createElement("div");gp.style.cssText="grid-row:8;grid-column:1/-1;height:6px";
G.appendChild(gp);
E.forEach(function(el){{
  var d=document.createElement("div");d.className="el";
  d.style.gridRow=el[5];d.style.gridColumn=el[6];
  var c=CC[el[4]]||"#6b7280";
  d.style.background=c+"18";d.style.borderColor=c+"30";
  d.innerHTML='<span class="z">'+el[0]+'</span><span class="sym" style="color:'+c+'">'+el[1]+'</span><span class="nm">'+el[2]+'</span>';
  d.onmouseenter=function(e){{sT(e,el,c)}};
  d.onmousemove=function(e){{mT(e)}};
  d.onmouseleave=hT;
  d.onclick=function(){{sD(el,c,d)}};
  G.appendChild(d)}});
var tt=document.getElementById("tt");
function sT(e,el,c){{
  tt.innerHTML='<div class="ts" style="color:'+c+'">'+el[1]+'</div>'+
    '<div class="tn">'+el[2]+' ('+el[1]+')</div>'+
    '<div class="tr">Atom No: '+el[0]+' | Kütle: '+el[3]+' amu</div>'+
    '<div class="tr">Kategori: '+(CN[el[4]]||el[4])+'</div>'+
    '<div class="tr" style="margin-top:4px;color:#cbd5e1;font-size:.7rem">'+el[7]+'</div>';
  tt.className="tt show";mT(e)}}
function mT(e){{var x=e.clientX+14,y=e.clientY+14;
  if(x+210>window.innerWidth)x=e.clientX-210;
  if(y+140>window.innerHeight)y=e.clientY-140;
  tt.style.left=x+"px";tt.style.top=y+"px"}}
function hT(){{tt.className="tt"}}
function sD(el,c,dv){{
  var p=document.querySelector(".el.sel");if(p)p.classList.remove("sel");
  dv.classList.add("sel");
  var dp=document.getElementById("dp"),dc=document.getElementById("dc");
  dc.innerHTML='<div class="dh"><div class="ds" style="background:'+c+'">'+el[1]+'</div>'+
    '<div class="dt"><h3>'+el[2]+' ('+el[1]+')</h3><p>Atom Numarasi: '+el[0]+
    ' \\u2022 '+(CN[el[4]]||el[4])+'</p></div></div>'+
    '<div class="dg"><div class="dc"><div class="dl">Atom No</div><div class="dv">'+el[0]+
    '</div></div><div class="dc"><div class="dl">Sembol</div><div class="dv" style="color:'+c+'">'+el[1]+
    '</div></div><div class="dc"><div class="dl">Kütle (amu)</div><div class="dv">'+el[3]+
    '</div></div><div class="dc"><div class="dl">Kategori</div><div class="dv" style="font-size:.7rem">'+
    (CN[el[4]]||el[4])+'</div></div></div>'+
    '<div class="di">\U0001f4a1 '+el[7]+'</div>';
  dp.className="det show";dp.scrollIntoView({{behavior:"smooth",block:"nearest"}})}}
function cD(){{document.getElementById("dp").className="det";
  var p=document.querySelector(".el.sel");if(p)p.classList.remove("sel")}}
</script></body></html>'''


def _render_periodiç_table_category(store, ci):
    """Periyodik Çizelge ozel kategori sayfasi — 118 elementli interaktif tablo."""
    cat_name, emoji, color, _ = _CATS[ci]
    styled_section(f"{emoji} {cat_name} — 118 Element", color)
    styled_info_banner(
        "Elementin uzerine gelerek kısa bilgi gorun, tiklayarak detaylari inceleyin!",
        "info", "\U0001f9ea"
    )
    html = _build_periodiç_table_html()
    components.html(html, height=720, scrolling=True)
    # Sesli anlatim + bilgi kartlari (genel periyodik cetvel)
    _render_anatomy_info(ci, 0, "Periyodik Çizelge", emoji, color)


def _build_turkey_map_html():
    """81 il — Premium 3D interaktif Türkiye haritasi."""
    if not _TR_ILLER:
        return "<html><body><p>Harita verisi yuklenemedi.</p></body></html>"
    iller_js = json.dumps(
        [[p, nm, bl, yz, nf, clr, inf] for p, nm, bl, yz, nf, clr, inf in _TR_ILLER],
        ensure_ascii=False
    )
    detay_js = json.dumps(_TR_DETAY, ensure_ascii=False)
    _IL_POS = {
        1:(491,409),2:(639,352),3:(252,280),4:(878,207),5:(517,137),6:(368,191),
        7:(261,417),8:(816,98),9:(118,345),10:(119,212),11:(225,182),12:(749,269),
        13:(831,304),14:(306,132),15:(240,355),16:(178,171),17:(46,174),18:(406,141),
        19:(473,145),20:(180,351),21:(737,341),22:(53,62),23:(686,284),24:(700,204),
        25:(789,193),26:(251,203),27:(594,405),28:(645,118),29:(699,151),30:(913,366),
        31:(534,453),32:(253,352),33:(457,423),34:(174,111),35:(82,303),36:(880,141),
        37:(414,82),38:(500,280),39:(87,57),40:(434,249),41:(219,123),42:(349,344),
        43:(224,229),44:(641,308),45:(97,289),46:(572,367),47:(762,385),48:(143,392),
        49:(800,280),50:(461,287),51:(459,338),52:(619,113),53:(751,110),54:(245,136),
        55:(542,90),56:(823,340),57:(483,35),58:(576,204),59:(101,111),60:(553,163),
        61:(711,111),62:(703,252),63:(665,396),64:(196,284),65:(894,298),66:(465,203),
        67:(315,77),68:(427,307),69:(737,166),70:(387,395),71:(401,197),72:(782,343),
        73:(848,377),74:(342,64),75:(860,103),76:(928,192),77:(189,137),78:(356,96),
        79:(581,429),80:(538,404),81:(283,123)
    }
    pos_js = json.dumps(_IL_POS, ensure_ascii=False)
    bölge_colors = {
        "Marmara": "#3b82f6", "Ege": "#22c55e", "Akdeniz": "#f97316",
        "İç Anadolu": "#eab308", "Karadeniz": "#10b981",
        "Doğu Anadolu": "#ef4444", "Güneydoğu Anadolu": "#a855f7"
    }
    bölge_js = json.dumps(bölge_colors, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:radial-gradient(ellipse at 30% 20%,#0c1929,#060d19 60%,#030712);color:#e2e8f0;padding:8px;overflow-x:hidden}}
.hdr{{text-align:center;padding:8px 0 10px}}
.hdr h2{{font-size:1.2rem;background:linear-gradient(90deg,#1A2035,#38bdf8,#1A2035);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:3px;font-weight:800;letter-spacing:.5px}}
.hdr p{{font-size:.72rem;color:#64748b}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-bottom:10px}}
.leg-i{{display:flex;align-items:center;gap:4px;font-size:.65rem;color:#94a3b8;cursor:pointer;
  padding:3px 10px;border-radius:20px;border:1px solid rgba(255,255,255,.06);
  background:rgba(255,255,255,.03);transition:all .3s;backdrop-filter:blur(4px)}}
.leg-i:hover{{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.15);transform:translateY(-1px)}}
.leg-d{{width:10px;height:10px;border-radius:50%;box-shadow:0 0 6px currentColor}}
.search-bar{{display:flex;gap:8px;margin-bottom:10px;justify-content:center}}
.search-bar input{{padding:8px 18px;border-radius:24px;border:1px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.04);color:#e2e8f0;font-size:.8rem;width:260px;outline:none;
  backdrop-filter:blur(8px);transition:all .3s}}
.search-bar input:focus{{border-color:rgba(56,189,248,.4);box-shadow:0 0 20px rgba(56,189,248,.1);background:rgba(255,255,255,.06)}}
.scene{{perspective:1200px;width:100%;margin-bottom:8px}}
.map3d{{position:relative;width:100%;aspect-ratio:2/1;
  transform:rotateX(25deg) rotateZ(-2deg);transform-style:preserve-3d;
  transition:transform .6s cubic-bezier(.23,1,.32,1);border-radius:18px;overflow:visible}}
.map3d:hover{{transform:rotateX(18deg) rotateZ(0deg)}}
.map-base{{position:absolute;inset:0;border-radius:18px;overflow:hidden}}
.map-base svg{{width:100%;height:100%;display:block}}
/* 3D kara katmani */
.land-layer{{position:absolute;inset:0;border-radius:18px;overflow:hidden;
  background:linear-gradient(180deg,
    rgba(21,94,56,.12) 0%,
    rgba(34,120,60,.08) 30%,
    rgba(139,90,43,.06) 60%,
    rgba(180,120,50,.04) 100%);
  box-shadow:
    0 4px 0 rgba(0,0,0,.3),
    0 8px 0 rgba(0,0,0,.2),
    0 12px 0 rgba(0,0,0,.15),
    0 16px 0 rgba(0,0,0,.1),
    0 20px 40px rgba(0,0,0,.5);
  transform:translateZ(0px)}}
.land-top{{position:absolute;inset:0;border-radius:18px;overflow:hidden;
  transform:translateZ(12px);
  box-shadow:inset 0 -2px 20px rgba(0,0,0,.2),inset 0 2px 20px rgba(255,255,255,.03)}}
/* Deniz */
.sea-layer{{position:absolute;inset:-20px;border-radius:22px;z-index:-1;
  background:radial-gradient(ellipse at 50% 50%,
    rgba(14,55,90,.6) 0%,
    rgba(8,38,68,.8) 40%,
    rgba(3,20,45,.9) 70%,
    rgba(2,12,30,1) 100%);
  transform:translateZ(-8px);
  box-shadow:0 30px 80px rgba(0,0,0,.6)}}
.sea-anim{{position:absolute;inset:0;border-radius:22px;overflow:hidden;opacity:.15}}
.sea-anim::before{{content:"";position:absolute;inset:-50%;
  background:repeating-linear-gradient(45deg,transparent,transparent 8px,rgba(56,189,248,.08) 8px,rgba(56,189,248,.08) 16px);
  animation:seaWave 12s linear infinite}}
@keyframes seaWave{{from{{transform:translate(0,0)}}to{{transform:translate(24px,24px)}}}}
/* Il isaretcileri */
.il-pin{{cursor:pointer;transition:all .25s cubic-bezier(.23,1,.32,1)}}
.il-pin:hover{{filter:brightness(1.5) drop-shadow(0 0 8px currentColor);transform:scale(1.3)}}
.il-lbl{{font-size:3px;fill:#1A2035;pointer-events:none;text-anchor:middle;
  font-weight:700;text-shadow:0 0 4px rgba(0,0,0,.9),0 1px 2px rgba(0,0,0,.8);letter-spacing:.2px}}
/* Tooltip */
.tt{{display:none;position:fixed;background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(30,41,59,.95));
  border:1px solid rgba(56,189,248,.2);border-radius:14px;padding:12px 16px;z-index:1000;
  pointer-events:none;box-shadow:0 20px 60px rgba(0,0,0,.6),0 0 30px rgba(56,189,248,.08);
  min-width:240px;max-width:340px;backdrop-filter:blur(20px)}}
.tt.show{{display:block}}
.tt .tn{{font-size:.95rem;font-weight:800;color:#1A2035;margin-bottom:5px;letter-spacing:.3px}}
.tt .tr{{font-size:.74rem;color:#94a3b8;margin-top:2px;line-height:1.6}}
.tt .tb{{display:inline-block;padding:2px 8px;border-radius:6px;font-size:.65rem;font-weight:600;margin-bottom:4px}}
/* Detay paneli */
.det{{margin-top:8px;background:linear-gradient(135deg,rgba(15,23,42,.98),rgba(30,41,59,.95));
  border-radius:16px;border:1px solid rgba(255,255,255,.08);padding:18px;display:none;
  animation:su .4s cubic-bezier(.23,1,.32,1);position:relative;max-height:420px;overflow-y:auto;
  backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,.4)}}
.det::-webkit-scrollbar{{width:4px}}.det::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.12);border-radius:4px}}
.det.show{{display:block}}
@keyframes su{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.dh{{display:flex;align-items:center;gap:14px;margin-bottom:14px}}
.d-badge{{width:56px;height:56px;border-radius:14px;display:flex;align-items:center;
  justify-content:center;font-size:1.3rem;font-weight:900;color:#fff;
  box-shadow:0 4px 15px rgba(0,0,0,.3)}}
.d-title h3{{font-size:1.1rem;color:#1A2035;font-weight:800}}
.d-title p{{font-size:.76rem;color:#94a3b8;margin-top:3px}}
.d-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}}
.d-card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:10px;text-align:center;transition:all .2s}}
.d-card:hover{{background:rgba(255,255,255,.07);transform:translateY(-1px)}}
.d-card .dl{{font-size:.58rem;color:#64748b;text-transform:uppercase;letter-spacing:.8px}}
.d-card .dv{{font-size:.85rem;font-weight:700;color:#1A2035;margin-top:3px}}
.d-sec{{margin-top:10px}}.d-sec h4{{font-size:.8rem;font-weight:700;margin-bottom:6px;
  display:flex;align-items:center;gap:4px}}
.d-tags{{display:flex;flex-wrap:wrap;gap:5px}}
.d-tag{{padding:4px 10px;border-radius:8px;font-size:.7rem;font-weight:500;
  transition:all .2s;cursor:default}}
.d-tag:hover{{transform:translateY(-1px)}}
.d-tag.dflt{{background:rgba(139,92,246,.1);color:#c4b5fd;border:1px solid rgba(139,92,246,.15)}}
.d-tag.food{{background:rgba(249,115,22,.1);color:#fb923c;border:1px solid rgba(249,115,22,.12)}}
.d-tag.agri{{background:rgba(34,197,94,.1);color:#4ade80;border:1px solid rgba(34,197,94,.12)}}
.d-tag.hist{{background:rgba(234,179,8,.1);color:#facc15;border:1px solid rgba(234,179,8,.12)}}
.d-info{{margin-top:8px;padding:12px 14px;background:rgba(255,255,255,.03);border-radius:12px;
  border:1px solid rgba(255,255,255,.05);font-size:.78rem;color:#cbd5e1;line-height:1.7}}
.cb{{position:absolute;top:12px;right:14px;background:rgba(255,255,255,.06);border:none;
  color:#94a3b8;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:.9rem;
  display:flex;align-items:center;justify-content:center;transition:all .2s;backdrop-filter:blur(4px)}}
.cb:hover{{background:rgba(239,68,68,.25);color:#f87171}}
</style></head><body>
<div class="hdr"><h2>\U0001f1f9\U0001f1f7 Türkiye Cumhuriyeti \u2014 81 Il Interaktif Haritasi</h2>
<p>3D haritada illere tiklayin \u2022 Fare ile bakis acisini degistirin \u2022 Arama yapin</p></div>
<div class="legend" id="leg"></div>
<div class="search-bar"><input type="text" id="sBox" placeholder="\U0001f50d Il ara... (Istanbul, 34, Karadeniz)" oninput="filterIl(this.value)"></div>
<div class="scene" id="scn">
  <div class="map3d" id="m3d">
    <div class="sea-layer"><div class="sea-anim"></div></div>
    <div class="land-layer"></div>
    <div class="land-top">
      <div class="map-base">
        <svg id="mapSvg" viewBox="0 0 1000 520" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>
              <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            <filter id="shadow"><feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000" flood-opacity=".5"/></filter>
            <radialGradient id="pinG" cx="50%" cy="30%"><stop offset="0%" stop-color="rgba(255,255,255,.3)"/>
              <stop offset="100%" stop-color="rgba(255,255,255,0)"/></radialGradient>
            <linearGradient id="landG" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#1a5c3a" stop-opacity=".35"/>
              <stop offset="30%" stop-color="#2d7a4a" stop-opacity=".25"/>
              <stop offset="60%" stop-color="#8B6914" stop-opacity=".18"/>
              <stop offset="100%" stop-color="#a67c52" stop-opacity=".12"/>
            </linearGradient>
          </defs>
          <!-- Türkiye sinir polygonu -->
          <path id="trBorder" d="M18,173 L53,62 L87,57 L101,111 L174,111 L189,137 L219,123 L283,123 L306,132 L315,77 L342,64 L356,96 L414,82 L483,35 L542,90 L619,113 L645,118 L699,151 L711,111 L751,110 L782,124 L816,98 L860,103 L880,141 L928,192 L940,208 L940,372 L913,366 L848,377 L823,340 L762,385 L677,418 L665,396 L581,429 L594,405 L572,367 L538,404 L534,453 L491,409 L457,423 L367,478 L254,444 L219,468 L181,442 L143,392 L118,345 L97,289 L82,303 L35,303 L28,198 L18,173Z"
            fill="url(#landG)" stroke="rgba(255,255,255,.18)" stroke-width="1.5" stroke-linejoin="round" filter="url(#shadow)"/>
          <!-- Bölgeler için gradient alan -->
          <path d="M18,173 L53,62 L87,57 L101,111 L174,111 L189,137 L225,182 L178,171 L119,212 L82,303 L35,303 L28,198 L18,173Z"
            fill="rgba(59,130,246,.06)" stroke="none"/>
          <!-- Istanbul Boğazı -->
          <path d="M176,88 Q180,98 178,108 Q175,115 177,122" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity=".6">
            <animate attributeName="opacity" values=".4;.8;.4" dur="3s" repeatCount="indefinite"/></path>
          <text x="193" y="107" fill="#38bdf8" font-size="5.5" font-weight="700" opacity=".7">Istanbul Boğazı</text>
          <!-- Çanakkale Boğazı -->
          <path d="M55,155 Q50,163 46,172 Q40,180 35,190" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity=".6">
            <animate attributeName="opacity" values=".4;.8;.4" dur="3s" repeatCount="indefinite" begin="1.5s"/></path>
          <text x="62" y="175" fill="#38bdf8" font-size="5.5" font-weight="700" opacity=".7">Çanakkale Bog.</text>
          <!-- Deniz isimleri -->
          <text x="480" y="22" fill="rgba(56,189,248,.2)" font-size="16" font-weight="800" text-anchor="middle" letter-spacing="8">KARADENIZ</text>
          <text x="200" y="125" fill="rgba(56,189,248,.12)" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="3">MARMARA</text>
          <text x="25" y="350" fill="rgba(56,189,248,.15)" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="4" transform="rotate(-90,25,350)">EGE</text>
          <text x="420" y="512" fill="rgba(56,189,248,.2)" font-size="16" font-weight="800" text-anchor="middle" letter-spacing="8">AKDENIZ</text>
        </svg>
      </div>
    </div>
  </div>
</div>
<div class="det" id="dp"><button class="cb" onclick="cD()">&#10005;</button><div id="dc"></div></div>
<div class="tt" id="tt"></div>
<script>
var IL={iller_js};
var DT={detay_js};
var POS={pos_js};
var BC={bölge_js};
var svg=document.getElementById("mapSvg");
var leg=document.getElementById("leg");
var m3d=document.getElementById("m3d");
var scn=document.getElementById("scn");
// 3D fare takibi
scn.addEventListener("mousemove",function(e){{
  var r=scn.getBoundingClientRect();
  var mx=(e.clientX-r.left)/r.width-.5;
  var my=(e.clientY-r.top)/r.height-.5;
  m3d.style.transform="rotateX("+(25-my*12)+"deg) rotateZ("+(-2+mx*6)+"deg)";
}});
scn.addEventListener("mouseleave",function(){{
  m3d.style.transform="rotateX(25deg) rotateZ(-2deg)";
}});
// Bölge->plaka eslemesi
var BOLGE_PLAKA={{
  "Marmara":[11,16,17,22,34,39,41,54,59,67,74,77,78,81,10],
  "Ege":[3,9,20,35,43,45,48,64],
  "Akdeniz":[7,15,31,32,33,46,70,80],
  "İç Anadolu":[6,18,26,38,40,42,50,51,58,66,68,71],
  "Karadeniz":[5,8,14,19,28,29,37,52,53,55,57,60,61,69],
  "Doğu Anadolu":[4,12,13,23,24,25,30,36,49,62,65,75,76],
  "Güneydoğu Anadolu":[2,21,27,44,47,56,63,72,73,79]
}};
function getBölge(plk){{for(var b in BOLGE_PLAKA)if(BOLGE_PLAKA[b].indexOf(plk)>=0)return b;return""}}
// Il sinirlarini GeoJSON'dan ciz
function projX(lon){{return(lon-25.5)*50}}
function projY(lat){{return(42.5-lat)*74.3}}
function drawProvinceBorders(){{
  fetch("https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json")
  .then(function(r){{return r.json()}})
  .then(function(geo){{
    var grp=document.createElementNS("http://www.w3.org/2000/svg","g");
    grp.setAttribute("id","borders");
    // GeoJSON adi -> plaka dogrudan esleme tablosu
    var GN={{"Adana":1,"Ad\u0131yaman":2,"Afyon":3,"A\u011fr\u0131":4,"Amasya":5,"Ankara":6,
      "Antalya":7,"Artvin":8,"Ayd\u0131n":9,"Bal\u0131kesir":10,"Bilecik":11,
      "Bing\u00f6l":12,"Bitlis":13,"Bolu":14,"Burdur":15,"Bursa":16,
      "\u00c7anakkale":17,"\u00c7ank\u0131r\u0131":18,"\u00c7orum":19,"Denizli":20,
      "Diyarbak\u0131r":21,"Edirne":22,"Elaz\u0131\u011f":23,"Erzincan":24,
      "Erzurum":25,"Eski\u015fehir":26,"Gaziantep":27,"Giresun":28,
      "G\u00fcm\u00fc\u015fhane":29,"Hakkari":30,"Hatay":31,"Isparta":32,
      "Mersin":33,"\u0130stanbul":34,"\u0130zmir":35,"Kars":36,"Kastamonu":37,
      "Kayseri":38,"K\u0131rklareli":39,"K\u0131r\u015fehir":40,"Kocaeli":41,
      "Konya":42,"K\u00fctahya":43,"Malatya":44,"Manisa":45,
      "Kahramanmara\u015f":46,"Mardin":47,"Mu\u011fla":48,"Mu\u015f":49,
      "Nev\u015fehir":50,"Ni\u011fde":51,"Ordu":52,"Rize":53,"Sakarya":54,
      "Samsun":55,"Siirt":56,"Sinop":57,"Sivas":58,"Tekirda\u011f":59,
      "Tokat":60,"Trabzon":61,"Tunceli":62,"\u015eanl\u0131urfa":63,
      "U\u015fak":64,"Van":65,"Yozgat":66,"Zonguldak":67,"Aksaray":68,
      "Bayburt":69,"Karaman":70,"K\u0131r\u0131kkale":71,"Batman":72,
      "\u015e\u0131rnak":73,"Bart\u0131n":74,"Ardahan":75,"I\u011fd\u0131r":76,
      "Yalova":77,"Karab\u00fck":78,"Kilis":79,"Osmaniye":80,"D\u00fczce":81}};
    function findIl(name){{
      var plk=GN[name]||GN[name.trim()]||0;
      if(!plk)return null;
      return IL.find(function(x){{return x[0]===plk}})||null;
    }}
    geo.features.forEach(function(feat){{
      var geoName=feat.properties.name||"";
      var il=findIl(geoName);
      var plk=il?il[0]:0;
      var clr=il?il[5]:"#475569";
      var bölge=il?il[2]:"";
      function coordsToPath(coords){{
        return coords.map(function(ring){{
          return "M"+ring.map(function(c){{return projX(c[0]).toFixed(1)+","+projY(c[1]).toFixed(1)}}).join("L")+"Z";
        }}).join(" ");
      }}
      var d="";
      if(feat.geometry.type==="Polygon"){{d=coordsToPath(feat.geometry.coordinates)}}
      else if(feat.geometry.type==="MultiPolygon"){{
        feat.geometry.coordinates.forEach(function(poly){{d+=coordsToPath(poly)+" "}})
      }}
      if(!d)return;
      var path=document.createElementNS("http://www.w3.org/2000/svg","path");
      path.setAttribute("d",d);
      path.setAttribute("fill",clr+"18");
      path.setAttribute("stroke",clr+"60");
      path.setAttribute("stroke-width","0.6");
      path.setAttribute("stroke-linejoin","round");
      path.setAttribute("data-plaka",plk);
      path.setAttribute("class","il-border");
      path.style.transition="all .25s";
      path.style.cursor="pointer";
      path.onmouseenter=function(e){{
        path.setAttribute("fill",clr+"35");
        path.setAttribute("stroke",clr);
        path.setAttribute("stroke-width","1.2");
        if(il)sT(e,il);
      }};
      path.onmousemove=function(e){{mT(e)}};
      path.onmouseleave=function(){{
        path.setAttribute("fill",clr+"18");
        path.setAttribute("stroke",clr+"60");
        path.setAttribute("stroke-width","0.6");
        hT();
      }};
      path.onclick=function(){{if(il)sD(il)}};
      grp.appendChild(path);
    }});
    // Sinir grubunu pin'lerin altına ekle
    var firstPin=svg.querySelector(".il-pin");
    if(firstPin)svg.insertBefore(grp,firstPin);
    else svg.appendChild(grp);
    // Eski statik border'i gizle
    var old=document.getElementById("trBorder");
    if(old)old.setAttribute("fill-opacity","0");
  }})
  .catch(function(err){{console.log("GeoJSON yuklenemedi:",err)}});
}}
drawProvinceBorders();
// Legend
var seenB={{}};
IL.forEach(function(il){{if(!seenB[il[2]]){{seenB[il[2]]=1;
  var d=document.createElement("div");d.className="leg-i";
  d.innerHTML='<span class="leg-d" style="background:'+il[5]+';box-shadow:0 0 6px '+il[5]+'"></span>'+il[2];
  leg.appendChild(d)}}}});
// Il isaretcileri
IL.forEach(function(il){{
  var p=il[0],nm=il[1],clr=il[5];
  var pos=POS[String(p)];if(!pos)return;
  var cx=pos[0],cy=pos[1];
  var g=document.createElementNS("http://www.w3.org/2000/svg","g");
  g.setAttribute("class","il-pin");g.setAttribute("data-plaka",p);
  g.style.color=clr;
  // Glow halkasi
  var c0=document.createElementNS("http://www.w3.org/2000/svg","circle");
  c0.setAttribute("cx",cx);c0.setAttribute("cy",cy);c0.setAttribute("r","9");
  c0.setAttribute("fill","none");c0.setAttribute("stroke",clr);c0.setAttribute("stroke-width","0.5");
  c0.setAttribute("stroke-opacity","0.2");
  // Dis daire
  var c1=document.createElementNS("http://www.w3.org/2000/svg","circle");
  c1.setAttribute("cx",cx);c1.setAttribute("cy",cy);c1.setAttribute("r","6");
  c1.setAttribute("fill",clr);c1.setAttribute("fill-opacity","0.15");
  c1.setAttribute("stroke",clr);c1.setAttribute("stroke-width","1");c1.setAttribute("stroke-opacity","0.5");
  // Ic nokta (3D parlak)
  var c2=document.createElementNS("http://www.w3.org/2000/svg","circle");
  c2.setAttribute("cx",cx);c2.setAttribute("cy",cy);c2.setAttribute("r","3");
  c2.setAttribute("fill",clr);
  // Parlaklik
  var c3=document.createElementNS("http://www.w3.org/2000/svg","circle");
  c3.setAttribute("cx",cx-0.8);c3.setAttribute("cy",cy-0.8);c3.setAttribute("r","1.2");
  c3.setAttribute("fill","rgba(255,255,255,.35)");
  // Il etiketi
  var txt=document.createElementNS("http://www.w3.org/2000/svg","text");
  txt.setAttribute("x",cx);txt.setAttribute("y",cy-10);txt.setAttribute("class","il-lbl");
  txt.textContent=nm;
  g.appendChild(c0);g.appendChild(c1);g.appendChild(c2);g.appendChild(c3);g.appendChild(txt);
  g.onmouseenter=function(e){{sT(e,il)}};
  g.onmousemove=function(e){{mT(e)}};
  g.onmouseleave=hT;
  g.onclick=function(){{sD(il)}};
  svg.appendChild(g);
}});
// Tooltip
var tt=document.getElementById("tt");
function sT(e,il){{
  var nf=il[4]>1000000?(il[4]/1000000).toFixed(1)+"M":il[4]>1000?(il[4]/1000).toFixed(0)+"K":il[4];
  tt.innerHTML='<div class="tn">\U0001f4cd '+il[0]+' \u2014 '+il[1]+'</div>'+
    '<div class="tb" style="background:'+il[5]+'18;color:'+il[5]+';border:1px solid '+il[5]+'30">'+il[2]+' Bölgesi</div>'+
    '<div class="tr">\U0001f4cf Yüzölçümü: '+il[3].toLocaleString("tr-TR")+' km\u00b2</div>'+
    '<div class="tr">\U0001f465 Nüfus: '+il[4].toLocaleString("tr-TR")+'</div>'+
    '<div class="tr" style="margin-top:4px;color:#cbd5e1;font-size:.72rem;border-top:1px solid rgba(255,255,255,.06);padding-top:4px">'+il[6]+'</div>';
  tt.className="tt show";mT(e)}}
function mT(e){{var x=e.clientX+16,y=e.clientY+16;
  if(x+260>window.innerWidth)x=e.clientX-260;
  if(y+170>window.innerHeight)y=e.clientY-170;
  tt.style.left=x+"px";tt.style.top=y+"px"}}
function hT(){{tt.className="tt"}}
// Detay paneli
function sD(il){{
  var p=il[0],nm=il[1],clr=il[5];
  var dt=DT[String(p)]||{{}};
  var dp=document.getElementById("dp"),dc=document.getElementById("dc");
  var nf=il[4].toLocaleString("tr-TR");
  var yz=il[3].toLocaleString("tr-TR");
  // Secili ili vurgula
  document.querySelectorAll(".il-pin").forEach(function(g){{
    g.style.filter="";g.style.transform="";
  }});
  var sel=document.querySelector('.il-pin[data-plaka="'+p+'"]');
  if(sel){{sel.style.filter="brightness(1.5) drop-shadow(0 0 10px "+clr+")";sel.style.transform="scale(1.4)"}}
  var h='<div class="dh"><div class="d-badge" style="background:linear-gradient(135deg,'+clr+','+clr+'88)">'+p+'</div>'+
    '<div class="d-title"><h3>'+nm+'</h3><p style="color:'+clr+'">'+il[2]+' Bölgesi</p></div></div>'+
    '<div class="d-grid">'+
    '<div class="d-card"><div class="dl">\U0001f3f7\ufe0f Plaka</div><div class="dv">'+p+'</div></div>'+
    '<div class="d-card"><div class="dl">\U0001f465 Nüfus</div><div class="dv">'+nf+'</div></div>'+
    '<div class="d-card"><div class="dl">\U0001f4cf Yüzölçümü</div><div class="dv">'+yz+' km\u00b2</div></div></div>';
  if(dt.göller&&dt.göller.length){{
    h+='<div class="d-sec"><h4 style="color:#38bdf8">\U0001f4a7 Göller ve Su Kaynaklari</h4><div class="d-tags">';
    dt.göller.forEach(function(g){{h+='<span class="d-tag dflt">'+g+'</span>'}});h+='</div></div>'}}
  if(dt.meşhur_yemekler&&dt.meşhur_yemekler.length){{
    h+='<div class="d-sec"><h4 style="color:#fb923c">\U0001f35c Meşhur Yemekler</h4><div class="d-tags">';
    dt.meşhur_yemekler.forEach(function(y){{h+='<span class="d-tag food">'+y+'</span>'}});h+='</div></div>'}}
  if(dt.tarım_ürünleri&&dt.tarım_ürünleri.length){{
    h+='<div class="d-sec"><h4 style="color:#4ade80">\U0001f33e Tarım Ürünleri</h4><div class="d-tags">';
    dt.tarım_ürünleri.forEach(function(t){{h+='<span class="d-tag agri">'+t+'</span>'}});h+='</div></div>'}}
  if(dt.tarihi_yerler&&dt.tarihi_yerler.length){{
    h+='<div class="d-sec"><h4 style="color:#facc15">\U0001f3db\ufe0f Tarihi Yerler</h4><div class="d-tags">';
    dt.tarihi_yerler.forEach(function(t){{h+='<span class="d-tag hist">'+t+'</span>'}});h+='</div></div>'}}
  if(dt.gurme)h+='<div class="d-info">\U0001f374 <b>Gurme:</b> '+dt.gurme+'</div>';
  if(dt.özellikler)h+='<div class="d-info">\U0001f4a1 <b>Özellik:</b> '+dt.özellikler+'</div>';
  dc.innerHTML=h;dp.className="det show";
  dp.scrollIntoView({{behavior:"smooth",block:"nearest"}})}}
function cD(){{document.getElementById("dp").className="det";
  document.querySelectorAll(".il-pin").forEach(function(g){{g.style.filter="";g.style.transform=""}})}}
function filterIl(q){{
  q=q.toLowerCase().replace(/\u0131/g,"i").replace(/\u00fc/g,"u").replace(/\u00f6/g,"o").replace(/\u015f/g,"s").replace(/\u00e7/g,"c").replace(/\u011f/g,"g");
  document.querySelectorAll(".il-pin").forEach(function(g){{
    var p=g.getAttribute("data-plaka");
    var il=IL.find(function(x){{return String(x[0])===p}});
    if(!il)return;
    var nm=il[1].toLowerCase();
    var match=!q||nm.indexOf(q)>=0||String(il[0])===q||il[2].toLowerCase().indexOf(q)>=0;
    g.style.opacity=match?"1":"0.08";
  }});
  // Sinir polygon'larini da filtrele
  document.querySelectorAll(".il-border").forEach(function(b){{
    var p=parseInt(b.getAttribute("data-plaka"));
    var il=IL.find(function(x){{return x[0]===p}});
    if(!il)return;
    var nm=il[1].toLowerCase();
    var match=!q||nm.indexOf(q)>=0||String(il[0])===q||il[2].toLowerCase().indexOf(q)>=0;
    b.style.opacity=match?"1":"0.06";
  }})}}
</script></body></html>'''


def _render_turkey_map_category(store, ci):
    """Türkiye İller Haritası ozel kategori sayfasi — 81 il interaktif harita."""
    cat_name, emoji, color, _ = _CATS[ci]
    styled_section(f"{emoji} {cat_name} — 81 Il", color)
    styled_info_banner(
        "Haritada illere tiklayin veya arama cubugunu kullanin!",
        "info", "\U0001f1f9\U0001f1f7"
    )
    html = _build_turkey_map_html()
    components.html(html, height=780, scrolling=True)
    # Sesli anlatim + bilgi kartlari (genel Türkiye bilgisi)
    _render_anatomy_info(ci, 0, "Türkiye İller Haritası", emoji, color)


def _build_turkey_geography_map_html():
    """Türkiye fiziki coğrafya haritasi — Premium 3D, GeoJSON sinirlar, dağlar, nehirler vb."""
    if not _COG_FEAT:
        return "<html><body><p>Coğrafya verisi yuklenemedi.</p></body></html>"
    features_js = json.dumps(
        [[f[0], f[1], f[2], f[3], f[4], f[5]] for f in _COG_FEAT],
        ensure_ascii=False
    )
    cats_js = json.dumps(_COG_CATS, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:radial-gradient(ellipse at 30% 20%,#0c1929,#060d19 60%,#030712);color:#e2e8f0;padding:8px;overflow-x:hidden}}
.hdr{{text-align:center;padding:8px 0 10px}}
.hdr h2{{font-size:1.2rem;background:linear-gradient(90deg,#4ade80,#38bdf8,#a78bfa);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:3px;font-weight:800;letter-spacing:.5px}}
.hdr p{{font-size:.72rem;color:#64748b}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;margin-bottom:8px}}
.leg-i{{display:flex;align-items:center;gap:4px;font-size:.63rem;color:#94a3b8;cursor:pointer;
  padding:3px 10px;border-radius:20px;border:1px solid rgba(255,255,255,.06);
  background:rgba(255,255,255,.03);transition:all .3s;backdrop-filter:blur(4px)}}
.leg-i:hover{{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.15);transform:translateY(-1px)}}
.leg-i.active{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25);box-shadow:0 0 12px rgba(255,255,255,.06)}}
.leg-d{{width:10px;height:10px;border-radius:50%;box-shadow:0 0 6px currentColor}}
.search-bar{{display:flex;gap:8px;margin-bottom:10px;justify-content:center}}
.search-bar input{{padding:8px 18px;border-radius:24px;border:1px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.04);color:#e2e8f0;font-size:.8rem;width:280px;outline:none;
  backdrop-filter:blur(8px);transition:all .3s}}
.search-bar input:focus{{border-color:rgba(74,222,128,.4);box-shadow:0 0 20px rgba(74,222,128,.1);background:rgba(255,255,255,.06)}}
.scene{{perspective:1200px;width:100%;margin-bottom:8px}}
.map3d{{position:relative;width:100%;aspect-ratio:2/1;
  transform:rotateX(25deg) rotateZ(-2deg);transform-style:preserve-3d;
  transition:transform .6s cubic-bezier(.23,1,.32,1);border-radius:18px;overflow:visible}}
.map3d:hover{{transform:rotateX(18deg) rotateZ(0deg)}}
.map-base{{position:absolute;inset:0;border-radius:18px;overflow:hidden}}
.map-base svg{{width:100%;height:100%;display:block}}
.land-layer{{position:absolute;inset:0;border-radius:18px;overflow:hidden;
  background:linear-gradient(180deg,
    rgba(16,70,45,.18) 0%,
    rgba(28,100,55,.12) 25%,
    rgba(120,80,35,.08) 55%,
    rgba(160,110,45,.06) 100%);
  box-shadow:
    0 4px 0 rgba(0,0,0,.3),
    0 8px 0 rgba(0,0,0,.2),
    0 12px 0 rgba(0,0,0,.15),
    0 16px 0 rgba(0,0,0,.1),
    0 20px 40px rgba(0,0,0,.5);
  transform:translateZ(0px)}}
.land-top{{position:absolute;inset:0;border-radius:18px;overflow:hidden;
  transform:translateZ(12px);
  box-shadow:inset 0 -2px 20px rgba(0,0,0,.2),inset 0 2px 20px rgba(255,255,255,.03)}}
.sea-layer{{position:absolute;inset:-20px;border-radius:22px;z-index:-1;
  background:radial-gradient(ellipse at 50% 50%,
    rgba(8,50,82,.6) 0%,
    rgba(5,32,60,.8) 40%,
    rgba(3,18,40,.9) 70%,
    rgba(2,10,28,1) 100%);
  transform:translateZ(-8px);
  box-shadow:0 30px 80px rgba(0,0,0,.6)}}
.sea-anim{{position:absolute;inset:0;border-radius:22px;overflow:hidden;opacity:.15}}
.sea-anim::before{{content:"";position:absolute;inset:-50%;
  background:repeating-linear-gradient(45deg,transparent,transparent 8px,rgba(56,189,248,.08) 8px,rgba(56,189,248,.08) 16px);
  animation:seaWave 12s linear infinite}}
@keyframes seaWave{{from{{transform:translate(0,0)}}to{{transform:translate(24px,24px)}}}}
.geo-dot{{cursor:pointer;transition:filter .3s ease, opacity .3s ease}}
.geo-dot:hover{{filter:brightness(1.5) drop-shadow(0 0 8px currentColor)}}
.geo-dot.selected{{filter:brightness(1.6) drop-shadow(0 0 12px currentColor)}}
.geo-label{{font-size:3.2px;fill:#1A2035;pointer-events:none;text-anchor:middle;
  font-weight:700;text-shadow:0 0 4px rgba(0,0,0,.9),0 1px 2px rgba(0,0,0,.8);letter-spacing:.2px}}
.tt{{display:none;position:fixed;background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(30,41,59,.95));
  border:1px solid rgba(74,222,128,.2);border-radius:14px;padding:12px 16px;z-index:1000;
  pointer-events:none;box-shadow:0 20px 60px rgba(0,0,0,.6),0 0 30px rgba(74,222,128,.08);
  min-width:240px;max-width:360px;backdrop-filter:blur(20px)}}
.tt.show{{display:block}}
.tt .tn{{font-size:.95rem;font-weight:800;color:#1A2035;margin-bottom:5px;letter-spacing:.3px}}
.tt .tc{{display:inline-block;padding:2px 8px;border-radius:6px;font-size:.65rem;font-weight:600;margin-bottom:4px}}
.tt .tr{{font-size:.74rem;color:#94a3b8;margin-top:2px;line-height:1.6}}
.det{{margin-top:8px;background:linear-gradient(135deg,rgba(15,23,42,.98),rgba(30,41,59,.95));
  border-radius:16px;border:1px solid rgba(255,255,255,.08);padding:18px;display:none;
  animation:su .4s cubic-bezier(.23,1,.32,1);position:relative;max-height:450px;overflow-y:auto;
  backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,.4)}}
.det::-webkit-scrollbar{{width:4px}}.det::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.12);border-radius:4px}}
.det.show{{display:block}}
@keyframes su{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.dh{{display:flex;align-items:center;gap:14px;margin-bottom:14px}}
.d-badge{{width:56px;height:56px;border-radius:14px;display:flex;align-items:center;
  justify-content:center;font-size:1.5rem;box-shadow:0 4px 15px rgba(0,0,0,.3)}}
.d-title h3{{font-size:1.1rem;color:#1A2035;font-weight:800}}
.d-title p{{font-size:.76rem;color:#94a3b8;margin-top:3px}}
.d-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:12px 0}}
.d-card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:10px;text-align:center;transition:all .2s}}
.d-card:hover{{background:rgba(255,255,255,.07);transform:translateY(-1px)}}
.d-card .dl{{font-size:.58rem;color:#64748b;text-transform:uppercase;letter-spacing:.8px}}
.d-card .dv{{font-size:.85rem;font-weight:700;color:#1A2035;margin-top:3px}}
.d-info{{margin-top:10px;padding:12px 14px;background:rgba(255,255,255,.03);border-radius:12px;
  border:1px solid rgba(255,255,255,.05);font-size:.78rem;color:#cbd5e1;line-height:1.7}}
.d-feat{{margin-top:8px;padding:8px 12px;background:rgba(139,92,246,.08);border-radius:10px;
  border:1px solid rgba(139,92,246,.12);font-size:.76rem;color:#c4b5fd}}
.cb{{position:absolute;top:12px;right:14px;background:rgba(255,255,255,.06);border:none;
  color:#94a3b8;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:.9rem;
  display:flex;align-items:center;justify-content:center;transition:all .2s;backdrop-filter:blur(4px)}}
.cb:hover{{background:rgba(239,68,68,.25);color:#f87171}}
.prov-border{{transition:all .25s;cursor:default}}
</style></head><body>
<div class="hdr"><h2>\U0001f3d4\ufe0f Türkiye Fiziki Coğrafya Haritasi</h2>
<p>3D haritada coğrafi ogelere tiklayin \u2022 Fare ile bakis acisini degistirin \u2022 Kategorilere tiklayarak filtreleyin</p></div>
<div class="legend" id="leg"></div>
<div class="search-bar"><input type="text" id="sBox" placeholder="\U0001f50d Ara... (Agri Dağı, Van Gölü, Firat Nehri)" oninput="filterF(this.value)"></div>
<div class="scene" id="scn">
  <div class="map3d" id="m3d">
    <div class="sea-layer"><div class="sea-anim"></div></div>
    <div class="land-layer"></div>
    <div class="land-top">
      <div class="map-base">
        <svg id="mapSvg" viewBox="0 0 1000 520" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>
              <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            <filter id="shadow"><feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000" flood-opacity=".5"/></filter>
            <linearGradient id="landG" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#1a5c3a" stop-opacity=".35"/>
              <stop offset="30%" stop-color="#2d7a4a" stop-opacity=".25"/>
              <stop offset="60%" stop-color="#8B6914" stop-opacity=".18"/>
              <stop offset="100%" stop-color="#a67c52" stop-opacity=".12"/>
            </linearGradient>
          </defs>
          <!-- Türkiye sinir polygonu -->
          <path id="trBorder" d="M18,173 L53,62 L87,57 L101,111 L174,111 L189,137 L219,123 L283,123 L306,132 L315,77 L342,64 L356,96 L414,82 L483,35 L542,90 L619,113 L645,118 L699,151 L711,111 L751,110 L782,124 L816,98 L860,103 L880,141 L928,192 L940,208 L940,372 L913,366 L848,377 L823,340 L762,385 L677,418 L665,396 L581,429 L594,405 L572,367 L538,404 L534,453 L491,409 L457,423 L367,478 L254,444 L219,468 L181,442 L143,392 L118,345 L97,289 L82,303 L35,303 L28,198 L18,173Z"
                fill="url(#landG)" stroke="rgba(255,255,255,.18)" stroke-width="1.5" stroke-linejoin="round" filter="url(#shadow)"/>
          <!-- Istanbul Boğazı -->
          <path d="M176,88 Q180,98 178,108 Q175,115 177,122" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity=".6">
            <animate attributeName="opacity" values=".4;.8;.4" dur="3s" repeatCount="indefinite"/></path>
          <text x="193" y="107" fill="#38bdf8" font-size="5.5" font-weight="700" opacity=".7">Istanbul Bog.</text>
          <!-- Çanakkale Boğazı -->
          <path d="M55,155 Q50,163 46,172 Q40,180 35,190" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" opacity=".6">
            <animate attributeName="opacity" values=".4;.8;.4" dur="3s" repeatCount="indefinite" begin="1.5s"/></path>
          <text x="62" y="175" fill="#38bdf8" font-size="5.5" font-weight="700" opacity=".7">Çanakkale Bog.</text>
          <!-- Deniz isimleri -->
          <text x="480" y="22" fill="rgba(56,189,248,.2)" font-size="16" font-weight="800" text-anchor="middle" letter-spacing="8">KARADENIZ</text>
          <text x="200" y="125" fill="rgba(56,189,248,.12)" font-size="9" font-weight="700" text-anchor="middle" letter-spacing="3">MARMARA</text>
          <text x="25" y="350" fill="rgba(56,189,248,.15)" font-size="11" font-weight="700" text-anchor="middle" letter-spacing="4" transform="rotate(-90,25,350)">EGE</text>
          <text x="420" y="512" fill="rgba(56,189,248,.2)" font-size="16" font-weight="800" text-anchor="middle" letter-spacing="8">AKDENIZ</text>
        </svg>
      </div>
    </div>
  </div>
</div>
<div class="det" id="dp"><button class="cb" onclick="cD()">&#10005;</button><div id="dc"></div></div>
<div class="tt" id="tt"></div>
<script>
var F={features_js};
var CATS={cats_js};
var svg=document.getElementById("mapSvg");
var leg=document.getElementById("leg");
var m3d=document.getElementById("m3d");
var scn=document.getElementById("scn");
var activeFilter=null;
var _trackPaused=false;
// 3D fare takibi
scn.addEventListener("mousemove",function(e){{
  if(_trackPaused)return;
  var r=scn.getBoundingClientRect();
  var mx=(e.clientX-r.left)/r.width-.5;
  var my=(e.clientY-r.top)/r.height-.5;
  m3d.style.transform="rotateX("+(25-my*12)+"deg) rotateZ("+(-2+mx*6)+"deg)";
}});
scn.addEventListener("mouseleave",function(){{
  if(_trackPaused)return;
  m3d.style.transform="rotateX(25deg) rotateZ(-2deg)";
}});
// GeoJSON il sınırlarini arka planda ciz
function projX(lon){{return(lon-25.5)*50}}
function projY(lat){{return(42.5-lat)*74.3}}
function drawProvinceBorders(){{
  fetch("https://raw.githubusercontent.com/cihadturhan/tr-geojson/master/geo/tr-cities-utf8.json")
  .then(function(r){{return r.json()}})
  .then(function(geo){{
    var grp=document.createElementNS("http://www.w3.org/2000/svg","g");
    grp.setAttribute("id","borders");
    var BOLGE_PLAKA={{
      "Marmara":[11,16,17,22,34,39,41,54,59,67,74,77,78,81,10],
      "Ege":[3,9,20,35,43,45,48,64],
      "Akdeniz":[7,15,31,32,33,46,70,80],
      "İç Anadolu":[6,18,26,38,40,42,50,51,58,66,68,71],
      "Karadeniz":[5,8,14,19,28,29,37,52,53,55,57,60,61,69],
      "Doğu Anadolu":[4,12,13,23,24,25,30,36,49,62,65,75,76],
      "Güneydoğu Anadolu":[2,21,27,44,47,56,63,72,73,79]
    }};
    var BOLGE_CLR={{"Marmara":"#3b82f6","Ege":"#22c55e","Akdeniz":"#f97316",
      "İç Anadolu":"#eab308","Karadeniz":"#10b981","Doğu Anadolu":"#ef4444","Güneydoğu Anadolu":"#a855f7"}};
    function getBölge(plk){{for(var b in BOLGE_PLAKA)if(BOLGE_PLAKA[b].indexOf(plk)>=0)return b;return""}}
    var GN={{"Adana":1,"Ad\u0131yaman":2,"Afyon":3,"A\u011fr\u0131":4,"Amasya":5,"Ankara":6,
      "Antalya":7,"Artvin":8,"Ayd\u0131n":9,"Bal\u0131kesir":10,"Bilecik":11,
      "Bing\u00f6l":12,"Bitlis":13,"Bolu":14,"Burdur":15,"Bursa":16,
      "\u00c7anakkale":17,"\u00c7ank\u0131r\u0131":18,"\u00c7orum":19,"Denizli":20,
      "Diyarbak\u0131r":21,"Edirne":22,"Elaz\u0131\u011f":23,"Erzincan":24,
      "Erzurum":25,"Eski\u015fehir":26,"Gaziantep":27,"Giresun":28,
      "G\u00fcm\u00fc\u015fhane":29,"Hakkari":30,"Hatay":31,"Isparta":32,
      "Mersin":33,"\u0130stanbul":34,"\u0130zmir":35,"Kars":36,"Kastamonu":37,
      "Kayseri":38,"K\u0131rklareli":39,"K\u0131r\u015fehir":40,"Kocaeli":41,
      "Konya":42,"K\u00fctahya":43,"Malatya":44,"Manisa":45,
      "Kahramanmara\u015f":46,"Mardin":47,"Mu\u011fla":48,"Mu\u015f":49,
      "Nev\u015fehir":50,"Ni\u011fde":51,"Ordu":52,"Rize":53,"Sakarya":54,
      "Samsun":55,"Siirt":56,"Sinop":57,"Sivas":58,"Tekirda\u011f":59,
      "Tokat":60,"Trabzon":61,"Tunceli":62,"\u015eanl\u0131urfa":63,
      "U\u015fak":64,"Van":65,"Yozgat":66,"Zonguldak":67,"Aksaray":68,
      "Bayburt":69,"Karaman":70,"K\u0131r\u0131kkale":71,"Batman":72,
      "\u015e\u0131rnak":73,"Bart\u0131n":74,"Ardahan":75,"I\u011fd\u0131r":76,
      "Yalova":77,"Karab\u00fck":78,"Kilis":79,"Osmaniye":80,"D\u00fczce":81}};
    geo.features.forEach(function(feat){{
      var geoName=feat.properties.name||"";
      var plk=GN[geoName]||GN[geoName.trim()]||0;
      if(!plk)return;
      var bölge=getBölge(plk);
      var clr=BOLGE_CLR[bölge]||"#475569";
      function coordsToPath(coords){{
        return coords.map(function(ring){{
          return "M"+ring.map(function(c){{return projX(c[0]).toFixed(1)+","+projY(c[1]).toFixed(1)}}).join("L")+"Z";
        }}).join(" ");
      }}
      var d="";
      if(feat.geometry.type==="Polygon"){{d=coordsToPath(feat.geometry.coordinates)}}
      else if(feat.geometry.type==="MultiPolygon"){{
        feat.geometry.coordinates.forEach(function(poly){{d+=coordsToPath(poly)+" "}})
      }}
      if(!d)return;
      var path=document.createElementNS("http://www.w3.org/2000/svg","path");
      path.setAttribute("d",d);
      path.setAttribute("fill",clr+"10");
      path.setAttribute("stroke",clr+"40");
      path.setAttribute("stroke-width","0.4");
      path.setAttribute("stroke-linejoin","round");
      path.setAttribute("class","prov-border");
      grp.appendChild(path);
    }});
    var firstDot=svg.querySelector(".geo-dot");
    if(firstDot)svg.insertBefore(grp,firstDot);
    else svg.appendChild(grp);
    var old=document.getElementById("trBorder");
    if(old)old.setAttribute("fill-opacity","0");
  }})
  .catch(function(err){{console.log("GeoJSON yuklenemedi:",err)}});
}}
drawProvinceBorders();
// Shape içons by category
var shapeMap={{
  dag:"triangle",nehir:"wave",gol:"diamond",ova:"rect",
  yanardag:"flame",plato:"hexagon",boğaz_geçit:"bridge",
  koy_bürün:"circle",ada:"star",sinir_kapisi:"gate"
}};
// Legend
Object.keys(CATS).forEach(function(k){{
  var c=CATS[k];
  var d=document.createElement("div");d.className="leg-i";d.setAttribute("data-cat",k);
  d.innerHTML='<span class="leg-d" style="background:'+c.color+';box-shadow:0 0 6px '+c.color+'"></span>'+c.emoji+' '+c.label;
  d.onclick=function(){{
    if(activeFilter===k){{activeFilter=null;document.querySelectorAll(".leg-i").forEach(function(e){{e.classList.remove("active")}})}}
    else{{activeFilter=k;document.querySelectorAll(".leg-i").forEach(function(e){{e.classList.remove("active")}});d.classList.add("active")}}
    applyFilter();
  }};
  leg.appendChild(d);
}});
function applyFilter(){{
  var q=document.getElementById("sBox").value.toLowerCase();
  document.querySelectorAll(".geo-dot").forEach(function(g){{
    var fid=g.getAttribute("data-fid");
    var feat=F.find(function(f){{return f[0]===fid}});
    if(!feat)return;
    var catMatch=!activeFilter||feat[2]===activeFilter;
    var textMatch=!q||feat[1].toLowerCase().indexOf(q)>=0||feat[2].toLowerCase().indexOf(q)>=0;
    g.style.opacity=(catMatch&&textMatch)?"1":"0.08";
  }});
}}
function filterF(q){{applyFilter()}}
// Render features on map
F.forEach(function(f){{
  var fid=f[0],name=f[1],cat=f[2],cx=f[3],cy=f[4],info=f[5];
  var catInfo=CATS[cat]||{{}};
  var clr=catInfo.color||"#94a3b8";
  var emoji=catInfo.emoji||"\u2b55";
  var g=document.createElementNS("http://www.w3.org/2000/svg","g");
  g.setAttribute("class","geo-dot");g.setAttribute("data-fid",fid);
  g.style.color=clr;
  // Glow halo
  var halo=document.createElementNS("http://www.w3.org/2000/svg","circle");
  halo.setAttribute("cx",cx);halo.setAttribute("cy",cy);halo.setAttribute("r","12");
  halo.setAttribute("fill","none");halo.setAttribute("stroke",clr);
  halo.setAttribute("stroke-width","0.4");halo.setAttribute("stroke-opacity","0.15");
  g.appendChild(halo);
  // Shape based on category
  var shape=shapeMap[cat]||"circle";
  if(shape==="triangle"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    p.setAttribute("points",(cx)+","+(cy-8)+" "+(cx-6)+","+(cy+4)+" "+(cx+6)+","+(cy+4));
    p.setAttribute("fill",clr);p.setAttribute("fill-opacity","0.8");
    p.setAttribute("stroke","#fff");p.setAttribute("stroke-width","0.5");p.setAttribute("stroke-opacity","0.3");g.appendChild(p);
    var sn=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    sn.setAttribute("points",(cx)+","+(cy-8)+" "+(cx-2)+","+(cy-4)+" "+(cx+2)+","+(cy-4));
    sn.setAttribute("fill","#fff");sn.setAttribute("fill-opacity","0.5");g.appendChild(sn);
  }}else if(shape==="diamond"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    p.setAttribute("points",cx+","+(cy-7)+" "+(cx+6)+","+cy+" "+cx+","+(cy+7)+" "+(cx-6)+","+cy);
    p.setAttribute("fill",clr);p.setAttribute("fill-opacity","0.6");
    p.setAttribute("stroke","#fff");p.setAttribute("stroke-width","0.5");p.setAttribute("stroke-opacity","0.3");g.appendChild(p);
    var ws=document.createElementNS("http://www.w3.org/2000/svg","ellipse");
    ws.setAttribute("cx",cx);ws.setAttribute("cy",cy);ws.setAttribute("rx","3");ws.setAttribute("ry","1.5");
    ws.setAttribute("fill","rgba(255,255,255,.2)");g.appendChild(ws);
  }}else if(shape==="rect"){{
    var r=document.createElementNS("http://www.w3.org/2000/svg","rect");
    r.setAttribute("x",cx-6);r.setAttribute("y",cy-3.5);r.setAttribute("width","12");r.setAttribute("height","7");
    r.setAttribute("rx","2");r.setAttribute("fill",clr);r.setAttribute("fill-opacity","0.6");
    r.setAttribute("stroke","#fff");r.setAttribute("stroke-width","0.5");r.setAttribute("stroke-opacity","0.3");g.appendChild(r);
  }}else if(shape==="flame"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    p.setAttribute("points",(cx)+","+(cy-9)+" "+(cx-5)+","+(cy+1)+" "+(cx-2)+","+(cy-2)+" "+(cx)+","+(cy+5)+" "+(cx+2)+","+(cy-2)+" "+(cx+5)+","+(cy+1));
    p.setAttribute("fill","#ef4444");p.setAttribute("fill-opacity","0.8");
    p.setAttribute("stroke","#fbbf24");p.setAttribute("stroke-width","0.8");g.appendChild(p);
    var lg=document.createElementNS("http://www.w3.org/2000/svg","circle");
    lg.setAttribute("cx",cx);lg.setAttribute("cy",cy-3);lg.setAttribute("r","4");
    lg.setAttribute("fill","#ef4444");lg.setAttribute("fill-opacity","0.15");g.appendChild(lg);
  }}else if(shape==="wave"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","path");
    p.setAttribute("d","M"+(cx-8)+","+cy+" Q"+(cx-4)+","+(cy-5)+" "+cx+","+cy+" Q"+(cx+4)+","+(cy+5)+" "+(cx+8)+","+cy);
    p.setAttribute("fill","none");p.setAttribute("stroke",clr);p.setAttribute("stroke-width","2.5");
    p.setAttribute("stroke-linecap","round");p.setAttribute("stroke-opacity","0.8");g.appendChild(p);
    var p2=document.createElementNS("http://www.w3.org/2000/svg","path");
    p2.setAttribute("d","M"+(cx-6)+","+(cy+3)+" Q"+(cx-2)+","+(cy)+" "+(cx+2)+","+(cy+3)+" Q"+(cx+4)+","+(cy+5)+" "+(cx+6)+","+(cy+3));
    p2.setAttribute("fill","none");p2.setAttribute("stroke",clr);p2.setAttribute("stroke-width","1.2");
    p2.setAttribute("stroke-linecap","round");p2.setAttribute("stroke-opacity","0.4");g.appendChild(p2);
  }}else if(shape==="star"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    var pts="";for(var i=0;i<5;i++){{var a1=(-90+i*72)*Math.PI/180;var a2=(-90+i*72+36)*Math.PI/180;
      pts+=(cx+6*Math.cos(a1))+","+(cy+6*Math.sin(a1))+" ";
      pts+=(cx+3*Math.cos(a2))+","+(cy+3*Math.sin(a2))+" ";}}
    p.setAttribute("points",pts);p.setAttribute("fill",clr);p.setAttribute("fill-opacity","0.7");
    p.setAttribute("stroke","#fff");p.setAttribute("stroke-width","0.4");p.setAttribute("stroke-opacity","0.3");g.appendChild(p);
  }}else if(shape==="hexagon"){{
    var pts="";for(var i=0;i<6;i++){{var a=i*60*Math.PI/180;pts+=(cx+6*Math.cos(a))+","+(cy+6*Math.sin(a))+" ";}}
    var p=document.createElementNS("http://www.w3.org/2000/svg","polygon");
    p.setAttribute("points",pts);p.setAttribute("fill",clr);p.setAttribute("fill-opacity","0.6");
    p.setAttribute("stroke","#fff");p.setAttribute("stroke-width","0.5");p.setAttribute("stroke-opacity","0.3");g.appendChild(p);
  }}else if(shape==="bridge"){{
    var p=document.createElementNS("http://www.w3.org/2000/svg","path");
    p.setAttribute("d","M"+(cx-6)+","+(cy+3)+" L"+(cx-6)+","+(cy-2)+" Q"+cx+","+(cy-8)+" "+(cx+6)+","+(cy-2)+" L"+(cx+6)+","+(cy+3));
    p.setAttribute("fill",clr);p.setAttribute("fill-opacity","0.6");
    p.setAttribute("stroke","#fff");p.setAttribute("stroke-width","0.5");p.setAttribute("stroke-opacity","0.3");g.appendChild(p);
  }}else if(shape==="gate"){{
    var r=document.createElementNS("http://www.w3.org/2000/svg","rect");
    r.setAttribute("x",cx-5);r.setAttribute("y",cy-6);r.setAttribute("width","10");r.setAttribute("height","12");
    r.setAttribute("rx","2");r.setAttribute("fill",clr);r.setAttribute("fill-opacity","0.7");
    r.setAttribute("stroke","#fff");r.setAttribute("stroke-width","0.6");r.setAttribute("stroke-opacity","0.4");g.appendChild(r);
    var arc=document.createElementNS("http://www.w3.org/2000/svg","path");
    arc.setAttribute("d","M"+(cx-5)+","+(cy-6)+" Q"+cx+","+(cy-12)+" "+(cx+5)+","+(cy-6));
    arc.setAttribute("fill",clr);arc.setAttribute("fill-opacity","0.5");
    arc.setAttribute("stroke","#fff");arc.setAttribute("stroke-width","0.4");g.appendChild(arc);
  }}else{{
    var c1=document.createElementNS("http://www.w3.org/2000/svg","circle");
    c1.setAttribute("cx",cx);c1.setAttribute("cy",cy);c1.setAttribute("r","6");
    c1.setAttribute("fill",clr);c1.setAttribute("fill-opacity","0.6");
    c1.setAttribute("stroke","#fff");c1.setAttribute("stroke-width","0.5");c1.setAttribute("stroke-opacity","0.3");g.appendChild(c1);
  }}
  // Shine dot
  var sh=document.createElementNS("http://www.w3.org/2000/svg","circle");
  sh.setAttribute("cx",cx-1);sh.setAttribute("cy",cy-2);sh.setAttribute("r","1.2");
  sh.setAttribute("fill","rgba(255,255,255,.3)");g.appendChild(sh);
  // Label
  var txt=document.createElementNS("http://www.w3.org/2000/svg","text");
  txt.setAttribute("x",cx);txt.setAttribute("y",cy-14);txt.setAttribute("class","geo-label");
  txt.textContent=name;g.appendChild(txt);
  // Events
  g.onmouseenter=function(e){{showTT(e,f,catInfo)}};
  g.onmousemove=function(e){{moveTT(e)}};
  g.onmouseleave=hideTT;
  g.onclick=function(){{showDetail(f,catInfo)}};
  svg.appendChild(g);
}});
// Tooltip
var tt=document.getElementById("tt");
function showTT(e,f,ci){{
  var info=f[5];var name=f[1];
  var h='<div class="tn">'+ci.emoji+' '+name+'</div>';
  h+='<div class="tc" style="background:'+ci.color+'18;color:'+ci.color+';border:1px solid '+ci.color+'30">'+ci.label+'</div>';
  var keys=["yükseklik","uzunluk","alan","konum","bölge","tur","genişlik","derinlik","kaynak","dökülme"];
  keys.forEach(function(k){{if(info[k])h+='<div class="tr">\u2022 '+k.charAt(0).toUpperCase()+k.slice(1)+': '+info[k]+'</div>'}});
  if(info.bilgi)h+='<div class="tr" style="margin-top:4px;color:#cbd5e1;font-size:.72rem;border-top:1px solid rgba(255,255,255,.06);padding-top:4px">'+info.bilgi.substring(0,120)+'...</div>';
  tt.innerHTML=h;tt.className="tt show";moveTT(e);
}}
function moveTT(e){{var x=e.clientX+16,y=e.clientY+16;
  if(x+280>window.innerWidth)x=e.clientX-280;
  if(y+200>window.innerHeight)y=e.clientY-200;
  tt.style.left=x+"px";tt.style.top=y+"px";
}}
function hideTT(){{tt.className="tt"}}
// Detail panel
function showDetail(f,ci){{
  _trackPaused=true;
  hideTT();
  var info=f[5];var name=f[1];var clr=ci.color;
  var dp=document.getElementById("dp"),dc=document.getElementById("dc");
  document.querySelectorAll(".geo-dot").forEach(function(g){{
    g.classList.remove("selected");g.style.filter="";
  }});
  var sel=document.querySelector('.geo-dot[data-fid="'+f[0]+'"]');
  if(sel){{sel.classList.add("selected")}}
  var h='<div class="dh"><div class="d-badge" style="background:linear-gradient(135deg,'+clr+','+clr+'88)">'+ci.emoji+'</div>';
  h+='<div class="d-title"><h3>'+name+'</h3><p style="color:'+clr+'">'+ci.label+'</p></div></div>';
  h+='<div class="d-grid">';
  var fields=[["yükseklik","Yükseklik"],["uzunluk","Uzunluk"],["alan","Alan"],
    ["konum","Konum"],["bölge","Bölge"],["derinlik","Derinlik"],
    ["kaynak","Kaynak"],["dökülme","Dokulme"],["tur","Tur"],["genişlik","Genişlik"]];
  fields.forEach(function(pair){{
    if(info[pair[0]])h+='<div class="d-card"><div class="dl">'+pair[1]+'</div><div class="dv">'+info[pair[0]]+'</div></div>';
  }});
  h+='</div>';
  if(info.bilgi)h+='<div class="d-info">\U0001f4d6 '+info.bilgi+'</div>';
  if(info.özellik)h+='<div class="d-feat">\u2b50 '+info.özellik+'</div>';
  dc.innerHTML=h;dp.className="det show";
  dp.scrollIntoView({{behavior:"smooth",block:"nearest"}});
}}
function cD(){{document.getElementById("dp").className="det";_trackPaused=false;
  document.querySelectorAll(".geo-dot").forEach(function(g){{g.classList.remove("selected");g.style.filter=""}})}}
</script></body></html>'''


def _render_turkey_geography_category(store, ci):
    """Türkiye Coğrafyası ozel kategori sayfasi — fiziki harita."""
    cat_name, emoji, color, _ = _CATS[ci]
    styled_section(f"{emoji} {cat_name} — Fiziki Harita", color)
    styled_info_banner(
        "Haritada dağlara, nehirlere, göllere ve diger coğrafi ogelere tiklayin!",
        "info", "\U0001f3d4\ufe0f"
    )
    html = _build_turkey_geography_map_html()
    components.html(html, height=820, scrolling=True)
    # Sesli anlatim + bilgi kartlari
    _render_anatomy_info(ci, 0, "Türkiye Coğrafyası", emoji, color)


def _build_world_political_map_html():
    """Dünya Siyasi Haritası — tamamen inline SVG, sıfır CDN/fetch. Anında yükleme."""
    if not _WORLD_C:
        return "<html><body><p>Dünya harita verisi yüklenemedi.</p></body></html>"
    countries_js = json.dumps(
        [[c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12]]
         for c in _WORLD_C], ensure_ascii=False)
    conts_js = json.dumps(_CONT_CLR, ensure_ascii=False)
    # ── Pre-computed SVG country paths (Python'da hesaplandı) ──
    svg_paths_html = []
    c_by_iso = {c[0]: c for c in _WORLD_C}
    for iso, d in _CPATHS.items():
        c = c_by_iso.get(iso)
        cont = c[2] if c else None
        clr = _CONT_CLR.get(cont, {}).get("color", "#475569") if cont else "#475569"
        svg_paths_html.append(
            f'<path d="{d}" fill="{clr}" fill-opacity="0.35" stroke="{clr}" '
            f'stroke-opacity="0.8" stroke-width="0.7" stroke-linejoin="round" '
            f'class="country-path" data-iso="{iso}" '
            f'onclick="hC({iso})" onmouseenter="hE(event,{iso})" '
            f'onmousemove="hM(event)" onmouseleave="hL(this,{iso})"/>'
        )
    all_paths = "\n".join(svg_paths_html)
    # ── Capital dots + labels (pre-rendered) ──
    dots_html = []
    for c in _WORLD_C:
        iso, name, cont = c[0], c[1], c[2]
        lat, lon, area = c[4], c[5], c[7]
        clr = _CONT_CLR.get(cont, {}).get("color", "#94a3b8")
        cx = (lon + 180) * (1400 / 360)
        cy = (90 - lat) * (700 / 180)
        if cx < 5 or cx > 1395 or cy < 5 or cy > 695:
            continue
        dots_html.append(
            f'<g class="cap-dot" data-iso="{iso}" data-cont="{cont}" '
            f'onclick="hC({iso})" onmouseenter="hE(event,{iso})" '
            f'onmousemove="hM(event)" onmouseleave="hL(this,{iso})">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{clr}" '
            f'fill-opacity="0.9" stroke="#fff" stroke-width="0.4"/>'
        )
        if area and area > 100000:
            dots_html.append(
                f'<text x="{cx:.1f}" y="{cy - 4:.1f}" class="country-label">{name}</text>'
            )
        dots_html.append('</g>')
    all_dots = "\n".join(dots_html)
    # ── Graticule SVG (pre-rendered) ──
    grat_lines = []
    for lon in range(-180, 181, 30):
        x = (lon + 180) * (1400 / 360)
        grat_lines.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="700" class="grat"/>')
    for lat in range(-60, 81, 30):
        y = (90 - lat) * (700 / 180)
        grat_lines.append(f'<line x1="0" y1="{y:.1f}" x2="1400" y2="{y:.1f}" class="grat"/>')
    eq_y = (90 - 0) * (700 / 180)
    grat_lines.append(f'<line x1="0" y1="{eq_y:.1f}" x2="1400" y2="{eq_y:.1f}" class="equator"/>')
    tc_y = (90 - 23.44) * (700 / 180)
    grat_lines.append(f'<line x1="0" y1="{tc_y:.1f}" x2="1400" y2="{tc_y:.1f}" class="tropic"/>')
    cp_y = (90 + 23.44) * (700 / 180)
    grat_lines.append(f'<line x1="0" y1="{cp_y:.1f}" x2="1400" y2="{cp_y:.1f}" class="tropic"/>')
    ocean_lbls = [
        ("ATLANTİK OKYANUSU", (-35 + 180) * 1400 / 360, (90 - 25) * 700 / 180),
        ("PASİFİK OKYANUSU", (-150 + 180) * 1400 / 360, (90 - 5) * 700 / 180),
        ("HİNT OKYANUSU", (75 + 180) * 1400 / 360, (90 + 20) * 700 / 180),
        ("KUZEY BUZ DENİZİ", (0 + 180) * 1400 / 360, (90 - 80) * 700 / 180),
    ]
    for lbl, ox, oy in ocean_lbls:
        grat_lines.append(f'<text x="{ox:.1f}" y="{oy:.1f}" class="ocean-lbl">{lbl}</text>')
    all_grat = "\n".join(grat_lines)
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:linear-gradient(135deg,#0a0f1a 0%,#0c1929 40%,#0d1f3c 100%);
font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden;color:#e2e8f0}}
.hdr{{text-align:center;padding:14px 10px 8px}}
.hdr h2{{font-size:1.15rem;background:linear-gradient(135deg,#60a5fa,#34d399,#a78bfa);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0}}
.hdr p{{font-size:.7rem;color:#64748b;margin-top:2px}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;padding:6px 12px}}
.leg-i{{display:inline-flex;align-items:center;gap:4px;padding:4px 10px;
background:rgba(30,41,59,.7);border:1px solid rgba(71,85,105,.3);border-radius:16px;
font-size:.68rem;cursor:pointer;transition:all .2s;user-select:none}}
.leg-i:hover{{background:rgba(51,65,85,.8);transform:translateY(-1px)}}
.leg-i.active{{background:rgba(59,130,246,.2);border-color:rgba(96,165,250,.5);color:#93c5fd;
box-shadow:0 0 10px rgba(59,130,246,.2)}}
.leg-d{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.search-bar{{text-align:center;padding:4px 12px 8px}}
#sBox{{width:260px;padding:6px 12px;background:rgba(30,41,59,.8);border:1px solid rgba(71,85,105,.3);
border-radius:18px;color:#e2e8f0;font-size:.72rem;outline:none}}
#sBox:focus{{border-color:rgba(96,165,250,.5);box-shadow:0 0 8px rgba(59,130,246,.15)}}
#sBox::placeholder{{color:#64748b}}
.scene{{perspective:1200px;display:flex;justify-content:center;padding:10px 5px}}
.map3d{{transform:rotateX(20deg) rotateZ(-1deg);transform-style:preserve-3d;
transition:transform .6s cubic-bezier(.23,1,.32,1);position:relative;
width:min(96vw,1100px);aspect-ratio:2/1}}
.map3d:hover{{transform:rotateX(15deg) rotateZ(0deg)}}
.sea-layer{{position:absolute;inset:0;border-radius:18px;overflow:hidden;
transform:translateZ(-8px);
background:linear-gradient(180deg,#0c1929 0%,#0a2540 50%,#0c1929 100%);z-index:-1}}
.sea-anim{{position:absolute;inset:-50%;
background:repeating-linear-gradient(120deg,transparent,transparent 40px,rgba(56,189,248,.03) 40px,rgba(56,189,248,.03) 80px);
animation:sw 25s linear infinite}}
@keyframes sw{{0%{{transform:translate(0,0)}}100%{{transform:translate(80px,80px)}}}}
.land-layer{{position:absolute;inset:0;border-radius:18px;
background:radial-gradient(ellipse at 50% 50%,rgba(16,185,129,.04) 0%,transparent 70%);
transform:translateZ(0px)}}
.land-top{{position:absolute;inset:0;transform:translateZ(12px)}}
.map-base{{width:100%;height:100%}}
#mapSvg{{width:100%;height:100%;filter:drop-shadow(0 4px 20px rgba(0,0,0,.4))}}
.country-path{{transition:fill-opacity .15s ease,opacity .3s ease,stroke-width .15s ease;cursor:pointer}}
.country-path:hover{{fill-opacity:.6;stroke-width:1.2;filter:brightness(1.4)}}
.cap-dot{{cursor:pointer;transition:opacity .3s ease}}
.country-label{{font-size:3.5px;fill:#e2e8f0;pointer-events:none;text-anchor:middle;font-weight:700;opacity:.85;text-shadow:0 0 2px rgba(0,0,0,.8)}}
.tt{{position:fixed;display:none;background:rgba(15,23,42,.95);backdrop-filter:blur(12px);
border:1px solid rgba(71,85,105,.4);border-radius:12px;padding:10px 14px;
max-width:300px;font-size:.72rem;color:#e2e8f0;z-index:9999;
box-shadow:0 8px 32px rgba(0,0,0,.4);pointer-events:none}}
.tt.show{{display:block}}
.tt .tn{{font-size:.82rem;font-weight:700;margin-bottom:4px}}
.tt .tc{{font-size:.62rem;padding:2px 8px;border-radius:8px;display:inline-block;margin-bottom:6px;color:#fff}}
.tt .ti{{font-size:.68rem;color:#94a3b8;line-height:1.5}}
.det{{display:none;margin:10px auto;max-width:700px;background:linear-gradient(135deg,rgba(15,23,42,.97),rgba(30,41,59,.95));
backdrop-filter:blur(16px);border:1px solid rgba(71,85,105,.3);border-radius:16px;
padding:18px;box-shadow:0 16px 48px rgba(0,0,0,.3)}}
.det.show{{display:block;animation:su .4s cubic-bezier(.23,1,.32,1)}}
@keyframes su{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.cb{{position:absolute;top:10px;right:14px;background:rgba(71,85,105,.3);border:none;
color:#94a3b8;font-size:1.1rem;cursor:pointer;border-radius:50%;width:28px;height:28px;
display:flex;align-items:center;justify-content:center}}
.cb:hover{{background:rgba(239,68,68,.3);color:#fca5a5}}
.dh{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.d-badge{{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;
justify-content:center;font-size:1.8rem}}
.d-title h3{{margin:0;font-size:.95rem;color:#1A2035}}
.d-title p{{margin:2px 0 0;font-size:.7rem;font-weight:600}}
.d-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:12px}}
.d-card{{background:rgba(30,41,59,.6);border:1px solid rgba(71,85,105,.2);border-radius:10px;padding:8px 10px}}
.d-card .dl{{font-size:.6rem;color:#64748b;text-transform:uppercase;letter-spacing:.5px}}
.d-card .dv{{font-size:.78rem;color:#1A2035;font-weight:600;margin-top:2px}}
.d-info{{font-size:.76rem;color:#94a3b8;line-height:1.7;padding:10px 12px;
background:rgba(30,41,59,.4);border-radius:10px;margin-bottom:10px;border-left:3px solid rgba(96,165,250,.4)}}
.d-video{{margin-top:10px;border-radius:12px;overflow:hidden}}
.d-video-title{{font-size:.65rem;color:#64748b;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px}}
.d-video iframe{{width:100%;height:200px;border-radius:10px;border:1px solid rgba(71,85,105,.2)}}
.d-yt-btn{{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;
background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border-radius:8px;
text-decoration:none;font-size:.75rem;font-weight:600;margin-top:8px;transition:all .2s}}
.d-yt-btn:hover{{filter:brightness(1.15);transform:translateY(-1px)}}
.d-tts-btn{{display:block;width:100%;padding:10px;
background:linear-gradient(135deg,rgba(139,92,246,.15),rgba(59,130,246,.1));
border:1px solid rgba(139,92,246,.2);border-radius:10px;
color:#a78bfa;font-size:.78rem;font-weight:600;cursor:pointer;margin-top:8px;transition:all .2s}}
.d-tts-btn:hover{{background:linear-gradient(135deg,rgba(139,92,246,.25),rgba(59,130,246,.15))}}
.grat{{stroke:rgba(148,163,184,.08);stroke-width:.3;fill:none}}
.equator{{stroke:rgba(250,204,21,.15);stroke-width:.5;stroke-dasharray:4,3;fill:none}}
.tropic{{stroke:rgba(251,146,60,.1);stroke-width:.3;stroke-dasharray:3,4;fill:none}}
.ocean-lbl{{font-size:5px;fill:rgba(56,189,248,.15);text-anchor:middle;font-weight:700;letter-spacing:2px}}
</style></head><body>
<div class="hdr">
<h2>\U0001f30d Dünya Siyasi Haritası</h2>
<p>195 ülke \u2022 7 kıta \u2022 Tıkla \u2192 Bilgi Kartı + Sesli Anlatım + Video</p>
</div>
<div class="legend" id="leg"></div>
<div class="search-bar"><input id="sBox" type="text" placeholder="\U0001f50d Ülke veya başkent ara..." oninput="applyFilter()"></div>
<div class="scene" id="scn">
<div class="map3d" id="m3d">
<div class="sea-layer"><div class="sea-anim"></div></div>
<div class="land-layer"></div>
<div class="land-top">
<div class="map-base">
<svg id="mapSvg" viewBox="0 0 1400 700" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="oceanG" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#0c4a6e" stop-opacity=".1"/>
<stop offset="100%" stop-color="#0a2540" stop-opacity=".05"/>
</linearGradient>
</defs>
<rect width="1400" height="700" fill="url(#oceanG)"/>
<g id="grat-g">{all_grat}</g>
<g id="country-grp">{all_paths}</g>
<g id="dots-g">{all_dots}</g>
</svg>
</div>
</div>
</div>
</div>
<div class="det" id="dp" style="position:relative">
<button class="cb" onclick="closeDetail()">\u2715</button>
<div id="dc"></div>
</div>
<div class="tt" id="tt"></div>
<script>
var C={countries_js};
var CONTS={conts_js};
var cByISO={{}};
C.forEach(function(c){{cByISO[c[0]]=c}});
var m3d=document.getElementById("m3d");
var scn=document.getElementById("scn");
var tt=document.getElementById("tt");
var dp=document.getElementById("dp");
var dc=document.getElementById("dc");
var activeFilter=null;
var _trackPaused=false;
var _cachedVoice=null;

// ── 3D Mouse tracking ──────────────────────────────
scn.addEventListener("mousemove",function(e){{
if(_trackPaused)return;
var r=scn.getBoundingClientRect();
var mx=(e.clientX-r.left)/r.width-.5;
var my=(e.clientY-r.top)/r.height-.5;
m3d.style.transform="rotateX("+(20-my*10)+"deg) rotateZ("+(-1+mx*4)+"deg)";
}});
scn.addEventListener("mouseleave",function(){{
if(!_trackPaused)m3d.style.transform="rotateX(20deg) rotateZ(-1deg)";
}});

// ── Inline event handlers (called from SVG onclick/onmouseenter) ──
function _clr(iso){{var c=cByISO[iso];return c&&CONTS[c[2]]?CONTS[c[2]].color:"#475569"}}
function hC(iso){{var c=cByISO[iso];if(c)showDetail(c,_clr(iso))}}
function hE(e,iso){{var c=cByISO[iso];if(c)showTT(e,c,_clr(iso));var el=e.currentTarget||e.target;if(el.tagName==="path"){{el.setAttribute("fill-opacity","0.6");el.setAttribute("stroke-width","1.2")}}}}
function hM(e){{moveTT(e)}}
function hL(el,iso){{hideTT();if(el.tagName==="path"){{el.setAttribute("fill-opacity","0.35");el.setAttribute("stroke-width","0.7")}}}}

// ── Legend ───────────────────────────────────────────
var legEl=document.getElementById("leg");
Object.keys(CONTS).forEach(function(k){{
if(k==="Antarktika")return;
var ci=CONTS[k];
var d=document.createElement("div");d.className="leg-i";d.setAttribute("data-cat",k);
d.innerHTML='<span class="leg-d" style="background:'+ci.color+'"></span>'+ci.emoji+" "+ci.label;
d.onclick=function(){{
if(activeFilter===k){{activeFilter=null;document.querySelectorAll(".leg-i").forEach(function(el){{el.classList.remove("active")}});}}
else{{activeFilter=k;document.querySelectorAll(".leg-i").forEach(function(el){{el.classList.remove("active")}});d.classList.add("active");}}
applyFilter();
}};
legEl.appendChild(d);
}});

// ── Tooltip ─────────────────────────────────────────
function fmtN(n){{
if(n>=1e9)return(n/1e9).toFixed(1)+" Mrd";
if(n>=1e6)return(n/1e6).toFixed(1)+" Mil";
if(n>=1e3)return(n/1e3).toFixed(0)+" Bin";
return String(n);
}}
function showTT(e,c,clr){{
var h='<div class="tn">'+c[10]+" "+c[1]+"</div>";
h+='<div class="tc" style="background:'+clr+'">'+c[2]+"</div>";
h+='<div class="ti">';
h+="\U0001f3db Başkent: "+c[3]+"<br>";
if(c[6])h+="\U0001f465 Nüfus: "+fmtN(c[6])+"<br>";
if(c[7])h+="\U0001f4cf Alan: "+fmtN(c[7])+" km\u00b2<br>";
h+="</div>";
tt.innerHTML=h;tt.className="tt show";
moveTT(e);
}}
function moveTT(e){{
var x=e.clientX+16,y=e.clientY+16;
if(x+300>window.innerWidth)x=e.clientX-300;
if(y+160>window.innerHeight)y=e.clientY-160;
tt.style.left=x+"px";tt.style.top=y+"px";
}}
function hideTT(){{tt.className="tt"}}

// ── Detail Panel ────────────────────────────────────
function showDetail(c,clr){{
_trackPaused=true;hideTT();
document.querySelectorAll(".country-path").forEach(function(p){{
p.style.opacity="0.2";p.style.transition="opacity .3s";
}});
var sel=document.querySelector('.country-path[data-iso="'+c[0]+'"]');
if(sel){{sel.style.opacity="1";sel.style.filter="brightness(1.5) drop-shadow(0 0 6px "+clr+")";}}
var h='<div class="dh">';
h+='<div class="d-badge" style="background:linear-gradient(135deg,'+clr+','+clr+'88);font-size:2rem">'+c[10]+"</div>";
h+='<div class="d-title"><h3>'+c[10]+" "+c[1]+"</h3>";
h+='<p style="color:'+clr+'">'+c[2]+"</p></div></div>";
h+='<div class="d-grid">';
h+='<div class="d-card"><div class="dl">Başkent</div><div class="dv">'+c[3]+"</div></div>";
h+='<div class="d-card"><div class="dl">Nüfus</div><div class="dv">'+fmtN(c[6])+"</div></div>";
h+='<div class="d-card"><div class="dl">Alan</div><div class="dv">'+fmtN(c[7])+" km\u00b2</div></div>";
h+='<div class="d-card"><div class="dl">Para Birimi</div><div class="dv">'+c[8]+"</div></div>";
h+='<div class="d-card"><div class="dl">Resmi Dil</div><div class="dv">'+c[9]+"</div></div>";
h+='<div class="d-card"><div class="dl">Koordinat</div><div class="dv">'+c[4].toFixed(1)+"\u00b0, "+c[5].toFixed(1)+"\u00b0</div></div>";
h+="</div>";
if(c[11])h+='<div class="d-info">\U0001f4d6 '+c[11]+"</div>";
if(c[12]&&c[12]!=="search"&&c[12]!==""){{
h+='<div class="d-video"><div class="d-video-title">\U0001f3ac Video İçerik</div>';
h+='<iframe src="'+c[12]+'?rel=0&modestbranding=1" frameborder="0" allowfullscreen ';
h+='allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"></iframe></div>';
}}else if(c[12]==="search"){{
var q=encodeURIComponent(c[1]+" ülkesi coğrafya belgeseli");
h+='<a class="d-yt-btn" href="https://www.youtube.com/results?search_query='+q+'" target="_blank">\u25b6 YouTube&#39;da İzle</a>';
}}
h+='<button class="d-tts-btn" onclick="speakC(this,'+c[0]+')">\U0001f50a Sesli Anlat</button>';
dc.innerHTML=h;dp.className="det show";
dp.scrollIntoView({{behavior:"smooth",block:"nearest"}});
}}
function closeDetail(){{
dp.className="det";_trackPaused=false;
document.querySelectorAll(".country-path").forEach(function(p){{
p.style.opacity="1";p.style.filter="";p.style.transition="opacity .3s";
}});
}}

// ── Per-country TTS ─────────────────────────────────
function speakC(btn,iso){{
speechSynthesis.cancel();
var c=cByISO[iso];if(!c)return;
var text=c[1]+", "+c[2]+" kıtasında yer alan bir ülkedir. ";
text+="Başkenti "+c[3]+"'dir. ";
var pop=c[6];
if(pop>=1000000000)text+="Nüfusu yaklaşık "+(pop/1000000000).toFixed(1)+" milyardır. ";
else if(pop>=1000000)text+="Nüfusu yaklaşık "+Math.round(pop/1000000)+" milyondur. ";
else if(pop>=1000)text+="Nüfusu yaklaşık "+Math.round(pop/1000)+" bindir. ";
if(c[11])text+=c[11];
var utt=new SpeechSynthesisUtterance(text);
utt.lang="tr-TR";utt.rate=1.0;utt.volume=1.0;
if(!_cachedVoice){{
var voices=speechSynthesis.getVoices();
var trV=voices.filter(function(v){{return v.lang&&v.lang.indexOf("tr")===0}});
var femN=["emel","yelda","seda","filiz","zeynep","ayse","elif","sibel","deniz"];
var best=null;var bestS=-999;
(trV.length>0?trV:voices).forEach(function(v){{
var s=0;var nl=v.name.toLowerCase();
if(v.lang&&v.lang.indexOf("tr")===0)s+=500;
if(nl.indexOf("neural")>=0)s+=200;
if(nl.indexOf("online")>=0||nl.indexOf("natural")>=0)s+=150;
femN.forEach(function(fn){{if(nl.indexOf(fn)>=0)s+=80}});
if(nl.indexOf("male")>=0&&nl.indexOf("female")<0)s-=5000;
if(s>bestS){{bestS=s;best=v;}}
}});
if(best){{_cachedVoice=best;}}
}}
if(_cachedVoice)utt.voice=_cachedVoice;
utt.pitch=1.05;
btn.textContent="\U0001f50a Oynatılıyor...";
btn.style.color="#60a5fa";
utt.onend=function(){{btn.textContent="\U0001f50a Sesli Anlat";btn.style.color="#a78bfa";}};
speechSynthesis.speak(utt);
if(window._ttsKA)clearInterval(window._ttsKA);
window._ttsKA=setInterval(function(){{
if(speechSynthesis.speaking&&!speechSynthesis.paused){{speechSynthesis.pause();speechSynthesis.resume();}}
else clearInterval(window._ttsKA);
}},10000);
}}
(function(){{
function lv(){{speechSynthesis.getVoices()}}
lv();if(speechSynthesis.onvoiceschanged!==undefined)speechSynthesis.onvoiceschanged=lv;
setTimeout(lv,100);setTimeout(lv,500);setTimeout(lv,1500);
}})();

// ── Filter ──────────────────────────────────────────
function applyFilter(){{
var q=document.getElementById("sBox").value.toLowerCase();
document.querySelectorAll(".cap-dot").forEach(function(g){{
var iso=parseInt(g.getAttribute("data-iso"));
var cont=g.getAttribute("data-cont");
var c=cByISO[iso];
var name=c?c[1].toLowerCase():"";
var cap=c?c[3].toLowerCase():"";
var catM=!activeFilter||cont===activeFilter;
var txtM=!q||name.indexOf(q)>=0||cap.indexOf(q)>=0;
g.style.opacity=(catM&&txtM)?"1":"0.06";
}});
document.querySelectorAll(".country-path").forEach(function(p){{
var iso=parseInt(p.getAttribute("data-iso"));
var c=cByISO[iso];
var cont=c?c[2]:null;
var catM=!activeFilter||cont===activeFilter;
p.style.opacity=catM?"1":"0.12";
}});
}}
</script></body></html>'''


def _render_world_map_category(store, ci):
    """Dünya Siyasi Haritası — premium 3D, TopoJSON, 195 ülke."""
    cat_name, emoji, color, _ = _CATS[ci]
    styled_section(f"{emoji} {cat_name} — 195 Ülke İnteraktif Harita", color)
    styled_info_banner(
        "Haritada ülkelere tıklayın — bilgi kartı, video ve sesli anlatım!",
        "info", "\U0001f30d"
    )
    html = _build_world_political_map_html()
    components.html(html, height=900, scrolling=True)
    _render_anatomy_info(ci, 0, "Dünya Siyasi Haritası", emoji, color)


# ══════════════════════════════════════════════════════════════
# ci=28  DÜNYA FİZİKİ HARİTASI
# ══════════════════════════════════════════════════════════════
def _phys_shape_svg(cat, cx, cy, clr):
    """Kategori bazlı SVG şekil üretici."""
    import math
    s = 5
    if cat == "dag":
        pts = f"{cx},{cy-s} {cx-s*.8},{cy+s*.5} {cx+s*.8},{cy+s*.5}"
        return (f'<polygon points="{pts}" fill="{clr}" fill-opacity="0.7" stroke="{clr}" stroke-width="0.5"/>'
                f'<circle cx="{cx}" cy="{cy-s+1.5}" r="1.2" fill="#fff" fill-opacity="0.7"/>')
    if cat == "nehir":
        return (f'<path d="M{cx-s},{cy} Q{cx-s*.3:.1f},{cy-s*.5:.1f} {cx},{cy} T{cx+s},{cy}" '
                f'fill="none" stroke="{clr}" stroke-width="1.5" stroke-linecap="round" stroke-opacity="0.8"/>')
    if cat == "yanardag":
        pts = f"{cx},{cy-s*1.2:.1f} {cx-s*.5:.1f},{cy-s*.3:.1f} {cx-s*.8:.1f},{cy+s*.5:.1f} {cx},{cy+s*.2:.1f} {cx+s*.8:.1f},{cy+s*.5:.1f} {cx+s*.5:.1f},{cy-s*.3:.1f}"
        return (f'<polygon points="{pts}" fill="{clr}" fill-opacity="0.8" stroke="#ff6600" stroke-width="0.3"/>'
                f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#ff4400" fill-opacity="0.2"/>')
    if cat == "gol":
        pts = f"{cx},{cy-s} {cx+s*.7:.1f},{cy} {cx},{cy+s} {cx-s*.7:.1f},{cy}"
        return (f'<polygon points="{pts}" fill="{clr}" fill-opacity="0.5" stroke="{clr}" stroke-width="0.5"/>'
                f'<ellipse cx="{cx}" cy="{cy+1}" rx="{s*.5:.1f}" ry="{s*.2:.1f}" fill="{clr}" fill-opacity="0.3"/>')
    if cat == "deniz":
        return f'<ellipse cx="{cx}" cy="{cy}" rx="{s*1.5:.1f}" ry="{s:.1f}" fill="{clr}" fill-opacity="0.18" stroke="{clr}" stroke-width="0.5" stroke-dasharray="2,1"/>'
    if cat == "okyanus":
        return (f'<circle cx="{cx}" cy="{cy}" r="{s*1.8:.1f}" fill="{clr}" fill-opacity="0.10" stroke="{clr}" stroke-width="0.5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{s:.1f}" fill="{clr}" fill-opacity="0.22"/>')
    if cat == "cukur":
        pts = f"{cx-s*.8:.1f},{cy-s*.5:.1f} {cx+s*.8:.1f},{cy-s*.5:.1f} {cx},{cy+s}"
        return f'<polygon points="{pts}" fill="{clr}" fill-opacity="0.7" stroke="{clr}" stroke-width="0.5"/>'
    if cat == "korfez":
        return f'<path d="M{cx-s},{cy} A{s},{s} 0 0 1 {cx+s},{cy}" fill="{clr}" fill-opacity="0.25" stroke="{clr}" stroke-width="0.6"/>'
    if cat == "burun":
        pts = f"{cx-s*.5:.1f},{cy-s*.4:.1f} {cx+s*.5:.1f},{cy} {cx-s*.5:.1f},{cy+s*.4:.1f}"
        return f'<polygon points="{pts}" fill="{clr}" fill-opacity="0.7" stroke="{clr}" stroke-width="0.5"/>'
    if cat == "ada":
        star_pts = []
        for i in range(10):
            r = s if i % 2 == 0 else s * 0.4
            a = math.pi / 2 + i * math.pi / 5
            star_pts.append(f"{cx + r * math.cos(a):.1f},{cy - r * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(star_pts)}" fill="{clr}" fill-opacity="0.55" stroke="{clr}" stroke-width="0.3"/>'
    if cat == "col":
        hex_pts = []
        for i in range(6):
            a = math.pi / 6 + i * math.pi / 3
            hex_pts.append(f"{cx + s * .8 * math.cos(a):.1f},{cy - s * .8 * math.sin(a):.1f}")
        return f'<polygon points="{" ".join(hex_pts)}" fill="{clr}" fill-opacity="0.45" stroke="{clr}" stroke-width="0.5"/>'
    if cat == "bogaz":
        return (f'<path d="M{cx-s},{cy+2} L{cx-s},{cy} A{s},{s*.8:.1f} 0 0 1 {cx+s},{cy} L{cx+s},{cy+2}" '
                f'fill="none" stroke="{clr}" stroke-width="1" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{s*.6:.1f}" fill="{clr}" fill-opacity="0.6" stroke="{clr}" stroke-width="0.5"/>'


def _build_world_physical_map_html():
    """Dünya Fiziki Haritası — dağ/nehir/yanardağ/göl/deniz/okyanus markerları + arka plan ülke sınırları."""
    if not _WORLD_GEO_FEAT:
        return "<html><body><p>Dünya fiziki coğrafya verisi yüklenemedi.</p></body></html>"
    features_js = json.dumps(
        [[f[0], f[1], f[2], f[3], f[4], f[5]] for f in _WORLD_GEO_FEAT],
        ensure_ascii=False)
    cats_js = json.dumps(_WORLD_GEO_CATS, ensure_ascii=False)
    # ── Arka plan ülke sınırları ──
    bg_paths = []
    for iso, d in _CPATHS.items():
        bg_paths.append(
            f'<path d="{d}" fill="#475569" fill-opacity="0.08" stroke="#475569" '
            f'stroke-opacity="0.15" stroke-width="0.4" class="bg-c"/>')
    all_bg = "\n".join(bg_paths)
    # ── Graticule ──
    grat_lines = []
    for lon in range(-180, 181, 30):
        x = (lon + 180) * (1400 / 360)
        grat_lines.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="700" class="grat"/>')
    for lat in range(-60, 81, 30):
        y = (90 - lat) * (700 / 180)
        grat_lines.append(f'<line x1="0" y1="{y:.1f}" x2="1400" y2="{y:.1f}" class="grat"/>')
    eq_y = (90 - 0) * (700 / 180)
    grat_lines.append(f'<line x1="0" y1="{eq_y:.1f}" x2="1400" y2="{eq_y:.1f}" class="equator"/>')
    for t_lat in [23.44, -23.44]:
        ty = (90 - t_lat) * (700 / 180)
        grat_lines.append(f'<line x1="0" y1="{ty:.1f}" x2="1400" y2="{ty:.1f}" class="tropic"/>')
    ocean_lbls = [
        (350, 280, "ATLANTİK\nOKYANUSU"), (1050, 250, "PASİFİK\nOKYANUSU"),
        (800, 420, "HİNT\nOKYANUSU"), (200, 80, "KUZEY BUZ\nDENİZİ"),
    ]
    for ox, oy, otxt in ocean_lbls:
        for li, ln in enumerate(otxt.split("\n")):
            grat_lines.append(f'<text x="{ox}" y="{oy + li * 8}" class="ocean-lbl">{ln}</text>')
    all_grat = "\n".join(grat_lines)
    # ── Coğrafi öge markerları ──
    markers = []
    for f in _WORLD_GEO_FEAT:
        fid, name, cat = f[0], f[1], f[2]
        lat, lon = f[3], f[4]
        cx = (lon + 180) * (1400 / 360)
        cy = (90 - lat) * (700 / 180)
        if cx < 3 or cx > 1397 or cy < 3 or cy > 697:
            continue
        clr = _WORLD_GEO_CATS.get(cat, {}).get("color", "#94a3b8")
        shape = _phys_shape_svg(cat, cx, cy, clr)
        markers.append(
            f'<g class="geo-dot" data-fid="{fid}" data-cat="{cat}" '
            f'onclick="hF(\'{fid}\')" onmouseenter="hFE(event,\'{fid}\')" '
            f'onmousemove="hFM(event)" onmouseleave="hFL(\'{fid}\')">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{clr}" fill-opacity="0.08" class="halo"/>'
            f'{shape}'
            f'<text x="{cx:.1f}" y="{cy - 7:.1f}" class="geo-lbl" fill="{clr}">{name}</text>'
            f'</g>')
    all_markers = "\n".join(markers)
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:linear-gradient(135deg,#0a0e1a 0%,#0d1526 50%,#091120 100%);
font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden;color:#e2e8f0}}
.hdr{{text-align:center;padding:14px 10px 8px;
background:linear-gradient(135deg,rgba(5,150,105,.12),rgba(16,185,129,.08));
border-bottom:1px solid rgba(16,185,129,.15)}}
.hdr h2{{font-size:1.1rem;
background:linear-gradient(135deg,#34d399,#10b981,#059669);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800}}
.hdr p{{font-size:.7rem;color:#64748b;margin-top:2px}}
.legend{{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;padding:8px 10px;
background:rgba(15,23,42,.5);border-bottom:1px solid rgba(51,65,85,.3)}}
.leg-i{{display:flex;align-items:center;gap:3px;padding:3px 8px;border-radius:6px;
font-size:.6rem;color:#94a3b8;cursor:pointer;border:1px solid rgba(71,85,105,.2);
transition:all .2s;background:rgba(30,41,59,.3)}}
.leg-i:hover{{background:rgba(51,65,85,.4);color:#e2e8f0}}
.leg-i.active{{border-color:rgba(16,185,129,.5);color:#34d399;
background:rgba(16,185,129,.08)}}
.leg-d{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.search-bar{{padding:6px 12px;background:rgba(15,23,42,.4);
border-bottom:1px solid rgba(51,65,85,.2)}}
.search-bar input{{width:100%;padding:6px 12px;border-radius:8px;border:1px solid rgba(71,85,105,.3);
background:rgba(30,41,59,.6);color:#e2e8f0;font-size:.72rem;outline:none}}
.search-bar input:focus{{border-color:rgba(16,185,129,.4)}}
.scene{{perspective:1200px;padding:12px;display:flex;justify-content:center}}
.map3d{{transform-style:preserve-3d;transform:rotateX(20deg) rotateZ(-1deg);
transition:transform .6s cubic-bezier(.23,1,.32,1);position:relative;
width:min(96vw,1100px);aspect-ratio:2/1}}
.map3d:hover{{transform:rotateX(15deg) rotateZ(0deg)}}
.sea-layer{{position:absolute;inset:-20px;border-radius:18px;
background:linear-gradient(180deg,#0a1628,#0c1e3a,#091a2f);
transform:translateZ(-8px);overflow:hidden;border:1px solid rgba(30,58,95,.3)}}
.sea-anim{{position:absolute;inset:-60px;
background:repeating-linear-gradient(45deg,transparent,transparent 40px,rgba(56,189,248,.03) 40px,rgba(56,189,248,.03) 80px);
animation:sw 12s linear infinite}}
@keyframes sw{{0%{{transform:translate(0,0)}}100%{{transform:translate(80px,80px)}}}}
.land-layer{{position:absolute;inset:-8px;border-radius:14px;
background:radial-gradient(ellipse at 50% 40%,rgba(16,54,36,.15),transparent 70%);
transform:translateZ(0)}}
.land-top{{position:relative;transform:translateZ(12px);border-radius:12px;
overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.4)}}
.map-base{{background:linear-gradient(180deg,rgba(10,20,40,.9),rgba(8,15,30,.95));
border-radius:12px;padding:2px}}
.bg-c{{pointer-events:none}}
.geo-dot{{cursor:pointer;transition:opacity .3s}}
.geo-dot:hover .halo{{fill-opacity:.2!important}}
.geo-lbl{{font-size:2.8px;fill-opacity:.85;text-anchor:middle;
font-weight:600;paint-order:stroke;stroke:#0a0e1a;stroke-width:.6px;
letter-spacing:.1px}}
.grat{{stroke:rgba(148,163,184,.08);stroke-width:.3;fill:none}}
.equator{{stroke:rgba(250,204,21,.15);stroke-width:.5;stroke-dasharray:4,3;fill:none}}
.tropic{{stroke:rgba(251,146,60,.1);stroke-width:.3;stroke-dasharray:3,4;fill:none}}
.ocean-lbl{{font-size:5px;fill:rgba(56,189,248,.12);text-anchor:middle;font-weight:700;letter-spacing:2px}}
.tt{{position:fixed;z-index:9999;pointer-events:none;
background:rgba(15,23,42,.95);backdrop-filter:blur(12px);
border:1px solid rgba(71,85,105,.3);border-radius:10px;
padding:8px 12px;min-width:180px;max-width:300px;
opacity:0;transition:opacity .15s;box-shadow:0 8px 24px rgba(0,0,0,.5)}}
.tt.show{{opacity:1}}
.tn{{font-size:.78rem;font-weight:700;color:#1A2035;margin-bottom:3px}}
.tc{{display:inline-block;padding:1px 7px;border-radius:4px;font-size:.6rem;
color:#fff;font-weight:600;margin-bottom:4px}}
.ti{{font-size:.65rem;color:#94a3b8;line-height:1.5}}
.det{{position:relative;max-width:700px;margin:0 auto;
background:linear-gradient(135deg,rgba(15,23,42,.97),rgba(20,30,52,.95));
border:1px solid rgba(71,85,105,.3);border-radius:16px;
padding:0;overflow:hidden;max-height:0;opacity:0;
transition:all .4s cubic-bezier(.23,1,.32,1)}}
.det.show{{max-height:3000px;opacity:1;padding:20px;margin-top:12px}}
.cb{{position:absolute;top:8px;right:10px;background:rgba(71,85,105,.3);
border:none;color:#94a3b8;width:26px;height:26px;border-radius:8px;
cursor:pointer;font-size:.8rem;z-index:10;transition:all .2s}}
.cb:hover{{background:rgba(239,68,68,.2);color:#f87171}}
.dh{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.d-badge{{width:48px;height:48px;border-radius:12px;display:flex;
align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0}}
.d-title h3{{font-size:1rem;color:#1A2035;font-weight:700}}
.d-title p{{font-size:.72rem;margin-top:2px}}
.d-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));
gap:8px;margin-bottom:10px}}
.d-card{{background:rgba(30,41,59,.5);border-radius:10px;padding:8px 10px;
border:1px solid rgba(71,85,105,.2);transition:all .2s}}
.d-card:hover{{border-color:rgba(16,185,129,.3);background:rgba(30,41,59,.7)}}
.dl{{font-size:.6rem;color:#64748b;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}}
.dv{{font-size:.78rem;color:#e2e8f0;font-weight:600}}
.d-info{{font-size:.76rem;color:#94a3b8;line-height:1.7;padding:10px 12px;
background:rgba(30,41,59,.4);border-radius:10px;margin-bottom:10px;
border-left:3px solid rgba(16,185,129,.4)}}
.d-yt-btn{{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;
background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border-radius:8px;
text-decoration:none;font-size:.75rem;font-weight:600;margin-top:8px;transition:all .2s}}
.d-yt-btn:hover{{filter:brightness(1.15);transform:translateY(-1px)}}
.d-tts-btn{{display:block;width:100%;padding:10px;
background:linear-gradient(135deg,rgba(16,185,129,.15),rgba(5,150,105,.1));
border:1px solid rgba(16,185,129,.2);border-radius:10px;
color:#34d399;font-size:.78rem;font-weight:600;cursor:pointer;margin-top:8px;transition:all .2s}}
.d-tts-btn:hover{{background:linear-gradient(135deg,rgba(16,185,129,.25),rgba(5,150,105,.15))}}
</style>
<script>
var F={features_js};
var CATS={cats_js};
var fByID={{}};F.forEach(function(f){{fByID[f[0]]=f}});
var activeFilter=null,_trackPaused=false,_cachedVoice=null;
var tt,dp,dc,m3d,scn;
var FIELDS={{
dag:[["yukseklik","Y\u00fckseklik"],["siradag","S\u0131ra Da\u011f"],["ulke","\u00dclke"],["kita","K\u0131ta"]],
nehir:[["uzunluk","Uzunluk"],["kaynak","Kaynak"],["dokulme","D\u00f6k\u00fclme"],["havza","Havza"],["ulkeler","\u00dclkeler"]],
yanardag:[["yukseklik","Y\u00fckseklik"],["son_patlama","Son Patlama"],["tur","T\u00fcr"],["ulke","\u00dclke"]],
gol:[["alan","Alan"],["derinlik","Derinlik"],["yukseklik","Y\u00fckseklik"],["tur","T\u00fcr"],["ulkeler","\u00dclkeler"]],
deniz:[["alan","Alan"],["derinlik","Derinlik"],["kiyi_ulkeleri","K\u0131y\u0131 \u00dclkeleri"]],
okyanus:[["alan","Alan"],["derinlik","Derinlik"],["en_derin","En Derin Nokta"]],
cukur:[["derinlik","Derinlik"],["okyanus","Okyanus"]],
korfez:[["alan","Alan"],["kiyi_ulkeleri","K\u0131y\u0131 \u00dclkeleri"]],
burun:[["ulke","\u00dclke"],["deniz_okyanus","Deniz / Okyanus"]],
ada:[["alan","Alan"],["ulke","\u00dclke"],["nufus","N\u00fcfus"]],
col:[["alan","Alan"],["tur","T\u00fcr"],["ulkeler","\u00dclkeler"]],
bogaz:[["uzunluk","Uzunluk"],["genislik","Geni\u015flik"],["baglanti","Ba\u011flant\u0131"]]
}};
function _clrF(fid){{var f=fByID[fid];return f&&CATS[f[2]]?CATS[f[2]].color:"#94a3b8"}}
function hF(fid){{var f=fByID[fid];if(f)showDetail(f,_clrF(fid))}}
function hFE(e,fid){{var f=fByID[fid];if(f)showTT(e,f,_clrF(fid))}}
function hFM(e){{moveTT(e)}}
function hFL(fid){{hideTT()}}
function showTT(e,f,clr){{
var info=f[5];var cat=f[2];var ci=CATS[cat];
var h='<div class="tn">'+(ci?ci.emoji:"")+" "+f[1]+"</div>";
h+='<div class="tc" style="background:'+clr+'">'+(ci?ci.label:cat)+"</div>";
h+='<div class="ti">';
var flds=FIELDS[cat]||[];
for(var i=0;i<flds.length&&i<3;i++){{var v=info[flds[i][0]];if(v)h+=flds[i][1]+": "+v+"<br>"}}
if(info.bilgi)h+=info.bilgi.substring(0,120)+"...";
h+="</div>";tt.innerHTML=h;tt.className="tt show";moveTT(e)}}
function moveTT(e){{var x=e.clientX+16,y=e.clientY+16;
if(x+300>window.innerWidth)x=e.clientX-300;
if(y+160>window.innerHeight)y=e.clientY-160;
tt.style.left=x+"px";tt.style.top=y+"px"}}
function hideTT(){{tt.className="tt"}}
function showDetail(f,clr){{
_trackPaused=true;hideTT();
document.querySelectorAll(".geo-dot").forEach(function(g){{g.style.opacity="0.15";g.style.transition="opacity .3s"}});
var sel=document.querySelector('.geo-dot[data-fid="'+f[0]+'"]');
if(sel){{sel.style.opacity="1";sel.style.filter="brightness(1.4) drop-shadow(0 0 6px "+clr+")"}}
var info=f[5];var cat=f[2];var ci=CATS[cat];
var h='<div class="dh">';
h+='<div class="d-badge" style="background:linear-gradient(135deg,'+clr+','+clr+'55);font-size:1.5rem">'+(ci?ci.emoji:"")+"</div>";
h+='<div class="d-title"><h3>'+(ci?ci.emoji:"")+" "+f[1]+"</h3>";
h+='<p style="color:'+clr+'">'+(ci?ci.label:cat)+"</p></div></div>";
h+='<div class="d-grid">';
var flds=FIELDS[cat]||[];
flds.forEach(function(fl){{var v=info[fl[0]];if(v)h+='<div class="d-card"><div class="dl">'+fl[1]+'</div><div class="dv">'+v+"</div></div>"}});
h+="</div>";
if(info.bilgi)h+='<div class="d-info">\U0001f4d6 '+info.bilgi+"</div>";
if(info.video_url&&info.video_url!=="search"&&info.video_url!==""){{
h+='<iframe src="'+info.video_url+'?rel=0&modestbranding=1" style="width:100%;height:200px;border-radius:10px;border:1px solid rgba(71,85,105,.2);margin-top:8px" frameborder="0" allowfullscreen></iframe>'}}
else if(info.video_url==="search"){{
var q=encodeURIComponent(f[1]+" co\u011frafya belgeseli");
h+='<a class="d-yt-btn" href="https://www.youtube.com/results?search_query='+q+'" target="_blank">\u25b6 YouTube&#39;da \u0130zle</a>'}}
h+='<button class="d-tts-btn" onclick="speakF(this,&#39;'+f[0]+'&#39;)">\U0001f50a Sesli Anlat</button>';
dc.innerHTML=h;dp.className="det show";
dp.scrollIntoView({{behavior:"smooth",block:"nearest"}})}}
function closeDetail(){{
dp.className="det";_trackPaused=false;
document.querySelectorAll(".geo-dot").forEach(function(g){{g.style.opacity="1";g.style.filter="";g.style.transition="opacity .3s"}})}}
function speakF(btn,fid){{
speechSynthesis.cancel();var f=fByID[fid];if(!f)return;
var info=f[5];var text=f[1]+". ";
if(info.bilgi)text+=info.bilgi;
var utt=new SpeechSynthesisUtterance(text);
utt.lang="tr-TR";utt.rate=1.0;utt.volume=1.0;
if(!_cachedVoice){{var voices=speechSynthesis.getVoices();
var trV=voices.filter(function(v){{return v.lang&&v.lang.indexOf("tr")===0}});
var femN=["emel","yelda","seda","filiz","zeynep","ayse","elif","sibel","deniz"];
var best=null;var bestS=-999;
(trV.length>0?trV:voices).forEach(function(v){{var s=0;var nl=v.name.toLowerCase();
if(v.lang&&v.lang.indexOf("tr")===0)s+=500;
if(nl.indexOf("neural")>=0)s+=200;
if(nl.indexOf("online")>=0||nl.indexOf("natural")>=0)s+=150;
femN.forEach(function(fn){{if(nl.indexOf(fn)>=0)s+=80}});
if(nl.indexOf("male")>=0&&nl.indexOf("female")<0)s-=5000;
if(s>bestS){{bestS=s;best=v}}}});
if(best)_cachedVoice=best}}
if(_cachedVoice)utt.voice=_cachedVoice;utt.pitch=1.05;
btn.textContent="\U0001f50a Oynat\u0131l\u0131yor...";btn.style.color="#34d399";
utt.onend=function(){{btn.textContent="\U0001f50a Sesli Anlat";btn.style.color="#34d399"}};
speechSynthesis.speak(utt);
if(window._ttsKA)clearInterval(window._ttsKA);
window._ttsKA=setInterval(function(){{if(speechSynthesis.speaking&&!speechSynthesis.paused){{speechSynthesis.pause();speechSynthesis.resume()}}else clearInterval(window._ttsKA)}},10000)}}
(function(){{function lv(){{speechSynthesis.getVoices()}}lv();
if(speechSynthesis.onvoiceschanged!==undefined)speechSynthesis.onvoiceschanged=lv;
setTimeout(lv,100);setTimeout(lv,500);setTimeout(lv,1500)}})();
function applyFilter(){{
var q=document.getElementById("sBox").value.toLowerCase();
document.querySelectorAll(".geo-dot").forEach(function(g){{
var fid=g.getAttribute("data-fid");
var cat=g.getAttribute("data-cat");
var f=fByID[fid];
var name=f?f[1].toLowerCase():"";
var catM=!activeFilter||cat===activeFilter;
var txtM=!q||name.indexOf(q)>=0;
g.style.opacity=(catM&&txtM)?"1":"0.06"}})}}
</script>
</head><body>
<div class="hdr">
<h2>\U0001f3d4\ufe0f D\u00fcnya Fiziki Haritas\u0131</h2>
<p>151 co\u011frafi \u00f6ge \u2022 12 kategori \u2022 T\u0131kla \u2192 Bilgi Kart\u0131 + Sesli Anlat\u0131m + Video</p>
</div>
<div class="legend" id="leg"></div>
<div class="search-bar"><input id="sBox" type="text" placeholder="\U0001f50d Co\u011frafi \u00f6ge ara..." oninput="applyFilter()"></div>
<div class="scene" id="scn">
<div class="map3d" id="m3d">
<div class="sea-layer"><div class="sea-anim"></div></div>
<div class="land-layer"></div>
<div class="land-top">
<div class="map-base">
<svg id="mapSvg" viewBox="0 0 1400 700" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="oceanG" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#0c4a6e" stop-opacity=".1"/>
<stop offset="100%" stop-color="#0a2540" stop-opacity=".05"/>
</linearGradient>
</defs>
<rect width="1400" height="700" fill="url(#oceanG)"/>
<g id="grat-g">{all_grat}</g>
<g id="bg-g">{all_bg}</g>
<g id="feat-g">{all_markers}</g>
</svg>
</div>
</div>
</div>
</div>
<div class="det" id="dp" style="position:relative">
<button class="cb" onclick="closeDetail()">\u2715</button>
<div id="dc"></div>
</div>
<div class="tt" id="tt"></div>
<script>
tt=document.getElementById("tt");dp=document.getElementById("dp");
dc=document.getElementById("dc");m3d=document.getElementById("m3d");
scn=document.getElementById("scn");
scn.addEventListener("mousemove",function(e){{
if(_trackPaused)return;
var r=scn.getBoundingClientRect();
var mx=(e.clientX-r.left)/r.width-.5;
var my=(e.clientY-r.top)/r.height-.5;
m3d.style.transform="rotateX("+(20-my*10)+"deg) rotateZ("+(-1+mx*4)+"deg)"}});
scn.addEventListener("mouseleave",function(){{
if(!_trackPaused)m3d.style.transform="rotateX(20deg) rotateZ(-1deg)"}});
var legEl=document.getElementById("leg");
Object.keys(CATS).forEach(function(k){{
var ci=CATS[k];
var d=document.createElement("div");d.className="leg-i";d.setAttribute("data-cat",k);
d.innerHTML='<span class="leg-d" style="background:'+ci.color+'"></span>'+ci.emoji+" "+ci.label;
d.onclick=function(){{
if(activeFilter===k){{activeFilter=null;document.querySelectorAll(".leg-i").forEach(function(el){{el.classList.remove("active")}})}}
else{{activeFilter=k;document.querySelectorAll(".leg-i").forEach(function(el){{el.classList.remove("active")}});d.classList.add("active")}}
applyFilter()}};
legEl.appendChild(d)}});
</script></body></html>'''


def _render_world_physical_map_category(store, ci):
    """Dünya Fiziki Haritası — dağlar, nehirler, yanardağlar, göller vb."""
    cat_name, emoji, color, _ = _CATS[ci]
    styled_section(f"{emoji} {cat_name} — İnteraktif Fiziki Harita", color)
    styled_info_banner(
        "Haritada dağlara, nehirlere, yanardağlara ve diğer coğrafi ögelere tıklayın!",
        "info", "\U0001f3d4\ufe0f"
    )
    html = _build_world_physical_map_html()
    components.html(html, height=900, scrolling=True)
    _render_anatomy_info(ci, 0, "Dünya Fiziki Haritası", emoji, color)


# ══════════════════════════════════════════════════════════════
# ci=29  DÜNYA TARİHİ — 7 DÖNEM TEK SAYFADA
# ══════════════════════════════════════════════════════════════

_DUNYA_TARIHI = [
    {
        "id": "kavimlergocu",
        "baslik": "Kavimler Göçü",
        "emoji": "🐎",
        "tarih": "375 – 568",
        "renk": "#92400E",
        "ozet": "Orta Asya'dan başlayan Hun akınlarının tetiklediği, Germen ve Slav kavimlerinin Avrupa'yı alt üst ettiği büyük göç dalgası. Roma İmparatorluğu'nun çöküşünü hızlandıran en kritik süreç.",
        "seslendirme": "Kavimler Göçü, 375 yılında Hunların Karadeniz'in kuzeyindeki Germen kavimlerine saldırmasıyla başlayan ve yaklaşık iki yüz yıl süren büyük göç dalgasıdır. Orta Asya'dan batıya doğru hareket eden Hunlar, önlerine çıkan Ostrogot, Vizigot, Vandal, Burgund ve Frank gibi Germen kavimlerini yerlerinden etti. Bu kavimler Roma İmparatorluğu topraklarına akın etti. Vizigotlar 410 yılında Roma şehrini yağmaladı. Vandallar Kuzey Afrika'yı ele geçirdi. Hunların en güçlü lideri Attila, Avrupa'yı titreten seferler düzenledi. Katalaunum Savaşı'nda Roma ve Vizigot ittifakına karşı savaştı. Kavimler Göçü Avrupa'nın etnik haritasını tamamen değiştirdi. Bugünkü Fransa, Almanya, İspanya ve İngiltere'nin temelleri bu dönemde atıldı. Roma İmparatorluğu'nun zayıflamasına ve bölünmesine yol açan en önemli etkenlerden biri oldu.",
        "bilgi_kartlari": [
            ("📅 Dönem", "375 – 568 (yaklaşık 200 yıl)"),
            ("📍 Coğrafya", "Orta Asya'dan Avrupa'ya, Kuzey Afrika'ya kadar"),
            ("🐎 Tetikleyen", "Hunların batıya doğru ilerlemesi"),
            ("⚔️ Göç Eden Kavimler", "Ostrogotlar, Vizigotlar, Vandallar, Franklar, Angıllar, Saksonlar"),
            ("👑 Attila", "Hun İmparatorluğu'nun en güçlü hükümdarı (434-453)"),
            ("🌍 Sonuç", "Avrupa'nın etnik ve siyasi haritası tamamen değişti"),
        ],
        "detay_kartlari": [
            ("🐎 Hunların Batıya İlerleyişi (375)", "Orta Asya steplerinden gelen Hunlar, süvari savaşçıları ve ok atma ustalıklarıyla Karadeniz'in kuzeyindeki Ostrogotları yendiler. Bu, domino etkisiyle tüm Germen kavimlerini harekete geçirdi."),
            ("⚔️ Vizigotların Roma'yı Yağması (410)", "Vizigot Kralı Alaric, Roma şehrini üç gün boyunca yağmaladı. Sekiz yüz yıldır fethedilmemiş olan Roma'nın düşüşü tüm dünyayı şoka uğrattı. Bu olay imparatorluğun sonunun habercisiydi."),
            ("👑 Attila — Tanrının Kırbacı (434-453)", "Hun İmparatoru Attila, Doğu Roma'dan haraç aldı, Galya'ya ve İtalya'ya seferler düzenledi. Avrupa'da 'Tanrının Kırbacı' olarak anıldı. 451'deki Katalaunum Savaşı tarihin en büyük muharebelerinden biridir."),
            ("🏴 Vandalların Akınları", "Vandallar İspanya üzerinden Kuzey Afrika'ya geçti, Kartaca'yı başkent yaptı. 455'te denizden gelerek Roma'yı ikinci kez yağmaladılar. Yıkıcılıkları öylesine ünlüdür ki 'vandalizm' kelimesi onlardan gelir."),
            ("🌍 Avrupa'nın Yeni Haritası", "Franklar Galya'ya yerleşti ve bugünkü Fransa'nın temelini attı. Angıllar ve Saksonlar Britanya'ya geçti. Ostrogotlar İtalya'yı, Vizigotlar İspanya'yı aldı. Modern Avrupa milletlerinin kökeni bu göçlere dayanır."),
        ],
        "video_url": "https://www.youtube.com/embed/hMXaHnIp9TI",
    },
    {
        "id": "romabolunme",
        "baslik": "Roma'nın İkiye Bölünmesi",
        "emoji": "🏛️",
        "tarih": "285 – 395",
        "renk": "#7C2D12",
        "ozet": "Yönetilmesi imkansız hale gelen devasa Roma İmparatorluğu'nun Doğu ve Batı olarak ikiye ayrılması. Tarih sahnesinin en büyük bölünmesi.",
        "seslendirme": "Roma İmparatorluğu'nun ikiye bölünmesi, tarih sahnesinin en önemli olaylarından biridir. İmparatorluk, üçüncü yüzyılda iç savaşlar, ekonomik krizler ve barbar akınlarıyla büyük bir kaos yaşadı. İmparator Diokletianus 285 yılında Tetrarşi sistemini kurarak imparatorluğu dört bölgeye ayırdı. Ancak kalıcı bölünme 395 yılında İmparator Theodosius'un ölümüyle gerçekleşti. Theodosius imparatorluğu iki oğlu arasında paylaştırdı. Batı Roma'nın başkenti Ravenna, Doğu Roma'nın başkenti Konstantinopolis oldu. Doğu Roma yani Bizans İmparatorluğu zengin ve güçlü kalırken, Batı Roma barbar akınları ve ekonomik çöküşle zayıfladı. Bu bölünme Avrupa tarihini kökten etkiledi. Batı karanlık çağa girerken, Doğu bin yıl daha ayakta kaldı. Doğu'da Ortodoks Hristiyanlık, Batı'da Katolik Kilisesi güçlendi ve bu ayrım bugünkü Avrupa kültür haritasının temelini oluşturdu.",
        "bilgi_kartlari": [
            ("📅 Dönem", "285 (Tetrarşi) – 395 (kesin bölünme)"),
            ("📍 Batı Roma", "Başkent: Ravenna/Roma — İtalya, Galya, Britanya, İspanya, Kuzey Afrika"),
            ("📍 Doğu Roma", "Başkent: Konstantinopolis — Anadolu, Balkanlar, Mısır, Suriye"),
            ("👑 Bölünme Kararı", "İmparator Theodosius'un vasiyeti (395)"),
            ("⛪ Dini Ayrışma", "Batı: Katolik Kilisesi — Doğu: Ortodoks Kilisesi"),
            ("⏳ Sonuç", "Batı Roma 476'da yıkıldı, Doğu Roma (Bizans) 1453'e kadar yaşadı"),
        ],
        "detay_kartlari": [
            ("📉 Üçüncü Yüzyıl Krizi (235-284)", "Elli yılda otuzdan fazla imparator gelip geçti. İç savaşlar, veba salgınları, enflasyon ve barbar akınları imparatorluğu çökme noktasına getirdi. Ticaret durdu, şehirler küçüldü."),
            ("👑 Diokletianus ve Tetrarşi (285)", "İmparator Diokletianus devasa imparatorluğu yönetmek için Tetrarşi sistemini kurdu: iki Augustus ve iki Caesar olmak üzere dört yönetici. Bu, bölünmenin ilk adımıydı."),
            ("⚔️ Konstantinopolis'in Kuruluşu (330)", "İmparator Konstantinus, eski Yunan kolonisi Byzantion'u yeniden inşa ederek Yeni Roma olarak adlandırdı. Stratejik konumu sayesinde bin yıl boyunca dünyayı en güçlü şehri oldu."),
            ("📜 Theodosius'un Vasiyeti (395)", "Son birleşik Roma İmparatoru Theodosius ölüm döşeğinde imparatorluğu iki oğluna bıraktı: Honorius Batı'yı, Arcadius Doğu'yu aldı. Bu tarih resmi bölünme olarak kabul edilir."),
            ("🔀 İki Farklı Kader", "Batı Roma zayıflayarak 476'da yıkıldı. Doğu Roma ise Justinianus döneminde parlak bir medeniyet kurdu, Ayasofya'yı inşa etti ve Roma hukukunu derledi. 1453'e kadar bin yıl daha yaşadı."),
        ],
        "video_url": "https://www.youtube.com/embed/IbH5GNGxC3s",
    },
    {
        "id": "batiromaciokusu",
        "baslik": "Batı Roma'nın Yıkılması",
        "emoji": "⚔️",
        "tarih": "410 – 476",
        "renk": "#DC2626",
        "ozet": "Barbar akınları altında çöken Batı Roma İmparatorluğu'nun son günleri. Antik Çağ'ın sonu ve Ortaçağ'ın başlangıcı.",
        "seslendirme": "Batı Roma İmparatorluğu'nun yıkılması, insanlık tarihinin en önemli dönüm noktalarından biridir. Beşinci yüzyılda imparatorluk artık kendini savunamaz hale gelmişti. Ordusu büyük ölçüde barbar paralı askerlerden oluşuyordu. Ekonomi çökmüş, nüfus azalmıştı. 410 yılında Vizigotlar Roma şehrini yağmaladı. 455'te Vandallar ikinci büyük yağmayı gerçekleştirdi. Son onlarca yılda imparatorlar kukla haline geldi, gerçek güç barbar generallerinin elindeydi. 4 Eylül 476'da Germen savaş şefi Odoaker, son Batı Roma İmparatoru Romulus Augustulus'u tahttan indirdi. İmparatorluk tacını Konstantinopolis'e gönderdi. Bu tarih geleneksel olarak Antik Çağ'ın sonu ve Ortaçağ'ın başlangıcı kabul edilir. Batı Roma'nın yıkılmasıyla Avrupa yüzlerce küçük krallığa bölündü, şehirler küçüldü, ticaret durdu ve karanlık çağ denilen dönem başladı.",
        "bilgi_kartlari": [
            ("📅 Dönem", "410 (Roma'nın yağması) – 476 (resmi yıkılış)"),
            ("📍 Başkent", "Ravenna (Roma artık başkent değildi)"),
            ("👑 Son İmparator", "Romulus Augustulus (tahttan indirildi: 4 Eylül 476)"),
            ("⚔️ Yıkıcılar", "Vizigotlar, Vandallar, Ostrogotlar, Germen kabileleri"),
            ("🏛️ Miras", "Roma hukuku, Latin dili, Hristiyanlık yaşamaya devam etti"),
            ("📜 Tarihsel Anlam", "Antik Çağ'ın sonu, Ortaçağ'ın başlangıcı"),
        ],
        "detay_kartlari": [
            ("📉 Çöküşün Nedenleri", "Askeri harcamalar, vergi yükü, nüfus azalması, barbar göçleri, iç savaşlar, salgın hastalıklar ve ahlaki çözülme. Tek bir neden değil, yüzlerce faktörün birleşimi imparatorluğu bitirdi."),
            ("⚔️ Roma'nın Yağmalanması (410 ve 455)", "Vizigot Kralı Alaric 410'da Roma'yı üç gün yağmaladı. 455'te Vandal Kralı Genserik denizden gelerek on dört gün boyunca şehri talan etti. Her iki olay da dünyayı derinden sarstı."),
            ("👑 Kukla İmparatorlar Dönemi", "Son yıllarda gerçek güç Ricimer, Gundobad gibi barbar generallerinin elindeydi. İmparatorlar sadece birer figürandı. Ordu tamamen barbar paralı askerlerden oluşuyordu."),
            ("🏴 Odoaker ve Son Gün (476)", "Germen savaş şefi Odoaker, askerlerine toprak dağıtılmasını istedi. Reddedilince ayaklandı ve son imparator Romulus Augustulus'u tahttan indirdi. İmparatorluk tacını Doğu Roma'ya gönderdi."),
            ("🌍 Yıkılışın Sonuçları", "Avrupa siyasi birliğini kaybetti. Yüzlerce küçük krallık ortaya çıktı. Şehir nüfusu düştü, ticaret durdu, okur-yazarlık azaldı. Ancak kilise ve manastırlar Roma kültürünü korudu ve geleceğe taşıdı."),
        ],
        "video_url": "https://www.youtube.com/embed/aPmGDVsNiAM",
    },
    {
        "id": "ortacag",
        "baslik": "Ortaçağ",
        "emoji": "🏰",
        "tarih": "476 – 1453",
        "renk": "#6B4423",
        "ozet": "Roma İmparatorluğu'nun çöküşünden İstanbul'un fethine kadar süren, feodalizm, kilise hakimiyeti ve büyük toplumsal dönüşümlerin yaşandığı bin yıllık dönem.",
        "seslendirme": "Ortaçağ, 476 yılında Batı Roma İmparatorluğu'nun yıkılmasıyla başlayan ve 1453'te İstanbul'un fethiyle sona eren yaklaşık bin yıllık bir dönemdir. Bu dönem Erken, Yüksek ve Geç Ortaçağ olmak üzere üç ana bölüme ayrılır. Erken Ortaçağ'da kavimler göçü Avrupa'yı alt üst etti, feodal sistem şekillendi ve kilise toplumun merkezi oldu. Yüksek Ortaçağ'da şehirler büyüdü, ticaret canlandı, üniversiteler kuruldu ve gotik katedraller yükseldi. Geç Ortaçağ'da ise Kara Veba Avrupa nüfusunun üçte birini yok etti, Yüzyıl Savaşları yaşandı ve feodal düzen çökmeye başladı. Ortaçağ Avrupa'sında kilise muazzam bir güce sahipti. Papa, krallardan bile güçlüydü. Manastırlar bilginin korunduğu merkezlerdi. İslam dünyası ise bu dönemde bilim, matematik, tıp ve felsefede altın çağını yaşadı. İbn-i Sina, Harezmi, Biruni gibi bilginler dünyayı aydınlattı. Osmanlı İmparatorluğu'nun kuruluşu ve yükselişi de Ortaçağ'ın son dönemine denk gelir.",
        "bilgi_kartlari": [
            ("📅 Dönem", "476 – 1453 (yaklaşık 1000 yıl)"),
            ("📍 Coğrafya", "Avrupa, Orta Doğu, Kuzey Afrika"),
            ("⚔️ Toplumsal Yapı", "Feodalizm: Kral → Senyör → Vassal → Serf"),
            ("⛪ Kilise", "Papa en güçlü otorite; manastırlar bilgi merkezleri"),
            ("🌙 İslam Dünyası", "Bilim ve kültürde Altın Çağ (800-1300)"),
            ("☠️ Kara Veba", "1347-1351, Avrupa nüfusunun %30-60'ını yok etti"),
        ],
        "detay_kartlari": [
            ("🏚️ Erken Ortaçağ (476-1000)", "Kavimler göçü Avrupa'yı karanlığa sürükledi. Gotlar, Vandallar, Hunlar Roma topraklarını istila etti. Frank Kralı Charlemagne kısa süreli bir birlik sağladı. Vikinglerin akınları kıyı bölgelerini tehdit etti. Feodal sistem ve manoryal düzen şekillendi."),
            ("🏰 Yüksek Ortaçağ (1000-1300)", "Tarımda ilerleme nüfusu artırdı. Şehirler büyüdü, lonca sistemi kuruldu. İlk üniversiteler Bologna, Paris ve Oxford'da açıldı. Gotik mimari doruğa ulaştı; Notre-Dame, Chartres katedralleri inşa edildi. Magna Carta 1215'te imzalandı."),
            ("☠️ Kara Veba (1347-1351)", "Asya'dan gelen veba salgını Avrupa nüfusunun üçte birini öldürdü. Toplumsal düzen alt üst oldu. İşgücü kıtlığı serfliğin çözülmesini hızlandırdı. Kiliseye güven sarsıldı."),
            ("🌙 İslam Altın Çağı", "İbn-i Sina tıpta, Harezmi matematikte, İbn Haldun tarih felsefesinde çığır açtı. Bağdat, Kurtuba, Kahire dünyanın en büyük kültür merkezleriydi. Cebir, algoritma, optik ve kimya alanlarında temel eserler yazıldı."),
            ("🇹🇷 Osmanlı'nın Kuruluşu (1299)", "Osman Bey liderliğinde Söğüt'te kurulan beylik, hızla büyüyerek imparatorluğa dönüştü. 1453'te İstanbul'un fethi ile Ortaçağ sona erdi ve Yeniçağ başladı."),
        ],
        "video_url": "https://www.youtube.com/embed/rNCw2MOfnLQ",
    },
    {
        "id": "hacliseferleri",
        "baslik": "Haçlı Seferleri",
        "emoji": "⚔️",
        "tarih": "1096 – 1291",
        "renk": "#B91C1C",
        "ozet": "Avrupa'nın Hristiyan krallıklarının Kudüs ve Kutsal Toprakları Müslümanlardan geri almak amacıyla düzenlediği askeri seferler serisi.",
        "seslendirme": "Haçlı Seferleri, 1096 ile 1291 yılları arasında Avrupa'daki Hristiyan krallıkların Kudüs ve Kutsal Toprakları ele geçirmek için düzenledikleri büyük askeri seferlerdir. İlk Haçlı Seferi 1096'da Papa II. Urbanus'un çağrısıyla başladı ve 1099'da Kudüs'ün fethedilmesiyle sonuçlandı. Toplam sekiz büyük sefer düzenlendi. Bu seferler Doğu ile Batı arasında kültürel, ticari ve bilimsel etkileşimi hızlandırdı. Avrupa'ya pusula, barut, kağıt yapımı ve yeni tarım teknikleri getirildi. Haçlı Seferleri sonucunda feodal sistem zayıfladı, ticaret canlandı ve şehirler büyüdü. Arap dünyasının bilimsel birikimi Avrupa'ya aktarılarak Rönesans'ın temellerini oluşturdu.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1096 – 1291 (yaklaşık 200 yıl)"),
            ("📍 Bölge", "Anadolu, Suriye, Filistin, Mısır"),
            ("👑 Önemli Liderler", "Aslan Yürekli Richard, Selahaddin Eyyubi, Godfrey de Bouillon"),
            ("⚔️ Sefer Sayısı", "8 büyük sefer + çok sayıda küçük sefer"),
            ("📜 Neden", "Kudüs'ün ve Kutsal Toprakların geri alınması"),
            ("🏰 Sonuç", "Kudüs geçici olarak Hristiyan kontrolüne girdi, ancak Müslümanlar geri aldı"),
        ],
        "detay_kartlari": [
            ("🏰 1. Haçlı Seferi (1096-1099)", "Papa II. Urbanus'un çağrısıyla başladı. Kudüs fethedildi ve Haçlı devletleri kuruldu. Halk Haçlı Seferi ile başlayan kaotik süreç, düzenli orduların katılımıyla dönüştü."),
            ("⚔️ 2. Haçlı Seferi (1147-1149)", "Edessa Kontluğu'nun düşmesi üzerine düzenlendi. Fransa Kralı VII. Louis ve Almanya Kralı III. Konrad liderlik etti ama başarısız oldu."),
            ("🌟 3. Haçlı Seferi (1189-1192)", "Selahaddin Eyyubi'nin Kudüs'ü alması üzerine başladı. Aslan Yürekli Richard ile Selahaddin arasındaki efsanevi mücadele yaşandı."),
            ("📦 4. Haçlı Seferi (1202-1204)", "Amacından saparak Konstantinopolis'i (İstanbul) yağmaladı. Bizans İmparatorluğu büyük darbe aldı."),
            ("🌍 Kültürel Etki", "Doğu-Batı ticareti canlandı; baharat, ipek, pusula, barut ve kağıt Avrupa'ya tanıtıldı. Üniversiteler ve hastaneler kuruldu."),
        ],
        "video_url": "https://www.youtube.com/embed/HIs5B2U7US0",
    },
    {
        "id": "istanbulunfethi",
        "baslik": "İstanbul'un Fethi",
        "emoji": "🇹🇷",
        "tarih": "29 Mayıs 1453",
        "renk": "#B91C1C",
        "ozet": "Sultan II. Mehmed'in Konstantinopolis'i fethederek bin yıllık Bizans İmparatorluğu'na son vermesi. Ortaçağ'ın bitişi, Yeniçağ'ın başlangıcı.",
        "seslendirme": "İstanbul'un Fethi, 29 Mayıs 1453'te Sultan İkinci Mehmed'in Konstantinopolis'i ele geçirmesiyle gerçekleşen ve dünya tarihinin akışını değiştiren bir olaydır. Yirmi bir yaşındaki genç padişah, bin yıllık Bizans İmparatorluğu'nun başkentini fethetmeyi hayatının en büyük hedefi olarak belirledi. Fetih hazırlıkları devasa ölçekteydi. Rumeli Hisarı Boğaz'ın en dar yerinde inşa edildi. Macar mühendis Urban'a dönemin en büyük topları döktürüldü. İki yüz bin kişilik ordu ve büyük bir donanma hazırlandı. Kuşatma elli üç gün sürdü. Konstantinopolis'in devasa surları Şahi toplarıyla dövüldü. En kritik hamle gemilerin karadan Haliç'e indirilmesiydi. Yetmiş iki gemi, Kasımpaşa sırtlarından yağlanmış kızaklarla Haliç'e taşındı. Bu dahi strateji Bizans'ın savunma planlarını çökertti. 29 Mayıs sabahı genel hücum başladı ve şehir düştü. Son Bizans İmparatoru on birinci Konstantinos surlar üzerinde savaşarak öldü. Fetih, Ortaçağ'ı sona erdirdi ve Yeniçağ'ı başlattı. İstanbul, Osmanlı İmparatorluğu'nun başkenti olarak dünya tarihinin en önemli şehirlerinden biri olmaya devam etti. Sultan Mehmed Fatih unvanını aldı ve şehri yeniden imar ederek bir dünya başkentine dönüştürdü.",
        "bilgi_kartlari": [
            ("📅 Tarih", "29 Mayıs 1453 (Salı günü)"),
            ("👑 Fatih", "Sultan II. Mehmed (21 yaşında)"),
            ("🏰 Hedef", "Konstantinopolis — Bizans İmparatorluğu'nun başkenti"),
            ("⚔️ Kuşatma", "53 gün (6 Nisan – 29 Mayıs 1453)"),
            ("💥 Şahi Topu", "8 metre uzunluk, 600 kg gülle, 1.5 km menzil"),
            ("🚢 Gemiler Karadan", "72 gemi kızaklarla Haliç'e indirildi"),
        ],
        "detay_kartlari": [
            ("🏗️ Rumeli Hisarı (1452)", "Fetih hazırlığının ilk adımı olarak Boğaz'ın en dar yerinde dört ayda inşa edildi. Anadolu Hisarı ile birlikte Boğaz trafiği kontrol altına alındı. Bizans'a denizden yardım gelmesi engellendi."),
            ("💥 Şahi Topları", "Macar mühendis Urban'a döktürülen devasa toplar surları dövdü. Şahi topu 600 kilogramlık gülleler fırlatıyordu. Topların geri tepmesi o kadar şiddetliydi ki günde ancak yedi atış yapılabiliyordu."),
            ("🚢 Gemilerin Karadan Yürütülmesi", "Haliç zincirle kapatılınca Fatih dahi bir plan uyguladı. Kasımpaşa sırtlarından yağlanmış kızaklar döşendi ve yetmiş iki gemi bir gecede karadan Haliç'e indirildi. Bizans şok oldu."),
            ("⚔️ Son Hücum — 29 Mayıs", "Gece yarısından itibaren üç dalga halinde hücum başladı. Önce azaplar, sonra Anadolu askerleri, en son yeniçeriler. Sabaha karşı Ulubatlı Hasan surlara bayrağı dikti. Şehir düştü."),
            ("🌍 Dünya Tarihine Etkisi", "Ortaçağ sona erdi, Yeniçağ başladı. Ticaret yolları değişti ve Coğrafi Keşifler hızlandı. Fatih, şehri imar etti; cami, medrese, hamam ve çarşılar inşa ederek İstanbul'u dünya başkentine dönüştürdü."),
        ],
        "video_url": "https://www.youtube.com/embed/kMHjxAjmSMo",
    },
    {
        "id": "cografikesifler",
        "baslik": "Coğrafi Keşifler",
        "emoji": "🧭",
        "tarih": "1415 – 1600",
        "renk": "#0369A1",
        "ozet": "Avrupalı denizcilerin yeni deniz yolları ve kıtalar keşfederek dünya haritasını yeniden çizdiği çağ.",
        "seslendirme": "Coğrafi Keşifler, 15. ve 16. yüzyıllarda Avrupalı denizcilerin yeni deniz yolları ve kıtalar keşfettiği dönemdir. Portekiz Prensi Henri'nin himayesinde başlayan keşif seferleri, Bartolomeu Dias'ın Ümit Burnu'nu geçmesi, Vasco da Gama'nın Hindistan'a ulaşması ve Kristof Kolomb'un Amerika kıtasına varmasıyla zirveye ulaştı. Macellan'ın filosu dünyayı dolaşan ilk sefer oldu. Bu keşifler, dünya ticaretini kökten değiştirdi. Yeni kıtalardan altın, gümüş, tütün, patates ve domates Avrupa'ya geldi. Ancak keşifler aynı zamanda sömürgeciliğin başlangıcını, yerli halkların yok edilmesini ve köle ticaretinin yaygınlaşmasını da beraberinde getirdi. Coğrafi Keşifler dünya tarihinin en önemli dönüm noktalarından biridir.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1415 – 1600 (yaklaşık 185 yıl)"),
            ("📍 Keşfedilen Yerler", "Amerika, Hint Deniz Yolu, Pasifik, Afrika kıyıları"),
            ("🧭 Öncü Ülkeler", "Portekiz ve İspanya"),
            ("⛵ Ünlü Kaşifler", "Kolomb, Vasco da Gama, Macellan, Dias, Piri Reis"),
            ("💰 Ekonomik Etki", "Dünya ticareti kökten değişti; sömürgecilik başladı"),
            ("🌽 Kolomb Değişimi", "Patates, domates, tütün, kakao Avrupa'ya; buğday, at, sığır Amerika'ya"),
        ],
        "detay_kartlari": [
            ("🇵🇹 Portekiz Kesifleri", "Prens Henri'nin Sagres'teki denizcilik okulu ile başladı. Bartolomeu Dias 1488'de Ümit Burnu'nu geçti. Vasco da Gama 1498'de Hindistan'a ulaştı."),
            ("🇪🇸 Kolomb ve Amerika (1492)", "İspanya Kraliçesi Isabella'nın desteğiyle yola çıkan Kristof Kolomb, Hindistan yerine Bahama Adaları'na ulaştı. 4 sefer düzenledi."),
            ("🌏 Macellan Seferi (1519-1522)", "Ferdinand Macellan dünyayı dolaşma seferine çıktı. Kendisi Filipinler'de öldürüldü ama gemisi El Cano komutasında dünyayı dolaştı."),
            ("🗺️ Piri Reis Haritası (1513)", "Osmanlı denizcisi Piri Reis, dünya haritası çizdi. Amerika kıyılarını gösteren bu harita, dönemin en doğru haritalarından biriydi."),
            ("⚠️ Karanlık Yüzü", "Yerli halkların toprakları ellerinden alındı, milyonlarca insan hastalık ve savaştan öldü. Afrika'dan Amerika'ya köle ticareti başladı."),
        ],
        "video_url": "https://www.youtube.com/embed/wOclF9eP5uM",
    },
    {
        "id": "ronesans",
        "baslik": "Rönesans ve Reform",
        "emoji": "🎨",
        "tarih": "1400 – 1600",
        "renk": "#7C3AED",
        "ozet": "Antik Yunan ve Roma kültürünün yeniden doğuşu ile bilim, sanat ve düşüncede büyük atılımların yaşandığı dönem.",
        "seslendirme": "Rönesans, 14. yüzyılda İtalya'da başlayarak tüm Avrupa'ya yayılan kültürel, sanatsal ve entelektüel bir yeniden doğuş hareketidir. Antik Yunan ve Roma medeniyetlerinin eserleri yeniden keşfedildi. Leonardo da Vinci, Michelangelo, Raphael gibi sanatçılar başyapıtlarını üretti. Bilimde Kopernik güneş merkezli evren modelini öne sürdü, Galileo teleskopu kullandı. Matbaanın icadı bilginin hızla yayılmasını sağladı. Reform hareketi ise Martin Luther'in 1517'de 95 tezini kilise kapısına asmasıyla başladı. Katolik Kilisesi'nin yozlaşmasına karşı çıkan Luther, Protestanlık mezhebinin doğuşuna yol açtı. Reform hareketi Avrupa'da din savaşlarına neden oldu ancak düşünce özgürlüğünün temellerini attı. Rönesans ve Reform birlikte modern dünya düşüncesinin temellerini oluşturdu.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1400 – 1600 (yaklaşık 200 yıl)"),
            ("📍 Başlangıç", "İtalya (Floransa, Roma, Venedik)"),
            ("🎨 Sanat Devleri", "Leonardo da Vinci, Michelangelo, Raphael, Botticelli"),
            ("🔬 Bilim Öncüleri", "Kopernik, Galileo, Kepler, Gutenberg"),
            ("⛪ Reform Liderleri", "Martin Luther, Jean Calvin, Zwingli"),
            ("📖 Matbaa", "Gutenberg 1440'ta hareketli harfli matbaayı icat etti"),
        ],
        "detay_kartlari": [
            ("🎨 Sanat Devrimi", "Perspektif, anatomi ve ışık-gölge teknikleri geliştirildi. Da Vinci'nin Mona Lisa'sı, Michelangelo'nun Sistine Şapeli tavanı, Raphael'in Atina Okulu eseri bu dönemin simgeleridir."),
            ("🔬 Bilimsel Devrim", "Kopernik güneş merkezli evren modelini ortaya koydu. Galileo teleskopu kullanarak Jupiter'in uydularını keşfetti. Bilimsel yöntem şekillenmeye başladı."),
            ("📖 Matbaanın Etkisi", "Gutenberg'in 1440'taki icadı, kitapların çoğaltılmasını ucuz ve hızlı hale getirdi. Bilgi artık sadece kilisenin tekelinde değildi."),
            ("⛪ Martin Luther (1517)", "95 tezini Wittenberg Kilisesi'ne asarak endüljans satışını ve kilisenin yozlaşmasını eleştirdi. Protestanlık mezhebinin doğuşuna yol açtı."),
            ("🌍 Hümanizm", "İnsanı merkeze alan düşünce sistemi. Erasmus, Machiavelli, Thomas More gibi düşünürler bu akımın öncüleri oldu."),
        ],
        "video_url": "https://www.youtube.com/embed/fI1OeMmwYjU",
    },
    {
        "id": "endustridevrimi",
        "baslik": "Endüstri Devrimi",
        "emoji": "🏭",
        "tarih": "1760 – 1840",
        "renk": "#CBD5E1",
        "ozet": "Buhar makinesi, fabrikalaşma ve seri üretimin başlamasıyla insanlık tarihinin en büyük ekonomik ve toplumsal dönüşümü.",
        "seslendirme": "Endüstri Devrimi, 18. yüzyılın ortalarında İngiltere'de başlayan ve tüm dünyayı etkileyen köklü bir dönüşüm sürecidir. James Watt'ın buhar makinesini geliştirmesi, fabrikaların kurulması ve seri üretimin başlaması bu devrimin temel taşlarıdır. Tekstil sanayi ilk etkilenen sektör oldu. Spinning Jenny ve mekanik dokuma tezgahları üretimi katladı. Demiryolları ve buharlı gemiler ulaşımı devrimleştirdi. Kırsal nüfus fabrikalara akarak şehirleşme hızlandı. İşçi sınıfı doğdu, sendikalar kuruldu. Çocuk işçiliği ve ağır çalışma koşulları ciddi toplumsal sorunlar yarattı. Endüstri Devrimi modern kapitalizmin, işçi haklarının ve teknolojik ilerlemenin temellerini attı. İkinci sanayi devrimi ise elektrik, çelik ve petrol ile devam etti.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1760 – 1840 (1. Dalga), 1870 – 1914 (2. Dalga)"),
            ("📍 Başlangıç", "İngiltere (Manchester, Birmingham)"),
            ("⚙️ Temel İcatlar", "Buhar makinesi, Spinning Jenny, Demiryolu"),
            ("🏭 Fabrikalaşma", "El işçiliğinden makine üretimine geçiş"),
            ("🚂 Ulaşım Devrimi", "Demiryolları, buharlı gemiler"),
            ("👷 Toplumsal Etki", "İşçi sınıfı, sendikalar, şehirleşme"),
        ],
        "detay_kartlari": [
            ("💨 Buhar Makinesi", "Thomas Newcomen'in ilk modelini James Watt geliştirdi. Fabrikaları, trenleri ve gemileri çalıştıran güç kaynağı oldu."),
            ("🧵 Tekstil Devrimi", "John Kay'in uçan mekiği, Hargreaves'in Spinning Jenny'si ve Arkwright'ın su gücüyle çalışan iplik makinesı üretimi katladı."),
            ("🚂 Demiryolu Çağı", "George Stephenson 1825'te ilk yolcu trenini çalıştırdı. Demiryolları hammadde taşımacılığını ve ticareti devrimleştirdi."),
            ("🏙️ Şehirleşme", "Köylerden fabrikalara göç başladı. Londra, Manchester gibi şehirler hızla büyüdü. Hijyen ve konut sorunları ortaya çıktı."),
            ("⚖️ İşçi Hakları", "12-16 saat çalışma, çocuk işçiliği, düşük ücretler. Sendikalaşma ve işçi hareketleri bu dönemde başladı."),
        ],
        "video_url": "https://www.youtube.com/embed/zjK7PWycRyI",
    },
    {
        "id": "fransizihtilali",
        "baslik": "Fransız İhtilali",
        "emoji": "🇫🇷",
        "tarih": "1789 – 1799",
        "renk": "#1D4ED8",
        "ozet": "Monarşinin yıkılması, cumhuriyetin ilanı ve insan hakları bildirgesiyle modern demokrasinin temellerinin atıldığı devrim.",
        "seslendirme": "Fransız İhtilali, 1789 yılında Fransa'da patlak veren ve tüm dünyayı etkileyen büyük bir devrimdir. Halkın açlık, eşitsizlik ve monarşinin baskısına karşı ayaklanmasıyla başladı. 14 Temmuz 1789'da Bastille Hapishanesi'nin basılması devrimin sembolik başlangıcı oldu. İnsan ve Yurttaş Hakları Bildirisi ilan edildi. Özgürlük, eşitlik ve kardeşlik sloganları tüm dünyaya yayıldı. Kral XVI. Louis ve Kraliçe Marie Antoinette giyotinle idam edildi. Devrim sürecinde Jakoben terörü yaşandı, binlerce kişi idam edildi. Sonunda Napolyon Bonapart iktidara geldi. Fransız İhtilali, monarşileri sarsan, ulus devlet kavramını doğuran ve demokratik hakların temelini atan tarihin en etkili devrimidir.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1789 – 1799 (10 yıl)"),
            ("📍 Yer", "Fransa (Paris merkez)"),
            ("🏛️ Nedenleri", "Mali kriz, eşitsizlik, aydınlanma düşüncesi"),
            ("📜 Bildirge", "İnsan ve Yurttaş Hakları Bildirisi (1789)"),
            ("⚖️ Slogan", "Liberté, Égalité, Fraternité (Özgürlük, Eşitlik, Kardeşlik)"),
            ("👑 Sonuç", "Monarşi yıkıldı, Cumhuriyet ilan edildi"),
        ],
        "detay_kartlari": [
            ("🏰 Bastille Baskını (14 Temmuz 1789)", "Paris halkı silah deposu olan Bastille Hapishanesi'ni bastı. Bu olay devrimin başlangıcı kabul edilir ve bugün Fransa'nın milli bayramıdır."),
            ("📜 İnsan Hakları Bildirisi", "26 Ağustos 1789'da ilan edildi. Tüm insanların özgür ve eşit doğduğunu, egemenliğin millete ait olduğunu ve düşünce özgürlüğünü ilan etti."),
            ("⚡ Terör Dönemi (1793-1794)", "Robespierre liderliğindeki Jakobenlerin yönetimi. Giyotin ile 16.000'den fazla kişi idam edildi. Robespierre de sonunda aynı akıbete uğradı."),
            ("👑 Kral ve Kraliçenin İdamı", "Kral XVI. Louis 21 Ocak 1793'te, Kraliçe Marie Antoinette 16 Ekim 1793'te giyotinle idam edildi."),
            ("🌍 Dünya Üzerindeki Etkisi", "Ulus devlet kavramı doğdu. Osmanlı'da Tanzimat, Latin Amerika'da bağımsızlık hareketleri bu devrimin etkisiyle başladı."),
        ],
        "video_url": "https://www.youtube.com/embed/5vL_5EILRCA",
    },
    {
        "id": "dunya1",
        "baslik": "1. Dünya Savaşı",
        "emoji": "💣",
        "tarih": "1914 – 1918",
        "renk": "#991B1B",
        "ozet": "İmparatorlukların çöküşü, yeni silah teknolojileri ve milyonlarca insanın hayatını kaybettiği ilk küresel savaş.",
        "seslendirme": "Birinci Dünya Savaşı, 1914-1918 yılları arasında yaşanan ve dünya tarihini kökten değiştiren ilk büyük küresel çatışmadır. Avusturya-Macaristan Veliahtı Franz Ferdinand'ın Saraybosna'da suikaste uğraması savaşı tetikledi. İttifak Devletleri ve İtilaf Devletleri olmak üzere iki blok oluştu. Siper savaşları, kimyasal silahlar, tanklar ve uçaklar ilk kez kullanıldı. Batı Cephesi'nde Verdun ve Somme muharebeleri milyonlarca can aldı. Osmanlı İmparatorluğu Çanakkale'de İtilaf güçlerini durdurdu ama sonunda yenildi. Savaş sonunda dört büyük imparatorluk çöktü: Osmanlı, Avusturya-Macaristan, Almanya ve Rusya. Versailles Antlaşması Almanya'ya ağır koşullar dayattı ve bu durum İkinci Dünya Savaşı'nın tohumlarını ekti.",
        "bilgi_kartlari": [
            ("📅 Dönem", "28 Temmuz 1914 – 11 Kasım 1918"),
            ("💀 Kayıp", "17 milyon ölü, 20 milyon yaralı"),
            ("⚔️ Taraflar", "İtilaf (İngiltere, Fransa, Rusya) vs İttifak (Almanya, Avusturya-Macaristan, Osmanlı)"),
            ("🔫 Yeni Silahlar", "Tank, kimyasal gaz, uçak, denizaltı"),
            ("🏰 Çanakkale", "Osmanlı'nın İtilaf güçlerini durduğu efsanevi savunma"),
            ("📜 Sonuç", "Versailles Antlaşması, 4 imparatorluğun çöküşü"),
        ],
        "detay_kartlari": [
            ("🎯 Savaşın Tetikleyicisi", "28 Haziran 1914'te Avusturya-Macaristan Veliahtı Franz Ferdinand, Saraybosna'da Gavrilo Princip tarafından öldürüldü. İttifaklar sistemi zincirleme savaş ilanlarına yol açtı."),
            ("🏳️ Siper Savaşları", "Batı Cephesi'nde yüzlerce kilometre siper kazıldı. Askerler çamur, soğuk ve hastalıklarla mücadele etti. Metrelerce ilerleme için binlerce asker hayatını kaybetti."),
            ("🇹🇷 Çanakkale Savaşı (1915)", "İtilaf güçlerinin İstanbul'u ele geçirme planı Çanakkale'de durduruldu. Mustafa Kemal'in liderliğinde Türk askerleri efsanevi bir savunma sergiledi."),
            ("🇺🇸 ABD'nin Savaşa Girmesi (1917)", "Almanya'nın sınırsız denizaltı savaşı ve Zimmermann Telgrafı ABD'yi savaşa soktu. Bu, savaşın kaderini değiştirdi."),
            ("📜 Versailles Antlaşması (1919)", "Almanya'ya çok ağır koşullar dayatıldı: toprak kayıpları, silahsızlanma, devasa tazminatlar. Bu koşullar 2. Dünya Savaşı'nın temellerini attı."),
        ],
        "video_url": "https://www.youtube.com/embed/dHSQAEam2yc",
    },
    {
        "id": "dunya2",
        "baslik": "2. Dünya Savaşı",
        "emoji": "🌍",
        "tarih": "1939 – 1945",
        "renk": "#1F2937",
        "ozet": "İnsanlık tarihinin en yıkıcı savaşı; Holokost, atom bombası ve modern dünya düzeninin şekillendiği dönem.",
        "seslendirme": "İkinci Dünya Savaşı, 1939-1945 yılları arasında yaşanan, insanlık tarihinin en yıkıcı çatışmasıdır. Hitler'in Nazi Almanyası'nın Polonya'yı işgal etmesiyle başladı. Mihver devletleri Almanya, İtalya ve Japonya; Müttefik güçler İngiltere, Sovyetler Birliği, ABD ve Fransa olarak karşı karşıya geldi. Holokost sırasında altı milyon Yahudi sistematik olarak katledildi. Stalingrad Muharebesi savaşın dönüm noktası oldu. 6 Haziran 1944'te Normandiya çıkarması ile müttefikler Avrupa'yı kurtarmaya başladı. ABD, Ağustos 1945'te Hiroşima ve Nagazaki'ye atom bombası atarak Japonya'yı teslim olmaya zorladı. Savaş 70-85 milyon insanın ölümüyle sonuçlandı. Birleşmiş Milletler kuruldu, Soğuk Savaş dönemi başladı ve dünya iki kutuplu bir yapıya bölündü.",
        "bilgi_kartlari": [
            ("📅 Dönem", "1 Eylül 1939 – 2 Eylül 1945"),
            ("💀 Kayıp", "70-85 milyon ölü (sivillerin çoğunluğu)"),
            ("⚔️ Taraflar", "Müttefikler (ABD, İngiltere, SSCB) vs Mihver (Almanya, İtalya, Japonya)"),
            ("☠️ Holokost", "6 milyon Yahudi sistematik olarak katledildi"),
            ("💥 Atom Bombası", "Hiroşima (6 Ağustos) ve Nagazaki (9 Ağustos 1945)"),
            ("🏛️ Sonuç", "BM kuruldu, Soğuk Savaş başladı, sömürgecilik çöktü"),
        ],
        "detay_kartlari": [
            ("🇩🇪 Hitler'in Yükselişi", "1933'te iktidara gelen Adolf Hitler, Versailles Antlaşması'nı reddetti, silahlandı ve yayılmacı politika izledi. 1 Eylül 1939'da Polonya'yı işgal etti."),
            ("⚡ Yıldırım Savaşı (Blitzkrieg)", "Alman ordusu tank ve hava gücünü birleştiren Blitzkrieg taktiğiyle Fransa'yı 6 haftada düşürdü. İngiltere yalnız kaldı."),
            ("🏔️ Stalingrad (1942-1943)", "Savaşın dönüm noktası. Alman 6. Ordusu Sovyet kuşatmasında imha edildi. 2 milyon asker hayatını kaybetti."),
            ("🏖️ Normandiya Çıkarması (D-Day)", "6 Haziran 1944'te 156.000 müttefik askeri Fransa kıyılarına çıktı. Tarihin en büyük amfibi operasyonuydu."),
            ("☢️ Atom Bombası ve Savaşın Sonu", "ABD, Japonya'ya iki atom bombası attı. 200.000'den fazla kişi hayatını kaybetti. 2 Eylül 1945'te Japonya teslim oldu."),
        ],
        "video_url": "https://www.youtube.com/embed/HUqy-OQvVtI",
    },
    {
        "id": "kurtulusavasi",
        "baslik": "Kurtuluş Savaşı",
        "emoji": "🇹🇷",
        "tarih": "1919 – 1923",
        "renk": "#DC2626",
        "ozet": "Mustafa Kemal Atatürk önderliğinde işgalci güçlere karşı verilen bağımsızlık mücadelesi. Osmanlı'nın küllerinden modern Türkiye Cumhuriyeti'nin doğuşu.",
        "seslendirme": "Kurtuluş Savaşı, 1919 ile 1923 yılları arasında Mustafa Kemal Atatürk önderliğinde Türk milletinin bağımsızlığı için verdiği destansı mücadeledir. Birinci Dünya Savaşı'nın ardından imzalanan Mondros Ateşkes Antlaşması ile Osmanlı İmparatorluğu fiilen çökmüştü. İtilaf devletleri Anadolu'yu işgal etmeye başladı. Yunanistan İzmir'e çıkarma yaptı, Fransa güneydoğuyu, İtalya Antalya bölgesini, İngiltere İstanbul ve Boğazları kontrol altına aldı. On dokuz Mayıs 1919'da Mustafa Kemal Samsun'a çıkarak milli mücadeleyi başlattı. Erzurum ve Sivas kongreleri ile ulusal direniş örgütlendi. Yirmi üç Nisan 1920'de Ankara'da Türkiye Büyük Millet Meclisi açıldı. İnönü muharebeleri savunma hatlarını güçlendirdi. Sakarya Meydan Muharebesi savaşın dönüm noktası oldu. Mustafa Kemal Başkomutanlık Meydan Muharebesi ile Büyük Taarruz'u başlattı. Türk ordusu otuz Ağustos 1922'de kesin zafer kazandı. Düşman kuvvetleri dokuz Eylül'de İzmir'den denize döküldü. On bir Ekim 1922'de Mudanya Ateşkes Antlaşması imzalandı. Yirmi dört Temmuz 1923'te Lozan Barış Antlaşması ile Türkiye'nin bağımsızlığı tüm dünyaya kabul ettirildi. Yirmi dokuz Ekim 1923'te Cumhuriyet ilan edildi ve Mustafa Kemal Atatürk ilk Cumhurbaşkanı seçildi.",
        "bilgi_kartlari": [
            ("📅 Dönem", "19 Mayıs 1919 – 29 Ekim 1923"),
            ("👑 Önder", "Mustafa Kemal Atatürk (Başkomutan)"),
            ("⚔️ Düşmanlar", "Yunanistan, İngiltere, Fransa, İtalya, Ermenistan"),
            ("🏛️ Meclis", "TBMM — 23 Nisan 1920, Ankara"),
            ("🗓️ Zafer", "30 Ağustos 1922 — Başkomutanlık Meydan Muharebesi"),
            ("📜 Sonuç", "Lozan Antlaşması (24 Temmuz 1923) + Cumhuriyet ilanı (29 Ekim 1923)"),
        ],
        "detay_kartlari": [
            ("🚢 Samsun'a Çıkış — 19 Mayıs 1919", "Mustafa Kemal, 9. Ordu Müfettişi olarak Bandırma vapuruyla Samsun'a çıktı. Görevi bölgedeki asayişi sağlamaktı ama asıl amacı milli mücadeleyi örgütlemekti. Bu tarih Türk bağımsızlık hareketinin başlangıcıdır."),
            ("📜 Kongreler Dönemi (1919)", "Erzurum Kongresi'nde milli sınırlar çizildi ve işgale karşı direnme kararı alındı. Sivas Kongresi'nde tüm direniş cemiyetleri Anadolu ve Rumeli Müdafaa-i Hukuk Cemiyeti altında birleştirildi. Milli irade ortaya kondu."),
            ("⚔️ İnönü Muharebeleri (1921)", "Birinci ve İkinci İnönü muharebeleri Yunan ilerleyişini durdurdu. İsmet Paşa komutasındaki Türk kuvvetleri büyük bir savunma başarısı gösterdi. Bu zaferler milli morali yükseltti ve TBMM hükümetine uluslararası meşruiyet kazandırdı."),
            ("🏔️ Sakarya Meydan Muharebesi (1921)", "Yirmi iki gün yirmi iki gece süren Sakarya Muharebesi savaşın dönüm noktasıydı. Mustafa Kemal'in 'Hattı müdafaa yoktur, sathı müdafaa vardır. O satıh bütün vatandır' emri tarihe geçti. Zafer sonrası Mustafa Kemal'e Gazilik unvanı ve Mareşallik rütbesi verildi."),
            ("🎖️ Büyük Taarruz ve Zafer (1922)", "26 Ağustos 1922'de başlayan Büyük Taarruz, 30 Ağustos'ta Başkomutanlık Meydan Muharebesi ile taçlandı. Düşman ordusu imha edildi. 9 Eylül'de İzmir kurtarıldı. 11 Ekim'de Mudanya Ateşkesi imzalandı. Savaş zaferle bitti."),
        ],
        "video_url": "https://www.youtube.com/embed/BzPLbJN6sOQ",
    },
]


def _build_tarih_timeline_html():
    """Dünya Tarihi zaman çizelgesi — interaktif HTML."""
    periods_js = json.dumps([{
        "id": d["id"], "baslik": d["baslik"], "emoji": d["emoji"],
        "tarih": d["tarih"], "renk": d["renk"], "ozet": d["ozet"]
    } for d in _DUNYA_TARIHI], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);
  color:#e2e8f0;padding:20px;overflow-x:hidden}}
.tl-title{{text-align:center;margin-bottom:24px}}
.tl-title h1{{font-size:1.6rem;background:linear-gradient(135deg,#fbbf24,#f59e0b);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px}}
.tl-title p{{font-size:.82rem;color:#94a3b8}}
.timeline{{position:relative;padding:10px 0}}
.timeline::before{{content:'';position:absolute;left:50%;top:0;bottom:0;width:3px;
  background:linear-gradient(180deg,#fbbf24,#ef4444,#8b5cf6,#3b82f6,#10b981);
  transform:translateX(-50%);border-radius:2px}}
.tl-item{{position:relative;margin:16px 0;display:flex;align-items:center;
  cursor:pointer;transition:all .3s}}
.tl-item:nth-child(odd){{flex-direction:row-reverse}}
.tl-item:nth-child(odd) .tl-card{{margin-left:auto;margin-right:calc(50% + 24px);text-align:right}}
.tl-item:nth-child(even) .tl-card{{margin-right:auto;margin-left:calc(50% + 24px)}}
.tl-dot{{position:absolute;left:50%;transform:translateX(-50%);width:20px;height:20px;
  border-radius:50%;border:3px solid #fbbf24;z-index:2;transition:all .3s;
  box-shadow:0 0 15px rgba(251,191,36,.3)}}
.tl-item:hover .tl-dot{{transform:translateX(-50%) scale(1.3);
  box-shadow:0 0 25px rgba(251,191,36,.6)}}
.tl-card{{width:42%;padding:14px 18px;border-radius:14px;
  background:rgba(30,41,59,.8);border:1px solid rgba(255,255,255,.08);
  backdrop-filter:blur(10px);transition:all .3s}}
.tl-card:hover{{border-color:rgba(251,191,36,.3);transform:translateY(-2px);
  box-shadow:0 8px 25px rgba(0,0,0,.3)}}
.tl-card.active{{border-color:rgba(251,191,36,.6);
  box-shadow:0 0 30px rgba(251,191,36,.15)}}
.tl-emoji{{font-size:1.5rem}}
.tl-date{{font-size:.72rem;color:#fbbf24;font-weight:700;margin:4px 0}}
.tl-name{{font-size:.92rem;font-weight:700;color:#1A2035}}
.tl-desc{{font-size:.76rem;color:#94a3b8;line-height:1.5;margin-top:6px;
  max-height:0;overflow:hidden;transition:max-height .4s ease}}
.tl-card.active .tl-desc{{max-height:200px}}
@media(max-width:600px){{
  .timeline::before{{left:20px}}
  .tl-item,.tl-item:nth-child(odd){{flex-direction:row}}
  .tl-item .tl-card,.tl-item:nth-child(odd) .tl-card{{margin:0 0 0 50px;width:calc(100% - 60px);text-align:left}}
  .tl-dot{{left:20px}}
}}
</style></head><body>
<div class="tl-title">
  <h1>\U0001f3db\ufe0f Dünya Tarihi Zaman Çizelgesi</h1>
  <p>375'ten 1923'e — İnsanlığı Değiştiren 13 Dönem</p>
</div>
<div class="timeline" id="timeline"></div>
<script>
var P={periods_js};
var tl=document.getElementById('timeline');
P.forEach(function(p,i){{
  var item=document.createElement('div');
  item.className='tl-item';
  item.innerHTML='<div class="tl-dot" style="background:'+p.renk+'"></div>'+
    '<div class="tl-card" id="card_'+p.id+'">'+
    '<span class="tl-emoji">'+p.emoji+'</span>'+
    '<div class="tl-date">'+p.tarih+'</div>'+
    '<div class="tl-name">'+p.baslik+'</div>'+
    '<div class="tl-desc">'+p.ozet+'</div></div>';
  item.onclick=function(){{
    document.querySelectorAll('.tl-card').forEach(function(c){{c.classList.remove('active')}});
    document.getElementById('card_'+p.id).classList.add('active');
    // Streamlit'e mesaj gönder
    window.parent.postMessage({{type:'streamlit:setComponentValue',value:i}},'*');
  }};
  tl.appendChild(item);
}});
// İlk kartı aç
setTimeout(function(){{document.getElementById('card_'+P[0].id).classList.add('active')}},300);
</script></body></html>"""


def _build_tarih_audio_html(period_data):
    """Belirli bir tarih dönemi için sesli anlatım HTML'i."""
    import re as _re
    narration = period_data["seslendirme"]
    sentences = [s.strip() for s in _re.split(r'(?<=[.!?])\s+', narration) if s.strip()]
    sentences_js = json.dumps(sentences, ensure_ascii=False)
    color = period_data["renk"]
    baslik = period_data["baslik"]
    emoji = period_data["emoji"]

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:14px 18px}}
.player{{display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:linear-gradient(135deg,#1e293b,#334155);border-radius:14px;
  border:1px solid rgba(255,255,255,.08);margin-bottom:12px}}
.pbtn{{width:46px;height:46px;border-radius:50%;border:none;cursor:pointer;
  background:linear-gradient(135deg,{color},#8b5cf6);color:#fff;font-size:18px;
  display:flex;align-items:center;justify-content:center;transition:all .2s;
  box-shadow:0 4px 15px rgba(139,92,246,.3);flex-shrink:0}}
.pbtn:hover{{transform:scale(1.08)}}
.pbtn.on{{background:linear-gradient(135deg,#ef4444,#dc2626)}}
.inf{{flex:1;min-width:0}}
.inf .t{{font-size:.85rem;font-weight:700;color:#1A2035}}
.inf .s{{font-size:.73rem;color:#94a3b8;margin-top:2px}}
.bar{{width:100%;height:4px;background:rgba(255,255,255,.08);border-radius:2px;margin-top:6px;overflow:hidden}}
.fill{{height:100%;width:0%;background:linear-gradient(90deg,{color},#8b5cf6);border-radius:2px;transition:width .3s}}
.spd{{padding:3px 8px;border-radius:6px;border:1px solid rgba(255,255,255,.12);
  background:transparent;color:#94a3b8;font-size:.7rem;cursor:pointer;transition:all .2s}}
.spd.act{{background:{color};color:#fff;border-color:{color}}}
.nar{{padding:14px 16px;background:rgba(255,255,255,.03);border-radius:10px;
  border:1px solid rgba(255,255,255,.06);max-height:160px;overflow-y:auto;line-height:1.8}}
.nar::-webkit-scrollbar{{width:3px}}
.nar::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.15);border-radius:2px}}
.sn{{font-size:.8rem;color:#64748b;padding:2px 4px;border-radius:4px;
  transition:all .4s;display:inline}}
.sn.act{{color:#1A2035;background:rgba(139,92,246,.15);font-weight:600}}
.sn.dn{{color:#94a3b8}}
.tm{{font-size:.73rem;color:#64748b;min-width:36px;text-align:right}}
</style></head><body>
<div class="player">
  <button class="pbtn" id="pb" onclick="tog()">&#9654;</button>
  <div class="inf">
    <div class="t">{emoji} {baslik} — Sesli Anlatım</div>
    <div class="s" id="st">Dinlemek için oynat tuşuna basın</div>
    <div class="bar"><div class="fill" id="pf"></div></div>
  </div>
  <div class="tm" id="tt">0:00</div>
  <button class="spd act" id="s1" onclick="spd(1)">1x</button>
  <button class="spd" id="s13" onclick="spd(1.3)">1.3x</button>
  <button class="spd" id="s08" onclick="spd(0.8)">0.8x</button>
</div>
<div class="nar" id="nb"></div>
<script>
var S={sentences_js};
var nb=document.getElementById('nb'),playing=false,paused=false,ci=0,utt=null,t0=0,te=0,rate=1;
S.forEach(function(s,i){{var sp=document.createElement('span');sp.className='sn';sp.id='w'+i;sp.textContent=s+' ';nb.appendChild(sp)}});
var tw=S.join(' ').split(/\\s+/).length;te=Math.round(tw/2.5);
function fmt(sec){{var m=Math.floor(sec/60),s=Math.floor(sec%60);return m+':'+(s<10?'0':'')+s}}
document.getElementById('tt').textContent='0:00 / ~'+fmt(te);
function hl(idx){{S.forEach(function(_,i){{var e=document.getElementById('w'+i);e.className=i<idx?'sn dn':i===idx?'sn act':'sn'}});
  var a=document.getElementById('w'+idx);if(a)a.scrollIntoView({{behavior:'smooth',block:'nearest'}});
  document.getElementById('pf').style.width=Math.min(100,Math.round(idx/S.length*100))+'%'}}
var _cv=null;
var _mN=['ahmet','mehmet','tolga','kerem','murat','male','erkek','man','david'];
var _fN=['emel','yelda','seda','filiz','female','kadin','kadın','woman','zeynep'];
function _isM(n){{var l=n.toLowerCase();return _mN.some(function(m){{return l.indexOf(m)>=0}})}}
function _isF(n){{var l=n.toLowerCase();return _fN.some(function(f){{return l.indexOf(f)>=0}})}}
function _score(v){{var s=0,n=v.name.toLowerCase();if(_isM(v.name))s-=5000;if(n.indexOf('neural')>=0)s+=200;
  if(n.indexOf('online')>=0||n.indexOf('natural')>=0)s+=150;if(_isF(v.name))s+=60;
  if(n.indexOf('microsoft')>=0)s+=40;if(v.lang&&v.lang.indexOf('tr')===0)s+=500;return s}}
function _pick(list){{if(!list||!list.length)return null;var sc=list.map(function(v){{return{{v:v,s:_score(v)}}}});
  sc.sort(function(a,b){{return b.s-a.s}});return sc[0].v}}
function speak(idx){{
  if(idx>=S.length){{playing=false;paused=false;ci=0;
    document.getElementById('pb').innerHTML='&#9654;';document.getElementById('pb').className='pbtn';
    document.getElementById('st').textContent='Anlatım tamamlandı';document.getElementById('pf').style.width='100%';
    S.forEach(function(_,i){{document.getElementById('w'+i).className='sn dn'}});return}}
  ci=idx;hl(idx);utt=new SpeechSynthesisUtterance(S[idx]);utt.lang='tr-TR';utt.rate=rate;utt.volume=1;
  if(_cv){{utt.voice=_cv}}else{{var vs=speechSynthesis.getVoices();
    var tr=vs.filter(function(v){{return v.lang&&v.lang.indexOf('tr')===0}});
    var b=_pick(tr.length>0?tr:vs);if(b){{utt.voice=b;_cv=b}}}}
  if(_cv&&_isM(_cv.name))utt.pitch=1.35;else utt.pitch=1.05;
  utt.onend=function(){{if(playing&&!paused)setTimeout(function(){{if(playing&&!paused)speak(idx+1)}},150)}};
  utt.onerror=function(e){{if(playing&&!paused&&e.error!=='canceled')setTimeout(function(){{if(playing&&!paused)speak(idx+1)}},200)}};
  utt.onstart=function(){{var el=Math.round((Date.now()-t0)/1000);
    document.getElementById('tt').textContent=fmt(el)+' / ~'+fmt(te);
    document.getElementById('st').textContent='Cümle '+(idx+1)+'/'+S.length}};
  if(window._ka)clearInterval(window._ka);
  window._ka=setInterval(function(){{if(speechSynthesis.speaking&&!speechSynthesis.paused){{speechSynthesis.pause();speechSynthesis.resume()}}else clearInterval(window._ka)}},10000);
  speechSynthesis.speak(utt)}}
function tog(){{
  if(!playing){{playing=true;paused=false;t0=Date.now();
    document.getElementById('pb').innerHTML='&#10074;&#10074;';document.getElementById('pb').className='pbtn on';
    document.getElementById('st').textContent='Oynatılıyor...';speechSynthesis.cancel();speak(ci)}}
  else if(!paused){{paused=true;speechSynthesis.pause();
    document.getElementById('pb').innerHTML='&#9654;';document.getElementById('pb').className='pbtn';
    document.getElementById('st').textContent='Duraklatıldı'}}
  else{{paused=false;speechSynthesis.resume();
    document.getElementById('pb').innerHTML='&#10074;&#10074;';document.getElementById('pb').className='pbtn on';
    document.getElementById('st').textContent='Oynatılıyor...'}}}}
function spd(r){{rate=r;document.querySelectorAll('.spd').forEach(function(b){{b.className='spd'}});
  if(r===1)document.getElementById('s1').className='spd act';
  else if(r===1.3)document.getElementById('s13').className='spd act';
  else document.getElementById('s08').className='spd act';
  if(playing&&!paused){{speechSynthesis.cancel();speak(ci)}}}}
function lv(){{var v=speechSynthesis.getVoices();if(v.length>0&&!_cv){{
  var tr=v.filter(function(x){{return x.lang&&x.lang.indexOf('tr')===0}});
  _cv=_pick(tr.length>0?tr:v)}}}}
lv();if(speechSynthesis.onvoiceschanged!==undefined)speechSynthesis.onvoiceschanged=lv;
setTimeout(lv,100);setTimeout(lv,500);
setInterval(function(){{if(playing&&!paused&&t0){{var el=Math.round((Date.now()-t0)/1000);
  document.getElementById('tt').textContent=fmt(el)+' / ~'+fmt(te)}}}},1000);
</script></body></html>"""


def _render_dunya_tarihi_category(store, ci):
    """Dünya Tarihi — 7 dönem tek sayfada, zaman çizelgesi, sesli anlatım, video, bilgi kartları."""
    cat_name, emoji, color, topics = _CATS[ci]
    styled_section(f"{emoji} Dünya Tarihi — İnsanlığı Değiştiren 13 Dönem", "#8B4513")

    # Zaman çizelgesi hero
    components.html(_build_tarih_timeline_html(), height=680, scrolling=True)

    # Dönem seçici
    donem_labels = [f"{d['emoji']} {d['baslik']}" for d in _DUNYA_TARIHI]
    secilen = st.radio(
        "Dönem Seçin", donem_labels,
        horizontal=True, key="tarih_donem_sec",
        label_visibility="collapsed"
    )
    secilen_idx = donem_labels.index(secilen)
    period = _DUNYA_TARIHI[secilen_idx]

    # === SEÇİLEN DÖNEM DETAYI ===
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{period["renk"]}15,{period["renk"]}08);'
        f'border:2px solid {period["renk"]}40;border-radius:16px;padding:20px 24px;margin:16px 0">'
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">'
        f'<span style="font-size:2.2rem">{period["emoji"]}</span>'
        f'<div><div style="font-size:1.3rem;font-weight:800;color:#0f172a">{period["baslik"]}</div>'
        f'<div style="font-size:.85rem;color:{period["renk"]};font-weight:700">{period["tarih"]}</div></div></div>'
        f'<div style="font-size:.9rem;color:#334155;line-height:1.7">{period["ozet"]}</div>'
        f'</div>', unsafe_allow_html=True)

    # Bilgi kartları
    styled_section(f"📋 Temel Bilgiler — {period['baslik']}", period["renk"])
    bk_html = ""
    for i, (key, val) in enumerate(period["bilgi_kartlari"]):
        bg = "#111827" if i % 2 == 0 else "#1A2035"
        bk_html += (
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:12px 18px;background:{bg};border-bottom:1px solid #e2e8f0">'
            f'<span style="font-size:.84rem;font-weight:700;color:#334155">{key}</span>'
            f'<span style="font-size:.84rem;color:#0f172a;font-weight:600;text-align:right;max-width:60%">{val}</span></div>')
    st.markdown(
        f'<div style="border:1px solid #e2e8f0;border-radius:14px;overflow:hidden;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.05)">{bk_html}</div>', unsafe_allow_html=True)

    # Sesli anlatım
    styled_section(f"🎧 Sesli Anlatım — {period['baslik']}", period["renk"])
    components.html(_build_tarih_audio_html(period), height=280, scrolling=False)

    # Detay kartları
    styled_section(f"📚 Detaylı Bilgiler — {period['baslik']}", period["renk"])
    for j, (title, desc) in enumerate(period["detay_kartlari"]):
        colors = ["#2563eb", "#7c3aed", "#0891b2", "#059669", "#d97706"]
        c = colors[j % len(colors)]
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#ffffff,#111827);'
            f'border:1px solid #e2e8f0;border-radius:14px;padding:18px 22px;margin:10px 0;'
            f'border-left:5px solid {c};box-shadow:0 2px 8px rgba(0,0,0,.04)">'
            f'<div style="font-size:.92rem;font-weight:700;color:#0f172a;margin-bottom:8px">{title}</div>'
            f'<div style="font-size:.84rem;color:#475569;line-height:1.7">{desc}</div>'
            f'</div>', unsafe_allow_html=True)

    # Video
    styled_section(f"🎬 Video — {period['baslik']}", period["renk"])
    video_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f172a;padding:12px;border-radius:14px}}
.vw{{position:relative;width:100%;padding-bottom:56.25%;border-radius:12px;overflow:hidden;
  box-shadow:0 8px 25px rgba(0,0,0,.4)}}
.vw iframe{{position:absolute;top:0;left:0;width:100%;height:100%;border:none}}
.vl{{text-align:center;padding:10px;font-family:sans-serif;color:#94a3b8;font-size:.78rem;margin-top:8px}}
</style></head><body>
<div class="vw"><iframe src="{period['video_url']}" allowfullscreen
  allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture"></iframe></div>
<div class="vl">{period['emoji']} {period['baslik']} — Belgesel / Eğitim Videosu</div>
</body></html>"""
    components.html(video_html, height=420, scrolling=False)

    # Diğer dönemler navigasyonu
    st.markdown("---")
    styled_section("🔄 Diğer Dönemler", "#64748b")
    nav_cols = st.columns(len(_DUNYA_TARIHI))
    for ni, nd in enumerate(_DUNYA_TARIHI):
        with nav_cols[ni]:
            if ni != secilen_idx:
                if st.button(f"{nd['emoji']}\n{nd['baslik'][:12]}", key=f"nav_tarih_{ni}",
                             use_container_width=True):
                    st.session_state["tarih_donem_sec"] = donem_labels[ni]
                    st.rerun()
            else:
                st.markdown(
                    f'<div style="text-align:center;padding:8px;background:{nd["renk"]}20;'
                    f'border-radius:10px;border:2px solid {nd["renk"]}">'
                    f'<div style="font-size:1.2rem">{nd["emoji"]}</div>'
                    f'<div style="font-size:.7rem;font-weight:700;color:{nd["renk"]}">{nd["baslik"][:12]}</div>'
                    f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# ci=30  BÜYÜK İMPARATORLUKLAR — 20 İMPARATORLUK
# ══════════════════════════════════════════════════════════════

_IMPARATORLUKLAR = [
    {
        "baslik": "Roma İmparatorluğu", "emoji": "🏛️", "tarih": "MÖ 27 – MS 476",
        "renk": "#991B1B", "bayrak": "🦅",
        "baskent": "Roma → Konstantinopolis",
        "kurucu": "Augustus (Octavianus)",
        "zirve_alan": "5 milyon km²",
        "nufus": "~70 milyon (MS 2. yy)",
        "ozet": "Akdeniz havzasının tamamını kontrol eden, hukuk, mühendislik ve yönetim sistemleriyle tüm Batı medeniyetinin temelini atan tarihın en etkili imparatorluğu.",
        "seslendirme": "Roma İmparatorluğu, tarih sahnesinin en etkili ve uzun ömürlü devletlerinden biridir. Milattan önce yirmi yedi yılında Augustus'un ilk imparator olmasıyla başlayan imparatorluk dönemi, beş yüz yılı aşkın sürdü. Roma, Akdeniz'in tamamını çevreleyen devasa bir imparatorluk kurdu. İspanya'dan Mezopotamya'ya, Britanya'dan Mısır'a kadar uzandı. Roma hukuku bugünkü hukuk sistemlerinin temelidir. Yolları, su kemerleri, amfitiyatroları ve forumları mühendislik harikasıydı. Roma ordusu lejyonlarıyla dünyanın en disiplinli askeri gücüydü. Hristiyanlık Roma'da doğdu ve yayıldı. Pax Romana döneminde iki yüz yıl boyunca barış ve refah hüküm sürdü. Ancak barbar akınları, iç savaşlar ve ekonomik sorunlar imparatorluğu yıktı.",
        "detaylar": [
            ("🦅 Pax Romana", "MÖ 27 – MS 180 arası yaklaşık 200 yıllık barış ve refah dönemi. Ticaret gelişti, nüfus arttı, şehirler büyüdü."),
            ("🏗️ Mühendislik Mirası", "50.000 km yol, su kemerleri, Kolezyum, Pantheon. 'Tüm yollar Roma'ya çıkar' sözü bu dönemden kalma."),
            ("⚖️ Roma Hukuku", "12 Levha Kanunları'ndan Justinianus Kanunları'na kadar gelişen hukuk sistemi tüm modern hukukun temelidir."),
            ("⚔️ Lejyonlar", "5.000-6.000 askerlik lejyonlar dönemin en disiplinli ordu birimiydi. Testudo formasyonu efsaneleşti."),
            ("📉 Çöküş", "3. yüzyıl krizi, barbar göçleri, ekonomik çöküş ve 476'da Batı Roma'nın yıkılması."),
        ],
    },
    {
        "baslik": "Osmanlı İmparatorluğu", "emoji": "☪️", "tarih": "1299 – 1922",
        "renk": "#DC2626", "bayrak": "🇹🇷",
        "baskent": "Söğüt → Bursa → Edirne → İstanbul",
        "kurucu": "Osman Gazi",
        "zirve_alan": "5.2 milyon km²",
        "nufus": "~35 milyon (17. yy)",
        "ozet": "Altı yüz yılı aşkın hüküm süren, üç kıtaya yayılan, İstanbul'u fetheden ve İslam dünyasının liderliğini üstlenen süper güç.",
        "seslendirme": "Osmanlı İmparatorluğu, 1299 yılında Osman Gazi tarafından küçük bir beylik olarak kuruldu ve altı yüz yılı aşkın süre hüküm sürdü. Fatih Sultan Mehmed 1453'te İstanbul'u fethederek imparatorluğu dünya gücü haline getirdi. Kanuni Sultan Süleyman döneminde imparatorluk zirvesine ulaştı. Üç kıtaya yayılan topraklar Viyana kapılarından Basra Körfezi'ne, Kuzey Afrika'dan Kafkasya'ya uzanıyordu. Osmanlı millet sistemiyle farklı din ve etnisitelerden halkları bir arada yönetmeyi başardı. Devşirme sistemi, tımar düzeni ve kapıkulu ordusu eşsiz yönetim mekanizmalarıydı. Mimar Sinan'ın eserleri, Osmanlı hat sanatı ve minyatürleri büyük bir kültürel miras bıraktı. On dokuzuncu yüzyılda Tanzimat reformlarıyla modernleşme çabası başladı ancak imparatorluk Birinci Dünya Savaşı'nın ardından 1922'de sona erdi.",
        "detaylar": [
            ("🏰 Kuruluş (1299)", "Osman Gazi'nin Söğüt'teki beyliği hızla büyüdü. Orhan Gazi Bursa'yı aldı, 1. Murad Edirne'yi fethederek Avrupa'ya geçti."),
            ("⚔️ İstanbul'un Fethi (1453)", "Fatih Sultan Mehmed 21 yaşında Konstantinopolis'i fethetti. Ortaçağ sona erdi, Osmanlı dünya gücü oldu."),
            ("👑 Kanuni Dönemi (1520-1566)", "46 yıllık saltanat. Mohaç, Rodos, Bağdat seferleri. Hukuk reformları. İmparatorluk en geniş sınırlarına ulaştı."),
            ("🕌 Mimar Sinan", "Selimiye, Süleymaniye, Şehzade camileri. 400'den fazla eser. Osmanlı mimarisini zirveye taşıdı."),
            ("📉 Duraklama ve Çöküş", "Karlofça (1699) ile toprak kayıpları başladı. Tanzimat, Meşrutiyet denemeleri yetersiz kaldı. 1. Dünya Savaşı sonrası imparatorluk sona erdi."),
        ],
    },
    {
        "baslik": "Moğol İmparatorluğu", "emoji": "🏹", "tarih": "1206 – 1368",
        "renk": "#1E40AF", "bayrak": "🐎",
        "baskent": "Karakurum → Hanbalık (Pekin)",
        "kurucu": "Cengiz Han",
        "zirve_alan": "24 milyon km² (tarihın en büyüğü)",
        "nufus": "~110 milyon",
        "ozet": "Cengiz Han'ın kurduğu, tarihın en geniş topraklara sahip imparatorluğu. Çin'den Avrupa kapılarına kadar uzanan devasa bir dünya gücü.",
        "seslendirme": "Moğol İmparatorluğu, 1206 yılında Cengiz Han tarafından kurulan ve tarihin en geniş kara imparatorluğu unvanını taşıyan devasa bir güçtür. Yirmi dört milyon kilometrekarelik topraklarıyla Pasifik Okyanusu'ndan Doğu Avrupa'ya kadar uzanıyordu. Cengiz Han dağınık Moğol kabilelerini birleştirdi ve müthiş bir askeri makine yarattı. Moğol süvarileri günde yüz kilometre yol kat edebiliyordu. Harezm, Çin ve Rusya'yı fethettiler. Bağdat'ı yıktılar. Ancak Moğollar sadece yıkım getirmedi. İpek Yolu'nu güvenli hale getirerek Doğu-Batı ticaretini canlandırdılar. Posta sistemi Yam ağını kurdular. Dinsel hoşgörü politikası uyguladılar. Cengiz Han'ın torunu Kubilay Han Çin'de Yuan hanedanlığını kurdu.",
        "detaylar": [
            ("🐎 Cengiz Han (1162-1227)", "Temuçin adıyla doğdu, Moğol kabilelerini birleştirip 'evrensel hükümdar' Cengiz Han unvanını aldı."),
            ("⚔️ Fetihler", "Harezm, Jin Çin, Song Çin, Abbasiler, Rusya, Polonya ve Macaristan'a kadar ulaştı."),
            ("🛣️ Pax Mongolica", "İpek Yolu güvenli hale geldi. Marco Polo bu dönemde Çin'e seyahat etti."),
            ("📮 Yam Sistemi", "Binlerce kilometre uzanan posta ve haberleşme ağı. Haberciler günde 300 km mesafe kat edebiliyordu."),
            ("🔀 Parçalanma", "Cengiz Han'ın ölümünden sonra Altın Orda, Çağatay, İlhanlı ve Yuan olarak dörde ayrıldı."),
        ],
    },
    {
        "baslik": "Britanya İmparatorluğu", "emoji": "🇬🇧", "tarih": "1583 – 1997",
        "renk": "#1E3A5F", "bayrak": "🇬🇧",
        "baskent": "Londra",
        "kurucu": "I. Elizabeth dönemi başlangıç",
        "zirve_alan": "35.5 milyon km² (tarihın en genişi)",
        "nufus": "~530 milyon (1938)",
        "ozet": "Güneş batmayan imparatorluk. Dünya kara yüzeyinin dörtte birini kontrol eden, modern dünya düzenini şekillendiren sömürge imparatorluğu.",
        "seslendirme": "Britanya İmparatorluğu, tarihin en geniş topraklara yayılmış sömürge imparatorluğudur. Otuz beş buçuk milyon kilometrekarelik alanıyla dünya kara yüzeyinin dörtte birini kontrol ediyordu. Güneş batmayan imparatorluk olarak anılırdı çünkü her zaman diliminde İngiliz toprağı vardı. On altıncı yüzyılda denizaşırı kolonilerle başlayan yayılma, on dokuzuncu yüzyılda zirvesine ulaştı. Hindistan imparatorluğun en değerli kolonisiydi. Kuzey Amerika, Avustralya, Afrika'nın büyük bölümü ve sayısız ada İngiliz kontrolündeydi. İngilizce dünya dili haline geldi. Parlamenter demokrasi, ortak hukuk sistemi ve serbest ticaret anlayışı dünyaya yayıldı. Ancak sömürgecilik aynı zamanda sömürü, kölelik ve kültürel yıkım anlamına da geldi. İkinci Dünya Savaşı sonrası sömürge halkları bağımsızlıklarını kazandı. 1997'de Hong Kong'un Çin'e devriyle imparatorluk resmen sona erdi.",
        "detaylar": [
            ("⛵ Deniz Hakimiyeti", "İspanyol Armadası'nın yenilmesi (1588) ile başlayan deniz üstünlüğü yüzyıllarca sürdü. Kraliyet Donanması dünyanın en güçlü filosuydu."),
            ("🇮🇳 Hindistan (1757-1947)", "Doğu Hindistan Şirketi ile başlayan kontrol, Kraliçe Victoria'nın Hindistan İmparatoriçesi ilan edilmesiyle taçlandı."),
            ("🌍 Afrika'nın Paylaşımı", "19. yy sonlarında Afrika'nın büyük bölümü İngiliz kontrolüne girdi. Mısır, Sudan, Kenya, Güney Afrika, Nijerya."),
            ("🗽 Amerika Kolonileri", "13 koloni 1776'da bağımsızlığını ilan etti. Bu kayıp İngiltere'yi Asya ve Afrika'ya yöneltti."),
            ("📉 Sömürgesizleşme", "2. Dünya Savaşı sonrası Hindistan, Pakistan, Afrika ülkeleri bağımsızlığını kazandı. 1997'de Hong Kong devriyle dönem kapandı."),
        ],
    },
    {
        "baslik": "Pers İmparatorluğu", "emoji": "🦁", "tarih": "MÖ 550 – MÖ 330",
        "renk": "#B45309", "bayrak": "🏺",
        "baskent": "Persepolis / Susa",
        "kurucu": "Büyük Kiros (Kyros)",
        "zirve_alan": "5.5 milyon km²",
        "nufus": "~50 milyon (antik dünyanın %44'ü)",
        "ozet": "Büyük Kiros'un kurduğu ilk dünya imparatorluğu. İnsan hakları, hoşgörü ve modern yönetim anlayışının öncüsü Akamenid İmparatorluğu.",
        "seslendirme": "Pers İmparatorluğu ya da Akamenid İmparatorluğu, milattan önce beş yüz elli yılında Büyük Kiros tarafından kurulan dünyanın ilk gerçek süper gücüdür. Antik dünyanın nüfusunun neredeyse yarısını yönetiyordu. Mısır'dan Hindistan'a kadar uzanan toprakları vardı. Büyük Kiros insan haklarının öncüsü olarak kabul edilir. Kiros Silindiri tarihin ilk insan hakları belgesi sayılır. Fethettiği halklara din ve kültür özgürlüğü tanıdı. Babil'deki Yahudileri serbest bıraktı. Darius döneminde Kral Yolu inşa edildi. İki bin altı yüz kilometrelik bu yolda haberciler bir haftada mesafe kat edebiliyordu. Persepolis görkemli bir törensel başkent olarak inşa edildi. Pers İmparatorluğu milattan önce üç yüz otuz yılında Büyük İskender'in fetihlerine boyun eğdi.",
        "detaylar": [
            ("👑 Büyük Kiros (MÖ 559-530)", "Medleri, Lidya'yı ve Babil'i fethetti. Hoşgörü politikasıyla halkların sevgisini kazandı."),
            ("📜 Kiros Silindiri", "MÖ 539'da yazılan kil tablet — tarihin ilk insan hakları belgesi kabul edilir."),
            ("🏛️ Persepolis", "Darius tarafından inşa ettirilen törensel başkent. 23 farklı halkın temsilcileri burada hediyeler sunardı."),
            ("🛣️ Kral Yolu", "Susa'dan Sardes'e 2.600 km uzunluğunda yol. Posta sistemi ile 7 günde haberleşme sağlanırdı."),
            ("⚔️ Yunan Savaşları", "Maraton, Termopilai, Salamis. Pers-Yunan savaşları antik tarihin en ünlü çatışmalarıdır."),
        ],
    },
    {
        "baslik": "Bizans İmparatorluğu", "emoji": "☦️", "tarih": "395 – 1453",
        "renk": "#7C3AED", "bayrak": "🏛️",
        "baskent": "Konstantinopolis (İstanbul)",
        "kurucu": "İmparator Arcadius (bölünme) / Konstantinus (şehir)",
        "zirve_alan": "3.5 milyon km² (Justinianus dönemi)",
        "nufus": "~26 milyon",
        "ozet": "Doğu Roma olarak bin yıl ayakta kalan, Antik Yunan-Roma mirasını koruyan ve Ortodoks Hristiyanlığın kalesi olan imparatorluk.",
        "seslendirme": "Bizans İmparatorluğu, Roma İmparatorluğu'nun doğu yarısı olarak bin yılı aşkın süre varlığını sürdürmüştür. Başkenti Konstantinopolis, yani bugünkü İstanbul, ortaçağ dünyasının en büyük ve en zengin şehriydi. Justinianus döneminde imparatorluk en geniş sınırlarına ulaştı. Ayasofya bu dönemde inşa edildi ve bin yıl boyunca dünyanın en büyük katedrali olarak kaldı. Bizans, Antik Yunan ve Roma kültürünü koruyarak Rönesans'a ilham verdi. Roma hukuku Bizans'ta derlendi ve bugünkü hukuk sistemlerinin temeli oldu. Rum Ateşi denilen gizli silah deniz savaşlarında rakipsiz üstünlük sağladı. Ancak Haçlı Seferleri ve Osmanlı'nın yükselişiyle zayıflayan imparatorluk, 1453'te İstanbul'un fethiyle sona erdi.",
        "detaylar": [
            ("🏛️ Konstantinopolis", "Stratejik konumuyla hem Asya hem Avrupa'yı kontrol eden dünyanın en zengin şehri. Surları yüzyıllarca aşılamadı."),
            ("⛪ Ayasofya (537)", "Justinianus döneminde inşa edilen başyapıt. 1.000 yıl dünyanın en büyük katedrali olarak kaldı."),
            ("⚖️ Justinianus Kanunları", "Roma hukuku derlenerek Corpus Juris Civilis oluşturuldu. Tüm modern hukuk sistemlerinin kaynağı."),
            ("🔥 Rum Ateşi", "Denizde bile yanan gizli silah. Formülü bugün bile tam olarak bilinmiyor. Deniz savaşlarında mutlak üstünlük sağladı."),
            ("📉 Çöküş", "4. Haçlı Seferi (1204) büyük darbe vurdu. Osmanlı kuşatmaları sürdü. 1453'te Fatih İstanbul'u fethetti."),
        ],
    },
    {
        "baslik": "Büyük İskender", "emoji": "⚔️", "tarih": "MÖ 336 – MÖ 323",
        "renk": "#0369A1", "bayrak": "🏺",
        "baskent": "Pella → Babil",
        "kurucu": "Büyük İskender (III. Aleksandros)",
        "zirve_alan": "5.2 milyon km²",
        "nufus": "~50 milyon",
        "ozet": "13 yılda Yunanistan'dan Hindistan'a kadar fetihler yapan askeri dahi. Hellenistik çağı başlatan ve Doğu-Batı kültürlerini birleştiren efsanevi komutan.",
        "seslendirme": "Büyük İskender, tarih sahnesinin en parlak askeri dehalarından biridir. Makedonya Kralı olarak yirmi yaşında tahta çıktı ve sadece on üç yıl içinde bilinen dünyanın büyük bölümünü fethetti. Persepolis'i aldı, Mısır'da İskenderiye şehrini kurdu, Hindistan'ın kapılarına dayandı. Hiçbir muharebede yenilmedi. Granikos, Issos ve Gaugamela muharebeleri askeri strateji tarihinin en parlak örnekleridir. İskender sadece bir fatih değil, aynı zamanda bir vizyonerdi. Fethettiği topraklarda Yunan kültürünü yaydı, yerel kültürlerle harmanladı ve Hellenistik çağı başlattı. Otuz iki yaşında Babil'de gizemli bir şekilde hayatını kaybetti. Ölümünden sonra imparatorluğu generalleri arasında paylaşıldı ve üç yüz yıl sürecek Hellenistik krallıklar dönemi başladı.",
        "detaylar": [
            ("👑 Gençlik ve Eğitim", "Babası II. Filip'in yanında askeri eğitim, Aristoteles'ten felsefe dersleri aldı. 16 yaşında babasının yokluğunda isyanı bastırdı."),
            ("⚔️ Pers Seferi", "MÖ 334'te 40.000 askerle Asya'ya geçti. Granikos, Issos, Gaugamela'da Pers ordularını yendi. Darius'u kaçmaya zorladı."),
            ("🏙️ İskenderiye", "Mısır'da kurduğu şehir antik dünyanın en büyük kütüphanesine ve deniz fenerine ev sahipliği yaptı."),
            ("🇮🇳 Hindistan Seferi", "MÖ 326'da Hydaspes'te Kral Porus'u yendi. Askerleri daha ileri gitmek istemeyince geri döndü."),
            ("💀 Gizemli Ölüm (MÖ 323)", "32 yaşında Babil'de öldü. Zehirlenme, sıtma veya aşırı içki nedenleri tartışılır."),
        ],
    },
    {
        "baslik": "Han Hanedanlığı", "emoji": "🐉", "tarih": "MÖ 206 – MS 220",
        "renk": "#B91C1C", "bayrak": "🇨🇳",
        "baskent": "Chang'an (Xi'an) / Luoyang",
        "kurucu": "Liu Bang (Gaozu İmparatoru)",
        "zirve_alan": "6.5 milyon km²",
        "nufus": "~60 milyon",
        "ozet": "Çin'in altın çağı. İpek Yolu'nu açan, kağıdı icat eden, Çin kültürünün temellerini atan dört yüz yıllık imparatorluk.",
        "seslendirme": "Han Hanedanlığı, Çin tarihinin en parlak dönemlerinden biridir ve dört yüz yılı aşkın süre hüküm sürmüştür. Liu Bang adında bir köylü, Qin hanedanlığını devirip milattan önce iki yüz altı yılında Han hanedanlığını kurdu. Han dönemi Çin kültürünün altın çağıydı. İpek Yolu bu dönemde açıldı ve Çin ipeği Roma'ya kadar ulaştı. Kağıt icat edildi, pusula geliştirildi. Konfüçyüsçülük devlet ideolojisi haline geldi. İmparatorluk sınav sistemiyle devlet memurları seçildi, bu sistem yüzyıllarca devam etti. Han döneminde Çin nüfusu altmış milyonu aştı ve dünyanın en kalabalık devleti oldu. Bugün Çin halkının çoğunluğunu oluşturan etnik grubun adı Han Çinlileri olarak bu hanedanlıktan gelmektedir.",
        "detaylar": [
            ("🛣️ İpek Yolu", "Zhang Qian'ın MÖ 138'deki keşif seferiyle başlayan ticaret ağı, Çin'i Roma'ya bağladı."),
            ("📜 Kağıdın İcadı", "Cai Lun MS 105'te kağıt üretim yöntemini geliştirdi. Bu icat insanlık tarihini değiştirdi."),
            ("📚 Konfüçyüsçülük", "Devlet ideolojisi olarak benimsendi. Memurluk sınavları ile yeteneğe dayalı yönetim kuruldu."),
            ("⚔️ Xiongnu Savaşları", "Kuzey sınırlarındaki göçebe Xiongnu tehdidine karşı Çin Seddi genişletildi ve askeri seferler düzenlendi."),
            ("🔬 Bilim ve Teknoloji", "Deprem ölçer, pusula, çelik üretimi, akupunktur geliştirildi."),
        ],
    },
    {
        "baslik": "Rus İmparatorluğu", "emoji": "🇷🇺", "tarih": "1721 – 1917",
        "renk": "#1E3A5F", "bayrak": "🇷🇺",
        "baskent": "Sankt Petersburg / Moskova",
        "kurucu": "I. Petro (Büyük Petro)",
        "zirve_alan": "22.8 milyon km²",
        "nufus": "~176 milyon (1914)",
        "ozet": "Dünyanın en geniş topraklı devleti. Büyük Petro'nun modernleşme hamleleriyle Avrupa'nın büyük güçleri arasına giren dev imparatorluk.",
        "seslendirme": "Rus İmparatorluğu, 1721'de Büyük Petro'nun ilan ettiği ve 1917 Bolşevik Devrimi'ne kadar varlığını sürdüren devasa bir imparatorluktur. Yirmi iki milyon kilometrekareyi aşan topraklarıyla Doğu Avrupa'dan Pasifik Okyanusu'na kadar uzanıyordu. Büyük Petro Rusya'yı modernleştirmek için radikal reformlar yaptı. Batılı tarzda ordu ve donanma kurdu, Sankt Petersburg şehrini inşa ettirdi. İkinci Katerina döneminde topraklar daha da genişledi ve kültürel gelişme zirveye çıktı. On dokuzuncu yüzyılda Rus edebiyatı Tolstoy, Dostoyevski ve Çehov ile dünya edebiyatının zirvesine çıktı. Ancak serflik sistemi, otokrasi ve modernleşme başarısızlıkları devasa sorunlar yarattı. 1917'de Bolşevik Devrimi imparatorluğu yıktı ve Sovyetler Birliği kuruldu.",
        "detaylar": [
            ("👑 Büyük Petro (1682-1725)", "Avrupa'ya gizli seyahat etti, gemi yapımı öğrendi. Orduyu modernleştirdi, Sankt Petersburg'u kurdu."),
            ("👸 II. Katerina (1762-1796)", "Kırım'ı aldı, Polonya'yı paylaştırdı. Aydınlanma fikirlerini benimsedi, sanat ve kültürü destekledi."),
            ("🗺️ Sibirya'nın Fethi", "Kozaklar ve kâşifler Pasifik'e kadar ilerleyerek dünyanın en geniş topraklı devletini oluşturdu."),
            ("⚔️ Napolyon Savaşı (1812)", "Napolyon'un Rusya seferi felaketle sonuçlandı. 600.000 askerden sadece 27.000'i geri dönebildi."),
            ("💥 1917 Devrimi", "Birinci Dünya Savaşı yenilgileri, açlık ve otokrasi devrime yol açtı. Çar tahttan indirildi, Bolşevikler iktidara geldi."),
        ],
    },
    {
        "baslik": "İspanya İmparatorluğu", "emoji": "🇪🇸", "tarih": "1492 – 1898",
        "renk": "#DC2626", "bayrak": "🇪🇸",
        "baskent": "Madrid",
        "kurucu": "Katolik Krallar (Fernando ve Isabella)",
        "zirve_alan": "13.7 milyon km²",
        "nufus": "~60 milyon (sömürgeler dahil)",
        "ozet": "Kolomb'un keşifleriyle başlayan, Amerika'nın altın ve gümüşüyle zenginleşen, ilk küresel sömürge imparatorluğu.",
        "seslendirme": "İspanya İmparatorluğu, Kolomb'un 1492'de Amerika'yı keşfetmesiyle başlayan ve dört yüz yıl süren ilk küresel sömürge imparatorluğudur. On altıncı yüzyılda İspanya dünyanın en güçlü devletiydi. Aztek ve İnka imparatorlukları fethedildi. Amerika'dan akan altın ve gümüş İspanya'yı zengin etti. Filip İkinci döneminde güneşin batmadığı imparatorluk unvanı kullanıldı. İspanyol Armadası dünyanın en büyük donanmasıydı. Ancak 1588'de İngilizlere yenilmesiyle gerileme başladı. Latin Amerika'da İspanyolca ve Katoliklik köklü şekilde yerleşti. On dokuzuncu yüzyılda sömürge halkları bağımsızlıklarını kazandı. 1898'de İspanya-ABD Savaşı ile son sömürgeler kaybedildi.",
        "detaylar": [
            ("🌎 Kolomb ve Keşifler (1492)", "Kristof Kolomb'un seferleriyle başlayan keşif çağı İspanya'yı küresel güç yaptı."),
            ("⚔️ Konkistadorlar", "Hernán Cortés Aztekleri, Francisco Pizarro İnkaları fethetti. Milyonlarca yerli hastalık ve savaştan öldü."),
            ("💰 Altın ve Gümüş", "Potosí gümüş madenleri ve Amerika'nın zenginlikleri İspanya'ya aktı."),
            ("🚢 İspanyol Armadası (1588)", "130 gemilik dev donanma İngiltere'yi istila etmeye çalıştı ama fırtına ve İngiliz taktikleriyle yenildi."),
            ("📉 Gerileme", "Latin Amerika bağımsızlık hareketleri (Bolívar, San Martín) ve 1898 ABD savaşı imparatorluğu sona erdirdi."),
        ],
    },
    {
        "baslik": "Abbasi Halifeliği", "emoji": "☪️", "tarih": "750 – 1258",
        "renk": "#1F2937", "bayrak": "🕌",
        "baskent": "Bağdat",
        "kurucu": "Ebu'l-Abbas es-Seffah",
        "zirve_alan": "11.1 milyon km²",
        "nufus": "~50 milyon",
        "ozet": "İslam Altın Çağı'nın mimarı. Bağdat'ı dünyanın bilim ve kültür merkezi yapan, matematik, tıp ve felsefede çığır açan halifelik.",
        "seslendirme": "Abbasi Halifeliği, 750 yılında Emevi hanedanlığını devirerek kurulan ve İslam medeniyetinin altın çağını yaşatan büyük bir imparatorluktur. Bağdat şehri halifeliğin göz kamaştırıcı başkenti olarak inşa edildi ve dönemin en büyük şehri haline geldi. Beytül Hikme yani Bilgelik Evi adlı kurumda Yunan, Hint ve Pers eserleri Arapçaya çevrildi. Harezmi cebiri kurdu, İbn-i Sina tıpta devrim yaptı, İbn Haldun sosyolojinin temellerini attı. Sıfır ve ondalık sayı sistemi İslam dünyası aracılığıyla Avrupa'ya ulaştı. Abbasi döneminde hastaneler, üniversiteler, kütüphaneler ve rasathaneler kuruldu. Ancak 1258'de Moğol lideri Hülagü Bağdat'ı yıktı, halife öldürüldü ve altın çağ sona erdi.",
        "detaylar": [
            ("🏙️ Bağdat'ın Kuruluşu (762)", "Halife Mansur tarafından Dicle kıyısında yuvarlak şehir olarak inşa edildi. Bir milyon nüfusuyla dünyanın en büyük şehriydi."),
            ("📚 Beytül Hikme", "Bilgelik Evi'nde Yunan, Hint ve Pers eserleri tercüme edildi. Aristo, Platon, Öklid Arapçaya çevrildi."),
            ("🔢 Harezmi ve Cebir", "El-Harezmi'nin El-Kitab adlı eseri cebir bilimini kurdu. 'Algoritma' kelimesi onun adından gelir."),
            ("⚕️ İbn-i Sina (980-1037)", "El-Kanun fi't-Tıb eseri 600 yıl boyunca Avrupa'da tıp kitabı olarak okutuldu."),
            ("💥 Bağdat'ın Yıkılışı (1258)", "Moğol Hülagü Han Bağdat'ı kuşattı, yüz binlerce kişi katledildi, kütüphaneler yakıldı. Dicle mürekkeple siyaha döndü."),
        ],
    },
    {
        "baslik": "Emevi Halifeliği", "emoji": "🌙", "tarih": "661 – 750",
        "renk": "#15803D", "bayrak": "☪️",
        "baskent": "Şam",
        "kurucu": "Muaviye bin Ebu Süfyan",
        "zirve_alan": "11.1 milyon km²",
        "nufus": "~62 milyon (dünya nüfusunun %30'u)",
        "ozet": "İslam tarihinin en geniş topraklara sahip devleti. İspanya'dan Orta Asya'ya uzanan, İslam mimarisinin temellerini atan halifelik.",
        "seslendirme": "Emevi Halifeliği, 661 yılında Muaviye'nin halifeliği ele geçirmesiyle kurulan ve İslam dünyasının en geniş sınırlarına ulaşmasını sağlayan imparatorluktur. Başkenti Şam olan halifelik, batıda İspanya'dan doğuda Orta Asya ve Hindistan sınırlarına kadar uzanıyordu. Dünya nüfusunun yaklaşık yüzde otuzunu yönetiyorlardı. Emeviler döneminde İslam coğrafyası iki katına çıktı. Tarık bin Ziyad 711'de İspanya'yı fethetti ve Endülüs medeniyeti başladı. Şam'daki Emevi Camii İslam mimarisinin ilk büyük başyapıtı oldu. Arapça resmi devlet dili ilan edildi. Posta ve para sistemi düzenlendi. Ancak Arap olmayan Müslümanlara karşı ayrımcılık politikası hoşnutsuzluk yarattı ve 750'de Abbasiler tarafından devrildi.",
        "detaylar": [
            ("👑 Kuruluş", "Hz. Ali'nin şehadetinden sonra Muaviye hilafeti ele geçirdi. Hilafet seçimden hanedanlığa dönüştü."),
            ("🇪🇸 Endülüs Fethi (711)", "Tarık bin Ziyad Cebelitarık Boğazı'nı geçerek İspanya'yı fethetti. Endülüs 800 yıl İslam medeniyetinin parçası oldu."),
            ("🕌 Emevi Camii (Şam)", "İslam mimarisinin ilk büyük başyapıtı. Altın mozaiklerle süslü dev cami bugün hâlâ ayakta."),
            ("🌍 Genişleme", "Kuzey Afrika, İspanya, Orta Asya, Sind (Pakistan). Tarihin en hızlı yayılan imparatorluklarından biri."),
            ("📉 Devrilme (750)", "Arap olmayan Müslümanların hoşnutsuzluğu, Abbasi devrimi ile sonuçlandı. Emevi ailesi katledildi, sadece Abdurrahman İspanya'ya kaçtı."),
        ],
    },
    {
        "baslik": "Antik Mısır", "emoji": "🏺", "tarih": "MÖ 3100 – MÖ 30",
        "renk": "#D97706", "bayrak": "☀️",
        "baskent": "Memphis → Teb → İskenderiye",
        "kurucu": "Kral Menes (Narmer)",
        "zirve_alan": "1 milyon km²",
        "nufus": "~5 milyon",
        "ozet": "Piramitler, firavunlar, hiyeroglif ve mumyalama sanatıyla insanlık tarihinin en gizemli ve en uzun ömürlü medeniyeti.",
        "seslendirme": "Antik Mısır, üç bin yılı aşan tarihiyle insanlık medeniyetinin en uzun ömürlü uygarlıklarından biridir. Nil Nehri'nin bereketli vadisinde doğan bu medeniyet piramitler, sfenksler ve tapınaklarıyla hâlâ hayranlık uyandırmaktadır. Firavunlar tanrı-kral olarak kabul edilirdi. Keops Piramidi antik dünyanın yedi harikasından günümüze ulaşan tek yapıdır. Mısırlılar hiyeroglif yazısını, güneş takvimini ve onluk sayı sistemini geliştirdi. Mumyalama sanatı, ölümden sonra yaşam inancının ürünüydü. Tıpta cerrahiyi ilk uygulayan medeniyetlerden biriydi. Hatşepsut tarihin ilk kadın firavunu olarak yirmi iki yıl ülkeyi yönetti. Ramses İkinci en güçlü firavun olarak anılır. Antik Mısır medeniyeti milattan önce otuz yılında Roma'nın eline geçmesiyle sona erdi.",
        "detaylar": [
            ("🔺 Piramitler", "Keops, Kefren, Mikerinos piramitleri MÖ 2500 civarında inşa edildi. Keops Piramidi 146 metre yüksekliğinde, 2.3 milyon taş bloktan oluşur."),
            ("📜 Hiyeroglif", "700'den fazla sembolden oluşan yazı sistemi. 1799'da bulunan Rosetta Taşı sayesinde çözüldü."),
            ("⚱️ Mumyalama", "Ölümsüzlük inancıyla geliştirilen karmaşık mumyalama süreci 70 gün sürerdi. İç organlar ayrı kavanozlarda saklanırdı."),
            ("👸 Kleopatra (MÖ 69-30)", "Son firavun. Julius Caesar ve Marcus Antonius ile ittifakları efsaneleşti. Roma'nın Mısır'ı ilhakıyla dönem kapandı."),
            ("🔬 Bilim Mirası", "365 günlük takvim, cerrahi aletler, geometri ve sulama sistemleri geliştirdiler."),
        ],
    },
    {
        "baslik": "Selçuklu İmparatorluğu", "emoji": "🏹", "tarih": "1037 – 1194",
        "renk": "#0891B2", "bayrak": "☪️",
        "baskent": "Nişabur → Rey → İsfahan",
        "kurucu": "Tuğrul Bey",
        "zirve_alan": "3.9 milyon km²",
        "nufus": "~20 milyon",
        "ozet": "Malazgirt zaferiyle Anadolu'nun kapılarını Türklere açan, Türk-İslam kültürünün temellerini atan büyük Oğuz Türk imparatorluğu.",
        "seslendirme": "Büyük Selçuklu İmparatorluğu, Oğuz Türklerinin kurduğu ve İslam dünyasının koruyuculuğunu üstlenen güçlü bir devlettir. 1037'de Tuğrul Bey liderliğinde kurulan imparatorluk, kısa sürede İran, Irak, Suriye ve Anadolu'ya hakim oldu. 1071'deki Malazgirt Muharebesi Türk tarihinin en önemli zaferlerinden biridir. Sultan Alparslan'ın Bizans İmparatoru Romen Diyojen'i yenilgiye uğratmasıyla Anadolu'nun kapıları Türklere açıldı. Selçuklular Nizamiye medreselerini kurarak İslam eğitim sisteminin temellerini attı. Vezir Nizamülmülk'ün Siyasetname'si yönetim sanatının başyapıtı olarak kabul edilir. İmam Gazali bu dönemde yaşamış ve İslam düşüncesini derinden etkilemiştir. Selçuklu mirası Osmanlı İmparatorluğu'na aktarıldı.",
        "detaylar": [
            ("⚔️ Malazgirt (1071)", "Sultan Alparslan 200.000 kişilik Bizans ordusunu yendi. Anadolu'nun Türk yurdu olmasının başlangıcı."),
            ("📚 Nizamiye Medreseleri", "Bağdat, İsfahan, Nişabur'da kurulan üniversiteler. Modern üniversite sisteminin öncüsü."),
            ("📖 Nizamülmülk", "Siyasetname eseriyle devlet yönetim sanatını kaleme aldı. İslam dünyasının en ünlü veziri."),
            ("🕌 İmam Gazali", "İhya'u Ulûmi'd-Din eseriyle İslam düşüncesini yeniden şekillendirdi."),
            ("🔀 Parçalanma", "Sultan Melikşah'ın ölümünden sonra taht kavgaları başladı. Anadolu Selçuklu, Kirman, Suriye kollarına ayrıldı."),
        ],
    },
    {
        "baslik": "Timur İmparatorluğu", "emoji": "⚔️", "tarih": "1370 – 1507",
        "renk": "#4C1D95", "bayrak": "🏹",
        "baskent": "Semerkant",
        "kurucu": "Timur (Aksak Timur / Tamerlane)",
        "zirve_alan": "4.4 milyon km²",
        "nufus": "~35 milyon",
        "ozet": "Cengiz Han'ın mirasını canlandırmaya çalışan, Semerkant'ı dünyanın en görkemli başkentine dönüştüren Türk-Moğol fatihi.",
        "seslendirme": "Timur İmparatorluğu, 1370'te Aksak Timur tarafından Semerkant merkezli kurulan güçlü bir Türk-Moğol devletidir. Timur kendisini Cengiz Han'ın varisi ilan etti ve devasa fetihler gerçekleştirdi. İran, Irak, Suriye, Hindistan ve Anadolu'yu fethetti. Ankara Muharebesi'nde Osmanlı Sultanı Yıldırım Bayezid'i yenilgiye uğrattı ve esir aldı. Bu olay Osmanlı'da Fetret Dönemi'ni başlattı. Timur askeri dehası kadar yıkımıyla da bilinir. Fethettigi şehirlerde kafatası kuleleri diktirdi. Ancak Semerkant'ı dönüştürmek için fethettiği yerlerden en iyi sanatçıları ve zanaatkarları getirdi. Registan Meydanı, Bibi Hanım Camii ve Gur-i Emir Türbesi dönemin başyapıtlarıdır. Torunu Uluğ Bey ise astronomide çığır açan bir bilim insanıydı.",
        "detaylar": [
            ("👑 Timur'un Yükselişi", "Barlas kabilesinden gelen Timur, Çağatay Hanlığı topraklarında güç kazandı ve 1370'te Semerkant'ı başkent yaptı."),
            ("⚔️ Ankara Muharebesi (1402)", "Yıldırım Bayezid'i yenip esir aldı. Osmanlı 11 yıl Fetret Dönemi yaşadı."),
            ("🏙️ Semerkant", "Fethettiği yerlerden sanatçıları getirerek Semerkant'ı dünyanın en güzel başkentine dönüştürdü."),
            ("🔭 Uluğ Bey", "Timur'un torunu Semerkant'ta rasathane kurdu. Yıldız kataloğu yüzyıllarca referans kaynağı oldu."),
            ("💀 Korkunç Miras", "Delhi'de 100.000 esir katledildi. İsfahan'da 70.000 kafatasından kule dikildi."),
        ],
    },
    {
        "baslik": "Babür İmparatorluğu", "emoji": "🕌", "tarih": "1526 – 1857",
        "renk": "#059669", "bayrak": "🇮🇳",
        "baskent": "Agra → Delhi",
        "kurucu": "Babür Şah (Zahirüddin Muhammed)",
        "zirve_alan": "4 milyon km²",
        "nufus": "~150 milyon (18. yy)",
        "ozet": "Timur ve Cengiz Han soyundan gelen Babür'ün Hindistan'da kurduğu, Tac Mahal'i inşa eden görkemli Türk-İslam imparatorluğu.",
        "seslendirme": "Babür İmparatorluğu, 1526 yılında Babür Şah tarafından Hindistan'da kurulan ve üç yüz yılı aşkın süre hüküm süren görkemli bir Türk-İslam devletidir. Babür Şah hem Timur'un hem Cengiz Han'ın soyundan geliyordu. Panipat Muharebesi'nde Delhi Sultanlığı'nı yenerek imparatorluğu kurdu. Babür İmparatorluğu döneminde Hint-İslam kültürü altın çağını yaşadı. Şah Cihan döneminde inşa edilen Tac Mahal, eşi Mümtaz Mahal anısına yapılan dünyanın en güzel yapısı olarak kabul edilir. Ekber Şah döneminde dinler arası hoşgörü politikası uygulandı ve imparatorluk en geniş sınırlarına ulaştı. On sekizinci yüzyılda imparatorluk zayıfladı ve İngiliz Doğu Hindistan Şirketi kontrolü ele geçirdi. 1857'deki Hint Ayaklanması'nın bastırılmasıyla son Babür imparatoru sürgüne gönderildi.",
        "detaylar": [
            ("👑 Babür Şah (1483-1530)", "Fergana'dan gelen Timur torunu. Kabil'i aldı, sonra Hindistan'a yöneldi. Panipat'ta Delhi Sultanlığı'nı yendi."),
            ("🌟 Ekber Şah (1556-1605)", "Tüm dinlere hoşgörü gösteren Din-i İlahi felsefesini geliştirdi. İmparatorluğu en geniş sınırlara taşıdı."),
            ("🏛️ Tac Mahal (1632-1653)", "Şah Cihan'ın eşi Mümtaz Mahal için yaptırdığı anıt mezar. 20.000 işçi 21 yılda tamamladı."),
            ("🎨 Kültürel Miras", "Mogul minyatürleri, bahçe mimarisi, Urdu dili bu dönemde gelişti."),
            ("📉 Çöküş", "İngiliz Doğu Hindistan Şirketi kontrolü ele geçirdi. 1857 İsyanı sonrası son imparator sürgün edildi."),
        ],
    },
    {
        "baslik": "Kutsal Roma-Germen", "emoji": "⚜️", "tarih": "800 – 1806",
        "renk": "#92400E", "bayrak": "🦅",
        "baskent": "Aachen → Prag → Viyana",
        "kurucu": "Charlemagne (Büyük Karl)",
        "zirve_alan": "0.9 milyon km² (parçalı yapı)",
        "nufus": "~25 milyon",
        "ozet": "Bin yıl ayakta kalan Avrupa'nın en uzun ömürlü siyasi yapısı. Ne kutsal, ne Roma, ne de Germen olmadığı söylenen gizemli imparatorluk.",
        "seslendirme": "Kutsal Roma Germen İmparatorluğu, sekiz yüz yılında Papa'nın Charlemagne'ı Roma İmparatoru ilan etmesiyle başlayan ve bin yılı aşkın süren Avrupa'nın en uzun ömürlü siyasi yapısıdır. Voltaire'in ne kutsal, ne Roma, ne de bir imparatorluk dediği bu yapı, Orta Avrupa'da yüzlerce prenslik, krallık ve şehir devletini gevşek bir çatı altında birleştiriyordu. İmparator seçimle belirlenirdi. Yedi seçici prens oy hakkına sahipti. Habsburg hanedanı yüzyıllarca imparatorluk tahtını elinde tuttu. Reformasyon bu imparatorluk içinde doğdu ve Otuz Yıl Savaşları Avrupa'yı harap etti. Westfalen Barışı modern uluslararası ilişkilerin temelini attı. Napolyon 1806'da imparatorluğu resmen feshetti.",
        "detaylar": [
            ("👑 Charlemagne (800)", "Papa III. Leo tarafından Roma İmparatoru ilan edildi. Batı Roma'nın mirasçısı olarak Frank İmparatorluğu'nu kurdu."),
            ("🗳️ Seçici Prensler", "7 seçici prens (3 din adamı, 4 laik) imparatoru seçerdi. Bu sistem yüzyıllarca devam etti."),
            ("⛪ Reformasyon (1517)", "Martin Luther'in hareketi imparatorluğu Katolik ve Protestan olarak ikiye böldü."),
            ("⚔️ 30 Yıl Savaşları (1618-1648)", "8 milyon ölü. Avrupa'nın en yıkıcı çatışmalarından biri. Westfalen Barışı ile sona erdi."),
            ("📉 Napolyon (1806)", "Napolyon birçok Alman devletini kendi himayesine aldı ve imparatorluğun feshini dayattı."),
        ],
    },
    {
        "baslik": "Asur İmparatorluğu", "emoji": "🦁", "tarih": "MÖ 2500 – MÖ 609",
        "renk": "#7C2D12", "bayrak": "🏹",
        "baskent": "Assur → Ninova",
        "kurucu": "Tudiya (ilk kral)",
        "zirve_alan": "1.4 milyon km²",
        "nufus": "~10 milyon",
        "ozet": "Mezopotamya'nın savaşçı imparatorluğu. Antik dünyanın en korkulan askeri gücü ve ilk kütüphaneyi kuran medeniyet.",
        "seslendirme": "Asur İmparatorluğu, Mezopotamya'nın en savaşçı ve en korkulan devletiydi. Milattan önce iki bin beş yüz yılından itibaren varlığını sürdüren Asur, Yeni Asur döneminde doruk noktasına ulaştı. Asur ordusu demir silahlar, kuşatma makineleri ve süvari birliklerini ilk kullanan güçtü. Fetih politikaları son derece acımasızdı. Ele geçirilen halklar sürgün edilir, şehirler yakılırdı. Ancak Asur aynı zamanda büyük bir medeniyetti. Kral Asurbanipal Ninova'da dünyanın ilk sistematik kütüphanesini kurdu. Otuz binden fazla kil tablet burada saklanıyordu. Gılgamış Destanı bu kütüphanede bulunmuştur. Devasa saray kabartmaları ve kanatlı boğa heykelleri sanat tarihinin başyapıtlarıdır. Asur İmparatorluğu milattan önce altı yüz dokuz yılında Babil ve Med ittifakı tarafından yıkıldı.",
        "detaylar": [
            ("⚔️ Askeri Güç", "Demir silahlar, kuşatma kuleleri, mancınıklar ve savaş arabaları kullanan ilk süper güç."),
            ("📚 Ninova Kütüphanesi", "Asurbanipal'in 30.000+ kil tabletten oluşan koleksiyonu. Gılgamış Destanı burada bulundu."),
            ("🦁 Lamassu Heykelleri", "İnsan başlı, kanatlı boğa heykelleri saray kapılarını süslerdi. Koruyucu ruhları simgeliyordu."),
            ("🌍 Sürgün Politikası", "Fethedilen halklar toplu sürgüne gönderilirdi. İsrail'in 10 kayıp kabilesi Asur sürgünüyle dağıldı."),
            ("💥 Ninova'nın Düşüşü (MÖ 612)", "Babil Kralı Nabopolassar ve Med Kralı Kyaxares ittifakı Ninova'yı yıktı. Asur tarihe karıştı."),
        ],
    },
    {
        "baslik": "Fransız Sömürge", "emoji": "🇫🇷", "tarih": "1534 – 1980",
        "renk": "#1D4ED8", "bayrak": "🇫🇷",
        "baskent": "Paris",
        "kurucu": "I. François (Kanada keşifleri)",
        "zirve_alan": "13 milyon km² (1920)",
        "nufus": "~110 milyon (sömürgeler)",
        "ozet": "Kanada'dan Afrika'ya, Hindiçini'den Pasifik'e yayılan, Fransız kültürünü ve dilini dünyaya taşıyan ikinci büyük sömürge imparatorluğu.",
        "seslendirme": "Fransız Sömürge İmparatorluğu, on altıncı yüzyılda başlayan ve yirminci yüzyılın ikinci yarısına kadar süren dünyanın ikinci en geniş sömürge imparatorluğudur. İlk dalga Kuzey Amerika'daki Yeni Fransa ile başladı. Quebec, Louisiana ve Karayipler Fransız kontrolüne girdi. Napolyon döneminden sonra ikinci sömürge dalgası Afrika'ya yöneldi. Cezayir, Fas, Tunus, Batı Afrika, Madagaskar ve Hindiçini Fransız sömürgesi oldu. Birinci Dünya Savaşı sonrası Suriye ve Lübnan da Fransız mandası altına girdi. Fransızca dünya dili haline geldi. Code Civil yani Fransız Medeni Kanunu birçok ülkede benimsendi. Ancak sömürge halkları büyük acılar yaşadı. Cezayir Bağımsızlık Savaşı ve Vietnam Savaşı imparatorluğun sonunu getirdi. Bugün hâlâ elli dört ülkede Fransızca resmi dil olarak konuşulmaktadır.",
        "detaylar": [
            ("🇨🇦 Yeni Fransa (1534-1763)", "Jacques Cartier Kanada'yı keşfetti. Quebec, Montreal kuruldu. 7 Yıl Savaşları'nda İngiltere'ye kaybedildi."),
            ("🌍 Afrika'nın Sömürgeleştirilmesi", "Cezayir (1830), Batı Afrika, Kongo, Madagaskar. Afrika kıtasının %35'i Fransız kontrolündeydi."),
            ("🇻🇳 Hindiçini (1887-1954)", "Vietnam, Laos, Kamboçya. Dien Bien Phu yenilgisi (1954) ile sona erdi."),
            ("⚔️ Cezayir Savaşı (1954-1962)", "8 yıl süren kanlı bağımsızlık savaşı. 1 milyondan fazla kişi hayatını kaybetti."),
            ("🗣️ Frankofoni", "Bugün 54 ülkede 300 milyon kişi Fransızca konuşuyor. Fransız kültürel etkisi devam ediyor."),
        ],
    },
    {
        "baslik": "Portekiz İmparatorluğu", "emoji": "🇵🇹", "tarih": "1415 – 1999",
        "renk": "#15803D", "bayrak": "🇵🇹",
        "baskent": "Lizbon",
        "kurucu": "Denizci Henri (Prens Henrique)",
        "zirve_alan": "10.4 milyon km²",
        "nufus": "~36 milyon (sömürgeler)",
        "ozet": "Keşifler çağını başlatan, altı kıtaya yayılan, tarihin en uzun ömürlü sömürge imparatorluğu. Brezilya'dan Makao'ya uzanan deniz gücü.",
        "seslendirme": "Portekiz İmparatorluğu, Avrupa'nın en küçük ülkelerinden birinin kurduğu en uzun ömürlü sömürge imparatorluğudur. 1415'te Kuzey Afrika'daki Ceuta'nın fethiyle başlayan keşifler çağı beş yüz yılı aşkın sürdü. Denizci Henri'nin Sagres'teki denizcilik okulunda yetiştirilen kaptanlar Afrika kıyılarını keşfetti. Bartolomeu Dias Ümit Burnu'nu geçti, Vasco da Gama Hindistan'a ulaştı. Pedro Alvares Cabral 1500'de Brezilya'yı keşfetti. Portekiz küçük ama stratejik noktaları kontrol ederek baharat ticaretini eline aldı. Goa, Makao, Mozambik, Angola ve Brezilya Portekiz sömürgesiydi. Brezilya imparatorluğun en değerli parçasıydı. Portekizce bugün iki yüz elli milyondan fazla insanın ana dili olarak yaşamaya devam ediyor. 1999'da Makao'nun Çin'e devriyle sömürge dönemi resmen sona erdi.",
        "detaylar": [
            ("⛵ Denizci Henri (1394-1460)", "Keşiflerin babası. Sagres'te denizcilik okulu kurdu. Portekiz kaşifleri yetiştirdi."),
            ("🇧🇷 Brezilya (1500-1822)", "Cabral tarafından keşfedildi. Şeker, altın ve kahve ile zenginleşti. 1822'de bağımsızlığını ilan etti."),
            ("🌏 Baharat Ticareti", "Goa, Malaka, Makao üzerinden baharat tekelini eline aldı. Avrupa'nın en zengin ülkesi oldu."),
            ("🔗 Köle Ticareti", "Afrika'dan Amerika'ya milyonlarca insanın zorla taşınmasında öncü rol oynadı. Tarihin en karanlık sayfalarından biri."),
            ("📉 Son Sömürgeler", "Angola ve Mozambik 1975'te bağımsız oldu. Makao 1999'da Çin'e devredildi. 584 yıllık dönem kapandı."),
        ],
    },
]


def _build_imparatorluk_gallery_html(empires_data):
    """İmparatorluklar galeri haritası — interaktif HTML."""
    cards_js = json.dumps([{
        "baslik": e["baslik"], "emoji": e["emoji"], "tarih": e["tarih"],
        "renk": e["renk"], "alan": e["zirve_alan"], "baskent": e["baskent"]
    } for e in empires_data], ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);color:#e2e8f0;padding:16px;overflow-x:hidden}}
.hdr{{text-align:center;margin-bottom:18px}}
.hdr h1{{font-size:1.4rem;background:linear-gradient(135deg,#fbbf24,#f59e0b);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hdr p{{font-size:.78rem;color:#94a3b8;margin-top:4px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
@media(max-width:700px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
.card{{padding:14px;border-radius:12px;background:rgba(30,41,59,.9);
  border:1px solid rgba(255,255,255,.06);cursor:pointer;transition:all .3s;
  text-align:center;position:relative;overflow:hidden}}
.card:hover{{transform:translateY(-3px);box-shadow:0 8px 25px rgba(0,0,0,.4)}}
.card.active{{border-width:2px}}
.card .em{{font-size:1.8rem;display:block;margin-bottom:6px}}
.card .nm{{font-size:.78rem;font-weight:700;color:#1A2035}}
.card .dt{{font-size:.65rem;color:#94a3b8;margin-top:2px}}
.card .ar{{font-size:.6rem;margin-top:4px;padding:2px 8px;border-radius:6px;
  display:inline-block;font-weight:600}}
.card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
</style></head><body>
<div class="hdr">
  <h1>👑 Tarihin En Büyük 20 İmparatorluğu</h1>
  <p>MÖ 3100'den 1999'a — Dünyayı Şekillendiren Güçler</p>
</div>
<div class="grid" id="grid"></div>
<script>
var E={cards_js};
var g=document.getElementById('grid');
E.forEach(function(e,i){{
  var c=document.createElement('div');
  c.className='card';
  c.style.borderColor=e.renk+'60';
  c.style.cssText+='--c:'+e.renk;
  c.innerHTML='<style>.card:nth-child('+(i+1)+')::before{{background:'+e.renk+'}}</style>'+
    '<span class="em">'+e.emoji+'</span>'+
    '<div class="nm">'+e.baslik+'</div>'+
    '<div class="dt">'+e.tarih+'</div>'+
    '<div class="ar" style="background:'+e.renk+'20;color:'+e.renk+'">'+e.alan+'</div>';
  c.onclick=function(){{
    document.querySelectorAll('.card').forEach(function(x){{x.classList.remove('active');x.style.borderColor=x.style.getPropertyValue('--c')+'60'}});
    c.classList.add('active');c.style.borderColor=e.renk;
    window.parent.postMessage({{type:'streamlit:setComponentValue',value:i}},'*');
  }};
  g.appendChild(c);
}});
</script></body></html>"""


def _render_imparatorluklar_category(store, ci):
    """Büyük İmparatorluklar — 20 imparatorluk galeri + detay."""
    cat_name, emoji_c, color, topics = _CATS[ci]
    styled_section(f"{emoji_c} Tarihin En Büyük 20 İmparatorluğu", "#DAA520")

    # Galeri
    components.html(_build_imparatorluk_gallery_html(_IMPARATORLUKLAR), height=620, scrolling=True)

    # İmparatorluk seçici
    imp_labels = [f"{e['emoji']} {e['baslik']}" for e in _IMPARATORLUKLAR]
    secilen = st.radio(
        "İmparatorluk Seçin", imp_labels,
        horizontal=True, key="imp_sec",
        label_visibility="collapsed"
    )
    idx = imp_labels.index(secilen)
    emp = _IMPARATORLUKLAR[idx]

    # === BAŞLIK KART ===
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{emp["renk"]}18,{emp["renk"]}08);'
        f'border:2px solid {emp["renk"]}40;border-radius:16px;padding:22px 26px;margin:14px 0">'
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">'
        f'<span style="font-size:2.5rem">{emp["emoji"]}</span>'
        f'<div><div style="font-size:1.4rem;font-weight:800;color:#0f172a">{emp["baslik"]}</div>'
        f'<div style="font-size:.85rem;color:{emp["renk"]};font-weight:700">{emp["tarih"]}</div></div></div>'
        f'<div style="font-size:.88rem;color:#334155;line-height:1.7">{emp["ozet"]}</div>'
        f'</div>', unsafe_allow_html=True)

    # === ÖZELLİKLER TABLOSU ===
    styled_section(f"📋 Temel Bilgiler — {emp['baslik']}", emp["renk"])
    info_rows = [
        ("👑 Kurucu", emp["kurucu"]),
        ("🏙️ Başkent", emp["baskent"]),
        ("🗺️ Zirve Alanı", emp["zirve_alan"]),
        ("👥 Nüfus", emp["nufus"]),
        ("📅 Dönem", emp["tarih"]),
    ]
    rows_html = ""
    for i, (k, v) in enumerate(info_rows):
        bg = "#111827" if i % 2 == 0 else "#1A2035"
        rows_html += (
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:12px 18px;background:{bg};border-bottom:1px solid #e2e8f0">'
            f'<span style="font-size:.84rem;font-weight:700;color:#334155">{k}</span>'
            f'<span style="font-size:.84rem;color:#0f172a;font-weight:600;text-align:right">{v}</span></div>')
    st.markdown(
        f'<div style="border:1px solid #e2e8f0;border-radius:14px;overflow:hidden;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.05)">{rows_html}</div>', unsafe_allow_html=True)

    # === SESLİ ANLATIM ===
    styled_section(f"🎧 Sesli Anlatım — {emp['baslik']}", emp["renk"])
    audio_data = {"baslik": emp["baslik"], "emoji": emp["emoji"], "renk": emp["renk"], "seslendirme": emp["seslendirme"]}
    components.html(_build_tarih_audio_html(audio_data), height=280, scrolling=False)

    # === DETAY KARTLARI ===
    styled_section(f"📚 Önemli Olaylar — {emp['baslik']}", emp["renk"])
    colors_cycle = ["#2563eb", "#7c3aed", "#0891b2", "#059669", "#d97706"]
    for j, (title, desc) in enumerate(emp["detaylar"]):
        c = colors_cycle[j % len(colors_cycle)]
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#ffffff,#111827);'
            f'border:1px solid #e2e8f0;border-radius:14px;padding:18px 22px;margin:10px 0;'
            f'border-left:5px solid {c};box-shadow:0 2px 8px rgba(0,0,0,.04)">'
            f'<div style="font-size:.92rem;font-weight:700;color:#0f172a;margin-bottom:8px">{title}</div>'
            f'<div style="font-size:.84rem;color:#475569;line-height:1.7">{desc}</div>'
            f'</div>', unsafe_allow_html=True)

    # === KARŞILAŞTIRMA BANDI ===
    st.markdown("---")
    styled_section("📊 Alan Karşılaştırması (İlk 5)", "#64748b")
    sorted_emps = sorted(_IMPARATORLUKLAR, key=lambda x: float(x["zirve_alan"].split(" ")[0].replace(",", ".")), reverse=True)[:5]
    max_alan = float(sorted_emps[0]["zirve_alan"].split(" ")[0].replace(",", "."))
    bar_html = ""
    for se in sorted_emps:
        alan_val = float(se["zirve_alan"].split(" ")[0].replace(",", "."))
        pct = alan_val / max_alan * 100
        is_current = se["baslik"] == emp["baslik"]
        border = f"border:2px solid {se['renk']}" if is_current else "border:1px solid #e2e8f0"
        bar_html += (
            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 14px;'
            f'margin:4px 0;border-radius:10px;{border};background:#111827">'
            f'<span style="font-size:1.1rem;width:30px">{se["emoji"]}</span>'
            f'<span style="font-size:.78rem;font-weight:700;color:#0f172a;width:180px">{se["baslik"]}</span>'
            f'<div style="flex:1;height:18px;background:#e2e8f0;border-radius:8px;overflow:hidden">'
            f'<div style="width:{pct:.0f}%;height:100%;background:linear-gradient(90deg,{se["renk"]},{se["renk"]}aa);'
            f'border-radius:8px;transition:width .5s"></div></div>'
            f'<span style="font-size:.75rem;font-weight:700;color:{se["renk"]};min-width:90px;text-align:right">'
            f'{se["zirve_alan"]}</span></div>')
    st.markdown(bar_html, unsafe_allow_html=True)

    # === DİĞER İMPARATORLUKLAR NAVİGASYON ===
    st.markdown("---")
    styled_section("🔄 Diğer İmparatorluklar", "#64748b")
    nav_rows = [_IMPARATORLUKLAR[i:i+5] for i in range(0, 20, 5)]
    for row in nav_rows:
        cols = st.columns(5)
        for ni, nd in enumerate(row):
            global_idx = _IMPARATORLUKLAR.index(nd)
            with cols[ni]:
                if global_idx != idx:
                    if st.button(f"{nd['emoji']} {nd['baslik'][:14]}", key=f"nav_imp_{global_idx}",
                                 use_container_width=True):
                        st.session_state["imp_sec"] = imp_labels[global_idx]
                        st.rerun()
                else:
                    st.markdown(
                        f'<div style="text-align:center;padding:6px;background:{nd["renk"]}20;'
                        f'border-radius:8px;border:2px solid {nd["renk"]}">'
                        f'<span style="font-size:1rem">{nd["emoji"]}</span>'
                        f'<div style="font-size:.65rem;font-weight:700;color:{nd["renk"]}">{nd["baslik"][:14]}</div>'
                        f'</div>', unsafe_allow_html=True)


def _build_lider_portre_css():
    """Premium CSS portrait frame styles per group."""
    return """
    .portre{position:relative;border-radius:50%;display:flex;flex-direction:column;
     align-items:center;justify-content:center;overflow:hidden;flex-shrink:0}
    .portre::before{content:'';position:absolute;top:0;left:0;right:0;height:50%;
     background:linear-gradient(180deg,rgba(255,255,255,.3),transparent);border-radius:50% 50% 0 0;z-index:1}
    .portre .em{z-index:2;line-height:1}
    .portre .ini{z-index:2;font-weight:800;color:#fff;border-radius:10px;letter-spacing:.5px;
     box-shadow:0 2px 6px rgba(0,0,0,.18)}
    /* Grup 1 — Turk-Osmanli-Islam: crescent glow */
    .portre.g1{border:3px solid var(--c);
     box-shadow:0 0 0 2px #C8952E,0 0 0 5px rgba(200,149,46,.2),0 4px 16px rgba(0,0,0,.12);
     background:radial-gradient(circle at 35% 35%,rgba(255,255,255,.15),transparent 60%),
      linear-gradient(135deg,color-mix(in srgb,var(--c) 12%,transparent),color-mix(in srgb,var(--c) 6%,transparent))}
    /* Grup 2 — Antik Cag: double border laurel */
    .portre.g2{border:3px double var(--c);
     box-shadow:0 0 0 3px color-mix(in srgb,var(--c) 20%,transparent),0 4px 16px rgba(0,0,0,.12);
     background:linear-gradient(180deg,color-mix(in srgb,var(--c) 18%,transparent),color-mix(in srgb,var(--c) 4%,transparent))}
    /* Grup 3 — Ortacag-Yenicag: inset frame */
    .portre.g3{border:3px solid var(--c);
     box-shadow:inset 0 0 0 3px color-mix(in srgb,var(--c) 12%,transparent),0 0 0 2px color-mix(in srgb,var(--c) 25%,transparent),0 4px 16px rgba(0,0,0,.12);
     background:linear-gradient(135deg,color-mix(in srgb,var(--c) 10%,transparent),#f8f0e3,color-mix(in srgb,var(--c) 10%,transparent))}
    /* Grup 4 — Asya-Afrika: thick warm */
    .portre.g4{border:4px solid var(--c);
     box-shadow:0 0 0 2px rgba(200,149,46,.35),0 4px 16px rgba(0,0,0,.12);
     background:linear-gradient(45deg,color-mix(in srgb,var(--c) 8%,transparent),color-mix(in srgb,var(--c) 18%,transparent),color-mix(in srgb,var(--c) 8%,transparent))}
    /* Grup 5 — Modern: clean minimal */
    .portre.g5{border:3px solid var(--c);
     box-shadow:0 0 0 1px color-mix(in srgb,var(--c) 35%,transparent),0 8px 24px rgba(0,0,0,.1);
     background:linear-gradient(135deg,color-mix(in srgb,var(--c) 6%,transparent),#0B0F19,color-mix(in srgb,var(--c) 6%,transparent))}
    """


def _lider_grup_class(grup_ad):
    """Return CSS class for a leader's group."""
    if "Türk" in grup_ad or "İslam" in grup_ad:
        return "g1"
    if "Antik" in grup_ad:
        return "g2"
    if "Ortaçağ" in grup_ad or "Yeniçağ" in grup_ad:
        return "g3"
    if "Asya" in grup_ad or "Afrika" in grup_ad:
        return "g4"
    return "g5"


def _build_lider_portre_inline(lider, size=90):
    """Inline HTML for a premium CSS portrait (for st.markdown)."""
    renk = lider["renk"]
    emoji = lider["emoji"]
    parts = lider["ad"].split()
    ini = (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()
    gcls = _lider_grup_class(lider.get("grup", ""))
    em_s = max(size // 3, 18)
    in_s = max(size // 8, 9)
    pad = max(size // 15, 4)
    # group-specific border style
    if gcls == "g1":
        bdr = f"border:3px solid {renk};box-shadow:0 0 0 2px #C8952E,0 0 0 5px {renk}30,0 4px 16px rgba(0,0,0,.12)"
        bg = f"background:radial-gradient(circle at 35% 35%,rgba(255,255,255,.15),transparent 60%),linear-gradient(135deg,{renk}12,{renk}06)"
    elif gcls == "g2":
        bdr = f"border:3px double {renk};box-shadow:0 0 0 3px {renk}20,0 4px 16px rgba(0,0,0,.12)"
        bg = f"background:linear-gradient(180deg,{renk}18,{renk}04)"
    elif gcls == "g3":
        bdr = f"border:3px solid {renk};box-shadow:inset 0 0 0 3px {renk}12,0 0 0 2px {renk}25,0 4px 16px rgba(0,0,0,.12)"
        bg = f"background:linear-gradient(135deg,{renk}10,#f8f0e3,{renk}10)"
    elif gcls == "g4":
        bdr = f"border:4px solid {renk};box-shadow:0 0 0 2px #C8952E40,0 4px 16px rgba(0,0,0,.12)"
        bg = f"background:linear-gradient(45deg,{renk}08,{renk}18,{renk}08)"
    else:
        bdr = f"border:3px solid {renk};box-shadow:0 0 0 1px {renk}40,0 8px 24px rgba(0,0,0,.10)"
        bg = f"background:linear-gradient(135deg,{renk}06,#0B0F19,{renk}06)"
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;{bg};{bdr};'
        f'display:flex;flex-direction:column;align-items:center;justify-content:center;'
        f'position:relative;overflow:hidden;flex-shrink:0">'
        f'<div style="position:absolute;top:0;left:0;right:0;height:50%;'
        f'background:linear-gradient(180deg,rgba(255,255,255,.28),transparent);'
        f'border-radius:50% 50% 0 0"></div>'
        f'<div style="font-size:{em_s}px;line-height:1;z-index:1">{emoji}</div>'
        f'<div style="font-size:{in_s}px;font-weight:800;color:#fff;'
        f'background:linear-gradient(135deg,{renk},{renk}cc);'
        f'padding:2px {pad}px;border-radius:10px;margin-top:{max(size//20,3)}px;'
        f'letter-spacing:.5px;z-index:1;box-shadow:0 2px 6px rgba(0,0,0,.15)">{ini}</div>'
        f'</div>'
    )


def _build_lider_gallery_html(liderler, grup_renk="#C8952E"):
    """100 Lider galeri grid HTML — portre kartlarıyla."""
    portre_css = _build_lider_portre_css()
    cards = ""
    for i, l in enumerate(liderler):
        gcls = _lider_grup_class(l.get("grup", ""))
        parts = l["ad"].split()
        ini = (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()
        cards += (
            f'<div class="card" style="--c:{l["renk"]}">'
            # portrait circle
            f'<div class="portre {gcls}" style="--c:{l["renk"]};width:72px;height:72px;margin:0 auto 8px">'
            f'<div class="em" style="font-size:1.7rem">{l["emoji"]}</div>'
            f'<div class="ini" style="font-size:.55rem;background:linear-gradient(135deg,{l["renk"]},{l["renk"]}cc);'
            f'padding:1px 6px;margin-top:2px">{ini}</div>'
            f'</div>'
            # info
            f'<div style="font-size:.72rem;font-weight:800;color:#0f172a;line-height:1.2">{l["ad"][:18]}</div>'
            f'<div style="font-size:.58rem;color:{l["renk"]};margin-top:3px;font-weight:600">{l["unvan"][:24]}</div>'
            f'<div style="font-size:.52rem;color:#64748b;margin-top:2px">{l["yasam"]}</div>'
            f'</div>')
    return (
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        f'*{{margin:0;padding:0;box-sizing:border-box}}'
        f'body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;padding:12px;'
        f'background:linear-gradient(135deg,#111827,#1A2035)}}'
        f'.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}'
        f'.card{{background:#fff;border-radius:14px;padding:16px 10px 12px;text-align:center;'
        f'border:1px solid #e2e8f0;border-top:4px solid var(--c,#C8952E);cursor:pointer;'
        f'transition:all .25s ease;box-shadow:0 2px 8px rgba(0,0,0,.05)}}'
        f'{portre_css}'
        f'</style></head><body>'
        f'<div class="grid">{cards}</div>'
        f'</body></html>')


def _render_100_lider_category(store, ci):
    """Tarihin En Etkili 100 Lideri — galeri + detay + ses + başarılar."""
    if not _LIDERLER_100:
        st.warning("Lider verileri yüklenemedi.")
        return
    cat_name, emoji_c, color, topics = _CATS[ci]
    styled_section(f"{emoji_c} Tarihin En Etkili 100 Lideri", "#C8952E")

    # === GRUP SEÇİCİ ===
    grup_labels = [f"{g['emoji']} {g['ad']}" for g in _LIDER_GRUPLARI]
    secili_grup = st.radio("Grup Seçin", grup_labels, horizontal=True, key="lider_grup_sec",
                           label_visibility="collapsed")
    grup_idx = grup_labels.index(secili_grup)
    grup = _LIDER_GRUPLARI[grup_idx]
    baslangic, bitis = grup["aralik"]
    grup_liderler = [l for l in _LIDERLER_100 if baslangic <= l["id"] <= bitis]

    # === GALERİ ===
    styled_section(f"{grup['emoji']} {grup['ad']} — {len(grup_liderler)} Lider", grup["renk"])
    components.html(_build_lider_gallery_html(grup_liderler, grup["renk"]), height=680, scrolling=True)

    # === LİDER SEÇİCİ ===
    lider_labels = [f"{l['emoji']} {l['id']}. {l['ad']}" for l in grup_liderler]
    secili_lider = st.radio("Lider Seçin", lider_labels, horizontal=False, key="lider_sec",
                            label_visibility="collapsed")
    lider_idx = lider_labels.index(secili_lider)
    lider = grup_liderler[lider_idx]

    # === BAŞLIK KARTI (portre ile) ===
    portre_html = _build_lider_portre_inline(lider, size=130)
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{lider["renk"]}18,{lider["renk"]}06,#ffffff);'
        f'border:2px solid {lider["renk"]}40;border-radius:20px;padding:26px 30px;margin:14px 0;'
        f'box-shadow:0 4px 24px rgba(0,0,0,.06)">'
        # row: portre + bilgi
        f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:16px">'
        f'{portre_html}'
        f'<div style="flex:1">'
        f'<div style="font-size:1.5rem;font-weight:800;color:#0f172a;line-height:1.2">'
        f'{lider["id"]}. {lider["ad"]}</div>'
        f'<div style="font-size:.92rem;color:{lider["renk"]};font-weight:700;margin-top:4px">'
        f'{lider["unvan"]}</div>'
        f'<div style="display:flex;align-items:center;gap:12px;margin-top:6px">'
        f'<span style="font-size:.78rem;color:#64748b">📅 {lider["yasam"]}</span>'
        f'<span style="font-size:.78rem;color:#64748b">🌍 {lider["ulke"]}</span>'
        f'<span style="font-size:.65rem;background:{lider["renk"]}15;color:{lider["renk"]};'
        f'padding:3px 10px;border-radius:12px;font-weight:700">{lider["grup"]}</span>'
        f'</div>'
        f'</div></div>'
        f'<div style="font-size:.88rem;color:#334155;line-height:1.8;'
        f'border-top:1px solid {lider["renk"]}15;padding-top:14px">{lider["ozet"]}</div>'
        f'</div>', unsafe_allow_html=True)

    # === BİLGİ TABLOSU ===
    info_rows = [
        ("🏷️ Unvan", lider["unvan"]),
        ("📅 Yaşam", lider["yasam"]),
        ("🌍 Ülke", lider["ulke"]),
        ("🏛️ Grup", lider["grup"]),
    ]
    rows_html = ""
    for i, (k, v) in enumerate(info_rows):
        bg = "#111827" if i % 2 == 0 else "#1A2035"
        rows_html += (
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:12px 18px;background:{bg};border-bottom:1px solid #e2e8f0">'
            f'<span style="font-size:.84rem;font-weight:700;color:#334155">{k}</span>'
            f'<span style="font-size:.84rem;color:#0f172a;font-weight:600;text-align:right">{v}</span></div>')
    st.markdown(
        f'<div style="border:1px solid #e2e8f0;border-radius:14px;overflow:hidden;'
        f'box-shadow:0 2px 8px rgba(0,0,0,.05)">{rows_html}</div>', unsafe_allow_html=True)

    # === SESLİ ANLATIM ===
    styled_section(f"🎧 Sesli Anlatım — {lider['ad']}", lider["renk"])
    audio_data = {"baslik": lider["ad"], "emoji": lider["emoji"],
                  "renk": lider["renk"], "seslendirme": lider["seslendirme"]}
    components.html(_build_tarih_audio_html(audio_data), height=280, scrolling=False)

    # === BAŞARILAR ===
    styled_section(f"🏆 Önemli Başarılar — {lider['ad']}", lider["renk"])
    colors_cycle = ["#2563eb", "#7c3aed", "#0891b2", "#059669", "#d97706"]
    for j, (title, desc) in enumerate(lider["basarilar"]):
        c = colors_cycle[j % len(colors_cycle)]
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#ffffff,#111827);'
            f'border:1px solid #e2e8f0;border-radius:14px;padding:18px 22px;margin:10px 0;'
            f'border-left:5px solid {c};box-shadow:0 2px 8px rgba(0,0,0,.04)">'
            f'<div style="font-size:.92rem;font-weight:700;color:#0f172a;margin-bottom:8px">{title}</div>'
            f'<div style="font-size:.84rem;color:#475569;line-height:1.7">{desc}</div>'
            f'</div>', unsafe_allow_html=True)

    # === NAVİGASYON ===
    st.markdown("---")
    styled_section(f"🔄 {grup['ad']} — Diğer Liderler", "#64748b")
    nav_rows = [grup_liderler[i:i+5] for i in range(0, len(grup_liderler), 5)]
    for row in nav_rows:
        cols = st.columns(5)
        for ni, nd in enumerate(row):
            local_idx = grup_liderler.index(nd)
            with cols[ni]:
                if local_idx != lider_idx:
                    if st.button(f"{nd['emoji']} {nd['ad'][:12]}", key=f"nav_lid_{nd['id']}",
                                 use_container_width=True):
                        st.session_state["lider_sec"] = lider_labels[local_idx]
                        st.rerun()
                else:
                    _mini = _build_lider_portre_inline(nd, size=48)
                    st.markdown(
                        f'<div style="text-align:center;padding:8px;background:{nd["renk"]}15;'
                        f'border-radius:12px;border:2px solid {nd["renk"]}">'
                        f'<div style="display:flex;justify-content:center;margin-bottom:4px">{_mini}</div>'
                        f'<div style="font-size:.6rem;font-weight:700;color:{nd["renk"]}">'
                        f'{nd["ad"][:12]}</div></div>', unsafe_allow_html=True)


def _render_category(store, ci):
    cat_name, emoji, color, topics = _CATS[ci]
    if cat_name == "Periyodik Çizelge":
        _render_periodiç_table_category(store, ci)
        return
    if cat_name == "Türkiye İller Haritası":
        _render_turkey_map_category(store, ci)
        return
    if cat_name == "Türkiye Coğrafyası":
        _render_turkey_geography_category(store, ci)
        return
    if cat_name == "Dünya Siyasi Haritası":
        _render_world_map_category(store, ci)
        return
    if cat_name == "Dünya Fiziki Haritası":
        _render_world_physical_map_category(store, ci)
        return
    if cat_name == "Dünya Tarihi":
        _render_dunya_tarihi_category(store, ci)
        return
    if cat_name == "Büyük İmparatorluklar":
        _render_imparatorluklar_category(store, ci)
        return
    if cat_name == "Tarihin 100 Lideri":
        _render_100_lider_category(store, ci)
        return
    styled_section(f"{emoji} {cat_name} — 20 Icerik", color)

    cols = st.columns(4)
    for ti, topic in enumerate(topics):
        with cols[ti % 4]:
            if st.button(f"{emoji} {topic}", key=f"cat{ci}_t{ti}", use_container_width=True):
                st.session_state["_sc3d_detail"] = f"SC3D-{ci:02d}-{ti:02d}"
                st.rerun()


def _parse_code(code):
    """SC3D-CC-TT -> (ci, ti) veya None."""
    try:
        parts = code.split("-")
        return int(parts[1]), int(parts[2])
    except Exception:
        return None


def _render_anatomy_info(ci, ti, topic_name, emoji, color):
    """Tum kategoriler için sesli anlatim + bilgi kartlari."""
    cat_info = _SCENE_INFO.get(ci) or _EXT_SCENE_DATA.get(ci)
    info = cat_info.get(ti) if cat_info else None
    if not info:
        # Bilgi henuz eklenmemis konular için basit kart
        st.markdown(
            f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;'
            f'padding:16px 20px;margin:10px 0;border-left:4px solid {color}">'
            f'<div style="font-size:.92rem;font-weight:700;color:#1e293b">{emoji} {topic_name}</div>'
            f'<div style="font-size:.82rem;color:#475569;line-height:1.5;margin-top:4px">'
            f'{topic_name} yapısını 3 boyutlu olarak inceleyebilirsiniz. '
            f'Modeli sürükleyerek döndürebilir, scroll ile yakınlaştırabilirsiniz.</div>'
            f'</div>', unsafe_allow_html=True)
        return

    # --- Sesli Anlatim Oynatiçi (Web Speech API + Senkronize Metin) ---
    narration = info["seslendirme"]
    # Cumlelere bol
    import re
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', narration) if s.strip()]
    sentences_js = json.dumps(sentences, ensure_ascii=False)

    tts_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:16px 20px;}}
.player{{display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:linear-gradient(135deg,#1e293b,#334155);border-radius:14px;
  border:1px solid rgba(255,255,255,.08);margin-bottom:14px;}}
.play-btn{{width:48px;height:48px;border-radius:50%;border:none;cursor:pointer;
  background:linear-gradient(135deg,{color},#8b5cf6);color:#fff;font-size:20px;
  display:flex;align-items:center;justify-content:center;transition:all .2s;
  box-shadow:0 4px 15px rgba(139,92,246,.3);flex-shrink:0;}}
.play-btn:hover{{transform:scale(1.08);box-shadow:0 6px 20px rgba(139,92,246,.5);}}
.play-btn.playing{{background:linear-gradient(135deg,#ef4444,#dc2626);}}
.info{{flex:1;min-width:0;}}
.title{{font-size:.88rem;font-weight:700;color:#1A2035;}}
.sub{{font-size:.75rem;color:#94a3b8;margin-top:2px;}}
.progress-bar{{width:100%;height:5px;background:rgba(255,255,255,.08);border-radius:3px;
  margin-top:8px;overflow:hidden;}}
.progress-fill{{height:100%;width:0%;background:linear-gradient(90deg,{color},#8b5cf6);
  border-radius:3px;transition:width .3s;}}
.speed-btn{{padding:4px 10px;border-radius:8px;border:1px solid rgba(255,255,255,.15);
  background:transparent;color:#94a3b8;font-size:.72rem;cursor:pointer;transition:all .2s;}}
.speed-btn.active{{background:{color};color:#fff;border-color:{color};}}
.narration{{padding:16px 18px;background:rgba(255,255,255,.03);border-radius:12px;
  border:1px solid rgba(255,255,255,.06);max-height:200px;overflow-y:auto;line-height:1.8;}}
.narration::-webkit-scrollbar{{width:4px;}}
.narration::-webkit-scrollbar-thumb{{background:rgba(255,255,255,.15);border-radius:2px;}}
.sent{{font-size:.82rem;color:#64748b;padding:3px 6px;border-radius:6px;
  transition:all .4s;display:inline;}}
.sent.active{{color:#1A2035;background:rgba(139,92,246,.15);font-weight:600;}}
.sent.done{{color:#94a3b8;}}
.time{{font-size:.75rem;color:#64748b;font-variant-numeriç:tabular-nums;min-width:40px;text-align:right;}}
</style></head>
<body>
<div class="player">
  <button class="play-btn" id="playBtn" onclick="togglePlay()">&#9654;</button>
  <div class="info">
    <div class="title">{info['emoji']} {info['baslik']} — Sesli Anlatım</div>
    <div class="sub" id="statusTxt">Dinlemek için oynat tuşuna basın</div>
    <div class="progress-bar"><div class="progress-fill" id="progFill"></div></div>
  </div>
  <div class="time" id="timeTxt">0:00</div>
  <button class="speed-btn active" id="sp1" onclick="setSpeed(1)">1x</button>
  <button class="speed-btn" id="sp15" onclick="setSpeed(1.3)">1.3x</button>
  <button class="speed-btn" id="sp2" onclick="setSpeed(0.8)">0.8x</button>
</div>
<div class="narration" id="narBox"></div>
<script>
var sents={sentences_js};
var box=document.getElementById('narBox');
var playing=false,paused=false,currentIdx=0,utterance=null,startTime=0,totalEst=0;
var rate=1.0;
// Cumleleri DOM'a ekle
sents.forEach(function(s,i){{
  var sp=document.createElement('span');
  sp.className='sent';sp.id='s'+i;sp.textContent=s+' ';
  box.appendChild(sp);
}});
// Toplam sure tahmini (türkçe ~2.5 kelime/sn)
var totalWords=sents.join(' ').split(/\\s+/).length;
totalEst=Math.round(totalWords/2.5);
function fmtTime(sec){{var m=Math.floor(sec/60);var s=Math.floor(sec%60);return m+':'+(s<10?'0':'')+s;}}
document.getElementById('timeTxt').textContent='0:00 / ~'+fmtTime(totalEst);
function highlightSent(idx){{
  sents.forEach(function(_,i){{
    var el=document.getElementById('s'+i);
    el.className=i<idx?'sent done':i===idx?'sent active':'sent';
  }});
  var active=document.getElementById('s'+idx);
  if(active)active.scrollIntoView({{behavior:'smooth',block:'nearest'}});
  var pct=Math.min(100,Math.round((idx/sents.length)*100));
  document.getElementById('progFill').style.width=pct+'%';
}}
function speakSentence(idx){{
  if(idx>=sents.length){{
    // Bitti
    playing=false;paused=false;currentIdx=0;
    document.getElementById('playBtn').innerHTML='&#9654;';
    document.getElementById('playBtn').className='play-btn';
    document.getElementById('statusTxt').textContent='Anlatım tamamlandı';
    document.getElementById('progFill').style.width='100%';
    highlightSent(-1);
    sents.forEach(function(_,i){{document.getElementById('s'+i).className='sent done';}});
    return;
  }}
  currentIdx=idx;
  highlightSent(idx);
  utterance=new SpeechSynthesisUtterance(sents[idx]);
  utterance.lang='tr-TR';utterance.rate=rate;utterance.volume=1.0;
  // ===== PREMIUM KADIN SES SECIMI =====
  if(_cachedVoice){{utterance.voice=_cachedVoice;}}
  else{{
    var voices=speechSynthesis.getVoices();
    var trAll=voices.filter(function(v){{return v.lang&&v.lang.indexOf('tr')===0}});
    var best=_pickPremiumFemale(trAll.length>0?trAll:voices);
    if(best){{utterance.voice=best;_cachedVoice=best;}}
  }}
  // Erkek sesi tespit edildiyse pitch yükselt → kadın tonu
  if(_cachedVoice&&_isMale(_cachedVoice.name)){{utterance.pitch=1.35;}}
  else{{utterance.pitch=1.05;}}
  utterance.onend=function(){{
    if(playing&&!paused){{
      // Cümleler arası 150ms doğal duraklatma — takılma önler
      setTimeout(function(){{if(playing&&!paused)speakSentence(idx+1);}},150);
    }}
  }};
  utterance.onerror=function(e){{
    // Hata olursa sonraki cümleye geç — sessiz kalma
    if(playing&&!paused&&e.error!=='canceled'){{
      setTimeout(function(){{if(playing&&!paused)speakSentence(idx+1);}},200);
    }}
  }};
  utterance.onstart=function(){{
    var elapsed=Math.round((Date.now()-startTime)/1000);
    document.getElementById('timeTxt').textContent=fmtTime(elapsed)+' / ~'+fmtTime(totalEst);
    document.getElementById('statusTxt').textContent='Cümle '+(idx+1)+'/'+sents.length;
  }};
  // Chrome 15-saniye bug fix: konuşma sırasında keepalive
  if(window._ttsKeepAlive)clearInterval(window._ttsKeepAlive);
  window._ttsKeepAlive=setInterval(function(){{
    if(speechSynthesis.speaking&&!speechSynthesis.paused){{
      speechSynthesis.pause();speechSynthesis.resume();
    }}else{{clearInterval(window._ttsKeepAlive);}}
  }},10000);
  speechSynthesis.speak(utterance);
}}
function togglePlay(){{
  if(!playing){{
    playing=true;paused=false;startTime=Date.now();
    document.getElementById('playBtn').innerHTML='&#10074;&#10074;';
    document.getElementById('playBtn').className='play-btn playing';
    document.getElementById('statusTxt').textContent='Oynatılıyor...';
    speechSynthesis.cancel();
    speakSentence(currentIdx);
  }}else if(!paused){{
    paused=true;speechSynthesis.pause();
    document.getElementById('playBtn').innerHTML='&#9654;';
    document.getElementById('playBtn').className='play-btn';
    document.getElementById('statusTxt').textContent='Duraklatıldı';
  }}else{{
    paused=false;speechSynthesis.resume();
    document.getElementById('playBtn').innerHTML='&#10074;&#10074;';
    document.getElementById('playBtn').className='play-btn playing';
    document.getElementById('statusTxt').textContent='Oynatılıyor...';
  }}
}}
function setSpeed(r){{
  rate=r;
  document.querySelectorAll('.speed-btn').forEach(function(b){{b.className='speed-btn';}});
  if(r===1)document.getElementById('sp1').className='speed-btn active';
  else if(r===1.3)document.getElementById('sp15').className='speed-btn active';
  else document.getElementById('sp2').className='speed-btn active';
  if(playing&&!paused){{speechSynthesis.cancel();speakSentence(currentIdx);}}
}}
// ===== PREMIUM KADIN SES MOTORU =====
var _cachedVoice=null;
// Erkek isimleri (kesinlikle reddet)
var _maleN=['ahmet','mehmet','tolga','kerem','murat','emre','cem','onur','baris',
  'male','erkek','man','david','mark','james','guy','ismail','hakan','burak','serdar'];
// Premium kadın isimleri (Microsoft Neural TR)
var _femN=['emel','yelda','seda','filiz','asu','zeynep','ayse','elif','beren',
  'ceren','defne','nilhan','heami','female','kadin','kadın','woman','ayla','sibel','deniz',
  'melike','asli','pinar','burcu','esra','ipek','cansu'];
function _isMale(nm){{var n=nm.toLowerCase();return _maleN.some(function(m){{return n.indexOf(m)>=0}})}}
function _isFem(nm){{var n=nm.toLowerCase();return _femN.some(function(f){{return n.indexOf(f)>=0}})}}
// Premium ses skorlama: en yüksek skor = en iyi kadın sesi
function _scoreVoice(v){{
  var s=0,n=v.name.toLowerCase();
  // Erkek sesi → çok düşük skor (ama -9999 değil, son çare olarak kullanılabilir)
  if(_isMale(v.name))s-=5000;
  // Neural = en üst düzey kalite (Edge/Chrome)
  if(n.indexOf('neural')>=0)s+=200;
  // Online Natural = ikinci en iyi
  if(n.indexOf('online')>=0||n.indexOf('natural')>=0)s+=150;
  // Bilinen premium kadın isimleri
  if(n.indexOf('emel')>=0)s+=100;
  if(n.indexOf('yelda')>=0)s+=90;
  if(n.indexOf('seda')>=0)s+=85;
  if(n.indexOf('filiz')>=0)s+=80;
  // Kadın ismi genel bonus
  if(_isFem(v.name))s+=60;
  // Microsoft > Google > diğer
  if(n.indexOf('microsoft')>=0)s+=40;
  if(n.indexOf('google')>=0)s+=30;
  // Türkçe dil bonusu
  if(v.lang&&v.lang.indexOf('tr')===0)s+=500;
  return s;
}}
// En iyi kadın sesini seç
function _pickPremiumFemale(list){{
  if(!list||list.length===0)return null;
  var scored=list.map(function(v){{return {{voice:v,score:_scoreVoice(v)}}}});
  scored.sort(function(a,b){{return b.score-a.score}});
  return scored[0].voice;
}}
function loadVoices(){{
  var v=speechSynthesis.getVoices();
  if(v.length>0&&!_cachedVoice){{
    var trAll=v.filter(function(x){{return x.lang&&x.lang.indexOf('tr')===0}});
    _cachedVoice=_pickPremiumFemale(trAll.length>0?trAll:v);
    if(_cachedVoice){{
      var label=_cachedVoice.name.replace('Microsoft ','').replace(' Online (Natural)','');
      var genderTag=_isMale(_cachedVoice.name)?' (pitch+)':' \u2640\ufe0f';
      document.getElementById('statusTxt').textContent='\U0001f399\ufe0f '+label+genderTag;
    }}
  }}
}}
loadVoices();
if(speechSynthesis.onvoiceschanged!==undefined)speechSynthesis.onvoiceschanged=loadVoices;
setTimeout(loadVoices,100);setTimeout(loadVoices,500);setTimeout(loadVoices,1500);
// Zamanlayıcı güncelle
setInterval(function(){{
  if(playing&&!paused&&startTime){{
    var elapsed=Math.round((Date.now()-startTime)/1000);
    document.getElementById('timeTxt').textContent=fmtTime(elapsed)+' / ~'+fmtTime(totalEst);
  }}
}},1000);
</script>
</body></html>"""
    styled_section(f"Sesli Anlatim — {topic_name}", color)
    components.html(tts_html, height=310, scrolling=False)

    # --- Bilgi Kartlari ---
    # 1. Tanim karti
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#ffffff,#111827);border:1px solid #e2e8f0;'
        f'border-radius:14px;padding:18px 22px;margin:12px 0;border-left:5px solid {color};'
        f'box-shadow:0 2px 8px rgba(0,0,0,.04)">'
        f'<div style="font-size:.95rem;font-weight:700;color:#0f172a;margin-bottom:8px">'
        f'{info["emoji"]} {info["baslik"]}</div>'
        f'<div style="font-size:.84rem;color:#475569;line-height:1.7">{info["tanim"]}</div>'
        f'</div>', unsafe_allow_html=True)

    # 2. Özellikler tablosu
    styled_section(f"Özellikler — {topic_name}", color)
    props = info.get("özellikler", [])
    if props:
        rows_html = ""
        for i, (k, v) in enumerate(props):
            bg = "rgba(248,250,252,1)" if i % 2 == 0 else "rgba(241,245,249,1)"
            rows_html += (
                f'<div style="display:flex;justify-content:space-between;padding:10px 16px;'
                f'background:{bg};border-bottom:1px solid #e2e8f0">'
                f'<span style="font-size:.83rem;font-weight:600;color:#334155">{k}</span>'
                f'<span style="font-size:.83rem;color:#0f172a;font-weight:700">{v}</span></div>')
        st.markdown(
            f'<div style="border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;'
            f'margin:8px 0;box-shadow:0 1px 4px rgba(0,0,0,.04)">{rows_html}</div>',
            unsafe_allow_html=True)

    # 3. Yapi bilgileri
    yapi = info.get("yapi_bilgileri", [])
    if yapi:
        styled_section(f"Anatomik Yapi — {topic_name}", color)
        cards = ""
        for em_label, desc in yapi:
            cards += (
                f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:10px 14px;margin:5px 0;display:flex;align-items:center;gap:10px;'
                f'box-shadow:0 1px 3px rgba(0,0,0,.03)">'
                f'<span style="font-size:.88rem;font-weight:700;white-space:nowrap">{em_label}</span>'
                f'<span style="font-size:.8rem;color:#475569">{desc}</span></div>')
        st.markdown(cards, unsafe_allow_html=True)

    # 4. Ilginc bilgiler
    facts = info.get("ilginc_bilgiler", [])
    if facts:
        styled_section(f"Ilginc Bilgiler — {topic_name}", _CLR["purple"])
        facts_html = ""
        for j, fact in enumerate(facts):
            facts_html += (
                f'<div style="background:linear-gradient(135deg,#faf5ff,#f5f3ff);'
                f'border:1px solid #e9d5ff;border-radius:10px;padding:10px 14px;margin:5px 0;'
                f'display:flex;align-items:flex-start;gap:8px">'
                f'<span style="font-size:1.1rem">💡</span>'
                f'<span style="font-size:.82rem;color:#4c1d95;line-height:1.6">{fact}</span></div>')
        st.markdown(facts_html, unsafe_allow_html=True)


def _render_detail(store, code):
    parsed = _parse_code(code)
    if not parsed or parsed[0] >= len(_CATS) or parsed[1] >= len(_CATS[parsed[0]][3]):
        styled_info_banner("Icerik bulunamadi!", "error")
        if st.button("\u2b05 Geri", key="sc3d_egiti_1"):

            del st.session_state["_sc3d_detail"]
            st.rerun()
        return

    ci, ti = parsed
    cat_name, emoji, color, topics = _CATS[ci]
    topic_name = topics[ti]

    if st.button("\u2b05 Geri Don", key="sc3d_back"):
        del st.session_state["_sc3d_detail"]
        st.rerun()

    styled_header(topic_name, f"{cat_name} kategorisi", emoji)
    styled_stat_row([
        ("Kategori", cat_name, color, emoji),
        ("Konu", f"{ti+1}/{len(topics)}", _CLR["blue"], "\U0001f4da"),
        ("Zorluk", ["Kolay","Orta","Zor"][ti%3], _DIFF_CLR[["Kolay","Orta","Zor"][ti%3]], "\U0001f4ca"),
        ("Sure", f"{5+ti%10} dk", _CLR["orange"], "\u23f1"),
    ])

    if ci in _WIKI and ti < len(_WIKI.get(ci, [])):
        _sec_labels = {20: "Bilim Insani Portresi", 21: "Ressam Portresi ve Eserleri",
                       22: "Kasif Portresi ve Kesifleri", 23: "Yazar Portresi ve Eserleri"}
        styled_section(f"{_sec_labels.get(ci, 'Portre')} — {topic_name}", color)
        html = _build_portrait_gallery_html(ci, ti, topic_name)
        _h = 520 if ci in _WIKI_WORKS and _WIKI_WORKS.get(ci, [[]])[ti] else 340
        components.html(html, height=_h, scrolling=True)
    else:
        styled_section(f"3D Goruntuleme — {topic_name}", color)
        html = _build_3d_html(ci, ti, topic_name)
        components.html(html, height=480, scrolling=False)

    # Sesli anlatim + bilgi kartlari
    _render_anatomy_info(ci, ti, topic_name, emoji, color)

    # Kategori içerisindeki diger konular
    with st.expander(f"\U0001f4c2 {cat_name} — Diger Konular", key="sc3d_egitim_1", expanded=False):
        cols = st.columns(4)
        for i, t in enumerate(topics):
            if i == ti:
                continue
            with cols[i % 4]:
                if st.button(f"{emoji} {t}", key=f"rel_{ci}_{i}", use_container_width=True):
                    st.session_state["_sc3d_detail"] = f"SC3D-{ci:02d}-{i:02d}"
                    st.rerun()


def _render_admin(store):
    styled_section("Veri Durumu", _CLR["dark"])
    contents = store.load_list("contents")
    styled_stat_row([
        ("Icerik", str(len(contents)), _CLR["blue"], "\U0001f4da"),
        ("Kategori", str(len(_CATS)), _CLR["purple"], "\U0001f4c2"),
        ("3D Sahne", str(len(contents)), _CLR["green"], "\U0001f3ac"),
    ])
    styled_section("Veri Yenile", _CLR["blue"])
    if st.button("\U0001f504 400 Icerigi Yeniden Olustur", type="primary", use_container_width=True, key="sc3d_egiti_2"):

        n = _auto_generate(store)
        styled_info_banner(f"{n} içerik basariyla olusturuldu!", "success")
        st.rerun()


# ══════════════════════════════════════════════════════════════
# ANA GIRIS NOKTASI
# ══════════════════════════════════════════════════════════════

def _render_main(store):
    contents = store.load_list("contents")

    # Gecersiz detay state temizle
    if "_sc3d_detail" in st.session_state:
        code = st.session_state["_sc3d_detail"]
        parsed = _parse_code(code)
        if not parsed or parsed[0] >= len(_CATS) or parsed[1] >= len(_CATS[parsed[0]][3]):
            del st.session_state["_sc3d_detail"]
        else:
            _render_detail(store, code)
            return

    active_cat = st.session_state.get("_sc3d_active_cat")

    # Aktif kategori secildiyse: geri butonu + kategori icerigi
    if active_cat is not None and active_cat == -1:
        # Yonetim paneli
        if st.button("⬅ Kategorilere Dön", key="sc3d_cat_back"):
            del st.session_state["_sc3d_active_cat"]
            st.rerun()
        _render_admin(store)
        return
    elif active_cat is not None and 0 <= active_cat < len(_CATS):
        if st.button("⬅ Kategorilere Dön", key="sc3d_cat_back_2"):
            del st.session_state["_sc3d_active_cat"]
            st.rerun()
        _render_category(store, active_cat)
        return

    # Ana ekran: hero + kategori kart grid
    _render_hero(len(contents))
    with st.expander("📊 Kategori Genel Bakış", expanded=False):
        try:
            _render_overview()
        except Exception as _e:
            st.info(f"Genel bakış yüklenemedi: {_e}")
    styled_section("Bir kategori seçin")

    cols_per_row = 5
    for row_start in range(0, len(_CATS), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx >= len(_CATS):
                break
            cat_name, emoji, color, topics = _CATS[idx]
            with col:
                if st.button(
                    f"{emoji}\n{cat_name}\n({len(topics)})",
                    key=f"sc3d_cat_{idx}",
                    use_container_width=True,
                ):
                    st.session_state["_sc3d_active_cat"] = idx
                    st.rerun()

    # Yonetim butonu
    st.markdown("---")
    if st.button("⚙️ Yönetim Paneli", key="sc3d_admin_btn"):
        st.session_state["_sc3d_active_cat"] = -1
        st.rerun()


def render_sc3d_egitim():
    """SC3D — Üç Boyutlu Egitim ana giriş noktası."""
    for old_key in ["_sc3d_css_injected"]:
        st.session_state.pop(old_key, None)
    _inject_css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("sc3d_egitim")
    except Exception:
        pass
    store = SC3DDataStore()
    contents = store.load_list("contents")
    if not contents:
        styled_header("Üç Boyutlu Egitim", "400 içerik otomatik olusturuluyor...", "\U0001f3ac")
        n = _auto_generate(store)
        styled_info_banner(f"{n} içerik olusturuldu! Sayfa yenileniyor...", "success")
        st.rerun()
    else:
        _render_main(store)
