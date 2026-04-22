"""
Okul Oncesi & Ilkokul — Zirve Ozellikleri
============================================
1. Cocuk Gelisim Takip Motoru (Milestone Tracker)
2. Haftalik Veli Rapor Karti
3. AI Erken Gelisim Uyari Sistemi
"""
from __future__ import annotations

import json
import os
import uuid
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


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


def _ogrenci_sec(store, key_prefix: str):
    """Ogrenci secimi helper — sinif/sube/ogrenci dropdown."""
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
# 1. ÇOCUK GELİŞİM TAKİP MOTORU (MILESTONE TRACKER)
# ============================================================

_GELISIM_ALANLARI = {
    "bilissel": {
        "label": "Bilissel Gelisim", "ikon": "🧠", "renk": "#2563eb",
        "milestones": {
            3: ["Renkleri taniyor", "3'e kadar sayiyor", "Basit puzzle yapiyor", "Sekilleri taniyor"],
            4: ["10'a kadar sayiyor", "Harfleri taniyor", "Eslestirme yapiyor", "Neden-sonuc anlıyor"],
            5: ["20'ye kadar sayiyor", "Adini yaziyor", "Basit toplama", "Oykuyu siralıyor"],
            6: ["Okuma baslangici", "Toplama-cikarma", "Saat okuma", "Para taniyor"],
            7: ["Akici okuma", "Carpma baslangici", "Problem cozme", "Harita okuma"],
        },
    },
    "dil": {
        "label": "Dil Gelisimi", "ikon": "🗣️", "renk": "#7c3aed",
        "milestones": {
            3: ["3-4 kelimelik cumle", "Sorulari anlama", "Hikaye dinleme", "Temel renk/sayi soyleme"],
            4: ["5-6 kelimelik cumle", "Gecmis zaman kullanma", "Sarki soyleme", "Basit hikaye anlatma"],
            5: ["Karmasik cumleler", "Espri anlama", "Oykuyu yeniden anlatma", "Harf sesleri"],
            6: ["Okuma baslangici", "Yazma baslangici", "Kelime hazisnesi genisleme", "Hikaye yazma"],
            7: ["Akici okuma", "Paragraf yazma", "Dinlediklerini ozetleme", "Siir ezberleme"],
        },
    },
    "motor": {
        "label": "Motor Gelisim", "ikon": "🤸", "renk": "#ea580c",
        "milestones": {
            3: ["Merdiven cikma", "Top atma", "Kalem tutma", "Boyama (sinir disina cikma)"],
            4: ["Tek ayak ziplama", "Makasla kesme", "Dugme ilikleme", "Cizgi cizme"],
            5: ["Bisiklet surme", "Ayakkabi baglama", "Harf yazma", "Makasla sekil kesme"],
            6: ["El yazisi", "Cetvel kullanma", "Ip atlama", "Top yakalama"],
            7: ["Duzgun el yazisi", "Igne ipliker gecirme", "Jimnastik hareketleri", "Alet kullanma"],
        },
    },
    "sosyal": {
        "label": "Sosyal-Duygusal", "ikon": "👫", "renk": "#10b981",
        "milestones": {
            3: ["Paylasma", "Sira bekleme", "Duygulari taniyor", "Kurallara uyma"],
            4: ["Grup oyununda katilim", "Empati gosterme", "Ouz dileme", "Arkadaslik kurma"],
            5: ["Cozum odakli dusunme", "Duygulari ifade", "Kurallara uyum", "Yardimlesme"],
            6: ["Takim calismasi", "Liderlik", "Catiisma cozme", "Sorumluluk alma"],
            7: ["Empati gelistirme", "Farkli bakis acilari", "Ozguven", "Topluluk onunde konusma"],
        },
    },
    "yaraticilik": {
        "label": "Yaraticilik", "ikon": "🎨", "renk": "#f59e0b",
        "milestones": {
            3: ["Parmak boyasi", "Hamur oyunu", "Muzik dinleme", "Dans etme"],
            4: ["Resim cizme (insan)", "Sarki soyleme", "Oyun kurma", "Masal uydurma"],
            5: ["Detayli resim", "Enstruman deneme", "Drama/rol yapma", "Kolaj yapma"],
            6: ["Hikaye yazma", "Resim sergileme", "Muzik ritim", "El isleri"],
            7: ["Proje tasarimi", "Siir yazma", "Sahne performansi", "Dijital icerik"],
        },
    },
    "oz_bakim": {
        "label": "Oz Bakim", "ikon": "🧹", "renk": "#0891b2",
        "milestones": {
            3: ["El yikama", "Tuvalet kullanma", "Kasigiyla yeme", "Ayakkabi giyme"],
            4: ["Bagımsız tuvalet", "Dis fircalama", "Giyinme", "Sofra kurma yardim"],
            5: ["Tam bagımsız giyinme", "Saclari tarama", "Yatağını duzeltme", "Cantasini hazirlama"],
            6: ["Odasini toplama", "Basit yemek hazirlama", "Zamani yonetme", "Kisisel hijyen"],
            7: ["Tam bagımsızlık", "Para yonetimi", "Planlama yapma", "Sorumluluk"],
        },
    },
}


