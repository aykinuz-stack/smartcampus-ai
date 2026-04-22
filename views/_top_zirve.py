"""
Toplanti & Kurullar — Zirve Ozellikleri
=========================================
1. Toplanti Verimlilik Motoru + Maliyet Analizi
2. Akilli Karar & Aksiyon Takip Merkezi
3. Toplanti Zaman Makinesi + AI Kurumsal Hafiza
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


# ============================================================
# 1. VERİMLİLİK MOTORU + MALİYET ANALİZİ
# ============================================================

def render_verimlilik_motoru(store):
    """Toplanti verimlilik + maliyet analizi."""
    styled_section("Toplanti Verimlilik & Maliyet", "#f59e0b")
    styled_info_banner(
        "Her toplantinin verimliligini ve maliyetini olcun. "
        "Sure asimi, karar hizi, katilim orani, TL maliyet.",
        banner_type="info", icon="💰")

    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []
    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    participants = store.load_list("participants") if hasattr(store, "load_list") else []
    agenda = store.load_list("agenda_items") if hasattr(store, "load_list") else []

    yapilan = [m for m in meetings if m.get("durum") in ("YAPILDI", "TUTANAK_TAMAM", "ONAYLANDI")]

    # Genel istatistikler
    toplam_karar = len(decisions)
    toplam_aksiyon = len(gorevler)
    tamam_aksiyon = sum(1 for g in gorevler if g.get("durum") == "TAMAMLANDI")
    geciken = sum(1 for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")
                   and g.get("hedef_tarih", "") and g["hedef_tarih"] < date.today().isoformat())

    # Ortalama katilimci
    ort_katilimci = 0
    if yapilan:
        mtg_ids = set(m.get("id") for m in yapilan)
        katilim_sayilari = []
        for mid in mtg_ids:
            kat = sum(1 for p in participants if p.get("meeting_id") == mid and p.get("katilim_durumu") == "KATILDI")
            if kat > 0:
                katilim_sayilari.append(kat)
        ort_katilimci = round(sum(katilim_sayilari) / max(len(katilim_sayilari), 1), 1) if katilim_sayilari else 0

    # Maliyet (tahmini saat ucreti)
    SAAT_UCRETI = 120  # TL/saat (ortalama)
    toplam_maliyet = 0
    toplanti_maliyetleri = []
    for m in yapilan:
        sure_dk = m.get("sure_dk", 60)
        mid = m.get("id")
        kat_sayi = sum(1 for p in participants if p.get("meeting_id") == mid and p.get("katilim_durumu") == "KATILDI")
        if kat_sayi == 0:
            kat_sayi = ort_katilimci or 5
        maliyet = round(kat_sayi * (sure_dk / 60) * SAAT_UCRETI)
        toplam_maliyet += maliyet
        toplanti_maliyetleri.append({**m, "maliyet": maliyet, "katilimci": kat_sayi})

    # Karar/maliyet
    karar_basina = round(toplam_maliyet / max(toplam_karar, 1)) if toplam_karar else 0

    styled_stat_row([
        ("Yapilan Toplanti", str(len(yapilan)), "#f59e0b", "📅"),
        ("Toplam Karar", str(toplam_karar), "#2563eb", "📋"),
        ("Toplam Maliyet", f"{toplam_maliyet:,.0f} TL", "#ef4444", "💰"),
        ("Karar Basina", f"{karar_basina:,.0f} TL", "#7c3aed", "📊"),
        ("Geciken Aksiyon", str(geciken), "#dc2626", "⚠️"),
    ])

    # ── HERO ──
    verimlilik = round(tamam_aksiyon / max(toplam_aksiyon, 1) * 100, 1) if toplam_aksiyon else 0
    v_renk = "#10b981" if verimlilik >= 70 else "#f59e0b" if verimlilik >= 45 else "#ef4444"

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 100%);
                border:2px solid {v_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {v_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;">Aksiyon Tamamlanma Orani</div>
        <div style="font-size:56px;font-weight:900;color:{v_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">%{verimlilik}</div>
        <div style="font-size:12px;color:#fde68a;">
            {tamam_aksiyon}/{toplam_aksiyon} aksiyon · {geciken} geciken · Ort. {ort_katilimci} katilimci</div>
    </div>""", unsafe_allow_html=True)

    # ── TOPLANTI BAZLI MALİYET ──
    styled_section("Toplanti Bazli Maliyet Siralaması")
    toplanti_maliyetleri.sort(key=lambda x: -x["maliyet"])
    for i, m in enumerate(toplanti_maliyetleri[:15], 1):
        baslik = m.get("baslik", "Toplanti")
        tarih = m.get("tarih", "")[:10]
        sure = m.get("sure_dk", 60)
        maliyet = m["maliyet"]
        kat = m["katilimci"]
        # Karar sayisi
        mid = m.get("id")
        m_karar = sum(1 for d in decisions if d.get("meeting_id") == mid)
        renk = "#ef4444" if maliyet > 1000 else "#f59e0b" if maliyet > 500 else "#10b981"

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                    border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{baslik}</span>
                    <span style="color:#94a3b8;font-size:10px;margin-left:8px;">{tarih}</span>
                </div>
                <span style="background:{renk}20;color:{renk};padding:3px 12px;border-radius:8px;
                            font-size:12px;font-weight:800;">{maliyet:,.0f} TL</span>
            </div>
            <div style="font-size:10px;color:#64748b;margin-top:3px;">
                {kat} kisi · {sure} dk · {m_karar} karar · Karar basina: {round(maliyet / max(m_karar, 1)):,.0f} TL</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 2. KARAR & AKSİYON TAKİP MERKEZİ
