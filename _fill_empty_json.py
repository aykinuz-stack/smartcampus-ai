"""Bos JSON dosyalarini ornek veriyle doldur."""
import json, os, uuid, random
from datetime import date, timedelta

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def rand_id(p="id"):
    return f"{p}_{uuid.uuid4().hex[:8]}"

ISIM = ["Ahmet","Mehmet","Ali","Kerem","Burak","Zeynep","Elif","Sude","Ada","Defne"]
SOY = ["Yilmaz","Kaya","Demir","Celik","Sahin","Arslan","Dogan","Kilic"]
TODAY = date.today().isoformat()

def rn():
    return f"{random.choice(ISIM)} {random.choice(SOY)}"

# Dosya -> ornek veri
SAMPLES = {
    "akademik/academic_plans.json": [{"id":rand_id("plan"),"sinif":8,"ders":"Matematik","donem":"2025-2026","hafta":w,"konu":f"Unite {w}"} for w in range(1,6)],
    "akademik/dijital_ogrenme.json": [{"id":rand_id("do"),"baslik":"Khan Academy","tur":"video","sinif":8}],
    "akademik/etut_kayitlari.json": [{"id":rand_id("etut"),"ogretmen":rn(),"sinif":"8","ders":"Matematik","tarih":TODAY,"saat":"15:00"}],
    "akademik/ilkokul_gunluk.json": [{"id":rand_id("ig"),"sinif":"2/A","tarih":TODAY,"notlar":"Normal gun"}],
    "akademik/ogretmen_izin.json": [{"id":rand_id("iz"),"ogretmen":rn(),"tarih":TODAY,"tur":"yillik","durum":"onaylandi"}],
    "akademik/online_ders.json": [{"id":rand_id("od"),"baslik":"Canli Ders","ogretmen":rn(),"tarih":TODAY}],
    "akademik/online_ders_kayit.json": [{"id":rand_id("ok"),"ders_id":"od_1","student_id":"stu_b5251b8f","katildi":True}],
    "akademik/veli_belge_talepleri.json": [{"id":rand_id("vbt"),"veli":rn(),"tur":"ogrenci_belgesi","durum":"bekliyor","tarih":TODAY}],
    "akademik/veli_geri_bildirim.json": [{"id":rand_id("vgb"),"veli":rn(),"puan":4,"mesaj":"Memnunuz","tarih":TODAY}],
    "akademik/teacher_assignments.json": [{"id":rand_id("ta"),"ogretmen":rn(),"sinif":"8/A","ders":"Matematik"}],
    "akademik/risk_alerts.json": [{"id":rand_id("ra"),"student_id":"stu_b5251b8f","tur":"devamsizlik","mesaj":"3 gun ust uste","tarih":TODAY}],
    "akademik/gunluk_bulten.json": {"tarih":TODAY,"ozet":"Bugun okulda etkinlik var.","duyurular":[],"etkinlikler":[]},
    "akademik/olcme_takvim.json": [{"id":"ot_001","ders":"Matematik","sinif":8,"tarih":"2026-04-28","tur":"yazili"}],
    "akademik/destek_planlari.json": [{"id":rand_id("dp"),"ogrenci":rn(),"ders":"Matematik","plan":"Ek ders + quiz"}],
    "akademik/kazanim_borclar.json": [{"id":rand_id("kb"),"student_id":"stu_b5251b8f","ders":"Matematik","kazanim":"Denklemler"}],
    "akademik/mudahale_kayitlari.json": [{"id":rand_id("mk"),"ogrenci":rn(),"tur":"akademik","tarih":TODAY}],
    "akademik/nobet_gorevler.json": [{"id":rand_id("ng"),"ogretmen":rn(),"tarih":TODAY,"yer":"Koridor","saat":"08:00-09:00"}],
    "akademik/nobet_kayitlar.json": [{"id":rand_id("nk"),"ogretmen":rn(),"tarih":TODAY,"durum":"tamamlandi"}],
    "akademik/ogretmen_onerileri.json": [{"id":rand_id("oo"),"ogretmen":rn(),"oneri":"Ders materyali artirilmali","tarih":TODAY}],
    "akademik/platform_giris.json": [{"id":rand_id("pg"),"kullanici":"admin","tarih":TODAY,"saat":"08:30","platform":"web"}],
    "akademik/sertifikalar.json": [{"id":rand_id("srt"),"ogrenci":rn(),"tur":"basari","tarih":TODAY}],
    "akademik/veli_mesajlar.json": [{"id":rand_id("vm"),"gonderen":rn(),"alici":"ogretmen","mesaj":"Gorusme istiyorum","tarih":TODAY}],
    "akademik/schedule.json": [{"id":rand_id("sc"),"sinif":"8","sube":"A","gun":"Pazartesi","saat":1,"ders":"Matematik","ogretmen":rn()}],
    "akademik/vekil_gorevler.json": [{"id":rand_id("vk"),"izinli":rn(),"vekil":rn(),"tarih":TODAY,"ders_saatleri":[1,2,3]}],
    "davranissal_risk/audit_log.json": [{"tarih":TODAY,"olay":"tarama","kullanici":"admin"}],
    "davranissal_risk/protocols.json": [{"id":rand_id("pr"),"ad":"Zorbalik Protokolu","adimlar":["Tespit","Gorusme","Takip"]}],
    "english/cefr_placement/placement_exams.json": [{"seviye":"A1","soru_sayisi":30}],
    "english/yd_answers.json": [{"student_id":"stu_b5251b8f","ders_no":1,"puan":85}],
    "english/yd_lesson_records.json": [{"student_id":"stu_b5251b8f","ders_no":1,"tamamlandi":True}],
    "kurumsal/pozisyonlar.json": [{"id":"poz_01","ad":"Okul Muduru"},{"id":"poz_02","ad":"Ogretmen"},{"id":"poz_03","ad":"Rehber"}],
    "mezunlar/mezunlar.json": [{"id":rand_id("mez"),"ad_soyad":rn(),"yil":2024,"uni":"Istanbul Uni"}],
    "olcme/rubrics.json": [{"id":rand_id("rub"),"ad":"Proje Rubrik","kriterler":[{"ad":"Icerik","max":25}]}],
    "olcme/stok_raporlari.json": [{"tarih":TODAY,"ders":"Matematik","toplam_soru":150}],
    "rehberlik/bep_planlari.json": [{"id":rand_id("bep"),"ogrenci":rn(),"engel":"Ogrenme Guclugu","durum":"aktif"}],
    "rehberlik/gelisim_dosyasi.json": [{"id":rand_id("gd"),"ogrenci":rn(),"guclu":["Matematik"],"gelisim":["Dikkat"]}],
    "rehberlik/kriz_mudahale.json": [{"id":rand_id("km"),"ogrenci":rn(),"tur":"siddet","ciddiyet":"orta","tarih":TODAY}],
    "rehberlik/risk_degerlendirme.json": [{"id":rand_id("rd"),"ogrenci":rn(),"seviye":"orta","skor":65,"tarih":TODAY}],
    "rehberlik/yonlendirmeler.json": [{"id":rand_id("yn"),"ogrenci":rn(),"tur":"RAM","durum":"bekliyor","tarih":TODAY}],
    "sosyal_etkinlik/etkinlikler.json": [{"id":rand_id("etk"),"ad":"23 Nisan","tarih":"2026-04-23","yer":"Salon"}],
    "sosyal_etkinlik/kulupler.json": [{"id":rand_id("k"),"ad":"Robotik","danisman":rn(),"sayi":15}],
    "toplanti/toplantilar.json": [{"id":rand_id("t"),"baslik":"Ogretmenler Kurulu","tarih":"2026-04-25","saat":"14:00"}],
    # SC3D
    "sc3d/hotspots.json": [{"id":"hs1","ad":"Kutuphane","x":100,"y":200}],
    "sc3d/quizzes.json": [{"id":"qz1","soru":"Okul kac yilinda kuruldu?","cevap":"2010"}],
    "sc3d/tour_steps.json": [{"id":"ts1","sira":1,"baslik":"Giris","aciklama":"Okula hos geldiniz"}],
    # KIM01
    "kim01_org_assignments.json": [{"id":rand_id("oa"),"pozisyon":"Mudur","kisi":rn()}],
    "kim01_org_chart.json": [{"id":"root","ad":"Okul Muduru","children":["poz_02"]}],
    "kim01_reporting_lines.json": [{"ust":"Mudur","alt":"Mudur Yardimcisi"}],
    # PR01
    "pr01_gorusme_davet.json": [{"id":rand_id("gd"),"aday":rn(),"tarih":TODAY,"durum":"gonderildi"}],
    # Olcme tenant
    "olcme/annual_plans.json": [{"id":rand_id("ap"),"ders":"Matematik","sinif":8,"donem":"2025-2026"}],
    "olcme/answers.json": [],
    "olcme/blueprints.json": [],
    "olcme/outcomes.json": [],
    "olcme/results.json": [],
    "olcme/sessions.json": [],
    "olcme/telafi_tasks.json": [],
    # Akademik tenant extras
    "akademik/kyt_cevaplar.json": [],
    "akademik/teachers.json": [{"id":rand_id("ogr"),"ad_soyad":rn(),"brans":"Matematik","email":"ogr@okul.com"}],
    # Toplanti tenant
    "toplanti/participants.json": [{"toplanti_id":"top_1","katilimci":rn(),"durum":"katildi"}],
}

filled = 0
for root, dirs, files in os.walk("data"):
    dirs[:] = [d for d in dirs if d not in ('.venv', '.git')]
    for f in files:
        if not f.endswith('.json'):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if data and data != [] and data != {}:
                continue
        except:
            pass

        # Bos — doldurmaya calis
        # Relative path'i bul (data/ veya data/tenants/X/ sonrasi)
        rel = os.path.relpath(path, "data")
        # Tenant prefix'i cikar
        for prefix in ["tenants/smartcampus_koleji/", "tenants/uz_koleji/"]:
            if rel.startswith(prefix):
                rel = rel[len(prefix):]
                break

        if rel in SAMPLES:
            save(path, SAMPLES[rel])
            filled += 1
        # else: bos kalir (onemli degil)

print(f"\nDoldurulan: {filled}")

# Final kontrol
empty = 0
for root, dirs, files in os.walk("data"):
    dirs[:] = [d for d in dirs if d not in ('.venv', '.git')]
    for f in files:
        if not f.endswith('.json'): continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                d = json.load(fh)
            if d == [] or d == {} or d is None:
                empty += 1
        except:
            empty += 1
print(f"Kalan bos: {empty}")
