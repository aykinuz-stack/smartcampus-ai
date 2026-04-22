"""
Pratik Dil Ogrenme - Premium Diamond Edition
SmartCampusAI - 5 Dil, 770 Kelime + 300 Cumle, Web Speech API TTS
"""

import json
import streamlit as st
import streamlit.components.v1 as components

from views._pratik_extra_words import EXTRA_WORDS
from views._pratik_sentences import SENTENCES
from views._pratik_sentences_extra import EXTRA_SENTENCES

# ── DATA: 770 entries (500 + 270 extra) ──────────────────────────────
# (category_id, turkish, english, en_phonetic, german, de_phonetic, italian, it_phonetic, spanish, es_phonetic, french, fr_phonetic)

WORDS = [
    # ── greetings (20) ─────────────────────────────────────────────────
    ("greetings", "Merhaba", "Hello", "Helou", "Hallo", "Halo", "Ciao", "Çao", "Hola", "Ola", "Bonjour", "Bonjur"),
    ("greetings", "Günaydın", "Good morning", "Gud morning", "Guten Morgen", "Gutn Morgın", "Buongiorno", "Buoncorno", "Buenos días", "Buenos dias", "Bonjour", "Bonjur"),
    ("greetings", "İyi akşamlar", "Good evening", "Gud ivning", "Guten Abend", "Gutn Abınt", "Buonasera", "Buonasera", "Buenas noches", "Buenas noçes", "Bonsoir", "Bonsuvar"),
    ("greetings", "İyi geceler", "Good night", "Gud nayt", "Gute Nacht", "Gutı Naht", "Buonanotte", "Buonanotte", "Buenas noches", "Buenas noçes", "Bonne nuit", "Bon nüi"),
    ("greetings", "Hoşça kal", "Goodbye", "Gudbay", "Auf Wiedersehen", "Auf Vidırzen", "Arrivederci", "Arrividirçi", "Adiós", "Adios", "Au revoir", "O rövuar"),
    ("greetings", "Görüşürüz", "See you later", "Si yu leytır", "Bis später", "Bis şpetır", "A dopo", "A dopo", "Hasta luego", "Asta luego", "À plus tard", "A plü tar"),
    ("greetings", "Nasılsınız?", "How are you?", "Hav ar yu?", "Wie geht es Ihnen?", "Vi geyt es İnen?", "Come sta?", "Kome sta?", "¿Cómo está?", "Komo esta?", "Comment allez-vous ?", "Koman ale vu ?"),
    ("greetings", "İyiyim, teşekkürler", "I'm fine, thanks", "Aym fayn, tenks", "Mir geht es gut, danke", "Mir geyt es gut, danke", "Sto bene, grazie", "Sto bene, gratsiye", "Estoy bien, gracias", "Estoy biyen, grasyas", "Je vais bien, merci", "Jö ve biyen, mersi"),
    ("greetings", "Lütfen", "Please", "Pliiz", "Bitte", "Bitte", "Per favore", "Per favore", "Por favor", "Por favor", "S'il vous plaît", "Sil vu ple"),
    ("greetings", "Teşekkür ederim", "Thank you", "Tenk yu", "Danke schön", "Danke şön", "Grazie", "Gratsiye", "Gracias", "Grasyas", "Merci", "Mersi"),
    ("greetings", "Rica ederim", "You're welcome", "Yor velkım", "Bitte schön", "Bitte şön", "Prego", "Prego", "De nada", "De nada", "De rien", "Dö riyen"),
    ("greetings", "Özür dilerim", "I'm sorry", "Aym sori", "Es tut mir leid", "Es tut mir layt", "Mi dispiace", "Mi dispiçe", "Lo siento", "Lo siyento", "Je suis désolé", "Jö süi dezole"),
    ("greetings", "Affedersiniz", "Excuse me", "Ekskiyuz mi", "Entschuldigung", "Entşuldigung", "Mi scusi", "Mi skuzi", "Disculpe", "Diskulpe", "Excusez-moi", "Eksküze mua"),
    ("greetings", "Evet", "Yes", "Yes", "Ja", "Ya", "Sì", "Si", "Sí", "Si", "Oui", "Ui"),
    ("greetings", "Hayır", "No", "No", "Nein", "Nayn", "No", "No", "No", "No", "Non", "Non"),
    ("greetings", "Benim adım...", "My name is...", "May neym iz...", "Ich heiße...", "İh hayse...", "Mi chiamo...", "Mi kiyamo...", "Me llamo...", "Me yamo...", "Je m'appelle...", "Jö mapel..."),
    ("greetings", "Tanıştığıma memnun oldum", "Nice to meet you", "Nays tu miit yu", "Freut mich", "Froyt mih", "Piacere di conoscerla", "Piyaçere di konoşerla", "Encantado", "Enkantado", "Enchanté", "Anşante"),
    ("greetings", "Hoş geldiniz", "Welcome", "Velkım", "Willkommen", "Vilkomın", "Benvenuto", "Benvenuto", "Bienvenido", "Biyenvenido", "Bienvenue", "Biyenvönü"),
    ("greetings", "İyi günler", "Have a nice day", "Hev e nays dey", "Einen schönen Tag", "Aynın şönın Tak", "Buona giornata", "Buona cornata", "Buen día", "Buyen dia", "Bonne journée", "Bon jurne"),
    ("greetings", "Ne haber?", "What's up?", "Vats ap?", "Was gibt's?", "Vas gibts?", "Che c'è?", "Ke çe?", "¿Qué tal?", "Ke tal?", "Quoi de neuf ?", "Kua dö nöf ?"),

    # ── numbers (20) ───────────────────────────────────────────────────
    ("numbers", "Bir", "One", "Van", "Eins", "Ayns", "Uno", "Uno", "Uno", "Uno", "Un", "Ön"),
    ("numbers", "İki", "Two", "Tuu", "Zwei", "Tsvay", "Due", "Due", "Dos", "Dos", "Deux", "Dö"),
    ("numbers", "Üç", "Three", "Trii", "Drei", "Dray", "Tre", "Tre", "Tres", "Tres", "Trois", "Trua"),
    ("numbers", "Dört", "Four", "For", "Vier", "Fir", "Quattro", "Kuattro", "Cuatro", "Kuatro", "Quatre", "Katr"),
    ("numbers", "Beş", "Five", "Fayv", "Fünf", "Fünf", "Cinque", "Çinkue", "Cinco", "Sinko", "Cinq", "Senk"),
    ("numbers", "Altı", "Six", "Siks", "Sechs", "Zeks", "Sei", "Sey", "Seis", "Seys", "Six", "Sis"),
    ("numbers", "Yedi", "Seven", "Sevın", "Sieben", "Zibın", "Sette", "Sette", "Siete", "Siyete", "Sept", "Set"),
    ("numbers", "Sekiz", "Eight", "Eyt", "Acht", "Aht", "Otto", "Otto", "Ocho", "Oço", "Huit", "Üit"),
    ("numbers", "Dokuz", "Nine", "Nayn", "Neun", "Noyn", "Nove", "Nove", "Nueve", "Nuyeve", "Neuf", "Nöf"),
    ("numbers", "On", "Ten", "Ten", "Zehn", "Tsen", "Dieci", "Diyeçi", "Diez", "Diyes", "Dix", "Dis"),
    ("numbers", "Yirmi", "Twenty", "Tventi", "Zwanzig", "Tsvantsih", "Venti", "Venti", "Veinte", "Beynte", "Vingt", "Ven"),
    ("numbers", "Otuz", "Thirty", "Tördi", "Dreißig", "Draysih", "Trenta", "Trenta", "Treinta", "Treynta", "Trente", "Trant"),
    ("numbers", "Kırk", "Forty", "Forti", "Vierzig", "Firtsih", "Quaranta", "Kuaranta", "Cuarenta", "Kuarenta", "Quarante", "Karant"),
    ("numbers", "Elli", "Fifty", "Fifti", "Fünfzig", "Fünftsih", "Cinquanta", "Çinkuanta", "Cincuenta", "Sinkuyenta", "Cinquante", "Senkant"),
    ("numbers", "Yüz", "Hundred", "Handrıd", "Hundert", "Hundırt", "Cento", "Çento", "Cien", "Siyen", "Cent", "San"),
    ("numbers", "Bin", "Thousand", "Tauzınd", "Tausend", "Tauzınt", "Mille", "Mille", "Mil", "Mil", "Mille", "Mil"),
    ("numbers", "Milyon", "Million", "Milyın", "Million", "Milyon", "Milione", "Milyone", "Millón", "Miyon", "Million", "Milyon"),
    ("numbers", "Birinci", "First", "Först", "Erste", "Erstı", "Primo", "Primo", "Primero", "Primero", "Premier", "Prömiye"),
    ("numbers", "İkinci", "Second", "Sekınd", "Zweite", "Tsvaytı", "Secondo", "Sekondo", "Segundo", "Segundo", "Deuxième", "Döziyen"),
    ("numbers", "Yarım", "Half", "Haf", "Halb", "Halp", "Mezzo", "Medzo", "Medio", "Mediyo", "Demi", "Dömi"),

    # ── time (18) ──────────────────────────────────────────────────────
    ("time", "Saat kaç?", "What time is it?", "Vat taym iz it?", "Wie spät ist es?", "Vi şpet ist es?", "Che ora è?", "Ke ora e?", "¿Qué hora es?", "Ke ora es?", "Quelle heure est-il ?", "Kel ör e til ?"),
    ("time", "Bugün", "Today", "Tudey", "Heute", "Hoytı", "Oggi", "Oci", "Hoy", "Oy", "Aujourd'hui", "Ojurdüi"),
    ("time", "Yarın", "Tomorrow", "Tumorou", "Morgen", "Morgın", "Domani", "Domani", "Mañana", "Manyana", "Demain", "Dömen"),
    ("time", "Dün", "Yesterday", "Yestırdey", "Gestern", "Gestırn", "Ieri", "Iyeri", "Ayer", "Ayer", "Hier", "İyer"),
    ("time", "Şimdi", "Now", "Nau", "Jetzt", "Yetst", "Adesso", "Adesso", "Ahora", "Aora", "Maintenant", "Mentenan"),
    ("time", "Sonra", "Later", "Leytır", "Später", "Şpetır", "Dopo", "Dopo", "Después", "Despues", "Plus tard", "Plü tar"),
    ("time", "Önce", "Before", "Bifor", "Vorher", "Forhır", "Prima", "Prima", "Antes", "Antes", "Avant", "Avan"),
    ("time", "Sabah", "Morning", "Morning", "Morgen", "Morgın", "Mattina", "Mattina", "Mañana", "Manyana", "Matin", "Maten"),
    ("time", "Öğlen", "Noon", "Nuun", "Mittag", "Mittak", "Mezzogiorno", "Medzocorno", "Mediodía", "Mediyodia", "Midi", "Midi"),
    ("time", "Akşam", "Evening", "İvning", "Abend", "Abınt", "Sera", "Sera", "Noche", "Noçe", "Soir", "Suar"),
    ("time", "Gece", "Night", "Nayt", "Nacht", "Naht", "Notte", "Notte", "Noche", "Noçe", "Nuit", "Nüi"),
    ("time", "Hafta", "Week", "Viik", "Woche", "Vohı", "Settimana", "Settimana", "Semana", "Semana", "Semaine", "Sömen"),
    ("time", "Ay", "Month", "Mant", "Monat", "Monat", "Mese", "Meze", "Mes", "Mes", "Mois", "Mua"),
    ("time", "Yıl", "Year", "Yiir", "Jahr", "Yar", "Anno", "Anno", "Año", "Anyo", "An", "An"),
    ("time", "Pazartesi", "Monday", "Mandey", "Montag", "Montak", "Lunedì", "Lunedi", "Lunes", "Lunes", "Lundi", "Löndi"),
    ("time", "Salı", "Tuesday", "Tyuuzdey", "Dienstag", "Diinstak", "Martedì", "Martedi", "Martes", "Martes", "Mardi", "Mardi"),
    ("time", "Çarşamba", "Wednesday", "Venzdey", "Mittwoch", "Mitvoh", "Mercoledì", "Merkoledi", "Miércoles", "Miyerkoles", "Mercredi", "Merkrödi"),
    ("time", "Her zaman", "Always", "Olveys", "Immer", "İmmır", "Sempre", "Sempre", "Siempre", "Siyempre", "Toujours", "Tujur"),

    # ── family (15) ────────────────────────────────────────────────────
    ("family", "Anne", "Mother", "Madır", "Mutter", "Mutır", "Madre", "Madre", "Madre", "Madre", "Mère", "Mer"),
    ("family", "Baba", "Father", "Fadır", "Vater", "Fatır", "Padre", "Padre", "Padre", "Padre", "Père", "Per"),
    ("family", "Kardeş", "Sibling", "Sibling", "Geschwister", "Geşvistır", "Fratello", "Fratello", "Hermano", "Ermano", "Frère/Sœur", "Frer/Sör"),
    ("family", "Kız kardeş", "Sister", "Sistır", "Schwester", "Şvestır", "Sorella", "Sorella", "Hermana", "Ermana", "Sœur", "Sör"),
    ("family", "Erkek kardeş", "Brother", "Bradır", "Bruder", "Brudır", "Fratello", "Fratello", "Hermano", "Ermano", "Frère", "Frer"),
    ("family", "Çocuk", "Child", "Çayld", "Kind", "Kint", "Bambino", "Bambino", "Niño", "Ninyo", "Enfant", "Anfan"),
    ("family", "Oğul", "Son", "San", "Sohn", "Zon", "Figlio", "Filyo", "Hijo", "İho", "Fils", "Fis"),
    ("family", "Kız", "Daughter", "Dotır", "Tochter", "Tohtır", "Figlia", "Filya", "Hija", "İha", "Fille", "Fiy"),
    ("family", "Büyükanne", "Grandmother", "Grendmadır", "Großmutter", "Grosmutır", "Nonna", "Nonna", "Abuela", "Abuela", "Grand-mère", "Gran mer"),
    ("family", "Büyükbaba", "Grandfather", "Grendfadır", "Großvater", "Grosfatır", "Nonno", "Nonno", "Abuelo", "Abuelo", "Grand-père", "Gran per"),
    ("family", "Eş", "Spouse", "Spauz", "Ehepartner", "Eepartner", "Coniuge", "Konyuce", "Cónyuge", "Konyuhe", "Époux/Épouse", "Epu/Epuz"),
    ("family", "Koca", "Husband", "Hazbınd", "Ehemann", "Eeman", "Marito", "Marito", "Esposo", "Esposo", "Mari", "Mari"),
    ("family", "Karı", "Wife", "Vayf", "Ehefrau", "Eefrau", "Moglie", "Molye", "Esposa", "Esposa", "Femme", "Fam"),
    ("family", "Aile", "Family", "Femıli", "Familie", "Familie", "Famiglia", "Familya", "Familia", "Familya", "Famille", "Famiy"),
    ("family", "Akraba", "Relative", "Relıtiv", "Verwandte", "Fervantı", "Parente", "Parente", "Pariente", "Pariyente", "Parent", "Paran"),

    # ── food (20) ──────────────────────────────────────────────────────
    ("food", "Su", "Water", "Votır", "Wasser", "Vasır", "Acqua", "Akua", "Agua", "Agua", "Eau", "O"),
    ("food", "Ekmek", "Bread", "Bred", "Brot", "Brot", "Pane", "Pane", "Pan", "Pan", "Pain", "Pen"),
    ("food", "Süt", "Milk", "Milk", "Milch", "Milh", "Latte", "Latte", "Leche", "Leçe", "Lait", "Le"),
    ("food", "Kahve", "Coffee", "Kofi", "Kaffee", "Kafe", "Caffè", "Kaffe", "Café", "Kafe", "Café", "Kafe"),
    ("food", "Çay", "Tea", "Tii", "Tee", "Te", "Tè", "Te", "Té", "Te", "Thé", "Te"),
    ("food", "Et", "Meat", "Miit", "Fleisch", "Flayş", "Carne", "Karne", "Carne", "Karne", "Viande", "Viyand"),
    ("food", "Balık", "Fish", "Fiş", "Fisch", "Fiş", "Pesce", "Peşe", "Pescado", "Peskado", "Poisson", "Puason"),
    ("food", "Tavuk", "Chicken", "Çikın", "Hähnchen", "Henhın", "Pollo", "Pollo", "Pollo", "Poyo", "Poulet", "Pule"),
    ("food", "Pirinç", "Rice", "Rays", "Reis", "Rays", "Riso", "Rizo", "Arroz", "Arros", "Riz", "Ri"),
    ("food", "Meyve", "Fruit", "Fruut", "Obst", "Obst", "Frutta", "Frutta", "Fruta", "Fruta", "Fruit", "Früi"),
    ("food", "Sebze", "Vegetable", "Vectıbıl", "Gemüse", "Gemüze", "Verdura", "Verdura", "Verdura", "Verdura", "Légume", "Legüm"),
    ("food", "Peynir", "Cheese", "Çiiz", "Käse", "Keze", "Formaggio", "Formaco", "Queso", "Keso", "Fromage", "Fromaj"),
    ("food", "Yumurta", "Egg", "Eg", "Ei", "Ay", "Uovo", "Uovo", "Huevo", "Uyevo", "Œuf", "Öf"),
    ("food", "Şeker", "Sugar", "Şugır", "Zucker", "Tsukır", "Zucchero", "Tsukkero", "Azúcar", "Asukar", "Sucre", "Sükr"),
    ("food", "Tuz", "Salt", "Solt", "Salz", "Zalts", "Sale", "Sale", "Sal", "Sal", "Sel", "Sel"),
    ("food", "Hesap, lütfen", "Check, please", "Çek, pliiz", "Die Rechnung, bitte", "Di Rehnung, bitte", "Il conto, per favore", "İl konto, per favore", "La cuenta, por favor", "La kuyenta, por favor", "L'addition, s'il vous plaît", "Ladisyon, sil vu ple"),
    ("food", "Çok lezzetli", "Very delicious", "Veri delişıs", "Sehr lecker", "Zer lekır", "Molto delizioso", "Molto delitsiyozo", "Muy delicioso", "Muy delisiyoso", "Très délicieux", "Tre delisiyö"),
    ("food", "Aç değilim", "I'm not hungry", "Aym not hangri", "Ich bin nicht hungrig", "İh bin niht hungrih", "Non ho fame", "Non o fame", "No tengo hambre", "No tengo ambre", "Je n'ai pas faim", "Jö ne pa fen"),
    ("food", "Acıktım", "I'm hungry", "Aym hangri", "Ich habe Hunger", "İh habe Hungır", "Ho fame", "O fame", "Tengo hambre", "Tengo ambre", "J'ai faim", "Je fen"),
    ("food", "Susadım", "I'm thirsty", "Aym törsti", "Ich habe Durst", "İh habe Durst", "Ho sete", "O sete", "Tengo sed", "Tengo sed", "J'ai soif", "Je suaf"),

    # ── shopping (12) ──────────────────────────────────────────────────
    ("shopping", "Bu ne kadar?", "How much is this?", "Hav maç iz dis?", "Wie viel kostet das?", "Vi fil kostıt das?", "Quanto costa?", "Kuanto kosta?", "¿Cuánto cuesta?", "Kuanto kuyesta?", "Combien ça coûte ?", "Konbiyen sa kut ?"),
    ("shopping", "Pahalı", "Expensive", "İkspensiv", "Teuer", "Toyır", "Costoso", "Kostozo", "Caro", "Karo", "Cher", "Şer"),
    ("shopping", "Ucuz", "Cheap", "Çiip", "Billig", "Billih", "Economico", "Ekonomiko", "Barato", "Barato", "Bon marché", "Bon marşe"),
    ("shopping", "İndirim", "Discount", "Diskaunt", "Rabatt", "Rabat", "Sconto", "Skonto", "Descuento", "Deskuyento", "Réduction", "Redüksyon"),
    ("shopping", "Ödeme", "Payment", "Peymınt", "Zahlung", "Tsalung", "Pagamento", "Pagamento", "Pago", "Pago", "Paiement", "Peyman"),
    ("shopping", "Kredi kartı", "Credit card", "Kredit kard", "Kreditkarte", "Kreditkarte", "Carta di credito", "Karta di kredito", "Tarjeta de crédito", "Tarheta de kredito", "Carte de crédit", "Kart dö kredi"),
    ("shopping", "Nakit", "Cash", "Keş", "Bargeld", "Bargelt", "Contanti", "Kontanti", "Efectivo", "Efektivo", "Espèces", "Espes"),
    ("shopping", "Fiş", "Receipt", "Risiit", "Quittung", "Kvitung", "Ricevuta", "Riçevuta", "Recibo", "Resibo", "Reçu", "Rösü"),
    ("shopping", "Beden", "Size", "Sayz", "Größe", "Grösı", "Taglia", "Talya", "Talla", "Taya", "Taille", "Tay"),
    ("shopping", "Almak istiyorum", "I want to buy", "Ay vant tu bay", "Ich möchte kaufen", "İh möhte kaufın", "Vorrei comprare", "Vorrey komprare", "Quiero comprar", "Kiyero komprar", "Je voudrais acheter", "Jö vudre aşte"),
    ("shopping", "Sadece bakıyorum", "Just looking", "Cast luking", "Ich schaue nur", "İh şauı nur", "Sto solo guardando", "Sto solo guardando", "Solo estoy mirando", "Solo estoy mirando", "Je regarde juste", "Jö rögard jüst"),
    ("shopping", "İade etmek istiyorum", "I want to return this", "Ay vant tu ritörn dis", "Ich möchte umtauschen", "İh möhte umtauşın", "Vorrei restituire", "Vorrey restituire", "Quiero devolver", "Kiyero devolber", "Je voudrais retourner ceci", "Jö vudre rötürne sösi"),

    # ── travel (18) ────────────────────────────────────────────────────
    ("travel", "Havaalanı", "Airport", "Erpört", "Flughafen", "Flughafın", "Aeroporto", "Aeroporto", "Aeropuerto", "Aeropuerto", "Aéroport", "Aeropor"),
    ("travel", "Otel", "Hotel", "Houtel", "Hotel", "Hotel", "Albergo", "Albergo", "Hotel", "Otel", "Hôtel", "Otel"),
    ("travel", "Bilet", "Ticket", "Tikıt", "Fahrkarte", "Farkartı", "Biglietto", "Bilyetto", "Billete", "Biyete", "Billet", "Biye"),
    ("travel", "Pasaport", "Passport", "Paspört", "Reisepass", "Rayzıpas", "Passaporto", "Passaporto", "Pasaporte", "Pasaporte", "Passeport", "Paspor"),
    ("travel", "Bavul", "Suitcase", "Suutkeys", "Koffer", "Kofır", "Valigia", "Valica", "Maleta", "Maleta", "Valise", "Valiz"),
    ("travel", "Tren", "Train", "Treyn", "Zug", "Tsug", "Treno", "Treno", "Tren", "Tren", "Train", "Tren"),
    ("travel", "Otobüs", "Bus", "Bas", "Bus", "Bus", "Autobus", "Autobus", "Autobús", "Autobus", "Bus", "Büs"),
    ("travel", "Taksi", "Taxi", "Teksi", "Taxi", "Taksi", "Taxi", "Taksi", "Taxi", "Taksi", "Taxi", "Taksi"),
    ("travel", "Harita", "Map", "Mep", "Karte", "Kartı", "Mappa", "Mappa", "Mapa", "Mapa", "Carte", "Kart"),
    ("travel", "Nerede?", "Where?", "Ver?", "Wo?", "Vo?", "Dove?", "Dove?", "¿Dónde?", "Donde?", "Où ?", "U ?"),
    ("travel", "Sağ", "Right", "Rayt", "Rechts", "Rehts", "Destra", "Destra", "Derecha", "Dereça", "Droite", "Druat"),
    ("travel", "Sol", "Left", "Left", "Links", "Links", "Sinistra", "Sinistra", "Izquierda", "İskiyerda", "Gauche", "Goş"),
    ("travel", "Düz", "Straight", "Streyt", "Geradeaus", "Geradeaus", "Dritto", "Dritto", "Recto", "Rekto", "Tout droit", "Tu drua"),
    ("travel", "Rezervasyon", "Reservation", "Rezırveyşın", "Reservierung", "Rezervirung", "Prenotazione", "Prenotatsyone", "Reservación", "Reservasyon", "Réservation", "Rezervasyon"),
    ("travel", "Giriş", "Entrance", "Entrıns", "Eingang", "Ayngang", "Entrata", "Entrata", "Entrada", "Entrada", "Entrée", "Antre"),
    ("travel", "Çıkış", "Exit", "Eksit", "Ausgang", "Ausgang", "Uscita", "Uşita", "Salida", "Salida", "Sortie", "Sorti"),
    ("travel", "Yardım edin!", "Help!", "Help!", "Hilfe!", "Hilfe!", "Aiuto!", "Ayuto!", "¡Ayuda!", "Ayuda!", "Au secours !", "O sökur !"),
    ("travel", "Kayboldum", "I'm lost", "Aym lost", "Ich habe mich verirrt", "İh habe mih ferirt", "Mi sono perso", "Mi sono perso", "Estoy perdido", "Estoy perdido", "Je suis perdu", "Jö süi perdü"),

    # ── health (14) ────────────────────────────────────────────────────
    ("health", "Doktor", "Doctor", "Doktır", "Arzt", "Artst", "Dottore", "Dottore", "Doctor", "Doktor", "Médecin", "Medsen"),
    ("health", "Hastane", "Hospital", "Hospitıl", "Krankenhaus", "Krankınhaus", "Ospedale", "Ospedale", "Hospital", "Ospital", "Hôpital", "Opital"),
    ("health", "Eczane", "Pharmacy", "Farmısi", "Apotheke", "Apoteke", "Farmacia", "Farmaçiya", "Farmacia", "Farmasiya", "Pharmacie", "Farmasi"),
    ("health", "İyi hissetmiyorum", "I don't feel well", "Ay dont fiil vel", "Ich fühle mich nicht wohl", "İh füle mih niht vol", "Non mi sento bene", "Non mi sento bene", "No me siento bien", "No me siyento biyen", "Je ne me sens pas bien", "Jö nö mö san pa biyen"),
    ("health", "Başım ağrıyor", "I have a headache", "Ay hev e hedeyk", "Ich habe Kopfschmerzen", "İh habe Kopfşmertsen", "Ho mal di testa", "O mal di testa", "Me duele la cabeza", "Me duyele la kabesa", "J'ai mal à la tête", "Je mal a la tet"),
    ("health", "Ateşim var", "I have a fever", "Ay hev e fivır", "Ich habe Fieber", "İh habe Fibır", "Ho la febbre", "O la febbre", "Tengo fiebre", "Tengo fiyebre", "J'ai de la fièvre", "Je dö la fiyevr"),
    ("health", "Alerji", "Allergy", "Alırci", "Allergie", "Allergi", "Allergia", "Allerciya", "Alergia", "Alerhiya", "Allergie", "Allerji"),
    ("health", "İlaç", "Medicine", "Medisın", "Medizin", "Meditsin", "Medicina", "Mediçina", "Medicina", "Medisina", "Médicament", "Medikaman"),
    ("health", "Reçete", "Prescription", "Priskripşın", "Rezept", "Retsept", "Ricetta", "Riçetta", "Receta", "Reseta", "Ordonnance", "Ordonans"),
    ("health", "Ambulans", "Ambulance", "Embyulıns", "Krankenwagen", "Krankınvagın", "Ambulanza", "Ambulantsa", "Ambulancia", "Ambulansiya", "Ambulance", "Anbülans"),
    ("health", "Acil durum", "Emergency", "İmörcınsi", "Notfall", "Notfal", "Emergenza", "Emergentsa", "Emergencia", "Emerhensiya", "Urgence", "Ürjans"),
    ("health", "Diş ağrısı", "Toothache", "Tuuteyk", "Zahnschmerzen", "Tsanşmertsen", "Mal di denti", "Mal di denti", "Dolor de muelas", "Dolor de muyelas", "Mal de dents", "Mal dö dan"),
    ("health", "Karnım ağrıyor", "I have a stomachache", "Ay hev e stamıkeyk", "Ich habe Bauchschmerzen", "İh habe Bauhşmertsen", "Ho mal di stomaco", "O mal di stomako", "Me duele el estómago", "Me duyele el estomago", "J'ai mal au ventre", "Je mal o vantr"),
    ("health", "Sigortam var", "I have insurance", "Ay hev inşurıns", "Ich bin versichert", "İh bin ferzihırt", "Ho l'assicurazione", "O lassikuratsyone", "Tengo seguro", "Tengo seguro", "J'ai une assurance", "Je ün asürans"),

    # ── adjectives (17) ────────────────────────────────────────────────
    ("adjectives", "Büyük", "Big", "Big", "Groß", "Gros", "Grande", "Grande", "Grande", "Grande", "Grand", "Gran"),
    ("adjectives", "Küçük", "Small", "Smol", "Klein", "Klayn", "Piccolo", "Pikkolo", "Pequeño", "Pekenyo", "Petit", "Pöti"),
    ("adjectives", "İyi", "Good", "Gud", "Gut", "Gut", "Buono", "Buono", "Bueno", "Buyeno", "Bon", "Bon"),
    ("adjectives", "Kötü", "Bad", "Bed", "Schlecht", "Şleht", "Cattivo", "Kattivo", "Malo", "Malo", "Mauvais", "Move"),
    ("adjectives", "Güzel", "Beautiful", "Byutifıl", "Schön", "Şön", "Bello", "Bello", "Hermoso", "Ermoso", "Beau", "Bo"),
    ("adjectives", "Çirkin", "Ugly", "Agli", "Hässlich", "Heslih", "Brutto", "Brutto", "Feo", "Feo", "Laid", "Le"),
    ("adjectives", "Sıcak", "Hot", "Hot", "Heiß", "Hays", "Caldo", "Kaldo", "Caliente", "Kaliyente", "Chaud", "Şo"),
    ("adjectives", "Soğuk", "Cold", "Kold", "Kalt", "Kalt", "Freddo", "Freddo", "Frío", "Friyo", "Froid", "Frua"),
    ("adjectives", "Yeni", "New", "Nyu", "Neu", "Noy", "Nuovo", "Nuovo", "Nuevo", "Nuyevo", "Nouveau", "Nuvo"),
    ("adjectives", "Eski", "Old", "Old", "Alt", "Alt", "Vecchio", "Vekkiyo", "Viejo", "Biyeho", "Vieux", "Viyö"),
    ("adjectives", "Hızlı", "Fast", "Fast", "Schnell", "Şnel", "Veloce", "Veloçe", "Rápido", "Rapido", "Rapide", "Rapid"),
    ("adjectives", "Yavaş", "Slow", "Slou", "Langsam", "Langzam", "Lento", "Lento", "Lento", "Lento", "Lent", "Lan"),
    ("adjectives", "Kolay", "Easy", "İizi", "Einfach", "Aynfah", "Facile", "Façile", "Fácil", "Fasil", "Facile", "Fasil"),
    ("adjectives", "Zor", "Difficult", "Difikılt", "Schwierig", "Şvirih", "Difficile", "Diffiçile", "Difícil", "Difisil", "Difficile", "Difisil"),
    ("adjectives", "Uzun", "Long", "Long", "Lang", "Lang", "Lungo", "Lungo", "Largo", "Largo", "Long", "Lon"),
    ("adjectives", "Kısa", "Short", "Şort", "Kurz", "Kurts", "Corto", "Korto", "Corto", "Korto", "Court", "Kur"),
    ("adjectives", "Mutlu", "Happy", "Hepi", "Glücklich", "Glüklih", "Felice", "Feliçe", "Feliz", "Felis", "Heureux", "Örö"),

    # ── verbs (20) ─────────────────────────────────────────────────────
    ("verbs", "Olmak", "To be", "Tu bi", "Sein", "Zayn", "Essere", "Essere", "Ser", "Ser", "Être", "Etr"),
    ("verbs", "Yapmak", "To do", "Tu du", "Machen", "Mahın", "Fare", "Fare", "Hacer", "Aser", "Faire", "Fer"),
    ("verbs", "Gitmek", "To go", "Tu go", "Gehen", "Geın", "Andare", "Andare", "Ir", "İr", "Aller", "Ale"),
    ("verbs", "Gelmek", "To come", "Tu kam", "Kommen", "Komın", "Venire", "Venire", "Venir", "Benir", "Venir", "Vönir"),
    ("verbs", "Yemek", "To eat", "Tu iit", "Essen", "Esın", "Mangiare", "Mancare", "Comer", "Komer", "Manger", "Manje"),
    ("verbs", "İçmek", "To drink", "Tu drink", "Trinken", "Trinkın", "Bere", "Bere", "Beber", "Beber", "Boire", "Buar"),
    ("verbs", "Uyumak", "To sleep", "Tu sliip", "Schlafen", "Şlafın", "Dormire", "Dormire", "Dormir", "Dormir", "Dormir", "Dormir"),
    ("verbs", "Konuşmak", "To speak", "Tu spiik", "Sprechen", "Şprehın", "Parlare", "Parlare", "Hablar", "Ablar", "Parler", "Parle"),
    ("verbs", "Okumak", "To read", "Tu riid", "Lesen", "Lezın", "Leggere", "Leccere", "Leer", "Leer", "Lire", "Lir"),
    ("verbs", "Yazmak", "To write", "Tu rayt", "Schreiben", "Şraybın", "Scrivere", "Skrivere", "Escribir", "Eskribir", "Écrire", "Ekrir"),
    ("verbs", "Görmek", "To see", "Tu sii", "Sehen", "Zeın", "Vedere", "Vedere", "Ver", "Ber", "Voir", "Vuar"),
    ("verbs", "Duymak", "To hear", "Tu hiir", "Hören", "Hörın", "Sentire", "Sentire", "Oír", "Oir", "Entendre", "Antandr"),
    ("verbs", "Bilmek", "To know", "Tu nou", "Wissen", "Visın", "Sapere", "Sapere", "Saber", "Saber", "Savoir", "Savuar"),
    ("verbs", "İstemek", "To want", "Tu vant", "Wollen", "Volın", "Volere", "Volere", "Querer", "Kerer", "Vouloir", "Vuluar"),
    ("verbs", "Sevmek", "To love", "Tu lav", "Lieben", "Libın", "Amare", "Amare", "Amar", "Amar", "Aimer", "Eme"),
    ("verbs", "Çalışmak", "To work", "Tu vörk", "Arbeiten", "Arbaytın", "Lavorare", "Lavorare", "Trabajar", "Trabahar", "Travailler", "Travaye"),
    ("verbs", "Öğrenmek", "To learn", "Tu lörn", "Lernen", "Lernın", "Imparare", "İmparare", "Aprender", "Aprender", "Apprendre", "Aprandr"),
    ("verbs", "Anlamak", "To understand", "Tu andırstand", "Verstehen", "Ferşteın", "Capire", "Kapire", "Entender", "Entender", "Comprendre", "Konprandr"),
    ("verbs", "Vermek", "To give", "Tu giv", "Geben", "Gebın", "Dare", "Dare", "Dar", "Dar", "Donner", "Done"),
    ("verbs", "Almak", "To take", "Tu teyk", "Nehmen", "Nemın", "Prendere", "Prendere", "Tomar", "Tomar", "Prendre", "Prandr"),

    # ── daily (18) ─────────────────────────────────────────────────────
    ("daily", "Türkçe bilmiyorum", "I don't speak Turkish", "Ay dont spiik törkiş", "Ich spreche kein Türkisch", "İh şprehe kayn Türkiş", "Non parlo turco", "Non parlo turko", "No hablo turco", "No ablo turko", "Je ne parle pas turc", "Jö nö parl pa türk"),
    ("daily", "İngilizce biliyor musunuz?", "Do you speak English?", "Du yu spiik ingliş?", "Sprechen Sie Englisch?", "Şprehın zi İngliş?", "Parla inglese?", "Parla ingleze?", "¿Habla inglés?", "Abla ingles?", "Parlez-vous anglais ?", "Parle vu angle ?"),
    ("daily", "Anlamıyorum", "I don't understand", "Ay dont andırstand", "Ich verstehe nicht", "İh ferşteye niht", "Non capisco", "Non kapisko", "No entiendo", "No entiyendo", "Je ne comprends pas", "Jö nö konpran pa"),
    ("daily", "Tekrar eder misiniz?", "Can you repeat?", "Ken yu ripiit?", "Können Sie wiederholen?", "Könın zi vidırholın?", "Può ripetere?", "Puo ripetere?", "¿Puede repetir?", "Puyede repetir?", "Pouvez-vous répéter ?", "Puve vu repete ?"),
    ("daily", "Yavaş konuşun lütfen", "Please speak slowly", "Pliiz spiik slouli", "Sprechen Sie bitte langsam", "Şprehın zi bitte langzam", "Parli lentamente, per favore", "Parli lentamente, per favore", "Hable despacio, por favor", "Able despasyo, por favor", "Parlez lentement, s'il vous plaît", "Parle lantöman, sil vu ple"),
    ("daily", "Tuvaleti nerede?", "Where is the toilet?", "Ver iz dı toylet?", "Wo ist die Toilette?", "Vo ist di Toylettı?", "Dov'è il bagno?", "Dove il banyo?", "¿Dónde está el baño?", "Donde esta el banyo?", "Où sont les toilettes ?", "U son le tualet ?"),
    ("daily", "Polis", "Police", "Poliis", "Polizei", "Politsay", "Polizia", "Politsiya", "Policía", "Polisiya", "Police", "Polis"),
    ("daily", "Telefon", "Phone", "Foun", "Telefon", "Telefon", "Telefono", "Telefono", "Teléfono", "Telefono", "Téléphone", "Telefon"),
    ("daily", "Wi-Fi şifresi ne?", "What is the Wi-Fi password?", "Vat iz dı vayfay pasvörd?", "Wie ist das WLAN-Passwort?", "Vi ist das Vlan-Passvort?", "Qual è la password del Wi-Fi?", "Kual e la passvord del vayfay?", "¿Cuál es la contraseña del Wi-Fi?", "Kual es la kontrasenyo del vayfay?", "Quel est le mot de passe Wi-Fi ?", "Kel e lö mo dö pas vayfay ?"),
    ("daily", "Hava nasıl?", "How's the weather?", "Hauz dı vedır?", "Wie ist das Wetter?", "Vi ist das Vetır?", "Com'è il tempo?", "Kome il tempo?", "¿Qué tiempo hace?", "Ke tiyempo ase?", "Quel temps fait-il ?", "Kel tan fe til ?"),
    ("daily", "Yağmur yağıyor", "It's raining", "İts reyning", "Es regnet", "Es regnıt", "Piove", "Piyove", "Está lloviendo", "Esta yoviyendo", "Il pleut", "İl plö"),
    ("daily", "Güneşli", "Sunny", "Sani", "Sonnig", "Zonnih", "Soleggiato", "Soleccato", "Soleado", "Soleado", "Ensoleillé", "Ansoleye"),
    ("daily", "Fotoğraf çekebilir miyim?", "Can I take a photo?", "Ken ay teyk e foto?", "Kann ich ein Foto machen?", "Kan ih ayn Foto mahın?", "Posso fare una foto?", "Posso fare una foto?", "¿Puedo tomar una foto?", "Puyedo tomar una foto?", "Puis-je prendre une photo ?", "Püij prandr ün foto ?"),
    ("daily", "Kayboldum, yardım eder misiniz?", "I'm lost, can you help?", "Aym lost, ken yu help?", "Ich bin verloren, können Sie helfen?", "İh bin ferlorın, könın zi helfın?", "Mi sono perso, può aiutarmi?", "Mi sono perso, puo ayutarmi?", "Estoy perdido, ¿puede ayudarme?", "Estoy perdido, puyede ayudarme?", "Je suis perdu, pouvez-vous m'aider ?", "Jö süi perdü, puve vu mede ?"),
    ("daily", "Saat kaçta açılıyor?", "What time does it open?", "Vat taym daz it oupın?", "Wann öffnet es?", "Van öfnıt es?", "A che ora apre?", "A ke ora apre?", "¿A qué hora abre?", "A ke ora abre?", "À quelle heure ça ouvre ?", "A kel ör sa uvr ?"),
    ("daily", "Bugün kapalı mı?", "Is it closed today?", "İz it klozd tudey?", "Ist es heute geschlossen?", "İst es hoytı geşlosın?", "È chiuso oggi?", "E kiyuzo oci?", "¿Está cerrado hoy?", "Esta serrado oy?", "Est-ce fermé aujourd'hui ?", "Es ferme ojurdüi ?"),
    ("daily", "Bir dakika", "One moment", "Van moumınt", "Einen Moment", "Aynın Momınt", "Un momento", "Un momento", "Un momento", "Un momento", "Un moment", "Ön moman"),
    ("daily", "Problem yok", "No problem", "No problım", "Kein Problem", "Kayn Problem", "Nessun problema", "Nessun problema", "No hay problema", "No ay problema", "Pas de problème", "Pa dö problem"),

    # ── places (8) ─────────────────────────────────────────────────────
    ("places", "Okul", "School", "Skuul", "Schule", "Şule", "Scuola", "Skuola", "Escuela", "Eskuyela", "École", "Ekol"),
    ("places", "Restoran", "Restaurant", "Restıront", "Restaurant", "Restorant", "Ristorante", "Ristorante", "Restaurante", "Restaurante", "Restaurant", "Restoran"),
    ("places", "Market", "Supermarket", "Supımarket", "Supermarkt", "Zupermarkt", "Supermercato", "Supermerkato", "Supermercado", "Supermerkado", "Supermarché", "Süpermarşe"),
    ("places", "Banka", "Bank", "Benk", "Bank", "Bank", "Banca", "Banka", "Banco", "Banko", "Banque", "Bank"),
    ("places", "Müze", "Museum", "Myuuziım", "Museum", "Muzeum", "Museo", "Muzeo", "Museo", "Museo", "Musée", "Müze"),
    ("places", "Park", "Park", "Park", "Park", "Park", "Parco", "Parko", "Parque", "Parke", "Parc", "Park"),
    ("places", "Plaj", "Beach", "Biç", "Strand", "Ştrant", "Spiaggia", "Spiyacca", "Playa", "Playa", "Plage", "Plaj"),
    ("places", "Kütüphane", "Library", "Laybrıri", "Bibliothek", "Bibliotek", "Biblioteca", "Biblioteka", "Biblioteca", "Biblioteka", "Bibliothèque", "Bibliyotek"),

    # ── greetings (ek +10) ────────────────────────────────────────────
    ("greetings", "Selam", "Hi", "Hay", "Hi", "Hay", "Salve", "Salve", "Saludos", "Saludos", "Salut", "Salü"),
    ("greetings", "Güle güle", "Bye", "Bay", "Tschüss", "Çüs", "Addio", "Addiyo", "Chao", "Çao", "Au revoir", "O rövuar"),
    ("greetings", "Tekrar hoş geldiniz", "Welcome back", "Velkım bek", "Willkommen zurück", "Vilkomın tsurük", "Bentornato", "Bentornato", "Bienvenido de nuevo", "Biyenvenido de nuyevo", "Bienvenue de retour", "Biyenvönü dö rötür"),
    ("greetings", "İyi öğlenler", "Good afternoon", "Gud aftırnuun", "Guten Nachmittag", "Gutn Nahmittak", "Buon pomeriggio", "Buon pomericco", "Buenas tardes", "Buyenas tardes", "Bon après-midi", "Bon apre midi"),
    ("greetings", "Çok naziksiniz", "You are very kind", "Yu ar veri kaynd", "Sie sind sehr nett", "Zi zint zer net", "Lei è molto gentile", "Ley e molto centile", "Usted es muy amable", "Usted es muy amable", "Vous êtes très gentil", "Vu zet tre jantiy"),
    ("greetings", "Memnuniyetle", "With pleasure", "Vid plejır", "Mit Vergnügen", "Mit Fergnügın", "Con piacere", "Kon piyaçere", "Con mucho gusto", "Kon muço gusto", "Avec plaisir", "Avek plezir"),
    ("greetings", "Tebrikler", "Congratulations", "Kongreçuleyşıns", "Herzlichen Glückwunsch", "Hertslihın Glükvunş", "Congratulazioni", "Kongratulatsyoni", "Felicidades", "Felisidades", "Félicitations", "Felisitasyon"),
    ("greetings", "İyi şanslar", "Good luck", "Gud lak", "Viel Glück", "Fil Glük", "Buona fortuna", "Buona fortuna", "Buena suerte", "Buyena suyerte", "Bonne chance", "Bon şans"),
    ("greetings", "İyi yolculuklar", "Have a nice trip", "Hev e nays trip", "Gute Reise", "Gutı Rayzı", "Buon viaggio", "Buon viacco", "Buen viaje", "Buyen biyahe", "Bon voyage", "Bon vuyaj"),
    ("greetings", "Kendine iyi bak", "Take care", "Teyk ker", "Pass auf dich auf", "Pas auf dih auf", "Abbi cura di te", "Abbi kura di te", "Cuídate", "Kuydate", "Prends soin de toi", "Pran suen dö tua"),

    # ── numbers (ek +5) ───────────────────────────────────────────────
    ("numbers", "Altmış", "Sixty", "Siksti", "Sechzig", "Zehtsih", "Sessanta", "Sessanta", "Sesenta", "Sesenta", "Soixante", "Suasant"),
    ("numbers", "Yetmiş", "Seventy", "Sevınti", "Siebzig", "Zibtsih", "Settanta", "Settanta", "Setenta", "Setenta", "Soixante-dix", "Suasant dis"),
    ("numbers", "Seksen", "Eighty", "Eyti", "Achtzig", "Ahttsih", "Ottanta", "Ottanta", "Ochenta", "Oçenta", "Quatre-vingts", "Katr ven"),
    ("numbers", "Doksan", "Ninety", "Naynti", "Neunzig", "Noyntsih", "Novanta", "Novanta", "Noventa", "Nobenta", "Quatre-vingt-dix", "Katr ven dis"),
    ("numbers", "Sıfır", "Zero", "Ziiro", "Null", "Nul", "Zero", "Dzero", "Cero", "Sero", "Zéro", "Zero"),

    # ── time (ek +7) ─────────────────────────────────────────────────
    ("time", "Perşembe", "Thursday", "Törzdey", "Donnerstag", "Donırstak", "Giovedì", "Covedi", "Jueves", "Huyeves", "Jeudi", "Jödi"),
    ("time", "Cuma", "Friday", "Fraydey", "Freitag", "Fraytak", "Venerdì", "Venerdi", "Viernes", "Biyernes", "Vendredi", "Vandredi"),
    ("time", "Cumartesi", "Saturday", "Setırdey", "Samstag", "Zamstak", "Sabato", "Sabato", "Sábado", "Sabado", "Samedi", "Samdi"),
    ("time", "Pazar", "Sunday", "Sandey", "Sonntag", "Zontak", "Domenica", "Domenika", "Domingo", "Domingo", "Dimanche", "Dimanş"),
    ("time", "Dakika", "Minute", "Minit", "Minute", "Minutı", "Minuto", "Minuto", "Minuto", "Minuto", "Minute", "Minüt"),
    ("time", "Saniye", "Second", "Sekınd", "Sekunde", "Zekundı", "Secondo", "Sekondo", "Segundo", "Segundo", "Seconde", "Sögond"),
    ("time", "Gün", "Day", "Dey", "Tag", "Tak", "Giorno", "Corno", "Día", "Diya", "Jour", "Jur"),

    # ── family (ek +5) ────────────────────────────────────────────────
    ("family", "Amca", "Uncle", "Ankıl", "Onkel", "Onkıl", "Zio", "Tsiyo", "Tío", "Tiyo", "Oncle", "Onkl"),
    ("family", "Teyze", "Aunt", "Ant", "Tante", "Tantı", "Zia", "Tsiya", "Tía", "Tiya", "Tante", "Tant"),
    ("family", "Kuzen", "Cousin", "Kazın", "Cousin", "Kuzın", "Cugino", "Kucino", "Primo", "Primo", "Cousin", "Kuzen"),
    ("family", "Yeğen", "Nephew/Niece", "Nefyu/Niis", "Neffe/Nichte", "Nefı/Nihtı", "Nipote", "Nipote", "Sobrino/a", "Sobrino/a", "Neveu/Nièce", "Növö/Niyes"),
    ("family", "Bebek", "Baby", "Beybi", "Baby", "Beybi", "Bambino", "Bambino", "Bebé", "Bebe", "Bébé", "Bebe"),

    # ── food (ek +10) ─────────────────────────────────────────────────
    ("food", "Makarna", "Pasta", "Pasta", "Nudeln", "Nudıln", "Pasta", "Pasta", "Pasta", "Pasta", "Pâtes", "Pat"),
    ("food", "Çorba", "Soup", "Suup", "Suppe", "Zupı", "Zuppa", "Tsuppa", "Sopa", "Sopa", "Soupe", "Sup"),
    ("food", "Salata", "Salad", "Selıd", "Salat", "Zalat", "Insalata", "İnsalata", "Ensalada", "Ensalada", "Salade", "Salad"),
    ("food", "Dondurma", "Ice cream", "Ays kriim", "Eis", "Ays", "Gelato", "Celato", "Helado", "Elado", "Glace", "Glas"),
    ("food", "Kek", "Cake", "Keyk", "Kuchen", "Kuhın", "Torta", "Torta", "Pastel", "Pastel", "Gâteau", "Gato"),
    ("food", "Tereyağı", "Butter", "Batır", "Butter", "Butır", "Burro", "Burro", "Mantequilla", "Mantekiya", "Beurre", "Bör"),
    ("food", "Bal", "Honey", "Hani", "Honig", "Honih", "Miele", "Miyele", "Miel", "Miyel", "Miel", "Miyel"),
    ("food", "Zeytin", "Olive", "Oliv", "Olive", "Olivı", "Oliva", "Oliva", "Aceituna", "Aseytuna", "Olive", "Oliv"),
    ("food", "Patates", "Potato", "Poteyto", "Kartoffel", "Kartofıl", "Patata", "Patata", "Patata", "Patata", "Pomme de terre", "Pom dö ter"),
    ("food", "Domates", "Tomato", "Tomeyto", "Tomate", "Tomatı", "Pomodoro", "Pomodoro", "Tomate", "Tomate", "Tomate", "Tomat"),

    # ── shopping (ek +8) ──────────────────────────────────────────────
    ("shopping", "Mağaza", "Store", "Stor", "Geschäft", "Geşeft", "Negozio", "Negotsyo", "Tienda", "Tiyenda", "Magasin", "Magazen"),
    ("shopping", "Fiyat", "Price", "Prays", "Preis", "Prays", "Prezzo", "Prettso", "Precio", "Presyo", "Prix", "Pri"),
    ("shopping", "Kasa", "Cash register", "Keş recistır", "Kasse", "Kassı", "Cassa", "Kassa", "Caja", "Kaha", "Caisse", "Kes"),
    ("shopping", "Çanta", "Bag", "Beg", "Tasche", "Taşı", "Borsa", "Borsa", "Bolsa", "Bolsa", "Sac", "Sak"),
    ("shopping", "Değişim", "Exchange", "İksçeync", "Umtausch", "Umtauş", "Cambio", "Kambiyo", "Cambio", "Kambiyo", "Échange", "Eşanj"),
    ("shopping", "Kalite", "Quality", "Kvolıti", "Qualität", "Kvalitet", "Qualità", "Kualita", "Calidad", "Kalidad", "Qualité", "Kalite"),
    ("shopping", "Vitrin", "Window display", "Vindou displey", "Schaufenster", "Şaufenstır", "Vetrina", "Vetrina", "Escaparate", "Eskaparate", "Vitrine", "Vitrin"),
    ("shopping", "Garanti", "Warranty", "Vorınti", "Garantie", "Garanti", "Garanzia", "Garantsiya", "Garantía", "Garantiya", "Garantie", "Garanti"),

    # ── travel (ek +7) ────────────────────────────────────────────────
    ("travel", "Vize", "Visa", "Viiza", "Visum", "Vizum", "Visto", "Visto", "Visa", "Bisa", "Visa", "Viza"),
    ("travel", "Gümrük", "Customs", "Kastımz", "Zoll", "Tsol", "Dogana", "Dogana", "Aduana", "Aduana", "Douane", "Duan"),
    ("travel", "Liman", "Port", "Port", "Hafen", "Hafın", "Porto", "Porto", "Puerto", "Puyerto", "Port", "Por"),
    ("travel", "İstasyon", "Station", "Steyşın", "Bahnhof", "Banhof", "Stazione", "Statsyone", "Estación", "Estasyon", "Gare", "Gar"),
    ("travel", "Uçuş", "Flight", "Flayt", "Flug", "Flug", "Volo", "Volo", "Vuelo", "Buyelo", "Vol", "Vol"),
    ("travel", "Bagaj", "Luggage", "Lagıc", "Gepäck", "Gepek", "Bagaglio", "Bagalyo", "Equipaje", "Ekipahe", "Bagage", "Bagaj"),
    ("travel", "Kalkış", "Departure", "Dipaarçır", "Abfahrt", "Apfart", "Partenza", "Partentsa", "Salida", "Salida", "Départ", "Depar"),

    # ── health (ek +6) ────────────────────────────────────────────────
    ("health", "Ağrı", "Pain", "Peyn", "Schmerz", "Şmerts", "Dolore", "Dolore", "Dolor", "Dolor", "Douleur", "Dulör"),
    ("health", "Öksürük", "Cough", "Kof", "Husten", "Hustın", "Tosse", "Tosse", "Tos", "Tos", "Toux", "Tu"),
    ("health", "Grip", "Flu", "Flu", "Grippe", "Grippı", "Influenza", "İnfluyentsa", "Gripe", "Gripe", "Grippe", "Grip"),
    ("health", "Yara", "Wound", "Vuund", "Wunde", "Vundı", "Ferita", "Ferita", "Herida", "Erida", "Blessure", "Blesür"),
    ("health", "Tansiyon", "Blood pressure", "Blad preşır", "Blutdruck", "Blutdruk", "Pressione", "Pressyone", "Presión", "Presiyon", "Tension artérielle", "Tansyon arteriyel"),
    ("health", "Muayene", "Examination", "İgzemineyşın", "Untersuchung", "Untırzuhung", "Visita medica", "Vizita medika", "Consulta", "Konsulta", "Examen médical", "Egzamen medikal"),

    # ── adjectives (ek +8) ────────────────────────────────────────────
    ("adjectives", "Ağır", "Heavy", "Hevi", "Schwer", "Şver", "Pesante", "Pezante", "Pesado", "Pesado", "Lourd", "Lur"),
    ("adjectives", "Hafif", "Light", "Layt", "Leicht", "Layht", "Leggero", "Leccero", "Ligero", "Lihero", "Léger", "Leje"),
    ("adjectives", "Temiz", "Clean", "Kliin", "Sauber", "Zaubır", "Pulito", "Pulito", "Limpio", "Limpiyo", "Propre", "Propr"),
    ("adjectives", "Kirli", "Dirty", "Dörti", "Schmutzig", "Şmutsih", "Sporco", "Sporko", "Sucio", "Susyo", "Sale", "Sal"),
    ("adjectives", "Zengin", "Rich", "Riç", "Reich", "Rayh", "Ricco", "Rikko", "Rico", "Riko", "Riche", "Riş"),
    ("adjectives", "Fakir", "Poor", "Pur", "Arm", "Arm", "Povero", "Povero", "Pobre", "Pobre", "Pauvre", "Povr"),
    ("adjectives", "Dolu", "Full", "Ful", "Voll", "Fol", "Pieno", "Piyeno", "Lleno", "Yeno", "Plein", "Plen"),
    ("adjectives", "Boş", "Empty", "Empti", "Leer", "Leer", "Vuoto", "Vuoto", "Vacío", "Basiyo", "Vide", "Vid"),

    # ── verbs (ek +10) ────────────────────────────────────────────────
    ("verbs", "Koşmak", "To run", "Tu ran", "Laufen", "Laufın", "Correre", "Korrere", "Correr", "Korrer", "Courir", "Kurir"),
    ("verbs", "Yüzmek", "To swim", "Tu svim", "Schwimmen", "Şvimın", "Nuotare", "Nuotare", "Nadar", "Nadar", "Nager", "Naje"),
    ("verbs", "Düşünmek", "To think", "Tu tink", "Denken", "Denkın", "Pensare", "Pensare", "Pensar", "Pensar", "Penser", "Panse"),
    ("verbs", "Hatırlamak", "To remember", "Tu rimembır", "Erinnern", "Erinnırn", "Ricordare", "Rikordare", "Recordar", "Rekordar", "Se souvenir", "Sö suvnir"),
    ("verbs", "Unutmak", "To forget", "Tu forget", "Vergessen", "Fergesın", "Dimenticare", "Dimentikare", "Olvidar", "Olbidar", "Oublier", "Ubliye"),
    ("verbs", "Açmak", "To open", "Tu oupın", "Öffnen", "Öfnın", "Aprire", "Aprire", "Abrir", "Abrir", "Ouvrir", "Uvrir"),
    ("verbs", "Kapamak", "To close", "Tu klouz", "Schließen", "Şlisın", "Chiudere", "Kiyudere", "Cerrar", "Serrar", "Fermer", "Ferme"),
    ("verbs", "Beklemek", "To wait", "Tu veyt", "Warten", "Vartın", "Aspettare", "Aspettare", "Esperar", "Esperar", "Attendre", "Atandr"),
    ("verbs", "Aramak", "To search", "Tu sörç", "Suchen", "Zuhın", "Cercare", "Çerkare", "Buscar", "Buskar", "Chercher", "Şerşe"),
    ("verbs", "Taşımak", "To carry", "Tu keri", "Tragen", "Tragın", "Portare", "Portare", "Llevar", "Yevar", "Porter", "Porte"),

    # ── daily (ek +7) ─────────────────────────────────────────────────
    ("daily", "Çok teşekkürler", "Thank you very much", "Tenk yu veri maç", "Vielen Dank", "Filın Dank", "Grazie mille", "Gratsiye mille", "Muchas gracias", "Muças grasyas", "Merci beaucoup", "Mersi boku"),
    ("daily", "Bunu sevdim", "I like this", "Ay layk dis", "Das gefällt mir", "Das gefelt mir", "Mi piace questo", "Mi piyaçe kuesto", "Me gusta esto", "Me gusta esto", "J'aime ça", "Jem sa"),
    ("daily", "Ne kadar sürer?", "How long does it take?", "Hav long daz it teyk?", "Wie lange dauert es?", "Vi langı dauırt es?", "Quanto tempo ci vuole?", "Kuanto tempo çi vuole?", "¿Cuánto tiempo tarda?", "Kuanto tiyempo tarda?", "Combien de temps ?", "Konbiyen dö tan ?"),
    ("daily", "Nereden geliyorsunuz?", "Where are you from?", "Ver ar yu from?", "Woher kommen Sie?", "Voher komın zi?", "Da dove viene?", "Da dove viyene?", "¿De dónde es usted?", "De donde es usted?", "D'où venez-vous ?", "Du vöne vu ?"),
    ("daily", "Burada oturuyorum", "I live here", "Ay liv hiir", "Ich wohne hier", "İh vonı hir", "Abito qui", "Abito kui", "Vivo aquí", "Bibo aki", "J'habite ici", "Jabit isi"),
    ("daily", "Çok güzel!", "Very nice!", "Veri nays!", "Sehr schön!", "Zer şön!", "Molto bello!", "Molto bello!", "¡Muy bonito!", "Muy bonito!", "Très beau !", "Tre bo !"),
    ("daily", "Emin misiniz?", "Are you sure?", "Ar yu şur?", "Sind Sie sicher?", "Zint zi zihır?", "È sicuro?", "E sikuro?", "¿Está seguro?", "Esta seguro?", "Êtes-vous sûr ?", "Et vu sür ?"),

    # ── places (ek +7) ────────────────────────────────────────────────
    ("places", "Hastane", "Hospital", "Hospitıl", "Krankenhaus", "Krankınhaus", "Ospedale", "Ospedale", "Hospital", "Ospital", "Hôpital", "Opital"),
    ("places", "Kilise", "Church", "Çörç", "Kirche", "Kirhı", "Chiesa", "Kiyeza", "Iglesia", "İglesya", "Église", "Egliz"),
    ("places", "Cami", "Mosque", "Mosk", "Moschee", "Moşe", "Moschea", "Moskea", "Mezquita", "Meskita", "Mosquée", "Moske"),
    ("places", "Postane", "Post office", "Post ofis", "Postamt", "Postamt", "Ufficio postale", "Uffiço postale", "Oficina de correos", "Ofisina de korreos", "Bureau de poste", "Büro dö post"),
    ("places", "Stadyum", "Stadium", "Steydiyım", "Stadion", "Ştadiyon", "Stadio", "Stadiyo", "Estadio", "Estadiyo", "Stade", "Stad"),
    ("places", "Sinema", "Cinema", "Sinıma", "Kino", "Kino", "Cinema", "Çinema", "Cine", "Sine", "Cinéma", "Sinema"),
    ("places", "Tiyatro", "Theater", "Tiıtır", "Theater", "Teatır", "Teatro", "Teatro", "Teatro", "Teatro", "Théâtre", "Teatr"),

    # ── weather (yeni, 25) ────────────────────────────────────────────
    ("weather", "Yağmur", "Rain", "Reyn", "Regen", "Regın", "Pioggia", "Piyocca", "Lluvia", "Yuviya", "Pluie", "Plüi"),
    ("weather", "Kar", "Snow", "Snou", "Schnee", "Şne", "Neve", "Neve", "Nieve", "Niyeve", "Neige", "Nej"),
    ("weather", "Güneş", "Sun", "San", "Sonne", "Zonnı", "Sole", "Sole", "Sol", "Sol", "Soleil", "Soley"),
    ("weather", "Bulut", "Cloud", "Klaud", "Wolke", "Volkı", "Nuvola", "Nuvola", "Nube", "Nube", "Nuage", "Nüaj"),
    ("weather", "Rüzgar", "Wind", "Vind", "Wind", "Vint", "Vento", "Vento", "Viento", "Biyento", "Vent", "Van"),
    ("weather", "Sıcak", "Hot", "Hot", "Heiß", "Hays", "Caldo", "Kaldo", "Caluroso", "Kaluroso", "Chaud", "Şo"),
    ("weather", "Soğuk", "Cold", "Kold", "Kalt", "Kalt", "Freddo", "Freddo", "Frío", "Friyo", "Froid", "Frua"),
    ("weather", "Fırtına", "Storm", "Storm", "Sturm", "Ştorm", "Tempesta", "Tempesta", "Tormenta", "Tormenta", "Tempête", "Tanpet"),
    ("weather", "Sis", "Fog", "Fog", "Nebel", "Nebıl", "Nebbia", "Nebbiya", "Niebla", "Niyebla", "Brouillard", "Bruyar"),
    ("weather", "Şemsiye", "Umbrella", "Ambrela", "Regenschirm", "Regınşirm", "Ombrello", "Ombrello", "Paraguas", "Paraguas", "Parapluie", "Paraplüi"),
    ("weather", "Sıcaklık", "Temperature", "Temprıçır", "Temperatur", "Temperatır", "Temperatura", "Temperatura", "Temperatura", "Temperatura", "Température", "Tanperatür"),
    ("weather", "Nemli", "Humid", "Hyuumid", "Feucht", "Foyht", "Umido", "Umido", "Húmedo", "Umedo", "Humide", "Ümid"),
    ("weather", "Kuru", "Dry", "Dray", "Trocken", "Trokın", "Secco", "Sekko", "Seco", "Seko", "Sec", "Sek"),
    ("weather", "Hava tahmini", "Forecast", "Forkast", "Vorhersage", "Forherzagı", "Previsione", "Previzyone", "Pronóstico", "Pronostiko", "Prévisions météo", "Previzyon meteo"),
    ("weather", "Mevsim", "Season", "Siizın", "Jahreszeit", "Yarestsayt", "Stagione", "Stacone", "Estación", "Estasyon", "Saison", "Sezon"),
    ("weather", "İlkbahar", "Spring", "Spring", "Frühling", "Früling", "Primavera", "Primavera", "Primavera", "Primavera", "Printemps", "Prentan"),
    ("weather", "Sonbahar", "Autumn", "Otım", "Herbst", "Herpst", "Autunno", "Autunno", "Otoño", "Otonyo", "Automne", "Oton"),
    ("weather", "Don", "Frost", "Frost", "Frost", "Frost", "Gelo", "Celo", "Escarcha", "Eskarça", "Gel", "Jel"),
    ("weather", "Gök gürültüsü", "Thunder", "Tandır", "Donner", "Donnır", "Tuono", "Tuono", "Trueno", "Truyeno", "Tonnerre", "Toner"),
    ("weather", "Şimşek", "Lightning", "Laytning", "Blitz", "Blits", "Fulmine", "Fulmine", "Relámpago", "Relampago", "Éclair", "Ekler"),
    ("weather", "Gökkuşağı", "Rainbow", "Reynbou", "Regenbogen", "Regınbogın", "Arcobaleno", "Arkobaleno", "Arcoíris", "Arkoiris", "Arc-en-ciel", "Ark an siyel"),
    ("weather", "Açık hava", "Clear sky", "Kliir skay", "Klarer Himmel", "Klarır Himmıl", "Cielo sereno", "Çiyelo sereno", "Cielo despejado", "Siyelo despeado", "Ciel dégagé", "Siyel degaje"),
    ("weather", "Bulutlu", "Cloudy", "Klaudi", "Bewölkt", "Bevölkt", "Nuvoloso", "Nuvolozo", "Nublado", "Nublado", "Nuageux", "Nüajö"),
    ("weather", "Ilık", "Warm", "Vorm", "Warm", "Varm", "Tiepido", "Tiyepido", "Templado", "Templado", "Tiède", "Tiyed"),
    ("weather", "Serin", "Cool", "Kuul", "Kühl", "Kül", "Fresco", "Fresko", "Fresco", "Fresko", "Frais", "Fre"),

    # ── clothing (yeni, 25) ───────────────────────────────────────────
    ("clothing", "Gömlek", "Shirt", "Şört", "Hemd", "Hemt", "Camicia", "Kamiça", "Camisa", "Kamisa", "Chemise", "Şömiz"),
    ("clothing", "Pantolon", "Pants", "Pents", "Hose", "Hozı", "Pantaloni", "Pantaloni", "Pantalones", "Pantalones", "Pantalon", "Pantalon"),
    ("clothing", "Elbise", "Dress", "Dres", "Kleid", "Klayt", "Vestito", "Vestito", "Vestido", "Bestido", "Robe", "Rob"),
    ("clothing", "Ayakkabı", "Shoes", "Şuuz", "Schuhe", "Şuı", "Scarpe", "Skarpe", "Zapatos", "Sapatos", "Chaussures", "Şosür"),
    ("clothing", "Şapka", "Hat", "Het", "Hut", "Hut", "Cappello", "Kappello", "Sombrero", "Sombrero", "Chapeau", "Şapo"),
    ("clothing", "Palto", "Coat", "Kout", "Mantel", "Mantıl", "Cappotto", "Kappotto", "Abrigo", "Abrigo", "Manteau", "Manto"),
    ("clothing", "Ceket", "Jacket", "Cekit", "Jacke", "Yakı", "Giacca", "Cakka", "Chaqueta", "Çaketa", "Veste", "Vest"),
    ("clothing", "Çorap", "Socks", "Soks", "Socken", "Zokın", "Calze", "Kaltse", "Calcetines", "Kalsetines", "Chaussettes", "Şoset"),
    ("clothing", "Atkı", "Scarf", "Skarf", "Schal", "Şal", "Sciarpa", "Şarpa", "Bufanda", "Bufanda", "Écharpe", "Eşarp"),
    ("clothing", "Eldiven", "Gloves", "Glavz", "Handschuhe", "Hantşuı", "Guanti", "Guanti", "Guantes", "Guantes", "Gants", "Gan"),
    ("clothing", "Çizme", "Boots", "Buuts", "Stiefel", "Ştifıl", "Stivali", "Stivali", "Botas", "Botas", "Bottes", "Bot"),
    ("clothing", "Etek", "Skirt", "Skürt", "Rock", "Rok", "Gonna", "Gonna", "Falda", "Falda", "Jupe", "Jüp"),
    ("clothing", "Kravat", "Tie", "Tay", "Krawatte", "Kravattı", "Cravatta", "Kravatta", "Corbata", "Korbata", "Cravate", "Kravat"),
    ("clothing", "Kemer", "Belt", "Belt", "Gürtel", "Gürtıl", "Cintura", "Çintura", "Cinturón", "Sinturon", "Ceinture", "Sentür"),
    ("clothing", "Gözlük", "Glasses", "Glasız", "Brille", "Brillı", "Occhiali", "Okkiyali", "Gafas", "Gafas", "Lunettes", "Lünet"),
    ("clothing", "Kol saati", "Watch", "Voç", "Armbanduhr", "Armbandur", "Orologio", "Oroloco", "Reloj", "Reloh", "Montre", "Montr"),
    ("clothing", "Yüzük", "Ring", "Ring", "Ring", "Ring", "Anello", "Anello", "Anillo", "Aniyo", "Bague", "Bag"),
    ("clothing", "Kolye", "Necklace", "Neklis", "Halskette", "Halskettı", "Collana", "Kollana", "Collar", "Koyar", "Collier", "Koliye"),
    ("clothing", "Çanta", "Bag", "Beg", "Tasche", "Taşı", "Borsa", "Borsa", "Bolso", "Bolso", "Sac", "Sak"),
    ("clothing", "Cep", "Pocket", "Pokıt", "Tasche", "Taşı", "Tasca", "Taska", "Bolsillo", "Bolsiyo", "Poche", "Poş"),
    ("clothing", "Düğme", "Button", "Batın", "Knopf", "Knopf", "Bottone", "Bottone", "Botón", "Boton", "Bouton", "Buton"),
    ("clothing", "Fermuar", "Zipper", "Zipır", "Reißverschluss", "Raysfırşlus", "Cerniera", "Çerniyera", "Cremallera", "Kremayera", "Fermeture éclair", "Fermötür ekler"),
    ("clothing", "Kol", "Sleeve", "Sliiv", "Ärmel", "Ermıl", "Manica", "Manika", "Manga", "Manga", "Manche", "Manş"),
    ("clothing", "Yaka", "Collar", "Kolır", "Kragen", "Kragın", "Colletto", "Kolletto", "Cuello", "Kuweyo", "Col", "Kol"),
    ("clothing", "İç çamaşırı", "Underwear", "Andırver", "Unterwäsche", "Untırveşı", "Biancheria intima", "Biyankeria intima", "Ropa interior", "Ropa interiyor", "Sous-vêtements", "Su vetman"),

    # ── education (yeni, 25) ──────────────────────────────────────────
    ("education", "Okul", "School", "Skuul", "Schule", "Şulı", "Scuola", "Skuola", "Escuela", "Eskuyela", "École", "Ekol"),
    ("education", "Öğretmen", "Teacher", "Tiçır", "Lehrer", "Lerır", "Insegnante", "İnsenyante", "Profesor", "Profesor", "Professeur", "Profesör"),
    ("education", "Öğrenci", "Student", "Studınt", "Schüler", "Şülır", "Studente", "Studente", "Estudiante", "Estudiyante", "Étudiant", "Etüdiyan"),
    ("education", "Kitap", "Book", "Buk", "Buch", "Buh", "Libro", "Libro", "Libro", "Libro", "Livre", "Livr"),
    ("education", "Kalem", "Pen", "Pen", "Kugelschreiber", "Kugelşraybır", "Penna", "Penna", "Bolígrafo", "Boligrafo", "Stylo", "Stilo"),
    ("education", "Kurşun kalem", "Pencil", "Pensıl", "Bleistift", "Blayştift", "Matita", "Matita", "Lápiz", "Lapis", "Crayon", "Kreyon"),
    ("education", "Defter", "Notebook", "Noutbuk", "Heft", "Heft", "Quaderno", "Kuaderno", "Cuaderno", "Kuaderno", "Cahier", "Kaye"),
    ("education", "Sınıf", "Classroom", "Klasruum", "Klassenzimmer", "Klasıntsimmır", "Aula", "Aula", "Aula", "Aula", "Classe", "Klas"),
    ("education", "Ödev", "Homework", "Houmvörk", "Hausaufgabe", "Hausaufgabı", "Compiti", "Kompiti", "Tarea", "Tarea", "Devoir", "Dövuar"),
    ("education", "Sınav", "Exam", "İgzem", "Prüfung", "Prüfung", "Esame", "Ezame", "Examen", "Eksamen", "Examen", "Egzamen"),
    ("education", "Not", "Grade", "Greyd", "Note", "Notı", "Voto", "Voto", "Nota", "Nota", "Note", "Not"),
    ("education", "Ders", "Lesson", "Lesın", "Unterricht", "Untırriht", "Lezione", "Letsyone", "Lección", "Leksyon", "Leçon", "Löson"),
    ("education", "Öğrenmek", "To learn", "Tu lörn", "Lernen", "Lernın", "Imparare", "İmparare", "Aprender", "Aprender", "Apprendre", "Aprandr"),
    ("education", "Çalışmak", "To study", "Tu stadi", "Studieren", "Ştudirın", "Studiare", "Studiyare", "Estudiar", "Estudiyar", "Travailler", "Travaye"),
    ("education", "Kütüphane", "Library", "Laybrıri", "Bibliothek", "Bibliotek", "Biblioteca", "Biblioteka", "Biblioteca", "Biblioteka", "Bibliothèque", "Bibliyotek"),
    ("education", "Üniversite", "University", "Yunivörsiti", "Universität", "Universitaet", "Università", "Universita", "Universidad", "Unibersidad", "Université", "Üniversite"),
    ("education", "Diploma", "Diploma", "Diploma", "Diplom", "Diplom", "Diploma", "Diploma", "Diploma", "Diploma", "Diplôme", "Diplom"),
    ("education", "Bilgi", "Knowledge", "Nolıc", "Wissen", "Visın", "Conoscenza", "Konoşentsa", "Conocimiento", "Konosimiyento", "Connaissance", "Konesans"),
    ("education", "Yazı tahtası", "Blackboard", "Blekbord", "Tafel", "Tafıl", "Lavagna", "Lavanya", "Pizarra", "Pisarra", "Tableau noir", "Tablo nuar"),
    ("education", "Tebeşir", "Chalk", "Çok", "Kreide", "Kraydı", "Gesso", "Cesso", "Tiza", "Tisa", "Craie", "Kre"),
    ("education", "Silgi", "Eraser", "İreyzır", "Radiergummi", "Radirgummi", "Gomma", "Gomma", "Borrador", "Borrador", "Gomme", "Gom"),
    ("education", "Cetvel", "Ruler", "Ruulır", "Lineal", "Lineal", "Righello", "Rigello", "Regla", "Regla", "Règle", "Regl"),
    ("education", "Makas", "Scissors", "Sizırz", "Schere", "Şerı", "Forbici", "Forbiçi", "Tijeras", "Tiheras", "Ciseaux", "Sizo"),
    ("education", "Kağıt", "Paper", "Peypır", "Papier", "Papir", "Carta", "Karta", "Papel", "Papel", "Papier", "Papiye"),
    ("education", "Sözlük", "Dictionary", "Dikşıneri", "Wörterbuch", "Vörtırbuh", "Dizionario", "Ditsyonaryo", "Diccionario", "Diksiyonaryo", "Dictionnaire", "Diksiyoner"),

    # ── emotions (yeni, 25) ───────────────────────────────────────────
    ("emotions", "Mutlu", "Happy", "Hepi", "Glücklich", "Glüklih", "Felice", "Feliçe", "Feliz", "Felis", "Heureux", "Örö"),
    ("emotions", "Üzgün", "Sad", "Sed", "Traurig", "Traurih", "Triste", "Triste", "Triste", "Triste", "Triste", "Trist"),
    ("emotions", "Kızgın", "Angry", "Engri", "Wütend", "Vütınt", "Arrabbiato", "Arrabbiyato", "Enfadado", "Enfadado", "En colère", "An koler"),
    ("emotions", "Korkmuş", "Scared", "Skerd", "Ängstlich", "Enstlih", "Spaventato", "Spaventato", "Asustado", "Asustado", "Effrayé", "Efreye"),
    ("emotions", "Şaşkın", "Surprised", "Sırprayzd", "Überrascht", "Überraşt", "Sorpreso", "Sorprezo", "Sorprendido", "Sorprendido", "Surpris", "Sürpri"),
    ("emotions", "Yorgun", "Tired", "Tayırd", "Müde", "Müdı", "Stanco", "Stanko", "Cansado", "Kansado", "Fatigué", "Fatige"),
    ("emotions", "Sıkılmış", "Bored", "Bord", "Gelangweilt", "Gelangvaylt", "Annoiato", "Annoyato", "Aburrido", "Aburrido", "Ennuyé", "Annüiye"),
    ("emotions", "Heyecanlı", "Excited", "İksaytıd", "Aufgeregt", "Aufgeregt", "Eccitato", "Eççitato", "Emocionado", "Emosyonado", "Excité", "Eksite"),
    ("emotions", "Endişeli", "Worried", "Vorid", "Besorgt", "Bezorgt", "Preoccupato", "Preokkupato", "Preocupado", "Preokupado", "Inquiet", "Enkiye"),
    ("emotions", "Gururlu", "Proud", "Praud", "Stolz", "Ştolts", "Orgoglioso", "Orgoliyozo", "Orgulloso", "Orguyoso", "Fier", "Fiyer"),
    ("emotions", "Kıskanç", "Jealous", "Celıs", "Eifersüchtig", "Ayfırzühtih", "Geloso", "Celozo", "Celoso", "Seloso", "Jaloux", "Jalu"),
    ("emotions", "Utangaç", "Shy", "Şay", "Schüchtern", "Şühtern", "Timido", "Timido", "Tímido", "Timido", "Timide", "Timid"),
    ("emotions", "Özgüvenli", "Confident", "Konfidınt", "Selbstbewusst", "Zelpstbevust", "Sicuro di sé", "Sikuro di se", "Seguro de sí", "Seguro de si", "Confiant", "Konfiyan"),
    ("emotions", "Yalnız", "Lonely", "Lounli", "Einsam", "Aynzam", "Solo", "Solo", "Solitario", "Solitaryo", "Seul", "Söl"),
    ("emotions", "Minnettar", "Grateful", "Greytfıl", "Dankbar", "Dankbar", "Grato", "Grato", "Agradecido", "Agradesido", "Reconnaissant", "Rökonessan"),
    ("emotions", "Gergin", "Nervous", "Növıs", "Nervös", "Nervös", "Nervoso", "Nervozo", "Nervioso", "Nerbiyoso", "Nerveux", "Nervö"),
    ("emotions", "Sakin", "Calm", "Kalm", "Ruhig", "Ruih", "Calmo", "Kalmo", "Tranquilo", "Trankilo", "Calme", "Kalm"),
    ("emotions", "Kafası karışık", "Confused", "Konfyuuzd", "Verwirrt", "Fervirt", "Confuso", "Konfuzo", "Confundido", "Konfundido", "Confus", "Konfü"),
    ("emotions", "Umutlu", "Hopeful", "Houpful", "Hoffnungsvoll", "Hofnungsfol", "Speranzoso", "Sperantsozo", "Esperanzado", "Esperansado", "Plein d'espoir", "Plen despuar"),
    ("emotions", "Hayal kırıklığı", "Disappointed", "Disıpointıd", "Enttäuscht", "Enttoyşt", "Deluso", "Deluzo", "Decepcionado", "Desepsyonado", "Déçu", "Desü"),
    ("emotions", "Aşk", "Love", "Lav", "Liebe", "Libı", "Amore", "Amore", "Amor", "Amor", "Amour", "Amur"),
    ("emotions", "Nefret", "Hate", "Heyt", "Hass", "Has", "Odio", "Odiyo", "Odio", "Odiyo", "Haine", "En"),
    ("emotions", "Gülmek", "To laugh", "Tu laf", "Lachen", "Lahın", "Ridere", "Ridere", "Reír", "Reir", "Rire", "Rir"),
    ("emotions", "Ağlamak", "To cry", "Tu kray", "Weinen", "Vaynın", "Piangere", "Piyancere", "Llorar", "Yorar", "Pleurer", "Plöre"),
    ("emotions", "Gülümsemek", "To smile", "Tu smayl", "Lächeln", "Lehıln", "Sorridere", "Sorridere", "Sonreír", "Sonreir", "Sourire", "Surir"),

    # ── nature (yeni, 25) ─────────────────────────────────────────────
    ("nature", "Ağaç", "Tree", "Trii", "Baum", "Baum", "Albero", "Albero", "Árbol", "Arbol", "Arbre", "Arbr"),
    ("nature", "Çiçek", "Flower", "Flavır", "Blume", "Blumı", "Fiore", "Fiyore", "Flor", "Flor", "Fleur", "Flör"),
    ("nature", "Nehir", "River", "Rivır", "Fluss", "Flus", "Fiume", "Fiyume", "Río", "Riyo", "Rivière", "Riviyer"),
    ("nature", "Dağ", "Mountain", "Mauntın", "Berg", "Berk", "Montagna", "Montanya", "Montaña", "Montanya", "Montagne", "Montany"),
    ("nature", "Deniz", "Sea", "Sii", "Meer", "Meer", "Mare", "Mare", "Mar", "Mar", "Mer", "Mer"),
    ("nature", "Güneş", "Sun", "San", "Sonne", "Zonnı", "Sole", "Sole", "Sol", "Sol", "Soleil", "Soley"),
    ("nature", "Ay", "Moon", "Muun", "Mond", "Mont", "Luna", "Luna", "Luna", "Luna", "Lune", "Lün"),
    ("nature", "Yıldız", "Star", "Star", "Stern", "Ştern", "Stella", "Stella", "Estrella", "Estreya", "Étoile", "Etual"),
    ("nature", "Gökyüzü", "Sky", "Skay", "Himmel", "Himmıl", "Cielo", "Çiyelo", "Cielo", "Siyelo", "Ciel", "Siyel"),
    ("nature", "Dünya", "Earth", "Öört", "Erde", "Erdı", "Terra", "Terra", "Tierra", "Tiyerra", "Terre", "Ter"),
    ("nature", "Orman", "Forest", "Forıst", "Wald", "Valt", "Foresta", "Foresta", "Bosque", "Boske", "Forêt", "Fore"),
    ("nature", "Göl", "Lake", "Leyk", "See", "Ze", "Lago", "Lago", "Lago", "Lago", "Lac", "Lak"),
    ("nature", "Tarla", "Field", "Fiild", "Feld", "Felt", "Campo", "Kampo", "Campo", "Kampo", "Champ", "Şan"),
    ("nature", "Bahçe", "Garden", "Gardın", "Garten", "Gartın", "Giardino", "Cardino", "Jardín", "Hardin", "Jardin", "Jarden"),
    ("nature", "Çimen", "Grass", "Gras", "Gras", "Gras", "Erba", "Erba", "Hierba", "İyerba", "Herbe", "Erb"),
    ("nature", "Yaprak", "Leaf", "Liif", "Blatt", "Blat", "Foglia", "Folya", "Hoja", "Oha", "Feuille", "Föy"),
    ("nature", "Taş", "Stone", "Stoun", "Stein", "Ştayn", "Pietra", "Piyetra", "Piedra", "Piyedra", "Pierre", "Piyer"),
    ("nature", "Kum", "Sand", "Send", "Sand", "Zant", "Sabbia", "Sabbiya", "Arena", "Arena", "Sable", "Sabl"),
    ("nature", "Ada", "Island", "Aylınd", "Insel", "İnzıl", "Isola", "İzola", "Isla", "İsla", "Île", "İl"),
    ("nature", "Vadi", "Valley", "Veli", "Tal", "Tal", "Valle", "Valle", "Valle", "Baye", "Vallée", "Vale"),
    ("nature", "Şelale", "Waterfall", "Votırfol", "Wasserfall", "Vasırfal", "Cascata", "Kaskata", "Cascada", "Kaskada", "Cascade", "Kaskad"),
    ("nature", "Bulut", "Cloud", "Klaud", "Wolke", "Volkı", "Nuvola", "Nuvola", "Nube", "Nube", "Nuage", "Nüaj"),
    ("nature", "Yağmur", "Rain", "Reyn", "Regen", "Regın", "Pioggia", "Piyocca", "Lluvia", "Yuviya", "Pluie", "Plüi"),
    ("nature", "Rüzgar", "Wind", "Vind", "Wind", "Vint", "Vento", "Vento", "Viento", "Biyento", "Vent", "Van"),
    ("nature", "Kar", "Snow", "Snou", "Schnee", "Şne", "Neve", "Neve", "Nieve", "Niyeve", "Neige", "Nej"),

    # ── professions (yeni, 25) ────────────────────────────────────────
    ("professions", "Doktor", "Doctor", "Doktır", "Arzt", "Artst", "Dottore", "Dottore", "Doctor", "Doktor", "Médecin", "Medsen"),
    ("professions", "Öğretmen", "Teacher", "Tiçır", "Lehrer", "Lerır", "Insegnante", "İnsenyante", "Profesor", "Profesor", "Professeur", "Profesör"),
    ("professions", "Mühendis", "Engineer", "Encinir", "Ingenieur", "İnjeniyör", "Ingegnere", "İncenyere", "Ingeniero", "İnheniyero", "Ingénieur", "Enjeniör"),
    ("professions", "Avukat", "Lawyer", "Loyır", "Anwalt", "Anvalt", "Avvocato", "Avvokato", "Abogado", "Abogado", "Avocat", "Avoka"),
    ("professions", "Aşçı", "Chef", "Şef", "Koch", "Koh", "Cuoco", "Kuoko", "Cocinero", "Kosinero", "Chef cuisinier", "Şef küiziniye"),
    ("professions", "Polis", "Police", "Poliis", "Polizist", "Politsist", "Poliziotto", "Politsiyotto", "Policía", "Polisiya", "Policier", "Polisiye"),
    ("professions", "İtfaiyeci", "Firefighter", "Fayırfaytır", "Feuerwehrmann", "Foyırverman", "Pompiere", "Pompiyere", "Bombero", "Bombero", "Pompier", "Ponpiye"),
    ("professions", "Şoför", "Driver", "Drayvır", "Fahrer", "Farır", "Autista", "Autista", "Conductor", "Konduktor", "Chauffeur", "Şoför"),
    ("professions", "Hemşire", "Nurse", "Nörs", "Krankenschwester", "Krankınşvestır", "Infermiera", "İnfermiyera", "Enfermera", "Enfermera", "Infirmière", "Enfirmiyer"),
    ("professions", "Çiftçi", "Farmer", "Farmır", "Bauer", "Bauır", "Agricoltore", "Agrikoltore", "Agricultor", "Agrikultor", "Agriculteur", "Agrikültör"),
    ("professions", "Sanatçı", "Artist", "Aartist", "Künstler", "Künstlır", "Artista", "Artista", "Artista", "Artista", "Artiste", "Artist"),
    ("professions", "Müzisyen", "Musician", "Myuzişın", "Musiker", "Muzikır", "Musicista", "Muziçista", "Músico", "Musiko", "Musicien", "Müzisiyen"),
    ("professions", "Yazar", "Writer", "Raytır", "Schriftsteller", "Şriftştelır", "Scrittore", "Skrittore", "Escritor", "Eskritor", "Écrivain", "Ekriven"),
    ("professions", "Pilot", "Pilot", "Paylıt", "Pilot", "Pilot", "Pilota", "Pilota", "Piloto", "Piloto", "Pilote", "Pilot"),
    ("professions", "Asker", "Soldier", "Souldcır", "Soldat", "Zoldat", "Soldato", "Soldato", "Soldado", "Soldado", "Soldat", "Solda"),
    ("professions", "Diş hekimi", "Dentist", "Dentist", "Zahnarzt", "Tsanartst", "Dentista", "Dentista", "Dentista", "Dentista", "Dentiste", "Dantist"),
    ("professions", "Eczacı", "Pharmacist", "Farmısist", "Apotheker", "Apotekır", "Farmacista", "Farmaçista", "Farmacéutico", "Farmaseutiko", "Pharmacien", "Farmasiyen"),
    ("professions", "Mimar", "Architect", "Arkitekt", "Architekt", "Arhitekt", "Architetto", "Arkitetto", "Arquitecto", "Arkitekto", "Architecte", "Arşitekt"),
    ("professions", "Bilim insanı", "Scientist", "Sayıntist", "Wissenschaftler", "Visınşaftlır", "Scienziato", "Şentsiyato", "Científico", "Siyentifiko", "Scientifique", "Siyantifik"),
    ("professions", "Gazeteci", "Journalist", "Cörnılist", "Journalist", "Jurnalist", "Giornalista", "Cornalista", "Periodista", "Periyodista", "Journaliste", "Jurnalist"),
    ("professions", "Fotoğrafçı", "Photographer", "Fotogırfır", "Fotograf", "Fotograf", "Fotografo", "Fotografo", "Fotógrafo", "Fotografo", "Photographe", "Fotograf"),
    ("professions", "Berber", "Barber", "Barbır", "Friseur", "Frizör", "Barbiere", "Barbiyere", "Barbero", "Barbero", "Coiffeur", "Kuaför"),
    ("professions", "Terzi", "Tailor", "Teylır", "Schneider", "Şnaydır", "Sarto", "Sarto", "Sastre", "Sastre", "Couturier", "Kutüriye"),
    ("professions", "Tamirci", "Mechanic", "Mekanik", "Mechaniker", "Mehanikır", "Meccanico", "Mekkaniko", "Mecánico", "Mekaniko", "Mécanicien", "Mekanisiyen"),
    ("professions", "Elektrikçi", "Electrician", "İlektriişın", "Elektriker", "Elektrikır", "Elettricista", "Elettriçista", "Electricista", "Elektrisista", "Électricien", "Elektrisiyen"),

    # ── home (yeni, 25) ───────────────────────────────────────────────
    ("home", "Ev", "House", "Haus", "Haus", "Haus", "Casa", "Kaza", "Casa", "Kasa", "Maison", "Mezon"),
    ("home", "Oda", "Room", "Ruum", "Zimmer", "Tsimmır", "Stanza", "Stantsa", "Habitación", "Abitasyon", "Chambre", "Şanbr"),
    ("home", "Mutfak", "Kitchen", "Kiçın", "Küche", "Kühe", "Cucina", "Kuçina", "Cocina", "Kosina", "Cuisine", "Küizin"),
    ("home", "Banyo", "Bathroom", "Batruum", "Badezimmer", "Badıtsimmır", "Bagno", "Banyo", "Baño", "Banyo", "Salle de bain", "Sal dö ben"),
    ("home", "Yatak odası", "Bedroom", "Bedruum", "Schlafzimmer", "Şlaftsimmır", "Camera da letto", "Kamera da letto", "Dormitorio", "Dormitoryo", "Chambre à coucher", "Şanbr a kuşe"),
    ("home", "Oturma odası", "Living room", "Living ruum", "Wohnzimmer", "Vontsimmır", "Soggiorno", "Soccorno", "Sala de estar", "Sala de estar", "Salon", "Salon"),
    ("home", "Kapı", "Door", "Dor", "Tür", "Tür", "Porta", "Porta", "Puerta", "Puyerta", "Porte", "Port"),
    ("home", "Pencere", "Window", "Vindou", "Fenster", "Fenstır", "Finestra", "Finestra", "Ventana", "Bentana", "Fenêtre", "Fönetr"),
    ("home", "Duvar", "Wall", "Vol", "Wand", "Vant", "Muro", "Muro", "Pared", "Pared", "Mur", "Mür"),
    ("home", "Zemin", "Floor", "Flor", "Boden", "Bodın", "Pavimento", "Pavimento", "Suelo", "Suyelo", "Sol", "Sol"),
    ("home", "Tavan", "Ceiling", "Siiling", "Decke", "Dekı", "Soffitto", "Soffitto", "Techo", "Teço", "Plafond", "Plafon"),
    ("home", "Merdiven", "Stairs", "Sterz", "Treppe", "Treppı", "Scale", "Skale", "Escaleras", "Eskaleras", "Escalier", "Eskaliye"),
    ("home", "Bahçe", "Garden", "Gardın", "Garten", "Gartın", "Giardino", "Cardino", "Jardín", "Hardin", "Jardin", "Jarden"),
    ("home", "Anahtar", "Key", "Kii", "Schlüssel", "Şlüsıl", "Chiave", "Kiyave", "Llave", "Yave", "Clé", "Kle"),
    ("home", "Lamba", "Lamp", "Lemp", "Lampe", "Lampı", "Lampada", "Lampada", "Lámpara", "Lampara", "Lampe", "Lanp"),
    ("home", "Ayna", "Mirror", "Mirır", "Spiegel", "Şpigıl", "Specchio", "Spekkiyo", "Espejo", "Espeho", "Miroir", "Miruar"),
    ("home", "Saat", "Clock", "Klok", "Uhr", "Ur", "Orologio", "Oroloco", "Reloj", "Reloh", "Horloge", "Orloj"),
    ("home", "Televizyon", "Television", "Telivijın", "Fernseher", "Fernzeır", "Televisione", "Televizyone", "Televisión", "Telebisiyon", "Télévision", "Televizyon"),
    ("home", "Buzdolabı", "Refrigerator", "Rifriceıreytır", "Kühlschrank", "Külşrank", "Frigorifero", "Frigorifero", "Refrigerador", "Refriherador", "Réfrigérateur", "Refrijeratör"),
    ("home", "Fırın", "Oven", "Avın", "Ofen", "Ofın", "Forno", "Forno", "Horno", "Orno", "Four", "Fur"),
    ("home", "Çamaşır makinesi", "Washing machine", "Voşing mışiin", "Waschmaschine", "Vaşmaşinı", "Lavatrice", "Lavatriçe", "Lavadora", "Labadora", "Machine à laver", "Maşin a lave"),
    ("home", "Kanepe", "Sofa", "Soufa", "Sofa", "Zofa", "Divano", "Divano", "Sofá", "Sofa", "Canapé", "Kanape"),
    ("home", "Halı", "Carpet", "Karpıt", "Teppich", "Teppih", "Tappeto", "Tappeto", "Alfombra", "Alfombra", "Tapis", "Tapi"),
    ("home", "Perde", "Curtain", "Körtın", "Vorhang", "Forhang", "Tenda", "Tenda", "Cortina", "Kortina", "Rideau", "Rido"),
    ("home", "Yastık", "Pillow", "Pilou", "Kissen", "Kissın", "Cuscino", "Kuşino", "Almohada", "Almoada", "Oreiller", "Oreye"),

    # ── body (yeni, 20) ───────────────────────────────────────────────
    ("body", "Baş", "Head", "Hed", "Kopf", "Kopf", "Testa", "Testa", "Cabeza", "Kabesa", "Tête", "Tet"),
    ("body", "Yüz", "Face", "Feys", "Gesicht", "Gezıht", "Viso", "Vizo", "Cara", "Kara", "Visage", "Vizaj"),
    ("body", "Göz", "Eye", "Ay", "Auge", "Augı", "Occhio", "Okkiyo", "Ojo", "Oho", "Œil", "Öy"),
    ("body", "Kulak", "Ear", "İır", "Ohr", "Or", "Orecchio", "Orekkiyo", "Oreja", "Oreha", "Oreille", "Orey"),
    ("body", "Burun", "Nose", "Nouz", "Nase", "Nazı", "Naso", "Nazo", "Nariz", "Naris", "Nez", "Ne"),
    ("body", "Ağız", "Mouth", "Maut", "Mund", "Munt", "Bocca", "Bokka", "Boca", "Boka", "Bouche", "Buş"),
    ("body", "Diş", "Tooth", "Tuut", "Zahn", "Tsan", "Dente", "Dente", "Diente", "Diyente", "Dent", "Dan"),
    ("body", "Dil", "Tongue", "Tang", "Zunge", "Tsungı", "Lingua", "Lingua", "Lengua", "Lengua", "Langue", "Lang"),
    ("body", "Boyun", "Neck", "Nek", "Hals", "Hals", "Collo", "Kollo", "Cuello", "Kuweyo", "Cou", "Ku"),
    ("body", "Omuz", "Shoulder", "Şouldır", "Schulter", "Şultır", "Spalla", "Spalla", "Hombro", "Ombro", "Épaule", "Epol"),
    ("body", "Kol", "Arm", "Arm", "Arm", "Arm", "Braccio", "Braçço", "Brazo", "Braso", "Manche", "Manş"),
    ("body", "El", "Hand", "Hend", "Hand", "Hant", "Mano", "Mano", "Mano", "Mano", "Main", "Men"),
    ("body", "Parmak", "Finger", "Fingır", "Finger", "Fingır", "Dito", "Dito", "Dedo", "Dedo", "Doigt", "Dua"),
    ("body", "Bacak", "Leg", "Leg", "Bein", "Bayn", "Gamba", "Gamba", "Pierna", "Piyerna", "Jambe", "Janb"),
    ("body", "Diz", "Knee", "Nii", "Knie", "Kni", "Ginocchio", "Cinokkiyo", "Rodilla", "Rodiya", "Genou", "Jönu"),
    ("body", "Ayak", "Foot", "Fut", "Fuß", "Fus", "Piede", "Piyede", "Pie", "Piye", "Pied", "Piye"),
    ("body", "Sırt", "Back", "Bek", "Rücken", "Rükın", "Schiena", "Skiyena", "Espalda", "Espalda", "Dos", "Do"),
    ("body", "Göğüs", "Chest", "Çest", "Brust", "Brust", "Petto", "Petto", "Pecho", "Peço", "Poitrine", "Puatrin"),
    ("body", "Karın", "Stomach", "Stamık", "Bauch", "Bauh", "Stomaco", "Stomako", "Estómago", "Estomago", "Ventre", "Vantr"),
    ("body", "Kalp", "Heart", "Hart", "Herz", "Herts", "Cuore", "Kuore", "Corazón", "Korason", "Cœur", "Kör"),

    # ── animals (yeni, 15) ────────────────────────────────────────────
    ("animals", "Kedi", "Cat", "Ket", "Katze", "Katsı", "Gatto", "Gatto", "Gato", "Gato", "Chat", "Şa"),
    ("animals", "Köpek", "Dog", "Dog", "Hund", "Hunt", "Cane", "Kane", "Perro", "Perro", "Chien", "Şiyen"),
    ("animals", "Kuş", "Bird", "Börd", "Vogel", "Fogıl", "Uccello", "Uççello", "Pájaro", "Paharo", "Oiseau", "Uazo"),
    ("animals", "Balık", "Fish", "Fiş", "Fisch", "Fiş", "Pesce", "Peşe", "Pez", "Pes", "Poisson", "Puason"),
    ("animals", "At", "Horse", "Hors", "Pferd", "Pfert", "Cavallo", "Kavallo", "Caballo", "Kabayo", "Cheval", "Şöval"),
    ("animals", "İnek", "Cow", "Kau", "Kuh", "Ku", "Mucca", "Mukka", "Vaca", "Baka", "Vache", "Vaş"),
    ("animals", "Koyun", "Sheep", "Şiip", "Schaf", "Şaf", "Pecora", "Pekora", "Oveja", "Oveha", "Mouton", "Muton"),
    ("animals", "Tavuk", "Chicken", "Çikın", "Huhn", "Hun", "Pollo", "Pollo", "Pollo", "Poyo", "Poulet", "Pule"),
    ("animals", "Tavşan", "Rabbit", "Rebıt", "Kaninchen", "Kaninhın", "Coniglio", "Konilyo", "Conejo", "Koneho", "Lapin", "Lapen"),
    ("animals", "Ayı", "Bear", "Ber", "Bär", "Ber", "Orso", "Orso", "Oso", "Oso", "Ours", "Urs"),
    ("animals", "Aslan", "Lion", "Layın", "Löwe", "Lövı", "Leone", "Leone", "León", "Leon", "Lion", "Liyon"),
    ("animals", "Fil", "Elephant", "Elıfınt", "Elefant", "Elefant", "Elefante", "Elefante", "Elefante", "Elefante", "Éléphant", "Elefan"),
    ("animals", "Maymun", "Monkey", "Manki", "Affe", "Affı", "Scimmia", "Şimmiya", "Mono", "Mono", "Singe", "Senj"),
    ("animals", "Yılan", "Snake", "Sneyk", "Schlange", "Şlangı", "Serpente", "Serpente", "Serpiente", "Serpiyente", "Serpent", "Serpan"),
    ("animals", "Kelebek", "Butterfly", "Batırflay", "Schmetterling", "Şmetırling", "Farfalla", "Farfalla", "Mariposa", "Mariposa", "Papillon", "Papiyõ"),
] + EXTRA_WORDS

