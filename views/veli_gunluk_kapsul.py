"""
Günlük Kapsül — Veli için Günlük AI Özet
===============================================
Her gün 16:00'da AI veliye 2 dakikalık özet hazırlar:
  "Çocuğunuzun bugünü — matematik sınavı 85, yeni arkadaş edindi, yarın kitap getirsin"
Akademik Takip'ten veri çeker, Smarti ile özetler, ses + fotoğraf ile sunar.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner, styled_header


# ══════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════

def _kapsul_dir() -> str:
    try:
        from utils.tenant import get_tenant_dir
        d = os.path.join(get_tenant_dir(), "veli_gunluk_kapsul")
    except Exception:
        d = os.path.join("data", "veli_gunluk_kapsul")
    os.makedirs(d, exist_ok=True)
    return d


def _kapsul_path() -> str:
    return os.path.join(_kapsul_dir(), "kapsuller.json")


def _load_kapsuller() -> list[dict]:
    p = _kapsul_path()
    if not os.path.exists(p):
        return []
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_kapsuller(data: list[dict]) -> None:
    with open(_kapsul_path(), "w", encoding="utf-8") as f:
        json.dump(data[-500:], f, ensure_ascii=False, indent=2)  # son 500 kapsül


# ══════════════════════════════════════════════════════════════
# VERİ TOPLAMA — Akademik Takip + Diğer Modüller
# ══════════════════════════════════════════════════════════════

def _collect_student_day_data(student_id: str, student_name: str, tarih: str) -> dict:
    """Bir öğrencinin belirli tarihteki tüm aktivitelerini topla."""
    data = {
        "student_id": student_id,
        "student_name": student_name,
        "tarih": tarih,
        "notlar": [],
        "devamsizlik": [],
        "odev": [],
        "etkinlik": [],
        "rehberlik": [],
        "olumlu": [],
        "gecmis_performans": {},
    }

    try:
        from utils.tenant import get_tenant_dir
        td = get_tenant_dir()
    except Exception:
        return data

    # Notlar
    try:
        with open(os.path.join(td, "akademik", "grades.json"), "r", encoding="utf-8") as f:
            grades = json.load(f)
        for g in grades:
            if (g.get("student_id") == student_id and g.get("tarih", "").startswith(tarih)):
                data["notlar"].append({
                    "ders": g.get("ders", ""),
                    "puan": g.get("puan", g.get("not_degeri", "")),
                    "tur": g.get("not_turu", "yazılı"),
                })
    except Exception:
        pass

    # Devamsızlık
    try:
        with open(os.path.join(td, "akademik", "attendance.json"), "r", encoding="utf-8") as f:
            att = json.load(f)
        for a in att:
            if a.get("student_id") == student_id and a.get("tarih") == tarih:
                data["devamsizlik"].append({
                    "ders": a.get("ders", ""),
                    "saat": a.get("ders_saati", ""),
                    "turu": a.get("turu", ""),
                })
    except Exception:
        pass

    # Ödevler (teslim edildi mi?)
    try:
        with open(os.path.join(td, "akademik", "odev_teslim.json"), "r", encoding="utf-8") as f:
            teslimler = json.load(f)
        for t in teslimler:
            if t.get("student_id") == student_id and t.get("teslim_tarihi", "").startswith(tarih):
                data["odev"].append({
                    "odev_id": t.get("odev_id", ""),
                    "durum": t.get("durum", "teslim edildi"),
                    "puan": t.get("puan", ""),
                })
    except Exception:
        pass

    # Olumlu davranış
    try:
        with open(os.path.join(td, "rehberlik", "olumlu_davranislar.json"), "r", encoding="utf-8") as f:
            olumlu = json.load(f)
        for o in olumlu:
            if o.get("student_id") == student_id and o.get("tarih", "").startswith(tarih):
                data["olumlu"].append({
                    "aciklama": o.get("aciklama", o.get("davranis", "")),
                })
    except Exception:
        pass

    # Rehberlik görüşmesi
    try:
        with open(os.path.join(td, "rehberlik", "gorusmeler.json"), "r", encoding="utf-8") as f:
            gorusmeler = json.load(f)
        for g in gorusmeler:
            if g.get("student_id") == student_id and g.get("tarih", "").startswith(tarih):
                data["rehberlik"].append({
                    "ozet": g.get("ozet", "")[:100],
                })
    except Exception:
        pass

    return data


# ══════════════════════════════════════════════════════════════
# AI ÖZET ÜRETİCİ
# ══════════════════════════════════════════════════════════════

def generate_kapsul_ozet(client, data: dict) -> dict:
    """AI ile veli için sıcak, kısa günlük özet üret."""
    not_count = len(data["notlar"])
    dev_count = len(data["devamsizlik"])
    odev_count = len(data["odev"])
    olumlu_count = len(data["olumlu"])
    rehberlik_count = len(data["rehberlik"])

    ozet_text = {
        "sicak_giris": "",
        "ana_olaylar": [],
        "yarin_icin": "",
        "duygusal_ton": "pozitif",  # pozitif / notr / dikkat
    }

    # Veri yoksa
    toplam_olay = not_count + dev_count + odev_count + olumlu_count + rehberlik_count
    if toplam_olay == 0:
        return {
            "sicak_giris": f"Sayın Velimiz, {data['student_name']} için bugün kayıtlı özel bir aktivite bulunmuyor.",
            "ana_olaylar": ["Normal bir gündü."],
            "yarin_icin": "Her zamanki gibi hazırlıklı olunsun.",
            "duygusal_ton": "notr",
        }

    # Basit özet (AI yoksa)
    ana_olaylar = []
    if data["notlar"]:
        for n in data["notlar"]:
            ana_olaylar.append(f"📝 {n['ders']} sınavı: **{n['puan']}**")
    if data["odev"]:
        ana_olaylar.append(f"✅ {odev_count} ödev teslim edildi")
    if data["olumlu"]:
        for o in data["olumlu"][:2]:
            ana_olaylar.append(f"⭐ {o['aciklama'][:80]}")
    if data["devamsizlik"]:
        for d in data["devamsizlik"]:
            durum = "özürsüz" if d.get("turu", "").lower() in ("ozursuz", "özürsüz") else "özürlü"
            ana_olaylar.append(f"⚠️ {d['ders']} dersinde {durum} devamsızlık")
        ozet_text["duygusal_ton"] = "dikkat"
    if data["rehberlik"]:
        ana_olaylar.append("🧠 Rehber öğretmenle görüşme yapıldı")

    ozet_text["ana_olaylar"] = ana_olaylar or ["Normal bir gündü."]

    if client:
        # AI ile zenginleştir
        try:
            context = (
                f"Öğrenci: {data['student_name']}\n"
                f"Tarih: {data['tarih']}\n"
                f"Notlar: {data['notlar']}\n"
                f"Devamsızlık: {data['devamsizlik']}\n"
                f"Teslim edilen ödevler: {data['odev']}\n"
                f"Olumlu davranışlar: {data['olumlu']}\n"
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "Sen sıcak, samimi, profesyonel bir okul asistanısın. "
                        "Velilere çocuklarının günlük özetini 100 kelimeyi geçmeyen, "
                        "2-3 cümlelik sıcak mesaj olarak yaz. 'Sayın Velimiz' ile başla. "
                        "Başarıları överek, dikkat gerektirenleri nazikçe belirt. Yarın için 1 kısa öneri ekle."
                    )},
                    {"role": "user", "content": context + "\n\nKapsül özeti yaz."},
                ],
                max_tokens=300, temperature=0.7,
            )
            sicak_metin = resp.choices[0].message.content or ""
            ozet_text["sicak_giris"] = sicak_metin
        except Exception:
            pass

    if not ozet_text["sicak_giris"]:
        # Fallback
        ozet_text["sicak_giris"] = (
            f"Sayın Velimiz, {data['student_name']} için bugünün özeti: "
            f"{toplam_olay} farklı aktivite kaydedildi."
        )

    # Yarın için öneri
    if data["devamsizlik"]:
        ozet_text["yarin_icin"] = "Yarın dikkat: devamsızlık telafisi için konu tekrarı yapılması önerilir."
    elif data["notlar"] and any(float(str(n.get("puan", 0)).replace(",", ".")) < 50 for n in data["notlar"] if str(n.get("puan", "")).replace(",", ".").replace(".", "").isdigit()):
        ozet_text["yarin_icin"] = "Yarın: düşük not alınan ders için destek çalışması planlanabilir."
    else:
        ozet_text["yarin_icin"] = "Yarın iyi bir gün olsun! 🌟"

    return ozet_text


# ══════════════════════════════════════════════════════════════
# VELİ PANELİ — "Çocuğumun Bugünü"
# ══════════════════════════════════════════════════════════════

def render_veli_gunluk_kapsul_panel():
    """Veli için ana panel — bugünün kapsülü."""
    styled_header(
        "📦 Günlük Kapsül",
        "Çocuğunuzun bugünkü okul özeti — her gün 16:00'da hazır",
        icon="📦",
    )

    try:
        auth = st.session_state.get("auth_user", {})
        veli_ad = auth.get("name", "")
        veli_email = auth.get("email", "")
        veli_username = auth.get("username", "")
    except Exception:
        veli_ad, veli_email, veli_username = "", "", ""

    # Veliye bağlı öğrenci(ler)i bul
    try:
        from models.akademik_takip import AkademikDataStore
        ak = AkademikDataStore()
        all_students = ak.get_students()
        children = [s for s in all_students if
                    (veli_ad and s.veli_adi and veli_ad.lower() in s.veli_adi.lower()) or
                    (veli_username and s.veli_telefon and veli_username in str(s.veli_telefon))]
    except Exception:
        children = []

    if not children:
        styled_info_banner(
            "Velisi olduğunuz öğrenci bulunamadı. Okul yönetimiyle iletişime geçin.",
            "warning",
        )
        # Demo çocuk listesi göster
        children = [type("Stu", (), {"id": "demo_1", "tam_ad": "Örnek Öğrenci", "sinif": 9, "sube": "A"})()]

    # Çoklu çocuk için seçim
    if len(children) > 1:
        child_names = [f"{c.tam_ad} ({c.sinif}/{c.sube})" for c in children]
        sel_idx = st.selectbox("Çocuğunuzu seçin", range(len(children)),
                                format_func=lambda i: child_names[i], key="_kps_child_widget")
        child = children[sel_idx]
    else:
        child = children[0]

    # Tarih seç (bugün varsayılan)
    tc1, tc2 = st.columns([1, 3])
    with tc1:
        secili_tarih = st.date_input("Tarih", value=date.today(), key="_kps_tarih_widget")

    tarih_str = secili_tarih.isoformat()
    today_str = date.today().isoformat()

    # Kapsül var mı?
    kapsuller = _load_kapsuller()
    mevcut = next(
        (k for k in kapsuller if k.get("student_id") == child.id and k.get("tarih") == tarih_str),
        None,
    )

    if mevcut:
        _render_kapsul_view(mevcut, secili_tarih == date.today())
    else:
        # Henüz üretilmemişse + bugün veya gelecek tarih ise
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#4F46E5,#7C3AED);border-radius:16px;
        padding:24px;color:white;text-align:center;margin:16px 0;">
            <div style="font-size:3rem;margin-bottom:8px;">📦</div>
            <div style="font-size:1.2rem;font-weight:700;">Kapsül Hazırlanıyor...</div>
            <div style="font-size:0.9rem;opacity:0.9;margin-top:6px;">
                {tarih_str} için kapsül henüz oluşturulmamış.<br/>
                Her gün 16:00'da otomatik hazırlanır.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Manuel oluşturma
        if st.button("🤖 Şimdi Hazırla (AI ile)", type="primary", key="_kps_gen_now"):
            with st.spinner("Kapsül hazırlanıyor..."):
                data = _collect_student_day_data(child.id, child.tam_ad, tarih_str)
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                except Exception:
                    client = None
                ozet = generate_kapsul_ozet(client, data)

                yeni_kapsul = {
                    "id": f"KPS-{len(kapsuller)+1:06d}",
                    "student_id": child.id,
                    "student_name": child.tam_ad,
                    "tarih": tarih_str,
                    "data": data,
                    "ozet": ozet,
                    "olusturma_tarihi": datetime.now().isoformat(),
                    "okundu": False,
                }
                kapsuller.append(yeni_kapsul)
                _save_kapsuller(kapsuller)
                st.rerun()

    # Geçmiş kapsüller
    st.divider()
    styled_section("📚 Geçmiş Kapsüller", "#64748B")

    child_kapsuller = [k for k in kapsuller if k.get("student_id") == child.id]
    child_kapsuller.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    if not child_kapsuller:
        styled_info_banner("Henüz kapsül yok.", "info")
    else:
        for k in child_kapsuller[:14]:  # son 2 hafta
            okundu_badge = "✅" if k.get("okundu") else "🔔"
            ozet = k.get("ozet", {})
            ton = ozet.get("duygusal_ton", "notr")
            ton_renk = {"pozitif": "#059669", "dikkat": "#D97706", "notr": "#64748B"}.get(ton, "#64748B")

            with st.expander(f"{okundu_badge} {k.get('tarih')} — {len(ozet.get('ana_olaylar', []))} olay"):
                _render_kapsul_view(k, compact=True)


def _render_kapsul_view(kapsul: dict, bugun_mu: bool = True, compact: bool = False):
    """Tek bir kapsülü göster."""
    ozet = kapsul.get("ozet", {})
    data = kapsul.get("data", {})
    ton = ozet.get("duygusal_ton", "notr")

    # Renk tonlama
    ton_colors = {
        "pozitif": "#059669",
        "dikkat": "#D97706",
        "notr": "#4F46E5",
    }
    ana_renk = ton_colors.get(ton, "#4F46E5")

    if not compact:
        # Hero kart
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{ana_renk}20,{ana_renk}05);
        border:2px solid {ana_renk}40;border-radius:16px;padding:24px;margin:16px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <div style="font-size:1.2rem;font-weight:800;color:{ana_renk};">
                    📦 {kapsul.get('student_name', '')} — {kapsul.get('tarih', '')}
                </div>
                <div style="font-size:0.82rem;color:#94A3B8;">
                    {datetime.fromisoformat(kapsul.get('olusturma_tarihi', datetime.now().isoformat())).strftime('%d.%m.%Y %H:%M')}
                </div>
            </div>
            <div style="font-size:0.95rem;color:#E4E4E7;line-height:1.7;white-space:pre-wrap;">
                {ozet.get('sicak_giris', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Ana olaylar
    if ozet.get("ana_olaylar"):
        st.markdown("**📌 Bugünün Özetleri:**")
        for olay in ozet["ana_olaylar"]:
            st.markdown(f"• {olay}")

    # Detaylar
    if not compact:
        with st.expander("🔍 Detaylar"):
            if data.get("notlar"):
                st.markdown("**📝 Notlar:**")
                for n in data["notlar"]:
                    st.markdown(f"  • {n['ders']}: **{n['puan']}** ({n['tur']})")
            if data.get("devamsizlik"):
                st.markdown("**⚠️ Devamsızlık:**")
                for d in data["devamsizlik"]:
                    st.markdown(f"  • {d['ders']} ({d['saat']}. saat) — {d['turu']}")
            if data.get("odev"):
                st.markdown("**✅ Teslim Edilen Ödevler:**")
                for o in data["odev"]:
                    st.markdown(f"  • Ödev {o.get('odev_id', '')}: {o.get('durum', '')}")
            if data.get("olumlu"):
                st.markdown("**⭐ Olumlu Davranışlar:**")
                for o in data["olumlu"]:
                    st.markdown(f"  • {o.get('aciklama', '')}")

    # Yarın için öneri
    if ozet.get("yarin_icin") and not compact:
        st.markdown(f"""
        <div style="background:#0284C720;border-left:4px solid #0284C7;
        border-radius:0 12px 12px 0;padding:14px 18px;margin:16px 0;">
            <div style="font-size:0.85rem;font-weight:700;color:#0284C7;margin-bottom:4px;">
                🌅 Yarın İçin
            </div>
            <div style="color:#E4E4E7;font-size:0.92rem;">
                {ozet['yarin_icin']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Okundu işareti
    if not kapsul.get("okundu") and not compact:
        if st.button("✅ Okudum", key=f"_kps_okudum_{kapsul.get('id')}"):
            kapsuller = _load_kapsuller()
            idx = next((i for i, k in enumerate(kapsuller) if k.get("id") == kapsul.get("id")), None)
            if idx is not None:
                kapsuller[idx]["okundu"] = True
                kapsuller[idx]["okunma_tarihi"] = datetime.now().isoformat()
                _save_kapsuller(kapsuller)
                st.rerun()


# ══════════════════════════════════════════════════════════════
# YÖNETİM PANELİ — Toplu kapsül üretimi, istatistik
# ══════════════════════════════════════════════════════════════

def render_kapsul_yonetim_panel():
    """Okul yönetimi için kapsül yönetim paneli."""
    styled_section("📦 Günlük Kapsül Yönetimi", "#4F46E5")

    styled_info_banner(
        "Her gün tüm öğrenciler için otomatik kapsül üretilir. "
        "Buradan manuel üretim yapabilir, istatistik görüntüleyebilirsiniz.",
        "info", "📦",
    )

    kapsuller = _load_kapsuller()

    # İstatistik
    toplam = len(kapsuller)
    bugun_str = date.today().isoformat()
    bugun_sayi = sum(1 for k in kapsuller if k.get("tarih") == bugun_str)
    okunan = sum(1 for k in kapsuller if k.get("okundu"))
    okunma_orani = round(okunan / max(toplam, 1) * 100, 1)

    styled_stat_row([
        ("Toplam Kapsül", str(toplam), "#4F46E5", "📦"),
        ("Bugün Üretilen", str(bugun_sayi), "#059669", "📅"),
        ("Okunan", str(okunan), "#D97706", "👁️"),
        ("Okunma Oranı", f"%{okunma_orani}", "#EC4899", "📊"),
    ])

    # Toplu üretim
    st.divider()
    styled_section("🚀 Toplu Kapsül Üret", "#059669")

    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        gen_tarih = st.date_input("Tarih", value=date.today(), key="_kps_yon_tarih_widget")
    with tc2:
        if st.button("🤖 Tüm Öğrenciler İçin Üret", type="primary", use_container_width=True, key="_kps_toplu_gen"):
            try:
                from models.akademik_takip import AkademikDataStore
                ak = AkademikDataStore()
                all_students = ak.get_students(durum="aktif")
            except Exception:
                all_students = []

            if not all_students:
                styled_info_banner("Öğrenci verisi bulunamadı.", "warning")
            else:
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                except Exception:
                    client = None

                progress_bar = st.progress(0)
                status = st.empty()
                tarih_str = gen_tarih.isoformat()
                olusturuldu = 0

                for i, stu in enumerate(all_students[:100]):  # max 100 öğrenci (test)
                    # Zaten var mı?
                    mevcut = next(
                        (k for k in kapsuller if k.get("student_id") == stu.id
                         and k.get("tarih") == tarih_str),
                        None,
                    )
                    if mevcut:
                        continue

                    status.text(f"Hazırlanıyor: {stu.tam_ad} ({i+1}/{len(all_students)})")
                    data = _collect_student_day_data(stu.id, stu.tam_ad, tarih_str)
                    ozet = generate_kapsul_ozet(client, data)

                    kapsuller.append({
                        "id": f"KPS-{len(kapsuller)+1:06d}",
                        "student_id": stu.id,
                        "student_name": stu.tam_ad,
                        "tarih": tarih_str,
                        "data": data,
                        "ozet": ozet,
                        "olusturma_tarihi": datetime.now().isoformat(),
                        "okundu": False,
                    })
                    olusturuldu += 1
                    progress_bar.progress((i + 1) / len(all_students))

                _save_kapsuller(kapsuller)
                status.empty()
                progress_bar.empty()
                st.success(f"✅ {olusturuldu} yeni kapsül üretildi!")
                st.balloons()
                st.rerun()
    with tc3:
        st.markdown("**💡 İpucu**")
        st.caption("Her gün 16:00'da otomatik üretim için cron/scheduler gerekir.")

    # Duygusal ton dağılımı (son 7 gün)
    st.divider()
    styled_section("📊 Duygusal Ton Dağılımı (Son 7 gün)", "#EC4899")

    week_ago = (date.today() - timedelta(days=7)).isoformat()
    recent = [k for k in kapsuller if k.get("tarih", "") >= week_ago]
    ton_counts = {"pozitif": 0, "notr": 0, "dikkat": 0}
    for k in recent:
        t = k.get("ozet", {}).get("duygusal_ton", "notr")
        ton_counts[t] = ton_counts.get(t, 0) + 1

    toplam_ton = sum(ton_counts.values())
    if toplam_ton > 0:
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.metric("😊 Pozitif", ton_counts["pozitif"], f"%{round(ton_counts['pozitif']/toplam_ton*100, 1)}")
        with pc2:
            st.metric("😐 Nötr", ton_counts["notr"], f"%{round(ton_counts['notr']/toplam_ton*100, 1)}")
        with pc3:
            st.metric("⚠️ Dikkat", ton_counts["dikkat"], f"%{round(ton_counts['dikkat']/toplam_ton*100, 1)}")


# ══════════════════════════════════════════════════════════════
# ANA GİRİŞ NOKTASI
# ══════════════════════════════════════════════════════════════

def render_veli_gunluk_kapsul():
    """Ana giriş — rol bazlı."""
    try:
        auth = st.session_state.get("auth_user", {})
        rol = auth.get("role", "").lower()
    except Exception:
        rol = ""

    # Rol bazlı yönlendirme
    if "veli" in rol:
        render_veli_gunluk_kapsul_panel()
    elif any(r in rol for r in ["mudur", "müdür", "yonetici", "kurucu", "admin", "koordinator"]):
        tabs = st.tabs(["👨‍👩‍👧 Veli Görünümü (Test)", "📊 Yönetim"])
        with tabs[0]:
            render_veli_gunluk_kapsul_panel()
        with tabs[1]:
            render_kapsul_yonetim_panel()
    else:
        render_veli_gunluk_kapsul_panel()  # Default veli görünümü