def _milestone_path() -> str:
    return os.path.join(_td(), "akademik", "milestone_takip.json")


def render_milestone_tracker(store):
    """Cocuk gelisim milestone takibi."""
    styled_section("Cocuk Gelisim Takip", "#6366f1")
    styled_info_banner(
        "Her cocugun yasina gore 6 gelisim alaninda milestone takibi. "
        "Tamamlanan, gelisen ve henuz baslanmamis becerileri izleyin.",
        banner_type="info", icon="🧒")

    sel, stu_data = _ogrenci_sec(store, "mst")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    sinif = stu_data.get("sinif", "")

    # Yas tahmini (sinif bazli)
    yas_map = {"Anasinifi 3 Yas": 3, "Anasinifi 4 Yas": 4, "Anasinifi 5 Yas": 5,
               "1. Sinif": 6, "2. Sinif": 7, "3. Sinif": 8, "4. Sinif": 9}
    yas = yas_map.get(str(sinif), 5)

    # Kayitli milestone
    tum_kayitlar = _lj(_milestone_path())
    ogr_kayit = next((k for k in tum_kayitlar if k.get("student_id") == sid), None)
    if not ogr_kayit:
        ogr_kayit = {"student_id": sid, "ad": ad, "milestones": {}}

    tamamlanan_toplam = sum(1 for v in ogr_kayit.get("milestones", {}).values() if v == "tamamlandi")
    gelisiyor_toplam = sum(1 for v in ogr_kayit.get("milestones", {}).values() if v == "gelisiyor")
    toplam_milestone = sum(len(m.get(yas, [])) for m in _GELISIM_ALANLARI.values())

    styled_stat_row([
        ("Yas Grubu", str(yas), "#6366f1", "🧒"),
        ("Tamamlanan", str(tamamlanan_toplam), "#10b981", "✅"),
        ("Gelisiyor", str(gelisiyor_toplam), "#f59e0b", "🔄"),
        ("Toplam Milestone", str(toplam_milestone), "#2563eb", "📋"),
    ])

    # Ilerleme gauge
    ilerleme = round(tamamlanan_toplam / max(toplam_milestone, 1) * 100)
    i_renk = "#10b981" if ilerleme >= 70 else "#f59e0b" if ilerleme >= 40 else "#ef4444"
    st.markdown(f"""
    <div style="background:#0f172a;border:1px solid {i_renk}40;border-radius:14px;
                padding:16px;text-align:center;margin:8px 0;">
        <div style="font-size:36px;font-weight:900;color:{i_renk};">%{ilerleme}</div>
        <div style="font-size:10px;color:#94a3b8;">Gelisim Tamamlanma Orani — {ad}</div>
        <div style="margin:8px auto 0;max-width:300px;background:#1e293b;border-radius:6px;height:10px;overflow:hidden;">
            <div style="width:{ilerleme}%;height:100%;background:{i_renk};border-radius:6px;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── ALAN BAZLI MILESTONE ──
    with st.form("milestone_form"):
        for alan_key, alan_info in _GELISIM_ALANLARI.items():
            milestones = alan_info.get("milestones", {}).get(yas, [])
            if not milestones:
                continue

            alan_tamam = sum(1 for m in milestones if ogr_kayit.get("milestones", {}).get(f"{alan_key}_{m}") == "tamamlandi")
            alan_pct = round(alan_tamam / max(len(milestones), 1) * 100)

            st.markdown(f"""
            <div style="background:#0f172a;border-left:4px solid {alan_info['renk']};
                        border-radius:0 10px 10px 0;padding:10px 14px;margin:8px 0 4px 0;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:13px;font-weight:700;color:#e2e8f0;">
                        {alan_info['ikon']} {alan_info['label']}</span>
                    <span style="background:{alan_info['renk']}20;color:{alan_info['renk']};padding:2px 10px;
                                border-radius:6px;font-size:10px;font-weight:700;">{alan_tamam}/{len(milestones)} — %{alan_pct}</span>
                </div>
            </div>""", unsafe_allow_html=True)

            cols = st.columns(2)
            for idx, m in enumerate(milestones):
                mkey = f"{alan_key}_{m}"
                mevcut = ogr_kayit.get("milestones", {}).get(mkey, "henuz")
                with cols[idx % 2]:
                    ogr_kayit.setdefault("milestones", {})[mkey] = st.selectbox(
                        m, ["henuz", "gelisiyor", "tamamlandi"],
                        index=["henuz", "gelisiyor", "tamamlandi"].index(mevcut),
                        format_func=lambda x: {"henuz": "⬜ Henuz", "gelisiyor": "🔄 Gelisiyor", "tamamlandi": "✅ Tamamlandi"}[x],
                        key=f"mst_{sid}_{mkey}")

        if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
            # Kaydet
            mevcut_kayitlar = [k for k in tum_kayitlar if k.get("student_id") != sid]
            ogr_kayit["updated_at"] = datetime.now().isoformat()
            mevcut_kayitlar.append(ogr_kayit)
            _sj(_milestone_path(), mevcut_kayitlar)
            st.success(f"Gelisim kaydi guncellendi: {ad}")
            st.rerun()


# ============================================================
# 2. HAFTALIK VELİ RAPOR KARTI
# ============================================================

def render_haftalik_veli_rapor(store):
    """Haftalik otomatik veli rapor ozeti."""
    styled_section("Haftalik Veli Rapor Karti", "#059669")
    styled_info_banner(
        "Her Cuma otomatik olusan haftalik ozet. "
        "5 gunun bultenlerinden yemek/uyku/ruh hali trendi + ogretmen yorumu.",
        banner_type="info", icon="📋")

    sel, stu_data = _ogrenci_sec(store, "hvr")
    if not sel:
        return

    sid = stu_data.get("id", "")
    ad = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()
    ak = _ak_dir()

    # Bu haftanin bultenleri
    bugun = date.today()
    hafta_bas = bugun - timedelta(days=bugun.weekday())
    hafta_bit = hafta_bas + timedelta(days=4)  # Cuma

    bultenler = _lj(os.path.join(ak, "gunluk_bulten.json"))
    if not bultenler:
        bultenler = _lj(os.path.join(ak, "ilkokul_gunluk.json"))

    hafta_bulten = [b for b in bultenler
                      if b.get("student_id") == sid
                      and hafta_bas.isoformat() <= b.get("tarih", "") <= hafta_bit.isoformat()]

    # Veli geri bildirimleri
    veli_fb = _lj(os.path.join(ak, "veli_geri_bildirim.json"))
    hafta_veli = [v for v in veli_fb
                    if v.get("student_id") == sid
                    and hafta_bas.isoformat() <= v.get("tarih", "") <= hafta_bit.isoformat()]

    styled_stat_row([
        ("Hafta", f"{hafta_bas.strftime('%d.%m')} — {hafta_bit.strftime('%d.%m')}", "#059669", "📅"),
        ("Bulten Sayisi", str(len(hafta_bulten)), "#2563eb", "📝"),
        ("Veli Bildirim", str(len(hafta_veli)), "#7c3aed", "📩"),
    ])

    if not hafta_bulten:
        styled_info_banner("Bu hafta icin bulten girilmemis.", banner_type="warning", icon="📝")
    else:
        # Gunluk ozet kartlari
        styled_section(f"{ad} — Haftalik Ozet")
        gun_adlari = ["Pzt", "Sal", "Car", "Per", "Cum"]

        for i in range(5):
            gun = hafta_bas + timedelta(days=i)
            gun_str = gun.isoformat()
            gun_bulten = next((b for b in hafta_bulten if b.get("tarih", "") == gun_str), None)

            if gun_bulten:
                yemek = gun_bulten.get("yemek", gun_bulten.get("beslenme", ""))
                uyku = gun_bulten.get("uyku", gun_bulten.get("uyku_durumu", ""))
                ruh = gun_bulten.get("ruh_hali", gun_bulten.get("duygu", gun_bulten.get("genel_durum", "")))
                basari = gun_bulten.get("basari", gun_bulten.get("bugunku_basarisi", ""))

                ruh_ikon = "😊" if "iyi" in str(ruh).lower() or "mutlu" in str(ruh).lower() else "😐" if "orta" in str(ruh).lower() else "😢" if "uzgun" in str(ruh).lower() else "😊"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #05966930;border-radius:10px;
                            padding:8px 14px;margin-bottom:4px;">
                    <div style="display:flex;gap:12px;align-items:center;font-size:11px;">
                        <span style="min-width:30px;font-weight:700;color:#6ee7b7;">{gun_adlari[i]}</span>
                        <span style="color:#94a3b8;">🍽️ {str(yemek)[:20] or '-'}</span>
                        <span style="color:#94a3b8;">😴 {str(uyku)[:15] or '-'}</span>
                        <span style="font-size:16px;">{ruh_ikon}</span>
                        <span style="color:#e2e8f0;flex:1;">{str(basari)[:40] or '-'}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#1e293b;border-radius:10px;padding:8px 14px;margin-bottom:4px;
                            font-size:11px;color:#64748b;">
                    {gun_adlari[i]} — Bulten girilmemis</div>""", unsafe_allow_html=True)

    # AI haftalik degerlendirme
    st.divider()
    if st.button("AI Haftalik Degerlendirme", key=f"hvr_ai_{sid}", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                bulten_ozet = "\n".join(
                    f"- {b.get('tarih', '')}: Yemek:{b.get('yemek', '-')}, Uyku:{b.get('uyku', '-')}, "
                    f"Ruh:{b.get('ruh_hali', b.get('duygu', '-'))}, Basari:{b.get('basari', b.get('bugunku_basarisi', '-'))}"
                    for b in hafta_bulten[:5]) or "Bulten yok"

                with st.spinner("AI haftalik rapor hazirlaniyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul oncesi/ilkokul ogretmenisin. Cocugun haftalik bultenlerini analiz et. Veliye hitaben kisa, sicak, olumlu bir haftalik degerlendirme yaz. Guclu yonleri ov, gelisim alanlarini nazikce belirt. Turkce."},
                            {"role": "user", "content": f"Ogrenci: {ad}, Sinif: {stu_data.get('sinif', '')}\n\nHaftalik Bultenler:\n{bulten_ozet}"},
                        ],
                        max_tokens=400, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #059669;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#6ee7b7;font-weight:700;margin-bottom:6px;">Haftalik Degerlendirme — {ad}</div>
                        <div style="font-size:12px;color:#d1fae5;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")