CATEGORIES = {
    "greetings": "Selamlaşma",
    "numbers": "Sayılar",
    "time": "Zaman",
    "family": "Aile",
    "food": "Yiyecek",
    "shopping": "Alışveriş",
    "travel": "Seyahat",
    "health": "Sağlık",
    "adjectives": "Sıfatlar",
    "verbs": "Fiiller",
    "daily": "Günlük",
    "places": "Mekanlar",
    "weather": "Hava Durumu",
    "clothing": "Giyim",
    "education": "Eğitim",
    "emotions": "Duygular",
    "nature": "Doğa",
    "professions": "Meslekler",
    "home": "Ev & Eşyalar",
    "body": "Vücut",
    "animals": "Hayvanlar",
    "technology": "Teknoloji",
    "sports": "Spor",
    "music": "Müzik",
    "kitchen": "Mutfak",
    "office": "Ofis & İş",
    "colors": "Renkler",
    "materials": "Malzemeler",
    "transport": "Ulaşım Araçları",
}

# Cumle kategorileri
SENTENCE_CATEGORIES = {
    "daily_conv": "Günlük Konuşma",
    "restaurant": "Restoran",
    "shopping": "Alışveriş",
    "hotel": "Otel",
    "transport": "Ulaşım",
    "health": "Sağlık",
    "directions": "Yön Tarifi",
    "emergency": "Acil Durumlar",
    "phone": "Telefon",
    "feelings": "Duygular",
    "travel": "Seyahat",
    "social": "Sosyal",
    "work": "İş",
    "education": "Eğitim/Okul",
    "home_daily": "Ev & Günlük",
    "airport_detail": "Havaalanı",
    "bank_detail": "Banka",
    "car_traffic": "Araba/Trafik",
    "culture_fun": "Kültür/Eğlence",
    "romantic_social": "Romantik/Sosyal",
    "children": "Çocuklar",
    "weather_detail": "Hava Durumu",
    "sports_fitness": "Spor/Fitness",
    "digital_tech": "Dijital/Teknoloji",
    "appointment_time": "Randevu/Zaman",
    "complaint": "Şikayet/Sorun",
    "proverbs": "Atasözleri/Deyimler",
}

