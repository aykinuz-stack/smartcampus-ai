# -*- coding: utf-8 -*-
"""
12. Sinif Fizik dersi - MEB 2025 mufredatina uygun referans verileri.
Ogrenme alanlari:
1. Cembersel Hareket
2. Basit Harmonik Hareket
3. Dalga Mekanigi
4. Atom Fizigi ve Radyoaktivite
5. Modern Fizik
"""

FIZIK_12_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. OGRENME ALANI: CEMBERSEL HAREKET
# ═══════════════════════════════════════════════════════════════

"FIZ.12.1.DUZGUN_CEMBERSEL": {
    "unite": "Çembersel Hareket",
    "baslik": "Düzgün Çembersel Hareket",
    "icerik": """DUZGUN CEMBERSEL HAREKET:

1. TANIM:
   - Bir cismin sabit hizla daire yolu uzerinde hareket etmesidir.
   - Surat sabittir ancak yon surekli degistigi icin hiz degisir.
   - Dolayisiyla ivme sifir degildir (merkepe yoneliktir).

2. ACISAL BUYUKLUKLER:
   - Acisal yer degistirme (θ): Radyan (rad) birimiyle olculur.
   - Acisal hiz (ω): ω = Δθ/Δt = 2π/T = 2πf (rad/s).
   - Periyot (T): Bir tam turun suresi (s).
   - Frekans (f): Birim zamandaki tur sayisi, f = 1/T (Hz).

3. CIZGISEL-ACISAL ILISKI:
   - v = ω·r (cizgisel hiz = acisal hiz × yaricap).
   - Yay uzunlugu: s = θ·r.
   - Ayni ω ile donen cisimlerde, r buyudukce v artar.

4. MERKEZCIL IVME VE KUVVET:
   - Merkezcil ivme: aₘ = v²/r = ω²·r (merkeze yonelik).
   - Merkezcil kuvvet: F = m·v²/r = m·ω²·r.
   - Bu kuvvet hareketin nedenidir, bagimsiz bir kuvvet degildir.
   - Iplikteki gerilme, yercekimi, surtunsme gibi kuvvetler merkezcil kuvvet gorevini ustlenebilir.

5. DUZLEMDE CEMBERSEL HAREKET ORNEKLERI:
   - Yatay duzlemde donen cisim: T·sinθ = mv²/r.
   - Virajda arac: Surtunsme kuvveti = mv²/r.
   - Banker viraj: tanθ = v²/(r·g).

6. DUSEY DUZLEMDE CEMBERSEL HAREKET:
   - En ust nokta: T + mg = mv²/r → T_min = 0 icin v_min = √(g·r).
   - En alt nokta: T - mg = mv²/r → T en buyuk.
   - Enerji korunumu ile hiz hesaplanir.
"""
},