# ============================================================
# 3. AI ERKEN GELİŞİM UYARI SİSTEMİ
# ============================================================

def render_erken_gelisim_uyari(store):
    """Bulten verilerinden otomatik gelisim uyarilari."""
    styled_section("AI Erken Gelisim Uyari", "#ef4444")
    styled_info_banner(
        "Gunluk bulten verilerinden gelisim risklerini otomatik tespit eder. "
        "Yemek reddi, uyku bozuklugu, sosyal izolasyon — erken mudahale.",
        banner_type="warning", icon="⚠️")

    ak = _ak_dir()
    bultenler = _lj(os.path.join(ak, "gunluk_bulten.json"))
    if not bultenler:
        bultenler = _lj(os.path.join(ak, "ilkokul_gunluk.json"))

    if not bultenler:
        styled_info_banner("Bulten verisi yok — uyari uretilemiyor.", banner_type="info", icon="📝")
        return

    # Son 14 gun
    son_14g = (date.today() - timedelta(days=14)).isoformat()
    son_bultenler = [b for b in bultenler if b.get("tarih", "") >= son_14g]

    # Ogrenci bazli grupla
    ogr_bultenler = {}
    for b in son_bultenler:
        sid = b.get("student_id", "")
        if sid:
            ogr_bultenler.setdefault(sid, []).append(b)

    # Uyari uret
    uyarilar = []

    for sid, blist in ogr_bultenler.items():
        # Ogrenci adi bul
        ogr_ad = blist[0].get("ogrenci_adi", blist[0].get("ad", sid))

        # 1. Yemek reddi
        yemek_kotu = sum(1 for b in blist if "az" in str(b.get("yemek", b.get("beslenme", ""))).lower()
                          or "yemedi" in str(b.get("yemek", b.get("beslenme", ""))).lower()
                          or "red" in str(b.get("yemek", b.get("beslenme", ""))).lower())
        if yemek_kotu >= 3:
            uyarilar.append({"ogrenci": ogr_ad, "sid": sid, "seviye": "yuksek", "ikon": "🍽️",
                              "sorun": f"Son 14 gunde {yemek_kotu} kez yemek sorunu",
                              "oneri": "Veli ile beslenme gorusmesi planlayin", "sorumlu": "Ogretmen + Saglik"})

        # 2. Uyku sorunu
        uyku_kotu = sum(1 for b in blist if "kotu" in str(b.get("uyku", b.get("uyku_durumu", ""))).lower()
                         or "uyumadi" in str(b.get("uyku", b.get("uyku_durumu", ""))).lower()
                         or "huzursuz" in str(b.get("uyku", b.get("uyku_durumu", ""))).lower())
        if uyku_kotu >= 3:
            uyarilar.append({"ogrenci": ogr_ad, "sid": sid, "seviye": "yuksek", "ikon": "😴",
                              "sorun": f"Son 14 gunde {uyku_kotu} kez uyku sorunu",
                              "oneri": "Uyku duzeni hakkinda veli bilgilendirme", "sorumlu": "Ogretmen + Veli"})

        # 3. Ruh hali
        uzgun = sum(1 for b in blist if "uzgun" in str(b.get("ruh_hali", b.get("duygu", b.get("genel_durum", "")))).lower()
                     or "aglamali" in str(b.get("ruh_hali", b.get("duygu", ""))).lower()
                     or "mutsuz" in str(b.get("ruh_hali", b.get("duygu", ""))).lower())
        if uzgun >= 3:
            uyarilar.append({"ogrenci": ogr_ad, "sid": sid, "seviye": "acil", "ikon": "😢",
                              "sorun": f"Son 14 gunde {uzgun} kez uzgun/mutsuz ruh hali",
                              "oneri": "Rehberlik gorusmesi acil planlayin", "sorumlu": "Rehberlik"})

        # 4. Sosyal
        yalniz = sum(1 for b in blist if "yalniz" in str(b.get("sosyal", b.get("oyun", ""))).lower()
                      or "tek" in str(b.get("sosyal", b.get("oyun", ""))).lower())
        if yalniz >= 3:
            uyarilar.append({"ogrenci": ogr_ad, "sid": sid, "seviye": "normal", "ikon": "👤",
                              "sorun": f"Son 14 gunde {yalniz} kez yalniz oyun tercihi",
                              "oneri": "Grup aktivitesine yonlendirin", "sorumlu": "Ogretmen"})

    # Render
    acil = sum(1 for u in uyarilar if u["seviye"] == "acil")
    yuksek = sum(1 for u in uyarilar if u["seviye"] == "yuksek")

    styled_stat_row([
        ("Taranan Ogrenci", str(len(ogr_bultenler)), "#2563eb", "👤"),
        ("Taranan Bulten", str(len(son_bultenler)), "#7c3aed", "📝"),
        ("Toplam Uyari", str(len(uyarilar)), "#f59e0b", "⚠️"),
        ("Acil", str(acil), "#ef4444", "🚨"),
    ])

    if not uyarilar:
        st.success("Harika! Son 14 gunde gelisim uyarisi tespit edilmedi.")
        return

    seviye_renk = {"acil": "#ef4444", "yuksek": "#f97316", "normal": "#f59e0b"}
    seviye_bg = {"acil": "#450a0a", "yuksek": "#431407", "normal": "#422006"}

    for u in sorted(uyarilar, key=lambda x: {"acil": 0, "yuksek": 1, "normal": 2}[x["seviye"]]):
        renk = seviye_renk.get(u["seviye"], "#64748b")
        bg = seviye_bg.get(u["seviye"], "#0f172a")
        st.markdown(f"""
        <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                    border-radius:0 14px 14px 0;padding:12px 16px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="font-size:16px;">{u['ikon']}</span>
                <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{u['ogrenci']}</span>
                <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                            font-size:9px;font-weight:700;margin-left:auto;">{u['seviye'].upper()}</span>
            </div>
            <div style="font-size:12px;color:#94a3b8;margin-bottom:4px;">{u['sorun']}</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:6px 10px;">
                <span style="font-size:11px;color:{renk};font-weight:700;">Oneri:</span>
                <span style="font-size:11px;color:#cbd5e1;"> {u['oneri']}</span>
                <span style="font-size:10px;color:#64748b;margin-left:8px;">({u['sorumlu']})</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # AI toplu analiz
    st.divider()
    if st.button("AI Toplu Gelisim Analizi", key="egu_ai", type="primary"):
        try:
            from utils.smarti_helper import _get_client
            client = _get_client()
            if client:
                uyari_ozet = "\n".join(f"- {u['ogrenci']}: {u['sorun']} ({u['seviye']})" for u in uyarilar[:15])
                with st.spinner("AI analiz ediyor..."):
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Sen bir okul oncesi gelisim uzmanisin. Verilen uyarilari analiz et. Genel degerlendirme + oncelikli mudahale plani + veli iletisim onerileri sun. Turkce, kisa."},
                            {"role": "user", "content": f"Uyarilar:\n{uyari_ozet}"},
                        ],
                        max_tokens=500, temperature=0.7,
                    )
                    ai = resp.choices[0].message.content or ""
                if ai:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#450a0a,#7f1d1d);border:1px solid #ef4444;
                                border-radius:14px;padding:16px 20px;">
                        <div style="font-size:12px;color:#fca5a5;font-weight:700;margin-bottom:6px;">AI Gelisim Analizi</div>
                        <div style="font-size:12px;color:#fecaca;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("OpenAI API bulunamadi.")
        except Exception as e:
            st.error(f"Hata: {e}")