SENTENCE_ICONS = {
    "daily_conv": "💬",
    "restaurant": "🍽️",
    "shopping": "🛒",
    "hotel": "🏨",
    "transport": "🚌",
    "health": "🏥",
    "directions": "🗺️",
    "emergency": "🚨",
    "phone": "📱",
    "feelings": "😊",
    "travel": "✈️",
    "social": "🤝",
    "work": "💼",
    "education": "🎓",
    "home_daily": "🏠",
    "airport_detail": "🛫",
    "bank_detail": "🏦",
    "car_traffic": "🚗",
    "culture_fun": "🎭",
    "romantic_social": "❤️",
    "children": "👶",
    "weather_detail": "🌦️",
    "sports_fitness": "🏋️",
    "digital_tech": "📲",
    "appointment_time": "📅",
    "complaint": "📢",
    "proverbs": "📜",
}

CATEGORY_ICONS = {
    "greetings": "👋",
    "numbers": "🔢",
    "time": "⏰",
    "family": "👨‍👩‍👧‍👦",
    "food": "🍽️",
    "shopping": "🛒",
    "travel": "✈️",
    "health": "🏥",
    "adjectives": "📝",
    "verbs": "🏃",
    "daily": "💬",
    "places": "📍",
    "weather": "🌤️",
    "clothing": "👔",
    "education": "📚",
    "emotions": "😊",
    "nature": "🌿",
    "professions": "👨‍💼",
    "home": "🏠",
    "body": "🫀",
    "animals": "🐾",
    "technology": "💻",
    "sports": "⚽",
    "music": "🎵",
    "kitchen": "🍳",
    "office": "🏢",
    "colors": "🎨",
    "materials": "🧱",
    "transport": "🚆",
}


