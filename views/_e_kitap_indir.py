"""
e-Kitaplik - Klasik Kitap Indirme Modulu
Project Gutenberg uzerinden ucretsiz klasik eserleri EPUB olarak indirir.
"""

import os
import urllib.request
import streamlit as st
from typing import List, Dict

# ---------------------------------------------------------------------------
# KATALOG
# ---------------------------------------------------------------------------

CATEGORIES = {
    "rus": "Rus Edebiyati",
    "fransiz": "Fransiz Edebiyati",
    "ingiliz": "Ingiliz Edebiyati",
    "amerikan": "Amerikan Edebiyati",
    "alman": "Alman Edebiyati",
    "dunya": "Dunya Edebiyati",
    "cocuk": "Cocuk & Genclik",
    "felsefe": "Felsefe & Dusunce",
    "turk": "Turk Edebiyati",
}

CATALOG: List[Dict] = [
    # ── Rus Edebiyati (15) ──────────────────────────────────────────────
    {"title": "Crime and Punishment", "title_tr": "Suc ve Ceza", "author": "Fyodor Dostoevsky", "year": 1866, "lang": "en", "gutenberg_id": 2554, "url": "https://www.gutenberg.org/ebooks/2554.epub3.images", "category": "rus", "description": "Raskolnikov'un ahlaki cokusunun ve kurtulusunun hikayesi", "pages": "~700", "emoji": "\U0001f4d5"},
    {"title": "The Brothers Karamazov", "title_tr": "Karamazov Kardesler", "author": "Fyodor Dostoevsky", "year": 1880, "lang": "en", "gutenberg_id": 28054, "url": "https://www.gutenberg.org/ebooks/28054.epub3.images", "category": "rus", "description": "Uc kardesin iman, suphe ve ozgurluk uzerine destansi hikayesi", "pages": "~800", "emoji": "\U0001f4d5"},
    {"title": "The Idiot", "title_tr": "Budala", "author": "Fyodor Dostoevsky", "year": 1869, "lang": "en", "gutenberg_id": 2638, "url": "https://www.gutenberg.org/ebooks/2638.epub3.images", "category": "rus", "description": "Saf iyiligin toplumla catismasinin romani", "pages": "~650", "emoji": "\U0001f4d5"},
    {"title": "Notes from Underground", "title_tr": "Yeraltindan Notlar", "author": "Fyodor Dostoevsky", "year": 1864, "lang": "en", "gutenberg_id": 600, "url": "https://www.gutenberg.org/ebooks/600.epub3.images", "category": "rus", "description": "Varolusguluk edebiyatinin oncusu", "pages": "~130", "emoji": "\U0001f4d5"},
    {"title": "War and Peace", "title_tr": "Savas ve Baris", "author": "Leo Tolstoy", "year": 1869, "lang": "en", "gutenberg_id": 2600, "url": "https://www.gutenberg.org/ebooks/2600.epub3.images", "category": "rus", "description": "Napoleon savaslarinda Rus toplumunun destansi panoramasi", "pages": "~1200", "emoji": "\U0001f4d7"},
    {"title": "Anna Karenina", "title_tr": "Anna Karenina", "author": "Leo Tolstoy", "year": 1877, "lang": "en", "gutenberg_id": 1399, "url": "https://www.gutenberg.org/ebooks/1399.epub3.images", "category": "rus", "description": "Ask, ihanet ve toplumsal baskinin trajik romani", "pages": "~850", "emoji": "\U0001f4d7"},
    {"title": "The Death of Ivan Ilyich", "title_tr": "Ivan Ilyic'in Olumu", "author": "Leo Tolstoy", "year": 1886, "lang": "en", "gutenberg_id": 927, "url": "https://www.gutenberg.org/ebooks/927.epub3.images", "category": "rus", "description": "Olumle yuzlesmenin ve hayatin anlaminin sorgulanmasi", "pages": "~80", "emoji": "\U0001f4d7"},
    {"title": "Dead Souls", "title_tr": "Olu Canlar", "author": "Nikolai Gogol", "year": 1842, "lang": "en", "gutenberg_id": 1081, "url": "https://www.gutenberg.org/ebooks/1081.epub3.images", "category": "rus", "description": "Rus toplumunun hicivsel bir tablosu", "pages": "~400", "emoji": "\U0001f4d9"},
    {"title": "The Cloak", "title_tr": "Palto", "author": "Nikolai Gogol", "year": 1842, "lang": "en", "gutenberg_id": 36238, "url": "https://www.gutenberg.org/ebooks/36238.epub3.images", "category": "rus", "description": "Kucuk bir memurun paltosuyla sembolik hikayesi", "pages": "~40", "emoji": "\U0001f4d9"},
    {"title": "Fathers and Sons", "title_tr": "Babalar ve Ogullar", "author": "Ivan Turgenev", "year": 1862, "lang": "en", "gutenberg_id": 30723, "url": "https://www.gutenberg.org/ebooks/30723.epub3.images", "category": "rus", "description": "Kusak catismasi ve nihilizm uzerine", "pages": "~250", "emoji": "\U0001f4d8"},
    {"title": "The Cherry Orchard", "title_tr": "Visne Bahcesi", "author": "Anton Chekhov", "year": 1904, "lang": "en", "gutenberg_id": 7986, "url": "https://www.gutenberg.org/ebooks/7986.epub3.images", "category": "rus", "description": "Degisen Rusya'nin huzunlu komedisi", "pages": "~80", "emoji": "\U0001f4d7"},
    {"title": "The Duel", "title_tr": "Duello", "author": "Anton Chekhov", "year": 1891, "lang": "en", "gutenberg_id": 13505, "url": "https://www.gutenberg.org/ebooks/13505.epub3.images", "category": "rus", "description": "Iki farkli dunya gorusunun carpismasini anlatan uzun hikaye", "pages": "~120", "emoji": "\U0001f4d7"},
    {"title": "Resurrection", "title_tr": "Dirilme", "author": "Leo Tolstoy", "year": 1899, "lang": "en", "gutenberg_id": 1938, "url": "https://www.gutenberg.org/ebooks/1938.epub3.images", "category": "rus", "description": "Tolstoy'un son buyuk romani, adalet ve kefaret", "pages": "~500", "emoji": "\U0001f4d7"},
    {"title": "A Hero of Our Time", "title_tr": "Zamanımızin Bir Kahramani", "author": "Mikhail Lermontov", "year": 1840, "lang": "en", "gutenberg_id": 656, "url": "https://www.gutenberg.org/ebooks/656.epub3.images", "category": "rus", "description": "Rus edebiyatinin ilk psikolojik romani", "pages": "~200", "emoji": "\U0001f4d8"},
    {"title": "Eugene Onegin", "title_tr": "Yevgeni Onegin", "author": "Alexander Pushkin", "year": 1833, "lang": "en", "gutenberg_id": 23997, "url": "https://www.gutenberg.org/ebooks/23997.epub3.images", "category": "rus", "description": "Rus edebiyatinin temel tasiydi, manzum roman", "pages": "~250", "emoji": "\U0001f4d8"},

    # ── Fransiz Edebiyati (12) ──────────────────────────────────────────
    {"title": "Les Miserables", "title_tr": "Sefiller", "author": "Victor Hugo", "year": 1862, "lang": "en", "gutenberg_id": 135, "url": "https://www.gutenberg.org/ebooks/135.epub3.images", "category": "fransiz", "description": "Adalet, merhamet ve insanlik uzerine dev bir destan", "pages": "~1500", "emoji": "\U0001f4d5"},
    {"title": "The Hunchback of Notre-Dame", "title_tr": "Notre Dame'in Kamburu", "author": "Victor Hugo", "year": 1831, "lang": "en", "gutenberg_id": 2610, "url": "https://www.gutenberg.org/ebooks/2610.epub3.images", "category": "fransiz", "description": "Quasimodo ve Esmeralda'nin trajik hikayesi", "pages": "~500", "emoji": "\U0001f4d5"},
    {"title": "The Count of Monte Cristo", "title_tr": "Monte Kristo Kontu", "author": "Alexandre Dumas", "year": 1844, "lang": "en", "gutenberg_id": 1184, "url": "https://www.gutenberg.org/ebooks/1184.epub3.images", "category": "fransiz", "description": "Intikam, umut ve adaletin destansi romani", "pages": "~1200", "emoji": "\U0001f4d9"},
    {"title": "The Three Musketeers", "title_tr": "Uc Silahsorler", "author": "Alexandre Dumas", "year": 1844, "lang": "en", "gutenberg_id": 1257, "url": "https://www.gutenberg.org/ebooks/1257.epub3.images", "category": "fransiz", "description": "D'Artagnan ve uc silahsorun macerasi", "pages": "~600", "emoji": "\U0001f4d9"},
    {"title": "Madame Bovary", "title_tr": "Madam Bovary", "author": "Gustave Flaubert", "year": 1857, "lang": "en", "gutenberg_id": 2413, "url": "https://www.gutenberg.org/ebooks/2413.epub3.images", "category": "fransiz", "description": "Modern romanin donus noktasi, Emma Bovary'nin trajedisi", "pages": "~350", "emoji": "\U0001f4d5"},
    {"title": "The Red and the Black", "title_tr": "Kirmizi ve Siyah", "author": "Stendhal", "year": 1830, "lang": "en", "gutenberg_id": 44747, "url": "https://www.gutenberg.org/ebooks/44747.epub3.images", "category": "fransiz", "description": "Julien Sorel'in hirsli yukselisinin ve dususunun romani", "pages": "~500", "emoji": "\U0001f4d5"},
    {"title": "Pere Goriot", "title_tr": "Goriot Baba", "author": "Honore de Balzac", "year": 1835, "lang": "en", "gutenberg_id": 1237, "url": "https://www.gutenberg.org/ebooks/1237.epub3.images", "category": "fransiz", "description": "Babalik sevgisi ve toplumsal hirslar", "pages": "~300", "emoji": "\U0001f4d7"},
    {"title": "Around the World in Eighty Days", "title_tr": "80 Gunde Devr-i Alem", "author": "Jules Verne", "year": 1872, "lang": "en", "gutenberg_id": 103, "url": "https://www.gutenberg.org/ebooks/103.epub3.images", "category": "fransiz", "description": "Phileas Fogg'un dunya turu macerasi", "pages": "~250", "emoji": "\U0001f30d"},
    {"title": "Twenty Thousand Leagues Under the Seas", "title_tr": "Denizler Altinda 20 Bin Fersah", "author": "Jules Verne", "year": 1870, "lang": "en", "gutenberg_id": 164, "url": "https://www.gutenberg.org/ebooks/164.epub3.images", "category": "fransiz", "description": "Kaptan Nemo ve Nautilus'un denizaltindaki seruveni", "pages": "~400", "emoji": "\U0001f30a"},
    {"title": "Germinal", "title_tr": "Germinal", "author": "Emile Zola", "year": 1885, "lang": "en", "gutenberg_id": 5711, "url": "https://www.gutenberg.org/ebooks/5711.epub3.images", "category": "fransiz", "description": "Maden iscilerinin grev ve mucadele romani", "pages": "~500", "emoji": "\U0001f4d5"},
    {"title": "The Phantom of the Opera", "title_tr": "Operadaki Hayalet", "author": "Gaston Leroux", "year": 1910, "lang": "en", "gutenberg_id": 175, "url": "https://www.gutenberg.org/ebooks/175.epub3.images", "category": "fransiz", "description": "Paris Operasi'nin gizemli hayaletinin hikayesi", "pages": "~300", "emoji": "\U0001f3ad"},
    {"title": "Cyrano de Bergerac", "title_tr": "Cyrano de Bergerac", "author": "Edmond Rostand", "year": 1897, "lang": "en", "gutenberg_id": 1254, "url": "https://www.gutenberg.org/ebooks/1254.epub3.images", "category": "fransiz", "description": "Buyuk burunlu saiirin olamsuz ask hikayesi", "pages": "~200", "emoji": "\U0001f3ad"},

    # ── Ingiliz Edebiyati (12) ──────────────────────────────────────────
    {"title": "Oliver Twist", "title_tr": "Oliver Twist", "author": "Charles Dickens", "year": 1838, "lang": "en", "gutenberg_id": 730, "url": "https://www.gutenberg.org/ebooks/730.epub3.images", "category": "ingiliz", "description": "Yetim bir cocugun Londra sokaklarindaki mucadelesi", "pages": "~450", "emoji": "\U0001f4d7"},
    {"title": "A Tale of Two Cities", "title_tr": "Iki Sehrin Hikayesi", "author": "Charles Dickens", "year": 1859, "lang": "en", "gutenberg_id": 98, "url": "https://www.gutenberg.org/ebooks/98.epub3.images", "category": "ingiliz", "description": "Fransiz Devrimi'nde ask ve fedakarlik", "pages": "~400", "emoji": "\U0001f4d7"},
    {"title": "Great Expectations", "title_tr": "Buyuk Umutlar", "author": "Charles Dickens", "year": 1861, "lang": "en", "gutenberg_id": 1400, "url": "https://www.gutenberg.org/ebooks/1400.epub3.images", "category": "ingiliz", "description": "Pip'in buyume ve hayalkirikligi romani", "pages": "~500", "emoji": "\U0001f4d7"},
    {"title": "Jane Eyre", "title_tr": "Jane Eyre", "author": "Charlotte Bronte", "year": 1847, "lang": "en", "gutenberg_id": 1260, "url": "https://www.gutenberg.org/ebooks/1260.epub3.images", "category": "ingiliz", "description": "Bagimsiz bir kadinin ask ve onur hikayesi", "pages": "~550", "emoji": "\U0001f4d5"},
    {"title": "Wuthering Heights", "title_tr": "Ugultulu Tepeler", "author": "Emily Bronte", "year": 1847, "lang": "en", "gutenberg_id": 768, "url": "https://www.gutenberg.org/ebooks/768.epub3.images", "category": "ingiliz", "description": "Heathcliff ve Catherine'in tutkulu ve yikici aski", "pages": "~350", "emoji": "\U0001f4d5"},
    {"title": "Pride and Prejudice", "title_tr": "Gurur ve Onyargi", "author": "Jane Austen", "year": 1813, "lang": "en", "gutenberg_id": 1342, "url": "https://www.gutenberg.org/ebooks/1342.epub3.images", "category": "ingiliz", "description": "Elizabeth Bennet ve Mr. Darcy'nin ince askinin hikayesi", "pages": "~350", "emoji": "\U0001f4d9"},
    {"title": "Sense and Sensibility", "title_tr": "Akliselim ve Duyarlilik", "author": "Jane Austen", "year": 1811, "lang": "en", "gutenberg_id": 161, "url": "https://www.gutenberg.org/ebooks/161.epub3.images", "category": "ingiliz", "description": "Iki kiz kardesin farkli ask anlayislari", "pages": "~350", "emoji": "\U0001f4d9"},
    {"title": "The Picture of Dorian Gray", "title_tr": "Dorian Gray'in Portresi", "author": "Oscar Wilde", "year": 1890, "lang": "en", "gutenberg_id": 174, "url": "https://www.gutenberg.org/ebooks/174.epub3.images", "category": "ingiliz", "description": "Guzellik, genclik ve ahlaki cokusun gotusu", "pages": "~250", "emoji": "\U0001f3a8"},
    {"title": "Treasure Island", "title_tr": "Define Adasi", "author": "Robert Louis Stevenson", "year": 1883, "lang": "en", "gutenberg_id": 120, "url": "https://www.gutenberg.org/ebooks/120.epub3.images", "category": "ingiliz", "description": "Korsanlar, hazine ve macera dolu yolculuk", "pages": "~250", "emoji": "\U0001f3f4\u200d\u2620\ufe0f"},
    {"title": "Strange Case of Dr Jekyll and Mr Hyde", "title_tr": "Dr. Jekyll ve Mr. Hyde", "author": "Robert Louis Stevenson", "year": 1886, "lang": "en", "gutenberg_id": 43, "url": "https://www.gutenberg.org/ebooks/43.epub3.images", "category": "ingiliz", "description": "Insanin icindeki iyilik-kotuluk ikiliegi", "pages": "~100", "emoji": "\U0001f9ea"},
    {"title": "Frankenstein", "title_tr": "Frankenstein", "author": "Mary Shelley", "year": 1818, "lang": "en", "gutenberg_id": 84, "url": "https://www.gutenberg.org/ebooks/84.epub3.images", "category": "ingiliz", "description": "Bilim kurgunun ilk eseri, yaratici ve yaratik", "pages": "~250", "emoji": "\U0001f9df"},
    {"title": "Dracula", "title_tr": "Drakula", "author": "Bram Stoker", "year": 1897, "lang": "en", "gutenberg_id": 345, "url": "https://www.gutenberg.org/ebooks/345.epub3.images", "category": "ingiliz", "description": "Vampir edebiyatinin basit yapiti", "pages": "~400", "emoji": "\U0001f9db"},

    # ── Amerikan Edebiyati (10) ─────────────────────────────────────────
    {"title": "The Adventures of Tom Sawyer", "title_tr": "Tom Sawyer'in Maceralari", "author": "Mark Twain", "year": 1876, "lang": "en", "gutenberg_id": 74, "url": "https://www.gutenberg.org/ebooks/74.epub3.images", "category": "amerikan", "description": "Mississippi kiyisinda bir cocugun maceralari", "pages": "~250", "emoji": "\U0001f3de\ufe0f"},
    {"title": "Adventures of Huckleberry Finn", "title_tr": "Huckleberry Finn'in Maceralari", "author": "Mark Twain", "year": 1884, "lang": "en", "gutenberg_id": 76, "url": "https://www.gutenberg.org/ebooks/76.epub3.images", "category": "amerikan", "description": "Amerikan edebiyatinin en onemli romanlarindan", "pages": "~350", "emoji": "\U0001f6f6"},
    {"title": "Moby Dick", "title_tr": "Moby Dick", "author": "Herman Melville", "year": 1851, "lang": "en", "gutenberg_id": 2701, "url": "https://www.gutenberg.org/ebooks/2701.epub3.images", "category": "amerikan", "description": "Kaptan Ahab'in beyaz balinaya takintisinina destani", "pages": "~600", "emoji": "\U0001f40b"},
    {"title": "The Call of the Wild", "title_tr": "Vahsetin Cagrisi", "author": "Jack London", "year": 1903, "lang": "en", "gutenberg_id": 215, "url": "https://www.gutenberg.org/ebooks/215.epub3.images", "category": "amerikan", "description": "Buck adli kopegin vahsi yasama donusu", "pages": "~150", "emoji": "\U0001f43a"},
    {"title": "White Fang", "title_tr": "Beyaz Dis", "author": "Jack London", "year": 1906, "lang": "en", "gutenberg_id": 910, "url": "https://www.gutenberg.org/ebooks/910.epub3.images", "category": "amerikan", "description": "Bir kurt-kopegin evcillesme hikayesi", "pages": "~250", "emoji": "\U0001f43a"},
    {"title": "The Fall of the House of Usher", "title_tr": "Usher Evi'nin Cokusu", "author": "Edgar Allan Poe", "year": 1839, "lang": "en", "gutenberg_id": 932, "url": "https://www.gutenberg.org/ebooks/932.epub3.images", "category": "amerikan", "description": "Poe'nun en unlu korku hikayeleri", "pages": "~200", "emoji": "\U0001f47b"},
    {"title": "The Scarlet Letter", "title_tr": "Kizil Damga", "author": "Nathaniel Hawthorne", "year": 1850, "lang": "en", "gutenberg_id": 25344, "url": "https://www.gutenberg.org/ebooks/25344.epub3.images", "category": "amerikan", "description": "Puriten Amerika'da gunah ve cezalandirma", "pages": "~250", "emoji": "\U0001f4d5"},
    {"title": "Little Women", "title_tr": "Kucuk Kadinlar", "author": "Louisa May Alcott", "year": 1868, "lang": "en", "gutenberg_id": 514, "url": "https://www.gutenberg.org/ebooks/514.epub3.images", "category": "amerikan", "description": "March kiz kardeslerinin buyume hikayesi", "pages": "~450", "emoji": "\U0001f4d5"},
    {"title": "The Red Badge of Courage", "title_tr": "Kirmizi Cesaret Nisani", "author": "Stephen Crane", "year": 1895, "lang": "en", "gutenberg_id": 73, "url": "https://www.gutenberg.org/ebooks/73.epub3.images", "category": "amerikan", "description": "Ic savas sirasinda genc bir askerin korkuyla yuzlesmesi", "pages": "~180", "emoji": "\U0001f396\ufe0f"},
    {"title": "The Awakening", "title_tr": "Uyanis", "author": "Kate Chopin", "year": 1899, "lang": "en", "gutenberg_id": 160, "url": "https://www.gutenberg.org/ebooks/160.epub3.images", "category": "amerikan", "description": "Feminist edebiyatin oncusu, Edna Pontellier'in oykusu", "pages": "~180", "emoji": "\U0001f4d5"},

    # ── Alman Edebiyati (8) ─────────────────────────────────────────────
    {"title": "Metamorphosis", "title_tr": "Donusum", "author": "Franz Kafka", "year": 1915, "lang": "en", "gutenberg_id": 5200, "url": "https://www.gutenberg.org/ebooks/5200.epub3.images", "category": "alman", "description": "Gregor Samsa bir sabah bocege donusur", "pages": "~60", "emoji": "\U0001f41b"},
    {"title": "The Trial", "title_tr": "Dava", "author": "Franz Kafka", "year": 1925, "lang": "en", "gutenberg_id": 7849, "url": "https://www.gutenberg.org/ebooks/7849.epub3.images", "category": "alman", "description": "Josef K.'nin absurd yargilanma sureci", "pages": "~250", "emoji": "\U0001f4d5"},
    {"title": "The Sorrows of Young Werther", "title_tr": "Genc Werther'in Acilari", "author": "Johann Wolfgang von Goethe", "year": 1774, "lang": "en", "gutenberg_id": 2527, "url": "https://www.gutenberg.org/ebooks/2527.epub3.images", "category": "alman", "description": "Karsiliksis askin ve romantizmin ilk buyuk eseri", "pages": "~120", "emoji": "\U0001f4d9"},
    {"title": "Faust", "title_tr": "Faust", "author": "Johann Wolfgang von Goethe", "year": 1808, "lang": "en", "gutenberg_id": 14591, "url": "https://www.gutenberg.org/ebooks/14591.epub3.images", "category": "alman", "description": "Seytanla pazarlik yapan bilim adami", "pages": "~300", "emoji": "\U0001f525"},
    {"title": "Grimms' Fairy Tales", "title_tr": "Grimm Masallari", "author": "Brothers Grimm", "year": 1812, "lang": "en", "gutenberg_id": 2591, "url": "https://www.gutenberg.org/ebooks/2591.epub3.images", "category": "alman", "description": "Pamuk Prenses, Kulkedisi ve daha fazlasi", "pages": "~350", "emoji": "\U0001f9da"},
    {"title": "Siddhartha", "title_tr": "Siddhartha", "author": "Hermann Hesse", "year": 1922, "lang": "en", "gutenberg_id": 2500, "url": "https://www.gutenberg.org/ebooks/2500.epub3.images", "category": "alman", "description": "Ruhani aydinlanma arayisinin hikayesi", "pages": "~120", "emoji": "\U0001f9d8"},
    {"title": "Thus Spoke Zarathustra", "title_tr": "Boyle Buyurdu Zerdust", "author": "Friedrich Nietzsche", "year": 1883, "lang": "en", "gutenberg_id": 1998, "url": "https://www.gutenberg.org/ebooks/1998.epub3.images", "category": "alman", "description": "Nietzsche'nin felsefi basyapiti", "pages": "~350", "emoji": "\U0001f4d5"},
    {"title": "All Quiet on the Western Front", "title_tr": "Bati Cephesinde Yeni Bir Sey Yok", "author": "Erich Maria Remarque", "year": 1929, "lang": "en", "gutenberg_id": 5765, "url": "https://www.gutenberg.org/cache/epub/5765/pg5765.epub", "category": "alman", "description": "Birinci Dunya Savasi'nin dehsetini anlatan anti-savas romani", "pages": "~200", "emoji": "\U0001f4d5"},

    # ── Dunya Edebiyati (10) ────────────────────────────────────────────
    {"title": "Don Quixote", "title_tr": "Don Kisot", "author": "Miguel de Cervantes", "year": 1605, "lang": "en", "gutenberg_id": 996, "url": "https://www.gutenberg.org/ebooks/996.epub3.images", "category": "dunya", "description": "Ilk modern roman, sovalye parodisi", "pages": "~1000", "emoji": "\U0001f3c7"},
    {"title": "Divine Comedy", "title_tr": "Ilahi Komedya", "author": "Dante Alighieri", "year": 1320, "lang": "en", "gutenberg_id": 8800, "url": "https://www.gutenberg.org/ebooks/8800.epub3.images", "category": "dunya", "description": "Cehennem, Araf ve Cennet'e yolculuk", "pages": "~500", "emoji": "\U0001f525"},
    {"title": "The Iliad", "title_tr": "Ilyada", "author": "Homer", "year": -750, "lang": "en", "gutenberg_id": 6130, "url": "https://www.gutenberg.org/ebooks/6130.epub3.images", "category": "dunya", "description": "Truva Savasi'nin destani", "pages": "~500", "emoji": "\U0001f3df\ufe0f"},
    {"title": "The Odyssey", "title_tr": "Odysseia", "author": "Homer", "year": -700, "lang": "en", "gutenberg_id": 1727, "url": "https://www.gutenberg.org/ebooks/1727.epub3.images", "category": "dunya", "description": "Odysseus'un eve donus yolculugu", "pages": "~400", "emoji": "\U0001f30a"},
    {"title": "Andersen's Fairy Tales", "title_tr": "Andersen Masallari", "author": "Hans Christian Andersen", "year": 1835, "lang": "en", "gutenberg_id": 1597, "url": "https://www.gutenberg.org/ebooks/1597.epub3.images", "category": "dunya", "description": "Cirkin Ordek Yavrusu, Kucuk Deniz Kizi ve daha fazlasi", "pages": "~300", "emoji": "\U0001f9da"},
    {"title": "A Doll's House", "title_tr": "Bir Bebek Evi", "author": "Henrik Ibsen", "year": 1879, "lang": "en", "gutenberg_id": 2542, "url": "https://www.gutenberg.org/ebooks/2542.epub3.images", "category": "dunya", "description": "Kadin haklarinin oncusu tiyatro eseri", "pages": "~80", "emoji": "\U0001f3ad"},
    {"title": "Gitanjali", "title_tr": "Gitanjali", "author": "Rabindranath Tagore", "year": 1910, "lang": "en", "gutenberg_id": 7164, "url": "https://www.gutenberg.org/ebooks/7164.epub3.images", "category": "dunya", "description": "Nobel odullu siir koleksiyonu", "pages": "~100", "emoji": "\U0001f4d6"},
    {"title": "The Analects", "title_tr": "Konusmalar (Konfucyus)", "author": "Confucius", "year": -500, "lang": "en", "gutenberg_id": 3330, "url": "https://www.gutenberg.org/ebooks/3330.epub3.images", "category": "dunya", "description": "Dogu felsefesinin temel eseri", "pages": "~150", "emoji": "\U0001f4d6"},
    {"title": "The Decameron", "title_tr": "Decameron", "author": "Giovanni Boccaccio", "year": 1353, "lang": "en", "gutenberg_id": 23700, "url": "https://www.gutenberg.org/ebooks/23700.epub3.images", "category": "dunya", "description": "Veba sirasinda anlatilan 100 hikaye", "pages": "~800", "emoji": "\U0001f4d5"},
    {"title": "One Thousand and One Nights", "title_tr": "Binbir Gece Masallari", "author": "Anonymous", "year": 800, "lang": "en", "gutenberg_id": 3435, "url": "https://www.gutenberg.org/ebooks/3435.epub3.images", "category": "dunya", "description": "Sehrazat'in olamsuz hikayeleri", "pages": "~600", "emoji": "\U0001f319"},

    # ── Cocuk & Genclik (10) ────────────────────────────────────────────
    {"title": "Alice's Adventures in Wonderland", "title_tr": "Alice Harikalar Diyarinda", "author": "Lewis Carroll", "year": 1865, "lang": "en", "gutenberg_id": 11, "url": "https://www.gutenberg.org/ebooks/11.epub3.images", "category": "cocuk", "description": "Tavan deligi ve harikalar ulkesi", "pages": "~100", "emoji": "\U0001f407"},
    {"title": "The Wonderful Wizard of Oz", "title_tr": "Oz Buyucusu", "author": "L. Frank Baum", "year": 1900, "lang": "en", "gutenberg_id": 55, "url": "https://www.gutenberg.org/ebooks/55.epub3.images", "category": "cocuk", "description": "Dorothy'nin Oz ulkesindeki macerasi", "pages": "~150", "emoji": "\U0001f3a9"},
    {"title": "Peter Pan", "title_tr": "Peter Pan", "author": "J. M. Barrie", "year": 1911, "lang": "en", "gutenberg_id": 16, "url": "https://www.gutenberg.org/ebooks/16.epub3.images", "category": "cocuk", "description": "Hic buyumeyen cocugun hikayesi", "pages": "~150", "emoji": "\U0001f9da"},
    {"title": "Gulliver's Travels", "title_tr": "Gulliver'in Gezileri", "author": "Jonathan Swift", "year": 1726, "lang": "en", "gutenberg_id": 829, "url": "https://www.gutenberg.org/ebooks/829.epub3.images", "category": "cocuk", "description": "Cuceler ve devler ulkesine yolculuk", "pages": "~300", "emoji": "\U0001f30d"},
    {"title": "Robinson Crusoe", "title_tr": "Robinson Crusoe", "author": "Daniel Defoe", "year": 1719, "lang": "en", "gutenberg_id": 521, "url": "https://www.gutenberg.org/ebooks/521.epub3.images", "category": "cocuk", "description": "Issiz adada hayatta kalma hikayesi", "pages": "~300", "emoji": "\U0001f3dd\ufe0f"},
    {"title": "Pollyanna", "title_tr": "Pollyanna", "author": "Eleanor H. Porter", "year": 1913, "lang": "en", "gutenberg_id": 1450, "url": "https://www.gutenberg.org/ebooks/1450.epub3.images", "category": "cocuk", "description": "Sevinc oyununu oynayan iyimser kiz", "pages": "~200", "emoji": "\U0001f31e"},
    {"title": "Heidi", "title_tr": "Heidi", "author": "Johanna Spyri", "year": 1881, "lang": "en", "gutenberg_id": 1448, "url": "https://www.gutenberg.org/ebooks/1448.epub3.images", "category": "cocuk", "description": "Isvicre Alpleri'nde yetim bir kizin hikayesi", "pages": "~250", "emoji": "\U0001f3d4\ufe0f"},
    {"title": "The Secret Garden", "title_tr": "Gizli Bahce", "author": "Frances Hodgson Burnett", "year": 1911, "lang": "en", "gutenberg_id": 113, "url": "https://www.gutenberg.org/ebooks/113.epub3.images", "category": "cocuk", "description": "Gizli bir bahcenin iyilestirici gucu", "pages": "~250", "emoji": "\U0001f33a"},
    {"title": "The Jungle Book", "title_tr": "Orman Kitabi", "author": "Rudyard Kipling", "year": 1894, "lang": "en", "gutenberg_id": 236, "url": "https://www.gutenberg.org/ebooks/236.epub3.images", "category": "cocuk", "description": "Mowgli'nin ormandaki macerasi", "pages": "~200", "emoji": "\U0001f405"},
    {"title": "Anne of Green Gables", "title_tr": "Yesil Camlarin Anne'i", "author": "L. M. Montgomery", "year": 1908, "lang": "en", "gutenberg_id": 45, "url": "https://www.gutenberg.org/ebooks/45.epub3.images", "category": "cocuk", "description": "Hayal gucu genis yetim bir kizin hikayesi", "pages": "~300", "emoji": "\U0001f338"},

    # ── Felsefe & Dusunce (8) ───────────────────────────────────────────
    {"title": "The Republic", "title_tr": "Devlet", "author": "Plato", "year": -380, "lang": "en", "gutenberg_id": 1497, "url": "https://www.gutenberg.org/ebooks/1497.epub3.images", "category": "felsefe", "description": "Ideal devlet ve adalet uzerine diyaloglar", "pages": "~350", "emoji": "\U0001f3db\ufe0f"},
    {"title": "Meditations", "title_tr": "Dusunceler", "author": "Marcus Aurelius", "year": 180, "lang": "en", "gutenberg_id": 2680, "url": "https://www.gutenberg.org/ebooks/2680.epub3.images", "category": "felsefe", "description": "Roma imparatorunun Stoacı dusunceleri", "pages": "~150", "emoji": "\U0001f4d6"},
    {"title": "The Art of War", "title_tr": "Savas Sanati", "author": "Sun Tzu", "year": -500, "lang": "en", "gutenberg_id": 132, "url": "https://www.gutenberg.org/ebooks/132.epub3.images", "category": "felsefe", "description": "Strateji ve liderlik uzerine klasik eser", "pages": "~80", "emoji": "\U00002694\ufe0f"},
    {"title": "The Prince", "title_tr": "Prens", "author": "Niccolo Machiavelli", "year": 1532, "lang": "en", "gutenberg_id": 1232, "url": "https://www.gutenberg.org/ebooks/1232.epub3.images", "category": "felsefe", "description": "Siyasi guc ve yonetim uzerine", "pages": "~120", "emoji": "\U0001f451"},
    {"title": "Utopia", "title_tr": "Utopya", "author": "Thomas More", "year": 1516, "lang": "en", "gutenberg_id": 2130, "url": "https://www.gutenberg.org/ebooks/2130.epub3.images", "category": "felsefe", "description": "Ideal toplum tasarimi", "pages": "~120", "emoji": "\U0001f3d9\ufe0f"},
    {"title": "Walden", "title_tr": "Walden", "author": "Henry David Thoreau", "year": 1854, "lang": "en", "gutenberg_id": 205, "url": "https://www.gutenberg.org/ebooks/205.epub3.images", "category": "felsefe", "description": "Dogada sade yasamin felsefi yansimalari", "pages": "~250", "emoji": "\U0001f332"},
    {"title": "On Liberty", "title_tr": "Ozgurluk Uzerine", "author": "John Stuart Mill", "year": 1859, "lang": "en", "gutenberg_id": 34901, "url": "https://www.gutenberg.org/ebooks/34901.epub3.images", "category": "felsefe", "description": "Bireysel ozgurluk ve devlet iliskisi", "pages": "~120", "emoji": "\U0001f5fd"},
    {"title": "Beyond Good and Evil", "title_tr": "Iyinin ve Kotunun Otesinde", "author": "Friedrich Nietzsche", "year": 1886, "lang": "en", "gutenberg_id": 4363, "url": "https://www.gutenberg.org/ebooks/4363.epub3.images", "category": "felsefe", "description": "Ahlak ve felsefenin radikal elestirisii", "pages": "~200", "emoji": "\U0001f4d5"},

    # ── Turk Edebiyati (20) — Kamu mali Turk klasikleri ──────────────────
    # Kaynak: kitab-evi.com, archive.org, 1000kitap.com (telif suresi dolmus eserler)
    {"title": "Kurk Mantolu Madonna", "title_tr": "Kurk Mantolu Madonna", "author": "Sabahattin Ali", "year": 1943, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/kurk-mantolu-madonna/Kurk%20Mantolu%20Madonna%20-%20Sabahattin%20Ali.epub", "category": "turk", "description": "Raif Efendi'nin Berlin'deki tutkulu ask hikayesi", "pages": "~160", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Icimizdeki Seytan", "title_tr": "Icimizdeki Seytan", "author": "Sabahattin Ali", "year": 1940, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/icimizdeki-seytan/Icimizdeki%20Seytan%20-%20Sabahattin%20Ali.epub", "category": "turk", "description": "Ataturk doneminde bir aydin gencin bocalamalari", "pages": "~250", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Kuyucakli Yusuf", "title_tr": "Kuyucakli Yusuf", "author": "Sabahattin Ali", "year": 1937, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/kuyucakli-yusuf/Kuyucakli%20Yusuf%20-%20Sabahattin%20Ali.epub", "category": "turk", "description": "Kucuk kasaba hayatinda bir gencin adaletsizlikle mucadelesi", "pages": "~200", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Calikusu", "title_tr": "Calikusu", "author": "Resat Nuri Guntekin", "year": 1922, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/calikusu/Calikusu%20-%20Resat%20Nuri%20Guntekin.epub", "category": "turk", "description": "Feride'nin Anadolu'daki ogretmenlik seruveni", "pages": "~400", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Yaprak Dokumu", "title_tr": "Yaprak Dokumu", "author": "Resat Nuri Guntekin", "year": 1930, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/yaprak-dokumu/Yaprak%20Dokumu%20-%20Resat%20Nuri%20Guntekin.epub", "category": "turk", "description": "Bir ailenin cozulusunun acikli hikayesi", "pages": "~300", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Acimak", "title_tr": "Acimak", "author": "Resat Nuri Guntekin", "year": 1928, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/acimak/Acimak%20-%20Resat%20Nuri%20Guntekin.epub", "category": "turk", "description": "Merhamet ve toplumsal baski arasindaki catisma", "pages": "~250", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Ask-i Memnu", "title_tr": "Ask-i Memnu", "author": "Halit Ziya Usakligil", "year": 1900, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/aski-memnu/Aski%20Memnu%20-%20Halit%20Ziya%20Usakligil.epub", "category": "turk", "description": "Yasak askin yikiciligi — Turk edebiyatinin ilk buyuk romani", "pages": "~350", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Mai ve Siyah", "title_tr": "Mai ve Siyah", "author": "Halit Ziya Usakligil", "year": 1897, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/mai-ve-siyah/Mai%20ve%20Siyah%20-%20Halit%20Ziya%20Usakligil.epub", "category": "turk", "description": "Idealist bir sairirin hayallerinin yikilisi", "pages": "~280", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Intibah", "title_tr": "Intibah", "author": "Namik Kemal", "year": 1876, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/intibah/Intibah%20-%20Namik%20Kemal.epub", "category": "turk", "description": "Turk edebiyatinin ilk romani sayilan eser", "pages": "~150", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Cezmi", "title_tr": "Cezmi", "author": "Namik Kemal", "year": 1880, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/cezmi/Cezmi%20-%20Namik%20Kemal.epub", "category": "turk", "description": "Turk tarihinden bir macera romani", "pages": "~200", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Araba Sevdasi", "title_tr": "Araba Sevdasi", "author": "Recaizade Mahmut Ekrem", "year": 1896, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/araba-sevdasi/Araba%20Sevdasi%20-%20Recaizade%20Mahmut%20Ekrem.epub", "category": "turk", "description": "Alafranga ozentisinin hicvedildigi klasik roman", "pages": "~200", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Serguzest", "title_tr": "Serguzest", "author": "Samipaşazade Sezai", "year": 1889, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/serguzest/Serguzest%20-%20Samipasazade%20Sezai.epub", "category": "turk", "description": "Bir cariyenin ozgurluk arayisi", "pages": "~120", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Safahat", "title_tr": "Safahat", "author": "Mehmet Akif Ersoy", "year": 1911, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/safahat/Safahat%20-%20Mehmet%20Akif%20Ersoy.epub", "category": "turk", "description": "Istiklal Marsi sairinin 7 kitaplik siir kulliyati", "pages": "~450", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Yaban", "title_tr": "Yaban", "author": "Yakup Kadri Karaosmanoglu", "year": 1932, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/yaban/Yaban%20-%20Yakup%20Kadri%20Karaosmanoglu.epub", "category": "turk", "description": "Kurtulus Savasi doneminde koylunun gercek yuzu", "pages": "~200", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Kirik Hayatlar", "title_tr": "Kirik Hayatlar", "author": "Halit Ziya Usakligil", "year": 1924, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/kirik-hayatlar/Kirik%20Hayatlar%20-%20Halit%20Ziya%20Usakligil.epub", "category": "turk", "description": "Kaybedilmis mutluluklarin ve kirilmis hayallerin romani", "pages": "~300", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Eylul", "title_tr": "Eylul", "author": "Mehmet Rauf", "year": 1901, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/eylul/Eylul%20-%20Mehmet%20Rauf.epub", "category": "turk", "description": "Turk edebiyatinin ilk psikolojik romani", "pages": "~250", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Karabibik", "title_tr": "Karabibik", "author": "Nabizade Nazim", "year": 1890, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/karabibik/Karabibik%20-%20Nabizade%20Nazim.epub", "category": "turk", "description": "Turk edebiyatinin ilk koy romani", "pages": "~80", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Felatun Bey ile Rakim Efendi", "title_tr": "Felatun Bey ile Rakim Efendi", "author": "Ahmet Mithat Efendi", "year": 1875, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/felatun-bey/Felatun%20Bey%20ile%20Rakim%20Efendi%20-%20Ahmet%20Mithat.epub", "category": "turk", "description": "Dogu-Bati catismasini anlatan ilk romanlardan", "pages": "~180", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Bomba", "title_tr": "Omer Seyfettin Hikayeleri", "author": "Omer Seyfettin", "year": 1919, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/omer-seyfettin/Omer%20Seyfettin%20-%20Hikayeler.epub", "category": "turk", "description": "Turk hikayeciligin ustasinin secme hikayeleri", "pages": "~300", "emoji": "\U0001f1f9\U0001f1f7"},
    {"title": "Atesten Gomlek", "title_tr": "Atesten Gomlek", "author": "Halide Edib Adivar", "year": 1922, "lang": "tr", "gutenberg_id": 0, "url": "https://archive.org/download/atesten-gomlek/Atesten%20Gomlek%20-%20Halide%20Edib%20Adivar.epub", "category": "turk", "description": "Kurtulus Savasi'nin en etkileyici romani", "pages": "~250", "emoji": "\U0001f1f9\U0001f1f7"},
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _safe_filename(author: str, title: str) -> str:
    """Dosya adi icin guvenli string olusturur."""
    keep = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_.")
    def clean(s: str) -> str:
        return "".join(c if c in keep else "_" for c in s).strip()
    return f"{clean(author)} - {clean(title)}.epub"


def _download_book(url: str, save_path: str, fallback_id: int) -> bool:
    """Kitabi indirir, basarisiz olursa alternatif URL dener."""
    urls_to_try = [url]
    if fallback_id and fallback_id > 0:
        urls_to_try.append(f"https://www.gutenberg.org/ebooks/{fallback_id}.epub.images")
        urls_to_try.append(f"https://www.gutenberg.org/cache/epub/{fallback_id}/pg{fallback_id}.epub")
    for u in urls_to_try:
        try:
            urllib.request.urlretrieve(u, save_path)
            if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
                return True
            # Dosya cok kucukse (hata sayfasi olabilir), sil ve sonraki URL'yi dene
            if os.path.exists(save_path):
                os.remove(save_path)
        except Exception:
            if os.path.exists(save_path):
                try:
                    os.remove(save_path)
                except OSError:
                    pass
    return False


def _filter_catalog(search: str, category: str) -> List[Dict]:
    """Katalogu arama ve kategoriye gore filtreler."""
    results = CATALOG
    if category and category != "Tumu":
        cat_key = [k for k, v in CATEGORIES.items() if v == category]
        if cat_key:
            results = [b for b in results if b["category"] == cat_key[0]]
    if search:
        s = search.lower()
        results = [
            b for b in results
            if s in b["title"].lower()
            or s in b["title_tr"].lower()
            or s in b["author"].lower()
            or s in b.get("description", "").lower()
        ]
    return results


# ---------------------------------------------------------------------------
# MAIN RENDER
# ---------------------------------------------------------------------------

def render_kitap_indir(kitaplar_dir: str, lang_filter: str = ""):
    """Klasik kitap indirme arayuzunu gosterir.
    lang_filter: 'en' veya 'tr' ise sadece o dildeki kitaplari gosterir.
    """

    os.makedirs(kitaplar_dir, exist_ok=True)

    # Dil filtresi uygula
    _catalog = CATALOG
    _categories = CATEGORIES
    if lang_filter:
        _catalog = [b for b in CATALOG if b.get("lang", "en") == lang_filter]
        _cat_keys = set(b["category"] for b in _catalog)
        _categories = {k: v for k, v in CATEGORIES.items() if k in _cat_keys}

    _prefix = f"ek_{lang_filter}_" if lang_filter else "ekitap_"

    if lang_filter == "en":
        st.subheader("Ingilizce Klasik Eserler")
        st.caption("Project Gutenberg uzerinden ucretsiz EPUB indir — Okuma pratiginizi guclendir!")
    elif lang_filter == "tr":
        st.subheader("Turk Edebiyati Klasikleri")
        st.caption("Kamu mali Turk klasiklerini ucretsiz EPUB indir.")
    else:
        st.subheader("Klasik Eserler Kutuphanesi")
        st.caption(
            "Project Gutenberg & Archive.org uzerinden ucretsiz, telif hakki sona ermis klasik eserleri "
            "EPUB formatinda indirin."
        )

    # -- Ust filtre satiri --
    col_search, col_cat, col_info = st.columns([3, 2, 2])
    with col_search:
        search = st.text_input(
            "Kitap veya yazar ara",
            placeholder="Ornek: Dostoevsky, Sefiller, Kafka...",
            key=f"{_prefix}search",
        )
    with col_cat:
        cat_options = ["Tumu"] + list(_categories.values())
        selected_cat = st.selectbox("Kategori", cat_options, key=f"{_prefix}cat")
    with col_info:
        total = len(_catalog)
        downloaded = sum(
            1 for b in _catalog
            if os.path.exists(os.path.join(kitaplar_dir, _safe_filename(b["author"], b["title"])))
        )
        st.metric("Katalog / Indirilmis", f"{total} / {downloaded}")

    # Filtrele
    books = _filter_catalog(search or "", selected_cat or "")
    # Apply lang_filter on top if specified
    if lang_filter:
        books = [b for b in books if b.get("lang", "en") == lang_filter]

    if not books:
        st.info("Aramanizla eslesen kitap bulunamadi.")
        return

    st.divider()
    st.caption(f"{len(books)} kitap listeleniyor")

    # -- Kitap kartlari (3 sutun grid) --
    for row_start in range(0, len(books), 3):
        row_books = books[row_start : row_start + 3]
        cols = st.columns(3)
        for idx, book in enumerate(row_books):
            with cols[idx]:
                fname = _safe_filename(book["author"], book["title"])
                fpath = os.path.join(kitaplar_dir, fname)
                already = os.path.exists(fpath)

                cat_label = CATEGORIES.get(book["category"], book["category"])
                year_str = str(abs(book["year"])) + (" MO" if book["year"] < 0 else "")

                with st.container(border=True):
                    st.markdown(f"### {book['emoji']} {book['title_tr']}")
                    st.markdown(f"**{book['author']}** ({year_str})")
                    st.caption(f"{cat_label} | {book['lang'].upper()} | {book['pages']} sayfa")
                    st.markdown(f"_{book['description']}_")

                    if already:
                        st.success("Mevcut - kutuphaneye eklendi")
                    else:
                        btn_key = f"{_prefix}dl_{book['category']}_{book['title_tr'][:20].replace(' ','_')}"
                        if st.button(f"Indir", key=btn_key, use_container_width=True):
                            with st.spinner(f"{book['title_tr']} indiriliyor..."):
                                ok = _download_book(book["url"], fpath, book["gutenberg_id"])
                            if ok:
                                st.success(f"{book['title_tr']} basariyla indirildi!")
                                st.rerun()
                            else:
                                st.error(
                                    f"Indirme basarisiz. Lutfen internet baglantinizi kontrol edin."
                                )
