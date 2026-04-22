# -*- coding: utf-8 -*-
"""
11. Sinif Fizik dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Kuvvet ve Hareket
2. Elektrik ve Manyetizma
3. Modern Fizik Giris
"""

FIZIK_11_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: KUVVET VE HAREKET
# ═══════════════════════════════════════════════════════════════

"FIZ.11.1.KUVVET_DENGE": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Kuvvet ve Denge",
    "icerik": """
KUVVET VE DENGE:

1. KUVVETIN VEKTOREL OZELLIGI:
   - Kuvvet bir vektor buyukluktur: buyukluk, yon ve dogrultusu vardir
   - Birimi: Newton (N) = kg*m/s^2
   - Bileskesi: Vektorel toplama ile bulunur
   - Paralel kuvvetler: Ayni yonde toplam, zit yonde fark alinir

2. KUVVET BILESENLERI:
   - Fx = F*cos(teta), Fy = F*sin(teta)
   - Bileske kuvvet: F_R = karekök(Fx^2 + Fy^2)
   - Yon acisi: tan(teta) = Fy/Fx

3. DENGE KOSULLARI:
   - Oteleme dengesi: toplam F = 0 (net kuvvet sifir)
   - Donme dengesi: toplam tork = 0 (net tork sifir)
   - Statik denge: Cisim hem oteleme hem donme dengesinde
   - Stabil / Labil / Notr denge turleri

4. TORK (KUVVET MOMENTI):
   - tork = F*d (d: kuvvet kolunun uzunlugu)
   - Birimi: N*m
   - Saat yonunde (-), saat yonunun tersinde (+)
   - Kuvvetin uygulama noktasi onemlidir

5. AGIRLIK MERKEZI:
   - Duzenli cisimlerde geometrik merkez
   - Duzensiz cisimlerde: x_am = toplam(mi*xi) / toplam(mi)
   - Agirlik merkezi cismin disinda olabilir (halka, L seklinde cisim)
"""
},

"FIZ.11.1.NEWTON_HAREKET": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Newton'un Hareket Yasalari",
    "icerik": """
NEWTON'UN HAREKET YASALARI:

1. NEWTON'UN 1. YASASI (EYLEMSIZLIK):
   - Net kuvvet sifir ise cisim durgunsa durgun, hareketliyse sabit hizla hareket eder
   - Eylemsizlik: Cismin mevcut hareket durumunu koruma egilimi
   - Kutle, eylemsizligin olcusudur
   - Referans cercevesi: Eylemsiz (inersiyal) referans cercevesinde gecerlidir

2. NEWTON'UN 2. YASASI:
   - F_net = m*a (net kuvvet = kutle x ivme)
   - Ivme, net kuvvetle dogru, kutle ile ters orantilidir
   - Ayni kuvvet altinda buyuk kutleli cisim daha az ivmelenir
   - Birimi: 1 N = 1 kg * 1 m/s^2

3. NEWTON'UN 3. YASASI (ETKI-TEPKI):
   - Her etkiye esit buyuklukte ve zit yonde tepki vardir
   - F_12 = -F_21
   - Etki-tepki kuvvetleri farkli cisimlere uygulanir
   - Ornek: Yere basan ayak yeri iter, yer ayagi iter

4. SURTUNME KUVVETI:
   - Statik surtunme: f_s <= mu_s * N (hareket baslamadan once)
   - Kinetik surtunme: f_k = mu_k * N (hareket sirasinda)
   - mu_s > mu_k (statik surtunme katsayisi her zaman buyuktur)
   - N: Normal kuvvet (yuzey tepki kuvveti)
   - Surtunme, temas yuzeyinin cinsine ve puruslugune baglidir

5. EGIK DUZLEM:
   - Agirligin bilesenleri: Fg_paralel = mg*sin(teta), Fg_dik = mg*cos(teta)
   - Normal kuvvet: N = mg*cos(teta) (ek kuvvet yoksa)
   - Surtunmesiz egik duzlemde ivme: a = g*sin(teta)
   - Surtunmeli egik duzlemde ivme: a = g*(sin(teta) - mu_k*cos(teta))
"""
},

