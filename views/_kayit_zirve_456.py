"""
Kayit Modulu — Zirve 4,5,6 Ozellikleri
=======================================
4. Kayip Nedeni Analizi
5. Sezonluk YoY Karsilastirma
6. Dinamik Kontenjan Yonetimi
"""
from __future__ import annotations

from collections import Counter
from datetime import date

import streamlit as st

from models.kayit_modulu import (
    KayitAday, KayitDataStore,
    PIPELINE_ASAMALARI, PIPELINE_INFO, KADEME_SECENEKLERI, SINIF_SECENEKLERI,
    KAYIP_NEDENLERI, KAYIP_NEDEN_LISTESI, VARSAYILAN_KONTENJAN, AY_ADLARI,
)


# ============================================================
# ZİRVE 4: KAYIP NEDENİ ANALİZİ
# ============================================================

def _render_kayip_analizi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Yapısal kayıp nedeni girişi + analiz dashboard."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Kayıp Nedeni Analizi", "#ef4444")
    styled_info_banner(
        "Neden kaybettiğini bilmeden iyileştiremezsin. Her olumsuz adayın kayıp nedeni burada "
        "kategorize edilir — fiyat mı, rakip mi, uzaklık mı? Veriye dayalı strateji üret.",
        banner_type="warning", icon="📉")

    olumsuzlar = [a for a in adaylar if a.asama == "olumsuz"]
    neden_girilmis = [a for a in olumsuzlar if a.kayip_nedeni]
    neden_bos = [a for a in olumsuzlar if not a.kayip_nedeni]

    styled_stat_row([
        ("Toplam Kayıp", str(len(olumsuzlar)), "#ef4444", "❌"),
        ("Nedeni Girilmiş", str(len(neden_girilmis)), "#10b981", "✅"),
        ("Nedeni Eksik", str(len(neden_bos)), "#f59e0b", "⚠️"),
        ("Doluluk", f"%{round(len(neden_girilmis) / max(len(olumsuzlar), 1) * 100, 1)}", "#7c3aed", "📊"),
    ])

    sub = st.tabs(["📊 Analiz Dashboard", "📝 Neden Girişi", "📋 Detay Tablo"])

    # ═══ SEKME 1: Analiz Dashboard ═══
    with sub[0]:
        if not neden_girilmis:
            styled_info_banner(
                "Henüz kayıp nedeni girilmemiş. 'Neden Girişi' sekmesinden olumsuz adaylara neden atayın.",
                banner_type="info", icon="📝")
        else:
            # Neden dağılımı
            neden_sayac = Counter(a.kayip_nedeni for a in neden_girilmis)
            styled_section("Kayıp Nedeni Dağılımı")
            en_buyuk = neden_sayac.most_common(1)[0][1] if neden_sayac else 1
            for neden_key, sayi in neden_sayac.most_common():
                info = KAYIP_NEDENLERI.get(neden_key, {"label": neden_key, "emoji": "📋", "color": "#94a3b8"})
                pct = round(sayi / len(neden_girilmis) * 100, 1)
                bar_w = round(sayi / en_buyuk * 100, 1)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                    <span style="font-size:18px;min-width:28px;">{info['emoji']}</span>
                    <span style="min-width:180px;font-size:13px;color:#e2e8f0;font-weight:700;">{info['label']}</span>
                    <div style="flex:1;background:#1e293b;border-radius:6px;height:28px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{info['color']},{info['color']}90);
                                    border-radius:6px;display:flex;align-items:center;padding:0 12px;">
                            <span style="font-size:11px;color:#fff;font-weight:800;">{sayi} (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Kademe bazlı kayıp
            styled_section("Kademe Bazlı Kayıp Nedeni")
            kademe_neden: dict[str, Counter] = {}
            for a in neden_girilmis:
                k = a.kademe or "Belirtilmedi"
                if k not in kademe_neden:
                    kademe_neden[k] = Counter()
                kademe_neden[k][a.kayip_nedeni] += 1

            for kademe in sorted(kademe_neden.keys()):
                sayac = kademe_neden[kademe]
                toplam = sum(sayac.values())
                en_sik = sayac.most_common(1)[0] if sayac else ("", 0)
                en_sik_info = KAYIP_NEDENLERI.get(en_sik[0], {"label": "-", "emoji": "", "color": "#94a3b8"})
                detay = " · ".join(
                    f"{KAYIP_NEDENLERI.get(n, {}).get('emoji', '')} {s}" for n, s in sayac.most_common(3))
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-left:4px solid {en_sik_info['color']};
                            border-radius:0 10px 10px 0;padding:10px 16px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{kademe}</span>
                        <span style="font-size:11px;color:#94a3b8;">{toplam} kayıp · #1: {en_sik_info['emoji']} {en_sik_info['label']}</span>
                    </div>
                    <div style="font-size:10px;color:#64748b;margin-top:4px;">{detay}</div>
                </div>""", unsafe_allow_html=True)

            # Rakip okul tercihi
            rakip_adaylar = [a for a in neden_girilmis if a.kayip_nedeni == "rakip" and a.kayip_rakip_okul]
            if rakip_adaylar:
                styled_section("Rakip Okul Tercihi")
                rakip_sayac = Counter(a.kayip_rakip_okul for a in rakip_adaylar)
                for okul, sayi in rakip_sayac.most_common(10):
                    st.markdown(f"- **{okul}**: {sayi} aday kaybedildi")

    # ═══ SEKME 2: Neden Girişi ═══
    with sub[1]:
        styled_section("Kayıp Nedeni Ata")
        if not neden_bos:
            if olumsuzlar:
                st.success("Tüm olumsuz adaylara kayıp nedeni girilmiş!")
            else:
                styled_info_banner("Olumsuz aday yok.", banner_type="info", icon="✅")
        else:
            st.caption(f"⚠️ {len(neden_bos)} olumsuz adayın kayıp nedeni eksik")

            for a in neden_bos[:30]:
                with st.expander(f"❌ {a.veli_adi} — {a.ogrenci_adi} ({a.kademe} {a.hedef_sinif})", expanded=False):
                    son_not = ""
                    if a.aramalar:
                        son_not = a.aramalar[-1].get("not", "")
                    elif a.gorusmeler:
                        son_not = a.gorusmeler[-1].get("not", "")
                    if son_not:
                        st.caption(f"Son not: {son_not[:120]}")

                    col1, col2 = st.columns(2)
                    with col1:
                        neden_labels = [f"{v['emoji']} {v['label']}" for v in KAYIP_NEDENLERI.values()]
                        secili_neden = st.selectbox("Kayıp Nedeni", [""] + neden_labels, key=f"kn_{a.id}")
                    with col2:
                        rakip_okul = st.text_input("Rakip Okul (varsa)", key=f"kn_rakip_{a.id}")

                    alt_neden = st.text_input("Detay Açıklama", key=f"kn_detay_{a.id}",
                                              placeholder="Ek bilgi yazın...")

                    if st.button("Kaydet", key=f"kn_btn_{a.id}", type="primary"):
                        if secili_neden:
                            neden_key = ""
                            for k, v in KAYIP_NEDENLERI.items():
                                if v["label"] in secili_neden:
                                    neden_key = k
                                    break
                            store.update(a.id, {
                                "kayip_nedeni": neden_key,
                                "kayip_alt_neden": alt_neden,
                                "kayip_rakip_okul": rakip_okul,
                            })
                            st.success(f"✅ {a.veli_adi} — Neden kaydedildi: {secili_neden}")
                            st.rerun()
                        else:
                            st.warning("Lütfen bir neden seçin.")

    # ═══ SEKME 3: Detay Tablo ═══
    with sub[2]:
        styled_section("Tüm Kayıplar — Detay")
        if not olumsuzlar:
            styled_info_banner("Olumsuz aday yok.", banner_type="info", icon="✅")
        else:
            fc1, fc2 = st.columns(2)
            with fc1:
                neden_fil = st.selectbox("Neden Filtresi",
                    ["Tümü", "⚠️ Nedeni Eksik"] + [f"{v['emoji']} {v['label']}" for v in KAYIP_NEDENLERI.values()],
                    key="kn_tbl_fil")
            with fc2:
                kademe_fil = st.selectbox("Kademe", ["Tümü"] + KADEME_SECENEKLERI, key="kn_tbl_kademe")

            filtered = olumsuzlar
            if neden_fil == "⚠️ Nedeni Eksik":
                filtered = [a for a in filtered if not a.kayip_nedeni]
            elif neden_fil != "Tümü":
                for k, v in KAYIP_NEDENLERI.items():
                    if v["label"] in neden_fil:
                        filtered = [a for a in filtered if a.kayip_nedeni == k]
                        break
            if kademe_fil != "Tümü":
                filtered = [a for a in filtered if a.kademe == kademe_fil]

            st.caption(f"📋 {len(filtered)} kayıt")

            rows = ""
            for a in filtered[:50]:
                ninfo = KAYIP_NEDENLERI.get(a.kayip_nedeni, {"label": "—", "emoji": "—", "color": "#94a3b8"})
                badge = (f'<span style="background:{ninfo["color"]}20;color:{ninfo["color"]};'
                         f'padding:2px 8px;border-radius:6px;font-size:10px;font-weight:700;">'
                         f'{ninfo["emoji"]} {ninfo["label"]}</span>') if a.kayip_nedeni else \
                    '<span style="color:#f59e0b;font-size:10px;">⚠️ Eksik</span>'
                rows += f"""<tr>
                    <td style="padding:6px 10px;font-weight:600;color:#e2e8f0;">{a.veli_adi}</td>
                    <td style="padding:6px 10px;color:#94a3b8;">{a.ogrenci_adi}</td>
                    <td style="padding:6px 10px;color:#94a3b8;">{a.kademe}</td>
                    <td style="padding:6px 10px;">{badge}</td>
                    <td style="padding:6px 10px;color:#64748b;font-size:11px;">{a.kayip_rakip_okul or '—'}</td>
                    <td style="padding:6px 10px;color:#64748b;font-size:11px;">{a.kapanma_tarihi[:10] if a.kapanma_tarihi else '—'}</td>
                </tr>"""
            if rows:
                st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
                <thead><tr style="background:#1e293b;">
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Veli</th>
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Öğrenci</th>
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Kademe</th>
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Kayıp Nedeni</th>
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Rakip Okul</th>
                    <th style="padding:8px 10px;text-align:left;color:#64748b;">Tarih</th>
                </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)


# ============================================================
# ZİRVE 5: SEZONLUK YoY KARŞILAŞTIRMA
# ============================================================

def _render_yoy_sezon(store: KayitDataStore, adaylar: list[KayitAday]):
    """Bu yıl vs geçen yıl aynı dönem karşılaştırması."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Sezonluk Karşılaştırma (YoY)", "#2563eb")
    styled_info_banner(
        "Bu kayıt sezonunun geçen yıl aynı dönemiyle karşılaştırması. "
        "Neredeyiz, ne kadar büyüdük, nerede gerideyiz — hepsini tek ekranda gör.",
        banner_type="info", icon="📅")

    bugun = date.today()
    bu_yil = bugun.year
    gecen_yil = bu_yil - 1

    def _yil(a: KayitAday) -> int:
        try:
            return int(a.olusturma_tarihi[:4])
        except (ValueError, TypeError):
            return 0

    def _ay(a: KayitAday) -> int:
        try:
            return int(a.olusturma_tarihi[5:7])
        except (ValueError, TypeError):
            return 0

    bu_yil_adaylar = [a for a in adaylar if _yil(a) == bu_yil]
    gecen_yil_adaylar = [a for a in adaylar if _yil(a) == gecen_yil]
    bu_ay = bugun.month
    gy_ayni_donem = [a for a in gecen_yil_adaylar if _ay(a) <= bu_ay]

    by_kesin = sum(1 for a in bu_yil_adaylar if a.asama == "kesin_kayit")
    gy_kesin = sum(1 for a in gy_ayni_donem if a.asama == "kesin_kayit")
    by_aktif = sum(1 for a in bu_yil_adaylar if a.aktif)

    def _degisim(bu, gecen):
        if gecen == 0:
            return "+∞" if bu > 0 else "—"
        fark = round((bu - gecen) / gecen * 100, 1)
        return f"+{fark}%" if fark >= 0 else f"{fark}%"

    def _degisim_renk(bu, gecen):
        if gecen == 0:
            return "#10b981"
        return "#10b981" if bu >= gecen else "#ef4444"

    styled_stat_row([
        (f"Aday {bu_yil}", str(len(bu_yil_adaylar)), "#2563eb", "📋"),
        (f"Aday {gecen_yil} (aynı dönem)", str(len(gy_ayni_donem)), "#64748b", "📋"),
        ("Değişim", _degisim(len(bu_yil_adaylar), len(gy_ayni_donem)),
         _degisim_renk(len(bu_yil_adaylar), len(gy_ayni_donem)), "📈"),
        (f"Kayıt {bu_yil}", str(by_kesin), "#10b981", "✅"),
        (f"Kayıt {gecen_yil}", str(gy_kesin), "#64748b", "✅"),
        ("Kayıt Değişim", _degisim(by_kesin, gy_kesin), _degisim_renk(by_kesin, gy_kesin), "📈"),
    ])

    # ── HERO ──
    buyume = round((by_kesin - gy_kesin) / max(gy_kesin, 1) * 100, 1) if gy_kesin > 0 else (100 if by_kesin > 0 else 0)
    hero_renk = "#10b981" if buyume >= 0 else "#ef4444"
    hero_ok = "▲" if buyume >= 0 else "▼"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0c4a6e 0%,#164e63 100%);border:2px solid {hero_renk};
                border-radius:18px;padding:22px;margin:14px 0;text-align:center;
                box-shadow:0 6px 24px {hero_renk}30;">
        <div style="font-size:11px;color:#94a3b8;letter-spacing:3px;text-transform:uppercase;">
            Kayıt Büyüme Oranı (YoY)</div>
        <div style="font-size:56px;font-weight:900;color:{hero_renk};
                    font-family:Playfair Display,Georgia,serif;">{hero_ok} %{abs(buyume)}</div>
        <div style="font-size:13px;color:#94a3b8;margin-top:4px;">
            {gecen_yil}: {gy_kesin} kayıt → {bu_yil}: {by_kesin} kayıt
            · {len(bu_yil_adaylar)} toplam aday · {by_aktif} hâlâ aktif</div>
    </div>""", unsafe_allow_html=True)

    # ── AYLIK TREND ──
    styled_section("Aylık Trend — Bu Yıl vs Geçen Yıl")
    for ay in range(1, 13):
        by_ay = [a for a in bu_yil_adaylar if _ay(a) == ay]
        gy_ay = [a for a in gecen_yil_adaylar if _ay(a) == ay]
        by_ay_kesin = sum(1 for a in by_ay if a.asama == "kesin_kayit")
        gy_ay_kesin = sum(1 for a in gy_ay if a.asama == "kesin_kayit")
        ay_adi = AY_ADLARI[ay - 1] if 1 <= ay <= 12 else str(ay)
        is_current = ay == bu_ay
        is_future = ay > bu_ay
        border = "border:2px solid #c9a84c;" if is_current else ""
        opacity = "opacity:0.4;" if is_future else ""
        max_val = max(len(by_ay), len(gy_ay), 1)
        by_w = round(len(by_ay) / max_val * 100)
        gy_w = round(len(gy_ay) / max_val * 100)
        d_r = _degisim_renk(len(by_ay), len(gy_ay))

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #1e293b;border-radius:10px;
                    padding:10px 14px;margin-bottom:6px;{border}{opacity}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-weight:700;color:#e2e8f0;font-size:13px;">
                    {'🔶 ' if is_current else ''}{ay_adi}</span>
                <div style="display:flex;gap:12px;font-size:11px;">
                    <span style="color:#94a3b8;">Aday: <b style="color:#3b82f6;">{len(by_ay)}</b> vs <b style="color:#64748b;">{len(gy_ay)}</b>
                        <span style="color:{d_r};font-weight:700;margin-left:4px;">{_degisim(len(by_ay), len(gy_ay))}</span></span>
                    <span style="color:#94a3b8;">Kayıt: <b style="color:#10b981;">{by_ay_kesin}</b> vs <b style="color:#64748b;">{gy_ay_kesin}</b>
                        <span style="color:{_degisim_renk(by_ay_kesin, gy_ay_kesin)};font-weight:700;margin-left:4px;">{_degisim(by_ay_kesin, gy_ay_kesin)}</span></span>
                </div>
            </div>
            <div style="display:flex;gap:4px;">
                <div style="flex:1;background:#1e293b;border-radius:3px;height:8px;overflow:hidden;">
                    <div style="width:{by_w}%;height:100%;background:#3b82f6;border-radius:3px;"></div></div>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:8px;overflow:hidden;">
                    <div style="width:{gy_w}%;height:100%;background:#64748b;border-radius:3px;"></div></div>
            </div>
            <div style="display:flex;gap:8px;margin-top:3px;font-size:9px;color:#64748b;">
                <span>🔵 {bu_yil}</span><span>⚫ {gecen_yil}</span></div>
        </div>""", unsafe_allow_html=True)

    # ── KADEME BAZLI YoY ──
    styled_section("Kademe Bazlı Büyüme")
    for kademe in KADEME_SECENEKLERI:
        by_k = [a for a in bu_yil_adaylar if a.kademe == kademe]
        gy_k = [a for a in gy_ayni_donem if a.kademe == kademe]
        by_k_kesin = sum(1 for a in by_k if a.asama == "kesin_kayit")
        gy_k_kesin = sum(1 for a in gy_k if a.asama == "kesin_kayit")
        deg = _degisim(by_k_kesin, gy_k_kesin)
        d_r = _degisim_renk(by_k_kesin, gy_k_kesin)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:6px 0;">
            <span style="min-width:80px;font-weight:700;color:#e2e8f0;font-size:13px;">{kademe}</span>
            <span style="color:#94a3b8;font-size:12px;">Aday: {len(by_k)} vs {len(gy_k)}</span>
            <span style="color:#94a3b8;font-size:12px;">Kayıt: <b style="color:#10b981">{by_k_kesin}</b> vs <b style="color:#64748b">{gy_k_kesin}</b></span>
            <span style="background:{d_r}20;color:{d_r};padding:2px 8px;border-radius:6px;font-size:11px;font-weight:700;">{deg}</span>
        </div>""", unsafe_allow_html=True)


# ============================================================
# ZİRVE 6: DİNAMİK KONTENJAN YÖNETİMİ
# ============================================================

def _render_kontenjan_yonetimi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Sınıf bazlı kontenjan takibi + doluluk analizi + uyarılar."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Kontenjan Yönetimi", "#0891b2")
    styled_info_banner(
        "Sınıf bazlı kontenjan limitleri ve doluluk oranları. "
        "Kontenjanı dolan sınıflar otomatik uyarı verir.",
        banner_type="info", icon="🎓")

    kontenjan_durum = store.kontenjan_durumu()
    kontenjanlar = store.load_kontenjanlar()

    toplam_kont = sum(d["kontenjan"] for d in kontenjan_durum)
    toplam_dolu = sum(d["dolu"] for d in kontenjan_durum)
    toplam_bos = sum(d["bos"] for d in kontenjan_durum)
    genel_doluluk = round(toplam_dolu / max(toplam_kont, 1) * 100, 1)
    dolu_sinif = sum(1 for d in kontenjan_durum if d["doluluk_yuzde"] >= 100)
    kritik_sinif = sum(1 for d in kontenjan_durum if 80 <= d["doluluk_yuzde"] < 100)

    styled_stat_row([
        ("Toplam Kontenjan", str(toplam_kont), "#0891b2", "🎓"),
        ("Dolu", str(toplam_dolu), "#10b981", "✅"),
        ("Boş", str(toplam_bos), "#f59e0b", "📋"),
        ("Genel Doluluk", f"%{genel_doluluk}", "#7c3aed", "📊"),
        ("Dolu Sınıf", str(dolu_sinif), "#ef4444", "🔴"),
        ("Kritik (≥%80)", str(kritik_sinif), "#f97316", "🟠"),
    ])

    # ── HERO ──
    g_renk = "#10b981" if genel_doluluk >= 70 else "#f59e0b" if genel_doluluk >= 40 else "#ef4444"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0c4a6e 0%,#155e75 100%);border:2px solid {g_renk};
                border-radius:18px;padding:22px;margin:14px 0;text-align:center;
                box-shadow:0 6px 24px {g_renk}30;">
        <div style="font-size:11px;color:#94a3b8;letter-spacing:3px;text-transform:uppercase;">
            Genel Doluluk Oranı</div>
        <div style="font-size:56px;font-weight:900;color:{g_renk};
                    font-family:Playfair Display,Georgia,serif;">%{genel_doluluk}</div>
        <div style="font-size:13px;color:#94a3b8;margin-top:4px;">
            {toplam_dolu}/{toplam_kont} öğrenci · {toplam_bos} boş · {dolu_sinif} sınıf dolu</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📊 Doluluk Haritası", "⚙️ Kontenjan Düzenle", "⚠️ Uyarılar"])

    # ═══ SEKME 1: Doluluk Haritası ═══
    with sub[0]:
        styled_section("Sınıf Bazlı Doluluk")
        for d in kontenjan_durum:
            pct = d["doluluk_yuzde"]
            renk = "#ef4444" if pct >= 100 else "#f97316" if pct >= 80 else "#f59e0b" if pct >= 60 else "#10b981"
            durum_txt = "DOLU" if pct >= 100 else "KRİTİK" if pct >= 80 else "AÇIK"
            bar_w = min(pct, 100)
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-left:4px solid {renk};
                        border-radius:0 10px 10px 0;padding:10px 16px;margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{d['sinif']}</span>
                    <div style="display:flex;gap:10px;align-items:center;">
                        <span style="font-size:12px;color:#94a3b8;">{d['dolu']}/{d['kontenjan']}</span>
                        <span style="background:{renk};color:#fff;padding:2px 10px;border-radius:6px;
                                    font-size:10px;font-weight:700;">{durum_txt} %{pct}</span>
                    </div>
                </div>
                <div style="margin-top:6px;background:#1e293b;border-radius:4px;height:10px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,{renk},{renk}80);
                                border-radius:4px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ SEKME 2: Kontenjan Düzenle ═══
    with sub[1]:
        styled_section("Kontenjan Limitlerini Düzenle")
        styled_info_banner("Her sınıfın maksimum öğrenci sayısını ayarlayın.", banner_type="info", icon="⚙️")

        with st.form("kontenjan_form"):
            yeni_kont = dict(kontenjanlar)
            cols = st.columns(4)
            for idx, sinif in enumerate(SINIF_SECENEKLERI):
                with cols[idx % 4]:
                    mevcut = kontenjanlar.get(sinif, VARSAYILAN_KONTENJAN.get(sinif, 30))
                    yeni_kont[sinif] = st.number_input(sinif, min_value=0, max_value=100, value=mevcut,
                                                        key=f"kont_{sinif}")

            if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                store.save_kontenjanlar(yeni_kont)
                st.success("Kontenjanlar kaydedildi!")
                st.rerun()

    # ═══ SEKME 3: Uyarılar ═══
    with sub[2]:
        styled_section("Kontenjan Uyarıları")

        dolu_siniflar = [d for d in kontenjan_durum if d["doluluk_yuzde"] >= 100]
        if dolu_siniflar:
            for d in dolu_siniflar:
                bekleyen = [a for a in adaylar if a.aktif and a.hedef_sinif == d["sinif"]]
                st.markdown(f"""
                <div style="background:#7f1d1d;border:1px solid #ef4444;border-radius:12px;
                            padding:12px 16px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:800;color:#fca5a5;font-size:14px;">
                            🔴 {d['sinif']} — KONTENJAN DOLDU</span>
                        <span style="color:#fca5a5;font-size:12px;">{d['dolu']}/{d['kontenjan']}</span>
                    </div>
                    <div style="font-size:11px;color:#fca5a5;margin-top:4px;">
                        ⚠️ Pipeline'da {len(bekleyen)} aktif aday bu sınıfı bekliyor!
                        {' Bekleme listesine alınması önerilir.' if bekleyen else ''}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Şu an hiçbir sınıfın kontenjanı dolmamış.")

        kritik = [d for d in kontenjan_durum if 80 <= d["doluluk_yuzde"] < 100]
        if kritik:
            styled_section("⚠️ Kritik Doluluk (≥%80)")
            for d in kritik:
                kalan = d["bos"]
                bekleyen = [a for a in adaylar if a.aktif and a.hedef_sinif == d["sinif"]]
                st.warning(f"**{d['sinif']}** — %{d['doluluk_yuzde']} dolu · {kalan} kalan · "
                           f"{len(bekleyen)} aday bekliyor")
