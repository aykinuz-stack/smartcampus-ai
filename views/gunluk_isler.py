"""Günlük İşler — Bugünkü devamsız öğrenciler tüm roller için."""
import json
import os
from datetime import date, datetime

import streamlit as st

from utils.ui_common import inject_common_css, styled_header


def render_gunluk_isler():
    """Günlük İşler ekranı — bugünkü yoklama sonuçları."""
    inject_common_css()
    styled_header("📋 Günlük İşler", "Bugünkü yoklama durumu ve devamsız öğrenciler")

    auth_user = st.session_state.get("auth_user", {})
    role = auth_user.get("role", "").lower()

    # Verileri yükle
    bugun = date.today().isoformat()
    attendance = _load_json("data/akademik/attendance.json")
    students = _load_json("data/akademik/students.json")
    users = _load_json("data/users.json")

    # Öğrenci haritası
    stu_map = {s.get("id"): s for s in students}

    # Bugünkü tüm yoklama kayıtları
    bugun_kayitlar = [a for a in attendance if a.get("tarih") == bugun]

    # Devamsız öğrenciler (devamsiz, ozursuz)
    devamsiz_ids = set()
    devamsiz_detay = {}  # student_id -> [{ders, ders_saati, turu}]
    for a in bugun_kayitlar:
        if a.get("turu") in ("devamsiz", "ozursuz"):
            sid = a.get("student_id", "")
            devamsiz_ids.add(sid)
            if sid not in devamsiz_detay:
                devamsiz_detay[sid] = []
            devamsiz_detay[sid].append({
                "ders": a.get("ders", ""),
                "ders_saati": a.get("ders_saati", 0),
                "turu": a.get("turu", ""),
            })

    # Geç kalan öğrenciler
    gec_ids = set()
    for a in bugun_kayitlar:
        if a.get("turu") == "gec":
            gec_ids.add(a.get("student_id", ""))

    # İzinli öğrenciler
    izinli_ids = set()
    for a in bugun_kayitlar:
        if a.get("turu") in ("izinli", "raporlu"):
            izinli_ids.add(a.get("student_id", ""))

    # Rol bazlı filtreleme
    if role == "veli":
        # Sadece kendi çocuklarını göster
        ogrenci_id = auth_user.get("ogrenci_id", "")
        children_ids = auth_user.get("children_ids", [])
        if ogrenci_id:
            children_ids = list(set(children_ids + [ogrenci_id]))
        devamsiz_ids = devamsiz_ids & set(children_ids)
        gec_ids = gec_ids & set(children_ids)
        izinli_ids = izinli_ids & set(children_ids)

    elif role == "ogrenci":
        # Sadece kendini göster (kendi sınıfındaki durumu)
        own_id = auth_user.get("student_id", auth_user.get("source_id", ""))
        if own_id:
            own_stu = stu_map.get(own_id, {})
            own_sinif = str(own_stu.get("sinif", ""))
            own_sube = own_stu.get("sube", "")
            # Kendi sınıfındaki devamsızları göster
            sinif_ids = {s.get("id") for s in students
                         if str(s.get("sinif", "")) == own_sinif
                         and s.get("sube", "") == own_sube}
            devamsiz_ids = devamsiz_ids & sinif_ids
            gec_ids = gec_ids & sinif_ids
            izinli_ids = izinli_ids & sinif_ids

    # ── ÖĞRETMEN EK BİLGİLERİ ──
    if role in ("ogretmen", "yonetici", "superadmin", "mudur"):
        gun_isimleri = {0: "Pazartesi", 1: "Salı", 2: "Çarşamba",
                        3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
        bugun_gun = gun_isimleri.get(date.today().weekday(), "")

        schedule = _load_json("data/akademik/schedule.json")
        ogretmen_adi = auth_user.get("name", "")
        # Sadece bu öğretmenin bugünkü dersleri (yönetici ise tümünü göster)
        bugun_tum = [s for s in schedule if s.get("gun", "").lower() == bugun_gun.lower()]
        if role == "ogretmen" and ogretmen_adi:
            bugun_dersler = [s for s in bugun_tum
                             if ogretmen_adi.lower() in (s.get("ogretmen_adi", "") or "").lower()]
        else:
            # Yönetici: tüm okulun bugünkü dersleri (ilk 20)
            bugun_dersler = bugun_tum[:20]
        def _saat_key(s):
            v = s.get("saat", 0)
            if isinstance(v, int):
                return v
            try:
                return int(str(v).split(":")[0].split("-")[0])
            except (ValueError, IndexError):
                return 0
        bugun_dersler.sort(key=_saat_key)

        nobet_data = _load_json("data/akademik/nobet_gorevler.json")
        bugun_nobet = any(n for n in nobet_data
                          if bugun_gun.lower() in n.get("gun", "").lower()
                          and ogretmen_adi.lower() in (n.get("ogretmen_adi", n.get("ogretmen", "")) or "").lower())

        mesajlar = _load_json("data/akademik/veli_mesajlar.json")
        okunmamis = sum(1 for m in mesajlar if not m.get("okundu", False) and "veli" in m.get("yon", ""))

        bugun_ay_gun = date.today().strftime("-%m-%d")
        dogum_gunu = [f"{s.get('ad', '')} {s.get('soyad', '')} ({s.get('sinif', '')}/{s.get('sube', '')})"
                      for s in students if (s.get("dogum_tarihi", "") or "").endswith(bugun_ay_gun)]

        if bugun_nobet:
            st.warning("🛡️ **Bugün nöbet günün!**")

        col_a, col_b = st.columns(2)
        with col_a:
            if okunmamis > 0:
                st.info(f"💬 **{okunmamis}** okunmamış mesaj")
        with col_b:
            if dogum_gunu:
                st.success(f"🎂 Doğum günü: {', '.join(dogum_gunu[:3])}")

        if bugun_dersler:
            with st.expander(f"📚 Bugünkü Derslerim ({bugun_gun}) — {len(bugun_dersler)} ders", expanded=False):
                for d in bugun_dersler:
                    st.markdown(f"`{d.get('saat', '?')}` — **{d.get('ders', '')}** ({d.get('sinif', '')}/{d.get('sube', '')})")

        st.markdown("---")

    # ── İstatistik Kartları ──
    toplam_yoklama = len(set(a.get("student_id") for a in bugun_kayitlar))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📊 Yoklama Alınan", toplam_yoklama)
    with c2:
        st.metric("❌ Devamsız", len(devamsiz_ids))
    with c3:
        st.metric("⏰ Geç Kalan", len(gec_ids))
    with c4:
        st.metric("📋 İzinli/Raporlu", len(izinli_ids))

    st.markdown("---")

    # ── Devamsız Öğrenci Tablosu ──
    if devamsiz_ids:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#dc2626,#ef4444);color:#fff;'
            'padding:14px 20px;border-radius:12px;margin-bottom:14px;font-weight:700;font-size:1.1rem">'
            f'❌ Bugün Devamsız Öğrenciler ({len(devamsiz_ids)} kişi) — {bugun}'
            '</div>', unsafe_allow_html=True,
        )

        rows = []
        for sid in sorted(devamsiz_ids):
            stu = stu_map.get(sid, {})
            ad = stu.get("ad", "?")
            soyad = stu.get("soyad", "?")
            sinif = stu.get("sinif", "?")
            sube = stu.get("sube", "?")
            numara = stu.get("numara", "?")
            veli_adi = f"{stu.get('veli_adi', '')} {stu.get('veli_soyadi', '')}".strip()
            veli_tel = stu.get("veli_telefon", "-")

            # Devamsız olduğu dersler
            dersler = devamsiz_detay.get(sid, [])
            ders_str = ", ".join([f"{d['ders']} ({d['ders_saati']}. ders)" for d in dersler])

            rows.append({
                "No": numara,
                "Ad Soyad": f"{ad} {soyad}",
                "Sınıf": f"{sinif}/{sube}",
                "Devamsız Dersler": ders_str,
                "Veli": veli_adi if veli_adi else "-",
                "Veli Tel": veli_tel,
            })

        # Sınıf filtresi
        siniflar = sorted(set(r["Sınıf"] for r in rows))
        if len(siniflar) > 1:
            secili_sinif = st.selectbox("Sınıf Filtresi", ["Tümü"] + siniflar, key="gi_sinif_f")
            if secili_sinif != "Tümü":
                rows = [r for r in rows if r["Sınıf"] == secili_sinif]

        # Tablo
        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
            column_config={
                "No": st.column_config.TextColumn("No", width="small"),
                "Ad Soyad": st.column_config.TextColumn("Ad Soyad", width="medium"),
                "Sınıf": st.column_config.TextColumn("Sınıf", width="small"),
                "Devamsız Dersler": st.column_config.TextColumn("Devamsız Dersler", width="large"),
                "Veli": st.column_config.TextColumn("Veli", width="medium"),
                "Veli Tel": st.column_config.TextColumn("Veli Tel", width="medium"),
            },
        )
    else:
        st.success("✅ Bugün devamsız öğrenci yok!")

    # ── Geç Kalan Öğrenciler ──
    if gec_ids:
        st.markdown("---")
        st.markdown(
            '<div style="background:linear-gradient(135deg,#f59e0b,#eab308);color:#fff;'
            'padding:12px 18px;border-radius:10px;margin-bottom:12px;font-weight:700">'
            f'⏰ Geç Kalan Öğrenciler ({len(gec_ids)} kişi)'
            '</div>', unsafe_allow_html=True,
        )
        gec_rows = []
        for sid in sorted(gec_ids):
            stu = stu_map.get(sid, {})
            gec_rows.append({
                "No": stu.get("numara", "?"),
                "Ad Soyad": f"{stu.get('ad', '?')} {stu.get('soyad', '?')}",
                "Sınıf": f"{stu.get('sinif', '?')}/{stu.get('sube', '?')}",
            })
        st.dataframe(gec_rows, use_container_width=True, hide_index=True)

    # ── İzinli/Raporlu ──
    if izinli_ids:
        st.markdown("---")
        st.markdown(
            '<div style="background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;'
            'padding:12px 18px;border-radius:10px;margin-bottom:12px;font-weight:700">'
            f'📋 İzinli / Raporlu ({len(izinli_ids)} kişi)'
            '</div>', unsafe_allow_html=True,
        )
        izinli_rows = []
        for sid in sorted(izinli_ids):
            stu = stu_map.get(sid, {})
            izinli_rows.append({
                "No": stu.get("numara", "?"),
                "Ad Soyad": f"{stu.get('ad', '?')} {stu.get('soyad', '?')}",
                "Sınıf": f"{stu.get('sinif', '?')}/{stu.get('sube', '?')}",
            })
        st.dataframe(izinli_rows, use_container_width=True, hide_index=True)

    # Yoklama henüz alınmamışsa
    if not bugun_kayitlar:
        st.warning("⚠️ Bugün henüz yoklama alınmamış.")


def _load_json(path: str) -> list:
    """JSON dosyasını yükle."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []
