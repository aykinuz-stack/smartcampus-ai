# -*- coding: utf-8 -*-
"""
11. Sinif Kimya dersi
MEB 2025 mufredatina uygun DOGRU referans verileri.

Uniteler:
1. Modern Atom Teorisi
2. Gazlar
3. Sivi Cozeltiler
4. Kimyasal Tepkimelerde Enerji
5. Tepkime Hizlari
6. Kimyasal Denge
"""

KIMYA_11_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. UNITE: MODERN ATOM TEORISI
# ═══════════════════════════════════════════════════════════════

"KIM.11.1.ATOM_MODELLERI": {
    "unite": "Modern Atom Teorisi",
    "baslik": "Atom Modelleri ve Kuantum Sayilari",
    "icerik": """
MODERN ATOM TEORISI:

1. BOHR ATOM MODELI:
   - Elektronlar cekirdek etrafinda belirli enerji duzeylerinde (yorunge) bulunur
   - Enerji seviyeleri: n = 1, 2, 3, ... (K, L, M, ... katmanlari)
   - Elektron enerji absorplayarak ust duzeye cikar (uyarma/eksitasyon)
   - Enerji yayarak alt duzeye iner (emisyon/isinim)
   - Cizgi spektrumu aciklar ancak cok elektronlu atomlarda yetersiz kalir

2. KUANTUM MEKANIKSEL MODEL:
   - Heisenberg Belirsizlik Ilkesi: Elektronun yeri ve momentumu ayni anda kesinlikle belirlenemez
   - Orbital: Elektronun bulunma olasiliginin yuksek oldugu bolge
   - Dalga fonksiyonu (psi): Elektronun uzaydaki davranisini tanimlar
   - |psi|^2: Olasilik yogunlugu (elektron bulutu)

3. KUANTUM SAYILARI:
   - Bas kuantum sayisi (n): 1, 2, 3, ... (enerji duzeyi, kabuk)
   - Acisal momentum kuantum sayisi (l): 0, 1, ..., n-1 (alt kabuk sekli)
     -> l=0: s (kuresel), l=1: p (dambil), l=2: d (yonca), l=3: f
   - Manyetik kuantum sayisi (ml): -l, ..., 0, ..., +l (orbitalin yonelimi)
   - Spin kuantum sayisi (ms): +1/2 veya -1/2

4. ORBITAL TURLERI VE KAPASITELERI:
   - s orbitali: 1 orbital, max 2 elektron
   - p orbitali: 3 orbital, max 6 elektron
   - d orbitali: 5 orbital, max 10 elektron
   - f orbitali: 7 orbital, max 14 elektron
   - n. katmandaki toplam elektron: 2n^2

5. ELEKTRON DIZILIMI KURALLARI:
   - Aufbau (Yapma) Ilkesi: Dusuk enerjili orbitalden baslanir (1s, 2s, 2p, 3s, 3p, 4s, 3d...)
   - Pauli Disarilik Ilkesi: Bir orbitalde en fazla 2 elektron (zit spinli)
   - Hund Kurali: Esdegerlik orbitalleri once teker teker, ayni spinle doldurulur
   - Ozel durumlar: Cr [Ar]3d5 4s1, Cu [Ar]3d10 4s1 (yarim ve tam dolu kararlilik)
"""
},

