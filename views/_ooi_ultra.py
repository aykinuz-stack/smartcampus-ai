"""
Okul Oncesi & Ilkokul — ULTRA MEGA Ozellikleri
=================================================
1. Cocuk Davranis DNA'si (Behavioral Intelligence)
2. Akilli Sinif Yonetim Asistani (Smart Classroom AI)
3. Ebeveyn Okulu (AI Parent Coach)
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


def _ogrenci_sec(store, key_prefix: str):
    try:
        from utils.shared_data import get_student_display_options
        students = get_student_display_options(include_empty=False)
    except Exception:
        students = {}
    if not students:
        st.warning("Ogrenci verisi bulunamadi.")
        return None, None
    sel = st.selectbox("Ogrenci Secin", [""] + list(students.keys()), key=f"{key_prefix}_sel")
    if not sel:
        return None, None
    return sel, students.get(sel, {})


# ============================================================
# 1. ÇOCUK DAVRANIŞ DNA'SI
# ============================================================

_DAVRANIS_BOYUTLARI = {
    "duygusal": {"label": "Duygusal Denge", "ikon": "😊", "renk": "#f59e0b"},
    "sosyal": {"label": "Sosyal Uyum", "ikon": "👫", "renk": "#10b981"},
    "beslenme": {"label": "Beslenme Duzeni", "ikon": "🍽️", "renk": "#ea580c"},
    "uyku": {"label": "Uyku Kalitesi", "ikon": "😴", "renk": "#7c3aed"},
    "odaklanma": {"label": "Odaklanma", "ikon": "🎯", "renk": "#2563eb"},
}


def _hesapla_davranis_puanlari(bultenler: list) -> dict[str, float]:
    """Bultenlerden 5 boyutlu davranis puani hesapla (0-100)."""
    if not bultenler:
        return {k: 50 for k in _DAVRANIS_BOYUTLARI}

    n = len(bultenler)
    puanlar = {}

    # Duygusal (ruh hali kararliligi)
    mutlu = sum(1 for b in bultenler if any(w in str(b.get("ruh_hali", b.get("duygu", b.get("genel_durum", "")))).lower() for w in ("iyi", "mutlu", "neseli")))
    puanlar["duygusal"] = round(mutlu / n * 100)

    # Sosyal
    sosyal_iyi = sum(1 for b in bultenler if any(w in str(b.get("sosyal", b.get("oyun", b.get("arkadaslik", "")))).lower() for w in ("grup", "birlikte", "paylast", "arkadaslari")))
    puanlar["sosyal"] = round(min(100, sosyal_iyi / n * 100 + 30))  # baz 30

    # Beslenme
    yemek_iyi = sum(1 for b in bultenler if not any(w in str(b.get("yemek", b.get("beslenme", ""))).lower() for w in ("az", "yemedi", "red", "istemedi")))
    puanlar["beslenme"] = round(yemek_iyi / n * 100)

    # Uyku
    uyku_iyi = sum(1 for b in bultenler if not any(w in str(b.get("uyku", b.get("uyku_durumu", ""))).lower() for w in ("kotu", "uyumadi", "huzursuz", "aglamali")))
    puanlar["uyku"] = round(uyku_iyi / n * 100)

    # Odaklanma
    odak_iyi = sum(1 for b in bultenler if any(w in str(b.get("basari", b.get("bugunku_basarisi", b.get("etkinlik", "")))).lower() for w in ("tamamla", "basari", "ogrendi", "katild", "yapt")))
    puanlar["odaklanma"] = round(min(100, odak_iyi / n * 100 + 20))

    return puanlar


def render_davranis_dna(store):
    """Cocuk davranis profili — 5 boyutlu analiz."""
    styled_section("Cocuk Davranis DNA'si", "#6366f1")
    styled_info_banner(
        "Butlenlerden otomatik 5 boyutlu davranis profili. "
        "Duygusal denge, sosyal uyum, beslenme, uyku, odaklanma.",
        banner_type="info", icon="🧬")

    sel, stu_data = _ogrenci_sec(store, "dna")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    ak = _ak_dir()

    # Bultenler
    tum = _lj(os.path.join(ak, "gunluk_bulten.json")) + _lj(os.path.join(ak, "ilkokul_gunluk.json"))
    ogr_bulten = [b for b in tum if b.get("student_id") == sid]

    if not ogr_bulten:
        styled_info_banner("Davranis analizi icin bulten verisi gerekli.", banner_type="warning", icon="📝")
        return

    # Son 30 gun
    son_30g = (date.today() - timedelta(days=30)).isoformat()
    son_bulten = [b for b in ogr_bulten if b.get("tarih", "") >= son_30g]
    if not son_bulten:
        son_bulten = ogr_bulten[-30:]

    puanlar = _hesapla_davranis_puanlari(son_bulten)
    genel = round(sum(puanlar.values()) / max(len(puanlar), 1))
    g_renk = "#10b981" if genel >= 70 else "#f59e0b" if genel >= 50 else "#ef4444"

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);
                border:2px solid {g_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {g_renk}30;text-align:center;">
        <div style="font-size:10px;color:#a5b4fc;letter-spacing:3px;text-transform:uppercase;">Davranis DNA — {ad}</div>
        <div style="font-size:56px;font-weight:900;color:{g_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{genel}</div>
        <div style="font-size:12px;color:#a5b4fc;">{len(son_bulten)} bulten analiz edildi</div>
    </div>""", unsafe_allow_html=True)

    # ── 5 BOYUT BAR CHART ──
    styled_section("Davranis Boyutlari")
    for boyut_key, boyut_info in _DAVRANIS_BOYUTLARI.items():
        puan = puanlar.get(boyut_key, 50)
        renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
        bar_w = min(puan, 100)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="font-size:18px;min-width:24px;">{boyut_info['ikon']}</span>
            <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:700;">{boyut_info['label']}</span>
            <div style="flex:1;background:#1e293b;border-radius:4px;height:22px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{boyut_info['renk']},{boyut_info['renk']}80);
                            border-radius:4px;display:flex;align-items:center;padding-left:8px;">
                    <span style="font-size:10px;color:#fff;font-weight:800;">{puan}</span></div></div>
        </div>""", unsafe_allow_html=True)

    # ── AI YORUM ──
    st.divider()
    if st.button("AI Davranis Degerlendirmesi", key=f"dna_ai_{sid}", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                veri = f"Cocuk: {ad}\nDavranis Puanlari: " + ", ".join(f"{_DAVRANIS_BOYUTLARI[k]['label']}:{v}" for k, v in puanlar.items())
                veri += f"\nGenel: {genel}/100, Bulten sayisi: {len(son_bulten)}"
                with st.spinner("AI analiz ediyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir cocuk gelisim uzmanisin. Cocugun davranis puanlarini analiz et. Guclu yonleri ov, gelisim alanlarini nazikce belirt, somut oneriler sun. Turkce, sicak, veliye hitaben."},
                            {"role": "user", "content": veri},
                        ],
                        max_tokens=400, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #6366f1;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#a5b4fc;font-weight:700;margin-bottom:6px;">AI Davranis Yorumu</div>
                        <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 2. AKILLI SINIF YÖNETİM ASİSTANI
# ============================================================

def render_sinif_asistani(store):
    """Ogretmenin dijital sinif asistani."""
    styled_section("Akilli Sinif Asistani", "#0891b2")
    styled_info_banner(
        "Sabah acilis ekrani: bugunku plan, dikkat edilecek ogrenciler, "
        "dogum gunu, eksik bultenler. Gun sonu otomatik ozet.",
        banner_type="info", icon="🎛️")

    bugun = date.today()
    bugun_str = bugun.isoformat()
    ak = _ak_dir()
    td = _td()

    # Sinif/sube sec
    col1, col2 = st.columns(2)
    with col1:
        sinif = st.selectbox("Sinif", ["Anasinifi 3 Yas", "Anasinifi 4 Yas", "Anasinifi 5 Yas",
                                         "1. Sinif", "2. Sinif", "3. Sinif", "4. Sinif"], key="sa_sinif")
    with col2:
        sube = st.selectbox("Sube", ["A", "B", "C", "D"], key="sa_sube")

    # Ogrenci listesi
    students = _lj(os.path.join(ak, "students.json"))
    sinif_ogr = [s for s in students if str(s.get("sinif", "")) == str(sinif) and s.get("sube", "") == sube
                  and s.get("durum", "aktif") == "aktif"]

    if not sinif_ogr:
        styled_info_banner(f"{sinif} {sube} sinifinda ogrenci bulunamadi.", banner_type="warning", icon="👤")
        return

    # Bultenler
    tum_bulten = _lj(os.path.join(ak, "gunluk_bulten.json")) + _lj(os.path.join(ak, "ilkokul_gunluk.json"))
    bugun_bulten_ids = set(b.get("student_id") for b in tum_bulten if b.get("tarih", "") == bugun_str)

    # Veli geri bildirim
    veli_fb = _lj(os.path.join(ak, "veli_geri_bildirim.json"))
    dun = (bugun - timedelta(days=1)).isoformat()
    dun_veli = [v for v in veli_fb if v.get("tarih", "") == dun]

    # Dogum gunu
    dogum_gunu = []
    for s in sinif_ogr:
        dg = s.get("dogum_tarihi", "")
        if dg and len(dg) >= 10 and dg[5:10] == bugun_str[5:10]:
            dogum_gunu.append(f"{s.get('ad', '')} {s.get('soyad', '')}")

    # Bulten eksik
    bulten_eksik = [s for s in sinif_ogr if s.get("id", "") not in bugun_bulten_ids]

    styled_stat_row([
        ("Sinif Mevcudu", str(len(sinif_ogr)), "#0891b2", "👤"),
        ("Bulten Girildi", str(len(sinif_ogr) - len(bulten_eksik)), "#10b981", "✅"),
        ("Bulten Eksik", str(len(bulten_eksik)), "#ef4444", "⚠️"),
        ("Dogum Gunu", str(len(dogum_gunu)), "#f59e0b", "🎂"),
    ])

    # ── SABAH BRİFİNG ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0c4a6e,#155e75);border:2px solid #0891b2;
                border-radius:16px;padding:18px 22px;margin:8px 0;">
        <div style="font-size:14px;font-weight:800;color:#67e8f9;margin-bottom:8px;">
            Gunaydin! {sinif} {sube} — {bugun.strftime('%d.%m.%Y')}</div>
        <div style="font-size:12px;color:#a5f3fc;line-height:1.8;">
            Sinif mevcudu: <b>{len(sinif_ogr)}</b> ogrenci ·
            Bulten girilmemis: <b style="color:{'#ef4444' if bulten_eksik else '#10b981'};">{len(bulten_eksik)}</b>
            {f' · 🎂 Dogum gunu: <b>{", ".join(dogum_gunu)}</b>' if dogum_gunu else ''}
        </div>
    </div>""", unsafe_allow_html=True)

    # Dikkat edilecek ogrenciler (dunku veli geri bildiriminden)
    dikkat = []
    for v in dun_veli:
        if v.get("student_id") in [s.get("id") for s in sinif_ogr]:
            mesaj = v.get("mesaj", v.get("aciklama", ""))
            if any(w in str(mesaj).lower() for w in ("agladi", "hasta", "uzgun", "kotu", "yemedi", "uyumadi", "korkt")):
                ogr = next((s for s in sinif_ogr if s.get("id") == v.get("student_id")), {})
                dikkat.append({"ad": f"{ogr.get('ad', '')} {ogr.get('soyad', '')}", "mesaj": mesaj[:60]})

    if dikkat:
        styled_section("Dikkat Edilecek Ogrenciler", "#ef4444")
        for d in dikkat:
            st.markdown(f"""
            <div style="background:#450a0a;border:1px solid #ef4444;border-radius:8px;
                        padding:8px 12px;margin-bottom:4px;">
                <span style="font-weight:700;color:#fca5a5;">{d['ad']}</span>
                <span style="color:#fca5a5;font-size:11px;margin-left:8px;">— Veli: "{d['mesaj']}"</span>
            </div>""", unsafe_allow_html=True)

    # Bulten eksik liste
    if bulten_eksik:
        styled_section(f"Bulten Eksik ({len(bulten_eksik)} ogrenci)", "#f59e0b")
        for s in bulten_eksik[:10]:
            st.markdown(f"- ⬜ {s.get('ad', '')} {s.get('soyad', '')}")

    # Dogum gunu kutlama
    if dogum_gunu:
        st.markdown(f"""
        <div style="background:#c9a84c15;border:2px solid #c9a84c;border-radius:14px;
                    padding:14px;text-align:center;margin:8px 0;">
            <div style="font-size:32px;">🎂🎈🎉</div>
            <div style="font-size:14px;font-weight:800;color:#c9a84c;margin:4px 0;">
                Dogum Gunu Kutlu Olsun!</div>
            <div style="font-size:13px;color:#e8d48b;">{', '.join(dogum_gunu)}</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. EBEVEYN OKULU (AI PARENT COACH)
# ============================================================

_YAS_REHBERLERI = {
    3: {
        "baslik": "3 Yas Gelisim Rehberi",
        "maddeler": [
            "Cocugunuz artik 3-4 kelimelik cumleler kurabilir",
            "Renkleri ve basit sekilleri tanir",
            "Paylasmayi ogrenmeye baslar — sabir gosterin",
            "Tuvalet egitimi tamamlanma asamasinda olabilir",
            "Hayal gucu hizla gelisir — hikaye okuyun",
        ],
    },
    4: {
        "baslik": "4 Yas Gelisim Rehberi",
        "maddeler": [
            "10'a kadar sayabilir, harfleri tanimaya baslar",
            "Makasla kesme becerisi gelisir — guvenli makas verin",
            "Grup oyunlarina katilim artar",
            "Neden-sonuc iliskisini anlamaya baslar",
            "Gecmis zaman kullanarak konusur",
        ],
    },
    5: {
        "baslik": "5 Yas Gelisim Rehberi",
        "maddeler": [
            "Adini yazabilir, harfleri tanir",
            "Basit toplama yapabilir",
            "Oykuleri sirasiyla anlatabilir",
            "Arkadaslik iliskileri derinlesir",
            "Okula hazirlik donemi — okuma ilgisini destekleyin",
        ],
    },
    6: {
        "baslik": "6 Yas (1. Sinif) Rehberi",
        "maddeler": [
            "Okuma-yazma ogrenme donemindedir — sabir gosterin",
            "Her cocugun okuma hizi farklıdır — kiyaslamayin",
            "Ev odevi rutini olusturun — kisa sureli, duzenli",
            "Sosyal becerileri guclendirin — arkadaslik destekleyin",
            "Ekran suresi sinirlandirin — kitap okuma tesvik edin",
        ],
    },
    7: {
        "baslik": "7 Yas (2. Sinif) Rehberi",
        "maddeler": [
            "Akici okuma beklenir — her gun 15 dk okuma yapin",
            "Carpma islemi baslar — oyunla ogrenmeyi deneyin",
            "Sorumluluk verin: cantasini hazirlama, odasini toplama",
            "Takım sporlari sosyal gelisimi destekler",
            "Ozguvenini besleyin — basarilarini takdir edin",
        ],
    },
}


def render_ebeveyn_okulu(store):
    """Velilere cocuk gelisim verisine dayali ebeveynlik onerileri."""
    styled_section("Ebeveyn Okulu", "#059669")
    styled_info_banner(
        "Cocugunuzun verilerine dayali kisisel ebeveynlik onerileri. "
        "Yasa gore rehber + AI kocluk + evde yapilacak aktiviteler.",
        banner_type="info", icon="👪")

    sel, stu_data = _ogrenci_sec(store, "eo")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    sinif = stu_data.get("sinif", "")
    ak = _ak_dir()
    td = _td()

    # Yas tahmini
    yas_map = {"Anasinifi 3 Yas": 3, "Anasinifi 4 Yas": 4, "Anasinifi 5 Yas": 5,
               "1. Sinif": 6, "2. Sinif": 7, "3. Sinif": 8, "4. Sinif": 9}
    yas = yas_map.get(str(sinif), 5)

    # Milestone
    milestones = next((k for k in _lj(os.path.join(td, "akademik", "milestone_takip.json")) if k.get("student_id") == sid), None)

    sub = st.tabs(["📚 Yas Rehberi", "🤖 AI Kocluk", "🏠 Evde Aktivite"])

    # ═══ YAŞ REHBERİ ═══
    with sub[0]:
        rehber = _YAS_REHBERLERI.get(yas)
        if rehber:
            styled_section(rehber["baslik"])
            for madde in rehber["maddeler"]:
                st.markdown(f"""
                <div style="background:#052e16;border:1px solid #059669;border-left:3px solid #059669;
                            border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:4px;">
                    <span style="font-size:12px;color:#6ee7b7;">✅ {madde}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info(f"{yas} yas icin rehber henuz tanimlanmamis.")

    # ═══ AI KOÇLUK ═══
    with sub[1]:
        styled_section("AI Ebeveynlik Koclucu")
        if st.button("AI Kisisel Oneri Olustur", key=f"eo_ai_{sid}", type="primary", use_container_width=True):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    # Veri topla
                    tum = _lj(os.path.join(ak, "gunluk_bulten.json")) + _lj(os.path.join(ak, "ilkokul_gunluk.json"))
                    ogr_bulten = [b for b in tum if b.get("student_id") == sid][-10:]
                    bulten_ozet = "\n".join(f"- {b.get('tarih', '')}: Yemek:{b.get('yemek', '-')}, Uyku:{b.get('uyku', '-')}, Ruh:{b.get('ruh_hali', '-')}" for b in ogr_bulten[:5]) or "Bulten yok"

                    ms_ozet = ""
                    if milestones:
                        ms_data = milestones.get("milestones", {})
                        henuz = [k.split("_", 1)[1] if "_" in k else k for k, v in ms_data.items() if v == "henuz"][:8]
                        ms_ozet = f"Henuz kazanilmamis: {', '.join(henuz)}" if henuz else "Tum milestone'lar tamamlanmis!"

                    with st.spinner("AI ebeveynlik onerileri hazirlaniyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir cocuk gelisim uzmani ve ebeveynlik kocusun. Cocugun verilerine dayanarak veliye kisisel oneriler sun: 1) Evde yapilacak 3 aktivite 2) Dikkat edilecek davranis 3) Beslenme/uyku onerisi 4) Haftalik hedef. Turkce, sicak, destekleyici."},
                                {"role": "user", "content": f"Cocuk: {ad}, Yas: {yas}, Sinif: {sinif}\nBultenler:\n{bulten_ozet}\n{ms_ozet}"},
                            ],
                            max_tokens=500, temperature=0.7,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #059669;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#6ee7b7;font-weight:700;margin-bottom:6px;">AI Ebeveynlik Onerileri — {ad}</div>
                            <div style="font-size:12px;color:#d1fae5;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")

    # ═══ EVDE AKTİVİTE ═══
    with sub[2]:
        styled_section("Evde Yapilabilecek Aktiviteler")

        _EV_AKTIVITELERI = {
            3: [("Boyama kitabi", "Sinirlar icinde kalmaya calisin — motor gelisim"), ("Lego/blok", "Sekil yapma — bilissel"), ("Sarki soyleme", "Dil gelisimi — birlikte sarki soyeleyin")],
            4: [("Makas ile kesme", "Daire kesmek — ince motor"), ("Sayma oyunu", "Merdiven cikarken sayma — bilissel"), ("Hikaye uydurma", "Baslangic verin cocuk devam etsin — dil")],
            5: [("Harf yazma", "Her gun 1 harf — okula hazirlik"), ("Puzzle (50+ parca)", "Sabir + problem cozme"), ("Sofra kurma", "Sorumluluk — oz bakim")],
            6: [("15 dk kitap okuma", "Her gun duzeni — okuma aliskanligi"), ("Toplama oyunu", "Zarla toplama — matematik"), ("Gunluk yazma", "3 cumle — yazma becerisi")],
            7: [("Kitap okuma (30 dk)", "Sesli okuma + anlama sorulari"), ("Carpma tablosu oyunu", "Kartlarla eslestirme"), ("Proje odevi", "Arastirma yapma — bagımsızlık")],
        }

        aktiviteler = _EV_AKTIVITELERI.get(yas, _EV_AKTIVITELERI.get(5, []))
        for akt_ad, akt_aciklama in aktiviteler:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #05966930;border-left:3px solid #059669;
                        border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:6px;">
                <span style="font-weight:700;color:#6ee7b7;font-size:13px;">{akt_ad}</span>
                <div style="font-size:11px;color:#94a3b8;margin-top:2px;">{akt_aciklama}</div>
            </div>""", unsafe_allow_html=True)

        st.caption(f"Yas grubu: {yas} yas · Sinif: {sinif}")