def _build_data_json() -> str:
    """Convert WORDS list to JSON for the HTML component."""
    items = []
    for w in WORDS:
        items.append({
            "cat": w[0],
            "tr": w[1],
            "en": w[2], "en_ph": w[3],
            "de": w[4], "de_ph": w[5],
            "it": w[6], "it_ph": w[7],
            "es": w[8], "es_ph": w[9],
            "fr": w[10], "fr_ph": w[11],
        })
    return json.dumps(items, ensure_ascii=False)


def _build_sentences_json() -> str:
    """Convert SENTENCES + EXTRA_SENTENCES to JSON for the HTML component."""
    all_sentences = SENTENCES + EXTRA_SENTENCES
    items = []
    for s in all_sentences:
        items.append({
            "cat": s[0],
            "tr": s[1],
            "en": s[2], "en_ph": s[3],
            "de": s[4], "de_ph": s[5],
            "it": s[6], "it_ph": s[7],
            "es": s[8], "es_ph": s[9],
            "fr": s[10], "fr_ph": s[11],
        })
    return json.dumps(items, ensure_ascii=False)


def _build_categories_json() -> str:
    cats = []
    for cid, label in CATEGORIES.items():
        cats.append({"id": cid, "label": label, "icon": CATEGORY_ICONS.get(cid, "")})
    return json.dumps(cats, ensure_ascii=False)