"KIM.11.1.PERIYODIK_OZELLIKLER": {
    "unite": "Modern Atom Teorisi",
    "baslik": "Periyodik Ozellikler ve Elektron Dizilimi",
    "icerik": """
PERIYODIK OZELLIKLER:

1. ATOM YARICAPI:
   - Periyotta soldan saga azalir (artan cekirdek yuku elektronlari daha cok ceker)
   - Grupta yukaridan asagiya artar (yeni katman eklenir)
   - Katyon < Notr atom < Anyon (elektron kaybetmek kucultur, kazanmak buyutur)

2. IYONLASMA ENERJISI (IE):
   - Gaz halindeki atomdan elektron kopartmak icin gereken minimum enerji
   - Periyotta soldan saga artar (atom kuculdukce elektron daha siki tutulur)
   - Grupta yukaridan asagiya azalir
   - 1. IE < 2. IE < 3. IE (ardisik iyonlasma enerjileri artar)
   - Soygazlarin IE degerleri en yuksektir

3. ELEKTRON ILGISI:
   - Gaz halindeki notr atomun elektron yakalama egilimi
   - Periyotta soldan saga genel olarak artar (halojenler en yuksek)
   - Grupta yukaridan asagiya genel olarak azalir
   - Soygazlar ve 2. grup elementlerinin elektron ilgisi dusuktur

4. ELEKTRONEGATIFLIK:
   - Atomun bagdaki elektron ciftini kendine cekme egilimi
   - Pauling olcegine gore: F (4,0) en yuksek
   - Periyotta soldan saga artar, grupta yukaridan asagiya azalir
   - Soygazlara elektronegatiflik degeri tanimlanmaz
   - Metal-ametal siniri: elektronegatiflik farki bag turunu belirler

5. METALIK KARAKTER:
   - Elektron verme egilimi (dusuk IE, dusuk elektronegatiflik)
   - Periyotta soldan saga azalir
   - Grupta yukaridan asagiya artar
   - En metalik: Fr (fransiyum), En ametalik: F (flor)
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. UNITE: GAZLAR
# ═══════════════════════════════════════════════════════════════

"KIM.11.2.GAZ_YASALARI": {
    "unite": "Gazlar",
    "baslik": "Gaz Yasalari ve Ideal Gaz",
    "icerik": """
GAZ YASALARI:

1. IDEAL GAZ OZELLIKLERI:
   - Gaz molekulleri hacimsizdır (noktasal)
   - Molekuller arasi etkilesim yoktur (cekim/itme kuvveti yok)
   - Carpismalari tam esnektir (enerji kaybi yok)
   - Gercek gazlar dusuk basinc ve yuksek sicaklikta ideale yaklasir
   - He en ideal gaza yakin davranir (kucuk, apolar)

2. BOYLE-MARIOTTE YASASI (Sabit T):
   - P1*V1 = P2*V2 (sicaklik sabitken basinc ve hacim ters orantili)
   - P-V grafigi: Hiperbol (izotermler)
   - Hacim artinca basinc azalir (ve tersi)

3. CHARLES YASASI (Sabit P):
   - V1/T1 = V2/T2 (basinc sabitken hacim ve sicaklik dogru orantili)
   - Sicaklik mutlak (Kelvin) olmalidir: T(K) = T(C) + 273
   - -273C (0 K): Mutlak sifir, teorik olarak hacim sifir olur

4. GAY-LUSSAC YASASI (Sabit V):
   - P1/T1 = P2/T2 (hacim sabitken basinc ve sicaklik dogru orantili)
   - Sicaklik artinca basinc artar

5. IDEAL GAZ DENKLEMI:
   - P*V = n*R*T
   - P: Basinc (atm), V: Hacim (L), n: Mol sayisi, T: Sicaklik (K)
   - R = 0,082 L*atm/(mol*K) (ideal gaz sabiti)
   - Normal kosullar (NK): 0C, 1 atm -> 1 mol gaz 22,4 L hacim kaplar

6. DALTON KISMI BASINC YASASI:
   - P_toplam = P1 + P2 + P3 + ... (toplam basinc = kismi basinclarin toplami)
   - Pi = xi * P_toplam (xi: mol kesri)
   - Su uzerinde toplanan gazlarda: P_toplam = P_gaz + P_su_buhari

7. GRAHAM DIFUZYON YASASI:
   - v1/v2 = karekök(M2/M1) (difuzyon hizi mol kutlesiyle ters orantili)
   - Hafif molekuller daha hizli yayilir (H2 en hizli)
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. UNITE: SIVI COZELTILER
# ═══════════════════════════════════════════════════════════════

"KIM.11.3.COZELTILER": {
    "unite": "Sivi Cozeltiler",
    "baslik": "Cozeltiler ve Derisiklik Birimleri",
    "icerik": """
COZELTILER VE DERISIKLIK BIRIMLERI:

1. COZELTI TANIMLARI:
   - Cozelti: Cozucu + cozunen homojen karisim
   - Cozucu: Fazla olan bilesen (genellikle su)
   - Cozunen: Az olan bilesen
   - Doymus cozelti: Belirli sicaklikta cozunebilecek max miktar cozulmus
   - Doymamis/Asiri doymus cozelti kavramlari

2. COZUNURLUK:
   - 100 g (veya 100 mL) cozucude cozunebilen max cozunen miktari
   - Sicaklik etkisi: Katilarin cogunun cozunurlugu sicaklikla artar
   - Gazlarin cozunurlugu sicaklikla azalir, basincla artar
   - Benzer benzeri cozer kurali (polar-polar, apolar-apolar)

3. DERISIKLIK BIRIMLERI:
   - Molarite (M): M = n/V (mol/litre)
   - Molalite (m): m = n/W_cozucu(kg)
   - Kutle yuzde: %m = (m_cozunen/m_cozelti) x 100
   - Hacim yuzde: %V = (V_cozunen/V_cozelti) x 100
   - ppm: mg/L veya mg/kg (milyonda bir)
   - Mol kesri: xi = ni / n_toplam

4. SEYRELTME:
   - M1*V1 = M2*V2 (mol sayisi korunur)
   - Su ekleme ile derisiklik azalir
   - Mol sayisi degismez, hacim artar

5. KOLIGATIF OZELLIKLER:
   - Cozunen tanecik sayisina bagli, cinsine bagli degil
   - Buhar basinci dususu: dP = x_cozunen * P_cozucu (Raoult Yasasi)
   - Kaynama noktasi yukselmesi: dTk = Kb * m * i
   - Donma noktasi dususu: dTd = Kd * m * i
   - Osmotik basinc: pi = M*R*T*i
   - i: van't Hoff faktoru (elektrolitler icin > 1)
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. UNITE: KIMYASAL TEPKIMELERDE ENERJI
# ═══════════════════════════════════════════════════════════════

"KIM.11.4.TERMOKIMYA": {
    "unite": "Kimyasal Tepkimelerde Enerji",
    "baslik": "Termokimya ve Entalpi",
    "icerik": """
TERMOKIMYA VE ENTALPI:

1. TEMEL KAVRAMLAR:
   - Sistem: Incelenen bolge; Cevre: Sistemin disindaki hersey
   - Acik/Kapali/Yalitilmis sistem turleri
   - Isi (q): Sicaklik farkiyla transfer olan enerji
   - Is (w): Mekanik enerji transferi
   - Ic enerji degisimi: dU = q + w (Termodinamigin 1. yasasi)

2. ENTALPI (H):
   - dH = q_p (sabit basincta isi degisimi = entalpi degisimi)
   - dH < 0: Ekzotermik (isi aciga cikar)
   - dH > 0: Endotermik (isi absorplanir)
   - Olusum entalpisi (dHf): Elementlerden 1 mol bilesik olusma entalpisi
   - Elementlerin standart olusum entalpisi = 0

3. HESS YASASI:
   - Bir tepkimenin entalpi degisimi, tepkimenin yolu ne olursa olsun aynidir
   - dH_toplam = dH1 + dH2 + dH3 + ...
   - Tepkimeler toplanabilir, cikarilabilir, katsayiyla carpilabilir
   - dH_tepkime = toplam(dHf urunler) - toplam(dHf girenler)

4. BAG ENERJISI:
   - Gaz halindeki bir molu kovalent bagi homolitik kirmak icin gereken enerji
   - Bag kirma: Endotermik (enerji gerektirir, +)
   - Bag olusma: Ekzotermik (enerji acigar, -)
   - dH = toplam(kirilan bag enerjileri) - toplam(olusan bag enerjileri)

5. KALORIMETRI:
   - q = m*c*dT (isi = kutle x ozel isi x sicaklik degisimi)
   - Suyun ozel isisi: c = 4,18 J/(g*C)
   - Kalorimetre: Tepkimenin isi etkisini olcen alet
   - q_sistem = -q_cevre (isi korunumu)

6. KENDILIGINDENLIK:
   - Entropi (S): Duzensizlik olcusu, dS > 0 duzensizlik artar
   - Gibbs serbest enerjisi: dG = dH - T*dS
   - dG < 0: Kendiliginden gerceklesir
   - dG > 0: Kendiliginden gerceklesmez
   - dG = 0: Denge durumu
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. UNITE: TEPKIME HIZLARI
# ═══════════════════════════════════════════════════════════════

"KIM.11.5.TEPKIME_HIZI": {
    "unite": "Tepkime Hizlari",
    "baslik": "Kimyasal Tepkime Hizlari ve Etkileyen Faktorler",
    "icerik": """
KIMYASAL TEPKIME HIZLARI:

1. TEPKIME HIZI TANIMI:
   - Birim zamandaki derisiklik degisimi
   - Hiz = -d[Giren]/dt = +d[Urun]/dt
   - Birimi: mol/(L*s) veya M/s
   - Ortalama hiz ve anlik hiz ayrimi
   - Anlik hiz: Derisiklik-zaman grafiğindeki teğetin eğimi

2. HIZ IFADESI (HIZ DENKLEMI):
   - aA + bB -> urunler icin: Hiz = k*[A]^m*[B]^n
   - k: Hiz sabiti (sicakliga baglidir)
   - m, n: Tepkime dereceleri (deneysel olarak bulunur, katsayilara esit olmak zorunda degil)
   - Toplam derece = m + n

3. AKTIVASYON ENERJISI:
   - Tepkimenin baslamasi icin gereken minimum enerji (Ea)
   - Aktiflesme kompleksi (gecis durumu): En yuksek enerjili ara durum
   - Ea buyukse tepkime yavas, kucukse hizlidir
   - Tepkime koordinat diyagraminda tepe noktasi

4. ETKILEYEN FAKTORLER:
   - Derisiklik: Artarsa hiz artar (daha sik carpismalar)
   - Sicaklik: Artarsa hiz artar (her 10C icin yaklasik 2-3 kat)
   - Temas yuzeyi: Artarsa hiz artar (toz haline getirmek)
   - Katalizor: Aktivasyon enerjisini dusurerek hizi artirir
   - Maddenin cinsi: Bag yapisi ve kuvvetine baglidir

5. KATALIZOR:
   - Aktivasyon enerjisini dusurup tepkimeyi hizlandirir
   - Tepkimede harcanmaz, tepkime sonunda geri kazanilir
   - Dengeyi etkilemez (ileri ve geri tepkimeyi esit olarak hizlandirir)
   - Homojen katalizor: Tepkenlerle ayni fazda
   - Heterojen katalizor: Farkli fazda (genellikle kati yuzey)
   - Enzimler: Biyolojik katalizorler (yuksek secicilik)
"""
},

# ═══════════════════════════════════════════════════════════════
# 6. UNITE: KIMYASAL DENGE
# ═══════════════════════════════════════════════════════════════

"KIM.11.6.KIMYASAL_DENGE": {
    "unite": "Kimyasal Denge",
    "baslik": "Kimyasal Denge ve Le Chatelier Ilkesi",
    "icerik": """
KIMYASAL DENGE:

1. DENGE KAVRAMI:
   - Tersinir tepkimelerde ileri ve geri tepkime hizlari esitlenmistir
   - Dinamik denge: Makroskopik ozellikler sabit, mikroskopik olaylar devam eder
   - Denge sabiti (Kc veya Kp) sicakliga baglidir
   - Kapali sistemde olusur

2. DENGE SABITI IFADESI:
   - aA + bB <=> cC + dD icin: Kc = [C]^c*[D]^d / ([A]^a*[B]^b)
   - Saf katilar ve saf sivilar denge ifadesine yazilmaz
   - Kc >> 1: Denge urunler tarafinda (tepkime tamamlanmaya yakin)
   - Kc << 1: Denge girenler tarafinda
   - Kp = Kc*(RT)^dn (dn = urun gaz mol - giren gaz mol)

3. LE CHATELIER ILKESI:
   - Dengedeki sisteme yapilan mudahale, sistemi mudahaleyi azaltacak yone kaydirir

   a) DERISIKLIK DEGISIMI:
   - Giren ekleme -> Denge urune kayar
   - Urun ekleme -> Denge girene kayar
   - Giren uzaklastirma -> Denge girene kayar

   b) BASINC/HACIM DEGISIMI (gaz tepkimeleri):
   - Basinc artisi (hacim azalmasi) -> Denge mol sayisi az olan tarafa kayar
   - Basinc azalmasi -> Denge mol sayisi cok olan tarafa kayar
   - Iki tarafta gaz mol sayisi esitse basinc degisimi dengeyi etkilemez

   c) SICAKLIK DEGISIMI:
   - Sicaklik artisi: Endotermik yone kayar (dH > 0 tarafa)
   - Sicaklik azalmasi: Ekzotermik yone kayar
   - Sicaklik, Kc degerini degistiren TEK faktordur

4. TEPKIME ORANI (Q):
   - Q < Kc: Tepkime ileri yonde gider (urun olusur)
   - Q = Kc: Sistem dengede
   - Q > Kc: Tepkime geri yonde gider (giren olusur)

5. KATALIZOR VE DENGE:
   - Katalizor dengeye ulasma suresini kisaltir
   - Denge konumunu (Kc) degistirmez
   - Hem ileri hem geri tepkimeyi esit oranda hizlandirir
"""
},

}

def get_kimya11_reference(topic: str) -> list:
    """Verilen konuya en yakin kimya 11 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in KIMYA_11_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_kimya11_keys() -> list:
    """Tum kimya 11 referans anahtarlarini dondurur."""
    return list(KIMYA_11_REFERANS.keys())