"FIZ.11.1.IS_ENERJI": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Is, Guc ve Enerji",
    "icerik": """
IS, GUC VE ENERJI:

1. IS (W):
   - W = F*d*cos(teta) (kuvvet x yer degistirme x aradaki acinin kosinusu)
   - Birimi: Joule (J) = N*m
   - teta = 0 -> W = F*d (maksimum is)
   - teta = 90 -> W = 0 (kuvvet harekete dik ise is yapilmaz)
   - teta > 90 -> Negatif is (kuvvet harekete zit)

2. GUC (P):
   - P = W/t = F*v*cos(teta) (is/zaman veya kuvvet x hiz)
   - Birimi: Watt (W) = J/s
   - 1 Beygir Gucu (HP) = 746 W (yaklasik)
   - Ortalama guc ve anlik guc ayrimi

3. KINETIK ENERJI:
   - Ek = (1/2)*m*v^2
   - Hareket halindeki cismin enerjisi
   - Is-Kinetik Enerji Teoremi: W_net = delta(Ek) = (1/2)*m*v2^2 - (1/2)*m*v1^2
   - Net is, kinetik enerjideki degisime esittir

4. POTANSIYEL ENERJI:
   - Yercekim potansiyel enerjisi: Ep = m*g*h
   - Referans noktasina gore olculur
   - h: cismin referans noktasina gore yuksekligi
   - Yay potansiyel enerjisi: Ep = (1/2)*k*x^2 (k: yay sabiti, x: uzama)

5. MEKANIK ENERJININ KORUNUMU:
   - Ek1 + Ep1 = Ek2 + Ep2 (surtunme yoksa)
   - Mekanik enerji = Kinetik enerji + Potansiyel enerji
   - Surtunme varsa: Ek1 + Ep1 = Ek2 + Ep2 + W_surtunme
   - Enerji yoktan var edilemez, vardan yok edilemez (Enerjinin Korunumu Yasasi)

6. ENERJI DONUSUMLERI:
   - Yuksekten dusen cisim: Ep -> Ek
   - Yukari firlatilan cisim: Ek -> Ep
   - Surtunme: Mekanik enerji -> Isi enerjisi
   - Verimlilik: n = (Faydali enerji / Toplam enerji) x 100%
"""
},

