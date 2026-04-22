"""
AI Bireysel Eğitim — Final Özellikler
=======================================
1. Veli Koçluk Paneli & Evde Destek Rehberi
2. Sınıf Bazlı AI Öğretmen Cockpit & Müdahale
3. Çapraz Modül Öğrenme Ekosistemi & Birleşik Puan
"""
from __future__ import annotations
import json, os, uuid, random
from collections import Counter, defaultdict
from datetime import datetime, date, timedelta
import streamlit as st
from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_sinif_sube_listesi
from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

def _dd():
    d = os.path.join(get_tenant_dir(), "ai_bireysel"); os.makedirs(d, exist_ok=True); return d
def _lj(n):
    p = os.path.join(_dd(), n)
    if not os.path.exists(p): return []
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return []
def _sj(n, d):
    with open(os.path.join(_dd(), n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
def _ogr_sec(key):
    students = load_shared_students()
    if not students: st.warning("Ogrenci verisi yok."); return None
    opts = ["-- Secin --"] + [f"{s.get('ad','')} {s.get('soyad','')} - {s.get('sinif','')}/{s.get('sube','')}" for s in students]
    idx = st.selectbox("Ogrenci", range(len(opts)), format_func=lambda i: opts[i], key=key)
    return students[idx - 1] if idx > 0 else None

_MIKRO_GOREVLER = [
    "Bu aksam cocugunuza 'Bugün okulda ne öğrendin?' diye sorun.",
    "Birlikte 15 dk sessiz okuma zamani yapin.",
    "Cocugunuzla bugunku derslerden birini tartışın.",
    "Matematikten bir günlük hayat problemi birlikte çözün.",
    "Cocugunuzun calısma masasını birlikte düzenleyin.",
    "Yarınki ders için birlikte hazırlık yapın.",
    "Cocugunuzun basardigini birsey icin onu takdir edin.",
    "Cocugunuzla Ingilizce bir sarkı birlikte dinleyin.",
    "Bugünkü ödevleri birlikte kontrol edin.",
    "Cocugunuza 'Sana nasıl yardımcı olabilirim?' diye sorun.",
]

_ENDEKS_BOYUTLARI = {
    "Akademik": {"ikon": "📚", "renk": "#3b82f6", "agirlik": 30},
    "Dijital": {"ikon": "💻", "renk": "#8b5cf6", "agirlik": 20},
    "Sosyal": {"ikon": "👥", "renk": "#10b981", "agirlik": 20},
    "Duygusal": {"ikon": "🧠", "renk": "#f59e0b", "agirlik": 15},
    "Motivasyon": {"ikon": "🔥", "renk": "#ef4444", "agirlik": 15},
}


# ════════════════════════════════════════════════════════════
# 1. VELİ KOÇLUK PANELİ & EVDE DESTEK REHBERİ
# ════════════════════════════════════════════════════════════

def render_veli_kocluk():
    """Veli Koçluk Paneli — çocuk verileri, mikro görev, ebeveyn notu."""
    styled_section("Veli Kocluk Paneli & Evde Destek Rehberi", "#059669")
    styled_info_banner(
        "Cocugunuzun tum AI bireysel egitim verilerini gorun. "
        "Gunluk mikro-gorev, evde destek ipuclari, ogretmen senkronizasyonu.",
        banner_type="info", icon="👨‍👩‍👧")

    calisma = _lj("calisma_log.json")
    quest = _lj("quest_log.json")
    odevler = _lj("ai_odevler.json")
    veli_notlari = _lj("veli_notlari.json")

    sub = st.tabs(["📊 Cocuk Ozeti", "📝 Mikro Gorev", "💬 Veli Notu", "📚 Evde Destek", "📈 Haftalik Rapor"])

    # ── ÇOCUK ÖZETİ ──
    with sub[0]:
        styled_section("Cocugunuzun Haftalik Ozeti")
        ogr = _ogr_sec("vk_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()

            hafta_cal = [c for c in calisma if c.get("ogrenci") == ogr_ad and c.get("tarih","")[:10] >= bu_hafta]
            hafta_quest = [q for q in quest if q.get("ogrenci") == ogr_ad and q.get("tarih","")[:10] >= bu_hafta]
            aktif_odev = [o for o in odevler if o.get("ogrenci") == ogr_ad and o.get("durum") in ("Atandi","Baslandi")]
            tamamlanan_odev = [o for o in odevler if o.get("ogrenci") == ogr_ad and o.get("durum") in ("Teslim Edildi","Degerlendirildi")]

            toplam_dk = sum(c.get("sure_dk", 0) for c in hafta_cal)
            quest_xp = sum(q.get("xp", 0) for q in hafta_quest)

            # Streak
            streak = 0
            gun = date.today()
            while True:
                if any(c.get("tarih","")[:10] == gun.isoformat() for c in calisma if c.get("ogrenci") == ogr_ad):
                    streak += 1; gun -= timedelta(days=1)
                else: break

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#05966920);border:2px solid #059669;
                border-radius:20px;padding:24px 28px;margin:10px 0;">
                <div style="text-align:center;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1.2rem;">👨‍👩‍👧 {ogr_ad}</div>
                    <div style="color:#6ee7b7;font-size:0.8rem;">Bu Haftanin Ozeti</div>
                </div>
                <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;flex-wrap:wrap;">
                    <div style="text-align:center;">
                        <div style="color:#059669;font-weight:900;font-size:1.8rem;">{toplam_dk}</div>
                        <div style="color:#64748b;font-size:0.62rem;">dakika calisma</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#c9a84c;font-weight:900;font-size:1.8rem;">{quest_xp}</div>
                        <div style="color:#64748b;font-size:0.62rem;">XP kazandi</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#ef4444;font-weight:900;font-size:1.8rem;">{streak}🔥</div>
                        <div style="color:#64748b;font-size:0.62rem;">gun streak</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#3b82f6;font-weight:900;font-size:1.8rem;">{len(tamamlanan_odev)}</div>
                        <div style="color:#64748b;font-size:0.62rem;">odev tamamladi</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#f59e0b;font-weight:900;font-size:1.8rem;">{len(aktif_odev)}</div>
                        <div style="color:#64748b;font-size:0.62rem;">bekleyen odev</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Ders dagilimi
            if hafta_cal:
                styled_section("Ders Bazli Calisma")
                ders_dk = defaultdict(int)
                for c in hafta_cal:
                    ders_dk[c.get("ders","")] += c.get("sure_dk", 0)
                for ders, dk in sorted(ders_dk.items(), key=lambda x: x[1], reverse=True):
                    pct = round(dk / max(toplam_dk, 1) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:8px;margin:3px 0;">
                        <span style="min-width:100px;color:#e2e8f0;font-weight:600;font-size:0.78rem;">{ders}</span>
                        <div style="flex:1;background:#1e293b;border-radius:4px;height:12px;overflow:hidden;">
                            <div style="width:{pct}%;height:100%;background:#059669;border-radius:4px;"></div>
                        </div>
                        <span style="font-size:0.65rem;color:#64748b;">{dk} dk</span>
                    </div>""", unsafe_allow_html=True)

    # ── MİKRO GÖREV ──
    with sub[1]:
        styled_section("Bugunun Mikro Gorevi")
        random.seed(hash(date.today().isoformat()))
        bugun_gorev = random.choice(_MIKRO_GOREVLER)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#05966915,#10b98110);border:2px solid #059669;
            border-radius:16px;padding:20px 24px;text-align:center;margin:14px 0;">
            <div style="font-size:2rem;">💡</div>
            <div style="color:#e2e8f0;font-weight:700;font-size:1rem;margin-top:8px;">
                {bugun_gorev}</div>
            <div style="color:#64748b;font-size:0.72rem;margin-top:6px;">
                Sadece 3 dakikanizi alir — cocugunuzun motivasyonunu arttirir!</div>
        </div>""", unsafe_allow_html=True)

        styled_section("Diger Oneriler")
        for g in _MIKRO_GOREVLER:
            if g != bugun_gorev:
                st.markdown(f"- 💡 {g}")

    # ── VELİ NOTU ──
    with sub[2]:
        styled_section("Evdeki Gozleminizi Paylasın")
        with st.form("veli_not_form"):
            vn_ogr = _ogr_sec("vk_not_ogr")
            vn_not = st.text_area("Gozleminiz / Notunuz", height=80, key="vk_not",
                placeholder="Evde motivasyonu dusuk gorunuyor... / Bu hafta cok calisti...")
            vn_tip = st.selectbox("Not Tipi",
                ["Genel Gozlem", "Motivasyon", "Calisma Aliskanligi", "Saglik", "Sosyal Durum", "Oneri"], key="vk_tip")

            if st.form_submit_button("Notu Kaydet", use_container_width=True):
                if vn_ogr and vn_not:
                    ogr_ad = f"{vn_ogr.get('ad','')} {vn_ogr.get('soyad','')}"
                    veli_notlari.append({
                        "ogrenci": ogr_ad, "not": vn_not, "tip": vn_tip,
                        "kaynak": "Veli", "tarih": datetime.now().isoformat(),
                    })
                    _sj("veli_notlari.json", veli_notlari)
                    st.success("Notunuz ogretmenle paylasildi!")
                    st.rerun()

        if veli_notlari:
            styled_section("Gecmis Notlar")
            for n in sorted(veli_notlari, key=lambda x: x.get("tarih",""), reverse=True)[:5]:
                st.markdown(f"""
                <div style="padding:6px 12px;margin:3px 0;background:#0f172a;
                    border-left:3px solid #059669;border-radius:0 8px 8px 0;">
                    <span style="color:#10b981;font-size:0.68rem;">{n.get('tip','')}</span>
                    <span style="color:#e2e8f0;font-size:0.75rem;margin-left:8px;">{n.get('not','')[:80]}</span>
                    <span style="color:#64748b;font-size:0.6rem;float:right;">{n.get('tarih','')[:10]}</span>
                </div>""", unsafe_allow_html=True)

    # ── EVDE DESTEK ──
    with sub[3]:
        styled_section("Evde Destek Ipuclari")
        ipuclari = [
            ("📅 Duzeni Saglayın", "Her gun ayni saatte calisma rutini olusturun.", "#3b82f6"),
            ("🚫 Dikkat Dagiticilarsi", "Calisma sirasinda telefon/tablet uzak tutun.", "#ef4444"),
            ("🎯 Kucuk Hedefler", "Buyuk hedefleri kucuk parcalara bolun.", "#f59e0b"),
            ("👏 Takdir Edin", "Basarilari ne kadar kucuk olursa olsun kutlayin.", "#10b981"),
            ("😊 Baski Yapmayin", "Motivasyonu destekleyin, ceza/baski degil.", "#8b5cf6"),
            ("🍎 Beslenme & Uyku", "Yeterli uyku ve saglikli beslenme basarinin temelidir.", "#059669"),
            ("💬 Acik Iletisim", "Cocugunuzla duygulari hakkında konusun.", "#0891b2"),
            ("📚 Birlikte Okuyun", "Okuma aliskanligini birlikte yapin.", "#c9a84c"),
        ]
        for baslik, aciklama, renk in ipuclari:
            st.markdown(f"""
            <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                border-radius:0 10px 10px 0;padding:8px 14px;margin:5px 0;">
                <span style="color:{renk};font-weight:800;font-size:0.82rem;">{baslik}</span>
                <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{aciklama}</div>
            </div>""", unsafe_allow_html=True)

    # ── HAFTALIK RAPOR ──
    with sub[4]:
        styled_section("Haftalik Veli Raporu")
        ogr2 = _ogr_sec("vk_rap_ogr")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
            h_cal = [c for c in calisma if c.get("ogrenci") == ogr_ad2 and c.get("tarih","")[:10] >= bu_hafta]
            h_dk = sum(c.get("sure_dk", 0) for c in h_cal)
            h_quest = sum(q.get("xp",0) for q in quest if q.get("ogrenci") == ogr_ad2 and q.get("tarih","")[:10] >= bu_hafta)

            st.markdown(f"""
            <div style="background:#0f172a;border:2px solid #059669;border-radius:16px;padding:20px 24px;">
                <div style="text-align:center;">
                    <div style="color:#e2e8f0;font-weight:900;font-size:1rem;">📨 Haftalik Rapor</div>
                    <div style="color:#6ee7b7;font-size:0.8rem;">{ogr_ad2}</div>
                    <div style="display:flex;justify-content:center;gap:30px;margin-top:12px;">
                        <div><div style="color:#059669;font-weight:900;font-size:1.5rem;">{h_dk}</div><div style="color:#64748b;font-size:0.62rem;">dakika</div></div>
                        <div><div style="color:#c9a84c;font-weight:900;font-size:1.5rem;">{h_quest}</div><div style="color:#64748b;font-size:0.62rem;">XP</div></div>
                        <div><div style="color:#3b82f6;font-weight:900;font-size:1.5rem;">{len(h_cal)}</div><div style="color:#64748b;font-size:0.62rem;">oturum</div></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 2. SINIF BAZLI AI ÖĞRETMEN COCKPİT & MÜDAHALE
# ════════════════════════════════════════════════════════════

def render_ai_cockpit():
    """Sınıf Bazlı AI Öğretmen Cockpit — trafik ışığı, ısı haritası, müdahale."""
    styled_section("Sinif Bazli AI Ogretmen Cockpit", "#2563eb")
    styled_info_banner(
        "Tum sinifi tek bakista gorun: yesil/sari/kirmizi trafik isigi. "
        "Konu bazli isi haritasi, bireysel mudahale onerisi.",
        banner_type="info", icon="🏫")

    calisma = _lj("calisma_log.json")
    konu_puanlari = _lj("konu_puanlari.json")
    odevler = _lj("ai_odevler.json")
    quest = _lj("quest_log.json")

    students = load_shared_students()

    sub = st.tabs(["🚦 Trafik Isigi", "🌡️ Konu Isi Haritasi", "💡 Mudahale Onerisi", "📊 Sinif Ozeti"])

    # ── TRAFİK IŞIĞI ──
    with sub[0]:
        styled_section("Sinif Trafik Isigi — Ogrenci Durumu")

        ss = get_sinif_sube_listesi()
        siniflar = ["Tumu"] + ss.get("siniflar", [])
        sec_sinif = st.selectbox("Sinif", siniflar, key="ck_sinif")

        filtered = students
        if sec_sinif != "Tumu":
            filtered = [s for s in students if str(s.get("sinif","")) == sec_sinif]

        if not filtered:
            st.info("Ogrenci yok.")
        else:
            bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()
            yesil, sari, kirmizi = 0, 0, 0
            ogr_durumlar = []

            for s in filtered[:50]:
                ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
                h_cal = sum(c.get("sure_dk",0) for c in calisma
                    if c.get("ogrenci") == ogr_ad and c.get("tarih","")[:10] >= bu_hafta)
                h_odev = sum(1 for o in odevler
                    if o.get("ogrenci") == ogr_ad and o.get("durum") in ("Teslim Edildi","Degerlendirildi")
                    and o.get("created_at","")[:10] >= bu_hafta)
                h_quest = sum(1 for q in quest
                    if q.get("ogrenci") == ogr_ad and q.get("tarih","")[:10] >= bu_hafta)

                skor = h_cal // 10 + h_odev * 5 + h_quest * 3
                if skor >= 15:
                    durum, renk, ikon = "Yolunda", "#10b981", "🟢"
                    yesil += 1
                elif skor >= 5:
                    durum, renk, ikon = "Dikkat", "#f59e0b", "🟡"
                    sari += 1
                else:
                    durum, renk, ikon = "Mudahale", "#ef4444", "🔴"
                    kirmizi += 1

                ogr_durumlar.append({"ad": ogr_ad, "sinif": f"{s.get('sinif','')}/{s.get('sube','')}",
                    "durum": durum, "renk": renk, "ikon": ikon, "skor": skor,
                    "dk": h_cal, "odev": h_odev, "quest": h_quest})

            styled_stat_row([
                ("Yesil", str(yesil), "#10b981", "🟢"),
                ("Sari", str(sari), "#f59e0b", "🟡"),
                ("Kirmizi", str(kirmizi), "#ef4444", "🔴"),
                ("Toplam", str(len(ogr_durumlar)), "#3b82f6", "👥"),
            ])

            # Liste
            for o in sorted(ogr_durumlar, key=lambda x: x["skor"]):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:4px solid {o['renk']};border-radius:0 8px 8px 0;">
                    <span style="font-size:0.9rem;">{o['ikon']}</span>
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{o['ad']}</span>
                    <span style="color:#64748b;font-size:0.65rem;">{o['sinif']}</span>
                    <span style="color:#94a3b8;font-size:0.62rem;">{o['dk']}dk | {o['odev']}ödev | {o['quest']}quest</span>
                    <span style="background:{o['renk']}20;color:{o['renk']};padding:2px 6px;border-radius:4px;
                        font-size:0.6rem;font-weight:700;">{o['durum']}</span>
                </div>""", unsafe_allow_html=True)

    # ── KONU ISI HARİTASI ──
    with sub[1]:
        styled_section("Konu Bazli Sinif Isi Haritasi")
        if not konu_puanlari:
            st.info("Konu puani verisi yok.")
        else:
            ders_grp = defaultdict(lambda: defaultdict(list))
            for k in konu_puanlari:
                ders_grp[k.get("ders","")][k.get("konu","")] .append(k.get("puan", 50))

            for ders, konular in sorted(ders_grp.items()):
                st.markdown(f"**📚 {ders}**")
                for konu, puanlar in sorted(konular.items(), key=lambda x: sum(x[1])/len(x[1])):
                    ort = round(sum(puanlar) / max(len(puanlar), 1))
                    renk = "#10b981" if ort >= 70 else "#f59e0b" if ort >= 50 else "#ef4444"
                    zorlanma = round((1 - ort / 100) * 100)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:6px;margin:2px 0;padding-left:16px;">
                        <span style="min-width:100px;color:#e2e8f0;font-size:0.72rem;">{konu}</span>
                        <div style="flex:1;background:#1e293b;border-radius:3px;height:10px;overflow:hidden;">
                            <div style="width:{zorlanma}%;height:100%;background:{renk};border-radius:3px;"></div>
                        </div>
                        <span style="color:{renk};font-size:0.6rem;font-weight:700;">%{zorlanma} zorlanma</span>
                    </div>""", unsafe_allow_html=True)

    # ── MÜDAHALE ÖNERİSİ ──
    with sub[2]:
        styled_section("Bireysel Mudahale Onerileri")
        bu_hafta = (date.today() - timedelta(days=date.today().weekday())).isoformat()

        oneriler = []
        for s in students[:30]:
            ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
            h_cal = sum(c.get("sure_dk",0) for c in calisma
                if c.get("ogrenci") == ogr_ad and c.get("tarih","")[:10] >= bu_hafta)
            geciken_odev = sum(1 for o in odevler if o.get("ogrenci") == ogr_ad and o.get("durum") == "Gecikti")

            if h_cal == 0:
                oneriler.append((ogr_ad, "Bu hafta hic calismamis — motivasyon gorusmesi yapın", "#ef4444", "🔴"))
            elif geciken_odev > 0:
                oneriler.append((ogr_ad, f"{geciken_odev} geciken odevi var — takip edin", "#f59e0b", "⏰"))
            elif h_cal < 30:
                oneriler.append((ogr_ad, "Calisma suresi cok dusuk — ekstra destek onerilir", "#f59e0b", "📌"))

        if not oneriler:
            st.success("Acil mudahale gerektiren ogrenci yok!")
        else:
            st.warning(f"{len(oneriler)} ogrenci icin mudahale onerilir:")
            for ad, mesaj, renk, ikon in oneriler:
                st.markdown(f"""
                <div style="background:{renk}08;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:8px 14px;margin:4px 0;">
                    <span style="color:{renk};font-weight:800;">{ikon} {ad}</span>
                    <div style="color:#e2e8f0;font-size:0.75rem;margin-top:2px;">{mesaj}</div>
                </div>""", unsafe_allow_html=True)

    # ── SINIF ÖZETİ ──
    with sub[3]:
        styled_section("Sinif Genel Ozet")
        if not calisma:
            st.info("Calisma verisi yok.")
        else:
            toplam_dk = sum(c.get("sure_dk",0) for c in calisma)
            aktif_ogr = len(set(c.get("ogrenci","") for c in calisma))
            ders_say = len(set(c.get("ders","") for c in calisma))

            styled_stat_row([
                ("Toplam Calisma", f"{toplam_dk} dk", "#2563eb", "⏱️"),
                ("Aktif Ogrenci", str(aktif_ogr), "#10b981", "👥"),
                ("Ders Cesitliligi", str(ders_say), "#8b5cf6", "📚"),
                ("Toplam Odev", str(len(odevler)), "#f59e0b", "📋"),
            ])


# ════════════════════════════════════════════════════════════
# 3. ÇAPRAZ MODÜL ÖĞRENME EKOSİSTEMİ & BİRLEŞİK PUAN
# ════════════════════════════════════════════════════════════

def _hesapla_ogrenme_endeksi(ogr_ad: str) -> dict:
    """Tüm modüllerden birleşik Öğrenme Gücü Endeksi hesapla."""
    calisma = _lj("calisma_log.json")
    quest = _lj("quest_log.json")
    odevler = _lj("ai_odevler.json")
    konu_puanlari = _lj("konu_puanlari.json")

    # Akademik
    ogr_kp = [k.get("puan", 50) for k in konu_puanlari if k.get("ogrenci") == ogr_ad]
    akademik = round(sum(ogr_kp) / max(len(ogr_kp), 1)) if ogr_kp else 50

    # Dijital
    ogr_cal = [c for c in calisma if c.get("ogrenci") == ogr_ad]
    toplam_dk = sum(c.get("sure_dk", 0) for c in ogr_cal)
    dijital = min(100, toplam_dk // 3)  # 300dk = 100

    # Sosyal (cross-module: sosyal etkinlik)
    try:
        sd = os.path.join(get_tenant_dir(), "sosyal_etkinlik")
        katilim_path = os.path.join(sd, "kulup_katilim.json")
        if os.path.exists(katilim_path):
            with open(katilim_path, "r", encoding="utf-8") as f:
                katilim = json.load(f)
            sosyal_sayi = sum(1 for k in katilim if ogr_ad in k.get("katilanlar", []))
            sosyal = min(100, sosyal_sayi * 8)
        else:
            sosyal = 40
    except Exception:
        sosyal = 40

    # Duygusal (cross-module: rehberlik)
    try:
        rd = os.path.join(get_tenant_dir(), "rehberlik")
        duygu_path = os.path.join(rd, "sosyo_duygusal.json")
        if os.path.exists(duygu_path):
            with open(duygu_path, "r", encoding="utf-8") as f:
                duygusal_data = json.load(f)
            _mp = {"Cok Mutlu": 5, "Mutlu": 4, "Normal": 3, "Mutsuz": 2, "Cok Mutsuz": 1, "Ofkeli": 1, "Kaygili": 2}
            ogr_duygu = [_mp.get(d.get("duygu","Normal"), 3) for d in duygusal_data if d.get("ogrenci_ad","").startswith(ogr_ad.split()[0])]
            duygusal = round(sum(ogr_duygu) / max(len(ogr_duygu), 1) / 5 * 100) if ogr_duygu else 60
        else:
            duygusal = 60
    except Exception:
        duygusal = 60

    # Motivasyon
    ogr_quest = sum(q.get("xp", 0) for q in quest if q.get("ogrenci") == ogr_ad)
    ogr_odev_ok = sum(1 for o in odevler if o.get("ogrenci") == ogr_ad and o.get("durum") in ("Teslim Edildi","Degerlendirildi"))
    motivasyon = min(100, ogr_quest // 3 + ogr_odev_ok * 10)

    # Genel
    boyutlar = {"Akademik": akademik, "Dijital": dijital, "Sosyal": sosyal,
                "Duygusal": duygusal, "Motivasyon": motivasyon}

    genel = 0
    for boyut, info in _ENDEKS_BOYUTLARI.items():
        genel += boyutlar.get(boyut, 50) * info["agirlik"] / 100

    return {"genel": round(genel), "boyutlar": boyutlar}


def render_ogrenme_ekosistemi():
    """Çapraz Modül Öğrenme Ekosistemi — birleşik Öğrenme Gücü Endeksi."""
    styled_section("Capraz Modul Ogrenme Ekosistemi", "#6366f1")
    styled_info_banner(
        "AI Bireysel Egitim + Olcme Degerlendirme + Dijital Kutuphane + Rehberlik "
        "verilerinden birlesik 'Ogrenme Gucu Endeksi' (0-100).",
        banner_type="info", icon="🌐")

    sub = st.tabs(["👤 Bireysel Endeks", "🏫 Sinif Haritasi", "📈 Trend", "📊 Boyut Analizi"])

    # ── BİREYSEL ENDEKS ──
    with sub[0]:
        styled_section("Ogrenci Ogrenme Gucu Endeksi")
        ogr = _ogr_sec("oe_ogr")
        if ogr:
            ogr_ad = f"{ogr.get('ad','')} {ogr.get('soyad','')}"
            endeks = _hesapla_ogrenme_endeksi(ogr_ad)
            genel = endeks["genel"]

            g_renk = "#10b981" if genel >= 75 else "#f59e0b" if genel >= 50 else "#ef4444"
            harf = "A+" if genel >= 95 else "A" if genel >= 85 else "B+" if genel >= 75 else "B" if genel >= 65 else "C" if genel >= 50 else "D" if genel >= 35 else "F"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b,{g_renk}15);border:3px solid {g_renk};
                border-radius:22px;padding:28px 32px;text-align:center;margin:10px 0;">
                <div style="color:#e2e8f0;font-weight:900;font-size:1.1rem;">{ogr_ad}</div>
                <div style="color:#94a3b8;font-size:0.8rem;">Ogrenme Gucu Endeksi</div>
                <div style="display:flex;justify-content:center;align-items:baseline;gap:14px;margin-top:8px;">
                    <span style="color:{g_renk};font-weight:900;font-size:4rem;">{harf}</span>
                    <span style="color:{g_renk};font-weight:700;font-size:1.8rem;">{genel}/100</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # Boyutlar
            styled_section("Boyut Bazli Analiz")
            for boyut, info in _ENDEKS_BOYUTLARI.items():
                puan = endeks["boyutlar"].get(boyut, 50)
                renk = "#10b981" if puan >= 70 else "#f59e0b" if puan >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin:8px 0;">
                    <span style="font-size:1.2rem;">{info['ikon']}</span>
                    <span style="min-width:85px;color:#e2e8f0;font-weight:700;font-size:0.82rem;">{boyut}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:22px;overflow:hidden;">
                        <div style="width:{puan}%;height:100%;background:linear-gradient(90deg,{info['renk']},{renk});
                            border-radius:6px;display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:0.65rem;color:#fff;font-weight:800;">{puan}/100</span>
                        </div>
                    </div>
                    <span style="font-size:0.65rem;color:#64748b;">{info['agirlik']}%</span>
                </div>""", unsafe_allow_html=True)

            en_zayif = min(endeks["boyutlar"], key=endeks["boyutlar"].get)
            st.warning(f"En zayif boyut: **{en_zayif}** ({endeks['boyutlar'][en_zayif]}/100) — bu alani iyilestirmek endeksi en cok arttirir.")

    # ── SINIF HARİTASI ──
    with sub[1]:
        styled_section("Sinif Bazli Ogrenme Gucu")
        students = load_shared_students()
        if not students:
            st.info("Ogrenci yok.")
        else:
            ss = get_sinif_sube_listesi()
            sec_s = st.selectbox("Sinif", ["Tumu"] + ss.get("siniflar", []), key="oe_sinif")
            filtered = students if sec_s == "Tumu" else [s for s in students if str(s.get("sinif","")) == sec_s]

            endeks_list = []
            for s in filtered[:40]:
                ogr_ad = f"{s.get('ad','')} {s.get('soyad','')}"
                e = _hesapla_ogrenme_endeksi(ogr_ad)
                endeks_list.append({"ad": ogr_ad, "sinif": f"{s.get('sinif','')}/{s.get('sube','')}", "genel": e["genel"]})

            endeks_list.sort(key=lambda x: x["genel"], reverse=True)

            yesil = sum(1 for e in endeks_list if e["genel"] >= 70)
            sari = sum(1 for e in endeks_list if 50 <= e["genel"] < 70)
            kirmizi = sum(1 for e in endeks_list if e["genel"] < 50)

            styled_stat_row([
                ("Guclu (70+)", str(yesil), "#10b981", "🟢"),
                ("Orta (50-69)", str(sari), "#f59e0b", "🟡"),
                ("Zayif (<50)", str(kirmizi), "#ef4444", "🔴"),
            ])

            for e in endeks_list[:20]:
                renk = "#10b981" if e["genel"] >= 70 else "#f59e0b" if e["genel"] >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:5px 12px;margin:2px 0;
                    background:#0f172a;border-left:4px solid {renk};border-radius:0 8px 8px 0;">
                    <span style="color:#e2e8f0;font-weight:700;font-size:0.78rem;flex:1;">{e['ad']}</span>
                    <span style="color:#64748b;font-size:0.65rem;">{e['sinif']}</span>
                    <span style="color:{renk};font-weight:800;font-size:0.78rem;">{e['genel']}/100</span>
                </div>""", unsafe_allow_html=True)

    # ── TREND ──
    with sub[2]:
        styled_section("Ogrenme Endeksi Trendi (Simule)")
        ogr2 = _ogr_sec("oe_ogr2")
        if ogr2:
            ogr_ad2 = f"{ogr2.get('ad','')} {ogr2.get('soyad','')}"
            endeks2 = _hesapla_ogrenme_endeksi(ogr_ad2)
            genel2 = endeks2["genel"]

            for i in range(5, -1, -1):
                ay = date.today().replace(day=1) - timedelta(days=30*i)
                sim = max(20, min(95, genel2 + random.randint(-10, 8)))
                renk = "#10b981" if sim >= 70 else "#f59e0b" if sim >= 50 else "#ef4444"
                is_bu = i == 0
                ay_ad = {1:"Oca",2:"Sub",3:"Mar",4:"Nis",5:"May",6:"Haz",7:"Tem",8:"Agu",9:"Eyl",10:"Eki",11:"Kas",12:"Ara"}
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:4px 0;
                    {'border-left:3px solid #c9a84c;padding-left:8px;' if is_bu else ''}">
                    <span style="min-width:35px;font-size:0.72rem;color:{'#c9a84c' if is_bu else '#94a3b8'};">{ay_ad.get(ay.month,'')}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{sim}%;height:100%;background:{renk};border-radius:4px;
                            display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:0.6rem;color:#fff;font-weight:700;">{sim}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ── BOYUT ANALİZİ ──
    with sub[3]:
        styled_section("Boyut Aciklamalari & Veri Kaynaklari")
        for boyut, info in _ENDEKS_BOYUTLARI.items():
            kaynaklar = {
                "Akademik": "Konu puanlari, sinav sonuclari (Olcme Degerlendirme)",
                "Dijital": "Calisma suresi, AI etkilesim (AI Bireysel Egitim)",
                "Sosyal": "Kulup katilimi, etkinlik (Sosyal Etkinlik)",
                "Duygusal": "Duygu kayitlari, risk skoru (Rehberlik)",
                "Motivasyon": "Quest XP, odev tamamlama, streak",
            }
            st.markdown(f"""
            <div style="background:#0f172a;border-left:5px solid {info['renk']};border-radius:0 12px 12px 0;
                padding:10px 14px;margin:6px 0;">
                <span style="font-size:1.1rem;">{info['ikon']}</span>
                <span style="color:#e2e8f0;font-weight:800;font-size:0.85rem;margin-left:6px;">{boyut}</span>
                <span style="color:#64748b;font-size:0.7rem;margin-left:8px;">(agirlik: %{info['agirlik']})</span>
                <div style="color:#94a3b8;font-size:0.72rem;margin-top:4px;">
                    Kaynak: {kaynaklar.get(boyut, '')}</div>
            </div>""", unsafe_allow_html=True)
