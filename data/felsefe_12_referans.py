# -*- coding: utf-8 -*-
"""
12. Sinif Felsefe (Secmeli) dersi - MEB 2025 mufredatina uygun referans verileri.
Ogrenme alanlari:
1. Mantiga Giris
2. Klasik Mantik
3. Modern Mantik
4. Bilgi-Bilim-Felsefe Iliskisi
"""

FELSEFE_12_REFERANS = {

# ═══════════════════════════════════════════════════════════════
# 1. MANTIGA GIRIS
# ═══════════════════════════════════════════════════════════════

"FEL.12.1.MANTIK_GIRIS": {
    "unite": "Mantığa Giriş",
    "baslik": "Mantik Nedir, Temel Kavramlar ve Akil Yurutme",
    "icerik": """MANTIGA GIRIS:

1. MANTIK NEDIR?
   - Mantik: Dogru dusunmenin kurallarini belirleyen, akil yurutmelerin
     gecerlilligini inceleyen bilim dalidir.
   - Kurucusu: Aristoteles (MO 384-322). "Organon" adli eserleri.
   - Mantik, dusuncenin ICI ile ilgilenir (icerik degil, FORM/BIÇIM).
   - Amac: Gecerli akil yurutme ile gecersizi ayirt etmek.

2. TEMEL KAVRAMLAR:
   - Terim (kavram): Dusuncenin en kucuk birimi. "Insan", "olumlu", "bitki".
   - Onerme (yargi): Dogru veya yanlis deger alabilen bildirm cumlesi.
     * "Ankara Turkiye'nin baskentidir." (DOGRU onerme)
     * "Dunya duzadir." (YANLIS onerme)
     * "Bugun hava guzel mi?" → Onerme DEGILDIR (soru cumlesi).
     * "Kapiyi kapat!" → Onerme DEGILDIR (emir cumlesi).
   - Akil yurutme (cikarim): Oncüllerden sonuc cikarma sureci.

3. AKIL YURUTME TURLERI:
   a) Tumdengelim (Deduksiyon): Genelden ozele. Oncüller dogru ise sonuc ZORUNLU OLARAK dogru.
      "Tum insanlar olumludur. Sokrates insandir. O halde Sokrates olumludur."
   b) Tümevarim (Induksiyon): Ozelden genele. Sonuc OLASILIK tasir, kesinlik yok.
      "Bugune kadar gorduğum tum kuğular beyazdir. Muhtemelen tum kugular beyazdir."
   c) Analoji (Benzetme): Benzer durumlardan cikarim. En zayif akil yurutme.
      "Mars Dunya'ya benzer. Dunya'da yasam var. Belki Mars'ta da vardir."

4. GECERLILIK VE DOGRULUK:
   - Gecerlilik: Akil yurutmenin BICIMSEL dogrulugu (mantiksal yapi).
   - Dogruluk: Onermelerin ICERIKSEL gerceklige uygunlugu.
   - Gecerli ama yanlış onculu akil yurutme mumkundur:
     "Tum kediler ucar. Pamuk bir kedidir. O halde Pamuk ucar." (Gecerli ama yanlis).
   - Saglamlk (tutarlilik): Hem gecerli hem oncuLleri dogru olan akil yurutme.

5. MANTIGIN DIGER BILIMLERLE ILISKISI:
   - Felsefe: Mantigin ana disiplini. Epistemoloji, etik ile iic ice.
   - Matematik: Ispat yontemleri, aksiyomatik sistem.
   - Bilgisayar bilimi: Programlama, yapay zeka, algoritmalar.
   - Hukuk: Kanun yorumlama, arguuman analizi.
   - Dil bilimi: Cumle yapisi, anlam analizi.
"""
},

# ═══════════════════════════════════════════════════════════════
# 2. KLASIK MANTIK
# ═══════════════════════════════════════════════════════════════

"FEL.12.2.KLASIK_ONERME": {
    "unite": "Klasik Mantık",
    "baslik": "Klasik Mantikta Onerme ve Kavram",
    "icerik": """KLASIK MANTIK - ONERME VE KAVRAM:

1. KAVRAM (TERIM):
   - Kavram: Bir nesne sinifini temsil eden zihinsel tasarim.
   - Icerik (connotation): Kavramın tanimi, ozellikleri. "Insan" → akilli, canli, memeli.
   - Kaplam (denotation): Kavramın kapsadigi bireyler. "Insan" → tum insanlar.
   - Icerik artar → kaplam azalir (ters orantı).
   - Bes tümel: Cins, tür, ayirim, ozguuluk, ilinti (Porfirus agaci).

2. ONERME TURLERI (NITELIK VE NICEELIK):
   - Nitelik: Olumlu (+) veya olumsuz (-).
   - Nicelik: Tumel (tum) veya tikel (bazi).
   - Dort temel onerme (AEIO):
     * A onermesi: Tumel olumlu → "Tum S, P'dir." (Her insan olumludur.)
     * E onermesi: Tumel olumsuz → "Hicbir S, P degildir." (Hicbir tas canli degildir.)
     * I onermesi: Tikel olumlu → "Bazi S, P'dir." (Bazi insanlar ogretmendir.)
     * O onermesi: Tikel olumsuz → "Bazi S, P degildir." (Bazi hayvanlar memeli degildir.)

3. ONERME ILISKILERI (KARESI):
   - Karşıt (konter): A-E → Ikisi birden dogru olamaz, ikisi birden yanlış olabilir.
   - Alt karşıt (subkonter): I-O → Ikisi birden yanlış olamaz, ikisi birden dogru olabilir.
   - Altik (subaltern): A-I ve E-O → Tumel dogru ise tikel de dogrudur.
   - Celiskili (kontradiktuar): A-O ve E-I → Biri dogru ise diger kesinlikle yanlıştır.

4. DONDURMELER:
   - Duz dondurme: Ozneyle yuklem yer degistirir.
     "Hicbir S, P degildir" → "Hicbir P, S degildir" (E→E gecerli).
     "Bazi S, P'dir" → "Bazi P, S'dir" (I→I gecerli).
     A→I (daraltma ile gecerli), O dondurulmez.
"""
},

"FEL.12.2.KIYAS": {
    "unite": "Klasik Mantık",
    "baslik": "Tasim (Kiyas / Sillogizm)",
    "icerik": """TASIM (KIYAS / SILLOGIZM):

1. TANIM:
   - Tasim: Iki oncul ve bir sonuctan olusan tumdengelimsel akil yurutme.
   - Standart biçim:
     Buyuk oncul: Tum M, P'dir.
     Kucuk oncul: Tum S, M'dir.
     Sonuc: Tum S, P'dir.

2. TERIMLER:
   - Buyuk terim (P): Sonucun yuklemi. Buyuk oncülde bulunur.
   - Kucuk terim (S): Sonucun oznesi. Kucuk oncülde bulunur.
   - Orta terim (M): Her iki oncülde bulunan ama sonucta olmayan terim.

3. TASIM FIGURLERI (SEKILLERI):
   - I. Figur: M-P, S-M → S-P (orta terim: buyukte ozne, kucukte yuklem).
   - II. Figur: P-M, S-M → S-P.
   - III. Figur: M-P, M-S → S-P.
   - IV. Figur: P-M, M-S → S-P.

4. TASIM KURALLARI:
   - Bir tasimda yalnizca uc terim olmalidir.
   - Orta terim en az bir kez tumel alinmalidir.
   - Oncullerde tikel olan terim sonucta tumel alinamaz.
   - Iki olumsuz oncülden sonuc cikmaz.
   - Oncüllerden biri olumsuz ise sonuc da olumsuz olmalidir.
   - Iki tikel oncülden gecerli sonuc cikmaz.

5. GECERLI TASIM KIPLERI:
   - I. Figur: Barbara (AAA), Celarent (EAE), Darii (AII), Ferio (EIO).
   - II. Figur: Cesare (EAE), Camestres (AEE), Festino (EIO), Baroco (AOO).
   - III. Figur: Darapti (AAI), Disamis (IAI), Datisi (AII), Felapton (EAO).

6. ENTIMEM:
   - Oncüllerden biri gizli (soylenmemis) olan kiyas.
   - "Sokrates olumludur, cunku o bir insandir."
     Gizli buyuk oncul: "Tum insanlar olumludur."

7. SORIT:
   - Birden fazla tasimin zincir halinde baglanmis hali.
   - Her tasimin sonucu bir sonraki tasimin onculu olur.
"""
},

# ═══════════════════════════════════════════════════════════════
# 3. MODERN MANTIK
# ═══════════════════════════════════════════════════════════════

"FEL.12.3.MODERN_MANTIK": {
    "unite": "Modern Mantık",
    "baslik": "Sembolik Mantik, Onerme Mantigi ve Dogruluk Tablolari",
    "icerik": """MODERN (SEMBOLIK) MANTIK:

1. MODERN MANTIK NEDIR?
   - Klasik mantigin sembollerle ifade edilmis, formellesmis halidir.
   - Dusunme ve akil yurutme sureclerini matematiksel sembollerle gosterir.
   - Kurucular: Boole, Frege, Russell, Whitehead, Tarski.

2. ONERME MANTIGI:
   - Onerme: Dogru (D) veya yanlis (Y) deger alan bildirim cumlesi.
   - Basit onerme: Tek yargi. Sembol: p, q, r, s...
   - Bilesik onerme: Basit onermelerin baglaclarla birlestirilmesi.

3. MANTIKSAL BAGLACLAR (KONNEKTIFLER):
   - Degilleme (Negasyon) ¬p: "p degil". p=D ise ¬p=Y; p=Y ise ¬p=D.
   - Ve (Konjunksiyon) p ∧ q: Her ikisi de D ise D. Biri Y ise Y.
   - Veya (Disjunksiyon) p ∨ q: En az biri D ise D. Ikisi de Y ise Y.
   - Kosullu (Implikasyon) p → q: Yalnizca p=D ve q=Y ise Y. Diger tum durumlar D.
   - Cift kosullu (Bikosul) p ↔ q: Ikisi ayni degerde ise D.

4. DOGRULUK TABLOLARI:
   - Her bilesik onermenin tum olası deger kombinasyonlarini gosterir.
   - n onerme icin 2^n satir olusur.
   - Totoloji: Her durumda D. Ornek: p ∨ ¬p.
   - Celiski: Her durumda Y. Ornek: p ∧ ¬p.
   - Olumsal: Bazi durumlarda D, bazi durumlarda Y.

5. MANTIKSAL DENKLIKLER:
   - De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q; ¬(p ∨ q) ≡ ¬p ∧ ¬q.
   - Kontrapozitif: (p → q) ≡ (¬q → ¬p).
   - Cift degilleme: ¬(¬p) ≡ p.
   - Dagilma: p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r).

6. GECERLI AKIL YURUTME KALIPLARI:
   - Modus Ponens: p → q, p ⊢ q.
   - Modus Tollens: p → q, ¬q ⊢ ¬p.
   - Hipotetik Tasim: p → q, q → r ⊢ p → r.
   - Disjunktif Tasim: p ∨ q, ¬p ⊢ q.
   - Yapici ikilem: p → q, r → s, p ∨ r ⊢ q ∨ s.
"""
},

# ═══════════════════════════════════════════════════════════════
# 4. BILGI-BILIM-FELSEFE ILISKISI
# ═══════════════════════════════════════════════════════════════

"FEL.12.4.BILGI_BILIM": {
    "unite": "Bilgi-Bilim-Felsefe İlişkisi",
    "baslik": "Bilgi Felsefesi, Bilim Felsefesi ve Bilimsel Yontem",
    "icerik": """BILGI-BILIM-FELSEFE ILISKISI:

1. BILGI FELSEFESI (EPISTEMOLOJI):
   - Bilginin ne oldugu, kaynaklari, sinirları ve gecerliligi.
   - Bilgi = Gerekcelendirilmis dogru inanc (Platon tanimi).
   - Bilgi kaynaklari:
     * Akil (Rasyonalizm): Descartes, Spinoza, Leibniz.
     * Deney/Deneyim (Ampirizm): Locke, Hume, Berkeley.
     * Sezgi (Intuisyonizm): Bergson.
     * Dogusstan fikirler (Nativizm): Platon, Descartes.
   - Kant sentezi: Bilgi hem deneyden hem akildan gelir (Kritisizm).

2. BILIM FELSEFESI:
   - Bilimsel bilginin doğasi, yontemleri ve sinirlari.
   - Yanlilanabilirlik (Popper): Bilimsel teori yanlislanabilir olmalidir.
     "Tum kugular beyazdir" → Tek siyah kugu yanlislar.
   - Paradigma (Kuhn): Bilimsel devrimler, normal bilim vs paradigma degisimi.
     Kopernik devrimi, Einstein fiziği.
   - Lakatos: Arastirma programlari. Sert cekirdek + koruyucu kusak.
   - Feyerabend: Epistemolojik anarsizm. "Her sey uyar."

3. BILIMSEL YONTEM:
   - Gozlem → Hipotez → Deney → Teori → Yasa.
   - Kontolu deney: Bagimsiz degisken manipule edilir.
   - Tumevarim: Tek tek gozlemlerden genel yasaya.
   - Tumdengelim: Genel yasadan tek tek durumlara.
   - Hipotetico-deduktif yontem: Hipotez → tahmin → test.

4. FELSEFE VE BILIM ILISKISI:
   - Felsefe bilimin annesidir (tarihsel olarak).
   - Bilim "nasil" sorusuna, felsefe "neden/ne" sorularina cevap arar.
   - Etik sorunlar: Gen muhendisligi, yapay zeka, cevrecilik.
   - Bilimin sinirları: Bilim her soruyu ceaplayabilir mi?

5. MANTIKSAL DUSUNME HATALARI (YANILTMACALAR):
   - Ad hominem: Arguman yerine kisiyi elestirme.
   - Otorite argumaani: "Prof. X soyledi, o halde doğrudur."
   - Yanlis neden-sonuc: Ardisiklik → nedensellik yanilgisi.
   - Genelleme hatasi: Yetersiz ornekten genel sonuc cikarma.
   - Saman adam: Karsinin argumanini carpitma.
   - Kaygan zemin: Kucuk bir adimin felaket zincirine yol acacagi iddiasi.
"""
},

}

def get_felsefe12_reference(topic: str) -> list:
    """Verilen konuya en yakin felsefe 12 referanslarini dondurur."""
    import difflib
    results = []
    topic_lower = topic.lower()
    for key, val in FELSEFE_12_REFERANS.items():
        searchable = f"{val['baslik']} {val['unite']} {val['icerik'][:500]}".lower()
        ratio = difflib.SequenceMatcher(None, topic_lower, searchable).ratio()
        if ratio > 0.25 or any(w in searchable for w in topic_lower.split() if len(w) > 3):
            results.append((ratio, key, val))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:5]

def get_all_felsefe12_keys() -> list:
    """Tum felsefe 12 referans anahtarlarini dondurur."""
    return list(FELSEFE_12_REFERANS.keys())