"FIZ.11.1.ITME_MOMENTUM": {
    "unite": "Kuvvet ve Hareket",
    "baslik": "Itme ve Momentum",
    "icerik": """
ITME VE MOMENTUM:

1. MOMENTUM (p):
   - p = m*v (kutle x hiz)
   - Vektor buyukluktur (hizin yonundedir)
   - Birimi: kg*m/s
   - Buyuk kutleli ve hizli cisimler buyuk momentuma sahiptir

2. ITME (J):
   - J = F*delta_t (kuvvet x zaman araligi)
   - J = delta_p = m*v2 - m*v1 (momentumdaki degisim)
   - Birimi: N*s = kg*m/s
   - Ayni itme icin: Kuvvet artarsa sure azalir (veya tersi)

3. MOMENTUMUN KORUNUMU:
   - Dis kuvvet yoksa (izole sistem): toplam(p_once) = toplam(p_sonra)
   - m1*v1 + m2*v2 = m1*v1' + m2*v2'
   - Carpisma, patlama ve geri tepme olaylarinda gecerlidir

4. CARPISMA TURLERI:
   - Esnek carpisma: Kinetik enerji ve momentum korunur
     -> Bilardo toplarinin carpismas
   - Esnek olmayan carpisma: Sadece momentum korunur, kinetik enerji korunmaz
   - Tam esnek olmayan: Cisimler yapisisir, birlikte hareket eder
     -> m1*v1 + m2*v2 = (m1+m2)*v_ortak

5. UYGULAMALAR:
   - Roket itisi: Gaz geriye firlatilir, roket ileri gider (3. yasa + momentum korunumu)
   - Hava yastiklarinin etkisi: Carpismada sureyi artirarak kuvveti azaltir
   - Tufegin geri tepmesi: m_mermi * v_mermi = m_tufek * v_tufek
   - Buz uzerinde kayan iki patenci: Birbirini itmesi
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: ELEKTRIK VE MANYETIZMA
# ═══════════════════════════════════════════════════════════════

"FIZ.11.2.ELEKTRIK_ALAN_POTANSIYEL": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Elektrik Alan ve Elektrik Potansiyel",
    "icerik": """
ELEKTRIK ALAN VE ELEKTRIK POTANSIYEL:

1. ELEKTRIK YUKU VE COULOMB YASASI:
   - Temel yuk birimi: e = 1,6 x 10^(-19) C
   - Coulomb Yasasi: F = k*|q1*q2|/r^2
   - k = 9 x 10^9 N*m^2/C^2 (Coulomb sabiti)
   - Ayni isaret yukler itisir, zit isaret yukler cekilir
   - Kuvvet, yuklerle dogru, uzakligin karesiyle ters orantili

2. ELEKTRIK ALAN (E):
   - E = F/q0 (birim pozitif yuke etki eden kuvvet)
   - Birimi: N/C veya V/m
   - Nokta yukun alani: E = k*|q|/r^2
   - Alan cizgileri pozitif yuktan cikar, negatif yuke girer
   - Duzgun elektrik alan: Paralel plakalar arasinda E = V/d

3. ELEKTRIK POTANSIYEL (V):
   - V = k*q/r (nokta yukun potansiyeli)
   - Birimi: Volt (V) = J/C
   - Potansiyel fark: delta_V = V_A - V_B
   - Pozitif yuk yuksek potansiyelden alcak potansiyele hareket eder

4. ELEKTRIK POTANSIYEL ENERJI:
   - U = k*q1*q2/r (iki yuk arasi potansiyel enerji)
   - W = q*delta_V (yuk tasimak icin yapilan is)
   - Esit potansiyel yuzeylerinde yuk tasimak is gerektirmez

5. KONDANSATORLER:
   - Kapasite: C = Q/V (birimi: Farad, F)
   - Paralel plaka: C = epsilon_0*A/d (A: alan, d: plakalar arasi mesafe)
   - Depolanan enerji: U = (1/2)*C*V^2 = Q^2/(2C)
   - Dielektrik: Plakalar arasina yalitkan koymak kapasiteyi artirir (C' = kappa*C)
"""
},

"FIZ.11.2.ELEKTRIK_DEVRE": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Elektrik Akimi ve Devreler",
    "icerik": """
ELEKTRIK AKIMI VE DEVRELER:

1. ELEKTRIK AKIMI (I):
   - I = Q/t (birim zamanda gecen yuk miktari)
   - Birimi: Amper (A) = C/s
   - Akim yonu: Pozitif yuklerin hareket yonu (konvansiyonel)
   - Elektronlar akimin ters yonunde hareket eder
   - DC (dogru akim): Yonu ve siddeti degismeyen akim

2. OHM YASASI:
   - V = I*R (gerilim = akim x direnc)
   - R: Direnc, birimi Ohm = V/A
   - Iletkenin direnci: R = ro*L/A (ro: ozdirenc, L: uzunluk, A: kesit alani)
   - Sicaklik artinca metallerin direnci artar

3. SERI BAGLANTI:
   - Ayni akim: I = I1 = I2 = I3
   - Gerilim paylasimi: V = V1 + V2 + V3
   - Toplam direnc: R_t = R1 + R2 + R3 (direncler toplanir)
   - Bir eleman bozulursa tum devre acilik olur

4. PARALEL BAGLANTI:
   - Ayni gerilim: V = V1 = V2 = V3
   - Akim paylasimi: I = I1 + I2 + I3
   - Toplam direnc: 1/R_t = 1/R1 + 1/R2 + 1/R3 (toplam direnc her birinden kucuk)
   - Bir eleman bozulursa diger kollar calismaya devam eder

5. ELEKTRIKSEL GUC VE ENERJI:
   - P = V*I = I^2*R = V^2/R
   - Birimi: Watt (W)
   - Elektrik enerjisi: E = P*t = V*I*t
   - Birimi: Joule (J) veya kWh (1 kWh = 3,6 x 10^6 J)

6. KIRCHHOFF KURALLARI:
   - Dugum kurali: Bir duguma giren akimlarin toplami = cikan akimlarin toplami
   - Cevrim kurali: Kapali bir cevrimdeki gerilim dususlerinin toplami = EMK toplami
   - Karisik devrelerin cozumunde kullanilir
"""
},

"FIZ.11.2.MANYETIZMA": {
    "unite": "Elektrik ve Manyetizma",
    "baslik": "Manyetizma ve Elektromanyetik Induksiyon",
    "icerik": """
MANYETIZMA VE ELEKTROMANYETIK INDUKSIYON:

1. MANYETIK ALAN:
   - Manyetik alan cizgileri N kutbundan cikar, S kutbuna girer
   - Birimi: Tesla (T) = Wb/m^2
   - Dunya bir dogal miknatistir (cografi kuzey yaklasik olarak manyetik guney)
   - Manyetik alan cizgileri kapali egridir (baslangic ve bitis yoktur)

2. AKIM TASIVAN ILETKENIN MANYETIK ALANI:
   - Dogru iletken: B = mu_0*I/(2*pi*r) (Biot-Savart)
   - Sag el kurali: Bas parmak akim yonu, parmaklar alan yonu
   - Dairesel iletken merkezinde: B = mu_0*I/(2r)
   - Selenoid icinde: B = mu_0*n*I (n: birim uzunluktaki sarim sayisi)
   - mu_0 = 4*pi x 10^(-7) T*m/A (vakumun manyetik gecirgenligi)

3. MANYETIK KUVVET:
   - Yuk uzerine: F = q*v*B*sin(teta)
   - Akim tasiyan tele: F = B*I*L*sin(teta)
   - Yon: Sag el kurali veya vektor carpim (F = qv x B)
   - Manyetik kuvvet is yapmaz (kuvvet hiza dik)

4. ELEKTROMANYETIK INDUKSIYON:
   - Faraday Yasasi: EMK = -delta(Fi)/delta(t) (manyetik aki degisimi EMK olusturur)
   - Manyetik aki: Fi = B*A*cos(teta) (birimi: Weber, Wb)
   - Lenz Yasasi: Induksiyon akimi, onu olusturan degisime karsi koyan yondedir
   - Induksiyon yollari: Manyetik alan, alan yuzeyi veya aci degisimi

5. UYGULAMALAR:
   - Elektrik motoru: Manyetik alandaki akim tasiyan bobine etki eden kuvvet
   - Jenerator (dinamo): Mekanik enerjiyi elektrik enerjisine donusturur
   - Transformator: Gerilim yukseltme/dusurme (V1/V2 = N1/N2)
   - Induksiyon ocagi: Degisen manyetik alan ile eddy akimlari olusturma
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: MODERN FIZIK GIRIS
# ═══════════════════════════════════════════════════════════════

"FIZ.11.3.MODERN_FIZIK": {
    "unite": "Modern Fizik Giris",
    "baslik": "Ozel Gorelilik ve Kuantum Fizigine Giris",
    "icerik": """
MODERN FIZIK GIRIS:

1. OZEL GORELILIK TEORISI (EINSTEIN, 1905):
   - Postulat 1: Fizik yasalari tum eylemsiz referans cercevelerinde aynidir
   - Postulat 2: Isik hizi (c = 3x10^8 m/s yaklasik) tum gozlemciler icin sabittir
   - Hicbir maddesel cisim isik hizina ulasamaz
   - Zaman genlemesi: delta_t = delta_t0 / karekök(1 - v^2/c^2) (hareket eden saatler yavaslar)
   - Uzunluk kisalmasi: L = L0*karekök(1 - v^2/c^2) (hareket yonunde kisalma)
   - Kutle-enerji esdegerligi: E = mc^2

2. FOTOELEKTRIK OLAY:
   - Isik metal yuzeyine dusunce elektron kopartir
   - Einstein aciklamasi: Isik fotonlardan olusur, E = h*f
   - h: Planck sabiti = 6,63 x 10^(-34) J*s
   - Esik frekans: f0 = W0/h (W0: cikis isi)
   - Kinetik enerji: Ek_max = h*f - W0
   - Isigin siddeti arttikca kopartilan elektron sayisi artar, enerjisi degismez
   - Isigin frekansi arttikca elektronlarin kinetik enerjisi artar

3. COMPTON SACILMASI:
   - Foton ile elektronun carpismasiyla fotonun dalga boyu uzar
   - Isigin tanecik dogasinin kaniti
   - delta_lambda = (h/(m_e*c))*(1 - cos(teta))

4. DE BROGLIE HIPOTEZI:
   - Madde de dalga ozelligi gosterir
   - lambda = h/(m*v) (de Broglie dalga boyu)
   - Elektronlarin dalga ozelligi Davisson-Germer deneyiyle dogrulandi
   - Buyuk kutleli cisimlerin dalga boyu ihmal edilecek kadar kucuktur

5. ATOM MODELLERI:
   - Dalton: Bolunmez kure modeli
   - Thomson: Uzumlu kek modeli (pozitif hamur icinde negatif yukler)
   - Rutherford: Cekirdekli atom modeli (alfa sacilma deneyi)
   - Bohr: Kararli yorungeler, enerji seviyeleri, kuantum sartlari
   - Modern (kuantum mekaniksel): Orbital kavrami, olasilik yogunlugu
"""
},

}

def get_fizik11_reference(topic: str) -> list:
    """Verilen konuya en yakin fizik 11 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in FIZIK_11_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_fizik11_keys() -> list:
    """Tum fizik 11 referans anahtarlarini dondurur."""
    return list(FIZIK_11_REFERANS.keys())