"FIZ.12.1.ACISAL_MOMENTUM": {
    "unite": "Çembersel Hareket",
    "baslik": "Acisal Momentum ve Dolanma",
    "icerik": """ACISAL MOMENTUM:

1. TORK (DONAME MOMENTI):
   - τ = r × F = r·F·sinθ (Nm biriminde).
   - Cismi dondurmeye calisan kuvvetin etkisi.
   - Kuvvet kolu (r): Kuvvet dogrusu ile donme ekseni arasi dik uzaklik.

2. ACISAL MOMENTUM:
   - L = I·ω (nokta kutle icin L = m·v·r).
   - I: Eylemsizlik momenti (kg·m²).
   - Eylemsizlik momenti kutle dagilimine baglidir.
   - Disk: I = ½mr², Cember: I = mr², Cubuk (merkezden): I = (1/12)mL².

3. ACISAL MOMENTUMUN KORUNUMU:
   - Dis tork sifir ise acisal momentum korunur: L₁ = L₂.
   - I₁·ω₁ = I₂·ω₂.
   - Buz patinajcisi kollarini toplar → I azalir → ω artar.
   - Donen sandalye deneyi.

4. KEPLER KANUNLARI:
   - I. Kanun: Gezegenler Gunes etrafinda eliptik yorungede doner.
   - II. Kanun: Gezegen-Gunes dogrusu esit zamanlarda esit alan tarar (acisal momentum korunumu).
   - III. Kanun: T² ∝ r³ (T²/r³ = sabit).

5. UYGULAMALAR:
   - Uydu hareketi: mg = mv²/r → v = √(g·R²/r).
   - Jeostasyoner uydu: T = 24 saat, r ≈ 42.000 km.
   - Karadelik yakininda madde diskinin hizlanmasi.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. OGRENME ALANI: BASIT HARMONIK HAREKET
# ═══════════════════════════════════════════════════════════════

"FIZ.12.2.BHH_TANIM": {
    "unite": "Basit Harmonik Hareket",
    "baslik": "Basit Harmonik Hareket (BHH)",
    "icerik": """BASIT HARMONIK HAREKET:

1. TANIM:
   - Denge noktasindan yer degistirme ile orantili ve denge noktasina yonelik
     geri cagirici kuvvetin etkisindeki periyodik harekettir.
   - F = -k·x (Hooke Yasasi).
   - a = -(k/m)·x = -ω²·x.

2. HAREKET DENKLEMLERI:
   - x(t) = A·cos(ωt + φ) (konum).
   - v(t) = -A·ω·sin(ωt + φ) (hiz).
   - a(t) = -A·ω²·cos(ωt + φ) = -ω²·x (ivme).
   - A: Genlik (maks yer degistirme).
   - ω = 2π/T = 2πf: Acisal frekans.
   - φ: Baslangic faz acisi.

3. PERIYOT:
   - Yay-kutle sistemi: T = 2π√(m/k).
   - Basit sarkaç: T = 2π√(L/g).
   - Periyot genlige bagimli degildir (kucuk acilarda).
   - Sarkaçta: Periyot kutle ve genlikten bagimsiz, ip uzunlugu ve g'ye bagli.

4. ENERJI:
   - Kinetik enerji: Eₖ = ½mv² = ½k(A² - x²).
   - Potansiyel enerji: Eₚ = ½kx².
   - Toplam enerji: E = ½kA² (sabit, korunur).
   - Denge noktasinda: Eₖ max, Eₚ = 0.
   - Uc noktalarda: Eₖ = 0, Eₚ max.

5. HIZ-KONUM ILISKISI:
   - v = ω√(A² - x²).
   - Maks hiz: v_max = ωA (x = 0'da).
   - Maks ivme: a_max = ω²A (x = ±A'da).

6. GRAFIK YORUMU:
   - x-t grafigi: Kosinüs egrisi.
   - v-t grafigi: -Sinüs egrisi (x'in turevidir).
   - a-t grafigi: -Kosinüs egrisi (v'nin turevidir).
   - Enerji-x grafigi: Parabol seklindedir.
"""
},

"FIZ.12.2.BHH_ORNEKLER": {
    "unite": "Basit Harmonik Hareket",
    "baslik": "BHH Uygulamalari ve Sönümlü Titresimler",
    "icerik": """BHH UYGULAMALARI:

1. YAY-KUTLE SISTEMI:
   - Yatay yay: T = 2π√(m/k), denge noktasi dogal boyda.
   - Dusey yay: T = 2π√(m/k), denge noktasi mg/k kadar uzamis halde.
   - Seri bagli yaylar: 1/k_es = 1/k₁ + 1/k₂.
   - Paralel bagli yaylar: k_es = k₁ + k₂.

2. BASIT SARKAC:
   - T = 2π√(L/g) (kucuk acilar icin, θ < 10°).
   - g bilinmeyen ortamda sarkac ile g olculebilir: g = 4π²L/T².
   - Asansorde: Yukari ivmelenen → T azalir, asagi ivmelenen → T artar.

3. FIZIKSEL SARKAC:
   - T = 2π√(I/(m·g·d)).
   - I: Donme ekseni etrafindaki eylemsizlik momenti.
   - d: Kutle merkezi ile donme ekseni arasi uzaklik.

4. SONUMLU TITRESIM:
   - Surtunsme/direnç nedeniyle genlik zamanla azalir.
   - x(t) = A·e^(-γt)·cos(ω't + φ).
   - Kritik sonumlu: En hizli sekilde dengeye doner (amortisör).
   - Asiri sonumlu: Yavasca dengeye doner, titresim yok.

5. ZORLANMIS TITRESIM VE REZONANS:
   - Disaridan periyodik kuvvet uygulanirsa zorlanmis titresim olusur.
   - Zorlama frekansi = dogal frekans ise REZONANS olusur.
   - Rezonansta genlik maksimum olur.
   - Ornek: Kopru titresimi, bardak kirma (ses frekansi), radyo ayarlama.

6. GUNLUK HAYAT UYGULAMALARI:
   - Sismograf: Deprem dalgalarini olcer (BHH prensibi).
   - Saat sarkaçlari: Periyodun genlikten bagimsizligi.
   - Arac suspansiyonu: Sonumlu titresim.
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. OGRENME ALANI: DALGA MEKANIGI
# ═══════════════════════════════════════════════════════════════

"FIZ.12.3.DALGA_TEMEL": {
    "unite": "Dalga Mekaniği",
    "baslik": "Dalga Temelleri",
    "icerik": """DALGA MEKANIGI:

1. DALGA TANIMI:
   - Enerji ve momentumun ortam icerisinde tasinmasidir.
   - Madde tasinmaz, enerji tasinir.
   - Dalga kaynagi: Titresim yapan cisim.

2. DALGA TURLERI:
   - Enine dalga: Titresim yonu yayilma yonune dik (isik, ip dalgasi).
   - Boyuna dalga: Titresim yonu yayilma yonu ile ayni (ses dalgasi).
   - Su dalgasi: Hem enine hem boyuna bilesenleri vardir.

3. DALGA BUYUKLUKLERI:
   - Dalga boyu (λ): Iki ardisik tepeden tepeye mesafe.
   - Frekans (f): Birim zamandaki dalga sayisi (Hz).
   - Periyot (T): Bir tam dalganin suresi, T = 1/f.
   - Genlik (A): Maksimum yer degistirme.
   - Dalga hizi: v = λ·f = λ/T.

4. DALGA DAVRANISLARI:
   - Yansima: Dalganin bir yuzeyden geri donmesi. Gelis acisi = yansima acisi.
   - Kirilma: Ortam degisince dalganin yon degistirmesi. Snell Yasasi: n₁sinθ₁ = n₂sinθ₂.
   - Kirinım (Difraksiyon): Dalganin engelin arkasina dolmasi. λ ≈ engel boyutu ise belirgin.
   - Girisim (Interferans): Iki dalganin ustuste binmesi.
     * Yapici girisim: Tepeler cakisir → genlik artar.
     * Yikici girisim: Tepe + cukur → genlik azalir/sifir olur.

5. DALGALARDA SUPERPOZISYON:
   - Iki dalga ayni noktada karsilastiginda yer degistirmeler toplanir.
   - Yasam prensibi: Dalgalar birbirinden etkilenmeden yoluna devam eder.

6. DURAN DALGA:
   - Gelen ve yansıyan dalganin ust uste binmesiyle olusur.
   - Dugum noktalari: Yer degistirme surekli sifir.
   - Karin noktalari: Yer degistirme maksimum.
   - Telli calgilar ve boru organlar duran dalga prensibi ile calisir.
"""
},

"FIZ.12.3.SES_ISIK": {
    "unite": "Dalga Mekaniği",
    "baslik": "Ses ve Isik Dalgalari",
    "icerik": """SES VE ISIK DALGALARI:

1. SES DALGASI:
   - Boyuna mekanik dalga, ortam gerektirir (boslukta yayilmaz).
   - Havada: ~340 m/s (20°C'de), sicaklikla artar.
   - Suda: ~1500 m/s, Celikte: ~5000 m/s.
   - Duyulabilir aralik: 20 Hz - 20.000 Hz.
   - Infrasound: < 20 Hz, Ultrasound: > 20.000 Hz.

2. SES OZELLIKLERI:
   - Siddet (sesin gurlugu): Genlik ile ilgili, desibel (dB) birimiyle olculur.
   - Perde (sesin inceligi/kalinligi): Frekans ile ilgili, yuksek frekans = ince ses.
   - Tini (ses rengi): Harmoniklerle ilgili, ayni nota farkli calgida farkli duyulur.

3. DOPPLER ETKISI:
   - Kaynak ve gozlemci birbirine yaklasirsa → frekans artar (daha ince ses).
   - Birbirinden uzaklasirsa → frekans azalir (daha kalin ses).
   - f' = f · (v ± v_gozlemci)/(v ∓ v_kaynak).
   - Ornek: Ambulans sireni, yildizlarin kirmiziya kayma.

4. ISIK:
   - Elektromanyetik dalga, ortam gerektirmez (boslukta yayilir).
   - c = 3 × 10⁸ m/s (boslukta).
   - Gorunur spektrum: 400 nm (mor) - 700 nm (kirmizi).
   - E = hf = hc/λ (foton enerjisi).

5. ELEKTROMANYETIK SPEKTRUM:
   - Radyo dalgalari > Mikrodalgalar > Kizilotesi > Gorunur isik >
     Morotesi > X-isinlari > Gama isinlari.
   - Frekans artinca enerji artar, dalga boyu kisalir.

6. ISIGIN DALGA DAVRANISLARI:
   - Girisim: Young deneyi, ince film girisimleri.
   - Kirinım: Tek yarik, cift yarik kirinım desenleri.
   - Polarizasyon: Enine dalga ozelligi, isik polarize edilebilir.
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. OGRENME ALANI: ATOM FIZIGI VE RADYOAKTIVITE
# ═══════════════════════════════════════════════════════════════

"FIZ.12.4.ATOM_MODELLERI": {
    "unite": "Atom Fiziği ve Radyoaktivite",
    "baslik": "Atom Modelleri ve Kuantum",
    "icerik": """ATOM MODELLERI:

1. TARIHSEL GELISIM:
   - Dalton (1803): Atom bolunemeyen en kucuk parca.
   - Thomson (1897): Uzumlu pudding modeli, elektron kesfedildi.
   - Rutherford (1911): Cekirdekli atom modeli, alfa sacilma deneyi.
   - Bohr (1913): Kuantumlu yorunge modeli, enerji seviyeleri.
   - Modern kuantum modeli: Olasilik bulutu, dalga fonksiyonu.

2. BOHR ATOM MODELI:
   - Elektronlar belirli enerji seviyelerinde (yorungelerde) bulunur.
   - Enerji seviyeleri: Eₙ = -13.6/n² eV (Hidrojen icin).
   - Elektron yorunge degistirirken foton yayar veya soger.
   - ΔE = E_ust - E_alt = hf (yayilan/sogurulan foton enerjisi).
   - Temel hal (n=1): En dusuk enerji seviyesi.
   - Uyarilmis hal (n>1): Daha yuksek enerji seviyeleri.

3. FOTON VE ENERJI SEVIYELERI:
   - Foton enerjisi: E = hf = hc/λ.
   - Planck sabiti: h = 6.63 × 10⁻³⁴ J·s.
   - Cizgi spektrumu: Her element kendine ozgu dalga boylarinda isik yayar.
   - Lyman serisi (morotesi): n → 1.
   - Balmer serisi (gorunur): n → 2.
   - Paschen serisi (kizilotesi): n → 3.

4. FOTOELEKTRIK ETKI:
   - Isik metal yuzeyine dusunce elektron koparilmasi.
   - E_foton = W (is fonksiyonu) + Eₖ (kinetik enerji).
   - Esik frekansi: f₀ = W/h, altinda elektron cikmaz.
   - Isik siddeti artinca elektron sayisi artar ama kinetik enerji artmaz.
   - Einstein aciklamasi: Isik fotonlardan olusur (parcacik dogasi).

5. DALGA-PARCACIK IKILILIGI:
   - de Broglie hipotezi: λ = h/(m·v) (madde dalgasi).
   - Elektron kirinım deneyi: Elektronlar dalga gibi davranir.
   - Heisenberg Belirsizlik Ilkesi: Δx·Δp ≥ h/(4π).
"""
},

"FIZ.12.4.RADYOAKTIVITE": {
    "unite": "Atom Fiziği ve Radyoaktivite",
    "baslik": "Radyoaktivite ve Cekirdek Fizigi",
    "icerik": """RADYOAKTIVITE:

1. CEKIRDEK YAPISI:
   - Proton (p): +1 yuklu, kutle ≈ 1.67 × 10⁻²⁷ kg.
   - Notron (n): Yuksuz, kutle ≈ proton kutlesi.
   - Kutle numarasi (A) = proton sayisi (Z) + notron sayisi (N).
   - Izotop: Ayni Z, farkli N (ornek: C-12, C-14).

2. RADYOAKTIF BOZUNMA TURLERI:
   - Alfa (α) bozunmasi: ⁴₂He cikar, A 4 azalir, Z 2 azalir.
   - Beta⁻ (β⁻) bozunmasi: Notron → proton + elektron + anti-notrino, Z 1 artar.
   - Beta⁺ (β⁺) bozunmasi: Proton → notron + pozitron + notrino, Z 1 azalir.
   - Gama (γ) isinlari: Cekirdek uyarilmis halden temel hale gecer, A ve Z degismez.

3. YARI OMUR:
   - Radyoaktif maddenin yarisinin bozunmasi icin gecen sure.
   - N(t) = N₀ · (1/2)^(t/T½).
   - Her yari omurde madde miktari yariya iner.
   - C-14: T½ ≈ 5730 yil (arkeolojik yaslama).
   - U-238: T½ ≈ 4.5 milyar yil (jeolojik yaslama).

4. CEKIRDEK TEPKIMELERI:
   - Fisyon (bolunsme): Agir cekirdek ikiye bolunur, enerji acigar.
     * U-235 + n → Ba-141 + Kr-92 + 3n + enerji.
     * Zincirleme reaksiyon: Kritik kutle gerekli.
     * Nukleer santral ve atom bombasi.
   - Fuzyon (birlesme): Hafif cekirdekler birlesir, enerji acigar.
     * H-2 + H-3 → He-4 + n + enerji.
     * Gunes enerjisinin kaynagi.
     * Cok yuksek sicaklik gerekli (~10⁷ K).

5. KUTLE-ENERJI ESDEGERLIGI:
   - E = mc² (Einstein).
   - Kutle acigi (Δm): Serbest nukleonlarin kutlesi − cekirdek kutlesi.
   - Baglama enerjisi: E_b = Δm · c².
   - Nukleon basina baglama enerjisi: Fe-56 en kararli cekirdek.

6. RADYASYONDAN KORUNMA:
   - Alfa: Kagit durdurabilir, dis isinim tehlikesi dusuk.
   - Beta: Aluminyum levha durdurur.
   - Gama: Kalin kursun veya beton gerekli.
   - ALARA prensibi: Mumkun oldugunca dusuk doz.
"""
},

# ═══════════════════════════════════════════════════════════════
# 5. OGRENME ALANI: MODERN FIZIK
# ═══════════════════════════════════════════════════════════════

"FIZ.12.5.OZEL_GORELILIK": {
    "unite": "Modern Fizik",
    "baslik": "Ozel Gorelilik Teorisi",
    "icerik": """OZEL GORELILIK:

1. EINSTEIN'IN POSTULATLARI:
   - I. Postulat: Fizik kanunlari tum eylemsiz referans cercevelerinde aynidir.
   - II. Postulat: Isigin boslukta hizi tum gozlemciler icin c = 3×10⁸ m/s'dir
     (kaynağin veya gozlemcinin hizindan bagimsiz).

2. ZAMAN GENLEMESI:
   - Hareket eden saatler daha yavas isler.
   - Δt = Δt₀ / √(1 - v²/c²) = γ·Δt₀.
   - γ = 1/√(1 - v²/c²): Lorentz faktoru (γ ≥ 1).
   - v << c ise γ ≈ 1 (klasik limit).
   - v → c ise γ → ∞ (zaman cok yavaslar).

3. UZUNLUK KISALMASI:
   - Hareket eden cisimler hareket yonunde kisalir.
   - L = L₀ · √(1 - v²/c²) = L₀/γ.
   - L₀: Durgun uzunluk (cisimle birlikte hareket eden gozlemciye gore).
   - Sadece hareket yonunde kisalma olur, dik yonlerde degisiklik yok.

4. KUTLE-ENERJI ESDEGERLIGI:
   - E = mc² (durgun kutle enerjisi).
   - Toplam enerji: E = γmc².
   - Kinetik enerji: Eₖ = (γ - 1)mc².
   - Momentum: p = γmv.
   - E² = (pc)² + (mc²)².

5. SONUCLAR VE UYGULAMALAR:
   - Kutleli hicbir cisim isik hizina erisamez (sonsuz enerji gerekir).
   - GPS uydu duzeltmeleri: Gorelilik etkileri hesaplanmazsa konum hatasi olusur.
   - Parcacik hizlandiricilari: Parcaciklar c'ye yakin hizlarda kinetik enerji artar.
   - Muon omru: Kozmik isinlardan gelen muonlar, zaman genlemesi sayesinde
     yeryuzune ulasir (yoksa bozunurlardi).
"""
},

"FIZ.12.5.KUANTUM_GIRIS": {
    "unite": "Modern Fizik",
    "baslik": "Kuantum Fizigine Giris",
    "icerik": """KUANTUM FIZIGI GIRIS:

1. PLANCK'IN KUANTUM HIPOTEZI:
   - Enerji surekli degil, kesikli (kuantumlu) degerlerde alinir/verilir.
   - E = nhf (n = 1, 2, 3, ...).
   - Karacisim isinlami problemini cozdu.
   - h = 6.63 × 10⁻³⁴ J·s (Planck sabiti).

2. COMPTON SACILMASI:
   - X-isinlari elektronlardan sacildiginda dalga boyu uzar.
   - Δλ = (h/mₑc)(1 - cosθ).
   - Fotonun parcacik gibi davrandigini dogruliyor.

3. BELIRSIZLIK ILKESI:
   - Heisenberg: Δx·Δp ≥ ℏ/2 (ℏ = h/2π).
   - Konum ne kadar kesin bilinirse, momentum o kadar belirsiz olur.
   - ΔE·Δt ≥ ℏ/2 (enerji-zaman belirsizligi).
   - Makroskopik cisimlerde etkisi ihmal edilebilir kucukluktedir.

4. SCHRODINGER DENKLEMI (TANITIM):
   - iℏ(∂Ψ/∂t) = ĤΨ (zamanla degisen Schrodinger denklemi).
   - Ψ(x,t): Dalga fonksiyonu.
   - |Ψ|²: Olasilik yogunlugu (parcacigin bulunma olasiligi).
   - Kuantum sayilari: n (temel), l (acisal momentum), mₗ (manyetik), mₛ (spin).

5. TUNEL ETKISI:
   - Klasik fizikte gecilemeyecek bir enerji bariyerini kuantum mekaniginde
     parcacik belirli olasilikla gecebilir.
   - Alfa bozunmasi bu etkiyle aciklanir.
   - Tunel diyot, taramali tunelleme mikroskobu (STM) uygulamalari.

6. STANDART MODEL (TANITIM):
   - Temel parcaciklar: Kuarklar (u, d, s, c, b, t) ve Leptonlar (e, μ, τ, νₑ, νμ, ντ).
   - Kuvvet tasiyicilar: Foton (EM), W±/Z° (zayif), Gluon (guclu).
   - Higgs bozonu: Kutlenin kaynagi (2012'de CERN'de kesfedildi).
"""
},

}

def get_fizik12_reference(topic: str) -> list:
    """Verilen konuya en yakin fizik 12 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in FIZIK_12_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_fizik12_keys() -> list:
    """Tum fizik 12 referans anahtarlarini dondurur."""
    return list(FIZIK_12_REFERANS.keys())