def _build_sentence_categories_json() -> str:
    cats = []
    for cid, label in SENTENCE_CATEGORIES.items():
        cats.append({"id": cid, "label": label, "icon": SENTENCE_ICONS.get(cid, "")})
    return json.dumps(cats, ensure_ascii=False)


def _build_html() -> str:
    data_json = _build_data_json()
    cats_json = _build_categories_json()
    sentences_json = _build_sentences_json()
    sent_cats_json = _build_sentence_categories_json()

    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --navy:#0B0F19;--navy2:#232B3E;--navy3:#131825;
  --gold:#6366F1;--gold2:#6366F1;--gold3:#A5B4FC;
  --card-bg:rgba(255,255,255,0.05);--card-border:rgba(212,175,55,0.3);
  --text:#E2E8F0;--text2:#CBD5E1;
}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  color:var(--text);min-height:100vh;padding:0;
}}
/* ─── HEADER ─── */
.header{{
  text-align:center;padding:28px 20px 18px;position:relative;overflow:hidden;
}}
.header::before{{
  content:'';position:absolute;top:0;left:-100%;width:200%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(212,175,55,0.08),transparent);
  animation:shimmer 3s infinite;
}}
@keyframes shimmer{{0%{{left:-100%}}100%{{left:100%}}}}
.header h1{{
  font-size:1.7em;letter-spacing:2px;
  background:linear-gradient(135deg,var(--gold),var(--gold2),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}}
.header .subtitle{{color:var(--text2);font-size:0.85em;margin-top:4px;letter-spacing:1px;}}
/* ─── LANG TABS ─── */
.lang-tabs{{
  display:flex;justify-content:center;gap:8px;padding:10px 16px;flex-wrap:wrap;
}}
.lang-tab{{
  padding:10px 22px;border-radius:25px;cursor:pointer;font-size:0.92em;font-weight:600;
  border:1.5px solid var(--card-border);background:var(--card-bg);color:var(--text);
  transition:all .3s;letter-spacing:0.5px;user-select:none;
}}
.lang-tab:hover{{border-color:var(--gold);background:rgba(212,175,55,0.1);}}
.lang-tab.active{{
  background:linear-gradient(135deg,var(--gold3),var(--gold));color:var(--navy);
  border-color:var(--gold);box-shadow:0 0 18px rgba(212,175,55,0.3);
}}
/* ─── CONTROLS ─── */
.controls{{padding:12px 20px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;}}
.search-box{{
  flex:1;min-width:200px;padding:10px 16px;border-radius:20px;
  background:rgba(255,255,255,0.06);border:1px solid var(--card-border);
  color:var(--text);font-size:0.9em;outline:none;transition:border .3s;
}}
.search-box:focus{{border-color:var(--gold);}}
.search-box::placeholder{{color:var(--text2);}}
.mode-btn{{
  padding:9px 20px;border-radius:20px;cursor:pointer;font-size:0.85em;font-weight:600;
  border:1.5px solid var(--gold);color:var(--gold);background:transparent;
  transition:all .3s;letter-spacing:0.5px;
}}
.mode-btn:hover,.mode-btn.active{{background:var(--gold);color:var(--navy);}}
/* ─── CATEGORY CHIPS ─── */
.chips{{
  display:flex;gap:7px;padding:6px 20px 14px;flex-wrap:wrap;justify-content:center;
}}
.chip{{
  padding:6px 14px;border-radius:16px;font-size:0.78em;cursor:pointer;
  border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.04);
  color:var(--text2);transition:all .25s;user-select:none;white-space:nowrap;
}}
.chip:hover{{border-color:var(--gold);color:var(--text);}}
.chip.active{{background:rgba(212,175,55,0.15);border-color:var(--gold);color:var(--gold);}}
/* ─── PROGRESS ─── */
.progress-bar-wrap{{
  margin:0 20px 10px;padding:8px 16px;border-radius:12px;
  background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
  display:flex;align-items:center;gap:12px;
}}
.progress-bar-wrap .label{{font-size:0.78em;color:var(--text2);white-space:nowrap;}}
.progress-track{{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,0.1);overflow:hidden;}}
.progress-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--gold3),var(--gold2));transition:width .5s;}}
.progress-bar-wrap .pct{{font-size:0.78em;color:var(--gold);font-weight:600;min-width:35px;text-align:right;}}
/* ─── WORD GRID ─── */
.grid{{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
  gap:14px;padding:10px 20px 30px;
}}
.card{{
  background:var(--card-bg);border:1px solid var(--card-border);border-radius:14px;
  padding:18px;transition:all .35s;position:relative;overflow:hidden;
  backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);
}}
.card::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:0;transition:opacity .3s;
}}
.card:hover{{transform:translateY(-3px);box-shadow:0 8px 25px rgba(0,0,0,0.3);border-color:var(--gold);}}
.card:hover::before{{opacity:1;}}
.card .word{{font-size:1.15em;font-weight:700;color:var(--gold2);margin-bottom:2px;}}
.card .phonetic{{font-size:0.82em;color:var(--text2);font-style:italic;margin-bottom:8px;}}
.card .turkish{{
  font-size:0.88em;color:var(--text);padding:6px 10px;border-radius:8px;
  background:rgba(212,175,55,0.08);border-left:3px solid var(--gold3);margin-bottom:10px;
}}
.card .cat-badge{{
  position:absolute;top:10px;right:10px;font-size:0.68em;padding:3px 8px;
  border-radius:10px;background:rgba(255,255,255,0.06);color:var(--text2);
}}
.play-btn{{
  display:inline-flex;align-items:center;gap:5px;padding:6px 14px;border-radius:16px;
  border:1px solid var(--gold);background:transparent;color:var(--gold);
  cursor:pointer;font-size:0.78em;transition:all .25s;
}}
.play-btn:hover{{background:var(--gold);color:var(--navy);}}
.play-btn svg{{width:14px;height:14px;fill:currentColor;}}
/* ─── FLASHCARD MODE ─── */
.flashcard-container{{padding:20px;display:none;}}
.flashcard{{
  max-width:440px;margin:0 auto;min-height:260px;perspective:1000px;cursor:pointer;
}}
.flashcard-inner{{
  position:relative;width:100%;min-height:260px;transition:transform .6s;
  transform-style:preserve-3d;
}}
.flashcard.flipped .flashcard-inner{{transform:rotateY(180deg);}}
.flashcard-face{{
  position:absolute;width:100%;min-height:260px;backface-visibility:hidden;
  border-radius:18px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:30px;text-align:center;
}}
.flashcard-front{{
  background:linear-gradient(135deg,rgba(26,26,78,0.9),rgba(10,10,46,0.95));
  border:2px solid var(--gold);
}}
.flashcard-back{{
  background:linear-gradient(135deg,rgba(212,175,55,0.15),rgba(26,26,78,0.95));
  border:2px solid var(--gold2);transform:rotateY(180deg);
}}
.flashcard-front .fc-label{{font-size:0.75em;color:var(--text2);margin-bottom:10px;letter-spacing:2px;text-transform:uppercase;}}
.flashcard-front .fc-word{{font-size:1.8em;font-weight:700;color:var(--gold2);margin-bottom:8px;}}
.flashcard-front .fc-hint{{font-size:0.82em;color:var(--text2);}}
.flashcard-back .fc-answer{{font-size:1.5em;font-weight:700;color:var(--gold);margin-bottom:4px;}}
.flashcard-back .fc-phonetic{{font-size:0.9em;color:var(--text2);font-style:italic;margin-bottom:10px;}}
.flashcard-back .fc-turkish{{font-size:0.85em;color:var(--text);}}
.fc-actions{{display:flex;gap:12px;justify-content:center;margin-top:18px;}}
.fc-btn{{
  padding:10px 24px;border-radius:20px;cursor:pointer;font-size:0.88em;font-weight:600;
  border:none;transition:all .25s;
}}
.fc-btn.learned{{background:#2ecc71;color:#fff;}}
.fc-btn.learned:hover{{background:#27ae60;}}
.fc-btn.repeat{{background:#e74c3c;color:#fff;}}
.fc-btn.repeat:hover{{background:#c0392b;}}
.fc-btn.skip{{background:rgba(255,255,255,0.1);color:var(--text);border:1px solid rgba(255,255,255,0.2);}}
.fc-btn.skip:hover{{background:rgba(255,255,255,0.15);}}
.fc-counter{{text-align:center;margin-bottom:14px;font-size:0.82em;color:var(--text2);}}
.fc-play-btn{{
  margin-top:10px;padding:8px 18px;border-radius:16px;
  border:1px solid var(--gold);background:transparent;color:var(--gold);
  cursor:pointer;font-size:0.82em;transition:all .25s;
}}
.fc-play-btn:hover{{background:var(--gold);color:var(--navy);}}
/* ─── QUIZ / EXERCISES ─── */
.quiz-container{{padding:16px 20px;display:none;}}
.quiz-type-grid{{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
  gap:12px;margin-bottom:20px;
}}
.quiz-type-card{{
  background:var(--card-bg);border:1.5px solid var(--card-border);border-radius:14px;
  padding:20px 16px;text-align:center;cursor:pointer;transition:all .3s;position:relative;overflow:hidden;
}}
.quiz-type-card:hover{{transform:translateY(-3px);border-color:var(--gold);box-shadow:0 6px 20px rgba(0,0,0,0.3);}}
.quiz-type-card.active{{border-color:var(--gold);background:rgba(99,102,241,0.12);}}
.quiz-type-card .qt-icon{{font-size:2.2em;margin-bottom:8px;}}
.quiz-type-card .qt-title{{font-weight:700;font-size:0.95em;color:var(--gold2);margin-bottom:4px;}}
.quiz-type-card .qt-desc{{font-size:0.75em;color:var(--text2);line-height:1.4;}}

.quiz-area{{max-width:640px;margin:0 auto;}}
.quiz-header{{
  background:linear-gradient(135deg,rgba(20,20,60,0.95),rgba(10,10,46,0.98));
  border:1px solid var(--card-border);border-radius:14px;padding:18px 22px;margin-bottom:16px;
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;
}}
.quiz-header .qh-title{{font-weight:800;font-size:1.05em;color:var(--gold2);}}
.quiz-header .qh-score{{font-size:0.88em;color:var(--text2);}}
.quiz-header .qh-score b{{color:#2ecc71;}}
.quiz-progress{{height:6px;border-radius:3px;background:rgba(255,255,255,0.1);margin-bottom:18px;overflow:hidden;}}
.quiz-progress-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--gold3),var(--gold2));transition:width .4s;}}

.quiz-question{{
  background:var(--card-bg);border:1px solid var(--card-border);border-radius:14px;
  padding:24px;margin-bottom:14px;text-align:center;
}}
.quiz-question .qq-label{{font-size:0.75em;color:var(--text2);text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;}}
.quiz-question .qq-word{{font-size:1.6em;font-weight:800;color:var(--gold2);margin-bottom:6px;}}
.quiz-question .qq-hint{{font-size:0.82em;color:var(--text2);font-style:italic;}}

.quiz-options{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}}
.quiz-opt{{
  padding:14px 18px;border-radius:12px;cursor:pointer;font-size:0.92em;font-weight:600;
  border:1.5px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.04);
  color:var(--text);transition:all .25s;text-align:center;
}}
.quiz-opt:hover{{border-color:var(--gold);background:rgba(99,102,241,0.08);}}
.quiz-opt.correct{{background:rgba(46,204,113,0.2);border-color:#2ecc71;color:#2ecc71;}}
.quiz-opt.wrong{{background:rgba(231,76,60,0.2);border-color:#e74c3c;color:#e74c3c;}}
.quiz-opt.disabled{{pointer-events:none;opacity:0.6;}}
.quiz-opt.highlight{{border-color:#2ecc71;background:rgba(46,204,113,0.15);color:#2ecc71;}}

.quiz-input-wrap{{margin-bottom:16px;text-align:center;}}
.quiz-input{{
  width:100%;max-width:400px;padding:14px 18px;border-radius:12px;font-size:1em;font-weight:600;
  border:1.5px solid var(--card-border);background:rgba(255,255,255,0.06);color:var(--text);
  outline:none;text-align:center;transition:border .3s;
}}
.quiz-input:focus{{border-color:var(--gold);}}
.quiz-input.correct{{border-color:#2ecc71;background:rgba(46,204,113,0.1);}}
.quiz-input.wrong{{border-color:#e74c3c;background:rgba(231,76,60,0.1);}}
.quiz-check-btn{{
  margin-top:10px;padding:12px 32px;border-radius:20px;cursor:pointer;font-size:0.92em;font-weight:700;
  border:none;background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--navy);transition:all .3s;
}}
.quiz-check-btn:hover{{box-shadow:0 4px 16px rgba(99,102,241,0.4);transform:scale(1.02);}}

.quiz-match-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;}}
.quiz-match-item{{
  padding:12px 14px;border-radius:10px;cursor:pointer;font-size:0.88em;font-weight:600;
  border:1.5px solid rgba(255,255,255,0.15);background:rgba(255,255,255,0.04);
  color:var(--text);transition:all .25s;text-align:center;
}}
.quiz-match-item:hover{{border-color:var(--gold);}}
.quiz-match-item.selected{{border-color:var(--gold);background:rgba(99,102,241,0.15);color:var(--gold);}}
.quiz-match-item.matched{{background:rgba(46,204,113,0.15);border-color:#2ecc71;color:#2ecc71;pointer-events:none;}}
.quiz-match-item.error{{background:rgba(231,76,60,0.15);border-color:#e74c3c;}}

.quiz-result{{
  background:linear-gradient(135deg,rgba(20,20,60,0.95),rgba(10,10,46,0.98));
  border:2px solid var(--gold);border-radius:18px;padding:30px;text-align:center;
}}
.quiz-result .qr-icon{{font-size:3.5em;margin-bottom:10px;}}
.quiz-result .qr-score{{font-size:2em;font-weight:800;color:var(--gold2);margin-bottom:4px;}}
.quiz-result .qr-label{{font-size:0.9em;color:var(--text2);margin-bottom:16px;}}
.quiz-result .qr-bar{{height:10px;border-radius:5px;background:rgba(255,255,255,0.1);overflow:hidden;margin:10px auto;max-width:300px;}}
.quiz-result .qr-bar-fill{{height:100%;border-radius:5px;transition:width .6s;}}
.quiz-next-btn{{
  margin-top:14px;padding:12px 36px;border-radius:20px;cursor:pointer;font-size:0.95em;font-weight:700;
  border:none;background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--navy);transition:all .3s;
}}
.quiz-next-btn:hover{{box-shadow:0 4px 16px rgba(99,102,241,0.4);}}

.quiz-tf-btns{{display:flex;gap:14px;justify-content:center;margin-bottom:16px;}}
.quiz-tf-btn{{
  padding:14px 36px;border-radius:14px;cursor:pointer;font-size:1em;font-weight:700;
  border:2px solid rgba(255,255,255,0.2);background:rgba(255,255,255,0.04);
  color:var(--text);transition:all .25s;min-width:130px;
}}
.quiz-tf-btn:hover{{border-color:var(--gold);}}
.quiz-tf-btn.correct{{background:rgba(46,204,113,0.2);border-color:#2ecc71;color:#2ecc71;}}
.quiz-tf-btn.wrong{{background:rgba(231,76,60,0.2);border-color:#e74c3c;color:#e74c3c;}}

.quiz-listen-btn{{
  display:inline-flex;align-items:center;gap:8px;padding:16px 32px;border-radius:50%;
  border:2px solid var(--gold);background:rgba(99,102,241,0.1);color:var(--gold);
  cursor:pointer;font-size:1.8em;transition:all .3s;margin-bottom:14px;
}}
.quiz-listen-btn:hover{{background:var(--gold);color:var(--navy);transform:scale(1.1);}}

/* ─── EMPTY STATE ─── */
.empty{{text-align:center;padding:60px 20px;color:var(--text2);}}
.empty .icon{{font-size:3em;margin-bottom:10px;}}
/* ─── STATS ROW ─── */
.stats-row{{
  display:flex;gap:10px;padding:0 20px 10px;flex-wrap:wrap;justify-content:center;
}}
.stat-card{{
  padding:8px 16px;border-radius:12px;background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);text-align:center;min-width:90px;
}}
.stat-card .sv{{font-size:1.2em;font-weight:700;color:var(--gold);}}
.stat-card .sl{{font-size:0.7em;color:var(--text2);margin-top:2px;}}
</style>
</head>
<body>

<div class="header">
  <h1>&#9830; Pratik Dil &Ouml;ğrenme</h1>
  <div class="subtitle">5 Dil &bull; 770 Kelime &amp; 600 C&uuml;mle &bull; Sesli Telaffuz</div>
</div>

<!-- Lang Tabs -->
<div class="lang-tabs" id="langTabs">
  <div class="lang-tab active" data-lang="en" onclick="setLang('en')">&#127468;&#127463; English</div>
  <div class="lang-tab" data-lang="de" onclick="setLang('de')">&#127465;&#127466; Almanca</div>
  <div class="lang-tab" data-lang="it" onclick="setLang('it')">&#127470;&#127481; İtalyanca</div>
  <div class="lang-tab" data-lang="es" onclick="setLang('es')">&#127466;&#127480; İspanyolca</div>
  <div class="lang-tab" data-lang="fr" onclick="setLang('fr')">&#127467;&#127479; Fransızca</div>
</div>

<!-- Main Mode Tabs: Kelimeler / Cumleler -->
<div id="mainTabs" style="display:flex;justify-content:center;gap:0;margin:14px 20px 10px;border-radius:14px;overflow:hidden;border:2px solid var(--gold);">
  <div class="main-tab active" data-mode="words" onclick="setMainMode('words')"
    style="flex:1;text-align:center;padding:14px 20px;cursor:pointer;font-weight:800;font-size:1.05em;
    letter-spacing:1px;transition:all .3s;background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--navy);">
    &#128218; KEL&#304;MELER (770)
  </div>
  <div class="main-tab" data-mode="sentences" onclick="setMainMode('sentences')"
    style="flex:1;text-align:center;padding:14px 20px;cursor:pointer;font-weight:800;font-size:1.05em;
    letter-spacing:1px;transition:all .3s;background:transparent;color:var(--gold);">
    &#128172; C&Uuml;MLELER (600)
  </div>
  <div class="main-tab" data-mode="quiz" onclick="setMainMode('quiz')"
    style="flex:1;text-align:center;padding:14px 20px;cursor:pointer;font-weight:800;font-size:1.05em;
    letter-spacing:1px;transition:all .3s;background:transparent;color:var(--gold);">
    &#127919; ALI&Scedil;TIRMALAR
  </div>
</div>

<!-- Stats -->
<div class="stats-row" id="statsRow"></div>

<!-- Progress -->
<div class="progress-bar-wrap" id="progressWrap">
  <span class="label">&#128218; İlerleme</span>
  <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  <span class="pct" id="progressPct">0%</span>
</div>

<!-- Controls -->
<div class="controls">
  <input class="search-box" id="searchBox" type="text" placeholder="&#128269; Kelime veya çeviri ara...">
  <button class="mode-btn" id="modeBtn" onclick="toggleMode()">&#127183; Flashcard Modu</button>
</div>

<!-- Category Chips -->
<div class="chips" id="chipsContainer"></div>

<!-- Grid View -->
<div class="grid" id="wordGrid"></div>

<!-- Flashcard View -->
<div class="flashcard-container" id="flashcardView">
  <div class="fc-counter" id="fcCounter"></div>
  <div class="flashcard" id="flashcard" onclick="flipCard()">
    <div class="flashcard-inner">
      <div class="flashcard-face flashcard-front">
        <div class="fc-label">TÜRKÇE</div>
        <div class="fc-word" id="fcWord"></div>
        <div class="fc-hint" id="fcHint">Kartı çevirmek için tıklayın</div>
      </div>
      <div class="flashcard-face flashcard-back">
        <div class="fc-answer" id="fcAnswer"></div>
        <div class="fc-phonetic" id="fcPhonetic"></div>
        <div class="fc-turkish" id="fcTurkish"></div>
        <button class="fc-play-btn" id="fcPlayBtn" onclick="event.stopPropagation();playFlashcardAudio()">&#9654; Dinle</button>
      </div>
    </div>
  </div>
  <div class="fc-actions">
    <button class="fc-btn repeat" onclick="markCard('repeat')">&#128260; Tekrar</button>
    <button class="fc-btn skip" onclick="markCard('skip')">&#9654; Atla</button>
    <button class="fc-btn learned" onclick="markCard('learned')">&#9989; Öğrendim</button>
  </div>
</div>

<!-- Quiz View -->
<div class="quiz-container" id="quizView">
  <!-- Quiz type selection -->
  <div id="quizTypeSelect">
    <div class="quiz-type-grid">
      <div class="quiz-type-card" onclick="startQuiz('mc')">
        <div class="qt-icon">&#127919;</div>
        <div class="qt-title">&Ccedil;oktan Se&ccedil;meli</div>
        <div class="qt-desc">T&uuml;rk&ccedil;e kelimeyi g&ouml;r, do&gbreve;ru &ccedil;eviriyi se&ccedil;</div>
      </div>
      <div class="quiz-type-card" onclick="startQuiz('write')">
        <div class="qt-icon">&#9997;&#65039;</div>
        <div class="qt-title">Yazarak Cevapla</div>
        <div class="qt-desc">T&uuml;rk&ccedil;e kelimeyi g&ouml;r, &ccedil;eviriyi yaz</div>
      </div>
      <div class="quiz-type-card" onclick="startQuiz('tf')">
        <div class="qt-icon">&#9989;</div>
        <div class="qt-title">Do&gbreve;ru / Yanl&#305;&scedil;</div>
        <div class="qt-desc">G&ouml;sterilen &ccedil;eviri do&gbreve;ru mu?</div>
      </div>
      <div class="quiz-type-card" onclick="startQuiz('match')">
        <div class="qt-icon">&#128279;</div>
        <div class="qt-title">E&scedil;le&scedil;tirme</div>
        <div class="qt-desc">5 kelimeyi &ccedil;evirileriyle e&scedil;le&scedil;tir</div>
      </div>
      <div class="quiz-type-card" onclick="startQuiz('listen')">
        <div class="qt-icon">&#127911;</div>
        <div class="qt-title">Dinleme</div>
        <div class="qt-desc">Kelimeyi dinle, T&uuml;rk&ccedil;e kar&scedil;&#305;l&#305;&gbreve;&#305;n&#305; se&ccedil;</div>
      </div>
      <div class="quiz-type-card" onclick="startQuiz('reverse')">
        <div class="qt-icon">&#128260;</div>
        <div class="qt-title">Ters &Ccedil;eviri</div>
        <div class="qt-desc">Yabanc&#305; kelimeyi g&ouml;r, T&uuml;rk&ccedil;esini se&ccedil;</div>
      </div>
    </div>
    <div style="text-align:center;margin-top:8px;">
      <div style="display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap;">
        <span style="font-size:0.82em;color:var(--text2);">Soru kayna&gbreve;&#305;:</span>
        <button class="mode-btn quiz-src-btn active" id="qSrcWords" onclick="setQuizSource('words')" style="padding:6px 16px;font-size:0.8em;">Kelimeler</button>
        <button class="mode-btn quiz-src-btn" id="qSrcSent" onclick="setQuizSource('sentences')" style="padding:6px 16px;font-size:0.8em;">C&uuml;mleler</button>
        <button class="mode-btn quiz-src-btn" id="qSrcAll" onclick="setQuizSource('all')" style="padding:6px 16px;font-size:0.8em;">Hepsi</button>
        <span style="font-size:0.82em;color:var(--text2);margin-left:8px;">Soru say&#305;s&#305;:</span>
        <select id="qCount" style="padding:6px 10px;border-radius:10px;background:rgba(255,255,255,0.06);border:1px solid var(--card-border);color:var(--text);font-size:0.85em;">
          <option value="10">10</option>
          <option value="20" selected>20</option>
          <option value="30">30</option>
          <option value="50">50</option>
        </select>
      </div>
    </div>
  </div>
  <!-- Active quiz area -->
  <div class="quiz-area" id="quizArea" style="display:none;"></div>
</div>

<!-- Load More -->
<div id="loadMoreWrap" style="text-align:center;padding:16px 20px;display:none;">
  <div class="lm-info" style="font-size:0.8em;color:var(--text2);margin-bottom:8px;"></div>
  <button onclick="loadMoreCards()" style="padding:10px 32px;border-radius:20px;border:1.5px solid var(--gold);
    background:transparent;color:var(--gold);cursor:pointer;font-size:0.9em;font-weight:600;
    transition:all .3s;letter-spacing:0.5px;">Daha Fazla Y&uuml;kle</button>
</div>

<!-- Empty -->
<div class="empty" id="emptyState" style="display:none">
  <div class="icon">&#128270;</div>
  <div>Sonuç bulunamadı</div>
</div>

<script>
const DATA = {data_json};
const CATS = {cats_json};
const SENT_DATA = {sentences_json};
const SENT_CATS = {sent_cats_json};

const LANG_CODES = {{en:'en-US',de:'de-DE',it:'it-IT',es:'es-ES',fr:'fr-FR'}};
const LANG_LABELS = {{en:'English',de:'Deutsch',it:'Italiano',es:'Español',fr:'Français'}};

let mainMode = 'words'; // 'words' or 'sentences'
let currentLang = 'en';
let activeCats = new Set();
let isFlashcard = false;
let fcIndex = 0;
let fcFiltered = [];
let learned = loadProgress();

function loadProgress(){{
  try{{ return JSON.parse(localStorage.getItem('pdl_learned')||'{{}}'); }}
  catch(e){{ return {{}}; }}
}}
function saveProgress(){{ localStorage.setItem('pdl_learned',JSON.stringify(learned)); }}

function speak(text, lang){{
  if(!window.speechSynthesis) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = LANG_CODES[lang]||'en-US';
  u.rate = 0.85;
  speechSynthesis.speak(u);
}}

function setMainMode(mode){{
  mainMode = mode;
  activeCats.clear();
  document.querySelectorAll('#mainTabs .main-tab').forEach(t=>{{
    const isActive = t.dataset.mode===mode;
    t.classList.toggle('active', isActive);
    if(isActive){{
      t.style.background='linear-gradient(135deg,var(--gold),var(--gold2))';
      t.style.color='var(--navy)';
    }} else {{
      t.style.background='transparent';
      t.style.color='var(--gold)';
    }}
  }});
  if(isFlashcard) {{ isFlashcard=false; document.getElementById('modeBtn').classList.remove('active'); document.getElementById('modeBtn').innerHTML='&#127183; Flashcard Modu'; }}
  render();
}}

function setLang(lang){{
  currentLang = lang;
  document.querySelectorAll('#langTabs .lang-tab').forEach(t=>{{
    t.classList.toggle('active', t.dataset.lang===lang);
  }});
  render();
}}

function toggleCat(catId){{
  if(activeCats.has(catId)) activeCats.delete(catId);
  else activeCats.add(catId);
  render();
}}

function toggleMode(){{
  isFlashcard = !isFlashcard;
  document.getElementById('modeBtn').classList.toggle('active', isFlashcard);
  document.getElementById('modeBtn').innerHTML = isFlashcard ? '&#128196; Kart Görünümü' : '&#127183; Flashcard Modu';
  if(isFlashcard) startFlashcards();
  render();
}}

function getCurrentData(){{ return mainMode==='sentences' ? SENT_DATA : DATA; }}
function getCurrentCats(){{ return mainMode==='sentences' ? SENT_CATS : CATS; }}

function getFiltered(){{
  const src = getCurrentData();
  const q = (document.getElementById('searchBox').value||'').toLowerCase().trim();
  return src.filter(w=>{{
    if(activeCats.size && !activeCats.has(w.cat)) return false;
    if(q){{
      const hay = (w.tr+' '+w[currentLang]+' '+w[currentLang+'_ph']).toLowerCase();
      if(!hay.includes(q)) return false;
    }}
    return true;
  }});
}}

function getLearnedKey(w){{ const prefix = mainMode==='sentences'?'s_':''; return prefix+w.tr+'|'+currentLang; }}

let displayLimit = 60;

function render(){{
  const grid = document.getElementById('wordGrid');
  const fc = document.getElementById('flashcardView');
  const empty = document.getElementById('emptyState');
  const loadMore = document.getElementById('loadMoreWrap');
  const quizView = document.getElementById('quizView');
  const chips = document.getElementById('chipsContainer');
  const controls = document.querySelector('.controls');
  const statsRow = document.getElementById('statsRow');
  const progressWrap = document.getElementById('progressWrap');

  // Quiz mode — hide other views
  if(mainMode==='quiz'){{
    grid.style.display='none';
    fc.style.display='none';
    empty.style.display='none';
    if(loadMore) loadMore.style.display='none';
    quizView.style.display='block';
    chips.style.display='none';
    controls.style.display='none';
    statsRow.style.display='none';
    progressWrap.style.display='none';
    return;
  }}

  // Words/Sentences mode
  quizView.style.display='none';
  chips.style.display='flex';
  controls.style.display='flex';
  statsRow.style.display='flex';
  progressWrap.style.display='flex';

  renderChips();
  renderStats();
  const filtered = getFiltered();

  if(isFlashcard){{
    grid.style.display='none';
    fc.style.display='block';
    empty.style.display='none';
    if(loadMore) loadMore.style.display='none';
    fcFiltered = filtered;
    if(fcIndex >= fcFiltered.length) fcIndex = 0;
    renderFlashcard();
  }} else {{
    fc.style.display='none';
    // Sentences use wider cards
    if(mainMode==='sentences'){{
      grid.style.gridTemplateColumns='repeat(auto-fill,minmax(340px,1fr))';
    }} else {{
      grid.style.gridTemplateColumns='repeat(auto-fill,minmax(260px,1fr))';
    }}
    if(!filtered.length){{
      grid.style.display='none';
      empty.style.display='block';
      if(loadMore) loadMore.style.display='none';
    }} else {{
      empty.style.display='none';
      grid.style.display='grid';
      displayLimit = 60;
      const show = filtered.slice(0, displayLimit);
      grid.innerHTML = show.map(w=>cardHTML(w)).join('');
      if(loadMore){{
        loadMore.style.display = filtered.length > displayLimit ? 'block' : 'none';
        loadMore.querySelector('.lm-info').textContent = show.length+' / '+filtered.length+' gösteriliyor';
      }}
    }}
  }}
  renderProgress();
}}

function loadMoreCards(){{
  const filtered = getFiltered();
  displayLimit += 60;
  const grid = document.getElementById('wordGrid');
  const show = filtered.slice(0, displayLimit);
  grid.innerHTML = show.map(w=>cardHTML(w)).join('');
  const loadMore = document.getElementById('loadMoreWrap');
  if(loadMore){{
    loadMore.style.display = filtered.length > displayLimit ? 'block' : 'none';
    loadMore.querySelector('.lm-info').textContent = show.length+' / '+filtered.length+' gösteriliyor';
  }}
}}

function cardHTML(w){{
  const word = w[currentLang];
  const ph = w[currentLang+'_ph'];
  const cats = getCurrentCats();
  const cat = cats.find(c=>c.id===w.cat);
  const lk = getLearnedKey(w);
  const isL = learned[lk];
  const isSent = mainMode==='sentences';
  const wordStyle = isSent ? 'font-size:1.05em;' : '';
  return `<div class="card" style="${{isL?'border-color:#2ecc71;':''}}" >
    <span class="cat-badge">${{cat?cat.icon+' '+cat.label:''}}</span>
    <div class="word" style="${{wordStyle}}">${{word}}</div>
    <div class="phonetic">[${{ph}}]</div>
    <div class="turkish">${{w.tr}}</div>
    <button class="play-btn" onclick="speak('${{word.replace(/'/g,"\\\\'")}}','${{currentLang}}')">
      <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> Dinle
    </button>
  </div>`;
}}

function renderChips(){{
  const c = document.getElementById('chipsContainer');
  const cats = getCurrentCats();
  const src = getCurrentData();
  const isSent = mainMode==='sentences';

  // Count items per category
  const catCounts = {{}};
  src.forEach(w=>{{ catCounts[w.cat]=(catCounts[w.cat]||0)+1; }});

  if(isSent){{
    // Sentences mode: big prominent category buttons with counts
    c.style.gap='8px';
    c.innerHTML = `<div class="chip ${{activeCats.size===0?'active':''}}" onclick="clearCats()" style="padding:10px 18px;font-size:0.88em;font-weight:700;border-radius:20px;">&#128172; T&uuml;m&uuml; (${{src.length}})</div>` +
      cats.map(cat=>{{
        const cnt = catCounts[cat.id]||0;
        const isA = activeCats.has(cat.id);
        return `<div class="chip ${{isA?'active':''}}" onclick="selectSentCat('${{cat.id}}')" style="padding:10px 18px;font-size:0.88em;font-weight:700;border-radius:20px;">${{cat.icon}} ${{cat.label}} <span style="opacity:0.7;font-size:0.85em;">(${{cnt}})</span></div>`;
      }}).join('');
  }} else {{
    // Words mode: standard chips
    c.style.gap='7px';
    c.innerHTML = cats.map(cat=>
      `<div class="chip ${{activeCats.has(cat.id)?'active':''}}" onclick="toggleCat('${{cat.id}}')">${{cat.icon}} ${{cat.label}} <span style="opacity:0.6;font-size:0.85em;">(${{catCounts[cat.id]||0}})</span></div>`
    ).join('');
  }}
}}

function clearCats(){{
  activeCats.clear();
  render();
}}

function selectSentCat(catId){{
  activeCats.clear();
  activeCats.add(catId);
  render();
}}

function renderStats(){{
  const src = getCurrentData();
  const total = src.length;
  const prefix = mainMode==='sentences'?'s_':'';
  const learnedCount = Object.keys(learned).filter(k=>k.endsWith('|'+currentLang)&&k.startsWith(prefix)&&learned[k]).length;
  const catCounts = {{}};
  src.forEach(w=>{{ catCounts[w.cat]=(catCounts[w.cat]||0)+1; }});
  const activeCatCount = activeCats.size||Object.keys(catCounts).length;
  const typeLabel = mainMode==='sentences'?'Cümle':'Kelime';
  document.getElementById('statsRow').innerHTML = `
    <div class="stat-card"><div class="sv">${{total}}</div><div class="sl">Toplam ${{typeLabel}}</div></div>
    <div class="stat-card"><div class="sv">${{learnedCount}}</div><div class="sl">Öğrenilen</div></div>
    <div class="stat-card"><div class="sv">${{total-learnedCount}}</div><div class="sl">Kalan</div></div>
    <div class="stat-card"><div class="sv">${{activeCatCount}}</div><div class="sl">Kategori</div></div>
  `;
}}

function renderProgress(){{
  const src = getCurrentData();
  const total = src.length;
  const prefix = mainMode==='sentences'?'s_':'';
  const learnedCount = Object.keys(learned).filter(k=>k.endsWith('|'+currentLang)&&k.startsWith(prefix)&&learned[k]).length;
  const pct = total?Math.round(learnedCount/total*100):0;
  document.getElementById('progressFill').style.width = pct+'%';
  document.getElementById('progressPct').textContent = pct+'%';
}}

/* ─── Flashcard ─── */
function startFlashcards(){{
  fcFiltered = getFiltered();
  fcIndex = 0;
  renderFlashcard();
}}

function renderFlashcard(){{
  const fc = document.getElementById('flashcard');
  fc.classList.remove('flipped');
  if(!fcFiltered.length){{ document.getElementById('fcWord').textContent='—'; return; }}
  const w = fcFiltered[fcIndex];
  document.getElementById('fcWord').textContent = w.tr;
  document.getElementById('fcAnswer').textContent = w[currentLang];
  document.getElementById('fcPhonetic').textContent = '['+w[currentLang+'_ph']+']';
  document.getElementById('fcTurkish').textContent = w.tr;
  document.getElementById('fcCounter').textContent = (fcIndex+1)+' / '+fcFiltered.length;
}}

function flipCard(){{ document.getElementById('flashcard').classList.toggle('flipped'); }}

function playFlashcardAudio(){{
  if(!fcFiltered.length) return;
  const w = fcFiltered[fcIndex];
  speak(w[currentLang], currentLang);
}}

function markCard(action){{
  if(!fcFiltered.length) return;
  const w = fcFiltered[fcIndex];
  const lk = getLearnedKey(w);
  if(action==='learned'){{ learned[lk]=true; saveProgress(); }}
  else if(action==='repeat'){{ learned[lk]=false; saveProgress(); }}
  fcIndex++;
  if(fcIndex>=fcFiltered.length) fcIndex=0;
  renderFlashcard();
  renderProgress();
  renderStats();
}}

/* ═══ QUIZ ENGINE ═══ */
let quizSource = 'words';
let quizType = '';
let quizQuestions = [];
let quizIndex = 0;
let quizCorrect = 0;
let quizAnswered = false;
// match state
let matchLeft = null;
let matchPairs = [];
let matchMatched = 0;

function setQuizSource(src){{
  quizSource = src;
  document.querySelectorAll('.quiz-src-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(src==='words'?'qSrcWords':src==='sentences'?'qSrcSent':'qSrcAll').classList.add('active');
}}

function getQuizPool(){{
  if(quizSource==='words') return DATA.slice();
  if(quizSource==='sentences') return SENT_DATA.slice();
  return DATA.concat(SENT_DATA);
}}

function shuffle(arr){{
  for(let i=arr.length-1;i>0;i--){{
    const j=Math.floor(Math.random()*(i+1));
    [arr[i],arr[j]]=[arr[j],arr[i]];
  }}
  return arr;
}}

function startQuiz(type){{
  quizType = type;
  const pool = getQuizPool();
  const count = parseInt(document.getElementById('qCount').value)||20;
  quizQuestions = shuffle(pool).slice(0, Math.min(count, pool.length));
  quizIndex = 0;
  quizCorrect = 0;
  quizAnswered = false;
  document.getElementById('quizTypeSelect').style.display='none';
  document.getElementById('quizArea').style.display='block';
  if(type==='match') renderMatchQuiz();
  else renderQuizQuestion();
}}

function endQuiz(){{
  document.getElementById('quizTypeSelect').style.display='block';
  document.getElementById('quizArea').style.display='none';
}}

function renderQuizQuestion(){{
  const area = document.getElementById('quizArea');
  if(quizIndex >= quizQuestions.length){{
    renderQuizResult();
    return;
  }}
  quizAnswered = false;
  const q = quizQuestions[quizIndex];
  const total = quizQuestions.length;
  const pct = Math.round(quizIndex/total*100);
  const lang = currentLang;
  const word = q[lang];
  const ph = q[lang+'_ph'];
  const tr = q.tr;

  let headerHTML = `
    <div class="quiz-header">
      <div class="qh-title">${{getQuizTitle()}}</div>
      <div class="qh-score">Soru ${{quizIndex+1}}/${{total}} &bull; <b>${{quizCorrect}} do&gbreve;ru</b></div>
    </div>
    <div class="quiz-progress"><div class="quiz-progress-fill" style="width:${{pct}}%"></div></div>`;

  if(quizType==='mc'){{
    // Multiple choice: show Turkish, pick translation
    const options = generateOptions(q, lang, 'word');
    area.innerHTML = headerHTML + `
      <div class="quiz-question">
        <div class="qq-label">Bu kelimenin ${{LANG_LABELS[lang]}} kar&scedil;&#305;l&#305;&gbreve;&#305; nedir?</div>
        <div class="qq-word">${{tr}}</div>
      </div>
      <div class="quiz-options">${{options.map((o,i)=>
        `<div class="quiz-opt" id="qopt${{i}}" onclick="checkMC(${{i}},${{options.indexOf(word)}})">${{o}}</div>`
      ).join('')}}</div>`;

  }} else if(quizType==='reverse'){{
    // Reverse: show foreign word, pick Turkish
    const options = generateOptions(q, 'tr_reverse', 'tr');
    area.innerHTML = headerHTML + `
      <div class="quiz-question">
        <div class="qq-label">${{LANG_LABELS[lang]}} &rarr; T&uuml;rk&ccedil;e</div>
        <div class="qq-word">${{word}}</div>
        <div class="qq-hint">[${{ph}}]</div>
      </div>
      <div class="quiz-options">${{options.map((o,i)=>
        `<div class="quiz-opt" id="qopt${{i}}" onclick="checkMC(${{i}},${{options.indexOf(tr)}})">${{o}}</div>`
      ).join('')}}</div>`;

  }} else if(quizType==='write'){{
    area.innerHTML = headerHTML + `
      <div class="quiz-question">
        <div class="qq-label">${{LANG_LABELS[lang]}} kar&scedil;&#305;l&#305;&gbreve;&#305;n&#305; yaz&#305;n</div>
        <div class="qq-word">${{tr}}</div>
      </div>
      <div class="quiz-input-wrap">
        <input class="quiz-input" id="qInput" type="text" placeholder="${{LANG_LABELS[lang]}} kar&scedil;&#305;l&#305;&gbreve;&#305;..." onkeydown="if(event.key==='Enter')checkWrite()">
        <br><button class="quiz-check-btn" onclick="checkWrite()">Kontrol Et</button>
        <div id="qWriteFeedback" style="margin-top:10px;font-size:0.9em;"></div>
      </div>`;
    setTimeout(()=>{{const inp=document.getElementById('qInput');if(inp)inp.focus();}},100);

  }} else if(quizType==='tf'){{
    const isCorrect = Math.random()>0.4;
    const shown = isCorrect ? word : getRandomWrong(q, lang);
    area.innerHTML = headerHTML + `
      <div class="quiz-question">
        <div class="qq-label">Bu &ccedil;eviri do&gbreve;ru mu?</div>
        <div class="qq-word">${{tr}}</div>
        <div style="margin-top:12px;font-size:1.2em;color:var(--gold);">= ${{shown}}</div>
      </div>
      <div class="quiz-tf-btns">
        <button class="quiz-tf-btn" id="tfTrue" onclick="checkTF(true,${{isCorrect}})">&#9989; Do&gbreve;ru</button>
        <button class="quiz-tf-btn" id="tfFalse" onclick="checkTF(false,${{isCorrect}})">&#10060; Yanl&#305;&scedil;</button>
      </div>
      <div id="qTfFeedback" style="text-align:center;font-size:0.9em;"></div>`;

  }} else if(quizType==='listen'){{
    const options = generateOptions(q, 'tr_reverse', 'tr');
    area.innerHTML = headerHTML + `
      <div class="quiz-question">
        <div class="qq-label">Dinle ve T&uuml;rk&ccedil;e kar&scedil;&#305;l&#305;&gbreve;&#305;n&#305; se&ccedil;</div>
        <button class="quiz-listen-btn" onclick="speak('${{word.replace(/'/g,"\\\\'")}}','${{lang}}')">&#128266;</button>
        <div class="qq-hint">Sesi dinlemek i&ccedil;in t&#305;klay&#305;n</div>
      </div>
      <div class="quiz-options">${{options.map((o,i)=>
        `<div class="quiz-opt" id="qopt${{i}}" onclick="checkMC(${{i}},${{options.indexOf(tr)}})">${{o}}</div>`
      ).join('')}}</div>`;
    // Auto play
    setTimeout(()=>speak(word,lang),300);
  }}
}}

function getQuizTitle(){{
  const titles = {{mc:'&Ccedil;oktan Se&ccedil;meli',write:'Yazarak Cevapla',tf:'Do&gbreve;ru / Yanl&#305;&scedil;',match:'E&scedil;le&scedil;tirme',listen:'Dinleme',reverse:'Ters &Ccedil;eviri'}};
  return titles[quizType]||'Al&#305;&scedil;t&#305;rma';
}}

function generateOptions(q, field, type){{
  const pool = getQuizPool();
  const lang = currentLang;
  let correct, others;
  if(type==='tr'){{
    correct = q.tr;
    others = shuffle(pool.filter(w=>w.tr!==correct)).slice(0,3).map(w=>w.tr);
  }} else {{
    correct = q[lang];
    others = shuffle(pool.filter(w=>w[lang]!==correct)).slice(0,3).map(w=>w[lang]);
  }}
  const opts = shuffle([correct,...others]);
  return opts;
}}

function getRandomWrong(q, lang){{
  const pool = getQuizPool();
  const filtered = pool.filter(w=>w[lang]!==q[lang]);
  return filtered.length ? filtered[Math.floor(Math.random()*filtered.length)][lang] : q[lang];
}}

function checkMC(selected, correctIdx){{
  if(quizAnswered) return;
  quizAnswered = true;
  const opts = document.querySelectorAll('.quiz-opt');
  opts.forEach((o,i)=>{{
    o.classList.add('disabled');
    if(i===correctIdx) o.classList.add('correct');
    if(i===selected && i!==correctIdx) o.classList.add('wrong');
  }});
  if(selected===correctIdx) quizCorrect++;
  setTimeout(()=>{{ quizIndex++; renderQuizQuestion(); }}, 1200);
}}

function checkWrite(){{
  if(quizAnswered) return;
  quizAnswered = true;
  const inp = document.getElementById('qInput');
  const fb = document.getElementById('qWriteFeedback');
  const q = quizQuestions[quizIndex];
  const correct = q[currentLang];
  const userAns = (inp.value||'').trim();
  const isCorrect = userAns.toLowerCase().replace(/[.!?,;:¿¡]/g,'').trim() === correct.toLowerCase().replace(/[.!?,;:¿¡]/g,'').trim();
  if(isCorrect){{
    inp.classList.add('correct');
    fb.innerHTML = '<span style="color:#2ecc71;">&#9989; Do&gbreve;ru!</span>';
    quizCorrect++;
  }} else {{
    inp.classList.add('wrong');
    fb.innerHTML = `<span style="color:#e74c3c;">&#10060; Yanl&#305;&scedil;.</span> Do&gbreve;ru cevap: <b style="color:var(--gold);">${{correct}}</b>`;
  }}
  setTimeout(()=>{{ quizIndex++; renderQuizQuestion(); }}, 1800);
}}

function checkTF(userAnswer, isCorrect){{
  if(quizAnswered) return;
  quizAnswered = true;
  const fb = document.getElementById('qTfFeedback');
  const right = userAnswer===isCorrect;
  if(right){{
    quizCorrect++;
    fb.innerHTML = '<span style="color:#2ecc71;">&#9989; Do&gbreve;ru!</span>';
  }} else {{
    fb.innerHTML = `<span style="color:#e74c3c;">&#10060; Yanl&#305;&scedil;!</span> Do&gbreve;ru cevap: <b style="color:var(--gold);">${{quizQuestions[quizIndex][currentLang]}}</b>`;
  }}
  document.getElementById(userAnswer?'tfTrue':'tfFalse').classList.add(right?'correct':'wrong');
  if(!right) document.getElementById(userAnswer?'tfFalse':'tfTrue').classList.add('correct');
  setTimeout(()=>{{ quizIndex++; renderQuizQuestion(); }}, 1400);
}}

/* ─── Match Quiz ─── */
function renderMatchQuiz(){{
  const area = document.getElementById('quizArea');
  const pool = getQuizPool();
  const lang = currentLang;
  const total = quizQuestions.length;
  const batchSize = 5;
  const batchStart = quizIndex;
  const batch = quizQuestions.slice(batchStart, batchStart+batchSize);
  if(!batch.length){{ renderQuizResult(); return; }}

  matchPairs = batch;
  matchLeft = null;
  matchMatched = 0;
  const pct = Math.round(batchStart/total*100);

  const leftItems = batch.map((w,i)=>({{id:'L'+i, text:w.tr, pairIdx:i, side:'left'}}));
  const rightItems = shuffle(batch.map((w,i)=>({{id:'R'+i, text:w[lang], pairIdx:i, side:'right'}})));

  area.innerHTML = `
    <div class="quiz-header">
      <div class="qh-title">E&scedil;le&scedil;tirme</div>
      <div class="qh-score">${{batchStart}}/${{total}} tamamland&#305; &bull; <b>${{quizCorrect}} do&gbreve;ru</b></div>
    </div>
    <div class="quiz-progress"><div class="quiz-progress-fill" style="width:${{pct}}%"></div></div>
    <div class="quiz-match-grid">
      <div>${{leftItems.map(it=>
        `<div class="quiz-match-item" id="${{it.id}}" data-pair="${{it.pairIdx}}" data-side="left" onclick="matchClick(this)">${{it.text}}</div>`
      ).join('')}}</div>
      <div>${{rightItems.map(it=>
        `<div class="quiz-match-item" id="${{it.id}}" data-pair="${{it.pairIdx}}" data-side="right" onclick="matchClick(this)">${{it.text}}</div>`
      ).join('')}}</div>
    </div>`;
}}

function matchClick(el){{
  if(el.classList.contains('matched')) return;
  const side = el.dataset.side;
  const pair = parseInt(el.dataset.pair);

  if(!matchLeft){{
    if(side!=='left') return;
    document.querySelectorAll('.quiz-match-item.selected').forEach(e=>e.classList.remove('selected'));
    el.classList.add('selected');
    matchLeft = {{el, pair}};
  }} else {{
    if(side!=='right'){{
      matchLeft.el.classList.remove('selected');
      if(side==='left'){{el.classList.add('selected'); matchLeft={{el,pair}};}}
      else matchLeft=null;
      return;
    }}
    // Check match
    if(pair===matchLeft.pair){{
      matchLeft.el.classList.remove('selected');
      matchLeft.el.classList.add('matched');
      el.classList.add('matched');
      matchMatched++;
      quizCorrect++;
      quizIndex++;
    }} else {{
      matchLeft.el.classList.add('error');
      el.classList.add('error');
      setTimeout(()=>{{
        matchLeft.el.classList.remove('error','selected');
        el.classList.remove('error');
      }},600);
    }}
    matchLeft = null;
    if(matchMatched>=matchPairs.length){{
      setTimeout(()=>renderMatchQuiz(),800);
    }}
  }}
}}

/* ─── Quiz Result ─── */
function renderQuizResult(){{
  const area = document.getElementById('quizArea');
  const total = quizQuestions.length;
  const pct = Math.round(quizCorrect/total*100);
  const emoji = pct>=90?'&#127942;':pct>=70?'&#11088;':pct>=50?'&#128170;':'&#128218;';
  const msg = pct>=90?'M&uuml;kemmel!':pct>=70?'&Ccedil;ok iyi!':pct>=50?'&#304;yi, devam et!':'Biraz daha &ccedil;al&#305;&scedil;!';
  const barColor = pct>=70?'#2ecc71':pct>=50?'#f39c12':'#e74c3c';
  area.innerHTML = `
    <div class="quiz-result">
      <div class="qr-icon">${{emoji}}</div>
      <div class="qr-score">${{quizCorrect}} / ${{total}}</div>
      <div class="qr-label">%${{pct}} ba&scedil;ar&#305; &bull; ${{msg}}</div>
      <div class="qr-bar"><div class="qr-bar-fill" style="width:${{pct}}%;background:${{barColor}};"></div></div>
      <br>
      <button class="quiz-next-btn" onclick="endQuiz()">&#128260; Yeni Al&#305;&scedil;t&#305;rma</button>
    </div>`;
}}

/* ─── Init ─── */
document.getElementById('searchBox').addEventListener('input', ()=>render());
render();
</script>
</body>
</html>'''


def render_pratik_dil():
    """Render the Premium Pratik Dil Ogrenme module."""
    html_str = _build_html()
    components.html(html_str, height=1100, scrolling=True)