# ============================================================

def render_karar_takip(store):
    """Tum toplantilarin kararlari ve aksiyonlari tek merkezde."""
    styled_section("Karar & Aksiyon Takip Merkezi", "#2563eb")
    styled_info_banner(
        "Tum toplantilardaki kararlar ve aksiyonlar. "
        "Geciken, bu hafta biten, sorumlu bazli yuk dagilimi.",
        banner_type="info", icon="🎯")

    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []

    bugun = date.today().isoformat()
    bu_hafta = (date.today() + timedelta(days=7)).isoformat()

    # Kategorize
    geciken = [g for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")
                and g.get("hedef_tarih", "") and g["hedef_tarih"] < bugun]
    bu_hafta_biten = [g for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")
                       and g.get("hedef_tarih", "") and bugun <= g["hedef_tarih"] <= bu_hafta]
    tamamlanan = [g for g in gorevler if g.get("durum") == "TAMAMLANDI"]
    acik = [g for g in gorevler if g.get("durum") in ("BEKLEMEDE", "DEVAM_EDIYOR")]

    styled_stat_row([
        ("Toplam Karar", str(len(decisions)), "#2563eb", "📋"),
        ("Toplam Aksiyon", str(len(gorevler)), "#7c3aed", "🎯"),
        ("Geciken", str(len(geciken)), "#ef4444", "🚨"),
        ("Bu Hafta Biten", str(len(bu_hafta_biten)), "#f59e0b", "⏰"),
        ("Tamamlanan", str(len(tamamlanan)), "#10b981", "✅"),
    ])

    sub = st.tabs(["🚨 Geciken", "⏰ Bu Hafta", "👤 Sorumlu Dagilimi", "📋 Tum Aksiyonlar"])

    # ═══ GECİKEN ═══
    with sub[0]:
        styled_section(f"Geciken Aksiyonlar ({len(geciken)})", "#ef4444")
        if not geciken:
            st.success("Geciken aksiyon yok!")
        else:
            for g in sorted(geciken, key=lambda x: x.get("hedef_tarih", "")):
                try:
                    gecikme_gun = (date.today() - date.fromisoformat(g["hedef_tarih"][:10])).days
                except Exception:
                    gecikme_gun = 0
                renk = "#ef4444" if gecikme_gun > 14 else "#f97316" if gecikme_gun > 7 else "#f59e0b"
                # Toplanti adi
                mtg = next((m for m in meetings if m.get("id") == g.get("meeting_id")), None)
                mtg_baslik = mtg.get("baslik", "?") if mtg else "?"

                st.markdown(f"""
                <div style="background:#450a0a;border:1px solid #ef4444;border-left:5px solid {renk};
                            border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#fca5a5;font-size:13px;">{g.get('gorev_tanimi', g.get('baslik', '?'))[:80]}</span>
                        <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:6px;
                                    font-size:10px;font-weight:700;">{gecikme_gun} gun gecikti</span>
                    </div>
                    <div style="font-size:10px;color:#fca5a5;margin-top:4px;">
                        Sorumlu: {g.get('sorumlu', '-')} · Hedef: {g.get('hedef_tarih', '-')[:10]} · Toplanti: {mtg_baslik[:40]}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ BU HAFTA ═══
    with sub[1]:
        styled_section(f"Bu Hafta Biten ({len(bu_hafta_biten)})", "#f59e0b")
        if not bu_hafta_biten:
            st.info("Bu hafta bitmesi gereken aksiyon yok.")
        else:
            for g in bu_hafta_biten:
                try:
                    kalan = (date.fromisoformat(g["hedef_tarih"][:10]) - date.today()).days
                except Exception:
                    kalan = 0
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #f59e0b30;border-left:4px solid #f59e0b;
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:600;color:#e2e8f0;font-size:12px;">{g.get('gorev_tanimi', g.get('baslik', '?'))[:80]}</span>
                        <span style="background:#f59e0b20;color:#f59e0b;padding:2px 8px;border-radius:6px;
                                    font-size:10px;font-weight:700;">{kalan} gun kaldi</span>
                    </div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:2px;">Sorumlu: {g.get('sorumlu', '-')}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ SORUMLU DAĞILIMI ═══
    with sub[2]:
        styled_section("Sorumlu Bazli Yuk Dagilimi")
        sorumlu_sayac = Counter()
        sorumlu_geciken = Counter()
        for g in acik:
            s = g.get("sorumlu", "Belirtilmedi")
            sorumlu_sayac[s] += 1
        for g in geciken:
            s = g.get("sorumlu", "Belirtilmedi")
            sorumlu_geciken[s] += 1

        if sorumlu_sayac:
            en_cok = sorumlu_sayac.most_common(1)[0][1]
            for kisi, sayi in sorumlu_sayac.most_common(15):
                geciken_s = sorumlu_geciken.get(kisi, 0)
                renk = "#ef4444" if geciken_s > 2 else "#f59e0b" if geciken_s > 0 else "#10b981"
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{kisi}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi} acik</span></div></div>
                    <span style="font-size:10px;color:#ef4444;min-width:50px;">{geciken_s} geciken</span>
                </div>""", unsafe_allow_html=True)

    # ═══ TÜM AKSİYONLAR ═══
    with sub[3]:
        styled_section("Tum Aksiyonlar")
        fil = st.selectbox("Durum Filtresi", ["Tumu", "Acik", "Geciken", "Tamamlanan"], key="kt_fil")
        filtered = gorevler
        if fil == "Acik":
            filtered = acik
        elif fil == "Geciken":
            filtered = geciken
        elif fil == "Tamamlanan":
            filtered = tamamlanan

        st.caption(f"{len(filtered)} aksiyon")
        rows = ""
        for g in sorted(filtered, key=lambda x: x.get("hedef_tarih", ""), reverse=True)[:30]:
            durum = g.get("durum", "?")
            d_renk = {"TAMAMLANDI": "#10b981", "BEKLEMEDE": "#3b82f6", "DEVAM_EDIYOR": "#f59e0b", "IPTAL": "#94a3b8"}.get(durum, "#64748b")
            rows += f"""<tr>
                <td style="padding:5px 8px;font-size:11px;color:#e2e8f0;font-weight:600;">{g.get('gorev_tanimi', g.get('baslik', ''))[:50]}</td>
                <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{g.get('sorumlu', '-')}</td>
                <td style="padding:5px 8px;font-size:11px;color:#94a3b8;">{g.get('hedef_tarih', '-')[:10]}</td>
                <td style="padding:5px 8px;"><span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;
                    border-radius:6px;font-size:9px;font-weight:700;">{durum}</span></td>
            </tr>"""
        if rows:
            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;">
            <thead><tr style="background:#1e293b;">
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Aksiyon</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Sorumlu</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Hedef</th>
                <th style="padding:6px 8px;text-align:left;color:#64748b;font-size:10px;">Durum</th>
            </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)


# ============================================================
# 3. TOPLANTI ZAMAN MAKİNESİ + AI HAFIZA
# ============================================================

def render_toplanti_hafiza(store):
    """Toplanti kararlari + tutanaklar — aranabilir kurumsal hafiza."""
    styled_section("Toplanti Kurumsal Hafizasi", "#7c3aed")
    styled_info_banner(
        "Tum toplanti tutanaklari, kararlari ve aksiyonlari aranabilir. "
        "Dogal dilde soru sorun, AI kurumsal hafizadan cevap versin.",
        banner_type="info", icon="🧠")

    meetings = store.load_list("meetings") if hasattr(store, "load_list") else []
    decisions = store.load_list("decisions") if hasattr(store, "load_list") else []
    gorevler = store.load_list("gorevler") if hasattr(store, "load_list") else []
    agenda = store.load_list("agenda_items") if hasattr(store, "load_list") else []
    kurullar = store.load_list("kurullar") if hasattr(store, "load_list") else []

    # Indeks olustur
    kayitlar = []
    for m in meetings:
        kayitlar.append({
            "tip": "Toplanti", "tarih": m.get("tarih", "")[:10],
            "baslik": m.get("baslik", ""), "detay": m.get("tutanak", "")[:300] if m.get("tutanak") else "",
            "id": m.get("id", ""), "kurul": m.get("kurul", ""),
        })
    for d in decisions:
        kayitlar.append({
            "tip": "Karar", "tarih": d.get("tarih", d.get("created_at", ""))[:10],
            "baslik": d.get("karar_metni", d.get("baslik", ""))[:200],
            "detay": d.get("aciklama", "")[:200],
            "id": d.get("id", ""), "kurul": "",
        })
    for g in gorevler:
        kayitlar.append({
            "tip": "Aksiyon", "tarih": g.get("created_at", g.get("hedef_tarih", ""))[:10],
            "baslik": g.get("gorev_tanimi", g.get("baslik", ""))[:200],
            "detay": f"Sorumlu: {g.get('sorumlu', '-')} · Durum: {g.get('durum', '-')}",
            "id": g.get("id", ""), "kurul": "",
        })
    for a in agenda:
        kayitlar.append({
            "tip": "Gundem", "tarih": a.get("created_at", "")[:10],
            "baslik": a.get("baslik", "")[:200],
            "detay": f"Sonuc: {a.get('sonuc', '-')}" if a.get("sonuc") else "",
            "id": a.get("id", ""), "kurul": "",
        })

    styled_stat_row([
        ("Toplanti", str(len(meetings)), "#7c3aed", "📅"),
        ("Karar", str(len(decisions)), "#2563eb", "📋"),
        ("Aksiyon", str(len(gorevler)), "#f59e0b", "🎯"),
        ("Gundem", str(len(agenda)), "#0891b2", "📝"),
        ("Hafiza Kaydi", str(len(kayitlar)), "#10b981", "🧠"),
    ])

    sub = st.tabs(["🔍 Arama", "🤖 AI Soru-Cevap", "📜 Kurul Gecmisi"])

    # ═══ ARAMA ═══
    with sub[0]:
        sorgu = st.text_input("Toplanti hafizasinda ara...", key="th_sorgu",
                               placeholder="Ornek: servis karari, burs politikasi, matematik zumre...")

        if sorgu and len(sorgu) >= 2:
            q = sorgu.strip().lower()
            sonuclar = [k for k in kayitlar
                         if q in (k.get("baslik", "") or "").lower()
                         or q in (k.get("detay", "") or "").lower()]

            st.caption(f"{len(sonuclar)} sonuc bulundu")

            tip_renk = {"Toplanti": "#7c3aed", "Karar": "#2563eb", "Aksiyon": "#f59e0b", "Gundem": "#0891b2"}
            for k in sonuclar[:20]:
                renk = tip_renk.get(k["tip"], "#64748b")
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-left:4px solid {renk};
                            border-radius:0 12px 12px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
                                    font-size:10px;font-weight:700;">{k['tip']}</span>
                        <span style="font-size:10px;color:#64748b;">{k['tarih']}</span>
                    </div>
                    <div style="font-size:12px;font-weight:700;color:#e2e8f0;margin-bottom:3px;">{k['baslik'][:120]}</div>
                    <div style="font-size:10px;color:#94a3b8;">{k['detay'][:150]}</div>
                </div>""", unsafe_allow_html=True)

            if not sonuclar:
                styled_info_banner(f'"{sorgu}" ile eslesen kayit bulunamadi.', banner_type="warning", icon="🔍")

    # ═══ AI SORU-CEVAP ═══
    with sub[1]:
        styled_section("AI Toplanti Hafiza Asistani")
        soru = st.text_area("Sorunuzu yazin...", key="th_ai_soru", height=80,
                             placeholder="Ornek: Gecen yil servis konusunda hangi kararlar alindi?")

        if st.button("AI'ya Sor", key="th_ai_btn", type="primary"):
            if soru:
                q = soru.strip().lower()
                ilgili = [k for k in kayitlar
                           if any(w in (k.get("baslik", "") + " " + k.get("detay", "")).lower()
                                  for w in q.split() if len(w) > 2)][:15]
                baglamlar = "\n".join(
                    f"[{k['tip']}] {k['tarih']}: {k['baslik']} — {k['detay'][:100]}" for k in ilgili)

                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if client:
                        with st.spinner("AI dusunuyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul toplanti hafiza asistanisin. Verilen toplanti/karar/aksiyon kayitlarina dayanarak soruyu cevapla. Kaynak goster. Turkce."},
                                    {"role": "user", "content": f"Soru: {soru}\n\nKayitlar:\n{baglamlar or 'Ilgili kayit bulunamadi.'}"},
                                ],
                                max_tokens=500, temperature=0.5,
                            )
                            ai = resp.choices[0].message.content or ""
                        if ai:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:1px solid #7c3aed;
                                        border-radius:14px;padding:16px 20px;">
                                <div style="font-size:12px;color:#c4b5fd;font-weight:700;margin-bottom:6px;">AI Cevap ({len(ilgili)} kayit tarandi)</div>
                                <div style="font-size:12px;color:#e0e7ff;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("OpenAI API bulunamadi.")
                except Exception as e:
                    st.error(f"Hata: {e}")

    # ═══ KURUL GEÇMİŞİ ═══
    with sub[2]:
        styled_section("Kurul Bazli Toplanti Gecmisi")
        if not kurullar:
            styled_info_banner("Kurul tanimlamasi yok.", banner_type="info", icon="📋")
        else:
            kurul_labels = [k.get("ad", k.get("baslik", "?")) for k in kurullar]
            secili_kurul = st.selectbox("Kurul Secin", ["Tumu"] + kurul_labels, key="th_kurul")

            filtered_mtg = meetings
            if secili_kurul != "Tumu":
                filtered_mtg = [m for m in meetings
                                 if secili_kurul.lower() in (m.get("baslik", "") or "").lower()
                                 or secili_kurul.lower() in (m.get("kurul", "") or "").lower()
                                 or secili_kurul.lower() in (m.get("toplanti_tipi", "") or "").lower()]

            st.caption(f"{len(filtered_mtg)} toplanti")
            for m in sorted(filtered_mtg, key=lambda x: x.get("tarih", ""), reverse=True)[:20]:
                durum = m.get("durum", "?")
                d_renk = {"YAPILDI": "#10b981", "TUTANAK_TAMAM": "#10b981", "ONAYLANDI": "#10b981",
                           "TASLAK": "#3b82f6", "IPTAL": "#94a3b8", "ERTELENDI": "#f59e0b"}.get(durum, "#64748b")
                m_karar = sum(1 for d in decisions if d.get("meeting_id") == m.get("id"))

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-left:4px solid {d_renk};
                            border-radius:0 10px 10px 0;padding:8px 14px;margin-bottom:4px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:600;color:#e2e8f0;font-size:12px;">{m.get('baslik', '')[:60]}</span>
                        <div style="display:flex;gap:6px;align-items:center;">
                            <span style="font-size:10px;color:#94a3b8;">{m.get('tarih', '')[:10]}</span>
                            <span style="font-size:10px;color:#2563eb;">{m_karar} karar</span>
                            <span style="background:{d_renk}20;color:{d_renk};padding:2px 6px;border-radius:4px;
                                        font-size:9px;font-weight:700;">{durum}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
